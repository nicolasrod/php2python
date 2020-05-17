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
def twentyseventeen_body_classes(classes_=None, *_args_):
    
    
    #// Add class of group-blog to blogs with more than 1 published author.
    if is_multi_author():
        classes_[-1] = "group-blog"
    # end if
    #// Add class of hfeed to non-singular pages.
    if (not is_singular()):
        classes_[-1] = "hfeed"
    # end if
    #// Add class if we're viewing the Customizer for easier styling of theme options.
    if is_customize_preview():
        classes_[-1] = "twentyseventeen-customizer"
    # end if
    #// Add class on front page.
    if is_front_page() and "posts" != get_option("show_on_front"):
        classes_[-1] = "twentyseventeen-front-page"
    # end if
    #// Add a class if there is a custom header.
    if has_header_image():
        classes_[-1] = "has-header-image"
    # end if
    #// Add class if sidebar is used.
    if is_active_sidebar("sidebar-1") and (not is_page()):
        classes_[-1] = "has-sidebar"
    # end if
    #// Add class for one or two column page layouts.
    if is_page() or is_archive():
        if "one-column" == get_theme_mod("page_layout"):
            classes_[-1] = "page-one-column"
        else:
            classes_[-1] = "page-two-column"
        # end if
    # end if
    #// Add class if the site title and tagline is hidden.
    if "blank" == get_header_textcolor():
        classes_[-1] = "title-tagline-hidden"
    # end if
    #// Get the colorscheme or the default if there isn't one.
    colors_ = twentyseventeen_sanitize_colorscheme(get_theme_mod("colorscheme", "light"))
    classes_[-1] = "colors-" + colors_
    return classes_
# end def twentyseventeen_body_classes
add_filter("body_class", "twentyseventeen_body_classes")
#// 
#// Count our number of active panels.
#// 
#// Primarily used to see if we have any panels active, duh.
#//
def twentyseventeen_panel_count(*_args_):
    
    
    panel_count_ = 0
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
        
        if get_theme_mod("panel_" + i_):
            panel_count_ += 1
        # end if
        i_ += 1
    # end while
    return panel_count_
# end def twentyseventeen_panel_count
#// 
#// Checks to see if we're on the front page or not.
#//
def twentyseventeen_is_frontpage(*_args_):
    
    
    return is_front_page() and (not is_home())
# end def twentyseventeen_is_frontpage
