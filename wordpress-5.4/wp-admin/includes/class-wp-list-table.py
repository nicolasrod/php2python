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
#// Administration API: WP_List_Table class
#// 
#// @package WordPress
#// @subpackage List_Table
#// @since 3.1.0
#// 
#// 
#// Base class for displaying a list of items in an ajaxified HTML table.
#// 
#// @since 3.1.0
#// @access private
#//
class WP_List_Table():
    #// 
    #// The current list of items.
    #// 
    #// @since 3.1.0
    #// @var array
    #//
    items = Array()
    #// 
    #// Various information about the current table.
    #// 
    #// @since 3.1.0
    #// @var array
    #//
    _args = Array()
    #// 
    #// Various information needed for displaying the pagination.
    #// 
    #// @since 3.1.0
    #// @var array
    #//
    _pagination_args = Array()
    #// 
    #// The current screen.
    #// 
    #// @since 3.1.0
    #// @var object
    #//
    screen = Array()
    #// 
    #// Cached bulk actions.
    #// 
    #// @since 3.1.0
    #// @var array
    #//
    _actions = Array()
    #// 
    #// Cached pagination output.
    #// 
    #// @since 3.1.0
    #// @var string
    #//
    _pagination = Array()
    #// 
    #// The view switcher modes.
    #// 
    #// @since 4.1.0
    #// @var array
    #//
    modes = Array()
    #// 
    #// Stores the value returned by ->get_column_info().
    #// 
    #// @since 4.1.0
    #// @var array
    #//
    _column_headers = Array()
    #// 
    #// {@internal Missing Summary}
    #// 
    #// @var array
    #//
    compat_fields = Array("_args", "_pagination_args", "screen", "_actions", "_pagination")
    #// 
    #// {@internal Missing Summary}
    #// 
    #// @var array
    #//
    compat_methods = Array("set_pagination_args", "get_views", "get_bulk_actions", "bulk_actions", "row_actions", "months_dropdown", "view_switcher", "comments_bubble", "get_items_per_page", "pagination", "get_sortable_columns", "get_column_info", "get_table_classes", "display_tablenav", "extra_tablenav", "single_row_columns")
    #// 
    #// Constructor.
    #// 
    #// The child class should call this constructor from its own constructor to override
    #// the default $args.
    #// 
    #// @since 3.1.0
    #// 
    #// @param array|string $args {
    #// Array or string of arguments.
    #// 
    #// @type string $plural   Plural value used for labels and the objects being listed.
    #// This affects things such as CSS class-names and nonces used
    #// in the list table, e.g. 'posts'. Default empty.
    #// @type string $singular Singular label for an object being listed, e.g. 'post'.
    #// Default empty
    #// @type bool   $ajax     Whether the list table supports Ajax. This includes loading
    #// and sorting data, for example. If true, the class will call
    #// the _js_vars() method in the footer to provide variables
    #// to any scripts handling Ajax events. Default false.
    #// @type string $screen   String containing the hook name used to determine the current
    #// screen. If left null, the current screen will be automatically set.
    #// Default null.
    #// }
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        args_ = wp_parse_args(args_, Array({"plural": "", "singular": "", "ajax": False, "screen": None}))
        self.screen = convert_to_screen(args_["screen"])
        add_filter(str("manage_") + str(self.screen.id) + str("_columns"), Array(self, "get_columns"), 0)
        if (not args_["plural"]):
            args_["plural"] = self.screen.base
        # end if
        args_["plural"] = sanitize_key(args_["plural"])
        args_["singular"] = sanitize_key(args_["singular"])
        self._args = args_
        if args_["ajax"]:
            #// wp_enqueue_script( 'list-table' );
            add_action("admin_footer", Array(self, "_js_vars"))
        # end if
        if php_empty(lambda : self.modes):
            self.modes = Array({"list": __("List View"), "excerpt": __("Excerpt View")})
        # end if
    # end def __init__
    #// 
    #// Make private properties readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to get.
    #// @return mixed Property.
    #//
    def __get(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return self.name_
        # end if
    # end def __get
    #// 
    #// Make private properties settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name  Property to check if set.
    #// @param mixed  $value Property value.
    #// @return mixed Newly-set property.
    #//
    def __set(self, name_=None, value_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            self.name_ = value_
            return self.name_
        # end if
    # end def __set
    #// 
    #// Make private properties checkable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to check if set.
    #// @return bool Whether the property is set.
    #//
    def __isset(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return (php_isset(lambda : self.name_))
        # end if
    # end def __isset
    #// 
    #// Make private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            self.name_ = None
        # end if
    # end def __unset
    #// 
    #// Make private/protected methods readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string   $name      Method to call.
    #// @param array    $arguments Arguments to pass when calling.
    #// @return mixed|bool Return value of the callback, false otherwise.
    #//
    def __call(self, name_=None, arguments_=None):
        
        
        if php_in_array(name_, self.compat_methods):
            return self.name_(arguments_)
        # end if
        return False
    # end def __call
    #// 
    #// Checks the current user's permissions
    #// 
    #// @since 3.1.0
    #// @abstract
    #//
    def ajax_user_can(self):
        
        
        php_print("function WP_List_Table::ajax_user_can() must be overridden in a subclass.")
        php_exit()
    # end def ajax_user_can
    #// 
    #// Prepares the list of items for displaying.
    #// 
    #// @uses WP_List_Table::set_pagination_args()
    #// 
    #// @since 3.1.0
    #// @abstract
    #//
    def prepare_items(self):
        
        
        php_print("function WP_List_Table::prepare_items() must be overridden in a subclass.")
        php_exit()
    # end def prepare_items
    #// 
    #// An internal method that sets all the necessary pagination arguments
    #// 
    #// @since 3.1.0
    #// 
    #// @param array|string $args Array or string of arguments with information about the pagination.
    #//
    def set_pagination_args(self, args_=None):
        
        
        args_ = wp_parse_args(args_, Array({"total_items": 0, "total_pages": 0, "per_page": 0}))
        if (not args_["total_pages"]) and args_["per_page"] > 0:
            args_["total_pages"] = ceil(args_["total_items"] / args_["per_page"])
        # end if
        #// Redirect if page number is invalid and headers are not already sent.
        if (not php_headers_sent()) and (not wp_doing_ajax()) and args_["total_pages"] > 0 and self.get_pagenum() > args_["total_pages"]:
            wp_redirect(add_query_arg("paged", args_["total_pages"]))
            php_exit(0)
        # end if
        self._pagination_args = args_
    # end def set_pagination_args
    #// 
    #// Access the pagination args.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $key Pagination argument to retrieve. Common values include 'total_items',
    #// 'total_pages', 'per_page', or 'infinite_scroll'.
    #// @return int Number of items that correspond to the given pagination argument.
    #//
    def get_pagination_arg(self, key_=None):
        
        
        if "page" == key_:
            return self.get_pagenum()
        # end if
        if (php_isset(lambda : self._pagination_args[key_])):
            return self._pagination_args[key_]
        # end if
    # end def get_pagination_arg
    #// 
    #// Whether the table has items to display or not
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def has_items(self):
        
        
        return (not php_empty(lambda : self.items))
    # end def has_items
    #// 
    #// Message to be displayed when there are no items
    #// 
    #// @since 3.1.0
    #//
    def no_items(self):
        
        
        _e("No items found.")
    # end def no_items
    #// 
    #// Displays the search box.
    #// 
    #// @since 3.1.0
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
        if (not php_empty(lambda : PHP_REQUEST["post_mime_type"])):
            php_print("<input type=\"hidden\" name=\"post_mime_type\" value=\"" + esc_attr(PHP_REQUEST["post_mime_type"]) + "\" />")
        # end if
        if (not php_empty(lambda : PHP_REQUEST["detached"])):
            php_print("<input type=\"hidden\" name=\"detached\" value=\"" + esc_attr(PHP_REQUEST["detached"]) + "\" />")
        # end if
        php_print("<p class=\"search-box\">\n   <label class=\"screen-reader-text\" for=\"")
        php_print(esc_attr(input_id_))
        php_print("\">")
        php_print(text_)
        php_print(":</label>\n  <input type=\"search\" id=\"")
        php_print(esc_attr(input_id_))
        php_print("\" name=\"s\" value=\"")
        _admin_search_query()
        php_print("\" />\n      ")
        submit_button(text_, "", "", False, Array({"id": "search-submit"}))
        php_print("</p>\n       ")
    # end def search_box
    #// 
    #// Get an associative array ( id => link ) with the list
    #// of views available on this table.
    #// 
    #// @since 3.1.0
    #// 
    #// @return array
    #//
    def get_views(self):
        
        
        return Array()
    # end def get_views
    #// 
    #// Display the list of views available on this table.
    #// 
    #// @since 3.1.0
    #//
    def views(self):
        
        
        views_ = self.get_views()
        #// 
        #// Filters the list of available list table views.
        #// 
        #// The dynamic portion of the hook name, `$this->screen->id`, refers
        #// to the ID of the current screen, usually a string.
        #// 
        #// @since 3.5.0
        #// 
        #// @param string[] $views An array of available list table views.
        #//
        views_ = apply_filters(str("views_") + str(self.screen.id), views_)
        if php_empty(lambda : views_):
            return
        # end if
        self.screen.render_screen_reader_content("heading_views")
        php_print("<ul class='subsubsub'>\n")
        for class_,view_ in views_.items():
            views_[class_] = str("  <li class='") + str(class_) + str("'>") + str(view_)
        # end for
        php_print(php_implode(" |</li>\n", views_) + "</li>\n")
        php_print("</ul>")
    # end def views
    #// 
    #// Get an associative array ( option_name => option_title ) with the list
    #// of bulk actions available on this table.
    #// 
    #// @since 3.1.0
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        return Array()
    # end def get_bulk_actions
    #// 
    #// Display the bulk actions dropdown.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $which The location of the bulk actions: 'top' or 'bottom'.
    #// This is designated as optional for backward compatibility.
    #//
    def bulk_actions(self, which_=""):
        
        
        if php_is_null(self._actions):
            self._actions = self.get_bulk_actions()
            #// 
            #// Filters the list table Bulk Actions drop-down.
            #// 
            #// The dynamic portion of the hook name, `$this->screen->id`, refers
            #// to the ID of the current screen, usually a string.
            #// 
            #// This filter can currently only be used to remove bulk actions.
            #// 
            #// @since 3.5.0
            #// 
            #// @param string[] $actions An array of the available bulk actions.
            #//
            self._actions = apply_filters(str("bulk_actions-") + str(self.screen.id), self._actions)
            #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
            two_ = ""
        else:
            two_ = "2"
        # end if
        if php_empty(lambda : self._actions):
            return
        # end if
        php_print("<label for=\"bulk-action-selector-" + esc_attr(which_) + "\" class=\"screen-reader-text\">" + __("Select bulk action") + "</label>")
        php_print("<select name=\"action" + two_ + "\" id=\"bulk-action-selector-" + esc_attr(which_) + "\">\n")
        php_print("<option value=\"-1\">" + __("Bulk Actions") + "</option>\n")
        for name_,title_ in self._actions.items():
            class_ = " class=\"hide-if-no-js\"" if "edit" == name_ else ""
            php_print(" " + "<option value=\"" + name_ + "\"" + class_ + ">" + title_ + "</option>\n")
        # end for
        php_print("</select>\n")
        submit_button(__("Apply"), "action", "", False, Array({"id": str("doaction") + str(two_)}))
        php_print("\n")
    # end def bulk_actions
    #// 
    #// Get the current action selected from the bulk actions dropdown.
    #// 
    #// @since 3.1.0
    #// 
    #// @return string|false The action name or False if no action was selected
    #//
    def current_action(self):
        
        
        if (php_isset(lambda : PHP_REQUEST["filter_action"])) and (not php_empty(lambda : PHP_REQUEST["filter_action"])):
            return False
        # end if
        if (php_isset(lambda : PHP_REQUEST["action"])) and -1 != PHP_REQUEST["action"]:
            return PHP_REQUEST["action"]
        # end if
        if (php_isset(lambda : PHP_REQUEST["action2"])) and -1 != PHP_REQUEST["action2"]:
            return PHP_REQUEST["action2"]
        # end if
        return False
    # end def current_action
    #// 
    #// Generates the required HTML for a list of row action links.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string[] $actions        An array of action links.
    #// @param bool     $always_visible Whether the actions should be always visible.
    #// @return string The HTML for the row actions.
    #//
    def row_actions(self, actions_=None, always_visible_=None):
        if always_visible_ is None:
            always_visible_ = False
        # end if
        
        action_count_ = php_count(actions_)
        i_ = 0
        if (not action_count_):
            return ""
        # end if
        out_ = "<div class=\"" + "row-actions visible" if always_visible_ else "row-actions" + "\">"
        for action_,link_ in actions_.items():
            i_ += 1
            sep_ = "" if i_ == action_count_ else " | "
            out_ += str("<span class='") + str(action_) + str("'>") + str(link_) + str(sep_) + str("</span>")
        # end for
        out_ += "</div>"
        out_ += "<button type=\"button\" class=\"toggle-row\"><span class=\"screen-reader-text\">" + __("Show more details") + "</span></button>"
        return out_
    # end def row_actions
    #// 
    #// Displays a dropdown for filtering items in the list table by month.
    #// 
    #// @since 3.1.0
    #// 
    #// @global wpdb      $wpdb      WordPress database abstraction object.
    #// @global WP_Locale $wp_locale WordPress date and time locale object.
    #// 
    #// @param string $post_type The post type.
    #//
    def months_dropdown(self, post_type_=None):
        
        
        global wpdb_
        global wp_locale_
        php_check_if_defined("wpdb_","wp_locale_")
        #// 
        #// Filters whether to remove the 'Months' drop-down from the post list table.
        #// 
        #// @since 4.2.0
        #// 
        #// @param bool   $disable   Whether to disable the drop-down. Default false.
        #// @param string $post_type The post type.
        #//
        if apply_filters("disable_months_dropdown", False, post_type_):
            return
        # end if
        extra_checks_ = "AND post_status != 'auto-draft'"
        if (not (php_isset(lambda : PHP_REQUEST["post_status"]))) or "trash" != PHP_REQUEST["post_status"]:
            extra_checks_ += " AND post_status != 'trash'"
        elif (php_isset(lambda : PHP_REQUEST["post_status"])):
            extra_checks_ = wpdb_.prepare(" AND post_status = %s", PHP_REQUEST["post_status"])
        # end if
        months_ = wpdb_.get_results(wpdb_.prepare(str("\n           SELECT DISTINCT YEAR( post_date ) AS year, MONTH( post_date ) AS month\n            FROM ") + str(wpdb_.posts) + str("\n            WHERE post_type = %s\n          ") + str(extra_checks_) + str("\n           ORDER BY post_date DESC\n       "), post_type_))
        #// 
        #// Filters the 'Months' drop-down results.
        #// 
        #// @since 3.7.0
        #// 
        #// @param object[] $months    Array of the months drop-down query results.
        #// @param string   $post_type The post type.
        #//
        months_ = apply_filters("months_dropdown_results", months_, post_type_)
        month_count_ = php_count(months_)
        if (not month_count_) or 1 == month_count_ and 0 == months_[0].month:
            return
        # end if
        m_ = php_int(PHP_REQUEST["m"]) if (php_isset(lambda : PHP_REQUEST["m"])) else 0
        php_print("     <label for=\"filter-by-date\" class=\"screen-reader-text\">")
        _e("Filter by date")
        php_print("</label>\n       <select name=\"m\" id=\"filter-by-date\">\n         <option")
        selected(m_, 0)
        php_print(" value=\"0\">")
        _e("All dates")
        php_print("</option>\n      ")
        for arc_row_ in months_:
            if 0 == arc_row_.year:
                continue
            # end if
            month_ = zeroise(arc_row_.month, 2)
            year_ = arc_row_.year
            printf("<option %s value='%s'>%s</option>\n", selected(m_, year_ + month_, False), esc_attr(arc_row_.year + month_), php_sprintf(__("%1$s %2$d"), wp_locale_.get_month(month_), year_))
        # end for
        php_print("     </select>\n     ")
    # end def months_dropdown
    #// 
    #// Display a view switcher
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $current_mode
    #//
    def view_switcher(self, current_mode_=None):
        
        
        php_print("     <input type=\"hidden\" name=\"mode\" value=\"")
        php_print(esc_attr(current_mode_))
        php_print("\" />\n      <div class=\"view-switch\">\n       ")
        for mode_,title_ in self.modes.items():
            classes_ = Array("view-" + mode_)
            aria_current_ = ""
            if current_mode_ == mode_:
                classes_[-1] = "current"
                aria_current_ = " aria-current=\"page\""
            # end if
            printf(str("<a href='%s' class='%s' id='view-switch-") + str(mode_) + str("'") + str(aria_current_) + str("><span class='screen-reader-text'>%s</span></a>\n"), esc_url(add_query_arg("mode", mode_)), php_implode(" ", classes_), title_)
        # end for
        php_print("     </div>\n        ")
    # end def view_switcher
    #// 
    #// Display a comment count bubble
    #// 
    #// @since 3.1.0
    #// 
    #// @param int $post_id          The post ID.
    #// @param int $pending_comments Number of pending comments.
    #//
    def comments_bubble(self, post_id_=None, pending_comments_=None):
        
        
        approved_comments_ = get_comments_number()
        approved_comments_number_ = number_format_i18n(approved_comments_)
        pending_comments_number_ = number_format_i18n(pending_comments_)
        approved_only_phrase_ = php_sprintf(_n("%s comment", "%s comments", approved_comments_), approved_comments_number_)
        approved_phrase_ = php_sprintf(_n("%s approved comment", "%s approved comments", approved_comments_), approved_comments_number_)
        pending_phrase_ = php_sprintf(_n("%s pending comment", "%s pending comments", pending_comments_), pending_comments_number_)
        #// No comments at all.
        if (not approved_comments_) and (not pending_comments_):
            printf("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">%s</span>", __("No comments"))
            pass
        elif approved_comments_:
            printf("<a href=\"%s\" class=\"post-com-count post-com-count-approved\"><span class=\"comment-count-approved\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(add_query_arg(Array({"p": post_id_, "comment_status": "approved"}), admin_url("edit-comments.php"))), approved_comments_number_, approved_phrase_ if pending_comments_ else approved_only_phrase_)
        else:
            printf("<span class=\"post-com-count post-com-count-no-comments\"><span class=\"comment-count comment-count-no-comments\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></span>", approved_comments_number_, __("No approved comments") if pending_comments_ else __("No comments"))
        # end if
        if pending_comments_:
            printf("<a href=\"%s\" class=\"post-com-count post-com-count-pending\"><span class=\"comment-count-pending\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(add_query_arg(Array({"p": post_id_, "comment_status": "moderated"}), admin_url("edit-comments.php"))), pending_comments_number_, pending_phrase_)
        else:
            printf("<span class=\"post-com-count post-com-count-pending post-com-count-no-pending\"><span class=\"comment-count comment-count-no-pending\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></span>", pending_comments_number_, __("No pending comments") if approved_comments_ else __("No comments"))
        # end if
    # end def comments_bubble
    #// 
    #// Get the current page number
    #// 
    #// @since 3.1.0
    #// 
    #// @return int
    #//
    def get_pagenum(self):
        
        
        pagenum_ = absint(PHP_REQUEST["paged"]) if (php_isset(lambda : PHP_REQUEST["paged"])) else 0
        if (php_isset(lambda : self._pagination_args["total_pages"])) and pagenum_ > self._pagination_args["total_pages"]:
            pagenum_ = self._pagination_args["total_pages"]
        # end if
        return php_max(1, pagenum_)
    # end def get_pagenum
    #// 
    #// Get number of items to display on a single page
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $option
    #// @param int    $default
    #// @return int
    #//
    def get_items_per_page(self, option_=None, default_=20):
        
        
        per_page_ = php_int(get_user_option(option_))
        if php_empty(lambda : per_page_) or per_page_ < 1:
            per_page_ = default_
        # end if
        #// 
        #// Filters the number of items to be displayed on each page of the list table.
        #// 
        #// The dynamic hook name, $option, refers to the `per_page` option depending
        #// on the type of list table in use. Possible values include: 'edit_comments_per_page',
        #// 'sites_network_per_page', 'site_themes_network_per_page', 'themes_network_per_page',
        #// 'users_network_per_page', 'edit_post_per_page', 'edit_page_per_page',
        #// 'edit_{$post_type}_per_page', etc.
        #// 
        #// @since 2.9.0
        #// 
        #// @param int $per_page Number of items to be displayed. Default 20.
        #//
        return php_int(apply_filters(str(option_), per_page_))
    # end def get_items_per_page
    #// 
    #// Display the pagination.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $which
    #//
    def pagination(self, which_=None):
        
        
        if php_empty(lambda : self._pagination_args):
            return
        # end if
        total_items_ = self._pagination_args["total_items"]
        total_pages_ = self._pagination_args["total_pages"]
        infinite_scroll_ = False
        if (php_isset(lambda : self._pagination_args["infinite_scroll"])):
            infinite_scroll_ = self._pagination_args["infinite_scroll"]
        # end if
        if "top" == which_ and total_pages_ > 1:
            self.screen.render_screen_reader_content("heading_pagination")
        # end if
        output_ = "<span class=\"displaying-num\">" + php_sprintf(_n("%s item", "%s items", total_items_), number_format_i18n(total_items_)) + "</span>"
        current_ = self.get_pagenum()
        removable_query_args_ = wp_removable_query_args()
        current_url_ = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
        current_url_ = remove_query_arg(removable_query_args_, current_url_)
        page_links_ = Array()
        total_pages_before_ = "<span class=\"paging-input\">"
        total_pages_after_ = "</span></span>"
        disable_first_ = False
        disable_last_ = False
        disable_prev_ = False
        disable_next_ = False
        if 1 == current_:
            disable_first_ = True
            disable_prev_ = True
        # end if
        if 2 == current_:
            disable_first_ = True
        # end if
        if total_pages_ == current_:
            disable_last_ = True
            disable_next_ = True
        # end if
        if total_pages_ - 1 == current_:
            disable_last_ = True
        # end if
        if disable_first_:
            page_links_[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&laquo;</span>"
        else:
            page_links_[-1] = php_sprintf("<a class='first-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(remove_query_arg("paged", current_url_)), __("First page"), "&laquo;")
        # end if
        if disable_prev_:
            page_links_[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&lsaquo;</span>"
        else:
            page_links_[-1] = php_sprintf("<a class='prev-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(add_query_arg("paged", php_max(1, current_ - 1), current_url_)), __("Previous page"), "&lsaquo;")
        # end if
        if "bottom" == which_:
            html_current_page_ = current_
            total_pages_before_ = "<span class=\"screen-reader-text\">" + __("Current Page") + "</span><span id=\"table-paging\" class=\"paging-input\"><span class=\"tablenav-paging-text\">"
        else:
            html_current_page_ = php_sprintf("%s<input class='current-page' id='current-page-selector' type='text' name='paged' value='%s' size='%d' aria-describedby='table-paging' /><span class='tablenav-paging-text'>", "<label for=\"current-page-selector\" class=\"screen-reader-text\">" + __("Current Page") + "</label>", current_, php_strlen(total_pages_))
        # end if
        html_total_pages_ = php_sprintf("<span class='total-pages'>%s</span>", number_format_i18n(total_pages_))
        page_links_[-1] = total_pages_before_ + php_sprintf(_x("%1$s of %2$s", "paging"), html_current_page_, html_total_pages_) + total_pages_after_
        if disable_next_:
            page_links_[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&rsaquo;</span>"
        else:
            page_links_[-1] = php_sprintf("<a class='next-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(add_query_arg("paged", php_min(total_pages_, current_ + 1), current_url_)), __("Next page"), "&rsaquo;")
        # end if
        if disable_last_:
            page_links_[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&raquo;</span>"
        else:
            page_links_[-1] = php_sprintf("<a class='last-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(add_query_arg("paged", total_pages_, current_url_)), __("Last page"), "&raquo;")
        # end if
        pagination_links_class_ = "pagination-links"
        if (not php_empty(lambda : infinite_scroll_)):
            pagination_links_class_ += " hide-if-js"
        # end if
        output_ += str("\n<span class='") + str(pagination_links_class_) + str("'>") + join("\n", page_links_) + "</span>"
        if total_pages_:
            page_class_ = " one-page" if total_pages_ < 2 else ""
        else:
            page_class_ = " no-pages"
        # end if
        self._pagination = str("<div class='tablenav-pages") + str(page_class_) + str("'>") + str(output_) + str("</div>")
        php_print(self._pagination)
    # end def pagination
    #// 
    #// Get a list of columns. The format is:
    #// 'internal-name' => 'Title'
    #// 
    #// @since 3.1.0
    #// @abstract
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        php_print("function WP_List_Table::get_columns() must be overridden in a subclass.")
        php_exit()
    # end def get_columns
    #// 
    #// Get a list of sortable columns. The format is:
    #// 'internal-name' => 'orderby'
    #// or
    #// 'internal-name' => array( 'orderby', true )
    #// 
    #// The second format will make the initial sorting order be descending
    #// 
    #// @since 3.1.0
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        
        return Array()
    # end def get_sortable_columns
    #// 
    #// Gets the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, an empty string.
    #//
    def get_default_primary_column_name(self):
        
        
        columns_ = self.get_columns()
        column_ = ""
        if php_empty(lambda : columns_):
            return column_
        # end if
        #// We need a primary defined so responsive views show something,
        #// so let's fall back to the first non-checkbox column.
        for col_,column_name_ in columns_.items():
            if "cb" == col_:
                continue
            # end if
            column_ = col_
            break
        # end for
        return column_
    # end def get_default_primary_column_name
    #// 
    #// Public wrapper for WP_List_Table::get_default_primary_column_name().
    #// 
    #// @since 4.4.0
    #// 
    #// @return string Name of the default primary column.
    #//
    def get_primary_column(self):
        
        
        return self.get_primary_column_name()
    # end def get_primary_column
    #// 
    #// Gets the name of the primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string The name of the primary column.
    #//
    def get_primary_column_name(self):
        
        
        columns_ = get_column_headers(self.screen)
        default_ = self.get_default_primary_column_name()
        #// If the primary column doesn't exist,
        #// fall back to the first non-checkbox column.
        if (not (php_isset(lambda : columns_[default_]))):
            default_ = WP_List_Table.get_default_primary_column_name()
        # end if
        #// 
        #// Filters the name of the primary column for the current list table.
        #// 
        #// @since 4.3.0
        #// 
        #// @param string $default Column name default for the specific list table, e.g. 'name'.
        #// @param string $context Screen ID for specific list table, e.g. 'plugins'.
        #//
        column_ = apply_filters("list_table_primary_column", default_, self.screen.id)
        if php_empty(lambda : column_) or (not (php_isset(lambda : columns_[column_]))):
            column_ = default_
        # end if
        return column_
    # end def get_primary_column_name
    #// 
    #// Get a list of all, hidden and sortable columns, with filter applied
    #// 
    #// @since 3.1.0
    #// 
    #// @return array
    #//
    def get_column_info(self):
        
        
        #// $_column_headers is already set / cached.
        if (php_isset(lambda : self._column_headers)) and php_is_array(self._column_headers):
            #// Back-compat for list tables that have been manually setting $_column_headers for horse reasons.
            #// In 4.3, we added a fourth argument for primary column.
            column_headers_ = Array(Array(), Array(), Array(), self.get_primary_column_name())
            for key_,value_ in self._column_headers.items():
                column_headers_[key_] = value_
            # end for
            return column_headers_
        # end if
        columns_ = get_column_headers(self.screen)
        hidden_ = get_hidden_columns(self.screen)
        sortable_columns_ = self.get_sortable_columns()
        #// 
        #// Filters the list table sortable columns for a specific screen.
        #// 
        #// The dynamic portion of the hook name, `$this->screen->id`, refers
        #// to the ID of the current screen, usually a string.
        #// 
        #// @since 3.5.0
        #// 
        #// @param array $sortable_columns An array of sortable columns.
        #//
        _sortable_ = apply_filters(str("manage_") + str(self.screen.id) + str("_sortable_columns"), sortable_columns_)
        sortable_ = Array()
        for id_,data_ in _sortable_.items():
            if php_empty(lambda : data_):
                continue
            # end if
            data_ = data_
            if (not (php_isset(lambda : data_[1]))):
                data_[1] = False
            # end if
            sortable_[id_] = data_
        # end for
        primary_ = self.get_primary_column_name()
        self._column_headers = Array(columns_, hidden_, sortable_, primary_)
        return self._column_headers
    # end def get_column_info
    #// 
    #// Return number of visible columns
    #// 
    #// @since 3.1.0
    #// 
    #// @return int
    #//
    def get_column_count(self):
        
        
        columns_, hidden_ = self.get_column_info()
        hidden_ = php_array_intersect(php_array_keys(columns_), php_array_filter(hidden_))
        return php_count(columns_) - php_count(hidden_)
    # end def get_column_count
    #// 
    #// Print column headers, accounting for hidden and sortable columns.
    #// 
    #// @since 3.1.0
    #// 
    #// @staticvar int $cb_counter
    #// 
    #// @param bool $with_id Whether to set the id attribute or not
    #//
    def print_column_headers(self, with_id_=None):
        if with_id_ is None:
            with_id_ = True
        # end if
        
        columns_, hidden_, sortable_, primary_ = self.get_column_info()
        current_url_ = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
        current_url_ = remove_query_arg("paged", current_url_)
        if (php_isset(lambda : PHP_REQUEST["orderby"])):
            current_orderby_ = PHP_REQUEST["orderby"]
        else:
            current_orderby_ = ""
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])) and "desc" == PHP_REQUEST["order"]:
            current_order_ = "desc"
        else:
            current_order_ = "asc"
        # end if
        if (not php_empty(lambda : columns_["cb"])):
            cb_counter_ = 1
            columns_["cb"] = "<label class=\"screen-reader-text\" for=\"cb-select-all-" + cb_counter_ + "\">" + __("Select All") + "</label>" + "<input id=\"cb-select-all-" + cb_counter_ + "\" type=\"checkbox\" />"
            cb_counter_ += 1
        # end if
        for column_key_,column_display_name_ in columns_.items():
            class_ = Array("manage-column", str("column-") + str(column_key_))
            if php_in_array(column_key_, hidden_):
                class_[-1] = "hidden"
            # end if
            if "cb" == column_key_:
                class_[-1] = "check-column"
            elif php_in_array(column_key_, Array("posts", "comments", "links")):
                class_[-1] = "num"
            # end if
            if column_key_ == primary_:
                class_[-1] = "column-primary"
            # end if
            if (php_isset(lambda : sortable_[column_key_])):
                orderby_, desc_first_ = sortable_[column_key_]
                if current_orderby_ == orderby_:
                    order_ = "desc" if "asc" == current_order_ else "asc"
                    class_[-1] = "sorted"
                    class_[-1] = current_order_
                else:
                    order_ = "desc" if desc_first_ else "asc"
                    class_[-1] = "sortable"
                    class_[-1] = "asc" if desc_first_ else "desc"
                # end if
                column_display_name_ = "<a href=\"" + esc_url(add_query_arg(php_compact("orderby_", "order_"), current_url_)) + "\"><span>" + column_display_name_ + "</span><span class=\"sorting-indicator\"></span></a>"
            # end if
            tag_ = "td" if "cb" == column_key_ else "th"
            scope_ = "scope=\"col\"" if "th" == tag_ else ""
            id_ = str("id='") + str(column_key_) + str("'") if with_id_ else ""
            if (not php_empty(lambda : class_)):
                class_ = "class='" + join(" ", class_) + "'"
            # end if
            php_print(str("<") + str(tag_) + str(" ") + str(scope_) + str(" ") + str(id_) + str(" ") + str(class_) + str(">") + str(column_display_name_) + str("</") + str(tag_) + str(">"))
        # end for
    # end def print_column_headers
    #// 
    #// Displays the table.
    #// 
    #// @since 3.1.0
    #//
    def display(self):
        
        
        singular_ = self._args["singular"]
        self.display_tablenav("top")
        self.screen.render_screen_reader_content("heading_list")
        php_print("<table class=\"wp-list-table ")
        php_print(php_implode(" ", self.get_table_classes()))
        php_print("""\">
        <thead>
        <tr>
        """)
        self.print_column_headers()
        php_print("""   </tr>
        </thead>
        <tbody id=\"the-list\"
        """)
        if singular_:
            php_print(str(" data-wp-lists='list:") + str(singular_) + str("'"))
        # end if
        php_print("     >\n     ")
        self.display_rows_or_placeholder()
        php_print("""   </tbody>
        <tfoot>
        <tr>
        """)
        self.print_column_headers(False)
        php_print("""   </tr>
        </tfoot>
        </table>
        """)
        self.display_tablenav("bottom")
    # end def display
    #// 
    #// Get a list of CSS classes for the WP_List_Table table tag.
    #// 
    #// @since 3.1.0
    #// 
    #// @return string[] Array of CSS classes for the table tag.
    #//
    def get_table_classes(self):
        
        
        return Array("widefat", "fixed", "striped", self._args["plural"])
    # end def get_table_classes
    #// 
    #// Generate the table navigation above or below the table
    #// 
    #// @since 3.1.0
    #// @param string $which
    #//
    def display_tablenav(self, which_=None):
        
        
        if "top" == which_:
            wp_nonce_field("bulk-" + self._args["plural"])
        # end if
        php_print(" <div class=\"tablenav ")
        php_print(esc_attr(which_))
        php_print("\">\n\n      ")
        if self.has_items():
            php_print("     <div class=\"alignleft actions bulkactions\">\n         ")
            self.bulk_actions(which_)
            php_print("     </div>\n            ")
        # end if
        self.extra_tablenav(which_)
        self.pagination(which_)
        php_print("""
        <br class=\"clear\" />
        </div>
        """)
    # end def display_tablenav
    #// 
    #// Extra controls to be displayed between bulk actions and pagination
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $which
    #//
    def extra_tablenav(self, which_=None):
        
        
        pass
    # end def extra_tablenav
    #// 
    #// Generate the tbody element for the list table.
    #// 
    #// @since 3.1.0
    #//
    def display_rows_or_placeholder(self):
        
        
        if self.has_items():
            self.display_rows()
        else:
            php_print("<tr class=\"no-items\"><td class=\"colspanchange\" colspan=\"" + self.get_column_count() + "\">")
            self.no_items()
            php_print("</td></tr>")
        # end if
    # end def display_rows_or_placeholder
    #// 
    #// Generate the table rows
    #// 
    #// @since 3.1.0
    #//
    def display_rows(self):
        
        
        for item_ in self.items:
            self.single_row(item_)
        # end for
    # end def display_rows
    #// 
    #// Generates content for a single row of the table
    #// 
    #// @since 3.1.0
    #// 
    #// @param object $item The current item
    #//
    def single_row(self, item_=None):
        
        
        php_print("<tr>")
        self.single_row_columns(item_)
        php_print("</tr>")
    # end def single_row
    #// 
    #// @param object $item
    #// @param string $column_name
    #//
    def column_default(self, item_=None, column_name_=None):
        
        
        pass
    # end def column_default
    #// 
    #// @param object $item
    #//
    def column_cb(self, item_=None):
        
        
        pass
    # end def column_cb
    #// 
    #// Generates the columns for a single row of the table
    #// 
    #// @since 3.1.0
    #// 
    #// @param object $item The current item
    #//
    def single_row_columns(self, item_=None):
        
        
        columns_, hidden_, sortable_, primary_ = self.get_column_info()
        for column_name_,column_display_name_ in columns_.items():
            classes_ = str(column_name_) + str(" column-") + str(column_name_)
            if primary_ == column_name_:
                classes_ += " has-row-actions column-primary"
            # end if
            if php_in_array(column_name_, hidden_):
                classes_ += " hidden"
            # end if
            #// Comments column uses HTML in the display name with screen reader text.
            #// Instead of using esc_attr(), we strip tags to get closer to a user-friendly string.
            data_ = "data-colname=\"" + wp_strip_all_tags(column_display_name_) + "\""
            attributes_ = str("class='") + str(classes_) + str("' ") + str(data_)
            if "cb" == column_name_:
                php_print("<th scope=\"row\" class=\"check-column\">")
                php_print(self.column_cb(item_))
                php_print("</th>")
            elif php_method_exists(self, "_column_" + column_name_):
                php_print(php_call_user_func(Array(self, "_column_" + column_name_), item_, classes_, data_, primary_))
            elif php_method_exists(self, "column_" + column_name_):
                php_print(str("<td ") + str(attributes_) + str(">"))
                php_print(php_call_user_func(Array(self, "column_" + column_name_), item_))
                php_print(self.handle_row_actions(item_, column_name_, primary_))
                php_print("</td>")
            else:
                php_print(str("<td ") + str(attributes_) + str(">"))
                php_print(self.column_default(item_, column_name_))
                php_print(self.handle_row_actions(item_, column_name_, primary_))
                php_print("</td>")
            # end if
        # end for
    # end def single_row_columns
    #// 
    #// Generates and display row actions links for the list table.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $item        The item being acted upon.
    #// @param string $column_name Current column name.
    #// @param string $primary     Primary column name.
    #// @return string The row actions HTML, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, item_=None, column_name_=None, primary_=None):
        
        
        return "<button type=\"button\" class=\"toggle-row\"><span class=\"screen-reader-text\">" + __("Show more details") + "</span></button>" if column_name_ == primary_ else ""
    # end def handle_row_actions
    #// 
    #// Handle an incoming ajax request (called from admin-ajax.php)
    #// 
    #// @since 3.1.0
    #//
    def ajax_response(self):
        
        
        self.prepare_items()
        ob_start()
        if (not php_empty(lambda : PHP_REQUEST["no_placeholder"])):
            self.display_rows()
        else:
            self.display_rows_or_placeholder()
        # end if
        rows_ = ob_get_clean()
        response_ = Array({"rows": rows_})
        if (php_isset(lambda : self._pagination_args["total_items"])):
            response_["total_items_i18n"] = php_sprintf(_n("%s item", "%s items", self._pagination_args["total_items"]), number_format_i18n(self._pagination_args["total_items"]))
        # end if
        if (php_isset(lambda : self._pagination_args["total_pages"])):
            response_["total_pages"] = self._pagination_args["total_pages"]
            response_["total_pages_i18n"] = number_format_i18n(self._pagination_args["total_pages"])
        # end if
        php_print(wp_json_encode(response_))
        php_exit()
    # end def ajax_response
    #// 
    #// Send required variables to JavaScript land
    #//
    def _js_vars(self):
        
        
        args_ = Array({"class": get_class(self), "screen": Array({"id": self.screen.id, "base": self.screen.base})})
        printf("<script type='text/javascript'>list_args = %s;</script>\n", wp_json_encode(args_))
    # end def _js_vars
# end class WP_List_Table
