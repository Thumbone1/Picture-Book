try:

    
    import os
    import tkinter as tk
    from PIL import Image, ImageTk

    # set working directory
    def set_working_directory():
        # Get the directory where the raw Python code is located
        script_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_dir)

    # Call the function to set the working directory before using any file paths
    set_working_directory()
    
    try:
        # Get the path/directory
        folder_name = "pictures"
        #current_dir = os.getcwd()
        folder_dir = "pictures"
        image_list = [image_filename for image_filename in os.listdir(folder_dir) if image_filename.endswith(".jpeg")]

        raw_folder_name = "raw_pictures"
        # current_dir_raw = os.getcwd()
        raw_picture_dir = "raw_pictures"
    except Exception as e:
        with open("B:\errors.txt", "a") as errors:
            errors.write(f"Error: {str(e)}\n")


    def resize_images(source_folder, destination_folder, new_size):
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        if not os.path.exists(source_folder):
            os.makedirs(source_folder)

        # Loop through all files in the source folder
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)

            if os.path.isfile(file_path) and filename.lower().endswith(".avif"):
                os.remove(file_path)
                print(".avif file is unsupported. sorry")

            if os.path.isfile(file_path) and filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")):
                try:
                    # Open the image using Pillow
                    img = Image.open(file_path)

                    # Resize the image
                    img = img.resize(new_size, Image.LANCZOS)

                    # Save the resized image to the destination folder
                    new_file_path = os.path.join(destination_folder, filename)

                    if filename.lower().endswith((".webp", ".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                        # Convert to JPEG before saving if it's in webp, avif, or other supported formats
                        converted_file_path = os.path.splitext(new_file_path)[0] + ".jpeg"
                        img = img.convert("RGB")  # Convert to RGB mode before saving as JPEG
                    else:
                        converted_file_path = new_file_path

                    img.save(converted_file_path)

                    # Delete raw picture after resizing
                    os.remove(file_path)

                    print(f"Resized, saved and removed {file_path}: {converted_file_path}")
                except Exception as e:
                    with open("B:\errors.txt", "a") as errors:
                        errors.write(f"Error: {str(e)}\n")

    #resize any images in the raw_images folder if there are any and add them to pictures
    resize_images(raw_picture_dir, folder_dir, (600, 600))
            
    # Initialize tkinter
    root = tk.Tk()
    root.title("Image Viewer")
    root.geometry("1920x1080")
    root.configure(background="#A6A6A6")

    # Load the first image
    current_image_index = 0
    current_image_path = os.path.join(folder_dir, image_list[current_image_index])
    current_image = Image.open(current_image_path)
    tk_image = ImageTk.PhotoImage(current_image)

    # Create a label to display the image
    image_label = tk.Label(root, image=tk_image)
    image_label.pack()
    image_label.place(relx=0.5, rely=0.5, anchor="center")

    def show_next_image(event):
        global current_image_index, current_image, tk_image

        # Update the current image index
        current_image_index = (current_image_index + 1) % len(image_list)

        # Load the next image
        current_image_path = os.path.join(folder_dir, image_list[current_image_index])
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
        current_image_path = os.path.join(folder_dir, image_list[current_image_index])
        current_image = Image.open(current_image_path)
        tk_image = ImageTk.PhotoImage(current_image)

        # Update the image on the label
        image_label.configure(image=tk_image)
        image_label.image = tk_image
        image_label.place(relx=0.5, rely=0.5, anchor="center")

    # Bind the right arrow key press event to the function
    root.bind("<Right>", show_next_image)
    root.bind("<Left>", show_last_image)

    # Start the main event loop
    root.mainloop()

except Exception as e:
    with open("B:\errors.txt", "a") as errors:
        errors.write(f"Error: {str(e)}\n")