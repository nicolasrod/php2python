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
    #// 
    #// Control type.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "cropped_image"
    #// 
    #// Suggested width for cropped image.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    width = 150
    #// 
    #// Suggested height for cropped image.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    height = 150
    #// 
    #// Whether the width is flexible.
    #// 
    #// @since 4.3.0
    #// @var bool
    #//
    flex_width = False
    #// 
    #// Whether the height is flexible.
    #// 
    #// @since 4.3.0
    #// @var bool
    #//
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
