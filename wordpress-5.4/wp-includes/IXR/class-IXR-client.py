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
#// IXR_Client
#// 
#// @package IXR
#// @since 1.5.0
#// 
#//
class IXR_Client():
    server = Array()
    port = Array()
    path = Array()
    useragent = Array()
    response = Array()
    message = False
    debug = False
    timeout = Array()
    headers = Array()
    #// Storage place for an error message
    error = False
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, server_=None, path_=None, port_=80, timeout_=15):
        if path_ is None:
            path_ = False
        # end if
        
        if (not path_):
            #// Assume we have been given a URL instead
            bits_ = php_parse_url(server_)
            self.server = bits_["host"]
            self.port = bits_["port"] if (php_isset(lambda : bits_["port"])) else 80
            self.path = bits_["path"] if (php_isset(lambda : bits_["path"])) else "/"
            #// Make absolutely sure we have a path
            if (not self.path):
                self.path = "/"
            # end if
            if (not php_empty(lambda : bits_["query"])):
                self.path += "?" + bits_["query"]
            # end if
        else:
            self.server = server_
            self.path = path_
            self.port = port_
        # end if
        self.useragent = "The Incutio XML-RPC PHP Library"
        self.timeout = timeout_
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_client(self, server_=None, path_=None, port_=80, timeout_=15):
        if path_ is None:
            path_ = False
        # end if
        
        self.__init__(server_, path_, port_, timeout_)
    # end def ixr_client
    def query(self):
        
        
        args_ = php_func_get_args()
        method_ = php_array_shift(args_)
        request_ = php_new_class("IXR_Request", lambda : IXR_Request(method_, args_))
        length_ = request_.getlength()
        xml_ = request_.getxml()
        r_ = "\r\n"
        request_ = str("POST ") + str(self.path) + str(" HTTP/1.0") + str(r_)
        #// Merged from WP #8145 - allow custom headers
        self.headers["Host"] = self.server
        self.headers["Content-Type"] = "text/xml"
        self.headers["User-Agent"] = self.useragent
        self.headers["Content-Length"] = length_
        for header_,value_ in self.headers.items():
            request_ += str(header_) + str(": ") + str(value_) + str(r_)
        # end for
        request_ += r_
        request_ += xml_
        #// Now send the request
        if self.debug:
            php_print("<pre class=\"ixr_request\">" + php_htmlspecialchars(request_) + """
            </pre>
            """)
        # end if
        if self.timeout:
            fp_ = php_no_error(lambda: fsockopen(self.server, self.port, errno_, errstr_, self.timeout))
        else:
            fp_ = php_no_error(lambda: fsockopen(self.server, self.port, errno_, errstr_))
        # end if
        if (not fp_):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32300, "transport error - could not open socket"))
            return False
        # end if
        fputs(fp_, request_)
        contents_ = ""
        debugContents_ = ""
        gotFirstLine_ = False
        gettingHeaders_ = True
        while True:
            
            if not ((not php_feof(fp_))):
                break
            # end if
            line_ = php_fgets(fp_, 4096)
            if (not gotFirstLine_):
                #// Check line for '200'
                if php_strstr(line_, "200") == False:
                    self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32300, "transport error - HTTP status code was not 200"))
                    return False
                # end if
                gotFirstLine_ = True
            # end if
            if php_trim(line_) == "":
                gettingHeaders_ = False
            # end if
            if (not gettingHeaders_):
                #// merged from WP #12559 - remove trim
                contents_ += line_
            # end if
            if self.debug:
                debugContents_ += line_
            # end if
        # end while
        if self.debug:
            php_print("<pre class=\"ixr_response\">" + php_htmlspecialchars(debugContents_) + """
            </pre>
            """)
        # end if
        #// Now parse what we've got back
        self.message = php_new_class("IXR_Message", lambda : IXR_Message(contents_))
        if (not self.message.parse()):
            #// XML error
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32700, "parse error. not well formed"))
            return False
        # end if
        #// Is the message a fault?
        if self.message.messageType == "fault":
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(self.message.faultCode, self.message.faultString))
            return False
        # end if
        #// Message must be OK
        return True
    # end def query
    def getresponse(self):
        
        
        #// methodResponses can only have one param - return that
        return self.message.params[0]
    # end def getresponse
    def iserror(self):
        
        
        return php_is_object(self.error)
    # end def iserror
    def geterrorcode(self):
        
        
        return self.error.code
    # end def geterrorcode
    def geterrormessage(self):
        
        
        return self.error.message
    # end def geterrormessage
# end class IXR_Client
