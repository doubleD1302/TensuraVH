#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_translation.py - Kiem tra ky thuat ban dich Unity (the, bien so, escape, NFC...)

Lop kiem tra TU DONG chay TRUOC Agent 04 (QA Validator). Cac ma loi va muc do
khop voi knowledge/04_unity_technical_rules.md va agents/agent_04_qa_validator.md,
dau ra co cung dinh dang bao cao ({"summary": ..., "reports": [...]}).

Chi dung thu vien chuan cua Python 3.8+.

CACH DUNG
---------
1) Mot file chua ca goc va dich (JSON list / CSV / TSV):
     python validate_translation.py data.json
     python validate_translation.py data.csv --id-col id --src-col source --tr-col translation

   JSON: [{"id": "S01_001", "source": "...", "translation": "...",
           "max_chars": 60, "max_lines": 2}, ...]
   (ten truong khac cung duoc: text/original cho goc; target/translated cho dich)

2) Hai file rieng, ghep theo id/key:
     python validate_translation.py --source jp.json --translation vi.json
   Moi file la JSON list [{"id","text"|"source"|"translation"}] hoac dict {key: text}.

3) Tu kiem tra:
     python validate_translation.py --selftest

TUY CHON CHINH
--------------
  --out report.json        Ghi bao cao JSON (mac dinh chi in ra man hinh)
  --only-problems          Bao cao JSON chi giu dong co loi
  --fail-on LEVEL          blocker (mac dinh) | major | minor | none -> ma thoat 1 neu co loi >= LEVEL
  --font-charset FILE      File txt liet ke cac ky tu font ho tro; ky tu ngoai danh sach -> CHAR_RISK
  --length-mode MODE       raw (mac dinh, tinh ca the) | visible (bo the khi dem max_chars)
  --no-bracket             Khong coi [Ten] la placeholder (neu game dung [..] lam nhan van ban)
  --allow-cjk              Khong bao UNTRANSLATED khi ban dich con chu Nhat/Han
  --fix-nfc OUT.json       Xuat cac ban dich da chuan hoa NFC (chi nhung dong bi thay doi)
  --quiet                  Chi in tom tat

MA THOAT: 0 = dat nguong, 1 = co loi >= --fail-on, 2 = loi dau vao.
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

SEV_RANK = {"INFO": 0, "MINOR": 1, "MAJOR": 2, "BLOCKER": 3}

DEFAULT_SEVERITY = {
    "TAG_MISSING": "BLOCKER", "TAG_EXTRA": "BLOCKER", "TAG_UNCLOSED": "BLOCKER",
    "TAG_MODIFIED": "BLOCKER", "PH_MISSING": "BLOCKER", "PH_EXTRA": "BLOCKER",
    "PH_FORMAT_CHANGED": "BLOCKER", "PH_ORDER": "BLOCKER", "ESC_CHANGED": "BLOCKER",
    "KEY_TRANSLATED": "BLOCKER", "STRUCT_BROKEN": "BLOCKER",
    "ENC_NFD": "MAJOR", "CHAR_RISK": "MAJOR", "OVER_LIMIT": "MAJOR",
    "WS_CHANGED": "MAJOR", "UNTRANSLATED": "MAJOR",
    "PUNCT_STYLE": "MINOR", "SPACING": "MINOR",
}

# ---------------------------------------------------------------------------
# Tokenizer: tach the, placeholder khoi chu thuong
# ---------------------------------------------------------------------------

RE_DOUBLE_ANGLE = re.compile(r"<<[^<>\s]+>>")
RE_TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9_\-]*(?:[=\s][^<>]*)?/?>")
RE_TAG_KEY = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9_\-]*)")

_LATIN_EXT = "A-Za-z0-9_\u00C0-\u1EF9"
PH_PATTERNS = [
    ("pctpct", re.compile(r"%%")),
    ("hash2", re.compile(r"##[A-Za-z_][A-Za-z0-9_]*##")),
    ("brace2", re.compile(r"\{\{[^{}]+\}\}")),
    ("brace", re.compile(r"\{[^{}]*\}")),
    ("pctname", re.compile(r"%[A-Za-z_][A-Za-z0-9_]+%")),
    ("printf", re.compile(
        r"%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?[sdfiuxX](?![" + _LATIN_EXT + r"])")),
    ("dollar", re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*\$")),
    ("at", re.compile(r"@[A-Za-z_][A-Za-z0-9_]*@")),
    ("hashname", re.compile(r"#[A-Za-z_][A-Za-z0-9_]*#")),
    ("bracket", re.compile(r"\[[A-Za-z_][A-Za-z0-9_]*\]")),
]

RE_ESC_LITERAL = re.compile(r'\\[nrt"\\/]|\\u[0-9a-fA-F]{4}')
RE_ENTITY = re.compile(r"&(?:[A-Za-z]+|#\d+|#x[0-9a-fA-F]+);")
RE_CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff66-\uff9f]")
RE_FULLWIDTH_PUNCT = re.compile(r"[\uff0c\u3002\uff01\uff1f\uff1a\uff1b\uff08\uff09\u300c\u300d\u300e\u300f\u3001\u30fb\uff5e]")
RE_EMOJI = re.compile("[\U0001F000-\U0001FAFF]")
RE_SPACE_BEFORE_PUNCT = re.compile(r"(?<=\S) [!?:;,.](?!\.)")
RE_DOUBLE_SPACE = re.compile(r"(?<=\S)  +(?=\S)")

RISK_CHARS = {
    "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
    "\u2014": "-", "\u2013": "-", "\u2026": "...",
}
INVISIBLE = {
    "\u200b": "ZERO WIDTH SPACE", "\u200c": "ZWNJ", "\u200d": "ZWJ",
    "\u2060": "WORD JOINER", "\ufeff": "BOM/ZWNBSP", "\u00ad": "SOFT HYPHEN",
}


def _mask(s, spans, ch):
    if not spans:
        return s
    arr = list(s)
    for a, b in spans:
        for i in range(a, b):
            arr[i] = ch
    return "".join(arr)


class Tokens:
    def __init__(self, text, bracket=True):
        self.text = text
        self.phs = []   # (kind, token, start, end)
        spans = []
        for m in RE_DOUBLE_ANGLE.finditer(text):
            self.phs.append(("angle2", m.group(0), m.start(), m.end()))
            spans.append((m.start(), m.end()))
        masked = _mask(text, spans, "\x01")

        self.tags = []  # (token, start)
        spans = []
        for m in RE_TAG.finditer(masked):
            self.tags.append((m.group(0), m.start()))
            spans.append((m.start(), m.end()))
        masked = _mask(masked, spans, "\x00")

        for kind, rx in PH_PATTERNS:
            if kind == "bracket" and not bracket:
                continue
            spans = []
            for m in rx.finditer(masked):
                self.phs.append((kind, m.group(0), m.start(), m.end()))
                spans.append((m.start(), m.end()))
            masked = _mask(masked, spans, "\x02")
        self.phs.sort(key=lambda x: x[2])
        self.plain = masked   # the = \x00, placeholder = \x02, angle2 = \x01

    def visible_text(self):
        return self.plain.replace("\x00", "")


def tag_key(tok):
    m = RE_TAG_KEY.match(tok)
    return (m.group(1), m.group(2).lower()) if m else ("", tok)


def ph_base(kind, tok):
    if kind == "brace":
        return "{" + tok[1:-1].split(":")[0].strip() + "}"
    return tok


# ---------------------------------------------------------------------------
# Cac phep kiem tra
# ---------------------------------------------------------------------------

def snip(s, n=150):
    s = s.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return s if len(s) <= n else s[: n - 3] + "..."


def balance_errors(tags, closer_names):
    stack, errs = [], []
    for tok, _ in tags:
        closing, name = tag_key(tok)
        if name not in closer_names or tok.endswith("/>"):
            continue
        if not closing:
            stack.append(name)
        else:
            if stack and stack[-1] == name:
                stack.pop()
            elif name in stack:
                errs.append("Thẻ </%s> đóng sai thứ tự lồng." % name)
                while stack and stack.pop() != name:
                    pass
            else:
                errs.append("Thẻ </%s> không có thẻ mở tương ứng." % name)
    for name in stack:
        errs.append("Thẻ <%s> mở nhưng chưa được đóng." % name)
    return errs


def check_tags(S, T, add):
    sc = Counter(t for t, _ in S.tags)
    tc = Counter(t for t, _ in T.tags)
    missing = list((sc - tc).elements())
    extra = list((tc - sc).elements())

    # Cung ten the nhung khac noi dung -> TAG_MODIFIED
    for m in list(missing):
        for e in list(extra):
            if tag_key(m) == tag_key(e):
                add("TAG_MODIFIED", "Gốc: %s — Dịch: %s" % (m, e),
                    "Nội dung thẻ bị sửa (mã màu, số hoặc ID).",
                    "Khôi phục đúng %s." % m)
                missing.remove(m)
                extra.remove(e)
                break

    for tok, n in Counter(missing).items():
        add("TAG_MISSING", "Gốc có %s ×%d, bản dịch thiếu." % (tok, n),
            "Bản dịch thiếu thẻ so với gốc.", "Thêm lại %s." % tok)
    for tok, n in Counter(extra).items():
        add("TAG_EXTRA", "Bản dịch có thêm %s ×%d." % (tok, n),
            "Bản dịch thừa thẻ không có ở gốc.", "Xóa %s." % tok)

    closers = {tag_key(t)[1] for t, _ in S.tags + T.tags if tag_key(t)[0] == "/"}
    if not balance_errors(S.tags, closers):
        for err in balance_errors(T.tags, closers):
            add("TAG_UNCLOSED", snip(T.text), err, "Sửa lại cặp thẻ mở/đóng cho cân bằng và lồng đúng thứ tự.")


def check_placeholders(S, T, add):
    sp = [(k, t) for k, t, _, _ in S.phs]
    tp = [(k, t) for k, t, _, _ in T.phs]
    sc, tc = Counter(t for _, t in sp), Counter(t for _, t in tp)
    kind_of = {t: k for k, t in sp + tp}

    missing = list((sc - tc).elements())
    extra = list((tc - sc).elements())
    for m in list(missing):
        bm = ph_base(kind_of[m], m)
        for e in list(extra):
            if ph_base(kind_of[e], e) == bm and kind_of[m] == kind_of[e]:
                add("PH_FORMAT_CHANGED", "Gốc: %s — Dịch: %s" % (m, e),
                    "Định dạng sau dấu ':' của biến số bị đổi.", "Khôi phục đúng %s." % m)
                missing.remove(m)
                extra.remove(e)
                break
    for tok, n in Counter(missing).items():
        add("PH_MISSING", "Gốc có %s ×%d, bản dịch thiếu." % (tok, n),
            "Thiếu placeholder (biến số).", "Thêm lại %s vào đúng chỗ trong câu." % tok)
    for tok, n in Counter(extra).items():
        add("PH_EXTRA", "Bản dịch có thêm %s ×%d." % (tok, n),
            "Thừa placeholder hoặc biến số bị thay bằng giá trị cố định.", "Xóa hoặc khôi phục biến số gốc.")

    # printf khong chi so: thu tu phai giu nguyen
    s_seq = [t for k, t in sp if k == "printf" and "$" not in t]
    t_seq = [t for k, t in tp if k == "printf" and "$" not in t]
    if s_seq != t_seq and Counter(s_seq) == Counter(t_seq):
        add("PH_ORDER", "Gốc: %s — Dịch: %s" % (" ".join(s_seq), " ".join(t_seq)),
            "Thứ tự printf không có chỉ số bị đổi, sẽ gán sai đối số.",
            "Viết lại câu để giữ thứ tự %s hoặc dùng dạng có chỉ số nếu game cho phép." % " → ".join(s_seq))

    # Ky tu dinh lien: {0}%  +{0}  x{0}
    def attached(tokens):
        c = Counter()
        for _, tok, a, b in tokens.phs:
            if b < len(tokens.text) and tokens.text[b] == "%":
                c[(tok, "right%")] += 1
            if a > 0 and tokens.text[a - 1] in "xX\u00d7+":
                c[(tokens.text[a - 1] + tok)] += 1
        return c
    lost = attached(S) - attached(T)
    if lost:
        names = []
        for k in lost:
            names.append(k[0] + "%" if isinstance(k, tuple) else k)
        add("WS_CHANGED", "Mất ký tự dính liền: " + ", ".join(names),
            "Ký tự dính liền với biến số bị tách hoặc mất.", "Giữ nguyên dạng " + ", ".join(names) + " (không chèn khoảng trắng).")


def esc_profile(s):
    c = Counter()
    c["xuống dòng thật (LF)"] = s.count("\n")
    c["CR"] = s.count("\r")
    c["TAB thật"] = s.count("\t")
    for m in RE_ESC_LITERAL.finditer(s):
        c[m.group(0)] += 1
    for m in RE_ENTITY.finditer(s):
        c[m.group(0)] += 1
    return +c


def check_escapes(src, tr, add):
    sp, tp = esc_profile(src), esc_profile(tr)
    if sp != tp:
        parts = []
        for k in sorted(set(sp) | set(tp)):
            if sp.get(k, 0) != tp.get(k, 0):
                parts.append("%s: gốc %d, dịch %d" % (k, sp.get(k, 0), tp.get(k, 0)))
        add("ESC_CHANGED", "; ".join(parts), "Ký tự điều khiển/escape/entity khác bản gốc.",
            "Giữ nguyên số lượng và dạng \\n, \\t, xuống dòng và &entity; như gốc.")


def check_edges(src, tr, add):
    ws = " \t\u3000\u00a0"
    sl = src[: len(src) - len(src.lstrip(ws))]
    sr = src[len(src.rstrip(ws)):]
    tl = tr[: len(tr) - len(tr.lstrip(ws))]
    trr = tr[len(tr.rstrip(ws)):]
    if sl != tl or sr != trr:
        sev = "MAJOR" if (sl or sr) else "MINOR"
        add("WS_CHANGED", "Gốc: %r…%r — Dịch: %r…%r" % (sl, sr, tl, trr),
            "Khoảng trắng đầu/cuối chuỗi khác bản gốc.", "Đặt khoảng trắng đầu/cuối giống gốc.", severity=sev)


def check_text_quality(src, tr, S, T, opts, add):
    # NFC
    if unicodedata.normalize("NFC", tr) != tr:
        add("ENC_NFD", snip(tr), "Chữ tiếng Việt chưa ở dạng NFC (dấu bị tách rời).",
            "Chuẩn hóa Unicode về NFC (dùng --fix-nfc).")

    # Ky tu rui ro font
    found = sorted({c for c in tr if c in RISK_CHARS})
    if found:
        add("CHAR_RISK", "Ký tự: " + " ".join("%s(U+%04X)" % (c, ord(c)) for c in found),
            "Ký tự có thể thiếu trong font game, dễ hiện ô vuông.",
            "Thay: " + ", ".join("%s → %s" % (c, RISK_CHARS[c]) for c in found))
    inv = sorted({c for c in tr if c in INVISIBLE})
    if inv:
        add("CHAR_RISK", "Ký tự vô hình: " + ", ".join("%s(U+%04X)" % (INVISIBLE[c], ord(c)) for c in inv),
            "Ký tự vô hình có thể làm lệch ngắt dòng/hiển thị.", "Xóa các ký tự vô hình.")
    emo = sorted({c for c in tr if RE_EMOJI.match(c) and c not in src})
    if emo:
        add("CHAR_RISK", "Emoji: " + " ".join(emo), "Emoji không có ở gốc và font thường không hỗ trợ.", "Xóa emoji.")
    if opts.charset:
        bad = sorted({c for c in tr if ord(c) > 127 and not c.isspace() and c not in opts.charset})
        if bad:
            add("CHAR_RISK", "Ngoài font: " + " ".join("%s(U+%04X)" % (c, ord(c)) for c in bad[:20]),
                "Có ký tự không nằm trong danh sách ký tự font hỗ trợ.",
                "Thay bằng ký tự có trong font hoặc bổ sung vào font atlas.")

    # Chu Nhat con sot
    if not opts.allow_cjk:
        cjk = RE_CJK.findall(T.plain)
        if cjk:
            add("UNTRANSLATED", "Còn chữ Nhật/Hán: " + "".join(dict.fromkeys(cjk))[:30],
                "Bản dịch còn sót chữ Nhật/Hán chưa dịch.", "Dịch nốt phần còn sót.")
    plain_src = S.plain.strip(" \x00\x01\x02\n\r\t\u3000")
    plain_tr = T.plain.strip(" \x00\x01\x02\n\r\t\u3000")
    if plain_src and not plain_tr:
        add("UNTRANSLATED", "Bản dịch rỗng (hoặc chỉ có thẻ/biến số).",
            "Gốc có chữ nhưng bản dịch không có nội dung.", "Điền bản dịch.")

    # Dau cau / khoang trang (MINOR)
    fw = sorted(set(RE_FULLWIDTH_PUNCT.findall(T.plain)))
    if fw:
        add("PUNCT_STYLE", "Dấu toàn角: " + " ".join(fw), "Dấu câu kiểu Nhật chưa đổi sang dấu Việt/ASCII.",
            "Đổi sang dấu thường (, . ! ? : ;) hoặc \" '.")
    vis = T.plain.replace("\x00", "")
    if RE_SPACE_BEFORE_PUNCT.search(vis):
        m = RE_SPACE_BEFORE_PUNCT.search(vis)
        add("SPACING", snip(vis[max(0, m.start() - 12): m.end() + 6]), "Có khoảng trắng thừa trước dấu câu.",
            "Bỏ khoảng trắng trước ! ? : ; , .")
    if RE_DOUBLE_SPACE.search(vis):
        m = RE_DOUBLE_SPACE.search(vis)
        add("SPACING", snip(vis[max(0, m.start() - 12): m.end() + 6]), "Có hai khoảng trắng liên tiếp.", "Chỉ giữ một khoảng trắng.")


def check_limits(item, tr, T, opts, add):
    mc, ml = item.get("max_chars"), item.get("max_lines")
    if mc not in (None, ""):
        try:
            mc = int(mc)
            n = len(tr) if opts.length_mode == "raw" else len(T.visible_text())
            if n > mc:
                add("OVER_LIMIT", "%d ký tự (%s) > max_chars=%d" % (n, opts.length_mode, mc),
                    "Vượt giới hạn ký tự.", "Rút gọn theo file 03 mục 6 (không cắt thẻ/biến số).")
        except ValueError:
            pass
    if ml not in (None, ""):
        try:
            ml = int(ml)
            lines = tr.count("\n") + len(re.findall(r"\\n", tr)) + 1
            if lines > ml:
                add("OVER_LIMIT", "%d dòng > max_lines=%d" % (lines, ml), "Vượt giới hạn số dòng.",
                    "Rút gọn câu hoặc giữ đúng số dòng của gốc.")
        except ValueError:
            pass


def validate_item(item, opts):
    issues = []

    def add(code, evidence, explanation, fix="", severity=None):
        issues.append({
            "code": code,
            "severity": severity or DEFAULT_SEVERITY[code],
            "category": "technical",
            "evidence": evidence,
            "explanation": explanation,
            "fix": fix,
        })

    src, tr = item.get("source"), item.get("translation")
    if src is None or tr is None:
        add("STRUCT_BROKEN", "Thiếu %s." % ("bản gốc" if src is None else "bản dịch"),
            "Dòng không có đủ cặp gốc/dịch.", "Bổ sung dòng còn thiếu.")
        return issues
    src, tr = str(src), str(tr)

    S, T = Tokens(src, opts.bracket), Tokens(tr, opts.bracket)
    check_tags(S, T, add)
    check_placeholders(S, T, add)
    check_escapes(src, tr, add)
    check_edges(src, tr, add)
    check_text_quality(src, tr, S, T, opts, add)
    check_limits(item, tr, T, opts, add)
    return issues


def verdict_of(issues):
    sev = {i["severity"] for i in issues}
    if "BLOCKER" in sev:
        return "FAIL"
    if "MAJOR" in sev:
        return "REVISE"
    return "PASS"


# ---------------------------------------------------------------------------
# Doc du lieu dau vao
# ---------------------------------------------------------------------------

SRC_NAMES = ["source", "text", "original", "src"]
TR_NAMES = ["translation", "target", "translated", "vi"]


def first(obj, names, override=None):
    if override and override in obj:
        return obj[override]
    for n in names:
        if n in obj:
            return obj[n]
    return None


def read_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def entries_from_json(data, id_field):
    """-> list of (id, obj) ; obj la dict hoac chuoi."""
    if isinstance(data, dict):
        for k in ("lines", "items", "entries", "data"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    out = []
    if isinstance(data, list):
        for i, o in enumerate(data):
            if isinstance(o, dict):
                out.append((str(o.get(id_field, o.get("key", i))), o))
            else:
                out.append((str(i), o))
    elif isinstance(data, dict):
        for k, v in data.items():
            out.append((str(k), v))
    else:
        raise ValueError("JSON phải là list hoặc dict.")
    return out


def entries_from_csv(path, id_col):
    delim = "\t" if path.lower().endswith(".tsv") else ","
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=delim))
    return [(str(r.get(id_col, i)), r) for i, r in enumerate(rows)]


def load_entries(path, id_field):
    if path.lower().endswith((".csv", ".tsv")):
        return entries_from_csv(path, id_field)
    return entries_from_json(read_json(path), id_field)


def text_of(obj, names, override=None):
    if isinstance(obj, dict):
        return first(obj, names, override)
    return obj


def build_items(args):
    items, extra_reports = [], []
    if args.source and args.translation:
        src_e = load_entries(args.source, args.id_field)
        tr_e = load_entries(args.translation, args.id_field)
        tr_map = {}
        for k, o in tr_e:
            tr_map[k] = o
        src_ids = [k for k, _ in src_e]
        missing = [k for k in src_ids if k not in tr_map]
        extra = [k for k, _ in tr_e if k not in set(src_ids)]
        renamed = bool(missing) and len(missing) == len(extra)
        for k, o in src_e:
            if k in tr_map:
                to = tr_map[k]
                tr_text = text_of(to, TR_NAMES + SRC_NAMES, args.tr_col)
                it = {"id": k, "source": text_of(o, SRC_NAMES, args.src_col), "translation": tr_text}
                if isinstance(o, dict):
                    for lim in ("max_chars", "max_lines"):
                        if lim in o:
                            it[lim] = o[lim]
                items.append(it)
        for k in missing:
            code = "KEY_TRANSLATED" if renamed else "STRUCT_BROKEN"
            msg = "Key '%s' có ở gốc nhưng không có ở bản dịch." % k
            extra_reports.append({"id": k, "issues": [mk(code, msg, "Thiếu key" + (" (có thể key đã bị dịch/đổi tên)." if renamed else "."),
                                                      "Khôi phục đúng key gốc.")]})
        for k in extra:
            code = "KEY_TRANSLATED" if renamed else "STRUCT_BROKEN"
            extra_reports.append({"id": k, "issues": [mk(code, "Key '%s' có ở bản dịch nhưng không có ở gốc." % k,
                                                      "Key lạ trong bản dịch.", "Xóa hoặc đổi lại đúng key gốc.")]})
        if len(src_ids) != len(set(src_ids)):
            extra_reports.append({"id": "(file gốc)", "issues": [mk("STRUCT_BROKEN", "Có id trùng lặp ở file gốc.", "Id không duy nhất.", "Kiểm tra lại dữ liệu.")]})
    else:
        for k, o in load_entries(args.file, args.id_field):
            if not isinstance(o, dict):
                continue
            it = {"id": k,
                  "source": first(o, SRC_NAMES, args.src_col),
                  "translation": first(o, TR_NAMES, args.tr_col)}
            for lim in ("max_chars", "max_lines"):
                if lim in o:
                    it[lim] = o[lim]
            items.append(it)
    return items, extra_reports


def mk(code, evidence, explanation, fix, severity=None):
    return {"code": code, "severity": severity or DEFAULT_SEVERITY[code], "category": "technical",
            "evidence": evidence, "explanation": explanation, "fix": fix}


# ---------------------------------------------------------------------------
# Chay + bao cao
# ---------------------------------------------------------------------------

def run(items, extra_reports, opts):
    reports = []
    for it in items:
        issues = validate_item(it, opts)
        reports.append({"id": it["id"], "verdict": verdict_of(issues), "issues": issues, "suggested_translation": None})
    for r in extra_reports:
        r["verdict"] = verdict_of(r["issues"])
        r["suggested_translation"] = None
        reports.append(r)
    allsev = Counter(i["severity"] for r in reports for i in r["issues"])
    summary = {
        "total": len(reports),
        "pass": sum(r["verdict"] == "PASS" for r in reports),
        "revise": sum(r["verdict"] == "REVISE" for r in reports),
        "fail": sum(r["verdict"] == "FAIL" for r in reports),
        "blockers": allsev.get("BLOCKER", 0),
        "majors": allsev.get("MAJOR", 0),
        "minors": allsev.get("MINOR", 0),
    }
    return {"summary": summary, "reports": reports}


def print_report(report, quiet):
    s = report["summary"]
    if not quiet:
        for r in report["reports"]:
            if not r["issues"]:
                continue
            print("[%s] %s" % (r["verdict"], r["id"]))
            for i in r["issues"]:
                print("   - %-8s %-18s %s" % (i["severity"], i["code"], i["evidence"]))
                print("       %s" % i["explanation"])
    print("-" * 60)
    print("Tổng %d dòng | PASS %d | REVISE %d | FAIL %d | BLOCKER %d | MAJOR %d | MINOR %d" % (
        s["total"], s["pass"], s["revise"], s["fail"], s["blockers"], s["majors"], s["minors"]))


def exit_code(report, fail_on):
    if fail_on == "none":
        return 0
    thr = SEV_RANK[fail_on.upper()]
    for r in report["reports"]:
        for i in r["issues"]:
            if SEV_RANK[i["severity"]] >= thr:
                return 1
    return 0


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

SELFTESTS = [
    ("OK the mau + bien so",
     "<color=#FFCC00>リムル</color>は{0}のダメージを受けた！",
     "<color=#FFCC00>Rimuru</color> đã chịu {0} sát thương!", set()),
    ("Thieu </color> va mat {0}",
     "<color=#FFCC00>リムル</color>は{0}のダメージを受けた！",
     "<color=#FFCC00>Rimuru đã chịu 0 sát thương!", {"TAG_MISSING", "TAG_UNCLOSED", "PH_MISSING"}),
    ("Ma mau bi cut",
     "<color=#FFCC00>リムル</color>は{0}のダメージ",
     "<color=#FFCC0>Rimuru</color> chịu {0} sát thương", {"TAG_MODIFIED"}),
    ("Them the la",
     "HP+{0}", "<b>HP</b>+{0}", {"TAG_EXTRA", }),
    ("Long sai thu tu",
     "<b><i>強い</i></b>", "<b><i>Mạnh</b></i>", {"TAG_UNCLOSED"}),
    ("Doi dinh dang {0:N0}",
     "{0:N0}ゴールド", "{0} vàng", {"PH_FORMAT_CHANGED"}),
    ("printf giu thu tu",
     "%sは%dレベルになった", "%s đã đạt cấp %d", set()),
    ("printf doi thu tu",
     "%sは%dレベルになった", "Cấp %d của %s", {"PH_ORDER"}),
    ("{0}% hop le (khong bat nham '% s')",
     "敵に{0}%のダメージ", "Gây {0}% sát thương", set()),
    ("Tach {0} %",
     "<b>HP</b> +{0}%", "<b>HP</b> + {0} %", {"WS_CHANGED"}),
    ("Mat \\n literal",
     "確認\\n本当に削除しますか？", "Xác nhận Bạn có chắc muốn xóa không?", {"ESC_CHANGED"}),
    ("Giu \\n literal",
     "確認\\n本当に削除しますか？", "Xác nhận\\nBạn có chắc muốn xóa không?", set()),
    ("Mat [PlayerName]",
     "[PlayerName]さん、ようこそ", "Chào mừng bạn", {"PH_MISSING"}),
    ("{{name}} giu nguyen",
     "{{name}}が来た", "{{name}} đã đến", set()),
    ("NFD",
     "確認", "Xa\u0301c nhận", {"ENC_NFD"}),
    ("Ky tu rui ro font",
     "ふむ…", "Hừm… “được rồi” — xong", {"CHAR_RISK"}),
    ("Qua gioi han ky tu",
     "確認", "Xác nhận hành động rất dài dòng", {"OVER_LIMIT"}),
    ("Con chu Nhat",
     "確認する", "Xác nhận する", {"UNTRANSLATED"}),
    ("Khoang trang truoc dau cau",
     "こんにちは", "Xin chào !", {"SPACING"}),
    ("Sprite giu nguyen",
     "<sprite=3>{0}獲得", "<sprite=3>{0} nhận được", set()),
    ("Entity giu nguyen",
     "A&nbsp;B", "A&nbsp;B", set()),
    ("Entity bi mat",
     "A&nbsp;B", "A B", {"ESC_CHANGED"}),
]


def run_selftest():
    class O:
        bracket = True
        allow_cjk = False
        charset = None
        length_mode = "raw"
    ok = True
    for name, src, tr, expected in SELFTESTS:
        item = {"id": name, "source": src, "translation": tr}
        if "gioi han ky tu" in name:
            item["max_chars"] = 12
        got = {i["code"] for i in validate_item(item, O)}
        status = "OK  " if got == expected else "LỖI "
        if got != expected:
            ok = False
        print("%s %-45s mong đợi=%s nhận=%s" % (status, name, sorted(expected), sorted(got)))
    print("=> SELFTEST " + ("ĐẠT" if ok else "KHÔNG ĐẠT"))
    return 0 if ok else 1


# ---------------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(description="Kiểm tra kỹ thuật bản dịch Unity (thẻ, biến số, escape, NFC...).")
    p.add_argument("file", nargs="?", help="File JSON/CSV/TSV chứa cả gốc và dịch.")
    p.add_argument("--source", help="File gốc (chế độ hai file).")
    p.add_argument("--translation", help="File dịch (chế độ hai file).")
    p.add_argument("--id-field", "--id-col", dest="id_field", default="id")
    p.add_argument("--src-col", default=None, help="Tên trường/cột chứa bản gốc.")
    p.add_argument("--tr-col", default=None, help="Tên trường/cột chứa bản dịch.")
    p.add_argument("--out", help="Ghi báo cáo JSON.")
    p.add_argument("--only-problems", action="store_true")
    p.add_argument("--fail-on", default="blocker", choices=["blocker", "major", "minor", "none"])
    p.add_argument("--font-charset", help="File txt liệt kê ký tự font hỗ trợ.")
    p.add_argument("--length-mode", default="raw", choices=["raw", "visible"])
    p.add_argument("--no-bracket", dest="bracket", action="store_false")
    p.add_argument("--allow-cjk", action="store_true")
    p.add_argument("--fix-nfc", metavar="OUT.json")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if args.selftest:
        return run_selftest()

    if not args.file and not (args.source and args.translation):
        p.print_usage(sys.stderr)
        print("Cần một file đầu vào, hoặc cả --source và --translation.", file=sys.stderr)
        return 2

    args.charset = None
    if args.font_charset:
        try:
            args.charset = set(Path(args.font_charset).read_text(encoding="utf-8-sig"))
        except OSError as e:
            print("Không đọc được --font-charset: %s" % e, file=sys.stderr)
            return 2

    try:
        items, extra_reports = build_items(args)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print("Lỗi đọc dữ liệu: %s" % e, file=sys.stderr)
        return 2
    if not items and not extra_reports:
        print("Không tìm thấy dòng nào để kiểm tra.", file=sys.stderr)
        return 2

    report = run(items, extra_reports, args)
    print_report(report, args.quiet)

    if args.out:
        out = dict(report)
        if args.only_problems:
            out["reports"] = [r for r in report["reports"] if r["issues"]]
        Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Đã ghi báo cáo: %s" % args.out)

    if args.fix_nfc:
        fixed = []
        for it in items:
            tr = it.get("translation")
            if isinstance(tr, str) and unicodedata.normalize("NFC", tr) != tr:
                fixed.append({"id": it["id"], "translation": unicodedata.normalize("NFC", tr)})
        Path(args.fix_nfc).write_text(json.dumps(fixed, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Đã ghi %d dòng chuẩn hóa NFC: %s" % (len(fixed), args.fix_nfc))

    return exit_code(report, args.fail_on)


if __name__ == "__main__":
    sys.exit(main())
