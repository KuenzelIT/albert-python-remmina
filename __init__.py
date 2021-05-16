# -*- coding: utf-8 -*-

"""This is the remmina python module for albert.

Synopsis: <trigger> [delay|throw] <query>"""
import subprocess

from albert import *
import os
import configparser

__title__ = "Remmina"
__version__ = "0.5.0"
__triggers__ = "rem "
__authors__ = "Denis Gerber"
# __exec_deps__ = ["whatever"]

HOME_DIR = os.environ["HOME"]
REMMINA_DIR = HOME_DIR + "/.remmina"


def handleQuery(query):
    # Return if string is empty
    if not query.string.strip():
        return

    if not os.path.isdir(REMMINA_DIR):
        return

    results = []

    search = query.string.lower()
    parser = configparser.RawConfigParser()
    files = os.listdir(REMMINA_DIR)

    for fileName in files:
        fullPath = REMMINA_DIR + '/' + fileName
        parser.read(fullPath)

        name = parser.get('remmina', 'name')
        nameLowered = name.lower()

        if search not in nameLowered:
            continue

        results.append(createRemminaItem(name, fullPath))

    return results


def createRemminaItem(name, fullPath):
    try:
        subprocess.call(["remmina", "-v"])
        action = ProcAction(text="ProcAction",
                            commandline=["remmina", fullPath],
                            cwd="~")
    except FileNotFoundError:
        # If remmina is not found in the PATH, fallback to using flatpak
        action = ProcAction(text="ProcAction",
                            commandline=["/usr/bin/flatpak", "run", "org.remmina.Remmina", fullPath],
                            cwd="~")

        # Other installation methods, like snap, are not supported yet

    return Item(id=__title__,
                icon=os.path.dirname(__file__) + "/icon.png",
                text=name,
                subtext="Connect to with Remmina",
                actions=[action])
