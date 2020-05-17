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
#// Event dispatcher
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// Event dispatcher
#// 
#// @package Requests
#// @subpackage Utilities
#//
class Requests_Hooker():
    #// 
    #// Register a callback for a hook
    #// 
    #// @param string $hook Hook name
    #// @param callback $callback Function/method to call on event
    #// @param int $priority Priority number. <0 is executed earlier, >0 is executed later
    #//
    def register(self, hook_=None, callback_=None, priority_=0):
        
        
        pass
    # end def register
    #// 
    #// Dispatch a message
    #// 
    #// @param string $hook Hook name
    #// @param array $parameters Parameters to pass to callbacks
    #// @return boolean Successfulness
    #//
    def dispatch(self, hook_=None, parameters_=None):
        if parameters_ is None:
            parameters_ = Array()
        # end if
        
        pass
    # end def dispatch
# end class Requests_Hooker
