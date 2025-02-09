import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def select_file():
    initial_dir = os.path.join(os.getcwd(), 'client')
    if not os.path.exists(initial_dir):
        initial_dir = os.getcwd()
        
    filename = filedialog.askopenfilename(
        title="Select Python file",
        initialdir=initial_dir,
        filetypes=[("Python files", "*.py")]
    )
    
    try:
        rel_path = os.path.relpath(filename, os.getcwd())
        file_entry.delete(0, tk.END)
        file_entry.insert(0, rel_path)
    except ValueError:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

def select_icon():
    filename = filedialog.askopenfilename(
        title="Select Icon",
        filetypes=[("Icon files", "*.ico")]
    )
    
    try:
        rel_path = os.path.relpath(filename, os.getcwd())
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, rel_path)
    except ValueError:
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, filename)

def compile_script():
    python_file = file_entry.get()
    icon_file = icon_entry.get()
    
    if not python_file:
        messagebox.showerror("Error", "Please select a Python file")
        return
        
    python_file = os.path.abspath(python_file)
    if icon_file:
        icon_file = os.path.abspath(icon_file)
        
    command = ["pyinstaller", "--noconfirm", "--onefile", "--windowed"]
    
    if icon_file:
        command.extend(["--icon", icon_file])
    
    command.append(python_file)
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Success", "Compilation completed successfully!")
        else:
            messagebox.showerror("Error", f"Error while compiling:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

root = tk.Tk()
root.title("Python to EXE Compiler")
root.geometry("600x400")
root.configure(padx=20, pady=20)

file_frame = tk.LabelFrame(root, text="Python File", padx=10, pady=10)
file_frame.pack(fill="x", padx=5, pady=5)

file_entry = tk.Entry(file_frame)
file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

file_button = tk.Button(file_frame, text="Browse", command=select_file)
file_button.pack(side="right")

icon_frame = tk.LabelFrame(root, text="Icon (optional)", padx=10, pady=10)
icon_frame.pack(fill="x", padx=5, pady=5)

icon_entry = tk.Entry(icon_frame)
icon_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

icon_button = tk.Button(icon_frame, text="Browse", command=select_icon)
icon_button.pack(side="right")

compile_button = tk.Button(root, text="Compile", command=compile_script, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), pady=10)
compile_button.pack(pady=20)

root.mainloop()