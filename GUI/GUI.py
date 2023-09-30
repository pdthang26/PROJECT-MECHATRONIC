import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import serial.tools.list_ports
from PIL import ImageTk, Image
import serial
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Đường dẫn tương đối của file

''' ảnh của nút tiến'''
back_for_release_path = '1.png'
back_for_press_path = '2.png'

''' ảnh của nút lùi'''
back_rev_release_path = '3.png'
back_rev_press_path = '4.png'

'''ảnh của nút phanh'''
brake_release_path = 'b_1.png'
brake_press_path = 'b_2.png'

'''ảnh nút Emergency stop'''
emergency_stop_path = 'emergency stop.png'

'''ảnh tick xanh thông báo UART kết nối thành công'''
successful_path = 'successful.png'

# Xác định đường dẫn tuyệt đối
back_for_release = os.path.abspath(back_for_release_path)
back_for_press = os.path.abspath(back_for_press_path)

back_rev_release = os.path.abspath(back_rev_release_path)
back_rev_press = os.path.abspath(back_rev_press_path)

brake_release = os.path.abspath(brake_release_path)
brake_press = os.path.abspath(brake_press_path)

emergency_stop = os.path.abspath(emergency_stop_path)

successful = os.path.abspath(successful_path)

'''Tạo các biến cần thiết cho chương trình'''

# biến màu giao diện
GUI_color = '#C9F4AA'

# biến màu frame Manual
manu_color = '#F7C8E0'

# Bit bắt đầu cho gửi UART bánh sau
b_start_bit = b'B'

# Bit kết thúc
stop_bit = b'\x0A'

# Tạo cửa sổ giao diện chính
root = tk.Tk()
root.geometry("1340x770")
root.configure(bg=GUI_color)
root.resizable(height=False, width=False)

# Tạo mảng bao gồm các thành phần trên giao diện
objects_1 = [] # mảng chứa các thành phần để active bằng nút manual
objects_2 = [] # mảng chứa các elements để active bằng nút Connect
objects_3 = [] # các element combobox về UART parameter

# Các biến dùng truyền UART
emer_uart= b_uart= f_uart= p_uart= ang_uart= vel_uart= dis_uart = None
gps_port = None

''' Chức năng giao diện '''

# Hàm cho nút connect
def connect_uart():

    #Kích hoạt nút Disconnect
    disconnect_button['state']='normal'

    # kích hoạt nút Manual, Auto, Show Car Value
    for obj in objects_2:
        obj['state'] = 'normal'

    global b_uart,f_uart,p_uart
    global ang_uart,vel_uart,dis_uart
    global emer_uart
    global gps_uart

    # Các biến parameter cho UART
    selected_port = com_port.get()
    selected_gps = gps_port.get()
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

    # Kiểm tra nếu cổng UART không được cung cấp
    if (selected_port == '')or(selected_gps ==''):
        messagebox.showwarning('Warning', 'The COM/GPS port is empty.\nPlease select a COM/GPS port.')
    else:
        try:
            # Khởi tạo đối tượng Serial
            emer_uart= ang_uart= vel_uart= dis_uart= b_uart= f_uart= p_uart =serial.Serial(
            port=selected_port,
            baudrate=selected_rate,
            stopbits=stop_bit_value,
            bytesize=data_bit_value,
            parity=parity_bit_value,
            timeout=1  # Timeout cho phép đọc từ giao diện UART
        )
             #khởi tạo đối tượng Serial
            gps_uart = serial.Serial(
                port=selected_gps,
                baudrate=9600,
                stopbits= stop_bit_value,
                bytesize= data_bit_value,
                parity= parity_bit_value,
                timeout=1
        )

            # Hiển thị thông báo kết nối UART thành công 
            if b_uart.is_open:

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

                image = Image.open(successful)
                image = image.resize((50, 50), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)

                canvas.create_image(40,60,image=photo)
                canvas.place(x= 1, y= 1)

                label = tk.Label(popup, text="UART connection successfull",font=('Arial',12,'bold'))
                label.place(x = 80, y= 30)

                ok_button = tk.Button(popup, text="OK",font=('Arial',11,'bold'), bg='white',command=popup.destroy)
                ok_button.place(x = 150, y = 70, width= 50, height= 30)

                popup.mainloop()

        except serial.SerialException as e:
            # Xử lý lỗi mở cổng UART
            messagebox.showerror('Error', f'Failed to open COM port: {str(e)}')

# Khởi tạo biến cờ và đặt giá trị ban đầu là False
update_flag = False

angle_p = 0

velocity_p = 0

distance_p= 0

def show():
    global angle_p, velocity_p, distance_p #, longitude, lattitude

    # Đọc dữ liệu UART về góc
    angle = ang_uart.readline().decode().strip()

    # Đọc dữ liệu UART về tốc độ
    velocity = vel_uart.readline().decode().strip()

    # Đọc dữ liệu UART về quãng đường
    distance = dis_uart.read().strip()

    # Đọc dữ liệu UART về GPS
    gps = gps_uart.readline().decode().strip()

    # Xử lý tín hiệu UART cho GPS
    if gps.startswith('$GPRMC'):
        data = gps.split(',')
        if data[2] == 'A':
            latitude = data[3]
            longitude = data[5]
            # Cập nhật giá trị lên các ô label
            longitude_display['text'] =  longitude
            latitude_display['text'] =  latitude

    # Xử lý tín hiệu UART cho góc
    if angle.startswith('Y'):
        angle_n = float(angle[1:])
        if angle_p != angle_n:
            angle_display['text'] =  angle[1:]
            angle_p = angle_n

    # Xử lý tín hiệu UART cho tốc độ
    if velocity.startswith('V'):
        velocity_n = float(velocity[1:])
        if velocity_p != velocity_n:
            vel_display['text'] = velocity[1:]
            velocity_p = velocity_

    # Xử lý tín hiệu UART cho quãng đường
    if distance.startswith(b'D'):
        distance_n = float(distance[1:])
        if distance_p != distance_n:
            dis_display['text'] =  distance[1:]
            distance_p = distance_n

    # Kiểm tra biến cờ để quyết định liệu có tiếp tục cập nhật hay không
    if update_flag:
        root.after(200, show)

# Hàm nhấn nút show value
def show_click():
    global update_flag
    if not update_flag:
        update_flag = True
        show()

#Hàm cho nút Disconnect
def disconnect_uart():
    
    global update_flag

    update_flag = False

    for obj in objects_1+objects_2:
        obj['state'] = 'disabled'

    com_port['text']=''
    gps_port['text']=''

    #Ngắt UART
    if b_uart.is_open:
        b_uart.close()
        f_uart.close()
        p_uart.close()
        ang_uart.close()
        vel_uart.close()
        dis_uart.close()

    if not b_uart.is_open:
        messagebox.showerror('Warning','UART is disconnected !')


# Hàm cho nút Open
def open_click():
    #Kích hoạt nút Connect 
    connect_button['state']='normal'
    #Kích hoạt các Combobox 
    for obj in objects_3:
        obj['state']='normal'
    
# Hàm cho nút Close
def close_click():
    
    # Hiện ô thông báo lữa chọn muốn đóng cửa sổ giao diện
    result = messagebox.askyesno("Exit", "Do you want to exit?")
    if result:
        root.destroy()

'''Tạo các nhãn'''

# Tạo nhãn cho ô chọn cổng COM
com_label = tk.Label(root, text="COM Port:", bg=GUI_color)
com_label.place(x=180, y=5)

# Tạo nhãn cho ô chọn GPS COM
gps_label = tk.Label(root, text ='GPS Port', bg=GUI_color)
gps_label.place(x=300,y=5)

# Tạo nhãn cho ô chọn Baudrate
rate_label = tk.Label(root, text='Baud Rate', bg=GUI_color)
rate_label.place(x=420, y=5)

# Tạo nhãn cho Data Bits
data_label = tk.Label(root,text='Data Bit:',bg=GUI_color)
data_label.place(x=180,y=65)

#Tạo nhãn cho Stop Bit
stop_label = tk.Label(root,text='Stop Bit',bg=GUI_color)
stop_label.place(x=300,y=65)

#Tạo nhãn cho Parity bit
parity_label = tk.Label(root,text = 'Parity Bit',bg=GUI_color)
parity_label.place(x=420,y=65)

# Tạo nhãn cho hiển thị Angle
angle_label = tk.Label(root,text='Angle',bg=GUI_color)
angle_label.place(x=640,y= 5)

#Tạo ô hiển thị cho Angle
angle_display = tk.Label(root,relief=tk.SUNKEN,anchor=tk.W,padx=10,bg='white',font=('Arial',13,'bold'))
angle_display.place(x=640,y=30,height=30,width=100)

# Tạo nhãn hiển thị đơn vị góc quay
ang_unit = tk.Label(root,text = '\u00B0',bg=GUI_color,font=('Arial',15,'bold'))
ang_unit.place(x=740,y=30)

#Tạo nhãn cho Distance
dis_label = tk.Label(root,text='Distance',bg=GUI_color)
dis_label.place(x= 770,y=5)

#Tạo ô hiển thị cho Distance 
dis_display = tk.Label(root,relief=tk.SUNKEN,anchor=tk.W,padx=10,bg='white')
dis_display.place(x=770,y=30,height=30,width=100)

#Tạo nhãn hiển thị đơn vị cho Distance
dis_unit =tk.Label(root,text='m',bg=GUI_color,font=('Arial',13))
dis_unit.place(x=870,y=30)

# Tạo nhãn cho Speed
vel_label = tk.Label(root,text='Speed',bg=GUI_color)
vel_label.place(x=900,y=5 )

#Tạo ô hiển thị Speed
vel_display= tk.Label(root,relief=tk.SUNKEN,anchor=tk.W,padx=10,bg='white',font=('Arial',13,'bold'))
vel_display.place(x=900,y=30,width=100,height=30)

# Tạo nhãn đơn vị cho tốc độ
speed_unit = tk.Label(root,text='m/s',bg=GUI_color,font=('Arial',13))
speed_unit.place(x=1000,y=30)

# Tạo nhãn cho Longitude
longitude_label= tk.Label(root,text='Longitude',bg = GUI_color)
longitude_label.place(x=1050,y=5)

# Tạo ô hiển thị Longitude
longitude_display = tk.Label(root,relief=tk.SUNKEN,padx=5,bg='white')
longitude_display.place(x=1050,y=30,height=30,width=280)

# Tạo nhãn hiển thị Latitude
latitude_label = tk.Label(root,text='Latitude',bg=GUI_color)
latitude_label.place(x=1050,y=65)

# Tạo ô hiển thị Latitude
latitude_display = tk.Label(root,relief=tk.SUNKEN,bg='white')
latitude_display.place(x=1050,y=90,height=30,width=280)

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
objects_3.append(com_port)

# Tạo ô chọn cổng COM cho GPS
gps_port = ttk.Combobox(root,values = com_ports,state='disabled')
gps_port.place(x=300,y=30,height=30,width=100)
objects_3.append(gps_port)

# Tạo ô chọn Baud Rate
rate_port = ttk.Combobox(root, values=rate, state='disabled')
rate_port.place(x=420, y=30, height=30, width=100)
rate_port.set(rate[10])
objects_3.append(rate_port)

# Tạo ô chọn Data Bits
data_port  = ttk.Combobox(root,values = ['7','8'],state='disabled')
data_port.set('8')
data_port.place(x=180, y=90, height=30, width=100)
objects_3.append(data_port)

#Tạo ô chọn Stop Bit
stop_port = ttk.Combobox(root,values=['1','1.5','2'],state='disabled')
stop_port.set('1')
stop_port.place(x=300,y=90,height=30,width=100)
objects_3.append(stop_port)

#Tạo ô chọn Parity Bit 
parity_port =ttk.Combobox(root,values=['even','odd','none'],state='disabled')
parity_port.set('none')
parity_port.place(x=420,y=90,height=30,width=100)
objects_3.append(parity_port)

''' Tạo các nút '''
# Tạo nút Open
btn_open = tk.Button(root, text='Open', command=open_click,bg='white')
btn_open.place(x=10, y=30, height=30, width=70)

# Tạo nút Close cửa sổ chương trình
btn_close = tk.Button(root, text='Close', command=close_click,bg='white')
btn_close.place(x=90, y=30, height=30, width=70)

# Tạo nút kết nối UART
connect_button = tk.Button(root, text="Connect", state='disabled', command=connect_uart,bg='white')
connect_button.place(x=540, y=30, height=30, width=80)

# Tạo nút ngắt UART 
disconnect_button = tk.Button(root,text='Disconnect',state ='disabled',bg='white',command=disconnect_uart)
disconnect_button.place(x=540,y=90,height=30,width=80)

# Tạo nút Show value
show_button = tk.Button(root,text = 'Show Value',state= 'disabled',bg='white',command=show_click)
show_button.place(x= 680,y=90,height=30,width=80)
objects_2.append(show_button)

''' chức năng auto'''
# Tạo nút Auto
btn_auto = tk.Button(root, text='Auto', state='disabled',bg='white')
btn_auto.place(x=10, y=90, height=30, width=70)
objects_2.append(btn_auto)

# Tạo nhãn cho Auto 
auto_fr_label = tk.Label(root,text = 'Auto Control',bg = GUI_color, font=('Arial',16,'bold'))
auto_fr_label.place(x= 10, y = 455)

# Tạo nhãn cho Auto Frame
auto_frame = tk.Frame(root,height=265,width=530,highlightthickness=2,highlightbackground='#241468',bg=manu_color)
auto_frame.place(x=10,y=495)

# Tạo nhãn ô nhập đi thẳng
linear_motion_label = tk.Label(auto_frame,text ='Vertical Movement',bg=manu_color)
linear_motion_label.place(x= 10, y=10)

#Tạo Entry nhập số m muốn xe đi chuyển
linear_entry = tk.Entry(auto_frame,relief=tk.SUNKEN,justify='center')
linear_entry.place(x=10,y=40,height=30,width=150)

# biến cờ 
flag = 0
desired_pos = 0
distance = 0

def go_click():
    
    global flag, desired_pos, distance
      
    # Cập nhật giá trị distance từ dữ liệu đọc từ UART
    data = dis_uart.readline().decode().strip()
    if data.startswith('D'):
        distance = float(data[1:])

    deriserd_pos = float(linear_entry.get())

    if desired_pos<0:
        direction = b'L'
    else:
        direction = b'T'

    while (distance <= desired_pos):
        flag = 1
    flag = 0
    
    flag_transmit = str(flag)
    uart_data = b_start_bit + direction + flag_transmit.encode('utf-8') + stop_bit
    b_uart.write(uart_data)
        
# Tạo nút Go
go_btn = tk.Button(auto_frame,text = 'Go',bg='white',command=go_click)
go_btn.place(x=170, y= 40,height=30,width=50)

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
manu_fr_label.place(x=10,y=130)

'''Tạo frame cho Manual Control'''
manu_frame = tk.Frame(root,width =530,height=265, highlightbackground='#241468',highlightthickness=2,bg=manu_color )
manu_frame.place(x= 10, y= 170)

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

# Gía trị hàng đơn vị khi không nhấn nút
back_adc_unit = b'0'

# Gía trị hàng chục khi không nhấn nút 
back_adc_dozen = b'0'

# Gía trị hàng trăm khi không nhấn nút
back_adc_hundred = b'0'

# Hợp 3 số lại 
back_adc = back_adc_hundred + back_adc_dozen + back_adc_unit

'''Code cho nút forward'''

# Hàm cho nút forward để đổi hình khi ấn
def forward(event):

    global forward_btn
    if btn_forward['state'] != 'disabled':
        if event.type == '4':  # ButtonPress event
            # Mở ảnh khi nút được nhấn
            forward_btn = PhotoImage(file=back_for_press)
            #truyền UART cho bánh sau
            if b_uart.is_open:
                back_for_adc = str(int(linear_scale.get()))
                direction = b'T'
                uart_data = b_start_bit + direction + back_for_adc.encode('utf-8') + stop_bit
                b_uart.write(uart_data)
            else:
                messagebox.showwarning('Warning','Please connect the UART')
        else:
            # Mở ảnh mặc định khi nút được thả ra
            forward_btn = PhotoImage(file=back_for_release)
            # truyền UART cho bánh sau
            if b_uart.is_open:
                
                uart_data = b_start_bit + back_adc + stop_bit
                b_uart.write(uart_data)
            else:
                messagebox.showwarning('Warning','Please connect the UART')

    btn_forward['image'] = forward_btn

# Mở ảnh 
forward_btn = PhotoImage(file=back_for_release)

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

    global reverse_btn

    if btn_reverse['state']!='disabled': # check trạng thái của nút
        if event.type == '4':  # ButtonPress event
            # Mở ảnh khi nút được nhấn
            reverse_btn = PhotoImage(file=back_rev_press)
            #truyền UART giá trị tốc độ cho bánh sau
            if b_uart.is_open:
                back_rev_adc = str(int(linear_scale.get())) #gán thành chuỗi kí tự
                direction = b'L'
                uart_data = b_start_bit + direction + back_rev_adc.encode('utf-8') + stop_bit
                b_uart.write(uart_data)

            else:
                messagebox.showwarning('Warning','Please connect the UART')
        else:
            # Mở ảnh mặc định khi nút được thả ra
            reverse_btn = PhotoImage(file=back_rev_release)
            #truyền UART giá trị tốc độ cho bánh sau
            if b_uart.is_open:
                uart_data = b_start_bit + back_adc  + stop_bit
                b_uart.write(uart_data)
            else:
                messagebox.showwarning('Warning','Please connect the UART')

    btn_reverse['image']= reverse_btn

# Mở ảnh
reverse_btn = PhotoImage(file=back_rev_release)

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

# Start bit for UART transmission on the front wheel
f_start_bit = b'F'

''' Code cho tạo thanh trượt rẽ trái phải'''
#truyền UART bánh trước
def turn_slide(value):
    
    turn_adc = str(int(value))
    uart_data = f_start_bit + turn_adc.encode('utf-8') + stop_bit    
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

# Start bit for UART transmission on brake
p_start_bit = b'P'

# Gía trị hàng đơn vị khi không nhấn nút 
brake_adc_unit = b'0'

#Gía trị hàng chục khi không nhấn nút 
brake_adc_dozen = b'0'

#Gía trị hàng trăm khi không nhấn nút 
brake_adc_hundred = b'0'

#Hợp giá trị 3 số 
brake_adc_1 = brake_adc_hundred + brake_adc_dozen + brake_adc_unit

''' Code cho nút phanh'''
# Hàm cho nút Brake để đổi hình khi ấn
def brake(event):

    global brake_btn

    if btn_brake['state']!='disabled':
        if event.type == '4':  # ButtonPress event
            # Mở ảnh khi nút được nhấn
            brake_btn = PhotoImage(file=brake_press)
            # truyền uart cho adc cho phanh
            if p_uart.is_open:
                brake_adc_0 = str(int(brake_slide.get()))
                uart_data = p_start_bit + brake_adc_0.encode('utf-8') + stop_bit
                p_uart.write(uart_data)
        else:
            # Mở ảnh mặc định khi nút được thả ra
            brake_btn = PhotoImage(file=brake_release)
            # truyền uart cho adc cho phanh
            if p_uart.is_open:
                uart_data = p_start_bit + brake_adc_1 + stop_bit
                p_uart.write(uart_data)
                
    btn_brake['image']= brake_btn

# Mở ảnh
brake_btn = PhotoImage(file=brake_release)

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

''' Code for Emergency Stop button in Manual Control '''

lines = []

# Hàm khi ấn nút Emergency Button 
def ma_em_click():

    brake_adc_emer = b'100'
    brake_emer = p_start_bit + brake_adc_emer + stop_bit
    lines.append(brake_emer)

    back_emer = b_start_bit + back_adc + stop_bit
    lines.append(back_emer)

    for line in lines:
        emer_uart.write(line)

# Mở ảnh
manu_emer = PhotoImage(file = emergency_stop)

# Emergency Stop button for manual mode creation
manu_emer_button = tk.Button(auto_frame,image = manu_emer, bg= manu_color, borderwidth=0, state='disabled',command = ma_em_click )
manu_emer_button.place(x=420, y=10, width=100, height=100)
objects_1.append(manu_emer_button)

# Khởi tạo đồ thị
fig = Figure()

ax1 = fig.add_subplot(2, 1, 1)
ax1.set_title('Car Trajectory')
ax1.set_xlabel('Time')
ax1.set_ylabel('Angle')
ax1.grid(True)
ax1.set_xlim(0, 100)
ax1.set_ylim(-190, 190)       
line1, = ax1.plot([], [], 'g')


ax2 = fig.add_subplot(2,1,2)
ax2.set_title('Car Position')
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Lattitude')
ax2.grid(True)
line2, = ax2.plot([], [], 'r')


# Khởi tạo canvas để hiển thị đồ thị
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=560, y=170, height=590, width=770)

# Điều chỉnh vị trí của đồ thị
fig.tight_layout()

# Mảng lưu các giá trị angles
angles = []

# Biến cờ cho đồ thị
run = False

# Hàm cập nhật dữ liệu nối tiếp và vẽ đồ thị
def update_plot():
    global run

    if run==True:
        # Đọc dữ liệu từ vi điều khiển qua UART
        data = ang_uart.readline().decode().strip()
        if data.startswith('Y'):
            angle = float(data[1:])
        
        # Kiểm tra nếu danh sách angles có quá nhiều giá trị, chỉ giữ lại 100 giá trị gần nhất
            if len(angles) < 100:
                # Thêm giá trị mới vào danh sách
                angles.append(angle)
            else:
                angles.pop(0)  # Xóa phần tử đầu tiên
                angles.append(angle)  # Thêm giá trị mới vào cuối danh sách
        
        # Xóa dữ liệu cũ trên đồ thị
        ax1.clear()
        
        # Vẽ đồ thị
        ax1.plot(range(len(angles)), angles, 'g')
        ax1.set_title('Car Trajectory')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Angle')
        ax1.grid(True)
        ax1.set_xlim(0, 100)
        ax1.set_ylim(-190, 190)
        
        # Cập nhật đồ thị
        canvas.draw()
    
    # Gọi lại hàm update_plot mỗi 100ms
    root.after(100, update_plot)

# Hàm cho nút Start
def start_click():
    global run
    run = True

# Nút start vẽ đồ thị 
start_btn = tk.Button(root, text = 'Start',bg='white',command = start_click,state='disabled')
start_btn.place(x=770,y = 90,height=30,width=80)
objects_2.append(start_btn)

def stop_click():
    global run
    run = False

# Nút Stop vẽ đồ thị
stop_btn = tk.Button(root,text ='Stop',bg='white',command=stop_click,state='disabled')
stop_btn.place(x =855,y=90,height=30,width=80 )
objects_2.append(stop_btn)

# Gọi hàm update_plot để bắt đầu cập nhật và vẽ đồ thị
update_plot()

# Chạy vòng lặp giao diện
root.mainloop()