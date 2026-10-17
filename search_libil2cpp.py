import re

with open(r'c:\slime\libil2cpp.so', 'rb') as f:
    data = f.read()

matches = set(re.findall(rb'/[^\x00"\'\r\n]*global-metadata\.dat', data))
print('global-metadata paths in libil2cpp:', matches)
matches2 = [m for m in re.findall(rb'[A-Za-z0-9_/.]*Metadata[A-Za-z0-9_/.]*', data) if len(m) > 5]
print('Metadata matches count:', len(matches2))
for m in matches2[:10]:
    print(' -', m.decode('utf-8', errors='ignore'))
