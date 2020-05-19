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
#// List Table API: WP_Media_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying media items in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Media_List_Table(WP_List_Table):
    #// 
    #// Holds the number of pending comments for each post.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    comment_pending_count = Array()
    detached = Array()
    is_trash = Array()
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
        
        self.detached = (php_isset(lambda : PHP_REQUEST["attachment-filter"])) and "detached" == PHP_REQUEST["attachment-filter"]
        self.modes = Array({"list": __("List View"), "grid": __("Grid View")})
        super().__init__(Array({"plural": "media", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
    # end def __init__
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        
        return current_user_can("upload_files")
    # end def ajax_user_can
    #// 
    #// @global WP_Query $wp_query              WordPress Query object.
    #// @global array    $post_mime_types
    #// @global array    $avail_post_mime_types
    #// @global string   $mode
    #//
    def prepare_items(self):
        
        
        global wp_query_
        global post_mime_types_
        global avail_post_mime_types_
        global mode_
        php_check_if_defined("wp_query_","post_mime_types_","avail_post_mime_types_","mode_")
        post_mime_types_, avail_post_mime_types_ = wp_edit_attachments_query(PHP_REQUEST)
        self.is_trash = (php_isset(lambda : PHP_REQUEST["attachment-filter"])) and "trash" == PHP_REQUEST["attachment-filter"]
        mode_ = "list" if php_empty(lambda : PHP_REQUEST["mode"]) else PHP_REQUEST["mode"]
        self.set_pagination_args(Array({"total_items": wp_query_.found_posts, "total_pages": wp_query_.max_num_pages, "per_page": wp_query_.query_vars["posts_per_page"]}))
    # end def prepare_items
    #// 
    #// @global array $post_mime_types
    #// @global array $avail_post_mime_types
    #// @return array
    #//
    def get_views(self):
        
        
        global post_mime_types_
        global avail_post_mime_types_
        php_check_if_defined("post_mime_types_","avail_post_mime_types_")
        type_links_ = Array()
        filter_ = "" if php_empty(lambda : PHP_REQUEST["attachment-filter"]) else PHP_REQUEST["attachment-filter"]
        type_links_["all"] = php_sprintf("<option value=\"\"%s>%s</option>", selected(filter_, True, False), __("All media items"))
        for mime_type_,label_ in post_mime_types_.items():
            if (not wp_match_mime_types(mime_type_, avail_post_mime_types_)):
                continue
            # end if
            selected_ = selected(filter_ and 0 == php_strpos(filter_, "post_mime_type:") and wp_match_mime_types(mime_type_, php_str_replace("post_mime_type:", "", filter_)), True, False)
            type_links_[mime_type_] = php_sprintf("<option value=\"post_mime_type:%s\"%s>%s</option>", esc_attr(mime_type_), selected_, label_[0])
        # end for
        type_links_["detached"] = "<option value=\"detached\"" + " selected=\"selected\"" if self.detached else "" + ">" + __("Unattached") + "</option>"
        type_links_["mine"] = php_sprintf("<option value=\"mine\"%s>%s</option>", selected("mine" == filter_, True, False), _x("Mine", "media items"))
        if self.is_trash or php_defined("MEDIA_TRASH") and MEDIA_TRASH:
            type_links_["trash"] = php_sprintf("<option value=\"trash\"%s>%s</option>", selected("trash" == filter_, True, False), _x("Trash", "attachment filter"))
        # end if
        return type_links_
    # end def get_views
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        actions_ = Array()
        if MEDIA_TRASH:
            if self.is_trash:
                actions_["untrash"] = __("Restore")
                actions_["delete"] = __("Delete Permanently")
            else:
                actions_["trash"] = __("Move to Trash")
            # end if
        else:
            actions_["delete"] = __("Delete Permanently")
        # end if
        if self.detached:
            actions_["attach"] = __("Attach")
        # end if
        return actions_
    # end def get_bulk_actions
    #// 
    #// @param string $which
    #//
    def extra_tablenav(self, which_=None):
        
        
        if "bar" != which_:
            return
        # end if
        php_print("     <div class=\"actions\">\n       ")
        if (not is_singular()):
            if (not self.is_trash):
                self.months_dropdown("attachment")
            # end if
            #// This action is documented in wp-admin/includes/class-wp-posts-list-table.php
            do_action("restrict_manage_posts", self.screen.post_type, which_)
            submit_button(__("Filter"), "", "filter_action", False, Array({"id": "post-query-submit"}))
        # end if
        if self.is_trash and current_user_can("edit_others_posts") and self.has_items():
            submit_button(__("Empty Trash"), "apply", "delete_all", False)
        # end if
        php_print("     </div>\n        ")
    # end def extra_tablenav
    #// 
    #// @return string
    #//
    def current_action(self):
        
        
        if (php_isset(lambda : PHP_REQUEST["found_post_id"])) and (php_isset(lambda : PHP_REQUEST["media"])):
            return "attach"
        # end if
        if (php_isset(lambda : PHP_REQUEST["parent_post_id"])) and (php_isset(lambda : PHP_REQUEST["media"])):
            return "detach"
        # end if
        if (php_isset(lambda : PHP_REQUEST["delete_all"])) or (php_isset(lambda : PHP_REQUEST["delete_all2"])):
            return "delete_all"
        # end if
        return super().current_action()
    # end def current_action
    #// 
    #// @return bool
    #//
    def has_items(self):
        
        
        return have_posts()
    # end def has_items
    #// 
    #//
    def no_items(self):
        
        
        if self.is_trash:
            _e("No media files found in Trash.")
        else:
            _e("No media files found.")
        # end if
    # end def no_items
    #// 
    #// Override parent views so we can use the filter bar display.
    #// 
    #// @global string $mode List table view mode.
    #//
    def views(self):
        
        
        global mode_
        php_check_if_defined("mode_")
        views_ = self.get_views()
        self.screen.render_screen_reader_content("heading_views")
        php_print("<div class=\"wp-filter\">\n  <div class=\"filter-items\">\n      ")
        self.view_switcher(mode_)
        php_print("\n       <label for=\"attachment-filter\" class=\"screen-reader-text\">")
        _e("Filter by type")
        php_print("</label>\n       <select class=\"attachment-filters\" name=\"attachment-filter\" id=\"attachment-filter\">\n         ")
        if (not php_empty(lambda : views_)):
            for class_,view_ in views_.items():
                php_print(str(" ") + str(view_) + str("\n"))
            # end for
        # end if
        php_print("     </select>\n\n       ")
        self.extra_tablenav("bar")
        #// This filter is documented in wp-admin/inclues/class-wp-list-table.php
        views_ = apply_filters(str("views_") + str(self.screen.id), Array())
        #// Back compat for pre-4.0 view links.
        if (not php_empty(lambda : views_)):
            php_print("<ul class=\"filter-links\">")
            for class_,view_ in views_.items():
                php_print(str("<li class='") + str(class_) + str("'>") + str(view_) + str("</li>"))
            # end for
            php_print("</ul>")
        # end if
        php_print("""   </div>
        <div class=\"search-form\">
        <label for=\"media-search-input\" class=\"media-search-input-label\">""")
        esc_html_e("Search")
        php_print("</label>\n       <input type=\"search\" id=\"media-search-input\" class=\"search\" name=\"s\" value=\"")
        _admin_search_query()
        php_print("\"></div>\n  </div>\n        ")
    # end def views
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        posts_columns_ = Array()
        posts_columns_["cb"] = "<input type=\"checkbox\" />"
        #// translators: Column name.
        posts_columns_["title"] = _x("File", "column name")
        posts_columns_["author"] = __("Author")
        taxonomies_ = get_taxonomies_for_attachments("objects")
        taxonomies_ = wp_filter_object_list(taxonomies_, Array({"show_admin_column": True}), "and", "name")
        #// 
        #// Filters the taxonomy columns for attachments in the Media list table.
        #// 
        #// @since 3.5.0
        #// 
        #// @param string[] $taxonomies An array of registered taxonomy names to show for attachments.
        #// @param string   $post_type  The post type. Default 'attachment'.
        #//
        taxonomies_ = apply_filters("manage_taxonomies_for_attachment_columns", taxonomies_, "attachment")
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
        #// translators: Column name.
        if (not self.detached):
            posts_columns_["parent"] = _x("Uploaded to", "column name")
            if post_type_supports("attachment", "comments"):
                posts_columns_["comments"] = "<span class=\"vers comment-grey-bubble\" title=\"" + esc_attr__("Comments") + "\"><span class=\"screen-reader-text\">" + __("Comments") + "</span></span>"
            # end if
        # end if
        #// translators: Column name.
        posts_columns_["date"] = _x("Date", "column name")
        #// 
        #// Filters the Media list table columns.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string[] $posts_columns An array of columns displayed in the Media list table.
        #// @param bool     $detached      Whether the list table contains media not attached
        #// to any posts. Default true.
        #//
        return apply_filters("manage_media_columns", posts_columns_, self.detached)
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        
        return Array({"title": "title", "author": "author", "parent": "parent", "comments": "comment_count", "date": Array("date", True)})
    # end def get_sortable_columns
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
            php_print(post_.ID)
            php_print("\">\n                ")
            #// translators: %s: Attachment title.
            printf(__("Select %s"), _draft_or_post_title())
            php_print("         </label>\n          <input type=\"checkbox\" name=\"media[]\" id=\"cb-select-")
            php_print(post_.ID)
            php_print("\" value=\"")
            php_print(post_.ID)
            php_print("\" />\n          ")
        # end if
    # end def column_cb
    #// 
    #// Handles the title column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_title(self, post_=None):
        
        
        mime_ = php_explode("/", post_.post_mime_type)
        title_ = _draft_or_post_title()
        thumb_ = wp_get_attachment_image(post_.ID, Array(60, 60), True, Array({"alt": ""}))
        link_start_ = ""
        link_end_ = ""
        if current_user_can("edit_post", post_.ID) and (not self.is_trash):
            link_start_ = php_sprintf("<a href=\"%s\" aria-label=\"%s\">", get_edit_post_link(post_.ID), esc_attr(php_sprintf(__("&#8220;%s&#8221; (Edit)"), title_)))
            link_end_ = "</a>"
        # end if
        class_ = " class=\"has-media-icon\"" if thumb_ else ""
        php_print("     <strong")
        php_print(class_)
        php_print(">\n          ")
        php_print(link_start_)
        if thumb_:
            php_print("             <span class=\"media-icon ")
            php_print(sanitize_html_class(mime_ + "-icon"))
            php_print("\">")
            php_print(thumb_)
            php_print("</span>\n                ")
        # end if
        php_print(title_ + link_end_)
        _media_states(post_)
        php_print("     </strong>\n     <p class=\"filename\">\n            <span class=\"screen-reader-text\">")
        _e("File name:")
        php_print(" </span>\n           ")
        file_ = get_attached_file(post_.ID)
        php_print(esc_html(wp_basename(file_)))
        php_print("     </p>\n      ")
    # end def column_title
    #// 
    #// Handles the author column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_author(self, post_=None):
        
        
        printf("<a href=\"%s\">%s</a>", esc_url(add_query_arg(Array({"author": get_the_author_meta("ID")}), "upload.php")), get_the_author())
    # end def column_author
    #// 
    #// Handles the description column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_desc(self, post_=None):
        
        
        php_print(post_.post_excerpt if has_excerpt() else "")
    # end def column_desc
    #// 
    #// Handles the date column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_date(self, post_=None):
        
        
        if "0000-00-00 00:00:00" == post_.post_date:
            h_time_ = __("Unpublished")
        else:
            time_ = get_post_timestamp(post_)
            time_diff_ = time() - time_
            if time_ and time_diff_ > 0 and time_diff_ < DAY_IN_SECONDS:
                #// translators: %s: Human-readable time difference.
                h_time_ = php_sprintf(__("%s ago"), human_time_diff(time_))
            else:
                h_time_ = get_the_time(__("Y/m/d"), post_)
            # end if
        # end if
        php_print(h_time_)
    # end def column_date
    #// 
    #// Handles the parent column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_parent(self, post_=None):
        
        
        user_can_edit_ = current_user_can("edit_post", post_.ID)
        if post_.post_parent > 0:
            parent_ = get_post(post_.post_parent)
        else:
            parent_ = False
        # end if
        if parent_:
            title_ = _draft_or_post_title(post_.post_parent)
            parent_type_ = get_post_type_object(parent_.post_type)
            if parent_type_ and parent_type_.show_ui and current_user_can("edit_post", post_.post_parent):
                php_print("             <strong><a href=\"")
                php_print(get_edit_post_link(post_.post_parent))
                php_print("\">\n                    ")
                php_print(title_)
                php_print("</a></strong>\n                              ")
            elif parent_type_ and current_user_can("read_post", post_.post_parent):
                php_print("             <strong>")
                php_print(title_)
                php_print("</strong>\n                                  ")
            else:
                _e("(Private post)")
            # end if
            if user_can_edit_:
                detach_url_ = add_query_arg(Array({"parent_post_id": post_.post_parent, "media[]": post_.ID, "_wpnonce": wp_create_nonce("bulk-" + self._args["plural"])}), "upload.php")
                printf("<br /><a href=\"%s\" class=\"hide-if-no-js detach-from-parent\" aria-label=\"%s\">%s</a>", detach_url_, esc_attr(php_sprintf(__("Detach from &#8220;%s&#8221;"), title_)), __("Detach"))
            # end if
        else:
            _e("(Unattached)")
            php_print("         ")
            if user_can_edit_:
                title_ = _draft_or_post_title(post_.post_parent)
                printf("<br /><a href=\"#the-list\" onclick=\"findPosts.open( 'media[]', '%s' ); return false;\" class=\"hide-if-no-js aria-button-if-js\" aria-label=\"%s\">%s</a>", post_.ID, esc_attr(php_sprintf(__("Attach &#8220;%s&#8221; to existing content"), title_)), __("Attach"))
            # end if
        # end if
    # end def column_parent
    #// 
    #// Handles the comments column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_comments(self, post_=None):
        
        
        php_print("<div class=\"post-com-count-wrapper\">")
        if (php_isset(lambda : self.comment_pending_count[post_.ID])):
            pending_comments_ = self.comment_pending_count[post_.ID]
        else:
            pending_comments_ = get_pending_comments_num(post_.ID)
        # end if
        self.comments_bubble(post_.ID, pending_comments_)
        php_print("</div>")
    # end def column_comments
    #// 
    #// Handles output for the default column.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post        The current WP_Post object.
    #// @param string  $column_name Current column name.
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
            terms_ = get_the_terms(post_.ID, taxonomy_)
            if php_is_array(terms_):
                out_ = Array()
                for t_ in terms_:
                    posts_in_term_qv_ = Array()
                    posts_in_term_qv_["taxonomy"] = taxonomy_
                    posts_in_term_qv_["term"] = t_.slug
                    out_[-1] = php_sprintf("<a href=\"%s\">%s</a>", esc_url(add_query_arg(posts_in_term_qv_, "upload.php")), esc_html(sanitize_term_field("name", t_.name, t_.term_id, taxonomy_, "display")))
                # end for
                #// translators: Used between list items, there is a space after the comma.
                php_print(join(__(", "), out_))
            else:
                php_print("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">" + get_taxonomy(taxonomy_).labels.no_terms + "</span>")
            # end if
            return
        # end if
        #// 
        #// Fires for each custom column in the Media list table.
        #// 
        #// Custom columns are registered using the {@see 'manage_media_columns'} filter.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string $column_name Name of the custom column.
        #// @param int    $post_id     Attachment ID.
        #//
        do_action("manage_media_custom_column", column_name_, post_.ID)
    # end def column_default
    #// 
    #// @global WP_Post $post Global post object.
    #//
    def display_rows(self):
        
        
        global post_
        global wp_query_
        php_check_if_defined("post_","wp_query_")
        post_ids_ = wp_list_pluck(wp_query_.posts, "ID")
        reset(wp_query_.posts)
        self.comment_pending_count = get_pending_comments_num(post_ids_)
        add_filter("the_title", "esc_html")
        while True:
            
            if not (have_posts()):
                break
            # end if
            the_post()
            if self.is_trash and "trash" != post_.post_status or (not self.is_trash) and "trash" == post_.post_status:
                continue
            # end if
            post_owner_ = "self" if get_current_user_id() == post_.post_author else "other"
            php_print("         <tr id=\"post-")
            php_print(post_.ID)
            php_print("\" class=\"")
            php_print(php_trim(" author-" + post_owner_ + " status-" + post_.post_status))
            php_print("\">\n                ")
            self.single_row_columns(post_)
            php_print("         </tr>\n         ")
        # end while
    # end def display_rows
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
    #// @param WP_Post $post
    #// @param string  $att_title
    #// 
    #// @return array
    #//
    def _get_row_actions(self, post_=None, att_title_=None):
        
        
        actions_ = Array()
        if self.detached:
            if current_user_can("edit_post", post_.ID):
                actions_["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_edit_post_link(post_.ID), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), att_title_)), __("Edit"))
            # end if
            if current_user_can("delete_post", post_.ID):
                if EMPTY_TRASH_DAYS and MEDIA_TRASH:
                    actions_["trash"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=trash&amp;post=") + str(post_.ID), "trash-post_" + post_.ID), esc_attr(php_sprintf(__("Move &#8220;%s&#8221; to the Trash"), att_title_)), _x("Trash", "verb"))
                else:
                    delete_ays_ = " onclick='return showNotice.warn();'" if (not MEDIA_TRASH) else ""
                    actions_["delete"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\"%s aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=delete&amp;post=") + str(post_.ID), "delete-post_" + post_.ID), delete_ays_, esc_attr(php_sprintf(__("Delete &#8220;%s&#8221; permanently"), att_title_)), __("Delete Permanently"))
                # end if
            # end if
            actions_["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\" rel=\"bookmark\">%s</a>", get_permalink(post_.ID), esc_attr(php_sprintf(__("View &#8220;%s&#8221;"), att_title_)), __("View"))
            if current_user_can("edit_post", post_.ID):
                actions_["attach"] = php_sprintf("<a href=\"#the-list\" onclick=\"findPosts.open( 'media[]', '%s' ); return false;\" class=\"hide-if-no-js aria-button-if-js\" aria-label=\"%s\">%s</a>", post_.ID, esc_attr(php_sprintf(__("Attach &#8220;%s&#8221; to existing content"), att_title_)), __("Attach"))
            # end if
        else:
            if current_user_can("edit_post", post_.ID) and (not self.is_trash):
                actions_["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_edit_post_link(post_.ID), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), att_title_)), __("Edit"))
            # end if
            if current_user_can("delete_post", post_.ID):
                if self.is_trash:
                    actions_["untrash"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=untrash&amp;post=") + str(post_.ID), "untrash-post_" + post_.ID), esc_attr(php_sprintf(__("Restore &#8220;%s&#8221; from the Trash"), att_title_)), __("Restore"))
                elif EMPTY_TRASH_DAYS and MEDIA_TRASH:
                    actions_["trash"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=trash&amp;post=") + str(post_.ID), "trash-post_" + post_.ID), esc_attr(php_sprintf(__("Move &#8220;%s&#8221; to the Trash"), att_title_)), _x("Trash", "verb"))
                # end if
                if self.is_trash or (not EMPTY_TRASH_DAYS) or (not MEDIA_TRASH):
                    delete_ays_ = " onclick='return showNotice.warn();'" if (not self.is_trash) and (not MEDIA_TRASH) else ""
                    actions_["delete"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\"%s aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=delete&amp;post=") + str(post_.ID), "delete-post_" + post_.ID), delete_ays_, esc_attr(php_sprintf(__("Delete &#8220;%s&#8221; permanently"), att_title_)), __("Delete Permanently"))
                # end if
            # end if
            if (not self.is_trash):
                actions_["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\" rel=\"bookmark\">%s</a>", get_permalink(post_.ID), esc_attr(php_sprintf(__("View &#8220;%s&#8221;"), att_title_)), __("View"))
            # end if
        # end if
        #// 
        #// Filters the action links for each attachment in the Media list table.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $actions  An array of action links for each attachment.
        #// Default 'Edit', 'Delete Permanently', 'View'.
        #// @param WP_Post  $post     WP_Post object for the current attachment.
        #// @param bool     $detached Whether the list table contains media not attached
        #// to any posts. Default true.
        #//
        return apply_filters("media_row_actions", actions_, post_, self.detached)
    # end def _get_row_actions
    #// 
    #// Generates and displays row action links.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $post        Attachment being acted upon.
    #// @param string $column_name Current column name.
    #// @param string $primary     Primary column name.
    #// @return string Row actions output for media attachments, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, post_=None, column_name_=None, primary_=None):
        
        
        if primary_ != column_name_:
            return ""
        # end if
        att_title_ = _draft_or_post_title()
        return self.row_actions(self._get_row_actions(post_, att_title_))
    # end def handle_row_actions
# end class WP_Media_List_Table
