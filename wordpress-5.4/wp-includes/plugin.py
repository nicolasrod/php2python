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
#// The plugin API is located in this file, which allows for creating actions
#// and filters and hooking functions, and methods. The functions or methods will
#// then be run when the action or filter is called.
#// 
#// The API callback examples reference functions, but can be methods of classes.
#// To hook methods, you'll need to pass an array one of two ways.
#// 
#// Any of the syntaxes explained in the PHP documentation for the
#// {@link https://www.php.net/manual/en/language.pseudo-types.php#language.types.callback 'callback'}
#// type are valid.
#// 
#// Also see the {@link https://developer.wordpress.org/plugins/ Plugin API} for
#// more information and examples on how to use a lot of these functions.
#// 
#// This file should have no external dependencies.
#// 
#// @package WordPress
#// @subpackage Plugin
#// @since 1.5.0
#// 
#// Initialize the filter globals.
php_include_file(__DIR__ + "/class-wp-hook.php", once=False)
#// @var WP_Hook[] $wp_filter
global wp_filter,wp_actions,wp_current_filter
php_check_if_defined("wp_filter","wp_actions","wp_current_filter")
if wp_filter:
    wp_filter = WP_Hook.build_preinitialized_hooks(wp_filter)
else:
    wp_filter = Array()
# end if
if (not (php_isset(lambda : wp_actions))):
    wp_actions = Array()
# end if
if (not (php_isset(lambda : wp_current_filter))):
    wp_current_filter = Array()
# end if
#// 
#// Hook a function or method to a specific filter action.
#// 
#// WordPress offers filter hooks to allow plugins to modify
#// various types of internal data at runtime.
#// 
#// A plugin can modify data by binding a callback to a filter hook. When the filter
#// is later applied, each bound callback is run in order of priority, and given
#// the opportunity to modify a value by returning a new value.
#// 
#// The following example shows how a callback function is bound to a filter hook.
#// 
#// Note that `$example` is passed to the callback, (maybe) modified, then returned:
#// 
#// function example_callback( $example ) {
#// Maybe modify $example in some way.
#// return $example;
#// }
#// add_filter( 'example_filter', 'example_callback' );
#// 
#// Bound callbacks can accept from none to the total number of arguments passed as parameters
#// in the corresponding apply_filters() call.
#// 
#// In other words, if an apply_filters() call passes four total arguments, callbacks bound to
#// it can accept none (the same as 1) of the arguments or up to four. The important part is that
#// the `$accepted_args` value must reflect the number of arguments the bound callback *actually
#// opted to accept. If no arguments were accepted by the callback that is considered to be the
#// same as accepting 1 argument. For example:
#// 
#// Filter call.
#// $value = apply_filters( 'hook', $value, $arg2, $arg3 );
#// 
#// Accepting zero/one arguments.
#// function example_callback() {
#// ...
#// return 'some value';
#// }
#// add_filter( 'hook', 'example_callback' ); // Where $priority is default 10, $accepted_args is default 1.
#// 
#// Accepting two arguments (three possible).
#// function example_callback( $value, $arg2 ) {
#// ...
#// return $maybe_modified_value;
#// }
#// add_filter( 'hook', 'example_callback', 10, 2 ); // Where $priority is 10, $accepted_args is 2.
#// 
#// Note:* The function will return true whether or not the callback is valid.
#// It is up to you to take care. This is done for optimization purposes, so
#// everything is as quick as possible.
#// 
#// @since 0.71
#// 
#// @global array $wp_filter A multidimensional array of all hooks and the callbacks hooked to them.
#// 
#// @param string   $tag             The name of the filter to hook the $function_to_add callback to.
#// @param callable $function_to_add The callback to be run when the filter is applied.
#// @param int      $priority        Optional. Used to specify the order in which the functions
#// associated with a particular action are executed.
#// Lower numbers correspond with earlier execution,
#// and functions with the same priority are executed
#// in the order in which they were added to the action. Default 10.
#// @param int      $accepted_args   Optional. The number of arguments the function accepts. Default 1.
#// @return true
#//
def add_filter(tag=None, function_to_add=None, priority=10, accepted_args=1, *args_):
    
    global wp_filter
    php_check_if_defined("wp_filter")
    if (not (php_isset(lambda : wp_filter[tag]))):
        wp_filter[tag] = php_new_class("WP_Hook", lambda : WP_Hook())
    # end if
    wp_filter[tag].add_filter(tag, function_to_add, priority, accepted_args)
    return True
# end def add_filter
#// 
#// Check if any filter has been registered for a hook.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_filter Stores all of the filters and actions.
#// 
#// @param string        $tag               The name of the filter hook.
#// @param callable|bool $function_to_check Optional. The callback to check for. Default false.
#// @return false|int If $function_to_check is omitted, returns boolean for whether the hook has
#// anything registered. When checking a specific function, the priority of that
#// hook is returned, or false if the function is not attached. When using the
#// $function_to_check argument, this function may return a non-boolean value
#// that evaluates to false (e.g.) 0, so use the === operator for testing the
#// return value.
#//
def has_filter(tag=None, function_to_check=False, *args_):
    
    global wp_filter
    php_check_if_defined("wp_filter")
    if (not (php_isset(lambda : wp_filter[tag]))):
        return False
    # end if
    return wp_filter[tag].has_filter(tag, function_to_check)
# end def has_filter
#// 
#// Calls the callback functions that have been added to a filter hook.
#// 
#// The callback functions attached to the filter hook are invoked by calling
#// this function. This function can be used to create a new filter hook by
#// simply calling this function with the name of the new hook specified using
#// the `$tag` parameter.
#// 
#// The function also allows for multiple additional arguments to be passed to hooks.
#// 
#// Example usage:
#// 
#// The filter callback function.
#// function example_callback( $string, $arg1, $arg2 ) {
#// (maybe) modify $string.
#// return $string;
#// }
#// add_filter( 'example_filter', 'example_callback', 10, 3 );
#// 
#// 
#// Apply the filters by calling the 'example_callback()' function
#// that's hooked onto `example_filter` above.
#// 
#// - 'example_filter' is the filter hook.
#// - 'filter me' is the value being filtered.
#// - $arg1 and $arg2 are the additional arguments passed to the callback.
#// $value = apply_filters( 'example_filter', 'filter me', $arg1, $arg2 );
#// 
#// @since 0.71
#// 
#// @global array $wp_filter         Stores all of the filters and actions.
#// @global array $wp_current_filter Stores the list of current filters with the current one last.
#// 
#// @param string $tag     The name of the filter hook.
#// @param mixed  $value   The value to filter.
#// @param mixed  ...$args Additional parameters to pass to the callback functions.
#// @return mixed The filtered value after all hooked functions are applied to it.
#//
def apply_filters(tag=None, value=None, *args_):
    
    global wp_filter,wp_current_filter
    php_check_if_defined("wp_filter","wp_current_filter")
    args = php_func_get_args()
    #// Do 'all' actions first.
    if (php_isset(lambda : wp_filter["all"])):
        wp_current_filter[-1] = tag
        _wp_call_all_hook(args)
    # end if
    if (not (php_isset(lambda : wp_filter[tag]))):
        if (php_isset(lambda : wp_filter["all"])):
            php_array_pop(wp_current_filter)
        # end if
        return value
    # end if
    if (not (php_isset(lambda : wp_filter["all"]))):
        wp_current_filter[-1] = tag
    # end if
    #// Don't pass the tag name to WP_Hook.
    php_array_shift(args)
    filtered = wp_filter[tag].apply_filters(value, args)
    php_array_pop(wp_current_filter)
    return filtered
# end def apply_filters
#// 
#// Calls the callback functions that have been added to a filter hook, specifying arguments in an array.
#// 
#// @since 3.0.0
#// 
#// @see apply_filters() This function is identical, but the arguments passed to the
#// functions hooked to `$tag` are supplied using an array.
#// 
#// @global array $wp_filter         Stores all of the filters and actions.
#// @global array $wp_current_filter Stores the list of current filters with the current one last.
#// 
#// @param string $tag  The name of the filter hook.
#// @param array  $args The arguments supplied to the functions hooked to $tag.
#// @return mixed The filtered value after all hooked functions are applied to it.
#//
def apply_filters_ref_array(tag=None, args=None, *args_):
    
    global wp_filter,wp_current_filter
    php_check_if_defined("wp_filter","wp_current_filter")
    #// Do 'all' actions first.
    if (php_isset(lambda : wp_filter["all"])):
        wp_current_filter[-1] = tag
        all_args = php_func_get_args()
        _wp_call_all_hook(all_args)
    # end if
    if (not (php_isset(lambda : wp_filter[tag]))):
        if (php_isset(lambda : wp_filter["all"])):
            php_array_pop(wp_current_filter)
        # end if
        return args[0]
    # end if
    if (not (php_isset(lambda : wp_filter["all"]))):
        wp_current_filter[-1] = tag
    # end if
    filtered = wp_filter[tag].apply_filters(args[0], args)
    php_array_pop(wp_current_filter)
    return filtered
# end def apply_filters_ref_array
#// 
#// Removes a function from a specified filter hook.
#// 
#// This function removes a function attached to a specified filter hook. This
#// method can be used to remove default functions attached to a specific filter
#// hook and possibly replace them with a substitute.
#// 
#// To remove a hook, the $function_to_remove and $priority arguments must match
#// when the hook was added. This goes for both filters and actions. No warning
#// will be given on removal failure.
#// 
#// @since 1.2.0
#// 
#// @global array $wp_filter Stores all of the filters and actions.
#// 
#// @param string   $tag                The filter hook to which the function to be removed is hooked.
#// @param callable $function_to_remove The name of the function which should be removed.
#// @param int      $priority           Optional. The priority of the function. Default 10.
#// @return bool    Whether the function existed before it was removed.
#//
def remove_filter(tag=None, function_to_remove=None, priority=10, *args_):
    
    global wp_filter
    php_check_if_defined("wp_filter")
    r = False
    if (php_isset(lambda : wp_filter[tag])):
        r = wp_filter[tag].remove_filter(tag, function_to_remove, priority)
        if (not wp_filter[tag].callbacks):
            wp_filter[tag] = None
        # end if
    # end if
    return r
# end def remove_filter
#// 
#// Remove all of the hooks from a filter.
#// 
#// @since 2.7.0
#// 
#// @global array $wp_filter Stores all of the filters and actions.
#// 
#// @param string   $tag      The filter to remove hooks from.
#// @param int|bool $priority Optional. The priority number to remove. Default false.
#// @return true True when finished.
#//
def remove_all_filters(tag=None, priority=False, *args_):
    
    global wp_filter
    php_check_if_defined("wp_filter")
    if (php_isset(lambda : wp_filter[tag])):
        wp_filter[tag].remove_all_filters(priority)
        if (not wp_filter[tag].has_filters()):
            wp_filter[tag] = None
        # end if
    # end if
    return True
# end def remove_all_filters
#// 
#// Retrieve the name of the current filter or action.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_current_filter Stores the list of current filters with the current one last
#// 
#// @return string Hook name of the current filter or action.
#//
def current_filter(*args_):
    
    global wp_current_filter
    php_check_if_defined("wp_current_filter")
    return php_end(wp_current_filter)
# end def current_filter
#// 
#// Retrieve the name of the current action.
#// 
#// @since 3.9.0
#// 
#// @return string Hook name of the current action.
#//
def current_action(*args_):
    
    return current_filter()
# end def current_action
#// 
#// Retrieve the name of a filter currently being processed.
#// 
#// The function current_filter() only returns the most recent filter or action
#// being executed. did_action() returns true once the action is initially
#// processed.
#// 
#// This function allows detection for any filter currently being
#// executed (despite not being the most recent filter to fire, in the case of
#// hooks called from hook callbacks) to be verified.
#// 
#// @since 3.9.0
#// 
#// @see current_filter()
#// @see did_action()
#// @global array $wp_current_filter Current filter.
#// 
#// @param null|string $filter Optional. Filter to check. Defaults to null, which
#// checks if any filter is currently being run.
#// @return bool Whether the filter is currently in the stack.
#//
def doing_filter(filter=None, *args_):
    
    global wp_current_filter
    php_check_if_defined("wp_current_filter")
    if None == filter:
        return (not php_empty(lambda : wp_current_filter))
    # end if
    return php_in_array(filter, wp_current_filter)
# end def doing_filter
#// 
#// Retrieve the name of an action currently being processed.
#// 
#// @since 3.9.0
#// 
#// @param string|null $action Optional. Action to check. Defaults to null, which checks
#// if any action is currently being run.
#// @return bool Whether the action is currently in the stack.
#//
def doing_action(action=None, *args_):
    
    return doing_filter(action)
# end def doing_action
#// 
#// Hooks a function on to a specific action.
#// 
#// Actions are the hooks that the WordPress core launches at specific points
#// during execution, or when specific events occur. Plugins can specify that
#// one or more of its PHP functions are executed at these points, using the
#// Action API.
#// 
#// @since 1.2.0
#// 
#// @param string   $tag             The name of the action to which the $function_to_add is hooked.
#// @param callable $function_to_add The name of the function you wish to be called.
#// @param int      $priority        Optional. Used to specify the order in which the functions
#// associated with a particular action are executed. Default 10.
#// Lower numbers correspond with earlier execution,
#// and functions with the same priority are executed
#// in the order in which they were added to the action.
#// @param int      $accepted_args   Optional. The number of arguments the function accepts. Default 1.
#// @return true Will always return true.
#//
def add_action(tag=None, function_to_add=None, priority=10, accepted_args=1, *args_):
    
    return add_filter(tag, function_to_add, priority, accepted_args)
# end def add_action
#// 
#// Execute functions hooked on a specific action hook.
#// 
#// This function invokes all functions attached to action hook `$tag`. It is
#// possible to create new action hooks by simply calling this function,
#// specifying the name of the new hook using the `$tag` parameter.
#// 
#// You can pass extra arguments to the hooks, much like you can with `apply_filters()`.
#// 
#// Example usage:
#// 
#// The action callback function.
#// function example_callback( $arg1, $arg2 ) {
#// (maybe) do something with the args.
#// }
#// add_action( 'example_action', 'example_callback', 10, 2 );
#// 
#// 
#// Trigger the actions by calling the 'example_callback()' function
#// that's hooked onto `example_action` above.
#// 
#// - 'example_action' is the action hook.
#// - $arg1 and $arg2 are the additional arguments passed to the callback.
#// $value = do_action( 'example_action', $arg1, $arg2 );
#// 
#// @since 1.2.0
#// @since 5.3.0 Formalized the existing and already documented `...$arg` parameter
#// by adding it to the function signature.
#// 
#// @global array $wp_filter         Stores all of the filters and actions.
#// @global array $wp_actions        Increments the amount of times action was triggered.
#// @global array $wp_current_filter Stores the list of current filters with the current one last.
#// 
#// @param string $tag    The name of the action to be executed.
#// @param mixed  ...$arg Optional. Additional arguments which are passed on to the
#// functions hooked to the action. Default empty.
#//
def do_action(tag=None, *arg):
    
    global wp_filter,wp_actions,wp_current_filter
    php_check_if_defined("wp_filter","wp_actions","wp_current_filter")
    if (not (php_isset(lambda : wp_actions[tag]))):
        wp_actions[tag] = 1
    else:
        wp_actions[tag] += 1
    # end if
    #// Do 'all' actions first.
    if (php_isset(lambda : wp_filter["all"])):
        wp_current_filter[-1] = tag
        all_args = php_func_get_args()
        _wp_call_all_hook(all_args)
    # end if
    if (not (php_isset(lambda : wp_filter[tag]))):
        if (php_isset(lambda : wp_filter["all"])):
            php_array_pop(wp_current_filter)
        # end if
        return
    # end if
    if (not (php_isset(lambda : wp_filter["all"]))):
        wp_current_filter[-1] = tag
    # end if
    if php_empty(lambda : arg):
        arg[-1] = ""
    elif php_is_array(arg[0]) and 1 == php_count(arg[0]) and (php_isset(lambda : arg[0][0])) and php_is_object(arg[0][0]):
        #// Backward compatibility for PHP4-style passing of `array( &$this )` as action `$arg`.
        arg[0] = arg[0][0]
    # end if
    wp_filter[tag].do_action(arg)
    php_array_pop(wp_current_filter)
# end def do_action
#// 
#// Retrieve the number of times an action is fired.
#// 
#// @since 2.1.0
#// 
#// @global array $wp_actions Increments the amount of times action was triggered.
#// 
#// @param string $tag The name of the action hook.
#// @return int The number of times action hook $tag is fired.
#//
def did_action(tag=None, *args_):
    
    global wp_actions
    php_check_if_defined("wp_actions")
    if (not (php_isset(lambda : wp_actions[tag]))):
        return 0
    # end if
    return wp_actions[tag]
# end def did_action
#// 
#// Calls the callback functions that have been added to an action hook, specifying arguments in an array.
#// 
#// @since 2.1.0
#// 
#// @see do_action() This function is identical, but the arguments passed to the
#// functions hooked to `$tag` are supplied using an array.
#// @global array $wp_filter         Stores all of the filters and actions.
#// @global array $wp_actions        Increments the amount of times action was triggered.
#// @global array $wp_current_filter Stores the list of current filters with the current one last.
#// 
#// @param string $tag  The name of the action to be executed.
#// @param array  $args The arguments supplied to the functions hooked to `$tag`.
#//
def do_action_ref_array(tag=None, args=None, *args_):
    
    global wp_filter,wp_actions,wp_current_filter
    php_check_if_defined("wp_filter","wp_actions","wp_current_filter")
    if (not (php_isset(lambda : wp_actions[tag]))):
        wp_actions[tag] = 1
    else:
        wp_actions[tag] += 1
    # end if
    #// Do 'all' actions first.
    if (php_isset(lambda : wp_filter["all"])):
        wp_current_filter[-1] = tag
        all_args = php_func_get_args()
        _wp_call_all_hook(all_args)
    # end if
    if (not (php_isset(lambda : wp_filter[tag]))):
        if (php_isset(lambda : wp_filter["all"])):
            php_array_pop(wp_current_filter)
        # end if
        return
    # end if
    if (not (php_isset(lambda : wp_filter["all"]))):
        wp_current_filter[-1] = tag
    # end if
    wp_filter[tag].do_action(args)
    php_array_pop(wp_current_filter)
# end def do_action_ref_array
#// 
#// Check if any action has been registered for a hook.
#// 
#// @since 2.5.0
#// 
#// @see has_filter() has_action() is an alias of has_filter().
#// 
#// @param string        $tag               The name of the action hook.
#// @param callable|bool $function_to_check Optional. The callback to check for. Default false.
#// @return bool|int If $function_to_check is omitted, returns boolean for whether the hook has
#// anything registered. When checking a specific function, the priority of that
#// hook is returned, or false if the function is not attached. When using the
#// $function_to_check argument, this function may return a non-boolean value
#// that evaluates to false (e.g.) 0, so use the === operator for testing the
#// return value.
#//
def has_action(tag=None, function_to_check=False, *args_):
    
    return has_filter(tag, function_to_check)
# end def has_action
#// 
#// Removes a function from a specified action hook.
#// 
#// This function removes a function attached to a specified action hook. This
#// method can be used to remove default functions attached to a specific filter
#// hook and possibly replace them with a substitute.
#// 
#// @since 1.2.0
#// 
#// @param string   $tag                The action hook to which the function to be removed is hooked.
#// @param callable $function_to_remove The name of the function which should be removed.
#// @param int      $priority           Optional. The priority of the function. Default 10.
#// @return bool Whether the function is removed.
#//
def remove_action(tag=None, function_to_remove=None, priority=10, *args_):
    
    return remove_filter(tag, function_to_remove, priority)
# end def remove_action
#// 
#// Remove all of the hooks from an action.
#// 
#// @since 2.7.0
#// 
#// @param string   $tag      The action to remove hooks from.
#// @param int|bool $priority The priority number to remove them from. Default false.
#// @return true True when finished.
#//
def remove_all_actions(tag=None, priority=False, *args_):
    
    return remove_all_filters(tag, priority)
# end def remove_all_actions
#// 
#// Fires functions attached to a deprecated filter hook.
#// 
#// When a filter hook is deprecated, the apply_filters() call is replaced with
#// apply_filters_deprecated(), which triggers a deprecation notice and then fires
#// the original filter hook.
#// 
#// Note: the value and extra arguments passed to the original apply_filters() call
#// must be passed here to `$args` as an array. For example:
#// 
#// Old filter.
#// return apply_filters( 'wpdocs_filter', $value, $extra_arg );
#// 
#// Deprecated.
#// return apply_filters_deprecated( 'wpdocs_filter', array( $value, $extra_arg ), '4.9.0', 'wpdocs_new_filter' );
#// 
#// @since 4.6.0
#// 
#// @see _deprecated_hook()
#// 
#// @param string $tag         The name of the filter hook.
#// @param array  $args        Array of additional function arguments to be passed to apply_filters().
#// @param string $version     The version of WordPress that deprecated the hook.
#// @param string $replacement Optional. The hook that should have been used. Default null.
#// @param string $message     Optional. A message regarding the change. Default null.
#//
def apply_filters_deprecated(tag=None, args=None, version=None, replacement=None, message=None, *args_):
    
    if (not has_filter(tag)):
        return args[0]
    # end if
    _deprecated_hook(tag, version, replacement, message)
    return apply_filters_ref_array(tag, args)
# end def apply_filters_deprecated
#// 
#// Fires functions attached to a deprecated action hook.
#// 
#// When an action hook is deprecated, the do_action() call is replaced with
#// do_action_deprecated(), which triggers a deprecation notice and then fires
#// the original hook.
#// 
#// @since 4.6.0
#// 
#// @see _deprecated_hook()
#// 
#// @param string $tag         The name of the action hook.
#// @param array  $args        Array of additional function arguments to be passed to do_action().
#// @param string $version     The version of WordPress that deprecated the hook.
#// @param string $replacement Optional. The hook that should have been used. Default null.
#// @param string $message     Optional. A message regarding the change. Default null.
#//
def do_action_deprecated(tag=None, args=None, version=None, replacement=None, message=None, *args_):
    
    if (not has_action(tag)):
        return
    # end if
    _deprecated_hook(tag, version, replacement, message)
    do_action_ref_array(tag, args)
# end def do_action_deprecated
#// 
#// Functions for handling plugins.
#// 
#// 
#// Gets the basename of a plugin.
#// 
#// This method extracts the name of a plugin from its filename.
#// 
#// @since 1.5.0
#// 
#// @global array $wp_plugin_paths
#// 
#// @param string $file The filename of plugin.
#// @return string The name of a plugin.
#//
def plugin_basename(file=None, *args_):
    
    global wp_plugin_paths
    php_check_if_defined("wp_plugin_paths")
    #// $wp_plugin_paths contains normalized paths.
    file = wp_normalize_path(file)
    arsort(wp_plugin_paths)
    for dir,realdir in wp_plugin_paths:
        if php_strpos(file, realdir) == 0:
            file = dir + php_substr(file, php_strlen(realdir))
        # end if
    # end for
    plugin_dir = wp_normalize_path(WP_PLUGIN_DIR)
    mu_plugin_dir = wp_normalize_path(WPMU_PLUGIN_DIR)
    #// Get relative path from plugins directory.
    file = php_preg_replace("#^" + preg_quote(plugin_dir, "#") + "/|^" + preg_quote(mu_plugin_dir, "#") + "/#", "", file)
    file = php_trim(file, "/")
    return file
# end def plugin_basename
#// 
#// Register a plugin's real path.
#// 
#// This is used in plugin_basename() to resolve symlinked paths.
#// 
#// @since 3.9.0
#// 
#// @see wp_normalize_path()
#// 
#// @global array $wp_plugin_paths
#// 
#// @staticvar string $wp_plugin_path
#// @staticvar string $wpmu_plugin_path
#// 
#// @param string $file Known path to the file.
#// @return bool Whether the path was able to be registered.
#//
def wp_register_plugin_realpath(file=None, *args_):
    
    global wp_plugin_paths
    php_check_if_defined("wp_plugin_paths")
    wp_plugin_path = None
    wpmu_plugin_path = None
    if (not (php_isset(lambda : wp_plugin_path))):
        wp_plugin_path = wp_normalize_path(WP_PLUGIN_DIR)
        wpmu_plugin_path = wp_normalize_path(WPMU_PLUGIN_DIR)
    # end if
    plugin_path = wp_normalize_path(php_dirname(file))
    plugin_realpath = wp_normalize_path(php_dirname(php_realpath(file)))
    if plugin_path == wp_plugin_path or plugin_path == wpmu_plugin_path:
        return False
    # end if
    if plugin_path != plugin_realpath:
        wp_plugin_paths[plugin_path] = plugin_realpath
    # end if
    return True
# end def wp_register_plugin_realpath
#// 
#// Get the filesystem directory path (with trailing slash) for the plugin __FILE__ passed in.
#// 
#// @since 2.8.0
#// 
#// @param string $file The filename of the plugin (__FILE__).
#// @return string the filesystem path of the directory that contains the plugin.
#//
def plugin_dir_path(file=None, *args_):
    
    return trailingslashit(php_dirname(file))
# end def plugin_dir_path
#// 
#// Get the URL directory path (with trailing slash) for the plugin __FILE__ passed in.
#// 
#// @since 2.8.0
#// 
#// @param string $file The filename of the plugin (__FILE__).
#// @return string the URL path of the directory that contains the plugin.
#//
def plugin_dir_url(file=None, *args_):
    
    return trailingslashit(plugins_url("", file))
# end def plugin_dir_url
#// 
#// Set the activation hook for a plugin.
#// 
#// When a plugin is activated, the action 'activate_PLUGINNAME' hook is
#// called. In the name of this hook, PLUGINNAME is replaced with the name
#// of the plugin, including the optional subdirectory. For example, when the
#// plugin is located in wp-content/plugins/sampleplugin/sample.php, then
#// the name of this hook will become 'activate_sampleplugin/sample.php'.
#// 
#// When the plugin consists of only one file and is (as by default) located at
#// wp-content/plugins/sample.php the name of this hook will be
#// 'activate_sample.php'.
#// 
#// @since 2.0.0
#// 
#// @param string   $file     The filename of the plugin including the path.
#// @param callable $function The function hooked to the 'activate_PLUGIN' action.
#//
def register_activation_hook(file=None, function=None, *args_):
    
    file = plugin_basename(file)
    add_action("activate_" + file, function)
# end def register_activation_hook
#// 
#// Set the deactivation hook for a plugin.
#// 
#// When a plugin is deactivated, the action 'deactivate_PLUGINNAME' hook is
#// called. In the name of this hook, PLUGINNAME is replaced with the name
#// of the plugin, including the optional subdirectory. For example, when the
#// plugin is located in wp-content/plugins/sampleplugin/sample.php, then
#// the name of this hook will become 'deactivate_sampleplugin/sample.php'.
#// 
#// When the plugin consists of only one file and is (as by default) located at
#// wp-content/plugins/sample.php the name of this hook will be
#// 'deactivate_sample.php'.
#// 
#// @since 2.0.0
#// 
#// @param string   $file     The filename of the plugin including the path.
#// @param callable $function The function hooked to the 'deactivate_PLUGIN' action.
#//
def register_deactivation_hook(file=None, function=None, *args_):
    
    file = plugin_basename(file)
    add_action("deactivate_" + file, function)
# end def register_deactivation_hook
#// 
#// Set the uninstallation hook for a plugin.
#// 
#// Registers the uninstall hook that will be called when the user clicks on the
#// uninstall link that calls for the plugin to uninstall itself. The link won't
#// be active unless the plugin hooks into the action.
#// 
#// The plugin should not run arbitrary code outside of functions, when
#// registering the uninstall hook. In order to run using the hook, the plugin
#// will have to be included, which means that any code laying outside of a
#// function will be run during the uninstallation process. The plugin should not
#// hinder the uninstallation process.
#// 
#// If the plugin can not be written without running code within the plugin, then
#// the plugin should create a file named 'uninstall.php' in the base plugin
#// folder. This file will be called, if it exists, during the uninstallation process
#// bypassing the uninstall hook. The plugin, when using the 'uninstall.php'
#// should always check for the 'WP_UNINSTALL_PLUGIN' constant, before
#// executing.
#// 
#// @since 2.7.0
#// 
#// @param string   $file     Plugin file.
#// @param callable $callback The callback to run when the hook is called. Must be
#// a static method or function.
#//
def register_uninstall_hook(file=None, callback=None, *args_):
    
    if php_is_array(callback) and php_is_object(callback[0]):
        _doing_it_wrong(__FUNCTION__, __("Only a static class method or function can be used in an uninstall hook."), "3.1.0")
        return
    # end if
    #// 
    #// The option should not be autoloaded, because it is not needed in most
    #// cases. Emphasis should be put on using the 'uninstall.php' way of
    #// uninstalling the plugin.
    #//
    uninstallable_plugins = get_option("uninstall_plugins")
    plugin_basename = plugin_basename(file)
    if (not (php_isset(lambda : uninstallable_plugins[plugin_basename]))) or uninstallable_plugins[plugin_basename] != callback:
        uninstallable_plugins[plugin_basename] = callback
        update_option("uninstall_plugins", uninstallable_plugins)
    # end if
# end def register_uninstall_hook
#// 
#// Call the 'all' hook, which will process the functions hooked into it.
#// 
#// The 'all' hook passes all of the arguments or parameters that were used for
#// the hook, which this function was called for.
#// 
#// This function is used internally for apply_filters(), do_action(), and
#// do_action_ref_array() and is not meant to be used from outside those
#// functions. This function does not check for the existence of the all hook, so
#// it will fail unless the all hook exists prior to this function call.
#// 
#// @since 2.5.0
#// @access private
#// 
#// @global array $wp_filter Stores all of the filters and actions.
#// 
#// @param array $args The collected parameters from the hook that was called.
#//
def _wp_call_all_hook(args=None, *args_):
    
    global wp_filter
    php_check_if_defined("wp_filter")
    wp_filter["all"].do_all_hook(args)
# end def _wp_call_all_hook
#// 
#// Build Unique ID for storage and retrieval.
#// 
#// The old way to serialize the callback caused issues and this function is the
#// solution. It works by checking for objects and creating a new property in
#// the class to keep track of the object and new objects of the same class that
#// need to be added.
#// 
#// It also allows for the removal of actions and filters for objects after they
#// change class properties. It is possible to include the property $wp_filter_id
#// in your class and set it to "null" or a number to bypass the workaround.
#// However this will prevent you from adding new classes and any new classes
#// will overwrite the previous hook by the same class.
#// 
#// Functions and static method callbacks are just returned as strings and
#// shouldn't have any speed penalty.
#// 
#// @link https://core.trac.wordpress.org/ticket/3875
#// 
#// @since 2.2.3
#// @since 5.3.0 Removed workarounds for spl_object_hash().
#// `$tag` and `$priority` are no longer used,
#// and the function always returns a string.
#// @access private
#// 
#// @param string   $tag      Unused. The name of the filter to build ID for.
#// @param callable $function The function to generate ID for.
#// @param int      $priority Unused. The order in which the functions
#// associated with a particular action are executed.
#// @return string Unique function ID for usage as array key.
#//
def _wp_filter_build_unique_id(tag=None, function=None, priority=None, *args_):
    
    if php_is_string(function):
        return function
    # end if
    if php_is_object(function):
        #// Closures are currently implemented as objects.
        function = Array(function, "")
    else:
        function = function
    # end if
    if php_is_object(function[0]):
        #// Object class calling.
        return spl_object_hash(function[0]) + function[1]
    elif php_is_string(function[0]):
        #// Static calling.
        return function[0] + "::" + function[1]
    # end if
# end def _wp_filter_build_unique_id
