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
#// Exception for 418 I'm A Teapot responses
#// 
#// @see https://tools.ietf.org/html/rfc2324
#// @package Requests
#// 
#// 
#// Exception for 418 I'm A Teapot responses
#// 
#// @see https://tools.ietf.org/html/rfc2324
#// @package Requests
#//
class Requests_Exception_HTTP_418(Requests_Exception_HTTP):
    #// 
    #// HTTP status code
    #// 
    #// @var integer
    #//
    code = 418
    #// 
    #// Reason phrase
    #// 
    #// @var string
    #//
    reason = "I'm A Teapot"
# end class Requests_Exception_HTTP_418
