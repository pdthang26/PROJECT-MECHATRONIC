import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    cv2.imshow("frame", frame)

    key = cv2.waitKey(30)
    if cv2.waitKey(30) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()


