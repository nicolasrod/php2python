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
    #// 
    #// An array of registered handle objects.
    #// 
    #// @since 2.6.8
    #// @var array
    #//
    registered = Array()
    #// 
    #// An array of handles of queued objects.
    #// 
    #// @since 2.6.8
    #// @var string[]
    #//
    queue = Array()
    #// 
    #// An array of handles of objects to queue.
    #// 
    #// @since 2.6.0
    #// @var string[]
    #//
    to_do = Array()
    #// 
    #// An array of handles of objects already queued.
    #// 
    #// @since 2.6.0
    #// @var string[]
    #//
    done = Array()
    #// 
    #// An array of additional arguments passed when a handle is registered.
    #// 
    #// Arguments are appended to the item query string.
    #// 
    #// @since 2.6.0
    #// @var array
    #//
    args = Array()
    #// 
    #// An array of handle groups to enqueue.
    #// 
    #// @since 2.8.0
    #// @var array
    #//
    groups = Array()
    #// 
    #// A handle group to enqueue.
    #// 
    #// @since 2.8.0
    #// @deprecated 4.5.0
    #// @var int
    #//
    group = 0
    #// 
    #// Cached lookup array of flattened queued items and dependencies.
    #// 
    #// @since 5.4.0
    #// @var array
    #//
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
    def do_items(self, handles_=None, group_=None):
        if handles_ is None:
            handles_ = False
        # end if
        if group_ is None:
            group_ = False
        # end if
        
        #// 
        #// If nothing is passed, print the queue. If a string is passed,
        #// print that item. If an array is passed, print those items.
        #//
        handles_ = self.queue if False == handles_ else handles_
        self.all_deps(handles_)
        for key_,handle_ in self.to_do.items():
            if (not php_in_array(handle_, self.done, True)) and (php_isset(lambda : self.registered[handle_])):
                #// 
                #// Attempt to process the item. If successful,
                #// add the handle to the done array.
                #// 
                #// Unset the item from the to_do array.
                #//
                if self.do_item(handle_, group_):
                    self.done[-1] = handle_
                # end if
                self.to_do[key_] = None
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
    def do_item(self, handle_=None):
        
        
        return (php_isset(lambda : self.registered[handle_]))
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
    def all_deps(self, handles_=None, recursion_=None, group_=None):
        if recursion_ is None:
            recursion_ = False
        # end if
        if group_ is None:
            group_ = False
        # end if
        
        handles_ = handles_
        if (not handles_):
            return False
        # end if
        for handle_ in handles_:
            handle_parts_ = php_explode("?", handle_)
            handle_ = handle_parts_[0]
            queued_ = php_in_array(handle_, self.to_do, True)
            if php_in_array(handle_, self.done, True):
                continue
            # end if
            moved_ = self.set_group(handle_, recursion_, group_)
            new_group_ = self.groups[handle_]
            if queued_ and (not moved_):
                continue
            # end if
            keep_going_ = True
            if (not (php_isset(lambda : self.registered[handle_]))):
                keep_going_ = False
                pass
            elif self.registered[handle_].deps and php_array_diff(self.registered[handle_].deps, php_array_keys(self.registered)):
                keep_going_ = False
                pass
            elif self.registered[handle_].deps and (not self.all_deps(self.registered[handle_].deps, True, new_group_)):
                keep_going_ = False
                pass
            # end if
            if (not keep_going_):
                #// Either item or its dependencies don't exist.
                if recursion_:
                    return False
                    pass
                else:
                    continue
                    pass
                # end if
            # end if
            if queued_:
                continue
            # end if
            if (php_isset(lambda : handle_parts_[1])):
                self.args[handle_] = handle_parts_[1]
            # end if
            self.to_do[-1] = handle_
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
    def add(self, handle_=None, src_=None, deps_=None, ver_=None, args_=None):
        if deps_ is None:
            deps_ = Array()
        # end if
        if ver_ is None:
            ver_ = False
        # end if
        if args_ is None:
            args_ = None
        # end if
        
        if (php_isset(lambda : self.registered[handle_])):
            return False
        # end if
        self.registered[handle_] = php_new_class("_WP_Dependency", lambda : _WP_Dependency(handle_, src_, deps_, ver_, args_))
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
    def add_data(self, handle_=None, key_=None, value_=None):
        
        
        if (not (php_isset(lambda : self.registered[handle_]))):
            return False
        # end if
        return self.registered[handle_].add_data(key_, value_)
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
    def get_data(self, handle_=None, key_=None):
        
        
        if (not (php_isset(lambda : self.registered[handle_]))):
            return False
        # end if
        if (not (php_isset(lambda : self.registered[handle_].extra[key_]))):
            return False
        # end if
        return self.registered[handle_].extra[key_]
    # end def get_data
    #// 
    #// Un-register an item or items.
    #// 
    #// @since 2.1.0
    #// @since 2.6.0 Moved from `WP_Scripts`.
    #// 
    #// @param string|string[] $handles Item handle (string) or item handles (array of strings).
    #//
    def remove(self, handles_=None):
        
        
        for handle_ in handles_:
            self.registered[handle_] = None
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
    def enqueue(self, handles_=None):
        
        
        for handle_ in handles_:
            handle_ = php_explode("?", handle_)
            if (not php_in_array(handle_[0], self.queue, True)) and (php_isset(lambda : self.registered[handle_[0]])):
                self.queue[-1] = handle_[0]
                #// Reset all dependencies so they must be recalculated in recurse_deps().
                self.all_queued_deps = None
                if (php_isset(lambda : handle_[1])):
                    self.args[handle_[0]] = handle_[1]
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
    def dequeue(self, handles_=None):
        
        
        for handle_ in handles_:
            handle_ = php_explode("?", handle_)
            key_ = php_array_search(handle_[0], self.queue, True)
            if False != key_:
                #// Reset all dependencies so they must be recalculated in recurse_deps().
                self.all_queued_deps = None
                self.queue[key_] = None
                self.args[handle_[0]] = None
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
    def recurse_deps(self, queue_=None, handle_=None):
        
        
        if (php_isset(lambda : self.all_queued_deps)):
            return (php_isset(lambda : self.all_queued_deps[handle_]))
        # end if
        all_deps_ = php_array_fill_keys(queue_, True)
        queues_ = Array()
        done_ = Array()
        while True:
            
            if not (queue_):
                break
            # end if
            for queued_ in queue_:
                if (not (php_isset(lambda : done_[queued_]))) and (php_isset(lambda : self.registered[queued_])):
                    deps_ = self.registered[queued_].deps
                    if deps_:
                        all_deps_ += php_array_fill_keys(deps_, True)
                        php_array_push(queues_, deps_)
                    # end if
                    done_[queued_] = True
                # end if
            # end for
            queue_ = php_array_pop(queues_)
        # end while
        self.all_queued_deps = all_deps_
        return (php_isset(lambda : self.all_queued_deps[handle_]))
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
    def query(self, handle_=None, list_="registered"):
        
        
        for case in Switch(list_):
            if case("registered"):
                pass
            # end if
            if case("scripts"):
                #// Back compat.
                if (php_isset(lambda : self.registered[handle_])):
                    return self.registered[handle_]
                # end if
                return False
            # end if
            if case("enqueued"):
                pass
            # end if
            if case("queue"):
                if php_in_array(handle_, self.queue, True):
                    return True
                # end if
                return self.recurse_deps(self.queue, handle_)
            # end if
            if case("to_do"):
                pass
            # end if
            if case("to_print"):
                #// Back compat.
                return php_in_array(handle_, self.to_do, True)
            # end if
            if case("done"):
                pass
            # end if
            if case("printed"):
                #// Back compat.
                return php_in_array(handle_, self.done, True)
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
    def set_group(self, handle_=None, recursion_=None, group_=None):
        
        
        group_ = php_int(group_)
        if (php_isset(lambda : self.groups[handle_])) and self.groups[handle_] <= group_:
            return False
        # end if
        self.groups[handle_] = group_
        return True
    # end def set_group
# end class WP_Dependencies
