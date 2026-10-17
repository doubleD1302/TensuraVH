# 04 — LUẬT BẢO TOÀN THẺ CODE, BIẾN SỐ UNITY

> **ĐÂY LÀ FILE ƯU TIÊN CAO NHẤT.** Mọi luật dịch/văn phong khác đều phải nhường file này.
> Một lỗi ở đây có thể làm **crash game, vỡ giao diện, hoặc mất hiển thị chữ**. Không có ngoại lệ "cho đẹp câu".
> Dùng bởi: Agent 02, 03 (tuân thủ), Agent 04 (kiểm tra).

---

## 0. Nguyên tắc vàng

1. **Mọi thứ không phải chữ người đọc đều BẤT KHẢ XÂM PHẠM.** Chỉ dịch phần chữ người chơi sẽ đọc.
2. **Giữ nguyên số lượng và loại** thẻ, biến số, ký tự điều khiển. Không thêm, không bớt, không đổi chữ hoa/thường, không đổi khoảng trắng bên trong thẻ.
3. **Thẻ đi theo cặp**: mỗi thẻ mở phải có thẻ đóng tương ứng, **lồng đúng thứ tự**.
4. **Khi nghi ngờ → KHÔNG đụng**, trả về nguyên văn và gắn cờ `TECH_UNSURE`.
5. **Giữ nguyên cấu trúc dữ liệu** của input (JSON/CSV/TSV/XML): cùng key, cùng số dòng, cùng thứ tự.

---

## 1. Các loại thẻ và token cần bảo toàn

### 1.1. Thẻ Rich Text (Unity UI / TextMeshPro)

| Mẫu | Ví dụ | Quy tắc |
|---|---|---|
| Màu | `<color=#FF0000>...</color>`, `<color=red>...</color>` | Giữ nguyên mã màu; chỉ dịch chữ **bên trong** |
| Đậm / nghiêng / gạch | `<b>..</b>`, `<i>..</i>`, `<u>..</u>`, `<s>..</s>` | Giữ cặp, giữ vị trí tương đối |
| Cỡ chữ | `<size=24>..</size>`, `<size=120%>..</size>` | Giữ nguyên số |
| Căn lề / khoảng cách | `<align=center>`, `<indent=10%>`, `<line-height=..>`, `<space=..>`, `<pos=..>` | Giữ nguyên |
| Sprite / icon | `<sprite=3>`, `<sprite name="coin">`, `<sprite index=2>` | **Không dịch, không di chuyển** icon sang vị trí vô nghĩa |
| Link | `<link="id">..</link>` | Giữ ID, dịch chữ hiển thị |
| Font / vật liệu | `<font="...">`, `<material=..>` | Giữ nguyên |
| Không ngắt dòng | `<nobr>..</nobr>` | Giữ nguyên |
| Chỉ số trên/dưới | `<sup>`, `<sub>`, `<voffset=..>` | Giữ nguyên |
| Xuống dòng TMP | `<br>` | Giữ nguyên |
| Alpha / gradient | `<alpha=#80>`, `<gradient="..">` | Giữ nguyên |
| Vị trí kỹ năng (nếu game có) | `<skill=...>`, `<ruby=..>` | Giữ nguyên; xem mục 1.4 |

### 1.2. Biến số & chỗ giữ chỗ (placeholder)

| Mẫu | Ví dụ | Quy tắc |
|---|---|---|
| Số thứ tự | `{0}`, `{1}`, `{2:N0}`, `{0:F1}` | Giữ nguyên **cả định dạng** sau dấu `:` |
| Tên đặt | `{name}`, `{player}`, `{item}`, `{count}` | Giữ nguyên |
| Dấu ngoặc vuông | `[PlayerName]`, `[item]`, `[value]` | Giữ nguyên |
| Printf | `%s`, `%d`, `%f`, `%1$s`, `%02d`, `%%` | Giữ nguyên **cả thứ tự đối số** |
| Hai dấu ngoặc | `{{name}}`, `<<name>>`, `##name##` | Giữ nguyên |
| Tag tự định nghĩa | `$VAR$`, `@name@`, `%name%`, `#VAR#` | Giữ nguyên |
| Biến trong biểu thức | `{0}%`, `{1}s`, `x{0}` | Giữ nguyên **cả ký tự dính liền** |

> **Được phép dời vị trí** placeholder trong câu **chỉ khi** ngữ pháp tiếng Việt bắt buộc, và với điều kiện: (a) giữ đủ số lượng, (b) không tách rời khỏi ký tự dính liền (ví dụ `{0}%`), (c) với printf có thứ tự (`%1$s`) thì thứ tự chỉ số vẫn giữ nguyên.
> Với printf **không có chỉ số** (`%s %d`) → **không đổi thứ tự**; viết lại câu cho khớp thứ tự.

### 1.3. Ký tự điều khiển & escape

| Mẫu | Quy tắc |
|---|---|
| `\n`, `\r\n`, `\t` (dạng chữ trong chuỗi) | Giữ nguyên dạng ký tự; **không** chuyển thành xuống dòng thật hoặc ngược lại |
| Xuống dòng thật trong ô CSV/JSON | Giữ nguyên số dòng; không gộp/tách tùy ý |
| `\"`, `\\`, `\/`, `\uXXXX` trong JSON | Giữ nguyên; **không dịch**, **không escape thêm** |
| `&nbsp;`, `&lt;`, `&gt;`, `&amp;` | Giữ nguyên |
| Khoảng trắng đầu/cuối chuỗi | Giữ nguyên (nhiều khi là căn lề có chủ đích) |
| Ký tự đặc biệt `●`, `★`, `♪`, `→`, `※` | Giữ nguyên trừ khi ngữ cảnh rõ ràng là chữ thường |

### 1.4. Thẻ đặc thù game (cần xác nhận với đội kỹ thuật)

> ⚠️ Mục này **phải được điền** bởi người nắm kỹ thuật game. Ví dụ để Agent hiểu:

```
- <name>              → tên nhân vật/người chơi được game thay vào
- <chara=ID>          → tên nhân vật tra theo ID
- <wait=0.5>          → ngắt nhịp hội thoại (giây)
- <shake>..</shake>   → hiệu ứng rung chữ
- <emo=happy>         → biểu cảm nhân vật
- [pause]/[wait]      → ngắt nhịp
```
Nếu input xuất hiện thẻ **không có trong danh sách trên và không nhận ra** → xử lý theo quy tắc "khi nghi ngờ" (mục 0.4).

---

## 2. Dịch gì & không dịch gì

### 2.1. CHỈ dịch
- Văn bản nằm **bên ngoài** thẻ (người chơi đọc được).
- Văn bản nằm **giữa** cặp thẻ định dạng (`<color=..>CHỮ NÀY</color>`).

### 2.2. TUYỆT ĐỐI KHÔNG dịch
- **Key / ID / tên trường** (`"key": "str_001"`, `id=...`).
- **Tên file, đường dẫn, URL, tên asset** (`UI/icon_coin.png`, `https://...`).
- **Tên biến, tên hàm, tên lớp**.
- **Mã sự kiện, mã nhân vật, mã vật phẩm** (`CHR_0012`, `EVT_Mirror_01`).
- **Giá trị cấu hình** (`true/false`, `null`, số dùng cho logic).
- **Chuỗi nằm trong thẻ mà thẻ đó quy định "dữ liệu"** (ví dụ ID trong `<link="id">`).
- **Comment** của lập trình (`// ...`, `/* ... */`, `#...`) — giữ nguyên, trừ khi được yêu cầu dịch.

---

## 3. Cấu trúc dữ liệu

1. **JSON**: giữ nguyên dấu ngoặc, dấu phẩy, thứ tự key. Chuỗi tiếng Việt vẫn phải hợp lệ JSON (escape `"` thành `\"`, xuống dòng thành `\n`).
2. **CSV/TSV**: giữ nguyên số cột, số dòng. Nếu ô có dấu phẩy/ngoặc kép → bọc đúng chuẩn CSV (`"..."` và `""` cho ngoặc kép bên trong).
3. **XML/HTML**: giữ nguyên thẻ; chỉ dịch text node. Không dịch thuộc tính trừ khi là thuộc tính hiển thị (ví dụ `title`, `alt`) và được cho phép.
4. **I2/Unity Localization / PO / XLIFF**: giữ nguyên key/msgid; chỉ điền `msgstr`/`target`.
5. **Số dòng**: số dòng output **bằng** số dòng input. Không gộp hai dòng thoại, không tách một dòng thành hai trừ khi input quy định rõ.

---

## 4. Mã hóa & Unicode (rất quan trọng với tiếng Việt)

1. **UTF-8, không BOM** (trừ khi pipeline yêu cầu).
2. **Chuẩn hóa Unicode: NFC** (dạng tổ hợp, ví dụ `ệ` là **một** ký tự U+1EC7). **Không** dùng NFD (chữ + dấu rời) vì nhiều font Unity/TMP sẽ hiển thị lỗi dấu.
3. **Chỉ dùng ký tự có trong font Việt hóa của game.** Tránh ký tự hiếm: dấu nháy cong `“ ” ‘ ’`, dấu gạch dài `—`, `…` — nếu font không có sẽ hiện ô vuông. Mặc định dùng **dấu nháy thẳng** `" '` và gạch ngang `-`; dấu ba chấm dùng `...` (khớp file 01).
4. Không dùng emoji trừ khi bản gốc có và font hỗ trợ.
5. Không chèn ký tự vô hình (zero-width space, soft hyphen).
6. Khi có ghi chú về font (ví dụ font TMP chưa hỗ trợ dấu Việt) → báo cờ `FONT_RISK`, đừng tự thay ký tự.

---

## 5. Độ dài & hiển thị

1. Nếu input có `max_chars`, `max_lines`, `max_width` → **bắt buộc tuân thủ** (xem cách rút gọn ở file 03 mục 6).
2. Hội thoại có hộp thoại cố định: ưu tiên **≤ 2 dòng, mỗi dòng ≤ khoảng 35–40 ký tự** nếu input không nói rõ (đề xuất — chỉnh theo game thực tế).
3. **Không tự ý chèn `\n`** để ngắt dòng. Chỉ giữ `\n` có sẵn trong bản gốc (vị trí tương đương theo ý nghĩa).
4. Không thêm dấu cách thừa, không thêm dấu cách trước `! ? : ;`.

---

## 6. Quy trình tự kiểm tra (self-check) trước khi trả kết quả

Trước khi xuất kết quả, Agent 02/03 phải tự trả lời **CÓ** cho cả 8 câu:

1. Số lượng thẻ mở = số lượng thẻ đóng, đúng thứ tự lồng?
2. Mọi thẻ trong bản gốc đều còn trong bản dịch, **giữ nguyên chữ**?
3. Mọi placeholder (`{0}`, `%s`, `[Name]`...) còn đủ, đúng định dạng?
4. Không có thẻ/placeholder mới xuất hiện?
5. Ký tự điều khiển (`\n`, `\t`...) còn đủ?
6. Không dịch key/ID/đường dẫn?
7. Số dòng, cấu trúc dữ liệu khớp input?
8. Văn bản ở dạng NFC, không có ký tự lạ?

Nếu có **bất kỳ câu nào KHÔNG** → sửa lại. Không sửa được → trả nguyên văn + cờ `TECH_UNSURE` + giải thích ngắn.

---

## 7. Bảng lỗi thường gặp (để Agent 04 bắt)

| Mã lỗi | Mô tả | Mức độ |
|---|---|---|
| `TAG_MISSING` | Thiếu thẻ so với bản gốc | BLOCKER |
| `TAG_EXTRA` | Thừa thẻ | BLOCKER |
| `TAG_UNCLOSED` | Thẻ mở không đóng / lồng sai thứ tự | BLOCKER |
| `TAG_MODIFIED` | Sửa nội dung thẻ (mã màu, số, ID) | BLOCKER |
| `PH_MISSING` / `PH_EXTRA` | Thiếu/thừa placeholder | BLOCKER |
| `PH_FORMAT_CHANGED` | Đổi định dạng (`{0:N0}` → `{0}`) | BLOCKER |
| `PH_ORDER` | Đổi thứ tự printf không chỉ số | BLOCKER |
| `ESC_CHANGED` | Đổi `\n`/escape | BLOCKER |
| `KEY_TRANSLATED` | Dịch key/ID/đường dẫn | BLOCKER |
| `STRUCT_BROKEN` | Phá cấu trúc JSON/CSV, lệch số dòng | BLOCKER |
| `ENC_NFD` | Chữ tiếng Việt không ở dạng NFC | MAJOR |
| `CHAR_RISK` | Ký tự có thể thiếu trong font | MAJOR |
| `OVER_LIMIT` | Vượt giới hạn ký tự/dòng | MAJOR |
| `WS_CHANGED` | Đổi khoảng trắng đầu/cuối hoặc trong thẻ | MINOR–MAJOR |

---

## 8. Ví dụ

**Ví dụ 1 — Thẻ màu**
```
Gốc : <color=#FFCC00>Rimuru</color>が{0}ダメージを与えた！
Dịch: <color=#FFCC00>Rimuru</color> đã gây {0} sát thương!
```
✅ Giữ thẻ màu, giữ `{0}`.

**Ví dụ 2 — Placeholder đổi vị trí hợp lệ**
```
Gốc : {0}は{1}を手に入れた！
Dịch: {0} đã nhận được {1}!
```
✅ Thứ tự giữ nguyên.

**Ví dụ 3 — Lỗi (CẤM)**
```
Gốc : <b>HP</b> +{0}%
Dịch: <b>Máu</b> + {0} %      ❌ đổi "HP" (nếu glossary giữ HP), thêm khoảng trắng, tách "%"
Đúng: <b>HP</b> +{0}%
```

**Ví dụ 4 — printf**
```
Gốc : %sは%dレベルになった
Dịch: %s đã đạt cấp %d
```
✅ Giữ thứ tự `%s` rồi `%d`.

**Ví dụ 5 — JSON**
```
Gốc : {"id":"UI_0012","text":"確認\n本当に削除しますか？"}
Dịch: {"id":"UI_0012","text":"Xác nhận\nBạn có chắc muốn xóa không?"}
```
✅ Giữ `id`, giữ `\n`, JSON hợp lệ.
