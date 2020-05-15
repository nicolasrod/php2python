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
#// Object Cache API
#// 
#// @link https://codex.wordpress.org/Class_Reference/WP_Object_Cache
#// 
#// @package WordPress
#// @subpackage Cache
#// 
#// WP_Object_Cache class
php_include_file(ABSPATH + WPINC + "/class-wp-object-cache.php", once=True)
#// 
#// Adds data to the cache, if the cache key doesn't already exist.
#// 
#// @since 2.0.0
#// 
#// @see WP_Object_Cache::add()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int|string $key    The cache key to use for retrieval later.
#// @param mixed      $data   The data to add to the cache.
#// @param string     $group  Optional. The group to add the cache to. Enables the same key
#// to be used across groups. Default empty.
#// @param int        $expire Optional. When the cache data should expire, in seconds.
#// Default 0 (no expiration).
#// @return bool True on success, false if cache key and group already exist.
#//
def wp_cache_add(key=None, data=None, group="", expire=0, *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.add(key, data, group, int(expire))
# end def wp_cache_add
#// 
#// Closes the cache.
#// 
#// This function has ceased to do anything since WordPress 2.5. The
#// functionality was removed along with the rest of the persistent cache.
#// 
#// This does not mean that plugins can't implement this function when they need
#// to make sure that the cache is cleaned up after WordPress no longer needs it.
#// 
#// @since 2.0.0
#// 
#// @return true Always returns true.
#//
def wp_cache_close(*args_):
    
    return True
# end def wp_cache_close
#// 
#// Decrements numeric cache item's value.
#// 
#// @since 3.3.0
#// 
#// @see WP_Object_Cache::decr()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int|string $key    The cache key to decrement.
#// @param int        $offset Optional. The amount by which to decrement the item's value. Default 1.
#// @param string     $group  Optional. The group the key is in. Default empty.
#// @return int|false The item's new value on success, false on failure.
#//
def wp_cache_decr(key=None, offset=1, group="", *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.decr(key, offset, group)
# end def wp_cache_decr
#// 
#// Removes the cache contents matching key and group.
#// 
#// @since 2.0.0
#// 
#// @see WP_Object_Cache::delete()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int|string $key   What the contents in the cache are called.
#// @param string     $group Optional. Where the cache contents are grouped. Default empty.
#// @return bool True on successful removal, false on failure.
#//
def wp_cache_delete(key=None, group="", *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.delete(key, group)
# end def wp_cache_delete
#// 
#// Removes all cache items.
#// 
#// @since 2.0.0
#// 
#// @see WP_Object_Cache::flush()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @return bool True on success, false on failure.
#//
def wp_cache_flush(*args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.flush()
# end def wp_cache_flush
#// 
#// Retrieves the cache contents from the cache by key and group.
#// 
#// @since 2.0.0
#// 
#// @see WP_Object_Cache::get()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int|string  $key    The key under which the cache contents are stored.
#// @param string      $group  Optional. Where the cache contents are grouped. Default empty.
#// @param bool        $force  Optional. Whether to force an update of the local cache from the persistent
#// cache. Default false.
#// @param bool        $found  Optional. Whether the key was found in the cache (passed by reference).
#// Disambiguates a return of false, a storable value. Default null.
#// @return bool|mixed False on failure to retrieve contents or the cache
#// contents on success
#//
def wp_cache_get(key=None, group="", force=False, found=None, *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.get(key, group, force, found)
# end def wp_cache_get
#// 
#// Increment numeric cache item's value
#// 
#// @since 3.3.0
#// 
#// @see WP_Object_Cache::incr()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int|string $key    The key for the cache contents that should be incremented.
#// @param int        $offset Optional. The amount by which to increment the item's value. Default 1.
#// @param string     $group  Optional. The group the key is in. Default empty.
#// @return int|false The item's new value on success, false on failure.
#//
def wp_cache_incr(key=None, offset=1, group="", *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.incr(key, offset, group)
# end def wp_cache_incr
#// 
#// Sets up Object Cache Global and assigns it.
#// 
#// @since 2.0.0
#// 
#// @global WP_Object_Cache $wp_object_cache
#//
def wp_cache_init(*args_):
    global PHP_GLOBALS
    PHP_GLOBALS["wp_object_cache"] = php_new_class("WP_Object_Cache", lambda : WP_Object_Cache())
# end def wp_cache_init
#// 
#// Replaces the contents of the cache with new data.
#// 
#// @since 2.0.0
#// 
#// @see WP_Object_Cache::replace()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int|string $key    The key for the cache data that should be replaced.
#// @param mixed      $data   The new data to store in the cache.
#// @param string     $group  Optional. The group for the cache data that should be replaced.
#// Default empty.
#// @param int        $expire Optional. When to expire the cache contents, in seconds.
#// Default 0 (no expiration).
#// @return bool False if original value does not exist, true if contents were replaced
#//
def wp_cache_replace(key=None, data=None, group="", expire=0, *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.replace(key, data, group, int(expire))
# end def wp_cache_replace
#// 
#// Saves the data to the cache.
#// 
#// Differs from wp_cache_add() and wp_cache_replace() in that it will always write data.
#// 
#// @since 2.0.0
#// 
#// @see WP_Object_Cache::set()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int|string $key    The cache key to use for retrieval later.
#// @param mixed      $data   The contents to store in the cache.
#// @param string     $group  Optional. Where to group the cache contents. Enables the same key
#// to be used across groups. Default empty.
#// @param int        $expire Optional. When to expire the cache contents, in seconds.
#// Default 0 (no expiration).
#// @return bool True on success, false on failure.
#//
def wp_cache_set(key=None, data=None, group="", expire=0, *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    return wp_object_cache.set(key, data, group, int(expire))
# end def wp_cache_set
#// 
#// Switches the internal blog ID.
#// 
#// This changes the blog id used to create keys in blog specific groups.
#// 
#// @since 3.5.0
#// 
#// @see WP_Object_Cache::switch_to_blog()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param int $blog_id Site ID.
#//
def wp_cache_switch_to_blog(blog_id=None, *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    wp_object_cache.switch_to_blog(blog_id)
# end def wp_cache_switch_to_blog
#// 
#// Adds a group or set of groups to the list of global groups.
#// 
#// @since 2.6.0
#// 
#// @see WP_Object_Cache::add_global_groups()
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#// 
#// @param string|array $groups A group or an array of groups to add.
#//
def wp_cache_add_global_groups(groups=None, *args_):
    
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    wp_object_cache.add_global_groups(groups)
# end def wp_cache_add_global_groups
#// 
#// Adds a group or set of groups to the list of non-persistent groups.
#// 
#// @since 2.6.0
#// 
#// @param string|array $groups A group or an array of groups to add.
#//
def wp_cache_add_non_persistent_groups(groups=None, *args_):
    
    pass
# end def wp_cache_add_non_persistent_groups
#// 
#// Reset internal cache keys and structures.
#// 
#// If the cache back end uses global blog or site IDs as part of its cache keys,
#// this function instructs the back end to reset those keys and perform any cleanup
#// since blog or site IDs have changed since cache init.
#// 
#// This function is deprecated. Use wp_cache_switch_to_blog() instead of this
#// function when preparing the cache for a blog switch. For clearing the cache
#// during unit tests, consider using wp_cache_init(). wp_cache_init() is not
#// recommended outside of unit tests as the performance penalty for using it is
#// high.
#// 
#// @since 2.6.0
#// @deprecated 3.5.0 WP_Object_Cache::reset()
#// @see WP_Object_Cache::reset()
#// 
#// @global WP_Object_Cache $wp_object_cache Object cache global instance.
#//
def wp_cache_reset(*args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0", "WP_Object_Cache::reset()")
    global wp_object_cache
    php_check_if_defined("wp_object_cache")
    wp_object_cache.reset()
# end def wp_cache_reset
