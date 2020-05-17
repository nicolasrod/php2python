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
#// Meta API: WP_Meta_Query class
#// 
#// @package WordPress
#// @subpackage Meta
#// @since 4.4.0
#// 
#// 
#// Core class used to implement meta queries for the Meta API.
#// 
#// Used for generating SQL clauses that filter a primary query according to metadata keys and values.
#// 
#// WP_Meta_Query is a helper that allows primary query classes, such as WP_Query and WP_User_Query,
#// 
#// to filter their results by object metadata, by generating `JOIN` and `WHERE` subclauses to be attached
#// to the primary SQL query string.
#// 
#// @since 3.2.0
#//
class WP_Meta_Query():
    #// 
    #// Array of metadata queries.
    #// 
    #// See WP_Meta_Query::__construct() for information on meta query arguments.
    #// 
    #// @since 3.2.0
    #// @var array
    #//
    queries = Array()
    #// 
    #// The relation between the queries. Can be one of 'AND' or 'OR'.
    #// 
    #// @since 3.2.0
    #// @var string
    #//
    relation = Array()
    #// 
    #// Database table to query for the metadata.
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    meta_table = Array()
    #// 
    #// Column in meta_table that represents the ID of the object the metadata belongs to.
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    meta_id_column = Array()
    #// 
    #// Database table that where the metadata's objects are stored (eg $wpdb->users).
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    primary_table = Array()
    #// 
    #// Column in primary_table that represents the ID of the object.
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    primary_id_column = Array()
    #// 
    #// A flat list of table aliases used in JOIN clauses.
    #// 
    #// @since 4.1.0
    #// @var array
    #//
    table_aliases = Array()
    #// 
    #// A flat list of clauses, keyed by clause 'name'.
    #// 
    #// @since 4.2.0
    #// @var array
    #//
    clauses = Array()
    #// 
    #// Whether the query contains any OR relations.
    #// 
    #// @since 4.3.0
    #// @var bool
    #//
    has_or_relation = False
    #// 
    #// Constructor.
    #// 
    #// @since 3.2.0
    #// @since 4.2.0 Introduced support for naming query clauses by associative array keys.
    #// @since 5.1.0 Introduced $compare_key clause parameter, which enables LIKE key matches.
    #// @since 5.3.0 Increased the number of operators available to $compare_key. Introduced $type_key,
    #// which enables the $key to be cast to a new data type for comparisons.
    #// 
    #// @param array $meta_query {
    #// Array of meta query clauses. When first-order clauses or sub-clauses use strings as
    #// their array keys, they may be referenced in the 'orderby' parameter of the parent query.
    #// 
    #// @type string $relation Optional. The MySQL keyword used to join
    #// the clauses of the query. Accepts 'AND', or 'OR'. Default 'AND'.
    #// @type array {
    #// Optional. An array of first-order clause parameters, or another fully-formed meta query.
    #// 
    #// @type string $key         Meta key to filter by.
    #// @type string $compare_key MySQL operator used for comparing the $key. Accepts '=', '!='
    #// 'LIKE', 'NOT LIKE', 'IN', 'NOT IN', 'REGEXP', 'NOT REGEXP', 'RLIKE',
    #// 'EXISTS' (alias of '=') or 'NOT EXISTS' (alias of '!=').
    #// Default is 'IN' when `$key` is an array, '=' otherwise.
    #// @type string $type_key    MySQL data type that the meta_key column will be CAST to for
    #// comparisons. Accepts 'BINARY' for case-sensitive regular expression
    #// comparisons. Default is ''.
    #// @type string $value       Meta value to filter by.
    #// @type string $compare     MySQL operator used for comparing the $value. Accepts '=',
    #// '!=', '>', '>=', '<', '<=', 'LIKE', 'NOT LIKE',
    #// 'IN', 'NOT IN', 'BETWEEN', 'NOT BETWEEN', 'REGEXP',
    #// 'NOT REGEXP', 'RLIKE', 'EXISTS' or 'NOT EXISTS'.
    #// Default is 'IN' when `$value` is an array, '=' otherwise.
    #// @type string $type        MySQL data type that the meta_value column will be CAST to for
    #// comparisons. Accepts 'NUMERIC', 'BINARY', 'CHAR', 'DATE',
    #// 'DATETIME', 'DECIMAL', 'SIGNED', 'TIME', or 'UNSIGNED'.
    #// Default is 'CHAR'.
    #// }
    #// }
    #//
    def __init__(self, meta_query_=None):
        if meta_query_ is None:
            meta_query_ = False
        # end if
        
        if (not meta_query_):
            return
        # end if
        if (php_isset(lambda : meta_query_["relation"])) and php_strtoupper(meta_query_["relation"]) == "OR":
            self.relation = "OR"
        else:
            self.relation = "AND"
        # end if
        self.queries = self.sanitize_query(meta_query_)
    # end def __init__
    #// 
    #// Ensure the 'meta_query' argument passed to the class constructor is well-formed.
    #// 
    #// Eliminates empty items and ensures that a 'relation' is set.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array $queries Array of query clauses.
    #// @return array Sanitized array of query clauses.
    #//
    def sanitize_query(self, queries_=None):
        
        
        clean_queries_ = Array()
        if (not php_is_array(queries_)):
            return clean_queries_
        # end if
        for key_,query_ in queries_:
            if "relation" == key_:
                relation_ = query_
            elif (not php_is_array(query_)):
                continue
                pass
            elif self.is_first_order_clause(query_):
                if (php_isset(lambda : query_["value"])) and Array() == query_["value"]:
                    query_["value"] = None
                # end if
                clean_queries_[key_] = query_
                pass
            else:
                cleaned_query_ = self.sanitize_query(query_)
                if (not php_empty(lambda : cleaned_query_)):
                    clean_queries_[key_] = cleaned_query_
                # end if
            # end if
        # end for
        if php_empty(lambda : clean_queries_):
            return clean_queries_
        # end if
        #// Sanitize the 'relation' key provided in the query.
        if (php_isset(lambda : relation_)) and "OR" == php_strtoupper(relation_):
            clean_queries_["relation"] = "OR"
            self.has_or_relation = True
            pass
        elif 1 == php_count(clean_queries_):
            clean_queries_["relation"] = "OR"
            pass
        else:
            clean_queries_["relation"] = "AND"
        # end if
        return clean_queries_
    # end def sanitize_query
    #// 
    #// Determine whether a query clause is first-order.
    #// 
    #// A first-order meta query clause is one that has either a 'key' or
    #// a 'value' array key.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array $query Meta query arguments.
    #// @return bool Whether the query clause is a first-order clause.
    #//
    def is_first_order_clause(self, query_=None):
        
        
        return (php_isset(lambda : query_["key"])) or (php_isset(lambda : query_["value"]))
    # end def is_first_order_clause
    #// 
    #// Constructs a meta query based on 'meta_*' query vars
    #// 
    #// @since 3.2.0
    #// 
    #// @param array $qv The query variables
    #//
    def parse_query_vars(self, qv_=None):
        
        
        meta_query_ = Array()
        #// 
        #// For orderby=meta_value to work correctly, simple query needs to be
        #// first (so that its table join is against an unaliased meta table) and
        #// needs to be its own clause (so it doesn't interfere with the logic of
        #// the rest of the meta_query).
        #//
        primary_meta_query_ = Array()
        for key_ in Array("key", "compare", "type", "compare_key", "type_key"):
            if (not php_empty(lambda : qv_[str("meta_") + str(key_)])):
                primary_meta_query_[key_] = qv_[str("meta_") + str(key_)]
            # end if
        # end for
        #// WP_Query sets 'meta_value' = '' by default.
        if (php_isset(lambda : qv_["meta_value"])) and "" != qv_["meta_value"] and (not php_is_array(qv_["meta_value"])) or qv_["meta_value"]:
            primary_meta_query_["value"] = qv_["meta_value"]
        # end if
        existing_meta_query_ = qv_["meta_query"] if (php_isset(lambda : qv_["meta_query"])) and php_is_array(qv_["meta_query"]) else Array()
        if (not php_empty(lambda : primary_meta_query_)) and (not php_empty(lambda : existing_meta_query_)):
            meta_query_ = Array({"relation": "AND"}, primary_meta_query_, existing_meta_query_)
        elif (not php_empty(lambda : primary_meta_query_)):
            meta_query_ = Array(primary_meta_query_)
        elif (not php_empty(lambda : existing_meta_query_)):
            meta_query_ = existing_meta_query_
        # end if
        self.__init__(meta_query_)
    # end def parse_query_vars
    #// 
    #// Return the appropriate alias for the given meta type if applicable.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $type MySQL type to cast meta_value.
    #// @return string MySQL type.
    #//
    def get_cast_for_type(self, type_=""):
        
        
        if php_empty(lambda : type_):
            return "CHAR"
        # end if
        meta_type_ = php_strtoupper(type_)
        if (not php_preg_match("/^(?:BINARY|CHAR|DATE|DATETIME|SIGNED|UNSIGNED|TIME|NUMERIC(?:\\(\\d+(?:,\\s?\\d+)?\\))?|DECIMAL(?:\\(\\d+(?:,\\s?\\d+)?\\))?)$/", meta_type_)):
            return "CHAR"
        # end if
        if "NUMERIC" == meta_type_:
            meta_type_ = "SIGNED"
        # end if
        return meta_type_
    # end def get_cast_for_type
    #// 
    #// Generates SQL clauses to be appended to a main query.
    #// 
    #// @since 3.2.0
    #// 
    #// @param string $type              Type of meta, eg 'user', 'post'.
    #// @param string $primary_table     Database table where the object being filtered is stored (eg wp_users).
    #// @param string $primary_id_column ID column for the filtered object in $primary_table.
    #// @param object $context           Optional. The main query object.
    #// @return array|false {
    #// Array containing JOIN and WHERE SQL clauses to append to the main query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql(self, type_=None, primary_table_=None, primary_id_column_=None, context_=None):
        
        
        meta_table_ = _get_meta_table(type_)
        if (not meta_table_):
            return False
        # end if
        self.table_aliases = Array()
        self.meta_table = meta_table_
        self.meta_id_column = sanitize_key(type_ + "_id")
        self.primary_table = primary_table_
        self.primary_id_column = primary_id_column_
        sql_ = self.get_sql_clauses()
        #// 
        #// If any JOINs are LEFT JOINs (as in the case of NOT EXISTS), then all JOINs should
        #// be LEFT. Otherwise posts with no metadata will be excluded from results.
        #//
        if False != php_strpos(sql_["join"], "LEFT JOIN"):
            sql_["join"] = php_str_replace("INNER JOIN", "LEFT JOIN", sql_["join"])
        # end if
        #// 
        #// Filters the meta query's generated SQL.
        #// 
        #// @since 3.1.0
        #// 
        #// @param array  $sql               Array containing the query's JOIN and WHERE clauses.
        #// @param array  $queries           Array of meta queries.
        #// @param string $type              Type of meta.
        #// @param string $primary_table     Primary table.
        #// @param string $primary_id_column Primary column ID.
        #// @param object $context           The main query object.
        #//
        return apply_filters_ref_array("get_meta_sql", Array(sql_, self.queries, type_, primary_table_, primary_id_column_, context_))
    # end def get_sql
    #// 
    #// Generate SQL clauses to be appended to a main query.
    #// 
    #// Called by the public WP_Meta_Query::get_sql(), this method is abstracted
    #// out to maintain parity with the other Query classes.
    #// 
    #// @since 4.1.0
    #// 
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to the main query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_clauses(self):
        
        
        #// 
        #// $queries are passed by reference to get_sql_for_query() for recursion.
        #// To keep $this->queries unaltered, pass a copy.
        #//
        queries_ = self.queries
        sql_ = self.get_sql_for_query(queries_)
        if (not php_empty(lambda : sql_["where"])):
            sql_["where"] = " AND " + sql_["where"]
        # end if
        return sql_
    # end def get_sql_clauses
    #// 
    #// Generate SQL clauses for a single query array.
    #// 
    #// If nested subqueries are found, this method recurses the tree to
    #// produce the properly nested SQL.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array $query Query to parse (passed by reference).
    #// @param int   $depth Optional. Number of tree levels deep we currently are.
    #// Used to calculate indentation. Default 0.
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to a single query array.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_for_query(self, query_=None, depth_=0):
        
        
        sql_chunks_ = Array({"join": Array(), "where": Array()})
        sql_ = Array({"join": "", "where": ""})
        indent_ = ""
        i_ = 0
        while i_ < depth_:
            
            indent_ += "  "
            i_ += 1
        # end while
        for key_,clause_ in query_:
            if "relation" == key_:
                relation_ = query_["relation"]
            elif php_is_array(clause_):
                #// This is a first-order clause.
                if self.is_first_order_clause(clause_):
                    clause_sql_ = self.get_sql_for_clause(clause_, query_, key_)
                    where_count_ = php_count(clause_sql_["where"])
                    if (not where_count_):
                        sql_chunks_["where"][-1] = ""
                    elif 1 == where_count_:
                        sql_chunks_["where"][-1] = clause_sql_["where"][0]
                    else:
                        sql_chunks_["where"][-1] = "( " + php_implode(" AND ", clause_sql_["where"]) + " )"
                    # end if
                    sql_chunks_["join"] = php_array_merge(sql_chunks_["join"], clause_sql_["join"])
                    pass
                else:
                    clause_sql_ = self.get_sql_for_query(clause_, depth_ + 1)
                    sql_chunks_["where"][-1] = clause_sql_["where"]
                    sql_chunks_["join"][-1] = clause_sql_["join"]
                # end if
            # end if
        # end for
        #// Filter to remove empties.
        sql_chunks_["join"] = php_array_filter(sql_chunks_["join"])
        sql_chunks_["where"] = php_array_filter(sql_chunks_["where"])
        if php_empty(lambda : relation_):
            relation_ = "AND"
        # end if
        #// Filter duplicate JOIN clauses and combine into a single string.
        if (not php_empty(lambda : sql_chunks_["join"])):
            sql_["join"] = php_implode(" ", array_unique(sql_chunks_["join"]))
        # end if
        #// Generate a single WHERE clause with proper brackets and indentation.
        if (not php_empty(lambda : sql_chunks_["where"])):
            sql_["where"] = "( " + "\n  " + indent_ + php_implode(" " + "\n  " + indent_ + relation_ + " " + "\n  " + indent_, sql_chunks_["where"]) + "\n" + indent_ + ")"
        # end if
        return sql_
    # end def get_sql_for_query
    #// 
    #// Generate SQL JOIN and WHERE clauses for a first-order query clause.
    #// 
    #// "First-order" means that it's an array with a 'key' or 'value'.
    #// 
    #// @since 4.1.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param array  $clause       Query clause (passed by reference).
    #// @param array  $parent_query Parent query array.
    #// @param string $clause_key   Optional. The array key used to name the clause in the original `$meta_query`
    #// parameters. If not provided, a key will be generated automatically.
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to a first-order query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_for_clause(self, clause_=None, parent_query_=None, clause_key_=""):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        sql_chunks_ = Array({"where": Array(), "join": Array()})
        if (php_isset(lambda : clause_["compare"])):
            clause_["compare"] = php_strtoupper(clause_["compare"])
        else:
            clause_["compare"] = "IN" if (php_isset(lambda : clause_["value"])) and php_is_array(clause_["value"]) else "="
        # end if
        non_numeric_operators_ = Array("=", "!=", "LIKE", "NOT LIKE", "IN", "NOT IN", "EXISTS", "NOT EXISTS", "RLIKE", "REGEXP", "NOT REGEXP")
        numeric_operators_ = Array(">", ">=", "<", "<=", "BETWEEN", "NOT BETWEEN")
        if (not php_in_array(clause_["compare"], non_numeric_operators_, True)) and (not php_in_array(clause_["compare"], numeric_operators_, True)):
            clause_["compare"] = "="
        # end if
        if (php_isset(lambda : clause_["compare_key"])):
            clause_["compare_key"] = php_strtoupper(clause_["compare_key"])
        else:
            clause_["compare_key"] = "IN" if (php_isset(lambda : clause_["key"])) and php_is_array(clause_["key"]) else "="
        # end if
        if (not php_in_array(clause_["compare_key"], non_numeric_operators_, True)):
            clause_["compare_key"] = "="
        # end if
        meta_compare_ = clause_["compare"]
        meta_compare_key_ = clause_["compare_key"]
        #// First build the JOIN clause, if one is required.
        join_ = ""
        #// We prefer to avoid joins if possible. Look for an existing join compatible with this clause.
        alias_ = self.find_compatible_table_alias(clause_, parent_query_)
        if False == alias_:
            i_ = php_count(self.table_aliases)
            alias_ = "mt" + i_ if i_ else self.meta_table
            #// JOIN clauses for NOT EXISTS have their own syntax.
            if "NOT EXISTS" == meta_compare_:
                join_ += str(" LEFT JOIN ") + str(self.meta_table)
                join_ += str(" AS ") + str(alias_) if i_ else ""
                if "LIKE" == meta_compare_key_:
                    join_ += wpdb_.prepare(str(" ON (") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias_) + str(".") + str(self.meta_id_column) + str(" AND ") + str(alias_) + str(".meta_key LIKE %s )"), "%" + wpdb_.esc_like(clause_["key"]) + "%")
                else:
                    join_ += wpdb_.prepare(str(" ON (") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias_) + str(".") + str(self.meta_id_column) + str(" AND ") + str(alias_) + str(".meta_key = %s )"), clause_["key"])
                # end if
                pass
            else:
                join_ += str(" INNER JOIN ") + str(self.meta_table)
                join_ += str(" AS ") + str(alias_) if i_ else ""
                join_ += str(" ON ( ") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias_) + str(".") + str(self.meta_id_column) + str(" )")
            # end if
            self.table_aliases[-1] = alias_
            sql_chunks_["join"][-1] = join_
        # end if
        #// Save the alias to this clause, for future siblings to find.
        clause_["alias"] = alias_
        #// Determine the data type.
        _meta_type_ = clause_["type"] if (php_isset(lambda : clause_["type"])) else ""
        meta_type_ = self.get_cast_for_type(_meta_type_)
        clause_["cast"] = meta_type_
        #// Fallback for clause keys is the table alias. Key must be a string.
        if php_is_int(clause_key_) or (not clause_key_):
            clause_key_ = clause_["alias"]
        # end if
        #// Ensure unique clause keys, so none are overwritten.
        iterator_ = 1
        clause_key_base_ = clause_key_
        while True:
            
            if not ((php_isset(lambda : self.clauses[clause_key_]))):
                break
            # end if
            clause_key_ = clause_key_base_ + "-" + iterator_
            iterator_ += 1
        # end while
        #// Store the clause in our flat array.
        self.clauses[clause_key_] = clause_
        #// Next, build the WHERE clause.
        #// meta_key.
        if php_array_key_exists("key", clause_):
            if "NOT EXISTS" == meta_compare_:
                sql_chunks_["where"][-1] = alias_ + "." + self.meta_id_column + " IS NULL"
            else:
                #// 
                #// In joined clauses negative operators have to be nested into a
                #// NOT EXISTS clause and flipped, to avoid returning records with
                #// matching post IDs but different meta keys. Here we prepare the
                #// nested clause.
                #//
                if php_in_array(meta_compare_key_, Array("!=", "NOT IN", "NOT LIKE", "NOT EXISTS", "NOT REGEXP"), True):
                    #// Negative clauses may be reused.
                    i_ = php_count(self.table_aliases)
                    subquery_alias_ = "mt" + i_ if i_ else self.meta_table
                    self.table_aliases[-1] = subquery_alias_
                    meta_compare_string_start_ = "NOT EXISTS ("
                    meta_compare_string_start_ += str("SELECT 1 FROM ") + str(wpdb_.postmeta) + str(" ") + str(subquery_alias_) + str(" ")
                    meta_compare_string_start_ += str("WHERE ") + str(subquery_alias_) + str(".post_ID = ") + str(alias_) + str(".post_ID ")
                    meta_compare_string_end_ = "LIMIT 1"
                    meta_compare_string_end_ += ")"
                # end if
                for case in Switch(meta_compare_key_):
                    if case("="):
                        pass
                    # end if
                    if case("EXISTS"):
                        where_ = wpdb_.prepare(str(alias_) + str(".meta_key = %s"), php_trim(clause_["key"]))
                        break
                    # end if
                    if case("LIKE"):
                        meta_compare_value_ = "%" + wpdb_.esc_like(php_trim(clause_["key"])) + "%"
                        where_ = wpdb_.prepare(str(alias_) + str(".meta_key LIKE %s"), meta_compare_value_)
                        break
                    # end if
                    if case("IN"):
                        meta_compare_string_ = str(alias_) + str(".meta_key IN (") + php_substr(php_str_repeat(",%s", php_count(clause_["key"])), 1) + ")"
                        where_ = wpdb_.prepare(meta_compare_string_, clause_["key"])
                        break
                    # end if
                    if case("RLIKE"):
                        pass
                    # end if
                    if case("REGEXP"):
                        operator_ = meta_compare_key_
                        if (php_isset(lambda : clause_["type_key"])) and "BINARY" == php_strtoupper(clause_["type_key"]):
                            cast_ = "BINARY"
                        else:
                            cast_ = ""
                        # end if
                        where_ = wpdb_.prepare(str(alias_) + str(".meta_key ") + str(operator_) + str(" ") + str(cast_) + str(" %s"), php_trim(clause_["key"]))
                        break
                    # end if
                    if case("!="):
                        pass
                    # end if
                    if case("NOT EXISTS"):
                        meta_compare_string_ = meta_compare_string_start_ + str("AND ") + str(subquery_alias_) + str(".meta_key = %s ") + meta_compare_string_end_
                        where_ = wpdb_.prepare(meta_compare_string_, clause_["key"])
                        break
                    # end if
                    if case("NOT LIKE"):
                        meta_compare_string_ = meta_compare_string_start_ + str("AND ") + str(subquery_alias_) + str(".meta_key LIKE %s ") + meta_compare_string_end_
                        meta_compare_value_ = "%" + wpdb_.esc_like(php_trim(clause_["key"])) + "%"
                        where_ = wpdb_.prepare(meta_compare_string_, meta_compare_value_)
                        break
                    # end if
                    if case("NOT IN"):
                        array_subclause_ = "(" + php_substr(php_str_repeat(",%s", php_count(clause_["key"])), 1) + ") "
                        meta_compare_string_ = meta_compare_string_start_ + str("AND ") + str(subquery_alias_) + str(".meta_key IN ") + array_subclause_ + meta_compare_string_end_
                        where_ = wpdb_.prepare(meta_compare_string_, clause_["key"])
                        break
                    # end if
                    if case("NOT REGEXP"):
                        operator_ = meta_compare_key_
                        if (php_isset(lambda : clause_["type_key"])) and "BINARY" == php_strtoupper(clause_["type_key"]):
                            cast_ = "BINARY"
                        else:
                            cast_ = ""
                        # end if
                        meta_compare_string_ = meta_compare_string_start_ + str("AND ") + str(subquery_alias_) + str(".meta_key REGEXP ") + str(cast_) + str(" %s ") + meta_compare_string_end_
                        where_ = wpdb_.prepare(meta_compare_string_, clause_["key"])
                        break
                    # end if
                # end for
                sql_chunks_["where"][-1] = where_
            # end if
        # end if
        #// meta_value.
        if php_array_key_exists("value", clause_):
            meta_value_ = clause_["value"]
            if php_in_array(meta_compare_, Array("IN", "NOT IN", "BETWEEN", "NOT BETWEEN")):
                if (not php_is_array(meta_value_)):
                    meta_value_ = php_preg_split("/[,\\s]+/", meta_value_)
                # end if
            else:
                meta_value_ = php_trim(meta_value_)
            # end if
            for case in Switch(meta_compare_):
                if case("IN"):
                    pass
                # end if
                if case("NOT IN"):
                    meta_compare_string_ = "(" + php_substr(php_str_repeat(",%s", php_count(meta_value_)), 1) + ")"
                    where_ = wpdb_.prepare(meta_compare_string_, meta_value_)
                    break
                # end if
                if case("BETWEEN"):
                    pass
                # end if
                if case("NOT BETWEEN"):
                    where_ = wpdb_.prepare("%s AND %s", meta_value_[0], meta_value_[1])
                    break
                # end if
                if case("LIKE"):
                    pass
                # end if
                if case("NOT LIKE"):
                    meta_value_ = "%" + wpdb_.esc_like(meta_value_) + "%"
                    where_ = wpdb_.prepare("%s", meta_value_)
                    break
                # end if
                if case("EXISTS"):
                    meta_compare_ = "="
                    where_ = wpdb_.prepare("%s", meta_value_)
                    break
                # end if
                if case("NOT EXISTS"):
                    where_ = ""
                    break
                # end if
                if case():
                    where_ = wpdb_.prepare("%s", meta_value_)
                    break
                # end if
            # end for
            if where_:
                if "CHAR" == meta_type_:
                    sql_chunks_["where"][-1] = str(alias_) + str(".meta_value ") + str(meta_compare_) + str(" ") + str(where_)
                else:
                    sql_chunks_["where"][-1] = str("CAST(") + str(alias_) + str(".meta_value AS ") + str(meta_type_) + str(") ") + str(meta_compare_) + str(" ") + str(where_)
                # end if
            # end if
        # end if
        #// 
        #// Multiple WHERE clauses (for meta_key and meta_value) should
        #// be joined in parentheses.
        #//
        if 1 < php_count(sql_chunks_["where"]):
            sql_chunks_["where"] = Array("( " + php_implode(" AND ", sql_chunks_["where"]) + " )")
        # end if
        return sql_chunks_
    # end def get_sql_for_clause
    #// 
    #// Get a flattened list of sanitized meta clauses.
    #// 
    #// This array should be used for clause lookup, as when the table alias and CAST type must be determined for
    #// a value of 'orderby' corresponding to a meta clause.
    #// 
    #// @since 4.2.0
    #// 
    #// @return array Meta clauses.
    #//
    def get_clauses(self):
        
        
        return self.clauses
    # end def get_clauses
    #// 
    #// Identify an existing table alias that is compatible with the current
    #// query clause.
    #// 
    #// We avoid unnecessary table joins by allowing each clause to look for
    #// an existing table alias that is compatible with the query that it
    #// needs to perform.
    #// 
    #// An existing alias is compatible if (a) it is a sibling of `$clause`
    #// (ie, it's under the scope of the same relation), and (b) the combination
    #// of operator and relation between the clauses allows for a shared table join.
    #// In the case of WP_Meta_Query, this only applies to 'IN' clauses that are
    #// connected by the relation 'OR'.
    #// 
    #// @since 4.1.0
    #// 
    #// @param  array       $clause       Query clause.
    #// @param  array       $parent_query Parent query of $clause.
    #// @return string|bool Table alias if found, otherwise false.
    #//
    def find_compatible_table_alias(self, clause_=None, parent_query_=None):
        
        
        alias_ = False
        for sibling_ in parent_query_:
            #// If the sibling has no alias yet, there's nothing to check.
            if php_empty(lambda : sibling_["alias"]):
                continue
            # end if
            #// We're only interested in siblings that are first-order clauses.
            if (not php_is_array(sibling_)) or (not self.is_first_order_clause(sibling_)):
                continue
            # end if
            compatible_compares_ = Array()
            #// Clauses connected by OR can share joins as long as they have "positive" operators.
            if "OR" == parent_query_["relation"]:
                compatible_compares_ = Array("=", "IN", "BETWEEN", "LIKE", "REGEXP", "RLIKE", ">", ">=", "<", "<=")
                pass
            elif (php_isset(lambda : sibling_["key"])) and (php_isset(lambda : clause_["key"])) and sibling_["key"] == clause_["key"]:
                compatible_compares_ = Array("!=", "NOT IN", "NOT LIKE")
            # end if
            clause_compare_ = php_strtoupper(clause_["compare"])
            sibling_compare_ = php_strtoupper(sibling_["compare"])
            if php_in_array(clause_compare_, compatible_compares_) and php_in_array(sibling_compare_, compatible_compares_):
                alias_ = sibling_["alias"]
                break
            # end if
        # end for
        #// 
        #// Filters the table alias identified as compatible with the current clause.
        #// 
        #// @since 4.1.0
        #// 
        #// @param string|bool   $alias        Table alias, or false if none was found.
        #// @param array         $clause       First-order query clause.
        #// @param array         $parent_query Parent of $clause.
        #// @param WP_Meta_Query $this         WP_Meta_Query object.
        #//
        return apply_filters("meta_query_find_compatible_table_alias", alias_, clause_, parent_query_, self)
    # end def find_compatible_table_alias
    #// 
    #// Checks whether the current query has any OR relations.
    #// 
    #// In some cases, the presence of an OR relation somewhere in the query will require
    #// the use of a `DISTINCT` or `GROUP BY` keyword in the `SELECT` clause. The current
    #// method can be used in these cases to determine whether such a clause is necessary.
    #// 
    #// @since 4.3.0
    #// 
    #// @return bool True if the query contains any `OR` relations, otherwise false.
    #//
    def has_or_relation(self):
        
        
        return self.has_or_relation
    # end def has_or_relation
# end class WP_Meta_Query
