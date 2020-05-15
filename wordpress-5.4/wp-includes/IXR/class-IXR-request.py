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
#// IXR_Request
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_Request():
    method = Array()
    args = Array()
    xml = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, method=None, args=None):
        
        self.method = method
        self.args = args
        self.xml = str("<?xml version=\"1.0\"?>\n<methodCall>\n<methodName>") + str(self.method) + str("</methodName>\n<params>\n")
        for arg in self.args:
            self.xml += "<param><value>"
            v = php_new_class("IXR_Value", lambda : IXR_Value(arg))
            self.xml += v.getxml()
            self.xml += "</value></param>\n"
        # end for
        self.xml += "</params></methodCall>"
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_request(self, method=None, args=None):
        
        self.__init__(method, args)
    # end def ixr_request
    def getlength(self):
        
        return php_strlen(self.xml)
    # end def getlength
    def getxml(self):
        
        return self.xml
    # end def getxml
# end class IXR_Request
