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
#// Edit Site Settings Administration Screen
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.1.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_sites")):
    wp_die(__("Sorry, you are not allowed to edit this site."))
# end if
get_current_screen().add_help_tab(get_site_screen_help_tab_args())
get_current_screen().set_help_sidebar(get_site_screen_help_sidebar_content())
id = php_intval(PHP_REQUEST["id"]) if (php_isset(lambda : PHP_REQUEST["id"])) else 0
if (not id):
    wp_die(__("Invalid site ID."))
# end if
details = get_site(id)
if (not details):
    wp_die(__("The requested site does not exist."))
# end if
if (not can_edit_network(details.site_id)):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
is_main_site = is_main_site(id)
if (php_isset(lambda : PHP_REQUEST["action"])) and "update-site" == PHP_REQUEST["action"] and php_is_array(PHP_POST["option"]):
    check_admin_referer("edit-site")
    switch_to_blog(id)
    skip_options = Array("allowedthemes")
    #// Don't update these options since they are handled elsewhere in the form.
    for key,val in PHP_POST["option"]:
        key = wp_unslash(key)
        val = wp_unslash(val)
        if 0 == key or php_is_array(val) or php_in_array(key, skip_options):
            continue
            pass
        # end if
        update_option(key, val)
    # end for
    #// 
    #// Fires after the site options are updated.
    #// 
    #// @since 3.0.0
    #// @since 4.4.0 Added `$id` parameter.
    #// 
    #// @param int $id The ID of the site being updated.
    #//
    do_action("wpmu_update_blog_options", id)
    restore_current_blog()
    wp_redirect(add_query_arg(Array({"update": "updated", "id": id}), "site-settings.php"))
    php_exit(0)
# end if
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages = Array()
    if "updated" == PHP_REQUEST["update"]:
        messages[-1] = __("Site options updated.")
    # end if
# end if
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
php_print("</a></p>\n\n")
network_edit_site_nav(Array({"blog_id": id, "selected": "site-settings"}))
if (not php_empty(lambda : messages)):
    for msg in messages:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg + "</p></div>")
    # end for
# end if
php_print("<form method=\"post\" action=\"site-settings.php?action=update-site\">\n ")
wp_nonce_field("edit-site")
php_print(" <input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id))
php_print("\" />\n  <table class=\"form-table\" role=\"presentation\">\n        ")
blog_prefix = wpdb.get_blog_prefix(id)
sql = str("SELECT * FROM ") + str(blog_prefix) + str("options\n         WHERE option_name NOT LIKE %s\n         AND option_name NOT LIKE %s")
query = wpdb.prepare(sql, wpdb.esc_like("_") + "%", "%" + wpdb.esc_like("user_roles"))
options = wpdb.get_results(query)
for option in options:
    if "default_role" == option.option_name:
        editblog_default_role = option.option_value
    # end if
    disabled = False
    class_ = "all-options"
    if is_serialized(option.option_value):
        if is_serialized_string(option.option_value):
            option.option_value = esc_html(maybe_unserialize(option.option_value))
        else:
            option.option_value = "SERIALIZED DATA"
            disabled = True
            class_ = "all-options disabled"
        # end if
    # end if
    if php_strpos(option.option_value, "\n") != False:
        php_print("             <tr class=\"form-field\">\n                 <th scope=\"row\"><label for=\"")
        php_print(esc_attr(option.option_name))
        php_print("\">")
        php_print(ucwords(php_str_replace("_", " ", option.option_name)))
        php_print("</label></th>\n                  <td><textarea class=\"")
        php_print(class_)
        php_print("\" rows=\"5\" cols=\"40\" name=\"option[")
        php_print(esc_attr(option.option_name))
        php_print("]\" id=\"")
        php_print(esc_attr(option.option_name))
        php_print("\"")
        disabled(disabled)
        php_print(">")
        php_print(esc_textarea(option.option_value))
        php_print("</textarea></td>\n               </tr>\n             ")
    else:
        php_print("             <tr class=\"form-field\">\n                 <th scope=\"row\"><label for=\"")
        php_print(esc_attr(option.option_name))
        php_print("\">")
        php_print(esc_html(ucwords(php_str_replace("_", " ", option.option_name))))
        php_print("</label></th>\n                  ")
        if is_main_site and php_in_array(option.option_name, Array("siteurl", "home")):
            php_print("                 <td><code>")
            php_print(esc_html(option.option_value))
            php_print("</code></td>\n                   ")
        else:
            php_print("                 <td><input class=\"")
            php_print(class_)
            php_print("\" name=\"option[")
            php_print(esc_attr(option.option_name))
            php_print("]\" type=\"text\" id=\"")
            php_print(esc_attr(option.option_name))
            php_print("\" value=\"")
            php_print(esc_attr(option.option_value))
            php_print("\" size=\"40\" ")
            disabled(disabled)
            php_print(" /></td>\n                   ")
        # end if
        php_print("             </tr>\n             ")
    # end if
# end for
#// End foreach.
#// 
#// Fires at the end of the Edit Site form, before the submit button.
#// 
#// @since 3.0.0
#// 
#// @param int $id Site ID.
#//
do_action("wpmueditblogaction", id)
php_print(" </table>\n  ")
submit_button()
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
