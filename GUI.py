import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

# Tạo mảng bao gồm các thành phần trên giao diện
objects = []

# Chức năng giao diện
def select_com_port():
    selected_port = com_port.get()
    print("Selected COM Port:", selected_port)

def open_click():
   for obj in objects:
        obj['state'] = 'normal'

def close_click():
    for obj in objects:
        obj['state'] = 'disable'

# Tạo cửa sổ giao diện
root = tk.Tk()
root.geometry("1100x500")
root.configure(bg='white')
root.resizable(height='False',width='False')

# Tạo nhãn cho ô chọn cổng COM
com_label = tk.Label(root, text="COM Port:",bg='white')
com_label.place(x = 180,y= 5)

# Tạo nhãn cho ô chọn Baudrate
rate_label = tk.Label(root,text='Baud Rate',bg='white')
rate_label.place(x= 300,y = 5 )

# Tạo nhãn cho Longitude
long_label = tk.Label(root,text = 'Longitude',bg='white')
long_label.place(x = 800, y=5)

# Tạo ô hiển thị cho Longitude
long_display = tk.Label(root,relief=tk.SUNKEN)
long_display.place(x= 800,y=30,height = 30, width = 250)
objects.append(long_display)

# Tạo nhãn cho Lattitude
lat_label = tk.Label(root,text ='Lattitude',bg = 'white')
lat_label.place(x= 800, y= 65 )

# Tạo ô hiển thị cho Lattitude
lat_display = tk.Label(root,relief=tk.SUNKEN)
lat_display.place(x= 800,y=90,height = 30, width = 250)
objects.append(lat_display)

# Lấy danh sách các cổng COM
com_ports = [port.device for port in serial.tools.list_ports.comports()]
# Lấy danh sách Baud Rate
rate = ['1200',
        '1800',
        '2400',
        '4800',
        '9600',
        '19200',
        '28800',
        '38400',
        '57600',
        '76800',
        '115200',
        '230400',
        '460800',
        '576000',
        '921600']

# Tạo ô chọn cổng COM
com_port = ttk.Combobox(root, values=com_ports,state='disable')
com_port.place(x=180,y=30,height=30,width=100)
objects.append(com_port)

# Tạo ô chọn Baud Rate
rate_port = ttk.Combobox(root,values=rate,state='disable')
rate_port.place(x=300,y=30,height=30,width=100)
rate_port.set(rate[4])
objects.append(rate_port)

# Tạo nút Open
btn_open = tk.Button(root, text='Open',command = open_click)
btn_open.place(x=10,y=30,height=30,width=70)

#Tạo nút Close
btn_close = tk.Button(root,text='Close',state='disable',command = close_click)
btn_close.place(x = 90,y=30,height=30,width=70)
objects.append(btn_close)

# Tạo nút chọn cổng COM
select_button = tk.Button(root, text="Select",state= 'disable', command=select_com_port)
select_button.place(x= 415,y=30,height=30,width=50 )
objects.append(select_button)

# Tạo nút Auto
btn_auto = tk.Button(root,text='Auto',state='disable')
btn_auto.place(x=10,y=80,height=30,width=70)
objects.append(btn_auto)

# Tạo nút Manual
btn_manu = tk.Button(root,text ='Manual',state='disable')
btn_manu.place(x=90,y= 80,height=30,width=70)
objects.append(btn_manu)

# Chạy vòng lặp giao diện
root.mainloop()