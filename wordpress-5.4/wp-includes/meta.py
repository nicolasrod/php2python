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
def add_metadata(meta_type_=None, object_id_=None, meta_key_=None, meta_value_=None, unique_=None, *_args_):
    if unique_ is None:
        unique_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not meta_type_) or (not meta_key_) or (not php_is_numeric(object_id_)):
        return False
    # end if
    object_id_ = absint(object_id_)
    if (not object_id_):
        return False
    # end if
    table_ = _get_meta_table(meta_type_)
    if (not table_):
        return False
    # end if
    meta_subtype_ = get_object_subtype(meta_type_, object_id_)
    column_ = sanitize_key(meta_type_ + "_id")
    #// expected_slashed ($meta_key)
    meta_key_ = wp_unslash(meta_key_)
    meta_value_ = wp_unslash(meta_value_)
    meta_value_ = sanitize_meta(meta_key_, meta_value_, meta_type_, meta_subtype_)
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
    check_ = apply_filters(str("add_") + str(meta_type_) + str("_metadata"), None, object_id_, meta_key_, meta_value_, unique_)
    if None != check_:
        return check_
    # end if
    if unique_ and wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(table_) + str(" WHERE meta_key = %s AND ") + str(column_) + str(" = %d"), meta_key_, object_id_)):
        return False
    # end if
    _meta_value_ = meta_value_
    meta_value_ = maybe_serialize(meta_value_)
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
    do_action(str("add_") + str(meta_type_) + str("_meta"), object_id_, meta_key_, _meta_value_)
    result_ = wpdb_.insert(table_, Array({column_: object_id_, "meta_key": meta_key_, "meta_value": meta_value_}))
    if (not result_):
        return False
    # end if
    mid_ = php_int(wpdb_.insert_id)
    wp_cache_delete(object_id_, meta_type_ + "_meta")
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
    do_action(str("added_") + str(meta_type_) + str("_meta"), mid_, object_id_, meta_key_, _meta_value_)
    return mid_
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
def update_metadata(meta_type_=None, object_id_=None, meta_key_=None, meta_value_=None, prev_value_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not meta_type_) or (not meta_key_) or (not php_is_numeric(object_id_)):
        return False
    # end if
    object_id_ = absint(object_id_)
    if (not object_id_):
        return False
    # end if
    table_ = _get_meta_table(meta_type_)
    if (not table_):
        return False
    # end if
    meta_subtype_ = get_object_subtype(meta_type_, object_id_)
    column_ = sanitize_key(meta_type_ + "_id")
    id_column_ = "umeta_id" if "user" == meta_type_ else "meta_id"
    #// expected_slashed ($meta_key)
    raw_meta_key_ = meta_key_
    meta_key_ = wp_unslash(meta_key_)
    passed_value_ = meta_value_
    meta_value_ = wp_unslash(meta_value_)
    meta_value_ = sanitize_meta(meta_key_, meta_value_, meta_type_, meta_subtype_)
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
    check_ = apply_filters(str("update_") + str(meta_type_) + str("_metadata"), None, object_id_, meta_key_, meta_value_, prev_value_)
    if None != check_:
        return php_bool(check_)
    # end if
    #// Compare existing value to new value if no prev value given and the key exists only once.
    if php_empty(lambda : prev_value_):
        old_value_ = get_metadata(meta_type_, object_id_, meta_key_)
        if php_count(old_value_) == 1:
            if old_value_[0] == meta_value_:
                return False
            # end if
        # end if
    # end if
    meta_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ") + str(id_column_) + str(" FROM ") + str(table_) + str(" WHERE meta_key = %s AND ") + str(column_) + str(" = %d"), meta_key_, object_id_))
    if php_empty(lambda : meta_ids_):
        return add_metadata(meta_type_, object_id_, raw_meta_key_, passed_value_)
    # end if
    _meta_value_ = meta_value_
    meta_value_ = maybe_serialize(meta_value_)
    data_ = php_compact("meta_value_")
    where_ = Array({column_: object_id_, "meta_key": meta_key_})
    if (not php_empty(lambda : prev_value_)):
        prev_value_ = maybe_serialize(prev_value_)
        where_["meta_value"] = prev_value_
    # end if
    for meta_id_ in meta_ids_:
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
        do_action(str("update_") + str(meta_type_) + str("_meta"), meta_id_, object_id_, meta_key_, _meta_value_)
        if "post" == meta_type_:
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
            do_action("update_postmeta", meta_id_, object_id_, meta_key_, meta_value_)
        # end if
    # end for
    result_ = wpdb_.update(table_, data_, where_)
    if (not result_):
        return False
    # end if
    wp_cache_delete(object_id_, meta_type_ + "_meta")
    for meta_id_ in meta_ids_:
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
        do_action(str("updated_") + str(meta_type_) + str("_meta"), meta_id_, object_id_, meta_key_, _meta_value_)
        if "post" == meta_type_:
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
            do_action("updated_postmeta", meta_id_, object_id_, meta_key_, meta_value_)
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
def delete_metadata(meta_type_=None, object_id_=None, meta_key_=None, meta_value_="", delete_all_=None, *_args_):
    if delete_all_ is None:
        delete_all_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not meta_type_) or (not meta_key_) or (not php_is_numeric(object_id_)) and (not delete_all_):
        return False
    # end if
    object_id_ = absint(object_id_)
    if (not object_id_) and (not delete_all_):
        return False
    # end if
    table_ = _get_meta_table(meta_type_)
    if (not table_):
        return False
    # end if
    type_column_ = sanitize_key(meta_type_ + "_id")
    id_column_ = "umeta_id" if "user" == meta_type_ else "meta_id"
    #// expected_slashed ($meta_key)
    meta_key_ = wp_unslash(meta_key_)
    meta_value_ = wp_unslash(meta_value_)
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
    check_ = apply_filters(str("delete_") + str(meta_type_) + str("_metadata"), None, object_id_, meta_key_, meta_value_, delete_all_)
    if None != check_:
        return php_bool(check_)
    # end if
    _meta_value_ = meta_value_
    meta_value_ = maybe_serialize(meta_value_)
    query_ = wpdb_.prepare(str("SELECT ") + str(id_column_) + str(" FROM ") + str(table_) + str(" WHERE meta_key = %s"), meta_key_)
    if (not delete_all_):
        query_ += wpdb_.prepare(str(" AND ") + str(type_column_) + str(" = %d"), object_id_)
    # end if
    if "" != meta_value_ and None != meta_value_ and False != meta_value_:
        query_ += wpdb_.prepare(" AND meta_value = %s", meta_value_)
    # end if
    meta_ids_ = wpdb_.get_col(query_)
    if (not php_count(meta_ids_)):
        return False
    # end if
    if delete_all_:
        if "" != meta_value_ and None != meta_value_ and False != meta_value_:
            object_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ") + str(type_column_) + str(" FROM ") + str(table_) + str(" WHERE meta_key = %s AND meta_value = %s"), meta_key_, meta_value_))
        else:
            object_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ") + str(type_column_) + str(" FROM ") + str(table_) + str(" WHERE meta_key = %s"), meta_key_))
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
    do_action(str("delete_") + str(meta_type_) + str("_meta"), meta_ids_, object_id_, meta_key_, _meta_value_)
    #// Old-style action.
    if "post" == meta_type_:
        #// 
        #// Fires immediately before deleting metadata for a post.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string[] $meta_ids An array of metadata entry IDs to delete.
        #//
        do_action("delete_postmeta", meta_ids_)
    # end if
    query_ = str("DELETE FROM ") + str(table_) + str(" WHERE ") + str(id_column_) + str(" IN( ") + php_implode(",", meta_ids_) + " )"
    count_ = wpdb_.query(query_)
    if (not count_):
        return False
    # end if
    if delete_all_:
        for o_id_ in object_ids_:
            wp_cache_delete(o_id_, meta_type_ + "_meta")
        # end for
    else:
        wp_cache_delete(object_id_, meta_type_ + "_meta")
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
    do_action(str("deleted_") + str(meta_type_) + str("_meta"), meta_ids_, object_id_, meta_key_, _meta_value_)
    #// Old-style action.
    if "post" == meta_type_:
        #// 
        #// Fires immediately after deleting metadata for a post.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string[] $meta_ids An array of metadata entry IDs to delete.
        #//
        do_action("deleted_postmeta", meta_ids_)
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
def get_metadata(meta_type_=None, object_id_=None, meta_key_="", single_=None, *_args_):
    if single_ is None:
        single_ = False
    # end if
    
    if (not meta_type_) or (not php_is_numeric(object_id_)):
        return False
    # end if
    object_id_ = absint(object_id_)
    if (not object_id_):
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
    check_ = apply_filters(str("get_") + str(meta_type_) + str("_metadata"), None, object_id_, meta_key_, single_)
    if None != check_:
        if single_ and php_is_array(check_):
            return check_[0]
        else:
            return check_
        # end if
    # end if
    meta_cache_ = wp_cache_get(object_id_, meta_type_ + "_meta")
    if (not meta_cache_):
        meta_cache_ = update_meta_cache(meta_type_, Array(object_id_))
        if (php_isset(lambda : meta_cache_[object_id_])):
            meta_cache_ = meta_cache_[object_id_]
        else:
            meta_cache_ = None
        # end if
    # end if
    if (not meta_key_):
        return meta_cache_
    # end if
    if (php_isset(lambda : meta_cache_[meta_key_])):
        if single_:
            return maybe_unserialize(meta_cache_[meta_key_][0])
        else:
            return php_array_map("maybe_unserialize", meta_cache_[meta_key_])
        # end if
    # end if
    if single_:
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
def metadata_exists(meta_type_=None, object_id_=None, meta_key_=None, *_args_):
    
    
    if (not meta_type_) or (not php_is_numeric(object_id_)):
        return False
    # end if
    object_id_ = absint(object_id_)
    if (not object_id_):
        return False
    # end if
    #// This filter is documented in wp-includes/meta.php
    check_ = apply_filters(str("get_") + str(meta_type_) + str("_metadata"), None, object_id_, meta_key_, True)
    if None != check_:
        return php_bool(check_)
    # end if
    meta_cache_ = wp_cache_get(object_id_, meta_type_ + "_meta")
    if (not meta_cache_):
        meta_cache_ = update_meta_cache(meta_type_, Array(object_id_))
        meta_cache_ = meta_cache_[object_id_]
    # end if
    if (php_isset(lambda : meta_cache_[meta_key_])):
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
def get_metadata_by_mid(meta_type_=None, meta_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not meta_type_) or (not php_is_numeric(meta_id_)) or floor(meta_id_) != meta_id_:
        return False
    # end if
    meta_id_ = php_intval(meta_id_)
    if meta_id_ <= 0:
        return False
    # end if
    table_ = _get_meta_table(meta_type_)
    if (not table_):
        return False
    # end if
    id_column_ = "umeta_id" if "user" == meta_type_ else "meta_id"
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
    check_ = apply_filters(str("get_") + str(meta_type_) + str("_metadata_by_mid"), None, meta_id_)
    if None != check_:
        return check_
    # end if
    meta_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(table_) + str(" WHERE ") + str(id_column_) + str(" = %d"), meta_id_))
    if php_empty(lambda : meta_):
        return False
    # end if
    if (php_isset(lambda : meta_.meta_value)):
        meta_.meta_value = maybe_unserialize(meta_.meta_value)
    # end if
    return meta_
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
def update_metadata_by_mid(meta_type_=None, meta_id_=None, meta_value_=None, meta_key_=None, *_args_):
    if meta_key_ is None:
        meta_key_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Make sure everything is valid.
    if (not meta_type_) or (not php_is_numeric(meta_id_)) or floor(meta_id_) != meta_id_:
        return False
    # end if
    meta_id_ = php_intval(meta_id_)
    if meta_id_ <= 0:
        return False
    # end if
    table_ = _get_meta_table(meta_type_)
    if (not table_):
        return False
    # end if
    column_ = sanitize_key(meta_type_ + "_id")
    id_column_ = "umeta_id" if "user" == meta_type_ else "meta_id"
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
    check_ = apply_filters(str("update_") + str(meta_type_) + str("_metadata_by_mid"), None, meta_id_, meta_value_, meta_key_)
    if None != check_:
        return php_bool(check_)
    # end if
    #// Fetch the meta and go on if it's found.
    meta_ = get_metadata_by_mid(meta_type_, meta_id_)
    if meta_:
        original_key_ = meta_.meta_key
        object_id_ = meta_.column_
        #// If a new meta_key (last parameter) was specified, change the meta key,
        #// otherwise use the original key in the update statement.
        if False == meta_key_:
            meta_key_ = original_key_
        elif (not php_is_string(meta_key_)):
            return False
        # end if
        meta_subtype_ = get_object_subtype(meta_type_, object_id_)
        #// Sanitize the meta.
        _meta_value_ = meta_value_
        meta_value_ = sanitize_meta(meta_key_, meta_value_, meta_type_, meta_subtype_)
        meta_value_ = maybe_serialize(meta_value_)
        #// Format the data query arguments.
        data_ = Array({"meta_key": meta_key_, "meta_value": meta_value_})
        #// Format the where query arguments.
        where_ = Array()
        where_[id_column_] = meta_id_
        #// This action is documented in wp-includes/meta.php
        do_action(str("update_") + str(meta_type_) + str("_meta"), meta_id_, object_id_, meta_key_, _meta_value_)
        if "post" == meta_type_:
            #// This action is documented in wp-includes/meta.php
            do_action("update_postmeta", meta_id_, object_id_, meta_key_, meta_value_)
        # end if
        #// Run the update query, all fields in $data are %s, $where is a %d.
        result_ = wpdb_.update(table_, data_, where_, "%s", "%d")
        if (not result_):
            return False
        # end if
        #// Clear the caches.
        wp_cache_delete(object_id_, meta_type_ + "_meta")
        #// This action is documented in wp-includes/meta.php
        do_action(str("updated_") + str(meta_type_) + str("_meta"), meta_id_, object_id_, meta_key_, _meta_value_)
        if "post" == meta_type_:
            #// This action is documented in wp-includes/meta.php
            do_action("updated_postmeta", meta_id_, object_id_, meta_key_, meta_value_)
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
def delete_metadata_by_mid(meta_type_=None, meta_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Make sure everything is valid.
    if (not meta_type_) or (not php_is_numeric(meta_id_)) or floor(meta_id_) != meta_id_:
        return False
    # end if
    meta_id_ = php_intval(meta_id_)
    if meta_id_ <= 0:
        return False
    # end if
    table_ = _get_meta_table(meta_type_)
    if (not table_):
        return False
    # end if
    #// Object and ID columns.
    column_ = sanitize_key(meta_type_ + "_id")
    id_column_ = "umeta_id" if "user" == meta_type_ else "meta_id"
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
    check_ = apply_filters(str("delete_") + str(meta_type_) + str("_metadata_by_mid"), None, meta_id_)
    if None != check_:
        return php_bool(check_)
    # end if
    #// Fetch the meta and go on if it's found.
    meta_ = get_metadata_by_mid(meta_type_, meta_id_)
    if meta_:
        object_id_ = php_int(meta_.column_)
        #// This action is documented in wp-includes/meta.php
        do_action(str("delete_") + str(meta_type_) + str("_meta"), meta_id_, object_id_, meta_.meta_key, meta_.meta_value)
        #// Old-style action.
        if "post" == meta_type_ or "comment" == meta_type_:
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
            do_action(str("delete_") + str(meta_type_) + str("meta"), meta_id_)
        # end if
        #// Run the query, will return true if deleted, false otherwise.
        result_ = php_bool(wpdb_.delete(table_, Array({id_column_: meta_id_})))
        #// Clear the caches.
        wp_cache_delete(object_id_, meta_type_ + "_meta")
        #// This action is documented in wp-includes/meta.php
        do_action(str("deleted_") + str(meta_type_) + str("_meta"), meta_id_, object_id_, meta_.meta_key, meta_.meta_value)
        #// Old-style action.
        if "post" == meta_type_ or "comment" == meta_type_:
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
            do_action(str("deleted_") + str(meta_type_) + str("meta"), meta_id_)
        # end if
        return result_
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
def update_meta_cache(meta_type_=None, object_ids_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not meta_type_) or (not object_ids_):
        return False
    # end if
    table_ = _get_meta_table(meta_type_)
    if (not table_):
        return False
    # end if
    column_ = sanitize_key(meta_type_ + "_id")
    if (not php_is_array(object_ids_)):
        object_ids_ = php_preg_replace("|[^0-9,]|", "", object_ids_)
        object_ids_ = php_explode(",", object_ids_)
    # end if
    object_ids_ = php_array_map("intval", object_ids_)
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
    check_ = apply_filters(str("update_") + str(meta_type_) + str("_metadata_cache"), None, object_ids_)
    if None != check_:
        return php_bool(check_)
    # end if
    cache_key_ = meta_type_ + "_meta"
    ids_ = Array()
    cache_ = Array()
    for id_ in object_ids_:
        cached_object_ = wp_cache_get(id_, cache_key_)
        if False == cached_object_:
            ids_[-1] = id_
        else:
            cache_[id_] = cached_object_
        # end if
    # end for
    if php_empty(lambda : ids_):
        return cache_
    # end if
    #// Get meta info.
    id_list_ = php_join(",", ids_)
    id_column_ = "umeta_id" if "user" == meta_type_ else "meta_id"
    meta_list_ = wpdb_.get_results(str("SELECT ") + str(column_) + str(", meta_key, meta_value FROM ") + str(table_) + str(" WHERE ") + str(column_) + str(" IN (") + str(id_list_) + str(") ORDER BY ") + str(id_column_) + str(" ASC"), ARRAY_A)
    if (not php_empty(lambda : meta_list_)):
        for metarow_ in meta_list_:
            mpid_ = php_intval(metarow_[column_])
            mkey_ = metarow_["meta_key"]
            mval_ = metarow_["meta_value"]
            #// Force subkeys to be array type.
            if (not (php_isset(lambda : cache_[mpid_]))) or (not php_is_array(cache_[mpid_])):
                cache_[mpid_] = Array()
            # end if
            if (not (php_isset(lambda : cache_[mpid_][mkey_]))) or (not php_is_array(cache_[mpid_][mkey_])):
                cache_[mpid_][mkey_] = Array()
            # end if
            #// Add a value to the current pid/key.
            cache_[mpid_][mkey_][-1] = mval_
        # end for
    # end if
    for id_ in ids_:
        if (not (php_isset(lambda : cache_[id_]))):
            cache_[id_] = Array()
        # end if
        wp_cache_add(id_, cache_[id_], cache_key_)
    # end for
    return cache_
# end def update_meta_cache
#// 
#// Retrieves the queue for lazy-loading metadata.
#// 
#// @since 4.5.0
#// 
#// @return WP_Metadata_Lazyloader $lazyloader Metadata lazyloader queue.
#//
def wp_metadata_lazyloader(*_args_):
    
    
    wp_metadata_lazyloader_ = None
    if None == wp_metadata_lazyloader_:
        wp_metadata_lazyloader_ = php_new_class("WP_Metadata_Lazyloader", lambda : WP_Metadata_Lazyloader())
    # end if
    return wp_metadata_lazyloader_
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
def get_meta_sql(meta_query_=None, type_=None, primary_table_=None, primary_id_column_=None, context_=None, *_args_):
    if context_ is None:
        context_ = None
    # end if
    
    meta_query_obj_ = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query(meta_query_))
    return meta_query_obj_.get_sql(type_, primary_table_, primary_id_column_, context_)
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
def _get_meta_table(type_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    table_name_ = type_ + "meta"
    if php_empty(lambda : wpdb_.table_name_):
        return False
    # end if
    return wpdb_.table_name_
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
def is_protected_meta(meta_key_=None, meta_type_="", *_args_):
    
    
    protected_ = "_" == meta_key_[0]
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
    return apply_filters("is_protected_meta", protected_, meta_key_, meta_type_)
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
def sanitize_meta(meta_key_=None, meta_value_=None, object_type_=None, object_subtype_="", *_args_):
    
    
    if (not php_empty(lambda : object_subtype_)) and has_filter(str("sanitize_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_)):
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
        return apply_filters(str("sanitize_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_), meta_value_, meta_key_, object_type_, object_subtype_)
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
    return apply_filters(str("sanitize_") + str(object_type_) + str("_meta_") + str(meta_key_), meta_value_, meta_key_, object_type_)
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
def register_meta(object_type_=None, meta_key_=None, args_=None, deprecated_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = None
    # end if
    
    global wp_meta_keys_
    php_check_if_defined("wp_meta_keys_")
    if (not php_is_array(wp_meta_keys_)):
        wp_meta_keys_ = Array()
    # end if
    defaults_ = Array({"object_subtype": "", "type": "string", "description": "", "single": False, "sanitize_callback": None, "auth_callback": None, "show_in_rest": False})
    #// There used to be individual args for sanitize and auth callbacks.
    has_old_sanitize_cb_ = False
    has_old_auth_cb_ = False
    if php_is_callable(args_):
        args_ = Array({"sanitize_callback": args_})
        has_old_sanitize_cb_ = True
    else:
        args_ = args_
    # end if
    if php_is_callable(deprecated_):
        args_["auth_callback"] = deprecated_
        has_old_auth_cb_ = True
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
    args_ = apply_filters("register_meta_args", args_, defaults_, object_type_, meta_key_)
    args_ = wp_parse_args(args_, defaults_)
    #// Require an item schema when registering array meta.
    if False != args_["show_in_rest"] and "array" == args_["type"]:
        if (not php_is_array(args_["show_in_rest"])) or (not (php_isset(lambda : args_["show_in_rest"]["schema"]["items"]))):
            _doing_it_wrong(inspect.currentframe().f_code.co_name, __("When registering an \"array\" meta type to show in the REST API, you must specify the schema for each array item in \"show_in_rest.schema.items\"."), "5.3.0")
            return False
        # end if
    # end if
    object_subtype_ = args_["object_subtype"] if (not php_empty(lambda : args_["object_subtype"])) else ""
    #// If `auth_callback` is not provided, fall back to `is_protected_meta()`.
    if php_empty(lambda : args_["auth_callback"]):
        if is_protected_meta(meta_key_, object_type_):
            args_["auth_callback"] = "__return_false"
        else:
            args_["auth_callback"] = "__return_true"
        # end if
    # end if
    #// Back-compat: old sanitize and auth callbacks are applied to all of an object type.
    if php_is_callable(args_["sanitize_callback"]):
        if (not php_empty(lambda : object_subtype_)):
            add_filter(str("sanitize_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_), args_["sanitize_callback"], 10, 4)
        else:
            add_filter(str("sanitize_") + str(object_type_) + str("_meta_") + str(meta_key_), args_["sanitize_callback"], 10, 3)
        # end if
    # end if
    if php_is_callable(args_["auth_callback"]):
        if (not php_empty(lambda : object_subtype_)):
            add_filter(str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_), args_["auth_callback"], 10, 6)
        else:
            add_filter(str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_), args_["auth_callback"], 10, 6)
        # end if
    # end if
    #// Global registry only contains meta keys registered with the array of arguments added in 4.6.0.
    if (not has_old_auth_cb_) and (not has_old_sanitize_cb_):
        args_["object_subtype"] = None
        wp_meta_keys_[object_type_][object_subtype_][meta_key_] = args_
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
def registered_meta_key_exists(object_type_=None, meta_key_=None, object_subtype_="", *_args_):
    
    
    meta_keys_ = get_registered_meta_keys(object_type_, object_subtype_)
    return (php_isset(lambda : meta_keys_[meta_key_]))
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
def unregister_meta_key(object_type_=None, meta_key_=None, object_subtype_="", *_args_):
    
    
    global wp_meta_keys_
    php_check_if_defined("wp_meta_keys_")
    if (not registered_meta_key_exists(object_type_, meta_key_, object_subtype_)):
        return False
    # end if
    args_ = wp_meta_keys_[object_type_][object_subtype_][meta_key_]
    if (php_isset(lambda : args_["sanitize_callback"])) and php_is_callable(args_["sanitize_callback"]):
        if (not php_empty(lambda : object_subtype_)):
            remove_filter(str("sanitize_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_), args_["sanitize_callback"])
        else:
            remove_filter(str("sanitize_") + str(object_type_) + str("_meta_") + str(meta_key_), args_["sanitize_callback"])
        # end if
    # end if
    if (php_isset(lambda : args_["auth_callback"])) and php_is_callable(args_["auth_callback"]):
        if (not php_empty(lambda : object_subtype_)):
            remove_filter(str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_) + str("_for_") + str(object_subtype_), args_["auth_callback"])
        else:
            remove_filter(str("auth_") + str(object_type_) + str("_meta_") + str(meta_key_), args_["auth_callback"])
        # end if
    # end if
    wp_meta_keys_[object_type_][object_subtype_][meta_key_] = None
    #// Do some clean up.
    if php_empty(lambda : wp_meta_keys_[object_type_][object_subtype_]):
        wp_meta_keys_[object_type_][object_subtype_] = None
    # end if
    if php_empty(lambda : wp_meta_keys_[object_type_]):
        wp_meta_keys_[object_type_] = None
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
def get_registered_meta_keys(object_type_=None, object_subtype_="", *_args_):
    
    
    global wp_meta_keys_
    php_check_if_defined("wp_meta_keys_")
    if (not php_is_array(wp_meta_keys_)) or (not (php_isset(lambda : wp_meta_keys_[object_type_]))) or (not (php_isset(lambda : wp_meta_keys_[object_type_][object_subtype_]))):
        return Array()
    # end if
    return wp_meta_keys_[object_type_][object_subtype_]
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
def get_registered_metadata(object_type_=None, object_id_=None, meta_key_="", *_args_):
    
    
    object_subtype_ = get_object_subtype(object_type_, object_id_)
    if (not php_empty(lambda : meta_key_)):
        if (not php_empty(lambda : object_subtype_)) and (not registered_meta_key_exists(object_type_, meta_key_, object_subtype_)):
            object_subtype_ = ""
        # end if
        if (not registered_meta_key_exists(object_type_, meta_key_, object_subtype_)):
            return False
        # end if
        meta_keys_ = get_registered_meta_keys(object_type_, object_subtype_)
        meta_key_data_ = meta_keys_[meta_key_]
        data_ = get_metadata(object_type_, object_id_, meta_key_, meta_key_data_["single"])
        return data_
    # end if
    data_ = get_metadata(object_type_, object_id_)
    if (not data_):
        return Array()
    # end if
    meta_keys_ = get_registered_meta_keys(object_type_)
    if (not php_empty(lambda : object_subtype_)):
        meta_keys_ = php_array_merge(meta_keys_, get_registered_meta_keys(object_type_, object_subtype_))
    # end if
    return php_array_intersect_key(data_, meta_keys_)
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
def _wp_register_meta_args_whitelist(args_=None, default_args_=None, *_args_):
    
    
    return php_array_intersect_key(args_, default_args_)
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
def get_object_subtype(object_type_=None, object_id_=None, *_args_):
    
    
    object_id_ = php_int(object_id_)
    object_subtype_ = ""
    for case in Switch(object_type_):
        if case("post"):
            post_type_ = get_post_type(object_id_)
            if (not php_empty(lambda : post_type_)):
                object_subtype_ = post_type_
            # end if
            break
        # end if
        if case("term"):
            term_ = get_term(object_id_)
            if (not type(term_).__name__ == "WP_Term"):
                break
            # end if
            object_subtype_ = term_.taxonomy
            break
        # end if
        if case("comment"):
            comment_ = get_comment(object_id_)
            if (not comment_):
                break
            # end if
            object_subtype_ = "comment"
            break
        # end if
        if case("user"):
            user_ = get_user_by("id", object_id_)
            if (not user_):
                break
            # end if
            object_subtype_ = "user"
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
    return apply_filters(str("get_object_subtype_") + str(object_type_), object_subtype_, object_id_)
# end def get_object_subtype
