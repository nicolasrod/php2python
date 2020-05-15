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
    response = Array()
    filename = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.6.0
    #// 
    #// @param Requests_Response $response HTTP response.
    #// @param string            $filename Optional. File name. Default empty.
    #//
    def __init__(self, response=None, filename=""):
        
        self.response = response
        self.filename = filename
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
        converted = php_new_class("Requests_Utility_CaseInsensitiveDictionary", lambda : Requests_Utility_CaseInsensitiveDictionary())
        for key,value in self.response.headers.getall():
            if php_count(value) == 1:
                converted[key] = value[0]
            else:
                converted[key] = value
            # end if
        # end for
        return converted
    # end def get_headers
    #// 
    #// Sets all header values.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array $headers Map of header name to header value.
    #//
    def set_headers(self, headers=None):
        
        self.response.headers = php_new_class("Requests_Response_Headers", lambda : Requests_Response_Headers(headers))
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
    def header(self, key=None, value=None, replace=True):
        
        if replace:
            self.response.headers[key] = None
        # end if
        self.response.headers[key] = value
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
    def set_status(self, code=None):
        
        self.response.status_code = absint(code)
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
    def set_data(self, data=None):
        
        self.response.body = data
    # end def set_data
    #// 
    #// Retrieves cookies from the response.
    #// 
    #// @since 4.6.0
    #// 
    #// @return WP_HTTP_Cookie[] List of cookie objects.
    #//
    def get_cookies(self):
        
        cookies = Array()
        for cookie in self.response.cookies:
            cookies[-1] = php_new_class("WP_Http_Cookie", lambda : WP_Http_Cookie(Array({"name": cookie.name, "value": urldecode(cookie.value), "expires": cookie.attributes["expires"] if (php_isset(lambda : cookie.attributes["expires"])) else None, "path": cookie.attributes["path"] if (php_isset(lambda : cookie.attributes["path"])) else None, "domain": cookie.attributes["domain"] if (php_isset(lambda : cookie.attributes["domain"])) else None, "host_only": cookie.flags["host-only"] if (php_isset(lambda : cookie.flags["host-only"])) else None})))
        # end for
        return cookies
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
