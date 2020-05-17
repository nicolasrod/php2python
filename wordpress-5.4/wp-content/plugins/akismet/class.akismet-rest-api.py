#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
class Akismet_REST_API():
    #// 
    #// Register the REST API routes.
    #//
    @classmethod
    def init(self):
        
        
        if (not php_function_exists("register_rest_route")):
            #// The REST API wasn't integrated into core until 4.4, and we support 4.0+ (for now).
            return False
        # end if
        register_rest_route("akismet/v1", "/key", Array(Array({"methods": WP_REST_Server.READABLE, "permission_callback": Array("Akismet_REST_API", "privileged_permission_callback"), "callback": Array("Akismet_REST_API", "get_key")}), Array({"methods": WP_REST_Server.EDITABLE, "permission_callback": Array("Akismet_REST_API", "privileged_permission_callback"), "callback": Array("Akismet_REST_API", "set_key"), "args": Array({"key": Array({"required": True, "type": "string", "sanitize_callback": Array("Akismet_REST_API", "sanitize_key"), "description": __("A 12-character Akismet API key. Available at akismet.com/get/", "akismet")})})}), Array({"methods": WP_REST_Server.DELETABLE, "permission_callback": Array("Akismet_REST_API", "privileged_permission_callback"), "callback": Array("Akismet_REST_API", "delete_key")})))
        register_rest_route("akismet/v1", "/settings/", Array(Array({"methods": WP_REST_Server.READABLE, "permission_callback": Array("Akismet_REST_API", "privileged_permission_callback"), "callback": Array("Akismet_REST_API", "get_settings")}), Array({"methods": WP_REST_Server.EDITABLE, "permission_callback": Array("Akismet_REST_API", "privileged_permission_callback"), "callback": Array("Akismet_REST_API", "set_boolean_settings"), "args": Array({"akismet_strictness": Array({"required": False, "type": "boolean", "description": __("If true, Akismet will automatically discard the worst spam automatically rather than putting it in the spam folder.", "akismet")})}, {"akismet_show_user_comments_approved": Array({"required": False, "type": "boolean", "description": __("If true, show the number of approved comments beside each comment author in the comments list page.", "akismet")})})})))
        register_rest_route("akismet/v1", "/stats", Array({"methods": WP_REST_Server.READABLE, "permission_callback": Array("Akismet_REST_API", "privileged_permission_callback"), "callback": Array("Akismet_REST_API", "get_stats"), "args": Array({"interval": Array({"required": False, "type": "string", "sanitize_callback": Array("Akismet_REST_API", "sanitize_interval"), "description": __("The time period for which to retrieve stats. Options: 60-days, 6-months, all", "akismet"), "default": "all"})})}))
        register_rest_route("akismet/v1", "/stats/(?P<interval>[\\w+])", Array({"args": Array({"interval": Array({"description": __("The time period for which to retrieve stats. Options: 60-days, 6-months, all", "akismet"), "type": "string"})})}, Array({"methods": WP_REST_Server.READABLE, "permission_callback": Array("Akismet_REST_API", "privileged_permission_callback"), "callback": Array("Akismet_REST_API", "get_stats")})))
        register_rest_route("akismet/v1", "/alert", Array(Array({"methods": WP_REST_Server.READABLE, "permission_callback": Array("Akismet_REST_API", "remote_call_permission_callback"), "callback": Array("Akismet_REST_API", "get_alert"), "args": Array({"key": Array({"required": False, "type": "string", "sanitize_callback": Array("Akismet_REST_API", "sanitize_key"), "description": __("A 12-character Akismet API key. Available at akismet.com/get/", "akismet")})})}), Array({"methods": WP_REST_Server.EDITABLE, "permission_callback": Array("Akismet_REST_API", "remote_call_permission_callback"), "callback": Array("Akismet_REST_API", "set_alert"), "args": Array({"key": Array({"required": False, "type": "string", "sanitize_callback": Array("Akismet_REST_API", "sanitize_key"), "description": __("A 12-character Akismet API key. Available at akismet.com/get/", "akismet")})})}), Array({"methods": WP_REST_Server.DELETABLE, "permission_callback": Array("Akismet_REST_API", "remote_call_permission_callback"), "callback": Array("Akismet_REST_API", "delete_alert"), "args": Array({"key": Array({"required": False, "type": "string", "sanitize_callback": Array("Akismet_REST_API", "sanitize_key"), "description": __("A 12-character Akismet API key. Available at akismet.com/get/", "akismet")})})})))
    # end def init
    #// 
    #// Get the current Akismet API key.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def get_key(self, request_=None):
        if request_ is None:
            request_ = None
        # end if
        
        return rest_ensure_response(Akismet.get_api_key())
    # end def get_key
    #// 
    #// Set the API key, if possible.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def set_key(self, request_=None):
        
        
        if php_defined("WPCOM_API_KEY"):
            return rest_ensure_response(php_new_class("WP_Error", lambda : WP_Error("hardcoded_key", __("This site's API key is hardcoded and cannot be changed via the API.", "akismet"), Array({"status": 409}))))
        # end if
        new_api_key_ = request_.get_param("key")
        if (not self.key_is_valid(new_api_key_)):
            return rest_ensure_response(php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("The value provided is not a valid and registered API key.", "akismet"), Array({"status": 400}))))
        # end if
        update_option("wordpress_api_key", new_api_key_)
        return self.get_key()
    # end def set_key
    #// 
    #// Unset the API key, if possible.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def delete_key(self, request_=None):
        
        
        if php_defined("WPCOM_API_KEY"):
            return rest_ensure_response(php_new_class("WP_Error", lambda : WP_Error("hardcoded_key", __("This site's API key is hardcoded and cannot be deleted.", "akismet"), Array({"status": 409}))))
        # end if
        delete_option("wordpress_api_key")
        return rest_ensure_response(True)
    # end def delete_key
    #// 
    #// Get the Akismet settings.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def get_settings(self, request_=None):
        if request_ is None:
            request_ = None
        # end if
        
        return rest_ensure_response(Array({"akismet_strictness": get_option("akismet_strictness", "1") == "1", "akismet_show_user_comments_approved": get_option("akismet_show_user_comments_approved", "1") == "1"}))
    # end def get_settings
    #// 
    #// Update the Akismet settings.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def set_boolean_settings(self, request_=None):
        
        
        for setting_key_ in Array("akismet_strictness", "akismet_show_user_comments_approved"):
            setting_value_ = request_.get_param(setting_key_)
            if php_is_null(setting_value_):
                continue
            # end if
            #// From 4.7+, WP core will ensure that these are always boolean
            #// values because they are registered with 'type' => 'boolean',
            #// but we need to do this ourselves for prior versions.
            setting_value_ = Akismet_REST_API.parse_boolean(setting_value_)
            update_option(setting_key_, "1" if setting_value_ else "0")
        # end for
        return self.get_settings()
    # end def set_boolean_settings
    #// 
    #// Parse a numeric or string boolean value into a boolean.
    #// 
    #// @param mixed $value The value to convert into a boolean.
    #// @return bool The converted value.
    #//
    @classmethod
    def parse_boolean(self, value_=None):
        
        
        for case in Switch(value_):
            if case(True):
                pass
            # end if
            if case("true"):
                pass
            # end if
            if case("1"):
                pass
            # end if
            if case(1):
                return True
            # end if
            if case(False):
                pass
            # end if
            if case("false"):
                pass
            # end if
            if case("0"):
                pass
            # end if
            if case(0):
                return False
            # end if
            if case():
                return php_bool(value_)
            # end if
        # end for
    # end def parse_boolean
    #// 
    #// Get the Akismet stats for a given time period.
    #// 
    #// Possible `interval` values:
    #// - all
    #// - 60-days
    #// - 6-months
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def get_stats(self, request_=None):
        
        
        api_key_ = Akismet.get_api_key()
        interval_ = request_.get_param("interval")
        stat_totals_ = Array()
        response_ = Akismet.http_post(Akismet.build_query(Array({"blog": get_option("home"), "key": api_key_, "from": interval_})), "get-stats")
        if (not php_empty(lambda : response_[1])):
            stat_totals_[interval_] = php_json_decode(response_[1])
        # end if
        return rest_ensure_response(stat_totals_)
    # end def get_stats
    #// 
    #// Get the current alert code and message. Alert codes are used to notify the site owner
    #// if there's a problem, like a connection issue between their site and the Akismet API,
    #// invalid requests being sent, etc.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def get_alert(self, request_=None):
        
        
        return rest_ensure_response(Array({"code": get_option("akismet_alert_code"), "message": get_option("akismet_alert_msg")}))
    # end def get_alert
    #// 
    #// Update the current alert code and message by triggering a call to the Akismet server.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def set_alert(self, request_=None):
        
        
        delete_option("akismet_alert_code")
        delete_option("akismet_alert_msg")
        #// Make a request so the most recent alert code and message are retrieved.
        Akismet.verify_key(Akismet.get_api_key())
        return self.get_alert(request_)
    # end def set_alert
    #// 
    #// Clear the current alert code and message.
    #// 
    #// @param WP_REST_Request $request
    #// @return WP_Error|WP_REST_Response
    #//
    @classmethod
    def delete_alert(self, request_=None):
        
        
        delete_option("akismet_alert_code")
        delete_option("akismet_alert_msg")
        return self.get_alert(request_)
    # end def delete_alert
    def key_is_valid(self, key_=None):
        
        
        response_ = Akismet.http_post(Akismet.build_query(Array({"key": key_, "blog": get_option("home")})), "verify-key")
        if response_[1] == "valid":
            return True
        # end if
        return False
    # end def key_is_valid
    @classmethod
    def privileged_permission_callback(self):
        
        
        return current_user_can("manage_options")
    # end def privileged_permission_callback
    #// 
    #// For calls that Akismet.com makes to the site to clear outdated alert codes, use the API key for authorization.
    #//
    @classmethod
    def remote_call_permission_callback(self, request_=None):
        
        
        local_key_ = Akismet.get_api_key()
        return local_key_ and php_strtolower(request_.get_param("key")) == php_strtolower(local_key_)
    # end def remote_call_permission_callback
    @classmethod
    def sanitize_interval(self, interval_=None, request_=None, param_=None):
        
        
        interval_ = php_trim(interval_)
        valid_intervals_ = Array("60-days", "6-months", "all")
        if (not php_in_array(interval_, valid_intervals_)):
            interval_ = "all"
        # end if
        return interval_
    # end def sanitize_interval
    @classmethod
    def sanitize_key(self, key_=None, request_=None, param_=None):
        
        
        return php_trim(key_)
    # end def sanitize_key
# end class Akismet_REST_API
