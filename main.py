import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
import markdown2

class AdvancedNotepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Notepad")
        self.geometry("800x600")
        self.iconbitmap("notepad.ico")  # "notepad.ico" is in the same folder
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=tk.BOTH, expand=1)
        self.autosave_interval = 5000  # Autosave every 5 seconds
        self.theme = "light"  # Default theme
        self.current_files = {}  # Track file paths in tabs
        self.text_font = font.Font(family="Arial", size=12)  # Default font

        self.create_menu()
        self.create_tab()
        self.start_autosave()
    
    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New File", command=self.create_tab)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As txt", command=self.save_as_txt)
        file_menu.add_command(label="Save as PDF", command=self.save_as_pdf)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: self.get_current_text().edit_undo())
        edit_menu.add_command(label="Redo", command=lambda: self.get_current_text().edit_redo())
        edit_menu.add_command(label="Copy", command=lambda: self.get_current_text().event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.get_current_text().event_generate("<<Paste>>"))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Dark Mode", command=self.toggle_theme)
        view_menu.add_command(label="Focus Mode", command=self.toggle_focus_mode)
        view_menu.add_command(label="Markdown Preview", command=self.markdown_preview)
        menu_bar.add_cascade(label="View", menu=view_menu)


    def create_tab(self, title="Untitled"):
        new_tab = tk.Frame(self.tabs)
        text_area = tk.Text(new_tab, wrap="word", undo=True, font=self.text_font)
        text_area.pack(fill=tk.BOTH, expand=1)
        text_area.bind("<KeyRelease>", lambda e: self.syntax_highlighting(text_area))
        self.tabs.add(new_tab, text=title)
        self.tabs.select(new_tab)
        self.current_files[new_tab] = None
    
    def get_current_text(self):
        return self.tabs.nametowidget(self.tabs.select()).winfo_children()[0]
    
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.create_tab(title=os.path.basename(file_path))
            text_area = self.get_current_text()
            text_area.insert(tk.END, content)
            self.current_files[self.tabs.select()] = file_path
    
    def save_file(self):
        current_tab = self.tabs.select()
        file_path = self.current_files[current_tab]
        if file_path:
            with open(file_path, "w") as file:
                content = self.get_current_text().get("1.0", tk.END)
                file.write(content)
        else:
            self.save_as_txt()
    
    def save_as_txt(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                content = self.get_current_text().get("1.0", tk.END)
                file.write(content)
            self.tabs.tab(self.tabs.select(), text=os.path.basename(file_path))
            self.current_files[self.tabs.select()] = file_path

    def save_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if file_path:
            text_content = self.get_current_text().get("1.0", tk.END)
            c = canvas.Canvas(file_path, pagesize=letter)
            text = c.beginText(40, 750)
            text.setFont("Helvetica", 12)
            text.textLines(text_content)
            c.drawText(text)
            c.save()

    def autosave(self):
        for tab, path in self.current_files.items():
            if path:
                with open(path, "w") as file:
                    content = tab.winfo_children()[0].get("1.0", tk.END)
                    file.write(content)
        self.after(self.autosave_interval, self.autosave)

    def start_autosave(self):
        self.after(self.autosave_interval, self.autosave)
    
    def syntax_highlighting(self, text_widget):
        text = text_widget.get("1.0", tk.END)
        for tag in text_widget.tag_names():
            text_widget.tag_delete(tag)
        for token, content in lex(text, PythonLexer()):
            if token in Token.Literal.String:
                text_widget.tag_configure("string", foreground="green")
                text_widget.tag_add("string", "1.0", tk.END)
    
    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.config(bg="black")
            for tab in self.tabs.tabs():
                text_widget = self.tabs.nametowidget(tab).winfo_children()[0]
                text_widget.config(bg="black", fg="white", insertbackground="white")
        else:
            self.theme = "light"
            self.config(bg="white")
            for tab in self.tabs.tabs():
                text_widget = self.tabs.nametowidget(tab).winfo_children()[0]
                text_widget.config(bg="white", fg="black", insertbackground="black")
    
    def toggle_focus_mode(self):
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)
        else:
            self.attributes("-fullscreen", True)
    
    def markdown_preview(self):
        content = self.get_current_text().get("1.0", tk.END)
        html_content = markdown2.markdown(content)
        preview_window = tk.Toplevel(self)
        preview_window.title("Markdown Preview")
        preview_area = tk.Text(preview_window, wrap="word")
        preview_area.insert("1.0", html_content)
        preview_area.pack(fill=tk.BOTH, expand=True)
    
if __name__ == "__main__":
    app = AdvancedNotepad()
    app.mainloop()