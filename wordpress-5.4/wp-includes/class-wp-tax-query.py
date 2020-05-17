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
    #// 
    #// Array of taxonomy queries.
    #// 
    #// See WP_Tax_Query::__construct() for information on tax query arguments.
    #// 
    #// @since 3.1.0
    #// @var array
    #//
    queries = Array()
    #// 
    #// The relation between the queries. Can be one of 'AND' or 'OR'.
    #// 
    #// @since 3.1.0
    #// @var string
    #//
    relation = Array()
    #// 
    #// Standard response when the query should not return any rows.
    #// 
    #// @since 3.2.0
    #// @var string
    #//
    no_results = Array({"join": Array(""), "where": Array("0 = 1")})
    #// 
    #// A flat list of table aliases used in the JOIN clauses.
    #// 
    #// @since 4.1.0
    #// @var array
    #//
    table_aliases = Array()
    #// 
    #// Terms and taxonomies fetched by this query.
    #// 
    #// We store this data in a flat array because they are referenced in a
    #// number of places by WP_Query.
    #// 
    #// @since 4.1.0
    #// @var array
    #//
    queried_terms = Array()
    #// 
    #// Database table that where the metadata's objects are stored (eg $wpdb->users).
    #// 
    #// @since 4.1.0
    #// @var string
    #//
    primary_table = Array()
    #// 
    #// Column in 'primary_table' that represents the ID of the object.
    #// 
    #// @since 4.1.0
    #// @var string
    #//
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
    def __init__(self, tax_query_=None):
        
        
        if (php_isset(lambda : tax_query_["relation"])):
            self.relation = self.sanitize_relation(tax_query_["relation"])
        else:
            self.relation = "AND"
        # end if
        self.queries = self.sanitize_query(tax_query_)
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
    def sanitize_query(self, queries_=None):
        
        
        cleaned_query_ = Array()
        defaults_ = Array({"taxonomy": "", "terms": Array(), "field": "term_id", "operator": "IN", "include_children": True})
        for key_,query_ in queries_:
            if "relation" == key_:
                cleaned_query_["relation"] = self.sanitize_relation(query_)
                pass
            elif self.is_first_order_clause(query_):
                cleaned_clause_ = php_array_merge(defaults_, query_)
                cleaned_clause_["terms"] = cleaned_clause_["terms"]
                cleaned_query_[-1] = cleaned_clause_
                #// 
                #// Keep a copy of the clause in the flate
                #// $queried_terms array, for use in WP_Query.
                #//
                if (not php_empty(lambda : cleaned_clause_["taxonomy"])) and "NOT IN" != cleaned_clause_["operator"]:
                    taxonomy_ = cleaned_clause_["taxonomy"]
                    if (not (php_isset(lambda : self.queried_terms[taxonomy_]))):
                        self.queried_terms[taxonomy_] = Array()
                    # end if
                    #// 
                    #// Backward compatibility: Only store the first
                    #// 'terms' and 'field' found for a given taxonomy.
                    #//
                    if (not php_empty(lambda : cleaned_clause_["terms"])) and (not (php_isset(lambda : self.queried_terms[taxonomy_]["terms"]))):
                        self.queried_terms[taxonomy_]["terms"] = cleaned_clause_["terms"]
                    # end if
                    if (not php_empty(lambda : cleaned_clause_["field"])) and (not (php_isset(lambda : self.queried_terms[taxonomy_]["field"]))):
                        self.queried_terms[taxonomy_]["field"] = cleaned_clause_["field"]
                    # end if
                # end if
                pass
            elif php_is_array(query_):
                cleaned_subquery_ = self.sanitize_query(query_)
                if (not php_empty(lambda : cleaned_subquery_)):
                    #// All queries with children must have a relation.
                    if (not (php_isset(lambda : cleaned_subquery_["relation"]))):
                        cleaned_subquery_["relation"] = "AND"
                    # end if
                    cleaned_query_[-1] = cleaned_subquery_
                # end if
            # end if
        # end for
        return cleaned_query_
    # end def sanitize_query
    #// 
    #// Sanitize a 'relation' operator.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $relation Raw relation key from the query argument.
    #// @return string Sanitized relation ('AND' or 'OR').
    #//
    def sanitize_relation(self, relation_=None):
        
        
        if "OR" == php_strtoupper(relation_):
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
    def is_first_order_clause(self, query_=None):
        
        
        return php_is_array(query_) and php_empty(lambda : query_) or php_array_key_exists("terms", query_) or php_array_key_exists("taxonomy", query_) or php_array_key_exists("include_children", query_) or php_array_key_exists("field", query_) or php_array_key_exists("operator", query_)
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
    def get_sql(self, primary_table_=None, primary_id_column_=None):
        
        
        self.primary_table = primary_table_
        self.primary_id_column = primary_id_column_
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
                    clause_sql_ = self.get_sql_for_clause(clause_, query_)
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
    def get_sql_for_clause(self, clause_=None, parent_query_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        sql_ = Array({"where": Array(), "join": Array()})
        join_ = ""
        where_ = ""
        self.clean_query(clause_)
        if is_wp_error(clause_):
            return self.no_results
        # end if
        terms_ = clause_["terms"]
        operator_ = php_strtoupper(clause_["operator"])
        if "IN" == operator_:
            if php_empty(lambda : terms_):
                return self.no_results
            # end if
            terms_ = php_implode(",", terms_)
            #// 
            #// Before creating another table join, see if this clause has a
            #// sibling with an existing join that can be shared.
            #//
            alias_ = self.find_compatible_table_alias(clause_, parent_query_)
            if False == alias_:
                i_ = php_count(self.table_aliases)
                alias_ = "tt" + i_ if i_ else wpdb_.term_relationships
                #// Store the alias as part of a flat array to build future iterators.
                self.table_aliases[-1] = alias_
                #// Store the alias with this clause, so later siblings can use it.
                clause_["alias"] = alias_
                join_ += str(" LEFT JOIN ") + str(wpdb_.term_relationships)
                join_ += str(" AS ") + str(alias_) if i_ else ""
                join_ += str(" ON (") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" = ") + str(alias_) + str(".object_id)")
            # end if
            where_ = str(alias_) + str(".term_taxonomy_id ") + str(operator_) + str(" (") + str(terms_) + str(")")
        elif "NOT IN" == operator_:
            if php_empty(lambda : terms_):
                return sql_
            # end if
            terms_ = php_implode(",", terms_)
            where_ = str(self.primary_table) + str(".") + str(self.primary_id_column) + str(" NOT IN (\n                SELECT object_id\n              FROM ") + str(wpdb_.term_relationships) + str("\n               WHERE term_taxonomy_id IN (") + str(terms_) + str(")\n          )")
        elif "AND" == operator_:
            if php_empty(lambda : terms_):
                return sql_
            # end if
            num_terms_ = php_count(terms_)
            terms_ = php_implode(",", terms_)
            where_ = str("(\n               SELECT COUNT(1)\n               FROM ") + str(wpdb_.term_relationships) + str("\n               WHERE term_taxonomy_id IN (") + str(terms_) + str(")\n              AND object_id = ") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str("\n         ) = ") + str(num_terms_)
        elif "NOT EXISTS" == operator_ or "EXISTS" == operator_:
            where_ = wpdb_.prepare(str(operator_) + str(" (\n               SELECT 1\n              FROM ") + str(wpdb_.term_relationships) + str("\n               INNER JOIN ") + str(wpdb_.term_taxonomy) + str("\n              ON ") + str(wpdb_.term_taxonomy) + str(".term_taxonomy_id = ") + str(wpdb_.term_relationships) + str(".term_taxonomy_id\n               WHERE ") + str(wpdb_.term_taxonomy) + str(".taxonomy = %s\n             AND ") + str(wpdb_.term_relationships) + str(".object_id = ") + str(self.primary_table) + str(".") + str(self.primary_id_column) + str("\n          )"), clause_["taxonomy"])
        # end if
        sql_["join"][-1] = join_
        sql_["where"][-1] = where_
        return sql_
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
    def find_compatible_table_alias(self, clause_=None, parent_query_=None):
        
        
        alias_ = False
        #// Sanity check. Only IN queries use the JOIN syntax.
        if (not (php_isset(lambda : clause_["operator"]))) or "IN" != clause_["operator"]:
            return alias_
        # end if
        #// Since we're only checking IN queries, we're only concerned with OR relations.
        if (not (php_isset(lambda : parent_query_["relation"]))) or "OR" != parent_query_["relation"]:
            return alias_
        # end if
        compatible_operators_ = Array("IN")
        for sibling_ in parent_query_:
            if (not php_is_array(sibling_)) or (not self.is_first_order_clause(sibling_)):
                continue
            # end if
            if php_empty(lambda : sibling_["alias"]) or php_empty(lambda : sibling_["operator"]):
                continue
            # end if
            #// The sibling must both have compatible operator to share its alias.
            if php_in_array(php_strtoupper(sibling_["operator"]), compatible_operators_):
                alias_ = sibling_["alias"]
                break
            # end if
        # end for
        return alias_
    # end def find_compatible_table_alias
    #// 
    #// Validates a single query.
    #// 
    #// @since 3.2.0
    #// 
    #// @param array $query The single query. Passed by reference.
    #//
    def clean_query(self, query_=None):
        
        
        if php_empty(lambda : query_["taxonomy"]):
            if "term_taxonomy_id" != query_["field"]:
                query_ = php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
                return
            # end if
            #// So long as there are shared terms, 'include_children' requires that a taxonomy is set.
            query_["include_children"] = False
        elif (not taxonomy_exists(query_["taxonomy"])):
            query_ = php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
            return
        # end if
        query_["terms"] = array_unique(query_["terms"])
        if is_taxonomy_hierarchical(query_["taxonomy"]) and query_["include_children"]:
            self.transform_query(query_, "term_id")
            if is_wp_error(query_):
                return
            # end if
            children_ = Array()
            for term_ in query_["terms"]:
                children_ = php_array_merge(children_, get_term_children(term_, query_["taxonomy"]))
                children_[-1] = term_
            # end for
            query_["terms"] = children_
        # end if
        self.transform_query(query_, "term_taxonomy_id")
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
    def transform_query(self, query_=None, resulting_field_=None):
        
        
        if php_empty(lambda : query_["terms"]):
            return
        # end if
        if query_["field"] == resulting_field_:
            return
        # end if
        resulting_field_ = sanitize_key(resulting_field_)
        #// Empty 'terms' always results in a null transformation.
        terms_ = php_array_filter(query_["terms"])
        if php_empty(lambda : terms_):
            query_["terms"] = Array()
            query_["field"] = resulting_field_
            return
        # end if
        args_ = Array({"get": "all", "number": 0, "taxonomy": query_["taxonomy"], "update_term_meta_cache": False, "orderby": "none"})
        #// Term query parameter name depends on the 'field' being searched on.
        for case in Switch(query_["field"]):
            if case("slug"):
                args_["slug"] = terms_
                break
            # end if
            if case("name"):
                args_["name"] = terms_
                break
            # end if
            if case("term_taxonomy_id"):
                args_["term_taxonomy_id"] = terms_
                break
            # end if
            if case():
                args_["include"] = wp_parse_id_list(terms_)
                break
            # end if
        # end for
        term_query_ = php_new_class("WP_Term_Query", lambda : WP_Term_Query())
        term_list_ = term_query_.query(args_)
        if is_wp_error(term_list_):
            query_ = term_list_
            return
        # end if
        if "AND" == query_["operator"] and php_count(term_list_) < php_count(query_["terms"]):
            query_ = php_new_class("WP_Error", lambda : WP_Error("inexistent_terms", __("Inexistent terms.")))
            return
        # end if
        query_["terms"] = wp_list_pluck(term_list_, resulting_field_)
        query_["field"] = resulting_field_
    # end def transform_query
# end class WP_Tax_Query
