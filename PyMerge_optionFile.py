#! /usr/bin/python

import re
import json
import os

__COMMAND_REGEX__ = r"\s*(?P<cmd>\w*)\s\"?(?(1)((?P<file>.*)\"\s*)|(?P<args>.*))\n?"

__out_file__ = None
__args__ = None
__cmd_array__ = []
__file_arr__ = []

# <Terminal colors>

class LinColor:
    NOTICE = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    RESET = '\033[0m'
    
class WinColor:
    NOTICE = "color 3"
    SUCCESS = "color 2"
    WARNING = '\033[93m'
    ERROR = "color 4"
    RESET = "color 0"

def err(msg, end="\n"):
    color = LinColor.ERROR
    if os.name == "nt":
        color = ""
        os.system(WinColor.ERROR)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def success(msg, end="\n"):
    color = LinColor.SUCCESS
    if os.name == "nt":
        color = ""
        os.system(WinColor.SUCCESS)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def p(msg ="", end="\n"):
    color = LinColor.RESET
    if os.name == "nt":
        color = ""
        os.system(WinColor.RESET)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def warn(msg, end="\n"):
    color = LinColor.WARNING
    if os.name == "nt":
        color = ""
        os.system(WinColor.WARNING)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def notice(msg, end="\n"):
    color = LinColor.NOTICE
    if os.name == "nt":
        color = ""
        os.system(WinColor.NOTICE)
    print("{x}{msg}".format(msg=msg, x=color),  end=end)
    
# </ Terminal colors >

def import_file(file):
    if not os.path.exists(file):
        return -1
    else:
        __file_arr__.append(file)
        return 0
    
def concat(files, out_file = "dist.js"):
    if os.path.exists(out_file):
        os.remove(out_file)
    with open(out_file, "w") as out:
        for f in files:
            with open(f) as _in:
                for line in _in.readlines():
                    out.writelines(line)
            # salto de linea entre archivos
            out.write("\n")

p()
with open("pymerge") as file:
    p("Reading config file!")
    content = file.read()
    regex = re.finditer(__COMMAND_REGEX__, content, re.MULTILINE)
    # recorremos las coincidencias
    for matchNum, match in enumerate(regex, start=1):
        __cmd_array__.append(match.groupdict())
if len(__cmd_array__) == 0:
    p()
    err("Empty config file!")
    p()
    exit(0)
else:
    p("Procces file!")
    for command in __cmd_array__:
        if command["cmd"] == "import":
            if import_file(command["file"]) == -1 :
                err("ERROR!", end=" ")
                p("- File {f} not exists".format(f=command["file"]))
        if command["cmd"] == "outFile":
            __out_file__ = command["file"]
    if len(__file_arr__) > 0:
        if __out_file__ == None:
            warn("Out file not set! Setting the default name: 'dist'!")
            __out_file__ = "dist"
        concat(__file_arr__, __out_file__)
        success("\nDone! - ", end="")
        warn("File {0} has been generated!".format(__out_file__))
p()
    
