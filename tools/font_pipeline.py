"""Preserve Unicode text; validate the separate game font asset pack.

I2 payload validation does not establish that the installed game's font changed.
The font is read from a signed APK asset pack on the affected Android device.
"""
from copy import deepcopy
from pathlib import Path
import unicodedata

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"
ROOT = Path(__file__).resolve().parents[1]
I2_PATH = ROOT / "com.bandainamcoent.tensuramrkww/files/UnityCache/Shared/baad181fc8596596149644262d31f2a6/b09686f380a54f90be924c34c81ea693/__data"
FONT_CAB = "CAB-67016901c4c8650c7761bba7d8915099"
FONT_PATH_ID = 5214114523134854813
VIETNAMESE = "ĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ₫"


def pointers(value):
    if isinstance(value, dict):
        if "m_FileID" in value and "m_PathID" in value:
            yield value
        else:
            for child in value.values():
                yield from pointers(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from pointers(child)


def language_source(env):
    matches = [(obj, obj.read_typetree()) for obj in env.objects
               if obj.type.name == "MonoBehaviour" and "mSource" in obj.read_typetree()]
    if len(matches) != 1:
        raise ValueError(f"Expected one I2 LanguageSource, found {len(matches)}")
    return matches[0]


def patch_text(env, items):
    obj, tree = language_source(env)
    translations = {i["term"]: unicodedata.normalize("NFC", i.get("vi", ""))
                    for i in items if i.get("vi", "").strip()}
    count = 0
    for term in tree["mSource"]["mTerms"]:
        # Font and material values are asset identifiers, not display text.
        if term["TermType"] != 0 or term["Term"] not in translations:
            continue
        if len(term["Languages"]) < 2:
            raise ValueError(f"English slot missing: {term['Term']}")
        term["Languages"][1] = translations[term["Term"]]
        count += 1
    obj.save_typetree(tree)
    return count


def validate_bundle(path, original_path, items):
    env, original = UnityPy.load(str(path)), UnityPy.load(str(original_path))
    obj, tree = language_source(env)
    _, base = language_source(original)
    expected = {i["term"]: unicodedata.normalize("NFC", i.get("vi", ""))
                for i in items if i.get("vi", "").strip()}
    wanted = deepcopy(base)
    patched = preserved = 0
    for term in wanted["mSource"]["mTerms"]:
        if term["TermType"] == 0 and term["Term"] in expected:
            term["Languages"][1] = expected[term["Term"]]
            patched += 1
        elif term["TermType"] != 0:
            preserved += 1
    if tree != wanted:
        raise ValueError("I2 differs outside canonical English text replacements")
    if [(x.path, x.guid, x.type) for x in obj.assets_file.externals] != [
            (x.path, x.guid, x.type) for x in next(o.assets_file for o in original.objects
             if o.type.name == "MonoBehaviour").externals]:
        raise ValueError("Original font/material dependencies changed")
    return {"scope": "unicode_text_payload_only", "text_terms": patched,
            "asset_terms_preserved": preserved, "nfc": True,
            "font_installation_verified": False}


def validate_font_bundle(path, original_path=ROOT / "primary_font_bundle.bundle"):
    import numpy as np
    env, old_env = UnityPy.load(str(path)), UnityPy.load(str(original_path))
    font = next(o.read_typetree() for o in env.objects if o.path_id == FONT_PATH_ID)
    old = next(o.read_typetree() for o in old_env.objects if o.path_id == FONT_PATH_ID)
    chars = {c["m_Unicode"]: c for c in font["m_CharacterTable"]}
    glyphs = {g["m_Index"]: g for g in font["m_GlyphTable"]}
    for c in old["m_CharacterTable"]:
        if chars.get(c["m_Unicode"]) != c:
            raise ValueError("An original character mapping changed")
    for g in old["m_GlyphTable"]:
        if glyphs.get(g["m_Index"]) != g:
            raise ValueError("An original glyph changed")
    missing = [c for c in VIETNAMESE if ord(c) not in chars]
    if missing or any(c["m_GlyphIndex"] not in glyphs for c in chars.values()):
        raise ValueError(f"Incomplete Vietnamese glyph mapping: {missing}")
    for g in glyphs.values():
        r = g["m_GlyphRect"]
        if min(r.values()) < 0 or r["m_X"] + r["m_Width"] > font["m_AtlasWidth"] or r["m_Y"] + r["m_Height"] > font["m_AtlasHeight"]:
            raise ValueError("Glyph outside atlas")
    new_pixels = np.frombuffer(env.file.files[FONT_CAB + ".resS"].bytes, dtype=np.uint8).reshape(4096, 4096)
    old_pixels = np.frombuffer(old_env.file.files[FONT_CAB + ".resS"].bytes, dtype=np.uint8).reshape(4096, 4096)
    y, x = np.where(new_pixels != old_pixels)
    if not len(x) or not ((x >= 2992) & (x < 3639) & (y >= 3714) & (y < 4095)).all():
        raise ValueError("Atlas edits extend beyond the reserved free region")
    return {"scope": "font_asset_structure_and_atlas", "characters": len(chars),
            "added_characters": len(chars) - len(old["m_CharacterTable"]),
            "missing_vietnamese": [], "original_glyphs_preserved": True,
            "changed_atlas_pixels": len(x), "atlas_edits_within_reserved_region": True}
