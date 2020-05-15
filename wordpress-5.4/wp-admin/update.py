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
#// Update/Install Plugin/Theme administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#//
if (not php_defined("IFRAME_REQUEST")) and (php_isset(lambda : PHP_REQUEST["action"])) and php_in_array(PHP_REQUEST["action"], Array("update-selected", "activate-plugin", "update-selected-themes")):
    php_define("IFRAME_REQUEST", True)
# end if
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
if (php_isset(lambda : PHP_REQUEST["action"])):
    plugin = php_trim(PHP_REQUEST["plugin"]) if (php_isset(lambda : PHP_REQUEST["plugin"])) else ""
    theme = urldecode(PHP_REQUEST["theme"]) if (php_isset(lambda : PHP_REQUEST["theme"])) else ""
    action = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else ""
    if "update-selected" == action:
        if (not current_user_can("update_plugins")):
            wp_die(__("Sorry, you are not allowed to update plugins for this site."))
        # end if
        check_admin_referer("bulk-update-plugins")
        if (php_isset(lambda : PHP_REQUEST["plugins"])):
            plugins = php_explode(",", stripslashes(PHP_REQUEST["plugins"]))
        elif (php_isset(lambda : PHP_POST["checked"])):
            plugins = PHP_POST["checked"]
        else:
            plugins = Array()
        # end if
        plugins = php_array_map("urldecode", plugins)
        url = "update.php?action=update-selected&amp;plugins=" + urlencode(php_implode(",", plugins))
        nonce = "bulk-update-plugins"
        wp_enqueue_script("updates")
        iframe_header()
        upgrader = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Bulk_Plugin_Upgrader_Skin", lambda : Bulk_Plugin_Upgrader_Skin(compact("nonce", "url")))))
        upgrader.bulk_upgrade(plugins)
        iframe_footer()
    elif "upgrade-plugin" == action:
        if (not current_user_can("update_plugins")):
            wp_die(__("Sorry, you are not allowed to update plugins for this site."))
        # end if
        check_admin_referer("upgrade-plugin_" + plugin)
        title = __("Update Plugin")
        parent_file = "plugins.php"
        submenu_file = "plugins.php"
        wp_enqueue_script("updates")
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        nonce = "upgrade-plugin_" + plugin
        url = "update.php?action=upgrade-plugin&plugin=" + urlencode(plugin)
        upgrader = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Plugin_Upgrader_Skin", lambda : Plugin_Upgrader_Skin(compact("title", "nonce", "url", "plugin")))))
        upgrader.upgrade(plugin)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "activate-plugin" == action:
        if (not current_user_can("update_plugins")):
            wp_die(__("Sorry, you are not allowed to update plugins for this site."))
        # end if
        check_admin_referer("activate-plugin_" + plugin)
        if (not (php_isset(lambda : PHP_REQUEST["failure"]))) and (not (php_isset(lambda : PHP_REQUEST["success"]))):
            wp_redirect(admin_url("update.php?action=activate-plugin&failure=true&plugin=" + urlencode(plugin) + "&_wpnonce=" + PHP_REQUEST["_wpnonce"]))
            activate_plugin(plugin, "", (not php_empty(lambda : PHP_REQUEST["networkwide"])), True)
            wp_redirect(admin_url("update.php?action=activate-plugin&success=true&plugin=" + urlencode(plugin) + "&_wpnonce=" + PHP_REQUEST["_wpnonce"]))
            php_exit(0)
        # end if
        iframe_header(__("Plugin Reactivation"), True)
        if (php_isset(lambda : PHP_REQUEST["success"])):
            php_print("<p>" + __("Plugin reactivated successfully.") + "</p>")
        # end if
        if (php_isset(lambda : PHP_REQUEST["failure"])):
            php_print("<p>" + __("Plugin failed to reactivate due to a fatal error.") + "</p>")
            php_error_reporting(E_CORE_ERROR | E_CORE_WARNING | E_COMPILE_ERROR | E_ERROR | E_WARNING | E_PARSE | E_USER_ERROR | E_USER_WARNING | E_RECOVERABLE_ERROR)
            php_ini_set("display_errors", True)
            #// Ensure that fatal errors are displayed.
            wp_register_plugin_realpath(WP_PLUGIN_DIR + "/" + plugin)
            php_include_file(WP_PLUGIN_DIR + "/" + plugin, once=False)
        # end if
        iframe_footer()
    elif "install-plugin" == action:
        if (not current_user_can("install_plugins")):
            wp_die(__("Sorry, you are not allowed to install plugins on this site."))
        # end if
        php_include_file(ABSPATH + "wp-admin/includes/plugin-install.php", once=False)
        #// For plugins_api().
        check_admin_referer("install-plugin_" + plugin)
        api = plugins_api("plugin_information", Array({"slug": plugin, "fields": Array({"sections": False})}))
        if is_wp_error(api):
            wp_die(api)
        # end if
        title = __("Plugin Installation")
        parent_file = "plugins.php"
        submenu_file = "plugin-install.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: Plugin name and version.
        title = php_sprintf(__("Installing Plugin: %s"), api.name + " " + api.version)
        nonce = "install-plugin_" + plugin
        url = "update.php?action=install-plugin&plugin=" + urlencode(plugin)
        if (php_isset(lambda : PHP_REQUEST["from"])):
            url += "&from=" + urlencode(stripslashes(PHP_REQUEST["from"]))
        # end if
        type = "web"
        #// Install plugin type, From Web or an Upload.
        upgrader = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Plugin_Installer_Skin", lambda : Plugin_Installer_Skin(compact("title", "url", "nonce", "plugin", "api")))))
        upgrader.install(api.download_link)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "upload-plugin" == action:
        if (not current_user_can("upload_plugins")):
            wp_die(__("Sorry, you are not allowed to install plugins on this site."))
        # end if
        check_admin_referer("plugin-upload")
        file_upload = php_new_class("File_Upload_Upgrader", lambda : File_Upload_Upgrader("pluginzip", "package"))
        title = __("Upload Plugin")
        parent_file = "plugins.php"
        submenu_file = "plugin-install.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: File name.
        title = php_sprintf(__("Installing Plugin from uploaded file: %s"), esc_html(php_basename(file_upload.filename)))
        nonce = "plugin-upload"
        url = add_query_arg(Array({"package": file_upload.id}), "update.php?action=upload-plugin")
        type = "upload"
        #// Install plugin type, From Web or an Upload.
        upgrader = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Plugin_Installer_Skin", lambda : Plugin_Installer_Skin(compact("type", "title", "nonce", "url")))))
        result = upgrader.install(file_upload.package)
        if result or is_wp_error(result):
            file_upload.cleanup()
        # end if
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "upgrade-theme" == action:
        if (not current_user_can("update_themes")):
            wp_die(__("Sorry, you are not allowed to update themes for this site."))
        # end if
        check_admin_referer("upgrade-theme_" + theme)
        wp_enqueue_script("updates")
        title = __("Update Theme")
        parent_file = "themes.php"
        submenu_file = "themes.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        nonce = "upgrade-theme_" + theme
        url = "update.php?action=upgrade-theme&theme=" + urlencode(theme)
        upgrader = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Theme_Upgrader_Skin", lambda : Theme_Upgrader_Skin(compact("title", "nonce", "url", "theme")))))
        upgrader.upgrade(theme)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "update-selected-themes" == action:
        if (not current_user_can("update_themes")):
            wp_die(__("Sorry, you are not allowed to update themes for this site."))
        # end if
        check_admin_referer("bulk-update-themes")
        if (php_isset(lambda : PHP_REQUEST["themes"])):
            themes = php_explode(",", stripslashes(PHP_REQUEST["themes"]))
        elif (php_isset(lambda : PHP_POST["checked"])):
            themes = PHP_POST["checked"]
        else:
            themes = Array()
        # end if
        themes = php_array_map("urldecode", themes)
        url = "update.php?action=update-selected-themes&amp;themes=" + urlencode(php_implode(",", themes))
        nonce = "bulk-update-themes"
        wp_enqueue_script("updates")
        iframe_header()
        upgrader = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Bulk_Theme_Upgrader_Skin", lambda : Bulk_Theme_Upgrader_Skin(compact("nonce", "url")))))
        upgrader.bulk_upgrade(themes)
        iframe_footer()
    elif "install-theme" == action:
        if (not current_user_can("install_themes")):
            wp_die(__("Sorry, you are not allowed to install themes on this site."))
        # end if
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=False)
        #// For themes_api().
        check_admin_referer("install-theme_" + theme)
        api = themes_api("theme_information", Array({"slug": theme, "fields": Array({"sections": False, "tags": False})}))
        #// Save on a bit of bandwidth.
        if is_wp_error(api):
            wp_die(api)
        # end if
        title = __("Install Themes")
        parent_file = "themes.php"
        submenu_file = "themes.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: Theme name and version.
        title = php_sprintf(__("Installing Theme: %s"), api.name + " " + api.version)
        nonce = "install-theme_" + theme
        url = "update.php?action=install-theme&theme=" + urlencode(theme)
        type = "web"
        #// Install theme type, From Web or an Upload.
        upgrader = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Theme_Installer_Skin", lambda : Theme_Installer_Skin(compact("title", "url", "nonce", "plugin", "api")))))
        upgrader.install(api.download_link)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "upload-theme" == action:
        if (not current_user_can("upload_themes")):
            wp_die(__("Sorry, you are not allowed to install themes on this site."))
        # end if
        check_admin_referer("theme-upload")
        file_upload = php_new_class("File_Upload_Upgrader", lambda : File_Upload_Upgrader("themezip", "package"))
        title = __("Upload Theme")
        parent_file = "themes.php"
        submenu_file = "theme-install.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: File name.
        title = php_sprintf(__("Installing Theme from uploaded file: %s"), esc_html(php_basename(file_upload.filename)))
        nonce = "theme-upload"
        url = add_query_arg(Array({"package": file_upload.id}), "update.php?action=upload-theme")
        type = "upload"
        #// Install theme type, From Web or an Upload.
        upgrader = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Theme_Installer_Skin", lambda : Theme_Installer_Skin(compact("type", "title", "nonce", "url")))))
        result = upgrader.install(file_upload.package)
        if result or is_wp_error(result):
            file_upload.cleanup()
        # end if
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    else:
        #// 
        #// Fires when a custom plugin or theme update request is received.
        #// 
        #// The dynamic portion of the hook name, `$action`, refers to the action
        #// provided in the request for wp-admin/update.php. Can be used to
        #// provide custom update functionality for themes and plugins.
        #// 
        #// @since 2.8.0
        #//
        do_action(str("update-custom_") + str(action))
        pass
    # end if
# end if
