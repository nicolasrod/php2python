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
#// Post API: Walker_Page class
#// 
#// @package WordPress
#// @subpackage Template
#// @since 4.4.0
#// 
#// 
#// Core walker class used to create an HTML list of pages.
#// 
#// @since 2.1.0
#// 
#// @see Walker
#//
class Walker_Page(Walker):
    tree_type = "page"
    db_fields = Array({"parent": "post_parent", "id": "ID"})
    #// 
    #// Outputs the beginning of the current level in the tree before elements are output.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::start_lvl()
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Optional. Depth of page. Used for padding. Default 0.
    #// @param array  $args   Optional. Arguments for outputting the next level.
    #// Default empty array.
    #//
    def start_lvl(self, output=None, depth=0, args=Array()):
        
        if (php_isset(lambda : args["item_spacing"])) and "preserve" == args["item_spacing"]:
            t = "   "
            n = "\n"
        else:
            t = ""
            n = ""
        # end if
        indent = php_str_repeat(t, depth)
        output += str(n) + str(indent) + str("<ul class='children'>") + str(n)
    # end def start_lvl
    #// 
    #// Outputs the end of the current level in the tree after elements are output.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::end_lvl()
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Optional. Depth of page. Used for padding. Default 0.
    #// @param array  $args   Optional. Arguments for outputting the end of the current level.
    #// Default empty array.
    #//
    def end_lvl(self, output=None, depth=0, args=Array()):
        
        if (php_isset(lambda : args["item_spacing"])) and "preserve" == args["item_spacing"]:
            t = "   "
            n = "\n"
        else:
            t = ""
            n = ""
        # end if
        indent = php_str_repeat(t, depth)
        output += str(indent) + str("</ul>") + str(n)
    # end def end_lvl
    #// 
    #// Outputs the beginning of the current element in the tree.
    #// 
    #// @see Walker::start_el()
    #// @since 2.1.0
    #// 
    #// @param string  $output       Used to append additional content. Passed by reference.
    #// @param WP_Post $page         Page data object.
    #// @param int     $depth        Optional. Depth of page. Used for padding. Default 0.
    #// @param array   $args         Optional. Array of arguments. Default empty array.
    #// @param int     $current_page Optional. Page ID. Default 0.
    #//
    def start_el(self, output=None, page=None, depth=0, args=Array(), current_page=0):
        
        if (php_isset(lambda : args["item_spacing"])) and "preserve" == args["item_spacing"]:
            t = "   "
            n = "\n"
        else:
            t = ""
            n = ""
        # end if
        if depth:
            indent = php_str_repeat(t, depth)
        else:
            indent = ""
        # end if
        css_class = Array("page_item", "page-item-" + page.ID)
        if (php_isset(lambda : args["pages_with_children"][page.ID])):
            css_class[-1] = "page_item_has_children"
        # end if
        if (not php_empty(lambda : current_page)):
            _current_page = get_post(current_page)
            if _current_page and php_in_array(page.ID, _current_page.ancestors):
                css_class[-1] = "current_page_ancestor"
            # end if
            if page.ID == current_page:
                css_class[-1] = "current_page_item"
            elif _current_page and page.ID == _current_page.post_parent:
                css_class[-1] = "current_page_parent"
            # end if
        elif get_option("page_for_posts") == page.ID:
            css_class[-1] = "current_page_parent"
        # end if
        #// 
        #// Filters the list of CSS classes to include with each page item in the list.
        #// 
        #// @since 2.8.0
        #// 
        #// @see wp_list_pages()
        #// 
        #// @param string[] $css_class    An array of CSS classes to be applied to each list item.
        #// @param WP_Post  $page         Page data object.
        #// @param int      $depth        Depth of page, used for padding.
        #// @param array    $args         An array of arguments.
        #// @param int      $current_page ID of the current page.
        #//
        css_classes = php_implode(" ", apply_filters("page_css_class", css_class, page, depth, args, current_page))
        css_classes = " class=\"" + esc_attr(css_classes) + "\"" if css_classes else ""
        if "" == page.post_title:
            #// translators: %d: ID of a post.
            page.post_title = php_sprintf(__("#%d (no title)"), page.ID)
        # end if
        args["link_before"] = "" if php_empty(lambda : args["link_before"]) else args["link_before"]
        args["link_after"] = "" if php_empty(lambda : args["link_after"]) else args["link_after"]
        atts = Array()
        atts["href"] = get_permalink(page.ID)
        atts["aria-current"] = "page" if page.ID == current_page else ""
        #// 
        #// Filters the HTML attributes applied to a page menu item's anchor element.
        #// 
        #// @since 4.8.0
        #// 
        #// @param array $atts {
        #// The HTML attributes applied to the menu item's `<a>` element, empty strings are ignored.
        #// 
        #// @type string $href         The href attribute.
        #// @type string $aria_current The aria-current attribute.
        #// }
        #// @param WP_Post $page         Page data object.
        #// @param int     $depth        Depth of page, used for padding.
        #// @param array   $args         An array of arguments.
        #// @param int     $current_page ID of the current page.
        #//
        atts = apply_filters("page_menu_link_attributes", atts, page, depth, args, current_page)
        attributes = ""
        for attr,value in atts:
            if is_scalar(value) and "" != value and False != value:
                value = esc_url(value) if "href" == attr else esc_attr(value)
                attributes += " " + attr + "=\"" + value + "\""
            # end if
        # end for
        output += indent + php_sprintf("<li%s><a%s>%s%s%s</a>", css_classes, attributes, args["link_before"], apply_filters("the_title", page.post_title, page.ID), args["link_after"])
        if (not php_empty(lambda : args["show_date"])):
            if "modified" == args["show_date"]:
                time = page.post_modified
            else:
                time = page.post_date
            # end if
            date_format = "" if php_empty(lambda : args["date_format"]) else args["date_format"]
            output += " " + mysql2date(date_format, time)
        # end if
    # end def start_el
    #// 
    #// Outputs the end of the current element in the tree.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::end_el()
    #// 
    #// @param string  $output Used to append additional content. Passed by reference.
    #// @param WP_Post $page   Page data object. Not used.
    #// @param int     $depth  Optional. Depth of page. Default 0 (unused).
    #// @param array   $args   Optional. Array of arguments. Default empty array.
    #//
    def end_el(self, output=None, page=None, depth=0, args=Array()):
        
        if (php_isset(lambda : args["item_spacing"])) and "preserve" == args["item_spacing"]:
            t = "   "
            n = "\n"
        else:
            t = ""
            n = ""
        # end if
        output += str("</li>") + str(n)
    # end def end_el
# end class Walker_Page
