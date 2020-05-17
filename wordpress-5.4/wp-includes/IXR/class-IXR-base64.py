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
#// IXR_Base64
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_Base64():
    data = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, data_=None):
        
        
        self.data = data_
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_base64(self, data_=None):
        
        
        self.__init__(data_)
    # end def ixr_base64
    def getxml(self):
        
        
        return "<base64>" + php_base64_encode(self.data) + "</base64>"
    # end def getxml
# end class IXR_Base64
