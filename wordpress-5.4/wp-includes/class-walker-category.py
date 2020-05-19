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
    #// 
    #// What the class handles.
    #// 
    #// @since 2.1.0
    #// @var string
    #// 
    #// @see Walker::$tree_type
    #//
    tree_type = "category"
    #// 
    #// Database fields to use.
    #// 
    #// @since 2.1.0
    #// @var array
    #// 
    #// @see Walker::$db_fields
    #// @todo Decouple this
    #//
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
    def start_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if "list" != args_["style"]:
            return
        # end if
        indent_ = php_str_repeat("  ", depth_)
        output_ += str(indent_) + str("<ul class='children'>\n")
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
    def end_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if "list" != args_["style"]:
            return
        # end if
        indent_ = php_str_repeat("  ", depth_)
        output_ += str(indent_) + str("</ul>\n")
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
    def start_el(self, output_=None, category_=None, depth_=0, args_=None, id_=0):
        if args_ is None:
            args_ = Array()
        # end if
        
        #// This filter is documented in wp-includes/category-template.php
        cat_name_ = apply_filters("list_cats", esc_attr(category_.name), category_)
        #// Don't generate an element if the category name is empty.
        if "" == cat_name_:
            return
        # end if
        atts_ = Array()
        atts_["href"] = get_term_link(category_)
        if args_["use_desc_for_title"] and (not php_empty(lambda : category_.description)):
            #// 
            #// Filters the category description for display.
            #// 
            #// @since 1.2.0
            #// 
            #// @param string $description Category description.
            #// @param object $category    Category object.
            #//
            atts_["title"] = strip_tags(apply_filters("category_description", category_.description, category_))
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
        atts_ = apply_filters("category_list_link_attributes", atts_, category_, depth_, args_, id_)
        attributes_ = ""
        for attr_,value_ in atts_.items():
            if php_is_scalar(value_) and "" != value_ and False != value_:
                value_ = esc_url(value_) if "href" == attr_ else esc_attr(value_)
                attributes_ += " " + attr_ + "=\"" + value_ + "\""
            # end if
        # end for
        link_ = php_sprintf("<a%s>%s</a>", attributes_, cat_name_)
        if (not php_empty(lambda : args_["feed_image"])) or (not php_empty(lambda : args_["feed"])):
            link_ += " "
            if php_empty(lambda : args_["feed_image"]):
                link_ += "("
            # end if
            link_ += "<a href=\"" + esc_url(get_term_feed_link(category_.term_id, category_.taxonomy, args_["feed_type"])) + "\""
            if php_empty(lambda : args_["feed"]):
                #// translators: %s: Category name.
                alt_ = " alt=\"" + php_sprintf(__("Feed for all posts filed under %s"), cat_name_) + "\""
            else:
                alt_ = " alt=\"" + args_["feed"] + "\""
                name_ = args_["feed"]
                link_ += "" if php_empty(lambda : args_["title"]) else args_["title"]
            # end if
            link_ += ">"
            if php_empty(lambda : args_["feed_image"]):
                link_ += name_
            else:
                link_ += "<img src='" + esc_url(args_["feed_image"]) + str("'") + str(alt_) + " />"
            # end if
            link_ += "</a>"
            if php_empty(lambda : args_["feed_image"]):
                link_ += ")"
            # end if
        # end if
        if (not php_empty(lambda : args_["show_count"])):
            link_ += " (" + number_format_i18n(category_.count) + ")"
        # end if
        if "list" == args_["style"]:
            output_ += "    <li"
            css_classes_ = Array("cat-item", "cat-item-" + category_.term_id)
            if (not php_empty(lambda : args_["current_category"])):
                #// 'current_category' can be an array, so we use `get_terms()`.
                _current_terms_ = get_terms(Array({"taxonomy": category_.taxonomy, "include": args_["current_category"], "hide_empty": False}))
                for _current_term_ in _current_terms_:
                    if category_.term_id == _current_term_.term_id:
                        css_classes_[-1] = "current-cat"
                        link_ = php_str_replace("<a", "<a aria-current=\"page\"", link_)
                    elif category_.term_id == _current_term_.parent:
                        css_classes_[-1] = "current-cat-parent"
                    # end if
                    while True:
                        
                        if not (_current_term_.parent):
                            break
                        # end if
                        if category_.term_id == _current_term_.parent:
                            css_classes_[-1] = "current-cat-ancestor"
                            break
                        # end if
                        _current_term_ = get_term(_current_term_.parent, category_.taxonomy)
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
            css_classes_ = php_implode(" ", apply_filters("category_css_class", css_classes_, category_, depth_, args_))
            css_classes_ = " class=\"" + esc_attr(css_classes_) + "\"" if css_classes_ else ""
            output_ += css_classes_
            output_ += str(">") + str(link_) + str("\n")
        elif (php_isset(lambda : args_["separator"])):
            output_ += str("    ") + str(link_) + args_["separator"] + "\n"
        else:
            output_ += str("    ") + str(link_) + str("<br />\n")
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
    def end_el(self, output_=None, page_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if "list" != args_["style"]:
            return
        # end if
        output_ += "</li>\n"
    # end def end_el
# end class Walker_Category
