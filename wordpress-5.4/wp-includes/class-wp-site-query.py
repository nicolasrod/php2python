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
#// Site API: WP_Site_Query class
#// 
#// @package WordPress
#// @subpackage Sites
#// @since 4.6.0
#// 
#// 
#// Core class used for querying sites.
#// 
#// @since 4.6.0
#// 
#// @see WP_Site_Query::__construct() for accepted arguments.
#//
class WP_Site_Query():
    request = Array()
    sql_clauses = Array({"select": "", "from": "", "where": Array(), "groupby": "", "orderby": "", "limits": ""})
    meta_query = False
    meta_query_clauses = Array()
    date_query = False
    query_vars = Array()
    query_var_defaults = Array()
    sites = Array()
    found_sites = 0
    max_num_pages = 0
    #// 
    #// Sets up the site query, based on the query vars passed.
    #// 
    #// @since 4.6.0
    #// @since 4.8.0 Introduced the 'lang_id', 'lang__in', and 'lang__not_in' parameters.
    #// @since 5.1.0 Introduced the 'update_site_meta_cache', 'meta_query', 'meta_key',
    #// 'meta_value', 'meta_type' and 'meta_compare' parameters.
    #// 
    #// @param string|array $query {
    #// Optional. Array or query string of site query parameters. Default empty.
    #// 
    #// @type array        $site__in               Array of site IDs to include. Default empty.
    #// @type array        $site__not_in           Array of site IDs to exclude. Default empty.
    #// @type bool         $count                  Whether to return a site count (true) or array of site objects.
    #// Default false.
    #// @type array        $date_query             Date query clauses to limit sites by. See WP_Date_Query.
    #// Default null.
    #// @type string       $fields                 Site fields to return. Accepts 'ids' (returns an array of site IDs)
    #// or empty (returns an array of complete site objects). Default empty.
    #// @type int          $ID                     A site ID to only return that site. Default empty.
    #// @type int          $number                 Maximum number of sites to retrieve. Default 100.
    #// @type int          $offset                 Number of sites to offset the query. Used to build LIMIT clause.
    #// Default 0.
    #// @type bool         $no_found_rows          Whether to disable the `SQL_CALC_FOUND_ROWS` query. Default true.
    #// @type string|array $orderby                Site status or array of statuses. Accepts 'id', 'domain', 'path',
    #// 'network_id', 'last_updated', 'registered', 'domain_length',
    #// 'path_length', 'site__in' and 'network__in'. Also accepts false,
    #// an empty array, or 'none' to disable `ORDER BY` clause.
    #// Default 'id'.
    #// @type string       $order                  How to order retrieved sites. Accepts 'ASC', 'DESC'. Default 'ASC'.
    #// @type int          $network_id             Limit results to those affiliated with a given network ID. If 0,
    #// include all networks. Default 0.
    #// @type array        $network__in            Array of network IDs to include affiliated sites for. Default empty.
    #// @type array        $network__not_in        Array of network IDs to exclude affiliated sites for. Default empty.
    #// @type string       $domain                 Limit results to those affiliated with a given domain. Default empty.
    #// @type array        $domain__in             Array of domains to include affiliated sites for. Default empty.
    #// @type array        $domain__not_in         Array of domains to exclude affiliated sites for. Default empty.
    #// @type string       $path                   Limit results to those affiliated with a given path. Default empty.
    #// @type array        $path__in               Array of paths to include affiliated sites for. Default empty.
    #// @type array        $path__not_in           Array of paths to exclude affiliated sites for. Default empty.
    #// @type int          $public                 Limit results to public sites. Accepts '1' or '0'. Default empty.
    #// @type int          $archived               Limit results to archived sites. Accepts '1' or '0'. Default empty.
    #// @type int          $mature                 Limit results to mature sites. Accepts '1' or '0'. Default empty.
    #// @type int          $spam                   Limit results to spam sites. Accepts '1' or '0'. Default empty.
    #// @type int          $deleted                Limit results to deleted sites. Accepts '1' or '0'. Default empty.
    #// @type int          $lang_id                Limit results to a language ID. Default empty.
    #// @type array        $lang__in               Array of language IDs to include affiliated sites for. Default empty.
    #// @type array        $lang__not_in           Array of language IDs to exclude affiliated sites for. Default empty.
    #// @type string       $search                 Search term(s) to retrieve matching sites for. Default empty.
    #// @type array        $search_columns         Array of column names to be searched. Accepts 'domain' and 'path'.
    #// Default empty array.
    #// @type bool         $update_site_cache      Whether to prime the cache for found sites. Default true.
    #// @type bool         $update_site_meta_cache Whether to prime the metadata cache for found sites. Default true.
    #// @type array        $meta_query             Meta query clauses to limit retrieved sites by. See `WP_Meta_Query`.
    #// Default empty.
    #// @type string       $meta_key               Limit sites to those matching a specific metadata key.
    #// Can be used in conjunction with `$meta_value`. Default empty.
    #// @type string       $meta_value             Limit sites to those matching a specific metadata value.
    #// Usually used in conjunction with `$meta_key`. Default empty.
    #// @type string       $meta_type              Data type that the `$meta_value` column will be CAST to for
    #// comparisons. Default empty.
    #// @type string       $meta_compare           Comparison operator to test the `$meta_value`. Default empty.
    #// }
    #//
    def __init__(self, query=""):
        
        self.query_var_defaults = Array({"fields": "", "ID": "", "site__in": "", "site__not_in": "", "number": 100, "offset": "", "no_found_rows": True, "orderby": "id", "order": "ASC", "network_id": 0, "network__in": "", "network__not_in": "", "domain": "", "domain__in": "", "domain__not_in": "", "path": "", "path__in": "", "path__not_in": "", "public": None, "archived": None, "mature": None, "spam": None, "deleted": None, "lang_id": None, "lang__in": "", "lang__not_in": "", "search": "", "search_columns": Array(), "count": False, "date_query": None, "update_site_cache": True, "update_site_meta_cache": True, "meta_query": "", "meta_key": "", "meta_value": "", "meta_type": "", "meta_compare": ""})
        if (not php_empty(lambda : query)):
            self.query(query)
        # end if
    # end def __init__
    #// 
    #// Parses arguments passed to the site query with default query parameters.
    #// 
    #// @since 4.6.0
    #// 
    #// @see WP_Site_Query::__construct()
    #// 
    #// @param string|array $query Array or string of WP_Site_Query arguments. See WP_Site_Query::__construct().
    #//
    def parse_query(self, query=""):
        
        if php_empty(lambda : query):
            query = self.query_vars
        # end if
        self.query_vars = wp_parse_args(query, self.query_var_defaults)
        #// 
        #// Fires after the site query vars have been parsed.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Site_Query $this The WP_Site_Query instance (passed by reference).
        #//
        do_action_ref_array("parse_site_query", Array(self))
    # end def parse_query
    #// 
    #// Sets up the WordPress query for retrieving sites.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|array $query Array or URL query string of parameters.
    #// @return array|int List of WP_Site objects, a list of site ids when 'fields' is set to 'ids',
    #// or the number of sites when 'count' is passed as a query var.
    #//
    def query(self, query=None):
        
        self.query_vars = wp_parse_args(query)
        return self.get_sites()
    # end def query
    #// 
    #// Retrieves a list of sites matching the query vars.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @return array|int List of WP_Site objects, a list of site ids when 'fields' is set to 'ids',
    #// or the number of sites when 'count' is passed as a query var.
    #//
    def get_sites(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        self.parse_query()
        #// Parse meta query.
        self.meta_query = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query())
        self.meta_query.parse_query_vars(self.query_vars)
        #// 
        #// Fires before sites are retrieved.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Site_Query $this Current instance of WP_Site_Query (passed by reference).
        #//
        do_action_ref_array("pre_get_sites", Array(self))
        #// Reparse query vars, in case they were modified in a 'pre_get_sites' callback.
        self.meta_query.parse_query_vars(self.query_vars)
        if (not php_empty(lambda : self.meta_query.queries)):
            self.meta_query_clauses = self.meta_query.get_sql("blog", wpdb.blogs, "blog_id", self)
        # end if
        site_data = None
        #// 
        #// Filter the site data before the get_sites query takes place.
        #// 
        #// Return a non-null value to bypass WordPress's default site queries.
        #// 
        #// The expected return type from this filter depends on the value passed in the request query_vars:
        #// When `$this->query_vars['count']` is set, the filter should return the site count as an int.
        #// When `'ids' == $this->query_vars['fields']`, the filter should return an array of site ids.
        #// Otherwise the filter should return an array of WP_Site objects.
        #// 
        #// @since 5.2.0
        #// 
        #// @param array|int|null $site_data Return an array of site data to short-circuit WP's site query,
        #// the site count as an integer if `$this->query_vars['count']` is set,
        #// or null to run the normal queries.
        #// @param WP_Site_Query  $this      The WP_Site_Query instance, passed by reference.
        #//
        site_data = apply_filters_ref_array("sites_pre_query", Array(site_data, self))
        if None != site_data:
            return site_data
        # end if
        #// $args can include anything. Only use the args defined in the query_var_defaults to compute the key.
        _args = wp_array_slice_assoc(self.query_vars, php_array_keys(self.query_var_defaults))
        _args["fields"] = None
        key = php_md5(serialize(_args))
        last_changed = wp_cache_get_last_changed("sites")
        cache_key = str("get_sites:") + str(key) + str(":") + str(last_changed)
        cache_value = wp_cache_get(cache_key, "sites")
        if False == cache_value:
            site_ids = self.get_site_ids()
            if site_ids:
                self.set_found_sites()
            # end if
            cache_value = Array({"site_ids": site_ids, "found_sites": self.found_sites})
            wp_cache_add(cache_key, cache_value, "sites")
        else:
            site_ids = cache_value["site_ids"]
            self.found_sites = cache_value["found_sites"]
        # end if
        if self.found_sites and self.query_vars["number"]:
            self.max_num_pages = ceil(self.found_sites / self.query_vars["number"])
        # end if
        #// If querying for a count only, there's nothing more to do.
        if self.query_vars["count"]:
            #// $site_ids is actually a count in this case.
            return php_intval(site_ids)
        # end if
        site_ids = php_array_map("intval", site_ids)
        if "ids" == self.query_vars["fields"]:
            self.sites = site_ids
            return self.sites
        # end if
        #// Prime site network caches.
        if self.query_vars["update_site_cache"]:
            _prime_site_caches(site_ids, self.query_vars["update_site_meta_cache"])
        # end if
        #// Fetch full site objects from the primed cache.
        _sites = Array()
        for site_id in site_ids:
            _site = get_site(site_id)
            if _site:
                _sites[-1] = _site
            # end if
        # end for
        #// 
        #// Filters the site query results.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Site[]     $_sites An array of WP_Site objects.
        #// @param WP_Site_Query $this   Current instance of WP_Site_Query (passed by reference).
        #//
        _sites = apply_filters_ref_array("the_sites", Array(_sites, self))
        #// Convert to WP_Site instances.
        self.sites = php_array_map("get_site", _sites)
        return self.sites
    # end def get_sites
    #// 
    #// Used internally to get a list of site IDs matching the query vars.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @return int|array A single count of site IDs if a count query. An array of site IDs if a full query.
    #//
    def get_site_ids(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        order = self.parse_order(self.query_vars["order"])
        #// Disable ORDER BY with 'none', an empty array, or boolean false.
        if php_in_array(self.query_vars["orderby"], Array("none", Array(), False), True):
            orderby = ""
        elif (not php_empty(lambda : self.query_vars["orderby"])):
            ordersby = self.query_vars["orderby"] if php_is_array(self.query_vars["orderby"]) else php_preg_split("/[,\\s]/", self.query_vars["orderby"])
            orderby_array = Array()
            for _key,_value in ordersby:
                if (not _value):
                    continue
                # end if
                if php_is_int(_key):
                    _orderby = _value
                    _order = order
                else:
                    _orderby = _key
                    _order = _value
                # end if
                parsed = self.parse_orderby(_orderby)
                if (not parsed):
                    continue
                # end if
                if "site__in" == _orderby or "network__in" == _orderby:
                    orderby_array[-1] = parsed
                    continue
                # end if
                orderby_array[-1] = parsed + " " + self.parse_order(_order)
            # end for
            orderby = php_implode(", ", orderby_array)
        else:
            orderby = str(wpdb.blogs) + str(".blog_id ") + str(order)
        # end if
        number = absint(self.query_vars["number"])
        offset = absint(self.query_vars["offset"])
        limits = ""
        if (not php_empty(lambda : number)):
            if offset:
                limits = "LIMIT " + offset + "," + number
            else:
                limits = "LIMIT " + number
            # end if
        # end if
        if self.query_vars["count"]:
            fields = "COUNT(*)"
        else:
            fields = str(wpdb.blogs) + str(".blog_id")
        # end if
        #// Parse site IDs for an IN clause.
        site_id = absint(self.query_vars["ID"])
        if (not php_empty(lambda : site_id)):
            self.sql_clauses["where"]["ID"] = wpdb.prepare(str(wpdb.blogs) + str(".blog_id = %d"), site_id)
        # end if
        #// Parse site IDs for an IN clause.
        if (not php_empty(lambda : self.query_vars["site__in"])):
            self.sql_clauses["where"]["site__in"] = str(wpdb.blogs) + str(".blog_id IN ( ") + php_implode(",", wp_parse_id_list(self.query_vars["site__in"])) + " )"
        # end if
        #// Parse site IDs for a NOT IN clause.
        if (not php_empty(lambda : self.query_vars["site__not_in"])):
            self.sql_clauses["where"]["site__not_in"] = str(wpdb.blogs) + str(".blog_id NOT IN ( ") + php_implode(",", wp_parse_id_list(self.query_vars["site__not_in"])) + " )"
        # end if
        network_id = absint(self.query_vars["network_id"])
        if (not php_empty(lambda : network_id)):
            self.sql_clauses["where"]["network_id"] = wpdb.prepare("site_id = %d", network_id)
        # end if
        #// Parse site network IDs for an IN clause.
        if (not php_empty(lambda : self.query_vars["network__in"])):
            self.sql_clauses["where"]["network__in"] = "site_id IN ( " + php_implode(",", wp_parse_id_list(self.query_vars["network__in"])) + " )"
        # end if
        #// Parse site network IDs for a NOT IN clause.
        if (not php_empty(lambda : self.query_vars["network__not_in"])):
            self.sql_clauses["where"]["network__not_in"] = "site_id NOT IN ( " + php_implode(",", wp_parse_id_list(self.query_vars["network__not_in"])) + " )"
        # end if
        if (not php_empty(lambda : self.query_vars["domain"])):
            self.sql_clauses["where"]["domain"] = wpdb.prepare("domain = %s", self.query_vars["domain"])
        # end if
        #// Parse site domain for an IN clause.
        if php_is_array(self.query_vars["domain__in"]):
            self.sql_clauses["where"]["domain__in"] = "domain IN ( '" + php_implode("', '", wpdb._escape(self.query_vars["domain__in"])) + "' )"
        # end if
        #// Parse site domain for a NOT IN clause.
        if php_is_array(self.query_vars["domain__not_in"]):
            self.sql_clauses["where"]["domain__not_in"] = "domain NOT IN ( '" + php_implode("', '", wpdb._escape(self.query_vars["domain__not_in"])) + "' )"
        # end if
        if (not php_empty(lambda : self.query_vars["path"])):
            self.sql_clauses["where"]["path"] = wpdb.prepare("path = %s", self.query_vars["path"])
        # end if
        #// Parse site path for an IN clause.
        if php_is_array(self.query_vars["path__in"]):
            self.sql_clauses["where"]["path__in"] = "path IN ( '" + php_implode("', '", wpdb._escape(self.query_vars["path__in"])) + "' )"
        # end if
        #// Parse site path for a NOT IN clause.
        if php_is_array(self.query_vars["path__not_in"]):
            self.sql_clauses["where"]["path__not_in"] = "path NOT IN ( '" + php_implode("', '", wpdb._escape(self.query_vars["path__not_in"])) + "' )"
        # end if
        if php_is_numeric(self.query_vars["archived"]):
            archived = absint(self.query_vars["archived"])
            self.sql_clauses["where"]["archived"] = wpdb.prepare("archived = %s ", absint(archived))
        # end if
        if php_is_numeric(self.query_vars["mature"]):
            mature = absint(self.query_vars["mature"])
            self.sql_clauses["where"]["mature"] = wpdb.prepare("mature = %d ", mature)
        # end if
        if php_is_numeric(self.query_vars["spam"]):
            spam = absint(self.query_vars["spam"])
            self.sql_clauses["where"]["spam"] = wpdb.prepare("spam = %d ", spam)
        # end if
        if php_is_numeric(self.query_vars["deleted"]):
            deleted = absint(self.query_vars["deleted"])
            self.sql_clauses["where"]["deleted"] = wpdb.prepare("deleted = %d ", deleted)
        # end if
        if php_is_numeric(self.query_vars["public"]):
            public = absint(self.query_vars["public"])
            self.sql_clauses["where"]["public"] = wpdb.prepare("public = %d ", public)
        # end if
        if php_is_numeric(self.query_vars["lang_id"]):
            lang_id = absint(self.query_vars["lang_id"])
            self.sql_clauses["where"]["lang_id"] = wpdb.prepare("lang_id = %d ", lang_id)
        # end if
        #// Parse site language IDs for an IN clause.
        if (not php_empty(lambda : self.query_vars["lang__in"])):
            self.sql_clauses["where"]["lang__in"] = "lang_id IN ( " + php_implode(",", wp_parse_id_list(self.query_vars["lang__in"])) + " )"
        # end if
        #// Parse site language IDs for a NOT IN clause.
        if (not php_empty(lambda : self.query_vars["lang__not_in"])):
            self.sql_clauses["where"]["lang__not_in"] = "lang_id NOT IN ( " + php_implode(",", wp_parse_id_list(self.query_vars["lang__not_in"])) + " )"
        # end if
        #// Falsey search strings are ignored.
        if php_strlen(self.query_vars["search"]):
            search_columns = Array()
            if self.query_vars["search_columns"]:
                search_columns = php_array_intersect(self.query_vars["search_columns"], Array("domain", "path"))
            # end if
            if (not search_columns):
                search_columns = Array("domain", "path")
            # end if
            #// 
            #// Filters the columns to search in a WP_Site_Query search.
            #// 
            #// The default columns include 'domain' and 'path.
            #// 
            #// @since 4.6.0
            #// 
            #// @param string[]      $search_columns Array of column names to be searched.
            #// @param string        $search         Text being searched.
            #// @param WP_Site_Query $this           The current WP_Site_Query instance.
            #//
            search_columns = apply_filters("site_search_columns", search_columns, self.query_vars["search"], self)
            self.sql_clauses["where"]["search"] = self.get_search_sql(self.query_vars["search"], search_columns)
        # end if
        date_query = self.query_vars["date_query"]
        if (not php_empty(lambda : date_query)) and php_is_array(date_query):
            self.date_query = php_new_class("WP_Date_Query", lambda : WP_Date_Query(date_query, "registered"))
            self.sql_clauses["where"]["date_query"] = php_preg_replace("/^\\s*AND\\s*/", "", self.date_query.get_sql())
        # end if
        join = ""
        groupby = ""
        if (not php_empty(lambda : self.meta_query_clauses)):
            join += self.meta_query_clauses["join"]
            #// Strip leading 'AND'.
            self.sql_clauses["where"]["meta_query"] = php_preg_replace("/^\\s*AND\\s*/", "", self.meta_query_clauses["where"])
            if (not self.query_vars["count"]):
                groupby = str(wpdb.blogs) + str(".blog_id")
            # end if
        # end if
        where = php_implode(" AND ", self.sql_clauses["where"])
        pieces = Array("fields", "join", "where", "orderby", "limits", "groupby")
        #// 
        #// Filters the site query clauses.
        #// 
        #// @since 4.6.0
        #// 
        #// @param string[]      $pieces An associative array of site query clauses.
        #// @param WP_Site_Query $this   Current instance of WP_Site_Query (passed by reference).
        #//
        clauses = apply_filters_ref_array("sites_clauses", Array(compact(pieces), self))
        fields = clauses["fields"] if (php_isset(lambda : clauses["fields"])) else ""
        join = clauses["join"] if (php_isset(lambda : clauses["join"])) else ""
        where = clauses["where"] if (php_isset(lambda : clauses["where"])) else ""
        orderby = clauses["orderby"] if (php_isset(lambda : clauses["orderby"])) else ""
        limits = clauses["limits"] if (php_isset(lambda : clauses["limits"])) else ""
        groupby = clauses["groupby"] if (php_isset(lambda : clauses["groupby"])) else ""
        if where:
            where = "WHERE " + where
        # end if
        if groupby:
            groupby = "GROUP BY " + groupby
        # end if
        if orderby:
            orderby = str("ORDER BY ") + str(orderby)
        # end if
        found_rows = ""
        if (not self.query_vars["no_found_rows"]):
            found_rows = "SQL_CALC_FOUND_ROWS"
        # end if
        self.sql_clauses["select"] = str("SELECT ") + str(found_rows) + str(" ") + str(fields)
        self.sql_clauses["from"] = str("FROM ") + str(wpdb.blogs) + str(" ") + str(join)
        self.sql_clauses["groupby"] = groupby
        self.sql_clauses["orderby"] = orderby
        self.sql_clauses["limits"] = limits
        self.request = str(self.sql_clauses["select"]) + str(" ") + str(self.sql_clauses["from"]) + str(" ") + str(where) + str(" ") + str(self.sql_clauses["groupby"]) + str(" ") + str(self.sql_clauses["orderby"]) + str(" ") + str(self.sql_clauses["limits"])
        if self.query_vars["count"]:
            return php_intval(wpdb.get_var(self.request))
        # end if
        site_ids = wpdb.get_col(self.request)
        return php_array_map("intval", site_ids)
    # end def get_site_ids
    #// 
    #// Populates found_sites and max_num_pages properties for the current query
    #// if the limit clause was used.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #//
    def set_found_sites(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        if self.query_vars["number"] and (not self.query_vars["no_found_rows"]):
            #// 
            #// Filters the query used to retrieve found site count.
            #// 
            #// @since 4.6.0
            #// 
            #// @param string        $found_sites_query SQL query. Default 'SELECT FOUND_ROWS()'.
            #// @param WP_Site_Query $site_query        The `WP_Site_Query` instance.
            #//
            found_sites_query = apply_filters("found_sites_query", "SELECT FOUND_ROWS()", self)
            self.found_sites = int(wpdb.get_var(found_sites_query))
        # end if
    # end def set_found_sites
    #// 
    #// Used internally to generate an SQL string for searching across multiple columns.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string   $string  Search string.
    #// @param string[] $columns Array of columns to search.
    #// @return string Search SQL.
    #//
    def get_search_sql(self, string=None, columns=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        if False != php_strpos(string, "*"):
            like = "%" + php_implode("%", php_array_map(Array(wpdb, "esc_like"), php_explode("*", string))) + "%"
        else:
            like = "%" + wpdb.esc_like(string) + "%"
        # end if
        searches = Array()
        for column in columns:
            searches[-1] = wpdb.prepare(str(column) + str(" LIKE %s"), like)
        # end for
        return "(" + php_implode(" OR ", searches) + ")"
    # end def get_search_sql
    #// 
    #// Parses and sanitizes 'orderby' keys passed to the site query.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $orderby Alias for the field to order by.
    #// @return string|false Value to used in the ORDER clause. False otherwise.
    #//
    def parse_orderby(self, orderby=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        parsed = False
        for case in Switch(orderby):
            if case("site__in"):
                site__in = php_implode(",", php_array_map("absint", self.query_vars["site__in"]))
                parsed = str("FIELD( ") + str(wpdb.blogs) + str(".blog_id, ") + str(site__in) + str(" )")
                break
            # end if
            if case("network__in"):
                network__in = php_implode(",", php_array_map("absint", self.query_vars["network__in"]))
                parsed = str("FIELD( ") + str(wpdb.blogs) + str(".site_id, ") + str(network__in) + str(" )")
                break
            # end if
            if case("domain"):
                pass
            # end if
            if case("last_updated"):
                pass
            # end if
            if case("path"):
                pass
            # end if
            if case("registered"):
                parsed = orderby
                break
            # end if
            if case("network_id"):
                parsed = "site_id"
                break
            # end if
            if case("domain_length"):
                parsed = "CHAR_LENGTH(domain)"
                break
            # end if
            if case("path_length"):
                parsed = "CHAR_LENGTH(path)"
                break
            # end if
            if case("id"):
                parsed = str(wpdb.blogs) + str(".blog_id")
                break
            # end if
        # end for
        if (not php_empty(lambda : parsed)) or php_empty(lambda : self.meta_query_clauses):
            return parsed
        # end if
        meta_clauses = self.meta_query.get_clauses()
        if php_empty(lambda : meta_clauses):
            return parsed
        # end if
        primary_meta_query = reset(meta_clauses)
        if (not php_empty(lambda : primary_meta_query["key"])) and primary_meta_query["key"] == orderby:
            orderby = "meta_value"
        # end if
        for case in Switch(orderby):
            if case("meta_value"):
                if (not php_empty(lambda : primary_meta_query["type"])):
                    parsed = str("CAST(") + str(primary_meta_query["alias"]) + str(".meta_value AS ") + str(primary_meta_query["cast"]) + str(")")
                else:
                    parsed = str(primary_meta_query["alias"]) + str(".meta_value")
                # end if
                break
            # end if
            if case("meta_value_num"):
                parsed = str(primary_meta_query["alias"]) + str(".meta_value+0")
                break
            # end if
            if case():
                if (php_isset(lambda : meta_clauses[orderby])):
                    meta_clause = meta_clauses[orderby]
                    parsed = str("CAST(") + str(meta_clause["alias"]) + str(".meta_value AS ") + str(meta_clause["cast"]) + str(")")
                # end if
            # end if
        # end for
        return parsed
    # end def parse_orderby
    #// 
    #// Parses an 'order' query variable and cast it to 'ASC' or 'DESC' as necessary.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $order The 'order' query variable.
    #// @return string The sanitized 'order' query variable.
    #//
    def parse_order(self, order=None):
        
        if (not php_is_string(order)) or php_empty(lambda : order):
            return "ASC"
        # end if
        if "ASC" == php_strtoupper(order):
            return "ASC"
        else:
            return "DESC"
        # end if
    # end def parse_order
# end class WP_Site_Query
