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
#// Customize API: WP_Customize_Cropped_Image_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Cropped Image Control class.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Image_Control
#//
class WP_Customize_Cropped_Image_Control(WP_Customize_Image_Control):
    type = "cropped_image"
    width = 150
    height = 150
    flex_width = False
    flex_height = False
    #// 
    #// Enqueue control related scripts/styles.
    #// 
    #// @since 4.3.0
    #//
    def enqueue(self):
        
        wp_enqueue_script("customize-views")
        super().enqueue()
    # end def enqueue
    #// 
    #// Refresh the parameters passed to the JavaScript via JSON.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Control::to_json()
    #//
    def to_json(self):
        
        super().to_json()
        self.json["width"] = absint(self.width)
        self.json["height"] = absint(self.height)
        self.json["flex_width"] = absint(self.flex_width)
        self.json["flex_height"] = absint(self.flex_height)
    # end def to_json
# end class WP_Customize_Cropped_Image_Control
