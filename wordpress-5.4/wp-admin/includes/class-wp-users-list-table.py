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
    #// 
    #// Site ID to generate the Users list table for.
    #// 
    #// @since 3.1.0
    #// @var int
    #//
    site_id = Array()
    #// 
    #// Whether or not the current Users list table is for Multisite.
    #// 
    #// @since 3.1.0
    #// @var bool
    #//
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
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        super().__init__(Array({"singular": "user", "plural": "users", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
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
        
        
        global role_
        global usersearch_
        php_check_if_defined("role_","usersearch_")
        usersearch_ = wp_unslash(php_trim(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        role_ = PHP_REQUEST["role"] if (php_isset(lambda : PHP_REQUEST["role"])) else ""
        per_page_ = "site_users_network_per_page" if self.is_site_users else "users_per_page"
        users_per_page_ = self.get_items_per_page(per_page_)
        paged_ = self.get_pagenum()
        if "none" == role_:
            args_ = Array({"number": users_per_page_, "offset": paged_ - 1 * users_per_page_, "include": wp_get_users_with_no_role(self.site_id), "search": usersearch_, "fields": "all_with_meta"})
        else:
            args_ = Array({"number": users_per_page_, "offset": paged_ - 1 * users_per_page_, "role": role_, "search": usersearch_, "fields": "all_with_meta"})
        # end if
        if "" != args_["search"]:
            args_["search"] = "*" + args_["search"] + "*"
        # end if
        if self.is_site_users:
            args_["blog_id"] = self.site_id
        # end if
        if (php_isset(lambda : PHP_REQUEST["orderby"])):
            args_["orderby"] = PHP_REQUEST["orderby"]
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])):
            args_["order"] = PHP_REQUEST["order"]
        # end if
        #// 
        #// Filters the query arguments used to retrieve users for the current users list table.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array $args Arguments passed to WP_User_Query to retrieve items for the current
        #// users list table.
        #//
        args_ = apply_filters("users_list_table_query_args", args_)
        #// Query the user IDs for this page.
        wp_user_search_ = php_new_class("WP_User_Query", lambda : WP_User_Query(args_))
        self.items = wp_user_search_.get_results()
        self.set_pagination_args(Array({"total_items": wp_user_search_.get_total(), "per_page": users_per_page_}))
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
        
        
        global role_
        php_check_if_defined("role_")
        wp_roles_ = wp_roles()
        if self.is_site_users:
            url_ = "site-users.php?id=" + self.site_id
            switch_to_blog(self.site_id)
            users_of_blog_ = count_users("time", self.site_id)
            restore_current_blog()
        else:
            url_ = "users.php"
            users_of_blog_ = count_users()
        # end if
        total_users_ = users_of_blog_["total_users"]
        avail_roles_ = users_of_blog_["avail_roles"]
        users_of_blog_ = None
        current_link_attributes_ = " class=\"current\" aria-current=\"page\"" if php_empty(lambda : role_) else ""
        role_links_ = Array()
        role_links_["all"] = php_sprintf("<a href=\"%s\"%s>%s</a>", url_, current_link_attributes_, php_sprintf(_nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", total_users_, "users"), number_format_i18n(total_users_)))
        for this_role_,name_ in wp_roles_.get_names():
            if (not (php_isset(lambda : avail_roles_[this_role_]))):
                continue
            # end if
            current_link_attributes_ = ""
            if this_role_ == role_:
                current_link_attributes_ = " class=\"current\" aria-current=\"page\""
            # end if
            name_ = translate_user_role(name_)
            name_ = php_sprintf(__("%1$s <span class=\"count\">(%2$s)</span>"), name_, number_format_i18n(avail_roles_[this_role_]))
            role_links_[this_role_] = "<a href='" + esc_url(add_query_arg("role", this_role_, url_)) + str("'") + str(current_link_attributes_) + str(">") + str(name_) + str("</a>")
        # end for
        if (not php_empty(lambda : avail_roles_["none"])):
            current_link_attributes_ = ""
            if "none" == role_:
                current_link_attributes_ = " class=\"current\" aria-current=\"page\""
            # end if
            name_ = __("No role")
            name_ = php_sprintf(__("%1$s <span class=\"count\">(%2$s)</span>"), name_, number_format_i18n(avail_roles_["none"]))
            role_links_["none"] = "<a href='" + esc_url(add_query_arg("role", "none", url_)) + str("'") + str(current_link_attributes_) + str(">") + str(name_) + str("</a>")
        # end if
        return role_links_
    # end def get_views
    #// 
    #// Retrieve an associative array of bulk actions available on this table.
    #// 
    #// @since 3.1.0
    #// 
    #// @return string[] Array of bulk action labels keyed by their action.
    #//
    def get_bulk_actions(self):
        
        
        actions_ = Array()
        if is_multisite():
            if current_user_can("remove_users"):
                actions_["remove"] = __("Remove")
            # end if
        else:
            if current_user_can("delete_users"):
                actions_["delete"] = __("Delete")
            # end if
        # end if
        return actions_
    # end def get_bulk_actions
    #// 
    #// Output the controls to allow user roles to be changed in bulk.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $which Whether this is being invoked above ("top")
    #// or below the table ("bottom").
    #//
    def extra_tablenav(self, which_=None):
        
        
        id_ = "new_role2" if "bottom" == which_ else "new_role"
        button_id_ = "changeit2" if "bottom" == which_ else "changeit"
        php_print(" <div class=\"alignleft actions\">\n     ")
        if current_user_can("promote_users") and self.has_items():
            php_print("     <label class=\"screen-reader-text\" for=\"")
            php_print(id_)
            php_print("\">")
            _e("Change role to&hellip;")
            php_print("</label>\n       <select name=\"")
            php_print(id_)
            php_print("\" id=\"")
            php_print(id_)
            php_print("\">\n            <option value=\"\">")
            _e("Change role to&hellip;")
            php_print("</option>\n          ")
            wp_dropdown_roles()
            php_print("     </select>\n         ")
            submit_button(__("Change"), "", button_id_, False)
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
        do_action("restrict_manage_users", which_)
        php_print("     </div>\n        ")
        #// 
        #// Fires immediately following the closing "actions" div in the tablenav for the users
        #// list table.
        #// 
        #// @since 4.9.0
        #// 
        #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
        #//
        do_action("manage_users_extra_tablenav", which_)
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
        
        
        c_ = Array({"cb": "<input type=\"checkbox\" />", "username": __("Username"), "name": __("Name"), "email": __("Email"), "role": __("Role"), "posts": __("Posts")})
        if self.is_site_users:
            c_["posts"] = None
        # end if
        return c_
    # end def get_columns
    #// 
    #// Get a list of sortable columns for the list table.
    #// 
    #// @since 3.1.0
    #// 
    #// @return array Array of sortable columns.
    #//
    def get_sortable_columns(self):
        
        
        c_ = Array({"username": "login", "email": "email"})
        return c_
    # end def get_sortable_columns
    #// 
    #// Generate the list table rows.
    #// 
    #// @since 3.1.0
    #//
    def display_rows(self):
        
        
        #// Query the post counts for this page.
        if (not self.is_site_users):
            post_counts_ = count_many_users_posts(php_array_keys(self.items))
        # end if
        for userid_,user_object_ in self.items:
            php_print("\n   " + self.single_row(user_object_, "", "", post_counts_[userid_] if (php_isset(lambda : post_counts_)) else 0))
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
    def single_row(self, user_object_=None, style_="", role_="", numposts_=0):
        
        
        if (not type(user_object_).__name__ == "WP_User"):
            user_object_ = get_userdata(php_int(user_object_))
        # end if
        user_object_.filter = "display"
        email_ = user_object_.user_email
        if self.is_site_users:
            url_ = str("site-users.php?id=") + str(self.site_id) + str("&amp;")
        else:
            url_ = "users.php?"
        # end if
        user_roles_ = self.get_role_list(user_object_)
        #// Set up the hover actions for this user.
        actions_ = Array()
        checkbox_ = ""
        super_admin_ = ""
        if is_multisite() and current_user_can("manage_network_users"):
            if php_in_array(user_object_.user_login, get_super_admins(), True):
                super_admin_ = " &mdash; " + __("Super Admin")
            # end if
        # end if
        #// Check if the user for this row is editable.
        if current_user_can("list_users"):
            #// Set up the user editing link.
            edit_link_ = esc_url(add_query_arg("wp_http_referer", urlencode(wp_unslash(PHP_SERVER["REQUEST_URI"])), get_edit_user_link(user_object_.ID)))
            if current_user_can("edit_user", user_object_.ID):
                edit_ = str("<strong><a href=\"") + str(edit_link_) + str("\">") + str(user_object_.user_login) + str("</a>") + str(super_admin_) + str("</strong><br />")
                actions_["edit"] = "<a href=\"" + edit_link_ + "\">" + __("Edit") + "</a>"
            else:
                edit_ = str("<strong>") + str(user_object_.user_login) + str(super_admin_) + str("</strong><br />")
            # end if
            if (not is_multisite()) and get_current_user_id() != user_object_.ID and current_user_can("delete_user", user_object_.ID):
                actions_["delete"] = "<a class='submitdelete' href='" + wp_nonce_url(str("users.php?action=delete&amp;user=") + str(user_object_.ID), "bulk-users") + "'>" + __("Delete") + "</a>"
            # end if
            if is_multisite() and current_user_can("remove_user", user_object_.ID):
                actions_["remove"] = "<a class='submitdelete' href='" + wp_nonce_url(url_ + str("action=remove&amp;user=") + str(user_object_.ID), "bulk-users") + "'>" + __("Remove") + "</a>"
            # end if
            #// Add a link to the user's author archive, if not empty.
            author_posts_url_ = get_author_posts_url(user_object_.ID)
            if author_posts_url_:
                actions_["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(author_posts_url_), esc_attr(php_sprintf(__("View posts by %s"), user_object_.display_name)), __("View"))
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
            actions_ = apply_filters("user_row_actions", actions_, user_object_)
            #// Role classes.
            role_classes_ = esc_attr(php_implode(" ", php_array_keys(user_roles_)))
            #// Set up the checkbox (because the user is editable, otherwise it's empty).
            checkbox_ = php_sprintf("<label class=\"screen-reader-text\" for=\"user_%1$s\">%2$s</label>" + "<input type=\"checkbox\" name=\"users[]\" id=\"user_%1$s\" class=\"%3$s\" value=\"%1$s\" />", user_object_.ID, php_sprintf(__("Select %s"), user_object_.user_login), role_classes_)
        else:
            edit_ = str("<strong>") + str(user_object_.user_login) + str(super_admin_) + str("</strong>")
        # end if
        avatar_ = get_avatar(user_object_.ID, 32)
        #// Comma-separated list of user roles.
        roles_list_ = php_implode(", ", user_roles_)
        r_ = str("<tr id='user-") + str(user_object_.ID) + str("'>")
        columns_, hidden_, sortable_, primary_ = self.get_column_info()
        for column_name_,column_display_name_ in columns_:
            classes_ = str(column_name_) + str(" column-") + str(column_name_)
            if primary_ == column_name_:
                classes_ += " has-row-actions column-primary"
            # end if
            if "posts" == column_name_:
                classes_ += " num"
                pass
            # end if
            if php_in_array(column_name_, hidden_):
                classes_ += " hidden"
            # end if
            data_ = "data-colname=\"" + wp_strip_all_tags(column_display_name_) + "\""
            attributes_ = str("class='") + str(classes_) + str("' ") + str(data_)
            if "cb" == column_name_:
                r_ += str("<th scope='row' class='check-column'>") + str(checkbox_) + str("</th>")
            else:
                r_ += str("<td ") + str(attributes_) + str(">")
                for case in Switch(column_name_):
                    if case("username"):
                        r_ += str(avatar_) + str(" ") + str(edit_)
                        break
                    # end if
                    if case("name"):
                        if user_object_.first_name and user_object_.last_name:
                            r_ += str(user_object_.first_name) + str(" ") + str(user_object_.last_name)
                        elif user_object_.first_name:
                            r_ += user_object_.first_name
                        elif user_object_.last_name:
                            r_ += user_object_.last_name
                        else:
                            r_ += php_sprintf("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">%s</span>", _x("Unknown", "name"))
                        # end if
                        break
                    # end if
                    if case("email"):
                        r_ += "<a href='" + esc_url(str("mailto:") + str(email_)) + str("'>") + str(email_) + str("</a>")
                        break
                    # end if
                    if case("role"):
                        r_ += esc_html(roles_list_)
                        break
                    # end if
                    if case("posts"):
                        if numposts_ > 0:
                            r_ += php_sprintf("<a href=\"%s\" class=\"edit\"><span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", str("edit.php?author=") + str(user_object_.ID), numposts_, php_sprintf(_n("%s post by this author", "%s posts by this author", numposts_), number_format_i18n(numposts_)))
                        else:
                            r_ += 0
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
                        r_ += apply_filters("manage_users_custom_column", "", column_name_, user_object_.ID)
                    # end if
                # end for
                if primary_ == column_name_:
                    r_ += self.row_actions(actions_)
                # end if
                r_ += "</td>"
            # end if
        # end for
        r_ += "</tr>"
        return r_
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
    def get_role_list(self, user_object_=None):
        
        
        wp_roles_ = wp_roles()
        role_list_ = Array()
        for role_ in user_object_.roles:
            if (php_isset(lambda : wp_roles_.role_names[role_])):
                role_list_[role_] = translate_user_role(wp_roles_.role_names[role_])
            # end if
        # end for
        if php_empty(lambda : role_list_):
            role_list_["none"] = _x("None", "no user roles")
        # end if
        #// 
        #// Filters the returned array of roles for a user.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[] $role_list   An array of user roles.
        #// @param WP_User  $user_object A WP_User object.
        #//
        return apply_filters("get_role_list", role_list_, user_object_)
    # end def get_role_list
# end class WP_Users_List_Table
