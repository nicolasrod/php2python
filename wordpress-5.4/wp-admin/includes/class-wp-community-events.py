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
#// Administration: Community Events class.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.8.0
#// 
#// 
#// Class WP_Community_Events.
#// 
#// A client for api.wordpress.org/events.
#// 
#// @since 4.8.0
#//
class WP_Community_Events():
    #// 
    #// ID for a WordPress user account.
    #// 
    #// @since 4.8.0
    #// 
    #// @var int
    #//
    user_id = 0
    #// 
    #// Stores location data for the user.
    #// 
    #// @since 4.8.0
    #// 
    #// @var bool|array
    #//
    user_location = False
    #// 
    #// Constructor for WP_Community_Events.
    #// 
    #// @since 4.8.0
    #// 
    #// @param int        $user_id       WP user ID.
    #// @param bool|array $user_location Stored location data for the user.
    #// false to pass no location;
    #// array to pass a location {
    #// @type string $description The name of the location
    #// @type string $latitude    The latitude in decimal degrees notation, without the degree
    #// symbol. e.g.: 47.615200.
    #// @type string $longitude   The longitude in decimal degrees notation, without the degree
    #// symbol. e.g.: -122.341100.
    #// @type string $country     The ISO 3166-1 alpha-2 country code. e.g.: BR
    #// }
    #//
    def __init__(self, user_id_=None, user_location_=None):
        if user_location_ is None:
            user_location_ = False
        # end if
        
        self.user_id = absint(user_id_)
        self.user_location = user_location_
    # end def __init__
    #// 
    #// Gets data about events near a particular location.
    #// 
    #// Cached events will be immediately returned if the `user_location` property
    #// is set for the current user, and cached events exist for that location.
    #// 
    #// Otherwise, this method sends a request to the w.org Events API with location
    #// data. The API will send back a recognized location based on the data, along
    #// with nearby events.
    #// 
    #// The browser's request for events is proxied with this method, rather
    #// than having the browser make the request directly to api.wordpress.org,
    #// because it allows results to be cached server-side and shared with other
    #// users and sites in the network. This makes the process more efficient,
    #// since increasing the number of visits that get cached data means users
    #// don't have to wait as often; if the user's browser made the request
    #// directly, it would also need to make a second request to WP in order to
    #// pass the data for caching. Having WP make the request also introduces
    #// the opportunity to anonymize the IP before sending it to w.org, which
    #// mitigates possible privacy concerns.
    #// 
    #// @since 4.8.0
    #// 
    #// @param string $location_search Optional. City name to help determine the location.
    #// e.g., "Seattle". Default empty string.
    #// @param string $timezone        Optional. Timezone to help determine the location.
    #// Default empty string.
    #// @return array|WP_Error A WP_Error on failure; an array with location and events on
    #// success.
    #//
    def get_events(self, location_search_="", timezone_=""):
        
        
        cached_events_ = self.get_cached_events()
        if (not location_search_) and cached_events_:
            return cached_events_
        # end if
        #// Include an unmodified $wp_version.
        php_include_file(ABSPATH + WPINC + "/version.php", once=False)
        api_url_ = "http://api.wordpress.org/events/1.0/"
        request_args_ = self.get_request_args(location_search_, timezone_)
        request_args_["user-agent"] = "WordPress/" + wp_version_ + "; " + home_url("/")
        if wp_http_supports(Array("ssl")):
            api_url_ = set_url_scheme(api_url_, "https")
        # end if
        response_ = wp_remote_get(api_url_, request_args_)
        response_code_ = wp_remote_retrieve_response_code(response_)
        response_body_ = php_json_decode(wp_remote_retrieve_body(response_), True)
        response_error_ = None
        if is_wp_error(response_):
            response_error_ = response_
        elif 200 != response_code_:
            response_error_ = php_new_class("WP_Error", lambda : WP_Error("api-error", php_sprintf(__("Invalid API response code (%d)."), response_code_)))
        elif (not (php_isset(lambda : response_body_["location"]) and php_isset(lambda : response_body_["events"]))):
            response_error_ = php_new_class("WP_Error", lambda : WP_Error("api-invalid-response", response_body_["error"] if (php_isset(lambda : response_body_["error"])) else __("Unknown API error.")))
        # end if
        if is_wp_error(response_error_):
            return response_error_
        else:
            expiration_ = False
            if (php_isset(lambda : response_body_["ttl"])):
                expiration_ = response_body_["ttl"]
                response_body_["ttl"] = None
            # end if
            #// 
            #// The IP in the response is usually the same as the one that was sent
            #// in the request, but in some cases it is different. In those cases,
            #// it's important to reset it back to the IP from the request.
            #// 
            #// For example, if the IP sent in the request is private (e.g., 192.168.1.100),
            #// then the API will ignore that and use the corresponding public IP instead,
            #// and the public IP will get returned. If the public IP were saved, though,
            #// then get_cached_events() would always return `false`, because the transient
            #// would be generated based on the public IP when saving the cache, but generated
            #// based on the private IP when retrieving the cache.
            #//
            if (not php_empty(lambda : response_body_["location"]["ip"])):
                response_body_["location"]["ip"] = request_args_["body"]["ip"]
            # end if
            #// 
            #// The API doesn't return a description for latitude/longitude requests,
            #// but the description is already saved in the user location, so that
            #// one can be used instead.
            #//
            if self.coordinates_match(request_args_["body"], response_body_["location"]) and php_empty(lambda : response_body_["location"]["description"]):
                response_body_["location"]["description"] = self.user_location["description"]
            # end if
            self.cache_events(response_body_, expiration_)
            response_body_ = self.trim_events(response_body_)
            response_body_ = self.format_event_data_time(response_body_)
            return response_body_
        # end if
    # end def get_events
    #// 
    #// Builds an array of args to use in an HTTP request to the w.org Events API.
    #// 
    #// @since 4.8.0
    #// 
    #// @param string $search   Optional. City search string. Default empty string.
    #// @param string $timezone Optional. Timezone string. Default empty string.
    #// @return array The request args.
    #//
    def get_request_args(self, search_="", timezone_=""):
        
        
        args_ = Array({"number": 5, "ip": self.get_unsafe_client_ip()})
        #// 
        #// Include the minimal set of necessary arguments, in order to increase the
        #// chances of a cache-hit on the API side.
        #//
        if php_empty(lambda : search_) and (php_isset(lambda : self.user_location["latitude"]) and php_isset(lambda : self.user_location["longitude"])):
            args_["latitude"] = self.user_location["latitude"]
            args_["longitude"] = self.user_location["longitude"]
        else:
            args_["locale"] = get_user_locale(self.user_id)
            if timezone_:
                args_["timezone"] = timezone_
            # end if
            if search_:
                args_["location"] = search_
            # end if
        # end if
        #// Wrap the args in an array compatible with the second parameter of `wp_remote_get()`.
        return Array({"body": args_})
    # end def get_request_args
    #// 
    #// Determines the user's actual IP address and attempts to partially
    #// anonymize an IP address by converting it to a network ID.
    #// 
    #// Geolocating the network ID usually returns a similar location as the
    #// actual IP, but provides some privacy for the user.
    #// 
    #// $_SERVER['REMOTE_ADDR'] cannot be used in all cases, such as when the user
    #// is making their request through a proxy, or when the web server is behind
    #// a proxy. In those cases, $_SERVER['REMOTE_ADDR'] is set to the proxy address rather
    #// than the user's actual address.
    #// 
    #// Modified from https://stackoverflow.com/a/2031935/450127, MIT license.
    #// Modified from https://github.com/geertw/php-ip-anonymizer, MIT license.
    #// 
    #// SECURITY WARNING: This function is _NOT_ intended to be used in
    #// circumstances where the authenticity of the IP address matters. This does
    #// _NOT_ guarantee that the returned address is valid or accurate, and it can
    #// be easily spoofed.
    #// 
    #// @since 4.8.0
    #// 
    #// @return string|false The anonymized address on success; the given address
    #// or false on failure.
    #//
    @classmethod
    def get_unsafe_client_ip(self):
        
        
        client_ip_ = False
        #// In order of preference, with the best ones for this purpose first.
        address_headers_ = Array("HTTP_CLIENT_IP", "HTTP_X_FORWARDED_FOR", "HTTP_X_FORWARDED", "HTTP_X_CLUSTER_CLIENT_IP", "HTTP_FORWARDED_FOR", "HTTP_FORWARDED", "REMOTE_ADDR")
        for header_ in address_headers_:
            if php_array_key_exists(header_, PHP_SERVER):
                #// 
                #// HTTP_X_FORWARDED_FOR can contain a chain of comma-separated
                #// addresses. The first one is the original client. It can't be
                #// trusted for authenticity, but we don't need to for this purpose.
                #//
                address_chain_ = php_explode(",", PHP_SERVER[header_])
                client_ip_ = php_trim(address_chain_[0])
                break
            # end if
        # end for
        if (not client_ip_):
            return False
        # end if
        anon_ip_ = wp_privacy_anonymize_ip(client_ip_, True)
        if "0.0.0.0" == anon_ip_ or "::" == anon_ip_:
            return False
        # end if
        return anon_ip_
    # end def get_unsafe_client_ip
    #// 
    #// Test if two pairs of latitude/longitude coordinates match each other.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array $a The first pair, with indexes 'latitude' and 'longitude'.
    #// @param array $b The second pair, with indexes 'latitude' and 'longitude'.
    #// @return bool True if they match, false if they don't.
    #//
    def coordinates_match(self, a_=None, b_=None):
        
        
        if (not (php_isset(lambda : a_["latitude"]) and php_isset(lambda : a_["longitude"]) and php_isset(lambda : b_["latitude"]) and php_isset(lambda : b_["longitude"]))):
            return False
        # end if
        return a_["latitude"] == b_["latitude"] and a_["longitude"] == b_["longitude"]
    # end def coordinates_match
    #// 
    #// Generates a transient key based on user location.
    #// 
    #// This could be reduced to a one-liner in the calling functions, but it's
    #// intentionally a separate function because it's called from multiple
    #// functions, and having it abstracted keeps the logic consistent and DRY,
    #// which is less prone to errors.
    #// 
    #// @since 4.8.0
    #// 
    #// @param  array $location Should contain 'latitude' and 'longitude' indexes.
    #// @return bool|string false on failure, or a string on success.
    #//
    def get_events_transient_key(self, location_=None):
        
        
        key_ = False
        if (php_isset(lambda : location_["ip"])):
            key_ = "community-events-" + php_md5(location_["ip"])
        elif (php_isset(lambda : location_["latitude"]) and php_isset(lambda : location_["longitude"])):
            key_ = "community-events-" + php_md5(location_["latitude"] + location_["longitude"])
        # end if
        return key_
    # end def get_events_transient_key
    #// 
    #// Caches an array of events data from the Events API.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array    $events     Response body from the API request.
    #// @param int|bool $expiration Optional. Amount of time to cache the events. Defaults to false.
    #// @return bool true if events were cached; false if not.
    #//
    def cache_events(self, events_=None, expiration_=None):
        if expiration_ is None:
            expiration_ = False
        # end if
        
        set_ = False
        transient_key_ = self.get_events_transient_key(events_["location"])
        cache_expiration_ = absint(expiration_) if expiration_ else HOUR_IN_SECONDS * 12
        if transient_key_:
            set_ = set_site_transient(transient_key_, events_, cache_expiration_)
        # end if
        return set_
    # end def cache_events
    #// 
    #// Gets cached events.
    #// 
    #// @since 4.8.0
    #// 
    #// @return array|false An array containing `location` and `events` items
    #// on success, false on failure.
    #//
    def get_cached_events(self):
        
        
        cached_response_ = get_site_transient(self.get_events_transient_key(self.user_location))
        cached_response_ = self.trim_events(cached_response_)
        return self.format_event_data_time(cached_response_)
    # end def get_cached_events
    #// 
    #// Adds formatted date and time items for each event in an API response.
    #// 
    #// This has to be called after the data is pulled from the cache, because
    #// the cached events are shared by all users. If it was called before storing
    #// the cache, then all users would see the events in the localized data/time
    #// of the user who triggered the cache refresh, rather than their own.
    #// 
    #// @since 4.8.0
    #// 
    #// @param  array $response_body The response which contains the events.
    #// @return array The response with dates and times formatted.
    #//
    def format_event_data_time(self, response_body_=None):
        
        
        if (php_isset(lambda : response_body_["events"])):
            for key_,event_ in response_body_["events"].items():
                timestamp_ = strtotime(event_["date"])
                #// 
                #// The `date_format` option is not used because it's important
                #// in this context to keep the day of the week in the formatted date,
                #// so that users can tell at a glance if the event is on a day they
                #// are available, without having to open the link.
                #// 
                #// translators: Date format for upcoming events on the dashboard. Include the day of the week. See https://www.php.net/date
                formatted_date_ = date_i18n(__("l, M j, Y"), timestamp_)
                formatted_time_ = date_i18n(get_option("time_format"), timestamp_)
                if (php_isset(lambda : event_["end_date"])):
                    end_timestamp_ = strtotime(event_["end_date"])
                    formatted_end_date_ = date_i18n(__("l, M j, Y"), end_timestamp_)
                    if "meetup" != event_["type"] and formatted_end_date_ != formatted_date_:
                        #// translators: Upcoming events month format. See https://www.php.net/date
                        start_month_ = date_i18n(_x("F", "upcoming events month format"), timestamp_)
                        end_month_ = date_i18n(_x("F", "upcoming events month format"), end_timestamp_)
                        if start_month_ == end_month_:
                            formatted_date_ = php_sprintf(__("%1$s %2$dâ%3$d, %4$d"), start_month_, date_i18n(_x("j", "upcoming events day format"), timestamp_), date_i18n(_x("j", "upcoming events day format"), end_timestamp_), date_i18n(_x("Y", "upcoming events year format"), timestamp_))
                        else:
                            formatted_date_ = php_sprintf(__("%1$s %2$d â %3$s %4$d, %5$d"), start_month_, date_i18n(_x("j", "upcoming events day format"), timestamp_), end_month_, date_i18n(_x("j", "upcoming events day format"), end_timestamp_), date_i18n(_x("Y", "upcoming events year format"), timestamp_))
                        # end if
                        formatted_date_ = wp_maybe_decline_date(formatted_date_, "F j, Y")
                    # end if
                # end if
                response_body_["events"][key_]["formatted_date"] = formatted_date_
                response_body_["events"][key_]["formatted_time"] = formatted_time_
            # end for
        # end if
        return response_body_
    # end def format_event_data_time
    #// 
    #// Prepares the event list for presentation.
    #// 
    #// Discards expired events, and makes WordCamps "sticky." Attendees need more
    #// advanced notice about WordCamps than they do for meetups, so camps should
    #// appear in the list sooner. If a WordCamp is coming up, the API will "stick"
    #// it in the response, even if it wouldn't otherwise appear. When that happens,
    #// the event will be at the end of the list, and will need to be moved into a
    #// higher position, so that it doesn't get trimmed off.
    #// 
    #// @since 4.8.0
    #// @since 4.9.7 Stick a WordCamp to the final list.
    #// 
    #// @param  array $response_body The response body which contains the events.
    #// @return array The response body with events trimmed.
    #//
    def trim_events(self, response_body_=None):
        
        
        if (php_isset(lambda : response_body_["events"])):
            wordcamps_ = Array()
            today_ = current_time("Y-m-d")
            for key_,event_ in response_body_["events"].items():
                #// 
                #// Skip WordCamps, because they might be multi-day events.
                #// Save a copy so they can be pinned later.
                #//
                if "wordcamp" == event_["type"]:
                    wordcamps_[-1] = event_
                    continue
                # end if
                #// We don't get accurate time with timezone from API, so we only take the date part (Y-m-d).
                event_date_ = php_substr(event_["date"], 0, 10)
                if today_ > event_date_:
                    response_body_["events"][key_] = None
                # end if
            # end for
            response_body_["events"] = php_array_slice(response_body_["events"], 0, 3)
            trimmed_event_types_ = wp_list_pluck(response_body_["events"], "type")
            #// Make sure the soonest upcoming WordCamp is pinned in the list.
            if (not php_in_array("wordcamp", trimmed_event_types_)) and wordcamps_:
                php_array_pop(response_body_["events"])
                php_array_push(response_body_["events"], wordcamps_[0])
            # end if
        # end if
        return response_body_
    # end def trim_events
    #// 
    #// Logs responses to Events API requests.
    #// 
    #// @since 4.8.0
    #// @deprecated 4.9.0 Use a plugin instead. See #41217 for an example.
    #// 
    #// @param string $message A description of what occurred.
    #// @param array  $details Details that provide more context for the
    #// log entry.
    #//
    def maybe_log_events_response(self, message_=None, details_=None):
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.9.0")
        if (not WP_DEBUG_LOG):
            return
        # end if
        php_error_log(php_sprintf("%s: %s. Details: %s", inspect.currentframe().f_code.co_name, php_trim(message_, "."), wp_json_encode(details_)))
    # end def maybe_log_events_response
# end class WP_Community_Events
