from tkinter import* #Imports all classes, functions, and variables from the tkinter library.
from tkinter import filedialog # Imports the filedialog module from the tkinter library for opening file dialogs.

root=Tk() #Creates the main application window.
root.geometry("200x60") #Sets the initial size of the window to 200x60 pixels.

def encrypt_image(): #This function is called when the "encrypt" button is clicked.
    file1= filedialog.askopenfile(mode='r',filetypes=[('jpg file', '*.jpg')])
    if file1 is not None:
        #print(file1)
        file_name= file1.name
        print(file_name)
        key= entry1.get(1.0, END) #reads the encryption key from a Text widget and stores it in the key variable.
        print(file_name, key)
        fi= open(file_name,'rb') #opens a file dialog for the user to select a .jpg image file for encryption.
        image= fi.read() #reads the file as bytes and stores it in the image variable
        fi.close()
        image=bytearray(image)
        for index,values in enumerate(image):
            image[index]=values^int(key) #performs a bitwise XOR operation between each byte of the image and the integer value of the key to encrypt the image.
        fi1=open(file_name,'wb')
        fi1.write(image)
        fi1.close()
b1=Button(root, text="encrypt", command=encrypt_image) #Creates a button labeled "encrypt" that calls the encrypt_image function when clicked.
b1.place(x=70, y=10) #positioning of the encrypt button

entry1= Text(root, height=1, width=10)
entry1.place(x=50, y=50)

root.mainloop() #starts the main event loop
