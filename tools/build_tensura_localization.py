# -*- coding: utf-8 -*-
"""
build_tensura_localization.py - Professional localization builder for Tensura: ISEKAI Memories
Strictly enforces:
  - Tensura Light Novel / Anime tone & terminology (knowledge/01_style_and_tone_guide.md)
  - Character pronouns & relationships (knowledge/02_character_pronouns_matrix.md)
  - UI & skill templates (knowledge/03_skill_and_ui_templates.md)
  - Unity technical rules: tag & token preservation, UTF-8 NFC (knowledge/04_unity_technical_rules.md)
  - Complete, natural Vietnamese with FULL diacritics (NO missing accents)
  - Font safety: Keep title 'Menu' as 'Menu' to prevent font tofu boxes (□)
"""

import os
import sys
import json
import re
import unicodedata

sys.path.append('.')
sys.path.append('scratch')

from dict_en_skills import EN_SKILL_AND_UI_MAP
from build_dictionary_764 import DICT_764
from han_viet_dict import HAN_VIET, SPECIAL_SKILL_OVERRIDES, translate_cjk

# Comprehensive Canonical UI and Gameplay Glossary
GLOSSARY = {
    # System & Core Buttons
    "OK": "OK",
    "YES": "CÓ",
    "NO": "KHÔNG",
    "Confirm": "Xác Nhận",
    "Cancel": "Hủy",
    "Close": "Đóng",
    "Back": "Quay Lại",
    "Next": "Tiếp",
    "Start": "Bắt Đầu",
    "Retry": "Thử Lại",
    "Save": "Lưu",
    "Delete": "Xóa",
    "Use": "Sử Dụng",
    "Details": "Chi Tiết",
    "Settings": "Cài Đặt",
    "Notice": "Thông Báo",
    "Auto": "Tự Động",
    "Skip": "Bỏ Qua",
    "Claim": "Nhận",
    "Claim All": "Nhận Tất Cả",
    "Receive": "Nhận",
    "Receive All": "Nhận Tất Cả",
    "Collect": "Thu Thập",
    "Collect All": "Thu Thập Tất Cả",
    "Reward": "Phần Thưởng",
    "Rewards": "Phần Thưởng",
    "Shop": "Cửa Hàng",
    "Inventory": "Túi Đồ",
    "Equipment": "Trang Bị",
    "Quest": "Nhiệm Vụ",
    "Quests": "Nhiệm Vụ",
    "Mission": "Nhiệm Vụ",
    "Missions": "Nhiệm Vụ",
    "Daily": "Hằng Ngày",
    "Weekly": "Hằng Tuần",
    "Event": "Sự Kiện",
    "Events": "Sự Kiện",
    "Ranking": "Bảng Xếp Hạng",
    "Login Bonus": "Quà Đăng Nhập",
    "Memory": "Ký Ức",
    "Memories": "Ký Ức",
    "Friend": "Bạn Bè",
    "Friends": "Bạn Bè",
    "Guild": "Hội",
    "Allies": "Đồng Minh",
    "Party": "Đội Hình",
    "Team": "Đội Hình",
    "Level Up": "Nâng Cấp",
    "Enhance": "Cường Hóa",
    "Awaken": "Thức Tỉnh",
    "Awakening": "Thức Tỉnh",
    "Awakened": "Thức Tỉnh",
    "Limit Break": "Phá Giới Hạn",
    "Evolve": "Tiến Hóa",
    "Evolution": "Tiến Hóa",
    "Incapacitated": "Không Thể Chiến Đấu",
    "Defeated": "Bị Đánh Bại",
    "Victory": "Chiến Thắng",
    "Defeat": "Thất Bại",
    "Draw": "Hòa",
    "Turn": "Lượt",
    "Wave": "Đợt",
    "Speed": "Tốc Độ",
    "Retire": "Rút Lui",
    "Give Up": "Từ Bỏ",
    "Bonus": "Thưởng",
    "Bonuses": "Thưởng",

    # Font Safe UI Elements
    "Menu": "Menu",
    "Support": "Hỗ Trợ",
    "Data Transfer": "Chuyển Đổi Dữ Liệu",
    "Data Transfer Settings": "Cài Đặt Chuyển Đổi Dữ Liệu",
    "Data Transfer Details": "Chi Tiết Chuyển Đổi Dữ Liệu",

    # Tensura Lore & World Terms
    "Jura Tempest Federation": "Liên Bang Jura Tempest",
    "Tempest": "Tempest",
    "Demon Lord": "Ma Vương",
    "Demon Lords": "Ma Vương",
    "Octagram": "Bát Tinh Ma Vương",
    "True Dragon": "Chân Long",
    "Hero": "Dũng Giả",
    "Great Sage": "Đại Hiền Giả",
    "Raphael": "Raphael",
    "Predator": "Kẻ Săn Mồi (Bổ Thực Giả)",
    "Magicule": "Ma Tố",
    "Magicules": "Ma Tố",
    "Magic": "Ma Pháp",
    "Spirit": "Tinh Linh",
    "Spirits": "Tinh Linh",
    "Slime": "Slime",
    "Goblin": "Goblin",
    "Ogre": "Ogre",
    "Kijin": "Quỷ Nhân (Kijin)",
    "Beastman": "Thú Nhân",
    "Dwarf": "Dwarf",
    "Elf": "Elf",
    "Adventurer's Guild": "Hội Mạo Hiểm Giả",
    "Walpurgis": "Walpurgis",
    "Mirror World": "Thế Giới Gương",
    "Valor Cup": "Cúp Anh Kiệt",

    # Tensura Gameplay Systems
    "Build Nation": "Xây Dựng Vương Quốc",
    "Nation Building": "Xây Dựng Vương Quốc",
    "Nation Facilities": "Công Trình Vương Quốc",
    "Facilities": "Công Trình",
    "Facility": "Công Trình",
    "Citizens": "Cư Dân",
    "Citizen": "Cư Dân",
    "Companions": "Đồng Đội",
    "Companion": "Đồng Đội",
    "Forge": "Xưởng Rèn",
    "Recruit": "Chiêu Mộ",
    "Recruitment": "Chiêu Mộ",
    "Recruits": "Chiêu Mộ",
    "Summon": "Triệu Hồi",
    "Summons": "Triệu Hồi",
    "Unique Interaction": "Giao Lưu Đặc Mệnh",
    "Unique Interaction Bonus": "Thưởng Giao Lưu Đặc Mệnh",
    "Unique Interaction Rank": "Hạng Giao Lưu Đặc Mệnh",
    "Bond Level": "Cấp Độ Thân Thiết",
    "Affinity": "Mức Gắn Kết",
    "Bazaar Points": "Điểm Đổi Thưởng",
    "Shared Bazaar Points": "Điểm Đổi Thưởng Chung",
    "Drop Rates": "Tỷ Lệ Xuất Hiện",
    "Drop Rate": "Tỷ Lệ Xuất Hiện",
    "Sworn Friend": "Đồng Minh",
    "Sworn Friends": "Đồng Minh",
    "Aid": "Viện Trợ",
    "Aid Request": "Yêu Cầu Viện Trợ",
    "Request Aid": "Gửi Yêu Cầu Viện Trợ",
    "Vitality": "Thể Lực",
    "Stamina": "Thể Lực",
    "EP": "EP",
    "HP": "HP",
    "MP": "MP",
    "ATK": "Công",
    "DEF": "Thủ",
    "SPD": "Tốc",
    "Attack": "Tấn Công",
    "Defense": "Phòng Thủ",
    "Speed": "Tốc Độ",
    "Critical Rate": "Tỉ Lệ Bạo Kích",
    "CRIT Rate": "Tỉ Lệ Bạo Kích",
    "CRIT DMG": "ST Bạo Kích",
    "Guard Rate": "Tỉ Lệ Chặn Đòn",
    "Piercing Rate": "Tỉ Lệ Xuyên Thấu",
    "Counterattack Rate": "Tỉ Lệ Phản Công",
    "Evasion Rate": "Tỉ Lệ Né Tránh",
    "Attribute": "Thuộc Tính",
    "Attributes": "Thuộc Tính",
    "Attack Type": "Loại Đòn Đánh",
    "Attack Resistances": "Kháng Đòn Đánh",
    "Attribute Resistances": "Kháng Thuộc Tính",
    "Abnormal Status Resistances": "Kháng Trạng Thái Bất Thường",

    # Skills & Combos
    "Unique Skill": "Kỹ Năng Độc Nhất",
    "Ultimate Skill": "Kỹ Năng Tối Thượng",
    "Extra Skill": "Kỹ Năng Đặc Biệt",
    "Common Skill": "Kỹ Năng Thường",
    "Battle Skill": "Kỹ Năng Chiến Đấu",
    "Battle Skills": "Kỹ Năng Chiến Đấu",
    "Secret Skill": "Tuyệt Kỹ",
    "Secret Skills": "Tuyệt Kỹ",
    "Secret Skill EP": "EP Tuyệt Kỹ",
    "Protection": "Gia Hộ",
    "Divine Protection": "Gia Hộ",
    "Protection Skill": "Kỹ Năng Gia Hộ",
    "Protection Support": "Hỗ Trợ Gia Hộ",
    "Supporting Divine Protection": "Chỉ Dẫn Hỗ Trợ Gia Hộ",
    "Protection Trait": "Đặc Tính Gia Hộ",
    "Protection Trait (Support)": "Đặc Tính Gia Hộ (Hỗ Trợ)",
    "Soul of Protection": "Linh Hồn Gia Hộ",
    "Soul of Combos": "Linh Hồn Liên Kích",
    "Soul of Secret Skills": "Linh Hồn Tuyệt Kỹ",
    "Soul Conversion": "Chuyển Hóa Linh Hồn",
    "Soul Lineage": "Phả Hệ Linh Hồn",
    "Heartprint Skill": "Kỹ Năng Tranh Tâm Thức",
    "Heartscape Skill": "Kỹ Năng Tâm Cảnh",
    "EX Ability": "Thiên Phú EX",
    "EX Ability Effect": "Hiệu Ứng Thiên Phú EX",
    "EX Ability Effects": "Danh Sách Hiệu Ứng Thiên Phú EX",
    "EX Ability Release": "Mở Khóa Thiên Phú EX",
    "EX Ability Release Result": "Kết Quả Mở Khóa Thiên Phú EX",
    "Change Main Slot": "Đổi Ô Chính",
    "Change Sub Slot": "Đổi Ô Phụ",
    "Main": "Chính",
    "Sub": "Phụ",
    "Vocals": "Lồng Tiếng",
    "No Vocals": "Không Lồng Tiếng",
    "With Vocals": "Có Lồng Tiếng",
    "Opponent": "Đối Thủ",
    "Class Battle": "Đấu Phân Hạng",
    "Developing": "Đang Khai Phá",
    "Work Done": "Khai Phá Hoàn Tất",
    "On Duty": "Đang Làm Nhiệm Vụ",
    "New Jobs": "Nhiệm Vụ Mới",
    "Defense Result": "Kết Quả Phòng Thủ",
    "Season": "Mùa Giải",
    "Firsts": "Lần Đầu",
    "Challenge Bonus": "Thưởng Thử Thách",
    "Character": "Nhân Vật",
    "Work Done Notification": "Thông Báo Hoàn Tất Khai Phá",
    "EX Ability Effect EP": "EP Hiệu Ứng Thiên Phú EX",
    "Accomplished": "Số Thử Thách Đạt",
    "Challenges Selected": "Số Thử Thách Chọn",
    "Locked": "Chưa Mở Khóa",
    "In Progress": "Đang Tiến Hành",
}

# Substring fixes for mistranslated terms in existing text
MISTRANSLATION_FIXES = [
    (r'\bThực đơn\b', 'Menu'),
    (r'\bỦng hộ\b', 'Hỗ Trợ'),
    (r'Truyền dữ liệu', 'Chuyển Đổi Dữ Liệu'),
    (r'truyền dữ liệu', 'chuyển đổi dữ liệu'),
    (r'\blò rèn\b', 'Xưởng Rèn'),
    (r'\bLò rèn\b', 'Xưởng Rèn'),
    (r'\bXây dựng đất nước\b', 'Xây dựng Vương quốc'),
    (r'\bxây dựng đất nước\b', 'xây dựng Vương quốc'),
    (r'\bđất nước\b', 'Vương quốc'),
    (r'\bĐất nước\b', 'Vương quốc'),
    (r'\btuyển dụng\b', 'chiêu mộ'),
    (r'\bTuyển dụng\b', 'Chiêu Mộ'),
    (r'\bCông dân\b', 'Cư Dân'),
    (r'\bcông dân\b', 'cư dân'),
    (r'Thu hồi quyền chiến đấu', 'Hồi phục lượt khiêu chiến'),
    (r'thu hồi quyền chiến đấu', 'hồi phục lượt khiêu chiến'),
    (r'Thu hồi quyền', 'Hồi phục lượt'),
    (r'thu hồi quyền', 'hồi phục lượt'),
    (r'Tỷ lệ quan trọng', 'Tỉ lệ Bạo kích'),
    (r'tỷ lệ quan trọng', 'tỉ lệ Bạo kích'),
    (r'Kỹ năng bí mật', 'Tuyệt Kỹ'),
    (r'kỹ năng bí mật', 'tuyệt kỹ'),
    (r'Sức sống không đủ', 'Không đủ Thể lực'),
    (r'sức sống không đủ', 'không đủ Thể lực'),
    (r'sức sống', 'Thể lực'),
    (r'Sức sống', 'Thể lực'),
    (r'giọng hát', 'lồng tiếng'),
    (r'Giọng hát', 'Lồng tiếng'),
    (r'\bĐÚNG\b', 'CÓ'),
    (r'\bĐƯỢC RỒI\b', 'OK'),
    (r'Cơn thịnh nộ của màu đỏ thẫm', 'Hồng Diễm Chi Nộ'),
    (r'Bắn Rồng', 'Huy Long Du Kích Chưởng'),
    (r'Mắt Quỷ', 'Ách Họa Nhãn Quang'),
    (r'Kiểm soát hỗn loạn', 'Hỗn Độn Chưởng Khống'),
    (r'Vùng lửa', 'Tiêu Viêm Ngục Vực'),
    (r'Người thay đổi rồng', 'Long Khí Chuyển Hoán'),
    (r'Thế giới nhỏ', 'Mê Cung Sáng Tạo'),
    (r'tù lắc', 'Luyện Ngục Ác Thủ'),
    (r'Tù lắc', 'Luyện Ngục Ác Thủ'),
    (r'máy nổ lớn', 'Đại Địa Oanh Tạc'),
    (r'lát cắt đột ngột', 'Thuấn Liệt Trảm'),
    (r'Ve sầu Flash', 'Không Thiền Nhất Thiểm'),
    (r'Ảo ảnh màu cam', 'Bão Tuyết Ảo Ảnh'),
    (r'Ba điều ác của lò rèn', 'Rèn Đúc Tam Binh'),
    (r'máy cắt rồng', 'Long Tinh Bạo Kích'),
    (r'Thợ lặn Drago', 'Long Tinh Băng Lạc Cước'),
    (r'Bàn tay báo lửa Fang', 'Báo Nha Bạo Viêm Chưởng'),
    (r'Sói âm thanh', 'Tật Phong Trảo Nha'),
    (r'thủ tướng', 'Lãnh Chúa'),
    (r'Thủ tướng', 'Lãnh Chúa'),
    (r'Jura Tempest</mspace><space=-8>Liên đoàn', 'Liên Bang</mspace><space=-8>Jura Tempest'),
    (r'Tương tác Độc nhất', 'Giao Lưu Đặc Mệnh'),
    (r'tương tác Độc nhất', 'giao lưu Đặc Mệnh'),
    (r'Tương tác độc nhất', 'Giao Lưu Đặc Mệnh'),
    (r'tương tác độc nhất', 'giao lưu Đặc Mệnh'),
    (r'tương tác độc đáo', 'giao lưu Đặc Mệnh'),
    (r'Tương tác độc đáo', 'Giao Lưu Đặc Mệnh'),
    (r'tương tác duy nhất', 'giao lưu Đặc Mệnh'),
    (r'Kịch bản kết thúc', 'Kết thúc và Bỏ qua'),
    (r'Kịch bản chơi', 'Xem Cốt Truyện'),
    (r'mất năng lực', 'không thể chiến đấu'),
    (r'Mất năng lực', 'Không Thể Chiến Đấu'),
    (r'Tỷ lệ xuyên thủng', 'Tỉ lệ Xuyên thấu'),
    (r'Tỷ lệ bảo vệ', 'Tỉ lệ Chặn đòn'),
    (r'Phục hồi quyền chiến đấu', 'Hồi phục lượt khiêu chiến'),
    (r'phục hồi quyền chiến đấu', 'hồi phục lượt khiêu chiến'),
    (r'Quyền chiến đấu', 'Lượt khiêu chiến'),
    (r'quyền chiến đấu', 'lượt khiêu chiến'),
    (r'Fused Kỹ năng Độc nhất', 'Kỹ Năng Độc Nhất Dung Hợp'),
    (r'Fused Unique', 'Kỹ Năng Độc Nhất Dung Hợp'),
    (r'Tỷ lệ rớt', 'Tỷ lệ xuất hiện'),
    (r'tỷ lệ rớt', 'tỷ lệ xuất hiện'),
    (r'Linh hồn bảo vệ', 'Linh Hồn Gia Hộ'),
    (r'linh hồn bảo vệ', 'Linh Hồn Gia Hộ'),
    (r'kích hoạt bảo vệ', 'kích hoạt Gia Hộ'),
    (r'Kích hoạt bảo vệ', 'Kích hoạt Gia Hộ'),
    (r'Kích hoạt Bảo vệ', 'Kích hoạt Gia Hộ'),
    (r'…', '...'),
]

# Specific sentence translations for prominent UI texts
SENTENCE_TRANSLATIONS = {
    "Insufficient Vitality.\nUse items to restore vitality?": "Không đủ Thể lực.\nBạn có muốn dùng vật phẩm để hồi phục Thể lực không?",
    "Insufficient Vitality.": "Không đủ Thể lực.",
    "Insufficient right to fight in the Valor Cup.\nRecover right to fight?": "Không đủ lượt khiêu chiến Cúp Anh Kiệt.\nBạn có muốn hồi phục lượt khiêu chiến không?",
    "Insufficient right to fight (Valor Cup).\nRecover right to fight?": "Không đủ lượt khiêu chiến (Cúp Anh Kiệt).\nBạn có muốn hồi phục lượt khiêu chiến không?",
    "* Limit\nreached": "* Đã đạt\ngiới hạn",
    "Not Cleared": "Chưa hoàn thành",
    "Subscription/Renewal Bonuses": "Ưu đãi Đăng ký / Gia hạn",
    "No content currently available to display.": "Hiện không có nội dung để hiển thị.",
    "Unlocked a New District": "Mở Khóa Khu Vực Mới",
    "Assign a character to Protection Support.": "Vui lòng chọn nhân vật xếp vào Hỗ Trợ Gia Hộ.",
    "Assign a character to the Protection slot.": "Vui lòng chọn nhân vật xếp vào ô Gia Hộ.",
    "Assign a character to the Protection Support slot.": "Vui lòng chọn nhân vật xếp vào ô Hỗ Trợ Gia Hộ.",
    "Select challenge conditions.": "Vui lòng chọn điều kiện thử thách.",
    "All mission rewards have been received.": "Đã nhận toàn bộ phần thưởng nhiệm vụ.",
    "Defeat enemies to get enhancement effects.": "Tiêu diệt kẻ địch để nhận hiệu ứng cường hóa.",
    "A facility in storage or located in another district has completed construction/leveling up.": "Một công trình trong kho hoặc ở khu vực khác đã hoàn tất xây dựng/nâng cấp.",
    "There are no current aid requests.": "Hiện không có yêu cầu viện trợ nào.",
    "There are no facilities currently under construction.": "Hiện không có công trình nào đang xây dựng.",
    "Level up and simultaneously send a request for aid?": "Nâng cấp và đồng thời gửi yêu cầu viện trợ?",
    "* Changing screens and select a sworn friend to send aid.": "* Chuyển màn hình và chọn Đồng Minh để gửi viện trợ.",
    "You can change your in-game graphics quality.": "Bạn có thể thay đổi chất lượng đồ họa trong game.",
    "You have purchased all recommended packs.\nCheck the shop for other available packs.": "Bạn đã mua tất cả các gói đề xuất.\nHãy kiểm tra cửa hàng để xem các gói khác.",
    "The following mission has been made available.": "Nhiệm vụ sau đã được mở khóa.",
    "The missions below have been cleared.": "Các nhiệm vụ dưới đây đã hoàn thành.",
    "* This material is meant for another skill. It requires magicules to use.": "* Nguyên liệu này dành cho kỹ năng khác. Cần Ma Tố để sử dụng.",
    "* This material is specialized for a lower skill. It requires magicules to use.": "* Nguyên liệu này chuyên dụng cho kỹ năng cấp thấp hơn. Cần Ma Tố để sử dụng.",
    "* You can try this service free for the first month.\n* Please read to the end of the scroll box.": "* Bạn có thể dùng thử dịch vụ này miễn phí trong tháng đầu tiên.\n* Vui lòng cuộn đọc đến hết nội dung bên dưới.",
    "Read scenario text and continue": "Đọc cốt truyện bằng văn bản rồi tiếp tục",
    "Skip to the next scenario?": "Chuyển sang cốt truyện tiếp theo?",
    "End Scenario": "Kết thúc và Bỏ qua",
    "Play Scenario": "Xem Cốt Truyện",
    "Download vocal data and play scenario?": "Tải dữ liệu lồng tiếng và phát cốt truyện?",
    "Download all episode data": "Tải toàn bộ dữ liệu các tập liên quan",
    "Download Size": "Dung lượng tải xuống",
    "Wi-Fi connection recommended for large downloads.": "Nếu dung lượng lớn, khuyến nghị kết nối Wi-Fi để tải xuống.",
    "No Vocals": "Không Lồng Tiếng",
    "With Vocals": "Có Lồng Tiếng",
    "Effect List": "Danh Sách Hiệu Ứng",
    "Change Members": "Thay Đổi Thành Viên",
    "Note: You can switch between SUB and MAIN once per turn.": "Lưu ý: Có thể đổi giữa Đội Phụ (SUB) và Đội Chính (MAIN) 1 lần mỗi lượt.",
    "Unassigned": "Chưa Xếp Đội",
    "Piercing Rate": "Tỉ Lệ Xuyên Thấu",
    "Evasion Rate": "Tỉ Lệ Né Tránh",
    "Counterattack Rate": "Tỉ Lệ Phản Công",
    "Guard Rate": "Tỉ Lệ Chặn Đòn",
    "Critical Rate": "Tỉ Lệ Bạo Kích",
    "Activated": "Đã Kích Hoạt",
    "Continue": "Tiếp Tục",
    "Select": "Lựa Chọn",
    "Skip Recruit Animations": "Bỏ qua Hoạt ảnh Chiêu Mộ",
    "Recruit x3 More": "Chiêu mộ thêm 3 lần",
    "Recruit Details/Drop Rates": "Chi Tiết Chiêu Mộ / Tỷ Lệ Xuất Hiện",
    "Companion Update In:": "Làm mới Đồng Đội sau:",
    "There are no companions that fulfill the conditions.\nPlease reselect the challenge conditions.": "Không có Đồng Đội nào thỏa mãn điều kiện.\nVui lòng chọn lại điều kiện thử thách.",
    "Your territory\nwill be expanded\nin accordance\nwith your new level.": "Lãnh thổ của bạn\nsẽ được mở rộng\ntương ứng\nvới cấp độ mới.",
    "Performing an eligible Recruit will grant shared bazaar points instead of regular bazaar points.\nShared bazaar points are shared across eligible Recruits and can be used interchangeably between them.\nThe following list of eligible Recruits will be updated as new Recruits are released in the future.": "Khi thực hiện Chiêu Mộ hợp lệ, bạn sẽ nhận được Điểm Đổi Thưởng Chung thay vì Điểm Đổi Thưởng thường.\nĐiểm Đổi Thưởng Chung có thể dùng chung và hoán đổi giữa các Chiêu Mộ áp dụng.\nDanh sách Chiêu Mộ áp dụng sẽ được cập nhật liên tục khi có Chiêu Mộ mới trong tương lai.",
    "* Shown with characters at max enhancement.\n* Only some characters included in the recruit are shown.\n* To see the available characters, go to \"Recruit Details/Drop Rates\".": "* Chỉ số hiển thị khi nhân vật đã cường hóa tối đa.\n* Chỉ hiển thị một số nhân vật có trong Chiêu Mộ.\n* Để xem toàn bộ nhân vật xuất hiện, vui lòng vào \"Chi Tiết Chiêu Mộ / Tỷ Lệ Xuất Hiện\".",
    "* Shown with characters at max enhancement. (Excludes additional enhancements)\n* Only some characters included in the recruit are shown.\n* To see the available characters, go to \"Recruit Details/Drop Rates\".": "* Chỉ số hiển thị khi nhân vật đã cường hóa tối đa (không tính cường hóa bổ sung).\n* Chỉ hiển thị một số nhân vật có trong Chiêu Mộ.\n* Để xem toàn bộ nhân vật xuất hiện, vui lòng vào \"Chi Tiết Chiêu Mộ / Tỷ Lệ Xuất Hiện\".",
    "* Only some characters included in the recruit are shown.\n* To see the available characters, go to 'Recruit Details/Drop Rates'.": "* Chỉ hiển thị một số nhân vật có trong Chiêu Mộ.\n* Để xem toàn bộ nhân vật xuất hiện, vui lòng vào 'Chi Tiết Chiêu Mộ / Tỷ Lệ Xuất Hiện'.",
    "Note: Content differs depending on the Recruit. Check the Drop Rates for details.": "Lưu ý: Nội dung sẽ khác nhau tùy theo từng Chiêu Mộ. Vui lòng kiểm tra Tỷ Lệ Xuất Hiện để biết chi tiết.",
    "Requested aid from {0:#,0} chancellor(s).\nConstruction time has been reduced, and you received the following items.": "Đã gửi yêu cầu viện trợ đến {0:#,0} Lãnh Chúa.\nThời gian xây dựng đã được rút ngắn, đồng thời bạn nhận được các vật phẩm sau.",
    "Bazaar Points: {0:#,0} / Shared Bazaar Points: {1:#,0}": "Điểm Đổi Thưởng: {0:#,0} / Điểm Đổi Thưởng Chung: {1:#,0}",
    "Insufficient Vitality.\nUse items to restore vitality?\n<color=#ED4B39>(Additional Vitality Required: {0})</color>": "Không đủ Thể lực.\nBạn có muốn dùng vật phẩm để hồi phục Thể lực không?\n<color=#ED4B39>(Thể lực cần thêm: {0})</color>",
    "Insufficient Vitality. {0}": "Không đủ Thể lực. {0}",
    "(Right to Fight Required: {0})": "(Lượt khiêu chiến cần thêm: {0})",
    "Executing Parallel Processing…": "Đang thực hiện Xử lý song song...",
    "Executing\nParallel Processing…": "Đang thực hiện\nXử lý song song...",
    "Download the app to your new device and go to the title screen.\nTap \"Menu\" > \"Data Transfer\", and enter your data transfer ID and password.": "Tải ứng dụng xuống thiết bị mới của bạn và chuyển đến màn hình tiêu đề.\nNhấn vào \"Menu\" > \"Chuyển Đổi Dữ Liệu\" rồi nhập ID và mật khẩu của bạn.",
    "Data transfer settings are complete. Download the app to your new device and go to the title screen.\nTap \"Menu\" > \"Data Transfer\", and enter your data transfer ID and password.": "Cài đặt chuyển đổi dữ liệu đã hoàn tất. Tải ứng dụng xuống thiết bị mới của bạn và chuyển đến màn hình tiêu đề.\nNhấn vào \"Menu\" > \"Chuyển Đổi Dữ Liệu\" rồi nhập ID và mật khẩu của bạn.",
    "Confirm the details before transferring data.": "Xác nhận các chi tiết trước khi chuyển đổi dữ liệu.",
}

# Exact ID overrides for 100% technical safety & placeholders
EXACT_ID_OVERRIDES = {
    37: "Ách Họa Nhãn Quang",
    54: "Hồn Diệt Trảm",
    125: "Tử Nghiệp Thiết Chùy",
    143: "Trảm Loạn Ảnh",
    158: "Menu",
    346: "Hỗ Trợ",
    548: "Menu",
    566: "Chuyển Đổi Dữ Liệu",
    921: "Xác nhận các chi tiết trước khi chuyển đổi dữ liệu.",
    923: "Menu",
    981: "Hỗ Trợ",
    1013: "Đang thực hiện Xử lý song song...",
    1151: "Đang thực hiện\nXử lý song song...",
    1152: "Đang thực hiện\nXử lý song song...",
    1593: "Cốt truyện thường ngày hôm nay <color=#ed4b39>Đã Giải Quyết</color>",
    1645: "Không đủ nguyên liệu. Đã kết thúc rèn lại.",
    1655: "Giao các vật phẩm sau?",
    1723: "<scale=0.8><space=-18><cspace=-3>EP Đội Hình</scale>",
    1760: "<cspace=0.22em>Đạt Cấp Mới</cspace>",
    1772: "Hằng Tuần <size=30>(Phòng Thủ)</size>",
    1788: "<mspace=0.84em><scale=0.75>Đạt Giới Hạn</scale></mspace>",
    1789: "<size=48>Kích Hoạt</size> Đặc Tính Anh Kiệt",
    1791: "<i angle=35><size=120>Liên Kích</size> Hung Bạo</i>",
    1792: "<i angle=35><size=120>Liên Kích</size> Cuồng Bạo</i>",
    1818: "Bạn có chắc muốn phân giải Phù Chú Khắc Ấn ở trên không?",
    1821: "<size=40>Chọn Nguyên Liệu</size> (Tối đa 5)",
    1837: "Bạn có chắc muốn đặt lại Phù Chú Khắc Ấn ở trên không?",
    1874: "<color=#f7e416>Mở Khóa</color> Bản Đồ Tầng <color=#f7e416>Tầm Nhìn</color>",
    1893: "Không đủ vật phẩm tiêu hao,\nkhông thể tiếp tục thực hiện.",
    1894: "Đã vượt quá số lượt, không thể tiếp tục.",
    1895: "Đã vượt quá thời hạn, không thể tiếp tục.",
    1954: "Bạn có chắc muốn thay đổi hình thức lãnh thổ không?",
    1990: "<mspace=1.08em>Kích Hoạt Hiệu Ứng Sân Khấu",
    2060: "Lật\nThẻ",
    2076: "Đổi vật phẩm bằng Vé Trang Phục?",
    2077: "Đổi vật phẩm bằng Tiền Vàng?",
    2078: "Đổi vật phẩm bằng Ma Tinh Thạch?",
    2166: "Bắt đầu dung hợp kỹ năng",
    2167: "Bắt đầu dung hợp kỹ năng",
    2259: "Thưởng Xu Lễ Hội Giới Hạn Ngày Cuối",
    2322: "Không bao gồm nhân vật đang bổ nhiệm",
    2323: "* Sức lao động tăng dựa trên số lần thức tỉnh\nvà tổng cấp độ của các đồng đội có cùng tên.",
    2358: "* Sức lao động tăng dựa trên tổng cấp độ\ncủa các đồng đội có cùng tên.",
    2390: "Bạn đã nhận được <color=#2be41d>vật phẩm thức tỉnh nhân vật 5★ EX</color>\nkhi nhận được nhân vật Cực 5★ EX.",
    2463: "<mspace=1.6em>Huy Hiệu",
    2464: "<mspace=1.6em>Đã Nhận",
    2488: "Tất cả gian hàng đang sôi động (Fever)!",
    2534: "Lung Thuấn Liệt Trảm! Cải!",
    2539: "* Tỉ lệ chiêu mộ bằng vé có thể xem trong Thông Báo Trong Game. Tỉ lệ vật phẩm có thể xem tại Menu > Trợ Giúp > Thông Tin Tỉ Lệ Vật Phẩm.",
    2649: "Xét duyệt: Cần duyệt mới được vào",
    2664: "Tự do: Không cần duyệt, vào ngay",
    2702: "Quyên góp các vật phẩm ở trên?",
    2757: "Áp dụng các hiệu ứng Ma Trang Bị này?",
    2843: "Cấp Liên Minh đã tăng, mở khóa các tính năng mới.",
    2847: "- Hình Dán Trò Chuyện Liên Minh -",
    2892: "Không có đối tượng nào để yêu cầu viện trợ.\nBạn không thể gửi yêu cầu viện trợ.",
    2980: "Hỗ Trợ",
    2983: "Giải Phóng\nThuộc Tính",
    3059: "Loại Kỹ Năng: <color=#2be41d>Đã Chỉ Định</color>",
    3061: "Loại Hiệu Ứng: <color=#2be41d>Đã Chỉ Định</color>",
    3094: "<size=72%>Chiêu Mộ x</size>3",
    3129: "<space=-12><cspace=-3><scale=0.92>Đang thực hiện Xử lý song song...",
    3130: "<space=-12><cspace=-3><scale=0.92>Xử lý song song hoàn tất",
    3196: "Xem Cửa Hàng Trực Tuyến\ntại đây",
    3249: "[<cspace=0.1em>Phong Ấn Hiệu Ứng Hồi Phục</cspace>] <cspace=0.1em>Đã Kích Hoạt</cspace>",
    3263: "Nâng MAX\nCấp",
    3264: "Chỉ Kỹ Năng\nTranh Tâm Thức",
    3267: "Bạn đã nhận được <color=#39D09C>vật phẩm thức tỉnh nhân vật 5★ EX</color>\nkhi nhận được nhân vật Cực 5★ EX.",
    3276: "Có thể đổi từng thành viên hàng sau lên hàng trước <color=#F2EC4E>mỗi lượt một lần</color>",
    3283: "Menu",
    3284: "Lượt 1 không thể dùng Kỹ năng Tranh Tâm Thức",
    3293: "Loại Kỹ Năng: <color=#39D09C>Đã Chỉ Định</color>",
    3310: "Loại Hiệu Ứng: <color=#39D09C>Đã Chỉ Định</color>",
    3340: "<mspace=1.2em>Tái Bản",
    3381: "<mspace=0.8em>Lật Thẻ</mspace>",
    3424: "Bạn có chắc muốn rút ngắn thời gian xây dựng không?",
    3428: "<size=133%>Giải Nhất</size>",
    3429: "<size=133%>Giải Nhì</size>",
    3430: "<size=133%>Giải Ba</size>",
    3488: "Nhận được Điểm Đổi Thưởng Chung!",
    3490: "Đổi bằng Điểm Đổi Thưởng / Điểm Đổi Thưởng Chung? Điểm Đổi Thưởng sẽ được ưu tiên sử dụng trước.",
    3522: "<rotate=90>Tuyệt Kỹ Tối Thượng</rotate>",
    3603: "Sở hữu: {0:#,0}",
    3606: "Còn lại: x<color=#ed4b39>{0}</color>",
    3611: "Khi kết thúc {0}/{1} trận",
    3612: "Đã kết thúc {0}/{1} trận",
    3616: "<size=32><color=#2BE41D>{0:#,0}</color></size> Chuỗi Thắng!",
    3624: "<size=31>Điểm Phân Hạng</size> <color=#F7E416>{0:#,0}</color>",
    3627: "Cập nhật thưởng Tuần / Phòng Thủ vào {0}",
    3633: "Điểm: <color=#2be41d>{0:#,0}</color>",
    3634: "Còn lại: x<color=red>{0}</color>",
    3635: "Hạng: {0}",
    3636: "TIẾP: {0}",
    3641: "HP <color=#2be41d>+{0}%</color>",
    3642: "Công <color=#2be41d>+{0}%</color>",
    3643: "Thủ <color=#2be41d>+{0}%</color>",
    3645: "<size=30>CV: </size><size=36>{0}</size>",
    3649: "Tình Trạng Xây Dựng: {0}/{1}",
    3651: "Đã Giải Quyết: {0}/{1}",
    3653: "Cấp Hiệu Ứng Khắc Ấn: {0}",
    3654: "Sở Hữu: {0}/{1}",
    3657: "Sở Hữu: {0:#,0}",
    3658: "TIẾP: {0:#,0}",
    3660: "Điều Kiện Lọc - {0} -",
    3665: "Số Lần Rèn Lại: {0}",
    3672: "Thời gian nhận viện trợ: {0}",
    3676: "Thời Gian Xây Được Rút Ngắn: <color=#f7e416>{0}</color>",
    3677: "Liên Bang Jura Tempest {0}",
    3679: "<color=#FFFAEC>Còn lại:</color> {0}",
    3683: "Bổ sung: <color=#13e600>{0:#,0}</color>",
    3684: "Độc Nhất: <color=#13e600>{0:#,0}</color>",
    3685: "{0:#,0}×<color=#2BE41D>{1:#,0}</color>",
    3688: "Điểm Đổi Thưởng: {0:#,0}",
    3690: "Điểm Đổi Thưởng Đang Có: {0:#,0}",
    3700: "TIẾP: {0:#,0}",
    3701: "- {0}",
    3702: "<size=75%>Thưởng Hỗ Trợ</size>\n+{0}%",
    3703: "{0:#,0}",
    3704: "{0:#,0} (Còn {1:#,0})",
    3705: "{0:#,0} (Còn {1:#,0})",
    3707: "{0} điểm",
    3722: "TIẾP: {0}",
    3723: "EXP Nhận Được: {0:#,0}",
    3724: "<size=24>Đến</size> {0}",
    3729: "{0}<size=90%>F</size>",
    3730: "Hiệu Ứng Cấp Ngoại Giao: {0}%",
    3733: "<color=#FFFAEC>Mậu Dịch Đồng Thời </color>{0}<color=#FFFAEC>/{1}</color>",
    3741: "Mở khóa bằng cách dùng hết số lượt khiêu chiến của tất cả {0} thuộc tính khác về 0",
    3743: "Khi kết thúc {0}/{1} trận",
    3744: "{0}/{1} Trận",
    3745: "(Tổng Điểm: {0:#,0})",
    3751: "Tỉ Lệ Xuất Hiện ★{0}: {1}%",
    3752: "Còn {0}<color=#FFFAEC> lượt</color>",
    3755: "Hiệu Ứng Sân Khấu - Mùa Giải {0} -",
    3759: "Chiêu Mộ: <size=53>{0}</size>",
    3762: "<size=31>Tổng Điểm</size> <color=#F7E416>{0:#,0}</color>",
    3765: "{0}<size=32> Vòng</size>",
    3766: "{0} LIÊN KÍCH",
    3769: "<size=34>THƯỞNG </size>\n {0}%",
    3774: "Công <color=#2be41d>+{0}%</color>",
    3775: "Còn lại: x<size=90>{0}</size>",
    3777: "Chi phí tiêu hao: {0}",
    3778: "Tiêu Hao Cost Kỹ Năng: {0}",
    3779: "Top {0}% - {1}%",
    3781: "Thủ <color=#2be41d>+{0}%</color>",
    3783: "Còn lại: x<color=#ed4b39><size=36>{0}</size></color>",
    3791: "{0:#,0}",
    3792: "{0:#,0}",
    3793: "{0:#,0}",
    3795: "Kết Quả Lễ Hội: Ngày {0}",
    3797: "{0:#,0}",
    3799: "{0:#,0})",
    3800: "{0}",
    3801: "Tổng Cấp Công Trình: {0:#,0}",
    3803: "Kết Quả Lễ Hội Lần {0}",
    3806: "Sở Hữu: {0:#,0}",
    3807: "Nhân vật áp dụng: <color=#2be41d>{0}</color>",
    3810: "{0:#,0} (Còn {1:#,0})",
    3813: "<color=#FFFAEC>Tỉ Lệ Thu Thập Toàn Thể: </color><size=36>{0}</size><size=30>%</size>",
    3824: "Giới Hạn Lời Mời: {0}/{1}",
    3825: "Điểm Liên Minh: {0:#,0}",
    3826: "Số lần tinh luyện: <size=50>{0}</size>",
    3829: "Thành Viên Liên Minh: {0}/{1}",
    3830: "<color=#FFFAEC>Tổng Tiến Độ: </color>{0}%",
    3838: "Đã phân tích <size=50>{0}</size> lần",
    3840: "Không đủ Ma Tinh Thạch. (Yêu cầu: {0:#,0})",
    3846: "{0:#,0} điểm",
    3853: "<size=73%>Số lượng </size>{0}",
    3855: "<size=30>Thưởng Hỗ Trợ</size>\n+{0}%",
    3856: "{0:#,0}×<color=#39D09C>{1:#,0}</color>",
    3858: "<size=31>Điểm Phân Hạng</size> <color=#F2EC4E>{0:#,0}</color>",
    3859: "<color=#39D09C>{0:#,0}</color> Chuỗi Thắng!",
    3860: "Điểm: <color=#39D09C>{0:#,0}</color>",
    3865: "HP <color=#39D09C>+{0}%</color>",
    3871: "Rút Ngắn Thời Gian Xây: <color=#F2EC4E>{0}</color>",
    3872: "Công <color=#39D09C>+{0}%</color>",
    3877: "Nhân vật áp dụng: <color=#39D09C>{0}</color>",
    3878: "Đang Mậu Dịch... ({0}/{1})",
    3879: "Thủ <color=#39D09C>+{0}%</color>",
    3881: "Mậu Dịch Hoàn Tất ({0}/{1})",
    3883: "Còn lại <color=#ed4b39>{0}</color>/99",
    3884: "Còn {0:#,0} đến khi giải phóng",
    3889: "Còn lại <color=#ed4b39>{0}</color>/{1}",
    3892: "Còn lại <color=#ed4b39>{0}</color> lượt",
    3894: "<size=114%><color=#39D09C>{0:#,0}</color></size> Chuỗi Thắng!",
    3896: "<size=80%>Ngày quay thưởng: </size>{0}",
    3897: "<size=133%>Giải {0}</size>",
}

# Import sentences from test_pipeline
from test_pipeline import EXACT_SENTENCE_MAP
_combined = dict(EXACT_SENTENCE_MAP)
_combined.update(EXACT_ID_OVERRIDES)
EXACT_ID_OVERRIDES = _combined

def clean_punctuation(text):
    text = text.replace('、', ', ').replace('。', '. ').replace('！', '! ').replace('？', '? ')
    text = text.replace('：', ': ').replace('；', '; ').replace('（', '(').replace('）', ')')
    text = text.replace('「', '"').replace('」', '"').replace('『', '"').replace('』', '"')
    text = text.replace('・', ' - ').replace('‧', ' - ')
    text = text.replace('…', '...')
    text = text.replace('　', ' ')
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\s+([,.:;!?])', r'\1', text)
    return text.strip()

def polish_entry(item):
    item_id = item.get('id')
    en = item.get('en', '').strip()
    ja = item.get('ja', '').strip()
    zh = item.get('zh', '').strip()
    vi = item.get('vi', '').strip()

    # 0. Do NOT touch internal materials/shaders/fonts/errors
    if en.startswith('Common ') or en.startswith('Tenslafont') or en.startswith('zhTW ') or en.startswith('en_') or en.startswith('Ruby'):
        return en

    # 1. Exact ID Override (Highest Priority)
    if item_id in EXACT_ID_OVERRIDES:
        return EXACT_ID_OVERRIDES[item_id]

    # 2. Exact Sentence Override
    if en in SENTENCE_TRANSLATIONS:
        return SENTENCE_TRANSLATIONS[en]

    # 3. Exact Glossary Match
    if en in GLOSSARY:
        return GLOSSARY[en]

    # 4. Canonical Skills & Combat Map
    if en in EN_SKILL_AND_UI_MAP:
        return EN_SKILL_AND_UI_MAP[en]

    # 5. Canonical 764 UI Terms
    if en in DICT_764:
        return DICT_764[en]

    # 6. CJK Skills Translation
    if any(ord(c) > 0x3000 for c in en):
        translated_skill = translate_cjk(en, zh)
        if translated_skill and not any(ord(c) > 0x3000 for c in translated_skill):
            return clean_punctuation(translated_skill)

    # 7. If already translated in 'vi', apply systematic fixes and restore proper tone
    if vi and vi != en:
        res = vi
        for pat, rep in MISTRANSLATION_FIXES:
            res = re.sub(pat, rep, res)
        res = clean_punctuation(res)
        return unicodedata.normalize('NFC', res)

    # 8. Templates
    m_recruit = re.match(r'^Recruit x\{([0-9]+)\}(.*)$', en)
    if m_recruit:
        return f"Chiêu mộ x{{{m_recruit.group(1)}}}{m_recruit.group(2)}"

    m_awakened = re.match(r'^Awakened ([0-9]+)★$', en)
    if m_awakened:
        return f"Thức tỉnh {m_awakened.group(1)}★"

    m_rank = re.match(r'^(<[^>]+>)?Rank:?(</[^>]+>)?\s*\{0.*\}$', en)
    if m_rank:
        tag1 = m_rank.group(1) or ""
        tag2 = m_rank.group(2) or ""
        return f"{tag1}Hạng:{tag2} {{0:#,0}}"

    # 9. Fallback to existing 'vi' or 'en'
    fallback = vi if vi else en
    for pat, rep in MISTRANSLATION_FIXES:
        fallback = re.sub(pat, rep, fallback)
    fallback = clean_punctuation(fallback)
    return unicodedata.normalize('NFC', fallback)

def main():
    with open('ui_terms.json', 'r', encoding='utf-8') as f:
        terms = json.load(f)

    updated_count = 0

    for item in terms:
        orig_vi = item.get('vi', '')
        new_vi = polish_entry(item)
        new_vi = unicodedata.normalize('NFC', new_vi)

        if new_vi != orig_vi:
            updated_count += 1
            item['vi'] = new_vi

    print(f"Total entries processed: {len(terms)}")
    print(f"Updated entries: {updated_count}")

    with open('ui_terms.json', 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)
    print("Saved polished translations to ui_terms.json successfully!")

if __name__ == '__main__':
    main()
