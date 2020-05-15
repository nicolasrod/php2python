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
#// List Table API: WP_MS_Users_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying users in a list table for the network admin.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_MS_Users_List_Table(WP_List_Table):
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        return current_user_can("manage_network_users")
    # end def ajax_user_can
    #// 
    #// @global string $usersearch
    #// @global string $role
    #// @global string $mode
    #//
    def prepare_items(self):
        global PHP_REQUEST
        global usersearch,role,mode
        php_check_if_defined("usersearch","role","mode")
        usersearch = wp_unslash(php_trim(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        users_per_page = self.get_items_per_page("users_network_per_page")
        role = PHP_REQUEST["role"] if (php_isset(lambda : PHP_REQUEST["role"])) else ""
        paged = self.get_pagenum()
        args = Array({"number": users_per_page, "offset": paged - 1 * users_per_page, "search": usersearch, "blog_id": 0, "fields": "all_with_meta"})
        if wp_is_large_network("users"):
            args["search"] = php_ltrim(args["search"], "*")
        elif "" != args["search"]:
            args["search"] = php_trim(args["search"], "*")
            args["search"] = "*" + args["search"] + "*"
        # end if
        if "super" == role:
            args["login__in"] = get_super_admins()
        # end if
        #// 
        #// If the network is large and a search is not being performed,
        #// show only the latest users with no paging in order to avoid
        #// expensive count queries.
        #//
        if (not usersearch) and wp_is_large_network("users"):
            if (not (php_isset(lambda : PHP_REQUEST["orderby"]))):
                PHP_REQUEST["orderby"] = "id"
                PHP_REQUEST["orderby"] = "id"
            # end if
            if (not (php_isset(lambda : PHP_REQUEST["order"]))):
                PHP_REQUEST["order"] = "DESC"
                PHP_REQUEST["order"] = "DESC"
            # end if
            args["count_total"] = False
        # end if
        if (php_isset(lambda : PHP_REQUEST["orderby"])):
            args["orderby"] = PHP_REQUEST["orderby"]
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])):
            args["order"] = PHP_REQUEST["order"]
        # end if
        if (not php_empty(lambda : PHP_REQUEST["mode"])):
            mode = "excerpt" if "excerpt" == PHP_REQUEST["mode"] else "list"
            set_user_setting("network_users_list_mode", mode)
        else:
            mode = get_user_setting("network_users_list_mode", "list")
        # end if
        #// This filter is documented in wp-admin/includes/class-wp-users-list-table.php
        args = apply_filters("users_list_table_query_args", args)
        #// Query the user IDs for this page.
        wp_user_search = php_new_class("WP_User_Query", lambda : WP_User_Query(args))
        self.items = wp_user_search.get_results()
        self.set_pagination_args(Array({"total_items": wp_user_search.get_total(), "per_page": users_per_page}))
    # end def prepare_items
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        actions = Array()
        if current_user_can("delete_users"):
            actions["delete"] = __("Delete")
        # end if
        actions["spam"] = _x("Mark as Spam", "user")
        actions["notspam"] = _x("Not Spam", "user")
        return actions
    # end def get_bulk_actions
    #// 
    #//
    def no_items(self):
        
        _e("No users found.")
    # end def no_items
    #// 
    #// @global string $role
    #// @return array
    #//
    def get_views(self):
        
        global role
        php_check_if_defined("role")
        total_users = get_user_count()
        super_admins = get_super_admins()
        total_admins = php_count(super_admins)
        current_link_attributes = " class=\"current\" aria-current=\"page\"" if "super" != role else ""
        role_links = Array()
        role_links["all"] = php_sprintf("<a href=\"%s\"%s>%s</a>", network_admin_url("users.php"), current_link_attributes, php_sprintf(_nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", total_users, "users"), number_format_i18n(total_users)))
        current_link_attributes = " class=\"current\" aria-current=\"page\"" if "super" == role else ""
        role_links["super"] = php_sprintf("<a href=\"%s\"%s>%s</a>", network_admin_url("users.php?role=super"), current_link_attributes, php_sprintf(_n("Super Admin <span class=\"count\">(%s)</span>", "Super Admins <span class=\"count\">(%s)</span>", total_admins), number_format_i18n(total_admins)))
        return role_links
    # end def get_views
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param string $which
    #//
    def pagination(self, which=None):
        
        global mode
        php_check_if_defined("mode")
        super().pagination(which)
        if "top" == which:
            self.view_switcher(mode)
        # end if
    # end def pagination
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        users_columns = Array({"cb": "<input type=\"checkbox\" />", "username": __("Username"), "name": __("Name"), "email": __("Email"), "registered": _x("Registered", "user"), "blogs": __("Sites")})
        #// 
        #// Filters the columns displayed in the Network Admin Users list table.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param string[] $users_columns An array of user columns. Default 'cb', 'username',
        #// 'name', 'email', 'registered', 'blogs'.
        #//
        return apply_filters("wpmu_users_columns", users_columns)
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        return Array({"username": "login", "name": "name", "email": "email", "registered": "id"})
    # end def get_sortable_columns
    #// 
    #// Handles the checkbox column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_cb(self, user=None):
        
        if is_super_admin(user.ID):
            return
        # end if
        php_print("     <label class=\"screen-reader-text\" for=\"blog_")
        php_print(user.ID)
        php_print("\">\n            ")
        #// translators: %s: User login.
        printf(__("Select %s"), user.user_login)
        php_print("     </label>\n      <input type=\"checkbox\" id=\"blog_")
        php_print(user.ID)
        php_print("\" name=\"allusers[]\" value=\"")
        php_print(esc_attr(user.ID))
        php_print("\" />\n      ")
    # end def column_cb
    #// 
    #// Handles the ID column output.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_id(self, user=None):
        
        php_print(user.ID)
    # end def column_id
    #// 
    #// Handles the username column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_username(self, user=None):
        
        super_admins = get_super_admins()
        avatar = get_avatar(user.user_email, 32)
        php_print(avatar)
        if current_user_can("edit_user", user.ID):
            edit_link = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user.ID)))
            edit = str("<a href=\"") + str(edit_link) + str("\">") + str(user.user_login) + str("</a>")
        else:
            edit = user.user_login
        # end if
        php_print("     <strong>\n          ")
        php_print(edit)
        if php_in_array(user.user_login, super_admins):
            php_print(" &mdash; " + __("Super Admin"))
        # end if
        php_print("     </strong>\n     ")
    # end def column_username
    #// 
    #// Handles the name column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_name(self, user=None):
        
        if user.first_name and user.last_name:
            php_print(str(user.first_name) + str(" ") + str(user.last_name))
        elif user.first_name:
            php_print(user.first_name)
        elif user.last_name:
            php_print(user.last_name)
        else:
            php_print("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">" + _x("Unknown", "name") + "</span>")
        # end if
    # end def column_name
    #// 
    #// Handles the email column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_email(self, user=None):
        
        php_print("<a href='" + esc_url(str("mailto:") + str(user.user_email)) + str("'>") + str(user.user_email) + str("</a>"))
    # end def column_email
    #// 
    #// Handles the registered date column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_registered(self, user=None):
        
        global mode
        php_check_if_defined("mode")
        if "list" == mode:
            date = __("Y/m/d")
        else:
            date = __("Y/m/d g:i:s a")
        # end if
        php_print(mysql2date(date, user.user_registered))
    # end def column_registered
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user
    #// @param string  $classes
    #// @param string  $data
    #// @param string  $primary
    #//
    def _column_blogs(self, user=None, classes=None, data=None, primary=None):
        
        php_print("<td class=\"", classes, " has-row-actions\" ", data, ">")
        php_print(self.column_blogs(user))
        php_print(self.handle_row_actions(user, "blogs", primary))
        php_print("</td>")
    # end def _column_blogs
    #// 
    #// Handles the sites column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_blogs(self, user=None):
        
        blogs = get_blogs_of_user(user.ID, True)
        if (not php_is_array(blogs)):
            return
        # end if
        for val in blogs:
            if (not can_edit_network(val.site_id)):
                continue
            # end if
            path = "" if "/" == val.path else val.path
            site_classes = Array("site-" + val.site_id)
            #// 
            #// Filters the span class for a site listing on the mulisite user list table.
            #// 
            #// @since 5.2.0
            #// 
            #// @param string[] $site_classes Array of class names used within the span tag. Default "site-#" with the site's network ID.
            #// @param int      $site_id      Site ID.
            #// @param int      $network_id   Network ID.
            #// @param WP_User  $user         WP_User object.
            #//
            site_classes = apply_filters("ms_user_list_site_class", site_classes, val.userblog_id, val.site_id, user)
            if php_is_array(site_classes) and (not php_empty(lambda : site_classes)):
                site_classes = php_array_map("sanitize_html_class", array_unique(site_classes))
                php_print("<span class=\"" + esc_attr(php_implode(" ", site_classes)) + "\">")
            else:
                php_print("<span>")
            # end if
            php_print("<a href=\"" + esc_url(network_admin_url("site-info.php?id=" + val.userblog_id)) + "\">" + php_str_replace("." + get_network().domain, "", val.domain + path) + "</a>")
            php_print(" <small class=\"row-actions\">")
            actions = Array()
            actions["edit"] = "<a href=\"" + esc_url(network_admin_url("site-info.php?id=" + val.userblog_id)) + "\">" + __("Edit") + "</a>"
            class_ = ""
            if 1 == val.spam:
                class_ += "site-spammed "
            # end if
            if 1 == val.mature:
                class_ += "site-mature "
            # end if
            if 1 == val.deleted:
                class_ += "site-deleted "
            # end if
            if 1 == val.archived:
                class_ += "site-archived "
            # end if
            actions["view"] = "<a class=\"" + class_ + "\" href=\"" + esc_url(get_home_url(val.userblog_id)) + "\">" + __("View") + "</a>"
            #// 
            #// Filters the action links displayed next the sites a user belongs to
            #// in the Network Admin Users list table.
            #// 
            #// @since 3.1.0
            #// 
            #// @param string[] $actions     An array of action links to be displayed. Default 'Edit', 'View'.
            #// @param int      $userblog_id The site ID.
            #//
            actions = apply_filters("ms_user_list_site_actions", actions, val.userblog_id)
            i = 0
            action_count = php_count(actions)
            for action,link in actions:
                i += 1
                sep = "" if i == action_count else " | "
                php_print(str("<span class='") + str(action) + str("'>") + str(link) + str(sep) + str("</span>"))
            # end for
            php_print("</small></span><br/>")
        # end for
    # end def column_blogs
    #// 
    #// Handles the default column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user       The current WP_User object.
    #// @param string $column_name The current column name.
    #//
    def column_default(self, user=None, column_name=None):
        
        #// This filter is documented in wp-admin/includes/class-wp-users-list-table.php
        php_print(apply_filters("manage_users_custom_column", "", column_name, user.ID))
    # end def column_default
    def display_rows(self):
        
        for user in self.items:
            class_ = ""
            status_list = Array({"spam": "site-spammed", "deleted": "site-deleted"})
            for status,col in status_list:
                if user.status:
                    class_ += str(" ") + str(col)
                # end if
            # end for
            php_print("         <tr class=\"")
            php_print(php_trim(class_))
            php_print("\">\n                ")
            self.single_row_columns(user)
            php_print("         </tr>\n         ")
        # end for
    # end def display_rows
    #// 
    #// Gets the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, 'username'.
    #//
    def get_default_primary_column_name(self):
        
        return "username"
    # end def get_default_primary_column_name
    #// 
    #// Generates and displays row action links.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $user        User being acted upon.
    #// @param string $column_name Current column name.
    #// @param string $primary     Primary column name.
    #// @return string Row actions output for users in Multisite, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, user=None, column_name=None, primary=None):
        
        if primary != column_name:
            return ""
        # end if
        super_admins = get_super_admins()
        actions = Array()
        if current_user_can("edit_user", user.ID):
            edit_link = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user.ID)))
            actions["edit"] = "<a href=\"" + edit_link + "\">" + __("Edit") + "</a>"
        # end if
        if current_user_can("delete_user", user.ID) and (not php_in_array(user.user_login, super_admins)):
            actions["delete"] = "<a href=\"" + esc_url(network_admin_url(add_query_arg("_wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), wp_nonce_url("users.php", "deleteuser") + "&amp;action=deleteuser&amp;id=" + user.ID))) + "\" class=\"delete\">" + __("Delete") + "</a>"
        # end if
        #// 
        #// Filters the action links displayed under each user in the Network Admin Users list table.
        #// 
        #// @since 3.2.0
        #// 
        #// @param string[] $actions An array of action links to be displayed. Default 'Edit', 'Delete'.
        #// @param WP_User  $user    WP_User object.
        #//
        actions = apply_filters("ms_user_row_actions", actions, user)
        return self.row_actions(actions)
    # end def handle_row_actions
# end class WP_MS_Users_List_Table
