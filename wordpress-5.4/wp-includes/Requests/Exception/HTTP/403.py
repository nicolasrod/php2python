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
#// Exception for 403 Forbidden responses
#// 
#// @package Requests
#// 
#// 
#// Exception for 403 Forbidden responses
#// 
#// @package Requests
#//
class Requests_Exception_HTTP_403(Requests_Exception_HTTP):
    code = 403
    reason = "Forbidden"
# end class Requests_Exception_HTTP_403
