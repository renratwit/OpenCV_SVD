from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os


def showImage():
    path = filedialog.askopenfilename()
    img = cv2.imread(path)
    cv2.imshow("STR", img)


root = Tk()

frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

lbl = Label(root)
lbl.pack()

btn = Button(frm, text="Upload Image", command=showImage)
btn.pack(side=tk.LEFT)

btn2 = Button(frm, text="Exit", command=lambda: exit())
btn2.pack(side=tk.LEFT, padx=10)

root.title("Image Browser")
root.geometry("300x350")
root.mainloop()
