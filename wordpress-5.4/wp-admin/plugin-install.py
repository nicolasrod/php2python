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
#// Install plugin administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// TODO: Route this page via a specific iframe handler instead of the do_action below.
if (not php_defined("IFRAME_REQUEST")) and (php_isset(lambda : PHP_REQUEST["tab"])) and "plugin-information" == PHP_REQUEST["tab"]:
    php_define("IFRAME_REQUEST", True)
# end if
#// 
#// WordPress Administration Bootstrap.
#//
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("install_plugins")):
    wp_die(__("Sorry, you are not allowed to install plugins on this site."))
# end if
if is_multisite() and (not is_network_admin()):
    wp_redirect(network_admin_url("plugin-install.php"))
    php_exit(0)
# end if
wp_list_table = _get_list_table("WP_Plugin_Install_List_Table")
pagenum = wp_list_table.get_pagenum()
if (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
    location = remove_query_arg("_wp_http_referer", wp_unslash(PHP_SERVER["REQUEST_URI"]))
    if (not php_empty(lambda : PHP_REQUEST["paged"])):
        location = add_query_arg("paged", php_int(PHP_REQUEST["paged"]), location)
    # end if
    wp_redirect(location)
    php_exit(0)
# end if
wp_list_table.prepare_items()
total_pages = wp_list_table.get_pagination_arg("total_pages")
if pagenum > total_pages and total_pages > 0:
    wp_redirect(add_query_arg("paged", total_pages))
    php_exit(0)
# end if
title = __("Add Plugins")
parent_file = "plugins.php"
wp_enqueue_script("plugin-install")
if "plugin-information" != tab:
    add_thickbox()
# end if
body_id = tab
wp_enqueue_script("updates")
#// 
#// Fires before each tab on the Install Plugins screen is loaded.
#// 
#// The dynamic portion of the action hook, `$tab`, allows for targeting
#// individual tabs, for instance 'install_plugins_pre_plugin-information'.
#// 
#// @since 2.7.0
#//
do_action(str("install_plugins_pre_") + str(tab))
#// 
#// Call the pre upload action on every non-upload plugin installation screen
#// because the form is always displayed on these screens.
#//
if "upload" != tab:
    #// This action is documented in wp-admin/plugin-install.php
    do_action("install_plugins_pre_upload")
# end if
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + php_sprintf(__("Plugins hook into WordPress to extend its functionality with custom features. Plugins are developed independently from the core WordPress application by thousands of developers all over the world. All plugins in the official <a href=\"%s\">WordPress Plugin Directory</a> are compatible with the license WordPress uses."), __("https://wordpress.org/plugins/")) + "</p>" + "<p>" + __("You can find new plugins to install by searching or browsing the directory right here in your own Plugins section.") + " <span id=\"live-search-desc\" class=\"hide-if-no-js\">" + __("The search results will be updated as you type.") + "</span></p>"}))
get_current_screen().add_help_tab(Array({"id": "adding-plugins", "title": __("Adding Plugins"), "content": "<p>" + __("If you know what you&#8217;re looking for, Search is your best bet. The Search screen has options to search the WordPress Plugin Directory for a particular Term, Author, or Tag. You can also search the directory by selecting popular tags. Tags in larger type mean more plugins have been labeled with that tag.") + "</p>" + "<p>" + __("If you just want to get an idea of what&#8217;s available, you can browse Featured and Popular plugins by using the links above the plugins list. These sections rotate regularly.") + "</p>" + "<p>" + __("You can also browse a user&#8217;s favorite plugins, by using the Favorites link above the plugins list and entering their WordPress.org username.") + "</p>" + "<p>" + __("If you want to install a plugin that you&#8217;ve downloaded elsewhere, click the Upload Plugin button above the plugins list. You will be prompted to upload the .zip package, and once uploaded, you can activate the new plugin.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/plugins-add-new-screen/\">Documentation on Installing Plugins</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter plugins list"), "heading_pagination": __("Plugins list navigation"), "heading_list": __("Plugins list")}))
#// 
#// WordPress Administration Template Header.
#//
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap ")
php_print(esc_attr(str("plugin-install-tab-") + str(tab)))
php_print("\">\n<h1 class=\"wp-heading-inline\">\n")
php_print(esc_html(title))
php_print("</h1>\n\n")
if (not php_empty(lambda : tabs["upload"])) and current_user_can("upload_plugins"):
    printf(" <a href=\"%s\" class=\"upload-view-toggle page-title-action\"><span class=\"upload\">%s</span><span class=\"browse\">%s</span></a>", self_admin_url("plugin-install.php") if "upload" == tab else self_admin_url("plugin-install.php?tab=upload"), __("Upload Plugin"), __("Browse Plugins"))
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
#// 
#// Output the upload plugin form on every non-upload plugin installation screen, so it can be
#// displayed via JavaScript rather then opening up the devoted upload plugin page.
#//
if "upload" != tab:
    php_print(" <div class=\"upload-plugin-wrap\">\n        ")
    #// This action is documented in wp-admin/plugin-install.php
    do_action("install_plugins_upload")
    php_print(" </div>\n    ")
    wp_list_table.views()
    php_print("<br class=\"clear\" />")
# end if
#// 
#// Fires after the plugins list table in each tab of the Install Plugins screen.
#// 
#// The dynamic portion of the action hook, `$tab`, allows for targeting
#// individual tabs, for instance 'install_plugins_plugin-information'.
#// 
#// @since 2.7.0
#// 
#// @param int $paged The current page number of the plugins list table.
#//
do_action(str("install_plugins_") + str(tab), paged)
php_print("""
<span class=\"spinner\"></span>
</div>
""")
wp_print_request_filesystem_credentials_modal()
wp_print_admin_notice_templates()
#// 
#// WordPress Administration Template Footer.
#//
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
