from lib.config import CFG

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json
import HttpError

class HttpFram(tornado.web.RequestHandler):
    
    APIVer = None
    Type = None
    TransCode = None

    def get(self):
        try:
            self.getRequestInfo()
        except:
            self.response(HttpError.HttpError(404), 404)
    
    def getRequestInfo(self):
        lUrl = self.request.path.split("/")
        self.APIVer = lUrl[1]
        self.Type = lUrl[2]
        self.TransCode = lUrl[3]
    
        self.write("hello %s " % lUrl)

    def main(self):
        self.getTransCode()

    def getObjects(self):
        sObjects = CFG().getOption('service', 'model')
        if self.Trans not in sObjects.keys():
            
            lObjectList.append(('.*', Error))
            return lObjectList

    def response(self, body, status=200):
        if status != 200:
            self.write_error(status)
        self.write(json.dumps(body))

        
       
def service(port):
    define("port", default=port, help="run on the given port", type=int)
    application = tornado.web.Application([(r".*",HttpFram),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    print "Port %s service stating successful!" % port


