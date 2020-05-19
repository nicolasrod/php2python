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
def get_preferred_from_update_core(*_args_):
    
    
    updates_ = get_core_updates()
    if (not php_is_array(updates_)):
        return False
    # end if
    if php_empty(lambda : updates_):
        return Array({"response": "latest"})
    # end if
    return updates_[0]
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
def get_core_updates(options_=None, *_args_):
    if options_ is None:
        options_ = Array()
    # end if
    
    options_ = php_array_merge(Array({"available": True, "dismissed": False}), options_)
    dismissed_ = get_site_option("dismissed_update_core")
    if (not php_is_array(dismissed_)):
        dismissed_ = Array()
    # end if
    from_api_ = get_site_transient("update_core")
    if (not (php_isset(lambda : from_api_.updates))) or (not php_is_array(from_api_.updates)):
        return False
    # end if
    updates_ = from_api_.updates
    result_ = Array()
    for update_ in updates_:
        if "autoupdate" == update_.response:
            continue
        # end if
        if php_array_key_exists(update_.current + "|" + update_.locale, dismissed_):
            if options_["dismissed"]:
                update_.dismissed = True
                result_[-1] = update_
            # end if
        else:
            if options_["available"]:
                update_.dismissed = False
                result_[-1] = update_
            # end if
        # end if
    # end for
    return result_
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
def find_core_auto_update(*_args_):
    
    
    updates_ = get_site_transient("update_core")
    if (not updates_) or php_empty(lambda : updates_.updates):
        return False
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    auto_update_ = False
    upgrader_ = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
    for update_ in updates_.updates:
        if "autoupdate" != update_.response:
            continue
        # end if
        if (not upgrader_.should_update("core", update_, ABSPATH)):
            continue
        # end if
        if (not auto_update_) or php_version_compare(update_.current, auto_update_.current, ">"):
            auto_update_ = update_
        # end if
    # end for
    return auto_update_
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
def get_core_checksums(version_=None, locale_=None, *_args_):
    
    
    http_url_ = "http://api.wordpress.org/core/checksums/1.0/?" + http_build_query(php_compact("version_", "locale_"), None, "&")
    url_ = http_url_
    ssl_ = wp_http_supports(Array("ssl"))
    if ssl_:
        url_ = set_url_scheme(url_, "https")
    # end if
    options_ = Array({"timeout": 30 if wp_doing_cron() else 3})
    response_ = wp_remote_get(url_, options_)
    if ssl_ and is_wp_error(response_):
        trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
        response_ = wp_remote_get(http_url_, options_)
    # end if
    if is_wp_error(response_) or 200 != wp_remote_retrieve_response_code(response_):
        return False
    # end if
    body_ = php_trim(wp_remote_retrieve_body(response_))
    body_ = php_json_decode(body_, True)
    if (not php_is_array(body_)) or (not (php_isset(lambda : body_["checksums"]))) or (not php_is_array(body_["checksums"])):
        return False
    # end if
    return body_["checksums"]
# end def get_core_checksums
#// 
#// Dismisses core update.
#// 
#// @since 2.7.0
#// 
#// @param object $update
#// @return bool
#//
def dismiss_core_update(update_=None, *_args_):
    
    
    dismissed_ = get_site_option("dismissed_update_core")
    dismissed_[update_.current + "|" + update_.locale] = True
    return update_site_option("dismissed_update_core", dismissed_)
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
def undismiss_core_update(version_=None, locale_=None, *_args_):
    
    
    dismissed_ = get_site_option("dismissed_update_core")
    key_ = version_ + "|" + locale_
    if (not (php_isset(lambda : dismissed_[key_]))):
        return False
    # end if
    dismissed_[key_] = None
    return update_site_option("dismissed_update_core", dismissed_)
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
def find_core_update(version_=None, locale_=None, *_args_):
    
    
    from_api_ = get_site_transient("update_core")
    if (not (php_isset(lambda : from_api_.updates))) or (not php_is_array(from_api_.updates)):
        return False
    # end if
    updates_ = from_api_.updates
    for update_ in updates_:
        if update_.current == version_ and update_.locale == locale_:
            return update_
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
def core_update_footer(msg_="", *_args_):
    
    
    if (not current_user_can("update_core")):
        #// translators: %s: WordPress version.
        return php_sprintf(__("Version %s"), get_bloginfo("version", "display"))
    # end if
    cur_ = get_preferred_from_update_core()
    if (not php_is_object(cur_)):
        cur_ = php_new_class("stdClass", lambda : stdClass())
    # end if
    if (not (php_isset(lambda : cur_.current))):
        cur_.current = ""
    # end if
    if (not (php_isset(lambda : cur_.url))):
        cur_.url = ""
    # end if
    if (not (php_isset(lambda : cur_.response))):
        cur_.response = ""
    # end if
    for case in Switch(cur_.response):
        if case("development"):
            return php_sprintf(__("You are using a development version (%1$s). Cool! Please <a href=\"%2$s\">stay updated</a>."), get_bloginfo("version", "display"), network_admin_url("update-core.php"))
        # end if
        if case("upgrade"):
            return php_sprintf("<strong><a href=\"%s\">%s</a></strong>", network_admin_url("update-core.php"), php_sprintf(__("Get Version %s"), cur_.current))
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
def update_nag(*_args_):
    
    
    if is_multisite() and (not current_user_can("update_core")):
        return False
    # end if
    global pagenow_
    php_check_if_defined("pagenow_")
    if "update-core.php" == pagenow_:
        return
    # end if
    cur_ = get_preferred_from_update_core()
    if (not (php_isset(lambda : cur_.response))) or "upgrade" != cur_.response:
        return False
    # end if
    version_url_ = php_sprintf(esc_url(__("https://wordpress.org/support/wordpress-version/version-%s/")), sanitize_title(cur_.current))
    if current_user_can("update_core"):
        msg_ = php_sprintf(__("<a href=\"%1$s\">WordPress %2$s</a> is available! <a href=\"%3$s\" aria-label=\"%4$s\">Please update now</a>."), version_url_, cur_.current, network_admin_url("update-core.php"), esc_attr__("Please update WordPress now"))
    else:
        msg_ = php_sprintf(__("<a href=\"%1$s\">WordPress %2$s</a> is available! Please notify the site administrator."), version_url_, cur_.current)
    # end if
    php_print(str("<div class='update-nag'>") + str(msg_) + str("</div>"))
# end def update_nag
#// 
#// Displays WordPress version and active theme in the 'At a Glance' dashboard widget.
#// 
#// @since 2.5.0
#//
def update_right_now_message(*_args_):
    
    
    theme_name_ = wp_get_theme()
    if current_user_can("switch_themes"):
        theme_name_ = php_sprintf("<a href=\"themes.php\">%1$s</a>", theme_name_)
    # end if
    msg_ = ""
    if current_user_can("update_core"):
        cur_ = get_preferred_from_update_core()
        if (php_isset(lambda : cur_.response)) and "upgrade" == cur_.response:
            msg_ += php_sprintf("<a href=\"%s\" class=\"button\" aria-describedby=\"wp-version\">%s</a> ", network_admin_url("update-core.php"), php_sprintf(__("Update to %s"), cur_.current if cur_.current else __("Latest")))
        # end if
    # end if
    #// translators: 1: Version number, 2: Theme name.
    content_ = __("WordPress %1$s running %2$s theme.")
    #// 
    #// Filters the text displayed in the 'At a Glance' dashboard widget.
    #// 
    #// Prior to 3.8.0, the widget was named 'Right Now'.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $content Default text.
    #//
    content_ = apply_filters("update_right_now_text", content_)
    msg_ += php_sprintf("<span id=\"wp-version\">" + content_ + "</span>", get_bloginfo("version", "display"), theme_name_)
    php_print(str("<p id='wp-version-message'>") + str(msg_) + str("</p>"))
# end def update_right_now_message
#// 
#// @since 2.9.0
#// 
#// @return array
#//
def get_plugin_updates(*_args_):
    
    
    all_plugins_ = get_plugins()
    upgrade_plugins_ = Array()
    current_ = get_site_transient("update_plugins")
    for plugin_file_,plugin_data_ in all_plugins_.items():
        if (php_isset(lambda : current_.response[plugin_file_])):
            upgrade_plugins_[plugin_file_] = plugin_data_
            upgrade_plugins_[plugin_file_].update = current_.response[plugin_file_]
        # end if
    # end for
    return upgrade_plugins_
# end def get_plugin_updates
#// 
#// @since 2.9.0
#//
def wp_plugin_update_rows(*_args_):
    
    
    if (not current_user_can("update_plugins")):
        return
    # end if
    plugins_ = get_site_transient("update_plugins")
    if (php_isset(lambda : plugins_.response)) and php_is_array(plugins_.response):
        plugins_ = php_array_keys(plugins_.response)
        for plugin_file_ in plugins_:
            add_action(str("after_plugin_row_") + str(plugin_file_), "wp_plugin_update_row", 10, 2)
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
def wp_plugin_update_row(file_=None, plugin_data_=None, *_args_):
    
    
    current_ = get_site_transient("update_plugins")
    if (not (php_isset(lambda : current_.response[file_]))):
        return False
    # end if
    response_ = current_.response[file_]
    plugins_allowedtags_ = Array({"a": Array({"href": Array(), "title": Array()})}, {"abbr": Array({"title": Array()})}, {"acronym": Array({"title": Array()})}, {"code": Array(), "em": Array(), "strong": Array()})
    plugin_name_ = wp_kses(plugin_data_["Name"], plugins_allowedtags_)
    details_url_ = self_admin_url("plugin-install.php?tab=plugin-information&plugin=" + response_.slug + "&section=changelog&TB_iframe=true&width=600&height=800")
    #// @var WP_Plugins_List_Table $wp_list_table
    wp_list_table_ = _get_list_table("WP_Plugins_List_Table")
    if is_network_admin() or (not is_multisite()):
        if is_network_admin():
            active_class_ = " active" if is_plugin_active_for_network(file_) else ""
        else:
            active_class_ = " active" if is_plugin_active(file_) else ""
        # end if
        requires_php_ = response_.requires_php if (php_isset(lambda : response_.requires_php)) else None
        compatible_php_ = is_php_version_compatible(requires_php_)
        notice_type_ = "notice-warning" if compatible_php_ else "notice-error"
        php_printf("<tr class=\"plugin-update-tr%s\" id=\"%s\" data-slug=\"%s\" data-plugin=\"%s\">" + "<td colspan=\"%s\" class=\"plugin-update colspanchange\">" + "<div class=\"update-message notice inline %s notice-alt\"><p>", active_class_, esc_attr(response_.slug + "-update"), esc_attr(response_.slug), esc_attr(file_), esc_attr(wp_list_table_.get_column_count()), notice_type_)
        if (not current_user_can("update_plugins")):
            php_printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>."), plugin_name_, esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name_, response_.new_version))), esc_attr(response_.new_version))
        elif php_empty(lambda : response_.package):
            php_printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>. <em>Automatic update is unavailable for this plugin.</em>"), plugin_name_, esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name_, response_.new_version))), esc_attr(response_.new_version))
        else:
            if compatible_php_:
                php_printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\" %6$s>update now</a>."), plugin_name_, esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name_, response_.new_version))), esc_attr(response_.new_version), wp_nonce_url(self_admin_url("update.php?action=upgrade-plugin&plugin=") + file_, "upgrade-plugin_" + file_), php_sprintf("class=\"update-link\" aria-label=\"%s\"", esc_attr(php_sprintf(__("Update %s now"), plugin_name_))))
            else:
                php_printf(__("There is a new version of %1$s available, but it doesn&#8217;t work with your version of PHP. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\">learn more about updating PHP</a>."), plugin_name_, esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_name_, response_.new_version))), esc_attr(response_.new_version), esc_url(wp_get_update_php_url()))
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
        do_action(str("in_plugin_update_message-") + str(file_), plugin_data_, response_)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        php_print("</p></div></td></tr>")
    # end if
# end def wp_plugin_update_row
#// 
#// @since 2.9.0
#// 
#// @return array
#//
def get_theme_updates(*_args_):
    
    
    current_ = get_site_transient("update_themes")
    if (not (php_isset(lambda : current_.response))):
        return Array()
    # end if
    update_themes_ = Array()
    for stylesheet_,data_ in current_.response.items():
        update_themes_[stylesheet_] = wp_get_theme(stylesheet_)
        update_themes_[stylesheet_].update = data_
    # end for
    return update_themes_
# end def get_theme_updates
#// 
#// @since 3.1.0
#//
def wp_theme_update_rows(*_args_):
    
    
    if (not current_user_can("update_themes")):
        return
    # end if
    themes_ = get_site_transient("update_themes")
    if (php_isset(lambda : themes_.response)) and php_is_array(themes_.response):
        themes_ = php_array_keys(themes_.response)
        for theme_ in themes_:
            add_action(str("after_theme_row_") + str(theme_), "wp_theme_update_row", 10, 2)
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
def wp_theme_update_row(theme_key_=None, theme_=None, *_args_):
    
    
    current_ = get_site_transient("update_themes")
    if (not (php_isset(lambda : current_.response[theme_key_]))):
        return False
    # end if
    response_ = current_.response[theme_key_]
    details_url_ = add_query_arg(Array({"TB_iframe": "true", "width": 1024, "height": 800}), current_.response[theme_key_]["url"])
    #// @var WP_MS_Themes_List_Table $wp_list_table
    wp_list_table_ = _get_list_table("WP_MS_Themes_List_Table")
    active_ = " active" if theme_.is_allowed("network") else ""
    php_printf("<tr class=\"plugin-update-tr%s\" id=\"%s\" data-slug=\"%s\">" + "<td colspan=\"%s\" class=\"plugin-update colspanchange\">" + "<div class=\"update-message notice inline notice-warning notice-alt\"><p>", active_, esc_attr(theme_.get_stylesheet() + "-update"), esc_attr(theme_.get_stylesheet()), wp_list_table_.get_column_count())
    if (not current_user_can("update_themes")):
        php_printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>."), theme_["Name"], esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_["Name"], response_["new_version"]))), response_["new_version"])
    elif php_empty(lambda : response_["package"]):
        php_printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>. <em>Automatic update is unavailable for this theme.</em>"), theme_["Name"], esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_["Name"], response_["new_version"]))), response_["new_version"])
    else:
        php_printf(__("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\" %6$s>update now</a>."), theme_["Name"], esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_["Name"], response_["new_version"]))), response_["new_version"], wp_nonce_url(self_admin_url("update.php?action=upgrade-theme&theme=") + theme_key_, "upgrade-theme_" + theme_key_), php_sprintf("class=\"update-link\" aria-label=\"%s\"", esc_attr(php_sprintf(__("Update %s now"), theme_["Name"]))))
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
    do_action(str("in_theme_update_message-") + str(theme_key_), theme_, response_)
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    php_print("</p></div></td></tr>")
# end def wp_theme_update_row
#// 
#// @since 2.7.0
#// 
#// @global int $upgrading
#// @return void|false
#//
def maintenance_nag(*_args_):
    
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    global upgrading_
    php_check_if_defined("upgrading_")
    nag_ = (php_isset(lambda : upgrading_))
    if (not nag_):
        failed_ = get_site_option("auto_core_update_failed")
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
        comparison_ = ">=" if (not php_empty(lambda : failed_["critical"])) else ">"
        if (php_isset(lambda : failed_["attempted"])) and php_version_compare(failed_["attempted"], wp_version_, comparison_):
            nag_ = True
        # end if
    # end if
    if (not nag_):
        return False
    # end if
    if current_user_can("update_core"):
        msg_ = php_sprintf(__("An automated WordPress update has failed to complete - <a href=\"%s\">please attempt the update again now</a>."), "update-core.php")
    else:
        msg_ = __("An automated WordPress update has failed to complete! Please notify the site administrator.")
    # end if
    php_print(str("<div class='update-nag'>") + str(msg_) + str("</div>"))
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
def wp_print_admin_notice_templates(*_args_):
    
    
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
    php_printf(__("%s plugin successfully updated."), "{{ data.successes }}")
    php_print("                     <# } else { #>\n                            ")
    #// translators: %s: Number of themes.
    php_printf(__("%s theme successfully updated."), "{{ data.successes }}")
    php_print("""                       <# } #>
    <# } else { #>
    <# if ( 'plugin' === data.type ) { #>
    """)
    #// translators: %s: Number of plugins.
    php_printf(__("%s plugins successfully updated."), "{{ data.successes }}")
    php_print("                     <# } else { #>\n                            ")
    #// translators: %s: Number of themes.
    php_printf(__("%s themes successfully updated."), "{{ data.successes }}")
    php_print("""                       <# } #>
    <# } #>
    <# } #>
    <# if ( data.errors ) { #>
    <button class=\"button-link bulk-action-errors-collapsed\" aria-expanded=\"false\">
    <# if ( 1 === data.errors ) { #>
    """)
    #// translators: %s: Number of failed updates.
    php_printf(__("%s update failed."), "{{ data.errors }}")
    php_print("                     <# } else { #>\n                            ")
    #// translators: %s: Number of failed updates.
    php_printf(__("%s updates failed."), "{{ data.errors }}")
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
def wp_print_update_row_templates(*_args_):
    
    
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
    php_printf(_x("%s was successfully deleted.", "plugin"), "<strong>{{{ data.name }}}</strong>")
    php_print("             <# } else { #>\n                    ")
    php_printf(_x("%s was successfully deleted.", "theme"), "<strong>{{{ data.name }}}</strong>")
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
def wp_recovery_mode_nag(*_args_):
    
    
    if (not wp_is_recovery_mode()):
        return
    # end if
    url_ = wp_login_url()
    url_ = add_query_arg("action", WP_Recovery_Mode.EXIT_ACTION, url_)
    url_ = wp_nonce_url(url_, WP_Recovery_Mode.EXIT_ACTION)
    php_print(" <div class=\"notice notice-info\">\n        <p>\n           ")
    php_printf(__("You are in recovery mode. This means there may be an error with a theme or plugin. To exit recovery mode, log out or use the Exit button. <a href=\"%s\">Exit Recovery Mode</a>"), esc_url(url_))
    php_print("     </p>\n  </div>\n    ")
# end def wp_recovery_mode_nag
