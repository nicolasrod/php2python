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
#// Taxonomy API: Walker_Category class
#// 
#// @package WordPress
#// @subpackage Template
#// @since 4.4.0
#// 
#// 
#// Core class used to create an HTML list of categories.
#// 
#// @since 2.1.0
#// 
#// @see Walker
#//
class Walker_Category(Walker):
    tree_type = "category"
    db_fields = Array({"parent": "parent", "id": "term_id"})
    #// 
    #// Starts the list before the elements are added.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::start_lvl()
    #// 
    #// @param string $output Used to append additional content. Passed by reference.
    #// @param int    $depth  Optional. Depth of category. Used for tab indentation. Default 0.
    #// @param array  $args   Optional. An array of arguments. Will only append content if style argument
    #// value is 'list'. See wp_list_categories(). Default empty array.
    #//
    def start_lvl(self, output=None, depth=0, args=Array()):
        
        if "list" != args["style"]:
            return
        # end if
        indent = php_str_repeat("   ", depth)
        output += str(indent) + str("<ul class='children'>\n")
    # end def start_lvl
    #// 
    #// Ends the list of after the elements are added.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::end_lvl()
    #// 
    #// @param string $output Used to append additional content. Passed by reference.
    #// @param int    $depth  Optional. Depth of category. Used for tab indentation. Default 0.
    #// @param array  $args   Optional. An array of arguments. Will only append content if style argument
    #// value is 'list'. See wp_list_categories(). Default empty array.
    #//
    def end_lvl(self, output=None, depth=0, args=Array()):
        
        if "list" != args["style"]:
            return
        # end if
        indent = php_str_repeat("   ", depth)
        output += str(indent) + str("</ul>\n")
    # end def end_lvl
    #// 
    #// Starts the element output.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::start_el()
    #// 
    #// @param string $output   Used to append additional content (passed by reference).
    #// @param object $category Category data object.
    #// @param int    $depth    Optional. Depth of category in reference to parents. Default 0.
    #// @param array  $args     Optional. An array of arguments. See wp_list_categories(). Default empty array.
    #// @param int    $id       Optional. ID of the current category. Default 0.
    #//
    def start_el(self, output=None, category=None, depth=0, args=Array(), id=0):
        
        #// This filter is documented in wp-includes/category-template.php
        cat_name = apply_filters("list_cats", esc_attr(category.name), category)
        #// Don't generate an element if the category name is empty.
        if "" == cat_name:
            return
        # end if
        atts = Array()
        atts["href"] = get_term_link(category)
        if args["use_desc_for_title"] and (not php_empty(lambda : category.description)):
            #// 
            #// Filters the category description for display.
            #// 
            #// @since 1.2.0
            #// 
            #// @param string $description Category description.
            #// @param object $category    Category object.
            #//
            atts["title"] = strip_tags(apply_filters("category_description", category.description, category))
        # end if
        #// 
        #// Filters the HTML attributes applied to a category list item's anchor element.
        #// 
        #// @since 5.2.0
        #// 
        #// @param array   $atts {
        #// The HTML attributes applied to the list item's `<a>` element, empty strings are ignored.
        #// 
        #// @type string $href  The href attribute.
        #// @type string $title The title attribute.
        #// }
        #// @param WP_Term $category Term data object.
        #// @param int     $depth    Depth of category, used for padding.
        #// @param array   $args     An array of arguments.
        #// @param int     $id       ID of the current category.
        #//
        atts = apply_filters("category_list_link_attributes", atts, category, depth, args, id)
        attributes = ""
        for attr,value in atts:
            if is_scalar(value) and "" != value and False != value:
                value = esc_url(value) if "href" == attr else esc_attr(value)
                attributes += " " + attr + "=\"" + value + "\""
            # end if
        # end for
        link = php_sprintf("<a%s>%s</a>", attributes, cat_name)
        if (not php_empty(lambda : args["feed_image"])) or (not php_empty(lambda : args["feed"])):
            link += " "
            if php_empty(lambda : args["feed_image"]):
                link += "("
            # end if
            link += "<a href=\"" + esc_url(get_term_feed_link(category.term_id, category.taxonomy, args["feed_type"])) + "\""
            if php_empty(lambda : args["feed"]):
                #// translators: %s: Category name.
                alt = " alt=\"" + php_sprintf(__("Feed for all posts filed under %s"), cat_name) + "\""
            else:
                alt = " alt=\"" + args["feed"] + "\""
                name = args["feed"]
                link += "" if php_empty(lambda : args["title"]) else args["title"]
            # end if
            link += ">"
            if php_empty(lambda : args["feed_image"]):
                link += name
            else:
                link += "<img src='" + esc_url(args["feed_image"]) + str("'") + str(alt) + " />"
            # end if
            link += "</a>"
            if php_empty(lambda : args["feed_image"]):
                link += ")"
            # end if
        # end if
        if (not php_empty(lambda : args["show_count"])):
            link += " (" + number_format_i18n(category.count) + ")"
        # end if
        if "list" == args["style"]:
            output += " <li"
            css_classes = Array("cat-item", "cat-item-" + category.term_id)
            if (not php_empty(lambda : args["current_category"])):
                #// 'current_category' can be an array, so we use `get_terms()`.
                _current_terms = get_terms(Array({"taxonomy": category.taxonomy, "include": args["current_category"], "hide_empty": False}))
                for _current_term in _current_terms:
                    if category.term_id == _current_term.term_id:
                        css_classes[-1] = "current-cat"
                        link = php_str_replace("<a", "<a aria-current=\"page\"", link)
                    elif category.term_id == _current_term.parent:
                        css_classes[-1] = "current-cat-parent"
                    # end if
                    while True:
                        
                        if not (_current_term.parent):
                            break
                        # end if
                        if category.term_id == _current_term.parent:
                            css_classes[-1] = "current-cat-ancestor"
                            break
                        # end if
                        _current_term = get_term(_current_term.parent, category.taxonomy)
                    # end while
                # end for
            # end if
            #// 
            #// Filters the list of CSS classes to include with each category in the list.
            #// 
            #// @since 4.2.0
            #// 
            #// @see wp_list_categories()
            #// 
            #// @param array  $css_classes An array of CSS classes to be applied to each list item.
            #// @param object $category    Category data object.
            #// @param int    $depth       Depth of page, used for padding.
            #// @param array  $args        An array of wp_list_categories() arguments.
            #//
            css_classes = php_implode(" ", apply_filters("category_css_class", css_classes, category, depth, args))
            css_classes = " class=\"" + esc_attr(css_classes) + "\"" if css_classes else ""
            output += css_classes
            output += str(">") + str(link) + str("\n")
        elif (php_isset(lambda : args["separator"])):
            output += str(" ") + str(link) + args["separator"] + "\n"
        else:
            output += str(" ") + str(link) + str("<br />\n")
        # end if
    # end def start_el
    #// 
    #// Ends the element output, if needed.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::end_el()
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param object $page   Not used.
    #// @param int    $depth  Optional. Depth of category. Not used.
    #// @param array  $args   Optional. An array of arguments. Only uses 'list' for whether should append
    #// to output. See wp_list_categories(). Default empty array.
    #//
    def end_el(self, output=None, page=None, depth=0, args=Array()):
        
        if "list" != args["style"]:
            return
        # end if
        output += "</li>\n"
    # end def end_el
# end class Walker_Category
