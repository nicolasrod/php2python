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
#// Exception for HTTP requests
#// 
#// @package Requests
#// 
#// 
#// Exception for HTTP requests
#// 
#// @package Requests
#//
class Requests_Exception(Exception):
    type = Array()
    data = Array()
    #// 
    #// Create a new exception
    #// 
    #// @param string $message Exception message
    #// @param string $type Exception type
    #// @param mixed $data Associated data
    #// @param integer $code Exception numerical code, if applicable
    #//
    def __init__(self, message=None, type=None, data=None, code=0):
        
        super().__init__(message, code)
        self.type = type
        self.data = data
    # end def __init__
    #// 
    #// Like {@see getCode()}, but a string code.
    #// 
    #// @codeCoverageIgnore
    #// @return string
    #//
    def gettype(self):
        
        return self.type
    # end def gettype
    #// 
    #// Gives any relevant data
    #// 
    #// @codeCoverageIgnore
    #// @return mixed
    #//
    def getdata(self):
        
        return self.data
    # end def getdata
# end class Requests_Exception
