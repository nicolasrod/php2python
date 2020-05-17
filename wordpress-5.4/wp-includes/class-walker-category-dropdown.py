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
#// Taxonomy API: Walker_CategoryDropdown class
#// 
#// @package WordPress
#// @subpackage Template
#// @since 4.4.0
#// 
#// 
#// Core class used to create an HTML dropdown list of Categories.
#// 
#// @since 2.1.0
#// 
#// @see Walker
#//
class Walker_CategoryDropdown(Walker):
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
    #// @todo Decouple this
    #// @var array
    #// 
    #// @see Walker::$db_fields
    #//
    db_fields = Array({"parent": "parent", "id": "term_id"})
    #// 
    #// Starts the element output.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::start_el()
    #// 
    #// @param string $output   Used to append additional content (passed by reference).
    #// @param object $category Category data object.
    #// @param int    $depth    Depth of category. Used for padding.
    #// @param array  $args     Uses 'selected', 'show_count', and 'value_field' keys, if they exist.
    #// See wp_dropdown_categories().
    #// @param int    $id       Optional. ID of the current category. Default 0 (unused).
    #//
    def start_el(self, output_=None, category_=None, depth_=0, args_=None, id_=0):
        if args_ is None:
            args_ = Array()
        # end if
        
        pad_ = php_str_repeat("&nbsp;", depth_ * 3)
        #// This filter is documented in wp-includes/category-template.php
        cat_name_ = apply_filters("list_cats", category_.name, category_)
        if (php_isset(lambda : args_["value_field"])) and (php_isset(lambda : category_.args_["value_field"])):
            value_field_ = args_["value_field"]
        else:
            value_field_ = "term_id"
        # end if
        output_ += str("    <option class=\"level-") + str(depth_) + str("\" value=\"") + esc_attr(category_.value_field_) + "\""
        #// Type-juggling causes false matches, so we force everything to a string.
        if php_str(category_.value_field_) == php_str(args_["selected"]):
            output_ += " selected=\"selected\""
        # end if
        output_ += ">"
        output_ += pad_ + cat_name_
        if args_["show_count"]:
            output_ += "&nbsp;&nbsp;(" + number_format_i18n(category_.count) + ")"
        # end if
        output_ += "</option>\n"
    # end def start_el
# end class Walker_CategoryDropdown
