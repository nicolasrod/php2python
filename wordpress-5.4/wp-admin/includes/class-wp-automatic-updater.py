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
#// Upgrade API: WP_Automatic_Updater class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Core class used for handling automatic background updates.
#// 
#// @since 3.7.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader.php.
#//
class WP_Automatic_Updater():
    #// 
    #// Tracks update results during processing.
    #// 
    #// @var array
    #//
    update_results = Array()
    #// 
    #// Whether the entire automatic updater is disabled.
    #// 
    #// @since 3.7.0
    #//
    def is_disabled(self):
        
        
        #// Background updates are disabled if you don't want file changes.
        if (not wp_is_file_mod_allowed("automatic_updater")):
            return True
        # end if
        if wp_installing():
            return True
        # end if
        #// More fine grained control can be done through the WP_AUTO_UPDATE_CORE constant and filters.
        disabled_ = php_defined("AUTOMATIC_UPDATER_DISABLED") and AUTOMATIC_UPDATER_DISABLED
        #// 
        #// Filters whether to entirely disable background updates.
        #// 
        #// There are more fine-grained filters and controls for selective disabling.
        #// This filter parallels the AUTOMATIC_UPDATER_DISABLED constant in name.
        #// 
        #// This also disables update notification emails. That may change in the future.
        #// 
        #// @since 3.7.0
        #// 
        #// @param bool $disabled Whether the updater should be disabled.
        #//
        return apply_filters("automatic_updater_disabled", disabled_)
    # end def is_disabled
    #// 
    #// Check for version control checkouts.
    #// 
    #// Checks for Subversion, Git, Mercurial, and Bazaar. It recursively looks up the
    #// filesystem to the top of the drive, erring on the side of detecting a VCS
    #// checkout somewhere.
    #// 
    #// ABSPATH is always checked in addition to whatever $context is (which may be the
    #// wp-content directory, for example). The underlying assumption is that if you are
    #// using version control *anywhere*, then you should be making decisions for
    #// how things get updated.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $context The filesystem path to check, in addition to ABSPATH.
    #//
    def is_vcs_checkout(self, context_=None):
        
        
        context_dirs_ = Array(untrailingslashit(context_))
        if ABSPATH != context_:
            context_dirs_[-1] = untrailingslashit(ABSPATH)
        # end if
        vcs_dirs_ = Array(".svn", ".git", ".hg", ".bzr")
        check_dirs_ = Array()
        for context_dir_ in context_dirs_:
            #// Walk up from $context_dir to the root.
            while True:
                check_dirs_[-1] = context_dir_
                #// Once we've hit '/' or 'C:\', we need to stop. dirname will keep returning the input here.
                if php_dirname(context_dir_) == context_dir_:
                    break
                # end if
                pass
                context_dir_ = php_dirname(context_dir_)
                if context_dir_:
                    break
                # end if
            # end while
        # end for
        check_dirs_ = array_unique(check_dirs_)
        #// Search all directories we've found for evidence of version control.
        for vcs_dir_ in vcs_dirs_:
            for check_dir_ in check_dirs_:
                checkout_ = php_no_error(lambda: php_is_dir(php_rtrim(check_dir_, "\\/") + str("/") + str(vcs_dir_)))
                if checkout_:
                    break
                # end if
            # end for
        # end for
        #// 
        #// Filters whether the automatic updater should consider a filesystem
        #// location to be potentially managed by a version control system.
        #// 
        #// @since 3.7.0
        #// 
        #// @param bool $checkout  Whether a VCS checkout was discovered at $context
        #// or ABSPATH, or anywhere higher.
        #// @param string $context The filesystem context (a path) against which
        #// filesystem status should be checked.
        #//
        return apply_filters("automatic_updates_is_vcs_checkout", checkout_, context_)
    # end def is_vcs_checkout
    #// 
    #// Tests to see if we can and should update a specific item.
    #// 
    #// @since 3.7.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $type    The type of update being checked: 'core', 'theme',
    #// 'plugin', 'translation'.
    #// @param object $item    The update offer.
    #// @param string $context The filesystem context (a path) against which filesystem
    #// access and status should be checked.
    #//
    def should_update(self, type_=None, item_=None, context_=None):
        
        
        #// Used to see if WP_Filesystem is set up to allow unattended updates.
        skin_ = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
        if self.is_disabled():
            return False
        # end if
        #// Only relax the filesystem checks when the update doesn't include new files.
        allow_relaxed_file_ownership_ = False
        if "core" == type_ and (php_isset(lambda : item_.new_files)) and (not item_.new_files):
            allow_relaxed_file_ownership_ = True
        # end if
        #// If we can't do an auto core update, we may still be able to email the user.
        if (not skin_.request_filesystem_credentials(False, context_, allow_relaxed_file_ownership_)) or self.is_vcs_checkout(context_):
            if "core" == type_:
                self.send_core_update_notification_email(item_)
            # end if
            return False
        # end if
        #// Next up, is this an item we can update?
        if "core" == type_:
            update_ = Core_Upgrader.should_update_to_version(item_.current)
        else:
            update_ = (not php_empty(lambda : item_.autoupdate))
        # end if
        #// 
        #// Filters whether to automatically update core, a plugin, a theme, or a language.
        #// 
        #// The dynamic portion of the hook name, `$type`, refers to the type of update
        #// being checked. Can be 'core', 'theme', 'plugin', or 'translation'.
        #// 
        #// Generally speaking, plugins, themes, and major core versions are not updated
        #// by default, while translations and minor and development versions for core
        #// are updated by default.
        #// 
        #// See the {@see 'allow_dev_auto_core_updates'}, {@see 'allow_minor_auto_core_updates'},
        #// and {@see 'allow_major_auto_core_updates'} filters for a more straightforward way to
        #// adjust core updates.
        #// 
        #// @since 3.7.0
        #// 
        #// @param bool   $update Whether to update.
        #// @param object $item   The update offer.
        #//
        update_ = apply_filters(str("auto_update_") + str(type_), update_, item_)
        if (not update_):
            if "core" == type_:
                self.send_core_update_notification_email(item_)
            # end if
            return False
        # end if
        #// If it's a core update, are we actually compatible with its requirements?
        if "core" == type_:
            global wpdb_
            php_check_if_defined("wpdb_")
            php_compat_ = php_version_compare(php_phpversion(), item_.php_version, ">=")
            if php_file_exists(WP_CONTENT_DIR + "/db.php") and php_empty(lambda : wpdb_.is_mysql):
                mysql_compat_ = True
            else:
                mysql_compat_ = php_version_compare(wpdb_.db_version(), item_.mysql_version, ">=")
            # end if
            if (not php_compat_) or (not mysql_compat_):
                return False
            # end if
        # end if
        #// If updating a plugin, ensure the minimum PHP version requirements are satisfied.
        if "plugin" == type_:
            if (not php_empty(lambda : item_.requires_php)) and php_version_compare(php_phpversion(), item_.requires_php, "<"):
                return False
            # end if
        # end if
        return True
    # end def should_update
    #// 
    #// Notifies an administrator of a core update.
    #// 
    #// @since 3.7.0
    #// 
    #// @param object $item The update offer.
    #//
    def send_core_update_notification_email(self, item_=None):
        
        
        notified_ = get_site_option("auto_core_update_notified")
        #// Don't notify if we've already notified the same email address of the same version.
        if notified_ and get_site_option("admin_email") == notified_["email"] and notified_["version"] == item_.current:
            return False
        # end if
        #// See if we need to notify users of a core update.
        notify_ = (not php_empty(lambda : item_.notify_email))
        #// 
        #// Filters whether to notify the site administrator of a new core update.
        #// 
        #// By default, administrators are notified when the update offer received
        #// from WordPress.org sets a particular flag. This allows some discretion
        #// in if and when to notify.
        #// 
        #// This filter is only evaluated once per release. If the same email address
        #// was already notified of the same new version, WordPress won't repeatedly
        #// email the administrator.
        #// 
        #// This filter is also used on about.php to check if a plugin has disabled
        #// these notifications.
        #// 
        #// @since 3.7.0
        #// 
        #// @param bool   $notify Whether the site administrator is notified.
        #// @param object $item   The update offer.
        #//
        if (not apply_filters("send_core_update_notification_email", notify_, item_)):
            return False
        # end if
        self.send_email("manual", item_)
        return True
    # end def send_core_update_notification_email
    #// 
    #// Update an item, if appropriate.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $type The type of update being checked: 'core', 'theme', 'plugin', 'translation'.
    #// @param object $item The update offer.
    #// 
    #// @return null|WP_Error
    #//
    def update(self, type_=None, item_=None):
        
        
        skin_ = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
        for case in Switch(type_):
            if case("core"):
                #// The Core upgrader doesn't use the Upgrader's skin during the actual main part of the upgrade, instead, firing a filter.
                add_filter("update_feedback", Array(skin_, "feedback"))
                upgrader_ = php_new_class("Core_Upgrader", lambda : Core_Upgrader(skin_))
                context_ = ABSPATH
                break
            # end if
            if case("plugin"):
                upgrader_ = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(skin_))
                context_ = WP_PLUGIN_DIR
                break
            # end if
            if case("theme"):
                upgrader_ = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(skin_))
                context_ = get_theme_root(item_.theme)
                break
            # end if
            if case("translation"):
                upgrader_ = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(skin_))
                context_ = WP_CONTENT_DIR
                break
            # end if
        # end for
        #// Determine whether we can and should perform this update.
        if (not self.should_update(type_, item_, context_)):
            return False
        # end if
        #// 
        #// Fires immediately prior to an auto-update.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $type    The type of update being checked: 'core', 'theme', 'plugin', or 'translation'.
        #// @param object $item    The update offer.
        #// @param string $context The filesystem context (a path) against which filesystem access and status
        #// should be checked.
        #//
        do_action("pre_auto_update", type_, item_, context_)
        upgrader_item_ = item_
        for case in Switch(type_):
            if case("core"):
                #// translators: %s: WordPress version.
                skin_.feedback(__("Updating to WordPress %s"), item_.version)
                #// translators: %s: WordPress version.
                item_name_ = php_sprintf(__("WordPress %s"), item_.version)
                break
            # end if
            if case("theme"):
                upgrader_item_ = item_.theme
                theme_ = wp_get_theme(upgrader_item_)
                item_name_ = theme_.get("Name")
                #// translators: %s: Theme name.
                skin_.feedback(__("Updating theme: %s"), item_name_)
                break
            # end if
            if case("plugin"):
                upgrader_item_ = item_.plugin
                plugin_data_ = get_plugin_data(context_ + "/" + upgrader_item_)
                item_name_ = plugin_data_["Name"]
                #// translators: %s: Plugin name.
                skin_.feedback(__("Updating plugin: %s"), item_name_)
                break
            # end if
            if case("translation"):
                language_item_name_ = upgrader_.get_name_for_update(item_)
                #// translators: %s: Project name (plugin, theme, or WordPress).
                item_name_ = php_sprintf(__("Translations for %s"), language_item_name_)
                #// translators: 1: Project name (plugin, theme, or WordPress), 2: Language.
                skin_.feedback(php_sprintf(__("Updating translations for %1$s (%2$s)&#8230;"), language_item_name_, item_.language))
                break
            # end if
        # end for
        allow_relaxed_file_ownership_ = False
        if "core" == type_ and (php_isset(lambda : item_.new_files)) and (not item_.new_files):
            allow_relaxed_file_ownership_ = True
        # end if
        #// Boom, this site's about to get a whole new splash of paint!
        upgrade_result_ = upgrader_.upgrade(upgrader_item_, Array({"clear_update_cache": False, "pre_check_md5": False, "attempt_rollback": True, "allow_relaxed_file_ownership": allow_relaxed_file_ownership_}))
        #// If the filesystem is unavailable, false is returned.
        if False == upgrade_result_:
            upgrade_result_ = php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", __("Could not access filesystem.")))
        # end if
        if "core" == type_:
            if is_wp_error(upgrade_result_) and "up_to_date" == upgrade_result_.get_error_code() or "locked" == upgrade_result_.get_error_code():
                #// These aren't actual errors, treat it as a skipped-update instead to avoid triggering the post-core update failure routines.
                return False
            # end if
            #// Core doesn't output this, so let's append it so we don't get confused.
            if is_wp_error(upgrade_result_):
                skin_.error(__("Installation Failed"), upgrade_result_)
            else:
                skin_.feedback(__("WordPress updated successfully"))
            # end if
        # end if
        self.update_results[type_][-1] = Array({"item": item_, "result": upgrade_result_, "name": item_name_, "messages": skin_.get_upgrade_messages()})
        return upgrade_result_
    # end def update
    #// 
    #// Kicks off the background update process, looping through all pending updates.
    #// 
    #// @since 3.7.0
    #//
    def run(self):
        
        
        if self.is_disabled():
            return
        # end if
        if (not is_main_network()) or (not is_main_site()):
            return
        # end if
        if (not WP_Upgrader.create_lock("auto_updater")):
            return
        # end if
        #// Don't automatically run these things, as we'll handle it ourselves.
        remove_action("upgrader_process_complete", Array("Language_Pack_Upgrader", "async_upgrade"), 20)
        remove_action("upgrader_process_complete", "wp_version_check")
        remove_action("upgrader_process_complete", "wp_update_plugins")
        remove_action("upgrader_process_complete", "wp_update_themes")
        #// Next, plugins.
        wp_update_plugins()
        #// Check for plugin updates.
        plugin_updates_ = get_site_transient("update_plugins")
        if plugin_updates_ and (not php_empty(lambda : plugin_updates_.response)):
            for plugin_ in plugin_updates_.response:
                self.update("plugin", plugin_)
            # end for
            #// Force refresh of plugin update information.
            wp_clean_plugins_cache()
        # end if
        #// Next, those themes we all love.
        wp_update_themes()
        #// Check for theme updates.
        theme_updates_ = get_site_transient("update_themes")
        if theme_updates_ and (not php_empty(lambda : theme_updates_.response)):
            for theme_ in theme_updates_.response:
                self.update("theme", theme_)
            # end for
            #// Force refresh of theme update information.
            wp_clean_themes_cache()
        # end if
        #// Next, process any core update.
        wp_version_check()
        #// Check for core updates.
        core_update_ = find_core_auto_update()
        if core_update_:
            self.update("core", core_update_)
        # end if
        #// Clean up, and check for any pending translations.
        #// (Core_Upgrader checks for core updates.)
        theme_stats_ = Array()
        if (php_isset(lambda : self.update_results["theme"])):
            for upgrade_ in self.update_results["theme"]:
                theme_stats_[upgrade_.item.theme] = True == upgrade_.result
            # end for
        # end if
        wp_update_themes(theme_stats_)
        #// Check for theme updates.
        plugin_stats_ = Array()
        if (php_isset(lambda : self.update_results["plugin"])):
            for upgrade_ in self.update_results["plugin"]:
                plugin_stats_[upgrade_.item.plugin] = True == upgrade_.result
            # end for
        # end if
        wp_update_plugins(plugin_stats_)
        #// Check for plugin updates.
        #// Finally, process any new translations.
        language_updates_ = wp_get_translation_updates()
        if language_updates_:
            for update_ in language_updates_:
                self.update("translation", update_)
            # end for
            #// Clear existing caches.
            wp_clean_update_cache()
            wp_version_check()
            #// Check for core updates.
            wp_update_themes()
            #// Check for theme updates.
            wp_update_plugins()
            pass
        # end if
        #// Send debugging email to admin for all development installations.
        if (not php_empty(lambda : self.update_results)):
            development_version_ = False != php_strpos(get_bloginfo("version"), "-")
            #// 
            #// Filters whether to send a debugging email for each automatic background update.
            #// 
            #// @since 3.7.0
            #// 
            #// @param bool $development_version By default, emails are sent if the
            #// install is a development version.
            #// Return false to avoid the email.
            #//
            if apply_filters("automatic_updates_send_debug_email", development_version_):
                self.send_debug_email()
            # end if
            if (not php_empty(lambda : self.update_results["core"])):
                self.after_core_update(self.update_results["core"][0])
            # end if
            #// 
            #// Fires after all automatic updates have run.
            #// 
            #// @since 3.8.0
            #// 
            #// @param array $update_results The results of all attempted updates.
            #//
            do_action("automatic_updates_complete", self.update_results)
        # end if
        WP_Upgrader.release_lock("auto_updater")
    # end def run
    #// 
    #// If we tried to perform a core update, check if we should send an email,
    #// and if we need to avoid processing future updates.
    #// 
    #// @since 3.7.0
    #// 
    #// @param object $update_result The result of the core update. Includes the update offer and result.
    #//
    def after_core_update(self, update_result_=None):
        
        
        wp_version_ = get_bloginfo("version")
        core_update_ = update_result_.item
        result_ = update_result_.result
        if (not is_wp_error(result_)):
            self.send_email("success", core_update_)
            return
        # end if
        error_code_ = result_.get_error_code()
        #// Any of these WP_Error codes are critical failures, as in they occurred after we started to copy core files.
        #// We should not try to perform a background update again until there is a successful one-click update performed by the user.
        critical_ = False
        if "disk_full" == error_code_ or False != php_strpos(error_code_, "__copy_dir"):
            critical_ = True
        elif "rollback_was_required" == error_code_ and is_wp_error(result_.get_error_data().rollback):
            #// A rollback is only critical if it failed too.
            critical_ = True
            rollback_result_ = result_.get_error_data().rollback
        elif False != php_strpos(error_code_, "do_rollback"):
            critical_ = True
        # end if
        if critical_:
            critical_data_ = Array({"attempted": core_update_.current, "current": wp_version_, "error_code": error_code_, "error_data": result_.get_error_data(), "timestamp": time(), "critical": True})
            if (php_isset(lambda : rollback_result_)):
                critical_data_["rollback_code"] = rollback_result_.get_error_code()
                critical_data_["rollback_data"] = rollback_result_.get_error_data()
            # end if
            update_site_option("auto_core_update_failed", critical_data_)
            self.send_email("critical", core_update_, result_)
            return
        # end if
        #// 
        #// Any other WP_Error code (like download_failed or files_not_writable) occurs before
        #// we tried to copy over core files. Thus, the failures are early and graceful.
        #// 
        #// We should avoid trying to perform a background update again for the same version.
        #// But we can try again if another version is released.
        #// 
        #// For certain 'transient' failures, like download_failed, we should allow retries.
        #// In fact, let's schedule a special update for an hour from now. (It's possible
        #// the issue could actually be on WordPress.org's side.) If that one fails, then email.
        #//
        send_ = True
        transient_failures_ = Array("incompatible_archive", "download_failed", "insane_distro", "locked")
        if php_in_array(error_code_, transient_failures_) and (not get_site_option("auto_core_update_failed")):
            wp_schedule_single_event(time() + HOUR_IN_SECONDS, "wp_maybe_auto_update")
            send_ = False
        # end if
        n_ = get_site_option("auto_core_update_notified")
        #// Don't notify if we've already notified the same email address of the same version of the same notification type.
        if n_ and "fail" == n_["type"] and get_site_option("admin_email") == n_["email"] and n_["version"] == core_update_.current:
            send_ = False
        # end if
        update_site_option("auto_core_update_failed", Array({"attempted": core_update_.current, "current": wp_version_, "error_code": error_code_, "error_data": result_.get_error_data(), "timestamp": time(), "retry": php_in_array(error_code_, transient_failures_)}))
        if send_:
            self.send_email("fail", core_update_, result_)
        # end if
    # end def after_core_update
    #// 
    #// Sends an email upon the completion or failure of a background core update.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $type        The type of email to send. Can be one of 'success', 'fail', 'manual', 'critical'.
    #// @param object $core_update The update offer that was attempted.
    #// @param mixed  $result      Optional. The result for the core update. Can be WP_Error.
    #//
    def send_email(self, type_=None, core_update_=None, result_=None):
        if result_ is None:
            result_ = None
        # end if
        
        update_site_option("auto_core_update_notified", Array({"type": type_, "email": get_site_option("admin_email"), "version": core_update_.current, "timestamp": time()}))
        next_user_core_update_ = get_preferred_from_update_core()
        #// If the update transient is empty, use the update we just performed.
        if (not next_user_core_update_):
            next_user_core_update_ = core_update_
        # end if
        newer_version_available_ = "upgrade" == next_user_core_update_.response and php_version_compare(next_user_core_update_.version, core_update_.version, ">")
        #// 
        #// Filters whether to send an email following an automatic background core update.
        #// 
        #// @since 3.7.0
        #// 
        #// @param bool   $send        Whether to send the email. Default true.
        #// @param string $type        The type of email to send. Can be one of
        #// 'success', 'fail', 'critical'.
        #// @param object $core_update The update offer that was attempted.
        #// @param mixed  $result      The result for the core update. Can be WP_Error.
        #//
        if "manual" != type_ and (not apply_filters("auto_core_update_send_email", True, type_, core_update_, result_)):
            return
        # end if
        for case in Switch(type_):
            if case("success"):
                #// We updated.
                #// translators: Site updated notification email subject. 1: Site title, 2: WordPress version.
                subject_ = __("[%1$s] Your site has updated to WordPress %2$s")
                break
            # end if
            if case("fail"):
                pass
            # end if
            if case("manual"):
                #// We can't update (and made no attempt).
                #// translators: Update available notification email subject. 1: Site title, 2: WordPress version.
                subject_ = __("[%1$s] WordPress %2$s is available. Please update!")
                break
            # end if
            if case("critical"):
                #// We tried to update, started to copy files, then things went wrong.
                #// translators: Site down notification email subject. 1: Site title.
                subject_ = __("[%1$s] URGENT: Your site may be down due to a failed update")
                break
            # end if
            if case():
                return
            # end if
        # end for
        #// If the auto update is not to the latest version, say that the current version of WP is available instead.
        version_ = core_update_.current if "success" == type_ else next_user_core_update_.current
        subject_ = php_sprintf(subject_, wp_specialchars_decode(get_option("blogname"), ENT_QUOTES), version_)
        body_ = ""
        for case in Switch(type_):
            if case("success"):
                body_ += php_sprintf(__("Howdy! Your site at %1$s has been updated automatically to WordPress %2$s."), home_url(), core_update_.current)
                body_ += "\n\n"
                if (not newer_version_available_):
                    body_ += __("No further action is needed on your part.") + " "
                # end if
                #// Can only reference the About screen if their update was successful.
                about_version_ = php_explode("-", core_update_.current, 2)
                #// translators: %s: WordPress version.
                body_ += php_sprintf(__("For more on version %s, see the About WordPress screen:"), about_version_)
                body_ += "\n" + admin_url("about.php")
                if newer_version_available_:
                    #// translators: %s: WordPress latest version.
                    body_ += "\n\n" + php_sprintf(__("WordPress %s is also now available."), next_user_core_update_.current) + " "
                    body_ += __("Updating is easy and only takes a few moments:")
                    body_ += "\n" + network_admin_url("update-core.php")
                # end if
                break
            # end if
            if case("fail"):
                pass
            # end if
            if case("manual"):
                body_ += php_sprintf(__("Please update your site at %1$s to WordPress %2$s."), home_url(), next_user_core_update_.current)
                body_ += "\n\n"
                #// Don't show this message if there is a newer version available.
                #// Potential for confusion, and also not useful for them to know at this point.
                if "fail" == type_ and (not newer_version_available_):
                    body_ += __("We tried but were unable to update your site automatically.") + " "
                # end if
                body_ += __("Updating is easy and only takes a few moments:")
                body_ += "\n" + network_admin_url("update-core.php")
                break
            # end if
            if case("critical"):
                if newer_version_available_:
                    body_ += php_sprintf(__("Your site at %1$s experienced a critical failure while trying to update WordPress to version %2$s."), home_url(), core_update_.current)
                else:
                    body_ += php_sprintf(__("Your site at %1$s experienced a critical failure while trying to update to the latest version of WordPress, %2$s."), home_url(), core_update_.current)
                # end if
                body_ += "\n\n" + __("This means your site may be offline or broken. Don't panic; this can be fixed.")
                body_ += "\n\n" + __("Please check out your site now. It's possible that everything is working. If it says you need to update, you should do so:")
                body_ += "\n" + network_admin_url("update-core.php")
                break
            # end if
        # end for
        critical_support_ = "critical" == type_ and (not php_empty(lambda : core_update_.support_email))
        if critical_support_:
            #// Support offer if available.
            body_ += "\n\n" + php_sprintf(__("The WordPress team is willing to help you. Forward this email to %s and the team will work with you to make sure your site is working."), core_update_.support_email)
        else:
            #// Add a note about the support forums.
            body_ += "\n\n" + __("If you experience any issues or need support, the volunteers in the WordPress.org support forums may be able to help.")
            body_ += "\n" + __("https://wordpress.org/support/forums/")
        # end if
        #// Updates are important!
        if "success" != type_ or newer_version_available_:
            body_ += "\n\n" + __("Keeping your site updated is important for security. It also makes the internet a safer place for you and your readers.")
        # end if
        if critical_support_:
            body_ += " " + __("If you reach out to us, we'll also ensure you'll never have this problem again.")
        # end if
        #// If things are successful and we're now on the latest, mention plugins and themes if any are out of date.
        if "success" == type_ and (not newer_version_available_) and get_plugin_updates() or get_theme_updates():
            body_ += "\n\n" + __("You also have some plugins or themes with updates available. Update them now:")
            body_ += "\n" + network_admin_url()
        # end if
        body_ += "\n\n" + __("The WordPress Team") + "\n"
        if "critical" == type_ and is_wp_error(result_):
            body_ += """
            ***
            """
            #// translators: %s: WordPress version.
            body_ += php_sprintf(__("Your site was running version %s."), get_bloginfo("version"))
            body_ += " " + __("We have some data that describes the error your site encountered.")
            body_ += " " + __("Your hosting company, support forum volunteers, or a friendly developer may be able to use this information to help you:")
            #// If we had a rollback and we're still critical, then the rollback failed too.
            #// Loop through all errors (the main WP_Error, the update result, the rollback result) for code, data, etc.
            if "rollback_was_required" == result_.get_error_code():
                errors_ = Array(result_, result_.get_error_data().update, result_.get_error_data().rollback)
            else:
                errors_ = Array(result_)
            # end if
            for error_ in errors_:
                if (not is_wp_error(error_)):
                    continue
                # end if
                error_code_ = error_.get_error_code()
                #// translators: %s: Error code.
                body_ += "\n\n" + php_sprintf(__("Error code: %s"), error_code_)
                if "rollback_was_required" == error_code_:
                    continue
                # end if
                if error_.get_error_message():
                    body_ += "\n" + error_.get_error_message()
                # end if
                error_data_ = error_.get_error_data()
                if error_data_:
                    body_ += "\n" + php_implode(", ", error_data_)
                # end if
            # end for
            body_ += "\n"
        # end if
        to_ = get_site_option("admin_email")
        headers_ = ""
        email_ = php_compact("to_", "subject_", "body_", "headers_")
        #// 
        #// Filters the email sent following an automatic background core update.
        #// 
        #// @since 3.7.0
        #// 
        #// @param array $email {
        #// Array of email arguments that will be passed to wp_mail().
        #// 
        #// @type string $to      The email recipient. An array of emails
        #// can be returned, as handled by wp_mail().
        #// @type string $subject The email's subject.
        #// @type string $body    The email message body.
        #// @type string $headers Any email headers, defaults to no headers.
        #// }
        #// @param string $type        The type of email being sent. Can be one of
        #// 'success', 'fail', 'manual', 'critical'.
        #// @param object $core_update The update offer that was attempted.
        #// @param mixed  $result      The result for the core update. Can be WP_Error.
        #//
        email_ = apply_filters("auto_core_update_email", email_, type_, core_update_, result_)
        wp_mail(email_["to"], wp_specialchars_decode(email_["subject"]), email_["body"], email_["headers"])
    # end def send_email
    #// 
    #// Prepares and sends an email of a full log of background update results, useful for debugging and geekery.
    #// 
    #// @since 3.7.0
    #//
    def send_debug_email(self):
        
        
        update_count_ = 0
        for type_,updates_ in self.update_results.items():
            update_count_ += php_count(updates_)
        # end for
        body_ = Array()
        failures_ = 0
        #// translators: %s: Network home URL.
        body_[-1] = php_sprintf(__("WordPress site: %s"), network_home_url("/"))
        #// Core.
        if (php_isset(lambda : self.update_results["core"])):
            result_ = self.update_results["core"][0]
            if result_.result and (not is_wp_error(result_.result)):
                #// translators: %s: WordPress version.
                body_[-1] = php_sprintf(__("SUCCESS: WordPress was successfully updated to %s"), result_.name)
            else:
                #// translators: %s: WordPress version.
                body_[-1] = php_sprintf(__("FAILED: WordPress failed to update to %s"), result_.name)
                failures_ += 1
            # end if
            body_[-1] = ""
        # end if
        #// Plugins, Themes, Translations.
        for type_ in Array("plugin", "theme", "translation"):
            if (not (php_isset(lambda : self.update_results[type_]))):
                continue
            # end if
            success_items_ = wp_list_filter(self.update_results[type_], Array({"result": True}))
            if success_items_:
                messages_ = Array({"plugin": __("The following plugins were successfully updated:"), "theme": __("The following themes were successfully updated:"), "translation": __("The following translations were successfully updated:")})
                body_[-1] = messages_[type_]
                for name_ in wp_list_pluck(success_items_, "name"):
                    #// translators: %s: Name of plugin / theme / translation.
                    body_[-1] = " * " + php_sprintf(__("SUCCESS: %s"), name_)
                # end for
            # end if
            if success_items_ != self.update_results[type_]:
                #// Failed updates.
                messages_ = Array({"plugin": __("The following plugins failed to update:"), "theme": __("The following themes failed to update:"), "translation": __("The following translations failed to update:")})
                body_[-1] = messages_[type_]
                for item_ in self.update_results[type_]:
                    if (not item_.result) or is_wp_error(item_.result):
                        #// translators: %s: Name of plugin / theme / translation.
                        body_[-1] = " * " + php_sprintf(__("FAILED: %s"), item_.name)
                        failures_ += 1
                    # end if
                # end for
            # end if
            body_[-1] = ""
        # end for
        site_title_ = wp_specialchars_decode(get_bloginfo("name"), ENT_QUOTES)
        if failures_:
            body_[-1] = php_trim(__("""BETA TESTING?
            =============
            This debugging email is sent when you are using a development version of WordPress.
            If you think these failures might be due to a bug in WordPress, could you report it?
            * Open a thread in the support forums: https://wordpress.org/support/forum/alphabeta
            * Or, if you're comfortable writing a bug report: https://core.trac.wordpress.org/
            Thanks! -- The WordPress Team"""))
            body_[-1] = ""
            #// translators: Background update failed notification email subject. %s: Site title.
            subject_ = php_sprintf(__("[%s] Background Update Failed"), site_title_)
        else:
            #// translators: Background update finished notification email subject. %s: Site title.
            subject_ = php_sprintf(__("[%s] Background Update Finished"), site_title_)
        # end if
        body_[-1] = php_trim(__("UPDATE LOG\n=========="))
        body_[-1] = ""
        for type_ in Array("core", "plugin", "theme", "translation"):
            if (not (php_isset(lambda : self.update_results[type_]))):
                continue
            # end if
            for update_ in self.update_results[type_]:
                body_[-1] = update_.name
                body_[-1] = php_str_repeat("-", php_strlen(update_.name))
                for message_ in update_.messages:
                    body_[-1] = "  " + html_entity_decode(php_str_replace("&#8230;", "...", message_))
                # end for
                if is_wp_error(update_.result):
                    results_ = Array({"update": update_.result})
                    #// If we rolled back, we want to know an error that occurred then too.
                    if "rollback_was_required" == update_.result.get_error_code():
                        results_ = update_.result.get_error_data()
                    # end if
                    for result_type_,result_ in results_.items():
                        if (not is_wp_error(result_)):
                            continue
                        # end if
                        if "rollback" == result_type_:
                            #// translators: 1: Error code, 2: Error message.
                            body_[-1] = "  " + php_sprintf(__("Rollback Error: [%1$s] %2$s"), result_.get_error_code(), result_.get_error_message())
                        else:
                            #// translators: 1: Error code, 2: Error message.
                            body_[-1] = "  " + php_sprintf(__("Error: [%1$s] %2$s"), result_.get_error_code(), result_.get_error_message())
                        # end if
                        if result_.get_error_data():
                            body_[-1] = "         " + php_implode(", ", result_.get_error_data())
                        # end if
                    # end for
                # end if
                body_[-1] = ""
            # end for
        # end for
        email_ = Array({"to": get_site_option("admin_email"), "subject": subject_, "body": php_implode("\n", body_), "headers": ""})
        #// 
        #// Filters the debug email that can be sent following an automatic
        #// background core update.
        #// 
        #// @since 3.8.0
        #// 
        #// @param array $email {
        #// Array of email arguments that will be passed to wp_mail().
        #// 
        #// @type string $to      The email recipient. An array of emails
        #// can be returned, as handled by wp_mail().
        #// @type string $subject Email subject.
        #// @type string $body    Email message body.
        #// @type string $headers Any email headers. Default empty.
        #// }
        #// @param int   $failures The number of failures encountered while upgrading.
        #// @param mixed $results  The results of all attempted updates.
        #//
        email_ = apply_filters("automatic_updates_debug_email", email_, failures_, self.update_results)
        wp_mail(email_["to"], wp_specialchars_decode(email_["subject"]), email_["body"], email_["headers"])
    # end def send_debug_email
# end class WP_Automatic_Updater
