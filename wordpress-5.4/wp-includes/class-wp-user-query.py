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
#// User API: WP_User_Query class
#// 
#// @package WordPress
#// @subpackage Users
#// @since 4.4.0
#// 
#// 
#// Core class used for querying users.
#// 
#// @since 3.1.0
#// 
#// @see WP_User_Query::prepare_query() for information on accepted arguments.
#//
class WP_User_Query():
    query_vars = Array()
    results = Array()
    total_users = 0
    meta_query = False
    request = Array()
    compat_fields = Array("results", "total_users")
    query_fields = Array()
    query_from = Array()
    query_where = Array()
    query_orderby = Array()
    query_limit = Array()
    #// 
    #// PHP5 constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @param null|string|array $query Optional. The query variables.
    #//
    def __init__(self, query=None):
        
        if (not php_empty(lambda : query)):
            self.prepare_query(query)
            self.query()
        # end if
    # end def __init__
    #// 
    #// Fills in missing query variables with default values.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $args Query vars, as passed to `WP_User_Query`.
    #// @return array Complete query variables with undefined ones filled in with defaults.
    #//
    @classmethod
    def fill_query_vars(self, args=None):
        
        defaults = Array({"blog_id": get_current_blog_id(), "role": "", "role__in": Array(), "role__not_in": Array(), "meta_key": "", "meta_value": "", "meta_compare": "", "include": Array(), "exclude": Array(), "search": "", "search_columns": Array(), "orderby": "login", "order": "ASC", "offset": "", "number": "", "paged": 1, "count_total": True, "fields": "all", "who": "", "has_published_posts": None, "nicename": "", "nicename__in": Array(), "nicename__not_in": Array(), "login": "", "login__in": Array(), "login__not_in": Array()})
        return wp_parse_args(args, defaults)
    # end def fill_query_vars
    #// 
    #// Prepare the query variables.
    #// 
    #// @since 3.1.0
    #// @since 4.1.0 Added the ability to order by the `include` value.
    #// @since 4.2.0 Added 'meta_value_num' support for `$orderby` parameter. Added multi-dimensional array syntax
    #// for `$orderby` parameter.
    #// @since 4.3.0 Added 'has_published_posts' parameter.
    #// @since 4.4.0 Added 'paged', 'role__in', and 'role__not_in' parameters. The 'role' parameter was updated to
    #// permit an array or comma-separated list of values. The 'number' parameter was updated to support
    #// querying for all users with using -1.
    #// @since 4.7.0 Added 'nicename', 'nicename__in', 'nicename__not_in', 'login', 'login__in',
    #// and 'login__not_in' parameters.
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// @global int  $blog_id
    #// 
    #// @param string|array $query {
    #// Optional. Array or string of Query parameters.
    #// 
    #// @type int          $blog_id             The site ID. Default is the current site.
    #// @type string|array $role                An array or a comma-separated list of role names that users must match
    #// to be included in results. Note that this is an inclusive list: users
    #// must match *each* role. Default empty.
    #// @type array        $role__in            An array of role names. Matched users must have at least one of these
    #// roles. Default empty array.
    #// @type array        $role__not_in        An array of role names to exclude. Users matching one or more of these
    #// roles will not be included in results. Default empty array.
    #// @type string       $meta_key            User meta key. Default empty.
    #// @type string       $meta_value          User meta value. Default empty.
    #// @type string       $meta_compare        Comparison operator to test the `$meta_value`. Accepts '=', '!=',
    #// '>', '>=', '<', '<=', 'LIKE', 'NOT LIKE', 'IN', 'NOT IN',
    #// 'BETWEEN', 'NOT BETWEEN', 'EXISTS', 'NOT EXISTS', 'REGEXP',
    #// 'NOT REGEXP', or 'RLIKE'. Default '='.
    #// @type array        $include             An array of user IDs to include. Default empty array.
    #// @type array        $exclude             An array of user IDs to exclude. Default empty array.
    #// @type string       $search              Search keyword. Searches for possible string matches on columns.
    #// When `$search_columns` is left empty, it tries to determine which
    #// column to search in based on search string. Default empty.
    #// @type array        $search_columns      Array of column names to be searched. Accepts 'ID', 'user_login',
    #// 'user_email', 'user_url', 'user_nicename', 'display_name'.
    #// Default empty array.
    #// @type string|array $orderby             Field(s) to sort the retrieved users by. May be a single value,
    #// an array of values, or a multi-dimensional array with fields as
    #// keys and orders ('ASC' or 'DESC') as values. Accepted values are
    #// 'ID', 'display_name' (or 'name'), 'include', 'user_login'
    #// (or 'login'), 'login__in', 'user_nicename' (or 'nicename'),
    #// 'nicename__in', 'user_email (or 'email'), 'user_url' (or 'url'),
    #// 'user_registered' (or 'registered'), 'post_count', 'meta_value',
    #// 'meta_value_num', the value of `$meta_key`, or an array key of
    #// `$meta_query`. To use 'meta_value' or 'meta_value_num', `$meta_key`
    #// must be also be defined. Default 'user_login'.
    #// @type string       $order               Designates ascending or descending order of users. Order values
    #// passed as part of an `$orderby` array take precedence over this
    #// parameter. Accepts 'ASC', 'DESC'. Default 'ASC'.
    #// @type int          $offset              Number of users to offset in retrieved results. Can be used in
    #// conjunction with pagination. Default 0.
    #// @type int          $number              Number of users to limit the query for. Can be used in
    #// conjunction with pagination. Value -1 (all) is supported, but
    #// should be used with caution on larger sites.
    #// Default -1 (all users).
    #// @type int          $paged               When used with number, defines the page of results to return.
    #// Default 1.
    #// @type bool         $count_total         Whether to count the total number of users found. If pagination
    #// is not needed, setting this to false can improve performance.
    #// Default true.
    #// @type string|array $fields              Which fields to return. Single or all fields (string), or array
    #// of fields. Accepts 'ID', 'display_name', 'user_login',
    #// 'user_nicename', 'user_email', 'user_url', 'user_registered'.
    #// Use 'all' for all fields and 'all_with_meta' to include
    #// meta fields. Default 'all'.
    #// @type string       $who                 Type of users to query. Accepts 'authors'.
    #// Default empty (all users).
    #// @type bool|array   $has_published_posts Pass an array of post types to filter results to users who have
    #// published posts in those post types. `true` is an alias for all
    #// public post types.
    #// @type string       $nicename            The user nicename. Default empty.
    #// @type array        $nicename__in        An array of nicenames to include. Users matching one of these
    #// nicenames will be included in results. Default empty array.
    #// @type array        $nicename__not_in    An array of nicenames to exclude. Users matching one of these
    #// nicenames will not be included in results. Default empty array.
    #// @type string       $login               The user login. Default empty.
    #// @type array        $login__in           An array of logins to include. Users matching one of these
    #// logins will be included in results. Default empty array.
    #// @type array        $login__not_in       An array of logins to exclude. Users matching one of these
    #// logins will not be included in results. Default empty array.
    #// }
    #//
    def prepare_query(self, query=Array()):
        
        global wpdb
        php_check_if_defined("wpdb")
        if php_empty(lambda : self.query_vars) or (not php_empty(lambda : query)):
            self.query_limit = None
            self.query_vars = self.fill_query_vars(query)
        # end if
        #// 
        #// Fires before the WP_User_Query has been parsed.
        #// 
        #// The passed WP_User_Query object contains the query variables, not
        #// yet passed into SQL.
        #// 
        #// @since 4.0.0
        #// 
        #// @param WP_User_Query $this The current WP_User_Query instance,
        #// passed by reference.
        #//
        do_action("pre_get_users", self)
        #// Ensure that query vars are filled after 'pre_get_users'.
        qv = self.query_vars
        qv = self.fill_query_vars(qv)
        if php_is_array(qv["fields"]):
            qv["fields"] = array_unique(qv["fields"])
            self.query_fields = Array()
            for field in qv["fields"]:
                field = "ID" if "ID" == field else sanitize_key(field)
                self.query_fields[-1] = str(wpdb.users) + str(".") + str(field)
            # end for
            self.query_fields = php_implode(",", self.query_fields)
        elif "all" == qv["fields"]:
            self.query_fields = str(wpdb.users) + str(".*")
        else:
            self.query_fields = str(wpdb.users) + str(".ID")
        # end if
        if (php_isset(lambda : qv["count_total"])) and qv["count_total"]:
            self.query_fields = "SQL_CALC_FOUND_ROWS " + self.query_fields
        # end if
        self.query_from = str("FROM ") + str(wpdb.users)
        self.query_where = "WHERE 1=1"
        #// Parse and sanitize 'include', for use by 'orderby' as well as 'include' below.
        if (not php_empty(lambda : qv["include"])):
            include = wp_parse_id_list(qv["include"])
        else:
            include = False
        # end if
        blog_id = 0
        if (php_isset(lambda : qv["blog_id"])):
            blog_id = absint(qv["blog_id"])
        # end if
        if qv["has_published_posts"] and blog_id:
            if True == qv["has_published_posts"]:
                post_types = get_post_types(Array({"public": True}))
            else:
                post_types = qv["has_published_posts"]
            # end if
            for post_type in post_types:
                post_type = wpdb.prepare("%s", post_type)
            # end for
            posts_table = wpdb.get_blog_prefix(blog_id) + "posts"
            self.query_where += str(" AND ") + str(wpdb.users) + str(".ID IN ( SELECT DISTINCT ") + str(posts_table) + str(".post_author FROM ") + str(posts_table) + str(" WHERE ") + str(posts_table) + str(".post_status = 'publish' AND ") + str(posts_table) + str(".post_type IN ( ") + join(", ", post_types) + " ) )"
        # end if
        #// nicename
        if "" != qv["nicename"]:
            self.query_where += wpdb.prepare(" AND user_nicename = %s", qv["nicename"])
        # end if
        if (not php_empty(lambda : qv["nicename__in"])):
            sanitized_nicename__in = php_array_map("esc_sql", qv["nicename__in"])
            nicename__in = php_implode("','", sanitized_nicename__in)
            self.query_where += str(" AND user_nicename IN ( '") + str(nicename__in) + str("' )")
        # end if
        if (not php_empty(lambda : qv["nicename__not_in"])):
            sanitized_nicename__not_in = php_array_map("esc_sql", qv["nicename__not_in"])
            nicename__not_in = php_implode("','", sanitized_nicename__not_in)
            self.query_where += str(" AND user_nicename NOT IN ( '") + str(nicename__not_in) + str("' )")
        # end if
        #// login
        if "" != qv["login"]:
            self.query_where += wpdb.prepare(" AND user_login = %s", qv["login"])
        # end if
        if (not php_empty(lambda : qv["login__in"])):
            sanitized_login__in = php_array_map("esc_sql", qv["login__in"])
            login__in = php_implode("','", sanitized_login__in)
            self.query_where += str(" AND user_login IN ( '") + str(login__in) + str("' )")
        # end if
        if (not php_empty(lambda : qv["login__not_in"])):
            sanitized_login__not_in = php_array_map("esc_sql", qv["login__not_in"])
            login__not_in = php_implode("','", sanitized_login__not_in)
            self.query_where += str(" AND user_login NOT IN ( '") + str(login__not_in) + str("' )")
        # end if
        #// Meta query.
        self.meta_query = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query())
        self.meta_query.parse_query_vars(qv)
        if (php_isset(lambda : qv["who"])) and "authors" == qv["who"] and blog_id:
            who_query = Array({"key": wpdb.get_blog_prefix(blog_id) + "user_level", "value": 0, "compare": "!="})
            #// Prevent extra meta query.
            qv["blog_id"] = 0
            blog_id = 0
            if php_empty(lambda : self.meta_query.queries):
                self.meta_query.queries = Array(who_query)
            else:
                #// Append the cap query to the original queries and reparse the query.
                self.meta_query.queries = Array({"relation": "AND"}, Array(self.meta_query.queries, who_query))
            # end if
            self.meta_query.parse_query_vars(self.meta_query.queries)
        # end if
        roles = Array()
        if (php_isset(lambda : qv["role"])):
            if php_is_array(qv["role"]):
                roles = qv["role"]
            elif php_is_string(qv["role"]) and (not php_empty(lambda : qv["role"])):
                roles = php_array_map("trim", php_explode(",", qv["role"]))
            # end if
        # end if
        role__in = Array()
        if (php_isset(lambda : qv["role__in"])):
            role__in = qv["role__in"]
        # end if
        role__not_in = Array()
        if (php_isset(lambda : qv["role__not_in"])):
            role__not_in = qv["role__not_in"]
        # end if
        if blog_id and (not php_empty(lambda : roles)) or (not php_empty(lambda : role__in)) or (not php_empty(lambda : role__not_in)) or is_multisite():
            role_queries = Array()
            roles_clauses = Array({"relation": "AND"})
            if (not php_empty(lambda : roles)):
                for role in roles:
                    roles_clauses[-1] = Array({"key": wpdb.get_blog_prefix(blog_id) + "capabilities", "value": "\"" + role + "\"", "compare": "LIKE"})
                # end for
                role_queries[-1] = roles_clauses
            # end if
            role__in_clauses = Array({"relation": "OR"})
            if (not php_empty(lambda : role__in)):
                for role in role__in:
                    role__in_clauses[-1] = Array({"key": wpdb.get_blog_prefix(blog_id) + "capabilities", "value": "\"" + role + "\"", "compare": "LIKE"})
                # end for
                role_queries[-1] = role__in_clauses
            # end if
            role__not_in_clauses = Array({"relation": "AND"})
            if (not php_empty(lambda : role__not_in)):
                for role in role__not_in:
                    role__not_in_clauses[-1] = Array({"key": wpdb.get_blog_prefix(blog_id) + "capabilities", "value": "\"" + role + "\"", "compare": "NOT LIKE"})
                # end for
                role_queries[-1] = role__not_in_clauses
            # end if
            #// If there are no specific roles named, make sure the user is a member of the site.
            if php_empty(lambda : role_queries):
                role_queries[-1] = Array({"key": wpdb.get_blog_prefix(blog_id) + "capabilities", "compare": "EXISTS"})
            # end if
            #// Specify that role queries should be joined with AND.
            role_queries["relation"] = "AND"
            if php_empty(lambda : self.meta_query.queries):
                self.meta_query.queries = role_queries
            else:
                #// Append the cap query to the original queries and reparse the query.
                self.meta_query.queries = Array({"relation": "AND"}, Array(self.meta_query.queries, role_queries))
            # end if
            self.meta_query.parse_query_vars(self.meta_query.queries)
        # end if
        if (not php_empty(lambda : self.meta_query.queries)):
            clauses = self.meta_query.get_sql("user", wpdb.users, "ID", self)
            self.query_from += clauses["join"]
            self.query_where += clauses["where"]
            if self.meta_query.has_or_relation():
                self.query_fields = "DISTINCT " + self.query_fields
            # end if
        # end if
        #// Sorting.
        qv["order"] = php_strtoupper(qv["order"]) if (php_isset(lambda : qv["order"])) else ""
        order = self.parse_order(qv["order"])
        if php_empty(lambda : qv["orderby"]):
            #// Default order is by 'user_login'.
            ordersby = Array({"user_login": order})
        elif php_is_array(qv["orderby"]):
            ordersby = qv["orderby"]
        else:
            #// 'orderby' values may be a comma- or space-separated list.
            ordersby = php_preg_split("/[,\\s]+/", qv["orderby"])
        # end if
        orderby_array = Array()
        for _key,_value in ordersby:
            if (not _value):
                continue
            # end if
            if php_is_int(_key):
                #// Integer key means this is a flat array of 'orderby' fields.
                _orderby = _value
                _order = order
            else:
                #// Non-integer key means this the key is the field and the value is ASC/DESC.
                _orderby = _key
                _order = _value
            # end if
            parsed = self.parse_orderby(_orderby)
            if (not parsed):
                continue
            # end if
            if "nicename__in" == _orderby or "login__in" == _orderby:
                orderby_array[-1] = parsed
            else:
                orderby_array[-1] = parsed + " " + self.parse_order(_order)
            # end if
        # end for
        #// If no valid clauses were found, order by user_login.
        if php_empty(lambda : orderby_array):
            orderby_array[-1] = str("user_login ") + str(order)
        # end if
        self.query_orderby = "ORDER BY " + php_implode(", ", orderby_array)
        #// Limit.
        if (php_isset(lambda : qv["number"])) and qv["number"] > 0:
            if qv["offset"]:
                self.query_limit = wpdb.prepare("LIMIT %d, %d", qv["offset"], qv["number"])
            else:
                self.query_limit = wpdb.prepare("LIMIT %d, %d", qv["number"] * qv["paged"] - 1, qv["number"])
            # end if
        # end if
        search = ""
        if (php_isset(lambda : qv["search"])):
            search = php_trim(qv["search"])
        # end if
        if search:
            leading_wild = php_ltrim(search, "*") != search
            trailing_wild = php_rtrim(search, "*") != search
            if leading_wild and trailing_wild:
                wild = "both"
            elif leading_wild:
                wild = "leading"
            elif trailing_wild:
                wild = "trailing"
            else:
                wild = False
            # end if
            if wild:
                search = php_trim(search, "*")
            # end if
            search_columns = Array()
            if qv["search_columns"]:
                search_columns = php_array_intersect(qv["search_columns"], Array("ID", "user_login", "user_email", "user_url", "user_nicename", "display_name"))
            # end if
            if (not search_columns):
                if False != php_strpos(search, "@"):
                    search_columns = Array("user_email")
                elif php_is_numeric(search):
                    search_columns = Array("user_login", "ID")
                elif php_preg_match("|^https?://|", search) and (not is_multisite() and wp_is_large_network("users")):
                    search_columns = Array("user_url")
                else:
                    search_columns = Array("user_login", "user_url", "user_email", "user_nicename", "display_name")
                # end if
            # end if
            #// 
            #// Filters the columns to search in a WP_User_Query search.
            #// 
            #// The default columns depend on the search term, and include 'ID', 'user_login',
            #// 'user_email', 'user_url', 'user_nicename', and 'display_name'.
            #// 
            #// @since 3.6.0
            #// 
            #// @param string[]      $search_columns Array of column names to be searched.
            #// @param string        $search         Text being searched.
            #// @param WP_User_Query $this           The current WP_User_Query instance.
            #//
            search_columns = apply_filters("user_search_columns", search_columns, search, self)
            self.query_where += self.get_search_sql(search, search_columns, wild)
        # end if
        if (not php_empty(lambda : include)):
            #// Sanitized earlier.
            ids = php_implode(",", include)
            self.query_where += str(" AND ") + str(wpdb.users) + str(".ID IN (") + str(ids) + str(")")
        elif (not php_empty(lambda : qv["exclude"])):
            ids = php_implode(",", wp_parse_id_list(qv["exclude"]))
            self.query_where += str(" AND ") + str(wpdb.users) + str(".ID NOT IN (") + str(ids) + str(")")
        # end if
        #// Date queries are allowed for the user_registered field.
        if (not php_empty(lambda : qv["date_query"])) and php_is_array(qv["date_query"]):
            date_query = php_new_class("WP_Date_Query", lambda : WP_Date_Query(qv["date_query"], "user_registered"))
            self.query_where += date_query.get_sql()
        # end if
        #// 
        #// Fires after the WP_User_Query has been parsed, and before
        #// the query is executed.
        #// 
        #// The passed WP_User_Query object contains SQL parts formed
        #// from parsing the given query.
        #// 
        #// @since 3.1.0
        #// 
        #// @param WP_User_Query $this The current WP_User_Query instance,
        #// passed by reference.
        #//
        do_action_ref_array("pre_user_query", Array(self))
    # end def prepare_query
    #// 
    #// Execute the query, with the current variables.
    #// 
    #// @since 3.1.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #//
    def query(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        qv = self.query_vars
        #// 
        #// Filters the users array before the query takes place.
        #// 
        #// Return a non-null value to bypass WordPress's default user queries.
        #// Filtering functions that require pagination information are encouraged to set
        #// the `total_users` property of the WP_User_Query object, passed to the filter
        #// by reference. If WP_User_Query does not perform a database query, it will not
        #// have enough information to generate these values itself.
        #// 
        #// @since 5.1.0
        #// 
        #// @param array|null $results Return an array of user data to short-circuit WP's user query
        #// or null to allow WP to run its normal queries.
        #// @param WP_User_Query $this The WP_User_Query instance (passed by reference).
        #//
        self.results = apply_filters_ref_array("users_pre_query", Array(None, self))
        if None == self.results:
            self.request = str("SELECT ") + str(self.query_fields) + str(" ") + str(self.query_from) + str(" ") + str(self.query_where) + str(" ") + str(self.query_orderby) + str(" ") + str(self.query_limit)
            if php_is_array(qv["fields"]) or "all" == qv["fields"]:
                self.results = wpdb.get_results(self.request)
            else:
                self.results = wpdb.get_col(self.request)
            # end if
            if (php_isset(lambda : qv["count_total"])) and qv["count_total"]:
                #// 
                #// Filters SELECT FOUND_ROWS() query for the current WP_User_Query instance.
                #// 
                #// @since 3.2.0
                #// @since 5.1.0 Added the `$this` parameter.
                #// 
                #// @global wpdb $wpdb WordPress database abstraction object.
                #// 
                #// @param string $sql         The SELECT FOUND_ROWS() query for the current WP_User_Query.
                #// @param WP_User_Query $this The current WP_User_Query instance.
                #//
                found_users_query = apply_filters("found_users_query", "SELECT FOUND_ROWS()", self)
                self.total_users = int(wpdb.get_var(found_users_query))
            # end if
        # end if
        if (not self.results):
            return
        # end if
        if "all_with_meta" == qv["fields"]:
            cache_users(self.results)
            r = Array()
            for userid in self.results:
                r[userid] = php_new_class("WP_User", lambda : WP_User(userid, "", qv["blog_id"]))
            # end for
            self.results = r
        elif "all" == qv["fields"]:
            for key,user in self.results:
                self.results[key] = php_new_class("WP_User", lambda : WP_User(user, "", qv["blog_id"]))
            # end for
        # end if
    # end def query
    #// 
    #// Retrieve query variable.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $query_var Query variable key.
    #// @return mixed
    #//
    def get(self, query_var=None):
        
        if (php_isset(lambda : self.query_vars[query_var])):
            return self.query_vars[query_var]
        # end if
        return None
    # end def get
    #// 
    #// Set query variable.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $query_var Query variable key.
    #// @param mixed $value Query variable value.
    #//
    def set(self, query_var=None, value=None):
        
        self.query_vars[query_var] = value
    # end def set
    #// 
    #// Used internally to generate an SQL string for searching across multiple columns
    #// 
    #// @since 3.1.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $string
    #// @param array  $cols
    #// @param bool   $wild   Whether to allow wildcard searches. Default is false for Network Admin, true for single site.
    #// Single site allows leading and trailing wildcards, Network Admin only trailing.
    #// @return string
    #//
    def get_search_sql(self, string=None, cols=None, wild=False):
        
        global wpdb
        php_check_if_defined("wpdb")
        searches = Array()
        leading_wild = "%" if "leading" == wild or "both" == wild else ""
        trailing_wild = "%" if "trailing" == wild or "both" == wild else ""
        like = leading_wild + wpdb.esc_like(string) + trailing_wild
        for col in cols:
            if "ID" == col:
                searches[-1] = wpdb.prepare(str(col) + str(" = %s"), string)
            else:
                searches[-1] = wpdb.prepare(str(col) + str(" LIKE %s"), like)
            # end if
        # end for
        return " AND (" + php_implode(" OR ", searches) + ")"
    # end def get_search_sql
    #// 
    #// Return the list of users.
    #// 
    #// @since 3.1.0
    #// 
    #// @return array Array of results.
    #//
    def get_results(self):
        
        return self.results
    # end def get_results
    #// 
    #// Return the total number of users for the current query.
    #// 
    #// @since 3.1.0
    #// 
    #// @return int Number of total users.
    #//
    def get_total(self):
        
        return self.total_users
    # end def get_total
    #// 
    #// Parse and sanitize 'orderby' keys passed to the user query.
    #// 
    #// @since 4.2.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $orderby Alias for the field to order by.
    #// @return string Value to used in the ORDER clause, if `$orderby` is valid.
    #//
    def parse_orderby(self, orderby=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        meta_query_clauses = self.meta_query.get_clauses()
        _orderby = ""
        if php_in_array(orderby, Array("login", "nicename", "email", "url", "registered")):
            _orderby = "user_" + orderby
        elif php_in_array(orderby, Array("user_login", "user_nicename", "user_email", "user_url", "user_registered")):
            _orderby = orderby
        elif "name" == orderby or "display_name" == orderby:
            _orderby = "display_name"
        elif "post_count" == orderby:
            #// @todo Avoid the JOIN.
            where = get_posts_by_author_sql("post")
            self.query_from += str(" LEFT OUTER JOIN (\n                SELECT post_author, COUNT(*) as post_count\n                FROM ") + str(wpdb.posts) + str("\n             ") + str(where) + str("\n               GROUP BY post_author\n          ) p ON (") + str(wpdb.users) + str(".ID = p.post_author)\n          ")
            _orderby = "post_count"
        elif "ID" == orderby or "id" == orderby:
            _orderby = "ID"
        elif "meta_value" == orderby or self.get("meta_key") == orderby:
            _orderby = str(wpdb.usermeta) + str(".meta_value")
        elif "meta_value_num" == orderby:
            _orderby = str(wpdb.usermeta) + str(".meta_value+0")
        elif "include" == orderby and (not php_empty(lambda : self.query_vars["include"])):
            include = wp_parse_id_list(self.query_vars["include"])
            include_sql = php_implode(",", include)
            _orderby = str("FIELD( ") + str(wpdb.users) + str(".ID, ") + str(include_sql) + str(" )")
        elif "nicename__in" == orderby:
            sanitized_nicename__in = php_array_map("esc_sql", self.query_vars["nicename__in"])
            nicename__in = php_implode("','", sanitized_nicename__in)
            _orderby = str("FIELD( user_nicename, '") + str(nicename__in) + str("' )")
        elif "login__in" == orderby:
            sanitized_login__in = php_array_map("esc_sql", self.query_vars["login__in"])
            login__in = php_implode("','", sanitized_login__in)
            _orderby = str("FIELD( user_login, '") + str(login__in) + str("' )")
        elif (php_isset(lambda : meta_query_clauses[orderby])):
            meta_clause = meta_query_clauses[orderby]
            _orderby = php_sprintf("CAST(%s.meta_value AS %s)", esc_sql(meta_clause["alias"]), esc_sql(meta_clause["cast"]))
        # end if
        return _orderby
    # end def parse_orderby
    #// 
    #// Parse an 'order' query variable and cast it to ASC or DESC as necessary.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $order The 'order' query variable.
    #// @return string The sanitized 'order' query variable.
    #//
    def parse_order(self, order=None):
        
        if (not php_is_string(order)) or php_empty(lambda : order):
            return "DESC"
        # end if
        if "ASC" == php_strtoupper(order):
            return "ASC"
        else:
            return "DESC"
        # end if
    # end def parse_order
    #// 
    #// Make private properties readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to get.
    #// @return mixed Property.
    #//
    def __get(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return self.name
        # end if
    # end def __get
    #// 
    #// Make private properties settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name  Property to check if set.
    #// @param mixed  $value Property value.
    #// @return mixed Newly-set property.
    #//
    def __set(self, name=None, value=None):
        
        if php_in_array(name, self.compat_fields):
            self.name = value
            return self.name
        # end if
    # end def __set
    #// 
    #// Make private properties checkable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to check if set.
    #// @return bool Whether the property is set.
    #//
    def __isset(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return (php_isset(lambda : self.name))
        # end if
    # end def __isset
    #// 
    #// Make private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            self.name = None
        # end if
    # end def __unset
    #// 
    #// Make private/protected methods readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string   $name      Method to call.
    #// @param array    $arguments Arguments to pass when calling.
    #// @return mixed Return value of the callback, false otherwise.
    #//
    def __call(self, name=None, arguments=None):
        
        if "get_search_sql" == name:
            return self.get_search_sql(arguments)
        # end if
        return False
    # end def __call
# end class WP_User_Query
