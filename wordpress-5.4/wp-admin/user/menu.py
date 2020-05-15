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
#// Build User Administration Menu.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#//
menu[2] = Array(__("Dashboard"), "exist", "index.php", "", "menu-top menu-top-first menu-icon-dashboard", "menu-dashboard", "dashicons-dashboard")
menu[4] = Array("", "exist", "separator1", "", "wp-menu-separator")
menu[70] = Array(__("Profile"), "exist", "profile.php", "", "menu-top menu-icon-users", "menu-users", "dashicons-admin-users")
menu[99] = Array("", "exist", "separator-last", "", "wp-menu-separator")
_wp_real_parent_file["users.php"] = "profile.php"
compat = Array()
submenu = Array()
php_include_file(ABSPATH + "wp-admin/includes/menu.php", once=True)
