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
#// Taxonomy API: Walker_Category_Checklist class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Core walker class to output an unordered list of category checkbox input elements.
#// 
#// @since 2.5.1
#// 
#// @see Walker
#// @see wp_category_checklist()
#// @see wp_terms_checklist()
#//
class Walker_Category_Checklist(Walker):
    tree_type = "category"
    db_fields = Array({"parent": "parent", "id": "term_id"})
    #// TODO: Decouple this.
    #// 
    #// Starts the list before the elements are added.
    #// 
    #// @see Walker:start_lvl()
    #// 
    #// @since 2.5.1
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Depth of category. Used for tab indentation.
    #// @param array  $args   An array of arguments. @see wp_terms_checklist()
    #//
    def start_lvl(self, output=None, depth=0, args=Array()):
        
        indent = php_str_repeat("   ", depth)
        output += str(indent) + str("<ul class='children'>\n")
    # end def start_lvl
    #// 
    #// Ends the list of after the elements are added.
    #// 
    #// @see Walker::end_lvl()
    #// 
    #// @since 2.5.1
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Depth of category. Used for tab indentation.
    #// @param array  $args   An array of arguments. @see wp_terms_checklist()
    #//
    def end_lvl(self, output=None, depth=0, args=Array()):
        
        indent = php_str_repeat("   ", depth)
        output += str(indent) + str("</ul>\n")
    # end def end_lvl
    #// 
    #// Start the element output.
    #// 
    #// @see Walker::start_el()
    #// 
    #// @since 2.5.1
    #// 
    #// @param string $output   Used to append additional content (passed by reference).
    #// @param object $category The current term object.
    #// @param int    $depth    Depth of the term in reference to parents. Default 0.
    #// @param array  $args     An array of arguments. @see wp_terms_checklist()
    #// @param int    $id       ID of the current term.
    #//
    def start_el(self, output=None, category=None, depth=0, args=Array(), id=0):
        
        if php_empty(lambda : args["taxonomy"]):
            taxonomy = "category"
        else:
            taxonomy = args["taxonomy"]
        # end if
        if "category" == taxonomy:
            name = "post_category"
        else:
            name = "tax_input[" + taxonomy + "]"
        # end if
        args["popular_cats"] = Array() if php_empty(lambda : args["popular_cats"]) else args["popular_cats"]
        class_ = " class=\"popular-category\"" if php_in_array(category.term_id, args["popular_cats"]) else ""
        args["selected_cats"] = Array() if php_empty(lambda : args["selected_cats"]) else args["selected_cats"]
        if (not php_empty(lambda : args["list_only"])):
            aria_checked = "false"
            inner_class = "category"
            if php_in_array(category.term_id, args["selected_cats"]):
                inner_class += " selected"
                aria_checked = "true"
            # end if
            output += "\n" + "<li" + class_ + ">" + "<div class=\"" + inner_class + "\" data-term-id=" + category.term_id + " tabindex=\"0\" role=\"checkbox\" aria-checked=\"" + aria_checked + "\">" + esc_html(apply_filters("the_category", category.name, "", "")) + "</div>"
        else:
            output += str("\n<li id='") + str(taxonomy) + str("-") + str(category.term_id) + str("'") + str(class_) + str(">") + "<label class=\"selectit\"><input value=\"" + category.term_id + "\" type=\"checkbox\" name=\"" + name + "[]\" id=\"in-" + taxonomy + "-" + category.term_id + "\"" + checked(php_in_array(category.term_id, args["selected_cats"]), True, False) + disabled(php_empty(lambda : args["disabled"]), False, False) + " /> " + esc_html(apply_filters("the_category", category.name, "", "")) + "</label>"
        # end if
    # end def start_el
    #// 
    #// Ends the element output, if needed.
    #// 
    #// @see Walker::end_el()
    #// 
    #// @since 2.5.1
    #// 
    #// @param string $output   Used to append additional content (passed by reference).
    #// @param object $category The current term object.
    #// @param int    $depth    Depth of the term in reference to parents. Default 0.
    #// @param array  $args     An array of arguments. @see wp_terms_checklist()
    #//
    def end_el(self, output=None, category=None, depth=0, args=Array()):
        
        output += "</li>\n"
    # end def end_el
# end class Walker_Category_Checklist
