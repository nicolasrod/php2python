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
#// Link/Bookmark API
#// 
#// @package WordPress
#// @subpackage Bookmark
#// 
#// 
#// Retrieve Bookmark data
#// 
#// @since 2.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|stdClass $bookmark
#// @param string $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// an stdClass object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string $filter Optional, default is 'raw'.
#// @return array|object|null Type returned depends on $output value.
#//
def get_bookmark(bookmark=None, output=OBJECT, filter="raw", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : bookmark):
        if (php_isset(lambda : PHP_GLOBALS["link"])):
            _bookmark = PHP_GLOBALS["link"]
        else:
            _bookmark = None
        # end if
    elif php_is_object(bookmark):
        wp_cache_add(bookmark.link_id, bookmark, "bookmark")
        _bookmark = bookmark
    else:
        if (php_isset(lambda : PHP_GLOBALS["link"])) and PHP_GLOBALS["link"].link_id == bookmark:
            _bookmark = PHP_GLOBALS["link"]
        else:
            _bookmark = wp_cache_get(bookmark, "bookmark")
            if (not _bookmark):
                _bookmark = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.links) + str(" WHERE link_id = %d LIMIT 1"), bookmark))
                if _bookmark:
                    _bookmark.link_category = array_unique(wp_get_object_terms(_bookmark.link_id, "link_category", Array({"fields": "ids"})))
                    wp_cache_add(_bookmark.link_id, _bookmark, "bookmark")
                # end if
            # end if
        # end if
    # end if
    if (not _bookmark):
        return _bookmark
    # end if
    _bookmark = sanitize_bookmark(_bookmark, filter)
    if OBJECT == output:
        return _bookmark
    elif ARRAY_A == output:
        return get_object_vars(_bookmark)
    elif ARRAY_N == output:
        return php_array_values(get_object_vars(_bookmark))
    else:
        return _bookmark
    # end if
# end def get_bookmark
#// 
#// Retrieve single bookmark data item or field.
#// 
#// @since 2.3.0
#// 
#// @param string $field The name of the data field to return
#// @param int $bookmark The bookmark ID to get field
#// @param string $context Optional. The context of how the field will be used.
#// @return string|WP_Error
#//
def get_bookmark_field(field=None, bookmark=None, context="display", *args_):
    
    bookmark = php_int(bookmark)
    bookmark = get_bookmark(bookmark)
    if is_wp_error(bookmark):
        return bookmark
    # end if
    if (not php_is_object(bookmark)):
        return ""
    # end if
    if (not (php_isset(lambda : bookmark.field))):
        return ""
    # end if
    return sanitize_bookmark_field(field, bookmark.field, bookmark.link_id, context)
# end def get_bookmark_field
#// 
#// Retrieves the list of bookmarks
#// 
#// Attempts to retrieve from the cache first based on MD5 hash of arguments. If
#// that fails, then the query will be built from the arguments and executed. The
#// results will be stored to the cache.
#// 
#// @since 2.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string|array $args {
#// Optional. String or array of arguments to retrieve bookmarks.
#// 
#// @type string   $orderby        How to order the links by. Accepts 'id', 'link_id', 'name', 'link_name',
#// 'url', 'link_url', 'visible', 'link_visible', 'rating', 'link_rating',
#// 'owner', 'link_owner', 'updated', 'link_updated', 'notes', 'link_notes',
#// 'description', 'link_description', 'length' and 'rand'.
#// When `$orderby` is 'length', orders by the character length of
#// 'link_name'. Default 'name'.
#// @type string   $order          Whether to order bookmarks in ascending or descending order.
#// Accepts 'ASC' (ascending) or 'DESC' (descending). Default 'ASC'.
#// @type int      $limit          Amount of bookmarks to display. Accepts any positive number or
#// -1 for all.  Default -1.
#// @type string   $category       Comma-separated list of category ids to include links from.
#// Default empty.
#// @type string   $category_name  Category to retrieve links for by name. Default empty.
#// @type int|bool $hide_invisible Whether to show or hide links marked as 'invisible'. Accepts
#// 1|true or 0|false. Default 1|true.
#// @type int|bool $show_updated   Whether to display the time the bookmark was last updated.
#// Accepts 1|true or 0|false. Default 0|false.
#// @type string   $include        Comma-separated list of bookmark IDs to include. Default empty.
#// @type string   $exclude        Comma-separated list of bookmark IDs to exclude. Default empty.
#// @type string   $search         Search terms. Will be SQL-formatted with wildcards before and after
#// and searched in 'link_url', 'link_name' and 'link_description'.
#// Default empty.
#// }
#// @return object[] List of bookmark row objects.
#//
def get_bookmarks(args="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    defaults = Array({"orderby": "name", "order": "ASC", "limit": -1, "category": "", "category_name": "", "hide_invisible": 1, "show_updated": 0, "include": "", "exclude": "", "search": ""})
    parsed_args = wp_parse_args(args, defaults)
    key = php_md5(serialize(parsed_args))
    cache = wp_cache_get("get_bookmarks", "bookmark")
    if "rand" != parsed_args["orderby"] and cache:
        if php_is_array(cache) and (php_isset(lambda : cache[key])):
            bookmarks = cache[key]
            #// 
            #// Filters the returned list of bookmarks.
            #// 
            #// The first time the hook is evaluated in this file, it returns the cached
            #// bookmarks list. The second evaluation returns a cached bookmarks list if the
            #// link category is passed but does not exist. The third evaluation returns
            #// the full cached results.
            #// 
            #// @since 2.1.0
            #// 
            #// @see get_bookmarks()
            #// 
            #// @param array $bookmarks   List of the cached bookmarks.
            #// @param array $parsed_args An array of bookmark query arguments.
            #//
            return apply_filters("get_bookmarks", bookmarks, parsed_args)
        # end if
    # end if
    if (not php_is_array(cache)):
        cache = Array()
    # end if
    inclusions = ""
    if (not php_empty(lambda : parsed_args["include"])):
        parsed_args["exclude"] = ""
        #// Ignore exclude, category, and category_name params if using include.
        parsed_args["category"] = ""
        parsed_args["category_name"] = ""
        inclinks = wp_parse_id_list(parsed_args["include"])
        if php_count(inclinks):
            for inclink in inclinks:
                if php_empty(lambda : inclusions):
                    inclusions = " AND ( link_id = " + inclink + " "
                else:
                    inclusions += " OR link_id = " + inclink + " "
                # end if
            # end for
        # end if
    # end if
    if (not php_empty(lambda : inclusions)):
        inclusions += ")"
    # end if
    exclusions = ""
    if (not php_empty(lambda : parsed_args["exclude"])):
        exlinks = wp_parse_id_list(parsed_args["exclude"])
        if php_count(exlinks):
            for exlink in exlinks:
                if php_empty(lambda : exclusions):
                    exclusions = " AND ( link_id <> " + exlink + " "
                else:
                    exclusions += " AND link_id <> " + exlink + " "
                # end if
            # end for
        # end if
    # end if
    if (not php_empty(lambda : exclusions)):
        exclusions += ")"
    # end if
    if (not php_empty(lambda : parsed_args["category_name"])):
        parsed_args["category"] = get_term_by("name", parsed_args["category_name"], "link_category")
        if parsed_args["category"]:
            parsed_args["category"] = parsed_args["category"].term_id
        else:
            cache[key] = Array()
            wp_cache_set("get_bookmarks", cache, "bookmark")
            #// This filter is documented in wp-includes/bookmark.php
            return apply_filters("get_bookmarks", Array(), parsed_args)
        # end if
    # end if
    search = ""
    if (not php_empty(lambda : parsed_args["search"])):
        like = "%" + wpdb.esc_like(parsed_args["search"]) + "%"
        search = wpdb.prepare(" AND ( (link_url LIKE %s) OR (link_name LIKE %s) OR (link_description LIKE %s) ) ", like, like, like)
    # end if
    category_query = ""
    join = ""
    if (not php_empty(lambda : parsed_args["category"])):
        incategories = wp_parse_id_list(parsed_args["category"])
        if php_count(incategories):
            for incat in incategories:
                if php_empty(lambda : category_query):
                    category_query = " AND ( tt.term_id = " + incat + " "
                else:
                    category_query += " OR tt.term_id = " + incat + " "
                # end if
            # end for
        # end if
    # end if
    if (not php_empty(lambda : category_query)):
        category_query += ") AND taxonomy = 'link_category'"
        join = str(" INNER JOIN ") + str(wpdb.term_relationships) + str(" AS tr ON (") + str(wpdb.links) + str(".link_id = tr.object_id) INNER JOIN ") + str(wpdb.term_taxonomy) + str(" as tt ON tt.term_taxonomy_id = tr.term_taxonomy_id")
    # end if
    if parsed_args["show_updated"]:
        recently_updated_test = ", IF (DATE_ADD(link_updated, INTERVAL 120 MINUTE) >= NOW(), 1,0) as recently_updated "
    else:
        recently_updated_test = ""
    # end if
    get_updated = ", UNIX_TIMESTAMP(link_updated) AS link_updated_f " if parsed_args["show_updated"] else ""
    orderby = php_strtolower(parsed_args["orderby"])
    length = ""
    for case in Switch(orderby):
        if case("length"):
            length = ", CHAR_LENGTH(link_name) AS length"
            break
        # end if
        if case("rand"):
            orderby = "rand()"
            break
        # end if
        if case("link_id"):
            orderby = str(wpdb.links) + str(".link_id")
            break
        # end if
        if case():
            orderparams = Array()
            keys = Array("link_id", "link_name", "link_url", "link_visible", "link_rating", "link_owner", "link_updated", "link_notes", "link_description")
            for ordparam in php_explode(",", orderby):
                ordparam = php_trim(ordparam)
                if php_in_array("link_" + ordparam, keys):
                    orderparams[-1] = "link_" + ordparam
                elif php_in_array(ordparam, keys):
                    orderparams[-1] = ordparam
                # end if
            # end for
            orderby = php_implode(",", orderparams)
        # end if
    # end for
    if php_empty(lambda : orderby):
        orderby = "link_name"
    # end if
    order = php_strtoupper(parsed_args["order"])
    if "" != order and (not php_in_array(order, Array("ASC", "DESC"))):
        order = "ASC"
    # end if
    visible = ""
    if parsed_args["hide_invisible"]:
        visible = "AND link_visible = 'Y'"
    # end if
    query = str("SELECT * ") + str(length) + str(" ") + str(recently_updated_test) + str(" ") + str(get_updated) + str(" FROM ") + str(wpdb.links) + str(" ") + str(join) + str(" WHERE 1=1 ") + str(visible) + str(" ") + str(category_query)
    query += str(" ") + str(exclusions) + str(" ") + str(inclusions) + str(" ") + str(search)
    query += str(" ORDER BY ") + str(orderby) + str(" ") + str(order)
    if -1 != parsed_args["limit"]:
        query += " LIMIT " + parsed_args["limit"]
    # end if
    results = wpdb.get_results(query)
    if "rand()" != orderby:
        cache[key] = results
        wp_cache_set("get_bookmarks", cache, "bookmark")
    # end if
    #// This filter is documented in wp-includes/bookmark.php
    return apply_filters("get_bookmarks", results, parsed_args)
# end def get_bookmarks
#// 
#// Sanitizes all bookmark fields
#// 
#// @since 2.3.0
#// 
#// @param stdClass|array $bookmark Bookmark row
#// @param string $context Optional, default is 'display'. How to filter the
#// fields
#// @return stdClass|array Same type as $bookmark but with fields sanitized.
#//
def sanitize_bookmark(bookmark=None, context="display", *args_):
    
    fields = Array("link_id", "link_url", "link_name", "link_image", "link_target", "link_category", "link_description", "link_visible", "link_owner", "link_rating", "link_updated", "link_rel", "link_notes", "link_rss")
    if php_is_object(bookmark):
        do_object = True
        link_id = bookmark.link_id
    else:
        do_object = False
        link_id = bookmark["link_id"]
    # end if
    for field in fields:
        if do_object:
            if (php_isset(lambda : bookmark.field)):
                bookmark.field = sanitize_bookmark_field(field, bookmark.field, link_id, context)
            # end if
        else:
            if (php_isset(lambda : bookmark[field])):
                bookmark[field] = sanitize_bookmark_field(field, bookmark[field], link_id, context)
            # end if
        # end if
    # end for
    return bookmark
# end def sanitize_bookmark
#// 
#// Sanitizes a bookmark field.
#// 
#// Sanitizes the bookmark fields based on what the field name is. If the field
#// has a strict value set, then it will be tested for that, else a more generic
#// filtering is applied. After the more strict filter is applied, if the `$context`
#// is 'raw' then the value is immediately return.
#// 
#// Hooks exist for the more generic cases. With the 'edit' context, the {@see 'edit_$field'}
#// filter will be called and passed the `$value` and `$bookmark_id` respectively.
#// 
#// With the 'db' context, the {@see 'pre_$field'} filter is called and passed the value.
#// The 'display' context is the final context and has the `$field` has the filter name
#// and is passed the `$value`, `$bookmark_id`, and `$context`, respectively.
#// 
#// @since 2.3.0
#// 
#// @param string $field       The bookmark field.
#// @param mixed  $value       The bookmark field value.
#// @param int    $bookmark_id Bookmark ID.
#// @param string $context     How to filter the field value. Accepts 'raw', 'edit', 'attribute',
#// 'js', 'db', or 'display'
#// @return mixed The filtered value.
#//
def sanitize_bookmark_field(field=None, value=None, bookmark_id=None, context=None, *args_):
    
    for case in Switch(field):
        if case("link_id"):
            pass
        # end if
        if case("link_rating"):
            value = php_int(value)
            break
        # end if
        if case("link_category"):
            #// array( ints )
            value = php_array_map("absint", value)
            #// We return here so that the categories aren't filtered.
            #// The 'link_category' filter is for the name of a link category, not an array of a link's link categories.
            return value
        # end if
        if case("link_visible"):
            #// bool stored as Y|N
            value = php_preg_replace("/[^YNyn]/", "", value)
            break
        # end if
        if case("link_target"):
            #// "enum"
            targets = Array("_top", "_blank")
            if (not php_in_array(value, targets)):
                value = ""
            # end if
            break
        # end if
    # end for
    if "raw" == context:
        return value
    # end if
    if "edit" == context:
        #// This filter is documented in wp-includes/post.php
        value = apply_filters(str("edit_") + str(field), value, bookmark_id)
        if "link_notes" == field:
            value = esc_html(value)
            pass
        else:
            value = esc_attr(value)
        # end if
    elif "db" == context:
        #// This filter is documented in wp-includes/post.php
        value = apply_filters(str("pre_") + str(field), value)
    else:
        #// This filter is documented in wp-includes/post.php
        value = apply_filters(str(field), value, bookmark_id, context)
        if "attribute" == context:
            value = esc_attr(value)
        elif "js" == context:
            value = esc_js(value)
        # end if
    # end if
    return value
# end def sanitize_bookmark_field
#// 
#// Deletes the bookmark cache.
#// 
#// @since 2.7.0
#// 
#// @param int $bookmark_id Bookmark ID.
#//
def clean_bookmark_cache(bookmark_id=None, *args_):
    
    wp_cache_delete(bookmark_id, "bookmark")
    wp_cache_delete("get_bookmarks", "bookmark")
    clean_object_term_cache(bookmark_id, "link")
# end def clean_bookmark_cache
