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
#// List Table API: WP_MS_Sites_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying sites in a list table for the network admin.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_MS_Sites_List_Table(WP_List_Table):
    status_list = Array()
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
        
        self.status_list = Array({"archived": Array("site-archived", __("Archived")), "spam": Array("site-spammed", _x("Spam", "site")), "deleted": Array("site-deleted", __("Deleted")), "mature": Array("site-mature", __("Mature"))})
        super().__init__(Array({"plural": "sites", "screen": args["screen"] if (php_isset(lambda : args["screen"])) else None}))
    # end def __init__
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        return current_user_can("manage_sites")
    # end def ajax_user_can
    #// 
    #// Prepares the list of sites for display.
    #// 
    #// @since 3.1.0
    #// 
    #// @global string $s
    #// @global string $mode
    #// @global wpdb   $wpdb WordPress database abstraction object.
    #//
    def prepare_items(self):
        global PHP_REQUEST
        global s,mode,wpdb
        php_check_if_defined("s","mode","wpdb")
        if (not php_empty(lambda : PHP_REQUEST["mode"])):
            mode = "excerpt" if "excerpt" == PHP_REQUEST["mode"] else "list"
            set_user_setting("sites_list_mode", mode)
        else:
            mode = get_user_setting("sites_list_mode", "list")
        # end if
        per_page = self.get_items_per_page("sites_network_per_page")
        pagenum = self.get_pagenum()
        s = wp_unslash(php_trim(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        wild = ""
        if False != php_strpos(s, "*"):
            wild = "*"
            s = php_trim(s, "*")
        # end if
        #// 
        #// If the network is large and a search is not being performed, show only
        #// the latest sites with no paging in order to avoid expensive count queries.
        #//
        if (not s) and wp_is_large_network():
            if (not (php_isset(lambda : PHP_REQUEST["orderby"]))):
                PHP_REQUEST["orderby"] = ""
                PHP_REQUEST["orderby"] = ""
            # end if
            if (not (php_isset(lambda : PHP_REQUEST["order"]))):
                PHP_REQUEST["order"] = "DESC"
                PHP_REQUEST["order"] = "DESC"
            # end if
        # end if
        args = Array({"number": php_intval(per_page), "offset": php_intval(pagenum - 1 * per_page), "network_id": get_current_network_id()})
        if php_empty(lambda : s):
            pass
        elif php_preg_match("/^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$/", s) or php_preg_match("/^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.?$/", s) or php_preg_match("/^[0-9]{1,3}\\.[0-9]{1,3}\\.?$/", s) or php_preg_match("/^[0-9]{1,3}\\.$/", s):
            #// IPv4 address.
            sql = wpdb.prepare(str("SELECT blog_id FROM ") + str(wpdb.registration_log) + str(" WHERE ") + str(wpdb.registration_log) + str(".IP LIKE %s"), wpdb.esc_like(s) + "%" if (not php_empty(lambda : wild)) else "")
            reg_blog_ids = wpdb.get_col(sql)
            if reg_blog_ids:
                args["site__in"] = reg_blog_ids
            # end if
        elif php_is_numeric(s) and php_empty(lambda : wild):
            args["ID"] = s
        else:
            args["search"] = s
            if (not is_subdomain_install()):
                args["search_columns"] = Array("path")
            # end if
        # end if
        order_by = PHP_REQUEST["orderby"] if (php_isset(lambda : PHP_REQUEST["orderby"])) else ""
        if "registered" == order_by:
            pass
        elif "lastupdated" == order_by:
            order_by = "last_updated"
        elif "blogname" == order_by:
            if is_subdomain_install():
                order_by = "domain"
            else:
                order_by = "path"
            # end if
        elif "blog_id" == order_by:
            order_by = "id"
        elif (not order_by):
            order_by = False
        # end if
        args["orderby"] = order_by
        if order_by:
            args["order"] = "DESC" if (php_isset(lambda : PHP_REQUEST["order"])) and "DESC" == php_strtoupper(PHP_REQUEST["order"]) else "ASC"
        # end if
        if wp_is_large_network():
            args["no_found_rows"] = True
        else:
            args["no_found_rows"] = False
        # end if
        #// Take into account the role the user has selected.
        status = wp_unslash(php_trim(PHP_REQUEST["status"])) if (php_isset(lambda : PHP_REQUEST["status"])) else ""
        if php_in_array(status, Array("public", "archived", "mature", "spam", "deleted"), True):
            args[status] = 1
        # end if
        #// 
        #// Filters the arguments for the site query in the sites list table.
        #// 
        #// @since 4.6.0
        #// 
        #// @param array $args An array of get_sites() arguments.
        #//
        args = apply_filters("ms_sites_list_table_query_args", args)
        _sites = get_sites(args)
        if php_is_array(_sites):
            update_site_cache(_sites)
            self.items = php_array_slice(_sites, 0, per_page)
        # end if
        total_sites = get_sites(php_array_merge(args, Array({"count": True, "offset": 0, "number": 0})))
        self.set_pagination_args(Array({"total_items": total_sites, "per_page": per_page}))
    # end def prepare_items
    #// 
    #//
    def no_items(self):
        
        _e("No sites found.")
    # end def no_items
    #// 
    #// Gets links to filter sites by status.
    #// 
    #// @since 5.3.0
    #// 
    #// @return array
    #// 
    #//
    def get_views(self):
        
        counts = wp_count_sites()
        statuses = Array({"all": _nx_noop("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", "sites"), "public": _n_noop("Public <span class=\"count\">(%s)</span>", "Public <span class=\"count\">(%s)</span>"), "archived": _n_noop("Archived <span class=\"count\">(%s)</span>", "Archived <span class=\"count\">(%s)</span>"), "mature": _n_noop("Mature <span class=\"count\">(%s)</span>", "Mature <span class=\"count\">(%s)</span>"), "spam": _nx_noop("Spam <span class=\"count\">(%s)</span>", "Spam <span class=\"count\">(%s)</span>", "sites"), "deleted": _n_noop("Deleted <span class=\"count\">(%s)</span>", "Deleted <span class=\"count\">(%s)</span>")})
        view_links = Array()
        requested_status = wp_unslash(php_trim(PHP_REQUEST["status"])) if (php_isset(lambda : PHP_REQUEST["status"])) else ""
        url = "sites.php"
        for status,label_count in statuses:
            current_link_attributes = " class=\"current\" aria-current=\"page\"" if requested_status == status or "" == requested_status and "all" == status else ""
            if int(counts[status]) > 0:
                label = php_sprintf(translate_nooped_plural(label_count, counts[status]), number_format_i18n(counts[status]))
                full_url = url if "all" == status else add_query_arg("status", status, url)
                view_links[status] = php_sprintf("<a href=\"%1$s\"%2$s>%3$s</a>", esc_url(full_url), current_link_attributes, label)
            # end if
        # end for
        return view_links
    # end def get_views
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        actions = Array()
        if current_user_can("delete_sites"):
            actions["delete"] = __("Delete")
        # end if
        actions["spam"] = _x("Mark as Spam", "site")
        actions["notspam"] = _x("Not Spam", "site")
        return actions
    # end def get_bulk_actions
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param string $which The location of the pagination nav markup: 'top' or 'bottom'.
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
    #// Extra controls to be displayed between bulk actions and pagination.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
    #//
    def extra_tablenav(self, which=None):
        
        php_print("     <div class=\"alignleft actions\">\n     ")
        if "top" == which:
            ob_start()
            #// 
            #// Fires before the Filter button on the MS sites list table.
            #// 
            #// @since 5.3.0
            #// 
            #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
            #//
            do_action("restrict_manage_sites", which)
            output = ob_get_clean()
            if (not php_empty(lambda : output)):
                php_print(output)
                submit_button(__("Filter"), "", "filter_action", False, Array({"id": "site-query-submit"}))
            # end if
        # end if
        php_print("     </div>\n        ")
        #// 
        #// Fires immediately following the closing "actions" div in the tablenav for the
        #// MS sites list table.
        #// 
        #// @since 5.3.0
        #// 
        #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
        #//
        do_action("manage_sites_extra_tablenav", which)
    # end def extra_tablenav
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        sites_columns = Array({"cb": "<input type=\"checkbox\" />", "blogname": __("URL"), "lastupdated": __("Last Updated"), "registered": _x("Registered", "site"), "users": __("Users")})
        if has_filter("wpmublogsaction"):
            sites_columns["plugins"] = __("Actions")
        # end if
        #// 
        #// Filters the displayed site columns in Sites list table.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param string[] $sites_columns An array of displayed site columns. Default 'cb',
        #// 'blogname', 'lastupdated', 'registered', 'users'.
        #//
        return apply_filters("wpmu_blogs_columns", sites_columns)
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        return Array({"blogname": "blogname", "lastupdated": "lastupdated", "registered": "blog_id"})
    # end def get_sortable_columns
    #// 
    #// Handles the checkbox column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $blog Current site.
    #//
    def column_cb(self, blog=None):
        
        if (not is_main_site(blog["blog_id"])):
            blogname = untrailingslashit(blog["domain"] + blog["path"])
            php_print("         <label class=\"screen-reader-text\" for=\"blog_")
            php_print(blog["blog_id"])
            php_print("\">\n                ")
            #// translators: %s: Site URL.
            printf(__("Select %s"), blogname)
            php_print("         </label>\n          <input type=\"checkbox\" id=\"blog_")
            php_print(blog["blog_id"])
            php_print("\" name=\"allblogs[]\" value=\"")
            php_print(esc_attr(blog["blog_id"]))
            php_print("\" />\n          ")
        # end if
    # end def column_cb
    #// 
    #// Handles the ID column output.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $blog Current site.
    #//
    def column_id(self, blog=None):
        
        php_print(blog["blog_id"])
    # end def column_id
    #// 
    #// Handles the site name column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param array $blog Current site.
    #//
    def column_blogname(self, blog=None):
        
        global mode
        php_check_if_defined("mode")
        blogname = untrailingslashit(blog["domain"] + blog["path"])
        php_print("     <strong>\n          <a href=\"")
        php_print(esc_url(network_admin_url("site-info.php?id=" + blog["blog_id"])))
        php_print("\" class=\"edit\">")
        php_print(blogname)
        php_print("</a>\n           ")
        self.site_states(blog)
        php_print("     </strong>\n     ")
        if "list" != mode:
            switch_to_blog(blog["blog_id"])
            php_print("<p>")
            printf(__("%1$s &#8211; %2$s"), get_option("blogname"), "<em>" + get_option("blogdescription") + "</em>")
            php_print("</p>")
            restore_current_blog()
        # end if
    # end def column_blogname
    #// 
    #// Handles the lastupdated column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param array $blog Current site.
    #//
    def column_lastupdated(self, blog=None):
        
        global mode
        php_check_if_defined("mode")
        if "list" == mode:
            date = __("Y/m/d")
        else:
            date = __("Y/m/d g:i:s a")
        # end if
        php_print(__("Never") if "0000-00-00 00:00:00" == blog["last_updated"] else mysql2date(date, blog["last_updated"]))
    # end def column_lastupdated
    #// 
    #// Handles the registered column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param array $blog Current site.
    #//
    def column_registered(self, blog=None):
        
        global mode
        php_check_if_defined("mode")
        if "list" == mode:
            date = __("Y/m/d")
        else:
            date = __("Y/m/d g:i:s a")
        # end if
        if "0000-00-00 00:00:00" == blog["registered"]:
            php_print("&#x2014;")
        else:
            php_print(mysql2date(date, blog["registered"]))
        # end if
    # end def column_registered
    #// 
    #// Handles the users column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $blog Current site.
    #//
    def column_users(self, blog=None):
        
        user_count = wp_cache_get(blog["blog_id"] + "_user_count", "blog-details")
        if (not user_count):
            blog_users = php_new_class("WP_User_Query", lambda : WP_User_Query(Array({"blog_id": blog["blog_id"], "fields": "ID", "number": 1, "count_total": True})))
            user_count = blog_users.get_total()
            wp_cache_set(blog["blog_id"] + "_user_count", user_count, "blog-details", 12 * HOUR_IN_SECONDS)
        # end if
        printf("<a href=\"%s\">%s</a>", esc_url(network_admin_url("site-users.php?id=" + blog["blog_id"])), number_format_i18n(user_count))
    # end def column_users
    #// 
    #// Handles the plugins column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $blog Current site.
    #//
    def column_plugins(self, blog=None):
        
        if has_filter("wpmublogsaction"):
            #// 
            #// Fires inside the auxiliary 'Actions' column of the Sites list table.
            #// 
            #// By default this column is hidden unless something is hooked to the action.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $blog_id The site ID.
            #//
            do_action("wpmublogsaction", blog["blog_id"])
        # end if
    # end def column_plugins
    #// 
    #// Handles output for the default column.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array  $blog        Current site.
    #// @param string $column_name Current column name.
    #//
    def column_default(self, blog=None, column_name=None):
        
        #// 
        #// Fires for each registered custom column in the Sites list table.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $column_name The name of the column to display.
        #// @param int    $blog_id     The site ID.
        #//
        do_action("manage_sites_custom_column", column_name, blog["blog_id"])
    # end def column_default
    #// 
    #// @global string $mode
    #//
    def display_rows(self):
        
        for blog in self.items:
            blog = blog.to_array()
            class_ = ""
            reset(self.status_list)
            for status,col in self.status_list:
                if 1 == blog[status]:
                    class_ = str(" class='") + str(col[0]) + str("'")
                # end if
            # end for
            php_print(str("<tr") + str(class_) + str(">"))
            self.single_row_columns(blog)
            php_print("</tr>")
        # end for
    # end def display_rows
    #// 
    #// Maybe output comma-separated site states.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $site
    #//
    def site_states(self, site=None):
        
        site_states = Array()
        #// $site is still an array, so get the object.
        _site = WP_Site.get_instance(site["blog_id"])
        if is_main_site(_site.id):
            site_states["main"] = __("Main")
        # end if
        reset(self.status_list)
        site_status = wp_unslash(php_trim(PHP_REQUEST["status"])) if (php_isset(lambda : PHP_REQUEST["status"])) else ""
        for status,col in self.status_list:
            if 1 == php_intval(_site.status) and site_status != status:
                site_states[col[0]] = col[1]
            # end if
        # end for
        #// 
        #// Filter the default site display states for items in the Sites list table.
        #// 
        #// @since 5.3.0
        #// 
        #// @param array $site_states An array of site states. Default 'Main',
        #// 'Archived', 'Mature', 'Spam', 'Deleted'.
        #// @param WP_Site $site The current site object.
        #//
        site_states = apply_filters("display_site_states", site_states, _site)
        if (not php_empty(lambda : site_states)):
            state_count = php_count(site_states)
            i = 0
            php_print(" &mdash; ")
            for state in site_states:
                i += 1
                sep = "" if i == state_count else ", "
                php_print(str("<span class='post-state'>") + str(state) + str(sep) + str("</span>"))
            # end for
        # end if
    # end def site_states
    #// 
    #// Gets the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, 'blogname'.
    #//
    def get_default_primary_column_name(self):
        
        return "blogname"
    # end def get_default_primary_column_name
    #// 
    #// Generates and displays row action links.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $blog        Site being acted upon.
    #// @param string $column_name Current column name.
    #// @param string $primary     Primary column name.
    #// @return string Row actions output for sites in Multisite, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, blog=None, column_name=None, primary=None):
        
        if primary != column_name:
            return ""
        # end if
        blogname = untrailingslashit(blog["domain"] + blog["path"])
        #// Preordered.
        actions = Array({"edit": "", "backend": "", "activate": "", "deactivate": "", "archive": "", "unarchive": "", "spam": "", "unspam": "", "delete": "", "visit": ""})
        actions["edit"] = "<a href=\"" + esc_url(network_admin_url("site-info.php?id=" + blog["blog_id"])) + "\">" + __("Edit") + "</a>"
        actions["backend"] = "<a href='" + esc_url(get_admin_url(blog["blog_id"])) + "' class='edit'>" + __("Dashboard") + "</a>"
        if get_network().site_id != blog["blog_id"]:
            if "1" == blog["deleted"]:
                actions["activate"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=activateblog&amp;id=" + blog["blog_id"]), "activateblog_" + blog["blog_id"])) + "\">" + __("Activate") + "</a>"
            else:
                actions["deactivate"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=deactivateblog&amp;id=" + blog["blog_id"]), "deactivateblog_" + blog["blog_id"])) + "\">" + __("Deactivate") + "</a>"
            # end if
            if "1" == blog["archived"]:
                actions["unarchive"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=unarchiveblog&amp;id=" + blog["blog_id"]), "unarchiveblog_" + blog["blog_id"])) + "\">" + __("Unarchive") + "</a>"
            else:
                actions["archive"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=archiveblog&amp;id=" + blog["blog_id"]), "archiveblog_" + blog["blog_id"])) + "\">" + _x("Archive", "verb; site") + "</a>"
            # end if
            if "1" == blog["spam"]:
                actions["unspam"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=unspamblog&amp;id=" + blog["blog_id"]), "unspamblog_" + blog["blog_id"])) + "\">" + _x("Not Spam", "site") + "</a>"
            else:
                actions["spam"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=spamblog&amp;id=" + blog["blog_id"]), "spamblog_" + blog["blog_id"])) + "\">" + _x("Spam", "site") + "</a>"
            # end if
            if current_user_can("delete_site", blog["blog_id"]):
                actions["delete"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=deleteblog&amp;id=" + blog["blog_id"]), "deleteblog_" + blog["blog_id"])) + "\">" + __("Delete") + "</a>"
            # end if
        # end if
        actions["visit"] = "<a href='" + esc_url(get_home_url(blog["blog_id"], "/")) + "' rel='bookmark'>" + __("Visit") + "</a>"
        #// 
        #// Filters the action links displayed for each site in the Sites list table.
        #// 
        #// The 'Edit', 'Dashboard', 'Delete', and 'Visit' links are displayed by
        #// default for each site. The site's status determines whether to show the
        #// 'Activate' or 'Deactivate' link, 'Unarchive' or 'Archive' links, and
        #// 'Not Spam' or 'Spam' link for each site.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[] $actions  An array of action links to be displayed.
        #// @param int      $blog_id  The site ID.
        #// @param string   $blogname Site path, formatted depending on whether it is a sub-domain
        #// or subdirectory multisite installation.
        #//
        actions = apply_filters("manage_sites_action_links", php_array_filter(actions), blog["blog_id"], blogname)
        return self.row_actions(actions)
    # end def handle_row_actions
# end class WP_MS_Sites_List_Table
