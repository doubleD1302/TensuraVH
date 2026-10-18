# 06 — Font tiếng Việt Android: nguyên nhân, cách sửa và bằng chứng

Tri thức phòng lỗi cho AI dịch thuật, sửa Unity/TMP, viết patcher và dựng APK. Bài học từ phiên sửa Tensura ngày 2026-10-18. Đây là quy tắc dự án; chỉ dẫn cụ thể mới nhất của người dùng vẫn được ưu tiên.

## 1. Giữ đúng tiếng Việt trước khi xử lý font

**Ô vuông là lỗi cần chẩn đoán; bỏ dấu làm hỏng bản dịch.** Không dùng bất kỳ bước “font safe”, “zero tofu” hay “compatibility” nào để:

- Đổi `đ` thành `d`, `ệ` thành `ê`, `ắ` thành `á` hoặc chữ không dấu.
- Lọc bản dịch về ASCII, ISO-8859-1/Latin-1, hay xóa dấu sau khi phân rã NFD.
- Thay chữ bằng ký tự nhìn gần giống nhưng khác nghĩa/mã Unicode.
- Tự thêm hàng loạt thẻ font/sprite/voffset để che lỗi khi chưa chứng minh renderer và tài nguyên hỗ trợ.

Nguồn văn bản hiện tại là `ui_terms.json`. Chuẩn hóa **NFC**, giữ nội dung có dấu, thẻ, placeholder, escape và khoảng trắng có chủ đích. `ui_terms_safe.json` và `ui_terms_font_safe.json` chỉ là tên đầu ra tương thích cũ; nội dung vẫn phải đầy đủ dấu. NFC không khôi phục được dấu mà bước trước đã xóa: phải lấy lại từ nguồn canonical, không đoán dấu hàng loạt.

Phân biệt các trường hợp trước khi sửa:

| Dấu hiệu | Kiểm tra trước | Hướng xử lý |
|---|---|---|
| File đã chứa `Cài dat dô hoa` thay cho `Cài đặt đồ họa` | So sánh term và codepoint với nguồn canonical | Sửa bước biến đổi văn bản; không đổ lỗi cho font |
| File chứa đúng `đ`, `ệ`, `ắ` nhưng màn hình hiện ô vuông | Font asset thực tế, bảng ký tự và đường nạp | Bổ sung glyph/fallback và áp dụng vào đúng tài nguyên |
| Chữ và dấu bị tách, lệch vị trí | NFC/NFD và renderer | Giữ NFC; xác minh hỗ trợ dấu của renderer |
| Chuỗi có dạng mojibake hoặc ký tự thay thế U+FFFD | Encoding tại từng bước đọc/ghi | Sửa decode/encode; không thay ký tự thủ công để che lỗi |
| `<font="...">` hiện nguyên văn | Tài nguyên có được tìm thấy và thẻ có được renderer xử lý không | Hoàn tác thẻ thử; xác minh cơ chế nạp trước khi dùng tiếp |

Nếu chưa xử lý được font, giữ bản dịch đúng và gắn `FONT_RISK`. Không báo “đã sửa font” chỉ vì không còn ký tự ngoài Latin-1 trong file.

## 2. I2 chứa cả văn bản và định danh tài nguyên

Trong schema đã kiểm tra của game 5.0.0:

- `TermType == 0`: văn bản hiển thị, slot English là `Languages[1]`.
- `TermType == 6`: Material; `TermType == 9`: Font. Giá trị như `Common`, `Common Material`, `Ruby` là tên tài nguyên cần tra cứu.
- Snapshot có 4.240 bản ghi, gồm 3.902 term văn bản và 338 term tài nguyên. Đây không phải số lượng mặc định cho mọi bản cập nhật.

Không import bản dịch vào tất cả term chỉ vì chúng đều có trường `Languages`. Không đổi tên font/material trong một bước dịch thuật. Nếu một thử nghiệm kỹ thuật cần đổi định danh, phải xử lý đồng bộ mọi bên tham chiếu, giữ trong candidate riêng và chứng minh runtime; không lẫn nó vào payload văn bản đã duyệt.

`patch_text` và `validate_bundle` trong `tools/font_pipeline.py` thực hiện phạm vi văn bản: đối chiếu cây I2 với bản sạch, chỉ cho phép các thay thế English text từ canonical. Báo cáo `font_installation_verified: false` của phép kiểm này là đúng: nó không kiểm tra việc cài font.

## 3. Sửa đúng font mà game đang nạp

Truy vết theo thứ tự sau, không bỏ qua bước nào:

1. Chọn một nhãn lỗi có term ID và chuỗi mong đợi rõ ràng; lưu ảnh/file trước khi sửa.
2. Kiểm tra codepoint của chuỗi đã import, không chỉ nhìn file JSON đầu vào.
3. Xác định component TMP, `m_fontAsset`, material, atlas và fallback. Kiểm tra cả I2 Localize, `mTermSecondary` và `TranslatedObjects`: quá trình bản địa hóa có thể gán lại font/material khi cập nhật nhãn.
4. Lần theo `m_FileID`/`m_PathID`, serialized file/CAB, bundle và metadata/catalog. Ghi nơi chứa tài nguyên: bundle cache, APK asset pack hay tài nguyên khác.
5. Xác nhận đúng phiên bản bundle/APK trên thiết bị hoặc giả lập. Một file cache tồn tại, có quyền đọc hoặc có `__info` hợp lệ vẫn chưa chứng minh game đã dùng nó.
6. Thử một thay đổi nhỏ có thể quan sát để xác nhận đường nạp; sau đó hoàn tác thay đổi chẩn đoán. Ví dụ đổi tạm tỷ lệ một hộp thoại đã giúp xác nhận đúng bundle giao diện.
7. Áp dụng bản font vào đúng nguồn đã xác định, dựng/cài candidate, mở lại game và kiểm tra chính nhãn ban đầu.

Không suy ra tên thư mục cache/hash phiên bản từ tên nội bộ bundle, URL hoặc tên file APK. Phải đọc metadata và kiểm chứng thực tế; chúng không được coi là một định danh duy nhất.

Trong pipeline hiện tại, APK patcher Shizuku chỉ chép I2 vào UnityCache. Font Common của bản game chính thức được kiểm tra nằm trong `split_android_assetpack.apk`. Vì vậy build patcher thành công hoặc đóng gói một font vào I2 không đủ để tuyên bố đã thay font gốc. Đây là giới hạn đã quan sát của pipeline này, không phải kết luận về mọi game hay mọi cách dùng Shizuku.

## 4. Các thử nghiệm không được nhầm thành bản sửa đã đạt

| Thử nghiệm trong phiên 2026-10-18 | Kết quả quan sát | Bài học phải giữ |
|---|---|---|
| Bỏ dấu/lọc Latin-1 | Nhiều dấu biến mất khỏi văn bản | Không dùng cách này, kể cả đặt tên “safe” |
| Chép font vào những đường cache suy đoán | Chưa thấy tác động lên nhãn lỗi | Dừng đoán đường; xác minh catalog và nơi game nạp |
| Nhúng/gộp font vào I2, đổi tên font/material | Các bản thử chưa sửa được menu; có bản làm chữ biến mất | Không đưa các prototype này vào bản cuối; nguyên nhân của từng thất bại chưa được cô lập đầy đủ |
| Thêm sprite fallback hoặc khởi tạo font từ một nút Menu giả định | Chưa đạt hiển thị mong muốn; thẻ font có lúc hiện nguyên văn | Đối tượng/bundle tồn tại không có nghĩa nó được dùng ở màn hình đang test |
| Gán font trực tiếp cho hộp thoại đồ họa và chặn liên kết font cũ trong bản thử | Hộp thoại hiển thị được đầy đủ dấu | Chứng minh font có thể render ở hộp thoại đó; chưa chứng minh sửa toàn game |
| Thay font đúng trong APK tài nguyên và đưa bản dịch NFC vào I2 của APK | Menu tiêu đề và hộp thoại đồ họa hiển thị đủ dấu trên giả lập | Kết quả đạt đúng hai màn hình, đúng bộ APK cuối; chưa thay cho QA máy thật/hội thoại/chiến đấu |

Không diễn giải một thử nghiệm thất bại thành “cách này luôn bất khả thi”. Mỗi lần thử ghi giả thuyết, đầu vào, thay đổi, kết quả quan sát và bước tiếp theo. Khi đường nạp chưa được chứng minh, bước kế tiếp phải tăng khả năng quan sát, không tiếp tục nhân bản các đường dẫn đoán.

## 5. Bảo toàn dữ liệu khi sửa Unity/TMP và dựng APK

- Giữ glyph, ánh xạ ký tự và khả năng hiển thị ngôn ngữ gốc; không cắt font về Latin chỉ để giảm kích thước.
- Bổ sung cả character table, glyph table, metrics và pixel SDF tương ứng. Kiểm tra kích thước atlas, padding, Used/FreeGlyphRects, vùng trống và mọi tham chiếu. Không ghi đè pixel của glyph cũ.
- Xác minh atlas stream `.resS`, offsets và đường resource. Nếu sao chép đối tượng giữa serialized file, kiểm tra type index, script index, external PPtr và preload/container liên quan. Ưu tiên giữ nguyên shader và dữ liệu không cần sửa.
- Trong UnityPy 1.25.4 đã dùng, `save_typetree` rồi `read_typetree` trên cùng object có thể đọc lại dữ liệu reader cũ. Nếu phải sửa tiếp cùng cây qua nhiều hàm, giữ một cây thống nhất hoặc save/reload trước bước sau; đọc lại đầu ra cuối để bắt việc ghi đè mất thay đổi.
- Tránh dùng `env.container` khi chỉ cần liệt kê asset bundle của dump lớn: ở phiên này nó có thể kéo theo tìm dependency trên cả workspace. Đọc `AssetBundle.m_Container` từ object để kiểm tra có giới hạn.
- Dùng bản `.bak` sạch và input đúng phiên bản; không dùng một prototype đã sửa làm baseline. Không tự ghi đè APK nguồn hoặc APK phát hành tại thư mục gốc.
- Với asset pack hơn 3 GB, lần đóng gói đầu bằng ZIP64 đã bị zipalign từ chối. Quy trình hiện tại dùng ZIP32 cho archive vẫn nằm trong giới hạn 4 GiB. Không áp dụng điều chỉnh ngưỡng ZIP32 cho archive vượt giới hạn; phải kiểm tra lại định dạng/kích thước và công cụ Android.
- Sau zipalign/ký, đọc lại font và I2 từ **APK đã ký** để đối chiếu payload. Kiểm tra chứng chỉ của cả ba split; ghi SHA-256 đầu ra.

## 6. Bằng chứng và cách báo kết quả

| Mức kiểm tra | Có thể kết luận | Chưa thể kết luận |
|---|---|---|
| Canonical → I2, bảo toàn term/NFC | Payload văn bản đúng phạm vi đã đối chiếu | Font được game dùng |
| Bảng glyph/atlas/dependency đạt | Tài nguyên font đạt các kiểm tra cấu trúc đã chạy | Chữ hiển thị đúng trên Android |
| Build, ký, zipalign, readback đạt | APK đã dựng đúng payload được kiểm tra | APK đã cài hoặc chạy được |
| Cài đặt đạt | Môi trường đó nhận bộ APK | Menu/hội thoại không lỗi font |
| Có ảnh runtime trên giả lập | Các nhãn/màn hình đã quan sát hiển thị đúng trên cấu hình đó | Máy thật, gameplay, mọi font/fallback đều đúng |
| Test máy thật | Phạm vi đã quan sát trên máy và APK tương ứng | Phát hành công khai hoặc toàn bộ nội dung đã QA |

`pass_scope`/mô tả phạm vi phải nói rõ môi trường, versionCode/versionName, hash APK, màn hình, chuỗi mẫu, kết quả và phần chưa test. Lưu ảnh màn hình thật, không tạo ảnh mô phỏng rồi gọi là ảnh game. Không gán kết quả cho APK mới nếu hash/snapshot khác bản đã test.

Mẫu báo cáo ngắn: “APK đã ký và cài được; menu tiêu đề và đồ họa hiển thị đủ dấu trên giả lập API 36. Chưa test bộ APK cuối trên điện thoại thật, hội thoại, chiến đấu hoặc cài/khôi phục qua Shizuku.”

Thiếu thiết bị không cấm dựng candidate hoặc test giả lập theo yêu cầu. Nó chỉ giới hạn kết luận. Không dùng các từ “đã hết lỗi toàn game”, “Zero-Tofu”, “an toàn không bị chặn” hoặc “đã phát hành” khi chưa có bằng chứng cho đúng điều đó.

## 7. Thiết bị, chữ ký và hoàn tác

- Chỉ định serial cho mọi lệnh ADB; đừng để một lệnh tự chọn giữa điện thoại thật và giả lập.
- Trước **mỗi** lần chạm, kiểm tra cửa sổ tiền cảnh và màn hình. Nếu màn hình không khớp điều kiện dự kiến thì không chạm theo tọa độ cũ. Trong phiên này một lần chuyển sang ứng dụng khác đã làm lệnh chạm đi sai ứng dụng; không được lặp lại.
- Lưu bản sao/hash trước khi ghi thử, quản lý danh sách chính xác các file đã thay/tạo. Khi thử thất bại hoặc dừng test, phục hồi file gốc và xóa đúng file thử do mình tạo; không quét xóa cache của game.
- Không clear data, gỡ game đang có tài khoản, hoặc dùng lệnh cài có hành vi xóa dữ liệu chỉ để vượt lỗi chữ ký. Bộ APK game QA ký riêng không cài đè được lên bản cửa hàng. Mặc định dùng một cài đặt mới trong giả lập QA.
- Khi người dùng ngừng test trên điện thoại/hết pin, chuyển sang phần công việc được phép tiếp tục và ghi giới hạn. Không tiếp tục chạm điện thoại.
- Giữ APK phát hành và ghi chú phát hành do người dùng quản lý. Candidate local và ảnh test không tự cho phép thay bản công khai.

## 8. Snapshot đã xác nhận — không dùng thay việc kiểm tra bản mới

| Mục | Giá trị của bản đã kiểm tra |
|---|---|
| Game | Tensura ISEKAI Memories 5.0.0, versionCode 66043 |
| Engine fallback dùng khi đọc bundle | Unity 2022.3.62f1; phải đối chiếu khi đổi input |
| Font Common | `CAB-67016901c4c8650c7761bba7d8915099`, pathID `5214114523134854813` |
| Font trong asset pack | `assets/assetpack/d5237ef8d9fe3a291e11c946bf02eefb/393eec1fce69c0a4e940258aa3c47e9c.bundle` |
| I2 trong asset pack | `assets/assetpack/7365c0463fafdb5bba0fb614f04c92be/99e26f569e2f542bc8463a25d058128b.bundle` |
| Glyph Common | 7.143 ký tự gốc → 7.246; bổ sung 103 ký tự |
| Atlas | 4096 × 4096 Alpha8; 106.683 pixel sửa đều trong vùng trống đã kiểm tra |
| Kết quả runtime | Giả lập API 36, ARM64 qua native translation, menu tiêu đề và đồ họa đạt |

Nguồn kiểm tra trong dự án:

- [Tình trạng và giới hạn](../docs/FONT_FIX_STATUS.md).
- [Validator văn bản và font](../tools/font_pipeline.py).
- [Build patcher Unicode](../build_apk.py) và [build bộ APK game QA](../tools/build_game_fontfix.py).
- [Báo cáo build của phiên thử](../artifacts/game-fontfix-5.0.0-preview/BUILD_QA.json).
- [Báo cáo runtime, hash và ảnh](../artifacts/game-fontfix-5.0.0-preview/RUNTIME_QA.json).

Hai báo cáo trong `artifacts/` là bằng chứng local bị Git bỏ qua; có thể không tồn tại trên checkout khác. Nếu thiếu, ghi “chưa có bằng chứng tại checkout này”, không tự tái tạo nội dung PASS từ tài liệu.
