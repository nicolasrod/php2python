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
    def start_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        indent_ = php_str_repeat("  ", depth_)
        output_ += str(indent_) + str("<ul class='children'>\n")
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
    def end_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        indent_ = php_str_repeat("  ", depth_)
        output_ += str(indent_) + str("</ul>\n")
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
    def start_el(self, output_=None, category_=None, depth_=0, args_=None, id_=0):
        if args_ is None:
            args_ = Array()
        # end if
        
        if php_empty(lambda : args_["taxonomy"]):
            taxonomy_ = "category"
        else:
            taxonomy_ = args_["taxonomy"]
        # end if
        if "category" == taxonomy_:
            name_ = "post_category"
        else:
            name_ = "tax_input[" + taxonomy_ + "]"
        # end if
        args_["popular_cats"] = Array() if php_empty(lambda : args_["popular_cats"]) else args_["popular_cats"]
        class_ = " class=\"popular-category\"" if php_in_array(category_.term_id, args_["popular_cats"]) else ""
        args_["selected_cats"] = Array() if php_empty(lambda : args_["selected_cats"]) else args_["selected_cats"]
        if (not php_empty(lambda : args_["list_only"])):
            aria_checked_ = "false"
            inner_class_ = "category"
            if php_in_array(category_.term_id, args_["selected_cats"]):
                inner_class_ += " selected"
                aria_checked_ = "true"
            # end if
            output_ += "\n" + "<li" + class_ + ">" + "<div class=\"" + inner_class_ + "\" data-term-id=" + category_.term_id + " tabindex=\"0\" role=\"checkbox\" aria-checked=\"" + aria_checked_ + "\">" + esc_html(apply_filters("the_category", category_.name, "", "")) + "</div>"
        else:
            output_ += str("\n<li id='") + str(taxonomy_) + str("-") + str(category_.term_id) + str("'") + str(class_) + str(">") + "<label class=\"selectit\"><input value=\"" + category_.term_id + "\" type=\"checkbox\" name=\"" + name_ + "[]\" id=\"in-" + taxonomy_ + "-" + category_.term_id + "\"" + checked(php_in_array(category_.term_id, args_["selected_cats"]), True, False) + disabled(php_empty(lambda : args_["disabled"]), False, False) + " /> " + esc_html(apply_filters("the_category", category_.name, "", "")) + "</label>"
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
    def end_el(self, output_=None, category_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        output_ += "</li>\n"
    # end def end_el
# end class Walker_Category_Checklist
