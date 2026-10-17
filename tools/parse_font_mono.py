import struct

with open('tmp_font_mono.bin', 'rb') as f:
    data = f.read()

print(f'Length: {len(data)}')

offset = 0
while offset < len(data):
    if offset + 4 <= len(data):
        val = struct.unpack('<I', data[offset:offset+4])[0]
        # check string
        if 2 < val < 100 and offset + 4 + val <= len(data):
            try:
                s = data[offset+4:offset+4+val].decode('utf-8')
                if all(32 <= ord(c) < 127 for c in s):
                    print(f'Offset {offset:4d} (0x{offset:03x}): str[{val}] = "{s}"')
            except Exception:
                pass
    offset += 4
