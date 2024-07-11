import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import zipfile
import os
import shutil

def check_for_update(current_version):
    user = "your_github_username"
    repo = "your_repository_name"
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    
    try:
        response = requests.get(url)
        data = response.json()
        latest_version = data['tag_name']
        download_url = data['assets'][0]['browser_download_url']
        
        if current_version < latest_version:
            answer = messagebox.askyesno(
                "Update Available",
                f"Version {latest_version} is available. Do you want to update now?"
            )
            if answer:
                download_and_extract_update(download_url)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check for updates: {str(e)}")

def download_and_extract_update(download_url):
    try:
        response = requests.get(download_url)
        zip_filename = 'update.zip'
        
        with open(zip_filename, 'wb') as zip_file:
            zip_file.write(response.content)
        
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(os.path.abspath(__file__)))
        
        os.remove(zip_filename)
        messagebox.showinfo("Success", "Update installed successfully. Please restart the application.")
        root.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download and install update: {str(e)}")

def download_and_extract_mods(url, mods_folder):
    try:
        response = requests.get(url)
        zip_filename = 'mods.zip'
        
        with open(zip_filename, 'wb') as zip_file:
            zip_file.write(response.content)
        
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(mods_folder)
        
        os.remove(zip_filename)
        
        messagebox.showinfo("Success", f"Mods have been downloaded and installed in {mods_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def start_download():
    url = url_entry.get()
    mods_folder = folder_entry.get()
    
    if not url or not mods_folder:
        messagebox.showerror("Error", "Please fill in both fields.")
        return
    
    download_and_extract_mods(url, mods_folder)

# Create the main window
root = tk.Tk()
root.title("Minecraft Mod Downloader")
root.geometry("400x200")

# URL input
url_label = tk.Label(root, text="Direct Download URL:")
url_label.pack(pady=(10, 0))
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Folder selection
folder_label = tk.Label(root, text="Mods Folder:")
folder_label.pack(pady=(10, 0))
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(side=tk.LEFT, padx=(10, 0))
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT, padx=(5, 10))

# Download button
download_button = tk.Button(root, text="Download Mods", command=start_download)
download_button.pack(pady=20)

# Check for updates at startup
current_version = "v1.0.0"  # Replace with your current version
check_for_update(current_version)

root.mainloop()
