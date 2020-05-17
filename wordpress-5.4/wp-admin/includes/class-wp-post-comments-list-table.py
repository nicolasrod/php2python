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
#// List Table API: WP_Post_Comments_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Core class used to implement displaying post comments in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_Comments_List_Table
#//
class WP_Post_Comments_List_Table(WP_Comments_List_Table):
    #// 
    #// @return array
    #//
    def get_column_info(self):
        
        
        return Array(Array({"author": __("Author"), "comment": _x("Comment", "column name")}), Array(), Array(), "comment")
    # end def get_column_info
    #// 
    #// @return array
    #//
    def get_table_classes(self):
        
        
        classes_ = super().get_table_classes()
        classes_[-1] = "wp-list-table"
        classes_[-1] = "comments-box"
        return classes_
    # end def get_table_classes
    #// 
    #// @param bool $output_empty
    #//
    def display(self, output_empty_=None):
        if output_empty_ is None:
            output_empty_ = False
        # end if
        
        singular_ = self._args["singular"]
        wp_nonce_field("fetch-list-" + get_class(self), "_ajax_fetch_list_nonce")
        php_print("<table class=\"")
        php_print(php_implode(" ", self.get_table_classes()))
        php_print("\" style=\"display:none;\">\n    <tbody id=\"the-comment-list\"\n        ")
        if singular_:
            php_print(str(" data-wp-lists='list:") + str(singular_) + str("'"))
        # end if
        php_print("     >\n     ")
        if (not output_empty_):
            self.display_rows_or_placeholder()
        # end if
        php_print(" </tbody>\n</table>\n        ")
    # end def display
    #// 
    #// @param bool $comment_status
    #// @return int
    #//
    def get_per_page(self, comment_status_=None):
        if comment_status_ is None:
            comment_status_ = False
        # end if
        
        return 10
    # end def get_per_page
# end class WP_Post_Comments_List_Table
