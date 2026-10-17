# 03 — KHUÔN MẪU DỊCH HIỆU ỨNG KỸ NĂNG & GIAO DIỆN (UI)

> Dùng bởi: Agent 03 (dịch UI & kỹ năng), Agent 04 (hậu kiểm).
> Mục tiêu: **cô đọng, nhất quán, vừa khung hiển thị**, không văn vẻ.
> Luật kỹ thuật (thẻ, biến số) nằm ở file 04 và **luôn thắng** file này khi có mâu thuẫn.

---

## 1. Nguyên tắc chung cho UI & Kỹ năng

1. **Ngắn gọn.** Tiếng Việt thường dài hơn tiếng Nhật 1,5–3 lần về số ký tự. Luôn ưu tiên từ ngắn, bỏ từ thừa.
2. **Nhất quán thuật ngữ.** Một khái niệm → một cách gọi (bảng mục 3).
3. **Không dùng văn nói** trong UI (trừ thông báo thân thiện được phép ở mục 5).
4. **Không chấm câu thừa**: nhãn nút không có dấu chấm cuối. Mô tả kỹ năng kết thúc bằng dấu chấm.
5. **Viết hoa**: chỉ viết hoa chữ đầu câu/nhãn và tên riêng. Không VIẾT HOA TOÀN BỘ trừ khi bản gốc làm vậy ở nhãn đặc biệt.
6. **Tôn trọng giới hạn ký tự**: nếu input có `max_chars`, bản dịch **không được vượt**. Nếu vượt → rút gọn theo thứ tự ưu tiên ở mục 6.

---

## 2. Tên kỹ năng

| Loại | Cách dịch | Ví dụ |
|---|---|---|
| Kỹ năng đã có trong glossary (file 01) | Dùng đúng bản dịch glossary | Đại Hiền Giả |
| Tên kỹ năng "hoành tráng" (tuyệt chiêu) | Hán Việt, 2–4 âm tiết, có nhịp | "Thiên Ma Giáng Lâm" |
| Tên kỹ năng thường (đánh thường/hồi máu) | Thuần Việt hoặc Hán Việt ngắn | "Chém Mạnh", "Hồi Phục" |
| Tên kỹ năng có tên riêng Romaji | Giữ Romaji + dịch nghĩa nếu cần | "Kuro-Ka Enbu" → "Hắc Viêm Vũ" (cần xác nhận) |
| Tên mang tính chơi chữ | Dịch ý, giữ vần/nhịp nếu được, ghi chú `PUN_NOTE` | |

**Quy ước định dạng tên kỹ năng**
- Tiêu đề: viết hoa chữ cái đầu mỗi từ chính (ví dụ: *Thiên Ma Giáng Lâm*).
- Tên kỹ năng khi nhắc trong mô tả: để trong **ngoặc kép** `"..."` hoặc theo định dạng game quy định (xem file 04 nếu có thẻ).

---

## 3. Từ vựng UI & chỉ số chuẩn

### 3.1. Chỉ số chiến đấu
| Gốc | Tiếng Việt | Ghi chú |
|---|---|---|
| HP | HP | Giữ nguyên |
| MP | MP | Giữ nguyên |
| ATK / Attack | Công | Hoặc "Tấn công" nếu có đủ chỗ |
| DEF / Defense | Thủ | Hoặc "Phòng thủ" |
| SPD / Speed | Tốc | Hoặc "Tốc độ" |
| CRIT Rate | Tỉ lệ Bạo kích | |
| CRIT DMG | ST Bạo kích | ST = Sát thương |
| DMG / Damage | Sát thương | |
| Heal | Hồi phục | |
| Shield | Khiên / Giáp chắn | Chọn một và khóa |
| Cooldown | Hồi chiêu | |
| Duration | Thời gian hiệu lực | |
| Buff | Tăng cường | |
| Debuff | Suy yếu | |
| Stun | Choáng | |
| Poison | Độc | |
| Burn | Thiêu đốt | |
| Freeze | Đóng băng | |

### 3.2. Hệ thống game
| Gốc | Tiếng Việt |
|---|---|
| Summon / Gacha / Pull | Triệu hồi |
| Stamina | Thể lực |
| Quest / Mission | Nhiệm vụ |
| Daily | Hằng ngày |
| Weekly | Hằng tuần |
| Event | Sự kiện |
| Shop | Cửa hàng |
| Inventory / Bag | Túi đồ |
| Equipment | Trang bị |
| Level Up | Nâng cấp / Lên cấp |
| Awakening | Thức tỉnh |
| Limit Break | Phá giới hạn |
| Evolve | Tiến hóa |
| Skill Level Up | Nâng cấp kỹ năng |
| Party / Team | Đội hình |
| Friend | Bạn bè |
| Guild / Alliance | Hội / Liên minh (chọn một) |
| Ranking | Bảng xếp hạng |
| Reward | Phần thưởng |
| Claim | Nhận |
| Auto | Tự động |
| Skip | Bỏ qua |
| Retry | Thử lại |
| Settings | Cài đặt |
| Notice / News | Thông báo |
| Login Bonus | Quà đăng nhập |
| Memory (card) | Ký Ức *(cần xác nhận)* |

### 3.3. Nút bấm chuẩn
| Gốc | Tiếng Việt |
|---|---|
| OK | OK |
| Yes / No | Có / Không |
| Confirm | Xác nhận |
| Cancel | Hủy |
| Close | Đóng |
| Back | Quay lại |
| Next | Tiếp |
| Start | Bắt đầu |
| Retry | Thử lại |
| Save | Lưu |
| Delete | Xóa |
| Use | Sử dụng |
| Details | Chi tiết |

---

## 4. Khuôn mẫu mô tả kỹ năng

### 4.1. Cấu trúc câu chuẩn

```
[Hành động] [Mục tiêu] [Hiệu ứng/Giá trị] [Điều kiện/Thời gian].
```

### 4.2. Mẫu theo loại

| Loại | Mẫu | Ví dụ |
|---|---|---|
| Sát thương đơn | Gây {X}% ATK sát thương lên 1 kẻ địch. | Gây 250% ATK sát thương lên 1 kẻ địch. |
| Sát thương diện rộng | Gây {X}% ATK sát thương lên toàn bộ kẻ địch. | |
| Hồi phục | Hồi {X}% HP cho 1 đồng minh. | |
| Buff | Tăng {Chỉ số} của {mục tiêu} thêm {X}% trong {N} lượt. | Tăng Công của toàn đội thêm 30% trong 3 lượt. |
| Debuff | Giảm {Chỉ số} của {mục tiêu} đi {X}% trong {N} lượt. | |
| Hiệu ứng trạng thái | Có {X}% xác suất gây {Trạng thái} trong {N} lượt. | Có 50% xác suất gây Choáng trong 1 lượt. |
| Nội tại (Passive) | [Nội tại] {Điều kiện}: {hiệu ứng}. | [Nội tại] Khi HP dưới 30%: tăng Công 20%. |
| Điều kiện kích hoạt | Khi {điều kiện}, {hiệu ứng}. | |
| Hồi chiêu | Hồi chiêu: {N} lượt. | Hồi chiêu: 4 lượt. |
| Tiêu hao | Tiêu hao {N} MP. | |

### 4.3. Từ nối chuẩn
- "lên", "cho", "của", "trong", "khi", "nếu", "đồng thời", "và".
- **Không** dùng "để", "nhằm", "với mục đích" trừ khi bắt buộc.

### 4.4. Quy tắc trình bày hiệu ứng nhiều dòng
- Mỗi hiệu ứng **một dòng** (giữ nguyên thẻ xuống dòng của file 04).
- Thứ tự: sát thương → hiệu ứng phụ → điều kiện đặc biệt → hồi chiêu.

---

## 5. Thông báo, lỗi & hướng dẫn

| Loại | Giọng | Ví dụ |
|---|---|---|
| Lỗi hệ thống | Trung tính, rõ ràng | "Không thể kết nối. Vui lòng thử lại." |
| Xác nhận hành động | Ngắn, hỏi thẳng | "Bạn có muốn dùng 10 Thể lực?" |
| Thành công | Ngắn | "Đã nhận phần thưởng." |
| Thiếu tài nguyên | Nêu rõ thiếu gì | "Không đủ Thể lực." |
| Hướng dẫn tân thủ | Thân thiện, câu ngắn, có thể dùng "nhé" | "Chạm vào màn hình để tiếp tục nhé." |
| Cảnh báo | Rõ ràng, không dọa | "Hành động này không thể hoàn tác." |

**Xưng hô với người chơi:** mặc định dùng **"bạn"**. Nếu game có nhân vật hướng dẫn nói với người chơi → theo ma trận file 02.

---

## 6. Thứ tự rút gọn khi vượt giới hạn ký tự

Áp dụng **lần lượt** đến khi vừa:
1. Bỏ từ thừa ("một", "những", "của" không cần thiết).
2. Thay cụm dài bằng từ Hán Việt ngắn tương đương.
3. Dùng viết tắt chuẩn (ST = Sát thương; Tốc = Tốc độ).
4. Rút gọn cấu trúc câu (bỏ chủ ngữ, dùng danh từ hóa).
5. **Không bao giờ** cắt thẻ, biến số, số liệu hoặc đơn vị (file 04).
6. Nếu vẫn không vừa → trả về bản tốt nhất + cờ `OVER_LIMIT` + đề xuất để người phụ trách quyết định.

---

## 7. Ví dụ đầy đủ

| Gốc (mô phỏng) | Bản dịch |
|---|---|
| "Deals 300% ATK damage to one enemy and has a 30% chance to stun for 1 turn." | "Gây 300% ATK sát thương lên 1 kẻ địch, có 30% xác suất gây Choáng trong 1 lượt." |
| "Restores 20% of max HP to all allies." | "Hồi 20% HP tối đa cho toàn đội." |
| "When HP is below 30%, increase ATK by 20%." | "Khi HP dưới 30%: tăng Công thêm 20%." |
| "Not enough Stamina." | "Không đủ Thể lực." |
