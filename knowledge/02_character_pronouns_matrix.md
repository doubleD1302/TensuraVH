# 02 — MA TRẬN XƯNG HÔ & KHẨU KHÍ NHÂN VẬT

> Dự án: Việt hóa *Slime Isekai Memories*
> Dùng bởi: Agent 01 (xác định người nói – người nghe), Agent 02 (dịch), Agent 04 (bắt lỗi xưng hô).
> ⚠️ Các giá trị dưới đây là **mặc định đề xuất** dựa trên tính cách nguyên tác. Cột **Trạng thái**: `Chốt` = đã khóa; `Đề xuất` = có thể điều chỉnh. Khi bạn đã chốt, hãy sửa trực tiếp trong file này — mọi Agent sẽ coi file này là nguồn sự thật.

---

## 1. Nguyên tắc chung

1. **Mỗi nhân vật có một "bộ xưng hô gốc"** (tự xưng + cách gọi người đối diện). Bộ này **không đổi** trừ khi có **quy tắc ngoại lệ** (mục 4) hoặc cốt truyện thay đổi quan hệ (mục 5 file 05).
2. **Xưng hô phụ thuộc cặp (người nói → người nghe)**, không chỉ người nói. Luôn xét cả hai.
3. **Giữ cố định** trong suốt dự án. Nếu cùng một cặp mà bản dịch trước đó đã dùng cách khác → **báo Agent 04**, không tự đổi.
4. **Không có "tôi – bạn" mặc định.** Nếu không có trong ma trận → dùng cờ `UNKNOWN_PAIR` để người phụ trách quyết định, không tự đoán.
5. Với câu **không rõ người nói** → Agent 01 phải đoán theo ngữ cảnh + gắn cờ `LOW_CONFIDENCE_SPEAKER`; Agent 02 không được tự bịa.

---

## 2. Bảng nhân vật chính

### 2.1. Nhóm Rimuru & Tempest

| Nhân vật | Tự xưng | Gọi Rimuru | Khẩu khí / giọng | Trợ từ & tic đặc trưng | Trạng thái |
|---|---|---|---|---|---|
| **Rimuru Tempest** | *tôi* (thân mật/thường); *ta* (tuyên bố trang trọng với thuộc hạ/ kẻ địch) | — | Trẻ, thực dụng, hơi tếu, dễ chịu; lúc nghiêm túc thì lạnh và uy nghiêm | "nhỉ", "thôi", "hả"; hay tự giễu | Đề xuất |
| **Shion** | *tôi* | *Rimuru-sama* | Nhiệt huyết, tận tụy, hơi ngốc, bộc trực; khi giận thì đáng sợ | "ạ", "ạ!" mạnh mẽ; nói to | Đề xuất |
| **Shuna** | *em* hoặc *tôi* (chọn một và khóa) | *Rimuru-sama* | Dịu dàng, lễ phép, điềm đạm, nữ tính | "ạ", "ạ?", "nhé"; câu mềm | Đề xuất |
| **Benimaru** | *tôi* | *Rimuru-sama* | Điềm tĩnh, dứt khoát, phong thái tướng quân, nam tính | Câu ngắn, ít cảm thán; "thưa" | Đề xuất |
| **Souei** | *tôi* (ngắn, lạnh) | *Rimuru-sama* | Kiệm lời, lạnh, chuyên nghiệp, sắc | Rất ít trợ từ; câu cụt | Đề xuất |
| **Hakuro** | *lão* | *Rimuru-sama* | Cổ phong, uy nghiêm, từng trải, hơi gia trưởng | "Ngài", "lão phu" khi trang trọng; "vậy sao" | Đề xuất |
| **Rigurd / Rigur** | *lão* hoặc *tôi* (khi khiêm tốn) | *Rimuru-sama* | Trung thành, chững chạc, lễ độ của quan văn | "thưa ngài" | Đề xuất |
| **Gobta** | *em* | *Rimuru-sama* | Nhí nhố, nịnh, trẻ con, tự tin quá đà | "ạ", "nha", "nè", "hì hì" | Đề xuất |
| **Ranga** | *tại hạ* | *Chủ nhân* | Trung thành, uy dũng, trang nghiêm kiểu hiệp sĩ | "Thưa Chủ nhân" | Đề xuất |
| **Diablo** | *tại hạ* (lễ nghi) hoặc *tôi* | *Rimuru-sama* | Quý tộc, nịnh nọt có chiều sâu, lạnh lùng với kẻ khác | "Kufufufu...", "Thưa ngài" | Đề xuất |
| **Veldora** | *ta* | *Rimuru* (thân) hoặc *bằng hữu* | Hào sảng, ngạo nghễ, cười lớn | "Kuahahaha!", "bằng hữu", "ngươi" | Đề xuất |
| **Ramiris** | *tớ* | *Rimuru* hoặc *Rimuru-san* (tuỳ nguyên tác) | Trẻ con, ngang tàng, nịnh, hay làm màu | "nha", "nè", "đó" | Đề xuất |
| **Milim Nava** | *ta* | *Rimuru* | Ngây thơ, bốc đồng, kiêu ngạo kiểu trẻ con; thân thiết | "đó!", "nha!", "~" nhiều | Đề xuất |
| **Hinata Sakaguchi** | *tôi* | *Rimuru Tempest* (lạnh), có thể chuyển sang thân hơn sau Falmuth | Lạnh, sắc, kiên định; lời lẽ sắc bén | Câu ngắn, ít trợ từ | Đề xuất |
| **Guy Crimson** | *ta* | — | Ngạo mạn, thích thú, quyền lực tuyệt đối | "Ngươi", cười ngạo | Đề xuất |

> Lưu ý: Nhân vật mới trong game (gồm nhân vật "Ký Ức", nhân vật trong Thế Giới Gương) **phải được thêm vào mục 3** trước khi dịch.

---

## 3. Mẫu thêm nhân vật mới (dùng cho nhân vật gốc game / Thế Giới Gương)

Sao chép khối này vào cuối file mỗi khi có nhân vật mới:

```
### [Tên nhân vật]
- Tên gốc (JP/EN):
- Giới tính / tuổi hiển thị:
- Phe / vai trò:
- Tự xưng:
- Gọi Rimuru:
- Gọi người chơi (nếu có):
- Khẩu khí:
- Tic ngôn ngữ / trợ từ:
- Quan hệ đặc biệt:
- Trạng thái: Đề xuất / Chốt
```

---

## 4. Ma trận cặp (người nói → người nghe)

Chỉ liệt kê những cặp **khác với bộ xưng hô gốc** hoặc cần nhấn mạnh. Cặp không có trong bảng → dùng bộ gốc ở mục 2.

| Người nói → Người nghe | Tự xưng | Gọi đối phương | Ghi chú |
|---|---|---|---|
| Rimuru → Veldora | tôi / tớ | Veldora / ngươi (đùa) | Thân thiết, hay trêu |
| Rimuru → Milim | tôi | Milim | Thân, hơi nuông chiều |
| Rimuru → thuộc hạ (khi tuyên bố) | ta | các ngươi / các vị | Trang trọng, uy nghi |
| Rimuru → thuộc hạ (khi thường ngày) | tôi | tên + "-san"/bỏ hậu tố | Thân mật |
| Rimuru → Shion | tôi | Shion | Hơi bất lực, dịu |
| Rimuru → Hinata (lúc thù địch) | ta | ngươi / Hinata | Căng |
| Rimuru → Hinata (sau hòa giải) | tôi | Hinata | Thân dần |
| Rimuru → kẻ địch / Ma Vương địch | ta | ngươi | Lạnh, uy |
| Milim → Rimuru | ta | Rimuru | Thân, hồn nhiên |
| Veldora → Rimuru | ta | Rimuru / bằng hữu | Tin tưởng tuyệt đối |
| Diablo → ngoài Rimuru | tại hạ | ngươi / các hạ | Khinh khỉnh, lịch sự giả |
| Hinata → Rimuru (đầu) | tôi | ngươi / Rimuru | Cảnh giác |

---

## 5. Ngoại lệ & trường hợp đặc biệt

1. **Nhân vật giả vờ / che giấu thân phận** → dùng xưng hô *đúng với vai che giấu*, ghi chú trong output.
2. **Mất kiểm soát / điên loạn / cảm xúc cực độ** → xưng hô có thể "vỡ" (ví dụ: "ta" → "tao"). Chỉ dùng khi nguyên tác rõ ràng và Agent 01 gắn cờ `EMOTIONAL_BREAK`.
3. **Độc thoại nội tâm** → dùng "tôi" hoặc "mình"; không dùng bộ xưng hô đối thoại.
4. **Hệ thống / giọng máy (Đại Hiền Giả, Raphael)** → không có đại từ nhân xưng; dùng giọng khách quan, câu ngắn: "Đã xác nhận...".
5. **Ngôn ngữ gương (Thế Giới Gương)** → nếu nhân vật phiên bản gương có tính cách đối lập, **xưng hô có thể khác** bản gốc. Phải ghi rõ trong mục nhân vật.

---

## 6. Cách Agent dùng file này

- **Agent 01**: với mỗi câu thoại, xuất `speaker`, `listener`, rồi **tra bảng** để điền `addressing` (tự xưng + gọi đối phương). Nếu không tra được → `flags: ["UNKNOWN_CHARACTER"]` hoặc `["UNKNOWN_PAIR"]`.
- **Agent 02**: **bắt buộc** dùng `addressing` do Agent 01 cung cấp; không tự đổi.
- **Agent 04**: đối chiếu bản dịch với bảng này để bắt lỗi sai xưng hô, lệch khẩu khí, hoặc dùng trợ từ không hợp vai.
