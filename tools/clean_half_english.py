import json

with open('ui_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

# Comprehensive translations for the remaining partially-translated terms
CLEAN_TRANSLATIONS = {
    1463: "Trang bị chưa được rèn lại hoàn chỉnh hoặc chưa tiến hóa lên cấp tối đa sẽ không thể thức tỉnh.",
    1464: "* Bình hồi phục Thể lực có thể nhận từ các nhiệm vụ và Chợ Đổi Thưởng.",
    1548: "Sau khi xuất phát, điều kiện khiêu chiến không thể thay đổi cho đến khi bạn bắt đầu lại hoặc đổi tầng.\nBắt đầu chơi với điều kiện hiện tại?",
    1615: "Yêu Cầu Chi Viện Từ Bạn Kết Giao",
    1644: "Điểm thành công đã đạt tối đa.\nTrang bị đã được rèn lại mà không cần dùng nguyên liệu.",
    1759: "Sự kiện tiếp theo sẽ sớm diễn ra.\n(Chỉ người tham gia đạt hạng Dũng Giả trở lên mới có thể tham gia Trận Đua Bảng Xếp Hạng.)",
    1833: "Xác nhận với hiệu ứng Bùa Chú ở trên?",
    1839: "Sử dụng Bùa Chú có cấp hiệu ứng từ <color=#2be41d>2</color> trở lên để đặt lại?",
    1919: "Độ Gắn Kết của bạn tăng lên sau mỗi trận đấu Cúp Anh Kiệt.",
    1926: "Thông Báo Về Việc Kết Thúc Dùng Thử Miễn Phí Tháng Đầu Tiên",
    1928: "Sự kiện tiếp theo sẽ sớm diễn ra.\n(Chỉ người tham gia đạt hạng Kim Cương trở lên mới có thể tham gia Trận Đua Bảng Xếp Hạng.)",
    1992: "Trong <color=#2be41d>các trận đấu thường Cúp Anh Kiệt</color>, hiệu ứng sau sẽ kích hoạt cho cả bạn và đối thủ.",
    1993: "Trong <color=#2be41d>Trận Đua Bảng Xếp Hạng Cúp Anh Kiệt</color>, hiệu ứng sau sẽ kích hoạt cho cả bạn và đối thủ.",
    2271: "Bắt đầu lễ hội với các thiết lập bổ nhiệm ở trên?",
    2458: "Bạn phải đồng ý với Điều Khoản Dịch Vụ, Chính Sách Quyền Riêng Tư, Thông Báo Quảng Cáo Trong Ứng Dụng và Chấp Thuận Toàn Cầu để sử dụng dịch vụ này.\nNếu bạn là trẻ vị thành niên, bạn cần có sự đồng ý của cha mẹ hoặc người giám hộ hợp pháp.\nLưu ý: Hãy hỏi cha mẹ hoặc người lớn nếu bạn cần trợ giúp.",
    2459: "Bạn phải đồng ý với Điều Khoản Dịch Vụ, Chính Sách Quyền Riêng Tư và Thông Báo Quảng Cáo Trong Ứng Dụng để sử dụng dịch vụ này.\nNếu bạn là trẻ vị thành niên, bạn cần có sự đồng ý của cha mẹ hoặc người giám hộ hợp pháp.\nLưu ý: Hãy hỏi cha mẹ hoặc người lớn nếu bạn cần trợ giúp.",
    2482: "Khi bạn nhấn \"Tiếp\", một hộp thoại yêu cầu cấp quyền theo dõi sẽ xuất hiện.\n\nĐối với những bạn đã đồng ý nhắm mục tiêu quảng cáo ở màn hình trước, vui lòng nhấn chấp nhận trên hộp thoại.\n\n※Có thể tắt tính năng này bất kỳ lúc nào trong cài đặt thiết bị của bạn.",
    2508: "Bạn có thể nhận lại các phần thưởng sau đây.\n-<color=#2be41d>Phần Thưởng Tăng Hạng Lần Đầu</color>",
    2748: "* Phần thưởng có hiệu lực trong vòng ba ngày sau khi thời gian sự kiện kết thúc.",
    2890: "Số lần khiêu chiến Cúp Anh Kiệt không đủ.\nHồi phục số lần khiêu chiến?\n<color=#ed4b39>(Cần Lượt Khiêu Chiến: {0})</color>",
    2892: "Trong <color=#39D09C>Trận Đua Bảng Xếp Hạng Cúp Anh Kiệt</color>, hiệu ứng sau sẽ được kích hoạt cho cả bạn và đối thủ.",
    2893: "Trong <color=#39D09C>các trận đấu thường Cúp Anh Kiệt</color>, hiệu ứng sau sẽ được kích hoạt cho cả bạn và đối thủ.",
    3274: "Trong <color=#39D09C>Trận Đua Bảng Xếp Hạng Cúp Anh Kiệt Chiến Lược</color>, hiệu ứng sau sẽ được kích hoạt cho cả bạn và đối thủ.",
    3275: "Trong <color=#39D09C>các trận đấu thường Cúp Anh Kiệt Chiến Lược</color>, hiệu ứng sau sẽ được kích hoạt cho cả bạn và đối thủ.",
    3359: "Trong <color=#39D09C>các trận đấu thường Cúp Anh Kiệt Hoàng Đô</color>, hiệu ứng sau sẽ được kích hoạt cho cả bạn và đối thủ.",
    3360: "Trong <color=#39D09C>Trận Đua Bảng Xếp Hạng Cúp Anh Kiệt Hoàng Đô</color>, hiệu ứng sau sẽ được kích hoạt cho cả bạn và đối thủ.",
    3604: "Số lượt khiêu chiến trong Cúp Anh Kiệt không đủ.\nHồi phục lượt khiêu chiến?\n<color=#ed4b39>(Lượt khiêu chiến yêu cầu: {0})</color>",
    3630: "Cúp Anh Kiệt -Mùa {0}- Tuần {1}/{2} Đang Diễn Ra",
    3631: "Cúp Anh Kiệt -Mùa {0}- Tuần {1}/{2} Đã Kết Thúc",
    3748: "Trận Đua Bảng Xếp Hạng Cúp Anh Kiệt <size=40>- {0} -</size>",
    3817: "Cúp Anh Kiệt đã khởi động lại từ {0}.",
    3875: "Cúp Anh Kiệt Chiến Lược -Mùa {0}- Tuần {1}/{2} Đang Diễn Ra",
    3876: "Cúp Anh Kiệt Chiến Lược -Mùa {0}- Tuần {1}/{2} Đã Kết Thúc",
    3886: "Cúp Anh Kiệt Hoàng Đô -Mùa {0}- Tuần {1}/{2} Đang Diễn Ra",
    3887: "Cúp Anh Kiệt Hoàng Đô -Mùa {0}- Tuần {1}/{2} Đã Kết Thúc"
}

count = 0
for t in terms:
    tid = t.get('id')
    if tid in CLEAN_TRANSLATIONS:
        t['vi'] = CLEAN_TRANSLATIONS[tid]
        count += 1

print(f"Applied clean translations to {count} terms!")

with open('ui_terms.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, ensure_ascii=False, indent=2)

print("Saved ui_terms.json!")
