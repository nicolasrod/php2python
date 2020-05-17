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
#// List Table API: WP_Plugins_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying installed plugins in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Plugins_List_Table(WP_List_Table):
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @see WP_List_Table::__construct() for more information on default arguments.
    #// 
    #// @global string $status
    #// @global int    $page
    #// 
    #// @param array $args An associative array of arguments.
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        global PHP_SERVER
        global status_
        global page_
        php_check_if_defined("status_","page_")
        super().__init__(Array({"plural": "plugins", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
        status_ = "all"
        if (php_isset(lambda : PHP_REQUEST["plugin_status"])) and php_in_array(PHP_REQUEST["plugin_status"], Array("active", "inactive", "recently_activated", "upgrade", "mustuse", "dropins", "search", "paused")):
            status_ = PHP_REQUEST["plugin_status"]
        # end if
        if (php_isset(lambda : PHP_REQUEST["s"])):
            PHP_SERVER["REQUEST_URI"] = add_query_arg("s", wp_unslash(PHP_REQUEST["s"]))
        # end if
        page_ = self.get_pagenum()
    # end def __init__
    #// 
    #// @return array
    #//
    def get_table_classes(self):
        
        
        return Array("widefat", self._args["plural"])
    # end def get_table_classes
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        
        return current_user_can("activate_plugins")
    # end def ajax_user_can
    #// 
    #// @global string $status
    #// @global array  $plugins
    #// @global array  $totals
    #// @global int    $page
    #// @global string $orderby
    #// @global string $order
    #// @global string $s
    #//
    def prepare_items(self):
        
        
        global status_
        global plugins_
        global totals_
        global page_
        global orderby_
        global order_
        global s_
        php_check_if_defined("status_","plugins_","totals_","page_","orderby_","order_","s_")
        wp_reset_vars(Array("orderby", "order"))
        #// 
        #// Filters the full array of plugins to list in the Plugins list table.
        #// 
        #// @since 3.0.0
        #// 
        #// @see get_plugins()
        #// 
        #// @param array $all_plugins An array of plugins to display in the list table.
        #//
        all_plugins_ = apply_filters("all_plugins", get_plugins())
        plugins_ = Array({"all": all_plugins_, "search": Array(), "active": Array(), "inactive": Array(), "recently_activated": Array(), "upgrade": Array(), "mustuse": Array(), "dropins": Array(), "paused": Array()})
        screen_ = self.screen
        if (not is_multisite()) or screen_.in_admin("network") and current_user_can("manage_network_plugins"):
            #// 
            #// Filters whether to display the advanced plugins list table.
            #// 
            #// There are two types of advanced plugins - must-use and drop-ins -
            #// which can be used in a single site or Multisite network.
            #// 
            #// The $type parameter allows you to differentiate between the type of advanced
            #// plugins to filter the display of. Contexts include 'mustuse' and 'dropins'.
            #// 
            #// @since 3.0.0
            #// 
            #// @param bool   $show Whether to show the advanced plugins for the specified
            #// plugin type. Default true.
            #// @param string $type The plugin type. Accepts 'mustuse', 'dropins'.
            #//
            if apply_filters("show_advanced_plugins", True, "mustuse"):
                plugins_["mustuse"] = get_mu_plugins()
            # end if
            #// This action is documented in wp-admin/includes/class-wp-plugins-list-table.php
            if apply_filters("show_advanced_plugins", True, "dropins"):
                plugins_["dropins"] = get_dropins()
            # end if
            if current_user_can("update_plugins"):
                current_ = get_site_transient("update_plugins")
                for plugin_file_,plugin_data_ in plugins_["all"]:
                    if (php_isset(lambda : current_.response[plugin_file_])):
                        plugins_["all"][plugin_file_]["update"] = True
                        plugins_["upgrade"][plugin_file_] = plugins_["all"][plugin_file_]
                    # end if
                # end for
            # end if
        # end if
        if (not screen_.in_admin("network")):
            show_ = current_user_can("manage_network_plugins")
            #// 
            #// Filters whether to display network-active plugins alongside plugins active for the current site.
            #// 
            #// This also controls the display of inactive network-only plugins (plugins with
            #// "Network: true" in the plugin header).
            #// 
            #// Plugins cannot be network-activated or network-deactivated from this screen.
            #// 
            #// @since 4.4.0
            #// 
            #// @param bool $show Whether to show network-active plugins. Default is whether the current
            #// user can manage network plugins (ie. a Super Admin).
            #//
            show_network_active_ = apply_filters("show_network_active_plugins", show_)
        # end if
        if screen_.in_admin("network"):
            recently_activated_ = get_site_option("recently_activated", Array())
        else:
            recently_activated_ = get_option("recently_activated", Array())
        # end if
        for key_,time_ in recently_activated_:
            if time_ + WEEK_IN_SECONDS < time():
                recently_activated_[key_] = None
            # end if
        # end for
        if screen_.in_admin("network"):
            update_site_option("recently_activated", recently_activated_)
        else:
            update_option("recently_activated", recently_activated_)
        # end if
        plugin_info_ = get_site_transient("update_plugins")
        for plugin_file_,plugin_data_ in plugins_["all"]:
            #// Extra info if known. array_merge() ensures $plugin_data has precedence if keys collide.
            if (php_isset(lambda : plugin_info_.response[plugin_file_])):
                plugin_data_ = php_array_merge(plugin_info_.response[plugin_file_], plugin_data_)
                plugins_["all"][plugin_file_] = plugin_data_
                #// Make sure that $plugins['upgrade'] also receives the extra info since it is used on ?plugin_status=upgrade.
                if (php_isset(lambda : plugins_["upgrade"][plugin_file_])):
                    plugins_["upgrade"][plugin_file_] = plugin_data_
                # end if
            elif (php_isset(lambda : plugin_info_.no_update[plugin_file_])):
                plugin_data_ = php_array_merge(plugin_info_.no_update[plugin_file_], plugin_data_)
                plugins_["all"][plugin_file_] = plugin_data_
                #// Make sure that $plugins['upgrade'] also receives the extra info since it is used on ?plugin_status=upgrade.
                if (php_isset(lambda : plugins_["upgrade"][plugin_file_])):
                    plugins_["upgrade"][plugin_file_] = plugin_data_
                # end if
            # end if
            #// Filter into individual sections.
            if is_multisite() and (not screen_.in_admin("network")) and is_network_only_plugin(plugin_file_) and (not is_plugin_active(plugin_file_)):
                if show_network_active_:
                    #// On the non-network screen, show inactive network-only plugins if allowed.
                    plugins_["inactive"][plugin_file_] = plugin_data_
                else:
                    plugins_["all"][plugin_file_] = None
                # end if
            elif (not screen_.in_admin("network")) and is_plugin_active_for_network(plugin_file_):
                if show_network_active_:
                    #// On the non-network screen, show network-active plugins if allowed.
                    plugins_["active"][plugin_file_] = plugin_data_
                else:
                    plugins_["all"][plugin_file_] = None
                # end if
            elif (not screen_.in_admin("network")) and is_plugin_active(plugin_file_) or screen_.in_admin("network") and is_plugin_active_for_network(plugin_file_):
                #// On the non-network screen, populate the active list with plugins that are individually activated.
                #// On the network admin screen, populate the active list with plugins that are network-activated.
                plugins_["active"][plugin_file_] = plugin_data_
                if (not screen_.in_admin("network")) and is_plugin_paused(plugin_file_):
                    plugins_["paused"][plugin_file_] = plugin_data_
                # end if
            else:
                if (php_isset(lambda : recently_activated_[plugin_file_])):
                    #// Populate the recently activated list with plugins that have been recently activated.
                    plugins_["recently_activated"][plugin_file_] = plugin_data_
                # end if
                #// Populate the inactive list with plugins that aren't activated.
                plugins_["inactive"][plugin_file_] = plugin_data_
            # end if
        # end for
        if php_strlen(s_):
            status_ = "search"
            plugins_["search"] = php_array_filter(plugins_["all"], Array(self, "_search_callback"))
        # end if
        totals_ = Array()
        for type_,list_ in plugins_:
            totals_[type_] = php_count(list_)
        # end for
        if php_empty(lambda : plugins_[status_]) and (not php_in_array(status_, Array("all", "search"))):
            status_ = "all"
        # end if
        self.items = Array()
        for plugin_file_,plugin_data_ in plugins_[status_]:
            #// Translate, don't apply markup, sanitize HTML.
            self.items[plugin_file_] = _get_plugin_data_markup_translate(plugin_file_, plugin_data_, False, True)
        # end for
        total_this_page_ = totals_[status_]
        js_plugins_ = Array()
        for key_,list_ in plugins_:
            js_plugins_[key_] = php_array_keys(list_)
        # end for
        wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"plugins": js_plugins_, "totals": wp_get_update_data()}))
        if (not orderby_):
            orderby_ = "Name"
        else:
            orderby_ = ucfirst(orderby_)
        # end if
        order_ = php_strtoupper(order_)
        uasort(self.items, Array(self, "_order_callback"))
        plugins_per_page_ = self.get_items_per_page(php_str_replace("-", "_", screen_.id + "_per_page"), 999)
        start_ = page_ - 1 * plugins_per_page_
        if total_this_page_ > plugins_per_page_:
            self.items = php_array_slice(self.items, start_, plugins_per_page_)
        # end if
        self.set_pagination_args(Array({"total_items": total_this_page_, "per_page": plugins_per_page_}))
    # end def prepare_items
    #// 
    #// @global string $s URL encoded search term.
    #// 
    #// @param array $plugin
    #// @return bool
    #//
    def _search_callback(self, plugin_=None):
        
        
        global s_
        php_check_if_defined("s_")
        for value_ in plugin_:
            if php_is_string(value_) and False != php_stripos(strip_tags(value_), urldecode(s_)):
                return True
            # end if
        # end for
        return False
    # end def _search_callback
    #// 
    #// @global string $orderby
    #// @global string $order
    #// @param array $plugin_a
    #// @param array $plugin_b
    #// @return int
    #//
    def _order_callback(self, plugin_a_=None, plugin_b_=None):
        
        
        global orderby_
        global order_
        php_check_if_defined("orderby_","order_")
        a_ = plugin_a_[orderby_]
        b_ = plugin_b_[orderby_]
        if a_ == b_:
            return 0
        # end if
        if "DESC" == order_:
            return strcasecmp(b_, a_)
        else:
            return strcasecmp(a_, b_)
        # end if
    # end def _order_callback
    #// 
    #// @global array $plugins
    #//
    def no_items(self):
        
        
        global plugins_
        php_check_if_defined("plugins_")
        if (not php_empty(lambda : PHP_REQUEST["s"])):
            s_ = esc_html(wp_unslash(PHP_REQUEST["s"]))
            #// translators: %s: Plugin search term.
            printf(__("No plugins found for &#8220;%s&#8221;."), s_)
            #// We assume that somebody who can install plugins in multisite is experienced enough to not need this helper link.
            if (not is_multisite()) and current_user_can("install_plugins"):
                php_print(" <a href=\"" + esc_url(admin_url("plugin-install.php?tab=search&s=" + urlencode(s_))) + "\">" + __("Search for plugins in the WordPress Plugin Directory.") + "</a>")
            # end if
        elif (not php_empty(lambda : plugins_["all"])):
            _e("No plugins found.")
        else:
            _e("You do not appear to have any plugins available at this time.")
        # end if
    # end def no_items
    #// 
    #// Displays the search box.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $text     The 'submit' button label.
    #// @param string $input_id ID attribute value for the search input field.
    #//
    def search_box(self, text_=None, input_id_=None):
        
        
        if php_empty(lambda : PHP_REQUEST["s"]) and (not self.has_items()):
            return
        # end if
        input_id_ = input_id_ + "-search-input"
        if (not php_empty(lambda : PHP_REQUEST["orderby"])):
            php_print("<input type=\"hidden\" name=\"orderby\" value=\"" + esc_attr(PHP_REQUEST["orderby"]) + "\" />")
        # end if
        if (not php_empty(lambda : PHP_REQUEST["order"])):
            php_print("<input type=\"hidden\" name=\"order\" value=\"" + esc_attr(PHP_REQUEST["order"]) + "\" />")
        # end if
        php_print("     <p class=\"search-box\">\n          <label class=\"screen-reader-text\" for=\"")
        php_print(esc_attr(input_id_))
        php_print("\">")
        php_print(text_)
        php_print(":</label>\n          <input type=\"search\" id=\"")
        php_print(esc_attr(input_id_))
        php_print("\" class=\"wp-filter-search\" name=\"s\" value=\"")
        _admin_search_query()
        php_print("\" placeholder=\"")
        esc_attr_e("Search installed plugins...")
        php_print("\"/>\n           ")
        submit_button(text_, "hide-if-js", "", False, Array({"id": "search-submit"}))
        php_print("     </p>\n      ")
    # end def search_box
    #// 
    #// @global string $status
    #// @return array
    #//
    def get_columns(self):
        
        
        global status_
        php_check_if_defined("status_")
        return Array({"cb": "<input type=\"checkbox\" />" if (not php_in_array(status_, Array("mustuse", "dropins"))) else "", "name": __("Plugin"), "description": __("Description")})
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        
        return Array()
    # end def get_sortable_columns
    #// 
    #// @global array $totals
    #// @global string $status
    #// @return array
    #//
    def get_views(self):
        
        
        global totals_
        global status_
        php_check_if_defined("totals_","status_")
        status_links_ = Array()
        for type_,count_ in totals_:
            if (not count_):
                continue
            # end if
            for case in Switch(type_):
                if case("all"):
                    #// translators: %s: Number of plugins.
                    text_ = _nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", count_, "plugins")
                    break
                # end if
                if case("active"):
                    #// translators: %s: Number of plugins.
                    text_ = _n("Active <span class=\"count\">(%s)</span>", "Active <span class=\"count\">(%s)</span>", count_)
                    break
                # end if
                if case("recently_activated"):
                    #// translators: %s: Number of plugins.
                    text_ = _n("Recently Active <span class=\"count\">(%s)</span>", "Recently Active <span class=\"count\">(%s)</span>", count_)
                    break
                # end if
                if case("inactive"):
                    #// translators: %s: Number of plugins.
                    text_ = _n("Inactive <span class=\"count\">(%s)</span>", "Inactive <span class=\"count\">(%s)</span>", count_)
                    break
                # end if
                if case("mustuse"):
                    #// translators: %s: Number of plugins.
                    text_ = _n("Must-Use <span class=\"count\">(%s)</span>", "Must-Use <span class=\"count\">(%s)</span>", count_)
                    break
                # end if
                if case("dropins"):
                    #// translators: %s: Number of plugins.
                    text_ = _n("Drop-in <span class=\"count\">(%s)</span>", "Drop-ins <span class=\"count\">(%s)</span>", count_)
                    break
                # end if
                if case("paused"):
                    #// translators: %s: Number of plugins.
                    text_ = _n("Paused <span class=\"count\">(%s)</span>", "Paused <span class=\"count\">(%s)</span>", count_)
                    break
                # end if
                if case("upgrade"):
                    #// translators: %s: Number of plugins.
                    text_ = _n("Update Available <span class=\"count\">(%s)</span>", "Update Available <span class=\"count\">(%s)</span>", count_)
                    break
                # end if
            # end for
            if "search" != type_:
                status_links_[type_] = php_sprintf("<a href='%s'%s>%s</a>", add_query_arg("plugin_status", type_, "plugins.php"), " class=\"current\" aria-current=\"page\"" if type_ == status_ else "", php_sprintf(text_, number_format_i18n(count_)))
            # end if
        # end for
        return status_links_
    # end def get_views
    #// 
    #// @global string $status
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        global status_
        php_check_if_defined("status_")
        actions_ = Array()
        if "active" != status_:
            actions_["activate-selected"] = __("Network Activate") if self.screen.in_admin("network") else __("Activate")
        # end if
        if "inactive" != status_ and "recent" != status_:
            actions_["deactivate-selected"] = __("Network Deactivate") if self.screen.in_admin("network") else __("Deactivate")
        # end if
        if (not is_multisite()) or self.screen.in_admin("network"):
            if current_user_can("update_plugins"):
                actions_["update-selected"] = __("Update")
            # end if
            if current_user_can("delete_plugins") and "active" != status_:
                actions_["delete-selected"] = __("Delete")
            # end if
        # end if
        return actions_
    # end def get_bulk_actions
    #// 
    #// @global string $status
    #// @param string $which
    #//
    def bulk_actions(self, which_=""):
        
        
        global status_
        php_check_if_defined("status_")
        if php_in_array(status_, Array("mustuse", "dropins")):
            return
        # end if
        super().bulk_actions(which_)
    # end def bulk_actions
    #// 
    #// @global string $status
    #// @param string $which
    #//
    def extra_tablenav(self, which_=None):
        
        
        global status_
        php_check_if_defined("status_")
        if (not php_in_array(status_, Array("recently_activated", "mustuse", "dropins"))):
            return
        # end if
        php_print("<div class=\"alignleft actions\">")
        if "recently_activated" == status_:
            submit_button(__("Clear List"), "", "clear-recent-list", False)
        elif "top" == which_ and "mustuse" == status_:
            php_print("<p>" + php_sprintf(__("Files in the %s directory are executed automatically."), "<code>" + php_str_replace(ABSPATH, "/", WPMU_PLUGIN_DIR) + "</code>") + "</p>")
        elif "top" == which_ and "dropins" == status_:
            php_print("<p>" + php_sprintf(__("Drop-ins are single files, found in the %s directory, that replace or enhance WordPress features in ways that are not possible for traditional plugins."), "<code>" + php_str_replace(ABSPATH, "", WP_CONTENT_DIR) + "</code>") + "</p>")
        # end if
        php_print("</div>")
    # end def extra_tablenav
    #// 
    #// @return string
    #//
    def current_action(self):
        
        
        if (php_isset(lambda : PHP_POST["clear-recent-list"])):
            return "clear-recent-list"
        # end if
        return super().current_action()
    # end def current_action
    #// 
    #// @global string $status
    #//
    def display_rows(self):
        
        
        global status_
        php_check_if_defined("status_")
        if is_multisite() and (not self.screen.in_admin("network")) and php_in_array(status_, Array("mustuse", "dropins")):
            return
        # end if
        for plugin_file_,plugin_data_ in self.items:
            self.single_row(Array(plugin_file_, plugin_data_))
        # end for
    # end def display_rows
    #// 
    #// @global string $status
    #// @global int $page
    #// @global string $s
    #// @global array $totals
    #// 
    #// @param array $item
    #//
    def single_row(self, item_=None):
        
        
        global status_
        global page_
        global s_
        global totals_
        php_check_if_defined("status_","page_","s_","totals_")
        plugin_file_, plugin_data_ = item_
        context_ = status_
        screen_ = self.screen
        #// Pre-order.
        actions_ = Array({"deactivate": "", "activate": "", "details": "", "delete": ""})
        #// Do not restrict by default.
        restrict_network_active_ = False
        restrict_network_only_ = False
        if "mustuse" == context_:
            is_active_ = True
        elif "dropins" == context_:
            dropins_ = _get_dropins()
            plugin_name_ = plugin_file_
            if plugin_file_ != plugin_data_["Name"]:
                plugin_name_ += "<br/>" + plugin_data_["Name"]
            # end if
            if True == dropins_[plugin_file_][1]:
                #// Doesn't require a constant.
                is_active_ = True
                description_ = "<p><strong>" + dropins_[plugin_file_][0] + "</strong></p>"
            elif php_defined(dropins_[plugin_file_][1]) and constant(dropins_[plugin_file_][1]):
                #// Constant is true.
                is_active_ = True
                description_ = "<p><strong>" + dropins_[plugin_file_][0] + "</strong></p>"
            else:
                is_active_ = False
                description_ = "<p><strong>" + dropins_[plugin_file_][0] + " <span class=\"error-message\">" + __("Inactive:") + "</span></strong> " + php_sprintf(__("Requires %1$s in %2$s file."), "<code>define('" + dropins_[plugin_file_][1] + "', true);</code>", "<code>wp-config.php</code>") + "</p>"
            # end if
            if plugin_data_["Description"]:
                description_ += "<p>" + plugin_data_["Description"] + "</p>"
            # end if
        else:
            if screen_.in_admin("network"):
                is_active_ = is_plugin_active_for_network(plugin_file_)
            else:
                is_active_ = is_plugin_active(plugin_file_)
                restrict_network_active_ = is_multisite() and is_plugin_active_for_network(plugin_file_)
                restrict_network_only_ = is_multisite() and is_network_only_plugin(plugin_file_) and (not is_active_)
            # end if
            if screen_.in_admin("network"):
                if is_active_:
                    if current_user_can("manage_network_plugins"):
                        actions_["deactivate"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=deactivate&amp;plugin=" + urlencode(plugin_file_) + "&amp;plugin_status=" + context_ + "&amp;paged=" + page_ + "&amp;s=" + s_, "deactivate-plugin_" + plugin_file_), esc_attr(php_sprintf(_x("Network Deactivate %s", "plugin"), plugin_data_["Name"])), __("Network Deactivate"))
                    # end if
                else:
                    if current_user_can("manage_network_plugins"):
                        actions_["activate"] = php_sprintf("<a href=\"%s\" class=\"edit\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;plugin=" + urlencode(plugin_file_) + "&amp;plugin_status=" + context_ + "&amp;paged=" + page_ + "&amp;s=" + s_, "activate-plugin_" + plugin_file_), esc_attr(php_sprintf(_x("Network Activate %s", "plugin"), plugin_data_["Name"])), __("Network Activate"))
                    # end if
                    if current_user_can("delete_plugins") and (not is_plugin_active(plugin_file_)):
                        actions_["delete"] = php_sprintf("<a href=\"%s\" class=\"delete\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=delete-selected&amp;checked[]=" + urlencode(plugin_file_) + "&amp;plugin_status=" + context_ + "&amp;paged=" + page_ + "&amp;s=" + s_, "bulk-plugins"), esc_attr(php_sprintf(_x("Delete %s", "plugin"), plugin_data_["Name"])), __("Delete"))
                    # end if
                # end if
            else:
                if restrict_network_active_:
                    actions_ = Array({"network_active": __("Network Active")})
                elif restrict_network_only_:
                    actions_ = Array({"network_only": __("Network Only")})
                elif is_active_:
                    if current_user_can("deactivate_plugin", plugin_file_):
                        actions_["deactivate"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=deactivate&amp;plugin=" + urlencode(plugin_file_) + "&amp;plugin_status=" + context_ + "&amp;paged=" + page_ + "&amp;s=" + s_, "deactivate-plugin_" + plugin_file_), esc_attr(php_sprintf(_x("Deactivate %s", "plugin"), plugin_data_["Name"])), __("Deactivate"))
                    # end if
                    if current_user_can("resume_plugin", plugin_file_) and is_plugin_paused(plugin_file_):
                        actions_["resume"] = php_sprintf("<a class=\"resume-link\" href=\"%s\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=resume&amp;plugin=" + urlencode(plugin_file_) + "&amp;plugin_status=" + context_ + "&amp;paged=" + page_ + "&amp;s=" + s_, "resume-plugin_" + plugin_file_), esc_attr(php_sprintf(_x("Resume %s", "plugin"), plugin_data_["Name"])), __("Resume"))
                    # end if
                else:
                    if current_user_can("activate_plugin", plugin_file_):
                        actions_["activate"] = php_sprintf("<a href=\"%s\" class=\"edit\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;plugin=" + urlencode(plugin_file_) + "&amp;plugin_status=" + context_ + "&amp;paged=" + page_ + "&amp;s=" + s_, "activate-plugin_" + plugin_file_), esc_attr(php_sprintf(_x("Activate %s", "plugin"), plugin_data_["Name"])), __("Activate"))
                    # end if
                    if (not is_multisite()) and current_user_can("delete_plugins"):
                        actions_["delete"] = php_sprintf("<a href=\"%s\" class=\"delete\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=delete-selected&amp;checked[]=" + urlencode(plugin_file_) + "&amp;plugin_status=" + context_ + "&amp;paged=" + page_ + "&amp;s=" + s_, "bulk-plugins"), esc_attr(php_sprintf(_x("Delete %s", "plugin"), plugin_data_["Name"])), __("Delete"))
                    # end if
                # end if
                pass
            # end if
            pass
        # end if
        #// End if $context.
        actions_ = php_array_filter(actions_)
        if screen_.in_admin("network"):
            #// 
            #// Filters the action links displayed for each plugin in the Network Admin Plugins list table.
            #// 
            #// @since 3.1.0
            #// 
            #// @param string[] $actions     An array of plugin action links. By default this can include 'activate',
            #// 'deactivate', and 'delete'.
            #// @param string   $plugin_file Path to the plugin file relative to the plugins directory.
            #// @param array    $plugin_data An array of plugin data. See `get_plugin_data()`.
            #// @param string   $context     The plugin context. By default this can include 'all', 'active', 'inactive',
            #// 'recently_activated', 'upgrade', 'mustuse', 'dropins', and 'search'.
            #//
            actions_ = apply_filters("network_admin_plugin_action_links", actions_, plugin_file_, plugin_data_, context_)
            #// 
            #// Filters the list of action links displayed for a specific plugin in the Network Admin Plugins list table.
            #// 
            #// The dynamic portion of the hook name, `$plugin_file`, refers to the path
            #// to the plugin file, relative to the plugins directory.
            #// 
            #// @since 3.1.0
            #// 
            #// @param string[] $actions     An array of plugin action links. By default this can include 'activate',
            #// 'deactivate', and 'delete'.
            #// @param string   $plugin_file Path to the plugin file relative to the plugins directory.
            #// @param array    $plugin_data An array of plugin data. See `get_plugin_data()`.
            #// @param string   $context     The plugin context. By default this can include 'all', 'active', 'inactive',
            #// 'recently_activated', 'upgrade', 'mustuse', 'dropins', and 'search'.
            #//
            actions_ = apply_filters(str("network_admin_plugin_action_links_") + str(plugin_file_), actions_, plugin_file_, plugin_data_, context_)
        else:
            #// 
            #// Filters the action links displayed for each plugin in the Plugins list table.
            #// 
            #// @since 2.5.0
            #// @since 2.6.0 The `$context` parameter was added.
            #// @since 4.9.0 The 'Edit' link was removed from the list of action links.
            #// 
            #// @param string[] $actions     An array of plugin action links. By default this can include 'activate',
            #// 'deactivate', and 'delete'. With Multisite active this can also include
            #// 'network_active' and 'network_only' items.
            #// @param string   $plugin_file Path to the plugin file relative to the plugins directory.
            #// @param array    $plugin_data An array of plugin data. See `get_plugin_data()`.
            #// @param string   $context     The plugin context. By default this can include 'all', 'active', 'inactive',
            #// 'recently_activated', 'upgrade', 'mustuse', 'dropins', and 'search'.
            #//
            actions_ = apply_filters("plugin_action_links", actions_, plugin_file_, plugin_data_, context_)
            #// 
            #// Filters the list of action links displayed for a specific plugin in the Plugins list table.
            #// 
            #// The dynamic portion of the hook name, `$plugin_file`, refers to the path
            #// to the plugin file, relative to the plugins directory.
            #// 
            #// @since 2.7.0
            #// @since 4.9.0 The 'Edit' link was removed from the list of action links.
            #// 
            #// @param string[] $actions     An array of plugin action links. By default this can include 'activate',
            #// 'deactivate', and 'delete'. With Multisite active this can also include
            #// 'network_active' and 'network_only' items.
            #// @param string   $plugin_file Path to the plugin file relative to the plugins directory.
            #// @param array    $plugin_data An array of plugin data. See `get_plugin_data()`.
            #// @param string   $context     The plugin context. By default this can include 'all', 'active', 'inactive',
            #// 'recently_activated', 'upgrade', 'mustuse', 'dropins', and 'search'.
            #//
            actions_ = apply_filters(str("plugin_action_links_") + str(plugin_file_), actions_, plugin_file_, plugin_data_, context_)
        # end if
        requires_php_ = plugin_data_["requires_php"] if (php_isset(lambda : plugin_data_["requires_php"])) else None
        compatible_php_ = is_php_version_compatible(requires_php_)
        class_ = "active" if is_active_ else "inactive"
        checkbox_id_ = "checkbox_" + php_md5(plugin_data_["Name"])
        if restrict_network_active_ or restrict_network_only_ or php_in_array(status_, Array("mustuse", "dropins")) or (not compatible_php_):
            checkbox_ = ""
        else:
            checkbox_ = php_sprintf("<label class=\"screen-reader-text\" for=\"%1$s\">%2$s</label>" + "<input type=\"checkbox\" name=\"checked[]\" value=\"%3$s\" id=\"%1$s\" />", checkbox_id_, php_sprintf(__("Select %s"), plugin_data_["Name"]), esc_attr(plugin_file_))
        # end if
        if "dropins" != context_:
            description_ = "<p>" + plugin_data_["Description"] if plugin_data_["Description"] else "&nbsp;" + "</p>"
            plugin_name_ = plugin_data_["Name"]
        # end if
        if (not php_empty(lambda : totals_["upgrade"])) and (not php_empty(lambda : plugin_data_["update"])):
            class_ += " update"
        # end if
        paused_ = (not screen_.in_admin("network")) and is_plugin_paused(plugin_file_)
        if paused_:
            class_ += " paused"
        # end if
        plugin_slug_ = plugin_data_["slug"] if (php_isset(lambda : plugin_data_["slug"])) else sanitize_title(plugin_name_)
        printf("<tr class=\"%s\" data-slug=\"%s\" data-plugin=\"%s\">", esc_attr(class_), esc_attr(plugin_slug_), esc_attr(plugin_file_))
        columns_, hidden_, sortable_, primary_ = self.get_column_info()
        for column_name_,column_display_name_ in columns_:
            extra_classes_ = ""
            if php_in_array(column_name_, hidden_):
                extra_classes_ = " hidden"
            # end if
            for case in Switch(column_name_):
                if case("cb"):
                    php_print(str("<th scope='row' class='check-column'>") + str(checkbox_) + str("</th>"))
                    break
                # end if
                if case("name"):
                    php_print(str("<td class='plugin-title column-primary'><strong>") + str(plugin_name_) + str("</strong>"))
                    php_print(self.row_actions(actions_, True))
                    php_print("</td>")
                    break
                # end if
                if case("description"):
                    classes_ = "column-description desc"
                    php_print(str("<td class='") + str(classes_) + str(extra_classes_) + str("'>\n                      <div class='plugin-description'>") + str(description_) + str("</div>\n                      <div class='") + str(class_) + str(" second plugin-version-author-uri'>"))
                    plugin_meta_ = Array()
                    if (not php_empty(lambda : plugin_data_["Version"])):
                        #// translators: %s: Plugin version number.
                        plugin_meta_[-1] = php_sprintf(__("Version %s"), plugin_data_["Version"])
                    # end if
                    if (not php_empty(lambda : plugin_data_["Author"])):
                        author_ = plugin_data_["Author"]
                        if (not php_empty(lambda : plugin_data_["AuthorURI"])):
                            author_ = "<a href=\"" + plugin_data_["AuthorURI"] + "\">" + plugin_data_["Author"] + "</a>"
                        # end if
                        #// translators: %s: Plugin author name.
                        plugin_meta_[-1] = php_sprintf(__("By %s"), author_)
                    # end if
                    #// Details link using API info, if available.
                    if (php_isset(lambda : plugin_data_["slug"])) and current_user_can("install_plugins"):
                        plugin_meta_[-1] = php_sprintf("<a href=\"%s\" class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\" data-title=\"%s\">%s</a>", esc_url(network_admin_url("plugin-install.php?tab=plugin-information&plugin=" + plugin_data_["slug"] + "&TB_iframe=true&width=600&height=550")), esc_attr(php_sprintf(__("More information about %s"), plugin_name_)), esc_attr(plugin_name_), __("View details"))
                    elif (not php_empty(lambda : plugin_data_["PluginURI"])):
                        plugin_meta_[-1] = php_sprintf("<a href=\"%s\">%s</a>", esc_url(plugin_data_["PluginURI"]), __("Visit plugin site"))
                    # end if
                    #// 
                    #// Filters the array of row meta for each plugin in the Plugins list table.
                    #// 
                    #// @since 2.8.0
                    #// 
                    #// @param string[] $plugin_meta An array of the plugin's metadata,
                    #// including the version, author,
                    #// author URI, and plugin URI.
                    #// @param string   $plugin_file Path to the plugin file relative to the plugins directory.
                    #// @param array    $plugin_data An array of plugin data.
                    #// @param string   $status      Status of the plugin. Defaults are 'All', 'Active',
                    #// 'Inactive', 'Recently Activated', 'Upgrade', 'Must-Use',
                    #// 'Drop-ins', 'Search', 'Paused'.
                    #//
                    plugin_meta_ = apply_filters("plugin_row_meta", plugin_meta_, plugin_file_, plugin_data_, status_)
                    php_print(php_implode(" | ", plugin_meta_))
                    php_print("</div>")
                    if paused_:
                        notice_text_ = __("This plugin failed to load properly and is paused during recovery mode.")
                        printf("<p><span class=\"dashicons dashicons-warning\"></span> <strong>%s</strong></p>", notice_text_)
                        error_ = wp_get_plugin_error(plugin_file_)
                        if False != error_:
                            printf("<div class=\"error-display\"><p>%s</p></div>", wp_get_extension_error_description(error_))
                        # end if
                    # end if
                    php_print("</td>")
                    break
                # end if
                if case():
                    classes_ = str(column_name_) + str(" column-") + str(column_name_) + str(" ") + str(class_)
                    php_print(str("<td class='") + str(classes_) + str(extra_classes_) + str("'>"))
                    #// 
                    #// Fires inside each custom column of the Plugins list table.
                    #// 
                    #// @since 3.1.0
                    #// 
                    #// @param string $column_name Name of the column.
                    #// @param string $plugin_file Path to the plugin file relative to the plugins directory.
                    #// @param array  $plugin_data An array of plugin data.
                    #//
                    do_action("manage_plugins_custom_column", column_name_, plugin_file_, plugin_data_)
                    php_print("</td>")
                # end if
            # end for
        # end for
        php_print("</tr>")
        #// 
        #// Fires after each row in the Plugins list table.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $plugin_file Path to the plugin file relative to the plugins directory.
        #// @param array  $plugin_data An array of plugin data.
        #// @param string $status      Status of the plugin. Defaults are 'All', 'Active',
        #// 'Inactive', 'Recently Activated', 'Upgrade', 'Must-Use',
        #// 'Drop-ins', 'Search', 'Paused'.
        #//
        do_action("after_plugin_row", plugin_file_, plugin_data_, status_)
        #// 
        #// Fires after each specific row in the Plugins list table.
        #// 
        #// The dynamic portion of the hook name, `$plugin_file`, refers to the path
        #// to the plugin file, relative to the plugins directory.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string $plugin_file Path to the plugin file relative to the plugins directory.
        #// @param array  $plugin_data An array of plugin data.
        #// @param string $status      Status of the plugin. Defaults are 'All', 'Active',
        #// 'Inactive', 'Recently Activated', 'Upgrade', 'Must-Use',
        #// 'Drop-ins', 'Search', 'Paused'.
        #//
        do_action(str("after_plugin_row_") + str(plugin_file_), plugin_file_, plugin_data_, status_)
    # end def single_row
    #// 
    #// Gets the name of the primary column for this specific list table.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Unalterable name for the primary column, in this case, 'name'.
    #//
    def get_primary_column_name(self):
        
        
        return "name"
    # end def get_primary_column_name
# end class WP_Plugins_List_Table
