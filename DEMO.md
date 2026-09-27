# KỊCH BẢN DEMO

## 1. Chuẩn bị

- Máy tính có webcam.
- Đã cài Python và các thư viện trong requirements.txt.
- Chạy `python main.py`.

## 2. Demo chức năng nhận diện

Đưa tay vào camera.

### Demo ROCK

Nắm tay lại.

Màn hình phải hiển thị:

`Your hand: ROCK`

### Demo PAPER

Xòe bàn tay.

Màn hình phải hiển thị:

`Your hand: PAPER`

### Demo SCISSORS

Duỗi ngón trỏ và ngón giữa, co ngón áp út và ngón út.

Màn hình phải hiển thị:

`Your hand: SCISSORS`

## 3. Demo một lượt chơi

Ví dụ người chơi ra ROCK.

Chương trình cho máy chọn ngẫu nhiên.

Nếu máy ra SCISSORS:

`YOU WIN!`

Điểm người chơi tăng lên 1.

## 4. Demo bộ lọc

Có thể di chuyển tay hoặc thay đổi gesture để cho thấy chương trình không lập tức chốt kết quả từ một frame duy nhất.

## 5. Demo reset

Nhấn `R`.

Điểm số trở về:

`You 0 - 0 Computer`

## 6. Kết thúc

Nhấn `Q` để đóng chương trình.

## 7. Nội dung nên nói khi thuyết trình

"Đầu tiên camera cung cấp hình ảnh cho chương trình. MediaPipe Hand phát hiện bàn tay và trả về 21 landmark. Từ các landmark này, em tự tính khoảng cách để xác định từng ngón đang duỗi hay co. Sau đó em dùng trạng thái của năm ngón để nhận diện Rock, Paper hoặc Scissors. Khi gesture ổn định trong nhiều frame, chương trình tạo một lượt chơi, máy chọn ngẫu nhiên và áp dụng luật oẳn tù tì để tính điểm."

## 8. Nếu giảng viên hỏi: "MediaPipe làm gì?"

"MediaPipe chủ yếu cung cấp landmark của bàn tay. Phần chuyển landmark thành Rock/Paper/Scissors là logic do em xây dựng."

## 9. Nếu giảng viên hỏi: "Tại sao cần bộ lọc nhiều frame?"

"Camera xử lý liên tục nên landmark có thể dao động giữa các frame. Nếu lấy ngay một frame thì có thể nhận sai gesture. Em yêu cầu gesture ổn định trong một số frame liên tiếp để giảm nhiễu."

## 10. Nếu giảng viên hỏi: "Thuật toán có gì của em?"

"Em tự thiết kế cách xác định ngón duỗi/co bằng quan hệ khoảng cách giữa các landmark, sau đó ánh xạ trạng thái năm ngón thành ba gesture và xây dựng bộ lọc ổn định cùng luật tính điểm."
