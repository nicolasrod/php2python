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
#// User administration panel
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 1.0.0
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("list_users")):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to list users.") + "</p>", 403)
# end if
wp_list_table_ = _get_list_table("WP_Users_List_Table")
pagenum_ = wp_list_table_.get_pagenum()
title_ = __("Users")
parent_file_ = "users.php"
add_screen_option("per_page")
#// Contextual help - choose Help on the top right of admin panel to preview this.
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen lists all the existing users for your site. Each user has one of five defined roles as set by the site admin: Site Administrator, Editor, Author, Contributor, or Subscriber. Users with roles other than Administrator will see fewer options in the dashboard navigation when they are logged in, based on their role.") + "</p>" + "<p>" + __("To add a new user for your site, click the Add New button at the top of the screen or Add New in the Users menu section.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "screen-content", "title": __("Screen Content"), "content": "<p>" + __("You can customize the display of this screen in a number of ways:") + "</p>" + "<ul>" + "<li>" + __("You can hide/display columns based on your needs and decide how many users to list per screen using the Screen Options tab.") + "</li>" + "<li>" + __("You can filter the list of users by User Role using the text links above the users list to show All, Administrator, Editor, Author, Contributor, or Subscriber. The default view is to show all users. Unused User Roles are not listed.") + "</li>" + "<li>" + __("You can view all posts made by a user by clicking on the number under the Posts column.") + "</li>" + "</ul>"}))
help_ = "<p>" + __("Hovering over a row in the users list will display action links that allow you to manage users. You can perform the following actions:") + "</p>" + "<ul>" + "<li>" + __("<strong>Edit</strong> takes you to the editable profile screen for that user. You can also reach that screen by clicking on the username.") + "</li>"
if is_multisite():
    help_ += "<li>" + __("<strong>Remove</strong> allows you to remove a user from your site. It does not delete their content. You can also remove multiple users at once by using Bulk Actions.") + "</li>"
else:
    help_ += "<li>" + __("<strong>Delete</strong> brings you to the Delete Users screen for confirmation, where you can permanently remove a user from your site and delete their content. You can also delete multiple users at once by using Bulk Actions.") + "</li>"
# end if
help_ += "</ul>"
get_current_screen().add_help_tab(Array({"id": "action-links", "title": __("Available Actions"), "content": help_}))
help_ = None
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/users-screen/\">Documentation on Managing Users</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/roles-and-capabilities/\">Descriptions of Roles and Capabilities</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter users list"), "heading_pagination": __("Users list navigation"), "heading_list": __("Users list")}))
if php_empty(lambda : PHP_REQUEST):
    referer_ = "<input type=\"hidden\" name=\"wp_http_referer\" value=\"" + esc_attr(wp_unslash(PHP_SERVER["REQUEST_URI"])) + "\" />"
elif (php_isset(lambda : PHP_REQUEST["wp_http_referer"])):
    redirect_ = remove_query_arg(Array("wp_http_referer", "updated", "delete_count"), wp_unslash(PHP_REQUEST["wp_http_referer"]))
    referer_ = "<input type=\"hidden\" name=\"wp_http_referer\" value=\"" + esc_attr(redirect_) + "\" />"
else:
    redirect_ = "users.php"
    referer_ = ""
# end if
update_ = ""
for case in Switch(wp_list_table_.current_action()):
    if case("promote"):
        check_admin_referer("bulk-users")
        if (not current_user_can("promote_users")):
            wp_die(__("Sorry, you are not allowed to edit this user."), 403)
        # end if
        if php_empty(lambda : PHP_REQUEST["users"]):
            wp_redirect(redirect_)
            php_exit(0)
        # end if
        editable_roles_ = get_editable_roles()
        role_ = False
        if (not php_empty(lambda : PHP_REQUEST["new_role2"])):
            role_ = PHP_REQUEST["new_role2"]
        elif (not php_empty(lambda : PHP_REQUEST["new_role"])):
            role_ = PHP_REQUEST["new_role"]
        # end if
        if (not role_) or php_empty(lambda : editable_roles_[role_]):
            wp_die(__("Sorry, you are not allowed to give users that role."), 403)
        # end if
        userids_ = PHP_REQUEST["users"]
        update_ = "promote"
        for id_ in userids_:
            id_ = php_int(id_)
            if (not current_user_can("promote_user", id_)):
                wp_die(__("Sorry, you are not allowed to edit this user."), 403)
            # end if
            #// The new role of the current user must also have the promote_users cap or be a multisite super admin.
            if id_ == current_user_.ID and (not wp_roles_.role_objects[role_].has_cap("promote_users")) and (not is_multisite() and current_user_can("manage_network_users")):
                update_ = "err_admin_role"
                continue
            # end if
            #// If the user doesn't already belong to the blog, bail.
            if is_multisite() and (not is_user_member_of_blog(id_)):
                wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("One of the selected users is not a member of this site.") + "</p>", 403)
            # end if
            user_ = get_userdata(id_)
            user_.set_role(role_)
        # end for
        wp_redirect(add_query_arg("update", update_, redirect_))
        php_exit(0)
    # end if
    if case("dodelete"):
        if is_multisite():
            wp_die(__("User deletion is not allowed from this screen."), 400)
        # end if
        check_admin_referer("delete-users")
        if php_empty(lambda : PHP_REQUEST["users"]):
            wp_redirect(redirect_)
            php_exit(0)
        # end if
        userids_ = php_array_map("intval", PHP_REQUEST["users"])
        if php_empty(lambda : PHP_REQUEST["delete_option"]):
            url_ = self_admin_url("users.php?action=delete&users[]=" + php_implode("&users[]=", userids_) + "&error=true")
            url_ = php_str_replace("&amp;", "&", wp_nonce_url(url_, "bulk-users"))
            wp_redirect(url_)
            php_exit(0)
        # end if
        if (not current_user_can("delete_users")):
            wp_die(__("Sorry, you are not allowed to delete users."), 403)
        # end if
        update_ = "del"
        delete_count_ = 0
        for id_ in userids_:
            if (not current_user_can("delete_user", id_)):
                wp_die(__("Sorry, you are not allowed to delete that user."), 403)
            # end if
            if id_ == current_user_.ID:
                update_ = "err_admin_del"
                continue
            # end if
            for case in Switch(PHP_REQUEST["delete_option"]):
                if case("delete"):
                    wp_delete_user(id_)
                    break
                # end if
                if case("reassign"):
                    wp_delete_user(id_, PHP_REQUEST["reassign_user"])
                    break
                # end if
            # end for
            delete_count_ += 1
        # end for
        redirect_ = add_query_arg(Array({"delete_count": delete_count_, "update": update_}), redirect_)
        wp_redirect(redirect_)
        php_exit(0)
    # end if
    if case("delete"):
        if is_multisite():
            wp_die(__("User deletion is not allowed from this screen."), 400)
        # end if
        check_admin_referer("bulk-users")
        if php_empty(lambda : PHP_REQUEST["users"]) and php_empty(lambda : PHP_REQUEST["user"]):
            wp_redirect(redirect_)
            php_exit(0)
        # end if
        if (not current_user_can("delete_users")):
            errors_ = php_new_class("WP_Error", lambda : WP_Error("edit_users", __("Sorry, you are not allowed to delete users.")))
        # end if
        if php_empty(lambda : PHP_REQUEST["users"]):
            userids_ = Array(php_intval(PHP_REQUEST["user"]))
        else:
            userids_ = php_array_map("intval", PHP_REQUEST["users"])
        # end if
        all_userids_ = userids_
        if php_in_array(current_user_.ID, userids_):
            userids_ = php_array_diff(userids_, Array(current_user_.ID))
        # end if
        #// 
        #// Filters whether the users being deleted have additional content
        #// associated with them outside of the `post_author` and `link_owner` relationships.
        #// 
        #// @since 5.2.0
        #// 
        #// @param boolean $users_have_additional_content Whether the users have additional content. Default false.
        #// @param int[]   $userids                       Array of IDs for users being deleted.
        #//
        users_have_content_ = php_bool(apply_filters("users_have_additional_content", False, userids_))
        if userids_ and (not users_have_content_):
            if wpdb_.get_var(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_author IN( ") + php_implode(",", userids_) + " ) LIMIT 1"):
                users_have_content_ = True
            elif wpdb_.get_var(str("SELECT link_id FROM ") + str(wpdb_.links) + str(" WHERE link_owner IN( ") + php_implode(",", userids_) + " ) LIMIT 1"):
                users_have_content_ = True
            # end if
        # end if
        if users_have_content_:
            add_action("admin_head", "delete_users_add_js")
        # end if
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        php_print(" <form method=\"post\" name=\"updateusers\" id=\"updateusers\">\n        ")
        wp_nonce_field("delete-users")
        php_print("     ")
        php_print(referer_)
        php_print("\n<div class=\"wrap\">\n<h1>")
        _e("Delete Users")
        php_print("</h1>\n      ")
        if (php_isset(lambda : PHP_REQUEST["error"])):
            php_print(" <div class=\"error\">\n     <p><strong>")
            _e("Error:")
            php_print("</strong> ")
            _e("Please select an option.")
            php_print("</p>\n   </div>\n        ")
        # end if
        php_print("\n       ")
        if 1 == php_count(all_userids_):
            php_print(" <p>")
            _e("You have specified this user for deletion:")
            php_print("</p>\n       ")
        else:
            php_print(" <p>")
            _e("You have specified these users for deletion:")
            php_print("</p>\n       ")
        # end if
        php_print("\n<ul>\n     ")
        go_delete_ = 0
        for id_ in all_userids_:
            user_ = get_userdata(id_)
            if id_ == current_user_.ID:
                #// translators: 1: User ID, 2: User login.
                php_print("<li>" + php_sprintf(__("ID #%1$s: %2$s <strong>The current user will not be deleted.</strong>"), id_, user_.user_login) + "</li>\n")
            else:
                #// translators: 1: User ID, 2: User login.
                php_print("<li><input type=\"hidden\" name=\"users[]\" value=\"" + esc_attr(id_) + "\" />" + php_sprintf(__("ID #%1$s: %2$s"), id_, user_.user_login) + "</li>\n")
                go_delete_ += 1
            # end if
        # end for
        php_print(" </ul>\n     ")
        if go_delete_:
            if (not users_have_content_):
                php_print("         <input type=\"hidden\" name=\"delete_option\" value=\"delete\" />\n         ")
            else:
                php_print("             ")
                if 1 == go_delete_:
                    php_print("         <fieldset><p><legend>")
                    _e("What should be done with content owned by this user?")
                    php_print("</legend></p>\n      ")
                else:
                    php_print("         <fieldset><p><legend>")
                    _e("What should be done with content owned by these users?")
                    php_print("</legend></p>\n      ")
                # end if
                php_print("     <ul style=\"list-style:none;\">\n           <li><label><input type=\"radio\" id=\"delete_option0\" name=\"delete_option\" value=\"delete\" />\n             ")
                _e("Delete all content.")
                php_print("</label></li>\n          <li><input type=\"radio\" id=\"delete_option1\" name=\"delete_option\" value=\"reassign\" />\n              ")
                php_print("<label for=\"delete_option1\">" + __("Attribute all content to:") + "</label> ")
                wp_dropdown_users(Array({"name": "reassign_user", "exclude": userids_, "show": "display_name_with_login"}))
                php_print("         </li>\n     </ul></fieldset>\n              ")
            # end if
            #// 
            #// Fires at the end of the delete users form prior to the confirm button.
            #// 
            #// @since 4.0.0
            #// @since 4.5.0 The `$userids` parameter was added.
            #// 
            #// @param WP_User $current_user WP_User object for the current user.
            #// @param int[]   $userids      Array of IDs for users being deleted.
            #//
            do_action("delete_user_form", current_user_, userids_)
            php_print(" <input type=\"hidden\" name=\"action\" value=\"dodelete\" />\n          ")
            submit_button(__("Confirm Deletion"), "primary")
            php_print(" ")
        else:
            php_print(" <p>")
            _e("There are no valid users selected for deletion.")
            php_print("</p>\n   ")
        # end if
        php_print(" </div>\n    </form>\n       ")
        break
    # end if
    if case("doremove"):
        check_admin_referer("remove-users")
        if (not is_multisite()):
            wp_die(__("You can&#8217;t remove users."), 400)
        # end if
        if php_empty(lambda : PHP_REQUEST["users"]):
            wp_redirect(redirect_)
            php_exit(0)
        # end if
        if (not current_user_can("remove_users")):
            wp_die(__("Sorry, you are not allowed to remove users."), 403)
        # end if
        userids_ = PHP_REQUEST["users"]
        update_ = "remove"
        for id_ in userids_:
            id_ = php_int(id_)
            if (not current_user_can("remove_user", id_)):
                update_ = "err_admin_remove"
                continue
            # end if
            remove_user_from_blog(id_, blog_id_)
        # end for
        redirect_ = add_query_arg(Array({"update": update_}), redirect_)
        wp_redirect(redirect_)
        php_exit(0)
    # end if
    if case("remove"):
        check_admin_referer("bulk-users")
        if (not is_multisite()):
            wp_die(__("You can&#8217;t remove users."), 400)
        # end if
        if php_empty(lambda : PHP_REQUEST["users"]) and php_empty(lambda : PHP_REQUEST["user"]):
            wp_redirect(redirect_)
            php_exit(0)
        # end if
        if (not current_user_can("remove_users")):
            error_ = php_new_class("WP_Error", lambda : WP_Error("edit_users", __("Sorry, you are not allowed to remove users.")))
        # end if
        if php_empty(lambda : PHP_REQUEST["users"]):
            userids_ = Array(php_intval(PHP_REQUEST["user"]))
        else:
            userids_ = PHP_REQUEST["users"]
        # end if
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        php_print(" <form method=\"post\" name=\"updateusers\" id=\"updateusers\">\n        ")
        wp_nonce_field("remove-users")
        php_print("     ")
        php_print(referer_)
        php_print("\n<div class=\"wrap\">\n<h1>")
        _e("Remove Users from Site")
        php_print("</h1>\n\n        ")
        if 1 == php_count(userids_):
            php_print(" <p>")
            _e("You have specified this user for removal:")
            php_print("</p>\n       ")
        else:
            php_print(" <p>")
            _e("You have specified these users for removal:")
            php_print("</p>\n       ")
        # end if
        php_print("\n<ul>\n     ")
        go_remove_ = False
        for id_ in userids_:
            id_ = php_int(id_)
            user_ = get_userdata(id_)
            if (not current_user_can("remove_user", id_)):
                #// translators: 1: User ID, 2: User login.
                php_print("<li>" + php_sprintf(__("ID #%1$s: %2$s <strong>Sorry, you are not allowed to remove this user.</strong>"), id_, user_.user_login) + "</li>\n")
            else:
                #// translators: 1: User ID, 2: User login.
                php_print(str("<li><input type=\"hidden\" name=\"users[]\" value=\"") + str(id_) + str("\" />") + php_sprintf(__("ID #%1$s: %2$s"), id_, user_.user_login) + "</li>\n")
                go_remove_ = True
            # end if
        # end for
        php_print(" </ul>\n     ")
        if go_remove_:
            php_print("     <input type=\"hidden\" name=\"action\" value=\"doremove\" />\n          ")
            submit_button(__("Confirm Removal"), "primary")
            php_print(" ")
        else:
            php_print(" <p>")
            _e("There are no valid users selected for removal.")
            php_print("</p>\n   ")
        # end if
        php_print(" </div>\n    </form>\n       ")
        break
    # end if
    if case():
        if (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
            wp_redirect(remove_query_arg(Array("_wp_http_referer", "_wpnonce"), wp_unslash(PHP_SERVER["REQUEST_URI"])))
            php_exit(0)
        # end if
        if wp_list_table_.current_action() and (not php_empty(lambda : PHP_REQUEST["users"])):
            screen_ = get_current_screen().id
            sendback_ = wp_get_referer()
            userids_ = PHP_REQUEST["users"]
            #// This action is documented in wp-admin/edit.php
            sendback_ = apply_filters(str("handle_bulk_actions-") + str(screen_), sendback_, wp_list_table_.current_action(), userids_)
            #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
            wp_safe_redirect(sendback_)
            php_exit(0)
        # end if
        wp_list_table_.prepare_items()
        total_pages_ = wp_list_table_.get_pagination_arg("total_pages")
        if pagenum_ > total_pages_ and total_pages_ > 0:
            wp_redirect(add_query_arg("paged", total_pages_))
            php_exit(0)
        # end if
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        messages_ = Array()
        if (php_isset(lambda : PHP_REQUEST["update"])):
            for case in Switch(PHP_REQUEST["update"]):
                if case("del"):
                    pass
                # end if
                if case("del_many"):
                    delete_count_ = php_int(PHP_REQUEST["delete_count"]) if (php_isset(lambda : PHP_REQUEST["delete_count"])) else 0
                    if 1 == delete_count_:
                        message_ = __("User deleted.")
                    else:
                        #// translators: %s: Number of users.
                        message_ = _n("%s user deleted.", "%s users deleted.", delete_count_)
                    # end if
                    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + php_sprintf(message_, number_format_i18n(delete_count_)) + "</p></div>"
                    break
                # end if
                if case("add"):
                    message_ = __("New user created.")
                    user_id_ = PHP_REQUEST["id"] if (php_isset(lambda : PHP_REQUEST["id"])) else False
                    if user_id_ and current_user_can("edit_user", user_id_):
                        message_ += php_sprintf(" <a href=\"%s\">%s</a>", esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), self_admin_url("user-edit.php?user_id=" + user_id_))), __("Edit user"))
                    # end if
                    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + message_ + "</p></div>"
                    break
                # end if
                if case("promote"):
                    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("Changed roles.") + "</p></div>"
                    break
                # end if
                if case("err_admin_role"):
                    messages_[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("The current user&#8217;s role must have user editing capabilities.") + "</p></div>"
                    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("Other user roles have been changed.") + "</p></div>"
                    break
                # end if
                if case("err_admin_del"):
                    messages_[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("You can&#8217;t delete the current user.") + "</p></div>"
                    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible\"><p>" + __("Other users have been deleted.") + "</p></div>"
                    break
                # end if
                if case("remove"):
                    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible fade\"><p>" + __("User removed from this site.") + "</p></div>"
                    break
                # end if
                if case("err_admin_remove"):
                    messages_[-1] = "<div id=\"message\" class=\"error notice is-dismissible\"><p>" + __("You can't remove the current user.") + "</p></div>"
                    messages_[-1] = "<div id=\"message\" class=\"updated notice is-dismissible fade\"><p>" + __("Other users have been removed.") + "</p></div>"
                    break
                # end if
            # end for
        # end if
        php_print("\n       ")
        if (php_isset(lambda : errors_)) and is_wp_error(errors_):
            php_print("     <div class=\"error\">\n         <ul>\n          ")
            for err_ in errors_.get_error_messages():
                php_print(str("<li>") + str(err_) + str("</li>\n"))
            # end for
            php_print("         </ul>\n     </div>\n            ")
        # end if
        if (not php_empty(lambda : messages_)):
            for msg_ in messages_:
                php_print(msg_)
            # end for
        # end if
        php_print("""
        <div class=\"wrap\">
        <h1 class=\"wp-heading-inline\">
        """)
        php_print(esc_html(title_))
        php_print("</h1>\n\n        ")
        if current_user_can("create_users"):
            php_print(" <a href=\"")
            php_print(admin_url("user-new.php"))
            php_print("\" class=\"page-title-action\">")
            php_print(esc_html_x("Add New", "user"))
            php_print("</a>\n")
        elif is_multisite() and current_user_can("promote_users"):
            php_print(" <a href=\"")
            php_print(admin_url("user-new.php"))
            php_print("\" class=\"page-title-action\">")
            php_print(esc_html_x("Add Existing", "user"))
            php_print("</a>\n           ")
        # end if
        if php_strlen(usersearch_):
            #// translators: %s: Search query.
            printf("<span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", esc_html(usersearch_))
        # end if
        php_print("""
        <hr class=\"wp-header-end\">
        """)
        wp_list_table_.views()
        php_print("""
        <form method=\"get\">
        """)
        wp_list_table_.search_box(__("Search Users"), "user")
        php_print("\n       ")
        if (not php_empty(lambda : PHP_REQUEST["role"])):
            php_print("<input type=\"hidden\" name=\"role\" value=\"")
            php_print(esc_attr(PHP_REQUEST["role"]))
            php_print("\" />\n")
        # end if
        php_print("\n       ")
        wp_list_table_.display()
        php_print("""</form>
        <br class=\"clear\" />
        </div>
        """)
        break
    # end if
# end for
#// End of the $doaction switch.
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
