from sys import platform
from platform import architecture
import logging
from ruamel.yaml import YAML
import appdirs
import os
from installations import Installation

log = logging.getLogger("constants.py")


class Constants:
    def __init__(self):
        self.config_dir = appdirs.user_config_dir("EndlessPy", appauthor=False)
        os.makedirs(self.config_dir, exist_ok=True)

        self.yaml = YAML()
        self.yaml.register_class(Installation)
        self.yaml.default_flow_style = False

        self.installations_file = os.path.join(self.config_dir, "installations.yaml")
        self.installations = self._read_installations()

        # Default Settings
        self.es_git = "https://github.com/endless-sky/endless-sky.git"
        self.es_master_zip = "https://codeload.github.com/endless-sky/endless-sky/zip/master"
        self.nightly_win64 = "http://mcofficer.me:8080/job/endless-sky-win64/lastSuccessfulBuild/artifact/bin/Release/EndlessSky.exe"
        self.nightly_osx_page = "https://api.github.com/repos/ES-Builds/endless-sky-osx/releases/latest"
        self.win64_libs = "https://endlesssky.mcofficer.me/requiredLibs.zip"
        self.osx_libs = "https://endlesssky.mcofficer.me/requiredLibsOSX.zip"
        self.win64_dev_libs = "http://endless-sky.github.io/win64-dev.zip"
        self.mingw_win64 = "https://endlesssky.mcofficer.me/x86_64-7.2.0-release-posix-seh-rt_v5-rev1.zip"
        self.plugin_hub = "https://endlesssky.mcofficer.me/pluginhub"
        self.plugin_api_endpoint = "/api/plugins"

        self.linux_plugin_dir = "~/.local/share/endless-sky/plugins/"
        self.windows_plugin_dir = appdirs.user_config_dir("plugins", "endless-sky", roaming=True)
        self.osx_plugin_dir = "~/Library/ApplicationSupport/endless-sky/plugins"

        if platform.startswith("linux"): # On Python 3.2 and older, "linux" may be followed by a version number
            self.os = "linux"
        elif platform == "win32":
            if architecture()[0] == "64bit":
                self.os = "win64"
            elif architecture()[1] == "32bit":
                self.os = "win32"
            else:
                logging.error("Got unknown system architecture " + architecture()[0] + "!")
        elif platform == "darwin":
            self.os = "osx"
        else:
            logging.error("Got unknown Operating System " + platform + "!")

    def _read_installations(self):
        if not os.path.exists(self.installations_file):
            return []
        else:
            with open(self.installations_file, "r") as f:
                return self.yaml.load(f) or []

    def _save_installations(self):
        with open(self.installations_file, "w") as f:
            self.yaml.dump(self.installations, f)

    def add_installation(self, installation):
        self.installations.append(installation)
        self._save_installations()
