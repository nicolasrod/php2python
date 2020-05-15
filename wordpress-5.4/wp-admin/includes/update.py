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
#// WordPress Administration Update API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Selects the first update version from the update_core option.
#// 
#// @since 2.7.0
#// 
#// @return object|array|false The response from the API on success, false on failure.
#//
def get_preferred_from_update_core(*args_):
    
    updates = get_core_updates()
    if (not php_is_array(updates)):
        return False
    # end if
    if php_empty(lambda : updates):
        return Array({"response": "latest"})
    # end if
    return updates[0]
# end def get_preferred_from_update_core
#// 
#// Gets available core updates.
#// 
#// @since 2.7.0
#// 
#// @param array $options Set $options['dismissed'] to true to show dismissed upgrades too,
#// set $options['available'] to false to skip not-dismissed updates.
#// @return array|false Array of the update objects on success, false on failure.
#//
def get_core_updates(options=Array(), *args_):
    
    options = php_array_merge(Array({"available": True, "dismissed": False}), options)
    dismissed = get_site_option("dismissed_update_core")
    if (not php_is_array(dismissed)):
        dismissed = Array()
    # end if
    from_api = get_site_transient("update_core")
    if (not (php_isset(lambda : from_api.updates))) or (not php_is_array(from_api.updates)):
        return False
    # end if
    updates = from_api.updates
    result = Array()
    for update in updates:
        if "autoupdate" == update.response:
            continue
        # end if
        if php_array_key_exists(update.current + "|" + update.locale, dismissed):
            if options["dismissed"]:
                update.dismissed = True
                result[-1] = update
            # end if
        else:
            if options["available"]:
                update.dismissed = False
                result[-1] = update
            # end if
        # end if
    # end for
    return result
# end def get_core_updates
#// 
#// Gets the best available (and enabled) Auto-Update for WordPress core.
#// 
#// If there's 1.2.3 and 1.3 on offer, it'll choose 1.3 if the installation allows it, else, 1.2.3.
#// 
#// @since 3.7.0
#// 
#// @return object|false The core update offering on success, false on failure.
#//
def find_core_auto_update(*args_):
    
    updates = get_site_transient("update_core")
    if (not updates) or php_empty(lambda : updates.updates):
        return False
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    auto_update = False
    upgrader = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
    for update in updates.updates:
        if "autoupdate" != update.response:
            continue
        # end if
        if (not upgrader.should_update("core", update, ABSPATH)):
            continue
        # end if
        if (not auto_update) or php_version_compare(update.current, auto_update.current, ">"):
            auto_update = update
        # end if
    # end for
    return auto_update
# end def find_core_auto_update
#// 
#// Gets and caches the checksums for the given version of WordPress.
#// 
#// @since 3.7.0
#// 
#// @param string $version Version string to query.
#// @param string $locale  Locale to query.
#// @return array|false An array of checksums on success, false on failure.
#//
def get_core_checksums(version=None, locale=None, *args_):
    
    http_url = "http://api.wordpress.org/core/checksums/1.0/?" + http_build_query(compact("version", "locale"), None, "&")
    url = http_url
    ssl = wp_http_supports(Array("ssl"))
    if ssl:
        url = set_url_scheme(url, "https")
    # end if
    options = Array({"timeout": 30 if wp_doing_cron() else 3})
    response = wp_remote_get(url, options)
    if ssl and is_wp_error(response):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        response = wp_remote_get(http_url, options)
    # end if
    if is_wp_error(response) or 200 != wp_remote_retrieve_response_code(response):
        return False
    # end if
    body = php_trim(wp_remote_retrieve_body(response))
    body = php_json_decode(body, True)
    if (not php_is_array(body)) or (not (php_isset(lambda : body["checksums"]))) or (not php_is_array(body["checksums"])):
        return False
    # end if
    return body["checksums"]
# end def get_core_checksums
#// 
#// Dismisses core update.
#// 
#// @since 2.7.0
#// 
#// @param object $update
#// @return bool
#//
def dismiss_core_update(update=None, *args_):
    
    dismissed = get_site_option("dismissed_update_core")
    dismissed[update.current + "|" + update.locale] = True
    return update_site_option("dismissed_update_core", dismissed)
# end def dismiss_core_update
#// 
#// Undismisses core update.
#// 
#// @since 2.7.0
#// 
#// @param string $version
#// @param string $locale
#// @return bool
#//
def undismiss_core_update(version=None, locale=None, *args_):
    
    dismissed = get_site_option("dismissed_update_core")
    key = version + "|" + locale
    if (not (php_isset(lambda : dismissed[key]))):
        return False
    # end if
    dismissed[key] = None
    return update_site_option("dismissed_update_core", dismissed)
# end def undismiss_core_update
#// 
#// Finds the available update for WordPress core.
#// 
#// @since 2.7.0
#// 
#// @param string $version Version string to find the update for.
#// @param string $locale  Locale to find the update for.
#// @return object|false The core update offering on success, false on failure.
#//
def find_core_update(version=None, locale=None, *args_):
    
    from_api = get_site_transient("update_core")
    if (not (php_isset(lambda : from_api.updates))) or (not php_is_array(from_api.updates)):
        return False
    # end if
    updates = from_api.updates
    for update in updates:
        if update.current == version and update.locale == locale:
            return update
        # end if
    # end for
    return False
# end def find_core_update
#// 
#// @since 2.3.0
#// 
#// @param string $msg
#// @return string
#//
def core_update_footer(msg="", *args_):
    
    if (not current_user_can("update_core")):
        #// translators: %s: WordPress version.
        return php_sprintf(__("Version %s"), get_bloginfo("version", "display"))
    # end if
    cur = get_preferred_from_update_core()
    if (not php_is_object(cur)):
        cur = php_new_class("stdClass", lambda : stdClass())
    # end if
    if (not (php_isset(lambda : cur.current))):
        cur.current = ""
    # end if
    if (not (php_isset(lambda : cur.url))):
        cur.url = ""
    # end if
    if (not (php_isset(lambda : cur.response))):
        cur.response = ""
    # end if
    for case in Switch(cur.response):
        if case("development"):
            return php_sprintf(__("You are using a development version (%1$s). Cool! Please <a href=\"%2$s\">stay updated</a>."), get_bloginfo("version", "display"), network_admin_url("update-core.php"))
        # end if
        if case("upgrade"):
            return php_sprintf("<strong><a href=\"%s\">%s</a></strong>", network_admin_url("update-core.php"), php_sprintf(__("Get Version %s"), cur.current))
        # end if
        if case("latest"):
            pass
        # end if
        if case():
            #// translators: %s: WordPress version.
            return php_sprintf(__("Version %s"), get_bloginfo("version", "display"))
        # end if
    # end for
# end def core_update_footer
#// 
#// @since 2.3.0
#// 
#// @global string $pagenow
#// @return void|false
#//
def update_nag(*args_):
    
    if is_multisite() and (not current_user_can("update_core")):
        return False
    # end if
    global pagenow
    php_check_if_defined("pagenow")
    if "update-core.php" == pagenow:
        return
    # end if
    cur = get_preferred_from_update_core()
    if (not (php_isset(lambda : cur.response))) or "upgrade" != cur.response:
        return False
    # end if
    version_url = php_sprintf(esc_url(__("https://wordpress.org/support/wordpress-version/version-%s/")), sanitize_title(cur.current))
    if current_user_can("update_core"):
        msg = php_sprintf(__("<a href=\"%1$s\">WordPress %2$s</a> is available! <a href=\"%3$s\" aria-label=\"%4$s\">Please update now</a>."), version_url, cur.current, network_admin_url("update-core.php"), esc_attr__("Please update WordPress now"))
    else:
        msg = php_sprintf(__("<a href=\"%1$s\">WordPress %2$s</a> is available! Please notify the site administrator."), version_url, cur.current)
    # end if
    php_print(str("<div class='update-nag'>") + str(msg) + str("</div>"))
# end def update_nag
#// 
#// Displays WordPress version and active theme in the 'At a Glance' dashboard widget.
#// 
#// @since 2.5.0
#//
def update_right_now_message(*args_):
    
    theme_name = wp_get_theme()
    if current_user_can("switch_themes"):
        theme_name = php_sprintf("<a href=\"themes.php\">%1$s</a>", theme_name)
    # end if
    msg = ""
    if current_user_can("update_core"):
        cur = get_preferred_from_update_core()
        if (php_isset(lambda : cur.response)) and "upgrade" == cur.response:
            msg += php_sprintf("<a href=\"%s\" class=\"button\" aria-describedby=\"wp-version\">%s</a> ", network_admin_url("update-core.php"), php_sprintf(__("Update to %s"), cur.current if cur.current else __("Latest")))
        # end if
    # end if
    #// translators: 1: Version number, 2: Theme name.
    content = __("WordPress %1$s running %2$s theme.")
    #// 
    #// Filters the text displayed in the 'At a Glance' dashboard widget.
    #// 
    #// Prior to 3.8.0, the widget was named 'Right Now'.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $content Default text.
    #//
    content = apply_filters("update_right_now_text", content)
    msg += php_sprintf("<span id=\"wp-version\">" + content + "</span>", get_bloginfo("version", "display"), theme_name)
    php_print(str("<p id='wp-version-message'>") + str(msg) + str("</p>"))
# end def update_right_now_message
#// 
#// @since 2.9.0
#// 
#// @return array
#//
def get_plugin_updates(*args_):
    
    all_plugins = get_plugins()
    upgrade_plugins = Array()
    current = get_site_transient("update_plugins")
    for plugin_file,plugin_data in all_plugins:
        if (php_isset(lambda : current.response[plugin_file])):
            upgrade_plugins[plugin_file] = plugin_data
            upgrade_plugins[plugin_file].update = current.response[plugin_file]
        # end if
    # end for
    return upgrade_plugins
# end def get_plugin_updates
#// 
#// @since 2.9.0
#//
def wp_plugin_update_rows(*args_):
    
    if (not current_user_can("update_plugins")):
        return
    # end if
    plugins = get_site_transient("update_plugins")
    if (php_isset(lambda : plugins.response)) and php_is_array(plugins.response):
        plugins = php_array_keys(plugins.response)
        for plugin_file in plugins:
            add_action(str("after_plugin_row_") + str(plugin_file), "wp_plugin_update_row", 10, 2)
        # end for
    # end if
# end def wp_plugin_update_rows
#// 
#// Displays update information for a plugin.
#// 
#// @since 2.3.0
#// 
#// @param string $file        Plugin basename.
#// @param array  $plugin_data Plugin information.
#// @return void|false
#//
def wp_plugin_update_row(file=None, plugin_data=None, *args_):
    
    current = get_site_transient("update_plugins")
    if (not (php_isset(lambda : current.response[file]))):
        return False
    # end if
    response = current.response[file]
    plugins_allowedtags = Array({"a": Array({"href": Array(), "title": Array()})}, {"abbr": Array({"title": Array()})}, {"acronym": Array({"title": Array()})}, {"code": Array(), "em": Array(), "strong": Array()})
    plugin_name = wp_kses(plugin_data["Name"], plugins_allowedtags)
    details_url = self_admin_url("plugin-install.php?tab=plugin-information&plugin=" + response.slug + "&section=changelog&TB_iframe=true&width=600&height=800")
    #// @var WP_Plugins_List_Table $wp_list_table
    wp_list_table = _get_list_table("WP_Plugins_List_Table")
    if is_network_admin() or (not is_multisite()):
        if is_network_admin():
            active_class = " active" if is_plugin_active_for_network(file) else ""
        else:
            active_class = " active" if is_plugin_active(file) else ""
        # end if
        requires_php = response.requires_php if (php_isset(lambda : response.requires_php)) else None
        compatible_php = is_php_version_compatible(requires_php)
        notice_type = "notice-warning" if compatible_php else "notice-error"
        printf("<tr class=\"plugin-update-tr%s\" id=\"%s\" data-slug=\"%s\" data-plugin=\"%s\">" + "<td colspan=\"%s\" class=\"plugin-update colspanchange\">" + "<div class=\"update-message notice inline %s notice-alt\"><p>", active_class, esc_attr(response.slug + "-update"), esc_attr(response.slug), esc_attr(file), esc_attr(wp_list_table.get_column_count()), notice_type)
        if (not current_user_can("update_plugins")):
            printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>."), plugin_name, esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name, response.new_version))), esc_attr(response.new_version))
        elif php_empty(lambda : response.package):
            printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>. <em>Automatic update is unavailable for this plugin.</em>"), plugin_name, esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name, response.new_version))), esc_attr(response.new_version))
        else:
            if compatible_php:
                printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\" %6$s>update now</a>."), plugin_name, esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name, response.new_version))), esc_attr(response.new_version), wp_nonce_url(self_admin_url("update.php?action=upgrade-plugin&plugin=") + file, "upgrade-plugin_" + file), php_sprintf("class=\"update-link\" aria-label=\"%s\"", esc_attr(php_sprintf(__("Update %s now"), plugin_name))))
            else:
                printf(__("There is a new version of %1$s available, but it doesn&#8217;t work with your version of PHP. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\">learn more about updating PHP</a>."), plugin_name, esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name, response.new_version))), esc_attr(response.new_version), esc_url(wp_get_update_php_url()))
                wp_update_php_annotation("<br><em>", "</em>")
            # end if
        # end if
        #// 
        #// Fires at the end of the update message container in each
        #// row of the plugins list table.
        #// 
        #// The dynamic portion of the hook name, `$file`, refers to the path
        #// of the plugin's primary file relative to the plugins directory.
        #// 
        #// @since 2.8.0
        #// 
        #// @param array $plugin_data {
        #// An array of plugin metadata.
        #// 
        #// @type string $name        The human-readable name of the plugin.
        #// @type string $plugin_uri  Plugin URI.
        #// @type string $version     Plugin version.
        #// @type string $description Plugin description.
        #// @type string $author      Plugin author.
        #// @type string $author_uri  Plugin author URI.
        #// @type string $text_domain Plugin text domain.
        #// @type string $domain_path Relative path to the plugin's .mo file(s).
        #// @type bool   $network     Whether the plugin can only be activated network wide.
        #// @type string $title       The human-readable title of the plugin.
        #// @type string $author_name Plugin author's name.
        #// @type bool   $update      Whether there's an available update. Default null.
        #// }
        #// @param array $response {
        #// An array of metadata about the available plugin update.
        #// 
        #// @type int    $id          Plugin ID.
        #// @type string $slug        Plugin slug.
        #// @type string $new_version New plugin version.
        #// @type string $url         Plugin URL.
        #// @type string $package     Plugin update package URL.
        #// }
        #//
        do_action(str("in_plugin_update_message-") + str(file), plugin_data, response)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        php_print("</p></div></td></tr>")
    # end if
# end def wp_plugin_update_row
#// 
#// @since 2.9.0
#// 
#// @return array
#//
def get_theme_updates(*args_):
    
    current = get_site_transient("update_themes")
    if (not (php_isset(lambda : current.response))):
        return Array()
    # end if
    update_themes = Array()
    for stylesheet,data in current.response:
        update_themes[stylesheet] = wp_get_theme(stylesheet)
        update_themes[stylesheet].update = data
    # end for
    return update_themes
# end def get_theme_updates
#// 
#// @since 3.1.0
#//
def wp_theme_update_rows(*args_):
    
    if (not current_user_can("update_themes")):
        return
    # end if
    themes = get_site_transient("update_themes")
    if (php_isset(lambda : themes.response)) and php_is_array(themes.response):
        themes = php_array_keys(themes.response)
        for theme in themes:
            add_action(str("after_theme_row_") + str(theme), "wp_theme_update_row", 10, 2)
        # end for
    # end if
# end def wp_theme_update_rows
#// 
#// Displays update information for a theme.
#// 
#// @since 3.1.0
#// 
#// @param string   $theme_key Theme stylesheet.
#// @param WP_Theme $theme     Theme object.
#// @return void|false
#//
def wp_theme_update_row(theme_key=None, theme=None, *args_):
    
    current = get_site_transient("update_themes")
    if (not (php_isset(lambda : current.response[theme_key]))):
        return False
    # end if
    response = current.response[theme_key]
    details_url = add_query_arg(Array({"TB_iframe": "true", "width": 1024, "height": 800}), current.response[theme_key]["url"])
    #// @var WP_MS_Themes_List_Table $wp_list_table
    wp_list_table = _get_list_table("WP_MS_Themes_List_Table")
    active = " active" if theme.is_allowed("network") else ""
    printf("<tr class=\"plugin-update-tr%s\" id=\"%s\" data-slug=\"%s\">" + "<td colspan=\"%s\" class=\"plugin-update colspanchange\">" + "<div class=\"update-message notice inline notice-warning notice-alt\"><p>", active, esc_attr(theme.get_stylesheet() + "-update"), esc_attr(theme.get_stylesheet()), wp_list_table.get_column_count())
    if (not current_user_can("update_themes")):
        printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>."), theme["Name"], esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme["Name"], response["new_version"]))), response["new_version"])
    elif php_empty(lambda : response["package"]):
        printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>. <em>Automatic update is unavailable for this theme.</em>"), theme["Name"], esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme["Name"], response["new_version"]))), response["new_version"])
    else:
        printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\" %6$s>update now</a>."), theme["Name"], esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme["Name"], response["new_version"]))), response["new_version"], wp_nonce_url(self_admin_url("update.php?action=upgrade-theme&theme=") + theme_key, "upgrade-theme_" + theme_key), php_sprintf("class=\"update-link\" aria-label=\"%s\"", esc_attr(php_sprintf(__("Update %s now"), theme["Name"]))))
    # end if
    #// 
    #// Fires at the end of the update message container in each
    #// row of the themes list table.
    #// 
    #// The dynamic portion of the hook name, `$theme_key`, refers to
    #// the theme slug as found in the WordPress.org themes repository.
    #// 
    #// @since 3.1.0
    #// 
    #// @param WP_Theme $theme    The WP_Theme object.
    #// @param array    $response {
    #// An array of metadata about the available theme update.
    #// 
    #// @type string $new_version New theme version.
    #// @type string $url         Theme URL.
    #// @type string $package     Theme update package URL.
    #// }
    #//
    do_action(str("in_theme_update_message-") + str(theme_key), theme, response)
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    php_print("</p></div></td></tr>")
# end def wp_theme_update_row
#// 
#// @since 2.7.0
#// 
#// @global int $upgrading
#// @return void|false
#//
def maintenance_nag(*args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    global upgrading
    php_check_if_defined("upgrading")
    nag = (php_isset(lambda : upgrading))
    if (not nag):
        failed = get_site_option("auto_core_update_failed")
        #// 
        #// If an update failed critically, we may have copied over version.php but not other files.
        #// In that case, if the installation claims we're running the version we attempted, nag.
        #// This is serious enough to err on the side of nagging.
        #// 
        #// If we simply failed to update before we tried to copy any files, then assume things are
        #// OK if they are now running the latest.
        #// 
        #// This flag is cleared whenever a successful update occurs using Core_Upgrader.
        #//
        comparison = ">=" if (not php_empty(lambda : failed["critical"])) else ">"
        if (php_isset(lambda : failed["attempted"])) and php_version_compare(failed["attempted"], wp_version, comparison):
            nag = True
        # end if
    # end if
    if (not nag):
        return False
    # end if
    if current_user_can("update_core"):
        msg = php_sprintf(__("An automated WordPress update has failed to complete - <a href=\"%s\">please attempt the update again now</a>."), "update-core.php")
    else:
        msg = __("An automated WordPress update has failed to complete! Please notify the site administrator.")
    # end if
    php_print(str("<div class='update-nag'>") + str(msg) + str("</div>"))
# end def maintenance_nag
#// 
#// Prints the JavaScript templates for update admin notices.
#// 
#// Template takes one argument with four values:
#// 
#// param {object} data {
#// Arguments for admin notice.
#// 
#// @type string id        ID of the notice.
#// @type string className Class names for the notice.
#// @type string message   The notice's message.
#// @type string type      The type of update the notice is for. Either 'plugin' or 'theme'.
#// }
#// 
#// @since 4.6.0
#//
def wp_print_admin_notice_templates(*args_):
    
    php_print("""   <script id=\"tmpl-wp-updates-admin-notice\" type=\"text/html\">
    <div <# if ( data.id ) { #>id=\"{{ data.id }}\"<# } #> class=\"notice {{ data.className }}\"><p>{{{ data.message }}}</p></div>
    </script>
    <script id=\"tmpl-wp-bulk-updates-admin-notice\" type=\"text/html\">
    <div id=\"{{ data.id }}\" class=\"{{ data.className }} notice <# if ( data.errors ) { #>notice-error<# } else { #>notice-success<# } #>\">
    <p>
    <# if ( data.successes ) { #>
    <# if ( 1 === data.successes ) { #>
    <# if ( 'plugin' === data.type ) { #>
    """)
    #// translators: %s: Number of plugins.
    printf(__("%s plugin successfully updated."), "{{ data.successes }}")
    php_print("                     <# } else { #>\n                            ")
    #// translators: %s: Number of themes.
    printf(__("%s theme successfully updated."), "{{ data.successes }}")
    php_print("""                       <# } #>
    <# } else { #>
    <# if ( 'plugin' === data.type ) { #>
    """)
    #// translators: %s: Number of plugins.
    printf(__("%s plugins successfully updated."), "{{ data.successes }}")
    php_print("                     <# } else { #>\n                            ")
    #// translators: %s: Number of themes.
    printf(__("%s themes successfully updated."), "{{ data.successes }}")
    php_print("""                       <# } #>
    <# } #>
    <# } #>
    <# if ( data.errors ) { #>
    <button class=\"button-link bulk-action-errors-collapsed\" aria-expanded=\"false\">
    <# if ( 1 === data.errors ) { #>
    """)
    #// translators: %s: Number of failed updates.
    printf(__("%s update failed."), "{{ data.errors }}")
    php_print("                     <# } else { #>\n                            ")
    #// translators: %s: Number of failed updates.
    printf(__("%s updates failed."), "{{ data.errors }}")
    php_print("                     <# } #>\n                       <span class=\"screen-reader-text\">")
    _e("Show more details")
    php_print("""</span>
    <span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
    </button>
    <# } #>
    </p>
    <# if ( data.errors ) { #>
    <ul class=\"bulk-action-errors hidden\">
    <# _.each( data.errorMessages, function( errorMessage ) { #>
    <li>{{ errorMessage }}</li>
    <# } ); #>
    </ul>
    <# } #>
    </div>
    </script>
    """)
# end def wp_print_admin_notice_templates
#// 
#// Prints the JavaScript templates for update and deletion rows in list tables.
#// 
#// The update template takes one argument with four values:
#// 
#// param {object} data {
#// Arguments for the update row
#// 
#// @type string slug    Plugin slug.
#// @type string plugin  Plugin base name.
#// @type string colspan The number of table columns this row spans.
#// @type string content The row content.
#// }
#// 
#// The delete template takes one argument with four values:
#// 
#// param {object} data {
#// Arguments for the update row
#// 
#// @type string slug    Plugin slug.
#// @type string plugin  Plugin base name.
#// @type string name    Plugin name.
#// @type string colspan The number of table columns this row spans.
#// }
#// 
#// @since 4.6.0
#//
def wp_print_update_row_templates(*args_):
    
    php_print("""   <script id=\"tmpl-item-update-row\" type=\"text/template\">
    <tr class=\"plugin-update-tr update\" id=\"{{ data.slug }}-update\" data-slug=\"{{ data.slug }}\" <# if ( data.plugin ) { #>data-plugin=\"{{ data.plugin }}\"<# } #>>
    <td colspan=\"{{ data.colspan }}\" class=\"plugin-update colspanchange\">
    {{{ data.content }}}
    </td>
    </tr>
    </script>
    <script id=\"tmpl-item-deleted-row\" type=\"text/template\">
    <tr class=\"plugin-deleted-tr inactive deleted\" id=\"{{ data.slug }}-deleted\" data-slug=\"{{ data.slug }}\" <# if ( data.plugin ) { #>data-plugin=\"{{ data.plugin }}\"<# } #>>
    <td colspan=\"{{ data.colspan }}\" class=\"plugin-update colspanchange\">
    <# if ( data.plugin ) { #>
    """)
    printf(_x("%s was successfully deleted.", "plugin"), "<strong>{{{ data.name }}}</strong>")
    php_print("             <# } else { #>\n                    ")
    printf(_x("%s was successfully deleted.", "theme"), "<strong>{{{ data.name }}}</strong>")
    php_print("""               <# } #>
    </td>
    </tr>
    </script>
    """)
# end def wp_print_update_row_templates
#// 
#// Displays a notice when the user is in recovery mode.
#// 
#// @since 5.2.0
#//
def wp_recovery_mode_nag(*args_):
    
    if (not wp_is_recovery_mode()):
        return
    # end if
    url = wp_login_url()
    url = add_query_arg("action", WP_Recovery_Mode.EXIT_ACTION, url)
    url = wp_nonce_url(url, WP_Recovery_Mode.EXIT_ACTION)
    php_print(" <div class=\"notice notice-info\">\n        <p>\n           ")
    printf(__("You are in recovery mode. This means there may be an error with a theme or plugin. To exit recovery mode, log out or use the Exit button. <a href=\"%s\">Exit Recovery Mode</a>"), esc_url(url))
    php_print("     </p>\n  </div>\n    ")
# end def wp_recovery_mode_nag
