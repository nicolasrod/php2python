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
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        global status_
        global page_
        php_check_if_defined("status_","page_")
        super().__init__(Array({"plural": "themes", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
        status_ = PHP_REQUEST["theme_status"] if (php_isset(lambda : PHP_REQUEST["theme_status"])) else "all"
        if (not php_in_array(status_, Array("all", "enabled", "disabled", "upgrade", "search", "broken"))):
            status_ = "all"
        # end if
        page_ = self.get_pagenum()
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
        
        
        global status_
        global totals_
        global page_
        global orderby_
        global order_
        global s_
        php_check_if_defined("status_","totals_","page_","orderby_","order_","s_")
        wp_reset_vars(Array("orderby", "order", "s"))
        themes_ = Array({"all": apply_filters("all_themes", wp_get_themes()), "search": Array(), "enabled": Array(), "disabled": Array(), "upgrade": Array(), "broken": Array() if self.is_site_themes else wp_get_themes(Array({"errors": True}))})
        if self.is_site_themes:
            themes_per_page_ = self.get_items_per_page("site_themes_network_per_page")
            allowed_where_ = "site"
        else:
            themes_per_page_ = self.get_items_per_page("themes_network_per_page")
            allowed_where_ = "network"
        # end if
        current_ = get_site_transient("update_themes")
        maybe_update_ = current_user_can("update_themes") and (not self.is_site_themes) and current_
        for key_,theme_ in themes_["all"].items():
            if self.is_site_themes and theme_.is_allowed("network"):
                themes_["all"][key_] = None
                continue
            # end if
            if maybe_update_ and (php_isset(lambda : current_.response[key_])):
                themes_["all"][key_].update = True
                themes_["upgrade"][key_] = themes_["all"][key_]
            # end if
            filter_ = "enabled" if theme_.is_allowed(allowed_where_, self.site_id) else "disabled"
            themes_[filter_][key_] = themes_["all"][key_]
        # end for
        if s_:
            status_ = "search"
            themes_["search"] = php_array_filter(php_array_merge(themes_["all"], themes_["broken"]), Array(self, "_search_callback"))
        # end if
        totals_ = Array()
        for type_,list_ in themes_.items():
            totals_[type_] = php_count(list_)
        # end for
        if php_empty(lambda : themes_[status_]) and (not php_in_array(status_, Array("all", "search"))):
            status_ = "all"
        # end if
        self.items = themes_[status_]
        WP_Theme.sort_by_name(self.items)
        self.has_items = (not php_empty(lambda : themes_["all"]))
        total_this_page_ = totals_[status_]
        wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"themes": totals_, "totals": wp_get_update_data()}))
        if orderby_:
            orderby_ = ucfirst(orderby_)
            order_ = php_strtoupper(order_)
            if "Name" == orderby_:
                if "ASC" == order_:
                    self.items = php_array_reverse(self.items)
                # end if
            else:
                uasort(self.items, Array(self, "_order_callback"))
            # end if
        # end if
        start_ = page_ - 1 * themes_per_page_
        if total_this_page_ > themes_per_page_:
            self.items = php_array_slice(self.items, start_, themes_per_page_, True)
        # end if
        self.set_pagination_args(Array({"total_items": total_this_page_, "per_page": themes_per_page_}))
    # end def prepare_items
    #// 
    #// @staticvar string $term
    #// @param WP_Theme $theme
    #// @return bool
    #//
    def _search_callback(self, theme_=None):
        
        
        term_ = None
        if php_is_null(term_):
            term_ = wp_unslash(PHP_REQUEST["s"])
        # end if
        for field_ in Array("Name", "Description", "Author", "Author", "AuthorURI"):
            #// Don't mark up; Do translate.
            if False != php_stripos(theme_.display(field_, False, True), term_):
                return True
            # end if
        # end for
        if False != php_stripos(theme_.get_stylesheet(), term_):
            return True
        # end if
        if False != php_stripos(theme_.get_template(), term_):
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
    def _order_callback(self, theme_a_=None, theme_b_=None):
        
        
        global orderby_
        global order_
        php_check_if_defined("orderby_","order_")
        a_ = theme_a_[orderby_]
        b_ = theme_b_[orderby_]
        if a_ == b_:
            return 0
        # end if
        if "DESC" == order_:
            return 1 if a_ < b_ else -1
        else:
            return -1 if a_ < b_ else 1
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
        
        
        global totals_
        global status_
        php_check_if_defined("totals_","status_")
        status_links_ = Array()
        for type_,count_ in totals_.items():
            if (not count_):
                continue
            # end if
            for case in Switch(type_):
                if case("all"):
                    #// translators: %s: Number of themes.
                    text_ = _nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", count_, "themes")
                    break
                # end if
                if case("enabled"):
                    #// translators: %s: Number of themes.
                    text_ = _nx("Enabled <span class=\"count\">(%s)</span>", "Enabled <span class=\"count\">(%s)</span>", count_, "themes")
                    break
                # end if
                if case("disabled"):
                    #// translators: %s: Number of themes.
                    text_ = _nx("Disabled <span class=\"count\">(%s)</span>", "Disabled <span class=\"count\">(%s)</span>", count_, "themes")
                    break
                # end if
                if case("upgrade"):
                    #// translators: %s: Number of themes.
                    text_ = _nx("Update Available <span class=\"count\">(%s)</span>", "Update Available <span class=\"count\">(%s)</span>", count_, "themes")
                    break
                # end if
                if case("broken"):
                    #// translators: %s: Number of themes.
                    text_ = _nx("Broken <span class=\"count\">(%s)</span>", "Broken <span class=\"count\">(%s)</span>", count_, "themes")
                    break
                # end if
            # end for
            if self.is_site_themes:
                url_ = "site-themes.php?id=" + self.site_id
            else:
                url_ = "themes.php"
            # end if
            if "search" != type_:
                status_links_[type_] = php_sprintf("<a href='%s'%s>%s</a>", esc_url(add_query_arg("theme_status", type_, url_)), " class=\"current\" aria-current=\"page\"" if type_ == status_ else "", php_sprintf(text_, number_format_i18n(count_)))
            # end if
        # end for
        return status_links_
    # end def get_views
    #// 
    #// @global string $status
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        global status_
        php_check_if_defined("status_")
        actions_ = Array()
        if "enabled" != status_:
            actions_["enable-selected"] = __("Enable") if self.is_site_themes else __("Network Enable")
        # end if
        if "disabled" != status_:
            actions_["disable-selected"] = __("Disable") if self.is_site_themes else __("Network Disable")
        # end if
        if (not self.is_site_themes):
            if current_user_can("update_themes"):
                actions_["update-selected"] = __("Update")
            # end if
            if current_user_can("delete_themes"):
                actions_["delete-selected"] = __("Delete")
            # end if
        # end if
        return actions_
    # end def get_bulk_actions
    #// 
    #//
    def display_rows(self):
        
        
        for theme_ in self.items:
            self.single_row(theme_)
        # end for
    # end def display_rows
    #// 
    #// Handles the checkbox column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Theme $theme The current WP_Theme object.
    #//
    def column_cb(self, theme_=None):
        
        
        checkbox_id_ = "checkbox_" + php_md5(theme_.get("Name"))
        php_print("     <input type=\"checkbox\" name=\"checked[]\" value=\"")
        php_print(esc_attr(theme_.get_stylesheet()))
        php_print("\" id=\"")
        php_print(checkbox_id_)
        php_print("\" />\n      <label class=\"screen-reader-text\" for=\"")
        php_print(checkbox_id_)
        php_print("\" >")
        _e("Select")
        php_print("  ")
        php_print(theme_.display("Name"))
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
    def column_name(self, theme_=None):
        
        
        global status_
        global page_
        global s_
        php_check_if_defined("status_","page_","s_")
        context_ = status_
        if self.is_site_themes:
            url_ = str("site-themes.php?id=") + str(self.site_id) + str("&amp;")
            allowed_ = theme_.is_allowed("site", self.site_id)
        else:
            url_ = "themes.php?"
            allowed_ = theme_.is_allowed("network")
        # end if
        #// Pre-order.
        actions_ = Array({"enable": "", "disable": "", "delete": ""})
        stylesheet_ = theme_.get_stylesheet()
        theme_key_ = urlencode(stylesheet_)
        if (not allowed_):
            if (not theme_.errors()):
                url_ = add_query_arg(Array({"action": "enable", "theme": theme_key_, "paged": page_, "s": s_}), url_)
                if self.is_site_themes:
                    #// translators: %s: Theme name.
                    aria_label_ = php_sprintf(__("Enable %s"), theme_.display("Name"))
                else:
                    #// translators: %s: Theme name.
                    aria_label_ = php_sprintf(__("Network Enable %s"), theme_.display("Name"))
                # end if
                actions_["enable"] = php_sprintf("<a href=\"%s\" class=\"edit\" aria-label=\"%s\">%s</a>", esc_url(wp_nonce_url(url_, "enable-theme_" + stylesheet_)), esc_attr(aria_label_), __("Enable") if self.is_site_themes else __("Network Enable"))
            # end if
        else:
            url_ = add_query_arg(Array({"action": "disable", "theme": theme_key_, "paged": page_, "s": s_}), url_)
            if self.is_site_themes:
                #// translators: %s: Theme name.
                aria_label_ = php_sprintf(__("Disable %s"), theme_.display("Name"))
            else:
                #// translators: %s: Theme name.
                aria_label_ = php_sprintf(__("Network Disable %s"), theme_.display("Name"))
            # end if
            actions_["disable"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(wp_nonce_url(url_, "disable-theme_" + stylesheet_)), esc_attr(aria_label_), __("Disable") if self.is_site_themes else __("Network Disable"))
        # end if
        if (not allowed_) and current_user_can("delete_themes") and (not self.is_site_themes) and get_option("stylesheet") != stylesheet_ and get_option("template") != stylesheet_:
            url_ = add_query_arg(Array({"action": "delete-selected", "checked[]": theme_key_, "theme_status": context_, "paged": page_, "s": s_}), "themes.php")
            #// translators: %s: Theme name.
            aria_label_ = php_sprintf(_x("Delete %s", "theme"), theme_.display("Name"))
            actions_["delete"] = php_sprintf("<a href=\"%s\" class=\"delete\" aria-label=\"%s\">%s</a>", esc_url(wp_nonce_url(url_, "bulk-themes")), esc_attr(aria_label_), __("Delete"))
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
        actions_ = apply_filters("theme_action_links", php_array_filter(actions_), theme_, context_)
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
        actions_ = apply_filters(str("theme_action_links_") + str(stylesheet_), actions_, theme_, context_)
        php_print(self.row_actions(actions_, True))
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
    def column_description(self, theme_=None):
        
        
        global status_
        global totals_
        php_check_if_defined("status_","totals_")
        if theme_.errors():
            pre_ = __("Broken Theme:") + " " if "broken" == status_ else ""
            php_print("<p><strong class=\"error-message\">" + pre_ + theme_.errors().get_error_message() + "</strong></p>")
        # end if
        if self.is_site_themes:
            allowed_ = theme_.is_allowed("site", self.site_id)
        else:
            allowed_ = theme_.is_allowed("network")
        # end if
        class_ = "inactive" if (not allowed_) else "active"
        if (not php_empty(lambda : totals_["upgrade"])) and (not php_empty(lambda : theme_.update)):
            class_ += " update"
        # end if
        php_print("<div class='theme-description'><p>" + theme_.display("Description") + str("</p></div>\n          <div class='") + str(class_) + str(" second theme-version-author-uri'>"))
        stylesheet_ = theme_.get_stylesheet()
        theme_meta_ = Array()
        if theme_.get("Version"):
            #// translators: %s: Theme version.
            theme_meta_[-1] = php_sprintf(__("Version %s"), theme_.display("Version"))
        # end if
        #// translators: %s: Theme author.
        theme_meta_[-1] = php_sprintf(__("By %s"), theme_.display("Author"))
        if theme_.get("ThemeURI"):
            #// translators: %s: Theme name.
            aria_label_ = php_sprintf(__("Visit %s homepage"), theme_.display("Name"))
            theme_meta_[-1] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", theme_.display("ThemeURI"), esc_attr(aria_label_), __("Visit Theme Site"))
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
        theme_meta_ = apply_filters("theme_row_meta", theme_meta_, stylesheet_, theme_, status_)
        php_print(php_implode(" | ", theme_meta_))
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
    def column_default(self, theme_=None, column_name_=None):
        
        
        stylesheet_ = theme_.get_stylesheet()
        #// 
        #// Fires inside each custom column of the Multisite themes list table.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string   $column_name Name of the column.
        #// @param string   $stylesheet  Directory name of the theme.
        #// @param WP_Theme $theme       Current WP_Theme object.
        #//
        do_action("manage_themes_custom_column", column_name_, stylesheet_, theme_)
    # end def column_default
    #// 
    #// Handles the output for a single table row.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Theme $item The current WP_Theme object.
    #//
    def single_row_columns(self, item_=None):
        
        
        columns_, hidden_, sortable_, primary_ = self.get_column_info()
        for column_name_,column_display_name_ in columns_.items():
            extra_classes_ = ""
            if php_in_array(column_name_, hidden_):
                extra_classes_ += " hidden"
            # end if
            for case in Switch(column_name_):
                if case("cb"):
                    php_print("<th scope=\"row\" class=\"check-column\">")
                    self.column_cb(item_)
                    php_print("</th>")
                    break
                # end if
                if case("name"):
                    active_theme_label_ = ""
                    #// The presence of the site_id property means that this is a subsite view and a label for the active theme needs to be added
                    if (not php_empty(lambda : self.site_id)):
                        stylesheet_ = get_blog_option(self.site_id, "stylesheet")
                        template_ = get_blog_option(self.site_id, "template")
                        #// Add a label for the active template
                        if item_.get_template() == template_:
                            active_theme_label_ = " &mdash; " + __("Active Theme")
                        # end if
                        #// In case this is a child theme, label it properly
                        if stylesheet_ != template_ and item_.get_stylesheet() == stylesheet_:
                            active_theme_label_ = " &mdash; " + __("Active Child Theme")
                        # end if
                    # end if
                    php_print(str("<td class='theme-title column-primary") + str(extra_classes_) + str("'><strong>") + item_.display("Name") + active_theme_label_ + "</strong>")
                    self.column_name(item_)
                    php_print("</td>")
                    break
                # end if
                if case("description"):
                    php_print(str("<td class='column-description desc") + str(extra_classes_) + str("'>"))
                    self.column_description(item_)
                    php_print("</td>")
                    break
                # end if
                if case():
                    php_print(str("<td class='") + str(column_name_) + str(" column-") + str(column_name_) + str(extra_classes_) + str("'>"))
                    self.column_default(item_, column_name_)
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
    def single_row(self, theme_=None):
        
        
        global status_
        global totals_
        php_check_if_defined("status_","totals_")
        if self.is_site_themes:
            allowed_ = theme_.is_allowed("site", self.site_id)
        else:
            allowed_ = theme_.is_allowed("network")
        # end if
        stylesheet_ = theme_.get_stylesheet()
        class_ = "inactive" if (not allowed_) else "active"
        if (not php_empty(lambda : totals_["upgrade"])) and (not php_empty(lambda : theme_.update)):
            class_ += " update"
        # end if
        php_printf("<tr class=\"%s\" data-slug=\"%s\">", esc_attr(class_), esc_attr(stylesheet_))
        self.single_row_columns(theme_)
        php_print("</tr>")
        if self.is_site_themes:
            remove_action(str("after_theme_row_") + str(stylesheet_), "wp_theme_update_row")
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
        do_action("after_theme_row", stylesheet_, theme_, status_)
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
        do_action(str("after_theme_row_") + str(stylesheet_), stylesheet_, theme_, status_)
    # end def single_row
# end class WP_MS_Themes_List_Table
