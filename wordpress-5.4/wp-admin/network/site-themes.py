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
#// Edit Site Themes Administration Screen
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.1.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_sites")):
    wp_die(__("Sorry, you are not allowed to manage themes for this site."))
# end if
get_current_screen().add_help_tab(get_site_screen_help_tab_args())
get_current_screen().set_help_sidebar(get_site_screen_help_sidebar_content())
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter site themes list"), "heading_pagination": __("Site themes list navigation"), "heading_list": __("Site themes list")}))
wp_list_table = _get_list_table("WP_MS_Themes_List_Table")
action = wp_list_table.current_action()
s = PHP_REQUEST["s"] if (php_isset(lambda : PHP_REQUEST["s"])) else ""
#// Clean up request URI from temporary args for screen options/paging uri's to work as expected.
temp_args = Array("enabled", "disabled", "error")
PHP_SERVER["REQUEST_URI"] = remove_query_arg(temp_args, PHP_SERVER["REQUEST_URI"])
referer = remove_query_arg(temp_args, wp_get_referer())
if (not php_empty(lambda : PHP_REQUEST["paged"])):
    referer = add_query_arg("paged", php_int(PHP_REQUEST["paged"]), referer)
# end if
id = php_intval(PHP_REQUEST["id"]) if (php_isset(lambda : PHP_REQUEST["id"])) else 0
if (not id):
    wp_die(__("Invalid site ID."))
# end if
wp_list_table.prepare_items()
details = get_site(id)
if (not details):
    wp_die(__("The requested site does not exist."))
# end if
if (not can_edit_network(details.site_id)):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
is_main_site = is_main_site(id)
if action:
    switch_to_blog(id)
    allowed_themes = get_option("allowedthemes")
    for case in Switch(action):
        if case("enable"):
            check_admin_referer("enable-theme_" + PHP_REQUEST["theme"])
            theme = PHP_REQUEST["theme"]
            action = "enabled"
            n = 1
            if (not allowed_themes):
                allowed_themes = Array({theme: True})
            else:
                allowed_themes[theme] = True
            # end if
            break
        # end if
        if case("disable"):
            check_admin_referer("disable-theme_" + PHP_REQUEST["theme"])
            theme = PHP_REQUEST["theme"]
            action = "disabled"
            n = 1
            if (not allowed_themes):
                allowed_themes = Array()
            else:
                allowed_themes[theme] = None
            # end if
            break
        # end if
        if case("enable-selected"):
            check_admin_referer("bulk-themes")
            if (php_isset(lambda : PHP_POST["checked"])):
                themes = PHP_POST["checked"]
                action = "enabled"
                n = php_count(themes)
                for theme in themes:
                    allowed_themes[theme] = True
                # end for
            else:
                action = "error"
                n = "none"
            # end if
            break
        # end if
        if case("disable-selected"):
            check_admin_referer("bulk-themes")
            if (php_isset(lambda : PHP_POST["checked"])):
                themes = PHP_POST["checked"]
                action = "disabled"
                n = php_count(themes)
                for theme in themes:
                    allowed_themes[theme] = None
                # end for
            else:
                action = "error"
                n = "none"
            # end if
            break
        # end if
        if case():
            if (php_isset(lambda : PHP_POST["checked"])):
                check_admin_referer("bulk-themes")
                themes = PHP_POST["checked"]
                n = php_count(themes)
                screen = get_current_screen().id
                #// 
                #// Fires when a custom bulk action should be handled.
                #// 
                #// The redirect link should be modified with success or failure feedback
                #// from the action to be used to display feedback to the user.
                #// 
                #// The dynamic portion of the hook name, `$screen`, refers to the current screen ID.
                #// 
                #// @since 4.7.0
                #// 
                #// @param string $redirect_url The redirect URL.
                #// @param string $action       The action being taken.
                #// @param array  $items        The items to take the action on.
                #// @param int    $site_id      The site ID.
                #//
                referer = apply_filters(str("handle_network_bulk_actions-") + str(screen), referer, action, themes, id)
                pass
            else:
                action = "error"
                n = "none"
            # end if
        # end if
    # end for
    update_option("allowedthemes", allowed_themes)
    restore_current_blog()
    wp_safe_redirect(add_query_arg(Array({"id": id, action: n}), referer))
    php_exit(0)
# end if
if (php_isset(lambda : PHP_REQUEST["action"])) and "update-site" == PHP_REQUEST["action"]:
    wp_safe_redirect(referer)
    php_exit(0)
# end if
add_thickbox()
add_screen_option("per_page")
#// translators: %s: Site title.
title = php_sprintf(__("Edit Site: %s"), esc_html(details.blogname))
parent_file = "sites.php"
submenu_file = "sites.php"
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 id=\"edit-site\">")
php_print(title)
php_print("</h1>\n<p class=\"edit-site-actions\"><a href=\"")
php_print(esc_url(get_home_url(id, "/")))
php_print("\">")
_e("Visit")
php_print("</a> | <a href=\"")
php_print(esc_url(get_admin_url(id)))
php_print("\">")
_e("Dashboard")
php_print("</a></p>\n")
network_edit_site_nav(Array({"blog_id": id, "selected": "site-themes"}))
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
elif (php_isset(lambda : PHP_REQUEST["error"])) and "none" == PHP_REQUEST["error"]:
    php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("No theme selected.") + "</p></div>")
# end if
php_print("\n<p>")
_e("Network enabled themes are not shown on this screen.")
php_print("""</p>
<form method=\"get\">
""")
wp_list_table.search_box(__("Search Installed Themes"), "theme")
php_print("<input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id))
php_print("""\" />
</form>
""")
wp_list_table.views()
php_print("\n<form method=\"post\" action=\"site-themes.php?action=update-site\">\n <input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id))
php_print("\" />\n\n")
wp_list_table.display()
php_print("""
</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
