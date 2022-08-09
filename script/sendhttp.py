from http.server import BaseHTTPRequestHandler
from io import BytesIO
from urllib3 import HTTPResponse as urllib3RES
from http.client import HTTPResponse
from lib.Interface import GunnerMod
import socket,ssl
from os.path import dirname,abspath
class GunnerHTTPRequestParser(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def __str__(self):
        return self.rfile.getvalue().decode()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

    def setHeaders(self, args={}):
        headers = dict(self.headers)
        if(len(args)):
            headerskey = list(headers.keys())
            klINm = [k.lower() for k in headerskey]
            for key, value in args.items():
                keyl = key.lower()
                if keyl not in klINm:
                    headers[key] = value
                    continue
                headers[headerskey[klINm.index(keyl)]] = value
        newreq = ["{} {} {}".format(self.command, self.path, self.request_version)]
        newreq.extend(list("{}: {}".format(k, v) for k, v in headers.items()))
        newreq = '\r\n'.join(newreq) + '\r\n'*2 + '' if not(body := self.rfile.read().decode()) else body
        self.__init__(newreq.encode())

 
@GunnerMod
def start(requestFile,taskinfo=None,**headers):
    with open(abspath(f"{dirname(__file__)}/{requestFile}"),'r') as reqf:
        req = GunnerHTTPRequestParser(reqf.read().encode())
    if req.error_code != None:
        print(req.error_message)
        return
    req.setHeaders(headers)
    res = request(req,taskinfo)
    #print(res.encode())
    taskinfo.log(res.encode())
    taskinfo.update("Response is in log file.")

def request(req,taskinfo):
    hostname = req.headers['Host']
    def http(req):
        with socket.create_connection((hostname, 80)) as sock:
            sock.send(str(req).encode())
            return Getres(sock)
    def https(req):
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.send(str(req).encode())
                return Getres(ssock)
    try:
        res = https(req)
    except ssl.SSLError as e:
        print(e)
        print("Error,trying http...")
        res = http(req)
    except Exception as e:
        taskinfo.error(e)
        return
    
    headers = ['{}: {}'.format(k,v) for k,v in res.headers.items()]
    body = res.data
    #Protocol Status Reason
    psr = 'HTTP {} {}\r\n'.format(res.status,res.reason)
    sres = psr + '\r\n'.join(headers) + '\r\n'*2 + body.decode() + '\r\n'
    return sres
    
def Getres(sock):
    res = HTTPResponse(sock)
    res.begin()
    res2 = urllib3RES.from_httplib(res)
    return res2

