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
        
        
        plugins_ = Array()
        plugin_info_ = get_site_transient("update_plugins")
        if (php_isset(lambda : plugin_info_.no_update)):
            for plugin_ in plugin_info_.no_update:
                plugin_.upgrade = False
                plugins_[plugin_.slug] = plugin_
            # end for
        # end if
        if (php_isset(lambda : plugin_info_.response)):
            for plugin_ in plugin_info_.response:
                plugin_.upgrade = True
                plugins_[plugin_.slug] = plugin_
            # end for
        # end if
        return plugins_
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
        global tabs_
        global tab_
        global paged_
        global type_
        global term_
        php_check_if_defined("tabs_","tab_","paged_","type_","term_")
        wp_reset_vars(Array("tab"))
        paged_ = self.get_pagenum()
        per_page_ = 36
        #// These are the tabs which are shown on the page.
        tabs_ = Array()
        if "search" == tab_:
            tabs_["search"] = __("Search Results")
        # end if
        if "beta" == tab_ or False != php_strpos(get_bloginfo("version"), "-"):
            tabs_["beta"] = _x("Beta Testing", "Plugin Installer")
        # end if
        tabs_["featured"] = _x("Featured", "Plugin Installer")
        tabs_["popular"] = _x("Popular", "Plugin Installer")
        tabs_["recommended"] = _x("Recommended", "Plugin Installer")
        tabs_["favorites"] = _x("Favorites", "Plugin Installer")
        if current_user_can("upload_plugins"):
            #// No longer a real tab. Here for filter compatibility.
            #// Gets skipped in get_views().
            tabs_["upload"] = __("Upload Plugin")
        # end if
        nonmenu_tabs_ = Array("plugin-information")
        #// Valid actions to perform which do not have a Menu item.
        #// 
        #// Filters the tabs shown on the Plugin Install screen.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string[] $tabs The tabs shown on the Plugin Install screen. Defaults include 'featured', 'popular',
        #// 'recommended', 'favorites', and 'upload'.
        #//
        tabs_ = apply_filters("install_plugins_tabs", tabs_)
        #// 
        #// Filters tabs not associated with a menu item on the Plugin Install screen.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string[] $nonmenu_tabs The tabs that don't have a menu item on the Plugin Install screen.
        #//
        nonmenu_tabs_ = apply_filters("install_plugins_nonmenu_tabs", nonmenu_tabs_)
        #// If a non-valid menu tab has been selected, And it's not a non-menu action.
        if php_empty(lambda : tab_) or (not (php_isset(lambda : tabs_[tab_]))) and (not php_in_array(tab_, nonmenu_tabs_)):
            tab_ = key(tabs_)
        # end if
        installed_plugins_ = self.get_installed_plugins()
        args_ = Array({"page": paged_, "per_page": per_page_, "locale": get_user_locale()})
        for case in Switch(tab_):
            if case("search"):
                type_ = wp_unslash(PHP_REQUEST["type"]) if (php_isset(lambda : PHP_REQUEST["type"])) else "term"
                term_ = wp_unslash(PHP_REQUEST["s"]) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
                for case in Switch(type_):
                    if case("tag"):
                        args_["tag"] = sanitize_title_with_dashes(term_)
                        break
                    # end if
                    if case("term"):
                        args_["search"] = term_
                        break
                    # end if
                    if case("author"):
                        args_["author"] = term_
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
                args_["browse"] = tab_
                break
            # end if
            if case("recommended"):
                args_["browse"] = tab_
                #// Include the list of installed plugins so we can get relevant results.
                args_["installed_plugins"] = php_array_keys(installed_plugins_)
                break
            # end if
            if case("favorites"):
                action_ = "save_wporg_username_" + get_current_user_id()
                if (php_isset(lambda : PHP_REQUEST["_wpnonce"])) and wp_verify_nonce(wp_unslash(PHP_REQUEST["_wpnonce"]), action_):
                    user_ = wp_unslash(PHP_REQUEST["user"]) if (php_isset(lambda : PHP_REQUEST["user"])) else get_user_option("wporg_favorites")
                    #// If the save url parameter is passed with a falsey value, don't save the favorite user.
                    if (not (php_isset(lambda : PHP_REQUEST["save"]))) or PHP_REQUEST["save"]:
                        update_user_meta(get_current_user_id(), "wporg_favorites", user_)
                    # end if
                else:
                    user_ = get_user_option("wporg_favorites")
                # end if
                if user_:
                    args_["user"] = user_
                else:
                    args_ = False
                # end if
                add_action("install_plugins_favorites", "install_plugins_favorites_form", 9, 0)
                break
            # end if
            if case():
                args_ = False
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
        args_ = apply_filters(str("install_plugins_table_api_args_") + str(tab_), args_)
        if (not args_):
            return
        # end if
        api_ = plugins_api("query_plugins", args_)
        if is_wp_error(api_):
            self.error = api_
            return
        # end if
        self.items = api_.plugins
        if self.orderby:
            uasort(self.items, Array(self, "order_callback"))
        # end if
        self.set_pagination_args(Array({"total_items": api_.info["results"], "per_page": args_["per_page"]}))
        if (php_isset(lambda : api_.info["groups"])):
            self.groups = api_.info["groups"]
        # end if
        if installed_plugins_:
            js_plugins_ = php_array_fill_keys(Array("all", "search", "active", "inactive", "recently_activated", "mustuse", "dropins"), Array())
            js_plugins_["all"] = php_array_values(wp_list_pluck(installed_plugins_, "plugin"))
            upgrade_plugins_ = wp_filter_object_list(installed_plugins_, Array({"upgrade": True}), "and", "plugin")
            if upgrade_plugins_:
                js_plugins_["upgrade"] = php_array_values(upgrade_plugins_)
            # end if
            wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"plugins": js_plugins_, "totals": wp_get_update_data()}))
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
        
        
        global tabs_
        global tab_
        php_check_if_defined("tabs_","tab_")
        display_tabs_ = Array()
        for action_,text_ in tabs_.items():
            current_link_attributes_ = " class=\"current\" aria-current=\"page\"" if action_ == tab_ else ""
            href_ = self_admin_url("plugin-install.php?tab=" + action_)
            display_tabs_["plugin-install-" + action_] = str("<a href='") + str(href_) + str("'") + str(current_link_attributes_) + str(">") + str(text_) + str("</a>")
        # end for
        display_tabs_["plugin-install-upload"] = None
        return display_tabs_
    # end def get_views
    #// 
    #// Override parent views so we can use the filter bar display.
    #//
    def views(self):
        
        
        views_ = self.get_views()
        #// This filter is documented in wp-admin/inclues/class-wp-list-table.php
        views_ = apply_filters(str("views_") + str(self.screen.id), views_)
        self.screen.render_screen_reader_content("heading_views")
        php_print("<div class=\"wp-filter\">\n  <ul class=\"filter-links\">\n       ")
        if (not php_empty(lambda : views_)):
            for class_,view_ in views_.items():
                views_[class_] = str("  <li class='") + str(class_) + str("'>") + str(view_)
            # end for
            php_print(php_implode(" </li>\n", views_) + "</li>\n")
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
        
        
        singular_ = self._args["singular"]
        data_attr_ = ""
        if singular_:
            data_attr_ = str(" data-wp-lists='list:") + str(singular_) + str("'")
        # end if
        self.display_tablenav("top")
        php_print("<div class=\"wp-list-table ")
        php_print(php_implode(" ", self.get_table_classes()))
        php_print("\">\n        ")
        self.screen.render_screen_reader_content("heading_list")
        php_print(" <div id=\"the-list\"")
        php_print(data_attr_)
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
    def display_tablenav(self, which_=None):
        
        
        if "featured" == PHP_GLOBALS["tab"]:
            return
        # end if
        if "top" == which_:
            wp_referer_field()
            php_print("         <div class=\"tablenav top\">\n              <div class=\"alignleft actions\">\n                 ")
            #// 
            #// Fires before the Plugin Install table header pagination is displayed.
            #// 
            #// @since 2.7.0
            #//
            do_action("install_plugins_table_header")
            php_print("             </div>\n                ")
            self.pagination(which_)
            php_print("             <br class=\"clear\" />\n            </div>\n        ")
        else:
            php_print("         <div class=\"tablenav bottom\">\n               ")
            self.pagination(which_)
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
    def order_callback(self, plugin_a_=None, plugin_b_=None):
        
        
        orderby_ = self.orderby
        if (not (php_isset(lambda : plugin_a_.orderby_) and php_isset(lambda : plugin_b_.orderby_))):
            return 0
        # end if
        a_ = plugin_a_.orderby_
        b_ = plugin_b_.orderby_
        if a_ == b_:
            return 0
        # end if
        if "DESC" == self.order:
            return 1 if a_ < b_ else -1
        else:
            return -1 if a_ < b_ else 1
        # end if
    # end def order_callback
    def display_rows(self):
        
        
        plugins_allowedtags_ = Array({"a": Array({"href": Array(), "title": Array(), "target": Array()})}, {"abbr": Array({"title": Array()})}, {"acronym": Array({"title": Array()})}, {"code": Array(), "pre": Array(), "em": Array(), "strong": Array(), "ul": Array(), "ol": Array(), "li": Array(), "p": Array(), "br": Array()})
        plugins_group_titles_ = Array({"Performance": _x("Performance", "Plugin installer group title"), "Social": _x("Social", "Plugin installer group title"), "Tools": _x("Tools", "Plugin installer group title")})
        group_ = None
        for plugin_ in self.items:
            if php_is_object(plugin_):
                plugin_ = plugin_
            # end if
            #// Display the group heading if there is one.
            if (php_isset(lambda : plugin_["group"])) and plugin_["group"] != group_:
                if (php_isset(lambda : self.groups[plugin_["group"]])):
                    group_name_ = self.groups[plugin_["group"]]
                    if (php_isset(lambda : plugins_group_titles_[group_name_])):
                        group_name_ = plugins_group_titles_[group_name_]
                    # end if
                else:
                    group_name_ = plugin_["group"]
                # end if
                #// Starting a new group, close off the divs of the last one.
                if (not php_empty(lambda : group_)):
                    php_print("</div></div>")
                # end if
                php_print("<div class=\"plugin-group\"><h3>" + esc_html(group_name_) + "</h3>")
                #// Needs an extra wrapping div for nth-child selectors to work.
                php_print("<div class=\"plugin-items\">")
                group_ = plugin_["group"]
            # end if
            title_ = wp_kses(plugin_["name"], plugins_allowedtags_)
            #// Remove any HTML from the description.
            description_ = strip_tags(plugin_["short_description"])
            version_ = wp_kses(plugin_["version"], plugins_allowedtags_)
            name_ = strip_tags(title_ + " " + version_)
            author_ = wp_kses(plugin_["author"], plugins_allowedtags_)
            if (not php_empty(lambda : author_)):
                #// translators: %s: Plugin author.
                author_ = " <cite>" + php_sprintf(__("By %s"), author_) + "</cite>"
            # end if
            requires_php_ = plugin_["requires_php"] if (php_isset(lambda : plugin_["requires_php"])) else None
            requires_wp_ = plugin_["requires"] if (php_isset(lambda : plugin_["requires"])) else None
            compatible_php_ = is_php_version_compatible(requires_php_)
            compatible_wp_ = is_wp_version_compatible(requires_wp_)
            tested_wp_ = php_empty(lambda : plugin_["tested"]) or php_version_compare(get_bloginfo("version"), plugin_["tested"], "<=")
            action_links_ = Array()
            if current_user_can("install_plugins") or current_user_can("update_plugins"):
                status_ = install_plugin_install_status(plugin_)
                for case in Switch(status_["status"]):
                    if case("install"):
                        if status_["url"]:
                            if compatible_php_ and compatible_wp_:
                                action_links_[-1] = php_sprintf("<a class=\"install-now button\" data-slug=\"%s\" href=\"%s\" aria-label=\"%s\" data-name=\"%s\">%s</a>", esc_attr(plugin_["slug"]), esc_url(status_["url"]), esc_attr(php_sprintf(__("Install %s now"), name_)), esc_attr(name_), __("Install Now"))
                            else:
                                action_links_[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Cannot Install", "plugin"))
                            # end if
                        # end if
                        break
                    # end if
                    if case("update_available"):
                        if status_["url"]:
                            if compatible_php_ and compatible_wp_:
                                action_links_[-1] = php_sprintf("<a class=\"update-now button aria-button-if-js\" data-plugin=\"%s\" data-slug=\"%s\" href=\"%s\" aria-label=\"%s\" data-name=\"%s\">%s</a>", esc_attr(status_["file"]), esc_attr(plugin_["slug"]), esc_url(status_["url"]), esc_attr(php_sprintf(__("Update %s now"), name_)), esc_attr(name_), __("Update Now"))
                            else:
                                action_links_[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Cannot Update", "plugin"))
                            # end if
                        # end if
                        break
                    # end if
                    if case("latest_installed"):
                        pass
                    # end if
                    if case("newer_installed"):
                        if is_plugin_active(status_["file"]):
                            action_links_[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Active", "plugin"))
                        elif current_user_can("activate_plugin", status_["file"]):
                            button_text_ = __("Activate")
                            #// translators: %s: Plugin name.
                            button_label_ = _x("Activate %s", "plugin")
                            activate_url_ = add_query_arg(Array({"_wpnonce": wp_create_nonce("activate-plugin_" + status_["file"]), "action": "activate", "plugin": status_["file"]}), network_admin_url("plugins.php"))
                            if is_network_admin():
                                button_text_ = __("Network Activate")
                                #// translators: %s: Plugin name.
                                button_label_ = _x("Network Activate %s", "plugin")
                                activate_url_ = add_query_arg(Array({"networkwide": 1}), activate_url_)
                            # end if
                            action_links_[-1] = php_sprintf("<a href=\"%1$s\" class=\"button activate-now\" aria-label=\"%2$s\">%3$s</a>", esc_url(activate_url_), esc_attr(php_sprintf(button_label_, plugin_["name"])), button_text_)
                        else:
                            action_links_[-1] = php_sprintf("<button type=\"button\" class=\"button button-disabled\" disabled=\"disabled\">%s</button>", _x("Installed", "plugin"))
                        # end if
                        break
                    # end if
                # end for
            # end if
            details_link_ = self_admin_url("plugin-install.php?tab=plugin-information&amp;plugin=" + plugin_["slug"] + "&amp;TB_iframe=true&amp;width=600&amp;height=550")
            action_links_[-1] = php_sprintf("<a href=\"%s\" class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\" data-title=\"%s\">%s</a>", esc_url(details_link_), esc_attr(php_sprintf(__("More information about %s"), name_)), esc_attr(name_), __("More Details"))
            if (not php_empty(lambda : plugin_["icons"]["svg"])):
                plugin_icon_url_ = plugin_["icons"]["svg"]
            elif (not php_empty(lambda : plugin_["icons"]["2x"])):
                plugin_icon_url_ = plugin_["icons"]["2x"]
            elif (not php_empty(lambda : plugin_["icons"]["1x"])):
                plugin_icon_url_ = plugin_["icons"]["1x"]
            else:
                plugin_icon_url_ = plugin_["icons"]["default"]
            # end if
            #// 
            #// Filters the install action links for a plugin.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $action_links An array of plugin action links. Defaults are links to Details and Install Now.
            #// @param array    $plugin       The plugin currently being listed.
            #//
            action_links_ = apply_filters("plugin_install_action_links", action_links_, plugin_)
            last_updated_timestamp_ = strtotime(plugin_["last_updated"])
            php_print("     <div class=\"plugin-card plugin-card-")
            php_print(sanitize_html_class(plugin_["slug"]))
            php_print("\">\n            ")
            if (not compatible_php_) or (not compatible_wp_):
                php_print("<div class=\"notice inline notice-error notice-alt\"><p>")
                if (not compatible_php_) and (not compatible_wp_):
                    _e("This plugin doesn&#8217;t work with your versions of WordPress and PHP.")
                    if current_user_can("update_core") and current_user_can("update_php"):
                        php_printf(" " + __("<a href=\"%1$s\">Please update WordPress</a>, and then <a href=\"%2$s\">learn more about updating PHP</a>."), self_admin_url("update-core.php"), esc_url(wp_get_update_php_url()))
                        wp_update_php_annotation("</p><p><em>", "</em>")
                    elif current_user_can("update_core"):
                        php_printf(" " + __("<a href=\"%s\">Please update WordPress</a>."), self_admin_url("update-core.php"))
                    elif current_user_can("update_php"):
                        php_printf(" " + __("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
                        wp_update_php_annotation("</p><p><em>", "</em>")
                    # end if
                elif (not compatible_wp_):
                    _e("This plugin doesn&#8217;t work with your version of WordPress.")
                    if current_user_can("update_core"):
                        php_printf(" " + __("<a href=\"%s\">Please update WordPress</a>."), self_admin_url("update-core.php"))
                    # end if
                elif (not compatible_php_):
                    _e("This plugin doesn&#8217;t work with your version of PHP.")
                    if current_user_can("update_php"):
                        php_printf(" " + __("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
                        wp_update_php_annotation("</p><p><em>", "</em>")
                    # end if
                # end if
                php_print("</p></div>")
            # end if
            php_print("""           <div class=\"plugin-card-top\">
            <div class=\"name column-name\">
            <h3>
            <a href=\"""")
            php_print(esc_url(details_link_))
            php_print("\" class=\"thickbox open-plugin-details-modal\">\n                       ")
            php_print(title_)
            php_print("                     <img src=\"")
            php_print(esc_attr(plugin_icon_url_))
            php_print("""\" class=\"plugin-icon\" alt=\"\">
            </a>
            </h3>
            </div>
            <div class=\"action-links\">
            """)
            if action_links_:
                php_print("<ul class=\"plugin-action-buttons\"><li>" + php_implode("</li><li>", action_links_) + "</li></ul>")
            # end if
            php_print("             </div>\n                <div class=\"desc column-description\">\n                   <p>")
            php_print(description_)
            php_print("</p>\n                   <p class=\"authors\">")
            php_print(author_)
            php_print("""</p>
            </div>
            </div>
            <div class=\"plugin-card-bottom\">
            <div class=\"vers column-rating\">
            """)
            wp_star_rating(Array({"rating": plugin_["rating"], "type": "percent", "number": plugin_["num_ratings"]}))
            php_print("                 <span class=\"num-ratings\" aria-hidden=\"true\">(")
            php_print(number_format_i18n(plugin_["num_ratings"]))
            php_print(""")</span>
            </div>
            <div class=\"column-updated\">
            <strong>""")
            _e("Last Updated:")
            php_print("</strong>\n                  ")
            #// translators: %s: Human-readable time difference.
            php_printf(__("%s ago"), human_time_diff(last_updated_timestamp_))
            php_print("             </div>\n                <div class=\"column-downloaded\">\n                 ")
            if plugin_["active_installs"] >= 1000000:
                active_installs_millions_ = floor(plugin_["active_installs"] / 1000000)
                active_installs_text_ = php_sprintf(_nx("%s+ Million", "%s+ Million", active_installs_millions_, "Active plugin installations"), number_format_i18n(active_installs_millions_))
            elif 0 == plugin_["active_installs"]:
                active_installs_text_ = _x("Less Than 10", "Active plugin installations")
            else:
                active_installs_text_ = number_format_i18n(plugin_["active_installs"]) + "+"
            # end if
            #// translators: %s: Number of installations.
            php_printf(__("%s Active Installations"), active_installs_text_)
            php_print("             </div>\n                <div class=\"column-compatibility\">\n                  ")
            if (not tested_wp_):
                php_print("<span class=\"compatibility-untested\">" + __("Untested with your version of WordPress") + "</span>")
            elif (not compatible_wp_):
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
        if (not php_empty(lambda : group_)):
            php_print("</div></div>")
        # end if
    # end def display_rows
# end class WP_Plugin_Install_List_Table
