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
#// A pseudo-CRON daemon for scheduling WordPress tasks
#// 
#// WP Cron is triggered when the site receives a visit. In the scenario
#// where a site may not receive enough visits to execute scheduled tasks
#// in a timely manner, this file can be called directly or via a server
#// CRON daemon for X number of times.
#// 
#// Defining DISABLE_WP_CRON as true and calling this file directly are
#// mutually exclusive and the latter does not rely on the former to work.
#// 
#// The HTTP request to this file will not slow down the visitor who happens to
#// visit when the cron job is needed to run.
#// 
#// @package WordPress
#//
ignore_user_abort(True)
#// Don't make the request block till we finish, if possible.
if php_function_exists("fastcgi_finish_request") and php_version_compare(php_phpversion(), "7.0.16", ">="):
    if (not php_headers_sent()):
        php_header("Expires: Wed, 11 Jan 1984 05:00:00 GMT")
        php_header("Cache-Control: no-cache, must-revalidate, max-age=0")
    # end if
    fastcgi_finish_request()
# end if
if (not php_empty(lambda : PHP_POST)) or php_defined("DOING_AJAX") or php_defined("DOING_CRON"):
    php_exit(0)
# end if
#// 
#// Tell WordPress we are doing the CRON task.
#// 
#// @var bool
#//
php_define("DOING_CRON", True)
if (not php_defined("ABSPATH")):
    #// Set up WordPress environment
    php_include_file(__DIR__ + "/wp-load.php", once=True)
# end if
#// 
#// Retrieves the cron lock.
#// 
#// Returns the uncached `doing_cron` transient.
#// 
#// @ignore
#// @since 3.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return string|false Value of the `doing_cron` transient, 0|false otherwise.
#//
def _get_cron_lock(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    value_ = 0
    if wp_using_ext_object_cache():
        #// 
        #// Skip local cache and force re-fetch of doing_cron transient
        #// in case another process updated the cache.
        #//
        value_ = wp_cache_get("doing_cron", "transient", True)
    else:
        row_ = wpdb_.get_row(wpdb_.prepare(str("SELECT option_value FROM ") + str(wpdb_.options) + str(" WHERE option_name = %s LIMIT 1"), "_transient_doing_cron"))
        if php_is_object(row_):
            value_ = row_.option_value
        # end if
    # end if
    return value_
# end def _get_cron_lock
crons_ = wp_get_ready_cron_jobs()
if php_empty(lambda : crons_):
    php_exit(0)
# end if
gmt_time_ = php_microtime(True)
#// The cron lock: a unix timestamp from when the cron was spawned.
doing_cron_transient_ = get_transient("doing_cron")
#// Use global $doing_wp_cron lock, otherwise use the GET lock. If no lock, try to grab a new lock.
if php_empty(lambda : doing_wp_cron_):
    if php_empty(lambda : PHP_REQUEST["doing_wp_cron"]):
        #// Called from external script/job. Try setting a lock.
        if doing_cron_transient_ and doing_cron_transient_ + WP_CRON_LOCK_TIMEOUT > gmt_time_:
            sys.exit(-1)
        # end if
        doing_wp_cron_ = php_sprintf("%.22F", php_microtime(True))
        doing_cron_transient_ = doing_wp_cron_
        set_transient("doing_cron", doing_wp_cron_)
    else:
        doing_wp_cron_ = PHP_REQUEST["doing_wp_cron"]
    # end if
# end if
#// 
#// The cron lock (a unix timestamp set when the cron was spawned),
#// must match $doing_wp_cron (the "key").
#//
if doing_cron_transient_ != doing_wp_cron_:
    sys.exit(-1)
# end if
for timestamp_,cronhooks_ in crons_.items():
    if timestamp_ > gmt_time_:
        break
    # end if
    for hook_,keys_ in cronhooks_.items():
        for k_,v_ in keys_.items():
            schedule_ = v_["schedule"]
            if schedule_:
                wp_reschedule_event(timestamp_, schedule_, hook_, v_["args"])
            # end if
            wp_unschedule_event(timestamp_, hook_, v_["args"])
            #// 
            #// Fires scheduled events.
            #// 
            #// @ignore
            #// @since 2.1.0
            #// 
            #// @param string $hook Name of the hook that was scheduled to be fired.
            #// @param array  $args The arguments to be passed to the hook.
            #//
            do_action_ref_array(hook_, v_["args"])
            #// If the hook ran too long and another cron process stole the lock, quit.
            if _get_cron_lock() != doing_wp_cron_:
                sys.exit(-1)
            # end if
        # end for
    # end for
# end for
if _get_cron_lock() == doing_wp_cron_:
    delete_transient("doing_cron")
# end if
php_exit(0)
