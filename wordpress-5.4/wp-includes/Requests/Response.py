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
#// HTTP response class
#// 
#// Contains a response from Requests::request()
#// @package Requests
#// 
#// 
#// HTTP response class
#// 
#// Contains a response from Requests::request()
#// @package Requests
#//
class Requests_Response():
    #// 
    #// Constructor
    #//
    def __init__(self):
        
        self.headers = php_new_class("Requests_Response_Headers", lambda : Requests_Response_Headers())
        self.cookies = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar())
    # end def __init__
    body = ""
    raw = ""
    headers = Array()
    status_code = False
    protocol_version = False
    success = False
    redirects = 0
    url = ""
    history = Array()
    cookies = Array()
    #// 
    #// Is the response a redirect?
    #// 
    #// @return boolean True if redirect (3xx status), false if not.
    #//
    def is_redirect(self):
        
        code = self.status_code
        return php_in_array(code, Array(300, 301, 302, 303, 307)) or code > 307 and code < 400
    # end def is_redirect
    #// 
    #// Throws an exception if the request was not successful
    #// 
    #// @throws Requests_Exception If `$allow_redirects` is false, and code is 3xx (`response.no_redirects`)
    #// @throws Requests_Exception_HTTP On non-successful status code. Exception class corresponds to code (e.g. {@see Requests_Exception_HTTP_404})
    #// @param boolean $allow_redirects Set to false to throw on a 3xx as well
    #//
    def throw_for_status(self, allow_redirects=True):
        
        if self.is_redirect():
            if (not allow_redirects):
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Redirection not allowed", "response.no_redirects", self))
            # end if
        elif (not self.success):
            exception = Requests_Exception_HTTP.get_class(self.status_code)
            raise php_new_class(exception, lambda : {**locals(), **globals()}[exception](None, self))
        # end if
    # end def throw_for_status
# end class Requests_Response
