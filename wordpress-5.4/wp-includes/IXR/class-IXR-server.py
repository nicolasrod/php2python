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
#// IXR_Server
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_Server():
    data = Array()
    callbacks = Array()
    message = Array()
    capabilities = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, callbacks=False, data=False, wait=False):
        
        self.setcapabilities()
        if callbacks:
            self.callbacks = callbacks
        # end if
        self.setcallbacks()
        if (not wait):
            self.serve(data)
        # end if
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_server(self, callbacks=False, data=False, wait=False):
        
        self.__init__(callbacks, data, wait)
    # end def ixr_server
    def serve(self, data=False):
        
        if (not data):
            if (php_isset(lambda : PHP_SERVER["REQUEST_METHOD"])) and PHP_SERVER["REQUEST_METHOD"] != "POST":
                if php_function_exists("status_header"):
                    status_header(405)
                    #// WP #20986
                    php_header("Allow: POST")
                # end if
                php_header("Content-Type: text/plain")
                #// merged from WP #9093
                php_print("XML-RPC server accepts POST requests only.")
                php_exit()
            # end if
            global HTTP_RAW_POST_DATA
            php_check_if_defined("HTTP_RAW_POST_DATA")
            if php_empty(lambda : HTTP_RAW_POST_DATA):
                #// workaround for a bug in PHP 5.2.2 - http://bugs.php.net/bug.php?id=41293
                data = php_file_get_contents("php://input")
            else:
                data = HTTP_RAW_POST_DATA
            # end if
        # end if
        self.message = php_new_class("IXR_Message", lambda : IXR_Message(data))
        if (not self.message.parse()):
            self.error(-32700, "parse error. not well formed")
        # end if
        if self.message.messageType != "methodCall":
            self.error(-32600, "server error. invalid xml-rpc. not conforming to spec. Request must be a methodCall")
        # end if
        result = self.call(self.message.methodName, self.message.params)
        #// Is the result an error?
        if php_is_a(result, "IXR_Error"):
            self.error(result)
        # end if
        #// Encode the result
        r = php_new_class("IXR_Value", lambda : IXR_Value(result))
        resultxml = r.getxml()
        #// Create the XML
        xml = str("""<methodResponse>\n  <params>\n    <param>\n      <value>\n      """) + str(resultxml) + str("""\n      </value>\n    </param>\n  </params>\n</methodResponse>\n""")
        #// Send it
        self.output(xml)
    # end def serve
    def call(self, methodname=None, args=None):
        
        if (not self.hasmethod(methodname)):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested method " + methodname + " does not exist."))
        # end if
        method = self.callbacks[methodname]
        #// Perform the callback and send the response
        if php_count(args) == 1:
            #// If only one parameter just send that instead of the whole array
            args = args[0]
        # end if
        #// Are we dealing with a function or a method?
        if php_is_string(method) and php_substr(method, 0, 5) == "this:":
            #// It's a class method - check it exists
            method = php_substr(method, 5)
            if (not php_method_exists(self, method)):
                return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested class method \"" + method + "\" does not exist."))
            # end if
            #// Call the method
            result = self.method(args)
        else:
            #// It's a function - does it exist?
            if php_is_array(method):
                if (not php_is_callable(Array(method[0], method[1]))):
                    return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested object method \"" + method[1] + "\" does not exist."))
                # end if
            else:
                if (not php_function_exists(method)):
                    return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested function \"" + method + "\" does not exist."))
                # end if
            # end if
            #// Call the function
            result = php_call_user_func(method, args)
        # end if
        return result
    # end def call
    def error(self, error=None, message=False):
        
        #// Accepts either an error object or an error code and message
        if message and (not php_is_object(error)):
            error = php_new_class("IXR_Error", lambda : IXR_Error(error, message))
        # end if
        self.output(error.getxml())
    # end def error
    def output(self, xml=None):
        
        charset = get_option("blog_charset") if php_function_exists("get_option") else ""
        if charset:
            xml = "<?xml version=\"1.0\" encoding=\"" + charset + "\"?>" + "\n" + xml
        else:
            xml = "<?xml version=\"1.0\"?>" + "\n" + xml
        # end if
        length = php_strlen(xml)
        php_header("Connection: close")
        if charset:
            php_header("Content-Type: text/xml; charset=" + charset)
        else:
            php_header("Content-Type: text/xml")
        # end if
        php_header("Date: " + gmdate("r"))
        php_print(xml)
        php_exit(0)
    # end def output
    def hasmethod(self, method=None):
        
        return php_in_array(method, php_array_keys(self.callbacks))
    # end def hasmethod
    def setcapabilities(self):
        
        #// Initialises capabilities array
        self.capabilities = Array({"xmlrpc": Array({"specUrl": "http://www.xmlrpc.com/spec", "specVersion": 1})}, {"faults_interop": Array({"specUrl": "http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php", "specVersion": 20010516})}, {"system.multicall": Array({"specUrl": "http://www.xmlrpc.com/discuss/msgReader$1208", "specVersion": 1})})
    # end def setcapabilities
    def getcapabilities(self, args=None):
        
        return self.capabilities
    # end def getcapabilities
    def setcallbacks(self):
        
        self.callbacks["system.getCapabilities"] = "this:getCapabilities"
        self.callbacks["system.listMethods"] = "this:listMethods"
        self.callbacks["system.multicall"] = "this:multiCall"
    # end def setcallbacks
    def listmethods(self, args=None):
        
        #// Returns a list of methods - uses array_reverse to ensure user defined
        #// methods are listed before server defined methods
        return array_reverse(php_array_keys(self.callbacks))
    # end def listmethods
    def multicall(self, methodcalls=None):
        
        #// See http://www.xmlrpc.com/discuss/msgReader$1208
        return_ = Array()
        for call in methodcalls:
            method = call["methodName"]
            params = call["params"]
            if method == "system.multicall":
                result = php_new_class("IXR_Error", lambda : IXR_Error(-32600, "Recursive calls to system.multicall are forbidden"))
            else:
                result = self.call(method, params)
            # end if
            if php_is_a(result, "IXR_Error"):
                return_[-1] = Array({"faultCode": result.code, "faultString": result.message})
            else:
                return_[-1] = Array(result)
            # end if
        # end for
        return return_
    # end def multicall
# end class IXR_Server
