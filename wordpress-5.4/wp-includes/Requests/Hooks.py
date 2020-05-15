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
#// Handles adding and dispatching events
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// Handles adding and dispatching events
#// 
#// @package Requests
#// @subpackage Utilities
#//
class Requests_Hooks(Requests_Hooker):
    hooks = Array()
    #// 
    #// Constructor
    #//
    def __init__(self):
        
        pass
    # end def __init__
    #// 
    #// Register a callback for a hook
    #// 
    #// @param string $hook Hook name
    #// @param callback $callback Function/method to call on event
    #// @param int $priority Priority number. <0 is executed earlier, >0 is executed later
    #//
    def register(self, hook=None, callback=None, priority=0):
        
        if (not (php_isset(lambda : self.hooks[hook]))):
            self.hooks[hook] = Array()
        # end if
        if (not (php_isset(lambda : self.hooks[hook][priority]))):
            self.hooks[hook][priority] = Array()
        # end if
        self.hooks[hook][priority][-1] = callback
    # end def register
    #// 
    #// Dispatch a message
    #// 
    #// @param string $hook Hook name
    #// @param array $parameters Parameters to pass to callbacks
    #// @return boolean Successfulness
    #//
    def dispatch(self, hook=None, parameters=Array()):
        
        if php_empty(lambda : self.hooks[hook]):
            return False
        # end if
        for priority,hooked in self.hooks[hook]:
            for callback in hooked:
                call_user_func_array(callback, parameters)
            # end for
        # end for
        return True
    # end def dispatch
# end class Requests_Hooks
