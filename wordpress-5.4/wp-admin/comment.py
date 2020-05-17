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
#// Comment Management Screen
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
parent_file_ = "edit-comments.php"
submenu_file_ = "edit-comments.php"
#// 
#// @global string $action
#//
global action_
php_check_if_defined("action_")
wp_reset_vars(Array("action"))
if (php_isset(lambda : PHP_POST["deletecomment"])):
    action_ = "deletecomment"
# end if
if "cdc" == action_:
    action_ = "delete"
elif "mac" == action_:
    action_ = "approve"
# end if
if (php_isset(lambda : PHP_REQUEST["dt"])):
    if "spam" == PHP_REQUEST["dt"]:
        action_ = "spam"
    elif "trash" == PHP_REQUEST["dt"]:
        action_ = "trash"
    # end if
# end if
for case in Switch(action_):
    if case("editcomment"):
        title_ = __("Edit Comment")
        get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can edit the information left in a comment if needed. This is often useful when you notice that a commenter has made a typographical error.") + "</p>" + "<p>" + __("You can also moderate the comment from this screen using the Status box, where you can also change the timestamp of the comment.") + "</p>"}))
        get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/comments-screen/\">Documentation on Comments</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
        wp_enqueue_script("comment")
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        comment_id_ = absint(PHP_REQUEST["c"])
        comment_ = get_comment(comment_id_)
        if (not comment_):
            comment_footer_die(__("Invalid comment ID.") + php_sprintf(" <a href=\"%s\">" + __("Go back") + "</a>.", "javascript:history.go(-1)"))
        # end if
        if (not current_user_can("edit_comment", comment_id_)):
            comment_footer_die(__("Sorry, you are not allowed to edit this comment."))
        # end if
        if "trash" == comment_.comment_approved:
            comment_footer_die(__("This comment is in the Trash. Please move it out of the Trash if you want to edit it."))
        # end if
        comment_ = get_comment_to_edit(comment_id_)
        php_include_file(ABSPATH + "wp-admin/edit-form-comment.php", once=False)
        break
    # end if
    if case("delete"):
        pass
    # end if
    if case("approve"):
        pass
    # end if
    if case("trash"):
        pass
    # end if
    if case("spam"):
        title_ = __("Moderate Comment")
        comment_id_ = absint(PHP_REQUEST["c"])
        comment_ = get_comment(comment_id_)
        if (not comment_):
            wp_redirect(admin_url("edit-comments.php?error=1"))
            php_exit(0)
        # end if
        if (not current_user_can("edit_comment", comment_.comment_ID)):
            wp_redirect(admin_url("edit-comments.php?error=2"))
            php_exit(0)
        # end if
        #// No need to re-approve/re-trash/re-spam a comment.
        if php_str_replace("1", "approve", comment_.comment_approved) == action_:
            wp_redirect(admin_url("edit-comments.php?same=" + comment_id_))
            php_exit(0)
        # end if
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        formaction_ = action_ + "comment"
        nonce_action_ = "approve-comment_" if "approve" == action_ else "delete-comment_"
        nonce_action_ += comment_id_
        php_print(" <div class=\"wrap\">\n\n    <h1>")
        php_print(esc_html(title_))
        php_print("</h1>\n\n        ")
        for case in Switch(action_):
            if case("spam"):
                caution_msg_ = __("You are about to mark the following comment as spam:")
                button_ = _x("Mark as Spam", "comment")
                break
            # end if
            if case("trash"):
                caution_msg_ = __("You are about to move the following comment to the Trash:")
                button_ = __("Move to Trash")
                break
            # end if
            if case("delete"):
                caution_msg_ = __("You are about to delete the following comment:")
                button_ = __("Permanently Delete Comment")
                break
            # end if
            if case():
                caution_msg_ = __("You are about to approve the following comment:")
                button_ = __("Approve Comment")
                break
            # end if
        # end for
        if "0" != comment_.comment_approved:
            #// If not unapproved.
            message_ = ""
            for case in Switch(comment_.comment_approved):
                if case("1"):
                    message_ = __("This comment is currently approved.")
                    break
                # end if
                if case("spam"):
                    message_ = __("This comment is currently marked as spam.")
                    break
                # end if
                if case("trash"):
                    message_ = __("This comment is currently in the Trash.")
                    break
                # end if
            # end for
            if message_:
                php_print("<div id=\"message\" class=\"notice notice-info\"><p>" + message_ + "</p></div>")
            # end if
        # end if
        php_print("<div id=\"message\" class=\"notice notice-warning\"><p><strong>")
        _e("Caution:")
        php_print("</strong> ")
        php_print(caution_msg_)
        php_print("""</p></div>
        <table class=\"form-table comment-ays\">
        <tr>
        <th scope=\"row\">""")
        _e("Author")
        php_print("</th>\n<td>")
        comment_author(comment_)
        php_print("</td>\n</tr>\n       ")
        if get_comment_author_email(comment_):
            php_print("<tr>\n<th scope=\"row\">")
            _e("Email")
            php_print("</th>\n<td>")
            comment_author_email(comment_)
            php_print("</td>\n</tr>\n")
        # end if
        php_print("     ")
        if get_comment_author_url(comment_):
            php_print("<tr>\n<th scope=\"row\">")
            _e("URL")
            php_print("</th>\n<td><a href=\"")
            comment_author_url(comment_)
            php_print("\">")
            comment_author_url(comment_)
            php_print("</a></td>\n</tr>\n")
        # end if
        php_print("<tr>\n   <th scope=\"row\">")
        #// translators: Column name or table row header.
        _e("In Response To")
        php_print("</th>\n  <td>\n      ")
        post_id_ = comment_.comment_post_ID
        if current_user_can("edit_post", post_id_):
            post_link_ = "<a href='" + esc_url(get_edit_post_link(post_id_)) + "'>"
            post_link_ += esc_html(get_the_title(post_id_)) + "</a>"
        else:
            post_link_ = esc_html(get_the_title(post_id_))
        # end if
        php_print(post_link_)
        if comment_.comment_parent:
            parent_ = get_comment(comment_.comment_parent)
            parent_link_ = esc_url(get_comment_link(parent_))
            name_ = get_comment_author(parent_)
            printf(" | " + __("In reply to %s."), "<a href=\"" + parent_link_ + "\">" + name_ + "</a>")
        # end if
        php_print("""   </td>
        </tr>
        <tr>
        <th scope=\"row\">""")
        _e("Submitted on")
        php_print("</th>\n  <td>\n      ")
        submitted_ = php_sprintf(__("%1$s at %2$s"), get_comment_date(__("Y/m/d"), comment_), get_comment_date(__("g:i a"), comment_))
        if "approved" == wp_get_comment_status(comment_) and (not php_empty(lambda : comment_.comment_post_ID)):
            php_print("<a href=\"" + esc_url(get_comment_link(comment_)) + "\">" + submitted_ + "</a>")
        else:
            php_print(submitted_)
        # end if
        php_print("""       </td>
        </tr>
        <tr>
        <th scope=\"row\">""")
        #// translators: Field name in comment form.
        _ex("Comment", "noun")
        php_print("</th>\n  <td class=\"comment-content\">\n        ")
        comment_text(comment_)
        php_print(" <p class=\"edit-comment\"><a href=\"")
        php_print(admin_url(str("comment.php?action=editcomment&amp;c=") + str(comment_.comment_ID)))
        php_print("\">")
        esc_html_e("Edit")
        php_print("""</a></p>
        </td>
        </tr>
        </table>
        <form action=\"comment.php\" method=\"get\" class=\"comment-ays-submit\">
        <p>
        """)
        submit_button(button_, "primary", "submit", False)
        php_print(" <a href=\"")
        php_print(admin_url("edit-comments.php"))
        php_print("\" class=\"button-cancel\">")
        esc_html_e("Cancel")
        php_print("""</a>
        </p>
        """)
        wp_nonce_field(nonce_action_)
        php_print(" <input type=\"hidden\" name=\"action\" value=\"")
        php_print(esc_attr(formaction_))
        php_print("\" />\n  <input type=\"hidden\" name=\"c\" value=\"")
        php_print(esc_attr(comment_.comment_ID))
        php_print("""\" />
        <input type=\"hidden\" name=\"noredir\" value=\"1\" />
        </form>
        </div>
        """)
        break
    # end if
    if case("deletecomment"):
        pass
    # end if
    if case("trashcomment"):
        pass
    # end if
    if case("untrashcomment"):
        pass
    # end if
    if case("spamcomment"):
        pass
    # end if
    if case("unspamcomment"):
        pass
    # end if
    if case("approvecomment"):
        pass
    # end if
    if case("unapprovecomment"):
        comment_id_ = absint(PHP_REQUEST["c"])
        if php_in_array(action_, Array("approvecomment", "unapprovecomment")):
            check_admin_referer("approve-comment_" + comment_id_)
        else:
            check_admin_referer("delete-comment_" + comment_id_)
        # end if
        noredir_ = (php_isset(lambda : PHP_REQUEST["noredir"]))
        comment_ = get_comment(comment_id_)
        if (not comment_):
            comment_footer_die(__("Invalid comment ID.") + php_sprintf(" <a href=\"%s\">" + __("Go back") + "</a>.", "edit-comments.php"))
        # end if
        if (not current_user_can("edit_comment", comment_.comment_ID)):
            comment_footer_die(__("Sorry, you are not allowed to edit comments on this post."))
        # end if
        if "" != wp_get_referer() and (not noredir_) and False == php_strpos(wp_get_referer(), "comment.php"):
            redir_ = wp_get_referer()
        elif "" != wp_get_original_referer() and (not noredir_):
            redir_ = wp_get_original_referer()
        elif php_in_array(action_, Array("approvecomment", "unapprovecomment")):
            redir_ = admin_url("edit-comments.php?p=" + absint(comment_.comment_post_ID))
        else:
            redir_ = admin_url("edit-comments.php")
        # end if
        redir_ = remove_query_arg(Array("spammed", "unspammed", "trashed", "untrashed", "deleted", "ids", "approved", "unapproved"), redir_)
        for case in Switch(action_):
            if case("deletecomment"):
                wp_delete_comment(comment_)
                redir_ = add_query_arg(Array({"deleted": "1"}), redir_)
                break
            # end if
            if case("trashcomment"):
                wp_trash_comment(comment_)
                redir_ = add_query_arg(Array({"trashed": "1", "ids": comment_id_}), redir_)
                break
            # end if
            if case("untrashcomment"):
                wp_untrash_comment(comment_)
                redir_ = add_query_arg(Array({"untrashed": "1"}), redir_)
                break
            # end if
            if case("spamcomment"):
                wp_spam_comment(comment_)
                redir_ = add_query_arg(Array({"spammed": "1", "ids": comment_id_}), redir_)
                break
            # end if
            if case("unspamcomment"):
                wp_unspam_comment(comment_)
                redir_ = add_query_arg(Array({"unspammed": "1"}), redir_)
                break
            # end if
            if case("approvecomment"):
                wp_set_comment_status(comment_, "approve")
                redir_ = add_query_arg(Array({"approved": 1}), redir_)
                break
            # end if
            if case("unapprovecomment"):
                wp_set_comment_status(comment_, "hold")
                redir_ = add_query_arg(Array({"unapproved": 1}), redir_)
                break
            # end if
        # end for
        wp_redirect(redir_)
        php_exit(0)
    # end if
    if case("editedcomment"):
        comment_id_ = absint(PHP_POST["comment_ID"])
        comment_post_id_ = absint(PHP_POST["comment_post_ID"])
        check_admin_referer("update-comment_" + comment_id_)
        edit_comment()
        location_ = str("edit-comments.php?p=") + str(comment_post_id_) if php_empty(lambda : PHP_POST["referredby"]) else PHP_POST["referredby"] + "#comment-" + comment_id_
        #// 
        #// Filters the URI the user is redirected to after editing a comment in the admin.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $location The URI the user will be redirected to.
        #// @param int $comment_id The ID of the comment being edited.
        #//
        location_ = apply_filters("comment_edit_redirect", location_, comment_id_)
        wp_redirect(location_)
        php_exit(0)
    # end if
    if case():
        wp_die(__("Unknown action."))
    # end if
# end for
#// End switch.
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
