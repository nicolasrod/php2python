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
#// @package Akismet
#// 
#// 
#// Plugin Name: Akismet Anti-Spam
#// Plugin URI: https://akismet.com
#// Description: Used by millions, Akismet is quite possibly the best way in the world to <strong>protect your blog from spam</strong>. It keeps your site protected even while you sleep. To get started: activate the Akismet plugin and then go to your Akismet Settings page to set up your API key.
#// Version: 4.1.4
#// Author: Automattic
#// Author URI: https://automattic.com/wordpress-plugins
#// License: GPLv2 or later
#// Text Domain: akismet
#// 
#// 
#// This program is free software; you can redistribute it and/or
#// modify it under the terms of the GNU General Public License
#// as published by the Free Software Foundation; either version 2
#// of the License, or (at your option) any later version.
#// This program is distributed in the hope that it will be useful,
#// but WITHOUT ANY WARRANTY; without even the implied warranty of
#// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#// GNU General Public License for more details.
#// You should have received a copy of the GNU General Public License
#// along with this program; if not, write to the Free Software
#// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#// Copyright 2005-2015 Automattic, Inc.
#// 
#// Make sure we don't expose any info if called directly
if (not php_function_exists("add_action")):
    php_print("Hi there!  I'm just a plugin, not much I can do when called directly.")
    php_exit(0)
# end if
php_define("AKISMET_VERSION", "4.1.4")
php_define("AKISMET__MINIMUM_WP_VERSION", "4.0")
php_define("AKISMET__PLUGIN_DIR", plugin_dir_path(__FILE__))
php_define("AKISMET_DELETE_LIMIT", 100000)
register_activation_hook(__FILE__, Array("Akismet", "plugin_activation"))
register_deactivation_hook(__FILE__, Array("Akismet", "plugin_deactivation"))
php_include_file(AKISMET__PLUGIN_DIR + "class.akismet.php", once=True)
php_include_file(AKISMET__PLUGIN_DIR + "class.akismet-widget.php", once=True)
php_include_file(AKISMET__PLUGIN_DIR + "class.akismet-rest-api.php", once=True)
add_action("init", Array("Akismet", "init"))
add_action("rest_api_init", Array("Akismet_REST_API", "init"))
if is_admin() or php_defined("WP_CLI") and WP_CLI:
    php_include_file(AKISMET__PLUGIN_DIR + "class.akismet-admin.php", once=True)
    add_action("init", Array("Akismet_Admin", "init"))
# end if
#// add wrapper class around deprecated akismet functions that are referenced elsewhere
php_include_file(AKISMET__PLUGIN_DIR + "wrapper.php", once=True)
if php_defined("WP_CLI") and WP_CLI:
    php_include_file(AKISMET__PLUGIN_DIR + "class.akismet-cli.php", once=True)
# end if
