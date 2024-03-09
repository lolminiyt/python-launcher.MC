from tkinter import ttk
import customtkinter as ctk
import minecraft_launcher_lib
import os
import os
import subprocess
import sys
import uuid
import threading
from CTkScrollableDropdown import *
MC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
GAME_DIR = r"./.minecraft"
ASSETS_DIR = r"./assets"
NATIVES_DIR = r"./natives"
JAVA_HOME = r"./runtime/java11/"
minecraft_directory = r"./.Minecraft"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.title("Minecraft Launcher")
root.geometry("275x150")
root.maxsize(width=275, height=150)
root.resizable(width=False, height=False)

versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
version_list = [version["id"] for version in versions if version["type"] == "release"]

def CTL(root, text, x, y):
    label = ctk.CTkLabel(root, text=text)
    label.place(x=x, y=y)
 
    textbox = ctk.CTkTextbox(root, width=165, height=10, corner_radius=0)
    textbox.place(x=x + 75, y=y)  
    return label, textbox
 
def CTB(root, text, x, y, values):
    label = ctk.CTkLabel(root, text=text)
    label.place(x=x, y=y)
    
 
    combobox = ctk.CTkComboBox(root, values=values, corner_radius=0)
    combobox.place(x=x + 75, y=y) 
    CTkScrollableDropdown(combobox, values=values, justify="left", button_color="transparent", corner_radius=1)
    return label, combobox

strfram= ctk.StringVar()

uuid_dict = {} 

def generate_uuid(username: str, uuid_dict: dict) -> str:
    if username in uuid_dict:
        return uuid_dict[username]

    new_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, username)
    uuid_dict[username] = new_uuid  
    return new_uuid

def Download_Play():
    username = username_textbox.get('1.0', 'end').strip() 
    version = version_combobox.get() 
    install_thread = threading.Thread(target=minecraft_launcher_lib.install.install_minecraft_version, args=(version, minecraft_directory))
    install_thread.start()
    install_thread.join()
    uuid = generate_uuid(username, uuid_dict)
    print(uuid)
    options = {
        "username": username,
        "uuid": str(uuid),  
        "token": "T",
    }   
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
 
    subprocess.call(minecraft_command)
 
    sys.exit(0)
  

label, username_textbox = CTL(root, "Username:", 20, 12)
label, version_combobox = CTB(root, "Version:", 20, 47, version_list)
rectangle_frame = ctk.CTkFrame(root, width=290, height=60, fg_color="#383838", corner_radius=0)
rectangle_frame.place(x=0, y=89)
Play = ctk.CTkButton(root, text="Jugar", width=195 , corner_radius=0, border_color="#565B5E", fg_color="#333333", border_width=2, command=Download_Play)
Play.place(x=16, y=105)
Settings = ctk.CTkButton(root, text="S", width=25 , corner_radius=0, border_color="#565B5E", fg_color="#333333", border_width=2)
Settings.place(x=228, y=105)
root.toplevel_window = None
root.mainloop()