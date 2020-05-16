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
    request = Array()
    meta_query = False
    meta_query_clauses = Array()
    sql_clauses = Array({"select": "", "from": "", "where": Array(), "orderby": "", "limits": ""})
    query_vars = Array()
    query_var_defaults = Array()
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
    def __init__(self, query=""):
        
        self.query_var_defaults = Array({"taxonomy": None, "object_ids": None, "orderby": "name", "order": "ASC", "hide_empty": True, "include": Array(), "exclude": Array(), "exclude_tree": Array(), "number": "", "offset": "", "fields": "all", "count": False, "name": "", "slug": "", "term_taxonomy_id": "", "hierarchical": True, "search": "", "name__like": "", "description__like": "", "pad_counts": False, "get": "", "child_of": 0, "parent": "", "childless": False, "cache_domain": "core", "update_term_meta_cache": True, "meta_query": "", "meta_key": "", "meta_value": "", "meta_type": "", "meta_compare": ""})
        if (not php_empty(lambda : query)):
            self.query(query)
        # end if
    # end def __init__
    #// 
    #// Parse arguments passed to the term query with default query parameters.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string|array $query WP_Term_Query arguments. See WP_Term_Query::__construct()
    #//
    def parse_query(self, query=""):
        
        if php_empty(lambda : query):
            query = self.query_vars
        # end if
        taxonomies = query["taxonomy"] if (php_isset(lambda : query["taxonomy"])) else None
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
        self.query_var_defaults = apply_filters("get_terms_defaults", self.query_var_defaults, taxonomies)
        query = wp_parse_args(query, self.query_var_defaults)
        query["number"] = absint(query["number"])
        query["offset"] = absint(query["offset"])
        #// 'parent' overrides 'child_of'.
        if 0 < php_intval(query["parent"]):
            query["child_of"] = False
        # end if
        if "all" == query["get"]:
            query["childless"] = False
            query["child_of"] = 0
            query["hide_empty"] = 0
            query["hierarchical"] = False
            query["pad_counts"] = False
        # end if
        query["taxonomy"] = taxonomies
        self.query_vars = query
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
    def query(self, query=None):
        
        self.query_vars = wp_parse_args(query)
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
        
        global wpdb
        php_check_if_defined("wpdb")
        self.parse_query(self.query_vars)
        args = self.query_vars
        #// Set up meta_query so it's available to 'pre_get_terms'.
        self.meta_query = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query())
        self.meta_query.parse_query_vars(args)
        #// 
        #// Fires before terms are retrieved.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Term_Query $this Current instance of WP_Term_Query.
        #//
        do_action("pre_get_terms", self)
        taxonomies = args["taxonomy"]
        #// Save queries by not crawling the tree in the case of multiple taxes or a flat tax.
        has_hierarchical_tax = False
        if taxonomies:
            for _tax in taxonomies:
                if is_taxonomy_hierarchical(_tax):
                    has_hierarchical_tax = True
                # end if
            # end for
        else:
            #// When no taxonomies are provided, assume we have to descend the tree.
            has_hierarchical_tax = True
        # end if
        if (not has_hierarchical_tax):
            args["hierarchical"] = False
            args["pad_counts"] = False
        # end if
        #// 'parent' overrides 'child_of'.
        if 0 < php_intval(args["parent"]):
            args["child_of"] = False
        # end if
        if "all" == args["get"]:
            args["childless"] = False
            args["child_of"] = 0
            args["hide_empty"] = 0
            args["hierarchical"] = False
            args["pad_counts"] = False
        # end if
        #// 
        #// Filters the terms query arguments.
        #// 
        #// @since 3.1.0
        #// 
        #// @param array    $args       An array of get_terms() arguments.
        #// @param string[] $taxonomies An array of taxonomy names.
        #//
        args = apply_filters("get_terms_args", args, taxonomies)
        #// Avoid the query if the queried parent/child_of term has no descendants.
        child_of = args["child_of"]
        parent = args["parent"]
        if child_of:
            _parent = child_of
        elif parent:
            _parent = parent
        else:
            _parent = False
        # end if
        if _parent:
            in_hierarchy = False
            for _tax in taxonomies:
                hierarchy = _get_term_hierarchy(_tax)
                if (php_isset(lambda : hierarchy[_parent])):
                    in_hierarchy = True
                # end if
            # end for
            if (not in_hierarchy):
                if "count" == args["fields"]:
                    return 0
                else:
                    self.terms = Array()
                    return self.terms
                # end if
            # end if
        # end if
        #// 'term_order' is a legal sort order only when joining the relationship table.
        _orderby = self.query_vars["orderby"]
        if "term_order" == _orderby and php_empty(lambda : self.query_vars["object_ids"]):
            _orderby = "term_id"
        # end if
        orderby = self.parse_orderby(_orderby)
        if orderby:
            orderby = str("ORDER BY ") + str(orderby)
        # end if
        order = self.parse_order(self.query_vars["order"])
        if taxonomies:
            self.sql_clauses["where"]["taxonomy"] = "tt.taxonomy IN ('" + php_implode("', '", php_array_map("esc_sql", taxonomies)) + "')"
        # end if
        exclude = args["exclude"]
        exclude_tree = args["exclude_tree"]
        include = args["include"]
        inclusions = ""
        if (not php_empty(lambda : include)):
            exclude = ""
            exclude_tree = ""
            inclusions = php_implode(",", wp_parse_id_list(include))
        # end if
        if (not php_empty(lambda : inclusions)):
            self.sql_clauses["where"]["inclusions"] = "t.term_id IN ( " + inclusions + " )"
        # end if
        exclusions = Array()
        if (not php_empty(lambda : exclude_tree)):
            exclude_tree = wp_parse_id_list(exclude_tree)
            excluded_children = exclude_tree
            for extrunk in exclude_tree:
                excluded_children = php_array_merge(excluded_children, get_terms(Array({"taxonomy": reset(taxonomies), "child_of": php_intval(extrunk), "fields": "ids", "hide_empty": 0})))
            # end for
            exclusions = php_array_merge(excluded_children, exclusions)
        # end if
        if (not php_empty(lambda : exclude)):
            exclusions = php_array_merge(wp_parse_id_list(exclude), exclusions)
        # end if
        #// 'childless' terms are those without an entry in the flattened term hierarchy.
        childless = php_bool(args["childless"])
        if childless:
            for _tax in taxonomies:
                term_hierarchy = _get_term_hierarchy(_tax)
                exclusions = php_array_merge(php_array_keys(term_hierarchy), exclusions)
            # end for
        # end if
        if (not php_empty(lambda : exclusions)):
            exclusions = "t.term_id NOT IN (" + php_implode(",", php_array_map("intval", exclusions)) + ")"
        else:
            exclusions = ""
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
        exclusions = apply_filters("list_terms_exclusions", exclusions, args, taxonomies)
        if (not php_empty(lambda : exclusions)):
            #// Must do string manipulation here for backward compatibility with filter.
            self.sql_clauses["where"]["exclusions"] = php_preg_replace("/^\\s*AND\\s*/", "", exclusions)
        # end if
        if (not php_empty(lambda : args["name"])) or php_is_string(args["name"]) and 0 != php_strlen(args["name"]):
            names = args["name"]
            for _name in names:
                #// `sanitize_term_field()` returns slashed data.
                _name = stripslashes(sanitize_term_field("name", _name, 0, reset(taxonomies), "db"))
            # end for
            self.sql_clauses["where"]["name"] = "t.name IN ('" + php_implode("', '", php_array_map("esc_sql", names)) + "')"
        # end if
        if (not php_empty(lambda : args["slug"])) or php_is_string(args["slug"]) and 0 != php_strlen(args["slug"]):
            if php_is_array(args["slug"]):
                slug = php_array_map("sanitize_title", args["slug"])
                self.sql_clauses["where"]["slug"] = "t.slug IN ('" + php_implode("', '", slug) + "')"
            else:
                slug = sanitize_title(args["slug"])
                self.sql_clauses["where"]["slug"] = str("t.slug = '") + str(slug) + str("'")
            # end if
        # end if
        if (not php_empty(lambda : args["term_taxonomy_id"])):
            if php_is_array(args["term_taxonomy_id"]):
                tt_ids = php_implode(",", php_array_map("intval", args["term_taxonomy_id"]))
                self.sql_clauses["where"]["term_taxonomy_id"] = str("tt.term_taxonomy_id IN (") + str(tt_ids) + str(")")
            else:
                self.sql_clauses["where"]["term_taxonomy_id"] = wpdb.prepare("tt.term_taxonomy_id = %d", args["term_taxonomy_id"])
            # end if
        # end if
        if (not php_empty(lambda : args["name__like"])):
            self.sql_clauses["where"]["name__like"] = wpdb.prepare("t.name LIKE %s", "%" + wpdb.esc_like(args["name__like"]) + "%")
        # end if
        if (not php_empty(lambda : args["description__like"])):
            self.sql_clauses["where"]["description__like"] = wpdb.prepare("tt.description LIKE %s", "%" + wpdb.esc_like(args["description__like"]) + "%")
        # end if
        if (not php_empty(lambda : args["object_ids"])):
            object_ids = args["object_ids"]
            if (not php_is_array(object_ids)):
                object_ids = Array(object_ids)
            # end if
            object_ids = php_implode(", ", php_array_map("intval", object_ids))
            self.sql_clauses["where"]["object_ids"] = str("tr.object_id IN (") + str(object_ids) + str(")")
        # end if
        #// 
        #// When querying for object relationships, the 'count > 0' check
        #// added by 'hide_empty' is superfluous.
        #//
        if (not php_empty(lambda : args["object_ids"])):
            args["hide_empty"] = False
        # end if
        if "" != parent:
            parent = php_int(parent)
            self.sql_clauses["where"]["parent"] = str("tt.parent = '") + str(parent) + str("'")
        # end if
        hierarchical = args["hierarchical"]
        if "count" == args["fields"]:
            hierarchical = False
        # end if
        if args["hide_empty"] and (not hierarchical):
            self.sql_clauses["where"]["count"] = "tt.count > 0"
        # end if
        number = args["number"]
        offset = args["offset"]
        #// Don't limit the query results when we have to descend the family tree.
        if number and (not hierarchical) and (not child_of) and "" == parent:
            if offset:
                limits = "LIMIT " + offset + "," + number
            else:
                limits = "LIMIT " + number
            # end if
        else:
            limits = ""
        # end if
        if (not php_empty(lambda : args["search"])):
            self.sql_clauses["where"]["search"] = self.get_search_sql(args["search"])
        # end if
        #// Meta query support.
        join = ""
        distinct = ""
        #// Reparse meta_query query_vars, in case they were modified in a 'pre_get_terms' callback.
        self.meta_query.parse_query_vars(self.query_vars)
        mq_sql = self.meta_query.get_sql("term", "t", "term_id")
        meta_clauses = self.meta_query.get_clauses()
        if (not php_empty(lambda : meta_clauses)):
            join += mq_sql["join"]
            self.sql_clauses["where"]["meta_query"] = php_preg_replace("/^\\s*AND\\s*/", "", mq_sql["where"])
            distinct += "DISTINCT"
        # end if
        selects = Array()
        for case in Switch(args["fields"]):
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
                selects = Array("t.*", "tt.*")
                if "all_with_object_id" == args["fields"] and (not php_empty(lambda : args["object_ids"])):
                    selects[-1] = "tr.object_id"
                # end if
                break
            # end if
            if case("ids"):
                pass
            # end if
            if case("id=>parent"):
                selects = Array("t.term_id", "tt.parent", "tt.count", "tt.taxonomy")
                break
            # end if
            if case("names"):
                selects = Array("t.term_id", "tt.parent", "tt.count", "t.name", "tt.taxonomy")
                break
            # end if
            if case("count"):
                orderby = ""
                order = ""
                selects = Array("COUNT(*)")
                break
            # end if
            if case("id=>name"):
                selects = Array("t.term_id", "t.name", "tt.count", "tt.taxonomy")
                break
            # end if
            if case("id=>slug"):
                selects = Array("t.term_id", "t.slug", "tt.count", "tt.taxonomy")
                break
            # end if
        # end for
        _fields = args["fields"]
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
        fields = php_implode(", ", apply_filters("get_terms_fields", selects, args, taxonomies))
        join += str(" INNER JOIN ") + str(wpdb.term_taxonomy) + str(" AS tt ON t.term_id = tt.term_id")
        if (not php_empty(lambda : self.query_vars["object_ids"])):
            join += str(" INNER JOIN ") + str(wpdb.term_relationships) + str(" AS tr ON tr.term_taxonomy_id = tt.term_taxonomy_id")
        # end if
        where = php_implode(" AND ", self.sql_clauses["where"])
        #// 
        #// Filters the terms query SQL clauses.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[] $pieces     Array of query SQL clauses.
        #// @param string[] $taxonomies An array of taxonomy names.
        #// @param array    $args       An array of term query arguments.
        #//
        clauses = apply_filters("terms_clauses", compact("fields", "join", "where", "distinct", "orderby", "order", "limits"), taxonomies, args)
        fields = clauses["fields"] if (php_isset(lambda : clauses["fields"])) else ""
        join = clauses["join"] if (php_isset(lambda : clauses["join"])) else ""
        where = clauses["where"] if (php_isset(lambda : clauses["where"])) else ""
        distinct = clauses["distinct"] if (php_isset(lambda : clauses["distinct"])) else ""
        orderby = clauses["orderby"] if (php_isset(lambda : clauses["orderby"])) else ""
        order = clauses["order"] if (php_isset(lambda : clauses["order"])) else ""
        limits = clauses["limits"] if (php_isset(lambda : clauses["limits"])) else ""
        if where:
            where = str("WHERE ") + str(where)
        # end if
        self.sql_clauses["select"] = str("SELECT ") + str(distinct) + str(" ") + str(fields)
        self.sql_clauses["from"] = str("FROM ") + str(wpdb.terms) + str(" AS t ") + str(join)
        self.sql_clauses["orderby"] = str(orderby) + str(" ") + str(order) if orderby else ""
        self.sql_clauses["limits"] = limits
        self.request = str(self.sql_clauses["select"]) + str(" ") + str(self.sql_clauses["from"]) + str(" ") + str(where) + str(" ") + str(self.sql_clauses["orderby"]) + str(" ") + str(self.sql_clauses["limits"])
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
        key = php_md5(serialize(wp_array_slice_assoc(args, php_array_keys(self.query_var_defaults))) + serialize(taxonomies) + self.request)
        last_changed = wp_cache_get_last_changed("terms")
        cache_key = str("get_terms:") + str(key) + str(":") + str(last_changed)
        cache = wp_cache_get(cache_key, "terms")
        if False != cache:
            if "all" == _fields or "all_with_object_id" == _fields:
                cache = self.populate_terms(cache)
            # end if
            self.terms = cache
            return self.terms
        # end if
        if "count" == _fields:
            count = wpdb.get_var(self.request)
            wp_cache_set(cache_key, count, "terms")
            return count
        # end if
        terms = wpdb.get_results(self.request)
        if "all" == _fields or "all_with_object_id" == _fields:
            update_term_cache(terms)
        # end if
        #// Prime termmeta cache.
        if args["update_term_meta_cache"]:
            term_ids = wp_list_pluck(terms, "term_id")
            update_termmeta_cache(term_ids)
        # end if
        if php_empty(lambda : terms):
            wp_cache_add(cache_key, Array(), "terms", DAY_IN_SECONDS)
            return Array()
        # end if
        if child_of:
            for _tax in taxonomies:
                children = _get_term_hierarchy(_tax)
                if (not php_empty(lambda : children)):
                    terms = _get_term_children(child_of, terms, _tax)
                # end if
            # end for
        # end if
        #// Update term counts to include children.
        if args["pad_counts"] and "all" == _fields:
            for _tax in taxonomies:
                _pad_term_counts(terms, _tax)
            # end for
        # end if
        #// Make sure we show empty categories that have children.
        if hierarchical and args["hide_empty"] and php_is_array(terms):
            for k,term in terms:
                if (not term.count):
                    children = get_term_children(term.term_id, term.taxonomy)
                    if php_is_array(children):
                        for child_id in children:
                            child = get_term(child_id, term.taxonomy)
                            if child.count:
                                continue
                            # end if
                        # end for
                    # end if
                    terms[k] = None
                # end if
            # end for
        # end if
        #// 
        #// When querying for terms connected to objects, we may get
        #// duplicate results. The duplicates should be preserved if
        #// `$fields` is 'all_with_object_id', but should otherwise be
        #// removed.
        #//
        if (not php_empty(lambda : args["object_ids"])) and "all_with_object_id" != _fields:
            _tt_ids = Array()
            _terms = Array()
            for term in terms:
                if (php_isset(lambda : _tt_ids[term.term_id])):
                    continue
                # end if
                _tt_ids[term.term_id] = 1
                _terms[-1] = term
            # end for
            terms = _terms
        # end if
        _terms = Array()
        if "id=>parent" == _fields:
            for term in terms:
                _terms[term.term_id] = term.parent
            # end for
        elif "ids" == _fields:
            for term in terms:
                _terms[-1] = php_int(term.term_id)
            # end for
        elif "tt_ids" == _fields:
            for term in terms:
                _terms[-1] = php_int(term.term_taxonomy_id)
            # end for
        elif "names" == _fields:
            for term in terms:
                _terms[-1] = term.name
            # end for
        elif "slugs" == _fields:
            for term in terms:
                _terms[-1] = term.slug
            # end for
        elif "id=>name" == _fields:
            for term in terms:
                _terms[term.term_id] = term.name
            # end for
        elif "id=>slug" == _fields:
            for term in terms:
                _terms[term.term_id] = term.slug
            # end for
        # end if
        if (not php_empty(lambda : _terms)):
            terms = _terms
        # end if
        #// Hierarchical queries are not limited, so 'offset' and 'number' must be handled now.
        if hierarchical and number and php_is_array(terms):
            if offset >= php_count(terms):
                terms = Array()
            else:
                terms = php_array_slice(terms, offset, number, True)
            # end if
        # end if
        wp_cache_add(cache_key, terms, "terms", DAY_IN_SECONDS)
        if "all" == _fields or "all_with_object_id" == _fields:
            terms = self.populate_terms(terms)
        # end if
        self.terms = terms
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
    def parse_orderby(self, orderby_raw=None):
        
        _orderby = php_strtolower(orderby_raw)
        maybe_orderby_meta = False
        if php_in_array(_orderby, Array("term_id", "name", "slug", "term_group"), True):
            orderby = str("t.") + str(_orderby)
        elif php_in_array(_orderby, Array("count", "parent", "taxonomy", "term_taxonomy_id", "description"), True):
            orderby = str("tt.") + str(_orderby)
        elif "term_order" == _orderby:
            orderby = "tr.term_order"
        elif "include" == _orderby and (not php_empty(lambda : self.query_vars["include"])):
            include = php_implode(",", wp_parse_id_list(self.query_vars["include"]))
            orderby = str("FIELD( t.term_id, ") + str(include) + str(" )")
        elif "slug__in" == _orderby and (not php_empty(lambda : self.query_vars["slug"])) and php_is_array(self.query_vars["slug"]):
            slugs = php_implode("', '", php_array_map("sanitize_title_for_query", self.query_vars["slug"]))
            orderby = "FIELD( t.slug, '" + slugs + "')"
        elif "none" == _orderby:
            orderby = ""
        elif php_empty(lambda : _orderby) or "id" == _orderby or "term_id" == _orderby:
            orderby = "t.term_id"
        else:
            orderby = "t.name"
            #// This may be a value of orderby related to meta.
            maybe_orderby_meta = True
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
        orderby = apply_filters("get_terms_orderby", orderby, self.query_vars, self.query_vars["taxonomy"])
        #// Run after the 'get_terms_orderby' filter for backward compatibility.
        if maybe_orderby_meta:
            maybe_orderby_meta = self.parse_orderby_meta(_orderby)
            if maybe_orderby_meta:
                orderby = maybe_orderby_meta
            # end if
        # end if
        return orderby
    # end def parse_orderby
    #// 
    #// Generate the ORDER BY clause for an 'orderby' param that is potentially related to a meta query.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $orderby_raw Raw 'orderby' value passed to WP_Term_Query.
    #// @return string ORDER BY clause.
    #//
    def parse_orderby_meta(self, orderby_raw=None):
        
        orderby = ""
        #// Tell the meta query to generate its SQL, so we have access to table aliases.
        self.meta_query.get_sql("term", "t", "term_id")
        meta_clauses = self.meta_query.get_clauses()
        if (not meta_clauses) or (not orderby_raw):
            return orderby
        # end if
        allowed_keys = Array()
        primary_meta_key = None
        primary_meta_query = reset(meta_clauses)
        if (not php_empty(lambda : primary_meta_query["key"])):
            primary_meta_key = primary_meta_query["key"]
            allowed_keys[-1] = primary_meta_key
        # end if
        allowed_keys[-1] = "meta_value"
        allowed_keys[-1] = "meta_value_num"
        allowed_keys = php_array_merge(allowed_keys, php_array_keys(meta_clauses))
        if (not php_in_array(orderby_raw, allowed_keys, True)):
            return orderby
        # end if
        for case in Switch(orderby_raw):
            if case(primary_meta_key):
                pass
            # end if
            if case("meta_value"):
                if (not php_empty(lambda : primary_meta_query["type"])):
                    orderby = str("CAST(") + str(primary_meta_query["alias"]) + str(".meta_value AS ") + str(primary_meta_query["cast"]) + str(")")
                else:
                    orderby = str(primary_meta_query["alias"]) + str(".meta_value")
                # end if
                break
            # end if
            if case("meta_value_num"):
                orderby = str(primary_meta_query["alias"]) + str(".meta_value+0")
                break
            # end if
            if case():
                if php_array_key_exists(orderby_raw, meta_clauses):
                    #// $orderby corresponds to a meta_query clause.
                    meta_clause = meta_clauses[orderby_raw]
                    orderby = str("CAST(") + str(meta_clause["alias"]) + str(".meta_value AS ") + str(meta_clause["cast"]) + str(")")
                # end if
                break
            # end if
        # end for
        return orderby
    # end def parse_orderby_meta
    #// 
    #// Parse an 'order' query variable and cast it to ASC or DESC as necessary.
    #// 
    #// @since 4.6.0
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
    #// Used internally to generate a SQL string related to the 'search' parameter.
    #// 
    #// @since 4.6.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $string
    #// @return string
    #//
    def get_search_sql(self, string=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        like = "%" + wpdb.esc_like(string) + "%"
        return wpdb.prepare("((t.name LIKE %s) OR (t.slug LIKE %s))", like, like)
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
    def populate_terms(self, term_ids=None):
        
        terms = Array()
        if (not php_is_array(term_ids)):
            return terms
        # end if
        for key,term_id in term_ids:
            term = get_term(term_id)
            if type(term).__name__ == "WP_Term":
                terms[key] = term
            # end if
        # end for
        return terms
    # end def populate_terms
# end class WP_Term_Query
