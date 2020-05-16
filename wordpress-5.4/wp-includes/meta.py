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
#// Core Metadata API
#// 
#// Functions for retrieving and manipulating metadata of various WordPress object types. Metadata
#// for an object is a represented by a simple key-value pair. Objects may contain multiple
#// metadata entries that share the same key and differ only in their value.
#// 
#// @package WordPress
#// @subpackage Meta
#// 
#// 
#// Adds metadata for the specified object.
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $meta_type  Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $object_id  ID of the object metadata is for.
#// @param string $meta_key   Metadata key.
#// @param mixed  $meta_value Metadata value. Must be serializable if non-scalar.
#// @param bool   $unique     Optional. Whether the specified metadata key should be unique for the object.
#// If true, and the object already has a value for the specified metadata key,
#// no change will be made. Default false.
#// @return int|false The meta ID on success, false on failure.
#//
def add_metadata(meta_type=None, object_id=None, meta_key=None, meta_value=None, unique=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not meta_type) or (not meta_key) or (not php_is_numeric(object_id)):
        return False
    # end if
    object_id = absint(object_id)
    if (not object_id):
        return False
    # end if
    table = _get_meta_table(meta_type)
    if (not table):
        return False
    # end if
    meta_subtype = get_object_subtype(meta_type, object_id)
    column = sanitize_key(meta_type + "_id")
    #// expected_slashed ($meta_key)
    meta_key = wp_unslash(meta_key)
    meta_value = wp_unslash(meta_value)
    meta_value = sanitize_meta(meta_key, meta_value, meta_type, meta_subtype)
    #// 
    #// Filters whether to add metadata of a specific type.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 3.1.0
    #// 
    #// @param null|bool $check      Whether to allow adding metadata for the given type.
    #// @param int       $object_id  ID of the object metadata is for.
    #// @param string    $meta_key   Metadata key.
    #// @param mixed     $meta_value Metadata value. Must be serializable if non-scalar.
    #// @param bool      $unique     Whether the specified meta key should be unique for the object.
    #//
    check = apply_filters(str("add_") + str(meta_type) + str("_metadata"), None, object_id, meta_key, meta_value, unique)
    if None != check:
        return check
    # end if
    if unique and wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(table) + str(" WHERE meta_key = %s AND ") + str(column) + str(" = %d"), meta_key, object_id)):
        return False
    # end if
    _meta_value = meta_value
    meta_value = maybe_serialize(meta_value)
    #// 
    #// Fires immediately before meta of a specific type is added.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user).
    #// 
    #// @since 3.1.0
    #// 
    #// @param int    $object_id   ID of the object metadata is for.
    #// @param string $meta_key    Metadata key.
    #// @param mixed  $_meta_value Metadata value. Serialized if non-scalar.
    #//
    do_action(str("add_") + str(meta_type) + str("_meta"), object_id, meta_key, _meta_value)
    result = wpdb.insert(table, Array({column: object_id, "meta_key": meta_key, "meta_value": meta_value}))
    if (not result):
        return False
    # end if
    mid = php_int(wpdb.insert_id)
    wp_cache_delete(object_id, meta_type + "_meta")
    #// 
    #// Fires immediately after meta of a specific type is added.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user).
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $mid         The meta ID after successful update.
    #// @param int    $object_id   ID of the object metadata is for.
    #// @param string $meta_key    Metadata key.
    #// @param mixed  $_meta_value Metadata value. Serialized if non-scalar.
    #//
    do_action(str("added_") + str(meta_type) + str("_meta"), mid, object_id, meta_key, _meta_value)
    return mid
# end def add_metadata
#// 
#// Updates metadata for the specified object. If no value already exists for the specified object
#// ID and metadata key, the metadata will be added.
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $meta_type  Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $object_id  ID of the object metadata is for.
#// @param string $meta_key   Metadata key.
#// @param mixed  $meta_value Metadata value. Must be serializable if non-scalar.
#// @param mixed  $prev_value Optional. If specified, only update existing metadata entries
#// with this value. Otherwise, update all entries.
#// @return int|bool The new meta field ID if a field with the given key didn't exist and was
#// therefore added, true on successful update, false on failure.
#//
def update_metadata(meta_type=None, object_id=None, meta_key=None, meta_value=None, prev_value="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not meta_type) or (not meta_key) or (not php_is_numeric(object_id)):
        return False
    # end if
    object_id = absint(object_id)
    if (not object_id):
        return False
    # end if
    table = _get_meta_table(meta_type)
    if (not table):
        return False
    # end if
    meta_subtype = get_object_subtype(meta_type, object_id)
    column = sanitize_key(meta_type + "_id")
    id_column = "umeta_id" if "user" == meta_type else "meta_id"
    #// expected_slashed ($meta_key)
    raw_meta_key = meta_key
    meta_key = wp_unslash(meta_key)
    passed_value = meta_value
    meta_value = wp_unslash(meta_value)
    meta_value = sanitize_meta(meta_key, meta_value, meta_type, meta_subtype)
    #// 
    #// Filters whether to update metadata of a specific type.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 3.1.0
    #// 
    #// @param null|bool $check      Whether to allow updating metadata for the given type.
    #// @param int       $object_id  ID of the object metadata is for.
    #// @param string    $meta_key   Metadata key.
    #// @param mixed     $meta_value Metadata value. Must be serializable if non-scalar.
    #// @param mixed     $prev_value Optional. If specified, only update existing metadata entries
    #// with this value. Otherwise, update all entries.
    #//
    check = apply_filters(str("update_") + str(meta_type) + str("_metadata"), None, object_id, meta_key, meta_value, prev_value)
    if None != check:
        return php_bool(check)
    # end if
    #// Compare existing value to new value if no prev value given and the key exists only once.
    if php_empty(lambda : prev_value):
        old_value = get_metadata(meta_type, object_id, meta_key)
        if php_count(old_value) == 1:
            if old_value[0] == meta_value:
                return False
            # end if
        # end if
    # end if
    meta_ids = wpdb.get_col(wpdb.prepare(str("SELECT ") + str(id_column) + str(" FROM ") + str(table) + str(" WHERE meta_key = %s AND ") + str(column) + str(" = %d"), meta_key, object_id))
    if php_empty(lambda : meta_ids):
        return add_metadata(meta_type, object_id, raw_meta_key, passed_value)
    # end if
    _meta_value = meta_value
    meta_value = maybe_serialize(meta_value)
    data = compact("meta_value")
    where = Array({column: object_id, "meta_key": meta_key})
    if (not php_empty(lambda : prev_value)):
        prev_value = maybe_serialize(prev_value)
        where["meta_value"] = prev_value
    # end if
    for meta_id in meta_ids:
        #// 
        #// Fires immediately before updating metadata of a specific type.
        #// 
        #// The dynamic portion of the hook, `$meta_type`, refers to the meta
        #// object type (comment, post, term, or user).
        #// 
        #// @since 2.9.0
        #// 
        #// @param int    $meta_id     ID of the metadata entry to update.
        #// @param int    $object_id   ID of the object metadata is for.
        #// @param string $meta_key    Metadata key.
        #// @param mixed  $_meta_value Metadata value. Serialized if non-scalar.
        #//
        do_action(str("update_") + str(meta_type) + str("_meta"), meta_id, object_id, meta_key, _meta_value)
        if "post" == meta_type:
            #// 
            #// Fires immediately before updating a post's metadata.
            #// 
            #// @since 2.9.0
            #// 
            #// @param int    $meta_id    ID of metadata entry to update.
            #// @param int    $object_id  Post ID.
            #// @param string $meta_key   Metadata key.
            #// @param mixed  $meta_value Metadata value. This will be a PHP-serialized string representation of the value
            #// if the value is an array, an object, or itself a PHP-serialized string.
            #//
            do_action("update_postmeta", meta_id, object_id, meta_key, meta_value)
        # end if
    # end for
    result = wpdb.update(table, data, where)
    if (not result):
        return False
    # end if
    wp_cache_delete(object_id, meta_type + "_meta")
    for meta_id in meta_ids:
        #// 
        #// Fires immediately after updating metadata of a specific type.
        #// 
        #// The dynamic portion of the hook, `$meta_type`, refers to the meta
        #// object type (comment, post, term, or user).
        #// 
        #// @since 2.9.0
        #// 
        #// @param int    $meta_id     ID of updated metadata entry.
        #// @param int    $object_id   ID of the object metadata is for.
        #// @param string $meta_key    Metadata key.
        #// @param mixed  $_meta_value Metadata value. Serialized if non-scalar.
        #//
        do_action(str("updated_") + str(meta_type) + str("_meta"), meta_id, object_id, meta_key, _meta_value)
        if "post" == meta_type:
            #// 
            #// Fires immediately after updating a post's metadata.
            #// 
            #// @since 2.9.0
            #// 
            #// @param int    $meta_id    ID of updated metadata entry.
            #// @param int    $object_id  Post ID.
            #// @param string $meta_key   Metadata key.
            #// @param mixed  $meta_value Metadata value. This will be a PHP-serialized string representation of the value
            #// if the value is an array, an object, or itself a PHP-serialized string.
            #//
            do_action("updated_postmeta", meta_id, object_id, meta_key, meta_value)
        # end if
    # end for
    return True
# end def update_metadata
#// 
#// Deletes metadata for the specified object.
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $meta_type  Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $object_id  ID of the object metadata is for.
#// @param string $meta_key   Metadata key.
#// @param mixed  $meta_value Optional. Metadata value. Must be serializable if non-scalar.
#// If specified, only delete metadata entries with this value.
#// Otherwise, delete all entries with the specified meta_key.
#// Pass `null`, `false`, or an empty string to skip this check.
#// (For backward compatibility, it is not possible to pass an empty string
#// to delete those entries with an empty string for a value.)
#// @param bool   $delete_all Optional. If true, delete matching metadata entries for all objects,
#// ignoring the specified object_id. Otherwise, only delete
#// matching metadata entries for the specified object_id. Default false.
#// @return bool True on successful delete, false on failure.
#//
def delete_metadata(meta_type=None, object_id=None, meta_key=None, meta_value="", delete_all=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not meta_type) or (not meta_key) or (not php_is_numeric(object_id)) and (not delete_all):
        return False
    # end if
    object_id = absint(object_id)
    if (not object_id) and (not delete_all):
        return False
    # end if
    table = _get_meta_table(meta_type)
    if (not table):
        return False
    # end if
    type_column = sanitize_key(meta_type + "_id")
    id_column = "umeta_id" if "user" == meta_type else "meta_id"
    #// expected_slashed ($meta_key)
    meta_key = wp_unslash(meta_key)
    meta_value = wp_unslash(meta_value)
    #// 
    #// Filters whether to delete metadata of a specific type.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 3.1.0
    #// 
    #// @param null|bool $delete     Whether to allow metadata deletion of the given type.
    #// @param int       $object_id  ID of the object metadata is for.
    #// @param string    $meta_key   Metadata key.
    #// @param mixed     $meta_value Metadata value. Must be serializable if non-scalar.
    #// @param bool      $delete_all Whether to delete the matching metadata entries
    #// for all objects, ignoring the specified $object_id.
    #// Default false.
    #//
    check = apply_filters(str("delete_") + str(meta_type) + str("_metadata"), None, object_id, meta_key, meta_value, delete_all)
    if None != check:
        return php_bool(check)
    # end if
    _meta_value = meta_value
    meta_value = maybe_serialize(meta_value)
    query = wpdb.prepare(str("SELECT ") + str(id_column) + str(" FROM ") + str(table) + str(" WHERE meta_key = %s"), meta_key)
    if (not delete_all):
        query += wpdb.prepare(str(" AND ") + str(type_column) + str(" = %d"), object_id)
    # end if
    if "" != meta_value and None != meta_value and False != meta_value:
        query += wpdb.prepare(" AND meta_value = %s", meta_value)
    # end if
    meta_ids = wpdb.get_col(query)
    if (not php_count(meta_ids)):
        return False
    # end if
    if delete_all:
        if "" != meta_value and None != meta_value and False != meta_value:
            object_ids = wpdb.get_col(wpdb.prepare(str("SELECT ") + str(type_column) + str(" FROM ") + str(table) + str(" WHERE meta_key = %s AND meta_value = %s"), meta_key, meta_value))
        else:
            object_ids = wpdb.get_col(wpdb.prepare(str("SELECT ") + str(type_column) + str(" FROM ") + str(table) + str(" WHERE meta_key = %s"), meta_key))
        # end if
    # end if
    #// 
    #// Fires immediately before deleting metadata of a specific type.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user).
    #// 
    #// @since 3.1.0
    #// 
    #// @param string[] $meta_ids    An array of metadata entry IDs to delete.
    #// @param int      $object_id   ID of the object metadata is for.
    #// @param string   $meta_key    Metadata key.
    #// @param mixed    $_meta_value Metadata value. Serialized if non-scalar.
    #//
    do_action(str("delete_") + str(meta_type) + str("_meta"), meta_ids, object_id, meta_key, _meta_value)
    #// Old-style action.
    if "post" == meta_type:
        #// 
        #// Fires immediately before deleting metadata for a post.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string[] $meta_ids An array of metadata entry IDs to delete.
        #//
        do_action("delete_postmeta", meta_ids)
    # end if
    query = str("DELETE FROM ") + str(table) + str(" WHERE ") + str(id_column) + str(" IN( ") + php_implode(",", meta_ids) + " )"
    count = wpdb.query(query)
    if (not count):
        return False
    # end if
    if delete_all:
        for o_id in object_ids:
            wp_cache_delete(o_id, meta_type + "_meta")
        # end for
    else:
        wp_cache_delete(object_id, meta_type + "_meta")
    # end if
    #// 
    #// Fires immediately after deleting metadata of a specific type.
    #// 
    #// The dynamic portion of the hook name, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user).
    #// 
    #// @since 2.9.0
    #// 
    #// @param string[] $meta_ids    An array of metadata entry IDs to delete.
    #// @param int      $object_id   ID of the object metadata is for.
    #// @param string   $meta_key    Metadata key.
    #// @param mixed    $_meta_value Metadata value. Serialized if non-scalar.
    #//
    do_action(str("deleted_") + str(meta_type) + str("_meta"), meta_ids, object_id, meta_key, _meta_value)
    #// Old-style action.
    if "post" == meta_type:
        #// 
        #// Fires immediately after deleting metadata for a post.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string[] $meta_ids An array of metadata entry IDs to delete.
        #//
        do_action("deleted_postmeta", meta_ids)
    # end if
    return True
# end def delete_metadata
#// 
#// Retrieves metadata for the specified object.
#// 
#// @since 2.9.0
#// 
#// @param string $meta_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $object_id ID of the object metadata is for.
#// @param string $meta_key  Optional. Metadata key. If not specified, retrieve all metadata for
#// the specified object. Default empty.
#// @param bool   $single    Optional. If true, return only the first value of the specified meta_key.
#// This parameter has no effect if meta_key is not specified. Default false.
#// @return mixed Single metadata value, or array of values
#//
def get_metadata(meta_type=None, object_id=None, meta_key="", single=False, *args_):
    
    if (not meta_type) or (not php_is_numeric(object_id)):
        return False
    # end if
    object_id = absint(object_id)
    if (not object_id):
        return False
    # end if
    #// 
    #// Filters whether to retrieve metadata of a specific type.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 3.1.0
    #// 
    #// @param null|array|string $value     The value get_metadata() should return - a single metadata value,
    #// or an array of values.
    #// @param int               $object_id ID of the object metadata is for.
    #// @param string            $meta_key  Metadata key.
    #// @param bool              $single    Whether to return only the first value of the specified $meta_key.
    #//
    check = apply_filters(str("get_") + str(meta_type) + str("_metadata"), None, object_id, meta_key, single)
    if None != check:
        if single and php_is_array(check):
            return check[0]
        else:
            return check
        # end if
    # end if
    meta_cache = wp_cache_get(object_id, meta_type + "_meta")
    if (not meta_cache):
        meta_cache = update_meta_cache(meta_type, Array(object_id))
        if (php_isset(lambda : meta_cache[object_id])):
            meta_cache = meta_cache[object_id]
        else:
            meta_cache = None
        # end if
    # end if
    if (not meta_key):
        return meta_cache
    # end if
    if (php_isset(lambda : meta_cache[meta_key])):
        if single:
            return maybe_unserialize(meta_cache[meta_key][0])
        else:
            return php_array_map("maybe_unserialize", meta_cache[meta_key])
        # end if
    # end if
    if single:
        return ""
    else:
        return Array()
    # end if
# end def get_metadata
#// 
#// Determines if a meta key is set for a given object.
#// 
#// @since 3.3.0
#// 
#// @param string $meta_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $object_id ID of the object metadata is for.
#// @param string $meta_key  Metadata key.
#// @return bool True of the key is set, false if not.
#//
def metadata_exists(meta_type=None, object_id=None, meta_key=None, *args_):
    
    if (not meta_type) or (not php_is_numeric(object_id)):
        return False
    # end if
    object_id = absint(object_id)
    if (not object_id):
        return False
    # end if
    #// This filter is documented in wp-includes/meta.php
    check = apply_filters(str("get_") + str(meta_type) + str("_metadata"), None, object_id, meta_key, True)
    if None != check:
        return php_bool(check)
    # end if
    meta_cache = wp_cache_get(object_id, meta_type + "_meta")
    if (not meta_cache):
        meta_cache = update_meta_cache(meta_type, Array(object_id))
        meta_cache = meta_cache[object_id]
    # end if
    if (php_isset(lambda : meta_cache[meta_key])):
        return True
    # end if
    return False
# end def metadata_exists
#// 
#// Retrieves metadata by meta ID.
#// 
#// @since 3.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $meta_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $meta_id   ID for a specific meta row.
#// @return object|false Meta object or false.
#//
def get_metadata_by_mid(meta_type=None, meta_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not meta_type) or (not php_is_numeric(meta_id)) or floor(meta_id) != meta_id:
        return False
    # end if
    meta_id = php_intval(meta_id)
    if meta_id <= 0:
        return False
    # end if
    table = _get_meta_table(meta_type)
    if (not table):
        return False
    # end if
    id_column = "umeta_id" if "user" == meta_type else "meta_id"
    #// 
    #// Filters whether to retrieve metadata of a specific type by meta ID.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 5.0.0
    #// 
    #// @param mixed $value    The value get_metadata_by_mid() should return.
    #// @param int   $meta_id  Meta ID.
    #//
    check = apply_filters(str("get_") + str(meta_type) + str("_metadata_by_mid"), None, meta_id)
    if None != check:
        return check
    # end if
    meta = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(table) + str(" WHERE ") + str(id_column) + str(" = %d"), meta_id))
    if php_empty(lambda : meta):
        return False
    # end if
    if (php_isset(lambda : meta.meta_value)):
        meta.meta_value = maybe_unserialize(meta.meta_value)
    # end if
    return meta
# end def get_metadata_by_mid
#// 
#// Updates metadata by meta ID.
#// 
#// @since 3.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $meta_type  Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $meta_id    ID for a specific meta row.
#// @param string $meta_value Metadata value.
#// @param string $meta_key   Optional. You can provide a meta key to update it. Default false.
#// @return bool True on successful update, false on failure.
#//
def update_metadata_by_mid(meta_type=None, meta_id=None, meta_value=None, meta_key=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Make sure everything is valid.
    if (not meta_type) or (not php_is_numeric(meta_id)) or floor(meta_id) != meta_id:
        return False
    # end if
    meta_id = php_intval(meta_id)
    if meta_id <= 0:
        return False
    # end if
    table = _get_meta_table(meta_type)
    if (not table):
        return False
    # end if
    column = sanitize_key(meta_type + "_id")
    id_column = "umeta_id" if "user" == meta_type else "meta_id"
    #// 
    #// Filters whether to update metadata of a specific type by meta ID.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 5.0.0
    #// 
    #// @param null|bool   $check      Whether to allow updating metadata for the given type.
    #// @param int         $meta_id    Meta ID.
    #// @param mixed       $meta_value Meta value. Must be serializable if non-scalar.
    #// @param string|bool $meta_key   Meta key, if provided.
    #//
    check = apply_filters(str("update_") + str(meta_type) + str("_metadata_by_mid"), None, meta_id, meta_value, meta_key)
    if None != check:
        return php_bool(check)
    # end if
    #// Fetch the meta and go on if it's found.
    meta = get_metadata_by_mid(meta_type, meta_id)
    if meta:
        original_key = meta.meta_key
        object_id = meta.column
        #// If a new meta_key (last parameter) was specified, change the meta key,
        #// otherwise use the original key in the update statement.
        if False == meta_key:
            meta_key = original_key
        elif (not php_is_string(meta_key)):
            return False
        # end if
        meta_subtype = get_object_subtype(meta_type, object_id)
        #// Sanitize the meta.
        _meta_value = meta_value
        meta_value = sanitize_meta(meta_key, meta_value, meta_type, meta_subtype)
        meta_value = maybe_serialize(meta_value)
        #// Format the data query arguments.
        data = Array({"meta_key": meta_key, "meta_value": meta_value})
        #// Format the where query arguments.
        where = Array()
        where[id_column] = meta_id
        #// This action is documented in wp-includes/meta.php
        do_action(str("update_") + str(meta_type) + str("_meta"), meta_id, object_id, meta_key, _meta_value)
        if "post" == meta_type:
            #// This action is documented in wp-includes/meta.php
            do_action("update_postmeta", meta_id, object_id, meta_key, meta_value)
        # end if
        #// Run the update query, all fields in $data are %s, $where is a %d.
        result = wpdb.update(table, data, where, "%s", "%d")
        if (not result):
            return False
        # end if
        #// Clear the caches.
        wp_cache_delete(object_id, meta_type + "_meta")
        #// This action is documented in wp-includes/meta.php
        do_action(str("updated_") + str(meta_type) + str("_meta"), meta_id, object_id, meta_key, _meta_value)
        if "post" == meta_type:
            #// This action is documented in wp-includes/meta.php
            do_action("updated_postmeta", meta_id, object_id, meta_key, meta_value)
        # end if
        return True
    # end if
    #// And if the meta was not found.
    return False
# end def update_metadata_by_mid
#// 
#// Deletes metadata by meta ID.
#// 
#// @since 3.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $meta_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $meta_id   ID for a specific meta row.
#// @return bool True on successful delete, false on failure.
#//
def delete_metadata_by_mid(meta_type=None, meta_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Make sure everything is valid.
    if (not meta_type) or (not php_is_numeric(meta_id)) or floor(meta_id) != meta_id:
        return False
    # end if
    meta_id = php_intval(meta_id)
    if meta_id <= 0:
        return False
    # end if
    table = _get_meta_table(meta_type)
    if (not table):
        return False
    # end if
    #// Object and ID columns.
    column = sanitize_key(meta_type + "_id")
    id_column = "umeta_id" if "user" == meta_type else "meta_id"
    #// 
    #// Filters whether to delete metadata of a specific type by meta ID.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 5.0.0
    #// 
    #// @param null|bool $delete  Whether to allow metadata deletion of the given type.
    #// @param int       $meta_id Meta ID.
    #//
    check = apply_filters(str("delete_") + str(meta_type) + str("_metadata_by_mid"), None, meta_id)
    if None != check:
        return php_bool(check)
    # end if
    #// Fetch the meta and go on if it's found.
    meta = get_metadata_by_mid(meta_type, meta_id)
    if meta:
        object_id = php_int(meta.column)
        #// This action is documented in wp-includes/meta.php
        do_action(str("delete_") + str(meta_type) + str("_meta"), meta_id, object_id, meta.meta_key, meta.meta_value)
        #// Old-style action.
        if "post" == meta_type or "comment" == meta_type:
            #// 
            #// Fires immediately before deleting post or comment metadata of a specific type.
            #// 
            #// The dynamic portion of the hook, `$meta_type`, refers to the meta
            #// object type (post or comment).
            #// 
            #// @since 3.4.0
            #// 
            #// @param int $meta_id ID of the metadata entry to delete.
            #//
            do_action(str("delete_") + str(meta_type) + str("meta"), meta_id)
        # end if
        #// Run the query, will return true if deleted, false otherwise.
        result = php_bool(wpdb.delete(table, Array({id_column: meta_id})))
        #// Clear the caches.
        wp_cache_delete(object_id, meta_type + "_meta")
        #// This action is documented in wp-includes/meta.php
        do_action(str("deleted_") + str(meta_type) + str("_meta"), meta_id, object_id, meta.meta_key, meta.meta_value)
        #// Old-style action.
        if "post" == meta_type or "comment" == meta_type:
            #// 
            #// Fires immediately after deleting post or comment metadata of a specific type.
            #// 
            #// The dynamic portion of the hook, `$meta_type`, refers to the meta
            #// object type (post or comment).
            #// 
            #// @since 3.4.0
            #// 
            #// @param int $meta_ids Deleted metadata entry ID.
            #//
            do_action(str("deleted_") + str(meta_type) + str("meta"), meta_id)
        # end if
        return result
    # end if
    #// Meta ID was not found.
    return False
# end def delete_metadata_by_mid
#// 
#// Updates the metadata cache for the specified objects.
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string       $meta_type  Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param string|int[] $object_ids Array or comma delimited list of object IDs to update cache for.
#// @return array|false Metadata cache for the specified objects, or false on failure.
#//
def update_meta_cache(meta_type=None, object_ids=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not meta_type) or (not object_ids):
        return False
    # end if
    table = _get_meta_table(meta_type)
    if (not table):
        return False
    # end if
    column = sanitize_key(meta_type + "_id")
    if (not php_is_array(object_ids)):
        object_ids = php_preg_replace("|[^0-9,]|", "", object_ids)
        object_ids = php_explode(",", object_ids)
    # end if
    object_ids = php_array_map("intval", object_ids)
    #// 
    #// Filters whether to update the metadata cache of a specific type.
    #// 
    #// The dynamic portion of the hook, `$meta_type`, refers to the meta
    #// object type (comment, post, term, or user). Returning a non-null value
    #// will effectively short-circuit the function.
    #// 
    #// @since 5.0.0
    #// 
    #// @param mixed $check      Whether to allow updating the meta cache of the given type.
    #// @param int[] $object_ids Array of object IDs to update the meta cache for.
    #//
    check = apply_filters(str("update_") + str(meta_type) + str("_metadata_cache"), None, object_ids)
    if None != check:
        return php_bool(check)
    # end if
    cache_key = meta_type + "_meta"
    ids = Array()
    cache = Array()
    for id in object_ids:
        cached_object = wp_cache_get(id, cache_key)
        if False == cached_object:
            ids[-1] = id
        else:
            cache[id] = cached_object
        # end if
    # end for
    if php_empty(lambda : ids):
        return cache
    # end if
    #// Get meta info.
    id_list = join(",", ids)
    id_column = "umeta_id" if "user" == meta_type else "meta_id"
    meta_list = wpdb.get_results(str("SELECT ") + str(column) + str(", meta_key, meta_value FROM ") + str(table) + str(" WHERE ") + str(column) + str(" IN (") + str(id_list) + str(") ORDER BY ") + str(id_column) + str(" ASC"), ARRAY_A)
    if (not php_empty(lambda : meta_list)):
        for metarow in meta_list:
            mpid = php_intval(metarow[column])
            mkey = metarow["meta_key"]
            mval = metarow["meta_value"]
            #// Force subkeys to be array type.
            if (not (php_isset(lambda : cache[mpid]))) or (not php_is_array(cache[mpid])):
                cache[mpid] = Array()
            # end if
            if (not (php_isset(lambda : cache[mpid][mkey]))) or (not php_is_array(cache[mpid][mkey])):
                cache[mpid][mkey] = Array()
            # end if
            #// Add a value to the current pid/key.
            cache[mpid][mkey][-1] = mval
        # end for
    # end if
    for id in ids:
        if (not (php_isset(lambda : cache[id]))):
            cache[id] = Array()
        # end if
        wp_cache_add(id, cache[id], cache_key)
    # end for
    return cache
# end def update_meta_cache
#// 
#// Retrieves the queue for lazy-loading metadata.
#// 
#// @since 4.5.0
#// 
#// @return WP_Metadata_Lazyloader $lazyloader Metadata lazyloader queue.
#//
def wp_metadata_lazyloader(*args_):
    
    wp_metadata_lazyloader.wp_metadata_lazyloader = None
    if None == wp_metadata_lazyloader.wp_metadata_lazyloader:
        wp_metadata_lazyloader.wp_metadata_lazyloader = php_new_class("WP_Metadata_Lazyloader", lambda : WP_Metadata_Lazyloader())
    # end if
    return wp_metadata_lazyloader.wp_metadata_lazyloader
# end def wp_metadata_lazyloader
#// 
#// Given a meta query, generates SQL clauses to be appended to a main query.
#// 
#// @since 3.2.0
#// 
#// @see WP_Meta_Query
#// 
#// @param array $meta_query         A meta query.
#// @param string $type              Type of meta.
#// @param string $primary_table     Primary database table name.
#// @param string $primary_id_column Primary ID column name.
#// @param object $context           Optional. The main query object
#// @return array Associative array of `JOIN` and `WHERE` SQL.
#//
def get_meta_sql(meta_query=None, type=None, primary_table=None, primary_id_column=None, context=None, *args_):
    
    meta_query_obj = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query(meta_query))
    return meta_query_obj.get_sql(type, primary_table, primary_id_column, context)
# end def get_meta_sql
#// 
#// Retrieves the name of the metadata table for the specified object type.
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @return string|false Metadata table name, or false if no metadata table exists
#//
def _get_meta_table(type=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    table_name = type + "meta"
    if php_empty(lambda : wpdb.table_name):
        return False
    # end if
    return wpdb.table_name
# end def _get_meta_table
#// 
#// Determines whether a meta key is considered protected.
#// 
#// @since 3.1.3
#// 
#// @param string $meta_key  Metadata key.
#// @param string $meta_type Optional. Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table. Default empty.
#// @return bool Whether the meta key is considered protected.
#//
def is_protected_meta(meta_key=None, meta_type="", *args_):
    
    protected = "_" == meta_key[0]
    #// 
    #// Filters whether a meta key is considered protected.
    #// 
    #// @since 3.2.0
    #// 
    #// @param bool   $protected Whether the key is considered protected.
    #// @param string $meta_key  Metadata key.
    #// @param string $meta_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
    #// or any other object type with an associated meta table.
    #//
    return apply_filters("is_protected_meta", protected, meta_key, meta_type)
# end def is_protected_meta
#// 
#// Sanitizes meta value.
#// 
#// @since 3.1.3
#// @since 4.9.8 The `$object_subtype` parameter was added.
#// 
#// @param string $meta_key       Metadata key.
#// @param mixed  $meta_value     Metadata value to sanitize.
#// @param string $object_type    Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param string $object_subtype Optional. The subtype of the object type.
#// @return mixed Sanitized $meta_value.
#//
def sanitize_meta(meta_key=None, meta_value=None, object_type=None, object_subtype="", *args_):
    
    if (not php_empty(lambda : object_subtype)) and has_filter(str("sanitize_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype)):
        #// 
        #// Filters the sanitization of a specific meta key of a specific meta type and subtype.
        #// 
        #// The dynamic portions of the hook name, `$object_type`, `$meta_key`,
        #// and `$object_subtype`, refer to the metadata object type (comment, post, term, or user),
        #// the meta key value, and the object subtype respectively.
        #// 
        #// @since 4.9.8
        #// 
        #// @param mixed  $meta_value     Metadata value to sanitize.
        #// @param string $meta_key       Metadata key.
        #// @param string $object_type    Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
        #// or any other object type with an associated meta table.
        #// @param string $object_subtype Object subtype.
        #//
        return apply_filters(str("sanitize_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype), meta_value, meta_key, object_type, object_subtype)
    # end if
    #// 
    #// Filters the sanitization of a specific meta key of a specific meta type.
    #// 
    #// The dynamic portions of the hook name, `$meta_type`, and `$meta_key`,
    #// refer to the metadata object type (comment, post, term, or user) and the meta
    #// key value, respectively.
    #// 
    #// @since 3.3.0
    #// 
    #// @param mixed  $meta_value  Metadata value to sanitize.
    #// @param string $meta_key    Metadata key.
    #// @param string $object_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
    #// or any other object type with an associated meta table.
    #//
    return apply_filters(str("sanitize_") + str(object_type) + str("_meta_") + str(meta_key), meta_value, meta_key, object_type)
# end def sanitize_meta
#// 
#// Registers a meta key.
#// 
#// It is recommended to register meta keys for a specific combination of object type and object subtype. If passing
#// an object subtype is omitted, the meta key will be registered for the entire object type, however it can be partly
#// overridden in case a more specific meta key of the same name exists for the same object type and a subtype.
#// 
#// If an object type does not support any subtypes, such as users or comments, you should commonly call this function
#// without passing a subtype.
#// 
#// @since 3.3.0
#// @since 4.6.0 {@link https://core.trac.wordpress.org/ticket/35658 Modified
#// to support an array of data to attach to registered meta keys}. Previous arguments for
#// `$sanitize_callback` and `$auth_callback` have been folded into this array.
#// @since 4.9.8 The `$object_subtype` argument was added to the arguments array.
#// @since 5.3.0 Valid meta types expanded to include "array" and "object".
#// 
#// @param string $object_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param string $meta_key    Meta key to register.
#// @param array  $args {
#// Data used to describe the meta key when registered.
#// 
#// @type string     $object_subtype    A subtype; e.g. if the object type is "post", the post type. If left empty,
#// the meta key will be registered on the entire object type. Default empty.
#// @type string     $type              The type of data associated with this meta key.
#// Valid values are 'string', 'boolean', 'integer', 'number', 'array', and 'object'.
#// @type string     $description       A description of the data attached to this meta key.
#// @type bool       $single            Whether the meta key has one value per object, or an array of values per object.
#// @type string     $sanitize_callback A function or method to call when sanitizing `$meta_key` data.
#// @type string     $auth_callback     Optional. A function or method to call when performing edit_post_meta,
#// add_post_meta, and delete_post_meta capability checks.
#// @type bool|array $show_in_rest      Whether data associated with this meta key can be considered public and
#// should be accessible via the REST API. A custom post type must also declare
#// support for custom fields for registered meta to be accessible via REST.
#// When registering complex meta values this argument may optionally be an
#// array with 'schema' or 'prepare_callback' keys instead of a boolean.
#// }
#// @param string|array $deprecated Deprecated. Use `$args` instead.
#// @return bool True if the meta key was successfully registered in the global array, false if not.
#// Registering a meta key with distinct sanitize and auth callbacks will fire those callbacks,
#// but will not add to the global registry.
#//
def register_meta(object_type=None, meta_key=None, args=None, deprecated=None, *args_):
    
    global wp_meta_keys
    php_check_if_defined("wp_meta_keys")
    if (not php_is_array(wp_meta_keys)):
        wp_meta_keys = Array()
    # end if
    defaults = Array({"object_subtype": "", "type": "string", "description": "", "single": False, "sanitize_callback": None, "auth_callback": None, "show_in_rest": False})
    #// There used to be individual args for sanitize and auth callbacks.
    has_old_sanitize_cb = False
    has_old_auth_cb = False
    if php_is_callable(args):
        args = Array({"sanitize_callback": args})
        has_old_sanitize_cb = True
    else:
        args = args
    # end if
    if php_is_callable(deprecated):
        args["auth_callback"] = deprecated
        has_old_auth_cb = True
    # end if
    #// 
    #// Filters the registration arguments when registering meta.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array  $args        Array of meta registration arguments.
    #// @param array  $defaults    Array of default arguments.
    #// @param string $object_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
    #// or any other object type with an associated meta table.
    #// @param string $meta_key    Meta key.
    #//
    args = apply_filters("register_meta_args", args, defaults, object_type, meta_key)
    args = wp_parse_args(args, defaults)
    #// Require an item schema when registering array meta.
    if False != args["show_in_rest"] and "array" == args["type"]:
        if (not php_is_array(args["show_in_rest"])) or (not (php_isset(lambda : args["show_in_rest"]["schema"]["items"]))):
            _doing_it_wrong(__FUNCTION__, __("When registering an \"array\" meta type to show in the REST API, you must specify the schema for each array item in \"show_in_rest.schema.items\"."), "5.3.0")
            return False
        # end if
    # end if
    object_subtype = args["object_subtype"] if (not php_empty(lambda : args["object_subtype"])) else ""
    #// If `auth_callback` is not provided, fall back to `is_protected_meta()`.
    if php_empty(lambda : args["auth_callback"]):
        if is_protected_meta(meta_key, object_type):
            args["auth_callback"] = "__return_false"
        else:
            args["auth_callback"] = "__return_true"
        # end if
    # end if
    #// Back-compat: old sanitize and auth callbacks are applied to all of an object type.
    if php_is_callable(args["sanitize_callback"]):
        if (not php_empty(lambda : object_subtype)):
            add_filter(str("sanitize_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype), args["sanitize_callback"], 10, 4)
        else:
            add_filter(str("sanitize_") + str(object_type) + str("_meta_") + str(meta_key), args["sanitize_callback"], 10, 3)
        # end if
    # end if
    if php_is_callable(args["auth_callback"]):
        if (not php_empty(lambda : object_subtype)):
            add_filter(str("auth_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype), args["auth_callback"], 10, 6)
        else:
            add_filter(str("auth_") + str(object_type) + str("_meta_") + str(meta_key), args["auth_callback"], 10, 6)
        # end if
    # end if
    #// Global registry only contains meta keys registered with the array of arguments added in 4.6.0.
    if (not has_old_auth_cb) and (not has_old_sanitize_cb):
        args["object_subtype"] = None
        wp_meta_keys[object_type][object_subtype][meta_key] = args
        return True
    # end if
    return False
# end def register_meta
#// 
#// Checks if a meta key is registered.
#// 
#// @since 4.6.0
#// @since 4.9.8 The `$object_subtype` parameter was added.
#// 
#// @param string $object_type    Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param string $meta_key       Metadata key.
#// @param string $object_subtype Optional. The subtype of the object type.
#// @return bool True if the meta key is registered to the object type and, if provided,
#// the object subtype. False if not.
#//
def registered_meta_key_exists(object_type=None, meta_key=None, object_subtype="", *args_):
    
    meta_keys = get_registered_meta_keys(object_type, object_subtype)
    return (php_isset(lambda : meta_keys[meta_key]))
# end def registered_meta_key_exists
#// 
#// Unregisters a meta key from the list of registered keys.
#// 
#// @since 4.6.0
#// @since 4.9.8 The `$object_subtype` parameter was added.
#// 
#// @param string $object_type    Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param string $meta_key       Metadata key.
#// @param string $object_subtype Optional. The subtype of the object type.
#// @return bool True if successful. False if the meta key was not registered.
#//
def unregister_meta_key(object_type=None, meta_key=None, object_subtype="", *args_):
    
    global wp_meta_keys
    php_check_if_defined("wp_meta_keys")
    if (not registered_meta_key_exists(object_type, meta_key, object_subtype)):
        return False
    # end if
    args = wp_meta_keys[object_type][object_subtype][meta_key]
    if (php_isset(lambda : args["sanitize_callback"])) and php_is_callable(args["sanitize_callback"]):
        if (not php_empty(lambda : object_subtype)):
            remove_filter(str("sanitize_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype), args["sanitize_callback"])
        else:
            remove_filter(str("sanitize_") + str(object_type) + str("_meta_") + str(meta_key), args["sanitize_callback"])
        # end if
    # end if
    if (php_isset(lambda : args["auth_callback"])) and php_is_callable(args["auth_callback"]):
        if (not php_empty(lambda : object_subtype)):
            remove_filter(str("auth_") + str(object_type) + str("_meta_") + str(meta_key) + str("_for_") + str(object_subtype), args["auth_callback"])
        else:
            remove_filter(str("auth_") + str(object_type) + str("_meta_") + str(meta_key), args["auth_callback"])
        # end if
    # end if
    wp_meta_keys[object_type][object_subtype][meta_key] = None
    #// Do some clean up.
    if php_empty(lambda : wp_meta_keys[object_type][object_subtype]):
        wp_meta_keys[object_type][object_subtype] = None
    # end if
    if php_empty(lambda : wp_meta_keys[object_type]):
        wp_meta_keys[object_type] = None
    # end if
    return True
# end def unregister_meta_key
#// 
#// Retrieves a list of registered meta keys for an object type.
#// 
#// @since 4.6.0
#// @since 4.9.8 The `$object_subtype` parameter was added.
#// 
#// @param string $object_type    Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param string $object_subtype Optional. The subtype of the object type.
#// @return string[] List of registered meta keys.
#//
def get_registered_meta_keys(object_type=None, object_subtype="", *args_):
    
    global wp_meta_keys
    php_check_if_defined("wp_meta_keys")
    if (not php_is_array(wp_meta_keys)) or (not (php_isset(lambda : wp_meta_keys[object_type]))) or (not (php_isset(lambda : wp_meta_keys[object_type][object_subtype]))):
        return Array()
    # end if
    return wp_meta_keys[object_type][object_subtype]
# end def get_registered_meta_keys
#// 
#// Retrieves registered metadata for a specified object.
#// 
#// The results include both meta that is registered specifically for the
#// object's subtype and meta that is registered for the entire object type.
#// 
#// @since 4.6.0
#// 
#// @param string $object_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $object_id   ID of the object the metadata is for.
#// @param string $meta_key    Optional. Registered metadata key. If not specified, retrieve all registered
#// metadata for the specified object.
#// @return mixed A single value or array of values for a key if specified. An array of all registered keys
#// and values for an object ID if not. False if a given $meta_key is not registered.
#//
def get_registered_metadata(object_type=None, object_id=None, meta_key="", *args_):
    
    object_subtype = get_object_subtype(object_type, object_id)
    if (not php_empty(lambda : meta_key)):
        if (not php_empty(lambda : object_subtype)) and (not registered_meta_key_exists(object_type, meta_key, object_subtype)):
            object_subtype = ""
        # end if
        if (not registered_meta_key_exists(object_type, meta_key, object_subtype)):
            return False
        # end if
        meta_keys = get_registered_meta_keys(object_type, object_subtype)
        meta_key_data = meta_keys[meta_key]
        data = get_metadata(object_type, object_id, meta_key, meta_key_data["single"])
        return data
    # end if
    data = get_metadata(object_type, object_id)
    if (not data):
        return Array()
    # end if
    meta_keys = get_registered_meta_keys(object_type)
    if (not php_empty(lambda : object_subtype)):
        meta_keys = php_array_merge(meta_keys, get_registered_meta_keys(object_type, object_subtype))
    # end if
    return php_array_intersect_key(data, meta_keys)
# end def get_registered_metadata
#// 
#// Filters out `register_meta()` args based on a whitelist.
#// 
#// `register_meta()` args may change over time, so requiring the whitelist
#// to be explicitly turned off is a warranty seal of sorts.
#// 
#// @access private
#// @since 4.6.0
#// 
#// @param array $args         Arguments from `register_meta()`.
#// @param array $default_args Default arguments for `register_meta()`.
#// @return array Filtered arguments.
#//
def _wp_register_meta_args_whitelist(args=None, default_args=None, *args_):
    
    return php_array_intersect_key(args, default_args)
# end def _wp_register_meta_args_whitelist
#// 
#// Returns the object subtype for a given object ID of a specific type.
#// 
#// @since 4.9.8
#// 
#// @param string $object_type Type of object metadata is for. Accepts 'post', 'comment', 'term', 'user',
#// or any other object type with an associated meta table.
#// @param int    $object_id   ID of the object to retrieve its subtype.
#// @return string The object subtype or an empty string if unspecified subtype.
#//
def get_object_subtype(object_type=None, object_id=None, *args_):
    
    object_id = php_int(object_id)
    object_subtype = ""
    for case in Switch(object_type):
        if case("post"):
            post_type = get_post_type(object_id)
            if (not php_empty(lambda : post_type)):
                object_subtype = post_type
            # end if
            break
        # end if
        if case("term"):
            term = get_term(object_id)
            if (not type(term).__name__ == "WP_Term"):
                break
            # end if
            object_subtype = term.taxonomy
            break
        # end if
        if case("comment"):
            comment = get_comment(object_id)
            if (not comment):
                break
            # end if
            object_subtype = "comment"
            break
        # end if
        if case("user"):
            user = get_user_by("id", object_id)
            if (not user):
                break
            # end if
            object_subtype = "user"
            break
        # end if
    # end for
    #// 
    #// Filters the object subtype identifier for a non standard object type.
    #// 
    #// The dynamic portion of the hook, `$object_type`, refers to the object
    #// type (post, comment, term, or user).
    #// 
    #// @since 4.9.8
    #// 
    #// @param string $object_subtype Empty string to override.
    #// @param int    $object_id      ID of the object to get the subtype for.
    #//
    return apply_filters(str("get_object_subtype_") + str(object_type), object_subtype, object_id)
# end def get_object_subtype
