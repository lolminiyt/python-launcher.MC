import keyboard 
from tkinter import Tk, Label, Entry, Button, mainloop
from tkinter.ttk import Combobox
from tkinter import *
import configparser
import os
import subprocess
import requests
from PIL import ImageTk, Image
import time
import tkinter
import customtkinter
import sys
MC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
GAME_DIR = r"./.minecraft"
ASSETS_DIR = r"./assets"
NATIVES_DIR = r"./natives"
JAVA_HOME = r"./runtime/java11/"
import minecraft_launcher_lib

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

import shutil

if not os.path.exists('config.png'):
    url2 = 'https://i.ibb.co/gtKRxXf/free-settings-icon-3110-thumb-2793537920.png'
    r2 = requests.get(url2, stream=True)
    with open('free-settings-icon-3110-thumb-2793537920.png', 'wb') as f:
        shutil.copyfileobj(r2.raw, f)
    try:
        os.rename('free-settings-icon-3110-thumb-2793537920.png', 'config.png')
    except FileExistsError:
        pass

minecraft_directory = r"./"

uuid_dict = {}

def generate_uuid(strfname: str, uuid_dict: dict) -> str:
    url = f"https://www.uuidtools.com/api/generate/v4/count/1"
    response = requests.get(url)
    if response.status_code == 200:
        uuid = response.json()[0]
        uuid_dict[strfname] = uuid  # Almacenar la uuid en el diccionario
        return uuid
    else:
        return ""

def main():
    def launch():
        window.withdraw()
        minecraft_launcher_lib.install.install_minecraft_version(version_select.get(), minecraft_directory)

        options = {
            "username": str(strfname.get()),
            "uuid": str(uuid_dict.get(strfname.get(), "")),  # Obtener la uuid del diccionario
            "token": "T",
         }   
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version_select.get(), minecraft_directory, options)

        subprocess.call(minecraft_command)

        sys.exit(0)

    def fabric(): 
            os.chdir(os.path.join(minecraft_directory))
            url = 'https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar'
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                # Guarda el archivo en el directorio GAME_DIR
                with open('fabric-installer.jar', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                print(os.getcwd())
                os.chdir(os.path.join(MC_DIR))
                print(os.getcwd())
                subprocess.call([r"./runtime/jre-legacy/windows-x64/jre-legacy/bin/java.exe", '-jar', 'fabric-installer.jar', 'client', '-dir',  "./.minecraft", '-mcversion', version_select.get(), '-noprofile'])
            else:
                print("Error al descargar el archivo de la URL")

    def forge():
        os.chdir(os.path.join(minecraft_directory))
        forge_version = minecraft_launcher_lib.forge.find_forge_version(version_select.get())
        if forge_version is None:
            print("This Minecraft Version is not supported by Forge")
            return
        print(os.getcwd())
        minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory)
    
    class ToplevelWindow(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("400x300")
            
            
    def optionmenu_callback(choice):
        print("optionmenu dropdown clicked:", choice)

        combobox = customtkinter.CTkOptionMenu(master=window,
                                       values=["option 1", "option 2"],
                                       command=optionmenu_callback)
        combobox.pack(padx=20, pady=10)
        combobox.set("option 2")  # set initial value

    def open_toplevel():
        toplevel_window = None
        if toplevel_window is None or not toplevel_window.winfo_exists():
            toplevel_window = ToplevelWindow()  # create window if its None or destroyed
        else:
            toplevel_window.focus()  # if window exists focus it

    window = Tk()
    window.title("Manzana")
    window.resizable(width=False, height=False)
    window.geometry("435x85")
    window.configure(background="black")

    versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
    version_list = []

    for version in versions:
        if version["type"] == "release":
            version_list.append(version["id"])

    strfname = StringVar()
    uuid = StringVar()
    strfram= StringVar()

    font_style = ("Helvetica", 10)


    customtkinter.CTkLabel(window, text="Version:").grid(row=3, column=0)
    version_select = customtkinter.CTkComboBox(window, values=version_list, width=155)  
    version_select.grid(row=3, column=1)

    customtkinter.CTkLabel(window, text="Username").grid(row=1, column=0)
    dname = customtkinter.CTkEntry(window, justify='left', textvariable=strfname)
    dname.grid(row=1, column=1)

    customtkinter.CTkButton(window, text="Launch", command=launch).grid(row=5, column=1)
    print(generate_uuid)

    photo = customtkinter.CTkImage(Image.open(r"C:\Users\Thinkpad\Documents\Python\.minecraft\config.png"))
    button = customtkinter.CTkButton(master=window, image=photo, text="", width=2, command=open_toplevel)
    button.place(relx=1, rely=0.15, anchor=tkinter.E)

    customtkinter.CTkButton(window, text="Install Fabric", command=fabric).grid(row=5, column=0)

    customtkinter.CTkButton(window, text="Install Forge", command=forge).grid(row=5, column=2)
    window.mainloop()


if __name__ == "__main__":
    main()
