# BÁO CÁO ASSIGNMENT
# XÂY DỰNG ỨNG DỤNG TƯƠNG TÁC VỚI CAMERA SỬ DỤNG MEDIAPIPE

## 1. Giới thiệu

Assignment yêu cầu xây dựng một trò chơi hoặc ứng dụng tương tác với người dùng thông qua camera, sử dụng một chức năng phù hợp của MediaPipe. Quy trình tổng quát là:

Camera → MediaPipe → Dữ liệu → Thuật toán của sinh viên → Game/Application.

Trong bài này, em xây dựng ứng dụng **MediaPipe Rock–Paper–Scissors**, một trò chơi oẳn tù tì trong đó người dùng điều khiển lựa chọn bằng hình dạng bàn tay trước webcam.

Ứng dụng sử dụng MediaPipe Hand để thu thập vị trí các landmark của bàn tay. Từ những dữ liệu này, em tự thiết kế thuật toán xác định trạng thái của bàn tay và chuyển trạng thái đó thành ba lựa chọn ROCK, PAPER và SCISSORS.

## 2. Ý tưởng và mục tiêu

### 2.1. Ý tưởng

Người chơi đưa một bàn tay trước camera. Chương trình phát hiện bàn tay và xác định hình dạng:

- ROCK: nắm tay.
- PAPER: xòe bàn tay.
- SCISSORS: duỗi ngón trỏ và ngón giữa.

Sau khi người chơi đưa ra lựa chọn, máy tính chọn ngẫu nhiên một lựa chọn. Hai lựa chọn được so sánh theo luật oẳn tù tì và kết quả được hiển thị trên màn hình.

### 2.2. Mục tiêu

Ứng dụng nhằm minh họa đầy đủ quy trình:

Camera → MediaPipe Hand → Hand Landmarks → Thuật toán nhận diện → Luật game → Kết quả.

Mục tiêu quan trọng không chỉ là nhận diện được bàn tay mà còn xây dựng phần logic xử lý dữ liệu MediaPipe để tạo thành một ứng dụng có tương tác.

## 3. Input và Output

### 3.1. Input

Input trực tiếp của ứng dụng là hình ảnh/video từ webcam.

MediaPipe Hand xử lý hình ảnh và cung cấp các landmark của bàn tay. Mỗi bàn tay được biểu diễn bởi 21 landmark.

### 3.2. Output

Ứng dụng hiển thị:

- Hình ảnh camera.
- Các landmark và đường nối của bàn tay.
- Trạng thái bàn tay hiện tại.
- Lựa chọn của người chơi.
- Lựa chọn của máy.
- Kết quả của lượt chơi.
- Điểm số.

## 4. MediaPipe được sử dụng

Ứng dụng sử dụng chức năng **MediaPipe Hand**.

MediaPipe cung cấp vị trí các landmark trên bàn tay. Các landmark này được sử dụng làm dữ liệu đầu vào cho thuật toán do sinh viên xây dựng.

Thay vì sử dụng trực tiếp một nhãn ROCK/PAPER/SCISSORS do một mô hình phân loại cung cấp, chương trình sử dụng tọa độ landmark để tự suy luận trạng thái của từng ngón tay.

Điều này giúp phần xử lý của ứng dụng thể hiện rõ vai trò:

MediaPipe cung cấp dữ liệu → thuật toán của chương trình xử lý dữ liệu → tạo ra hành động trong game.

## 5. Thiết kế thuật toán

## 5.1. Xác định ngón tay duỗi hay co

Với các ngón trỏ, giữa, áp út và út, chương trình sử dụng khoảng cách từ đầu ngón tới cổ tay.

Gọi:

- W là landmark cổ tay.
- T là đầu ngón tay.
- P là khớp PIP.

Ta tính khoảng cách Euclid giữa các landmark.

Nếu đầu ngón tay có khoảng cách tới cổ tay lớn hơn khoảng cách của khớp PIP tới cổ tay, chương trình xem ngón tay đang duỗi.

Công thức:

d(A,B) = sqrt((xA-xB)^2 + (yA-yB)^2)

Sau đó:

distance(T, W) > distance(P, W)

thì ngón được xem là đang duỗi.

Với ngón cái, chương trình sử dụng khoảng cách giữa đầu ngón cái, cổ tay và khớp MCP để xác định trạng thái.

## 5.2. Chuyển trạng thái ngón thành gesture

Sau khi xác định trạng thái của năm ngón, chương trình áp dụng luật:

| Trạng thái | Gesture |
|---|---|
| Không có ngón duỗi | ROCK |
| Cả năm ngón duỗi | PAPER |
| Trỏ + giữa duỗi, áp út + út co | SCISSORS |
| Các trường hợp khác | NONE |

Như vậy, dữ liệu hình học từ MediaPipe được chuyển thành một trạng thái có ý nghĩa đối với game.

## 5.3. Bộ lọc ổn định

Camera xử lý từng frame nên trong một vài frame có thể xảy ra nhận diện không ổn định.

Ví dụ người chơi đang đưa ROCK nhưng chương trình có thể tạm thời nhận thành NONE hoặc SCISSORS.

Để giảm vấn đề này, chương trình sử dụng bộ lọc:

1. Lưu gesture hiện tại.
2. Nếu gesture giống frame trước thì tăng số frame liên tiếp.
3. Nếu gesture thay đổi thì bắt đầu đếm lại.
4. Chỉ chấp nhận gesture khi nó xuất hiện ổn định trong một số frame liên tiếp.

Cách này giúp game không phản ứng ngay với một frame nhiễu.

## 5.4. Luật game

Máy tính chọn ngẫu nhiên một trong:

ROCK, PAPER, SCISSORS.

Sau đó:

- ROCK thắng SCISSORS.
- SCISSORS thắng PAPER.
- PAPER thắng ROCK.
- Hai lựa chọn giống nhau → DRAW.

Điểm của người chơi, máy và số lượt hòa được cập nhật sau mỗi lượt.

## 6. Quy trình xử lý của chương trình

Mỗi frame được xử lý theo các bước:

### Bước 1: Nhận ảnh từ webcam

OpenCV đọc một frame từ camera.

### Bước 2: Chuyển đổi ảnh

Frame được chuyển từ BGR sang RGB trước khi đưa vào MediaPipe.

### Bước 3: MediaPipe Hand

MediaPipe tìm bàn tay và trả về các landmark.

### Bước 4: Xử lý landmark

Chương trình tính khoảng cách giữa các landmark để xác định ngón nào đang duỗi.

### Bước 5: Nhận diện gesture

Từ trạng thái năm ngón, chương trình xác định ROCK/PAPER/SCISSORS/NONE.

### Bước 6: Ổn định kết quả

Gesture cần xuất hiện ổn định trong nhiều frame trước khi được dùng để chơi.

### Bước 7: Máy chọn

Máy tính chọn ngẫu nhiên một gesture.

### Bước 8: Tính kết quả

Hai gesture được đưa vào hàm xử lý luật chơi.

### Bước 9: Hiển thị

Kết quả và điểm số được vẽ lên frame bằng OpenCV.

## 7. Pseudocode

```text
START

Open webcam
Initialize MediaPipe Hand

WHILE camera is running:
    Read frame
    Flip frame
    Convert BGR -> RGB

    Detect hand landmarks

    IF hand exists:
        Determine state of each finger
        IF 0 fingers extended:
            gesture = ROCK
        ELSE IF 5 fingers extended:
            gesture = PAPER
        ELSE IF index and middle are extended
                AND ring and pinky are folded:
            gesture = SCISSORS
        ELSE:
            gesture = NONE

    Apply stability filter

    IF a valid gesture is stable:
        computer = random(ROCK, PAPER, SCISSORS)

        Compare player and computer

        Update score
        Display result

    Display camera and information

    IF Q:
        BREAK

END
```

## 8. Kết quả thực nghiệm

Ứng dụng được thiết kế để nhận diện ba gesture chính.

### Trường hợp 1: ROCK

Người dùng nắm bàn tay. Không có ngón chính được xác định là duỗi.

Kết quả:

```text
Your hand: ROCK
```

### Trường hợp 2: PAPER

Người dùng xòe bàn tay. Các ngón được xác định là duỗi.

Kết quả:

```text
Your hand: PAPER
```

### Trường hợp 3: SCISSORS

Người dùng duỗi ngón trỏ và ngón giữa, đồng thời giữ ngón áp út và ngón út.

Kết quả:

```text
Your hand: SCISSORS
```

Sau khi nhận diện thành công, máy chọn một gesture và kết quả của lượt chơi được hiển thị.

## 9. Khó khăn

### 9.1. Gesture thay đổi giữa các frame

Do camera xử lý liên tục nên landmark có thể dao động. Điều này có thể khiến một gesture bị nhận diện sai trong một frame.

Giải pháp là sử dụng bộ lọc ổn định nhiều frame.

### 9.2. Điều kiện ánh sáng

Trong môi trường quá tối hoặc bàn tay bị che khuất, việc phát hiện landmark có thể không ổn định.

### 9.3. Các tư thế bàn tay không thuộc ba gesture

Không phải mọi hình dạng bàn tay đều là ROCK, PAPER hoặc SCISSORS. Vì vậy chương trình có trạng thái NONE để bỏ qua những trường hợp không phù hợp.

## 10. Hướng phát triển

Có thể phát triển ứng dụng theo các hướng:

- Thêm nhiều mức độ khó.
- Thêm hiệu ứng âm thanh.
- Thêm countdown trước mỗi lượt.
- Lưu lịch sử các lượt chơi.
- Thêm chế độ thi đấu nhiều điểm.
- Thiết kế giao diện đẹp hơn.
- Cho phép hai người chơi bằng hai bàn tay.
- Thêm thống kê tỷ lệ thắng/hòa/thua.

## 11. Kết luận

Ứng dụng đã minh họa quy trình sử dụng camera kết hợp MediaPipe để xây dựng một ứng dụng tương tác. MediaPipe đóng vai trò cung cấp dữ liệu landmark của bàn tay, trong khi phần xử lý trạng thái ngón tay, nhận diện gesture, ổn định kết quả và luật chơi được xây dựng trong chương trình.

Qua assignment, có thể thấy dữ liệu hình ảnh từ camera có thể được chuyển thành dữ liệu có cấu trúc thông qua MediaPipe, sau đó tiếp tục được xử lý bằng thuật toán để tạo ra tương tác trong một ứng dụng.
