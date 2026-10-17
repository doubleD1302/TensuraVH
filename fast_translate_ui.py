import os
import sys
import re
import json
import csv
import time
import unicodedata
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

GLOSSARY = {
    # System terms
    "Vitality": "Thể lực",
    "vitality": "thể lực",
    "Stamina": "Thể lực",
    "stamina": "thể lực",
    "Quest": "Nhiệm vụ",
    "Quests": "Nhiệm vụ",
    "Mission": "Nhiệm vụ",
    "Missions": "Nhiệm vụ",
    "Summon": "Triệu hồi",
    "Summons": "Triệu hồi",
    "Gacha": "Triệu hồi",
    "Awakened": "Thức tỉnh",
    "Awakening": "Thức tỉnh",
    "Limit Break": "Phá giới hạn",
    "Evolve": "Tiến hóa",
    "Evolution": "Tiến hóa",
    "Party": "Đội hình",
    "Team": "Đội hình",
    "Equipment": "Trang bị",
    "Inventory": "Túi đồ",
    "Login Bonus": "Quà đăng nhập",
    "Ranking": "Bảng xếp hạng",
    "Soul Lineage": "Phả hệ Linh hồn",
    "Not Cleared": "Chưa hoàn thành",
    "Cleared": "Đã hoàn thành",
    "Remaining Requests": "Yêu cầu còn lại",
    "Unique Interaction": "Tương tác Độc nhất",
    "Unique Skill": "Kỹ năng Độc nhất",
    "Ultimate Skill": "Kỹ năng Tối thượng",
    "Extra Skill": "Kỹ năng Đặc biệt",
    "Common Skill": "Kỹ năng Thường",
    "Great Sage": "Đại Hiền Giả",
    "Predator": "Kẻ Săn Mồi",
    "Magicule": "Ma tố",
    "Magic": "Ma pháp",
    "Hero": "Dũng Giả",
    "Mirror World": "Thế Giới Gương",
    "Valor Cup": "Cúp Dũng Khí",
    "Change Sub Slot": "Đổi ô Phụ",
    "Change Main Slot": "Đổi ô Chính",
    "Confirm": "Xác nhận",
    "Cancel": "Hủy",
    "Close": "Đóng",
    "Back": "Quay lại",
    "Next": "Tiếp",
    "Start": "Bắt đầu",
    "Retry": "Thử lại",
    "Save": "Lưu",
    "Delete": "Xóa",
    "Use": "Sử dụng",
    "Details": "Chi tiết",
    "Settings": "Cài đặt",
    "Notice": "Thông báo",
    "Auto": "Tự động",
    "Skip": "Bỏ qua",
    "Claim": "Nhận",
    "Reward": "Phần thưởng",
    "Rewards": "Phần thưởng",
    "Friend": "Bạn bè",
    "Friends": "Bạn bè",
    "Guild": "Hội",
    "Shop": "Cửa hàng",
}

DELIM = "\n__SEP__\n"

def protect_tags(text):
    tokens = {}
    counter = [0]
    
    def repl(m):
        t = f"PTK{counter[0]}X"
        tokens[t] = m.group(0)
        counter[0] += 1
        return t
        
    pattern = r'(\\[nrt]|\\\"|<[^>]+>|\{[0-9]+(?::[^}]+)?\}|\{[a-zA-Z_0-9]+\}|\[[a-zA-Z_0-9]+\]|\b(?:HP|MP|ATK|DEF|SPD|CRIT)\b)'
    protected = re.sub(pattern, repl, text)
    return protected, tokens

def restore_tags(text, tokens):
    for k, v in tokens.items():
        text = re.sub(rf'\s*{re.escape(k)}\s*', v, text, flags=re.IGNORECASE)
    return text

def post_process_vn(text):
    for k, v in GLOSSARY.items():
        text = re.sub(rf'\b{re.escape(k)}\b', v, text)
    text = re.sub(r'\s+([,.:;?!])', r'\1', text)
    text = text.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    return unicodedata.normalize('NFC', text)

def translate_batch_gtx(texts):
    # Returns list of translated texts
    if not texts:
        return []
    
    # Check glossary first
    results = [None] * len(texts)
    to_translate = []
    to_translate_indices = []
    
    for idx, t in enumerate(texts):
        if not t or not t.strip():
            results[idx] = t
        elif t in GLOSSARY:
            results[idx] = unicodedata.normalize('NFC', GLOSSARY[t])
        else:
            to_translate.append(t)
            to_translate_indices.append(idx)
            
    if not to_translate:
        return results
        
    # Protect tags
    protected_list = []
    tokens_list = []
    for t in to_translate:
        p, toks = protect_tags(t)
        protected_list.append(p)
        tokens_list.append(toks)
        
    joined = DELIM.join(protected_list)
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=' + urllib.parse.quote(joined)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            full_tr = ''.join([part[0] for part in data[0] if part[0]])
            # Split by separator
            parts = [p.strip() for p in re.split(r'\s*__SEP__\s*', full_tr)]
            if len(parts) == len(to_translate):
                for i, orig_idx in enumerate(to_translate_indices):
                    restored = restore_tags(parts[i], tokens_list[i])
                    results[orig_idx] = post_process_vn(restored)
                return results
    except Exception as e:
        pass
        
    # Fallback: translate individually
    for i, orig_idx in enumerate(to_translate_indices):
        p = protected_list[i]
        toks = tokens_list[i]
        try:
            url_single = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=' + urllib.parse.quote(p)
            req_single = urllib.request.Request(url_single, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_single, timeout=8) as r:
                d = json.loads(r.read().decode('utf-8'))
                raw_tr = ''.join([part[0] for part in d[0] if part[0]])
                restored = restore_tags(raw_tr, toks)
                results[orig_idx] = post_process_vn(restored)
        except Exception:
            results[orig_idx] = post_process_vn(to_translate[i])
            
    return results

def main():
    print("Loading ui_terms.json...")
    with open('ui_terms.json', 'r', encoding='utf-8') as f:
        terms = json.load(f)
        
    print(f"Total terms: {len(terms)}")
    unique_strings = list(dict.fromkeys(t.get('en', '').strip() for t in terms if t.get('en', '').strip()))
    print(f"Unique strings to translate: {len(unique_strings)}")
    
    batch_size = 20
    batches = [unique_strings[i:i + batch_size] for i in range(0, len(unique_strings), batch_size)]
    print(f"Total batches: {len(batches)} (size {batch_size})")
    
    t0 = time.time()
    translated_map = {}
    completed_items = 0
    
    def process_batch(b):
        trs = translate_batch_gtx(b)
        return dict(zip(b, trs))
        
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_batch, b) for b in batches]
        for fut in futures:
            res = fut.result()
            translated_map.update(res)
            completed_items += len(res)
            elapsed = time.time() - t0
            rate = completed_items / elapsed if elapsed > 0 else 0
            rem = (len(unique_strings) - completed_items) / rate if rate > 0 else 0
            print(f"Progress: {completed_items}/{len(unique_strings)} ({completed_items/len(unique_strings)*100:.1f}%) | {rate:.1f} str/s | ETA: {rem:.0f}s", flush=True)
            
    # Apply translations back
    for t in terms:
        en = t.get('en', '').strip()
        if en in translated_map and translated_map[en]:
            t['vi'] = translated_map[en]
        else:
            t['vi'] = en
            
    # Save ui_terms.json
    print("Saving ui_terms.json...")
    with open('ui_terms.json', 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)
        
    # Save ui_terms.csv
    print("Saving ui_terms.csv...")
    with open('ui_terms.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'term', 'en', 'vi', 'ja', 'zh'])
        writer.writeheader()
        for row in terms:
            writer.writerow(row)
            
    print(f"Done in {time.time()-t0:.1f}s! All {len(terms)} terms updated.")
    
    # Import into bundle
    print("\n--- Running import_i2_ui.py to repack __data ---")
    import import_i2_ui
    import_i2_ui.import_translations('ui_terms.json')

if __name__ == '__main__':
    main()
