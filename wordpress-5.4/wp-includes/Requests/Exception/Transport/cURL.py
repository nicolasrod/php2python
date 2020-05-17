#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
class Requests_Exception_Transport_cURL(Requests_Exception_Transport):
    EASY = "cURLEasy"
    MULTI = "cURLMulti"
    SHARE = "cURLShare"
    #// 
    #// cURL error code
    #// 
    #// @var integer
    #//
    code = -1
    #// 
    #// Which type of cURL error
    #// 
    #// EASY|MULTI|SHARE
    #// 
    #// @var string
    #//
    type = "Unknown"
    #// 
    #// Clear text error message
    #// 
    #// @var string
    #//
    reason = "Unknown"
    def __init__(self, message_=None, type_=None, data_=None, code_=0):
        
        
        if type_ != None:
            self.type = type_
        # end if
        if code_ != None:
            self.code = code_
        # end if
        if message_ != None:
            self.reason = message_
        # end if
        message_ = php_sprintf("%d %s", self.code, self.reason)
        super().__init__(message_, self.type, data_, self.code)
    # end def __init__
    #// 
    #// Get the error message
    #//
    def getreason(self):
        
        
        return self.reason
    # end def getreason
# end class Requests_Exception_Transport_cURL
