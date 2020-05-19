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
        def start_el(self, output_=None, page_=None, depth_=0, args_=None, current_page_=0):
            if args_ is None:
                args_ = Array()
            # end if
            
            if (php_isset(lambda : args_["item_spacing"])) and "preserve" == args_["item_spacing"]:
                t_ = "  "
                n_ = "\n"
            else:
                t_ = ""
                n_ = ""
            # end if
            if depth_:
                indent_ = php_str_repeat(t_, depth_)
            else:
                indent_ = ""
            # end if
            css_class_ = Array("page_item", "page-item-" + page_.ID)
            if (php_isset(lambda : args_["pages_with_children"][page_.ID])):
                css_class_[-1] = "page_item_has_children"
            # end if
            if (not php_empty(lambda : current_page_)):
                _current_page_ = get_post(current_page_)
                if _current_page_ and php_in_array(page_.ID, _current_page_.ancestors, True):
                    css_class_[-1] = "current_page_ancestor"
                # end if
                if page_.ID == current_page_:
                    css_class_[-1] = "current_page_item"
                elif _current_page_ and page_.ID == _current_page_.post_parent:
                    css_class_[-1] = "current_page_parent"
                # end if
            elif get_option("page_for_posts") == page_.ID:
                css_class_[-1] = "current_page_parent"
            # end if
            #// This filter is documented in wp-includes/class-walker-page.php
            css_classes_ = php_implode(" ", apply_filters("page_css_class", css_class_, page_, depth_, args_, current_page_))
            css_classes_ = " class=\"" + esc_attr(css_classes_) + "\"" if css_classes_ else ""
            if "" == page_.post_title:
                #// translators: %d: ID of a post.
                page_.post_title = php_sprintf(__("#%d (no title)", "twentytwenty"), page_.ID)
            # end if
            args_["link_before"] = "" if php_empty(lambda : args_["link_before"]) else args_["link_before"]
            args_["link_after"] = "" if php_empty(lambda : args_["link_after"]) else args_["link_after"]
            atts_ = Array()
            atts_["href"] = get_permalink(page_.ID)
            atts_["aria-current"] = "page" if page_.ID == current_page_ else ""
            #// This filter is documented in wp-includes/class-walker-page.php
            atts_ = apply_filters("page_menu_link_attributes", atts_, page_, depth_, args_, current_page_)
            attributes_ = ""
            for attr_,value_ in atts_.items():
                if (not php_empty(lambda : value_)):
                    value_ = esc_url(value_) if "href" == attr_ else esc_attr(value_)
                    attributes_ += " " + attr_ + "=\"" + value_ + "\""
                # end if
            # end for
            args_["list_item_before"] = ""
            args_["list_item_after"] = ""
            #// Wrap the link in a div and append a sub menu toggle.
            if (php_isset(lambda : args_["show_toggles"])) and True == args_["show_toggles"]:
                #// Wrap the menu item link contents in a div, used for positioning.
                args_["list_item_before"] = "<div class=\"ancestor-wrapper\">"
                args_["list_item_after"] = ""
                #// Add a toggle to items with children.
                if (php_isset(lambda : args_["pages_with_children"][page_.ID])):
                    toggle_target_string_ = ".menu-modal .page-item-" + page_.ID + " > ul"
                    toggle_duration_ = twentytwenty_toggle_duration()
                    #// Add the sub menu toggle.
                    args_["list_item_after"] += "<button class=\"toggle sub-menu-toggle fill-children-current-color\" data-toggle-target=\"" + toggle_target_string_ + "\" data-toggle-type=\"slidetoggle\" data-toggle-duration=\"" + absint(toggle_duration_) + "\" aria-expanded=\"false\"><span class=\"screen-reader-text\">" + __("Show sub menu", "twentytwenty") + "</span>" + twentytwenty_get_theme_svg("chevron-down") + "</button>"
                # end if
                #// Close the wrapper.
                args_["list_item_after"] += "</div><!-- .ancestor-wrapper -->"
            # end if
            #// Add icons to menu items with children.
            if (php_isset(lambda : args_["show_sub_menu_icons"])) and True == args_["show_sub_menu_icons"]:
                if (php_isset(lambda : args_["pages_with_children"][page_.ID])):
                    args_["list_item_after"] = "<span class=\"icon\"></span>"
                # end if
            # end if
            output_ += indent_ + php_sprintf("<li%s>%s<a%s>%s%s%s</a>%s", css_classes_, args_["list_item_before"], attributes_, args_["link_before"], apply_filters("the_title", page_.post_title, page_.ID), args_["link_after"], args_["list_item_after"])
            if (not php_empty(lambda : args_["show_date"])):
                if "modified" == args_["show_date"]:
                    time_ = page_.post_modified
                else:
                    time_ = page_.post_date
                # end if
                date_format_ = "" if php_empty(lambda : args_["date_format"]) else args_["date_format"]
                output_ += " " + mysql2date(date_format_, time_)
            # end if
        # end def start_el
    # end class TwentyTwenty_Walker_Page
# end if
