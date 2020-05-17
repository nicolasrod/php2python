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
#// Feed API: WP_SimplePie_File class
#// 
#// @package WordPress
#// @subpackage Feed
#// @since 4.7.0
#// 
#// 
#// Core class for fetching remote files and reading local files with SimplePie.
#// 
#// @since 2.8.0
#// 
#// @see SimplePie_File
#//
class WP_SimplePie_File(SimplePie_File):
    #// 
    #// Constructor.
    #// 
    #// @since 2.8.0
    #// @since 3.2.0 Updated to use a PHP5 constructor.
    #// 
    #// @param string       $url             Remote file URL.
    #// @param integer      $timeout         Optional. How long the connection should stay open in seconds.
    #// Default 10.
    #// @param integer      $redirects       Optional. The number of allowed redirects. Default 5.
    #// @param string|array $headers         Optional. Array or string of headers to send with the request.
    #// Default null.
    #// @param string       $useragent       Optional. User-agent value sent. Default null.
    #// @param boolean      $force_fsockopen Optional. Whether to force opening internet or unix domain socket
    #// connection or not. Default false.
    #//
    def __init__(self, url_=None, timeout_=10, redirects_=5, headers_=None, useragent_=None, force_fsockopen_=None):
        if force_fsockopen_ is None:
            force_fsockopen_ = False
        # end if
        
        self.url = url_
        self.timeout = timeout_
        self.redirects = redirects_
        self.headers = headers_
        self.useragent = useragent_
        self.method = SIMPLEPIE_FILE_SOURCE_REMOTE
        if php_preg_match("/^http(s)?:\\/\\//i", url_):
            args_ = Array({"timeout": self.timeout, "redirection": self.redirects})
            if (not php_empty(lambda : self.headers)):
                args_["headers"] = self.headers
            # end if
            if SIMPLEPIE_USERAGENT != self.useragent:
                #// Use default WP user agent unless custom has been specified.
                args_["user-agent"] = self.useragent
            # end if
            res_ = wp_safe_remote_request(url_, args_)
            if is_wp_error(res_):
                self.error = "WP HTTP Error: " + res_.get_error_message()
                self.success = False
            else:
                self.headers = wp_remote_retrieve_headers(res_)
                self.body = wp_remote_retrieve_body(res_)
                self.status_code = wp_remote_retrieve_response_code(res_)
            # end if
        else:
            self.error = ""
            self.success = False
        # end if
    # end def __init__
# end class WP_SimplePie_File
