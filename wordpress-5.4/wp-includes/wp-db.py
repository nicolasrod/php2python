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
#// WordPress DB Class
#// 
#// Original code from {@link http://php.justinvincent.com Justin Vincent (justin@visunet.ie)}
#// 
#// @package WordPress
#// @subpackage Database
#// @since 0.71
#// 
#// 
#// @since 0.71
#//
php_define("EZSQL_VERSION", "WP1.25")
#// 
#// @since 0.71
#//
php_define("OBJECT", "OBJECT")
#// phpcs:ignore Generic.NamingConventions.UpperCaseConstantName.ConstantNotUpperCase
php_define("object", "OBJECT")
#// Back compat.
#// 
#// @since 2.5.0
#//
php_define("OBJECT_K", "OBJECT_K")
#// 
#// @since 0.71
#//
php_define("ARRAY_A", "ARRAY_A")
#// 
#// @since 0.71
#//
php_define("ARRAY_N", "ARRAY_N")
#// 
#// WordPress Database Access Abstraction Object
#// 
#// It is possible to replace this class with your own
#// by setting the $wpdb global variable in wp-content/db.php
#// file to your class. The wpdb class will still be included,
#// so you can extend it or simply use your own.
#// 
#// @link https://codex.wordpress.org/Function_Reference/wpdb_Class
#// 
#// @since 0.71
#//
class wpdb():
    show_errors = False
    suppress_errors = False
    last_error = ""
    num_queries = 0
    num_rows = 0
    rows_affected = 0
    insert_id = 0
    last_query = Array()
    last_result = Array()
    result = Array()
    col_meta = Array()
    table_charset = Array()
    check_current_query = True
    checking_collation = False
    col_info = Array()
    queries = Array()
    reconnect_retries = 5
    prefix = ""
    base_prefix = Array()
    ready = False
    blogid = 0
    siteid = 0
    tables = Array("posts", "comments", "links", "options", "postmeta", "terms", "term_taxonomy", "term_relationships", "termmeta", "commentmeta")
    old_tables = Array("categories", "post2cat", "link2cat")
    global_tables = Array("users", "usermeta")
    ms_global_tables = Array("blogs", "blogmeta", "signups", "site", "sitemeta", "sitecategories", "registration_log")
    comments = Array()
    commentmeta = Array()
    links = Array()
    options = Array()
    postmeta = Array()
    posts = Array()
    terms = Array()
    term_relationships = Array()
    term_taxonomy = Array()
    termmeta = Array()
    usermeta = Array()
    users = Array()
    blogs = Array()
    blogmeta = Array()
    registration_log = Array()
    signups = Array()
    site = Array()
    sitecategories = Array()
    sitemeta = Array()
    field_types = Array()
    charset = Array()
    collate = Array()
    dbuser = Array()
    dbpassword = Array()
    dbname = Array()
    dbhost = Array()
    dbh = Array()
    func_call = Array()
    is_mysql = None
    incompatible_modes = Array("NO_ZERO_DATE", "ONLY_FULL_GROUP_BY", "STRICT_TRANS_TABLES", "STRICT_ALL_TABLES", "TRADITIONAL", "ANSI")
    use_mysqli = False
    has_connected = False
    #// 
    #// Connects to the database server and selects a database
    #// 
    #// PHP5 style constructor for compatibility with PHP5. Does
    #// the actual setting up of the class properties and connection
    #// to the database.
    #// 
    #// @link https://core.trac.wordpress.org/ticket/3354
    #// @since 2.0.8
    #// 
    #// @global string $wp_version The WordPress version string.
    #// 
    #// @param string $dbuser     MySQL database user
    #// @param string $dbpassword MySQL database password
    #// @param string $dbname     MySQL database name
    #// @param string $dbhost     MySQL database host
    #//
    def __init__(self, dbuser=None, dbpassword=None, dbname=None, dbhost=None):
        
        if WP_DEBUG and WP_DEBUG_DISPLAY:
            self.show_errors()
        # end if
        #// Use ext/mysqli if it exists unless WP_USE_EXT_MYSQL is defined as true.
        if php_function_exists("mysqli_connect"):
            self.use_mysqli = True
            if php_defined("WP_USE_EXT_MYSQL"):
                self.use_mysqli = (not WP_USE_EXT_MYSQL)
            # end if
        # end if
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbname = dbname
        self.dbhost = dbhost
        #// wp-config.php creation will manually connect when ready.
        if php_defined("WP_SETUP_CONFIG"):
            return
        # end if
        self.db_connect()
    # end def __init__
    #// 
    #// Makes private properties readable for backward compatibility.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $name The private member to get, and optionally process
    #// @return mixed The private member
    #//
    def __get(self, name=None):
        
        if "col_info" == name:
            self.load_col_info()
        # end if
        return self.name
    # end def __get
    #// 
    #// Makes private properties settable for backward compatibility.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $name  The private member to set
    #// @param mixed  $value The value to set
    #//
    def __set(self, name=None, value=None):
        
        protected_members = Array("col_meta", "table_charset", "check_current_query")
        if php_in_array(name, protected_members, True):
            return
        # end if
        self.name = value
    # end def __set
    #// 
    #// Makes private properties check-able for backward compatibility.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $name  The private member to check
    #// 
    #// @return bool If the member is set or not
    #//
    def __isset(self, name=None):
        
        return (php_isset(lambda : self.name))
    # end def __isset
    #// 
    #// Makes private properties un-settable for backward compatibility.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $name  The private member to unset
    #//
    def __unset(self, name=None):
        
        self.name = None
    # end def __unset
    #// 
    #// Set $this->charset and $this->collate
    #// 
    #// @since 3.1.0
    #//
    def init_charset(self):
        
        charset = ""
        collate = ""
        if php_function_exists("is_multisite") and is_multisite():
            charset = "utf8"
            if php_defined("DB_COLLATE") and DB_COLLATE:
                collate = DB_COLLATE
            else:
                collate = "utf8_general_ci"
            # end if
        elif php_defined("DB_COLLATE"):
            collate = DB_COLLATE
        # end if
        if php_defined("DB_CHARSET"):
            charset = DB_CHARSET
        # end if
        charset_collate = self.determine_charset(charset, collate)
        self.charset = charset_collate["charset"]
        self.collate = charset_collate["collate"]
    # end def init_charset
    #// 
    #// Determines the best charset and collation to use given a charset and collation.
    #// 
    #// For example, when able, utf8mb4 should be used instead of utf8.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $charset The character set to check.
    #// @param string $collate The collation to check.
    #// @return array {
    #// The most appropriate character set and collation to use.
    #// 
    #// @type string $charset Character set.
    #// @type string $collate Collation.
    #// }
    #//
    def determine_charset(self, charset=None, collate=None):
        
        if self.use_mysqli and (not type(self.dbh).__name__ == "mysqli") or php_empty(lambda : self.dbh):
            return compact("charset", "collate")
        # end if
        if "utf8" == charset and self.has_cap("utf8mb4"):
            charset = "utf8mb4"
        # end if
        if "utf8mb4" == charset and (not self.has_cap("utf8mb4")):
            charset = "utf8"
            collate = php_str_replace("utf8mb4_", "utf8_", collate)
        # end if
        if "utf8mb4" == charset:
            #// _general_ is outdated, so we can upgrade it to _unicode_, instead.
            if (not collate) or "utf8_general_ci" == collate:
                collate = "utf8mb4_unicode_ci"
            else:
                collate = php_str_replace("utf8_", "utf8mb4_", collate)
            # end if
        # end if
        #// _unicode_520_ is a better collation, we should use that when it's available.
        if self.has_cap("utf8mb4_520") and "utf8mb4_unicode_ci" == collate:
            collate = "utf8mb4_unicode_520_ci"
        # end if
        return compact("charset", "collate")
    # end def determine_charset
    #// 
    #// Sets the connection's character set.
    #// 
    #// @since 3.1.0
    #// 
    #// @param resource $dbh     The resource given by mysql_connect
    #// @param string   $charset Optional. The character set. Default null.
    #// @param string   $collate Optional. The collation. Default null.
    #//
    def set_charset(self, dbh=None, charset=None, collate=None):
        
        if (not (php_isset(lambda : charset))):
            charset = self.charset
        # end if
        if (not (php_isset(lambda : collate))):
            collate = self.collate
        # end if
        if self.has_cap("collation") and (not php_empty(lambda : charset)):
            set_charset_succeeded = True
            if self.use_mysqli:
                if php_function_exists("mysqli_set_charset") and self.has_cap("set_charset"):
                    set_charset_succeeded = mysqli_set_charset(dbh, charset)
                # end if
                if set_charset_succeeded:
                    query = self.prepare("SET NAMES %s", charset)
                    if (not php_empty(lambda : collate)):
                        query += self.prepare(" COLLATE %s", collate)
                    # end if
                    mysqli_query(dbh, query)
                # end if
            else:
                if php_function_exists("mysql_set_charset") and self.has_cap("set_charset"):
                    set_charset_succeeded = mysql_set_charset(charset, dbh)
                # end if
                if set_charset_succeeded:
                    query = self.prepare("SET NAMES %s", charset)
                    if (not php_empty(lambda : collate)):
                        query += self.prepare(" COLLATE %s", collate)
                    # end if
                    mysql_query(query, dbh)
                # end if
            # end if
        # end if
    # end def set_charset
    #// 
    #// Change the current SQL mode, and ensure its WordPress compatibility.
    #// 
    #// If no modes are passed, it will ensure the current MySQL server
    #// modes are compatible.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $modes Optional. A list of SQL modes to set.
    #//
    def set_sql_mode(self, modes=Array()):
        
        if php_empty(lambda : modes):
            if self.use_mysqli:
                res = mysqli_query(self.dbh, "SELECT @@SESSION.sql_mode")
            else:
                res = mysql_query("SELECT @@SESSION.sql_mode", self.dbh)
            # end if
            if php_empty(lambda : res):
                return
            # end if
            if self.use_mysqli:
                modes_array = mysqli_fetch_array(res)
                if php_empty(lambda : modes_array[0]):
                    return
                # end if
                modes_str = modes_array[0]
            else:
                modes_str = mysql_result(res, 0)
            # end if
            if php_empty(lambda : modes_str):
                return
            # end if
            modes = php_explode(",", modes_str)
        # end if
        modes = php_array_change_key_case(modes, CASE_UPPER)
        #// 
        #// Filters the list of incompatible SQL modes to exclude.
        #// 
        #// @since 3.9.0
        #// 
        #// @param array $incompatible_modes An array of incompatible modes.
        #//
        incompatible_modes = apply_filters("incompatible_sql_modes", self.incompatible_modes)
        for i,mode in modes:
            if php_in_array(mode, incompatible_modes):
                modes[i] = None
            # end if
        # end for
        modes_str = php_implode(",", modes)
        if self.use_mysqli:
            mysqli_query(self.dbh, str("SET SESSION sql_mode='") + str(modes_str) + str("'"))
        else:
            mysql_query(str("SET SESSION sql_mode='") + str(modes_str) + str("'"), self.dbh)
        # end if
    # end def set_sql_mode
    #// 
    #// Sets the table prefix for the WordPress tables.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $prefix          Alphanumeric name for the new prefix.
    #// @param bool   $set_table_names Optional. Whether the table names, e.g. wpdb::$posts, should be updated or not.
    #// @return string|WP_Error Old prefix or WP_Error on error
    #//
    def set_prefix(self, prefix=None, set_table_names=True):
        
        if php_preg_match("|[^a-z0-9_]|i", prefix):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_db_prefix", "Invalid database prefix"))
        # end if
        old_prefix = "" if is_multisite() else prefix
        if (php_isset(lambda : self.base_prefix)):
            old_prefix = self.base_prefix
        # end if
        self.base_prefix = prefix
        if set_table_names:
            for table,prefixed_table in self.tables("global"):
                self.table = prefixed_table
            # end for
            if is_multisite() and php_empty(lambda : self.blogid):
                return old_prefix
            # end if
            self.prefix = self.get_blog_prefix()
            for table,prefixed_table in self.tables("blog"):
                self.table = prefixed_table
            # end for
            for table,prefixed_table in self.tables("old"):
                self.table = prefixed_table
            # end for
        # end if
        return old_prefix
    # end def set_prefix
    #// 
    #// Sets blog id.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int $blog_id
    #// @param int $network_id Optional.
    #// @return int previous blog id
    #//
    def set_blog_id(self, blog_id=None, network_id=0):
        
        if (not php_empty(lambda : network_id)):
            self.siteid = network_id
        # end if
        old_blog_id = self.blogid
        self.blogid = blog_id
        self.prefix = self.get_blog_prefix()
        for table,prefixed_table in self.tables("blog"):
            self.table = prefixed_table
        # end for
        for table,prefixed_table in self.tables("old"):
            self.table = prefixed_table
        # end for
        return old_blog_id
    # end def set_blog_id
    #// 
    #// Gets blog prefix.
    #// 
    #// @since 3.0.0
    #// @param int $blog_id Optional.
    #// @return string Blog prefix.
    #//
    def get_blog_prefix(self, blog_id=None):
        
        if is_multisite():
            if None == blog_id:
                blog_id = self.blogid
            # end if
            blog_id = php_int(blog_id)
            if php_defined("MULTISITE") and 0 == blog_id or 1 == blog_id:
                return self.base_prefix
            else:
                return self.base_prefix + blog_id + "_"
            # end if
        else:
            return self.base_prefix
        # end if
    # end def get_blog_prefix
    #// 
    #// Returns an array of WordPress tables.
    #// 
    #// Also allows for the CUSTOM_USER_TABLE and CUSTOM_USER_META_TABLE to
    #// override the WordPress users and usermeta tables that would otherwise
    #// be determined by the prefix.
    #// 
    #// The scope argument can take one of the following:
    #// 
    #// 'all' - returns 'all' and 'global' tables. No old tables are returned.
    #// 'blog' - returns the blog-level tables for the queried blog.
    #// 'global' - returns the global tables for the installation, returning multisite tables only if running multisite.
    #// 'ms_global' - returns the multisite global tables, regardless if current installation is multisite.
    #// 'old' - returns tables which are deprecated.
    #// 
    #// @since 3.0.0
    #// @uses wpdb::$tables
    #// @uses wpdb::$old_tables
    #// @uses wpdb::$global_tables
    #// @uses wpdb::$ms_global_tables
    #// 
    #// @param string $scope   Optional. Can be all, global, ms_global, blog, or old tables. Defaults to all.
    #// @param bool   $prefix  Optional. Whether to include table prefixes. Default true. If blog
    #// prefix is requested, then the custom users and usermeta tables will be mapped.
    #// @param int    $blog_id Optional. The blog_id to prefix. Defaults to wpdb::$blogid. Used only when prefix is requested.
    #// @return array Table names. When a prefix is requested, the key is the unprefixed table name.
    #//
    def tables(self, scope="all", prefix=True, blog_id=0):
        
        for case in Switch(scope):
            if case("all"):
                tables = php_array_merge(self.global_tables, self.tables)
                if is_multisite():
                    tables = php_array_merge(tables, self.ms_global_tables)
                # end if
                break
            # end if
            if case("blog"):
                tables = self.tables
                break
            # end if
            if case("global"):
                tables = self.global_tables
                if is_multisite():
                    tables = php_array_merge(tables, self.ms_global_tables)
                # end if
                break
            # end if
            if case("ms_global"):
                tables = self.ms_global_tables
                break
            # end if
            if case("old"):
                tables = self.old_tables
                break
            # end if
            if case():
                return Array()
            # end if
        # end for
        if prefix:
            if (not blog_id):
                blog_id = self.blogid
            # end if
            blog_prefix = self.get_blog_prefix(blog_id)
            base_prefix = self.base_prefix
            global_tables = php_array_merge(self.global_tables, self.ms_global_tables)
            for k,table in tables:
                if php_in_array(table, global_tables):
                    tables[table] = base_prefix + table
                else:
                    tables[table] = blog_prefix + table
                # end if
                tables[k] = None
            # end for
            if (php_isset(lambda : tables["users"])) and php_defined("CUSTOM_USER_TABLE"):
                tables["users"] = CUSTOM_USER_TABLE
            # end if
            if (php_isset(lambda : tables["usermeta"])) and php_defined("CUSTOM_USER_META_TABLE"):
                tables["usermeta"] = CUSTOM_USER_META_TABLE
            # end if
        # end if
        return tables
    # end def tables
    #// 
    #// Selects a database using the current database connection.
    #// 
    #// The database name will be changed based on the current database
    #// connection. On failure, the execution will bail and display an DB error.
    #// 
    #// @since 0.71
    #// 
    #// @param string        $db  MySQL database name
    #// @param resource|null $dbh Optional link identifier.
    #//
    def select(self, db=None, dbh=None):
        
        if is_null(dbh):
            dbh = self.dbh
        # end if
        if self.use_mysqli:
            success = mysqli_select_db(dbh, db)
        else:
            success = mysql_select_db(db, dbh)
        # end if
        if (not success):
            self.ready = False
            if (not did_action("template_redirect")):
                wp_load_translations_early()
                message = "<h1>" + __("Can&#8217;t select database") + "</h1>\n"
                message += "<p>" + php_sprintf(__("We were able to connect to the database server (which means your username and password is okay) but not able to select the %s database."), "<code>" + htmlspecialchars(db, ENT_QUOTES) + "</code>") + "</p>\n"
                message += "<ul>\n"
                message += "<li>" + __("Are you sure it exists?") + "</li>\n"
                message += "<li>" + php_sprintf(__("Does the user %1$s have permission to use the %2$s database?"), "<code>" + htmlspecialchars(self.dbuser, ENT_QUOTES) + "</code>", "<code>" + htmlspecialchars(db, ENT_QUOTES) + "</code>") + "</li>\n"
                message += "<li>" + php_sprintf(__("On some systems the name of your database is prefixed with your username, so it would be like <code>username_%1$s</code>. Could that be the problem?"), htmlspecialchars(db, ENT_QUOTES)) + "</li>\n"
                message += "</ul>\n"
                message += "<p>" + php_sprintf(__("If you don&#8217;t know how to set up a database you should <strong>contact your host</strong>. If all else fails you may find help at the <a href=\"%s\">WordPress Support Forums</a>."), __("https://wordpress.org/support/forums/")) + "</p>\n"
                self.bail(message, "db_select_fail")
            # end if
        # end if
    # end def select
    #// 
    #// Do not use, deprecated.
    #// 
    #// Use esc_sql() or wpdb::prepare() instead.
    #// 
    #// @since 2.8.0
    #// @deprecated 3.6.0 Use wpdb::prepare()
    #// @see wpdb::prepare
    #// @see esc_sql()
    #// 
    #// @param string $string
    #// @return string
    #//
    def _weak_escape(self, string=None):
        
        if php_func_num_args() == 1 and php_function_exists("_deprecated_function"):
            _deprecated_function(__METHOD__, "3.6.0", "wpdb::prepare() or esc_sql()")
        # end if
        return addslashes(string)
    # end def _weak_escape
    #// 
    #// Real escape, using mysqli_real_escape_string() or mysql_real_escape_string()
    #// 
    #// @see mysqli_real_escape_string()
    #// @see mysql_real_escape_string()
    #// @since 2.8.0
    #// 
    #// @param  string $string to escape
    #// @return string escaped
    #//
    def _real_escape(self, string=None):
        
        if self.dbh:
            if self.use_mysqli:
                escaped = mysqli_real_escape_string(self.dbh, string)
            else:
                escaped = mysql_real_escape_string(string, self.dbh)
            # end if
        else:
            class_ = get_class(self)
            if php_function_exists("__"):
                #// translators: %s: Database access abstraction class, usually wpdb or a class extending wpdb.
                _doing_it_wrong(class_, php_sprintf(__("%s must set a database connection for use with escaping."), class_), "3.6.0")
            else:
                _doing_it_wrong(class_, php_sprintf("%s must set a database connection for use with escaping.", class_), "3.6.0")
            # end if
            escaped = addslashes(string)
        # end if
        return self.add_placeholder_escape(escaped)
    # end def _real_escape
    #// 
    #// Escape data. Works on arrays.
    #// 
    #// @uses wpdb::_real_escape()
    #// @since 2.8.0
    #// 
    #// @param  string|array $data
    #// @return string|array escaped
    #//
    def _escape(self, data=None):
        
        if php_is_array(data):
            for k,v in data:
                if php_is_array(v):
                    data[k] = self._escape(v)
                else:
                    data[k] = self._real_escape(v)
                # end if
            # end for
        else:
            data = self._real_escape(data)
        # end if
        return data
    # end def _escape
    #// 
    #// Do not use, deprecated.
    #// 
    #// Use esc_sql() or wpdb::prepare() instead.
    #// 
    #// @since 0.71
    #// @deprecated 3.6.0 Use wpdb::prepare()
    #// @see wpdb::prepare()
    #// @see esc_sql()
    #// 
    #// @param mixed $data
    #// @return mixed
    #//
    def escape(self, data=None):
        
        if php_func_num_args() == 1 and php_function_exists("_deprecated_function"):
            _deprecated_function(__METHOD__, "3.6.0", "wpdb::prepare() or esc_sql()")
        # end if
        if php_is_array(data):
            for k,v in data:
                if php_is_array(v):
                    data[k] = self.escape(v, "recursive")
                else:
                    data[k] = self._weak_escape(v, "internal")
                # end if
            # end for
        else:
            data = self._weak_escape(data, "internal")
        # end if
        return data
    # end def escape
    #// 
    #// Escapes content by reference for insertion into the database, for security
    #// 
    #// @uses wpdb::_real_escape()
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $string to escape
    #//
    def escape_by_ref(self, string=None):
        
        if (not php_is_float(string)):
            string = self._real_escape(string)
        # end if
    # end def escape_by_ref
    #// 
    #// Prepares a SQL query for safe execution. Uses sprintf()-like syntax.
    #// 
    #// The following placeholders can be used in the query string:
    #// %d (integer)
    #// %f (float)
    #// %s (string)
    #// 
    #// All placeholders MUST be left unquoted in the query string. A corresponding argument
    #// MUST be passed for each placeholder.
    #// 
    #// For compatibility with old behavior, numbered or formatted string placeholders (eg, %1$s, %5s)
    #// will not have quotes added by this function, so should be passed with appropriate quotes around
    #// them for your usage.
    #// 
    #// Literal percentage signs (%) in the query string must be written as %%. Percentage wildcards (for example,
    #// to use in LIKE syntax) must be passed via a substitution argument containing the complete LIKE string, these
    #// cannot be inserted directly in the query string. Also see wpdb::esc_like().
    #// 
    #// Arguments may be passed as individual arguments to the method, or as a single array containing
    #// all arguments. A combination of the two is not supported.
    #// 
    #// Examples:
    #// $wpdb->prepare( "SELECT * FROM `table` WHERE `column` = %s AND `field` = %d OR `other_field` LIKE %s", array( 'foo', 1337, '%bar' ) );
    #// $wpdb->prepare( "SELECT DATE_FORMAT(`field`, '%%c') FROM `table` WHERE `column` = %s", 'foo' );
    #// 
    #// @link https://www.php.net/sprintf Description of syntax.
    #// @since 2.3.0
    #// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
    #// by updating the function signature. The second parameter was changed
    #// from `$args` to `...$args`.
    #// 
    #// @param string      $query   Query statement with sprintf()-like placeholders
    #// @param array|mixed $args    The array of variables to substitute into the query's placeholders
    #// if being called with an array of arguments, or the first variable
    #// to substitute into the query's placeholders if being called with
    #// individual arguments.
    #// @param mixed       ...$args Further variables to substitute into the query's placeholders
    #// if being called with individual arguments.
    #// @return string|void Sanitized query string, if there is a query to prepare.
    #//
    def prepare(self, query=None, *args):
        
        if is_null(query):
            return
        # end if
        #// This is not meant to be foolproof -- but it will catch obviously incorrect usage.
        if php_strpos(query, "%") == False:
            wp_load_translations_early()
            _doing_it_wrong("wpdb::prepare", php_sprintf(__("The query argument of %s must have a placeholder."), "wpdb::prepare()"), "3.9.0")
        # end if
        #// If args were passed as an array (as in vsprintf), move them up.
        passed_as_array = False
        if php_is_array(args[0]) and php_count(args) == 1:
            passed_as_array = True
            args = args[0]
        # end if
        for arg in args:
            if (not is_scalar(arg)) and (not is_null(arg)):
                wp_load_translations_early()
                _doing_it_wrong("wpdb::prepare", php_sprintf(__("Unsupported value type (%s)."), gettype(arg)), "4.8.2")
            # end if
        # end for
        #// 
        #// Specify the formatting allowed in a placeholder. The following are allowed:
        #// 
        #// - Sign specifier. eg, $+d
        #// - Numbered placeholders. eg, %1$s
        #// - Padding specifier, including custom padding characters. eg, %05s, %'#5s
        #// - Alignment specifier. eg, %05-s
        #// - Precision specifier. eg, %.2f
        #//
        allowed_format = "(?:[1-9][0-9]*[$])?[-+0-9]*(?: |0|'.)?[-+0-9]*(?:\\.[0-9]+)?"
        #// 
        #// If a %s placeholder already has quotes around it, removing the existing quotes and re-inserting them
        #// ensures the quotes are consistent.
        #// 
        #// For backward compatibility, this is only applied to %s, and not to placeholders like %1$s, which are frequently
        #// used in the middle of longer strings, or as table name placeholders.
        #//
        query = php_str_replace("'%s'", "%s", query)
        #// Strip any existing single quotes.
        query = php_str_replace("\"%s\"", "%s", query)
        #// Strip any existing double quotes.
        query = php_preg_replace("/(?<!%)%s/", "'%s'", query)
        #// Quote the strings, avoiding escaped strings like %%s.
        query = php_preg_replace(str("/(?<!%)(%(") + str(allowed_format) + str(")?f)/"), "%\\2F", query)
        #// Force floats to be locale-unaware.
        query = php_preg_replace(str("/%(?:%|$|(?!(") + str(allowed_format) + str(")?[sdF]))/"), "%%\\1", query)
        #// Escape any unescaped percents.
        #// Count the number of valid placeholders in the query.
        placeholders = preg_match_all(str("/(^|[^%]|(%%)+)%(") + str(allowed_format) + str(")?[sdF]/"), query, matches)
        if php_count(args) != placeholders:
            if 1 == placeholders and passed_as_array:
                #// If the passed query only expected one argument, but the wrong number of arguments were sent as an array, bail.
                wp_load_translations_early()
                _doing_it_wrong("wpdb::prepare", __("The query only expected one placeholder, but an array of multiple placeholders was sent."), "4.9.0")
                return
            else:
                #// 
                #// If we don't have the right number of placeholders, but they were passed as individual arguments,
                #// or we were expecting multiple arguments in an array, throw a warning.
                #//
                wp_load_translations_early()
                _doing_it_wrong("wpdb::prepare", php_sprintf(__("The query does not contain the correct number of placeholders (%1$d) for the number of arguments passed (%2$d)."), placeholders, php_count(args)), "4.8.3")
            # end if
        # end if
        array_walk(args, Array(self, "escape_by_ref"))
        query = vsprintf(query, args)
        return self.add_placeholder_escape(query)
    # end def prepare
    #// 
    #// First half of escaping for LIKE special characters % and _ before preparing for MySQL.
    #// 
    #// Use this only before wpdb::prepare() or esc_sql().  Reversing the order is very bad for security.
    #// 
    #// Example Prepared Statement:
    #// 
    #// $wild = '%';
    #// $find = 'only 43% of planets';
    #// $like = $wild . $wpdb->esc_like( $find ) . $wild;
    #// $sql  = $wpdb->prepare( "SELECT * FROM $wpdb->posts WHERE post_content LIKE %s", $like );
    #// 
    #// Example Escape Chain:
    #// 
    #// $sql  = esc_sql( $wpdb->esc_like( $input ) );
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $text The raw text to be escaped. The input typed by the user should have no
    #// extra or deleted slashes.
    #// @return string Text in the form of a LIKE phrase. The output is not SQL safe. Call $wpdb::prepare()
    #// or real_escape next.
    #//
    def esc_like(self, text=None):
        
        return addcslashes(text, "_%\\")
    # end def esc_like
    #// 
    #// Print SQL/DB error.
    #// 
    #// @since 0.71
    #// @global array $EZSQL_ERROR Stores error information of query and error string.
    #// 
    #// @param string $str The error to display.
    #// @return void|false Void if the showing of errors is enabled, false if disabled.
    #//
    def print_error(self, str=""):
        
        global EZSQL_ERROR
        php_check_if_defined("EZSQL_ERROR")
        if (not str):
            if self.use_mysqli:
                str = mysqli_error(self.dbh)
            else:
                str = mysql_error(self.dbh)
            # end if
        # end if
        EZSQL_ERROR[-1] = Array({"query": self.last_query, "error_str": str})
        if self.suppress_errors:
            return False
        # end if
        wp_load_translations_early()
        caller = self.get_caller()
        if caller:
            #// translators: 1: Database error message, 2: SQL query, 3: Name of the calling function.
            error_str = php_sprintf(__("WordPress database error %1$s for query %2$s made by %3$s"), str, self.last_query, caller)
        else:
            #// translators: 1: Database error message, 2: SQL query.
            error_str = php_sprintf(__("WordPress database error %1$s for query %2$s"), str, self.last_query)
        # end if
        php_error_log(error_str)
        #// Are we showing errors?
        if (not self.show_errors):
            return False
        # end if
        #// If there is an error then take note of it.
        if is_multisite():
            msg = php_sprintf("%s [%s]\n%s\n", __("WordPress database error:"), str, self.last_query)
            if php_defined("ERRORLOGFILE"):
                php_error_log(msg, 3, ERRORLOGFILE)
            # end if
            if php_defined("DIEONDBERROR"):
                wp_die(msg)
            # end if
        else:
            str = htmlspecialchars(str, ENT_QUOTES)
            query = htmlspecialchars(self.last_query, ENT_QUOTES)
            printf("<div id=\"error\"><p class=\"wpdberror\"><strong>%s</strong> [%s]<br /><code>%s</code></p></div>", __("WordPress database error:"), str, query)
        # end if
    # end def print_error
    #// 
    #// Enables showing of database errors.
    #// 
    #// This function should be used only to enable showing of errors.
    #// wpdb::hide_errors() should be used instead for hiding of errors. However,
    #// this function can be used to enable and disable showing of database
    #// errors.
    #// 
    #// @since 0.71
    #// @see wpdb::hide_errors()
    #// 
    #// @param bool $show Whether to show or hide errors
    #// @return bool Old value for showing errors.
    #//
    def show_errors(self, show=True):
        
        errors = self.show_errors
        self.show_errors = show
        return errors
    # end def show_errors
    #// 
    #// Disables showing of database errors.
    #// 
    #// By default database errors are not shown.
    #// 
    #// @since 0.71
    #// @see wpdb::show_errors()
    #// 
    #// @return bool Whether showing of errors was active
    #//
    def hide_errors(self):
        
        show = self.show_errors
        self.show_errors = False
        return show
    # end def hide_errors
    #// 
    #// Whether to suppress database errors.
    #// 
    #// By default database errors are suppressed, with a simple
    #// call to this function they can be enabled.
    #// 
    #// @since 2.5.0
    #// @see wpdb::hide_errors()
    #// @param bool $suppress Optional. New value. Defaults to true.
    #// @return bool Old value
    #//
    def suppress_errors(self, suppress=True):
        
        errors = self.suppress_errors
        self.suppress_errors = php_bool(suppress)
        return errors
    # end def suppress_errors
    #// 
    #// Kill cached query results.
    #// 
    #// @since 0.71
    #//
    def flush(self):
        
        self.last_result = Array()
        self.col_info = None
        self.last_query = None
        self.rows_affected = 0
        self.num_rows = 0
        self.last_error = ""
        if self.use_mysqli and type(self.result).__name__ == "mysqli_result":
            mysqli_free_result(self.result)
            self.result = None
            #// Sanity check before using the handle.
            if php_empty(lambda : self.dbh) or (not type(self.dbh).__name__ == "mysqli"):
                return
            # end if
            #// Clear out any results from a multi-query.
            while True:
                
                if not (mysqli_more_results(self.dbh)):
                    break
                # end if
                mysqli_next_result(self.dbh)
            # end while
        elif is_resource(self.result):
            mysql_free_result(self.result)
        # end if
    # end def flush
    #// 
    #// Connect to and select database.
    #// 
    #// If $allow_bail is false, the lack of database connection will need
    #// to be handled manually.
    #// 
    #// @since 3.0.0
    #// @since 3.9.0 $allow_bail parameter added.
    #// 
    #// @param bool $allow_bail Optional. Allows the function to bail. Default true.
    #// @return bool True with a successful connection, false on failure.
    #//
    def db_connect(self, allow_bail=True):
        
        self.is_mysql = True
        #// 
        #// Deprecated in 3.9+ when using MySQLi. No equivalent
        #// $new_link parameter exists for mysqli_* functions.
        #//
        new_link = MYSQL_NEW_LINK if php_defined("MYSQL_NEW_LINK") else True
        client_flags = MYSQL_CLIENT_FLAGS if php_defined("MYSQL_CLIENT_FLAGS") else 0
        if self.use_mysqli:
            self.dbh = php_mysqli_init()
            host = self.dbhost
            port = None
            socket = None
            is_ipv6 = False
            host_data = self.parse_db_host(self.dbhost)
            if host_data:
                host, port, socket, is_ipv6 = host_data
            # end if
            #// 
            #// If using the `mysqlnd` library, the IPv6 address needs to be
            #// enclosed in square brackets, whereas it doesn't while using the
            #// `libmysqlclient` library.
            #// @see https://bugs.php.net/bug.php?id=67563
            #//
            if is_ipv6 and php_extension_loaded("mysqlnd"):
                host = str("[") + str(host) + str("]")
            # end if
            if WP_DEBUG:
                php_mysqli_real_connect(self.dbh, host, self.dbuser, self.dbpassword, None, port, socket, client_flags)
            else:
                #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
                php_no_error(lambda: php_mysqli_real_connect(self.dbh, host, self.dbuser, self.dbpassword, None, port, socket, client_flags))
            # end if
            if self.dbh.connect_errno:
                self.dbh = None
                #// 
                #// It's possible ext/mysqli is misconfigured. Fall back to ext/mysql if:
                #// - We haven't previously connected, and
                #// - WP_USE_EXT_MYSQL isn't set to false, and
                #// - ext/mysql is loaded.
                #//
                attempt_fallback = True
                if self.has_connected:
                    attempt_fallback = False
                elif php_defined("WP_USE_EXT_MYSQL") and (not WP_USE_EXT_MYSQL):
                    attempt_fallback = False
                elif (not php_function_exists("mysql_connect")):
                    attempt_fallback = False
                # end if
                if attempt_fallback:
                    self.use_mysqli = False
                    return self.db_connect(allow_bail)
                # end if
            # end if
        else:
            if WP_DEBUG:
                self.dbh = mysql_connect(self.dbhost, self.dbuser, self.dbpassword, new_link, client_flags)
            else:
                #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
                self.dbh = php_no_error(lambda: mysql_connect(self.dbhost, self.dbuser, self.dbpassword, new_link, client_flags))
            # end if
        # end if
        if (not self.dbh) and allow_bail:
            wp_load_translations_early()
            #// Load custom DB error template, if present.
            if php_file_exists(WP_CONTENT_DIR + "/db-error.php"):
                php_include_file(WP_CONTENT_DIR + "/db-error.php", once=True)
                php_exit(0)
            # end if
            message = "<h1>" + __("Error establishing a database connection") + "</h1>\n"
            message += "<p>" + php_sprintf(__("This either means that the username and password information in your %1$s file is incorrect or we can&#8217;t contact the database server at %2$s. This could mean your host&#8217;s database server is down."), "<code>wp-config.php</code>", "<code>" + htmlspecialchars(self.dbhost, ENT_QUOTES) + "</code>") + "</p>\n"
            message += "<ul>\n"
            message += "<li>" + __("Are you sure you have the correct username and password?") + "</li>\n"
            message += "<li>" + __("Are you sure you have typed the correct hostname?") + "</li>\n"
            message += "<li>" + __("Are you sure the database server is running?") + "</li>\n"
            message += "</ul>\n"
            message += "<p>" + php_sprintf(__("If you&#8217;re unsure what these terms mean you should probably contact your host. If you still need help you can always visit the <a href=\"%s\">WordPress Support Forums</a>."), __("https://wordpress.org/support/forums/")) + "</p>\n"
            self.bail(message, "db_connect_fail")
            return False
        elif self.dbh:
            if (not self.has_connected):
                self.init_charset()
            # end if
            self.has_connected = True
            self.set_charset(self.dbh)
            self.ready = True
            self.set_sql_mode()
            self.select(self.dbname, self.dbh)
            return True
        # end if
        return False
    # end def db_connect
    #// 
    #// Parse the DB_HOST setting to interpret it for mysqli_real_connect.
    #// 
    #// mysqli_real_connect doesn't support the host param including a port or
    #// socket like mysql_connect does. This duplicates how mysql_connect detects
    #// a port and/or socket file.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $host The DB_HOST setting to parse.
    #// @return array|bool Array containing the host, the port, the socket and whether
    #// it is an IPv6 address, in that order. If $host couldn't be parsed,
    #// returns false.
    #//
    def parse_db_host(self, host=None):
        
        port = None
        socket = None
        is_ipv6 = False
        #// First peel off the socket parameter from the right, if it exists.
        socket_pos = php_strpos(host, ":/")
        if False != socket_pos:
            socket = php_substr(host, socket_pos + 1)
            host = php_substr(host, 0, socket_pos)
        # end if
        #// We need to check for an IPv6 address first.
        #// An IPv6 address will always contain at least two colons.
        if php_substr_count(host, ":") > 1:
            pattern = "#^(?:\\[)?(?P<host>[0-9a-fA-F:]+)(?:\\]:(?P<port>[\\d]+))?#"
            is_ipv6 = True
        else:
            #// We seem to be dealing with an IPv4 address.
            pattern = "#^(?P<host>[^:/]*)(?::(?P<port>[\\d]+))?#"
        # end if
        matches = Array()
        result = php_preg_match(pattern, host, matches)
        if 1 != result:
            #// Couldn't parse the address, bail.
            return False
        # end if
        host = ""
        for component in Array("host", "port"):
            if (not php_empty(lambda : matches[component])):
                component = matches[component]
            # end if
        # end for
        return Array(host, port, socket, is_ipv6)
    # end def parse_db_host
    #// 
    #// Checks that the connection to the database is still up. If not, try to reconnect.
    #// 
    #// If this function is unable to reconnect, it will forcibly die, or if after the
    #// the {@see 'template_redirect'} hook has been fired, return false instead.
    #// 
    #// If $allow_bail is false, the lack of database connection will need
    #// to be handled manually.
    #// 
    #// @since 3.9.0
    #// 
    #// @param bool $allow_bail Optional. Allows the function to bail. Default true.
    #// @return bool|void True if the connection is up.
    #//
    def check_connection(self, allow_bail=True):
        
        if self.use_mysqli:
            if (not php_empty(lambda : self.dbh)) and mysqli_ping(self.dbh):
                return True
            # end if
        else:
            if (not php_empty(lambda : self.dbh)) and mysql_ping(self.dbh):
                return True
            # end if
        # end if
        error_reporting = False
        #// Disable warnings, as we don't want to see a multitude of "unable to connect" messages.
        if WP_DEBUG:
            error_reporting = php_error_reporting()
            php_error_reporting(error_reporting & (1 << (E_WARNING).bit_length()) - 1 - E_WARNING)
        # end if
        tries = 1
        while tries <= self.reconnect_retries:
            
            #// On the last try, re-enable warnings. We want to see a single instance
            #// of the "unable to connect" message on the bail() screen, if it appears.
            if self.reconnect_retries == tries and WP_DEBUG:
                php_error_reporting(error_reporting)
            # end if
            if self.db_connect(False):
                if error_reporting:
                    php_error_reporting(error_reporting)
                # end if
                return True
            # end if
            sleep(1)
            tries += 1
        # end while
        #// If template_redirect has already happened, it's too late for wp_die()/dead_db().
        #// Let's just return and hope for the best.
        if did_action("template_redirect"):
            return False
        # end if
        if (not allow_bail):
            return False
        # end if
        wp_load_translations_early()
        message = "<h1>" + __("Error reconnecting to the database") + "</h1>\n"
        message += "<p>" + php_sprintf(__("This means that we lost contact with the database server at %s. This could mean your host&#8217;s database server is down."), "<code>" + htmlspecialchars(self.dbhost, ENT_QUOTES) + "</code>") + "</p>\n"
        message += "<ul>\n"
        message += "<li>" + __("Are you sure the database server is running?") + "</li>\n"
        message += "<li>" + __("Are you sure the database server is not under particularly heavy load?") + "</li>\n"
        message += "</ul>\n"
        message += "<p>" + php_sprintf(__("If you&#8217;re unsure what these terms mean you should probably contact your host. If you still need help you can always visit the <a href=\"%s\">WordPress Support Forums</a>."), __("https://wordpress.org/support/forums/")) + "</p>\n"
        #// We weren't able to reconnect, so we better bail.
        self.bail(message, "db_connect_fail")
        #// Call dead_db() if bail didn't die, because this database is no more.
        #// It has ceased to be (at least temporarily).
        dead_db()
    # end def check_connection
    #// 
    #// Perform a MySQL database query, using current database connection.
    #// 
    #// More information can be found on the codex page.
    #// 
    #// @since 0.71
    #// 
    #// @param string $query Database query
    #// @return int|bool Boolean true for CREATE, ALTER, TRUNCATE and DROP queries. Number of rows
    #// affected/selected for all other queries. Boolean false on error.
    #//
    def query(self, query=None):
        
        if (not self.ready):
            self.check_current_query = True
            return False
        # end if
        #// 
        #// Filters the database query.
        #// 
        #// Some queries are made before the plugins have been loaded,
        #// and thus cannot be filtered with this method.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $query Database query.
        #//
        query = apply_filters("query", query)
        self.flush()
        #// Log how the function was called.
        self.func_call = str("$db->query(\"") + str(query) + str("\")")
        #// If we're writing to the database, make sure the query will write safely.
        if self.check_current_query and (not self.check_ascii(query)):
            stripped_query = self.strip_invalid_text_from_query(query)
            #// strip_invalid_text_from_query() can perform queries, so we need
            #// to flush again, just to make sure everything is clear.
            self.flush()
            if stripped_query != query:
                self.insert_id = 0
                return False
            # end if
        # end if
        self.check_current_query = True
        #// Keep track of the last query for debug.
        self.last_query = query
        self._do_query(query)
        #// MySQL server has gone away, try to reconnect.
        mysql_errno = 0
        if (not php_empty(lambda : self.dbh)):
            if self.use_mysqli:
                if type(self.dbh).__name__ == "mysqli":
                    mysql_errno = mysqli_errno(self.dbh)
                else:
                    #// $dbh is defined, but isn't a real connection.
                    #// Something has gone horribly wrong, let's try a reconnect.
                    mysql_errno = 2006
                # end if
            else:
                if is_resource(self.dbh):
                    mysql_errno = mysql_errno(self.dbh)
                else:
                    mysql_errno = 2006
                # end if
            # end if
        # end if
        if php_empty(lambda : self.dbh) or 2006 == mysql_errno:
            if self.check_connection():
                self._do_query(query)
            else:
                self.insert_id = 0
                return False
            # end if
        # end if
        #// If there is an error then take note of it.
        if self.use_mysqli:
            if type(self.dbh).__name__ == "mysqli":
                self.last_error = mysqli_error(self.dbh)
            else:
                self.last_error = __("Unable to retrieve the error message from MySQL")
            # end if
        else:
            if is_resource(self.dbh):
                self.last_error = mysql_error(self.dbh)
            else:
                self.last_error = __("Unable to retrieve the error message from MySQL")
            # end if
        # end if
        if self.last_error:
            #// Clear insert_id on a subsequent failed insert.
            if self.insert_id and php_preg_match("/^\\s*(insert|replace)\\s/i", query):
                self.insert_id = 0
            # end if
            self.print_error()
            return False
        # end if
        if php_preg_match("/^\\s*(create|alter|truncate|drop)\\s/i", query):
            return_val = self.result
        elif php_preg_match("/^\\s*(insert|delete|update|replace)\\s/i", query):
            if self.use_mysqli:
                self.rows_affected = mysqli_affected_rows(self.dbh)
            else:
                self.rows_affected = mysql_affected_rows(self.dbh)
            # end if
            #// Take note of the insert_id.
            if php_preg_match("/^\\s*(insert|replace)\\s/i", query):
                if self.use_mysqli:
                    self.insert_id = mysqli_insert_id(self.dbh)
                else:
                    self.insert_id = mysql_insert_id(self.dbh)
                # end if
            # end if
            #// Return number of rows affected.
            return_val = self.rows_affected
        else:
            num_rows = 0
            if self.use_mysqli and type(self.result).__name__ == "mysqli_result":
                while True:
                    row = mysqli_fetch_object(self.result)
                    if not (row):
                        break
                    # end if
                    self.last_result[num_rows] = row
                    num_rows += 1
                # end while
            elif is_resource(self.result):
                while True:
                    row = mysql_fetch_object(self.result)
                    if not (row):
                        break
                    # end if
                    self.last_result[num_rows] = row
                    num_rows += 1
                # end while
            # end if
            #// Log number of rows the query returned
            #// and return number of rows selected.
            self.num_rows = num_rows
            return_val = num_rows
        # end if
        return return_val
    # end def query
    #// 
    #// Internal function to perform the mysql_query() call.
    #// 
    #// @since 3.9.0
    #// 
    #// @see wpdb::query()
    #// 
    #// @param string $query The query to run.
    #//
    def _do_query(self, query=None):
        
        if php_defined("SAVEQUERIES") and SAVEQUERIES:
            self.timer_start()
        # end if
        if (not php_empty(lambda : self.dbh)) and self.use_mysqli:
            self.result = mysqli_query(self.dbh, query)
        elif (not php_empty(lambda : self.dbh)):
            self.result = mysql_query(query, self.dbh)
        # end if
        self.num_queries += 1
        if php_defined("SAVEQUERIES") and SAVEQUERIES:
            self.log_query(query, self.timer_stop(), self.get_caller(), self.time_start, Array())
        # end if
    # end def _do_query
    #// 
    #// Logs query data.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $query           The query's SQL.
    #// @param float  $query_time      Total time spent on the query, in seconds.
    #// @param string $query_callstack Comma separated list of the calling functions.
    #// @param float  $query_start     Unix timestamp of the time at the start of the query.
    #// @param array  $query_data      Custom query data.
    #// }
    #//
    def log_query(self, query=None, query_time=None, query_callstack=None, query_start=None, query_data=None):
        
        #// 
        #// Filters the custom query data being logged.
        #// 
        #// Caution should be used when modifying any of this data, it is recommended that any additional
        #// information you need to store about a query be added as a new associative entry to the fourth
        #// element $query_data.
        #// 
        #// @since 5.3.0
        #// 
        #// @param array  $query_data      Custom query data.
        #// @param string $query           The query's SQL.
        #// @param float  $query_time      Total time spent on the query, in seconds.
        #// @param string $query_callstack Comma separated list of the calling functions.
        #// @param float  $query_start     Unix timestamp of the time at the start of the query.
        #//
        query_data = apply_filters("log_query_custom_data", query_data, query, query_time, query_callstack, query_start)
        self.queries[-1] = Array(query, query_time, query_callstack, query_start, query_data)
    # end def log_query
    #// 
    #// Generates and returns a placeholder escape string for use in queries returned by ::prepare().
    #// 
    #// @since 4.8.3
    #// 
    #// @return string String to escape placeholders.
    #//
    def placeholder_escape(self):
        
        placeholder_escape.placeholder = None
        if (not placeholder_escape.placeholder):
            #// If ext/hash is not present, compat.php's hash_hmac() does not support sha256.
            algo = "sha256" if php_function_exists("hash") else "sha1"
            #// Old WP installs may not have AUTH_SALT defined.
            salt = AUTH_SALT if php_defined("AUTH_SALT") and AUTH_SALT else php_str(rand())
            placeholder_escape.placeholder = "{" + hash_hmac(algo, uniqid(salt, True), salt) + "}"
        # end if
        #// 
        #// Add the filter to remove the placeholder escaper. Uses priority 0, so that anything
        #// else attached to this filter will receive the query with the placeholder string removed.
        #//
        if False == has_filter("query", Array(self, "remove_placeholder_escape")):
            add_filter("query", Array(self, "remove_placeholder_escape"), 0)
        # end if
        return placeholder_escape.placeholder
    # end def placeholder_escape
    #// 
    #// Adds a placeholder escape string, to escape anything that resembles a printf() placeholder.
    #// 
    #// @since 4.8.3
    #// 
    #// @param string $query The query to escape.
    #// @return string The query with the placeholder escape string inserted where necessary.
    #//
    def add_placeholder_escape(self, query=None):
        
        #// 
        #// To prevent returning anything that even vaguely resembles a placeholder,
        #// we clobber every % we can find.
        #//
        return php_str_replace("%", self.placeholder_escape(), query)
    # end def add_placeholder_escape
    #// 
    #// Removes the placeholder escape strings from a query.
    #// 
    #// @since 4.8.3
    #// 
    #// @param string $query The query from which the placeholder will be removed.
    #// @return string The query with the placeholder removed.
    #//
    def remove_placeholder_escape(self, query=None):
        
        return php_str_replace(self.placeholder_escape(), "%", query)
    # end def remove_placeholder_escape
    #// 
    #// Insert a row into a table.
    #// 
    #// wpdb::insert( 'table', array( 'column' => 'foo', 'field' => 'bar' ) )
    #// wpdb::insert( 'table', array( 'column' => 'foo', 'field' => 1337 ), array( '%s', '%d' ) )
    #// 
    #// @since 2.5.0
    #// @see wpdb::prepare()
    #// @see wpdb::$field_types
    #// @see wp_set_wpdb_vars()
    #// 
    #// @param string       $table  Table name
    #// @param array        $data   Data to insert (in column => value pairs).
    #// Both $data columns and $data values should be "raw" (neither should be SQL escaped).
    #// Sending a null value will cause the column to be set to NULL - the corresponding format is ignored in this case.
    #// @param array|string $format Optional. An array of formats to be mapped to each of the value in $data.
    #// If string, that format will be used for all of the values in $data.
    #// A format is one of '%d', '%f', '%s' (integer, float, string).
    #// If omitted, all values in $data will be treated as strings unless otherwise specified in wpdb::$field_types.
    #// @return int|false The number of rows inserted, or false on error.
    #//
    def insert(self, table=None, data=None, format=None):
        
        return self._insert_replace_helper(table, data, format, "INSERT")
    # end def insert
    #// 
    #// Replace a row into a table.
    #// 
    #// wpdb::replace( 'table', array( 'column' => 'foo', 'field' => 'bar' ) )
    #// wpdb::replace( 'table', array( 'column' => 'foo', 'field' => 1337 ), array( '%s', '%d' ) )
    #// 
    #// @since 3.0.0
    #// @see wpdb::prepare()
    #// @see wpdb::$field_types
    #// @see wp_set_wpdb_vars()
    #// 
    #// @param string       $table  Table name
    #// @param array        $data   Data to insert (in column => value pairs).
    #// Both $data columns and $data values should be "raw" (neither should be SQL escaped).
    #// Sending a null value will cause the column to be set to NULL - the corresponding format is ignored in this case.
    #// @param array|string $format Optional. An array of formats to be mapped to each of the value in $data.
    #// If string, that format will be used for all of the values in $data.
    #// A format is one of '%d', '%f', '%s' (integer, float, string).
    #// If omitted, all values in $data will be treated as strings unless otherwise specified in wpdb::$field_types.
    #// @return int|false The number of rows affected, or false on error.
    #//
    def replace(self, table=None, data=None, format=None):
        
        return self._insert_replace_helper(table, data, format, "REPLACE")
    # end def replace
    #// 
    #// Helper function for insert and replace.
    #// 
    #// Runs an insert or replace query based on $type argument.
    #// 
    #// @since 3.0.0
    #// @see wpdb::prepare()
    #// @see wpdb::$field_types
    #// @see wp_set_wpdb_vars()
    #// 
    #// @param string       $table  Table name
    #// @param array        $data   Data to insert (in column => value pairs).
    #// Both $data columns and $data values should be "raw" (neither should be SQL escaped).
    #// Sending a null value will cause the column to be set to NULL - the corresponding format is ignored in this case.
    #// @param array|string $format Optional. An array of formats to be mapped to each of the value in $data.
    #// If string, that format will be used for all of the values in $data.
    #// A format is one of '%d', '%f', '%s' (integer, float, string).
    #// If omitted, all values in $data will be treated as strings unless otherwise specified in wpdb::$field_types.
    #// @param string $type         Optional. What type of operation is this? INSERT or REPLACE. Defaults to INSERT.
    #// @return int|false The number of rows affected, or false on error.
    #//
    def _insert_replace_helper(self, table=None, data=None, format=None, type="INSERT"):
        
        self.insert_id = 0
        if (not php_in_array(php_strtoupper(type), Array("REPLACE", "INSERT"))):
            return False
        # end if
        data = self.process_fields(table, data, format)
        if False == data:
            return False
        # end if
        formats = Array()
        values = Array()
        for value in data:
            if is_null(value["value"]):
                formats[-1] = "NULL"
                continue
            # end if
            formats[-1] = value["format"]
            values[-1] = value["value"]
        # end for
        fields = "`" + php_implode("`, `", php_array_keys(data)) + "`"
        formats = php_implode(", ", formats)
        sql = str(type) + str(" INTO `") + str(table) + str("` (") + str(fields) + str(") VALUES (") + str(formats) + str(")")
        self.check_current_query = False
        return self.query(self.prepare(sql, values))
    # end def _insert_replace_helper
    #// 
    #// Update a row in the table
    #// 
    #// wpdb::update( 'table', array( 'column' => 'foo', 'field' => 'bar' ), array( 'ID' => 1 ) )
    #// wpdb::update( 'table', array( 'column' => 'foo', 'field' => 1337 ), array( 'ID' => 1 ), array( '%s', '%d' ), array( '%d' ) )
    #// 
    #// @since 2.5.0
    #// @see wpdb::prepare()
    #// @see wpdb::$field_types
    #// @see wp_set_wpdb_vars()
    #// 
    #// @param string       $table        Table name
    #// @param array        $data         Data to update (in column => value pairs).
    #// Both $data columns and $data values should be "raw" (neither should be SQL escaped).
    #// Sending a null value will cause the column to be set to NULL - the corresponding
    #// format is ignored in this case.
    #// @param array        $where        A named array of WHERE clauses (in column => value pairs).
    #// Multiple clauses will be joined with ANDs.
    #// Both $where columns and $where values should be "raw".
    #// Sending a null value will create an IS NULL comparison - the corresponding format will be ignored in this case.
    #// @param array|string $format       Optional. An array of formats to be mapped to each of the values in $data.
    #// If string, that format will be used for all of the values in $data.
    #// A format is one of '%d', '%f', '%s' (integer, float, string).
    #// If omitted, all values in $data will be treated as strings unless otherwise specified in wpdb::$field_types.
    #// @param array|string $where_format Optional. An array of formats to be mapped to each of the values in $where.
    #// If string, that format will be used for all of the items in $where.
    #// A format is one of '%d', '%f', '%s' (integer, float, string).
    #// If omitted, all values in $where will be treated as strings.
    #// @return int|false The number of rows updated, or false on error.
    #//
    def update(self, table=None, data=None, where=None, format=None, where_format=None):
        
        if (not php_is_array(data)) or (not php_is_array(where)):
            return False
        # end if
        data = self.process_fields(table, data, format)
        if False == data:
            return False
        # end if
        where = self.process_fields(table, where, where_format)
        if False == where:
            return False
        # end if
        fields = Array()
        conditions = Array()
        values = Array()
        for field,value in data:
            if is_null(value["value"]):
                fields[-1] = str("`") + str(field) + str("` = NULL")
                continue
            # end if
            fields[-1] = str("`") + str(field) + str("` = ") + value["format"]
            values[-1] = value["value"]
        # end for
        for field,value in where:
            if is_null(value["value"]):
                conditions[-1] = str("`") + str(field) + str("` IS NULL")
                continue
            # end if
            conditions[-1] = str("`") + str(field) + str("` = ") + value["format"]
            values[-1] = value["value"]
        # end for
        fields = php_implode(", ", fields)
        conditions = php_implode(" AND ", conditions)
        sql = str("UPDATE `") + str(table) + str("` SET ") + str(fields) + str(" WHERE ") + str(conditions)
        self.check_current_query = False
        return self.query(self.prepare(sql, values))
    # end def update
    #// 
    #// Delete a row in the table
    #// 
    #// wpdb::delete( 'table', array( 'ID' => 1 ) )
    #// wpdb::delete( 'table', array( 'ID' => 1 ), array( '%d' ) )
    #// 
    #// @since 3.4.0
    #// @see wpdb::prepare()
    #// @see wpdb::$field_types
    #// @see wp_set_wpdb_vars()
    #// 
    #// @param string       $table        Table name
    #// @param array        $where        A named array of WHERE clauses (in column => value pairs).
    #// Multiple clauses will be joined with ANDs.
    #// Both $where columns and $where values should be "raw".
    #// Sending a null value will create an IS NULL comparison - the corresponding format will be ignored in this case.
    #// @param array|string $where_format Optional. An array of formats to be mapped to each of the values in $where.
    #// If string, that format will be used for all of the items in $where.
    #// A format is one of '%d', '%f', '%s' (integer, float, string).
    #// If omitted, all values in $where will be treated as strings unless otherwise specified in wpdb::$field_types.
    #// @return int|false The number of rows updated, or false on error.
    #//
    def delete(self, table=None, where=None, where_format=None):
        
        if (not php_is_array(where)):
            return False
        # end if
        where = self.process_fields(table, where, where_format)
        if False == where:
            return False
        # end if
        conditions = Array()
        values = Array()
        for field,value in where:
            if is_null(value["value"]):
                conditions[-1] = str("`") + str(field) + str("` IS NULL")
                continue
            # end if
            conditions[-1] = str("`") + str(field) + str("` = ") + value["format"]
            values[-1] = value["value"]
        # end for
        conditions = php_implode(" AND ", conditions)
        sql = str("DELETE FROM `") + str(table) + str("` WHERE ") + str(conditions)
        self.check_current_query = False
        return self.query(self.prepare(sql, values))
    # end def delete
    #// 
    #// Processes arrays of field/value pairs and field formats.
    #// 
    #// This is a helper method for wpdb's CRUD methods, which take field/value
    #// pairs for inserts, updates, and where clauses. This method first pairs
    #// each value with a format. Then it determines the charset of that field,
    #// using that to determine if any invalid text would be stripped. If text is
    #// stripped, then field processing is rejected and the query fails.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $table  Table name.
    #// @param array  $data   Field/value pair.
    #// @param mixed  $format Format for each field.
    #// @return array|false Returns an array of fields that contain paired values
    #// and formats. Returns false for invalid values.
    #//
    def process_fields(self, table=None, data=None, format=None):
        
        data = self.process_field_formats(data, format)
        if False == data:
            return False
        # end if
        data = self.process_field_charsets(data, table)
        if False == data:
            return False
        # end if
        data = self.process_field_lengths(data, table)
        if False == data:
            return False
        # end if
        converted_data = self.strip_invalid_text(data)
        if data != converted_data:
            return False
        # end if
        return data
    # end def process_fields
    #// 
    #// Prepares arrays of value/format pairs as passed to wpdb CRUD methods.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array $data   Array of fields to values.
    #// @param mixed $format Formats to be mapped to the values in $data.
    #// @return array Array, keyed by field names with values being an array
    #// of 'value' and 'format' keys.
    #//
    def process_field_formats(self, data=None, format=None):
        
        formats = format
        original_formats = formats
        for field,value in data:
            value = Array({"value": value, "format": "%s"})
            if (not php_empty(lambda : format)):
                value["format"] = php_array_shift(formats)
                if (not value["format"]):
                    value["format"] = reset(original_formats)
                # end if
            elif (php_isset(lambda : self.field_types[field])):
                value["format"] = self.field_types[field]
            # end if
            data[field] = value
        # end for
        return data
    # end def process_field_formats
    #// 
    #// Adds field charsets to field/value/format arrays generated by
    #// the wpdb::process_field_formats() method.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array  $data  As it comes from the wpdb::process_field_formats() method.
    #// @param string $table Table name.
    #// @return array|false The same array as $data with additional 'charset' keys.
    #//
    def process_field_charsets(self, data=None, table=None):
        
        for field,value in data:
            if "%d" == value["format"] or "%f" == value["format"]:
                #// 
                #// We can skip this field if we know it isn't a string.
                #// This checks %d/%f versus ! %s because its sprintf() could take more.
                #//
                value["charset"] = False
            else:
                value["charset"] = self.get_col_charset(table, field)
                if is_wp_error(value["charset"]):
                    return False
                # end if
            # end if
            data[field] = value
        # end for
        return data
    # end def process_field_charsets
    #// 
    #// For string fields, record the maximum string length that field can safely save.
    #// 
    #// @since 4.2.1
    #// 
    #// @param array  $data  As it comes from the wpdb::process_field_charsets() method.
    #// @param string $table Table name.
    #// @return array|false The same array as $data with additional 'length' keys, or false if
    #// any of the values were too long for their corresponding field.
    #//
    def process_field_lengths(self, data=None, table=None):
        
        for field,value in data:
            if "%d" == value["format"] or "%f" == value["format"]:
                #// 
                #// We can skip this field if we know it isn't a string.
                #// This checks %d/%f versus ! %s because its sprintf() could take more.
                #//
                value["length"] = False
            else:
                value["length"] = self.get_col_length(table, field)
                if is_wp_error(value["length"]):
                    return False
                # end if
            # end if
            data[field] = value
        # end for
        return data
    # end def process_field_lengths
    #// 
    #// Retrieve one variable from the database.
    #// 
    #// Executes a SQL query and returns the value from the SQL result.
    #// If the SQL result contains more than one column and/or more than one row, this function returns the value in the column and row specified.
    #// If $query is null, this function returns the value in the specified column and row from the previous SQL result.
    #// 
    #// @since 0.71
    #// 
    #// @param string|null $query Optional. SQL query. Defaults to null, use the result from the previous query.
    #// @param int         $x     Optional. Column of value to return. Indexed from 0.
    #// @param int         $y     Optional. Row of value to return. Indexed from 0.
    #// @return string|null Database query result (as string), or null on failure
    #//
    def get_var(self, query=None, x=0, y=0):
        
        self.func_call = str("$db->get_var(\"") + str(query) + str("\", ") + str(x) + str(", ") + str(y) + str(")")
        if self.check_current_query and self.check_safe_collation(query):
            self.check_current_query = False
        # end if
        if query:
            self.query(query)
        # end if
        #// Extract var out of cached results based x,y vals.
        if (not php_empty(lambda : self.last_result[y])):
            values = php_array_values(get_object_vars(self.last_result[y]))
        # end if
        #// If there is a value return it else return null.
        return values[x] if (php_isset(lambda : values[x])) and "" != values[x] else None
    # end def get_var
    #// 
    #// Retrieve one row from the database.
    #// 
    #// Executes a SQL query and returns the row from the SQL result.
    #// 
    #// @since 0.71
    #// 
    #// @param string|null $query  SQL query.
    #// @param string      $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
    #// an stdClass object, an associative array, or a numeric array, respectively. Default OBJECT.
    #// @param int         $y      Optional. Row to return. Indexed from 0.
    #// @return array|object|null|void Database query result in format specified by $output or null on failure
    #//
    def get_row(self, query=None, output=OBJECT, y=0):
        
        self.func_call = str("$db->get_row(\"") + str(query) + str("\",") + str(output) + str(",") + str(y) + str(")")
        if self.check_current_query and self.check_safe_collation(query):
            self.check_current_query = False
        # end if
        if query:
            self.query(query)
        else:
            return None
        # end if
        if (not (php_isset(lambda : self.last_result[y]))):
            return None
        # end if
        if OBJECT == output:
            return self.last_result[y] if self.last_result[y] else None
        elif ARRAY_A == output:
            return get_object_vars(self.last_result[y]) if self.last_result[y] else None
        elif ARRAY_N == output:
            return php_array_values(get_object_vars(self.last_result[y])) if self.last_result[y] else None
        elif OBJECT == php_strtoupper(output):
            #// Back compat for OBJECT being previously case-insensitive.
            return self.last_result[y] if self.last_result[y] else None
        else:
            self.print_error(" $db->get_row(string query, output type, int offset) -- Output type must be one of: OBJECT, ARRAY_A, ARRAY_N")
        # end if
    # end def get_row
    #// 
    #// Retrieve one column from the database.
    #// 
    #// Executes a SQL query and returns the column from the SQL result.
    #// If the SQL result contains more than one column, this function returns the column specified.
    #// If $query is null, this function returns the specified column from the previous SQL result.
    #// 
    #// @since 0.71
    #// 
    #// @param string|null $query Optional. SQL query. Defaults to previous query.
    #// @param int         $x     Optional. Column to return. Indexed from 0.
    #// @return array Database query result. Array indexed from 0 by SQL result row number.
    #//
    def get_col(self, query=None, x=0):
        
        if self.check_current_query and self.check_safe_collation(query):
            self.check_current_query = False
        # end if
        if query:
            self.query(query)
        # end if
        new_array = Array()
        #// Extract the column values.
        if self.last_result:
            i = 0
            j = php_count(self.last_result)
            while i < j:
                
                new_array[i] = self.get_var(None, x, i)
                i += 1
            # end while
        # end if
        return new_array
    # end def get_col
    #// 
    #// Retrieve an entire SQL result set from the database (i.e., many rows)
    #// 
    #// Executes a SQL query and returns the entire SQL result.
    #// 
    #// @since 0.71
    #// 
    #// @param string $query  SQL query.
    #// @param string $output Optional. Any of ARRAY_A | ARRAY_N | OBJECT | OBJECT_K constants.
    #// With one of the first three, return an array of rows indexed from 0 by SQL result row number.
    #// Each row is an associative array (column => value, ...), a numerically indexed array (0 => value, ...), or an object. ( ->column = value ), respectively.
    #// With OBJECT_K, return an associative array of row objects keyed by the value of each row's first column's value.
    #// Duplicate keys are discarded.
    #// @return array|object|null Database query results
    #//
    def get_results(self, query=None, output=OBJECT):
        
        self.func_call = str("$db->get_results(\"") + str(query) + str("\", ") + str(output) + str(")")
        if self.check_current_query and self.check_safe_collation(query):
            self.check_current_query = False
        # end if
        if query:
            self.query(query)
        else:
            return None
        # end if
        new_array = Array()
        if OBJECT == output:
            #// Return an integer-keyed array of row objects.
            return self.last_result
        elif OBJECT_K == output:
            #// Return an array of row objects with keys from column 1.
            #// (Duplicates are discarded.)
            if self.last_result:
                for row in self.last_result:
                    var_by_ref = get_object_vars(row)
                    key = php_array_shift(var_by_ref)
                    if (not (php_isset(lambda : new_array[key]))):
                        new_array[key] = row
                    # end if
                # end for
            # end if
            return new_array
        elif ARRAY_A == output or ARRAY_N == output:
            #// Return an integer-keyed array of...
            if self.last_result:
                for row in self.last_result:
                    if ARRAY_N == output:
                        #// ...integer-keyed row arrays.
                        new_array[-1] = php_array_values(get_object_vars(row))
                    else:
                        #// ...column name-keyed row arrays.
                        new_array[-1] = get_object_vars(row)
                    # end if
                # end for
            # end if
            return new_array
        elif php_strtoupper(output) == OBJECT:
            #// Back compat for OBJECT being previously case-insensitive.
            return self.last_result
        # end if
        return None
    # end def get_results
    #// 
    #// Retrieves the character set for the given table.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $table Table name.
    #// @return string|WP_Error Table character set, WP_Error object if it couldn't be found.
    #//
    def get_table_charset(self, table=None):
        
        tablekey = php_strtolower(table)
        #// 
        #// Filters the table charset value before the DB is checked.
        #// 
        #// Passing a non-null value to the filter will effectively short-circuit
        #// checking the DB for the charset, returning that value instead.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string|null $charset The character set to use. Default null.
        #// @param string      $table   The name of the table being checked.
        #//
        charset = apply_filters("pre_get_table_charset", None, table)
        if None != charset:
            return charset
        # end if
        if (php_isset(lambda : self.table_charset[tablekey])):
            return self.table_charset[tablekey]
        # end if
        charsets = Array()
        columns = Array()
        table_parts = php_explode(".", table)
        table = "`" + php_implode("`.`", table_parts) + "`"
        results = self.get_results(str("SHOW FULL COLUMNS FROM ") + str(table))
        if (not results):
            return php_new_class("WP_Error", lambda : WP_Error("wpdb_get_table_charset_failure"))
        # end if
        for column in results:
            columns[php_strtolower(column.Field)] = column
        # end for
        self.col_meta[tablekey] = columns
        for column in columns:
            if (not php_empty(lambda : column.Collation)):
                charset = php_explode("_", column.Collation)
                #// If the current connection can't support utf8mb4 characters, let's only send 3-byte utf8 characters.
                if "utf8mb4" == charset and (not self.has_cap("utf8mb4")):
                    charset = "utf8"
                # end if
                charsets[php_strtolower(charset)] = True
            # end if
            type = php_explode("(", column.Type)
            #// A binary/blob means the whole query gets treated like this.
            if php_in_array(php_strtoupper(type), Array("BINARY", "VARBINARY", "TINYBLOB", "MEDIUMBLOB", "BLOB", "LONGBLOB")):
                self.table_charset[tablekey] = "binary"
                return "binary"
            # end if
        # end for
        #// utf8mb3 is an alias for utf8.
        if (php_isset(lambda : charsets["utf8mb3"])):
            charsets["utf8"] = True
            charsets["utf8mb3"] = None
        # end if
        #// Check if we have more than one charset in play.
        count = php_count(charsets)
        if 1 == count:
            charset = key(charsets)
        elif 0 == count:
            #// No charsets, assume this table can store whatever.
            charset = False
        else:
            charsets["latin1"] = None
            count = php_count(charsets)
            if 1 == count:
                #// Only one charset (besides latin1).
                charset = key(charsets)
            elif 2 == count and (php_isset(lambda : charsets["utf8"]) and php_isset(lambda : charsets["utf8mb4"])):
                #// Two charsets, but they're utf8 and utf8mb4, use utf8.
                charset = "utf8"
            else:
                #// Two mixed character sets. ascii.
                charset = "ascii"
            # end if
        # end if
        self.table_charset[tablekey] = charset
        return charset
    # end def get_table_charset
    #// 
    #// Retrieves the character set for the given column.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $table  Table name.
    #// @param string $column Column name.
    #// @return string|false|WP_Error Column character set as a string. False if the column has no
    #// character set. WP_Error object if there was an error.
    #//
    def get_col_charset(self, table=None, column=None):
        
        tablekey = php_strtolower(table)
        columnkey = php_strtolower(column)
        #// 
        #// Filters the column charset value before the DB is checked.
        #// 
        #// Passing a non-null value to the filter will short-circuit
        #// checking the DB for the charset, returning that value instead.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string|null $charset The character set to use. Default null.
        #// @param string      $table   The name of the table being checked.
        #// @param string      $column  The name of the column being checked.
        #//
        charset = apply_filters("pre_get_col_charset", None, table, column)
        if None != charset:
            return charset
        # end if
        #// Skip this entirely if this isn't a MySQL database.
        if php_empty(lambda : self.is_mysql):
            return False
        # end if
        if php_empty(lambda : self.table_charset[tablekey]):
            #// This primes column information for us.
            table_charset = self.get_table_charset(table)
            if is_wp_error(table_charset):
                return table_charset
            # end if
        # end if
        #// If still no column information, return the table charset.
        if php_empty(lambda : self.col_meta[tablekey]):
            return self.table_charset[tablekey]
        # end if
        #// If this column doesn't exist, return the table charset.
        if php_empty(lambda : self.col_meta[tablekey][columnkey]):
            return self.table_charset[tablekey]
        # end if
        #// Return false when it's not a string column.
        if php_empty(lambda : self.col_meta[tablekey][columnkey].Collation):
            return False
        # end if
        charset = php_explode("_", self.col_meta[tablekey][columnkey].Collation)
        return charset
    # end def get_col_charset
    #// 
    #// Retrieve the maximum string length allowed in a given column.
    #// The length may either be specified as a byte length or a character length.
    #// 
    #// @since 4.2.1
    #// 
    #// @param string $table  Table name.
    #// @param string $column Column name.
    #// @return array|false|WP_Error array( 'length' => (int), 'type' => 'byte' | 'char' )
    #// false if the column has no length (for example, numeric column)
    #// WP_Error object if there was an error.
    #//
    def get_col_length(self, table=None, column=None):
        
        tablekey = php_strtolower(table)
        columnkey = php_strtolower(column)
        #// Skip this entirely if this isn't a MySQL database.
        if php_empty(lambda : self.is_mysql):
            return False
        # end if
        if php_empty(lambda : self.col_meta[tablekey]):
            #// This primes column information for us.
            table_charset = self.get_table_charset(table)
            if is_wp_error(table_charset):
                return table_charset
            # end if
        # end if
        if php_empty(lambda : self.col_meta[tablekey][columnkey]):
            return False
        # end if
        typeinfo = php_explode("(", self.col_meta[tablekey][columnkey].Type)
        type = php_strtolower(typeinfo[0])
        if (not php_empty(lambda : typeinfo[1])):
            length = php_trim(typeinfo[1], ")")
        else:
            length = False
        # end if
        for case in Switch(type):
            if case("char"):
                pass
            # end if
            if case("varchar"):
                return Array({"type": "char", "length": php_int(length)})
            # end if
            if case("binary"):
                pass
            # end if
            if case("varbinary"):
                return Array({"type": "byte", "length": php_int(length)})
            # end if
            if case("tinyblob"):
                pass
            # end if
            if case("tinytext"):
                return Array({"type": "byte", "length": 255})
            # end if
            if case("blob"):
                pass
            # end if
            if case("text"):
                return Array({"type": "byte", "length": 65535})
            # end if
            if case("mediumblob"):
                pass
            # end if
            if case("mediumtext"):
                return Array({"type": "byte", "length": 16777215})
            # end if
            if case("longblob"):
                pass
            # end if
            if case("longtext"):
                return Array({"type": "byte", "length": 4294967295})
            # end if
            if case():
                return False
            # end if
        # end for
    # end def get_col_length
    #// 
    #// Check if a string is ASCII.
    #// 
    #// The negative regex is faster for non-ASCII strings, as it allows
    #// the search to finish as soon as it encounters a non-ASCII character.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $string String to check.
    #// @return bool True if ASCII, false if not.
    #//
    def check_ascii(self, string=None):
        
        if php_function_exists("mb_check_encoding"):
            if mb_check_encoding(string, "ASCII"):
                return True
            # end if
        elif (not php_preg_match("/[^\\x00-\\x7F]/", string)):
            return True
        # end if
        return False
    # end def check_ascii
    #// 
    #// Check if the query is accessing a collation considered safe on the current version of MySQL.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $query The query to check.
    #// @return bool True if the collation is safe, false if it isn't.
    #//
    def check_safe_collation(self, query=None):
        
        if self.checking_collation:
            return True
        # end if
        #// We don't need to check the collation for queries that don't read data.
        query = php_ltrim(query, "\r\n   (")
        if php_preg_match("/^(?:SHOW|DESCRIBE|DESC|EXPLAIN|CREATE)\\s/i", query):
            return True
        # end if
        #// All-ASCII queries don't need extra checking.
        if self.check_ascii(query):
            return True
        # end if
        table = self.get_table_from_query(query)
        if (not table):
            return False
        # end if
        self.checking_collation = True
        collation = self.get_table_charset(table)
        self.checking_collation = False
        #// Tables with no collation, or latin1 only, don't need extra checking.
        if False == collation or "latin1" == collation:
            return True
        # end if
        table = php_strtolower(table)
        if php_empty(lambda : self.col_meta[table]):
            return False
        # end if
        #// If any of the columns don't have one of these collations, it needs more sanity checking.
        for col in self.col_meta[table]:
            if php_empty(lambda : col.Collation):
                continue
            # end if
            if (not php_in_array(col.Collation, Array("utf8_general_ci", "utf8_bin", "utf8mb4_general_ci", "utf8mb4_bin"), True)):
                return False
            # end if
        # end for
        return True
    # end def check_safe_collation
    #// 
    #// Strips any invalid characters based on value/charset pairs.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array $data Array of value arrays. Each value array has the keys
    #// 'value' and 'charset'. An optional 'ascii' key can be
    #// set to false to avoid redundant ASCII checks.
    #// @return array|WP_Error The $data parameter, with invalid characters removed from
    #// each value. This works as a passthrough: any additional keys
    #// such as 'field' are retained in each value array. If we cannot
    #// remove invalid characters, a WP_Error object is returned.
    #//
    def strip_invalid_text(self, data=None):
        
        db_check_string = False
        for value in data:
            charset = value["charset"]
            if php_is_array(value["length"]):
                length = value["length"]["length"]
                truncate_by_byte_length = "byte" == value["length"]["type"]
            else:
                length = False
                #// 
                #// Since we have no length, we'll never truncate.
                #// Initialize the variable to false. true would take us
                #// through an unnecessary (for this case) codepath below.
                #//
                truncate_by_byte_length = False
            # end if
            #// There's no charset to work with.
            if False == charset:
                continue
            # end if
            #// Column isn't a string.
            if (not php_is_string(value["value"])):
                continue
            # end if
            needs_validation = True
            if "latin1" == charset or (not (php_isset(lambda : value["ascii"]))) and self.check_ascii(value["value"]):
                truncate_by_byte_length = True
                needs_validation = False
            # end if
            if truncate_by_byte_length:
                mbstring_binary_safe_encoding()
                if False != length and php_strlen(value["value"]) > length:
                    value["value"] = php_substr(value["value"], 0, length)
                # end if
                reset_mbstring_encoding()
                if (not needs_validation):
                    continue
                # end if
            # end if
            #// utf8 can be handled by regex, which is a bunch faster than a DB lookup.
            if "utf8" == charset or "utf8mb3" == charset or "utf8mb4" == charset and php_function_exists("mb_strlen"):
                regex = """/
                (
                (?: [\\x00-\\x7F]                  # single-byte sequences   0xxxxxxx
                |   [\\xC2-\\xDF][\\x80-\\xBF]       # double-byte sequences   110xxxxx 10xxxxxx
                |   \\xE0[\\xA0-\\xBF][\\x80-\\xBF]   # triple-byte sequences   1110xxxx 10xxxxxx * 2
                |   [\\xE1-\\xEC][\\x80-\\xBF]{2}
                |   \\xED[\\x80-\\x9F][\\x80-\\xBF]
                |   [\\xEE-\\xEF][\\x80-\\xBF]{2}"""
                if "utf8mb4" == charset:
                    regex += """
                    |    \\xF0[\\x90-\\xBF][\\x80-\\xBF]{2} # four-byte sequences   11110xxx 10xxxxxx * 3
                    |    [\\xF1-\\xF3][\\x80-\\xBF]{3}
                    |    \\xF4[\\x80-\\x8F][\\x80-\\xBF]{2}
                    """
                # end if
                regex += """){1,40}                          # ...one or more times
                )
                | .                                  # anything else
                /x"""
                value["value"] = php_preg_replace(regex, "$1", value["value"])
                if False != length and php_mb_strlen(value["value"], "UTF-8") > length:
                    value["value"] = php_mb_substr(value["value"], 0, length, "UTF-8")
                # end if
                continue
            # end if
            #// We couldn't use any local conversions, send it to the DB.
            value["db"] = True
            db_check_string = True
        # end for
        value = None
        #// Remove by reference.
        if db_check_string:
            queries = Array()
            for col,value in data:
                if (not php_empty(lambda : value["db"])):
                    #// We're going to need to truncate by characters or bytes, depending on the length value we have.
                    if (php_isset(lambda : value["length"]["type"])) and "byte" == value["length"]["type"]:
                        #// Using binary causes LEFT() to truncate by bytes.
                        charset = "binary"
                    else:
                        charset = value["charset"]
                    # end if
                    if self.charset:
                        connection_charset = self.charset
                    else:
                        if self.use_mysqli:
                            connection_charset = mysqli_character_set_name(self.dbh)
                        else:
                            connection_charset = mysql_client_encoding()
                        # end if
                    # end if
                    if php_is_array(value["length"]):
                        length = php_sprintf("%.0f", value["length"]["length"])
                        queries[col] = self.prepare(str("CONVERT( LEFT( CONVERT( %s USING ") + str(charset) + str(" ), ") + str(length) + str(" ) USING ") + str(connection_charset) + str(" )"), value["value"])
                    elif "binary" != charset:
                        #// If we don't have a length, there's no need to convert binary - it will always return the same result.
                        queries[col] = self.prepare(str("CONVERT( CONVERT( %s USING ") + str(charset) + str(" ) USING ") + str(connection_charset) + str(" )"), value["value"])
                    # end if
                    data[col]["db"] = None
                # end if
            # end for
            sql = Array()
            for column,query in queries:
                if (not query):
                    continue
                # end if
                sql[-1] = query + str(" AS x_") + str(column)
            # end for
            self.check_current_query = False
            row = self.get_row("SELECT " + php_implode(", ", sql), ARRAY_A)
            if (not row):
                return php_new_class("WP_Error", lambda : WP_Error("wpdb_strip_invalid_text_failure"))
            # end if
            for column in php_array_keys(data):
                if (php_isset(lambda : row[str("x_") + str(column)])):
                    data[column]["value"] = row[str("x_") + str(column)]
                # end if
            # end for
        # end if
        return data
    # end def strip_invalid_text
    #// 
    #// Strips any invalid characters from the query.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $query Query to convert.
    #// @return string|WP_Error The converted query, or a WP_Error object if the conversion fails.
    #//
    def strip_invalid_text_from_query(self, query=None):
        
        #// We don't need to check the collation for queries that don't read data.
        trimmed_query = php_ltrim(query, "\r\n   (")
        if php_preg_match("/^(?:SHOW|DESCRIBE|DESC|EXPLAIN|CREATE)\\s/i", trimmed_query):
            return query
        # end if
        table = self.get_table_from_query(query)
        if table:
            charset = self.get_table_charset(table)
            if is_wp_error(charset):
                return charset
            # end if
            #// We can't reliably strip text from tables containing binary/blob columns.
            if "binary" == charset:
                return query
            # end if
        else:
            charset = self.charset
        # end if
        data = Array({"value": query, "charset": charset, "ascii": False, "length": False})
        data = self.strip_invalid_text(Array(data))
        if is_wp_error(data):
            return data
        # end if
        return data[0]["value"]
    # end def strip_invalid_text_from_query
    #// 
    #// Strips any invalid characters from the string for a given table and column.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $table  Table name.
    #// @param string $column Column name.
    #// @param string $value  The text to check.
    #// @return string|WP_Error The converted string, or a WP_Error object if the conversion fails.
    #//
    def strip_invalid_text_for_column(self, table=None, column=None, value=None):
        
        if (not php_is_string(value)):
            return value
        # end if
        charset = self.get_col_charset(table, column)
        if (not charset):
            #// Not a string column.
            return value
        elif is_wp_error(charset):
            #// Bail on real errors.
            return charset
        # end if
        data = Array({column: Array({"value": value, "charset": charset, "length": self.get_col_length(table, column)})})
        data = self.strip_invalid_text(data)
        if is_wp_error(data):
            return data
        # end if
        return data[column]["value"]
    # end def strip_invalid_text_for_column
    #// 
    #// Find the first table name referenced in a query.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $query The query to search.
    #// @return string|false $table The table name found, or false if a table couldn't be found.
    #//
    def get_table_from_query(self, query=None):
        
        #// Remove characters that can legally trail the table name.
        query = php_rtrim(query, ";/-#")
        #// Allow (select...) union [...] style queries. Use the first query's table name.
        query = php_ltrim(query, "\r\n   (")
        #// Strip everything between parentheses except nested selects.
        query = php_preg_replace("/\\((?!\\s*select)[^(]*?\\)/is", "()", query)
        #// Quickly match most common queries.
        if php_preg_match("/^\\s*(?:" + "SELECT.*?\\s+FROM" + "|INSERT(?:\\s+LOW_PRIORITY|\\s+DELAYED|\\s+HIGH_PRIORITY)?(?:\\s+IGNORE)?(?:\\s+INTO)?" + "|REPLACE(?:\\s+LOW_PRIORITY|\\s+DELAYED)?(?:\\s+INTO)?" + "|UPDATE(?:\\s+LOW_PRIORITY)?(?:\\s+IGNORE)?" + "|DELETE(?:\\s+LOW_PRIORITY|\\s+QUICK|\\s+IGNORE)*(?:.+?FROM)?" + ")\\s+((?:[0-9a-zA-Z$_.`-]|[\\xC2-\\xDF][\\x80-\\xBF])+)/is", query, maybe):
            return php_str_replace("`", "", maybe[1])
        # end if
        #// SHOW TABLE STATUS and SHOW TABLES WHERE Name = 'wp_posts'
        if php_preg_match("/^\\s*SHOW\\s+(?:TABLE\\s+STATUS|(?:FULL\\s+)?TABLES).+WHERE\\s+Name\\s*=\\s*(\"|')((?:[0-9a-zA-Z$_.-]|[\\xC2-\\xDF][\\x80-\\xBF])+)\\1/is", query, maybe):
            return maybe[2]
        # end if
        #// 
        #// SHOW TABLE STATUS LIKE and SHOW TABLES LIKE 'wp\_123\_%'
        #// This quoted LIKE operand seldom holds a full table name.
        #// It is usually a pattern for matching a prefix so we just
        #// strip the trailing % and unescape the _ to get 'wp_123_'
        #// which drop-ins can use for routing these SQL statements.
        #//
        if php_preg_match("/^\\s*SHOW\\s+(?:TABLE\\s+STATUS|(?:FULL\\s+)?TABLES)\\s+(?:WHERE\\s+Name\\s+)?LIKE\\s*(\"|')((?:[\\\\0-9a-zA-Z$_.-]|[\\xC2-\\xDF][\\x80-\\xBF])+)%?\\1/is", query, maybe):
            return php_str_replace("\\_", "_", maybe[2])
        # end if
        #// Big pattern for the rest of the table-related queries.
        if php_preg_match("/^\\s*(?:" + "(?:EXPLAIN\\s+(?:EXTENDED\\s+)?)?SELECT.*?\\s+FROM" + "|DESCRIBE|DESC|EXPLAIN|HANDLER" + "|(?:LOCK|UNLOCK)\\s+TABLE(?:S)?" + "|(?:RENAME|OPTIMIZE|BACKUP|RESTORE|CHECK|CHECKSUM|ANALYZE|REPAIR).*\\s+TABLE" + "|TRUNCATE(?:\\s+TABLE)?" + "|CREATE(?:\\s+TEMPORARY)?\\s+TABLE(?:\\s+IF\\s+NOT\\s+EXISTS)?" + "|ALTER(?:\\s+IGNORE)?\\s+TABLE" + "|DROP\\s+TABLE(?:\\s+IF\\s+EXISTS)?" + "|CREATE(?:\\s+\\w+)?\\s+INDEX.*\\s+ON" + "|DROP\\s+INDEX.*\\s+ON" + "|LOAD\\s+DATA.*INFILE.*INTO\\s+TABLE" + "|(?:GRANT|REVOKE).*ON\\s+TABLE" + "|SHOW\\s+(?:.*FROM|.*TABLE)" + ")\\s+\\(*\\s*((?:[0-9a-zA-Z$_.`-]|[\\xC2-\\xDF][\\x80-\\xBF])+)\\s*\\)*/is", query, maybe):
            return php_str_replace("`", "", maybe[1])
        # end if
        return False
    # end def get_table_from_query
    #// 
    #// Load the column metadata from the last query.
    #// 
    #// @since 3.5.0
    #//
    def load_col_info(self):
        
        if self.col_info:
            return
        # end if
        if self.use_mysqli:
            num_fields = mysqli_num_fields(self.result)
            i = 0
            while i < num_fields:
                
                self.col_info[i] = mysqli_fetch_field(self.result)
                i += 1
            # end while
        else:
            num_fields = mysql_num_fields(self.result)
            i = 0
            while i < num_fields:
                
                self.col_info[i] = mysql_fetch_field(self.result, i)
                i += 1
            # end while
        # end if
    # end def load_col_info
    #// 
    #// Retrieve column metadata from the last query.
    #// 
    #// @since 0.71
    #// 
    #// @param string $info_type  Optional. Type one of name, table, def, max_length, not_null, primary_key, multiple_key, unique_key, numeric, blob, type, unsigned, zerofill
    #// @param int    $col_offset Optional. 0: col name. 1: which table the col's in. 2: col's max length. 3: if the col is numeric. 4: col's type
    #// @return mixed Column Results
    #//
    def get_col_info(self, info_type="name", col_offset=-1):
        
        self.load_col_info()
        if self.col_info:
            if -1 == col_offset:
                i = 0
                new_array = Array()
                for col in self.col_info:
                    new_array[i] = col.info_type
                    i += 1
                # end for
                return new_array
            else:
                return self.col_info[col_offset].info_type
            # end if
        # end if
    # end def get_col_info
    #// 
    #// Starts the timer, for debugging purposes.
    #// 
    #// @since 1.5.0
    #// 
    #// @return true
    #//
    def timer_start(self):
        
        self.time_start = php_microtime(True)
        return True
    # end def timer_start
    #// 
    #// Stops the debugging timer.
    #// 
    #// @since 1.5.0
    #// 
    #// @return float Total time spent on the query, in seconds.
    #//
    def timer_stop(self):
        
        return php_microtime(True) - self.time_start
    # end def timer_stop
    #// 
    #// Wraps errors in a nice header and footer and dies.
    #// 
    #// Will not die if wpdb::$show_errors is false.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $message    The error message.
    #// @param string $error_code Optional. A computer-readable string to identify the error.
    #// @return void|false Void if the showing of errors is enabled, false if disabled.
    #//
    def bail(self, message=None, error_code="500"):
        
        if self.show_errors:
            error = ""
            if self.use_mysqli:
                if type(self.dbh).__name__ == "mysqli":
                    error = mysqli_error(self.dbh)
                elif mysqli_connect_errno():
                    error = mysqli_connect_error()
                # end if
            else:
                if is_resource(self.dbh):
                    error = mysql_error(self.dbh)
                else:
                    error = mysql_error()
                # end if
            # end if
            if error:
                message = "<p><code>" + error + "</code></p>\n" + message
            # end if
            wp_die(message)
        else:
            if php_class_exists("WP_Error", False):
                self.error = php_new_class("WP_Error", lambda : WP_Error(error_code, message))
            else:
                self.error = message
            # end if
            return False
        # end if
    # end def bail
    #// 
    #// Closes the current database connection.
    #// 
    #// @since 4.5.0
    #// 
    #// @return bool True if the connection was successfully closed, false if it wasn't,
    #// or the connection doesn't exist.
    #//
    def close(self):
        
        if (not self.dbh):
            return False
        # end if
        if self.use_mysqli:
            closed = mysqli_close(self.dbh)
        else:
            closed = mysql_close(self.dbh)
        # end if
        if closed:
            self.dbh = None
            self.ready = False
            self.has_connected = False
        # end if
        return closed
    # end def close
    #// 
    #// Whether MySQL database is at least the required minimum version.
    #// 
    #// @since 2.5.0
    #// 
    #// @global string $wp_version             The WordPress version string.
    #// @global string $required_mysql_version The required MySQL version string.
    #// 
    #// @return void|WP_Error
    #//
    def check_database_version(self):
        
        global wp_version,required_mysql_version
        php_check_if_defined("wp_version","required_mysql_version")
        #// Make sure the server has the required MySQL version.
        if php_version_compare(self.db_version(), required_mysql_version, "<"):
            #// translators: 1: WordPress version number, 2: Minimum required MySQL version number.
            return php_new_class("WP_Error", lambda : WP_Error("database_version", php_sprintf(__("<strong>Error</strong>: WordPress %1$s requires MySQL %2$s or higher"), wp_version, required_mysql_version)))
        # end if
    # end def check_database_version
    #// 
    #// Whether the database supports collation.
    #// 
    #// Called when WordPress is generating the table scheme.
    #// 
    #// Use `wpdb::has_cap( 'collation' )`.
    #// 
    #// @since 2.5.0
    #// @deprecated 3.5.0 Use wpdb::has_cap()
    #// 
    #// @return bool True if collation is supported, false if version does not
    #//
    def supports_collation(self):
        
        _deprecated_function(__FUNCTION__, "3.5.0", "wpdb::has_cap( 'collation' )")
        return self.has_cap("collation")
    # end def supports_collation
    #// 
    #// The database character collate.
    #// 
    #// @since 3.5.0
    #// 
    #// @return string The database character collate.
    #//
    def get_charset_collate(self):
        
        charset_collate = ""
        if (not php_empty(lambda : self.charset)):
            charset_collate = str("DEFAULT CHARACTER SET ") + str(self.charset)
        # end if
        if (not php_empty(lambda : self.collate)):
            charset_collate += str(" COLLATE ") + str(self.collate)
        # end if
        return charset_collate
    # end def get_charset_collate
    #// 
    #// Determine if a database supports a particular feature.
    #// 
    #// @since 2.7.0
    #// @since 4.1.0 Added support for the 'utf8mb4' feature.
    #// @since 4.6.0 Added support for the 'utf8mb4_520' feature.
    #// 
    #// @see wpdb::db_version()
    #// 
    #// @param string $db_cap The feature to check for. Accepts 'collation',
    #// 'group_concat', 'subqueries', 'set_charset',
    #// 'utf8mb4', or 'utf8mb4_520'.
    #// @return int|false Whether the database feature is supported, false otherwise.
    #//
    def has_cap(self, db_cap=None):
        
        version = self.db_version()
        for case in Switch(php_strtolower(db_cap)):
            if case("collation"):
                pass
            # end if
            if case("group_concat"):
                pass
            # end if
            if case("subqueries"):
                #// @since 2.7.0
                return php_version_compare(version, "4.1", ">=")
            # end if
            if case("set_charset"):
                return php_version_compare(version, "5.0.7", ">=")
            # end if
            if case("utf8mb4"):
                #// @since 4.1.0
                if php_version_compare(version, "5.5.3", "<"):
                    return False
                # end if
                if self.use_mysqli:
                    client_version = mysqli_get_client_info()
                else:
                    client_version = mysql_get_client_info()
                # end if
                #// 
                #// libmysql has supported utf8mb4 since 5.5.3, same as the MySQL server.
                #// mysqlnd has supported utf8mb4 since 5.0.9.
                #//
                if False != php_strpos(client_version, "mysqlnd"):
                    client_version = php_preg_replace("/^\\D+([\\d.]+).*/", "$1", client_version)
                    return php_version_compare(client_version, "5.0.9", ">=")
                else:
                    return php_version_compare(client_version, "5.5.3", ">=")
                # end if
            # end if
            if case("utf8mb4_520"):
                #// @since 4.6.0
                return php_version_compare(version, "5.6", ">=")
            # end if
        # end for
        return False
    # end def has_cap
    #// 
    #// Retrieve the name of the function that called wpdb.
    #// 
    #// Searches up the list of functions until it reaches
    #// the one that would most logically had called this method.
    #// 
    #// @since 2.5.0
    #// 
    #// @return string Comma separated list of the calling functions.
    #//
    def get_caller(self):
        
        return wp_debug_backtrace_summary(__CLASS__)
    # end def get_caller
    #// 
    #// Retrieves the MySQL server version.
    #// 
    #// @since 2.7.0
    #// 
    #// @return null|string Null on failure, version number on success.
    #//
    def db_version(self):
        
        if self.use_mysqli:
            server_info = mysqli_get_server_info(self.dbh)
        else:
            server_info = mysql_get_server_info(self.dbh)
        # end if
        return php_preg_replace("/[^0-9.].*/", "", server_info)
    # end def db_version
# end class wpdb
