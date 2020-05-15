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
#// Helper functions for displaying a list of items in an ajaxified HTML table.
#// 
#// @package WordPress
#// @subpackage List_Table
#// @since 3.1.0
#// 
#// 
#// Fetches an instance of a WP_List_Table class.
#// 
#// @access private
#// @since 3.1.0
#// 
#// @global string $hook_suffix
#// 
#// @param string $class The type of the list table, which is the class name.
#// @param array  $args  Optional. Arguments to pass to the class. Accepts 'screen'.
#// @return WP_List_Table|bool List table object on success, false if the class does not exist.
#//
def _get_list_table(class_=None, args=Array(), *args_):
    
    core_classes = Array({"WP_Posts_List_Table": "posts", "WP_Media_List_Table": "media", "WP_Terms_List_Table": "terms", "WP_Users_List_Table": "users", "WP_Comments_List_Table": "comments", "WP_Post_Comments_List_Table": Array("comments", "post-comments"), "WP_Links_List_Table": "links", "WP_Plugin_Install_List_Table": "plugin-install", "WP_Themes_List_Table": "themes", "WP_Theme_Install_List_Table": Array("themes", "theme-install"), "WP_Plugins_List_Table": "plugins", "WP_MS_Sites_List_Table": "ms-sites", "WP_MS_Users_List_Table": "ms-users", "WP_MS_Themes_List_Table": "ms-themes", "WP_Privacy_Data_Export_Requests_List_Table": "privacy-data-export-requests", "WP_Privacy_Data_Removal_Requests_List_Table": "privacy-data-removal-requests"})
    if (php_isset(lambda : core_classes[class_])):
        for required in core_classes[class_]:
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-" + required + "-list-table.php", once=True)
        # end for
        if (php_isset(lambda : args["screen"])):
            args["screen"] = convert_to_screen(args["screen"])
        elif (php_isset(lambda : PHP_GLOBALS["hook_suffix"])):
            args["screen"] = get_current_screen()
        else:
            args["screen"] = None
        # end if
        return php_new_class(class_, lambda : {**locals(), **globals()}[class_](args))
    # end if
    return False
# end def _get_list_table
#// 
#// Register column headers for a particular screen.
#// 
#// @see get_column_headers(), print_column_headers(), get_hidden_columns()
#// 
#// @since 2.7.0
#// 
#// @param string  $screen   The handle for the screen to add help to. This is usually the hook name returned by the
#// add_*_page() functions.
#// @param string[] $columns An array of columns with column IDs as the keys and translated column names as the values.
#//
def register_column_headers(screen=None, columns=None, *args_):
    
    php_new_class("_WP_List_Table_Compat", lambda : _WP_List_Table_Compat(screen, columns))
# end def register_column_headers
#// 
#// Prints column headers for a particular screen.
#// 
#// @since 2.7.0
#// 
#// @param string|WP_Screen $screen  The screen hook name or screen object.
#// @param bool             $with_id Whether to set the id attribute or not.
#//
def print_column_headers(screen=None, with_id=True, *args_):
    
    wp_list_table = php_new_class("_WP_List_Table_Compat", lambda : _WP_List_Table_Compat(screen))
    wp_list_table.print_column_headers(with_id)
# end def print_column_headers
