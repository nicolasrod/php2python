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
class Requests_Exception_Transport_cURL(Requests_Exception_Transport):
    EASY = "cURLEasy"
    MULTI = "cURLMulti"
    SHARE = "cURLShare"
    code = -1
    type = "Unknown"
    reason = "Unknown"
    def __init__(self, message=None, type=None, data=None, code=0):
        
        if type != None:
            self.type = type
        # end if
        if code != None:
            self.code = code
        # end if
        if message != None:
            self.reason = message
        # end if
        message = php_sprintf("%d %s", self.code, self.reason)
        super().__init__(message, self.type, data, self.code)
    # end def __init__
    #// 
    #// Get the error message
    #//
    def getreason(self):
        
        return self.reason
    # end def getreason
# end class Requests_Exception_Transport_cURL
