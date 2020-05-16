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
#// Upgrade API: Core_Upgrader class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Core class used for updating core.
#// 
#// It allows for WordPress to upgrade itself in combination with
#// the wp-admin/includes/update-core.php file.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader.php.
#// 
#// @see WP_Upgrader
#//
class Core_Upgrader(WP_Upgrader):
    #// 
    #// Initialize the upgrade strings.
    #// 
    #// @since 2.8.0
    #//
    def upgrade_strings(self):
        
        self.strings["up_to_date"] = __("WordPress is at the latest version.")
        self.strings["locked"] = __("Another update is currently in progress.")
        self.strings["no_package"] = __("Update package not available.")
        #// translators: %s: Package URL.
        self.strings["downloading_package"] = php_sprintf(__("Downloading update from %s&#8230;"), "<span class=\"code\">%s</span>")
        self.strings["unpack_package"] = __("Unpacking the update&#8230;")
        self.strings["copy_failed"] = __("Could not copy files.")
        self.strings["copy_failed_space"] = __("Could not copy files. You may have run out of disk space.")
        self.strings["start_rollback"] = __("Attempting to roll back to previous version.")
        self.strings["rollback_was_required"] = __("Due to an error during updating, WordPress has rolled back to your previous version.")
    # end def upgrade_strings
    #// 
    #// Upgrade WordPress core.
    #// 
    #// @since 2.8.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem                WordPress filesystem subclass.
    #// @global callable           $_wp_filesystem_direct_method
    #// 
    #// @param object $current Response object for whether WordPress is current.
    #// @param array  $args {
    #// Optional. Arguments for upgrading WordPress core. Default empty array.
    #// 
    #// @type bool $pre_check_md5    Whether to check the file checksums before
    #// attempting the upgrade. Default true.
    #// @type bool $attempt_rollback Whether to attempt to rollback the chances if
    #// there is a problem. Default false.
    #// @type bool $do_rollback      Whether to perform this "upgrade" as a rollback.
    #// Default false.
    #// }
    #// @return string|false|WP_Error New WordPress version on success, false or WP_Error on failure.
    #//
    def upgrade(self, current=None, args=Array()):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        php_include_file(ABSPATH + WPINC + "/version.php", once=False)
        #// $wp_version;
        start_time = time()
        defaults = Array({"pre_check_md5": True, "attempt_rollback": False, "do_rollback": False, "allow_relaxed_file_ownership": False})
        parsed_args = wp_parse_args(args, defaults)
        self.init()
        self.upgrade_strings()
        #// Is an update available?
        if (not (php_isset(lambda : current.response))) or "latest" == current.response:
            return php_new_class("WP_Error", lambda : WP_Error("up_to_date", self.strings["up_to_date"]))
        # end if
        res = self.fs_connect(Array(ABSPATH, WP_CONTENT_DIR), parsed_args["allow_relaxed_file_ownership"])
        if (not res) or is_wp_error(res):
            return res
        # end if
        wp_dir = trailingslashit(wp_filesystem.abspath())
        partial = True
        if parsed_args["do_rollback"]:
            partial = False
        elif parsed_args["pre_check_md5"] and (not self.check_files()):
            partial = False
        # end if
        #// 
        #// If partial update is returned from the API, use that, unless we're doing
        #// a reinstallation. If we cross the new_bundled version number, then use
        #// the new_bundled zip. Don't though if the constant is set to skip bundled items.
        #// If the API returns a no_content zip, go with it. Finally, default to the full zip.
        #//
        if parsed_args["do_rollback"] and current.packages.rollback:
            to_download = "rollback"
        elif current.packages.partial and "reinstall" != current.response and wp_version == current.partial_version and partial:
            to_download = "partial"
        elif current.packages.new_bundled and php_version_compare(wp_version, current.new_bundled, "<") and (not php_defined("CORE_UPGRADE_SKIP_NEW_BUNDLED")) or (not CORE_UPGRADE_SKIP_NEW_BUNDLED):
            to_download = "new_bundled"
        elif current.packages.no_content:
            to_download = "no_content"
        else:
            to_download = "full"
        # end if
        #// Lock to prevent multiple Core Updates occurring.
        lock = WP_Upgrader.create_lock("core_updater", 15 * MINUTE_IN_SECONDS)
        if (not lock):
            return php_new_class("WP_Error", lambda : WP_Error("locked", self.strings["locked"]))
        # end if
        download = self.download_package(current.packages.to_download, True)
        #// Allow for signature soft-fail.
        #// WARNING: This may be removed in the future.
        if is_wp_error(download) and download.get_error_data("softfail-filename"):
            #// Outout the failure error as a normal feedback, and not as an error:
            #// This filter is documented in wp-admin/includes/update-core.php
            apply_filters("update_feedback", download.get_error_message())
            #// Report this failure back to WordPress.org for debugging purposes.
            wp_version_check(Array({"signature_failure_code": download.get_error_code(), "signature_failure_data": download.get_error_data()}))
            #// Pretend this error didn't happen.
            download = download.get_error_data("softfail-filename")
        # end if
        if is_wp_error(download):
            WP_Upgrader.release_lock("core_updater")
            return download
        # end if
        working_dir = self.unpack_package(download)
        if is_wp_error(working_dir):
            WP_Upgrader.release_lock("core_updater")
            return working_dir
        # end if
        #// Copy update-core.php from the new version into place.
        if (not wp_filesystem.copy(working_dir + "/wordpress/wp-admin/includes/update-core.php", wp_dir + "wp-admin/includes/update-core.php", True)):
            wp_filesystem.delete(working_dir, True)
            WP_Upgrader.release_lock("core_updater")
            return php_new_class("WP_Error", lambda : WP_Error("copy_failed_for_update_core_file", __("The update cannot be installed because we will be unable to copy some files. This is usually due to inconsistent file permissions."), "wp-admin/includes/update-core.php"))
        # end if
        wp_filesystem.chmod(wp_dir + "wp-admin/includes/update-core.php", FS_CHMOD_FILE)
        php_include_file(ABSPATH + "wp-admin/includes/update-core.php", once=True)
        if (not php_function_exists("update_core")):
            WP_Upgrader.release_lock("core_updater")
            return php_new_class("WP_Error", lambda : WP_Error("copy_failed_space", self.strings["copy_failed_space"]))
        # end if
        result = update_core(working_dir, wp_dir)
        #// In the event of an issue, we may be able to roll back.
        if parsed_args["attempt_rollback"] and current.packages.rollback and (not parsed_args["do_rollback"]):
            try_rollback = False
            if is_wp_error(result):
                error_code = result.get_error_code()
                #// 
                #// Not all errors are equal. These codes are critical: copy_failed__copy_dir,
                #// mkdir_failed__copy_dir, copy_failed__copy_dir_retry, and disk_full.
                #// do_rollback allows for update_core() to trigger a rollback if needed.
                #//
                if False != php_strpos(error_code, "do_rollback"):
                    try_rollback = True
                elif False != php_strpos(error_code, "__copy_dir"):
                    try_rollback = True
                elif "disk_full" == error_code:
                    try_rollback = True
                # end if
            # end if
            if try_rollback:
                #// This filter is documented in wp-admin/includes/update-core.php
                apply_filters("update_feedback", result)
                #// This filter is documented in wp-admin/includes/update-core.php
                apply_filters("update_feedback", self.strings["start_rollback"])
                rollback_result = self.upgrade(current, php_array_merge(parsed_args, Array({"do_rollback": True})))
                original_result = result
                result = php_new_class("WP_Error", lambda : WP_Error("rollback_was_required", self.strings["rollback_was_required"], Array({"update": original_result, "rollback": rollback_result})))
            # end if
        # end if
        #// This action is documented in wp-admin/includes/class-wp-upgrader.php
        do_action("upgrader_process_complete", self, Array({"action": "update", "type": "core"}))
        #// Clear the current updates.
        delete_site_transient("update_core")
        if (not parsed_args["do_rollback"]):
            stats = Array({"update_type": current.response, "success": True, "fs_method": wp_filesystem.method, "fs_method_forced": php_defined("FS_METHOD") or has_filter("filesystem_method"), "fs_method_direct": PHP_GLOBALS["_wp_filesystem_direct_method"] if (not php_empty(lambda : PHP_GLOBALS["_wp_filesystem_direct_method"])) else "", "time_taken": time() - start_time, "reported": wp_version, "attempted": current.version})
            if is_wp_error(result):
                stats["success"] = False
                #// Did a rollback occur?
                if (not php_empty(lambda : try_rollback)):
                    stats["error_code"] = original_result.get_error_code()
                    stats["error_data"] = original_result.get_error_data()
                    #// Was the rollback successful? If not, collect its error too.
                    stats["rollback"] = (not is_wp_error(rollback_result))
                    if is_wp_error(rollback_result):
                        stats["rollback_code"] = rollback_result.get_error_code()
                        stats["rollback_data"] = rollback_result.get_error_data()
                    # end if
                else:
                    stats["error_code"] = result.get_error_code()
                    stats["error_data"] = result.get_error_data()
                # end if
            # end if
            wp_version_check(stats)
        # end if
        WP_Upgrader.release_lock("core_updater")
        return result
    # end def upgrade
    #// 
    #// Determines if this WordPress Core version should update to an offered version or not.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $offered_ver The offered version, of the format x.y.z.
    #// @return bool True if we should update to the offered version, otherwise false.
    #//
    @classmethod
    def should_update_to_version(self, offered_ver=None):
        
        php_include_file(ABSPATH + WPINC + "/version.php", once=False)
        #// $wp_version; // x.y.z
        current_branch = php_implode(".", php_array_slice(php_preg_split("/[.-]/", wp_version), 0, 2))
        #// x.y
        new_branch = php_implode(".", php_array_slice(php_preg_split("/[.-]/", offered_ver), 0, 2))
        #// x.y
        current_is_development_version = php_bool(php_strpos(wp_version, "-"))
        #// Defaults:
        upgrade_dev = True
        upgrade_minor = True
        upgrade_major = False
        #// WP_AUTO_UPDATE_CORE = true (all), 'minor', false.
        if php_defined("WP_AUTO_UPDATE_CORE"):
            if False == WP_AUTO_UPDATE_CORE:
                #// Defaults to turned off, unless a filter allows it.
                upgrade_dev = False
                upgrade_minor = False
                upgrade_major = False
            elif True == WP_AUTO_UPDATE_CORE:
                #// ALL updates for core.
                upgrade_dev = True
                upgrade_minor = True
                upgrade_major = True
            elif "minor" == WP_AUTO_UPDATE_CORE:
                #// Only minor updates for core.
                upgrade_dev = False
                upgrade_minor = True
                upgrade_major = False
            # end if
        # end if
        #// 1: If we're already on that version, not much point in updating?
        if offered_ver == wp_version:
            return False
        # end if
        #// 2: If we're running a newer version, that's a nope.
        if php_version_compare(wp_version, offered_ver, ">"):
            return False
        # end if
        failure_data = get_site_option("auto_core_update_failed")
        if failure_data:
            #// If this was a critical update failure, cannot update.
            if (not php_empty(lambda : failure_data["critical"])):
                return False
            # end if
            #// Don't claim we can update on update-core.php if we have a non-critical failure logged.
            if wp_version == failure_data["current"] and False != php_strpos(offered_ver, ".1.next.minor"):
                return False
            # end if
            #// 
            #// Cannot update if we're retrying the same A to B update that caused a non-critical failure.
            #// Some non-critical failures do allow retries, like download_failed.
            #// 3.7.1 => 3.7.2 resulted in files_not_writable, if we are still on 3.7.1 and still trying to update to 3.7.2.
            #//
            if php_empty(lambda : failure_data["retry"]) and wp_version == failure_data["current"] and offered_ver == failure_data["attempted"]:
                return False
            # end if
        # end if
        #// 3: 3.7-alpha-25000 -> 3.7-alpha-25678 -> 3.7-beta1 -> 3.7-beta2.
        if current_is_development_version:
            #// 
            #// Filters whether to enable automatic core updates for development versions.
            #// 
            #// @since 3.7.0
            #// 
            #// @param bool $upgrade_dev Whether to enable automatic updates for
            #// development versions.
            #//
            if (not apply_filters("allow_dev_auto_core_updates", upgrade_dev)):
                return False
            # end if
            pass
        # end if
        #// 4: Minor in-branch updates (3.7.0 -> 3.7.1 -> 3.7.2 -> 3.7.4).
        if current_branch == new_branch:
            #// 
            #// Filters whether to enable minor automatic core updates.
            #// 
            #// @since 3.7.0
            #// 
            #// @param bool $upgrade_minor Whether to enable minor automatic core updates.
            #//
            return apply_filters("allow_minor_auto_core_updates", upgrade_minor)
        # end if
        #// 5: Major version updates (3.7.0 -> 3.8.0 -> 3.9.1).
        if php_version_compare(new_branch, current_branch, ">"):
            #// 
            #// Filters whether to enable major automatic core updates.
            #// 
            #// @since 3.7.0
            #// 
            #// @param bool $upgrade_major Whether to enable major automatic core updates.
            #//
            return apply_filters("allow_major_auto_core_updates", upgrade_major)
        # end if
        #// If we're not sure, we don't want it.
        return False
    # end def should_update_to_version
    #// 
    #// Compare the disk file checksums against the expected checksums.
    #// 
    #// @since 3.7.0
    #// 
    #// @global string $wp_version       The WordPress version string.
    #// @global string $wp_local_package Locale code of the package.
    #// 
    #// @return bool True if the checksums match, otherwise false.
    #//
    def check_files(self):
        
        global wp_version,wp_local_package
        php_check_if_defined("wp_version","wp_local_package")
        checksums = get_core_checksums(wp_version, wp_local_package if (php_isset(lambda : wp_local_package)) else "en_US")
        if (not php_is_array(checksums)):
            return False
        # end if
        for file,checksum in checksums:
            #// Skip files which get updated.
            if "wp-content" == php_substr(file, 0, 10):
                continue
            # end if
            if (not php_file_exists(ABSPATH + file)) or php_md5_file(ABSPATH + file) != checksum:
                return False
            # end if
        # end for
        return True
    # end def check_files
# end class Core_Upgrader
