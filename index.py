import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ttkbootstrap as tb

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.style = tb.Style()
        self.style.theme_use('darkly')
        
        self.folder_path = tk.StringVar()
        self.search_var = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        frame = tb.Frame(self.root, padding=10)
        frame.pack(fill='x')
        
        tb.Label(frame, text="Select Folder:").pack(side='left', padx=5)
        tb.Entry(frame, textvariable=self.folder_path, width=40).pack(side='left', padx=5)
        tb.Button(frame, text="Browse", command=self.browse_folder).pack(side='left', padx=5)
        
        tb.Label(self.root, text="Search Files:").pack(pady=5)
        search_entry = tb.Entry(self.root, textvariable=self.search_var, width=50)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", self.search_files)
        
        self.file_listbox = tk.Listbox(self.root, height=10, width=80)
        self.file_listbox.pack(pady=10)
        
        tb.Button(self.root, text="Organize Files", command=self.organize_files).pack(pady=5)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.list_files()
    
    def list_files(self):
        self.file_listbox.delete(0, tk.END)
        folder = self.folder_path.get()
        if folder:
            for file in os.listdir(folder):
                self.file_listbox.insert(tk.END, file)
    
    def search_files(self, event=None):
        search_term = self.search_var.get().lower()
        self.file_listbox.delete(0, tk.END)
        folder = self.folder_path.get()
        if folder:
            for file in os.listdir(folder):
                if search_term in file.lower():
                    self.file_listbox.insert(tk.END, file)
    
    def organize_files(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder first")
            return
        
        file_types = {
            'Images': ['.jpg', '.png', '.jpeg', '.gif'],
            'Videos': ['.mp4', '.mov', '.avi'],
            'Documents': ['.pdf', '.docx', '.txt'],
            'Audio': ['.mp3', '.wav']
        }
        
        for category, extensions in file_types.items():
            category_folder = os.path.join(folder, category)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
            
            for file in os.listdir(folder):
                if any(file.endswith(ext) for ext in extensions):
                    shutil.move(os.path.join(folder, file), os.path.join(category_folder, file))
        
        messagebox.showinfo("Success", "Files have been organized!")
        self.list_files()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
