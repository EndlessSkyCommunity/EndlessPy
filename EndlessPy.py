import PySimpleGUI as sg
import logging
from install import install
from constants import Constants
import utils

logging.basicConfig(level="INFO")
log = logging.getLogger("EndlessPy.py")

sg.SetOptions(button_color=("#dfdfdf", "#202020"),
              border_width="1",
              progress_meter_color=("#9f9f9f", "#181818"),
              progress_meter_size=(15, 20),
              progress_meter_relief="groove",
              background_color="#202020",
              element_background_color="#202020",
              text_element_background_color="#202020",
              input_elements_background_color="#393939",
              element_text_color="#dfdfdf",
              text_color="#dfdfdf")

constants = Constants()

layout = [
    [sg.Button("Play Endless Sky")],
    [sg.Button("Manage Plug-Ins")],
    [sg.Button("Install Nightly")],
    [sg.Button("Install from Source")],
    [sg.Button("Manage Installations")]
]

window = sg.Window("EndlessPy").Layout(layout)

while True:
    event, value = window.Read()
    if event is None or event == "Exit":
        break
    window.Hide()

    try:
        if event == "Install Nightly":
            install.install_nightly(constants)
        if event == "Install from Source":
            install.compile_win(constants)
    except Exception as e:
        utils.exception_popup(e)
    window.UnHide()
window.Close()