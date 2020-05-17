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
#// Base HTTP transport
#// 
#// @package Requests
#// @subpackage Transport
#// 
#// 
#// Base HTTP transport
#// 
#// @package Requests
#// @subpackage Transport
#//
class Requests_Transport():
    #// 
    #// Perform a request
    #// 
    #// @param string $url URL to request
    #// @param array $headers Associative array of request headers
    #// @param string|array $data Data to send either as the POST body, or as parameters in the URL for a GET/HEAD
    #// @param array $options Request options, see {@see Requests::response()} for documentation
    #// @return string Raw HTTP result
    #//
    def request(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        pass
    # end def request
    #// 
    #// Send multiple requests simultaneously
    #// 
    #// @param array $requests Request data (array of 'url', 'headers', 'data', 'options') as per {@see Requests_Transport::request}
    #// @param array $options Global options, see {@see Requests::response()} for documentation
    #// @return array Array of Requests_Response objects (may contain Requests_Exception or string responses as well)
    #//
    def request_multiple(self, requests_=None, options_=None):
        
        
        pass
    # end def request_multiple
    #// 
    #// Self-test whether the transport can be used
    #// @return bool
    #//
    @classmethod
    def test(self):
        
        
        pass
    # end def test
# end class Requests_Transport
