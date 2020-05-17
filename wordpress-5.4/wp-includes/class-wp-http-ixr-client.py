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
#// WP_HTTP_IXR_Client
#// 
#// @package WordPress
#// @since 3.1.0
#//
class WP_HTTP_IXR_Client(IXR_Client):
    scheme = Array()
    #// 
    #// @var IXR_Error
    #//
    error = Array()
    #// 
    #// @param string $server
    #// @param string|bool $path
    #// @param int|bool $port
    #// @param int $timeout
    #//
    def __init__(self, server_=None, path_=None, port_=None, timeout_=15):
        if path_ is None:
            path_ = False
        # end if
        if port_ is None:
            port_ = False
        # end if
        
        if (not path_):
            #// Assume we have been given a URL instead.
            bits_ = php_parse_url(server_)
            self.scheme = bits_["scheme"]
            self.server = bits_["host"]
            self.port = bits_["port"] if (php_isset(lambda : bits_["port"])) else port_
            self.path = bits_["path"] if (not php_empty(lambda : bits_["path"])) else "/"
            #// Make absolutely sure we have a path.
            if (not self.path):
                self.path = "/"
            # end if
            if (not php_empty(lambda : bits_["query"])):
                self.path += "?" + bits_["query"]
            # end if
        else:
            self.scheme = "http"
            self.server = server_
            self.path = path_
            self.port = port_
        # end if
        self.useragent = "The Incutio XML-RPC PHP Library"
        self.timeout = timeout_
    # end def __init__
    #// 
    #// @return bool
    #//
    def query(self):
        
        
        args_ = php_func_get_args()
        method_ = php_array_shift(args_)
        request_ = php_new_class("IXR_Request", lambda : IXR_Request(method_, args_))
        xml_ = request_.getxml()
        port_ = str(":") + str(self.port) if self.port else ""
        url_ = self.scheme + "://" + self.server + port_ + self.path
        args_ = Array({"headers": Array({"Content-Type": "text/xml"})}, {"user-agent": self.useragent, "body": xml_})
        #// Merge Custom headers ala #8145.
        for header_,value_ in self.headers:
            args_["headers"][header_] = value_
        # end for
        #// 
        #// Filters the headers collection to be sent to the XML-RPC server.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[] $headers Associative array of headers to be sent.
        #//
        args_["headers"] = apply_filters("wp_http_ixr_client_headers", args_["headers"])
        if False != self.timeout:
            args_["timeout"] = self.timeout
        # end if
        #// Now send the request.
        if self.debug:
            php_print("<pre class=\"ixr_request\">" + htmlspecialchars(xml_) + """
            </pre>
            """)
        # end if
        response_ = wp_remote_post(url_, args_)
        if is_wp_error(response_):
            errno_ = response_.get_error_code()
            errorstr_ = response_.get_error_message()
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32300, str("transport error: ") + str(errno_) + str(" ") + str(errorstr_)))
            return False
        # end if
        if 200 != wp_remote_retrieve_response_code(response_):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32301, "transport error - HTTP status code was not 200 (" + wp_remote_retrieve_response_code(response_) + ")"))
            return False
        # end if
        if self.debug:
            php_print("<pre class=\"ixr_response\">" + htmlspecialchars(wp_remote_retrieve_body(response_)) + """
            </pre>
            """)
        # end if
        #// Now parse what we've got back.
        self.message = php_new_class("IXR_Message", lambda : IXR_Message(wp_remote_retrieve_body(response_)))
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
