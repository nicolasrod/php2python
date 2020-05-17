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
#// Edit user administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
wp_reset_vars(Array("action", "user_id", "wp_http_referer"))
user_id_ = php_int(user_id_)
current_user_ = wp_get_current_user()
if (not php_defined("IS_PROFILE_PAGE")):
    php_define("IS_PROFILE_PAGE", user_id_ == current_user_.ID)
# end if
if (not user_id_) and IS_PROFILE_PAGE:
    user_id_ = current_user_.ID
elif (not user_id_) and (not IS_PROFILE_PAGE):
    wp_die(__("Invalid user ID."))
elif (not get_userdata(user_id_)):
    wp_die(__("Invalid user ID."))
# end if
wp_enqueue_script("user-profile")
if IS_PROFILE_PAGE:
    title_ = __("Profile")
else:
    #// translators: %s: User's display name.
    title_ = __("Edit User %s")
# end if
if current_user_can("edit_users") and (not IS_PROFILE_PAGE):
    submenu_file_ = "users.php"
else:
    submenu_file_ = "profile.php"
# end if
if current_user_can("edit_users") and (not is_user_admin()):
    parent_file_ = "users.php"
else:
    parent_file_ = "profile.php"
# end if
profile_help_ = "<p>" + __("Your profile contains information about you (your &#8220;account&#8221;) as well as some personal options related to using WordPress.") + "</p>" + "<p>" + __("You can change your password, turn on keyboard shortcuts, change the color scheme of your WordPress administration screens, and turn off the WYSIWYG (Visual) editor, among other things. You can hide the Toolbar (formerly called the Admin Bar) from the front end of your site, however it cannot be disabled on the admin screens.") + "</p>" + "<p>" + __("You can select the language you wish to use while using the WordPress administration screen without affecting the language site visitors see.") + "</p>" + "<p>" + __("Your username cannot be changed, but you can use other fields to enter your real name or a nickname, and change which name to display on your posts.") + "</p>" + "<p>" + __("You can log out of other devices, such as your phone or a public computer, by clicking the Log Out Everywhere Else button.") + "</p>" + "<p>" + __("Required fields are indicated; the rest are optional. Profile information will only be displayed if your theme is set up to do so.") + "</p>" + "<p>" + __("Remember to click the Update Profile button when you are finished.") + "</p>"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": profile_help_}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/users-your-profile-screen/\">Documentation on User Profiles</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
wp_http_referer_ = remove_query_arg(Array("update", "delete_count", "user_id"), wp_http_referer_)
user_can_edit_ = current_user_can("edit_posts") or current_user_can("edit_pages")
#// 
#// Filters whether to allow administrators on Multisite to edit every user.
#// 
#// Enabling the user editing form via this filter also hinges on the user holding
#// the 'manage_network_users' cap, and the logged-in user not matching the user
#// profile open for editing.
#// 
#// The filter was introduced to replace the EDIT_ANY_USER constant.
#// 
#// @since 3.0.0
#// 
#// @param bool $allow Whether to allow editing of any user. Default true.
#//
if is_multisite() and (not current_user_can("manage_network_users")) and user_id_ != current_user_.ID and (not apply_filters("enable_edit_any_user_configuration", True)):
    wp_die(__("Sorry, you are not allowed to edit this user."))
# end if
#// Execute confirmed email change. See send_confirmation_on_profile_email().
if IS_PROFILE_PAGE and (php_isset(lambda : PHP_REQUEST["newuseremail"])) and current_user_.ID:
    new_email_ = get_user_meta(current_user_.ID, "_new_email", True)
    if new_email_ and hash_equals(new_email_["hash"], PHP_REQUEST["newuseremail"]):
        user_ = php_new_class("stdClass", lambda : stdClass())
        user_.ID = current_user_.ID
        user_.user_email = esc_html(php_trim(new_email_["newemail"]))
        if is_multisite() and wpdb_.get_var(wpdb_.prepare(str("SELECT user_login FROM ") + str(wpdb_.signups) + str(" WHERE user_login = %s"), current_user_.user_login)):
            wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.signups) + str(" SET user_email = %s WHERE user_login = %s"), user_.user_email, current_user_.user_login))
        # end if
        wp_update_user(user_)
        delete_user_meta(current_user_.ID, "_new_email")
        wp_redirect(add_query_arg(Array({"updated": "true"}), self_admin_url("profile.php")))
        php_exit(0)
    else:
        wp_redirect(add_query_arg(Array({"error": "new-email"}), self_admin_url("profile.php")))
    # end if
elif IS_PROFILE_PAGE and (not php_empty(lambda : PHP_REQUEST["dismiss"])) and current_user_.ID + "_new_email" == PHP_REQUEST["dismiss"]:
    check_admin_referer("dismiss-" + current_user_.ID + "_new_email")
    delete_user_meta(current_user_.ID, "_new_email")
    wp_redirect(add_query_arg(Array({"updated": "true"}), self_admin_url("profile.php")))
    php_exit(0)
# end if
for case in Switch(action_):
    if case("update"):
        check_admin_referer("update-user_" + user_id_)
        if (not current_user_can("edit_user", user_id_)):
            wp_die(__("Sorry, you are not allowed to edit this user."))
        # end if
        if IS_PROFILE_PAGE:
            #// 
            #// Fires before the page loads on the 'Your Profile' editing screen.
            #// 
            #// The action only fires if the current user is editing their own profile.
            #// 
            #// @since 2.0.0
            #// 
            #// @param int $user_id The user ID.
            #//
            do_action("personal_options_update", user_id_)
        else:
            #// 
            #// Fires before the page loads on the 'Edit User' screen.
            #// 
            #// @since 2.7.0
            #// 
            #// @param int $user_id The user ID.
            #//
            do_action("edit_user_profile_update", user_id_)
        # end if
        #// Update the email address in signups, if present.
        if is_multisite():
            user_ = get_userdata(user_id_)
            if user_.user_login and (php_isset(lambda : PHP_POST["email"])) and is_email(PHP_POST["email"]) and wpdb_.get_var(wpdb_.prepare(str("SELECT user_login FROM ") + str(wpdb_.signups) + str(" WHERE user_login = %s"), user_.user_login)):
                wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.signups) + str(" SET user_email = %s WHERE user_login = %s"), PHP_POST["email"], user_login_))
            # end if
        # end if
        #// Update the user.
        errors_ = edit_user(user_id_)
        #// Grant or revoke super admin status if requested.
        if is_multisite() and is_network_admin() and (not IS_PROFILE_PAGE) and current_user_can("manage_network_options") and (not (php_isset(lambda : super_admins_))) and php_empty(lambda : PHP_POST["super_admin"]) == is_super_admin(user_id_):
            revoke_super_admin(user_id_) if php_empty(lambda : PHP_POST["super_admin"]) else grant_super_admin(user_id_)
        # end if
        if (not is_wp_error(errors_)):
            redirect_ = add_query_arg("updated", True, get_edit_user_link(user_id_))
            if wp_http_referer_:
                redirect_ = add_query_arg("wp_http_referer", urlencode(wp_http_referer_), redirect_)
            # end if
            wp_redirect(redirect_)
            php_exit(0)
        # end if
    # end if
    if case():
        profileuser_ = get_user_to_edit(user_id_)
        if (not current_user_can("edit_user", user_id_)):
            wp_die(__("Sorry, you are not allowed to edit this user."))
        # end if
        title_ = php_sprintf(title_, profileuser_.display_name)
        sessions_ = WP_Session_Tokens.get_instance(profileuser_.ID)
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        php_print("\n       ")
        if (not IS_PROFILE_PAGE) and is_super_admin(profileuser_.ID) and current_user_can("manage_network_options"):
            php_print(" <div class=\"notice notice-info\"><p><strong>")
            _e("Important:")
            php_print("</strong> ")
            _e("This user has super admin privileges.")
            php_print("</p></div>\n")
        # end if
        php_print("     ")
        if (php_isset(lambda : PHP_REQUEST["updated"])):
            php_print("<div id=\"message\" class=\"updated notice is-dismissible\">\n           ")
            if IS_PROFILE_PAGE:
                php_print(" <p><strong>")
                _e("Profile updated.")
                php_print("</strong></p>\n  ")
            else:
                php_print(" <p><strong>")
                _e("User updated.")
                php_print("</strong></p>\n  ")
            # end if
            php_print("         ")
            if wp_http_referer_ and False == php_strpos(wp_http_referer_, "user-new.php") and (not IS_PROFILE_PAGE):
                php_print(" <p><a href=\"")
                php_print(esc_url(wp_validate_redirect(esc_url_raw(wp_http_referer_), self_admin_url("users.php"))))
                php_print("\">")
                _e("&larr; Back to Users")
                php_print("</a></p>\n   ")
            # end if
            php_print("</div>\n     ")
        # end if
        php_print("     ")
        if (php_isset(lambda : PHP_REQUEST["error"])):
            php_print("<div class=\"notice notice-error\">\n            ")
            if "new-email" == PHP_REQUEST["error"]:
                php_print(" <p>")
                _e("Error while saving the new email address. Please try again.")
                php_print("</p>\n   ")
            # end if
            php_print("</div>\n     ")
        # end if
        php_print("     ")
        if (php_isset(lambda : errors_)) and is_wp_error(errors_):
            php_print("<div class=\"error\"><p>")
            php_print(php_implode("</p>\n<p>", errors_.get_error_messages()))
            php_print("</p></div>\n     ")
        # end if
        php_print("""
        <div class=\"wrap\" id=\"profile-page\">
        <h1 class=\"wp-heading-inline\">
        """)
        php_print(esc_html(title_))
        php_print("</h1>\n\n        ")
        if (not IS_PROFILE_PAGE):
            if current_user_can("create_users"):
                php_print("     <a href=\"user-new.php\" class=\"page-title-action\">")
                php_print(esc_html_x("Add New", "user"))
                php_print("</a>\n   ")
            elif is_multisite() and current_user_can("promote_users"):
                php_print("     <a href=\"user-new.php\" class=\"page-title-action\">")
                php_print(esc_html_x("Add Existing", "user"))
                php_print("</a>\n               ")
            # end if
        # end if
        php_print("""
        <hr class=\"wp-header-end\">
        <form id=\"your-profile\" action=\"""")
        php_print(esc_url(self_admin_url("profile.php" if IS_PROFILE_PAGE else "user-edit.php")))
        php_print("\" method=\"post\" novalidate=\"novalidate\"\n       ")
        #// 
        #// Fires inside the your-profile form tag on the user editing screen.
        #// 
        #// @since 3.0.0
        #//
        do_action("user_edit_form_tag")
        php_print(" >\n     ")
        wp_nonce_field("update-user_" + user_id_)
        php_print("     ")
        if wp_http_referer_:
            php_print(" <input type=\"hidden\" name=\"wp_http_referer\" value=\"")
            php_print(esc_url(wp_http_referer_))
            php_print("\" />\n      ")
        # end if
        php_print("<p>\n<input type=\"hidden\" name=\"from\" value=\"profile\" />\n<input type=\"hidden\" name=\"checkuser_id\" value=\"")
        php_print(get_current_user_id())
        php_print("""\" />
        </p>
        <h2>""")
        _e("Personal Options")
        php_print("""</h2>
        <table class=\"form-table\" role=\"presentation\">
        """)
        if (not IS_PROFILE_PAGE and (not user_can_edit_)):
            php_print(" <tr class=\"user-rich-editing-wrap\">\n     <th scope=\"row\">")
            _e("Visual Editor")
            php_print("</th>\n      <td>\n          <label for=\"rich_editing\"><input name=\"rich_editing\" type=\"checkbox\" id=\"rich_editing\" value=\"false\" ")
            checked("false", profileuser_.rich_editing)
            php_print(" />\n                ")
            _e("Disable the visual editor when writing")
            php_print("""           </label>
            </td>
            </tr>
            """)
        # end if
        php_print("     ")
        show_syntax_highlighting_preference_ = user_can(profileuser_, "edit_theme_options") or user_can(profileuser_, "edit_plugins") or user_can(profileuser_, "edit_themes")
        php_print("\n       ")
        if show_syntax_highlighting_preference_:
            php_print(" <tr class=\"user-syntax-highlighting-wrap\">\n      <th scope=\"row\">")
            _e("Syntax Highlighting")
            php_print("</th>\n      <td>\n          <label for=\"syntax_highlighting\"><input name=\"syntax_highlighting\" type=\"checkbox\" id=\"syntax_highlighting\" value=\"false\" ")
            checked("false", profileuser_.syntax_highlighting)
            php_print(" />\n                ")
            _e("Disable syntax highlighting when editing code")
            php_print("""           </label>
            </td>
            </tr>
            """)
        # end if
        php_print("\n       ")
        if php_count(_wp_admin_css_colors_) > 1 and has_action("admin_color_scheme_picker"):
            php_print(" <tr class=\"user-admin-color-wrap\">\n      <th scope=\"row\">")
            _e("Admin Color Scheme")
            php_print("</th>\n      <td>\n          ")
            #// 
            #// Fires in the 'Admin Color Scheme' section of the user editing screen.
            #// 
            #// The section is only enabled if a callback is hooked to the action,
            #// and if there is more than one defined color scheme for the admin.
            #// 
            #// @since 3.0.0
            #// @since 3.8.1 Added `$user_id` parameter.
            #// 
            #// @param int $user_id The user ID.
            #//
            do_action("admin_color_scheme_picker", user_id_)
            php_print("     </td>\n </tr>\n     ")
        # end if
        pass
        php_print("\n       ")
        if (not IS_PROFILE_PAGE and (not user_can_edit_)):
            php_print(" <tr class=\"user-comment-shortcuts-wrap\">\n        <th scope=\"row\">")
            _e("Keyboard Shortcuts")
            php_print("""</th>
            <td>
            <label for=\"comment_shortcuts\">
            <input type=\"checkbox\" name=\"comment_shortcuts\" id=\"comment_shortcuts\" value=\"true\" """)
            checked("true", profileuser_.comment_shortcuts)
            php_print(" />\n                ")
            _e("Enable keyboard shortcuts for comment moderation.")
            php_print("         </label>\n          ")
            _e("<a href=\"https://wordpress.org/support/article/keyboard-shortcuts/\" target=\"_blank\">More information</a>")
            php_print("     </td>\n </tr>\n     ")
        # end if
        php_print("\n   <tr class=\"show-admin-bar user-admin-bar-front-wrap\">\n       <th scope=\"row\">")
        _e("Toolbar")
        php_print("""</th>
        <td>
        <label for=\"admin_bar_front\">
        <input name=\"admin_bar_front\" type=\"checkbox\" id=\"admin_bar_front\" value=\"1\"""")
        checked(_get_admin_bar_pref("front", profileuser_.ID))
        php_print(" />\n                ")
        _e("Show Toolbar when viewing site")
        php_print("""           </label><br />
        </td>
        </tr>
        """)
        languages_ = get_available_languages()
        if languages_:
            php_print(" <tr class=\"user-language-wrap\">\n     <th scope=\"row\">\n            ")
            pass
            php_print("         <label for=\"locale\">")
            _e("Language")
            php_print("""<span class=\"dashicons dashicons-translation\" aria-hidden=\"true\"></span></label>
            </th>
            <td>
            """)
            user_locale_ = profileuser_.locale
            if "en_US" == user_locale_:
                user_locale_ = ""
            elif "" == user_locale_ or (not php_in_array(user_locale_, languages_, True)):
                user_locale_ = "site-default"
            # end if
            wp_dropdown_languages(Array({"name": "locale", "id": "locale", "selected": user_locale_, "languages": languages_, "show_available_translations": False, "show_option_site_default": True}))
            php_print("     </td>\n </tr>\n         ")
        # end if
        php_print("\n       ")
        #// 
        #// Fires at the end of the 'Personal Options' settings table on the user editing screen.
        #// 
        #// @since 2.7.0
        #// 
        #// @param WP_User $profileuser The current WP_User object.
        #//
        do_action("personal_options", profileuser_)
        php_print("\n</table>\n     ")
        if IS_PROFILE_PAGE:
            #// 
            #// Fires after the 'Personal Options' settings table on the 'Your Profile' editing screen.
            #// 
            #// The action only fires if the current user is editing their own profile.
            #// 
            #// @since 2.0.0
            #// 
            #// @param WP_User $profileuser The current WP_User object.
            #//
            do_action("profile_personal_options", profileuser_)
        # end if
        php_print("\n<h2>")
        _e("Name")
        php_print("""</h2>
        <table class=\"form-table\" role=\"presentation\">
        <tr class=\"user-user-login-wrap\">
        <th><label for=\"user_login\">""")
        _e("Username")
        php_print("</label></th>\n      <td><input type=\"text\" name=\"user_login\" id=\"user_login\" value=\"")
        php_print(esc_attr(profileuser_.user_login))
        php_print("\" disabled=\"disabled\" class=\"regular-text\" /> <span class=\"description\">")
        _e("Usernames cannot be changed.")
        php_print("""</span></td>
        </tr>
        """)
        if (not IS_PROFILE_PAGE) and (not is_network_admin()) and current_user_can("promote_user", profileuser_.ID):
            php_print("<tr class=\"user-role-wrap\"><th><label for=\"role\">")
            _e("Role")
            php_print("</label></th>\n<td><select name=\"role\" id=\"role\">\n          ")
            #// Compare user role against currently editable roles.
            user_roles_ = php_array_intersect(php_array_values(profileuser_.roles), php_array_keys(get_editable_roles()))
            user_role_ = reset(user_roles_)
            #// Print the full list of roles with the primary one selected.
            wp_dropdown_roles(user_role_)
            #// Print the 'no role' option. Make it selected if the user has no role yet.
            if user_role_:
                php_print("<option value=\"\">" + __("&mdash; No role for this site &mdash;") + "</option>")
            else:
                php_print("<option value=\"\" selected=\"selected\">" + __("&mdash; No role for this site &mdash;") + "</option>")
            # end if
            php_print("</select></td></tr>\n            ")
        # end if
        #// End if ! IS_PROFILE_PAGE.
        if is_multisite() and is_network_admin() and (not IS_PROFILE_PAGE) and current_user_can("manage_network_options") and (not (php_isset(lambda : super_admins_))):
            php_print("<tr class=\"user-super-admin-wrap\"><th>")
            _e("Super Admin")
            php_print("</th>\n<td>\n            ")
            if 0 != strcasecmp(profileuser_.user_email, get_site_option("admin_email")) or (not is_super_admin(profileuser_.ID)):
                php_print("<p><label><input type=\"checkbox\" id=\"super_admin\" name=\"super_admin\"")
                checked(is_super_admin(profileuser_.ID))
                php_print(" /> ")
                _e("Grant this user super admin privileges for the Network.")
                php_print("</label></p>\n")
            else:
                php_print("<p>")
                _e("Super admin privileges cannot be removed because this user has the network admin email.")
                php_print("</p>\n")
            # end if
            php_print("</td></tr>\n     ")
        # end if
        php_print("\n<tr class=\"user-first-name-wrap\">\n  <th><label for=\"first_name\">")
        _e("First Name")
        php_print("</label></th>\n  <td><input type=\"text\" name=\"first_name\" id=\"first_name\" value=\"")
        php_print(esc_attr(profileuser_.first_name))
        php_print("""\" class=\"regular-text\" /></td>
        </tr>
        <tr class=\"user-last-name-wrap\">
        <th><label for=\"last_name\">""")
        _e("Last Name")
        php_print("</label></th>\n  <td><input type=\"text\" name=\"last_name\" id=\"last_name\" value=\"")
        php_print(esc_attr(profileuser_.last_name))
        php_print("""\" class=\"regular-text\" /></td>
        </tr>
        <tr class=\"user-nickname-wrap\">
        <th><label for=\"nickname\">""")
        _e("Nickname")
        php_print(" <span class=\"description\">")
        _e("(required)")
        php_print("</span></label></th>\n   <td><input type=\"text\" name=\"nickname\" id=\"nickname\" value=\"")
        php_print(esc_attr(profileuser_.nickname))
        php_print("""\" class=\"regular-text\" /></td>
        </tr>
        <tr class=\"user-display-name-wrap\">
        <th><label for=\"display_name\">""")
        _e("Display name publicly as")
        php_print("""</label></th>
        <td>
        <select name=\"display_name\" id=\"display_name\">
        """)
        public_display_ = Array()
        public_display_["display_nickname"] = profileuser_.nickname
        public_display_["display_username"] = profileuser_.user_login
        if (not php_empty(lambda : profileuser_.first_name)):
            public_display_["display_firstname"] = profileuser_.first_name
        # end if
        if (not php_empty(lambda : profileuser_.last_name)):
            public_display_["display_lastname"] = profileuser_.last_name
        # end if
        if (not php_empty(lambda : profileuser_.first_name)) and (not php_empty(lambda : profileuser_.last_name)):
            public_display_["display_firstlast"] = profileuser_.first_name + " " + profileuser_.last_name
            public_display_["display_lastfirst"] = profileuser_.last_name + " " + profileuser_.first_name
        # end if
        if (not php_in_array(profileuser_.display_name, public_display_)):
            #// Only add this if it isn't duplicated elsewhere.
            public_display_ = Array({"display_displayname": profileuser_.display_name}) + public_display_
        # end if
        public_display_ = php_array_map("trim", public_display_)
        public_display_ = array_unique(public_display_)
        for id_,item_ in public_display_:
            php_print("     <option ")
            selected(profileuser_.display_name, item_)
            php_print(">")
            php_print(item_)
            php_print("</option>\n          ")
        # end for
        php_print("""       </select>
        </td>
        </tr>
        </table>
        <h2>""")
        _e("Contact Info")
        php_print("""</h2>
        <table class=\"form-table\" role=\"presentation\">
        <tr class=\"user-email-wrap\">
        <th><label for=\"email\">""")
        _e("Email")
        php_print(" <span class=\"description\">")
        _e("(required)")
        php_print("</span></label></th>\n       <td><input type=\"email\" name=\"email\" id=\"email\" aria-describedby=\"email-description\" value=\"")
        php_print(esc_attr(profileuser_.user_email))
        php_print("\" class=\"regular-text ltr\" />\n       ")
        if profileuser_.ID == current_user_.ID:
            php_print("     <p class=\"description\" id=\"email-description\">\n            ")
            _e("If you change this, we will send you an email at your new address to confirm it. <strong>The new address will not become active until confirmed.</strong>")
            php_print("     </p>\n          ")
        # end if
        new_email_ = get_user_meta(current_user_.ID, "_new_email", True)
        if new_email_ and new_email_["newemail"] != current_user_.user_email and profileuser_.ID == current_user_.ID:
            php_print("     <div class=\"updated inline\">\n        <p>\n           ")
            printf(__("There is a pending change of your email to %s."), "<code>" + esc_html(new_email_["newemail"]) + "</code>")
            printf(" <a href=\"%1$s\">%2$s</a>", esc_url(wp_nonce_url(self_admin_url("profile.php?dismiss=" + current_user_.ID + "_new_email"), "dismiss-" + current_user_.ID + "_new_email")), __("Cancel"))
            php_print("     </p>\n      </div>\n        ")
        # end if
        php_print("""   </td>
        </tr>
        <tr class=\"user-url-wrap\">
        <th><label for=\"url\">""")
        _e("Website")
        php_print("</label></th>\n  <td><input type=\"url\" name=\"url\" id=\"url\" value=\"")
        php_print(esc_attr(profileuser_.user_url))
        php_print("""\" class=\"regular-text code\" /></td>
        </tr>
        """)
        for name_,desc_ in wp_get_user_contact_methods(profileuser_):
            php_print(" <tr class=\"user-")
            php_print(name_)
            php_print("-wrap\">\n<th><label for=\"")
            php_print(name_)
            php_print("\">\n            ")
            #// 
            #// Filters a user contactmethod label.
            #// 
            #// The dynamic portion of the filter hook, `$name`, refers to
            #// each of the keys in the contactmethods array.
            #// 
            #// @since 2.9.0
            #// 
            #// @param string $desc The translatable label for the contactmethod.
            #//
            php_print(apply_filters(str("user_") + str(name_) + str("_label"), desc_))
            php_print(" </label></th>\n <td><input type=\"text\" name=\"")
            php_print(name_)
            php_print("\" id=\"")
            php_print(name_)
            php_print("\" value=\"")
            php_print(esc_attr(profileuser_.name_))
            php_print("\" class=\"regular-text\" /></td>\n  </tr>\n         ")
        # end for
        php_print(" </table>\n\n    <h2>")
        _e("About Yourself") if IS_PROFILE_PAGE else _e("About the user")
        php_print("""</h2>
        <table class=\"form-table\" role=\"presentation\">
        <tr class=\"user-description-wrap\">
        <th><label for=\"description\">""")
        _e("Biographical Info")
        php_print("</label></th>\n  <td><textarea name=\"description\" id=\"description\" rows=\"5\" cols=\"30\">")
        php_print(profileuser_.description)
        pass
        php_print("</textarea>\n    <p class=\"description\">")
        _e("Share a little biographical information to fill out your profile. This may be shown publicly.")
        php_print("""</p></td>
        </tr>
        """)
        if get_option("show_avatars"):
            php_print("<tr class=\"user-profile-picture\">\n    <th>")
            _e("Profile Picture")
            php_print("</th>\n  <td>\n          ")
            php_print(get_avatar(user_id_))
            php_print("     <p class=\"description\">\n         ")
            if IS_PROFILE_PAGE:
                description_ = php_sprintf(__("<a href=\"%s\">You can change your profile picture on Gravatar</a>."), __("https://en.gravatar.com/"))
            else:
                description_ = ""
            # end if
            #// 
            #// Filters the user profile picture description displayed under the Gravatar.
            #// 
            #// @since 4.4.0
            #// @since 4.7.0 Added the `$profileuser` parameter.
            #// 
            #// @param string  $description The description that will be printed.
            #// @param WP_User $profileuser The current WP_User object.
            #//
            php_print(apply_filters("user_profile_picture_description", description_, profileuser_))
            php_print("""       </p>
            </td>
            </tr>
            """)
        # end if
        php_print("\n       ")
        #// 
        #// Filters the display of the password fields.
        #// 
        #// @since 1.5.1
        #// @since 2.8.0 Added the `$profileuser` parameter.
        #// @since 4.4.0 Now evaluated only in user-edit.php.
        #// 
        #// @param bool    $show        Whether to show the password fields. Default true.
        #// @param WP_User $profileuser User object for the current user to edit.
        #//
        show_password_fields_ = apply_filters("show_password_fields", True, profileuser_)
        if show_password_fields_:
            php_print(" </table>\n\n    <h2>")
            _e("Account Management")
            php_print("""</h2>
            <table class=\"form-table\" role=\"presentation\">
            <tr id=\"password\" class=\"user-pass1-wrap\">
            <th><label for=\"pass1\">""")
            _e("New Password")
            php_print("""</label></th>
            <td>
            <input class=\"hidden\" value=\" \" /><!-- #24364 workaround -->
            <button type=\"button\" class=\"button wp-generate-pw hide-if-no-js\">""")
            _e("Generate Password")
            php_print("""</button>
            <div class=\"wp-pwd hide-if-js\">
            <span class=\"password-input-wrapper\">
            <input type=\"password\" name=\"pass1\" id=\"pass1\" class=\"regular-text\" value=\"\" autocomplete=\"off\" data-pw=\"""")
            php_print(esc_attr(wp_generate_password(24)))
            php_print("\" aria-describedby=\"pass-strength-result\" />\n            </span>\n           <button type=\"button\" class=\"button wp-hide-pw hide-if-no-js\" data-toggle=\"0\" aria-label=\"")
            esc_attr_e("Hide password")
            php_print("\">\n                <span class=\"dashicons dashicons-hidden\" aria-hidden=\"true\"></span>\n               <span class=\"text\">")
            _e("Hide")
            php_print("</span>\n            </button>\n         <button type=\"button\" class=\"button wp-cancel-pw hide-if-no-js\" data-toggle=\"0\" aria-label=\"")
            esc_attr_e("Cancel password change")
            php_print("\">\n                <span class=\"dashicons dashicons-no\" aria-hidden=\"true\"></span>\n               <span class=\"text\">")
            _e("Cancel")
            php_print("""</span>
            </button>
            <div style=\"display:none\" id=\"pass-strength-result\" aria-live=\"polite\"></div>
            </div>
            </td>
            </tr>
            <tr class=\"user-pass2-wrap hide-if-js\">
            <th scope=\"row\"><label for=\"pass2\">""")
            _e("Repeat New Password")
            php_print("""</label></th>
            <td>
            <input name=\"pass2\" type=\"password\" id=\"pass2\" class=\"regular-text\" value=\"\" autocomplete=\"off\" />
            <p class=\"description\">""")
            _e("Type your new password again.")
            php_print("""</p>
            </td>
            </tr>
            <tr class=\"pw-weak\">
            <th>""")
            _e("Confirm Password")
            php_print("""</th>
            <td>
            <label>
            <input type=\"checkbox\" name=\"pw_weak\" class=\"pw-checkbox\" />
            <span id=\"pw-weak-text-label\">""")
            _e("Confirm use of potentially weak password")
            php_print("""</span>
            </label>
            </td>
            </tr>
            """)
        # end if
        php_print("\n       ")
        if IS_PROFILE_PAGE and php_count(sessions_.get_all()) == 1:
            php_print(" <tr class=\"user-sessions-wrap hide-if-no-js\">\n       <th>")
            _e("Sessions")
            php_print("</th>\n      <td aria-live=\"assertive\">\n          <div class=\"destroy-sessions\"><button type=\"button\" disabled class=\"button\">")
            _e("Log Out Everywhere Else")
            php_print("</button></div>\n            <p class=\"description\">\n             ")
            _e("You are only logged in at this location.")
            php_print("""           </p>
            </td>
            </tr>
            """)
        elif IS_PROFILE_PAGE and php_count(sessions_.get_all()) > 1:
            php_print(" <tr class=\"user-sessions-wrap hide-if-no-js\">\n       <th>")
            _e("Sessions")
            php_print("</th>\n      <td aria-live=\"assertive\">\n          <div class=\"destroy-sessions\"><button type=\"button\" class=\"button\" id=\"destroy-sessions\">")
            _e("Log Out Everywhere Else")
            php_print("</button></div>\n            <p class=\"description\">\n             ")
            _e("Did you lose your phone or leave your account logged in at a public computer? You can log out everywhere else, and stay logged in here.")
            php_print("""           </p>
            </td>
            </tr>
            """)
        elif (not IS_PROFILE_PAGE) and sessions_.get_all():
            php_print(" <tr class=\"user-sessions-wrap hide-if-no-js\">\n       <th>")
            _e("Sessions")
            php_print("</th>\n      <td>\n          <p><button type=\"button\" class=\"button\" id=\"destroy-sessions\">")
            _e("Log Out Everywhere")
            php_print("</button></p>\n          <p class=\"description\">\n             ")
            #// translators: %s: User's display name.
            printf(__("Log %s out of all locations."), profileuser_.display_name)
            php_print("""           </p>
            </td>
            </tr>
            """)
        # end if
        php_print("""
        </table>
        """)
        if IS_PROFILE_PAGE:
            #// 
            #// Fires after the 'About Yourself' settings table on the 'Your Profile' editing screen.
            #// 
            #// The action only fires if the current user is editing their own profile.
            #// 
            #// @since 2.0.0
            #// 
            #// @param WP_User $profileuser The current WP_User object.
            #//
            do_action("show_user_profile", profileuser_)
        else:
            #// 
            #// Fires after the 'About the User' settings table on the 'Edit User' screen.
            #// 
            #// @since 2.0.0
            #// 
            #// @param WP_User $profileuser The current WP_User object.
            #//
            do_action("edit_user_profile", profileuser_)
        # end if
        php_print("\n       ")
        #// 
        #// Filters whether to display additional capabilities for the user.
        #// 
        #// The 'Additional Capabilities' section will only be enabled if
        #// the number of the user's capabilities exceeds their number of
        #// roles.
        #// 
        #// @since 2.8.0
        #// 
        #// @param bool    $enable      Whether to display the capabilities. Default true.
        #// @param WP_User $profileuser The current WP_User object.
        #//
        if php_count(profileuser_.caps) > php_count(profileuser_.roles) and apply_filters("additional_capabilities_display", True, profileuser_):
            php_print(" <h2>")
            _e("Additional Capabilities")
            php_print("""</h2>
            <table class=\"form-table\" role=\"presentation\">
            <tr class=\"user-capabilities-wrap\">
            <th scope=\"row\">""")
            _e("Capabilities")
            php_print("</th>\n  <td>\n          ")
            output_ = ""
            for cap_,value_ in profileuser_.caps:
                if (not wp_roles_.is_role(cap_)):
                    if "" != output_:
                        output_ += ", "
                    # end if
                    if value_:
                        output_ += cap_
                    else:
                        #// translators: %s: Capability name.
                        output_ += php_sprintf(__("Denied: %s"), cap_)
                    # end if
                # end if
            # end for
            php_print(output_)
            php_print("""   </td>
            </tr>
            </table>
            """)
        # end if
        php_print("\n<input type=\"hidden\" name=\"action\" value=\"update\" />\n<input type=\"hidden\" name=\"user_id\" id=\"user_id\" value=\"")
        php_print(esc_attr(user_id_))
        php_print("\" />\n\n        ")
        submit_button(__("Update Profile") if IS_PROFILE_PAGE else __("Update User"))
        php_print("""
        </form>
        </div>
        """)
        break
    # end if
# end for
php_print("""<script type=\"text/javascript\">
if (window.location.hash == '#password') {
document.getElementById('pass1').focus();
}
</script>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
