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
def comment_exists(comment_author_=None, comment_date_=None, timezone_="blog", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    date_field_ = "comment_date"
    if "gmt" == timezone_:
        date_field_ = "comment_date_gmt"
    # end if
    return wpdb_.get_var(wpdb_.prepare(str("SELECT comment_post_ID FROM ") + str(wpdb_.comments) + str("\n          WHERE comment_author = %s AND ") + str(date_field_) + str(" = %s"), stripslashes(comment_author_), stripslashes(comment_date_)))
# end def comment_exists
#// 
#// Update a comment with values provided in $_POST.
#// 
#// @since 2.0.0
#//
def edit_comment(*_args_):
    
    global PHP_POST
    if (not current_user_can("edit_comment", php_int(PHP_POST["comment_ID"]))):
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
        PHP_POST["comment_ID"] = php_int(PHP_POST["comment_ID"])
    # end if
    for timeunit_ in Array("aa", "mm", "jj", "hh", "mn"):
        if (not php_empty(lambda : PHP_POST["hidden_" + timeunit_])) and PHP_POST["hidden_" + timeunit_] != PHP_POST[timeunit_]:
            PHP_POST["edit_date"] = "1"
            break
        # end if
    # end for
    if (not php_empty(lambda : PHP_POST["edit_date"])):
        aa_ = PHP_POST["aa"]
        mm_ = PHP_POST["mm"]
        jj_ = PHP_POST["jj"]
        hh_ = PHP_POST["hh"]
        mn_ = PHP_POST["mn"]
        ss_ = PHP_POST["ss"]
        jj_ = 31 if jj_ > 31 else jj_
        hh_ = hh_ - 24 if hh_ > 23 else hh_
        mn_ = mn_ - 60 if mn_ > 59 else mn_
        ss_ = ss_ - 60 if ss_ > 59 else ss_
        PHP_POST["comment_date"] = str(aa_) + str("-") + str(mm_) + str("-") + str(jj_) + str(" ") + str(hh_) + str(":") + str(mn_) + str(":") + str(ss_)
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
def get_comment_to_edit(id_=None, *_args_):
    
    
    comment_ = get_comment(id_)
    if (not comment_):
        return False
    # end if
    comment_.comment_ID = php_int(comment_.comment_ID)
    comment_.comment_post_ID = php_int(comment_.comment_post_ID)
    comment_.comment_content = format_to_edit(comment_.comment_content)
    #// 
    #// Filters the comment content before editing.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $comment->comment_content Comment content.
    #//
    comment_.comment_content = apply_filters("comment_edit_pre", comment_.comment_content)
    comment_.comment_author = format_to_edit(comment_.comment_author)
    comment_.comment_author_email = format_to_edit(comment_.comment_author_email)
    comment_.comment_author_url = format_to_edit(comment_.comment_author_url)
    comment_.comment_author_url = esc_url(comment_.comment_author_url)
    return comment_
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
def get_pending_comments_num(post_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    single_ = False
    if (not php_is_array(post_id_)):
        post_id_array_ = post_id_
        single_ = True
    else:
        post_id_array_ = post_id_
    # end if
    post_id_array_ = php_array_map("intval", post_id_array_)
    post_id_in_ = "'" + php_implode("', '", post_id_array_) + "'"
    pending_ = wpdb_.get_results(str("SELECT comment_post_ID, COUNT(comment_ID) as num_comments FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID IN ( ") + str(post_id_in_) + str(" ) AND comment_approved = '0' GROUP BY comment_post_ID"), ARRAY_A)
    if single_:
        if php_empty(lambda : pending_):
            return 0
        else:
            return absint(pending_[0]["num_comments"])
        # end if
    # end if
    pending_keyed_ = Array()
    #// Default to zero pending for all posts in request.
    for id_ in post_id_array_:
        pending_keyed_[id_] = 0
    # end for
    if (not php_empty(lambda : pending_)):
        for pend_ in pending_:
            pending_keyed_[pend_["comment_post_ID"]] = absint(pend_["num_comments"])
        # end for
    # end if
    return pending_keyed_
# end def get_pending_comments_num
#// 
#// Add avatars to relevant places in admin, or try to.
#// 
#// @since 2.5.0
#// 
#// @param string $name User name.
#// @return string Avatar with Admin name.
#//
def floated_admin_avatar(name_=None, *_args_):
    
    
    avatar_ = get_avatar(get_comment(), 32, "mystery")
    return str(avatar_) + str(" ") + str(name_)
# end def floated_admin_avatar
#// 
#// @since 2.7.0
#//
def enqueue_comment_hotkeys_js(*_args_):
    
    
    if "true" == get_user_option("comment_shortcuts"):
        wp_enqueue_script("jquery-table-hotkeys")
    # end if
# end def enqueue_comment_hotkeys_js
#// 
#// Display error message at bottom of comments.
#// 
#// @param string $msg Error Message. Assumed to contain HTML and be sanitized.
#//
def comment_footer_die(msg_=None, *_args_):
    
    
    php_print(str("<div class='wrap'><p>") + str(msg_) + str("</p></div>"))
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    php_exit(0)
# end def comment_footer_die
