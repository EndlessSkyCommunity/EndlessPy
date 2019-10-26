import logging
from platform import architecture
from sys import platform

import appdirs

log = logging.getLogger("constants.py")


class Constants:
    def __init__(self):
        # Default Settings
        self.es_git = "https://github.com/endless-sky/endless-sky.git"
        self.es_master_zip = "https://codeload.github.com/endless-sky/endless-sky/zip/master"
        self.nightly_win64 = "http://mcofficer.me:8080/job/endless-sky-win64/lastSuccessfulBuild/artifact/bin/Release" \
                             "/EndlessSky.exe "
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

        if platform.startswith("linux"):  # On Python 3.2 and older, "linux" may be followed by a version number
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
