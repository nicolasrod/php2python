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
    def __init__(self, server=None, path=False, port=80):
        
        super().ixr_client(server, path, port)
        self.useragent = "The Incutio XML-RPC PHP Library (multicall client)"
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_clientmulticall(self, server=None, path=False, port=80):
        
        self.__init__(server, path, port)
    # end def ixr_clientmulticall
    def addcall(self):
        
        args = php_func_get_args()
        methodName = php_array_shift(args)
        struct = Array({"methodName": methodName, "params": args})
        self.calls[-1] = struct
    # end def addcall
    def query(self):
        
        #// Prepare multicall, then call the parent::query() method
        return super().query("system.multicall", self.calls)
    # end def query
# end class IXR_ClientMulticall
