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
#// Exception based on HTTP response
#// 
#// @package Requests
#// 
#// 
#// Exception based on HTTP response
#// 
#// @package Requests
#//
class Requests_Exception_HTTP(Requests_Exception):
    code = 0
    reason = "Unknown"
    #// 
    #// Create a new exception
    #// 
    #// There is no mechanism to pass in the status code, as this is set by the
    #// subclass used. Reason phrases can vary, however.
    #// 
    #// @param string|null $reason Reason phrase
    #// @param mixed $data Associated data
    #//
    def __init__(self, reason=None, data=None):
        
        if reason != None:
            self.reason = reason
        # end if
        message = php_sprintf("%d %s", self.code, self.reason)
        super().__init__(message, "httpresponse", data, self.code)
    # end def __init__
    #// 
    #// Get the status message
    #//
    def getreason(self):
        
        return self.reason
    # end def getreason
    #// 
    #// Get the correct exception class for a given error code
    #// 
    #// @param int|bool $code HTTP status code, or false if unavailable
    #// @return string Exception class name to use
    #//
    @classmethod
    def get_class(self, code=None):
        
        if (not code):
            return "Requests_Exception_HTTP_Unknown"
        # end if
        class_ = php_sprintf("Requests_Exception_HTTP_%d", code)
        if php_class_exists(class_):
            return class_
        # end if
        return "Requests_Exception_HTTP_Unknown"
    # end def get_class
# end class Requests_Exception_HTTP
