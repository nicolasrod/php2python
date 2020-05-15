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
#// Handles Comment Post to WordPress and prevents duplicate comment posting.
#// 
#// @package WordPress
#//
if "POST" != PHP_SERVER["REQUEST_METHOD"]:
    protocol = PHP_SERVER["SERVER_PROTOCOL"]
    if (not php_in_array(protocol, Array("HTTP/1.1", "HTTP/2", "HTTP/2.0"), True)):
        protocol = "HTTP/1.0"
    # end if
    php_header("Allow: POST")
    php_header(str(protocol) + str(" 405 Method Not Allowed"))
    php_header("Content-Type: text/plain")
    php_exit(0)
# end if
#// Sets up the WordPress Environment.
php_include_file(__DIR__ + "/wp-load.php", once=False)
nocache_headers()
comment = wp_handle_comment_submission(wp_unslash(PHP_POST))
if is_wp_error(comment):
    data = php_intval(comment.get_error_data())
    if (not php_empty(lambda : data)):
        wp_die("<p>" + comment.get_error_message() + "</p>", __("Comment Submission Failure"), Array({"response": data, "back_link": True}))
    else:
        php_exit(0)
    # end if
# end if
user = wp_get_current_user()
cookies_consent = (php_isset(lambda : PHP_POST["wp-comment-cookies-consent"]))
#// 
#// Perform other actions when comment cookies are set.
#// 
#// @since 3.4.0
#// @since 4.9.6 The `$cookies_consent` parameter was added.
#// 
#// @param WP_Comment $comment         Comment object.
#// @param WP_User    $user            Comment author's user object. The user may not exist.
#// @param boolean    $cookies_consent Comment author's consent to store cookies.
#//
do_action("set_comment_cookies", comment, user, cookies_consent)
location = get_comment_link(comment) if php_empty(lambda : PHP_POST["redirect_to"]) else PHP_POST["redirect_to"] + "#comment-" + comment.comment_ID
#// Add specific query arguments to display the awaiting moderation message.
if "unapproved" == wp_get_comment_status(comment) and (not php_empty(lambda : comment.comment_author_email)):
    location = add_query_arg(Array({"unapproved": comment.comment_ID, "moderation-hash": wp_hash(comment.comment_date_gmt)}), location)
# end if
#// 
#// Filters the location URI to send the commenter after posting.
#// 
#// @since 2.0.5
#// 
#// @param string     $location The 'redirect_to' URI sent via $_POST.
#// @param WP_Comment $comment  Comment object.
#//
location = apply_filters("comment_post_redirect", location, comment)
wp_safe_redirect(location)
php_exit(0)
