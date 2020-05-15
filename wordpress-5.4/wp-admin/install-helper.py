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
#// Plugins may load this file to gain access to special helper functions for
#// plugin installation. This file is not included by WordPress and it is
#// recommended, to prevent fatal errors, that this file is included using
#// require_once.
#// 
#// These functions are not optimized for speed, but they should only be used
#// once in a while, so speed shouldn't be a concern. If it is and you are
#// needing to use these functions a lot, you might experience time outs. If you
#// do, then it is advised to just write the SQL code yourself.
#// 
#// check_column( 'wp_links', 'link_description', 'mediumtext' );
#// if ( check_column( $wpdb->comments, 'comment_author', 'tinytext' ) ) {
#// echo "ok\n";
#// }
#// 
#// $error_count = 0;
#// $tablename = $wpdb->links;
#// Check the column.
#// if ( ! check_column( $wpdb->links, 'link_description', 'varchar( 255 )' ) ) {
#// $ddl = "ALTER TABLE $wpdb->links MODIFY COLUMN link_description varchar(255) NOT NULL DEFAULT '' ";
#// $q = $wpdb->query( $ddl );
#// }
#// 
#// if ( check_column( $wpdb->links, 'link_description', 'varchar( 255 )' ) ) {
#// $res .= $tablename . ' - ok <br />';
#// } else {
#// $res .= 'There was a problem with ' . $tablename . '<br />';
#// ++$error_count;
#// }
#// 
#// @package WordPress
#// @subpackage Plugin
#// 
#// Load WordPress Bootstrap
php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
if (not php_function_exists("maybe_create_table")):
    #// 
    #// Create database table, if it doesn't already exist.
    #// 
    #// @since 1.0.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $table_name Database table name.
    #// @param string $create_ddl Create database table SQL.
    #// @return bool False on error, true if already exists or success.
    #//
    def maybe_create_table(table_name=None, create_ddl=None, *args_):
        
        global wpdb
        php_check_if_defined("wpdb")
        for table in wpdb.get_col("SHOW TABLES", 0):
            if table == table_name:
                return True
            # end if
        # end for
        #// Didn't find it, so try to create it.
        wpdb.query(create_ddl)
        #// We cannot directly tell that whether this succeeded!
        for table in wpdb.get_col("SHOW TABLES", 0):
            if table == table_name:
                return True
            # end if
        # end for
        return False
    # end def maybe_create_table
# end if
if (not php_function_exists("maybe_add_column")):
    #// 
    #// Add column to database table, if column doesn't already exist in table.
    #// 
    #// @since 1.0.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $table_name Database table name
    #// @param string $column_name Table column name
    #// @param string $create_ddl SQL to add column to table.
    #// @return bool False on failure. True, if already exists or was successful.
    #//
    def maybe_add_column(table_name=None, column_name=None, create_ddl=None, *args_):
        
        global wpdb
        php_check_if_defined("wpdb")
        for column in wpdb.get_col(str("DESC ") + str(table_name), 0):
            if column == column_name:
                return True
            # end if
        # end for
        #// Didn't find it, so try to create it.
        wpdb.query(create_ddl)
        #// We cannot directly tell that whether this succeeded!
        for column in wpdb.get_col(str("DESC ") + str(table_name), 0):
            if column == column_name:
                return True
            # end if
        # end for
        return False
    # end def maybe_add_column
# end if
#// 
#// Drop column from database table, if it exists.
#// 
#// @since 1.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $table_name Table name
#// @param string $column_name Column name
#// @param string $drop_ddl SQL statement to drop column.
#// @return bool True on success or if the column doesn't exist, false on failure.
#//
def maybe_drop_column(table_name=None, column_name=None, drop_ddl=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    for column in wpdb.get_col(str("DESC ") + str(table_name), 0):
        if column == column_name:
            #// Found it, so try to drop it.
            wpdb.query(drop_ddl)
            #// We cannot directly tell that whether this succeeded!
            for column in wpdb.get_col(str("DESC ") + str(table_name), 0):
                if column == column_name:
                    return False
                # end if
            # end for
        # end if
    # end for
    #// Else didn't find it.
    return True
# end def maybe_drop_column
#// 
#// Check column matches criteria.
#// 
#// Uses the SQL DESC for retrieving the table info for the column. It will help
#// understand the parameters, if you do more research on what column information
#// is returned by the SQL statement. Pass in null to skip checking that
#// criteria.
#// 
#// Column names returned from DESC table are case sensitive and are listed:
#// Field
#// Type
#// Null
#// Key
#// Default
#// Extra
#// 
#// @since 1.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $table_name Table name
#// @param string $col_name   Column name
#// @param string $col_type   Column type
#// @param bool   $is_null    Optional. Check is null.
#// @param mixed  $key        Optional. Key info.
#// @param mixed  $default    Optional. Default value.
#// @param mixed  $extra      Optional. Extra value.
#// @return bool True, if matches. False, if not matching.
#//
def check_column(table_name=None, col_name=None, col_type=None, is_null=None, key=None, default=None, extra=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    diffs = 0
    results = wpdb.get_results(str("DESC ") + str(table_name))
    for row in results:
        if row.Field == col_name:
            #// Got our column, check the params.
            if None != col_type and row.Type != col_type:
                diffs += 1
            # end if
            if None != is_null and row.Null != is_null:
                diffs += 1
            # end if
            if None != key and row.Key != key:
                diffs += 1
            # end if
            if None != default and row.Default != default:
                diffs += 1
            # end if
            if None != extra and row.Extra != extra:
                diffs += 1
            # end if
            if diffs > 0:
                return False
            # end if
            return True
        # end if
        pass
    # end for
    return False
# end def check_column
