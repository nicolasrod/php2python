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
    tree_type = "category"
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
    def start_el(self, output=None, category=None, depth=0, args=Array(), id=0):
        
        pad = php_str_repeat("&nbsp;", depth * 3)
        #// This filter is documented in wp-includes/category-template.php
        cat_name = apply_filters("list_cats", category.name, category)
        if (php_isset(lambda : args["value_field"])) and (php_isset(lambda : category.args["value_field"])):
            value_field = args["value_field"]
        else:
            value_field = "term_id"
        # end if
        output += str(" <option class=\"level-") + str(depth) + str("\" value=\"") + esc_attr(category.value_field) + "\""
        #// Type-juggling causes false matches, so we force everything to a string.
        if php_str(category.value_field) == php_str(args["selected"]):
            output += " selected=\"selected\""
        # end if
        output += ">"
        output += pad + cat_name
        if args["show_count"]:
            output += "&nbsp;&nbsp;(" + number_format_i18n(category.count) + ")"
        # end if
        output += "</option>\n"
    # end def start_el
# end class Walker_CategoryDropdown
