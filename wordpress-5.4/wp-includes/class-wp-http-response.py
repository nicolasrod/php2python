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
#// HTTP API: WP_HTTP_Response class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 4.4.0
#// 
#// 
#// Core class used to prepare HTTP responses.
#// 
#// @since 4.4.0
#//
class WP_HTTP_Response():
    #// 
    #// Response data.
    #// 
    #// @since 4.4.0
    #// @var mixed
    #//
    data = Array()
    #// 
    #// Response headers.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    headers = Array()
    #// 
    #// Response status.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    status = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.4.0
    #// 
    #// @param mixed $data    Response data. Default null.
    #// @param int   $status  Optional. HTTP status code. Default 200.
    #// @param array $headers Optional. HTTP header map. Default empty array.
    #//
    def __init__(self, data_=None, status_=200, headers_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        
        self.set_data(data_)
        self.set_status(status_)
        self.set_headers(headers_)
    # end def __init__
    #// 
    #// Retrieves headers associated with the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Map of header name to header value.
    #//
    def get_headers(self):
        
        
        return self.headers
    # end def get_headers
    #// 
    #// Sets all header values.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $headers Map of header name to header value.
    #//
    def set_headers(self, headers_=None):
        
        
        self.headers = headers_
    # end def set_headers
    #// 
    #// Sets a single HTTP header.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key     Header name.
    #// @param string $value   Header value.
    #// @param bool   $replace Optional. Whether to replace an existing header of the same name.
    #// Default true.
    #//
    def header(self, key_=None, value_=None, replace_=None):
        if replace_ is None:
            replace_ = True
        # end if
        
        if replace_ or (not (php_isset(lambda : self.headers[key_]))):
            self.headers[key_] = value_
        else:
            self.headers[key_] += ", " + value_
        # end if
    # end def header
    #// 
    #// Retrieves the HTTP return code for the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @return int The 3-digit HTTP status code.
    #//
    def get_status(self):
        
        
        return self.status
    # end def get_status
    #// 
    #// Sets the 3-digit HTTP status code.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int $code HTTP status.
    #//
    def set_status(self, code_=None):
        
        
        self.status = absint(code_)
    # end def set_status
    #// 
    #// Retrieves the response data.
    #// 
    #// @since 4.4.0
    #// 
    #// @return mixed Response data.
    #//
    def get_data(self):
        
        
        return self.data
    # end def get_data
    #// 
    #// Sets the response data.
    #// 
    #// @since 4.4.0
    #// 
    #// @param mixed $data Response data.
    #//
    def set_data(self, data_=None):
        
        
        self.data = data_
    # end def set_data
    #// 
    #// Retrieves the response data for JSON serialization.
    #// 
    #// It is expected that in most implementations, this will return the same as get_data(),
    #// however this may be different if you want to do custom JSON data handling.
    #// 
    #// @since 4.4.0
    #// 
    #// @return mixed Any JSON-serializable value.
    #//
    def jsonserialize(self):
        
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        return self.get_data()
    # end def jsonserialize
# end class WP_HTTP_Response
