import os
import sys
import time
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = '2022.3.62f1'

def scan_bundle(path):
    found = []
    try:
        env = UnityPy.load(path)
        # 1. Container check
        for k in env.container.keys():
            kl = k.lower()
            if any(w in kl for w in ['font', 'textmesh', 'mincho', 'gothic', 'serif', 'sans']):
                found.append({'path': path, 'reason': f'container: {k}'})

        # 2. Objects check
        for obj in env.objects:
            tname = obj.type.name
            if tname in ('Font', 'FontAsset'):
                try:
                    d = obj.read()
                    name = getattr(d, 'm_Name', getattr(d, 'name', ''))
                    found.append({'path': path, 'reason': f'Font object: {name}'})
                except Exception:
                    found.append({'path': path, 'reason': f'Font object: (read error)'})
            elif tname == 'MonoScript':
                try:
                    d = obj.read()
                    name = getattr(d, 'm_Name', '')
                    if any(w in name.lower() for w in ['tmp_fontasset', 'fontasset', 'font']):
                        found.append({'path': path, 'reason': f'MonoScript: {name}'})
                except Exception:
                    pass
            elif tname == 'Material':
                try:
                    d = obj.read()
                    name = getattr(d, 'm_Name', '')
                    m_Shader = getattr(d, 'm_Shader', None)
                    sname = ''
                    if m_Shader:
                        try:
                            s = m_Shader.read()
                            sname = getattr(s, 'm_Name', '')
                        except:
                            pass
                    if 'textmesh' in sname.lower() or 'textmesh' in name.lower() or 'font' in name.lower():
                        found.append({'path': path, 'reason': f'Material: {name} (Shader: {sname})'})
                except Exception:
                    pass
            elif tname == 'MonoBehaviour':
                try:
                    # quick raw check for m_CharacterTable or FontAsset
                    raw = obj.get_raw_data()
                    if b'TMP_FontAsset' in raw or b'm_CharacterTable' in raw:
                        found.append({'path': path, 'reason': f'MonoBehaviour with CharacterTable/TMP_FontAsset (path_id {obj.path_id})'})
                except Exception:
                    pass
    except Exception:
        pass
    return found

def main():
    with open('candidates_100k_30m.txt', 'r', encoding='utf-8') as f:
        paths = [line.strip().split('\t')[1] for line in f if '\t' in line]
    
    total = len(paths)
    print(f'Starting scan of {total} candidate bundles with multiprocessing...', flush=True)
    t0 = time.time()
    
    workers = min(os.cpu_count() or 4, 8)
    results = []
    completed = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_bundle, p): p for p in paths}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                results.extend(res)
                for item in res:
                    print(f"[FOUND] {item['reason']} -> {item['path']}", flush=True)
            completed += 1
            if completed % 1000 == 0:
                elapsed = time.time() - t0
                rate = completed / elapsed
                print(f'Progress: {completed}/{total} ({completed/total*100:.1f}%) | {rate:.1f} b/s | Found: {len(results)}', flush=True)

    print(f'Finished scan in {time.time()-t0:.1f}s. Total matches: {len(results)}')
    with open('all_font_matches.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print('Saved to all_font_matches.json')

if __name__ == '__main__':
    main()
