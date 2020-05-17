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
#// Upgrader API: Bulk_Plugin_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Bulk Plugin Upgrader Skin for WordPress Plugin Upgrades.
#// 
#// @since 3.0.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see Bulk_Upgrader_Skin
#//
class Bulk_Plugin_Upgrader_Skin(Bulk_Upgrader_Skin):
    plugin_info = Array()
    #// Plugin_Upgrader::bulk_upgrade() will fill this in.
    def add_strings(self):
        
        
        super().add_strings()
        #// translators: 1: Plugin name, 2: Number of the plugin, 3: Total number of plugins being updated.
        self.upgrader.strings["skin_before_update_header"] = __("Updating Plugin %1$s (%2$d/%3$d)")
    # end def add_strings
    #// 
    #// @param string $title
    #//
    def before(self, title_=""):
        
        
        super().before(self.plugin_info["Title"])
    # end def before
    #// 
    #// @param string $title
    #//
    def after(self, title_=""):
        
        
        super().after(self.plugin_info["Title"])
        self.decrement_update_count("plugin")
    # end def after
    #// 
    #//
    def bulk_footer(self):
        
        
        super().bulk_footer()
        update_actions_ = Array({"plugins_page": php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("plugins.php"), __("Return to Plugins page")), "updates_page": php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("update-core.php"), __("Return to WordPress Updates page"))})
        if (not current_user_can("activate_plugins")):
            update_actions_["plugins_page"] = None
        # end if
        #// 
        #// Filters the list of action links available following bulk plugin updates.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $update_actions Array of plugin action links.
        #// @param array    $plugin_info    Array of information for the last-updated plugin.
        #//
        update_actions_ = apply_filters("update_bulk_plugins_complete_actions", update_actions_, self.plugin_info)
        if (not php_empty(lambda : update_actions_)):
            self.feedback(php_implode(" | ", update_actions_))
        # end if
    # end def bulk_footer
# end class Bulk_Plugin_Upgrader_Skin
