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
#// Twenty Seventeen: Customizer
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// 
#// 
#// Add postMessage support for site title and description for the Theme Customizer.
#// 
#// @param WP_Customize_Manager $wp_customize Theme Customizer object.
#//
def twentyseventeen_customize_register(wp_customize_=None, *_args_):
    
    
    wp_customize_.get_setting("blogname").transport = "postMessage"
    wp_customize_.get_setting("blogdescription").transport = "postMessage"
    wp_customize_.get_setting("header_textcolor").transport = "postMessage"
    wp_customize_.selective_refresh.add_partial("blogname", Array({"selector": ".site-title a", "render_callback": "twentyseventeen_customize_partial_blogname"}))
    wp_customize_.selective_refresh.add_partial("blogdescription", Array({"selector": ".site-description", "render_callback": "twentyseventeen_customize_partial_blogdescription"}))
    #// 
    #// Custom colors.
    #//
    wp_customize_.add_setting("colorscheme", Array({"default": "light", "transport": "postMessage", "sanitize_callback": "twentyseventeen_sanitize_colorscheme"}))
    wp_customize_.add_setting("colorscheme_hue", Array({"default": 250, "transport": "postMessage", "sanitize_callback": "absint"}))
    wp_customize_.add_control("colorscheme", Array({"type": "radio", "label": __("Color Scheme", "twentyseventeen"), "choices": Array({"light": __("Light", "twentyseventeen"), "dark": __("Dark", "twentyseventeen"), "custom": __("Custom", "twentyseventeen")})}, {"section": "colors", "priority": 5}))
    wp_customize_.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(wp_customize_, "colorscheme_hue", Array({"mode": "hue", "section": "colors", "priority": 6}))))
    #// 
    #// Theme options.
    #//
    wp_customize_.add_section("theme_options", Array({"title": __("Theme Options", "twentyseventeen"), "priority": 130}))
    wp_customize_.add_setting("page_layout", Array({"default": "two-column", "sanitize_callback": "twentyseventeen_sanitize_page_layout", "transport": "postMessage"}))
    wp_customize_.add_control("page_layout", Array({"label": __("Page Layout", "twentyseventeen"), "section": "theme_options", "type": "radio", "description": __("When the two-column layout is assigned, the page title is in one column and content is in the other.", "twentyseventeen"), "choices": Array({"one-column": __("One Column", "twentyseventeen"), "two-column": __("Two Column", "twentyseventeen")})}, {"active_callback": "twentyseventeen_is_view_with_layout_option"}))
    #// 
    #// Filter number of front page sections in Twenty Seventeen.
    #// 
    #// @since Twenty Seventeen 1.0
    #// 
    #// @param int $num_sections Number of front page sections.
    #//
    num_sections_ = apply_filters("twentyseventeen_front_page_sections", 4)
    #// Create a setting and control for each of the sections available in the theme.
    i_ = 1
    while i_ < 1 + num_sections_:
        
        wp_customize_.add_setting("panel_" + i_, Array({"default": False, "sanitize_callback": "absint", "transport": "postMessage"}))
        wp_customize_.add_control("panel_" + i_, Array({"label": php_sprintf(__("Front Page Section %d Content", "twentyseventeen"), i_), "description": "" if 1 != i_ else __("Select pages to feature in each area from the dropdowns. Add an image to a section by setting a featured image in the page editor. Empty sections will not be displayed.", "twentyseventeen"), "section": "theme_options", "type": "dropdown-pages", "allow_addition": True, "active_callback": "twentyseventeen_is_static_front_page"}))
        wp_customize_.selective_refresh.add_partial("panel_" + i_, Array({"selector": "#panel" + i_, "render_callback": "twentyseventeen_front_page_section", "container_inclusive": True}))
        i_ += 1
    # end while
# end def twentyseventeen_customize_register
add_action("customize_register", "twentyseventeen_customize_register")
#// 
#// Sanitize the page layout options.
#// 
#// @param string $input Page layout.
#//
def twentyseventeen_sanitize_page_layout(input_=None, *_args_):
    
    
    valid_ = Array({"one-column": __("One Column", "twentyseventeen"), "two-column": __("Two Column", "twentyseventeen")})
    if php_array_key_exists(input_, valid_):
        return input_
    # end if
    return ""
# end def twentyseventeen_sanitize_page_layout
#// 
#// Sanitize the colorscheme.
#// 
#// @param string $input Color scheme.
#//
def twentyseventeen_sanitize_colorscheme(input_=None, *_args_):
    
    
    valid_ = Array("light", "dark", "custom")
    if php_in_array(input_, valid_, True):
        return input_
    # end if
    return "light"
# end def twentyseventeen_sanitize_colorscheme
#// 
#// Render the site title for the selective refresh partial.
#// 
#// @since Twenty Seventeen 1.0
#// @see twentyseventeen_customize_register()
#// 
#// @return void
#//
def twentyseventeen_customize_partial_blogname(*_args_):
    
    
    bloginfo("name")
# end def twentyseventeen_customize_partial_blogname
#// 
#// Render the site tagline for the selective refresh partial.
#// 
#// @since Twenty Seventeen 1.0
#// @see twentyseventeen_customize_register()
#// 
#// @return void
#//
def twentyseventeen_customize_partial_blogdescription(*_args_):
    
    
    bloginfo("description")
# end def twentyseventeen_customize_partial_blogdescription
#// 
#// Return whether we're previewing the front page and it's a static page.
#//
def twentyseventeen_is_static_front_page(*_args_):
    
    
    return is_front_page() and (not is_home())
# end def twentyseventeen_is_static_front_page
#// 
#// Return whether we're on a view that supports a one or two column layout.
#//
def twentyseventeen_is_view_with_layout_option(*_args_):
    
    
    #// This option is available on all pages. It's also available on archives when there isn't a sidebar.
    return is_page() or is_archive() and (not is_active_sidebar("sidebar-1"))
# end def twentyseventeen_is_view_with_layout_option
#// 
#// Bind JS handlers to instantly live-preview changes.
#//
def twentyseventeen_customize_preview_js(*_args_):
    
    
    wp_enqueue_script("twentyseventeen-customize-preview", get_theme_file_uri("/assets/js/customize-preview.js"), Array("customize-preview"), "20161002", True)
# end def twentyseventeen_customize_preview_js
add_action("customize_preview_init", "twentyseventeen_customize_preview_js")
#// 
#// Load dynamic logic for the customizer controls area.
#//
def twentyseventeen_panels_js(*_args_):
    
    
    wp_enqueue_script("twentyseventeen-customize-controls", get_theme_file_uri("/assets/js/customize-controls.js"), Array(), "20161020", True)
# end def twentyseventeen_panels_js
add_action("customize_controls_enqueue_scripts", "twentyseventeen_panels_js")
