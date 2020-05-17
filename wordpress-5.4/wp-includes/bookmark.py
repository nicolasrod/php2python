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
def get_bookmark(bookmark_=None, output_=None, filter_="raw", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : bookmark_):
        if (php_isset(lambda : PHP_GLOBALS["link"])):
            _bookmark_ = PHP_GLOBALS["link"]
        else:
            _bookmark_ = None
        # end if
    elif php_is_object(bookmark_):
        wp_cache_add(bookmark_.link_id, bookmark_, "bookmark")
        _bookmark_ = bookmark_
    else:
        if (php_isset(lambda : PHP_GLOBALS["link"])) and PHP_GLOBALS["link"].link_id == bookmark_:
            _bookmark_ = PHP_GLOBALS["link"]
        else:
            _bookmark_ = wp_cache_get(bookmark_, "bookmark")
            if (not _bookmark_):
                _bookmark_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.links) + str(" WHERE link_id = %d LIMIT 1"), bookmark_))
                if _bookmark_:
                    _bookmark_.link_category = array_unique(wp_get_object_terms(_bookmark_.link_id, "link_category", Array({"fields": "ids"})))
                    wp_cache_add(_bookmark_.link_id, _bookmark_, "bookmark")
                # end if
            # end if
        # end if
    # end if
    if (not _bookmark_):
        return _bookmark_
    # end if
    _bookmark_ = sanitize_bookmark(_bookmark_, filter_)
    if OBJECT == output_:
        return _bookmark_
    elif ARRAY_A == output_:
        return get_object_vars(_bookmark_)
    elif ARRAY_N == output_:
        return php_array_values(get_object_vars(_bookmark_))
    else:
        return _bookmark_
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
def get_bookmark_field(field_=None, bookmark_=None, context_="display", *_args_):
    
    
    bookmark_ = php_int(bookmark_)
    bookmark_ = get_bookmark(bookmark_)
    if is_wp_error(bookmark_):
        return bookmark_
    # end if
    if (not php_is_object(bookmark_)):
        return ""
    # end if
    if (not (php_isset(lambda : bookmark_.field_))):
        return ""
    # end if
    return sanitize_bookmark_field(field_, bookmark_.field_, bookmark_.link_id, context_)
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
def get_bookmarks(args_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    defaults_ = Array({"orderby": "name", "order": "ASC", "limit": -1, "category": "", "category_name": "", "hide_invisible": 1, "show_updated": 0, "include": "", "exclude": "", "search": ""})
    parsed_args_ = wp_parse_args(args_, defaults_)
    key_ = php_md5(serialize(parsed_args_))
    cache_ = wp_cache_get("get_bookmarks", "bookmark")
    if "rand" != parsed_args_["orderby"] and cache_:
        if php_is_array(cache_) and (php_isset(lambda : cache_[key_])):
            bookmarks_ = cache_[key_]
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
            return apply_filters("get_bookmarks", bookmarks_, parsed_args_)
        # end if
    # end if
    if (not php_is_array(cache_)):
        cache_ = Array()
    # end if
    inclusions_ = ""
    if (not php_empty(lambda : parsed_args_["include"])):
        parsed_args_["exclude"] = ""
        #// Ignore exclude, category, and category_name params if using include.
        parsed_args_["category"] = ""
        parsed_args_["category_name"] = ""
        inclinks_ = wp_parse_id_list(parsed_args_["include"])
        if php_count(inclinks_):
            for inclink_ in inclinks_:
                if php_empty(lambda : inclusions_):
                    inclusions_ = " AND ( link_id = " + inclink_ + " "
                else:
                    inclusions_ += " OR link_id = " + inclink_ + " "
                # end if
            # end for
        # end if
    # end if
    if (not php_empty(lambda : inclusions_)):
        inclusions_ += ")"
    # end if
    exclusions_ = ""
    if (not php_empty(lambda : parsed_args_["exclude"])):
        exlinks_ = wp_parse_id_list(parsed_args_["exclude"])
        if php_count(exlinks_):
            for exlink_ in exlinks_:
                if php_empty(lambda : exclusions_):
                    exclusions_ = " AND ( link_id <> " + exlink_ + " "
                else:
                    exclusions_ += " AND link_id <> " + exlink_ + " "
                # end if
            # end for
        # end if
    # end if
    if (not php_empty(lambda : exclusions_)):
        exclusions_ += ")"
    # end if
    if (not php_empty(lambda : parsed_args_["category_name"])):
        parsed_args_["category"] = get_term_by("name", parsed_args_["category_name"], "link_category")
        if parsed_args_["category"]:
            parsed_args_["category"] = parsed_args_["category"].term_id
        else:
            cache_[key_] = Array()
            wp_cache_set("get_bookmarks", cache_, "bookmark")
            #// This filter is documented in wp-includes/bookmark.php
            return apply_filters("get_bookmarks", Array(), parsed_args_)
        # end if
    # end if
    search_ = ""
    if (not php_empty(lambda : parsed_args_["search"])):
        like_ = "%" + wpdb_.esc_like(parsed_args_["search"]) + "%"
        search_ = wpdb_.prepare(" AND ( (link_url LIKE %s) OR (link_name LIKE %s) OR (link_description LIKE %s) ) ", like_, like_, like_)
    # end if
    category_query_ = ""
    join_ = ""
    if (not php_empty(lambda : parsed_args_["category"])):
        incategories_ = wp_parse_id_list(parsed_args_["category"])
        if php_count(incategories_):
            for incat_ in incategories_:
                if php_empty(lambda : category_query_):
                    category_query_ = " AND ( tt.term_id = " + incat_ + " "
                else:
                    category_query_ += " OR tt.term_id = " + incat_ + " "
                # end if
            # end for
        # end if
    # end if
    if (not php_empty(lambda : category_query_)):
        category_query_ += ") AND taxonomy = 'link_category'"
        join_ = str(" INNER JOIN ") + str(wpdb_.term_relationships) + str(" AS tr ON (") + str(wpdb_.links) + str(".link_id = tr.object_id) INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" as tt ON tt.term_taxonomy_id = tr.term_taxonomy_id")
    # end if
    if parsed_args_["show_updated"]:
        recently_updated_test_ = ", IF (DATE_ADD(link_updated, INTERVAL 120 MINUTE) >= NOW(), 1,0) as recently_updated "
    else:
        recently_updated_test_ = ""
    # end if
    get_updated_ = ", UNIX_TIMESTAMP(link_updated) AS link_updated_f " if parsed_args_["show_updated"] else ""
    orderby_ = php_strtolower(parsed_args_["orderby"])
    length_ = ""
    for case in Switch(orderby_):
        if case("length"):
            length_ = ", CHAR_LENGTH(link_name) AS length"
            break
        # end if
        if case("rand"):
            orderby_ = "rand()"
            break
        # end if
        if case("link_id"):
            orderby_ = str(wpdb_.links) + str(".link_id")
            break
        # end if
        if case():
            orderparams_ = Array()
            keys_ = Array("link_id", "link_name", "link_url", "link_visible", "link_rating", "link_owner", "link_updated", "link_notes", "link_description")
            for ordparam_ in php_explode(",", orderby_):
                ordparam_ = php_trim(ordparam_)
                if php_in_array("link_" + ordparam_, keys_):
                    orderparams_[-1] = "link_" + ordparam_
                elif php_in_array(ordparam_, keys_):
                    orderparams_[-1] = ordparam_
                # end if
            # end for
            orderby_ = php_implode(",", orderparams_)
        # end if
    # end for
    if php_empty(lambda : orderby_):
        orderby_ = "link_name"
    # end if
    order_ = php_strtoupper(parsed_args_["order"])
    if "" != order_ and (not php_in_array(order_, Array("ASC", "DESC"))):
        order_ = "ASC"
    # end if
    visible_ = ""
    if parsed_args_["hide_invisible"]:
        visible_ = "AND link_visible = 'Y'"
    # end if
    query_ = str("SELECT * ") + str(length_) + str(" ") + str(recently_updated_test_) + str(" ") + str(get_updated_) + str(" FROM ") + str(wpdb_.links) + str(" ") + str(join_) + str(" WHERE 1=1 ") + str(visible_) + str(" ") + str(category_query_)
    query_ += str(" ") + str(exclusions_) + str(" ") + str(inclusions_) + str(" ") + str(search_)
    query_ += str(" ORDER BY ") + str(orderby_) + str(" ") + str(order_)
    if -1 != parsed_args_["limit"]:
        query_ += " LIMIT " + parsed_args_["limit"]
    # end if
    results_ = wpdb_.get_results(query_)
    if "rand()" != orderby_:
        cache_[key_] = results_
        wp_cache_set("get_bookmarks", cache_, "bookmark")
    # end if
    #// This filter is documented in wp-includes/bookmark.php
    return apply_filters("get_bookmarks", results_, parsed_args_)
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
def sanitize_bookmark(bookmark_=None, context_="display", *_args_):
    
    
    fields_ = Array("link_id", "link_url", "link_name", "link_image", "link_target", "link_category", "link_description", "link_visible", "link_owner", "link_rating", "link_updated", "link_rel", "link_notes", "link_rss")
    if php_is_object(bookmark_):
        do_object_ = True
        link_id_ = bookmark_.link_id
    else:
        do_object_ = False
        link_id_ = bookmark_["link_id"]
    # end if
    for field_ in fields_:
        if do_object_:
            if (php_isset(lambda : bookmark_.field_)):
                bookmark_.field_ = sanitize_bookmark_field(field_, bookmark_.field_, link_id_, context_)
            # end if
        else:
            if (php_isset(lambda : bookmark_[field_])):
                bookmark_[field_] = sanitize_bookmark_field(field_, bookmark_[field_], link_id_, context_)
            # end if
        # end if
    # end for
    return bookmark_
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
def sanitize_bookmark_field(field_=None, value_=None, bookmark_id_=None, context_=None, *_args_):
    
    
    for case in Switch(field_):
        if case("link_id"):
            pass
        # end if
        if case("link_rating"):
            value_ = php_int(value_)
            break
        # end if
        if case("link_category"):
            #// array( ints )
            value_ = php_array_map("absint", value_)
            #// We return here so that the categories aren't filtered.
            #// The 'link_category' filter is for the name of a link category, not an array of a link's link categories.
            return value_
        # end if
        if case("link_visible"):
            #// bool stored as Y|N
            value_ = php_preg_replace("/[^YNyn]/", "", value_)
            break
        # end if
        if case("link_target"):
            #// "enum"
            targets_ = Array("_top", "_blank")
            if (not php_in_array(value_, targets_)):
                value_ = ""
            # end if
            break
        # end if
    # end for
    if "raw" == context_:
        return value_
    # end if
    if "edit" == context_:
        #// This filter is documented in wp-includes/post.php
        value_ = apply_filters(str("edit_") + str(field_), value_, bookmark_id_)
        if "link_notes" == field_:
            value_ = esc_html(value_)
            pass
        else:
            value_ = esc_attr(value_)
        # end if
    elif "db" == context_:
        #// This filter is documented in wp-includes/post.php
        value_ = apply_filters(str("pre_") + str(field_), value_)
    else:
        #// This filter is documented in wp-includes/post.php
        value_ = apply_filters(str(field_), value_, bookmark_id_, context_)
        if "attribute" == context_:
            value_ = esc_attr(value_)
        elif "js" == context_:
            value_ = esc_js(value_)
        # end if
    # end if
    return value_
# end def sanitize_bookmark_field
#// 
#// Deletes the bookmark cache.
#// 
#// @since 2.7.0
#// 
#// @param int $bookmark_id Bookmark ID.
#//
def clean_bookmark_cache(bookmark_id_=None, *_args_):
    
    
    wp_cache_delete(bookmark_id_, "bookmark")
    wp_cache_delete("get_bookmarks", "bookmark")
    clean_object_term_cache(bookmark_id_, "link")
# end def clean_bookmark_cache
