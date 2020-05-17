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
    plugin_ = php_trim(PHP_REQUEST["plugin"]) if (php_isset(lambda : PHP_REQUEST["plugin"])) else ""
    theme_ = urldecode(PHP_REQUEST["theme"]) if (php_isset(lambda : PHP_REQUEST["theme"])) else ""
    action_ = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else ""
    if "update-selected" == action_:
        if (not current_user_can("update_plugins")):
            wp_die(__("Sorry, you are not allowed to update plugins for this site."))
        # end if
        check_admin_referer("bulk-update-plugins")
        if (php_isset(lambda : PHP_REQUEST["plugins"])):
            plugins_ = php_explode(",", stripslashes(PHP_REQUEST["plugins"]))
        elif (php_isset(lambda : PHP_POST["checked"])):
            plugins_ = PHP_POST["checked"]
        else:
            plugins_ = Array()
        # end if
        plugins_ = php_array_map("urldecode", plugins_)
        url_ = "update.php?action=update-selected&amp;plugins=" + urlencode(php_implode(",", plugins_))
        nonce_ = "bulk-update-plugins"
        wp_enqueue_script("updates")
        iframe_header()
        upgrader_ = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Bulk_Plugin_Upgrader_Skin", lambda : Bulk_Plugin_Upgrader_Skin(php_compact("nonce", "url")))))
        upgrader_.bulk_upgrade(plugins_)
        iframe_footer()
    elif "upgrade-plugin" == action_:
        if (not current_user_can("update_plugins")):
            wp_die(__("Sorry, you are not allowed to update plugins for this site."))
        # end if
        check_admin_referer("upgrade-plugin_" + plugin_)
        title_ = __("Update Plugin")
        parent_file_ = "plugins.php"
        submenu_file_ = "plugins.php"
        wp_enqueue_script("updates")
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        nonce_ = "upgrade-plugin_" + plugin_
        url_ = "update.php?action=upgrade-plugin&plugin=" + urlencode(plugin_)
        upgrader_ = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Plugin_Upgrader_Skin", lambda : Plugin_Upgrader_Skin(php_compact("title", "nonce", "url", "plugin")))))
        upgrader_.upgrade(plugin_)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "activate-plugin" == action_:
        if (not current_user_can("update_plugins")):
            wp_die(__("Sorry, you are not allowed to update plugins for this site."))
        # end if
        check_admin_referer("activate-plugin_" + plugin_)
        if (not (php_isset(lambda : PHP_REQUEST["failure"]))) and (not (php_isset(lambda : PHP_REQUEST["success"]))):
            wp_redirect(admin_url("update.php?action=activate-plugin&failure=true&plugin=" + urlencode(plugin_) + "&_wpnonce=" + PHP_REQUEST["_wpnonce"]))
            activate_plugin(plugin_, "", (not php_empty(lambda : PHP_REQUEST["networkwide"])), True)
            wp_redirect(admin_url("update.php?action=activate-plugin&success=true&plugin=" + urlencode(plugin_) + "&_wpnonce=" + PHP_REQUEST["_wpnonce"]))
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
            wp_register_plugin_realpath(WP_PLUGIN_DIR + "/" + plugin_)
            php_include_file(WP_PLUGIN_DIR + "/" + plugin_, once=False)
        # end if
        iframe_footer()
    elif "install-plugin" == action_:
        if (not current_user_can("install_plugins")):
            wp_die(__("Sorry, you are not allowed to install plugins on this site."))
        # end if
        php_include_file(ABSPATH + "wp-admin/includes/plugin-install.php", once=False)
        #// For plugins_api().
        check_admin_referer("install-plugin_" + plugin_)
        api_ = plugins_api("plugin_information", Array({"slug": plugin_, "fields": Array({"sections": False})}))
        if is_wp_error(api_):
            wp_die(api_)
        # end if
        title_ = __("Plugin Installation")
        parent_file_ = "plugins.php"
        submenu_file_ = "plugin-install.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: Plugin name and version.
        title_ = php_sprintf(__("Installing Plugin: %s"), api_.name + " " + api_.version)
        nonce_ = "install-plugin_" + plugin_
        url_ = "update.php?action=install-plugin&plugin=" + urlencode(plugin_)
        if (php_isset(lambda : PHP_REQUEST["from"])):
            url_ += "&from=" + urlencode(stripslashes(PHP_REQUEST["from"]))
        # end if
        type_ = "web"
        #// Install plugin type, From Web or an Upload.
        upgrader_ = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Plugin_Installer_Skin", lambda : Plugin_Installer_Skin(php_compact("title", "url", "nonce", "plugin", "api")))))
        upgrader_.install(api_.download_link)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "upload-plugin" == action_:
        if (not current_user_can("upload_plugins")):
            wp_die(__("Sorry, you are not allowed to install plugins on this site."))
        # end if
        check_admin_referer("plugin-upload")
        file_upload_ = php_new_class("File_Upload_Upgrader", lambda : File_Upload_Upgrader("pluginzip", "package"))
        title_ = __("Upload Plugin")
        parent_file_ = "plugins.php"
        submenu_file_ = "plugin-install.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: File name.
        title_ = php_sprintf(__("Installing Plugin from uploaded file: %s"), esc_html(php_basename(file_upload_.filename)))
        nonce_ = "plugin-upload"
        url_ = add_query_arg(Array({"package": file_upload_.id}), "update.php?action=upload-plugin")
        type_ = "upload"
        #// Install plugin type, From Web or an Upload.
        upgrader_ = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(php_new_class("Plugin_Installer_Skin", lambda : Plugin_Installer_Skin(php_compact("type", "title", "nonce", "url")))))
        result_ = upgrader_.install(file_upload_.package)
        if result_ or is_wp_error(result_):
            file_upload_.cleanup()
        # end if
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "upgrade-theme" == action_:
        if (not current_user_can("update_themes")):
            wp_die(__("Sorry, you are not allowed to update themes for this site."))
        # end if
        check_admin_referer("upgrade-theme_" + theme_)
        wp_enqueue_script("updates")
        title_ = __("Update Theme")
        parent_file_ = "themes.php"
        submenu_file_ = "themes.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        nonce_ = "upgrade-theme_" + theme_
        url_ = "update.php?action=upgrade-theme&theme=" + urlencode(theme_)
        upgrader_ = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Theme_Upgrader_Skin", lambda : Theme_Upgrader_Skin(php_compact("title", "nonce", "url", "theme")))))
        upgrader_.upgrade(theme_)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "update-selected-themes" == action_:
        if (not current_user_can("update_themes")):
            wp_die(__("Sorry, you are not allowed to update themes for this site."))
        # end if
        check_admin_referer("bulk-update-themes")
        if (php_isset(lambda : PHP_REQUEST["themes"])):
            themes_ = php_explode(",", stripslashes(PHP_REQUEST["themes"]))
        elif (php_isset(lambda : PHP_POST["checked"])):
            themes_ = PHP_POST["checked"]
        else:
            themes_ = Array()
        # end if
        themes_ = php_array_map("urldecode", themes_)
        url_ = "update.php?action=update-selected-themes&amp;themes=" + urlencode(php_implode(",", themes_))
        nonce_ = "bulk-update-themes"
        wp_enqueue_script("updates")
        iframe_header()
        upgrader_ = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Bulk_Theme_Upgrader_Skin", lambda : Bulk_Theme_Upgrader_Skin(php_compact("nonce", "url")))))
        upgrader_.bulk_upgrade(themes_)
        iframe_footer()
    elif "install-theme" == action_:
        if (not current_user_can("install_themes")):
            wp_die(__("Sorry, you are not allowed to install themes on this site."))
        # end if
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=False)
        #// For themes_api().
        check_admin_referer("install-theme_" + theme_)
        api_ = themes_api("theme_information", Array({"slug": theme_, "fields": Array({"sections": False, "tags": False})}))
        #// Save on a bit of bandwidth.
        if is_wp_error(api_):
            wp_die(api_)
        # end if
        title_ = __("Install Themes")
        parent_file_ = "themes.php"
        submenu_file_ = "themes.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: Theme name and version.
        title_ = php_sprintf(__("Installing Theme: %s"), api_.name + " " + api_.version)
        nonce_ = "install-theme_" + theme_
        url_ = "update.php?action=install-theme&theme=" + urlencode(theme_)
        type_ = "web"
        #// Install theme type, From Web or an Upload.
        upgrader_ = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Theme_Installer_Skin", lambda : Theme_Installer_Skin(php_compact("title", "url", "nonce", "plugin", "api")))))
        upgrader_.install(api_.download_link)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    elif "upload-theme" == action_:
        if (not current_user_can("upload_themes")):
            wp_die(__("Sorry, you are not allowed to install themes on this site."))
        # end if
        check_admin_referer("theme-upload")
        file_upload_ = php_new_class("File_Upload_Upgrader", lambda : File_Upload_Upgrader("themezip", "package"))
        title_ = __("Upload Theme")
        parent_file_ = "themes.php"
        submenu_file_ = "theme-install.php"
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        #// translators: %s: File name.
        title_ = php_sprintf(__("Installing Theme from uploaded file: %s"), esc_html(php_basename(file_upload_.filename)))
        nonce_ = "theme-upload"
        url_ = add_query_arg(Array({"package": file_upload_.id}), "update.php?action=upload-theme")
        type_ = "upload"
        #// Install theme type, From Web or an Upload.
        upgrader_ = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(php_new_class("Theme_Installer_Skin", lambda : Theme_Installer_Skin(php_compact("type", "title", "nonce", "url")))))
        result_ = upgrader_.install(file_upload_.package)
        if result_ or is_wp_error(result_):
            file_upload_.cleanup()
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
        do_action(str("update-custom_") + str(action_))
        pass
    # end if
# end if
