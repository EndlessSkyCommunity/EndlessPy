import logging
import os
import shutil
import sys
import traceback
from zipfile import ZipFile

import PySimpleGUI as sg
import requests

from constants import Constants

log = logging.getLogger("utils.py")


def install_git(dir: str, constants: Constants):
    log.info("Downloading Git")
    os.makedirs(dir, exist_ok=True)
    archive = os.path.join(dir, "git" + os.path.splitext(constants.win64_git)[1])
    download_file(constants.win64_git, archive, None)
    git_dir = os.path.join(dir, "git")
    extract(archive, git_dir)
    return os.path.join(git_dir, "cmd")


def clone(repo_url: str, dir: str, git_dir: str):
    log.info("Cloning %s to %s" % (repo_url, dir))

    def update(op_code, cur_count, max_count=None, message=""):
        sg.OneLineProgressMeter("Cloning", cur_count, max_count, "clonemeter", message, orientation="h")

    # Black Magic to make GitPython use the right git executable, see https://stackoverflow.com/questions/58581468/
    os.environ["PATH"] = os.pathsep.join([git_dir]) + os.pathsep + os.environ["PATH"]
    import git

    temp_dir = os.path.join(dir, "temp")
    repo = git.Repo.clone_from(repo_url, temp_dir, progress=update)
    repo.close()

    for f in os.listdir(temp_dir):
        shutil.move(os.path.join(temp_dir, f), dir)
    os.rmdir(temp_dir)

    return git.Repo(dir)


def download_file(url: str, path: str, size_estimate: int = None):
    log.info("Downloading file %s to %s" % (url, path))
    r = requests.get(url, stream=True)
    size = int(r.headers.get('content-length', 0))
    size_estimated = size == 0
    if size_estimated:
        size = size_estimate
    name = os.path.basename(path)

    chunk_size = 1024 * 512
    with open(path, "wb") as handle:
        done = 0
        for data in r.iter_content(chunk_size):
            done += chunk_size
            sg.OneLineProgressMeter("Downloading %s" % name, done, size, "downloadmeter",
                                    "Note: Total size is an estimate." if size_estimated else "", orientation="h")
            handle.write(data)


def extract(archive: str, dir: str):
    log.info("Extracting Archive %s to %s" % (archive, dir))
    if archive.endswith(".zip"):
        with ZipFile(archive) as z:
            z.extractall(dir)
    else:
        log.error("format not supported!")
    log.info("Removing archive")
    os.remove(archive)


def empty_directory(dirpath: str):
    log.info("Emptying directory " + dirpath)
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


def exception_popup(exception: Exception):
    type_, value_, tb = sys.exc_info()
    sg.PopupOK("An Error occurred:\n" + "".join(traceback.format_exception(type_, value_, tb)))
