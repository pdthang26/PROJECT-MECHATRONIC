    if angle <=-38:
        flag = 1
    elif angle >=38:
        flag = 0
    if flag == 1:
        angle +=1
    elif flag ==0:
        angle -=1
    # Thoát khỏi vòng lặp nếu nhấn phím 'q'