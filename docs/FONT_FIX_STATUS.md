# Sửa font Android — 2026-10-18

## Phạm vi và nguyên nhân

- Các công cụ cũ chuyển `đ` thành `d`, `ệ` thành `ê` và bỏ nhiều dấu khác. Pipeline hiện giữ nguyên văn bản từ `ui_terms.json`, chỉ chuẩn hóa NFC.
- Chỉ thay các term văn bản (TermType 0); giữ nguyên 338 tên tài nguyên font/material, tham chiếu và các slot ngôn ngữ còn lại.
- Font Common của game 5.0.0 (66043) nằm trong `split_android_assetpack.apk`. Chỉ tạo một font bundle trên máy tính hoặc chép nó vào một thư mục cache không chứng minh game sử dụng font đó.

## Hai bộ cài khác nhau

- `artifacts/fontfix-v1.1.1/Tensura_VietHoa_Shizuku_v1.1.1_unicode_preview.apk`: patcher có dữ liệu đầy đủ dấu. Đây là bản sửa pipeline văn bản; một mình APK này chưa sửa được font của game chính thức.
- `artifacts/game-fontfix-5.0.0-preview/`: bộ ba APK game dùng cho cài mới trong môi trường QA, có font Common bổ sung 103 ký tự và font dự phòng. Cả ba APK dùng cùng chữ ký thử nghiệm; chữ ký khác bản cửa hàng nên không cài đè được lên bản cửa hàng.

Không gỡ game đang chứa tài khoản để thử bộ QA. Điện thoại đã được hoàn tác bốn bundle thử về đúng bản sao lưu trước phiên test; bản phát hành `Tensura_VietHoa_Shizuku.apk` tại thư mục gốc không bị ghi đè.

## Kiểm tra

- I2: 3.902 term văn bản NFC; 338 term tài nguyên giữ nguyên.
- Font: 7.246 ký tự, thêm 103 ký tự; giữ nguyên glyph và ánh xạ cũ. 106.683 pixel thay đổi đều nằm trong vùng trống dự kiến của atlas.
- Build Android, zipalign, apksigner và đọc lại payload từ APK: đạt.
- Bộ APK game và patcher cài thành công trên giả lập Android API 36, hỗ trợ ARM64.
- Game vào được màn hình tiêu đề. Menu và hộp thoại đồ họa của bộ APK cuối hiển thị đầy đủ dấu, không thấy ô vuông trong các nhãn đã kiểm tra; đã lưu ảnh màn hình và `RUNTIME_QA.json` cùng bộ cài.
- Patcher 1.1.1 mở giao diện thành công, nhận đúng game 5.0.0. Giả lập chưa chạy Shizuku nên chưa kiểm thử thao tác cài/khôi phục qua Shizuku.
- Chưa kiểm tra hội thoại, chiến đấu, đăng nhập tài khoản hoặc toàn bộ màn hình trong game.
- Trên điện thoại trước khi hết pin: chỉ hộp thoại đồ họa thử nghiệm đã hiển thị đầy đủ dấu; chưa xác nhận bản sửa toàn game trên máy thật.

## Lệnh dựng lại tại máy hiện tại

```powershell
.\.venv\Scripts\python.exe patch_font_bundle.py
.\.venv\Scripts\python.exe import_i2_ui.py
.\.venv\Scripts\python.exe build_apk.py
.\.venv\Scripts\python.exe tools\build_game_fontfix.py
```

Cần bộ APK game gốc đúng phiên bản, font nguồn `test_font.ttf`, bundle Common gốc và I2 `.bak` sạch. Script xuất kết quả vào `artifacts/`, giữ nguyên các APK gốc. `BUILD_QA.json` ghi hash từng APK, chứng chỉ ký và phạm vi kiểm tra dữ liệu; kiểm tra tĩnh không thay thế kiểm tra hiển thị trong game.
