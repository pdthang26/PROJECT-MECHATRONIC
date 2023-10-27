import cv2
import numpy as np

# Khởi tạo đối tượng camera
def detect (frame):
    obstructing_objects = []
    all_obstructing_objects = []

    # Chuyển đổi không gian màu từ BGR sang HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Định nghĩa phạm vi màu sắc cho việc nhận diện, trừ màu đen
    lower_color = np.array([0, 10, 10])
    upper_color = np.array([180, 180, 180])

    # Áp dụng ngưỡng màu để nhận diện màu sắc
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    # Áp dụng bộ lọc Gaussian để làm mờ ảnh và giảm nhiễu
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    # Tìm các đối tượng trong khung hình đã xử lý
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Vẽ khung hình chữ nhật xung quanh các đối tượng và lưu tọa độ
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Lưu tọa độ của góc dưới cùng bên trái
        bottom_left = (x, y + h)

        # Lưu tọa độ của góc dưới cùng bên phải
        bottom_right = (x + w, y)
        obstructing_objects = [bottom_left,bottom_right]
        all_obstructing_objects.append(obstructing_objects)
        # In ra tọa độ của góc dưới cùng bên trái và góc dưới cùng bên phải

    # Hiển thị khung hình gốc và khung hình đã xử lý
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Processed Frame', blurred)
    return all_obstructing_objects




camera = cv2.VideoCapture(0)

# Kiểm tra xem camera có khả dụng hay không
if not camera.isOpened():
    raise IOError("Không thể mở camera")

# Vòng lặp chạy liên tục để đọc và xử lý khung hình từ camera
while True:
    # Đọc khung hình từ camera
    ret, frame = camera.read()

    # Kiểm tra xem việc đọc khung hình thành công hay không
    if not ret:
        break

    print(detect(frame))

    # Kiểm tra xem người dùng có ấn phím 'q' để thoát khỏi vòng lặp hay không
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ hiển thị
camera.release()
cv2.destroyAllWindows()