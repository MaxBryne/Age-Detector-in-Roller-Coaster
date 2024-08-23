# Import the necessary libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from turtle import heading
from csv import DictWriter
import datetime
import os
import numpy as np


# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age and Gender Detector')
top.configure(background='#CDCDCD')

# Loading the Model
from keras.models import load_model
model = load_model('Age_Sex_Detector.h5')

# Initializing the labels for both age and gender
label1 = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
label2 = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)

# Initializing the function to Detect Age and Gender
def Detect(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((48, 48))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    image = np.delete(image, 0, 1)
    image = np.resize(image, (48, 48, 3))
    print(image.shape)
    
    sex_f = ['Male', 'Female']
    image = np.array([image])/255
    pred = model.predict(image)
    age = int(np.round(pred[1][0]))
    sex = int(np.round(pred[0][0]))
    
    if(13<=age<=60):
        print(f"Predicted Age is {age}")
        print(f"Predicted Gender is {sex}")
    else:
        print("Not Allowed")
    
    entry = datetime.datetime.now().time()
    entry_time = datetime.isoformat(entry)
    
    with open('file.csv', 'a', newline='') as f:
        dict_writer = DictWriter(f, fieldnames=['Age', 'Gender', 'Entry Time'])
        if os.stat('file.csv').st_size == 0:
            dict_writer.writeheader()
            
        dict_writer.writerow({
            'Age': age,
            'Gender': sex,
            'Entry Time': entry_time
        })
        
    label1.configure(foreground='#011638', text=age)
    label2.configure(foreground='#011638', text=sex_f[sex])
    
# Defining Show_Detect button function
def show_detect_btn(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)
    
# Defining upload image function
def uplaod_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)
        
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_detect_btn(file_path)
    except:
        pass
    
upload = Button(top, text="Upload an Image", command=uplaod_image, padx=10, pady=5)
upload.configure(background='#234156', foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)

sign_image.pack(side='bottom', expand=True)
label1.pack(side='bottom', expand=True)
label2.pack(side='bottom', expand=True)
heading = Label(top, text="Age and Gender Detector", pady=20, font=('arial', 10, 'bold'))
heading.configure(background='#CDCDCD', foreground='#364156')
heading.pack()
top.mainloop()