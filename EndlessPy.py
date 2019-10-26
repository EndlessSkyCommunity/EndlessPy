import logging

import PySimpleGUI as sg

import colors
import utils
from constants import Constants
from install import install

logging.basicConfig(level="INFO")
log = logging.getLogger("EndlessPy.py")

sg.SetOptions(button_color=(colors.TEXT, colors.BACKGROUND),
              border_width="1",
              progress_meter_color=("#9f9f9f", "#181818"),
              progress_meter_size=(15, 20),
              progress_meter_relief="groove",
              background_color=colors.BACKGROUND,
              element_background_color=colors.BACKGROUND,
              text_element_background_color=colors.BACKGROUND,
              input_elements_background_color=colors.BACKGROUND_LIGHT,
              input_text_color=colors.TEXT_DARKER,
              element_text_color=colors.TEXT,
              text_color=colors.TEXT, )

constants = Constants()

layout = [
    [
        sg.Button("Install Nightly"),
    ],
    [
        sg.Button("Install from Source")
    ]
]

window = sg.Window("EndlessPy").Layout(layout)

while True:
    event, values = window.Read()
    if not event or event == "Exit":
        break
    window.Hide()

    try:
        if event == "Install Nightly":
            install.install_nightly(constants)
        elif event == "Install from Source":
            install.compile_win(constants)

    except Exception as e:
        utils.exception_popup(e)
    window.UnHide()
window.Close()
