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
#// Edit Site Users Administration Screen
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.1.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_sites")):
    wp_die(__("Sorry, you are not allowed to edit this site."), 403)
# end if
wp_list_table_ = _get_list_table("WP_Users_List_Table")
wp_list_table_.prepare_items()
get_current_screen().add_help_tab(get_site_screen_help_tab_args())
get_current_screen().set_help_sidebar(get_site_screen_help_sidebar_content())
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter site users list"), "heading_pagination": __("Site users list navigation"), "heading_list": __("Site users list")}))
PHP_SERVER["REQUEST_URI"] = remove_query_arg("update", PHP_SERVER["REQUEST_URI"])
referer_ = remove_query_arg("update", wp_get_referer())
if (not php_empty(lambda : PHP_REQUEST["paged"])):
    referer_ = add_query_arg("paged", php_int(PHP_REQUEST["paged"]), referer_)
# end if
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
switch_to_blog(id_)
action_ = wp_list_table_.current_action()
if action_:
    for case in Switch(action_):
        if case("newuser"):
            check_admin_referer("add-user", "_wpnonce_add-new-user")
            user_ = PHP_POST["user"]
            if (not php_is_array(PHP_POST["user"])) or php_empty(lambda : user_["username"]) or php_empty(lambda : user_["email"]):
                update_ = "err_new"
            else:
                password_ = wp_generate_password(12, False)
                user_id_ = wpmu_create_user(esc_html(php_strtolower(user_["username"])), password_, esc_html(user_["email"]))
                if False == user_id_:
                    update_ = "err_new_dup"
                else:
                    result_ = add_user_to_blog(id_, user_id_, PHP_POST["new_role"])
                    if is_wp_error(result_):
                        update_ = "err_add_fail"
                    else:
                        update_ = "newuser"
                        #// 
                        #// Fires after a user has been created via the network site-users.php page.
                        #// 
                        #// @since 4.4.0
                        #// 
                        #// @param int $user_id ID of the newly created user.
                        #//
                        do_action("network_site_users_created_user", user_id_)
                    # end if
                # end if
            # end if
            break
        # end if
        if case("adduser"):
            check_admin_referer("add-user", "_wpnonce_add-user")
            if (not php_empty(lambda : PHP_POST["newuser"])):
                update_ = "adduser"
                newuser_ = PHP_POST["newuser"]
                user_ = get_user_by("login", newuser_)
                if user_ and user_.exists():
                    if (not is_user_member_of_blog(user_.ID, id_)):
                        result_ = add_user_to_blog(id_, user_.ID, PHP_POST["new_role"])
                        if is_wp_error(result_):
                            update_ = "err_add_fail"
                        # end if
                    else:
                        update_ = "err_add_member"
                    # end if
                else:
                    update_ = "err_add_notfound"
                # end if
            else:
                update_ = "err_add_notfound"
            # end if
            break
        # end if
        if case("remove"):
            if (not current_user_can("remove_users")):
                wp_die(__("Sorry, you are not allowed to remove users."), 403)
            # end if
            check_admin_referer("bulk-users")
            update_ = "remove"
            if (php_isset(lambda : PHP_REQUEST["users"])):
                userids_ = PHP_REQUEST["users"]
                for user_id_ in userids_:
                    user_id_ = php_int(user_id_)
                    remove_user_from_blog(user_id_, id_)
                # end for
            elif (php_isset(lambda : PHP_REQUEST["user"])):
                remove_user_from_blog(PHP_REQUEST["user"])
            else:
                update_ = "err_remove"
            # end if
            break
        # end if
        if case("promote"):
            check_admin_referer("bulk-users")
            editable_roles_ = get_editable_roles()
            role_ = False
            if (not php_empty(lambda : PHP_REQUEST["new_role2"])):
                role_ = PHP_REQUEST["new_role2"]
            elif (not php_empty(lambda : PHP_REQUEST["new_role"])):
                role_ = PHP_REQUEST["new_role"]
            # end if
            if php_empty(lambda : editable_roles_[role_]):
                wp_die(__("Sorry, you are not allowed to give users that role."), 403)
            # end if
            if (php_isset(lambda : PHP_REQUEST["users"])):
                userids_ = PHP_REQUEST["users"]
                update_ = "promote"
                for user_id_ in userids_:
                    user_id_ = php_int(user_id_)
                    #// If the user doesn't already belong to the blog, bail.
                    if (not is_user_member_of_blog(user_id_)):
                        wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("One of the selected users is not a member of this site.") + "</p>", 403)
                    # end if
                    user_ = get_userdata(user_id_)
                    user_.set_role(role_)
                # end for
            else:
                update_ = "err_promote"
            # end if
            break
        # end if
        if case():
            if (not (php_isset(lambda : PHP_REQUEST["users"]))):
                break
            # end if
            check_admin_referer("bulk-users")
            userids_ = PHP_REQUEST["users"]
            #// This action is documented in wp-admin/network/site-themes.php
            referer_ = apply_filters("handle_network_bulk_actions-" + get_current_screen().id, referer_, action_, userids_, id_)
            #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
            update_ = action_
            break
        # end if
    # end for
    wp_safe_redirect(add_query_arg("update", update_, referer_))
    php_exit(0)
# end if
restore_current_blog()
if (php_isset(lambda : PHP_REQUEST["action"])) and "update-site" == PHP_REQUEST["action"]:
    wp_safe_redirect(referer_)
    php_exit(0)
# end if
add_screen_option("per_page")
#// translators: %s: Site title.
title_ = php_sprintf(__("Edit Site: %s"), esc_html(details_.blogname))
parent_file_ = "sites.php"
submenu_file_ = "sites.php"
#// 
#// Filters whether to show the Add Existing User form on the Multisite Users screen.
#// 
#// @since 3.1.0
#// 
#// @param bool $bool Whether to show the Add Existing User form. Default true.
#//
if (not wp_is_large_network("users")) and apply_filters("show_network_site_users_add_existing_form", True):
    wp_enqueue_script("user-suggest")
# end if
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<script type=\"text/javascript\">\nvar current_site_id = ")
php_print(id_)
php_print(""";
</script>
<div class=\"wrap\">
<h1 id=\"edit-site\">""")
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
network_edit_site_nav(Array({"blog_id": id_, "selected": "site-users"}))
if (php_isset(lambda : PHP_REQUEST["update"])):
    for case in Switch(PHP_REQUEST["update"]):
        if case("adduser"):
            php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("User added.") + "</p></div>")
            break
        # end if
        if case("err_add_member"):
            php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("User is already a member of this site.") + "</p></div>")
            break
        # end if
        if case("err_add_fail"):
            php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("User could not be added to this site.") + "</p></div>")
            break
        # end if
        if case("err_add_notfound"):
            php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("Enter the username of an existing user.") + "</p></div>")
            break
        # end if
        if case("promote"):
            php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("Changed roles.") + "</p></div>")
            break
        # end if
        if case("err_promote"):
            php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("Select a user to change role.") + "</p></div>")
            break
        # end if
        if case("remove"):
            php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("User removed from this site.") + "</p></div>")
            break
        # end if
        if case("err_remove"):
            php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("Select a user to remove.") + "</p></div>")
            break
        # end if
        if case("newuser"):
            php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("User created.") + "</p></div>")
            break
        # end if
        if case("err_new"):
            php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("Enter the username and email.") + "</p></div>")
            break
        # end if
        if case("err_new_dup"):
            php_print("<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("Duplicated username or email address.") + "</p></div>")
            break
        # end if
    # end for
# end if
php_print("\n<form class=\"search-form\" method=\"get\">\n")
wp_list_table_.search_box(__("Search Users"), "user")
php_print("<input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id_))
php_print("""\" />
</form>
""")
wp_list_table_.views()
php_print("\n<form method=\"post\" action=\"site-users.php?action=update-site\">\n  <input type=\"hidden\" name=\"id\" value=\"")
php_print(esc_attr(id_))
php_print("\" />\n\n")
wp_list_table_.display()
php_print("""
</form>
""")
#// 
#// Fires after the list table on the Users screen in the Multisite Network Admin.
#// 
#// @since 3.1.0
#//
do_action("network_site_users_after_list_table")
#// This filter is documented in wp-admin/network/site-users.php
if current_user_can("promote_users") and apply_filters("show_network_site_users_add_existing_form", True):
    php_print("<h2 id=\"add-existing-user\">")
    _e("Add Existing User")
    php_print("</h2>\n<form action=\"site-users.php?action=adduser\" id=\"adduser\" method=\"post\">\n  <input type=\"hidden\" name=\"id\" value=\"")
    php_print(esc_attr(id_))
    php_print("""\" />
    <table class=\"form-table\" role=\"presentation\">
    <tr>
    <th scope=\"row\"><label for=\"newuser\">""")
    _e("Username")
    php_print("""</label></th>
    <td><input type=\"text\" class=\"regular-text wp-suggest-user\" name=\"newuser\" id=\"newuser\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"new_role_adduser\">""")
    _e("Role")
    php_print("</label></th>\n          <td><select name=\"new_role\" id=\"new_role_adduser\">\n            ")
    switch_to_blog(id_)
    wp_dropdown_roles(get_option("default_role"))
    restore_current_blog()
    php_print("""           </select></td>
    </tr>
    </table>
    """)
    wp_nonce_field("add-user", "_wpnonce_add-user")
    php_print(" ")
    submit_button(__("Add User"), "primary", "add-user", True, Array({"id": "submit-add-existing-user"}))
    php_print("</form>\n")
# end if
php_print("\n")
#// 
#// Filters whether to show the Add New User form on the Multisite Users screen.
#// 
#// @since 3.1.0
#// 
#// @param bool $bool Whether to show the Add New User form. Default true.
#//
if current_user_can("create_users") and apply_filters("show_network_site_users_add_new_form", True):
    php_print("<h2 id=\"add-new-user\">")
    _e("Add New User")
    php_print("</h2>\n<form action=\"")
    php_print(network_admin_url("site-users.php?action=newuser"))
    php_print("\" id=\"newuser\" method=\"post\">\n <input type=\"hidden\" name=\"id\" value=\"")
    php_print(esc_attr(id_))
    php_print("""\" />
    <table class=\"form-table\" role=\"presentation\">
    <tr>
    <th scope=\"row\"><label for=\"user_username\">""")
    _e("Username")
    php_print("""</label></th>
    <td><input type=\"text\" class=\"regular-text\" name=\"user[username]\" id=\"user_username\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"user_email\">""")
    _e("Email")
    php_print("""</label></th>
    <td><input type=\"text\" class=\"regular-text\" name=\"user[email]\" id=\"user_email\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"new_role_newuser\">""")
    _e("Role")
    php_print("</label></th>\n          <td><select name=\"new_role\" id=\"new_role_newuser\">\n            ")
    switch_to_blog(id_)
    wp_dropdown_roles(get_option("default_role"))
    restore_current_blog()
    php_print("""           </select></td>
    </tr>
    <tr class=\"form-field\">
    <td colspan=\"2\" class=\"td-full\">""")
    _e("A password reset link will be sent to the user via email.")
    php_print("""</td>
    </tr>
    </table>
    """)
    wp_nonce_field("add-user", "_wpnonce_add-new-user")
    php_print(" ")
    submit_button(__("Add New User"), "primary", "add-user", True, Array({"id": "submit-add-user"}))
    php_print("</form>\n")
# end if
php_print("</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
