import zipfile, json

with zipfile.ZipFile('c:/slime/base.apk', 'r') as z:
    raw = z.read('assets/bin/Data/71873006aabdb4950b61390e22068231')

start = raw.find(b'{"')
end = raw.rfind(b'}')
print(f"start: {start}, end: {end}")
json_str = raw[start:end+1].decode('utf-8', errors='ignore')
data = json.loads(json_str)
bundles = data.get('embedBundles', [])
print(f"Total embed bundles: {len(bundles)}")
for b in bundles[:5]:
    print(b)
for b in bundles:
    if 'd5237ef8' in b.get('internalId', ''):
        print("Found target font bundle in embedBundles:")
        print(b)
