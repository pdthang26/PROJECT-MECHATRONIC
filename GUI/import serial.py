import serial

# Khởi tạo đối tượng Serial với cổng và tốc độ baudrate tương ứng
ser = serial.Serial('COM2', 9600)  # Thay đổi '/dev/ttyUSB0' thành cổng UART thực tế và '9600' thành baudrate thích hợp

while True:
    # Đọc dữ liệu từ UART
    data = ser.readline().decode().strip()
    
    # Kiểm tra xem dữ liệu có bắt đầu bằng 'A' không
    if data.startswith('A'):
        # In ra phần sau ký tự bắt đầu 'A'
        print(data[1:])