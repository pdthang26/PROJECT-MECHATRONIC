import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import serial.tools.list_ports
from PIL import ImageTk, Image
import serial
from math import *

# Tạo mảng bao gồm các thành phần trên giao diện
objects_0 = []
objects_1 = []

# Chức năng giao diện

uart = None
# Hàm cho nút connect
def connect_uart():
    global uart
    selected_port = com_port.get()
    selected_rate = int(rate_port.get())
    uart = serial.Serial(
        port=selected_port,
        baudrate=selected_rate,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1  # Timeout cho phép đọc từ giao diện UART
    )

# Hàm cho nút Open
def open_click():
    for obj in objects_0:
        obj['state'] = 'normal'
    long_display['text'] = 'hello'
    lat_display['text'] = 'hi'

# Hàm cho nút Close
def close_click():
    for obj in objects_0:
        obj['state'] = 'disabled'
    for obj in objects_1:
        obj['state'] = 'disabled'
    long_display['text'] = ''
    lat_display['text'] = ''
    com_port.set('')

# Tạo cửa sổ giao diện
root = tk.Tk()
root.geometry("1040x400")
root.configure(bg='#A8DF8E')
root.resizable(height=False, width=False)

'''Tạo các nhãn'''

# Tạo nhãn cho ô chọn cổng COM
com_label = tk.Label(root, text="COM Port:", bg='#A8DF8E')
com_label.place(x=180, y=5)

# Tạo nhãn cho ô chọn Baudrate
rate_label = tk.Label(root, text='Baud Rate', bg='#A8DF8E')
rate_label.place(x=300, y=5)

# Tạo nhãn cho Data Bits
data_label = tk.Label(root,text='Data Bit:',bg='#A8DF8E')
data_label.place(x=180,y=65)

#Tạo nhãn cho Parity Bit
parity_label = tk.Label(root,text='Parity Bit',bg='#A8DF8E')
parity_label.place(x=300,y=65)

# Tạo nhãn cho di chuyển trước và sau
back_wheel_label = tk.Label(root,text='Back Wheel Control',bg='#A8DF8E',font=('Arial',12,'bold'))
back_wheel_label.place(x=10,y=140)

# Tạo nhãn cho bánh trước
front_wheel_label = tk.Label(root,text='Front Wheel Control',bg='#A8DF8E',font=('Arial',12,'bold'))
front_wheel_label.place(x=205, y=140)

# Tạo nhãn cho phanh
brake_label = tk.Label(root, text = 'Brake Control',bg='#A8DF8E',font=('Arial',12,'bold'))
brake_label.place(x= 205, y= 265 )

# Tạo nhãn cho Longitude
long_label = tk.Label(root, text='Longitude', bg='#A8DF8E')
long_label.place(x=550, y=5)

# Tạo ô hiển thị cho Longitude
long_display = tk.Label(root, relief=tk.SUNKEN,anchor=tk.W, padx=10,bg='white')
long_display.place(x=550, y=30, height=30, width=230)

# Tạo nhãn cho Lattitude
lat_label = tk.Label(root, text='Lattitude', bg='#A8DF8E')
lat_label.place(x=800, y=5)

# Tạo ô hiển thị cho Lattitude
lat_display = tk.Label(root, relief=tk.SUNKEN,anchor=tk.W,padx=10,bg='white')
lat_display.place(x=800, y=30, height=30, width=230)

# Lấy danh sách tất cả các cổng COM
com_ports = [port.device for port in serial.tools.list_ports.comports()]

# Lấy danh sách Baud Rate
rate = [
    '1200', '1800', '2400', '4800', '9600', '19200', '28800', '38400',
    '57600', '76800', '115200', '230400', '460800', '576000', '921600']

''' Tạo các combobox cho các thông số liên quan tới UART'''
# Tạo ô chọn cổng COM
com_port = ttk.Combobox(root, values=com_ports, state='disabled')
com_port.place(x=180, y=30, height=30, width=100)
objects_0.append(com_port)

# Tạo ô chọn Baud Rate
rate_port = ttk.Combobox(root, values=rate, state='disabled')
rate_port.place(x=300, y=30, height=30, width=100)
rate_port.set(rate[4])
objects_0.append(rate_port)

# Tạo ô chọn Data Bits
data_port  = ttk.Combobox(root,values = ['7','8'],state='disabled')
data_port.place(x=180, y=90, height=30, width=100)
objects_0.append(data_port)

#Tạo ô chọn Parity Bit
parity_port = ttk.Combobox(root,values=['even','odd','none'],state='disabled')
parity_port.place(x=300,y=90,height=30,width=100)
objects_0.append(parity_port)

''' Tạo các nút '''
# Tạo nút Open
btn_open = tk.Button(root, text='Open', command=open_click,bg='white')
btn_open.place(x=10, y=30, height=30, width=70)

# Tạo nút Close
btn_close = tk.Button(root, text='Close', state='disabled', command=close_click,bg='white')
btn_close.place(x=90, y=30, height=30, width=70)
objects_0.append(btn_close)

# Tạo nút chọn cổng COM
select_button = tk.Button(root, text="Connect", state='disabled', command=connect_uart,bg='white')
select_button.place(x=415, y=30, height=30, width=70)
objects_0.append(select_button)

''' chức năng auto'''
# Tạo nút Auto
btn_auto = tk.Button(root, text='Auto', state='disabled',bg='white')
btn_auto.place(x=10, y=90, height=30, width=70)
objects_0.append(btn_auto)

''' Chức năng manual'''
# Hàm chức năng cho nút Manual
def manual_click():
    for obj in objects_1:
        obj['state'] = 'normal'

# Tạo nút Manual
btn_manu = tk.Button(root, text='Manual', state='disabled',bg='white',command= manual_click)
btn_manu.place(x=90, y=90, height=30, width=70)
objects_0.append(btn_manu)

''' Tạo frame cho bánh sau'''
back_frame = tk.Frame(root, width=185, height=215, highlightbackground='red', highlightthickness=2,bg='#A8DF8E')
back_frame.place(x= 10, y= 170)

'''Khai báo biến direction'''
direction = 0

'''Code cho nút forward'''
# Hàm cho nút forward để đổi hình khi ấn
def forward(event):

    global forward_btn,direction
    if btn_forward['state'] != 'disabled':
        if event.type == '4':  # ButtonPress event
            # Mở ảnh khi nút được nhấn
            forward_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/2.png')
            #truyền UART cho bánh sau
            if uart.is_open:
                back_for_adc = linear_scale.get()
                direction = "F"
                uart.write(bytearray([ord(direction),back_for_adc]))
            else:
                messagebox.showwarning('Warning','Please connect the UART')
        else:
            # Mở ảnh mặc định khi nút được thả ra
            forward_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/1.png')
            # truyền UART cho bánh sau
            if uart.is_open:
                back_for_adc = 0
                uart.write(bytes([back_for_adc]))
            else:
                messagebox.showwarning('Warning','Please connect the UART')

    btn_forward['image'] = forward_btn

# Mở ảnh 
forward_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/1.png')

# Tạo nút forward
btn_forward = tk.Button(back_frame, image=forward_btn, borderwidth=0, state='disabled', bg='#A8DF8E')
btn_forward.place(x=10, y=10, height=90, width=90)
objects_1.append(btn_forward)

# Gắn sự kiện cho nút forward
btn_forward.bind('<ButtonPress-1>', forward)
btn_forward.bind('<ButtonRelease-1>', forward)

''' Code cho Reverse Button '''
# Hàm cho nút Reverse để dổi hình khi ấn
def reverse(event):

    global reverse_btn,direction

    if btn_reverse['state']!='disabled': # check trạng thái của nút
        if event.type == '4':  # ButtonPress event
            # Mở ảnh khi nút được nhấn
            reverse_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/4.png')
            #truyền UART giá trị tốc độ cho bánh sau
            if uart.is_open:
                back_rev_adc = linear_scale.get()
                direction = "R"
                uart.write(bytearray([ord(direction),back_rev_adc]))
            else:
                messagebox.showwarning('Warning','Please connect the UART')
        else:
            # Mở ảnh mặc định khi nút được thả ra
            reverse_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/3.png')
            #truyền UART giá trị tốc độ cho bánh sau
            if uart.is_open:
                back_rev_adc = 0
                uart.write(bytes([back_rev_adc]))
            else:
                messagebox.showwarning('Warning','Please connect the UART')

    btn_reverse['image']= reverse_btn

# Mở ảnh
reverse_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/3.png')

# Tạo nút Reverse
btn_reverse = Button(back_frame, image=reverse_btn, bg='#A8DF8E', borderwidth=0, state='disabled')
btn_reverse.place(x=10, y=110, width=90, height=90)
objects_1.append(btn_reverse)

# Gắn sự kiện cho nút reverse
btn_reverse.bind('<ButtonPress-1>', reverse)
btn_reverse.bind('<ButtonRelease-1>', reverse)

''' Thanh điều tốc cho bánh sau '''
linear_scale = tk.Scale(back_frame, from_=0, to=100, orient=tk.VERTICAL,bg='white',
                        showvalue=True,state='disabled')
linear_scale.set(0)
linear_scale.place(x = 120, y= 10,height = 190)
objects_1.append(linear_scale)

'''Tạo frame cho bánh trước'''
front_frame = tk.Frame(root,height=85, width=315,bg='#A8DF8E',highlightbackground='red',highlightthickness=2)
front_frame.place(x=205,y=170)

''' Code cho tạo thanh trượt rẽ trái phải'''
#truyền UART bánh trước
def turn_slide(value):
    turn_adc = int(value)
    if turn_adc < 0:
        orient = 'L'
    else:
        orient = 'R' 

    uart_data = bytearray([ord(orient),abs(turn_adc)])
    if uart.is_open:
        uart.write(uart_data)  

# Tạo ô trượt điều khiển trái phải
turn_scale = tk.Scale(front_frame, from_=-100, to=100, orient=tk.HORIZONTAL,bg='white',bd=1, 
    tickinterval=25, showvalue=True,troughcolor='white',state='disabled',command=turn_slide)
turn_scale.set(0)
turn_scale.place(x = 5, y= 5, height= 70, width = 300)
objects_1.append(turn_scale)


'''Tạo frame cho phanh'''
brake_frame = tk.Frame(root,height=90,width=315,bg='#A8DF8E',highlightbackground='red',highlightthickness=2)
brake_frame.place(x=205,y=295)

''' Code cho nút phanh'''
# Hàm cho nút Brake để đổi hình khi ấn
def brake(event):

    global brake_btn

    if btn_brake['state']!='disabled':
        if event.type == '4':  # ButtonPress event
            # Mở ảnh khi nút được nhấn
            brake_btn = PhotoImage(file='D:/STUDYING\Mechatronic Project/PROJECT-MECHATRONIC/GUI/b_2.png')
            # truyền uart cho adc cho phanh
            if uart.is_open:
                brake_adc = brake_slide.get()
                uart.write(bytes([brake_adc]))
        else:
            # Mở ảnh mặc định khi nút được thả ra
            brake_btn = PhotoImage(file='D:/STUDYING\Mechatronic Project/PROJECT-MECHATRONIC/GUI/b_1.png')
            # truyền uart cho adc cho phanh
            if uart.is_open:
                brake_adc = 0
                uart.write(bytes([brake_adc]))

    btn_brake['image']= brake_btn

# Mở ảnh
brake_btn = PhotoImage(file='D:/STUDYING\Mechatronic Project/PROJECT-MECHATRONIC/GUI/b_1.png')

# Tạo nút Brake
btn_brake = Button(brake_frame, image=brake_btn, bg='#A8DF8E', borderwidth=0, state='disabled')
btn_brake.place(x=10, y=10, width=70, height=70)
objects_1.append(btn_brake)

# Gắn sự kiện cho nút reverse
btn_brake.bind('<ButtonPress-1>', brake)
btn_brake.bind('<ButtonRelease-1>', brake)

'''Code cho thanh trượt độ lớn xung cấp cho phanh'''
brake_slide = tk.Scale(brake_frame,from_=0,to=100,orient=tk.HORIZONTAL,bg='white',bd=1,tickinterval=25,
                       showvalue=True,troughcolor='white',state='disabled')
brake_slide.set(0)
brake_slide.place(x=85,y=10,width=220,height=70)
objects_1.append(brake_slide)

# Chạy vòng lặp giao diện
root.mainloop()