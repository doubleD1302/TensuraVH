import os
import json
import csv
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = '2022.3.62f1'

I2_BUNDLE_PATH = r'com.bandainamcoent.tensuramrkww/files/UnityCache/Shared\baad181fc8596596149644262d31f2a6\b09686f380a54f90be924c34c81ea693\__data'

def export_terms():
    print(f"Loading {I2_BUNDLE_PATH}...")
    env = UnityPy.load(I2_BUNDLE_PATH)
    
    terms_list = []
    
    for obj in env.objects:
        if obj.type.name == 'MonoBehaviour':
            tree = obj.read_typetree()
            src = tree.get('mSource', {})
            mTerms = src.get('mTerms', [])
            
            print(f"Total terms found: {len(mTerms)}")
            for idx, t in enumerate(mTerms):
                langs = t.get('Languages', [])
                ja = langs[0] if len(langs) > 0 else ""
                en = langs[1] if len(langs) > 1 else ""
                zh = langs[2] if len(langs) > 2 else ""
                
                terms_list.append({
                    "id": idx,
                    "term": t.get('Term', ''),
                    "en": en,
                    "ja": ja,
                    "zh": zh,
                    "vi": ""  # To be filled with Vietnamese translation
                })
            break
            
    # Save as JSON
    json_path = 'ui_terms.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(terms_list, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(terms_list)} terms to {json_path}")
    
    # Also save as CSV for easy editing in Excel
    csv_path = 'ui_terms.csv'
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'term', 'en', 'vi', 'ja', 'zh'])
        writer.writeheader()
        for row in terms_list:
            writer.writerow(row)
    print(f"Exported {len(terms_list)} terms to {csv_path}")

if __name__ == '__main__':
    export_terms()
