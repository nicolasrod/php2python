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
#// Exception for 413 Request Entity Too Large responses
#// 
#// @package Requests
#// 
#// 
#// Exception for 413 Request Entity Too Large responses
#// 
#// @package Requests
#//
class Requests_Exception_HTTP_413(Requests_Exception_HTTP):
    #// 
    #// HTTP status code
    #// 
    #// @var integer
    #//
    code = 413
    #// 
    #// Reason phrase
    #// 
    #// @var string
    #//
    reason = "Request Entity Too Large"
# end class Requests_Exception_HTTP_413
