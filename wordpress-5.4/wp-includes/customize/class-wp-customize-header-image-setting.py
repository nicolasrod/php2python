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
#// Customize API: WP_Customize_Header_Image_Setting class
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
class WP_Customize_Header_Image_Setting(WP_Customize_Setting):
    id = "header_image_data"
    #// 
    #// @since 3.4.0
    #// 
    #// @global Custom_Image_Header $custom_image_header
    #// 
    #// @param $value
    #//
    def update(self, value_=None):
        
        
        global custom_image_header_
        php_check_if_defined("custom_image_header_")
        #// If _custom_header_background_just_in_time() fails to initialize $custom_image_header when not is_admin().
        if php_empty(lambda : custom_image_header_):
            php_include_file(ABSPATH + "wp-admin/includes/class-custom-image-header.php", once=True)
            args_ = get_theme_support("custom-header")
            admin_head_callback_ = args_[0]["admin-head-callback"] if (php_isset(lambda : args_[0]["admin-head-callback"])) else None
            admin_preview_callback_ = args_[0]["admin-preview-callback"] if (php_isset(lambda : args_[0]["admin-preview-callback"])) else None
            custom_image_header_ = php_new_class("Custom_Image_Header", lambda : Custom_Image_Header(admin_head_callback_, admin_preview_callback_))
        # end if
        #// If the value doesn't exist (removed or random),
        #// use the header_image value.
        if (not value_):
            value_ = self.manager.get_setting("header_image").post_value()
        # end if
        if php_is_array(value_) and (php_isset(lambda : value_["choice"])):
            custom_image_header_.set_header_image(value_["choice"])
        else:
            custom_image_header_.set_header_image(value_)
        # end if
    # end def update
# end class WP_Customize_Header_Image_Setting
