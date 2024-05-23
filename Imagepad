from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Initialize the main window
window = Tk()
window.title("Notepad")
window.geometry("800x600")

# Global variables for image and zoom level
current_image = None
img_label = None
zoom_level = 1



# Function to open image
def open_image():
    global current_image, img_label, zoom_level
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        # Open and display the image
        current_image = Image.open(file_path)
        zoom_level = 1  # Reset zoom level
        display_image(current_image)

# Function to resize image to fit within 800x600
def resize_to_fit(img, max_width=800, max_height=600):
    width_ratio = max_width / img.width
    height_ratio = max_height / img.height
    resize_ratio = min(width_ratio, height_ratio)
    new_width = int(img.width * resize_ratio)
    new_height = int(img.height * resize_ratio)
    return img.resize((new_width, new_height), Image.LANCZOS)

# Function to display image
def display_image(img):
    global img_label
    # Resize image to fit within 800x600 before applying zoom
    img_resized = resize_to_fit(img)
    img_resized = img_resized.resize((int(img_resized.width * zoom_level), int(img_resized.height * zoom_level)), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    if img_label:
        img_label.config(image=img_tk)
        img_label.image = img_tk
    else:
        img_label = Label(window, image=img_tk)
        img_label.image = img_tk
        img_label.pack()
    canvas.config(scrollregion=canvas.bbox(ALL))

# Zoom in and out functions
def zoom_in(event):
    global zoom_level
    zoom_level *= 1.1  # Increase zoom level by 10%
    display_image(current_image)
    canvas.config(scrollregion=canvas.bbox(ALL))

def zoom_out(event):
    global zoom_level
    zoom_level /= 1.1  # Decrease zoom level by 10%
    display_image(current_image)
    canvas.config(scrollregion=canvas.bbox(ALL))

# Bind mouse wheel to zoom functions
window.bind("<Control-MouseWheel>", lambda event: zoom_in(event) if event.delta > 0 else zoom_out(event))

# Menu bar
menu = Menu(window)
window.config(menu=menu)

# Menu for Open Images
open_img_menu = Menu(menu)
menu.add_cascade(label="Open Image", menu=open_img_menu)
open_img_menu.add_command(label="Open Image", command=open_image)

# Scrollbar
canvas = Canvas(window, bg="white")
img_label = Label(canvas)
img_label.grid(row=0, column=0)

hbar = Scrollbar(window, orient=HORIZONTAL, command=canvas.xview)
hbar.pack(side=BOTTOM, fill=X)
vbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
vbar.pack(side=RIGHT, fill=Y)

canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT, expand=True, fill=BOTH)

canvas.create_window((0, 0), window=img_label, anchor="nw")
                         
# Create an Exit button
# close_window = Button(window, text="Close", command=window.destroy)
# close_window.pack(side=BOTTOM)

window.mainloop()
