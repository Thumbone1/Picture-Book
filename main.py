import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps


# ---------------------------Initialize Lists and directory---------------------------#

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

download_list = [
    image_filename for image_filename in os.listdir(downloaded_pic_dir)
]

# --------------------------------- Program Logic ----------------------------------#


def resize_images(source_folder, destination_folder, max_size):
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
                img = Image.open(file_path)
                img = ImageOps.exif_transpose(img)  # do not rotate images
                img.thumbnail(max_size)  # resize and keep aspect ratio

                new_file_path = os.path.join(destination_folder, filename)

                if filename.lower().endswith(
                    (".webp", ".png", ".jpg", ".gif", ".bmp")
                ):
                    # Convert to JPEG before saving if it's in webp, or other supported formats
                    converted_file_path = (
                        os.path.splitext(new_file_path)[0] + ".jpeg"
                    )
                    # Convert to RGB mode before saving as JPEG
                    img = img.convert("RGB")
                else:
                    converted_file_path = new_file_path

                img.save(converted_file_path, "JPEG")

                os.remove(file_path)  # Delete raw picture after resizing
                print(
                    f"Resized, saved and removed {file_path}: {converted_file_path}"
                )

            # log any errors while trying to open/convert/save picture
            except Exception as e:
                with open(f"{os.getcwd()}\\errors.txt", "a") as errors:
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


# ----------------------------- Initialize tkinter ------------------------------#

window = tk.Tk()
window_width = int(window.winfo_screenwidth() * 0.75)
window_height = int(window.winfo_screenheight() * 0.75)
window.title("Picture Viewer")
window.geometry(f"{window_width}x{window_height}")
window.configure(background="#61677A")
print("initializing window!")

# ---------------------------- Check for empty lists ----------------------------#

# need to check here to pass window_width and height to resize_images
# also to prevent an index out of bounds error when checking image list in 
if not image_list and not download_list:
    messagebox.showinfo(
        title="No Images Found",
        message=f"Please add some images to {os.path.join(os.getcwd(), downloaded_pic_dir)}\
                \n\nYou can download from google images or add your own :)",
    )
    exit(0)

else:
    # resize any images in the raw_images folder if there are any and add them to pictures
    resize_images(
        downloaded_pic_dir,
        picture_dir,
        (int(window_width * 0.8), int(window_height * 0.8)),
    )
    image_list = [
        image_filename
        for image_filename in os.listdir(picture_dir)
        if image_filename.endswith(".jpeg")
    ]

# --------------------------------- UI -------------------------------------#

# Load the first image.
current_image_index = 0
current_image_path = os.path.join(picture_dir, image_list[current_image_index])
current_image = Image.open(current_image_path)
tk_image = ImageTk.PhotoImage(current_image)

# Create a label to display the image
image_label = tk.Label(window, image=tk_image)
image_label.pack()
image_label.place(relx=0.5, rely=0.5, anchor="center")

# Bind the right arrow key press event to the function
window.bind("<Right>", show_next_image)
window.bind("<Left>", show_last_image)

# Start the main event loop
window.mainloop()
