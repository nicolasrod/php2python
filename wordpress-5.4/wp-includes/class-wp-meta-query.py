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
    queries = Array()
    relation = Array()
    meta_table = Array()
    meta_id_column = Array()
    primary_table = Array()
    primary_id_column = Array()
    table_aliases = Array()
    clauses = Array()
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
    def __init__(self, meta_query=False):
        
        if (not meta_query):
            return
        # end if
        if (php_isset(lambda : meta_query["relation"])) and php_strtoupper(meta_query["relation"]) == "OR":
            self.relation = "OR"
        else:
            self.relation = "AND"
        # end if
        self.queries = self.sanitize_query(meta_query)
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
    def sanitize_query(self, queries=None):
        
        clean_queries = Array()
        if (not php_is_array(queries)):
            return clean_queries
        # end if
        for key,query in queries:
            if "relation" == key:
                relation = query
            elif (not php_is_array(query)):
                continue
                pass
            elif self.is_first_order_clause(query):
                if (php_isset(lambda : query["value"])) and Array() == query["value"]:
                    query["value"] = None
                # end if
                clean_queries[key] = query
                pass
            else:
                cleaned_query = self.sanitize_query(query)
                if (not php_empty(lambda : cleaned_query)):
                    clean_queries[key] = cleaned_query
                # end if
            # end if
        # end for
        if php_empty(lambda : clean_queries):
            return clean_queries
        # end if
        #// Sanitize the 'relation' key provided in the query.
        if (php_isset(lambda : relation)) and "OR" == php_strtoupper(relation):
            clean_queries["relation"] = "OR"
            self.has_or_relation = True
            pass
        elif 1 == php_count(clean_queries):
            clean_queries["relation"] = "OR"
            pass
        else:
            clean_queries["relation"] = "AND"
        # end if
        return clean_queries
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
    def is_first_order_clause(self, query=None):
        
        return (php_isset(lambda : query["key"])) or (php_isset(lambda : query["value"]))
    # end def is_first_order_clause
    #// 
    #// Constructs a meta query based on 'meta_*' query vars
    #// 
    #// @since 3.2.0
    #// 
    #// @param array $qv The query variables
    #//
    def parse_query_vars(self, qv=None):
        
        meta_query = Array()
        #// 
        #// For orderby=meta_value to work correctly, simple query needs to be
        #// first (so that its table join is against an unaliased meta table) and
        #// needs to be its own clause (so it doesn't interfere with the logic of
        #// the rest of the meta_query).
        #//
        primary_meta_query = Array()
        for key in Array("key", "compare", "type", "compare_key", "type_key"):
            if (not php_empty(lambda : qv[str("meta_") + str(key)])):
                primary_meta_query[key] = qv[str("meta_") + str(key)]
            # end if
        # end for
        #// WP_Query sets 'meta_value' = '' by default.
        if (php_isset(lambda : qv["meta_value"])) and "" != qv["meta_value"] and (not php_is_array(qv["meta_value"])) or qv["meta_value"]:
            primary_meta_query["value"] = qv["meta_value"]
        # end if
        existing_meta_query = qv["meta_query"] if (php_isset(lambda : qv["meta_query"])) and php_is_array(qv["meta_query"]) else Array()
        if (not php_empty(lambda : primary_meta_query)) and (not php_empty(lambda : existing_meta_query)):
            meta_query = Array({"relation": "AND"}, primary_meta_query, existing_meta_query)
        elif (not php_empty(lambda : primary_meta_query)):
            meta_query = Array(primary_meta_query)
        elif (not php_empty(lambda : existing_meta_query)):
            meta_query = existing_meta_query
        # end if
        self.__init__(meta_query)
    # end def parse_query_vars
    #// 
    #// Return the appropriate alias for the given meta type if applicable.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $type MySQL type to cast meta_value.
    #// @return string MySQL type.
    #//
    def get_cast_for_type(self, type=""):
        
        if php_empty(lambda : type):
            return "CHAR"
        # end if
        meta_type = php_strtoupper(type)
        if (not php_preg_match("/^(?:BINARY|CHAR|DATE|DATETIME|SIGNED|UNSIGNED|TIME|NUMERIC(?:\\(\\d+(?:,\\s?\\d+)?\\))?|DECIMAL(?:\\(\\d+(?:,\\s?\\d+)?\\))?)$/", meta_type)):
            return "CHAR"
        # end if
        if "NUMERIC" == meta_type:
            meta_type = "SIGNED"
        # end if
        return meta_type
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
    def get_sql(self, type=None, primary_table=None, primary_id_column=None, context=None):
        
        meta_table = _get_meta_table(type)
        if (not meta_table):
            return False
        # end if
        self.table_aliases = Array()
        self.meta_table = meta_table
        self.meta_id_column = sanitize_key(type + "_id")
        self.primary_table = primary_table
        self.primary_id_column = primary_id_column
        sql = self.get_sql_clauses()
        #// 
        #// If any JOINs are LEFT JOINs (as in the case of NOT EXISTS), then all JOINs should
        #// be LEFT. Otherwise posts with no metadata will be excluded from results.
        #//
        if False != php_strpos(sql["join"], "LEFT JOIN"):
            sql["join"] = php_str_replace("INNER JOIN", "LEFT JOIN", sql["join"])
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
        return apply_filters_ref_array("get_meta_sql", Array(sql, self.queries, type, primary_table, primary_id_column, context))
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
        queries = self.queries
        sql = self.get_sql_for_query(queries)
        if (not php_empty(lambda : sql["where"])):
            sql["where"] = " AND " + sql["where"]
        # end if
        return sql
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
    def get_sql_for_query(self, query=None, depth=0):
        
        sql_chunks = Array({"join": Array(), "where": Array()})
        sql = Array({"join": "", "where": ""})
        indent = ""
        i = 0
        while i < depth:
            
            indent += "  "
            i += 1
        # end while
        for key,clause in query:
            if "relation" == key:
                relation = query["relation"]
            elif php_is_array(clause):
                #// This is a first-order clause.
                if self.is_first_order_clause(clause):
                    clause_sql = self.get_sql_for_clause(clause, query, key)
                    where_count = php_count(clause_sql["where"])
                    if (not where_count):
                        sql_chunks["where"][-1] = ""
                    elif 1 == where_count:
                        sql_chunks["where"][-1] = clause_sql["where"][0]
                    else:
                        sql_chunks["where"][-1] = "( " + php_implode(" AND ", clause_sql["where"]) + " )"
                    # end if
                    sql_chunks["join"] = php_array_merge(sql_chunks["join"], clause_sql["join"])
                    pass
                else:
                    clause_sql = self.get_sql_for_query(clause, depth + 1)
                    sql_chunks["where"][-1] = clause_sql["where"]
                    sql_chunks["join"][-1] = clause_sql["join"]
                # end if
            # end if
        # end for
        #// Filter to remove empties.
        sql_chunks["join"] = php_array_filter(sql_chunks["join"])
        sql_chunks["where"] = php_array_filter(sql_chunks["where"])
        if php_empty(lambda : relation):
            relation = "AND"
        # end if
        #// Filter duplicate JOIN clauses and combine into a single string.
        if (not php_empty(lambda : sql_chunks["join"])):
            sql["join"] = php_implode(" ", array_unique(sql_chunks["join"]))
        # end if
        #// Generate a single WHERE clause with proper brackets and indentation.
        if (not php_empty(lambda : sql_chunks["where"])):
            sql["where"] = "( " + "\n  " + indent + php_implode(" " + "\n  " + indent + relation + " " + "\n  " + indent, sql_chunks["where"]) + "\n" + indent + ")"
        # end if
        return sql
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
    def get_sql_for_clause(self, clause=None, parent_query=None, clause_key=""):
        
        global wpdb
        php_check_if_defined("wpdb")
        sql_chunks = Array({"where": Array(), "join": Array()})
        if (php_isset(lambda : clause["compare"])):
            clause["compare"] = php_strtoupper(clause["compare"])
        else:
            clause["compare"] = "IN" if (php_isset(lambda : clause["value"])) and php_is_array(clause["value"]) else "="
        # end if
        non_numeric_operators = Array("=", "!=", "LIKE", "NOT LIKE", "IN", "NOT IN", "EXISTS", "NOT EXISTS", "RLIKE", "REGEXP", "NOT REGEXP")
        numeric_operators = Array(">", ">=", "<", "<=", "BETWEEN", "NOT BETWEEN")
        if (not php_in_array(clause["compare"], non_numeric_operators, True)) and (not php_in_array(clause["compare"], numeric_operators, True)):
            clause["compare"] = "="
        # end if
        if (php_isset(lambda : clause["compare_key"])):
            clause["compare_key"] = php_strtoupper(clause["compare_key"])
        else:
            clause["compare_key"] = "IN" if (php_isset(lambda : clause["key"])) and php_is_array(clause["key"]) else "="
        # end if
        if (not php_in_array(clause["compare_key"], non_numeric_operators, True)):
            clause["compare_key"] = "="
        # end if
        meta_compare = clause["compare"]
        meta_compare_key = clause["compare_key"]
        #// First build the JOIN clause, if one is required.
        join = ""
        #// We prefer to avoid joins if possible. Look for an existing join compatible with this clause.
        alias = self.find_compatible_table_alias(clause, parent_query)
        if False == alias:
            i = php_count(self.table_aliases)
            alias = "mt" + i if i else self.meta_table
            #// JOIN clauses for NOT EXISTS have their own syntax.
            if "NOT EXISTS" == meta_compare:
                join += str(" LEFT JOIN ") + str(self.meta_table)
                join += str(" AS ") + str(alias) if i else ""
                if "LIKE" == meta_compare_key:
                    join += wpdb.prepare(str(" ON (") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias) + str(".") + str(self.meta_id_column) + str(" AND ") + str(alias) + str(".meta_key LIKE %s )"), "%" + wpdb.esc_like(clause["key"]) + "%")
                else:
                    join += wpdb.prepare(str(" ON (") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias) + str(".") + str(self.meta_id_column) + str(" AND ") + str(alias) + str(".meta_key = %s )"), clause["key"])
                # end if
                pass
            else:
                join += str(" INNER JOIN ") + str(self.meta_table)
                join += str(" AS ") + str(alias) if i else ""
                join += str(" ON ( ") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias) + str(".") + str(self.meta_id_column) + str(" )")
            # end if
            self.table_aliases[-1] = alias
            sql_chunks["join"][-1] = join
        # end if
        #// Save the alias to this clause, for future siblings to find.
        clause["alias"] = alias
        #// Determine the data type.
        _meta_type = clause["type"] if (php_isset(lambda : clause["type"])) else ""
        meta_type = self.get_cast_for_type(_meta_type)
        clause["cast"] = meta_type
        #// Fallback for clause keys is the table alias. Key must be a string.
        if php_is_int(clause_key) or (not clause_key):
            clause_key = clause["alias"]
        # end if
        #// Ensure unique clause keys, so none are overwritten.
        iterator = 1
        clause_key_base = clause_key
        while True:
            
            if not ((php_isset(lambda : self.clauses[clause_key]))):
                break
            # end if
            clause_key = clause_key_base + "-" + iterator
            iterator += 1
        # end while
        #// Store the clause in our flat array.
        self.clauses[clause_key] = clause
        #// Next, build the WHERE clause.
        #// meta_key.
        if php_array_key_exists("key", clause):
            if "NOT EXISTS" == meta_compare:
                sql_chunks["where"][-1] = alias + "." + self.meta_id_column + " IS NULL"
            else:
                #// 
                #// In joined clauses negative operators have to be nested into a
                #// NOT EXISTS clause and flipped, to avoid returning records with
                #// matching post IDs but different meta keys. Here we prepare the
                #// nested clause.
                #//
                if php_in_array(meta_compare_key, Array("!=", "NOT IN", "NOT LIKE", "NOT EXISTS", "NOT REGEXP"), True):
                    #// Negative clauses may be reused.
                    i = php_count(self.table_aliases)
                    subquery_alias = "mt" + i if i else self.meta_table
                    self.table_aliases[-1] = subquery_alias
                    meta_compare_string_start = "NOT EXISTS ("
                    meta_compare_string_start += str("SELECT 1 FROM ") + str(wpdb.postmeta) + str(" ") + str(subquery_alias) + str(" ")
                    meta_compare_string_start += str("WHERE ") + str(subquery_alias) + str(".post_ID = ") + str(alias) + str(".post_ID ")
                    meta_compare_string_end = "LIMIT 1"
                    meta_compare_string_end += ")"
                # end if
                for case in Switch(meta_compare_key):
                    if case("="):
                        pass
                    # end if
                    if case("EXISTS"):
                        where = wpdb.prepare(str(alias) + str(".meta_key = %s"), php_trim(clause["key"]))
                        break
                    # end if
                    if case("LIKE"):
                        meta_compare_value = "%" + wpdb.esc_like(php_trim(clause["key"])) + "%"
                        where = wpdb.prepare(str(alias) + str(".meta_key LIKE %s"), meta_compare_value)
                        break
                    # end if
                    if case("IN"):
                        meta_compare_string = str(alias) + str(".meta_key IN (") + php_substr(php_str_repeat(",%s", php_count(clause["key"])), 1) + ")"
                        where = wpdb.prepare(meta_compare_string, clause["key"])
                        break
                    # end if
                    if case("RLIKE"):
                        pass
                    # end if
                    if case("REGEXP"):
                        operator = meta_compare_key
                        if (php_isset(lambda : clause["type_key"])) and "BINARY" == php_strtoupper(clause["type_key"]):
                            cast = "BINARY"
                        else:
                            cast = ""
                        # end if
                        where = wpdb.prepare(str(alias) + str(".meta_key ") + str(operator) + str(" ") + str(cast) + str(" %s"), php_trim(clause["key"]))
                        break
                    # end if
                    if case("!="):
                        pass
                    # end if
                    if case("NOT EXISTS"):
                        meta_compare_string = meta_compare_string_start + str("AND ") + str(subquery_alias) + str(".meta_key = %s ") + meta_compare_string_end
                        where = wpdb.prepare(meta_compare_string, clause["key"])
                        break
                    # end if
                    if case("NOT LIKE"):
                        meta_compare_string = meta_compare_string_start + str("AND ") + str(subquery_alias) + str(".meta_key LIKE %s ") + meta_compare_string_end
                        meta_compare_value = "%" + wpdb.esc_like(php_trim(clause["key"])) + "%"
                        where = wpdb.prepare(meta_compare_string, meta_compare_value)
                        break
                    # end if
                    if case("NOT IN"):
                        array_subclause = "(" + php_substr(php_str_repeat(",%s", php_count(clause["key"])), 1) + ") "
                        meta_compare_string = meta_compare_string_start + str("AND ") + str(subquery_alias) + str(".meta_key IN ") + array_subclause + meta_compare_string_end
                        where = wpdb.prepare(meta_compare_string, clause["key"])
                        break
                    # end if
                    if case("NOT REGEXP"):
                        operator = meta_compare_key
                        if (php_isset(lambda : clause["type_key"])) and "BINARY" == php_strtoupper(clause["type_key"]):
                            cast = "BINARY"
                        else:
                            cast = ""
                        # end if
                        meta_compare_string = meta_compare_string_start + str("AND ") + str(subquery_alias) + str(".meta_key REGEXP ") + str(cast) + str(" %s ") + meta_compare_string_end
                        where = wpdb.prepare(meta_compare_string, clause["key"])
                        break
                    # end if
                # end for
                sql_chunks["where"][-1] = where
            # end if
        # end if
        #// meta_value.
        if php_array_key_exists("value", clause):
            meta_value = clause["value"]
            if php_in_array(meta_compare, Array("IN", "NOT IN", "BETWEEN", "NOT BETWEEN")):
                if (not php_is_array(meta_value)):
                    meta_value = php_preg_split("/[,\\s]+/", meta_value)
                # end if
            else:
                meta_value = php_trim(meta_value)
            # end if
            for case in Switch(meta_compare):
                if case("IN"):
                    pass
                # end if
                if case("NOT IN"):
                    meta_compare_string = "(" + php_substr(php_str_repeat(",%s", php_count(meta_value)), 1) + ")"
                    where = wpdb.prepare(meta_compare_string, meta_value)
                    break
                # end if
                if case("BETWEEN"):
                    pass
                # end if
                if case("NOT BETWEEN"):
                    where = wpdb.prepare("%s AND %s", meta_value[0], meta_value[1])
                    break
                # end if
                if case("LIKE"):
                    pass
                # end if
                if case("NOT LIKE"):
                    meta_value = "%" + wpdb.esc_like(meta_value) + "%"
                    where = wpdb.prepare("%s", meta_value)
                    break
                # end if
                if case("EXISTS"):
                    meta_compare = "="
                    where = wpdb.prepare("%s", meta_value)
                    break
                # end if
                if case("NOT EXISTS"):
                    where = ""
                    break
                # end if
                if case():
                    where = wpdb.prepare("%s", meta_value)
                    break
                # end if
            # end for
            if where:
                if "CHAR" == meta_type:
                    sql_chunks["where"][-1] = str(alias) + str(".meta_value ") + str(meta_compare) + str(" ") + str(where)
                else:
                    sql_chunks["where"][-1] = str("CAST(") + str(alias) + str(".meta_value AS ") + str(meta_type) + str(") ") + str(meta_compare) + str(" ") + str(where)
                # end if
            # end if
        # end if
        #// 
        #// Multiple WHERE clauses (for meta_key and meta_value) should
        #// be joined in parentheses.
        #//
        if 1 < php_count(sql_chunks["where"]):
            sql_chunks["where"] = Array("( " + php_implode(" AND ", sql_chunks["where"]) + " )")
        # end if
        return sql_chunks
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
    def find_compatible_table_alias(self, clause=None, parent_query=None):
        
        alias = False
        for sibling in parent_query:
            #// If the sibling has no alias yet, there's nothing to check.
            if php_empty(lambda : sibling["alias"]):
                continue
            # end if
            #// We're only interested in siblings that are first-order clauses.
            if (not php_is_array(sibling)) or (not self.is_first_order_clause(sibling)):
                continue
            # end if
            compatible_compares = Array()
            #// Clauses connected by OR can share joins as long as they have "positive" operators.
            if "OR" == parent_query["relation"]:
                compatible_compares = Array("=", "IN", "BETWEEN", "LIKE", "REGEXP", "RLIKE", ">", ">=", "<", "<=")
                pass
            elif (php_isset(lambda : sibling["key"])) and (php_isset(lambda : clause["key"])) and sibling["key"] == clause["key"]:
                compatible_compares = Array("!=", "NOT IN", "NOT LIKE")
            # end if
            clause_compare = php_strtoupper(clause["compare"])
            sibling_compare = php_strtoupper(sibling["compare"])
            if php_in_array(clause_compare, compatible_compares) and php_in_array(sibling_compare, compatible_compares):
                alias = sibling["alias"]
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
        return apply_filters("meta_query_find_compatible_table_alias", alias, clause, parent_query, self)
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
