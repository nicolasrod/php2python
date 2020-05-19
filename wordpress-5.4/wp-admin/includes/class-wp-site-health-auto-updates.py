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
#// Class for testing automatic updates in the WordPress code.
#// 
#// @package WordPress
#// @subpackage Site_Health
#// @since 5.2.0
#//
class WP_Site_Health_Auto_Updates():
    #// 
    #// WP_Site_Health_Auto_Updates constructor.
    #// @since 5.2.0
    #//
    def __init__(self):
        
        
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    # end def __init__
    #// 
    #// Run tests to determine if auto-updates can run.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def run_tests(self):
        
        
        tests_ = Array(self.test_constants("WP_AUTO_UPDATE_CORE", True), self.test_wp_version_check_attached(), self.test_filters_automatic_updater_disabled(), self.test_wp_automatic_updates_disabled(), self.test_if_failed_update(), self.test_vcs_abspath(), self.test_check_wp_filesystem_method(), self.test_all_files_writable(), self.test_accepts_dev_updates(), self.test_accepts_minor_updates())
        tests_ = php_array_filter(tests_)
        def _closure_ae5a306c(test_=None):
            
            
            test_ = test_
            if php_empty(lambda : test_.severity):
                test_.severity = "warning"
            # end if
            return test_
        # end def _closure_ae5a306c
        tests_ = php_array_map((lambda *args, **kwargs: _closure_ae5a306c(*args, **kwargs)), tests_)
        return tests_
    # end def run_tests
    #// 
    #// Test if auto-updates related constants are set correctly.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $constant The name of the constant to check.
    #// @param bool   $value    The value that the constant should be, if set.
    #// @return array The test results.
    #//
    def test_constants(self, constant_=None, value_=None):
        
        
        if php_defined(constant_) and constant(constant_) != value_:
            return Array({"description": php_sprintf(__("The %s constant is defined and enabled."), str("<code>") + str(constant_) + str("</code>")), "severity": "fail"})
        # end if
    # end def test_constants
    #// 
    #// Check if updates are intercepted by a filter.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def test_wp_version_check_attached(self):
        
        
        if (not is_main_site()):
            return
        # end if
        cookies_ = wp_unslash(PHP_COOKIE)
        timeout_ = 10
        headers_ = Array({"Cache-Control": "no-cache"})
        #// This filter is documented in wp-includes/class-wp-http-streams.php
        sslverify_ = apply_filters("https_local_ssl_verify", False)
        #// Include Basic auth in loopback requests.
        if (php_isset(lambda : PHP_SERVER["PHP_AUTH_USER"])) and (php_isset(lambda : PHP_SERVER["PHP_AUTH_PW"])):
            headers_["Authorization"] = "Basic " + php_base64_encode(wp_unslash(PHP_SERVER["PHP_AUTH_USER"]) + ":" + wp_unslash(PHP_SERVER["PHP_AUTH_PW"]))
        # end if
        url_ = add_query_arg(Array({"health-check-test-wp_version_check": True}), admin_url("site-health.php"))
        test_ = wp_remote_get(url_, php_compact("cookies_", "headers_", "timeout_", "sslverify_"))
        if is_wp_error(test_):
            return Array({"description": php_sprintf(__("Could not confirm that the %s filter is available."), "<code>wp_version_check()</code>"), "severity": "warning"})
        # end if
        response_ = wp_remote_retrieve_body(test_)
        if "yes" != response_:
            return Array({"description": php_sprintf(__("A plugin has prevented updates by disabling %s."), "<code>wp_version_check()</code>"), "severity": "fail"})
        # end if
    # end def test_wp_version_check_attached
    #// 
    #// Check if automatic updates are disabled by a filter.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def test_filters_automatic_updater_disabled(self):
        
        
        #// This filter is documented in wp-admin/includes/class-wp-automatic-updater.php
        if apply_filters("automatic_updater_disabled", False):
            return Array({"description": php_sprintf(__("The %s filter is enabled."), "<code>automatic_updater_disabled</code>"), "severity": "fail"})
        # end if
    # end def test_filters_automatic_updater_disabled
    #// 
    #// Check if automatic updates are disabled.
    #// 
    #// @since 5.3.0
    #// 
    #// @return array|bool The test results. False if auto updates are enabled.
    #//
    def test_wp_automatic_updates_disabled(self):
        
        
        if (not php_class_exists("WP_Automatic_Updater")):
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-automatic-updates.php", once=True)
        # end if
        auto_updates_ = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
        if (not auto_updates_.is_disabled()):
            return False
        # end if
        return Array({"description": __("All automatic updates are disabled."), "severity": "fail"})
    # end def test_wp_automatic_updates_disabled
    #// 
    #// Check if automatic updates have tried to run, but failed, previously.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array|bool The test results. False if the auto updates failed.
    #//
    def test_if_failed_update(self):
        
        
        failed_ = get_site_option("auto_core_update_failed")
        if (not failed_):
            return False
        # end if
        if (not php_empty(lambda : failed_["critical"])):
            description_ = __("A previous automatic background update ended with a critical failure, so updates are now disabled.")
            description_ += " " + __("You would have received an email because of this.")
            description_ += " " + __("When you've been able to update using the \"Update Now\" button on Dashboard > Updates, we'll clear this error for future update attempts.")
            description_ += " " + php_sprintf(__("The error code was %s."), "<code>" + failed_["error_code"] + "</code>")
            return Array({"description": description_, "severity": "warning"})
        # end if
        description_ = __("A previous automatic background update could not occur.")
        if php_empty(lambda : failed_["retry"]):
            description_ += " " + __("You would have received an email because of this.")
        # end if
        description_ += " " + __("We'll try again with the next release.")
        description_ += " " + php_sprintf(__("The error code was %s."), "<code>" + failed_["error_code"] + "</code>")
        return Array({"description": description_, "severity": "warning"})
    # end def test_if_failed_update
    #// 
    #// Check if WordPress is controlled by a VCS (Git, Subversion etc).
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def test_vcs_abspath(self):
        
        
        context_dirs_ = Array(ABSPATH)
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
                #// phpcs:ignore
                checkout_ = php_no_error(lambda: php_is_dir(php_rtrim(check_dir_, "\\/") + str("/") + str(vcs_dir_)))
                if checkout_:
                    break
                # end if
            # end for
        # end for
        #// This filter is documented in wp-admin/includes/class-wp-automatic-updater.php
        if checkout_ and (not apply_filters("automatic_updates_is_vcs_checkout", True, ABSPATH)):
            return Array({"description": php_sprintf(__("The folder %1$s was detected as being under version control (%2$s), but the %3$s filter is allowing updates."), "<code>" + check_dir_ + "</code>", str("<code>") + str(vcs_dir_) + str("</code>"), "<code>automatic_updates_is_vcs_checkout</code>"), "severity": "info"})
        # end if
        if checkout_:
            return Array({"description": php_sprintf(__("The folder %1$s was detected as being under version control (%2$s)."), "<code>" + check_dir_ + "</code>", str("<code>") + str(vcs_dir_) + str("</code>")), "severity": "warning"})
        # end if
        return Array({"description": __("No version control systems were detected."), "severity": "pass"})
    # end def test_vcs_abspath
    #// 
    #// Check if we can access files without providing credentials.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def test_check_wp_filesystem_method(self):
        
        
        skin_ = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
        success_ = skin_.request_filesystem_credentials(False, ABSPATH)
        if (not success_):
            description_ = __("Your installation of WordPress prompts for FTP credentials to perform updates.")
            description_ += " " + __("(Your site is performing updates over FTP due to file ownership. Talk to your hosting company.)")
            return Array({"description": description_, "severity": "fail"})
        # end if
        return Array({"description": __("Your installation of WordPress doesn't require FTP credentials to perform updates."), "severity": "pass"})
    # end def test_check_wp_filesystem_method
    #// 
    #// Check if core files are writable by the web user/group.
    #// 
    #// @since 5.2.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
    #// 
    #// @return array|bool The test results. False if they're not writeable.
    #//
    def test_all_files_writable(self):
        
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        php_include_file(ABSPATH + WPINC + "/version.php", once=False)
        #// $wp_version; // x.y.z
        skin_ = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
        success_ = skin_.request_filesystem_credentials(False, ABSPATH)
        if (not success_):
            return False
        # end if
        WP_Filesystem()
        if "direct" != wp_filesystem_.method:
            return False
        # end if
        checksums_ = get_core_checksums(wp_version_, "en_US")
        dev_ = False != php_strpos(wp_version_, "-")
        #// Get the last stable version's files and test against that.
        if (not checksums_) and dev_:
            checksums_ = get_core_checksums(php_float(wp_version_) - 0.1, "en_US")
        # end if
        #// There aren't always checksums for development releases, so just skip the test if we still can't find any.
        if (not checksums_) and dev_:
            return False
        # end if
        if (not checksums_):
            description_ = php_sprintf(__("Couldn't retrieve a list of the checksums for WordPress %s."), wp_version_)
            description_ += " " + __("This could mean that connections are failing to WordPress.org.")
            return Array({"description": description_, "severity": "warning"})
        # end if
        unwritable_files_ = Array()
        for file_ in php_array_keys(checksums_):
            if "wp-content" == php_substr(file_, 0, 10):
                continue
            # end if
            if (not php_file_exists(ABSPATH + file_)):
                continue
            # end if
            if (not php_is_writable(ABSPATH + file_)):
                unwritable_files_[-1] = file_
            # end if
        # end for
        if unwritable_files_:
            if php_count(unwritable_files_) > 20:
                unwritable_files_ = php_array_slice(unwritable_files_, 0, 20)
                unwritable_files_[-1] = "..."
            # end if
            return Array({"description": __("Some files are not writable by WordPress:") + " <ul><li>" + php_implode("</li><li>", unwritable_files_) + "</li></ul>", "severity": "fail"})
        else:
            return Array({"description": __("All of your WordPress files are writable."), "severity": "pass"})
        # end if
    # end def test_all_files_writable
    #// 
    #// Check if the install is using a development branch and can use nightly packages.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array|bool The test results. False if it isn't a development version.
    #//
    def test_accepts_dev_updates(self):
        
        
        php_include_file(ABSPATH + WPINC + "/version.php", once=False)
        #// $wp_version; // x.y.z
        #// Only for dev versions.
        if False == php_strpos(wp_version_, "-"):
            return False
        # end if
        if php_defined("WP_AUTO_UPDATE_CORE") and "minor" == WP_AUTO_UPDATE_CORE or False == WP_AUTO_UPDATE_CORE:
            return Array({"description": php_sprintf(__("WordPress development updates are blocked by the %s constant."), "<code>WP_AUTO_UPDATE_CORE</code>"), "severity": "fail"})
        # end if
        #// This filter is documented in wp-admin/includes/class-core-upgrader.php
        if (not apply_filters("allow_dev_auto_core_updates", wp_version_)):
            return Array({"description": php_sprintf(__("WordPress development updates are blocked by the %s filter."), "<code>allow_dev_auto_core_updates</code>"), "severity": "fail"})
        # end if
    # end def test_accepts_dev_updates
    #// 
    #// Check if the site supports automatic minor updates.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def test_accepts_minor_updates(self):
        
        
        if php_defined("WP_AUTO_UPDATE_CORE") and False == WP_AUTO_UPDATE_CORE:
            return Array({"description": php_sprintf(__("WordPress security and maintenance releases are blocked by %s."), "<code>define( 'WP_AUTO_UPDATE_CORE', false );</code>"), "severity": "fail"})
        # end if
        #// This filter is documented in wp-admin/includes/class-core-upgrader.php
        if (not apply_filters("allow_minor_auto_core_updates", True)):
            return Array({"description": php_sprintf(__("WordPress security and maintenance releases are blocked by the %s filter."), "<code>allow_minor_auto_core_updates</code>"), "severity": "fail"})
        # end if
    # end def test_accepts_minor_updates
# end class WP_Site_Health_Auto_Updates
