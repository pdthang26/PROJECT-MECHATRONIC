import numpy as np 
import cv2
from math import *


camera = cv2.VideoCapture(0)
ret, frame = camera.read()
height, width, _ = frame.shape

pts1 = np.float32([[0,0],[width,0],[0,height],[width,height]])
pts2 = np.float32([[0,0],[1080,0],[350,720],[730,720]])

M_forward = cv2.getPerspectiveTransform(pts1,pts2)
M_inverse = cv2.getPerspectiveTransform(pts2,pts1)


def calulation_turning_point(start_point,distance_turn, angle_turn):
    pixel_per_miles = 180
    x = start_point[0]
    y = start_point[1]
    x_turn = sin(radians(angle_turn)) * distance_turn 
    y_turn = cos(radians(angle_turn)) * distance_turn 
    turning_point = [int (x-x_turn*pixel_per_miles), int(y- y_turn*pixel_per_miles)]
    
    return turning_point



def draw_grid(image, grid_size, color=(110, 0, 0), thickness=1):
    height, width = image.shape[:2]
    cell_width = width // grid_size[1]
    cell_height = height // grid_size[0]

    # Vẽ đường dọc
    for i in range(1, grid_size[1]):
        x = i * cell_width
        cv2.line(image, (x, 0), (x, height), color, thickness)

    # Vẽ đường ngang
    for i in range(1, grid_size[0]):
        y = i * cell_height
        cv2.line(image, (0, y), (width, y), color, thickness)


def draw_trajectory (frame, array_movement, array_angle, actual_distance, actual_dis_p, actual_angle):
    step = 0
    array_turning_point =[[540,720]]
    for i in range(len(array_movement)):
        if actual_distance< actual_dis_p + array_movement[i]:
            step = i
            break
    start_point_left = [540,720]

    for count in range(step,len(array_movement)) :
        next_turning_point = calulation_turning_point(start_point_left, array_movement[count] - actual_distance, array_angle[count]-actual_angle )
        cv2.line(frame,start_point_left,next_turning_point,(0, 0, 255), 2 )
        start_point_left = next_turning_point
        array_turning_point.append(next_turning_point)

    return array_turning_point


def Perspective_point(matrix,arr_point):
    arr_new_point = []
    for i in range(len(arr_point)):
        original_x = arr_point[i][0]
        original_y = arr_point[i][1]
        transformed_coords = np.dot(matrix, np.array([original_x, original_y, 1]))

        # Chia tọa độ x và y cho tọa độ z để chuẩn hóa
        transformed_x = transformed_coords[0] / transformed_coords[2]
        transformed_y = transformed_coords[1] / transformed_coords[2]

        new_point = [transformed_x,transformed_y]
        arr_new_point.append(new_point)
    return arr_new_point



    
def detect (frame_of_interest, object_detector):
    
    obstructing_objects = []
    
    mask = object_detector.apply(frame_of_interest)
    _, mask = cv2.threshold(mask, 230, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 5000:
            # cv2.drawContours(frame_of_interest, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            obstructing_objects.append([x, y, w, h])
            cv2.rectangle(frame_of_interest, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imshow('mask',mask)
    
    return obstructing_objects


    
    

object_detector = cv2.createBackgroundSubtractorMOG2(history = 30, varThreshold = 40)

array_movement = [14.142135623730951, 21.35323817465893, 31.35323817465893]
array_angle = [-45.00000000000001, 56.30993247402021, -7.105427357601002e-15]
actual_distance = 13
actual_dis_p = 0
actual_angle = -45
print(height, width)

while(camera.isOpened()):

    ret, frame = camera.read()
    if ret==True:
        detect (frame, object_detector)
        # Adjust your 4 points
        dst = cv2.warpPerspective(frame,M_forward,(1080,720))
        
        
        draw_trajectory (dst,array_movement , array_angle, actual_distance, actual_dis_p, actual_angle)
        frame = cv2.warpPerspective(dst,M_inverse,(width,height))
        

        # grid_size = (72, 108)  # Kích thước của đường lưới (số hàng, số cột)
        
        # draw_grid(dst, grid_size)
        cv2.namedWindow("Input", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Input", 1080, 720)
        cv2.imshow('Input',frame)
        cv2.imshow('Output',dst)
            
            # Exit by pressing 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
                
        # Breaking when video is finished
    else:
        break

cv2.destroyAllWindows()
camera.release()

