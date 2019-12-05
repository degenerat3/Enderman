# Enderman
Inject code into python files

### Config
Default payload (beacon.py) is a [crowd control](https://github.com/degenerat3/CrowdControl) callback, but any python file/function can be used as a payload.  

In `main.py` update the `MODULE_CODE` variable with the name of the payload (default is "beacon.py") and update the `DEST_MODULE_NAME` with what you would like the payload file to be called on-system.  

Use `builder.sh` to put the payload into "ender.zip" or whatever you wanna call it. 

### Usage  

`python3 ender.zip /` will, when run with root privs, infect every `site.py` on the system.  
The "site.py" is imported any time that python is invoked, and we make the site.py import our malicious module. Since python will run the `main` function at import time, this means our malicious code will be run every time python is invoked (a script is ran, a python console is opened, etc). 
