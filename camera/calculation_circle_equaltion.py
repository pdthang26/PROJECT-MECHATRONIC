def lagrange_interpolation(data, x):
    n = len(data)
    result = 0

    for i in range(n):
        xi, yi = data[i]

        # Tính giá trị của hàm Lagrange cho điểm x
        term = yi
        for j in range(n):
            if j != i:
                xj, _ = data[j]
                term *= (x - xj) / (xi - xj)

        result += term

    return result

# Mảng dữ liệu mẫu (x, y)
data = [(1, 2), (2, 4), (3, 6), (4, 8)]

# Giá trị x cần nội suy để tìm giá trị tương ứng y
x = 2.5

# Tính giá trị y bằng phương pháp nội suy Lagrange
y = lagrange_interpolation(data, x)

print(f"Gia tri y tai x = {x} la: {y}")