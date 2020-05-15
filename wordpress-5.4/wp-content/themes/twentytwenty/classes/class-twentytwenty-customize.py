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
#// Customizer settings for this theme.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if (not php_class_exists("TwentyTwenty_Customize")):
    #// 
    #// CUSTOMIZER SETTINGS
    #//
    class TwentyTwenty_Customize():
        #// 
        #// Register customizer options.
        #// 
        #// @param WP_Customize_Manager $wp_customize Theme Customizer object.
        #//
        @classmethod
        def register(self, wp_customize=None):
            
            #// 
            #// Site Title & Description.
            #//
            wp_customize.get_setting("blogname").transport = "postMessage"
            wp_customize.get_setting("blogdescription").transport = "postMessage"
            wp_customize.selective_refresh.add_partial("blogname", Array({"selector": ".site-title a", "render_callback": "twentytwenty_customize_partial_blogname"}))
            wp_customize.selective_refresh.add_partial("blogdescription", Array({"selector": ".site-description", "render_callback": "twentytwenty_customize_partial_blogdescription"}))
            wp_customize.selective_refresh.add_partial("custom_logo", Array({"selector": ".header-titles [class*=site-]:not(.site-description)", "render_callback": "twentytwenty_customize_partial_site_logo"}))
            wp_customize.selective_refresh.add_partial("retina_logo", Array({"selector": ".header-titles [class*=site-]:not(.site-description)", "render_callback": "twentytwenty_customize_partial_site_logo"}))
            #// 
            #// Site Identity
            #// 
            #// 2X Header Logo ----------------
            wp_customize.add_setting("retina_logo", Array({"capability": "edit_theme_options", "sanitize_callback": Array(__CLASS__, "sanitize_checkbox"), "transport": "postMessage"}))
            wp_customize.add_control("retina_logo", Array({"type": "checkbox", "section": "title_tagline", "priority": 10, "label": __("Retina logo", "twentytwenty"), "description": __("Scales the logo to half its uploaded size, making it sharp on high-res screens.", "twentytwenty")}))
            #// Header & Footer Background Color.
            wp_customize.add_setting("header_footer_background_color", Array({"default": "#ffffff", "sanitize_callback": "sanitize_hex_color", "transport": "postMessage"}))
            wp_customize.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(wp_customize, "header_footer_background_color", Array({"label": __("Header &amp; Footer Background Color", "twentytwenty"), "section": "colors"}))))
            #// Enable picking an accent color.
            wp_customize.add_setting("accent_hue_active", Array({"capability": "edit_theme_options", "sanitize_callback": Array(__CLASS__, "sanitize_select"), "transport": "postMessage", "default": "default"}))
            wp_customize.add_control("accent_hue_active", Array({"type": "radio", "section": "colors", "label": __("Primary Color", "twentytwenty"), "choices": Array({"default": __("Default", "twentytwenty"), "custom": __("Custom", "twentytwenty")})}))
            #// 
            #// Implementation for the accent color.
            #// This is different to all other color options because of the accessibility enhancements.
            #// The control is a hue-only colorpicker, and there is a separate setting that holds values
            #// for other colors calculated based on the selected hue and various background-colors on the page.
            #// 
            #// @since Twenty Twenty 1.0
            #// 
            #// Add the setting for the hue colorpicker.
            wp_customize.add_setting("accent_hue", Array({"default": 344, "type": "theme_mod", "sanitize_callback": "absint", "transport": "postMessage"}))
            #// Add setting to hold colors derived from the accent hue.
            wp_customize.add_setting("accent_accessible_colors", Array({"default": Array({"content": Array({"text": "#000000", "accent": "#cd2653", "secondary": "#6d6d6d", "borders": "#dcd7ca"})}, {"header-footer": Array({"text": "#000000", "accent": "#cd2653", "secondary": "#6d6d6d", "borders": "#dcd7ca"})})}, {"type": "theme_mod", "transport": "postMessage", "sanitize_callback": Array(__CLASS__, "sanitize_accent_accessible_colors")}))
            #// Add the hue-only colorpicker for the accent color.
            wp_customize.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(wp_customize, "accent_hue", Array({"section": "colors", "settings": "accent_hue", "description": __("Apply a custom color for links, buttons, featured images.", "twentytwenty"), "mode": "hue", "active_callback": (lambda :  "custom" == wp_customize.get_setting("accent_hue_active").value())}))))
            #// Update background color with postMessage, so inline CSS output is updated as well.
            wp_customize.get_setting("background_color").transport = "postMessage"
            #// 
            #// Theme Options
            #//
            wp_customize.add_section("options", Array({"title": __("Theme Options", "twentytwenty"), "priority": 40, "capability": "edit_theme_options"}))
            #// Enable Header Search -----------------------------------------------
            wp_customize.add_setting("enable_header_search", Array({"capability": "edit_theme_options", "default": True, "sanitize_callback": Array(__CLASS__, "sanitize_checkbox")}))
            wp_customize.add_control("enable_header_search", Array({"type": "checkbox", "section": "options", "priority": 10, "label": __("Show search in header", "twentytwenty")}))
            #// Show author bio ----------------------------------------------------
            wp_customize.add_setting("show_author_bio", Array({"capability": "edit_theme_options", "default": True, "sanitize_callback": Array(__CLASS__, "sanitize_checkbox")}))
            wp_customize.add_control("show_author_bio", Array({"type": "checkbox", "section": "options", "priority": 10, "label": __("Show author bio", "twentytwenty")}))
            #// Display full content or excerpts on the blog and archives ---------
            wp_customize.add_setting("blog_content", Array({"capability": "edit_theme_options", "default": "full", "sanitize_callback": Array(__CLASS__, "sanitize_select")}))
            wp_customize.add_control("blog_content", Array({"type": "radio", "section": "options", "priority": 10, "label": __("On archive pages, posts show:", "twentytwenty"), "choices": Array({"full": __("Full text", "twentytwenty"), "summary": __("Summary", "twentytwenty")})}))
            #// 
            #// Template: Cover Template.
            #//
            wp_customize.add_section("cover_template_options", Array({"title": __("Cover Template", "twentytwenty"), "capability": "edit_theme_options", "description": __("Settings for the \"Cover Template\" page template. Add a featured image to use as background.", "twentytwenty"), "priority": 42}))
            #// Overlay Fixed Background ------
            wp_customize.add_setting("cover_template_fixed_background", Array({"capability": "edit_theme_options", "default": True, "sanitize_callback": Array(__CLASS__, "sanitize_checkbox"), "transport": "postMessage"}))
            wp_customize.add_control("cover_template_fixed_background", Array({"type": "checkbox", "section": "cover_template_options", "label": __("Fixed Background Image", "twentytwenty"), "description": __("Creates a parallax effect when the visitor scrolls.", "twentytwenty")}))
            wp_customize.selective_refresh.add_partial("cover_template_fixed_background", Array({"selector": ".cover-header", "type": "cover_fixed"}))
            #// Separator ---------------------
            wp_customize.add_setting("cover_template_separator_1", Array({"sanitize_callback": "wp_filter_nohtml_kses"}))
            wp_customize.add_control(php_new_class("TwentyTwenty_Separator_Control", lambda : TwentyTwenty_Separator_Control(wp_customize, "cover_template_separator_1", Array({"section": "cover_template_options"}))))
            #// Overlay Background Color ------
            wp_customize.add_setting("cover_template_overlay_background_color", Array({"default": twentytwenty_get_color_for_area("content", "accent"), "sanitize_callback": "sanitize_hex_color"}))
            wp_customize.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(wp_customize, "cover_template_overlay_background_color", Array({"label": __("Overlay Background Color", "twentytwenty"), "description": __("The color used for the overlay. Defaults to the accent color.", "twentytwenty"), "section": "cover_template_options"}))))
            #// Overlay Text Color ------------
            wp_customize.add_setting("cover_template_overlay_text_color", Array({"default": "#ffffff", "sanitize_callback": "sanitize_hex_color"}))
            wp_customize.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(wp_customize, "cover_template_overlay_text_color", Array({"label": __("Overlay Text Color", "twentytwenty"), "description": __("The color used for the text in the overlay.", "twentytwenty"), "section": "cover_template_options"}))))
            #// Overlay Color Opacity ---------
            wp_customize.add_setting("cover_template_overlay_opacity", Array({"default": 80, "sanitize_callback": "absint", "transport": "postMessage"}))
            wp_customize.add_control("cover_template_overlay_opacity", Array({"label": __("Overlay Opacity", "twentytwenty"), "description": __("Make sure that the contrast is high enough so that the text is readable.", "twentytwenty"), "section": "cover_template_options", "type": "range", "input_attrs": twentytwenty_customize_opacity_range()}))
            wp_customize.selective_refresh.add_partial("cover_template_overlay_opacity", Array({"selector": ".cover-color-overlay", "type": "cover_opacity"}))
        # end def register
        #// 
        #// Sanitization callback for the "accent_accessible_colors" setting.
        #// 
        #// @static
        #// @access public
        #// @since Twenty Twenty 1.0
        #// @param array $value The value we want to sanitize.
        #// @return array       Returns sanitized value. Each item in the array gets sanitized separately.
        #//
        @classmethod
        def sanitize_accent_accessible_colors(self, value=None):
            
            #// Make sure the value is an array. Do not typecast, use empty array as fallback.
            value = value if php_is_array(value) else Array()
            #// Loop values.
            for area,values in value:
                for context,color_val in values:
                    value[area][context] = sanitize_hex_color(color_val)
                # end for
            # end for
            return value
        # end def sanitize_accent_accessible_colors
        #// 
        #// Sanitize select.
        #// 
        #// @param string $input The input from the setting.
        #// @param object $setting The selected setting.
        #// 
        #// @return string $input|$setting->default The input from the setting or the default setting.
        #//
        @classmethod
        def sanitize_select(self, input=None, setting=None):
            
            input = sanitize_key(input)
            choices = setting.manager.get_control(setting.id).choices
            return input if php_array_key_exists(input, choices) else setting.default
        # end def sanitize_select
        #// 
        #// Sanitize boolean for checkbox.
        #// 
        #// @param bool $checked Whether or not a box is checked.
        #// 
        #// @return bool
        #//
        @classmethod
        def sanitize_checkbox(self, checked=None):
            
            return True if (php_isset(lambda : checked)) and True == checked else False
        # end def sanitize_checkbox
    # end class TwentyTwenty_Customize
    #// Setup the Theme Customizer settings and controls.
    add_action("customize_register", Array("TwentyTwenty_Customize", "register"))
# end if
#// 
#// PARTIAL REFRESH FUNCTIONS
#//
if (not php_function_exists("twentytwenty_customize_partial_blogname")):
    #// 
    #// Render the site title for the selective refresh partial.
    #//
    def twentytwenty_customize_partial_blogname(*args_):
        
        bloginfo("name")
    # end def twentytwenty_customize_partial_blogname
# end if
if (not php_function_exists("twentytwenty_customize_partial_blogdescription")):
    #// 
    #// Render the site description for the selective refresh partial.
    #//
    def twentytwenty_customize_partial_blogdescription(*args_):
        
        bloginfo("description")
    # end def twentytwenty_customize_partial_blogdescription
# end if
if (not php_function_exists("twentytwenty_customize_partial_site_logo")):
    #// 
    #// Render the site logo for the selective refresh partial.
    #// 
    #// Doing it this way so we don't have issues with `render_callback`'s arguments.
    #//
    def twentytwenty_customize_partial_site_logo(*args_):
        
        twentytwenty_site_logo()
    # end def twentytwenty_customize_partial_site_logo
# end if
#// 
#// Input attributes for cover overlay opacity option.
#// 
#// @return array Array containing attribute names and their values.
#//
def twentytwenty_customize_opacity_range(*args_):
    
    #// 
    #// Filter the input attributes for opacity
    #// 
    #// @param array $attrs {
    #// The attributes
    #// 
    #// @type int $min Minimum value
    #// @type int $max Maximum value
    #// @type int $step Interval between numbers
    #// }
    #//
    return apply_filters("twentytwenty_customize_opacity_range", Array({"min": 0, "max": 90, "step": 5}))
# end def twentytwenty_customize_opacity_range
