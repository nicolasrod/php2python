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
#// Multisite themes administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.1.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_network_themes")):
    wp_die(__("Sorry, you are not allowed to manage network themes."))
# end if
wp_list_table = _get_list_table("WP_MS_Themes_List_Table")
pagenum = wp_list_table.get_pagenum()
action = wp_list_table.current_action()
s = PHP_REQUEST["s"] if (php_isset(lambda : PHP_REQUEST["s"])) else ""
#// Clean up request URI from temporary args for screen options/paging uri's to work as expected.
temp_args = Array("enabled", "disabled", "deleted", "error")
PHP_SERVER["REQUEST_URI"] = remove_query_arg(temp_args, PHP_SERVER["REQUEST_URI"])
referer = remove_query_arg(temp_args, wp_get_referer())
if action:
    for case in Switch(action):
        if case("enable"):
            check_admin_referer("enable-theme_" + PHP_REQUEST["theme"])
            WP_Theme.network_enable_theme(PHP_REQUEST["theme"])
            if False == php_strpos(referer, "/network/themes.php"):
                wp_redirect(network_admin_url("themes.php?enabled=1"))
            else:
                wp_safe_redirect(add_query_arg("enabled", 1, referer))
            # end if
            php_exit(0)
        # end if
        if case("disable"):
            check_admin_referer("disable-theme_" + PHP_REQUEST["theme"])
            WP_Theme.network_disable_theme(PHP_REQUEST["theme"])
            wp_safe_redirect(add_query_arg("disabled", "1", referer))
            php_exit(0)
        # end if
        if case("enable-selected"):
            check_admin_referer("bulk-themes")
            themes = PHP_POST["checked"] if (php_isset(lambda : PHP_POST["checked"])) else Array()
            if php_empty(lambda : themes):
                wp_safe_redirect(add_query_arg("error", "none", referer))
                php_exit(0)
            # end if
            WP_Theme.network_enable_theme(themes)
            wp_safe_redirect(add_query_arg("enabled", php_count(themes), referer))
            php_exit(0)
        # end if
        if case("disable-selected"):
            check_admin_referer("bulk-themes")
            themes = PHP_POST["checked"] if (php_isset(lambda : PHP_POST["checked"])) else Array()
            if php_empty(lambda : themes):
                wp_safe_redirect(add_query_arg("error", "none", referer))
                php_exit(0)
            # end if
            WP_Theme.network_disable_theme(themes)
            wp_safe_redirect(add_query_arg("disabled", php_count(themes), referer))
            php_exit(0)
        # end if
        if case("update-selected"):
            check_admin_referer("bulk-themes")
            if (php_isset(lambda : PHP_REQUEST["themes"])):
                themes = php_explode(",", PHP_REQUEST["themes"])
            elif (php_isset(lambda : PHP_POST["checked"])):
                themes = PHP_POST["checked"]
            else:
                themes = Array()
            # end if
            title = __("Update Themes")
            parent_file = "themes.php"
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print("<div class=\"wrap\">")
            php_print("<h1>" + esc_html(title) + "</h1>")
            url = self_admin_url("update.php?action=update-selected-themes&amp;themes=" + urlencode(join(",", themes)))
            url = wp_nonce_url(url, "bulk-update-themes")
            php_print(str("<iframe src='") + str(url) + str("' style='width: 100%; height:100%; min-height:850px;'></iframe>"))
            php_print("</div>")
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        if case("delete-selected"):
            if (not current_user_can("delete_themes")):
                wp_die(__("Sorry, you are not allowed to delete themes for this site."))
            # end if
            check_admin_referer("bulk-themes")
            themes = PHP_REQUEST["checked"] if (php_isset(lambda : PHP_REQUEST["checked"])) else Array()
            if php_empty(lambda : themes):
                wp_safe_redirect(add_query_arg("error", "none", referer))
                php_exit(0)
            # end if
            themes = php_array_diff(themes, Array(get_option("stylesheet"), get_option("template")))
            if php_empty(lambda : themes):
                wp_safe_redirect(add_query_arg("error", "main", referer))
                php_exit(0)
            # end if
            theme_info = Array()
            for key,theme in themes:
                theme_info[theme] = wp_get_theme(theme)
            # end for
            php_include_file(ABSPATH + "wp-admin/update.php", once=False)
            parent_file = "themes.php"
            if (not (php_isset(lambda : PHP_REQUEST["verify-delete"]))):
                wp_enqueue_script("jquery")
                php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
                themes_to_delete = php_count(themes)
                php_print("         <div class=\"wrap\">\n              ")
                if 1 == themes_to_delete:
                    php_print("                 <h1>")
                    _e("Delete Theme")
                    php_print("</h1>\n                  <div class=\"error\"><p><strong>")
                    _e("Caution:")
                    php_print("</strong> ")
                    _e("This theme may be active on other sites in the network.")
                    php_print("</p></div>\n                 <p>")
                    _e("You are about to remove the following theme:")
                    php_print("</p>\n               ")
                else:
                    php_print("                 <h1>")
                    _e("Delete Themes")
                    php_print("</h1>\n                  <div class=\"error\"><p><strong>")
                    _e("Caution:")
                    php_print("</strong> ")
                    _e("These themes may be active on other sites in the network.")
                    php_print("</p></div>\n                 <p>")
                    _e("You are about to remove the following themes:")
                    php_print("</p>\n               ")
                # end if
                php_print("                 <ul class=\"ul-disc\">\n                    ")
                for theme in theme_info:
                    php_print("<li>" + php_sprintf(_x("%1$s by %2$s", "theme"), "<strong>" + theme.display("Name") + "</strong>", "<em>" + theme.display("Author") + "</em>") + "</li>")
                # end for
                php_print("                 </ul>\n             ")
                if 1 == themes_to_delete:
                    php_print("                 <p>")
                    _e("Are you sure you want to delete this theme?")
                    php_print("</p>\n               ")
                else:
                    php_print("                 <p>")
                    _e("Are you sure you want to delete these themes?")
                    php_print("</p>\n               ")
                # end if
                php_print("             <form method=\"post\" action=\"")
                php_print(esc_url(PHP_SERVER["REQUEST_URI"]))
                php_print("""\" style=\"display:inline;\">
                <input type=\"hidden\" name=\"verify-delete\" value=\"1\" />
                <input type=\"hidden\" name=\"action\" value=\"delete-selected\" />
                """)
                for theme in themes:
                    php_print("<input type=\"hidden\" name=\"checked[]\" value=\"" + esc_attr(theme) + "\" />")
                # end for
                wp_nonce_field("bulk-themes")
                if 1 == themes_to_delete:
                    submit_button(__("Yes, delete this theme"), "", "submit", False)
                else:
                    submit_button(__("Yes, delete these themes"), "", "submit", False)
                # end if
                php_print("             </form>\n               ")
                referer = wp_get_referer()
                php_print("             <form method=\"post\" action=\"")
                php_print(esc_url(referer) if referer else "")
                php_print("\" style=\"display:inline;\">\n                  ")
                submit_button(__("No, return me to the theme list"), "", "submit", False)
                php_print("             </form>\n           </div>\n                ")
                php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
                php_exit(0)
            # end if
            #// End if verify-delete.
            for theme in themes:
                delete_result = delete_theme(theme, esc_url(add_query_arg(Array({"verify-delete": 1, "action": "delete-selected", "checked": PHP_REQUEST["checked"], "_wpnonce": PHP_REQUEST["_wpnonce"]}), network_admin_url("themes.php"))))
            # end for
            paged = PHP_REQUEST["paged"] if PHP_REQUEST["paged"] else 1
            wp_redirect(add_query_arg(Array({"deleted": php_count(themes), "paged": paged, "s": s}), network_admin_url("themes.php")))
            php_exit(0)
        # end if
        if case():
            themes = PHP_POST["checked"] if (php_isset(lambda : PHP_POST["checked"])) else Array()
            if php_empty(lambda : themes):
                wp_safe_redirect(add_query_arg("error", "none", referer))
                php_exit(0)
            # end if
            check_admin_referer("bulk-themes")
            #// This action is documented in wp-admin/network/site-themes.php
            referer = apply_filters("handle_network_bulk_actions-" + get_current_screen().id, referer, action, themes)
            #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
            wp_safe_redirect(referer)
            php_exit(0)
        # end if
    # end for
# end if
wp_list_table.prepare_items()
add_thickbox()
add_screen_option("per_page")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen enables and disables the inclusion of themes available to choose in the Appearance menu for each site. It does not activate or deactivate which theme a site is currently using.") + "</p>" + "<p>" + __("If the network admin disables a theme that is in use, it can still remain selected on that site. If another theme is chosen, the disabled theme will not appear in the site&#8217;s Appearance > Themes screen.") + "</p>" + "<p>" + __("Themes can be enabled on a site by site basis by the network admin on the Edit Site screen (which has a Themes tab); get there via the Edit action link on the All Sites screen. Only network admins are able to install or edit themes.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Network_Admin_Themes_Screen\">Documentation on Network Themes</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter themes list"), "heading_pagination": __("Themes list navigation"), "heading_list": __("Themes list")}))
title = __("Themes")
parent_file = "themes.php"
wp_enqueue_script("updates")
wp_enqueue_script("theme-preview")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 class=\"wp-heading-inline\">")
php_print(esc_html(title))
php_print("</h1>\n\n")
if current_user_can("install_themes"):
    php_print(" <a href=\"theme-install.php\" class=\"page-title-action\">")
    php_print(esc_html_x("Add New", "theme"))
    php_print("</a>\n")
# end if
php_print("\n")
if (php_isset(lambda : PHP_REQUEST["s"])) and php_strlen(PHP_REQUEST["s"]):
    #// translators: %s: Search query.
    printf("<span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", esc_html(s))
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
if (php_isset(lambda : PHP_REQUEST["enabled"])):
    enabled = absint(PHP_REQUEST["enabled"])
    if 1 == enabled:
        message = __("Theme enabled.")
    else:
        #// translators: %s: Number of themes.
        message = _n("%s theme enabled.", "%s themes enabled.", enabled)
    # end if
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + php_sprintf(message, number_format_i18n(enabled)) + "</p></div>")
elif (php_isset(lambda : PHP_REQUEST["disabled"])):
    disabled = absint(PHP_REQUEST["disabled"])
    if 1 == disabled:
        message = __("Theme disabled.")
    else:
        #// translators: %s: Number of themes.
        message = _n("%s theme disabled.", "%s themes disabled.", disabled)
    # end if
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + php_sprintf(message, number_format_i18n(disabled)) + "</p></div>")
elif (php_isset(lambda : PHP_REQUEST["deleted"])):
    deleted = absint(PHP_REQUEST["deleted"])
    if 1 == deleted:
        message = __("Theme deleted.")
    else:
        #// translators: %s: Number of themes.
        message = _n("%s theme deleted.", "%s themes deleted.", deleted)
    # end if
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + php_sprintf(message, number_format_i18n(deleted)) + "</p></div>")
elif (php_isset(lambda : PHP_REQUEST["error"])) and "none" == PHP_REQUEST["error"]:
    php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("No theme selected.") + "</p></div>")
elif (php_isset(lambda : PHP_REQUEST["error"])) and "main" == PHP_REQUEST["error"]:
    php_print("<div class=\"error notice is-dismissible\"><p>" + __("You cannot delete a theme while it is active on the main site.") + "</p></div>")
# end if
php_print("\n<form method=\"get\">\n")
wp_list_table.search_box(__("Search Installed Themes"), "theme")
php_print("</form>\n\n")
wp_list_table.views()
if "broken" == status:
    php_print("<p class=\"clear\">" + __("The following themes are installed but incomplete.") + "</p>")
# end if
php_print("\n<form id=\"bulk-action-form\" method=\"post\">\n<input type=\"hidden\" name=\"theme_status\" value=\"")
php_print(esc_attr(status))
php_print("\" />\n<input type=\"hidden\" name=\"paged\" value=\"")
php_print(esc_attr(page))
php_print("\" />\n\n")
wp_list_table.display()
php_print("""</form>
</div>
""")
wp_print_request_filesystem_credentials_modal()
wp_print_admin_notice_templates()
wp_print_update_row_templates()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)