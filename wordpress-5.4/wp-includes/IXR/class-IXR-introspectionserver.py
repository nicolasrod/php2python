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
    def addcallback(self, method_=None, callback_=None, args_=None, help_=None):
        
        
        self.callbacks[method_] = callback_
        self.signatures[method_] = args_
        self.help[method_] = help_
    # end def addcallback
    def call(self, methodname_=None, args_=None):
        
        
        #// Make sure it's in an array
        if args_ and (not php_is_array(args_)):
            args_ = Array(args_)
        # end if
        #// Over-rides default call method, adds signature check
        if (not self.hasmethod(methodname_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested method \"" + self.message.methodName + "\" not specified."))
        # end if
        method_ = self.callbacks[methodname_]
        signature_ = self.signatures[methodname_]
        returnType_ = php_array_shift(signature_)
        #// Check the number of arguments
        if php_count(args_) != php_count(signature_):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32602, "server error. wrong number of method parameters"))
        # end if
        #// Check the argument types
        ok_ = True
        argsbackup_ = args_
        i_ = 0
        j_ = php_count(args_)
        while i_ < j_:
            
            arg_ = php_array_shift(args_)
            type_ = php_array_shift(signature_)
            for case in Switch(type_):
                if case("int"):
                    pass
                # end if
                if case("i4"):
                    if php_is_array(arg_) or (not php_is_int(arg_)):
                        ok_ = False
                    # end if
                    break
                # end if
                if case("base64"):
                    pass
                # end if
                if case("string"):
                    if (not php_is_string(arg_)):
                        ok_ = False
                    # end if
                    break
                # end if
                if case("boolean"):
                    if arg_ != False and arg_ != True:
                        ok_ = False
                    # end if
                    break
                # end if
                if case("float"):
                    pass
                # end if
                if case("double"):
                    if (not php_is_float(arg_)):
                        ok_ = False
                    # end if
                    break
                # end if
                if case("date"):
                    pass
                # end if
                if case("dateTime.iso8601"):
                    if (not php_is_a(arg_, "IXR_Date")):
                        ok_ = False
                    # end if
                    break
                # end if
            # end for
            if (not ok_):
                return php_new_class("IXR_Error", lambda : IXR_Error(-32602, "server error. invalid method parameters"))
            # end if
            i_ += 1
        # end while
        #// It passed the test - run the "real" method call
        return super().call(methodname_, argsbackup_)
    # end def call
    def methodsignature(self, method_=None):
        
        
        if (not self.hasmethod(method_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(-32601, "server error. requested method \"" + method_ + "\" not specified."))
        # end if
        #// We should be returning an array of types
        types_ = self.signatures[method_]
        return_ = Array()
        for type_ in types_:
            for case in Switch(type_):
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
    def methodhelp(self, method_=None):
        
        
        return self.help[method_]
    # end def methodhelp
# end class IXR_IntrospectionServer
