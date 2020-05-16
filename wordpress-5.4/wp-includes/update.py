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
def wp_version_check(extra_stats=Array(), force_check=False, *args_):
    
    if wp_installing():
        return
    # end if
    global wpdb,wp_local_package
    php_check_if_defined("wpdb","wp_local_package")
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    php_version = php_phpversion()
    current = get_site_transient("update_core")
    translations = wp_get_installed_translations("core")
    #// Invalidate the transient when $wp_version changes.
    if php_is_object(current) and wp_version != current.version_checked:
        current = False
    # end if
    if (not php_is_object(current)):
        current = php_new_class("stdClass", lambda : stdClass())
        current.updates = Array()
        current.version_checked = wp_version
    # end if
    if (not php_empty(lambda : extra_stats)):
        force_check = True
    # end if
    #// Wait 1 minute between multiple version check requests.
    timeout = MINUTE_IN_SECONDS
    time_not_changed = (php_isset(lambda : current.last_checked)) and timeout > time() - current.last_checked
    if (not force_check) and time_not_changed:
        return
    # end if
    #// 
    #// Filters the locale requested for WordPress core translations.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $locale Current locale.
    #//
    locale = apply_filters("core_version_check_locale", get_locale())
    #// Update last_checked for current to prevent multiple blocking requests if request hangs.
    current.last_checked = time()
    set_site_transient("update_core", current)
    if php_method_exists(wpdb, "db_version"):
        mysql_version = php_preg_replace("/[^0-9.].*/", "", wpdb.db_version())
    else:
        mysql_version = "N/A"
    # end if
    if is_multisite():
        user_count = get_user_count()
        num_blogs = get_blog_count()
        wp_install = network_site_url()
        multisite_enabled = 1
    else:
        user_count = count_users()
        user_count = user_count["total_users"]
        multisite_enabled = 0
        num_blogs = 1
        wp_install = home_url("/")
    # end if
    query = Array({"version": wp_version, "php": php_version, "locale": locale, "mysql": mysql_version, "local_package": wp_local_package if (php_isset(lambda : wp_local_package)) else "", "blogs": num_blogs, "users": user_count, "multisite_enabled": multisite_enabled, "initial_db_version": get_site_option("initial_db_version")})
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
    query = apply_filters("core_version_check_query_args", query)
    post_body = Array({"translations": wp_json_encode(translations)})
    if php_is_array(extra_stats):
        post_body = php_array_merge(post_body, extra_stats)
    # end if
    url = "http://api.wordpress.org/core/version-check/1.7/?" + http_build_query(query, None, "&")
    http_url = url
    ssl = wp_http_supports(Array("ssl"))
    if ssl:
        url = set_url_scheme(url, "https")
    # end if
    doing_cron = wp_doing_cron()
    options = Array({"timeout": 30 if doing_cron else 3, "user-agent": "WordPress/" + wp_version + "; " + home_url("/"), "headers": Array({"wp_install": wp_install, "wp_blog": home_url("/")})}, {"body": post_body})
    response = wp_remote_post(url, options)
    if ssl and is_wp_error(response):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        response = wp_remote_post(http_url, options)
    # end if
    if is_wp_error(response) or 200 != wp_remote_retrieve_response_code(response):
        return
    # end if
    body = php_trim(wp_remote_retrieve_body(response))
    body = php_json_decode(body, True)
    if (not php_is_array(body)) or (not (php_isset(lambda : body["offers"]))):
        return
    # end if
    offers = body["offers"]
    for offer in offers:
        for offer_key,value in offer:
            if "packages" == offer_key:
                offer["packages"] = php_array_intersect_key(php_array_map("esc_url", offer["packages"]), php_array_fill_keys(Array("full", "no_content", "new_bundled", "partial", "rollback"), ""))
            elif "download" == offer_key:
                offer["download"] = esc_url(value)
            else:
                offer[offer_key] = esc_html(value)
            # end if
        # end for
        offer = php_array_intersect_key(offer, php_array_fill_keys(Array("response", "download", "locale", "packages", "current", "version", "php_version", "mysql_version", "new_bundled", "partial_version", "notify_email", "support_email", "new_files"), ""))
    # end for
    updates = php_new_class("stdClass", lambda : stdClass())
    updates.updates = offers
    updates.last_checked = time()
    updates.version_checked = wp_version
    if (php_isset(lambda : body["translations"])):
        updates.translations = body["translations"]
    # end if
    set_site_transient("update_core", updates)
    if (not php_empty(lambda : body["ttl"])):
        ttl = php_int(body["ttl"])
        if ttl and time() + ttl < wp_next_scheduled("wp_version_check"):
            #// Queue an event to re-run the update check in $ttl seconds.
            wp_schedule_single_event(time() + ttl, "wp_version_check")
        # end if
    # end if
    #// Trigger background updates if running non-interactively, and we weren't called from the update handler.
    if doing_cron and (not doing_action("wp_maybe_auto_update")):
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
def wp_update_plugins(extra_stats=Array(), *args_):
    
    if wp_installing():
        return
    # end if
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    #// If running blog-side, bail unless we've not checked in the last 12 hours.
    if (not php_function_exists("get_plugins")):
        php_include_file(ABSPATH + "wp-admin/includes/plugin.php", once=True)
    # end if
    plugins = get_plugins()
    translations = wp_get_installed_translations("plugins")
    active = get_option("active_plugins", Array())
    current = get_site_transient("update_plugins")
    if (not php_is_object(current)):
        current = php_new_class("stdClass", lambda : stdClass())
    # end if
    new_option = php_new_class("stdClass", lambda : stdClass())
    new_option.last_checked = time()
    doing_cron = wp_doing_cron()
    #// Check for update on a different schedule, depending on the page.
    for case in Switch(current_filter()):
        if case("upgrader_process_complete"):
            timeout = 0
            break
        # end if
        if case("load-update-core.php"):
            timeout = MINUTE_IN_SECONDS
            break
        # end if
        if case("load-plugins.php"):
            pass
        # end if
        if case("load-update.php"):
            timeout = HOUR_IN_SECONDS
            break
        # end if
        if case():
            if doing_cron:
                timeout = 2 * HOUR_IN_SECONDS
            else:
                timeout = 12 * HOUR_IN_SECONDS
            # end if
        # end if
    # end for
    time_not_changed = (php_isset(lambda : current.last_checked)) and timeout > time() - current.last_checked
    if time_not_changed and (not extra_stats):
        plugin_changed = False
        for file,p in plugins:
            new_option.checked[file] = p["Version"]
            if (not (php_isset(lambda : current.checked[file]))) or php_strval(current.checked[file]) != php_strval(p["Version"]):
                plugin_changed = True
            # end if
        # end for
        if (php_isset(lambda : current.response)) and php_is_array(current.response):
            for plugin_file,update_details in current.response:
                if (not (php_isset(lambda : plugins[plugin_file]))):
                    plugin_changed = True
                    break
                # end if
            # end for
        # end if
        #// Bail if we've checked recently and if nothing has changed.
        if (not plugin_changed):
            return
        # end if
    # end if
    #// Update last_checked for current to prevent multiple blocking requests if request hangs.
    current.last_checked = time()
    set_site_transient("update_plugins", current)
    to_send = compact("plugins", "active")
    locales = php_array_values(get_available_languages())
    #// 
    #// Filters the locales requested for plugin translations.
    #// 
    #// @since 3.7.0
    #// @since 4.5.0 The default value of the `$locales` parameter changed to include all locales.
    #// 
    #// @param array $locales Plugin locales. Default is all available locales of the site.
    #//
    locales = apply_filters("plugins_update_check_locales", locales)
    locales = array_unique(locales)
    if doing_cron:
        timeout = 30
    else:
        #// Three seconds, plus one extra second for every 10 plugins.
        timeout = 3 + php_int(php_count(plugins) / 10)
    # end if
    options = Array({"timeout": timeout, "body": Array({"plugins": wp_json_encode(to_send), "translations": wp_json_encode(translations), "locale": wp_json_encode(locales), "all": wp_json_encode(True)})}, {"user-agent": "WordPress/" + wp_version + "; " + home_url("/")})
    if extra_stats:
        options["body"]["update_stats"] = wp_json_encode(extra_stats)
    # end if
    url = "http://api.wordpress.org/plugins/update-check/1.1/"
    http_url = url
    ssl = wp_http_supports(Array("ssl"))
    if ssl:
        url = set_url_scheme(url, "https")
    # end if
    raw_response = wp_remote_post(url, options)
    if ssl and is_wp_error(raw_response):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        raw_response = wp_remote_post(http_url, options)
    # end if
    if is_wp_error(raw_response) or 200 != wp_remote_retrieve_response_code(raw_response):
        return
    # end if
    response = php_json_decode(wp_remote_retrieve_body(raw_response), True)
    for plugin in response["plugins"]:
        plugin = plugin
        if (php_isset(lambda : plugin.compatibility)):
            plugin.compatibility = plugin.compatibility
            for data in plugin.compatibility:
                data = data
            # end for
        # end if
    # end for
    plugin = None
    data = None
    for plugin in response["no_update"]:
        plugin = plugin
    # end for
    plugin = None
    if php_is_array(response):
        new_option.response = response["plugins"]
        new_option.translations = response["translations"]
        #// TODO: Perhaps better to store no_update in a separate transient with an expiry?
        new_option.no_update = response["no_update"]
    else:
        new_option.response = Array()
        new_option.translations = Array()
        new_option.no_update = Array()
    # end if
    set_site_transient("update_plugins", new_option)
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
def wp_update_themes(extra_stats=Array(), *args_):
    
    if wp_installing():
        return
    # end if
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    installed_themes = wp_get_themes()
    translations = wp_get_installed_translations("themes")
    last_update = get_site_transient("update_themes")
    if (not php_is_object(last_update)):
        last_update = php_new_class("stdClass", lambda : stdClass())
    # end if
    themes = Array()
    checked = Array()
    request = Array()
    #// Put slug of current theme into request.
    request["active"] = get_option("stylesheet")
    for theme in installed_themes:
        checked[theme.get_stylesheet()] = theme.get("Version")
        themes[theme.get_stylesheet()] = Array({"Name": theme.get("Name"), "Title": theme.get("Name"), "Version": theme.get("Version"), "Author": theme.get("Author"), "Author URI": theme.get("AuthorURI"), "Template": theme.get_template(), "Stylesheet": theme.get_stylesheet()})
    # end for
    doing_cron = wp_doing_cron()
    #// Check for update on a different schedule, depending on the page.
    for case in Switch(current_filter()):
        if case("upgrader_process_complete"):
            timeout = 0
            break
        # end if
        if case("load-update-core.php"):
            timeout = MINUTE_IN_SECONDS
            break
        # end if
        if case("load-themes.php"):
            pass
        # end if
        if case("load-update.php"):
            timeout = HOUR_IN_SECONDS
            break
        # end if
        if case():
            if doing_cron:
                timeout = 2 * HOUR_IN_SECONDS
            else:
                timeout = 12 * HOUR_IN_SECONDS
            # end if
        # end if
    # end for
    time_not_changed = (php_isset(lambda : last_update.last_checked)) and timeout > time() - last_update.last_checked
    if time_not_changed and (not extra_stats):
        theme_changed = False
        for slug,v in checked:
            if (not (php_isset(lambda : last_update.checked[slug]))) or php_strval(last_update.checked[slug]) != php_strval(v):
                theme_changed = True
            # end if
        # end for
        if (php_isset(lambda : last_update.response)) and php_is_array(last_update.response):
            for slug,update_details in last_update.response:
                if (not (php_isset(lambda : checked[slug]))):
                    theme_changed = True
                    break
                # end if
            # end for
        # end if
        #// Bail if we've checked recently and if nothing has changed.
        if (not theme_changed):
            return
        # end if
    # end if
    #// Update last_checked for current to prevent multiple blocking requests if request hangs.
    last_update.last_checked = time()
    set_site_transient("update_themes", last_update)
    request["themes"] = themes
    locales = php_array_values(get_available_languages())
    #// 
    #// Filters the locales requested for theme translations.
    #// 
    #// @since 3.7.0
    #// @since 4.5.0 The default value of the `$locales` parameter changed to include all locales.
    #// 
    #// @param array $locales Theme locales. Default is all available locales of the site.
    #//
    locales = apply_filters("themes_update_check_locales", locales)
    locales = array_unique(locales)
    if doing_cron:
        timeout = 30
    else:
        #// Three seconds, plus one extra second for every 10 themes.
        timeout = 3 + php_int(php_count(themes) / 10)
    # end if
    options = Array({"timeout": timeout, "body": Array({"themes": wp_json_encode(request), "translations": wp_json_encode(translations), "locale": wp_json_encode(locales)})}, {"user-agent": "WordPress/" + wp_version + "; " + home_url("/")})
    if extra_stats:
        options["body"]["update_stats"] = wp_json_encode(extra_stats)
    # end if
    url = "http://api.wordpress.org/themes/update-check/1.1/"
    http_url = url
    ssl = wp_http_supports(Array("ssl"))
    if ssl:
        url = set_url_scheme(url, "https")
    # end if
    raw_response = wp_remote_post(url, options)
    if ssl and is_wp_error(raw_response):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        raw_response = wp_remote_post(http_url, options)
    # end if
    if is_wp_error(raw_response) or 200 != wp_remote_retrieve_response_code(raw_response):
        return
    # end if
    new_update = php_new_class("stdClass", lambda : stdClass())
    new_update.last_checked = time()
    new_update.checked = checked
    response = php_json_decode(wp_remote_retrieve_body(raw_response), True)
    if php_is_array(response):
        new_update.response = response["themes"]
        new_update.translations = response["translations"]
    # end if
    set_site_transient("update_themes", new_update)
# end def wp_update_themes
#// 
#// Performs WordPress automatic background updates.
#// 
#// @since 3.7.0
#//
def wp_maybe_auto_update(*args_):
    
    php_include_file(ABSPATH + "wp-admin/includes/admin.php", once=False)
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    upgrader = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
    upgrader.run()
# end def wp_maybe_auto_update
#// 
#// Retrieves a list of all language updates available.
#// 
#// @since 3.7.0
#// 
#// @return object[] Array of translation objects that have available updates.
#//
def wp_get_translation_updates(*args_):
    
    updates = Array()
    transients = Array({"update_core": "core", "update_plugins": "plugin", "update_themes": "theme"})
    for transient,type in transients:
        transient = get_site_transient(transient)
        if php_empty(lambda : transient.translations):
            continue
        # end if
        for translation in transient.translations:
            updates[-1] = translation
        # end for
    # end for
    return updates
# end def wp_get_translation_updates
#// 
#// Collect counts and UI strings for available updates
#// 
#// @since 3.3.0
#// 
#// @return array
#//
def wp_get_update_data(*args_):
    
    counts = Array({"plugins": 0, "themes": 0, "wordpress": 0, "translations": 0})
    plugins = current_user_can("update_plugins")
    if plugins:
        update_plugins = get_site_transient("update_plugins")
        if (not php_empty(lambda : update_plugins.response)):
            counts["plugins"] = php_count(update_plugins.response)
        # end if
    # end if
    themes = current_user_can("update_themes")
    if themes:
        update_themes = get_site_transient("update_themes")
        if (not php_empty(lambda : update_themes.response)):
            counts["themes"] = php_count(update_themes.response)
        # end if
    # end if
    core = current_user_can("update_core")
    if core and php_function_exists("get_core_updates"):
        update_wordpress = get_core_updates(Array({"dismissed": False}))
        if (not php_empty(lambda : update_wordpress)) and (not php_in_array(update_wordpress[0].response, Array("development", "latest"))) and current_user_can("update_core"):
            counts["wordpress"] = 1
        # end if
    # end if
    if core or plugins or themes and wp_get_translation_updates():
        counts["translations"] = 1
    # end if
    counts["total"] = counts["plugins"] + counts["themes"] + counts["wordpress"] + counts["translations"]
    titles = Array()
    if counts["wordpress"]:
        #// translators: %d: Number of available WordPress updates.
        titles["wordpress"] = php_sprintf(__("%d WordPress Update"), counts["wordpress"])
    # end if
    if counts["plugins"]:
        #// translators: %d: Number of available plugin updates.
        titles["plugins"] = php_sprintf(_n("%d Plugin Update", "%d Plugin Updates", counts["plugins"]), counts["plugins"])
    # end if
    if counts["themes"]:
        #// translators: %d: Number of available theme updates.
        titles["themes"] = php_sprintf(_n("%d Theme Update", "%d Theme Updates", counts["themes"]), counts["themes"])
    # end if
    if counts["translations"]:
        titles["translations"] = __("Translation Updates")
    # end if
    update_title = esc_attr(php_implode(", ", titles)) if titles else ""
    update_data = Array({"counts": counts, "title": update_title})
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
    return apply_filters("wp_get_update_data", update_data, titles)
# end def wp_get_update_data
#// 
#// Determines whether core should be updated.
#// 
#// @since 2.8.0
#// 
#// @global string $wp_version The WordPress version string.
#//
def _maybe_update_core(*args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    current = get_site_transient("update_core")
    if (php_isset(lambda : current.last_checked) and php_isset(lambda : current.version_checked)) and 12 * HOUR_IN_SECONDS > time() - current.last_checked and current.version_checked == wp_version:
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
def _maybe_update_plugins(*args_):
    
    current = get_site_transient("update_plugins")
    if (php_isset(lambda : current.last_checked)) and 12 * HOUR_IN_SECONDS > time() - current.last_checked:
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
def _maybe_update_themes(*args_):
    
    current = get_site_transient("update_themes")
    if (php_isset(lambda : current.last_checked)) and 12 * HOUR_IN_SECONDS > time() - current.last_checked:
        return
    # end if
    wp_update_themes()
# end def _maybe_update_themes
#// 
#// Schedule core, theme, and plugin update checks.
#// 
#// @since 3.1.0
#//
def wp_schedule_update_checks(*args_):
    
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
def wp_clean_update_cache(*args_):
    
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
