import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import serial.tools.list_ports
from PIL import ImageTk, Image
import serial
from math import *

'''Tạo các biến cần thiết cho chương trình'''

# biến màu giao diện
GUI_color = '#C9F4AA'

# biến màu frame Manual
manu_color = '#F7C8E0'

# Tạo mảng bao gồm các thành phần trên giao diện
objects_0 = [] # mảng cho nút để active các elements trong open và disable tất cả trong close
objects_1 = [] # mảng chứa các thành phần để active bằn nút manual
objects_2 = [] # mảng chứa các elements để active bằng nút Connect
objects_3 = [] # các element combobox về UART parameter

# Bit kết thúc
stop_bit = '\n'

# Các biến dùng truyền UART
b_uart=f_uart=p_uart=para_uart= None

''' Chức năng giao diện '''

# Hàm cho nút connect
def connect_uart():
    # kích hoạt nút Manual, Auto
    for obj in objects_2:
        obj['state'] = 'normal'

    global b_uart,f_uart,p_uart,para_uart

    
    # Các biến parameter cho UART
    selected_port = com_port.get()
    selected_rate = int(rate_port.get())
    selected_stop = stop_port.get()
    select_data = int(data_port.get())
    select_parity = parity_port.get()
        
    # tạo một switch case check coi stop bit chọn bao nhiêu bit
    def switch_case_1(argument):
        if argument == '1':
                output = serial.STOPBITS_ONE
        elif argument == '1.5':
                output = serial.STOPBITS_ONE_POINT_FIVE
        elif argument == '2':
                output = serial.STOPBITS_TWO
        return output
    stop_bit_value = switch_case_1(selected_stop)

    # tạo một switch case để check coi data bit truyền là 7 hay 8 bits
    def switch_case_2(argument):
        if argument == 7:
            output = serial.SEVENBITS
        elif argument == 8:
            output = serial.EIGHTBITS
        return output
    data_bit_value = switch_case_2(select_data)

    #tạo một switch case để check coi parity bit được chọn là even, odd hay none
    def switch_case_3(argument):
        if argument == 'even':
            output = serial.PARITY_EVEN
        elif argument =='odd':
            output = serial.PARITY_ODD
        elif argument =='none':
            output =serial.PARITY_NONE
        return output
    parity_bit_value =switch_case_3(select_parity)

    # Tạo kết nối UART với các biến bánh trước, bánh sau, phanh
    b_uart = f_uart = p_uart= para_uart= serial.Serial(
        port=selected_port,
        baudrate=selected_rate,
        stopbits=stop_bit_value,
        bytesize=data_bit_value,
        parity=parity_bit_value,
        timeout=1  # Timeout cho phép đọc từ giao diện UART
    )

    if b_uart.is_open:
        open_status['bg']='green'
        close_status['bg']='white'

        # tạo popup thông báo kết nối thành công 
        popup = tk.Toplevel()
        popup.title('Success')
        popup.resizable(height=False,width=False)
        
        # Tính toán vị trí của popup
        root_width = root.winfo_width()
        root_height = root.winfo_height()
        popup_width = 320
        popup_height = 120
        x = root.winfo_rootx() + (root_width - popup_width) // 2
        y = root.winfo_rooty() + (root_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        canvas = tk.Canvas(popup, width=100, height=100,bd=0)
        canvas.place(x=1,y=1)

        image = Image.open("D:\PROJECT-MECHATRONIC/GUI/successful.png")
        image = image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        image = Image.open("D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/successful.png")
        image = image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        canvas.create_image(40,60,image=photo)
        canvas.place(x= 1, y= 1)

        label = tk.Label(popup, text="UART connection successfull",font=('Arial',12,'bold'))
        label.place(x = 80, y= 30)

        ok_button = tk.Button(popup, text="OK",font=('Arial',11,'bold'), bg='white',command=popup.destroy)
        ok_button.place(x = 150, y = 70, width= 50, height= 30)

        popup.mainloop()

def show_click():

    #Đọc dữ liệu uart 
    # # đọc UART theo dòng decode dữ liệu là bỏ khoảng trắng và kí tự xuống dòng bên phải dữ liệu
    parameter= para_uart_uart.readline().decode().strip() 
       
    # Xử lý tính hiệu UART
    if para_uart.startswith('A'):
        angle_display['text']=parameter[1:]
    elif para_uart.startswith('V'):
        vel_display['text']=parameter[1:]
    elif para_uart.startswith('D'):
        dis_display['text']=parameter[1:]

# Hàm cho nút Open
def open_click():
    for obj in objects_0:
        obj['state'] = 'normal'
    
# Hàm cho nút Close
def close_click():
    for obj in objects_0+objects_1+objects_2:
        obj['state'] = 'disabled'
    for obj in objects_3:
        obj.set('')
    
    #Ngắt UART
    if b_uart.is_open:
        b_uart.close()
        f_uart.close()
        p_uart.close()
        angle_uart.close()
        velocity_uart.close()

    if not b_uart.is_open:
        open_status['bg']='white'
        close_status['bg']='red'

# Tạo cửa sổ giao diện chính
root = tk.Tk()
root.geometry("1060x500")
root.configure(bg=GUI_color)
root.resizable(height=False, width=False)

'''Tạo các nhãn'''

# Tạo nhãn cho ô chọn cổng COM
com_label = tk.Label(root, text="COM Port:", bg=GUI_color)
com_label.place(x=180, y=5)

# Tạo nhãn cho ô chọn Baudrate
rate_label = tk.Label(root, text='Baud Rate', bg=GUI_color)
rate_label.place(x=300, y=5)

# Tạo nhãn cho Data Bits
data_label = tk.Label(root,text='Data Bit:',bg=GUI_color)
data_label.place(x=180,y=65)

#Tạo nhãn cho Stop Bit
stop_label = tk.Label(root,text='Stop Bit',bg=GUI_color)
stop_label.place(x=300,y=65)

#Tạo nhãn cho Parity bit
parity_label = tk.Label(root,text = 'Parity Bit',bg=GUI_color)
parity_label.place(x=420,y=5)

# Tạo nhãn cho hiển thị Angle
angle_label = tk.Label(root,text='Angle',bg=GUI_color)
angle_label.place(x=700,y= 5)

#Tạo ô hiển thị cho Angle
angle_display = tk.Label(root,relief=tk.SUNKEN,anchor=tk.W,padx=10,bg='white')
angle_display.place(x=700,y=30,height=30,width=100)

# Tạo nhãn cho Velocity
vel_label = tk.Label(root,text='Velocity',bg=GUI_color)
vel_label.place(x= 820,y=5 )

#Tạo ô hiển thị Velocity
vel_display= tk.Label(root,relief=tk.SUNKEN,anchor=tk.W,padx=10,bg='white')
vel_display.place(x=820,y=30,width=100,height=30)

#Tạo nhãn cho Distance
dis_label = tk.Label(root,text='Distance',bg=GUI_color)
dis_label.place(x= 940,y=5)

#Tạo ô hiển thị cho Distance 
dis_display = tk.Label(root,relief=tk.SUNKEN,anchor=tk.W,padx=10,bg='white')
dis_display.place(x=940,y=30,height=30,width=100)

#Tạo nhãn cho status
status_label = tk.Label(root,text='UART status',bg=GUI_color)
status_label.place(x=420,y=65)

# Lấy danh sách tất cả các cổng COM 
com_ports = [port.device for port in serial.tools.list_ports.comports()]

# Lấy danh sách Baud Rate
rate = [
    '1200', '1800', '2400', '4800', '9600', '19200', '28800', '38400',
    '57600', '76800', '115200', '230400', '460800', '576000', '921600']

''' Tạo các combobox cho các thông số liên quan tới UART'''
# Tạo ô chọn cổng COM cho điều khiển
com_port = ttk.Combobox(root, values=com_ports, state='disabled')
com_port.place(x=180, y=30, height=30, width=100)
objects_0.append(com_port)
objects_3.append(com_port)

# Tạo ô chọn Baud Rate
rate_port = ttk.Combobox(root, values=rate, state='disabled')
rate_port.place(x=300, y=30, height=30, width=100)
rate_port.set(rate[10])
objects_0.append(rate_port)
objects_3.append(rate_port)

# Tạo ô chọn Data Bits
data_port  = ttk.Combobox(root,values = ['7','8'],state='disabled')
data_port.place(x=180, y=90, height=30, width=100)
objects_0.append(data_port)
objects_3.append(data_port)

#Tạo ô chọn Stop Bit
stop_port = ttk.Combobox(root,values=['1','1.5','2'],state='disabled')
stop_port.place(x=300,y=90,height=30,width=100)
objects_0.append(stop_port)
objects_3.append(stop_port)

#Tạo ô chọn Parity Bit 
parity_port =ttk.Combobox(root,values=['even','odd','none'],state='disabled')
parity_port.place(x=420,y=30,height=30,width=100)
objects_0.append(parity_port)
objects_3.append(parity_port)

''' Tạo các nút '''
# Tạo nút Open
btn_open = tk.Button(root, text='Open', command=open_click,bg='white')
btn_open.place(x=10, y=30, height=30, width=70)

# Tạo nút Close
btn_close = tk.Button(root, text='Close', state='disabled', command=close_click,bg='white')
btn_close.place(x=90, y=30, height=30, width=70)
objects_0.append(btn_close)

# Tạo nút chọn cổng COM
connect_button = tk.Button(root, text="Connect", state='disabled', command=connect_uart,bg='white')
connect_button.place(x=540, y=30, height=30, width=100)
objects_0.append(connect_button)

# Tạo nút Show value
show_button = tk.Button(root,text = 'Show value',state= 'disabled',bg='white',command=show_click)
show_button.place(x= 540,y=90,height=30,width=100)
objects_2.append(show_button)

# Frame Status Uart
status_frame = tk.Frame(root,height=30,width=100,bg='white')
status_frame.place(x= 420,y=90)

#Trạng thái UART is open
open_status = tk.Label(status_frame)
open_status.place(x=0,y=0,height=30,width=50)

#Trạng thái UART close
close_status =tk.Label(status_frame,bg='red')
close_status.place(x=50,y=0,height=30,width=50)

''' chức năng auto'''
# Tạo nút Auto
btn_auto = tk.Button(root, text='Auto', state='disabled',bg='white')
btn_auto.place(x=10, y=90, height=30, width=70)
objects_2.append(btn_auto)

''' Chức năng manual'''
# Hàm chức năng cho nút Manual
def manual_click():
    for obj in objects_1:
        obj['state'] = 'normal'

# Tạo nút Manual
btn_manu = tk.Button(root, text='Manual', state='disabled',bg='white',command= manual_click)
btn_manu.place(x=90, y=90, height=30, width=70)
objects_2.append(btn_manu)

# Tạo nhãn cho manu frame
manu_fr_label = tk.Label(root,text='Manual Control', bg=GUI_color,font=('Arial',16,'bold'))
manu_fr_label.place(x=10,y=150)

'''Tạo frame cho Manual Control'''
manu_frame = tk.Frame(root,width =530,height=265, highlightbackground='#241468',highlightthickness=2,bg=manu_color )
manu_frame.place(x= 10, y= 190)

# Tạo nhãn cho di chuyển trước và sau
back_wheel_label = tk.Label(manu_frame,text='Back Wheel Control',bg=manu_color,font=('Arial',12,'bold'))
back_wheel_label.place(x=10,y=10)

# Tạo nhãn cho bánh trước
front_wheel_label = tk.Label(manu_frame,text='Front Wheel Control',bg=manu_color,font=('Arial',12,'bold'))
front_wheel_label.place(x=205, y=10)

# Tạo nhãn cho phanh
brake_label = tk.Label(manu_frame, text = 'Brake Control',bg=manu_color,font=('Arial',12,'bold'))
brake_label.place(x= 205, y= 135 )

''' Tạo frame cho bánh sau'''
back_frame = tk.Frame(manu_frame, width=185, height=215, highlightbackground='#645CAA', highlightthickness=2,bg=manu_color)
back_frame.place(x= 10, y= 40)

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
            if b_uart.is_open:
                start_bit = 'B'
                back_for_adc = linear_scale.get()
                direction = "T"
                b_uart.write(bytearray([ord(start_bit),ord(direction),back_for_adc,ord(stop_bit)]))
            else:
                messagebox.showwarning('Warning','Please connect the UART')
        else:
            # Mở ảnh mặc định khi nút được thả ra
            forward_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/1.png')
            # truyền UART cho bánh sau
            if b_uart.is_open:
                start_bit = 'B'
                back_for_adc = 0
                b_uart.write(bytearray([ord(start_bit),back_for_adc,ord(stop_bit)]))
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
            if b_uart.is_open:
                start_bit = 'B'
                back_rev_adc = linear_scale.get()
                direction = "L"
                b_uart.write(bytearray([ord(start_bit),ord(direction),back_rev_adc,ord(stop_bit)]))
            else:
                messagebox.showwarning('Warning','Please connect the UART')
        else:
            # Mở ảnh mặc định khi nút được thả ra
            reverse_btn = PhotoImage(file='D:/STUDYING/Mechatronic Project/PROJECT-MECHATRONIC/GUI/3.png')
            #truyền UART giá trị tốc độ cho bánh sau
            if b_uart.is_open:
                start_bit = 'B'
                back_rev_adc = 0
                b_uart.write(bytearray([ord(start_bit),back_rev_adc,ord(stop_bit)]))
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
front_frame = tk.Frame(manu_frame,height=85, width=315,bg=manu_color,highlightbackground='#645CAA',highlightthickness=2)
front_frame.place(x=205,y=40)

''' Code cho tạo thanh trượt rẽ trái phải'''
#truyền UART bánh trước
def turn_slide(value):
    turn_adc = int(value)
    start_bit = 'F'
    uart_data = bytearray([ord(start_bit),abs(turn_adc),ord(stop_bit)])
    if f_uart.is_open:
        f_uart.write(uart_data)  

# Tạo ô trượt điều khiển trái phải
turn_scale = tk.Scale(front_frame, from_=0, to=200, orient=tk.HORIZONTAL,bg='white',bd=1, 
    tickinterval=25, showvalue=True,troughcolor='white',state='disabled',command=turn_slide)
turn_scale.place(x = 5, y= 5, height= 70, width = 300)
turn_scale.set(100)
objects_1.append(turn_scale)


'''Tạo frame cho phanh'''
brake_frame = tk.Frame(manu_frame,height=90,width=315,bg=manu_color,highlightbackground='#645CAA',highlightthickness=2)
brake_frame.place(x=205,y=165)

''' Code cho nút phanh'''
# Hàm cho nút Brake để đổi hình khi ấn
def brake(event):

    global brake_btn

    if btn_brake['state']!='disabled':
        if event.type == '4':  # ButtonPress event
            # Mở ảnh khi nút được nhấn
            brake_btn = PhotoImage(file='D:/STUDYING\Mechatronic Project/PROJECT-MECHATRONIC/GUI/b_2.png')
            # truyền uart cho adc cho phanh
            if p_uart.is_open:
                start_bit = 'P'
                brake_adc = brake_slide.get()
                p_uart.write(bytearray([ord(start_bit),brake_adc,ord(stop_bit)]))
        else:
            # Mở ảnh mặc định khi nút được thả ra
            brake_btn = PhotoImage(file='D:/STUDYING\Mechatronic Project/PROJECT-MECHATRONIC/GUI/b_1.png')
            # truyền uart cho adc cho phanh
            if p_uart.is_open:
                start_bit = 'P'
                brake_adc = 0
                p_uart.write(bytearray([ord(start_bit),brake_adc,ord(stop_bit)]))

    btn_brake['image']= brake_btn

# Mở ảnh
brake_btn = PhotoImage(file='D:/STUDYING\Mechatronic Project/PROJECT-MECHATRONIC/GUI/b_1.png')

# Tạo nút Brake
btn_brake = Button(brake_frame, image=brake_btn, bg=manu_color, borderwidth=0, state='disabled')
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