#! /usr/bin/python

import argparse
import re
import sys
import os

# < CONSTANTS >
__CMD_COMPILE__          = "compile"
__CMD_IMPORT__           = "import"
__CMD_OUTFILE__          = "outFile"
__CMD_REMOVE_COMF__      = "rmCompile"
__COMMAND_REGEX__        = r"((#)|(\/\/))\s*!(?P<cmd>\w*)\s\"?(?(1)((?P<file>.*)\"\s*)|(?P<args>.*))\n?$"
__CMD_ARR__              = (__CMD_COMPILE__, __CMD_IMPORT__, __CMD_OUTFILE__,__CMD_REMOVE_COMF__)
__COMMAND_WITH_STRING__  = (__CMD_IMPORT__, __CMD_COMPILE__, __CMD_OUTFILE__)
__FILE_COMPILER_PREFIX__ = "_"
__OUT_FILE_NAME__        = "mergered.pymerge"
# </ CONSTANT >

# < VARS >
__args__         = None
__cmd_array__    = []
__file_arr__     = []
__files2delete__ = []
__out_file__     = None
# </ VARS >

# <Terminal colors>
class LinColor:
    ERROR   = "\033[91m"
    NOTICE  = "\033[94m"
    RESET   = "\033[0m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    
class WinColor:
    ERROR   = "color 4"
    NOTICE  = "color 3"
    RESET   = "color 0"
    SUCCESS = "color 2"
    WARNING = "color 6"

def err(msg, end = "\n"):
    color = LinColor.ERROR
    if os.name == "nt":
        color = ""
        os.system(WinColor.ERROR)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def success(msg, end = "\n"):
    color = LinColor.SUCCESS
    if os.name == "nt":
        color = ""
        os.system(WinColor.SUCCESS)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def p(msg ="", end = "\n"):
    color = LinColor.RESET
    if os.name == "nt":
        color = ""
        os.system(WinColor.RESET)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def warn(msg, end = "\n"):
    color = LinColor.WARNING
    if os.name == "nt":
        color = ""
        os.system(WinColor.WARNING)
    print("{x}{msg}".format(msg=msg, x=color), end=end)
    
def notice(msg, end = "\n"):
    color = LinColor.NOTICE
    if os.name == "nt":
        color = ""
        os.system(WinColor.NOTICE)
    print("{x}{msg}".format(msg=msg, x=color),  end=end)
# </ Terminal colors >

# File exists function
def exists(file):
    if not os.path.exists(file):
        return False
    else:
        __file_arr__.append(file)
        return True

# Create the compile file name and add to the delete files list
def generate_compile_file(file):
    if file.rfind(os.path.sep) == -1:
        return f"{__FILE_COMPILER_PREFIX__}{file}"
    path_separator_index = file.rindex(os.path.sep)
    f_name = file[path_separator_index+1:]
    _dir = file[0:path_separator_index+1]
    return f"{_dir}{__FILE_COMPILER_PREFIX__}{f_name}"

# delete compiling files
def del_files():
    p()
    notice("Removing compiling files")
    for f in __files2delete__:
        warn(f"\tRemoving {f}")
        os.remove(f)
    p()
            
# For the compile proces, it read line by line and processed it
# to look for any keyword, the command of the compiler
# for this job rewrite the file into another, the compile file,
# when compile finish, the file can be used to be imported in other files.
# If there is any error or compile sucessfully al compile files will be removed
def compile(file, delete = True):
    
    if not exists(file):
        err("File {} not exists!".format(file))
        exit(2)
    
    outF = generate_compile_file(file)
    if not delete:
        __files2delete__.append(outF)
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
                    # save group that match wiht the regex
                    groups = match.groupdict()
                    # get the command of the groups
                    cmd = groups["cmd"]
                    args = ""
                    # get the arguments for the command
                    if cmd in __COMMAND_WITH_STRING__:
                        args = groups["file"]
                        if args == "" or args == None:
                            err("{} - Line {} : File name not found in {} command".format(file,lineN,cmd))
                            p()
                            if delete:
                                __files2delete__.append(outF)
                            else:
                                return
                            del_files()
                            exit(2)
                    else:
                        args = groups["args"]
                        if args == "" or args == None:
                            err("{} - Line {} : Arguments not found in {} command".format(file,lineN, cmd))
                            p()
                            if delete:
                                __files2delete__.append(outF)
                            else:
                                return
                            del_files();
                            exit(2)
                    if cmd == __CMD_IMPORT__:
                        importFile = generate_compile_file(args)
                        notice("{}: Import {}".format(file, args))
                        if not exists(importFile):
                            # if not exists the compile file, compile the original
                            # file an then import it
                            compile(args, False)
                        with open(importFile) as inF:
                            for inLine in inF:
                                f.write(inLine)
                        f.write("\n")
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
    if len(__files2delete__) > 0 and delete:
        del_files()
           

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

p()
