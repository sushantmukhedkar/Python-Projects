import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from signature import match
import mysql.connector 

# Matching Threshold
THRESHOLD = 85 

#connecting to the database

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ashw@123",
    database="student_db"
)

cursor=db.cursor()

# Create a table to store student information
cursor.execute(
    '''
create table if not exists students
 (id int auto_increment primary key , 
 name varchar(255) , reg_no varchar(255))
'''
)

def browsefunc(ent):
    filename = askopenfilename(filetypes=[
        ("Image", ".jpeg"),
        ("Image", ".png"),
        ("Image", ".jpg"),
    ])
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

# Define the directory to store captured images
capture_directory = r"C:\Users\ashun\OneDrive\Pictures\Camera Roll"

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC key pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE key pressed
            if not os.path.isdir(capture_directory):
                os.mkdir(capture_directory, mode=0o777)  # Make sure the directory exists
            if sign == 1:
                img_name = os.path.join(capture_directory, "test_img1.png")
            else:
                img_name = os.path.join(capture_directory, "test_img2.png")
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    if sign == 1:
        filename = os.path.join(capture_directory, "test_img1.png")
    else:
        filename = os.path.join(capture_directory, "test_img2.png")
    res = messagebox.askquestion('Click Picture', 'Press Space Bar to capture an image and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure: Signatures Do Not Match", "Signatures are {:.2f}% similar.".format(result))
    else:
        messagebox.showinfo("Success: Signatures Match", "Signatures are {:.2f}% similar.".format(result))
    return True

def deleteCapturedImages():
    if os.path.exists(os.path.join(capture_directory, "test_img1.png")):
        os.remove(os.path.join(capture_directory, "test_img1.png"))
    
    if os.exists(os.path.join(capture_directory, "test_img2.png")):
        os.remove(os.path.join(capture_directory, "test_img2.png"))

def get_student_info():
    name = name_entry.get()
    reg_no = reg_no_entry.get()

    cursor.execute('insert into students (name,reg_no) values(%s,%s)',(name,reg_no))
    db.commit()
    messagebox.showinfo("Student Information", f"Name: {name}\nRegistration No: {reg_no}")

root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")  # Set the window size

# Add labels for student info
student_info_label = tk.Label(root, text="Student Information", font=12)
student_info_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

name_label = tk.Label(root, text="Student Name:", font=10)
name_label.grid(row=1, column=0, padx=10, pady=10)

reg_no_label = tk.Label(root, text="Registration Number:", font=10)
reg_no_label.grid(row=2, column=0, padx=10, pady=10)

# Add entry fields for student info
name_entry = tk.Entry(root, font=10)
name_entry.grid(row=1, column=1, padx=10, pady=10)

reg_no_entry = tk.Entry(root, font=10)
reg_no_entry.grid(row=2, column=1, padx=10, pady=10)

# Add signature comparison section
signature_compare_label = tk.Label(root, text="Compare Two Signatures", font=12)
signature_compare_label.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

img1_message = tk.Label(root, text="Signature 1", font=10)
img1_message.grid(row=4, column=0, padx=10, pady=10)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.grid(row=4, column=1, padx=10, pady=10)

img1_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.grid(row=4, column=2, padx=10, pady=10)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.grid(row=4, column=3, padx=10, pady=10)

img2_message = tk.Label(root, text="Signature 2", font=10)
img2_message.grid(row=5, column=0, padx=10, pady=10)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.grid(row=5, column=1, padx=10, pady=10)

img2_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.grid(row=5, column=2, padx=10, pady=10)

img2_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.grid(row=5, column=3, padx=10, pady=10)

compare_button = tk.Button(
    root, text="Compare", font=10, command=lambda: checkSimilarity(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get()))
compare_button.grid(row=6, column=0, padx=10, pady=10, columnspan=4)

get_info_button = tk.Button(
    root, text="Get Student Info", font=10, command=get_student_info)
get_info_button.grid(row=7, column=0, padx=10, pady=10, columnspan=4)

delete_button = tk.Button(
    root, text="Delete Captured Images", font=10, command=deleteCapturedImages)
delete_button.grid(row=8, column=0, padx=10, pady=10, columnspan=4)

root.mainloop()
