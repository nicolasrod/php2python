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
#// Customize API: WP_Customize_Background_Image_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Background Image Control class.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Image_Control
#//
class WP_Customize_Background_Image_Control(WP_Customize_Image_Control):
    type = "background"
    #// 
    #// Constructor.
    #// 
    #// @since 3.4.0
    #// @uses WP_Customize_Image_Control::__construct()
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #//
    def __init__(self, manager_=None):
        
        
        super().__init__(manager_, "background_image", Array({"label": __("Background Image"), "section": "background_image"}))
    # end def __init__
    #// 
    #// Enqueue control related scripts/styles.
    #// 
    #// @since 4.1.0
    #//
    def enqueue(self):
        
        
        super().enqueue()
        custom_background_ = get_theme_support("custom-background")
        wp_localize_script("customize-controls", "_wpCustomizeBackground", Array({"defaults": custom_background_[0] if (not php_empty(lambda : custom_background_[0])) else Array(), "nonces": Array({"add": wp_create_nonce("background-add")})}))
    # end def enqueue
# end class WP_Customize_Background_Image_Control
