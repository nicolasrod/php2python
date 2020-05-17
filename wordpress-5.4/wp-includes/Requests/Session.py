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
    #// 
    #// Base URL for requests
    #// 
    #// URLs will be made absolute using this as the base
    #// @var string|null
    #//
    url = None
    #// 
    #// Base headers for requests
    #// @var array
    #//
    headers = Array()
    #// 
    #// Base data for requests
    #// 
    #// If both the base data and the per-request data are arrays, the data will
    #// be merged before sending the request.
    #// 
    #// @var array
    #//
    data = Array()
    #// 
    #// Base options for requests
    #// 
    #// The base options are merged with the per-request data for each request.
    #// The only default option is a shared cookie jar between requests.
    #// 
    #// Values here can also be set directly via properties on the Session
    #// object, e.g. `$session->useragent = 'X';`
    #// 
    #// @var array
    #//
    options = Array()
    #// 
    #// Create a new session
    #// 
    #// @param string|null $url Base URL for requests
    #// @param array $headers Default headers for requests
    #// @param array $data Default data for requests
    #// @param array $options Default options for requests
    #//
    def __init__(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        self.url = url_
        self.headers = headers_
        self.data = data_
        self.options = options_
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
    def __get(self, key_=None):
        
        
        if (php_isset(lambda : self.options[key_])):
            return self.options[key_]
        # end if
        return None
    # end def __get
    #// 
    #// Set a property's value
    #// 
    #// @param string $key Property key
    #// @param mixed $value Property value
    #//
    def __set(self, key_=None, value_=None):
        
        
        self.options[key_] = value_
    # end def __set
    #// 
    #// Remove a property's value
    #// 
    #// @param string $key Property key
    #//
    def __isset(self, key_=None):
        
        
        return (php_isset(lambda : self.options[key_]))
    # end def __isset
    #// 
    #// Remove a property's value
    #// 
    #// @param string $key Property key
    #//
    def __unset(self, key_=None):
        
        
        if (php_isset(lambda : self.options[key_])):
            self.options[key_] = None
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
    def get(self, url_=None, headers_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, None, Requests.GET, options_)
    # end def get
    #// 
    #// Send a HEAD request
    #//
    def head(self, url_=None, headers_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, None, Requests.HEAD, options_)
    # end def head
    #// 
    #// Send a DELETE request
    #//
    def delete(self, url_=None, headers_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, None, Requests.DELETE, options_)
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
    def post(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, data_, Requests.POST, options_)
    # end def post
    #// 
    #// Send a PUT request
    #//
    def put(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, data_, Requests.PUT, options_)
    # end def put
    #// 
    #// Send a PATCH request
    #// 
    #// Note: Unlike {@see post} and {@see put}, `$headers` is required, as the
    #// specification recommends that should send an ETag
    #// 
    #// @link https://tools.ietf.org/html/rfc5789
    #//
    def patch(self, url_=None, headers_=None, data_=None, options_=None):
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, data_, Requests.PATCH, options_)
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
    def request(self, url_=None, headers_=None, data_=None, type_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if type_ is None:
            type_ = Requests.GET
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        request_ = self.merge_request(php_compact("url", "headers", "data", "options"))
        return Requests.request(request_["url"], request_["headers"], request_["data"], type_, request_["options"])
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
    def request_multiple(self, requests_=None, options_=None):
        if options_ is None:
            options_ = Array()
        # end if
        
        for key_,request_ in requests_:
            requests_[key_] = self.merge_request(request_, False)
        # end for
        options_ = php_array_merge(self.options, options_)
        options_["type"] = None
        return Requests.request_multiple(requests_, options_)
    # end def request_multiple
    #// 
    #// Merge a request's data with the default data
    #// 
    #// @param array $request Request data (same form as {@see request_multiple})
    #// @param boolean $merge_options Should we merge options as well?
    #// @return array Request data
    #//
    def merge_request(self, request_=None, merge_options_=None):
        if merge_options_ is None:
            merge_options_ = True
        # end if
        
        if self.url != None:
            request_["url"] = Requests_IRI.absolutize(self.url, request_["url"])
            request_["url"] = request_["url"].uri
        # end if
        if php_empty(lambda : request_["headers"]):
            request_["headers"] = Array()
        # end if
        request_["headers"] = php_array_merge(self.headers, request_["headers"])
        if php_empty(lambda : request_["data"]):
            if php_is_array(self.data):
                request_["data"] = self.data
            # end if
        elif php_is_array(request_["data"]) and php_is_array(self.data):
            request_["data"] = php_array_merge(self.data, request_["data"])
        # end if
        if merge_options_ != False:
            request_["options"] = php_array_merge(self.options, request_["options"])
            request_["options"]["type"] = None
        # end if
        return request_
    # end def merge_request
# end class Requests_Session
