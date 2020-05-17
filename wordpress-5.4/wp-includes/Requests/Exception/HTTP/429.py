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
#// Exception for 429 Too Many Requests responses
#// 
#// @see https://tools.ietf.org/html/draft-nottingham-http-new-status-04
#// @package Requests
#// 
#// 
#// Exception for 429 Too Many Requests responses
#// 
#// @see https://tools.ietf.org/html/draft-nottingham-http-new-status-04
#// @package Requests
#//
class Requests_Exception_HTTP_429(Requests_Exception_HTTP):
    #// 
    #// HTTP status code
    #// 
    #// @var integer
    #//
    code = 429
    #// 
    #// Reason phrase
    #// 
    #// @var string
    #//
    reason = "Too Many Requests"
# end class Requests_Exception_HTTP_429
