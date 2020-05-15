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
    user = wp_unslash(PHP_POST["user"])
    user_details = wpmu_validate_user_signup(user["username"], user["email"])
    if is_wp_error(user_details["errors"]) and user_details["errors"].has_errors():
        add_user_errors = user_details["errors"]
    else:
        password = wp_generate_password(12, False)
        user_id = wpmu_create_user(esc_html(php_strtolower(user["username"])), password, sanitize_email(user["email"]))
        if (not user_id):
            add_user_errors = php_new_class("WP_Error", lambda : WP_Error("add_user_fail", __("Cannot add user.")))
        else:
            #// 
            #// Fires after a new user has been created via the network user-new.php page.
            #// 
            #// @since 4.4.0
            #// 
            #// @param int $user_id ID of the newly created user.
            #//
            do_action("network_user_new_created_user", user_id)
            wp_redirect(add_query_arg(Array({"update": "added", "user_id": user_id}), "user-new.php"))
            php_exit(0)
        # end if
    # end if
# end if
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages = Array()
    if "added" == PHP_REQUEST["update"]:
        edit_link = ""
        if (php_isset(lambda : PHP_REQUEST["user_id"])):
            user_id_new = absint(PHP_REQUEST["user_id"])
            if user_id_new:
                edit_link = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user_id_new)))
            # end if
        # end if
        message = __("User added.")
        if edit_link:
            message += php_sprintf(" <a href=\"%s\">%s</a>", edit_link, __("Edit user"))
        # end if
        messages[-1] = message
    # end if
# end if
title = __("Add New User")
parent_file = "users.php"
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1 id=\"add-new-user\">")
_e("Add New User")
php_print("</h1>\n")
if (not php_empty(lambda : messages)):
    for msg in messages:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg + "</p></div>")
    # end for
# end if
if (php_isset(lambda : add_user_errors)) and is_wp_error(add_user_errors):
    php_print(" <div class=\"error\">\n     ")
    for message in add_user_errors.get_error_messages():
        php_print(str("<p>") + str(message) + str("</p>"))
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
