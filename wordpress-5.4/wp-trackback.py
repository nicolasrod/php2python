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
#// Handle Trackbacks and Pingbacks Sent to WordPress
#// 
#// @since 0.71
#// 
#// @package WordPress
#// @subpackage Trackbacks
#//
if php_empty(lambda : wp_):
    php_include_file(__DIR__ + "/wp-load.php", once=True)
    wp(Array({"tb": "1"}))
# end if
#// 
#// Response to a trackback.
#// 
#// Responds with an error or success XML message.
#// 
#// @since 0.71
#// 
#// @param int|bool $error         Whether there was an error.
#// Default '0'. Accepts '0' or '1', true or false.
#// @param string   $error_message Error message if an error occurred.
#//
def trackback_response(error_=0, error_message_="", *_args_):
    
    
    php_header("Content-Type: text/xml; charset=" + get_option("blog_charset"))
    if error_:
        php_print("<?xml version=\"1.0\" encoding=\"utf-8\"?" + ">\n")
        php_print("<response>\n")
        php_print("<error>1</error>\n")
        php_print(str("<message>") + str(error_message_) + str("</message>\n"))
        php_print("</response>")
        php_exit(0)
    else:
        php_print("<?xml version=\"1.0\" encoding=\"utf-8\"?" + ">\n")
        php_print("<response>\n")
        php_print("<error>0</error>\n")
        php_print("</response>")
    # end if
# end def trackback_response
#// Trackback is done by a POST.
request_array_ = "HTTP_POST_VARS"
if (not (php_isset(lambda : PHP_REQUEST["tb_id"]))) or (not PHP_REQUEST["tb_id"]):
    tb_id_ = php_explode("/", PHP_SERVER["REQUEST_URI"])
    tb_id_ = php_intval(tb_id_[php_count(tb_id_) - 1])
# end if
tb_url_ = PHP_POST["url"] if (php_isset(lambda : PHP_POST["url"])) else ""
charset_ = PHP_POST["charset"] if (php_isset(lambda : PHP_POST["charset"])) else ""
#// These three are stripslashed here so they can be properly escaped after mb_convert_encoding().
title_ = wp_unslash(PHP_POST["title"]) if (php_isset(lambda : PHP_POST["title"])) else ""
excerpt_ = wp_unslash(PHP_POST["excerpt"]) if (php_isset(lambda : PHP_POST["excerpt"])) else ""
blog_name_ = wp_unslash(PHP_POST["blog_name"]) if (php_isset(lambda : PHP_POST["blog_name"])) else ""
if charset_:
    charset_ = php_str_replace(Array(",", " "), "", php_strtoupper(php_trim(charset_)))
else:
    charset_ = "ASCII, UTF-8, ISO-8859-1, JIS, EUC-JP, SJIS"
# end if
#// No valid uses for UTF-7.
if False != php_strpos(charset_, "UTF-7"):
    php_exit(0)
# end if
#// For international trackbacks.
if php_function_exists("mb_convert_encoding"):
    title_ = mb_convert_encoding(title_, get_option("blog_charset"), charset_)
    excerpt_ = mb_convert_encoding(excerpt_, get_option("blog_charset"), charset_)
    blog_name_ = mb_convert_encoding(blog_name_, get_option("blog_charset"), charset_)
# end if
#// Now that mb_convert_encoding() has been given a swing, we need to escape these three.
title_ = wp_slash(title_)
excerpt_ = wp_slash(excerpt_)
blog_name_ = wp_slash(blog_name_)
if is_single() or is_page():
    tb_id_ = posts_[0].ID
# end if
if (not (php_isset(lambda : tb_id_))) or (not php_intval(tb_id_)):
    trackback_response(1, __("I really need an ID for this to work."))
# end if
if php_empty(lambda : title_) and php_empty(lambda : tb_url_) and php_empty(lambda : blog_name_):
    #// If it doesn't look like a trackback at all.
    wp_redirect(get_permalink(tb_id_))
    php_exit(0)
# end if
if (not php_empty(lambda : tb_url_)) and (not php_empty(lambda : title_)):
    #// 
    #// Fires before the trackback is added to a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int    $tb_id     Post ID related to the trackback.
    #// @param string $tb_url    Trackback URL.
    #// @param string $charset   Character Set.
    #// @param string $title     Trackback Title.
    #// @param string $excerpt   Trackback Excerpt.
    #// @param string $blog_name Blog Name.
    #//
    do_action("pre_trackback_post", tb_id_, tb_url_, charset_, title_, excerpt_, blog_name_)
    php_header("Content-Type: text/xml; charset=" + get_option("blog_charset"))
    if (not pings_open(tb_id_)):
        trackback_response(1, __("Sorry, trackbacks are closed for this item."))
    # end if
    title_ = wp_html_excerpt(title_, 250, "&#8230;")
    excerpt_ = wp_html_excerpt(excerpt_, 252, "&#8230;")
    comment_post_ID_ = php_int(tb_id_)
    comment_author_ = blog_name_
    comment_author_email_ = ""
    comment_author_url_ = tb_url_
    comment_content_ = str("<strong>") + str(title_) + str("</strong>\n\n") + str(excerpt_)
    comment_type_ = "trackback"
    dupe_ = wpdb_.get_results(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d AND comment_author_url = %s"), comment_post_ID_, comment_author_url_))
    if dupe_:
        trackback_response(1, __("We already have a ping from that URL for this post."))
    # end if
    commentdata_ = php_compact("comment_post_ID", "comment_author", "comment_author_email", "comment_author_url", "comment_content", "comment_type")
    result_ = wp_new_comment(commentdata_)
    if is_wp_error(result_):
        trackback_response(1, result_.get_error_message())
    # end if
    trackback_id_ = wpdb_.insert_id
    #// 
    #// Fires after a trackback is added to a post.
    #// 
    #// @since 1.2.0
    #// 
    #// @param int $trackback_id Trackback ID.
    #//
    do_action("trackback_post", trackback_id_)
    trackback_response(0)
# end if
