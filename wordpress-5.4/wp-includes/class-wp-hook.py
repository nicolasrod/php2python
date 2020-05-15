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
#// Plugin API: WP_Hook class
#// 
#// @package WordPress
#// @subpackage Plugin
#// @since 4.7.0
#// 
#// 
#// Core class used to implement action and filter hook functionality.
#// 
#// @since 4.7.0
#// 
#// @see Iterator
#// @see ArrayAccess
#//
class WP_Hook():
    callbacks = Array()
    iterations = Array()
    current_priority = Array()
    nesting_level = 0
    doing_action = False
    #// 
    #// Hooks a function or method to a specific filter action.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string   $tag             The name of the filter to hook the $function_to_add callback to.
    #// @param callable $function_to_add The callback to be run when the filter is applied.
    #// @param int      $priority        The order in which the functions associated with a particular action
    #// are executed. Lower numbers correspond with earlier execution,
    #// and functions with the same priority are executed in the order
    #// in which they were added to the action.
    #// @param int      $accepted_args   The number of arguments the function accepts.
    #//
    def add_filter(self, tag=None, function_to_add=None, priority=None, accepted_args=None):
        
        idx = _wp_filter_build_unique_id(tag, function_to_add, priority)
        priority_existed = (php_isset(lambda : self.callbacks[priority]))
        self.callbacks[priority][idx] = Array({"function": function_to_add, "accepted_args": accepted_args})
        #// If we're adding a new priority to the list, put them back in sorted order.
        if (not priority_existed) and php_count(self.callbacks) > 1:
            ksort(self.callbacks, SORT_NUMERIC)
        # end if
        if self.nesting_level > 0:
            self.resort_active_iterations(priority, priority_existed)
        # end if
    # end def add_filter
    #// 
    #// Handles resetting callback priority keys mid-iteration.
    #// 
    #// @since 4.7.0
    #// 
    #// @param bool|int $new_priority     Optional. The priority of the new filter being added. Default false,
    #// for no priority being added.
    #// @param bool     $priority_existed Optional. Flag for whether the priority already existed before the new
    #// filter was added. Default false.
    #//
    def resort_active_iterations(self, new_priority=False, priority_existed=False):
        
        new_priorities = php_array_keys(self.callbacks)
        #// If there are no remaining hooks, clear out all running iterations.
        if (not new_priorities):
            for index,iteration in self.iterations:
                self.iterations[index] = new_priorities
            # end for
            return
        # end if
        min = php_min(new_priorities)
        for index,iteration in self.iterations:
            current = current(iteration)
            #// If we're already at the end of this iteration, just leave the array pointer where it is.
            if False == current:
                continue
            # end if
            iteration = new_priorities
            if current < min:
                array_unshift(iteration, current)
                continue
            # end if
            while True:
                
                if not (current(iteration) < current):
                    break
                # end if
                if False == next(iteration):
                    break
                # end if
            # end while
            #// If we have a new priority that didn't exist, but ::apply_filters() or ::do_action() thinks it's the current priority...
            if new_priority == self.current_priority[index] and (not priority_existed):
                #// 
                #// ...and the new priority is the same as what $this->iterations thinks is the previous
                #// priority, we need to move back to it.
                #//
                if False == current(iteration):
                    #// If we've already moved off the end of the array, go back to the last element.
                    prev = php_end(iteration)
                else:
                    #// Otherwise, just go back to the previous element.
                    prev = php_prev(iteration)
                # end if
                if False == prev:
                    #// Start of the array. Reset, and go about our day.
                    reset(iteration)
                elif new_priority != prev:
                    #// Previous wasn't the same. Move forward again.
                    next(iteration)
                # end if
            # end if
        # end for
        iteration = None
    # end def resort_active_iterations
    #// 
    #// Unhooks a function or method from a specific filter action.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string   $tag                The filter hook to which the function to be removed is hooked.
    #// @param callable $function_to_remove The callback to be removed from running when the filter is applied.
    #// @param int      $priority           The exact priority used when adding the original filter callback.
    #// @return bool Whether the callback existed before it was removed.
    #//
    def remove_filter(self, tag=None, function_to_remove=None, priority=None):
        
        function_key = _wp_filter_build_unique_id(tag, function_to_remove, priority)
        exists = (php_isset(lambda : self.callbacks[priority][function_key]))
        if exists:
            self.callbacks[priority][function_key] = None
            if (not self.callbacks[priority]):
                self.callbacks[priority] = None
                if self.nesting_level > 0:
                    self.resort_active_iterations()
                # end if
            # end if
        # end if
        return exists
    # end def remove_filter
    #// 
    #// Checks if a specific action has been registered for this hook.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string        $tag               Optional. The name of the filter hook. Default empty.
    #// @param callable|bool $function_to_check Optional. The callback to check for. Default false.
    #// @return bool|int The priority of that hook is returned, or false if the function is not attached.
    #//
    def has_filter(self, tag="", function_to_check=False):
        
        if False == function_to_check:
            return self.has_filters()
        # end if
        function_key = _wp_filter_build_unique_id(tag, function_to_check, False)
        if (not function_key):
            return False
        # end if
        for priority,callbacks in self.callbacks:
            if (php_isset(lambda : callbacks[function_key])):
                return priority
            # end if
        # end for
        return False
    # end def has_filter
    #// 
    #// Checks if any callbacks have been registered for this hook.
    #// 
    #// @since 4.7.0
    #// 
    #// @return bool True if callbacks have been registered for the current hook, otherwise false.
    #//
    def has_filters(self):
        
        for callbacks in self.callbacks:
            if callbacks:
                return True
            # end if
        # end for
        return False
    # end def has_filters
    #// 
    #// Removes all callbacks from the current filter.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int|bool $priority Optional. The priority number to remove. Default false.
    #//
    def remove_all_filters(self, priority=False):
        
        if (not self.callbacks):
            return
        # end if
        if False == priority:
            self.callbacks = Array()
        elif (php_isset(lambda : self.callbacks[priority])):
            self.callbacks[priority] = None
        # end if
        if self.nesting_level > 0:
            self.resort_active_iterations()
        # end if
    # end def remove_all_filters
    #// 
    #// Calls the callback functions that have been added to a filter hook.
    #// 
    #// @since 4.7.0
    #// 
    #// @param mixed $value The value to filter.
    #// @param array $args  Additional parameters to pass to the callback functions.
    #// This array is expected to include $value at index 0.
    #// @return mixed The filtered value after all hooked functions are applied to it.
    #//
    def apply_filters(self, value=None, args=None):
        
        if (not self.callbacks):
            return value
        # end if
        nesting_level = self.nesting_level
        self.nesting_level += 1
        self.iterations[nesting_level] = php_array_keys(self.callbacks)
        num_args = php_count(args)
        while True:
            self.current_priority[nesting_level] = current(self.iterations[nesting_level])
            priority = self.current_priority[nesting_level]
            for the_ in self.callbacks[priority]:
                if (not self.doing_action):
                    args[0] = value
                # end if
                #// Avoid the array_slice() if possible.
                if 0 == the_["accepted_args"]:
                    value = php_call_user_func(the_["function"])
                elif the_["accepted_args"] >= num_args:
                    value = call_user_func_array(the_["function"], args)
                else:
                    value = call_user_func_array(the_["function"], php_array_slice(args, 0, int(the_["accepted_args"])))
                # end if
            # end for
            
            if False != next(self.iterations[nesting_level]):
                break
            # end if
        # end while
        self.iterations[nesting_level] = None
        self.current_priority[nesting_level] = None
        self.nesting_level -= 1
        return value
    # end def apply_filters
    #// 
    #// Calls the callback functions that have been added to an action hook.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $args Parameters to pass to the callback functions.
    #//
    def do_action(self, args=None):
        
        self.doing_action = True
        self.apply_filters("", args)
        #// If there are recursive calls to the current action, we haven't finished it until we get to the last one.
        if (not self.nesting_level):
            self.doing_action = False
        # end if
    # end def do_action
    #// 
    #// Processes the functions hooked into the 'all' hook.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $args Arguments to pass to the hook callbacks. Passed by reference.
    #//
    def do_all_hook(self, args=None):
        
        nesting_level = self.nesting_level
        self.nesting_level += 1
        self.iterations[nesting_level] = php_array_keys(self.callbacks)
        while True:
            priority = current(self.iterations[nesting_level])
            for the_ in self.callbacks[priority]:
                call_user_func_array(the_["function"], args)
            # end for
            
            if False != next(self.iterations[nesting_level]):
                break
            # end if
        # end while
        self.iterations[nesting_level] = None
        self.nesting_level -= 1
    # end def do_all_hook
    #// 
    #// Return the current priority level of the currently running iteration of the hook.
    #// 
    #// @since 4.7.0
    #// 
    #// @return int|false If the hook is running, return the current priority level. If it isn't running, return false.
    #//
    def current_priority(self):
        
        if False == current(self.iterations):
            return False
        # end if
        return current(current(self.iterations))
    # end def current_priority
    #// 
    #// Normalizes filters set up before WordPress has initialized to WP_Hook objects.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $filters Filters to normalize.
    #// @return WP_Hook[] Array of normalized filters.
    #//
    @classmethod
    def build_preinitialized_hooks(self, filters=None):
        
        #// @var WP_Hook[] $normalized
        normalized = Array()
        for tag,callback_groups in filters:
            if php_is_object(callback_groups) and type(callback_groups).__name__ == "WP_Hook":
                normalized[tag] = callback_groups
                continue
            # end if
            hook = php_new_class("WP_Hook", lambda : WP_Hook())
            #// Loop through callback groups.
            for priority,callbacks in callback_groups:
                #// Loop through callbacks.
                for cb in callbacks:
                    hook.add_filter(tag, cb["function"], priority, cb["accepted_args"])
                # end for
            # end for
            normalized[tag] = hook
        # end for
        return normalized
    # end def build_preinitialized_hooks
    #// 
    #// Determines whether an offset value exists.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/arrayaccess.offsetexists.php
    #// 
    #// @param mixed $offset An offset to check for.
    #// @return bool True if the offset exists, false otherwise.
    #//
    def offsetexists(self, offset=None):
        
        return (php_isset(lambda : self.callbacks[offset]))
    # end def offsetexists
    #// 
    #// Retrieves a value at a specified offset.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/arrayaccess.offsetget.php
    #// 
    #// @param mixed $offset The offset to retrieve.
    #// @return mixed If set, the value at the specified offset, null otherwise.
    #//
    def offsetget(self, offset=None):
        
        return self.callbacks[offset] if (php_isset(lambda : self.callbacks[offset])) else None
    # end def offsetget
    #// 
    #// Sets a value at a specified offset.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/arrayaccess.offsetset.php
    #// 
    #// @param mixed $offset The offset to assign the value to.
    #// @param mixed $value The value to set.
    #//
    def offsetset(self, offset=None, value=None):
        
        if php_is_null(offset):
            self.callbacks[-1] = value
        else:
            self.callbacks[offset] = value
        # end if
    # end def offsetset
    #// 
    #// Unsets a specified offset.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/arrayaccess.offsetunset.php
    #// 
    #// @param mixed $offset The offset to unset.
    #//
    def offsetunset(self, offset=None):
        
        self.callbacks[offset] = None
    # end def offsetunset
    #// 
    #// Returns the current element.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/iterator.current.php
    #// 
    #// @return array Of callbacks at current priority.
    #//
    def current(self):
        
        return current(self.callbacks)
    # end def current
    #// 
    #// Moves forward to the next element.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/iterator.next.php
    #// 
    #// @return array Of callbacks at next priority.
    #//
    def next(self):
        
        return next(self.callbacks)
    # end def next
    #// 
    #// Returns the key of the current element.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/iterator.key.php
    #// 
    #// @return mixed Returns current priority on success, or NULL on failure
    #//
    def key(self):
        
        return key(self.callbacks)
    # end def key
    #// 
    #// Checks if current position is valid.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/iterator.valid.php
    #// 
    #// @return boolean
    #//
    def valid(self):
        
        return key(self.callbacks) != None
    # end def valid
    #// 
    #// Rewinds the Iterator to the first element.
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://www.php.net/manual/en/iterator.rewind.php
    #//
    def rewind(self):
        
        reset(self.callbacks)
    # end def rewind
# end class WP_Hook
