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
#// Authentication provider interface
#// 
#// @package Requests
#// @subpackage Authentication
#// 
#// 
#// Authentication provider interface
#// 
#// Implement this interface to act as an authentication provider.
#// 
#// Parameters should be passed via the constructor where possible, as this
#// makes it much easier for users to use your provider.
#// 
#// @see Requests_Hooks
#// @package Requests
#// @subpackage Authentication
#//
class Requests_Auth():
    #// 
    #// Register hooks as needed
    #// 
    #// This method is called in {@see Requests::request} when the user has set
    #// an instance as the 'auth' option. Use this callback to register all the
    #// hooks you'll need.
    #// 
    #// @see Requests_Hooks::register
    #// @param Requests_Hooks $hooks Hook system
    #//
    def register(self, hooks=None):
        
        pass
    # end def register
# end class Requests_Auth
