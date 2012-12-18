#!/usr/bin/env python
import controller
from controller import *
from ClientInput import ClientInput
    
class ClientRequest:
    
    _lTransCode = controller.__all__
    url = ''
    _error = None
    transCode = None
    _defaultTransCode    = 'DEFAULT'
    _defaultOperationCode = 'do'
    
    cotrollerPrefix = 'c%s'
    contoller = None
    
    def __init__(self, url):
        self.url = url
        self.transCode = self.getTransCode()

        if self.checkTranCode(self.transCode[0]) == False:
            self._error = 404
            
    def __del__(self):
        pass
    
    def getError(self):
        return self._error
    
    def checkTranCode(self, transCode):
        return (self.cotrollerPrefix % transCode in self._lTransCode)
        
    def getTransCode(self):

        lUrl = fliter(None, self.url.split('/'))
        if len (lUrl) > 3:
            tCode = (lUrl[2].upper(), lUrl[3].lower())
        elif len(lUrl) > 2:
            tCode = (lUrl[2].upper(), self._defaultOperationCode)
        else:
            tCode = (self._defaultTransCode, self._defaultOperationCode)

        self.transCode = tCode
        return self.transCode
    
    def getRequestInfo(self, var):
        inputFliter = ClientInput(self.transCode, var)
        return inputFliter.fliter()
    
    def _getController(self):
        controllerName = self.cotrollerPrefix % self.transCode[0]
        exec ('objec = controller.%s.Main' % controllerName)
        
        return objec
        
    def controllerPerpare(self, var):
        objec = self._getController()
        self.controller = objec(var)
        return self.controller.async
        
    def controllerOperation(self):
        do = 'self.controller.%s()' % self.transCode[1]
        exec(do)
    
    def controllerResult(self):
        return self.controller.getResult()
    
    def getStatus(self):
        return self.controller.status
        
    