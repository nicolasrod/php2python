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
#// Upgrader API: Plugin_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Plugin Upgrader Skin for WordPress Plugin Upgrades.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see WP_Upgrader_Skin
#//
class Plugin_Upgrader_Skin(WP_Upgrader_Skin):
    plugin = ""
    plugin_active = False
    plugin_network_active = False
    #// 
    #// @param array $args
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"url": "", "plugin": "", "nonce": "", "title": __("Update Plugin")})
        args_ = wp_parse_args(args_, defaults_)
        self.plugin = args_["plugin"]
        self.plugin_active = is_plugin_active(self.plugin)
        self.plugin_network_active = is_plugin_active_for_network(self.plugin)
        super().__init__(args_)
    # end def __init__
    #// 
    #//
    def after(self):
        
        
        self.plugin = self.upgrader.plugin_info()
        if (not php_empty(lambda : self.plugin)) and (not is_wp_error(self.result)) and self.plugin_active:
            #// Currently used only when JS is off for a single plugin update?
            php_printf("<iframe title=\"%s\" style=\"border:0;overflow:hidden\" width=\"100%%\" height=\"170\" src=\"%s\"></iframe>", esc_attr__("Update progress"), wp_nonce_url("update.php?action=activate-plugin&networkwide=" + self.plugin_network_active + "&plugin=" + urlencode(self.plugin), "activate-plugin_" + self.plugin))
        # end if
        self.decrement_update_count("plugin")
        update_actions_ = Array({"activate_plugin": php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;plugin=" + urlencode(self.plugin), "activate-plugin_" + self.plugin), __("Activate Plugin")), "plugins_page": php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("plugins.php"), __("Return to Plugins page"))})
        if self.plugin_active or (not self.result) or is_wp_error(self.result) or (not current_user_can("activate_plugin", self.plugin)):
            update_actions_["activate_plugin"] = None
        # end if
        #// 
        #// Filters the list of action links available following a single plugin update.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string[] $update_actions Array of plugin action links.
        #// @param string   $plugin         Path to the plugin file relative to the plugins directory.
        #//
        update_actions_ = apply_filters("update_plugin_complete_actions", update_actions_, self.plugin)
        if (not php_empty(lambda : update_actions_)):
            self.feedback(php_implode(" | ", update_actions_))
        # end if
    # end def after
# end class Plugin_Upgrader_Skin
