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
#// List Table API: WP_Theme_Install_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying themes to install in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_Themes_List_Table
#//
class WP_Theme_Install_List_Table(WP_Themes_List_Table):
    features = Array()
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        return current_user_can("install_themes")
    # end def ajax_user_can
    #// 
    #// @global array  $tabs
    #// @global string $tab
    #// @global int    $paged
    #// @global string $type
    #// @global array  $theme_field_defaults
    #//
    def prepare_items(self):
        global PHP_REQUEST
        php_include_file(ABSPATH + "wp-admin/includes/theme-install.php", once=False)
        global tabs,tab,paged,type,theme_field_defaults
        php_check_if_defined("tabs","tab","paged","type","theme_field_defaults")
        wp_reset_vars(Array("tab"))
        search_terms = Array()
        search_string = ""
        if (not php_empty(lambda : PHP_REQUEST["s"])):
            search_string = php_strtolower(wp_unslash(PHP_REQUEST["s"]))
            search_terms = array_unique(php_array_filter(php_array_map("trim", php_explode(",", search_string))))
        # end if
        if (not php_empty(lambda : PHP_REQUEST["features"])):
            self.features = PHP_REQUEST["features"]
        # end if
        paged = self.get_pagenum()
        per_page = 36
        #// These are the tabs which are shown on the page,
        tabs = Array()
        tabs["dashboard"] = __("Search")
        if "search" == tab:
            tabs["search"] = __("Search Results")
        # end if
        tabs["upload"] = __("Upload")
        tabs["featured"] = _x("Featured", "themes")
        #// $tabs['popular']  = _x( 'Popular', 'themes' );
        tabs["new"] = _x("Latest", "themes")
        tabs["updated"] = _x("Recently Updated", "themes")
        nonmenu_tabs = Array("theme-information")
        #// Valid actions to perform which do not have a Menu item.
        #// This filter is documented in wp-admin/theme-install.php
        tabs = apply_filters("install_themes_tabs", tabs)
        #// 
        #// Filters tabs not associated with a menu item on the Install Themes screen.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $nonmenu_tabs The tabs that don't have a menu item on
        #// the Install Themes screen.
        #//
        nonmenu_tabs = apply_filters("install_themes_nonmenu_tabs", nonmenu_tabs)
        #// If a non-valid menu tab has been selected, And it's not a non-menu action.
        if php_empty(lambda : tab) or (not (php_isset(lambda : tabs[tab]))) and (not php_in_array(tab, nonmenu_tabs)):
            tab = key(tabs)
        # end if
        args = Array({"page": paged, "per_page": per_page, "fields": theme_field_defaults})
        for case in Switch(tab):
            if case("search"):
                type = wp_unslash(PHP_REQUEST["type"]) if (php_isset(lambda : PHP_REQUEST["type"])) else "term"
                for case in Switch(type):
                    if case("tag"):
                        args["tag"] = php_array_map("sanitize_key", search_terms)
                        break
                    # end if
                    if case("term"):
                        args["search"] = search_string
                        break
                    # end if
                    if case("author"):
                        args["author"] = search_string
                        break
                    # end if
                # end for
                if (not php_empty(lambda : self.features)):
                    args["tag"] = self.features
                    PHP_REQUEST["s"] = php_implode(",", self.features)
                    PHP_REQUEST["type"] = "tag"
                # end if
                add_action("install_themes_table_header", "install_theme_search_form", 10, 0)
                break
            # end if
            if case("featured"):
                pass
            # end if
            if case("new"):
                pass
            # end if
            if case("updated"):
                args["browse"] = tab
                break
            # end if
            if case():
                args = False
                break
            # end if
        # end for
        #// 
        #// Filters API request arguments for each Install Themes screen tab.
        #// 
        #// The dynamic portion of the hook name, `$tab`, refers to the theme install
        #// tabs. Default tabs are 'dashboard', 'search', 'upload', 'featured',
        #// 'new', and 'updated'.
        #// 
        #// @since 3.7.0
        #// 
        #// @param array $args An array of themes API arguments.
        #//
        args = apply_filters(str("install_themes_table_api_args_") + str(tab), args)
        if (not args):
            return
        # end if
        api = themes_api("query_themes", args)
        if is_wp_error(api):
            wp_die(api.get_error_message() + "</p> <p><a href=\"#\" onclick=\"document.location.reload(); return false;\">" + __("Try Again") + "</a>")
        # end if
        self.items = api.themes
        self.set_pagination_args(Array({"total_items": api.info["results"], "per_page": args["per_page"], "infinite_scroll": True}))
    # end def prepare_items
    #// 
    #//
    def no_items(self):
        
        _e("No themes match your request.")
    # end def no_items
    #// 
    #// @global array $tabs
    #// @global string $tab
    #// @return array
    #//
    def get_views(self):
        
        global tabs,tab
        php_check_if_defined("tabs","tab")
        display_tabs = Array()
        for action,text in tabs:
            current_link_attributes = " class=\"current\" aria-current=\"page\"" if action == tab else ""
            href = self_admin_url("theme-install.php?tab=" + action)
            display_tabs["theme-install-" + action] = str("<a href='") + str(href) + str("'") + str(current_link_attributes) + str(">") + str(text) + str("</a>")
        # end for
        return display_tabs
    # end def get_views
    #// 
    #// Displays the theme install table.
    #// 
    #// Overrides the parent display() method to provide a different container.
    #// 
    #// @since 3.1.0
    #//
    def display(self):
        
        wp_nonce_field("fetch-list-" + get_class(self), "_ajax_fetch_list_nonce")
        php_print("     <div class=\"tablenav top themes\">\n           <div class=\"alignleft actions\">\n             ")
        #// 
        #// Fires in the Install Themes list table header.
        #// 
        #// @since 2.8.0
        #//
        do_action("install_themes_table_header")
        php_print("         </div>\n            ")
        self.pagination("top")
        php_print("""           <br class=\"clear\" />
        </div>
        <div id=\"availablethemes\">
        """)
        self.display_rows_or_placeholder()
        php_print("     </div>\n\n      ")
        self.tablenav("bottom")
    # end def display
    #// 
    #//
    def display_rows(self):
        
        themes = self.items
        for theme in themes:
            php_print("             <div class=\"available-theme installable-theme\">\n             ")
            self.single_row(theme)
            php_print("             </div>\n            ")
        # end for
        #// End foreach $theme_names.
        self.theme_installer()
    # end def display_rows
    #// 
    #// Prints a theme from the WordPress.org API.
    #// 
    #// @since 3.1.0
    #// 
    #// @global array $themes_allowedtags
    #// 
    #// @param object $theme {
    #// An object that contains theme data returned by the WordPress.org API.
    #// 
    #// @type string $name           Theme name, e.g. 'Twenty Twenty'.
    #// @type string $slug           Theme slug, e.g. 'twentytwenty'.
    #// @type string $version        Theme version, e.g. '1.1'.
    #// @type string $author         Theme author username, e.g. 'melchoyce'.
    #// @type string $preview_url    Preview URL, e.g. 'http://2020.wordpress.net/'.
    #// @type string $screenshot_url Screenshot URL, e.g. 'https://wordpress.org/themes/twentytwenty/'.
    #// @type float  $rating         Rating score.
    #// @type int    $num_ratings    The number of ratings.
    #// @type string $homepage       Theme homepage, e.g. 'https://wordpress.org/themes/twentytwenty/'.
    #// @type string $description    Theme description.
    #// @type string $download_link  Theme ZIP download URL.
    #// }
    #//
    def single_row(self, theme=None):
        
        global themes_allowedtags
        php_check_if_defined("themes_allowedtags")
        if php_empty(lambda : theme):
            return
        # end if
        name = wp_kses(theme.name, themes_allowedtags)
        author = wp_kses(theme.author, themes_allowedtags)
        #// translators: %s: Theme name.
        preview_title = php_sprintf(__("Preview &#8220;%s&#8221;"), name)
        preview_url = add_query_arg(Array({"tab": "theme-information", "theme": theme.slug}), self_admin_url("theme-install.php"))
        actions = Array()
        install_url = add_query_arg(Array({"action": "install-theme", "theme": theme.slug}), self_admin_url("update.php"))
        update_url = add_query_arg(Array({"action": "upgrade-theme", "theme": theme.slug}), self_admin_url("update.php"))
        status = self._get_theme_status(theme)
        for case in Switch(status):
            if case("update_available"):
                actions[-1] = php_sprintf("<a class=\"install-now\" href=\"%s\" title=\"%s\">%s</a>", esc_url(wp_nonce_url(update_url, "upgrade-theme_" + theme.slug)), esc_attr(php_sprintf(__("Update to version %s"), theme.version)), __("Update"))
                break
            # end if
            if case("newer_installed"):
                pass
            # end if
            if case("latest_installed"):
                actions[-1] = php_sprintf("<span class=\"install-now\" title=\"%s\">%s</span>", esc_attr__("This theme is already installed and is up to date"), _x("Installed", "theme"))
                break
            # end if
            if case("install"):
                pass
            # end if
            if case():
                actions[-1] = php_sprintf("<a class=\"install-now\" href=\"%s\" title=\"%s\">%s</a>", esc_url(wp_nonce_url(install_url, "install-theme_" + theme.slug)), esc_attr(php_sprintf(__("Install %s"), name)), __("Install Now"))
                break
            # end if
        # end for
        actions[-1] = php_sprintf("<a class=\"install-theme-preview\" href=\"%s\" title=\"%s\">%s</a>", esc_url(preview_url), esc_attr(php_sprintf(__("Preview %s"), name)), __("Preview"))
        #// 
        #// Filters the install action links for a theme in the Install Themes list table.
        #// 
        #// @since 3.4.0
        #// 
        #// @param string[] $actions An array of theme action links. Defaults are
        #// links to Install Now, Preview, and Details.
        #// @param WP_Theme $theme   Theme object.
        #//
        actions = apply_filters("theme_install_actions", actions, theme)
        php_print("     <a class=\"screenshot install-theme-preview\" href=\"")
        php_print(esc_url(preview_url))
        php_print("\" title=\"")
        php_print(esc_attr(preview_title))
        php_print("\">\n            <img src=\"")
        php_print(esc_url(theme.screenshot_url))
        php_print("""\" width=\"150\" alt=\"\" />
        </a>
        <h3>""")
        php_print(name)
        php_print("</h3>\n      <div class=\"theme-author\">\n      ")
        #// translators: %s: Theme author.
        printf(__("By %s"), author)
        php_print("""       </div>
        <div class=\"action-links\">
        <ul>
        """)
        for action in actions:
            php_print("                 <li>")
            php_print(action)
            php_print("</li>\n              ")
        # end for
        php_print("             <li class=\"hide-if-no-js\"><a href=\"#\" class=\"theme-detail\">")
        _e("Details")
        php_print("""</a></li>
        </ul>
        </div>
        """)
        self.install_theme_info(theme)
    # end def single_row
    #// 
    #// Prints the wrapper for the theme installer.
    #//
    def theme_installer(self):
        
        php_print("""       <div id=\"theme-installer\" class=\"wp-full-overlay expanded\">
        <div class=\"wp-full-overlay-sidebar\">
        <div class=\"wp-full-overlay-header\">
        <a href=\"#\" class=\"close-full-overlay button\">""")
        _e("Close")
        php_print("""</a>
        <span class=\"theme-install\"></span>
        </div>
        <div class=\"wp-full-overlay-sidebar-content\">
        <div class=\"install-theme-info\"></div>
        </div>
        <div class=\"wp-full-overlay-footer\">
        <button type=\"button\" class=\"collapse-sidebar button\" aria-expanded=\"true\" aria-label=\"""")
        esc_attr_e("Collapse Sidebar")
        php_print("\">\n                        <span class=\"collapse-sidebar-arrow\"></span>\n                        <span class=\"collapse-sidebar-label\">")
        _e("Collapse")
        php_print("""</span>
        </button>
        </div>
        </div>
        <div class=\"wp-full-overlay-main\"></div>
        </div>
        """)
    # end def theme_installer
    #// 
    #// Prints the wrapper for the theme installer with a provided theme's data.
    #// Used to make the theme installer work for no-js.
    #// 
    #// @param object $theme - A WordPress.org Theme API object.
    #//
    def theme_installer_single(self, theme=None):
        
        php_print("     <div id=\"theme-installer\" class=\"wp-full-overlay single-theme\">\n           <div class=\"wp-full-overlay-sidebar\">\n               ")
        self.install_theme_info(theme)
        php_print("         </div>\n            <div class=\"wp-full-overlay-main\">\n              <iframe src=\"")
        php_print(esc_url(theme.preview_url))
        php_print("""\"></iframe>
        </div>
        </div>
        """)
    # end def theme_installer_single
    #// 
    #// Prints the info for a theme (to be used in the theme installer modal).
    #// 
    #// @global array $themes_allowedtags
    #// 
    #// @param object $theme - A WordPress.org Theme API object.
    #//
    def install_theme_info(self, theme=None):
        
        global themes_allowedtags
        php_check_if_defined("themes_allowedtags")
        if php_empty(lambda : theme):
            return
        # end if
        name = wp_kses(theme.name, themes_allowedtags)
        author = wp_kses(theme.author, themes_allowedtags)
        install_url = add_query_arg(Array({"action": "install-theme", "theme": theme.slug}), self_admin_url("update.php"))
        update_url = add_query_arg(Array({"action": "upgrade-theme", "theme": theme.slug}), self_admin_url("update.php"))
        status = self._get_theme_status(theme)
        php_print("     <div class=\"install-theme-info\">\n        ")
        for case in Switch(status):
            if case("update_available"):
                printf("<a class=\"theme-install button button-primary\" href=\"%s\" title=\"%s\">%s</a>", esc_url(wp_nonce_url(update_url, "upgrade-theme_" + theme.slug)), esc_attr(php_sprintf(__("Update to version %s"), theme.version)), __("Update"))
                break
            # end if
            if case("newer_installed"):
                pass
            # end if
            if case("latest_installed"):
                printf("<span class=\"theme-install\" title=\"%s\">%s</span>", esc_attr__("This theme is already installed and is up to date"), _x("Installed", "theme"))
                break
            # end if
            if case("install"):
                pass
            # end if
            if case():
                printf("<a class=\"theme-install button button-primary\" href=\"%s\">%s</a>", esc_url(wp_nonce_url(install_url, "install-theme_" + theme.slug)), __("Install"))
                break
            # end if
        # end for
        php_print("         <h3 class=\"theme-name\">")
        php_print(name)
        php_print("</h3>\n          <span class=\"theme-by\">\n         ")
        #// translators: %s: Theme author.
        printf(__("By %s"), author)
        php_print("         </span>\n           ")
        if (php_isset(lambda : theme.screenshot_url)):
            php_print("             <img class=\"theme-screenshot\" src=\"")
            php_print(esc_url(theme.screenshot_url))
            php_print("\" alt=\"\" />\n         ")
        # end if
        php_print("         <div class=\"theme-details\">\n             ")
        wp_star_rating(Array({"rating": theme.rating, "type": "percent", "number": theme.num_ratings}))
        php_print("             <div class=\"theme-version\">\n                 <strong>")
        _e("Version:")
        php_print(" </strong>\n                 ")
        php_print(wp_kses(theme.version, themes_allowedtags))
        php_print("             </div>\n                <div class=\"theme-description\">\n                 ")
        php_print(wp_kses(theme.description, themes_allowedtags))
        php_print("             </div>\n            </div>\n            <input class=\"theme-preview-url\" type=\"hidden\" value=\"")
        php_print(esc_url(theme.preview_url))
        php_print("\" />\n      </div>\n        ")
    # end def install_theme_info
    #// 
    #// Send required variables to JavaScript land
    #// 
    #// @since 3.4.0
    #// 
    #// @global string $tab  Current tab within Themes->Install screen
    #// @global string $type Type of search.
    #// 
    #// @param array $extra_args Unused.
    #//
    def _js_vars(self, extra_args=Array()):
        
        global tab,type
        php_check_if_defined("tab","type")
        super()._js_vars(compact("tab", "type"))
    # end def _js_vars
    #// 
    #// Check to see if the theme is already installed.
    #// 
    #// @since 3.4.0
    #// 
    #// @param object $theme - A WordPress.org Theme API object.
    #// @return string Theme status.
    #//
    def _get_theme_status(self, theme=None):
        
        status = "install"
        installed_theme = wp_get_theme(theme.slug)
        if installed_theme.exists():
            if php_version_compare(installed_theme.get("Version"), theme.version, "="):
                status = "latest_installed"
            elif php_version_compare(installed_theme.get("Version"), theme.version, ">"):
                status = "newer_installed"
            else:
                status = "update_available"
            # end if
        # end if
        return status
    # end def _get_theme_status
# end class WP_Theme_Install_List_Table
