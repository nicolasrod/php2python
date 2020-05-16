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
#// Functions which enhance the theme by hooking into WordPress
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#// 
#// 
#// Adds custom classes to the array of body classes.
#// 
#// @param array $classes Classes for the body element.
#// @return array
#//
def twentynineteen_body_classes(classes=None, *args_):
    
    if is_singular():
        #// Adds `singular` to singular pages.
        classes[-1] = "singular"
    else:
        #// Adds `hfeed` to non singular pages.
        classes[-1] = "hfeed"
    # end if
    #// Adds a class if image filters are enabled.
    if twentynineteen_image_filters_enabled():
        classes[-1] = "image-filters-enabled"
    # end if
    return classes
# end def twentynineteen_body_classes
add_filter("body_class", "twentynineteen_body_classes")
#// 
#// Adds custom class to the array of posts classes.
#//
def twentynineteen_post_classes(classes=None, class_=None, post_id=None, *args_):
    
    classes[-1] = "entry"
    return classes
# end def twentynineteen_post_classes
add_filter("post_class", "twentynineteen_post_classes", 10, 3)
#// 
#// Add a pingback url auto-discovery header for single posts, pages, or attachments.
#//
def twentynineteen_pingback_header(*args_):
    
    if is_singular() and pings_open():
        php_print("<link rel=\"pingback\" href=\"", esc_url(get_bloginfo("pingback_url")), "\">")
    # end if
# end def twentynineteen_pingback_header
add_action("wp_head", "twentynineteen_pingback_header")
#// 
#// Changes comment form default fields.
#//
def twentynineteen_comment_form_defaults(defaults=None, *args_):
    
    comment_field = defaults["comment_field"]
    #// Adjust height of comment form.
    defaults["comment_field"] = php_preg_replace("/rows=\"\\d+\"/", "rows=\"5\"", comment_field)
    return defaults
# end def twentynineteen_comment_form_defaults
add_filter("comment_form_defaults", "twentynineteen_comment_form_defaults")
#// 
#// Filters the default archive titles.
#//
def twentynineteen_get_the_archive_title(*args_):
    
    if is_category():
        title = __("Category Archives: ", "twentynineteen") + "<span class=\"page-description\">" + single_term_title("", False) + "</span>"
    elif is_tag():
        title = __("Tag Archives: ", "twentynineteen") + "<span class=\"page-description\">" + single_term_title("", False) + "</span>"
    elif is_author():
        title = __("Author Archives: ", "twentynineteen") + "<span class=\"page-description\">" + get_the_author_meta("display_name") + "</span>"
    elif is_year():
        title = __("Yearly Archives: ", "twentynineteen") + "<span class=\"page-description\">" + get_the_date(_x("Y", "yearly archives date format", "twentynineteen")) + "</span>"
    elif is_month():
        title = __("Monthly Archives: ", "twentynineteen") + "<span class=\"page-description\">" + get_the_date(_x("F Y", "monthly archives date format", "twentynineteen")) + "</span>"
    elif is_day():
        title = __("Daily Archives: ", "twentynineteen") + "<span class=\"page-description\">" + get_the_date() + "</span>"
    elif is_post_type_archive():
        title = __("Post Type Archives: ", "twentynineteen") + "<span class=\"page-description\">" + post_type_archive_title("", False) + "</span>"
    elif is_tax():
        tax = get_taxonomy(get_queried_object().taxonomy)
        #// translators: %s: Taxonomy singular name.
        title = php_sprintf(esc_html__("%s Archives:", "twentynineteen"), tax.labels.singular_name)
    else:
        title = __("Archives:", "twentynineteen")
    # end if
    return title
# end def twentynineteen_get_the_archive_title
add_filter("get_the_archive_title", "twentynineteen_get_the_archive_title")
#// 
#// Add custom sizes attribute to responsive image functionality for post thumbnails.
#// 
#// @origin Twenty Nineteen 1.0
#// 
#// @param array $attr  Attributes for the image markup.
#// @return string Value for use in post thumbnail 'sizes' attribute.
#//
def twentynineteen_post_thumbnail_sizes_attr(attr=None, *args_):
    
    if is_admin():
        return attr
    # end if
    if (not is_singular()):
        attr["sizes"] = "(max-width: 34.9rem) calc(100vw - 2rem), (max-width: 53rem) calc(8 * (100vw / 12)), (min-width: 53rem) calc(6 * (100vw / 12)), 100vw"
    # end if
    return attr
# end def twentynineteen_post_thumbnail_sizes_attr
add_filter("wp_get_attachment_image_attributes", "twentynineteen_post_thumbnail_sizes_attr", 10, 1)
#// 
#// Add an extra menu to our nav for our priority+ navigation to use
#// 
#// @param object $nav_menu  Nav menu.
#// @param object $args      Nav menu args.
#// @return string More link for hidden menu items.
#//
def twentynineteen_add_ellipses_to_nav(nav_menu=None, args=None, *args_):
    
    if "menu-1" == args.theme_location:
        nav_menu += """
        <div class=\"main-menu-more\">
        <ul class=\"main-menu\">
        <li class=\"menu-item menu-item-has-children\">
        <button class=\"submenu-expand main-menu-more-toggle is-empty\" tabindex=\"-1\"
        aria-label=\"""" + esc_attr__("More", "twentynineteen") + "\" aria-haspopup=\"true\" aria-expanded=\"false\">" + twentynineteen_get_icon_svg("arrow_drop_down_ellipsis") + """
        </button>
        <ul class=\"sub-menu hidden-links\">
        <li class=\"mobile-parent-nav-menu-item\">
        <button class=\"menu-item-link-return\">""" + twentynineteen_get_icon_svg("chevron_left") + esc_html__("Back", "twentynineteen") + """
        </button>
        </li>
        </ul>
        </li>
        </ul>
        </div>"""
    # end if
    return nav_menu
# end def twentynineteen_add_ellipses_to_nav
add_filter("wp_nav_menu", "twentynineteen_add_ellipses_to_nav", 10, 2)
#// 
#// WCAG 2.0 Attributes for Dropdown Menus
#// 
#// Adjustments to menu attributes tot support WCAG 2.0 recommendations
#// for flyout and dropdown menus.
#// 
#// @ref https://www.w3.org/WAI/tutorials/menus/flyout
#//
def twentynineteen_nav_menu_link_attributes(atts=None, item=None, args=None, depth=None, *args_):
    
    #// Add [aria-haspopup] and [aria-expanded] to menu items that have children.
    item_has_children = php_in_array("menu-item-has-children", item.classes)
    if item_has_children:
        atts["aria-haspopup"] = "true"
        atts["aria-expanded"] = "false"
    # end if
    return atts
# end def twentynineteen_nav_menu_link_attributes
add_filter("nav_menu_link_attributes", "twentynineteen_nav_menu_link_attributes", 10, 4)
#// 
#// Create a nav menu item to be displayed on mobile to navigate from submenu back to the parent.
#// 
#// This duplicates each parent nav menu item and makes it the first child of itself.
#// 
#// @param array  $sorted_menu_items Sorted nav menu items.
#// @param object $args              Nav menu args.
#// @return array Amended nav menu items.
#//
def twentynineteen_add_mobile_parent_nav_menu_items(sorted_menu_items=None, args=None, *args_):
    
    twentynineteen_add_mobile_parent_nav_menu_items.pseudo_id = 0
    if (not (php_isset(lambda : args.theme_location))) or "menu-1" != args.theme_location:
        return sorted_menu_items
    # end if
    amended_menu_items = Array()
    for nav_menu_item in sorted_menu_items:
        amended_menu_items[-1] = nav_menu_item
        if php_in_array("menu-item-has-children", nav_menu_item.classes, True):
            parent_menu_item = copy.deepcopy(nav_menu_item)
            parent_menu_item.original_id = nav_menu_item.ID
            twentynineteen_add_mobile_parent_nav_menu_items.pseudo_id -= 1
            parent_menu_item.ID = twentynineteen_add_mobile_parent_nav_menu_items.pseudo_id
            parent_menu_item.db_id = parent_menu_item.ID
            parent_menu_item.object_id = parent_menu_item.ID
            parent_menu_item.classes = Array("mobile-parent-nav-menu-item")
            parent_menu_item.menu_item_parent = nav_menu_item.ID
            amended_menu_items[-1] = parent_menu_item
        # end if
    # end for
    return amended_menu_items
# end def twentynineteen_add_mobile_parent_nav_menu_items
add_filter("wp_nav_menu_objects", "twentynineteen_add_mobile_parent_nav_menu_items", 10, 2)
