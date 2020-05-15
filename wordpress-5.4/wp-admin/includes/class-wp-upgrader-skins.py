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
#// The User Interface "Skins" for the WordPress File Upgrader
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 2.8.0
#// @deprecated 4.7.0
#//
_deprecated_file(php_basename(__FILE__), "4.7.0", "class-wp-upgrader.php")
#// WP_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader-skin.php", once=True)
#// Plugin_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-plugin-upgrader-skin.php", once=True)
#// Theme_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-theme-upgrader-skin.php", once=True)
#// Bulk_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-bulk-upgrader-skin.php", once=True)
#// Bulk_Plugin_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-bulk-plugin-upgrader-skin.php", once=True)
#// Bulk_Theme_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-bulk-theme-upgrader-skin.php", once=True)
#// Plugin_Installer_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-plugin-installer-skin.php", once=True)
#// Theme_Installer_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-theme-installer-skin.php", once=True)
#// Language_Pack_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-language-pack-upgrader-skin.php", once=True)
#// Automatic_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-automatic-upgrader-skin.php", once=True)
#// WP_Ajax_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-wp-ajax-upgrader-skin.php", once=True)
