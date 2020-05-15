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
#// Object Cache API: WP_Object_Cache class
#// 
#// @package WordPress
#// @subpackage Cache
#// @since 5.4.0
#// 
#// 
#// Core class that implements an object cache.
#// 
#// The WordPress Object Cache is used to save on trips to the database. The
#// Object Cache stores all of the cache data to memory and makes the cache
#// contents available by using a key, which is used to name and later retrieve
#// the cache contents.
#// 
#// The Object Cache can be replaced by other caching mechanisms by placing files
#// in the wp-content folder which is looked at in wp-settings. If that file
#// exists, then this file will not be included.
#// 
#// @since 2.0.0
#//
class WP_Object_Cache():
    cache = Array()
    cache_hits = 0
    cache_misses = 0
    global_groups = Array()
    blog_prefix = Array()
    multisite = Array()
    #// 
    #// Sets up object properties; PHP 5 style constructor.
    #// 
    #// @since 2.0.8
    #//
    def __init__(self):
        
        self.multisite = is_multisite()
        self.blog_prefix = get_current_blog_id() + ":" if self.multisite else ""
    # end def __init__
    #// 
    #// Makes private properties readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to get.
    #// @return mixed Property.
    #//
    def __get(self, name=None):
        
        return self.name
    # end def __get
    #// 
    #// Makes private properties settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name  Property to set.
    #// @param mixed  $value Property value.
    #// @return mixed Newly-set property.
    #//
    def __set(self, name=None, value=None):
        
        self.name = value
        return self.name
    # end def __set
    #// 
    #// Makes private properties checkable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to check if set.
    #// @return bool Whether the property is set.
    #//
    def __isset(self, name=None):
        
        return (php_isset(lambda : self.name))
    # end def __isset
    #// 
    #// Makes private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name=None):
        
        self.name = None
    # end def __unset
    #// 
    #// Adds data to the cache if it doesn't already exist.
    #// 
    #// @since 2.0.0
    #// 
    #// @uses WP_Object_Cache::_exists() Checks to see if the cache already has data.
    #// @uses WP_Object_Cache::set()     Sets the data after the checking the cache
    #// contents existence.
    #// 
    #// @param int|string $key    What to call the contents in the cache.
    #// @param mixed      $data   The contents to store in the cache.
    #// @param string     $group  Optional. Where to group the cache contents. Default 'default'.
    #// @param int        $expire Optional. When to expire the cache contents. Default 0 (no expiration).
    #// @return bool True on success, false if cache key and group already exist.
    #//
    def add(self, key=None, data=None, group="default", expire=0):
        
        if wp_suspend_cache_addition():
            return False
        # end if
        if php_empty(lambda : group):
            group = "default"
        # end if
        id = key
        if self.multisite and (not (php_isset(lambda : self.global_groups[group]))):
            id = self.blog_prefix + key
        # end if
        if self._exists(id, group):
            return False
        # end if
        return self.set(key, data, group, int(expire))
    # end def add
    #// 
    #// Sets the list of global cache groups.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $groups List of groups that are global.
    #//
    def add_global_groups(self, groups=None):
        
        groups = groups
        groups = php_array_fill_keys(groups, True)
        self.global_groups = php_array_merge(self.global_groups, groups)
    # end def add_global_groups
    #// 
    #// Decrements numeric cache item's value.
    #// 
    #// @since 3.3.0
    #// 
    #// @param int|string $key    The cache key to decrement.
    #// @param int        $offset Optional. The amount by which to decrement the item's value. Default 1.
    #// @param string     $group  Optional. The group the key is in. Default 'default'.
    #// @return int|false The item's new value on success, false on failure.
    #//
    def decr(self, key=None, offset=1, group="default"):
        
        if php_empty(lambda : group):
            group = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group]))):
            key = self.blog_prefix + key
        # end if
        if (not self._exists(key, group)):
            return False
        # end if
        if (not php_is_numeric(self.cache[group][key])):
            self.cache[group][key] = 0
        # end if
        offset = int(offset)
        self.cache[group][key] -= offset
        if self.cache[group][key] < 0:
            self.cache[group][key] = 0
        # end if
        return self.cache[group][key]
    # end def decr
    #// 
    #// Removes the contents of the cache key in the group.
    #// 
    #// If the cache key does not exist in the group, then nothing will happen.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int|string $key        What the contents in the cache are called.
    #// @param string     $group      Optional. Where the cache contents are grouped. Default 'default'.
    #// @param bool       $deprecated Optional. Unused. Default false.
    #// @return bool False if the contents weren't deleted and true on success.
    #//
    def delete(self, key=None, group="default", deprecated=False):
        
        if php_empty(lambda : group):
            group = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group]))):
            key = self.blog_prefix + key
        # end if
        if (not self._exists(key, group)):
            return False
        # end if
        self.cache[group][key] = None
        return True
    # end def delete
    #// 
    #// Clears the object cache of all data.
    #// 
    #// @since 2.0.0
    #// 
    #// @return true Always returns true.
    #//
    def flush(self):
        
        self.cache = Array()
        return True
    # end def flush
    #// 
    #// Retrieves the cache contents, if it exists.
    #// 
    #// The contents will be first attempted to be retrieved by searching by the
    #// key in the cache group. If the cache is hit (success) then the contents
    #// are returned.
    #// 
    #// On failure, the number of cache misses will be incremented.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int|string $key    What the contents in the cache are called.
    #// @param string     $group  Optional. Where the cache contents are grouped. Default 'default'.
    #// @param bool       $force  Optional. Unused. Whether to force a refetch rather than relying on the local
    #// cache. Default false.
    #// @param bool       $found  Optional. Whether the key was found in the cache (passed by reference).
    #// Disambiguates a return of false, a storable value. Default null.
    #// @return mixed|false The cache contents on success, false on failure to retrieve contents.
    #//
    def get(self, key=None, group="default", force=False, found=None):
        
        if php_empty(lambda : group):
            group = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group]))):
            key = self.blog_prefix + key
        # end if
        if self._exists(key, group):
            found = True
            self.cache_hits += 1
            if php_is_object(self.cache[group][key]):
                return copy.deepcopy(self.cache[group][key])
            else:
                return self.cache[group][key]
            # end if
        # end if
        found = False
        self.cache_misses += 1
        return False
    # end def get
    #// 
    #// Increments numeric cache item's value.
    #// 
    #// @since 3.3.0
    #// 
    #// @param int|string $key    The cache key to increment
    #// @param int        $offset Optional. The amount by which to increment the item's value. Default 1.
    #// @param string     $group  Optional. The group the key is in. Default 'default'.
    #// @return int|false The item's new value on success, false on failure.
    #//
    def incr(self, key=None, offset=1, group="default"):
        
        if php_empty(lambda : group):
            group = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group]))):
            key = self.blog_prefix + key
        # end if
        if (not self._exists(key, group)):
            return False
        # end if
        if (not php_is_numeric(self.cache[group][key])):
            self.cache[group][key] = 0
        # end if
        offset = int(offset)
        self.cache[group][key] += offset
        if self.cache[group][key] < 0:
            self.cache[group][key] = 0
        # end if
        return self.cache[group][key]
    # end def incr
    #// 
    #// Replaces the contents in the cache, if contents already exist.
    #// 
    #// @since 2.0.0
    #// 
    #// @see WP_Object_Cache::set()
    #// 
    #// @param int|string $key    What to call the contents in the cache.
    #// @param mixed      $data   The contents to store in the cache.
    #// @param string     $group  Optional. Where to group the cache contents. Default 'default'.
    #// @param int        $expire Optional. When to expire the cache contents. Default 0 (no expiration).
    #// @return bool False if not exists, true if contents were replaced.
    #//
    def replace(self, key=None, data=None, group="default", expire=0):
        
        if php_empty(lambda : group):
            group = "default"
        # end if
        id = key
        if self.multisite and (not (php_isset(lambda : self.global_groups[group]))):
            id = self.blog_prefix + key
        # end if
        if (not self._exists(id, group)):
            return False
        # end if
        return self.set(key, data, group, int(expire))
    # end def replace
    #// 
    #// Resets cache keys.
    #// 
    #// @since 3.0.0
    #// 
    #// @deprecated 3.5.0 Use switch_to_blog()
    #// @see switch_to_blog()
    #//
    def reset(self):
        
        _deprecated_function(__FUNCTION__, "3.5.0", "switch_to_blog()")
        #// Clear out non-global caches since the blog ID has changed.
        for group in php_array_keys(self.cache):
            if (not (php_isset(lambda : self.global_groups[group]))):
                self.cache[group] = None
            # end if
        # end for
    # end def reset
    #// 
    #// Sets the data contents into the cache.
    #// 
    #// The cache contents are grouped by the $group parameter followed by the
    #// $key. This allows for duplicate ids in unique groups. Therefore, naming of
    #// the group should be used with care and should follow normal function
    #// naming guidelines outside of core WordPress usage.
    #// 
    #// The $expire parameter is not used, because the cache will automatically
    #// expire for each time a page is accessed and PHP finishes. The method is
    #// more for cache plugins which use files.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int|string $key    What to call the contents in the cache.
    #// @param mixed      $data   The contents to store in the cache.
    #// @param string     $group  Optional. Where to group the cache contents. Default 'default'.
    #// @param int        $expire Not Used.
    #// @return true Always returns true.
    #//
    def set(self, key=None, data=None, group="default", expire=0):
        
        if php_empty(lambda : group):
            group = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group]))):
            key = self.blog_prefix + key
        # end if
        if php_is_object(data):
            data = copy.deepcopy(data)
        # end if
        self.cache[group][key] = data
        return True
    # end def set
    #// 
    #// Echoes the stats of the caching.
    #// 
    #// Gives the cache hits, and cache misses. Also prints every cached group,
    #// key and the data.
    #// 
    #// @since 2.0.0
    #//
    def stats(self):
        
        php_print("<p>")
        php_print(str("<strong>Cache Hits:</strong> ") + str(self.cache_hits) + str("<br />"))
        php_print(str("<strong>Cache Misses:</strong> ") + str(self.cache_misses) + str("<br />"))
        php_print("</p>")
        php_print("<ul>")
        for group,cache in self.cache:
            php_print(str("<li><strong>Group:</strong> ") + str(group) + str(" - ( ") + number_format(php_strlen(serialize(cache)) / KB_IN_BYTES, 2) + "k )</li>")
        # end for
        php_print("</ul>")
    # end def stats
    #// 
    #// Switches the internal blog ID.
    #// 
    #// This changes the blog ID used to create keys in blog specific groups.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int $blog_id Blog ID.
    #//
    def switch_to_blog(self, blog_id=None):
        
        blog_id = int(blog_id)
        self.blog_prefix = blog_id + ":" if self.multisite else ""
    # end def switch_to_blog
    #// 
    #// Serves as a utility function to determine whether a key exists in the cache.
    #// 
    #// @since 3.4.0
    #// 
    #// @param int|string $key   Cache key to check for existence.
    #// @param string     $group Cache group for the key existence check.
    #// @return bool Whether the key exists in the cache for the given group.
    #//
    def _exists(self, key=None, group=None):
        
        return (php_isset(lambda : self.cache[group])) and (php_isset(lambda : self.cache[group][key])) or php_array_key_exists(key, self.cache[group])
    # end def _exists
# end class WP_Object_Cache
