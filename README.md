# Tensura ISEKAI Memories — Dự Án Việt Hóa & Ứng Dụng Cài Đặt Tự Động (TensuraVH)

Dự án Việt hóa tựa game **That Time I Got Reincarnated as a Slime: ISEKAI Memories** (`com.bandainamcoent.tensuramrkww`) trên nền tảng Android.

Ứng dụng patcher dùng **Shizuku** để chép dữ liệu bản dịch vào UnityCache mà không sửa APK game. Font trong APK tài nguyên được xử lý bằng bộ APK QA riêng; hai cách này có phạm vi và yêu cầu cài đặt khác nhau, được ghi tại [tình trạng sửa font](docs/FONT_FIX_STATUS.md).

AI làm việc trong dự án phải đọc [AGENTS.md](AGENTS.md), [luật kỹ thuật Unity](knowledge/04_unity_technical_rules.md) và [tri thức phòng lỗi font/mất dấu](knowledge/06_android_font_unicode_and_runtime_qa.md) trước khi sửa bản dịch, pipeline hoặc APK. Các kết quả test hiện có được ghi riêng tại [FONT_FIX_STATUS.md](docs/FONT_FIX_STATUS.md).

---

## 🌟 Tính Năng Nổi Bật

- **Dữ liệu Việt hóa**: 4.240 bản ghi, gồm 3.902 mục văn bản và 338 tên tài nguyên font/material cần giữ nguyên.
- **Không Cần Root (Hỗ trợ Shizuku)**: Tự động ghi dữ liệu bản dịch vào `UnityCache/Shared` của game chỉ với 1 chạm.
- **Giữ đầy đủ dấu tiếng Việt**: Dữ liệu được chuẩn hóa Unicode NFC. Không chuyển sang ISO-8859-1 hoặc bỏ dấu để né ô vuông. Font sửa đang được kiểm thử riêng; xem [tình trạng sửa font](docs/FONT_FIX_STATUS.md).
- **Tự Động Cập Nhật**: Tích hợp kiểm tra và cài đặt phiên bản mới trực tiếp từ GitHub Releases của repo `doubleD1302/TensuraVH`.
- **Khôi Phục Gốc Dễ Dàng**: Cho phép hoàn tác về tiếng Anh nguyên bản bất cứ lúc nào.

---

## 📱 Hướng Dẫn Cài Đặt & Sử Dụng

### Bước 1: Kích hoạt Shizuku
1. Cài đặt ứng dụng **Shizuku** từ [Google Play Store](https://play.google.com/store/apps/details?id=moe.shizuku.privileged.api) hoặc [GitHub](https://github.com/RikkaApps/Shizuku).
2. Mở Cài đặt điện thoại ➔ **Tùy chọn nhà phát triển** ➔ Bật **Gỡ lỗi qua Wi-Fi (Wireless Debugging)**.
3. Mở Shizuku và bấm **Ghép nối (Pairing)**, sau đó bấm **Bắt đầu (Start)** để chạy dịch vụ Shizuku.

### Bước 2: Cài đặt Tensura Việt Hóa
1. Tải file **`Tensura_VietHoa_Shizuku.apk`** từ mục [Releases](https://github.com/doubleD1302/TensuraVH/releases) và cài đặt vào điện thoại.
2. Mở ứng dụng **Tensura Việt Hóa**.
3. Khi app hiển thị yêu cầu quyền Shizuku, bấm **Cho phép (Allow)**.

### Bước 3: Cài đặt bản dịch vào game
1. Đảm bảo app hiển thị:
   - `🟢 Shizuku đã kết nối & cấp quyền`
   - `🟢 Đã cài đặt game Tensura (v5.0.0)`
2. Bấm nút **`🚀 CÀI ĐẶT BẢN VIỆT HÓA`**.
3. Chờ 2 giây cho đến khi app báo cài đặt thành công.
4. Bấm **`🎮 KHỞI ĐỘNG GAME NGAY`** để thưởng thức game bằng tiếng Việt!

---

## 🛠️ Cấu Trúc Dự Án

```
├── apk_builder/               # Mã nguồn ứng dụng Android Patcher (Java/XML/AAPT2)
│   ├── src/com/tensura/patcher/MainActivity.java  # Logic cài đặt cache, Shizuku pipe & auto-update
│   ├── res/                   # Giao diện giao diện người dùng tiếng Việt, layout, drawables
│   └── AndroidManifest.xml    # Cấu hình SDK 34, Shizuku API
├── knowledge/                 # Bộ quy tắc dịch thuật, ngôi xưng, văn phong & kỹ thuật Unity
├── agent/                     # Đặc tả quy trình AI Analyzer, Translator, QA Validator
├── tools/                     # Công cụ kiểm thử dịch thuật, quét font, giải mã asset bundle
├── ui_terms.json              # Dữ liệu dịch thuật tiếng Việt đầy đủ Unicode
├── ui_terms_safe.json         # Tên cũ được giữ tương thích; nội dung NFC, đầy đủ dấu
├── patch_font_bundle.py       # Công cụ nhúng 103 ký tự tiếng Việt vào TextMeshPro Font Atlas
├── build_apk.py               # Script tự động biên dịch, zipalign & ký APK
└── Tensura_VietHoa_Shizuku.apk # File cài đặt Android sẵn sàng sử dụng
```

APK patcher chỉ chép bản dịch vào UnityCache. Nó chưa thay được font Common nằm trong APK tài nguyên của bản game chính thức. Bộ APK game sửa font trong `artifacts/game-fontfix-5.0.0-preview/` là bản QA ký riêng, không phải bản cập nhật cài đè lên game từ cửa hàng.

---

## 📄 Bản Quyền & Giấy Phép

Dự án phục vụ mục đích phi thương mại cho cộng đồng yêu thích Tensura ISEKAI Memories tại Việt Nam. Toàn bộ tài nguyên game thuộc bản quyền của Bandai Namco Entertainment và tác giả Fuse.
