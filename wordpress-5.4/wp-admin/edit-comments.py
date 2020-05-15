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
wp_list_table = _get_list_table("WP_Comments_List_Table")
pagenum = wp_list_table.get_pagenum()
doaction = wp_list_table.current_action()
if doaction:
    check_admin_referer("bulk-comments")
    if "delete_all" == doaction and (not php_empty(lambda : PHP_REQUEST["pagegen_timestamp"])):
        comment_status = wp_unslash(PHP_REQUEST["comment_status"])
        delete_time = wp_unslash(PHP_REQUEST["pagegen_timestamp"])
        comment_ids = wpdb.get_col(wpdb.prepare(str("SELECT comment_ID FROM ") + str(wpdb.comments) + str(" WHERE comment_approved = %s AND %s > comment_date_gmt"), comment_status, delete_time))
        doaction = "delete"
    elif (php_isset(lambda : PHP_REQUEST["delete_comments"])):
        comment_ids = PHP_REQUEST["delete_comments"]
        doaction = PHP_REQUEST["action"] if -1 != PHP_REQUEST["action"] else PHP_REQUEST["action2"]
    elif (php_isset(lambda : PHP_REQUEST["ids"])):
        comment_ids = php_array_map("absint", php_explode(",", PHP_REQUEST["ids"]))
    elif wp_get_referer():
        wp_safe_redirect(wp_get_referer())
        php_exit(0)
    # end if
    approved = 0
    unapproved = 0
    spammed = 0
    unspammed = 0
    trashed = 0
    untrashed = 0
    deleted = 0
    redirect_to = remove_query_arg(Array("trashed", "untrashed", "deleted", "spammed", "unspammed", "approved", "unapproved", "ids"), wp_get_referer())
    redirect_to = add_query_arg("paged", pagenum, redirect_to)
    wp_defer_comment_counting(True)
    for comment_id in comment_ids:
        #// Check the permissions on each.
        if (not current_user_can("edit_comment", comment_id)):
            continue
        # end if
        for case in Switch(doaction):
            if case("approve"):
                wp_set_comment_status(comment_id, "approve")
                approved += 1
                break
            # end if
            if case("unapprove"):
                wp_set_comment_status(comment_id, "hold")
                unapproved += 1
                break
            # end if
            if case("spam"):
                wp_spam_comment(comment_id)
                spammed += 1
                break
            # end if
            if case("unspam"):
                wp_unspam_comment(comment_id)
                unspammed += 1
                break
            # end if
            if case("trash"):
                wp_trash_comment(comment_id)
                trashed += 1
                break
            # end if
            if case("untrash"):
                wp_untrash_comment(comment_id)
                untrashed += 1
                break
            # end if
            if case("delete"):
                wp_delete_comment(comment_id)
                deleted += 1
                break
            # end if
        # end for
    # end for
    if (not php_in_array(doaction, Array("approve", "unapprove", "spam", "unspam", "trash", "delete"), True)):
        screen = get_current_screen().id
        #// This action is documented in wp-admin/edit.php
        redirect_to = apply_filters(str("handle_bulk_actions-") + str(screen), redirect_to, doaction, comment_ids)
        pass
    # end if
    wp_defer_comment_counting(False)
    if approved:
        redirect_to = add_query_arg("approved", approved, redirect_to)
    # end if
    if unapproved:
        redirect_to = add_query_arg("unapproved", unapproved, redirect_to)
    # end if
    if spammed:
        redirect_to = add_query_arg("spammed", spammed, redirect_to)
    # end if
    if unspammed:
        redirect_to = add_query_arg("unspammed", unspammed, redirect_to)
    # end if
    if trashed:
        redirect_to = add_query_arg("trashed", trashed, redirect_to)
    # end if
    if untrashed:
        redirect_to = add_query_arg("untrashed", untrashed, redirect_to)
    # end if
    if deleted:
        redirect_to = add_query_arg("deleted", deleted, redirect_to)
    # end if
    if trashed or spammed:
        redirect_to = add_query_arg("ids", join(",", comment_ids), redirect_to)
    # end if
    wp_safe_redirect(redirect_to)
    php_exit(0)
elif (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
    wp_redirect(remove_query_arg(Array("_wp_http_referer", "_wpnonce"), wp_unslash(PHP_SERVER["REQUEST_URI"])))
    php_exit(0)
# end if
wp_list_table.prepare_items()
wp_enqueue_script("admin-comments")
enqueue_comment_hotkeys_js()
if post_id:
    comments_count = wp_count_comments(post_id)
    draft_or_post_title = wp_html_excerpt(_draft_or_post_title(post_id), 50, "&hellip;")
    if comments_count.moderated > 0:
        title = php_sprintf(__("Comments (%1$s) on &#8220;%2$s&#8221;"), number_format_i18n(comments_count.moderated), draft_or_post_title)
    else:
        title = php_sprintf(__("Comments on &#8220;%s&#8221;"), draft_or_post_title)
    # end if
else:
    comments_count = wp_count_comments()
    if comments_count.moderated > 0:
        title = php_sprintf(__("Comments (%s)"), number_format_i18n(comments_count.moderated))
    else:
        title = __("Comments")
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
if post_id:
    printf(__("Comments on &#8220;%s&#8221;"), php_sprintf("<a href=\"%1$s\">%2$s</a>", get_edit_post_link(post_id), wp_html_excerpt(_draft_or_post_title(post_id), 50, "&hellip;")))
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
    error = int(PHP_REQUEST["error"])
    error_msg = ""
    for case in Switch(error):
        if case(1):
            error_msg = __("Invalid comment ID.")
            break
        # end if
        if case(2):
            error_msg = __("Sorry, you are not allowed to edit comments on this post.")
            break
        # end if
    # end for
    if error_msg:
        php_print("<div id=\"moderated\" class=\"error\"><p>" + error_msg + "</p></div>")
    # end if
# end if
if (php_isset(lambda : PHP_REQUEST["approved"])) or (php_isset(lambda : PHP_REQUEST["deleted"])) or (php_isset(lambda : PHP_REQUEST["trashed"])) or (php_isset(lambda : PHP_REQUEST["untrashed"])) or (php_isset(lambda : PHP_REQUEST["spammed"])) or (php_isset(lambda : PHP_REQUEST["unspammed"])) or (php_isset(lambda : PHP_REQUEST["same"])):
    approved = int(PHP_REQUEST["approved"]) if (php_isset(lambda : PHP_REQUEST["approved"])) else 0
    deleted = int(PHP_REQUEST["deleted"]) if (php_isset(lambda : PHP_REQUEST["deleted"])) else 0
    trashed = int(PHP_REQUEST["trashed"]) if (php_isset(lambda : PHP_REQUEST["trashed"])) else 0
    untrashed = int(PHP_REQUEST["untrashed"]) if (php_isset(lambda : PHP_REQUEST["untrashed"])) else 0
    spammed = int(PHP_REQUEST["spammed"]) if (php_isset(lambda : PHP_REQUEST["spammed"])) else 0
    unspammed = int(PHP_REQUEST["unspammed"]) if (php_isset(lambda : PHP_REQUEST["unspammed"])) else 0
    same = int(PHP_REQUEST["same"]) if (php_isset(lambda : PHP_REQUEST["same"])) else 0
    if approved > 0 or deleted > 0 or trashed > 0 or untrashed > 0 or spammed > 0 or unspammed > 0 or same > 0:
        if approved > 0:
            #// translators: %s: Number of comments.
            messages[-1] = php_sprintf(_n("%s comment approved.", "%s comments approved.", approved), approved)
        # end if
        if spammed > 0:
            ids = PHP_REQUEST["ids"] if (php_isset(lambda : PHP_REQUEST["ids"])) else 0
            #// translators: %s: Number of comments.
            messages[-1] = php_sprintf(_n("%s comment marked as spam.", "%s comments marked as spam.", spammed), spammed) + " <a href=\"" + esc_url(wp_nonce_url(str("edit-comments.php?doaction=undo&action=unspam&ids=") + str(ids), "bulk-comments")) + "\">" + __("Undo") + "</a><br />"
        # end if
        if unspammed > 0:
            #// translators: %s: Number of comments.
            messages[-1] = php_sprintf(_n("%s comment restored from the spam.", "%s comments restored from the spam.", unspammed), unspammed)
        # end if
        if trashed > 0:
            ids = PHP_REQUEST["ids"] if (php_isset(lambda : PHP_REQUEST["ids"])) else 0
            #// translators: %s: Number of comments.
            messages[-1] = php_sprintf(_n("%s comment moved to the Trash.", "%s comments moved to the Trash.", trashed), trashed) + " <a href=\"" + esc_url(wp_nonce_url(str("edit-comments.php?doaction=undo&action=untrash&ids=") + str(ids), "bulk-comments")) + "\">" + __("Undo") + "</a><br />"
        # end if
        if untrashed > 0:
            #// translators: %s: Number of comments.
            messages[-1] = php_sprintf(_n("%s comment restored from the Trash.", "%s comments restored from the Trash.", untrashed), untrashed)
        # end if
        if deleted > 0:
            #// translators: %s: Number of comments.
            messages[-1] = php_sprintf(_n("%s comment permanently deleted.", "%s comments permanently deleted.", deleted), deleted)
        # end if
        if same > 0:
            comment = get_comment(same)
            if comment:
                for case in Switch(comment.comment_approved):
                    if case("1"):
                        messages[-1] = __("This comment is already approved.") + " <a href=\"" + esc_url(admin_url(str("comment.php?action=editcomment&c=") + str(same))) + "\">" + __("Edit comment") + "</a>"
                        break
                    # end if
                    if case("trash"):
                        messages[-1] = __("This comment is already in the Trash.") + " <a href=\"" + esc_url(admin_url("edit-comments.php?comment_status=trash")) + "\"> " + __("View Trash") + "</a>"
                        break
                    # end if
                    if case("spam"):
                        messages[-1] = __("This comment is already marked as spam.") + " <a href=\"" + esc_url(admin_url(str("comment.php?action=editcomment&c=") + str(same))) + "\">" + __("Edit comment") + "</a>"
                        break
                    # end if
                # end for
            # end if
        # end if
        php_print("<div id=\"moderated\" class=\"updated notice is-dismissible\"><p>" + php_implode("<br/>\n", messages) + "</p></div>")
    # end if
# end if
php_print("\n")
wp_list_table.views()
php_print("""
<form id=\"comments-form\" method=\"get\">
""")
wp_list_table.search_box(__("Search Comments"), "comment")
php_print("\n")
if post_id:
    php_print("<input type=\"hidden\" name=\"p\" value=\"")
    php_print(esc_attr(php_intval(post_id)))
    php_print("\" />\n")
# end if
php_print("<input type=\"hidden\" name=\"comment_status\" value=\"")
php_print(esc_attr(comment_status))
php_print("\" />\n<input type=\"hidden\" name=\"pagegen_timestamp\" value=\"")
php_print(esc_attr(current_time("mysql", 1)))
php_print("\" />\n\n<input type=\"hidden\" name=\"_total\" value=\"")
php_print(esc_attr(wp_list_table.get_pagination_arg("total_items")))
php_print("\" />\n<input type=\"hidden\" name=\"_per_page\" value=\"")
php_print(esc_attr(wp_list_table.get_pagination_arg("per_page")))
php_print("\" />\n<input type=\"hidden\" name=\"_page\" value=\"")
php_print(esc_attr(wp_list_table.get_pagination_arg("page")))
php_print("\" />\n\n")
if (php_isset(lambda : PHP_REQUEST["paged"])):
    php_print(" <input type=\"hidden\" name=\"paged\" value=\"")
    php_print(esc_attr(absint(PHP_REQUEST["paged"])))
    php_print("\" />\n")
# end if
php_print("\n")
wp_list_table.display()
php_print("""</form>
</div>
<div id=\"ajax-response\"></div>
""")
wp_comment_reply("-1", True, "detail")
wp_comment_trashnotice()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
