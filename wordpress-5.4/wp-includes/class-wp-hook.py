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
class WP_Hook(IteratorArrayAccess):
    #// 
    #// Hook callbacks.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    callbacks = Array()
    #// 
    #// The priority keys of actively running iterations of a hook.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    iterations = Array()
    #// 
    #// The current priority of actively running iterations of a hook.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    current_priority = Array()
    #// 
    #// Number of levels this hook can be recursively called.
    #// 
    #// @since 4.7.0
    #// @var int
    #//
    nesting_level = 0
    #// 
    #// Flag for if we're current doing an action, rather than a filter.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
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
    def add_filter(self, tag_=None, function_to_add_=None, priority_=None, accepted_args_=None):
        
        
        idx_ = _wp_filter_build_unique_id(tag_, function_to_add_, priority_)
        priority_existed_ = (php_isset(lambda : self.callbacks[priority_]))
        self.callbacks[priority_][idx_] = Array({"function": function_to_add_, "accepted_args": accepted_args_})
        #// If we're adding a new priority to the list, put them back in sorted order.
        if (not priority_existed_) and php_count(self.callbacks) > 1:
            ksort(self.callbacks, SORT_NUMERIC)
        # end if
        if self.nesting_level > 0:
            self.resort_active_iterations(priority_, priority_existed_)
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
    def resort_active_iterations(self, new_priority_=None, priority_existed_=None):
        if new_priority_ is None:
            new_priority_ = False
        # end if
        if priority_existed_ is None:
            priority_existed_ = False
        # end if
        
        new_priorities_ = php_array_keys(self.callbacks)
        #// If there are no remaining hooks, clear out all running iterations.
        if (not new_priorities_):
            for index_,iteration_ in self.iterations:
                self.iterations[index_] = new_priorities_
            # end for
            return
        # end if
        min_ = php_min(new_priorities_)
        for index_,iteration_ in self.iterations:
            current_ = current(iteration_)
            #// If we're already at the end of this iteration, just leave the array pointer where it is.
            if False == current_:
                continue
            # end if
            iteration_ = new_priorities_
            if current_ < min_:
                array_unshift(iteration_, current_)
                continue
            # end if
            while True:
                
                if not (current(iteration_) < current_):
                    break
                # end if
                if False == next(iteration_):
                    break
                # end if
            # end while
            #// If we have a new priority that didn't exist, but ::apply_filters() or ::do_action() thinks it's the current priority...
            if new_priority_ == self.current_priority[index_] and (not priority_existed_):
                #// 
                #// ...and the new priority is the same as what $this->iterations thinks is the previous
                #// priority, we need to move back to it.
                #//
                if False == current(iteration_):
                    #// If we've already moved off the end of the array, go back to the last element.
                    prev_ = php_end(iteration_)
                else:
                    #// Otherwise, just go back to the previous element.
                    prev_ = php_prev(iteration_)
                # end if
                if False == prev_:
                    #// Start of the array. Reset, and go about our day.
                    reset(iteration_)
                elif new_priority_ != prev_:
                    #// Previous wasn't the same. Move forward again.
                    next(iteration_)
                # end if
            # end if
        # end for
        iteration_ = None
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
    def remove_filter(self, tag_=None, function_to_remove_=None, priority_=None):
        
        
        function_key_ = _wp_filter_build_unique_id(tag_, function_to_remove_, priority_)
        exists_ = (php_isset(lambda : self.callbacks[priority_][function_key_]))
        if exists_:
            self.callbacks[priority_][function_key_] = None
            if (not self.callbacks[priority_]):
                self.callbacks[priority_] = None
                if self.nesting_level > 0:
                    self.resort_active_iterations()
                # end if
            # end if
        # end if
        return exists_
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
    def has_filter(self, tag_="", function_to_check_=None):
        if function_to_check_ is None:
            function_to_check_ = False
        # end if
        
        if False == function_to_check_:
            return self.has_filters()
        # end if
        function_key_ = _wp_filter_build_unique_id(tag_, function_to_check_, False)
        if (not function_key_):
            return False
        # end if
        for priority_,callbacks_ in self.callbacks:
            if (php_isset(lambda : callbacks_[function_key_])):
                return priority_
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
        
        
        for callbacks_ in self.callbacks:
            if callbacks_:
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
    def remove_all_filters(self, priority_=None):
        if priority_ is None:
            priority_ = False
        # end if
        
        if (not self.callbacks):
            return
        # end if
        if False == priority_:
            self.callbacks = Array()
        elif (php_isset(lambda : self.callbacks[priority_])):
            self.callbacks[priority_] = None
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
    def apply_filters(self, value_=None, args_=None):
        
        
        if (not self.callbacks):
            return value_
        # end if
        nesting_level_ = self.nesting_level
        self.nesting_level += 1
        self.iterations[nesting_level_] = php_array_keys(self.callbacks)
        num_args_ = php_count(args_)
        while True:
            self.current_priority[nesting_level_] = current(self.iterations[nesting_level_])
            priority_ = self.current_priority[nesting_level_]
            for the__ in self.callbacks[priority_]:
                if (not self.doing_action):
                    args_[0] = value_
                # end if
                #// Avoid the array_slice() if possible.
                if 0 == the__["accepted_args"]:
                    value_ = php_call_user_func(the__["function"])
                elif the__["accepted_args"] >= num_args_:
                    value_ = call_user_func_array(the__["function"], args_)
                else:
                    value_ = call_user_func_array(the__["function"], php_array_slice(args_, 0, php_int(the__["accepted_args"])))
                # end if
            # end for
            
            if False != next(self.iterations[nesting_level_]):
                break
            # end if
        # end while
        self.iterations[nesting_level_] = None
        self.current_priority[nesting_level_] = None
        self.nesting_level -= 1
        return value_
    # end def apply_filters
    #// 
    #// Calls the callback functions that have been added to an action hook.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $args Parameters to pass to the callback functions.
    #//
    def do_action(self, args_=None):
        
        
        self.doing_action = True
        self.apply_filters("", args_)
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
    def do_all_hook(self, args_=None):
        
        
        nesting_level_ = self.nesting_level
        self.nesting_level += 1
        self.iterations[nesting_level_] = php_array_keys(self.callbacks)
        while True:
            priority_ = current(self.iterations[nesting_level_])
            for the__ in self.callbacks[priority_]:
                call_user_func_array(the__["function"], args_)
            # end for
            
            if False != next(self.iterations[nesting_level_]):
                break
            # end if
        # end while
        self.iterations[nesting_level_] = None
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
    def build_preinitialized_hooks(self, filters_=None):
        
        
        #// @var WP_Hook[] $normalized
        normalized_ = Array()
        for tag_,callback_groups_ in filters_:
            if php_is_object(callback_groups_) and type(callback_groups_).__name__ == "WP_Hook":
                normalized_[tag_] = callback_groups_
                continue
            # end if
            hook_ = php_new_class("WP_Hook", lambda : WP_Hook())
            #// Loop through callback groups.
            for priority_,callbacks_ in callback_groups_:
                #// Loop through callbacks.
                for cb_ in callbacks_:
                    hook_.add_filter(tag_, cb_["function"], priority_, cb_["accepted_args"])
                # end for
            # end for
            normalized_[tag_] = hook_
        # end for
        return normalized_
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
    def offsetexists(self, offset_=None):
        
        
        return (php_isset(lambda : self.callbacks[offset_]))
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
    def offsetget(self, offset_=None):
        
        
        return self.callbacks[offset_] if (php_isset(lambda : self.callbacks[offset_])) else None
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
    def offsetset(self, offset_=None, value_=None):
        
        
        if php_is_null(offset_):
            self.callbacks[-1] = value_
        else:
            self.callbacks[offset_] = value_
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
    def offsetunset(self, offset_=None):
        
        
        self.callbacks[offset_] = None
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
