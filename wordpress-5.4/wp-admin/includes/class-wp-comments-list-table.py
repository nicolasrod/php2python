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
#// List Table API: WP_Comments_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying comments in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Comments_List_Table(WP_List_Table):
    checkbox = True
    pending_count = Array()
    extra_items = Array()
    user_can = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @see WP_List_Table::__construct() for more information on default arguments.
    #// 
    #// @global int $post_id
    #// 
    #// @param array $args An associative array of arguments.
    #//
    def __init__(self, args=Array()):
        
        global post_id
        php_check_if_defined("post_id")
        post_id = absint(PHP_REQUEST["p"]) if (php_isset(lambda : PHP_REQUEST["p"])) else 0
        if get_option("show_avatars"):
            add_filter("comment_author", Array(self, "floated_admin_avatar"), 10, 2)
        # end if
        super().__init__(Array({"plural": "comments", "singular": "comment", "ajax": True, "screen": args["screen"] if (php_isset(lambda : args["screen"])) else None}))
    # end def __init__
    def floated_admin_avatar(self, name=None, comment_ID=None):
        
        comment = get_comment(comment_ID)
        avatar = get_avatar(comment, 32, "mystery")
        return str(avatar) + str(" ") + str(name)
    # end def floated_admin_avatar
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        return current_user_can("edit_posts")
    # end def ajax_user_can
    #// 
    #// @global int    $post_id
    #// @global string $comment_status
    #// @global string $search
    #// @global string $comment_type
    #//
    def prepare_items(self):
        
        global post_id,comment_status,search,comment_type
        php_check_if_defined("post_id","comment_status","search","comment_type")
        comment_status = PHP_REQUEST["comment_status"] if (php_isset(lambda : PHP_REQUEST["comment_status"])) else "all"
        if (not php_in_array(comment_status, Array("all", "mine", "moderated", "approved", "spam", "trash"))):
            comment_status = "all"
        # end if
        comment_type = PHP_REQUEST["comment_type"] if (not php_empty(lambda : PHP_REQUEST["comment_type"])) else ""
        search = PHP_REQUEST["s"] if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        post_type = sanitize_key(PHP_REQUEST["post_type"]) if (php_isset(lambda : PHP_REQUEST["post_type"])) else ""
        user_id = PHP_REQUEST["user_id"] if (php_isset(lambda : PHP_REQUEST["user_id"])) else ""
        orderby = PHP_REQUEST["orderby"] if (php_isset(lambda : PHP_REQUEST["orderby"])) else ""
        order = PHP_REQUEST["order"] if (php_isset(lambda : PHP_REQUEST["order"])) else ""
        comments_per_page = self.get_per_page(comment_status)
        doing_ajax = wp_doing_ajax()
        if (php_isset(lambda : PHP_REQUEST["number"])):
            number = int(PHP_REQUEST["number"])
        else:
            number = comments_per_page + php_min(8, comments_per_page)
            pass
        # end if
        page = self.get_pagenum()
        if (php_isset(lambda : PHP_REQUEST["start"])):
            start = PHP_REQUEST["start"]
        else:
            start = page - 1 * comments_per_page
        # end if
        if doing_ajax and (php_isset(lambda : PHP_REQUEST["offset"])):
            start += PHP_REQUEST["offset"]
        # end if
        status_map = Array({"mine": "", "moderated": "hold", "approved": "approve", "all": ""})
        args = Array({"status": status_map[comment_status] if (php_isset(lambda : status_map[comment_status])) else comment_status, "search": search, "user_id": user_id, "offset": start, "number": number, "post_id": post_id, "type": comment_type, "orderby": orderby, "order": order, "post_type": post_type})
        #// 
        #// Filters the arguments for the comment query in the comments list table.
        #// 
        #// @since 5.1.0
        #// 
        #// @param array $args An array of get_comments() arguments.
        #//
        args = apply_filters("comments_list_table_query_args", args)
        _comments = get_comments(args)
        if php_is_array(_comments):
            update_comment_cache(_comments)
            self.items = php_array_slice(_comments, 0, comments_per_page)
            self.extra_items = php_array_slice(_comments, comments_per_page)
            _comment_post_ids = array_unique(wp_list_pluck(_comments, "comment_post_ID"))
            self.pending_count = get_pending_comments_num(_comment_post_ids)
        # end if
        total_comments = get_comments(php_array_merge(args, Array({"count": True, "offset": 0, "number": 0})))
        self.set_pagination_args(Array({"total_items": total_comments, "per_page": comments_per_page}))
    # end def prepare_items
    #// 
    #// @param string $comment_status
    #// @return int
    #//
    def get_per_page(self, comment_status="all"):
        
        comments_per_page = self.get_items_per_page("edit_comments_per_page")
        #// 
        #// Filters the number of comments listed per page in the comments list table.
        #// 
        #// @since 2.6.0
        #// 
        #// @param int    $comments_per_page The number of comments to list per page.
        #// @param string $comment_status    The comment status name. Default 'All'.
        #//
        return apply_filters("comments_per_page", comments_per_page, comment_status)
    # end def get_per_page
    #// 
    #// @global string $comment_status
    #//
    def no_items(self):
        
        global comment_status
        php_check_if_defined("comment_status")
        if "moderated" == comment_status:
            _e("No comments awaiting moderation.")
        elif "trash" == comment_status:
            _e("No comments found in Trash.")
        else:
            _e("No comments found.")
        # end if
    # end def no_items
    #// 
    #// @global int $post_id
    #// @global string $comment_status
    #// @global string $comment_type
    #//
    def get_views(self):
        
        global post_id,comment_status,comment_type
        php_check_if_defined("post_id","comment_status","comment_type")
        status_links = Array()
        num_comments = wp_count_comments(post_id) if post_id else wp_count_comments()
        stati = Array({"all": _nx_noop("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", "comments"), "mine": _nx_noop("Mine <span class=\"count\">(%s)</span>", "Mine <span class=\"count\">(%s)</span>", "comments"), "moderated": _nx_noop("Pending <span class=\"count\">(%s)</span>", "Pending <span class=\"count\">(%s)</span>", "comments"), "approved": _nx_noop("Approved <span class=\"count\">(%s)</span>", "Approved <span class=\"count\">(%s)</span>", "comments"), "spam": _nx_noop("Spam <span class=\"count\">(%s)</span>", "Spam <span class=\"count\">(%s)</span>", "comments"), "trash": _nx_noop("Trash <span class=\"count\">(%s)</span>", "Trash <span class=\"count\">(%s)</span>", "comments")})
        if (not EMPTY_TRASH_DAYS):
            stati["trash"] = None
        # end if
        link = admin_url("edit-comments.php")
        if (not php_empty(lambda : comment_type)) and "all" != comment_type:
            link = add_query_arg("comment_type", comment_type, link)
        # end if
        for status,label in stati:
            current_link_attributes = ""
            if status == comment_status:
                current_link_attributes = " class=\"current\" aria-current=\"page\""
            # end if
            if "mine" == status:
                current_user_id = get_current_user_id()
                num_comments.mine = get_comments(Array({"post_id": post_id if post_id else 0, "user_id": current_user_id, "count": True}))
                link = add_query_arg("user_id", current_user_id, link)
            else:
                link = remove_query_arg("user_id", link)
            # end if
            if (not (php_isset(lambda : num_comments.status))):
                num_comments.status = 10
            # end if
            link = add_query_arg("comment_status", status, link)
            if post_id:
                link = add_query_arg("p", absint(post_id), link)
            # end if
            #// 
            #// I toyed with this, but decided against it. Leaving it in here in case anyone thinks it is a good idea. ~ Mark
            #// if ( !empty( $_REQUEST['s'] ) )
            #// $link = add_query_arg( 's', esc_attr( wp_unslash( $_REQUEST['s'] ) ), $link );
            #//
            status_links[status] = str("<a href='") + str(link) + str("'") + str(current_link_attributes) + str(">") + php_sprintf(translate_nooped_plural(label, num_comments.status), php_sprintf("<span class=\"%s-count\">%s</span>", "pending" if "moderated" == status else status, number_format_i18n(num_comments.status))) + "</a>"
        # end for
        #// 
        #// Filters the comment status links.
        #// 
        #// @since 2.5.0
        #// @since 5.1.0 The 'Mine' link was added.
        #// 
        #// @param string[] $status_links An associative array of fully-formed comment status links. Includes 'All', 'Mine',
        #// 'Pending', 'Approved', 'Spam', and 'Trash'.
        #//
        return apply_filters("comment_status_links", status_links)
    # end def get_views
    #// 
    #// @global string $comment_status
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        global comment_status
        php_check_if_defined("comment_status")
        actions = Array()
        if php_in_array(comment_status, Array("all", "approved")):
            actions["unapprove"] = __("Unapprove")
        # end if
        if php_in_array(comment_status, Array("all", "moderated")):
            actions["approve"] = __("Approve")
        # end if
        if php_in_array(comment_status, Array("all", "moderated", "approved", "trash")):
            actions["spam"] = _x("Mark as Spam", "comment")
        # end if
        if "trash" == comment_status:
            actions["untrash"] = __("Restore")
        elif "spam" == comment_status:
            actions["unspam"] = _x("Not Spam", "comment")
        # end if
        if php_in_array(comment_status, Array("trash", "spam")) or (not EMPTY_TRASH_DAYS):
            actions["delete"] = __("Delete Permanently")
        else:
            actions["trash"] = __("Move to Trash")
        # end if
        return actions
    # end def get_bulk_actions
    #// 
    #// @global string $comment_status
    #// @global string $comment_type
    #// 
    #// @param string $which
    #//
    def extra_tablenav(self, which=None):
        
        global comment_status,comment_type
        php_check_if_defined("comment_status","comment_type")
        has_items = None
        if (not (php_isset(lambda : has_items))):
            has_items = self.has_items()
        # end if
        php_print("     <div class=\"alignleft actions\">\n     ")
        if "top" == which:
            php_print(" <label class=\"screen-reader-text\" for=\"filter-by-comment-type\">")
            _e("Filter by comment type")
            php_print("</label>\n   <select id=\"filter-by-comment-type\" name=\"comment_type\">\n      <option value=\"\">")
            _e("All comment types")
            php_print("</option>\n          ")
            #// 
            #// Filters the comment types dropdown menu.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $comment_types An array of comment types. Accepts 'Comments', 'Pings'.
            #//
            comment_types = apply_filters("admin_comment_types_dropdown", Array({"comment": __("Comments"), "pings": __("Pings")}))
            for type,label in comment_types:
                php_print(" " + "<option value=\"" + esc_attr(type) + "\"" + selected(comment_type, type, False) + str(">") + str(label) + str("</option>\n"))
            # end for
            php_print(" </select>\n         ")
            #// 
            #// Fires just before the Filter submit button for comment types.
            #// 
            #// @since 3.5.0
            #//
            do_action("restrict_manage_comments")
            submit_button(__("Filter"), "", "filter_action", False, Array({"id": "post-query-submit"}))
        # end if
        if "spam" == comment_status or "trash" == comment_status and current_user_can("moderate_comments") and has_items:
            wp_nonce_field("bulk-destroy", "_destroy_nonce")
            title = esc_attr__("Empty Spam") if "spam" == comment_status else esc_attr__("Empty Trash")
            submit_button(title, "apply", "delete_all", False)
        # end if
        #// 
        #// Fires after the Filter submit button for comment types.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string $comment_status The comment status name. Default 'All'.
        #//
        do_action("manage_comments_nav", comment_status)
        php_print("</div>")
    # end def extra_tablenav
    #// 
    #// @return string|false
    #//
    def current_action(self):
        
        if (php_isset(lambda : PHP_REQUEST["delete_all"])) or (php_isset(lambda : PHP_REQUEST["delete_all2"])):
            return "delete_all"
        # end if
        return super().current_action()
    # end def current_action
    #// 
    #// @global int $post_id
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        global post_id
        php_check_if_defined("post_id")
        columns = Array()
        if self.checkbox:
            columns["cb"] = "<input type=\"checkbox\" />"
        # end if
        columns["author"] = __("Author")
        columns["comment"] = _x("Comment", "column name")
        if (not post_id):
            #// translators: Column name or table row header.
            columns["response"] = __("In Response To")
        # end if
        columns["date"] = _x("Submitted On", "column name")
        return columns
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        return Array({"author": "comment_author", "response": "comment_post_ID", "date": "comment_date"})
    # end def get_sortable_columns
    #// 
    #// Get the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, 'comment'.
    #//
    def get_default_primary_column_name(self):
        
        return "comment"
    # end def get_default_primary_column_name
    #// 
    #// Displays the comments table.
    #// 
    #// Overrides the parent display() method to render extra comments.
    #// 
    #// @since 3.1.0
    #//
    def display(self):
        
        wp_nonce_field("fetch-list-" + get_class(self), "_ajax_fetch_list_nonce")
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
        <tbody id=\"the-comment-list\" data-wp-lists=\"list:comment\">
        """)
        self.display_rows_or_placeholder()
        php_print("""   </tbody>
        <tbody id=\"the-extra-comment-list\" data-wp-lists=\"list:comment\" style=\"display: none;\">
        """)
        #// 
        #// Back up the items to restore after printing the extra items markup.
        #// The extra items may be empty, which will prevent the table nav from displaying later.
        #//
        items = self.items
        self.items = self.extra_items
        self.display_rows_or_placeholder()
        self.items = items
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
    #// @global WP_Post    $post    Global post object.
    #// @global WP_Comment $comment Global comment object.
    #// 
    #// @param WP_Comment $item
    #//
    def single_row(self, item=None):
        
        global post,comment
        php_check_if_defined("post","comment")
        comment = item
        the_comment_class = wp_get_comment_status(comment)
        if (not the_comment_class):
            the_comment_class = ""
        # end if
        the_comment_class = join(" ", get_comment_class(the_comment_class, comment, comment.comment_post_ID))
        if comment.comment_post_ID > 0:
            post = get_post(comment.comment_post_ID)
        # end if
        self.user_can = current_user_can("edit_comment", comment.comment_ID)
        php_print(str("<tr id='comment-") + str(comment.comment_ID) + str("' class='") + str(the_comment_class) + str("'>"))
        self.single_row_columns(comment)
        php_print("</tr>\n")
        PHP_GLOBALS["post"] = None
        PHP_GLOBALS["comment"] = None
    # end def single_row
    #// 
    #// Generate and display row actions links.
    #// 
    #// @since 4.3.0
    #// 
    #// @global string $comment_status Status for the current listed comments.
    #// 
    #// @param WP_Comment $comment     The comment object.
    #// @param string     $column_name Current column name.
    #// @param string     $primary     Primary column name.
    #// @return string Row actions output for comments. An empty string
    #// if the current column is not the primary column,
    #// or if the current user cannot edit the comment.
    #//
    def handle_row_actions(self, comment=None, column_name=None, primary=None):
        
        global comment_status
        php_check_if_defined("comment_status")
        if primary != column_name:
            return ""
        # end if
        if (not self.user_can):
            return ""
        # end if
        the_comment_status = wp_get_comment_status(comment)
        out = ""
        del_nonce = esc_html("_wpnonce=" + wp_create_nonce(str("delete-comment_") + str(comment.comment_ID)))
        approve_nonce = esc_html("_wpnonce=" + wp_create_nonce(str("approve-comment_") + str(comment.comment_ID)))
        url = str("comment.php?c=") + str(comment.comment_ID)
        approve_url = esc_url(url + str("&action=approvecomment&") + str(approve_nonce))
        unapprove_url = esc_url(url + str("&action=unapprovecomment&") + str(approve_nonce))
        spam_url = esc_url(url + str("&action=spamcomment&") + str(del_nonce))
        unspam_url = esc_url(url + str("&action=unspamcomment&") + str(del_nonce))
        trash_url = esc_url(url + str("&action=trashcomment&") + str(del_nonce))
        untrash_url = esc_url(url + str("&action=untrashcomment&") + str(del_nonce))
        delete_url = esc_url(url + str("&action=deletecomment&") + str(del_nonce))
        #// Preorder it: Approve | Reply | Quick Edit | Edit | Spam | Trash.
        actions = Array({"approve": "", "unapprove": "", "reply": "", "quickedit": "", "edit": "", "spam": "", "unspam": "", "trash": "", "untrash": "", "delete": ""})
        #// Not looking at all comments.
        if comment_status and "all" != comment_status:
            if "approved" == the_comment_status:
                actions["unapprove"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-u vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", unapprove_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str(":e7e7d3:action=dim-comment&amp;new=unapproved"), esc_attr__("Unapprove this comment"), __("Unapprove"))
            elif "unapproved" == the_comment_status:
                actions["approve"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-a vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", approve_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str(":e7e7d3:action=dim-comment&amp;new=approved"), esc_attr__("Approve this comment"), __("Approve"))
            # end if
        else:
            actions["approve"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-a aria-button-if-js\" aria-label=\"%s\">%s</a>", approve_url, str("dim:the-comment-list:comment-") + str(comment.comment_ID) + str(":unapproved:e7e7d3:e7e7d3:new=approved"), esc_attr__("Approve this comment"), __("Approve"))
            actions["unapprove"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-u aria-button-if-js\" aria-label=\"%s\">%s</a>", unapprove_url, str("dim:the-comment-list:comment-") + str(comment.comment_ID) + str(":unapproved:e7e7d3:e7e7d3:new=unapproved"), esc_attr__("Unapprove this comment"), __("Unapprove"))
        # end if
        if "spam" != the_comment_status:
            actions["spam"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-s vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", spam_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str("::spam=1"), esc_attr__("Mark this comment as spam"), _x("Spam", "verb"))
        elif "spam" == the_comment_status:
            actions["unspam"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-z vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", unspam_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str(":66cc66:unspam=1"), esc_attr__("Restore this comment from the spam"), _x("Not Spam", "comment"))
        # end if
        if "trash" == the_comment_status:
            actions["untrash"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-z vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", untrash_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str(":66cc66:untrash=1"), esc_attr__("Restore this comment from the Trash"), __("Restore"))
        # end if
        if "spam" == the_comment_status or "trash" == the_comment_status or (not EMPTY_TRASH_DAYS):
            actions["delete"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"delete vim-d vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", delete_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str("::delete=1"), esc_attr__("Delete this comment permanently"), __("Delete Permanently"))
        else:
            actions["trash"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"delete vim-d vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", trash_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str("::trash=1"), esc_attr__("Move this comment to the Trash"), _x("Trash", "verb"))
        # end if
        if "spam" != the_comment_status and "trash" != the_comment_status:
            actions["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", str("comment.php?action=editcomment&amp;c=") + str(comment.comment_ID), esc_attr__("Edit this comment"), __("Edit"))
            format = "<button type=\"button\" data-comment-id=\"%d\" data-post-id=\"%d\" data-action=\"%s\" class=\"%s button-link\" aria-expanded=\"false\" aria-label=\"%s\">%s</button>"
            actions["quickedit"] = php_sprintf(format, comment.comment_ID, comment.comment_post_ID, "edit", "vim-q comment-inline", esc_attr__("Quick edit this comment inline"), __("Quick&nbsp;Edit"))
            actions["reply"] = php_sprintf(format, comment.comment_ID, comment.comment_post_ID, "replyto", "vim-r comment-inline", esc_attr__("Reply to this comment"), __("Reply"))
        # end if
        #// This filter is documented in wp-admin/includes/dashboard.php
        actions = apply_filters("comment_row_actions", php_array_filter(actions), comment)
        i = 0
        out += "<div class=\"row-actions\">"
        for action,link in actions:
            i += 1
            sep = "" if "approve" == action or "unapprove" == action and 2 == i or 1 == i else " | "
            #// Reply and quickedit need a hide-if-no-js span when not added with ajax.
            if "reply" == action or "quickedit" == action and (not wp_doing_ajax()):
                action += " hide-if-no-js"
            elif "untrash" == action and "trash" == the_comment_status or "unspam" == action and "spam" == the_comment_status:
                if "1" == get_comment_meta(comment.comment_ID, "_wp_trash_meta_status", True):
                    action += " approve"
                else:
                    action += " unapprove"
                # end if
            # end if
            out += str("<span class='") + str(action) + str("'>") + str(sep) + str(link) + str("</span>")
        # end for
        out += "</div>"
        out += "<button type=\"button\" class=\"toggle-row\"><span class=\"screen-reader-text\">" + __("Show more details") + "</span></button>"
        return out
    # end def handle_row_actions
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_cb(self, comment=None):
        
        if self.user_can:
            php_print("     <label class=\"screen-reader-text\" for=\"cb-select-")
            php_print(comment.comment_ID)
            php_print("\">")
            _e("Select comment")
            php_print("</label>\n       <input id=\"cb-select-")
            php_print(comment.comment_ID)
            php_print("\" type=\"checkbox\" name=\"delete_comments[]\" value=\"")
            php_print(comment.comment_ID)
            php_print("\" />\n          ")
        # end if
    # end def column_cb
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_comment(self, comment=None):
        
        php_print("<div class=\"comment-author\">")
        self.column_author(comment)
        php_print("</div>")
        if comment.comment_parent:
            parent = get_comment(comment.comment_parent)
            if parent:
                parent_link = esc_url(get_comment_link(parent))
                name = get_comment_author(parent)
                printf(__("In reply to %s."), "<a href=\"" + parent_link + "\">" + name + "</a>")
            # end if
        # end if
        comment_text(comment)
        if self.user_can:
            #// This filter is documented in wp-admin/includes/comment.php
            comment_content = apply_filters("comment_edit_pre", comment.comment_content)
            php_print("     <div id=\"inline-")
            php_print(comment.comment_ID)
            php_print("\" class=\"hidden\">\n           <textarea class=\"comment\" rows=\"1\" cols=\"1\">")
            php_print(esc_textarea(comment_content))
            php_print("</textarea>\n            <div class=\"author-email\">")
            php_print(esc_attr(comment.comment_author_email))
            php_print("</div>\n         <div class=\"author\">")
            php_print(esc_attr(comment.comment_author))
            php_print("</div>\n         <div class=\"author-url\">")
            php_print(esc_attr(comment.comment_author_url))
            php_print("</div>\n         <div class=\"comment_status\">")
            php_print(comment.comment_approved)
            php_print("</div>\n     </div>\n            ")
        # end if
    # end def column_comment
    #// 
    #// @global string $comment_status
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_author(self, comment=None):
        
        global comment_status
        php_check_if_defined("comment_status")
        author_url = get_comment_author_url(comment)
        author_url_display = untrailingslashit(php_preg_replace("|^http(s)?://(www\\.)?|i", "", author_url))
        if php_strlen(author_url_display) > 50:
            author_url_display = wp_html_excerpt(author_url_display, 49, "&hellip;")
        # end if
        php_print("<strong>")
        comment_author(comment)
        php_print("</strong><br />")
        if (not php_empty(lambda : author_url_display)):
            printf("<a href=\"%s\">%s</a><br />", esc_url(author_url), esc_html(author_url_display))
        # end if
        if self.user_can:
            if (not php_empty(lambda : comment.comment_author_email)):
                #// This filter is documented in wp-includes/comment-template.php
                email = apply_filters("comment_email", comment.comment_author_email, comment)
                if (not php_empty(lambda : email)) and "@" != email:
                    printf("<a href=\"%1$s\">%2$s</a><br />", esc_url("mailto:" + email), esc_html(email))
                # end if
            # end if
            author_ip = get_comment_author_IP(comment)
            if author_ip:
                author_ip_url = add_query_arg(Array({"s": author_ip, "mode": "detail"}), admin_url("edit-comments.php"))
                if "spam" == comment_status:
                    author_ip_url = add_query_arg("comment_status", "spam", author_ip_url)
                # end if
                printf("<a href=\"%1$s\">%2$s</a>", esc_url(author_ip_url), esc_html(author_ip))
            # end if
        # end if
    # end def column_author
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_date(self, comment=None):
        
        submitted = php_sprintf(__("%1$s at %2$s"), get_comment_date(__("Y/m/d"), comment), get_comment_date(__("g:i a"), comment))
        php_print("<div class=\"submitted-on\">")
        if "approved" == wp_get_comment_status(comment) and (not php_empty(lambda : comment.comment_post_ID)):
            printf("<a href=\"%s\">%s</a>", esc_url(get_comment_link(comment)), submitted)
        else:
            php_print(submitted)
        # end if
        php_print("</div>")
    # end def column_date
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_response(self, comment=None):
        
        post = get_post()
        if (not post):
            return
        # end if
        if (php_isset(lambda : self.pending_count[post.ID])):
            pending_comments = self.pending_count[post.ID]
        else:
            _pending_count_temp = get_pending_comments_num(Array(post.ID))
            pending_comments = _pending_count_temp[post.ID]
            self.pending_count[post.ID] = pending_comments
        # end if
        if current_user_can("edit_post", post.ID):
            post_link = "<a href='" + get_edit_post_link(post.ID) + "' class='comments-edit-item-link'>"
            post_link += esc_html(get_the_title(post.ID)) + "</a>"
        else:
            post_link = esc_html(get_the_title(post.ID))
        # end if
        php_print("<div class=\"response-links\">")
        if "attachment" == post.post_type:
            thumb = wp_get_attachment_image(post.ID, Array(80, 60), True)
            if thumb:
                php_print(thumb)
            # end if
        # end if
        php_print(post_link)
        post_type_object = get_post_type_object(post.post_type)
        php_print("<a href='" + get_permalink(post.ID) + "' class='comments-view-item-link'>" + post_type_object.labels.view_item + "</a>")
        php_print("<span class=\"post-com-count-wrapper post-com-count-", post.ID, "\">")
        self.comments_bubble(post.ID, pending_comments)
        php_print("</span> ")
        php_print("</div>")
    # end def column_response
    #// 
    #// @param WP_Comment $comment     The comment object.
    #// @param string     $column_name The custom column's name.
    #//
    def column_default(self, comment=None, column_name=None):
        
        #// 
        #// Fires when the default column output is displayed for a single row.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $column_name         The custom column's name.
        #// @param int    $comment->comment_ID The custom column's unique ID number.
        #//
        do_action("manage_comments_custom_column", column_name, comment.comment_ID)
    # end def column_default
# end class WP_Comments_List_Table
