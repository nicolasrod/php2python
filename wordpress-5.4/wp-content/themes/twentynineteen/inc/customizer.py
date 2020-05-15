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
#// Twenty Nineteen: Customizer
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#// 
#// 
#// Add postMessage support for site title and description for the Theme Customizer.
#// 
#// @param WP_Customize_Manager $wp_customize Theme Customizer object.
#//
def twentynineteen_customize_register(wp_customize=None, *args_):
    
    wp_customize.get_setting("blogname").transport = "postMessage"
    wp_customize.get_setting("blogdescription").transport = "postMessage"
    wp_customize.get_setting("header_textcolor").transport = "postMessage"
    if (php_isset(lambda : wp_customize.selective_refresh)):
        wp_customize.selective_refresh.add_partial("blogname", Array({"selector": ".site-title a", "render_callback": "twentynineteen_customize_partial_blogname"}))
        wp_customize.selective_refresh.add_partial("blogdescription", Array({"selector": ".site-description", "render_callback": "twentynineteen_customize_partial_blogdescription"}))
    # end if
    #// 
    #// Primary color.
    #//
    wp_customize.add_setting("primary_color", Array({"default": "default", "transport": "postMessage", "sanitize_callback": "twentynineteen_sanitize_color_option"}))
    wp_customize.add_control("primary_color", Array({"type": "radio", "label": __("Primary Color", "twentynineteen"), "choices": Array({"default": _x("Default", "primary color", "twentynineteen"), "custom": _x("Custom", "primary color", "twentynineteen")})}, {"section": "colors", "priority": 5}))
    #// Add primary color hue setting and control.
    wp_customize.add_setting("primary_color_hue", Array({"default": 199, "transport": "postMessage", "sanitize_callback": "absint"}))
    wp_customize.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(wp_customize, "primary_color_hue", Array({"description": __("Apply a custom color for buttons, links, featured images, etc.", "twentynineteen"), "section": "colors", "mode": "hue"}))))
    #// Add image filter setting and control.
    wp_customize.add_setting("image_filter", Array({"default": 1, "sanitize_callback": "absint", "transport": "postMessage"}))
    wp_customize.add_control("image_filter", Array({"label": __("Apply a filter to featured images using the primary color", "twentynineteen"), "section": "colors", "type": "checkbox"}))
# end def twentynineteen_customize_register
add_action("customize_register", "twentynineteen_customize_register")
#// 
#// Render the site title for the selective refresh partial.
#// 
#// @return void
#//
def twentynineteen_customize_partial_blogname(*args_):
    
    bloginfo("name")
# end def twentynineteen_customize_partial_blogname
#// 
#// Render the site tagline for the selective refresh partial.
#// 
#// @return void
#//
def twentynineteen_customize_partial_blogdescription(*args_):
    
    bloginfo("description")
# end def twentynineteen_customize_partial_blogdescription
#// 
#// Bind JS handlers to instantly live-preview changes.
#//
def twentynineteen_customize_preview_js(*args_):
    
    wp_enqueue_script("twentynineteen-customize-preview", get_theme_file_uri("/js/customize-preview.js"), Array("customize-preview"), "20181214", True)
# end def twentynineteen_customize_preview_js
add_action("customize_preview_init", "twentynineteen_customize_preview_js")
#// 
#// Load dynamic logic for the customizer controls area.
#//
def twentynineteen_panels_js(*args_):
    
    wp_enqueue_script("twentynineteen-customize-controls", get_theme_file_uri("/js/customize-controls.js"), Array(), "20181214", True)
# end def twentynineteen_panels_js
add_action("customize_controls_enqueue_scripts", "twentynineteen_panels_js")
#// 
#// Sanitize custom color choice.
#// 
#// @param string $choice Whether image filter is active.
#// 
#// @return string
#//
def twentynineteen_sanitize_color_option(choice=None, *args_):
    
    valid = Array("default", "custom")
    if php_in_array(choice, valid, True):
        return choice
    # end if
    return "default"
# end def twentynineteen_sanitize_color_option
