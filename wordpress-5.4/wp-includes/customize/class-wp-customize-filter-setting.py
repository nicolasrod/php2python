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
#// Customize API: WP_Customize_Filter_Setting class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// A setting that is used to filter a value, but will not save the results.
#// 
#// Results should be properly handled using another setting or callback.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Setting
#//
class WP_Customize_Filter_Setting(WP_Customize_Setting):
    #// 
    #// Saves the value of the setting, using the related API.
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $value The value to update.
    #//
    def update(self, value=None):
        
        pass
    # end def update
# end class WP_Customize_Filter_Setting
