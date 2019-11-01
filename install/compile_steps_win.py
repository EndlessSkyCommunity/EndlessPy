import os
import shutil
import subprocess
from multiprocessing import cpu_count

import PySimpleGUI as sg

import utils
from constants import Constants


def prepare(constants: Constants):
    layout = [
        [sg.Text("Select Install Directory")],
        [sg.Input(key="installdir"), sg.FolderBrowse("Browse")],
        [sg.Text("Number of CPU cores to be used for compiling"),
         sg.Spin([i + 1 for i in range(0, cpu_count())], initial_value=cpu_count(), key="cpu_cores")],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window("Install Nightly").Layout(layout)

    while True:
        event, values = window.Read()
        if not event or event == "Exit" or event == "Cancel":
            window.Close()
            return None
        if event == "Ok":
            invalid = {}
            for key, value in values.items():
                if value == "":
                    invalid[key] = value
            if invalid:
                text = "Invalid Inputs:\n"
                for key, value in invalid.items():
                    text += "\n%s - %s" % (key, value)
                sg.Popup(text)
                window.Fill(values)
            else:
                if os.listdir(values["installdir"]):
                    p = sg.PopupYesNo("The selected Directory is not empty. Do you want to delete all files in it?")
                    if p == "No":
                        window.Fill(values)
                        continue
                    utils.empty_directory(values["installdir"])
                window.Close()
                return values


def cloning(constants: Constants, settings: {}, progress: sg.ProgressBar):
    git_dir = utils.install_git(settings["resourcedir"], constants)
    utils.clone(constants.es_git, settings["installdir"], git_dir)


def download_compiler(constants: Constants, settings: {}, progress: sg.ProgressBar):
    archive = os.path.join(settings["installdir"], "mingw-win64.zip")
    utils.download_file(constants.mingw_win64, archive, 140409321)
    utils.extract(archive, settings["installdir"])


def download_libs(constants: Constants, settings: {}, progress: sg.ProgressBar):
    archive = os.path.join(settings["installdir"], "libraries.zip")
    utils.download_file(constants.win64_dev_libs, archive, 2492854)
    utils.extract(archive, settings["installdir"])

    dlldir = os.path.join(settings["installdir"], "dev64", "bin")
    for lib in os.listdir(dlldir):
        shutil.copyfile(os.path.join(dlldir, lib), os.path.join(settings["installdir"], lib))


def create_buildscript(constants: Constants, settings: {}, progress: sg.ProgressBar):
    build_script = r"""
cd /D %%~dp0     &:: Switch to the script's directory, to not mess up relative paths
set CXX=.\mingw64\bin\g++.exe
set LD=.\mingw64\bin\g++.exe
set WINDRES=.\mingw64\bin\windres.exe
set DIR_ESLIB=.\dev64
set DIR_MINGW64=.\mingw64\x86_64-w64-mingw32
.\mingw64\bin\mingw32-make.exe -e -f .winmake -j %s release     &:: Compile
MOVE .\bin\win64\EndlessSky.exe .\EndlessSky.exe
    """.strip() % settings["cpu_cores"]

    with open(os.path.join(settings["installdir"], "build.bat"), "w") as bat:
        bat.write(build_script)


def offer_compilation(constants: Constants, settings: {}, progress: sg.ProgressBar):
    p = sg.PopupYesNo("Do you want me to compile now? (You will have to do it eventually)")
    if p == "No":
        return
    subprocess.run("start \"Compiling...\" \"%s\" & exit" % os.path.join(settings["installdir"], "build.bat"),
                   shell=True)
