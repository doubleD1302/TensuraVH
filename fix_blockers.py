import json

fixes = {
    32: 'Không đủ Thể lực.\nDùng vật phẩm để hồi phục Thể lực?\n<color=#ED4B39>(Thể lực cần thêm: {0})</color>',
    925: 'Bạn có thể đặt lại dữ liệu bằng cách xóa dữ liệu hiện tại\nvà chơi "TenSura: Ma Vương và Long Chủng"\nlại từ đầu.\n\n<color=#ed4b39>\n\nKhi dữ liệu đã bị xóa, bạn sẽ không thể khôi phục lại.</color>',
    950: '<color=#eae6e0>Tiến hóa</color> Kỹ năng Thường\n<color=#eae6e0>thành</color> Kỹ năng Đặc biệt.',
    951: '<color=#1e1d1b>Tiến hóa</color> Kỹ năng Thường\n<color=#1e1d1b>thành</color> Kỹ năng Đặc biệt.',
    952: '<color=#eae6e0>Tiến hóa</color> Kỹ năng Đặc biệt\n<color=#eae6e0>thành</color> Kỹ năng Độc nhất.',
    953: '<color=#1e1d1b>Tiến hóa</color> Kỹ năng Đặc biệt\n<color=#1e1d1b>thành</color> Kỹ năng Độc nhất.',
    954: '<color=#eae6e0>Tiến hóa </color>Kỹ năng Độc nhất\n<color=#eae6e0>lên cấp</color> tiến hóa tối hậu.',
    955: '<color=#1e1d1b>Tiến hóa </color>Kỹ năng Độc nhất\n<color=#1e1d1b>lên cấp</color> tiến hóa tối hậu.',
    1179: 'Tempest\n<mspace=0.85em>Bảng xếp hạng tổng EP</mspace>'
}

with open('ui_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

for t in terms:
    tid = int(t['id'])
    if tid in fixes:
        t['vi'] = fixes[tid]

with open('ui_terms.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, ensure_ascii=False, indent=2)

print('Applied 9 blocker fixes successfully!')
