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
id_ = php_intval(PHP_REQUEST["id"]) if (php_isset(lambda : PHP_REQUEST["id"])) else 0
if (not id_):
    wp_die(__("Invalid site ID."))
# end if
details_ = get_site(id_)
if (not details_):
    wp_die(__("The requested site does not exist."))
# end if
if (not can_edit_network(details_.site_id)):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
parsed_scheme_ = php_parse_url(details_.siteurl, PHP_URL_SCHEME)
is_main_site_ = is_main_site(id_)
if (php_isset(lambda : PHP_REQUEST["action"])) and "update-site" == PHP_REQUEST["action"]:
    check_admin_referer("edit-site")
    switch_to_blog(id_)
    #// Rewrite rules can't be flushed during switch to blog.
    delete_option("rewrite_rules")
    blog_data_ = wp_unslash(PHP_POST["blog"])
    blog_data_["scheme"] = parsed_scheme_
    if is_main_site_:
        #// On the network's main site, don't allow the domain or path to change.
        blog_data_["domain"] = details_.domain
        blog_data_["path"] = details_.path
    else:
        #// For any other site, the scheme, domain, and path can all be changed. We first
        #// need to ensure a scheme has been provided, otherwise fallback to the existing.
        new_url_scheme_ = php_parse_url(blog_data_["url"], PHP_URL_SCHEME)
        if (not new_url_scheme_):
            blog_data_["url"] = esc_url(parsed_scheme_ + "://" + blog_data_["url"])
        # end if
        update_parsed_url_ = php_parse_url(blog_data_["url"])
        #// If a path is not provided, use the default of `/`.
        if (not (php_isset(lambda : update_parsed_url_["path"]))):
            update_parsed_url_["path"] = "/"
        # end if
        blog_data_["scheme"] = update_parsed_url_["scheme"]
        blog_data_["domain"] = update_parsed_url_["host"]
        blog_data_["path"] = update_parsed_url_["path"]
    # end if
    existing_details_ = get_site(id_)
    blog_data_checkboxes_ = Array("public", "archived", "spam", "mature", "deleted")
    for c_ in blog_data_checkboxes_:
        if (not php_in_array(existing_details_.c_, Array(0, 1))):
            blog_data_[c_] = existing_details_.c_
        else:
            blog_data_[c_] = 1 if (php_isset(lambda : PHP_POST["blog"][c_])) else 0
        # end if
    # end for
    update_blog_details(id_, blog_data_)
    #// Maybe update home and siteurl options.
    new_details_ = get_site(id_)
    old_home_url_ = trailingslashit(esc_url(get_option("home")))
    old_home_parsed_ = php_parse_url(old_home_url_)
    if old_home_parsed_["host"] == existing_details_.domain and old_home_parsed_["path"] == existing_details_.path:
        new_home_url_ = untrailingslashit(esc_url_raw(blog_data_["scheme"] + "://" + new_details_.domain + new_details_.path))
        update_option("home", new_home_url_)
    # end if
    old_site_url_ = trailingslashit(esc_url(get_option("siteurl")))
    old_site_parsed_ = php_parse_url(old_site_url_)
    if old_site_parsed_["host"] == existing_details_.domain and old_site_parsed_["path"] == existing_details_.path:
        new_site_url_ = untrailingslashit(esc_url_raw(blog_data_["scheme"] + "://" + new_details_.domain + new_details_.path))
        update_option("siteurl", new_site_url_)
    # end if
    restore_current_blog()
    wp_redirect(add_query_arg(Array({"update": "updated", "id": id_}), "site-info.php"))
    php_exit(0)
# end if
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages_ = Array()
    if "updated" == PHP_REQUEST["update"]:
        messages_[-1] = __("Site info updated.")
    # end if
# end if
#// translators: %s: Site title.
title_ = php_sprintf(__("Edit Site: %s"), esc_html(details_.blogname))
parent_file_ = "sites.php"
submenu_file_ = "sites.php"
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 id=\"edit-site\">")
php_print(title_)
php_print("</h1>\n<p class=\"edit-site-actions\"><a href=\"")
php_print(esc_url(get_home_url(id_, "/")))
php_print("\">")
_e("Visit")
php_print("</a> | <a href=\"")
php_print(esc_url(get_admin_url(id_)))
php_print("\">")
_e("Dashboard")
php_print("</a></p>\n")
network_edit_site_nav(Array({"blog_id": id_, "selected": "site-info"}))
if (not php_empty(lambda : messages_)):
    for msg_ in messages_:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg_ + "</p></div>")
    # end for
# end if
php_print("<form method=\"post\" action=\"site-info.php?action=update-site\">\n ")
wp_nonce_field("edit-site")
php_print(" <input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id_))
php_print("\" />\n  <table class=\"form-table\" role=\"presentation\">\n        ")
#// The main site of the network should not be updated on this page.
if is_main_site_:
    php_print("     <tr class=\"form-field\">\n         <th scope=\"row\">")
    _e("Site Address (URL)")
    php_print("</th>\n          <td>")
    php_print(esc_url(parsed_scheme_ + "://" + details_.domain + details_.path))
    php_print("</td>\n      </tr>\n         ")
    pass
else:
    php_print("     <tr class=\"form-field form-required\">\n           <th scope=\"row\"><label for=\"url\">")
    _e("Site Address (URL)")
    php_print("</label></th>\n          <td><input name=\"blog[url]\" type=\"text\" id=\"url\" value=\"")
    php_print(parsed_scheme_ + "://" + esc_attr(details_.domain) + esc_attr(details_.path))
    php_print("\" /></td>\n     </tr>\n     ")
# end if
php_print("\n       <tr class=\"form-field\">\n         <th scope=\"row\"><label for=\"blog_registered\">")
_ex("Registered", "site")
php_print("</label></th>\n          <td><input name=\"blog[registered]\" type=\"text\" id=\"blog_registered\" value=\"")
php_print(esc_attr(details_.registered))
php_print("""\" /></td>
</tr>
<tr class=\"form-field\">
<th scope=\"row\"><label for=\"blog_last_updated\">""")
_e("Last Updated")
php_print("</label></th>\n          <td><input name=\"blog[last_updated]\" type=\"text\" id=\"blog_last_updated\" value=\"")
php_print(esc_attr(details_.last_updated))
php_print("\" /></td>\n     </tr>\n     ")
attribute_fields_ = Array({"public": __("Public")})
if (not is_main_site_):
    attribute_fields_["archived"] = __("Archived")
    attribute_fields_["spam"] = _x("Spam", "site")
    attribute_fields_["deleted"] = __("Deleted")
# end if
attribute_fields_["mature"] = __("Mature")
php_print("     <tr>\n          <th scope=\"row\">")
_e("Attributes")
php_print("""</th>
<td>
<fieldset>
<legend class=\"screen-reader-text\">""")
_e("Set site attributes")
php_print("</legend>\n          ")
for field_key_,field_label_ in attribute_fields_.items():
    php_print("             <label><input type=\"checkbox\" name=\"blog[")
    php_print(field_key_)
    php_print("]\" value=\"1\" ")
    checked(php_bool(details_.field_key_), True)
    php_print(" ")
    disabled((not php_in_array(details_.field_key_, Array(0, 1))))
    php_print(" />\n                ")
    php_print(field_label_)
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
