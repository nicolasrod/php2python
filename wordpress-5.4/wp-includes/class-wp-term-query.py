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
#// Taxonomy API: WP_Term_Query class.
#// 
#// @package WordPress
#// @subpackage Taxonomy
#// @since 4.6.0
#// 
#// 
#// Class used for querying terms.
#// 
#// @since 4.6.0
#// 
#// @see WP_Term_Query::__construct() for accepted arguments.
#//
class WP_Term_Query():
    #// 
    #// SQL string used to perform database query.
    #// 
    #// @since 4.6.0
    #// @var string
    #//
    request = Array()
    #// 
    #// Metadata query container.
    #// 
    #// @since 4.6.0
    #// @var object WP_Meta_Query
    #//
    meta_query = False
    #// 
    #// Metadata query clauses.
    #// 
    #// @since 4.6.0
    #// @var array
    #//
    meta_query_clauses = Array()
    #// 
    #// SQL query clauses.
    #// 
    #// @since 4.6.0
    #// @var array
    #//
    sql_clauses = Array({"select": "", "from": "", "where": Array(), "orderby": "", "limits": ""})
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
    #// List of terms located by the query.
    #// 
    #// @since 4.6.0
    #// @var array
    #//
    terms = Array()
    #// 
    #// Constructor.
    #// 
    #// Sets up the term query, based on the query vars passed.
    #// 
    #// @since 4.6.0
    #// @since 4.6.0 Introduced 'term_taxonomy_id' parameter.
    #// @since 4.7.0 Introduced 'object_ids' parameter.
    #// @since 4.9.0 Added 'slug__in' support for 'orderby'.
    #// 
    #// @param string|array $query {
    #// Optional. Array or query string of term query parameters. Default empty.
    #// 
    #// @type string|array $taxonomy               Taxonomy name, or array of taxonomies, to which results should
    #// be limited.
    #// @type int|array    $object_ids             Optional. Object ID, or array of object IDs. Results will be
    #// limited to terms associated with these objects.
    #// @type string       $orderby                Field(s) to order terms by. Accepts term fields ('name',
    #// 'slug', 'term_group', 'term_id', 'id', 'description', 'parent'),
    #// 'count' for term taxonomy count, 'include' to match the
    #// 'order' of the $include param, 'slug__in' to match the
    #// 'order' of the $slug param, 'meta_value', 'meta_value_num',
    #// the value of `$meta_key`, the array keys of `$meta_query`, or
    #// 'none' to omit the ORDER BY clause. Defaults to 'name'.
    #// @type string       $order                  Whether to order terms in ascending or descending order.
    #// Accepts 'ASC' (ascending) or 'DESC' (descending).
    #// Default 'ASC'.
    #// @type bool|int     $hide_empty             Whether to hide terms not assigned to any posts. Accepts
    #// 1|true or 0|false. Default 1|true.
    #// @type array|string $include                Array or comma/space-separated string of term ids to include.
    #// Default empty array.
    #// @type array|string $exclude                Array or comma/space-separated string of term ids to exclude.
    #// If $include is non-empty, $exclude is ignored.
    #// Default empty array.
    #// @type array|string $exclude_tree           Array or comma/space-separated string of term ids to exclude
    #// along with all of their descendant terms. If $include is
    #// non-empty, $exclude_tree is ignored. Default empty array.
    #// @type int|string   $number                 Maximum number of terms to return. Accepts ''|0 (all) or any
    #// positive number. Default ''|0 (all). Note that $number may
    #// not return accurate results when coupled with $object_ids.
    #// See #41796 for details.
    #// @type int          $offset                 The number by which to offset the terms query. Default empty.
    #// @type string       $fields                 Term fields to query for. Accepts:
    #// - 'all' Returns an array of complete term objects (`WP_Term[]`).
    #// - 'all_with_object_id' Returns an array of term objects with the 'object_id'
    #// param (`WP_Term[]`). Works only when the `$object_ids` parameter is populated.
    #// - 'ids' Returns an array of term IDs (`int[]`).
    #// - 'tt_ids' Returns an array of term taxonomy IDs (`int[]`).
    #// - 'names' Returns an array of term names (`string[]`).
    #// - 'slugs' Returns an array of term slugs (`string[]`).
    #// - 'count' Returns the number of matching terms (`int`).
    #// - 'id=>parent' Returns an associative array of parent term IDs, keyed by term ID (`int[]`).
    #// - 'id=>name' Returns an associative array of term names, keyed by term ID (`string[]`).
    #// - 'id=>slug' Returns an associative array of term slugs, keyed by term ID (`string[]`).
    #// Default 'all'.
    #// @type bool         $count                  Whether to return a term count. Will take precedence over `$fields` if true.
    #// Default false.
    #// @type string|array $name                   Optional. Name or array of names to return term(s) for.
    #// Default empty.
    #// @type string|array $slug                   Optional. Slug or array of slugs to return term(s) for.
    #// Default empty.
    #// @type int|array    $term_taxonomy_id       Optional. Term taxonomy ID, or array of term taxonomy IDs,
    #// to match when querying terms.
    #// @type bool         $hierarchical           Whether to include terms that have non-empty descendants (even
    #// if $hide_empty is set to true). Default true.
    #// @type string       $search                 Search criteria to match terms. Will be SQL-formatted with
    #// wildcards before and after. Default empty.
    #// @type string       $name__like             Retrieve terms with criteria by which a term is LIKE
    #// `$name__like`. Default empty.
    #// @type string       $description__like      Retrieve terms where the description is LIKE
    #// `$description__like`. Default empty.
    #// @type bool         $pad_counts             Whether to pad the quantity of a term's children in the
    #// quantity of each term's "count" object variable.
    #// Default false.
    #// @type string       $get                    Whether to return terms regardless of ancestry or whether the
    #// terms are empty. Accepts 'all' or empty (disabled).
    #// Default empty.
    #// @type int          $child_of               Term ID to retrieve child terms of. If multiple taxonomies
    #// are passed, $child_of is ignored. Default 0.
    #// @type int|string   $parent                 Parent term ID to retrieve direct-child terms of.
    #// Default empty.
    #// @type bool         $childless              True to limit results to terms that have no children.
    #// This parameter has no effect on non-hierarchical taxonomies.
    #// Default false.
    #// @type string       $cache_domain           Unique cache key to be produced when this query is stored in
    #// an object cache. Default is 'core'.
    #// @type bool         $update_term_meta_cache Whether to prime meta caches for matched terms. Default true.
    #// @type array        $meta_query             Optional. Meta query clauses to limit retrieved terms by.
    #// See `WP_Meta_Query`. Default empty.
    #// @type string       $meta_key               Limit terms to those matching a specific metadata key.
    #// Can be used in conjunction with `$meta_value`. Default empty.
    #// @type string       $meta_value             Limit terms to those matching a specific metadata value.
    #// Usually used in conjunction with `$meta_key`. Default empty.
    #// @type string       $meta_type              MySQL data type that the `$meta_value` will be CAST to for
    #// comparisons. Default empty.
    #// @type string       $meta_compare           Comparison operator to test the 'meta_value'. Default empty.
    #// }
    #//
    def __init__(self, query_=""):
        
        
        self.query_var_defaults = Array({"taxonomy": None, "object_ids": None, "orderby": "name", "order": "ASC", "hide_empty": True, "include": Array(), "exclude": Array(), "exclude_tree": Array(), "number": "", "offset": "", "fields": "all", "count": False, "name": "", "slug": "", "term_taxonomy_id": "", "hierarchical": True, "search": "", "name__like": "", "description__like": "", "pad_counts": False, "get": "", "child_of": 0, "parent": "", "childless": False, "cache_domain": "core", "update_term_meta_cache": True, "meta_query": "", "meta_key": "", "meta_value": "", "meta_type": "", "meta_compare": ""})
        if (not php_empty(lambda : query_)):
            self.query(query_)
        # end if
    # end def __init__
    #// 
    #// Parse arguments passed to the term query with default query parameters.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|array $query WP_Term_Query arguments. See WP_Term_Query::__construct()
    #//
    def parse_query(self, query_=""):
        
        
        if php_empty(lambda : query_):
            query_ = self.query_vars
        # end if
        taxonomies_ = query_["taxonomy"] if (php_isset(lambda : query_["taxonomy"])) else None
        #// 
        #// Filters the terms query default arguments.
        #// 
        #// Use {@see 'get_terms_args'} to filter the passed arguments.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array    $defaults   An array of default get_terms() arguments.
        #// @param string[] $taxonomies An array of taxonomy names.
        #//
        self.query_var_defaults = apply_filters("get_terms_defaults", self.query_var_defaults, taxonomies_)
        query_ = wp_parse_args(query_, self.query_var_defaults)
        query_["number"] = absint(query_["number"])
        query_["offset"] = absint(query_["offset"])
        #// 'parent' overrides 'child_of'.
        if 0 < php_intval(query_["parent"]):
            query_["child_of"] = False
        # end if
        if "all" == query_["get"]:
            query_["childless"] = False
            query_["child_of"] = 0
            query_["hide_empty"] = 0
            query_["hierarchical"] = False
            query_["pad_counts"] = False
        # end if
        query_["taxonomy"] = taxonomies_
        self.query_vars = query_
        #// 
        #// Fires after term query vars have been parsed.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Term_Query $this Current instance of WP_Term_Query.
        #//
        do_action("parse_term_query", self)
    # end def parse_query
    #// 
    #// Sets up the query for retrieving terms.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|array $query Array or URL query string of parameters.
    #// @return array|int List of terms, or number of terms when 'count' is passed as a query var.
    #//
    def query(self, query_=None):
        
        
        self.query_vars = wp_parse_args(query_)
        return self.get_terms()
    # end def query
    #// 
    #// Get terms, based on query_vars.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @return array List of terms.
    #//
    def get_terms(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        self.parse_query(self.query_vars)
        args_ = self.query_vars
        #// Set up meta_query so it's available to 'pre_get_terms'.
        self.meta_query = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query())
        self.meta_query.parse_query_vars(args_)
        #// 
        #// Fires before terms are retrieved.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Term_Query $this Current instance of WP_Term_Query.
        #//
        do_action("pre_get_terms", self)
        taxonomies_ = args_["taxonomy"]
        #// Save queries by not crawling the tree in the case of multiple taxes or a flat tax.
        has_hierarchical_tax_ = False
        if taxonomies_:
            for _tax_ in taxonomies_:
                if is_taxonomy_hierarchical(_tax_):
                    has_hierarchical_tax_ = True
                # end if
            # end for
        else:
            #// When no taxonomies are provided, assume we have to descend the tree.
            has_hierarchical_tax_ = True
        # end if
        if (not has_hierarchical_tax_):
            args_["hierarchical"] = False
            args_["pad_counts"] = False
        # end if
        #// 'parent' overrides 'child_of'.
        if 0 < php_intval(args_["parent"]):
            args_["child_of"] = False
        # end if
        if "all" == args_["get"]:
            args_["childless"] = False
            args_["child_of"] = 0
            args_["hide_empty"] = 0
            args_["hierarchical"] = False
            args_["pad_counts"] = False
        # end if
        #// 
        #// Filters the terms query arguments.
        #// 
        #// @since 3.1.0
        #// 
        #// @param array    $args       An array of get_terms() arguments.
        #// @param string[] $taxonomies An array of taxonomy names.
        #//
        args_ = apply_filters("get_terms_args", args_, taxonomies_)
        #// Avoid the query if the queried parent/child_of term has no descendants.
        child_of_ = args_["child_of"]
        parent_ = args_["parent"]
        if child_of_:
            _parent_ = child_of_
        elif parent_:
            _parent_ = parent_
        else:
            _parent_ = False
        # end if
        if _parent_:
            in_hierarchy_ = False
            for _tax_ in taxonomies_:
                hierarchy_ = _get_term_hierarchy(_tax_)
                if (php_isset(lambda : hierarchy_[_parent_])):
                    in_hierarchy_ = True
                # end if
            # end for
            if (not in_hierarchy_):
                if "count" == args_["fields"]:
                    return 0
                else:
                    self.terms = Array()
                    return self.terms
                # end if
            # end if
        # end if
        #// 'term_order' is a legal sort order only when joining the relationship table.
        _orderby_ = self.query_vars["orderby"]
        if "term_order" == _orderby_ and php_empty(lambda : self.query_vars["object_ids"]):
            _orderby_ = "term_id"
        # end if
        orderby_ = self.parse_orderby(_orderby_)
        if orderby_:
            orderby_ = str("ORDER BY ") + str(orderby_)
        # end if
        order_ = self.parse_order(self.query_vars["order"])
        if taxonomies_:
            self.sql_clauses["where"]["taxonomy"] = "tt.taxonomy IN ('" + php_implode("', '", php_array_map("esc_sql", taxonomies_)) + "')"
        # end if
        exclude_ = args_["exclude"]
        exclude_tree_ = args_["exclude_tree"]
        include_ = args_["include"]
        inclusions_ = ""
        if (not php_empty(lambda : include_)):
            exclude_ = ""
            exclude_tree_ = ""
            inclusions_ = php_implode(",", wp_parse_id_list(include_))
        # end if
        if (not php_empty(lambda : inclusions_)):
            self.sql_clauses["where"]["inclusions"] = "t.term_id IN ( " + inclusions_ + " )"
        # end if
        exclusions_ = Array()
        if (not php_empty(lambda : exclude_tree_)):
            exclude_tree_ = wp_parse_id_list(exclude_tree_)
            excluded_children_ = exclude_tree_
            for extrunk_ in exclude_tree_:
                excluded_children_ = php_array_merge(excluded_children_, get_terms(Array({"taxonomy": reset(taxonomies_), "child_of": php_intval(extrunk_), "fields": "ids", "hide_empty": 0})))
            # end for
            exclusions_ = php_array_merge(excluded_children_, exclusions_)
        # end if
        if (not php_empty(lambda : exclude_)):
            exclusions_ = php_array_merge(wp_parse_id_list(exclude_), exclusions_)
        # end if
        #// 'childless' terms are those without an entry in the flattened term hierarchy.
        childless_ = php_bool(args_["childless"])
        if childless_:
            for _tax_ in taxonomies_:
                term_hierarchy_ = _get_term_hierarchy(_tax_)
                exclusions_ = php_array_merge(php_array_keys(term_hierarchy_), exclusions_)
            # end for
        # end if
        if (not php_empty(lambda : exclusions_)):
            exclusions_ = "t.term_id NOT IN (" + php_implode(",", php_array_map("intval", exclusions_)) + ")"
        else:
            exclusions_ = ""
        # end if
        #// 
        #// Filters the terms to exclude from the terms query.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string   $exclusions `NOT IN` clause of the terms query.
        #// @param array    $args       An array of terms query arguments.
        #// @param string[] $taxonomies An array of taxonomy names.
        #//
        exclusions_ = apply_filters("list_terms_exclusions", exclusions_, args_, taxonomies_)
        if (not php_empty(lambda : exclusions_)):
            #// Must do string manipulation here for backward compatibility with filter.
            self.sql_clauses["where"]["exclusions"] = php_preg_replace("/^\\s*AND\\s*/", "", exclusions_)
        # end if
        if (not php_empty(lambda : args_["name"])) or php_is_string(args_["name"]) and 0 != php_strlen(args_["name"]):
            names_ = args_["name"]
            for _name_ in names_:
                #// `sanitize_term_field()` returns slashed data.
                _name_ = stripslashes(sanitize_term_field("name", _name_, 0, reset(taxonomies_), "db"))
            # end for
            self.sql_clauses["where"]["name"] = "t.name IN ('" + php_implode("', '", php_array_map("esc_sql", names_)) + "')"
        # end if
        if (not php_empty(lambda : args_["slug"])) or php_is_string(args_["slug"]) and 0 != php_strlen(args_["slug"]):
            if php_is_array(args_["slug"]):
                slug_ = php_array_map("sanitize_title", args_["slug"])
                self.sql_clauses["where"]["slug"] = "t.slug IN ('" + php_implode("', '", slug_) + "')"
            else:
                slug_ = sanitize_title(args_["slug"])
                self.sql_clauses["where"]["slug"] = str("t.slug = '") + str(slug_) + str("'")
            # end if
        # end if
        if (not php_empty(lambda : args_["term_taxonomy_id"])):
            if php_is_array(args_["term_taxonomy_id"]):
                tt_ids_ = php_implode(",", php_array_map("intval", args_["term_taxonomy_id"]))
                self.sql_clauses["where"]["term_taxonomy_id"] = str("tt.term_taxonomy_id IN (") + str(tt_ids_) + str(")")
            else:
                self.sql_clauses["where"]["term_taxonomy_id"] = wpdb_.prepare("tt.term_taxonomy_id = %d", args_["term_taxonomy_id"])
            # end if
        # end if
        if (not php_empty(lambda : args_["name__like"])):
            self.sql_clauses["where"]["name__like"] = wpdb_.prepare("t.name LIKE %s", "%" + wpdb_.esc_like(args_["name__like"]) + "%")
        # end if
        if (not php_empty(lambda : args_["description__like"])):
            self.sql_clauses["where"]["description__like"] = wpdb_.prepare("tt.description LIKE %s", "%" + wpdb_.esc_like(args_["description__like"]) + "%")
        # end if
        if (not php_empty(lambda : args_["object_ids"])):
            object_ids_ = args_["object_ids"]
            if (not php_is_array(object_ids_)):
                object_ids_ = Array(object_ids_)
            # end if
            object_ids_ = php_implode(", ", php_array_map("intval", object_ids_))
            self.sql_clauses["where"]["object_ids"] = str("tr.object_id IN (") + str(object_ids_) + str(")")
        # end if
        #// 
        #// When querying for object relationships, the 'count > 0' check
        #// added by 'hide_empty' is superfluous.
        #//
        if (not php_empty(lambda : args_["object_ids"])):
            args_["hide_empty"] = False
        # end if
        if "" != parent_:
            parent_ = php_int(parent_)
            self.sql_clauses["where"]["parent"] = str("tt.parent = '") + str(parent_) + str("'")
        # end if
        hierarchical_ = args_["hierarchical"]
        if "count" == args_["fields"]:
            hierarchical_ = False
        # end if
        if args_["hide_empty"] and (not hierarchical_):
            self.sql_clauses["where"]["count"] = "tt.count > 0"
        # end if
        number_ = args_["number"]
        offset_ = args_["offset"]
        #// Don't limit the query results when we have to descend the family tree.
        if number_ and (not hierarchical_) and (not child_of_) and "" == parent_:
            if offset_:
                limits_ = "LIMIT " + offset_ + "," + number_
            else:
                limits_ = "LIMIT " + number_
            # end if
        else:
            limits_ = ""
        # end if
        if (not php_empty(lambda : args_["search"])):
            self.sql_clauses["where"]["search"] = self.get_search_sql(args_["search"])
        # end if
        #// Meta query support.
        join_ = ""
        distinct_ = ""
        #// Reparse meta_query query_vars, in case they were modified in a 'pre_get_terms' callback.
        self.meta_query.parse_query_vars(self.query_vars)
        mq_sql_ = self.meta_query.get_sql("term", "t", "term_id")
        meta_clauses_ = self.meta_query.get_clauses()
        if (not php_empty(lambda : meta_clauses_)):
            join_ += mq_sql_["join"]
            self.sql_clauses["where"]["meta_query"] = php_preg_replace("/^\\s*AND\\s*/", "", mq_sql_["where"])
            distinct_ += "DISTINCT"
        # end if
        selects_ = Array()
        for case in Switch(args_["fields"]):
            if case("all"):
                pass
            # end if
            if case("all_with_object_id"):
                pass
            # end if
            if case("tt_ids"):
                pass
            # end if
            if case("slugs"):
                selects_ = Array("t.*", "tt.*")
                if "all_with_object_id" == args_["fields"] and (not php_empty(lambda : args_["object_ids"])):
                    selects_[-1] = "tr.object_id"
                # end if
                break
            # end if
            if case("ids"):
                pass
            # end if
            if case("id=>parent"):
                selects_ = Array("t.term_id", "tt.parent", "tt.count", "tt.taxonomy")
                break
            # end if
            if case("names"):
                selects_ = Array("t.term_id", "tt.parent", "tt.count", "t.name", "tt.taxonomy")
                break
            # end if
            if case("count"):
                orderby_ = ""
                order_ = ""
                selects_ = Array("COUNT(*)")
                break
            # end if
            if case("id=>name"):
                selects_ = Array("t.term_id", "t.name", "tt.count", "tt.taxonomy")
                break
            # end if
            if case("id=>slug"):
                selects_ = Array("t.term_id", "t.slug", "tt.count", "tt.taxonomy")
                break
            # end if
        # end for
        _fields_ = args_["fields"]
        #// 
        #// Filters the fields to select in the terms query.
        #// 
        #// Field lists modified using this filter will only modify the term fields returned
        #// by the function when the `$fields` parameter set to 'count' or 'all'. In all other
        #// cases, the term fields in the results array will be determined by the `$fields`
        #// parameter alone.
        #// 
        #// Use of this filter can result in unpredictable behavior, and is not recommended.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $selects    An array of fields to select for the terms query.
        #// @param array    $args       An array of term query arguments.
        #// @param string[] $taxonomies An array of taxonomy names.
        #//
        fields_ = php_implode(", ", apply_filters("get_terms_fields", selects_, args_, taxonomies_))
        join_ += str(" INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" AS tt ON t.term_id = tt.term_id")
        if (not php_empty(lambda : self.query_vars["object_ids"])):
            join_ += str(" INNER JOIN ") + str(wpdb_.term_relationships) + str(" AS tr ON tr.term_taxonomy_id = tt.term_taxonomy_id")
        # end if
        where_ = php_implode(" AND ", self.sql_clauses["where"])
        #// 
        #// Filters the terms query SQL clauses.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[] $pieces     Array of query SQL clauses.
        #// @param string[] $taxonomies An array of taxonomy names.
        #// @param array    $args       An array of term query arguments.
        #//
        clauses_ = apply_filters("terms_clauses", php_compact("fields_", "join_", "where_", "distinct_", "orderby_", "order_", "limits_"), taxonomies_, args_)
        fields_ = clauses_["fields"] if (php_isset(lambda : clauses_["fields"])) else ""
        join_ = clauses_["join"] if (php_isset(lambda : clauses_["join"])) else ""
        where_ = clauses_["where"] if (php_isset(lambda : clauses_["where"])) else ""
        distinct_ = clauses_["distinct"] if (php_isset(lambda : clauses_["distinct"])) else ""
        orderby_ = clauses_["orderby"] if (php_isset(lambda : clauses_["orderby"])) else ""
        order_ = clauses_["order"] if (php_isset(lambda : clauses_["order"])) else ""
        limits_ = clauses_["limits"] if (php_isset(lambda : clauses_["limits"])) else ""
        if where_:
            where_ = str("WHERE ") + str(where_)
        # end if
        self.sql_clauses["select"] = str("SELECT ") + str(distinct_) + str(" ") + str(fields_)
        self.sql_clauses["from"] = str("FROM ") + str(wpdb_.terms) + str(" AS t ") + str(join_)
        self.sql_clauses["orderby"] = str(orderby_) + str(" ") + str(order_) if orderby_ else ""
        self.sql_clauses["limits"] = limits_
        self.request = str(self.sql_clauses["select"]) + str(" ") + str(self.sql_clauses["from"]) + str(" ") + str(where_) + str(" ") + str(self.sql_clauses["orderby"]) + str(" ") + str(self.sql_clauses["limits"])
        self.terms = None
        #// 
        #// Filter the terms array before the query takes place.
        #// 
        #// Return a non-null value to bypass WordPress's default term queries.
        #// 
        #// @since 5.3.0
        #// 
        #// @param array|null    $terms Return an array of term data to short-circuit WP's term query,
        #// or null to allow WP queries to run normally.
        #// @param WP_Term_Query $this  The WP_Term_Query instance, passed by reference.
        #// 
        #//
        self.terms = apply_filters_ref_array("terms_pre_query", Array(self.terms, self))
        if None != self.terms:
            return self.terms
        # end if
        #// $args can be anything. Only use the args defined in defaults to compute the key.
        key_ = php_md5(serialize(wp_array_slice_assoc(args_, php_array_keys(self.query_var_defaults))) + serialize(taxonomies_) + self.request)
        last_changed_ = wp_cache_get_last_changed("terms")
        cache_key_ = str("get_terms:") + str(key_) + str(":") + str(last_changed_)
        cache_ = wp_cache_get(cache_key_, "terms")
        if False != cache_:
            if "all" == _fields_ or "all_with_object_id" == _fields_:
                cache_ = self.populate_terms(cache_)
            # end if
            self.terms = cache_
            return self.terms
        # end if
        if "count" == _fields_:
            count_ = wpdb_.get_var(self.request)
            wp_cache_set(cache_key_, count_, "terms")
            return count_
        # end if
        terms_ = wpdb_.get_results(self.request)
        if "all" == _fields_ or "all_with_object_id" == _fields_:
            update_term_cache(terms_)
        # end if
        #// Prime termmeta cache.
        if args_["update_term_meta_cache"]:
            term_ids_ = wp_list_pluck(terms_, "term_id")
            update_termmeta_cache(term_ids_)
        # end if
        if php_empty(lambda : terms_):
            wp_cache_add(cache_key_, Array(), "terms", DAY_IN_SECONDS)
            return Array()
        # end if
        if child_of_:
            for _tax_ in taxonomies_:
                children_ = _get_term_hierarchy(_tax_)
                if (not php_empty(lambda : children_)):
                    terms_ = _get_term_children(child_of_, terms_, _tax_)
                # end if
            # end for
        # end if
        #// Update term counts to include children.
        if args_["pad_counts"] and "all" == _fields_:
            for _tax_ in taxonomies_:
                _pad_term_counts(terms_, _tax_)
            # end for
        # end if
        #// Make sure we show empty categories that have children.
        if hierarchical_ and args_["hide_empty"] and php_is_array(terms_):
            for k_,term_ in terms_.items():
                if (not term_.count):
                    children_ = get_term_children(term_.term_id, term_.taxonomy)
                    if php_is_array(children_):
                        for child_id_ in children_:
                            child_ = get_term(child_id_, term_.taxonomy)
                            if child_.count:
                                continue
                            # end if
                        # end for
                    # end if
                    terms_[k_] = None
                # end if
            # end for
        # end if
        #// 
        #// When querying for terms connected to objects, we may get
        #// duplicate results. The duplicates should be preserved if
        #// `$fields` is 'all_with_object_id', but should otherwise be
        #// removed.
        #//
        if (not php_empty(lambda : args_["object_ids"])) and "all_with_object_id" != _fields_:
            _tt_ids_ = Array()
            _terms_ = Array()
            for term_ in terms_:
                if (php_isset(lambda : _tt_ids_[term_.term_id])):
                    continue
                # end if
                _tt_ids_[term_.term_id] = 1
                _terms_[-1] = term_
            # end for
            terms_ = _terms_
        # end if
        _terms_ = Array()
        if "id=>parent" == _fields_:
            for term_ in terms_:
                _terms_[term_.term_id] = term_.parent
            # end for
        elif "ids" == _fields_:
            for term_ in terms_:
                _terms_[-1] = php_int(term_.term_id)
            # end for
        elif "tt_ids" == _fields_:
            for term_ in terms_:
                _terms_[-1] = php_int(term_.term_taxonomy_id)
            # end for
        elif "names" == _fields_:
            for term_ in terms_:
                _terms_[-1] = term_.name
            # end for
        elif "slugs" == _fields_:
            for term_ in terms_:
                _terms_[-1] = term_.slug
            # end for
        elif "id=>name" == _fields_:
            for term_ in terms_:
                _terms_[term_.term_id] = term_.name
            # end for
        elif "id=>slug" == _fields_:
            for term_ in terms_:
                _terms_[term_.term_id] = term_.slug
            # end for
        # end if
        if (not php_empty(lambda : _terms_)):
            terms_ = _terms_
        # end if
        #// Hierarchical queries are not limited, so 'offset' and 'number' must be handled now.
        if hierarchical_ and number_ and php_is_array(terms_):
            if offset_ >= php_count(terms_):
                terms_ = Array()
            else:
                terms_ = php_array_slice(terms_, offset_, number_, True)
            # end if
        # end if
        wp_cache_add(cache_key_, terms_, "terms", DAY_IN_SECONDS)
        if "all" == _fields_ or "all_with_object_id" == _fields_:
            terms_ = self.populate_terms(terms_)
        # end if
        self.terms = terms_
        return self.terms
    # end def get_terms
    #// 
    #// Parse and sanitize 'orderby' keys passed to the term query.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $orderby_raw Alias for the field to order by.
    #// @return string|false Value to used in the ORDER clause. False otherwise.
    #//
    def parse_orderby(self, orderby_raw_=None):
        
        
        _orderby_ = php_strtolower(orderby_raw_)
        maybe_orderby_meta_ = False
        if php_in_array(_orderby_, Array("term_id", "name", "slug", "term_group"), True):
            orderby_ = str("t.") + str(_orderby_)
        elif php_in_array(_orderby_, Array("count", "parent", "taxonomy", "term_taxonomy_id", "description"), True):
            orderby_ = str("tt.") + str(_orderby_)
        elif "term_order" == _orderby_:
            orderby_ = "tr.term_order"
        elif "include" == _orderby_ and (not php_empty(lambda : self.query_vars["include"])):
            include_ = php_implode(",", wp_parse_id_list(self.query_vars["include"]))
            orderby_ = str("FIELD( t.term_id, ") + str(include_) + str(" )")
        elif "slug__in" == _orderby_ and (not php_empty(lambda : self.query_vars["slug"])) and php_is_array(self.query_vars["slug"]):
            slugs_ = php_implode("', '", php_array_map("sanitize_title_for_query", self.query_vars["slug"]))
            orderby_ = "FIELD( t.slug, '" + slugs_ + "')"
        elif "none" == _orderby_:
            orderby_ = ""
        elif php_empty(lambda : _orderby_) or "id" == _orderby_ or "term_id" == _orderby_:
            orderby_ = "t.term_id"
        else:
            orderby_ = "t.name"
            #// This may be a value of orderby related to meta.
            maybe_orderby_meta_ = True
        # end if
        #// 
        #// Filters the ORDERBY clause of the terms query.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string   $orderby    `ORDERBY` clause of the terms query.
        #// @param array    $args       An array of term query arguments.
        #// @param string[] $taxonomies An array of taxonomy names.
        #//
        orderby_ = apply_filters("get_terms_orderby", orderby_, self.query_vars, self.query_vars["taxonomy"])
        #// Run after the 'get_terms_orderby' filter for backward compatibility.
        if maybe_orderby_meta_:
            maybe_orderby_meta_ = self.parse_orderby_meta(_orderby_)
            if maybe_orderby_meta_:
                orderby_ = maybe_orderby_meta_
            # end if
        # end if
        return orderby_
    # end def parse_orderby
    #// 
    #// Generate the ORDER BY clause for an 'orderby' param that is potentially related to a meta query.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $orderby_raw Raw 'orderby' value passed to WP_Term_Query.
    #// @return string ORDER BY clause.
    #//
    def parse_orderby_meta(self, orderby_raw_=None):
        
        
        orderby_ = ""
        #// Tell the meta query to generate its SQL, so we have access to table aliases.
        self.meta_query.get_sql("term", "t", "term_id")
        meta_clauses_ = self.meta_query.get_clauses()
        if (not meta_clauses_) or (not orderby_raw_):
            return orderby_
        # end if
        allowed_keys_ = Array()
        primary_meta_key_ = None
        primary_meta_query_ = reset(meta_clauses_)
        if (not php_empty(lambda : primary_meta_query_["key"])):
            primary_meta_key_ = primary_meta_query_["key"]
            allowed_keys_[-1] = primary_meta_key_
        # end if
        allowed_keys_[-1] = "meta_value"
        allowed_keys_[-1] = "meta_value_num"
        allowed_keys_ = php_array_merge(allowed_keys_, php_array_keys(meta_clauses_))
        if (not php_in_array(orderby_raw_, allowed_keys_, True)):
            return orderby_
        # end if
        for case in Switch(orderby_raw_):
            if case(primary_meta_key_):
                pass
            # end if
            if case("meta_value"):
                if (not php_empty(lambda : primary_meta_query_["type"])):
                    orderby_ = str("CAST(") + str(primary_meta_query_["alias"]) + str(".meta_value AS ") + str(primary_meta_query_["cast"]) + str(")")
                else:
                    orderby_ = str(primary_meta_query_["alias"]) + str(".meta_value")
                # end if
                break
            # end if
            if case("meta_value_num"):
                orderby_ = str(primary_meta_query_["alias"]) + str(".meta_value+0")
                break
            # end if
            if case():
                if php_array_key_exists(orderby_raw_, meta_clauses_):
                    #// $orderby corresponds to a meta_query clause.
                    meta_clause_ = meta_clauses_[orderby_raw_]
                    orderby_ = str("CAST(") + str(meta_clause_["alias"]) + str(".meta_value AS ") + str(meta_clause_["cast"]) + str(")")
                # end if
                break
            # end if
        # end for
        return orderby_
    # end def parse_orderby_meta
    #// 
    #// Parse an 'order' query variable and cast it to ASC or DESC as necessary.
    #// 
    #// @since 4.6.0
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
    #// Used internally to generate a SQL string related to the 'search' parameter.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $string
    #// @return string
    #//
    def get_search_sql(self, string_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        like_ = "%" + wpdb_.esc_like(string_) + "%"
        return wpdb_.prepare("((t.name LIKE %s) OR (t.slug LIKE %s))", like_, like_)
    # end def get_search_sql
    #// 
    #// Creates an array of term objects from an array of term IDs.
    #// 
    #// Also discards invalid term objects.
    #// 
    #// @since 4.9.8
    #// 
    #// @param array $term_ids Term IDs.
    #// @return array
    #//
    def populate_terms(self, term_ids_=None):
        
        
        terms_ = Array()
        if (not php_is_array(term_ids_)):
            return terms_
        # end if
        for key_,term_id_ in term_ids_.items():
            term_ = get_term(term_id_)
            if type(term_).__name__ == "WP_Term":
                terms_[key_] = term_
            # end if
        # end for
        return terms_
    # end def populate_terms
# end class WP_Term_Query
