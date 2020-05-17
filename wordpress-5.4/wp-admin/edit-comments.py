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
#// Edit Comments Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("edit_posts")):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit comments.") + "</p>", 403)
# end if
wp_list_table_ = _get_list_table("WP_Comments_List_Table")
pagenum_ = wp_list_table_.get_pagenum()
doaction_ = wp_list_table_.current_action()
if doaction_:
    check_admin_referer("bulk-comments")
    if "delete_all" == doaction_ and (not php_empty(lambda : PHP_REQUEST["pagegen_timestamp"])):
        comment_status_ = wp_unslash(PHP_REQUEST["comment_status"])
        delete_time_ = wp_unslash(PHP_REQUEST["pagegen_timestamp"])
        comment_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT comment_ID FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = %s AND %s > comment_date_gmt"), comment_status_, delete_time_))
        doaction_ = "delete"
    elif (php_isset(lambda : PHP_REQUEST["delete_comments"])):
        comment_ids_ = PHP_REQUEST["delete_comments"]
        doaction_ = PHP_REQUEST["action"] if -1 != PHP_REQUEST["action"] else PHP_REQUEST["action2"]
    elif (php_isset(lambda : PHP_REQUEST["ids"])):
        comment_ids_ = php_array_map("absint", php_explode(",", PHP_REQUEST["ids"]))
    elif wp_get_referer():
        wp_safe_redirect(wp_get_referer())
        php_exit(0)
    # end if
    approved_ = 0
    unapproved_ = 0
    spammed_ = 0
    unspammed_ = 0
    trashed_ = 0
    untrashed_ = 0
    deleted_ = 0
    redirect_to_ = remove_query_arg(Array("trashed", "untrashed", "deleted", "spammed", "unspammed", "approved", "unapproved", "ids"), wp_get_referer())
    redirect_to_ = add_query_arg("paged", pagenum_, redirect_to_)
    wp_defer_comment_counting(True)
    for comment_id_ in comment_ids_:
        #// Check the permissions on each.
        if (not current_user_can("edit_comment", comment_id_)):
            continue
        # end if
        for case in Switch(doaction_):
            if case("approve"):
                wp_set_comment_status(comment_id_, "approve")
                approved_ += 1
                break
            # end if
            if case("unapprove"):
                wp_set_comment_status(comment_id_, "hold")
                unapproved_ += 1
                break
            # end if
            if case("spam"):
                wp_spam_comment(comment_id_)
                spammed_ += 1
                break
            # end if
            if case("unspam"):
                wp_unspam_comment(comment_id_)
                unspammed_ += 1
                break
            # end if
            if case("trash"):
                wp_trash_comment(comment_id_)
                trashed_ += 1
                break
            # end if
            if case("untrash"):
                wp_untrash_comment(comment_id_)
                untrashed_ += 1
                break
            # end if
            if case("delete"):
                wp_delete_comment(comment_id_)
                deleted_ += 1
                break
            # end if
        # end for
    # end for
    if (not php_in_array(doaction_, Array("approve", "unapprove", "spam", "unspam", "trash", "delete"), True)):
        screen_ = get_current_screen().id
        #// This action is documented in wp-admin/edit.php
        redirect_to_ = apply_filters(str("handle_bulk_actions-") + str(screen_), redirect_to_, doaction_, comment_ids_)
        pass
    # end if
    wp_defer_comment_counting(False)
    if approved_:
        redirect_to_ = add_query_arg("approved", approved_, redirect_to_)
    # end if
    if unapproved_:
        redirect_to_ = add_query_arg("unapproved", unapproved_, redirect_to_)
    # end if
    if spammed_:
        redirect_to_ = add_query_arg("spammed", spammed_, redirect_to_)
    # end if
    if unspammed_:
        redirect_to_ = add_query_arg("unspammed", unspammed_, redirect_to_)
    # end if
    if trashed_:
        redirect_to_ = add_query_arg("trashed", trashed_, redirect_to_)
    # end if
    if untrashed_:
        redirect_to_ = add_query_arg("untrashed", untrashed_, redirect_to_)
    # end if
    if deleted_:
        redirect_to_ = add_query_arg("deleted", deleted_, redirect_to_)
    # end if
    if trashed_ or spammed_:
        redirect_to_ = add_query_arg("ids", join(",", comment_ids_), redirect_to_)
    # end if
    wp_safe_redirect(redirect_to_)
    php_exit(0)
elif (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
    wp_redirect(remove_query_arg(Array("_wp_http_referer", "_wpnonce"), wp_unslash(PHP_SERVER["REQUEST_URI"])))
    php_exit(0)
# end if
wp_list_table_.prepare_items()
wp_enqueue_script("admin-comments")
enqueue_comment_hotkeys_js()
if post_id_:
    comments_count_ = wp_count_comments(post_id_)
    draft_or_post_title_ = wp_html_excerpt(_draft_or_post_title(post_id_), 50, "&hellip;")
    if comments_count_.moderated > 0:
        title_ = php_sprintf(__("Comments (%1$s) on &#8220;%2$s&#8221;"), number_format_i18n(comments_count_.moderated), draft_or_post_title_)
    else:
        title_ = php_sprintf(__("Comments on &#8220;%s&#8221;"), draft_or_post_title_)
    # end if
else:
    comments_count_ = wp_count_comments()
    if comments_count_.moderated > 0:
        title_ = php_sprintf(__("Comments (%s)"), number_format_i18n(comments_count_.moderated))
    else:
        title_ = __("Comments")
    # end if
# end if
add_screen_option("per_page")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can manage comments made on your site similar to the way you manage posts and other content. This screen is customizable in the same ways as other management screens, and you can act on comments using the on-hover action links or the Bulk Actions.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "moderating-comments", "title": __("Moderating Comments"), "content": "<p>" + __("A red bar on the left means the comment is waiting for you to moderate it.") + "</p>" + "<p>" + __("In the <strong>Author</strong> column, in addition to the author&#8217;s name, email address, and blog URL, the commenter&#8217;s IP address is shown. Clicking on this link will show you all the comments made from this IP address.") + "</p>" + "<p>" + __("In the <strong>Comment</strong> column, hovering over any comment gives you options to approve, reply (and approve), quick edit, edit, spam mark, or trash that comment.") + "</p>" + "<p>" + __("In the <strong>In Response To</strong> column, there are three elements. The text is the name of the post that inspired the comment, and links to the post editor for that entry. The View Post link leads to that post on your live site. The small bubble with the number in it shows the number of approved comments that post has received. If there are pending comments, a red notification circle with the number of pending comments is displayed. Clicking the notification circle will filter the comments screen to show only pending comments on that post.") + "</p>" + "<p>" + __("In the <strong>Submitted On</strong> column, the date and time the comment was left on your site appears. Clicking on the date/time link will take you to that comment on your live site.") + "</p>" + "<p>" + __("Many people take advantage of keyboard shortcuts to moderate their comments more quickly. Use the link to the side to learn more.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/comments-screen/\">Documentation on Comments</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/comment-spam/\">Documentation on Comment Spam</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/keyboard-shortcuts/\">Documentation on Keyboard Shortcuts</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
get_current_screen().set_screen_reader_content(Array({"heading_views": __("Filter comments list"), "heading_pagination": __("Comments list navigation"), "heading_list": __("Comments list")}))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("""
<div class=\"wrap\">
<h1 class=\"wp-heading-inline\">
""")
if post_id_:
    printf(__("Comments on &#8220;%s&#8221;"), php_sprintf("<a href=\"%1$s\">%2$s</a>", get_edit_post_link(post_id_), wp_html_excerpt(_draft_or_post_title(post_id_), 50, "&hellip;")))
else:
    _e("Comments")
# end if
php_print("</h1>\n\n")
if (php_isset(lambda : PHP_REQUEST["s"])) and php_strlen(PHP_REQUEST["s"]):
    php_print("<span class=\"subtitle\">")
    printf(__("Search results for &#8220;%s&#8221;"), wp_html_excerpt(esc_html(wp_unslash(PHP_REQUEST["s"])), 50, "&hellip;"))
    php_print("</span>")
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
if (php_isset(lambda : PHP_REQUEST["error"])):
    error_ = php_int(PHP_REQUEST["error"])
    error_msg_ = ""
    for case in Switch(error_):
        if case(1):
            error_msg_ = __("Invalid comment ID.")
            break
        # end if
        if case(2):
            error_msg_ = __("Sorry, you are not allowed to edit comments on this post.")
            break
        # end if
    # end for
    if error_msg_:
        php_print("<div id=\"moderated\" class=\"error\"><p>" + error_msg_ + "</p></div>")
    # end if
# end if
if (php_isset(lambda : PHP_REQUEST["approved"])) or (php_isset(lambda : PHP_REQUEST["deleted"])) or (php_isset(lambda : PHP_REQUEST["trashed"])) or (php_isset(lambda : PHP_REQUEST["untrashed"])) or (php_isset(lambda : PHP_REQUEST["spammed"])) or (php_isset(lambda : PHP_REQUEST["unspammed"])) or (php_isset(lambda : PHP_REQUEST["same"])):
    approved_ = php_int(PHP_REQUEST["approved"]) if (php_isset(lambda : PHP_REQUEST["approved"])) else 0
    deleted_ = php_int(PHP_REQUEST["deleted"]) if (php_isset(lambda : PHP_REQUEST["deleted"])) else 0
    trashed_ = php_int(PHP_REQUEST["trashed"]) if (php_isset(lambda : PHP_REQUEST["trashed"])) else 0
    untrashed_ = php_int(PHP_REQUEST["untrashed"]) if (php_isset(lambda : PHP_REQUEST["untrashed"])) else 0
    spammed_ = php_int(PHP_REQUEST["spammed"]) if (php_isset(lambda : PHP_REQUEST["spammed"])) else 0
    unspammed_ = php_int(PHP_REQUEST["unspammed"]) if (php_isset(lambda : PHP_REQUEST["unspammed"])) else 0
    same_ = php_int(PHP_REQUEST["same"]) if (php_isset(lambda : PHP_REQUEST["same"])) else 0
    if approved_ > 0 or deleted_ > 0 or trashed_ > 0 or untrashed_ > 0 or spammed_ > 0 or unspammed_ > 0 or same_ > 0:
        if approved_ > 0:
            #// translators: %s: Number of comments.
            messages_[-1] = php_sprintf(_n("%s comment approved.", "%s comments approved.", approved_), approved_)
        # end if
        if spammed_ > 0:
            ids_ = PHP_REQUEST["ids"] if (php_isset(lambda : PHP_REQUEST["ids"])) else 0
            #// translators: %s: Number of comments.
            messages_[-1] = php_sprintf(_n("%s comment marked as spam.", "%s comments marked as spam.", spammed_), spammed_) + " <a href=\"" + esc_url(wp_nonce_url(str("edit-comments.php?doaction=undo&action=unspam&ids=") + str(ids_), "bulk-comments")) + "\">" + __("Undo") + "</a><br />"
        # end if
        if unspammed_ > 0:
            #// translators: %s: Number of comments.
            messages_[-1] = php_sprintf(_n("%s comment restored from the spam.", "%s comments restored from the spam.", unspammed_), unspammed_)
        # end if
        if trashed_ > 0:
            ids_ = PHP_REQUEST["ids"] if (php_isset(lambda : PHP_REQUEST["ids"])) else 0
            #// translators: %s: Number of comments.
            messages_[-1] = php_sprintf(_n("%s comment moved to the Trash.", "%s comments moved to the Trash.", trashed_), trashed_) + " <a href=\"" + esc_url(wp_nonce_url(str("edit-comments.php?doaction=undo&action=untrash&ids=") + str(ids_), "bulk-comments")) + "\">" + __("Undo") + "</a><br />"
        # end if
        if untrashed_ > 0:
            #// translators: %s: Number of comments.
            messages_[-1] = php_sprintf(_n("%s comment restored from the Trash.", "%s comments restored from the Trash.", untrashed_), untrashed_)
        # end if
        if deleted_ > 0:
            #// translators: %s: Number of comments.
            messages_[-1] = php_sprintf(_n("%s comment permanently deleted.", "%s comments permanently deleted.", deleted_), deleted_)
        # end if
        if same_ > 0:
            comment_ = get_comment(same_)
            if comment_:
                for case in Switch(comment_.comment_approved):
                    if case("1"):
                        messages_[-1] = __("This comment is already approved.") + " <a href=\"" + esc_url(admin_url(str("comment.php?action=editcomment&c=") + str(same_))) + "\">" + __("Edit comment") + "</a>"
                        break
                    # end if
                    if case("trash"):
                        messages_[-1] = __("This comment is already in the Trash.") + " <a href=\"" + esc_url(admin_url("edit-comments.php?comment_status=trash")) + "\"> " + __("View Trash") + "</a>"
                        break
                    # end if
                    if case("spam"):
                        messages_[-1] = __("This comment is already marked as spam.") + " <a href=\"" + esc_url(admin_url(str("comment.php?action=editcomment&c=") + str(same_))) + "\">" + __("Edit comment") + "</a>"
                        break
                    # end if
                # end for
            # end if
        # end if
        php_print("<div id=\"moderated\" class=\"updated notice is-dismissible\"><p>" + php_implode("<br/>\n", messages_) + "</p></div>")
    # end if
# end if
php_print("\n")
wp_list_table_.views()
php_print("""
<form id=\"comments-form\" method=\"get\">
""")
wp_list_table_.search_box(__("Search Comments"), "comment")
php_print("\n")
if post_id_:
    php_print("<input type=\"hidden\" name=\"p\" value=\"")
    php_print(esc_attr(php_intval(post_id_)))
    php_print("\" />\n")
# end if
php_print("<input type=\"hidden\" name=\"comment_status\" value=\"")
php_print(esc_attr(comment_status_))
php_print("\" />\n<input type=\"hidden\" name=\"pagegen_timestamp\" value=\"")
php_print(esc_attr(current_time("mysql", 1)))
php_print("\" />\n\n<input type=\"hidden\" name=\"_total\" value=\"")
php_print(esc_attr(wp_list_table_.get_pagination_arg("total_items")))
php_print("\" />\n<input type=\"hidden\" name=\"_per_page\" value=\"")
php_print(esc_attr(wp_list_table_.get_pagination_arg("per_page")))
php_print("\" />\n<input type=\"hidden\" name=\"_page\" value=\"")
php_print(esc_attr(wp_list_table_.get_pagination_arg("page")))
php_print("\" />\n\n")
if (php_isset(lambda : PHP_REQUEST["paged"])):
    php_print(" <input type=\"hidden\" name=\"paged\" value=\"")
    php_print(esc_attr(absint(PHP_REQUEST["paged"])))
    php_print("\" />\n")
# end if
php_print("\n")
wp_list_table_.display()
php_print("""</form>
</div>
<div id=\"ajax-response\"></div>
""")
wp_comment_reply("-1", True, "detail")
wp_comment_trashnotice()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
