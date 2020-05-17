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
#// SVG icons related functions
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#// 
#// 
#// Gets the SVG code for a given icon.
#//
def twentynineteen_get_icon_svg(icon_=None, size_=24, *_args_):
    
    
    return TwentyNineteen_SVG_Icons.get_svg("ui", icon_, size_)
# end def twentynineteen_get_icon_svg
#// 
#// Gets the SVG code for a given social icon.
#//
def twentynineteen_get_social_icon_svg(icon_=None, size_=24, *_args_):
    
    
    return TwentyNineteen_SVG_Icons.get_svg("social", icon_, size_)
# end def twentynineteen_get_social_icon_svg
#// 
#// Detects the social network from a URL and returns the SVG code for its icon.
#//
def twentynineteen_get_social_link_svg(uri_=None, size_=24, *_args_):
    
    
    return TwentyNineteen_SVG_Icons.get_social_link_svg(uri_, size_)
# end def twentynineteen_get_social_link_svg
#// 
#// Display SVG icons in social links menu.
#// 
#// @param  string  $item_output The menu item output.
#// @param  WP_Post $item        Menu item object.
#// @param  int     $depth       Depth of the menu.
#// @param  array   $args        wp_nav_menu() arguments.
#// @return string  $item_output The menu item output with social icon.
#//
def twentynineteen_nav_menu_social_icons(item_output_=None, item_=None, depth_=None, args_=None, *_args_):
    
    
    #// Change SVG icon inside social links menu if there is supported URL.
    if "social" == args_.theme_location:
        svg_ = twentynineteen_get_social_link_svg(item_.url, 26)
        if php_empty(lambda : svg_):
            svg_ = twentynineteen_get_icon_svg("link")
        # end if
        item_output_ = php_str_replace(args_.link_after, "</span>" + svg_, item_output_)
    # end if
    return item_output_
# end def twentynineteen_nav_menu_social_icons
add_filter("walker_nav_menu_start_el", "twentynineteen_nav_menu_social_icons", 10, 4)
#// 
#// Add a dropdown icon to top-level menu items.
#// 
#// @param string $output Nav menu item start element.
#// @param object $item   Nav menu item.
#// @param int    $depth  Depth.
#// @param object $args   Nav menu args.
#// @return string Nav menu item start element.
#// Add a dropdown icon to top-level menu items
#//
def twentynineteen_add_dropdown_icons(output_=None, item_=None, depth_=None, args_=None, *_args_):
    
    
    #// Only add class to 'top level' items on the 'primary' menu.
    if (not (php_isset(lambda : args_.theme_location))) or "menu-1" != args_.theme_location:
        return output_
    # end if
    if php_in_array("mobile-parent-nav-menu-item", item_.classes, True) and (php_isset(lambda : item_.original_id)):
        #// Inject the keyboard_arrow_left SVG inside the parent nav menu item, and let the item link to the parent item.
        #// @todo Only do this for nested submenus? If on a first-level submenu, then really the link could be "#" since the desire is to remove the target entirely.
        link_ = php_sprintf("<button class=\"menu-item-link-return\" tabindex=\"-1\">%s", twentynineteen_get_icon_svg("chevron_left", 24))
        #// Replace opening <a> with <button>.
        output_ = php_preg_replace("/<a\\s.*?>/", link_, output_, 1)
        #// Replace closing </a> with </button>.
        output_ = php_preg_replace("#</a>#i", "</button>", output_, 1)
    elif php_in_array("menu-item-has-children", item_.classes, True):
        #// Add SVG icon to parent items.
        icon_ = twentynineteen_get_icon_svg("keyboard_arrow_down", 24)
        output_ += php_sprintf("<button class=\"submenu-expand\" tabindex=\"-1\">%s</button>", icon_)
    # end if
    return output_
# end def twentynineteen_add_dropdown_icons
add_filter("walker_nav_menu_start_el", "twentynineteen_add_dropdown_icons", 10, 4)
