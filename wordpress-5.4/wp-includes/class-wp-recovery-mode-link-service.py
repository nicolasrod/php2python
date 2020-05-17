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
#// Error Protection API: WP_Recovery_Mode_Link_Handler class
#// 
#// @package WordPress
#// @since 5.2.0
#// 
#// 
#// Core class used to generate and handle recovery mode links.
#// 
#// @since 5.2.0
#//
class WP_Recovery_Mode_Link_Service():
    LOGIN_ACTION_ENTER = "enter_recovery_mode"
    LOGIN_ACTION_ENTERED = "entered_recovery_mode"
    #// 
    #// Service to generate and validate recovery mode keys.
    #// 
    #// @since 5.2.0
    #// @var WP_Recovery_Mode_Key_Service
    #//
    key_service = Array()
    #// 
    #// Service to handle cookies.
    #// 
    #// @since 5.2.0
    #// @var WP_Recovery_Mode_Cookie_Service
    #//
    cookie_service = Array()
    #// 
    #// WP_Recovery_Mode_Link_Service constructor.
    #// 
    #// @since 5.2.0
    #// 
    #// @param WP_Recovery_Mode_Cookie_Service $cookie_service Service to handle setting the recovery mode cookie.
    #// @param WP_Recovery_Mode_Key_Service    $key_service    Service to handle generating recovery mode keys.
    #//
    def __init__(self, cookie_service_=None, key_service_=None):
        
        
        self.cookie_service = cookie_service_
        self.key_service = key_service_
    # end def __init__
    #// 
    #// Generates a URL to begin recovery mode.
    #// 
    #// Only one recovery mode URL can may be valid at the same time.
    #// 
    #// @since 5.2.0
    #// 
    #// @return string Generated URL.
    #//
    def generate_url(self):
        
        
        token_ = self.key_service.generate_recovery_mode_token()
        key_ = self.key_service.generate_and_store_recovery_mode_key(token_)
        return self.get_recovery_mode_begin_url(token_, key_)
    # end def generate_url
    #// 
    #// Enters recovery mode when the user hits wp-login.php with a valid recovery mode link.
    #// 
    #// @since 5.2.0
    #// 
    #// @param int $ttl Number of seconds the link should be valid for.
    #//
    def handle_begin_link(self, ttl_=None):
        
        
        if (not (php_isset(lambda : PHP_GLOBALS["pagenow"]))) or "wp-login.php" != PHP_GLOBALS["pagenow"]:
            return
        # end if
        if (not (php_isset(lambda : PHP_REQUEST["action"]) and php_isset(lambda : PHP_REQUEST["rm_token"]) and php_isset(lambda : PHP_REQUEST["rm_key"]))) or self.LOGIN_ACTION_ENTER != PHP_REQUEST["action"]:
            return
        # end if
        if (not php_function_exists("wp_generate_password")):
            php_include_file(ABSPATH + WPINC + "/pluggable.php", once=True)
        # end if
        validated_ = self.key_service.validate_recovery_mode_key(PHP_REQUEST["rm_token"], PHP_REQUEST["rm_key"], ttl_)
        if is_wp_error(validated_):
            wp_die(validated_, "")
        # end if
        self.cookie_service.set_cookie()
        url_ = add_query_arg("action", self.LOGIN_ACTION_ENTERED, wp_login_url())
        wp_redirect(url_)
        php_exit(0)
    # end def handle_begin_link
    #// 
    #// Gets a URL to begin recovery mode.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $token Recovery Mode token created by {@see generate_recovery_mode_token()}.
    #// @param string $key   Recovery Mode key created by {@see generate_and_store_recovery_mode_key()}.
    #// @return string Recovery mode begin URL.
    #//
    def get_recovery_mode_begin_url(self, token_=None, key_=None):
        
        
        url_ = add_query_arg(Array({"action": self.LOGIN_ACTION_ENTER, "rm_token": token_, "rm_key": key_}), wp_login_url())
        #// 
        #// Filter the URL to begin recovery mode.
        #// 
        #// @since 5.2.0
        #// 
        #// @param string $url   The generated recovery mode begin URL.
        #// @param string $token The token used to identify the key.
        #// @param string $key   The recovery mode key.
        #//
        return apply_filters("recovery_mode_begin_url", url_, token_, key_)
    # end def get_recovery_mode_begin_url
# end class WP_Recovery_Mode_Link_Service
