# Advanced Notepad

## Description
**Advanced Notepad** is a modern and feature-rich text editor designed for developers, writers, and anyone looking for an efficient way to manage text. Built with Python's Tkinter library, this application supports multi-tabbed editing, syntax highlighting, Markdown preview, PDF export, and much more.

---

## Features
### Core Features:
- **Tabbed Interface**: Work on multiple files simultaneously.
- **File Management**:
  - Create, open, save, and export files as `.txt` or `.pdf`.
- **Editing Options**:
  - Undo, redo, copy, and paste support.
- **Autosave**: Prevent data loss by automatically saving files every 5 seconds.

### Additional Features:
- **Dark Mode**: Reduce eye strain with an optional dark theme.
- **Focus Mode**: Write without distractions in fullscreen mode.
- **Markdown Preview**: Render Markdown content in a pop-up window for easy preview.

### Developer Tools:
- **Syntax Highlighting**: Highlight Python code in real time.

---

## Requirements
To run **Advanced Notepad**, you need the following:
- Python 3.x installed on your machine.
- Required Python packages:
  - `tkinter` (pre-installed with Python).
  - `reportlab` (for PDF export).
  - `pygments` (for syntax highlighting).
  - `markdown2` (for Markdown rendering).

Install Dependences
```
pip install reportlab pygments markdown2
```
---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/advanced-notepad.git
   ```


# Usage
## Menu Options:

### File:
* New File: Create a new blank tab.
* Open File: Load a .txt file into a tab.
* Save: Save changes to the current file.
* Save As txt: Save the current content as a new .txt file.
* Save as PDF: Export the current content to a .pdf file.

### Edit:
* Undo, Redo, Copy, Paste: Standard editing tools.

### View:
* Toggle between Dark Mode and Light Mode.
* Enable/disable Focus Mode for fullscreen writing.
* Preview Markdown content in a pop-up window.   
