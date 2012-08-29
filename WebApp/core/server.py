#!/usr/bin/env python

from lib.config import CFG
from lib import signature

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json
import HttpError
from model import *

class HttpFram(tornado.web.RequestHandler):
    
    APIVer = None
    Type = None
    TransCode = None

    def get(self):
        self.getRequestInfo()
        self.getRespones()
   
    def getRequestInfo(self):
        lUrl = self.request.path.split("/")
        if len(lUrl) < 3:
            self.response(HttpError.HttpError(404), 404)
        else:
            self.APIVer = lUrl[1]
            self.Type = lUrl[2]
            self.TransCode = lUrl[3]
     
    def getRespones(self):
        var = self.checkRequest()
        if var is None:
            return 
        className = "m%s.Main" % (self.TransCode)
        exec "oClass = "+className
        mClass = oClass(var)
        mClass.do()

        result = mClass.getResult()
        
        self.response(result)
 
    def checkRequest(self):
        jVar = self.get_argument('var', None)
        sign = self.get_argument('sign', None)        

        if sign is None :#or signature.check(var, sign) == False:
            self.response(HttpError.HttpError(405), 405)
        else:    
            try:
                return json.loads(jVar)
            except:
                self.respone(HttpError.HttpError(406), 406)

    def response(self, body, status=200):
        if status != 200:
            self.set_status(status)
            self.finish(json.dumps(body))
        else:
            sign = signature.get(json.dumps(body))
            fullBody = { self.TransCode : body, "sig" : sign }
            self.finish(json.dumps(fullBody)) 

def service(port):
    define("port", default=port, help="run on the given port", type=int)
    application = tornado.web.Application([(r".*",HttpFram),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    print "Port %s service stating successful!" % port
