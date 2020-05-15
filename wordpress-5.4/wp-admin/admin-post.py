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
#// WordPress Generic Request (POST/GET) Handler
#// 
#// Intended for form submission handling in themes and plugins.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// We are located in WordPress Administration Screens
if (not php_defined("WP_ADMIN")):
    php_define("WP_ADMIN", True)
# end if
if php_defined("ABSPATH"):
    php_include_file(ABSPATH + "wp-load.php", once=True)
else:
    php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
# end if
#// Allow for cross-domain requests (from the front end).
send_origin_headers()
php_include_file(ABSPATH + "wp-admin/includes/admin.php", once=True)
nocache_headers()
#// This action is documented in wp-admin/admin.php
do_action("admin_init")
action = "" if php_empty(lambda : PHP_REQUEST["action"]) else PHP_REQUEST["action"]
if (not is_user_logged_in()):
    if php_empty(lambda : action):
        #// 
        #// Fires on a non-authenticated admin post request where no action is supplied.
        #// 
        #// @since 2.6.0
        #//
        do_action("admin_post_nopriv")
    else:
        #// 
        #// Fires on a non-authenticated admin post request for the given action.
        #// 
        #// The dynamic portion of the hook name, `$action`, refers to the given
        #// request action.
        #// 
        #// @since 2.6.0
        #//
        do_action(str("admin_post_nopriv_") + str(action))
    # end if
else:
    if php_empty(lambda : action):
        #// 
        #// Fires on an authenticated admin post request where no action is supplied.
        #// 
        #// @since 2.6.0
        #//
        do_action("admin_post")
    else:
        #// 
        #// Fires on an authenticated admin post request for the given action.
        #// 
        #// The dynamic portion of the hook name, `$action`, refers to the given
        #// request action.
        #// 
        #// @since 2.6.0
        #//
        do_action(str("admin_post_") + str(action))
    # end if
# end if
