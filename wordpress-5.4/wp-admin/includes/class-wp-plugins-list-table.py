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
    def __init__(self, args=Array()):
        global PHP_SERVER
        global status,page
        php_check_if_defined("status","page")
        super().__init__(Array({"plural": "plugins", "screen": args["screen"] if (php_isset(lambda : args["screen"])) else None}))
        status = "all"
        if (php_isset(lambda : PHP_REQUEST["plugin_status"])) and php_in_array(PHP_REQUEST["plugin_status"], Array("active", "inactive", "recently_activated", "upgrade", "mustuse", "dropins", "search", "paused")):
            status = PHP_REQUEST["plugin_status"]
        # end if
        if (php_isset(lambda : PHP_REQUEST["s"])):
            PHP_SERVER["REQUEST_URI"] = add_query_arg("s", wp_unslash(PHP_REQUEST["s"]))
        # end if
        page = self.get_pagenum()
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
        
        global status,plugins,totals,page,orderby,order,s
        php_check_if_defined("status","plugins","totals","page","orderby","order","s")
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
        all_plugins = apply_filters("all_plugins", get_plugins())
        plugins = Array({"all": all_plugins, "search": Array(), "active": Array(), "inactive": Array(), "recently_activated": Array(), "upgrade": Array(), "mustuse": Array(), "dropins": Array(), "paused": Array()})
        screen = self.screen
        if (not is_multisite()) or screen.in_admin("network") and current_user_can("manage_network_plugins"):
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
                plugins["mustuse"] = get_mu_plugins()
            # end if
            #// This action is documented in wp-admin/includes/class-wp-plugins-list-table.php
            if apply_filters("show_advanced_plugins", True, "dropins"):
                plugins["dropins"] = get_dropins()
            # end if
            if current_user_can("update_plugins"):
                current = get_site_transient("update_plugins")
                for plugin_file,plugin_data in plugins["all"]:
                    if (php_isset(lambda : current.response[plugin_file])):
                        plugins["all"][plugin_file]["update"] = True
                        plugins["upgrade"][plugin_file] = plugins["all"][plugin_file]
                    # end if
                # end for
            # end if
        # end if
        if (not screen.in_admin("network")):
            show = current_user_can("manage_network_plugins")
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
            show_network_active = apply_filters("show_network_active_plugins", show)
        # end if
        if screen.in_admin("network"):
            recently_activated = get_site_option("recently_activated", Array())
        else:
            recently_activated = get_option("recently_activated", Array())
        # end if
        for key,time in recently_activated:
            if time + WEEK_IN_SECONDS < time():
                recently_activated[key] = None
            # end if
        # end for
        if screen.in_admin("network"):
            update_site_option("recently_activated", recently_activated)
        else:
            update_option("recently_activated", recently_activated)
        # end if
        plugin_info = get_site_transient("update_plugins")
        for plugin_file,plugin_data in plugins["all"]:
            #// Extra info if known. array_merge() ensures $plugin_data has precedence if keys collide.
            if (php_isset(lambda : plugin_info.response[plugin_file])):
                plugin_data = php_array_merge(plugin_info.response[plugin_file], plugin_data)
                plugins["all"][plugin_file] = plugin_data
                #// Make sure that $plugins['upgrade'] also receives the extra info since it is used on ?plugin_status=upgrade.
                if (php_isset(lambda : plugins["upgrade"][plugin_file])):
                    plugins["upgrade"][plugin_file] = plugin_data
                # end if
            elif (php_isset(lambda : plugin_info.no_update[plugin_file])):
                plugin_data = php_array_merge(plugin_info.no_update[plugin_file], plugin_data)
                plugins["all"][plugin_file] = plugin_data
                #// Make sure that $plugins['upgrade'] also receives the extra info since it is used on ?plugin_status=upgrade.
                if (php_isset(lambda : plugins["upgrade"][plugin_file])):
                    plugins["upgrade"][plugin_file] = plugin_data
                # end if
            # end if
            #// Filter into individual sections.
            if is_multisite() and (not screen.in_admin("network")) and is_network_only_plugin(plugin_file) and (not is_plugin_active(plugin_file)):
                if show_network_active:
                    #// On the non-network screen, show inactive network-only plugins if allowed.
                    plugins["inactive"][plugin_file] = plugin_data
                else:
                    plugins["all"][plugin_file] = None
                # end if
            elif (not screen.in_admin("network")) and is_plugin_active_for_network(plugin_file):
                if show_network_active:
                    #// On the non-network screen, show network-active plugins if allowed.
                    plugins["active"][plugin_file] = plugin_data
                else:
                    plugins["all"][plugin_file] = None
                # end if
            elif (not screen.in_admin("network")) and is_plugin_active(plugin_file) or screen.in_admin("network") and is_plugin_active_for_network(plugin_file):
                #// On the non-network screen, populate the active list with plugins that are individually activated.
                #// On the network admin screen, populate the active list with plugins that are network-activated.
                plugins["active"][plugin_file] = plugin_data
                if (not screen.in_admin("network")) and is_plugin_paused(plugin_file):
                    plugins["paused"][plugin_file] = plugin_data
                # end if
            else:
                if (php_isset(lambda : recently_activated[plugin_file])):
                    #// Populate the recently activated list with plugins that have been recently activated.
                    plugins["recently_activated"][plugin_file] = plugin_data
                # end if
                #// Populate the inactive list with plugins that aren't activated.
                plugins["inactive"][plugin_file] = plugin_data
            # end if
        # end for
        if php_strlen(s):
            status = "search"
            plugins["search"] = php_array_filter(plugins["all"], Array(self, "_search_callback"))
        # end if
        totals = Array()
        for type,list in plugins:
            totals[type] = php_count(list)
        # end for
        if php_empty(lambda : plugins[status]) and (not php_in_array(status, Array("all", "search"))):
            status = "all"
        # end if
        self.items = Array()
        for plugin_file,plugin_data in plugins[status]:
            #// Translate, don't apply markup, sanitize HTML.
            self.items[plugin_file] = _get_plugin_data_markup_translate(plugin_file, plugin_data, False, True)
        # end for
        total_this_page = totals[status]
        js_plugins = Array()
        for key,list in plugins:
            js_plugins[key] = php_array_keys(list)
        # end for
        wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"plugins": js_plugins, "totals": wp_get_update_data()}))
        if (not orderby):
            orderby = "Name"
        else:
            orderby = ucfirst(orderby)
        # end if
        order = php_strtoupper(order)
        uasort(self.items, Array(self, "_order_callback"))
        plugins_per_page = self.get_items_per_page(php_str_replace("-", "_", screen.id + "_per_page"), 999)
        start = page - 1 * plugins_per_page
        if total_this_page > plugins_per_page:
            self.items = php_array_slice(self.items, start, plugins_per_page)
        # end if
        self.set_pagination_args(Array({"total_items": total_this_page, "per_page": plugins_per_page}))
    # end def prepare_items
    #// 
    #// @global string $s URL encoded search term.
    #// 
    #// @param array $plugin
    #// @return bool
    #//
    def _search_callback(self, plugin=None):
        
        global s
        php_check_if_defined("s")
        for value in plugin:
            if php_is_string(value) and False != php_stripos(strip_tags(value), urldecode(s)):
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
    def _order_callback(self, plugin_a=None, plugin_b=None):
        
        global orderby,order
        php_check_if_defined("orderby","order")
        a = plugin_a[orderby]
        b = plugin_b[orderby]
        if a == b:
            return 0
        # end if
        if "DESC" == order:
            return strcasecmp(b, a)
        else:
            return strcasecmp(a, b)
        # end if
    # end def _order_callback
    #// 
    #// @global array $plugins
    #//
    def no_items(self):
        
        global plugins
        php_check_if_defined("plugins")
        if (not php_empty(lambda : PHP_REQUEST["s"])):
            s = esc_html(wp_unslash(PHP_REQUEST["s"]))
            #// translators: %s: Plugin search term.
            printf(__("No plugins found for &#8220;%s&#8221;."), s)
            #// We assume that somebody who can install plugins in multisite is experienced enough to not need this helper link.
            if (not is_multisite()) and current_user_can("install_plugins"):
                php_print(" <a href=\"" + esc_url(admin_url("plugin-install.php?tab=search&s=" + urlencode(s))) + "\">" + __("Search for plugins in the WordPress Plugin Directory.") + "</a>")
            # end if
        elif (not php_empty(lambda : plugins["all"])):
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
    def search_box(self, text=None, input_id=None):
        
        if php_empty(lambda : PHP_REQUEST["s"]) and (not self.has_items()):
            return
        # end if
        input_id = input_id + "-search-input"
        if (not php_empty(lambda : PHP_REQUEST["orderby"])):
            php_print("<input type=\"hidden\" name=\"orderby\" value=\"" + esc_attr(PHP_REQUEST["orderby"]) + "\" />")
        # end if
        if (not php_empty(lambda : PHP_REQUEST["order"])):
            php_print("<input type=\"hidden\" name=\"order\" value=\"" + esc_attr(PHP_REQUEST["order"]) + "\" />")
        # end if
        php_print("     <p class=\"search-box\">\n          <label class=\"screen-reader-text\" for=\"")
        php_print(esc_attr(input_id))
        php_print("\">")
        php_print(text)
        php_print(":</label>\n          <input type=\"search\" id=\"")
        php_print(esc_attr(input_id))
        php_print("\" class=\"wp-filter-search\" name=\"s\" value=\"")
        _admin_search_query()
        php_print("\" placeholder=\"")
        esc_attr_e("Search installed plugins...")
        php_print("\"/>\n           ")
        submit_button(text, "hide-if-js", "", False, Array({"id": "search-submit"}))
        php_print("     </p>\n      ")
    # end def search_box
    #// 
    #// @global string $status
    #// @return array
    #//
    def get_columns(self):
        
        global status
        php_check_if_defined("status")
        return Array({"cb": "<input type=\"checkbox\" />" if (not php_in_array(status, Array("mustuse", "dropins"))) else "", "name": __("Plugin"), "description": __("Description")})
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
        
        global totals,status
        php_check_if_defined("totals","status")
        status_links = Array()
        for type,count in totals:
            if (not count):
                continue
            # end if
            for case in Switch(type):
                if case("all"):
                    #// translators: %s: Number of plugins.
                    text = _nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", count, "plugins")
                    break
                # end if
                if case("active"):
                    #// translators: %s: Number of plugins.
                    text = _n("Active <span class=\"count\">(%s)</span>", "Active <span class=\"count\">(%s)</span>", count)
                    break
                # end if
                if case("recently_activated"):
                    #// translators: %s: Number of plugins.
                    text = _n("Recently Active <span class=\"count\">(%s)</span>", "Recently Active <span class=\"count\">(%s)</span>", count)
                    break
                # end if
                if case("inactive"):
                    #// translators: %s: Number of plugins.
                    text = _n("Inactive <span class=\"count\">(%s)</span>", "Inactive <span class=\"count\">(%s)</span>", count)
                    break
                # end if
                if case("mustuse"):
                    #// translators: %s: Number of plugins.
                    text = _n("Must-Use <span class=\"count\">(%s)</span>", "Must-Use <span class=\"count\">(%s)</span>", count)
                    break
                # end if
                if case("dropins"):
                    #// translators: %s: Number of plugins.
                    text = _n("Drop-in <span class=\"count\">(%s)</span>", "Drop-ins <span class=\"count\">(%s)</span>", count)
                    break
                # end if
                if case("paused"):
                    #// translators: %s: Number of plugins.
                    text = _n("Paused <span class=\"count\">(%s)</span>", "Paused <span class=\"count\">(%s)</span>", count)
                    break
                # end if
                if case("upgrade"):
                    #// translators: %s: Number of plugins.
                    text = _n("Update Available <span class=\"count\">(%s)</span>", "Update Available <span class=\"count\">(%s)</span>", count)
                    break
                # end if
            # end for
            if "search" != type:
                status_links[type] = php_sprintf("<a href='%s'%s>%s</a>", add_query_arg("plugin_status", type, "plugins.php"), " class=\"current\" aria-current=\"page\"" if type == status else "", php_sprintf(text, number_format_i18n(count)))
            # end if
        # end for
        return status_links
    # end def get_views
    #// 
    #// @global string $status
    #// @return array
    #//
    def get_bulk_actions(self):
        
        global status
        php_check_if_defined("status")
        actions = Array()
        if "active" != status:
            actions["activate-selected"] = __("Network Activate") if self.screen.in_admin("network") else __("Activate")
        # end if
        if "inactive" != status and "recent" != status:
            actions["deactivate-selected"] = __("Network Deactivate") if self.screen.in_admin("network") else __("Deactivate")
        # end if
        if (not is_multisite()) or self.screen.in_admin("network"):
            if current_user_can("update_plugins"):
                actions["update-selected"] = __("Update")
            # end if
            if current_user_can("delete_plugins") and "active" != status:
                actions["delete-selected"] = __("Delete")
            # end if
        # end if
        return actions
    # end def get_bulk_actions
    #// 
    #// @global string $status
    #// @param string $which
    #//
    def bulk_actions(self, which=""):
        
        global status
        php_check_if_defined("status")
        if php_in_array(status, Array("mustuse", "dropins")):
            return
        # end if
        super().bulk_actions(which)
    # end def bulk_actions
    #// 
    #// @global string $status
    #// @param string $which
    #//
    def extra_tablenav(self, which=None):
        
        global status
        php_check_if_defined("status")
        if (not php_in_array(status, Array("recently_activated", "mustuse", "dropins"))):
            return
        # end if
        php_print("<div class=\"alignleft actions\">")
        if "recently_activated" == status:
            submit_button(__("Clear List"), "", "clear-recent-list", False)
        elif "top" == which and "mustuse" == status:
            php_print("<p>" + php_sprintf(__("Files in the %s directory are executed automatically."), "<code>" + php_str_replace(ABSPATH, "/", WPMU_PLUGIN_DIR) + "</code>") + "</p>")
        elif "top" == which and "dropins" == status:
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
        
        global status
        php_check_if_defined("status")
        if is_multisite() and (not self.screen.in_admin("network")) and php_in_array(status, Array("mustuse", "dropins")):
            return
        # end if
        for plugin_file,plugin_data in self.items:
            self.single_row(Array(plugin_file, plugin_data))
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
    def single_row(self, item=None):
        
        global status,page,s,totals
        php_check_if_defined("status","page","s","totals")
        plugin_file, plugin_data = item
        context = status
        screen = self.screen
        #// Pre-order.
        actions = Array({"deactivate": "", "activate": "", "details": "", "delete": ""})
        #// Do not restrict by default.
        restrict_network_active = False
        restrict_network_only = False
        if "mustuse" == context:
            is_active = True
        elif "dropins" == context:
            dropins = _get_dropins()
            plugin_name = plugin_file
            if plugin_file != plugin_data["Name"]:
                plugin_name += "<br/>" + plugin_data["Name"]
            # end if
            if True == dropins[plugin_file][1]:
                #// Doesn't require a constant.
                is_active = True
                description = "<p><strong>" + dropins[plugin_file][0] + "</strong></p>"
            elif php_defined(dropins[plugin_file][1]) and constant(dropins[plugin_file][1]):
                #// Constant is true.
                is_active = True
                description = "<p><strong>" + dropins[plugin_file][0] + "</strong></p>"
            else:
                is_active = False
                description = "<p><strong>" + dropins[plugin_file][0] + " <span class=\"error-message\">" + __("Inactive:") + "</span></strong> " + php_sprintf(__("Requires %1$s in %2$s file."), "<code>define('" + dropins[plugin_file][1] + "', true);</code>", "<code>wp-config.php</code>") + "</p>"
            # end if
            if plugin_data["Description"]:
                description += "<p>" + plugin_data["Description"] + "</p>"
            # end if
        else:
            if screen.in_admin("network"):
                is_active = is_plugin_active_for_network(plugin_file)
            else:
                is_active = is_plugin_active(plugin_file)
                restrict_network_active = is_multisite() and is_plugin_active_for_network(plugin_file)
                restrict_network_only = is_multisite() and is_network_only_plugin(plugin_file) and (not is_active)
            # end if
            if screen.in_admin("network"):
                if is_active:
                    if current_user_can("manage_network_plugins"):
                        actions["deactivate"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=deactivate&amp;plugin=" + urlencode(plugin_file) + "&amp;plugin_status=" + context + "&amp;paged=" + page + "&amp;s=" + s, "deactivate-plugin_" + plugin_file), esc_attr(php_sprintf(_x("Network Deactivate %s", "plugin"), plugin_data["Name"])), __("Network Deactivate"))
                    # end if
                else:
                    if current_user_can("manage_network_plugins"):
                        actions["activate"] = php_sprintf("<a href=\"%s\" class=\"edit\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;plugin=" + urlencode(plugin_file) + "&amp;plugin_status=" + context + "&amp;paged=" + page + "&amp;s=" + s, "activate-plugin_" + plugin_file), esc_attr(php_sprintf(_x("Network Activate %s", "plugin"), plugin_data["Name"])), __("Network Activate"))
                    # end if
                    if current_user_can("delete_plugins") and (not is_plugin_active(plugin_file)):
                        actions["delete"] = php_sprintf("<a href=\"%s\" class=\"delete\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=delete-selected&amp;checked[]=" + urlencode(plugin_file) + "&amp;plugin_status=" + context + "&amp;paged=" + page + "&amp;s=" + s, "bulk-plugins"), esc_attr(php_sprintf(_x("Delete %s", "plugin"), plugin_data["Name"])), __("Delete"))
                    # end if
                # end if
            else:
                if restrict_network_active:
                    actions = Array({"network_active": __("Network Active")})
                elif restrict_network_only:
                    actions = Array({"network_only": __("Network Only")})
                elif is_active:
                    if current_user_can("deactivate_plugin", plugin_file):
                        actions["deactivate"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=deactivate&amp;plugin=" + urlencode(plugin_file) + "&amp;plugin_status=" + context + "&amp;paged=" + page + "&amp;s=" + s, "deactivate-plugin_" + plugin_file), esc_attr(php_sprintf(_x("Deactivate %s", "plugin"), plugin_data["Name"])), __("Deactivate"))
                    # end if
                    if current_user_can("resume_plugin", plugin_file) and is_plugin_paused(plugin_file):
                        actions["resume"] = php_sprintf("<a class=\"resume-link\" href=\"%s\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=resume&amp;plugin=" + urlencode(plugin_file) + "&amp;plugin_status=" + context + "&amp;paged=" + page + "&amp;s=" + s, "resume-plugin_" + plugin_file), esc_attr(php_sprintf(_x("Resume %s", "plugin"), plugin_data["Name"])), __("Resume"))
                    # end if
                else:
                    if current_user_can("activate_plugin", plugin_file):
                        actions["activate"] = php_sprintf("<a href=\"%s\" class=\"edit\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=activate&amp;plugin=" + urlencode(plugin_file) + "&amp;plugin_status=" + context + "&amp;paged=" + page + "&amp;s=" + s, "activate-plugin_" + plugin_file), esc_attr(php_sprintf(_x("Activate %s", "plugin"), plugin_data["Name"])), __("Activate"))
                    # end if
                    if (not is_multisite()) and current_user_can("delete_plugins"):
                        actions["delete"] = php_sprintf("<a href=\"%s\" class=\"delete\" aria-label=\"%s\">%s</a>", wp_nonce_url("plugins.php?action=delete-selected&amp;checked[]=" + urlencode(plugin_file) + "&amp;plugin_status=" + context + "&amp;paged=" + page + "&amp;s=" + s, "bulk-plugins"), esc_attr(php_sprintf(_x("Delete %s", "plugin"), plugin_data["Name"])), __("Delete"))
                    # end if
                # end if
                pass
            # end if
            pass
        # end if
        #// End if $context.
        actions = php_array_filter(actions)
        if screen.in_admin("network"):
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
            actions = apply_filters("network_admin_plugin_action_links", actions, plugin_file, plugin_data, context)
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
            actions = apply_filters(str("network_admin_plugin_action_links_") + str(plugin_file), actions, plugin_file, plugin_data, context)
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
            actions = apply_filters("plugin_action_links", actions, plugin_file, plugin_data, context)
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
            actions = apply_filters(str("plugin_action_links_") + str(plugin_file), actions, plugin_file, plugin_data, context)
        # end if
        requires_php = plugin_data["requires_php"] if (php_isset(lambda : plugin_data["requires_php"])) else None
        compatible_php = is_php_version_compatible(requires_php)
        class_ = "active" if is_active else "inactive"
        checkbox_id = "checkbox_" + php_md5(plugin_data["Name"])
        if restrict_network_active or restrict_network_only or php_in_array(status, Array("mustuse", "dropins")) or (not compatible_php):
            checkbox = ""
        else:
            checkbox = php_sprintf("<label class=\"screen-reader-text\" for=\"%1$s\">%2$s</label>" + "<input type=\"checkbox\" name=\"checked[]\" value=\"%3$s\" id=\"%1$s\" />", checkbox_id, php_sprintf(__("Select %s"), plugin_data["Name"]), esc_attr(plugin_file))
        # end if
        if "dropins" != context:
            description = "<p>" + plugin_data["Description"] if plugin_data["Description"] else "&nbsp;" + "</p>"
            plugin_name = plugin_data["Name"]
        # end if
        if (not php_empty(lambda : totals["upgrade"])) and (not php_empty(lambda : plugin_data["update"])):
            class_ += " update"
        # end if
        paused = (not screen.in_admin("network")) and is_plugin_paused(plugin_file)
        if paused:
            class_ += " paused"
        # end if
        plugin_slug = plugin_data["slug"] if (php_isset(lambda : plugin_data["slug"])) else sanitize_title(plugin_name)
        printf("<tr class=\"%s\" data-slug=\"%s\" data-plugin=\"%s\">", esc_attr(class_), esc_attr(plugin_slug), esc_attr(plugin_file))
        columns, hidden, sortable, primary = self.get_column_info()
        for column_name,column_display_name in columns:
            extra_classes = ""
            if php_in_array(column_name, hidden):
                extra_classes = " hidden"
            # end if
            for case in Switch(column_name):
                if case("cb"):
                    php_print(str("<th scope='row' class='check-column'>") + str(checkbox) + str("</th>"))
                    break
                # end if
                if case("name"):
                    php_print(str("<td class='plugin-title column-primary'><strong>") + str(plugin_name) + str("</strong>"))
                    php_print(self.row_actions(actions, True))
                    php_print("</td>")
                    break
                # end if
                if case("description"):
                    classes = "column-description desc"
                    php_print(str("<td class='") + str(classes) + str(extra_classes) + str("'>\n                        <div class='plugin-description'>") + str(description) + str("</div>\n                       <div class='") + str(class_) + str(" second plugin-version-author-uri'>"))
                    plugin_meta = Array()
                    if (not php_empty(lambda : plugin_data["Version"])):
                        #// translators: %s: Plugin version number.
                        plugin_meta[-1] = php_sprintf(__("Version %s"), plugin_data["Version"])
                    # end if
                    if (not php_empty(lambda : plugin_data["Author"])):
                        author = plugin_data["Author"]
                        if (not php_empty(lambda : plugin_data["AuthorURI"])):
                            author = "<a href=\"" + plugin_data["AuthorURI"] + "\">" + plugin_data["Author"] + "</a>"
                        # end if
                        #// translators: %s: Plugin author name.
                        plugin_meta[-1] = php_sprintf(__("By %s"), author)
                    # end if
                    #// Details link using API info, if available.
                    if (php_isset(lambda : plugin_data["slug"])) and current_user_can("install_plugins"):
                        plugin_meta[-1] = php_sprintf("<a href=\"%s\" class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\" data-title=\"%s\">%s</a>", esc_url(network_admin_url("plugin-install.php?tab=plugin-information&plugin=" + plugin_data["slug"] + "&TB_iframe=true&width=600&height=550")), esc_attr(php_sprintf(__("More information about %s"), plugin_name)), esc_attr(plugin_name), __("View details"))
                    elif (not php_empty(lambda : plugin_data["PluginURI"])):
                        plugin_meta[-1] = php_sprintf("<a href=\"%s\">%s</a>", esc_url(plugin_data["PluginURI"]), __("Visit plugin site"))
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
                    plugin_meta = apply_filters("plugin_row_meta", plugin_meta, plugin_file, plugin_data, status)
                    php_print(php_implode(" | ", plugin_meta))
                    php_print("</div>")
                    if paused:
                        notice_text = __("This plugin failed to load properly and is paused during recovery mode.")
                        printf("<p><span class=\"dashicons dashicons-warning\"></span> <strong>%s</strong></p>", notice_text)
                        error = wp_get_plugin_error(plugin_file)
                        if False != error:
                            printf("<div class=\"error-display\"><p>%s</p></div>", wp_get_extension_error_description(error))
                        # end if
                    # end if
                    php_print("</td>")
                    break
                # end if
                if case():
                    classes = str(column_name) + str(" column-") + str(column_name) + str(" ") + str(class_)
                    php_print(str("<td class='") + str(classes) + str(extra_classes) + str("'>"))
                    #// 
                    #// Fires inside each custom column of the Plugins list table.
                    #// 
                    #// @since 3.1.0
                    #// 
                    #// @param string $column_name Name of the column.
                    #// @param string $plugin_file Path to the plugin file relative to the plugins directory.
                    #// @param array  $plugin_data An array of plugin data.
                    #//
                    do_action("manage_plugins_custom_column", column_name, plugin_file, plugin_data)
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
        do_action("after_plugin_row", plugin_file, plugin_data, status)
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
        do_action(str("after_plugin_row_") + str(plugin_file), plugin_file, plugin_data, status)
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
