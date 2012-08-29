import redis
import random

__all__ = ['KeyValue', "Queue", "Counter", "KeyList", "HashTable", "SortSet"]

class redisPool(object):
    _pool ={}
    
    poolSize = 1
    
    def __init__(self, host):
        if host not in self._cache.keys() or len(self._cache[host]) == 0:
            self._pool[host] = []
            for i in range(0, self.poolSize):
                self._pool[host].append(self.connect(host))            


    def __del__(self):
        for key in self._pool.keys():
            for handle in self._pool[key]:
                handle.close()

    def connect(self, host):        
        try:
            handle=redis.Redis(host, port=port, db=db)
        except:
            errorMessage = "Can't connect to %s:%s/%s" % (host, port, db)
            raise IOException, errorMessage
        
        return handle
        
    def getConnect(self, host, db=0):
        rand = random.randint(0, self.poolSize + 1)
        handle = self._pool[host][rand]
        
        handle.select(db)
        
        return handle

class redisHandle:

    handle = None    
    _keyPre = "%s"
    
    def __init__(self, host, db=0):
        pool = redisPool(host)
        self.handle = pool.getConnect(host, db)
            
    def getKey(self, key):
        return self._keyPre % key
    
    def delete(self, key):
        key = self.getKey(key)
        return self.handle.delete(key)
        
    def setExp(self, key, time=3600):
        key = self.getKey(key)
        return self.handle.expire(key,time)

    def exist(self, key):
        key = self.getKey(key)
        return self.handle.exists(key)
        
class KeyValue(redisHandle):
    _keyPre="k%s"
    
    def set(self, key, value=""):
        key = self.getKey(key)
        return self.handle.set(key, value)
        
    def incr(self, key, value=1):
        key = self.getKey(key)
        value = int(value)
        
        return self.handle.incrby(key, value)
        
class Counter(KeyValue):
    _keyPre = "c%s"
    add = incr

class Queue(redisHandle):
    _keyPre = "q%s"
    
    def push(self, key, value="", desc=False):
        key = self.getKey(key)
        if desc:
            return self.handle.rpush(key, value)
        return self.handle.lpush(key, value)
        
    def pushMulit(self, key, lValue, desc=False):
        key = self.getKey(key)
        count = 0
        for value in lValue: 
            if desc:
                self.handle.rpush(key, value)
            else:
                self.handle.lpush(key, value)
            count += 1
        return count
        
    def pop(self, key, desc=False):
        key = self.getKey(key)
        if desc:
            return self.handle.rpop(key)
        return self.handle.lpop(key)
        
    def popMulit(self, key, count=1, desc=False):
        if count <= 1:
            return self.pop(key, desc)
        
        key = self.getKey(key)
        lResult = []
        for loop in range(0, count):
            if desc:
                result = self.handle.rpop(key)
            else:
                result = self.handle.lpop(key)
            
            lResult.append(result)
            
        return lResult 
        
    def count(self, key):
        key = self.getKey(key)
        return self.handle.llen(key)
        
    def all(self, key):
        key = self.getKey(key)
        return self.handle.lrange(key, 0, -1)
        
class KeyList(Queue):
    _keyPre = "l%s"
    
    def insert(self, key, source, value, before=False):
        key = self.getKey(key)
        return self.handle.linsert(key, source, before, value)
    
    def setByIndex(self, key, value, index=-1):
        key = self.getKey(key)
        return self.handle.lset(key, index, value)
    
    def getByIndex(self, key, index=-1):
        key = self.getKey(key)
        
        return self.handle.lindex(key, index)
        
    def deleteByIndex(self, key, start=1, count=1):
        key = self.getKey(key)
        end = start + count
        
        return self.handle.ltrim(key, start, stop)
        
class HashTable(redisHandle):
    _keyPre = "h%s"
    
    def set(self, key, dValue={}):
        key = self.getKey(key)
        return self.handle.hmset(key, dValue)
    
    def setField(self, key, field, value):
        key = self.getKey(key)
        return self.handle.hset(key, field, value)
    
    def get(self, key, field=None):
        key = self.getKey(key)
        if field is None:
            return self.handle.hgetall(key)
        return self.handle.hmget(key, field)
            
    def hasField(self, key, field):
        key = self.getKey(key)
        return self.handle.hexists(key, field)
        
    def incr(self, key, filed, value=1):
        key = self.getKey(key)
        return self.handle.hincrby(key, fieldm, value)
        
    def getAllKeys(self, key):
        key = self.getKey(key)
        return self.handle.hkeys(key)
        
    def deleteField(self, key, field):
        key = self.getKeys(key)
        return self.handle.hdel(key, field)

class SortSet(redisHandle):
    _keyPre = "s%s"
    
    def set(self, key, field, value):
        key = self.getKey(key)
        return self.handle.zadd(key, value, field)
        
    def getScore(self, key, member):
        key = self.getKey(key)
        return self.handle.zscore(key, member)
    
    def getRank(self, key, member):
        key = self.getKey(key)
        return self.handle.zrank(key, member)
        
    def getRange(self, key, min=0, max=0, withScore=True):
        key = self.getKey(key)
        if withScore:
            return self.handle.zrange(key, min, max, true)
        return self.handle.zrange(key, min, max)
        
    def deleteMember(self, key, member):
        key = self.getKey(key)
        return self.handle.zrem(key, member)
        
    def getCount(self, key, min=None, max=None):
        key = self.getKey(key)
        if min is None:
            return self.handle.zcard(key)
        if min is not None and max is None:
            max = min
        return self.handle.zcount(key, min, max)
        
    def incr(self, key, member, value):
        key = self.getKey(key)
        return self.handle.zincrby(key, value, member)
        
    