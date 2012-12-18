#!/usr/bin/env python
#coding=utf-8
from lib.config import CFG

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json
from ClientRequest import ClientRequest
from ClientInput import ClientInput

class HttpFram(tornado.web.RequestHandler):
    
    def get(self):
        request = ClientRequest(self.request.path)

        if request.getError() is not None:
            self.noFound()

        else:
            clientInput = ClientInput(request.transCode, self.request.arguments)
        
            if request.controllerPerpare(clientInput.fliter()):
                self.callFunctionAsync(request, callback = self.responseAsync)
            else:
                (content, status) = self.callFunction(request)
                self.response(content, status)
            
    def callFunction(self, Function):
        self.checkClient()
        Function.controllerOperation()
        # try:
        self.checkClient()
        content = Function.controllerResult()
        status  = Function.getStatus()
        # except:
        #     content = {}
        #     status  = 500

        return (content, status)
    
    def noFound(self):
        body  = {'ret': -1, 'msg': 'Page no Found'}
        error = 404
        
        self.response(body, 404)
        
    def checkClient(self):
        if self.request.connection.stream.closed(): 
            self.clear()
            
    # call the controller layer functions
    @tornado.web.asynchronous    
    def callFunctionAsync(self, Function, callback):
        self.checkClient()
        (content, status) = self.callFunction(Function)
        self.checkClient()
        callback(content, status)
            
    # Webview Builder for json format
    def response(self, body={}, status=200, async=False):
        self.checkClient()
        if status != 200:
            self.set_status(status)
        body = json.dumps(body, ensure_ascii=False, encoding="utf-8")
        if async: 
            self.finish(body)
        else: 
            self.write(body)
        
    @tornado.web.asynchronous
    def responseAsync(self, body={}, status=200):
        self.response(body, status, True)

def service(port):
    define("port", default=port, help="run on the given port", type=int)
    ver = CFG.getOption('service', 'ver') 
    apiUrl = "/%s/.*" % ver  
    application = tornado.web.Application([(apiUrl, HttpFram)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    print "Port %s service stating successful!" % port



