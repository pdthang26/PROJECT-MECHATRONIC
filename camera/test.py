import cv2
import numpy as np


vat  = [[(12,15),(16,15)],[(34,15),(23,15)],[(12,15),(16,15)]]
print(vat)

# def fill_bounded_regions(frame, points):
#     # Tạo một mảng NumPy từ danh sách các điểm
#     points_array = np.array(points, np.int32)

#     # Tạo mặt nạ (mask) từ đa giác bao quanh các điểm
#     mask = np.zeros_like(frame)
#     cv2.fillPoly(mask, [points_array], (0, 255, 0))

#     # Áp dụng mặt nạ lên frame
#     result = cv2.bitwise_and(frame, mask)

#     return result

# # Khởi tạo camera
# cap = cv2.VideoCapture(0)

# while True:
#     # Đọc frame từ camera
#     ret, frame = cap.read()

#     # Nếu không đọc được frame, thoát khỏi vòng lặp
#     if not ret:
#         break

#     # Mảng các điểm
#     points = [(100, 100), (200, 100), (200, 200), (100, 200)]

#     # Tô màu miền được bao quanh bởi các điểm trên frame
#     result = fill_bounded_regions(frame, points)

#     # Hiển thị frame với miền được tô màu
#     cv2.imshow("Filled Regions", result)

#     # Nhấn phím 'q' để thoát khỏi vòng lặp
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Giải phóng camera và đóng cửa sổ hiển thị
# cap.release()
# cv2.destroyAllWindows()