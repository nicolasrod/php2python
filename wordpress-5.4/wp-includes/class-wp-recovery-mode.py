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
#// Error Protection API: WP_Recovery_Mode class
#// 
#// @package WordPress
#// @since 5.2.0
#// 
#// 
#// Core class used to implement Recovery Mode.
#// 
#// @since 5.2.0
#//
class WP_Recovery_Mode():
    EXIT_ACTION = "exit_recovery_mode"
    cookie_service = Array()
    key_service = Array()
    link_service = Array()
    email_service = Array()
    is_initialized = False
    is_active = False
    session_id = ""
    #// 
    #// WP_Recovery_Mode constructor.
    #// 
    #// @since 5.2.0
    #//
    def __init__(self):
        
        self.cookie_service = php_new_class("WP_Recovery_Mode_Cookie_Service", lambda : WP_Recovery_Mode_Cookie_Service())
        self.key_service = php_new_class("WP_Recovery_Mode_Key_Service", lambda : WP_Recovery_Mode_Key_Service())
        self.link_service = php_new_class("WP_Recovery_Mode_Link_Service", lambda : WP_Recovery_Mode_Link_Service(self.cookie_service, self.key_service))
        self.email_service = php_new_class("WP_Recovery_Mode_Email_Service", lambda : WP_Recovery_Mode_Email_Service(self.link_service))
    # end def __init__
    #// 
    #// Initialize recovery mode for the current request.
    #// 
    #// @since 5.2.0
    #//
    def initialize(self):
        
        self.is_initialized = True
        add_action("wp_logout", Array(self, "exit_recovery_mode"))
        add_action("login_form_" + self.EXIT_ACTION, Array(self, "handle_exit_recovery_mode"))
        add_action("recovery_mode_clean_expired_keys", Array(self, "clean_expired_keys"))
        if (not wp_next_scheduled("recovery_mode_clean_expired_keys")) and (not wp_installing()):
            wp_schedule_event(time(), "daily", "recovery_mode_clean_expired_keys")
        # end if
        if php_defined("WP_RECOVERY_MODE_SESSION_ID"):
            self.is_active = True
            self.session_id = WP_RECOVERY_MODE_SESSION_ID
            return
        # end if
        if self.cookie_service.is_cookie_set():
            self.handle_cookie()
            return
        # end if
        self.link_service.handle_begin_link(self.get_link_ttl())
    # end def initialize
    #// 
    #// Checks whether recovery mode is active.
    #// 
    #// This will not change after recovery mode has been initialized. {@see WP_Recovery_Mode::run()}.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool True if recovery mode is active, false otherwise.
    #//
    def is_active(self):
        
        return self.is_active
    # end def is_active
    #// 
    #// Gets the recovery mode session ID.
    #// 
    #// @since 5.2.0
    #// 
    #// @return string The session ID if recovery mode is active, empty string otherwise.
    #//
    def get_session_id(self):
        
        return self.session_id
    # end def get_session_id
    #// 
    #// Checks whether recovery mode has been initialized.
    #// 
    #// Recovery mode should not be used until this point. Initialization happens immediately before loading plugins.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool
    #//
    def is_initialized(self):
        
        return self.is_initialized
    # end def is_initialized
    #// 
    #// Handles a fatal error occurring.
    #// 
    #// The calling API should immediately die() after calling this function.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $error Error details from {@see error_get_last()}
    #// @return true|WP_Error True if the error was handled and headers have already been sent.
    #// Or the request will exit to try and catch multiple errors at once.
    #// WP_Error if an error occurred preventing it from being handled.
    #//
    def handle_error(self, error=None):
        
        extension = self.get_extension_for_error(error)
        if (not extension) or self.is_network_plugin(extension):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_source", __("Error not caused by a plugin or theme.")))
        # end if
        if (not self.is_active()):
            if (not is_protected_endpoint()):
                return php_new_class("WP_Error", lambda : WP_Error("non_protected_endpoint", __("Error occurred on a non-protected endpoint.")))
            # end if
            if (not php_function_exists("wp_generate_password")):
                php_include_file(ABSPATH + WPINC + "/pluggable.php", once=True)
            # end if
            return self.email_service.maybe_send_recovery_mode_email(self.get_email_rate_limit(), error, extension)
        # end if
        if (not self.store_error(error)):
            return php_new_class("WP_Error", lambda : WP_Error("storage_error", __("Failed to store the error.")))
        # end if
        if php_headers_sent():
            return True
        # end if
        self.redirect_protected()
    # end def handle_error
    #// 
    #// Ends the current recovery mode session.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool True on success, false on failure.
    #//
    def exit_recovery_mode(self):
        
        if (not self.is_active()):
            return False
        # end if
        self.email_service.clear_rate_limit()
        self.cookie_service.clear_cookie()
        wp_paused_plugins().delete_all()
        wp_paused_themes().delete_all()
        return True
    # end def exit_recovery_mode
    #// 
    #// Handles a request to exit Recovery Mode.
    #// 
    #// @since 5.2.0
    #//
    def handle_exit_recovery_mode(self):
        
        redirect_to = wp_get_referer()
        #// Safety check in case referrer returns false.
        if (not redirect_to):
            redirect_to = admin_url() if is_user_logged_in() else home_url()
        # end if
        if (not self.is_active()):
            wp_safe_redirect(redirect_to)
            php_exit(0)
        # end if
        if (not (php_isset(lambda : PHP_REQUEST["action"]))) or self.EXIT_ACTION != PHP_REQUEST["action"]:
            return
        # end if
        if (not (php_isset(lambda : PHP_REQUEST["_wpnonce"]))) or (not wp_verify_nonce(PHP_REQUEST["_wpnonce"], self.EXIT_ACTION)):
            wp_die(__("Exit recovery mode link expired."), 403)
        # end if
        if (not self.exit_recovery_mode()):
            wp_die(__("Failed to exit recovery mode. Please try again later."))
        # end if
        wp_safe_redirect(redirect_to)
        php_exit(0)
    # end def handle_exit_recovery_mode
    #// 
    #// Cleans any recovery mode keys that have expired according to the link TTL.
    #// 
    #// Executes on a daily cron schedule.
    #// 
    #// @since 5.2.0
    #//
    def clean_expired_keys(self):
        
        self.key_service.clean_expired_keys(self.get_link_ttl())
    # end def clean_expired_keys
    #// 
    #// Handles checking for the recovery mode cookie and validating it.
    #// 
    #// @since 5.2.0
    #//
    def handle_cookie(self):
        
        validated = self.cookie_service.validate_cookie()
        if is_wp_error(validated):
            self.cookie_service.clear_cookie()
            validated.add_data(Array({"status": 403}))
            wp_die(validated)
        # end if
        session_id = self.cookie_service.get_session_id_from_cookie()
        if is_wp_error(session_id):
            self.cookie_service.clear_cookie()
            session_id.add_data(Array({"status": 403}))
            wp_die(session_id)
        # end if
        self.is_active = True
        self.session_id = session_id
    # end def handle_cookie
    #// 
    #// Gets the rate limit between sending new recovery mode email links.
    #// 
    #// @since 5.2.0
    #// 
    #// @return int Rate limit in seconds.
    #//
    def get_email_rate_limit(self):
        
        #// 
        #// Filter the rate limit between sending new recovery mode email links.
        #// 
        #// @since 5.2.0
        #// 
        #// @param int $rate_limit Time to wait in seconds. Defaults to 1 day.
        #//
        return apply_filters("recovery_mode_email_rate_limit", DAY_IN_SECONDS)
    # end def get_email_rate_limit
    #// 
    #// Gets the number of seconds the recovery mode link is valid for.
    #// 
    #// @since 5.2.0
    #// 
    #// @return int Interval in seconds.
    #//
    def get_link_ttl(self):
        
        rate_limit = self.get_email_rate_limit()
        valid_for = rate_limit
        #// 
        #// Filter the amount of time the recovery mode email link is valid for.
        #// 
        #// The ttl must be at least as long as the email rate limit.
        #// 
        #// @since 5.2.0
        #// 
        #// @param int $valid_for The number of seconds the link is valid for.
        #//
        valid_for = apply_filters("recovery_mode_email_link_ttl", valid_for)
        return php_max(valid_for, rate_limit)
    # end def get_link_ttl
    #// 
    #// Gets the extension that the error occurred in.
    #// 
    #// @since 5.2.0
    #// 
    #// @global array $wp_theme_directories
    #// 
    #// @param array  $error Error that was triggered.
    #// 
    #// @return array|false {
    #// @type string  $slug  The extension slug. This is the plugin or theme's directory.
    #// @type string  $type  The extension type. Either 'plugin' or 'theme'.
    #// }
    #//
    def get_extension_for_error(self, error=None):
        
        global wp_theme_directories
        php_check_if_defined("wp_theme_directories")
        if (not (php_isset(lambda : error["file"]))):
            return False
        # end if
        if (not php_defined("WP_PLUGIN_DIR")):
            return False
        # end if
        error_file = wp_normalize_path(error["file"])
        wp_plugin_dir = wp_normalize_path(WP_PLUGIN_DIR)
        if 0 == php_strpos(error_file, wp_plugin_dir):
            path = php_str_replace(wp_plugin_dir + "/", "", error_file)
            parts = php_explode("/", path)
            return Array({"type": "plugin", "slug": parts[0]})
        # end if
        if php_empty(lambda : wp_theme_directories):
            return False
        # end if
        for theme_directory in wp_theme_directories:
            theme_directory = wp_normalize_path(theme_directory)
            if 0 == php_strpos(error_file, theme_directory):
                path = php_str_replace(theme_directory + "/", "", error_file)
                parts = php_explode("/", path)
                return Array({"type": "theme", "slug": parts[0]})
            # end if
        # end for
        return False
    # end def get_extension_for_error
    #// 
    #// Checks whether the given extension a network activated plugin.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $extension Extension data.
    #// @return bool True if network plugin, false otherwise.
    #//
    def is_network_plugin(self, extension=None):
        
        if "plugin" != extension["type"]:
            return False
        # end if
        if (not is_multisite()):
            return False
        # end if
        network_plugins = wp_get_active_network_plugins()
        for plugin in network_plugins:
            if 0 == php_strpos(plugin, extension["slug"] + "/"):
                return True
            # end if
        # end for
        return False
    # end def is_network_plugin
    #// 
    #// Stores the given error so that the extension causing it is paused.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $error Error that was triggered.
    #// @return bool True if the error was stored successfully, false otherwise.
    #//
    def store_error(self, error=None):
        
        extension = self.get_extension_for_error(error)
        if (not extension):
            return False
        # end if
        for case in Switch(extension["type"]):
            if case("plugin"):
                return wp_paused_plugins().set(extension["slug"], error)
            # end if
            if case("theme"):
                return wp_paused_themes().set(extension["slug"], error)
            # end if
            if case():
                return False
            # end if
        # end for
    # end def store_error
    #// 
    #// Redirects the current request to allow recovering multiple errors in one go.
    #// 
    #// The redirection will only happen when on a protected endpoint.
    #// 
    #// It must be ensured that this method is only called when an error actually occurred and will not occur on the
    #// next request again. Otherwise it will create a redirect loop.
    #// 
    #// @since 5.2.0
    #//
    def redirect_protected(self):
        
        #// Pluggable is usually loaded after plugins, so we manually include it here for redirection functionality.
        if (not php_function_exists("wp_safe_redirect")):
            php_include_file(ABSPATH + WPINC + "/pluggable.php", once=True)
        # end if
        scheme = "https://" if is_ssl() else "http://"
        url = str(scheme) + str(PHP_SERVER["HTTP_HOST"]) + str(PHP_SERVER["REQUEST_URI"])
        wp_safe_redirect(url)
        php_exit(0)
    # end def redirect_protected
# end class WP_Recovery_Mode
