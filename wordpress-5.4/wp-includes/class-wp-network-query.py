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
#// Network API: WP_Network_Query class
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 4.6.0
#// 
#// 
#// Core class used for querying networks.
#// 
#// @since 4.6.0
#// 
#// @see WP_Network_Query::__construct() for accepted arguments.
#//
class WP_Network_Query():
    #// 
    #// SQL for database query.
    #// 
    #// @since 4.6.0
    #// @var string
    #//
    request = Array()
    #// 
    #// SQL query clauses.
    #// 
    #// @since 4.6.0
    #// @var array
    #//
    sql_clauses = Array({"select": "", "from": "", "where": Array(), "groupby": "", "orderby": "", "limits": ""})
    #// 
    #// Query vars set by the user.
    #// 
    #// @since 4.6.0
    #// @var array
    #//
    query_vars = Array()
    #// 
    #// Default values for query vars.
    #// 
    #// @since 4.6.0
    #// @var array
    #//
    query_var_defaults = Array()
    #// 
    #// List of networks located by the query.
    #// 
    #// @since 4.6.0
    #// @var array
    #//
    networks = Array()
    #// 
    #// The amount of found networks for the current query.
    #// 
    #// @since 4.6.0
    #// @var int
    #//
    found_networks = 0
    #// 
    #// The number of pages.
    #// 
    #// @since 4.6.0
    #// @var int
    #//
    max_num_pages = 0
    #// 
    #// Constructor.
    #// 
    #// Sets up the network query, based on the query vars passed.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|array $query {
    #// Optional. Array or query string of network query parameters. Default empty.
    #// 
    #// @type array        $network__in          Array of network IDs to include. Default empty.
    #// @type array        $network__not_in      Array of network IDs to exclude. Default empty.
    #// @type bool         $count                Whether to return a network count (true) or array of network objects.
    #// Default false.
    #// @type string       $fields               Network fields to return. Accepts 'ids' (returns an array of network IDs)
    #// or empty (returns an array of complete network objects). Default empty.
    #// @type int          $number               Maximum number of networks to retrieve. Default empty (no limit).
    #// @type int          $offset               Number of networks to offset the query. Used to build LIMIT clause.
    #// Default 0.
    #// @type bool         $no_found_rows        Whether to disable the `SQL_CALC_FOUND_ROWS` query. Default true.
    #// @type string|array $orderby              Network status or array of statuses. Accepts 'id', 'domain', 'path',
    #// 'domain_length', 'path_length' and 'network__in'. Also accepts false,
    #// an empty array, or 'none' to disable `ORDER BY` clause. Default 'id'.
    #// @type string       $order                How to order retrieved networks. Accepts 'ASC', 'DESC'. Default 'ASC'.
    #// @type string       $domain               Limit results to those affiliated with a given domain. Default empty.
    #// @type array        $domain__in           Array of domains to include affiliated networks for. Default empty.
    #// @type array        $domain__not_in       Array of domains to exclude affiliated networks for. Default empty.
    #// @type string       $path                 Limit results to those affiliated with a given path. Default empty.
    #// @type array        $path__in             Array of paths to include affiliated networks for. Default empty.
    #// @type array        $path__not_in         Array of paths to exclude affiliated networks for. Default empty.
    #// @type string       $search               Search term(s) to retrieve matching networks for. Default empty.
    #// @type bool         $update_network_cache Whether to prime the cache for found networks. Default true.
    #// }
    #//
    def __init__(self, query_=""):
        
        
        self.query_var_defaults = Array({"network__in": "", "network__not_in": "", "count": False, "fields": "", "number": "", "offset": "", "no_found_rows": True, "orderby": "id", "order": "ASC", "domain": "", "domain__in": "", "domain__not_in": "", "path": "", "path__in": "", "path__not_in": "", "search": "", "update_network_cache": True})
        if (not php_empty(lambda : query_)):
            self.query(query_)
        # end if
    # end def __init__
    #// 
    #// Parses arguments passed to the network query with default query parameters.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|array $query WP_Network_Query arguments. See WP_Network_Query::__construct()
    #//
    def parse_query(self, query_=""):
        
        
        if php_empty(lambda : query_):
            query_ = self.query_vars
        # end if
        self.query_vars = wp_parse_args(query_, self.query_var_defaults)
        #// 
        #// Fires after the network query vars have been parsed.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Network_Query $this The WP_Network_Query instance (passed by reference).
        #//
        do_action_ref_array("parse_network_query", Array(self))
    # end def parse_query
    #// 
    #// Sets up the WordPress query for retrieving networks.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|array $query Array or URL query string of parameters.
    #// @return array|int List of WP_Network objects, a list of network ids when 'fields' is set to 'ids',
    #// or the number of networks when 'count' is passed as a query var.
    #//
    def query(self, query_=None):
        
        
        self.query_vars = wp_parse_args(query_)
        return self.get_networks()
    # end def query
    #// 
    #// Gets a list of networks matching the query vars.
    #// 
    #// @since 4.6.0
    #// 
    #// @return array|int List of WP_Network objects, a list of network ids when 'fields' is set to 'ids',
    #// or the number of networks when 'count' is passed as a query var.
    #//
    def get_networks(self):
        
        
        self.parse_query()
        #// 
        #// Fires before networks are retrieved.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Network_Query $this Current instance of WP_Network_Query (passed by reference).
        #//
        do_action_ref_array("pre_get_networks", Array(self))
        network_data_ = None
        #// 
        #// Filter the network data before the query takes place.
        #// 
        #// Return a non-null value to bypass WordPress's default network queries.
        #// 
        #// The expected return type from this filter depends on the value passed in the request query_vars.
        #// When `$this->query_vars['count']` is set, the filter should return the network count as an int.
        #// When `'ids' === $this->query_vars['fields']`, the filter should return an array of network ids.
        #// Otherwise the filter should return an array of WP_Network objects.
        #// 
        #// @since 5.2.0
        #// 
        #// @param array|null       $network_data Return an array of network data to short-circuit WP's network query,
        #// the network count as an integer if `$this->query_vars['count']` is set,
        #// or null to allow WP to run its normal queries.
        #// @param WP_Network_Query $this         The WP_Network_Query instance, passed by reference.
        #//
        network_data_ = apply_filters_ref_array("networks_pre_query", Array(network_data_, self))
        if None != network_data_:
            return network_data_
        # end if
        #// $args can include anything. Only use the args defined in the query_var_defaults to compute the key.
        _args_ = wp_array_slice_assoc(self.query_vars, php_array_keys(self.query_var_defaults))
        _args_["fields"] = None
        key_ = php_md5(serialize(_args_))
        last_changed_ = wp_cache_get_last_changed("networks")
        cache_key_ = str("get_network_ids:") + str(key_) + str(":") + str(last_changed_)
        cache_value_ = wp_cache_get(cache_key_, "networks")
        if False == cache_value_:
            network_ids_ = self.get_network_ids()
            if network_ids_:
                self.set_found_networks()
            # end if
            cache_value_ = Array({"network_ids": network_ids_, "found_networks": self.found_networks})
            wp_cache_add(cache_key_, cache_value_, "networks")
        else:
            network_ids_ = cache_value_["network_ids"]
            self.found_networks = cache_value_["found_networks"]
        # end if
        if self.found_networks and self.query_vars["number"]:
            self.max_num_pages = ceil(self.found_networks / self.query_vars["number"])
        # end if
        #// If querying for a count only, there's nothing more to do.
        if self.query_vars["count"]:
            #// $network_ids is actually a count in this case.
            return php_intval(network_ids_)
        # end if
        network_ids_ = php_array_map("intval", network_ids_)
        if "ids" == self.query_vars["fields"]:
            self.networks = network_ids_
            return self.networks
        # end if
        if self.query_vars["update_network_cache"]:
            _prime_network_caches(network_ids_)
        # end if
        #// Fetch full network objects from the primed cache.
        _networks_ = Array()
        for network_id_ in network_ids_:
            _network_ = get_network(network_id_)
            if _network_:
                _networks_[-1] = _network_
            # end if
        # end for
        #// 
        #// Filters the network query results.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Network[]     $_networks An array of WP_Network objects.
        #// @param WP_Network_Query $this      Current instance of WP_Network_Query (passed by reference).
        #//
        _networks_ = apply_filters_ref_array("the_networks", Array(_networks_, self))
        #// Convert to WP_Network instances.
        self.networks = php_array_map("get_network", _networks_)
        return self.networks
    # end def get_networks
    #// 
    #// Used internally to get a list of network IDs matching the query vars.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @return int|array A single count of network IDs if a count query. An array of network IDs if a full query.
    #//
    def get_network_ids(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        order_ = self.parse_order(self.query_vars["order"])
        #// Disable ORDER BY with 'none', an empty array, or boolean false.
        if php_in_array(self.query_vars["orderby"], Array("none", Array(), False), True):
            orderby_ = ""
        elif (not php_empty(lambda : self.query_vars["orderby"])):
            ordersby_ = self.query_vars["orderby"] if php_is_array(self.query_vars["orderby"]) else php_preg_split("/[,\\s]/", self.query_vars["orderby"])
            orderby_array_ = Array()
            for _key_,_value_ in ordersby_.items():
                if (not _value_):
                    continue
                # end if
                if php_is_int(_key_):
                    _orderby_ = _value_
                    _order_ = order_
                else:
                    _orderby_ = _key_
                    _order_ = _value_
                # end if
                parsed_ = self.parse_orderby(_orderby_)
                if (not parsed_):
                    continue
                # end if
                if "network__in" == _orderby_:
                    orderby_array_[-1] = parsed_
                    continue
                # end if
                orderby_array_[-1] = parsed_ + " " + self.parse_order(_order_)
            # end for
            orderby_ = php_implode(", ", orderby_array_)
        else:
            orderby_ = str(wpdb_.site) + str(".id ") + str(order_)
        # end if
        number_ = absint(self.query_vars["number"])
        offset_ = absint(self.query_vars["offset"])
        limits_ = ""
        if (not php_empty(lambda : number_)):
            if offset_:
                limits_ = "LIMIT " + offset_ + "," + number_
            else:
                limits_ = "LIMIT " + number_
            # end if
        # end if
        if self.query_vars["count"]:
            fields_ = "COUNT(*)"
        else:
            fields_ = str(wpdb_.site) + str(".id")
        # end if
        #// Parse network IDs for an IN clause.
        if (not php_empty(lambda : self.query_vars["network__in"])):
            self.sql_clauses["where"]["network__in"] = str(wpdb_.site) + str(".id IN ( ") + php_implode(",", wp_parse_id_list(self.query_vars["network__in"])) + " )"
        # end if
        #// Parse network IDs for a NOT IN clause.
        if (not php_empty(lambda : self.query_vars["network__not_in"])):
            self.sql_clauses["where"]["network__not_in"] = str(wpdb_.site) + str(".id NOT IN ( ") + php_implode(",", wp_parse_id_list(self.query_vars["network__not_in"])) + " )"
        # end if
        if (not php_empty(lambda : self.query_vars["domain"])):
            self.sql_clauses["where"]["domain"] = wpdb_.prepare(str(wpdb_.site) + str(".domain = %s"), self.query_vars["domain"])
        # end if
        #// Parse network domain for an IN clause.
        if php_is_array(self.query_vars["domain__in"]):
            self.sql_clauses["where"]["domain__in"] = str(wpdb_.site) + str(".domain IN ( '") + php_implode("', '", wpdb_._escape(self.query_vars["domain__in"])) + "' )"
        # end if
        #// Parse network domain for a NOT IN clause.
        if php_is_array(self.query_vars["domain__not_in"]):
            self.sql_clauses["where"]["domain__not_in"] = str(wpdb_.site) + str(".domain NOT IN ( '") + php_implode("', '", wpdb_._escape(self.query_vars["domain__not_in"])) + "' )"
        # end if
        if (not php_empty(lambda : self.query_vars["path"])):
            self.sql_clauses["where"]["path"] = wpdb_.prepare(str(wpdb_.site) + str(".path = %s"), self.query_vars["path"])
        # end if
        #// Parse network path for an IN clause.
        if php_is_array(self.query_vars["path__in"]):
            self.sql_clauses["where"]["path__in"] = str(wpdb_.site) + str(".path IN ( '") + php_implode("', '", wpdb_._escape(self.query_vars["path__in"])) + "' )"
        # end if
        #// Parse network path for a NOT IN clause.
        if php_is_array(self.query_vars["path__not_in"]):
            self.sql_clauses["where"]["path__not_in"] = str(wpdb_.site) + str(".path NOT IN ( '") + php_implode("', '", wpdb_._escape(self.query_vars["path__not_in"])) + "' )"
        # end if
        #// Falsey search strings are ignored.
        if php_strlen(self.query_vars["search"]):
            self.sql_clauses["where"]["search"] = self.get_search_sql(self.query_vars["search"], Array(str(wpdb_.site) + str(".domain"), str(wpdb_.site) + str(".path")))
        # end if
        join_ = ""
        where_ = php_implode(" AND ", self.sql_clauses["where"])
        groupby_ = ""
        pieces_ = Array("fields", "join", "where", "orderby", "limits", "groupby")
        #// 
        #// Filters the network query clauses.
        #// 
        #// @since 4.6.0
        #// 
        #// @param string[]         $pieces An associative array of network query clauses.
        #// @param WP_Network_Query $this   Current instance of WP_Network_Query (passed by reference).
        #//
        clauses_ = apply_filters_ref_array("networks_clauses", Array(php_compact(pieces_), self))
        fields_ = clauses_["fields"] if (php_isset(lambda : clauses_["fields"])) else ""
        join_ = clauses_["join"] if (php_isset(lambda : clauses_["join"])) else ""
        where_ = clauses_["where"] if (php_isset(lambda : clauses_["where"])) else ""
        orderby_ = clauses_["orderby"] if (php_isset(lambda : clauses_["orderby"])) else ""
        limits_ = clauses_["limits"] if (php_isset(lambda : clauses_["limits"])) else ""
        groupby_ = clauses_["groupby"] if (php_isset(lambda : clauses_["groupby"])) else ""
        if where_:
            where_ = "WHERE " + where_
        # end if
        if groupby_:
            groupby_ = "GROUP BY " + groupby_
        # end if
        if orderby_:
            orderby_ = str("ORDER BY ") + str(orderby_)
        # end if
        found_rows_ = ""
        if (not self.query_vars["no_found_rows"]):
            found_rows_ = "SQL_CALC_FOUND_ROWS"
        # end if
        self.sql_clauses["select"] = str("SELECT ") + str(found_rows_) + str(" ") + str(fields_)
        self.sql_clauses["from"] = str("FROM ") + str(wpdb_.site) + str(" ") + str(join_)
        self.sql_clauses["groupby"] = groupby_
        self.sql_clauses["orderby"] = orderby_
        self.sql_clauses["limits"] = limits_
        self.request = str(self.sql_clauses["select"]) + str(" ") + str(self.sql_clauses["from"]) + str(" ") + str(where_) + str(" ") + str(self.sql_clauses["groupby"]) + str(" ") + str(self.sql_clauses["orderby"]) + str(" ") + str(self.sql_clauses["limits"])
        if self.query_vars["count"]:
            return php_intval(wpdb_.get_var(self.request))
        # end if
        network_ids_ = wpdb_.get_col(self.request)
        return php_array_map("intval", network_ids_)
    # end def get_network_ids
    #// 
    #// Populates found_networks and max_num_pages properties for the current query
    #// if the limit clause was used.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #//
    def set_found_networks(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if self.query_vars["number"] and (not self.query_vars["no_found_rows"]):
            #// 
            #// Filters the query used to retrieve found network count.
            #// 
            #// @since 4.6.0
            #// 
            #// @param string           $found_networks_query SQL query. Default 'SELECT FOUND_ROWS()'.
            #// @param WP_Network_Query $network_query        The `WP_Network_Query` instance.
            #//
            found_networks_query_ = apply_filters("found_networks_query", "SELECT FOUND_ROWS()", self)
            self.found_networks = php_int(wpdb_.get_var(found_networks_query_))
        # end if
    # end def set_found_networks
    #// 
    #// Used internally to generate an SQL string for searching across multiple columns.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string   $string  Search string.
    #// @param string[] $columns Array of columns to search.
    #// 
    #// @return string Search SQL.
    #//
    def get_search_sql(self, string_=None, columns_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        like_ = "%" + wpdb_.esc_like(string_) + "%"
        searches_ = Array()
        for column_ in columns_:
            searches_[-1] = wpdb_.prepare(str(column_) + str(" LIKE %s"), like_)
        # end for
        return "(" + php_implode(" OR ", searches_) + ")"
    # end def get_search_sql
    #// 
    #// Parses and sanitizes 'orderby' keys passed to the network query.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $orderby Alias for the field to order by.
    #// @return string|false Value to used in the ORDER clause. False otherwise.
    #//
    def parse_orderby(self, orderby_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        allowed_keys_ = Array("id", "domain", "path")
        parsed_ = False
        if "network__in" == orderby_:
            network__in_ = php_implode(",", php_array_map("absint", self.query_vars["network__in"]))
            parsed_ = str("FIELD( ") + str(wpdb_.site) + str(".id, ") + str(network__in_) + str(" )")
        elif "domain_length" == orderby_ or "path_length" == orderby_:
            field_ = php_substr(orderby_, 0, -7)
            parsed_ = str("CHAR_LENGTH(") + str(wpdb_.site) + str(".") + str(field_) + str(")")
        elif php_in_array(orderby_, allowed_keys_):
            parsed_ = str(wpdb_.site) + str(".") + str(orderby_)
        # end if
        return parsed_
    # end def parse_orderby
    #// 
    #// Parses an 'order' query variable and cast it to 'ASC' or 'DESC' as necessary.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $order The 'order' query variable.
    #// @return string The sanitized 'order' query variable.
    #//
    def parse_order(self, order_=None):
        
        
        if (not php_is_string(order_)) or php_empty(lambda : order_):
            return "ASC"
        # end if
        if "ASC" == php_strtoupper(order_):
            return "ASC"
        else:
            return "DESC"
        # end if
    # end def parse_order
# end class WP_Network_Query
