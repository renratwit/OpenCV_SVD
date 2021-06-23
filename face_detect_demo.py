import cv2
import math

# Load the cascade
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('HS.xml')
# Read the input image
img = cv2.imread('couple.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def draw_lines(frame, faces):
    for (x, y, w, h) in faces:
        for (x2, y2, w2, h2) in faces:
            if(x == x2 and y == y2):
                continue
            center_1 = (((x+int(w/2)), (y+int(h/2))))
            center_2 = ((x2+int(w2/2), (y2+int(h2/2))))

            # print("CENTER 1 " + str(center_1))
            # print("CENTER 2 " + str(center_2))
            dis = math.sqrt((x-x2)**2 + (y-y2)**2)
            print("DISTANCE = " + str(dis))
            cv2.line(frame, center_1, center_2, (0, 0, 255), 2)
    return 0

#cv2.rectangle(img, (0, 0), (380, 218), (255, 0, 0,), 2)


# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
draw_lines(img, faces)
print("Faces ", faces)
# Draw rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
# Display the output
cv2.imshow('img', img)
cv2.waitKey()
