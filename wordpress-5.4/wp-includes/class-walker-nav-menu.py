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
#// Nav Menu API: Walker_Nav_Menu class
#// 
#// @package WordPress
#// @subpackage Nav_Menus
#// @since 4.6.0
#// 
#// 
#// Core class used to implement an HTML list of nav menu items.
#// 
#// @since 3.0.0
#// 
#// @see Walker
#//
class Walker_Nav_Menu(Walker):
    tree_type = Array("post_type", "taxonomy", "custom")
    db_fields = Array({"parent": "menu_item_parent", "id": "db_id"})
    #// 
    #// Starts the list before the elements are added.
    #// 
    #// @since 3.0.0
    #// 
    #// @see Walker::start_lvl()
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param int      $depth  Depth of menu item. Used for padding.
    #// @param stdClass $args   An object of wp_nav_menu() arguments.
    #//
    def start_lvl(self, output=None, depth=0, args=None):
        
        if (php_isset(lambda : args.item_spacing)) and "discard" == args.item_spacing:
            t = ""
            n = ""
        else:
            t = "   "
            n = "\n"
        # end if
        indent = php_str_repeat(t, depth)
        #// Default class.
        classes = Array("sub-menu")
        #// 
        #// Filters the CSS class(es) applied to a menu list element.
        #// 
        #// @since 4.8.0
        #// 
        #// @param string[] $classes Array of the CSS classes that are applied to the menu `<ul>` element.
        #// @param stdClass $args    An object of `wp_nav_menu()` arguments.
        #// @param int      $depth   Depth of menu item. Used for padding.
        #//
        class_names = join(" ", apply_filters("nav_menu_submenu_css_class", classes, args, depth))
        class_names = " class=\"" + esc_attr(class_names) + "\"" if class_names else ""
        output += str(n) + str(indent) + str("<ul") + str(class_names) + str(">") + str(n)
    # end def start_lvl
    #// 
    #// Ends the list of after the elements are added.
    #// 
    #// @since 3.0.0
    #// 
    #// @see Walker::end_lvl()
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param int      $depth  Depth of menu item. Used for padding.
    #// @param stdClass $args   An object of wp_nav_menu() arguments.
    #//
    def end_lvl(self, output=None, depth=0, args=None):
        
        if (php_isset(lambda : args.item_spacing)) and "discard" == args.item_spacing:
            t = ""
            n = ""
        else:
            t = "   "
            n = "\n"
        # end if
        indent = php_str_repeat(t, depth)
        output += str(indent) + str("</ul>") + str(n)
    # end def end_lvl
    #// 
    #// Starts the element output.
    #// 
    #// @since 3.0.0
    #// @since 4.4.0 The {@see 'nav_menu_item_args'} filter was added.
    #// 
    #// @see Walker::start_el()
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param WP_Post  $item   Menu item data object.
    #// @param int      $depth  Depth of menu item. Used for padding.
    #// @param stdClass $args   An object of wp_nav_menu() arguments.
    #// @param int      $id     Current item ID.
    #//
    def start_el(self, output=None, item=None, depth=0, args=None, id=0):
        
        if (php_isset(lambda : args.item_spacing)) and "discard" == args.item_spacing:
            t = ""
            n = ""
        else:
            t = "   "
            n = "\n"
        # end if
        indent = php_str_repeat(t, depth) if depth else ""
        classes = Array() if php_empty(lambda : item.classes) else item.classes
        classes[-1] = "menu-item-" + item.ID
        #// 
        #// Filters the arguments for a single nav menu item.
        #// 
        #// @since 4.4.0
        #// 
        #// @param stdClass $args  An object of wp_nav_menu() arguments.
        #// @param WP_Post  $item  Menu item data object.
        #// @param int      $depth Depth of menu item. Used for padding.
        #//
        args = apply_filters("nav_menu_item_args", args, item, depth)
        #// 
        #// Filters the CSS classes applied to a menu item's list item element.
        #// 
        #// @since 3.0.0
        #// @since 4.1.0 The `$depth` parameter was added.
        #// 
        #// @param string[] $classes Array of the CSS classes that are applied to the menu item's `<li>` element.
        #// @param WP_Post  $item    The current menu item.
        #// @param stdClass $args    An object of wp_nav_menu() arguments.
        #// @param int      $depth   Depth of menu item. Used for padding.
        #//
        class_names = join(" ", apply_filters("nav_menu_css_class", php_array_filter(classes), item, args, depth))
        class_names = " class=\"" + esc_attr(class_names) + "\"" if class_names else ""
        #// 
        #// Filters the ID applied to a menu item's list item element.
        #// 
        #// @since 3.0.1
        #// @since 4.1.0 The `$depth` parameter was added.
        #// 
        #// @param string   $menu_id The ID that is applied to the menu item's `<li>` element.
        #// @param WP_Post  $item    The current menu item.
        #// @param stdClass $args    An object of wp_nav_menu() arguments.
        #// @param int      $depth   Depth of menu item. Used for padding.
        #//
        id = apply_filters("nav_menu_item_id", "menu-item-" + item.ID, item, args, depth)
        id = " id=\"" + esc_attr(id) + "\"" if id else ""
        output += indent + "<li" + id + class_names + ">"
        atts = Array()
        atts["title"] = item.attr_title if (not php_empty(lambda : item.attr_title)) else ""
        atts["target"] = item.target if (not php_empty(lambda : item.target)) else ""
        if "_blank" == item.target and php_empty(lambda : item.xfn):
            atts["rel"] = "noopener noreferrer"
        else:
            atts["rel"] = item.xfn
        # end if
        atts["href"] = item.url if (not php_empty(lambda : item.url)) else ""
        atts["aria-current"] = "page" if item.current else ""
        #// 
        #// Filters the HTML attributes applied to a menu item's anchor element.
        #// 
        #// @since 3.6.0
        #// @since 4.1.0 The `$depth` parameter was added.
        #// 
        #// @param array $atts {
        #// The HTML attributes applied to the menu item's `<a>` element, empty strings are ignored.
        #// 
        #// @type string $title        Title attribute.
        #// @type string $target       Target attribute.
        #// @type string $rel          The rel attribute.
        #// @type string $href         The href attribute.
        #// @type string $aria_current The aria-current attribute.
        #// }
        #// @param WP_Post  $item  The current menu item.
        #// @param stdClass $args  An object of wp_nav_menu() arguments.
        #// @param int      $depth Depth of menu item. Used for padding.
        #//
        atts = apply_filters("nav_menu_link_attributes", atts, item, args, depth)
        attributes = ""
        for attr,value in atts:
            if is_scalar(value) and "" != value and False != value:
                value = esc_url(value) if "href" == attr else esc_attr(value)
                attributes += " " + attr + "=\"" + value + "\""
            # end if
        # end for
        #// This filter is documented in wp-includes/post-template.php
        title = apply_filters("the_title", item.title, item.ID)
        #// 
        #// Filters a menu item's title.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string   $title The menu item's title.
        #// @param WP_Post  $item  The current menu item.
        #// @param stdClass $args  An object of wp_nav_menu() arguments.
        #// @param int      $depth Depth of menu item. Used for padding.
        #//
        title = apply_filters("nav_menu_item_title", title, item, args, depth)
        item_output = args.before
        item_output += "<a" + attributes + ">"
        item_output += args.link_before + title + args.link_after
        item_output += "</a>"
        item_output += args.after
        #// 
        #// Filters a menu item's starting output.
        #// 
        #// The menu item's starting output only includes `$args->before`, the opening `<a>`,
        #// the menu item's title, the closing `</a>`, and `$args->after`. Currently, there is
        #// no filter for modifying the opening and closing `<li>` for a menu item.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string   $item_output The menu item's starting HTML output.
        #// @param WP_Post  $item        Menu item data object.
        #// @param int      $depth       Depth of menu item. Used for padding.
        #// @param stdClass $args        An object of wp_nav_menu() arguments.
        #//
        output += apply_filters("walker_nav_menu_start_el", item_output, item, depth, args)
    # end def start_el
    #// 
    #// Ends the element output, if needed.
    #// 
    #// @since 3.0.0
    #// 
    #// @see Walker::end_el()
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param WP_Post  $item   Page data object. Not used.
    #// @param int      $depth  Depth of page. Not Used.
    #// @param stdClass $args   An object of wp_nav_menu() arguments.
    #//
    def end_el(self, output=None, item=None, depth=0, args=None):
        
        if (php_isset(lambda : args.item_spacing)) and "discard" == args.item_spacing:
            t = ""
            n = ""
        else:
            t = "   "
            n = "\n"
        # end if
        output += str("</li>") + str(n)
    # end def end_el
# end class Walker_Nav_Menu
