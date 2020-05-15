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
#// Upgrade API: Theme_Upgrader class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Core class used for upgrading/installing themes.
#// 
#// It is designed to upgrade/install themes from a local zip, remote zip URL,
#// or uploaded zip file.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader.php.
#// 
#// @see WP_Upgrader
#//
class Theme_Upgrader(WP_Upgrader):
    result = Array()
    bulk = False
    #// 
    #// Initialize the upgrade strings.
    #// 
    #// @since 2.8.0
    #//
    def upgrade_strings(self):
        
        self.strings["up_to_date"] = __("The theme is at the latest version.")
        self.strings["no_package"] = __("Update package not available.")
        #// translators: %s: Package URL.
        self.strings["downloading_package"] = php_sprintf(__("Downloading update from %s&#8230;"), "<span class=\"code\">%s</span>")
        self.strings["unpack_package"] = __("Unpacking the update&#8230;")
        self.strings["remove_old"] = __("Removing the old version of the theme&#8230;")
        self.strings["remove_old_failed"] = __("Could not remove the old theme.")
        self.strings["process_failed"] = __("Theme update failed.")
        self.strings["process_success"] = __("Theme updated successfully.")
    # end def upgrade_strings
    #// 
    #// Initialize the installation strings.
    #// 
    #// @since 2.8.0
    #//
    def install_strings(self):
        
        self.strings["no_package"] = __("Installation package not available.")
        #// translators: %s: Package URL.
        self.strings["downloading_package"] = php_sprintf(__("Downloading installation package from %s&#8230;"), "<span class=\"code\">%s</span>")
        self.strings["unpack_package"] = __("Unpacking the package&#8230;")
        self.strings["installing_package"] = __("Installing the theme&#8230;")
        self.strings["no_files"] = __("The theme contains no files.")
        self.strings["process_failed"] = __("Theme installation failed.")
        self.strings["process_success"] = __("Theme installed successfully.")
        #// translators: 1: Theme name, 2: Theme version.
        self.strings["process_success_specific"] = __("Successfully installed the theme <strong>%1$s %2$s</strong>.")
        self.strings["parent_theme_search"] = __("This theme requires a parent theme. Checking if it is installed&#8230;")
        #// translators: 1: Theme name, 2: Theme version.
        self.strings["parent_theme_prepare_install"] = __("Preparing to install <strong>%1$s %2$s</strong>&#8230;")
        #// translators: 1: Theme name, 2: Theme version.
        self.strings["parent_theme_currently_installed"] = __("The parent theme, <strong>%1$s %2$s</strong>, is currently installed.")
        #// translators: 1: Theme name, 2: Theme version.
        self.strings["parent_theme_install_success"] = __("Successfully installed the parent theme, <strong>%1$s %2$s</strong>.")
        #// translators: %s: Theme name.
        self.strings["parent_theme_not_found"] = php_sprintf(__("<strong>The parent theme could not be found.</strong> You will need to install the parent theme, %s, before you can use this child theme."), "<strong>%s</strong>")
    # end def install_strings
    #// 
    #// Check if a child theme is being installed and we need to install its parent.
    #// 
    #// Hooked to the {@see 'upgrader_post_install'} filter by Theme_Upgrader::install().
    #// 
    #// @since 3.4.0
    #// 
    #// @param bool  $install_result
    #// @param array $hook_extra
    #// @param array $child_result
    #// @return bool
    #//
    def check_parent_theme_filter(self, install_result=None, hook_extra=None, child_result=None):
        
        #// Check to see if we need to install a parent theme.
        theme_info = self.theme_info()
        if (not theme_info.parent()):
            return install_result
        # end if
        self.skin.feedback("parent_theme_search")
        if (not theme_info.parent().errors()):
            self.skin.feedback("parent_theme_currently_installed", theme_info.parent().display("Name"), theme_info.parent().display("Version"))
            #// We already have the theme, fall through.
            return install_result
        # end if
        #// We don't have the parent theme, let's install it.
        api = themes_api("theme_information", Array({"slug": theme_info.get("Template"), "fields": Array({"sections": False, "tags": False})}))
        #// Save on a bit of bandwidth.
        if (not api) or is_wp_error(api):
            self.skin.feedback("parent_theme_not_found", theme_info.get("Template"))
            #// Don't show activate or preview actions after installation.
            add_filter("install_theme_complete_actions", Array(self, "hide_activate_preview_actions"))
            return install_result
        # end if
        #// Backup required data we're going to override:
        child_api = self.skin.api
        child_success_message = self.strings["process_success"]
        #// Override them.
        self.skin.api = api
        self.strings["process_success_specific"] = self.strings["parent_theme_install_success"]
        #// , $api->name, $api->version );
        self.skin.feedback("parent_theme_prepare_install", api.name, api.version)
        add_filter("install_theme_complete_actions", "__return_false", 999)
        #// Don't show any actions after installing the theme.
        #// Install the parent theme.
        parent_result = self.run(Array({"package": api.download_link, "destination": get_theme_root(), "clear_destination": False, "clear_working": True}))
        if is_wp_error(parent_result):
            add_filter("install_theme_complete_actions", Array(self, "hide_activate_preview_actions"))
        # end if
        #// Start cleaning up after the parent's installation.
        remove_filter("install_theme_complete_actions", "__return_false", 999)
        #// Reset child's result and data.
        self.result = child_result
        self.skin.api = child_api
        self.strings["process_success"] = child_success_message
        return install_result
    # end def check_parent_theme_filter
    #// 
    #// Don't display the activate and preview actions to the user.
    #// 
    #// Hooked to the {@see 'install_theme_complete_actions'} filter by
    #// Theme_Upgrader::check_parent_theme_filter() when installing
    #// a child theme and installing the parent theme fails.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $actions Preview actions.
    #// @return array
    #//
    def hide_activate_preview_actions(self, actions=None):
        
        actions["activate"] = None
        actions["preview"] = None
        return actions
    # end def hide_activate_preview_actions
    #// 
    #// Install a theme package.
    #// 
    #// @since 2.8.0
    #// @since 3.7.0 The `$args` parameter was added, making clearing the update cache optional.
    #// 
    #// @param string $package The full local path or URI of the package.
    #// @param array  $args {
    #// Optional. Other arguments for installing a theme package. Default empty array.
    #// 
    #// @type bool $clear_update_cache Whether to clear the updates cache if successful.
    #// Default true.
    #// }
    #// 
    #// @return bool|WP_Error True if the installation was successful, false or a WP_Error object otherwise.
    #//
    def install(self, package=None, args=Array()):
        
        defaults = Array({"clear_update_cache": True})
        parsed_args = wp_parse_args(args, defaults)
        self.init()
        self.install_strings()
        add_filter("upgrader_source_selection", Array(self, "check_package"))
        add_filter("upgrader_post_install", Array(self, "check_parent_theme_filter"), 10, 3)
        if parsed_args["clear_update_cache"]:
            #// Clear cache so wp_update_themes() knows about the new theme.
            add_action("upgrader_process_complete", "wp_clean_themes_cache", 9, 0)
        # end if
        self.run(Array({"package": package, "destination": get_theme_root(), "clear_destination": False, "clear_working": True, "hook_extra": Array({"type": "theme", "action": "install"})}))
        remove_action("upgrader_process_complete", "wp_clean_themes_cache", 9)
        remove_filter("upgrader_source_selection", Array(self, "check_package"))
        remove_filter("upgrader_post_install", Array(self, "check_parent_theme_filter"))
        if (not self.result) or is_wp_error(self.result):
            return self.result
        # end if
        #// Refresh the Theme Update information.
        wp_clean_themes_cache(parsed_args["clear_update_cache"])
        return True
    # end def install
    #// 
    #// Upgrade a theme.
    #// 
    #// @since 2.8.0
    #// @since 3.7.0 The `$args` parameter was added, making clearing the update cache optional.
    #// 
    #// @param string $theme The theme slug.
    #// @param array  $args {
    #// Optional. Other arguments for upgrading a theme. Default empty array.
    #// 
    #// @type bool $clear_update_cache Whether to clear the update cache if successful.
    #// Default true.
    #// }
    #// @return bool|WP_Error True if the upgrade was successful, false or a WP_Error object otherwise.
    #//
    def upgrade(self, theme=None, args=Array()):
        
        defaults = Array({"clear_update_cache": True})
        parsed_args = wp_parse_args(args, defaults)
        self.init()
        self.upgrade_strings()
        #// Is an update available?
        current = get_site_transient("update_themes")
        if (not (php_isset(lambda : current.response[theme]))):
            self.skin.before()
            self.skin.set_result(False)
            self.skin.error("up_to_date")
            self.skin.after()
            return False
        # end if
        r = current.response[theme]
        add_filter("upgrader_pre_install", Array(self, "current_before"), 10, 2)
        add_filter("upgrader_post_install", Array(self, "current_after"), 10, 2)
        add_filter("upgrader_clear_destination", Array(self, "delete_old_theme"), 10, 4)
        if parsed_args["clear_update_cache"]:
            #// Clear cache so wp_update_themes() knows about the new theme.
            add_action("upgrader_process_complete", "wp_clean_themes_cache", 9, 0)
        # end if
        self.run(Array({"package": r["package"], "destination": get_theme_root(theme), "clear_destination": True, "clear_working": True, "hook_extra": Array({"theme": theme, "type": "theme", "action": "update"})}))
        remove_action("upgrader_process_complete", "wp_clean_themes_cache", 9)
        remove_filter("upgrader_pre_install", Array(self, "current_before"))
        remove_filter("upgrader_post_install", Array(self, "current_after"))
        remove_filter("upgrader_clear_destination", Array(self, "delete_old_theme"))
        if (not self.result) or is_wp_error(self.result):
            return self.result
        # end if
        wp_clean_themes_cache(parsed_args["clear_update_cache"])
        return True
    # end def upgrade
    #// 
    #// Upgrade several themes at once.
    #// 
    #// @since 3.0.0
    #// @since 3.7.0 The `$args` parameter was added, making clearing the update cache optional.
    #// 
    #// @param string[] $themes Array of the theme slugs.
    #// @param array    $args {
    #// Optional. Other arguments for upgrading several themes at once. Default empty array.
    #// 
    #// @type bool $clear_update_cache Whether to clear the update cache if successful.
    #// Default true.
    #// }
    #// @return array[]|false An array of results, or false if unable to connect to the filesystem.
    #//
    def bulk_upgrade(self, themes=None, args=Array()):
        
        defaults = Array({"clear_update_cache": True})
        parsed_args = wp_parse_args(args, defaults)
        self.init()
        self.bulk = True
        self.upgrade_strings()
        current = get_site_transient("update_themes")
        add_filter("upgrader_pre_install", Array(self, "current_before"), 10, 2)
        add_filter("upgrader_post_install", Array(self, "current_after"), 10, 2)
        add_filter("upgrader_clear_destination", Array(self, "delete_old_theme"), 10, 4)
        self.skin.header()
        #// Connect to the filesystem first.
        res = self.fs_connect(Array(WP_CONTENT_DIR))
        if (not res):
            self.skin.footer()
            return False
        # end if
        self.skin.bulk_header()
        #// 
        #// Only start maintenance mode if:
        #// - running Multisite and there are one or more themes specified, OR
        #// - a theme with an update available is currently in use.
        #// @todo For multisite, maintenance mode should only kick in for individual sites if at all possible.
        #//
        maintenance = is_multisite() and (not php_empty(lambda : themes))
        for theme in themes:
            maintenance = maintenance or get_stylesheet() == theme or get_template() == theme
        # end for
        if maintenance:
            self.maintenance_mode(True)
        # end if
        results = Array()
        self.update_count = php_count(themes)
        self.update_current = 0
        for theme in themes:
            self.update_current += 1
            self.skin.theme_info = self.theme_info(theme)
            if (not (php_isset(lambda : current.response[theme]))):
                self.skin.set_result(True)
                self.skin.before()
                self.skin.feedback("up_to_date")
                self.skin.after()
                results[theme] = True
                continue
            # end if
            #// Get the URL to the zip file.
            r = current.response[theme]
            result = self.run(Array({"package": r["package"], "destination": get_theme_root(theme), "clear_destination": True, "clear_working": True, "is_multi": True, "hook_extra": Array({"theme": theme})}))
            results[theme] = self.result
            #// Prevent credentials auth screen from displaying multiple times.
            if False == result:
                break
            # end if
        # end for
        #// End foreach $themes.
        self.maintenance_mode(False)
        #// Refresh the Theme Update information.
        wp_clean_themes_cache(parsed_args["clear_update_cache"])
        #// This action is documented in wp-admin/includes/class-wp-upgrader.php
        do_action("upgrader_process_complete", self, Array({"action": "update", "type": "theme", "bulk": True, "themes": themes}))
        self.skin.bulk_footer()
        self.skin.footer()
        #// Cleanup our hooks, in case something else does a upgrade on this connection.
        remove_filter("upgrader_pre_install", Array(self, "current_before"))
        remove_filter("upgrader_post_install", Array(self, "current_after"))
        remove_filter("upgrader_clear_destination", Array(self, "delete_old_theme"))
        return results
    # end def bulk_upgrade
    #// 
    #// Check that the package source contains a valid theme.
    #// 
    #// Hooked to the {@see 'upgrader_source_selection'} filter by Theme_Upgrader::install().
    #// It will return an error if the theme doesn't have style.css or index.php
    #// files.
    #// 
    #// @since 3.3.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
    #// 
    #// @param string $source The full path to the package source.
    #// @return string|WP_Error The source or a WP_Error.
    #//
    def check_package(self, source=None):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        if is_wp_error(source):
            return source
        # end if
        #// Check that the folder contains a valid theme.
        working_directory = php_str_replace(wp_filesystem.wp_content_dir(), trailingslashit(WP_CONTENT_DIR), source)
        if (not php_is_dir(working_directory)):
            #// Sanity check, if the above fails, let's not prevent installation.
            return source
        # end if
        #// A proper archive should have a style.css file in the single subdirectory.
        if (not php_file_exists(working_directory + "style.css")):
            return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive_theme_no_style", self.strings["incompatible_archive"], php_sprintf(__("The theme is missing the %s stylesheet."), "<code>style.css</code>")))
        # end if
        info = get_file_data(working_directory + "style.css", Array({"Name": "Theme Name", "Template": "Template"}))
        if php_empty(lambda : info["Name"]):
            return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive_theme_no_name", self.strings["incompatible_archive"], php_sprintf(__("The %s stylesheet doesn&#8217;t contain a valid theme header."), "<code>style.css</code>")))
        # end if
        #// If it's not a child theme, it must have at least an index.php to be legit.
        if php_empty(lambda : info["Template"]) and (not php_file_exists(working_directory + "index.php")):
            return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive_theme_no_index", self.strings["incompatible_archive"], php_sprintf(__("The theme is missing the %s file."), "<code>index.php</code>")))
        # end if
        return source
    # end def check_package
    #// 
    #// Turn on maintenance mode before attempting to upgrade the current theme.
    #// 
    #// Hooked to the {@see 'upgrader_pre_install'} filter by Theme_Upgrader::upgrade() and
    #// Theme_Upgrader::bulk_upgrade().
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool|WP_Error $return Upgrade offer return.
    #// @param array         $theme  Theme arguments.
    #// @return bool|WP_Error The passed in $return param or WP_Error.
    #//
    def current_before(self, return_=None, theme=None):
        
        if is_wp_error(return_):
            return return_
        # end if
        theme = theme["theme"] if (php_isset(lambda : theme["theme"])) else ""
        #// Only run if current theme
        if get_stylesheet() != theme:
            return return_
        # end if
        #// Change to maintenance mode. Bulk edit handles this separately.
        if (not self.bulk):
            self.maintenance_mode(True)
        # end if
        return return_
    # end def current_before
    #// 
    #// Turn off maintenance mode after upgrading the current theme.
    #// 
    #// Hooked to the {@see 'upgrader_post_install'} filter by Theme_Upgrader::upgrade()
    #// and Theme_Upgrader::bulk_upgrade().
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool|WP_Error $return Upgrade offer return.
    #// @param array         $theme  Theme arguments.
    #// @return bool|WP_Error The passed in $return param or WP_Error.
    #//
    def current_after(self, return_=None, theme=None):
        
        if is_wp_error(return_):
            return return_
        # end if
        theme = theme["theme"] if (php_isset(lambda : theme["theme"])) else ""
        #// Only run if current theme.
        if get_stylesheet() != theme:
            return return_
        # end if
        #// Ensure stylesheet name hasn't changed after the upgrade:
        if get_stylesheet() == theme and theme != self.result["destination_name"]:
            wp_clean_themes_cache()
            stylesheet = self.result["destination_name"]
            switch_theme(stylesheet)
        # end if
        #// Time to remove maintenance mode. Bulk edit handles this separately.
        if (not self.bulk):
            self.maintenance_mode(False)
        # end if
        return return_
    # end def current_after
    #// 
    #// Delete the old theme during an upgrade.
    #// 
    #// Hooked to the {@see 'upgrader_clear_destination'} filter by Theme_Upgrader::upgrade()
    #// and Theme_Upgrader::bulk_upgrade().
    #// 
    #// @since 2.8.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem Subclass
    #// 
    #// @param bool   $removed
    #// @param string $local_destination
    #// @param string $remote_destination
    #// @param array  $theme
    #// @return bool
    #//
    def delete_old_theme(self, removed=None, local_destination=None, remote_destination=None, theme=None):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        if is_wp_error(removed):
            return removed
            pass
        # end if
        if (not (php_isset(lambda : theme["theme"]))):
            return removed
        # end if
        theme = theme["theme"]
        themes_dir = trailingslashit(wp_filesystem.wp_themes_dir(theme))
        if wp_filesystem.exists(themes_dir + theme):
            if (not wp_filesystem.delete(themes_dir + theme, True)):
                return False
            # end if
        # end if
        return True
    # end def delete_old_theme
    #// 
    #// Get the WP_Theme object for a theme.
    #// 
    #// @since 2.8.0
    #// @since 3.0.0 The `$theme` argument was added.
    #// 
    #// @param string $theme The directory name of the theme. This is optional, and if not supplied,
    #// the directory name from the last result will be used.
    #// @return WP_Theme|false The theme's info object, or false `$theme` is not supplied
    #// and the last result isn't set.
    #//
    def theme_info(self, theme=None):
        
        if php_empty(lambda : theme):
            if (not php_empty(lambda : self.result["destination_name"])):
                theme = self.result["destination_name"]
            else:
                return False
            # end if
        # end if
        return wp_get_theme(theme)
    # end def theme_info
# end class Theme_Upgrader
