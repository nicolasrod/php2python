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
#// WP_HTTP_IXR_Client
#// 
#// @package WordPress
#// @since 3.1.0
#//
class WP_HTTP_IXR_Client(IXR_Client):
    scheme = Array()
    error = Array()
    #// 
    #// @param string $server
    #// @param string|bool $path
    #// @param int|bool $port
    #// @param int $timeout
    #//
    def __init__(self, server=None, path=False, port=False, timeout=15):
        
        if (not path):
            #// Assume we have been given a URL instead.
            bits = php_parse_url(server)
            self.scheme = bits["scheme"]
            self.server = bits["host"]
            self.port = bits["port"] if (php_isset(lambda : bits["port"])) else port
            self.path = bits["path"] if (not php_empty(lambda : bits["path"])) else "/"
            #// Make absolutely sure we have a path.
            if (not self.path):
                self.path = "/"
            # end if
            if (not php_empty(lambda : bits["query"])):
                self.path += "?" + bits["query"]
            # end if
        else:
            self.scheme = "http"
            self.server = server
            self.path = path
            self.port = port
        # end if
        self.useragent = "The Incutio XML-RPC PHP Library"
        self.timeout = timeout
    # end def __init__
    #// 
    #// @return bool
    #//
    def query(self):
        
        args = php_func_get_args()
        method = php_array_shift(args)
        request = php_new_class("IXR_Request", lambda : IXR_Request(method, args))
        xml = request.getxml()
        port = str(":") + str(self.port) if self.port else ""
        url = self.scheme + "://" + self.server + port + self.path
        args = Array({"headers": Array({"Content-Type": "text/xml"})}, {"user-agent": self.useragent, "body": xml})
        #// Merge Custom headers ala #8145.
        for header,value in self.headers:
            args["headers"][header] = value
        # end for
        #// 
        #// Filters the headers collection to be sent to the XML-RPC server.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[] $headers Associative array of headers to be sent.
        #//
        args["headers"] = apply_filters("wp_http_ixr_client_headers", args["headers"])
        if False != self.timeout:
            args["timeout"] = self.timeout
        # end if
        #// Now send the request.
        if self.debug:
            php_print("<pre class=\"ixr_request\">" + htmlspecialchars(xml) + """
            </pre>
            """)
        # end if
        response = wp_remote_post(url, args)
        if is_wp_error(response):
            errno = response.get_error_code()
            errorstr = response.get_error_message()
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32300, str("transport error: ") + str(errno) + str(" ") + str(errorstr)))
            return False
        # end if
        if 200 != wp_remote_retrieve_response_code(response):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32301, "transport error - HTTP status code was not 200 (" + wp_remote_retrieve_response_code(response) + ")"))
            return False
        # end if
        if self.debug:
            php_print("<pre class=\"ixr_response\">" + htmlspecialchars(wp_remote_retrieve_body(response)) + """
            </pre>
            """)
        # end if
        #// Now parse what we've got back.
        self.message = php_new_class("IXR_Message", lambda : IXR_Message(wp_remote_retrieve_body(response)))
        if (not self.message.parse()):
            #// XML error.
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32700, "parse error. not well formed"))
            return False
        # end if
        #// Is the message a fault?
        if "fault" == self.message.messageType:
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(self.message.faultCode, self.message.faultString))
            return False
        # end if
        #// Message must be OK.
        return True
    # end def query
# end class WP_HTTP_IXR_Client
