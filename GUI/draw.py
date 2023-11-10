import tkinter as tk
import numpy as np
arr_point = []


root = tk.Tk()
root.title("Paint App")

canvas = tk.Canvas(root, bg="white", width=400, height=400)
canvas.pack()

pen_color = "black"
pen_width = 2
is_drawing = False
prev_x = None
prev_y = None

def start_paint(event):
    global is_drawing, prev_x, prev_y
    is_drawing = True
    prev_x = event.x
    prev_y = event.y



def paint(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        x, y = event.x, event.y
        if prev_x and prev_y:
            canvas.create_line(prev_x, prev_y, x, y, fill=pen_color, width=pen_width)
            arr_point.append((x,y))
        prev_x = x
        prev_y = y
    
    
    
    

def stop_paint(event):
    global is_drawing, prev_x, prev_y
    is_drawing = False
    prev_x = None
    prev_y = None




canvas.bind("<Button-1>", start_paint)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", stop_paint)

root.mainloop()


print(arr_point)


