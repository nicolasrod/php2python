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
    #// 
    #// Result of the language pack upgrade.
    #// 
    #// @since 3.7.0
    #// @var array|WP_Error $result
    #// @see WP_Upgrader::$result
    #//
    result = Array()
    #// 
    #// Whether a bulk upgrade/installation is being performed.
    #// 
    #// @since 3.7.0
    #// @var bool $bulk
    #//
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
    def async_upgrade(self, upgrader_=None):
        if upgrader_ is None:
            upgrader_ = False
        # end if
        
        #// Avoid recursion.
        if upgrader_ and type(upgrader_).__name__ == "Language_Pack_Upgrader":
            return
        # end if
        #// Nothing to do?
        language_updates_ = wp_get_translation_updates()
        if (not language_updates_):
            return
        # end if
        #// 
        #// Avoid messing with VCS installations, at least for now.
        #// Noted: this is not the ideal way to accomplish this.
        #//
        check_vcs_ = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
        if check_vcs_.is_vcs_checkout(WP_CONTENT_DIR):
            return
        # end if
        for key_,language_update_ in language_updates_.items():
            update_ = (not php_empty(lambda : language_update_.autoupdate))
            #// 
            #// Filters whether to asynchronously update translation for core, a plugin, or a theme.
            #// 
            #// @since 4.0.0
            #// 
            #// @param bool   $update          Whether to update.
            #// @param object $language_update The update offer.
            #//
            update_ = apply_filters("async_update_translation", update_, language_update_)
            if (not update_):
                language_updates_[key_] = None
            # end if
        # end for
        if php_empty(lambda : language_updates_):
            return
        # end if
        #// Re-use the automatic upgrader skin if the parent upgrader is using it.
        if upgrader_ and type(upgrader_.skin).__name__ == "Automatic_Upgrader_Skin":
            skin_ = upgrader_.skin
        else:
            skin_ = php_new_class("Language_Pack_Upgrader_Skin", lambda : Language_Pack_Upgrader_Skin(Array({"skip_header_footer": True})))
        # end if
        lp_upgrader_ = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(skin_))
        lp_upgrader_.bulk_upgrade(language_updates_)
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
    def upgrade(self, update_=None, args_=None):
        if update_ is None:
            update_ = False
        # end if
        if args_ is None:
            args_ = Array()
        # end if
        
        if update_:
            update_ = Array(update_)
        # end if
        results_ = self.bulk_upgrade(update_, args_)
        if (not php_is_array(results_)):
            return results_
        # end if
        return results_[0]
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
    def bulk_upgrade(self, language_updates_=None, args_=None):
        if language_updates_ is None:
            language_updates_ = Array()
        # end if
        if args_ is None:
            args_ = Array()
        # end if
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        defaults_ = Array({"clear_update_cache": True})
        parsed_args_ = wp_parse_args(args_, defaults_)
        self.init()
        self.upgrade_strings()
        if (not language_updates_):
            language_updates_ = wp_get_translation_updates()
        # end if
        if php_empty(lambda : language_updates_):
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
        res_ = self.fs_connect(Array(WP_CONTENT_DIR, WP_LANG_DIR))
        if (not res_):
            self.skin.footer()
            return False
        # end if
        results_ = Array()
        self.update_count = php_count(language_updates_)
        self.update_current = 0
        #// 
        #// The filesystem's mkdir() is not recursive. Make sure WP_LANG_DIR exists,
        #// as we then may need to create a /plugins or /themes directory inside of it.
        #//
        remote_destination_ = wp_filesystem_.find_folder(WP_LANG_DIR)
        if (not wp_filesystem_.exists(remote_destination_)):
            if (not wp_filesystem_.mkdir(remote_destination_, FS_CHMOD_DIR)):
                return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_lang_dir", self.strings["mkdir_failed"], remote_destination_))
            # end if
        # end if
        language_updates_results_ = Array()
        for language_update_ in language_updates_:
            self.skin.language_update = language_update_
            destination_ = WP_LANG_DIR
            if "plugin" == language_update_.type:
                destination_ += "/plugins"
            elif "theme" == language_update_.type:
                destination_ += "/themes"
            # end if
            self.update_current += 1
            options_ = Array({"package": language_update_.package, "destination": destination_, "clear_destination": True, "abort_if_destination_exists": False, "clear_working": True, "is_multi": True, "hook_extra": Array({"language_update_type": language_update_.type, "language_update": language_update_})})
            result_ = self.run(options_)
            results_[-1] = self.result
            #// Prevent credentials auth screen from displaying multiple times.
            if False == result_:
                break
            # end if
            language_updates_results_[-1] = Array({"language": language_update_.language, "type": language_update_.type, "slug": language_update_.slug if (php_isset(lambda : language_update_.slug)) else "default", "version": language_update_.version})
        # end for
        #// Remove upgrade hooks which are not required for translation updates.
        remove_action("upgrader_process_complete", Array("Language_Pack_Upgrader", "async_upgrade"), 20)
        remove_action("upgrader_process_complete", "wp_version_check")
        remove_action("upgrader_process_complete", "wp_update_plugins")
        remove_action("upgrader_process_complete", "wp_update_themes")
        #// This action is documented in wp-admin/includes/class-wp-upgrader.php
        do_action("upgrader_process_complete", self, Array({"action": "update", "type": "translation", "bulk": True, "translations": language_updates_results_}))
        #// Re-add upgrade hooks.
        add_action("upgrader_process_complete", Array("Language_Pack_Upgrader", "async_upgrade"), 20)
        add_action("upgrader_process_complete", "wp_version_check", 10, 0)
        add_action("upgrader_process_complete", "wp_update_plugins", 10, 0)
        add_action("upgrader_process_complete", "wp_update_themes", 10, 0)
        self.skin.bulk_footer()
        self.skin.footer()
        #// Clean up our hooks, in case something else does an upgrade on this connection.
        remove_filter("upgrader_source_selection", Array(self, "check_package"))
        if parsed_args_["clear_update_cache"]:
            wp_clean_update_cache()
        # end if
        return results_
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
    def check_package(self, source_=None, remote_source_=None):
        
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        if is_wp_error(source_):
            return source_
        # end if
        #// Check that the folder contains a valid language.
        files_ = wp_filesystem_.dirlist(remote_source_)
        #// Check to see if a .po and .mo exist in the folder.
        po_ = False
        mo_ = False
        for file_,filedata_ in files_.items():
            if ".po" == php_substr(file_, -3):
                po_ = True
            elif ".mo" == php_substr(file_, -3):
                mo_ = True
            # end if
        # end for
        if (not mo_) or (not po_):
            return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive_pomo", self.strings["incompatible_archive"], php_sprintf(__("The language pack is missing either the %1$s or %2$s files."), "<code>.po</code>", "<code>.mo</code>")))
        # end if
        return source_
    # end def check_package
    #// 
    #// Get the name of an item being updated.
    #// 
    #// @since 3.7.0
    #// 
    #// @param object $update The data for an update.
    #// @return string The name of the item being updated.
    #//
    def get_name_for_update(self, update_=None):
        
        
        for case in Switch(update_.type):
            if case("core"):
                return "WordPress"
            # end if
            if case("theme"):
                theme_ = wp_get_theme(update_.slug)
                if theme_.exists():
                    return theme_.get("Name")
                # end if
                break
            # end if
            if case("plugin"):
                plugin_data_ = get_plugins("/" + update_.slug)
                plugin_data_ = reset(plugin_data_)
                if plugin_data_:
                    return plugin_data_["Name"]
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
    def clear_destination(self, remote_destination_=None):
        
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        language_update_ = self.skin.language_update
        language_directory_ = WP_LANG_DIR + "/"
        #// Local path for use with glob().
        if "core" == language_update_.type:
            files_ = Array(remote_destination_ + language_update_.language + ".po", remote_destination_ + language_update_.language + ".mo", remote_destination_ + "admin-" + language_update_.language + ".po", remote_destination_ + "admin-" + language_update_.language + ".mo", remote_destination_ + "admin-network-" + language_update_.language + ".po", remote_destination_ + "admin-network-" + language_update_.language + ".mo", remote_destination_ + "continents-cities-" + language_update_.language + ".po", remote_destination_ + "continents-cities-" + language_update_.language + ".mo")
            json_translation_files_ = glob(language_directory_ + language_update_.language + "-*.json")
            if json_translation_files_:
                for json_translation_file_ in json_translation_files_:
                    files_[-1] = php_str_replace(language_directory_, remote_destination_, json_translation_file_)
                # end for
            # end if
        else:
            files_ = Array(remote_destination_ + language_update_.slug + "-" + language_update_.language + ".po", remote_destination_ + language_update_.slug + "-" + language_update_.language + ".mo")
            language_directory_ = language_directory_ + language_update_.type + "s/"
            json_translation_files_ = glob(language_directory_ + language_update_.slug + "-" + language_update_.language + "-*.json")
            if json_translation_files_:
                for json_translation_file_ in json_translation_files_:
                    files_[-1] = php_str_replace(language_directory_, remote_destination_, json_translation_file_)
                # end for
            # end if
        # end if
        files_ = php_array_filter(files_, Array(wp_filesystem_, "exists"))
        #// No files to delete.
        if (not files_):
            return True
        # end if
        #// Check all files are writable before attempting to clear the destination.
        unwritable_files_ = Array()
        #// Check writability.
        for file_ in files_:
            if (not wp_filesystem_.is_writable(file_)):
                #// Attempt to alter permissions to allow writes and try again.
                wp_filesystem_.chmod(file_, FS_CHMOD_FILE)
                if (not wp_filesystem_.is_writable(file_)):
                    unwritable_files_[-1] = file_
                # end if
            # end if
        # end for
        if (not php_empty(lambda : unwritable_files_)):
            return php_new_class("WP_Error", lambda : WP_Error("files_not_writable", self.strings["files_not_writable"], php_implode(", ", unwritable_files_)))
        # end if
        for file_ in files_:
            if (not wp_filesystem_.delete(file_)):
                return php_new_class("WP_Error", lambda : WP_Error("remove_old_failed", self.strings["remove_old_failed"]))
            # end if
        # end for
        return True
    # end def clear_destination
# end class Language_Pack_Upgrader
