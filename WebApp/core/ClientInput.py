class ClientInput:
    
    transCode     = None
    operationCode = None
    var           = {}
    
    
    def __init__(self, transCode, var):
        (self.transCode, self.operationCode) = transCode
        self.var = var

    def __del__(self):
        pass
        
    def fliter(self):
        function = 'self.%s(self.operationCode)' % self.transCode
        
        exec('obj = %s ' % function)
        return obj
    
    def __call__(self, **argv):
        return self.var
    
    def _getVar(self, fieldName, default=None):
        
        try:
            var = self.var[fieldName]
            return var[0]
        except:
            return default