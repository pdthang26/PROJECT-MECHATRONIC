import cv2
import numpy as np

# Tạo hình ảnh trắng
image = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Các điểm đầu vào
points = np.array([[100, 100], [90, 200], [70, 300], [50, 400]])

# Chuyển đổi các điểm đầu vào thành đường cong
curve = []
for t in np.arange(0, 1, 0.01):
    x = int((1 - t) ** 3 * points[0][0] + 3 * (1 - t) ** 2 * t * points[1][0] + 3 * (1 - t) * t ** 2 * points[2][0] + t ** 3 * points[3][0])
    y = int((1 - t) ** 3 * points[0][1] + 3 * (1 - t) ** 2 * t * points[1][1] + 3 * (1 - t) * t ** 2 * points[2][1] + t ** 3 * points[3][1])
    curve.append([x, y])

# Vẽ đường cong trên hình ảnh
curve = np.array(curve)
cv2.polylines(image, [curve], False, (0, 255, 0), 2)

# Hiển thị hình ảnh
cv2.imshow("Curve", image)
cv2.waitKey(0)
cv2.destroyAllWindows()