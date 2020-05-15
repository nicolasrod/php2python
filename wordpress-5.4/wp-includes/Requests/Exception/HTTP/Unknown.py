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
#// Exception for unknown status responses
#// 
#// @package Requests
#// 
#// 
#// Exception for unknown status responses
#// 
#// @package Requests
#//
class Requests_Exception_HTTP_Unknown(Requests_Exception_HTTP):
    code = 0
    reason = "Unknown"
    #// 
    #// Create a new exception
    #// 
    #// If `$data` is an instance of {@see Requests_Response}, uses the status
    #// code from it. Otherwise, sets as 0
    #// 
    #// @param string|null $reason Reason phrase
    #// @param mixed $data Associated data
    #//
    def __init__(self, reason=None, data=None):
        
        if type(data).__name__ == "Requests_Response":
            self.code = data.status_code
        # end if
        super().__init__(reason, data)
    # end def __init__
# end class Requests_Exception_HTTP_Unknown
