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
#// Class for looking up a site's health based on a user's WordPress environment.
#// 
#// @package WordPress
#// @subpackage Site_Health
#// @since 5.2.0
#//
class WP_Site_Health():
    instance = None
    mysql_min_version_check = Array()
    mysql_rec_version_check = Array()
    is_mariadb = False
    mysql_server_version = ""
    health_check_mysql_required_version = "5.5"
    health_check_mysql_rec_version = ""
    schedules = Array()
    crons = Array()
    last_missed_cron = None
    last_late_cron = None
    timeout_missed_cron = None
    timeout_late_cron = None
    #// 
    #// WP_Site_Health constructor.
    #// 
    #// @since 5.2.0
    #//
    def __init__(self):
        
        
        self.maybe_create_scheduled_event()
        self.timeout_late_cron = 0
        self.timeout_missed_cron = -5 * MINUTE_IN_SECONDS
        if php_defined("DISABLE_WP_CRON") and DISABLE_WP_CRON:
            self.timeout_late_cron = -15 * MINUTE_IN_SECONDS
            self.timeout_missed_cron = -1 * HOUR_IN_SECONDS
        # end if
        add_filter("admin_body_class", Array(self, "admin_body_class"))
        add_action("admin_enqueue_scripts", Array(self, "enqueue_scripts"))
        add_action("wp_site_health_scheduled_check", Array(self, "wp_cron_scheduled_check"))
    # end def __init__
    #// 
    #// Return an instance of the WP_Site_Health class, or create one if none exist yet.
    #// 
    #// @since 5.4.0
    #// 
    #// @return WP_Site_Health|null
    #//
    @classmethod
    def get_instance(self):
        
        
        if None == self.instance:
            self.instance = php_new_class("WP_Site_Health", lambda : WP_Site_Health())
        # end if
        return self.instance
    # end def get_instance
    #// 
    #// Enqueues the site health scripts.
    #// 
    #// @since 5.2.0
    #//
    def enqueue_scripts(self):
        
        
        screen_ = get_current_screen()
        if "site-health" != screen_.id and "dashboard" != screen_.id:
            return
        # end if
        health_check_js_variables_ = Array({"screen": screen_.id, "nonce": Array({"site_status": wp_create_nonce("health-check-site-status"), "site_status_result": wp_create_nonce("health-check-site-status-result")})}, {"site_status": Array({"direct": Array(), "async": Array(), "issues": Array({"good": 0, "recommended": 0, "critical": 0})})})
        issue_counts_ = get_transient("health-check-site-status-result")
        if False != issue_counts_:
            issue_counts_ = php_json_decode(issue_counts_)
            health_check_js_variables_["site_status"]["issues"] = issue_counts_
        # end if
        if "site-health" == screen_.id and (not (php_isset(lambda : PHP_REQUEST["tab"]))):
            tests_ = WP_Site_Health.get_tests()
            #// Don't run https test on localhost.
            if "localhost" == php_preg_replace("|https?://|", "", get_site_url()):
                tests_["direct"]["https_status"] = None
            # end if
            for test_ in tests_["direct"]:
                if php_is_string(test_["test"]):
                    test_function_ = php_sprintf("get_test_%s", test_["test"])
                    if php_method_exists(self, test_function_) and php_is_callable(Array(self, test_function_)):
                        health_check_js_variables_["site_status"]["direct"][-1] = self.perform_test(Array(self, test_function_))
                        continue
                    # end if
                # end if
                if php_is_callable(test_["test"]):
                    health_check_js_variables_["site_status"]["direct"][-1] = self.perform_test(test_["test"])
                # end if
            # end for
            for test_ in tests_["async"]:
                if php_is_string(test_["test"]):
                    health_check_js_variables_["site_status"]["async"][-1] = Array({"test": test_["test"], "completed": False})
                # end if
            # end for
        # end if
        wp_localize_script("site-health", "SiteHealth", health_check_js_variables_)
    # end def enqueue_scripts
    #// 
    #// Run a Site Health test directly.
    #// 
    #// @since 5.4.0
    #// 
    #// @param $callback
    #// 
    #// @return mixed|void
    #//
    def perform_test(self, callback_=None):
        
        
        #// 
        #// Filter the output of a finished Site Health test.
        #// 
        #// @since 5.3.0
        #// 
        #// @param array $test_result {
        #// An associated array of test result data.
        #// 
        #// @param string $label  A label describing the test, and is used as a header in the output.
        #// @param string $status The status of the test, which can be a value of `good`, `recommended` or `critical`.
        #// @param array  $badge {
        #// Tests are put into categories which have an associated badge shown, these can be modified and assigned here.
        #// 
        #// @param string $label The test label, for example `Performance`.
        #// @param string $color Default `blue`. A string representing a color to use for the label.
        #// }
        #// @param string $description A more descriptive explanation of what the test looks for, and why it is important for the end user.
        #// @param string $actions     An action to direct the user to where they can resolve the issue, if one exists.
        #// @param string $test        The name of the test being ran, used as a reference point.
        #// }
        #//
        return apply_filters("site_status_test_result", php_call_user_func(callback_))
    # end def perform_test
    #// 
    #// Run the SQL version checks.
    #// 
    #// These values are used in later tests, but the part of preparing them is more easily managed early
    #// in the class for ease of access and discovery.
    #// 
    #// @since 5.2.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #//
    def prepare_sql_data(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if wpdb_.use_mysqli:
            #// phpcs:ignore WordPress.DB.RestrictedFunctions.mysql_mysqli_get_server_info
            mysql_server_type_ = mysqli_get_server_info(wpdb_.dbh)
        else:
            #// phpcs:ignore WordPress.DB.RestrictedFunctions.mysql_mysql_get_server_info,PHPCompatibility.Extensions.RemovedExtensions.mysql_DeprecatedRemoved
            mysql_server_type_ = mysql_get_server_info(wpdb_.dbh)
        # end if
        self.mysql_server_version = wpdb_.get_var("SELECT VERSION()")
        self.health_check_mysql_rec_version = "5.6"
        if php_stristr(mysql_server_type_, "mariadb"):
            self.is_mariadb = True
            self.health_check_mysql_rec_version = "10.0"
        # end if
        self.mysql_min_version_check = php_version_compare("5.5", self.mysql_server_version, "<=")
        self.mysql_rec_version_check = php_version_compare(self.health_check_mysql_rec_version, self.mysql_server_version, "<=")
    # end def prepare_sql_data
    #// 
    #// Test if `wp_version_check` is blocked.
    #// 
    #// It's possible to block updates with the `wp_version_check` filter, but this can't be checked during an
    #// AJAX call, as the filter is never introduced then.
    #// 
    #// This filter overrides a normal page request if it's made by an admin through the AJAX call with the
    #// right query argument to check for this.
    #// 
    #// @since 5.2.0
    #//
    def check_wp_version_check_exists(self):
        
        
        if (not is_admin()) or (not is_user_logged_in()) or (not current_user_can("update_core")) or (not (php_isset(lambda : PHP_REQUEST["health-check-test-wp_version_check"]))):
            return
        # end if
        php_print("yes" if has_filter("wp_version_check", "wp_version_check") else "no")
        php_exit(0)
    # end def check_wp_version_check_exists
    #// 
    #// Tests for WordPress version and outputs it.
    #// 
    #// Gives various results depending on what kind of updates are available, if any, to encourage the
    #// user to install security updates as a priority.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test result.
    #//
    def get_test_wordpress_version(self):
        
        
        result_ = Array({"label": "", "status": "", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": "", "actions": "", "test": "wordpress_version"})
        core_current_version_ = get_bloginfo("version")
        core_updates_ = get_core_updates()
        if (not php_is_array(core_updates_)):
            result_["status"] = "recommended"
            result_["label"] = php_sprintf(__("WordPress version %s"), core_current_version_)
            result_["description"] = php_sprintf("<p>%s</p>", __("We were unable to check if any new versions of WordPress are available."))
            result_["actions"] = php_sprintf("<a href=\"%s\">%s</a>", esc_url(admin_url("update-core.php?force-check=1")), __("Check for updates manually"))
        else:
            for core_,update_ in core_updates_:
                if "upgrade" == update_.response:
                    current_version_ = php_explode(".", core_current_version_)
                    new_version_ = php_explode(".", update_.version)
                    current_major_ = current_version_[0] + "." + current_version_[1]
                    new_major_ = new_version_[0] + "." + new_version_[1]
                    result_["label"] = php_sprintf(__("WordPress update available (%s)"), update_.version)
                    result_["actions"] = php_sprintf("<a href=\"%s\">%s</a>", esc_url(admin_url("update-core.php")), __("Install the latest version of WordPress"))
                    if current_major_ != new_major_:
                        #// This is a major version mismatch.
                        result_["status"] = "recommended"
                        result_["description"] = php_sprintf("<p>%s</p>", __("A new version of WordPress is available."))
                    else:
                        #// This is a minor version, sometimes considered more critical.
                        result_["status"] = "critical"
                        result_["badge"]["label"] = __("Security")
                        result_["description"] = php_sprintf("<p>%s</p>", __("A new minor update is available for your site. Because minor updates often address security, it&#8217;s important to install them."))
                    # end if
                else:
                    result_["status"] = "good"
                    result_["label"] = php_sprintf(__("Your version of WordPress (%s) is up to date"), core_current_version_)
                    result_["description"] = php_sprintf("<p>%s</p>", __("You are currently running the latest version of WordPress available, keep it up!"))
                # end if
            # end for
        # end if
        return result_
    # end def get_test_wordpress_version
    #// 
    #// Test if plugins are outdated, or unnecessary.
    #// 
    #// The tests checks if your plugins are up to date, and encourages you to remove any that are not in use.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test result.
    #//
    def get_test_plugin_version(self):
        
        
        result_ = Array({"label": __("Your plugins are all up to date"), "status": "good", "badge": Array({"label": __("Security"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Plugins extend your site&#8217;s functionality with things like contact forms, ecommerce and much more. That means they have deep access to your site, so it&#8217;s vital to keep them up to date.")), "actions": php_sprintf("<p><a href=\"%s\">%s</a></p>", esc_url(admin_url("plugins.php")), __("Manage your plugins")), "test": "plugin_version"})
        plugins_ = get_plugins()
        plugin_updates_ = get_plugin_updates()
        plugins_have_updates_ = False
        plugins_active_ = 0
        plugins_total_ = 0
        plugins_need_update_ = 0
        #// Loop over the available plugins and check their versions and active state.
        for plugin_path_,plugin_ in plugins_:
            plugins_total_ += 1
            if is_plugin_active(plugin_path_):
                plugins_active_ += 1
            # end if
            plugin_version_ = plugin_["Version"]
            if php_array_key_exists(plugin_path_, plugin_updates_):
                plugins_need_update_ += 1
                plugins_have_updates_ = True
            # end if
        # end for
        #// Add a notice if there are outdated plugins.
        if plugins_need_update_ > 0:
            result_["status"] = "critical"
            result_["label"] = __("You have plugins waiting to be updated")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(_n("Your site has %d plugin waiting to be updated.", "Your site has %d plugins waiting to be updated.", plugins_need_update_), plugins_need_update_))
            result_["actions"] += php_sprintf("<p><a href=\"%s\">%s</a></p>", esc_url(network_admin_url("plugins.php?plugin_status=upgrade")), __("Update your plugins"))
        else:
            if 1 == plugins_active_:
                result_["description"] += php_sprintf("<p>%s</p>", __("Your site has 1 active plugin, and it is up to date."))
            else:
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(_n("Your site has %d active plugin, and it is up to date.", "Your site has %d active plugins, and they are all up to date.", plugins_active_), plugins_active_))
            # end if
        # end if
        #// Check if there are inactive plugins.
        if plugins_total_ > plugins_active_ and (not is_multisite()):
            unused_plugins_ = plugins_total_ - plugins_active_
            result_["status"] = "recommended"
            result_["label"] = __("You should remove inactive plugins")
            result_["description"] += php_sprintf("<p>%s %s</p>", php_sprintf(_n("Your site has %d inactive plugin.", "Your site has %d inactive plugins.", unused_plugins_), unused_plugins_), __("Inactive plugins are tempting targets for attackers. If you&#8217;re not going to use a plugin, we recommend you remove it."))
            result_["actions"] += php_sprintf("<p><a href=\"%s\">%s</a></p>", esc_url(admin_url("plugins.php?plugin_status=inactive")), __("Manage inactive plugins"))
        # end if
        return result_
    # end def get_test_plugin_version
    #// 
    #// Test if themes are outdated, or unnecessary.
    #// 
    #// The tests checks if your site has a default theme (to fall back on if there is a need), if your themes
    #// are up to date and, finally, encourages you to remove any themes that are not needed.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_theme_version(self):
        
        
        result_ = Array({"label": __("Your themes are all up to date"), "status": "good", "badge": Array({"label": __("Security"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Themes add your site&#8217;s look and feel. It&#8217;s important to keep them up to date, to stay consistent with your brand and keep your site secure.")), "actions": php_sprintf("<p><a href=\"%s\">%s</a></p>", esc_url(admin_url("themes.php")), __("Manage your themes")), "test": "theme_version"})
        theme_updates_ = get_theme_updates()
        themes_total_ = 0
        themes_need_updates_ = 0
        themes_inactive_ = 0
        #// This value is changed during processing to determine how many themes are considered a reasonable amount.
        allowed_theme_count_ = 1
        has_default_theme_ = False
        has_unused_themes_ = False
        show_unused_themes_ = True
        using_default_theme_ = False
        #// Populate a list of all themes available in the install.
        all_themes_ = wp_get_themes()
        active_theme_ = wp_get_theme()
        #// If WP_DEFAULT_THEME doesn't exist, fall back to the latest core default theme.
        default_theme_ = wp_get_theme(WP_DEFAULT_THEME)
        if (not default_theme_.exists()):
            default_theme_ = WP_Theme.get_core_default_theme()
        # end if
        if default_theme_:
            has_default_theme_ = True
            if active_theme_.get_stylesheet() == default_theme_.get_stylesheet() or is_child_theme() and active_theme_.get_template() == default_theme_.get_template():
                using_default_theme_ = True
            # end if
        # end if
        for theme_slug_,theme_ in all_themes_:
            themes_total_ += 1
            if php_array_key_exists(theme_slug_, theme_updates_):
                themes_need_updates_ += 1
            # end if
        # end for
        #// If this is a child theme, increase the allowed theme count by one, to account for the parent.
        if is_child_theme():
            allowed_theme_count_ += 1
        # end if
        #// If there's a default theme installed and not in use, we count that as allowed as well.
        if has_default_theme_ and (not using_default_theme_):
            allowed_theme_count_ += 1
        # end if
        if themes_total_ > allowed_theme_count_:
            has_unused_themes_ = True
            themes_inactive_ = themes_total_ - allowed_theme_count_
        # end if
        #// Check if any themes need to be updated.
        if themes_need_updates_ > 0:
            result_["status"] = "critical"
            result_["label"] = __("You have themes waiting to be updated")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(_n("Your site has %d theme waiting to be updated.", "Your site has %d themes waiting to be updated.", themes_need_updates_), themes_need_updates_))
        else:
            #// Give positive feedback about the site being good about keeping things up to date.
            if 1 == themes_total_:
                result_["description"] += php_sprintf("<p>%s</p>", __("Your site has 1 installed theme, and it is up to date."))
            else:
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(_n("Your site has %d installed theme, and it is up to date.", "Your site has %d installed themes, and they are all up to date.", themes_total_), themes_total_))
            # end if
        # end if
        if has_unused_themes_ and show_unused_themes_ and (not is_multisite()):
            #// This is a child theme, so we want to be a bit more explicit in our messages.
            if is_child_theme():
                #// Recommend removing inactive themes, except a default theme, your current one, and the parent theme.
                result_["status"] = "recommended"
                result_["label"] = __("You should remove inactive themes")
                if using_default_theme_:
                    result_["description"] += php_sprintf("<p>%s %s</p>", php_sprintf(_n("Your site has %d inactive theme.", "Your site has %d inactive themes.", themes_inactive_), themes_inactive_), php_sprintf(__("To enhance your site&#8217;s security, we recommend you remove any themes you&#8217;re not using. You should keep your current theme, %1$s, and %2$s, its parent theme."), active_theme_.name, active_theme_.parent().name))
                else:
                    result_["description"] += php_sprintf("<p>%s %s</p>", php_sprintf(_n("Your site has %d inactive theme.", "Your site has %d inactive themes.", themes_inactive_), themes_inactive_), php_sprintf(__("To enhance your site&#8217;s security, we recommend you remove any themes you&#8217;re not using. You should keep %1$s, the default WordPress theme, %2$s, your current theme, and %3$s, its parent theme."), default_theme_.name if default_theme_ else WP_DEFAULT_THEME, active_theme_.name, active_theme_.parent().name))
                # end if
            else:
                #// Recommend removing all inactive themes.
                result_["status"] = "recommended"
                result_["label"] = __("You should remove inactive themes")
                if using_default_theme_:
                    result_["description"] += php_sprintf("<p>%s %s</p>", php_sprintf(_n("Your site has %1$d inactive theme, other than %2$s, your active theme.", "Your site has %1$d inactive themes, other than %2$s, your active theme.", themes_inactive_), themes_inactive_, active_theme_.name), __("We recommend removing any unused themes to enhance your site&#8217;s security."))
                else:
                    result_["description"] += php_sprintf("<p>%s %s</p>", php_sprintf(_n("Your site has %1$d inactive theme, other than %2$s, the default WordPress theme, and %3$s, your active theme.", "Your site has %1$d inactive themes, other than %2$s, the default WordPress theme, and %3$s, your active theme.", themes_inactive_), themes_inactive_, default_theme_.name if default_theme_ else WP_DEFAULT_THEME, active_theme_.name), __("We recommend removing any unused themes to enhance your site&#8217;s security."))
                # end if
            # end if
        # end if
        #// If no default Twenty* theme exists.
        if (not has_default_theme_):
            result_["status"] = "recommended"
            result_["label"] = __("Have a default theme available")
            result_["description"] += php_sprintf("<p>%s</p>", __("Your site does not have any default theme. Default themes are used by WordPress automatically if anything is wrong with your normal theme."))
        # end if
        return result_
    # end def get_test_theme_version
    #// 
    #// Test if the supplied PHP version is supported.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_php_version(self):
        
        
        response_ = wp_check_php_version()
        result_ = Array({"label": php_sprintf(__("Your site is running the current version of PHP (%s)"), PHP_VERSION), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", php_sprintf(__("PHP is the programming language used to build and maintain WordPress. Newer versions of PHP are faster and more secure, so staying up to date will help your site&#8217;s overall performance and security. The minimum recommended version of PHP is %s."), response_["recommended_version"])), "actions": php_sprintf("<p><a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">%s <span class=\"screen-reader-text\">%s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a></p>", esc_url(wp_get_update_php_url()), __("Learn more about updating PHP"), __("(opens in a new tab)")), "test": "php_version"})
        #// PHP is up to date.
        if (not response_) or php_version_compare(PHP_VERSION, response_["recommended_version"], ">="):
            return result_
        # end if
        #// The PHP version is older than the recommended version, but still receiving active support.
        if response_["is_supported"]:
            result_["label"] = php_sprintf(__("Your site is running an older version of PHP (%s)"), PHP_VERSION)
            result_["status"] = "recommended"
            return result_
        # end if
        #// The PHP version is only receiving security fixes.
        if response_["is_secure"]:
            result_["label"] = php_sprintf(__("Your site is running an older version of PHP (%s), which should be updated"), PHP_VERSION)
            result_["status"] = "recommended"
            return result_
        # end if
        #// Anything no longer secure must be updated.
        result_["label"] = php_sprintf(__("Your site is running an outdated version of PHP (%s), which requires an update"), PHP_VERSION)
        result_["status"] = "critical"
        result_["badge"]["label"] = __("Security")
        return result_
    # end def get_test_php_version
    #// 
    #// Check if the passed extension or function are available.
    #// 
    #// Make the check for available PHP modules into a simple boolean operator for a cleaner test runner.
    #// 
    #// @since 5.2.0
    #// @since 5.3.0 The `$constant` and `$class` parameters were added.
    #// 
    #// @param string $extension Optional. The extension name to test. Default null.
    #// @param string $function  Optional. The function name to test. Default null.
    #// @param string $constant  Optional. The constant name to test for. Default null.
    #// @param string $class     Optional. The class name to test for. Default null.
    #// 
    #// @return bool Whether or not the extension and function are available.
    #//
    def test_php_extension_availability(self, extension_=None, function_=None, constant_=None, class_=None):
        
        
        #// If no extension or function is passed, claim to fail testing, as we have nothing to test against.
        if (not extension_) and (not function_) and (not constant_) and (not class_):
            return False
        # end if
        if extension_ and (not php_extension_loaded(extension_)):
            return False
        # end if
        if function_ and (not php_function_exists(function_)):
            return False
        # end if
        if constant_ and (not php_defined(constant_)):
            return False
        # end if
        if class_ and (not php_class_exists(class_)):
            return False
        # end if
        return True
    # end def test_php_extension_availability
    #// 
    #// Test if required PHP modules are installed on the host.
    #// 
    #// This test builds on the recommendations made by the WordPress Hosting Team
    #// as seen at https://make.wordpress.org/hosting/handbook/handbook/server-environment/#php-extensions
    #// 
    #// @since 5.2.0
    #// 
    #// @return array
    #//
    def get_test_php_extensions(self):
        
        
        result_ = Array({"label": __("Required and recommended modules are installed"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p><p>%s</p>", __("PHP modules perform most of the tasks on the server that make your site run. Any changes to these must be made by your server administrator."), php_sprintf(__("The WordPress Hosting Team maintains a list of those modules, both recommended and required, in <a href=\"%1$s\" %2$s>the team handbook%3$s</a>."), esc_url(__("https://make.wordpress.org/hosting/handbook/handbook/server-environment/#php-extensions")), "target=\"_blank\" rel=\"noopener noreferrer\"", php_sprintf(" <span class=\"screen-reader-text\">%s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span>", __("(opens in a new tab)")))), "actions": "", "test": "php_extensions"})
        modules_ = Array({"curl": Array({"function": "curl_version", "required": False})}, {"dom": Array({"class": "DOMNode", "required": False})}, {"exif": Array({"function": "exif_read_data", "required": False})}, {"fileinfo": Array({"function": "finfo_file", "required": False})}, {"hash": Array({"function": "hash", "required": False})}, {"json": Array({"function": "json_last_error", "required": True})}, {"mbstring": Array({"function": "mb_check_encoding", "required": False})}, {"mysqli": Array({"function": "mysqli_connect", "required": False})}, {"libsodium": Array({"constant": "SODIUM_LIBRARY_VERSION", "required": False, "php_bundled_version": "7.2.0"})}, {"openssl": Array({"function": "openssl_encrypt", "required": False})}, {"pcre": Array({"function": "preg_match", "required": False})}, {"imagick": Array({"extension": "imagick", "required": False})}, {"mod_xml": Array({"extension": "libxml", "required": False})}, {"zip": Array({"class": "ZipArchive", "required": False})}, {"filter": Array({"function": "filter_list", "required": False})}, {"gd": Array({"extension": "gd", "required": False, "fallback_for": "imagick"})}, {"iconv": Array({"function": "iconv", "required": False})}, {"mcrypt": Array({"extension": "mcrypt", "required": False, "fallback_for": "libsodium"})}, {"simplexml": Array({"extension": "simplexml", "required": False, "fallback_for": "mod_xml"})}, {"xmlreader": Array({"extension": "xmlreader", "required": False, "fallback_for": "mod_xml"})}, {"zlib": Array({"extension": "zlib", "required": False, "fallback_for": "zip"})})
        #// 
        #// An array representing all the modules we wish to test for.
        #// 
        #// @since 5.2.0
        #// @since 5.3.0 The `$constant` and `$class` parameters were added.
        #// 
        #// @param array $modules {
        #// An associated array of modules to test for.
        #// 
        #// array $module {
        #// An associated array of module properties used during testing.
        #// One of either `$function` or `$extension` must be provided, or they will fail by default.
        #// 
        #// string $function     Optional. A function name to test for the existence of.
        #// string $extension    Optional. An extension to check if is loaded in PHP.
        #// string $constant     Optional. A constant name to check for to verify an extension exists.
        #// string $class        Optional. A class name to check for to verify an extension exists.
        #// bool   $required     Is this a required feature or not.
        #// string $fallback_for Optional. The module this module replaces as a fallback.
        #// }
        #// }
        #//
        modules_ = apply_filters("site_status_test_php_modules", modules_)
        failures_ = Array()
        for library_,module_ in modules_:
            extension_ = module_["extension"] if (php_isset(lambda : module_["extension"])) else None
            function_ = module_["function"] if (php_isset(lambda : module_["function"])) else None
            constant_ = module_["constant"] if (php_isset(lambda : module_["constant"])) else None
            class_name_ = module_["class"] if (php_isset(lambda : module_["class"])) else None
            #// If this module is a fallback for another function, check if that other function passed.
            if (php_isset(lambda : module_["fallback_for"])):
                #// 
                #// If that other function has a failure, mark this module as required for normal operations.
                #// If that other function hasn't failed, skip this test as it's only a fallback.
                #//
                if (php_isset(lambda : failures_[module_["fallback_for"]])):
                    module_["required"] = True
                else:
                    continue
                # end if
            # end if
            if (not self.test_php_extension_availability(extension_, function_, constant_, class_name_)) and (not (php_isset(lambda : module_["php_bundled_version"]))) or php_version_compare(PHP_VERSION, module_["php_bundled_version"], "<"):
                if module_["required"]:
                    result_["status"] = "critical"
                    class_ = "error"
                    screen_reader_ = __("Error")
                    message_ = php_sprintf(__("The required module, %s, is not installed, or has been disabled."), library_)
                else:
                    class_ = "warning"
                    screen_reader_ = __("Warning")
                    message_ = php_sprintf(__("The optional module, %s, is not installed, or has been disabled."), library_)
                # end if
                if (not module_["required"]) and "good" == result_["status"]:
                    result_["status"] = "recommended"
                # end if
                failures_[library_] = str("<span class='dashicons ") + str(class_) + str("'><span class='screen-reader-text'>") + str(screen_reader_) + str("</span></span> ") + str(message_)
            # end if
        # end for
        if (not php_empty(lambda : failures_)):
            output_ = "<ul>"
            for failure_ in failures_:
                output_ += php_sprintf("<li>%s</li>", failure_)
            # end for
            output_ += "</ul>"
        # end if
        if "good" != result_["status"]:
            if "recommended" == result_["status"]:
                result_["label"] = __("One or more recommended modules are missing")
            # end if
            if "critical" == result_["status"]:
                result_["label"] = __("One or more required modules are missing")
            # end if
            result_["description"] += php_sprintf("<p>%s</p>", output_)
        # end if
        return result_
    # end def get_test_php_extensions
    #// 
    #// Test if the PHP default timezone is set to UTC.
    #// 
    #// @since 5.3.1
    #// 
    #// @return array The test results.
    #//
    def get_test_php_default_timezone(self):
        
        
        result_ = Array({"label": __("PHP default timezone is valid"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("PHP default timezone was configured by WordPress on loading. This is necessary for correct calculations of dates and times.")), "test": "php_default_timezone"})
        if "UTC" != php_date_default_timezone_get():
            result_["status"] = "critical"
            result_["label"] = __("PHP default timezone is invalid")
            result_["description"] = php_sprintf("<p>%s</p>", php_sprintf(__("PHP default timezone was changed after WordPress loading by a %s function call. This interferes with correct calculations of dates and times."), "<code>date_default_timezone_set()</code>"))
        # end if
        return result_
    # end def get_test_php_default_timezone
    #// 
    #// Test if the SQL server is up to date.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_sql_server(self):
        
        
        if (not self.mysql_server_version):
            self.prepare_sql_data()
        # end if
        result_ = Array({"label": __("SQL server is up to date"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("The SQL server is a required piece of software for the database WordPress uses to store all your site&#8217;s content and settings.")), "actions": php_sprintf("<p><a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">%s <span class=\"screen-reader-text\">%s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a></p>", esc_url(__("https://wordpress.org/about/requirements/")), __("Learn more about what WordPress requires to run."), __("(opens in a new tab)")), "test": "sql_server"})
        db_dropin_ = php_file_exists(WP_CONTENT_DIR + "/db.php")
        if (not self.mysql_rec_version_check):
            result_["status"] = "recommended"
            result_["label"] = __("Outdated SQL server")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("For optimal performance and security reasons, we recommend running %1$s version %2$s or higher. Contact your web hosting company to correct this."), "MariaDB" if self.is_mariadb else "MySQL", self.health_check_mysql_rec_version))
        # end if
        if (not self.mysql_min_version_check):
            result_["status"] = "critical"
            result_["label"] = __("Severely outdated SQL server")
            result_["badge"]["label"] = __("Security")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("WordPress requires %1$s version %2$s or higher. Contact your web hosting company to correct this."), "MariaDB" if self.is_mariadb else "MySQL", self.health_check_mysql_required_version))
        # end if
        if db_dropin_:
            result_["description"] += php_sprintf("<p>%s</p>", wp_kses(php_sprintf(__("You are using a %1$s drop-in which might mean that a %2$s database is not being used."), "<code>wp-content/db.php</code>", "MariaDB" if self.is_mariadb else "MySQL"), Array({"code": True})))
        # end if
        return result_
    # end def get_test_sql_server
    #// 
    #// Test if the database server is capable of using utf8mb4.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_utf8mb4_support(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if (not self.mysql_server_version):
            self.prepare_sql_data()
        # end if
        result_ = Array({"label": __("UTF8MB4 is supported"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("UTF8MB4 is the character set WordPress prefers for database storage because it safely supports the widest set of characters and encodings, including Emoji, enabling better support for non-English languages.")), "actions": "", "test": "utf8mb4_support"})
        if (not self.is_mariadb):
            if php_version_compare(self.mysql_server_version, "5.5.3", "<"):
                result_["status"] = "recommended"
                result_["label"] = __("utf8mb4 requires a MySQL update")
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("WordPress&#8217; utf8mb4 support requires MySQL version %s or greater. Please contact your server administrator."), "5.5.3"))
            else:
                result_["description"] += php_sprintf("<p>%s</p>", __("Your MySQL version supports utf8mb4."))
            # end if
        else:
            #// MariaDB introduced utf8mb4 support in 5.5.0.
            if php_version_compare(self.mysql_server_version, "5.5.0", "<"):
                result_["status"] = "recommended"
                result_["label"] = __("utf8mb4 requires a MariaDB update")
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("WordPress&#8217; utf8mb4 support requires MariaDB version %s or greater. Please contact your server administrator."), "5.5.0"))
            else:
                result_["description"] += php_sprintf("<p>%s</p>", __("Your MariaDB version supports utf8mb4."))
            # end if
        # end if
        if wpdb_.use_mysqli:
            #// phpcs:ignore WordPress.DB.RestrictedFunctions.mysql_mysqli_get_client_info
            mysql_client_version_ = mysqli_get_client_info()
        else:
            #// phpcs:ignore WordPress.DB.RestrictedFunctions.mysql_mysql_get_client_info,PHPCompatibility.Extensions.RemovedExtensions.mysql_DeprecatedRemoved
            mysql_client_version_ = mysql_get_client_info()
        # end if
        #// 
        #// libmysql has supported utf8mb4 since 5.5.3, same as the MySQL server.
        #// mysqlnd has supported utf8mb4 since 5.0.9.
        #//
        if False != php_strpos(mysql_client_version_, "mysqlnd"):
            mysql_client_version_ = php_preg_replace("/^\\D+([\\d.]+).*/", "$1", mysql_client_version_)
            if php_version_compare(mysql_client_version_, "5.0.9", "<"):
                result_["status"] = "recommended"
                result_["label"] = __("utf8mb4 requires a newer client library")
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("WordPress&#8217; utf8mb4 support requires MySQL client library (%1$s) version %2$s or newer. Please contact your server administrator."), "mysqlnd", "5.0.9"))
            # end if
        else:
            if php_version_compare(mysql_client_version_, "5.5.3", "<"):
                result_["status"] = "recommended"
                result_["label"] = __("utf8mb4 requires a newer client library")
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("WordPress&#8217; utf8mb4 support requires MySQL client library (%1$s) version %2$s or newer. Please contact your server administrator."), "libmysql", "5.5.3"))
            # end if
        # end if
        return result_
    # end def get_test_utf8mb4_support
    #// 
    #// Test if the site can communicate with WordPress.org.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_dotorg_communication(self):
        
        
        result_ = Array({"label": __("Can communicate with WordPress.org"), "status": "", "badge": Array({"label": __("Security"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Communicating with the WordPress servers is used to check for new versions, and to both install and update WordPress core, themes or plugins.")), "actions": "", "test": "dotorg_communication"})
        wp_dotorg_ = wp_remote_get("https://api.wordpress.org", Array({"timeout": 10}))
        if (not is_wp_error(wp_dotorg_)):
            result_["status"] = "good"
        else:
            result_["status"] = "critical"
            result_["label"] = __("Could not reach WordPress.org")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf("<span class=\"error\"><span class=\"screen-reader-text\">%s</span></span> %s", __("Error"), php_sprintf(__("Your site is unable to reach WordPress.org at %1$s, and returned the error: %2$s"), gethostbyname("api.wordpress.org"), wp_dotorg_.get_error_message())))
            result_["actions"] = php_sprintf("<p><a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">%s <span class=\"screen-reader-text\">%s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a></p>", esc_url(__("https://wordpress.org/support")), __("Get help resolving this issue."), __("(opens in a new tab)"))
        # end if
        return result_
    # end def get_test_dotorg_communication
    #// 
    #// Test if debug information is enabled.
    #// 
    #// When WP_DEBUG is enabled, errors and information may be disclosed to site visitors, or it may be
    #// logged to a publicly accessible file.
    #// 
    #// Debugging is also frequently left enabled after looking for errors on a site, as site owners do
    #// not understand the implications of this.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_is_in_debug_mode(self):
        
        
        result_ = Array({"label": __("Your site is not set to output debug information"), "status": "good", "badge": Array({"label": __("Security"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Debug mode is often enabled to gather more details about an error or site failure, but may contain sensitive information which should not be available on a publicly available website.")), "actions": php_sprintf("<p><a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">%s <span class=\"screen-reader-text\">%s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a></p>", esc_url(__("https://wordpress.org/support/article/debugging-in-wordpress/")), __("Learn more about debugging in WordPress."), __("(opens in a new tab)")), "test": "is_in_debug_mode"})
        if php_defined("WP_DEBUG") and WP_DEBUG:
            if php_defined("WP_DEBUG_LOG") and WP_DEBUG_LOG:
                result_["label"] = __("Your site is set to log errors to a potentially public file.")
                result_["status"] = "critical" if 0 == php_strpos(php_ini_get("error_log"), ABSPATH) else "recommended"
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("The value, %s, has been added to this website&#8217;s configuration file. This means any errors on the site will be written to a file which is potentially available to normal users."), "<code>WP_DEBUG_LOG</code>"))
            # end if
            if php_defined("WP_DEBUG_DISPLAY") and WP_DEBUG_DISPLAY:
                result_["label"] = __("Your site is set to display errors to site visitors")
                result_["status"] = "critical"
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("The value, %1$s, has either been enabled by %2$s or added to your configuration file. This will make errors display on the front end of your site."), "<code>WP_DEBUG_DISPLAY</code>", "<code>WP_DEBUG</code>"))
            # end if
        # end if
        return result_
    # end def get_test_is_in_debug_mode
    #// 
    #// Test if your site is serving content over HTTPS.
    #// 
    #// Many sites have varying degrees of HTTPS support, the most common of which is sites that have it
    #// enabled, but only if you visit the right site address.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_https_status(self):
        
        
        result_ = Array({"label": __("Your website is using an active HTTPS connection."), "status": "good", "badge": Array({"label": __("Security"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("An HTTPS connection is a more secure way of browsing the web. Many services now have HTTPS as a requirement. HTTPS allows you to take advantage of new features that can increase site speed, improve search rankings, and gain the trust of your visitors by helping to protect their online privacy.")), "actions": php_sprintf("<p><a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">%s <span class=\"screen-reader-text\">%s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a></p>", esc_url(__("https://wordpress.org/support/article/why-should-i-use-https/")), __("Learn more about why you should use HTTPS"), __("(opens in a new tab)")), "test": "https_status"})
        if is_ssl():
            wp_url_ = get_bloginfo("wpurl")
            site_url_ = get_bloginfo("url")
            if "https" != php_substr(wp_url_, 0, 5) or "https" != php_substr(site_url_, 0, 5):
                result_["status"] = "recommended"
                result_["label"] = __("Only parts of your site are using HTTPS")
                result_["description"] = php_sprintf("<p>%s</p>", php_sprintf(__("You are accessing this website using HTTPS, but your <a href=\"%s\">WordPress Address</a> is not set up to use HTTPS by default."), esc_url(admin_url("options-general.php"))))
                result_["actions"] += php_sprintf("<p><a href=\"%s\">%s</a></p>", esc_url(admin_url("options-general.php")), __("Update your site addresses"))
            # end if
        else:
            result_["status"] = "recommended"
            result_["label"] = __("Your site does not use HTTPS")
        # end if
        return result_
    # end def get_test_https_status
    #// 
    #// Check if the HTTP API can handle SSL/TLS requests.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_ssl_support(self):
        
        
        result_ = Array({"label": "", "status": "", "badge": Array({"label": __("Security"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Securely communicating between servers are needed for transactions such as fetching files, conducting sales on store sites, and much more.")), "actions": "", "test": "ssl_support"})
        supports_https_ = wp_http_supports(Array("ssl"))
        if supports_https_:
            result_["status"] = "good"
            result_["label"] = __("Your site can communicate securely with other services")
        else:
            result_["status"] = "critical"
            result_["label"] = __("Your site is unable to communicate securely with other services")
            result_["description"] += php_sprintf("<p>%s</p>", __("Talk to your web host about OpenSSL support for PHP."))
        # end if
        return result_
    # end def get_test_ssl_support
    #// 
    #// Test if scheduled events run as intended.
    #// 
    #// If scheduled events are not running, this may indicate something with WP_Cron is not working as intended,
    #// or that there are orphaned events hanging around from older code.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_scheduled_events(self):
        
        
        result_ = Array({"label": __("Scheduled events are running"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Scheduled events are what periodically looks for updates to plugins, themes and WordPress itself. It is also what makes sure scheduled posts are published on time. It may also be used by various plugins to make sure that planned actions are executed.")), "actions": "", "test": "scheduled_events"})
        self.wp_schedule_test_init()
        if is_wp_error(self.has_missed_cron()):
            result_["status"] = "critical"
            result_["label"] = __("It was not possible to check your scheduled events")
            result_["description"] = php_sprintf("<p>%s</p>", php_sprintf(__("While trying to test your site&#8217;s scheduled events, the following error was returned: %s"), self.has_missed_cron().get_error_message()))
        elif self.has_missed_cron():
            result_["status"] = "recommended"
            result_["label"] = __("A scheduled event has failed")
            result_["description"] = php_sprintf("<p>%s</p>", php_sprintf(__("The scheduled event, %s, failed to run. Your site still works, but this may indicate that scheduling posts or automated updates may not work as intended."), self.last_missed_cron))
        elif self.has_late_cron():
            result_["status"] = "recommended"
            result_["label"] = __("A scheduled event is late")
            result_["description"] = php_sprintf("<p>%s</p>", php_sprintf(__("The scheduled event, %s, is late to run. Your site still works, but this may indicate that scheduling posts or automated updates may not work as intended."), self.last_late_cron))
        # end if
        return result_
    # end def get_test_scheduled_events
    #// 
    #// Test if WordPress can run automated background updates.
    #// 
    #// Background updates in WordPress are primarily used for minor releases and security updates. It's important
    #// to either have these working, or be aware that they are intentionally disabled for whatever reason.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_background_updates(self):
        
        
        result_ = Array({"label": __("Background updates are working"), "status": "good", "badge": Array({"label": __("Security"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Background updates ensure that WordPress can auto-update if a security update is released for the version you are currently using.")), "actions": "", "test": "background_updates"})
        if (not php_class_exists("WP_Site_Health_Auto_Updates")):
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health-auto-updates.php", once=True)
        # end if
        #// Run the auto-update tests in a separate class,
        #// as there are many considerations to be made.
        automatic_updates_ = php_new_class("WP_Site_Health_Auto_Updates", lambda : WP_Site_Health_Auto_Updates())
        tests_ = automatic_updates_.run_tests()
        output_ = "<ul>"
        for test_ in tests_:
            severity_string_ = __("Passed")
            if "fail" == test_.severity:
                result_["label"] = __("Background updates are not working as expected")
                result_["status"] = "critical"
                severity_string_ = __("Error")
            # end if
            if "warning" == test_.severity and "good" == result_["status"]:
                result_["label"] = __("Background updates may not be working properly")
                result_["status"] = "recommended"
                severity_string_ = __("Warning")
            # end if
            output_ += php_sprintf("<li><span class=\"dashicons %s\"><span class=\"screen-reader-text\">%s</span></span> %s</li>", esc_attr(test_.severity), severity_string_, test_.description)
        # end for
        output_ += "</ul>"
        if "good" != result_["status"]:
            result_["description"] += php_sprintf("<p>%s</p>", output_)
        # end if
        return result_
    # end def get_test_background_updates
    #// 
    #// Test if loopbacks work as expected.
    #// 
    #// A loopback is when WordPress queries itself, for example to start a new WP_Cron instance, or when editing a
    #// plugin or theme. This has shown itself to be a recurring issue as code can very easily break this interaction.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_loopback_requests(self):
        
        
        result_ = Array({"label": __("Your site can perform loopback requests"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("Loopback requests are used to run scheduled events, and are also used by the built-in editors for themes and plugins to verify code stability.")), "actions": "", "test": "loopback_requests"})
        check_loopback_ = self.can_perform_loopback()
        result_["status"] = check_loopback_.status
        if "good" != check_loopback_.status:
            result_["label"] = __("Your site could not complete a loopback request")
            result_["description"] += php_sprintf("<p>%s</p>", check_loopback_.message)
        # end if
        return result_
    # end def get_test_loopback_requests
    #// 
    #// Test if HTTP requests are blocked.
    #// 
    #// It's possible to block all outgoing communication (with the possibility of whitelisting hosts) via the
    #// HTTP API. This may create problems for users as many features are running as services these days.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_http_requests(self):
        
        
        result_ = Array({"label": __("HTTP requests seem to be working as expected"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("It is possible for site maintainers to block all, or some, communication to other sites and services. If set up incorrectly, this may prevent plugins and themes from working as intended.")), "actions": "", "test": "http_requests"})
        blocked_ = False
        hosts_ = Array()
        if php_defined("WP_HTTP_BLOCK_EXTERNAL") and WP_HTTP_BLOCK_EXTERNAL:
            blocked_ = True
        # end if
        if php_defined("WP_ACCESSIBLE_HOSTS"):
            hosts_ = php_explode(",", WP_ACCESSIBLE_HOSTS)
        # end if
        if blocked_ and 0 == sizeof(hosts_):
            result_["status"] = "critical"
            result_["label"] = __("HTTP requests are blocked")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("HTTP requests have been blocked by the %s constant, with no allowed hosts."), "<code>WP_HTTP_BLOCK_EXTERNAL</code>"))
        # end if
        if blocked_ and 0 < sizeof(hosts_):
            result_["status"] = "recommended"
            result_["label"] = __("HTTP requests are partially blocked")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("HTTP requests have been blocked by the %1$s constant, with some hosts whitelisted: %2$s."), "<code>WP_HTTP_BLOCK_EXTERNAL</code>", php_implode(",", hosts_)))
        # end if
        return result_
    # end def get_test_http_requests
    #// 
    #// Test if the REST API is accessible.
    #// 
    #// Various security measures may block the REST API from working, or it may have been disabled in general.
    #// This is required for the new block editor to work, so we explicitly test for this.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The test results.
    #//
    def get_test_rest_availability(self):
        
        
        result_ = Array({"label": __("The REST API is available"), "status": "good", "badge": Array({"label": __("Performance"), "color": "blue"})}, {"description": php_sprintf("<p>%s</p>", __("The REST API is one way WordPress, and other applications, communicate with the server. One example is the block editor screen, which relies on this to display, and save, your posts and pages.")), "actions": "", "test": "rest_availability"})
        cookies_ = wp_unslash(PHP_COOKIE)
        timeout_ = 10
        headers_ = Array({"Cache-Control": "no-cache", "X-WP-Nonce": wp_create_nonce("wp_rest")})
        #// This filter is documented in wp-includes/class-wp-http-streams.php
        sslverify_ = apply_filters("https_local_ssl_verify", False)
        #// Include Basic auth in loopback requests.
        if (php_isset(lambda : PHP_SERVER["PHP_AUTH_USER"])) and (php_isset(lambda : PHP_SERVER["PHP_AUTH_PW"])):
            headers_["Authorization"] = "Basic " + php_base64_encode(wp_unslash(PHP_SERVER["PHP_AUTH_USER"]) + ":" + wp_unslash(PHP_SERVER["PHP_AUTH_PW"]))
        # end if
        url_ = rest_url("wp/v2/types/post")
        #// The context for this is editing with the new block editor.
        url_ = add_query_arg(Array({"context": "edit"}), url_)
        r_ = wp_remote_get(url_, php_compact("cookies", "headers", "timeout", "sslverify"))
        if is_wp_error(r_):
            result_["status"] = "critical"
            result_["label"] = __("The REST API encountered an error")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf("%s<br>%s", __("The REST API request failed due to an error."), php_sprintf(__("Error: %1$s (%2$s)"), r_.get_error_message(), r_.get_error_code())))
        elif 200 != wp_remote_retrieve_response_code(r_):
            result_["status"] = "recommended"
            result_["label"] = __("The REST API encountered an unexpected result")
            result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("The REST API call gave the following unexpected result: (%1$d) %2$s."), wp_remote_retrieve_response_code(r_), wp_remote_retrieve_body(r_)))
        else:
            json_ = php_json_decode(wp_remote_retrieve_body(r_), True)
            if False != json_ and (not (php_isset(lambda : json_["capabilities"]))):
                result_["status"] = "recommended"
                result_["label"] = __("The REST API did not behave correctly")
                result_["description"] += php_sprintf("<p>%s</p>", php_sprintf(__("The REST API did not process the %s query parameter correctly."), "<code>context</code>"))
            # end if
        # end if
        return result_
    # end def get_test_rest_availability
    #// 
    #// Return a set of tests that belong to the site status page.
    #// 
    #// Each site status test is defined here, they may be `direct` tests, that run on page load, or `async` tests
    #// which will run later down the line via JavaScript calls to improve page performance and hopefully also user
    #// experiences.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The list of tests to run.
    #//
    @classmethod
    def get_tests(self):
        
        
        tests_ = Array({"direct": Array({"wordpress_version": Array({"label": __("WordPress Version"), "test": "wordpress_version"})}, {"plugin_version": Array({"label": __("Plugin Versions"), "test": "plugin_version"})}, {"theme_version": Array({"label": __("Theme Versions"), "test": "theme_version"})}, {"php_version": Array({"label": __("PHP Version"), "test": "php_version"})}, {"php_extensions": Array({"label": __("PHP Extensions"), "test": "php_extensions"})}, {"php_default_timezone": Array({"label": __("PHP Default Timezone"), "test": "php_default_timezone"})}, {"sql_server": Array({"label": __("Database Server version"), "test": "sql_server"})}, {"utf8mb4_support": Array({"label": __("MySQL utf8mb4 support"), "test": "utf8mb4_support"})}, {"https_status": Array({"label": __("HTTPS status"), "test": "https_status"})}, {"ssl_support": Array({"label": __("Secure communication"), "test": "ssl_support"})}, {"scheduled_events": Array({"label": __("Scheduled events"), "test": "scheduled_events"})}, {"http_requests": Array({"label": __("HTTP Requests"), "test": "http_requests"})}, {"debug_enabled": Array({"label": __("Debugging enabled"), "test": "is_in_debug_mode"})})}, {"async": Array({"dotorg_communication": Array({"label": __("Communication with WordPress.org"), "test": "dotorg_communication"})}, {"background_updates": Array({"label": __("Background updates"), "test": "background_updates"})}, {"loopback_requests": Array({"label": __("Loopback request"), "test": "loopback_requests"})})})
        #// Conditionally include REST rules if the function for it exists.
        if php_function_exists("rest_url"):
            tests_["direct"]["rest_availability"] = Array({"label": __("REST API availability"), "test": "rest_availability"})
        # end if
        #// 
        #// Add or modify which site status tests are run on a site.
        #// 
        #// The site health is determined by a set of tests based on best practices from
        #// both the WordPress Hosting Team, but also web standards in general.
        #// 
        #// Some sites may not have the same requirements, for example the automatic update
        #// checks may be handled by a host, and are therefore disabled in core.
        #// Or maybe you want to introduce a new test, is caching enabled/disabled/stale for example.
        #// 
        #// Tests may be added either as direct, or asynchronous ones. Any test that may require some time
        #// to complete should run asynchronously, to avoid extended loading periods within wp-admin.
        #// 
        #// @since 5.2.0
        #// 
        #// @param array $test_type {
        #// An associative array, where the `$test_type` is either `direct` or
        #// `async`, to declare if the test should run via AJAX calls after page load.
        #// 
        #// @type array $identifier {
        #// `$identifier` should be a unique identifier for the test that should run.
        #// Plugins and themes are encouraged to prefix test identifiers with their slug
        #// to avoid any collisions between tests.
        #// 
        #// @type string $label A friendly label for your test to identify it by.
        #// @type mixed  $test  A callable to perform a direct test, or a string AJAX action to be called
        #// to perform an async test.
        #// }
        #// }
        #//
        tests_ = apply_filters("site_status_tests", tests_)
        return tests_
    # end def get_tests
    #// 
    #// Add a class to the body HTML tag.
    #// 
    #// Filters the body class string for admin pages and adds our own class for easier styling.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $body_class The body class string.
    #// @return string The modified body class string.
    #//
    def admin_body_class(self, body_class_=None):
        
        
        screen_ = get_current_screen()
        if "site-health" != screen_.id:
            return body_class_
        # end if
        body_class_ += " site-health"
        return body_class_
    # end def admin_body_class
    #// 
    #// Initiate the WP_Cron schedule test cases.
    #// 
    #// @since 5.2.0
    #//
    def wp_schedule_test_init(self):
        
        
        self.schedules = wp_get_schedules()
        self.get_cron_tasks()
    # end def wp_schedule_test_init
    #// 
    #// Populate our list of cron events and store them to a class-wide variable.
    #// 
    #// @since 5.2.0
    #//
    def get_cron_tasks(self):
        
        
        cron_tasks_ = _get_cron_array()
        if php_empty(lambda : cron_tasks_):
            self.crons = php_new_class("WP_Error", lambda : WP_Error("no_tasks", __("No scheduled events exist on this site.")))
            return
        # end if
        self.crons = Array()
        for time_,cron_ in cron_tasks_:
            for hook_,dings_ in cron_:
                for sig_,data_ in dings_:
                    self.crons[str(hook_) + str("-") + str(sig_) + str("-") + str(time_)] = Array({"hook": hook_, "time": time_, "sig": sig_, "args": data_["args"], "schedule": data_["schedule"], "interval": data_["interval"] if (php_isset(lambda : data_["interval"])) else None})
                # end for
            # end for
        # end for
    # end def get_cron_tasks
    #// 
    #// Check if any scheduled tasks have been missed.
    #// 
    #// Returns a boolean value of `true` if a scheduled task has been missed and ends processing. If the list of
    #// crons is an instance of WP_Error, return the instance instead of a boolean value.
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool|WP_Error True if a cron was missed, false if not. WP_Error if the cron is set to that.
    #//
    def has_missed_cron(self):
        
        
        if is_wp_error(self.crons):
            return self.crons
        # end if
        for id_,cron_ in self.crons:
            if cron_.time - time() < self.timeout_missed_cron:
                self.last_missed_cron = cron_.hook
                return True
            # end if
        # end for
        return False
    # end def has_missed_cron
    #// 
    #// Check if any scheduled tasks are late.
    #// 
    #// Returns a boolean value of `true` if a scheduled task is late and ends processing. If the list of
    #// crons is an instance of WP_Error, return the instance instead of a boolean value.
    #// 
    #// @since 5.3.0
    #// 
    #// @return bool|WP_Error True if a cron is late, false if not. WP_Error if the cron is set to that.
    #//
    def has_late_cron(self):
        
        
        if is_wp_error(self.crons):
            return self.crons
        # end if
        for id_,cron_ in self.crons:
            cron_offset_ = cron_.time - time()
            if cron_offset_ >= self.timeout_missed_cron and cron_offset_ < self.timeout_late_cron:
                self.last_late_cron = cron_.hook
                return True
            # end if
        # end for
        return False
    # end def has_late_cron
    #// 
    #// Run a loopback test on our site.
    #// 
    #// Loopbacks are what WordPress uses to communicate with itself to start up WP_Cron, scheduled posts,
    #// make sure plugin or theme edits don't cause site failures and similar.
    #// 
    #// @since 5.2.0
    #// 
    #// @return object The test results.
    #//
    def can_perform_loopback(self):
        
        
        cookies_ = wp_unslash(PHP_COOKIE)
        timeout_ = 10
        headers_ = Array({"Cache-Control": "no-cache"})
        #// This filter is documented in wp-includes/class-wp-http-streams.php
        sslverify_ = apply_filters("https_local_ssl_verify", False)
        #// Include Basic auth in loopback requests.
        if (php_isset(lambda : PHP_SERVER["PHP_AUTH_USER"])) and (php_isset(lambda : PHP_SERVER["PHP_AUTH_PW"])):
            headers_["Authorization"] = "Basic " + php_base64_encode(wp_unslash(PHP_SERVER["PHP_AUTH_USER"]) + ":" + wp_unslash(PHP_SERVER["PHP_AUTH_PW"]))
        # end if
        url_ = admin_url()
        r_ = wp_remote_get(url_, php_compact("cookies", "headers", "timeout", "sslverify"))
        if is_wp_error(r_):
            return Array({"status": "critical", "message": php_sprintf("%s<br>%s", __("The loopback request to your site failed, this means features relying on them are not currently working as expected."), php_sprintf(__("Error: %1$s (%2$s)"), r_.get_error_message(), r_.get_error_code()))})
        # end if
        if 200 != wp_remote_retrieve_response_code(r_):
            return Array({"status": "recommended", "message": php_sprintf(__("The loopback request returned an unexpected http status code, %d, it was not possible to determine if this will prevent features from working as expected."), wp_remote_retrieve_response_code(r_))})
        # end if
        return Array({"status": "good", "message": __("The loopback request to your site completed successfully.")})
    # end def can_perform_loopback
    #// 
    #// Create a weekly cron event, if one does not already exist.
    #// 
    #// @since 5.4.0
    #//
    def maybe_create_scheduled_event(self):
        
        
        if (not wp_next_scheduled("wp_site_health_scheduled_check")) and (not wp_installing()):
            wp_schedule_event(time() + DAY_IN_SECONDS, "weekly", "wp_site_health_scheduled_check")
        # end if
    # end def maybe_create_scheduled_event
    #// 
    #// Run our scheduled event to check and update the latest site health status for the website.
    #// 
    #// @since 5.4.0
    #//
    def wp_cron_scheduled_check(self):
        
        
        #// Bootstrap wp-admin, as WP_Cron doesn't do this for us.
        php_include_file(trailingslashit(ABSPATH) + "wp-admin/includes/admin.php", once=True)
        tests_ = WP_Site_Health.get_tests()
        results_ = Array()
        site_status_ = Array({"good": 0, "recommended": 0, "critical": 0})
        #// Don't run https test on localhost.
        if "localhost" == php_preg_replace("|https?://|", "", get_site_url()):
            tests_["direct"]["https_status"] = None
        # end if
        for test_ in tests_["direct"]:
            if php_is_string(test_["test"]):
                test_function_ = php_sprintf("get_test_%s", test_["test"])
                if php_method_exists(self, test_function_) and php_is_callable(Array(self, test_function_)):
                    results_[-1] = self.perform_test(Array(self, test_function_))
                    continue
                # end if
            # end if
            if php_is_callable(test_["test"]):
                results_[-1] = self.perform_test(test_["test"])
            # end if
        # end for
        for test_ in tests_["async"]:
            if php_is_string(test_["test"]):
                if (php_isset(lambda : test_["has_rest"])) and test_["has_rest"]:
                    result_fetch_ = wp_remote_post(rest_url(test_["test"]), Array({"body": Array({"_wpnonce": wp_create_nonce("wp_rest")})}))
                else:
                    result_fetch_ = wp_remote_post(admin_url("admin-ajax.php"), Array({"body": Array({"action": test_["test"], "_wpnonce": wp_create_nonce("health-check-site-status")})}))
                # end if
                if (not is_wp_error(result_fetch_)):
                    results_[-1] = php_json_decode(wp_remote_retrieve_body(result_fetch_))
                else:
                    results_[-1] = Array({"status": "recommended", "label": __("A test is unavailable")})
                # end if
            # end if
        # end for
        for result_ in results_:
            if "critical" == result_["status"]:
                site_status_["critical"] += 1
            elif "recommended" == result_["status"]:
                site_status_["recommended"] += 1
            else:
                site_status_["good"] += 1
            # end if
        # end for
        set_transient("health-check-site-status-result", wp_json_encode(site_status_))
    # end def wp_cron_scheduled_check
# end class WP_Site_Health
