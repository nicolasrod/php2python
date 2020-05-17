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
    #// 
    #// What the class handles.
    #// 
    #// @since 3.0.0
    #// @var string
    #// 
    #// @see Walker::$tree_type
    #//
    tree_type = Array("post_type", "taxonomy", "custom")
    #// 
    #// Database fields to use.
    #// 
    #// @since 3.0.0
    #// @todo Decouple this.
    #// @var array
    #// 
    #// @see Walker::$db_fields
    #//
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
    def start_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = None
        # end if
        
        if (php_isset(lambda : args_.item_spacing)) and "discard" == args_.item_spacing:
            t_ = ""
            n_ = ""
        else:
            t_ = "  "
            n_ = "\n"
        # end if
        indent_ = php_str_repeat(t_, depth_)
        #// Default class.
        classes_ = Array("sub-menu")
        #// 
        #// Filters the CSS class(es) applied to a menu list element.
        #// 
        #// @since 4.8.0
        #// 
        #// @param string[] $classes Array of the CSS classes that are applied to the menu `<ul>` element.
        #// @param stdClass $args    An object of `wp_nav_menu()` arguments.
        #// @param int      $depth   Depth of menu item. Used for padding.
        #//
        class_names_ = join(" ", apply_filters("nav_menu_submenu_css_class", classes_, args_, depth_))
        class_names_ = " class=\"" + esc_attr(class_names_) + "\"" if class_names_ else ""
        output_ += str(n_) + str(indent_) + str("<ul") + str(class_names_) + str(">") + str(n_)
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
    def end_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = None
        # end if
        
        if (php_isset(lambda : args_.item_spacing)) and "discard" == args_.item_spacing:
            t_ = ""
            n_ = ""
        else:
            t_ = "  "
            n_ = "\n"
        # end if
        indent_ = php_str_repeat(t_, depth_)
        output_ += str(indent_) + str("</ul>") + str(n_)
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
    def start_el(self, output_=None, item_=None, depth_=0, args_=None, id_=0):
        if args_ is None:
            args_ = None
        # end if
        
        if (php_isset(lambda : args_.item_spacing)) and "discard" == args_.item_spacing:
            t_ = ""
            n_ = ""
        else:
            t_ = "  "
            n_ = "\n"
        # end if
        indent_ = php_str_repeat(t_, depth_) if depth_ else ""
        classes_ = Array() if php_empty(lambda : item_.classes) else item_.classes
        classes_[-1] = "menu-item-" + item_.ID
        #// 
        #// Filters the arguments for a single nav menu item.
        #// 
        #// @since 4.4.0
        #// 
        #// @param stdClass $args  An object of wp_nav_menu() arguments.
        #// @param WP_Post  $item  Menu item data object.
        #// @param int      $depth Depth of menu item. Used for padding.
        #//
        args_ = apply_filters("nav_menu_item_args", args_, item_, depth_)
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
        class_names_ = join(" ", apply_filters("nav_menu_css_class", php_array_filter(classes_), item_, args_, depth_))
        class_names_ = " class=\"" + esc_attr(class_names_) + "\"" if class_names_ else ""
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
        id_ = apply_filters("nav_menu_item_id", "menu-item-" + item_.ID, item_, args_, depth_)
        id_ = " id=\"" + esc_attr(id_) + "\"" if id_ else ""
        output_ += indent_ + "<li" + id_ + class_names_ + ">"
        atts_ = Array()
        atts_["title"] = item_.attr_title if (not php_empty(lambda : item_.attr_title)) else ""
        atts_["target"] = item_.target if (not php_empty(lambda : item_.target)) else ""
        if "_blank" == item_.target and php_empty(lambda : item_.xfn):
            atts_["rel"] = "noopener noreferrer"
        else:
            atts_["rel"] = item_.xfn
        # end if
        atts_["href"] = item_.url if (not php_empty(lambda : item_.url)) else ""
        atts_["aria-current"] = "page" if item_.current else ""
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
        atts_ = apply_filters("nav_menu_link_attributes", atts_, item_, args_, depth_)
        attributes_ = ""
        for attr_,value_ in atts_:
            if php_is_scalar(value_) and "" != value_ and False != value_:
                value_ = esc_url(value_) if "href" == attr_ else esc_attr(value_)
                attributes_ += " " + attr_ + "=\"" + value_ + "\""
            # end if
        # end for
        #// This filter is documented in wp-includes/post-template.php
        title_ = apply_filters("the_title", item_.title, item_.ID)
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
        title_ = apply_filters("nav_menu_item_title", title_, item_, args_, depth_)
        item_output_ = args_.before
        item_output_ += "<a" + attributes_ + ">"
        item_output_ += args_.link_before + title_ + args_.link_after
        item_output_ += "</a>"
        item_output_ += args_.after
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
        output_ += apply_filters("walker_nav_menu_start_el", item_output_, item_, depth_, args_)
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
    def end_el(self, output_=None, item_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = None
        # end if
        
        if (php_isset(lambda : args_.item_spacing)) and "discard" == args_.item_spacing:
            t_ = ""
            n_ = ""
        else:
            t_ = "  "
            n_ = "\n"
        # end if
        output_ += str("</li>") + str(n_)
    # end def end_el
# end class Walker_Nav_Menu
