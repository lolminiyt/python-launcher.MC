import keyboard
from tkinter import Tk, Label, Entry, Button, mainloop
from tkinter.ttk import Combobox
from tkinter import *
import os
import subprocess
import requests
import time
import sys
MC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
GAME_DIR = r"./.minecraft"
ASSETS_DIR = r"./assets"
NATIVES_DIR = r"./natives"
JAVA_HOME = r"./runtime/java11/"
import minecraft_launcher_lib
cwd = os.getcwd()
import shutil

current_max = 0


def set_status(status: str):
    print(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")


def set_max(new_max: int):
    global current_max
    current_max = new_max

minecraft_directory = r"./"

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

print("Launcher para minecraft 1.16.5/1.19.2 portable, optimizado y creado en python")

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
            "token": "T"
         }   
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version_select.get(), minecraft_directory, options)

        subprocess.call(minecraft_command)

        sys.exit(0)

    def fabric(): 
            os.chdir(os.path.join(MC_DIR, GAME_DIR))
            url = 'https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar'
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                # Guarda el archivo en el directorio GAME_DIR
                with open('fabric-installer.jar', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                subprocess.call(['java', '-jar', 'fabric-installer.jar', 'client', '-dir',  "./", '-mcversion', version_select.get(), '-noprofile'])
                print(os.getcwd())
            else:
                print("Error al descargar el archivo de la URL")

    def forge():
        os.chdir(os.path.join(MC_DIR))
        forge_version = minecraft_launcher_lib.forge.find_forge_version(version_select.get())
        if forge_version is None:
            print("This Minecraft Version is not supported by Forge")
            return
        print(os.getcwd())
        minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory)

    window = Tk()
    window.title("Minecraft Launcher")
    window.resizable(width=False, height=False)

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

    Button(window, text="Launch", command=launch).grid(row=5, column=1)
    print(generate_uuid)

    Button(window, text="Install Fabric ", command=fabric).grid(row=5, column=0)

    Button(window, text="Install Forge ", command=forge).grid(row=5, column=2)

    mainloop()


if __name__ == "__main__":
    main()
