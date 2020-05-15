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
#// Action handler for Multisite administration panels.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
action = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else ""
if php_empty(lambda : action):
    wp_redirect(network_admin_url())
    php_exit(0)
# end if
#// 
#// Fires just before the action handler in several Network Admin screens.
#// 
#// This hook fires on multiple screens in the Multisite Network Admin,
#// including Users, Network Settings, and Site Settings.
#// 
#// @since 3.0.0
#//
do_action("wpmuadminedit")
#// 
#// Fires the requested handler action.
#// 
#// The dynamic portion of the hook name, `$action`, refers to the name
#// of the requested action derived from the `GET` request.
#// 
#// @since 3.1.0
#//
do_action(str("network_admin_edit_") + str(action))
wp_redirect(network_admin_url())
php_exit(0)
