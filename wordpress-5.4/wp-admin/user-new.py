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
#// New User Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if is_multisite():
    if (not current_user_can("create_users")) and (not current_user_can("promote_users")):
        wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to add users to this network.") + "</p>", 403)
    # end if
elif (not current_user_can("create_users")):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to create users.") + "</p>", 403)
# end if
if is_multisite():
    add_filter("wpmu_signup_user_notification_email", "admin_created_user_email")
# end if
if (php_isset(lambda : PHP_REQUEST["action"])) and "adduser" == PHP_REQUEST["action"]:
    check_admin_referer("add-user", "_wpnonce_add-user")
    user_details = None
    user_email = wp_unslash(PHP_REQUEST["email"])
    if False != php_strpos(user_email, "@"):
        user_details = get_user_by("email", user_email)
    else:
        if current_user_can("manage_network_users"):
            user_details = get_user_by("login", user_email)
        else:
            wp_redirect(add_query_arg(Array({"update": "enter_email"}), "user-new.php"))
            php_exit(0)
        # end if
    # end if
    if (not user_details):
        wp_redirect(add_query_arg(Array({"update": "does_not_exist"}), "user-new.php"))
        php_exit(0)
    # end if
    if (not current_user_can("promote_user", user_details.ID)):
        wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to add users to this network.") + "</p>", 403)
    # end if
    #// Adding an existing user to this blog.
    new_user_email = user_details.user_email
    redirect = "user-new.php"
    username = user_details.user_login
    user_id = user_details.ID
    if None != username and php_array_key_exists(blog_id, get_blogs_of_user(user_id)):
        redirect = add_query_arg(Array({"update": "addexisting"}), "user-new.php")
    else:
        if (php_isset(lambda : PHP_POST["noconfirmation"])) and current_user_can("manage_network_users"):
            result = add_existing_user_to_blog(Array({"user_id": user_id, "role": PHP_REQUEST["role"]}))
            if (not is_wp_error(result)):
                redirect = add_query_arg(Array({"update": "addnoconfirmation", "user_id": user_id}), "user-new.php")
            else:
                redirect = add_query_arg(Array({"update": "could_not_add"}), "user-new.php")
            # end if
        else:
            newuser_key = wp_generate_password(20, False)
            add_option("new_user_" + newuser_key, Array({"user_id": user_id, "email": user_details.user_email, "role": PHP_REQUEST["role"]}))
            roles = get_editable_roles()
            role = roles[PHP_REQUEST["role"]]
            #// 
            #// Fires immediately after a user is invited to join a site, but before the notification is sent.
            #// 
            #// @since 4.4.0
            #// 
            #// @param int    $user_id     The invited user's ID.
            #// @param array  $role        Array containing role information for the invited user.
            #// @param string $newuser_key The key of the invitation.
            #//
            do_action("invite_user", user_id, role, newuser_key)
            switched_locale = switch_to_locale(get_user_locale(user_details))
            #// translators: 1: Site title, 2: Site URL, 3: User role, 4: Activation URL.
            message = __("""Hi,
            You've been invited to join '%1$s' at
            %2$s with the role of %3$s.
            Please click the following link to confirm the invite:
            %4$s""")
            wp_mail(new_user_email, php_sprintf(__("[%s] Joining Confirmation"), wp_specialchars_decode(get_option("blogname"))), php_sprintf(message, get_option("blogname"), home_url(), wp_specialchars_decode(translate_user_role(role["name"])), home_url(str("/newbloguser/") + str(newuser_key) + str("/"))))
            if switched_locale:
                restore_previous_locale()
            # end if
            redirect = add_query_arg(Array({"update": "add"}), "user-new.php")
        # end if
    # end if
    wp_redirect(redirect)
    php_exit(0)
elif (php_isset(lambda : PHP_REQUEST["action"])) and "createuser" == PHP_REQUEST["action"]:
    check_admin_referer("create-user", "_wpnonce_create-user")
    if (not current_user_can("create_users")):
        wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to create users.") + "</p>", 403)
    # end if
    if (not is_multisite()):
        user_id = edit_user()
        if is_wp_error(user_id):
            add_user_errors = user_id
        else:
            if current_user_can("list_users"):
                redirect = "users.php?update=add&id=" + user_id
            else:
                redirect = add_query_arg("update", "add", "user-new.php")
            # end if
            wp_redirect(redirect)
            php_exit(0)
        # end if
    else:
        #// Adding a new user to this site.
        new_user_email = wp_unslash(PHP_REQUEST["email"])
        user_details = wpmu_validate_user_signup(PHP_REQUEST["user_login"], new_user_email)
        if is_wp_error(user_details["errors"]) and user_details["errors"].has_errors():
            add_user_errors = user_details["errors"]
        else:
            #// This filter is documented in wp-includes/user.php
            new_user_login = apply_filters("pre_user_login", sanitize_user(wp_unslash(PHP_REQUEST["user_login"]), True))
            if (php_isset(lambda : PHP_POST["noconfirmation"])) and current_user_can("manage_network_users"):
                add_filter("wpmu_signup_user_notification", "__return_false")
                #// Disable confirmation email.
                add_filter("wpmu_welcome_user_notification", "__return_false")
                pass
            # end if
            wpmu_signup_user(new_user_login, new_user_email, Array({"add_to_blog": get_current_blog_id(), "new_role": PHP_REQUEST["role"]}))
            if (php_isset(lambda : PHP_POST["noconfirmation"])) and current_user_can("manage_network_users"):
                key = wpdb.get_var(wpdb.prepare(str("SELECT activation_key FROM ") + str(wpdb.signups) + str(" WHERE user_login = %s AND user_email = %s"), new_user_login, new_user_email))
                new_user = wpmu_activate_signup(key)
                if is_wp_error(new_user):
                    redirect = add_query_arg(Array({"update": "addnoconfirmation"}), "user-new.php")
                elif (not is_user_member_of_blog(new_user["user_id"])):
                    redirect = add_query_arg(Array({"update": "created_could_not_add"}), "user-new.php")
                else:
                    redirect = add_query_arg(Array({"update": "addnoconfirmation", "user_id": new_user["user_id"]}), "user-new.php")
                # end if
            else:
                redirect = add_query_arg(Array({"update": "newuserconfirmation"}), "user-new.php")
            # end if
            wp_redirect(redirect)
            php_exit(0)
        # end if
    # end if
# end if
title = __("Add New User")
parent_file = "users.php"
do_both = False
if is_multisite() and current_user_can("promote_users") and current_user_can("create_users"):
    do_both = True
# end if
help = "<p>" + __("To add a new user to your site, fill in the form on this screen and click the Add New User button at the bottom.") + "</p>"
if is_multisite():
    help += "<p>" + __("Because this is a multisite installation, you may add accounts that already exist on the Network by specifying a username or email, and defining a role. For more options, such as specifying a password, you have to be a Network Administrator and use the hover link under an existing user&#8217;s name to Edit the user profile under Network Admin > All Users.") + "</p>" + "<p>" + __("New users will receive an email letting them know they&#8217;ve been added as a user for your site. This email will also contain their password. Check the box if you don&#8217;t want the user to receive a welcome email.") + "</p>"
else:
    help += "<p>" + __("New users are automatically assigned a password, which they can change after logging in. You can view or edit the assigned password by clicking the Show Password button. The username cannot be changed once the user has been added.") + "</p>" + "<p>" + __("By default, new users will receive an email letting them know they&#8217;ve been added as a user for your site. This email will also contain a password reset link. Uncheck the box if you don&#8217;t want to send the new user a welcome email.") + "</p>"
# end if
help += "<p>" + __("Remember to click the Add New User button at the bottom of this screen when you are finished.") + "</p>"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": help}))
get_current_screen().add_help_tab(Array({"id": "user-roles", "title": __("User Roles"), "content": "<p>" + __("Here is a basic overview of the different user roles and the permissions associated with each one:") + "</p>" + "<ul>" + "<li>" + __("Subscribers can read comments/comment/receive newsletters, etc. but cannot create regular site content.") + "</li>" + "<li>" + __("Contributors can write and manage their posts but not publish posts or upload media files.") + "</li>" + "<li>" + __("Authors can publish and manage their own posts, and are able to upload files.") + "</li>" + "<li>" + __("Editors can publish posts, manage posts as well as manage other people&#8217;s posts, etc.") + "</li>" + "<li>" + __("Administrators have access to all the administration features.") + "</li>" + "</ul>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/users-add-new-screen/\">Documentation on Adding New Users</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
wp_enqueue_script("wp-ajax-response")
wp_enqueue_script("user-profile")
#// 
#// Filters whether to enable user auto-complete for non-super admins in Multisite.
#// 
#// @since 3.4.0
#// 
#// @param bool $enable Whether to enable auto-complete for non-super admins. Default false.
#//
if is_multisite() and current_user_can("promote_users") and (not wp_is_large_network("users")) and current_user_can("manage_network_users") or apply_filters("autocomplete_users_for_site_admins", False):
    wp_enqueue_script("user-suggest")
# end if
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
if (php_isset(lambda : PHP_REQUEST["update"])):
    messages = Array()
    if is_multisite():
        edit_link = ""
        if (php_isset(lambda : PHP_REQUEST["user_id"])):
            user_id_new = absint(PHP_REQUEST["user_id"])
            if user_id_new:
                edit_link = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user_id_new)))
            # end if
        # end if
        for case in Switch(PHP_REQUEST["update"]):
            if case("newuserconfirmation"):
                messages[-1] = __("Invitation email sent to new user. A confirmation link must be clicked before their account is created.")
                break
            # end if
            if case("add"):
                messages[-1] = __("Invitation email sent to user. A confirmation link must be clicked for them to be added to your site.")
                break
            # end if
            if case("addnoconfirmation"):
                message = __("User has been added to your site.")
                if edit_link:
                    message += php_sprintf(" <a href=\"%s\">%s</a>", edit_link, __("Edit user"))
                # end if
                messages[-1] = message
                break
            # end if
            if case("addexisting"):
                messages[-1] = __("That user is already a member of this site.")
                break
            # end if
            if case("could_not_add"):
                add_user_errors = php_new_class("WP_Error", lambda : WP_Error("could_not_add", __("That user could not be added to this site.")))
                break
            # end if
            if case("created_could_not_add"):
                add_user_errors = php_new_class("WP_Error", lambda : WP_Error("created_could_not_add", __("User has been created, but could not be added to this site.")))
                break
            # end if
            if case("does_not_exist"):
                add_user_errors = php_new_class("WP_Error", lambda : WP_Error("does_not_exist", __("The requested user does not exist.")))
                break
            # end if
            if case("enter_email"):
                add_user_errors = php_new_class("WP_Error", lambda : WP_Error("enter_email", __("Please enter a valid email address.")))
                break
            # end if
        # end for
    else:
        if "add" == PHP_REQUEST["update"]:
            messages[-1] = __("User added.")
        # end if
    # end if
# end if
php_print("<div class=\"wrap\">\n<h1 id=\"add-new-user\">\n")
if current_user_can("create_users"):
    _e("Add New User")
elif current_user_can("promote_users"):
    _e("Add Existing User")
# end if
php_print("</h1>\n\n")
if (php_isset(lambda : errors)) and is_wp_error(errors):
    php_print(" <div class=\"error\">\n     <ul>\n      ")
    for err in errors.get_error_messages():
        php_print(str("<li>") + str(err) + str("</li>\n"))
    # end for
    php_print("     </ul>\n </div>\n    ")
# end if
if (not php_empty(lambda : messages)):
    for msg in messages:
        php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + msg + "</p></div>")
    # end for
# end if
php_print("\n")
if (php_isset(lambda : add_user_errors)) and is_wp_error(add_user_errors):
    php_print(" <div class=\"error\">\n     ")
    for message in add_user_errors.get_error_messages():
        php_print(str("<p>") + str(message) + str("</p>"))
    # end for
    php_print(" </div>\n")
# end if
php_print("<div id=\"ajax-response\"></div>\n\n")
if is_multisite() and current_user_can("promote_users"):
    if do_both:
        php_print("<h2 id=\"add-existing-user\">" + __("Add Existing User") + "</h2>")
    # end if
    if (not current_user_can("manage_network_users")):
        php_print("<p>" + __("Enter the email address of an existing user on this network to invite them to this site. That person will be sent an email asking them to confirm the invite.") + "</p>")
        label = __("Email")
        type = "email"
    else:
        php_print("<p>" + __("Enter the email address or username of an existing user on this network to invite them to this site. That person will be sent an email asking them to confirm the invite.") + "</p>")
        label = __("Email or Username")
        type = "text"
    # end if
    php_print("<form method=\"post\" name=\"adduser\" id=\"adduser\" class=\"validate\" novalidate=\"novalidate\"\n ")
    #// 
    #// Fires inside the adduser form tag.
    #// 
    #// @since 3.0.0
    #//
    do_action("user_new_form_tag")
    php_print(">\n<input name=\"action\" type=\"hidden\" value=\"adduser\" />\n ")
    wp_nonce_field("add-user", "_wpnonce_add-user")
    php_print("""
    <table class=\"form-table\" role=\"presentation\">
    <tr class=\"form-field form-required\">
    <th scope=\"row\"><label for=\"adduser-email\">""")
    php_print(label)
    php_print("</label></th>\n      <td><input name=\"email\" type=\"")
    php_print(type)
    php_print("""\" id=\"adduser-email\" class=\"wp-suggest-user\" value=\"\" /></td>
    </tr>
    <tr class=\"form-field\">
    <th scope=\"row\"><label for=\"adduser-role\">""")
    _e("Role")
    php_print("</label></th>\n      <td><select name=\"role\" id=\"adduser-role\">\n            ")
    wp_dropdown_roles(get_option("default_role"))
    php_print("""           </select>
    </td>
    </tr>
    """)
    if current_user_can("manage_network_users"):
        php_print(" <tr>\n      <th scope=\"row\">")
        _e("Skip Confirmation Email")
        php_print("""</th>
        <td>
        <input type=\"checkbox\" name=\"noconfirmation\" id=\"adduser-noconfirmation\" value=\"1\" />
        <label for=\"adduser-noconfirmation\">""")
        _e("Add the user without sending an email that requires their confirmation.")
        php_print("""</label>
        </td>
        </tr>
        """)
    # end if
    php_print("</table>\n   ")
    #// 
    #// Fires at the end of the new user form.
    #// 
    #// Passes a contextual string to make both types of new user forms
    #// uniquely targetable. Contexts are 'add-existing-user' (Multisite),
    #// and 'add-new-user' (single site and network admin).
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $type A contextual string specifying which type of new user form the hook follows.
    #//
    do_action("user_new_form", "add-existing-user")
    php_print(" ")
    submit_button(__("Add Existing User"), "primary", "adduser", True, Array({"id": "addusersub"}))
    php_print("</form>\n    ")
# end if
#// End if is_multisite().
if current_user_can("create_users"):
    if do_both:
        php_print("<h2 id=\"create-new-user\">" + __("Add New User") + "</h2>")
    # end if
    php_print("<p>")
    _e("Create a brand new user and add them to this site.")
    php_print("</p>\n<form method=\"post\" name=\"createuser\" id=\"createuser\" class=\"validate\" novalidate=\"novalidate\"\n ")
    #// This action is documented in wp-admin/user-new.php
    do_action("user_new_form_tag")
    php_print(">\n<input name=\"action\" type=\"hidden\" value=\"createuser\" />\n  ")
    wp_nonce_field("create-user", "_wpnonce_create-user")
    php_print(" ")
    #// Load up the passed data, else set to a default.
    creating = (php_isset(lambda : PHP_POST["createuser"]))
    new_user_login = wp_unslash(PHP_POST["user_login"]) if creating and (php_isset(lambda : PHP_POST["user_login"])) else ""
    new_user_firstname = wp_unslash(PHP_POST["first_name"]) if creating and (php_isset(lambda : PHP_POST["first_name"])) else ""
    new_user_lastname = wp_unslash(PHP_POST["last_name"]) if creating and (php_isset(lambda : PHP_POST["last_name"])) else ""
    new_user_email = wp_unslash(PHP_POST["email"]) if creating and (php_isset(lambda : PHP_POST["email"])) else ""
    new_user_uri = wp_unslash(PHP_POST["url"]) if creating and (php_isset(lambda : PHP_POST["url"])) else ""
    new_user_role = wp_unslash(PHP_POST["role"]) if creating and (php_isset(lambda : PHP_POST["role"])) else ""
    new_user_send_notification = False if creating and (not (php_isset(lambda : PHP_POST["send_user_notification"]))) else True
    new_user_ignore_pass = wp_unslash(PHP_POST["noconfirmation"]) if creating and (php_isset(lambda : PHP_POST["noconfirmation"])) else ""
    php_print("<table class=\"form-table\" role=\"presentation\">\n <tr class=\"form-field form-required\">\n       <th scope=\"row\"><label for=\"user_login\">")
    _e("Username")
    php_print(" <span class=\"description\">")
    _e("(required)")
    php_print("</span></label></th>\n       <td><input name=\"user_login\" type=\"text\" id=\"user_login\" value=\"")
    php_print(esc_attr(new_user_login))
    php_print("""\" aria-required=\"true\" autocapitalize=\"none\" autocorrect=\"off\" maxlength=\"60\" /></td>
    </tr>
    <tr class=\"form-field form-required\">
    <th scope=\"row\"><label for=\"email\">""")
    _e("Email")
    php_print(" <span class=\"description\">")
    _e("(required)")
    php_print("</span></label></th>\n       <td><input name=\"email\" type=\"email\" id=\"email\" value=\"")
    php_print(esc_attr(new_user_email))
    php_print("\" /></td>\n </tr>\n ")
    if (not is_multisite()):
        php_print(" <tr class=\"form-field\">\n     <th scope=\"row\"><label for=\"first_name\">")
        _e("First Name")
        php_print(" </label></th>\n     <td><input name=\"first_name\" type=\"text\" id=\"first_name\" value=\"")
        php_print(esc_attr(new_user_firstname))
        php_print("""\" /></td>
        </tr>
        <tr class=\"form-field\">
        <th scope=\"row\"><label for=\"last_name\">""")
        _e("Last Name")
        php_print(" </label></th>\n     <td><input name=\"last_name\" type=\"text\" id=\"last_name\" value=\"")
        php_print(esc_attr(new_user_lastname))
        php_print("""\" /></td>
        </tr>
        <tr class=\"form-field\">
        <th scope=\"row\"><label for=\"url\">""")
        _e("Website")
        php_print("</label></th>\n      <td><input name=\"url\" type=\"url\" id=\"url\" class=\"code\" value=\"")
        php_print(esc_attr(new_user_uri))
        php_print("""\" /></td>
        </tr>
        <tr class=\"form-field form-required user-pass1-wrap\">
        <th scope=\"row\">
        <label for=\"pass1\">
        """)
        _e("Password")
        php_print("             <span class=\"description hide-if-js\">")
        _e("(required)")
        php_print("""</span>
        </label>
        </th>
        <td>
        <input class=\"hidden\" value=\" \" /><!-- #24364 workaround -->
        <button type=\"button\" class=\"button wp-generate-pw hide-if-no-js\">""")
        _e("Show password")
        php_print("</button>\n          <div class=\"wp-pwd hide-if-js\">\n             ")
        initial_password = wp_generate_password(24)
        php_print("             <span class=\"password-input-wrapper\">\n                   <input type=\"password\" name=\"pass1\" id=\"pass1\" class=\"regular-text\" autocomplete=\"off\" data-reveal=\"1\" data-pw=\"")
        php_print(esc_attr(initial_password))
        php_print("\" aria-describedby=\"pass-strength-result\" />\n                </span>\n               <button type=\"button\" class=\"button wp-hide-pw hide-if-no-js\" data-toggle=\"0\" aria-label=\"")
        esc_attr_e("Hide password")
        php_print("\">\n                    <span class=\"dashicons dashicons-hidden\" aria-hidden=\"true\"></span>\n                   <span class=\"text\">")
        _e("Hide")
        php_print("</span>\n                </button>\n             <button type=\"button\" class=\"button wp-cancel-pw hide-if-no-js\" data-toggle=\"0\" aria-label=\"")
        esc_attr_e("Cancel password change")
        php_print("\">\n                    <span class=\"dashicons dashicons-no\" aria-hidden=\"true\"></span>\n                   <span class=\"text\">")
        _e("Cancel")
        php_print("""</span>
        </button>
        <div style=\"display:none\" id=\"pass-strength-result\" aria-live=\"polite\"></div>
        </div>
        </td>
        </tr>
        <tr class=\"form-field form-required user-pass2-wrap hide-if-js\">
        <th scope=\"row\"><label for=\"pass2\">""")
        _e("Repeat Password")
        php_print(" <span class=\"description\">")
        _e("(required)")
        php_print("""</span></label></th>
        <td>
        <input name=\"pass2\" type=\"password\" id=\"pass2\" autocomplete=\"off\" />
        </td>
        </tr>
        <tr class=\"pw-weak\">
        <th>""")
        _e("Confirm Password")
        php_print("""</th>
        <td>
        <label>
        <input type=\"checkbox\" name=\"pw_weak\" class=\"pw-checkbox\" />
        """)
        _e("Confirm use of weak password")
        php_print("""           </label>
        </td>
        </tr>
        <tr>
        <th scope=\"row\">""")
        _e("Send User Notification")
        php_print("</th>\n      <td>\n          <input type=\"checkbox\" name=\"send_user_notification\" id=\"send_user_notification\" value=\"1\" ")
        checked(new_user_send_notification)
        php_print(" />\n            <label for=\"send_user_notification\">")
        _e("Send the new user an email about their account.")
        php_print("""</label>
        </td>
        </tr>
        """)
    # end if
    pass
    php_print(" <tr class=\"form-field\">\n     <th scope=\"row\"><label for=\"role\">")
    _e("Role")
    php_print("</label></th>\n      <td><select name=\"role\" id=\"role\">\n            ")
    if (not new_user_role):
        new_user_role = current_role if (not php_empty(lambda : current_role)) else get_option("default_role")
    # end if
    wp_dropdown_roles(new_user_role)
    php_print("""           </select>
    </td>
    </tr>
    """)
    if is_multisite() and current_user_can("manage_network_users"):
        php_print(" <tr>\n      <th scope=\"row\">")
        _e("Skip Confirmation Email")
        php_print("</th>\n      <td>\n          <input type=\"checkbox\" name=\"noconfirmation\" id=\"noconfirmation\" value=\"1\" ")
        checked(new_user_ignore_pass)
        php_print(" />\n            <label for=\"noconfirmation\">")
        _e("Add the user without sending an email that requires their confirmation.")
        php_print("""</label>
        </td>
        </tr>
        """)
    # end if
    php_print("</table>\n\n ")
    #// This action is documented in wp-admin/user-new.php
    do_action("user_new_form", "add-new-user")
    php_print("\n   ")
    submit_button(__("Add New User"), "primary", "createuser", True, Array({"id": "createusersub"}))
    php_print("\n</form>\n")
# end if
pass
php_print("</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
