import PySimpleGUI as sg
import logging
from install import nightly_steps, compile_steps_win
import traceback
import sys
import utils
from installations import Installation

log = logging.getLogger("install.py")


class Installer:
    def __init__(self, steps, finalize_func=None):
        self.steps = steps
        self.finalize = finalize_func

    def run(self, constants, settings):
        layout = [[sg.Text(step.description, key=step.desc_key)] for step in self.steps]
        window = sg.Window("Installing").Layout(layout)
        window.Read(timeout=0)

        try:
            [step.run(constants, settings, window) for step in self.steps]
        except Exception as e:
            utils.exception_popup(e)
            window.Close()
            return

        constants.add_installation(Installation(**settings))

        window.Close()
        if self.finalize:
            self.finalize(constants, settings)


class InstallStep:
    def __init__(self, description, desc_key, execute_func):
        self.execute = execute_func
        self.description = description
        self.desc_key = desc_key

    def run(self, constants, settings, window):
        window.FindElement(self.desc_key).Update(value=u"\u27F3" + " " + self.description)
        self.execute(constants, settings)
        self._finalize(window)

    def _finalize(self, window):
        window.FindElement(self.desc_key).Update(value=u"\u2713" + " " + self.description)


def install_nightly(constants):
    settings = nightly_steps.prepare(constants)
    if not settings: # Aborted
        return
    settings["type"] = "nightly-%s-%s" % (constants.os, "git" if settings["git"] else "nogit")
    steps = [
        InstallStep("Setting up workspace", "1", nightly_steps.setup_workspace),
        InstallStep("Cloning" if settings["git"] else "Downloading Master", "2", nightly_steps.download_resources),
        InstallStep("Downloading required libraries", "3", nightly_steps.download_libraries),
        InstallStep("Downloading Nightly", "4", nightly_steps.download_nightly)
    ]
    Installer(steps).run(constants, settings)


def compile_win(constants):
    settings = compile_steps_win.prepare(constants)
    if not settings: # Aborted
        return
    settings["type"] = "source-%s" % constants.os
    steps = [
        InstallStep("Cloning", "1", compile_steps_win.cloning),
        InstallStep("Downloading MinGW-w64", "2", compile_steps_win.download_compiler),
        InstallStep("Downloading development libraries", "3", compile_steps_win.download_libs),
        InstallStep("Creating Buildscript", "4", compile_steps_win.create_buildscript)
    ]
    Installer(steps, compile_steps_win.offer_compilation).run(constants, settings)
