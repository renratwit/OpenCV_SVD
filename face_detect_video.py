import cv2
import math

# Load the cascade
face_cascade = cv2.CascadeClassifier('HS.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)

# KNOWN WIDTH OF BOX = ~16in


def distance_from_camera(known_width, focal_length, per_width):
    return (float(known_width) * float(focal_length)) / float(per_width)


KNOWN_WIDTH = 16.0
KNOWN_DISTANCE = 25.0

F = (350 * 29) / 16
font = cv2.FONT_HERSHEY_SIMPLEX


def get_distance_from_faces(frame, faces):
    for (x, y, w, h) in faces:
        for (x2, y2, w2, h2) in faces:
            # draw lines
            if (x == x2 and y == y2):
                continue
            pixel_distance = math.sqrt(math.sqrt(((x2-x)**2)+((y2-y)**2)))
            # print(pixel_distance)
            # cv2.putText(frame,
            #             str(pixel_distance),
            #             (x, y),
            #             font, 1,
            #             (0, 255, 255),
            #             2,
            #             cv2.LINE_4)
    return 0


while True:
    # Read the frame
    _, img = cap.read()
    img = cv2.imread('Group_Photo.jpg')
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    get_distance_from_faces(img, faces)

    # Draw the rectangle around each face AND do other things :)
    for (x, y, w, h) in faces:
        x_end = x + w
        y_end = y + h

        x_mid = math.floor((x + x_end) / 2)
        y_mid = math.floor((y + y_end) / 2)
        est_dist = round((16 * F) / w, 2)
        x_mid_inches = (x_mid * est_dist) / F
        y_mid_inches = (y_mid * est_dist) / F

        for (x2, y2, w2, h2) in faces:
            if (x == x2 and y == y2):
                continue
            x2_end = x2+w2
            y2_end = y2+h2
            x2_mid = math.floor((x2 + x2_end) / 2)
            y2_mid = math.floor((y2 + y2_end) / 2)
            est_dist2 = round((16 * F) / w, 2)
            x2_mid_inches = (x2_mid * est_dist) / F
            y2_mid_inches = (y2_mid * est_dist) / F
            face_distance = math.sqrt((x2_mid_inches - x_mid_inches)**2 + (
                y2_mid_inches - y_mid_inches)**2 + (est_dist2 - est_dist)**2)
            print("FACE DISTANCE", face_distance)
            cv2.line(img, (x2_mid, y2_mid), (x_mid, y_mid), (255, 0, 0), 2)

        cv2.rectangle(img, (x, y), (x+w, y+h), (100, 100, 0), 2)

        cv2.putText(img,
                    str(est_dist),
                    (x, y),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)

    # Display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(1)
        cv2.imwrite(img_name, img)
        print("{} written!".format(img_name))

# Release the VideoCapture object
cap.release()
