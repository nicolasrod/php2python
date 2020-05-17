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
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        global post_id_
        php_check_if_defined("post_id_")
        post_id_ = absint(PHP_REQUEST["p"]) if (php_isset(lambda : PHP_REQUEST["p"])) else 0
        if get_option("show_avatars"):
            add_filter("comment_author", Array(self, "floated_admin_avatar"), 10, 2)
        # end if
        super().__init__(Array({"plural": "comments", "singular": "comment", "ajax": True, "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
    # end def __init__
    def floated_admin_avatar(self, name_=None, comment_ID_=None):
        
        
        comment_ = get_comment(comment_ID_)
        avatar_ = get_avatar(comment_, 32, "mystery")
        return str(avatar_) + str(" ") + str(name_)
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
        
        
        global post_id_
        global comment_status_
        global search_
        global comment_type_
        php_check_if_defined("post_id_","comment_status_","search_","comment_type_")
        comment_status_ = PHP_REQUEST["comment_status"] if (php_isset(lambda : PHP_REQUEST["comment_status"])) else "all"
        if (not php_in_array(comment_status_, Array("all", "mine", "moderated", "approved", "spam", "trash"))):
            comment_status_ = "all"
        # end if
        comment_type_ = PHP_REQUEST["comment_type"] if (not php_empty(lambda : PHP_REQUEST["comment_type"])) else ""
        search_ = PHP_REQUEST["s"] if (php_isset(lambda : PHP_REQUEST["s"])) else ""
        post_type_ = sanitize_key(PHP_REQUEST["post_type"]) if (php_isset(lambda : PHP_REQUEST["post_type"])) else ""
        user_id_ = PHP_REQUEST["user_id"] if (php_isset(lambda : PHP_REQUEST["user_id"])) else ""
        orderby_ = PHP_REQUEST["orderby"] if (php_isset(lambda : PHP_REQUEST["orderby"])) else ""
        order_ = PHP_REQUEST["order"] if (php_isset(lambda : PHP_REQUEST["order"])) else ""
        comments_per_page_ = self.get_per_page(comment_status_)
        doing_ajax_ = wp_doing_ajax()
        if (php_isset(lambda : PHP_REQUEST["number"])):
            number_ = php_int(PHP_REQUEST["number"])
        else:
            number_ = comments_per_page_ + php_min(8, comments_per_page_)
            pass
        # end if
        page_ = self.get_pagenum()
        if (php_isset(lambda : PHP_REQUEST["start"])):
            start_ = PHP_REQUEST["start"]
        else:
            start_ = page_ - 1 * comments_per_page_
        # end if
        if doing_ajax_ and (php_isset(lambda : PHP_REQUEST["offset"])):
            start_ += PHP_REQUEST["offset"]
        # end if
        status_map_ = Array({"mine": "", "moderated": "hold", "approved": "approve", "all": ""})
        args_ = Array({"status": status_map_[comment_status_] if (php_isset(lambda : status_map_[comment_status_])) else comment_status_, "search": search_, "user_id": user_id_, "offset": start_, "number": number_, "post_id": post_id_, "type": comment_type_, "orderby": orderby_, "order": order_, "post_type": post_type_})
        #// 
        #// Filters the arguments for the comment query in the comments list table.
        #// 
        #// @since 5.1.0
        #// 
        #// @param array $args An array of get_comments() arguments.
        #//
        args_ = apply_filters("comments_list_table_query_args", args_)
        _comments_ = get_comments(args_)
        if php_is_array(_comments_):
            update_comment_cache(_comments_)
            self.items = php_array_slice(_comments_, 0, comments_per_page_)
            self.extra_items = php_array_slice(_comments_, comments_per_page_)
            _comment_post_ids_ = array_unique(wp_list_pluck(_comments_, "comment_post_ID"))
            self.pending_count = get_pending_comments_num(_comment_post_ids_)
        # end if
        total_comments_ = get_comments(php_array_merge(args_, Array({"count": True, "offset": 0, "number": 0})))
        self.set_pagination_args(Array({"total_items": total_comments_, "per_page": comments_per_page_}))
    # end def prepare_items
    #// 
    #// @param string $comment_status
    #// @return int
    #//
    def get_per_page(self, comment_status_="all"):
        
        
        comments_per_page_ = self.get_items_per_page("edit_comments_per_page")
        #// 
        #// Filters the number of comments listed per page in the comments list table.
        #// 
        #// @since 2.6.0
        #// 
        #// @param int    $comments_per_page The number of comments to list per page.
        #// @param string $comment_status    The comment status name. Default 'All'.
        #//
        return apply_filters("comments_per_page", comments_per_page_, comment_status_)
    # end def get_per_page
    #// 
    #// @global string $comment_status
    #//
    def no_items(self):
        
        
        global comment_status_
        php_check_if_defined("comment_status_")
        if "moderated" == comment_status_:
            _e("No comments awaiting moderation.")
        elif "trash" == comment_status_:
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
        
        
        global post_id_
        global comment_status_
        global comment_type_
        php_check_if_defined("post_id_","comment_status_","comment_type_")
        status_links_ = Array()
        num_comments_ = wp_count_comments(post_id_) if post_id_ else wp_count_comments()
        stati_ = Array({"all": _nx_noop("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", "comments"), "mine": _nx_noop("Mine <span class=\"count\">(%s)</span>", "Mine <span class=\"count\">(%s)</span>", "comments"), "moderated": _nx_noop("Pending <span class=\"count\">(%s)</span>", "Pending <span class=\"count\">(%s)</span>", "comments"), "approved": _nx_noop("Approved <span class=\"count\">(%s)</span>", "Approved <span class=\"count\">(%s)</span>", "comments"), "spam": _nx_noop("Spam <span class=\"count\">(%s)</span>", "Spam <span class=\"count\">(%s)</span>", "comments"), "trash": _nx_noop("Trash <span class=\"count\">(%s)</span>", "Trash <span class=\"count\">(%s)</span>", "comments")})
        if (not EMPTY_TRASH_DAYS):
            stati_["trash"] = None
        # end if
        link_ = admin_url("edit-comments.php")
        if (not php_empty(lambda : comment_type_)) and "all" != comment_type_:
            link_ = add_query_arg("comment_type", comment_type_, link_)
        # end if
        for status_,label_ in stati_:
            current_link_attributes_ = ""
            if status_ == comment_status_:
                current_link_attributes_ = " class=\"current\" aria-current=\"page\""
            # end if
            if "mine" == status_:
                current_user_id_ = get_current_user_id()
                num_comments_.mine = get_comments(Array({"post_id": post_id_ if post_id_ else 0, "user_id": current_user_id_, "count": True}))
                link_ = add_query_arg("user_id", current_user_id_, link_)
            else:
                link_ = remove_query_arg("user_id", link_)
            # end if
            if (not (php_isset(lambda : num_comments_.status_))):
                num_comments_.status_ = 10
            # end if
            link_ = add_query_arg("comment_status", status_, link_)
            if post_id_:
                link_ = add_query_arg("p", absint(post_id_), link_)
            # end if
            #// 
            #// I toyed with this, but decided against it. Leaving it in here in case anyone thinks it is a good idea. ~ Mark
            #// if ( !empty( $_REQUEST['s'] ) )
            #// $link = add_query_arg( 's', esc_attr( wp_unslash( $_REQUEST['s'] ) ), $link );
            #//
            status_links_[status_] = str("<a href='") + str(link_) + str("'") + str(current_link_attributes_) + str(">") + php_sprintf(translate_nooped_plural(label_, num_comments_.status_), php_sprintf("<span class=\"%s-count\">%s</span>", "pending" if "moderated" == status_ else status_, number_format_i18n(num_comments_.status_))) + "</a>"
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
        return apply_filters("comment_status_links", status_links_)
    # end def get_views
    #// 
    #// @global string $comment_status
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        global comment_status_
        php_check_if_defined("comment_status_")
        actions_ = Array()
        if php_in_array(comment_status_, Array("all", "approved")):
            actions_["unapprove"] = __("Unapprove")
        # end if
        if php_in_array(comment_status_, Array("all", "moderated")):
            actions_["approve"] = __("Approve")
        # end if
        if php_in_array(comment_status_, Array("all", "moderated", "approved", "trash")):
            actions_["spam"] = _x("Mark as Spam", "comment")
        # end if
        if "trash" == comment_status_:
            actions_["untrash"] = __("Restore")
        elif "spam" == comment_status_:
            actions_["unspam"] = _x("Not Spam", "comment")
        # end if
        if php_in_array(comment_status_, Array("trash", "spam")) or (not EMPTY_TRASH_DAYS):
            actions_["delete"] = __("Delete Permanently")
        else:
            actions_["trash"] = __("Move to Trash")
        # end if
        return actions_
    # end def get_bulk_actions
    #// 
    #// @global string $comment_status
    #// @global string $comment_type
    #// 
    #// @param string $which
    #//
    def extra_tablenav(self, which_=None):
        
        
        global comment_status_
        global comment_type_
        php_check_if_defined("comment_status_","comment_type_")
        has_items_ = None
        if (not (php_isset(lambda : has_items_))):
            has_items_ = self.has_items()
        # end if
        php_print("     <div class=\"alignleft actions\">\n     ")
        if "top" == which_:
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
            comment_types_ = apply_filters("admin_comment_types_dropdown", Array({"comment": __("Comments"), "pings": __("Pings")}))
            for type_,label_ in comment_types_:
                php_print(" " + "<option value=\"" + esc_attr(type_) + "\"" + selected(comment_type_, type_, False) + str(">") + str(label_) + str("</option>\n"))
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
        if "spam" == comment_status_ or "trash" == comment_status_ and current_user_can("moderate_comments") and has_items_:
            wp_nonce_field("bulk-destroy", "_destroy_nonce")
            title_ = esc_attr__("Empty Spam") if "spam" == comment_status_ else esc_attr__("Empty Trash")
            submit_button(title_, "apply", "delete_all", False)
        # end if
        #// 
        #// Fires after the Filter submit button for comment types.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string $comment_status The comment status name. Default 'All'.
        #//
        do_action("manage_comments_nav", comment_status_)
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
        
        
        global post_id_
        php_check_if_defined("post_id_")
        columns_ = Array()
        if self.checkbox:
            columns_["cb"] = "<input type=\"checkbox\" />"
        # end if
        columns_["author"] = __("Author")
        columns_["comment"] = _x("Comment", "column name")
        if (not post_id_):
            #// translators: Column name or table row header.
            columns_["response"] = __("In Response To")
        # end if
        columns_["date"] = _x("Submitted On", "column name")
        return columns_
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
        items_ = self.items
        self.items = self.extra_items
        self.display_rows_or_placeholder()
        self.items = items_
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
    def single_row(self, item_=None):
        
        
        global post_
        global comment_
        php_check_if_defined("post_","comment_")
        comment_ = item_
        the_comment_class_ = wp_get_comment_status(comment_)
        if (not the_comment_class_):
            the_comment_class_ = ""
        # end if
        the_comment_class_ = join(" ", get_comment_class(the_comment_class_, comment_, comment_.comment_post_ID))
        if comment_.comment_post_ID > 0:
            post_ = get_post(comment_.comment_post_ID)
        # end if
        self.user_can = current_user_can("edit_comment", comment_.comment_ID)
        php_print(str("<tr id='comment-") + str(comment_.comment_ID) + str("' class='") + str(the_comment_class_) + str("'>"))
        self.single_row_columns(comment_)
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
    def handle_row_actions(self, comment_=None, column_name_=None, primary_=None):
        
        
        global comment_status_
        php_check_if_defined("comment_status_")
        if primary_ != column_name_:
            return ""
        # end if
        if (not self.user_can):
            return ""
        # end if
        the_comment_status_ = wp_get_comment_status(comment_)
        out_ = ""
        del_nonce_ = esc_html("_wpnonce=" + wp_create_nonce(str("delete-comment_") + str(comment_.comment_ID)))
        approve_nonce_ = esc_html("_wpnonce=" + wp_create_nonce(str("approve-comment_") + str(comment_.comment_ID)))
        url_ = str("comment.php?c=") + str(comment_.comment_ID)
        approve_url_ = esc_url(url_ + str("&action=approvecomment&") + str(approve_nonce_))
        unapprove_url_ = esc_url(url_ + str("&action=unapprovecomment&") + str(approve_nonce_))
        spam_url_ = esc_url(url_ + str("&action=spamcomment&") + str(del_nonce_))
        unspam_url_ = esc_url(url_ + str("&action=unspamcomment&") + str(del_nonce_))
        trash_url_ = esc_url(url_ + str("&action=trashcomment&") + str(del_nonce_))
        untrash_url_ = esc_url(url_ + str("&action=untrashcomment&") + str(del_nonce_))
        delete_url_ = esc_url(url_ + str("&action=deletecomment&") + str(del_nonce_))
        #// Preorder it: Approve | Reply | Quick Edit | Edit | Spam | Trash.
        actions_ = Array({"approve": "", "unapprove": "", "reply": "", "quickedit": "", "edit": "", "spam": "", "unspam": "", "trash": "", "untrash": "", "delete": ""})
        #// Not looking at all comments.
        if comment_status_ and "all" != comment_status_:
            if "approved" == the_comment_status_:
                actions_["unapprove"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-u vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", unapprove_url_, str("delete:the-comment-list:comment-") + str(comment_.comment_ID) + str(":e7e7d3:action=dim-comment&amp;new=unapproved"), esc_attr__("Unapprove this comment"), __("Unapprove"))
            elif "unapproved" == the_comment_status_:
                actions_["approve"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-a vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", approve_url_, str("delete:the-comment-list:comment-") + str(comment_.comment_ID) + str(":e7e7d3:action=dim-comment&amp;new=approved"), esc_attr__("Approve this comment"), __("Approve"))
            # end if
        else:
            actions_["approve"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-a aria-button-if-js\" aria-label=\"%s\">%s</a>", approve_url_, str("dim:the-comment-list:comment-") + str(comment_.comment_ID) + str(":unapproved:e7e7d3:e7e7d3:new=approved"), esc_attr__("Approve this comment"), __("Approve"))
            actions_["unapprove"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-u aria-button-if-js\" aria-label=\"%s\">%s</a>", unapprove_url_, str("dim:the-comment-list:comment-") + str(comment_.comment_ID) + str(":unapproved:e7e7d3:e7e7d3:new=unapproved"), esc_attr__("Unapprove this comment"), __("Unapprove"))
        # end if
        if "spam" != the_comment_status_:
            actions_["spam"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-s vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", spam_url_, str("delete:the-comment-list:comment-") + str(comment_.comment_ID) + str("::spam=1"), esc_attr__("Mark this comment as spam"), _x("Spam", "verb"))
        elif "spam" == the_comment_status_:
            actions_["unspam"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-z vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", unspam_url_, str("delete:the-comment-list:comment-") + str(comment_.comment_ID) + str(":66cc66:unspam=1"), esc_attr__("Restore this comment from the spam"), _x("Not Spam", "comment"))
        # end if
        if "trash" == the_comment_status_:
            actions_["untrash"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-z vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", untrash_url_, str("delete:the-comment-list:comment-") + str(comment_.comment_ID) + str(":66cc66:untrash=1"), esc_attr__("Restore this comment from the Trash"), __("Restore"))
        # end if
        if "spam" == the_comment_status_ or "trash" == the_comment_status_ or (not EMPTY_TRASH_DAYS):
            actions_["delete"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"delete vim-d vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", delete_url_, str("delete:the-comment-list:comment-") + str(comment_.comment_ID) + str("::delete=1"), esc_attr__("Delete this comment permanently"), __("Delete Permanently"))
        else:
            actions_["trash"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"delete vim-d vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", trash_url_, str("delete:the-comment-list:comment-") + str(comment_.comment_ID) + str("::trash=1"), esc_attr__("Move this comment to the Trash"), _x("Trash", "verb"))
        # end if
        if "spam" != the_comment_status_ and "trash" != the_comment_status_:
            actions_["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", str("comment.php?action=editcomment&amp;c=") + str(comment_.comment_ID), esc_attr__("Edit this comment"), __("Edit"))
            format_ = "<button type=\"button\" data-comment-id=\"%d\" data-post-id=\"%d\" data-action=\"%s\" class=\"%s button-link\" aria-expanded=\"false\" aria-label=\"%s\">%s</button>"
            actions_["quickedit"] = php_sprintf(format_, comment_.comment_ID, comment_.comment_post_ID, "edit", "vim-q comment-inline", esc_attr__("Quick edit this comment inline"), __("Quick&nbsp;Edit"))
            actions_["reply"] = php_sprintf(format_, comment_.comment_ID, comment_.comment_post_ID, "replyto", "vim-r comment-inline", esc_attr__("Reply to this comment"), __("Reply"))
        # end if
        #// This filter is documented in wp-admin/includes/dashboard.php
        actions_ = apply_filters("comment_row_actions", php_array_filter(actions_), comment_)
        i_ = 0
        out_ += "<div class=\"row-actions\">"
        for action_,link_ in actions_:
            i_ += 1
            sep_ = "" if "approve" == action_ or "unapprove" == action_ and 2 == i_ or 1 == i_ else " | "
            #// Reply and quickedit need a hide-if-no-js span when not added with ajax.
            if "reply" == action_ or "quickedit" == action_ and (not wp_doing_ajax()):
                action_ += " hide-if-no-js"
            elif "untrash" == action_ and "trash" == the_comment_status_ or "unspam" == action_ and "spam" == the_comment_status_:
                if "1" == get_comment_meta(comment_.comment_ID, "_wp_trash_meta_status", True):
                    action_ += " approve"
                else:
                    action_ += " unapprove"
                # end if
            # end if
            out_ += str("<span class='") + str(action_) + str("'>") + str(sep_) + str(link_) + str("</span>")
        # end for
        out_ += "</div>"
        out_ += "<button type=\"button\" class=\"toggle-row\"><span class=\"screen-reader-text\">" + __("Show more details") + "</span></button>"
        return out_
    # end def handle_row_actions
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_cb(self, comment_=None):
        
        
        if self.user_can:
            php_print("     <label class=\"screen-reader-text\" for=\"cb-select-")
            php_print(comment_.comment_ID)
            php_print("\">")
            _e("Select comment")
            php_print("</label>\n       <input id=\"cb-select-")
            php_print(comment_.comment_ID)
            php_print("\" type=\"checkbox\" name=\"delete_comments[]\" value=\"")
            php_print(comment_.comment_ID)
            php_print("\" />\n          ")
        # end if
    # end def column_cb
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_comment(self, comment_=None):
        
        
        php_print("<div class=\"comment-author\">")
        self.column_author(comment_)
        php_print("</div>")
        if comment_.comment_parent:
            parent_ = get_comment(comment_.comment_parent)
            if parent_:
                parent_link_ = esc_url(get_comment_link(parent_))
                name_ = get_comment_author(parent_)
                printf(__("In reply to %s."), "<a href=\"" + parent_link_ + "\">" + name_ + "</a>")
            # end if
        # end if
        comment_text(comment_)
        if self.user_can:
            #// This filter is documented in wp-admin/includes/comment.php
            comment_content_ = apply_filters("comment_edit_pre", comment_.comment_content)
            php_print("     <div id=\"inline-")
            php_print(comment_.comment_ID)
            php_print("\" class=\"hidden\">\n           <textarea class=\"comment\" rows=\"1\" cols=\"1\">")
            php_print(esc_textarea(comment_content_))
            php_print("</textarea>\n            <div class=\"author-email\">")
            php_print(esc_attr(comment_.comment_author_email))
            php_print("</div>\n         <div class=\"author\">")
            php_print(esc_attr(comment_.comment_author))
            php_print("</div>\n         <div class=\"author-url\">")
            php_print(esc_attr(comment_.comment_author_url))
            php_print("</div>\n         <div class=\"comment_status\">")
            php_print(comment_.comment_approved)
            php_print("</div>\n     </div>\n            ")
        # end if
    # end def column_comment
    #// 
    #// @global string $comment_status
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_author(self, comment_=None):
        
        
        global comment_status_
        php_check_if_defined("comment_status_")
        author_url_ = get_comment_author_url(comment_)
        author_url_display_ = untrailingslashit(php_preg_replace("|^http(s)?://(www\\.)?|i", "", author_url_))
        if php_strlen(author_url_display_) > 50:
            author_url_display_ = wp_html_excerpt(author_url_display_, 49, "&hellip;")
        # end if
        php_print("<strong>")
        comment_author(comment_)
        php_print("</strong><br />")
        if (not php_empty(lambda : author_url_display_)):
            printf("<a href=\"%s\">%s</a><br />", esc_url(author_url_), esc_html(author_url_display_))
        # end if
        if self.user_can:
            if (not php_empty(lambda : comment_.comment_author_email)):
                #// This filter is documented in wp-includes/comment-template.php
                email_ = apply_filters("comment_email", comment_.comment_author_email, comment_)
                if (not php_empty(lambda : email_)) and "@" != email_:
                    printf("<a href=\"%1$s\">%2$s</a><br />", esc_url("mailto:" + email_), esc_html(email_))
                # end if
            # end if
            author_ip_ = get_comment_author_IP(comment_)
            if author_ip_:
                author_ip_url_ = add_query_arg(Array({"s": author_ip_, "mode": "detail"}), admin_url("edit-comments.php"))
                if "spam" == comment_status_:
                    author_ip_url_ = add_query_arg("comment_status", "spam", author_ip_url_)
                # end if
                printf("<a href=\"%1$s\">%2$s</a>", esc_url(author_ip_url_), esc_html(author_ip_))
            # end if
        # end if
    # end def column_author
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_date(self, comment_=None):
        
        
        submitted_ = php_sprintf(__("%1$s at %2$s"), get_comment_date(__("Y/m/d"), comment_), get_comment_date(__("g:i a"), comment_))
        php_print("<div class=\"submitted-on\">")
        if "approved" == wp_get_comment_status(comment_) and (not php_empty(lambda : comment_.comment_post_ID)):
            printf("<a href=\"%s\">%s</a>", esc_url(get_comment_link(comment_)), submitted_)
        else:
            php_print(submitted_)
        # end if
        php_print("</div>")
    # end def column_date
    #// 
    #// @param WP_Comment $comment The comment object.
    #//
    def column_response(self, comment_=None):
        
        
        post_ = get_post()
        if (not post_):
            return
        # end if
        if (php_isset(lambda : self.pending_count[post_.ID])):
            pending_comments_ = self.pending_count[post_.ID]
        else:
            _pending_count_temp_ = get_pending_comments_num(Array(post_.ID))
            pending_comments_ = _pending_count_temp_[post_.ID]
            self.pending_count[post_.ID] = pending_comments_
        # end if
        if current_user_can("edit_post", post_.ID):
            post_link_ = "<a href='" + get_edit_post_link(post_.ID) + "' class='comments-edit-item-link'>"
            post_link_ += esc_html(get_the_title(post_.ID)) + "</a>"
        else:
            post_link_ = esc_html(get_the_title(post_.ID))
        # end if
        php_print("<div class=\"response-links\">")
        if "attachment" == post_.post_type:
            thumb_ = wp_get_attachment_image(post_.ID, Array(80, 60), True)
            if thumb_:
                php_print(thumb_)
            # end if
        # end if
        php_print(post_link_)
        post_type_object_ = get_post_type_object(post_.post_type)
        php_print("<a href='" + get_permalink(post_.ID) + "' class='comments-view-item-link'>" + post_type_object_.labels.view_item + "</a>")
        php_print("<span class=\"post-com-count-wrapper post-com-count-", post_.ID, "\">")
        self.comments_bubble(post_.ID, pending_comments_)
        php_print("</span> ")
        php_print("</div>")
    # end def column_response
    #// 
    #// @param WP_Comment $comment     The comment object.
    #// @param string     $column_name The custom column's name.
    #//
    def column_default(self, comment_=None, column_name_=None):
        
        
        #// 
        #// Fires when the default column output is displayed for a single row.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $column_name         The custom column's name.
        #// @param int    $comment->comment_ID The custom column's unique ID number.
        #//
        do_action("manage_comments_custom_column", column_name_, comment_.comment_ID)
    # end def column_default
# end class WP_Comments_List_Table
