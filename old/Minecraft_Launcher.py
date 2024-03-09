## bufixes -  el launcher crasheaba si no se tenia una carpeta .minecraft - fabric installer no usaba el java incluido, usaba el java asignado a la pc
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
import customtkinter
import configparser
###########################################################################
config_file = configparser.ConfigParser()
config_file.add_section("Launcher_Settings")
config_file.set("Launcher_Settings", "Mostrar Solo Versiones Instaladas", "Si")
config_file.set("Launcher_Settings", "Mostrar Snapshots", "No")
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()
###########################################################################

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

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
            "token": "T",
            "jvmArguments": strfram.get()
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

    window = Tk()
    window.title("Minecraft Launcher")
    window.resizable(width=False, height=False)



    versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
    version_list = []

    for i in versions:
        version_list.append(i["id"])

    strfname = StringVar()
    uuid = StringVar()
    strfram= StringVar()

    font_style = ("Helvetica", 10)

    Label(window, text="Version:",font=font_style).grid(row=3, column=0)
    version_select = Combobox(window, values=version_list, width=25)
    version_select.grid(row=3, column=1)
    version_select.current(0)

    labeld = Label(window, text = 'Username',font=font_style).grid(row=1, column=0)
    dname = Entry(window, justify='left', textvariable = strfname).grid(row=1, column=1) #strlname get input 

    Button(window, text="Launch", command=launch,font=font_style).grid(row=5, column=1)
    print(generate_uuid)

    Button(window, text="Install Fabric ", command=fabric,font=font_style).grid(row=5, column=0)

    Button(window, text="Install Forge ", command=forge,font=font_style).grid(row=5, column=2)

    mainloop()


if __name__ == "__main__":
    main()
