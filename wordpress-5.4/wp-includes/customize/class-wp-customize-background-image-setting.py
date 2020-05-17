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
#// Customize API: WP_Customize_Background_Image_Setting class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customizer Background Image Setting class.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Setting
#//
class WP_Customize_Background_Image_Setting(WP_Customize_Setting):
    id = "background_image_thumb"
    #// 
    #// @since 3.4.0
    #// 
    #// @param $value
    #//
    def update(self, value_=None):
        
        
        remove_theme_mod("background_image_thumb")
    # end def update
# end class WP_Customize_Background_Image_Setting
