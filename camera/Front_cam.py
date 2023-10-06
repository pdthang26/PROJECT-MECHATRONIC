import cv2
import numpy as np

# Kích thước khung hình
frame_width = 640
frame_height = 480

# Tạo đối tượng VideoWriter để ghi video
focal_length = 1080  # Độ dài tiêu cự (focal length) của camera (đơn vị pixel)
sensor_width = 36  # Chiều rộng cảm biến của camera (đơn vị mm)
image_width = 640  # Chiều rộng hình ảnh (đơn vị pixel)
image_height = 480  # Chiều cao hình ảnh (đơn vị pixel)

# Kích thước của đường tròn trên mặt đất
ground_circle_radius = 1  # Bán kính đường tròn trên mặt đất (đơn vị mét)
# Tạo cửa sổ hiển thị camera
cv2.namedWindow("Camera")
# Tọa độ ban đầu của xe

# Kích thước và vị trí vùng an toàn
camera = cv2.VideoCapture(0)
while True:
    # Đọc khung hình từ camera
    ret, frame = camera.read()

    # Vẽ vùng an toàn
    # Lấy kích thước của khung hình
    height, width, _ = frame.shape

    # Tính toán các tọa độ của tam giác
    bottom_left = (0, height)  # Điểm bottom-left nằm ở góc dưới bên trái
    bottom_right = (width, height)  # Điểm bottom-right nằm ở góc dưới bên phải
    top_center = (int(width / 2), int(height / 2))  # Điểm top-center nằm ở giữa phía trên

    # Tạo mảng các điểm tạo nên tam giác
    points = np.array([bottom_left, bottom_right, top_center])

    # Vẽ tam giác lên khung hình
    cv2.drawContours(frame, [points], 0, (0, 255, 0), 2)
    

    # Tính toán bán kính của đường tròn trên hình ảnh
    pixel_radius = (focal_length * ground_circle_radius * image_width) / (sensor_width * 1000)

    # Vẽ đường tròn trên hình ảnh
    center = (image_width // 2, image_height // 2)  # Tìm tâm của hình ảnh
    color = (0, 255, 0)  # Màu xanh lá cây (BGR)
    thickness = 2  # Độ dày đường viền
    cv2.circle(frame, center, int(pixel_radius), color, thickness)

    

    # Hiển thị khung hình
    cv2.imshow("Camera", frame)

    # Thoát khỏi vòng lặp nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ hiển thị
camera.release()
cv2.destroyAllWindows()