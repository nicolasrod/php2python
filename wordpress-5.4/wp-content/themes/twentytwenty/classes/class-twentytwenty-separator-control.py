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
#// Customizer Separator Control settings for this theme.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if php_class_exists("WP_Customize_Control"):
    if (not php_class_exists("TwentyTwenty_Separator_Control")):
        #// 
        #// Separator Control.
        #//
        class TwentyTwenty_Separator_Control(WP_Customize_Control):
            #// 
            #// Render the hr.
            #//
            def render_content(self):
                
                
                php_print("<hr/>")
            # end def render_content
        # end class TwentyTwenty_Separator_Control
    # end if
# end if
