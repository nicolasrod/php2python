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
class Requests_Cookie_Jar(ArrayAccessIteratorAggregate):
    #// 
    #// Actual item data
    #// 
    #// @var array
    #//
    cookies = Array()
    #// 
    #// Create a new jar
    #// 
    #// @param array $cookies Existing cookie values
    #//
    def __init__(self, cookies_=None):
        if cookies_ is None:
            cookies_ = Array()
        # end if
        
        self.cookies = cookies_
    # end def __init__
    #// 
    #// Normalise cookie data into a Requests_Cookie
    #// 
    #// @param string|Requests_Cookie $cookie
    #// @return Requests_Cookie
    #//
    def normalize_cookie(self, cookie_=None, key_=None):
        if key_ is None:
            key_ = None
        # end if
        
        if type(cookie_).__name__ == "Requests_Cookie":
            return cookie_
        # end if
        return Requests_Cookie.parse(cookie_, key_)
    # end def normalize_cookie
    #// 
    #// Normalise cookie data into a Requests_Cookie
    #// 
    #// @codeCoverageIgnore
    #// @deprecated Use {@see Requests_Cookie_Jar::normalize_cookie}
    #// @return Requests_Cookie
    #//
    def normalizecookie(self, cookie_=None, key_=None):
        if key_ is None:
            key_ = None
        # end if
        
        return self.normalize_cookie(cookie_, key_)
    # end def normalizecookie
    #// 
    #// Check if the given item exists
    #// 
    #// @param string $key Item key
    #// @return boolean Does the item exist?
    #//
    def offsetexists(self, key_=None):
        
        
        return (php_isset(lambda : self.cookies[key_]))
    # end def offsetexists
    #// 
    #// Get the value for the item
    #// 
    #// @param string $key Item key
    #// @return string Item value
    #//
    def offsetget(self, key_=None):
        
        
        if (not (php_isset(lambda : self.cookies[key_]))):
            return None
        # end if
        return self.cookies[key_]
    # end def offsetget
    #// 
    #// Set the given item
    #// 
    #// @throws Requests_Exception On attempting to use dictionary as list (`invalidset`)
    #// 
    #// @param string $key Item name
    #// @param string $value Item value
    #//
    def offsetset(self, key_=None, value_=None):
        
        
        if key_ == None:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Object is a dictionary, not a list", "invalidset"))
        # end if
        self.cookies[key_] = value_
    # end def offsetset
    #// 
    #// Unset the given header
    #// 
    #// @param string $key
    #//
    def offsetunset(self, key_=None):
        
        
        self.cookies[key_] = None
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
    def register(self, hooks_=None):
        
        
        hooks_.register("requests.before_request", Array(self, "before_request"))
        hooks_.register("requests.before_redirect_check", Array(self, "before_redirect_check"))
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
    def before_request(self, url_=None, headers_=None, data_=None, type_=None, options_=None):
        
        
        if (not type(url_).__name__ == "Requests_IRI"):
            url_ = php_new_class("Requests_IRI", lambda : Requests_IRI(url_))
        # end if
        if (not php_empty(lambda : self.cookies)):
            cookies_ = Array()
            for key_,cookie_ in self.cookies:
                cookie_ = self.normalize_cookie(cookie_, key_)
                #// Skip expired cookies
                if cookie_.is_expired():
                    continue
                # end if
                if cookie_.domain_matches(url_.host):
                    cookies_[-1] = cookie_.format_for_header()
                # end if
            # end for
            headers_["Cookie"] = php_implode("; ", cookies_)
        # end if
    # end def before_request
    #// 
    #// Parse all cookies from a response and attach them to the response
    #// 
    #// @var Requests_Response $response
    #//
    def before_redirect_check(self, return_=None):
        
        
        url_ = return_.url
        if (not type(url_).__name__ == "Requests_IRI"):
            url_ = php_new_class("Requests_IRI", lambda : Requests_IRI(url_))
        # end if
        cookies_ = Requests_Cookie.parse_from_headers(return_.headers, url_)
        self.cookies = php_array_merge(self.cookies, cookies_)
        return_.cookies = self
    # end def before_redirect_check
# end class Requests_Cookie_Jar
