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
    error = False
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, server=None, path=False, port=80, timeout=15):
        
        if (not path):
            #// Assume we have been given a URL instead
            bits = php_parse_url(server)
            self.server = bits["host"]
            self.port = bits["port"] if (php_isset(lambda : bits["port"])) else 80
            self.path = bits["path"] if (php_isset(lambda : bits["path"])) else "/"
            #// Make absolutely sure we have a path
            if (not self.path):
                self.path = "/"
            # end if
            if (not php_empty(lambda : bits["query"])):
                self.path += "?" + bits["query"]
            # end if
        else:
            self.server = server
            self.path = path
            self.port = port
        # end if
        self.useragent = "The Incutio XML-RPC PHP Library"
        self.timeout = timeout
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_client(self, server=None, path=False, port=80, timeout=15):
        
        self.__init__(server, path, port, timeout)
    # end def ixr_client
    def query(self):
        
        args = php_func_get_args()
        method = php_array_shift(args)
        request = php_new_class("IXR_Request", lambda : IXR_Request(method, args))
        length = request.getlength()
        xml = request.getxml()
        r = "\r\n"
        request = str("POST ") + str(self.path) + str(" HTTP/1.0") + str(r)
        #// Merged from WP #8145 - allow custom headers
        self.headers["Host"] = self.server
        self.headers["Content-Type"] = "text/xml"
        self.headers["User-Agent"] = self.useragent
        self.headers["Content-Length"] = length
        for header,value in self.headers:
            request += str(header) + str(": ") + str(value) + str(r)
        # end for
        request += r
        request += xml
        #// Now send the request
        if self.debug:
            php_print("<pre class=\"ixr_request\">" + htmlspecialchars(request) + """
            </pre>
            """)
        # end if
        if self.timeout:
            fp = php_no_error(lambda: fsockopen(self.server, self.port, errno, errstr, self.timeout))
        else:
            fp = php_no_error(lambda: fsockopen(self.server, self.port, errno, errstr))
        # end if
        if (not fp):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32300, "transport error - could not open socket"))
            return False
        # end if
        fputs(fp, request)
        contents = ""
        debugContents = ""
        gotFirstLine = False
        gettingHeaders = True
        while True:
            
            if not ((not php_feof(fp))):
                break
            # end if
            line = php_fgets(fp, 4096)
            if (not gotFirstLine):
                #// Check line for '200'
                if php_strstr(line, "200") == False:
                    self.error = php_new_class("IXR_Error", lambda : IXR_Error(-32300, "transport error - HTTP status code was not 200"))
                    return False
                # end if
                gotFirstLine = True
            # end if
            if php_trim(line) == "":
                gettingHeaders = False
            # end if
            if (not gettingHeaders):
                #// merged from WP #12559 - remove trim
                contents += line
            # end if
            if self.debug:
                debugContents += line
            # end if
        # end while
        if self.debug:
            php_print("<pre class=\"ixr_response\">" + htmlspecialchars(debugContents) + """
            </pre>
            """)
        # end if
        #// Now parse what we've got back
        self.message = php_new_class("IXR_Message", lambda : IXR_Message(contents))
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
