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
#// A simple set of functions to check our version 1.0 update service.
#// 
#// @package WordPress
#// @since 2.3.0
#// 
#// 
#// Check WordPress version against the newest version.
#// 
#// The WordPress version, PHP version, and Locale is sent. Checks against the
#// WordPress server at api.wordpress.org server. Will only check if WordPress
#// isn't installing.
#// 
#// @since 2.3.0
#// @global string $wp_version       Used to check against the newest WordPress version.
#// @global wpdb   $wpdb             WordPress database abstraction object.
#// @global string $wp_local_package Locale code of the package.
#// 
#// @param array $extra_stats Extra statistics to report to the WordPress.org API.
#// @param bool  $force_check Whether to bypass the transient cache and force a fresh update check. Defaults to false, true if $extra_stats is set.
#//
def wp_version_check(extra_stats_=None, force_check_=None, *_args_):
    if extra_stats_ is None:
        extra_stats_ = Array()
    # end if
    if force_check_ is None:
        force_check_ = False
    # end if
    
    if wp_installing():
        return
    # end if
    global wpdb_
    global wp_local_package_
    php_check_if_defined("wpdb_","wp_local_package_")
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    php_version_ = php_phpversion()
    current_ = get_site_transient("update_core")
    translations_ = wp_get_installed_translations("core")
    #// Invalidate the transient when $wp_version changes.
    if php_is_object(current_) and wp_version_ != current_.version_checked:
        current_ = False
    # end if
    if (not php_is_object(current_)):
        current_ = php_new_class("stdClass", lambda : stdClass())
        current_.updates = Array()
        current_.version_checked = wp_version_
    # end if
    if (not php_empty(lambda : extra_stats_)):
        force_check_ = True
    # end if
    #// Wait 1 minute between multiple version check requests.
    timeout_ = MINUTE_IN_SECONDS
    time_not_changed_ = (php_isset(lambda : current_.last_checked)) and timeout_ > time() - current_.last_checked
    if (not force_check_) and time_not_changed_:
        return
    # end if
    #// 
    #// Filters the locale requested for WordPress core translations.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $locale Current locale.
    #//
    locale_ = apply_filters("core_version_check_locale", get_locale())
    #// Update last_checked for current to prevent multiple blocking requests if request hangs.
    current_.last_checked = time()
    set_site_transient("update_core", current_)
    if php_method_exists(wpdb_, "db_version"):
        mysql_version_ = php_preg_replace("/[^0-9.].*/", "", wpdb_.db_version())
    else:
        mysql_version_ = "N/A"
    # end if
    if is_multisite():
        user_count_ = get_user_count()
        num_blogs_ = get_blog_count()
        wp_install_ = network_site_url()
        multisite_enabled_ = 1
    else:
        user_count_ = count_users()
        user_count_ = user_count_["total_users"]
        multisite_enabled_ = 0
        num_blogs_ = 1
        wp_install_ = home_url("/")
    # end if
    query_ = Array({"version": wp_version_, "php": php_version_, "locale": locale_, "mysql": mysql_version_, "local_package": wp_local_package_ if (php_isset(lambda : wp_local_package_)) else "", "blogs": num_blogs_, "users": user_count_, "multisite_enabled": multisite_enabled_, "initial_db_version": get_site_option("initial_db_version")})
    #// 
    #// Filter the query arguments sent as part of the core version check.
    #// 
    #// WARNING: Changing this data may result in your site not receiving security updates.
    #// Please exercise extreme caution.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $query {
    #// Version check query arguments.
    #// 
    #// @type string $version            WordPress version number.
    #// @type string $php                PHP version number.
    #// @type string $locale             The locale to retrieve updates for.
    #// @type string $mysql              MySQL version number.
    #// @type string $local_package      The value of the $wp_local_package global, when set.
    #// @type int    $blogs              Number of sites on this WordPress installation.
    #// @type int    $users              Number of users on this WordPress installation.
    #// @type int    $multisite_enabled  Whether this WordPress installation uses Multisite.
    #// @type int    $initial_db_version Database version of WordPress at time of installation.
    #// }
    #//
    query_ = apply_filters("core_version_check_query_args", query_)
    post_body_ = Array({"translations": wp_json_encode(translations_)})
    if php_is_array(extra_stats_):
        post_body_ = php_array_merge(post_body_, extra_stats_)
    # end if
    url_ = "http://api.wordpress.org/core/version-check/1.7/?" + http_build_query(query_, None, "&")
    http_url_ = url_
    ssl_ = wp_http_supports(Array("ssl"))
    if ssl_:
        url_ = set_url_scheme(url_, "https")
    # end if
    doing_cron_ = wp_doing_cron()
    options_ = Array({"timeout": 30 if doing_cron_ else 3, "user-agent": "WordPress/" + wp_version_ + "; " + home_url("/"), "headers": Array({"wp_install": wp_install_, "wp_blog": home_url("/")})}, {"body": post_body_})
    response_ = wp_remote_post(url_, options_)
    if ssl_ and is_wp_error(response_):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        response_ = wp_remote_post(http_url_, options_)
    # end if
    if is_wp_error(response_) or 200 != wp_remote_retrieve_response_code(response_):
        return
    # end if
    body_ = php_trim(wp_remote_retrieve_body(response_))
    body_ = php_json_decode(body_, True)
    if (not php_is_array(body_)) or (not (php_isset(lambda : body_["offers"]))):
        return
    # end if
    offers_ = body_["offers"]
    for offer_ in offers_:
        for offer_key_,value_ in offer_.items():
            if "packages" == offer_key_:
                offer_["packages"] = php_array_intersect_key(php_array_map("esc_url", offer_["packages"]), php_array_fill_keys(Array("full", "no_content", "new_bundled", "partial", "rollback"), ""))
            elif "download" == offer_key_:
                offer_["download"] = esc_url(value_)
            else:
                offer_[offer_key_] = esc_html(value_)
            # end if
        # end for
        offer_ = php_array_intersect_key(offer_, php_array_fill_keys(Array("response", "download", "locale", "packages", "current", "version", "php_version", "mysql_version", "new_bundled", "partial_version", "notify_email", "support_email", "new_files"), ""))
    # end for
    updates_ = php_new_class("stdClass", lambda : stdClass())
    updates_.updates = offers_
    updates_.last_checked = time()
    updates_.version_checked = wp_version_
    if (php_isset(lambda : body_["translations"])):
        updates_.translations = body_["translations"]
    # end if
    set_site_transient("update_core", updates_)
    if (not php_empty(lambda : body_["ttl"])):
        ttl_ = php_int(body_["ttl"])
        if ttl_ and time() + ttl_ < wp_next_scheduled("wp_version_check"):
            #// Queue an event to re-run the update check in $ttl seconds.
            wp_schedule_single_event(time() + ttl_, "wp_version_check")
        # end if
    # end if
    #// Trigger background updates if running non-interactively, and we weren't called from the update handler.
    if doing_cron_ and (not doing_action("wp_maybe_auto_update")):
        #// 
        #// Fires during wp_cron, starting the auto update process.
        #// 
        #// @since 3.9.0
        #//
        do_action("wp_maybe_auto_update")
    # end if
# end def wp_version_check
#// 
#// Check plugin versions against the latest versions hosted on WordPress.org.
#// 
#// The WordPress version, PHP version, and Locale is sent along with a list of
#// all plugins installed. Checks against the WordPress server at
#// api.wordpress.org. Will only check if WordPress isn't installing.
#// 
#// @since 2.3.0
#// @global string $wp_version The WordPress version string.
#// 
#// @param array $extra_stats Extra statistics to report to the WordPress.org API.
#//
def wp_update_plugins(extra_stats_=None, *_args_):
    if extra_stats_ is None:
        extra_stats_ = Array()
    # end if
    
    if wp_installing():
        return
    # end if
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    #// If running blog-side, bail unless we've not checked in the last 12 hours.
    if (not php_function_exists("get_plugins")):
        php_include_file(ABSPATH + "wp-admin/includes/plugin.php", once=True)
    # end if
    plugins_ = get_plugins()
    translations_ = wp_get_installed_translations("plugins")
    active_ = get_option("active_plugins", Array())
    current_ = get_site_transient("update_plugins")
    if (not php_is_object(current_)):
        current_ = php_new_class("stdClass", lambda : stdClass())
    # end if
    new_option_ = php_new_class("stdClass", lambda : stdClass())
    new_option_.last_checked = time()
    doing_cron_ = wp_doing_cron()
    #// Check for update on a different schedule, depending on the page.
    for case in Switch(current_filter()):
        if case("upgrader_process_complete"):
            timeout_ = 0
            break
        # end if
        if case("load-update-core.php"):
            timeout_ = MINUTE_IN_SECONDS
            break
        # end if
        if case("load-plugins.php"):
            pass
        # end if
        if case("load-update.php"):
            timeout_ = HOUR_IN_SECONDS
            break
        # end if
        if case():
            if doing_cron_:
                timeout_ = 2 * HOUR_IN_SECONDS
            else:
                timeout_ = 12 * HOUR_IN_SECONDS
            # end if
        # end if
    # end for
    time_not_changed_ = (php_isset(lambda : current_.last_checked)) and timeout_ > time() - current_.last_checked
    if time_not_changed_ and (not extra_stats_):
        plugin_changed_ = False
        for file_,p_ in plugins_.items():
            new_option_.checked[file_] = p_["Version"]
            if (not (php_isset(lambda : current_.checked[file_]))) or php_strval(current_.checked[file_]) != php_strval(p_["Version"]):
                plugin_changed_ = True
            # end if
        # end for
        if (php_isset(lambda : current_.response)) and php_is_array(current_.response):
            for plugin_file_,update_details_ in current_.response.items():
                if (not (php_isset(lambda : plugins_[plugin_file_]))):
                    plugin_changed_ = True
                    break
                # end if
            # end for
        # end if
        #// Bail if we've checked recently and if nothing has changed.
        if (not plugin_changed_):
            return
        # end if
    # end if
    #// Update last_checked for current to prevent multiple blocking requests if request hangs.
    current_.last_checked = time()
    set_site_transient("update_plugins", current_)
    to_send_ = php_compact("plugins_", "active_")
    locales_ = php_array_values(get_available_languages())
    #// 
    #// Filters the locales requested for plugin translations.
    #// 
    #// @since 3.7.0
    #// @since 4.5.0 The default value of the `$locales` parameter changed to include all locales.
    #// 
    #// @param array $locales Plugin locales. Default is all available locales of the site.
    #//
    locales_ = apply_filters("plugins_update_check_locales", locales_)
    locales_ = array_unique(locales_)
    if doing_cron_:
        timeout_ = 30
    else:
        #// Three seconds, plus one extra second for every 10 plugins.
        timeout_ = 3 + php_int(php_count(plugins_) / 10)
    # end if
    options_ = Array({"timeout": timeout_, "body": Array({"plugins": wp_json_encode(to_send_), "translations": wp_json_encode(translations_), "locale": wp_json_encode(locales_), "all": wp_json_encode(True)})}, {"user-agent": "WordPress/" + wp_version_ + "; " + home_url("/")})
    if extra_stats_:
        options_["body"]["update_stats"] = wp_json_encode(extra_stats_)
    # end if
    url_ = "http://api.wordpress.org/plugins/update-check/1.1/"
    http_url_ = url_
    ssl_ = wp_http_supports(Array("ssl"))
    if ssl_:
        url_ = set_url_scheme(url_, "https")
    # end if
    raw_response_ = wp_remote_post(url_, options_)
    if ssl_ and is_wp_error(raw_response_):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        raw_response_ = wp_remote_post(http_url_, options_)
    # end if
    if is_wp_error(raw_response_) or 200 != wp_remote_retrieve_response_code(raw_response_):
        return
    # end if
    response_ = php_json_decode(wp_remote_retrieve_body(raw_response_), True)
    for plugin_ in response_["plugins"]:
        plugin_ = plugin_
        if (php_isset(lambda : plugin_.compatibility)):
            plugin_.compatibility = plugin_.compatibility
            for data_ in plugin_.compatibility:
                data_ = data_
            # end for
        # end if
    # end for
    plugin_ = None
    data_ = None
    for plugin_ in response_["no_update"]:
        plugin_ = plugin_
    # end for
    plugin_ = None
    if php_is_array(response_):
        new_option_.response = response_["plugins"]
        new_option_.translations = response_["translations"]
        #// TODO: Perhaps better to store no_update in a separate transient with an expiry?
        new_option_.no_update = response_["no_update"]
    else:
        new_option_.response = Array()
        new_option_.translations = Array()
        new_option_.no_update = Array()
    # end if
    set_site_transient("update_plugins", new_option_)
# end def wp_update_plugins
#// 
#// Check theme versions against the latest versions hosted on WordPress.org.
#// 
#// A list of all themes installed in sent to WP. Checks against the
#// WordPress server at api.wordpress.org. Will only check if WordPress isn't
#// installing.
#// 
#// @since 2.7.0
#// @global string $wp_version The WordPress version string.
#// 
#// @param array $extra_stats Extra statistics to report to the WordPress.org API.
#//
def wp_update_themes(extra_stats_=None, *_args_):
    if extra_stats_ is None:
        extra_stats_ = Array()
    # end if
    
    if wp_installing():
        return
    # end if
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    installed_themes_ = wp_get_themes()
    translations_ = wp_get_installed_translations("themes")
    last_update_ = get_site_transient("update_themes")
    if (not php_is_object(last_update_)):
        last_update_ = php_new_class("stdClass", lambda : stdClass())
    # end if
    themes_ = Array()
    checked_ = Array()
    request_ = Array()
    #// Put slug of current theme into request.
    request_["active"] = get_option("stylesheet")
    for theme_ in installed_themes_:
        checked_[theme_.get_stylesheet()] = theme_.get("Version")
        themes_[theme_.get_stylesheet()] = Array({"Name": theme_.get("Name"), "Title": theme_.get("Name"), "Version": theme_.get("Version"), "Author": theme_.get("Author"), "Author URI": theme_.get("AuthorURI"), "Template": theme_.get_template(), "Stylesheet": theme_.get_stylesheet()})
    # end for
    doing_cron_ = wp_doing_cron()
    #// Check for update on a different schedule, depending on the page.
    for case in Switch(current_filter()):
        if case("upgrader_process_complete"):
            timeout_ = 0
            break
        # end if
        if case("load-update-core.php"):
            timeout_ = MINUTE_IN_SECONDS
            break
        # end if
        if case("load-themes.php"):
            pass
        # end if
        if case("load-update.php"):
            timeout_ = HOUR_IN_SECONDS
            break
        # end if
        if case():
            if doing_cron_:
                timeout_ = 2 * HOUR_IN_SECONDS
            else:
                timeout_ = 12 * HOUR_IN_SECONDS
            # end if
        # end if
    # end for
    time_not_changed_ = (php_isset(lambda : last_update_.last_checked)) and timeout_ > time() - last_update_.last_checked
    if time_not_changed_ and (not extra_stats_):
        theme_changed_ = False
        for slug_,v_ in checked_.items():
            if (not (php_isset(lambda : last_update_.checked[slug_]))) or php_strval(last_update_.checked[slug_]) != php_strval(v_):
                theme_changed_ = True
            # end if
        # end for
        if (php_isset(lambda : last_update_.response)) and php_is_array(last_update_.response):
            for slug_,update_details_ in last_update_.response.items():
                if (not (php_isset(lambda : checked_[slug_]))):
                    theme_changed_ = True
                    break
                # end if
            # end for
        # end if
        #// Bail if we've checked recently and if nothing has changed.
        if (not theme_changed_):
            return
        # end if
    # end if
    #// Update last_checked for current to prevent multiple blocking requests if request hangs.
    last_update_.last_checked = time()
    set_site_transient("update_themes", last_update_)
    request_["themes"] = themes_
    locales_ = php_array_values(get_available_languages())
    #// 
    #// Filters the locales requested for theme translations.
    #// 
    #// @since 3.7.0
    #// @since 4.5.0 The default value of the `$locales` parameter changed to include all locales.
    #// 
    #// @param array $locales Theme locales. Default is all available locales of the site.
    #//
    locales_ = apply_filters("themes_update_check_locales", locales_)
    locales_ = array_unique(locales_)
    if doing_cron_:
        timeout_ = 30
    else:
        #// Three seconds, plus one extra second for every 10 themes.
        timeout_ = 3 + php_int(php_count(themes_) / 10)
    # end if
    options_ = Array({"timeout": timeout_, "body": Array({"themes": wp_json_encode(request_), "translations": wp_json_encode(translations_), "locale": wp_json_encode(locales_)})}, {"user-agent": "WordPress/" + wp_version_ + "; " + home_url("/")})
    if extra_stats_:
        options_["body"]["update_stats"] = wp_json_encode(extra_stats_)
    # end if
    url_ = "http://api.wordpress.org/themes/update-check/1.1/"
    http_url_ = url_
    ssl_ = wp_http_supports(Array("ssl"))
    if ssl_:
        url_ = set_url_scheme(url_, "https")
    # end if
    raw_response_ = wp_remote_post(url_, options_)
    if ssl_ and is_wp_error(raw_response_):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        raw_response_ = wp_remote_post(http_url_, options_)
    # end if
    if is_wp_error(raw_response_) or 200 != wp_remote_retrieve_response_code(raw_response_):
        return
    # end if
    new_update_ = php_new_class("stdClass", lambda : stdClass())
    new_update_.last_checked = time()
    new_update_.checked = checked_
    response_ = php_json_decode(wp_remote_retrieve_body(raw_response_), True)
    if php_is_array(response_):
        new_update_.response = response_["themes"]
        new_update_.translations = response_["translations"]
    # end if
    set_site_transient("update_themes", new_update_)
# end def wp_update_themes
#// 
#// Performs WordPress automatic background updates.
#// 
#// @since 3.7.0
#//
def wp_maybe_auto_update(*_args_):
    
    
    php_include_file(ABSPATH + "wp-admin/includes/admin.php", once=False)
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    upgrader_ = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
    upgrader_.run()
# end def wp_maybe_auto_update
#// 
#// Retrieves a list of all language updates available.
#// 
#// @since 3.7.0
#// 
#// @return object[] Array of translation objects that have available updates.
#//
def wp_get_translation_updates(*_args_):
    
    
    updates_ = Array()
    transients_ = Array({"update_core": "core", "update_plugins": "plugin", "update_themes": "theme"})
    for transient_,type_ in transients_.items():
        transient_ = get_site_transient(transient_)
        if php_empty(lambda : transient_.translations):
            continue
        # end if
        for translation_ in transient_.translations:
            updates_[-1] = translation_
        # end for
    # end for
    return updates_
# end def wp_get_translation_updates
#// 
#// Collect counts and UI strings for available updates
#// 
#// @since 3.3.0
#// 
#// @return array
#//
def wp_get_update_data(*_args_):
    
    
    counts_ = Array({"plugins": 0, "themes": 0, "wordpress": 0, "translations": 0})
    plugins_ = current_user_can("update_plugins")
    if plugins_:
        update_plugins_ = get_site_transient("update_plugins")
        if (not php_empty(lambda : update_plugins_.response)):
            counts_["plugins"] = php_count(update_plugins_.response)
        # end if
    # end if
    themes_ = current_user_can("update_themes")
    if themes_:
        update_themes_ = get_site_transient("update_themes")
        if (not php_empty(lambda : update_themes_.response)):
            counts_["themes"] = php_count(update_themes_.response)
        # end if
    # end if
    core_ = current_user_can("update_core")
    if core_ and php_function_exists("get_core_updates"):
        update_wordpress_ = get_core_updates(Array({"dismissed": False}))
        if (not php_empty(lambda : update_wordpress_)) and (not php_in_array(update_wordpress_[0].response, Array("development", "latest"))) and current_user_can("update_core"):
            counts_["wordpress"] = 1
        # end if
    # end if
    if core_ or plugins_ or themes_ and wp_get_translation_updates():
        counts_["translations"] = 1
    # end if
    counts_["total"] = counts_["plugins"] + counts_["themes"] + counts_["wordpress"] + counts_["translations"]
    titles_ = Array()
    if counts_["wordpress"]:
        #// translators: %d: Number of available WordPress updates.
        titles_["wordpress"] = php_sprintf(__("%d WordPress Update"), counts_["wordpress"])
    # end if
    if counts_["plugins"]:
        #// translators: %d: Number of available plugin updates.
        titles_["plugins"] = php_sprintf(_n("%d Plugin Update", "%d Plugin Updates", counts_["plugins"]), counts_["plugins"])
    # end if
    if counts_["themes"]:
        #// translators: %d: Number of available theme updates.
        titles_["themes"] = php_sprintf(_n("%d Theme Update", "%d Theme Updates", counts_["themes"]), counts_["themes"])
    # end if
    if counts_["translations"]:
        titles_["translations"] = __("Translation Updates")
    # end if
    update_title_ = esc_attr(php_implode(", ", titles_)) if titles_ else ""
    update_data_ = Array({"counts": counts_, "title": update_title_})
    #// 
    #// Filters the returned array of update data for plugins, themes, and WordPress core.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array $update_data {
    #// Fetched update data.
    #// 
    #// @type array   $counts       An array of counts for available plugin, theme, and WordPress updates.
    #// @type string  $update_title Titles of available updates.
    #// }
    #// @param array $titles An array of update counts and UI strings for available updates.
    #//
    return apply_filters("wp_get_update_data", update_data_, titles_)
# end def wp_get_update_data
#// 
#// Determines whether core should be updated.
#// 
#// @since 2.8.0
#// 
#// @global string $wp_version The WordPress version string.
#//
def _maybe_update_core(*_args_):
    
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    current_ = get_site_transient("update_core")
    if (php_isset(lambda : current_.last_checked) and php_isset(lambda : current_.version_checked)) and 12 * HOUR_IN_SECONDS > time() - current_.last_checked and current_.version_checked == wp_version_:
        return
    # end if
    wp_version_check()
# end def _maybe_update_core
#// 
#// Check the last time plugins were run before checking plugin versions.
#// 
#// This might have been backported to WordPress 2.6.1 for performance reasons.
#// This is used for the wp-admin to check only so often instead of every page
#// load.
#// 
#// @since 2.7.0
#// @access private
#//
def _maybe_update_plugins(*_args_):
    
    
    current_ = get_site_transient("update_plugins")
    if (php_isset(lambda : current_.last_checked)) and 12 * HOUR_IN_SECONDS > time() - current_.last_checked:
        return
    # end if
    wp_update_plugins()
# end def _maybe_update_plugins
#// 
#// Check themes versions only after a duration of time.
#// 
#// This is for performance reasons to make sure that on the theme version
#// checker is not run on every page load.
#// 
#// @since 2.7.0
#// @access private
#//
def _maybe_update_themes(*_args_):
    
    
    current_ = get_site_transient("update_themes")
    if (php_isset(lambda : current_.last_checked)) and 12 * HOUR_IN_SECONDS > time() - current_.last_checked:
        return
    # end if
    wp_update_themes()
# end def _maybe_update_themes
#// 
#// Schedule core, theme, and plugin update checks.
#// 
#// @since 3.1.0
#//
def wp_schedule_update_checks(*_args_):
    
    
    if (not wp_next_scheduled("wp_version_check")) and (not wp_installing()):
        wp_schedule_event(time(), "twicedaily", "wp_version_check")
    # end if
    if (not wp_next_scheduled("wp_update_plugins")) and (not wp_installing()):
        wp_schedule_event(time(), "twicedaily", "wp_update_plugins")
    # end if
    if (not wp_next_scheduled("wp_update_themes")) and (not wp_installing()):
        wp_schedule_event(time(), "twicedaily", "wp_update_themes")
    # end if
# end def wp_schedule_update_checks
#// 
#// Clear existing update caches for plugins, themes, and core.
#// 
#// @since 4.1.0
#//
def wp_clean_update_cache(*_args_):
    
    
    if php_function_exists("wp_clean_plugins_cache"):
        wp_clean_plugins_cache()
    else:
        delete_site_transient("update_plugins")
    # end if
    wp_clean_themes_cache()
    delete_site_transient("update_core")
# end def wp_clean_update_cache
if (not is_main_site()) and (not is_network_admin()) or wp_doing_ajax():
    sys.exit(-1)
# end if
add_action("admin_init", "_maybe_update_core")
add_action("wp_version_check", "wp_version_check")
add_action("load-plugins.php", "wp_update_plugins")
add_action("load-update.php", "wp_update_plugins")
add_action("load-update-core.php", "wp_update_plugins")
add_action("admin_init", "_maybe_update_plugins")
add_action("wp_update_plugins", "wp_update_plugins")
add_action("load-themes.php", "wp_update_themes")
add_action("load-update.php", "wp_update_themes")
add_action("load-update-core.php", "wp_update_themes")
add_action("admin_init", "_maybe_update_themes")
add_action("wp_update_themes", "wp_update_themes")
add_action("update_option_WPLANG", "wp_clean_update_cache", 10, 0)
add_action("wp_maybe_auto_update", "wp_maybe_auto_update")
add_action("init", "wp_schedule_update_checks")
