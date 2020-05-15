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
#// Cookie holder object
#// 
#// @package Requests
#// @subpackage Cookies
#// 
#// 
#// Cookie holder object
#// 
#// @package Requests
#// @subpackage Cookies
#//
class Requests_Cookie_Jar():
    cookies = Array()
    #// 
    #// Create a new jar
    #// 
    #// @param array $cookies Existing cookie values
    #//
    def __init__(self, cookies=Array()):
        
        self.cookies = cookies
    # end def __init__
    #// 
    #// Normalise cookie data into a Requests_Cookie
    #// 
    #// @param string|Requests_Cookie $cookie
    #// @return Requests_Cookie
    #//
    def normalize_cookie(self, cookie=None, key=None):
        
        if type(cookie).__name__ == "Requests_Cookie":
            return cookie
        # end if
        return Requests_Cookie.parse(cookie, key)
    # end def normalize_cookie
    #// 
    #// Normalise cookie data into a Requests_Cookie
    #// 
    #// @codeCoverageIgnore
    #// @deprecated Use {@see Requests_Cookie_Jar::normalize_cookie}
    #// @return Requests_Cookie
    #//
    def normalizecookie(self, cookie=None, key=None):
        
        return self.normalize_cookie(cookie, key)
    # end def normalizecookie
    #// 
    #// Check if the given item exists
    #// 
    #// @param string $key Item key
    #// @return boolean Does the item exist?
    #//
    def offsetexists(self, key=None):
        
        return (php_isset(lambda : self.cookies[key]))
    # end def offsetexists
    #// 
    #// Get the value for the item
    #// 
    #// @param string $key Item key
    #// @return string Item value
    #//
    def offsetget(self, key=None):
        
        if (not (php_isset(lambda : self.cookies[key]))):
            return None
        # end if
        return self.cookies[key]
    # end def offsetget
    #// 
    #// Set the given item
    #// 
    #// @throws Requests_Exception On attempting to use dictionary as list (`invalidset`)
    #// 
    #// @param string $key Item name
    #// @param string $value Item value
    #//
    def offsetset(self, key=None, value=None):
        
        if key == None:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Object is a dictionary, not a list", "invalidset"))
        # end if
        self.cookies[key] = value
    # end def offsetset
    #// 
    #// Unset the given header
    #// 
    #// @param string $key
    #//
    def offsetunset(self, key=None):
        
        self.cookies[key] = None
    # end def offsetunset
    #// 
    #// Get an iterator for the data
    #// 
    #// @return ArrayIterator
    #//
    def getiterator(self):
        
        return php_new_class("ArrayIterator", lambda : ArrayIterator(self.cookies))
    # end def getiterator
    #// 
    #// Register the cookie handler with the request's hooking system
    #// 
    #// @param Requests_Hooker $hooks Hooking system
    #//
    def register(self, hooks=None):
        
        hooks.register("requests.before_request", Array(self, "before_request"))
        hooks.register("requests.before_redirect_check", Array(self, "before_redirect_check"))
    # end def register
    #// 
    #// Add Cookie header to a request if we have any
    #// 
    #// As per RFC 6265, cookies are separated by '; '
    #// 
    #// @param string $url
    #// @param array $headers
    #// @param array $data
    #// @param string $type
    #// @param array $options
    #//
    def before_request(self, url=None, headers=None, data=None, type=None, options=None):
        
        if (not type(url).__name__ == "Requests_IRI"):
            url = php_new_class("Requests_IRI", lambda : Requests_IRI(url))
        # end if
        if (not php_empty(lambda : self.cookies)):
            cookies = Array()
            for key,cookie in self.cookies:
                cookie = self.normalize_cookie(cookie, key)
                #// Skip expired cookies
                if cookie.is_expired():
                    continue
                # end if
                if cookie.domain_matches(url.host):
                    cookies[-1] = cookie.format_for_header()
                # end if
            # end for
            headers["Cookie"] = php_implode("; ", cookies)
        # end if
    # end def before_request
    #// 
    #// Parse all cookies from a response and attach them to the response
    #// 
    #// @var Requests_Response $response
    #//
    def before_redirect_check(self, return_=None):
        
        url = return_.url
        if (not type(url).__name__ == "Requests_IRI"):
            url = php_new_class("Requests_IRI", lambda : Requests_IRI(url))
        # end if
        cookies = Requests_Cookie.parse_from_headers(return_.headers, url)
        self.cookies = php_array_merge(self.cookies, cookies)
        return_.cookies = self
    # end def before_redirect_check
# end class Requests_Cookie_Jar
