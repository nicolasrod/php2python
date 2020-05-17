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
    #// 
    #// HTTP status code
    #// 
    #// @var integer|bool Code if available, false if an error occurred
    #//
    code = 0
    #// 
    #// Reason phrase
    #// 
    #// @var string
    #//
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
    def __init__(self, reason_=None, data_=None):
        if reason_ is None:
            reason_ = None
        # end if
        if data_ is None:
            data_ = None
        # end if
        
        if type(data_).__name__ == "Requests_Response":
            self.code = data_.status_code
        # end if
        super().__init__(reason_, data_)
    # end def __init__
# end class Requests_Exception_HTTP_Unknown
