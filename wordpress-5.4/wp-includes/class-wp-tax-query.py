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
#// Taxonomy API: WP_Tax_Query class
#// 
#// @package WordPress
#// @subpackage Taxonomy
#// @since 4.4.0
#// 
#// 
#// Core class used to implement taxonomy queries for the Taxonomy API.
#// 
#// Used for generating SQL clauses that filter a primary query according to object
#// taxonomy terms.
#// 
#// WP_Tax_Query is a helper that allows primary query classes, such as WP_Query, to filter
#// their results by object metadata, by generating `JOIN` and `WHERE` subclauses to be
#// attached to the primary SQL query string.
#// 
#// @since 3.1.0
#//
class WP_Tax_Query():
    queries = Array()
    relation = Array()
    no_results = Array({"join": Array(""), "where": Array("0 = 1")})
    table_aliases = Array()
    queried_terms = Array()
    primary_table = Array()
    primary_id_column = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// @since 4.1.0 Added support for `$operator` 'NOT EXISTS' and 'EXISTS' values.
    #// 
    #// @param array $tax_query {
    #// Array of taxonomy query clauses.
    #// 
    #// @type string $relation Optional. The MySQL keyword used to join
    #// the clauses of the query. Accepts 'AND', or 'OR'. Default 'AND'.
    #// @type array {
    #// Optional. An array of first-order clause parameters, or another fully-formed tax query.
    #// 
    #// @type string           $taxonomy         Taxonomy being queried. Optional when field=term_taxonomy_id.
    #// @type string|int|array $terms            Term or terms to filter by.
    #// @type string           $field            Field to match $terms against. Accepts 'term_id', 'slug',
    #// 'name', or 'term_taxonomy_id'. Default: 'term_id'.
    #// @type string           $operator         MySQL operator to be used with $terms in the WHERE clause.
    #// Accepts 'AND', 'IN', 'NOT IN', 'EXISTS', 'NOT EXISTS'.
    #// Default: 'IN'.
    #// @type bool             $include_children Optional. Whether to include child terms.
    #// Requires a $taxonomy. Default: true.
    #// }
    #// }
    #//
    def __init__(self, tax_query=None):
        
        if (php_isset(lambda : tax_query["relation"])):
            self.relation = self.sanitize_relation(tax_query["relation"])
        else:
            self.relation = "AND"
        # end if
        self.queries = self.sanitize_query(tax_query)
    # end def __init__
    #// 
    #// Ensure the 'tax_query' argument passed to the class constructor is well-formed.
    #// 
    #// Ensures that each query-level clause has a 'relation' key, and that
    #// each first-order clause contains all the necessary keys from `$defaults`.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array $queries Array of queries clauses.
    #// @return array Sanitized array of query clauses.
    #//
    def sanitize_query(self, queries=None):
        
        cleaned_query = Array()
        defaults = Array({"taxonomy": "", "terms": Array(), "field": "term_id", "operator": "IN", "include_children": True})
        for key,query in queries:
            if "relation" == key:
                cleaned_query["relation"] = self.sanitize_relation(query)
                pass
            elif self.is_first_order_clause(query):
                cleaned_clause = php_array_merge(defaults, query)
                cleaned_clause["terms"] = cleaned_clause["terms"]
                cleaned_query[-1] = cleaned_clause
                #// 
                #// Keep a copy of the clause in the flate
                #// $queried_terms array, for use in WP_Query.
                #//
                if (not php_empty(lambda : cleaned_clause["taxonomy"])) and "NOT IN" != cleaned_clause["operator"]:
                    taxonomy = cleaned_clause["taxonomy"]
                    if (not (php_isset(lambda : self.queried_terms[taxonomy]))):
                        self.queried_terms[taxonomy] = Array()
                    # end if
                    #// 
                    #// Backward compatibility: Only store the first
                    #// 'terms' and 'field' found for a given taxonomy.
                    #//
                    if (not php_empty(lambda : cleaned_clause["terms"])) and (not (php_isset(lambda : self.queried_terms[taxonomy]["terms"]))):
                        self.queried_terms[taxonomy]["terms"] = cleaned_clause["terms"]
                    # end if
                    if (not php_empty(lambda : cleaned_clause["field"])) and (not (php_isset(lambda : self.queried_terms[taxonomy]["field"]))):
                        self.queried_terms[taxonomy]["field"] = cleaned_clause["field"]
                    # end if
                # end if
                pass
            elif php_is_array(query):
                cleaned_subquery = self.sanitize_query(query)
                if (not php_empty(lambda : cleaned_subquery)):
                    #// All queries with children must have a relation.
                    if (not (php_isset(lambda : cleaned_subquery["relation"]))):
                        cleaned_subquery["relation"] = "AND"
                    # end if
                    cleaned_query[-1] = cleaned_subquery
                # end if
            # end if
        # end for
        return cleaned_query
    # end def sanitize_query
    #// 
    #// Sanitize a 'relation' operator.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $relation Raw relation key from the query argument.
    #// @return string Sanitized relation ('AND' or 'OR').
    #//
    def sanitize_relation(self, relation=None):
        
        if "OR" == php_strtoupper(relation):
            return "OR"
        else:
            return "AND"
        # end if
    # end def sanitize_relation
    #// 
    #// Determine whether a clause is first-order.
    #// 
    #// A "first-order" clause is one that contains any of the first-order
    #// clause keys ('terms', 'taxonomy', 'include_children', 'field',
    #// 'operator'). An empty clause also counts as a first-order clause,
    #// for backward compatibility. Any clause that doesn't meet this is
    #// determined, by process of elimination, to be a higher-order query.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array $query Tax query arguments.
    #// @return bool Whether the query clause is a first-order clause.
    #//
    def is_first_order_clause(self, query=None):
        
        return php_is_array(query) and php_empty(lambda : query) or php_array_key_exists("terms", query) or php_array_key_exists("taxonomy", query) or php_array_key_exists("include_children", query) or php_array_key_exists("field", query) or php_array_key_exists("operator", query)
    # end def is_first_order_clause
    #// 
    #// Generates SQL clauses to be appended to a main query.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $primary_table     Database table where the object being filtered is stored (eg wp_users).
    #// @param string $primary_id_column ID column for the filtered object in $primary_table.
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to the main query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql(self, primary_table=None, primary_id_column=None):
        
        self.primary_table = primary_table
        self.primary_id_column = primary_id_column
        return self.get_sql_clauses()
    # end def get_sql
    #// 
    #// Generate SQL clauses to be appended to a main query.
    #// 
    #// Called by the public WP_Tax_Query::get_sql(), this method
    #// is abstracted out to maintain parity with the other Query classes.
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
                    clause_sql = self.get_sql_for_clause(clause, query)
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
    #// Generate SQL JOIN and WHERE clauses for a "first-order" query clause.
    #// 
    #// @since 4.1.0
    #// 
    #// @global wpdb $wpdb The WordPress database abstraction object.
    #// 
    #// @param array $clause       Query clause (passed by reference).
    #// @param array $parent_query Parent query array.
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to a first-order query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_for_clause(self, clause=None, parent_query=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        sql = Array({"where": Array(), "join": Array()})
        join = ""
        where = ""
        self.clean_query(clause)
        if is_wp_error(clause):
            return self.no_results
        # end if
        terms = clause["terms"]
        operator = php_strtoupper(clause["operator"])
        if "IN" == operator:
            if php_empty(lambda : terms):
                return self.no_results
            # end if
            terms = php_implode(",", terms)
            #// 
            #// Before creating another table join, see if this clause has a
            #// sibling with an existing join that can be shared.
            #//
            alias = self.find_compatible_table_alias(clause, parent_query)
            if False == alias:
                i = php_count(self.table_aliases)
                alias = "tt" + i if i else wpdb.term_relationships
                #// Store the alias as part of a flat array to build future iterators.
                self.table_aliases[-1] = alias
                #// Store the alias with this clause, so later siblings can use it.
                clause["alias"] = alias
                join += str(" LEFT JOIN ") + str(wpdb.term_relationships)
                join += str(" AS ") + str(alias) if i else ""
                join += str(" ON (") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias) + str(".object_id)")
            # end if
            where = str(alias) + str(".term_taxonomy_id ") + str(operator) + str(" (") + str(terms) + str(")")
        elif "NOT IN" == operator:
            if php_empty(lambda : terms):
                return sql
            # end if
            terms = php_implode(",", terms)
            where = str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" NOT IN (\n             SELECT object_id\n              FROM ") + str(wpdb.term_relationships) + str("\n                WHERE term_taxonomy_id IN (") + str(terms) + str(")\n           )")
        elif "AND" == operator:
            if php_empty(lambda : terms):
                return sql
            # end if
            num_terms = php_count(terms)
            terms = php_implode(",", terms)
            where = str("(\n                SELECT COUNT(1)\n               FROM ") + str(wpdb.term_relationships) + str("\n                WHERE term_taxonomy_id IN (") + str(terms) + str(")\n               AND object_id = ") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str("\n         ) = ") + str(num_terms)
        elif "NOT EXISTS" == operator or "EXISTS" == operator:
            where = wpdb.prepare(str(operator) + str(" (\n              SELECT 1\n              FROM ") + str(wpdb.term_relationships) + str("\n                INNER JOIN ") + str(wpdb.term_taxonomy) + str("\n               ON ") + str(wpdb.term_taxonomy) + str(".term_taxonomy_id = ") + str(wpdb.term_relationships) + str(".term_taxonomy_id\n             WHERE ") + str(wpdb.term_taxonomy) + str(".taxonomy = %s\n              AND ") + str(wpdb.term_relationships) + str(".object_id = ") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str("\n           )"), clause["taxonomy"])
        # end if
        sql["join"][-1] = join
        sql["where"][-1] = where
        return sql
    # end def get_sql_for_clause
    #// 
    #// Identify an existing table alias that is compatible with the current query clause.
    #// 
    #// We avoid unnecessary table joins by allowing each clause to look for
    #// an existing table alias that is compatible with the query that it
    #// needs to perform.
    #// 
    #// An existing alias is compatible if (a) it is a sibling of `$clause`
    #// (ie, it's under the scope of the same relation), and (b) the combination
    #// of operator and relation between the clauses allows for a shared table
    #// join. In the case of WP_Tax_Query, this only applies to 'IN'
    #// clauses that are connected by the relation 'OR'.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array       $clause       Query clause.
    #// @param array       $parent_query Parent query of $clause.
    #// @return string|false Table alias if found, otherwise false.
    #//
    def find_compatible_table_alias(self, clause=None, parent_query=None):
        
        alias = False
        #// Sanity check. Only IN queries use the JOIN syntax.
        if (not (php_isset(lambda : clause["operator"]))) or "IN" != clause["operator"]:
            return alias
        # end if
        #// Since we're only checking IN queries, we're only concerned with OR relations.
        if (not (php_isset(lambda : parent_query["relation"]))) or "OR" != parent_query["relation"]:
            return alias
        # end if
        compatible_operators = Array("IN")
        for sibling in parent_query:
            if (not php_is_array(sibling)) or (not self.is_first_order_clause(sibling)):
                continue
            # end if
            if php_empty(lambda : sibling["alias"]) or php_empty(lambda : sibling["operator"]):
                continue
            # end if
            #// The sibling must both have compatible operator to share its alias.
            if php_in_array(php_strtoupper(sibling["operator"]), compatible_operators):
                alias = sibling["alias"]
                break
            # end if
        # end for
        return alias
    # end def find_compatible_table_alias
    #// 
    #// Validates a single query.
    #// 
    #// @since 3.2.0
    #// 
    #// @param array $query The single query. Passed by reference.
    #//
    def clean_query(self, query=None):
        
        if php_empty(lambda : query["taxonomy"]):
            if "term_taxonomy_id" != query["field"]:
                query = php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
                return
            # end if
            #// So long as there are shared terms, 'include_children' requires that a taxonomy is set.
            query["include_children"] = False
        elif (not taxonomy_exists(query["taxonomy"])):
            query = php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
            return
        # end if
        query["terms"] = array_unique(query["terms"])
        if is_taxonomy_hierarchical(query["taxonomy"]) and query["include_children"]:
            self.transform_query(query, "term_id")
            if is_wp_error(query):
                return
            # end if
            children = Array()
            for term in query["terms"]:
                children = php_array_merge(children, get_term_children(term, query["taxonomy"]))
                children[-1] = term
            # end for
            query["terms"] = children
        # end if
        self.transform_query(query, "term_taxonomy_id")
    # end def clean_query
    #// 
    #// Transforms a single query, from one field to another.
    #// 
    #// Operates on the `$query` object by reference. In the case of error,
    #// `$query` is converted to a WP_Error object.
    #// 
    #// @since 3.2.0
    #// 
    #// @global wpdb $wpdb The WordPress database abstraction object.
    #// 
    #// @param array  $query           The single query. Passed by reference.
    #// @param string $resulting_field The resulting field. Accepts 'slug', 'name', 'term_taxonomy_id',
    #// or 'term_id'. Default 'term_id'.
    #//
    def transform_query(self, query=None, resulting_field=None):
        
        if php_empty(lambda : query["terms"]):
            return
        # end if
        if query["field"] == resulting_field:
            return
        # end if
        resulting_field = sanitize_key(resulting_field)
        #// Empty 'terms' always results in a null transformation.
        terms = php_array_filter(query["terms"])
        if php_empty(lambda : terms):
            query["terms"] = Array()
            query["field"] = resulting_field
            return
        # end if
        args = Array({"get": "all", "number": 0, "taxonomy": query["taxonomy"], "update_term_meta_cache": False, "orderby": "none"})
        #// Term query parameter name depends on the 'field' being searched on.
        for case in Switch(query["field"]):
            if case("slug"):
                args["slug"] = terms
                break
            # end if
            if case("name"):
                args["name"] = terms
                break
            # end if
            if case("term_taxonomy_id"):
                args["term_taxonomy_id"] = terms
                break
            # end if
            if case():
                args["include"] = wp_parse_id_list(terms)
                break
            # end if
        # end for
        term_query = php_new_class("WP_Term_Query", lambda : WP_Term_Query())
        term_list = term_query.query(args)
        if is_wp_error(term_list):
            query = term_list
            return
        # end if
        if "AND" == query["operator"] and php_count(term_list) < php_count(query["terms"]):
            query = php_new_class("WP_Error", lambda : WP_Error("inexistent_terms", __("Inexistent terms.")))
            return
        # end if
        query["terms"] = wp_list_pluck(term_list, resulting_field)
        query["field"] = resulting_field
    # end def transform_query
# end class WP_Tax_Query
