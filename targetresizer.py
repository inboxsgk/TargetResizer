from PIL import Image
import os
import shutil
import apytl
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def resize_image(input_image_path, output_image_path, target_size_kb):
    init_size = round(os.path.getsize(input_image_path) / 1024, 2)

    with Image.open(input_image_path) as image:
        shutil.copy(input_image_path, output_image_path)

        # Calculate aspect ratio
        aspect_ratio = image.width / image.height

        # Reduce image size in a loop until it's smaller than the target size
        while os.path.getsize(output_image_path) > target_size_kb * 1024:

            # Calculate new width and height while maintaining aspect ratio
            if aspect_ratio > 1:
                new_width = int(image.width * 0.9)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = int(image.height * 0.9)
                new_width = int(new_height * aspect_ratio)

            # Resize image
            resized_image = image.resize((new_width, new_height))

            # Save resized image with reduced quality
            resized_image.save(output_image_path, optimize=True, quality=85)
            image = resized_image

            cur_size = round(os.path.getsize(output_image_path) / 1024, 2)
            percent = ((init_size - cur_size) / (init_size - target_size_kb)) * 100
            if percent > 0:
                apytl.Bar().drawbar(percent, 100, fill="=")
        print("\n\nReduced image size to", round(os.path.getsize(output_image_path) / 1024, 2), "KB")


output_image_path = 'output_img.jpg'


#Interactve inputs on runtime
Tk().withdraw()
input_image_path = askopenfilename()
print("Chosen file size:", (os.stat(input_image_path).st_size/1024))
target_size_kb = int(input("What size do you want the output to be? (in KB)\n"))

# Resize image to target file size
resize_image(input_image_path, output_image_path, target_size_kb)
