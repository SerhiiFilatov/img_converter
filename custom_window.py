import customtkinter
import imghdr
import os
import time
import threading
import tkinter as tk

from PIL import Image
from pillow_heif import register_heif_opener
from pypdf import PdfWriter
from tkinter import filedialog
from tkinter import messagebox
from typing import List

import data

register_heif_opener()



class MainWindow:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("Image converter")
        self.app.geometry("400x250+800+300")
        self.uploaded_images = []
        self.conv_imeges = 0
        self.text = ''
        self.type_for_convert = ''
        self.create_objects()

    def open_file(self):
        input_file_path = filedialog.askopenfilenames(
            title="Select an image",
            filetypes=[("Image files", "*.png;*.jpg;*.gif;*.bmp;*.heic;*.pdf;*.jpeg"), ("All files", "*.*")]
        )
        valid_images = [file for file in input_file_path if imghdr.what(file) is not None
                        or file.lower().endswith(".heic") or file.lower().endswith(".pdf")]

        self.uploaded_images = valid_images
        return input_file_path

    def convert_and_save(self):
        if not self.uploaded_images:
            messagebox.showinfo("No Images", "No images selected.")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")
        if not output_folder:
            return

        threading.Thread(target=self.conversion_thread, args=(output_folder,)).start()


    def conversion_thread(self, output_folder):

        for input_file_path in self.uploaded_images:
            img = Image.open(input_file_path)
            output_file_path = os.path.join(output_folder,
                                            f"{os.path.splitext(os.path.basename(input_file_path))[0]}."
                                            f"{self.type_for_convert}")
            img.save(output_file_path)
            print(f"Image {os.path.basename(input_file_path)} converted and saved to {output_file_path}")

        messagebox.showinfo("Conversion Complete", "Images converted and saved successfully.")

    def combobox_callback(self, choice):
        self.type_for_convert = choice
        print(self.type_for_convert)

    def merge_pdf(self):
        merger = PdfWriter()

        if not self.uploaded_images:
            messagebox.showinfo("No Images", "No images selected.")
            return

        if not self.check_if_pdf():
            messagebox.showinfo("No PDF")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")
        if not output_folder:
            return

        output_filepath = f"{output_folder}/merged-pdf.pdf"

        for pdf in self.uploaded_images:
            merger.append(pdf)

        with open(output_filepath, 'wb') as output_file:
            merger.write(output_file)

        messagebox.showinfo("Merge Complete", f"PDF files merged and saved to {output_filepath}")

    def check_if_pdf(self):
        for file in self.uploaded_images:
            if file.lower().endswith(".pdf"):
                return True


    def create_objects(self):

        self.button_upload = MyButton(
            root=self.app, text='Завантажити', height=30, width=70,
            x=30, y=30, command=self.open_file
        )

        self.button_convert_img = MyButton(
            root=self.app, text='Конвертувати', height=30, width=70,
            x=270, y=30, command=self.convert_and_save
        )

        self.button_merge_pdf = MyButton(
            root=self.app, text='Об\'єднати pdf',height=30,width=70,
            x=270, y=70,
            command=self.merge_pdf
        )

        self.type_of_image = MyComboBoxButton(
            root=self.app, values=data.file_types, height=30, width=96, x=150, y=30, command=self.combobox_callback
        )

        # self.progressbar = MyProgressBar(
        #     root=self.app, x=50, y=150
        # )
        # self.progressbar.set_value(0)

        # self.info_panel = MyLabel(root=self.app, text=self.text, height=70, width=120, x=230, y=130)

    def run(self):
        self.app.mainloop()



class MyComboBoxButton:
    def __init__(self, root, height, width, x, y, values: List, command):
        self.combobox_button = customtkinter.CTkComboBox(
            root, justify='left', state="readonly", height=height,
            width=width, values=values, command=command
        )
        self.combobox_button.place(x=x, y=y)

    def get_value(self, event=None):
        select_value = self.combobox_button.get()
        return select_value



class MyButton:
    def __init__(self, root, text, height, width, x, y, command=None):
        self.button = customtkinter.CTkButton(root, text=text, height=height, width=width, command=command)
        self.button.place(x=x, y=y)



class MyLabel:
    def __init__(self, root, text, height, width, x, y):
        self.label = customtkinter.CTkLabel(
            root, text=text, height=height, width=width, fg_color='white',
            text_color='black', corner_radius=20
        )
        self.label.place( x=x, y=y)

    def update_text(self, new_text):
        self.label.configure(text=new_text)



class MyProgressBar:
    def __init__(self, root, x, y):
        self.progressbar = customtkinter.CTkProgressBar(
            root, orientation="horizontal", width=80, height=20, border_width=3, corner_radius=1,
            border_color='black', fg_color='black', progress_color='green', mode="determinate")
        self.progressbar.place(x=x, y=y)

    def set_value(self, val):
        self.progressbar.set(val)

    def upd(self):
        self.progressbar.update()