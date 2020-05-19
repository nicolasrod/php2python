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
#// WordPress Cron API
#// 
#// @package WordPress
#// 
#// 
#// Schedules an event to run only once.
#// 
#// Schedules a hook which will be triggered by WordPress at the specified time.
#// The action will trigger when someone visits your WordPress site if the scheduled
#// time has passed.
#// 
#// Note that scheduling an event to occur within 10 minutes of an existing event
#// with the same action hook will be ignored unless you pass unique `$args` values
#// for each scheduled event.
#// 
#// Use wp_next_scheduled() to prevent duplicate events.
#// 
#// Use wp_schedule_event() to schedule a recurring event.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return value modified to boolean indicating success or failure,
#// {@see 'pre_schedule_event'} filter added to short-circuit the function.
#// 
#// @link https://developer.wordpress.org/reference/functions/wp_schedule_single_event
#// 
#// @param int    $timestamp  Unix timestamp (UTC) for when to next run the event.
#// @param string $hook       Action hook to execute when the event is run.
#// @param array  $args       Optional. Array containing each separate argument to pass to the hook's callback function.
#// @return bool True if event successfully scheduled. False for failure.
#//
def wp_schedule_single_event(timestamp_=None, hook_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Make sure timestamp is a positive integer.
    if (not php_is_numeric(timestamp_)) or timestamp_ <= 0:
        return False
    # end if
    event_ = Array({"hook": hook_, "timestamp": timestamp_, "schedule": False, "args": args_})
    #// 
    #// Filter to preflight or hijack scheduling an event.
    #// 
    #// Returning a non-null value will short-circuit adding the event to the
    #// cron array, causing the function to return the filtered value instead.
    #// 
    #// Both single events and recurring events are passed through this filter;
    #// single events have `$event->schedule` as false, whereas recurring events
    #// have this set to a recurrence from wp_get_schedules(). Recurring
    #// events also have the integer recurrence interval set as `$event->interval`.
    #// 
    #// For plugins replacing wp-cron, it is recommended you check for an
    #// identical event within ten minutes and apply the {@see 'schedule_event'}
    #// filter to check if another plugin has disallowed the event before scheduling.
    #// 
    #// Return true if the event was scheduled, false if not.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|bool $pre   Value to return instead. Default null to continue adding the event.
    #// @param stdClass  $event {
    #// An object containing an event's data.
    #// 
    #// @type string       $hook      Action hook to execute when the event is run.
    #// @type int          $timestamp Unix timestamp (UTC) for when to next run the event.
    #// @type string|false $schedule  How often the event should subsequently recur.
    #// @type array        $args      Array containing each separate argument to pass to the hook's callback function.
    #// @type int          $interval  The interval time in seconds for the schedule. Only present for recurring events.
    #// }
    #//
    pre_ = apply_filters("pre_schedule_event", None, event_)
    if None != pre_:
        return pre_
    # end if
    #// 
    #// Check for a duplicated event.
    #// 
    #// Don't schedule an event if there's already an identical event
    #// within 10 minutes.
    #// 
    #// When scheduling events within ten minutes of the current time,
    #// all past identical events are considered duplicates.
    #// 
    #// When scheduling an event with a past timestamp (ie, before the
    #// current time) all events scheduled within the next ten minutes
    #// are considered duplicates.
    #//
    crons_ = _get_cron_array()
    key_ = php_md5(serialize(event_.args))
    duplicate_ = False
    if event_.timestamp < time() + 10 * MINUTE_IN_SECONDS:
        min_timestamp_ = 0
    else:
        min_timestamp_ = event_.timestamp - 10 * MINUTE_IN_SECONDS
    # end if
    if event_.timestamp < time():
        max_timestamp_ = time() + 10 * MINUTE_IN_SECONDS
    else:
        max_timestamp_ = event_.timestamp + 10 * MINUTE_IN_SECONDS
    # end if
    for event_timestamp_,cron_ in crons_.items():
        if event_timestamp_ < min_timestamp_:
            continue
        # end if
        if event_timestamp_ > max_timestamp_:
            break
        # end if
        if (php_isset(lambda : cron_[event_.hook][key_])):
            duplicate_ = True
            break
        # end if
    # end for
    if duplicate_:
        return False
    # end if
    #// 
    #// Modify an event before it is scheduled.
    #// 
    #// @since 3.1.0
    #// 
    #// @param stdClass $event {
    #// An object containing an event's data.
    #// 
    #// @type string       $hook      Action hook to execute when the event is run.
    #// @type int          $timestamp Unix timestamp (UTC) for when to next run the event.
    #// @type string|false $schedule  How often the event should subsequently recur.
    #// @type array        $args      Array containing each separate argument to pass to the hook's callback function.
    #// @type int          $interval  The interval time in seconds for the schedule. Only present for recurring events.
    #// }
    #//
    event_ = apply_filters("schedule_event", event_)
    #// A plugin disallowed this event.
    if (not event_):
        return False
    # end if
    crons_[event_.timestamp][event_.hook][key_] = Array({"schedule": event_.schedule, "args": event_.args})
    uksort(crons_, "strnatcasecmp")
    return _set_cron_array(crons_)
# end def wp_schedule_single_event
#// 
#// Schedules a recurring event.
#// 
#// Schedules a hook which will be triggered by WordPress at the specified interval.
#// The action will trigger when someone visits your WordPress site if the scheduled
#// time has passed.
#// 
#// Valid values for the recurrence are 'hourly', 'daily', and 'twicedaily'. These can
#// be extended using the {@see 'cron_schedules'} filter in wp_get_schedules().
#// 
#// Note that scheduling an event to occur within 10 minutes of an existing event
#// with the same action hook will be ignored unless you pass unique `$args` values
#// for each scheduled event.
#// 
#// Use wp_next_scheduled() to prevent duplicate events.
#// 
#// Use wp_schedule_single_event() to schedule a non-recurring event.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return value modified to boolean indicating success or failure,
#// {@see 'pre_schedule_event'} filter added to short-circuit the function.
#// 
#// @link https://developer.wordpress.org/reference/functions/wp_schedule_event
#// 
#// @param int    $timestamp  Unix timestamp (UTC) for when to next run the event.
#// @param string $recurrence How often the event should subsequently recur. See wp_get_schedules() for accepted values.
#// @param string $hook       Action hook to execute when the event is run.
#// @param array  $args       Optional. Array containing each separate argument to pass to the hook's callback function.
#// @return bool True if event successfully scheduled. False for failure.
#//
def wp_schedule_event(timestamp_=None, recurrence_=None, hook_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Make sure timestamp is a positive integer.
    if (not php_is_numeric(timestamp_)) or timestamp_ <= 0:
        return False
    # end if
    schedules_ = wp_get_schedules()
    if (not (php_isset(lambda : schedules_[recurrence_]))):
        return False
    # end if
    event_ = Array({"hook": hook_, "timestamp": timestamp_, "schedule": recurrence_, "args": args_, "interval": schedules_[recurrence_]["interval"]})
    #// This filter is documented in wp-includes/cron.php
    pre_ = apply_filters("pre_schedule_event", None, event_)
    if None != pre_:
        return pre_
    # end if
    #// This filter is documented in wp-includes/cron.php
    event_ = apply_filters("schedule_event", event_)
    #// A plugin disallowed this event.
    if (not event_):
        return False
    # end if
    key_ = php_md5(serialize(event_.args))
    crons_ = _get_cron_array()
    crons_[event_.timestamp][event_.hook][key_] = Array({"schedule": event_.schedule, "args": event_.args, "interval": event_.interval})
    uksort(crons_, "strnatcasecmp")
    return _set_cron_array(crons_)
# end def wp_schedule_event
#// 
#// Reschedules a recurring event.
#// 
#// Mainly for internal use, this takes the time stamp of a previously run
#// recurring event and reschedules it for its next run.
#// 
#// To change upcoming scheduled events, use wp_schedule_event() to
#// change the recurrence frequency.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return value modified to boolean indicating success or failure,
#// {@see 'pre_reschedule_event'} filter added to short-circuit the function.
#// 
#// @param int    $timestamp  Unix timestamp (UTC) for when the event was scheduled.
#// @param string $recurrence How often the event should subsequently recur. See wp_get_schedules() for accepted values.
#// @param string $hook       Action hook to execute when the event is run.
#// @param array  $args       Optional. Array containing each separate argument to pass to the hook's callback function.
#// @return bool True if event successfully rescheduled. False for failure.
#//
def wp_reschedule_event(timestamp_=None, recurrence_=None, hook_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Make sure timestamp is a positive integer.
    if (not php_is_numeric(timestamp_)) or timestamp_ <= 0:
        return False
    # end if
    schedules_ = wp_get_schedules()
    interval_ = 0
    #// First we try to get the interval from the schedule.
    if (php_isset(lambda : schedules_[recurrence_])):
        interval_ = schedules_[recurrence_]["interval"]
    # end if
    #// Now we try to get it from the saved interval in case the schedule disappears.
    if 0 == interval_:
        scheduled_event_ = wp_get_scheduled_event(hook_, args_, timestamp_)
        if scheduled_event_ and (php_isset(lambda : scheduled_event_.interval)):
            interval_ = scheduled_event_.interval
        # end if
    # end if
    event_ = Array({"hook": hook_, "timestamp": timestamp_, "schedule": recurrence_, "args": args_, "interval": interval_})
    #// 
    #// Filter to preflight or hijack rescheduling of events.
    #// 
    #// Returning a non-null value will short-circuit the normal rescheduling
    #// process, causing the function to return the filtered value instead.
    #// 
    #// For plugins replacing wp-cron, return true if the event was successfully
    #// rescheduled, false if not.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|bool $pre   Value to return instead. Default null to continue adding the event.
    #// @param stdClass  $event {
    #// An object containing an event's data.
    #// 
    #// @type string       $hook      Action hook to execute when the event is run.
    #// @type int          $timestamp Unix timestamp (UTC) for when to next run the event.
    #// @type string|false $schedule  How often the event should subsequently recur.
    #// @type array        $args      Array containing each separate argument to pass to the hook's callback function.
    #// @type int          $interval  The interval time in seconds for the schedule. Only present for recurring events.
    #// }
    #//
    pre_ = apply_filters("pre_reschedule_event", None, event_)
    if None != pre_:
        return pre_
    # end if
    #// Now we assume something is wrong and fail to schedule.
    if 0 == interval_:
        return False
    # end if
    now_ = time()
    if timestamp_ >= now_:
        timestamp_ = now_ + interval_
    else:
        timestamp_ = now_ + interval_ - now_ - timestamp_ % interval_
    # end if
    return wp_schedule_event(timestamp_, recurrence_, hook_, args_)
# end def wp_reschedule_event
#// 
#// Unschedule a previously scheduled event.
#// 
#// The $timestamp and $hook parameters are required so that the event can be
#// identified.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return value modified to boolean indicating success or failure,
#// {@see 'pre_unschedule_event'} filter added to short-circuit the function.
#// 
#// @param int    $timestamp Unix timestamp (UTC) of the event.
#// @param string $hook      Action hook of the event.
#// @param array  $args      Optional. Array containing each separate argument to pass to the hook's callback function.
#// Although not passed to a callback, these arguments are used to uniquely identify the
#// event, so they should be the same as those used when originally scheduling the event.
#// @return bool True if event successfully unscheduled. False for failure.
#//
def wp_unschedule_event(timestamp_=None, hook_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Make sure timestamp is a positive integer.
    if (not php_is_numeric(timestamp_)) or timestamp_ <= 0:
        return False
    # end if
    #// 
    #// Filter to preflight or hijack unscheduling of events.
    #// 
    #// Returning a non-null value will short-circuit the normal unscheduling
    #// process, causing the function to return the filtered value instead.
    #// 
    #// For plugins replacing wp-cron, return true if the event was successfully
    #// unscheduled, false if not.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|bool $pre       Value to return instead. Default null to continue unscheduling the event.
    #// @param int       $timestamp Timestamp for when to run the event.
    #// @param string    $hook      Action hook, the execution of which will be unscheduled.
    #// @param array     $args      Arguments to pass to the hook's callback function.
    #//
    pre_ = apply_filters("pre_unschedule_event", None, timestamp_, hook_, args_)
    if None != pre_:
        return pre_
    # end if
    crons_ = _get_cron_array()
    key_ = php_md5(serialize(args_))
    crons_[timestamp_][hook_][key_] = None
    if php_empty(lambda : crons_[timestamp_][hook_]):
        crons_[timestamp_][hook_] = None
    # end if
    if php_empty(lambda : crons_[timestamp_]):
        crons_[timestamp_] = None
    # end if
    return _set_cron_array(crons_)
# end def wp_unschedule_event
#// 
#// Unschedules all events attached to the hook with the specified arguments.
#// 
#// Warning: This function may return Boolean FALSE, but may also return a non-Boolean
#// value which evaluates to FALSE. For information about casting to booleans see the
#// {@link https://www.php.net/manual/en/language.types.boolean.php PHP documentation}. Use
#// the `===` operator for testing the return value of this function.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return value modified to indicate success or failure,
#// {@see 'pre_clear_scheduled_hook'} filter added to short-circuit the function.
#// 
#// @param string $hook Action hook, the execution of which will be unscheduled.
#// @param array  $args Optional. Arguments that were to be passed to the hook's callback function.
#// @return int|false On success an integer indicating number of events unscheduled (0 indicates no
#// events were registered with the hook and arguments combination), false if
#// unscheduling one or more events fail.
#//
def wp_clear_scheduled_hook(hook_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Backward compatibility.
    #// Previously, this function took the arguments as discrete vars rather than an array like the rest of the API.
    if (not php_is_array(args_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.0.0", __("This argument has changed to an array to match the behavior of the other cron functions."))
        args_ = php_array_slice(php_func_get_args(), 1)
    # end if
    #// 
    #// Filter to preflight or hijack clearing a scheduled hook.
    #// 
    #// Returning a non-null value will short-circuit the normal unscheduling
    #// process, causing the function to return the filtered value instead.
    #// 
    #// For plugins replacing wp-cron, return the number of events successfully
    #// unscheduled (zero if no events were registered with the hook) or false
    #// if unscheduling one or more events fails.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|int|false $pre  Value to return instead. Default null to continue unscheduling the event.
    #// @param string         $hook Action hook, the execution of which will be unscheduled.
    #// @param array          $args Arguments to pass to the hook's callback function.
    #//
    pre_ = apply_filters("pre_clear_scheduled_hook", None, hook_, args_)
    if None != pre_:
        return pre_
    # end if
    #// 
    #// This logic duplicates wp_next_scheduled().
    #// It's required due to a scenario where wp_unschedule_event() fails due to update_option() failing,
    #// and, wp_next_scheduled() returns the same schedule in an infinite loop.
    #//
    crons_ = _get_cron_array()
    if php_empty(lambda : crons_):
        return 0
    # end if
    results_ = Array()
    key_ = php_md5(serialize(args_))
    for timestamp_,cron_ in crons_.items():
        if (php_isset(lambda : cron_[hook_][key_])):
            results_[-1] = wp_unschedule_event(timestamp_, hook_, args_)
        # end if
    # end for
    if php_in_array(False, results_, True):
        return False
    # end if
    return php_count(results_)
# end def wp_clear_scheduled_hook
#// 
#// Unschedules all events attached to the hook.
#// 
#// Can be useful for plugins when deactivating to clean up the cron queue.
#// 
#// Warning: This function may return Boolean FALSE, but may also return a non-Boolean
#// value which evaluates to FALSE. For information about casting to booleans see the
#// {@link https://www.php.net/manual/en/language.types.boolean.php PHP documentation}. Use
#// the `===` operator for testing the return value of this function.
#// 
#// @since 4.9.0
#// @since 5.1.0 Return value added to indicate success or failure.
#// 
#// @param string $hook Action hook, the execution of which will be unscheduled.
#// @return int|false On success an integer indicating number of events unscheduled (0 indicates no
#// events were registered on the hook), false if unscheduling fails.
#//
def wp_unschedule_hook(hook_=None, *_args_):
    
    
    #// 
    #// Filter to preflight or hijack clearing all events attached to the hook.
    #// 
    #// Returning a non-null value will short-circuit the normal unscheduling
    #// process, causing the function to return the filtered value instead.
    #// 
    #// For plugins replacing wp-cron, return the number of events successfully
    #// unscheduled (zero if no events were registered with the hook) or false
    #// if unscheduling one or more events fails.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|int|false $pre  Value to return instead. Default null to continue unscheduling the hook.
    #// @param string         $hook Action hook, the execution of which will be unscheduled.
    #//
    pre_ = apply_filters("pre_unschedule_hook", None, hook_)
    if None != pre_:
        return pre_
    # end if
    crons_ = _get_cron_array()
    if php_empty(lambda : crons_):
        return 0
    # end if
    results_ = Array()
    for timestamp_,args_ in crons_.items():
        if (not php_empty(lambda : crons_[timestamp_][hook_])):
            results_[-1] = php_count(crons_[timestamp_][hook_])
        # end if
        crons_[timestamp_][hook_] = None
        if php_empty(lambda : crons_[timestamp_]):
            crons_[timestamp_] = None
        # end if
    # end for
    #// 
    #// If the results are empty (zero events to unschedule), no attempt
    #// to update the cron array is required.
    #//
    if php_empty(lambda : results_):
        return 0
    # end if
    if _set_cron_array(crons_):
        return array_sum(results_)
    # end if
    return False
# end def wp_unschedule_hook
#// 
#// Retrieve a scheduled event.
#// 
#// Retrieve the full event object for a given event, if no timestamp is specified the next
#// scheduled event is returned.
#// 
#// @since 5.1.0
#// 
#// @param string   $hook      Action hook of the event.
#// @param array    $args      Optional. Array containing each separate argument to pass to the hook's callback function.
#// Although not passed to a callback, these arguments are used to uniquely identify the
#// event, so they should be the same as those used when originally scheduling the event.
#// @param int|null $timestamp Optional. Unix timestamp (UTC) of the event. If not specified, the next scheduled event is returned.
#// @return object|false The event object. False if the event does not exist.
#//
def wp_get_scheduled_event(hook_=None, args_=None, timestamp_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    if timestamp_ is None:
        timestamp_ = None
    # end if
    
    #// 
    #// Filter to preflight or hijack retrieving a scheduled event.
    #// 
    #// Returning a non-null value will short-circuit the normal process,
    #// returning the filtered value instead.
    #// 
    #// Return false if the event does not exist, otherwise an event object
    #// should be returned.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|false|object $pre  Value to return instead. Default null to continue retrieving the event.
    #// @param string            $hook Action hook of the event.
    #// @param array             $args Array containing each separate argument to pass to the hook's callback function.
    #// Although not passed to a callback, these arguments are used to uniquely identify
    #// the event.
    #// @param int|null  $timestamp Unix timestamp (UTC) of the event. Null to retrieve next scheduled event.
    #//
    pre_ = apply_filters("pre_get_scheduled_event", None, hook_, args_, timestamp_)
    if None != pre_:
        return pre_
    # end if
    if None != timestamp_ and (not php_is_numeric(timestamp_)):
        return False
    # end if
    crons_ = _get_cron_array()
    if php_empty(lambda : crons_):
        return False
    # end if
    key_ = php_md5(serialize(args_))
    if (not timestamp_):
        #// Get next event.
        next_ = False
        for timestamp_,cron_ in crons_.items():
            if (php_isset(lambda : cron_[hook_][key_])):
                next_ = timestamp_
                break
            # end if
        # end for
        if (not next_):
            return False
        # end if
        timestamp_ = next_
    elif (not (php_isset(lambda : crons_[timestamp_][hook_][key_]))):
        return False
    # end if
    event_ = Array({"hook": hook_, "timestamp": timestamp_, "schedule": crons_[timestamp_][hook_][key_]["schedule"], "args": args_})
    if (php_isset(lambda : crons_[timestamp_][hook_][key_]["interval"])):
        event_.interval = crons_[timestamp_][hook_][key_]["interval"]
    # end if
    return event_
# end def wp_get_scheduled_event
#// 
#// Retrieve the next timestamp for an event.
#// 
#// @since 2.1.0
#// 
#// @param string $hook Action hook of the event.
#// @param array  $args Optional. Array containing each separate argument to pass to the hook's callback function.
#// Although not passed to a callback, these arguments are used to uniquely identify the
#// event, so they should be the same as those used when originally scheduling the event.
#// @return int|false The Unix timestamp of the next time the event will occur. False if the event doesn't exist.
#//
def wp_next_scheduled(hook_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    next_event_ = wp_get_scheduled_event(hook_, args_)
    if (not next_event_):
        return False
    # end if
    return next_event_.timestamp
# end def wp_next_scheduled
#// 
#// Sends a request to run cron through HTTP request that doesn't halt page loading.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return values added.
#// 
#// @param int $gmt_time Optional. Unix timestamp (UTC). Default 0 (current time is used).
#// @return bool True if spawned, false if no events spawned.
#//
def spawn_cron(gmt_time_=0, *_args_):
    
    
    if (not gmt_time_):
        gmt_time_ = php_microtime(True)
    # end if
    if php_defined("DOING_CRON") or (php_isset(lambda : PHP_REQUEST["doing_wp_cron"])):
        return False
    # end if
    #// 
    #// Get the cron lock, which is a Unix timestamp of when the last cron was spawned
    #// and has not finished running.
    #// 
    #// Multiple processes on multiple web servers can run this code concurrently,
    #// this lock attempts to make spawning as atomic as possible.
    #//
    lock_ = get_transient("doing_cron")
    if lock_ > gmt_time_ + 10 * MINUTE_IN_SECONDS:
        lock_ = 0
    # end if
    #// Don't run if another process is currently running it or more than once every 60 sec.
    if lock_ + WP_CRON_LOCK_TIMEOUT > gmt_time_:
        return False
    # end if
    #// Sanity check.
    crons_ = wp_get_ready_cron_jobs()
    if php_empty(lambda : crons_):
        return False
    # end if
    keys_ = php_array_keys(crons_)
    if (php_isset(lambda : keys_[0])) and keys_[0] > gmt_time_:
        return False
    # end if
    if php_defined("ALTERNATE_WP_CRON") and ALTERNATE_WP_CRON:
        if "GET" != PHP_SERVER["REQUEST_METHOD"] or php_defined("DOING_AJAX") or php_defined("XMLRPC_REQUEST"):
            return False
        # end if
        doing_wp_cron_ = php_sprintf("%.22F", gmt_time_)
        set_transient("doing_cron", doing_wp_cron_)
        ob_start()
        wp_redirect(add_query_arg("doing_wp_cron", doing_wp_cron_, wp_unslash(PHP_SERVER["REQUEST_URI"])))
        php_print(" ")
        #// Flush any buffers and send the headers.
        wp_ob_end_flush_all()
        flush()
        php_include_file(ABSPATH + "wp-cron.php", once=False)
        return True
    # end if
    #// Set the cron lock with the current unix timestamp, when the cron is being spawned.
    doing_wp_cron_ = php_sprintf("%.22F", gmt_time_)
    set_transient("doing_cron", doing_wp_cron_)
    #// 
    #// Filters the cron request arguments.
    #// 
    #// @since 3.5.0
    #// @since 4.5.0 The `$doing_wp_cron` parameter was added.
    #// 
    #// @param array $cron_request_array {
    #// An array of cron request URL arguments.
    #// 
    #// @type string $url  The cron request URL.
    #// @type int    $key  The 22 digit GMT microtime.
    #// @type array  $args {
    #// An array of cron request arguments.
    #// 
    #// @type int  $timeout   The request timeout in seconds. Default .01 seconds.
    #// @type bool $blocking  Whether to set blocking for the request. Default false.
    #// @type bool $sslverify Whether SSL should be verified for the request. Default false.
    #// }
    #// }
    #// @param string $doing_wp_cron The unix timestamp of the cron lock.
    #//
    cron_request_ = apply_filters("cron_request", Array({"url": add_query_arg("doing_wp_cron", doing_wp_cron_, site_url("wp-cron.php")), "key": doing_wp_cron_, "args": Array({"timeout": 0.01, "blocking": False, "sslverify": apply_filters("https_local_ssl_verify", False)})}), doing_wp_cron_)
    result_ = wp_remote_post(cron_request_["url"], cron_request_["args"])
    return (not is_wp_error(result_))
# end def spawn_cron
#// 
#// Run scheduled callbacks or spawn cron for all scheduled events.
#// 
#// Warning: This function may return Boolean FALSE, but may also return a non-Boolean
#// value which evaluates to FALSE. For information about casting to booleans see the
#// {@link https://www.php.net/manual/en/language.types.boolean.php PHP documentation}. Use
#// the `===` operator for testing the return value of this function.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return value added to indicate success or failure.
#// 
#// @return bool|int On success an integer indicating number of events spawned (0 indicates no
#// events needed to be spawned), false if spawning fails for one or more events.
#//
def wp_cron(*_args_):
    
    
    #// Prevent infinite loops caused by lack of wp-cron.php.
    if php_strpos(PHP_SERVER["REQUEST_URI"], "/wp-cron.php") != False or php_defined("DISABLE_WP_CRON") and DISABLE_WP_CRON:
        return 0
    # end if
    crons_ = wp_get_ready_cron_jobs()
    if php_empty(lambda : crons_):
        return 0
    # end if
    gmt_time_ = php_microtime(True)
    keys_ = php_array_keys(crons_)
    if (php_isset(lambda : keys_[0])) and keys_[0] > gmt_time_:
        return 0
    # end if
    schedules_ = wp_get_schedules()
    results_ = Array()
    for timestamp_,cronhooks_ in crons_.items():
        if timestamp_ > gmt_time_:
            break
        # end if
        for hook_,args_ in cronhooks_.items():
            if (php_isset(lambda : schedules_[hook_]["callback"])) and (not php_call_user_func(schedules_[hook_]["callback"])):
                continue
            # end if
            results_[-1] = spawn_cron(gmt_time_)
            break
        # end for
    # end for
    if php_in_array(False, results_, True):
        return False
    # end if
    return php_count(results_)
# end def wp_cron
#// 
#// Retrieve supported event recurrence schedules.
#// 
#// The default supported recurrences are 'hourly', 'twicedaily', 'daily', and 'weekly'.
#// A plugin may add more by hooking into the {@see 'cron_schedules'} filter.
#// The filter accepts an array of arrays. The outer array has a key that is the name
#// of the schedule, for example 'monthly'. The value is an array with two keys,
#// one is 'interval' and the other is 'display'.
#// 
#// The 'interval' is a number in seconds of when the cron job should run.
#// So for 'hourly' the time is `HOUR_IN_SECONDS` (60 * 60 or 3600). For 'monthly',
#// the value would be `MONTH_IN_SECONDS` (30 * 24 * 60 * 60 or 2592000).
#// 
#// The 'display' is the description. For the 'monthly' key, the 'display'
#// would be `__( 'Once Monthly' )`.
#// 
#// For your plugin, you will be passed an array. You can easily add your
#// schedule by doing the following.
#// 
#// Filter parameter variable name is 'array'.
#// $array['monthly'] = array(
#// 'interval' => MONTH_IN_SECONDS,
#// 'display'  => __( 'Once Monthly' )
#// );
#// 
#// @since 2.1.0
#// @since 5.4.0 The 'weekly' schedule was added.
#// 
#// @return array
#//
def wp_get_schedules(*_args_):
    
    
    schedules_ = Array({"hourly": Array({"interval": HOUR_IN_SECONDS, "display": __("Once Hourly")})}, {"twicedaily": Array({"interval": 12 * HOUR_IN_SECONDS, "display": __("Twice Daily")})}, {"daily": Array({"interval": DAY_IN_SECONDS, "display": __("Once Daily")})}, {"weekly": Array({"interval": WEEK_IN_SECONDS, "display": __("Once Weekly")})})
    #// 
    #// Filters the non-default cron schedules.
    #// 
    #// @since 2.1.0
    #// 
    #// @param array $new_schedules An array of non-default cron schedules. Default empty.
    #//
    return php_array_merge(apply_filters("cron_schedules", Array()), schedules_)
# end def wp_get_schedules
#// 
#// Retrieve the recurrence schedule for an event.
#// 
#// @see wp_get_schedules() for available schedules.
#// 
#// @since 2.1.0
#// @since 5.1.0 {@see 'get_schedule'} filter added.
#// 
#// @param string $hook Action hook to identify the event.
#// @param array $args Optional. Arguments passed to the event's callback function.
#// @return string|false False, if no schedule. Schedule name on success.
#//
def wp_get_schedule(hook_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    schedule_ = False
    event_ = wp_get_scheduled_event(hook_, args_)
    if event_:
        schedule_ = event_.schedule
    # end if
    #// 
    #// Filter the schedule for a hook.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string|bool $schedule Schedule for the hook. False if not found.
    #// @param string      $hook     Action hook to execute when cron is run.
    #// @param array       $args     Optional. Arguments to pass to the hook's callback function.
    #//
    return apply_filters("get_schedule", schedule_, hook_, args_)
# end def wp_get_schedule
#// 
#// Retrieve cron jobs ready to be run.
#// 
#// Returns the results of _get_cron_array() limited to events ready to be run,
#// ie, with a timestamp in the past.
#// 
#// @since 5.1.0
#// 
#// @return array Cron jobs ready to be run.
#//
def wp_get_ready_cron_jobs(*_args_):
    
    
    #// 
    #// Filter to preflight or hijack retrieving ready cron jobs.
    #// 
    #// Returning an array will short-circuit the normal retrieval of ready
    #// cron jobs, causing the function to return the filtered value instead.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|array $pre Array of ready cron tasks to return instead. Default null
    #// to continue using results from _get_cron_array().
    #//
    pre_ = apply_filters("pre_get_ready_cron_jobs", None)
    if None != pre_:
        return pre_
    # end if
    crons_ = _get_cron_array()
    if False == crons_:
        return Array()
    # end if
    gmt_time_ = php_microtime(True)
    keys_ = php_array_keys(crons_)
    if (php_isset(lambda : keys_[0])) and keys_[0] > gmt_time_:
        return Array()
    # end if
    results_ = Array()
    for timestamp_,cronhooks_ in crons_.items():
        if timestamp_ > gmt_time_:
            break
        # end if
        results_[timestamp_] = cronhooks_
    # end for
    return results_
# end def wp_get_ready_cron_jobs
#// 
#// Private functions.
#// 
#// 
#// Retrieve cron info array option.
#// 
#// @since 2.1.0
#// @access private
#// 
#// @return array|false CRON info array.
#//
def _get_cron_array(*_args_):
    
    
    cron_ = get_option("cron")
    if (not php_is_array(cron_)):
        return False
    # end if
    if (not (php_isset(lambda : cron_["version"]))):
        cron_ = _upgrade_cron_array(cron_)
    # end if
    cron_["version"] = None
    return cron_
# end def _get_cron_array
#// 
#// Updates the CRON option with the new CRON array.
#// 
#// @since 2.1.0
#// @since 5.1.0 Return value modified to outcome of update_option().
#// 
#// @access private
#// 
#// @param array $cron Cron info array from _get_cron_array().
#// @return bool True if cron array updated, false on failure.
#//
def _set_cron_array(cron_=None, *_args_):
    
    
    cron_["version"] = 2
    return update_option("cron", cron_)
# end def _set_cron_array
#// 
#// Upgrade a Cron info array.
#// 
#// This function upgrades the Cron info array to version 2.
#// 
#// @since 2.1.0
#// @access private
#// 
#// @param array $cron Cron info array from _get_cron_array().
#// @return array An upgraded Cron info array.
#//
def _upgrade_cron_array(cron_=None, *_args_):
    
    
    if (php_isset(lambda : cron_["version"])) and 2 == cron_["version"]:
        return cron_
    # end if
    new_cron_ = Array()
    for timestamp_,hooks_ in cron_.items():
        for hook_,args_ in hooks_.items():
            key_ = php_md5(serialize(args_["args"]))
            new_cron_[timestamp_][hook_][key_] = args_
        # end for
    # end for
    new_cron_["version"] = 2
    update_option("cron", new_cron_)
    return new_cron_
# end def _upgrade_cron_array
