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
#// Core Comment API
#// 
#// @package WordPress
#// @subpackage Comment
#// 
#// 
#// Check whether a comment passes internal checks to be allowed to add.
#// 
#// If manual comment moderation is set in the administration, then all checks,
#// regardless of their type and whitelist, will fail and the function will
#// return false.
#// 
#// If the number of links exceeds the amount in the administration, then the
#// check fails. If any of the parameter contents match the blacklist of words,
#// then the check fails.
#// 
#// If the comment author was approved before, then the comment is automatically
#// whitelisted.
#// 
#// If all checks pass, the function will return true.
#// 
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $author       Comment author name.
#// @param string $email        Comment author email.
#// @param string $url          Comment author URL.
#// @param string $comment      Content of the comment.
#// @param string $user_ip      Comment author IP address.
#// @param string $user_agent   Comment author User-Agent.
#// @param string $comment_type Comment type, either user-submitted comment,
#// trackback, or pingback.
#// @return bool If all checks pass, true, otherwise false.
#//
def check_comment(author_=None, email_=None, url_=None, comment_=None, user_ip_=None, user_agent_=None, comment_type_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// If manual moderation is enabled, skip all checks and return false.
    if 1 == get_option("comment_moderation"):
        return False
    # end if
    #// This filter is documented in wp-includes/comment-template.php
    comment_ = apply_filters("comment_text", comment_, None, Array())
    #// Check for the number of external links if a max allowed number is set.
    max_links_ = get_option("comment_max_links")
    if max_links_:
        num_links_ = preg_match_all("/<a [^>]*href/i", comment_, out_)
        #// 
        #// Filters the number of links found in a comment.
        #// 
        #// @since 3.0.0
        #// @since 4.7.0 Added the `$comment` parameter.
        #// 
        #// @param int    $num_links The number of links found.
        #// @param string $url       Comment author's URL. Included in allowed links total.
        #// @param string $comment   Content of the comment.
        #//
        num_links_ = apply_filters("comment_max_links_url", num_links_, url_, comment_)
        #// 
        #// If the number of links in the comment exceeds the allowed amount,
        #// fail the check by returning false.
        #//
        if num_links_ >= max_links_:
            return False
        # end if
    # end if
    mod_keys_ = php_trim(get_option("moderation_keys"))
    #// If moderation 'keys' (keywords) are set, process them.
    if (not php_empty(lambda : mod_keys_)):
        words_ = php_explode("\n", mod_keys_)
        for word_ in words_:
            word_ = php_trim(word_)
            #// Skip empty lines.
            if php_empty(lambda : word_):
                continue
            # end if
            #// 
            #// Do some escaping magic so that '#' (number of) characters in the spam
            #// words don't break things:
            #//
            word_ = preg_quote(word_, "#")
            #// 
            #// Check the comment fields for moderation keywords. If any are found,
            #// fail the check for the given field by returning false.
            #//
            pattern_ = str("#") + str(word_) + str("#i")
            if php_preg_match(pattern_, author_):
                return False
            # end if
            if php_preg_match(pattern_, email_):
                return False
            # end if
            if php_preg_match(pattern_, url_):
                return False
            # end if
            if php_preg_match(pattern_, comment_):
                return False
            # end if
            if php_preg_match(pattern_, user_ip_):
                return False
            # end if
            if php_preg_match(pattern_, user_agent_):
                return False
            # end if
        # end for
    # end if
    #// 
    #// Check if the option to approve comments by previously-approved authors is enabled.
    #// 
    #// If it is enabled, check whether the comment author has a previously-approved comment,
    #// as well as whether there are any moderation keywords (if set) present in the author
    #// email address. If both checks pass, return true. Otherwise, return false.
    #//
    if 1 == get_option("comment_whitelist"):
        if "trackback" != comment_type_ and "pingback" != comment_type_ and "" != author_ and "" != email_:
            comment_user_ = get_user_by("email", wp_unslash(email_))
            if (not php_empty(lambda : comment_user_.ID)):
                ok_to_comment_ = wpdb_.get_var(wpdb_.prepare(str("SELECT comment_approved FROM ") + str(wpdb_.comments) + str(" WHERE user_id = %d AND comment_approved = '1' LIMIT 1"), comment_user_.ID))
            else:
                #// expected_slashed ($author, $email)
                ok_to_comment_ = wpdb_.get_var(wpdb_.prepare(str("SELECT comment_approved FROM ") + str(wpdb_.comments) + str(" WHERE comment_author = %s AND comment_author_email = %s and comment_approved = '1' LIMIT 1"), author_, email_))
            # end if
            if 1 == ok_to_comment_ and php_empty(lambda : mod_keys_) or False == php_strpos(email_, mod_keys_):
                return True
            else:
                return False
            # end if
        else:
            return False
        # end if
    # end if
    return True
# end def check_comment
#// 
#// Retrieve the approved comments for post $post_id.
#// 
#// @since 2.0.0
#// @since 4.1.0 Refactored to leverage WP_Comment_Query over a direct query.
#// 
#// @param  int   $post_id The ID of the post.
#// @param  array $args    Optional. See WP_Comment_Query::__construct() for information on accepted arguments.
#// @return int|array $comments The approved comments, or number of comments if `$count`
#// argument is true.
#//
def get_approved_comments(post_id_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    if (not post_id_):
        return Array()
    # end if
    defaults_ = Array({"status": 1, "post_id": post_id_, "order": "ASC"})
    parsed_args_ = wp_parse_args(args_, defaults_)
    query_ = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
    return query_.query(parsed_args_)
# end def get_approved_comments
#// 
#// Retrieves comment data given a comment ID or comment object.
#// 
#// If an object is passed then the comment data will be cached and then returned
#// after being passed through a filter. If the comment is empty, then the global
#// comment variable will be used, if it is set.
#// 
#// @since 2.0.0
#// 
#// @global WP_Comment $comment Global comment object.
#// 
#// @param WP_Comment|string|int $comment Comment to retrieve.
#// @param string                $output  Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Comment object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @return WP_Comment|array|null Depends on $output value.
#//
def get_comment(comment_=None, output_=None, *_args_):
    if comment_ is None:
        comment_ = None
    # end if
    if output_ is None:
        output_ = OBJECT
    # end if
    
    if php_empty(lambda : comment_) and (php_isset(lambda : PHP_GLOBALS["comment"])):
        comment_ = PHP_GLOBALS["comment"]
    # end if
    if type(comment_).__name__ == "WP_Comment":
        _comment_ = comment_
    elif php_is_object(comment_):
        _comment_ = php_new_class("WP_Comment", lambda : WP_Comment(comment_))
    else:
        _comment_ = WP_Comment.get_instance(comment_)
    # end if
    if (not _comment_):
        return None
    # end if
    #// 
    #// Fires after a comment is retrieved.
    #// 
    #// @since 2.3.0
    #// 
    #// @param WP_Comment $_comment Comment data.
    #//
    _comment_ = apply_filters("get_comment", _comment_)
    if OBJECT == output_:
        return _comment_
    elif ARRAY_A == output_:
        return _comment_.to_array()
    elif ARRAY_N == output_:
        return php_array_values(_comment_.to_array())
    # end if
    return _comment_
# end def get_comment
#// 
#// Retrieve a list of comments.
#// 
#// The comment list can be for the blog as a whole or for an individual post.
#// 
#// @since 2.7.0
#// 
#// @param string|array $args Optional. Array or string of arguments. See WP_Comment_Query::__construct()
#// for information on accepted arguments. Default empty.
#// @return int|array List of comments or number of found comments if `$count` argument is true.
#//
def get_comments(args_="", *_args_):
    
    
    query_ = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
    return query_.query(args_)
# end def get_comments
#// 
#// Retrieve all of the WordPress supported comment statuses.
#// 
#// Comments have a limited set of valid status values, this provides the comment
#// status values and descriptions.
#// 
#// @since 2.7.0
#// 
#// @return string[] List of comment status labels keyed by status.
#//
def get_comment_statuses(*_args_):
    
    
    status_ = Array({"hold": __("Unapproved"), "approve": _x("Approved", "comment status"), "spam": _x("Spam", "comment status"), "trash": _x("Trash", "comment status")})
    return status_
# end def get_comment_statuses
#// 
#// Gets the default comment status for a post type.
#// 
#// @since 4.3.0
#// 
#// @param string $post_type    Optional. Post type. Default 'post'.
#// @param string $comment_type Optional. Comment type. Default 'comment'.
#// @return string Expected return value is 'open' or 'closed'.
#//
def get_default_comment_status(post_type_="post", comment_type_="comment", *_args_):
    
    
    for case in Switch(comment_type_):
        if case("pingback"):
            pass
        # end if
        if case("trackback"):
            supports_ = "trackbacks"
            option_ = "ping"
            break
        # end if
        if case():
            supports_ = "comments"
            option_ = "comment"
            break
        # end if
    # end for
    #// Set the status.
    if "page" == post_type_:
        status_ = "closed"
    elif post_type_supports(post_type_, supports_):
        status_ = get_option(str("default_") + str(option_) + str("_status"))
    else:
        status_ = "closed"
    # end if
    #// 
    #// Filters the default comment status for the given post type.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string $status       Default status for the given post type,
    #// either 'open' or 'closed'.
    #// @param string $post_type    Post type. Default is `post`.
    #// @param string $comment_type Type of comment. Default is `comment`.
    #//
    return apply_filters("get_default_comment_status", status_, post_type_, comment_type_)
# end def get_default_comment_status
#// 
#// The date the last comment was modified.
#// 
#// @since 1.5.0
#// @since 4.7.0 Replaced caching the modified date in a local static variable
#// with the Object Cache API.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $timezone Which timezone to use in reference to 'gmt', 'blog', or 'server' locations.
#// @return string|false Last comment modified date on success, false on failure.
#//
def get_lastcommentmodified(timezone_="server", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    timezone_ = php_strtolower(timezone_)
    key_ = str("lastcommentmodified:") + str(timezone_)
    comment_modified_date_ = wp_cache_get(key_, "timeinfo")
    if False != comment_modified_date_:
        return comment_modified_date_
    # end if
    for case in Switch(timezone_):
        if case("gmt"):
            comment_modified_date_ = wpdb_.get_var(str("SELECT comment_date_gmt FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = '1' ORDER BY comment_date_gmt DESC LIMIT 1"))
            break
        # end if
        if case("blog"):
            comment_modified_date_ = wpdb_.get_var(str("SELECT comment_date FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = '1' ORDER BY comment_date_gmt DESC LIMIT 1"))
            break
        # end if
        if case("server"):
            add_seconds_server_ = gmdate("Z")
            comment_modified_date_ = wpdb_.get_var(wpdb_.prepare(str("SELECT DATE_ADD(comment_date_gmt, INTERVAL %s SECOND) FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = '1' ORDER BY comment_date_gmt DESC LIMIT 1"), add_seconds_server_))
            break
        # end if
    # end for
    if comment_modified_date_:
        wp_cache_set(key_, comment_modified_date_, "timeinfo")
        return comment_modified_date_
    # end if
    return False
# end def get_lastcommentmodified
#// 
#// Retrieves the total comment counts for the whole site or a single post.
#// 
#// Unlike wp_count_comments(), this function always returns the live comment counts without caching.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $post_id Optional. Restrict the comment counts to the given post. Default 0, which indicates that
#// comment counts for the whole site will be retrieved.
#// @return array() {
#// The number of comments keyed by their status.
#// 
#// @type int|string $approved            The number of approved comments.
#// @type int|string $awaiting_moderation The number of comments awaiting moderation (a.k.a. pending).
#// @type int|string $spam                The number of spam comments.
#// @type int|string $trash               The number of trashed comments.
#// @type int|string $post-trashed        The number of comments for posts that are in the trash.
#// @type int        $total_comments      The total number of non-trashed comments, including spam.
#// @type int        $all                 The total number of pending or approved comments.
#// }
#//
def get_comment_count(post_id_=0, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_id_ = php_int(post_id_)
    where_ = ""
    if post_id_ > 0:
        where_ = wpdb_.prepare("WHERE comment_post_ID = %d", post_id_)
    # end if
    totals_ = wpdb_.get_results(str("\n     SELECT comment_approved, COUNT( * ) AS total\n      FROM ") + str(wpdb_.comments) + str("\n     ") + str(where_) + str("\n      GROUP BY comment_approved\n "), ARRAY_A)
    comment_count_ = Array({"approved": 0, "awaiting_moderation": 0, "spam": 0, "trash": 0, "post-trashed": 0, "total_comments": 0, "all": 0})
    for row_ in totals_:
        for case in Switch(row_["comment_approved"]):
            if case("trash"):
                comment_count_["trash"] = row_["total"]
                break
            # end if
            if case("post-trashed"):
                comment_count_["post-trashed"] = row_["total"]
                break
            # end if
            if case("spam"):
                comment_count_["spam"] = row_["total"]
                comment_count_["total_comments"] += row_["total"]
                break
            # end if
            if case("1"):
                comment_count_["approved"] = row_["total"]
                comment_count_["total_comments"] += row_["total"]
                comment_count_["all"] += row_["total"]
                break
            # end if
            if case("0"):
                comment_count_["awaiting_moderation"] = row_["total"]
                comment_count_["total_comments"] += row_["total"]
                comment_count_["all"] += row_["total"]
                break
            # end if
            if case():
                break
            # end if
        # end for
    # end for
    return comment_count_
# end def get_comment_count
#// 
#// Comment meta functions.
#// 
#// 
#// Add meta data field to a comment.
#// 
#// @since 2.9.0
#// @link https://developer.wordpress.org/reference/functions/add_comment_meta
#// 
#// @param int $comment_id Comment ID.
#// @param string $meta_key Metadata name.
#// @param mixed $meta_value Metadata value.
#// @param bool $unique Optional, default is false. Whether the same key should not be added.
#// @return int|bool Meta ID on success, false on failure.
#//
def add_comment_meta(comment_id_=None, meta_key_=None, meta_value_=None, unique_=None, *_args_):
    if unique_ is None:
        unique_ = False
    # end if
    
    return add_metadata("comment", comment_id_, meta_key_, meta_value_, unique_)
# end def add_comment_meta
#// 
#// Remove metadata matching criteria from a comment.
#// 
#// You can match based on the key, or key and value. Removing based on key and
#// value, will keep from removing duplicate metadata with the same key. It also
#// allows removing all metadata matching key, if needed.
#// 
#// @since 2.9.0
#// @link https://developer.wordpress.org/reference/functions/delete_comment_meta
#// 
#// @param int $comment_id comment ID
#// @param string $meta_key Metadata name.
#// @param mixed $meta_value Optional. Metadata value.
#// @return bool True on success, false on failure.
#//
def delete_comment_meta(comment_id_=None, meta_key_=None, meta_value_="", *_args_):
    
    
    return delete_metadata("comment", comment_id_, meta_key_, meta_value_)
# end def delete_comment_meta
#// 
#// Retrieve comment meta field for a comment.
#// 
#// @since 2.9.0
#// @link https://developer.wordpress.org/reference/functions/get_comment_meta
#// 
#// @param int $comment_id Comment ID.
#// @param string $key Optional. The meta key to retrieve. By default, returns data for all keys.
#// @param bool $single Whether to return a single value.
#// @return mixed Will be an array if $single is false. Will be value of meta data field if $single
#// is true.
#//
def get_comment_meta(comment_id_=None, key_="", single_=None, *_args_):
    if single_ is None:
        single_ = False
    # end if
    
    return get_metadata("comment", comment_id_, key_, single_)
# end def get_comment_meta
#// 
#// Update comment meta field based on comment ID.
#// 
#// Use the $prev_value parameter to differentiate between meta fields with the
#// same key and comment ID.
#// 
#// If the meta field for the comment does not exist, it will be added.
#// 
#// @since 2.9.0
#// @link https://developer.wordpress.org/reference/functions/update_comment_meta
#// 
#// @param int $comment_id Comment ID.
#// @param string $meta_key Metadata key.
#// @param mixed $meta_value Metadata value.
#// @param mixed $prev_value Optional. Previous value to check before removing.
#// @return int|bool Meta ID if the key didn't exist, true on successful update, false on failure.
#//
def update_comment_meta(comment_id_=None, meta_key_=None, meta_value_=None, prev_value_="", *_args_):
    
    
    return update_metadata("comment", comment_id_, meta_key_, meta_value_, prev_value_)
# end def update_comment_meta
#// 
#// Queues comments for metadata lazy-loading.
#// 
#// @since 4.5.0
#// 
#// @param WP_Comment[] $comments Array of comment objects.
#//
def wp_queue_comments_for_comment_meta_lazyload(comments_=None, *_args_):
    
    
    #// Don't use `wp_list_pluck()` to avoid by-reference manipulation.
    comment_ids_ = Array()
    if php_is_array(comments_):
        for comment_ in comments_:
            if type(comment_).__name__ == "WP_Comment":
                comment_ids_[-1] = comment_.comment_ID
            # end if
        # end for
    # end if
    if comment_ids_:
        lazyloader_ = wp_metadata_lazyloader()
        lazyloader_.queue_objects("comment", comment_ids_)
    # end if
# end def wp_queue_comments_for_comment_meta_lazyload
#// 
#// Sets the cookies used to store an unauthenticated commentator's identity. Typically used
#// to recall previous comments by this commentator that are still held in moderation.
#// 
#// @since 3.4.0
#// @since 4.9.6 The `$cookies_consent` parameter was added.
#// 
#// @param WP_Comment $comment         Comment object.
#// @param WP_User    $user            Comment author's user object. The user may not exist.
#// @param boolean    $cookies_consent Optional. Comment author's consent to store cookies. Default true.
#//
def wp_set_comment_cookies(comment_=None, user_=None, cookies_consent_=None, *_args_):
    if cookies_consent_ is None:
        cookies_consent_ = True
    # end if
    
    #// If the user already exists, or the user opted out of cookies, don't set cookies.
    if user_.exists():
        return
    # end if
    if False == cookies_consent_:
        #// Remove any existing cookies.
        past_ = time() - YEAR_IN_SECONDS
        setcookie("comment_author_" + COOKIEHASH, " ", past_, COOKIEPATH, COOKIE_DOMAIN)
        setcookie("comment_author_email_" + COOKIEHASH, " ", past_, COOKIEPATH, COOKIE_DOMAIN)
        setcookie("comment_author_url_" + COOKIEHASH, " ", past_, COOKIEPATH, COOKIE_DOMAIN)
        return
    # end if
    #// 
    #// Filters the lifetime of the comment cookie in seconds.
    #// 
    #// @since 2.8.0
    #// 
    #// @param int $seconds Comment cookie lifetime. Default 30000000.
    #//
    comment_cookie_lifetime_ = time() + apply_filters("comment_cookie_lifetime", 30000000)
    secure_ = "https" == php_parse_url(home_url(), PHP_URL_SCHEME)
    setcookie("comment_author_" + COOKIEHASH, comment_.comment_author, comment_cookie_lifetime_, COOKIEPATH, COOKIE_DOMAIN, secure_)
    setcookie("comment_author_email_" + COOKIEHASH, comment_.comment_author_email, comment_cookie_lifetime_, COOKIEPATH, COOKIE_DOMAIN, secure_)
    setcookie("comment_author_url_" + COOKIEHASH, esc_url(comment_.comment_author_url), comment_cookie_lifetime_, COOKIEPATH, COOKIE_DOMAIN, secure_)
# end def wp_set_comment_cookies
#// 
#// Sanitizes the cookies sent to the user already.
#// 
#// Will only do anything if the cookies have already been created for the user.
#// Mostly used after cookies had been sent to use elsewhere.
#// 
#// @since 2.0.4
#//
def sanitize_comment_cookies(*_args_):
    
    global PHP_COOKIE
    if (php_isset(lambda : PHP_COOKIE["comment_author_" + COOKIEHASH])):
        #// 
        #// Filters the comment author's name cookie before it is set.
        #// 
        #// When this filter hook is evaluated in wp_filter_comment(),
        #// the comment author's name string is passed.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string $author_cookie The comment author name cookie.
        #//
        comment_author_ = apply_filters("pre_comment_author_name", PHP_COOKIE["comment_author_" + COOKIEHASH])
        comment_author_ = wp_unslash(comment_author_)
        comment_author_ = esc_attr(comment_author_)
        PHP_COOKIE["comment_author_" + COOKIEHASH] = comment_author_
    # end if
    if (php_isset(lambda : PHP_COOKIE["comment_author_email_" + COOKIEHASH])):
        #// 
        #// Filters the comment author's email cookie before it is set.
        #// 
        #// When this filter hook is evaluated in wp_filter_comment(),
        #// the comment author's email string is passed.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string $author_email_cookie The comment author email cookie.
        #//
        comment_author_email_ = apply_filters("pre_comment_author_email", PHP_COOKIE["comment_author_email_" + COOKIEHASH])
        comment_author_email_ = wp_unslash(comment_author_email_)
        comment_author_email_ = esc_attr(comment_author_email_)
        PHP_COOKIE["comment_author_email_" + COOKIEHASH] = comment_author_email_
    # end if
    if (php_isset(lambda : PHP_COOKIE["comment_author_url_" + COOKIEHASH])):
        #// 
        #// Filters the comment author's URL cookie before it is set.
        #// 
        #// When this filter hook is evaluated in wp_filter_comment(),
        #// the comment author's URL string is passed.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string $author_url_cookie The comment author URL cookie.
        #//
        comment_author_url_ = apply_filters("pre_comment_author_url", PHP_COOKIE["comment_author_url_" + COOKIEHASH])
        comment_author_url_ = wp_unslash(comment_author_url_)
        PHP_COOKIE["comment_author_url_" + COOKIEHASH] = comment_author_url_
    # end if
# end def sanitize_comment_cookies
#// 
#// Validates whether this comment is allowed to be made.
#// 
#// @since 2.0.0
#// @since 4.7.0 The `$avoid_die` parameter was added, allowing the function to
#// return a WP_Error object instead of dying.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $commentdata Contains information on the comment.
#// @param bool  $avoid_die   When true, a disallowed comment will result in the function
#// returning a WP_Error object, rather than executing wp_die().
#// Default false.
#// @return int|string|WP_Error Allowed comments return the approval status (0|1|'spam'|'trash').
#// If `$avoid_die` is true, disallowed comments return a WP_Error.
#//
def wp_allow_comment(commentdata_=None, avoid_die_=None, *_args_):
    if avoid_die_ is None:
        avoid_die_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Simple duplicate check.
    #// expected_slashed ($comment_post_ID, $comment_author, $comment_author_email, $comment_content)
    dupe_ = wpdb_.prepare(str("SELECT comment_ID FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d AND comment_parent = %s AND comment_approved != 'trash' AND ( comment_author = %s "), wp_unslash(commentdata_["comment_post_ID"]), wp_unslash(commentdata_["comment_parent"]), wp_unslash(commentdata_["comment_author"]))
    if commentdata_["comment_author_email"]:
        dupe_ += wpdb_.prepare("AND comment_author_email = %s ", wp_unslash(commentdata_["comment_author_email"]))
    # end if
    dupe_ += wpdb_.prepare(") AND comment_content = %s LIMIT 1", wp_unslash(commentdata_["comment_content"]))
    dupe_id_ = wpdb_.get_var(dupe_)
    #// 
    #// Filters the ID, if any, of the duplicate comment found when creating a new comment.
    #// 
    #// Return an empty value from this filter to allow what WP considers a duplicate comment.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int   $dupe_id     ID of the comment identified as a duplicate.
    #// @param array $commentdata Data for the comment being created.
    #//
    dupe_id_ = apply_filters("duplicate_comment_id", dupe_id_, commentdata_)
    if dupe_id_:
        #// 
        #// Fires immediately after a duplicate comment is detected.
        #// 
        #// @since 3.0.0
        #// 
        #// @param array $commentdata Comment data.
        #//
        do_action("comment_duplicate_trigger", commentdata_)
        #// 
        #// Filters duplicate comment error message.
        #// 
        #// @since 5.2.0
        #// 
        #// @param string $comment_duplicate_message Duplicate comment error message.
        #//
        comment_duplicate_message_ = apply_filters("comment_duplicate_message", __("Duplicate comment detected; it looks as though you&#8217;ve already said that!"))
        if True == avoid_die_:
            return php_new_class("WP_Error", lambda : WP_Error("comment_duplicate", comment_duplicate_message_, 409))
        else:
            if wp_doing_ajax():
                php_print(comment_duplicate_message_)
                php_exit()
            # end if
            wp_die(comment_duplicate_message_, 409)
        # end if
    # end if
    #// 
    #// Fires immediately before a comment is marked approved.
    #// 
    #// Allows checking for comment flooding.
    #// 
    #// @since 2.3.0
    #// @since 4.7.0 The `$avoid_die` parameter was added.
    #// 
    #// @param string $comment_author_IP    Comment author's IP address.
    #// @param string $comment_author_email Comment author's email.
    #// @param string $comment_date_gmt     GMT date the comment was posted.
    #// @param bool   $avoid_die            Whether to prevent executing wp_die()
    #// or die() if a comment flood is occurring.
    #//
    do_action("check_comment_flood", commentdata_["comment_author_IP"], commentdata_["comment_author_email"], commentdata_["comment_date_gmt"], avoid_die_)
    #// 
    #// Filters whether a comment is part of a comment flood.
    #// 
    #// The default check is wp_check_comment_flood(). See check_comment_flood_db().
    #// 
    #// @since 4.7.0
    #// 
    #// @param bool   $is_flood             Is a comment flooding occurring? Default false.
    #// @param string $comment_author_IP    Comment author's IP address.
    #// @param string $comment_author_email Comment author's email.
    #// @param string $comment_date_gmt     GMT date the comment was posted.
    #// @param bool   $avoid_die            Whether to prevent executing wp_die()
    #// or die() if a comment flood is occurring.
    #//
    is_flood_ = apply_filters("wp_is_comment_flood", False, commentdata_["comment_author_IP"], commentdata_["comment_author_email"], commentdata_["comment_date_gmt"], avoid_die_)
    if is_flood_:
        #// This filter is documented in wp-includes/comment-template.php
        comment_flood_message_ = apply_filters("comment_flood_message", __("You are posting comments too quickly. Slow down."))
        return php_new_class("WP_Error", lambda : WP_Error("comment_flood", comment_flood_message_, 429))
    # end if
    if (not php_empty(lambda : commentdata_["user_id"])):
        user_ = get_userdata(commentdata_["user_id"])
        post_author_ = wpdb_.get_var(wpdb_.prepare(str("SELECT post_author FROM ") + str(wpdb_.posts) + str(" WHERE ID = %d LIMIT 1"), commentdata_["comment_post_ID"]))
    # end if
    if (php_isset(lambda : user_)) and commentdata_["user_id"] == post_author_ or user_.has_cap("moderate_comments"):
        #// The author and the admins get respect.
        approved_ = 1
    else:
        #// Everyone else's comments will be checked.
        if check_comment(commentdata_["comment_author"], commentdata_["comment_author_email"], commentdata_["comment_author_url"], commentdata_["comment_content"], commentdata_["comment_author_IP"], commentdata_["comment_agent"], commentdata_["comment_type"]):
            approved_ = 1
        else:
            approved_ = 0
        # end if
        if wp_blacklist_check(commentdata_["comment_author"], commentdata_["comment_author_email"], commentdata_["comment_author_url"], commentdata_["comment_content"], commentdata_["comment_author_IP"], commentdata_["comment_agent"]):
            approved_ = "trash" if EMPTY_TRASH_DAYS else "spam"
        # end if
    # end if
    #// 
    #// Filters a comment's approval status before it is set.
    #// 
    #// @since 2.1.0
    #// @since 4.9.0 Returning a WP_Error value from the filter will shortcircuit comment insertion
    #// and allow skipping further processing.
    #// 
    #// @param int|string|WP_Error $approved    The approval status. Accepts 1, 0, 'spam', 'trash',
    #// or WP_Error.
    #// @param array               $commentdata Comment data.
    #//
    return apply_filters("pre_comment_approved", approved_, commentdata_)
# end def wp_allow_comment
#// 
#// Hooks WP's native database-based comment-flood check.
#// 
#// This wrapper maintains backward compatibility with plugins that expect to
#// be able to unhook the legacy check_comment_flood_db() function from
#// 'check_comment_flood' using remove_action().
#// 
#// @since 2.3.0
#// @since 4.7.0 Converted to be an add_filter() wrapper.
#//
def check_comment_flood_db(*_args_):
    
    
    add_filter("wp_is_comment_flood", "wp_check_comment_flood", 10, 5)
# end def check_comment_flood_db
#// 
#// Checks whether comment flooding is occurring.
#// 
#// Won't run, if current user can manage options, so to not block
#// administrators.
#// 
#// @since 4.7.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param bool   $is_flood  Is a comment flooding occurring?
#// @param string $ip        Comment author's IP address.
#// @param string $email     Comment author's email address.
#// @param string $date      MySQL time string.
#// @param bool   $avoid_die When true, a disallowed comment will result in the function
#// returning a WP_Error object, rather than executing wp_die().
#// Default false.
#// @return bool Whether comment flooding is occurring.
#//
def wp_check_comment_flood(is_flood_=None, ip_=None, email_=None, date_=None, avoid_die_=None, *_args_):
    if avoid_die_ is None:
        avoid_die_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Another callback has declared a flood. Trust it.
    if True == is_flood_:
        return is_flood_
    # end if
    #// Don't throttle admins or moderators.
    if current_user_can("manage_options") or current_user_can("moderate_comments"):
        return False
    # end if
    hour_ago_ = gmdate("Y-m-d H:i:s", time() - HOUR_IN_SECONDS)
    if is_user_logged_in():
        user_ = get_current_user_id()
        check_column_ = "`user_id`"
    else:
        user_ = ip_
        check_column_ = "`comment_author_IP`"
    # end if
    sql_ = wpdb_.prepare(str("SELECT `comment_date_gmt` FROM `") + str(wpdb_.comments) + str("` WHERE `comment_date_gmt` >= %s AND ( ") + str(check_column_) + str(" = %s OR `comment_author_email` = %s ) ORDER BY `comment_date_gmt` DESC LIMIT 1"), hour_ago_, user_, email_)
    lasttime_ = wpdb_.get_var(sql_)
    if lasttime_:
        time_lastcomment_ = mysql2date("U", lasttime_, False)
        time_newcomment_ = mysql2date("U", date_, False)
        #// 
        #// Filters the comment flood status.
        #// 
        #// @since 2.1.0
        #// 
        #// @param bool $bool             Whether a comment flood is occurring. Default false.
        #// @param int  $time_lastcomment Timestamp of when the last comment was posted.
        #// @param int  $time_newcomment  Timestamp of when the new comment was posted.
        #//
        flood_die_ = apply_filters("comment_flood_filter", False, time_lastcomment_, time_newcomment_)
        if flood_die_:
            #// 
            #// Fires before the comment flood message is triggered.
            #// 
            #// @since 1.5.0
            #// 
            #// @param int $time_lastcomment Timestamp of when the last comment was posted.
            #// @param int $time_newcomment  Timestamp of when the new comment was posted.
            #//
            do_action("comment_flood_trigger", time_lastcomment_, time_newcomment_)
            if True == avoid_die_:
                return True
            else:
                #// 
                #// Filters the comment flood error message.
                #// 
                #// @since 5.2.0
                #// 
                #// @param string $comment_flood_message Comment flood error message.
                #//
                comment_flood_message_ = apply_filters("comment_flood_message", __("You are posting comments too quickly. Slow down."))
                if wp_doing_ajax():
                    php_print(comment_flood_message_)
                    php_exit()
                # end if
                wp_die(comment_flood_message_, 429)
            # end if
        # end if
    # end if
    return False
# end def wp_check_comment_flood
#// 
#// Separates an array of comments into an array keyed by comment_type.
#// 
#// @since 2.7.0
#// 
#// @param WP_Comment[] $comments Array of comments
#// @return WP_Comment[] Array of comments keyed by comment_type.
#//
def separate_comments(comments_=None, *_args_):
    
    
    comments_by_type_ = Array({"comment": Array(), "trackback": Array(), "pingback": Array(), "pings": Array()})
    count_ = php_count(comments_)
    i_ = 0
    while i_ < count_:
        
        type_ = comments_[i_].comment_type
        if php_empty(lambda : type_):
            type_ = "comment"
        # end if
        comments_by_type_[type_][-1] = comments_[i_]
        if "trackback" == type_ or "pingback" == type_:
            comments_by_type_["pings"][-1] = comments_[i_]
        # end if
        i_ += 1
    # end while
    return comments_by_type_
# end def separate_comments
#// 
#// Calculate the total number of comment pages.
#// 
#// @since 2.7.0
#// 
#// @uses Walker_Comment
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param WP_Comment[] $comments Optional. Array of WP_Comment objects. Defaults to $wp_query->comments.
#// @param int          $per_page Optional. Comments per page.
#// @param bool         $threaded Optional. Control over flat or threaded comments.
#// @return int Number of comment pages.
#//
def get_comment_pages_count(comments_=None, per_page_=None, threaded_=None, *_args_):
    if comments_ is None:
        comments_ = None
    # end if
    if per_page_ is None:
        per_page_ = None
    # end if
    if threaded_ is None:
        threaded_ = None
    # end if
    
    global wp_query_
    php_check_if_defined("wp_query_")
    if None == comments_ and None == per_page_ and None == threaded_ and (not php_empty(lambda : wp_query_.max_num_comment_pages)):
        return wp_query_.max_num_comment_pages
    # end if
    if (not comments_) or (not php_is_array(comments_)) and (not php_empty(lambda : wp_query_.comments)):
        comments_ = wp_query_.comments
    # end if
    if php_empty(lambda : comments_):
        return 0
    # end if
    if (not get_option("page_comments")):
        return 1
    # end if
    if (not (php_isset(lambda : per_page_))):
        per_page_ = php_int(get_query_var("comments_per_page"))
    # end if
    if 0 == per_page_:
        per_page_ = php_int(get_option("comments_per_page"))
    # end if
    if 0 == per_page_:
        return 1
    # end if
    if (not (php_isset(lambda : threaded_))):
        threaded_ = get_option("thread_comments")
    # end if
    if threaded_:
        walker_ = php_new_class("Walker_Comment", lambda : Walker_Comment())
        count_ = ceil(walker_.get_number_of_root_elements(comments_) / per_page_)
    else:
        count_ = ceil(php_count(comments_) / per_page_)
    # end if
    return count_
# end def get_comment_pages_count
#// 
#// Calculate what page number a comment will appear on for comment paging.
#// 
#// @since 2.7.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int   $comment_ID Comment ID.
#// @param array $args {
#// Array of optional arguments.
#// @type string     $type      Limit paginated comments to those matching a given type. Accepts 'comment',
#// 'trackback', 'pingback', 'pings' (trackbacks and pingbacks), or 'all'.
#// Default is 'all'.
#// @type int        $per_page  Per-page count to use when calculating pagination. Defaults to the value of the
#// 'comments_per_page' option.
#// @type int|string $max_depth If greater than 1, comment page will be determined for the top-level parent of
#// `$comment_ID`. Defaults to the value of the 'thread_comments_depth' option.
#// }
#// @return int|null Comment page number or null on error.
#//
def get_page_of_comment(comment_ID_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    page_ = None
    comment_ = get_comment(comment_ID_)
    if (not comment_):
        return
    # end if
    defaults_ = Array({"type": "all", "page": "", "per_page": "", "max_depth": ""})
    args_ = wp_parse_args(args_, defaults_)
    original_args_ = args_
    #// Order of precedence: 1. `$args['per_page']`, 2. 'comments_per_page' query_var, 3. 'comments_per_page' option.
    if get_option("page_comments"):
        if "" == args_["per_page"]:
            args_["per_page"] = get_query_var("comments_per_page")
        # end if
        if "" == args_["per_page"]:
            args_["per_page"] = get_option("comments_per_page")
        # end if
    # end if
    if php_empty(lambda : args_["per_page"]):
        args_["per_page"] = 0
        args_["page"] = 0
    # end if
    if args_["per_page"] < 1:
        page_ = 1
    # end if
    if None == page_:
        if "" == args_["max_depth"]:
            if get_option("thread_comments"):
                args_["max_depth"] = get_option("thread_comments_depth")
            else:
                args_["max_depth"] = -1
            # end if
        # end if
        #// Find this comment's top-level parent if threading is enabled.
        if args_["max_depth"] > 1 and 0 != comment_.comment_parent:
            return get_page_of_comment(comment_.comment_parent, args_)
        # end if
        comment_args_ = Array({"type": args_["type"], "post_id": comment_.comment_post_ID, "fields": "ids", "count": True, "status": "approve", "parent": 0, "date_query": Array(Array({"column": str(wpdb_.comments) + str(".comment_date_gmt"), "before": comment_.comment_date_gmt}))})
        comment_query_ = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
        older_comment_count_ = comment_query_.query(comment_args_)
        #// No older comments? Then it's page #1.
        if 0 == older_comment_count_:
            page_ = 1
            pass
        else:
            page_ = ceil(older_comment_count_ + 1 / args_["per_page"])
        # end if
    # end if
    #// 
    #// Filters the calculated page on which a comment appears.
    #// 
    #// @since 4.4.0
    #// @since 4.7.0 Introduced the `$comment_ID` parameter.
    #// 
    #// @param int   $page          Comment page.
    #// @param array $args {
    #// Arguments used to calculate pagination. These include arguments auto-detected by the function,
    #// based on query vars, system settings, etc. For pristine arguments passed to the function,
    #// see `$original_args`.
    #// 
    #// @type string $type      Type of comments to count.
    #// @type int    $page      Calculated current page.
    #// @type int    $per_page  Calculated number of comments per page.
    #// @type int    $max_depth Maximum comment threading depth allowed.
    #// }
    #// @param array $original_args {
    #// Array of arguments passed to the function. Some or all of these may not be set.
    #// 
    #// @type string $type      Type of comments to count.
    #// @type int    $page      Current comment page.
    #// @type int    $per_page  Number of comments per page.
    #// @type int    $max_depth Maximum comment threading depth allowed.
    #// }
    #// @param int $comment_ID ID of the comment.
    #//
    return apply_filters("get_page_of_comment", php_int(page_), args_, original_args_, comment_ID_)
# end def get_page_of_comment
#// 
#// Retrieves the maximum character lengths for the comment form fields.
#// 
#// @since 4.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return int[] Array of maximum lengths keyed by field name.
#//
def wp_get_comment_fields_max_lengths(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    lengths_ = Array({"comment_author": 245, "comment_author_email": 100, "comment_author_url": 200, "comment_content": 65525})
    if wpdb_.is_mysql:
        for column_,length_ in lengths_.items():
            col_length_ = wpdb_.get_col_length(wpdb_.comments, column_)
            max_length_ = 0
            #// No point if we can't get the DB column lengths.
            if is_wp_error(col_length_):
                break
            # end if
            if (not php_is_array(col_length_)) and php_int(col_length_) > 0:
                max_length_ = php_int(col_length_)
            elif php_is_array(col_length_) and (php_isset(lambda : col_length_["length"])) and php_intval(col_length_["length"]) > 0:
                max_length_ = php_int(col_length_["length"])
                if (not php_empty(lambda : col_length_["type"])) and "byte" == col_length_["type"]:
                    max_length_ = max_length_ - 10
                # end if
            # end if
            if max_length_ > 0:
                lengths_[column_] = max_length_
            # end if
        # end for
    # end if
    #// 
    #// Filters the lengths for the comment form fields.
    #// 
    #// @since 4.5.0
    #// 
    #// @param int[] $lengths Array of maximum lengths keyed by field name.
    #//
    return apply_filters("wp_get_comment_fields_max_lengths", lengths_)
# end def wp_get_comment_fields_max_lengths
#// 
#// Compares the lengths of comment data against the maximum character limits.
#// 
#// @since 4.7.0
#// 
#// @param array $comment_data Array of arguments for inserting a comment.
#// @return WP_Error|true WP_Error when a comment field exceeds the limit,
#// otherwise true.
#//
def wp_check_comment_data_max_lengths(comment_data_=None, *_args_):
    
    
    max_lengths_ = wp_get_comment_fields_max_lengths()
    if (php_isset(lambda : comment_data_["comment_author"])) and php_mb_strlen(comment_data_["comment_author"], "8bit") > max_lengths_["comment_author"]:
        return php_new_class("WP_Error", lambda : WP_Error("comment_author_column_length", __("<strong>Error</strong>: Your name is too long."), 200))
    # end if
    if (php_isset(lambda : comment_data_["comment_author_email"])) and php_strlen(comment_data_["comment_author_email"]) > max_lengths_["comment_author_email"]:
        return php_new_class("WP_Error", lambda : WP_Error("comment_author_email_column_length", __("<strong>Error</strong>: Your email address is too long."), 200))
    # end if
    if (php_isset(lambda : comment_data_["comment_author_url"])) and php_strlen(comment_data_["comment_author_url"]) > max_lengths_["comment_author_url"]:
        return php_new_class("WP_Error", lambda : WP_Error("comment_author_url_column_length", __("<strong>Error</strong>: Your URL is too long."), 200))
    # end if
    if (php_isset(lambda : comment_data_["comment_content"])) and php_mb_strlen(comment_data_["comment_content"], "8bit") > max_lengths_["comment_content"]:
        return php_new_class("WP_Error", lambda : WP_Error("comment_content_column_length", __("<strong>Error</strong>: Your comment is too long."), 200))
    # end if
    return True
# end def wp_check_comment_data_max_lengths
#// 
#// Does comment contain blacklisted characters or words.
#// 
#// @since 1.5.0
#// 
#// @param string $author The author of the comment
#// @param string $email The email of the comment
#// @param string $url The url used in the comment
#// @param string $comment The comment content
#// @param string $user_ip The comment author's IP address
#// @param string $user_agent The author's browser user agent
#// @return bool True if comment contains blacklisted content, false if comment does not
#//
def wp_blacklist_check(author_=None, email_=None, url_=None, comment_=None, user_ip_=None, user_agent_=None, *_args_):
    
    
    #// 
    #// Fires before the comment is tested for blacklisted characters or words.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $author     Comment author.
    #// @param string $email      Comment author's email.
    #// @param string $url        Comment author's URL.
    #// @param string $comment    Comment content.
    #// @param string $user_ip    Comment author's IP address.
    #// @param string $user_agent Comment author's browser user agent.
    #//
    do_action("wp_blacklist_check", author_, email_, url_, comment_, user_ip_, user_agent_)
    mod_keys_ = php_trim(get_option("blacklist_keys"))
    if "" == mod_keys_:
        return False
        pass
    # end if
    #// Ensure HTML tags are not being used to bypass the blacklist.
    comment_without_html_ = wp_strip_all_tags(comment_)
    words_ = php_explode("\n", mod_keys_)
    for word_ in words_:
        word_ = php_trim(word_)
        #// Skip empty lines.
        if php_empty(lambda : word_):
            continue
        # end if
        #// Do some escaping magic so that '#' chars
        #// in the spam words don't break things:
        word_ = preg_quote(word_, "#")
        pattern_ = str("#") + str(word_) + str("#i")
        if php_preg_match(pattern_, author_) or php_preg_match(pattern_, email_) or php_preg_match(pattern_, url_) or php_preg_match(pattern_, comment_) or php_preg_match(pattern_, comment_without_html_) or php_preg_match(pattern_, user_ip_) or php_preg_match(pattern_, user_agent_):
            return True
        # end if
    # end for
    return False
# end def wp_blacklist_check
#// 
#// Retrieves the total comment counts for the whole site or a single post.
#// 
#// The comment stats are cached and then retrieved, if they already exist in the
#// cache.
#// 
#// @see get_comment_count() Which handles fetching the live comment counts.
#// 
#// @since 2.5.0
#// 
#// @param int $post_id Optional. Restrict the comment counts to the given post. Default 0, which indicates that
#// comment counts for the whole site will be retrieved.
#// @return stdClass {
#// The number of comments keyed by their status.
#// 
#// @type int|string $approved       The number of approved comments.
#// @type int|string $moderated      The number of comments awaiting moderation (a.k.a. pending).
#// @type int|string $spam           The number of spam comments.
#// @type int|string $trash          The number of trashed comments.
#// @type int|string $post-trashed   The number of comments for posts that are in the trash.
#// @type int        $total_comments The total number of non-trashed comments, including spam.
#// @type int        $all            The total number of pending or approved comments.
#// }
#//
def wp_count_comments(post_id_=0, *_args_):
    
    
    post_id_ = php_int(post_id_)
    #// 
    #// Filters the comments count for a given post or the whole site.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array|stdClass $count   An empty array or an object containing comment counts.
    #// @param int            $post_id The post ID. Can be 0 to represent the whole site.
    #//
    filtered_ = apply_filters("wp_count_comments", Array(), post_id_)
    if (not php_empty(lambda : filtered_)):
        return filtered_
    # end if
    count_ = wp_cache_get(str("comments-") + str(post_id_), "counts")
    if False != count_:
        return count_
    # end if
    stats_ = get_comment_count(post_id_)
    stats_["moderated"] = stats_["awaiting_moderation"]
    stats_["awaiting_moderation"] = None
    stats_object_ = stats_
    wp_cache_set(str("comments-") + str(post_id_), stats_object_, "counts")
    return stats_object_
# end def wp_count_comments
#// 
#// Trashes or deletes a comment.
#// 
#// The comment is moved to Trash instead of permanently deleted unless Trash is
#// disabled, item is already in the Trash, or $force_delete is true.
#// 
#// The post comment count will be updated if the comment was approved and has a
#// post ID available.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Comment $comment_id   Comment ID or WP_Comment object.
#// @param bool           $force_delete Whether to bypass Trash and force deletion. Default is false.
#// @return bool True on success, false on failure.
#//
def wp_delete_comment(comment_id_=None, force_delete_=None, *_args_):
    if force_delete_ is None:
        force_delete_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    comment_ = get_comment(comment_id_)
    if (not comment_):
        return False
    # end if
    if (not force_delete_) and EMPTY_TRASH_DAYS and (not php_in_array(wp_get_comment_status(comment_), Array("trash", "spam"))):
        return wp_trash_comment(comment_id_)
    # end if
    #// 
    #// Fires immediately before a comment is deleted from the database.
    #// 
    #// @since 1.2.0
    #// @since 4.9.0 Added the `$comment` parameter.
    #// 
    #// @param int        $comment_id The comment ID.
    #// @param WP_Comment $comment    The comment to be deleted.
    #//
    do_action("delete_comment", comment_.comment_ID, comment_)
    #// Move children up a level.
    children_ = wpdb_.get_col(wpdb_.prepare(str("SELECT comment_ID FROM ") + str(wpdb_.comments) + str(" WHERE comment_parent = %d"), comment_.comment_ID))
    if (not php_empty(lambda : children_)):
        wpdb_.update(wpdb_.comments, Array({"comment_parent": comment_.comment_parent}), Array({"comment_parent": comment_.comment_ID}))
        clean_comment_cache(children_)
    # end if
    #// Delete metadata.
    meta_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.commentmeta) + str(" WHERE comment_id = %d"), comment_.comment_ID))
    for mid_ in meta_ids_:
        delete_metadata_by_mid("comment", mid_)
    # end for
    if (not wpdb_.delete(wpdb_.comments, Array({"comment_ID": comment_.comment_ID}))):
        return False
    # end if
    #// 
    #// Fires immediately after a comment is deleted from the database.
    #// 
    #// @since 2.9.0
    #// @since 4.9.0 Added the `$comment` parameter.
    #// 
    #// @param int        $comment_id The comment ID.
    #// @param WP_Comment $comment    The deleted comment.
    #//
    do_action("deleted_comment", comment_.comment_ID, comment_)
    post_id_ = comment_.comment_post_ID
    if post_id_ and 1 == comment_.comment_approved:
        wp_update_comment_count(post_id_)
    # end if
    clean_comment_cache(comment_.comment_ID)
    #// This action is documented in wp-includes/comment.php
    do_action("wp_set_comment_status", comment_.comment_ID, "delete")
    wp_transition_comment_status("delete", comment_.comment_approved, comment_)
    return True
# end def wp_delete_comment
#// 
#// Moves a comment to the Trash
#// 
#// If Trash is disabled, comment is permanently deleted.
#// 
#// @since 2.9.0
#// 
#// @param int|WP_Comment $comment_id Comment ID or WP_Comment object.
#// @return bool True on success, false on failure.
#//
def wp_trash_comment(comment_id_=None, *_args_):
    
    
    if (not EMPTY_TRASH_DAYS):
        return wp_delete_comment(comment_id_, True)
    # end if
    comment_ = get_comment(comment_id_)
    if (not comment_):
        return False
    # end if
    #// 
    #// Fires immediately before a comment is sent to the Trash.
    #// 
    #// @since 2.9.0
    #// @since 4.9.0 Added the `$comment` parameter.
    #// 
    #// @param int        $comment_id The comment ID.
    #// @param WP_Comment $comment    The comment to be trashed.
    #//
    do_action("trash_comment", comment_.comment_ID, comment_)
    if wp_set_comment_status(comment_, "trash"):
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_status")
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_time")
        add_comment_meta(comment_.comment_ID, "_wp_trash_meta_status", comment_.comment_approved)
        add_comment_meta(comment_.comment_ID, "_wp_trash_meta_time", time())
        #// 
        #// Fires immediately after a comment is sent to Trash.
        #// 
        #// @since 2.9.0
        #// @since 4.9.0 Added the `$comment` parameter.
        #// 
        #// @param int        $comment_id The comment ID.
        #// @param WP_Comment $comment    The trashed comment.
        #//
        do_action("trashed_comment", comment_.comment_ID, comment_)
        return True
    # end if
    return False
# end def wp_trash_comment
#// 
#// Removes a comment from the Trash
#// 
#// @since 2.9.0
#// 
#// @param int|WP_Comment $comment_id Comment ID or WP_Comment object.
#// @return bool True on success, false on failure.
#//
def wp_untrash_comment(comment_id_=None, *_args_):
    
    
    comment_ = get_comment(comment_id_)
    if (not comment_):
        return False
    # end if
    #// 
    #// Fires immediately before a comment is restored from the Trash.
    #// 
    #// @since 2.9.0
    #// @since 4.9.0 Added the `$comment` parameter.
    #// 
    #// @param int        $comment_id The comment ID.
    #// @param WP_Comment $comment    The comment to be untrashed.
    #//
    do_action("untrash_comment", comment_.comment_ID, comment_)
    status_ = php_str(get_comment_meta(comment_.comment_ID, "_wp_trash_meta_status", True))
    if php_empty(lambda : status_):
        status_ = "0"
    # end if
    if wp_set_comment_status(comment_, status_):
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_time")
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_status")
        #// 
        #// Fires immediately after a comment is restored from the Trash.
        #// 
        #// @since 2.9.0
        #// @since 4.9.0 Added the `$comment` parameter.
        #// 
        #// @param int        $comment_id The comment ID.
        #// @param WP_Comment $comment    The untrashed comment.
        #//
        do_action("untrashed_comment", comment_.comment_ID, comment_)
        return True
    # end if
    return False
# end def wp_untrash_comment
#// 
#// Marks a comment as Spam
#// 
#// @since 2.9.0
#// 
#// @param int|WP_Comment $comment_id Comment ID or WP_Comment object.
#// @return bool True on success, false on failure.
#//
def wp_spam_comment(comment_id_=None, *_args_):
    
    
    comment_ = get_comment(comment_id_)
    if (not comment_):
        return False
    # end if
    #// 
    #// Fires immediately before a comment is marked as Spam.
    #// 
    #// @since 2.9.0
    #// @since 4.9.0 Added the `$comment` parameter.
    #// 
    #// @param int        $comment_id The comment ID.
    #// @param WP_Comment $comment    The comment to be marked as spam.
    #//
    do_action("spam_comment", comment_.comment_ID, comment_)
    if wp_set_comment_status(comment_, "spam"):
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_status")
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_time")
        add_comment_meta(comment_.comment_ID, "_wp_trash_meta_status", comment_.comment_approved)
        add_comment_meta(comment_.comment_ID, "_wp_trash_meta_time", time())
        #// 
        #// Fires immediately after a comment is marked as Spam.
        #// 
        #// @since 2.9.0
        #// @since 4.9.0 Added the `$comment` parameter.
        #// 
        #// @param int        $comment_id The comment ID.
        #// @param WP_Comment $comment    The comment marked as spam.
        #//
        do_action("spammed_comment", comment_.comment_ID, comment_)
        return True
    # end if
    return False
# end def wp_spam_comment
#// 
#// Removes a comment from the Spam
#// 
#// @since 2.9.0
#// 
#// @param int|WP_Comment $comment_id Comment ID or WP_Comment object.
#// @return bool True on success, false on failure.
#//
def wp_unspam_comment(comment_id_=None, *_args_):
    
    
    comment_ = get_comment(comment_id_)
    if (not comment_):
        return False
    # end if
    #// 
    #// Fires immediately before a comment is unmarked as Spam.
    #// 
    #// @since 2.9.0
    #// @since 4.9.0 Added the `$comment` parameter.
    #// 
    #// @param int        $comment_id The comment ID.
    #// @param WP_Comment $comment    The comment to be unmarked as spam.
    #//
    do_action("unspam_comment", comment_.comment_ID, comment_)
    status_ = php_str(get_comment_meta(comment_.comment_ID, "_wp_trash_meta_status", True))
    if php_empty(lambda : status_):
        status_ = "0"
    # end if
    if wp_set_comment_status(comment_, status_):
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_status")
        delete_comment_meta(comment_.comment_ID, "_wp_trash_meta_time")
        #// 
        #// Fires immediately after a comment is unmarked as Spam.
        #// 
        #// @since 2.9.0
        #// @since 4.9.0 Added the `$comment` parameter.
        #// 
        #// @param int        $comment_id The comment ID.
        #// @param WP_Comment $comment    The comment unmarked as spam.
        #//
        do_action("unspammed_comment", comment_.comment_ID, comment_)
        return True
    # end if
    return False
# end def wp_unspam_comment
#// 
#// The status of a comment by ID.
#// 
#// @since 1.0.0
#// 
#// @param int|WP_Comment $comment_id Comment ID or WP_Comment object
#// @return string|false Status might be 'trash', 'approved', 'unapproved', 'spam'. False on failure.
#//
def wp_get_comment_status(comment_id_=None, *_args_):
    
    
    comment_ = get_comment(comment_id_)
    if (not comment_):
        return False
    # end if
    approved_ = comment_.comment_approved
    if None == approved_:
        return False
    elif "1" == approved_:
        return "approved"
    elif "0" == approved_:
        return "unapproved"
    elif "spam" == approved_:
        return "spam"
    elif "trash" == approved_:
        return "trash"
    else:
        return False
    # end if
# end def wp_get_comment_status
#// 
#// Call hooks for when a comment status transition occurs.
#// 
#// Calls hooks for comment status transitions. If the new comment status is not the same
#// as the previous comment status, then two hooks will be ran, the first is
#// {@see 'transition_comment_status'} with new status, old status, and comment data.
#// The next action called is {@see 'comment_$old_status_to_$new_status'}. It has
#// the comment data.
#// 
#// The final action will run whether or not the comment statuses are the same.
#// The action is named {@see 'comment_$new_status_$comment->comment_type'}.
#// 
#// @since 2.7.0
#// 
#// @param string     $new_status New comment status.
#// @param string     $old_status Previous comment status.
#// @param WP_Comment $comment    Comment object.
#//
def wp_transition_comment_status(new_status_=None, old_status_=None, comment_=None, *_args_):
    
    
    #// 
    #// Translate raw statuses to human-readable formats for the hooks.
    #// This is not a complete list of comment status, it's only the ones
    #// that need to be renamed.
    #//
    comment_statuses_ = Array({0: "unapproved", "hold": "unapproved", 1: "approved", "approve": "approved"})
    if (php_isset(lambda : comment_statuses_[new_status_])):
        new_status_ = comment_statuses_[new_status_]
    # end if
    if (php_isset(lambda : comment_statuses_[old_status_])):
        old_status_ = comment_statuses_[old_status_]
    # end if
    #// Call the hooks.
    if new_status_ != old_status_:
        #// 
        #// Fires when the comment status is in transition.
        #// 
        #// @since 2.7.0
        #// 
        #// @param int|string $new_status The new comment status.
        #// @param int|string $old_status The old comment status.
        #// @param WP_Comment $comment    Comment object.
        #//
        do_action("transition_comment_status", new_status_, old_status_, comment_)
        #// 
        #// Fires when the comment status is in transition from one specific status to another.
        #// 
        #// The dynamic portions of the hook name, `$old_status`, and `$new_status`,
        #// refer to the old and new comment statuses, respectively.
        #// 
        #// @since 2.7.0
        #// 
        #// @param WP_Comment $comment Comment object.
        #//
        do_action(str("comment_") + str(old_status_) + str("_to_") + str(new_status_), comment_)
    # end if
    #// 
    #// Fires when the status of a specific comment type is in transition.
    #// 
    #// The dynamic portions of the hook name, `$new_status`, and `$comment->comment_type`,
    #// refer to the new comment status, and the type of comment, respectively.
    #// 
    #// Typical comment types include an empty string (standard comment), 'pingback',
    #// or 'trackback'.
    #// 
    #// @since 2.7.0
    #// 
    #// @param int        $comment_ID The comment ID.
    #// @param WP_Comment $comment    Comment object.
    #//
    do_action(str("comment_") + str(new_status_) + str("_") + str(comment_.comment_type), comment_.comment_ID, comment_)
# end def wp_transition_comment_status
#// 
#// Clear the lastcommentmodified cached value when a comment status is changed.
#// 
#// Deletes the lastcommentmodified cache key when a comment enters or leaves
#// 'approved' status.
#// 
#// @since 4.7.0
#// @access private
#// 
#// @param string $new_status The new comment status.
#// @param string $old_status The old comment status.
#//
def _clear_modified_cache_on_transition_comment_status(new_status_=None, old_status_=None, *_args_):
    
    
    if "approved" == new_status_ or "approved" == old_status_:
        for timezone_ in Array("server", "gmt", "blog"):
            wp_cache_delete(str("lastcommentmodified:") + str(timezone_), "timeinfo")
        # end for
    # end if
# end def _clear_modified_cache_on_transition_comment_status
#// 
#// Get current commenter's name, email, and URL.
#// 
#// Expects cookies content to already be sanitized. User of this function might
#// wish to recheck the returned array for validity.
#// 
#// @see sanitize_comment_cookies() Use to sanitize cookies
#// 
#// @since 2.0.4
#// 
#// @return array {
#// An array of current commenter variables.
#// 
#// @type string $comment_author       The name of the current commenter, or an empty string.
#// @type string $comment_author_email The email address of the current commenter, or an empty string.
#// @type string $comment_author_url   The URL address of the current commenter, or an empty string.
#// }
#//
def wp_get_current_commenter(*_args_):
    
    
    #// Cookies should already be sanitized.
    comment_author_ = ""
    if (php_isset(lambda : PHP_COOKIE["comment_author_" + COOKIEHASH])):
        comment_author_ = PHP_COOKIE["comment_author_" + COOKIEHASH]
    # end if
    comment_author_email_ = ""
    if (php_isset(lambda : PHP_COOKIE["comment_author_email_" + COOKIEHASH])):
        comment_author_email_ = PHP_COOKIE["comment_author_email_" + COOKIEHASH]
    # end if
    comment_author_url_ = ""
    if (php_isset(lambda : PHP_COOKIE["comment_author_url_" + COOKIEHASH])):
        comment_author_url_ = PHP_COOKIE["comment_author_url_" + COOKIEHASH]
    # end if
    #// 
    #// Filters the current commenter's name, email, and URL.
    #// 
    #// @since 3.1.0
    #// 
    #// @param array $comment_author_data {
    #// An array of current commenter variables.
    #// 
    #// @type string $comment_author       The name of the current commenter, or an empty string.
    #// @type string $comment_author_email The email address of the current commenter, or an empty string.
    #// @type string $comment_author_url   The URL address of the current commenter, or an empty string.
    #// }
    #//
    return apply_filters("wp_get_current_commenter", php_compact("comment_author_", "comment_author_email_", "comment_author_url_"))
# end def wp_get_current_commenter
#// 
#// Get unapproved comment author's email.
#// 
#// Used to allow the commenter to see their pending comment.
#// 
#// @since 5.1.0
#// 
#// @return string The unapproved comment author's email (when supplied).
#//
def wp_get_unapproved_comment_author_email(*_args_):
    
    
    commenter_email_ = ""
    if (not php_empty(lambda : PHP_REQUEST["unapproved"])) and (not php_empty(lambda : PHP_REQUEST["moderation-hash"])):
        comment_id_ = php_int(PHP_REQUEST["unapproved"])
        comment_ = get_comment(comment_id_)
        if comment_ and hash_equals(PHP_REQUEST["moderation-hash"], wp_hash(comment_.comment_date_gmt)):
            commenter_email_ = comment_.comment_author_email
        # end if
    # end if
    if (not commenter_email_):
        commenter_ = wp_get_current_commenter()
        commenter_email_ = commenter_["comment_author_email"]
    # end if
    return commenter_email_
# end def wp_get_unapproved_comment_author_email
#// 
#// Inserts a comment into the database.
#// 
#// @since 2.0.0
#// @since 4.4.0 Introduced `$comment_meta` argument.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $commentdata {
#// Array of arguments for inserting a new comment.
#// 
#// @type string     $comment_agent        The HTTP user agent of the `$comment_author` when
#// the comment was submitted. Default empty.
#// @type int|string $comment_approved     Whether the comment has been approved. Default 1.
#// @type string     $comment_author       The name of the author of the comment. Default empty.
#// @type string     $comment_author_email The email address of the `$comment_author`. Default empty.
#// @type string     $comment_author_IP    The IP address of the `$comment_author`. Default empty.
#// @type string     $comment_author_url   The URL address of the `$comment_author`. Default empty.
#// @type string     $comment_content      The content of the comment. Default empty.
#// @type string     $comment_date         The date the comment was submitted. To set the date
#// manually, `$comment_date_gmt` must also be specified.
#// Default is the current time.
#// @type string     $comment_date_gmt     The date the comment was submitted in the GMT timezone.
#// Default is `$comment_date` in the site's GMT timezone.
#// @type int        $comment_karma        The karma of the comment. Default 0.
#// @type int        $comment_parent       ID of this comment's parent, if any. Default 0.
#// @type int        $comment_post_ID      ID of the post that relates to the comment, if any.
#// Default 0.
#// @type string     $comment_type         Comment type. Default empty.
#// @type array      $comment_meta         Optional. Array of key/value pairs to be stored in commentmeta for the
#// new comment.
#// @type int        $user_id              ID of the user who submitted the comment. Default 0.
#// }
#// @return int|false The new comment's ID on success, false on failure.
#//
def wp_insert_comment(commentdata_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    data_ = wp_unslash(commentdata_)
    comment_author_ = "" if (not (php_isset(lambda : data_["comment_author"]))) else data_["comment_author"]
    comment_author_email_ = "" if (not (php_isset(lambda : data_["comment_author_email"]))) else data_["comment_author_email"]
    comment_author_url_ = "" if (not (php_isset(lambda : data_["comment_author_url"]))) else data_["comment_author_url"]
    comment_author_IP_ = "" if (not (php_isset(lambda : data_["comment_author_IP"]))) else data_["comment_author_IP"]
    comment_date_ = current_time("mysql") if (not (php_isset(lambda : data_["comment_date"]))) else data_["comment_date"]
    comment_date_gmt_ = get_gmt_from_date(comment_date_) if (not (php_isset(lambda : data_["comment_date_gmt"]))) else data_["comment_date_gmt"]
    comment_post_ID_ = 0 if (not (php_isset(lambda : data_["comment_post_ID"]))) else data_["comment_post_ID"]
    comment_content_ = "" if (not (php_isset(lambda : data_["comment_content"]))) else data_["comment_content"]
    comment_karma_ = 0 if (not (php_isset(lambda : data_["comment_karma"]))) else data_["comment_karma"]
    comment_approved_ = 1 if (not (php_isset(lambda : data_["comment_approved"]))) else data_["comment_approved"]
    comment_agent_ = "" if (not (php_isset(lambda : data_["comment_agent"]))) else data_["comment_agent"]
    comment_type_ = "" if (not (php_isset(lambda : data_["comment_type"]))) else data_["comment_type"]
    comment_parent_ = 0 if (not (php_isset(lambda : data_["comment_parent"]))) else data_["comment_parent"]
    user_id_ = 0 if (not (php_isset(lambda : data_["user_id"]))) else data_["user_id"]
    compacted_ = php_compact("comment_post_ID_", "comment_author_", "comment_author_email_", "comment_author_url_", "comment_author_IP_", "comment_date_", "comment_date_gmt_", "comment_content_", "comment_karma_", "comment_approved_", "comment_agent_", "comment_type_", "comment_parent_", "user_id_")
    if (not wpdb_.insert(wpdb_.comments, compacted_)):
        return False
    # end if
    id_ = php_int(wpdb_.insert_id)
    if 1 == comment_approved_:
        wp_update_comment_count(comment_post_ID_)
        for timezone_ in Array("server", "gmt", "blog"):
            wp_cache_delete(str("lastcommentmodified:") + str(timezone_), "timeinfo")
        # end for
    # end if
    clean_comment_cache(id_)
    comment_ = get_comment(id_)
    #// If metadata is provided, store it.
    if (php_isset(lambda : commentdata_["comment_meta"])) and php_is_array(commentdata_["comment_meta"]):
        for meta_key_,meta_value_ in commentdata_["comment_meta"].items():
            add_comment_meta(comment_.comment_ID, meta_key_, meta_value_, True)
        # end for
    # end if
    #// 
    #// Fires immediately after a comment is inserted into the database.
    #// 
    #// @since 2.8.0
    #// 
    #// @param int        $id      The comment ID.
    #// @param WP_Comment $comment Comment object.
    #//
    do_action("wp_insert_comment", id_, comment_)
    return id_
# end def wp_insert_comment
#// 
#// Filters and sanitizes comment data.
#// 
#// Sets the comment data 'filtered' field to true when finished. This can be
#// checked as to whether the comment should be filtered and to keep from
#// filtering the same comment more than once.
#// 
#// @since 2.0.0
#// 
#// @param array $commentdata Contains information on the comment.
#// @return array Parsed comment information.
#//
def wp_filter_comment(commentdata_=None, *_args_):
    
    
    if (php_isset(lambda : commentdata_["user_ID"])):
        #// 
        #// Filters the comment author's user id before it is set.
        #// 
        #// The first time this filter is evaluated, 'user_ID' is checked
        #// (for back-compat), followed by the standard 'user_id' value.
        #// 
        #// @since 1.5.0
        #// 
        #// @param int $user_ID The comment author's user ID.
        #//
        commentdata_["user_id"] = apply_filters("pre_user_id", commentdata_["user_ID"])
    elif (php_isset(lambda : commentdata_["user_id"])):
        #// This filter is documented in wp-includes/comment.php
        commentdata_["user_id"] = apply_filters("pre_user_id", commentdata_["user_id"])
    # end if
    #// 
    #// Filters the comment author's browser user agent before it is set.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $comment_agent The comment author's browser user agent.
    #//
    commentdata_["comment_agent"] = apply_filters("pre_comment_user_agent", commentdata_["comment_agent"] if (php_isset(lambda : commentdata_["comment_agent"])) else "")
    #// This filter is documented in wp-includes/comment.php
    commentdata_["comment_author"] = apply_filters("pre_comment_author_name", commentdata_["comment_author"])
    #// 
    #// Filters the comment content before it is set.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $comment_content The comment content.
    #//
    commentdata_["comment_content"] = apply_filters("pre_comment_content", commentdata_["comment_content"])
    #// 
    #// Filters the comment author's IP address before it is set.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $comment_author_ip The comment author's IP address.
    #//
    commentdata_["comment_author_IP"] = apply_filters("pre_comment_user_ip", commentdata_["comment_author_IP"])
    #// This filter is documented in wp-includes/comment.php
    commentdata_["comment_author_url"] = apply_filters("pre_comment_author_url", commentdata_["comment_author_url"])
    #// This filter is documented in wp-includes/comment.php
    commentdata_["comment_author_email"] = apply_filters("pre_comment_author_email", commentdata_["comment_author_email"])
    commentdata_["filtered"] = True
    return commentdata_
# end def wp_filter_comment
#// 
#// Whether a comment should be blocked because of comment flood.
#// 
#// @since 2.1.0
#// 
#// @param bool $block Whether plugin has already blocked comment.
#// @param int $time_lastcomment Timestamp for last comment.
#// @param int $time_newcomment Timestamp for new comment.
#// @return bool Whether comment should be blocked.
#//
def wp_throttle_comment_flood(block_=None, time_lastcomment_=None, time_newcomment_=None, *_args_):
    
    
    if block_:
        #// A plugin has already blocked... we'll let that decision stand.
        return block_
    # end if
    if time_newcomment_ - time_lastcomment_ < 15:
        return True
    # end if
    return False
# end def wp_throttle_comment_flood
#// 
#// Adds a new comment to the database.
#// 
#// Filters new comment to ensure that the fields are sanitized and valid before
#// inserting comment into database. Calls {@see 'comment_post'} action with comment ID
#// and whether comment is approved by WordPress. Also has {@see 'preprocess_comment'}
#// filter for processing the comment data before the function handles it.
#// 
#// We use `REMOTE_ADDR` here directly. If you are behind a proxy, you should ensure
#// that it is properly set, such as in wp-config.php, for your environment.
#// 
#// See {@link https://core.trac.wordpress.org/ticket/9235}
#// 
#// @since 1.5.0
#// @since 4.3.0 'comment_agent' and 'comment_author_IP' can be set via `$commentdata`.
#// @since 4.7.0 The `$avoid_die` parameter was added, allowing the function to
#// return a WP_Error object instead of dying.
#// 
#// @see wp_insert_comment()
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $commentdata {
#// Comment data.
#// 
#// @type string $comment_author       The name of the comment author.
#// @type string $comment_author_email The comment author email address.
#// @type string $comment_author_url   The comment author URL.
#// @type string $comment_content      The content of the comment.
#// @type string $comment_date         The date the comment was submitted. Default is the current time.
#// @type string $comment_date_gmt     The date the comment was submitted in the GMT timezone.
#// Default is `$comment_date` in the GMT timezone.
#// @type int    $comment_parent       The ID of this comment's parent, if any. Default 0.
#// @type int    $comment_post_ID      The ID of the post that relates to the comment.
#// @type int    $user_id              The ID of the user who submitted the comment. Default 0.
#// @type int    $user_ID              Kept for backward-compatibility. Use `$user_id` instead.
#// @type string $comment_agent        Comment author user agent. Default is the value of 'HTTP_USER_AGENT'
#// in the `$_SERVER` superglobal sent in the original request.
#// @type string $comment_author_IP    Comment author IP address in IPv4 format. Default is the value of
#// 'REMOTE_ADDR' in the `$_SERVER` superglobal sent in the original request.
#// }
#// @param bool $avoid_die Should errors be returned as WP_Error objects instead of
#// executing wp_die()? Default false.
#// @return int|false|WP_Error The ID of the comment on success, false or WP_Error on failure.
#//
def wp_new_comment(commentdata_=None, avoid_die_=None, *_args_):
    if avoid_die_ is None:
        avoid_die_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (php_isset(lambda : commentdata_["user_ID"])):
        commentdata_["user_ID"] = php_int(commentdata_["user_ID"])
        commentdata_["user_id"] = commentdata_["user_ID"]
    # end if
    prefiltered_user_id_ = php_int(commentdata_["user_id"]) if (php_isset(lambda : commentdata_["user_id"])) else 0
    #// 
    #// Filters a comment's data before it is sanitized and inserted into the database.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $commentdata Comment data.
    #//
    commentdata_ = apply_filters("preprocess_comment", commentdata_)
    commentdata_["comment_post_ID"] = php_int(commentdata_["comment_post_ID"])
    if (php_isset(lambda : commentdata_["user_ID"])) and prefiltered_user_id_ != php_int(commentdata_["user_ID"]):
        commentdata_["user_ID"] = php_int(commentdata_["user_ID"])
        commentdata_["user_id"] = commentdata_["user_ID"]
    elif (php_isset(lambda : commentdata_["user_id"])):
        commentdata_["user_id"] = php_int(commentdata_["user_id"])
    # end if
    commentdata_["comment_parent"] = absint(commentdata_["comment_parent"]) if (php_isset(lambda : commentdata_["comment_parent"])) else 0
    parent_status_ = wp_get_comment_status(commentdata_["comment_parent"]) if 0 < commentdata_["comment_parent"] else ""
    commentdata_["comment_parent"] = commentdata_["comment_parent"] if "approved" == parent_status_ or "unapproved" == parent_status_ else 0
    if (not (php_isset(lambda : commentdata_["comment_author_IP"]))):
        commentdata_["comment_author_IP"] = PHP_SERVER["REMOTE_ADDR"]
    # end if
    commentdata_["comment_author_IP"] = php_preg_replace("/[^0-9a-fA-F:., ]/", "", commentdata_["comment_author_IP"])
    if (not (php_isset(lambda : commentdata_["comment_agent"]))):
        commentdata_["comment_agent"] = PHP_SERVER["HTTP_USER_AGENT"] if (php_isset(lambda : PHP_SERVER["HTTP_USER_AGENT"])) else ""
    # end if
    commentdata_["comment_agent"] = php_substr(commentdata_["comment_agent"], 0, 254)
    if php_empty(lambda : commentdata_["comment_date"]):
        commentdata_["comment_date"] = current_time("mysql")
    # end if
    if php_empty(lambda : commentdata_["comment_date_gmt"]):
        commentdata_["comment_date_gmt"] = current_time("mysql", 1)
    # end if
    commentdata_ = wp_filter_comment(commentdata_)
    commentdata_["comment_approved"] = wp_allow_comment(commentdata_, avoid_die_)
    if is_wp_error(commentdata_["comment_approved"]):
        return commentdata_["comment_approved"]
    # end if
    comment_ID_ = wp_insert_comment(commentdata_)
    if (not comment_ID_):
        fields_ = Array("comment_author", "comment_author_email", "comment_author_url", "comment_content")
        for field_ in fields_:
            if (php_isset(lambda : commentdata_[field_])):
                commentdata_[field_] = wpdb_.strip_invalid_text_for_column(wpdb_.comments, field_, commentdata_[field_])
            # end if
        # end for
        commentdata_ = wp_filter_comment(commentdata_)
        commentdata_["comment_approved"] = wp_allow_comment(commentdata_, avoid_die_)
        if is_wp_error(commentdata_["comment_approved"]):
            return commentdata_["comment_approved"]
        # end if
        comment_ID_ = wp_insert_comment(commentdata_)
        if (not comment_ID_):
            return False
        # end if
    # end if
    #// 
    #// Fires immediately after a comment is inserted into the database.
    #// 
    #// @since 1.2.0
    #// @since 4.5.0 The `$commentdata` parameter was added.
    #// 
    #// @param int        $comment_ID       The comment ID.
    #// @param int|string $comment_approved 1 if the comment is approved, 0 if not, 'spam' if spam.
    #// @param array      $commentdata      Comment data.
    #//
    do_action("comment_post", comment_ID_, commentdata_["comment_approved"], commentdata_)
    return comment_ID_
# end def wp_new_comment
#// 
#// Send a comment moderation notification to the comment moderator.
#// 
#// @since 4.4.0
#// 
#// @param int $comment_ID ID of the comment.
#// @return bool True on success, false on failure.
#//
def wp_new_comment_notify_moderator(comment_ID_=None, *_args_):
    
    
    comment_ = get_comment(comment_ID_)
    #// Only send notifications for pending comments.
    maybe_notify_ = "0" == comment_.comment_approved
    #// This filter is documented in wp-includes/comment.php
    maybe_notify_ = apply_filters("notify_moderator", maybe_notify_, comment_ID_)
    if (not maybe_notify_):
        return False
    # end if
    return wp_notify_moderator(comment_ID_)
# end def wp_new_comment_notify_moderator
#// 
#// Send a notification of a new comment to the post author.
#// 
#// @since 4.4.0
#// 
#// Uses the {@see 'notify_post_author'} filter to determine whether the post author
#// should be notified when a new comment is added, overriding site setting.
#// 
#// @param int $comment_ID Comment ID.
#// @return bool True on success, false on failure.
#//
def wp_new_comment_notify_postauthor(comment_ID_=None, *_args_):
    
    
    comment_ = get_comment(comment_ID_)
    maybe_notify_ = get_option("comments_notify")
    #// 
    #// Filters whether to send the post author new comment notification emails,
    #// overriding the site setting.
    #// 
    #// @since 4.4.0
    #// 
    #// @param bool $maybe_notify Whether to notify the post author about the new comment.
    #// @param int  $comment_ID   The ID of the comment for the notification.
    #//
    maybe_notify_ = apply_filters("notify_post_author", maybe_notify_, comment_ID_)
    #// 
    #// wp_notify_postauthor() checks if notifying the author of their own comment.
    #// By default, it won't, but filters can override this.
    #//
    if (not maybe_notify_):
        return False
    # end if
    #// Only send notifications for approved comments.
    if (not (php_isset(lambda : comment_.comment_approved))) or "1" != comment_.comment_approved:
        return False
    # end if
    return wp_notify_postauthor(comment_ID_)
# end def wp_new_comment_notify_postauthor
#// 
#// Sets the status of a comment.
#// 
#// The {@see 'wp_set_comment_status'} action is called after the comment is handled.
#// If the comment status is not in the list, then false is returned.
#// 
#// @since 1.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Comment $comment_id     Comment ID or WP_Comment object.
#// @param string         $comment_status New comment status, either 'hold', 'approve', 'spam', or 'trash'.
#// @param bool           $wp_error       Whether to return a WP_Error object if there is a failure. Default is false.
#// @return bool|WP_Error True on success, false or WP_Error on failure.
#//
def wp_set_comment_status(comment_id_=None, comment_status_=None, wp_error_=None, *_args_):
    if wp_error_ is None:
        wp_error_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    for case in Switch(comment_status_):
        if case("hold"):
            pass
        # end if
        if case("0"):
            status_ = "0"
            break
        # end if
        if case("approve"):
            pass
        # end if
        if case("1"):
            status_ = "1"
            add_action("wp_set_comment_status", "wp_new_comment_notify_postauthor")
            break
        # end if
        if case("spam"):
            status_ = "spam"
            break
        # end if
        if case("trash"):
            status_ = "trash"
            break
        # end if
        if case():
            return False
        # end if
    # end for
    comment_old_ = copy.deepcopy(get_comment(comment_id_))
    if (not wpdb_.update(wpdb_.comments, Array({"comment_approved": status_}), Array({"comment_ID": comment_old_.comment_ID}))):
        if wp_error_:
            return php_new_class("WP_Error", lambda : WP_Error("db_update_error", __("Could not update comment status"), wpdb_.last_error))
        else:
            return False
        # end if
    # end if
    clean_comment_cache(comment_old_.comment_ID)
    comment_ = get_comment(comment_old_.comment_ID)
    #// 
    #// Fires immediately before transitioning a comment's status from one to another
    #// in the database.
    #// 
    #// @since 1.5.0
    #// 
    #// @param int         $comment_id     Comment ID.
    #// @param string|bool $comment_status Current comment status. Possible values include
    #// 'hold', 'approve', 'spam', 'trash', or false.
    #//
    do_action("wp_set_comment_status", comment_.comment_ID, comment_status_)
    wp_transition_comment_status(comment_status_, comment_old_.comment_approved, comment_)
    wp_update_comment_count(comment_.comment_post_ID)
    return True
# end def wp_set_comment_status
#// 
#// Updates an existing comment in the database.
#// 
#// Filters the comment and makes sure certain fields are valid before updating.
#// 
#// @since 2.0.0
#// @since 4.9.0 Add updating comment meta during comment update.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $commentarr Contains information on the comment.
#// @return int The value 1 if the comment was updated, 0 if not updated.
#//
def wp_update_comment(commentarr_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// First, get all of the original fields.
    comment_ = get_comment(commentarr_["comment_ID"], ARRAY_A)
    if php_empty(lambda : comment_):
        return 0
    # end if
    #// Make sure that the comment post ID is valid (if specified).
    if (not php_empty(lambda : commentarr_["comment_post_ID"])) and (not get_post(commentarr_["comment_post_ID"])):
        return 0
    # end if
    #// Escape data pulled from DB.
    comment_ = wp_slash(comment_)
    old_status_ = comment_["comment_approved"]
    #// Merge old and new fields with new fields overwriting old ones.
    commentarr_ = php_array_merge(comment_, commentarr_)
    commentarr_ = wp_filter_comment(commentarr_)
    #// Now extract the merged array.
    data_ = wp_unslash(commentarr_)
    #// 
    #// Filters the comment content before it is updated in the database.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $comment_content The comment data.
    #//
    data_["comment_content"] = apply_filters("comment_save_pre", data_["comment_content"])
    data_["comment_date_gmt"] = get_gmt_from_date(data_["comment_date"])
    if (not (php_isset(lambda : data_["comment_approved"]))):
        data_["comment_approved"] = 1
    elif "hold" == data_["comment_approved"]:
        data_["comment_approved"] = 0
    elif "approve" == data_["comment_approved"]:
        data_["comment_approved"] = 1
    # end if
    comment_ID_ = data_["comment_ID"]
    comment_post_ID_ = data_["comment_post_ID"]
    #// 
    #// Filters the comment data immediately before it is updated in the database.
    #// 
    #// Note: data being passed to the filter is already unslashed.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $data       The new, processed comment data.
    #// @param array $comment    The old, unslashed comment data.
    #// @param array $commentarr The new, raw comment data.
    #//
    data_ = apply_filters("wp_update_comment_data", data_, comment_, commentarr_)
    keys_ = Array("comment_post_ID", "comment_content", "comment_author", "comment_author_email", "comment_approved", "comment_karma", "comment_author_url", "comment_date", "comment_date_gmt", "comment_type", "comment_parent", "user_id", "comment_agent", "comment_author_IP")
    data_ = wp_array_slice_assoc(data_, keys_)
    rval_ = wpdb_.update(wpdb_.comments, data_, php_compact("comment_ID_"))
    #// If metadata is provided, store it.
    if (php_isset(lambda : commentarr_["comment_meta"])) and php_is_array(commentarr_["comment_meta"]):
        for meta_key_,meta_value_ in commentarr_["comment_meta"].items():
            update_comment_meta(comment_ID_, meta_key_, meta_value_)
        # end for
    # end if
    clean_comment_cache(comment_ID_)
    wp_update_comment_count(comment_post_ID_)
    #// 
    #// Fires immediately after a comment is updated in the database.
    #// 
    #// The hook also fires immediately before comment status transition hooks are fired.
    #// 
    #// @since 1.2.0
    #// @since 4.6.0 Added the `$data` parameter.
    #// 
    #// @param int   $comment_ID The comment ID.
    #// @param array $data       Comment data.
    #//
    do_action("edit_comment", comment_ID_, data_)
    comment_ = get_comment(comment_ID_)
    wp_transition_comment_status(comment_.comment_approved, old_status_, comment_)
    return rval_
# end def wp_update_comment
#// 
#// Whether to defer comment counting.
#// 
#// When setting $defer to true, all post comment counts will not be updated
#// until $defer is set to false. When $defer is set to false, then all
#// previously deferred updated post comment counts will then be automatically
#// updated without having to call wp_update_comment_count() after.
#// 
#// @since 2.5.0
#// @staticvar bool $_defer
#// 
#// @param bool $defer
#// @return bool
#//
def wp_defer_comment_counting(defer_=None, *_args_):
    if defer_ is None:
        defer_ = None
    # end if
    
    _defer_ = False
    if php_is_bool(defer_):
        _defer_ = defer_
        #// Flush any deferred counts.
        if (not defer_):
            wp_update_comment_count(None, True)
        # end if
    # end if
    return _defer_
# end def wp_defer_comment_counting
#// 
#// Updates the comment count for post(s).
#// 
#// When $do_deferred is false (is by default) and the comments have been set to
#// be deferred, the post_id will be added to a queue, which will be updated at a
#// later date and only updated once per post ID.
#// 
#// If the comments have not be set up to be deferred, then the post will be
#// updated. When $do_deferred is set to true, then all previous deferred post
#// IDs will be updated along with the current $post_id.
#// 
#// @since 2.1.0
#// @see wp_update_comment_count_now() For what could cause a false return value
#// 
#// @staticvar array $_deferred
#// 
#// @param int|null $post_id     Post ID.
#// @param bool     $do_deferred Optional. Whether to process previously deferred
#// post comment counts. Default false.
#// @return bool|void True on success, false on failure or if post with ID does
#// not exist.
#//
def wp_update_comment_count(post_id_=None, do_deferred_=None, *_args_):
    if do_deferred_ is None:
        do_deferred_ = False
    # end if
    
    _deferred_ = Array()
    if php_empty(lambda : post_id_) and (not do_deferred_):
        return False
    # end if
    if do_deferred_:
        _deferred_ = array_unique(_deferred_)
        for i_,_post_id_ in _deferred_.items():
            wp_update_comment_count_now(_post_id_)
            _deferred_[i_] = None
            pass
        # end for
    # end if
    if wp_defer_comment_counting():
        _deferred_[-1] = post_id_
        return True
    elif post_id_:
        return wp_update_comment_count_now(post_id_)
    # end if
# end def wp_update_comment_count
#// 
#// Updates the comment count for the post.
#// 
#// @since 2.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $post_id Post ID
#// @return bool True on success, false if the post does not exist.
#//
def wp_update_comment_count_now(post_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_id_ = php_int(post_id_)
    if (not post_id_):
        return False
    # end if
    wp_cache_delete("comments-0", "counts")
    wp_cache_delete(str("comments-") + str(post_id_), "counts")
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    old_ = php_int(post_.comment_count)
    #// 
    #// Filters a post's comment count before it is updated in the database.
    #// 
    #// @since 4.5.0
    #// 
    #// @param int|null $new     The new comment count. Default null.
    #// @param int      $old     The old comment count.
    #// @param int      $post_id Post ID.
    #//
    new_ = apply_filters("pre_wp_update_comment_count_now", None, old_, post_id_)
    if php_is_null(new_):
        new_ = php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d AND comment_approved = '1'"), post_id_)))
    else:
        new_ = php_int(new_)
    # end if
    wpdb_.update(wpdb_.posts, Array({"comment_count": new_}), Array({"ID": post_id_}))
    clean_post_cache(post_)
    #// 
    #// Fires immediately after a post's comment count is updated in the database.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int $post_id Post ID.
    #// @param int $new     The new comment count.
    #// @param int $old     The old comment count.
    #//
    do_action("wp_update_comment_count", post_id_, new_, old_)
    #// This action is documented in wp-includes/post.php
    do_action(str("edit_post_") + str(post_.post_type), post_id_, post_)
    #// This action is documented in wp-includes/post.php
    do_action("edit_post", post_id_, post_)
    return True
# end def wp_update_comment_count_now
#// 
#// Ping and trackback functions.
#// 
#// 
#// Finds a pingback server URI based on the given URL.
#// 
#// Checks the HTML for the rel="pingback" link and x-pingback headers. It does
#// a check for the x-pingback headers first and returns that, if available. The
#// check for the rel="pingback" has more overhead than just the header.
#// 
#// @since 1.5.0
#// 
#// @param string $url URL to ping.
#// @param int $deprecated Not Used.
#// @return string|false String containing URI on success, false on failure.
#//
def discover_pingback_server_uri(url_=None, deprecated_="", *_args_):
    
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.7.0")
    # end if
    pingback_str_dquote_ = "rel=\"pingback\""
    pingback_str_squote_ = "rel='pingback'"
    #// @todo Should use Filter Extension or custom preg_match instead.
    parsed_url_ = php_parse_url(url_)
    if (not (php_isset(lambda : parsed_url_["host"]))):
        #// Not a URL. This should never happen.
        return False
    # end if
    #// Do not search for a pingback server on our own uploads.
    uploads_dir_ = wp_get_upload_dir()
    if 0 == php_strpos(url_, uploads_dir_["baseurl"]):
        return False
    # end if
    response_ = wp_safe_remote_head(url_, Array({"timeout": 2, "httpversion": "1.0"}))
    if is_wp_error(response_):
        return False
    # end if
    if wp_remote_retrieve_header(response_, "x-pingback"):
        return wp_remote_retrieve_header(response_, "x-pingback")
    # end if
    #// Not an (x)html, sgml, or xml page, no use going further.
    if php_preg_match("#(image|audio|video|model)/#is", wp_remote_retrieve_header(response_, "content-type")):
        return False
    # end if
    #// Now do a GET since we're going to look in the html headers (and we're sure it's not a binary file).
    response_ = wp_safe_remote_get(url_, Array({"timeout": 2, "httpversion": "1.0"}))
    if is_wp_error(response_):
        return False
    # end if
    contents_ = wp_remote_retrieve_body(response_)
    pingback_link_offset_dquote_ = php_strpos(contents_, pingback_str_dquote_)
    pingback_link_offset_squote_ = php_strpos(contents_, pingback_str_squote_)
    if pingback_link_offset_dquote_ or pingback_link_offset_squote_:
        quote_ = "\"" if pingback_link_offset_dquote_ else "'"
        pingback_link_offset_ = pingback_link_offset_dquote_ if "\"" == quote_ else pingback_link_offset_squote_
        pingback_href_pos_ = php_strpos(contents_, "href=", pingback_link_offset_)
        pingback_href_start_ = pingback_href_pos_ + 6
        pingback_href_end_ = php_strpos(contents_, quote_, pingback_href_start_)
        pingback_server_url_len_ = pingback_href_end_ - pingback_href_start_
        pingback_server_url_ = php_substr(contents_, pingback_href_start_, pingback_server_url_len_)
        #// We may find rel="pingback" but an incomplete pingback URL.
        if pingback_server_url_len_ > 0:
            #// We got it!
            return pingback_server_url_
        # end if
    # end if
    return False
# end def discover_pingback_server_uri
#// 
#// Perform all pingbacks, enclosures, trackbacks, and send to pingback services.
#// 
#// @since 2.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def do_all_pings(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Do pingbacks.
    pings_ = get_posts(Array({"post_type": get_post_types(), "suppress_filters": False, "nopaging": True, "meta_key": "_pingme", "fields": "ids"}))
    for ping_ in pings_:
        delete_post_meta(ping_, "_pingme")
        pingback(None, ping_)
    # end for
    #// Do enclosures.
    enclosures_ = get_posts(Array({"post_type": get_post_types(), "suppress_filters": False, "nopaging": True, "meta_key": "_encloseme", "fields": "ids"}))
    for enclosure_ in enclosures_:
        delete_post_meta(enclosure_, "_encloseme")
        do_enclose(None, enclosure_)
    # end for
    #// Do trackbacks.
    trackbacks_ = get_posts(Array({"post_type": get_post_types(), "suppress_filters": False, "nopaging": True, "meta_key": "_trackbackme", "fields": "ids"}))
    for trackback_ in trackbacks_:
        delete_post_meta(trackback_, "_trackbackme")
        do_trackbacks(trackback_)
    # end for
    #// Do Update Services/Generic Pings.
    generic_ping()
# end def do_all_pings
#// 
#// Perform trackbacks.
#// 
#// @since 1.5.0
#// @since 4.7.0 `$post_id` can be a WP_Post object.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Post $post_id Post object or ID to do trackbacks on.
#//
def do_trackbacks(post_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    to_ping_ = get_to_ping(post_)
    pinged_ = get_pung(post_)
    if php_empty(lambda : to_ping_):
        wpdb_.update(wpdb_.posts, Array({"to_ping": ""}), Array({"ID": post_.ID}))
        return
    # end if
    if php_empty(lambda : post_.post_excerpt):
        #// This filter is documented in wp-includes/post-template.php
        excerpt_ = apply_filters("the_content", post_.post_content, post_.ID)
    else:
        #// This filter is documented in wp-includes/post-template.php
        excerpt_ = apply_filters("the_excerpt", post_.post_excerpt)
    # end if
    excerpt_ = php_str_replace("]]>", "]]&gt;", excerpt_)
    excerpt_ = wp_html_excerpt(excerpt_, 252, "&#8230;")
    #// This filter is documented in wp-includes/post-template.php
    post_title_ = apply_filters("the_title", post_.post_title, post_.ID)
    post_title_ = strip_tags(post_title_)
    if to_ping_:
        for tb_ping_ in to_ping_:
            tb_ping_ = php_trim(tb_ping_)
            if (not php_in_array(tb_ping_, pinged_)):
                trackback(tb_ping_, post_title_, excerpt_, post_.ID)
                pinged_[-1] = tb_ping_
            else:
                wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.posts) + str(" SET to_ping = TRIM(REPLACE(to_ping, %s,\n                   '')) WHERE ID = %d"), tb_ping_, post_.ID))
            # end if
        # end for
    # end if
# end def do_trackbacks
#// 
#// Sends pings to all of the ping site services.
#// 
#// @since 1.2.0
#// 
#// @param int $post_id Post ID.
#// @return int Same as Post ID from parameter
#//
def generic_ping(post_id_=0, *_args_):
    
    
    services_ = get_option("ping_sites")
    services_ = php_explode("\n", services_)
    for service_ in services_:
        service_ = php_trim(service_)
        if "" != service_:
            weblog_ping(service_)
        # end if
    # end for
    return post_id_
# end def generic_ping
#// 
#// Pings back the links found in a post.
#// 
#// @since 0.71
#// @since 4.7.0 `$post_id` can be a WP_Post object.
#// 
#// @param string $content Post content to check for links. If empty will retrieve from post.
#// @param int|WP_Post $post_id Post Object or ID.
#//
def pingback(content_=None, post_id_=None, *_args_):
    
    
    php_include_file(ABSPATH + WPINC + "/class-IXR.php", once=False)
    php_include_file(ABSPATH + WPINC + "/class-wp-http-ixr-client.php", once=False)
    #// Original code by Mort (http://mort.mine.nu:8080).
    post_links_ = Array()
    post_ = get_post(post_id_)
    if (not post_):
        return
    # end if
    pung_ = get_pung(post_)
    if php_empty(lambda : content_):
        content_ = post_.post_content
    # end if
    #// 
    #// Step 1.
    #// Parsing the post, external links (if any) are stored in the $post_links array.
    #//
    post_links_temp_ = wp_extract_urls(content_)
    #// 
    #// Step 2.
    #// Walking through the links array.
    #// First we get rid of links pointing to sites, not to specific files.
    #// Example:
    #// http://dummy-weblog.org
    #// http://dummy-weblog.org
    #// http://dummy-weblog.org/post.php
    #// We don't wanna ping first and second types, even if they have a valid <link/>.
    #//
    for link_test_ in post_links_temp_:
        #// If we haven't pung it already and it isn't a link to itself.
        if (not php_in_array(link_test_, pung_)) and url_to_postid(link_test_) != post_.ID and (not is_local_attachment(link_test_)):
            test_ = php_no_error(lambda: php_parse_url(link_test_))
            if test_:
                if (php_isset(lambda : test_["query"])):
                    post_links_[-1] = link_test_
                elif (php_isset(lambda : test_["path"])) and "/" != test_["path"] and "" != test_["path"]:
                    post_links_[-1] = link_test_
                # end if
            # end if
        # end if
    # end for
    post_links_ = array_unique(post_links_)
    #// 
    #// Fires just before pinging back links found in a post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string[] $post_links Array of link URLs to be checked (passed by reference).
    #// @param string[] $pung       Array of link URLs already pinged (passed by reference).
    #// @param int      $post_ID    The post ID.
    #//
    do_action_ref_array("pre_ping", Array(post_links_, pung_, post_.ID))
    for pagelinkedto_ in post_links_:
        pingback_server_url_ = discover_pingback_server_uri(pagelinkedto_)
        if pingback_server_url_:
            set_time_limit(60)
            #// Now, the RPC call.
            pagelinkedfrom_ = get_permalink(post_)
            #// Using a timeout of 3 seconds should be enough to cover slow servers.
            client_ = php_new_class("WP_HTTP_IXR_Client", lambda : WP_HTTP_IXR_Client(pingback_server_url_))
            client_.timeout = 3
            #// 
            #// Filters the user agent sent when pinging-back a URL.
            #// 
            #// @since 2.9.0
            #// 
            #// @param string $concat_useragent    The user agent concatenated with ' -- WordPress/'
            #// and the WordPress version.
            #// @param string $useragent           The useragent.
            #// @param string $pingback_server_url The server URL being linked to.
            #// @param string $pagelinkedto        URL of page linked to.
            #// @param string $pagelinkedfrom      URL of page linked from.
            #//
            client_.useragent = apply_filters("pingback_useragent", client_.useragent + " -- WordPress/" + get_bloginfo("version"), client_.useragent, pingback_server_url_, pagelinkedto_, pagelinkedfrom_)
            #// When set to true, this outputs debug messages by itself.
            client_.debug = False
            if client_.query("pingback.ping", pagelinkedfrom_, pagelinkedto_) or (php_isset(lambda : client_.error.code)) and 48 == client_.error.code:
                #// Already registered.
                add_ping(post_, pagelinkedto_)
            # end if
        # end if
    # end for
# end def pingback
#// 
#// Check whether blog is public before returning sites.
#// 
#// @since 2.1.0
#// 
#// @param mixed $sites Will return if blog is public, will not return if not public.
#// @return mixed Empty string if blog is not public, returns $sites, if site is public.
#//
def privacy_ping_filter(sites_=None, *_args_):
    
    
    if "0" != get_option("blog_public"):
        return sites_
    else:
        return ""
    # end if
# end def privacy_ping_filter
#// 
#// Send a Trackback.
#// 
#// Updates database when sending trackback to prevent duplicates.
#// 
#// @since 0.71
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $trackback_url URL to send trackbacks.
#// @param string $title Title of post.
#// @param string $excerpt Excerpt of post.
#// @param int $ID Post ID.
#// @return int|false|void Database query from update.
#//
def trackback(trackback_url_=None, title_=None, excerpt_=None, ID_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : trackback_url_):
        return
    # end if
    options_ = Array()
    options_["timeout"] = 10
    options_["body"] = Array({"title": title_, "url": get_permalink(ID_), "blog_name": get_option("blogname"), "excerpt": excerpt_})
    response_ = wp_safe_remote_post(trackback_url_, options_)
    if is_wp_error(response_):
        return
    # end if
    wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.posts) + str(" SET pinged = CONCAT(pinged, '\n', %s) WHERE ID = %d"), trackback_url_, ID_))
    return wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.posts) + str(" SET to_ping = TRIM(REPLACE(to_ping, %s, '')) WHERE ID = %d"), trackback_url_, ID_))
# end def trackback
#// 
#// Send a pingback.
#// 
#// @since 1.2.0
#// 
#// @param string $server Host of blog to connect to.
#// @param string $path Path to send the ping.
#//
def weblog_ping(server_="", path_="", *_args_):
    
    
    php_include_file(ABSPATH + WPINC + "/class-IXR.php", once=False)
    php_include_file(ABSPATH + WPINC + "/class-wp-http-ixr-client.php", once=False)
    #// Using a timeout of 3 seconds should be enough to cover slow servers.
    client_ = php_new_class("WP_HTTP_IXR_Client", lambda : WP_HTTP_IXR_Client(server_, False if (not php_strlen(php_trim(path_))) or "/" == path_ else path_))
    client_.timeout = 3
    client_.useragent += " -- WordPress/" + get_bloginfo("version")
    #// When set to true, this outputs debug messages by itself.
    client_.debug = False
    home_ = trailingslashit(home_url())
    if (not client_.query("weblogUpdates.extendedPing", get_option("blogname"), home_, get_bloginfo("rss2_url"))):
        #// Then try a normal ping.
        client_.query("weblogUpdates.ping", get_option("blogname"), home_)
    # end if
# end def weblog_ping
#// 
#// Default filter attached to pingback_ping_source_uri to validate the pingback's Source URI
#// 
#// @since 3.5.1
#// @see wp_http_validate_url()
#// 
#// @param string $source_uri
#// @return string
#//
def pingback_ping_source_uri(source_uri_=None, *_args_):
    
    
    return php_str(wp_http_validate_url(source_uri_))
# end def pingback_ping_source_uri
#// 
#// Default filter attached to xmlrpc_pingback_error.
#// 
#// Returns a generic pingback error code unless the error code is 48,
#// which reports that the pingback is already registered.
#// 
#// @since 3.5.1
#// @link https://www.hixie.ch/specs/pingback/pingback#TOC3
#// 
#// @param IXR_Error $ixr_error
#// @return IXR_Error
#//
def xmlrpc_pingback_error(ixr_error_=None, *_args_):
    
    
    if 48 == ixr_error_.code:
        return ixr_error_
    # end if
    return php_new_class("IXR_Error", lambda : IXR_Error(0, ""))
# end def xmlrpc_pingback_error
#// 
#// Cache.
#// 
#// 
#// Removes a comment from the object cache.
#// 
#// @since 2.3.0
#// 
#// @param int|array $ids Comment ID or an array of comment IDs to remove from cache.
#//
def clean_comment_cache(ids_=None, *_args_):
    
    
    for id_ in ids_:
        wp_cache_delete(id_, "comment")
        #// 
        #// Fires immediately after a comment has been removed from the object cache.
        #// 
        #// @since 4.5.0
        #// 
        #// @param int $id Comment ID.
        #//
        do_action("clean_comment_cache", id_)
    # end for
    wp_cache_set("last_changed", php_microtime(), "comment")
# end def clean_comment_cache
#// 
#// Updates the comment cache of given comments.
#// 
#// Will add the comments in $comments to the cache. If comment ID already exists
#// in the comment cache then it will not be updated. The comment is added to the
#// cache using the comment group with the key using the ID of the comments.
#// 
#// @since 2.3.0
#// @since 4.4.0 Introduced the `$update_meta_cache` parameter.
#// 
#// @param WP_Comment[] $comments          Array of comment objects
#// @param bool         $update_meta_cache Whether to update commentmeta cache. Default true.
#//
def update_comment_cache(comments_=None, update_meta_cache_=None, *_args_):
    if update_meta_cache_ is None:
        update_meta_cache_ = True
    # end if
    
    for comment_ in comments_:
        wp_cache_add(comment_.comment_ID, comment_, "comment")
    # end for
    if update_meta_cache_:
        #// Avoid `wp_list_pluck()` in case `$comments` is passed by reference.
        comment_ids_ = Array()
        for comment_ in comments_:
            comment_ids_[-1] = comment_.comment_ID
        # end for
        update_meta_cache("comment", comment_ids_)
    # end if
# end def update_comment_cache
#// 
#// Adds any comments from the given IDs to the cache that do not already exist in cache.
#// 
#// @since 4.4.0
#// @access private
#// 
#// @see update_comment_cache()
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int[] $comment_ids       Array of comment IDs.
#// @param bool  $update_meta_cache Optional. Whether to update the meta cache. Default true.
#//
def _prime_comment_caches(comment_ids_=None, update_meta_cache_=None, *_args_):
    if update_meta_cache_ is None:
        update_meta_cache_ = True
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    non_cached_ids_ = _get_non_cached_ids(comment_ids_, "comment")
    if (not php_empty(lambda : non_cached_ids_)):
        fresh_comments_ = wpdb_.get_results(php_sprintf(str("SELECT ") + str(wpdb_.comments) + str(".* FROM ") + str(wpdb_.comments) + str(" WHERE comment_ID IN (%s)"), php_join(",", php_array_map("intval", non_cached_ids_))))
        update_comment_cache(fresh_comments_, update_meta_cache_)
    # end if
# end def _prime_comment_caches
#// 
#// Internal.
#// 
#// 
#// Close comments on old posts on the fly, without any extra DB queries. Hooked to the_posts.
#// 
#// @access private
#// @since 2.7.0
#// 
#// @param WP_Post  $posts Post data object.
#// @param WP_Query $query Query object.
#// @return array
#//
def _close_comments_for_old_posts(posts_=None, query_=None, *_args_):
    
    
    if php_empty(lambda : posts_) or (not query_.is_singular()) or (not get_option("close_comments_for_old_posts")):
        return posts_
    # end if
    #// 
    #// Filters the list of post types to automatically close comments for.
    #// 
    #// @since 3.2.0
    #// 
    #// @param string[] $post_types An array of post type names.
    #//
    post_types_ = apply_filters("close_comments_for_post_types", Array("post"))
    if (not php_in_array(posts_[0].post_type, post_types_)):
        return posts_
    # end if
    days_old_ = php_int(get_option("close_comments_days_old"))
    if (not days_old_):
        return posts_
    # end if
    if time() - strtotime(posts_[0].post_date_gmt) > days_old_ * DAY_IN_SECONDS:
        posts_[0].comment_status = "closed"
        posts_[0].ping_status = "closed"
    # end if
    return posts_
# end def _close_comments_for_old_posts
#// 
#// Close comments on an old post. Hooked to comments_open and pings_open.
#// 
#// @access private
#// @since 2.7.0
#// 
#// @param bool $open Comments open or closed
#// @param int $post_id Post ID
#// @return bool $open
#//
def _close_comments_for_old_post(open_=None, post_id_=None, *_args_):
    
    
    if (not open_):
        return open_
    # end if
    if (not get_option("close_comments_for_old_posts")):
        return open_
    # end if
    days_old_ = php_int(get_option("close_comments_days_old"))
    if (not days_old_):
        return open_
    # end if
    post_ = get_post(post_id_)
    #// This filter is documented in wp-includes/comment.php
    post_types_ = apply_filters("close_comments_for_post_types", Array("post"))
    if (not php_in_array(post_.post_type, post_types_)):
        return open_
    # end if
    #// Undated drafts should not show up as comments closed.
    if "0000-00-00 00:00:00" == post_.post_date_gmt:
        return open_
    # end if
    if time() - strtotime(post_.post_date_gmt) > days_old_ * DAY_IN_SECONDS:
        return False
    # end if
    return open_
# end def _close_comments_for_old_post
#// 
#// Handles the submission of a comment, usually posted to wp-comments-post.php via a comment form.
#// 
#// This function expects unslashed data, as opposed to functions such as `wp_new_comment()` which
#// expect slashed data.
#// 
#// @since 4.4.0
#// 
#// @param array $comment_data {
#// Comment data.
#// 
#// @type string|int $comment_post_ID             The ID of the post that relates to the comment.
#// @type string     $author                      The name of the comment author.
#// @type string     $email                       The comment author email address.
#// @type string     $url                         The comment author URL.
#// @type string     $comment                     The content of the comment.
#// @type string|int $comment_parent              The ID of this comment's parent, if any. Default 0.
#// @type string     $_wp_unfiltered_html_comment The nonce value for allowing unfiltered HTML.
#// }
#// @return WP_Comment|WP_Error A WP_Comment object on success, a WP_Error object on failure.
#//
def wp_handle_comment_submission(comment_data_=None, *_args_):
    
    
    comment_post_ID_ = 0
    comment_parent_ = 0
    user_ID_ = 0
    comment_author_ = None
    comment_author_email_ = None
    comment_author_url_ = None
    comment_content_ = None
    if (php_isset(lambda : comment_data_["comment_post_ID"])):
        comment_post_ID_ = php_int(comment_data_["comment_post_ID"])
    # end if
    if (php_isset(lambda : comment_data_["author"])) and php_is_string(comment_data_["author"]):
        comment_author_ = php_trim(strip_tags(comment_data_["author"]))
    # end if
    if (php_isset(lambda : comment_data_["email"])) and php_is_string(comment_data_["email"]):
        comment_author_email_ = php_trim(comment_data_["email"])
    # end if
    if (php_isset(lambda : comment_data_["url"])) and php_is_string(comment_data_["url"]):
        comment_author_url_ = php_trim(comment_data_["url"])
    # end if
    if (php_isset(lambda : comment_data_["comment"])) and php_is_string(comment_data_["comment"]):
        comment_content_ = php_trim(comment_data_["comment"])
    # end if
    if (php_isset(lambda : comment_data_["comment_parent"])):
        comment_parent_ = absint(comment_data_["comment_parent"])
    # end if
    post_ = get_post(comment_post_ID_)
    if php_empty(lambda : post_.comment_status):
        #// 
        #// Fires when a comment is attempted on a post that does not exist.
        #// 
        #// @since 1.5.0
        #// 
        #// @param int $comment_post_ID Post ID.
        #//
        do_action("comment_id_not_found", comment_post_ID_)
        return php_new_class("WP_Error", lambda : WP_Error("comment_id_not_found"))
    # end if
    #// get_post_status() will get the parent status for attachments.
    status_ = get_post_status(post_)
    if "private" == status_ and (not current_user_can("read_post", comment_post_ID_)):
        return php_new_class("WP_Error", lambda : WP_Error("comment_id_not_found"))
    # end if
    status_obj_ = get_post_status_object(status_)
    if (not comments_open(comment_post_ID_)):
        #// 
        #// Fires when a comment is attempted on a post that has comments closed.
        #// 
        #// @since 1.5.0
        #// 
        #// @param int $comment_post_ID Post ID.
        #//
        do_action("comment_closed", comment_post_ID_)
        return php_new_class("WP_Error", lambda : WP_Error("comment_closed", __("Sorry, comments are closed for this item."), 403))
    elif "trash" == status_:
        #// 
        #// Fires when a comment is attempted on a trashed post.
        #// 
        #// @since 2.9.0
        #// 
        #// @param int $comment_post_ID Post ID.
        #//
        do_action("comment_on_trash", comment_post_ID_)
        return php_new_class("WP_Error", lambda : WP_Error("comment_on_trash"))
    elif (not status_obj_.public) and (not status_obj_.private):
        #// 
        #// Fires when a comment is attempted on a post in draft mode.
        #// 
        #// @since 1.5.1
        #// 
        #// @param int $comment_post_ID Post ID.
        #//
        do_action("comment_on_draft", comment_post_ID_)
        if current_user_can("read_post", comment_post_ID_):
            return php_new_class("WP_Error", lambda : WP_Error("comment_on_draft", __("Sorry, comments are not allowed for this item."), 403))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("comment_on_draft"))
        # end if
    elif post_password_required(comment_post_ID_):
        #// 
        #// Fires when a comment is attempted on a password-protected post.
        #// 
        #// @since 2.9.0
        #// 
        #// @param int $comment_post_ID Post ID.
        #//
        do_action("comment_on_password_protected", comment_post_ID_)
        return php_new_class("WP_Error", lambda : WP_Error("comment_on_password_protected"))
    else:
        #// 
        #// Fires before a comment is posted.
        #// 
        #// @since 2.8.0
        #// 
        #// @param int $comment_post_ID Post ID.
        #//
        do_action("pre_comment_on_post", comment_post_ID_)
    # end if
    #// If the user is logged in.
    user_ = wp_get_current_user()
    if user_.exists():
        if php_empty(lambda : user_.display_name):
            user_.display_name = user_.user_login
        # end if
        comment_author_ = user_.display_name
        comment_author_email_ = user_.user_email
        comment_author_url_ = user_.user_url
        user_ID_ = user_.ID
        if current_user_can("unfiltered_html"):
            if (not (php_isset(lambda : comment_data_["_wp_unfiltered_html_comment"]))) or (not wp_verify_nonce(comment_data_["_wp_unfiltered_html_comment"], "unfiltered-html-comment_" + comment_post_ID_)):
                kses_remove_filters()
                #// Start with a clean slate.
                kses_init_filters()
                #// Set up the filters.
                remove_filter("pre_comment_content", "wp_filter_post_kses")
                add_filter("pre_comment_content", "wp_filter_kses")
            # end if
        # end if
    else:
        if get_option("comment_registration"):
            return php_new_class("WP_Error", lambda : WP_Error("not_logged_in", __("Sorry, you must be logged in to comment."), 403))
        # end if
    # end if
    comment_type_ = ""
    if get_option("require_name_email") and (not user_.exists()):
        if "" == comment_author_email_ or "" == comment_author_:
            return php_new_class("WP_Error", lambda : WP_Error("require_name_email", __("<strong>Error</strong>: Please fill the required fields (name, email)."), 200))
        elif (not is_email(comment_author_email_)):
            return php_new_class("WP_Error", lambda : WP_Error("require_valid_email", __("<strong>Error</strong>: Please enter a valid email address."), 200))
        # end if
    # end if
    commentdata_ = php_compact("comment_post_ID_", "comment_author_", "comment_author_email_", "comment_author_url_", "comment_content_", "comment_type_", "comment_parent_", "user_ID_")
    #// 
    #// Filters whether an empty comment should be allowed.
    #// 
    #// @since 5.1.0
    #// 
    #// @param bool  $allow_empty_comment Whether to allow empty comments. Default false.
    #// @param array $commentdata         Array of comment data to be sent to wp_insert_comment().
    #//
    allow_empty_comment_ = apply_filters("allow_empty_comment", False, commentdata_)
    if "" == comment_content_ and (not allow_empty_comment_):
        return php_new_class("WP_Error", lambda : WP_Error("require_valid_comment", __("<strong>Error</strong>: Please type a comment."), 200))
    # end if
    check_max_lengths_ = wp_check_comment_data_max_lengths(commentdata_)
    if is_wp_error(check_max_lengths_):
        return check_max_lengths_
    # end if
    comment_id_ = wp_new_comment(wp_slash(commentdata_), True)
    if is_wp_error(comment_id_):
        return comment_id_
    # end if
    if (not comment_id_):
        return php_new_class("WP_Error", lambda : WP_Error("comment_save_error", __("<strong>Error</strong>: The comment could not be saved. Please try again later."), 500))
    # end if
    return get_comment(comment_id_)
# end def wp_handle_comment_submission
#// 
#// Registers the personal data exporter for comments.
#// 
#// @since 4.9.6
#// 
#// @param array $exporters An array of personal data exporters.
#// @return array An array of personal data exporters.
#//
def wp_register_comment_personal_data_exporter(exporters_=None, *_args_):
    
    
    exporters_["wordpress-comments"] = Array({"exporter_friendly_name": __("WordPress Comments"), "callback": "wp_comments_personal_data_exporter"})
    return exporters_
# end def wp_register_comment_personal_data_exporter
#// 
#// Finds and exports personal data associated with an email address from the comments table.
#// 
#// @since 4.9.6
#// 
#// @param string $email_address The comment author email address.
#// @param int    $page          Comment page.
#// @return array An array of personal data.
#//
def wp_comments_personal_data_exporter(email_address_=None, page_=1, *_args_):
    
    
    #// Limit us to 500 comments at a time to avoid timing out.
    number_ = 500
    page_ = php_int(page_)
    data_to_export_ = Array()
    comments_ = get_comments(Array({"author_email": email_address_, "number": number_, "paged": page_, "order_by": "comment_ID", "order": "ASC", "update_comment_meta_cache": False}))
    comment_prop_to_export_ = Array({"comment_author": __("Comment Author"), "comment_author_email": __("Comment Author Email"), "comment_author_url": __("Comment Author URL"), "comment_author_IP": __("Comment Author IP"), "comment_agent": __("Comment Author User Agent"), "comment_date": __("Comment Date"), "comment_content": __("Comment Content"), "comment_link": __("Comment URL")})
    for comment_ in comments_:
        comment_data_to_export_ = Array()
        for key_,name_ in comment_prop_to_export_.items():
            value_ = ""
            for case in Switch(key_):
                if case("comment_author"):
                    pass
                # end if
                if case("comment_author_email"):
                    pass
                # end if
                if case("comment_author_url"):
                    pass
                # end if
                if case("comment_author_IP"):
                    pass
                # end if
                if case("comment_agent"):
                    pass
                # end if
                if case("comment_date"):
                    value_ = comment_.key_
                    break
                # end if
                if case("comment_content"):
                    value_ = get_comment_text(comment_.comment_ID)
                    break
                # end if
                if case("comment_link"):
                    value_ = get_comment_link(comment_.comment_ID)
                    value_ = php_sprintf("<a href=\"%s\" target=\"_blank\" rel=\"noreferrer noopener\">%s</a>", esc_url(value_), esc_html(value_))
                    break
                # end if
            # end for
            if (not php_empty(lambda : value_)):
                comment_data_to_export_[-1] = Array({"name": name_, "value": value_})
            # end if
        # end for
        data_to_export_[-1] = Array({"group_id": "comments", "group_label": __("Comments"), "group_description": __("User&#8217;s comment data."), "item_id": str("comment-") + str(comment_.comment_ID), "data": comment_data_to_export_})
    # end for
    done_ = php_count(comments_) < number_
    return Array({"data": data_to_export_, "done": done_})
# end def wp_comments_personal_data_exporter
#// 
#// Registers the personal data eraser for comments.
#// 
#// @since 4.9.6
#// 
#// @param  array $erasers An array of personal data erasers.
#// @return array An array of personal data erasers.
#//
def wp_register_comment_personal_data_eraser(erasers_=None, *_args_):
    
    
    erasers_["wordpress-comments"] = Array({"eraser_friendly_name": __("WordPress Comments"), "callback": "wp_comments_personal_data_eraser"})
    return erasers_
# end def wp_register_comment_personal_data_eraser
#// 
#// Erases personal data associated with an email address from the comments table.
#// 
#// @since 4.9.6
#// 
#// @param  string $email_address The comment author email address.
#// @param  int    $page          Comment page.
#// @return array
#//
def wp_comments_personal_data_eraser(email_address_=None, page_=1, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : email_address_):
        return Array({"items_removed": False, "items_retained": False, "messages": Array(), "done": True})
    # end if
    #// Limit us to 500 comments at a time to avoid timing out.
    number_ = 500
    page_ = php_int(page_)
    items_removed_ = False
    items_retained_ = False
    comments_ = get_comments(Array({"author_email": email_address_, "number": number_, "paged": page_, "order_by": "comment_ID", "order": "ASC", "include_unapproved": True}))
    #// translators: Name of a comment's author after being anonymized.
    anon_author_ = __("Anonymous")
    messages_ = Array()
    for comment_ in comments_:
        anonymized_comment_ = Array()
        anonymized_comment_["comment_agent"] = ""
        anonymized_comment_["comment_author"] = anon_author_
        anonymized_comment_["comment_author_email"] = ""
        anonymized_comment_["comment_author_IP"] = wp_privacy_anonymize_data("ip", comment_.comment_author_IP)
        anonymized_comment_["comment_author_url"] = ""
        anonymized_comment_["user_id"] = 0
        comment_id_ = php_int(comment_.comment_ID)
        #// 
        #// Filters whether to anonymize the comment.
        #// 
        #// @since 4.9.6
        #// 
        #// @param bool|string $anon_message       Whether to apply the comment anonymization (bool) or a custom
        #// message (string). Default true.
        #// @param WP_Comment  $comment            WP_Comment object.
        #// @param array       $anonymized_comment Anonymized comment data.
        #//
        anon_message_ = apply_filters("wp_anonymize_comment", True, comment_, anonymized_comment_)
        if True != anon_message_:
            if anon_message_ and php_is_string(anon_message_):
                messages_[-1] = esc_html(anon_message_)
            else:
                #// translators: %d: Comment ID.
                messages_[-1] = php_sprintf(__("Comment %d contains personal data but could not be anonymized."), comment_id_)
            # end if
            items_retained_ = True
            continue
        # end if
        args_ = Array({"comment_ID": comment_id_})
        updated_ = wpdb_.update(wpdb_.comments, anonymized_comment_, args_)
        if updated_:
            items_removed_ = True
            clean_comment_cache(comment_id_)
        else:
            items_retained_ = True
        # end if
    # end for
    done_ = php_count(comments_) < number_
    return Array({"items_removed": items_removed_, "items_retained": items_retained_, "messages": messages_, "done": done_})
# end def wp_comments_personal_data_eraser
#// 
#// Sets the last changed time for the 'comment' cache group.
#// 
#// @since 5.0.0
#//
def wp_cache_set_comments_last_changed(*_args_):
    
    
    wp_cache_set("last_changed", php_microtime(), "comment")
# end def wp_cache_set_comments_last_changed
