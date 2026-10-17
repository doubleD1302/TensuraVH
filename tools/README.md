# tools/validate_translation.py

Kiểm tra kỹ thuật bản dịch Unity (thẻ, biến số, escape, NFC, ký tự rủi ro font, giới hạn độ dài).
Chạy TRƯỚC Agent 04. Chỉ cần Python 3.8+, không cần cài thêm gì.

    python tools/validate_translation.py --selftest
    python tools/validate_translation.py data.json --out report.json --only-problems
    python tools/validate_translation.py --source jp.json --translation vi.json
    python tools/validate_translation.py data.csv --src-col source --tr-col translation

Mã thoát: 0 = đạt, 1 = có lỗi >= --fail-on (mặc định blocker), 2 = lỗi đầu vào.
Báo cáo JSON cùng định dạng với Agent 04 (summary + reports) nên có thể gộp chung.
Xem đầu file script để biết đầy đủ tuỳ chọn (--font-charset, --length-mode, --no-bracket, --fix-nfc...).
