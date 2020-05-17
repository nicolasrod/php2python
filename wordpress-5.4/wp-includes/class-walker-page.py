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
    #// 
    #// What the class handles.
    #// 
    #// @since 2.1.0
    #// @var string
    #// 
    #// @see Walker::$tree_type
    #//
    tree_type = "page"
    #// 
    #// Database fields to use.
    #// 
    #// @since 2.1.0
    #// @var array
    #// 
    #// @see Walker::$db_fields
    #// @todo Decouple this.
    #//
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
    def start_lvl(self, output_=None, depth_=0, args_=None):
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
        indent_ = php_str_repeat(t_, depth_)
        output_ += str(n_) + str(indent_) + str("<ul class='children'>") + str(n_)
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
    def end_lvl(self, output_=None, depth_=0, args_=None):
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
        indent_ = php_str_repeat(t_, depth_)
        output_ += str(indent_) + str("</ul>") + str(n_)
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
            if _current_page_ and php_in_array(page_.ID, _current_page_.ancestors):
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
        css_classes_ = php_implode(" ", apply_filters("page_css_class", css_class_, page_, depth_, args_, current_page_))
        css_classes_ = " class=\"" + esc_attr(css_classes_) + "\"" if css_classes_ else ""
        if "" == page_.post_title:
            #// translators: %d: ID of a post.
            page_.post_title = php_sprintf(__("#%d (no title)"), page_.ID)
        # end if
        args_["link_before"] = "" if php_empty(lambda : args_["link_before"]) else args_["link_before"]
        args_["link_after"] = "" if php_empty(lambda : args_["link_after"]) else args_["link_after"]
        atts_ = Array()
        atts_["href"] = get_permalink(page_.ID)
        atts_["aria-current"] = "page" if page_.ID == current_page_ else ""
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
        atts_ = apply_filters("page_menu_link_attributes", atts_, page_, depth_, args_, current_page_)
        attributes_ = ""
        for attr_,value_ in atts_:
            if php_is_scalar(value_) and "" != value_ and False != value_:
                value_ = esc_url(value_) if "href" == attr_ else esc_attr(value_)
                attributes_ += " " + attr_ + "=\"" + value_ + "\""
            # end if
        # end for
        output_ += indent_ + php_sprintf("<li%s><a%s>%s%s%s</a>", css_classes_, attributes_, args_["link_before"], apply_filters("the_title", page_.post_title, page_.ID), args_["link_after"])
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
    def end_el(self, output_=None, page_=None, depth_=0, args_=None):
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
        output_ += str("</li>") + str(n_)
    # end def end_el
# end class Walker_Page
