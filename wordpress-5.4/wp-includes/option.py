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
def get_option(option_=None, default_=None, *_args_):
    if default_ is None:
        default_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    option_ = php_trim(option_)
    if php_empty(lambda : option_):
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
    pre_ = apply_filters(str("pre_option_") + str(option_), False, option_, default_)
    if False != pre_:
        return pre_
    # end if
    if php_defined("WP_SETUP_CONFIG"):
        return False
    # end if
    #// Distinguish between `false` as a default, and not passing one.
    passed_default_ = php_func_num_args() > 1
    if (not wp_installing()):
        #// Prevent non-existent options from triggering multiple queries.
        notoptions_ = wp_cache_get("notoptions", "options")
        if (php_isset(lambda : notoptions_[option_])):
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
            return apply_filters(str("default_option_") + str(option_), default_, option_, passed_default_)
        # end if
        alloptions_ = wp_load_alloptions()
        if (php_isset(lambda : alloptions_[option_])):
            value_ = alloptions_[option_]
        else:
            value_ = wp_cache_get(option_, "options")
            if False == value_:
                row_ = wpdb_.get_row(wpdb_.prepare(str("SELECT option_value FROM ") + str(wpdb_.options) + str(" WHERE option_name = %s LIMIT 1"), option_))
                #// Has to be get_row() instead of get_var() because of funkiness with 0, false, null values.
                if php_is_object(row_):
                    value_ = row_.option_value
                    wp_cache_add(option_, value_, "options")
                else:
                    #// Option does not exist, so we must cache its non-existence.
                    if (not php_is_array(notoptions_)):
                        notoptions_ = Array()
                    # end if
                    notoptions_[option_] = True
                    wp_cache_set("notoptions", notoptions_, "options")
                    #// This filter is documented in wp-includes/option.php
                    return apply_filters(str("default_option_") + str(option_), default_, option_, passed_default_)
                # end if
            # end if
        # end if
    else:
        suppress_ = wpdb_.suppress_errors()
        row_ = wpdb_.get_row(wpdb_.prepare(str("SELECT option_value FROM ") + str(wpdb_.options) + str(" WHERE option_name = %s LIMIT 1"), option_))
        wpdb_.suppress_errors(suppress_)
        if php_is_object(row_):
            value_ = row_.option_value
        else:
            #// This filter is documented in wp-includes/option.php
            return apply_filters(str("default_option_") + str(option_), default_, option_, passed_default_)
        # end if
    # end if
    #// If home is not set, use siteurl.
    if "home" == option_ and "" == value_:
        return get_option("siteurl")
    # end if
    if php_in_array(option_, Array("siteurl", "home", "category_base", "tag_base")):
        value_ = untrailingslashit(value_)
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
    return apply_filters(str("option_") + str(option_), maybe_unserialize(value_), option_)
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
def wp_protect_special_option(option_=None, *_args_):
    
    
    if "alloptions" == option_ or "notoptions" == option_:
        wp_die(php_sprintf(__("%s is a protected WP option and may not be modified"), esc_html(option_)))
    # end if
# end def wp_protect_special_option
#// 
#// Prints option value after sanitizing for forms.
#// 
#// @since 1.5.0
#// 
#// @param string $option Option name.
#//
def form_option(option_=None, *_args_):
    
    
    php_print(esc_attr(get_option(option_)))
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
def wp_load_alloptions(force_cache_=None, *_args_):
    if force_cache_ is None:
        force_cache_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not wp_installing()) or (not is_multisite()):
        alloptions_ = wp_cache_get("alloptions", "options", force_cache_)
    else:
        alloptions_ = False
    # end if
    if (not alloptions_):
        suppress_ = wpdb_.suppress_errors()
        alloptions_db_ = wpdb_.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb_.options) + str(" WHERE autoload = 'yes'"))
        if (not alloptions_db_):
            alloptions_db_ = wpdb_.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb_.options))
        # end if
        wpdb_.suppress_errors(suppress_)
        alloptions_ = Array()
        for o_ in alloptions_db_:
            alloptions_[o_.option_name] = o_.option_value
        # end for
        if (not wp_installing()) or (not is_multisite()):
            #// 
            #// Filters all options before caching them.
            #// 
            #// @since 4.9.0
            #// 
            #// @param array $alloptions Array with all options.
            #//
            alloptions_ = apply_filters("pre_cache_alloptions", alloptions_)
            wp_cache_add("alloptions", alloptions_, "options")
        # end if
    # end if
    #// 
    #// Filters all options after retrieving them.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $alloptions Array with all options.
    #//
    return apply_filters("alloptions", alloptions_)
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
def wp_load_core_site_options(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not is_multisite()) or wp_using_ext_object_cache() or wp_installing():
        return
    # end if
    if php_empty(lambda : network_id_):
        network_id_ = get_current_network_id()
    # end if
    core_options_ = Array("site_name", "siteurl", "active_sitewide_plugins", "_site_transient_timeout_theme_roots", "_site_transient_theme_roots", "site_admins", "can_compress_scripts", "global_terms_enabled", "ms_files_rewriting")
    core_options_in_ = "'" + php_implode("', '", core_options_) + "'"
    options_ = wpdb_.get_results(wpdb_.prepare(str("SELECT meta_key, meta_value FROM ") + str(wpdb_.sitemeta) + str(" WHERE meta_key IN (") + str(core_options_in_) + str(") AND site_id = %d"), network_id_))
    for option_ in options_:
        key_ = option_.meta_key
        cache_key_ = str(network_id_) + str(":") + str(key_)
        option_.meta_value = maybe_unserialize(option_.meta_value)
        wp_cache_set(cache_key_, option_.meta_value, "site-options")
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
def update_option(option_=None, value_=None, autoload_=None, *_args_):
    if autoload_ is None:
        autoload_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    option_ = php_trim(option_)
    if php_empty(lambda : option_):
        return False
    # end if
    wp_protect_special_option(option_)
    if php_is_object(value_):
        value_ = copy.deepcopy(value_)
    # end if
    value_ = sanitize_option(option_, value_)
    old_value_ = get_option(option_)
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
    value_ = apply_filters(str("pre_update_option_") + str(option_), value_, old_value_, option_)
    #// 
    #// Filters an option before its value is (maybe) serialized and updated.
    #// 
    #// @since 3.9.0
    #// 
    #// @param mixed  $value     The new, unserialized option value.
    #// @param string $option    Name of the option.
    #// @param mixed  $old_value The old option value.
    #//
    value_ = apply_filters("pre_update_option", value_, option_, old_value_)
    #// 
    #// If the new and old values are the same, no need to update.
    #// 
    #// Unserialized values will be adequate in most cases. If the unserialized
    #// data differs, the (maybe) serialized data is checked to avoid
    #// unnecessary database calls for otherwise identical object instances.
    #// 
    #// See https://core.trac.wordpress.org/ticket/38903
    #//
    if value_ == old_value_ or maybe_serialize(value_) == maybe_serialize(old_value_):
        return False
    # end if
    #// This filter is documented in wp-includes/option.php
    if apply_filters(str("default_option_") + str(option_), False, option_, False) == old_value_:
        #// Default setting for new options is 'yes'.
        if None == autoload_:
            autoload_ = "yes"
        # end if
        return add_option(option_, value_, "", autoload_)
    # end if
    serialized_value_ = maybe_serialize(value_)
    #// 
    #// Fires immediately before an option value is updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option    Name of the option to update.
    #// @param mixed  $old_value The old option value.
    #// @param mixed  $value     The new option value.
    #//
    do_action("update_option", option_, old_value_, value_)
    update_args_ = Array({"option_value": serialized_value_})
    if None != autoload_:
        update_args_["autoload"] = "no" if "no" == autoload_ or False == autoload_ else "yes"
    # end if
    result_ = wpdb_.update(wpdb_.options, update_args_, Array({"option_name": option_}))
    if (not result_):
        return False
    # end if
    notoptions_ = wp_cache_get("notoptions", "options")
    if php_is_array(notoptions_) and (php_isset(lambda : notoptions_[option_])):
        notoptions_[option_] = None
        wp_cache_set("notoptions", notoptions_, "options")
    # end if
    if (not wp_installing()):
        alloptions_ = wp_load_alloptions(True)
        if (php_isset(lambda : alloptions_[option_])):
            alloptions_[option_] = serialized_value_
            wp_cache_set("alloptions", alloptions_, "options")
        else:
            wp_cache_set(option_, serialized_value_, "options")
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
    do_action(str("update_option_") + str(option_), old_value_, value_, option_)
    #// 
    #// Fires after the value of an option has been successfully updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option    Name of the updated option.
    #// @param mixed  $old_value The old option value.
    #// @param mixed  $value     The new option value.
    #//
    do_action("updated_option", option_, old_value_, value_)
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
def add_option(option_=None, value_="", deprecated_="", autoload_="yes", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.3.0")
    # end if
    option_ = php_trim(option_)
    if php_empty(lambda : option_):
        return False
    # end if
    wp_protect_special_option(option_)
    if php_is_object(value_):
        value_ = copy.deepcopy(value_)
    # end if
    value_ = sanitize_option(option_, value_)
    #// Make sure the option doesn't already exist.
    #// We can check the 'notoptions' cache before we ask for a DB query.
    notoptions_ = wp_cache_get("notoptions", "options")
    if (not php_is_array(notoptions_)) or (not (php_isset(lambda : notoptions_[option_]))):
        #// This filter is documented in wp-includes/option.php
        if apply_filters(str("default_option_") + str(option_), False, option_, False) != get_option(option_):
            return False
        # end if
    # end if
    serialized_value_ = maybe_serialize(value_)
    autoload_ = "no" if "no" == autoload_ or False == autoload_ else "yes"
    #// 
    #// Fires before an option is added.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option Name of the option to add.
    #// @param mixed  $value  Value of the option.
    #//
    do_action("add_option", option_, value_)
    result_ = wpdb_.query(wpdb_.prepare(str("INSERT INTO `") + str(wpdb_.options) + str("` (`option_name`, `option_value`, `autoload`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `option_name` = VALUES(`option_name`), `option_value` = VALUES(`option_value`), `autoload` = VALUES(`autoload`)"), option_, serialized_value_, autoload_))
    if (not result_):
        return False
    # end if
    if (not wp_installing()):
        if "yes" == autoload_:
            alloptions_ = wp_load_alloptions(True)
            alloptions_[option_] = serialized_value_
            wp_cache_set("alloptions", alloptions_, "options")
        else:
            wp_cache_set(option_, serialized_value_, "options")
        # end if
    # end if
    #// This option exists now.
    notoptions_ = wp_cache_get("notoptions", "options")
    #// Yes, again... we need it to be fresh.
    if php_is_array(notoptions_) and (php_isset(lambda : notoptions_[option_])):
        notoptions_[option_] = None
        wp_cache_set("notoptions", notoptions_, "options")
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
    do_action(str("add_option_") + str(option_), option_, value_)
    #// 
    #// Fires after an option has been added.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option Name of the added option.
    #// @param mixed  $value  Value of the option.
    #//
    do_action("added_option", option_, value_)
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
def delete_option(option_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    option_ = php_trim(option_)
    if php_empty(lambda : option_):
        return False
    # end if
    wp_protect_special_option(option_)
    #// Get the ID, if no ID then return.
    row_ = wpdb_.get_row(wpdb_.prepare(str("SELECT autoload FROM ") + str(wpdb_.options) + str(" WHERE option_name = %s"), option_))
    if php_is_null(row_):
        return False
    # end if
    #// 
    #// Fires immediately before an option is deleted.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $option Name of the option to delete.
    #//
    do_action("delete_option", option_)
    result_ = wpdb_.delete(wpdb_.options, Array({"option_name": option_}))
    if (not wp_installing()):
        if "yes" == row_.autoload:
            alloptions_ = wp_load_alloptions(True)
            if php_is_array(alloptions_) and (php_isset(lambda : alloptions_[option_])):
                alloptions_[option_] = None
                wp_cache_set("alloptions", alloptions_, "options")
            # end if
        else:
            wp_cache_delete(option_, "options")
        # end if
    # end if
    if result_:
        #// 
        #// Fires after a specific option has been deleted.
        #// 
        #// The dynamic portion of the hook name, `$option`, refers to the option name.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $option Name of the deleted option.
        #//
        do_action(str("delete_option_") + str(option_), option_)
        #// 
        #// Fires after an option has been deleted.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string $option Name of the deleted option.
        #//
        do_action("deleted_option", option_)
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
def delete_transient(transient_=None, *_args_):
    
    
    #// 
    #// Fires immediately before a specific transient is deleted.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $transient Transient name.
    #//
    do_action(str("delete_transient_") + str(transient_), transient_)
    if wp_using_ext_object_cache():
        result_ = wp_cache_delete(transient_, "transient")
    else:
        option_timeout_ = "_transient_timeout_" + transient_
        option_ = "_transient_" + transient_
        result_ = delete_option(option_)
        if result_:
            delete_option(option_timeout_)
        # end if
    # end if
    if result_:
        #// 
        #// Fires after a transient is deleted.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $transient Deleted transient name.
        #//
        do_action("deleted_transient", transient_)
    # end if
    return result_
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
def get_transient(transient_=None, *_args_):
    
    
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
    pre_ = apply_filters(str("pre_transient_") + str(transient_), False, transient_)
    if False != pre_:
        return pre_
    # end if
    if wp_using_ext_object_cache():
        value_ = wp_cache_get(transient_, "transient")
    else:
        transient_option_ = "_transient_" + transient_
        if (not wp_installing()):
            #// If option is not in alloptions, it is not autoloaded and thus has a timeout.
            alloptions_ = wp_load_alloptions()
            if (not (php_isset(lambda : alloptions_[transient_option_]))):
                transient_timeout_ = "_transient_timeout_" + transient_
                timeout_ = get_option(transient_timeout_)
                if False != timeout_ and timeout_ < time():
                    delete_option(transient_option_)
                    delete_option(transient_timeout_)
                    value_ = False
                # end if
            # end if
        # end if
        if (not (php_isset(lambda : value_))):
            value_ = get_option(transient_option_)
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
    return apply_filters(str("transient_") + str(transient_), value_, transient_)
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
def set_transient(transient_=None, value_=None, expiration_=0, *_args_):
    
    
    expiration_ = php_int(expiration_)
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
    value_ = apply_filters(str("pre_set_transient_") + str(transient_), value_, expiration_, transient_)
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
    expiration_ = apply_filters(str("expiration_of_transient_") + str(transient_), expiration_, value_, transient_)
    if wp_using_ext_object_cache():
        result_ = wp_cache_set(transient_, value_, "transient", expiration_)
    else:
        transient_timeout_ = "_transient_timeout_" + transient_
        transient_option_ = "_transient_" + transient_
        if False == get_option(transient_option_):
            autoload_ = "yes"
            if expiration_:
                autoload_ = "no"
                add_option(transient_timeout_, time() + expiration_, "", "no")
            # end if
            result_ = add_option(transient_option_, value_, "", autoload_)
        else:
            #// If expiration is requested, but the transient has no timeout option,
            #// delete, then re-create transient rather than update.
            update_ = True
            if expiration_:
                if False == get_option(transient_timeout_):
                    delete_option(transient_option_)
                    add_option(transient_timeout_, time() + expiration_, "", "no")
                    result_ = add_option(transient_option_, value_, "", "no")
                    update_ = False
                else:
                    update_option(transient_timeout_, time() + expiration_)
                # end if
            # end if
            if update_:
                result_ = update_option(transient_option_, value_)
            # end if
        # end if
    # end if
    if result_:
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
        do_action(str("set_transient_") + str(transient_), value_, expiration_, transient_)
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
        do_action("setted_transient", transient_, value_, expiration_)
    # end if
    return result_
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
def delete_expired_transients(force_db_=None, *_args_):
    if force_db_ is None:
        force_db_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not force_db_) and wp_using_ext_object_cache():
        return
    # end if
    wpdb_.query(wpdb_.prepare(str("DELETE a, b FROM ") + str(wpdb_.options) + str(" a, ") + str(wpdb_.options) + str(""" b\n            WHERE a.option_name LIKE %s\n           AND a.option_name NOT LIKE %s\n         AND b.option_name = CONCAT( '_transient_timeout_', SUBSTRING( a.option_name, 12 ) )\n           AND b.option_value < %d"""), wpdb_.esc_like("_transient_") + "%", wpdb_.esc_like("_transient_timeout_") + "%", time()))
    if (not is_multisite()):
        #// Single site stores site transients in the options table.
        wpdb_.query(wpdb_.prepare(str("DELETE a, b FROM ") + str(wpdb_.options) + str(" a, ") + str(wpdb_.options) + str(""" b\n                WHERE a.option_name LIKE %s\n               AND a.option_name NOT LIKE %s\n             AND b.option_name = CONCAT( '_site_transient_timeout_', SUBSTRING( a.option_name, 17 ) )\n              AND b.option_value < %d"""), wpdb_.esc_like("_site_transient_") + "%", wpdb_.esc_like("_site_transient_timeout_") + "%", time()))
    elif is_multisite() and is_main_site() and is_main_network():
        #// Multisite stores site transients in the sitemeta table.
        wpdb_.query(wpdb_.prepare(str("DELETE a, b FROM ") + str(wpdb_.sitemeta) + str(" a, ") + str(wpdb_.sitemeta) + str(""" b\n              WHERE a.meta_key LIKE %s\n              AND a.meta_key NOT LIKE %s\n                AND b.meta_key = CONCAT( '_site_transient_timeout_', SUBSTRING( a.meta_key, 17 ) )\n                AND b.meta_value < %d"""), wpdb_.esc_like("_site_transient_") + "%", wpdb_.esc_like("_site_transient_timeout_") + "%", time()))
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
def wp_user_settings(*_args_):
    
    global PHP_COOKIE
    if (not is_admin()) or wp_doing_ajax():
        return
    # end if
    user_id_ = get_current_user_id()
    if (not user_id_):
        return
    # end if
    if (not is_user_member_of_blog()):
        return
    # end if
    settings_ = php_str(get_user_option("user-settings", user_id_))
    if (php_isset(lambda : PHP_COOKIE["wp-settings-" + user_id_])):
        cookie_ = php_preg_replace("/[^A-Za-z0-9=&_]/", "", PHP_COOKIE["wp-settings-" + user_id_])
        #// No change or both empty.
        if cookie_ == settings_:
            return
        # end if
        last_saved_ = php_int(get_user_option("user-settings-time", user_id_))
        current_ = php_preg_replace("/[^0-9]/", "", PHP_COOKIE["wp-settings-time-" + user_id_]) if (php_isset(lambda : PHP_COOKIE["wp-settings-time-" + user_id_])) else 0
        #// The cookie is newer than the saved value. Update the user_option and leave the cookie as-is.
        if current_ > last_saved_:
            update_user_option(user_id_, "user-settings", cookie_, False)
            update_user_option(user_id_, "user-settings-time", time() - 5, False)
            return
        # end if
    # end if
    #// The cookie is not set in the current browser or the saved value is newer.
    secure_ = "https" == php_parse_url(admin_url(), PHP_URL_SCHEME)
    setcookie("wp-settings-" + user_id_, settings_, time() + YEAR_IN_SECONDS, SITECOOKIEPATH, None, secure_)
    setcookie("wp-settings-time-" + user_id_, time(), time() + YEAR_IN_SECONDS, SITECOOKIEPATH, None, secure_)
    PHP_COOKIE["wp-settings-" + user_id_] = settings_
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
def get_user_setting(name_=None, default_=None, *_args_):
    if default_ is None:
        default_ = False
    # end if
    
    all_user_settings_ = get_all_user_settings()
    return all_user_settings_[name_] if (php_isset(lambda : all_user_settings_[name_])) else default_
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
def set_user_setting(name_=None, value_=None, *_args_):
    
    
    if php_headers_sent():
        return False
    # end if
    all_user_settings_ = get_all_user_settings()
    all_user_settings_[name_] = value_
    return wp_set_all_user_settings(all_user_settings_)
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
def delete_user_setting(names_=None, *_args_):
    
    
    if php_headers_sent():
        return False
    # end if
    all_user_settings_ = get_all_user_settings()
    names_ = names_
    deleted_ = False
    for name_ in names_:
        if (php_isset(lambda : all_user_settings_[name_])):
            all_user_settings_[name_] = None
            deleted_ = True
        # end if
    # end for
    if deleted_:
        return wp_set_all_user_settings(all_user_settings_)
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
def get_all_user_settings(*_args_):
    
    
    global _updated_user_settings_
    php_check_if_defined("_updated_user_settings_")
    user_id_ = get_current_user_id()
    if (not user_id_):
        return Array()
    # end if
    if (php_isset(lambda : _updated_user_settings_)) and php_is_array(_updated_user_settings_):
        return _updated_user_settings_
    # end if
    user_settings_ = Array()
    if (php_isset(lambda : PHP_COOKIE["wp-settings-" + user_id_])):
        cookie_ = php_preg_replace("/[^A-Za-z0-9=&_-]/", "", PHP_COOKIE["wp-settings-" + user_id_])
        if php_strpos(cookie_, "="):
            #// '=' cannot be 1st char.
            parse_str(cookie_, user_settings_)
        # end if
    else:
        option_ = get_user_option("user-settings", user_id_)
        if option_ and php_is_string(option_):
            parse_str(option_, user_settings_)
        # end if
    # end if
    _updated_user_settings_ = user_settings_
    return user_settings_
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
def wp_set_all_user_settings(user_settings_=None, *_args_):
    
    
    global _updated_user_settings_
    php_check_if_defined("_updated_user_settings_")
    user_id_ = get_current_user_id()
    if (not user_id_):
        return False
    # end if
    if (not is_user_member_of_blog()):
        return
    # end if
    settings_ = ""
    for name_,value_ in user_settings_.items():
        _name_ = php_preg_replace("/[^A-Za-z0-9_-]+/", "", name_)
        _value_ = php_preg_replace("/[^A-Za-z0-9_-]+/", "", value_)
        if (not php_empty(lambda : _name_)):
            settings_ += _name_ + "=" + _value_ + "&"
        # end if
    # end for
    settings_ = php_rtrim(settings_, "&")
    parse_str(settings_, _updated_user_settings_)
    update_user_option(user_id_, "user-settings", settings_, False)
    update_user_option(user_id_, "user-settings-time", time(), False)
    return True
# end def wp_set_all_user_settings
#// 
#// Deletes the user settings of the current user.
#// 
#// @since 2.7.0
#//
def delete_all_user_settings(*_args_):
    
    
    user_id_ = get_current_user_id()
    if (not user_id_):
        return
    # end if
    update_user_option(user_id_, "user-settings", "", False)
    setcookie("wp-settings-" + user_id_, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH)
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
def get_site_option(option_=None, default_=None, deprecated_=None, *_args_):
    if default_ is None:
        default_ = False
    # end if
    if deprecated_ is None:
        deprecated_ = True
    # end if
    
    return get_network_option(None, option_, default_)
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
def add_site_option(option_=None, value_=None, *_args_):
    
    
    return add_network_option(None, option_, value_)
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
def delete_site_option(option_=None, *_args_):
    
    
    return delete_network_option(None, option_)
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
def update_site_option(option_=None, value_=None, *_args_):
    
    
    return update_network_option(None, option_, value_)
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
def get_network_option(network_id_=None, option_=None, default_=None, *_args_):
    if default_ is None:
        default_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if network_id_ and (not php_is_numeric(network_id_)):
        return False
    # end if
    network_id_ = php_int(network_id_)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id_):
        network_id_ = get_current_network_id()
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
    pre_ = apply_filters(str("pre_site_option_") + str(option_), False, option_, network_id_, default_)
    if False != pre_:
        return pre_
    # end if
    #// Prevent non-existent options from triggering multiple queries.
    notoptions_key_ = str(network_id_) + str(":notoptions")
    notoptions_ = wp_cache_get(notoptions_key_, "site-options")
    if php_is_array(notoptions_) and (php_isset(lambda : notoptions_[option_])):
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
        return apply_filters(str("default_site_option_") + str(option_), default_, option_, network_id_)
    # end if
    if (not is_multisite()):
        #// This filter is documented in wp-includes/option.php
        default_ = apply_filters("default_site_option_" + option_, default_, option_, network_id_)
        value_ = get_option(option_, default_)
    else:
        cache_key_ = str(network_id_) + str(":") + str(option_)
        value_ = wp_cache_get(cache_key_, "site-options")
        if (not (php_isset(lambda : value_))) or False == value_:
            row_ = wpdb_.get_row(wpdb_.prepare(str("SELECT meta_value FROM ") + str(wpdb_.sitemeta) + str(" WHERE meta_key = %s AND site_id = %d"), option_, network_id_))
            #// Has to be get_row() instead of get_var() because of funkiness with 0, false, null values.
            if php_is_object(row_):
                value_ = row_.meta_value
                value_ = maybe_unserialize(value_)
                wp_cache_set(cache_key_, value_, "site-options")
            else:
                if (not php_is_array(notoptions_)):
                    notoptions_ = Array()
                # end if
                notoptions_[option_] = True
                wp_cache_set(notoptions_key_, notoptions_, "site-options")
                #// This filter is documented in wp-includes/option.php
                value_ = apply_filters("default_site_option_" + option_, default_, option_, network_id_)
            # end if
        # end if
    # end if
    if (not php_is_array(notoptions_)):
        notoptions_ = Array()
        wp_cache_set(notoptions_key_, notoptions_, "site-options")
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
    return apply_filters(str("site_option_") + str(option_), value_, option_, network_id_)
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
def add_network_option(network_id_=None, option_=None, value_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if network_id_ and (not php_is_numeric(network_id_)):
        return False
    # end if
    network_id_ = php_int(network_id_)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id_):
        network_id_ = get_current_network_id()
    # end if
    wp_protect_special_option(option_)
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
    value_ = apply_filters(str("pre_add_site_option_") + str(option_), value_, option_, network_id_)
    notoptions_key_ = str(network_id_) + str(":notoptions")
    if (not is_multisite()):
        result_ = add_option(option_, value_, "", "no")
    else:
        cache_key_ = str(network_id_) + str(":") + str(option_)
        #// Make sure the option doesn't already exist.
        #// We can check the 'notoptions' cache before we ask for a DB query.
        notoptions_ = wp_cache_get(notoptions_key_, "site-options")
        if (not php_is_array(notoptions_)) or (not (php_isset(lambda : notoptions_[option_]))):
            if False != get_network_option(network_id_, option_, False):
                return False
            # end if
        # end if
        value_ = sanitize_option(option_, value_)
        serialized_value_ = maybe_serialize(value_)
        result_ = wpdb_.insert(wpdb_.sitemeta, Array({"site_id": network_id_, "meta_key": option_, "meta_value": serialized_value_}))
        if (not result_):
            return False
        # end if
        wp_cache_set(cache_key_, value_, "site-options")
        #// This option exists now.
        notoptions_ = wp_cache_get(notoptions_key_, "site-options")
        #// Yes, again... we need it to be fresh.
        if php_is_array(notoptions_) and (php_isset(lambda : notoptions_[option_])):
            notoptions_[option_] = None
            wp_cache_set(notoptions_key_, notoptions_, "site-options")
        # end if
    # end if
    if result_:
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
        do_action(str("add_site_option_") + str(option_), option_, value_, network_id_)
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
        do_action("add_site_option", option_, value_, network_id_)
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
def delete_network_option(network_id_=None, option_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if network_id_ and (not php_is_numeric(network_id_)):
        return False
    # end if
    network_id_ = php_int(network_id_)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id_):
        network_id_ = get_current_network_id()
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
    do_action(str("pre_delete_site_option_") + str(option_), option_, network_id_)
    if (not is_multisite()):
        result_ = delete_option(option_)
    else:
        row_ = wpdb_.get_row(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.sitemeta) + str(" WHERE meta_key = %s AND site_id = %d"), option_, network_id_))
        if php_is_null(row_) or (not row_.meta_id):
            return False
        # end if
        cache_key_ = str(network_id_) + str(":") + str(option_)
        wp_cache_delete(cache_key_, "site-options")
        result_ = wpdb_.delete(wpdb_.sitemeta, Array({"meta_key": option_, "site_id": network_id_}))
    # end if
    if result_:
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
        do_action(str("delete_site_option_") + str(option_), option_, network_id_)
        #// 
        #// Fires after a network option has been deleted.
        #// 
        #// @since 3.0.0
        #// @since 4.7.0 The `$network_id` parameter was added.
        #// 
        #// @param string $option     Name of the network option.
        #// @param int    $network_id ID of the network.
        #//
        do_action("delete_site_option", option_, network_id_)
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
def update_network_option(network_id_=None, option_=None, value_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if network_id_ and (not php_is_numeric(network_id_)):
        return False
    # end if
    network_id_ = php_int(network_id_)
    #// Fallback to the current network if a network ID is not specified.
    if (not network_id_):
        network_id_ = get_current_network_id()
    # end if
    wp_protect_special_option(option_)
    old_value_ = get_network_option(network_id_, option_, False)
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
    value_ = apply_filters(str("pre_update_site_option_") + str(option_), value_, old_value_, option_, network_id_)
    #// 
    #// If the new and old values are the same, no need to update.
    #// 
    #// Unserialized values will be adequate in most cases. If the unserialized
    #// data differs, the (maybe) serialized data is checked to avoid
    #// unnecessary database calls for otherwise identical object instances.
    #// 
    #// See https://core.trac.wordpress.org/ticket/44956
    #//
    if value_ == old_value_ or maybe_serialize(value_) == maybe_serialize(old_value_):
        return False
    # end if
    if False == old_value_:
        return add_network_option(network_id_, option_, value_)
    # end if
    notoptions_key_ = str(network_id_) + str(":notoptions")
    notoptions_ = wp_cache_get(notoptions_key_, "site-options")
    if php_is_array(notoptions_) and (php_isset(lambda : notoptions_[option_])):
        notoptions_[option_] = None
        wp_cache_set(notoptions_key_, notoptions_, "site-options")
    # end if
    if (not is_multisite()):
        result_ = update_option(option_, value_, "no")
    else:
        value_ = sanitize_option(option_, value_)
        serialized_value_ = maybe_serialize(value_)
        result_ = wpdb_.update(wpdb_.sitemeta, Array({"meta_value": serialized_value_}), Array({"site_id": network_id_, "meta_key": option_}))
        if result_:
            cache_key_ = str(network_id_) + str(":") + str(option_)
            wp_cache_set(cache_key_, value_, "site-options")
        # end if
    # end if
    if result_:
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
        do_action(str("update_site_option_") + str(option_), option_, value_, old_value_, network_id_)
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
        do_action("update_site_option", option_, value_, old_value_, network_id_)
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
def delete_site_transient(transient_=None, *_args_):
    
    
    #// 
    #// Fires immediately before a specific site transient is deleted.
    #// 
    #// The dynamic portion of the hook name, `$transient`, refers to the transient name.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $transient Transient name.
    #//
    do_action(str("delete_site_transient_") + str(transient_), transient_)
    if wp_using_ext_object_cache():
        result_ = wp_cache_delete(transient_, "site-transient")
    else:
        option_timeout_ = "_site_transient_timeout_" + transient_
        option_ = "_site_transient_" + transient_
        result_ = delete_site_option(option_)
        if result_:
            delete_site_option(option_timeout_)
        # end if
    # end if
    if result_:
        #// 
        #// Fires after a transient is deleted.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $transient Deleted transient name.
        #//
        do_action("deleted_site_transient", transient_)
    # end if
    return result_
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
def get_site_transient(transient_=None, *_args_):
    
    
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
    pre_ = apply_filters(str("pre_site_transient_") + str(transient_), False, transient_)
    if False != pre_:
        return pre_
    # end if
    if wp_using_ext_object_cache():
        value_ = wp_cache_get(transient_, "site-transient")
    else:
        #// Core transients that do not have a timeout. Listed here so querying timeouts can be avoided.
        no_timeout_ = Array("update_core", "update_plugins", "update_themes")
        transient_option_ = "_site_transient_" + transient_
        if (not php_in_array(transient_, no_timeout_)):
            transient_timeout_ = "_site_transient_timeout_" + transient_
            timeout_ = get_site_option(transient_timeout_)
            if False != timeout_ and timeout_ < time():
                delete_site_option(transient_option_)
                delete_site_option(transient_timeout_)
                value_ = False
            # end if
        # end if
        if (not (php_isset(lambda : value_))):
            value_ = get_site_option(transient_option_)
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
    return apply_filters(str("site_transient_") + str(transient_), value_, transient_)
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
def set_site_transient(transient_=None, value_=None, expiration_=0, *_args_):
    
    
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
    value_ = apply_filters(str("pre_set_site_transient_") + str(transient_), value_, transient_)
    expiration_ = php_int(expiration_)
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
    expiration_ = apply_filters(str("expiration_of_site_transient_") + str(transient_), expiration_, value_, transient_)
    if wp_using_ext_object_cache():
        result_ = wp_cache_set(transient_, value_, "site-transient", expiration_)
    else:
        transient_timeout_ = "_site_transient_timeout_" + transient_
        option_ = "_site_transient_" + transient_
        if False == get_site_option(option_):
            if expiration_:
                add_site_option(transient_timeout_, time() + expiration_)
            # end if
            result_ = add_site_option(option_, value_)
        else:
            if expiration_:
                update_site_option(transient_timeout_, time() + expiration_)
            # end if
            result_ = update_site_option(option_, value_)
        # end if
    # end if
    if result_:
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
        do_action(str("set_site_transient_") + str(transient_), value_, expiration_, transient_)
        #// 
        #// Fires after the value for a site transient has been set.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $transient  The name of the site transient.
        #// @param mixed  $value      Site transient value.
        #// @param int    $expiration Time until expiration in seconds.
        #//
        do_action("setted_site_transient", transient_, value_, expiration_)
    # end if
    return result_
# end def set_site_transient
#// 
#// Registers default settings available in WordPress.
#// 
#// The settings registered here are primarily useful for the REST API, so this
#// does not encompass all settings available in WordPress.
#// 
#// @since 4.7.0
#//
def register_initial_settings(*_args_):
    
    
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
def register_setting(option_group_=None, option_name_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global new_whitelist_options_
    global wp_registered_settings_
    php_check_if_defined("new_whitelist_options_","wp_registered_settings_")
    defaults_ = Array({"type": "string", "group": option_group_, "description": "", "sanitize_callback": None, "show_in_rest": False})
    #// Back-compat: old sanitize callback is added.
    if php_is_callable(args_):
        args_ = Array({"sanitize_callback": args_})
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
    args_ = apply_filters("register_setting_args", args_, defaults_, option_group_, option_name_)
    args_ = wp_parse_args(args_, defaults_)
    #// Require an item schema when registering settings with an array type.
    if False != args_["show_in_rest"] and "array" == args_["type"] and (not php_is_array(args_["show_in_rest"])) or (not (php_isset(lambda : args_["show_in_rest"]["schema"]["items"]))):
        _doing_it_wrong(inspect.currentframe().f_code.co_name, __("When registering an \"array\" setting to show in the REST API, you must specify the schema for each array item in \"show_in_rest.schema.items\"."), "5.4.0")
    # end if
    if (not php_is_array(wp_registered_settings_)):
        wp_registered_settings_ = Array()
    # end if
    if "misc" == option_group_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.0.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "misc"))
        option_group_ = "general"
    # end if
    if "privacy" == option_group_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.5.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "privacy"))
        option_group_ = "reading"
    # end if
    new_whitelist_options_[option_group_][-1] = option_name_
    if (not php_empty(lambda : args_["sanitize_callback"])):
        add_filter(str("sanitize_option_") + str(option_name_), args_["sanitize_callback"])
    # end if
    if php_array_key_exists("default", args_):
        add_filter(str("default_option_") + str(option_name_), "filter_default_option", 10, 3)
    # end if
    wp_registered_settings_[option_name_] = args_
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
def unregister_setting(option_group_=None, option_name_=None, deprecated_="", *_args_):
    
    
    global new_whitelist_options_
    global wp_registered_settings_
    php_check_if_defined("new_whitelist_options_","wp_registered_settings_")
    if "misc" == option_group_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.0.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "misc"))
        option_group_ = "general"
    # end if
    if "privacy" == option_group_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.5.0", php_sprintf(__("The \"%s\" options group has been removed. Use another settings group."), "privacy"))
        option_group_ = "reading"
    # end if
    pos_ = php_array_search(option_name_, new_whitelist_options_[option_group_])
    if False != pos_:
        new_whitelist_options_[option_group_][pos_] = None
    # end if
    if "" != deprecated_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "4.7.0", php_sprintf(__("%1$s is deprecated. The callback from %2$s is used instead."), "<code>$sanitize_callback</code>", "<code>register_setting()</code>"))
        remove_filter(str("sanitize_option_") + str(option_name_), deprecated_)
    # end if
    if (php_isset(lambda : wp_registered_settings_[option_name_])):
        #// Remove the sanitize callback if one was set during registration.
        if (not php_empty(lambda : wp_registered_settings_[option_name_]["sanitize_callback"])):
            remove_filter(str("sanitize_option_") + str(option_name_), wp_registered_settings_[option_name_]["sanitize_callback"])
        # end if
        #// Remove the default filter if a default was provided during registration.
        if php_array_key_exists("default", wp_registered_settings_[option_name_]):
            remove_filter(str("default_option_") + str(option_name_), "filter_default_option", 10)
        # end if
        wp_registered_settings_[option_name_] = None
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
def get_registered_settings(*_args_):
    
    
    global wp_registered_settings_
    php_check_if_defined("wp_registered_settings_")
    if (not php_is_array(wp_registered_settings_)):
        return Array()
    # end if
    return wp_registered_settings_
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
def filter_default_option(default_=None, option_=None, passed_default_=None, *_args_):
    
    
    if passed_default_:
        return default_
    # end if
    registered_ = get_registered_settings()
    if php_empty(lambda : registered_[option_]):
        return default_
    # end if
    return registered_[option_]["default"]
# end def filter_default_option
