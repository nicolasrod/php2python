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
#// Edit Site Info Administration Screen
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
parsed_scheme = php_parse_url(details.siteurl, PHP_URL_SCHEME)
is_main_site = is_main_site(id)
if (php_isset(lambda : PHP_REQUEST["action"])) and "update-site" == PHP_REQUEST["action"]:
    check_admin_referer("edit-site")
    switch_to_blog(id)
    #// Rewrite rules can't be flushed during switch to blog.
    delete_option("rewrite_rules")
    blog_data = wp_unslash(PHP_POST["blog"])
    blog_data["scheme"] = parsed_scheme
    if is_main_site:
        #// On the network's main site, don't allow the domain or path to change.
        blog_data["domain"] = details.domain
        blog_data["path"] = details.path
    else:
        #// For any other site, the scheme, domain, and path can all be changed. We first
        #// need to ensure a scheme has been provided, otherwise fallback to the existing.
        new_url_scheme = php_parse_url(blog_data["url"], PHP_URL_SCHEME)
        if (not new_url_scheme):
            blog_data["url"] = esc_url(parsed_scheme + "://" + blog_data["url"])
        # end if
        update_parsed_url = php_parse_url(blog_data["url"])
        #// If a path is not provided, use the default of `/`.
        if (not (php_isset(lambda : update_parsed_url["path"]))):
            update_parsed_url["path"] = "/"
        # end if
        blog_data["scheme"] = update_parsed_url["scheme"]
        blog_data["domain"] = update_parsed_url["host"]
        blog_data["path"] = update_parsed_url["path"]
    # end if
    existing_details = get_site(id)
    blog_data_checkboxes = Array("public", "archived", "spam", "mature", "deleted")
    for c in blog_data_checkboxes:
        if (not php_in_array(existing_details.c, Array(0, 1))):
            blog_data[c] = existing_details.c
        else:
            blog_data[c] = 1 if (php_isset(lambda : PHP_POST["blog"][c])) else 0
        # end if
    # end for
    update_blog_details(id, blog_data)
    #// Maybe update home and siteurl options.
    new_details = get_site(id)
    old_home_url = trailingslashit(esc_url(get_option("home")))
    old_home_parsed = php_parse_url(old_home_url)
    if old_home_parsed["host"] == existing_details.domain and old_home_parsed["path"] == existing_details.path:
        new_home_url = untrailingslashit(esc_url_raw(blog_data["scheme"] + "://" + new_details.domain + new_details.path))
        update_option("home", new_home_url)
    # end if
    old_site_url = trailingslashit(esc_url(get_option("siteurl")))
    old_site_parsed = php_parse_url(old_site_url)
    if old_site_parsed["host"] == existing_details.domain and old_site_parsed["path"] == existing_details.path:
        new_site_url = untrailingslashit(esc_url_raw(blog_data["scheme"] + "://" + new_details.domain + new_details.path))
        update_option("siteurl", new_site_url)
    # end if
    restore_current_blog()
    wp_redirect(add_query_arg(Array({"update": "updated", "id": id}), "site-info.php"))
    php_exit(0)
# end if
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages = Array()
    if "updated" == PHP_REQUEST["update"]:
        messages[-1] = __("Site info updated.")
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
php_print("</a></p>\n")
network_edit_site_nav(Array({"blog_id": id, "selected": "site-info"}))
if (not php_empty(lambda : messages)):
    for msg in messages:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg + "</p></div>")
    # end for
# end if
php_print("<form method=\"post\" action=\"site-info.php?action=update-site\">\n ")
wp_nonce_field("edit-site")
php_print(" <input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id))
php_print("\" />\n  <table class=\"form-table\" role=\"presentation\">\n        ")
#// The main site of the network should not be updated on this page.
if is_main_site:
    php_print("     <tr class=\"form-field\">\n         <th scope=\"row\">")
    _e("Site Address (URL)")
    php_print("</th>\n          <td>")
    php_print(esc_url(parsed_scheme + "://" + details.domain + details.path))
    php_print("</td>\n      </tr>\n         ")
    pass
else:
    php_print("     <tr class=\"form-field form-required\">\n           <th scope=\"row\"><label for=\"url\">")
    _e("Site Address (URL)")
    php_print("</label></th>\n          <td><input name=\"blog[url]\" type=\"text\" id=\"url\" value=\"")
    php_print(parsed_scheme + "://" + esc_attr(details.domain) + esc_attr(details.path))
    php_print("\" /></td>\n     </tr>\n     ")
# end if
php_print("\n       <tr class=\"form-field\">\n         <th scope=\"row\"><label for=\"blog_registered\">")
_ex("Registered", "site")
php_print("</label></th>\n          <td><input name=\"blog[registered]\" type=\"text\" id=\"blog_registered\" value=\"")
php_print(esc_attr(details.registered))
php_print("""\" /></td>
</tr>
<tr class=\"form-field\">
<th scope=\"row\"><label for=\"blog_last_updated\">""")
_e("Last Updated")
php_print("</label></th>\n          <td><input name=\"blog[last_updated]\" type=\"text\" id=\"blog_last_updated\" value=\"")
php_print(esc_attr(details.last_updated))
php_print("\" /></td>\n     </tr>\n     ")
attribute_fields = Array({"public": __("Public")})
if (not is_main_site):
    attribute_fields["archived"] = __("Archived")
    attribute_fields["spam"] = _x("Spam", "site")
    attribute_fields["deleted"] = __("Deleted")
# end if
attribute_fields["mature"] = __("Mature")
php_print("     <tr>\n          <th scope=\"row\">")
_e("Attributes")
php_print("""</th>
<td>
<fieldset>
<legend class=\"screen-reader-text\">""")
_e("Set site attributes")
php_print("</legend>\n          ")
for field_key,field_label in attribute_fields:
    php_print("             <label><input type=\"checkbox\" name=\"blog[")
    php_print(field_key)
    php_print("]\" value=\"1\" ")
    checked(bool(details.field_key), True)
    php_print(" ")
    disabled((not php_in_array(details.field_key, Array(0, 1))))
    php_print(" />\n                ")
    php_print(field_label)
    php_print("</label><br/>\n          ")
# end for
php_print("""           <fieldset>
</td>
</tr>
</table>
""")
submit_button()
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
