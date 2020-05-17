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
#// Build Network Administration Menu.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.1.0
#// 
#// translators: Network menu item.
menu_[2] = Array(__("Dashboard"), "manage_network", "index.php", "", "menu-top menu-top-first menu-icon-dashboard", "menu-dashboard", "dashicons-dashboard")
submenu_["index.php"][0] = Array(__("Home"), "read", "index.php")
if current_user_can("update_core"):
    cap_ = "update_core"
elif current_user_can("update_plugins"):
    cap_ = "update_plugins"
elif current_user_can("update_themes"):
    cap_ = "update_themes"
else:
    cap_ = "update_languages"
# end if
update_data_ = wp_get_update_data()
if update_data_["counts"]["total"]:
    submenu_["index.php"][10] = Array(php_sprintf(__("Updates %s"), php_sprintf("<span class=\"update-plugins count-%s\"><span class=\"update-count\">%s</span></span>", update_data_["counts"]["total"], number_format_i18n(update_data_["counts"]["total"]))), cap_, "update-core.php")
else:
    submenu_["index.php"][10] = Array(__("Updates"), cap_, "update-core.php")
# end if
cap_ = None
submenu_["index.php"][15] = Array(__("Upgrade Network"), "upgrade_network", "upgrade.php")
menu_[4] = Array("", "read", "separator1", "", "wp-menu-separator")
#// translators: Sites menu item.
menu_[5] = Array(__("Sites"), "manage_sites", "sites.php", "", "menu-top menu-icon-site", "menu-site", "dashicons-admin-multisite")
submenu_["sites.php"][5] = Array(__("All Sites"), "manage_sites", "sites.php")
submenu_["sites.php"][10] = Array(_x("Add New", "site"), "create_sites", "site-new.php")
menu_[10] = Array(__("Users"), "manage_network_users", "users.php", "", "menu-top menu-icon-users", "menu-users", "dashicons-admin-users")
submenu_["users.php"][5] = Array(__("All Users"), "manage_network_users", "users.php")
submenu_["users.php"][10] = Array(_x("Add New", "user"), "create_users", "user-new.php")
if current_user_can("update_themes") and update_data_["counts"]["themes"]:
    menu_[15] = Array(php_sprintf(__("Themes %s"), php_sprintf("<span class=\"update-plugins count-%s\"><span class=\"theme-count\">%s</span></span>", update_data_["counts"]["themes"], number_format_i18n(update_data_["counts"]["themes"]))), "manage_network_themes", "themes.php", "", "menu-top menu-icon-appearance", "menu-appearance", "dashicons-admin-appearance")
else:
    menu_[15] = Array(__("Themes"), "manage_network_themes", "themes.php", "", "menu-top menu-icon-appearance", "menu-appearance", "dashicons-admin-appearance")
# end if
submenu_["themes.php"][5] = Array(__("Installed Themes"), "manage_network_themes", "themes.php")
submenu_["themes.php"][10] = Array(_x("Add New", "theme"), "install_themes", "theme-install.php")
submenu_["themes.php"][15] = Array(__("Theme Editor"), "edit_themes", "theme-editor.php")
if current_user_can("update_plugins") and update_data_["counts"]["plugins"]:
    menu_[20] = Array(php_sprintf(__("Plugins %s"), php_sprintf("<span class=\"update-plugins count-%s\"><span class=\"plugin-count\">%s</span></span>", update_data_["counts"]["plugins"], number_format_i18n(update_data_["counts"]["plugins"]))), "manage_network_plugins", "plugins.php", "", "menu-top menu-icon-plugins", "menu-plugins", "dashicons-admin-plugins")
else:
    menu_[20] = Array(__("Plugins"), "manage_network_plugins", "plugins.php", "", "menu-top menu-icon-plugins", "menu-plugins", "dashicons-admin-plugins")
# end if
submenu_["plugins.php"][5] = Array(__("Installed Plugins"), "manage_network_plugins", "plugins.php")
submenu_["plugins.php"][10] = Array(_x("Add New", "plugin"), "install_plugins", "plugin-install.php")
submenu_["plugins.php"][15] = Array(__("Plugin Editor"), "edit_plugins", "plugin-editor.php")
menu_[25] = Array(__("Settings"), "manage_network_options", "settings.php", "", "menu-top menu-icon-settings", "menu-settings", "dashicons-admin-settings")
if php_defined("MULTISITE") and php_defined("WP_ALLOW_MULTISITE") and WP_ALLOW_MULTISITE:
    submenu_["settings.php"][5] = Array(__("Network Settings"), "manage_network_options", "settings.php")
    submenu_["settings.php"][10] = Array(__("Network Setup"), "setup_network", "setup.php")
# end if
update_data_ = None
menu_[99] = Array("", "exist", "separator-last", "", "wp-menu-separator")
php_include_file(ABSPATH + "wp-admin/includes/menu.php", once=True)
