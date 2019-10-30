import logging
from threading import Thread

import PySimpleGUI as sg

import utils
from constants import Constants
from install import nightly_steps, compile_steps_win

# TODO make dynamic
log = logging.getLogger("install.py")


class InstallStep:
    def __init__(self, description: str, desc_key, execute_func):
        self.execute = execute_func
        self.description = description
        self.desc_key = desc_key

    def run(self, constants: Constants, settings: {}, window: sg.Window):
        thread = Thread(target=self.execute, args=(constants, settings))
        thread.start()
        while thread.is_alive():
            window.read(1)
        thread.join()


class Installer:
    def __init__(self, steps: [InstallStep], finalize_func: callable = None):
        self.steps = steps
        self.finalize = finalize_func

    def run(self, constants: Constants, settings: {}):
        label = sg.Text("")
        progress_bar = sg.ProgressBar(len(self.steps), "h")
        layout = [
            [label],
            [progress_bar]
        ]
        window = sg.Window("Installing").Layout(layout)
        window.Read(timeout=0)

        try:
            i = 0
            for step in self.steps:
                progress_bar.update_bar(i)
                label.update(value=step.description)
                step.run(constants, settings, window)
                i += 1
        except Exception as e:
            utils.exception_popup(e)
            window.Close()
            return

        window.Close()
        if self.finalize:
            self.finalize(constants, settings)


def install_nightly(constants: Constants):
    settings = nightly_steps.prepare(constants)
    if not settings:  # Aborted
        return
    settings["type"] = "nightly-%s-%s" % (constants.os, "git" if settings["git"] else "nogit")
    steps = [
        InstallStep("Setting up workspace", "1", nightly_steps.setup_workspace),
        InstallStep("Cloning" if settings["git"] else "Downloading Master", "2", nightly_steps.download_resources),
        InstallStep("Downloading required libraries", "3", nightly_steps.download_libraries),
        InstallStep("Downloading Nightly", "4", nightly_steps.download_nightly)
    ]
    Installer(steps).run(constants, settings)


def compile_win(constants: Constants):
    settings = compile_steps_win.prepare(constants)
    if not settings:  # Aborted
        return
    settings["type"] = "source-%s" % constants.os
    steps = [
        InstallStep("Cloning", "1", compile_steps_win.cloning),
        InstallStep("Downloading MinGW-w64", "2", compile_steps_win.download_compiler),
        InstallStep("Downloading development libraries", "3", compile_steps_win.download_libs),
        InstallStep("Creating Buildscript", "4", compile_steps_win.create_buildscript)
    ]
    Installer(steps, compile_steps_win.offer_compilation).run(constants, settings)
