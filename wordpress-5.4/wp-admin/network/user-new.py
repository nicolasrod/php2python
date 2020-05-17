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
#// Add New User network administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.1.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("create_users")):
    wp_die(__("Sorry, you are not allowed to add users to this network."))
# end if
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Add User will set up a new user account on the network and send that person an email with username and password.") + "</p>" + "<p>" + __("Users who are signed up to the network without a site are added as subscribers to the main or primary dashboard site, giving them profile pages to manage their accounts. These users will only see Dashboard and My Sites in the main navigation until a site is created for them.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Network_Admin_Users_Screen\">Documentation on Network Users</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/forum/multisite/\">Support Forums</a>") + "</p>")
if (php_isset(lambda : PHP_REQUEST["action"])) and "add-user" == PHP_REQUEST["action"]:
    check_admin_referer("add-user", "_wpnonce_add-user")
    if (not current_user_can("manage_network_users")):
        wp_die(__("Sorry, you are not allowed to access this page."), 403)
    # end if
    if (not php_is_array(PHP_POST["user"])):
        wp_die(__("Cannot create an empty user."))
    # end if
    user_ = wp_unslash(PHP_POST["user"])
    user_details_ = wpmu_validate_user_signup(user_["username"], user_["email"])
    if is_wp_error(user_details_["errors"]) and user_details_["errors"].has_errors():
        add_user_errors_ = user_details_["errors"]
    else:
        password_ = wp_generate_password(12, False)
        user_id_ = wpmu_create_user(esc_html(php_strtolower(user_["username"])), password_, sanitize_email(user_["email"]))
        if (not user_id_):
            add_user_errors_ = php_new_class("WP_Error", lambda : WP_Error("add_user_fail", __("Cannot add user.")))
        else:
            #// 
            #// Fires after a new user has been created via the network user-new.php page.
            #// 
            #// @since 4.4.0
            #// 
            #// @param int $user_id ID of the newly created user.
            #//
            do_action("network_user_new_created_user", user_id_)
            wp_redirect(add_query_arg(Array({"update": "added", "user_id": user_id_}), "user-new.php"))
            php_exit(0)
        # end if
    # end if
# end if
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages_ = Array()
    if "added" == PHP_REQUEST["update"]:
        edit_link_ = ""
        if (php_isset(lambda : PHP_REQUEST["user_id"])):
            user_id_new_ = absint(PHP_REQUEST["user_id"])
            if user_id_new_:
                edit_link_ = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user_id_new_)))
            # end if
        # end if
        message_ = __("User added.")
        if edit_link_:
            message_ += php_sprintf(" <a href=\"%s\">%s</a>", edit_link_, __("Edit user"))
        # end if
        messages_[-1] = message_
    # end if
# end if
title_ = __("Add New User")
parent_file_ = "users.php"
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 id=\"add-new-user\">")
_e("Add New User")
php_print("</h1>\n")
if (not php_empty(lambda : messages_)):
    for msg_ in messages_:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg_ + "</p></div>")
    # end for
# end if
if (php_isset(lambda : add_user_errors_)) and is_wp_error(add_user_errors_):
    php_print(" <div class=\"error\">\n     ")
    for message_ in add_user_errors_.get_error_messages():
        php_print(str("<p>") + str(message_) + str("</p>"))
    # end for
    php_print(" </div>\n")
# end if
php_print(" <form action=\"")
php_print(network_admin_url("user-new.php?action=add-user"))
php_print("""\" id=\"adduser\" method=\"post\" novalidate=\"novalidate\">
<table class=\"form-table\" role=\"presentation\">
<tr class=\"form-field form-required\">
<th scope=\"row\"><label for=\"username\">""")
_e("Username")
php_print("""</label></th>
<td><input type=\"text\" class=\"regular-text\" name=\"user[username]\" id=\"username\" autocapitalize=\"none\" autocorrect=\"off\" maxlength=\"60\" /></td>
</tr>
<tr class=\"form-field form-required\">
<th scope=\"row\"><label for=\"email\">""")
_e("Email")
php_print("""</label></th>
<td><input type=\"email\" class=\"regular-text\" name=\"user[email]\" id=\"email\"/></td>
</tr>
<tr class=\"form-field\">
<td colspan=\"2\" class=\"td-full\">""")
_e("A password reset link will be sent to the user via email.")
php_print("""</td>
</tr>
</table>
""")
#// 
#// Fires at the end of the new user form in network admin.
#// 
#// @since 4.5.0
#//
do_action("network_user_new_form")
wp_nonce_field("add-user", "_wpnonce_add-user")
submit_button(__("Add User"), "primary", "add-user")
php_print(" </form>\n</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
