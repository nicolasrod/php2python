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
#// Additional features to allow styling of the templates
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// 
#// 
#// Adds custom classes to the array of body classes.
#// 
#// @param array $classes Classes for the body element.
#// @return array
#//
def twentyseventeen_body_classes(classes=None, *args_):
    
    #// Add class of group-blog to blogs with more than 1 published author.
    if is_multi_author():
        classes[-1] = "group-blog"
    # end if
    #// Add class of hfeed to non-singular pages.
    if (not is_singular()):
        classes[-1] = "hfeed"
    # end if
    #// Add class if we're viewing the Customizer for easier styling of theme options.
    if is_customize_preview():
        classes[-1] = "twentyseventeen-customizer"
    # end if
    #// Add class on front page.
    if is_front_page() and "posts" != get_option("show_on_front"):
        classes[-1] = "twentyseventeen-front-page"
    # end if
    #// Add a class if there is a custom header.
    if has_header_image():
        classes[-1] = "has-header-image"
    # end if
    #// Add class if sidebar is used.
    if is_active_sidebar("sidebar-1") and (not is_page()):
        classes[-1] = "has-sidebar"
    # end if
    #// Add class for one or two column page layouts.
    if is_page() or is_archive():
        if "one-column" == get_theme_mod("page_layout"):
            classes[-1] = "page-one-column"
        else:
            classes[-1] = "page-two-column"
        # end if
    # end if
    #// Add class if the site title and tagline is hidden.
    if "blank" == get_header_textcolor():
        classes[-1] = "title-tagline-hidden"
    # end if
    #// Get the colorscheme or the default if there isn't one.
    colors = twentyseventeen_sanitize_colorscheme(get_theme_mod("colorscheme", "light"))
    classes[-1] = "colors-" + colors
    return classes
# end def twentyseventeen_body_classes
add_filter("body_class", "twentyseventeen_body_classes")
#// 
#// Count our number of active panels.
#// 
#// Primarily used to see if we have any panels active, duh.
#//
def twentyseventeen_panel_count(*args_):
    
    panel_count = 0
    #// 
    #// Filter number of front page sections in Twenty Seventeen.
    #// 
    #// @since Twenty Seventeen 1.0
    #// 
    #// @param int $num_sections Number of front page sections.
    #//
    num_sections = apply_filters("twentyseventeen_front_page_sections", 4)
    #// Create a setting and control for each of the sections available in the theme.
    i = 1
    while i < 1 + num_sections:
        
        if get_theme_mod("panel_" + i):
            panel_count += 1
        # end if
        i += 1
    # end while
    return panel_count
# end def twentyseventeen_panel_count
#// 
#// Checks to see if we're on the front page or not.
#//
def twentyseventeen_is_frontpage(*args_):
    
    return is_front_page() and (not is_home())
# end def twentyseventeen_is_frontpage
