import numpy as np
import matplotlib.pyplot as plt

def calculate_angle(a1, a2, a3):
    # Chuyển đổi các vector thành dạng numpy array
    a1 = np.array(a1)
    a2 = np.array(a2)
    a3 = np.array(a3)

    # Tính toán vector hướng của đường thẳng A và B
    direction_A = a2 - a1
    direction_B = a3 - a2

    # Chuẩn hóa vector hướng
    normalized_direction_A = direction_A / np.linalg.norm(direction_A)
    normalized_direction_B = direction_B / np.linalg.norm(direction_B)

    # Tính toán góc giữa hai vector
    angle_rad = np.arccos(np.dot(normalized_direction_A, normalized_direction_B))
    angle_deg = np.degrees(angle_rad)

    return angle_deg

def plot_lines_and_angle(a1, a2, a3, ax):
    # Vẽ đường thẳng A
    ax.plot([a1[0], a2[0]], [a1[1], a2[1]], 'b-', label='A')

    # Vẽ đường thẳng B
    ax.plot([a2[0], a3[0]], [a2[1], a3[1]], 'r-', label='B')

    # Tính toán và vẽ góc giữa hai đường thẳng
    angle = calculate_angle(a1, a2, a3)
    angle_text = f'Angle: {angle:.2f} degrees'
    ax.text(a2[0], a2[1], angle_text, fontsize=10, ha='center')

# Ví dụ sử dụng:
a1 = (10, 0)
a2 = (10, 10)
a3 = (0, 15)
a4 = (12, 4)
a5 = (20, 0)
a6 = (0, 14)
arr = [a1, a2, a3, a4, a5, a6]

fig, ax = plt.subplots()

for i in range(len(arr) - 2):
    plot_lines_and_angle(arr[i], arr[i+1], arr[i+2], ax)

# Đặt tiêu đề và chú thích cho biểu đồ
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Lines and Angle')
ax.legend()

plt.grid(True)
plt.axis('equal')
plt.show()
