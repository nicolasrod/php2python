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
        global usersearch_
        global role_
        global mode_
        php_check_if_defined("usersearch_","role_","mode_")
        usersearch_ = wp_unslash(php_trim(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        users_per_page_ = self.get_items_per_page("users_network_per_page")
        role_ = PHP_REQUEST["role"] if (php_isset(lambda : PHP_REQUEST["role"])) else ""
        paged_ = self.get_pagenum()
        args_ = Array({"number": users_per_page_, "offset": paged_ - 1 * users_per_page_, "search": usersearch_, "blog_id": 0, "fields": "all_with_meta"})
        if wp_is_large_network("users"):
            args_["search"] = php_ltrim(args_["search"], "*")
        elif "" != args_["search"]:
            args_["search"] = php_trim(args_["search"], "*")
            args_["search"] = "*" + args_["search"] + "*"
        # end if
        if "super" == role_:
            args_["login__in"] = get_super_admins()
        # end if
        #// 
        #// If the network is large and a search is not being performed,
        #// show only the latest users with no paging in order to avoid
        #// expensive count queries.
        #//
        if (not usersearch_) and wp_is_large_network("users"):
            if (not (php_isset(lambda : PHP_REQUEST["orderby"]))):
                PHP_REQUEST["orderby"] = "id"
                PHP_REQUEST["orderby"] = "id"
            # end if
            if (not (php_isset(lambda : PHP_REQUEST["order"]))):
                PHP_REQUEST["order"] = "DESC"
                PHP_REQUEST["order"] = "DESC"
            # end if
            args_["count_total"] = False
        # end if
        if (php_isset(lambda : PHP_REQUEST["orderby"])):
            args_["orderby"] = PHP_REQUEST["orderby"]
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])):
            args_["order"] = PHP_REQUEST["order"]
        # end if
        if (not php_empty(lambda : PHP_REQUEST["mode"])):
            mode_ = "excerpt" if "excerpt" == PHP_REQUEST["mode"] else "list"
            set_user_setting("network_users_list_mode", mode_)
        else:
            mode_ = get_user_setting("network_users_list_mode", "list")
        # end if
        #// This filter is documented in wp-admin/includes/class-wp-users-list-table.php
        args_ = apply_filters("users_list_table_query_args", args_)
        #// Query the user IDs for this page.
        wp_user_search_ = php_new_class("WP_User_Query", lambda : WP_User_Query(args_))
        self.items = wp_user_search_.get_results()
        self.set_pagination_args(Array({"total_items": wp_user_search_.get_total(), "per_page": users_per_page_}))
    # end def prepare_items
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        actions_ = Array()
        if current_user_can("delete_users"):
            actions_["delete"] = __("Delete")
        # end if
        actions_["spam"] = _x("Mark as Spam", "user")
        actions_["notspam"] = _x("Not Spam", "user")
        return actions_
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
        
        
        global role_
        php_check_if_defined("role_")
        total_users_ = get_user_count()
        super_admins_ = get_super_admins()
        total_admins_ = php_count(super_admins_)
        current_link_attributes_ = " class=\"current\" aria-current=\"page\"" if "super" != role_ else ""
        role_links_ = Array()
        role_links_["all"] = php_sprintf("<a href=\"%s\"%s>%s</a>", network_admin_url("users.php"), current_link_attributes_, php_sprintf(_nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", total_users_, "users"), number_format_i18n(total_users_)))
        current_link_attributes_ = " class=\"current\" aria-current=\"page\"" if "super" == role_ else ""
        role_links_["super"] = php_sprintf("<a href=\"%s\"%s>%s</a>", network_admin_url("users.php?role=super"), current_link_attributes_, php_sprintf(_n("Super Admin <span class=\"count\">(%s)</span>", "Super Admins <span class=\"count\">(%s)</span>", total_admins_), number_format_i18n(total_admins_)))
        return role_links_
    # end def get_views
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param string $which
    #//
    def pagination(self, which_=None):
        
        
        global mode_
        php_check_if_defined("mode_")
        super().pagination(which_)
        if "top" == which_:
            self.view_switcher(mode_)
        # end if
    # end def pagination
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        users_columns_ = Array({"cb": "<input type=\"checkbox\" />", "username": __("Username"), "name": __("Name"), "email": __("Email"), "registered": _x("Registered", "user"), "blogs": __("Sites")})
        #// 
        #// Filters the columns displayed in the Network Admin Users list table.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param string[] $users_columns An array of user columns. Default 'cb', 'username',
        #// 'name', 'email', 'registered', 'blogs'.
        #//
        return apply_filters("wpmu_users_columns", users_columns_)
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
    def column_cb(self, user_=None):
        
        
        if is_super_admin(user_.ID):
            return
        # end if
        php_print("     <label class=\"screen-reader-text\" for=\"blog_")
        php_print(user_.ID)
        php_print("\">\n            ")
        #// translators: %s: User login.
        printf(__("Select %s"), user_.user_login)
        php_print("     </label>\n      <input type=\"checkbox\" id=\"blog_")
        php_print(user_.ID)
        php_print("\" name=\"allusers[]\" value=\"")
        php_print(esc_attr(user_.ID))
        php_print("\" />\n      ")
    # end def column_cb
    #// 
    #// Handles the ID column output.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_id(self, user_=None):
        
        
        php_print(user_.ID)
    # end def column_id
    #// 
    #// Handles the username column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_username(self, user_=None):
        
        
        super_admins_ = get_super_admins()
        avatar_ = get_avatar(user_.user_email, 32)
        php_print(avatar_)
        if current_user_can("edit_user", user_.ID):
            edit_link_ = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user_.ID)))
            edit_ = str("<a href=\"") + str(edit_link_) + str("\">") + str(user_.user_login) + str("</a>")
        else:
            edit_ = user_.user_login
        # end if
        php_print("     <strong>\n          ")
        php_print(edit_)
        if php_in_array(user_.user_login, super_admins_):
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
    def column_name(self, user_=None):
        
        
        if user_.first_name and user_.last_name:
            php_print(str(user_.first_name) + str(" ") + str(user_.last_name))
        elif user_.first_name:
            php_print(user_.first_name)
        elif user_.last_name:
            php_print(user_.last_name)
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
    def column_email(self, user_=None):
        
        
        php_print("<a href='" + esc_url(str("mailto:") + str(user_.user_email)) + str("'>") + str(user_.user_email) + str("</a>"))
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
    def column_registered(self, user_=None):
        
        
        global mode_
        php_check_if_defined("mode_")
        if "list" == mode_:
            date_ = __("Y/m/d")
        else:
            date_ = __("Y/m/d g:i:s a")
        # end if
        php_print(mysql2date(date_, user_.user_registered))
    # end def column_registered
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user
    #// @param string  $classes
    #// @param string  $data
    #// @param string  $primary
    #//
    def _column_blogs(self, user_=None, classes_=None, data_=None, primary_=None):
        
        
        php_print("<td class=\"", classes_, " has-row-actions\" ", data_, ">")
        php_print(self.column_blogs(user_))
        php_print(self.handle_row_actions(user_, "blogs", primary_))
        php_print("</td>")
    # end def _column_blogs
    #// 
    #// Handles the sites column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_User $user The current WP_User object.
    #//
    def column_blogs(self, user_=None):
        
        
        blogs_ = get_blogs_of_user(user_.ID, True)
        if (not php_is_array(blogs_)):
            return
        # end if
        for val_ in blogs_:
            if (not can_edit_network(val_.site_id)):
                continue
            # end if
            path_ = "" if "/" == val_.path else val_.path
            site_classes_ = Array("site-" + val_.site_id)
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
            site_classes_ = apply_filters("ms_user_list_site_class", site_classes_, val_.userblog_id, val_.site_id, user_)
            if php_is_array(site_classes_) and (not php_empty(lambda : site_classes_)):
                site_classes_ = php_array_map("sanitize_html_class", array_unique(site_classes_))
                php_print("<span class=\"" + esc_attr(php_implode(" ", site_classes_)) + "\">")
            else:
                php_print("<span>")
            # end if
            php_print("<a href=\"" + esc_url(network_admin_url("site-info.php?id=" + val_.userblog_id)) + "\">" + php_str_replace("." + get_network().domain, "", val_.domain + path_) + "</a>")
            php_print(" <small class=\"row-actions\">")
            actions_ = Array()
            actions_["edit"] = "<a href=\"" + esc_url(network_admin_url("site-info.php?id=" + val_.userblog_id)) + "\">" + __("Edit") + "</a>"
            class_ = ""
            if 1 == val_.spam:
                class_ += "site-spammed "
            # end if
            if 1 == val_.mature:
                class_ += "site-mature "
            # end if
            if 1 == val_.deleted:
                class_ += "site-deleted "
            # end if
            if 1 == val_.archived:
                class_ += "site-archived "
            # end if
            actions_["view"] = "<a class=\"" + class_ + "\" href=\"" + esc_url(get_home_url(val_.userblog_id)) + "\">" + __("View") + "</a>"
            #// 
            #// Filters the action links displayed next the sites a user belongs to
            #// in the Network Admin Users list table.
            #// 
            #// @since 3.1.0
            #// 
            #// @param string[] $actions     An array of action links to be displayed. Default 'Edit', 'View'.
            #// @param int      $userblog_id The site ID.
            #//
            actions_ = apply_filters("ms_user_list_site_actions", actions_, val_.userblog_id)
            i_ = 0
            action_count_ = php_count(actions_)
            for action_,link_ in actions_.items():
                i_ += 1
                sep_ = "" if i_ == action_count_ else " | "
                php_print(str("<span class='") + str(action_) + str("'>") + str(link_) + str(sep_) + str("</span>"))
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
    def column_default(self, user_=None, column_name_=None):
        
        
        #// This filter is documented in wp-admin/includes/class-wp-users-list-table.php
        php_print(apply_filters("manage_users_custom_column", "", column_name_, user_.ID))
    # end def column_default
    def display_rows(self):
        
        
        for user_ in self.items:
            class_ = ""
            status_list_ = Array({"spam": "site-spammed", "deleted": "site-deleted"})
            for status_,col_ in status_list_.items():
                if user_.status_:
                    class_ += str(" ") + str(col_)
                # end if
            # end for
            php_print("         <tr class=\"")
            php_print(php_trim(class_))
            php_print("\">\n                ")
            self.single_row_columns(user_)
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
    def handle_row_actions(self, user_=None, column_name_=None, primary_=None):
        
        
        if primary_ != column_name_:
            return ""
        # end if
        super_admins_ = get_super_admins()
        actions_ = Array()
        if current_user_can("edit_user", user_.ID):
            edit_link_ = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user_.ID)))
            actions_["edit"] = "<a href=\"" + edit_link_ + "\">" + __("Edit") + "</a>"
        # end if
        if current_user_can("delete_user", user_.ID) and (not php_in_array(user_.user_login, super_admins_)):
            actions_["delete"] = "<a href=\"" + esc_url(network_admin_url(add_query_arg("_wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), wp_nonce_url("users.php", "deleteuser") + "&amp;action=deleteuser&amp;id=" + user_.ID))) + "\" class=\"delete\">" + __("Delete") + "</a>"
        # end if
        #// 
        #// Filters the action links displayed under each user in the Network Admin Users list table.
        #// 
        #// @since 3.2.0
        #// 
        #// @param string[] $actions An array of action links to be displayed. Default 'Edit', 'Delete'.
        #// @param WP_User  $user    WP_User object.
        #//
        actions_ = apply_filters("ms_user_row_actions", actions_, user_)
        return self.row_actions(actions_)
    # end def handle_row_actions
# end class WP_MS_Users_List_Table
