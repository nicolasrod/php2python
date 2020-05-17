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
    def __init__(self, screen_=None, columns_=None):
        if columns_ is None:
            columns_ = Array()
        # end if
        
        if php_is_string(screen_):
            screen_ = convert_to_screen(screen_)
        # end if
        self._screen = screen_
        if (not php_empty(lambda : columns_)):
            self._columns = columns_
            add_filter("manage_" + screen_.id + "_columns", Array(self, "get_columns"), 0)
        # end if
    # end def __init__
    #// 
    #// @return array
    #//
    def get_column_info(self):
        
        
        columns_ = get_column_headers(self._screen)
        hidden_ = get_hidden_columns(self._screen)
        sortable_ = Array()
        primary_ = self.get_default_primary_column_name()
        return Array(columns_, hidden_, sortable_, primary_)
    # end def get_column_info
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        return self._columns
    # end def get_columns
# end class _WP_List_Table_Compat
