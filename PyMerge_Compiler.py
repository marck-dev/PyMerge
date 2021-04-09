#! /usr/bin/python

import argparse
import re
import sys
import os

# < CONSTANTS >
__CMD_IMPORT__ = "import"
__CMD_OUTFILE__ = "outFile"
__CMD_COMPILE__ = "compile"
__CMD_REMOVE_COMF__ = "rmCompile"
__FILE_COMPILER_PREFIX__ = "_"
__COMMAND_WITH_STRING__ = (__CMD_IMPORT__, __CMD_COMPILE__, __CMD_OUTFILE__)
__CMD_ARR__ = (__CMD_COMPILE__, __CMD_IMPORT__, __CMD_OUTFILE__,__CMD_REMOVE_COMF__)
__COMMAND_REGEX__ = r"\s*!(?P<cmd>\w*)\s\"?(?(1)((?P<file>.*)\"\s*)|(?P<args>.*))\n?"
__OUT_FILE_NAME__ = "mergered.pymerge"
# </ CONSTANT >

__out_file__      = None
__args__          = None
__cmd_array__     = []
__file_arr__      = []

# <Terminal colors>
class LinColor:
    NOTICE  = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR   = '\033[91m'
    RESET   = '\033[0m'
    
class WinColor:
    NOTICE  = "color 3"
    SUCCESS = "color 2"
    WARNING = 'color 6'
    ERROR   = "color 4"
    RESET   = "color 0"

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

def exists(file):
    if not os.path.exists(file):
        return False
    else:
        __file_arr__.append(file)
        return True


def generate_compile_file(file):
    return "{}{}".format(__FILE_COMPILER_PREFIX__, file)
            
# Para la compilacion se lee el archivo linea a linea
# se procesa cada linea y si hay alguna importacion
# primero se compila el archivo y luego se importa el
# archivo compilado
def compile(file):
    # generate the cimpile file name
    # TODO: procces paht not only files in current dir
    if not exists(file):
        err("File {} not exists!".format(file))
        exit(2)
    
    outF = generate_compile_file(file)
    altName = None
    notice("Compiling {}".format(file) )
    p()
    if exists(outF):
        notice("Removing {}".format(outF))
        p()
        # lo borramos
        os.remove(outF)
    with open(outF, "w") as f:
        with open(file) as inFile:
            for lineN,l in enumerate(inFile, start=1):
                regex = re.finditer(__COMMAND_REGEX__, l, re.I)
                is_process = False
                for match in regex:
                    is_process = True
                    # guardamos los grupos de las coinidencias
                    groups = match.groupdict()
                    # procesamos el commando:
                    cmd = groups["cmd"]
                    args = ""
                    # get the arguments for the command
                    if cmd in __COMMAND_WITH_STRING__:
                        args = groups["file"]
                        if args == "" or args == None:
                            err("{} - Line {} : File name not found in {} command".format(file,lineN,cmd))
                            p()
                            exit(2)
                    else:
                        args = groups["args"]
                        if args == "" or args == None:
                            err("{} - Line {} : Arguments not found in {} command".format(file,lineN, cmd))
                            p()
                            exit(2)
                    # if cmd == __CMD_COMPILE__:
                    #     notice("Start subprocess:", end="")
                    #     warn("{} - Compiling {}".format(file,args))
                    #     p()
                    #     compile(args)
                    #     continue
                    if cmd == __CMD_IMPORT__:
                        importFile = generate_compile_file(args)
                        notice("{}: Import {}".format(file, args))
                        if not exists(importFile):
                            compile(args)
                            # p()
                            # err("{} - Line {} : File {} not fount! - ".format(file,lineN,importFile), end="")
                            # p("You must compile file before import!")
                            # p()
                            # exit(1)
                        with open(importFile) as inF:
                            for inLine in inF:
                                f.write(inLine)
                        f.write("\n")
                        os.remove(importFile)
                        continue
                    if cmd == __CMD_OUTFILE__:
                        altName = args
                        warn("Set out name to {}".format(args), end="")
                        p()
                        continue
                        
                if not is_process:
                    f.write(l)
    if altName != None:
        os.rename(outF, altName)
           
def concat(files, out_file = __OUT_FILE_NAME__):
    if exists(out_file):
        os.remove(out_file)
    for f in files:
        compile(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile Files")
    parser.add_argument("files", metavar="F", nargs="+", help="File to compile")
    args = parser.parse_args()
    if len(args.files) != 0:
        for file in args.files:
            if exists(file):
                compile(file)
            else:
                err("File {} not exists!".format(file))
    
# compile("test.js")
p()