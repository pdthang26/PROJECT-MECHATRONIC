# # 
# import time

# a=(0,0)
# x=[a] 
# print(x)
# time.sleep(2)
# x = [a,(1,1),(2,2),(3,3),(4,4),(5,5)]
# print(x)
# time.sleep(2)
# a=x[len(x)-1]
# x=[a]
# print(a)
# print(x)

# a = 30
# a_p = 30
# b = 40
# c = 0
# while a<=b:
#     if a >= a_p and a <= a_p + 2:
#         c = 10
#     elif a > a_p+2 and a<b:
#         c = 20
#     else:
#         c = 0
#         a_p = a

#     print("a =", a, "c =", c)
#     a += 1
#     time.sleep(1)
# print(a_p)

# import math

# def move_car(points, angles):
#     current_poin = (0, 0)  # Điểm ban đầu
#     total_distance = 0

#     for i in range(len(points)):
#         next_point = points[i]
#         angle = angles[i]

#         distance = math.sqrt((next_point[0] - current_point[0]) ** 2 + (next_point[1] - current_point[1]) ** 2)
#         total_distance += distance

#         print(f"Di chuyển từ {current_point} đến {next_point}, quay {angle} độ, quãng đường: {distance}m")

#         current_point = next_point

#         if i < len(points) - 1:
#             print(f"Xe quay {angle} độ")

#     print(f"Tổng chiều dài đường đi: {total_distance}m")

# # Các điểm và góc tương ứng
# distance = [5, 5, 5]
# angles = [0, 90, -90]

# move_car(points, angles)

a = [5,6,5]
b= [0,90,-90]


d= 0 # actual_p
e = 11# actual

f = 0 # desired_p
g = 16 # desired
h= g+f #total_length

speed = 0 # speed

angle = 0 
act_ang = 0
act_ang_p =0

'''điều xung theo góc cho bánh trước'''
MAX_left_pulse = 20000 # bánh đánh hết sang bên trái
STRAIGHT_pulse = 10000 # bánh đánh thẳng
MIN_right_pulse = 0 # bánh đánh hết sang phải
Max_steering = 38 # góc quay tối đa qua một bên

def adjust_front_pulse(desired,actual):

    # điều xung cho quay bên trái
    if desired - actual > 45:
        pulse = MAX_left_pulse
    elif (desired - actual)>=0 and (desired - actual)<= 45:
        pulse = STRAIGHT_pulse

    # điều xung cho quay bên phải
    if desired - actual <-45:
        pulse = MIN_right_pulse
    elif (desired - actual)>=-45 and (desired - actual)<=0:
        pulse = STRAIGHT_pulse
  
    return pulse
'''----oooo----'''


if e<g:
    c= 0 # displacement
    for i in range(len(a)):
        for j in range(len(b)):   
            c += a[i]
            if e >= d and e<d+a[0]:
                if e==d:
                    act_ang_p = act_ang
                angle = b[0]
            elif e>=d+c:
                if j+1<len(b):
                    if e == d+c:
                        act_ang_p = act_ang
                    angle = b[j+1]

    desired = act_ang_p + angle
    print ("góc quay mỗi điểm:",angle)
    print ('góc của xe tại các điểm:',act_ang_p)
    print ('góc mong muốn:',desired)

    if e>=d and e<=d+2:
        speed = 75
    if e> d+2 and e<=h-1:
        if act_ang-desired>=-1 and act_ang-desired<=1:
            speed = 30
        else:
            speed = 50
    print('tốc độ:',speed)
    print('tổng trước:',f)
    print('thực tế trước:',d)
else:
    speed = 0
    f = h
    d = e
    print('tốc độ:',speed)
    print('tổng trước:',f)
    print('thực tế trước:',d)

pwm = adjust_front_pulse(desired,act_ang)
print('xung bánh trước:',pwm)