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
    #// 
    #// Query vars, after parsing
    #// 
    #// @since 3.5.0
    #// @var array
    #//
    query_vars = Array()
    #// 
    #// List of found user ids
    #// 
    #// @since 3.1.0
    #// @var array
    #//
    results = Array()
    #// 
    #// Total number of found users for the current query
    #// 
    #// @since 3.1.0
    #// @var int
    #//
    total_users = 0
    #// 
    #// Metadata query container.
    #// 
    #// @since 4.2.0
    #// @var WP_Meta_Query
    #//
    meta_query = False
    #// 
    #// The SQL query used to fetch matching users.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    request = Array()
    compat_fields = Array("results", "total_users")
    #// SQL clauses.
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
    def __init__(self, query_=None):
        if query_ is None:
            query_ = None
        # end if
        
        if (not php_empty(lambda : query_)):
            self.prepare_query(query_)
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
    def fill_query_vars(self, args_=None):
        
        
        defaults_ = Array({"blog_id": get_current_blog_id(), "role": "", "role__in": Array(), "role__not_in": Array(), "meta_key": "", "meta_value": "", "meta_compare": "", "include": Array(), "exclude": Array(), "search": "", "search_columns": Array(), "orderby": "login", "order": "ASC", "offset": "", "number": "", "paged": 1, "count_total": True, "fields": "all", "who": "", "has_published_posts": None, "nicename": "", "nicename__in": Array(), "nicename__not_in": Array(), "login": "", "login__in": Array(), "login__not_in": Array()})
        return wp_parse_args(args_, defaults_)
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
    def prepare_query(self, query_=None):
        if query_ is None:
            query_ = Array()
        # end if
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if php_empty(lambda : self.query_vars) or (not php_empty(lambda : query_)):
            self.query_limit = None
            self.query_vars = self.fill_query_vars(query_)
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
        qv_ = self.query_vars
        qv_ = self.fill_query_vars(qv_)
        if php_is_array(qv_["fields"]):
            qv_["fields"] = array_unique(qv_["fields"])
            self.query_fields = Array()
            for field_ in qv_["fields"]:
                field_ = "ID" if "ID" == field_ else sanitize_key(field_)
                self.query_fields[-1] = str(wpdb_.users) + str(".") + str(field_)
            # end for
            self.query_fields = php_implode(",", self.query_fields)
        elif "all" == qv_["fields"]:
            self.query_fields = str(wpdb_.users) + str(".*")
        else:
            self.query_fields = str(wpdb_.users) + str(".ID")
        # end if
        if (php_isset(lambda : qv_["count_total"])) and qv_["count_total"]:
            self.query_fields = "SQL_CALC_FOUND_ROWS " + self.query_fields
        # end if
        self.query_from = str("FROM ") + str(wpdb_.users)
        self.query_where = "WHERE 1=1"
        #// Parse and sanitize 'include', for use by 'orderby' as well as 'include' below.
        if (not php_empty(lambda : qv_["include"])):
            include_ = wp_parse_id_list(qv_["include"])
        else:
            include_ = False
        # end if
        blog_id_ = 0
        if (php_isset(lambda : qv_["blog_id"])):
            blog_id_ = absint(qv_["blog_id"])
        # end if
        if qv_["has_published_posts"] and blog_id_:
            if True == qv_["has_published_posts"]:
                post_types_ = get_post_types(Array({"public": True}))
            else:
                post_types_ = qv_["has_published_posts"]
            # end if
            for post_type_ in post_types_:
                post_type_ = wpdb_.prepare("%s", post_type_)
            # end for
            posts_table_ = wpdb_.get_blog_prefix(blog_id_) + "posts"
            self.query_where += str(" AND ") + str(wpdb_.users) + str(".ID IN ( SELECT DISTINCT ") + str(posts_table_) + str(".post_author FROM ") + str(posts_table_) + str(" WHERE ") + str(posts_table_) + str(".post_status = 'publish' AND ") + str(posts_table_) + str(".post_type IN ( ") + php_join(", ", post_types_) + " ) )"
        # end if
        #// nicename
        if "" != qv_["nicename"]:
            self.query_where += wpdb_.prepare(" AND user_nicename = %s", qv_["nicename"])
        # end if
        if (not php_empty(lambda : qv_["nicename__in"])):
            sanitized_nicename__in_ = php_array_map("esc_sql", qv_["nicename__in"])
            nicename__in_ = php_implode("','", sanitized_nicename__in_)
            self.query_where += str(" AND user_nicename IN ( '") + str(nicename__in_) + str("' )")
        # end if
        if (not php_empty(lambda : qv_["nicename__not_in"])):
            sanitized_nicename__not_in_ = php_array_map("esc_sql", qv_["nicename__not_in"])
            nicename__not_in_ = php_implode("','", sanitized_nicename__not_in_)
            self.query_where += str(" AND user_nicename NOT IN ( '") + str(nicename__not_in_) + str("' )")
        # end if
        #// login
        if "" != qv_["login"]:
            self.query_where += wpdb_.prepare(" AND user_login = %s", qv_["login"])
        # end if
        if (not php_empty(lambda : qv_["login__in"])):
            sanitized_login__in_ = php_array_map("esc_sql", qv_["login__in"])
            login__in_ = php_implode("','", sanitized_login__in_)
            self.query_where += str(" AND user_login IN ( '") + str(login__in_) + str("' )")
        # end if
        if (not php_empty(lambda : qv_["login__not_in"])):
            sanitized_login__not_in_ = php_array_map("esc_sql", qv_["login__not_in"])
            login__not_in_ = php_implode("','", sanitized_login__not_in_)
            self.query_where += str(" AND user_login NOT IN ( '") + str(login__not_in_) + str("' )")
        # end if
        #// Meta query.
        self.meta_query = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query())
        self.meta_query.parse_query_vars(qv_)
        if (php_isset(lambda : qv_["who"])) and "authors" == qv_["who"] and blog_id_:
            who_query_ = Array({"key": wpdb_.get_blog_prefix(blog_id_) + "user_level", "value": 0, "compare": "!="})
            #// Prevent extra meta query.
            qv_["blog_id"] = 0
            blog_id_ = 0
            if php_empty(lambda : self.meta_query.queries):
                self.meta_query.queries = Array(who_query_)
            else:
                #// Append the cap query to the original queries and reparse the query.
                self.meta_query.queries = Array({"relation": "AND"}, Array(self.meta_query.queries, who_query_))
            # end if
            self.meta_query.parse_query_vars(self.meta_query.queries)
        # end if
        roles_ = Array()
        if (php_isset(lambda : qv_["role"])):
            if php_is_array(qv_["role"]):
                roles_ = qv_["role"]
            elif php_is_string(qv_["role"]) and (not php_empty(lambda : qv_["role"])):
                roles_ = php_array_map("trim", php_explode(",", qv_["role"]))
            # end if
        # end if
        role__in_ = Array()
        if (php_isset(lambda : qv_["role__in"])):
            role__in_ = qv_["role__in"]
        # end if
        role__not_in_ = Array()
        if (php_isset(lambda : qv_["role__not_in"])):
            role__not_in_ = qv_["role__not_in"]
        # end if
        if blog_id_ and (not php_empty(lambda : roles_)) or (not php_empty(lambda : role__in_)) or (not php_empty(lambda : role__not_in_)) or is_multisite():
            role_queries_ = Array()
            roles_clauses_ = Array({"relation": "AND"})
            if (not php_empty(lambda : roles_)):
                for role_ in roles_:
                    roles_clauses_[-1] = Array({"key": wpdb_.get_blog_prefix(blog_id_) + "capabilities", "value": "\"" + role_ + "\"", "compare": "LIKE"})
                # end for
                role_queries_[-1] = roles_clauses_
            # end if
            role__in_clauses_ = Array({"relation": "OR"})
            if (not php_empty(lambda : role__in_)):
                for role_ in role__in_:
                    role__in_clauses_[-1] = Array({"key": wpdb_.get_blog_prefix(blog_id_) + "capabilities", "value": "\"" + role_ + "\"", "compare": "LIKE"})
                # end for
                role_queries_[-1] = role__in_clauses_
            # end if
            role__not_in_clauses_ = Array({"relation": "AND"})
            if (not php_empty(lambda : role__not_in_)):
                for role_ in role__not_in_:
                    role__not_in_clauses_[-1] = Array({"key": wpdb_.get_blog_prefix(blog_id_) + "capabilities", "value": "\"" + role_ + "\"", "compare": "NOT LIKE"})
                # end for
                role_queries_[-1] = role__not_in_clauses_
            # end if
            #// If there are no specific roles named, make sure the user is a member of the site.
            if php_empty(lambda : role_queries_):
                role_queries_[-1] = Array({"key": wpdb_.get_blog_prefix(blog_id_) + "capabilities", "compare": "EXISTS"})
            # end if
            #// Specify that role queries should be joined with AND.
            role_queries_["relation"] = "AND"
            if php_empty(lambda : self.meta_query.queries):
                self.meta_query.queries = role_queries_
            else:
                #// Append the cap query to the original queries and reparse the query.
                self.meta_query.queries = Array({"relation": "AND"}, Array(self.meta_query.queries, role_queries_))
            # end if
            self.meta_query.parse_query_vars(self.meta_query.queries)
        # end if
        if (not php_empty(lambda : self.meta_query.queries)):
            clauses_ = self.meta_query.get_sql("user", wpdb_.users, "ID", self)
            self.query_from += clauses_["join"]
            self.query_where += clauses_["where"]
            if self.meta_query.has_or_relation():
                self.query_fields = "DISTINCT " + self.query_fields
            # end if
        # end if
        #// Sorting.
        qv_["order"] = php_strtoupper(qv_["order"]) if (php_isset(lambda : qv_["order"])) else ""
        order_ = self.parse_order(qv_["order"])
        if php_empty(lambda : qv_["orderby"]):
            #// Default order is by 'user_login'.
            ordersby_ = Array({"user_login": order_})
        elif php_is_array(qv_["orderby"]):
            ordersby_ = qv_["orderby"]
        else:
            #// 'orderby' values may be a comma- or space-separated list.
            ordersby_ = php_preg_split("/[,\\s]+/", qv_["orderby"])
        # end if
        orderby_array_ = Array()
        for _key_,_value_ in ordersby_.items():
            if (not _value_):
                continue
            # end if
            if php_is_int(_key_):
                #// Integer key means this is a flat array of 'orderby' fields.
                _orderby_ = _value_
                _order_ = order_
            else:
                #// Non-integer key means this the key is the field and the value is ASC/DESC.
                _orderby_ = _key_
                _order_ = _value_
            # end if
            parsed_ = self.parse_orderby(_orderby_)
            if (not parsed_):
                continue
            # end if
            if "nicename__in" == _orderby_ or "login__in" == _orderby_:
                orderby_array_[-1] = parsed_
            else:
                orderby_array_[-1] = parsed_ + " " + self.parse_order(_order_)
            # end if
        # end for
        #// If no valid clauses were found, order by user_login.
        if php_empty(lambda : orderby_array_):
            orderby_array_[-1] = str("user_login ") + str(order_)
        # end if
        self.query_orderby = "ORDER BY " + php_implode(", ", orderby_array_)
        #// Limit.
        if (php_isset(lambda : qv_["number"])) and qv_["number"] > 0:
            if qv_["offset"]:
                self.query_limit = wpdb_.prepare("LIMIT %d, %d", qv_["offset"], qv_["number"])
            else:
                self.query_limit = wpdb_.prepare("LIMIT %d, %d", qv_["number"] * qv_["paged"] - 1, qv_["number"])
            # end if
        # end if
        search_ = ""
        if (php_isset(lambda : qv_["search"])):
            search_ = php_trim(qv_["search"])
        # end if
        if search_:
            leading_wild_ = php_ltrim(search_, "*") != search_
            trailing_wild_ = php_rtrim(search_, "*") != search_
            if leading_wild_ and trailing_wild_:
                wild_ = "both"
            elif leading_wild_:
                wild_ = "leading"
            elif trailing_wild_:
                wild_ = "trailing"
            else:
                wild_ = False
            # end if
            if wild_:
                search_ = php_trim(search_, "*")
            # end if
            search_columns_ = Array()
            if qv_["search_columns"]:
                search_columns_ = php_array_intersect(qv_["search_columns"], Array("ID", "user_login", "user_email", "user_url", "user_nicename", "display_name"))
            # end if
            if (not search_columns_):
                if False != php_strpos(search_, "@"):
                    search_columns_ = Array("user_email")
                elif php_is_numeric(search_):
                    search_columns_ = Array("user_login", "ID")
                elif php_preg_match("|^https?://|", search_) and (not is_multisite() and wp_is_large_network("users")):
                    search_columns_ = Array("user_url")
                else:
                    search_columns_ = Array("user_login", "user_url", "user_email", "user_nicename", "display_name")
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
            search_columns_ = apply_filters("user_search_columns", search_columns_, search_, self)
            self.query_where += self.get_search_sql(search_, search_columns_, wild_)
        # end if
        if (not php_empty(lambda : include_)):
            #// Sanitized earlier.
            ids_ = php_implode(",", include_)
            self.query_where += str(" AND ") + str(wpdb_.users) + str(".ID IN (") + str(ids_) + str(")")
        elif (not php_empty(lambda : qv_["exclude"])):
            ids_ = php_implode(",", wp_parse_id_list(qv_["exclude"]))
            self.query_where += str(" AND ") + str(wpdb_.users) + str(".ID NOT IN (") + str(ids_) + str(")")
        # end if
        #// Date queries are allowed for the user_registered field.
        if (not php_empty(lambda : qv_["date_query"])) and php_is_array(qv_["date_query"]):
            date_query_ = php_new_class("WP_Date_Query", lambda : WP_Date_Query(qv_["date_query"], "user_registered"))
            self.query_where += date_query_.get_sql()
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
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        qv_ = self.query_vars
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
            if php_is_array(qv_["fields"]) or "all" == qv_["fields"]:
                self.results = wpdb_.get_results(self.request)
            else:
                self.results = wpdb_.get_col(self.request)
            # end if
            if (php_isset(lambda : qv_["count_total"])) and qv_["count_total"]:
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
                found_users_query_ = apply_filters("found_users_query", "SELECT FOUND_ROWS()", self)
                self.total_users = php_int(wpdb_.get_var(found_users_query_))
            # end if
        # end if
        if (not self.results):
            return
        # end if
        if "all_with_meta" == qv_["fields"]:
            cache_users(self.results)
            r_ = Array()
            for userid_ in self.results:
                r_[userid_] = php_new_class("WP_User", lambda : WP_User(userid_, "", qv_["blog_id"]))
            # end for
            self.results = r_
        elif "all" == qv_["fields"]:
            for key_,user_ in self.results.items():
                self.results[key_] = php_new_class("WP_User", lambda : WP_User(user_, "", qv_["blog_id"]))
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
    def get(self, query_var_=None):
        
        
        if (php_isset(lambda : self.query_vars[query_var_])):
            return self.query_vars[query_var_]
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
    def set(self, query_var_=None, value_=None):
        
        
        self.query_vars[query_var_] = value_
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
    def get_search_sql(self, string_=None, cols_=None, wild_=None):
        if wild_ is None:
            wild_ = False
        # end if
        
        global wpdb_
        php_check_if_defined("wpdb_")
        searches_ = Array()
        leading_wild_ = "%" if "leading" == wild_ or "both" == wild_ else ""
        trailing_wild_ = "%" if "trailing" == wild_ or "both" == wild_ else ""
        like_ = leading_wild_ + wpdb_.esc_like(string_) + trailing_wild_
        for col_ in cols_:
            if "ID" == col_:
                searches_[-1] = wpdb_.prepare(str(col_) + str(" = %s"), string_)
            else:
                searches_[-1] = wpdb_.prepare(str(col_) + str(" LIKE %s"), like_)
            # end if
        # end for
        return " AND (" + php_implode(" OR ", searches_) + ")"
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
    def parse_orderby(self, orderby_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        meta_query_clauses_ = self.meta_query.get_clauses()
        _orderby_ = ""
        if php_in_array(orderby_, Array("login", "nicename", "email", "url", "registered")):
            _orderby_ = "user_" + orderby_
        elif php_in_array(orderby_, Array("user_login", "user_nicename", "user_email", "user_url", "user_registered")):
            _orderby_ = orderby_
        elif "name" == orderby_ or "display_name" == orderby_:
            _orderby_ = "display_name"
        elif "post_count" == orderby_:
            #// @todo Avoid the JOIN.
            where_ = get_posts_by_author_sql("post")
            self.query_from += str(" LEFT OUTER JOIN (\n                SELECT post_author, COUNT(*) as post_count\n                FROM ") + str(wpdb_.posts) + str("\n                ") + str(where_) + str("\n              GROUP BY post_author\n          ) p ON (") + str(wpdb_.users) + str(".ID = p.post_author)\n         ")
            _orderby_ = "post_count"
        elif "ID" == orderby_ or "id" == orderby_:
            _orderby_ = "ID"
        elif "meta_value" == orderby_ or self.get("meta_key") == orderby_:
            _orderby_ = str(wpdb_.usermeta) + str(".meta_value")
        elif "meta_value_num" == orderby_:
            _orderby_ = str(wpdb_.usermeta) + str(".meta_value+0")
        elif "include" == orderby_ and (not php_empty(lambda : self.query_vars["include"])):
            include_ = wp_parse_id_list(self.query_vars["include"])
            include_sql_ = php_implode(",", include_)
            _orderby_ = str("FIELD( ") + str(wpdb_.users) + str(".ID, ") + str(include_sql_) + str(" )")
        elif "nicename__in" == orderby_:
            sanitized_nicename__in_ = php_array_map("esc_sql", self.query_vars["nicename__in"])
            nicename__in_ = php_implode("','", sanitized_nicename__in_)
            _orderby_ = str("FIELD( user_nicename, '") + str(nicename__in_) + str("' )")
        elif "login__in" == orderby_:
            sanitized_login__in_ = php_array_map("esc_sql", self.query_vars["login__in"])
            login__in_ = php_implode("','", sanitized_login__in_)
            _orderby_ = str("FIELD( user_login, '") + str(login__in_) + str("' )")
        elif (php_isset(lambda : meta_query_clauses_[orderby_])):
            meta_clause_ = meta_query_clauses_[orderby_]
            _orderby_ = php_sprintf("CAST(%s.meta_value AS %s)", esc_sql(meta_clause_["alias"]), esc_sql(meta_clause_["cast"]))
        # end if
        return _orderby_
    # end def parse_orderby
    #// 
    #// Parse an 'order' query variable and cast it to ASC or DESC as necessary.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $order The 'order' query variable.
    #// @return string The sanitized 'order' query variable.
    #//
    def parse_order(self, order_=None):
        
        
        if (not php_is_string(order_)) or php_empty(lambda : order_):
            return "DESC"
        # end if
        if "ASC" == php_strtoupper(order_):
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
    def __get(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return self.name_
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
    def __set(self, name_=None, value_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            self.name_ = value_
            return self.name_
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
    def __isset(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return (php_isset(lambda : self.name_))
        # end if
    # end def __isset
    #// 
    #// Make private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            self.name_ = None
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
    def __call(self, name_=None, arguments_=None):
        
        
        if "get_search_sql" == name_:
            return self.get_search_sql(arguments_)
        # end if
        return False
    # end def __call
# end class WP_User_Query
