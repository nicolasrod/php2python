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
#// Dependencies API: WP_Dependencies base class
#// 
#// @since 2.6.0
#// 
#// @package WordPress
#// @subpackage Dependencies
#// 
#// 
#// Core base class extended to register items.
#// 
#// @since 2.6.0
#// 
#// @see _WP_Dependency
#//
class WP_Dependencies():
    registered = Array()
    queue = Array()
    to_do = Array()
    done = Array()
    args = Array()
    groups = Array()
    group = 0
    all_queued_deps = Array()
    #// 
    #// Processes the items and dependencies.
    #// 
    #// Processes the items passed to it or the queue, and their dependencies.
    #// 
    #// @since 2.6.0
    #// @since 2.8.0 Added the `$group` parameter.
    #// 
    #// @param string|string[]|false $handles Optional. Items to be processed: queue (false),
    #// single item (string), or multiple items (array of strings).
    #// Default false.
    #// @param int|false             $group   Optional. Group level: level (int), no groups (false).
    #// @return string[] Array of handles of items that have been processed.
    #//
    def do_items(self, handles=False, group=False):
        
        #// 
        #// If nothing is passed, print the queue. If a string is passed,
        #// print that item. If an array is passed, print those items.
        #//
        handles = self.queue if False == handles else handles
        self.all_deps(handles)
        for key,handle in self.to_do:
            if (not php_in_array(handle, self.done, True)) and (php_isset(lambda : self.registered[handle])):
                #// 
                #// Attempt to process the item. If successful,
                #// add the handle to the done array.
                #// 
                #// Unset the item from the to_do array.
                #//
                if self.do_item(handle, group):
                    self.done[-1] = handle
                # end if
                self.to_do[key] = None
            # end if
        # end for
        return self.done
    # end def do_items
    #// 
    #// Processes a dependency.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $handle Name of the item. Should be unique.
    #// @return bool True on success, false if not set.
    #//
    def do_item(self, handle=None):
        
        return (php_isset(lambda : self.registered[handle]))
    # end def do_item
    #// 
    #// Determines dependencies.
    #// 
    #// Recursively builds an array of items to process taking
    #// dependencies into account. Does NOT catch infinite loops.
    #// 
    #// @since 2.1.0
    #// @since 2.6.0 Moved from `WP_Scripts`.
    #// @since 2.8.0 Added the `$group` parameter.
    #// 
    #// @param string|string[] $handles   Item handle (string) or item handles (array of strings).
    #// @param bool            $recursion Optional. Internal flag that function is calling itself.
    #// Default false.
    #// @param int|false       $group     Optional. Group level: level (int), no groups (false).
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def all_deps(self, handles=None, recursion=False, group=False):
        
        handles = handles
        if (not handles):
            return False
        # end if
        for handle in handles:
            handle_parts = php_explode("?", handle)
            handle = handle_parts[0]
            queued = php_in_array(handle, self.to_do, True)
            if php_in_array(handle, self.done, True):
                continue
            # end if
            moved = self.set_group(handle, recursion, group)
            new_group = self.groups[handle]
            if queued and (not moved):
                continue
            # end if
            keep_going = True
            if (not (php_isset(lambda : self.registered[handle]))):
                keep_going = False
                pass
            elif self.registered[handle].deps and php_array_diff(self.registered[handle].deps, php_array_keys(self.registered)):
                keep_going = False
                pass
            elif self.registered[handle].deps and (not self.all_deps(self.registered[handle].deps, True, new_group)):
                keep_going = False
                pass
            # end if
            if (not keep_going):
                #// Either item or its dependencies don't exist.
                if recursion:
                    return False
                    pass
                else:
                    continue
                    pass
                # end if
            # end if
            if queued:
                continue
            # end if
            if (php_isset(lambda : handle_parts[1])):
                self.args[handle] = handle_parts[1]
            # end if
            self.to_do[-1] = handle
        # end for
        return True
    # end def all_deps
    #// 
    #// Register an item.
    #// 
    #// Registers the item if no item of that name already exists.
    #// 
    #// @since 2.1.0
    #// @since 2.6.0 Moved from `WP_Scripts`.
    #// 
    #// @param string           $handle Name of the item. Should be unique.
    #// @param string|bool      $src    Full URL of the item, or path of the item relative
    #// to the WordPress root directory. If source is set to false,
    #// item is an alias of other items it depends on.
    #// @param string[]         $deps   Optional. An array of registered item handles this item depends on.
    #// Default empty array.
    #// @param string|bool|null $ver    Optional. String specifying item version number, if it has one,
    #// which is added to the URL as a query string for cache busting purposes.
    #// If version is set to false, a version number is automatically added
    #// equal to current installed WordPress version.
    #// If set to null, no version is added.
    #// @param mixed            $args   Optional. Custom property of the item. NOT the class property $args.
    #// Examples: $media, $in_footer.
    #// @return bool Whether the item has been registered. True on success, false on failure.
    #//
    def add(self, handle=None, src=None, deps=Array(), ver=False, args=None):
        
        if (php_isset(lambda : self.registered[handle])):
            return False
        # end if
        self.registered[handle] = php_new_class("_WP_Dependency", lambda : _WP_Dependency(handle, src, deps, ver, args))
        return True
    # end def add
    #// 
    #// Add extra item data.
    #// 
    #// Adds data to a registered item.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $handle Name of the item. Should be unique.
    #// @param string $key    The data key.
    #// @param mixed  $value  The data value.
    #// @return bool True on success, false on failure.
    #//
    def add_data(self, handle=None, key=None, value=None):
        
        if (not (php_isset(lambda : self.registered[handle]))):
            return False
        # end if
        return self.registered[handle].add_data(key, value)
    # end def add_data
    #// 
    #// Get extra item data.
    #// 
    #// Gets data associated with a registered item.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $handle Name of the item. Should be unique.
    #// @param string $key    The data key.
    #// @return mixed Extra item data (string), false otherwise.
    #//
    def get_data(self, handle=None, key=None):
        
        if (not (php_isset(lambda : self.registered[handle]))):
            return False
        # end if
        if (not (php_isset(lambda : self.registered[handle].extra[key]))):
            return False
        # end if
        return self.registered[handle].extra[key]
    # end def get_data
    #// 
    #// Un-register an item or items.
    #// 
    #// @since 2.1.0
    #// @since 2.6.0 Moved from `WP_Scripts`.
    #// 
    #// @param string|string[] $handles Item handle (string) or item handles (array of strings).
    #//
    def remove(self, handles=None):
        
        for handle in handles:
            self.registered[handle] = None
        # end for
    # end def remove
    #// 
    #// Queue an item or items.
    #// 
    #// Decodes handles and arguments, then queues handles and stores
    #// arguments in the class property $args. For example in extending
    #// classes, $args is appended to the item url as a query string.
    #// Note $args is NOT the $args property of items in the $registered array.
    #// 
    #// @since 2.1.0
    #// @since 2.6.0 Moved from `WP_Scripts`.
    #// 
    #// @param string|string[] $handles Item handle (string) or item handles (array of strings).
    #//
    def enqueue(self, handles=None):
        
        for handle in handles:
            handle = php_explode("?", handle)
            if (not php_in_array(handle[0], self.queue, True)) and (php_isset(lambda : self.registered[handle[0]])):
                self.queue[-1] = handle[0]
                #// Reset all dependencies so they must be recalculated in recurse_deps().
                self.all_queued_deps = None
                if (php_isset(lambda : handle[1])):
                    self.args[handle[0]] = handle[1]
                # end if
            # end if
        # end for
    # end def enqueue
    #// 
    #// Dequeue an item or items.
    #// 
    #// Decodes handles and arguments, then dequeues handles
    #// and removes arguments from the class property $args.
    #// 
    #// @since 2.1.0
    #// @since 2.6.0 Moved from `WP_Scripts`.
    #// 
    #// @param string|string[] $handles Item handle (string) or item handles (array of strings).
    #//
    def dequeue(self, handles=None):
        
        for handle in handles:
            handle = php_explode("?", handle)
            key = php_array_search(handle[0], self.queue, True)
            if False != key:
                #// Reset all dependencies so they must be recalculated in recurse_deps().
                self.all_queued_deps = None
                self.queue[key] = None
                self.args[handle[0]] = None
            # end if
        # end for
    # end def dequeue
    #// 
    #// Recursively search the passed dependency tree for $handle.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string[] $queue  An array of queued _WP_Dependency handles.
    #// @param string   $handle Name of the item. Should be unique.
    #// @return bool Whether the handle is found after recursively searching the dependency tree.
    #//
    def recurse_deps(self, queue=None, handle=None):
        
        if (php_isset(lambda : self.all_queued_deps)):
            return (php_isset(lambda : self.all_queued_deps[handle]))
        # end if
        all_deps = php_array_fill_keys(queue, True)
        queues = Array()
        done = Array()
        while True:
            
            if not (queue):
                break
            # end if
            for queued in queue:
                if (not (php_isset(lambda : done[queued]))) and (php_isset(lambda : self.registered[queued])):
                    deps = self.registered[queued].deps
                    if deps:
                        all_deps += php_array_fill_keys(deps, True)
                        php_array_push(queues, deps)
                    # end if
                    done[queued] = True
                # end if
            # end for
            queue = php_array_pop(queues)
        # end while
        self.all_queued_deps = all_deps
        return (php_isset(lambda : self.all_queued_deps[handle]))
    # end def recurse_deps
    #// 
    #// Query list for an item.
    #// 
    #// @since 2.1.0
    #// @since 2.6.0 Moved from `WP_Scripts`.
    #// 
    #// @param string $handle Name of the item. Should be unique.
    #// @param string $list   Optional. Property name of list array. Default 'registered'.
    #// @return bool|_WP_Dependency Found, or object Item data.
    #//
    def query(self, handle=None, list="registered"):
        
        for case in Switch(list):
            if case("registered"):
                pass
            # end if
            if case("scripts"):
                #// Back compat.
                if (php_isset(lambda : self.registered[handle])):
                    return self.registered[handle]
                # end if
                return False
            # end if
            if case("enqueued"):
                pass
            # end if
            if case("queue"):
                if php_in_array(handle, self.queue, True):
                    return True
                # end if
                return self.recurse_deps(self.queue, handle)
            # end if
            if case("to_do"):
                pass
            # end if
            if case("to_print"):
                #// Back compat.
                return php_in_array(handle, self.to_do, True)
            # end if
            if case("done"):
                pass
            # end if
            if case("printed"):
                #// Back compat.
                return php_in_array(handle, self.done, True)
            # end if
        # end for
        return False
    # end def query
    #// 
    #// Set item group, unless already in a lower group.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string    $handle    Name of the item. Should be unique.
    #// @param bool      $recursion Internal flag that calling function was called recursively.
    #// @param int|false $group     Group level: level (int), no groups (false).
    #// @return bool Not already in the group or a lower group.
    #//
    def set_group(self, handle=None, recursion=None, group=None):
        
        group = int(group)
        if (php_isset(lambda : self.groups[handle])) and self.groups[handle] <= group:
            return False
        # end if
        self.groups[handle] = group
        return True
    # end def set_group
# end class WP_Dependencies
