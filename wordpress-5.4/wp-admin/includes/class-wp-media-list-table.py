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
    def __init__(self, args=Array()):
        
        self.detached = (php_isset(lambda : PHP_REQUEST["attachment-filter"])) and "detached" == PHP_REQUEST["attachment-filter"]
        self.modes = Array({"list": __("List View"), "grid": __("Grid View")})
        super().__init__(Array({"plural": "media", "screen": args["screen"] if (php_isset(lambda : args["screen"])) else None}))
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
        
        global wp_query,post_mime_types,avail_post_mime_types,mode
        php_check_if_defined("wp_query","post_mime_types","avail_post_mime_types","mode")
        post_mime_types, avail_post_mime_types = wp_edit_attachments_query(PHP_REQUEST)
        self.is_trash = (php_isset(lambda : PHP_REQUEST["attachment-filter"])) and "trash" == PHP_REQUEST["attachment-filter"]
        mode = "list" if php_empty(lambda : PHP_REQUEST["mode"]) else PHP_REQUEST["mode"]
        self.set_pagination_args(Array({"total_items": wp_query.found_posts, "total_pages": wp_query.max_num_pages, "per_page": wp_query.query_vars["posts_per_page"]}))
    # end def prepare_items
    #// 
    #// @global array $post_mime_types
    #// @global array $avail_post_mime_types
    #// @return array
    #//
    def get_views(self):
        
        global post_mime_types,avail_post_mime_types
        php_check_if_defined("post_mime_types","avail_post_mime_types")
        type_links = Array()
        filter = "" if php_empty(lambda : PHP_REQUEST["attachment-filter"]) else PHP_REQUEST["attachment-filter"]
        type_links["all"] = php_sprintf("<option value=\"\"%s>%s</option>", selected(filter, True, False), __("All media items"))
        for mime_type,label in post_mime_types:
            if (not wp_match_mime_types(mime_type, avail_post_mime_types)):
                continue
            # end if
            selected = selected(filter and 0 == php_strpos(filter, "post_mime_type:") and wp_match_mime_types(mime_type, php_str_replace("post_mime_type:", "", filter)), True, False)
            type_links[mime_type] = php_sprintf("<option value=\"post_mime_type:%s\"%s>%s</option>", esc_attr(mime_type), selected, label[0])
        # end for
        type_links["detached"] = "<option value=\"detached\"" + " selected=\"selected\"" if self.detached else "" + ">" + __("Unattached") + "</option>"
        type_links["mine"] = php_sprintf("<option value=\"mine\"%s>%s</option>", selected("mine" == filter, True, False), _x("Mine", "media items"))
        if self.is_trash or php_defined("MEDIA_TRASH") and MEDIA_TRASH:
            type_links["trash"] = php_sprintf("<option value=\"trash\"%s>%s</option>", selected("trash" == filter, True, False), _x("Trash", "attachment filter"))
        # end if
        return type_links
    # end def get_views
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        actions = Array()
        if MEDIA_TRASH:
            if self.is_trash:
                actions["untrash"] = __("Restore")
                actions["delete"] = __("Delete Permanently")
            else:
                actions["trash"] = __("Move to Trash")
            # end if
        else:
            actions["delete"] = __("Delete Permanently")
        # end if
        if self.detached:
            actions["attach"] = __("Attach")
        # end if
        return actions
    # end def get_bulk_actions
    #// 
    #// @param string $which
    #//
    def extra_tablenav(self, which=None):
        
        if "bar" != which:
            return
        # end if
        php_print("     <div class=\"actions\">\n       ")
        if (not is_singular()):
            if (not self.is_trash):
                self.months_dropdown("attachment")
            # end if
            #// This action is documented in wp-admin/includes/class-wp-posts-list-table.php
            do_action("restrict_manage_posts", self.screen.post_type, which)
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
        
        global mode
        php_check_if_defined("mode")
        views = self.get_views()
        self.screen.render_screen_reader_content("heading_views")
        php_print("<div class=\"wp-filter\">\n  <div class=\"filter-items\">\n      ")
        self.view_switcher(mode)
        php_print("\n       <label for=\"attachment-filter\" class=\"screen-reader-text\">")
        _e("Filter by type")
        php_print("</label>\n       <select class=\"attachment-filters\" name=\"attachment-filter\" id=\"attachment-filter\">\n         ")
        if (not php_empty(lambda : views)):
            for class_,view in views:
                php_print(str(" ") + str(view) + str("\n"))
            # end for
        # end if
        php_print("     </select>\n\n       ")
        self.extra_tablenav("bar")
        #// This filter is documented in wp-admin/inclues/class-wp-list-table.php
        views = apply_filters(str("views_") + str(self.screen.id), Array())
        #// Back compat for pre-4.0 view links.
        if (not php_empty(lambda : views)):
            php_print("<ul class=\"filter-links\">")
            for class_,view in views:
                php_print(str("<li class='") + str(class_) + str("'>") + str(view) + str("</li>"))
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
        
        posts_columns = Array()
        posts_columns["cb"] = "<input type=\"checkbox\" />"
        #// translators: Column name.
        posts_columns["title"] = _x("File", "column name")
        posts_columns["author"] = __("Author")
        taxonomies = get_taxonomies_for_attachments("objects")
        taxonomies = wp_filter_object_list(taxonomies, Array({"show_admin_column": True}), "and", "name")
        #// 
        #// Filters the taxonomy columns for attachments in the Media list table.
        #// 
        #// @since 3.5.0
        #// 
        #// @param string[] $taxonomies An array of registered taxonomy names to show for attachments.
        #// @param string   $post_type  The post type. Default 'attachment'.
        #//
        taxonomies = apply_filters("manage_taxonomies_for_attachment_columns", taxonomies, "attachment")
        taxonomies = php_array_filter(taxonomies, "taxonomy_exists")
        for taxonomy in taxonomies:
            if "category" == taxonomy:
                column_key = "categories"
            elif "post_tag" == taxonomy:
                column_key = "tags"
            else:
                column_key = "taxonomy-" + taxonomy
            # end if
            posts_columns[column_key] = get_taxonomy(taxonomy).labels.name
        # end for
        #// translators: Column name.
        if (not self.detached):
            posts_columns["parent"] = _x("Uploaded to", "column name")
            if post_type_supports("attachment", "comments"):
                posts_columns["comments"] = "<span class=\"vers comment-grey-bubble\" title=\"" + esc_attr__("Comments") + "\"><span class=\"screen-reader-text\">" + __("Comments") + "</span></span>"
            # end if
        # end if
        #// translators: Column name.
        posts_columns["date"] = _x("Date", "column name")
        #// 
        #// Filters the Media list table columns.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string[] $posts_columns An array of columns displayed in the Media list table.
        #// @param bool     $detached      Whether the list table contains media not attached
        #// to any posts. Default true.
        #//
        return apply_filters("manage_media_columns", posts_columns, self.detached)
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
    def column_cb(self, post=None):
        
        if current_user_can("edit_post", post.ID):
            php_print("         <label class=\"screen-reader-text\" for=\"cb-select-")
            php_print(post.ID)
            php_print("\">\n                ")
            #// translators: %s: Attachment title.
            printf(__("Select %s"), _draft_or_post_title())
            php_print("         </label>\n          <input type=\"checkbox\" name=\"media[]\" id=\"cb-select-")
            php_print(post.ID)
            php_print("\" value=\"")
            php_print(post.ID)
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
    def column_title(self, post=None):
        
        mime = php_explode("/", post.post_mime_type)
        title = _draft_or_post_title()
        thumb = wp_get_attachment_image(post.ID, Array(60, 60), True, Array({"alt": ""}))
        link_start = ""
        link_end = ""
        if current_user_can("edit_post", post.ID) and (not self.is_trash):
            link_start = php_sprintf("<a href=\"%s\" aria-label=\"%s\">", get_edit_post_link(post.ID), esc_attr(php_sprintf(__("&#8220;%s&#8221; (Edit)"), title)))
            link_end = "</a>"
        # end if
        class_ = " class=\"has-media-icon\"" if thumb else ""
        php_print("     <strong")
        php_print(class_)
        php_print(">\n          ")
        php_print(link_start)
        if thumb:
            php_print("             <span class=\"media-icon ")
            php_print(sanitize_html_class(mime + "-icon"))
            php_print("\">")
            php_print(thumb)
            php_print("</span>\n                ")
        # end if
        php_print(title + link_end)
        _media_states(post)
        php_print("     </strong>\n     <p class=\"filename\">\n            <span class=\"screen-reader-text\">")
        _e("File name:")
        php_print(" </span>\n           ")
        file = get_attached_file(post.ID)
        php_print(esc_html(wp_basename(file)))
        php_print("     </p>\n      ")
    # end def column_title
    #// 
    #// Handles the author column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_author(self, post=None):
        
        printf("<a href=\"%s\">%s</a>", esc_url(add_query_arg(Array({"author": get_the_author_meta("ID")}), "upload.php")), get_the_author())
    # end def column_author
    #// 
    #// Handles the description column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_desc(self, post=None):
        
        php_print(post.post_excerpt if has_excerpt() else "")
    # end def column_desc
    #// 
    #// Handles the date column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_date(self, post=None):
        
        if "0000-00-00 00:00:00" == post.post_date:
            h_time = __("Unpublished")
        else:
            time = get_post_timestamp(post)
            time_diff = time() - time
            if time and time_diff > 0 and time_diff < DAY_IN_SECONDS:
                #// translators: %s: Human-readable time difference.
                h_time = php_sprintf(__("%s ago"), human_time_diff(time))
            else:
                h_time = get_the_time(__("Y/m/d"), post)
            # end if
        # end if
        php_print(h_time)
    # end def column_date
    #// 
    #// Handles the parent column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Post $post The current WP_Post object.
    #//
    def column_parent(self, post=None):
        
        user_can_edit = current_user_can("edit_post", post.ID)
        if post.post_parent > 0:
            parent = get_post(post.post_parent)
        else:
            parent = False
        # end if
        if parent:
            title = _draft_or_post_title(post.post_parent)
            parent_type = get_post_type_object(parent.post_type)
            if parent_type and parent_type.show_ui and current_user_can("edit_post", post.post_parent):
                php_print("             <strong><a href=\"")
                php_print(get_edit_post_link(post.post_parent))
                php_print("\">\n                    ")
                php_print(title)
                php_print("</a></strong>\n                              ")
            elif parent_type and current_user_can("read_post", post.post_parent):
                php_print("             <strong>")
                php_print(title)
                php_print("</strong>\n                                  ")
            else:
                _e("(Private post)")
            # end if
            if user_can_edit:
                detach_url = add_query_arg(Array({"parent_post_id": post.post_parent, "media[]": post.ID, "_wpnonce": wp_create_nonce("bulk-" + self._args["plural"])}), "upload.php")
                printf("<br /><a href=\"%s\" class=\"hide-if-no-js detach-from-parent\" aria-label=\"%s\">%s</a>", detach_url, esc_attr(php_sprintf(__("Detach from &#8220;%s&#8221;"), title)), __("Detach"))
            # end if
        else:
            _e("(Unattached)")
            php_print("         ")
            if user_can_edit:
                title = _draft_or_post_title(post.post_parent)
                printf("<br /><a href=\"#the-list\" onclick=\"findPosts.open( 'media[]', '%s' ); return false;\" class=\"hide-if-no-js aria-button-if-js\" aria-label=\"%s\">%s</a>", post.ID, esc_attr(php_sprintf(__("Attach &#8220;%s&#8221; to existing content"), title)), __("Attach"))
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
    def column_comments(self, post=None):
        
        php_print("<div class=\"post-com-count-wrapper\">")
        if (php_isset(lambda : self.comment_pending_count[post.ID])):
            pending_comments = self.comment_pending_count[post.ID]
        else:
            pending_comments = get_pending_comments_num(post.ID)
        # end if
        self.comments_bubble(post.ID, pending_comments)
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
    def column_default(self, post=None, column_name=None):
        
        if "categories" == column_name:
            taxonomy = "category"
        elif "tags" == column_name:
            taxonomy = "post_tag"
        elif 0 == php_strpos(column_name, "taxonomy-"):
            taxonomy = php_substr(column_name, 9)
        else:
            taxonomy = False
        # end if
        if taxonomy:
            terms = get_the_terms(post.ID, taxonomy)
            if php_is_array(terms):
                out = Array()
                for t in terms:
                    posts_in_term_qv = Array()
                    posts_in_term_qv["taxonomy"] = taxonomy
                    posts_in_term_qv["term"] = t.slug
                    out[-1] = php_sprintf("<a href=\"%s\">%s</a>", esc_url(add_query_arg(posts_in_term_qv, "upload.php")), esc_html(sanitize_term_field("name", t.name, t.term_id, taxonomy, "display")))
                # end for
                #// translators: Used between list items, there is a space after the comma.
                php_print(join(__(", "), out))
            else:
                php_print("<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">" + get_taxonomy(taxonomy).labels.no_terms + "</span>")
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
        do_action("manage_media_custom_column", column_name, post.ID)
    # end def column_default
    #// 
    #// @global WP_Post $post Global post object.
    #//
    def display_rows(self):
        
        global post,wp_query
        php_check_if_defined("post","wp_query")
        post_ids = wp_list_pluck(wp_query.posts, "ID")
        reset(wp_query.posts)
        self.comment_pending_count = get_pending_comments_num(post_ids)
        add_filter("the_title", "esc_html")
        while True:
            
            if not (have_posts()):
                break
            # end if
            the_post()
            if self.is_trash and "trash" != post.post_status or (not self.is_trash) and "trash" == post.post_status:
                continue
            # end if
            post_owner = "self" if get_current_user_id() == post.post_author else "other"
            php_print("         <tr id=\"post-")
            php_print(post.ID)
            php_print("\" class=\"")
            php_print(php_trim(" author-" + post_owner + " status-" + post.post_status))
            php_print("\">\n                ")
            self.single_row_columns(post)
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
    def _get_row_actions(self, post=None, att_title=None):
        
        actions = Array()
        if self.detached:
            if current_user_can("edit_post", post.ID):
                actions["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_edit_post_link(post.ID), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), att_title)), __("Edit"))
            # end if
            if current_user_can("delete_post", post.ID):
                if EMPTY_TRASH_DAYS and MEDIA_TRASH:
                    actions["trash"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=trash&amp;post=") + str(post.ID), "trash-post_" + post.ID), esc_attr(php_sprintf(__("Move &#8220;%s&#8221; to the Trash"), att_title)), _x("Trash", "verb"))
                else:
                    delete_ays = " onclick='return showNotice.warn();'" if (not MEDIA_TRASH) else ""
                    actions["delete"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\"%s aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=delete&amp;post=") + str(post.ID), "delete-post_" + post.ID), delete_ays, esc_attr(php_sprintf(__("Delete &#8220;%s&#8221; permanently"), att_title)), __("Delete Permanently"))
                # end if
            # end if
            actions["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\" rel=\"bookmark\">%s</a>", get_permalink(post.ID), esc_attr(php_sprintf(__("View &#8220;%s&#8221;"), att_title)), __("View"))
            if current_user_can("edit_post", post.ID):
                actions["attach"] = php_sprintf("<a href=\"#the-list\" onclick=\"findPosts.open( 'media[]', '%s' ); return false;\" class=\"hide-if-no-js aria-button-if-js\" aria-label=\"%s\">%s</a>", post.ID, esc_attr(php_sprintf(__("Attach &#8220;%s&#8221; to existing content"), att_title)), __("Attach"))
            # end if
        else:
            if current_user_can("edit_post", post.ID) and (not self.is_trash):
                actions["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_edit_post_link(post.ID), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), att_title)), __("Edit"))
            # end if
            if current_user_can("delete_post", post.ID):
                if self.is_trash:
                    actions["untrash"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=untrash&amp;post=") + str(post.ID), "untrash-post_" + post.ID), esc_attr(php_sprintf(__("Restore &#8220;%s&#8221; from the Trash"), att_title)), __("Restore"))
                elif EMPTY_TRASH_DAYS and MEDIA_TRASH:
                    actions["trash"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=trash&amp;post=") + str(post.ID), "trash-post_" + post.ID), esc_attr(php_sprintf(__("Move &#8220;%s&#8221; to the Trash"), att_title)), _x("Trash", "verb"))
                # end if
                if self.is_trash or (not EMPTY_TRASH_DAYS) or (not MEDIA_TRASH):
                    delete_ays = " onclick='return showNotice.warn();'" if (not self.is_trash) and (not MEDIA_TRASH) else ""
                    actions["delete"] = php_sprintf("<a href=\"%s\" class=\"submitdelete aria-button-if-js\"%s aria-label=\"%s\">%s</a>", wp_nonce_url(str("post.php?action=delete&amp;post=") + str(post.ID), "delete-post_" + post.ID), delete_ays, esc_attr(php_sprintf(__("Delete &#8220;%s&#8221; permanently"), att_title)), __("Delete Permanently"))
                # end if
            # end if
            if (not self.is_trash):
                actions["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\" rel=\"bookmark\">%s</a>", get_permalink(post.ID), esc_attr(php_sprintf(__("View &#8220;%s&#8221;"), att_title)), __("View"))
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
        return apply_filters("media_row_actions", actions, post, self.detached)
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
    def handle_row_actions(self, post=None, column_name=None, primary=None):
        
        if primary != column_name:
            return ""
        # end if
        att_title = _draft_or_post_title()
        return self.row_actions(self._get_row_actions(post, att_title))
    # end def handle_row_actions
# end class WP_Media_List_Table
