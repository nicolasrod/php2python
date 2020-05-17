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
is_main_site_ = is_main_site(id_)
if (php_isset(lambda : PHP_REQUEST["action"])) and "update-site" == PHP_REQUEST["action"] and php_is_array(PHP_POST["option"]):
    check_admin_referer("edit-site")
    switch_to_blog(id_)
    skip_options_ = Array("allowedthemes")
    #// Don't update these options since they are handled elsewhere in the form.
    for key_,val_ in PHP_POST["option"]:
        key_ = wp_unslash(key_)
        val_ = wp_unslash(val_)
        if 0 == key_ or php_is_array(val_) or php_in_array(key_, skip_options_):
            continue
            pass
        # end if
        update_option(key_, val_)
    # end for
    #// 
    #// Fires after the site options are updated.
    #// 
    #// @since 3.0.0
    #// @since 4.4.0 Added `$id` parameter.
    #// 
    #// @param int $id The ID of the site being updated.
    #//
    do_action("wpmu_update_blog_options", id_)
    restore_current_blog()
    wp_redirect(add_query_arg(Array({"update": "updated", "id": id_}), "site-settings.php"))
    php_exit(0)
# end if
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages_ = Array()
    if "updated" == PHP_REQUEST["update"]:
        messages_[-1] = __("Site options updated.")
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
php_print("</a></p>\n\n")
network_edit_site_nav(Array({"blog_id": id_, "selected": "site-settings"}))
if (not php_empty(lambda : messages_)):
    for msg_ in messages_:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg_ + "</p></div>")
    # end for
# end if
php_print("<form method=\"post\" action=\"site-settings.php?action=update-site\">\n ")
wp_nonce_field("edit-site")
php_print(" <input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id_))
php_print("\" />\n  <table class=\"form-table\" role=\"presentation\">\n        ")
blog_prefix_ = wpdb_.get_blog_prefix(id_)
sql_ = str("SELECT * FROM ") + str(blog_prefix_) + str("options\n           WHERE option_name NOT LIKE %s\n         AND option_name NOT LIKE %s")
query_ = wpdb_.prepare(sql_, wpdb_.esc_like("_") + "%", "%" + wpdb_.esc_like("user_roles"))
options_ = wpdb_.get_results(query_)
for option_ in options_:
    if "default_role" == option_.option_name:
        editblog_default_role_ = option_.option_value
    # end if
    disabled_ = False
    class_ = "all-options"
    if is_serialized(option_.option_value):
        if is_serialized_string(option_.option_value):
            option_.option_value = esc_html(maybe_unserialize(option_.option_value))
        else:
            option_.option_value = "SERIALIZED DATA"
            disabled_ = True
            class_ = "all-options disabled"
        # end if
    # end if
    if php_strpos(option_.option_value, "\n") != False:
        php_print("             <tr class=\"form-field\">\n                 <th scope=\"row\"><label for=\"")
        php_print(esc_attr(option_.option_name))
        php_print("\">")
        php_print(ucwords(php_str_replace("_", " ", option_.option_name)))
        php_print("</label></th>\n                  <td><textarea class=\"")
        php_print(class_)
        php_print("\" rows=\"5\" cols=\"40\" name=\"option[")
        php_print(esc_attr(option_.option_name))
        php_print("]\" id=\"")
        php_print(esc_attr(option_.option_name))
        php_print("\"")
        disabled(disabled_)
        php_print(">")
        php_print(esc_textarea(option_.option_value))
        php_print("</textarea></td>\n               </tr>\n             ")
    else:
        php_print("             <tr class=\"form-field\">\n                 <th scope=\"row\"><label for=\"")
        php_print(esc_attr(option_.option_name))
        php_print("\">")
        php_print(esc_html(ucwords(php_str_replace("_", " ", option_.option_name))))
        php_print("</label></th>\n                  ")
        if is_main_site_ and php_in_array(option_.option_name, Array("siteurl", "home")):
            php_print("                 <td><code>")
            php_print(esc_html(option_.option_value))
            php_print("</code></td>\n                   ")
        else:
            php_print("                 <td><input class=\"")
            php_print(class_)
            php_print("\" name=\"option[")
            php_print(esc_attr(option_.option_name))
            php_print("]\" type=\"text\" id=\"")
            php_print(esc_attr(option_.option_name))
            php_print("\" value=\"")
            php_print(esc_attr(option_.option_value))
            php_print("\" size=\"40\" ")
            disabled(disabled_)
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
do_action("wpmueditblogaction", id_)
php_print(" </table>\n  ")
submit_button()
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
