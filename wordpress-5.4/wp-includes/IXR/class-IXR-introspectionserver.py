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
#// IXR_IntrospectionServer
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_IntrospectionServer(IXR_Server):
    signatures = Array()
    help = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self):
        
        self.setcallbacks()
        self.setcapabilities()
        self.capabilities["introspection"] = Array({"specUrl": "http://xmlrpc.usefulinc.com/doc/reserved.html", "specVersion": 1})
        self.addcallback("system.methodSignature", "this:methodSignature", Array("array", "string"), "Returns an array describing the return type and required parameters of a method")
        self.addcallback("system.getCapabilities", "this:getCapabilities", Array("struct"), "Returns a struct describing the XML-RPC specifications supported by this server")
        self.addcallback("system.listMethods", "this:listMethods", Array("array"), "Returns an array of available methods on this server")
        self.addcallback("system.methodHelp", "this:methodHelp", Array("string", "string"), "Returns a documentation string for the specified method")
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_introspectionserver(self):
        
        self.__init__()
    # end def ixr_introspectionserver
    def addcallback(self, method=None, callback=None, args=None, help=None):
        
        self.callbacks[method] = callback
        self.signatures[method] = args
        self.help[method] = help
    # end def addcallback
    def call(self, methodname=None, args=None):
        
        #// Make sure it's in an array
        if args and (not php_is_array(args)):
            args = Array(args)
        # end if
        #// Over-rides default call method, adds signature check
        if (not self.hasmethod(methodname)):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested method \"" + self.message.methodName + "\" not specified."))
        # end if
        method = self.callbacks[methodname]
        signature = self.signatures[methodname]
        returnType = php_array_shift(signature)
        #// Check the number of arguments
        if php_count(args) != php_count(signature):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32602, "server error. wrong number of method parameters"))
        # end if
        #// Check the argument types
        ok = True
        argsbackup = args
        i = 0
        j = php_count(args)
        while i < j:
            
            arg = php_array_shift(args)
            type = php_array_shift(signature)
            for case in Switch(type):
                if case("int"):
                    pass
                # end if
                if case("i4"):
                    if php_is_array(arg) or (not php_is_int(arg)):
                        ok = False
                    # end if
                    break
                # end if
                if case("base64"):
                    pass
                # end if
                if case("string"):
                    if (not php_is_string(arg)):
                        ok = False
                    # end if
                    break
                # end if
                if case("boolean"):
                    if arg != False and arg != True:
                        ok = False
                    # end if
                    break
                # end if
                if case("float"):
                    pass
                # end if
                if case("double"):
                    if (not php_is_float(arg)):
                        ok = False
                    # end if
                    break
                # end if
                if case("date"):
                    pass
                # end if
                if case("dateTime.iso8601"):
                    if (not php_is_a(arg, "IXR_Date")):
                        ok = False
                    # end if
                    break
                # end if
            # end for
            if (not ok):
                return php_new_class("IXR_Error", lambda : IXR_Error(-32602, "server error. invalid method parameters"))
            # end if
            i += 1
        # end while
        #// It passed the test - run the "real" method call
        return super().call(methodname, argsbackup)
    # end def call
    def methodsignature(self, method=None):
        
        if (not self.hasmethod(method)):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested method \"" + method + "\" not specified."))
        # end if
        #// We should be returning an array of types
        types = self.signatures[method]
        return_ = Array()
        for type in types:
            for case in Switch(type):
                if case("string"):
                    return_[-1] = "string"
                    break
                # end if
                if case("int"):
                    pass
                # end if
                if case("i4"):
                    return_[-1] = 42
                    break
                # end if
                if case("double"):
                    return_[-1] = 3.1415
                    break
                # end if
                if case("dateTime.iso8601"):
                    return_[-1] = php_new_class("IXR_Date", lambda : IXR_Date(time()))
                    break
                # end if
                if case("boolean"):
                    return_[-1] = True
                    break
                # end if
                if case("base64"):
                    return_[-1] = php_new_class("IXR_Base64", lambda : IXR_Base64("base64"))
                    break
                # end if
                if case("array"):
                    return_[-1] = Array("array")
                    break
                # end if
                if case("struct"):
                    return_[-1] = Array({"struct": "struct"})
                    break
                # end if
            # end for
        # end for
        return return_
    # end def methodsignature
    def methodhelp(self, method=None):
        
        return self.help[method]
    # end def methodhelp
# end class IXR_IntrospectionServer
