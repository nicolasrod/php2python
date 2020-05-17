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
#// Build User Administration Menu.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#//
menu_[2] = Array(__("Dashboard"), "exist", "index.php", "", "menu-top menu-top-first menu-icon-dashboard", "menu-dashboard", "dashicons-dashboard")
menu_[4] = Array("", "exist", "separator1", "", "wp-menu-separator")
menu_[70] = Array(__("Profile"), "exist", "profile.php", "", "menu-top menu-icon-users", "menu-users", "dashicons-admin-users")
menu_[99] = Array("", "exist", "separator-last", "", "wp-menu-separator")
_wp_real_parent_file_["users.php"] = "profile.php"
compat_ = Array()
submenu_ = Array()
php_include_file(ABSPATH + "wp-admin/includes/menu.php", once=True)
