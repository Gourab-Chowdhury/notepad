from tkinter import *
from pymongo import MongoClient
from datetime import datetime
window = Tk()
window.title("Notepad")
# window.geometry("512x512")


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

# Add textarea
TextArea = Text(window, font="luicda 13")
TextArea.pack()

# Button for add notes
b1 = Button(window, text = "Add", 
            command=add_note
            )
b1.pack()
# side="left"

# Button for View Notes
b2 = Button(window, text = "View", 
            command=view_notes
            )
b2.pack()

# Button for Delete Notes
b3 = Button(window, text = "Clear Notes", 
            command=delete_note
            )
b3.pack()

# Create an Exit button.
b4 = Button(window, text = "Delete",
            command = window.destroy)
b4.pack()


# Listbox to display notes
note_listbox = Listbox(window, width=50)
note_listbox.pack()

window.mainloop()
