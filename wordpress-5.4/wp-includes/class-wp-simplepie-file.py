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
    def __init__(self, url=None, timeout=10, redirects=5, headers=None, useragent=None, force_fsockopen=False):
        
        self.url = url
        self.timeout = timeout
        self.redirects = redirects
        self.headers = headers
        self.useragent = useragent
        self.method = SIMPLEPIE_FILE_SOURCE_REMOTE
        if php_preg_match("/^http(s)?:\\/\\//i", url):
            args = Array({"timeout": self.timeout, "redirection": self.redirects})
            if (not php_empty(lambda : self.headers)):
                args["headers"] = self.headers
            # end if
            if SIMPLEPIE_USERAGENT != self.useragent:
                #// Use default WP user agent unless custom has been specified.
                args["user-agent"] = self.useragent
            # end if
            res = wp_safe_remote_request(url, args)
            if is_wp_error(res):
                self.error = "WP HTTP Error: " + res.get_error_message()
                self.success = False
            else:
                self.headers = wp_remote_retrieve_headers(res)
                self.body = wp_remote_retrieve_body(res)
                self.status_code = wp_remote_retrieve_response_code(res)
            # end if
        else:
            self.error = ""
            self.success = False
        # end if
    # end def __init__
# end class WP_SimplePie_File
