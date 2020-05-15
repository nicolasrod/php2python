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
#// List Table API: WP_Plugin_Install_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying plugins to install in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Plugin_Install_List_Table(WP_List_Table):
    order = "ASC"
    orderby = None
    groups = Array()
    error = Array()
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        return current_user_can("install_plugins")
    # end def ajax_user_can
    #// 
    #// Return the list of known plugins.
    #// 
    #// Uses the transient data from the updates API to determine the known
    #// installed plugins.
    #// 
    #// @since 4.9.0
    #// @access protected
    #// 
    #// @return array
    #//
    def get_installed_plugins(self):
        
        plugins = Array()
        plugin_info = get_site_transient("update_plugins")
        if (php_isset(lambda : plugin_info.no_update)):
            for plugin in plugin_info.no_update:
                plugin.upgrade = False
                plugins[plugin.slug] = plugin
            # end for
        # end if
        if (php_isset(lambda : plugin_info.response)):
            for plugin in plugin_info.response:
                plugin.upgrade = True
                plugins[plugin.slug] = plugin
            # end for
        # end if
        return plugins
    # end def get_installed_plugins
    #// 
    #// Return a list of slugs of installed plugins, if known.
    #// 
    #// Uses the transient data from the updates API to determine the slugs of
    #// known installed plugins. This might be better elsewhere, perhaps even
    #// within get_plugins().
    #// 
    #// @since 4.0.0
    #// 
    #// @return array
    #//
    def get_installed_plugin_slugs(self):
        
        return php_array_keys(self.get_installed_plugins())
    # end def get_installed_plugin_slugs
    #// 
    #// @global array  $tabs
    #// @global string $tab
    #// @global int    $paged
    #// @global string $type
    #// @global string $term
    #//
    def prepare_items(self):
        
        php_include_file(ABSPATH + "wp-admin/includes/plugin-install.php", once=False)
        global tabs,tab,paged,type,term
        php_check_if_defined("tabs","tab","paged","type","term")
        wp_reset_vars(Array("tab"))
        paged = self.get_pagenum()
        per_page = 36
        #// These are the tabs which are shown on the page.
        tabs = Array()
        if "search" == tab:
            tabs["search"] = __("Search Results")
        # end if
        if "beta" == tab or False != php_strpos(get_bloginfo("version"), "-"):
            tabs["beta"] = _x("Beta Testing", "Plugin Installer")
        # end if
        tabs["featured"] = _x("Featured", "Plugin Installer")
        tabs["popular"] = _x("Popular", "Plugin Installer")
        tabs["recommended"] = _x("Recommended", "Plugin Installer")
        tabs["favorites"] = _x("Favorites", "Plugin Installer")
        if current_user_can("upload_plugins"):
            #// No longer a real tab. Here for filter compatibility.
            #// Gets skipped in get_views().
            tabs["upload"] = __("Upload Plugin")
        # end if
        nonmenu_tabs = Array("plugin-information")
        #// Valid actions to perform which do not have a Menu item.
        #// 
        #// Filters the tabs shown on the Plugin Install screen.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string[] $tabs The tabs shown on the Plugin Install screen. Defaults include 'featured', 'popular',
        #// 'recommended', 'favorites', and 'upload'.
        #//
        tabs = apply_filters("install_plugins_tabs", tabs)
        #// 
        #// Filters tabs not associated with a menu item on the Plugin Install screen.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string[] $nonmenu_tabs The tabs that don't have a menu item on the Plugin Install screen.
        #//
        nonmenu_tabs = apply_filters("install_plugins_nonmenu_tabs", nonmenu_tabs)
        #// If a non-valid menu tab has been selected, And it's not a non-menu action.
        if php_empty(lambda : tab) or (not (php_isset(lambda : tabs[tab]))) and (not php_in_array(tab, nonmenu_tabs)):
            tab = key(tabs)
        # end if
        installed_plugins = self.get_installed_plugins()
        args = Array({"page": paged, "per_page": per_page, "locale": get_user_locale()})
        for case in Switch(tab):
            if case("search"):
                type = wp_unslash(PHP_REQUEST["type"]) if (php_isset(lambda : PHP_REQUEST["type"])) else "term"
                term = wp_unslash(PHP_REQUEST["s"]) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
                for case in Switch(type):
                    if case("tag"):
                        args["tag"] = sanitize_title_with_dashes(term)
                        break
                    # end if
                    if case("term"):
                        args["search"] = term
                        break
                    # end if
                    if case("author"):
                        args["author"] = term
                        break
                    # end if
                # end for
                break
            # end if
            if case("featured"):
                pass
            # end if
            if case("popular"):
                pass
            # end if
            if case("new"):
                pass
            # end if
            if case("beta"):
                args["browse"] = tab
                break
            # end if
            if case("recommended"):
                args["browse"] = tab
                #// Include the list of installed plugins so we can get relevant results.
                args["installed_plugins"] = php_array_keys(installed_plugins)
                break
            # end if
            if case("favorites"):
                action = "save_wporg_username_" + get_current_user_id()
                if (php_isset(lambda : PHP_REQUEST["_wpnonce"])) and wp_verify_nonce(wp_unslash(PHP_REQUEST["_wpnonce"]), action):
                    user = wp_unslash(PHP_REQUEST["user"]) if (php_isset(lambda : PHP_REQUEST["user"])) else get_user_option("wporg_favorites")
                    #// If the save url parameter is passed with a falsey value, don't save the favorite user.
                    if (not (php_isset(lambda : PHP_REQUEST["save"]))) or PHP_REQUEST["save"]:
                        update_user_meta(get_current_user_id(), "wporg_favorites", user)
                    # end if
                else:
                    user = get_user_option("wporg_favorites")
                # end if
                if user:
                    args["user"] = user
                else:
                    args = False
                # end if
                add_action("install_plugins_favorites", "install_plugins_favorites_form", 9, 0)
                break
            # end if
            if case():
                args = False
                break
            # end if
        # end for
        #// 
        #// Filters API request arguments for each Plugin Install screen tab.
        #// 
        #// The dynamic portion of the hook name, `$tab`, refers to the plugin install tabs.
        #// Default tabs include 'featured', 'popular', 'recommended', 'favorites', and 'upload'.
        #// 
        #// @since 3.7.0
        #// 
        #// @param array|bool $args Plugin Install API arguments.
        #//
        args = apply_filters(str("install_plugins_table_api_args_") + str(tab), args)
        if (not args):
            return
        # end if
        api = plugins_api("query_plugins", args)
        if is_wp_error(api):
            self.error = api
            return
        # end if
        self.items = api.plugins
        if self.orderby:
            uasort(self.items, Array(self, "order_callback"))
        # end if
        self.set_pagination_args(Array({"total_items": api.info["results"], "per_page": args["per_page"]}))
        if (php_isset(lambda : api.info["groups"])):
            self.groups = api.info["groups"]
        # end if
        if installed_plugins:
            js_plugins = php_array_fill_keys(Array("all", "search", "active", "inactive", "recently_activated", "mustuse", "dropins"), Array())
            js_plugins["all"] = php_array_values(wp_list_pluck(installed_plugins, "plugin"))
            upgrade_plugins = wp_filter_object_list(installed_plugins, Array({"upgrade": True}), "and", "plugin")
            if upgrade_plugins:
                js_plugins["upgrade"] = php_array_values(upgrade_plugins)
            # end if
            wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"plugins": js_plugins, "totals": wp_get_update_data()}))
        # end if
    # end def prepare_items
    #// 
    #//
    def no_items(self):
        
        if (php_isset(lambda : self.error)):
            php_print("         <div class=\"inline error\"><p>")
            php_print(self.error.get_error_message())
            php_print("</p>\n               <p class=\"hide-if-no-js\"><button class=\"button try-again\">")
            _e("Try Again")
            php_print("</button></p>\n          </div>\n        ")
        else:
            php_print("         <div class=\"no-plugin-results\">")
            _e("No plugins found. Try a different search.")
            php_print("</div>\n         ")
        # end if
    # end def no_items
    #// 
    #// @global array $tabs
    #// @global string $tab
    #// 
    #// @return array
    #//
    def get_views(self):
        
        global tabs,tab
        php_check_if_defined("tabs","tab")
        display_tabs = Array()
        for action,text in tabs:
            current_link_attributes = " class=\"current\" aria-current=\"page\"" if action == tab else ""
            href = self_admin_url("plugin-install.php?tab=" + action)
            display_tabs["plugin-install-" + action] = str("<a href='") + str(href) + str("'") + str(current_link_attributes) + str(">") + str(text) + str("</a>")
        # end for
        display_tabs["plugin-install-upload"] = None
        return display_tabs
    # end def get_views
    #// 
    #// Override parent views so we can use the filter bar display.
    #//
    def views(self):
        
        views = self.get_views()
        #// This filter is documented in wp-admin/inclues/class-wp-list-table.php
        views = apply_filters(str("views_") + str(self.screen.id), views)
        self.screen.render_screen_reader_content("heading_views")
        php_print("<div class=\"wp-filter\">\n  <ul class=\"filter-links\">\n       ")
        if (not php_empty(lambda : views)):
            for class_,view in views:
                views[class_] = str("   <li class='") + str(class_) + str("'>") + str(view)
            # end for
            php_print(php_implode(" </li>\n", views) + "</li>\n")
        # end if
        php_print(" </ul>\n\n       ")
        install_search_form()
        php_print("</div>\n     ")
    # end def views
    #// 
    #// Displays the plugin install table.
    #// 
    #// Overrides the parent display() method to provide a different container.
    #// 
    #// @since 4.0.0
    #//
    def display(self):
        
        singular = self._args["singular"]
        data_attr = ""
        if singular:
            data_attr = str(" data-wp-lists='list:") + str(singular) + str("'")
        # end if
        self.display_tablenav("top")
        php_print("<div class=\"wp-list-table ")
        php_print(php_implode(" ", self.get_table_classes()))
        php_print("\">\n        ")
        self.screen.render_screen_reader_content("heading_list")
        php_print(" <div id=\"the-list\"")
        php_print(data_attr)
        php_print(">\n      ")
        self.display_rows_or_placeholder()
        php_print(" </div>\n</div>\n        ")
        self.display_tablenav("bottom")
    # end def display
    #// 
    #// @global string $tab
    #// 
    #// @param string $which
    #//
    def display_tablenav(self, which=None):
        
        if "featured" == PHP_GLOBALS["tab"]:
            return
        # end if
        if "top" == which:
            wp_referer_field()
            php_print("         <div class=\"tablenav top\">\n              <div class=\"alignleft actions\">\n                 ")
            #// 
            #// Fires before the Plugin Install table header pagination is displayed.
            #// 
            #// @since 2.7.0
            #//
            do_action("install_plugins_table_header")
            php_print("             </div>\n                ")
            self.pagination(which)
            php_print("             <br class=\"clear\" />\n            </div>\n        ")
        else:
            php_print("         <div class=\"tablenav bottom\">\n               ")
            self.pagination(which)
            php_print("             <br class=\"clear\" />\n            </div>\n            ")
        # end if
    # end def display_tablenav
    #// 
    #// @return array
    #//
    def get_table_classes(self):
        
        return Array("widefat", self._args["plural"])
    # end def get_table_classes
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        return Array()
    # end def get_columns
    #// 
    #// @param object $plugin_a
    #// @param object $plugin_b
    #// @return int
    #//
    def order_callback(self, plugin_a=None, plugin_b=None):
        
        orderby = self.orderby
        if (not (php_isset(lambda : plugin_a.orderby) and php_isset(lambda : plugin_b.orderby))):
            return 0
        # end if
        a = plugin_a.orderby
        b = plugin_b.orderby
        if a == b:
            return 0
        # end if
        if "DESC" == self.order:
            return 1 if a < b else -1
        else:
            return -1 if a < b else 1
        # end if
    # end def order_callback
    def display_rows(self):
        
        plugins_allowedtags = Array({"a": Array({"href": Array(), "title": Array(), "target": Array()})}, {"abbr": Array({"title": Array()})}, {"acronym": Array({"title": Array()})}, {"code": Array(), "pre": Array(), "em": Array(), "strong": Array(), "ul": Array(), "ol": Array(), "li": Array(), "p": Array(), "br": Array()})
        plugins_group_titles = Array({"Performance": _x("Performance", "Plugin installer group title"), "Social": _x("Social", "Plugin installer group title"), "Tools": _x("Tools", "Plugin installer group title")})
        group = None
        for plugin in self.items:
            if php_is_object(plugin):
                plugin = plugin
            # end if
            #// Display the group heading if there is one.
            if (php_isset(lambda : plugin["group"])) and plugin["group"] != group:
                if (php_isset(lambda : self.groups[plugin["group"]])):
                    group_name = self.groups[plugin["group"]]
                    if (php_isset(lambda : plugins_group_titles[group_name])):
                        group_name = plugins_group_titles[group_name]
                    # end if
                else:
                    group_name = plugin["group"]
                # end if
                #// Starting a new group, close off the divs of the last one.
                if (not php_empty(lambda : group)):
                    php_print("</div></div>")
                # end if
                php_print("<div class=\"plugin-group\"><h3>" + esc_html(group_name) + "</h3>")
                #// Needs an extra wrapping div for nth-child selectors to work.
                php_print("<div class=\"plugin-items\">")
                group = plugin["group"]
            # end if
            title = wp_kses(plugin["name"], plugins_allowedtags)
            #// Remove any HTML from the description.
            description = strip_tags(plugin["short_description"])
            version = wp_kses(plugin["version"], plugins_allowedtags)
            name = strip_tags(title + " " + version)
            author = wp_kses(plugin["author"], plugins_allowedtags)
            if (not php_empty(lambda : author)):
                #// translators: %s: Plugin author.
                author = " <cite>" + php_sprintf(__("By %s"), author) + "</cite>"
            # end if
            requires_php = plugin["requires_php"] if (php_isset(lambda : plugin["requires_php"])) else None
            requires_wp = plugin["requires"] if (php_isset(lambda : plugin["requires"])) else None
            compatible_php = is_php_version_compatible(requires_php)
            compatible_wp = is_wp_version_compatible(requires_wp)
            tested_wp = php_empty(lambda : plugin["tested"]) or php_version_compare(get_bloginfo("version"), plugin["tested"], "<=")
            action_links = Array()
            if current_user_can("install_plugins") or current_user_can("update_plugins"):
                status = install_plugin_install_status(plugin)
                for case in Switch(status["status"]):
                    if case("install"):
                        if status["url"]:
                            if compatible_php and compatible_wp:
                                action_links[-1] = php_sprintf("<a class=\"install-now button\" data-slug=\"%s\" href=\"%s\" aria-label=\"%s\" data-name=\"%s\">%s</a>", esc_attr(plugin["slug"]), esc_url(status["url"]), esc_attr(php_sprintf(__("Install %s now"), name)), esc_attr(name), __("Install Now"))
                            else:
                                action_links[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Cannot Install", "plugin"))
                            # end if
                        # end if
                        break
                    # end if
                    if case("update_available"):
                        if status["url"]:
                            if compatible_php and compatible_wp:
                                action_links[-1] = php_sprintf("<a class=\"update-now button aria-button-if-js\" data-plugin=\"%s\" data-slug=\"%s\" href=\"%s\" aria-label=\"%s\" data-name=\"%s\">%s</a>", esc_attr(status["file"]), esc_attr(plugin["slug"]), esc_url(status["url"]), esc_attr(php_sprintf(__("Update %s now"), name)), esc_attr(name), __("Update Now"))
                            else:
                                action_links[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Cannot Update", "plugin"))
                            # end if
                        # end if
                        break
                    # end if
                    if case("latest_installed"):
                        pass
                    # end if
                    if case("newer_installed"):
                        if is_plugin_active(status["file"]):
                            action_links[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Active", "plugin"))
                        elif current_user_can("activate_plugin", status["file"]):
                            button_text = __("Activate")
                            #// translators: %s: Plugin name.
                            button_label = _x("Activate %s", "plugin")
                            activate_url = add_query_arg(Array({"_wpnonce": wp_create_nonce("activate-plugin_" + status["file"]), "action": "activate", "plugin": status["file"]}), network_admin_url("plugins.php"))
                            if is_network_admin():
                                button_text = __("Network Activate")
                                #// translators: %s: Plugin name.
                                button_label = _x("Network Activate %s", "plugin")
                                activate_url = add_query_arg(Array({"networkwide": 1}), activate_url)
                            # end if
                            action_links[-1] = php_sprintf("<a href=\"%1$s\" class=\"button activate-now\" aria-label=\"%2$s\">%3$s</a>", esc_url(activate_url), esc_attr(php_sprintf(button_label, plugin["name"])), button_text)
                        else:
                            action_links[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Installed", "plugin"))
                        # end if
                        break
                    # end if
                # end for
            # end if
            details_link = self_admin_url("plugin-install.php?tab=plugin-information&amp;plugin=" + plugin["slug"] + "&amp;TB_iframe=true&amp;width=600&amp;height=550")
            action_links[-1] = php_sprintf("<a href=\"%s\" class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\" data-title=\"%s\">%s</a>", esc_url(details_link), esc_attr(php_sprintf(__("More information about %s"), name)), esc_attr(name), __("More Details"))
            if (not php_empty(lambda : plugin["icons"]["svg"])):
                plugin_icon_url = plugin["icons"]["svg"]
            elif (not php_empty(lambda : plugin["icons"]["2x"])):
                plugin_icon_url = plugin["icons"]["2x"]
            elif (not php_empty(lambda : plugin["icons"]["1x"])):
                plugin_icon_url = plugin["icons"]["1x"]
            else:
                plugin_icon_url = plugin["icons"]["default"]
            # end if
            #// 
            #// Filters the install action links for a plugin.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $action_links An array of plugin action links. Defaults are links to Details and Install Now.
            #// @param array    $plugin       The plugin currently being listed.
            #//
            action_links = apply_filters("plugin_install_action_links", action_links, plugin)
            last_updated_timestamp = strtotime(plugin["last_updated"])
            php_print("     <div class=\"plugin-card plugin-card-")
            php_print(sanitize_html_class(plugin["slug"]))
            php_print("\">\n            ")
            if (not compatible_php) or (not compatible_wp):
                php_print("<div class=\"notice inline notice-error notice-alt\"><p>")
                if (not compatible_php) and (not compatible_wp):
                    _e("This plugin doesn&#8217;t work with your versions of WordPress and PHP.")
                    if current_user_can("update_core") and current_user_can("update_php"):
                        printf(" " + __("<a href=\"%1$s\">Please update WordPress</a>, and then <a href=\"%2$s\">learn more about updating PHP</a>."), self_admin_url("update-core.php"), esc_url(wp_get_update_php_url()))
                        wp_update_php_annotation("</p><p><em>", "</em>")
                    elif current_user_can("update_core"):
                        printf(" " + __("<a href=\"%s\">Please update WordPress</a>."), self_admin_url("update-core.php"))
                    elif current_user_can("update_php"):
                        printf(" " + __("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
                        wp_update_php_annotation("</p><p><em>", "</em>")
                    # end if
                elif (not compatible_wp):
                    _e("This plugin doesn&#8217;t work with your version of WordPress.")
                    if current_user_can("update_core"):
                        printf(" " + __("<a href=\"%s\">Please update WordPress</a>."), self_admin_url("update-core.php"))
                    # end if
                elif (not compatible_php):
                    _e("This plugin doesn&#8217;t work with your version of PHP.")
                    if current_user_can("update_php"):
                        printf(" " + __("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
                        wp_update_php_annotation("</p><p><em>", "</em>")
                    # end if
                # end if
                php_print("</p></div>")
            # end if
            php_print("""           <div class=\"plugin-card-top\">
            <div class=\"name column-name\">
            <h3>
            <a href=\"""")
            php_print(esc_url(details_link))
            php_print("\" class=\"thickbox open-plugin-details-modal\">\n                       ")
            php_print(title)
            php_print("                     <img src=\"")
            php_print(esc_attr(plugin_icon_url))
            php_print("""\" class=\"plugin-icon\" alt=\"\">
            </a>
            </h3>
            </div>
            <div class=\"action-links\">
            """)
            if action_links:
                php_print("<ul class=\"plugin-action-buttons\"><li>" + php_implode("</li><li>", action_links) + "</li></ul>")
            # end if
            php_print("             </div>\n                <div class=\"desc column-description\">\n                   <p>")
            php_print(description)
            php_print("</p>\n                   <p class=\"authors\">")
            php_print(author)
            php_print("""</p>
            </div>
            </div>
            <div class=\"plugin-card-bottom\">
            <div class=\"vers column-rating\">
            """)
            wp_star_rating(Array({"rating": plugin["rating"], "type": "percent", "number": plugin["num_ratings"]}))
            php_print("                 <span class=\"num-ratings\" aria-hidden=\"true\">(")
            php_print(number_format_i18n(plugin["num_ratings"]))
            php_print(""")</span>
            </div>
            <div class=\"column-updated\">
            <strong>""")
            _e("Last Updated:")
            php_print("</strong>\n                  ")
            #// translators: %s: Human-readable time difference.
            printf(__("%s ago"), human_time_diff(last_updated_timestamp))
            php_print("             </div>\n                <div class=\"column-downloaded\">\n                 ")
            if plugin["active_installs"] >= 1000000:
                active_installs_millions = floor(plugin["active_installs"] / 1000000)
                active_installs_text = php_sprintf(_nx("%s+ Million", "%s+ Million", active_installs_millions, "Active plugin installations"), number_format_i18n(active_installs_millions))
            elif 0 == plugin["active_installs"]:
                active_installs_text = _x("Less Than 10", "Active plugin installations")
            else:
                active_installs_text = number_format_i18n(plugin["active_installs"]) + "+"
            # end if
            #// translators: %s: Number of installations.
            printf(__("%s Active Installations"), active_installs_text)
            php_print("             </div>\n                <div class=\"column-compatibility\">\n                  ")
            if (not tested_wp):
                php_print("<span class=\"compatibility-untested\">" + __("Untested with your version of WordPress") + "</span>")
            elif (not compatible_wp):
                php_print("<span class=\"compatibility-incompatible\">" + __("<strong>Incompatible</strong> with your version of WordPress") + "</span>")
            else:
                php_print("<span class=\"compatibility-compatible\">" + __("<strong>Compatible</strong> with your version of WordPress") + "</span>")
            # end if
            php_print("""               </div>
            </div>
            </div>
            """)
        # end for
        #// Close off the group divs of the last one.
        if (not php_empty(lambda : group)):
            php_print("</div></div>")
        # end if
    # end def display_rows
# end class WP_Plugin_Install_List_Table
