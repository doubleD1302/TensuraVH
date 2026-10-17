import re

with open(r'c:\slime\base.apk', 'rb') as f:
    data = f.read()

matches = set(re.findall(rb'Assets/[^\x00"\'\r\n]+', data))
fonts = [m.decode('utf-8', errors='ignore') for m in matches if 'font' in m.lower() or 'mincho' in m.lower() or 'tmp' in m.lower()]
print(f"Fonts found in base.apk: {len(fonts)}")
for f in sorted(fonts):
    print(f)
