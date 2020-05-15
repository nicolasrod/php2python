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
#// Upgrade API: Language_Pack_Upgrader class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Core class used for updating/installing language packs (translations)
#// for plugins, themes, and core.
#// 
#// @since 3.7.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader.php.
#// 
#// @see WP_Upgrader
#//
class Language_Pack_Upgrader(WP_Upgrader):
    result = Array()
    bulk = True
    #// 
    #// Asynchronously upgrades language packs after other upgrades have been made.
    #// 
    #// Hooked to the {@see 'upgrader_process_complete'} action by default.
    #// 
    #// @since 3.7.0
    #// 
    #// @param false|WP_Upgrader $upgrader Optional. WP_Upgrader instance or false. If `$upgrader` is
    #// a Language_Pack_Upgrader instance, the method will bail to
    #// avoid recursion. Otherwise unused. Default false.
    #//
    @classmethod
    def async_upgrade(self, upgrader=False):
        
        #// Avoid recursion.
        if upgrader and type(upgrader).__name__ == "Language_Pack_Upgrader":
            return
        # end if
        #// Nothing to do?
        language_updates = wp_get_translation_updates()
        if (not language_updates):
            return
        # end if
        #// 
        #// Avoid messing with VCS installations, at least for now.
        #// Noted: this is not the ideal way to accomplish this.
        #//
        check_vcs = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
        if check_vcs.is_vcs_checkout(WP_CONTENT_DIR):
            return
        # end if
        for key,language_update in language_updates:
            update = (not php_empty(lambda : language_update.autoupdate))
            #// 
            #// Filters whether to asynchronously update translation for core, a plugin, or a theme.
            #// 
            #// @since 4.0.0
            #// 
            #// @param bool   $update          Whether to update.
            #// @param object $language_update The update offer.
            #//
            update = apply_filters("async_update_translation", update, language_update)
            if (not update):
                language_updates[key] = None
            # end if
        # end for
        if php_empty(lambda : language_updates):
            return
        # end if
        #// Re-use the automatic upgrader skin if the parent upgrader is using it.
        if upgrader and type(upgrader.skin).__name__ == "Automatic_Upgrader_Skin":
            skin = upgrader.skin
        else:
            skin = php_new_class("Language_Pack_Upgrader_Skin", lambda : Language_Pack_Upgrader_Skin(Array({"skip_header_footer": True})))
        # end if
        lp_upgrader = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(skin))
        lp_upgrader.bulk_upgrade(language_updates)
    # end def async_upgrade
    #// 
    #// Initialize the upgrade strings.
    #// 
    #// @since 3.7.0
    #//
    def upgrade_strings(self):
        
        self.strings["starting_upgrade"] = __("Some of your translations need updating. Sit tight for a few more seconds while we update them as well.")
        self.strings["up_to_date"] = __("Your translations are all up to date.")
        self.strings["no_package"] = __("Update package not available.")
        #// translators: %s: Package URL.
        self.strings["downloading_package"] = php_sprintf(__("Downloading translation from %s&#8230;"), "<span class=\"code\">%s</span>")
        self.strings["unpack_package"] = __("Unpacking the update&#8230;")
        self.strings["process_failed"] = __("Translation update failed.")
        self.strings["process_success"] = __("Translation updated successfully.")
        self.strings["remove_old"] = __("Removing the old version of the translation&#8230;")
        self.strings["remove_old_failed"] = __("Could not remove the old translation.")
    # end def upgrade_strings
    #// 
    #// Upgrade a language pack.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string|false $update Optional. Whether an update offer is available. Default false.
    #// @param array        $args   Optional. Other optional arguments, see
    #// Language_Pack_Upgrader::bulk_upgrade(). Default empty array.
    #// @return array|bool|WP_Error The result of the upgrade, or a WP_Error object instead.
    #//
    def upgrade(self, update=False, args=Array()):
        
        if update:
            update = Array(update)
        # end if
        results = self.bulk_upgrade(update, args)
        if (not php_is_array(results)):
            return results
        # end if
        return results[0]
    # end def upgrade
    #// 
    #// Bulk upgrade language packs.
    #// 
    #// @since 3.7.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
    #// 
    #// @param object[] $language_updates Optional. Array of language packs to update. @see wp_get_translation_updates().
    #// Default empty array.
    #// @param array    $args {
    #// Other arguments for upgrading multiple language packs. Default empty array.
    #// 
    #// @type bool $clear_update_cache Whether to clear the update cache when done.
    #// Default true.
    #// }
    #// @return array|bool|WP_Error Will return an array of results, or true if there are no updates,
    #// false or WP_Error for initial errors.
    #//
    def bulk_upgrade(self, language_updates=Array(), args=Array()):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        defaults = Array({"clear_update_cache": True})
        parsed_args = wp_parse_args(args, defaults)
        self.init()
        self.upgrade_strings()
        if (not language_updates):
            language_updates = wp_get_translation_updates()
        # end if
        if php_empty(lambda : language_updates):
            self.skin.header()
            self.skin.set_result(True)
            self.skin.feedback("up_to_date")
            self.skin.bulk_footer()
            self.skin.footer()
            return True
        # end if
        if "upgrader_process_complete" == current_filter():
            self.skin.feedback("starting_upgrade")
        # end if
        #// Remove any existing upgrade filters from the plugin/theme upgraders #WP29425 & #WP29230.
        remove_all_filters("upgrader_pre_install")
        remove_all_filters("upgrader_clear_destination")
        remove_all_filters("upgrader_post_install")
        remove_all_filters("upgrader_source_selection")
        add_filter("upgrader_source_selection", Array(self, "check_package"), 10, 2)
        self.skin.header()
        #// Connect to the filesystem first.
        res = self.fs_connect(Array(WP_CONTENT_DIR, WP_LANG_DIR))
        if (not res):
            self.skin.footer()
            return False
        # end if
        results = Array()
        self.update_count = php_count(language_updates)
        self.update_current = 0
        #// 
        #// The filesystem's mkdir() is not recursive. Make sure WP_LANG_DIR exists,
        #// as we then may need to create a /plugins or /themes directory inside of it.
        #//
        remote_destination = wp_filesystem.find_folder(WP_LANG_DIR)
        if (not wp_filesystem.exists(remote_destination)):
            if (not wp_filesystem.mkdir(remote_destination, FS_CHMOD_DIR)):
                return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_lang_dir", self.strings["mkdir_failed"], remote_destination))
            # end if
        # end if
        language_updates_results = Array()
        for language_update in language_updates:
            self.skin.language_update = language_update
            destination = WP_LANG_DIR
            if "plugin" == language_update.type:
                destination += "/plugins"
            elif "theme" == language_update.type:
                destination += "/themes"
            # end if
            self.update_current += 1
            options = Array({"package": language_update.package, "destination": destination, "clear_destination": True, "abort_if_destination_exists": False, "clear_working": True, "is_multi": True, "hook_extra": Array({"language_update_type": language_update.type, "language_update": language_update})})
            result = self.run(options)
            results[-1] = self.result
            #// Prevent credentials auth screen from displaying multiple times.
            if False == result:
                break
            # end if
            language_updates_results[-1] = Array({"language": language_update.language, "type": language_update.type, "slug": language_update.slug if (php_isset(lambda : language_update.slug)) else "default", "version": language_update.version})
        # end for
        #// Remove upgrade hooks which are not required for translation updates.
        remove_action("upgrader_process_complete", Array("Language_Pack_Upgrader", "async_upgrade"), 20)
        remove_action("upgrader_process_complete", "wp_version_check")
        remove_action("upgrader_process_complete", "wp_update_plugins")
        remove_action("upgrader_process_complete", "wp_update_themes")
        #// This action is documented in wp-admin/includes/class-wp-upgrader.php
        do_action("upgrader_process_complete", self, Array({"action": "update", "type": "translation", "bulk": True, "translations": language_updates_results}))
        #// Re-add upgrade hooks.
        add_action("upgrader_process_complete", Array("Language_Pack_Upgrader", "async_upgrade"), 20)
        add_action("upgrader_process_complete", "wp_version_check", 10, 0)
        add_action("upgrader_process_complete", "wp_update_plugins", 10, 0)
        add_action("upgrader_process_complete", "wp_update_themes", 10, 0)
        self.skin.bulk_footer()
        self.skin.footer()
        #// Clean up our hooks, in case something else does an upgrade on this connection.
        remove_filter("upgrader_source_selection", Array(self, "check_package"))
        if parsed_args["clear_update_cache"]:
            wp_clean_update_cache()
        # end if
        return results
    # end def bulk_upgrade
    #// 
    #// Check the package source to make sure there are .mo and .po files.
    #// 
    #// Hooked to the {@see 'upgrader_source_selection'} filter by
    #// Language_Pack_Upgrader::bulk_upgrade().
    #// 
    #// @since 3.7.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem Subclass
    #// 
    #// @param string|WP_Error $source
    #// @param string          $remote_source
    #//
    def check_package(self, source=None, remote_source=None):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        if is_wp_error(source):
            return source
        # end if
        #// Check that the folder contains a valid language.
        files = wp_filesystem.dirlist(remote_source)
        #// Check to see if a .po and .mo exist in the folder.
        po = False
        mo = False
        for file,filedata in files:
            if ".po" == php_substr(file, -3):
                po = True
            elif ".mo" == php_substr(file, -3):
                mo = True
            # end if
        # end for
        if (not mo) or (not po):
            return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive_pomo", self.strings["incompatible_archive"], php_sprintf(__("The language pack is missing either the %1$s or %2$s files."), "<code>.po</code>", "<code>.mo</code>")))
        # end if
        return source
    # end def check_package
    #// 
    #// Get the name of an item being updated.
    #// 
    #// @since 3.7.0
    #// 
    #// @param object $update The data for an update.
    #// @return string The name of the item being updated.
    #//
    def get_name_for_update(self, update=None):
        
        for case in Switch(update.type):
            if case("core"):
                return "WordPress"
            # end if
            if case("theme"):
                theme = wp_get_theme(update.slug)
                if theme.exists():
                    return theme.get("Name")
                # end if
                break
            # end if
            if case("plugin"):
                plugin_data = get_plugins("/" + update.slug)
                plugin_data = reset(plugin_data)
                if plugin_data:
                    return plugin_data["Name"]
                # end if
                break
            # end if
        # end for
        return ""
    # end def get_name_for_update
    #// 
    #// Clears existing translations where this item is going to be installed into.
    #// 
    #// @since 5.1.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
    #// 
    #// @param string $remote_destination The location on the remote filesystem to be cleared.
    #// @return bool|WP_Error True upon success, WP_Error on failure.
    #//
    def clear_destination(self, remote_destination=None):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        language_update = self.skin.language_update
        language_directory = WP_LANG_DIR + "/"
        #// Local path for use with glob().
        if "core" == language_update.type:
            files = Array(remote_destination + language_update.language + ".po", remote_destination + language_update.language + ".mo", remote_destination + "admin-" + language_update.language + ".po", remote_destination + "admin-" + language_update.language + ".mo", remote_destination + "admin-network-" + language_update.language + ".po", remote_destination + "admin-network-" + language_update.language + ".mo", remote_destination + "continents-cities-" + language_update.language + ".po", remote_destination + "continents-cities-" + language_update.language + ".mo")
            json_translation_files = glob(language_directory + language_update.language + "-*.json")
            if json_translation_files:
                for json_translation_file in json_translation_files:
                    files[-1] = php_str_replace(language_directory, remote_destination, json_translation_file)
                # end for
            # end if
        else:
            files = Array(remote_destination + language_update.slug + "-" + language_update.language + ".po", remote_destination + language_update.slug + "-" + language_update.language + ".mo")
            language_directory = language_directory + language_update.type + "s/"
            json_translation_files = glob(language_directory + language_update.slug + "-" + language_update.language + "-*.json")
            if json_translation_files:
                for json_translation_file in json_translation_files:
                    files[-1] = php_str_replace(language_directory, remote_destination, json_translation_file)
                # end for
            # end if
        # end if
        files = php_array_filter(files, Array(wp_filesystem, "exists"))
        #// No files to delete.
        if (not files):
            return True
        # end if
        #// Check all files are writable before attempting to clear the destination.
        unwritable_files = Array()
        #// Check writability.
        for file in files:
            if (not wp_filesystem.is_writable(file)):
                #// Attempt to alter permissions to allow writes and try again.
                wp_filesystem.chmod(file, FS_CHMOD_FILE)
                if (not wp_filesystem.is_writable(file)):
                    unwritable_files[-1] = file
                # end if
            # end if
        # end for
        if (not php_empty(lambda : unwritable_files)):
            return php_new_class("WP_Error", lambda : WP_Error("files_not_writable", self.strings["files_not_writable"], php_implode(", ", unwritable_files)))
        # end if
        for file in files:
            if (not wp_filesystem.delete(file)):
                return php_new_class("WP_Error", lambda : WP_Error("remove_old_failed", self.strings["remove_old_failed"]))
            # end if
        # end for
        return True
    # end def clear_destination
# end class Language_Pack_Upgrader
