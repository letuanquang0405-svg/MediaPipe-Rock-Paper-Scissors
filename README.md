# MediaPipe Rock–Paper–Scissors

Ứng dụng game **Oẳn tù tì bằng bàn tay** sử dụng webcam và MediaPipe Hand.

## 1. Ý tưởng

Người chơi đưa bàn tay trước webcam. MediaPipe phát hiện 21 landmark trên bàn tay. Chương trình tự xử lý tọa độ landmark để xác định người chơi đang ra:

- ROCK: ✊
- PAPER: ✋
- SCISSORS: ✌️

Sau đó máy tính chọn ngẫu nhiên một trong ba trạng thái và chương trình áp dụng luật oẳn tù tì để tính kết quả.

## 2. Công nghệ

- Python 3
- OpenCV
- MediaPipe
- Webcam

## 3. Cài đặt

Khuyến nghị tạo virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Cài thư viện:

```bash
pip install -r requirements.txt
```

Chạy:

```bash
python main.py
```

## 4. Điều khiển

- Đưa tay trước camera và giữ ROCK/PAPER/SCISSORS trong một khoảng ngắn để chơi một lượt.
- `R`: reset điểm.
- `Q`: thoát.

## 5. Thuật toán

MediaPipe Hand cung cấp 21 landmark của bàn tay. Mỗi landmark có tọa độ chuẩn hóa `(x, y, z)`.

Chương trình không dùng một bộ phân loại Rock/Paper/Scissors có sẵn. Thay vào đó:

1. Lấy landmark của bàn tay.
2. Tính khoảng cách từ các đầu ngón tay tới cổ tay.
3. So sánh đầu ngón với khớp PIP/MCP để xác định ngón đang duỗi.
4. Biểu diễn bàn tay bằng trạng thái 5 ngón:
   - 0 ngón duỗi → ROCK
   - 5 ngón duỗi → PAPER
   - ngón trỏ + ngón giữa duỗi, áp út + út co → SCISSORS
5. Các trạng thái khác được xem là `NONE`.
6. Để tránh một frame nhận sai làm chơi nhầm, gesture phải ổn định trong nhiều frame liên tiếp.
7. Máy chọn ngẫu nhiên.
8. So sánh hai lựa chọn và cập nhật điểm.

## 6. Cấu trúc

```text
mediapipe_rps/
├── main.py
├── requirements.txt
└── README.md
```

## 7. Lưu ý

Nếu webcam không mở được, kiểm tra quyền truy cập camera và đóng các ứng dụng khác đang sử dụng webcam.

Khi demo, nên đứng đủ sáng và đưa toàn bộ bàn tay vào vùng camera.
