#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    def __init__(self, method_=None, args_=None):
        
        
        self.method = method_
        self.args = args_
        self.xml = str("<?xml version=\"1.0\"?>\n<methodCall>\n<methodName>") + str(self.method) + str("</methodName>\n<params>\n")
        for arg_ in self.args:
            self.xml += "<param><value>"
            v_ = php_new_class("IXR_Value", lambda : IXR_Value(arg_))
            self.xml += v_.getxml()
            self.xml += "</value></param>\n"
        # end for
        self.xml += "</params></methodCall>"
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_request(self, method_=None, args_=None):
        
        
        self.__init__(method_, args_)
    # end def ixr_request
    def getlength(self):
        
        
        return php_strlen(self.xml)
    # end def getlength
    def getxml(self):
        
        
        return self.xml
    # end def getxml
# end class IXR_Request
