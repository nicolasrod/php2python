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
#// WordPress user administration API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Creates a new user from the "Users" form using $_POST information.
#// 
#// @since 2.0.0
#// 
#// @return int|WP_Error WP_Error or User ID.
#//
def add_user(*args_):
    
    return edit_user()
# end def add_user
#// 
#// Edit user settings based on contents of $_POST
#// 
#// Used on user-edit.php and profile.php to manage and process user options, passwords etc.
#// 
#// @since 2.0.0
#// 
#// @param int $user_id Optional. User ID.
#// @return int|WP_Error user id of the updated user.
#//
def edit_user(user_id=0, *args_):
    
    wp_roles = wp_roles()
    user = php_new_class("stdClass", lambda : stdClass())
    user_id = php_int(user_id)
    if user_id:
        update = True
        user.ID = user_id
        userdata = get_userdata(user_id)
        user.user_login = wp_slash(userdata.user_login)
    else:
        update = False
    # end if
    if (not update) and (php_isset(lambda : PHP_POST["user_login"])):
        user.user_login = sanitize_user(wp_unslash(PHP_POST["user_login"]), True)
    # end if
    pass1 = ""
    pass2 = ""
    if (php_isset(lambda : PHP_POST["pass1"])):
        pass1 = PHP_POST["pass1"]
    # end if
    if (php_isset(lambda : PHP_POST["pass2"])):
        pass2 = PHP_POST["pass2"]
    # end if
    if (php_isset(lambda : PHP_POST["role"])) and current_user_can("promote_users") and (not user_id) or current_user_can("promote_user", user_id):
        new_role = sanitize_text_field(PHP_POST["role"])
        #// If the new role isn't editable by the logged-in user die with error.
        editable_roles = get_editable_roles()
        if (not php_empty(lambda : new_role)) and php_empty(lambda : editable_roles[new_role]):
            wp_die(__("Sorry, you are not allowed to give users that role."), 403)
        # end if
        potential_role = wp_roles.role_objects[new_role] if (php_isset(lambda : wp_roles.role_objects[new_role])) else False
        #// 
        #// Don't let anyone with 'promote_users' edit their own role to something without it.
        #// Multisite super admins can freely edit their roles, they possess all caps.
        #//
        if is_multisite() and current_user_can("manage_network_users") or get_current_user_id() != user_id or potential_role and potential_role.has_cap("promote_users"):
            user.role = new_role
        # end if
    # end if
    if (php_isset(lambda : PHP_POST["email"])):
        user.user_email = sanitize_text_field(wp_unslash(PHP_POST["email"]))
    # end if
    if (php_isset(lambda : PHP_POST["url"])):
        if php_empty(lambda : PHP_POST["url"]) or "http://" == PHP_POST["url"]:
            user.user_url = ""
        else:
            user.user_url = esc_url_raw(PHP_POST["url"])
            protocols = php_implode("|", php_array_map("preg_quote", wp_allowed_protocols()))
            user.user_url = user.user_url if php_preg_match("/^(" + protocols + "):/is", user.user_url) else "http://" + user.user_url
        # end if
    # end if
    if (php_isset(lambda : PHP_POST["first_name"])):
        user.first_name = sanitize_text_field(PHP_POST["first_name"])
    # end if
    if (php_isset(lambda : PHP_POST["last_name"])):
        user.last_name = sanitize_text_field(PHP_POST["last_name"])
    # end if
    if (php_isset(lambda : PHP_POST["nickname"])):
        user.nickname = sanitize_text_field(PHP_POST["nickname"])
    # end if
    if (php_isset(lambda : PHP_POST["display_name"])):
        user.display_name = sanitize_text_field(PHP_POST["display_name"])
    # end if
    if (php_isset(lambda : PHP_POST["description"])):
        user.description = php_trim(PHP_POST["description"])
    # end if
    for method,name in wp_get_user_contact_methods(user):
        if (php_isset(lambda : PHP_POST[method])):
            user.method = sanitize_text_field(PHP_POST[method])
        # end if
    # end for
    if update:
        user.rich_editing = "false" if (php_isset(lambda : PHP_POST["rich_editing"])) and "false" == PHP_POST["rich_editing"] else "true"
        user.syntax_highlighting = "false" if (php_isset(lambda : PHP_POST["syntax_highlighting"])) and "false" == PHP_POST["syntax_highlighting"] else "true"
        user.admin_color = sanitize_text_field(PHP_POST["admin_color"]) if (php_isset(lambda : PHP_POST["admin_color"])) else "fresh"
        user.show_admin_bar_front = "true" if (php_isset(lambda : PHP_POST["admin_bar_front"])) else "false"
        user.locale = ""
        if (php_isset(lambda : PHP_POST["locale"])):
            locale = sanitize_text_field(PHP_POST["locale"])
            if "site-default" == locale:
                locale = ""
            elif "" == locale:
                locale = "en_US"
            elif (not php_in_array(locale, get_available_languages(), True)):
                locale = ""
            # end if
            user.locale = locale
        # end if
    # end if
    user.comment_shortcuts = "true" if (php_isset(lambda : PHP_POST["comment_shortcuts"])) and "true" == PHP_POST["comment_shortcuts"] else ""
    user.use_ssl = 0
    if (not php_empty(lambda : PHP_POST["use_ssl"])):
        user.use_ssl = 1
    # end if
    errors = php_new_class("WP_Error", lambda : WP_Error())
    #// checking that username has been typed
    if "" == user.user_login:
        errors.add("user_login", __("<strong>Error</strong>: Please enter a username."))
    # end if
    #// checking that nickname has been typed
    if update and php_empty(lambda : user.nickname):
        errors.add("nickname", __("<strong>Error</strong>: Please enter a nickname."))
    # end if
    #// 
    #// Fires before the password and confirm password fields are checked for congruity.
    #// 
    #// @since 1.5.1
    #// 
    #// @param string $user_login The username.
    #// @param string $pass1     The password (passed by reference).
    #// @param string $pass2     The confirmed password (passed by reference).
    #//
    do_action_ref_array("check_passwords", Array(user.user_login, pass1, pass2))
    #// Check for blank password when adding a user.
    if (not update) and php_empty(lambda : pass1):
        errors.add("pass", __("<strong>Error</strong>: Please enter a password."), Array({"form-field": "pass1"}))
    # end if
    #// Check for "\" in password.
    if False != php_strpos(wp_unslash(pass1), "\\"):
        errors.add("pass", __("<strong>Error</strong>: Passwords may not contain the character \"\\\"."), Array({"form-field": "pass1"}))
    # end if
    #// Checking the password has been typed twice the same.
    if update or (not php_empty(lambda : pass1)) and pass1 != pass2:
        errors.add("pass", __("<strong>Error</strong>: Please enter the same password in both password fields."), Array({"form-field": "pass1"}))
    # end if
    if (not php_empty(lambda : pass1)):
        user.user_pass = pass1
    # end if
    if (not update) and (php_isset(lambda : PHP_POST["user_login"])) and (not validate_username(PHP_POST["user_login"])):
        errors.add("user_login", __("<strong>Error</strong>: This username is invalid because it uses illegal characters. Please enter a valid username."))
    # end if
    if (not update) and username_exists(user.user_login):
        errors.add("user_login", __("<strong>Error</strong>: This username is already registered. Please choose another one."))
    # end if
    #// This filter is documented in wp-includes/user.php
    illegal_logins = apply_filters("illegal_user_logins", Array())
    if php_in_array(php_strtolower(user.user_login), php_array_map("strtolower", illegal_logins), True):
        errors.add("invalid_username", __("<strong>Error</strong>: Sorry, that username is not allowed."))
    # end if
    #// checking email address
    if php_empty(lambda : user.user_email):
        errors.add("empty_email", __("<strong>Error</strong>: Please enter an email address."), Array({"form-field": "email"}))
    elif (not is_email(user.user_email)):
        errors.add("invalid_email", __("<strong>Error</strong>: The email address isn&#8217;t correct."), Array({"form-field": "email"}))
    else:
        owner_id = email_exists(user.user_email)
        if owner_id and (not update) or owner_id != user.ID:
            errors.add("email_exists", __("<strong>Error</strong>: This email is already registered, please choose another one."), Array({"form-field": "email"}))
        # end if
    # end if
    #// 
    #// Fires before user profile update errors are returned.
    #// 
    #// @since 2.8.0
    #// 
    #// @param WP_Error $errors WP_Error object (passed by reference).
    #// @param bool     $update  Whether this is a user update.
    #// @param stdClass $user   User object (passed by reference).
    #//
    do_action_ref_array("user_profile_update_errors", Array(errors, update, user))
    if errors.has_errors():
        return errors
    # end if
    if update:
        user_id = wp_update_user(user)
    else:
        user_id = wp_insert_user(user)
        notify = "both" if (php_isset(lambda : PHP_POST["send_user_notification"])) else "admin"
        #// 
        #// Fires after a new user has been created.
        #// 
        #// @since 4.4.0
        #// 
        #// @param int    $user_id ID of the newly created user.
        #// @param string $notify  Type of notification that should happen. See wp_send_new_user_notifications()
        #// for more information on possible values.
        #//
        do_action("edit_user_created_user", user_id, notify)
    # end if
    return user_id
# end def edit_user
#// 
#// Fetch a filtered list of user roles that the current user is
#// allowed to edit.
#// 
#// Simple function whose main purpose is to allow filtering of the
#// list of roles in the $wp_roles object so that plugins can remove
#// inappropriate ones depending on the situation or user making edits.
#// Specifically because without filtering anyone with the edit_users
#// capability can edit others to be administrators, even if they are
#// only editors or authors. This filter allows admins to delegate
#// user management.
#// 
#// @since 2.8.0
#// 
#// @return array[] Array of arrays containing role information.
#//
def get_editable_roles(*args_):
    
    all_roles = wp_roles().roles
    #// 
    #// Filters the list of editable roles.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array[] $all_roles Array of arrays containing role information.
    #//
    editable_roles = apply_filters("editable_roles", all_roles)
    return editable_roles
# end def get_editable_roles
#// 
#// Retrieve user data and filter it.
#// 
#// @since 2.0.5
#// 
#// @param int $user_id User ID.
#// @return WP_User|bool WP_User object on success, false on failure.
#//
def get_user_to_edit(user_id=None, *args_):
    
    user = get_userdata(user_id)
    if user:
        user.filter = "edit"
    # end if
    return user
# end def get_user_to_edit
#// 
#// Retrieve the user's drafts.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $user_id User ID.
#// @return array
#//
def get_users_drafts(user_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    query = wpdb.prepare(str("SELECT ID, post_title FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'post' AND post_status = 'draft' AND post_author = %d ORDER BY post_modified DESC"), user_id)
    #// 
    #// Filters the user's drafts query string.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $query The user's drafts query string.
    #//
    query = apply_filters("get_users_drafts", query)
    return wpdb.get_results(query)
# end def get_users_drafts
#// 
#// Remove user and optionally reassign posts and links to another user.
#// 
#// If the $reassign parameter is not assigned to a User ID, then all posts will
#// be deleted of that user. The action {@see 'delete_user'} that is passed the User ID
#// being deleted will be run after the posts are either reassigned or deleted.
#// The user meta will also be deleted that are for that User ID.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $id User ID.
#// @param int $reassign Optional. Reassign posts and links to new User ID.
#// @return bool True when finished.
#//
def wp_delete_user(id=None, reassign=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not php_is_numeric(id)):
        return False
    # end if
    id = php_int(id)
    user = php_new_class("WP_User", lambda : WP_User(id))
    if (not user.exists()):
        return False
    # end if
    #// Normalize $reassign to null or a user ID. 'novalue' was an older default.
    if "novalue" == reassign:
        reassign = None
    elif None != reassign:
        reassign = php_int(reassign)
    # end if
    #// 
    #// Fires immediately before a user is deleted from the database.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int      $id       ID of the user to delete.
    #// @param int|null $reassign ID of the user to reassign posts and links to.
    #// Default null, for no reassignment.
    #//
    do_action("delete_user", id, reassign)
    if None == reassign:
        post_types_to_delete = Array()
        for post_type in get_post_types(Array(), "objects"):
            if post_type.delete_with_user:
                post_types_to_delete[-1] = post_type.name
            elif None == post_type.delete_with_user and post_type_supports(post_type.name, "author"):
                post_types_to_delete[-1] = post_type.name
            # end if
        # end for
        #// 
        #// Filters the list of post types to delete with a user.
        #// 
        #// @since 3.4.0
        #// 
        #// @param string[] $post_types_to_delete Array of post types to delete.
        #// @param int      $id                   User ID.
        #//
        post_types_to_delete = apply_filters("post_types_to_delete_with_user", post_types_to_delete, id)
        post_types_to_delete = php_implode("', '", post_types_to_delete)
        post_ids = wpdb.get_col(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_author = %d AND post_type IN ('") + str(post_types_to_delete) + str("')"), id))
        if post_ids:
            for post_id in post_ids:
                wp_delete_post(post_id)
            # end for
        # end if
        #// Clean links.
        link_ids = wpdb.get_col(wpdb.prepare(str("SELECT link_id FROM ") + str(wpdb.links) + str(" WHERE link_owner = %d"), id))
        if link_ids:
            for link_id in link_ids:
                wp_delete_link(link_id)
            # end for
        # end if
    else:
        post_ids = wpdb.get_col(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_author = %d"), id))
        wpdb.update(wpdb.posts, Array({"post_author": reassign}), Array({"post_author": id}))
        if (not php_empty(lambda : post_ids)):
            for post_id in post_ids:
                clean_post_cache(post_id)
            # end for
        # end if
        link_ids = wpdb.get_col(wpdb.prepare(str("SELECT link_id FROM ") + str(wpdb.links) + str(" WHERE link_owner = %d"), id))
        wpdb.update(wpdb.links, Array({"link_owner": reassign}), Array({"link_owner": id}))
        if (not php_empty(lambda : link_ids)):
            for link_id in link_ids:
                clean_bookmark_cache(link_id)
            # end for
        # end if
    # end if
    #// FINALLY, delete user.
    if is_multisite():
        remove_user_from_blog(id, get_current_blog_id())
    else:
        meta = wpdb.get_col(wpdb.prepare(str("SELECT umeta_id FROM ") + str(wpdb.usermeta) + str(" WHERE user_id = %d"), id))
        for mid in meta:
            delete_metadata_by_mid("user", mid)
        # end for
        wpdb.delete(wpdb.users, Array({"ID": id}))
    # end if
    clean_user_cache(user)
    #// 
    #// Fires immediately after a user is deleted from the database.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int      $id       ID of the deleted user.
    #// @param int|null $reassign ID of the user to reassign posts and links to.
    #// Default null, for no reassignment.
    #//
    do_action("deleted_user", id, reassign)
    return True
# end def wp_delete_user
#// 
#// Remove all capabilities from user.
#// 
#// @since 2.1.0
#// 
#// @param int $id User ID.
#//
def wp_revoke_user(id=None, *args_):
    
    id = php_int(id)
    user = php_new_class("WP_User", lambda : WP_User(id))
    user.remove_all_caps()
# end def wp_revoke_user
#// 
#// @since 2.8.0
#// 
#// @global int $user_ID
#// 
#// @param false $errors Deprecated.
#//
def default_password_nag_handler(errors=False, *args_):
    
    global user_ID
    php_check_if_defined("user_ID")
    #// Short-circuit it.
    if (not get_user_option("default_password_nag")):
        return
    # end if
    #// get_user_setting() = JS-saved UI setting. Else no-js-fallback code.
    if "hide" == get_user_setting("default_password_nag") or (php_isset(lambda : PHP_REQUEST["default_password_nag"])) and "0" == PHP_REQUEST["default_password_nag"]:
        delete_user_setting("default_password_nag")
        update_user_option(user_ID, "default_password_nag", False, True)
    # end if
# end def default_password_nag_handler
#// 
#// @since 2.8.0
#// 
#// @param int    $user_ID
#// @param object $old_data
#//
def default_password_nag_edit_user(user_ID=None, old_data=None, *args_):
    
    #// Short-circuit it.
    if (not get_user_option("default_password_nag", user_ID)):
        return
    # end if
    new_data = get_userdata(user_ID)
    #// Remove the nag if the password has been changed.
    if new_data.user_pass != old_data.user_pass:
        delete_user_setting("default_password_nag")
        update_user_option(user_ID, "default_password_nag", False, True)
    # end if
# end def default_password_nag_edit_user
#// 
#// @since 2.8.0
#// 
#// @global string $pagenow
#//
def default_password_nag(*args_):
    
    global pagenow
    php_check_if_defined("pagenow")
    #// Short-circuit it.
    if "profile.php" == pagenow or (not get_user_option("default_password_nag")):
        return
    # end if
    php_print("<div class=\"error default-password-nag\">")
    php_print("<p>")
    php_print("<strong>" + __("Notice:") + "</strong> ")
    _e("You&rsquo;re using the auto-generated password for your account. Would you like to change it?")
    php_print("</p><p>")
    printf("<a href=\"%s\">" + __("Yes, take me to my profile page") + "</a> | ", get_edit_profile_url() + "#password")
    printf("<a href=\"%s\" id=\"default-password-nag-no\">" + __("No thanks, do not remind me again") + "</a>", "?default_password_nag=0")
    php_print("</p></div>")
# end def default_password_nag
#// 
#// @since 3.5.0
#// @access private
#//
def delete_users_add_js(*args_):
    
    php_print("""<script>
    jQuery(document).ready( function($) {
    var submit = $('#submit').prop('disabled', true);
    $('input[name=\"delete_option\"]').one('change', function() {
    submit.prop('disabled', false);
    });
    $('#reassign_user').focus( function() {
    $('#delete_option1').prop('checked', true).trigger('change');
    });
    });
    </script>
    """)
# end def delete_users_add_js
#// 
#// Optional SSL preference that can be turned on by hooking to the 'personal_options' action.
#// 
#// See the {@see 'personal_options'} action.
#// 
#// @since 2.7.0
#// 
#// @param WP_User $user User data object.
#//
def use_ssl_preference(user=None, *args_):
    
    php_print(" <tr class=\"user-use-ssl-wrap\">\n      <th scope=\"row\">")
    _e("Use https")
    php_print("</th>\n      <td><label for=\"use_ssl\"><input name=\"use_ssl\" type=\"checkbox\" id=\"use_ssl\" value=\"1\" ")
    checked("1", user.use_ssl)
    php_print(" /> ")
    _e("Always use https when visiting the admin")
    php_print("</label></td>\n  </tr>\n ")
# end def use_ssl_preference
#// 
#// @since MU (3.0.0)
#// 
#// @param string $text
#// @return string
#//
def admin_created_user_email(text=None, *args_):
    
    roles = get_editable_roles()
    role = roles[PHP_REQUEST["role"]]
    return php_sprintf(__("""Hi,
    You've been invited to join '%1$s' at
    %2$s with the role of %3$s.
    If you do not want to join this site please ignore
    this email. This invitation will expire in a few days.
    Please click the following link to activate your user account:
    %%s"""), wp_specialchars_decode(get_bloginfo("name"), ENT_QUOTES), home_url(), wp_specialchars_decode(translate_user_role(role["name"])))
# end def admin_created_user_email
