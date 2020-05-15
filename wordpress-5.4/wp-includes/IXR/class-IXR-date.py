#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// IXR_Date
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_Date():
    year = Array()
    month = Array()
    day = Array()
    hour = Array()
    minute = Array()
    second = Array()
    timezone = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, time=None):
        
        #// $time can be a PHP timestamp or an ISO one
        if php_is_numeric(time):
            self.parsetimestamp(time)
        else:
            self.parseiso(time)
        # end if
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_date(self, time=None):
        
        self.__init__(time)
    # end def ixr_date
    def parsetimestamp(self, timestamp=None):
        
        self.year = gmdate("Y", timestamp)
        self.month = gmdate("m", timestamp)
        self.day = gmdate("d", timestamp)
        self.hour = gmdate("H", timestamp)
        self.minute = gmdate("i", timestamp)
        self.second = gmdate("s", timestamp)
        self.timezone = ""
    # end def parsetimestamp
    def parseiso(self, iso=None):
        
        self.year = php_substr(iso, 0, 4)
        self.month = php_substr(iso, 4, 2)
        self.day = php_substr(iso, 6, 2)
        self.hour = php_substr(iso, 9, 2)
        self.minute = php_substr(iso, 12, 2)
        self.second = php_substr(iso, 15, 2)
        self.timezone = php_substr(iso, 17)
    # end def parseiso
    def getiso(self):
        
        return self.year + self.month + self.day + "T" + self.hour + ":" + self.minute + ":" + self.second + self.timezone
    # end def getiso
    def getxml(self):
        
        return "<dateTime.iso8601>" + self.getiso() + "</dateTime.iso8601>"
    # end def getxml
    def gettimestamp(self):
        
        return mktime(self.hour, self.minute, self.second, self.month, self.day, self.year)
    # end def gettimestamp
# end class IXR_Date
