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
#// WordPress Comment Administration API.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 2.3.0
#// 
#// 
#// Determine if a comment exists based on author and date.
#// 
#// For best performance, use `$timezone = 'gmt'`, which queries a field that is properly indexed. The default value
#// for `$timezone` is 'blog' for legacy reasons.
#// 
#// @since 2.0.0
#// @since 4.4.0 Added the `$timezone` parameter.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $comment_author Author of the comment.
#// @param string $comment_date   Date of the comment.
#// @param string $timezone       Timezone. Accepts 'blog' or 'gmt'. Default 'blog'.
#// 
#// @return mixed Comment post ID on success.
#//
def comment_exists(comment_author=None, comment_date=None, timezone="blog", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    date_field = "comment_date"
    if "gmt" == timezone:
        date_field = "comment_date_gmt"
    # end if
    return wpdb.get_var(wpdb.prepare(str("SELECT comment_post_ID FROM ") + str(wpdb.comments) + str("\n         WHERE comment_author = %s AND ") + str(date_field) + str(" = %s"), stripslashes(comment_author), stripslashes(comment_date)))
# end def comment_exists
#// 
#// Update a comment with values provided in $_POST.
#// 
#// @since 2.0.0
#//
def edit_comment(*args_):
    global PHP_POST
    if (not current_user_can("edit_comment", int(PHP_POST["comment_ID"]))):
        wp_die(__("Sorry, you are not allowed to edit comments on this post."))
    # end if
    if (php_isset(lambda : PHP_POST["newcomment_author"])):
        PHP_POST["comment_author"] = PHP_POST["newcomment_author"]
    # end if
    if (php_isset(lambda : PHP_POST["newcomment_author_email"])):
        PHP_POST["comment_author_email"] = PHP_POST["newcomment_author_email"]
    # end if
    if (php_isset(lambda : PHP_POST["newcomment_author_url"])):
        PHP_POST["comment_author_url"] = PHP_POST["newcomment_author_url"]
    # end if
    if (php_isset(lambda : PHP_POST["comment_status"])):
        PHP_POST["comment_approved"] = PHP_POST["comment_status"]
    # end if
    if (php_isset(lambda : PHP_POST["content"])):
        PHP_POST["comment_content"] = PHP_POST["content"]
    # end if
    if (php_isset(lambda : PHP_POST["comment_ID"])):
        PHP_POST["comment_ID"] = int(PHP_POST["comment_ID"])
    # end if
    for timeunit in Array("aa", "mm", "jj", "hh", "mn"):
        if (not php_empty(lambda : PHP_POST["hidden_" + timeunit])) and PHP_POST["hidden_" + timeunit] != PHP_POST[timeunit]:
            PHP_POST["edit_date"] = "1"
            break
        # end if
    # end for
    if (not php_empty(lambda : PHP_POST["edit_date"])):
        aa = PHP_POST["aa"]
        mm = PHP_POST["mm"]
        jj = PHP_POST["jj"]
        hh = PHP_POST["hh"]
        mn = PHP_POST["mn"]
        ss = PHP_POST["ss"]
        jj = 31 if jj > 31 else jj
        hh = hh - 24 if hh > 23 else hh
        mn = mn - 60 if mn > 59 else mn
        ss = ss - 60 if ss > 59 else ss
        PHP_POST["comment_date"] = str(aa) + str("-") + str(mm) + str("-") + str(jj) + str(" ") + str(hh) + str(":") + str(mn) + str(":") + str(ss)
    # end if
    wp_update_comment(PHP_POST)
# end def edit_comment
#// 
#// Returns a WP_Comment object based on comment ID.
#// 
#// @since 2.0.0
#// 
#// @param int $id ID of comment to retrieve.
#// @return WP_Comment|false Comment if found. False on failure.
#//
def get_comment_to_edit(id=None, *args_):
    
    comment = get_comment(id)
    if (not comment):
        return False
    # end if
    comment.comment_ID = int(comment.comment_ID)
    comment.comment_post_ID = int(comment.comment_post_ID)
    comment.comment_content = format_to_edit(comment.comment_content)
    #// 
    #// Filters the comment content before editing.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $comment->comment_content Comment content.
    #//
    comment.comment_content = apply_filters("comment_edit_pre", comment.comment_content)
    comment.comment_author = format_to_edit(comment.comment_author)
    comment.comment_author_email = format_to_edit(comment.comment_author_email)
    comment.comment_author_url = format_to_edit(comment.comment_author_url)
    comment.comment_author_url = esc_url(comment.comment_author_url)
    return comment
# end def get_comment_to_edit
#// 
#// Get the number of pending comments on a post or posts
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|array $post_id Either a single Post ID or an array of Post IDs
#// @return int|array Either a single Posts pending comments as an int or an array of ints keyed on the Post IDs
#//
def get_pending_comments_num(post_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    single = False
    if (not php_is_array(post_id)):
        post_id_array = post_id
        single = True
    else:
        post_id_array = post_id
    # end if
    post_id_array = php_array_map("intval", post_id_array)
    post_id_in = "'" + php_implode("', '", post_id_array) + "'"
    pending = wpdb.get_results(str("SELECT comment_post_ID, COUNT(comment_ID) as num_comments FROM ") + str(wpdb.comments) + str(" WHERE comment_post_ID IN ( ") + str(post_id_in) + str(" ) AND comment_approved = '0' GROUP BY comment_post_ID"), ARRAY_A)
    if single:
        if php_empty(lambda : pending):
            return 0
        else:
            return absint(pending[0]["num_comments"])
        # end if
    # end if
    pending_keyed = Array()
    #// Default to zero pending for all posts in request.
    for id in post_id_array:
        pending_keyed[id] = 0
    # end for
    if (not php_empty(lambda : pending)):
        for pend in pending:
            pending_keyed[pend["comment_post_ID"]] = absint(pend["num_comments"])
        # end for
    # end if
    return pending_keyed
# end def get_pending_comments_num
#// 
#// Add avatars to relevant places in admin, or try to.
#// 
#// @since 2.5.0
#// 
#// @param string $name User name.
#// @return string Avatar with Admin name.
#//
def floated_admin_avatar(name=None, *args_):
    
    avatar = get_avatar(get_comment(), 32, "mystery")
    return str(avatar) + str(" ") + str(name)
# end def floated_admin_avatar
#// 
#// @since 2.7.0
#//
def enqueue_comment_hotkeys_js(*args_):
    
    if "true" == get_user_option("comment_shortcuts"):
        wp_enqueue_script("jquery-table-hotkeys")
    # end if
# end def enqueue_comment_hotkeys_js
#// 
#// Display error message at bottom of comments.
#// 
#// @param string $msg Error Message. Assumed to contain HTML and be sanitized.
#//
def comment_footer_die(msg=None, *args_):
    
    php_print(str("<div class='wrap'><p>") + str(msg) + str("</p></div>"))
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    php_exit(0)
# end def comment_footer_die
