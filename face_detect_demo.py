import cv2
import math
from face import Face
import numpy as np

# Load the cascade
face_cascade = cv2.CascadeClassifier('HS.xml')
mouth_cascade = cv2.CascadeClassifier('Mouth.xml')
head_cascade = cv2.CascadeClassifier('face_front.xml')
# Read the input image
img = cv2.imread('./pictures/mask2.bmp')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def draw_lines_again(frame, face_list):
    for f in face_list:
        for f2 in face_list:
            if f.x == f2.x and f.y == f2.y:
                continue
            center_1 = ((f.x + int(f.w / 2), (f.y + int(f.h / 2))))
            center_2 = ((f2.x + int(f2.w / 2), (f2.y + int(f2.h / 2))))
            dist = math.sqrt((f.x - f2.x)**2 + (f.y - f2.y)**2)
            inches = (dist / f2.w) * 16
            if inches <= 15:
                cv2.line(frame, center_1, center_2, (0, 0, 255), 2)
    return 0


def compareColorAverage(top_matrix, bottom_matrix):
    top_average = np.mean(top_matrix)
    bottom_average = np.mean(bottom_matrix)
    color_ratio = abs(top_average - bottom_average)
    return color_ratio


# Detect faces + shoulders
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
face_list = []
for (x, y, w, h) in faces:
    cFace = Face(x, y, w, h)
    face_list.append(cFace)

# create a list of just faces
heads = []
for h in head_cascade.detectMultiScale(img, 1.1, 4):
    heads.append(h)

for face in face_list:
    print(face.x)
    # Display distance from camera
    cv2.putText(img,
                str(face.est_dist),
                (face.x, face.y),
                face.font, 1,
                (0, 255, 0),
                2,
                cv2.LINE_4)

    # Isolate head+shoulder into matrix
    face_mat = gray[face.y: face.y_end, face.x: face.x_end]
    # cv2.imshow(str(face.x), face_mat)
    # Try to find a face in head+shoulder matrix
    head = head_cascade.detectMultiScale(face_mat, 1.1, 4)

    if len(head) > 0:  # If no head is detected, then mask is found
        face.isMask = True
        face.box_color = (0, 0, 255)

    for(x, y, w, h) in head:
        # Must add (face.x and face.y) to rectangle to account for dimension of entire image
        cv2.rectangle(img, (x+face.x, y+face.y),
                      (x+face.x+w, y+face.y+h), (0, 0, 255), 1)
        matrix = gray[y+face.y:face.y+y+h, face.x+x:face.x+x+w]

        top_matrix = matrix[0:y, :]
        bottom_matrix = matrix[y:y+h, :]

        # cv2.imshow(str(x), bottom_matrix)

        color_ratio = compareColorAverage(top_matrix, bottom_matrix)
        # print("BOOHOO " + str(color_ratio))
        if color_ratio >= 4:
            face.isMask = True
        else:
            face.isMask = False

# Draw things
for f in face_list:
    print(f.isMask)
    box_color = (0, 255, 0)
    if f.isMask:
        box_color = (0, 0, 255)
    cv2.rectangle(img, (f.x, f.y), (f.x_end, f.y_end), box_color, 2)

draw_lines_again(img, face_list)

# Display the output
cv2.imshow('img', img)
cv2.waitKey()
