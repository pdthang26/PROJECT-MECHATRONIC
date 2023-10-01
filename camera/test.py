import numpy as np
import matplotlib.pyplot as plt

# Kích thước của hình vẽ
width = 10
height = 5

# Vẽ hình vuông đại diện cho xe
plt.plot([-width/2, width/2, width/2, -width/2, -width/2],
         [-height/2, -height/2, height/2, height/2, -height/2], 'k')

# Vẽ vạch dọc
num_stripes = 8  # Số vạch dọc
stripe_width = 0.2  # Độ rộng của mỗi vạch

for i in range(num_stripes):
    x = i * stripe_width - width/2
    plt.plot([x, x], [-height/2, height/2], 'r--')

plt.axis('equal')  # Đảm bảo tỉ lệ trục x và y giống nhau
plt.xlabel('X')
plt.ylabel('Y')

# Hiển thị đồ thị
plt.show()