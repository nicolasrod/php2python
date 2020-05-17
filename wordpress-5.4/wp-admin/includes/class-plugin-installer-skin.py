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
#// Upgrader API: Plugin_Installer_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Plugin Installer Skin for WordPress Plugin Installer.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see WP_Upgrader_Skin
#//
class Plugin_Installer_Skin(WP_Upgrader_Skin):
    api = Array()
    type = Array()
    #// 
    #// @param array $args
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"type": "web", "url": "", "plugin": "", "nonce": "", "title": ""})
        args_ = wp_parse_args(args_, defaults_)
        self.type = args_["type"]
        self.api = args_["api"] if (php_isset(lambda : args_["api"])) else Array()
        super().__init__(args_)
    # end def __init__
    #// 
    #//
    def before(self):
        
        
        if (not php_empty(lambda : self.api)):
            self.upgrader.strings["process_success"] = php_sprintf(__("Successfully installed the plugin <strong>%1$s %2$s</strong>."), self.api.name, self.api.version)
        # end if
    # end def before
    #// 
    #//
    def after(self):
        
        
        plugin_file_ = self.upgrader.plugin_info()
        install_actions_ = Array()
        from_ = wp_unslash(PHP_REQUEST["from"]) if (php_isset(lambda : PHP_REQUEST["from"])) else "plugins"
        if "import" == from_:
            install_actions_["activate_plugin"] = php_sprintf("<a class=\"button button-primary\" href=\"%s\" target=\"_parent\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;from=import&amp;plugin=" + urlencode(plugin_file_), "activate-plugin_" + plugin_file_), __("Activate Plugin &amp; Run Importer"))
        elif "press-this" == from_:
            install_actions_["activate_plugin"] = php_sprintf("<a class=\"button button-primary\" href=\"%s\" target=\"_parent\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;from=press-this&amp;plugin=" + urlencode(plugin_file_), "activate-plugin_" + plugin_file_), __("Activate Plugin &amp; Return to Press This"))
        else:
            install_actions_["activate_plugin"] = php_sprintf("<a class=\"button button-primary\" href=\"%s\" target=\"_parent\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;plugin=" + urlencode(plugin_file_), "activate-plugin_" + plugin_file_), __("Activate Plugin"))
        # end if
        if is_multisite() and current_user_can("manage_network_plugins"):
            install_actions_["network_activate"] = php_sprintf("<a class=\"button button-primary\" href=\"%s\" target=\"_parent\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;networkwide=1&amp;plugin=" + urlencode(plugin_file_), "activate-plugin_" + plugin_file_), __("Network Activate"))
            install_actions_["activate_plugin"] = None
        # end if
        if "import" == from_:
            install_actions_["importers_page"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", admin_url("import.php"), __("Return to Importers"))
        elif "web" == self.type:
            install_actions_["plugins_page"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("plugin-install.php"), __("Return to Plugin Installer"))
        elif "upload" == self.type and "plugins" == from_:
            install_actions_["plugins_page"] = php_sprintf("<a href=\"%s\">%s</a>", self_admin_url("plugin-install.php"), __("Return to Plugin Installer"))
        else:
            install_actions_["plugins_page"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("plugins.php"), __("Return to Plugins page"))
        # end if
        if (not self.result) or is_wp_error(self.result):
            install_actions_["activate_plugin"] = None
            install_actions_["network_activate"] = None
        elif (not current_user_can("activate_plugin", plugin_file_)):
            install_actions_["activate_plugin"] = None
        # end if
        #// 
        #// Filters the list of action links available following a single plugin installation.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string[] $install_actions Array of plugin action links.
        #// @param object   $api             Object containing WordPress.org API plugin data. Empty
        #// for non-API installs, such as when a plugin is installed
        #// via upload.
        #// @param string   $plugin_file     Path to the plugin file relative to the plugins directory.
        #//
        install_actions_ = apply_filters("install_plugin_complete_actions", install_actions_, self.api, plugin_file_)
        if (not php_empty(lambda : install_actions_)):
            self.feedback(php_implode(" ", install_actions_))
        # end if
    # end def after
# end class Plugin_Installer_Skin
