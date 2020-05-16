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
#// List Table API: WP_Users_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying users in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Users_List_Table(WP_List_Table):
    site_id = Array()
    is_site_users = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @see WP_List_Table::__construct() for more information on default arguments.
    #// 
    #// @param array $args An associative array of arguments.
    #//
    def __init__(self, args=Array()):
        
        super().__init__(Array({"singular": "user", "plural": "users", "screen": args["screen"] if (php_isset(lambda : args["screen"])) else None}))
        self.is_site_users = "site-users-network" == self.screen.id
        if self.is_site_users:
            self.site_id = php_intval(PHP_REQUEST["id"]) if (php_isset(lambda : PHP_REQUEST["id"])) else 0
        # end if
    # end def __init__
    #// 
    #// Check the current user's permissions.
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        if self.is_site_users:
            return current_user_can("manage_sites")
        else:
            return current_user_can("list_users")
        # end if
    # end def ajax_user_can
    #// 
    #// Prepare the users list for display.
    #// 
    #// @since 3.1.0
    #// 
    #// @global string $role
    #// @global string $usersearch
    #//
    def prepare_items(self):
        
        global role,usersearch
        php_check_if_defined("role","usersearch")
        usersearch = wp_unslash(php_trim(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        role = PHP_REQUEST["role"] if (php_isset(lambda : PHP_REQUEST["role"])) else ""
        per_page = "site_users_network_per_page" if self.is_site_users else "users_per_page"
        users_per_page = self.get_items_per_page(per_page)
        paged = self.get_pagenum()
        if "none" == role:
            args = Array({"number": users_per_page, "offset": paged - 1 * users_per_page, "include": wp_get_users_with_no_role(self.site_id), "search": usersearch, "fields": "all_with_meta"})
        else:
            args = Array({"number": users_per_page, "offset": paged - 1 * users_per_page, "role": role, "search": usersearch, "fields": "all_with_meta"})
        # end if
        if "" != args["search"]:
            args["search"] = "*" + args["search"] + "*"
        # end if
        if self.is_site_users:
            args["blog_id"] = self.site_id
        # end if
        if (php_isset(lambda : PHP_REQUEST["orderby"])):
            args["orderby"] = PHP_REQUEST["orderby"]
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])):
            args["order"] = PHP_REQUEST["order"]
        # end if
        #// 
        #// Filters the query arguments used to retrieve users for the current users list table.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array $args Arguments passed to WP_User_Query to retrieve items for the current
        #// users list table.
        #//
        args = apply_filters("users_list_table_query_args", args)
        #// Query the user IDs for this page.
        wp_user_search = php_new_class("WP_User_Query", lambda : WP_User_Query(args))
        self.items = wp_user_search.get_results()
        self.set_pagination_args(Array({"total_items": wp_user_search.get_total(), "per_page": users_per_page}))
    # end def prepare_items
    #// 
    #// Output 'no users' message.
    #// 
    #// @since 3.1.0
    #//
    def no_items(self):
        
        _e("No users found.")
    # end def no_items
    #// 
    #// Return an associative array listing all the views that can be used
    #// with this table.
    #// 
    #// Provides a list of roles and user count for that role for easy
    #// Filtersing of the user table.
    #// 
    #// @since 3.1.0
    #// 
    #// @global string $role
    #// 
    #// @return string[] An array of HTML links keyed by their view.
    #//
    def get_views(self):
        
        global role
        php_check_if_defined("role")
        wp_roles = wp_roles()
        if self.is_site_users:
            url = "site-users.php?id=" + self.site_id
            switch_to_blog(self.site_id)
            users_of_blog = count_users("time", self.site_id)
            restore_current_blog()
        else:
            url = "users.php"
            users_of_blog = count_users()
        # end if
        total_users = users_of_blog["total_users"]
        avail_roles = users_of_blog["avail_roles"]
        users_of_blog = None
        current_link_attributes = " class=\"current\" aria-current=\"page\"" if php_empty(lambda : role) else ""
        role_links = Array()
        role_links["all"] = php_sprintf("<a href=\"%s\"%s>%s</a>", url, current_link_attributes, php_sprintf(_nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", total_users, "users"), number_format_i18n(total_users)))
        for this_role,name in wp_roles.get_names():
            if (not (php_isset(lambda : avail_roles[this_role]))):
                continue
            # end if
            current_link_attributes = ""
            if this_role == role:
                current_link_attributes = " class=\"current\" aria-current=\"page\""
            # end if
            name = translate_user_role(name)
            name = php_sprintf(__("%1$s <span class=\"count\">(%2$s)</span>"), name, number_format_i18n(avail_roles[this_role]))
            role_links[this_role] = "<a href='" + esc_url(add_query_arg("role", this_role, url)) + str("'") + str(current_link_attributes) + str(">") + str(name) + str("</a>")
        # end for
        if (not php_empty(lambda : avail_roles["none"])):
            current_link_attributes = ""
            if "none" == role:
                current_link_attributes = " class=\"current\" aria-current=\"page\""
            # end if
            name = __("No role")
            name = php_sprintf(__("%1$s <span class=\"count\">(%2$s)</span>"), name, number_format_i18n(avail_roles["none"]))
            role_links["none"] = "<a href='" + esc_url(add_query_arg("role", "none", url)) + str("'") + str(current_link_attributes) + str(">") + str(name) + str("</a>")
        # end if
        return role_links
    # end def get_views
    #// 
    #// Retrieve an associative array of bulk actions available on this table.
    #// 
    #// @since 3.1.0
    #// 
    #// @return string[] Array of bulk action labels keyed by their action.
    #//
    def get_bulk_actions(self):
        
        actions = Array()
        if is_multisite():
            if current_user_can("remove_users"):
                actions["remove"] = __("Remove")
            # end if
        else:
            if current_user_can("delete_users"):
                actions["delete"] = __("Delete")
            # end if
        # end if
        return actions
    # end def get_bulk_actions
    #// 
    #// Output the controls to allow user roles to be changed in bulk.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $which Whether this is being invoked above ("top")
    #// or below the table ("bottom").
    #//
    def extra_tablenav(self, which=None):
        
        id = "new_role2" if "bottom" == which else "new_role"
        button_id = "changeit2" if "bottom" == which else "changeit"
        php_print(" <div class=\"alignleft actions\">\n     ")
        if current_user_can("promote_users") and self.has_items():
            php_print("     <label class=\"screen-reader-text\" for=\"")
            php_print(id)
            php_print("\">")
            _e("Change role to&hellip;")
            php_print("</label>\n       <select name=\"")
            php_print(id)
            php_print("\" id=\"")
            php_print(id)
            php_print("\">\n            <option value=\"\">")
            _e("Change role to&hellip;")
            php_print("</option>\n          ")
            wp_dropdown_roles()
            php_print("     </select>\n         ")
            submit_button(__("Change"), "", button_id, False)
        # end if
        #// 
        #// Fires just before the closing div containing the bulk role-change controls
        #// in the Users list table.
        #// 
        #// @since 3.5.0
        #// @since 4.6.0 The `$which` parameter was added.
        #// 
        #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
        #//
        do_action("restrict_manage_users", which)
        php_print("     </div>\n        ")
        #// 
        #// Fires immediately following the closing "actions" div in the tablenav for the users
        #// list table.
        #// 
        #// @since 4.9.0
        #// 
        #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
        #//
        do_action("manage_users_extra_tablenav", which)
    # end def extra_tablenav
    #// 
    #// Capture the bulk action required, and return it.
    #// 
    #// Overridden from the base class implementation to capture
    #// the role change drop-down.
    #// 
    #// @since 3.1.0
    #// 
    #// @return string The bulk action required.
    #//
    def current_action(self):
        
        if (php_isset(lambda : PHP_REQUEST["changeit"])) or (php_isset(lambda : PHP_REQUEST["changeit2"])) and (not php_empty(lambda : PHP_REQUEST["new_role"])) or (not php_empty(lambda : PHP_REQUEST["new_role2"])):
            return "promote"
        # end if
        return super().current_action()
    # end def current_action
    #// 
    #// Get a list of columns for the list table.
    #// 
    #// @since 3.1.0
    #// 
    #// @return string[] Array of column titles keyed by their column name.
    #//
    def get_columns(self):
        
        c = Array({"cb": "<input type=\"checkbox\" />", "username": __("Username"), "name": __("Name"), "email": __("Email"), "role": __("Role"), "posts": __("Posts")})
        if self.is_site_users:
            c["posts"] = None
        # end if
        return c
    # end def get_columns
    #// 
    #// Get a list of sortable columns for the list table.
    #// 
    #// @since 3.1.0
    #// 
    #// @return array Array of sortable columns.
    #//
    def get_sortable_columns(self):
        
        c = Array({"username": "login", "email": "email"})
        return c
    # end def get_sortable_columns
    #// 
    #// Generate the list table rows.
    #// 
    #// @since 3.1.0
    #//
    def display_rows(self):
        
        #// Query the post counts for this page.
        if (not self.is_site_users):
            post_counts = count_many_users_posts(php_array_keys(self.items))
        # end if
        for userid,user_object in self.items:
            php_print("\n   " + self.single_row(user_object, "", "", post_counts[userid] if (php_isset(lambda : post_counts)) else 0))
        # end for
    # end def display_rows
    #// 
    #// Generate HTML for a single row on the users.php admin panel.
    #// 
    #// @since 3.1.0
    #// @since 4.2.0 The `$style` parameter was deprecated.
    #// @since 4.4.0 The `$role` parameter was deprecated.
    #// 
    #// @param WP_User $user_object The current user object.
    #// @param string  $style       Deprecated. Not used.
    #// @param string  $role        Deprecated. Not used.
    #// @param int     $numposts    Optional. Post count to display for this user. Defaults
    #// to zero, as in, a new user has made zero posts.
    #// @return string Output for a single row.
    #//
    def single_row(self, user_object=None, style="", role="", numposts=0):
        
        if (not type(user_object).__name__ == "WP_User"):
            user_object = get_userdata(php_int(user_object))
        # end if
        user_object.filter = "display"
        email = user_object.user_email
        if self.is_site_users:
            url = str("site-users.php?id=") + str(self.site_id) + str("&amp;")
        else:
            url = "users.php?"
        # end if
        user_roles = self.get_role_list(user_object)
        #// Set up the hover actions for this user.
        actions = Array()
        checkbox = ""
        super_admin = ""
        if is_multisite() and current_user_can("manage_network_users"):
            if php_in_array(user_object.user_login, get_super_admins(), True):
                super_admin = " &mdash; " + __("Super Admin")
            # end if
        # end if
        #// Check if the user for this row is editable.
        if current_user_can("list_users"):
            #// Set up the user editing link.
            edit_link = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user_object.ID)))
            if current_user_can("edit_user", user_object.ID):
                edit = str("<strong><a href=\"") + str(edit_link) + str("\">") + str(user_object.user_login) + str("</a>") + str(super_admin) + str("</strong><br />")
                actions["edit"] = "<a href=\"" + edit_link + "\">" + __("Edit") + "</a>"
            else:
                edit = str("<strong>") + str(user_object.user_login) + str(super_admin) + str("</strong><br />")
            # end if
            if (not is_multisite()) and get_current_user_id() != user_object.ID and current_user_can("delete_user", user_object.ID):
                actions["delete"] = "<a class='submitdelete' href='" + wp_nonce_url(str("users.php?action=delete&amp;user=") + str(user_object.ID), "bulk-users") + "'>" + __("Delete") + "</a>"
            # end if
            if is_multisite() and current_user_can("remove_user", user_object.ID):
                actions["remove"] = "<a class='submitdelete' href='" + wp_nonce_url(url + str("action=remove&amp;user=") + str(user_object.ID), "bulk-users") + "'>" + __("Remove") + "</a>"
            # end if
            #// Add a link to the user's author archive, if not empty.
            author_posts_url = get_author_posts_url(user_object.ID)
            if author_posts_url:
                actions["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(author_posts_url), esc_attr(php_sprintf(__("View posts by %s"), user_object.display_name)), __("View"))
            # end if
            #// 
            #// Filters the action links displayed under each user in the Users list table.
            #// 
            #// @since 2.8.0
            #// 
            #// @param string[] $actions     An array of action links to be displayed.
            #// Default 'Edit', 'Delete' for single site, and
            #// 'Edit', 'Remove' for Multisite.
            #// @param WP_User  $user_object WP_User object for the currently listed user.
            #//
            actions = apply_filters("user_row_actions", actions, user_object)
            #// Role classes.
            role_classes = esc_attr(php_implode(" ", php_array_keys(user_roles)))
            #// Set up the checkbox (because the user is editable, otherwise it's empty).
            checkbox = php_sprintf("<label class=\"screen-reader-text\" for=\"user_%1$s\">%2$s</label>" + "<input type=\"checkbox\" name=\"users[]\" id=\"user_%1$s\" class=\"%3$s\" value=\"%1$s\" />", user_object.ID, php_sprintf(__("Select %s"), user_object.user_login), role_classes)
        else:
            edit = str("<strong>") + str(user_object.user_login) + str(super_admin) + str("</strong>")
        # end if
        avatar = get_avatar(user_object.ID, 32)
        #// Comma-separated list of user roles.
        roles_list = php_implode(", ", user_roles)
        r = str("<tr id='user-") + str(user_object.ID) + str("'>")
        columns, hidden, sortable, primary = self.get_column_info()
        for column_name,column_display_name in columns:
            classes = str(column_name) + str(" column-") + str(column_name)
            if primary == column_name:
                classes += " has-row-actions column-primary"
            # end if
            if "posts" == column_name:
                classes += " num"
                pass
            # end if
            if php_in_array(column_name, hidden):
                classes += " hidden"
            # end if
            data = "data-colname=\"" + wp_strip_all_tags(column_display_name) + "\""
            attributes = str("class='") + str(classes) + str("' ") + str(data)
            if "cb" == column_name:
                r += str("<th scope='row' class='check-column'>") + str(checkbox) + str("</th>")
            else:
                r += str("<td ") + str(attributes) + str(">")
                for case in Switch(column_name):
                    if case("username"):
                        r += str(avatar) + str(" ") + str(edit)
                        break
                    # end if
                    if case("name"):
                        if user_object.first_name and user_object.last_name:
                            r += str(user_object.first_name) + str(" ") + str(user_object.last_name)
                        elif user_object.first_name:
                            r += user_object.first_name
                        elif user_object.last_name:
                            r += user_object.last_name
                        else:
                            r += php_sprintf("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">%s</span>", _x("Unknown", "name"))
                        # end if
                        break
                    # end if
                    if case("email"):
                        r += "<a href='" + esc_url(str("mailto:") + str(email)) + str("'>") + str(email) + str("</a>")
                        break
                    # end if
                    if case("role"):
                        r += esc_html(roles_list)
                        break
                    # end if
                    if case("posts"):
                        if numposts > 0:
                            r += php_sprintf("<a href=\"%s\" class=\"edit\"><span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", str("edit.php?author=") + str(user_object.ID), numposts, php_sprintf(_n("%s post by this author", "%s posts by this author", numposts), number_format_i18n(numposts)))
                        else:
                            r += 0
                        # end if
                        break
                    # end if
                    if case():
                        #// 
                        #// Filters the display output of custom columns in the Users list table.
                        #// 
                        #// @since 2.8.0
                        #// 
                        #// @param string $output      Custom column output. Default empty.
                        #// @param string $column_name Column name.
                        #// @param int    $user_id     ID of the currently-listed user.
                        #//
                        r += apply_filters("manage_users_custom_column", "", column_name, user_object.ID)
                    # end if
                # end for
                if primary == column_name:
                    r += self.row_actions(actions)
                # end if
                r += "</td>"
            # end if
        # end for
        r += "</tr>"
        return r
    # end def single_row
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
    #// Returns an array of user roles for a given user object.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_User $user_object The WP_User object.
    #// @return string[] An array of user roles.
    #//
    def get_role_list(self, user_object=None):
        
        wp_roles = wp_roles()
        role_list = Array()
        for role in user_object.roles:
            if (php_isset(lambda : wp_roles.role_names[role])):
                role_list[role] = translate_user_role(wp_roles.role_names[role])
            # end if
        # end for
        if php_empty(lambda : role_list):
            role_list["none"] = _x("None", "no user roles")
        # end if
        #// 
        #// Filters the returned array of roles for a user.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[] $role_list   An array of user roles.
        #// @param WP_User  $user_object A WP_User object.
        #//
        return apply_filters("get_role_list", role_list, user_object)
    # end def get_role_list
# end class WP_Users_List_Table
