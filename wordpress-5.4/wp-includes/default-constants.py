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
#// Defines constants and global variables that can be overridden, generally in wp-config.php.
#// 
#// @package WordPress
#// 
#// 
#// Defines initial WordPress constants.
#// 
#// @see wp_debug_mode()
#// 
#// @since 3.0.0
#// 
#// @global int    $blog_id    The current site ID.
#// @global string $wp_version The WordPress version string.
#//
def wp_initial_constants(*args_):
    
    global blog_id
    php_check_if_defined("blog_id")
    #// #@+
    #// Constants for expressing human-readable data sizes in their respective number of bytes.
    #// 
    #// @since 4.4.0
    #//
    php_define("KB_IN_BYTES", 1024)
    php_define("MB_IN_BYTES", 1024 * KB_IN_BYTES)
    php_define("GB_IN_BYTES", 1024 * MB_IN_BYTES)
    php_define("TB_IN_BYTES", 1024 * GB_IN_BYTES)
    #// #@-
    #// Start of run timestamp.
    if (not php_defined("WP_START_TIMESTAMP")):
        php_define("WP_START_TIMESTAMP", php_microtime(True))
    # end if
    current_limit = php_ini_get("memory_limit")
    current_limit_int = wp_convert_hr_to_bytes(current_limit)
    #// Define memory limits.
    if (not php_defined("WP_MEMORY_LIMIT")):
        if False == wp_is_ini_value_changeable("memory_limit"):
            php_define("WP_MEMORY_LIMIT", current_limit)
        elif is_multisite():
            php_define("WP_MEMORY_LIMIT", "64M")
        else:
            php_define("WP_MEMORY_LIMIT", "40M")
        # end if
    # end if
    if (not php_defined("WP_MAX_MEMORY_LIMIT")):
        if False == wp_is_ini_value_changeable("memory_limit"):
            php_define("WP_MAX_MEMORY_LIMIT", current_limit)
        elif -1 == current_limit_int or current_limit_int > 268435456:
            php_define("WP_MAX_MEMORY_LIMIT", current_limit)
        else:
            php_define("WP_MAX_MEMORY_LIMIT", "256M")
        # end if
    # end if
    #// Set memory limits.
    wp_limit_int = wp_convert_hr_to_bytes(WP_MEMORY_LIMIT)
    if -1 != current_limit_int and -1 == wp_limit_int or wp_limit_int > current_limit_int:
        php_ini_set("memory_limit", WP_MEMORY_LIMIT)
    # end if
    if (not (php_isset(lambda : blog_id))):
        blog_id = 1
    # end if
    if (not php_defined("WP_CONTENT_DIR")):
        php_define("WP_CONTENT_DIR", ABSPATH + "wp-content")
        pass
    # end if
    #// Add define( 'WP_DEBUG', true ); to wp-config.php to enable display of notices during development.
    if (not php_defined("WP_DEBUG")):
        php_define("WP_DEBUG", False)
    # end if
    #// Add define( 'WP_DEBUG_DISPLAY', null ); to wp-config.php to use the globally configured setting
    #// for 'display_errors' and not force errors to be displayed. Use false to force 'display_errors' off.
    if (not php_defined("WP_DEBUG_DISPLAY")):
        php_define("WP_DEBUG_DISPLAY", True)
    # end if
    #// Add define( 'WP_DEBUG_LOG', true ); to enable error logging to wp-content/debug.log.
    if (not php_defined("WP_DEBUG_LOG")):
        php_define("WP_DEBUG_LOG", False)
    # end if
    if (not php_defined("WP_CACHE")):
        php_define("WP_CACHE", False)
    # end if
    #// Add define( 'SCRIPT_DEBUG', true ); to wp-config.php to enable loading of non-minified,
    #// non-concatenated scripts and stylesheets.
    if (not php_defined("SCRIPT_DEBUG")):
        if (not php_empty(lambda : PHP_GLOBALS["wp_version"])):
            develop_src = False != php_strpos(PHP_GLOBALS["wp_version"], "-src")
        else:
            develop_src = False
        # end if
        php_define("SCRIPT_DEBUG", develop_src)
    # end if
    #// 
    #// Private
    #//
    if (not php_defined("MEDIA_TRASH")):
        php_define("MEDIA_TRASH", False)
    # end if
    if (not php_defined("SHORTINIT")):
        php_define("SHORTINIT", False)
    # end if
    #// Constants for features added to WP that should short-circuit their plugin implementations.
    php_define("WP_FEATURE_BETTER_PASSWORDS", True)
    #// #@+
    #// Constants for expressing human-readable intervals
    #// in their respective number of seconds.
    #// 
    #// Please note that these values are approximate and are provided for convenience.
    #// For example, MONTH_IN_SECONDS wrongly assumes every month has 30 days and
    #// YEAR_IN_SECONDS does not take leap years into account.
    #// 
    #// If you need more accuracy please consider using the DateTime class (https://www.php.net/manual/en/class.datetime.php).
    #// 
    #// @since 3.5.0
    #// @since 4.4.0 Introduced `MONTH_IN_SECONDS`.
    #//
    php_define("MINUTE_IN_SECONDS", 60)
    php_define("HOUR_IN_SECONDS", 60 * MINUTE_IN_SECONDS)
    php_define("DAY_IN_SECONDS", 24 * HOUR_IN_SECONDS)
    php_define("WEEK_IN_SECONDS", 7 * DAY_IN_SECONDS)
    php_define("MONTH_IN_SECONDS", 30 * DAY_IN_SECONDS)
    php_define("YEAR_IN_SECONDS", 365 * DAY_IN_SECONDS)
    pass
# end def wp_initial_constants
#// 
#// Defines plugin directory WordPress constants.
#// 
#// Defines must-use plugin directory constants, which may be overridden in the sunrise.php drop-in.
#// 
#// @since 3.0.0
#//
def wp_plugin_directory_constants(*args_):
    
    if (not php_defined("WP_CONTENT_URL")):
        php_define("WP_CONTENT_URL", get_option("siteurl") + "/wp-content")
        pass
    # end if
    #// 
    #// Allows for the plugins directory to be moved from the default location.
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("WP_PLUGIN_DIR")):
        php_define("WP_PLUGIN_DIR", WP_CONTENT_DIR + "/plugins")
        pass
    # end if
    #// 
    #// Allows for the plugins directory to be moved from the default location.
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("WP_PLUGIN_URL")):
        php_define("WP_PLUGIN_URL", WP_CONTENT_URL + "/plugins")
        pass
    # end if
    #// 
    #// Allows for the plugins directory to be moved from the default location.
    #// 
    #// @since 2.1.0
    #// @deprecated
    #//
    if (not php_defined("PLUGINDIR")):
        php_define("PLUGINDIR", "wp-content/plugins")
        pass
    # end if
    #// 
    #// Allows for the mu-plugins directory to be moved from the default location.
    #// 
    #// @since 2.8.0
    #//
    if (not php_defined("WPMU_PLUGIN_DIR")):
        php_define("WPMU_PLUGIN_DIR", WP_CONTENT_DIR + "/mu-plugins")
        pass
    # end if
    #// 
    #// Allows for the mu-plugins directory to be moved from the default location.
    #// 
    #// @since 2.8.0
    #//
    if (not php_defined("WPMU_PLUGIN_URL")):
        php_define("WPMU_PLUGIN_URL", WP_CONTENT_URL + "/mu-plugins")
        pass
    # end if
    #// 
    #// Allows for the mu-plugins directory to be moved from the default location.
    #// 
    #// @since 2.8.0
    #// @deprecated
    #//
    if (not php_defined("MUPLUGINDIR")):
        php_define("MUPLUGINDIR", "wp-content/mu-plugins")
        pass
    # end if
# end def wp_plugin_directory_constants
#// 
#// Defines cookie-related WordPress constants.
#// 
#// Defines constants after multisite is loaded.
#// 
#// @since 3.0.0
#//
def wp_cookie_constants(*args_):
    
    #// 
    #// Used to guarantee unique hash cookies.
    #// 
    #// @since 1.5.0
    #//
    if (not php_defined("COOKIEHASH")):
        siteurl = get_site_option("siteurl")
        if siteurl:
            php_define("COOKIEHASH", php_md5(siteurl))
        else:
            php_define("COOKIEHASH", "")
        # end if
    # end if
    #// 
    #// @since 2.0.0
    #//
    if (not php_defined("USER_COOKIE")):
        php_define("USER_COOKIE", "wordpressuser_" + COOKIEHASH)
    # end if
    #// 
    #// @since 2.0.0
    #//
    if (not php_defined("PASS_COOKIE")):
        php_define("PASS_COOKIE", "wordpresspass_" + COOKIEHASH)
    # end if
    #// 
    #// @since 2.5.0
    #//
    if (not php_defined("AUTH_COOKIE")):
        php_define("AUTH_COOKIE", "wordpress_" + COOKIEHASH)
    # end if
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("SECURE_AUTH_COOKIE")):
        php_define("SECURE_AUTH_COOKIE", "wordpress_sec_" + COOKIEHASH)
    # end if
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("LOGGED_IN_COOKIE")):
        php_define("LOGGED_IN_COOKIE", "wordpress_logged_in_" + COOKIEHASH)
    # end if
    #// 
    #// @since 2.3.0
    #//
    if (not php_defined("TEST_COOKIE")):
        php_define("TEST_COOKIE", "wordpress_test_cookie")
    # end if
    #// 
    #// @since 1.2.0
    #//
    if (not php_defined("COOKIEPATH")):
        php_define("COOKIEPATH", php_preg_replace("|https?://[^/]+|i", "", get_option("home") + "/"))
    # end if
    #// 
    #// @since 1.5.0
    #//
    if (not php_defined("SITECOOKIEPATH")):
        php_define("SITECOOKIEPATH", php_preg_replace("|https?://[^/]+|i", "", get_option("siteurl") + "/"))
    # end if
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("ADMIN_COOKIE_PATH")):
        php_define("ADMIN_COOKIE_PATH", SITECOOKIEPATH + "wp-admin")
    # end if
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("PLUGINS_COOKIE_PATH")):
        php_define("PLUGINS_COOKIE_PATH", php_preg_replace("|https?://[^/]+|i", "", WP_PLUGIN_URL))
    # end if
    #// 
    #// @since 2.0.0
    #//
    if (not php_defined("COOKIE_DOMAIN")):
        php_define("COOKIE_DOMAIN", False)
    # end if
    if (not php_defined("RECOVERY_MODE_COOKIE")):
        #// 
        #// @since 5.2.0
        #//
        php_define("RECOVERY_MODE_COOKIE", "wordpress_rec_" + COOKIEHASH)
    # end if
# end def wp_cookie_constants
#// 
#// Defines SSL-related WordPress constants.
#// 
#// @since 3.0.0
#//
def wp_ssl_constants(*args_):
    
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("FORCE_SSL_ADMIN")):
        if "https" == php_parse_url(get_option("siteurl"), PHP_URL_SCHEME):
            php_define("FORCE_SSL_ADMIN", True)
        else:
            php_define("FORCE_SSL_ADMIN", False)
        # end if
    # end if
    force_ssl_admin(FORCE_SSL_ADMIN)
    #// 
    #// @since 2.6.0
    #// @deprecated 4.0.0
    #//
    if php_defined("FORCE_SSL_LOGIN") and FORCE_SSL_LOGIN:
        force_ssl_admin(True)
    # end if
# end def wp_ssl_constants
#// 
#// Defines functionality-related WordPress constants.
#// 
#// @since 3.0.0
#//
def wp_functionality_constants(*args_):
    
    #// 
    #// @since 2.5.0
    #//
    if (not php_defined("AUTOSAVE_INTERVAL")):
        php_define("AUTOSAVE_INTERVAL", MINUTE_IN_SECONDS)
    # end if
    #// 
    #// @since 2.9.0
    #//
    if (not php_defined("EMPTY_TRASH_DAYS")):
        php_define("EMPTY_TRASH_DAYS", 30)
    # end if
    if (not php_defined("WP_POST_REVISIONS")):
        php_define("WP_POST_REVISIONS", True)
    # end if
    #// 
    #// @since 3.3.0
    #//
    if (not php_defined("WP_CRON_LOCK_TIMEOUT")):
        php_define("WP_CRON_LOCK_TIMEOUT", MINUTE_IN_SECONDS)
    # end if
# end def wp_functionality_constants
#// 
#// Defines templating-related WordPress constants.
#// 
#// @since 3.0.0
#//
def wp_templating_constants(*args_):
    
    #// 
    #// Filesystem path to the current active template directory.
    #// 
    #// @since 1.5.0
    #//
    php_define("TEMPLATEPATH", get_template_directory())
    #// 
    #// Filesystem path to the current active template stylesheet directory.
    #// 
    #// @since 2.1.0
    #//
    php_define("STYLESHEETPATH", get_stylesheet_directory())
    #// 
    #// Slug of the default theme for this installation.
    #// Used as the default theme when installing new sites.
    #// It will be used as the fallback if the current theme doesn't exist.
    #// 
    #// @since 3.0.0
    #// @see WP_Theme::get_core_default_theme()
    #//
    if (not php_defined("WP_DEFAULT_THEME")):
        php_define("WP_DEFAULT_THEME", "twentytwenty")
    # end if
# end def wp_templating_constants
