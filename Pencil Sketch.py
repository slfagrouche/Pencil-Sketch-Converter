# Pencil Sketch Converter
# Author: Said Lfagrouche
# Description: This program allows users to upload an image and convert it to a pencil sketch using OpenCV and Tkinter.

import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, Label
from PIL import ImageTk, Image


class PencilSketchConverter:
    def __init__(self):
        self.window = Tk()
        self.window.title("Pencil Sketch Converter")
        self.window_width = 800
        self.window_height = 600
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.x = (self.screen_width // 2) - (self.window_width // 2)
        self.y = (self.screen_height // 2) - (self.window_height // 2)

        # Load and set the background image
        background_image = Image.open("/Users/saidlfagrouche/Downloads/hand-pencil-drawing-sketch-wallpaper-preview.jpg")
        background_image = background_image.resize((self.window_width, self.window_height), Image.ANTIALIAS)
        self.background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(self.window, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set up image placeholders
        self.original_image_label = Label(background_label)
        self.pencil_sketch_label = Label(background_label)

        #setting up clear upload_button
        self.upload_button = Button(
            background_label,
            text="Upload Image",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="#000000",
            width=20,
            height=2,
            command=self.upload_image,
        )

        #setting up clear images button
        self.clear_button = Button(
            background_label,
            text="Clear",
            font=("Arial", 16, "bold"),
            bg="#f44336",
            fg="#000000",
            width=7,
            height=2,
            command=self.clear_images,
        )

        #seting window size and center it on the screen
        self.window.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")
        self.window.configure(bg="#f0f0f0")

        #position the components
        self.original_image_label.place(x=50, y=50)
        self.pencil_sketch_label.place(x=self.window_width // 2 + 50, y=50)

        # centering the two buttons vertically between the pics
        button_x = self.window_width // 2 - 100 +52
        upload_button_button_x = self.window_width // 2 - 100
        button_y = (self.window_height - 100) // 2
        self.upload_button.place(x=upload_button_button_x, y=button_y - 100 - 150)
        self.clear_button.place(x=button_x, y=button_y + 100 - 300)


    def upload_image(self):
        #open file dialog to select an image file
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG Files", "*.jpg; *.jpeg"), ("HEIC Files", "*.heic"), ("PNG Files", "*.png")]
        )

        #check if a file was selected
        if file_path:
            self.display_images(file_path)

    def display_images(self, image_path):
        # load the image and resize
        image = Image.open(image_path)
        image = image.resize((int(self.window_width / 2) - 100, int(self.window_height) - 100), Image.ANTIALIAS)

        #convert the image to photo-image format for display in Tkinter
        image_tk = ImageTk.PhotoImage(image)

        # update the original image label
        self.original_image_label.config(image=image_tk)
        self.original_image_label.image = image_tk

        # convert the image to a penccil sketch
        pencil_sketch = self.generate_pencil_sketch(image_path)

        #cnvert the pencil sketch to PhotoImage format for display in Tkinter
        pencil_sketch_tk = ImageTk.PhotoImage(pencil_sketch)

        # update the pencil sketch label
        self.pencil_sketch_label.config(image=pencil_sketch_tk)
        self.pencil_sketch_label.image = pencil_sketch_tk

    def generate_pencil_sketch(self, image_path, kernel_size=21):
        #load the image
        image = cv2.imread(image_path)

        #convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #invert the grayscale image
        inverted_image = 255 - gray_image

        #apply Gaussian blur to the invertted image
        blurred = cv2.GaussianBlur(inverted_image, (kernel_size, kernel_size), 0)

        #invert the blurred image
        inverted_blurred = 255 - blurred

        # ceating a pencil sketch effect bydividing the grayscale image by the invverted blurred image
        pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)

        # converting the pencil sketch imagee back to PIL format
        sketch_image = Image.fromarray(pencil_sketch)

        #resize the image to fit the window
        sketch_image = sketch_image.resize((int(self.window_width / 2) - 100, int(self.window_height) - 50), Image.ANTIALIAS)
        return sketch_image


    def clear_images(self):
        # clearing the image labels for new tries/images uploads
        self.original_image_label.config(image="")
        self.pencil_sketch_label.config(image="")

    def run(self):
        #runnig the Tkinter event loop
        self.window.mainloop()


# Making object of our PencilSketchConverter and run by calling run()
converter = PencilSketchConverter()
converter.run()
