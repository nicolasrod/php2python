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
#// List Table API: WP_Themes_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying installed themes in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Themes_List_Table(WP_List_Table):
    search_terms = Array()
    features = Array()
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
        
        super().__init__(Array({"ajax": True, "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
    # end def __init__
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        
        #// Do not check edit_theme_options here. Ajax calls for available themes require switch_themes.
        return current_user_can("switch_themes")
    # end def ajax_user_can
    #// 
    #//
    def prepare_items(self):
        
        
        themes_ = wp_get_themes(Array({"allowed": True}))
        if (not php_empty(lambda : PHP_REQUEST["s"])):
            self.search_terms = array_unique(php_array_filter(php_array_map("trim", php_explode(",", php_strtolower(wp_unslash(PHP_REQUEST["s"]))))))
        # end if
        if (not php_empty(lambda : PHP_REQUEST["features"])):
            self.features = PHP_REQUEST["features"]
        # end if
        if self.search_terms or self.features:
            for key_,theme_ in themes_:
                if (not self.search_theme(theme_)):
                    themes_[key_] = None
                # end if
            # end for
        # end if
        themes_[get_option("stylesheet")] = None
        WP_Theme.sort_by_name(themes_)
        per_page_ = 36
        page_ = self.get_pagenum()
        start_ = page_ - 1 * per_page_
        self.items = php_array_slice(themes_, start_, per_page_, True)
        self.set_pagination_args(Array({"total_items": php_count(themes_), "per_page": per_page_, "infinite_scroll": True}))
    # end def prepare_items
    #// 
    #//
    def no_items(self):
        
        
        if self.search_terms or self.features:
            _e("No items found.")
            return
        # end if
        blog_id_ = get_current_blog_id()
        if is_multisite():
            if current_user_can("install_themes") and current_user_can("manage_network_themes"):
                printf(__("You only have one theme enabled for this site right now. Visit the Network Admin to <a href=\"%1$s\">enable</a> or <a href=\"%2$s\">install</a> more themes."), network_admin_url("site-themes.php?id=" + blog_id_), network_admin_url("theme-install.php"))
                return
            elif current_user_can("manage_network_themes"):
                printf(__("You only have one theme enabled for this site right now. Visit the Network Admin to <a href=\"%s\">enable</a> more themes."), network_admin_url("site-themes.php?id=" + blog_id_))
                return
            # end if
            pass
        else:
            if current_user_can("install_themes"):
                printf(__("You only have one theme installed right now. Live a little! You can choose from over 1,000 free themes in the WordPress Theme Directory at any time: just click on the <a href=\"%s\">Install Themes</a> tab above."), admin_url("theme-install.php"))
                return
            # end if
        # end if
        #// Fallthrough.
        printf(__("Only the current theme is available to you. Contact the %s administrator for information about accessing additional themes."), get_site_option("site_name"))
    # end def no_items
    #// 
    #// @param string $which
    #//
    def tablenav(self, which_="top"):
        
        
        if self.get_pagination_arg("total_pages") <= 1:
            return
        # end if
        php_print("     <div class=\"tablenav themes ")
        php_print(which_)
        php_print("\">\n            ")
        self.pagination(which_)
        php_print("""           <span class=\"spinner\"></span>
        <br class=\"clear\" />
        </div>
        """)
    # end def tablenav
    #// 
    #// Displays the themes table.
    #// 
    #// Overrides the parent display() method to provide a different container.
    #// 
    #// @since 3.1.0
    #//
    def display(self):
        
        
        wp_nonce_field("fetch-list-" + get_class(self), "_ajax_fetch_list_nonce")
        php_print("     ")
        self.tablenav("top")
        php_print("\n       <div id=\"availablethemes\">\n          ")
        self.display_rows_or_placeholder()
        php_print("     </div>\n\n      ")
        self.tablenav("bottom")
        php_print("     ")
    # end def display
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        return Array()
    # end def get_columns
    #// 
    #//
    def display_rows_or_placeholder(self):
        
        
        if self.has_items():
            self.display_rows()
        else:
            php_print("<div class=\"no-items\">")
            self.no_items()
            php_print("</div>")
        # end if
    # end def display_rows_or_placeholder
    #// 
    #//
    def display_rows(self):
        
        
        themes_ = self.items
        for theme_ in themes_:
            php_print("         <div class=\"available-theme\">\n           ")
            template_ = theme_.get_template()
            stylesheet_ = theme_.get_stylesheet()
            title_ = theme_.display("Name")
            version_ = theme_.display("Version")
            author_ = theme_.display("Author")
            activate_link_ = wp_nonce_url("themes.php?action=activate&amp;template=" + urlencode(template_) + "&amp;stylesheet=" + urlencode(stylesheet_), "switch-theme_" + stylesheet_)
            actions_ = Array()
            actions_["activate"] = php_sprintf("<a href=\"%s\" class=\"activatelink\" title=\"%s\">%s</a>", activate_link_, esc_attr(php_sprintf(__("Activate &#8220;%s&#8221;"), title_)), __("Activate"))
            if current_user_can("edit_theme_options") and current_user_can("customize"):
                actions_["preview"] += php_sprintf("<a href=\"%s\" class=\"load-customize hide-if-no-customize\">%s</a>", wp_customize_url(stylesheet_), __("Live Preview"))
            # end if
            if (not is_multisite()) and current_user_can("delete_themes"):
                actions_["delete"] = php_sprintf("<a class=\"submitdelete deletion\" href=\"%s\" onclick=\"return confirm( '%s' );\">%s</a>", wp_nonce_url("themes.php?action=delete&amp;stylesheet=" + urlencode(stylesheet_), "delete-theme_" + stylesheet_), esc_js(php_sprintf(__("You are about to delete this theme '%s'\n  'Cancel' to stop, 'OK' to delete."), title_)), __("Delete"))
            # end if
            #// This filter is documented in wp-admin/includes/class-wp-ms-themes-list-table.php
            actions_ = apply_filters("theme_action_links", actions_, theme_, "all")
            #// This filter is documented in wp-admin/includes/class-wp-ms-themes-list-table.php
            actions_ = apply_filters(str("theme_action_links_") + str(stylesheet_), actions_, theme_, "all")
            delete_action_ = "<div class=\"delete-theme\">" + actions_["delete"] + "</div>" if (php_isset(lambda : actions_["delete"])) else ""
            actions_["delete"] = None
            screenshot_ = theme_.get_screenshot()
            php_print("\n           <span class=\"screenshot hide-if-customize\">\n             ")
            if screenshot_:
                php_print("                 <img src=\"")
                php_print(esc_url(screenshot_))
                php_print("\" alt=\"\" />\n             ")
            # end if
            php_print("         </span>\n           <a href=\"")
            php_print(wp_customize_url(stylesheet_))
            php_print("\" class=\"screenshot load-customize hide-if-no-customize\">\n               ")
            if screenshot_:
                php_print("                 <img src=\"")
                php_print(esc_url(screenshot_))
                php_print("\" alt=\"\" />\n             ")
            # end if
            php_print("         </a>\n\n            <h3>")
            php_print(title_)
            php_print("</h3>\n          <div class=\"theme-author\">\n              ")
            #// translators: %s: Theme author.
            printf(__("By %s"), author_)
            php_print("""           </div>
            <div class=\"action-links\">
            <ul>
            """)
            for action_ in actions_:
                php_print("                     <li>")
                php_print(action_)
                php_print("</li>\n                  ")
            # end for
            php_print("                 <li class=\"hide-if-no-js\"><a href=\"#\" class=\"theme-detail\">")
            _e("Details")
            php_print("</a></li>\n              </ul>\n             ")
            php_print(delete_action_)
            php_print("\n               ")
            theme_update_available(theme_)
            php_print("""           </div>
            <div class=\"themedetaildiv hide-if-js\">
            <p><strong>""")
            _e("Version:")
            php_print("</strong> ")
            php_print(version_)
            php_print("</p>\n               <p>")
            php_print(theme_.display("Description"))
            php_print("</p>\n               ")
            if theme_.parent():
                printf(" <p class=\"howto\">" + __("This <a href=\"%1$s\">child theme</a> requires its parent theme, %2$s.") + "</p>", __("https://developer.wordpress.org/themes/advanced-topics/child-themes/"), theme_.parent().display("Name"))
            # end if
            php_print("""           </div>
            </div>
            """)
        # end for
    # end def display_rows
    #// 
    #// @param WP_Theme $theme
    #// @return bool
    #//
    def search_theme(self, theme_=None):
        
        
        #// Search the features.
        for word_ in self.features:
            if (not php_in_array(word_, theme_.get("Tags"))):
                return False
            # end if
        # end for
        #// Match all phrases.
        for word_ in self.search_terms:
            if php_in_array(word_, theme_.get("Tags")):
                continue
            # end if
            for header_ in Array("Name", "Description", "Author", "AuthorURI"):
                #// Don't mark up; Do translate.
                if False != php_stripos(strip_tags(theme_.display(header_, False, True)), word_):
                    continue
                # end if
            # end for
            if False != php_stripos(theme_.get_stylesheet(), word_):
                continue
            # end if
            if False != php_stripos(theme_.get_template(), word_):
                continue
            # end if
            return False
        # end for
        return True
    # end def search_theme
    #// 
    #// Send required variables to JavaScript land
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $extra_args
    #//
    def _js_vars(self, extra_args_=None):
        if extra_args_ is None:
            extra_args_ = Array()
        # end if
        
        search_string_ = esc_attr(wp_unslash(PHP_REQUEST["s"])) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        args_ = Array({"search": search_string_, "features": self.features, "paged": self.get_pagenum(), "total_pages": self._pagination_args["total_pages"] if (not php_empty(lambda : self._pagination_args["total_pages"])) else 1})
        if php_is_array(extra_args_):
            args_ = php_array_merge(args_, extra_args_)
        # end if
        printf("<script type='text/javascript'>var theme_list_args = %s;</script>\n", wp_json_encode(args_))
        super()._js_vars()
    # end def _js_vars
# end class WP_Themes_List_Table
