import pymongo

class MongoDB:
    
    _hostName = None
    poolSize = 0
    connectionPool = []
    
    _instance = None
    _poolCursor = 0
    
    def __init__(self, hostName, poolSize=1, readOnly = False):
        if readOnly:
            hostName = hostName + "-" + "read"
            
        self._hostName = hostName
        
        for i in range(poolSize):
            Host = CFG().getOption("mongodb", hostName)
            self.connectionPool.apend(pymongo.Connection(Host))
        
        self.poolSize = poolSize
        
    def __new__(self, hostName, poolSize, readOnly):
        if not self._instance and self._hostName != hostName:  
            self._instance = super(MongoDB, self).__new__(  
                                        self, hostName, poolSize, readOnly)  
        return self._instance
        
    def __del__(self):
        for connection in self.connectionPool:
            connection.close()
    
    def _getConnection(self):
        if self._poolCursor == self.poolSize: self._poolCursor = 0
        else: self._poolCursor += 1
        
        return self.connectionPool[self._poolCursor]
    
    def __getattr__(self, collectionName):
        conn = self._getConnection()
        return conn[collectionName]
    