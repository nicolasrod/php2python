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
    #// 
    #// Holds the cached objects.
    #// 
    #// @since 2.0.0
    #// @var array
    #//
    cache = Array()
    #// 
    #// The amount of times the cache data was already stored in the cache.
    #// 
    #// @since 2.5.0
    #// @var int
    #//
    cache_hits = 0
    #// 
    #// Amount of times the cache did not have the request in cache.
    #// 
    #// @since 2.0.0
    #// @var int
    #//
    cache_misses = 0
    #// 
    #// List of global cache groups.
    #// 
    #// @since 3.0.0
    #// @var array
    #//
    global_groups = Array()
    #// 
    #// The blog prefix to prepend to keys in non-global groups.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    blog_prefix = Array()
    #// 
    #// Holds the value of is_multisite().
    #// 
    #// @since 3.5.0
    #// @var bool
    #//
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
    def __get(self, name_=None):
        
        
        return self.name_
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
    def __set(self, name_=None, value_=None):
        
        
        self.name_ = value_
        return self.name_
    # end def __set
    #// 
    #// Makes private properties checkable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to check if set.
    #// @return bool Whether the property is set.
    #//
    def __isset(self, name_=None):
        
        
        return (php_isset(lambda : self.name_))
    # end def __isset
    #// 
    #// Makes private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name_=None):
        
        
        self.name_ = None
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
    def add(self, key_=None, data_=None, group_="default", expire_=0):
        
        
        if wp_suspend_cache_addition():
            return False
        # end if
        if php_empty(lambda : group_):
            group_ = "default"
        # end if
        id_ = key_
        if self.multisite and (not (php_isset(lambda : self.global_groups[group_]))):
            id_ = self.blog_prefix + key_
        # end if
        if self._exists(id_, group_):
            return False
        # end if
        return self.set(key_, data_, group_, php_int(expire_))
    # end def add
    #// 
    #// Sets the list of global cache groups.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $groups List of groups that are global.
    #//
    def add_global_groups(self, groups_=None):
        
        
        groups_ = groups_
        groups_ = php_array_fill_keys(groups_, True)
        self.global_groups = php_array_merge(self.global_groups, groups_)
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
    def decr(self, key_=None, offset_=1, group_="default"):
        
        
        if php_empty(lambda : group_):
            group_ = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group_]))):
            key_ = self.blog_prefix + key_
        # end if
        if (not self._exists(key_, group_)):
            return False
        # end if
        if (not php_is_numeric(self.cache[group_][key_])):
            self.cache[group_][key_] = 0
        # end if
        offset_ = php_int(offset_)
        self.cache[group_][key_] -= offset_
        if self.cache[group_][key_] < 0:
            self.cache[group_][key_] = 0
        # end if
        return self.cache[group_][key_]
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
    def delete(self, key_=None, group_="default", deprecated_=None):
        if deprecated_ is None:
            deprecated_ = False
        # end if
        
        if php_empty(lambda : group_):
            group_ = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group_]))):
            key_ = self.blog_prefix + key_
        # end if
        if (not self._exists(key_, group_)):
            return False
        # end if
        self.cache[group_][key_] = None
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
    def get(self, key_=None, group_="default", force_=None, found_=None):
        if force_ is None:
            force_ = False
        # end if
        if found_ is None:
            found_ = None
        # end if
        
        if php_empty(lambda : group_):
            group_ = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group_]))):
            key_ = self.blog_prefix + key_
        # end if
        if self._exists(key_, group_):
            found_ = True
            self.cache_hits += 1
            if php_is_object(self.cache[group_][key_]):
                return copy.deepcopy(self.cache[group_][key_])
            else:
                return self.cache[group_][key_]
            # end if
        # end if
        found_ = False
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
    def incr(self, key_=None, offset_=1, group_="default"):
        
        
        if php_empty(lambda : group_):
            group_ = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group_]))):
            key_ = self.blog_prefix + key_
        # end if
        if (not self._exists(key_, group_)):
            return False
        # end if
        if (not php_is_numeric(self.cache[group_][key_])):
            self.cache[group_][key_] = 0
        # end if
        offset_ = php_int(offset_)
        self.cache[group_][key_] += offset_
        if self.cache[group_][key_] < 0:
            self.cache[group_][key_] = 0
        # end if
        return self.cache[group_][key_]
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
    def replace(self, key_=None, data_=None, group_="default", expire_=0):
        
        
        if php_empty(lambda : group_):
            group_ = "default"
        # end if
        id_ = key_
        if self.multisite and (not (php_isset(lambda : self.global_groups[group_]))):
            id_ = self.blog_prefix + key_
        # end if
        if (not self._exists(id_, group_)):
            return False
        # end if
        return self.set(key_, data_, group_, php_int(expire_))
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
        for group_ in php_array_keys(self.cache):
            if (not (php_isset(lambda : self.global_groups[group_]))):
                self.cache[group_] = None
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
    def set(self, key_=None, data_=None, group_="default", expire_=0):
        
        
        if php_empty(lambda : group_):
            group_ = "default"
        # end if
        if self.multisite and (not (php_isset(lambda : self.global_groups[group_]))):
            key_ = self.blog_prefix + key_
        # end if
        if php_is_object(data_):
            data_ = copy.deepcopy(data_)
        # end if
        self.cache[group_][key_] = data_
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
        for group_,cache_ in self.cache:
            php_print(str("<li><strong>Group:</strong> ") + str(group_) + str(" - ( ") + number_format(php_strlen(serialize(cache_)) / KB_IN_BYTES, 2) + "k )</li>")
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
    def switch_to_blog(self, blog_id_=None):
        
        
        blog_id_ = php_int(blog_id_)
        self.blog_prefix = blog_id_ + ":" if self.multisite else ""
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
    def _exists(self, key_=None, group_=None):
        
        
        return (php_isset(lambda : self.cache[group_])) and (php_isset(lambda : self.cache[group_][key_])) or php_array_key_exists(key_, self.cache[group_])
    # end def _exists
# end class WP_Object_Cache
