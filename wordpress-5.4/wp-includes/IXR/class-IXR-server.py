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
    def __init__(self, callbacks_=None, data_=None, wait_=None):
        if callbacks_ is None:
            callbacks_ = False
        # end if
        if data_ is None:
            data_ = False
        # end if
        if wait_ is None:
            wait_ = False
        # end if
        
        self.setcapabilities()
        if callbacks_:
            self.callbacks = callbacks_
        # end if
        self.setcallbacks()
        if (not wait_):
            self.serve(data_)
        # end if
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_server(self, callbacks_=None, data_=None, wait_=None):
        if callbacks_ is None:
            callbacks_ = False
        # end if
        if data_ is None:
            data_ = False
        # end if
        if wait_ is None:
            wait_ = False
        # end if
        
        self.__init__(callbacks_, data_, wait_)
    # end def ixr_server
    def serve(self, data_=None):
        if data_ is None:
            data_ = False
        # end if
        
        if (not data_):
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
            global HTTP_RAW_POST_DATA_
            php_check_if_defined("HTTP_RAW_POST_DATA_")
            if php_empty(lambda : HTTP_RAW_POST_DATA_):
                #// workaround for a bug in PHP 5.2.2 - http://bugs.php.net/bug.php?id=41293
                data_ = php_file_get_contents("php://input")
            else:
                data_ = HTTP_RAW_POST_DATA_
            # end if
        # end if
        self.message = php_new_class("IXR_Message", lambda : IXR_Message(data_))
        if (not self.message.parse()):
            self.error(-32700, "parse error. not well formed")
        # end if
        if self.message.messageType != "methodCall":
            self.error(-32600, "server error. invalid xml-rpc. not conforming to spec. Request must be a methodCall")
        # end if
        result_ = self.call(self.message.methodName, self.message.params)
        #// Is the result an error?
        if php_is_a(result_, "IXR_Error"):
            self.error(result_)
        # end if
        #// Encode the result
        r_ = php_new_class("IXR_Value", lambda : IXR_Value(result_))
        resultxml_ = r_.getxml()
        #// Create the XML
        xml_ = str("""<methodResponse>\n  <params>\n    <param>\n      <value>\n      """) + str(resultxml_) + str("""\n      </value>\n    </param>\n  </params>\n</methodResponse>\n""")
        #// Send it
        self.output(xml_)
    # end def serve
    def call(self, methodname_=None, args_=None):
        
        
        if (not self.hasmethod(methodname_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested method " + methodname_ + " does not exist."))
        # end if
        method_ = self.callbacks[methodname_]
        #// Perform the callback and send the response
        if php_count(args_) == 1:
            #// If only one parameter just send that instead of the whole array
            args_ = args_[0]
        # end if
        #// Are we dealing with a function or a method?
        if php_is_string(method_) and php_substr(method_, 0, 5) == "this:":
            #// It's a class method - check it exists
            method_ = php_substr(method_, 5)
            if (not php_method_exists(self, method_)):
                return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested class method \"" + method_ + "\" does not exist."))
            # end if
            #// Call the method
            result_ = self.method_(args_)
        else:
            #// It's a function - does it exist?
            if php_is_array(method_):
                if (not php_is_callable(Array(method_[0], method_[1]))):
                    return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested object method \"" + method_[1] + "\" does not exist."))
                # end if
            else:
                if (not php_function_exists(method_)):
                    return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested function \"" + method_ + "\" does not exist."))
                # end if
            # end if
            #// Call the function
            result_ = php_call_user_func(method_, args_)
        # end if
        return result_
    # end def call
    def error(self, error_=None, message_=None):
        if message_ is None:
            message_ = False
        # end if
        
        #// Accepts either an error object or an error code and message
        if message_ and (not php_is_object(error_)):
            error_ = php_new_class("IXR_Error", lambda : IXR_Error(error_, message_))
        # end if
        self.output(error_.getxml())
    # end def error
    def output(self, xml_=None):
        
        
        charset_ = get_option("blog_charset") if php_function_exists("get_option") else ""
        if charset_:
            xml_ = "<?xml version=\"1.0\" encoding=\"" + charset_ + "\"?>" + "\n" + xml_
        else:
            xml_ = "<?xml version=\"1.0\"?>" + "\n" + xml_
        # end if
        length_ = php_strlen(xml_)
        php_header("Connection: close")
        if charset_:
            php_header("Content-Type: text/xml; charset=" + charset_)
        else:
            php_header("Content-Type: text/xml")
        # end if
        php_header("Date: " + gmdate("r"))
        php_print(xml_)
        php_exit(0)
    # end def output
    def hasmethod(self, method_=None):
        
        
        return php_in_array(method_, php_array_keys(self.callbacks))
    # end def hasmethod
    def setcapabilities(self):
        
        
        #// Initialises capabilities array
        self.capabilities = Array({"xmlrpc": Array({"specUrl": "http://www.xmlrpc.com/spec", "specVersion": 1})}, {"faults_interop": Array({"specUrl": "http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php", "specVersion": 20010516})}, {"system.multicall": Array({"specUrl": "http://www.xmlrpc.com/discuss/msgReader$1208", "specVersion": 1})})
    # end def setcapabilities
    def getcapabilities(self, args_=None):
        
        
        return self.capabilities
    # end def getcapabilities
    def setcallbacks(self):
        
        
        self.callbacks["system.getCapabilities"] = "this:getCapabilities"
        self.callbacks["system.listMethods"] = "this:listMethods"
        self.callbacks["system.multicall"] = "this:multiCall"
    # end def setcallbacks
    def listmethods(self, args_=None):
        
        
        #// Returns a list of methods - uses array_reverse to ensure user defined
        #// methods are listed before server defined methods
        return array_reverse(php_array_keys(self.callbacks))
    # end def listmethods
    def multicall(self, methodcalls_=None):
        
        
        #// See http://www.xmlrpc.com/discuss/msgReader$1208
        return_ = Array()
        for call_ in methodcalls_:
            method_ = call_["methodName"]
            params_ = call_["params"]
            if method_ == "system.multicall":
                result_ = php_new_class("IXR_Error", lambda : IXR_Error(-32600, "Recursive calls to system.multicall are forbidden"))
            else:
                result_ = self.call(method_, params_)
            # end if
            if php_is_a(result_, "IXR_Error"):
                return_[-1] = Array({"faultCode": result_.code, "faultString": result_.message})
            else:
                return_[-1] = Array(result_)
            # end if
        # end for
        return return_
    # end def multicall
# end class IXR_Server
