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
#// Custom page walker for this theme.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if (not php_class_exists("TwentyTwenty_Walker_Page")):
    #// 
    #// CUSTOM PAGE WALKER
    #// A custom walker for pages.
    #//
    class TwentyTwenty_Walker_Page(Walker_Page):
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
                if _current_page and php_in_array(page.ID, _current_page.ancestors, True):
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
            #// This filter is documented in wp-includes/class-walker-page.php
            css_classes = php_implode(" ", apply_filters("page_css_class", css_class, page, depth, args, current_page))
            css_classes = " class=\"" + esc_attr(css_classes) + "\"" if css_classes else ""
            if "" == page.post_title:
                #// translators: %d: ID of a post.
                page.post_title = php_sprintf(__("#%d (no title)", "twentytwenty"), page.ID)
            # end if
            args["link_before"] = "" if php_empty(lambda : args["link_before"]) else args["link_before"]
            args["link_after"] = "" if php_empty(lambda : args["link_after"]) else args["link_after"]
            atts = Array()
            atts["href"] = get_permalink(page.ID)
            atts["aria-current"] = "page" if page.ID == current_page else ""
            #// This filter is documented in wp-includes/class-walker-page.php
            atts = apply_filters("page_menu_link_attributes", atts, page, depth, args, current_page)
            attributes = ""
            for attr,value in atts:
                if (not php_empty(lambda : value)):
                    value = esc_url(value) if "href" == attr else esc_attr(value)
                    attributes += " " + attr + "=\"" + value + "\""
                # end if
            # end for
            args["list_item_before"] = ""
            args["list_item_after"] = ""
            #// Wrap the link in a div and append a sub menu toggle.
            if (php_isset(lambda : args["show_toggles"])) and True == args["show_toggles"]:
                #// Wrap the menu item link contents in a div, used for positioning.
                args["list_item_before"] = "<div class=\"ancestor-wrapper\">"
                args["list_item_after"] = ""
                #// Add a toggle to items with children.
                if (php_isset(lambda : args["pages_with_children"][page.ID])):
                    toggle_target_string = ".menu-modal .page-item-" + page.ID + " > ul"
                    toggle_duration = twentytwenty_toggle_duration()
                    #// Add the sub menu toggle.
                    args["list_item_after"] += "<button class=\"toggle sub-menu-toggle fill-children-current-color\" data-toggle-target=\"" + toggle_target_string + "\" data-toggle-type=\"slidetoggle\" data-toggle-duration=\"" + absint(toggle_duration) + "\" aria-expanded=\"false\"><span class=\"screen-reader-text\">" + __("Show sub menu", "twentytwenty") + "</span>" + twentytwenty_get_theme_svg("chevron-down") + "</button>"
                # end if
                #// Close the wrapper.
                args["list_item_after"] += "</div><!-- .ancestor-wrapper -->"
            # end if
            #// Add icons to menu items with children.
            if (php_isset(lambda : args["show_sub_menu_icons"])) and True == args["show_sub_menu_icons"]:
                if (php_isset(lambda : args["pages_with_children"][page.ID])):
                    args["list_item_after"] = "<span class=\"icon\"></span>"
                # end if
            # end if
            output += indent + php_sprintf("<li%s>%s<a%s>%s%s%s</a>%s", css_classes, args["list_item_before"], attributes, args["link_before"], apply_filters("the_title", page.post_title, page.ID), args["link_after"], args["list_item_after"])
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
    # end class TwentyTwenty_Walker_Page
# end if
