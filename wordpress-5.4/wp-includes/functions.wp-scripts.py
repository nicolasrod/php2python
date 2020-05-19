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
#// Dependencies API: Scripts functions
#// 
#// @since 2.6.0
#// 
#// @package WordPress
#// @subpackage Dependencies
#// 
#// 
#// Initialize $wp_scripts if it has not been set.
#// 
#// @global WP_Scripts $wp_scripts
#// 
#// @since 4.2.0
#// 
#// @return WP_Scripts WP_Scripts instance.
#//
def wp_scripts(*_args_):
    
    
    global wp_scripts_
    php_check_if_defined("wp_scripts_")
    if (not type(wp_scripts_).__name__ == "WP_Scripts"):
        wp_scripts_ = php_new_class("WP_Scripts", lambda : WP_Scripts())
    # end if
    return wp_scripts_
# end def wp_scripts
#// 
#// Helper function to output a _doing_it_wrong message when applicable.
#// 
#// @ignore
#// @since 4.2.0
#// 
#// @param string $function Function name.
#//
def _wp_scripts_maybe_doing_it_wrong(function_=None, *_args_):
    
    
    if did_action("init") or did_action("admin_enqueue_scripts") or did_action("wp_enqueue_scripts") or did_action("login_enqueue_scripts"):
        return
    # end if
    _doing_it_wrong(function_, php_sprintf(__("Scripts and styles should not be registered or enqueued until the %1$s, %2$s, or %3$s hooks."), "<code>wp_enqueue_scripts</code>", "<code>admin_enqueue_scripts</code>", "<code>login_enqueue_scripts</code>"), "3.3.0")
# end def _wp_scripts_maybe_doing_it_wrong
#// 
#// Prints scripts in document head that are in the $handles queue.
#// 
#// Called by admin-header.php and {@see 'wp_head'} hook. Since it is called by wp_head on every page load,
#// the function does not instantiate the WP_Scripts object unless script names are explicitly passed.
#// Makes use of already-instantiated $wp_scripts global if present. Use provided {@see 'wp_print_scripts'}
#// hook to register/enqueue new scripts.
#// 
#// @see WP_Scripts::do_item()
#// @global WP_Scripts $wp_scripts The WP_Scripts object for printing scripts.
#// 
#// @since 2.1.0
#// 
#// @param string|bool|array $handles Optional. Scripts to be printed. Default 'false'.
#// @return string[] On success, an array of handles of processed WP_Dependencies items; otherwise, an empty array.
#//
def wp_print_scripts(handles_=None, *_args_):
    if handles_ is None:
        handles_ = False
    # end if
    
    #// 
    #// Fires before scripts in the $handles queue are printed.
    #// 
    #// @since 2.1.0
    #//
    do_action("wp_print_scripts")
    if "" == handles_:
        #// For 'wp_head'.
        handles_ = False
    # end if
    _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
    global wp_scripts_
    php_check_if_defined("wp_scripts_")
    if (not type(wp_scripts_).__name__ == "WP_Scripts"):
        if (not handles_):
            return Array()
            pass
        # end if
    # end if
    return wp_scripts().do_items(handles_)
# end def wp_print_scripts
#// 
#// Adds extra code to a registered script.
#// 
#// Code will only be added if the script is already in the queue.
#// Accepts a string $data containing the Code. If two or more code blocks
#// are added to the same script $handle, they will be printed in the order
#// they were added, i.e. the latter added code can redeclare the previous.
#// 
#// @since 4.5.0
#// 
#// @see WP_Scripts::add_inline_script()
#// 
#// @param string $handle   Name of the script to add the inline script to.
#// @param string $data     String containing the javascript to be added.
#// @param string $position Optional. Whether to add the inline script before the handle
#// or after. Default 'after'.
#// @return bool True on success, false on failure.
#//
def wp_add_inline_script(handle_=None, data_=None, position_="after", *_args_):
    
    
    _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
    if False != php_stripos(data_, "</script>"):
        _doing_it_wrong(inspect.currentframe().f_code.co_name, php_sprintf(__("Do not pass %1$s tags to %2$s."), "<code>&lt;script&gt;</code>", "<code>wp_add_inline_script()</code>"), "4.5.0")
        data_ = php_trim(php_preg_replace("#<script[^>]*>(.*)</script>#is", "$1", data_))
    # end if
    return wp_scripts().add_inline_script(handle_, data_, position_)
# end def wp_add_inline_script
#// 
#// Register a new script.
#// 
#// Registers a script to be enqueued later using the wp_enqueue_script() function.
#// 
#// @see WP_Dependencies::add()
#// @see WP_Dependencies::add_data()
#// 
#// @since 2.1.0
#// @since 4.3.0 A return value was added.
#// 
#// @param string           $handle    Name of the script. Should be unique.
#// @param string|bool      $src       Full URL of the script, or path of the script relative to the WordPress root directory.
#// If source is set to false, script is an alias of other scripts it depends on.
#// @param string[]         $deps      Optional. An array of registered script handles this script depends on. Default empty array.
#// @param string|bool|null $ver       Optional. String specifying script version number, if it has one, which is added to the URL
#// as a query string for cache busting purposes. If version is set to false, a version
#// number is automatically added equal to current installed WordPress version.
#// If set to null, no version is added.
#// @param bool             $in_footer Optional. Whether to enqueue the script before </body> instead of in the <head>.
#// Default 'false'.
#// @return bool Whether the script has been registered. True on success, false on failure.
#//
def wp_register_script(handle_=None, src_=None, deps_=None, ver_=None, in_footer_=None, *_args_):
    if deps_ is None:
        deps_ = Array()
    # end if
    if ver_ is None:
        ver_ = False
    # end if
    if in_footer_ is None:
        in_footer_ = False
    # end if
    
    wp_scripts_ = wp_scripts()
    _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
    registered_ = wp_scripts_.add(handle_, src_, deps_, ver_)
    if in_footer_:
        wp_scripts_.add_data(handle_, "group", 1)
    # end if
    return registered_
# end def wp_register_script
#// 
#// Localize a script.
#// 
#// Works only if the script has already been added.
#// 
#// Accepts an associative array $l10n and creates a JavaScript object:
#// 
#// "$object_name" = {
#// key: value,
#// key: value,
#// ...
#// }
#// 
#// @see WP_Scripts::localize()
#// @link https://core.trac.wordpress.org/ticket/11520
#// @global WP_Scripts $wp_scripts The WP_Scripts object for printing scripts.
#// 
#// @since 2.2.0
#// 
#// @todo Documentation cleanup
#// 
#// @param string $handle      Script handle the data will be attached to.
#// @param string $object_name Name for the JavaScript object. Passed directly, so it should be qualified JS variable.
#// Example: '/[a-zA-Z0-9_]+/'.
#// @param array $l10n         The data itself. The data can be either a single or multi-dimensional array.
#// @return bool True if the script was successfully localized, false otherwise.
#//
def wp_localize_script(handle_=None, object_name_=None, l10n_=None, *_args_):
    
    
    global wp_scripts_
    php_check_if_defined("wp_scripts_")
    if (not type(wp_scripts_).__name__ == "WP_Scripts"):
        _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
        return False
    # end if
    return wp_scripts_.localize(handle_, object_name_, l10n_)
# end def wp_localize_script
#// 
#// Sets translated strings for a script.
#// 
#// Works only if the script has already been added.
#// 
#// @see WP_Scripts::set_translations()
#// @global WP_Scripts $wp_scripts The WP_Scripts object for printing scripts.
#// 
#// @since 5.0.0
#// @since 5.1.0 The `$domain` parameter was made optional.
#// 
#// @param string $handle Script handle the textdomain will be attached to.
#// @param string $domain Optional. Text domain. Default 'default'.
#// @param string $path   Optional. The full file path to the directory containing translation files.
#// @return bool True if the text domain was successfully localized, false otherwise.
#//
def wp_set_script_translations(handle_=None, domain_="default", path_=None, *_args_):
    if path_ is None:
        path_ = None
    # end if
    
    global wp_scripts_
    php_check_if_defined("wp_scripts_")
    if (not type(wp_scripts_).__name__ == "WP_Scripts"):
        _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
        return False
    # end if
    return wp_scripts_.set_translations(handle_, domain_, path_)
# end def wp_set_script_translations
#// 
#// Remove a registered script.
#// 
#// Note: there are intentional safeguards in place to prevent critical admin scripts,
#// such as jQuery core, from being unregistered.
#// 
#// @see WP_Dependencies::remove()
#// 
#// @since 2.1.0
#// 
#// @param string $handle Name of the script to be removed.
#//
def wp_deregister_script(handle_=None, *_args_):
    
    
    _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
    #// 
    #// Do not allow accidental or negligent de-registering of critical scripts in the admin.
    #// Show minimal remorse if the correct hook is used.
    #//
    current_filter_ = current_filter()
    if is_admin() and "admin_enqueue_scripts" != current_filter_ or "wp-login.php" == PHP_GLOBALS["pagenow"] and "login_enqueue_scripts" != current_filter_:
        no_ = Array("jquery", "jquery-core", "jquery-migrate", "jquery-ui-core", "jquery-ui-accordion", "jquery-ui-autocomplete", "jquery-ui-button", "jquery-ui-datepicker", "jquery-ui-dialog", "jquery-ui-draggable", "jquery-ui-droppable", "jquery-ui-menu", "jquery-ui-mouse", "jquery-ui-position", "jquery-ui-progressbar", "jquery-ui-resizable", "jquery-ui-selectable", "jquery-ui-slider", "jquery-ui-sortable", "jquery-ui-spinner", "jquery-ui-tabs", "jquery-ui-tooltip", "jquery-ui-widget", "underscore", "backbone")
        if php_in_array(handle_, no_):
            message_ = php_sprintf(__("Do not deregister the %1$s script in the administration area. To target the front-end theme, use the %2$s hook."), str("<code>") + str(handle_) + str("</code>"), "<code>wp_enqueue_scripts</code>")
            _doing_it_wrong(inspect.currentframe().f_code.co_name, message_, "3.6.0")
            return
        # end if
    # end if
    wp_scripts().remove(handle_)
# end def wp_deregister_script
#// 
#// Enqueue a script.
#// 
#// Registers the script if $src provided (does NOT overwrite), and enqueues it.
#// 
#// @see WP_Dependencies::add()
#// @see WP_Dependencies::add_data()
#// @see WP_Dependencies::enqueue()
#// 
#// @since 2.1.0
#// 
#// @param string           $handle    Name of the script. Should be unique.
#// @param string           $src       Full URL of the script, or path of the script relative to the WordPress root directory.
#// Default empty.
#// @param string[]         $deps      Optional. An array of registered script handles this script depends on. Default empty array.
#// @param string|bool|null $ver       Optional. String specifying script version number, if it has one, which is added to the URL
#// as a query string for cache busting purposes. If version is set to false, a version
#// number is automatically added equal to current installed WordPress version.
#// If set to null, no version is added.
#// @param bool             $in_footer Optional. Whether to enqueue the script before </body> instead of in the <head>.
#// Default 'false'.
#//
def wp_enqueue_script(handle_=None, src_="", deps_=None, ver_=None, in_footer_=None, *_args_):
    if deps_ is None:
        deps_ = Array()
    # end if
    if ver_ is None:
        ver_ = False
    # end if
    if in_footer_ is None:
        in_footer_ = False
    # end if
    
    wp_scripts_ = wp_scripts()
    _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
    if src_ or in_footer_:
        _handle_ = php_explode("?", handle_)
        if src_:
            wp_scripts_.add(_handle_[0], src_, deps_, ver_)
        # end if
        if in_footer_:
            wp_scripts_.add_data(_handle_[0], "group", 1)
        # end if
    # end if
    wp_scripts_.enqueue(handle_)
# end def wp_enqueue_script
#// 
#// Remove a previously enqueued script.
#// 
#// @see WP_Dependencies::dequeue()
#// 
#// @since 3.1.0
#// 
#// @param string $handle Name of the script to be removed.
#//
def wp_dequeue_script(handle_=None, *_args_):
    
    
    _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
    wp_scripts().dequeue(handle_)
# end def wp_dequeue_script
#// 
#// Determines whether a script has been added to the queue.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.8.0
#// @since 3.5.0 'enqueued' added as an alias of the 'queue' list.
#// 
#// @param string $handle Name of the script.
#// @param string $list   Optional. Status of the script to check. Default 'enqueued'.
#// Accepts 'enqueued', 'registered', 'queue', 'to_do', and 'done'.
#// @return bool Whether the script is queued.
#//
def wp_script_is(handle_=None, list_="enqueued", *_args_):
    
    
    _wp_scripts_maybe_doing_it_wrong(inspect.currentframe().f_code.co_name)
    return php_bool(wp_scripts().query(handle_, list_))
# end def wp_script_is
#// 
#// Add metadata to a script.
#// 
#// Works only if the script has already been added.
#// 
#// Possible values for $key and $value:
#// 'conditional' string Comments for IE 6, lte IE 7, etc.
#// 
#// @since 4.2.0
#// 
#// @see WP_Dependencies::add_data()
#// 
#// @param string $handle Name of the script.
#// @param string $key    Name of data point for which we're storing a value.
#// @param mixed  $value  String containing the data to be added.
#// @return bool True on success, false on failure.
#//
def wp_script_add_data(handle_=None, key_=None, value_=None, *_args_):
    
    
    return wp_scripts().add_data(handle_, key_, value_)
# end def wp_script_add_data
