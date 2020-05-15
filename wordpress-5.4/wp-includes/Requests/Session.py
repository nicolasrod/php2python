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
#// Session handler for persistent requests and default parameters
#// 
#// @package Requests
#// @subpackage Session Handler
#// 
#// 
#// Session handler for persistent requests and default parameters
#// 
#// Allows various options to be set as default values, and merges both the
#// options and URL properties together. A base URL can be set for all requests,
#// with all subrequests resolved from this. Base options can be set (including
#// a shared cookie jar), then overridden for individual requests.
#// 
#// @package Requests
#// @subpackage Session Handler
#//
class Requests_Session():
    url = None
    headers = Array()
    data = Array()
    options = Array()
    #// 
    #// Create a new session
    #// 
    #// @param string|null $url Base URL for requests
    #// @param array $headers Default headers for requests
    #// @param array $data Default data for requests
    #// @param array $options Default options for requests
    #//
    def __init__(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        self.url = url
        self.headers = headers
        self.data = data
        self.options = options
        if php_empty(lambda : self.options["cookies"]):
            self.options["cookies"] = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar())
        # end if
    # end def __init__
    #// 
    #// Get a property's value
    #// 
    #// @param string $key Property key
    #// @return mixed|null Property value, null if none found
    #//
    def __get(self, key=None):
        
        if (php_isset(lambda : self.options[key])):
            return self.options[key]
        # end if
        return None
    # end def __get
    #// 
    #// Set a property's value
    #// 
    #// @param string $key Property key
    #// @param mixed $value Property value
    #//
    def __set(self, key=None, value=None):
        
        self.options[key] = value
    # end def __set
    #// 
    #// Remove a property's value
    #// 
    #// @param string $key Property key
    #//
    def __isset(self, key=None):
        
        return (php_isset(lambda : self.options[key]))
    # end def __isset
    #// 
    #// Remove a property's value
    #// 
    #// @param string $key Property key
    #//
    def __unset(self, key=None):
        
        if (php_isset(lambda : self.options[key])):
            self.options[key] = None
        # end if
    # end def __unset
    #// #@+
    #// @see request()
    #// @param string $url
    #// @param array $headers
    #// @param array $options
    #// @return Requests_Response
    #// 
    #// 
    #// Send a GET request
    #//
    def get(self, url=None, headers=Array(), options=Array()):
        
        return self.request(url, headers, None, Requests.GET, options)
    # end def get
    #// 
    #// Send a HEAD request
    #//
    def head(self, url=None, headers=Array(), options=Array()):
        
        return self.request(url, headers, None, Requests.HEAD, options)
    # end def head
    #// 
    #// Send a DELETE request
    #//
    def delete(self, url=None, headers=Array(), options=Array()):
        
        return self.request(url, headers, None, Requests.DELETE, options)
    # end def delete
    #// #@-
    #// #@+
    #// @see request()
    #// @param string $url
    #// @param array $headers
    #// @param array $data
    #// @param array $options
    #// @return Requests_Response
    #// 
    #// 
    #// Send a POST request
    #//
    def post(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        return self.request(url, headers, data, Requests.POST, options)
    # end def post
    #// 
    #// Send a PUT request
    #//
    def put(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        return self.request(url, headers, data, Requests.PUT, options)
    # end def put
    #// 
    #// Send a PATCH request
    #// 
    #// Note: Unlike {@see post} and {@see put}, `$headers` is required, as the
    #// specification recommends that should send an ETag
    #// 
    #// @link https://tools.ietf.org/html/rfc5789
    #//
    def patch(self, url=None, headers=None, data=Array(), options=Array()):
        
        return self.request(url, headers, data, Requests.PATCH, options)
    # end def patch
    #// #@-
    #// 
    #// Main interface for HTTP requests
    #// 
    #// This method initiates a request and sends it via a transport before
    #// parsing.
    #// 
    #// @see Requests::request()
    #// 
    #// @throws Requests_Exception On invalid URLs (`nonhttp`)
    #// 
    #// @param string $url URL to request
    #// @param array $headers Extra headers to send with the request
    #// @param array|null $data Data to send either as a query string for GET/HEAD requests, or in the body for POST requests
    #// @param string $type HTTP request type (use Requests constants)
    #// @param array $options Options for the request (see {@see Requests::request})
    #// @return Requests_Response
    #//
    def request(self, url=None, headers=Array(), data=Array(), type=Requests.GET, options=Array()):
        
        request = self.merge_request(compact("url", "headers", "data", "options"))
        return Requests.request(request["url"], request["headers"], request["data"], type, request["options"])
    # end def request
    #// 
    #// Send multiple HTTP requests simultaneously
    #// 
    #// @see Requests::request_multiple()
    #// 
    #// @param array $requests Requests data (see {@see Requests::request_multiple})
    #// @param array $options Global and default options (see {@see Requests::request})
    #// @return array Responses (either Requests_Response or a Requests_Exception object)
    #//
    def request_multiple(self, requests=None, options=Array()):
        
        for key,request in requests:
            requests[key] = self.merge_request(request, False)
        # end for
        options = php_array_merge(self.options, options)
        options["type"] = None
        return Requests.request_multiple(requests, options)
    # end def request_multiple
    #// 
    #// Merge a request's data with the default data
    #// 
    #// @param array $request Request data (same form as {@see request_multiple})
    #// @param boolean $merge_options Should we merge options as well?
    #// @return array Request data
    #//
    def merge_request(self, request=None, merge_options=True):
        
        if self.url != None:
            request["url"] = Requests_IRI.absolutize(self.url, request["url"])
            request["url"] = request["url"].uri
        # end if
        if php_empty(lambda : request["headers"]):
            request["headers"] = Array()
        # end if
        request["headers"] = php_array_merge(self.headers, request["headers"])
        if php_empty(lambda : request["data"]):
            if php_is_array(self.data):
                request["data"] = self.data
            # end if
        elif php_is_array(request["data"]) and php_is_array(self.data):
            request["data"] = php_array_merge(self.data, request["data"])
        # end if
        if merge_options != False:
            request["options"] = php_array_merge(self.options, request["options"])
            request["options"]["type"] = None
        # end if
        return request
    # end def merge_request
# end class Requests_Session
