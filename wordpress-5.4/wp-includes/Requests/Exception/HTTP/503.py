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
#// Exception for 503 Service Unavailable responses
#// 
#// @package Requests
#// 
#// 
#// Exception for 503 Service Unavailable responses
#// 
#// @package Requests
#//
class Requests_Exception_HTTP_503(Requests_Exception_HTTP):
    #// 
    #// HTTP status code
    #// 
    #// @var integer
    #//
    code = 503
    #// 
    #// Reason phrase
    #// 
    #// @var string
    #//
    reason = "Service Unavailable"
# end class Requests_Exception_HTTP_503
