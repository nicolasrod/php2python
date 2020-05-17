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
    def maybe_create_table(table_name_=None, create_ddl_=None, *_args_):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        for table_ in wpdb_.get_col("SHOW TABLES", 0):
            if table_ == table_name_:
                return True
            # end if
        # end for
        #// Didn't find it, so try to create it.
        wpdb_.query(create_ddl_)
        #// We cannot directly tell that whether this succeeded!
        for table_ in wpdb_.get_col("SHOW TABLES", 0):
            if table_ == table_name_:
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
    def maybe_add_column(table_name_=None, column_name_=None, create_ddl_=None, *_args_):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        for column_ in wpdb_.get_col(str("DESC ") + str(table_name_), 0):
            if column_ == column_name_:
                return True
            # end if
        # end for
        #// Didn't find it, so try to create it.
        wpdb_.query(create_ddl_)
        #// We cannot directly tell that whether this succeeded!
        for column_ in wpdb_.get_col(str("DESC ") + str(table_name_), 0):
            if column_ == column_name_:
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
def maybe_drop_column(table_name_=None, column_name_=None, drop_ddl_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    for column_ in wpdb_.get_col(str("DESC ") + str(table_name_), 0):
        if column_ == column_name_:
            #// Found it, so try to drop it.
            wpdb_.query(drop_ddl_)
            #// We cannot directly tell that whether this succeeded!
            for column_ in wpdb_.get_col(str("DESC ") + str(table_name_), 0):
                if column_ == column_name_:
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
def check_column(table_name_=None, col_name_=None, col_type_=None, is_null_=None, key_=None, default_=None, extra_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    diffs_ = 0
    results_ = wpdb_.get_results(str("DESC ") + str(table_name_))
    for row_ in results_:
        if row_.Field == col_name_:
            #// Got our column, check the params.
            if None != col_type_ and row_.Type != col_type_:
                diffs_ += 1
            # end if
            if None != is_null_ and row_.Null != is_null_:
                diffs_ += 1
            # end if
            if None != key_ and row_.Key != key_:
                diffs_ += 1
            # end if
            if None != default_ and row_.Default != default_:
                diffs_ += 1
            # end if
            if None != extra_ and row_.Extra != extra_:
                diffs_ += 1
            # end if
            if diffs_ > 0:
                return False
            # end if
            return True
        # end if
        pass
    # end for
    return False
# end def check_column
