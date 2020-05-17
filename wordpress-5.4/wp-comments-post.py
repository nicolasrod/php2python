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
#// Handles Comment Post to WordPress and prevents duplicate comment posting.
#// 
#// @package WordPress
#//
if "POST" != PHP_SERVER["REQUEST_METHOD"]:
    protocol_ = PHP_SERVER["SERVER_PROTOCOL"]
    if (not php_in_array(protocol_, Array("HTTP/1.1", "HTTP/2", "HTTP/2.0"), True)):
        protocol_ = "HTTP/1.0"
    # end if
    php_header("Allow: POST")
    php_header(str(protocol_) + str(" 405 Method Not Allowed"))
    php_header("Content-Type: text/plain")
    php_exit(0)
# end if
#// Sets up the WordPress Environment.
php_include_file(__DIR__ + "/wp-load.php", once=False)
nocache_headers()
comment_ = wp_handle_comment_submission(wp_unslash(PHP_POST))
if is_wp_error(comment_):
    data_ = php_intval(comment_.get_error_data())
    if (not php_empty(lambda : data_)):
        wp_die("<p>" + comment_.get_error_message() + "</p>", __("Comment Submission Failure"), Array({"response": data_, "back_link": True}))
    else:
        php_exit(0)
    # end if
# end if
user_ = wp_get_current_user()
cookies_consent_ = (php_isset(lambda : PHP_POST["wp-comment-cookies-consent"]))
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
do_action("set_comment_cookies", comment_, user_, cookies_consent_)
location_ = get_comment_link(comment_) if php_empty(lambda : PHP_POST["redirect_to"]) else PHP_POST["redirect_to"] + "#comment-" + comment_.comment_ID
#// Add specific query arguments to display the awaiting moderation message.
if "unapproved" == wp_get_comment_status(comment_) and (not php_empty(lambda : comment_.comment_author_email)):
    location_ = add_query_arg(Array({"unapproved": comment_.comment_ID, "moderation-hash": wp_hash(comment_.comment_date_gmt)}), location_)
# end if
#// 
#// Filters the location URI to send the commenter after posting.
#// 
#// @since 2.0.5
#// 
#// @param string     $location The 'redirect_to' URI sent via $_POST.
#// @param WP_Comment $comment  Comment object.
#//
location_ = apply_filters("comment_post_redirect", location_, comment_)
wp_safe_redirect(location_)
php_exit(0)
