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
#// Basic Authentication provider
#// 
#// @package Requests
#// @subpackage Authentication
#// 
#// 
#// Basic Authentication provider
#// 
#// Provides a handler for Basic HTTP authentication via the Authorization
#// header.
#// 
#// @package Requests
#// @subpackage Authentication
#//
class Requests_Auth_Basic(Requests_Auth):
    user = Array()
    pass_ = Array()
    #// 
    #// Constructor
    #// 
    #// @throws Requests_Exception On incorrect number of arguments (`authbasicbadargs`)
    #// @param array|null $args Array of user and password. Must have exactly two elements
    #//
    def __init__(self, args=None):
        
        if php_is_array(args):
            if php_count(args) != 2:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid number of arguments", "authbasicbadargs"))
            # end if
            self.user, self.pass_ = args
        # end if
    # end def __init__
    #// 
    #// Register the necessary callbacks
    #// 
    #// @see curl_before_send
    #// @see fsockopen_header
    #// @param Requests_Hooks $hooks Hook system
    #//
    def register(self, hooks=None):
        
        hooks.register("curl.before_send", Array(self, "curl_before_send"))
        hooks.register("fsockopen.after_headers", Array(self, "fsockopen_header"))
    # end def register
    #// 
    #// Set cURL parameters before the data is sent
    #// 
    #// @param resource $handle cURL resource
    #//
    def curl_before_send(self, handle=None):
        
        curl_setopt(handle, CURLOPT_HTTPAUTH, CURLAUTH_BASIC)
        curl_setopt(handle, CURLOPT_USERPWD, self.getauthstring())
    # end def curl_before_send
    #// 
    #// Add extra headers to the request before sending
    #// 
    #// @param string $out HTTP header string
    #//
    def fsockopen_header(self, out=None):
        
        out += php_sprintf("Authorization: Basic %s\r\n", php_base64_encode(self.getauthstring()))
    # end def fsockopen_header
    #// 
    #// Get the authentication string (user:pass)
    #// 
    #// @return string
    #//
    def getauthstring(self):
        
        return self.user + ":" + self.pass_
    # end def getauthstring
# end class Requests_Auth_Basic
