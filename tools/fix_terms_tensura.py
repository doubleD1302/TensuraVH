import json, re

print("=== Fixing Mistranslations & Mixed English in ui_terms.json ===")

with open('ui_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

# Comprehensive dictionary of term fixes based on Tensura Light Novel / Anime canon
FIXES = {
    # Loup Loupe / Mirror Realm
    '22e67390d5a33c608c5eb12452d15f7b': 'Ảo Kính Ma Cảnh',
    
    # Eiketsu-hai / Valor Cup
    '4a667ef79a8df19bafe10df6d6e845f3': 'Cúp Anh Kiệt Hoàng Đô',
    '10ffdd2620d12e2b6afeb98c817f2f80': 'Cúp Anh Kiệt Chiến Lược',
    '8771464cbc6d5cf3d6795f8959d2520d': 'Cúp Anh Kiệt -Mùa {0}-',
    '1ed3b568d1b67c5cb22582f42d662443': 'Cúp Anh Kiệt Chiến Lược -Mùa {0}-',
    '2e3dbfeb10a557ef284895f471896c46': 'Cúp Anh Kiệt Hoàng Đô -Mùa {0}-',
    '728b34d2ace7c890456c06124f480a65': 'Trận Đấu Tập Cúp Anh Kiệt Hoàng Đô',
    'ea5e024771ad96681661e85d04f5cd02': 'Điều Kiện Thưởng 1 Cúp Anh Kiệt Hoàng Đô',
    '5a40b370633081f917b26819bb0454d3': 'Điều Kiện Thưởng 2 Cúp Anh Kiệt Hoàng Đô',
    '5aa45ef36c66a183e4d5eba916f625d2': 'Phần Thưởng Cúp Anh Kiệt Chiến Lược',
    '8abf87ef0c3c15bf0c1457857558150d': 'Phần Thưởng Cúp Anh Kiệt Hoàng Đô',
    '3330dd8f69cb0dec794663806dbf097d': 'Hồi phục {0} lượt khiêu chiến (Cúp Anh Kiệt)',
    
    # Chancellor Union / Guild
    '1727a00ee9d26b539a11c57ebfb0fb24': 'Bang Hội',
    '0331c7e2ac54757e1a1ab33e5b62303f': 'Gửi Lời Mời Bang Hội',
    '27b1d917eeef2124f679ac82fc98ef39': 'Gia nhập Bang Hội!',
    '17968039e19715801858925d551a9587': 'Thành Lập Bang Hội',
    'cbbccdd1222b5eed352bd5564edfe6c1': 'Tìm Kiếm Bang Hội',
    'b5f23cf5498c58ab16835a37b1ec6c35': 'Không tìm thấy Bang Hội phù hợp.',
    'e2bb063b05dd83456b59bff83cb8efc4': 'Xu Bang Hội',
    'dd0fb3acb73c4016275855af62cf799c': 'Giới Thiệu Bang Hội',
    '884d8508f1d467b4f617d296f764ba47': 'Chưa gia nhập Bang Hội.',
    'ec002f1b312fb6a25486e98a87fbbff1': 'Đã quyên góp cho Bang Hội.',
    '9943f5ff783ff1ce5e26cb973f327400': 'Mở khóa khi Bang Hội đạt Cấp {0}',
    
    # Tokumei Koryu / Unique Interaction
    '9b8809e68921bab1c675eb0f8ff9a174': 'Giao Lưu Đặc Biệt',
    '33a6f87cad496cf210edc33dec9dab62': 'Thưởng Giao Lưu Đặc Biệt',
    '90b343d49592f4844b5a31a09b4542c6': 'Thứ Tự Thưởng Giao Lưu Đặc Biệt',
    '784724d089b70ed14af0980e218f9492': 'Hạng Giao Lưu Đặc Biệt',
    
    # Limited event banner
    '0f3d3fdfbb3fccc23dc55742d5ff704d': 'Giới Hạn',
    
    # Blacksmith
    'd83838234ea7eb45ba252b4ee2d93e15': 'Lò Rèn',
    
    # Town building
    '39f67a213e2bb97f7faea4b74cfbf197': 'Kiến Thiết Quốc Gia',
}

# Regex replacements for recurring mixed-English patterns
REGEX_REPLACEMENTS = [
    (r'\bRoyal Cúp Dũng Khí\b', 'Cúp Anh Kiệt Hoàng Đô'),
    (r'\bStrategic Cúp Dũng Khí\b', 'Cúp Anh Kiệt Chiến Lược'),
    (r'\bCúp Dũng Khí\b', 'Cúp Anh Kiệt'),
    (r'\bLiên Minh Minh Chủ\b', 'Bang Hội'),
    (r'\bĐặc Mệnh\b', 'Đặc Biệt'),
    (r'\bKính lúp\b', 'Ảo Kính Ma Cảnh'),
    (r'\bBảng xếp hạng Battle\b', 'Trận Đua Bảng Xếp Hạng'),
    (r'\bregular battles\b', 'các trận đấu thường'),
    (r'\bRanking Battle\b', 'Trận Đua Bảng Xếp Hạng'),
    (r'\bAcquired Phần thưởng\b', 'Phần Thưởng Nhận Được'),
    (r'\bWeek (\d+)/(\d+) Underway\b', r'Tuần \1/\2 Đang Diễn Ra'),
    (r'\bWeek (\d+)/(\d+) Concluded\b', r'Tuần \1/\2 Đã Kết Thúc'),
    (r'\bweek (\d+)/(\d+) Underway\b', r'Tuần \1/\2 Đang Diễn Ra'),
    (r'\bweek (\d+)/(\d+) Concluded\b', r'Tuần \1/\2 Đã Kết Thúc'),
    (r'\bExhibition Match\b', 'Trận Đấu Tập'),
    (r'\bBonus Condition (\d+)\b', r'Điều Kiện Thưởng \1'),
    (r'\brestarted from \{0\}\b', r'đã khởi động lại từ {0}'),
    (r'In the <color=#39D09C>(.*?)</color>, the following effect is activated for both you and your opponent\.',
     r'Trong <color=#39D09C>\1</color>, hiệu ứng sau đây sẽ được kích hoạt cho cả bạn và đối thủ.'),
    (r'Insufficient right to fight in the (.*?)\.\nRecover right to fight\?\n<color=#ed4b39>\(Right to Fight Required: \{0\}\)</color>',
     r'Không đủ lượt khiêu chiến trong \1.\nHồi phục lượt khiêu chiến?\n<color=#ed4b39>(Lượt khiêu chiến yêu cầu: {0})</color>'),
]

fixed_count = 0
for t in terms:
    t_id = t.get('term', '')
    vi = t.get('vi', '')
    orig_vi = vi
    
    # 1. Exact term replacement
    if t_id in FIXES:
        vi = FIXES[t_id]
        
    # 2. Pattern replacements
    for pattern, repl in REGEX_REPLACEMENTS:
        vi = re.sub(pattern, repl, vi)
        
    if vi != orig_vi:
        t['vi'] = vi
        fixed_count += 1

print(f"Fixed {fixed_count} terms in ui_terms.json!")

with open('ui_terms.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, ensure_ascii=False, indent=2)

print("Saved updated ui_terms.json successfully!")
