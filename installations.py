import subprocess
import os


class Installation:
    def __init__(self, name="", installdir="", type="", es_git=None, es_master_zip=None, nightly_win64=None,
                 nightly_osx_page=None, win64_libs=None, osx_libs=None, win64_dev_libs=None, mingw_win64=None, **kwargs):
        self.name = name
        self.installdir = installdir
        self.type = type
        self.es_git = es_git
        self.es_master_zip = es_master_zip
        self.nightly_win64 = nightly_win64
        self.nightly_osx_page = nightly_osx_page
        self.win64_libs = win64_libs
        self.osx_libs = osx_libs
        self.win64_dev_libs = win64_dev_libs
        self.mingw_w64 = mingw_win64

    def launch(self):
        subprocess.run(os.path.join(self.installdir, "EndlessSky.exe"))
