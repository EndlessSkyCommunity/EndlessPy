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
              input_text_color="#bfbfbf",
              element_text_color="#dfdfdf",
              text_color="#dfdfdf")

constants = Constants()


def installations_table():
    if not constants.installations:
        return sg.Text("No Installations yet!")

    headings = ["Name", "Directory", "Git", "Type"]
    data = [
        [
            i.name,
            i.installdir,
            bool(i.es_git),
            i.type,
        ] for i in constants.installations]
    return sg.Table(values=data, headings=headings, key="installations_table")


layout = [
    [
    ],
    [
        sg.TabGroup([
            [
                sg.Tab("Installations", key="installations_tab", layout=
                [
                    [
                        sg.Button("Launch Selected"),
                        sg.Button("Remove Selected"),
                        sg.Button("Install Nightly"),
                        sg.Button("Install from Source"),
                        sg.Button("Add Local Installation")
                    ],
                    [installations_table()]
                ]),
                sg.Tab("Plug-Ins", key="plugins_tab", layout=[]),
            ]
        ])
    ]
]

window = sg.Window("EndlessPy").Layout(layout)

while True:
    event, values = window.Read()
    if not event or event == "Exit":
        break
    window.Hide()

    try:
        if event == "Launch Selected":
            if not values["installations_table"]: # Nothing selected
                continue
            constants.installations[values["installations_table"][0]].launch()
        elif event == "Install Nightly":
            install.install_nightly(constants)
        elif event == "Install from Source":
            install.compile_win(constants)

    except Exception as e:
        utils.exception_popup(e)
    window.UnHide()
window.Close()
