import imghdr
from pypdf import PdfWriter
import os
from PIL import Image
from pillow_heif import register_heif_opener
import tkinter as tk
from typing import List
from tkinter import ttk, messagebox
from tkinter import filedialog


import data





class MainWindow:
    def __init__(self, title='Image converter'):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.config(bg='grey')
        self.root.geometry('300x250+700+360')
        self.root.resizable(False, False)
        self.root.option_add("*tearOff", False)
        self.text = f'Обрано: 0\n' \
                    f'Конвертувати в : '
        self.uploaded_images = ()
        self.type_for_convert = ''
        self.create_buttons()
        self.create_label()
        self.create_progressbar()

    def open_file(self):
        input_file_path = filedialog.askopenfilenames(
            title="Select an image",
            filetypes=[("Image files", "*.png;*.jpg;*.gif;*.bmp;*.heic;*.pdf"), ("All files", "*.*")]
        )
        valid_images = [file for file in input_file_path if imghdr.what(file) is not None
                        or file.lower().endswith(".heic") or file.lower().endswith(".pdf")]

        self.uploaded_images = valid_images
        self.text = f'Обрано: {len(self.uploaded_images)}\n' \
                    f'Конвертувати в : {self.type_for_convert}'
        self.header.update_text(self.text)
        return input_file_path

    def convert_and_save(self):
        if not self.uploaded_images:
            messagebox.showinfo("No Images", "No images selected.")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")

        if not output_folder:
            return

        for input_file_path in self.uploaded_images:
            img = Image.open(input_file_path)
            output_file_path = os.path.join(output_folder,
                                            f"{os.path.splitext(os.path.basename(input_file_path))[0]}."
                                            f"{self.type_for_convert}")
            img.save(output_file_path)
            print(f"Image {os.path.basename(input_file_path)} converted and saved to {output_file_path}")

        messagebox.showinfo("Conversion Complete", "Images converted and saved successfully.")
        self.text = f'Обрано: 0\n' \
                    f'Конвертувати в : '
        self.header.update_text(self.text)

    def merge_pdf(self):
        merger = PdfWriter()

        if not self.uploaded_images:
            messagebox.showinfo("No Images", "No images selected.")
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

    def on_combobox_select(self, event):
        self.type_for_convert = self.button_type_for_convert.get_value()
        self.text = f'Обрано: {len(self.uploaded_images)}\n' \
                    f'Конвертувати в : {self.type_for_convert}'
        self.header.update_text(self.text)

    def create_buttons(self):
        self.button_convert = MyButton(
            root=self.root,
            text='Convert image',
            height=40,
            width=90,
            x=20,
            y=130,
            command=self.convert_and_save
        )

        self.button_merge_pdf = MyButton(
            root=self.root,
            text='Merge pdf',
            height=40,
            width=90,
            x=20,
            y=180,
            command=self.merge_pdf
        )
        self.button_download = MyButton(
            root=self.root,
            text='Download',
            height=40,
            width=90,
            x=20,
            y=30,
            command=self.open_file
        )
        self.button_type_for_convert = MyComboBoxButton(
            root=self.root,
            justify='center',
            values=data.file_types,
            height=25,
            width=90,
            x=20,
            y=90,
        )
        self.button_type_for_convert.combobox_button.bind("<<ComboboxSelected>>", self.on_combobox_select)

    def create_label(self):
        self.header = MyLabel(root=self.root, text=self.text, height=40, width=120, x=130, y=30)

    def create_progressbar(self):
        self.progressbar = MyProgressbar(x=130, y=140)

    def run(self):
        self.root.mainloop()



class MyLabel:
    def __init__(self, root, text, height, width, x, y):
        self.label = ttk.Label(root, text=text, anchor='c', background='green', foreground='black')
        self.label.place(height=height, width=width, x=x, y=y)

    def update_text(self, new_text):
        self.label.config(text=new_text)



class MyButton:
    def __init__(self, root, text, height, width, x, y, command=None):
        self.button = ttk.Button(root, text=text, command=command)
        self.button.place(height=height, width=width, x=x, y=y)



class MyComboBoxButton:
    def __init__(self, root, height, width, x, y, justify, values: List):
        self.combobox_button = ttk.Combobox(
            root,
            justify=justify,
            state="readonly",
            values=values
        )
        self.combobox_button.place(height=height, width=width, x=x, y=y)

    def get_value(self, event=None):
        select_value = self.combobox_button.get()
        return select_value



class MyProgressbar:
    def __init__(self, x, y,):
        self.progressbar = ttk.Progressbar(orient="horizontal", length=100, value=1)
        self.progressbar.place(x=x, y=y)