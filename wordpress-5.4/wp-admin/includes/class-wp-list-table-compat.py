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
#// @since 4.7.0
#// 
#// 
#// Helper class to be used only by back compat functions
#// 
#// @since 3.1.0
#//
class _WP_List_Table_Compat(WP_List_Table):
    _screen = Array()
    _columns = Array()
    def __init__(self, screen=None, columns=Array()):
        
        if php_is_string(screen):
            screen = convert_to_screen(screen)
        # end if
        self._screen = screen
        if (not php_empty(lambda : columns)):
            self._columns = columns
            add_filter("manage_" + screen.id + "_columns", Array(self, "get_columns"), 0)
        # end if
    # end def __init__
    #// 
    #// @return array
    #//
    def get_column_info(self):
        
        columns = get_column_headers(self._screen)
        hidden = get_hidden_columns(self._screen)
        sortable = Array()
        primary = self.get_default_primary_column_name()
        return Array(columns, hidden, sortable, primary)
    # end def get_column_info
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        return self._columns
    # end def get_columns
# end class _WP_List_Table_Compat
