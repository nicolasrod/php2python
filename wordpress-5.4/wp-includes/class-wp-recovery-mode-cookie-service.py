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
#// Error Protection API: WP_Recovery_Mode_Cookie_Service class
#// 
#// @package WordPress
#// @since 5.2.0
#// 
#// 
#// Core class used to set, validate, and clear cookies that identify a Recovery Mode session.
#// 
#// @since 5.2.0
#//
class WP_Recovery_Mode_Cookie_Service():
    #// 
    #// Checks whether the recovery mode cookie is set.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool True if the cookie is set, false otherwise.
    #//
    def is_cookie_set(self):
        
        return (not php_empty(lambda : PHP_COOKIE[RECOVERY_MODE_COOKIE]))
    # end def is_cookie_set
    #// 
    #// Sets the recovery mode cookie.
    #// 
    #// This must be immediately followed by exiting the request.
    #// 
    #// @since 5.2.0
    #//
    def set_cookie(self):
        
        value = self.generate_cookie()
        #// 
        #// Filter the length of time a Recovery Mode cookie is valid for.
        #// 
        #// @since 5.2.0
        #// 
        #// @param int $length Length in seconds.
        #//
        length = apply_filters("recovery_mode_cookie_length", WEEK_IN_SECONDS)
        expire = time() + length
        setcookie(RECOVERY_MODE_COOKIE, value, expire, COOKIEPATH, COOKIE_DOMAIN, is_ssl(), True)
        if COOKIEPATH != SITECOOKIEPATH:
            setcookie(RECOVERY_MODE_COOKIE, value, expire, SITECOOKIEPATH, COOKIE_DOMAIN, is_ssl(), True)
        # end if
    # end def set_cookie
    #// 
    #// Clears the recovery mode cookie.
    #// 
    #// @since 5.2.0
    #//
    def clear_cookie(self):
        
        setcookie(RECOVERY_MODE_COOKIE, " ", time() - YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN)
        setcookie(RECOVERY_MODE_COOKIE, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH, COOKIE_DOMAIN)
    # end def clear_cookie
    #// 
    #// Validates the recovery mode cookie.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $cookie Optionally specify the cookie string.
    #// If omitted, it will be retrieved from the super global.
    #// @return true|WP_Error True on success, error object on failure.
    #//
    def validate_cookie(self, cookie=""):
        
        if (not cookie):
            if php_empty(lambda : PHP_COOKIE[RECOVERY_MODE_COOKIE]):
                return php_new_class("WP_Error", lambda : WP_Error("no_cookie", __("No cookie present.")))
            # end if
            cookie = PHP_COOKIE[RECOVERY_MODE_COOKIE]
        # end if
        parts = self.parse_cookie(cookie)
        if is_wp_error(parts):
            return parts
        # end if
        created_at, random, signature = parts
        if (not ctype_digit(created_at)):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_created_at", __("Invalid cookie format.")))
        # end if
        #// This filter is documented in wp-includes/class-wp-recovery-mode-cookie-service.php
        length = apply_filters("recovery_mode_cookie_length", WEEK_IN_SECONDS)
        if time() > created_at + length:
            return php_new_class("WP_Error", lambda : WP_Error("expired", __("Cookie expired.")))
        # end if
        to_sign = php_sprintf("recovery_mode|%s|%s", created_at, random)
        hashed = self.recovery_mode_hash(to_sign)
        if (not hash_equals(signature, hashed)):
            return php_new_class("WP_Error", lambda : WP_Error("signature_mismatch", __("Invalid cookie.")))
        # end if
        return True
    # end def validate_cookie
    #// 
    #// Gets the session identifier from the cookie.
    #// 
    #// The cookie should be validated before calling this API.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $cookie Optionally specify the cookie string.
    #// If omitted, it will be retrieved from the super global.
    #// @return string|WP_Error Session ID on success, or error object on failure.
    #//
    def get_session_id_from_cookie(self, cookie=""):
        
        if (not cookie):
            if php_empty(lambda : PHP_COOKIE[RECOVERY_MODE_COOKIE]):
                return php_new_class("WP_Error", lambda : WP_Error("no_cookie", __("No cookie present.")))
            # end if
            cookie = PHP_COOKIE[RECOVERY_MODE_COOKIE]
        # end if
        parts = self.parse_cookie(cookie)
        if is_wp_error(parts):
            return parts
        # end if
        random = parts
        return sha1(random)
    # end def get_session_id_from_cookie
    #// 
    #// Parses the cookie into its four parts.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $cookie Cookie content.
    #// @return array|WP_Error Cookie parts array, or error object on failure.
    #//
    def parse_cookie(self, cookie=None):
        
        cookie = php_base64_decode(cookie)
        parts = php_explode("|", cookie)
        if 4 != php_count(parts):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_format", __("Invalid cookie format.")))
        # end if
        return parts
    # end def parse_cookie
    #// 
    #// Generates the recovery mode cookie value.
    #// 
    #// The cookie is a base64 encoded string with the following format:
    #// 
    #// recovery_mode|iat|rand|signature
    #// 
    #// Where "recovery_mode" is a constant string,
    #// iat is the time the cookie was generated at,
    #// rand is a randomly generated password that is also used as a session identifier
    #// and signature is an hmac of the preceding 3 parts.
    #// 
    #// @since 5.2.0
    #// 
    #// @return string Generated cookie content.
    #//
    def generate_cookie(self):
        
        to_sign = php_sprintf("recovery_mode|%s|%s", time(), wp_generate_password(20, False))
        signed = self.recovery_mode_hash(to_sign)
        return php_base64_encode(php_sprintf("%s|%s", to_sign, signed))
    # end def generate_cookie
    #// 
    #// Gets a form of `wp_hash()` specific to Recovery Mode.
    #// 
    #// We cannot use `wp_hash()` because it is defined in `pluggable.php` which is not loaded until after plugins are loaded,
    #// which is too late to verify the recovery mode cookie.
    #// 
    #// This tries to use the `AUTH` salts first, but if they aren't valid specific salts will be generated and stored.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $data Data to hash.
    #// @return string|false The hashed $data, or false on failure.
    #//
    def recovery_mode_hash(self, data=None):
        
        if (not php_defined("AUTH_KEY")) or AUTH_KEY == "put your unique phrase here":
            auth_key = get_site_option("recovery_mode_auth_key")
            if (not auth_key):
                if (not php_function_exists("wp_generate_password")):
                    php_include_file(ABSPATH + WPINC + "/pluggable.php", once=True)
                # end if
                auth_key = wp_generate_password(64, True, True)
                update_site_option("recovery_mode_auth_key", auth_key)
            # end if
        else:
            auth_key = AUTH_KEY
        # end if
        if (not php_defined("AUTH_SALT")) or AUTH_SALT == "put your unique phrase here" or AUTH_SALT == auth_key:
            auth_salt = get_site_option("recovery_mode_auth_salt")
            if (not auth_salt):
                if (not php_function_exists("wp_generate_password")):
                    php_include_file(ABSPATH + WPINC + "/pluggable.php", once=True)
                # end if
                auth_salt = wp_generate_password(64, True, True)
                update_site_option("recovery_mode_auth_salt", auth_salt)
            # end if
        else:
            auth_salt = AUTH_SALT
        # end if
        secret = auth_key + auth_salt
        return hash_hmac("sha1", data, secret)
    # end def recovery_mode_hash
# end class WP_Recovery_Mode_Cookie_Service
