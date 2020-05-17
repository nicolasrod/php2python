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
#// IXR_ClientMulticall
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_ClientMulticall(IXR_Client):
    calls = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, server_=None, path_=None, port_=80):
        if path_ is None:
            path_ = False
        # end if
        
        super().ixr_client(server_, path_, port_)
        self.useragent = "The Incutio XML-RPC PHP Library (multicall client)"
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_clientmulticall(self, server_=None, path_=None, port_=80):
        if path_ is None:
            path_ = False
        # end if
        
        self.__init__(server_, path_, port_)
    # end def ixr_clientmulticall
    def addcall(self):
        
        
        args_ = php_func_get_args()
        methodName_ = php_array_shift(args_)
        struct_ = Array({"methodName": methodName_, "params": args_})
        self.calls[-1] = struct_
    # end def addcall
    def query(self):
        
        
        #// Prepare multicall, then call the parent::query() method
        return super().query("system.multicall", self.calls)
    # end def query
# end class IXR_ClientMulticall
