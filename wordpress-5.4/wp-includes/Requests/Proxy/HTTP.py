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
#// HTTP Proxy connection interface
#// 
#// @package Requests
#// @subpackage Proxy
#// @since 1.6
#// 
#// 
#// HTTP Proxy connection interface
#// 
#// Provides a handler for connection via an HTTP proxy
#// 
#// @package Requests
#// @subpackage Proxy
#// @since 1.6
#//
class Requests_Proxy_HTTP(Requests_Proxy):
    #// 
    #// Proxy host and port
    #// 
    #// Notation: "host:port" (eg 127.0.0.1:8080 or someproxy.com:3128)
    #// 
    #// @var string
    #//
    proxy = Array()
    #// 
    #// Username
    #// 
    #// @var string
    #//
    user = Array()
    #// 
    #// Password
    #// 
    #// @var string
    #//
    pass_ = Array()
    #// 
    #// Do we need to authenticate? (ie username & password have been provided)
    #// 
    #// @var boolean
    #//
    use_authentication = Array()
    #// 
    #// Constructor
    #// 
    #// @since 1.6
    #// @throws Requests_Exception On incorrect number of arguments (`authbasicbadargs`)
    #// @param array|null $args Array of user and password. Must have exactly two elements
    #//
    def __init__(self, args_=None):
        
        
        if php_is_string(args_):
            self.proxy = args_
        elif php_is_array(args_):
            if php_count(args_) == 1:
                self.proxy = args_
            elif php_count(args_) == 3:
                self.proxy, self.user, self.pass_ = args_
                self.use_authentication = True
            else:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid number of arguments", "proxyhttpbadargs"))
            # end if
        # end if
    # end def __init__
    #// 
    #// Register the necessary callbacks
    #// 
    #// @since 1.6
    #// @see curl_before_send
    #// @see fsockopen_remote_socket
    #// @see fsockopen_remote_host_path
    #// @see fsockopen_header
    #// @param Requests_Hooks $hooks Hook system
    #//
    def register(self, hooks_=None):
        
        
        hooks_.register("curl.before_send", Array(self, "curl_before_send"))
        hooks_.register("fsockopen.remote_socket", Array(self, "fsockopen_remote_socket"))
        hooks_.register("fsockopen.remote_host_path", Array(self, "fsockopen_remote_host_path"))
        if self.use_authentication:
            hooks_.register("fsockopen.after_headers", Array(self, "fsockopen_header"))
        # end if
    # end def register
    #// 
    #// Set cURL parameters before the data is sent
    #// 
    #// @since 1.6
    #// @param resource $handle cURL resource
    #//
    def curl_before_send(self, handle_=None):
        
        
        curl_setopt(handle_, CURLOPT_PROXYTYPE, CURLPROXY_HTTP)
        curl_setopt(handle_, CURLOPT_PROXY, self.proxy)
        if self.use_authentication:
            curl_setopt(handle_, CURLOPT_PROXYAUTH, CURLAUTH_ANY)
            curl_setopt(handle_, CURLOPT_PROXYUSERPWD, self.get_auth_string())
        # end if
    # end def curl_before_send
    #// 
    #// Alter remote socket information before opening socket connection
    #// 
    #// @since 1.6
    #// @param string $remote_socket Socket connection string
    #//
    def fsockopen_remote_socket(self, remote_socket_=None):
        
        
        remote_socket_ = self.proxy
    # end def fsockopen_remote_socket
    #// 
    #// Alter remote path before getting stream data
    #// 
    #// @since 1.6
    #// @param string $path Path to send in HTTP request string ("GET ...")
    #// @param string $url Full URL we're requesting
    #//
    def fsockopen_remote_host_path(self, path_=None, url_=None):
        
        
        path_ = url_
    # end def fsockopen_remote_host_path
    #// 
    #// Add extra headers to the request before sending
    #// 
    #// @since 1.6
    #// @param string $out HTTP header string
    #//
    def fsockopen_header(self, out_=None):
        
        
        out_ += php_sprintf("Proxy-Authorization: Basic %s\r\n", php_base64_encode(self.get_auth_string()))
    # end def fsockopen_header
    #// 
    #// Get the authentication string (user:pass)
    #// 
    #// @since 1.6
    #// @return string
    #//
    def get_auth_string(self):
        
        
        return self.user + ":" + self.pass_
    # end def get_auth_string
# end class Requests_Proxy_HTTP
