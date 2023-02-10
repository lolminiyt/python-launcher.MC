import keyboard
from tkinter import Tk, Label, Entry, Button, mainloop
from tkinter.ttk import Combobox
from tkinter import *
import os
import subprocess
import requests
import time
import sys
MC_DIR = os.getcwd()
GAME_DIR = MC_DIR
ASSETS_DIR = r"./assets"
NATIVES_DIR = r"./natives"
JAVA_HOME = r"./runtime/java11/"
import minecraft_launcher_lib

current_max = 0


def set_status(status: str):
    print(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")


def set_max(new_max: int):
    global current_max
    current_max = new_max

minecraft_directory = r"./data/minecraft_launcher_lib"

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

print("Launcher para minecraft 1.16.5/1.19.2 portable, optimizado y creado en python")

def main():
    def launch():
        window.withdraw()
        minecraft_launcher_lib.install.install_minecraft_version(version_select.get(), minecraft_directory, callback=callback)

        options = {
            "username": str(strfname.get()),
            "uuid": str(uuid.get()),
            "token": "T"
         }   
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version_select.get(), minecraft_directory, options)

        subprocess.call(minecraft_command)

        sys.exit(0)

    def fabric(): 
        minecraft_launcher_lib.fabric.install_fabric(version_select.get(), minecraft_directory, callback=callback)

    def forge():
        forge_version = minecraft_launcher_lib.forge.find_forge_version(version_select.get())
        if forge_version is None:
            print("This Minecraft Version is not supported by Forge")
            return
        minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory, callback=callback)

    window = Tk()
    window.title("Minecraft Launcher")

    versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
    version_list = []

    for i in versions:
        version_list.append(i["id"])

    strfname = StringVar()
    uuid = StringVar()

    Label(window, text="Version:").grid(row=3, column=0)
    version_select = Combobox(window, values=version_list)
    version_select.grid(row=3, column=1)
    version_select.current(0)

    labelf = Label(window, text = 'Username').grid(row=1, column=0)
    fname = Entry(window, justify='left', textvariable = strfname).grid(row=1, column=1) #strlname get input 

    Label(window, text="UUID:").grid(row=2, column=0)
    luuid = Entry(window, justify='left', textvariable = uuid).grid(row=2, column=1) #strlname get input 

    Button(window, text="Launch", command=launch).grid(row=5, column=1)

    Button(window, text="Install Fabric ", command=fabric).grid(row=5, column=0)

    Button(window, text="Install Forge", command=forge).grid(row=5, column=2)

    mainloop()


if __name__ == "__main__":
    main()
