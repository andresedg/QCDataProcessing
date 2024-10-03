import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory

def test_tkinter():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filedirectory = askdirectory(title='Select folder')
    root.destroy()
    return filedirectory


directory = test_tkinter()
print(directory)