# Hướng dẫn AI — Tensura Việt hóa

Áp dụng cho dự án Tensura ISEKAI Memories trong thư mục này, package Android `com.bandainamcoent.tensuramrkww`. Không áp dụng cấu trúc font/cache của dự án game khác vào đây nếu chưa kiểm tra.

## Đọc trước khi làm

- Mọi thay đổi bản dịch, import/export, font, patcher hoặc build phải đọc [luật kỹ thuật Unity](knowledge/04_unity_technical_rules.md) và [tri thức sửa font Android](knowledge/06_android_font_unicode_and_runtime_qa.md).
- Xem [tình trạng kiểm thử hiện tại](docs/FONT_FIX_STATUS.md) trước khi tiếp tục sửa font. Các đường dẫn, hash, số lượng và phiên bản trong tài liệu là snapshot; phải đối chiếu với bản đang xử lý.
- Khi dùng các vai trò dịch/QA, đọc prompt tương ứng trong `agent/` cùng tri thức mà prompt yêu cầu.

## Quy tắc không được lặp lại lỗi

1. **Không bỏ dấu để né ô vuông.** Không đổi `đ → d`, `ệ → ê`, không lọc về ASCII/Latin-1 hoặc xóa combining mark. Giữ bản dịch đầy đủ dấu, chuẩn hóa NFC; thiếu glyph thì gắn `FONT_RISK` và sửa đường nạp/font.
2. **Không dịch tên tài nguyên.** Trong schema I2 đã kiểm tra, chỉ thay English text của `TermType == 0`; giữ các term font/material, ID, tham chiếu, placeholder và các ngôn ngữ khác. Xác nhận lại schema/slot nếu game thay phiên bản.
3. **File font đã tạo không đồng nghĩa font đã được game dùng.** Truy vết nhãn → font/material → bundle/CAB → cache hoặc APK asset pack → gói thực tế đã cài. Không đoán đường cache từ tên bundle.
4. **Patcher và game APK là hai sản phẩm khác nhau.** `build_apk.py` dựng patcher chép văn bản I2; nó chưa thay font Common trong APK game chính thức. `tools/build_game_fontfix.py` dựng bộ APK game ký riêng cho QA. Không quảng bá patcher Unicode là bản sửa font toàn game.
5. **Báo kết quả đúng bằng chứng.** Tách build/ký/readback, cài đặt, hiển thị giả lập, máy thật, hội thoại/chiến đấu và phát hành. PASS ở một bước hoặc một hộp thoại không phải PASS toàn game. Thiếu máy thật vẫn được dựng/test giả lập theo yêu cầu, nhưng phải ghi phần chưa kiểm tra.
6. **Giữ bản gốc và đường hoàn tác.** Không tự ghi đè APK phát hành, APK game nguồn, `.bak` sạch hoặc dữ liệu tài khoản. Xuất candidate vào `artifacts/`. APK game ký thử không cài đè lên bản cửa hàng; không tự gỡ game/xóa dữ liệu để vượt lỗi chữ ký.
7. **Thử nghiệm có giới hạn.** Mỗi lần thử nêu giả thuyết, dùng một thay đổi có thể quan sát và kiểm tra đúng file đã nạp. Thử thất bại phải được đánh dấu và hoàn tác; không để gói thất bại trở thành payload cuối.
8. **Thao tác đúng thiết bị và ứng dụng.** Chỉ định serial rõ ràng; kiểm tra cửa sổ tiền cảnh và màn hình hiện tại trước mỗi lần chạm. Nếu ứng dụng khác đang mở thì dừng chuỗi chạm, xác nhận lại trạng thái và phạm vi được phép tiếp tục. Khi ngừng test, hoàn tác đúng các file thử đã ghi và dừng giả lập do mình mở nếu không cần nữa.

## Kiểm tra theo phạm vi thay đổi

- Văn bản: dùng `tools/font_pipeline.py::validate_bundle` để đối chiếu nguồn canonical và bảo toàn tên tài nguyên.
- Font: dùng `validate_font_bundle` để kiểm tra glyph, ánh xạ cũ và vùng atlas được sửa; kiểm tra thêm dependency/fallback nếu thay chúng.
- APK: zipalign, apksigner, cùng chứng chỉ giữa các split và đọc lại đúng payload từ APK đã ký.
- Hiển thị: test chính APK cuối, chụp nhãn có dấu, ghi phiên bản/hash và phạm vi vào báo cáo runtime. Không sửa/bịa kết quả PASS khi chưa nhìn thấy màn hình.
- Chỉ sửa tài liệu thì kiểm tra nội dung và liên kết; không cần dựng lại APK hoặc mở thiết bị.
