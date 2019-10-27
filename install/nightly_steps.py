import os
import shutil
import stat

import PySimpleGUI as sg
import requests

import utils


def prepare(constants):
    layout = [
        [sg.Text("Select Install Directory")],
        [sg.Input(key="installdir"), sg.FolderBrowse("Browse")],
        [sg.Text("Using Git is recommended, but it may slow down the installation process.")],
        [sg.Checkbox("Use Git", default=True, key="git")],
        [sg.Text("Advanced Options - Only use if you know what you're doing")],
        [sg.Text("Git Repository"), sg.InputText(constants.es_git, key="es_git")],
        [sg.Text("Endless Sky archive"), sg.InputText(constants.es_master_zip, key="es_master_zip")],
        [sg.Text("Windows Runtime Libraries"), sg.InputText(constants.win64_libs, key="win64_libs")],
        [sg.Text("Windows Nightly Download"), sg.InputText(constants.nightly_win64, key="nightly_win64")],
        [sg.Text("OSX Nightly Download Page"), sg.InputText(constants.nightly_osx_page, key="nightly_osx_page")],
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
                    window.Close()
                    utils.empty_directory(values["installdir"])
                else:
                    window.Close()
                return values


def setup_workspace(constants, settings):
    if constants.os == "osx":
        settings["resourcedir"] = os.path.join(settings["installdir"], "Resources")
        settings["libdir"] = os.path.join(settings["installdir"], "Frameworks")
        settings["bindir"] = os.path.join(settings["installdir"], "MacOS")
        os.mkdir(settings["resourcedir"])
        os.mkdir(settings["libdir"])
        os.mkdir(settings["libdir"])
    else:
        settings["resourcedir"] = settings["installdir"]
        settings["libdir"] = settings["installdir"]
        settings["bindir"] = settings["installdir"]


def download_resources(constants, settings):
    if settings["git"]:
        utils.clone(settings["es_git"], settings["resourcedir"], None)
    else:
        archive = os.path.join(settings["resourcedir"], "master.zip")
        utils.download_file(settings["es_master_zip"], archive, 89800000)

        utils.extract(archive, settings["resourcedir"])

        temppath = os.path.join(settings["resourcedir"], "endless-sky-master")
        for file in os.listdir(temppath):
            shutil.move(os.path.join(temppath, file), os.path.join(settings["resourcedir"], file))
        shutil.rmtree(os.path.join(temppath))


def download_libraries(constants, settings):
    archive = os.path.join(settings["libdir"], "libraries.zip")
    liburl = settings["win64_libs"] if constants.os == "win64" else settings["osx_libs"]
    utils.download_file(liburl, archive, 0)
    utils.extract(archive, settings["libdir"])


def download_nightly(constants, settings):
    executable = os.path.join(settings["bindir"], "EndlessSky" + (".exe" if constants.os == "win64" else ""))
    if constants.os == "win64":
        nightly_url = settings["nightly_win64"]
        target = executable
    else:
        print("Fetching download URL")
        j = requests.get(settings["nightly_osx_page"]).json()
        nightly_url = j["assets"][0]["browser_download_url"]
        target = executable + ".zip"
    print("Downloading Nightly")
    utils.download_file(nightly_url, target, 0)

    if os == "osx" or True:
        # util.extract(target, bindir)
        st = os.stat(executable)
        os.chmod(executable, st.st_mode | stat.S_IEXEC)
        script = os.path.join(settings["installdir"], "EndlessSky.sh")
        with open(script, "x") as s:
            s.write(os.path.relpath(executable, settings["installdir"]) + " --resources "
                    + os.path.relpath(settings["resourcedir"], settings["installdir"]) + " \"$@\"")
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC)
