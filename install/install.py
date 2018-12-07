import PySimpleGUI as sg
import logging
import os
import utils
import shutil

log = logging.getLogger("install.py")

def prepare_nightly_installation(constants):
    layout = [
        [sg.Text("Name:"), sg.Input(key="name")],
        [sg.Text("Select Install Directory")],
        [sg.Input(key="installdir"), sg.FolderBrowse("Browse")],
        [sg.Text("Using Git is recommended, but it may slow down the installation process.")],
        [sg.Checkbox("Use Git", default=True, key="git")],
        [sg.Text("Advanced Options - Only use if you know what you're doing")],
        [sg.Text("Git Repository"), sg.Input(constants.es_git, key="es_git")],
        [sg.Text("Endless Sky archive"), sg.Input(constants.es_master_zip, key="es_master_zip")],
        [sg.Text("Windows Runtime Libraries"), sg.Input(constants.win64_libs, key="win64_libs")],
        [sg.Text("OSX Nightly Download Page"), sg.Input(constants.nightly_osx_page, key="nightly_osx_page")],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window("Install Nightly").Layout(layout)

    while True:
        event, values = window.Read()
        if event is None or event == "Exit" or event == "Cancel":
            window.Close()
            break
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
                window.Close()
                return values

def install_nightly(constants):
    settings = prepare_nightly_installation(constants)

    layout = [
        [sg.Text("Setting up workspace", key="step1")],
        [sg.Text("Cloning" if settings["git"] else "Downloading Master", key="step2")]
    ]

    window = sg.Window("Installing").Layout(layout)
    window.Read(timeout=0)

    step1 = window.FindElement("step1")
    step2 = window.FindElement("step2")

    if constants.os == "osx":
        resourcedir = os.path.join(settings["installdir"], "Resources")
        libdir = os.path.join(settings["installdir"], "Frameworks")
        bindir = os.path.join(settings["installdir"], "MacOS")
        os.mkdir(resourcedir)
        os.mkdir(libdir)
        os.mkdir(bindir)
    else:
        resourcedir = settings["installdir"]
        libdir = settings["installdir"]
        bindir = settings["installdir"]

    step1.Update(value= u"\u2713" + " " + step1.DisplayText)

    if settings["git"]:
        utils.clone(settings["es_git"], resourcedir)
    else:
        archive = os.path.join(resourcedir, "master.zip")
        utils.download_file(settings["es_master_zip"], archive, 89800000)

        utils.extract(archive, resourcedir)

        temppath = os.path.join(resourcedir, "endless-sky-master")
        for file in os.listdir(temppath):
            shutil.move(os.path.join(temppath, file), os.path.join(resourcedir, file))
        shutil.rmtree(os.path.join(temppath))
