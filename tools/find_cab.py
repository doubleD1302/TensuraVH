import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = '2022.3.62f1'

TARGET_CAB = 'CAB-67016901c4c8650c7761bba7d8915099'

def check_cab(path):
    try:
        env = UnityPy.load(path)
        for k in env.file.files.keys():
            if TARGET_CAB in k:
                return (path, k)
    except Exception:
        pass
    return None

def main():
    with open('candidates_100k_30m.txt', 'r', encoding='utf-8') as f:
        paths = [line.strip().split('\t')[1] for line in f if '\t' in line]
    
    print(f'Searching {len(paths)} candidate bundles for {TARGET_CAB}...', flush=True)
    t0 = time.time()
    
    workers = min(os.cpu_count() or 4, 8)
    found = None
    completed = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check_cab, p): p for p in paths}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                found = res
                print(f'\n*** FOUND TARGET CAB! ***\nBundle: {res[0]}\nCAB: {res[1]}', flush=True)
                # cancel remaining
                for f in futures:
                    f.cancel()
                break
            completed += 1
            if completed % 1000 == 0:
                print(f'Progress: {completed}/{len(paths)} ({completed/len(paths)*100:.1f}%)', flush=True)
                
    if found:
        print(f'Done! Found in {found[0]} after {time.time()-t0:.2f}s')
    else:
        print(f'Done! Not found in local cache after {time.time()-t0:.2f}s')

if __name__ == '__main__':
    main()
