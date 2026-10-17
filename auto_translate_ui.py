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

# Load glossary rules
GLOSSARY = {
    # Systems & UI
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
}

def protect_tags(text):
    tokens = {}
    counter = [0]
    
    def repl(m):
        t = f"___T{counter[0]}X___"
        tokens[t] = m.group(0)
        counter[0] += 1
        return t
        
    pattern = r'(\\[nrt]|\\\"|<[^>]+>|\{[0-9]+(?::[^}]+)?\}|\{[a-zA-Z_0-9]+\}|\[[a-zA-Z_0-9]+\]|\b(?:HP|MP|ATK|DEF|SPD|CRIT)\b)'
    protected = re.sub(pattern, repl, text)
    return protected, tokens

def restore_tags(text, tokens):
    for k, v in tokens.items():
        # Match token with optional surrounding spaces that translator might add
        text = re.sub(rf'\s*{re.escape(k)}\s*', v, text, flags=re.IGNORECASE)
    return text

def translate_gtx(text):
    if not text.strip():
        return text
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=' + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        return ''.join([part[0] for part in res[0]])

def post_process_vn(text):
    # Apply glossary
    for k, v in GLOSSARY.items():
        # Case sensitive word boundary replacement
        text = re.sub(rf'\b{re.escape(k)}\b', v, text)
    
    # Clean up punctuation spacing
    text = re.sub(r'\s+([,.:;?!])', r'\1', text)
    # Ensure quotes are standard ASCII
    text = text.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    # Normalize to Unicode NFC
    text = unicodedata.normalize('NFC', text)
    return text

def translate_single(text):
    if not text or not text.strip():
        return text
    
    # Check exact glossary match
    if text in GLOSSARY:
        return unicodedata.normalize('NFC', GLOSSARY[text])
        
    protected, tokens = protect_tags(text)
    try:
        raw_tr = translate_gtx(protected)
        restored = restore_tags(raw_tr, tokens)
        final = post_process_vn(restored)
        return final
    except Exception as e:
        # Fallback to glossary or original if translation fails
        return post_process_vn(text)

def main():
    print("Loading ui_terms.json...")
    with open('ui_terms.json', 'r', encoding='utf-8') as f:
        terms = json.load(f)
        
    print(f"Total terms: {len(terms)}")
    
    # Collect unique English strings
    unique_map = {}
    for t in terms:
        en = t.get('en', '').strip()
        if en and en not in unique_map:
            unique_map[en] = ""
            
    print(f"Unique strings to translate: {len(unique_map)}")
    
    # Translate with ThreadPoolExecutor
    t0 = time.time()
    translated_map = {}
    
    items = list(unique_map.keys())
    batch_size = 10
    
    def worker(chunk):
        res = {}
        for s in chunk:
            res[s] = translate_single(s)
            time.sleep(0.05)  # slight pause to be gentle
        return res

    chunks = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    print(f"Translating in {len(chunks)} chunks with 4 workers...")
    
    done_count = 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker, c) for c in chunks]
        for fut in futures:
            res = fut.result()
            translated_map.update(res)
            done_count += len(res)
            if done_count % 200 == 0 or done_count == len(items):
                elapsed = time.time() - t0
                rate = done_count / elapsed if elapsed > 0 else 0
                rem = (len(items) - done_count) / rate if rate > 0 else 0
                print(f"Progress: {done_count}/{len(items)} ({done_count/len(items)*100:.1f}%) | {rate:.1f} str/s | ETA: {rem/60:.1f}m")
                
    # Fill back into terms
    for t in terms:
        en = t.get('en', '').strip()
        if en in translated_map:
            t['vi'] = translated_map[en]
        else:
            t['vi'] = en
            
    # Save back to ui_terms.json
    print("Saving to ui_terms.json...")
    with open('ui_terms.json', 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)
        
    # Save back to ui_terms.csv
    print("Saving to ui_terms.csv...")
    with open('ui_terms.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'term', 'en', 'vi', 'ja', 'zh'])
        writer.writeheader()
        for row in terms:
            writer.writerow(row)
            
    print(f"All {len(terms)} terms translated and saved in {time.time()-t0:.1f}s!")

if __name__ == '__main__':
    main()
