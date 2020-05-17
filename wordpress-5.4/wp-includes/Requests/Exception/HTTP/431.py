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
#// Exception for 431 Request Header Fields Too Large responses
#// 
#// @see https://tools.ietf.org/html/rfc6585
#// @package Requests
#// 
#// 
#// Exception for 431 Request Header Fields Too Large responses
#// 
#// @see https://tools.ietf.org/html/rfc6585
#// @package Requests
#//
class Requests_Exception_HTTP_431(Requests_Exception_HTTP):
    #// 
    #// HTTP status code
    #// 
    #// @var integer
    #//
    code = 431
    #// 
    #// Reason phrase
    #// 
    #// @var string
    #//
    reason = "Request Header Fields Too Large"
# end class Requests_Exception_HTTP_431
