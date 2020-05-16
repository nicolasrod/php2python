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
#// Option API
#// 
#// @package WordPress
#// @subpackage Option
#// 
#// 
#// Retrieves an option value based on an option name.
#// 
#// If the option does not exist or does not have a value, then the return value
#// will be false. This is useful to check whether you need to install an option
#// and is commonly used during installation of plugin options and to test
#// whether upgrading is required.
#// 
#// If the option was serialized then it will be unserialized when it is returned.
#// 
#// Any scalar values will be returned as strings. You may coerce the return type of
#// a given option by registering an {@see 'option_$option'} filter callback.
#// 
#// @since 1.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $option  Name of option to retrieve. Expected to not be SQL-escaped.
#// @param mixed  $default Optional. Default value to return if the option does not exist.
#// @return mixed Value set for the option.
#//
def get_option(option=None, default=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    option = php_trim(option)
    if php_empty(lambda : option):
        return False
    # end if
    #// 
    #// Filters the value of an existing option before it is retrieved.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// Passing a truthy value to the filter will short-circuit retrieving
    #// the option value, returning the passed value instead.
    #// 
    #// @since 1.5.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// @since 4.9.0 The `$default` parameter was added.
    #// 
    #// @param bool|mixed $pre_option The value to return instead of the option value. This differs from
    #// `$default`, which is used as the fallback value in the event the option
    #// doesn't exist elsewhere in get_option(). Default false (to skip past the
    #// short-circuit).
    #// @param string     $option     Option name.
    #// @param mixed      $default    The fallback value to return if the option does not exist.
    #// Default is false.
    #//
    pre = apply_filters(str("pre_option_") + str(option), False, option, default)
    if False != pre:
        return pre
    # end if
    if php_defined("WP_SETUP_CONFIG"):
        return False
    # end if
    #// Distinguish between `false` as a default, and not passing one.
    passed_default = php_func_num_args() > 1
    if (not wp_installing()):
        #// Prevent non-existent options from triggering multiple queries.
        notoptions = wp_cache_get("notoptions", "options")
        if (php_isset(lambda : notoptions[option])):
            #// 
            #// Filters the default value for an option.
            #// 
            #// The dynamic portion of the hook name, `$option`, refers to the option name.
            #// 
            #// @since 3.4.0
            #// @since 4.4.0 The `$option` parameter was added.
            #// @since 4.7.0 The `$passed_default` parameter was added to distinguish between a `false` value and the default parameter value.
            #// 
            #// @param mixed  $default The default value to return if the option does not exist
            #// in the database.
            #// @param string $option  Option name.
            #// @param bool   $passed_default Was `get_option()` passed a default value?
            #//
            return apply_filters(str("default_option_") + str(option), default, option, passed_default)
        # end if
        alloptions = wp_load_alloptions()
        if (php_isset(lambda : alloptions[option])):
            value = alloptions[option]
        else:
            value = wp_cache_get(option, "options")
            if False == value:
                row = wpdb.get_row(wpdb.prepare(str("SELECT option_value FROM ") + str(wpdb.options) + str(" WHERE option_name = %s LIMIT 1"), option))
                #// Has to be get_row() instead of get_var() because of funkiness with 0, false, null values.
                if php_is_object(row):
                    value = row.option_value
                    wp_cache_add(option, value, "options")
                else:
                    #// Option does not exist, so we must cache its non-existence.
                    if (not php_is_array(notoptions)):
                        notoptions = Array()
                    # end if
                    notoptions[option] = True
                    wp_cache_set("notoptions", notoptions, "options")
                    #// This filter is documented in wp-includes/option.php
                    return apply_filters(str("default_option_") + str(option), default, option, passed_default)
                # end if
            # end if
        # end if
    else:
        suppress = wpdb.suppress_errors()
        row = wpdb.get_row(wpdb.prepare(str("SELECT option_value FROM ") + str(wpdb.options) + str(" WHERE option_name = %s LIMIT 1"), option))
        wpdb.suppress_errors(suppress)
        if php_is_object(row):
            value = row.option_value
        else:
            #// This filter is documented in wp-includes/option.php
            return apply_filters(str("default_option_") + str(option), default, option, passed_default)
        # end if
    # end if
    #// If home is not set, use siteurl.
    if "home" == option and "" == value:
        return get_option("siteurl")
    # end if
    if php_in_array(option, Array("siteurl", "home", "category_base", "tag_base")):
        value = untrailingslashit(value)
    # end if
    #// 
    #// Filters the value of an existing option.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 1.5.0 As 'option_' . $setting
    #// @since 3.0.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// 
    #// @param mixed  $value  Value of the option. If stored serialized, it will be
    #// unserialized prior to being returned.
    #// @param string $option Option name.
    #//
    return apply_filters(str("option_") + str(option), maybe_unserialize(value), option)
# end def get_option
#// 
#// Protects WordPress special option from being modified.
#// 
#// Will die if $option is in protected list. Protected options are 'alloptions'
#// and 'notoptions' options.
#// 
#// @since 2.2.0
#// 
#// @param string $option Option name.
#//
def wp_protect_special_option(option=None, *args_):
    
    if "alloptions" == option or "notoptions" == option:
        wp_die(php_sprintf(__("%s is a protected WP option and may not be modified"), esc_html(option)))
    # end if
# end def wp_protect_special_option
#// 
#// Prints option value after sanitizing for forms.
#// 
#// @since 1.5.0
#// 
#// @param string $option Option name.
#//
def form_option(option=None, *args_):
    
    php_print(esc_attr(get_option(option)))
# end def form_option
#// 
#// Loads and caches all autoloaded options, if available or all options.
#// 
#// @since 2.2.0
#// @since 5.3.1 The `$force_cache` parameter was added.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param bool $force_cache Optional. Whether to force an update of the local cache
#// from the persistent cache. Default false.
#// @return array List of all options.
#//
def wp_load_alloptions(force_cache=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not wp_installing()) or (not is_multisite()):
        alloptions = wp_cache_get("alloptions", "options", force_cache)
    else:
        alloptions = False
    # end if
    if (not alloptions):
        suppress = wpdb.suppress_errors()
        alloptions_db = wpdb.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb.options) + str(" WHERE autoload = 'yes'"))
        if (not alloptions_db):
            alloptions_db = wpdb.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb.options))
        # end if
        wpdb.suppress_errors(suppress)
        alloptions = Array()
        for o in alloptions_db:
            alloptions[o.option_name] = o.option_value
        # end for
        if (not wp_installing()) or (not is_multisite()):
            #// 
            #// Filters all options before caching them.
            #// 
            #// @since 4.9.0
            #// 
            #// @param array $alloptions Array with all options.
            #//
            alloptions = apply_filters("pre_cache_alloptions", alloptions)
            wp_cache_add("alloptions", alloptions, "options")
        # end if
    # end if
    #// 
    #// Filters all options after retrieving them.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $alloptions Array with all options.
    #//
    return apply_filters("alloptions", alloptions)
# end def wp_load_alloptions
#// 
#// Loads and caches certain often requested site options if is_multisite() and a persistent cache is not being used.
#// 
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $network_id Optional site ID for which to query the options. Defaults to the current site.
#//
def wp_load_core_site_options(network_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not is_multisite()) or wp_using_ext_object_cache() or wp_installing():
        return
    # end if
    if php_empty(lambda : network_id):
        network_id = get_current_network_id()
    # end if
    core_options = Array("site_name", "siteurl", "active_sitewide_plugins", "_site_transient_timeout_theme_roots", "_site_transient_theme_roots", "site_admins", "can_compress_scripts", "global_terms_enabled", "ms_files_rewriting")
    core_options_in = "'" + php_implode("', '", core_options) + "'"
    options = wpdb.get_results(wpdb.prepare(str("SELECT meta_key, meta_value FROM ") + str(wpdb.sitemeta) + str(" WHERE meta_key IN (") + str(core_options_in) + str(") AND site_id = %d"), network_id))
    for option in options:
        key = option.meta_key
        cache_key = str(network_id) + str(":") + str(key)
        option.meta_value = maybe_unserialize(option.meta_value)
        wp_cache_set(cache_key, option.meta_value, "site-options")
    # end for
# end def wp_load_core_site_options
#// 
#// Updates the value of an option that was already added.
#// 
#// You do not need to serialize values. If the value needs to be serialized,
#// then it will be serialized before it is inserted into the database.
#// Remember, resources cannot be serialized or added as an option.
#// 
#// If the option does not exist, it will be created.
#// This function is designed to work with or without a logged-in user. In terms of security,
#// plugin developers should check the current user's capabilities before updating any options.
#// 
#// @since 1.0.0
#// @since 4.2.0 The `$autoload` parameter was added.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string      $option   Option name. Expected to not be SQL-escaped.
#// @param mixed       $value    Option value. Must be serializable if non-scalar. Expected to not be SQL-escaped.
#// @param string|bool $autoload Optional. Whether to load the option when WordPress starts up. For existing options,
#// `$autoload` can only be updated using `update_option()` if `$value` is also changed.
#// Accepts 'yes'|true to enable or 'no'|false to disable. For non-existent options,
#// the default value is 'yes'. Default null.
#// @return bool False if value was not updated and true if value was updated.
#//
def update_option(option=None, value=None, autoload=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    option = php_trim(option)
    if php_empty(lambda : option):
        return False
    # end if
    wp_protect_special_option(option)
    if php_is_object(value):
        value = copy.deepcopy(value)
    # end if
    value = sanitize_option(option, value)
    old_value = get_option(option)
    #// 
    #// Filters a specific option before its value is (maybe) serialized and updated.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 2.6.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// 
    #// @param mixed  $value     The new, unserialized option value.
    #// @param mixed  $old_value The old option value.
    #// @param string $option    Option name.
    #//
    value = apply_filters(str("pre_update_option_") + str(option), value, old_value, option)
    #// 
    #// Filters an option before its value is (maybe) serialized and updated.
    #// 
    #// @since 3.9.0
    #// 
    #// @param mixed  $value     The new, unserialized option value.
    #// @param string $option    Name of the option.
    #// @param mixed  $old_value The old option value.
    #//
    value = apply_filters("pre_update_option", value, option, old_value)
    #// 
    #// If the new and old values are the same, no need to update.
    #// 
    #// Unserialized values will be adequate in most cases. If the unserialized
    #// data differs, the (maybe) serialized data is checked to avoid
    #// unnecessary database calls for otherwise identical object instances.
    #// 
    #// See https://core.trac.wordpress.org/ticket/38903
    #//
    if value == old_value or maybe_serialize(value) == maybe_serialize(old_value):
        return False
    # end if
    #// This filter is documented in wp-includes/option.php
    if apply_filters(str("default_option_") + str(option), False, option, False) == old_value:
        #// Default setting for new options is 'yes'.
        if None == autoload:
            autoload = "yes"
        # end if
        return add_option(option, value, "", autoload)
    # end if
    serialized_value = maybe_serialize(value)
    #// 
    #// Fires immediately before an option value is updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option    Name of the option to update.
    #// @param mixed  $old_value The old option value.
    #// @param mixed  $value     The new option value.
    #//
    do_action("update_option", option, old_value, value)
    update_args = Array({"option_value": serialized_value})
    if None != autoload:
        update_args["autoload"] = "no" if "no" == autoload or False == autoload else "yes"
    # end if
    result = wpdb.update(wpdb.options, update_args, Array({"option_name": option}))
    if (not result):
        return False
    # end if
    notoptions = wp_cache_get("notoptions", "options")
    if php_is_array(notoptions) and (php_isset(lambda : notoptions[option])):
        notoptions[option] = None
        wp_cache_set("notoptions", notoptions, "options")
    # end if
    if (not wp_installing()):
        alloptions = wp_load_alloptions(True)
        if (php_isset(lambda : alloptions[option])):
            alloptions[option] = serialized_value
            wp_cache_set("alloptions", alloptions, "options")
        else:
            wp_cache_set(option, serialized_value, "options")
        # end if
    # end if
    #// 
    #// Fires after the value of a specific option has been successfully updated.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 2.0.1
    #// @since 4.4.0 The `$option` parameter was added.
    #// 
    #// @param mixed  $old_value The old option value.
    #// @param mixed  $value     The new option value.
    #// @param string $option    Option name.
    #//
    do_action(str("update_option_") + str(option), old_value, value, option)
    #// 
    #// Fires after the value of an option has been successfully updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option    Name of the updated option.
    #// @param mixed  $old_value The old option value.
    #// @param mixed  $value     The new option value.
    #//
    do_action("updated_option", option, old_value, value)
    return True
# end def update_option
#// 
#// Adds a new option.
#// 
#// You do not need to serialize values. If the value needs to be serialized,
#// then it will be serialized before it is inserted into the database.
#// Remember, resources cannot be serialized or added as an option.
#// 
#// You can create options without values and then update the values later.
#// Existing options will not be updated and checks are performed to ensure that you
#// aren't adding a protected WordPress option. Care should be taken to not name
#// options the same as the ones which are protected.
#// 
#// @since 1.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string         $option      Name of option to add. Expected to not be SQL-escaped.
#// @param mixed          $value       Optional. Option value. Must be serializable if non-scalar. Expected to not be SQL-escaped.
#// @param string         $deprecated  Optional. Description. Not used anymore.
#// @param string|bool    $autoload    Optional. Whether to load the option when WordPress starts up.
#// Default is enabled. Accepts 'no' to disable for legacy reasons.
#// @return bool False if option was not added and true if option was added.
#//
def add_option(option=None, value="", deprecated="", autoload="yes", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.3.0")
    # end if
    option = php_trim(option)
    if php_empty(lambda : option):
        return False
    # end if
    wp_protect_special_option(option)
    if php_is_object(value):
        value = copy.deepcopy(value)
    # end if
    value = sanitize_option(option, value)
    #// Make sure the option doesn't already exist.
    #// We can check the 'notoptions' cache before we ask for a DB query.
    notoptions = wp_cache_get("notoptions", "options")
    if (not php_is_array(notoptions)) or (not (php_isset(lambda : notoptions[option]))):
        #// This filter is documented in wp-includes/option.php
        if apply_filters(str("default_option_") + str(option), False, option, False) != get_option(option):
            return False
        # end if
    # end if
    serialized_value = maybe_serialize(value)
    autoload = "no" if "no" == autoload or False == autoload else "yes"
    #// 
    #// Fires before an option is added.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option Name of the option to add.
    #// @param mixed  $value  Value of the option.
    #//
    do_action("add_option", option, value)
    result = wpdb.query(wpdb.prepare(str("INSERT INTO `") + str(wpdb.options) + str("` (`option_name`, `option_value`, `autoload`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `option_name` = VALUES(`option_name`), `option_value` = VALUES(`option_value`), `autoload` = VALUES(`autoload`)"), option, serialized_value, autoload))
    if (not result):
        return False
    # end if
    if (not wp_installing()):
        if "yes" == autoload:
            alloptions = wp_load_alloptions(True)
            alloptions[option] = serialized_value
            wp_cache_set("alloptions", alloptions, "options")
        else:
            wp_cache_set(option, serialized_value, "options")
        # end if
    # end if
    #// This option exists now.
    notoptions = wp_cache_get("notoptions", "options")
    #// Yes, again... we need it to be fresh.
    if php_is_array(notoptions) and (php_isset(lambda : notoptions[option])):
        notoptions[option] = None
        wp_cache_set("notoptions", notoptions, "options")
    # end if
    #// 
    #// Fires after a specific option has been added.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 2.5.0 As "add_option_{$name}"
    #// @since 3.0.0
    #// 
    #// @param string $option Name of the option to add.
    #// @param mixed  $value  Value of the option.
    #//
    do_action(str("add_option_") + str(option), option, value)
    #// 
    #// Fires after an option has been added.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option Name of the added option.
    #// @param mixed  $value  Value of the option.
    #//
    do_action("added_option", option, value)
    return True
# end def add_option
#// 
#// Removes option by name. Prevents removal of protected WordPress options.
#// 
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $option Name of option to remove. Expected to not be SQL-escaped.
#// @return bool True, if option is successfully deleted. False on failure.
#//
def delete_option(option=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    option = php_trim(option)
    if php_empty(lambda : option):
        return False
    # end if
    wp_protect_special_option(option)
    #// Get the ID, if no ID then return.
    row = wpdb.get_row(wpdb.prepare(str("SELECT autoload FROM ") + str(wpdb.options) + str(" WHERE option_name = %s"), option))
    if is_null(row):
        return False
    # end if
    #// 
    #// Fires immediately before an option is deleted.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option Name of the option to delete.
    #//
    do_action("delete_option", option)
    result = wpdb.delete(wpdb.options, Array({"option_name": option}))
    if (not wp_installing()):
        if "yes" == row.autoload:
            alloptions = wp_load_alloptions(True)
            if php_is_array(alloptions) and (php_isset(lambda : alloptions[option])):
                alloptions[option] = None
                wp_cache_set("alloptions", alloptions, "options")
            # end if
        else:
            wp_cache_delete(option, "options")
        # end if
    # end if
    if result:
        #// 
        #// Fires after a specific option has been deleted.
        #// 
        #// The dynamic portion of the hook name, `$option`, refers to the option name.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $option Name of the deleted option.
        #//
        do_action(str("delete_option_") + str(option), option)
        #// 
        #// Fires after an option has been deleted.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string $option Name of the deleted option.
        #//
        do_action("deleted_option", option)
        return True
    # end if
    return False
# end def delete_option
#// 
#// Deletes a transient.
#// 
#// @since 2.8.0
#// 
#// @param string $transient Transient name. Expected to not be SQL-escaped.
#// @return bool true if successful, false otherwise
#//
def delete_transient(transient=None, *args_):
    
    #// 
    #// Fires immediately before a specific transient is deleted.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $transient Transient name.
    #//
    do_action(str("delete_transient_") + str(transient), transient)
    if wp_using_ext_object_cache():
        result = wp_cache_delete(transient, "transient")
    else:
        option_timeout = "_transient_timeout_" + transient
        option = "_transient_" + transient
        result = delete_option(option)
        if result:
            delete_option(option_timeout)
        # end if
    # end if
    if result:
        #// 
        #// Fires after a transient is deleted.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $transient Deleted transient name.
        #//
        do_action("deleted_transient", transient)
    # end if
    return result
# end def delete_transient
#// 
#// Retrieves the value of a transient.
#// 
#// If the transient does not exist, does not have a value, or has expired,
#// then the return value will be false.
#// 
#// @since 2.8.0
#// 
#// @param string $transient Transient name. Expected to not be SQL-escaped.
#// @return mixed Value of transient.
#//
def get_transient(transient=None, *args_):
    
    #// 
    #// Filters the value of an existing transient.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// Passing a truthy value to the filter will effectively short-circuit retrieval
    #// of the transient, returning the passed value instead.
    #// 
    #// @since 2.8.0
    #// @since 4.4.0 The `$transient` parameter was added
    #// 
    #// @param mixed  $pre_transient The default value to return if the transient does not exist.
    #// Any value other than false will short-circuit the retrieval
    #// of the transient, and return the returned value.
    #// @param string $transient     Transient name.
    #//
    pre = apply_filters(str("pre_transient_") + str(transient), False, transient)
    if False != pre:
        return pre
    # end if
    if wp_using_ext_object_cache():
        value = wp_cache_get(transient, "transient")
    else:
        transient_option = "_transient_" + transient
        if (not wp_installing()):
            #// If option is not in alloptions, it is not autoloaded and thus has a timeout.
            alloptions = wp_load_alloptions()
            if (not (php_isset(lambda : alloptions[transient_option]))):
                transient_timeout = "_transient_timeout_" + transient
                timeout = get_option(transient_timeout)
                if False != timeout and timeout < time():
                    delete_option(transient_option)
                    delete_option(transient_timeout)
                    value = False
                # end if
            # end if
        # end if
        if (not (php_isset(lambda : value))):
            value = get_option(transient_option)
        # end if
    # end if
    #// 
    #// Filters an existing transient's value.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 2.8.0
    #// @since 4.4.0 The `$transient` parameter was added
    #// 
    #// @param mixed  $value     Value of transient.
    #// @param string $transient Transient name.
    #//
    return apply_filters(str("transient_") + str(transient), value, transient)
# end def get_transient
#// 
#// Sets/updates the value of a transient.
#// 
#// You do not need to serialize values. If the value needs to be serialized,
#// then it will be serialized before it is set.
#// 
#// @since 2.8.0
#// 
#// @param string $transient  Transient name. Expected to not be SQL-escaped. Must be
#// 172 characters or fewer in length.
#// @param mixed  $value      Transient value. Must be serializable if non-scalar.
#// Expected to not be SQL-escaped.
#// @param int    $expiration Optional. Time until expiration in seconds. Default 0 (no expiration).
#// @return bool False if value was not set and true if value was set.
#//
def set_transient(transient=None, value=None, expiration=0, *args_):
    
    expiration = php_int(expiration)
    #// 
    #// Filters a specific transient before its value is set.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 3.0.0
    #// @since 4.2.0 The `$expiration` parameter was added.
    #// @since 4.4.0 The `$transient` parameter was added.
    #// 
    #// @param mixed  $value      New value of transient.
    #// @param int    $expiration Time until expiration in seconds.
    #// @param string $transient  Transient name.
    #//
    value = apply_filters(str("pre_set_transient_") + str(transient), value, expiration, transient)
    #// 
    #// Filters the expiration for a transient before its value is set.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int    $expiration Time until expiration in seconds. Use 0 for no expiration.
    #// @param mixed  $value      New value of transient.
    #// @param string $transient  Transient name.
    #//
    expiration = apply_filters(str("expiration_of_transient_") + str(transient), expiration, value, transient)
    if wp_using_ext_object_cache():
        result = wp_cache_set(transient, value, "transient", expiration)
    else:
        transient_timeout = "_transient_timeout_" + transient
        transient_option = "_transient_" + transient
        if False == get_option(transient_option):
            autoload = "yes"
            if expiration:
                autoload = "no"
                add_option(transient_timeout, time() + expiration, "", "no")
            # end if
            result = add_option(transient_option, value, "", autoload)
        else:
            #// If expiration is requested, but the transient has no timeout option,
            #// delete, then re-create transient rather than update.
            update = True
            if expiration:
                if False == get_option(transient_timeout):
                    delete_option(transient_option)
                    add_option(transient_timeout, time() + expiration, "", "no")
                    result = add_option(transient_option, value, "", "no")
                    update = False
                else:
                    update_option(transient_timeout, time() + expiration)
                # end if
            # end if
            if update:
                result = update_option(transient_option, value)
            # end if
        # end if
    # end if
    if result:
        #// 
        #// Fires after the value for a specific transient has been set.
        #// 
        #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
        #// 
        #// @since 3.0.0
        #// @since 3.6.0 The `$value` and `$expiration` parameters were added.
        #// @since 4.4.0 The `$transient` parameter was added.
        #// 
        #// @param mixed  $value      Transient value.
        #// @param int    $expiration Time until expiration in seconds.
        #// @param string $transient  The name of the transient.
        #//
        do_action(str("set_transient_") + str(transient), value, expiration, transient)
        #// 
        #// Fires after the value for a transient has been set.
        #// 
        #// @since 3.0.0
        #// @since 3.6.0 The `$value` and `$expiration` parameters were added.
        #// 
        #// @param string $transient  The name of the transient.
        #// @param mixed  $value      Transient value.
        #// @param int    $expiration Time until expiration in seconds.
        #//
        do_action("setted_transient", transient, value, expiration)
    # end if
    return result
# end def set_transient
#// 
#// Deletes all expired transients.
#// 
#// The multi-table delete syntax is used to delete the transient record
#// from table a, and the corresponding transient_timeout record from table b.
#// 
#// @since 4.9.0
#// 
#// @param bool $force_db Optional. Force cleanup to run against the database even when an external object cache is used.
#//
def delete_expired_transients(force_db=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not force_db) and wp_using_ext_object_cache():
        return
    # end if
    wpdb.query(wpdb.prepare(str("DELETE a, b FROM ") + str(wpdb.options) + str(" a, ") + str(wpdb.options) + str(""" b\n            WHERE a.option_name LIKE %s\n           AND a.option_name NOT LIKE %s\n         AND b.option_name = CONCAT( '_transient_timeout_', SUBSTRING( a.option_name, 12 ) )\n           AND b.option_value < %d"""), wpdb.esc_like("_transient_") + "%", wpdb.esc_like("_transient_timeout_") + "%", time()))
    if (not is_multisite()):
        #// Single site stores site transients in the options table.
        wpdb.query(wpdb.prepare(str("DELETE a, b FROM ") + str(wpdb.options) + str(" a, ") + str(wpdb.options) + str(""" b\n                WHERE a.option_name LIKE %s\n               AND a.option_name NOT LIKE %s\n             AND b.option_name = CONCAT( '_site_transient_timeout_', SUBSTRING( a.option_name, 17 ) )\n              AND b.option_value < %d"""), wpdb.esc_like("_site_transient_") + "%", wpdb.esc_like("_site_transient_timeout_") + "%", time()))
    elif is_multisite() and is_main_site() and is_main_network():
        #// Multisite stores site transients in the sitemeta table.
        wpdb.query(wpdb.prepare(str("DELETE a, b FROM ") + str(wpdb.sitemeta) + str(" a, ") + str(wpdb.sitemeta) + str(""" b\n              WHERE a.meta_key LIKE %s\n              AND a.meta_key NOT LIKE %s\n                AND b.meta_key = CONCAT( '_site_transient_timeout_', SUBSTRING( a.meta_key, 17 ) )\n                AND b.meta_value < %d"""), wpdb.esc_like("_site_transient_") + "%", wpdb.esc_like("_site_transient_timeout_") + "%", time()))
    # end if
# end def delete_expired_transients
#// 
#// Saves and restores user interface settings stored in a cookie.
#// 
#// Checks if the current user-settings cookie is updated and stores it. When no
#// cookie exists (different browser used), adds the last saved cookie restoring
#// the settings.
#// 
#// @since 2.7.0
#//
def wp_user_settings(*args_):
    global PHP_COOKIE
    if (not is_admin()) or wp_doing_ajax():
        return
    # end if
    user_id = get_current_user_id()
    if (not user_id):
        return
    # end if
    if (not is_user_member_of_blog()):
        return
    # end if
    settings = php_str(get_user_option("user-settings", user_id))
    if (php_isset(lambda : PHP_COOKIE["wp-settings-" + user_id])):
        cookie = php_preg_replace("/[^A-Za-z0-9=&_]/", "", PHP_COOKIE["wp-settings-" + user_id])
        #// No change or both empty.
        if cookie == settings:
            return
        # end if
        last_saved = php_int(get_user_option("user-settings-time", user_id))
        current = php_preg_replace("/[^0-9]/", "", PHP_COOKIE["wp-settings-time-" + user_id]) if (php_isset(lambda : PHP_COOKIE["wp-settings-time-" + user_id])) else 0
        #// The cookie is newer than the saved value. Update the user_option and leave the cookie as-is.
        if current > last_saved:
            update_user_option(user_id, "user-settings", cookie, False)
            update_user_option(user_id, "user-settings-time", time() - 5, False)
            return
        # end if
    # end if
    #// The cookie is not set in the current browser or the saved value is newer.
    secure = "https" == php_parse_url(admin_url(), PHP_URL_SCHEME)
    setcookie("wp-settings-" + user_id, settings, time() + YEAR_IN_SECONDS, SITECOOKIEPATH, None, secure)
    setcookie("wp-settings-time-" + user_id, time(), time() + YEAR_IN_SECONDS, SITECOOKIEPATH, None, secure)
    PHP_COOKIE["wp-settings-" + user_id] = settings
# end def wp_user_settings
#// 
#// Retrieves user interface setting value based on setting name.
#// 
#// @since 2.7.0
#// 
#// @param string $name    The name of the setting.
#// @param string $default Optional default value to return when $name is not set.
#// @return mixed the last saved user setting or the default value/false if it doesn't exist.
#//
def get_user_setting(name=None, default=False, *args_):
    
    all_user_settings = get_all_user_settings()
    return all_user_settings[name] if (php_isset(lambda : all_user_settings[name])) else default
# end def get_user_setting
#// 
#// Adds or updates user interface setting.
#// 
#// Both $name and $value can contain only ASCII letters, numbers, hyphens, and underscores.
#// 
#// This function has to be used before any output has started as it calls setcookie().
#// 
#// @since 2.8.0
#// 
#// @param string $name  The name of the setting.
#// @param string $value The value for the setting.
#// @return bool|null True if set successfully, false if not. Null if the current user can't be established.
#//
def set_user_setting(name=None, value=None, *args_):
    
    if php_headers_sent():
        return False
    # end if
    all_user_settings = get_all_user_settings()
    all_user_settings[name] = value
    return wp_set_all_user_settings(all_user_settings)
# end def set_user_setting
#// 
#// Deletes user interface settings.
#// 
#// Deleting settings would reset them to the defaults.
#// 
#// This function has to be used before any output has started as it calls setcookie().
#// 
#// @since 2.7.0
#// 
#// @param string $names The name or array of names of the setting to be deleted.
#// @return bool|null True if deleted successfully, false if not. Null if the current user can't be established.
#//
def delete_user_setting(names=None, *args_):
    
    if php_headers_sent():
        return False
    # end if
    all_user_settings = get_all_user_settings()
    names = names
    deleted = False
    for name in names:
        if (php_isset(lambda : all_user_settings[name])):
            all_user_settings[name] = None
            deleted = True
        # end if
    # end for
    if deleted:
        return wp_set_all_user_settings(all_user_settings)
    # end if
    return False
# end def delete_user_setting
#// 
#// Retrieves all user interface settings.
#// 
#// @since 2.7.0
#// 
#// @global array $_updated_user_settings
#// 
#// @return array the last saved user settings or empty array.
#//
def get_all_user_settings(*args_):
    
    global _updated_user_settings
    php_check_if_defined("_updated_user_settings")
    user_id = get_current_user_id()
    if (not user_id):
        return Array()
    # end if
    if (php_isset(lambda : _updated_user_settings)) and php_is_array(_updated_user_settings):
        return _updated_user_settings
    # end if
    user_settings = Array()
    if (php_isset(lambda : PHP_COOKIE["wp-settings-" + user_id])):
        cookie = php_preg_replace("/[^A-Za-z0-9=&_-]/", "", PHP_COOKIE["wp-settings-" + user_id])
        if php_strpos(cookie, "="):
            #// '=' cannot be 1st char.
            parse_str(cookie, user_settings)
        # end if
    else:
        option = get_user_option("user-settings", user_id)
        if option and php_is_string(option):
            parse_str(option, user_settings)
        # end if
    # end if
    _updated_user_settings = user_settings
    return user_settings
# end def get_all_user_settings
#// 
#// Private. Sets all user interface settings.
#// 
#// @since 2.8.0
#// @access private
#// 
#// @global array $_updated_user_settings
#// 
#// @param array $user_settings User settings.
#// @return bool|null False if the current user can't be found, null if the current
#// user is not a super admin or a member of the site, otherwise true.
#//
def wp_set_all_user_settings(user_settings=None, *args_):
    
    global _updated_user_settings
    php_check_if_defined("_updated_user_settings")
    user_id = get_current_user_id()
    if (not user_id):
        return False
    # end if
    if (not is_user_member_of_blog()):
        return
    # end if
    settings = ""
    for name,value in user_settings:
        _name = php_preg_replace("/[^A-Za-z0-9_-]+/", "", name)
        _value = php_preg_replace("/[^A-Za-z0-9_-]+/", "", value)
        if (not php_empty(lambda : _name)):
            settings += _name + "=" + _value + "&"
        # end if
    # end for
    settings = php_rtrim(settings, "&")
    parse_str(settings, _updated_user_settings)
    update_user_option(user_id, "user-settings", settings, False)
    update_user_option(user_id, "user-settings-time", time(), False)
    return True
# end def wp_set_all_user_settings
#// 
#// Deletes the user settings of the current user.
#// 
#// @since 2.7.0
#//
def delete_all_user_settings(*args_):
    
    user_id = get_current_user_id()
    if (not user_id):
        return
    # end if
    update_user_option(user_id, "user-settings", "", False)
    setcookie("wp-settings-" + user_id, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH)
# end def delete_all_user_settings
#// 
#// Retrieve an option value for the current network based on name of option.
#// 
#// @since 2.8.0
#// @since 4.4.0 The `$use_cache` parameter was deprecated.
#// @since 4.4.0 Modified into wrapper for get_network_option()
#// 
#// @see get_network_option()
#// 
#// @param string $option     Name of option to retrieve. Expected to not be SQL-escaped.
#// @param mixed  $default    Optional value to return if option doesn't exist. Default false.
#// @param bool   $deprecated Whether to use cache. Multisite only. Always set to true.
#// @return mixed Value set for the option.
#//
def get_site_option(option=None, default=False, deprecated=True, *args_):
    
    return get_network_option(None, option, default)
# end def get_site_option
#// 
#// Adds a new option for the current network.
#// 
#// Existing options will not be updated. Note that prior to 3.3 this wasn't the case.
#// 
#// @since 2.8.0
#// @since 4.4.0 Modified into wrapper for add_network_option()
#// 
#// @see add_network_option()
#// 
#// @param string $option Name of option to add. Expected to not be SQL-escaped.
#// @param mixed  $value  Option value, can be anything. Expected to not be SQL-escaped.
#// @return bool False if the option was not added. True if the option was added.
#//
def add_site_option(option=None, value=None, *args_):
    
    return add_network_option(None, option, value)
# end def add_site_option
#// 
#// Removes a option by name for the current network.
#// 
#// @since 2.8.0
#// @since 4.4.0 Modified into wrapper for delete_network_option()
#// 
#// @see delete_network_option()
#// 
#// @param string $option Name of option to remove. Expected to not be SQL-escaped.
#// @return bool True, if succeed. False, if failure.
#//
def delete_site_option(option=None, *args_):
    
    return delete_network_option(None, option)
# end def delete_site_option
#// 
#// Updates the value of an option that was already added for the current network.
#// 
#// @since 2.8.0
#// @since 4.4.0 Modified into wrapper for update_network_option()
#// 
#// @see update_network_option()
#// 
#// @param string $option Name of option. Expected to not be SQL-escaped.
#// @param mixed  $value  Option value. Expected to not be SQL-escaped.
#// @return bool False if value was not updated. True if value was updated.
#//
def update_site_option(option=None, value=None, *args_):
    
    return update_network_option(None, option, value)
# end def update_site_option
#// 
#// Retrieves a network's option value based on the option name.
#// 
#// @since 4.4.0
#// 
#// @see get_option()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int      $network_id ID of the network. Can be null to default to the current network ID.
#// @param string   $option     Name of option to retrieve. Expected to not be SQL-escaped.
#// @param mixed    $default    Optional. Value to return if the option doesn't exist. Default false.
#// @return mixed Value set for the option.
#//
def get_network_option(network_id=None, option=None, default=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if network_id and (not php_is_numeric(network_id)):
        return False
    # end if
    network_id = php_int(network_id)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id):
        network_id = get_current_network_id()
    # end if
    #// 
    #// Filters an existing network option before it is retrieved.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// Passing a truthy value to the filter will effectively short-circuit retrieval,
    #// returning the passed value instead.
    #// 
    #// @since 2.9.0 As 'pre_site_option_' . $key
    #// @since 3.0.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// @since 4.7.0 The `$network_id` parameter was added.
    #// @since 4.9.0 The `$default` parameter was added.
    #// 
    #// @param mixed  $pre_option The value to return instead of the option value. This differs from
    #// `$default`, which is used as the fallback value in the event the
    #// option doesn't exist elsewhere in get_network_option(). Default
    #// is false (to skip past the short-circuit).
    #// @param string $option     Option name.
    #// @param int    $network_id ID of the network.
    #// @param mixed  $default    The fallback value to return if the option does not exist.
    #// Default is false.
    #//
    pre = apply_filters(str("pre_site_option_") + str(option), False, option, network_id, default)
    if False != pre:
        return pre
    # end if
    #// Prevent non-existent options from triggering multiple queries.
    notoptions_key = str(network_id) + str(":notoptions")
    notoptions = wp_cache_get(notoptions_key, "site-options")
    if php_is_array(notoptions) and (php_isset(lambda : notoptions[option])):
        #// 
        #// Filters a specific default network option.
        #// 
        #// The dynamic portion of the hook name, `$option`, refers to the option name.
        #// 
        #// @since 3.4.0
        #// @since 4.4.0 The `$option` parameter was added.
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param mixed  $default    The value to return if the site option does not exist
        #// in the database.
        #// @param string $option     Option name.
        #// @param int    $network_id ID of the network.
        #//
        return apply_filters(str("default_site_option_") + str(option), default, option, network_id)
    # end if
    if (not is_multisite()):
        #// This filter is documented in wp-includes/option.php
        default = apply_filters("default_site_option_" + option, default, option, network_id)
        value = get_option(option, default)
    else:
        cache_key = str(network_id) + str(":") + str(option)
        value = wp_cache_get(cache_key, "site-options")
        if (not (php_isset(lambda : value))) or False == value:
            row = wpdb.get_row(wpdb.prepare(str("SELECT meta_value FROM ") + str(wpdb.sitemeta) + str(" WHERE meta_key = %s AND site_id = %d"), option, network_id))
            #// Has to be get_row() instead of get_var() because of funkiness with 0, false, null values.
            if php_is_object(row):
                value = row.meta_value
                value = maybe_unserialize(value)
                wp_cache_set(cache_key, value, "site-options")
            else:
                if (not php_is_array(notoptions)):
                    notoptions = Array()
                # end if
                notoptions[option] = True
                wp_cache_set(notoptions_key, notoptions, "site-options")
                #// This filter is documented in wp-includes/option.php
                value = apply_filters("default_site_option_" + option, default, option, network_id)
            # end if
        # end if
    # end if
    if (not php_is_array(notoptions)):
        notoptions = Array()
        wp_cache_set(notoptions_key, notoptions, "site-options")
    # end if
    #// 
    #// Filters the value of an existing network option.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 2.9.0 As 'site_option_' . $key
    #// @since 3.0.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// @since 4.7.0 The `$network_id` parameter was added.
    #// 
    #// @param mixed  $value      Value of network option.
    #// @param string $option     Option name.
    #// @param int    $network_id ID of the network.
    #//
    return apply_filters(str("site_option_") + str(option), value, option, network_id)
# end def get_network_option
#// 
#// Adds a new network option.
#// 
#// Existing options will not be updated.
#// 
#// @since 4.4.0
#// 
#// @see add_option()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $network_id ID of the network. Can be null to default to the current network ID.
#// @param string $option     Name of option to add. Expected to not be SQL-escaped.
#// @param mixed  $value      Option value, can be anything. Expected to not be SQL-escaped.
#// @return bool False if option was not added and true if option was added.
#//
def add_network_option(network_id=None, option=None, value=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if network_id and (not php_is_numeric(network_id)):
        return False
    # end if
    network_id = php_int(network_id)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id):
        network_id = get_current_network_id()
    # end if
    wp_protect_special_option(option)
    #// 
    #// Filters the value of a specific network option before it is added.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 2.9.0 As 'pre_add_site_option_' . $key
    #// @since 3.0.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// @since 4.7.0 The `$network_id` parameter was added.
    #// 
    #// @param mixed  $value      Value of network option.
    #// @param string $option     Option name.
    #// @param int    $network_id ID of the network.
    #//
    value = apply_filters(str("pre_add_site_option_") + str(option), value, option, network_id)
    notoptions_key = str(network_id) + str(":notoptions")
    if (not is_multisite()):
        result = add_option(option, value, "", "no")
    else:
        cache_key = str(network_id) + str(":") + str(option)
        #// Make sure the option doesn't already exist.
        #// We can check the 'notoptions' cache before we ask for a DB query.
        notoptions = wp_cache_get(notoptions_key, "site-options")
        if (not php_is_array(notoptions)) or (not (php_isset(lambda : notoptions[option]))):
            if False != get_network_option(network_id, option, False):
                return False
            # end if
        # end if
        value = sanitize_option(option, value)
        serialized_value = maybe_serialize(value)
        result = wpdb.insert(wpdb.sitemeta, Array({"site_id": network_id, "meta_key": option, "meta_value": serialized_value}))
        if (not result):
            return False
        # end if
        wp_cache_set(cache_key, value, "site-options")
        #// This option exists now.
        notoptions = wp_cache_get(notoptions_key, "site-options")
        #// Yes, again... we need it to be fresh.
        if php_is_array(notoptions) and (php_isset(lambda : notoptions[option])):
            notoptions[option] = None
            wp_cache_set(notoptions_key, notoptions, "site-options")
        # end if
    # end if
    if result:
        #// 
        #// Fires after a specific network option has been successfully added.
        #// 
        #// The dynamic portion of the hook name, `$option`, refers to the option name.
        #// 
        #// @since 2.9.0 As "add_site_option_{$key}"
        #// @since 3.0.0
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param string $option     Name of the network option.
        #// @param mixed  $value      Value of the network option.
        #// @param int    $network_id ID of the network.
        #//
        do_action(str("add_site_option_") + str(option), option, value, network_id)
        #// 
        #// Fires after a network option has been successfully added.
        #// 
        #// @since 3.0.0
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param string $option     Name of the network option.
        #// @param mixed  $value      Value of the network option.
        #// @param int    $network_id ID of the network.
        #//
        do_action("add_site_option", option, value, network_id)
        return True
    # end if
    return False
# end def add_network_option
#// 
#// Removes a network option by name.
#// 
#// @since 4.4.0
#// 
#// @see delete_option()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $network_id ID of the network. Can be null to default to the current network ID.
#// @param string $option     Name of option to remove. Expected to not be SQL-escaped.
#// @return bool True, if succeed. False, if failure.
#//
def delete_network_option(network_id=None, option=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if network_id and (not php_is_numeric(network_id)):
        return False
    # end if
    network_id = php_int(network_id)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id):
        network_id = get_current_network_id()
    # end if
    #// 
    #// Fires immediately before a specific network option is deleted.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 3.0.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// @since 4.7.0 The `$network_id` parameter was added.
    #// 
    #// @param string $option     Option name.
    #// @param int    $network_id ID of the network.
    #//
    do_action(str("pre_delete_site_option_") + str(option), option, network_id)
    if (not is_multisite()):
        result = delete_option(option)
    else:
        row = wpdb.get_row(wpdb.prepare(str("SELECT meta_id FROM ") + str(wpdb.sitemeta) + str(" WHERE meta_key = %s AND site_id = %d"), option, network_id))
        if is_null(row) or (not row.meta_id):
            return False
        # end if
        cache_key = str(network_id) + str(":") + str(option)
        wp_cache_delete(cache_key, "site-options")
        result = wpdb.delete(wpdb.sitemeta, Array({"meta_key": option, "site_id": network_id}))
    # end if
    if result:
        #// 
        #// Fires after a specific network option has been deleted.
        #// 
        #// The dynamic portion of the hook name, `$option`, refers to the option name.
        #// 
        #// @since 2.9.0 As "delete_site_option_{$key}"
        #// @since 3.0.0
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param string $option     Name of the network option.
        #// @param int    $network_id ID of the network.
        #//
        do_action(str("delete_site_option_") + str(option), option, network_id)
        #// 
        #// Fires after a network option has been deleted.
        #// 
        #// @since 3.0.0
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param string $option     Name of the network option.
        #// @param int    $network_id ID of the network.
        #//
        do_action("delete_site_option", option, network_id)
        return True
    # end if
    return False
# end def delete_network_option
#// 
#// Updates the value of a network option that was already added.
#// 
#// @since 4.4.0
#// 
#// @see update_option()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int      $network_id ID of the network. Can be null to default to the current network ID.
#// @param string   $option     Name of option. Expected to not be SQL-escaped.
#// @param mixed    $value      Option value. Expected to not be SQL-escaped.
#// @return bool False if value was not updated and true if value was updated.
#//
def update_network_option(network_id=None, option=None, value=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if network_id and (not php_is_numeric(network_id)):
        return False
    # end if
    network_id = php_int(network_id)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id):
        network_id = get_current_network_id()
    # end if
    wp_protect_special_option(option)
    old_value = get_network_option(network_id, option, False)
    #// 
    #// Filters a specific network option before its value is updated.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the option name.
    #// 
    #// @since 2.9.0 As 'pre_update_site_option_' . $key
    #// @since 3.0.0
    #// @since 4.4.0 The `$option` parameter was added.
    #// @since 4.7.0 The `$network_id` parameter was added.
    #// 
    #// @param mixed  $value      New value of the network option.
    #// @param mixed  $old_value  Old value of the network option.
    #// @param string $option     Option name.
    #// @param int    $network_id ID of the network.
    #//
    value = apply_filters(str("pre_update_site_option_") + str(option), value, old_value, option, network_id)
    #// 
    #// If the new and old values are the same, no need to update.
    #// 
    #// Unserialized values will be adequate in most cases. If the unserialized
    #// data differs, the (maybe) serialized data is checked to avoid
    #// unnecessary database calls for otherwise identical object instances.
    #// 
    #// See https://core.trac.wordpress.org/ticket/44956
    #//
    if value == old_value or maybe_serialize(value) == maybe_serialize(old_value):
        return False
    # end if
    if False == old_value:
        return add_network_option(network_id, option, value)
    # end if
    notoptions_key = str(network_id) + str(":notoptions")
    notoptions = wp_cache_get(notoptions_key, "site-options")
    if php_is_array(notoptions) and (php_isset(lambda : notoptions[option])):
        notoptions[option] = None
        wp_cache_set(notoptions_key, notoptions, "site-options")
    # end if
    if (not is_multisite()):
        result = update_option(option, value, "no")
    else:
        value = sanitize_option(option, value)
        serialized_value = maybe_serialize(value)
        result = wpdb.update(wpdb.sitemeta, Array({"meta_value": serialized_value}), Array({"site_id": network_id, "meta_key": option}))
        if result:
            cache_key = str(network_id) + str(":") + str(option)
            wp_cache_set(cache_key, value, "site-options")
        # end if
    # end if
    if result:
        #// 
        #// Fires after the value of a specific network option has been successfully updated.
        #// 
        #// The dynamic portion of the hook name, `$option`, refers to the option name.
        #// 
        #// @since 2.9.0 As "update_site_option_{$key}"
        #// @since 3.0.0
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param string $option     Name of the network option.
        #// @param mixed  $value      Current value of the network option.
        #// @param mixed  $old_value  Old value of the network option.
        #// @param int    $network_id ID of the network.
        #//
        do_action(str("update_site_option_") + str(option), option, value, old_value, network_id)
        #// 
        #// Fires after the value of a network option has been successfully updated.
        #// 
        #// @since 3.0.0
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param string $option     Name of the network option.
        #// @param mixed  $value      Current value of the network option.
        #// @param mixed  $old_value  Old value of the network option.
        #// @param int    $network_id ID of the network.
        #//
        do_action("update_site_option", option, value, old_value, network_id)
        return True
    # end if
    return False
# end def update_network_option
#// 
#// Deletes a site transient.
#// 
#// @since 2.9.0
#// 
#// @param string $transient Transient name. Expected to not be SQL-escaped.
#// @return bool True if successful, false otherwise
#//
def delete_site_transient(transient=None, *args_):
    
    #// 
    #// Fires immediately before a specific site transient is deleted.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $transient Transient name.
    #//
    do_action(str("delete_site_transient_") + str(transient), transient)
    if wp_using_ext_object_cache():
        result = wp_cache_delete(transient, "site-transient")
    else:
        option_timeout = "_site_transient_timeout_" + transient
        option = "_site_transient_" + transient
        result = delete_site_option(option)
        if result:
            delete_site_option(option_timeout)
        # end if
    # end if
    if result:
        #// 
        #// Fires after a transient is deleted.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $transient Deleted transient name.
        #//
        do_action("deleted_site_transient", transient)
    # end if
    return result
# end def delete_site_transient
#// 
#// Retrieves the value of a site transient.
#// 
#// If the transient does not exist, does not have a value, or has expired,
#// then the return value will be false.
#// 
#// @since 2.9.0
#// 
#// @see get_transient()
#// 
#// @param string $transient Transient name. Expected to not be SQL-escaped.
#// @return mixed Value of transient.
#//
def get_site_transient(transient=None, *args_):
    
    #// 
    #// Filters the value of an existing site transient.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// Passing a truthy value to the filter will effectively short-circuit retrieval,
    #// returning the passed value instead.
    #// 
    #// @since 2.9.0
    #// @since 4.4.0 The `$transient` parameter was added.
    #// 
    #// @param mixed  $pre_site_transient The default value to return if the site transient does not exist.
    #// Any value other than false will short-circuit the retrieval
    #// of the transient, and return the returned value.
    #// @param string $transient          Transient name.
    #//
    pre = apply_filters(str("pre_site_transient_") + str(transient), False, transient)
    if False != pre:
        return pre
    # end if
    if wp_using_ext_object_cache():
        value = wp_cache_get(transient, "site-transient")
    else:
        #// Core transients that do not have a timeout. Listed here so querying timeouts can be avoided.
        no_timeout = Array("update_core", "update_plugins", "update_themes")
        transient_option = "_site_transient_" + transient
        if (not php_in_array(transient, no_timeout)):
            transient_timeout = "_site_transient_timeout_" + transient
            timeout = get_site_option(transient_timeout)
            if False != timeout and timeout < time():
                delete_site_option(transient_option)
                delete_site_option(transient_timeout)
                value = False
            # end if
        # end if
        if (not (php_isset(lambda : value))):
            value = get_site_option(transient_option)
        # end if
    # end if
    #// 
    #// Filters the value of an existing site transient.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 2.9.0
    #// @since 4.4.0 The `$transient` parameter was added.
    #// 
    #// @param mixed  $value     Value of site transient.
    #// @param string $transient Transient name.
    #//
    return apply_filters(str("site_transient_") + str(transient), value, transient)
# end def get_site_transient
#// 
#// Sets/updates the value of a site transient.
#// 
#// You do not need to serialize values. If the value needs to be serialized,
#// then it will be serialized before it is set.
#// 
#// @since 2.9.0
#// 
#// @see set_transient()
#// 
#// @param string $transient  Transient name. Expected to not be SQL-escaped. Must be
#// 167 characters or fewer in length.
#// @param mixed  $value      Transient value. Expected to not be SQL-escaped.
#// @param int    $expiration Optional. Time until expiration in seconds. Default 0 (no expiration).
#// @return bool False if value was not set and true if value was set.
#//
def set_site_transient(transient=None, value=None, expiration=0, *args_):
    
    #// 
    #// Filters the value of a specific site transient before it is set.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 3.0.0
    #// @since 4.4.0 The `$transient` parameter was added.
    #// 
    #// @param mixed  $value     New value of site transient.
    #// @param string $transient Transient name.
    #//
    value = apply_filters(str("pre_set_site_transient_") + str(transient), value, transient)
    expiration = php_int(expiration)
    #// 
    #// Filters the expiration for a site transient before its value is set.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int    $expiration Time until expiration in seconds. Use 0 for no expiration.
    #// @param mixed  $value      New value of site transient.
    #// @param string $transient  Transient name.
    #//
    expiration = apply_filters(str("expiration_of_site_transient_") + str(transient), expiration, value, transient)
    if wp_using_ext_object_cache():
        result = wp_cache_set(transient, value, "site-transient", expiration)
    else:
        transient_timeout = "_site_transient_timeout_" + transient
        option = "_site_transient_" + transient
        if False == get_site_option(option):
            if expiration:
                add_site_option(transient_timeout, time() + expiration)
            # end if
            result = add_site_option(option, value)
        else:
            if expiration:
                update_site_option(transient_timeout, time() + expiration)
            # end if
            result = update_site_option(option, value)
        # end if
    # end if
    if result:
        #// 
        #// Fires after the value for a specific site transient has been set.
        #// 
        #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
        #// 
        #// @since 3.0.0
        #// @since 4.4.0 The `$transient` parameter was added
        #// 
        #// @param mixed  $value      Site transient value.
        #// @param int    $expiration Time until expiration in seconds.
        #// @param string $transient  Transient name.
        #//
        do_action(str("set_site_transient_") + str(transient), value, expiration, transient)
        #// 
        #// Fires after the value for a site transient has been set.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $transient  The name of the site transient.
        #// @param mixed  $value      Site transient value.
        #// @param int    $expiration Time until expiration in seconds.
        #//
        do_action("setted_site_transient", transient, value, expiration)
    # end if
    return result
# end def set_site_transient
#// 
#// Registers default settings available in WordPress.
#// 
#// The settings registered here are primarily useful for the REST API, so this
#// does not encompass all settings available in WordPress.
#// 
#// @since 4.7.0
#//
def register_initial_settings(*args_):
    
    register_setting("general", "blogname", Array({"show_in_rest": Array({"name": "title"})}, {"type": "string", "description": __("Site title.")}))
    register_setting("general", "blogdescription", Array({"show_in_rest": Array({"name": "description"})}, {"type": "string", "description": __("Site tagline.")}))
    if (not is_multisite()):
        register_setting("general", "siteurl", Array({"show_in_rest": Array({"name": "url", "schema": Array({"format": "uri"})})}, {"type": "string", "description": __("Site URL.")}))
    # end if
    if (not is_multisite()):
        register_setting("general", "admin_email", Array({"show_in_rest": Array({"name": "email", "schema": Array({"format": "email"})})}, {"type": "string", "description": __("This address is used for admin purposes, like new user notification.")}))
    # end if
    register_setting("general", "timezone_string", Array({"show_in_rest": Array({"name": "timezone"})}, {"type": "string", "description": __("A city in the same timezone as you.")}))
    register_setting("general", "date_format", Array({"show_in_rest": True, "type": "string", "description": __("A date format for all date strings.")}))
    register_setting("general", "time_format", Array({"show_in_rest": True, "type": "string", "description": __("A time format for all time strings.")}))
    register_setting("general", "start_of_week", Array({"show_in_rest": True, "type": "integer", "description": __("A day number of the week that the week should start on.")}))
    register_setting("general", "WPLANG", Array({"show_in_rest": Array({"name": "language"})}, {"type": "string", "description": __("WordPress locale code."), "default": "en_US"}))
    register_setting("writing", "use_smilies", Array({"show_in_rest": True, "type": "boolean", "description": __("Convert emoticons like :-) and :-P to graphics on display."), "default": True}))
    register_setting("writing", "default_category", Array({"show_in_rest": True, "type": "integer", "description": __("Default post category.")}))
    register_setting("writing", "default_post_format", Array({"show_in_rest": True, "type": "string", "description": __("Default post format.")}))
    register_setting("reading", "posts_per_page", Array({"show_in_rest": True, "type": "integer", "description": __("Blog pages show at most."), "default": 10}))
    register_setting("discussion", "default_ping_status", Array({"show_in_rest": Array({"schema": Array({"enum": Array("open", "closed")})})}, {"type": "string", "description": __("Allow link notifications from other blogs (pingbacks and trackbacks) on new articles.")}))
    register_setting("discussion", "default_comment_status", Array({"show_in_rest": Array({"schema": Array({"enum": Array("open", "closed")})})}, {"type": "string", "description": __("Allow people to submit comments on new posts.")}))
# end def register_initial_settings
#// 
#// Registers a setting and its data.
#// 
#// @since 2.7.0
#// @since 4.7.0 `$args` can be passed to set flags on the setting, similar to `register_meta()`.
#// 
#// @global array $new_whitelist_options
#// @global array $wp_registered_settings
#// 
#// @param string $option_group A settings group name. Should correspond to a whitelisted option key name.
#// Default whitelisted option key names include 'general', 'discussion', 'media',
#// 'reading', 'writing', 'misc', 'options', and 'privacy'.
#// @param string $option_name The name of an option to sanitize and save.
#// @param array  $args {
#// Data used to describe the setting when registered.
#// 
#// @type string     $type              The type of data associated with this setting.
#// Valid values are 'string', 'boolean', 'integer', 'number', 'array', and 'object'.
#// @type string     $description       A description of the data attached to this setting.
#// @type callable   $sanitize_callback A callback function that sanitizes the option's value.
#// @type bool|array $show_in_rest      Whether data associated with this setting should be included in the REST API.
#// When registering complex settings, this argument may optionally be an
#// array with a 'schema' key.
#// @type mixed      $default           Default value when calling `get_option()`.
#// }
#//
def register_setting(option_group=None, option_name=None, args=Array(), *args_):
    
    global new_whitelist_options,wp_registered_settings
    php_check_if_defined("new_whitelist_options","wp_registered_settings")
    defaults = Array({"type": "string", "group": option_group, "description": "", "sanitize_callback": None, "show_in_rest": False})
    #// Back-compat: old sanitize callback is added.
    if php_is_callable(args):
        args = Array({"sanitize_callback": args})
    # end if
    #// 
    #// Filters the registration arguments when registering a setting.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $args         Array of setting registration arguments.
    #// @param array  $defaults     Array of default arguments.
    #// @param string $option_group Setting group.
    #// @param string $option_name  Setting name.
    #//
    args = apply_filters("register_setting_args", args, defaults, option_group, option_name)
    args = wp_parse_args(args, defaults)
    #// Require an item schema when registering settings with an array type.
    if False != args["show_in_rest"] and "array" == args["type"] and (not php_is_array(args["show_in_rest"])) or (not (php_isset(lambda : args["show_in_rest"]["schema"]["items"]))):
        _doing_it_wrong(__FUNCTION__, __("When registering an \"array\" setting to show in the REST API, you must specify the schema for each array item in \"show_in_rest.schema.items\"."), "5.4.0")
    # end if
    if (not php_is_array(wp_registered_settings)):
        wp_registered_settings = Array()
    # end if
    if "misc" == option_group:
        _deprecated_argument(__FUNCTION__, "3.0.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "misc"))
        option_group = "general"
    # end if
    if "privacy" == option_group:
        _deprecated_argument(__FUNCTION__, "3.5.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "privacy"))
        option_group = "reading"
    # end if
    new_whitelist_options[option_group][-1] = option_name
    if (not php_empty(lambda : args["sanitize_callback"])):
        add_filter(str("sanitize_option_") + str(option_name), args["sanitize_callback"])
    # end if
    if php_array_key_exists("default", args):
        add_filter(str("default_option_") + str(option_name), "filter_default_option", 10, 3)
    # end if
    wp_registered_settings[option_name] = args
# end def register_setting
#// 
#// Unregisters a setting.
#// 
#// @since 2.7.0
#// @since 4.7.0 `$sanitize_callback` was deprecated. The callback from `register_setting()` is now used instead.
#// 
#// @global array $new_whitelist_options
#// @global array $wp_registered_settings
#// 
#// @param string   $option_group      The settings group name used during registration.
#// @param string   $option_name       The name of the option to unregister.
#// @param callable $deprecated        Deprecated.
#//
def unregister_setting(option_group=None, option_name=None, deprecated="", *args_):
    
    global new_whitelist_options,wp_registered_settings
    php_check_if_defined("new_whitelist_options","wp_registered_settings")
    if "misc" == option_group:
        _deprecated_argument(__FUNCTION__, "3.0.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "misc"))
        option_group = "general"
    # end if
    if "privacy" == option_group:
        _deprecated_argument(__FUNCTION__, "3.5.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "privacy"))
        option_group = "reading"
    # end if
    pos = php_array_search(option_name, new_whitelist_options[option_group])
    if False != pos:
        new_whitelist_options[option_group][pos] = None
    # end if
    if "" != deprecated:
        _deprecated_argument(__FUNCTION__, "4.7.0", php_sprintf(__("%1$s is deprecated. The callback from %2$s is used instead."), "<code>$sanitize_callback</code>", "<code>register_setting()</code>"))
        remove_filter(str("sanitize_option_") + str(option_name), deprecated)
    # end if
    if (php_isset(lambda : wp_registered_settings[option_name])):
        #// Remove the sanitize callback if one was set during registration.
        if (not php_empty(lambda : wp_registered_settings[option_name]["sanitize_callback"])):
            remove_filter(str("sanitize_option_") + str(option_name), wp_registered_settings[option_name]["sanitize_callback"])
        # end if
        #// Remove the default filter if a default was provided during registration.
        if php_array_key_exists("default", wp_registered_settings[option_name]):
            remove_filter(str("default_option_") + str(option_name), "filter_default_option", 10)
        # end if
        wp_registered_settings[option_name] = None
    # end if
# end def unregister_setting
#// 
#// Retrieves an array of registered settings.
#// 
#// @since 4.7.0
#// 
#// @global array $wp_registered_settings
#// 
#// @return array List of registered settings, keyed by option name.
#//
def get_registered_settings(*args_):
    
    global wp_registered_settings
    php_check_if_defined("wp_registered_settings")
    if (not php_is_array(wp_registered_settings)):
        return Array()
    # end if
    return wp_registered_settings
# end def get_registered_settings
#// 
#// Filters the default value for the option.
#// 
#// For settings which register a default setting in `register_setting()`, this
#// function is added as a filter to `default_option_{$option}`.
#// 
#// @since 4.7.0
#// 
#// @param mixed $default Existing default value to return.
#// @param string $option Option name.
#// @param bool $passed_default Was `get_option()` passed a default value?
#// @return mixed Filtered default value.
#//
def filter_default_option(default=None, option=None, passed_default=None, *args_):
    
    if passed_default:
        return default
    # end if
    registered = get_registered_settings()
    if php_empty(lambda : registered[option]):
        return default
    # end if
    return registered[option]["default"]
# end def filter_default_option
