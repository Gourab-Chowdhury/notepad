from tkinter import *
from pymongo import MongoClient
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog
import io
import os


window = Tk()
window.title("Notepad")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["note_app"]
notes_collection = db["notes"]

# Add a Note
def add_note():

    task = TextArea.get("1.0", END)  # Get text from the TextArea widget
    # task = TextArea.get()
    # priority = priority_entry.get()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # saveimg = save_image_to_mongodb
    # save_img =saveimg.get()

    note = {"task": task, "date": date}
    result = notes_collection.insert_one(note)

    update_notes()
    clear_text()

# View notes in the ListBox
def view_notes():
    notes = notes_collection.find()
    note_listbox.delete(0, END)
    for note in notes:
        note_listbox.insert(END, f"{note['task']} - Date: {note['date']}")

# Delete a note
def delete_note():
    selected_task = note_listbox.get(note_listbox.curselection())
    task_to_delete = selected_task.split(" - ")[0]
    
    result = notes_collection.delete_one({"task": task_to_delete})
    if result.deleted_count > 0:
        update_notes()

def clear_text():
    TextArea.delete(0, END)

def update_notes():
    view_notes()
    clear_text()

# Global variables for image and zoom level
current_image = None
img_label = None
zoom_level = 1

# Function to open image
def open_image():
    global current_image, img_label, zoom_level, current_image_file_name
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        # Open and display the image
        current_image = Image.open(file_path)
        zoom_level = 1  # Reset zoom level
        
        display_image(current_image)
        current_image_file_name = os.path.basename(file_path)  # Get the file name

        # Save image to MongoDB
        # save_image_to_mongodb(file_path, current_image)

def display_image(img):
    global img_label
    # Resize image for display based on zoom level
    img_resized = img.resize((int(img.width * zoom_level), int(img.height * zoom_level)), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    if img_label:
        img_label.config(image=img_tk)
        img_label.image = img_tk
    else:
        img_label = Label(window, image=img_tk)
        img_label.image = img_tk
        img_label.pack()

def save_img_to_mongodb():
    # text_data = TextArea.get("1.0", END).strip()      
    if current_image:
        img_byte_arr = io.BytesIO()
        current_image.save(img_byte_arr, format=current_image.format)
        img_binary = img_byte_arr.getvalue()
    else:
        img_binary = None

    note_data = {
        # 'text': text_data,
        'image_file_name': current_image_file_name,
        'image': img_binary
    }
    notes_collection.insert_one(note_data)
    print("Note saved to MongoDB.")



# Zoom in and out functions
def zoom_in(event):
    global zoom_level
    zoom_level *= 1.1  # Increase zoom level by 10%
    display_image(current_image)

def zoom_out(event):
    global zoom_level
    zoom_level /= 1.1  # Decrease zoom level by 10%
    display_image(current_image)

# Bind mouse wheel to zoom functions
window.bind("<Control-MouseWheel>", lambda 
            event: zoom_in(event) if event.delta > 0 else zoom_out(event))


# Add textarea
TextArea = Text(window, font="luicda 13", width=50, height=10)
TextArea.pack()

# Menu bar
menu = Menu(window)
window.config(menu=menu)

# Menu for Addind notes and Images 
save_menu = Menu(menu)
menu.add_cascade(label="Save", menu=save_menu)
save_menu.add_command(label="Save Note", command=add_note)
save_menu.add_separator()
save_menu.add_command(label="Save Image", command=save_img_to_mongodb)

# Menu for Delete notes and Images 
delete_menu = Menu(menu)
menu.add_cascade(label="Delete", menu=delete_menu)
delete_menu.add_command(label="Delete", command=delete_note)
delete_menu.add_separator()
# delete_menu.add_command(label="Delete Image", command=)

# Menu for view notes and Images 
view_menu = Menu(menu)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="View notes", command=view_notes)
view_menu.add_separator()
view_menu.add_command(label="Display Image", command=display_image)


# Menu for Open Images 
openImg_menu = Menu(menu)
menu.add_cascade(label="Open Image", menu=openImg_menu)
openImg_menu.add_command(label="Open Image", command=open_image)
# openImg_menu.add_separator()
# openImg_menu.add_command(label="Save Image", command=save_image_to_mongodb)

# Create an Exit button.
# Close_window = Button(window, text = "Close", command = window.destroy)
# Close_window.pack()

# Listbox to display notes
note_listbox = Listbox(window, width=50)
note_listbox.pack()

window.mainloop()
