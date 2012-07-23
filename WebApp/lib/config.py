import os
from ConfigParser import ConfigParser

class lConfig (object):
    __cache = {}
    __filename = 'config.ini'

    def __init__(self, sFile = ''):
        if sFile != '':
            self.__filename = sFile

        config = ConfigParser()
        config.read(self.__filename)
        
        for section in config.sections():
            self.__cache[section] = {}
            for option in config.options(section):
                self.__cache[section][option] = config.get(section, option)

    def __getattr__(self, section):
        if self.__cache.has_key(section):
            return self.__cache[section]
        else:
            return {}

    def getSection(self, section):
        if self.__cache.has_key(section):
            return self.__cache[section]
        else:
            errorMessage = 'Section %s not found!' % (section)
            raise NameError, errorMessage

    def getOption(self, section, option):
        if self.__cache.has_key(section) and self.__cache[section].has_key(option):
            return self.__cache[section][option]
        else:
            errorMessage = 'Option %s[%s] not found!' % (section, option)
            raise NameError, errorMessage

    def __repr__(self):
        filestring = open(self.__filename, 'r').read()
        string = '''Config File: %s
----------
%s
----------
        ''' % (self.__filename, filestring)

        return string

class CFG(lConfig):
    pass
