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
    code = 431
    reason = "Request Header Fields Too Large"
# end class Requests_Exception_HTTP_431
