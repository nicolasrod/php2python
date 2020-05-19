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
#// List Table API: WP_Posts_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying posts in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Posts_List_Table(WP_List_Table):
    #// 
    #// Whether the items should be displayed hierarchically or linearly.
    #// 
    #// @since 3.1.0
    #// @var bool
    #//
    hierarchical_display = Array()
    #// 
    #// Holds the number of pending comments for each post.
    #// 
    #// @since 3.1.0
    #// @var array
    #//
    comment_pending_count = Array()
    #// 
    #// Holds the number of posts for this user.
    #// 
    #// @since 3.1.0
    #// @var int
    #//
    user_posts_count = Array()
    #// 
    #// Holds the number of posts which are sticky.
    #// 
    #// @since 3.1.0
    #// @var int
    #//
    sticky_posts_count = 0
    is_trash = Array()
    #// 
    #// Current level for output.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    current_level = 0
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @see WP_List_Table::__construct() for more information on default arguments.
    #// 
    #// @global WP_Post_Type $post_type_object
    #// @global wpdb         $wpdb             WordPress database abstraction object.
    #// 
    #// @param array $args An associative array of arguments.
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        global PHP_REQUEST
        global post_type_object_
        global wpdb_
        php_check_if_defined("post_type_object_","wpdb_")
        super().__init__(Array({"plural": "posts", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
        post_type_ = self.screen.post_type
        post_type_object_ = get_post_type_object(post_type_)
        exclude_states_ = get_post_stati(Array({"show_in_admin_all_list": False}))
        self.user_posts_count = php_intval(wpdb_.get_var(wpdb_.prepare(str("\n          SELECT COUNT( 1 )\n         FROM ") + str(wpdb_.posts) + str("\n            WHERE post_type = %s\n          AND post_status NOT IN ( '") + php_implode("','", exclude_states_) + "' )\n         AND post_author = %d\n      ", post_type_, get_current_user_id())))
        if self.user_posts_count and (not current_user_can(post_type_object_.cap.edit_others_posts)) and php_empty(lambda : PHP_REQUEST["post_status"]) and php_empty(lambda : PHP_REQUEST["all_posts"]) and php_empty(lambda : PHP_REQUEST["author"]) and php_empty(lambda : PHP_REQUEST["show_sticky"]):
            PHP_REQUEST["author"] = get_current_user_id()
        # end if
        sticky_posts_ = get_option("sticky_posts")
        if "post" == post_type_ and sticky_posts_:
            sticky_posts_ = php_implode(", ", php_array_map("absint", sticky_posts_))
            self.sticky_posts_count = wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT( 1 ) FROM ") + str(wpdb_.posts) + str(" WHERE post_type = %s AND post_status NOT IN ('trash', 'auto-draft') AND ID IN (") + str(sticky_posts_) + str(")"), post_type_))
        # end if
    # end def __init__
    #// 
    #// Sets whether the table layout should be hierarchical or not.
    #// 
    #// @since 4.2.0
    #// 
    #// @param bool $display Whether the table layout should be hierarchical.
    #//
    def set_hierarchical_display(self, display_=None):
        
        
        self.hierarchical_display = display_
    # end def set_hierarchical_display
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        
        return current_user_can(get_post_type_object(self.screen.post_type).cap.edit_posts)
    # end def ajax_user_can
    #// 
    #// @global array    $avail_post_stati
    #// @global WP_Query $wp_query         WordPress Query object.
    #// @global int      $per_page
    #// @global string   $mode
    #//
    def prepare_items(self):
        
        
        global avail_post_stati_
        global wp_query_
        global per_page_
        global mode_
        php_check_if_defined("avail_post_stati_","wp_query_","per_page_","mode_")
        #// Is going to call wp().
        avail_post_stati_ = wp_edit_posts_query()
        self.set_hierarchical_display(is_post_type_hierarchical(self.screen.post_type) and "menu_order title" == wp_query_.query["orderby"])
        post_type_ = self.screen.post_type
        per_page_ = self.get_items_per_page("edit_" + post_type_ + "_per_page")
        #// This filter is documented in wp-admin/includes/post.php
        per_page_ = apply_filters("edit_posts_per_page", per_page_, post_type_)
        if self.hierarchical_display:
            total_items_ = wp_query_.post_count
        elif wp_query_.found_posts or self.get_pagenum() == 1:
            total_items_ = wp_query_.found_posts
        else:
            post_counts_ = wp_count_posts(post_type_, "readable")
            if (php_isset(lambda : PHP_REQUEST["post_status"])) and php_in_array(PHP_REQUEST["post_status"], avail_post_stati_):
                total_items_ = post_counts_[PHP_REQUEST["post_status"]]
            elif (php_isset(lambda : PHP_REQUEST["show_sticky"])) and PHP_REQUEST["show_sticky"]:
                total_items_ = self.sticky_posts_count
            elif (php_isset(lambda : PHP_REQUEST["author"])) and get_current_user_id() == PHP_REQUEST["author"]:
                total_items_ = self.user_posts_count
            else:
                total_items_ = array_sum(post_counts_)
                #// Subtract post types that are not included in the admin all list.
                for state_ in get_post_stati(Array({"show_in_admin_all_list": False})):
                    total_items_ -= post_counts_[state_]
                # end for
            # end if
        # end if
        if (not php_empty(lambda : PHP_REQUEST["mode"])):
            mode_ = "excerpt" if "excerpt" == PHP_REQUEST["mode"] else "list"
            set_user_setting("posts_list_mode", mode_)
        else:
            mode_ = get_user_setting("posts_list_mode", "list")
        # end if
        self.is_trash = (php_isset(lambda : PHP_REQUEST["post_status"])) and "trash" == PHP_REQUEST["post_status"]
        self.set_pagination_args(Array({"total_items": total_items_, "per_page": per_page_}))
    # end def prepare_items
    #// 
    #// @return bool
    #//
    def has_items(self):
        
        
        return have_posts()
    # end def has_items
    #// 
    #//
    def no_items(self):
        
        
        if (php_isset(lambda : PHP_REQUEST["post_status"])) and "trash" == PHP_REQUEST["post_status"]:
            php_print(get_post_type_object(self.screen.post_type).labels.not_found_in_trash)
        else:
            php_print(get_post_type_object(self.screen.post_type).labels.not_found)
        # end if
    # end def no_items
    #// 
    #// Determine if the current view is the "All" view.
    #// 
    #// @since 4.2.0
    #// 
    #// @return bool Whether the current view is the "All" view.
    #//
    def is_base_request(self):
        
        
        vars_ = PHP_REQUEST
        vars_["paged"] = None
        if php_empty(lambda : vars_):
            return True
        elif 1 == php_count(vars_) and (not php_empty(lambda : vars_["post_type"])):
            return self.screen.post_type == vars_["post_type"]
        # end if
        return 1 == php_count(vars_) and (not php_empty(lambda : vars_["mode"]))
    # end def is_base_request
    #// 
    #// Helper to create links to edit.php with params.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string[] $args  Associative array of URL parameters for the link.
    #// @param string   $label Link text.
    #// @param string   $class Optional. Class attribute. Default empty string.
    #// @return string The formatted link string.
    #//
    def get_edit_link(self, args_=None, label_=None, class_=""):
        
        
        url_ = add_query_arg(args_, "edit.php")
        class_html_ = ""
        aria_current_ = ""
        if (not php_empty(lambda : class_)):
            class_html_ = php_sprintf(" class=\"%s\"", esc_attr(class_))
            if "current" == class_:
                aria_current_ = " aria-current=\"page\""
            # end if
        # end if
        return php_sprintf("<a href=\"%s\"%s%s>%s</a>", esc_url(url_), class_html_, aria_current_, label_)
    # end def get_edit_link
    #// 
    #// @global array $locked_post_status This seems to be deprecated.
    #// @global array $avail_post_stati
    #// @return array
    #//
    def get_views(self):
        
        
        global locked_post_status_
        global avail_post_stati_
        php_check_if_defined("locked_post_status_","avail_post_stati_")
        post_type_ = self.screen.post_type
        if (not php_empty(lambda : locked_post_status_)):
            return Array()
        # end if
        status_links_ = Array()
        num_posts_ = wp_count_posts(post_type_, "readable")
        total_posts_ = array_sum(num_posts_)
        class_ = ""
        current_user_id_ = get_current_user_id()
        all_args_ = Array({"post_type": post_type_})
        mine_ = ""
        #// Subtract post types that are not included in the admin all list.
        for state_ in get_post_stati(Array({"show_in_admin_all_list": False})):
            total_posts_ -= num_posts_.state_
        # end for
        if self.user_posts_count and self.user_posts_count != total_posts_:
            if (php_isset(lambda : PHP_REQUEST["author"])) and PHP_REQUEST["author"] == current_user_id_:
                class_ = "current"
            # end if
            mine_args_ = Array({"post_type": post_type_, "author": current_user_id_})
            mine_inner_html_ = php_sprintf(_nx("Mine <span class=\"count\">(%s)</span>", "Mine <span class=\"count\">(%s)</span>", self.user_posts_count, "posts"), number_format_i18n(self.user_posts_count))
            mine_ = self.get_edit_link(mine_args_, mine_inner_html_, class_)
            all_args_["all_posts"] = 1
            class_ = ""
        # end if
        if php_empty(lambda : class_) and self.is_base_request() or (php_isset(lambda : PHP_REQUEST["all_posts"])):
            class_ = "current"
        # end if
        all_inner_html_ = php_sprintf(_nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", total_posts_, "posts"), number_format_i18n(total_posts_))
        status_links_["all"] = self.get_edit_link(all_args_, all_inner_html_, class_)
        if mine_:
            status_links_["mine"] = mine_
        # end if
        for status_ in get_post_stati(Array({"show_in_admin_status_list": True}), "objects"):
            class_ = ""
            status_name_ = status_.name
            if (not php_in_array(status_name_, avail_post_stati_)) or php_empty(lambda : num_posts_.status_name_):
                continue
            # end if
            if (php_isset(lambda : PHP_REQUEST["post_status"])) and status_name_ == PHP_REQUEST["post_status"]:
                class_ = "current"
            # end if
            status_args_ = Array({"post_status": status_name_, "post_type": post_type_})
            status_label_ = php_sprintf(translate_nooped_plural(status_.label_count, num_posts_.status_name_), number_format_i18n(num_posts_.status_name_))
            status_links_[status_name_] = self.get_edit_link(status_args_, status_label_, class_)
        # end for
        if (not php_empty(lambda : self.sticky_posts_count)):
            class_ = "current" if (not php_empty(lambda : PHP_REQUEST["show_sticky"])) else ""
            sticky_args_ = Array({"post_type": post_type_, "show_sticky": 1})
            sticky_inner_html_ = php_sprintf(_nx("Sticky <span class=\"count\">(%s)</span>", "Sticky <span class=\"count\">(%s)</span>", self.sticky_posts_count, "posts"), number_format_i18n(self.sticky_posts_count))
            sticky_link_ = Array({"sticky": self.get_edit_link(sticky_args_, sticky_inner_html_, class_)})
            #// Sticky comes after Publish, or if not listed, after All.
            split_ = 1 + php_array_search("publish" if (php_isset(lambda : status_links_["publish"])) else "all", php_array_keys(status_links_))
            status_links_ = php_array_merge(php_array_slice(status_links_, 0, split_), sticky_link_, php_array_slice(status_links_, split_))
        # end if
        return status_links_
    # end def get_views
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        actions_ = Array()
        post_type_obj_ = get_post_type_object(self.screen.post_type)
        if current_user_can(post_type_obj_.cap.edit_posts):
            if self.is_trash:
                actions_["untrash"] = __("Restore")
            else:
                actions_["edit"] = __("Edit")
            # end if
        # end if
        if current_user_can(post_type_obj_.cap.delete_posts):
            if self.is_trash or (not EMPTY_TRASH_DAYS):
                actions_["delete"] = __("Delete Permanently")
            else:
                actions_["trash"] = __("Move to Trash")
            # end if
        # end if
        return actions_
    # end def get_bulk_actions
    #// 
    #// Displays a categories drop-down for filtering on the Posts list table.
    #// 
    #// @since 4.6.0
    #// 
    #// @global int $cat Currently selected category.
    #// 
    #// @param string $post_type Post type slug.
    #//
    def categories_dropdown(self, post_type_=None):
        
        
        global cat_
        php_check_if_defined("cat_")
        #// 
        #// Filters whether to remove the 'Categories' drop-down from the post list table.
        #// 
        #// @since 4.6.0
        #// 
        #// @param bool   $disable   Whether to disable the categories drop-down. Default false.
        #// @param string $post_type Post type slug.
        #//
        if False != apply_filters("disable_categories_dropdown", False, post_type_):
            return
        # end if
        if is_object_in_taxonomy(post_type_, "category"):
            dropdown_options_ = Array({"show_option_all": get_taxonomy("category").labels.all_items, "hide_empty": 0, "hierarchical": 1, "show_count": 0, "orderby": "name", "selected": cat_})
            php_print("<label class=\"screen-reader-text\" for=\"cat\">" + __("Filter by category") + "</label>")
            wp_dropdown_categories(dropdown_options_)
        # end if
    # end def categories_dropdown
    #// 
    #// Displays a formats drop-down for filtering items.
    #// 
    #// @since 5.2.0
    #// @access protected
    #// 
    #// @param string $post_type Post type key.
    #//
    def formats_dropdown(self, post_type_=None):
        
        
        #// 
        #// Filters whether to remove the 'Formats' drop-down from the post list table.
        #// 
        #// @since 5.2.0
        #// 
        #// @param bool $disable Whether to disable the drop-down. Default false.
        #//
        if apply_filters("disable_formats_dropdown", False):
            return
        # end if
        #// Make sure the dropdown shows only formats with a post count greater than 0.
        used_post_formats_ = get_terms(Array({"taxonomy": "post_format", "hide_empty": True}))
        #// 
        #// Return if the post type doesn't have post formats, or there are no posts using formats,
        #// or if we're in the Trash.
        #//
        if (not is_object_in_taxonomy(post_type_, "post_format")) or (not used_post_formats_) or self.is_trash:
            return
        # end if
        displayed_post_format_ = PHP_REQUEST["post_format"] if (php_isset(lambda : PHP_REQUEST["post_format"])) else ""
        php_print("     <label for=\"filter-by-format\" class=\"screen-reader-text\">")
        _e("Filter by post format")
        php_print("</label>\n       <select name=\"post_format\" id=\"filter-by-format\">\n         <option")
        selected(displayed_post_format_, "")
        php_print(" value=\"\">")
        _e("All formats")
        php_print("</option>\n          ")
        for used_post_format_ in used_post_formats_:
            #// Post format slug.
            slug_ = php_str_replace("post-format-", "", used_post_format_.slug)
            #// Pretty, translated version of the post format slug.
            pretty_name_ = get_post_format_string(slug_)
            #// Skip the standard post format.
            if "standard" == slug_:
                continue
            # end if
            php_print("             <option")
            selected(displayed_post_format_, slug_)
            php_print(" value=\"")
            php_print(esc_attr(slug_))
            php_print("\">")
            php_print(esc_html(pretty_name_))
            php_print("</option>\n              ")
        # end for
        php_print("     </select>\n     ")
    # end def formats_dropdown
    #// 
    #// @param string $which
    #//
    def extra_tablenav(self, which_=None):
        
        
        php_print("     <div class=\"alignleft actions\">\n     ")
        if "top" == which_ and (not is_singular()):
            ob_start()
            self.months_dropdown(self.screen.post_type)
            self.categories_dropdown(self.screen.post_type)
            self.formats_dropdown(self.screen.post_type)
            #// 
            #// Fires before the Filter button on the Posts and Pages list tables.
            #// 
            #// The Filter button allows sorting by date and/or category on the
            #// Posts list table, and sorting by date on the Pages list table.
            #// 
            #// @since 2.1.0
            #// @since 4.4.0 The `$post_type` parameter was added.
            #// @since 4.6.0 The `$which` parameter was added.
            #// 
            #// @param string $post_type The post type slug.
            #// @param string $which     The location of the extra table nav markup:
            #// 'top' or 'bottom' for WP_Posts_List_Table,
            #// 'bar' for WP_Media_List_Table.
            #//
            do_action("restrict_manage_posts", self.screen.post_type, which_)
            output_ = ob_get_clean()
            if (not php_empty(lambda : output_)):
                php_print(output_)
                submit_button(__("Filter"), "", "filter_action", False, Array({"id": "post-query-submit"}))
            # end if
        # end if
        if self.is_trash and current_user_can(get_post_type_object(self.screen.post_type).cap.edit_others_posts) and self.has_items():
            submit_button(__("Empty Trash"), "apply", "delete_all", False)
        # end if
        php_print("     </div>\n        ")
        #// 
        #// Fires immediately following the closing "actions" div in the tablenav for the posts
        #// list table.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $which The location of the extra table nav markup: 'top' or 'bottom'.
        #//
        do_action("manage_posts_extra_tablenav", which_)
    # end def extra_tablenav
    #// 
    #// @return string
    #//
    def current_action(self):
        
        
        if (php_isset(lambda : PHP_REQUEST["delete_all"])) or (php_isset(lambda : PHP_REQUEST["delete_all2"])):
            return "delete_all"
        # end if
        return super().current_action()
    # end def current_action
    #// 
    #// @return array
    #//
    def get_table_classes(self):
        
        
        return Array("widefat", "fixed", "striped", "pages" if is_post_type_hierarchical(self.screen.post_type) else "posts")
    # end def get_table_classes
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        post_type_ = self.screen.post_type
        posts_columns_ = Array()
        posts_columns_["cb"] = "<input type=\"checkbox\" />"
        #// translators: Posts screen column name.
        posts_columns_["title"] = _x("Title", "column name")
        if post_type_supports(post_type_, "author"):
            posts_columns_["author"] = __("Author")
        # end if
        taxonomies_ = get_object_taxonomies(post_type_, "objects")
        taxonomies_ = wp_filter_object_list(taxonomies_, Array({"show_admin_column": True}), "and", "name")
        #// 
        #// Filters the taxonomy columns in the Posts list table.
        #// 
        #// The dynamic portion of the hook name, `$post_type`, refers to the post
        #// type slug.
        #// 
        #// @since 3.5.0
        #// 
        #// @param string[] $taxonomies Array of taxonomy names to show columns for.
        #// @param string   $post_type  The post type.
        #//
        taxonomies_ = apply_filters(str("manage_taxonomies_for_") + str(post_type_) + str("_columns"), taxonomies_, post_type_)
        taxonomies_ = php_array_filter(taxonomies_, "taxonomy_exists")
        for taxonomy_ in taxonomies_:
            if "category" == taxonomy_:
                column_key_ = "categories"
            elif "post_tag" == taxonomy_:
                column_key_ = "tags"
            else:
                column_key_ = "taxonomy-" + taxonomy_
            # end if
            posts_columns_[column_key_] = get_taxonomy(taxonomy_).labels.name
        # end for
        post_status_ = PHP_REQUEST["post_status"] if (not php_empty(lambda : PHP_REQUEST["post_status"])) else "all"
        if post_type_supports(post_type_, "comments") and (not php_in_array(post_status_, Array("pending", "draft", "future"))):
            posts_columns_["comments"] = "<span class=\"vers comment-grey-bubble\" title=\"" + esc_attr__("Comments") + "\"><span class=\"screen-reader-text\">" + __("Comments") + "</span></span>"
        # end if
        posts_columns_["date"] = __("Date")
        if "page" == post_type_:
            #// 
            #// Filters the columns displayed in the Pages list table.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string[] $post_columns An associative array of column headings.
            #//
            posts_columns_ = apply_filters("manage_pages_columns", posts_columns_)
        else:
            #// 
            #// Filters the columns displayed in the Posts list table.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string[] $post_columns An associative array of column headings.
            #// @param string   $post_type    The post type slug.
            #//
            posts_columns_ = apply_filters("manage_posts_columns", posts_columns_, post_type_)
        # end if
        #// 
        #// Filters the columns displayed in the Posts list table for a specific post type.
        #// 
        #// The dynamic portion of the hook name, `$post_type`, refers to the post type slug.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $post_columns An associative array of column headings.
        #//
        return apply_filters(str("manage_") + str(post_type_) + str("_posts_columns"), posts_columns_)
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        
        return Array({"title": "title", "parent": "parent", "comments": "comment_count", "date": Array("date", True)})
    # end def get_sortable_columns
    #// 
    #// @global WP_Query $wp_query WordPress Query object.
    #// @global int $per_page
    #// @param array $posts
    #// @param int $level
    #//
    def display_rows(self, posts_=None, level_=0):
        if posts_ is None:
            posts_ = Array()
        # end if
        
        global wp_query_
        global per_page_
        php_check_if_defined("wp_query_","per_page_")
        if php_empty(lambda : posts_):
            posts_ = wp_query_.posts
        # end if
        add_filter("the_title", "esc_html")
        if self.hierarchical_display:
            self._display_rows_hierarchical(posts_, self.get_pagenum(), per_page_)
        else:
            self._display_rows(posts_, level_)
        # end if
    # end def display_rows
    #// 
    #// @param array $posts
    #// @param int $level
    #//
    def _display_rows(self, posts_=None, level_=0):
        
        
        post_type_ = self.screen.post_type
        #// Create array of post IDs.
        post_ids_ = Array()
        for a_post_ in posts_:
            post_ids_[-1] = a_post_.ID
        # end for
        if post_type_supports(post_type_, "comments"):
            self.comment_pending_count = get_pending_comments_num(post_ids_)
        # end if
        for post_ in posts_:
            self.single_row(post_, level_)
        # end for
    # end def _display_rows
    #// 
    #// @global wpdb    $wpdb WordPress database abstraction object.
    #// @global WP_Post $post Global post object.
    #// @param array $pages
    #// @param int $pagenum
    #// @param int $per_page
    #//
    def _display_rows_hierarchical(self, pages_=None, pagenum_=1, per_page_=20):
        
        global PHP_GLOBALS
        global wpdb_
        php_check_if_defined("wpdb_")
        level_ = 0
        if (not pages_):
            pages_ = get_pages(Array({"sort_column": "menu_order"}))
            if (not pages_):
                return
            # end if
        # end if
        #// 
        #// Arrange pages into two parts: top level pages and children_pages
        #// children_pages is two dimensional array, eg.
        #// children_pages[10][] contains all sub-pages whose parent is 10.
        #// It only takes O( N ) to arrange this and it takes O( 1 ) for subsequent lookup operations
        #// If searching, ignore hierarchy and treat everything as top level
        #//
        if php_empty(lambda : PHP_REQUEST["s"]):
            top_level_pages_ = Array()
            children_pages_ = Array()
            for page_ in pages_:
                #// Catch and repair bad pages.
                if page_.post_parent == page_.ID:
                    page_.post_parent = 0
                    wpdb_.update(wpdb_.posts, Array({"post_parent": 0}), Array({"ID": page_.ID}))
                    clean_post_cache(page_)
                # end if
                if 0 == page_.post_parent:
                    top_level_pages_[-1] = page_
                else:
                    children_pages_[page_.post_parent][-1] = page_
                # end if
            # end for
            pages_ = top_level_pages_
        # end if
        count_ = 0
        start_ = pagenum_ - 1 * per_page_
        end_ = start_ + per_page_
        to_display_ = Array()
        for page_ in pages_:
            if count_ >= end_:
                break
            # end if
            if count_ >= start_:
                to_display_[page_.ID] = level_
            # end if
            count_ += 1
            if (php_isset(lambda : children_pages_)):
                self._page_rows(children_pages_, count_, page_.ID, level_ + 1, pagenum_, per_page_, to_display_)
            # end if
        # end for
        #// If it is the last pagenum and there are orphaned pages, display them with paging as well.
        if (php_isset(lambda : children_pages_)) and count_ < end_:
            for orphans_ in children_pages_:
                for op_ in orphans_:
                    if count_ >= end_:
                        break
                    # end if
                    if count_ >= start_:
                        to_display_[op_.ID] = 0
                    # end if
                    count_ += 1
                # end for
            # end for
        # end if
        ids_ = php_array_keys(to_display_)
        _prime_post_caches(ids_)
        if (not (php_isset(lambda : PHP_GLOBALS["post"]))):
            PHP_GLOBALS["post"] = reset(ids_)
        # end if
        for page_id_,level_ in to_display_.items():
            php_print(" ")
            self.single_row(page_id_, level_)
        # end for
    # end def _display_rows_hierarchical
    #// 
    #// Given a top level page ID, display the nested hierarchy of sub-pages
    #// together with paging support
    #// 
    #// @since 3.1.0 (Standalone function exists since 2.6.0)
    #// @since 4.2.0 Added the `$to_display` parameter.
    #// 
    #// @param array $children_pages
    #// @param int $count
    #// @param int $parent
    #// @param int $level
    #// @param int $pagenum
    #// @param int $per_page
    #// @param array $to_display List of pages to be displayed. Passed by reference.
    #//
    def _page_rows(self, children_pages_=None, count_=None, parent_=None, level_=None, pagenum_=None, per_page_=None, to_display_=None):
        
        
        if (not (php_isset(lambda : children_pages_[parent_]))):
            return
        # end if
        start_ = pagenum_ - 1 * per_page_
        end_ = start_ + per_page_
        for page_ in children_pages_[parent_]:
            if count_ >= end_:
                break
            # end if
            #// If the page starts in a subtree, print the parents.
            if count_ == start_ and page_.post_parent > 0:
                my_parents_ = Array()
                my_parent_ = page_.post_parent
                while True:
                    
                    if not (my_parent_):
                        break
                    # end if
                    #// Get the ID from the list or the attribute if my_parent is an object.
                    parent_id_ = my_parent_
                    if php_is_object(my_parent_):
                        parent_id_ = my_parent_.ID
                    # end if
                    my_parent_ = get_post(parent_id_)
                    my_parents_[-1] = my_parent_
                    if (not my_parent_.post_parent):
                        break
                    # end if
                    my_parent_ = my_parent_.post_parent
                # end while
                num_parents_ = php_count(my_parents_)
                while True:
                    my_parent_ = php_array_pop(my_parents_)
                    if not (my_parent_):
                        break
                    # end if
                    to_display_[my_parent_.ID] = level_ - num_parents_
                    num_parents_ -= 1
                # end while
            # end if
            if count_ >= start_:
                to_display_[page_.ID] = level_
            # end if
            count_ += 1
            self._page_rows(children_pages_, count_, page_.ID, level_ + 1, pagenum_, per_page_, to_display_)
        # end for
        children_pages_[parent_] = None
        pass
    # end def _page_rows
    #// 
    #// Handles the checkbox column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_cb(self, post_=None):
        
        
        if current_user_can("edit_post", post_.ID):
            php_print("         <label class=\"screen-reader-text\" for=\"cb-select-")
            the_ID()
            php_print("\">\n                ")
            #// translators: %s: Post title.
            printf(__("Select %s"), _draft_or_post_title())
            php_print("         </label>\n          <input id=\"cb-select-")
            the_ID()
            php_print("\" type=\"checkbox\" name=\"post[]\" value=\"")
            the_ID()
            php_print("""\" />
            <div class=\"locked-indicator\">
            <span class=\"locked-indicator-icon\" aria-hidden=\"true\"></span>
            <span class=\"screen-reader-text\">
            """)
            printf(__("&#8220;%s&#8221; is locked"), _draft_or_post_title())
            php_print("             </span>\n           </div>\n            ")
        # end if
    # end def column_cb
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post
    #// @param string  $classes
    #// @param string  $data
    #// @param string  $primary
    #//
    def _column_title(self, post_=None, classes_=None, data_=None, primary_=None):
        
        
        php_print("<td class=\"" + classes_ + " page-title\" ", data_, ">")
        php_print(self.column_title(post_))
        php_print(self.handle_row_actions(post_, "title", primary_))
        php_print("</td>")
    # end def _column_title
    #// 
    #// Handles the title column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_title(self, post_=None):
        
        
        global mode_
        php_check_if_defined("mode_")
        if self.hierarchical_display:
            if 0 == self.current_level and php_int(post_.post_parent) > 0:
                #// Sent level 0 by accident, by default, or because we don't know the actual level.
                find_main_page_ = php_int(post_.post_parent)
                while True:
                    
                    if not (find_main_page_ > 0):
                        break
                    # end if
                    parent_ = get_post(find_main_page_)
                    if php_is_null(parent_):
                        break
                    # end if
                    self.current_level += 1
                    find_main_page_ = php_int(parent_.post_parent)
                    if (not (php_isset(lambda : parent_name_))):
                        #// This filter is documented in wp-includes/post-template.php
                        parent_name_ = apply_filters("the_title", parent_.post_title, parent_.ID)
                    # end if
                # end while
            # end if
        # end if
        can_edit_post_ = current_user_can("edit_post", post_.ID)
        if can_edit_post_ and "trash" != post_.post_status:
            lock_holder_ = wp_check_post_lock(post_.ID)
            if lock_holder_:
                lock_holder_ = get_userdata(lock_holder_)
                locked_avatar_ = get_avatar(lock_holder_.ID, 18)
                #// translators: %s: User's display name.
                locked_text_ = esc_html(php_sprintf(__("%s is currently editing"), lock_holder_.display_name))
            else:
                locked_avatar_ = ""
                locked_text_ = ""
            # end if
            php_print("<div class=\"locked-info\"><span class=\"locked-avatar\">" + locked_avatar_ + "</span> <span class=\"locked-text\">" + locked_text_ + "</span></div>\n")
        # end if
        pad_ = php_str_repeat("&#8212; ", self.current_level)
        php_print("<strong>")
        title_ = _draft_or_post_title()
        if can_edit_post_ and "trash" != post_.post_status:
            printf("<a class=\"row-title\" href=\"%s\" aria-label=\"%s\">%s%s</a>", get_edit_post_link(post_.ID), esc_attr(php_sprintf(__("&#8220;%s&#8221; (Edit)"), title_)), pad_, title_)
        else:
            printf("<span>%s%s</span>", pad_, title_)
        # end if
        _post_states(post_)
        if (php_isset(lambda : parent_name_)):
            post_type_object_ = get_post_type_object(post_.post_type)
            php_print(" | " + post_type_object_.labels.parent_item_colon + " " + esc_html(parent_name_))
        # end if
        php_print("</strong>\n")
        if (not is_post_type_hierarchical(self.screen.post_type)) and "excerpt" == mode_ and current_user_can("read_post", post_.ID):
            if post_password_required(post_):
                php_print("<span class=\"protected-post-excerpt\">" + esc_html(get_the_excerpt()) + "</span>")
            else:
                php_print(esc_html(get_the_excerpt()))
            # end if
        # end if
        get_inline_data(post_)
    # end def column_title
    #// 
    #// Handles the post date column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $mode List table view mode.
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_date(self, post_=None):
        
        
        global mode_
        php_check_if_defined("mode_")
        if "0000-00-00 00:00:00" == post_.post_date:
            t_time_ = __("Unpublished")
            h_time_ = t_time_
            time_diff_ = 0
        else:
            t_time_ = get_the_time(__("Y/m/d g:i:s a"), post_)
            time_ = get_post_timestamp(post_)
            time_diff_ = time() - time_
            if time_ and time_diff_ > 0 and time_diff_ < DAY_IN_SECONDS:
                #// translators: %s: Human-readable time difference.
                h_time_ = php_sprintf(__("%s ago"), human_time_diff(time_))
            else:
                h_time_ = get_the_time(__("Y/m/d"), post_)
            # end if
        # end if
        if "publish" == post_.post_status:
            status_ = __("Published")
        elif "future" == post_.post_status:
            if time_diff_ > 0:
                status_ = "<strong class=\"error-message\">" + __("Missed schedule") + "</strong>"
            else:
                status_ = __("Scheduled")
            # end if
        else:
            status_ = __("Last Modified")
        # end if
        #// 
        #// Filters the status text of the post.
        #// 
        #// @since 4.8.0
        #// 
        #// @param string  $status      The status text.
        #// @param WP_Post $post        Post object.
        #// @param string  $column_name The column name.
        #// @param string  $mode        The list display mode ('excerpt' or 'list').
        #//
        status_ = apply_filters("post_date_column_status", status_, post_, "date", mode_)
        if status_:
            php_print(status_ + "<br />")
        # end if
        if "excerpt" == mode_:
            #// 
            #// Filters the published time of the post.
            #// 
            #// If `$mode` equals 'excerpt', the published time and date are both displayed.
            #// If `$mode` equals 'list' (default), the publish date is displayed, with the
            #// time and date together available as an abbreviation definition.
            #// 
            #// @since 2.5.1
            #// 
            #// @param string  $t_time      The published time.
            #// @param WP_Post $post        Post object.
            #// @param string  $column_name The column name.
            #// @param string  $mode        The list display mode ('excerpt' or 'list').
            #//
            php_print(apply_filters("post_date_column_time", t_time_, post_, "date", mode_))
        else:
            #// This filter is documented in wp-admin/includes/class-wp-posts-list-table.php
            php_print("<span title=\"" + t_time_ + "\">" + apply_filters("post_date_column_time", h_time_, post_, "date", mode_) + "</span>")
        # end if
    # end def column_date
    #// 
    #// Handles the comments column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_comments(self, post_=None):
        
        
        php_print("     <div class=\"post-com-count-wrapper\">\n        ")
        pending_comments_ = self.comment_pending_count[post_.ID] if (php_isset(lambda : self.comment_pending_count[post_.ID])) else 0
        self.comments_bubble(post_.ID, pending_comments_)
        php_print("     </div>\n        ")
    # end def column_comments
    #// 
    #// Handles the post author column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_author(self, post_=None):
        
        
        args_ = Array({"post_type": post_.post_type, "author": get_the_author_meta("ID")})
        php_print(self.get_edit_link(args_, get_the_author()))
    # end def column_author
    #// 
    #// Handles the default column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post        The current WP_Post object.
    #// @param string  $column_name The current column name.
    #//
    def column_default(self, post_=None, column_name_=None):
        
        
        if "categories" == column_name_:
            taxonomy_ = "category"
        elif "tags" == column_name_:
            taxonomy_ = "post_tag"
        elif 0 == php_strpos(column_name_, "taxonomy-"):
            taxonomy_ = php_substr(column_name_, 9)
        else:
            taxonomy_ = False
        # end if
        if taxonomy_:
            taxonomy_object_ = get_taxonomy(taxonomy_)
            terms_ = get_the_terms(post_.ID, taxonomy_)
            if php_is_array(terms_):
                term_links_ = Array()
                for t_ in terms_:
                    posts_in_term_qv_ = Array()
                    if "post" != post_.post_type:
                        posts_in_term_qv_["post_type"] = post_.post_type
                    # end if
                    if taxonomy_object_.query_var:
                        posts_in_term_qv_[taxonomy_object_.query_var] = t_.slug
                    else:
                        posts_in_term_qv_["taxonomy"] = taxonomy_
                        posts_in_term_qv_["term"] = t_.slug
                    # end if
                    label_ = esc_html(sanitize_term_field("name", t_.name, t_.term_id, taxonomy_, "display"))
                    term_links_[-1] = self.get_edit_link(posts_in_term_qv_, label_)
                # end for
                #// 
                #// Filters the links in `$taxonomy` column of edit.php.
                #// 
                #// @since 5.2.0
                #// 
                #// @param string[]  $term_links Array of term editing links.
                #// @param string    $taxonomy   Taxonomy name.
                #// @param WP_Term[] $terms      Array of term objects appearing in the post row.
                #//
                term_links_ = apply_filters("post_column_taxonomy_links", term_links_, taxonomy_, terms_)
                #// translators: Used between list items, there is a space after the comma.
                php_print(join(__(", "), term_links_))
            else:
                php_print("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">" + taxonomy_object_.labels.no_terms + "</span>")
            # end if
            return
        # end if
        if is_post_type_hierarchical(post_.post_type):
            #// 
            #// Fires in each custom column on the Posts list table.
            #// 
            #// This hook only fires if the current post type is hierarchical,
            #// such as pages.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string $column_name The name of the column to display.
            #// @param int    $post_id     The current post ID.
            #//
            do_action("manage_pages_custom_column", column_name_, post_.ID)
        else:
            #// 
            #// Fires in each custom column in the Posts list table.
            #// 
            #// This hook only fires if the current post type is non-hierarchical,
            #// such as posts.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string $column_name The name of the column to display.
            #// @param int    $post_id     The current post ID.
            #//
            do_action("manage_posts_custom_column", column_name_, post_.ID)
        # end if
        #// 
        #// Fires for each custom column of a specific post type in the Posts list table.
        #// 
        #// The dynamic portion of the hook name, `$post->post_type`, refers to the post type.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $column_name The name of the column to display.
        #// @param int    $post_id     The current post ID.
        #//
        do_action(str("manage_") + str(post_.post_type) + str("_posts_custom_column"), column_name_, post_.ID)
    # end def column_default
    #// 
    #// @global WP_Post $post Global post object.
    #// 
    #// @param int|WP_Post $post
    #// @param int         $level
    #//
    def single_row(self, post_=None, level_=0):
        
        global PHP_GLOBALS
        global_post_ = get_post()
        post_ = get_post(post_)
        self.current_level = level_
        PHP_GLOBALS["post"] = post_
        setup_postdata(post_)
        classes_ = "iedit author-" + "self" if get_current_user_id() == post_.post_author else "other"
        lock_holder_ = wp_check_post_lock(post_.ID)
        if lock_holder_:
            classes_ += " wp-locked"
        # end if
        if post_.post_parent:
            count_ = php_count(get_post_ancestors(post_.ID))
            classes_ += " level-" + count_
        else:
            classes_ += " level-0"
        # end if
        php_print("     <tr id=\"post-")
        php_print(post_.ID)
        php_print("\" class=\"")
        php_print(php_implode(" ", get_post_class(classes_, post_.ID)))
        php_print("\">\n            ")
        self.single_row_columns(post_)
        php_print("     </tr>\n     ")
        PHP_GLOBALS["post"] = global_post_
    # end def single_row
    #// 
    #// Gets the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, 'title'.
    #//
    def get_default_primary_column_name(self):
        
        
        return "title"
    # end def get_default_primary_column_name
    #// 
    #// Generates and displays row action links.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $post        Post being acted upon.
    #// @param string $column_name Current column name.
    #// @param string $primary     Primary column name.
    #// @return string Row actions output for posts, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, post_=None, column_name_=None, primary_=None):
        
        
        if primary_ != column_name_:
            return ""
        # end if
        post_type_object_ = get_post_type_object(post_.post_type)
        can_edit_post_ = current_user_can("edit_post", post_.ID)
        actions_ = Array()
        title_ = _draft_or_post_title()
        if can_edit_post_ and "trash" != post_.post_status:
            actions_["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_edit_post_link(post_.ID), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), title_)), __("Edit"))
            if "wp_block" != post_.post_type:
                actions_["inline hide-if-no-js"] = php_sprintf("<button type=\"button\" class=\"button-link editinline\" aria-label=\"%s\" aria-expanded=\"false\">%s</button>", esc_attr(php_sprintf(__("Quick edit &#8220;%s&#8221; inline"), title_)), __("Quick&nbsp;Edit"))
            # end if
        # end if
        if current_user_can("delete_post", post_.ID):
            if "trash" == post_.post_status:
                actions_["untrash"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", wp_nonce_url(admin_url(php_sprintf(post_type_object_._edit_link + "&amp;action=untrash", post_.ID)), "untrash-post_" + post_.ID), esc_attr(php_sprintf(__("Restore &#8220;%s&#8221; from the Trash"), title_)), __("Restore"))
            elif EMPTY_TRASH_DAYS:
                actions_["trash"] = php_sprintf("<a href=\"%s\" class=\"submitdelete\" aria-label=\"%s\">%s</a>", get_delete_post_link(post_.ID), esc_attr(php_sprintf(__("Move &#8220;%s&#8221; to the Trash"), title_)), _x("Trash", "verb"))
            # end if
            if "trash" == post_.post_status or (not EMPTY_TRASH_DAYS):
                actions_["delete"] = php_sprintf("<a href=\"%s\" class=\"submitdelete\" aria-label=\"%s\">%s</a>", get_delete_post_link(post_.ID, "", True), esc_attr(php_sprintf(__("Delete &#8220;%s&#8221; permanently"), title_)), __("Delete Permanently"))
            # end if
        # end if
        if is_post_type_viewable(post_type_object_):
            if php_in_array(post_.post_status, Array("pending", "draft", "future")):
                if can_edit_post_:
                    preview_link_ = get_preview_post_link(post_)
                    actions_["view"] = php_sprintf("<a href=\"%s\" rel=\"bookmark\" aria-label=\"%s\">%s</a>", esc_url(preview_link_), esc_attr(php_sprintf(__("Preview &#8220;%s&#8221;"), title_)), __("Preview"))
                # end if
            elif "trash" != post_.post_status:
                actions_["view"] = php_sprintf("<a href=\"%s\" rel=\"bookmark\" aria-label=\"%s\">%s</a>", get_permalink(post_.ID), esc_attr(php_sprintf(__("View &#8220;%s&#8221;"), title_)), __("View"))
            # end if
        # end if
        if "wp_block" == post_.post_type:
            actions_["export"] = php_sprintf("<button type=\"button\" class=\"wp-list-reusable-blocks__export button-link\" data-id=\"%s\" aria-label=\"%s\">%s</button>", post_.ID, esc_attr(php_sprintf(__("Export &#8220;%s&#8221; as JSON"), title_)), __("Export as JSON"))
        # end if
        if is_post_type_hierarchical(post_.post_type):
            #// 
            #// Filters the array of row action links on the Pages list table.
            #// 
            #// The filter is evaluated only for hierarchical post types.
            #// 
            #// @since 2.8.0
            #// 
            #// @param string[] $actions An array of row action links. Defaults are
            #// 'Edit', 'Quick Edit', 'Restore', 'Trash',
            #// 'Delete Permanently', 'Preview', and 'View'.
            #// @param WP_Post  $post    The post object.
            #//
            actions_ = apply_filters("page_row_actions", actions_, post_)
        else:
            #// 
            #// Filters the array of row action links on the Posts list table.
            #// 
            #// The filter is evaluated only for non-hierarchical post types.
            #// 
            #// @since 2.8.0
            #// 
            #// @param string[] $actions An array of row action links. Defaults are
            #// 'Edit', 'Quick Edit', 'Restore', 'Trash',
            #// 'Delete Permanently', 'Preview', and 'View'.
            #// @param WP_Post  $post    The post object.
            #//
            actions_ = apply_filters("post_row_actions", actions_, post_)
        # end if
        return self.row_actions(actions_)
    # end def handle_row_actions
    #// 
    #// Outputs the hidden row displayed when inline editing
    #// 
    #// @since 3.1.0
    #// 
    #// @global string $mode List table view mode.
    #//
    def inline_edit(self):
        
        
        global mode_
        php_check_if_defined("mode_")
        screen_ = self.screen
        post_ = get_default_post_to_edit(screen_.post_type)
        post_type_object_ = get_post_type_object(screen_.post_type)
        taxonomy_names_ = get_object_taxonomies(screen_.post_type)
        hierarchical_taxonomies_ = Array()
        flat_taxonomies_ = Array()
        for taxonomy_name_ in taxonomy_names_:
            taxonomy_ = get_taxonomy(taxonomy_name_)
            show_in_quick_edit_ = taxonomy_.show_in_quick_edit
            #// 
            #// Filters whether the current taxonomy should be shown in the Quick Edit panel.
            #// 
            #// @since 4.2.0
            #// 
            #// @param bool   $show_in_quick_edit Whether to show the current taxonomy in Quick Edit.
            #// @param string $taxonomy_name      Taxonomy name.
            #// @param string $post_type          Post type of current Quick Edit post.
            #//
            if (not apply_filters("quick_edit_show_taxonomy", show_in_quick_edit_, taxonomy_name_, screen_.post_type)):
                continue
            # end if
            if taxonomy_.hierarchical:
                hierarchical_taxonomies_[-1] = taxonomy_
            else:
                flat_taxonomies_[-1] = taxonomy_
            # end if
        # end for
        m_ = "excerpt" if (php_isset(lambda : mode_)) and "excerpt" == mode_ else "list"
        can_publish_ = current_user_can(post_type_object_.cap.publish_posts)
        core_columns_ = Array({"cb": True, "date": True, "title": True, "categories": True, "tags": True, "comments": True, "author": True})
        php_print("""
        <form method=\"get\">
        <table style=\"display: none\"><tbody id=\"inlineedit\">
        """)
        hclass_ = "post" if php_count(hierarchical_taxonomies_) else "page"
        inline_edit_classes_ = str("inline-edit-row inline-edit-row-") + str(hclass_)
        bulk_edit_classes_ = str("bulk-edit-row bulk-edit-row-") + str(hclass_) + str(" bulk-edit-") + str(screen_.post_type)
        quick_edit_classes_ = str("quick-edit-row quick-edit-row-") + str(hclass_) + str(" inline-edit-") + str(screen_.post_type)
        bulk_ = 0
        while True:
            
            if not (bulk_ < 2):
                break
            # end if
            classes_ = inline_edit_classes_ + " "
            classes_ += bulk_edit_classes_ if bulk_ else quick_edit_classes_
            php_print("         <tr id=\"")
            php_print("bulk-edit" if bulk_ else "inline-edit")
            php_print("\" class=\"")
            php_print(classes_)
            php_print("\" style=\"display: none\">\n            <td colspan=\"")
            php_print(self.get_column_count())
            php_print("""\" class=\"colspanchange\">
            <fieldset class=\"inline-edit-col-left\">
            <legend class=\"inline-edit-legend\">""")
            php_print(__("Bulk Edit") if bulk_ else __("Quick Edit"))
            php_print("""</legend>
            <div class=\"inline-edit-col\">
            """)
            if post_type_supports(screen_.post_type, "title"):
                php_print("\n                   ")
                if bulk_:
                    php_print("""
                    <div id=\"bulk-title-div\">
                    <div id=\"bulk-titles\"></div>
                    </div>
                    """)
                else:
                    pass
                    php_print("\n                       <label>\n                           <span class=\"title\">")
                    _e("Title")
                    php_print("""</span>
                    <span class=\"input-text-wrap\"><input type=\"text\" name=\"post_title\" class=\"ptitle\" value=\"\" /></span>
                    </label>
                    """)
                    if is_post_type_viewable(screen_.post_type):
                        php_print("\n                           <label>\n                               <span class=\"title\">")
                        _e("Slug")
                        php_print("""</span>
                        <span class=\"input-text-wrap\"><input type=\"text\" name=\"post_name\" value=\"\" /></span>
                        </label>
                        """)
                    # end if
                    pass
                    php_print("\n                   ")
                # end if
                pass
                php_print("\n               ")
            # end if
            pass
            php_print("\n               ")
            if (not bulk_):
                php_print("                 <fieldset class=\"inline-edit-date\">\n                     <legend><span class=\"title\">")
                _e("Date")
                php_print("</span></legend>\n                       ")
                touch_time(1, 1, 0, 1)
                php_print("                 </fieldset>\n                   <br class=\"clear\" />\n                ")
            # end if
            pass
            php_print("\n               ")
            if post_type_supports(screen_.post_type, "author"):
                authors_dropdown_ = ""
                if current_user_can(post_type_object_.cap.edit_others_posts):
                    users_opt_ = Array({"hide_if_only_one_author": False, "who": "authors", "name": "post_author", "class": "authors", "multi": 1, "echo": 0, "show": "display_name_with_login"})
                    if bulk_:
                        users_opt_["show_option_none"] = __("&mdash; No Change &mdash;")
                    # end if
                    authors_ = wp_dropdown_users(users_opt_)
                    if authors_:
                        authors_dropdown_ = "<label class=\"inline-edit-author\">"
                        authors_dropdown_ += "<span class=\"title\">" + __("Author") + "</span>"
                        authors_dropdown_ += authors_
                        authors_dropdown_ += "</label>"
                    # end if
                # end if
                pass
                php_print("\n                   ")
                if (not bulk_):
                    php_print(authors_dropdown_)
                # end if
            # end if
            pass
            php_print("\n               ")
            if (not bulk_) and can_publish_:
                php_print("""
                <div class=\"inline-edit-group wp-clearfix\">
                <label class=\"alignleft\">
                <span class=\"title\">""")
                _e("Password")
                php_print("""</span>
                <span class=\"input-text-wrap\"><input type=\"text\" name=\"post_password\" class=\"inline-edit-password-input\" value=\"\" /></span>
                </label>
                <span class=\"alignleft inline-edit-or\">
                """)
                #// translators: Between password field and private checkbox on post quick edit interface.
                _e("&ndash;OR&ndash;")
                php_print("""                       </span>
                <label class=\"alignleft inline-edit-private\">
                <input type=\"checkbox\" name=\"keep_private\" value=\"private\" />
                <span class=\"checkbox-title\">""")
                _e("Private")
                php_print("""</span>
                </label>
                </div>
                """)
            # end if
            php_print("""
            </div>
            </fieldset>
            """)
            if php_count(hierarchical_taxonomies_) and (not bulk_):
                php_print("""
                <fieldset class=\"inline-edit-col-center inline-edit-categories\">
                <div class=\"inline-edit-col\">
                """)
                for taxonomy_ in hierarchical_taxonomies_:
                    php_print("\n                       <span class=\"title inline-edit-categories-label\">")
                    php_print(esc_html(taxonomy_.labels.name))
                    php_print("</span>\n                        <input type=\"hidden\" name=\"")
                    php_print("post_category[]" if "category" == taxonomy_.name else "tax_input[" + esc_attr(taxonomy_.name) + "][]")
                    php_print("\" value=\"0\" />\n                      <ul class=\"cat-checklist ")
                    php_print(esc_attr(taxonomy_.name))
                    php_print("-checklist\">\n                          ")
                    wp_terms_checklist(None, Array({"taxonomy": taxonomy_.name}))
                    php_print("                     </ul>\n\n                   ")
                # end for
                pass
                php_print("""
                </div>
                </fieldset>
                """)
            # end if
            pass
            php_print("""
            <fieldset class=\"inline-edit-col-right\">
            <div class=\"inline-edit-col\">
            """)
            if post_type_supports(screen_.post_type, "author") and bulk_:
                php_print(authors_dropdown_)
            # end if
            php_print("\n               ")
            if post_type_supports(screen_.post_type, "page-attributes"):
                php_print("\n                   ")
                if post_type_object_.hierarchical:
                    php_print("\n                       <label>\n                           <span class=\"title\">")
                    _e("Parent")
                    php_print("</span>\n                            ")
                    dropdown_args_ = Array({"post_type": post_type_object_.name, "selected": post_.post_parent, "name": "post_parent", "show_option_none": __("Main Page (no parent)"), "option_none_value": 0, "sort_column": "menu_order, post_title"})
                    if bulk_:
                        dropdown_args_["show_option_no_change"] = __("&mdash; No Change &mdash;")
                    # end if
                    #// 
                    #// Filters the arguments used to generate the Quick Edit page-parent drop-down.
                    #// 
                    #// @since 2.7.0
                    #// 
                    #// @see wp_dropdown_pages()
                    #// 
                    #// @param array $dropdown_args An array of arguments.
                    #//
                    dropdown_args_ = apply_filters("quick_edit_dropdown_pages_args", dropdown_args_)
                    wp_dropdown_pages(dropdown_args_)
                    php_print("                     </label>\n\n                    ")
                # end if
                pass
                php_print("\n                   ")
                if (not bulk_):
                    php_print("\n                       <label>\n                           <span class=\"title\">")
                    _e("Order")
                    php_print("</span>\n                            <span class=\"input-text-wrap\"><input type=\"text\" name=\"menu_order\" class=\"inline-edit-menu-order-input\" value=\"")
                    php_print(post_.menu_order)
                    php_print("""\" /></span>
                    </label>
                    """)
                # end if
                pass
                php_print("\n               ")
            # end if
            pass
            php_print("\n               ")
            if 0 < php_count(get_page_templates(None, screen_.post_type)):
                php_print("\n                   <label>\n                       <span class=\"title\">")
                _e("Template")
                php_print("</span>\n                        <select name=\"page_template\">\n                           ")
                if bulk_:
                    php_print("                         <option value=\"-1\">")
                    _e("&mdash; No Change &mdash;")
                    php_print("</option>\n                          ")
                # end if
                pass
                php_print("                         ")
                #// This filter is documented in wp-admin/includes/meta-boxes.php
                default_title_ = apply_filters("default_page_template_title", __("Default Template"), "quick-edit")
                php_print("                         <option value=\"default\">")
                php_print(esc_html(default_title_))
                php_print("</option>\n                          ")
                page_template_dropdown("", screen_.post_type)
                php_print("""                       </select>
                </label>
                """)
            # end if
            php_print("\n               ")
            if php_count(flat_taxonomies_) and (not bulk_):
                php_print("\n                   ")
                for taxonomy_ in flat_taxonomies_:
                    php_print("\n                       ")
                    if current_user_can(taxonomy_.cap.assign_terms):
                        php_print("                         ")
                        taxonomy_name_ = esc_attr(taxonomy_.name)
                        php_print("\n                           <label class=\"inline-edit-tags\">\n                                <span class=\"title\">")
                        php_print(esc_html(taxonomy_.labels.name))
                        php_print("</span>\n                                <textarea data-wp-taxonomy=\"")
                        php_print(taxonomy_name_)
                        php_print("\" cols=\"22\" rows=\"1\" name=\"tax_input[")
                        php_print(taxonomy_name_)
                        php_print("]\" class=\"tax_input_")
                        php_print(taxonomy_name_)
                        php_print("""\"></textarea>
                        </label>
                        """)
                    # end if
                    pass
                    php_print("\n                   ")
                # end for
                pass
                php_print("\n               ")
            # end if
            pass
            php_print("\n               ")
            if post_type_supports(screen_.post_type, "comments") or post_type_supports(screen_.post_type, "trackbacks"):
                php_print("\n                   ")
                if bulk_:
                    php_print("""
                    <div class=\"inline-edit-group wp-clearfix\">
                    """)
                    if post_type_supports(screen_.post_type, "comments"):
                        php_print("\n                           <label class=\"alignleft\">\n                               <span class=\"title\">")
                        _e("Comments")
                        php_print("</span>\n                                <select name=\"comment_status\">\n                                  <option value=\"\">")
                        _e("&mdash; No Change &mdash;")
                        php_print("</option>\n                                  <option value=\"open\">")
                        _e("Allow")
                        php_print("</option>\n                                  <option value=\"closed\">")
                        _e("Do not allow")
                        php_print("""</option>
                        </select>
                        </label>
                        """)
                    # end if
                    php_print("\n                       ")
                    if post_type_supports(screen_.post_type, "trackbacks"):
                        php_print("\n                           <label class=\"alignright\">\n                              <span class=\"title\">")
                        _e("Pings")
                        php_print("</span>\n                                <select name=\"ping_status\">\n                                 <option value=\"\">")
                        _e("&mdash; No Change &mdash;")
                        php_print("</option>\n                                  <option value=\"open\">")
                        _e("Allow")
                        php_print("</option>\n                                  <option value=\"closed\">")
                        _e("Do not allow")
                        php_print("""</option>
                        </select>
                        </label>
                        """)
                    # end if
                    php_print("""
                    </div>
                    """)
                else:
                    pass
                    php_print("""
                    <div class=\"inline-edit-group wp-clearfix\">
                    """)
                    if post_type_supports(screen_.post_type, "comments"):
                        php_print("""
                        <label class=\"alignleft\">
                        <input type=\"checkbox\" name=\"comment_status\" value=\"open\" />
                        <span class=\"checkbox-title\">""")
                        _e("Allow Comments")
                        php_print("""</span>
                        </label>
                        """)
                    # end if
                    php_print("\n                       ")
                    if post_type_supports(screen_.post_type, "trackbacks"):
                        php_print("""
                        <label class=\"alignleft\">
                        <input type=\"checkbox\" name=\"ping_status\" value=\"open\" />
                        <span class=\"checkbox-title\">""")
                        _e("Allow Pings")
                        php_print("""</span>
                        </label>
                        """)
                    # end if
                    php_print("""
                    </div>
                    """)
                # end if
                pass
                php_print("\n               ")
            # end if
            pass
            php_print("""
            <div class=\"inline-edit-group wp-clearfix\">
            <label class=\"inline-edit-status alignleft\">
            <span class=\"title\">""")
            _e("Status")
            php_print("</span>\n                            <select name=\"_status\">\n                             ")
            if bulk_:
                php_print("                                 <option value=\"-1\">")
                _e("&mdash; No Change &mdash;")
                php_print("</option>\n                              ")
            # end if
            pass
            php_print("\n                               ")
            if can_publish_:
                pass
                php_print("                                 <option value=\"publish\">")
                _e("Published")
                php_print("</option>\n                                  <option value=\"future\">")
                _e("Scheduled")
                php_print("</option>\n                                  ")
                if bulk_:
                    php_print("                                     <option value=\"private\">")
                    _e("Private")
                    php_print("</option>\n                                  ")
                # end if
                pass
                php_print("                             ")
            # end if
            php_print("\n                               <option value=\"pending\">")
            _e("Pending Review")
            php_print("</option>\n                              <option value=\"draft\">")
            _e("Draft")
            php_print("""</option>
            </select>
            </label>
            """)
            if "post" == screen_.post_type and can_publish_ and current_user_can(post_type_object_.cap.edit_others_posts):
                php_print("\n                           ")
                if bulk_:
                    php_print("\n                               <label class=\"alignright\">\n                                  <span class=\"title\">")
                    _e("Sticky")
                    php_print("</span>\n                                    <select name=\"sticky\">\n                                      <option value=\"-1\">")
                    _e("&mdash; No Change &mdash;")
                    php_print("</option>\n                                      <option value=\"sticky\">")
                    _e("Sticky")
                    php_print("</option>\n                                      <option value=\"unsticky\">")
                    _e("Not Sticky")
                    php_print("""</option>
                    </select>
                    </label>
                    """)
                else:
                    pass
                    php_print("""
                    <label class=\"alignleft\">
                    <input type=\"checkbox\" name=\"sticky\" value=\"sticky\" />
                    <span class=\"checkbox-title\">""")
                    _e("Make this post sticky")
                    php_print("""</span>
                    </label>
                    """)
                # end if
                pass
                php_print("\n                       ")
            # end if
            pass
            php_print("""
            </div>
            """)
            if bulk_ and current_theme_supports("post-formats") and post_type_supports(screen_.post_type, "post-formats"):
                php_print("                 ")
                post_formats_ = get_theme_support("post-formats")
                php_print("\n                   <label class=\"alignleft\">\n                       <span class=\"title\">")
                _ex("Format", "post format")
                php_print("</span>\n                        <select name=\"post_format\">\n                         <option value=\"-1\">")
                _e("&mdash; No Change &mdash;")
                php_print("</option>\n                          <option value=\"0\">")
                php_print(get_post_format_string("standard"))
                php_print("</option>\n                          ")
                if php_is_array(post_formats_[0]):
                    php_print("                             ")
                    for format_ in post_formats_[0]:
                        php_print("                                 <option value=\"")
                        php_print(esc_attr(format_))
                        php_print("\">")
                        php_print(esc_html(get_post_format_string(format_)))
                        php_print("</option>\n                              ")
                    # end for
                    php_print("                         ")
                # end if
                php_print("""                       </select>
                </label>
                """)
            # end if
            php_print("""
            </div>
            </fieldset>
            """)
            columns_ = self.get_column_info()
            for column_name_,column_display_name_ in columns_.items():
                if (php_isset(lambda : core_columns_[column_name_])):
                    continue
                # end if
                if bulk_:
                    #// 
                    #// Fires once for each column in Bulk Edit mode.
                    #// 
                    #// @since 2.7.0
                    #// 
                    #// @param string $column_name Name of the column to edit.
                    #// @param string $post_type   The post type slug.
                    #//
                    do_action("bulk_edit_custom_box", column_name_, screen_.post_type)
                else:
                    #// 
                    #// Fires once for each column in Quick Edit mode.
                    #// 
                    #// @since 2.7.0
                    #// 
                    #// @param string $column_name Name of the column to edit.
                    #// @param string $post_type   The post type slug, or current screen name if this is a taxonomy list table.
                    #// @param string $taxonomy    The taxonomy name, if any.
                    #//
                    do_action("quick_edit_custom_box", column_name_, screen_.post_type, "")
                # end if
            # end for
            php_print("\n           <div class=\"submit inline-edit-save\">\n               <button type=\"button\" class=\"button cancel alignleft\">")
            _e("Cancel")
            php_print("</button>\n\n                ")
            if (not bulk_):
                php_print("                 ")
                wp_nonce_field("inlineeditnonce", "_inline_edit", False)
                php_print("                 <button type=\"button\" class=\"button button-primary save alignright\">")
                _e("Update")
                php_print("</button>\n                  <span class=\"spinner\"></span>\n               ")
            else:
                php_print("                 ")
                submit_button(__("Update"), "primary alignright", "bulk_edit", False)
                php_print("             ")
            # end if
            php_print("\n               <input type=\"hidden\" name=\"post_view\" value=\"")
            php_print(esc_attr(m_))
            php_print("\" />\n              <input type=\"hidden\" name=\"screen\" value=\"")
            php_print(esc_attr(screen_.id))
            php_print("\" />\n              ")
            if (not bulk_) and (not post_type_supports(screen_.post_type, "author")):
                php_print("                 <input type=\"hidden\" name=\"post_author\" value=\"")
                php_print(esc_attr(post_.post_author))
                php_print("\" />\n              ")
            # end if
            php_print("""               <br class=\"clear\" />
            <div class=\"notice notice-error notice-alt inline hidden\">
            <p class=\"error\"></p>
            </div>
            </div>
            </td></tr>
            """)
            bulk_ += 1
        # end while
        php_print("     </tbody></table>\n      </form>\n       ")
    # end def inline_edit
# end class WP_Posts_List_Table
