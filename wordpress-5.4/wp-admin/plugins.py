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
#// Plugins administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("activate_plugins")):
    wp_die(__("Sorry, you are not allowed to manage plugins for this site."))
# end if
wp_list_table = _get_list_table("WP_Plugins_List_Table")
pagenum = wp_list_table.get_pagenum()
action = wp_list_table.current_action()
plugin = wp_unslash(PHP_REQUEST["plugin"]) if (php_isset(lambda : PHP_REQUEST["plugin"])) else ""
s = urlencode(wp_unslash(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
#// Clean up request URI from temporary args for screen options/paging uri's to work as expected.
PHP_SERVER["REQUEST_URI"] = remove_query_arg(Array("error", "deleted", "activate", "activate-multi", "deactivate", "deactivate-multi", "_error_nonce"), PHP_SERVER["REQUEST_URI"])
wp_enqueue_script("updates")
if action:
    for case in Switch(action):
        if case("activate"):
            if (not current_user_can("activate_plugin", plugin)):
                wp_die(__("Sorry, you are not allowed to activate this plugin."))
            # end if
            if is_multisite() and (not is_network_admin()) and is_network_only_plugin(plugin):
                wp_redirect(self_admin_url(str("plugins.php?plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
                php_exit(0)
            # end if
            check_admin_referer("activate-plugin_" + plugin)
            result = activate_plugin(plugin, self_admin_url("plugins.php?error=true&plugin=" + urlencode(plugin)), is_network_admin())
            if is_wp_error(result):
                if "unexpected_output" == result.get_error_code():
                    redirect = self_admin_url("plugins.php?error=true&charsout=" + php_strlen(result.get_error_data()) + "&plugin=" + urlencode(plugin) + str("&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s))
                    wp_redirect(add_query_arg("_error_nonce", wp_create_nonce("plugin-activation-error_" + plugin), redirect))
                    php_exit(0)
                else:
                    wp_die(result)
                # end if
            # end if
            if (not is_network_admin()):
                recent = get_option("recently_activated")
                recent[plugin] = None
                update_option("recently_activated", recent)
            else:
                recent = get_site_option("recently_activated")
                recent[plugin] = None
                update_site_option("recently_activated", recent)
            # end if
            if (php_isset(lambda : PHP_REQUEST["from"])) and "import" == PHP_REQUEST["from"]:
                #// Overrides the ?error=true one above and redirects to the Imports page, stripping the -importer suffix.
                wp_redirect(self_admin_url("import.php?import=" + php_str_replace("-importer", "", php_dirname(plugin))))
            elif (php_isset(lambda : PHP_REQUEST["from"])) and "press-this" == PHP_REQUEST["from"]:
                wp_redirect(self_admin_url("press-this.php"))
            else:
                #// Overrides the ?error=true one above.
                wp_redirect(self_admin_url(str("plugins.php?activate=true&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
            # end if
            php_exit(0)
        # end if
        if case("activate-selected"):
            if (not current_user_can("activate_plugins")):
                wp_die(__("Sorry, you are not allowed to activate plugins for this site."))
            # end if
            check_admin_referer("bulk-plugins")
            plugins = wp_unslash(PHP_POST["checked"]) if (php_isset(lambda : PHP_POST["checked"])) else Array()
            if is_network_admin():
                for i,plugin in plugins:
                    #// Only activate plugins which are not already network activated.
                    if is_plugin_active_for_network(plugin):
                        plugins[i] = None
                    # end if
                # end for
            else:
                for i,plugin in plugins:
                    #// Only activate plugins which are not already active and are not network-only when on Multisite.
                    if is_plugin_active(plugin) or is_multisite() and is_network_only_plugin(plugin):
                        plugins[i] = None
                    # end if
                    #// Only activate plugins which the user can activate.
                    if (not current_user_can("activate_plugin", plugin)):
                        plugins[i] = None
                    # end if
                # end for
            # end if
            if php_empty(lambda : plugins):
                wp_redirect(self_admin_url(str("plugins.php?plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
                php_exit(0)
            # end if
            activate_plugins(plugins, self_admin_url("plugins.php?error=true"), is_network_admin())
            if (not is_network_admin()):
                recent = get_option("recently_activated")
            else:
                recent = get_site_option("recently_activated")
            # end if
            for plugin in plugins:
                recent[plugin] = None
            # end for
            if (not is_network_admin()):
                update_option("recently_activated", recent)
            else:
                update_site_option("recently_activated", recent)
            # end if
            wp_redirect(self_admin_url(str("plugins.php?activate-multi=true&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
            php_exit(0)
        # end if
        if case("update-selected"):
            check_admin_referer("bulk-plugins")
            if (php_isset(lambda : PHP_REQUEST["plugins"])):
                plugins = php_explode(",", wp_unslash(PHP_REQUEST["plugins"]))
            elif (php_isset(lambda : PHP_POST["checked"])):
                plugins = wp_unslash(PHP_POST["checked"])
            else:
                plugins = Array()
            # end if
            title = __("Update Plugins")
            parent_file = "plugins.php"
            wp_enqueue_script("updates")
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print("<div class=\"wrap\">")
            php_print("<h1>" + esc_html(title) + "</h1>")
            url = self_admin_url("update.php?action=update-selected&amp;plugins=" + urlencode(join(",", plugins)))
            url = wp_nonce_url(url, "bulk-update-plugins")
            php_print(str("<iframe src='") + str(url) + str("' style='width: 100%; height:100%; min-height:850px;'></iframe>"))
            php_print("</div>")
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        if case("error_scrape"):
            if (not current_user_can("activate_plugin", plugin)):
                wp_die(__("Sorry, you are not allowed to activate this plugin."))
            # end if
            check_admin_referer("plugin-activation-error_" + plugin)
            valid = validate_plugin(plugin)
            if is_wp_error(valid):
                wp_die(valid)
            # end if
            if (not WP_DEBUG):
                php_error_reporting(E_CORE_ERROR | E_CORE_WARNING | E_COMPILE_ERROR | E_ERROR | E_WARNING | E_PARSE | E_USER_ERROR | E_USER_WARNING | E_RECOVERABLE_ERROR)
            # end if
            php_ini_set("display_errors", True)
            #// Ensure that fatal errors are displayed.
            #// Go back to "sandbox" scope so we get the same errors as before.
            plugin_sandbox_scrape(plugin)
            #// This action is documented in wp-admin/includes/plugin.php
            do_action(str("activate_") + str(plugin))
            php_exit(0)
        # end if
        if case("deactivate"):
            if (not current_user_can("deactivate_plugin", plugin)):
                wp_die(__("Sorry, you are not allowed to deactivate this plugin."))
            # end if
            check_admin_referer("deactivate-plugin_" + plugin)
            if (not is_network_admin()) and is_plugin_active_for_network(plugin):
                wp_redirect(self_admin_url(str("plugins.php?plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
                php_exit(0)
            # end if
            deactivate_plugins(plugin, False, is_network_admin())
            if (not is_network_admin()):
                update_option("recently_activated", Array({plugin: time()}) + get_option("recently_activated"))
            else:
                update_site_option("recently_activated", Array({plugin: time()}) + get_site_option("recently_activated"))
            # end if
            if php_headers_sent():
                php_print("<meta http-equiv='refresh' content='" + esc_attr(str("0;url=plugins.php?deactivate=true&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)) + "' />")
            else:
                wp_redirect(self_admin_url(str("plugins.php?deactivate=true&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
            # end if
            php_exit(0)
        # end if
        if case("deactivate-selected"):
            if (not current_user_can("deactivate_plugins")):
                wp_die(__("Sorry, you are not allowed to deactivate plugins for this site."))
            # end if
            check_admin_referer("bulk-plugins")
            plugins = wp_unslash(PHP_POST["checked"]) if (php_isset(lambda : PHP_POST["checked"])) else Array()
            #// Do not deactivate plugins which are already deactivated.
            if is_network_admin():
                plugins = php_array_filter(plugins, "is_plugin_active_for_network")
            else:
                plugins = php_array_filter(plugins, "is_plugin_active")
                plugins = php_array_diff(plugins, php_array_filter(plugins, "is_plugin_active_for_network"))
                for i,plugin in plugins:
                    #// Only deactivate plugins which the user can deactivate.
                    if (not current_user_can("deactivate_plugin", plugin)):
                        plugins[i] = None
                    # end if
                # end for
            # end if
            if php_empty(lambda : plugins):
                wp_redirect(self_admin_url(str("plugins.php?plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
                php_exit(0)
            # end if
            deactivate_plugins(plugins, False, is_network_admin())
            deactivated = Array()
            for plugin in plugins:
                deactivated[plugin] = time()
            # end for
            if (not is_network_admin()):
                update_option("recently_activated", deactivated + get_option("recently_activated"))
            else:
                update_site_option("recently_activated", deactivated + get_site_option("recently_activated"))
            # end if
            wp_redirect(self_admin_url(str("plugins.php?deactivate-multi=true&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
            php_exit(0)
        # end if
        if case("delete-selected"):
            if (not current_user_can("delete_plugins")):
                wp_die(__("Sorry, you are not allowed to delete plugins for this site."))
            # end if
            check_admin_referer("bulk-plugins")
            #// $_POST = from the plugin form; $_GET = from the FTP details screen.
            plugins = wp_unslash(PHP_REQUEST["checked"]) if (php_isset(lambda : PHP_REQUEST["checked"])) else Array()
            if php_empty(lambda : plugins):
                wp_redirect(self_admin_url(str("plugins.php?plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
                php_exit(0)
            # end if
            plugins = php_array_filter(plugins, "is_plugin_inactive")
            #// Do not allow to delete activated plugins.
            if php_empty(lambda : plugins):
                wp_redirect(self_admin_url(str("plugins.php?error=true&main=true&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
                php_exit(0)
            # end if
            #// Bail on all if any paths are invalid.
            #// validate_file() returns truthy for invalid files.
            invalid_plugin_files = php_array_filter(plugins, "validate_file")
            if invalid_plugin_files:
                wp_redirect(self_admin_url(str("plugins.php?plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
                php_exit(0)
            # end if
            php_include_file(ABSPATH + "wp-admin/update.php", once=False)
            parent_file = "plugins.php"
            if (not (php_isset(lambda : PHP_REQUEST["verify-delete"]))):
                wp_enqueue_script("jquery")
                php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
                php_print("         <div class=\"wrap\">\n              ")
                plugin_info = Array()
                have_non_network_plugins = False
                for plugin in plugins:
                    plugin_slug = php_dirname(plugin)
                    if "." == plugin_slug:
                        data = get_plugin_data(WP_PLUGIN_DIR + "/" + plugin)
                        if data:
                            plugin_info[plugin] = data
                            plugin_info[plugin]["is_uninstallable"] = is_uninstallable_plugin(plugin)
                            if (not plugin_info[plugin]["Network"]):
                                have_non_network_plugins = True
                            # end if
                        # end if
                    else:
                        #// Get plugins list from that folder.
                        folder_plugins = get_plugins("/" + plugin_slug)
                        if folder_plugins:
                            for plugin_file,data in folder_plugins:
                                plugin_info[plugin_file] = _get_plugin_data_markup_translate(plugin_file, data)
                                plugin_info[plugin_file]["is_uninstallable"] = is_uninstallable_plugin(plugin)
                                if (not plugin_info[plugin_file]["Network"]):
                                    have_non_network_plugins = True
                                # end if
                            # end for
                        # end if
                    # end if
                # end for
                plugins_to_delete = php_count(plugin_info)
                php_print("             ")
                if 1 == plugins_to_delete:
                    php_print("                 <h1>")
                    _e("Delete Plugin")
                    php_print("</h1>\n                  ")
                    if have_non_network_plugins and is_network_admin():
                        php_print("                     <div class=\"error\"><p><strong>")
                        _e("Caution:")
                        php_print("</strong> ")
                        _e("This plugin may be active on other sites in the network.")
                        php_print("</p></div>\n                 ")
                    # end if
                    php_print("                 <p>")
                    _e("You are about to remove the following plugin:")
                    php_print("</p>\n               ")
                else:
                    php_print("                 <h1>")
                    _e("Delete Plugins")
                    php_print("</h1>\n                  ")
                    if have_non_network_plugins and is_network_admin():
                        php_print("                     <div class=\"error\"><p><strong>")
                        _e("Caution:")
                        php_print("</strong> ")
                        _e("These plugins may be active on other sites in the network.")
                        php_print("</p></div>\n                 ")
                    # end if
                    php_print("                 <p>")
                    _e("You are about to remove the following plugins:")
                    php_print("</p>\n               ")
                # end if
                php_print("                 <ul class=\"ul-disc\">\n                        ")
                data_to_delete = False
                for plugin in plugin_info:
                    if plugin["is_uninstallable"]:
                        #// translators: 1: Plugin name, 2: Plugin author.
                        php_print("<li>", php_sprintf(__("%1$s by %2$s (will also <strong>delete its data</strong>)"), "<strong>" + plugin["Name"] + "</strong>", "<em>" + plugin["AuthorName"] + "</em>"), "</li>")
                        data_to_delete = True
                    else:
                        #// translators: 1: Plugin name, 2: Plugin author.
                        php_print("<li>", php_sprintf(_x("%1$s by %2$s", "plugin"), "<strong>" + plugin["Name"] + "</strong>", "<em>" + plugin["AuthorName"]) + "</em>", "</li>")
                    # end if
                # end for
                php_print("                 </ul>\n             <p>\n               ")
                if data_to_delete:
                    _e("Are you sure you want to delete these files and data?")
                else:
                    _e("Are you sure you want to delete these files?")
                # end if
                php_print("             </p>\n              <form method=\"post\" action=\"")
                php_print(esc_url(PHP_SERVER["REQUEST_URI"]))
                php_print("""\" style=\"display:inline;\">
                <input type=\"hidden\" name=\"verify-delete\" value=\"1\" />
                <input type=\"hidden\" name=\"action\" value=\"delete-selected\" />
                """)
                for plugin in plugins:
                    php_print("<input type=\"hidden\" name=\"checked[]\" value=\"" + esc_attr(plugin) + "\" />")
                # end for
                php_print("                 ")
                wp_nonce_field("bulk-plugins")
                php_print("                 ")
                submit_button(__("Yes, delete these files and data") if data_to_delete else __("Yes, delete these files"), "", "submit", False)
                php_print("             </form>\n               ")
                referer = wp_get_referer()
                php_print("             <form method=\"post\" action=\"")
                php_print(esc_url(referer) if referer else "")
                php_print("\" style=\"display:inline;\">\n                  ")
                submit_button(__("No, return me to the plugin list"), "", "submit", False)
                php_print("             </form>\n           </div>\n                ")
                php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
                php_exit(0)
            else:
                plugins_to_delete = php_count(plugins)
            # end if
            #// End if verify-delete.
            delete_result = delete_plugins(plugins)
            #// Store the result in a cache rather than a URL param due to object type & length.
            set_transient("plugins_delete_result_" + user_ID, delete_result)
            wp_redirect(self_admin_url(str("plugins.php?deleted=") + str(plugins_to_delete) + str("&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
            php_exit(0)
        # end if
        if case("clear-recent-list"):
            if (not is_network_admin()):
                update_option("recently_activated", Array())
            else:
                update_site_option("recently_activated", Array())
            # end if
            break
        # end if
        if case("resume"):
            if is_multisite():
                sys.exit(-1)
            # end if
            if (not current_user_can("resume_plugin", plugin)):
                wp_die(__("Sorry, you are not allowed to resume this plugin."))
            # end if
            check_admin_referer("resume-plugin_" + plugin)
            result = resume_plugin(plugin, self_admin_url(str("plugins.php?error=resuming&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
            if is_wp_error(result):
                wp_die(result)
            # end if
            wp_redirect(self_admin_url(str("plugins.php?resume=true&plugin_status=") + str(status) + str("&paged=") + str(page) + str("&s=") + str(s)))
            php_exit(0)
        # end if
        if case():
            if (php_isset(lambda : PHP_POST["checked"])):
                check_admin_referer("bulk-plugins")
                screen = get_current_screen().id
                sendback = wp_get_referer()
                plugins = wp_unslash(PHP_POST["checked"]) if (php_isset(lambda : PHP_POST["checked"])) else Array()
                #// This action is documented in wp-admin/edit.php
                sendback = apply_filters(str("handle_bulk_actions-") + str(screen), sendback, action, plugins)
                #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
                wp_safe_redirect(sendback)
                php_exit(0)
            # end if
            break
        # end if
    # end for
# end if
wp_list_table.prepare_items()
wp_enqueue_script("plugin-install")
add_thickbox()
add_screen_option("per_page", Array({"default": 999}))
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Plugins extend and expand the functionality of WordPress. Once a plugin is installed, you may activate it or deactivate it here.") + "</p>" + "<p>" + __("The search for installed plugins will search for terms in their name, description, or author.") + " <span id=\"live-search-desc\" class=\"hide-if-no-js\">" + __("The search results will be updated as you type.") + "</span></p>" + "<p>" + php_sprintf(__("If you would like to see more plugins to choose from, click on the &#8220;Add New&#8221; button and you will be able to browse or search for additional plugins from the <a href=\"%s\">WordPress Plugin Directory</a>. Plugins in the WordPress Plugin Directory are designed and developed by third parties, and are compatible with the license WordPress uses. Oh, and they&#8217;re free!"), __("https://wordpress.org/plugins/")) + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "compatibility-problems", "title": __("Troubleshooting"), "content": "<p>" + __("Most of the time, plugins play nicely with the core of WordPress and with other plugins. Sometimes, though, a plugin&#8217;s code will get in the way of another plugin, causing compatibility issues. If your site starts doing strange things, this may be the problem. Try deactivating all your plugins and re-activating them in various combinations until you isolate which one(s) caused the issue.") + "</p>" + "<p>" + php_sprintf(__("If something goes wrong with a plugin and you can&#8217;t use WordPress, delete or rename that file in the %s directory and it will be automatically deactivated."), "<code>" + WP_PLUGIN_DIR + "</code>") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/managing-plugins/\">Documentation on Managing Plugins</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter plugins list"), "heading_pagination": __("Plugins list navigation"), "heading_list": __("Plugins list")}))
title = __("Plugins")
parent_file = "plugins.php"
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
invalid = validate_active_plugins()
if (not php_empty(lambda : invalid)):
    for plugin_file,error in invalid:
        php_print("<div id=\"message\" class=\"error\"><p>")
        printf(__("The plugin %1$s has been deactivated due to an error: %2$s"), "<code>" + esc_html(plugin_file) + "</code>", error.get_error_message())
        php_print("</p></div>")
    # end for
# end if
php_print("\n")
if (php_isset(lambda : PHP_REQUEST["error"])):
    if (php_isset(lambda : PHP_REQUEST["main"])):
        errmsg = __("You cannot delete a plugin while it is active on the main site.")
    elif (php_isset(lambda : PHP_REQUEST["charsout"])):
        errmsg = php_sprintf(_n("The plugin generated %d character of <strong>unexpected output</strong> during activation.", "The plugin generated %d characters of <strong>unexpected output</strong> during activation.", PHP_REQUEST["charsout"]), PHP_REQUEST["charsout"])
        errmsg += " " + __("If you notice &#8220;headers already sent&#8221; messages, problems with syndication feeds or other issues, try deactivating or removing this plugin.")
    elif "resuming" == PHP_REQUEST["error"]:
        errmsg = __("Plugin could not be resumed because it triggered a <strong>fatal error</strong>.")
    else:
        errmsg = __("Plugin could not be activated because it triggered a <strong>fatal error</strong>.")
    # end if
    php_print(" <div id=\"message\" class=\"error\"><p>")
    php_print(errmsg)
    php_print("</p>\n   ")
    if (not (php_isset(lambda : PHP_REQUEST["main"]))) and (not (php_isset(lambda : PHP_REQUEST["charsout"]))) and wp_verify_nonce(PHP_REQUEST["_error_nonce"], "plugin-activation-error_" + plugin):
        iframe_url = add_query_arg(Array({"action": "error_scrape", "plugin": urlencode(plugin), "_wpnonce": urlencode(PHP_REQUEST["_error_nonce"])}), admin_url("plugins.php"))
        php_print(" <iframe style=\"border:0\" width=\"100%\" height=\"70px\" src=\"")
        php_print(esc_url(iframe_url))
        php_print("\"></iframe>\n       ")
    # end if
    php_print(" </div>\n    ")
elif (php_isset(lambda : PHP_REQUEST["deleted"])):
    delete_result = get_transient("plugins_delete_result_" + user_ID)
    #// Delete it once we're done.
    delete_transient("plugins_delete_result_" + user_ID)
    if is_wp_error(delete_result):
        php_print("     <div id=\"message\" class=\"error notice is-dismissible\">\n            <p>\n               ")
        printf(__("Plugin could not be deleted due to an error: %s"), delete_result.get_error_message())
        php_print("         </p>\n      </div>\n        ")
    else:
        php_print("     <div id=\"message\" class=\"updated notice is-dismissible\">\n          <p>\n               ")
        if 1 == int(PHP_REQUEST["deleted"]):
            _e("The selected plugin has been deleted.")
        else:
            _e("The selected plugins have been deleted.")
        # end if
        php_print("         </p>\n      </div>\n        ")
    # end if
elif (php_isset(lambda : PHP_REQUEST["activate"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("Plugin activated.")
    php_print("</p></div>\n")
elif (php_isset(lambda : PHP_REQUEST["activate-multi"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("Selected plugins activated.")
    php_print("</p></div>\n")
elif (php_isset(lambda : PHP_REQUEST["deactivate"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("Plugin deactivated.")
    php_print("</p></div>\n")
elif (php_isset(lambda : PHP_REQUEST["deactivate-multi"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("Selected plugins deactivated.")
    php_print("</p></div>\n")
elif "update-selected" == action:
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("All selected plugins are up to date.")
    php_print("</p></div>\n")
elif (php_isset(lambda : PHP_REQUEST["resume"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("Plugin resumed.")
    php_print("</p></div>\n")
# end if
php_print("""
<div class=\"wrap\">
<h1 class=\"wp-heading-inline\">
""")
php_print(esc_html(title))
php_print("</h1>\n\n")
if (not is_multisite()) or is_network_admin() and current_user_can("install_plugins"):
    php_print(" <a href=\"")
    php_print(self_admin_url("plugin-install.php"))
    php_print("\" class=\"page-title-action\">")
    php_print(esc_html_x("Add New", "plugin"))
    php_print("</a>\n   ")
# end if
if php_strlen(s):
    #// translators: %s: Search query.
    printf("<span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", esc_html(urldecode(s)))
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
#// 
#// Fires before the plugins list table is rendered.
#// 
#// This hook also fires before the plugins list table is rendered in the Network Admin.
#// 
#// Please note: The 'active' portion of the hook name does not refer to whether the current
#// view is for active plugins, but rather all plugins actively-installed.
#// 
#// @since 3.0.0
#// 
#// @param array[] $plugins_all An array of arrays containing information on all installed plugins.
#//
do_action("pre_current_active_plugins", plugins["all"])
php_print("\n")
wp_list_table.views()
php_print("\n<form class=\"search-form search-plugins\" method=\"get\">\n")
wp_list_table.search_box(__("Search Installed Plugins"), "plugin")
php_print("""</form>
<form method=\"post\" id=\"bulk-action-form\">
<input type=\"hidden\" name=\"plugin_status\" value=\"""")
php_print(esc_attr(status))
php_print("\" />\n<input type=\"hidden\" name=\"paged\" value=\"")
php_print(esc_attr(page))
php_print("\" />\n\n")
wp_list_table.display()
php_print("""</form>
<span class=\"spinner\"></span>
</div>
""")
wp_print_request_filesystem_credentials_modal()
wp_print_admin_notice_templates()
wp_print_update_row_templates()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
