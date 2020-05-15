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
#// List Table API: WP_MS_Themes_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying themes in a list table for the network admin.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_MS_Themes_List_Table(WP_List_Table):
    site_id = Array()
    is_site_themes = Array()
    has_items = Array()
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
        
        global status,page
        php_check_if_defined("status","page")
        super().__init__(Array({"plural": "themes", "screen": args["screen"] if (php_isset(lambda : args["screen"])) else None}))
        status = PHP_REQUEST["theme_status"] if (php_isset(lambda : PHP_REQUEST["theme_status"])) else "all"
        if (not php_in_array(status, Array("all", "enabled", "disabled", "upgrade", "search", "broken"))):
            status = "all"
        # end if
        page = self.get_pagenum()
        self.is_site_themes = True if "site-themes-network" == self.screen.id else False
        if self.is_site_themes:
            self.site_id = php_intval(PHP_REQUEST["id"]) if (php_isset(lambda : PHP_REQUEST["id"])) else 0
        # end if
    # end def __init__
    #// 
    #// @return array
    #//
    def get_table_classes(self):
        
        #// @todo Remove and add CSS for .themes.
        return Array("widefat", "plugins")
    # end def get_table_classes
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        if self.is_site_themes:
            return current_user_can("manage_sites")
        else:
            return current_user_can("manage_network_themes")
        # end if
    # end def ajax_user_can
    #// 
    #// @global string $status
    #// @global array $totals
    #// @global int $page
    #// @global string $orderby
    #// @global string $order
    #// @global string $s
    #//
    def prepare_items(self):
        
        global status,totals,page,orderby,order,s
        php_check_if_defined("status","totals","page","orderby","order","s")
        wp_reset_vars(Array("orderby", "order", "s"))
        themes = Array({"all": apply_filters("all_themes", wp_get_themes()), "search": Array(), "enabled": Array(), "disabled": Array(), "upgrade": Array(), "broken": Array() if self.is_site_themes else wp_get_themes(Array({"errors": True}))})
        if self.is_site_themes:
            themes_per_page = self.get_items_per_page("site_themes_network_per_page")
            allowed_where = "site"
        else:
            themes_per_page = self.get_items_per_page("themes_network_per_page")
            allowed_where = "network"
        # end if
        current = get_site_transient("update_themes")
        maybe_update = current_user_can("update_themes") and (not self.is_site_themes) and current
        for key,theme in themes["all"]:
            if self.is_site_themes and theme.is_allowed("network"):
                themes["all"][key] = None
                continue
            # end if
            if maybe_update and (php_isset(lambda : current.response[key])):
                themes["all"][key].update = True
                themes["upgrade"][key] = themes["all"][key]
            # end if
            filter = "enabled" if theme.is_allowed(allowed_where, self.site_id) else "disabled"
            themes[filter][key] = themes["all"][key]
        # end for
        if s:
            status = "search"
            themes["search"] = php_array_filter(php_array_merge(themes["all"], themes["broken"]), Array(self, "_search_callback"))
        # end if
        totals = Array()
        for type,list in themes:
            totals[type] = php_count(list)
        # end for
        if php_empty(lambda : themes[status]) and (not php_in_array(status, Array("all", "search"))):
            status = "all"
        # end if
        self.items = themes[status]
        WP_Theme.sort_by_name(self.items)
        self.has_items = (not php_empty(lambda : themes["all"]))
        total_this_page = totals[status]
        wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"themes": totals, "totals": wp_get_update_data()}))
        if orderby:
            orderby = ucfirst(orderby)
            order = php_strtoupper(order)
            if "Name" == orderby:
                if "ASC" == order:
                    self.items = array_reverse(self.items)
                # end if
            else:
                uasort(self.items, Array(self, "_order_callback"))
            # end if
        # end if
        start = page - 1 * themes_per_page
        if total_this_page > themes_per_page:
            self.items = php_array_slice(self.items, start, themes_per_page, True)
        # end if
        self.set_pagination_args(Array({"total_items": total_this_page, "per_page": themes_per_page}))
    # end def prepare_items
    #// 
    #// @staticvar string $term
    #// @param WP_Theme $theme
    #// @return bool
    #//
    def _search_callback(self, theme=None):
        
        term = None
        if php_is_null(term):
            term = wp_unslash(PHP_REQUEST["s"])
        # end if
        for field in Array("Name", "Description", "Author", "Author", "AuthorURI"):
            #// Don't mark up; Do translate.
            if False != php_stripos(theme.display(field, False, True), term):
                return True
            # end if
        # end for
        if False != php_stripos(theme.get_stylesheet(), term):
            return True
        # end if
        if False != php_stripos(theme.get_template(), term):
            return True
        # end if
        return False
    # end def _search_callback
    #// Not used by any core columns.
    #// 
    #// @global string $orderby
    #// @global string $order
    #// @param array $theme_a
    #// @param array $theme_b
    #// @return int
    #//
    def _order_callback(self, theme_a=None, theme_b=None):
        
        global orderby,order
        php_check_if_defined("orderby","order")
        a = theme_a[orderby]
        b = theme_b[orderby]
        if a == b:
            return 0
        # end if
        if "DESC" == order:
            return 1 if a < b else -1
        else:
            return -1 if a < b else 1
        # end if
    # end def _order_callback
    #// 
    #//
    def no_items(self):
        
        if self.has_items:
            _e("No themes found.")
        else:
            _e("You do not appear to have any themes available at this time.")
        # end if
    # end def no_items
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        return Array({"cb": "<input type=\"checkbox\" />", "name": __("Theme"), "description": __("Description")})
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        return Array({"name": "name"})
    # end def get_sortable_columns
    #// 
    #// Gets the name of the primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Unalterable name of the primary column name, in this case, 'name'.
    #//
    def get_primary_column_name(self):
        
        return "name"
    # end def get_primary_column_name
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
                    #// translators: %s: Number of themes.
                    text = _nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", count, "themes")
                    break
                # end if
                if case("enabled"):
                    #// translators: %s: Number of themes.
                    text = _nx("Enabled <span class=\"count\">(%s)</span>", "Enabled <span class=\"count\">(%s)</span>", count, "themes")
                    break
                # end if
                if case("disabled"):
                    #// translators: %s: Number of themes.
                    text = _nx("Disabled <span class=\"count\">(%s)</span>", "Disabled <span class=\"count\">(%s)</span>", count, "themes")
                    break
                # end if
                if case("upgrade"):
                    #// translators: %s: Number of themes.
                    text = _nx("Update Available <span class=\"count\">(%s)</span>", "Update Available <span class=\"count\">(%s)</span>", count, "themes")
                    break
                # end if
                if case("broken"):
                    #// translators: %s: Number of themes.
                    text = _nx("Broken <span class=\"count\">(%s)</span>", "Broken <span class=\"count\">(%s)</span>", count, "themes")
                    break
                # end if
            # end for
            if self.is_site_themes:
                url = "site-themes.php?id=" + self.site_id
            else:
                url = "themes.php"
            # end if
            if "search" != type:
                status_links[type] = php_sprintf("<a href='%s'%s>%s</a>", esc_url(add_query_arg("theme_status", type, url)), " class=\"current\" aria-current=\"page\"" if type == status else "", php_sprintf(text, number_format_i18n(count)))
            # end if
        # end for
        return status_links
    # end def get_views
    #// 
    #// @global string $status
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        global status
        php_check_if_defined("status")
        actions = Array()
        if "enabled" != status:
            actions["enable-selected"] = __("Enable") if self.is_site_themes else __("Network Enable")
        # end if
        if "disabled" != status:
            actions["disable-selected"] = __("Disable") if self.is_site_themes else __("Network Disable")
        # end if
        if (not self.is_site_themes):
            if current_user_can("update_themes"):
                actions["update-selected"] = __("Update")
            # end if
            if current_user_can("delete_themes"):
                actions["delete-selected"] = __("Delete")
            # end if
        # end if
        return actions
    # end def get_bulk_actions
    #// 
    #//
    def display_rows(self):
        
        for theme in self.items:
            self.single_row(theme)
        # end for
    # end def display_rows
    #// 
    #// Handles the checkbox column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Theme $theme The current WP_Theme object.
    #//
    def column_cb(self, theme=None):
        
        checkbox_id = "checkbox_" + php_md5(theme.get("Name"))
        php_print("     <input type=\"checkbox\" name=\"checked[]\" value=\"")
        php_print(esc_attr(theme.get_stylesheet()))
        php_print("\" id=\"")
        php_print(checkbox_id)
        php_print("\" />\n      <label class=\"screen-reader-text\" for=\"")
        php_print(checkbox_id)
        php_print("\" >")
        _e("Select")
        php_print("  ")
        php_print(theme.display("Name"))
        php_print("</label>\n       ")
    # end def column_cb
    #// 
    #// Handles the name column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $status
    #// @global int    $page
    #// @global string $s
    #// 
    #// @param WP_Theme $theme The current WP_Theme object.
    #//
    def column_name(self, theme=None):
        
        global status,page,s
        php_check_if_defined("status","page","s")
        context = status
        if self.is_site_themes:
            url = str("site-themes.php?id=") + str(self.site_id) + str("&amp;")
            allowed = theme.is_allowed("site", self.site_id)
        else:
            url = "themes.php?"
            allowed = theme.is_allowed("network")
        # end if
        #// Pre-order.
        actions = Array({"enable": "", "disable": "", "delete": ""})
        stylesheet = theme.get_stylesheet()
        theme_key = urlencode(stylesheet)
        if (not allowed):
            if (not theme.errors()):
                url = add_query_arg(Array({"action": "enable", "theme": theme_key, "paged": page, "s": s}), url)
                if self.is_site_themes:
                    #// translators: %s: Theme name.
                    aria_label = php_sprintf(__("Enable %s"), theme.display("Name"))
                else:
                    #// translators: %s: Theme name.
                    aria_label = php_sprintf(__("Network Enable %s"), theme.display("Name"))
                # end if
                actions["enable"] = php_sprintf("<a href=\"%s\" class=\"edit\" aria-label=\"%s\">%s</a>", esc_url(wp_nonce_url(url, "enable-theme_" + stylesheet)), esc_attr(aria_label), __("Enable") if self.is_site_themes else __("Network Enable"))
            # end if
        else:
            url = add_query_arg(Array({"action": "disable", "theme": theme_key, "paged": page, "s": s}), url)
            if self.is_site_themes:
                #// translators: %s: Theme name.
                aria_label = php_sprintf(__("Disable %s"), theme.display("Name"))
            else:
                #// translators: %s: Theme name.
                aria_label = php_sprintf(__("Network Disable %s"), theme.display("Name"))
            # end if
            actions["disable"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(wp_nonce_url(url, "disable-theme_" + stylesheet)), esc_attr(aria_label), __("Disable") if self.is_site_themes else __("Network Disable"))
        # end if
        if (not allowed) and current_user_can("delete_themes") and (not self.is_site_themes) and get_option("stylesheet") != stylesheet and get_option("template") != stylesheet:
            url = add_query_arg(Array({"action": "delete-selected", "checked[]": theme_key, "theme_status": context, "paged": page, "s": s}), "themes.php")
            #// translators: %s: Theme name.
            aria_label = php_sprintf(_x("Delete %s", "theme"), theme.display("Name"))
            actions["delete"] = php_sprintf("<a href=\"%s\" class=\"delete\" aria-label=\"%s\">%s</a>", esc_url(wp_nonce_url(url, "bulk-themes")), esc_attr(aria_label), __("Delete"))
        # end if
        #// 
        #// Filters the action links displayed for each theme in the Multisite
        #// themes list table.
        #// 
        #// The action links displayed are determined by the theme's status, and
        #// which Multisite themes list table is being displayed - the Network
        #// themes list table (themes.php), which displays all installed themes,
        #// or the Site themes list table (site-themes.php), which displays the
        #// non-network enabled themes when editing a site in the Network admin.
        #// 
        #// The default action links for the Network themes list table include
        #// 'Network Enable', 'Network Disable', and 'Delete'.
        #// 
        #// The default action links for the Site themes list table include
        #// 'Enable', and 'Disable'.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $actions An array of action links.
        #// @param WP_Theme $theme   The current WP_Theme object.
        #// @param string   $context Status of the theme, one of 'all', 'enabled', or 'disabled'.
        #//
        actions = apply_filters("theme_action_links", php_array_filter(actions), theme, context)
        #// 
        #// Filters the action links of a specific theme in the Multisite themes
        #// list table.
        #// 
        #// The dynamic portion of the hook name, `$stylesheet`, refers to the
        #// directory name of the theme, which in most cases is synonymous
        #// with the template name.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[] $actions An array of action links.
        #// @param WP_Theme $theme   The current WP_Theme object.
        #// @param string   $context Status of the theme, one of 'all', 'enabled', or 'disabled'.
        #//
        actions = apply_filters(str("theme_action_links_") + str(stylesheet), actions, theme, context)
        php_print(self.row_actions(actions, True))
    # end def column_name
    #// 
    #// Handles the description column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $status
    #// @global array  $totals
    #// 
    #// @param WP_Theme $theme The current WP_Theme object.
    #//
    def column_description(self, theme=None):
        
        global status,totals
        php_check_if_defined("status","totals")
        if theme.errors():
            pre = __("Broken Theme:") + " " if "broken" == status else ""
            php_print("<p><strong class=\"error-message\">" + pre + theme.errors().get_error_message() + "</strong></p>")
        # end if
        if self.is_site_themes:
            allowed = theme.is_allowed("site", self.site_id)
        else:
            allowed = theme.is_allowed("network")
        # end if
        class_ = "inactive" if (not allowed) else "active"
        if (not php_empty(lambda : totals["upgrade"])) and (not php_empty(lambda : theme.update)):
            class_ += " update"
        # end if
        php_print("<div class='theme-description'><p>" + theme.display("Description") + str("</p></div>\n           <div class='") + str(class_) + str(" second theme-version-author-uri'>"))
        stylesheet = theme.get_stylesheet()
        theme_meta = Array()
        if theme.get("Version"):
            #// translators: %s: Theme version.
            theme_meta[-1] = php_sprintf(__("Version %s"), theme.display("Version"))
        # end if
        #// translators: %s: Theme author.
        theme_meta[-1] = php_sprintf(__("By %s"), theme.display("Author"))
        if theme.get("ThemeURI"):
            #// translators: %s: Theme name.
            aria_label = php_sprintf(__("Visit %s homepage"), theme.display("Name"))
            theme_meta[-1] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", theme.display("ThemeURI"), esc_attr(aria_label), __("Visit Theme Site"))
        # end if
        #// 
        #// Filters the array of row meta for each theme in the Multisite themes
        #// list table.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[] $theme_meta An array of the theme's metadata,
        #// including the version, author, and
        #// theme URI.
        #// @param string   $stylesheet Directory name of the theme.
        #// @param WP_Theme $theme      WP_Theme object.
        #// @param string   $status     Status of the theme.
        #//
        theme_meta = apply_filters("theme_row_meta", theme_meta, stylesheet, theme, status)
        php_print(php_implode(" | ", theme_meta))
        php_print("</div>")
    # end def column_description
    #// 
    #// Handles default column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Theme $theme       The current WP_Theme object.
    #// @param string   $column_name The current column name.
    #//
    def column_default(self, theme=None, column_name=None):
        
        stylesheet = theme.get_stylesheet()
        #// 
        #// Fires inside each custom column of the Multisite themes list table.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string   $column_name Name of the column.
        #// @param string   $stylesheet  Directory name of the theme.
        #// @param WP_Theme $theme       Current WP_Theme object.
        #//
        do_action("manage_themes_custom_column", column_name, stylesheet, theme)
    # end def column_default
    #// 
    #// Handles the output for a single table row.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Theme $item The current WP_Theme object.
    #//
    def single_row_columns(self, item=None):
        
        columns, hidden, sortable, primary = self.get_column_info()
        for column_name,column_display_name in columns:
            extra_classes = ""
            if php_in_array(column_name, hidden):
                extra_classes += " hidden"
            # end if
            for case in Switch(column_name):
                if case("cb"):
                    php_print("<th scope=\"row\" class=\"check-column\">")
                    self.column_cb(item)
                    php_print("</th>")
                    break
                # end if
                if case("name"):
                    active_theme_label = ""
                    #// The presence of the site_id property means that this is a subsite view and a label for the active theme needs to be added
                    if (not php_empty(lambda : self.site_id)):
                        stylesheet = get_blog_option(self.site_id, "stylesheet")
                        template = get_blog_option(self.site_id, "template")
                        #// Add a label for the active template
                        if item.get_template() == template:
                            active_theme_label = " &mdash; " + __("Active Theme")
                        # end if
                        #// In case this is a child theme, label it properly
                        if stylesheet != template and item.get_stylesheet() == stylesheet:
                            active_theme_label = " &mdash; " + __("Active Child Theme")
                        # end if
                    # end if
                    php_print(str("<td class='theme-title column-primary") + str(extra_classes) + str("'><strong>") + item.display("Name") + active_theme_label + "</strong>")
                    self.column_name(item)
                    php_print("</td>")
                    break
                # end if
                if case("description"):
                    php_print(str("<td class='column-description desc") + str(extra_classes) + str("'>"))
                    self.column_description(item)
                    php_print("</td>")
                    break
                # end if
                if case():
                    php_print(str("<td class='") + str(column_name) + str(" column-") + str(column_name) + str(extra_classes) + str("'>"))
                    self.column_default(item, column_name)
                    php_print("</td>")
                    break
                # end if
            # end for
        # end for
    # end def single_row_columns
    #// 
    #// @global string $status
    #// @global array  $totals
    #// 
    #// @param WP_Theme $theme
    #//
    def single_row(self, theme=None):
        
        global status,totals
        php_check_if_defined("status","totals")
        if self.is_site_themes:
            allowed = theme.is_allowed("site", self.site_id)
        else:
            allowed = theme.is_allowed("network")
        # end if
        stylesheet = theme.get_stylesheet()
        class_ = "inactive" if (not allowed) else "active"
        if (not php_empty(lambda : totals["upgrade"])) and (not php_empty(lambda : theme.update)):
            class_ += " update"
        # end if
        printf("<tr class=\"%s\" data-slug=\"%s\">", esc_attr(class_), esc_attr(stylesheet))
        self.single_row_columns(theme)
        php_print("</tr>")
        if self.is_site_themes:
            remove_action(str("after_theme_row_") + str(stylesheet), "wp_theme_update_row")
        # end if
        #// 
        #// Fires after each row in the Multisite themes list table.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string   $stylesheet Directory name of the theme.
        #// @param WP_Theme $theme      Current WP_Theme object.
        #// @param string   $status     Status of the theme.
        #//
        do_action("after_theme_row", stylesheet, theme, status)
        #// 
        #// Fires after each specific row in the Multisite themes list table.
        #// 
        #// The dynamic portion of the hook name, `$stylesheet`, refers to the
        #// directory name of the theme, most often synonymous with the template
        #// name of the theme.
        #// 
        #// @since 3.5.0
        #// 
        #// @param string   $stylesheet Directory name of the theme.
        #// @param WP_Theme $theme      Current WP_Theme object.
        #// @param string   $status     Status of the theme.
        #//
        do_action(str("after_theme_row_") + str(stylesheet), stylesheet, theme, status)
    # end def single_row
# end class WP_MS_Themes_List_Table
