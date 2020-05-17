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
#// HTTP API: WP_HTTP_Requests_Response class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 4.6.0
#// 
#// 
#// Core wrapper object for a Requests_Response for standardisation.
#// 
#// @since 4.6.0
#// 
#// @see WP_HTTP_Response
#//
class WP_HTTP_Requests_Response(WP_HTTP_Response):
    #// 
    #// Requests Response object.
    #// 
    #// @since 4.6.0
    #// @var Requests_Response
    #//
    response = Array()
    #// 
    #// Filename the response was saved to.
    #// 
    #// @since 4.6.0
    #// @var string|null
    #//
    filename = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.6.0
    #// 
    #// @param Requests_Response $response HTTP response.
    #// @param string            $filename Optional. File name. Default empty.
    #//
    def __init__(self, response_=None, filename_=""):
        
        
        self.response = response_
        self.filename = filename_
    # end def __init__
    #// 
    #// Retrieves the response object for the request.
    #// 
    #// @since 4.6.0
    #// 
    #// @return Requests_Response HTTP response.
    #//
    def get_response_object(self):
        
        
        return self.response
    # end def get_response_object
    #// 
    #// Retrieves headers associated with the response.
    #// 
    #// @since 4.6.0
    #// 
    #// @return \Requests_Utility_CaseInsensitiveDictionary Map of header name to header value.
    #//
    def get_headers(self):
        
        
        #// Ensure headers remain case-insensitive.
        converted_ = php_new_class("Requests_Utility_CaseInsensitiveDictionary", lambda : Requests_Utility_CaseInsensitiveDictionary())
        for key_,value_ in self.response.headers.getall():
            if php_count(value_) == 1:
                converted_[key_] = value_[0]
            else:
                converted_[key_] = value_
            # end if
        # end for
        return converted_
    # end def get_headers
    #// 
    #// Sets all header values.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array $headers Map of header name to header value.
    #//
    def set_headers(self, headers_=None):
        
        
        self.response.headers = php_new_class("Requests_Response_Headers", lambda : Requests_Response_Headers(headers_))
    # end def set_headers
    #// 
    #// Sets a single HTTP header.
    #// 
    #// @since 4.6.0
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
        
        if replace_:
            self.response.headers[key_] = None
        # end if
        self.response.headers[key_] = value_
    # end def header
    #// 
    #// Retrieves the HTTP return code for the response.
    #// 
    #// @since 4.6.0
    #// 
    #// @return int The 3-digit HTTP status code.
    #//
    def get_status(self):
        
        
        return self.response.status_code
    # end def get_status
    #// 
    #// Sets the 3-digit HTTP status code.
    #// 
    #// @since 4.6.0
    #// 
    #// @param int $code HTTP status.
    #//
    def set_status(self, code_=None):
        
        
        self.response.status_code = absint(code_)
    # end def set_status
    #// 
    #// Retrieves the response data.
    #// 
    #// @since 4.6.0
    #// 
    #// @return string Response data.
    #//
    def get_data(self):
        
        
        return self.response.body
    # end def get_data
    #// 
    #// Sets the response data.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $data Response data.
    #//
    def set_data(self, data_=None):
        
        
        self.response.body = data_
    # end def set_data
    #// 
    #// Retrieves cookies from the response.
    #// 
    #// @since 4.6.0
    #// 
    #// @return WP_HTTP_Cookie[] List of cookie objects.
    #//
    def get_cookies(self):
        
        
        cookies_ = Array()
        for cookie_ in self.response.cookies:
            cookies_[-1] = php_new_class("WP_Http_Cookie", lambda : WP_Http_Cookie(Array({"name": cookie_.name, "value": urldecode(cookie_.value), "expires": cookie_.attributes["expires"] if (php_isset(lambda : cookie_.attributes["expires"])) else None, "path": cookie_.attributes["path"] if (php_isset(lambda : cookie_.attributes["path"])) else None, "domain": cookie_.attributes["domain"] if (php_isset(lambda : cookie_.attributes["domain"])) else None, "host_only": cookie_.flags["host-only"] if (php_isset(lambda : cookie_.flags["host-only"])) else None})))
        # end for
        return cookies_
    # end def get_cookies
    #// 
    #// Converts the object to a WP_Http response array.
    #// 
    #// @since 4.6.0
    #// 
    #// @return array WP_Http response array, per WP_Http::request().
    #//
    def to_array(self):
        
        
        return Array({"headers": self.get_headers(), "body": self.get_data(), "response": Array({"code": self.get_status(), "message": get_status_header_desc(self.get_status())})}, {"cookies": self.get_cookies(), "filename": self.filename})
    # end def to_array
# end class WP_HTTP_Requests_Response
