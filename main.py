import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# set folder directories
picture_dir = "pictures"
downloaded_pic_dir = "downloaded_pics"

# create folder directories if they don't exist
if not os.path.exists(picture_dir):
    os.makedirs(picture_dir)

if not os.path.exists(downloaded_pic_dir):
    os.makedirs(downloaded_pic_dir)

image_list = [
    image_filename
    for image_filename in os.listdir(picture_dir)
    if image_filename.endswith(".jpeg")
]

def resize_images(source_folder, destination_folder, new_size):
    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path) and filename.lower().endswith(".avif"):
            os.remove(file_path)
            print(".avif file is unsupported. sorry")

        if os.path.isfile(file_path) and filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
        ):
            try:
                # Open the image using Pillow
                img = Image.open(file_path)

                # Resize the image
                img = img.resize(new_size, Image.LANCZOS)

                # Save the resized image to the destination folder
                new_file_path = os.path.join(destination_folder, filename)

                if filename.lower().endswith(
                    (".webp", ".png", ".jpg", ".jpeg", ".gif", ".bmp")
                ):
                    # Convert to JPEG before saving if it's in webp, or other supported formats
                    converted_file_path = (
                        os.path.splitext(new_file_path)[0] + ".jpeg"
                    )
                    img = img.convert(
                        "RGB"
                    )  # Convert to RGB mode before saving as JPEG
                else:
                    converted_file_path = new_file_path

                img.save(converted_file_path)

                # Delete raw picture after resizing
                os.remove(file_path)

                print(
                    f"Resized, saved and removed {file_path}: {converted_file_path}"
                )
            except Exception as e:
                with open("B:\errors.txt", "a") as errors:
                    errors.write(f"Error: {str(e)}\n")


def show_next_image(event):
    global current_image_index, current_image, tk_image

    # Update the current image index
    current_image_index = (current_image_index + 1) % len(image_list)

    # Load the next image
    current_image_path = os.path.join(
        picture_dir, image_list[current_image_index]
    )
    current_image = Image.open(current_image_path)
    tk_image = ImageTk.PhotoImage(current_image)

    # Update the image on the label
    image_label.configure(image=tk_image)
    image_label.image = tk_image
    image_label.place(relx=0.5, rely=0.5, anchor="center")


def show_last_image(event):
    global current_image_index, current_image, tk_image

    # Update the current image index
    current_image_index = (current_image_index - 1) % len(image_list)

    # Load the next image
    current_image_path = os.path.join(
        picture_dir, image_list[current_image_index]
    )
    current_image = Image.open(current_image_path)
    tk_image = ImageTk.PhotoImage(current_image)

    # Update the image on the label
    image_label.configure(image=tk_image)
    image_label.image = tk_image
    image_label.place(relx=0.5, rely=0.5, anchor="center")


# Initialize tkinter
window = tk.Tk()
window.title("Image Viewer")
window.geometry("1920x1080")
window.configure(background="#61677A")
print("initializing window!")

# Try to Load the first image. Display warning if list is empty
current_image_index = 0
try:
    current_image_path = os.path.join(
        picture_dir, image_list[current_image_index]
    )
except IndexError:
    messagebox.showinfo(
        title="No Images Found",
        message=f"Please add some images to {os.path.join(os.getcwd(), downloaded_pic_dir)}\
                \n\nYou can download from google images or add your own :)",
    )
    exit(0)
else:
    current_image = Image.open(current_image_path)
    tk_image = ImageTk.PhotoImage(current_image)
    print("setting up pictures!")

# Create a label to display the image
image_label = tk.Label(window, image=tk_image)
image_label.pack()
image_label.place(relx=0.5, rely=0.5, anchor="center")


# resize any images in the raw_images folder if there are any and add them to pictures
resize_images(downloaded_pic_dir, picture_dir, (600, 600))


# Bind the right arrow key press event to the function
window.bind("<Right>", show_next_image)
window.bind("<Left>", show_last_image)

# Start the main event loop
window.mainloop()
