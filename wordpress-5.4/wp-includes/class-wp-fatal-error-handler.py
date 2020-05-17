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
#// Error Protection API: WP_Fatal_Error_Handler class
#// 
#// @package WordPress
#// @since 5.2.0
#// 
#// 
#// Core class used as the default shutdown handler for fatal errors.
#// 
#// A drop-in 'fatal-error-handler.php' can be used to override the instance of this class and use a custom
#// implementation for the fatal error handler that WordPress registers. The custom class should extend this class and
#// can override its methods individually as necessary. The file must return the instance of the class that should be
#// registered.
#// 
#// @since 5.2.0
#//
class WP_Fatal_Error_Handler():
    #// 
    #// Runs the shutdown handler.
    #// 
    #// This method is registered via `register_shutdown_function()`.
    #// 
    #// @since 5.2.0
    #//
    def handle(self):
        
        
        if php_defined("WP_SANDBOX_SCRAPING") and WP_SANDBOX_SCRAPING:
            return
        # end if
        try: 
            #// Bail if no error found.
            error_ = self.detect_error()
            if (not error_):
                return
            # end if
            if (not (php_isset(lambda : PHP_GLOBALS["wp_locale"]))) and php_function_exists("load_default_textdomain"):
                load_default_textdomain()
            # end if
            handled_ = False
            if (not is_multisite()) and wp_recovery_mode().is_initialized():
                handled_ = wp_recovery_mode().handle_error(error_)
            # end if
            #// Display the PHP error template if headers not sent.
            if is_admin() or (not php_headers_sent()):
                self.display_error_template(error_, handled_)
            # end if
        except Exception as e_:
            pass
        # end try
    # end def handle
    #// 
    #// Detects the error causing the crash if it should be handled.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array|null Error that was triggered, or null if no error received or if the error should not be handled.
    #//
    def detect_error(self):
        
        
        error_ = error_get_last()
        #// No error, just skip the error handling code.
        if None == error_:
            return None
        # end if
        #// Bail if this error should not be handled.
        if (not self.should_handle_error(error_)):
            return None
        # end if
        return error_
    # end def detect_error
    #// 
    #// Determines whether we are dealing with an error that WordPress should handle
    #// in order to protect the admin backend against WSODs.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $error Error information retrieved from error_get_last().
    #// @return bool Whether WordPress should handle this error.
    #//
    def should_handle_error(self, error_=None):
        
        
        error_types_to_handle_ = Array(E_ERROR, E_PARSE, E_USER_ERROR, E_COMPILE_ERROR, E_RECOVERABLE_ERROR)
        if (php_isset(lambda : error_["type"])) and php_in_array(error_["type"], error_types_to_handle_, True):
            return True
        # end if
        #// 
        #// Filters whether a given thrown error should be handled by the fatal error handler.
        #// 
        #// This filter is only fired if the error is not already configured to be handled by WordPress core. As such,
        #// it exclusively allows adding further rules for which errors should be handled, but not removing existing
        #// ones.
        #// 
        #// @since 5.2.0
        #// 
        #// @param bool  $should_handle_error Whether the error should be handled by the fatal error handler.
        #// @param array $error               Error information retrieved from error_get_last().
        #//
        return php_bool(apply_filters("wp_should_handle_php_error", False, error_))
    # end def should_handle_error
    #// 
    #// Displays the PHP error template and sends the HTTP status code, typically 500.
    #// 
    #// A drop-in 'php-error.php' can be used as a custom template. This drop-in should control the HTTP status code and
    #// print the HTML markup indicating that a PHP error occurred. Note that this drop-in may potentially be executed
    #// very early in the WordPress bootstrap process, so any core functions used that are not part of
    #// `wp-includes/load.php` should be checked for before being called.
    #// 
    #// If no such drop-in is available, this will call {@see WP_Fatal_Error_Handler::display_default_error_template()}.
    #// 
    #// @since 5.2.0
    #// @since 5.3.0 The `$handled` parameter was added.
    #// 
    #// @param array         $error   Error information retrieved from `error_get_last()`.
    #// @param true|WP_Error $handled Whether Recovery Mode handled the fatal error.
    #//
    def display_error_template(self, error_=None, handled_=None):
        
        
        if php_defined("WP_CONTENT_DIR"):
            #// Load custom PHP error template, if present.
            php_error_pluggable_ = WP_CONTENT_DIR + "/php-error.php"
            if php_is_readable(php_error_pluggable_):
                php_include_file(php_error_pluggable_, once=True)
                return
            # end if
        # end if
        #// Otherwise, display the default error template.
        self.display_default_error_template(error_, handled_)
    # end def display_error_template
    #// 
    #// Displays the default PHP error template.
    #// 
    #// This method is called conditionally if no 'php-error.php' drop-in is available.
    #// 
    #// It calls {@see wp_die()} with a message indicating that the site is experiencing technical difficulties and a
    #// login link to the admin backend. The {@see 'wp_php_error_message'} and {@see 'wp_php_error_args'} filters can
    #// be used to modify these parameters.
    #// 
    #// @since 5.2.0
    #// @since 5.3.0 The `$handled` parameter was added.
    #// 
    #// @param array         $error   Error information retrieved from `error_get_last()`.
    #// @param true|WP_Error $handled Whether Recovery Mode handled the fatal error.
    #//
    def display_default_error_template(self, error_=None, handled_=None):
        
        
        if (not php_function_exists("__")):
            wp_load_translations_early()
        # end if
        if (not php_function_exists("wp_die")):
            php_include_file(ABSPATH + WPINC + "/functions.php", once=True)
        # end if
        if (not php_class_exists("WP_Error")):
            php_include_file(ABSPATH + WPINC + "/class-wp-error.php", once=True)
        # end if
        if True == handled_ and wp_is_recovery_mode():
            message_ = __("There has been a critical error on your website, putting it in recovery mode. Please check the Themes and Plugins screens for more details. If you just installed or updated a theme or plugin, check the relevant page for that first.")
        elif is_protected_endpoint():
            message_ = __("There has been a critical error on your website. Please check your site admin email inbox for instructions.")
        else:
            message_ = __("There has been a critical error on your website.")
        # end if
        message_ = php_sprintf("<p>%s</p><p><a href=\"%s\">%s</a></p>", message_, __("https://wordpress.org/support/article/debugging-in-wordpress/"), __("Learn more about debugging in WordPress."))
        args_ = Array({"response": 500, "exit": False})
        #// 
        #// Filters the message that the default PHP error template displays.
        #// 
        #// @since 5.2.0
        #// 
        #// @param string $message HTML error message to display.
        #// @param array  $error   Error information retrieved from `error_get_last()`.
        #//
        message_ = apply_filters("wp_php_error_message", message_, error_)
        #// 
        #// Filters the arguments passed to {@see wp_die()} for the default PHP error template.
        #// 
        #// @since 5.2.0
        #// 
        #// @param array $args Associative array of arguments passed to `wp_die()`. By default these contain a
        #// 'response' key, and optionally 'link_url' and 'link_text' keys.
        #// @param array $error Error information retrieved from `error_get_last()`.
        #//
        args_ = apply_filters("wp_php_error_args", args_, error_)
        wp_error_ = php_new_class("WP_Error", lambda : WP_Error("internal_server_error", message_, Array({"error": error_})))
        wp_die(wp_error_, "", args_)
    # end def display_default_error_template
# end class WP_Fatal_Error_Handler
