import os
import sys
import time
import zipfile
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = '2022.3.62f1'

TARGET_CAB = 'CAB-67016901c4c8650c7761bba7d8915099'
TARGET_PATH_ID = 5214114523134854813

def find_font_bundle(apk_path='split_android_assetpack.apk'):
    print(f'Opening {apk_path}...')
    t0 = time.time()
    with zipfile.ZipFile(apk_path) as z:
        namelist = [n for n in z.namelist() if n.endswith('.bundle')]
        print(f'Total bundles in APK: {len(namelist)}')
        for i, name in enumerate(namelist):
            try:
                data = z.read(name)
                # check if CAB is in data
                if TARGET_CAB.encode('ascii') in data:
                    print(f'\n*** FOUND {TARGET_CAB} in {name}! *** (took {time.time()-t0:.2f}s)')
                    with open('target_font_bundle.bundle', 'wb') as out_f:
                        out_f.write(data)
                    print('Saved bundle to target_font_bundle.bundle')
                    return name, data
            except Exception:
                pass
            if (i + 1) % 200 == 0:
                print(f'Checked {i+1}/{len(namelist)} bundles...', flush=True)
    return None, None

def inspect_bundle(data):
    env = UnityPy.load(data)
    print('\n=== BUNDLE OBJECTS ===')
    for obj in env.objects:
        print(f'Type: {obj.type.name}, PathID: {obj.path_id}')
        try:
            d = obj.read()
            name = getattr(d, 'm_Name', getattr(d, 'name', ''))
            print(f'  Name: {name}')
            if obj.path_id == TARGET_PATH_ID or 'font' in obj.type.name.lower() or 'font' in name.lower():
                tree = obj.read_typetree()
                if isinstance(tree, dict):
                    print(f'  Font Asset details:')
                    print(f'    m_Name: {tree.get("m_Name")}')
                    print(f'    m_AtlasPopulationMode: {tree.get("m_AtlasPopulationMode")}')
                    print(f'    m_CharacterTable count: {len(tree.get("m_CharacterTable", []))}')
                    print(f'    m_GlyphTable count: {len(tree.get("m_GlyphTable", []))}')
                    print(f'    m_AtlasTextures count: {len(tree.get("m_AtlasTextures", []))}')
                    print(f'    m_FallbackFontAssetTable: {tree.get("m_FallbackFontAssetTable")}')
                    print(f'    m_Version: {tree.get("m_Version")}')
        except Exception as e:
            print(f'  Err: {e}')

if __name__ == '__main__':
    name, data = find_font_bundle()
    if data:
        inspect_bundle(data)
