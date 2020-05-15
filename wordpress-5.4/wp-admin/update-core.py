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
#// Update Core administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
wp_enqueue_style("plugin-install")
wp_enqueue_script("plugin-install")
wp_enqueue_script("updates")
add_thickbox()
if is_multisite() and (not is_network_admin()):
    wp_redirect(network_admin_url("update-core.php"))
    php_exit(0)
# end if
if (not current_user_can("update_core")) and (not current_user_can("update_themes")) and (not current_user_can("update_plugins")) and (not current_user_can("update_languages")):
    wp_die(__("Sorry, you are not allowed to update this site."))
# end if
#// 
#// Lists available core updates.
#// 
#// @since 2.7.0
#// 
#// @global string $wp_local_package Locale code of the package.
#// @global wpdb   $wpdb             WordPress database abstraction object.
#// 
#// @staticvar bool $first_pass
#// 
#// @param object $update
#//
def list_core_update(update=None, *args_):
    
    global wp_local_package,wpdb
    php_check_if_defined("wp_local_package","wpdb")
    first_pass = True
    wp_version = get_bloginfo("version")
    version_string = php_sprintf("%s&ndash;<strong>%s</strong>", update.current, update.locale)
    if "en_US" == update.locale and "en_US" == get_locale():
        version_string = update.current
    elif "en_US" == update.locale and update.packages.partial and wp_version == update.partial_version:
        updates = get_core_updates()
        if updates and 1 == php_count(updates):
            #// If the only available update is a partial builds, it doesn't need a language-specific version string.
            version_string = update.current
        # end if
    # end if
    current = False
    if (not (php_isset(lambda : update.response))) or "latest" == update.response:
        current = True
    # end if
    submit = __("Update Now")
    form_action = "update-core.php?action=do-core-upgrade"
    php_version = php_phpversion()
    mysql_version = wpdb.db_version()
    show_buttons = True
    if "development" == update.response:
        message = __("You are using a development version of WordPress. You can update to the latest nightly build automatically:")
    else:
        if current:
            #// translators: %s: WordPress version.
            message = php_sprintf(__("If you need to re-install version %s, you can do so here:"), version_string)
            submit = __("Re-install Now")
            form_action = "update-core.php?action=do-core-reinstall"
        else:
            php_compat = php_version_compare(php_version, update.php_version, ">=")
            if php_file_exists(WP_CONTENT_DIR + "/db.php") and php_empty(lambda : wpdb.is_mysql):
                mysql_compat = True
            else:
                mysql_compat = php_version_compare(mysql_version, update.mysql_version, ">=")
            # end if
            version_url = php_sprintf(esc_url(__("https://wordpress.org/support/wordpress-version/version-%s/")), sanitize_title(update.current))
            php_update_message = "</p><p>" + php_sprintf(__("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
            annotation = wp_get_update_php_annotation()
            if annotation:
                php_update_message += "</p><p><em>" + annotation + "</em>"
            # end if
            if (not mysql_compat) and (not php_compat):
                message = php_sprintf(__("You cannot update because <a href=\"%1$s\">WordPress %2$s</a> requires PHP version %3$s or higher and MySQL version %4$s or higher. You are running PHP version %5$s and MySQL version %6$s."), version_url, update.current, update.php_version, update.mysql_version, php_version, mysql_version) + php_update_message
            elif (not php_compat):
                message = php_sprintf(__("You cannot update because <a href=\"%1$s\">WordPress %2$s</a> requires PHP version %3$s or higher. You are running version %4$s."), version_url, update.current, update.php_version, php_version) + php_update_message
            elif (not mysql_compat):
                message = php_sprintf(__("You cannot update because <a href=\"%1$s\">WordPress %2$s</a> requires MySQL version %3$s or higher. You are running version %4$s."), version_url, update.current, update.mysql_version, mysql_version)
            else:
                message = php_sprintf(__("You can update to <a href=\"%1$s\">WordPress %2$s</a> automatically:"), version_url, version_string)
            # end if
            if (not mysql_compat) or (not php_compat):
                show_buttons = False
            # end if
        # end if
    # end if
    php_print("<p>")
    php_print(message)
    php_print("</p>")
    php_print("<form method=\"post\" action=\"" + form_action + "\" name=\"upgrade\" class=\"upgrade\">")
    wp_nonce_field("upgrade-core")
    php_print("<p>")
    php_print("<input name=\"version\" value=\"" + esc_attr(update.current) + "\" type=\"hidden\"/>")
    php_print("<input name=\"locale\" value=\"" + esc_attr(update.locale) + "\" type=\"hidden\"/>")
    if show_buttons:
        if first_pass:
            submit_button(submit, "" if current else "primary regular", "upgrade", False)
            first_pass = False
        else:
            submit_button(submit, "", "upgrade", False)
        # end if
    # end if
    if "en_US" != update.locale:
        if (not (php_isset(lambda : update.dismissed))) or (not update.dismissed):
            submit_button(__("Hide this update"), "", "dismiss", False)
        else:
            submit_button(__("Bring back this update"), "", "undismiss", False)
        # end if
    # end if
    php_print("</p>")
    if "en_US" != update.locale and (not (php_isset(lambda : wp_local_package))) or wp_local_package != update.locale:
        php_print("<p class=\"hint\">" + __("This localized version contains both the translation and various other localization fixes.") + "</p>")
    elif "en_US" == update.locale and "en_US" != get_locale() and (not update.packages.partial) and wp_version == update.partial_version:
        #// Partial builds don't need language-specific warnings.
        php_print("<p class=\"hint\">" + php_sprintf(__("You are about to install WordPress %s <strong>in English (US).</strong> There is a chance this update will break your translation. You may prefer to wait for the localized version to be released."), update.current if "development" != update.response else "") + "</p>")
    # end if
    php_print("</form>")
# end def list_core_update
#// 
#// Display dismissed updates.
#// 
#// @since 2.7.0
#//
def dismissed_updates(*args_):
    
    dismissed = get_core_updates(Array({"dismissed": True, "available": False}))
    if dismissed:
        show_text = esc_js(__("Show hidden updates"))
        hide_text = esc_js(__("Hide hidden updates"))
        php_print("""   <script type=\"text/javascript\">
        jQuery(function( $ ) {
        $( 'dismissed-updates' ).show();
        $( '#show-dismissed' ).toggle( function() { $( this ).text( '""")
        php_print(hide_text)
        php_print("' ).attr( 'aria-expanded', 'true' ); }, function() { $( this ).text( '")
        php_print(show_text)
        php_print("""' ).attr( 'aria-expanded', 'false' ); } );
        $( '#show-dismissed' ).click( function() { $( '#dismissed-updates' ).toggle( 'fast' ); } );
        });
        </script>
        """)
        php_print("<p class=\"hide-if-no-js\"><button type=\"button\" class=\"button\" id=\"show-dismissed\" aria-expanded=\"false\">" + __("Show hidden updates") + "</button></p>")
        php_print("<ul id=\"dismissed-updates\" class=\"core-updates dismissed\">")
        for update in dismissed:
            php_print("<li>")
            list_core_update(update)
            php_print("</li>")
        # end for
        php_print("</ul>")
    # end if
# end def dismissed_updates
#// 
#// Display upgrade WordPress for downloading latest or upgrading automatically form.
#// 
#// @since 2.7.0
#// 
#// @global string $required_php_version   The required PHP version string.
#// @global string $required_mysql_version The required MySQL version string.
#//
def core_upgrade_preamble(*args_):
    
    global required_php_version,required_mysql_version
    php_check_if_defined("required_php_version","required_mysql_version")
    wp_version = get_bloginfo("version")
    updates = get_core_updates()
    if (not (php_isset(lambda : updates[0].response))) or "latest" == updates[0].response:
        php_print("<h2>")
        _e("You have the latest version of WordPress.")
        if wp_http_supports(Array("ssl")):
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
            upgrader = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
            future_minor_update = Array({"current": wp_version + ".1.next.minor", "version": wp_version + ".1.next.minor", "php_version": required_php_version, "mysql_version": required_mysql_version})
            should_auto_update = upgrader.should_update("core", future_minor_update, ABSPATH)
            if should_auto_update:
                php_print(" " + __("Future security updates will be applied automatically."))
            # end if
        # end if
        php_print("</h2>")
    # end if
    if (php_isset(lambda : updates[0].version)) and php_version_compare(updates[0].version, wp_version, ">"):
        php_print("<div class=\"notice notice-warning\"><p>")
        _e("<strong>Important:</strong> Before updating, please <a href=\"https://wordpress.org/support/article/wordpress-backups/\">back up your database and files</a>. For help with updates, visit the <a href=\"https://wordpress.org/support/article/updating-wordpress/\">Updating WordPress</a> documentation page.")
        php_print("</p></div>")
        php_print("<h2 class=\"response\">")
        _e("An updated version of WordPress is available.")
        php_print("</h2>")
    # end if
    if (php_isset(lambda : updates[0])) and "development" == updates[0].response:
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
        upgrader = php_new_class("WP_Automatic_Updater", lambda : WP_Automatic_Updater())
        if wp_http_supports("ssl") and upgrader.should_update("core", updates[0], ABSPATH):
            php_print("<div class=\"updated inline\"><p>")
            php_print("<strong>" + __("BETA TESTERS:") + "</strong> " + __("This site is set up to install updates of future beta versions automatically."))
            php_print("</p></div>")
        # end if
    # end if
    php_print("<ul class=\"core-updates\">")
    for update in updates:
        php_print("<li>")
        list_core_update(update)
        php_print("</li>")
    # end for
    php_print("</ul>")
    #// Don't show the maintenance mode notice when we are only showing a single re-install option.
    if updates and php_count(updates) > 1 or "latest" != updates[0].response:
        php_print("<p>" + __("While your site is being updated, it will be in maintenance mode. As soon as your updates are complete, your site will return to normal.") + "</p>")
    elif (not updates):
        normalized_version = php_explode("-", wp_version)
        php_print("<p>" + php_sprintf(__("<a href=\"%1$s\">Learn more about WordPress %2$s</a>."), esc_url(self_admin_url("about.php")), normalized_version) + "</p>")
    # end if
    dismissed_updates()
# end def core_upgrade_preamble
#// 
#// Display the upgrade plugins form.
#// 
#// @since 2.9.0
#//
def list_plugin_updates(*args_):
    
    wp_version = get_bloginfo("version")
    cur_wp_version = php_preg_replace("/-.*$/", "", wp_version)
    php_include_file(ABSPATH + "wp-admin/includes/plugin-install.php", once=True)
    plugins = get_plugin_updates()
    if php_empty(lambda : plugins):
        php_print("<h2>" + __("Plugins") + "</h2>")
        php_print("<p>" + __("Your plugins are all up to date.") + "</p>")
        return
    # end if
    form_action = "update-core.php?action=do-plugin-upgrade"
    core_updates = get_core_updates()
    if (not (php_isset(lambda : core_updates[0].response))) or "latest" == core_updates[0].response or "development" == core_updates[0].response or php_version_compare(core_updates[0].current, cur_wp_version, "="):
        core_update_version = False
    else:
        core_update_version = core_updates[0].current
    # end if
    php_print("<h2>")
    _e("Plugins")
    php_print("</h2>\n<p>")
    _e("The following plugins have new versions available. Check the ones you want to update and then click &#8220;Update Plugins&#8221;.")
    php_print("</p>\n<form method=\"post\" action=\"")
    php_print(esc_url(form_action))
    php_print("\" name=\"upgrade-plugins\" class=\"upgrade\">\n ")
    wp_nonce_field("upgrade-core")
    php_print("<p><input id=\"upgrade-plugins\" class=\"button\" type=\"submit\" value=\"")
    esc_attr_e("Update Plugins")
    php_print("""\" name=\"upgrade\" /></p>
    <table class=\"widefat updates-table\" id=\"update-plugins-table\">
    <thead>
    <tr>
    <td class=\"manage-column check-column\"><input type=\"checkbox\" id=\"plugins-select-all\" /></td>
    <td class=\"manage-column\"><label for=\"plugins-select-all\">""")
    _e("Select All")
    php_print("""</label></td>
    </tr>
    </thead>
    <tbody class=\"plugins\">
    """)
    for plugin_file,plugin_data in plugins:
        plugin_data = _get_plugin_data_markup_translate(plugin_file, plugin_data, False, True)
        icon = "<span class=\"dashicons dashicons-admin-plugins\"></span>"
        preferred_icons = Array("svg", "2x", "1x", "default")
        for preferred_icon in preferred_icons:
            if (not php_empty(lambda : plugin_data.update.icons[preferred_icon])):
                icon = "<img src=\"" + esc_url(plugin_data.update.icons[preferred_icon]) + "\" alt=\"\" />"
                break
            # end if
        # end for
        #// Get plugin compat for running version of WordPress.
        if (php_isset(lambda : plugin_data.update.tested)) and php_version_compare(plugin_data.update.tested, cur_wp_version, ">="):
            #// translators: %s: WordPress version.
            compat = "<br />" + php_sprintf(__("Compatibility with WordPress %s: 100%% (according to its author)"), cur_wp_version)
        else:
            #// translators: %s: WordPress version.
            compat = "<br />" + php_sprintf(__("Compatibility with WordPress %s: Unknown"), cur_wp_version)
        # end if
        #// Get plugin compat for updated version of WordPress.
        if core_update_version:
            if (php_isset(lambda : plugin_data.update.tested)) and php_version_compare(plugin_data.update.tested, core_update_version, ">="):
                #// translators: %s: WordPress version.
                compat += "<br />" + php_sprintf(__("Compatibility with WordPress %s: 100%% (according to its author)"), core_update_version)
            else:
                #// translators: %s: WordPress version.
                compat += "<br />" + php_sprintf(__("Compatibility with WordPress %s: Unknown"), core_update_version)
            # end if
        # end if
        requires_php = plugin_data.update.requires_php if (php_isset(lambda : plugin_data.update.requires_php)) else None
        compatible_php = is_php_version_compatible(requires_php)
        if (not compatible_php) and current_user_can("update_php"):
            compat += "<br>" + __("This update doesn&#8217;t work with your version of PHP.") + "&nbsp;"
            compat += php_sprintf(__("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
            annotation = wp_get_update_php_annotation()
            if annotation:
                compat += "</p><p><em>" + annotation + "</em>"
            # end if
        # end if
        #// Get the upgrade notice for the new plugin version.
        if (php_isset(lambda : plugin_data.update.upgrade_notice)):
            upgrade_notice = "<br />" + strip_tags(plugin_data.update.upgrade_notice)
        else:
            upgrade_notice = ""
        # end if
        details_url = self_admin_url("plugin-install.php?tab=plugin-information&plugin=" + plugin_data.update.slug + "&section=changelog&TB_iframe=true&width=640&height=662")
        details = php_sprintf("<a href=\"%1$s\" class=\"thickbox open-plugin-details-modal\" aria-label=\"%2$s\">%3$s</a>", esc_url(details_url), esc_attr(php_sprintf(__("View %1$s version %2$s details"), plugin_data.Name, plugin_data.update.new_version)), php_sprintf(__("View version %s details."), plugin_data.update.new_version))
        checkbox_id = "checkbox_" + php_md5(plugin_data.Name)
        php_print(" <tr>\n      <td class=\"check-column\">\n       ")
        if compatible_php:
            php_print("         <input type=\"checkbox\" name=\"checked[]\" id=\"")
            php_print(checkbox_id)
            php_print("\" value=\"")
            php_print(esc_attr(plugin_file))
            php_print("\" />\n          <label for=\"")
            php_print(checkbox_id)
            php_print("\" class=\"screen-reader-text\">\n               ")
            #// translators: %s: Plugin name.
            printf(__("Select %s"), plugin_data.Name)
            php_print("         </label>\n      ")
        # end if
        php_print("     </td>\n     <td class=\"plugin-title\"><p>\n            ")
        php_print(icon)
        php_print("         <strong>")
        php_print(plugin_data.Name)
        php_print("</strong>\n          ")
        printf(__("You have version %1$s installed. Update to %2$s."), plugin_data.Version, plugin_data.update.new_version)
        php_print(" " + details + compat + upgrade_notice)
        php_print("     </p></td>\n </tr>\n     ")
    # end for
    php_print("""   </tbody>
    <tfoot>
    <tr>
    <td class=\"manage-column check-column\"><input type=\"checkbox\" id=\"plugins-select-all-2\" /></td>
    <td class=\"manage-column\"><label for=\"plugins-select-all-2\">""")
    _e("Select All")
    php_print("""</label></td>
    </tr>
    </tfoot>
    </table>
    <p><input id=\"upgrade-plugins-2\" class=\"button\" type=\"submit\" value=\"""")
    esc_attr_e("Update Plugins")
    php_print("\" name=\"upgrade\" /></p>\n</form>\n    ")
# end def list_plugin_updates
#// 
#// Display the upgrade themes form.
#// 
#// @since 2.9.0
#//
def list_theme_updates(*args_):
    
    themes = get_theme_updates()
    if php_empty(lambda : themes):
        php_print("<h2>" + __("Themes") + "</h2>")
        php_print("<p>" + __("Your themes are all up to date.") + "</p>")
        return
    # end if
    form_action = "update-core.php?action=do-theme-upgrade"
    php_print("<h2>")
    _e("Themes")
    php_print("</h2>\n<p>")
    _e("The following themes have new versions available. Check the ones you want to update and then click &#8220;Update Themes&#8221;.")
    php_print("</p>\n<p>\n  ")
    printf(__("<strong>Please Note:</strong> Any customizations you have made to theme files will be lost. Please consider using <a href=\"%s\">child themes</a> for modifications."), __("https://developer.wordpress.org/themes/advanced-topics/child-themes/"))
    php_print("</p>\n<form method=\"post\" action=\"")
    php_print(esc_url(form_action))
    php_print("\" name=\"upgrade-themes\" class=\"upgrade\">\n  ")
    wp_nonce_field("upgrade-core")
    php_print("<p><input id=\"upgrade-themes\" class=\"button\" type=\"submit\" value=\"")
    esc_attr_e("Update Themes")
    php_print("""\" name=\"upgrade\" /></p>
    <table class=\"widefat updates-table\" id=\"update-themes-table\">
    <thead>
    <tr>
    <td class=\"manage-column check-column\"><input type=\"checkbox\" id=\"themes-select-all\" /></td>
    <td class=\"manage-column\"><label for=\"themes-select-all\">""")
    _e("Select All")
    php_print("""</label></td>
    </tr>
    </thead>
    <tbody class=\"plugins\">
    """)
    for stylesheet,theme in themes:
        checkbox_id = "checkbox_" + php_md5(theme.get("Name"))
        php_print(" <tr>\n      <td class=\"check-column\">\n           <input type=\"checkbox\" name=\"checked[]\" id=\"")
        php_print(checkbox_id)
        php_print("\" value=\"")
        php_print(esc_attr(stylesheet))
        php_print("\" />\n          <label for=\"")
        php_print(checkbox_id)
        php_print("\" class=\"screen-reader-text\">\n               ")
        #// translators: %s: Theme name.
        printf(__("Select %s"), theme.display("Name"))
        php_print("""           </label>
        </td>
        <td class=\"plugin-title\"><p>
        <img src=\"""")
        php_print(esc_url(theme.get_screenshot()))
        php_print("\" width=\"85\" height=\"64\" class=\"updates-table-screenshot\" alt=\"\" />\n           <strong>")
        php_print(theme.display("Name"))
        php_print("</strong>\n          ")
        printf(__("You have version %1$s installed. Update to %2$s."), theme.display("Version"), theme.update["new_version"])
        php_print("     </p></td>\n </tr>\n         ")
    # end for
    php_print("""   </tbody>
    <tfoot>
    <tr>
    <td class=\"manage-column check-column\"><input type=\"checkbox\" id=\"themes-select-all-2\" /></td>
    <td class=\"manage-column\"><label for=\"themes-select-all-2\">""")
    _e("Select All")
    php_print("""</label></td>
    </tr>
    </tfoot>
    </table>
    <p><input id=\"upgrade-themes-2\" class=\"button\" type=\"submit\" value=\"""")
    esc_attr_e("Update Themes")
    php_print("\" name=\"upgrade\" /></p>\n</form>\n    ")
# end def list_theme_updates
#// 
#// Display the update translations form.
#// 
#// @since 3.7.0
#//
def list_translation_updates(*args_):
    
    updates = wp_get_translation_updates()
    if (not updates):
        if "en_US" != get_locale():
            php_print("<h2>" + __("Translations") + "</h2>")
            php_print("<p>" + __("Your translations are all up to date.") + "</p>")
        # end if
        return
    # end if
    form_action = "update-core.php?action=do-translation-upgrade"
    php_print(" <h2>")
    _e("Translations")
    php_print("</h2>\n  <form method=\"post\" action=\"")
    php_print(esc_url(form_action))
    php_print("\" name=\"upgrade-translations\" class=\"upgrade\">\n        <p>")
    _e("New translations are available.")
    php_print("</p>\n       ")
    wp_nonce_field("upgrade-translations")
    php_print("     <p><input class=\"button\" type=\"submit\" value=\"")
    esc_attr_e("Update Translations")
    php_print("\" name=\"upgrade\" /></p>\n </form>\n   ")
# end def list_translation_updates
#// 
#// Upgrade WordPress core display.
#// 
#// @since 2.7.0
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param bool $reinstall
#//
def do_core_upgrade(reinstall=False, *args_):
    
    global wp_filesystem
    php_check_if_defined("wp_filesystem")
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    if reinstall:
        url = "update-core.php?action=do-core-reinstall"
    else:
        url = "update-core.php?action=do-core-upgrade"
    # end if
    url = wp_nonce_url(url, "upgrade-core")
    version = PHP_POST["version"] if (php_isset(lambda : PHP_POST["version"])) else False
    locale = PHP_POST["locale"] if (php_isset(lambda : PHP_POST["locale"])) else "en_US"
    update = find_core_update(version, locale)
    if (not update):
        return
    # end if
    #// Allow relaxed file ownership writes for User-initiated upgrades when the API specifies
    #// that it's safe to do so. This only happens when there are no new files to create.
    allow_relaxed_file_ownership = (not reinstall) and (php_isset(lambda : update.new_files)) and (not update.new_files)
    php_print(" <div class=\"wrap\">\n  <h1>")
    _e("Update WordPress")
    php_print("</h1>\n  ")
    credentials = request_filesystem_credentials(url, "", False, ABSPATH, Array("version", "locale"), allow_relaxed_file_ownership)
    if False == credentials:
        php_print("</div>")
        return
    # end if
    if (not WP_Filesystem(credentials, ABSPATH, allow_relaxed_file_ownership)):
        #// Failed to connect. Error and request again.
        request_filesystem_credentials(url, "", True, ABSPATH, Array("version", "locale"), allow_relaxed_file_ownership)
        php_print("</div>")
        return
    # end if
    if wp_filesystem.errors.has_errors():
        for message in wp_filesystem.errors.get_error_messages():
            show_message(message)
        # end for
        php_print("</div>")
        return
    # end if
    if reinstall:
        update.response = "reinstall"
    # end if
    add_filter("update_feedback", "show_message")
    upgrader = php_new_class("Core_Upgrader", lambda : Core_Upgrader())
    result = upgrader.upgrade(update, Array({"allow_relaxed_file_ownership": allow_relaxed_file_ownership}))
    if is_wp_error(result):
        show_message(result)
        if "up_to_date" != result.get_error_code() and "locked" != result.get_error_code():
            show_message(__("Installation Failed"))
        # end if
        php_print("</div>")
        return
    # end if
    show_message(__("WordPress updated successfully"))
    show_message("<span class=\"hide-if-no-js\">" + php_sprintf(__("Welcome to WordPress %1$s. You will be redirected to the About WordPress screen. If not, click <a href=\"%2$s\">here</a>."), result, esc_url(self_admin_url("about.php?updated"))) + "</span>")
    show_message("<span class=\"hide-if-js\">" + php_sprintf(__("Welcome to WordPress %1$s. <a href=\"%2$s\">Learn more</a>."), result, esc_url(self_admin_url("about.php?updated"))) + "</span>")
    php_print(" </div>\n    <script type=\"text/javascript\">\n window.location = '")
    php_print(self_admin_url("about.php?updated"))
    php_print("';\n </script>\n ")
# end def do_core_upgrade
#// 
#// Dismiss a core update.
#// 
#// @since 2.7.0
#//
def do_dismiss_core_update(*args_):
    
    version = PHP_POST["version"] if (php_isset(lambda : PHP_POST["version"])) else False
    locale = PHP_POST["locale"] if (php_isset(lambda : PHP_POST["locale"])) else "en_US"
    update = find_core_update(version, locale)
    if (not update):
        return
    # end if
    dismiss_core_update(update)
    wp_redirect(wp_nonce_url("update-core.php?action=upgrade-core", "upgrade-core"))
    php_exit(0)
# end def do_dismiss_core_update
#// 
#// Undismiss a core update.
#// 
#// @since 2.7.0
#//
def do_undismiss_core_update(*args_):
    
    version = PHP_POST["version"] if (php_isset(lambda : PHP_POST["version"])) else False
    locale = PHP_POST["locale"] if (php_isset(lambda : PHP_POST["locale"])) else "en_US"
    update = find_core_update(version, locale)
    if (not update):
        return
    # end if
    undismiss_core_update(version, locale)
    wp_redirect(wp_nonce_url("update-core.php?action=upgrade-core", "upgrade-core"))
    php_exit(0)
# end def do_undismiss_core_update
action = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else "upgrade-core"
upgrade_error = False
if "do-theme-upgrade" == action or "do-plugin-upgrade" == action and (not (php_isset(lambda : PHP_REQUEST["plugins"]))) and (not (php_isset(lambda : PHP_POST["checked"]))):
    upgrade_error = "themes" if "do-theme-upgrade" == action else "plugins"
    action = "upgrade-core"
# end if
title = __("WordPress Updates")
parent_file = "index.php"
updates_overview = "<p>" + __("On this screen, you can update to the latest version of WordPress, as well as update your themes, plugins, and translations from the WordPress.org repositories.") + "</p>"
updates_overview += "<p>" + __("If an update is available, you&#8127;ll see a notification appear in the Toolbar and navigation menu.") + " " + __("Keeping your site updated is important for security. It also makes the internet a safer place for you and your readers.") + "</p>"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": updates_overview}))
updates_howto = "<p>" + __("<strong>WordPress</strong> &mdash; Updating your WordPress installation is a simple one-click procedure: just <strong>click on the &#8220;Update Now&#8221; button</strong> when you are notified that a new version is available.") + " " + __("In most cases, WordPress will automatically apply maintenance and security updates in the background for you.") + "</p>"
updates_howto += "<p>" + __("<strong>Themes and Plugins</strong> &mdash; To update individual themes or plugins from this screen, use the checkboxes to make your selection, then <strong>click on the appropriate &#8220;Update&#8221; button</strong>. To update all of your themes or plugins at once, you can check the box at the top of the section to select all before clicking the update button.") + "</p>"
if "en_US" != get_locale():
    updates_howto += "<p>" + __("<strong>Translations</strong> &mdash; The files translating WordPress into your language are updated for you whenever any other updates occur. But if these files are out of date, you can <strong>click the &#8220;Update Translations&#8221;</strong> button.") + "</p>"
# end if
get_current_screen().add_help_tab(Array({"id": "how-to-update", "title": __("How to Update"), "content": updates_howto}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/dashboard-updates-screen/\">Documentation on Updating WordPress</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
if "upgrade-core" == action:
    #// Force a update check when requested.
    force_check = (not php_empty(lambda : PHP_REQUEST["force-check"]))
    wp_version_check(Array(), force_check)
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    php_print(" <div class=\"wrap\">\n  <h1>")
    _e("WordPress Updates")
    php_print("</h1>\n  ")
    if upgrade_error:
        php_print("<div class=\"error\"><p>")
        if "themes" == upgrade_error:
            _e("Please select one or more themes to update.")
        else:
            _e("Please select one or more plugins to update.")
        # end if
        php_print("</p></div>")
    # end if
    last_update_check = False
    current = get_site_transient("update_core")
    if current and (php_isset(lambda : current.last_checked)):
        last_update_check = current.last_checked + get_option("gmt_offset") * HOUR_IN_SECONDS
    # end if
    php_print("<p>")
    #// translators: 1: Date, 2: Time.
    printf(__("Last checked on %1$s at %2$s."), date_i18n(__("F j, Y"), last_update_check), date_i18n(__("g:i a"), last_update_check))
    php_print(" &nbsp; <a class=\"button\" href=\"" + esc_url(self_admin_url("update-core.php?force-check=1")) + "\">" + __("Check Again") + "</a>")
    php_print("</p>")
    if current_user_can("update_core"):
        core_upgrade_preamble()
    # end if
    if current_user_can("update_plugins"):
        list_plugin_updates()
    # end if
    if current_user_can("update_themes"):
        list_theme_updates()
    # end if
    if current_user_can("update_languages"):
        list_translation_updates()
    # end if
    #// 
    #// Fires after the core, plugin, and theme update tables.
    #// 
    #// @since 2.9.0
    #//
    do_action("core_upgrade_preamble")
    php_print("</div>")
    wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"totals": wp_get_update_data()}))
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
elif "do-core-upgrade" == action or "do-core-reinstall" == action:
    if (not current_user_can("update_core")):
        wp_die(__("Sorry, you are not allowed to update this site."))
    # end if
    check_admin_referer("upgrade-core")
    #// Do the (un)dismiss actions before headers, so that they can redirect.
    if (php_isset(lambda : PHP_POST["dismiss"])):
        do_dismiss_core_update()
    elif (php_isset(lambda : PHP_POST["undismiss"])):
        do_undismiss_core_update()
    # end if
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    if "do-core-reinstall" == action:
        reinstall = True
    else:
        reinstall = False
    # end if
    if (php_isset(lambda : PHP_POST["upgrade"])):
        do_core_upgrade(reinstall)
    # end if
    wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"totals": wp_get_update_data()}))
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
elif "do-plugin-upgrade" == action:
    if (not current_user_can("update_plugins")):
        wp_die(__("Sorry, you are not allowed to update this site."))
    # end if
    check_admin_referer("upgrade-core")
    if (php_isset(lambda : PHP_REQUEST["plugins"])):
        plugins = php_explode(",", PHP_REQUEST["plugins"])
    elif (php_isset(lambda : PHP_POST["checked"])):
        plugins = PHP_POST["checked"]
    else:
        wp_redirect(admin_url("update-core.php"))
        php_exit(0)
    # end if
    url = "update.php?action=update-selected&plugins=" + urlencode(php_implode(",", plugins))
    url = wp_nonce_url(url, "bulk-update-plugins")
    title = __("Update Plugins")
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    php_print("<div class=\"wrap\">")
    php_print("<h1>" + __("Update Plugins") + "</h1>")
    php_print("<iframe src=\"", url, "\" style=\"width: 100%; height: 100%; min-height: 750px;\" frameborder=\"0\" title=\"" + esc_attr__("Update progress") + "\"></iframe>")
    php_print("</div>")
    wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"totals": wp_get_update_data()}))
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
elif "do-theme-upgrade" == action:
    if (not current_user_can("update_themes")):
        wp_die(__("Sorry, you are not allowed to update this site."))
    # end if
    check_admin_referer("upgrade-core")
    if (php_isset(lambda : PHP_REQUEST["themes"])):
        themes = php_explode(",", PHP_REQUEST["themes"])
    elif (php_isset(lambda : PHP_POST["checked"])):
        themes = PHP_POST["checked"]
    else:
        wp_redirect(admin_url("update-core.php"))
        php_exit(0)
    # end if
    url = "update.php?action=update-selected-themes&themes=" + urlencode(php_implode(",", themes))
    url = wp_nonce_url(url, "bulk-update-themes")
    title = __("Update Themes")
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    php_print(" <div class=\"wrap\">\n      <h1>")
    _e("Update Themes")
    php_print("</h1>\n      <iframe src=\"")
    php_print(url)
    php_print("\" style=\"width: 100%; height: 100%; min-height: 750px;\" frameborder=\"0\" title=\"")
    esc_attr_e("Update progress")
    php_print("\"></iframe>\n   </div>\n    ")
    wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"totals": wp_get_update_data()}))
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
elif "do-translation-upgrade" == action:
    if (not current_user_can("update_languages")):
        wp_die(__("Sorry, you are not allowed to update this site."))
    # end if
    check_admin_referer("upgrade-translations")
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    url = "update-core.php?action=do-translation-upgrade"
    nonce = "upgrade-translations"
    title = __("Update Translations")
    context = WP_LANG_DIR
    upgrader = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(php_new_class("Language_Pack_Upgrader_Skin", lambda : Language_Pack_Upgrader_Skin(compact("url", "nonce", "title", "context")))))
    result = upgrader.bulk_upgrade()
    wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"totals": wp_get_update_data()}))
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
else:
    #// 
    #// Fires for each custom update action on the WordPress Updates screen.
    #// 
    #// The dynamic portion of the hook name, `$action`, refers to the
    #// passed update action. The hook fires in lieu of all available
    #// default update actions.
    #// 
    #// @since 3.2.0
    #//
    do_action(str("update-core-custom_") + str(action))
    pass
# end if
