# 01 — QUY CHUẨN VĂN PHONG HÁN VIỆT & TỰ NHIÊN

> Dự án: Việt hóa *That Time I Got Reincarnated as a Slime: Isekai Memories* (Tensura – Slime Isekai Memories)
> Phạm vi: mọi Agent dịch (02, 03) và Agent hậu kiểm (04) đều phải tuân thủ file này.
> Nguyên tắc ưu tiên khi các luật mâu thuẫn: **04 (kỹ thuật) > 02 (xưng hô) > 01 (văn phong) > 03 (khuôn mẫu)**.

---

## 1. Triết lý dịch

1. **Tự nhiên trước, trung thành sau.** Người đọc Việt phải thấy câu văn như được viết bằng tiếng Việt, không phải "tiếng Nhật mặc áo Việt".
2. **Trung thành về ý, tình cảm, giọng điệu — không trung thành về cấu trúc câu.** Được phép tách câu, gộp câu, đảo trật tự, lược chủ ngữ/đại từ khi tiếng Việt tự nhiên hơn.
3. **Giữ chất Light Novel / Isekai**: giàu cảm xúc, có nhịp điệu, nhân vật nói đúng "chất" của mình (xem file 02).
4. **Không thêm, không bớt thông tin.** Chỉ được thêm/bớt từ ngữ mang tính ngữ pháp. Không tự bịa tình tiết, không tự giải thích bằng ngoặc đơn trừ khi file 05 cho phép.
5. **Nhất quán thuật ngữ tuyệt đối.** Một thuật ngữ — một cách dịch trong toàn dự án (xem mục 5).

---

## 2. Hán Việt: khi nào dùng, khi nào không

### 2.1. NÊN dùng Hán Việt
| Loại | Ví dụ |
|---|---|
| Chức danh, tước vị, cấp bậc | Ma Vương, Dũng Giả, Chân Long, Thánh Kỵ Sĩ, Quốc Vương, Đại Tướng |
| Tên kỹ năng, ma pháp, tuyệt chiêu mang tính "hoành tráng" | Đại Hiền Giả, Hắc Viêm, Thiên Ma Giáng Lâm |
| Khái niệm thế giới quan | Ma tố, Ma lực, Linh hồn, Thế Giới Gương, Liên Bang |
| Văn cảnh trang trọng, nghi lễ, tuyên bố, cổ phong | Lời tuyên bố của Ma Vương, hội nghị Walpurgis |

### 2.2. KHÔNG dùng Hán Việt (dùng thuần Việt)
- Hội thoại đời thường, đùa giỡn, bữa ăn, trò chuyện giữa đồng đội.
- Độc thoại nội tâm của Rimuru (giọng trẻ trung, hơi tếu, thực dụng).
- Mô tả cảm xúc cá nhân. Ví dụ: dùng "vui sướng", "bực mình", "hoảng quá" thay vì "hoan hỷ", "phẫn nộ", "kinh hoàng" (trừ khi nhân vật vốn nói văn vẻ).

### 2.3. Nguyên tắc cân bằng
- Một câu **không có quá 2 cụm Hán Việt nặng** liên tiếp trong văn cảnh đời thường.
- Nếu nghe giống "phim kiếm hiệp" mà bối cảnh không phải kiếm hiệp → đổi sang thuần Việt.
- Nhân vật cổ phong/uy nghiêm (Veldora, Hakuro, Rigurd, Guy, Diablo khi trang trọng) được phép đậm Hán Việt hơn.

---

## 3. Văn phong theo loại văn bản

| Loại | Giọng | Ghi chú |
|---|---|---|
| **Hội thoại** | Theo khẩu khí từng nhân vật (file 02). Ngắn, có nhịp, có ngắt câu bằng dấu phẩy/dấu ba chấm. | Không "giáo khoa". Không dùng "Tôi nghĩ rằng ..." nếu có thể nói "Tôi nghĩ ...". |
| **Độc thoại nội tâm** | Ngôi thứ nhất, trẻ, tếu, tự giễu. Đôi lúc "Raphael" chen vào bằng giọng máy móc, lạnh. | Nhận diện qua dấu ngoặc 「」, ( ), in nghiêng, hoặc cờ `is_inner_monologue` từ Agent 01. |
| **Dẫn truyện (narration)** | Ngôi thứ ba hoặc ngôi thứ nhất theo nguyên tác. Văn xuôi mượt, giàu hình ảnh nhưng không dài dòng. | Tránh lặp chủ ngữ. Có thể bỏ chủ ngữ khi ngữ cảnh rõ. |
| **Hệ thống / thông báo trong truyện** | Giọng "máy": lạnh, ngắn, chính xác. Ví dụ lời của Đại Hiền Giả: "Đã xác nhận. Kỹ năng ... đã được thu nhận." | Giữ nhất quán: *Đã xác nhận / Đã hoàn tất / Cảnh báo*. |
| **Tiếng cười / thán từ / tượng thanh** | Chuyển sang tiếng Việt tương đương, giữ cá tính. | Xem mục 8. |

---

## 4. Quy tắc câu chữ

### 4.1. Câu
- Độ dài mục tiêu: **tự nhiên theo nhịp thoại**. Hội thoại thường ≤ 25 từ/câu.
- Chủ ngữ tiếng Nhật hay bị lược → **đừng tự thêm chủ ngữ bừa**; lấy từ kết quả Agent 01 (người nói – người nghe) để quyết định.
- Tránh bị động kiểu "bị/được" tràn lan. Chỉ dùng khi thật sự có sắc thái bị hại/được lợi.

### 4.2. Từ nối & trợ từ cuối câu
Dùng vừa phải để tạo giọng, không lạm dụng: *nhỉ, nhé, nha, đấy, mà, chứ, hử, hả, nè, thôi, vậy*.
Mỗi nhân vật có "bộ trợ từ" riêng (file 02). Không dùng trợ từ lệch vai (ví dụ: Veldora không nói "nha nè").

### 4.3. Dấu câu
- Dùng dấu câu tiếng Việt chuẩn: `, . ! ? …`
- Dấu ba chấm: dùng **`...`** (3 dấu chấm ASCII) hoặc `…` — chọn **một kiểu** và giữ nhất quán toàn dự án. **Mặc định của dự án: `...`**.
- Dấu `~` kéo dài giọng: giữ nếu nhân vật có tính cách đó (Milim, Ramiris, Gobta), tối đa 1 lần/câu.
- Dấu ngoặc nhật 「」『』: chuyển thành `"..."` hoặc `'...'` **trừ khi nằm trong chuỗi mà file 04 yêu cầu giữ nguyên ký tự**.
- Không dùng dấu chấm than liên tiếp quá 2 (`!!`) trừ khi nguyên tác có ý nhấn mạnh đặc biệt.

### 4.4. Số, đơn vị, ngày giờ
- Số: dùng chữ số Ả Rập. Tách hàng nghìn bằng dấu chấm nếu UI hiển thị thủ công (`10.000`); nếu là biến số do game tự format thì **không đụng** (file 04).
- Phần trăm: `50%` (không cách).
- Thời gian: `3 giờ`, `30 phút`, `7 ngày`.

---

## 5. Thuật ngữ cố định (GLOSSARY GỐC)

> ⚠️ Đây là bản **đề xuất mặc định**. Nếu dự án đã có glossary chính thức, hãy ghi đè bảng này và giữ làm "nguồn sự thật duy nhất". Cột *Trạng thái* ghi rõ mức chốt.

| Gốc (EN/JP) | Bản dịch chuẩn | Trạng thái | Ghi chú |
|---|---|---|---|
| Rimuru Tempest | Rimuru Tempest | Chốt | Giữ nguyên Romaji |
| Tempest | Tempest | Chốt | |
| Jura Tempest Federation | Liên Bang Jura Tempest | Đề xuất | |
| Demon Lord | Ma Vương | Chốt | |
| Octagram | Bát Tinh Ma Vương | Đề xuất | Hoặc "Octagram" nếu game giữ nguyên |
| True Dragon | Chân Long | Chốt | |
| Hero | Dũng Giả | Chốt | |
| Great Sage | Đại Hiền Giả | Đề xuất | |
| Raphael | Raphael | Chốt | Giữ Romaji |
| Predator | Kẻ Săn Mồi | Đề xuất | Hoặc "Bổ Thực Giả" — chọn một |
| Magicule | Ma tố | Đề xuất | |
| Magic / Spirit magic | Ma pháp / Tinh linh ma pháp | Đề xuất | |
| Unique Skill | Kỹ năng Độc Nhất | Đề xuất | |
| Ultimate Skill | Kỹ năng Tối Thượng | Đề xuất | |
| Extra Skill | Kỹ năng Đặc Biệt | Đề xuất | |
| Common Skill | Kỹ năng Thường | Đề xuất | |
| Resistance | Kháng tính | Đề xuất | |
| Evolution | Tiến hóa | Chốt | |
| Namesake / Naming | Ban tên | Chốt | "Được ban tên" |
| Soul / Spirit | Linh hồn / Tinh linh | Chốt | |
| Slime | Slime | Chốt | Không dịch |
| Goblin / Orc / Ogre | Goblin / Orc / Ogre | Chốt | Giữ nguyên |
| Kijin | Quỷ nhân (Kijin) | Đề xuất | Lần đầu ghi kèm Romaji |
| Beastman | Thú nhân | Chốt | |
| Dwarf / Elf | Dwarf / Elf | Chốt | |
| Adventurer's Guild | Hội Mạo Hiểm Giả | Chốt | |
| Rank A / S ... | Hạng A / Hạng S ... | Chốt | |
| Walpurgis | Walpurgis | Chốt | Hội nghị Walpurgis |
| Mirror World | Thế Giới Gương | Chốt | Theo tên bạn cung cấp |
| Memory (card/character) | Ký Ức | Cần xác nhận | Tùy cách game gọi |

**Quy tắc tên riêng**
- Tên nhân vật, địa danh: **giữ Romaji**, không phiên âm Hán Việt (ví dụ: *Benimaru*, không dịch "Hồng Hoàn").
- Tên có nghĩa rõ ràng và game cũng dịch nghĩa → dịch nghĩa, ghi vào glossary.
- Lần đầu xuất hiện của thuật ngữ lạ trong cốt truyện có thể kèm Romaji trong ngoặc: *Quỷ nhân (Kijin)* — **chỉ khi** file 05 hoặc input cho phép.

---

## 6. Honorific (hậu tố kính ngữ)

| Gốc | Mặc định | Ghi chú |
|---|---|---|
| -sama | Giữ nguyên **-sama** khi gắn với Rimuru (*Rimuru-sama*); với nhân vật khác dịch theo quan hệ ("ngài", "đại nhân") | Chi tiết ở file 02 |
| -san | "anh/chị/cô/ông" theo tuổi + giới, hoặc giữ nguyên nếu là giọng thân thiện | |
| -kun / -chan | Bỏ hậu tố; thể hiện bằng cách xưng hô (em/cậu/nhóc/bé) | |
| -dono | "các hạ", "ngài" (cổ phong) | |
| -sensei | "thầy/cô" hoặc "sư phụ" tùy bối cảnh | |
| -senpai | "tiền bối" hoặc "anh/chị" | |

---

## 7. Tên riêng & chuỗi đặc biệt
- **Không dịch**: tên file, key, ID, tên biến, đường dẫn, mã sự kiện (file 04).
- **Không dịch**: nội dung nằm trong thẻ mà file 04 quy định là "bất khả xâm phạm".
- Tên kỹ năng của nhân vật: tham khảo file 03 về cách dịch tên kỹ năng.

---

## 8. Thán từ, tiếng cười, tượng thanh

| Gốc | Gợi ý (tùy nhân vật) |
|---|---|
| ふふふ / Fufufu | "Fufufu..." (giữ nguyên) hoặc "Hì hì hì..." (nhẹ nhàng) |
| ククク / Kukuku | "Kukuku..." (giữ nguyên, thường cho Diablo/phản diện) |
| ハハハ / Hahaha | "Ha ha ha!" |
| クアーハッハッハ / Kuahahaha | "Kuahahaha!" (Veldora — **giữ nguyên**) |
| えへへ | "Hì hì..." |
| ええっ!? | "Hả?!" / "Cái gì cơ?!" |
| まあ | "Ôi chao" / "Chà" (nữ) |
| ふむ | "Hừm" |
| ちっ | "Chậc" |

---

## 9. Danh sách LỖI CẤM

1. **Dịch sát chữ (word-by-word)**: "Tôi sẽ làm của tôi tốt nhất" ← sai; "Tôi sẽ cố hết sức" ← đúng.
2. **Lạm dụng "của", "những", "các", "đã", "sẽ"**.
3. **Lạm dụng đại từ "nó", "điều đó", "việc đó"** thay vì gọi thẳng đối tượng.
4. **Lặp chủ ngữ ở mỗi câu** (đặc sản của dịch máy).
5. **Xưng hô sai vai** (xem 02).
6. **Hán Việt quá liều trong thoại đời thường.**
7. **Để sót chữ Nhật/Anh** chưa dịch (trừ tên riêng giữ Romaji).
8. **Dịch lệch thuật ngữ** so với glossary.
9. **Tự ý thêm "ngoặc giải thích"** mà không được phép.
10. **Văn phong "thông báo hành chính"** trong cảnh cảm xúc.

---

## 10. Ví dụ Trước / Sau

| # | Bản dịch sát chữ ❌ | Bản tự nhiên ✅ | Lý do |
|---|---|---|---|
| 1 | "Tôi không thể tha thứ cho điều đó." | "Chuyện đó... tôi không thể bỏ qua được." | Bỏ "điều đó" cứng, thêm nhịp ngắt |
| 2 | "Bởi vì bạn là bạn của tôi, tôi sẽ giúp đỡ bạn." | "Là bạn bè thì giúp nhau thôi, có gì đâu." | Tự nhiên, không lặp đại từ |
| 3 | "Ta là Chân Long Veldora, và ta sẽ bảo vệ bạn của ta." | "Ta là Chân Long Veldora! Ai dám động đến bằng hữu của ta, kẻ đó chết chắc!" | Hợp khẩu khí, thêm khí thế |
| 4 | "Xin chào, Rimuru-sama. Tôi đã chuẩn bị bữa ăn." | "Rimuru-sama, bữa ăn đã sẵn sàng rồi ạ." | Lược chủ ngữ, thêm "ạ" |
