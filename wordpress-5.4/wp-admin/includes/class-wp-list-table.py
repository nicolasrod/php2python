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
    items = Array()
    _args = Array()
    _pagination_args = Array()
    screen = Array()
    _actions = Array()
    _pagination = Array()
    modes = Array()
    _column_headers = Array()
    compat_fields = Array("_args", "_pagination_args", "screen", "_actions", "_pagination")
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
    def __init__(self, args=Array()):
        
        args = wp_parse_args(args, Array({"plural": "", "singular": "", "ajax": False, "screen": None}))
        self.screen = convert_to_screen(args["screen"])
        add_filter(str("manage_") + str(self.screen.id) + str("_columns"), Array(self, "get_columns"), 0)
        if (not args["plural"]):
            args["plural"] = self.screen.base
        # end if
        args["plural"] = sanitize_key(args["plural"])
        args["singular"] = sanitize_key(args["singular"])
        self._args = args
        if args["ajax"]:
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
    def __get(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return self.name
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
    def __set(self, name=None, value=None):
        
        if php_in_array(name, self.compat_fields):
            self.name = value
            return self.name
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
    def __isset(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return (php_isset(lambda : self.name))
        # end if
    # end def __isset
    #// 
    #// Make private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            self.name = None
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
    def __call(self, name=None, arguments=None):
        
        if php_in_array(name, self.compat_methods):
            return self.name(arguments)
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
    def set_pagination_args(self, args=None):
        
        args = wp_parse_args(args, Array({"total_items": 0, "total_pages": 0, "per_page": 0}))
        if (not args["total_pages"]) and args["per_page"] > 0:
            args["total_pages"] = ceil(args["total_items"] / args["per_page"])
        # end if
        #// Redirect if page number is invalid and headers are not already sent.
        if (not php_headers_sent()) and (not wp_doing_ajax()) and args["total_pages"] > 0 and self.get_pagenum() > args["total_pages"]:
            wp_redirect(add_query_arg("paged", args["total_pages"]))
            php_exit(0)
        # end if
        self._pagination_args = args
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
    def get_pagination_arg(self, key=None):
        
        if "page" == key:
            return self.get_pagenum()
        # end if
        if (php_isset(lambda : self._pagination_args[key])):
            return self._pagination_args[key]
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
        if (not php_empty(lambda : PHP_REQUEST["post_mime_type"])):
            php_print("<input type=\"hidden\" name=\"post_mime_type\" value=\"" + esc_attr(PHP_REQUEST["post_mime_type"]) + "\" />")
        # end if
        if (not php_empty(lambda : PHP_REQUEST["detached"])):
            php_print("<input type=\"hidden\" name=\"detached\" value=\"" + esc_attr(PHP_REQUEST["detached"]) + "\" />")
        # end if
        php_print("<p class=\"search-box\">\n   <label class=\"screen-reader-text\" for=\"")
        php_print(esc_attr(input_id))
        php_print("\">")
        php_print(text)
        php_print(":</label>\n  <input type=\"search\" id=\"")
        php_print(esc_attr(input_id))
        php_print("\" name=\"s\" value=\"")
        _admin_search_query()
        php_print("\" />\n      ")
        submit_button(text, "", "", False, Array({"id": "search-submit"}))
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
        
        views = self.get_views()
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
        views = apply_filters(str("views_") + str(self.screen.id), views)
        if php_empty(lambda : views):
            return
        # end if
        self.screen.render_screen_reader_content("heading_views")
        php_print("<ul class='subsubsub'>\n")
        for class_,view in views:
            views[class_] = str("   <li class='") + str(class_) + str("'>") + str(view)
        # end for
        php_print(php_implode(" |</li>\n", views) + "</li>\n")
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
    def bulk_actions(self, which=""):
        
        if is_null(self._actions):
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
            two = ""
        else:
            two = "2"
        # end if
        if php_empty(lambda : self._actions):
            return
        # end if
        php_print("<label for=\"bulk-action-selector-" + esc_attr(which) + "\" class=\"screen-reader-text\">" + __("Select bulk action") + "</label>")
        php_print("<select name=\"action" + two + "\" id=\"bulk-action-selector-" + esc_attr(which) + "\">\n")
        php_print("<option value=\"-1\">" + __("Bulk Actions") + "</option>\n")
        for name,title in self._actions:
            class_ = " class=\"hide-if-no-js\"" if "edit" == name else ""
            php_print(" " + "<option value=\"" + name + "\"" + class_ + ">" + title + "</option>\n")
        # end for
        php_print("</select>\n")
        submit_button(__("Apply"), "action", "", False, Array({"id": str("doaction") + str(two)}))
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
    def row_actions(self, actions=None, always_visible=False):
        
        action_count = php_count(actions)
        i = 0
        if (not action_count):
            return ""
        # end if
        out = "<div class=\"" + "row-actions visible" if always_visible else "row-actions" + "\">"
        for action,link in actions:
            i += 1
            sep = "" if i == action_count else " | "
            out += str("<span class='") + str(action) + str("'>") + str(link) + str(sep) + str("</span>")
        # end for
        out += "</div>"
        out += "<button type=\"button\" class=\"toggle-row\"><span class=\"screen-reader-text\">" + __("Show more details") + "</span></button>"
        return out
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
    def months_dropdown(self, post_type=None):
        
        global wpdb,wp_locale
        php_check_if_defined("wpdb","wp_locale")
        #// 
        #// Filters whether to remove the 'Months' drop-down from the post list table.
        #// 
        #// @since 4.2.0
        #// 
        #// @param bool   $disable   Whether to disable the drop-down. Default false.
        #// @param string $post_type The post type.
        #//
        if apply_filters("disable_months_dropdown", False, post_type):
            return
        # end if
        extra_checks = "AND post_status != 'auto-draft'"
        if (not (php_isset(lambda : PHP_REQUEST["post_status"]))) or "trash" != PHP_REQUEST["post_status"]:
            extra_checks += " AND post_status != 'trash'"
        elif (php_isset(lambda : PHP_REQUEST["post_status"])):
            extra_checks = wpdb.prepare(" AND post_status = %s", PHP_REQUEST["post_status"])
        # end if
        months = wpdb.get_results(wpdb.prepare(str("\n          SELECT DISTINCT YEAR( post_date ) AS year, MONTH( post_date ) AS month\n            FROM ") + str(wpdb.posts) + str("\n         WHERE post_type = %s\n          ") + str(extra_checks) + str("\n            ORDER BY post_date DESC\n       "), post_type))
        #// 
        #// Filters the 'Months' drop-down results.
        #// 
        #// @since 3.7.0
        #// 
        #// @param object[] $months    Array of the months drop-down query results.
        #// @param string   $post_type The post type.
        #//
        months = apply_filters("months_dropdown_results", months, post_type)
        month_count = php_count(months)
        if (not month_count) or 1 == month_count and 0 == months[0].month:
            return
        # end if
        m = php_int(PHP_REQUEST["m"]) if (php_isset(lambda : PHP_REQUEST["m"])) else 0
        php_print("     <label for=\"filter-by-date\" class=\"screen-reader-text\">")
        _e("Filter by date")
        php_print("</label>\n       <select name=\"m\" id=\"filter-by-date\">\n         <option")
        selected(m, 0)
        php_print(" value=\"0\">")
        _e("All dates")
        php_print("</option>\n      ")
        for arc_row in months:
            if 0 == arc_row.year:
                continue
            # end if
            month = zeroise(arc_row.month, 2)
            year = arc_row.year
            printf("<option %s value='%s'>%s</option>\n", selected(m, year + month, False), esc_attr(arc_row.year + month), php_sprintf(__("%1$s %2$d"), wp_locale.get_month(month), year))
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
    def view_switcher(self, current_mode=None):
        
        php_print("     <input type=\"hidden\" name=\"mode\" value=\"")
        php_print(esc_attr(current_mode))
        php_print("\" />\n      <div class=\"view-switch\">\n       ")
        for mode,title in self.modes:
            classes = Array("view-" + mode)
            aria_current = ""
            if current_mode == mode:
                classes[-1] = "current"
                aria_current = " aria-current=\"page\""
            # end if
            printf(str("<a href='%s' class='%s' id='view-switch-") + str(mode) + str("'") + str(aria_current) + str("><span class='screen-reader-text'>%s</span></a>\n"), esc_url(add_query_arg("mode", mode)), php_implode(" ", classes), title)
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
    def comments_bubble(self, post_id=None, pending_comments=None):
        
        approved_comments = get_comments_number()
        approved_comments_number = number_format_i18n(approved_comments)
        pending_comments_number = number_format_i18n(pending_comments)
        approved_only_phrase = php_sprintf(_n("%s comment", "%s comments", approved_comments), approved_comments_number)
        approved_phrase = php_sprintf(_n("%s approved comment", "%s approved comments", approved_comments), approved_comments_number)
        pending_phrase = php_sprintf(_n("%s pending comment", "%s pending comments", pending_comments), pending_comments_number)
        #// No comments at all.
        if (not approved_comments) and (not pending_comments):
            printf("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">%s</span>", __("No comments"))
            pass
        elif approved_comments:
            printf("<a href=\"%s\" class=\"post-com-count post-com-count-approved\"><span class=\"comment-count-approved\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(add_query_arg(Array({"p": post_id, "comment_status": "approved"}), admin_url("edit-comments.php"))), approved_comments_number, approved_phrase if pending_comments else approved_only_phrase)
        else:
            printf("<span class=\"post-com-count post-com-count-no-comments\"><span class=\"comment-count comment-count-no-comments\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></span>", approved_comments_number, __("No approved comments") if pending_comments else __("No comments"))
        # end if
        if pending_comments:
            printf("<a href=\"%s\" class=\"post-com-count post-com-count-pending\"><span class=\"comment-count-pending\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(add_query_arg(Array({"p": post_id, "comment_status": "moderated"}), admin_url("edit-comments.php"))), pending_comments_number, pending_phrase)
        else:
            printf("<span class=\"post-com-count post-com-count-pending post-com-count-no-pending\"><span class=\"comment-count comment-count-no-pending\" aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></span>", pending_comments_number, __("No pending comments") if approved_comments else __("No comments"))
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
        
        pagenum = absint(PHP_REQUEST["paged"]) if (php_isset(lambda : PHP_REQUEST["paged"])) else 0
        if (php_isset(lambda : self._pagination_args["total_pages"])) and pagenum > self._pagination_args["total_pages"]:
            pagenum = self._pagination_args["total_pages"]
        # end if
        return php_max(1, pagenum)
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
    def get_items_per_page(self, option=None, default=20):
        
        per_page = php_int(get_user_option(option))
        if php_empty(lambda : per_page) or per_page < 1:
            per_page = default
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
        return php_int(apply_filters(str(option), per_page))
    # end def get_items_per_page
    #// 
    #// Display the pagination.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $which
    #//
    def pagination(self, which=None):
        
        if php_empty(lambda : self._pagination_args):
            return
        # end if
        total_items = self._pagination_args["total_items"]
        total_pages = self._pagination_args["total_pages"]
        infinite_scroll = False
        if (php_isset(lambda : self._pagination_args["infinite_scroll"])):
            infinite_scroll = self._pagination_args["infinite_scroll"]
        # end if
        if "top" == which and total_pages > 1:
            self.screen.render_screen_reader_content("heading_pagination")
        # end if
        output = "<span class=\"displaying-num\">" + php_sprintf(_n("%s item", "%s items", total_items), number_format_i18n(total_items)) + "</span>"
        current = self.get_pagenum()
        removable_query_args = wp_removable_query_args()
        current_url = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
        current_url = remove_query_arg(removable_query_args, current_url)
        page_links = Array()
        total_pages_before = "<span class=\"paging-input\">"
        total_pages_after = "</span></span>"
        disable_first = False
        disable_last = False
        disable_prev = False
        disable_next = False
        if 1 == current:
            disable_first = True
            disable_prev = True
        # end if
        if 2 == current:
            disable_first = True
        # end if
        if total_pages == current:
            disable_last = True
            disable_next = True
        # end if
        if total_pages - 1 == current:
            disable_last = True
        # end if
        if disable_first:
            page_links[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&laquo;</span>"
        else:
            page_links[-1] = php_sprintf("<a class='first-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(remove_query_arg("paged", current_url)), __("First page"), "&laquo;")
        # end if
        if disable_prev:
            page_links[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&lsaquo;</span>"
        else:
            page_links[-1] = php_sprintf("<a class='prev-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(add_query_arg("paged", php_max(1, current - 1), current_url)), __("Previous page"), "&lsaquo;")
        # end if
        if "bottom" == which:
            html_current_page = current
            total_pages_before = "<span class=\"screen-reader-text\">" + __("Current Page") + "</span><span id=\"table-paging\" class=\"paging-input\"><span class=\"tablenav-paging-text\">"
        else:
            html_current_page = php_sprintf("%s<input class='current-page' id='current-page-selector' type='text' name='paged' value='%s' size='%d' aria-describedby='table-paging' /><span class='tablenav-paging-text'>", "<label for=\"current-page-selector\" class=\"screen-reader-text\">" + __("Current Page") + "</label>", current, php_strlen(total_pages))
        # end if
        html_total_pages = php_sprintf("<span class='total-pages'>%s</span>", number_format_i18n(total_pages))
        page_links[-1] = total_pages_before + php_sprintf(_x("%1$s of %2$s", "paging"), html_current_page, html_total_pages) + total_pages_after
        if disable_next:
            page_links[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&rsaquo;</span>"
        else:
            page_links[-1] = php_sprintf("<a class='next-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(add_query_arg("paged", php_min(total_pages, current + 1), current_url)), __("Next page"), "&rsaquo;")
        # end if
        if disable_last:
            page_links[-1] = "<span class=\"tablenav-pages-navspan button disabled\" aria-hidden=\"true\">&raquo;</span>"
        else:
            page_links[-1] = php_sprintf("<a class='last-page button' href='%s'><span class='screen-reader-text'>%s</span><span aria-hidden='true'>%s</span></a>", esc_url(add_query_arg("paged", total_pages, current_url)), __("Last page"), "&raquo;")
        # end if
        pagination_links_class = "pagination-links"
        if (not php_empty(lambda : infinite_scroll)):
            pagination_links_class += " hide-if-js"
        # end if
        output += str("\n<span class='") + str(pagination_links_class) + str("'>") + join("\n", page_links) + "</span>"
        if total_pages:
            page_class = " one-page" if total_pages < 2 else ""
        else:
            page_class = " no-pages"
        # end if
        self._pagination = str("<div class='tablenav-pages") + str(page_class) + str("'>") + str(output) + str("</div>")
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
        
        columns = self.get_columns()
        column = ""
        if php_empty(lambda : columns):
            return column
        # end if
        #// We need a primary defined so responsive views show something,
        #// so let's fall back to the first non-checkbox column.
        for col,column_name in columns:
            if "cb" == col:
                continue
            # end if
            column = col
            break
        # end for
        return column
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
        
        columns = get_column_headers(self.screen)
        default = self.get_default_primary_column_name()
        #// If the primary column doesn't exist,
        #// fall back to the first non-checkbox column.
        if (not (php_isset(lambda : columns[default]))):
            default = WP_List_Table.get_default_primary_column_name()
        # end if
        #// 
        #// Filters the name of the primary column for the current list table.
        #// 
        #// @since 4.3.0
        #// 
        #// @param string $default Column name default for the specific list table, e.g. 'name'.
        #// @param string $context Screen ID for specific list table, e.g. 'plugins'.
        #//
        column = apply_filters("list_table_primary_column", default, self.screen.id)
        if php_empty(lambda : column) or (not (php_isset(lambda : columns[column]))):
            column = default
        # end if
        return column
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
            column_headers = Array(Array(), Array(), Array(), self.get_primary_column_name())
            for key,value in self._column_headers:
                column_headers[key] = value
            # end for
            return column_headers
        # end if
        columns = get_column_headers(self.screen)
        hidden = get_hidden_columns(self.screen)
        sortable_columns = self.get_sortable_columns()
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
        _sortable = apply_filters(str("manage_") + str(self.screen.id) + str("_sortable_columns"), sortable_columns)
        sortable = Array()
        for id,data in _sortable:
            if php_empty(lambda : data):
                continue
            # end if
            data = data
            if (not (php_isset(lambda : data[1]))):
                data[1] = False
            # end if
            sortable[id] = data
        # end for
        primary = self.get_primary_column_name()
        self._column_headers = Array(columns, hidden, sortable, primary)
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
        
        columns, hidden = self.get_column_info()
        hidden = php_array_intersect(php_array_keys(columns), php_array_filter(hidden))
        return php_count(columns) - php_count(hidden)
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
    def print_column_headers(self, with_id=True):
        
        columns, hidden, sortable, primary = self.get_column_info()
        current_url = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
        current_url = remove_query_arg("paged", current_url)
        if (php_isset(lambda : PHP_REQUEST["orderby"])):
            current_orderby = PHP_REQUEST["orderby"]
        else:
            current_orderby = ""
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])) and "desc" == PHP_REQUEST["order"]:
            current_order = "desc"
        else:
            current_order = "asc"
        # end if
        if (not php_empty(lambda : columns["cb"])):
            cb_counter = 1
            columns["cb"] = "<label class=\"screen-reader-text\" for=\"cb-select-all-" + cb_counter + "\">" + __("Select All") + "</label>" + "<input id=\"cb-select-all-" + cb_counter + "\" type=\"checkbox\" />"
            cb_counter += 1
        # end if
        for column_key,column_display_name in columns:
            class_ = Array("manage-column", str("column-") + str(column_key))
            if php_in_array(column_key, hidden):
                class_[-1] = "hidden"
            # end if
            if "cb" == column_key:
                class_[-1] = "check-column"
            elif php_in_array(column_key, Array("posts", "comments", "links")):
                class_[-1] = "num"
            # end if
            if column_key == primary:
                class_[-1] = "column-primary"
            # end if
            if (php_isset(lambda : sortable[column_key])):
                orderby, desc_first = sortable[column_key]
                if current_orderby == orderby:
                    order = "desc" if "asc" == current_order else "asc"
                    class_[-1] = "sorted"
                    class_[-1] = current_order
                else:
                    order = "desc" if desc_first else "asc"
                    class_[-1] = "sortable"
                    class_[-1] = "asc" if desc_first else "desc"
                # end if
                column_display_name = "<a href=\"" + esc_url(add_query_arg(compact("orderby", "order"), current_url)) + "\"><span>" + column_display_name + "</span><span class=\"sorting-indicator\"></span></a>"
            # end if
            tag = "td" if "cb" == column_key else "th"
            scope = "scope=\"col\"" if "th" == tag else ""
            id = str("id='") + str(column_key) + str("'") if with_id else ""
            if (not php_empty(lambda : class_)):
                class_ = "class='" + join(" ", class_) + "'"
            # end if
            php_print(str("<") + str(tag) + str(" ") + str(scope) + str(" ") + str(id) + str(" ") + str(class_) + str(">") + str(column_display_name) + str("</") + str(tag) + str(">"))
        # end for
    # end def print_column_headers
    #// 
    #// Displays the table.
    #// 
    #// @since 3.1.0
    #//
    def display(self):
        
        singular = self._args["singular"]
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
        if singular:
            php_print(str(" data-wp-lists='list:") + str(singular) + str("'"))
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
    def display_tablenav(self, which=None):
        
        if "top" == which:
            wp_nonce_field("bulk-" + self._args["plural"])
        # end if
        php_print(" <div class=\"tablenav ")
        php_print(esc_attr(which))
        php_print("\">\n\n      ")
        if self.has_items():
            php_print("     <div class=\"alignleft actions bulkactions\">\n         ")
            self.bulk_actions(which)
            php_print("     </div>\n            ")
        # end if
        self.extra_tablenav(which)
        self.pagination(which)
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
    def extra_tablenav(self, which=None):
        
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
        
        for item in self.items:
            self.single_row(item)
        # end for
    # end def display_rows
    #// 
    #// Generates content for a single row of the table
    #// 
    #// @since 3.1.0
    #// 
    #// @param object $item The current item
    #//
    def single_row(self, item=None):
        
        php_print("<tr>")
        self.single_row_columns(item)
        php_print("</tr>")
    # end def single_row
    #// 
    #// @param object $item
    #// @param string $column_name
    #//
    def column_default(self, item=None, column_name=None):
        
        pass
    # end def column_default
    #// 
    #// @param object $item
    #//
    def column_cb(self, item=None):
        
        pass
    # end def column_cb
    #// 
    #// Generates the columns for a single row of the table
    #// 
    #// @since 3.1.0
    #// 
    #// @param object $item The current item
    #//
    def single_row_columns(self, item=None):
        
        columns, hidden, sortable, primary = self.get_column_info()
        for column_name,column_display_name in columns:
            classes = str(column_name) + str(" column-") + str(column_name)
            if primary == column_name:
                classes += " has-row-actions column-primary"
            # end if
            if php_in_array(column_name, hidden):
                classes += " hidden"
            # end if
            #// Comments column uses HTML in the display name with screen reader text.
            #// Instead of using esc_attr(), we strip tags to get closer to a user-friendly string.
            data = "data-colname=\"" + wp_strip_all_tags(column_display_name) + "\""
            attributes = str("class='") + str(classes) + str("' ") + str(data)
            if "cb" == column_name:
                php_print("<th scope=\"row\" class=\"check-column\">")
                php_print(self.column_cb(item))
                php_print("</th>")
            elif php_method_exists(self, "_column_" + column_name):
                php_print(php_call_user_func(Array(self, "_column_" + column_name), item, classes, data, primary))
            elif php_method_exists(self, "column_" + column_name):
                php_print(str("<td ") + str(attributes) + str(">"))
                php_print(php_call_user_func(Array(self, "column_" + column_name), item))
                php_print(self.handle_row_actions(item, column_name, primary))
                php_print("</td>")
            else:
                php_print(str("<td ") + str(attributes) + str(">"))
                php_print(self.column_default(item, column_name))
                php_print(self.handle_row_actions(item, column_name, primary))
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
    def handle_row_actions(self, item=None, column_name=None, primary=None):
        
        return "<button type=\"button\" class=\"toggle-row\"><span class=\"screen-reader-text\">" + __("Show more details") + "</span></button>" if column_name == primary else ""
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
        rows = ob_get_clean()
        response = Array({"rows": rows})
        if (php_isset(lambda : self._pagination_args["total_items"])):
            response["total_items_i18n"] = php_sprintf(_n("%s item", "%s items", self._pagination_args["total_items"]), number_format_i18n(self._pagination_args["total_items"]))
        # end if
        if (php_isset(lambda : self._pagination_args["total_pages"])):
            response["total_pages"] = self._pagination_args["total_pages"]
            response["total_pages_i18n"] = number_format_i18n(self._pagination_args["total_pages"])
        # end if
        php_print(wp_json_encode(response))
        php_exit()
    # end def ajax_response
    #// 
    #// Send required variables to JavaScript land
    #//
    def _js_vars(self):
        
        args = Array({"class": get_class(self), "screen": Array({"id": self.screen.id, "base": self.screen.base})})
        printf("<script type='text/javascript'>list_args = %s;</script>\n", wp_json_encode(args))
    # end def _js_vars
# end class WP_List_Table
