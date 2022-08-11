# Copyright 2022 iiPython
# Uses .format() as Python can be as low as v3.5

# Modules
import os
import sys
import shutil
import tarfile

from latest_ver import get_ver

# Uncomment following line and line 47 to keep repl alive till python is updated
# from keep_alive import keep_alive

# Initialization
packages_installed = False
_PYTHON_VERSION = get_ver()
_PYTHON_BASE_URL = "https://www.python.org/ftp/python/{}/Python-{}.tar.xz"
_PYTHON_DIR = os.path.join(os.path.dirname(__file__), "python")
_PYTHON_SRC = os.path.join(os.path.dirname(__file__), "python_src")

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
_VER_FILE = os.path.join(_PYTHON_DIR, "ver.txt")
_LAST_VER = open(_VER_FILE, "r").read() if os.path.isfile(_VER_FILE) else ""

# Make configuration
_CONFIGURE_FLAGS = "--enable-optimizations"
_CONFIGURE_FLAGS += " --prefix={}".format(os.path.abspath(_PYTHON_DIR))

_INIT_COMMAND = "wget -O package.tar.xz '{}' && tar -xf package.tar.xz"
_MAKE_COMMAND = "./configure {} && make && make install && clear"
_CLEAN_COMMAND = "rm -rf p*"

# Functions
def init() -> None:
    print("Downloading + extracting...")
    os.chdir(os.path.dirname(__file__))
    os.system(
        _INIT_COMMAND.format(_PYTHON_BASE_URL.format(_PYTHON_VERSION, _PYTHON_VERSION))
    )

    os.rename("Python-{}".format(_PYTHON_VERSION), "python_src")
    os.mkdir("python")

    os.chdir("../")


def build() -> None:
    keep_alive()
    print("Building Python {}...".format(_PYTHON_VERSION))
    os.chdir(_PYTHON_SRC)
    os.system(_MAKE_COMMAND.format(_CONFIGURE_FLAGS))

    os.chdir("../python")
    with open("ver.txt", "w+") as verfile:
        verfile.write(_PYTHON_VERSION)

    os.system("./bin/python3 -m ensurepip --upgrade")
    os.chdir("../")

    os.remove("package.tar.xz")
    shutil.rmtree("python_src")

    os.chdir("../")
    print(
        "Python Updated to {}!\nInstalling Python packages listed in requirements.txt...".format(
            _PYTHON_VERSION
        )
    )
    os.system("./custom_python/python/bin/python3 -m pip install -r requirements.txt")
    packages_installed = True


def clean() -> None:
    print("Cleaning...")
    os.chdir(os.path.dirname(__file__))
    os.system(_CLEAN_COMMAND)
    os.chdir("../")


# CLI
args = sys.argv[1:]
cmds = {"init": init, "build": build, "clean": clean}
if args and args[0] in cmds:
    cmds[args[0]]()
    sys.exit(0)

# Handle building
if _PYTHON_VERSION != _LAST_VER:
    i = input(
        "New version available!\nUpgrade to {} ? (May take 30 min at )[y/n]: ".format(
            _PYTHON_VERSION
        )
    )
    if i.startswith("y"):
        # Rebuild
        for f in [clean, init, build]:
            f()
    else:
        pass

# Run script
os.system("clear && ./custom_python/python/bin/python3 -O main.py".format(""))
# Add './custom_python/python/bin/python3 -m pip install -r requirements.txt &&' if not packages_installed else '')
