import logging
import os
import shutil
import sys
import traceback
from zipfile import ZipFile

import PySimpleGUI as sg
import git
import requests

log = logging.getLogger("utils.py")


def clone(repo_url, dir, git_bin):
    log.info("Cloning %s to %s" % (repo_url, dir))
    git_bin = git_bin or r"C:\Users\Florian\Downloads\mingit-busybox\cmd\git"

    def update(op_code, cur_count, max_count=None, message=""):
        log.info("Cloning, op_code: %s, current: %s, max: %s, message: %s" % (op_code, cur_count, max_count, message))
        sg.OneLineProgressMeter("Cloning", cur_count, max_count, "clonemeter", message, orientation="h")

    os.putenv("GIT_PYTHON_GIT_EXECUTABLE", git_bin)
    g = git.Git(dir)
    log.info(g.GIT_PYTHON_GIT_EXECUTABLE)
    log.info(str(g.version_info))
    log.info(str(g.environment()))
    repo = git.Repo.clone_from(repo_url, dir, env={"GIT_PYTHON_GIT_EXECUTABLE": git_bin}, progress=update)
    return repo


def download_file(url, path, size_estimate):
    log.info("Downloading file %s to %s" % (url, path))
    r = requests.get(url, stream=True)
    size = int(r.headers.get('content-length', 0))
    size_estimated = size == 0
    if size_estimated:
        size = size_estimate
    name = os.path.basename(path)
    with open(path, "wb") as handle:
        done = 0
        for data in r.iter_content(1024):
            done += 1024
            sg.OneLineProgressMeter("Downloading %s" % name, done, size, "downloadmeter",
                                    "Note: Total size is an estimate." if size_estimated else "", orientation="h")
            handle.write(data)


def extract(archive, dir):
    log.info("Extracting Archive %s to %s" % (archive, dir))
    if archive.endswith(".zip"):
        with ZipFile(archive) as z:
            z.extractall(dir)
    else:
        log.error("format not supported!")
    log.info("Removing archive")
    os.remove(archive)


def empty_directory(dirpath):
    log.info("Emptying directory " + dirpath)
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


def exception_popup(exception):
    type_, value_, tb = sys.exc_info()
    sg.PopupOK("An Error occurred:\n" + "".join(traceback.format_exception(type_, value_, tb)))
