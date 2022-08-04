from http.server import BaseHTTPRequestHandler
from io import BytesIO
from urllib3 import HTTPResponse as urllib3RES
from http.client import HTTPResponse

class HTTPRequestParser(BaseHTTPRequestHandler):
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

    def setHeaders(self, args):
        headers = dict(self.headers)
        if(len(args)):
            headerskey = list(headers.keys())
            klINm = [k.lower() for k in headerskey]
            for key, value in args.items():
                keyl = key.lower()
                if keyl not in klINm:
                    headers[key] = value
                    continue
                if (index := klINm.index(keyl)) != -1:
                    headers[headerskey[index]] = value
                    continue
        newreq = ["{} {} {}".format(self.command, self.path, self.request_version)]
        newreq.extend(list("{}: {}".format(k, v) for k, v in headers.items()))
        newreq = '\r\n'.join(newreq) + '\r\n'*2 + '' if not(body := self.rfile.read().decode()) else body
        self.__init__(newreq.encode())

class GunnerResponse():
    def __init__(self, response_bytes):
        self._file = BytesIO(response_bytes)
    def makefile(self, *args, **kwargs):
        return self._file
    def getHTTPResponse(self):
        httpres = HTTPResponse(self)
        httpres.begin()
        return httpres
    def getParsedRes(self):
        res = self.getHTTPResponse()
        return urllib3RES.from_httplib(res)
    

