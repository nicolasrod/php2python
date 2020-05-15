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
#// Bootstrap file for setting the ABSPATH constant
#// and loading the wp-config.php file. The wp-config.php
#// file will then load the wp-settings.php file, which
#// will then set up the WordPress environment.
#// 
#// If the wp-config.php file is not found then an error
#// will be displayed asking the visitor to set up the
#// wp-config.php file.
#// 
#// Will also search for wp-config.php in WordPress' parent
#// directory to allow the WordPress directory to remain
#// untouched.
#// 
#// @package WordPress
#// 
#// Define ABSPATH as this file's directory
if (not php_defined("ABSPATH")):
    php_define("ABSPATH", __DIR__ + "/")
# end if
php_error_reporting(E_CORE_ERROR | E_CORE_WARNING | E_COMPILE_ERROR | E_ERROR | E_WARNING | E_PARSE | E_USER_ERROR | E_USER_WARNING | E_RECOVERABLE_ERROR)
#// 
#// If wp-config.php exists in the WordPress root, or if it exists in the root and wp-settings.php
#// doesn't, load wp-config.php. The secondary check for wp-settings.php has the added benefit
#// of avoiding cases where the current directory is a nested installation, e.g. / is WordPress(a)
#// and /blog/ is WordPress(b).
#// 
#// If neither set of conditions is true, initiate loading the setup process.
#//
if php_file_exists(ABSPATH + "wp-config.php"):
    #// The config file resides in ABSPATH
    php_include_file(ABSPATH + "wp-config.php", once=True)
elif php_no_error(lambda: php_file_exists(php_dirname(ABSPATH) + "/wp-config.php")) and (not php_no_error(lambda: php_file_exists(php_dirname(ABSPATH) + "/wp-settings.php"))):
    #// The config file resides one level above ABSPATH but is not part of another installation
    php_include_file(php_dirname(ABSPATH) + "/wp-config.php", once=True)
else:
    #// A config file doesn't exist.
    php_define("WPINC", "wp-includes")
    php_include_file(ABSPATH + WPINC + "/load.php", once=True)
    #// Standardize $_SERVER variables across setups.
    wp_fix_server_vars()
    php_include_file(ABSPATH + WPINC + "/functions.php", once=True)
    path = wp_guess_url() + "/wp-admin/setup-config.php"
    #// 
    #// We're going to redirect to setup-config.php. While this shouldn't result
    #// in an infinite loop, that's a silly thing to assume, don't you think? If
    #// we're traveling in circles, our last-ditch effort is "Need more help?"
    #//
    if False == php_strpos(PHP_SERVER["REQUEST_URI"], "setup-config"):
        php_header("Location: " + path)
        php_exit(0)
    # end if
    php_define("WP_CONTENT_DIR", ABSPATH + "wp-content")
    php_include_file(ABSPATH + WPINC + "/version.php", once=True)
    wp_check_php_mysql_versions()
    wp_load_translations_early()
    #// Die with an error message
    die = php_sprintf(__("There doesn't seem to be a %s file. I need this before we can get started."), "<code>wp-config.php</code>") + "</p>"
    die += "<p>" + php_sprintf(__("Need more help? <a href='%s'>We got it</a>."), __("https://wordpress.org/support/article/editing-wp-config-php/")) + "</p>"
    die += "<p>" + php_sprintf(__("You can create a %s file through a web interface, but this doesn't work for all server setups. The safest way is to manually create the file."), "<code>wp-config.php</code>") + "</p>"
    die += "<p><a href=\"" + path + "\" class=\"button button-large\">" + __("Create a Configuration File") + "</a>"
    wp_die(die, __("WordPress &rsaquo; Error"))
# end if
