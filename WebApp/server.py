
from lib.config import config
from objects import *

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.web
from tornado.options import define, options

def getPorts():
    sPort = config().getOption('service', 'ports')
    lPortList = []
    for port in sPort.split(','):
        try:
            lPortList.append(int(port))
        except:
            pass

    return lPortList

def getObjects():
    sObjects = config.getOption('service', 'model')

    lObjectList = []
    for ojc in sObjects.split(','):
        sRegex = r'^/%s/(.*)' % ojc
        lObjectList.append((sRegex, ojc))
    #
    # code defend
    #
    lObjectList.append(('.*', Error))
    return lObjectList

def service(port):
    define("port", default=port, help="run on the given port", type=int)

    objects = getObjects()
    application = tornado.web.Application(objects)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    print "Port %s service stating successful!" % port

def start():
    if os.fork() != 0:
        exit()
    map(service, getPorts())

if __name__ == "__main__":
    start()

