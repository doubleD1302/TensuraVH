import os
import shutil
import json
import csv
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = '2022.3.62f1'

I2_BUNDLE_PATH = r'com.bandainamcoent.tensuramrkww/files/UnityCache/Shared\baad181fc8596596149644262d31f2a6\b09686f380a54f90be924c34c81ea693\__data'

def import_translations(translation_source='ui_terms.json'):
    # Backup original __data if not already backed up
    bak_path = I2_BUNDLE_PATH + '.bak'
    if not os.path.exists(bak_path):
        print(f"Creating backup: {bak_path}")
        shutil.copy2(I2_BUNDLE_PATH, bak_path)
    else:
        print(f"Backup already exists: {bak_path}")
        
    # Read translations
    translations = {}
    if translation_source.endswith('.json'):
        with open(translation_source, 'r', encoding='utf-8') as f:
            items = json.load(f)
            for item in items:
                vi = item.get('vi', '').strip()
                if vi:
                    translations[item['term']] = vi
    elif translation_source.endswith('.csv'):
        with open(translation_source, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vi = row.get('vi', '').strip()
                if vi:
                    translations[row['term']] = vi
                    
    print(f"Loaded {len(translations)} translated terms to import.")
    if not translations:
        print("No translations found in source file!")
        return

    # Load bundle from backup so we always patch from clean original
    print(f"Loading base bundle from backup {bak_path}...")
    env = UnityPy.load(bak_path)
    
    patched_count = 0
    for obj in env.objects:
        if obj.type.name == 'MonoBehaviour':
            tree = obj.read_typetree()
            src = tree.get('mSource', {})
            mTerms = src.get('mTerms', [])
            
            for t in mTerms:
                term_key = t.get('Term', '')
                if term_key in translations:
                    vi_text = translations[term_key]
                    langs = t.get('Languages', [])
                    if len(langs) > 1:
                        langs[1] = vi_text  # Replace English (index 1) with Vietnamese
                        patched_count += 1
                        
            # Save modified typetree
            obj.save_typetree(tree)
            break
            
    print(f"Patched {patched_count} terms into LanguageSourceData.")
    
    # Save back to __data
    print(f"Saving modified bundle to {I2_BUNDLE_PATH}...")
    saved_bytes = env.file.save()
    with open(I2_BUNDLE_PATH, 'wb') as f:
        f.write(saved_bytes)
        
    print(f"SUCCESS! Repacked AssetBundle saved ({len(saved_bytes)} bytes).")

if __name__ == '__main__':
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else 'ui_terms.json'
    import_translations(src)
