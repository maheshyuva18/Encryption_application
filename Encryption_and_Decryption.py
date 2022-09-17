# Import the required Libraries
from tkinter import *
from tkinter.filedialog import askopenfile
from cryptography.fernet import Fernet
import os

# Create an instance of tkinter frame
win = Tk()
win.title("Encryption and Decryption")
content = None
file_name = None
strvar = StringVar(win, "Only for decryption")
# Set the geometry of tkinter frame
win.geometry("700x350")

def open_file():
    global file_name
    global content
    file = askopenfile(mode='r', filetypes=[('text Files', '*.txt'),('encrypted ','*.enc')])
    if file:
        file_name = file.name.split('/')[-1]
        content = file.read()
    file.close()
    os.remove(file.name)

def encryptor():
    global content
    global file_name
    key = Fernet.generate_key()
    
    with open('keys.txt','ab') as filekey:
        filekey.write(bytes((file_name.split(".")[0]+" : "),'utf-8'))
        filekey.write(key)
        filekey.write(bytes("\n",'utf-8'))
    
    original = bytes(content, 'utf-8')

    #Encrypting
    fernet = Fernet(key)
    encrypted = fernet.encrypt(original)

    # writing encrypted data
    with open(file_name.split(".")[0]+".enc",'wb') as enc_file:
        enc_file.write(encrypted)

def decryptor():
    global content
    global file_name
    key = strvar.get()

    fernet = Fernet(key)

    
    encrypted =  bytes(content,"utf-8")

    decrypted = fernet.decrypt(encrypted)

    with open(file_name.split(".")[0]+".txt",'wb') as dec_file:
        dec_file.write(decrypted)

# Add a Label widget
label = Label(win, text="Click the Button to browse the Files", font=('Georgia 13'))
label.pack(pady=10)

# Create a Buttonos
Button(win, text= "Browse", command=open_file).pack(pady=20)
Button(win, text = "Encrypt", command= encryptor).pack(pady=20)
T = Entry(win, width=20, textvariable=strvar)
T.pack(pady = 20)
Button(win, text = "Decrypt", command= decryptor).pack(pady=20)
win.mainloop()
