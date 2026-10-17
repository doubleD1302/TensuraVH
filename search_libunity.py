import re

with open(r'c:\slime\libunity.so', 'rb') as f:
    data = f.read()

matches = set(re.findall(rb'/[^\x00"\'\r\n]*global-metadata\.dat', data))
print('global-metadata paths in libunity:', matches)
matches2 = set(re.findall(rb'[A-Za-z0-9_/.]*il2cpp[A-Za-z0-9_/.]*', data))
print(f'il2cpp matches: {len(matches2)}')
for m in list(matches2)[:10]:
    print(' -', m.decode('utf-8', errors='ignore'))
matches3 = set(re.findall(rb'[A-Za-z0-9_/.]*UnityCache[A-Za-z0-9_/.]*', data))
print(f'UnityCache matches: {len(matches3)}')
for m in list(matches3)[:10]:
    print(' -', m.decode('utf-8', errors='ignore'))
