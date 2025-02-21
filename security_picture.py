import cv2

def security_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
    else:
        while True:
            ret, frame = cap.read()
            cv2.imwrite("security_picture.jpg", frame)
            print("Image saved.")
            break
        cap.release()
        cv2.destroyAllWindows()