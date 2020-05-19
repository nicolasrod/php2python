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
    #// 
    #// Site status list.
    #// 
    #// @since 4.3.0
    #// @var array
    #//
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
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        self.status_list = Array({"archived": Array("site-archived", __("Archived")), "spam": Array("site-spammed", _x("Spam", "site")), "deleted": Array("site-deleted", __("Deleted")), "mature": Array("site-mature", __("Mature"))})
        super().__init__(Array({"plural": "sites", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
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
        global s_
        global mode_
        global wpdb_
        php_check_if_defined("s_","mode_","wpdb_")
        if (not php_empty(lambda : PHP_REQUEST["mode"])):
            mode_ = "excerpt" if "excerpt" == PHP_REQUEST["mode"] else "list"
            set_user_setting("sites_list_mode", mode_)
        else:
            mode_ = get_user_setting("sites_list_mode", "list")
        # end if
        per_page_ = self.get_items_per_page("sites_network_per_page")
        pagenum_ = self.get_pagenum()
        s_ = wp_unslash(php_trim(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        wild_ = ""
        if False != php_strpos(s_, "*"):
            wild_ = "*"
            s_ = php_trim(s_, "*")
        # end if
        #// 
        #// If the network is large and a search is not being performed, show only
        #// the latest sites with no paging in order to avoid expensive count queries.
        #//
        if (not s_) and wp_is_large_network():
            if (not (php_isset(lambda : PHP_REQUEST["orderby"]))):
                PHP_REQUEST["orderby"] = ""
                PHP_REQUEST["orderby"] = ""
            # end if
            if (not (php_isset(lambda : PHP_REQUEST["order"]))):
                PHP_REQUEST["order"] = "DESC"
                PHP_REQUEST["order"] = "DESC"
            # end if
        # end if
        args_ = Array({"number": php_intval(per_page_), "offset": php_intval(pagenum_ - 1 * per_page_), "network_id": get_current_network_id()})
        if php_empty(lambda : s_):
            pass
        elif php_preg_match("/^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$/", s_) or php_preg_match("/^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.?$/", s_) or php_preg_match("/^[0-9]{1,3}\\.[0-9]{1,3}\\.?$/", s_) or php_preg_match("/^[0-9]{1,3}\\.$/", s_):
            #// IPv4 address.
            sql_ = wpdb_.prepare(str("SELECT blog_id FROM ") + str(wpdb_.registration_log) + str(" WHERE ") + str(wpdb_.registration_log) + str(".IP LIKE %s"), wpdb_.esc_like(s_) + "%" if (not php_empty(lambda : wild_)) else "")
            reg_blog_ids_ = wpdb_.get_col(sql_)
            if reg_blog_ids_:
                args_["site__in"] = reg_blog_ids_
            # end if
        elif php_is_numeric(s_) and php_empty(lambda : wild_):
            args_["ID"] = s_
        else:
            args_["search"] = s_
            if (not is_subdomain_install()):
                args_["search_columns"] = Array("path")
            # end if
        # end if
        order_by_ = PHP_REQUEST["orderby"] if (php_isset(lambda : PHP_REQUEST["orderby"])) else ""
        if "registered" == order_by_:
            pass
        elif "lastupdated" == order_by_:
            order_by_ = "last_updated"
        elif "blogname" == order_by_:
            if is_subdomain_install():
                order_by_ = "domain"
            else:
                order_by_ = "path"
            # end if
        elif "blog_id" == order_by_:
            order_by_ = "id"
        elif (not order_by_):
            order_by_ = False
        # end if
        args_["orderby"] = order_by_
        if order_by_:
            args_["order"] = "DESC" if (php_isset(lambda : PHP_REQUEST["order"])) and "DESC" == php_strtoupper(PHP_REQUEST["order"]) else "ASC"
        # end if
        if wp_is_large_network():
            args_["no_found_rows"] = True
        else:
            args_["no_found_rows"] = False
        # end if
        #// Take into account the role the user has selected.
        status_ = wp_unslash(php_trim(PHP_REQUEST["status"])) if (php_isset(lambda : PHP_REQUEST["status"])) else ""
        if php_in_array(status_, Array("public", "archived", "mature", "spam", "deleted"), True):
            args_[status_] = 1
        # end if
        #// 
        #// Filters the arguments for the site query in the sites list table.
        #// 
        #// @since 4.6.0
        #// 
        #// @param array $args An array of get_sites() arguments.
        #//
        args_ = apply_filters("ms_sites_list_table_query_args", args_)
        _sites_ = get_sites(args_)
        if php_is_array(_sites_):
            update_site_cache(_sites_)
            self.items = php_array_slice(_sites_, 0, per_page_)
        # end if
        total_sites_ = get_sites(php_array_merge(args_, Array({"count": True, "offset": 0, "number": 0})))
        self.set_pagination_args(Array({"total_items": total_sites_, "per_page": per_page_}))
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
        
        
        counts_ = wp_count_sites()
        statuses_ = Array({"all": _nx_noop("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", "sites"), "public": _n_noop("Public <span class=\"count\">(%s)</span>", "Public <span class=\"count\">(%s)</span>"), "archived": _n_noop("Archived <span class=\"count\">(%s)</span>", "Archived <span class=\"count\">(%s)</span>"), "mature": _n_noop("Mature <span class=\"count\">(%s)</span>", "Mature <span class=\"count\">(%s)</span>"), "spam": _nx_noop("Spam <span class=\"count\">(%s)</span>", "Spam <span class=\"count\">(%s)</span>", "sites"), "deleted": _n_noop("Deleted <span class=\"count\">(%s)</span>", "Deleted <span class=\"count\">(%s)</span>")})
        view_links_ = Array()
        requested_status_ = wp_unslash(php_trim(PHP_REQUEST["status"])) if (php_isset(lambda : PHP_REQUEST["status"])) else ""
        url_ = "sites.php"
        for status_,label_count_ in statuses_.items():
            current_link_attributes_ = " class=\"current\" aria-current=\"page\"" if requested_status_ == status_ or "" == requested_status_ and "all" == status_ else ""
            if php_int(counts_[status_]) > 0:
                label_ = php_sprintf(translate_nooped_plural(label_count_, counts_[status_]), number_format_i18n(counts_[status_]))
                full_url_ = url_ if "all" == status_ else add_query_arg("status", status_, url_)
                view_links_[status_] = php_sprintf("<a href=\"%1$s\"%2$s>%3$s</a>", esc_url(full_url_), current_link_attributes_, label_)
            # end if
        # end for
        return view_links_
    # end def get_views
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        actions_ = Array()
        if current_user_can("delete_sites"):
            actions_["delete"] = __("Delete")
        # end if
        actions_["spam"] = _x("Mark as Spam", "site")
        actions_["notspam"] = _x("Not Spam", "site")
        return actions_
    # end def get_bulk_actions
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param string $which The location of the pagination nav markup: 'top' or 'bottom'.
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
    #// Extra controls to be displayed between bulk actions and pagination.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
    #//
    def extra_tablenav(self, which_=None):
        
        
        php_print("     <div class=\"alignleft actions\">\n     ")
        if "top" == which_:
            ob_start()
            #// 
            #// Fires before the Filter button on the MS sites list table.
            #// 
            #// @since 5.3.0
            #// 
            #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
            #//
            do_action("restrict_manage_sites", which_)
            output_ = ob_get_clean()
            if (not php_empty(lambda : output_)):
                php_print(output_)
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
        do_action("manage_sites_extra_tablenav", which_)
    # end def extra_tablenav
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        sites_columns_ = Array({"cb": "<input type=\"checkbox\" />", "blogname": __("URL"), "lastupdated": __("Last Updated"), "registered": _x("Registered", "site"), "users": __("Users")})
        if has_filter("wpmublogsaction"):
            sites_columns_["plugins"] = __("Actions")
        # end if
        #// 
        #// Filters the displayed site columns in Sites list table.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param string[] $sites_columns An array of displayed site columns. Default 'cb',
        #// 'blogname', 'lastupdated', 'registered', 'users'.
        #//
        return apply_filters("wpmu_blogs_columns", sites_columns_)
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
    def column_cb(self, blog_=None):
        
        
        if (not is_main_site(blog_["blog_id"])):
            blogname_ = untrailingslashit(blog_["domain"] + blog_["path"])
            php_print("         <label class=\"screen-reader-text\" for=\"blog_")
            php_print(blog_["blog_id"])
            php_print("\">\n                ")
            #// translators: %s: Site URL.
            printf(__("Select %s"), blogname_)
            php_print("         </label>\n          <input type=\"checkbox\" id=\"blog_")
            php_print(blog_["blog_id"])
            php_print("\" name=\"allblogs[]\" value=\"")
            php_print(esc_attr(blog_["blog_id"]))
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
    def column_id(self, blog_=None):
        
        
        php_print(blog_["blog_id"])
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
    def column_blogname(self, blog_=None):
        
        
        global mode_
        php_check_if_defined("mode_")
        blogname_ = untrailingslashit(blog_["domain"] + blog_["path"])
        php_print("     <strong>\n          <a href=\"")
        php_print(esc_url(network_admin_url("site-info.php?id=" + blog_["blog_id"])))
        php_print("\" class=\"edit\">")
        php_print(blogname_)
        php_print("</a>\n           ")
        self.site_states(blog_)
        php_print("     </strong>\n     ")
        if "list" != mode_:
            switch_to_blog(blog_["blog_id"])
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
    def column_lastupdated(self, blog_=None):
        
        
        global mode_
        php_check_if_defined("mode_")
        if "list" == mode_:
            date_ = __("Y/m/d")
        else:
            date_ = __("Y/m/d g:i:s a")
        # end if
        php_print(__("Never") if "0000-00-00 00:00:00" == blog_["last_updated"] else mysql2date(date_, blog_["last_updated"]))
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
    def column_registered(self, blog_=None):
        
        
        global mode_
        php_check_if_defined("mode_")
        if "list" == mode_:
            date_ = __("Y/m/d")
        else:
            date_ = __("Y/m/d g:i:s a")
        # end if
        if "0000-00-00 00:00:00" == blog_["registered"]:
            php_print("&#x2014;")
        else:
            php_print(mysql2date(date_, blog_["registered"]))
        # end if
    # end def column_registered
    #// 
    #// Handles the users column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $blog Current site.
    #//
    def column_users(self, blog_=None):
        
        
        user_count_ = wp_cache_get(blog_["blog_id"] + "_user_count", "blog-details")
        if (not user_count_):
            blog_users_ = php_new_class("WP_User_Query", lambda : WP_User_Query(Array({"blog_id": blog_["blog_id"], "fields": "ID", "number": 1, "count_total": True})))
            user_count_ = blog_users_.get_total()
            wp_cache_set(blog_["blog_id"] + "_user_count", user_count_, "blog-details", 12 * HOUR_IN_SECONDS)
        # end if
        printf("<a href=\"%s\">%s</a>", esc_url(network_admin_url("site-users.php?id=" + blog_["blog_id"])), number_format_i18n(user_count_))
    # end def column_users
    #// 
    #// Handles the plugins column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $blog Current site.
    #//
    def column_plugins(self, blog_=None):
        
        
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
            do_action("wpmublogsaction", blog_["blog_id"])
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
    def column_default(self, blog_=None, column_name_=None):
        
        
        #// 
        #// Fires for each registered custom column in the Sites list table.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $column_name The name of the column to display.
        #// @param int    $blog_id     The site ID.
        #//
        do_action("manage_sites_custom_column", column_name_, blog_["blog_id"])
    # end def column_default
    #// 
    #// @global string $mode
    #//
    def display_rows(self):
        
        
        for blog_ in self.items:
            blog_ = blog_.to_array()
            class_ = ""
            reset(self.status_list)
            for status_,col_ in self.status_list.items():
                if 1 == blog_[status_]:
                    class_ = str(" class='") + str(col_[0]) + str("'")
                # end if
            # end for
            php_print(str("<tr") + str(class_) + str(">"))
            self.single_row_columns(blog_)
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
    def site_states(self, site_=None):
        
        
        site_states_ = Array()
        #// $site is still an array, so get the object.
        _site_ = WP_Site.get_instance(site_["blog_id"])
        if is_main_site(_site_.id):
            site_states_["main"] = __("Main")
        # end if
        reset(self.status_list)
        site_status_ = wp_unslash(php_trim(PHP_REQUEST["status"])) if (php_isset(lambda : PHP_REQUEST["status"])) else ""
        for status_,col_ in self.status_list.items():
            if 1 == php_intval(_site_.status_) and site_status_ != status_:
                site_states_[col_[0]] = col_[1]
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
        site_states_ = apply_filters("display_site_states", site_states_, _site_)
        if (not php_empty(lambda : site_states_)):
            state_count_ = php_count(site_states_)
            i_ = 0
            php_print(" &mdash; ")
            for state_ in site_states_:
                i_ += 1
                sep_ = "" if i_ == state_count_ else ", "
                php_print(str("<span class='post-state'>") + str(state_) + str(sep_) + str("</span>"))
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
    def handle_row_actions(self, blog_=None, column_name_=None, primary_=None):
        
        
        if primary_ != column_name_:
            return ""
        # end if
        blogname_ = untrailingslashit(blog_["domain"] + blog_["path"])
        #// Preordered.
        actions_ = Array({"edit": "", "backend": "", "activate": "", "deactivate": "", "archive": "", "unarchive": "", "spam": "", "unspam": "", "delete": "", "visit": ""})
        actions_["edit"] = "<a href=\"" + esc_url(network_admin_url("site-info.php?id=" + blog_["blog_id"])) + "\">" + __("Edit") + "</a>"
        actions_["backend"] = "<a href='" + esc_url(get_admin_url(blog_["blog_id"])) + "' class='edit'>" + __("Dashboard") + "</a>"
        if get_network().site_id != blog_["blog_id"]:
            if "1" == blog_["deleted"]:
                actions_["activate"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=activateblog&amp;id=" + blog_["blog_id"]), "activateblog_" + blog_["blog_id"])) + "\">" + __("Activate") + "</a>"
            else:
                actions_["deactivate"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=deactivateblog&amp;id=" + blog_["blog_id"]), "deactivateblog_" + blog_["blog_id"])) + "\">" + __("Deactivate") + "</a>"
            # end if
            if "1" == blog_["archived"]:
                actions_["unarchive"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=unarchiveblog&amp;id=" + blog_["blog_id"]), "unarchiveblog_" + blog_["blog_id"])) + "\">" + __("Unarchive") + "</a>"
            else:
                actions_["archive"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=archiveblog&amp;id=" + blog_["blog_id"]), "archiveblog_" + blog_["blog_id"])) + "\">" + _x("Archive", "verb; site") + "</a>"
            # end if
            if "1" == blog_["spam"]:
                actions_["unspam"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=unspamblog&amp;id=" + blog_["blog_id"]), "unspamblog_" + blog_["blog_id"])) + "\">" + _x("Not Spam", "site") + "</a>"
            else:
                actions_["spam"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=spamblog&amp;id=" + blog_["blog_id"]), "spamblog_" + blog_["blog_id"])) + "\">" + _x("Spam", "site") + "</a>"
            # end if
            if current_user_can("delete_site", blog_["blog_id"]):
                actions_["delete"] = "<a href=\"" + esc_url(wp_nonce_url(network_admin_url("sites.php?action=confirm&amp;action2=deleteblog&amp;id=" + blog_["blog_id"]), "deleteblog_" + blog_["blog_id"])) + "\">" + __("Delete") + "</a>"
            # end if
        # end if
        actions_["visit"] = "<a href='" + esc_url(get_home_url(blog_["blog_id"], "/")) + "' rel='bookmark'>" + __("Visit") + "</a>"
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
        actions_ = apply_filters("manage_sites_action_links", php_array_filter(actions_), blog_["blog_id"], blogname_)
        return self.row_actions(actions_)
    # end def handle_row_actions
# end class WP_MS_Sites_List_Table
