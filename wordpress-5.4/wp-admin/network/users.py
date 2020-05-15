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
#// Multisite users administration panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_network_users")):
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
if (php_isset(lambda : PHP_REQUEST["action"])):
    #// This action is documented in wp-admin/network/edit.php
    do_action("wpmuadminedit")
    for case in Switch(PHP_REQUEST["action"]):
        if case("deleteuser"):
            if (not current_user_can("manage_network_users")):
                wp_die(__("Sorry, you are not allowed to access this page."), 403)
            # end if
            check_admin_referer("deleteuser")
            id = php_intval(PHP_REQUEST["id"])
            if "0" != id and "1" != id:
                PHP_POST["allusers"] = Array(id)
                #// confirm_delete_users() can only handle arrays.
                title = __("Users")
                parent_file = "users.php"
                php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
                php_print("<div class=\"wrap\">")
                confirm_delete_users(PHP_POST["allusers"])
                php_print("</div>")
                php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            else:
                wp_redirect(network_admin_url("users.php"))
            # end if
            php_exit(0)
        # end if
        if case("allusers"):
            if (not current_user_can("manage_network_users")):
                wp_die(__("Sorry, you are not allowed to access this page."), 403)
            # end if
            if (php_isset(lambda : PHP_POST["action"])) or (php_isset(lambda : PHP_POST["action2"])) and (php_isset(lambda : PHP_POST["allusers"])):
                check_admin_referer("bulk-users-network")
                doaction = PHP_POST["action"] if -1 != PHP_POST["action"] else PHP_POST["action2"]
                userfunction = ""
                for user_id in PHP_POST["allusers"]:
                    if (not php_empty(lambda : user_id)):
                        for case in Switch(doaction):
                            if case("delete"):
                                if (not current_user_can("delete_users")):
                                    wp_die(__("Sorry, you are not allowed to access this page."), 403)
                                # end if
                                title = __("Users")
                                parent_file = "users.php"
                                php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
                                php_print("<div class=\"wrap\">")
                                confirm_delete_users(PHP_POST["allusers"])
                                php_print("</div>")
                                php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
                                php_exit(0)
                            # end if
                            if case("spam"):
                                user = get_userdata(user_id)
                                if is_super_admin(user.ID):
                                    wp_die(php_sprintf(__("Warning! User cannot be modified. The user %s is a network administrator."), esc_html(user.user_login)))
                                # end if
                                userfunction = "all_spam"
                                blogs = get_blogs_of_user(user_id, True)
                                for details in blogs:
                                    if get_network().site_id != details.userblog_id:
                                        #// Main blog is not a spam!
                                        update_blog_status(details.userblog_id, "spam", "1")
                                    # end if
                                # end for
                                user_data = user.to_array()
                                user_data["spam"] = "1"
                                wp_update_user(user_data)
                                break
                            # end if
                            if case("notspam"):
                                user = get_userdata(user_id)
                                userfunction = "all_notspam"
                                blogs = get_blogs_of_user(user_id, True)
                                for details in blogs:
                                    update_blog_status(details.userblog_id, "spam", "0")
                                # end for
                                user_data = user.to_array()
                                user_data["spam"] = "0"
                                wp_update_user(user_data)
                                break
                            # end if
                        # end for
                    # end if
                # end for
                if (not php_in_array(doaction, Array("delete", "spam", "notspam"), True)):
                    sendback = wp_get_referer()
                    user_ids = PHP_POST["allusers"]
                    #// This action is documented in wp-admin/network/site-themes.php
                    sendback = apply_filters("handle_network_bulk_actions-" + get_current_screen().id, sendback, doaction, user_ids)
                    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
                    wp_safe_redirect(sendback)
                    php_exit(0)
                # end if
                wp_safe_redirect(add_query_arg(Array({"updated": "true", "action": userfunction}), wp_get_referer()))
            else:
                location = network_admin_url("users.php")
                if (not php_empty(lambda : PHP_REQUEST["paged"])):
                    location = add_query_arg("paged", int(PHP_REQUEST["paged"]), location)
                # end if
                wp_redirect(location)
            # end if
            php_exit(0)
        # end if
        if case("dodelete"):
            check_admin_referer("ms-users-delete")
            if (not current_user_can("manage_network_users") and current_user_can("delete_users")):
                wp_die(__("Sorry, you are not allowed to access this page."), 403)
            # end if
            if (not php_empty(lambda : PHP_POST["blog"])) and php_is_array(PHP_POST["blog"]):
                for id,users in PHP_POST["blog"]:
                    for blogid,user_id in users:
                        if (not current_user_can("delete_user", id)):
                            continue
                        # end if
                        if (not php_empty(lambda : PHP_POST["delete"])) and "reassign" == PHP_POST["delete"][blogid][id]:
                            remove_user_from_blog(id, blogid, int(user_id))
                        else:
                            remove_user_from_blog(id, blogid)
                        # end if
                    # end for
                # end for
            # end if
            i = 0
            if php_is_array(PHP_POST["user"]) and (not php_empty(lambda : PHP_POST["user"])):
                for id in PHP_POST["user"]:
                    if (not current_user_can("delete_user", id)):
                        continue
                    # end if
                    wpmu_delete_user(id)
                    i += 1
                # end for
            # end if
            if 1 == i:
                deletefunction = "delete"
            else:
                deletefunction = "all_delete"
            # end if
            wp_redirect(add_query_arg(Array({"updated": "true", "action": deletefunction}), network_admin_url("users.php")))
            php_exit(0)
        # end if
    # end for
# end if
wp_list_table = _get_list_table("WP_MS_Users_List_Table")
pagenum = wp_list_table.get_pagenum()
wp_list_table.prepare_items()
total_pages = wp_list_table.get_pagination_arg("total_pages")
if pagenum > total_pages and total_pages > 0:
    wp_redirect(add_query_arg("paged", total_pages))
    php_exit(0)
# end if
title = __("Users")
parent_file = "users.php"
add_screen_option("per_page")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This table shows all users across the network and the sites to which they are assigned.") + "</p>" + "<p>" + __("Hover over any user on the list to make the edit links appear. The Edit link on the left will take you to their Edit User profile page; the Edit link on the right by any site name goes to an Edit Site screen for that site.") + "</p>" + "<p>" + __("You can also go to the user&#8217;s profile page by clicking on the individual username.") + "</p>" + "<p>" + __("You can sort the table by clicking on any of the table headings and switch between list and excerpt views by using the icons above the users list.") + "</p>" + "<p>" + __("The bulk action will permanently delete selected users, or mark/unmark those selected as spam. Spam users will have posts removed and will be unable to sign up again with the same email addresses.") + "</p>" + "<p>" + __("You can make an existing user an additional super admin by going to the Edit User profile page and checking the box to grant that privilege.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Network_Admin_Users_Screen\">Documentation on Network Users</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/forum/multisite/\">Support Forums</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter users list"), "heading_pagination": __("Users list navigation"), "heading_list": __("Users list")}))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
if (php_isset(lambda : PHP_REQUEST["updated"])) and "true" == PHP_REQUEST["updated"] and (not php_empty(lambda : PHP_REQUEST["action"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\"><p>\n       ")
    for case in Switch(PHP_REQUEST["action"]):
        if case("delete"):
            _e("User deleted.")
            break
        # end if
        if case("all_spam"):
            _e("Users marked as spam.")
            break
        # end if
        if case("all_notspam"):
            _e("Users removed from spam.")
            break
        # end if
        if case("all_delete"):
            _e("Users deleted.")
            break
        # end if
        if case("add"):
            _e("User added.")
            break
        # end if
    # end for
    php_print(" </p></div>\n    ")
# end if
php_print("<div class=\"wrap\">\n   <h1 class=\"wp-heading-inline\">")
esc_html_e("Users")
php_print("</h1>\n\n    ")
if current_user_can("create_users"):
    php_print("     <a href=\"")
    php_print(network_admin_url("user-new.php"))
    php_print("\" class=\"page-title-action\">")
    php_print(esc_html_x("Add New", "user"))
    php_print("</a>\n                           ")
# end if
if php_strlen(usersearch):
    #// translators: %s: Search query.
    printf("<span class=\"subtitle\">" + __("Search results for &#8220;%s&#8221;") + "</span>", esc_html(usersearch))
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
wp_list_table.views()
php_print("\n   <form method=\"get\" class=\"search-form\">\n       ")
wp_list_table.search_box(__("Search Users"), "all-user")
php_print("""   </form>
<form id=\"form-user-list\" action=\"users.php?action=allusers\" method=\"post\">
""")
wp_list_table.display()
php_print("""   </form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
