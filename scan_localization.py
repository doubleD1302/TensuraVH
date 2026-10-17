import os
import sys
import time
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = '2022.3.62f1'

KEYWORDS = [
    'i2languages',
    'languagesource',
    'localization',
    'masterlocalization',
    'tmp_font',
    'fontasset',
    '/fonts/',
    '/font/',
    'master_localization',
    'localiz',
    'ui/font',
]

EXCLUDE_EXTS = ('.fbx', '.png', '.wav', '.mp3', '.ogg', '.usm')

def check_bundle(data_path):
    matches = []
    try:
        env = UnityPy.load(data_path)
        container = env.container
        for k in container.keys():
            kl = k.lower()
            if any(kl.endswith(ext) for ext in EXCLUDE_EXTS):
                continue
            if any(w in kl for w in KEYWORDS):
                matches.append({'path': data_path, 'type': 'container', 'name': k})
        
        # Check if container was empty or didn't match, check types
        for obj in env.objects:
            tname = obj.type.name
            if tname == 'MonoBehaviour':
                try:
                    data = obj.read()
                    name = getattr(data, 'name', '') or getattr(data, 'm_Name', '')
                    nl = name.lower()
                    if any(w in nl for w in KEYWORDS) and not any(nl.endswith(ext) for ext in EXCLUDE_EXTS):
                        matches.append({'path': data_path, 'type': 'MonoBehaviour', 'name': name})
                except Exception:
                    pass
            elif tname == 'TextAsset':
                try:
                    data = obj.read()
                    name = getattr(data, 'm_Name', '')
                    nl = name.lower()
                    if any(w in nl for w in KEYWORDS) and not any(nl.endswith(ext) for ext in EXCLUDE_EXTS):
                        matches.append({'path': data_path, 'type': 'TextAsset', 'name': name})
                except Exception:
                    pass
            elif tname in ('Font', 'FontAsset'):
                try:
                    data = obj.read()
                    name = getattr(data, 'm_Name', '')
                    matches.append({'path': data_path, 'type': tname, 'name': name})
                except Exception:
                    pass
    except Exception:
        pass
    return matches

def collect_paths(root):
    paths = []
    for entry in os.scandir(root):
        if not entry.is_dir():
            continue
        for sub in os.scandir(entry.path):
            if sub.is_dir():
                p = os.path.join(sub.path, '__data')
                if os.path.exists(p):
                    paths.append(p)
    return paths

def main():
    root = 'com.bandainamcoent.tensuramrkww/files/UnityCache/Shared'
    print(f"Collecting bundle paths from {root}...")
    paths = collect_paths(root)
    total = len(paths)
    print(f"Total bundles to scan: {total}")
    
    out_file = 'found_localization_bundles.json'
    results = []
    t0 = time.time()
    
    workers = min(os.cpu_count() or 4, 8)
    print(f"Scanning with {workers} workers (optimized filter)...")
    
    completed = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check_bundle, p): p for p in paths}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                results.extend(res)
                for item in res:
                    print(f"[{item['type']}] {item['name']} -> {item['path']}", flush=True)
            completed += 1
            if completed % 2000 == 0:
                elapsed = time.time() - t0
                rate = completed / elapsed
                rem = (total - completed) / rate if rate > 0 else 0
                print(f"Progress: {completed}/{total} ({completed/total*100:.1f}%) | {rate:.1f} b/s | ETA: {rem/60:.1f} min | Matches: {len(results)}", flush=True)
                
    print(f"\nDone! Scanned {total} in {time.time()-t0:.1f}s. Found {len(results)} matches.")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved results to {out_file}")

if __name__ == '__main__':
    main()
