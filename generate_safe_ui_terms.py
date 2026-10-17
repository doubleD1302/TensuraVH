import json

# Load ui_terms.json
with open('c:/slime/ui_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

# Comprehensive mapping: unsupported Vietnamese characters -> supported Latin-1 / ASCII
# Preserves: à, á, â, è, é, ê, ì, í, ò, ó, ô, ù, ú, ý (which exist in Common.asset)
safe_map = {
    # a with horns / tones
    'ă': 'a', 'Ă': 'A', 'ằ': 'à', 'Ằ': 'À', 'ắ': 'á', 'Ắ': 'Á', 'ẳ': 'a', 'Ẳ': 'A', 'ẵ': 'a', 'Ẵ': 'A', 'ặ': 'a', 'Ặ': 'A',
    'ầ': 'â', 'Ầ': 'Â', 'ấ': 'â', 'Ấ': 'Â', 'ẩ': 'â', 'Ẩ': 'Â', 'ẫ': 'â', 'Ẫ': 'Â', 'ậ': 'â', 'Ậ': 'Â',
    'ả': 'a', 'Ả': 'A', 'ã': 'a', 'Ã': 'A', 'ạ': 'a', 'Ạ': 'A',
    
    # d
    'đ': 'd', 'Đ': 'D',
    
    # e
    'ẻ': 'e', 'Ẻ': 'E', 'ẽ': 'e', 'Ẽ': 'E', 'ẹ': 'e', 'Ẹ': 'E',
    'ề': 'ê', 'Ề': 'Ê', 'ế': 'ê', 'Ế': 'Ê', 'ể': 'ê', 'Ể': 'Ê', 'ễ': 'ê', 'Ễ': 'Ê', 'ệ': 'ê', 'Ệ': 'Ê',
    
    # i
    'ỉ': 'i', 'Ỉ': 'I', 'ĩ': 'i', 'Ĩ': 'I', 'ị': 'i', 'Ị': 'I',
    
    # o
    'ỏ': 'o', 'Ỏ': 'O', 'õ': 'o', 'Õ': 'O', 'ọ': 'o', 'Ọ': 'O',
    'ồ': 'ô', 'Ồ': 'Ô', 'ố': 'ô', 'Ố': 'Ô', 'ổ': 'ô', 'Ổ': 'Ô', 'ỗ': 'ô', 'Ỗ': 'Ô', 'ộ': 'ô', 'Ộ': 'Ô',
    'ơ': 'o', 'Ơ': 'O', 'ờ': 'o', 'Ờ': 'O', 'ớ': 'o', 'Ớ': 'O', 'ở': 'o', 'Ở': 'O', 'ỡ': 'o', 'Ỡ': 'O', 'ợ': 'o', 'Ợ': 'O',
    
    # u
    'ủ': 'u', 'Ủ': 'U', 'ũ': 'u', 'Ũ': 'U', 'ụ': 'u', 'Ụ': 'U',
    'ư': 'u', 'Ư': 'U', 'ừ': 'u', 'Ừ': 'U', 'ứ': 'u', 'Ứ': 'U', 'ử': 'u', 'Ử': 'U', 'ữ': 'u', 'Ữ': 'U', 'ự': 'u', 'Ự': 'U',
    
    # y
    'ỷ': 'y', 'Ỷ': 'Y', 'ỹ': 'y', 'Ỹ': 'Y', 'ỵ': 'y', 'Ỵ': 'Y', 'ỳ': 'y', 'Ỳ': 'Y',
    
    # currency
    '₫': 'd'
}

count_replaced = 0
for item in terms:
    vi = item.get('vi', '')
    if vi:
        new_vi = ''.join(safe_map.get(c, c) for c in vi)
        if new_vi != vi:
            count_replaced += 1
            item['vi'] = new_vi

print(f"Replaced characters in {count_replaced} terms.")

with open('c:/slime/ui_terms_safe.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, ensure_ascii=False, indent=2)

print("Saved c:/slime/ui_terms_safe.json successfully!")
