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
#// Customize API: WP_Customize_Custom_CSS_Setting class
#// 
#// This handles validation, sanitization and saving of the value.
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.7.0
#// 
#// 
#// Custom Setting to handle WP Custom CSS.
#// 
#// @since 4.7.0
#// 
#// @see WP_Customize_Setting
#//
class WP_Customize_Custom_CSS_Setting(WP_Customize_Setting):
    type = "custom_css"
    transport = "postMessage"
    capability = "edit_css"
    stylesheet = ""
    #// 
    #// WP_Customize_Custom_CSS_Setting constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @throws Exception If the setting ID does not match the pattern `custom_css[$stylesheet]`.
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      A specific ID of the setting.
    #// Can be a theme mod or option name.
    #// @param array                $args    Setting arguments.
    #//
    def __init__(self, manager=None, id=None, args=Array()):
        
        super().__init__(manager, id, args)
        if "custom_css" != self.id_data["base"]:
            raise php_new_class("Exception", lambda : Exception("Expected custom_css id_base."))
        # end if
        if 1 != php_count(self.id_data["keys"]) or php_empty(lambda : self.id_data["keys"][0]):
            raise php_new_class("Exception", lambda : Exception("Expected single stylesheet key."))
        # end if
        self.stylesheet = self.id_data["keys"][0]
    # end def __init__
    #// 
    #// Add filter to preview post value.
    #// 
    #// @since 4.7.9
    #// 
    #// @return bool False when preview short-circuits due no change needing to be previewed.
    #//
    def preview(self):
        
        if self.is_previewed:
            return False
        # end if
        self.is_previewed = True
        add_filter("wp_get_custom_css", Array(self, "filter_previewed_wp_get_custom_css"), 9, 2)
        return True
    # end def preview
    #// 
    #// Filter `wp_get_custom_css` for applying the customized value.
    #// 
    #// This is used in the preview when `wp_get_custom_css()` is called for rendering the styles.
    #// 
    #// @since 4.7.0
    #// @see wp_get_custom_css()
    #// 
    #// @param string $css        Original CSS.
    #// @param string $stylesheet Current stylesheet.
    #// @return string CSS.
    #//
    def filter_previewed_wp_get_custom_css(self, css=None, stylesheet=None):
        
        if stylesheet == self.stylesheet:
            customized_value = self.post_value(None)
            if (not php_is_null(customized_value)):
                css = customized_value
            # end if
        # end if
        return css
    # end def filter_previewed_wp_get_custom_css
    #// 
    #// Fetch the value of the setting. Will return the previewed value when `preview()` is called.
    #// 
    #// @since 4.7.0
    #// @see WP_Customize_Setting::value()
    #// 
    #// @return string
    #//
    def value(self):
        
        if self.is_previewed:
            post_value = self.post_value(None)
            if None != post_value:
                return post_value
            # end if
        # end if
        id_base = self.id_data["base"]
        value = ""
        post = wp_get_custom_css_post(self.stylesheet)
        if post:
            value = post.post_content
        # end if
        if php_empty(lambda : value):
            value = self.default
        # end if
        #// This filter is documented in wp-includes/class-wp-customize-setting.php
        value = apply_filters(str("customize_value_") + str(id_base), value, self)
        return value
    # end def value
    #// 
    #// Validate CSS.
    #// 
    #// Checks for imbalanced braces, brackets, and comments.
    #// Notifications are rendered when the customizer state is saved.
    #// 
    #// @since 4.7.0
    #// @since 4.9.0 Checking for balanced characters has been moved client-side via linting in code editor.
    #// 
    #// @param string $css The input string.
    #// @return true|WP_Error True if the input was validated, otherwise WP_Error.
    #//
    def validate(self, css=None):
        
        validity = php_new_class("WP_Error", lambda : WP_Error())
        if php_preg_match("#</?\\w+#", css):
            validity.add("illegal_markup", __("Markup is not allowed in CSS."))
        # end if
        if (not validity.has_errors()):
            validity = super().validate(css)
        # end if
        return validity
    # end def validate
    #// 
    #// Store the CSS setting value in the custom_css custom post type for the stylesheet.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $css The input value.
    #// @return int|false The post ID or false if the value could not be saved.
    #//
    def update(self, css=None):
        
        if php_empty(lambda : css):
            css = ""
        # end if
        r = wp_update_custom_css_post(css, Array({"stylesheet": self.stylesheet}))
        if type(r).__name__ == "WP_Error":
            return False
        # end if
        post_id = r.ID
        #// Cache post ID in theme mod for performance to avoid additional DB query.
        if self.manager.get_stylesheet() == self.stylesheet:
            set_theme_mod("custom_css_post_id", post_id)
        # end if
        return post_id
    # end def update
# end class WP_Customize_Custom_CSS_Setting
