import cv2
import math
from face import Face
import numpy as np
from tkinter import *
from tkinter import filedialog
import tkinter as tk

# Load the cascade
face_cascade = cv2.CascadeClassifier('HS.xml')
head_cascade = cv2.CascadeClassifier('face_front.xml')


def detect(n, d, c):
    print("D " + d)
    print("C " + c)

    if c is '':
        c = 20

    if d is '':
        d = 50

    input_distance = int(d)
    input_color_threshold = int(c)

    img = ''

    if n == 1:
        # Read the input image
        path = filedialog.askopenfilename()
        img = cv2.imread(path)

    if n == 0:
        cam = cv2.VideoCapture(0)
        while True:
            ret, frame = cam.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            HS = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in HS:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (100, 100, 0), 2)
            cv2.imshow("Input", frame)
            k = cv2.waitKey(1)
            if k % 256 == 27:
                print("Closing...")
                break
            elif k % 256 == 32:
                img_name = "OpenCV_Input.png"
                cv2.imwrite("./pictures/openCV_Input.png", frame)
                img = cv2.imread("./pictures/openCV_Input.png")
                break

        cam.release()
        # cv2.namedWindow("Input")

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (3, 3))
    # cv2.imshow("Blur", gray)

    def draw_lines_again(frame, face_list):
        for f in face_list:
            for f2 in face_list:
                if f.x == f2.x and f.y == f2.y:
                    continue
                center_1 = ((f.x + int(f.w / 2), (f.y + int(f.h / 2))))
                center_2 = ((f2.x + int(f2.w / 2), (f2.y + int(f2.h / 2))))
                dist = math.sqrt((f.x - f2.x)**2 + (f.y - f2.y)**2)
                inches = (dist / f2.w) * 16
                print("DIST: ", str(inches))
                if inches <= input_distance:
                    cv2.line(frame, center_1, center_2, (0, 0, 255), 2)
        return 0

    def compareColorAverage(top_matrix, bottom_matrix):
        top_average = np.mean(top_matrix)
        bottom_average = np.mean(bottom_matrix)
        print("TOP AVG: ", str(top_average))
        print("BOTTOM AVG: ", str(bottom_average))
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

            #cv2.imshow(str(y), top_matrix)
            #cv2.imshow(str(x), bottom_matrix)

            color_ratio = compareColorAverage(top_matrix, bottom_matrix)
            if color_ratio <= input_color_threshold:
                face.isMask = True
            else:
                face.isMask = False

    # Draw things
    for f in face_list:
        print("MASK: ", f.isMask)
        box_color = (0, 255, 0)
        if f.isMask:
            box_color = (0, 0, 255)
        cv2.rectangle(img, (f.x, f.y), (f.x_end, f.y_end), box_color, 2)
        # Display distance from camera
        cv2.putText(img,
                    str(f.est_dist),
                    (f.x, f.y),
                    f.font, 1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_4)

    draw_lines_again(img, face_list)

    # Display the output
    cv2.imwrite("./pictures/output.jpg", img)

    output = cv2.imread("./pictures/output.jpg")
    cv2.imshow("OUTPUT", output)

    cv2.waitKey()


root = Tk()

frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

lbl = Label(root)
lbl.pack()

Label(
    root, text="Minimal Distance (inches) [Default = 50 inches]", pady=20).pack()
input = Entry(root)
input.pack()

Label(root, text="Color Threshold [Default = 20]", pady=20).pack()
input2 = Entry(root)
input2.pack()

Label(root, text="Allow box to focus on subject and use Spacebar to take picture", pady=50).pack()

btn = Button(frm, text="Upload Image",
             command=lambda: detect(1, input.get(), input2.get()))
btn.pack(side=tk.LEFT)

btn3 = Button(frm, text="Upload from webcam",
              command=lambda: detect(0, input.get(), input2.get()))
btn3.pack(side=tk.LEFT, padx=10)

btn2 = Button(frm, text="Exit", command=lambda: exit())
btn2.pack(side=tk.LEFT, padx=10)

root.title("SVI with Images")
root.geometry("350x350")
root.mainloop()
