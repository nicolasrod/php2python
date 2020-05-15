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
#// Comment template functions
#// 
#// These functions are meant to live inside of the WordPress loop.
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// Retrieves the author of the current comment.
#// 
#// If the comment has an empty comment_author field, then 'Anonymous' person is
#// assumed.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to retrieve the author.
#// Default current comment.
#// @return string The comment author
#//
def get_comment_author(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    if php_empty(lambda : comment.comment_author):
        user = get_userdata(comment.user_id) if comment.user_id else False
        if user:
            author = user.display_name
        else:
            author = __("Anonymous")
        # end if
    else:
        author = comment.comment_author
    # end if
    #// 
    #// Filters the returned comment author name.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$comment_ID` and `$comment` parameters were added.
    #// 
    #// @param string     $author     The comment author's username.
    #// @param int        $comment_ID The comment ID.
    #// @param WP_Comment $comment    The comment object.
    #//
    return apply_filters("get_comment_author", author, comment.comment_ID, comment)
# end def get_comment_author
#// 
#// Displays the author of the current comment.
#// 
#// @since 0.71
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to print the author.
#// Default current comment.
#//
def comment_author(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    author = get_comment_author(comment)
    #// 
    #// Filters the comment author's name for display.
    #// 
    #// @since 1.2.0
    #// @since 4.1.0 The `$comment_ID` parameter was added.
    #// 
    #// @param string $author     The comment author's username.
    #// @param int    $comment_ID The comment ID.
    #//
    php_print(apply_filters("comment_author", author, comment.comment_ID))
# end def comment_author
#// 
#// Retrieves the email of the author of the current comment.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to get the author's email.
#// Default current comment.
#// @return string The current comment author's email
#//
def get_comment_author_email(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    #// 
    #// Filters the comment author's returned email address.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$comment_ID` and `$comment` parameters were added.
    #// 
    #// @param string     $comment_author_email The comment author's email address.
    #// @param int        $comment_ID           The comment ID.
    #// @param WP_Comment $comment              The comment object.
    #//
    return apply_filters("get_comment_author_email", comment.comment_author_email, comment.comment_ID, comment)
# end def get_comment_author_email
#// 
#// Displays the email of the author of the current global $comment.
#// 
#// Care should be taken to protect the email address and assure that email
#// harvesters do not capture your commenter's email address. Most assume that
#// their email address will not appear in raw form on the site. Doing so will
#// enable anyone, including those that people don't want to get the email
#// address and use it for their own means good and bad.
#// 
#// @since 0.71
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to print the author's email.
#// Default current comment.
#//
def comment_author_email(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    author_email = get_comment_author_email(comment)
    #// 
    #// Filters the comment author's email for display.
    #// 
    #// @since 1.2.0
    #// @since 4.1.0 The `$comment_ID` parameter was added.
    #// 
    #// @param string $author_email The comment author's email address.
    #// @param int    $comment_ID   The comment ID.
    #//
    php_print(apply_filters("author_email", author_email, comment.comment_ID))
# end def comment_author_email
#// 
#// Displays the HTML email link to the author of the current comment.
#// 
#// Care should be taken to protect the email address and assure that email
#// harvesters do not capture your commenter's email address. Most assume that
#// their email address will not appear in raw form on the site. Doing so will
#// enable anyone, including those that people don't want to get the email
#// address and use it for their own means good and bad.
#// 
#// @since 0.71
#// @since 4.6.0 Added the `$comment` parameter.
#// 
#// @param string         $linktext Optional. Text to display instead of the comment author's email address.
#// Default empty.
#// @param string         $before   Optional. Text or HTML to display before the email link. Default empty.
#// @param string         $after    Optional. Text or HTML to display after the email link. Default empty.
#// @param int|WP_Comment $comment  Optional. Comment ID or WP_Comment object. Default is the current comment.
#//
def comment_author_email_link(linktext="", before="", after="", comment=None, *args_):
    
    link = get_comment_author_email_link(linktext, before, after, comment)
    if link:
        php_print(link)
    # end if
# end def comment_author_email_link
#// 
#// Returns the HTML email link to the author of the current comment.
#// 
#// Care should be taken to protect the email address and assure that email
#// harvesters do not capture your commenter's email address. Most assume that
#// their email address will not appear in raw form on the site. Doing so will
#// enable anyone, including those that people don't want to get the email
#// address and use it for their own means good and bad.
#// 
#// @since 2.7.0
#// @since 4.6.0 Added the `$comment` parameter.
#// 
#// @param string         $linktext Optional. Text to display instead of the comment author's email address.
#// Default empty.
#// @param string         $before   Optional. Text or HTML to display before the email link. Default empty.
#// @param string         $after    Optional. Text or HTML to display after the email link. Default empty.
#// @param int|WP_Comment $comment  Optional. Comment ID or WP_Comment object. Default is the current comment.
#// @return string HTML markup for the comment author email link. By default, the email address is obfuscated
#// via the {@see 'comment_email'} filter with antispambot().
#//
def get_comment_author_email_link(linktext="", before="", after="", comment=None, *args_):
    
    comment = get_comment(comment)
    #// 
    #// Filters the comment author's email for display.
    #// 
    #// Care should be taken to protect the email address and assure that email
    #// harvesters do not capture your commenter's email address.
    #// 
    #// @since 1.2.0
    #// @since 4.1.0 The `$comment` parameter was added.
    #// 
    #// @param string     $comment_author_email The comment author's email address.
    #// @param WP_Comment $comment              The comment object.
    #//
    email = apply_filters("comment_email", comment.comment_author_email, comment)
    if (not php_empty(lambda : email)) and "@" != email:
        display = linktext if "" != linktext else email
        return_ = before
        return_ += php_sprintf("<a href=\"%1$s\">%2$s</a>", esc_url("mailto:" + email), esc_html(display))
        return_ += after
        return return_
    else:
        return ""
    # end if
# end def get_comment_author_email_link
#// 
#// Retrieves the HTML link to the URL of the author of the current comment.
#// 
#// Both get_comment_author_url() and get_comment_author() rely on get_comment(),
#// which falls back to the global comment variable if the $comment_ID argument is empty.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to get the author's link.
#// Default current comment.
#// @return string The comment author name or HTML link for author's URL.
#//
def get_comment_author_link(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    url = get_comment_author_url(comment)
    author = get_comment_author(comment)
    if php_empty(lambda : url) or "http://" == url:
        return_ = author
    else:
        return_ = str("<a href='") + str(url) + str("' rel='external nofollow ugc' class='url'>") + str(author) + str("</a>")
    # end if
    #// 
    #// Filters the comment author's link for display.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$author` and `$comment_ID` parameters were added.
    #// 
    #// @param string $return     The HTML-formatted comment author link.
    #// Empty for an invalid URL.
    #// @param string $author     The comment author's username.
    #// @param int    $comment_ID The comment ID.
    #//
    return apply_filters("get_comment_author_link", return_, author, comment.comment_ID)
# end def get_comment_author_link
#// 
#// Displays the HTML link to the URL of the author of the current comment.
#// 
#// @since 0.71
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to print the author's link.
#// Default current comment.
#//
def comment_author_link(comment_ID=0, *args_):
    
    php_print(get_comment_author_link(comment_ID))
# end def comment_author_link
#// 
#// Retrieve the IP address of the author of the current comment.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to get the author's IP address.
#// Default current comment.
#// @return string Comment author's IP address.
#//
def get_comment_author_IP(comment_ID=0, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    comment = get_comment(comment_ID)
    #// 
    #// Filters the comment author's returned IP address.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$comment_ID` and `$comment` parameters were added.
    #// 
    #// @param string     $comment_author_IP The comment author's IP address.
    #// @param int        $comment_ID        The comment ID.
    #// @param WP_Comment $comment           The comment object.
    #//
    return apply_filters("get_comment_author_IP", comment.comment_author_IP, comment.comment_ID, comment)
    pass
# end def get_comment_author_IP
#// 
#// Displays the IP address of the author of the current comment.
#// 
#// @since 0.71
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to print the author's IP address.
#// Default current comment.
#//
def comment_author_IP(comment_ID=0, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    php_print(esc_html(get_comment_author_IP(comment_ID)))
# end def comment_author_IP
#// 
#// Retrieves the URL of the author of the current comment, not linked.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to get the author's URL.
#// Default current comment.
#// @return string Comment author URL, if provided, an empty string otherwise.
#//
def get_comment_author_url(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    url = ""
    id = 0
    if (not php_empty(lambda : comment)):
        author_url = "" if "http://" == comment.comment_author_url else comment.comment_author_url
        url = esc_url(author_url, Array("http", "https"))
        id = comment.comment_ID
    # end if
    #// 
    #// Filters the comment author's URL.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$comment_ID` and `$comment` parameters were added.
    #// 
    #// @param string     $url        The comment author's URL.
    #// @param int        $comment_ID The comment ID.
    #// @param WP_Comment $comment    The comment object.
    #//
    return apply_filters("get_comment_author_url", url, id, comment)
# end def get_comment_author_url
#// 
#// Displays the URL of the author of the current comment, not linked.
#// 
#// @since 0.71
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or the ID of the comment for which to print the author's URL.
#// Default current comment.
#//
def comment_author_url(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    author_url = get_comment_author_url(comment)
    #// 
    #// Filters the comment author's URL for display.
    #// 
    #// @since 1.2.0
    #// @since 4.1.0 The `$comment_ID` parameter was added.
    #// 
    #// @param string $author_url The comment author's URL.
    #// @param int    $comment_ID The comment ID.
    #//
    php_print(apply_filters("comment_url", author_url, comment.comment_ID))
# end def comment_author_url
#// 
#// Retrieves the HTML link of the URL of the author of the current comment.
#// 
#// $linktext parameter is only used if the URL does not exist for the comment
#// author. If the URL does exist then the URL will be used and the $linktext
#// will be ignored.
#// 
#// Encapsulate the HTML link between the $before and $after. So it will appear
#// in the order of $before, link, and finally $after.
#// 
#// @since 1.5.0
#// @since 4.6.0 Added the `$comment` parameter.
#// 
#// @param string         $linktext Optional. The text to display instead of the comment
#// author's email address. Default empty.
#// @param string         $before   Optional. The text or HTML to display before the email link.
#// Default empty.
#// @param string         $after    Optional. The text or HTML to display after the email link.
#// Default empty.
#// @param int|WP_Comment $comment  Optional. Comment ID or WP_Comment object.
#// Default is the current comment.
#// @return string The HTML link between the $before and $after parameters.
#//
def get_comment_author_url_link(linktext="", before="", after="", comment=0, *args_):
    
    url = get_comment_author_url(comment)
    display = linktext if "" != linktext else url
    display = php_str_replace("http://www.", "", display)
    display = php_str_replace("http://", "", display)
    if "/" == php_substr(display, -1):
        display = php_substr(display, 0, -1)
    # end if
    return_ = str(before) + str("<a href='") + str(url) + str("' rel='external'>") + str(display) + str("</a>") + str(after)
    #// 
    #// Filters the comment author's returned URL link.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $return The HTML-formatted comment author URL link.
    #//
    return apply_filters("get_comment_author_url_link", return_)
# end def get_comment_author_url_link
#// 
#// Displays the HTML link of the URL of the author of the current comment.
#// 
#// @since 0.71
#// @since 4.6.0 Added the `$comment` parameter.
#// 
#// @param string         $linktext Optional. Text to display instead of the comment author's
#// email address. Default empty.
#// @param string         $before   Optional. Text or HTML to display before the email link.
#// Default empty.
#// @param string         $after    Optional. Text or HTML to display after the email link.
#// Default empty.
#// @param int|WP_Comment $comment  Optional. Comment ID or WP_Comment object.
#// Default is the current comment.
#//
def comment_author_url_link(linktext="", before="", after="", comment=0, *args_):
    
    php_print(get_comment_author_url_link(linktext, before, after, comment))
# end def comment_author_url_link
#// 
#// Generates semantic classes for each comment element.
#// 
#// @since 2.7.0
#// @since 4.4.0 Added the ability for `$comment` to also accept a WP_Comment object.
#// 
#// @param string|array   $class    Optional. One or more classes to add to the class list.
#// Default empty.
#// @param int|WP_Comment $comment  Comment ID or WP_Comment object. Default current comment.
#// @param int|WP_Post    $post_id  Post ID or WP_Post object. Default current post.
#// @param bool           $echo     Optional. Whether to echo or return the output.
#// Default true.
#// @return void|string Void if `$echo` argument is true, comment classes if `$echo` is false.
#//
def comment_class(class_="", comment=None, post_id=None, echo=True, *args_):
    
    #// Separates classes with a single space, collates classes for comment DIV.
    class_ = "class=\"" + join(" ", get_comment_class(class_, comment, post_id)) + "\""
    if echo:
        php_print(class_)
    else:
        return class_
    # end if
# end def comment_class
#// 
#// Returns the classes for the comment div as an array.
#// 
#// @since 2.7.0
#// @since 4.4.0 Added the ability for `$comment_id` to also accept a WP_Comment object.
#// 
#// @global int $comment_alt
#// @global int $comment_depth
#// @global int $comment_thread_alt
#// 
#// @param string|array   $class      Optional. One or more classes to add to the class list. Default empty.
#// @param int|WP_Comment $comment_id Comment ID or WP_Comment object. Default current comment.
#// @param int|WP_Post    $post_id    Post ID or WP_Post object. Default current post.
#// @return string[] An array of classes.
#//
def get_comment_class(class_="", comment_id=None, post_id=None, *args_):
    
    global comment_alt,comment_depth,comment_thread_alt
    php_check_if_defined("comment_alt","comment_depth","comment_thread_alt")
    classes = Array()
    comment = get_comment(comment_id)
    if (not comment):
        return classes
    # end if
    #// Get the comment type (comment, trackback).
    classes[-1] = "comment" if php_empty(lambda : comment.comment_type) else comment.comment_type
    #// Add classes for comment authors that are registered users.
    user = get_userdata(comment.user_id) if comment.user_id else False
    if user:
        classes[-1] = "byuser"
        classes[-1] = "comment-author-" + sanitize_html_class(user.user_nicename, comment.user_id)
        #// For comment authors who are the author of the post.
        post = get_post(post_id)
        if post:
            if comment.user_id == post.post_author:
                classes[-1] = "bypostauthor"
            # end if
        # end if
    # end if
    if php_empty(lambda : comment_alt):
        comment_alt = 0
    # end if
    if php_empty(lambda : comment_depth):
        comment_depth = 1
    # end if
    if php_empty(lambda : comment_thread_alt):
        comment_thread_alt = 0
    # end if
    if comment_alt % 2:
        classes[-1] = "odd"
        classes[-1] = "alt"
    else:
        classes[-1] = "even"
    # end if
    comment_alt += 1
    #// Alt for top-level comments.
    if 1 == comment_depth:
        if comment_thread_alt % 2:
            classes[-1] = "thread-odd"
            classes[-1] = "thread-alt"
        else:
            classes[-1] = "thread-even"
        # end if
        comment_thread_alt += 1
    # end if
    classes[-1] = str("depth-") + str(comment_depth)
    if (not php_empty(lambda : class_)):
        if (not php_is_array(class_)):
            class_ = php_preg_split("#\\s+#", class_)
        # end if
        classes = php_array_merge(classes, class_)
    # end if
    classes = php_array_map("esc_attr", classes)
    #// 
    #// Filters the returned CSS classes for the current comment.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string[]    $classes    An array of comment classes.
    #// @param string      $class      A comma-separated list of additional classes added to the list.
    #// @param int         $comment_id The comment id.
    #// @param WP_Comment  $comment    The comment object.
    #// @param int|WP_Post $post_id    The post ID or WP_Post object.
    #//
    return apply_filters("comment_class", classes, class_, comment.comment_ID, comment, post_id)
# end def get_comment_class
#// 
#// Retrieves the comment date of the current comment.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param string          $format     Optional. The format of the date. Default user's setting.
#// @param int|WP_Comment  $comment_ID WP_Comment or ID of the comment for which to get the date.
#// Default current comment.
#// @return string The comment's date.
#//
def get_comment_date(format="", comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    if "" == format:
        date = mysql2date(get_option("date_format"), comment.comment_date)
    else:
        date = mysql2date(format, comment.comment_date)
    # end if
    #// 
    #// Filters the returned comment date.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string|int $date    Formatted date string or Unix timestamp.
    #// @param string     $format  The format of the date.
    #// @param WP_Comment $comment The comment object.
    #//
    return apply_filters("get_comment_date", date, format, comment)
# end def get_comment_date
#// 
#// Displays the comment date of the current comment.
#// 
#// @since 0.71
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param string         $format     Optional. The format of the date. Default user's settings.
#// @param int|WP_Comment $comment_ID WP_Comment or ID of the comment for which to print the date.
#// Default current comment.
#//
def comment_date(format="", comment_ID=0, *args_):
    
    php_print(get_comment_date(format, comment_ID))
# end def comment_date
#// 
#// Retrieves the excerpt of the given comment.
#// 
#// Returns a maximum of 20 words with an ellipsis appended if necessary.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID  WP_Comment or ID of the comment for which to get the excerpt.
#// Default current comment.
#// @return string The possibly truncated comment excerpt.
#//
def get_comment_excerpt(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    comment_text = strip_tags(php_str_replace(Array("\n", "\r"), " ", comment.comment_content))
    #// translators: Maximum number of words used in a comment excerpt.
    comment_excerpt_length = php_intval(_x("20", "comment_excerpt_length"))
    #// 
    #// Filters the maximum number of words used in the comment excerpt.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int $comment_excerpt_length The amount of words you want to display in the comment excerpt.
    #//
    comment_excerpt_length = apply_filters("comment_excerpt_length", comment_excerpt_length)
    excerpt = wp_trim_words(comment_text, comment_excerpt_length, "&hellip;")
    #// 
    #// Filters the retrieved comment excerpt.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$comment_ID` and `$comment` parameters were added.
    #// 
    #// @param string     $excerpt    The comment excerpt text.
    #// @param int        $comment_ID The comment ID.
    #// @param WP_Comment $comment    The comment object.
    #//
    return apply_filters("get_comment_excerpt", excerpt, comment.comment_ID, comment)
# end def get_comment_excerpt
#// 
#// Displays the excerpt of the current comment.
#// 
#// @since 1.2.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID  WP_Comment or ID of the comment for which to print the excerpt.
#// Default current comment.
#//
def comment_excerpt(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    comment_excerpt = get_comment_excerpt(comment)
    #// 
    #// Filters the comment excerpt for display.
    #// 
    #// @since 1.2.0
    #// @since 4.1.0 The `$comment_ID` parameter was added.
    #// 
    #// @param string $comment_excerpt The comment excerpt text.
    #// @param int    $comment_ID      The comment ID.
    #//
    php_print(apply_filters("comment_excerpt", comment_excerpt, comment.comment_ID))
# end def comment_excerpt
#// 
#// Retrieves the comment id of the current comment.
#// 
#// @since 1.5.0
#// 
#// @return int The comment ID.
#//
def get_comment_ID(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    comment = get_comment()
    #// 
    #// Filters the returned comment ID.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$comment_ID` parameter was added.
    #// 
    #// @param int        $comment_ID The current comment ID.
    #// @param WP_Comment $comment    The comment object.
    #//
    return apply_filters("get_comment_ID", comment.comment_ID, comment)
    pass
# end def get_comment_ID
#// 
#// Displays the comment id of the current comment.
#// 
#// @since 0.71
#//
def comment_ID(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    php_print(get_comment_ID())
# end def comment_ID
#// 
#// Retrieves the link to a given comment.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment` to also accept a WP_Comment object. Added `$cpage` argument.
#// 
#// @see get_page_of_comment()
#// 
#// @global WP_Rewrite $wp_rewrite      WordPress rewrite component.
#// @global bool       $in_comment_loop
#// 
#// @param WP_Comment|int|null $comment Comment to retrieve. Default current comment.
#// @param array               $args {
#// An array of optional arguments to override the defaults.
#// 
#// @type string     $type      Passed to get_page_of_comment().
#// @type int        $page      Current page of comments, for calculating comment pagination.
#// @type int        $per_page  Per-page value for comment pagination.
#// @type int        $max_depth Passed to get_page_of_comment().
#// @type int|string $cpage     Value to use for the comment's "comment-page" or "cpage" value.
#// If provided, this value overrides any value calculated from `$page`
#// and `$per_page`.
#// }
#// @return string The permalink to the given comment.
#//
def get_comment_link(comment=None, args=Array(), *args_):
    
    global wp_rewrite,in_comment_loop
    php_check_if_defined("wp_rewrite","in_comment_loop")
    comment = get_comment(comment)
    #// Back-compat.
    if (not php_is_array(args)):
        args = Array({"page": args})
    # end if
    defaults = Array({"type": "all", "page": "", "per_page": "", "max_depth": "", "cpage": None})
    args = wp_parse_args(args, defaults)
    link = get_permalink(comment.comment_post_ID)
    #// The 'cpage' param takes precedence.
    if (not php_is_null(args["cpage"])):
        cpage = args["cpage"]
        pass
    else:
        if "" == args["per_page"] and get_option("page_comments"):
            args["per_page"] = get_option("comments_per_page")
        # end if
        if php_empty(lambda : args["per_page"]):
            args["per_page"] = 0
            args["page"] = 0
        # end if
        cpage = args["page"]
        if "" == cpage:
            if (not php_empty(lambda : in_comment_loop)):
                cpage = get_query_var("cpage")
            else:
                #// Requires a database hit, so we only do it when we can't figure out from context.
                cpage = get_page_of_comment(comment.comment_ID, args)
            # end if
        # end if
        #// 
        #// If the default page displays the oldest comments, the permalinks for comments on the default page
        #// do not need a 'cpage' query var.
        #//
        if "oldest" == get_option("default_comments_page") and 1 == cpage:
            cpage = ""
        # end if
    # end if
    if cpage and get_option("page_comments"):
        if wp_rewrite.using_permalinks():
            if cpage:
                link = trailingslashit(link) + wp_rewrite.comments_pagination_base + "-" + cpage
            # end if
            link = user_trailingslashit(link, "comment")
        elif cpage:
            link = add_query_arg("cpage", cpage, link)
        # end if
    # end if
    if wp_rewrite.using_permalinks():
        link = user_trailingslashit(link, "comment")
    # end if
    link = link + "#comment-" + comment.comment_ID
    #// 
    #// Filters the returned single comment permalink.
    #// 
    #// @since 2.8.0
    #// @since 4.4.0 Added the `$cpage` parameter.
    #// 
    #// @see get_page_of_comment()
    #// 
    #// @param string     $link    The comment permalink with '#comment-$id' appended.
    #// @param WP_Comment $comment The current comment object.
    #// @param array      $args    An array of arguments to override the defaults.
    #// @param int        $cpage   The calculated 'cpage' value.
    #//
    return apply_filters("get_comment_link", link, comment, args, cpage)
# end def get_comment_link
#// 
#// Retrieves the link to the current post comments.
#// 
#// @since 1.5.0
#// 
#// @param int|WP_Post $post_id Optional. Post ID or WP_Post object. Default is global $post.
#// @return string The link to the comments.
#//
def get_comments_link(post_id=0, *args_):
    
    hash = "#comments" if get_comments_number(post_id) else "#respond"
    comments_link = get_permalink(post_id) + hash
    #// 
    #// Filters the returned post comments permalink.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string      $comments_link Post comments permalink with '#comments' appended.
    #// @param int|WP_Post $post_id       Post ID or WP_Post object.
    #//
    return apply_filters("get_comments_link", comments_link, post_id)
# end def get_comments_link
#// 
#// Displays the link to the current post comments.
#// 
#// @since 0.71
#// 
#// @param string $deprecated   Not Used.
#// @param string $deprecated_2 Not Used.
#//
def comments_link(deprecated="", deprecated_2="", *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "0.72")
    # end if
    if (not php_empty(lambda : deprecated_2)):
        _deprecated_argument(__FUNCTION__, "1.3.0")
    # end if
    php_print(esc_url(get_comments_link()))
# end def comments_link
#// 
#// Retrieves the amount of comments a post has.
#// 
#// @since 1.5.0
#// 
#// @param int|WP_Post $post_id Optional. Post ID or WP_Post object. Default is the global `$post`.
#// @return string|int If the post exists, a numeric string representing the number of comments
#// the post has, otherwise 0.
#//
def get_comments_number(post_id=0, *args_):
    
    post = get_post(post_id)
    if (not post):
        count = 0
    else:
        count = post.comment_count
        post_id = post.ID
    # end if
    #// 
    #// Filters the returned comment count for a post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string|int $count   A string representing the number of comments a post has, otherwise 0.
    #// @param int        $post_id Post ID.
    #//
    return apply_filters("get_comments_number", count, post_id)
# end def get_comments_number
#// 
#// Displays the language string for the number of comments the current post has.
#// 
#// @since 0.71
#// @since 5.4.0 The `$deprecated` parameter was changed to `$post_id`.
#// 
#// @param string      $zero       Optional. Text for no comments. Default false.
#// @param string      $one        Optional. Text for one comment. Default false.
#// @param string      $more       Optional. Text for more than one comment. Default false.
#// @param int|WP_Post $post_id    Optional. Post ID or WP_Post object. Default is the global `$post`.
#//
def comments_number(zero=False, one=False, more=False, post_id=0, *args_):
    
    php_print(get_comments_number_text(zero, one, more, post_id))
# end def comments_number
#// 
#// Displays the language string for the number of comments the current post has.
#// 
#// @since 4.0.0
#// @since 5.4.0 Added the `$post_id` parameter to allow using the function outside of the loop.
#// 
#// @param string      $zero    Optional. Text for no comments. Default false.
#// @param string      $one     Optional. Text for one comment. Default false.
#// @param string      $more    Optional. Text for more than one comment. Default false.
#// @param int|WP_Post $post_id Optional. Post ID or WP_Post object. Default is the global `$post`.
#// @return string Language string for the number of comments a post has.
#//
def get_comments_number_text(zero=False, one=False, more=False, post_id=0, *args_):
    
    number = get_comments_number(post_id)
    if number > 1:
        if False == more:
            #// translators: %s: Number of comments.
            output = php_sprintf(_n("%s Comment", "%s Comments", number), number_format_i18n(number))
        else:
            #// % Comments
            #// 
            #// translators: If comment number in your language requires declension,
            #// translate this to 'on'. Do not translate into your own language.
            #//
            if "on" == _x("off", "Comment number declension: on or off"):
                text = php_preg_replace("#<span class=\"screen-reader-text\">.+?</span>#", "", more)
                text = php_preg_replace("/&.+?;/", "", text)
                #// Kill entities.
                text = php_trim(strip_tags(text), "% ")
                #// Replace '% Comments' with a proper plural form.
                if text and (not php_preg_match("/[0-9]+/", text)) and False != php_strpos(more, "%"):
                    #// translators: %s: Number of comments.
                    new_text = _n("%s Comment", "%s Comments", number)
                    new_text = php_trim(php_sprintf(new_text, ""))
                    more = php_str_replace(text, new_text, more)
                    if False == php_strpos(more, "%"):
                        more = "% " + more
                    # end if
                # end if
            # end if
            output = php_str_replace("%", number_format_i18n(number), more)
        # end if
    elif 0 == number:
        output = __("No Comments") if False == zero else zero
    else:
        #// Must be one.
        output = __("1 Comment") if False == one else one
    # end if
    #// 
    #// Filters the comments count for display.
    #// 
    #// @since 1.5.0
    #// 
    #// @see _n()
    #// 
    #// @param string $output A translatable string formatted based on whether the count
    #// is equal to 0, 1, or 1+.
    #// @param int    $number The number of post comments.
    #//
    return apply_filters("comments_number", output, number)
# end def get_comments_number_text
#// 
#// Retrieves the text of the current comment.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// @since 5.4.0 Added 'In reply to %s.' prefix to child comments in comments feed.
#// 
#// @see Walker_Comment::comment()
#// 
#// @param int|WP_Comment  $comment_ID WP_Comment or ID of the comment for which to get the text.
#// Default current comment.
#// @param array           $args       Optional. An array of arguments. Default empty array.
#// @return string The comment content.
#//
def get_comment_text(comment_ID=0, args=Array(), *args_):
    
    comment = get_comment(comment_ID)
    comment_content = comment.comment_content
    if is_comment_feed() and comment.comment_parent:
        parent = get_comment(comment.comment_parent)
        if parent:
            parent_link = esc_url(get_comment_link(parent))
            name = get_comment_author(parent)
            comment_content = php_sprintf(ent2ncr(__("In reply to %s.")), "<a href=\"" + parent_link + "\">" + name + "</a>") + "\n\n" + comment_content
        # end if
    # end if
    #// 
    #// Filters the text of a comment.
    #// 
    #// @since 1.5.0
    #// 
    #// @see Walker_Comment::comment()
    #// 
    #// @param string     $comment_content Text of the comment.
    #// @param WP_Comment $comment         The comment object.
    #// @param array      $args            An array of arguments.
    #//
    return apply_filters("get_comment_text", comment_content, comment, args)
# end def get_comment_text
#// 
#// Displays the text of the current comment.
#// 
#// @since 0.71
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @see Walker_Comment::comment()
#// 
#// @param int|WP_Comment  $comment_ID WP_Comment or ID of the comment for which to print the text.
#// Default current comment.
#// @param array           $args       Optional. An array of arguments. Default empty array.
#//
def comment_text(comment_ID=0, args=Array(), *args_):
    
    comment = get_comment(comment_ID)
    comment_text = get_comment_text(comment, args)
    #// 
    #// Filters the text of a comment to be displayed.
    #// 
    #// @since 1.2.0
    #// 
    #// @see Walker_Comment::comment()
    #// 
    #// @param string          $comment_text Text of the current comment.
    #// @param WP_Comment|null $comment      The comment object.
    #// @param array           $args         An array of arguments.
    #//
    php_print(apply_filters("comment_text", comment_text, comment, args))
# end def comment_text
#// 
#// Retrieves the comment time of the current comment.
#// 
#// @since 1.5.0
#// 
#// @param string $format    Optional. The format of the time. Default user's settings.
#// @param bool   $gmt       Optional. Whether to use the GMT date. Default false.
#// @param bool   $translate Optional. Whether to translate the time (for use in feeds).
#// Default true.
#// @return string The formatted time.
#//
def get_comment_time(format="", gmt=False, translate=True, *args_):
    
    comment = get_comment()
    comment_date = comment.comment_date_gmt if gmt else comment.comment_date
    if "" == format:
        date = mysql2date(get_option("time_format"), comment_date, translate)
    else:
        date = mysql2date(format, comment_date, translate)
    # end if
    #// 
    #// Filters the returned comment time.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string|int $date      The comment time, formatted as a date string or Unix timestamp.
    #// @param string     $format    Date format.
    #// @param bool       $gmt       Whether the GMT date is in use.
    #// @param bool       $translate Whether the time is translated.
    #// @param WP_Comment $comment   The comment object.
    #//
    return apply_filters("get_comment_time", date, format, gmt, translate, comment)
# end def get_comment_time
#// 
#// Displays the comment time of the current comment.
#// 
#// @since 0.71
#// 
#// @param string $format Optional. The format of the time. Default user's settings.
#//
def comment_time(format="", *args_):
    
    php_print(get_comment_time(format))
# end def comment_time
#// 
#// Retrieves the comment type of the current comment.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability for `$comment_ID` to also accept a WP_Comment object.
#// 
#// @param int|WP_Comment $comment_ID Optional. WP_Comment or ID of the comment for which to get the type.
#// Default current comment.
#// @return string The comment type.
#//
def get_comment_type(comment_ID=0, *args_):
    
    comment = get_comment(comment_ID)
    if "" == comment.comment_type:
        comment.comment_type = "comment"
    # end if
    #// 
    #// Filters the returned comment type.
    #// 
    #// @since 1.5.0
    #// @since 4.1.0 The `$comment_ID` and `$comment` parameters were added.
    #// 
    #// @param string     $comment_type The type of comment, such as 'comment', 'pingback', or 'trackback'.
    #// @param int        $comment_ID   The comment ID.
    #// @param WP_Comment $comment      The comment object.
    #//
    return apply_filters("get_comment_type", comment.comment_type, comment.comment_ID, comment)
# end def get_comment_type
#// 
#// Displays the comment type of the current comment.
#// 
#// @since 0.71
#// 
#// @param string $commenttxt   Optional. String to display for comment type. Default false.
#// @param string $trackbacktxt Optional. String to display for trackback type. Default false.
#// @param string $pingbacktxt  Optional. String to display for pingback type. Default false.
#//
def comment_type(commenttxt=False, trackbacktxt=False, pingbacktxt=False, *args_):
    
    if False == commenttxt:
        commenttxt = _x("Comment", "noun")
    # end if
    if False == trackbacktxt:
        trackbacktxt = __("Trackback")
    # end if
    if False == pingbacktxt:
        pingbacktxt = __("Pingback")
    # end if
    type = get_comment_type()
    for case in Switch(type):
        if case("trackback"):
            php_print(trackbacktxt)
            break
        # end if
        if case("pingback"):
            php_print(pingbacktxt)
            break
        # end if
        if case():
            php_print(commenttxt)
        # end if
    # end for
# end def comment_type
#// 
#// Retrieves the current post's trackback URL.
#// 
#// There is a check to see if permalink's have been enabled and if so, will
#// retrieve the pretty path. If permalinks weren't enabled, the ID of the
#// current post is used and appended to the correct page to go to.
#// 
#// @since 1.5.0
#// 
#// @return string The trackback URL after being filtered.
#//
def get_trackback_url(*args_):
    
    if "" != get_option("permalink_structure"):
        tb_url = trailingslashit(get_permalink()) + user_trailingslashit("trackback", "single_trackback")
    else:
        tb_url = get_option("siteurl") + "/wp-trackback.php?p=" + get_the_ID()
    # end if
    #// 
    #// Filters the returned trackback URL.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $tb_url The trackback URL.
    #//
    return apply_filters("trackback_url", tb_url)
# end def get_trackback_url
#// 
#// Displays the current post's trackback URL.
#// 
#// @since 0.71
#// 
#// @param bool $deprecated_echo Not used.
#// @return void|string Should only be used to echo the trackback URL, use get_trackback_url()
#// for the result instead.
#//
def trackback_url(deprecated_echo=True, *args_):
    
    if True != deprecated_echo:
        _deprecated_argument(__FUNCTION__, "2.5.0", php_sprintf(__("Use %s instead if you do not want the value echoed."), "<code>get_trackback_url()</code>"))
    # end if
    if deprecated_echo:
        php_print(get_trackback_url())
    else:
        return get_trackback_url()
    # end if
# end def trackback_url
#// 
#// Generates and displays the RDF for the trackback information of current post.
#// 
#// Deprecated in 3.0.0, and restored in 3.0.1.
#// 
#// @since 0.71
#// 
#// @param int $deprecated Not used (Was $timezone = 0).
#//
def trackback_rdf(deprecated="", *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.5.0")
    # end if
    if (php_isset(lambda : PHP_SERVER["HTTP_USER_AGENT"])) and False != php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "W3C_Validator"):
        return
    # end if
    php_print("""<rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"
    xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
    xmlns:trackback=\"http://madskills.com/public/xml/rss/module/trackback/\">
    <rdf:Description rdf:about=\"""")
    the_permalink()
    php_print("\"" + "\n")
    php_print("    dc:identifier=\"")
    the_permalink()
    php_print("\"" + "\n")
    php_print("    dc:title=\"" + php_str_replace("--", "&#x2d;&#x2d;", wptexturize(strip_tags(get_the_title()))) + "\"" + "\n")
    php_print("    trackback:ping=\"" + get_trackback_url() + "\"" + " />\n")
    php_print("</rdf:RDF>")
# end def trackback_rdf
#// 
#// Determines whether the current post is open for comments.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @param int|WP_Post $post_id Post ID or WP_Post object. Default current post.
#// @return bool True if the comments are open.
#//
def comments_open(post_id=None, *args_):
    
    _post = get_post(post_id)
    post_id = _post.ID if _post else 0
    open_ = "open" == _post.comment_status
    #// 
    #// Filters whether the current post is open for comments.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool $open    Whether the current post is open for comments.
    #// @param int  $post_id The post ID.
    #//
    return apply_filters("comments_open", open_, post_id)
# end def comments_open
#// 
#// Determines whether the current post is open for pings.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @param int|WP_Post $post_id Post ID or WP_Post object. Default current post.
#// @return bool True if pings are accepted
#//
def pings_open(post_id=None, *args_):
    
    _post = get_post(post_id)
    post_id = _post.ID if _post else 0
    open_ = "open" == _post.ping_status
    #// 
    #// Filters whether the current post is open for pings.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool $open    Whether the current post is open for pings.
    #// @param int  $post_id The post ID.
    #//
    return apply_filters("pings_open", open_, post_id)
# end def pings_open
#// 
#// Displays form token for unfiltered comments.
#// 
#// Will only display nonce token if the current user has permissions for
#// unfiltered html. Won't display the token for other users.
#// 
#// The function was backported to 2.0.10 and was added to versions 2.1.3 and
#// above. Does not exist in versions prior to 2.0.10 in the 2.0 branch and in
#// the 2.1 branch, prior to 2.1.3. Technically added in 2.2.0.
#// 
#// Backported to 2.0.10.
#// 
#// @since 2.1.3
#//
def wp_comment_form_unfiltered_html_nonce(*args_):
    
    post = get_post()
    post_id = post.ID if post else 0
    if current_user_can("unfiltered_html"):
        wp_nonce_field("unfiltered-html-comment_" + post_id, "_wp_unfiltered_html_comment_disabled", False)
        php_print("<script>(function(){if(window===window.parent){document.getElementById('_wp_unfiltered_html_comment_disabled').name='_wp_unfiltered_html_comment';}})();</script>\n")
    # end if
# end def wp_comment_form_unfiltered_html_nonce
#// 
#// Loads the comment template specified in $file.
#// 
#// Will not display the comments template if not on single post or page, or if
#// the post does not have comments.
#// 
#// Uses the WordPress database object to query for the comments. The comments
#// are passed through the {@see 'comments_array'} filter hook with the list of comments
#// and the post ID respectively.
#// 
#// The `$file` path is passed through a filter hook called {@see 'comments_template'},
#// which includes the TEMPLATEPATH and $file combined. Tries the $filtered path
#// first and if it fails it will require the default comment template from the
#// default theme. If either does not exist, then the WordPress process will be
#// halted. It is advised for that reason, that the default theme is not deleted.
#// 
#// Will not try to get the comments if the post has none.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query   $wp_query         WordPress Query object.
#// @global WP_Post    $post             Global post object.
#// @global wpdb       $wpdb             WordPress database abstraction object.
#// @global int        $id
#// @global WP_Comment $comment          Global comment object.
#// @global string     $user_login
#// @global int        $user_ID
#// @global string     $user_identity
#// @global bool       $overridden_cpage
#// @global bool       $withcomments
#// 
#// @param string $file              Optional. The file to load. Default '/comments.php'.
#// @param bool   $separate_comments Optional. Whether to separate the comments by comment type.
#// Default false.
#//
def comments_template(file="/comments.php", separate_comments=False, *args_):
    
    global wp_query,withcomments,post,wpdb,id,comment,user_login,user_ID,user_identity,overridden_cpage
    php_check_if_defined("wp_query","withcomments","post","wpdb","id","comment","user_login","user_ID","user_identity","overridden_cpage")
    if (not is_single() or is_page() or withcomments) or php_empty(lambda : post):
        return
    # end if
    if php_empty(lambda : file):
        file = "/comments.php"
    # end if
    req = get_option("require_name_email")
    #// 
    #// Comment author information fetched from the comment cookies.
    #//
    commenter = wp_get_current_commenter()
    #// 
    #// The name of the current comment author escaped for use in attributes.
    #// Escaped by sanitize_comment_cookies().
    #//
    comment_author = commenter["comment_author"]
    #// 
    #// The email address of the current comment author escaped for use in attributes.
    #// Escaped by sanitize_comment_cookies().
    #//
    comment_author_email = commenter["comment_author_email"]
    #// 
    #// The URL of the current comment author escaped for use in attributes.
    #//
    comment_author_url = esc_url(commenter["comment_author_url"])
    comment_args = Array({"orderby": "comment_date_gmt", "order": "ASC", "status": "approve", "post_id": post.ID, "no_found_rows": False, "update_comment_meta_cache": False})
    if get_option("thread_comments"):
        comment_args["hierarchical"] = "threaded"
    else:
        comment_args["hierarchical"] = False
    # end if
    if user_ID:
        comment_args["include_unapproved"] = Array(user_ID)
    else:
        unapproved_email = wp_get_unapproved_comment_author_email()
        if unapproved_email:
            comment_args["include_unapproved"] = Array(unapproved_email)
        # end if
    # end if
    per_page = 0
    if get_option("page_comments"):
        per_page = int(get_query_var("comments_per_page"))
        if 0 == per_page:
            per_page = int(get_option("comments_per_page"))
        # end if
        comment_args["number"] = per_page
        page = int(get_query_var("cpage"))
        if page:
            comment_args["offset"] = page - 1 * per_page
        elif "oldest" == get_option("default_comments_page"):
            comment_args["offset"] = 0
        else:
            #// If fetching the first page of 'newest', we need a top-level comment count.
            top_level_query = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
            top_level_args = Array({"count": True, "orderby": False, "post_id": post.ID, "status": "approve"})
            if comment_args["hierarchical"]:
                top_level_args["parent"] = 0
            # end if
            if (php_isset(lambda : comment_args["include_unapproved"])):
                top_level_args["include_unapproved"] = comment_args["include_unapproved"]
            # end if
            top_level_count = top_level_query.query(top_level_args)
            comment_args["offset"] = ceil(top_level_count / per_page) - 1 * per_page
        # end if
    # end if
    #// 
    #// Filters the arguments used to query comments in comments_template().
    #// 
    #// @since 4.5.0
    #// 
    #// @see WP_Comment_Query::__construct()
    #// 
    #// @param array $comment_args {
    #// Array of WP_Comment_Query arguments.
    #// 
    #// @type string|array $orderby                   Field(s) to order by.
    #// @type string       $order                     Order of results. Accepts 'ASC' or 'DESC'.
    #// @type string       $status                    Comment status.
    #// @type array        $include_unapproved        Array of IDs or email addresses whose unapproved comments
    #// will be included in results.
    #// @type int          $post_id                   ID of the post.
    #// @type bool         $no_found_rows             Whether to refrain from querying for found rows.
    #// @type bool         $update_comment_meta_cache Whether to prime cache for comment meta.
    #// @type bool|string  $hierarchical              Whether to query for comments hierarchically.
    #// @type int          $offset                    Comment offset.
    #// @type int          $number                    Number of comments to fetch.
    #// }
    #//
    comment_args = apply_filters("comments_template_query_args", comment_args)
    comment_query = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query(comment_args))
    _comments = comment_query.comments
    #// Trees must be flattened before they're passed to the walker.
    if comment_args["hierarchical"]:
        comments_flat = Array()
        for _comment in _comments:
            comments_flat[-1] = _comment
            comment_children = _comment.get_children(Array({"format": "flat", "status": comment_args["status"], "orderby": comment_args["orderby"]}))
            for comment_child in comment_children:
                comments_flat[-1] = comment_child
            # end for
        # end for
    else:
        comments_flat = _comments
    # end if
    #// 
    #// Filters the comments array.
    #// 
    #// @since 2.1.0
    #// 
    #// @param array $comments Array of comments supplied to the comments template.
    #// @param int   $post_ID  Post ID.
    #//
    wp_query.comments = apply_filters("comments_array", comments_flat, post.ID)
    comments = wp_query.comments
    wp_query.comment_count = php_count(wp_query.comments)
    wp_query.max_num_comment_pages = comment_query.max_num_pages
    if separate_comments:
        wp_query.comments_by_type = separate_comments(comments)
        comments_by_type = wp_query.comments_by_type
    else:
        wp_query.comments_by_type = Array()
    # end if
    overridden_cpage = False
    if "" == get_query_var("cpage") and wp_query.max_num_comment_pages > 1:
        set_query_var("cpage", get_comment_pages_count() if "newest" == get_option("default_comments_page") else 1)
        overridden_cpage = True
    # end if
    if (not php_defined("COMMENTS_TEMPLATE")):
        php_define("COMMENTS_TEMPLATE", True)
    # end if
    theme_template = STYLESHEETPATH + file
    #// 
    #// Filters the path to the theme template file used for the comments template.
    #// 
    #// @since 1.5.1
    #// 
    #// @param string $theme_template The path to the theme template file.
    #//
    include = apply_filters("comments_template", theme_template)
    if php_file_exists(include):
        php_include_file(include, once=False)
    elif php_file_exists(TEMPLATEPATH + file):
        php_include_file(TEMPLATEPATH + file, once=False)
    else:
        #// Backward compat code will be removed in a future release.
        php_include_file(ABSPATH + WPINC + "/theme-compat/comments.php", once=False)
    # end if
# end def comments_template
#// 
#// Displays the link to the comments for the current post ID.
#// 
#// @since 0.71
#// 
#// @param false|string $zero      Optional. String to display when no comments. Default false.
#// @param false|string $one       Optional. String to display when only one comment is available. Default false.
#// @param false|string $more      Optional. String to display when there are more than one comment. Default false.
#// @param string       $css_class Optional. CSS class to use for comments. Default empty.
#// @param false|string $none      Optional. String to display when comments have been turned off. Default false.
#//
def comments_popup_link(zero=False, one=False, more=False, css_class="", none=False, *args_):
    
    id = get_the_ID()
    title = get_the_title()
    number = get_comments_number(id)
    if False == zero:
        #// translators: %s: Post title.
        zero = php_sprintf(__("No Comments<span class=\"screen-reader-text\"> on %s</span>"), title)
    # end if
    if False == one:
        #// translators: %s: Post title.
        one = php_sprintf(__("1 Comment<span class=\"screen-reader-text\"> on %s</span>"), title)
    # end if
    if False == more:
        #// translators: 1: Number of comments, 2: Post title.
        more = _n("%1$s Comment<span class=\"screen-reader-text\"> on %2$s</span>", "%1$s Comments<span class=\"screen-reader-text\"> on %2$s</span>", number)
        more = php_sprintf(more, number_format_i18n(number), title)
    # end if
    if False == none:
        #// translators: %s: Post title.
        none = php_sprintf(__("Comments Off<span class=\"screen-reader-text\"> on %s</span>"), title)
    # end if
    if 0 == number and (not comments_open()) and (not pings_open()):
        php_print("<span" + " class=\"" + esc_attr(css_class) + "\"" if (not php_empty(lambda : css_class)) else "" + ">" + none + "</span>")
        return
    # end if
    if post_password_required():
        _e("Enter your password to view comments.")
        return
    # end if
    php_print("<a href=\"")
    if 0 == number:
        respond_link = get_permalink() + "#respond"
        #// 
        #// Filters the respond link when a post has no comments.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $respond_link The default response link.
        #// @param integer $id The post ID.
        #//
        php_print(apply_filters("respond_link", respond_link, id))
    else:
        comments_link()
    # end if
    php_print("\"")
    if (not php_empty(lambda : css_class)):
        php_print(" class=\"" + css_class + "\" ")
    # end if
    attributes = ""
    #// 
    #// Filters the comments link attributes for display.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $attributes The comments link attributes. Default empty.
    #//
    php_print(apply_filters("comments_popup_link_attributes", attributes))
    php_print(">")
    comments_number(zero, one, more)
    php_print("</a>")
# end def comments_popup_link
#// 
#// Retrieves HTML content for reply to comment link.
#// 
#// @since 2.7.0
#// @since 4.4.0 Added the ability for `$comment` to also accept a WP_Comment object.
#// 
#// @param array $args {
#// Optional. Override default arguments.
#// 
#// @type string $add_below  The first part of the selector used to identify the comment to respond below.
#// The resulting value is passed as the first parameter to addComment.moveForm(),
#// concatenated as $add_below-$comment->comment_ID. Default 'comment'.
#// @type string $respond_id The selector identifying the responding comment. Passed as the third parameter
#// to addComment.moveForm(), and appended to the link URL as a hash value.
#// Default 'respond'.
#// @type string $reply_text The text of the Reply link. Default 'Reply'.
#// @type string $login_text The text of the link to reply if logged out. Default 'Log in to Reply'.
#// @type int    $max_depth  The max depth of the comment tree. Default 0.
#// @type int    $depth      The depth of the new comment. Must be greater than 0 and less than the value
#// of the 'thread_comments_depth' option set in Settings > Discussion. Default 0.
#// @type string $before     The text or HTML to add before the reply link. Default empty.
#// @type string $after      The text or HTML to add after the reply link. Default empty.
#// }
#// @param int|WP_Comment $comment Comment being replied to. Default current comment.
#// @param int|WP_Post    $post    Post ID or WP_Post object the comment is going to be displayed on.
#// Default current post.
#// @return string|false|null Link to show comment form, if successful. False, if comments are closed.
#//
def get_comment_reply_link(args=Array(), comment=None, post=None, *args_):
    
    defaults = Array({"add_below": "comment", "respond_id": "respond", "reply_text": __("Reply"), "reply_to_text": __("Reply to %s"), "login_text": __("Log in to Reply"), "max_depth": 0, "depth": 0, "before": "", "after": ""})
    args = wp_parse_args(args, defaults)
    if 0 == args["depth"] or args["max_depth"] <= args["depth"]:
        return
    # end if
    comment = get_comment(comment)
    if php_empty(lambda : comment):
        return
    # end if
    if php_empty(lambda : post):
        post = comment.comment_post_ID
    # end if
    post = get_post(post)
    if (not comments_open(post.ID)):
        return False
    # end if
    #// 
    #// Filters the comment reply link arguments.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array      $args    Comment reply link arguments. See get_comment_reply_link()
    #// for more information on accepted arguments.
    #// @param WP_Comment $comment The object of the comment being replied to.
    #// @param WP_Post    $post    The WP_Post object.
    #//
    args = apply_filters("comment_reply_link_args", args, comment, post)
    if get_option("comment_registration") and (not is_user_logged_in()):
        link = php_sprintf("<a rel=\"nofollow\" class=\"comment-reply-login\" href=\"%s\">%s</a>", esc_url(wp_login_url(get_permalink())), args["login_text"])
    else:
        data_attributes = Array({"commentid": comment.comment_ID, "postid": post.ID, "belowelement": args["add_below"] + "-" + comment.comment_ID, "respondelement": args["respond_id"]})
        data_attribute_string = ""
        for name,value in data_attributes:
            data_attribute_string += str(" data-") + str(name) + str("=\"") + esc_attr(value) + "\""
        # end for
        data_attribute_string = php_trim(data_attribute_string)
        link = php_sprintf("<a rel='nofollow' class='comment-reply-link' href='%s' %s aria-label='%s'>%s</a>", esc_url(add_query_arg(Array({"replytocom": comment.comment_ID, "unapproved": False, "moderation-hash": False}), get_permalink(post.ID))) + "#" + args["respond_id"], data_attribute_string, esc_attr(php_sprintf(args["reply_to_text"], comment.comment_author)), args["reply_text"])
    # end if
    #// 
    #// Filters the comment reply link.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string     $link    The HTML markup for the comment reply link.
    #// @param array      $args    An array of arguments overriding the defaults.
    #// @param WP_Comment $comment The object of the comment being replied.
    #// @param WP_Post    $post    The WP_Post object.
    #//
    return apply_filters("comment_reply_link", args["before"] + link + args["after"], args, comment, post)
# end def get_comment_reply_link
#// 
#// Displays the HTML content for reply to comment link.
#// 
#// @since 2.7.0
#// 
#// @see get_comment_reply_link()
#// 
#// @param array          $args    Optional. Override default options. Default empty array.
#// @param int|WP_Comment $comment Comment being replied to. Default current comment.
#// @param int|WP_Post    $post    Post ID or WP_Post object the comment is going to be displayed on.
#// Default current post.
#//
def comment_reply_link(args=Array(), comment=None, post=None, *args_):
    
    php_print(get_comment_reply_link(args, comment, post))
# end def comment_reply_link
#// 
#// Retrieves HTML content for reply to post link.
#// 
#// @since 2.7.0
#// 
#// @param array $args {
#// Optional. Override default arguments.
#// 
#// @type string $add_below  The first part of the selector used to identify the comment to respond below.
#// The resulting value is passed as the first parameter to addComment.moveForm(),
#// concatenated as $add_below-$comment->comment_ID. Default is 'post'.
#// @type string $respond_id The selector identifying the responding comment. Passed as the third parameter
#// to addComment.moveForm(), and appended to the link URL as a hash value.
#// Default 'respond'.
#// @type string $reply_text Text of the Reply link. Default is 'Leave a Comment'.
#// @type string $login_text Text of the link to reply if logged out. Default is 'Log in to leave a Comment'.
#// @type string $before     Text or HTML to add before the reply link. Default empty.
#// @type string $after      Text or HTML to add after the reply link. Default empty.
#// }
#// @param int|WP_Post $post    Optional. Post ID or WP_Post object the comment is going to be displayed on.
#// Default current post.
#// @return string|false|null Link to show comment form, if successful. False, if comments are closed.
#//
def get_post_reply_link(args=Array(), post=None, *args_):
    
    defaults = Array({"add_below": "post", "respond_id": "respond", "reply_text": __("Leave a Comment"), "login_text": __("Log in to leave a Comment"), "before": "", "after": ""})
    args = wp_parse_args(args, defaults)
    post = get_post(post)
    if (not comments_open(post.ID)):
        return False
    # end if
    if get_option("comment_registration") and (not is_user_logged_in()):
        link = php_sprintf("<a rel=\"nofollow\" class=\"comment-reply-login\" href=\"%s\">%s</a>", wp_login_url(get_permalink()), args["login_text"])
    else:
        onclick = php_sprintf("return addComment.moveForm( \"%1$s-%2$s\", \"0\", \"%3$s\", \"%2$s\" )", args["add_below"], post.ID, args["respond_id"])
        link = php_sprintf("<a rel='nofollow' class='comment-reply-link' href='%s' onclick='%s'>%s</a>", get_permalink(post.ID) + "#" + args["respond_id"], onclick, args["reply_text"])
    # end if
    formatted_link = args["before"] + link + args["after"]
    #// 
    #// Filters the formatted post comments link HTML.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string      $formatted The HTML-formatted post comments link.
    #// @param int|WP_Post $post      The post ID or WP_Post object.
    #//
    return apply_filters("post_comments_link", formatted_link, post)
# end def get_post_reply_link
#// 
#// Displays the HTML content for reply to post link.
#// 
#// @since 2.7.0
#// 
#// @see get_post_reply_link()
#// 
#// @param array       $args Optional. Override default options. Default empty array.
#// @param int|WP_Post $post Post ID or WP_Post object the comment is going to be displayed on.
#// Default current post.
#//
def post_reply_link(args=Array(), post=None, *args_):
    
    php_print(get_post_reply_link(args, post))
# end def post_reply_link
#// 
#// Retrieves HTML content for cancel comment reply link.
#// 
#// @since 2.7.0
#// 
#// @param string $text Optional. Text to display for cancel reply link. Default empty.
#// @return string
#//
def get_cancel_comment_reply_link(text="", *args_):
    
    if php_empty(lambda : text):
        text = __("Click here to cancel reply.")
    # end if
    style = "" if (php_isset(lambda : PHP_REQUEST["replytocom"])) else " style=\"display:none;\""
    link = esc_html(remove_query_arg(Array("replytocom", "unapproved", "moderation-hash"))) + "#respond"
    formatted_link = "<a rel=\"nofollow\" id=\"cancel-comment-reply-link\" href=\"" + link + "\"" + style + ">" + text + "</a>"
    #// 
    #// Filters the cancel comment reply link HTML.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $formatted_link The HTML-formatted cancel comment reply link.
    #// @param string $link           Cancel comment reply link URL.
    #// @param string $text           Cancel comment reply link text.
    #//
    return apply_filters("cancel_comment_reply_link", formatted_link, link, text)
# end def get_cancel_comment_reply_link
#// 
#// Displays HTML content for cancel comment reply link.
#// 
#// @since 2.7.0
#// 
#// @param string $text Optional. Text to display for cancel reply link. Default empty.
#//
def cancel_comment_reply_link(text="", *args_):
    
    php_print(get_cancel_comment_reply_link(text))
# end def cancel_comment_reply_link
#// 
#// Retrieves hidden input HTML for replying to comments.
#// 
#// @since 3.0.0
#// 
#// @param int $id Optional. Post ID. Default current post ID.
#// @return string Hidden input HTML for replying to comments
#//
def get_comment_id_fields(id=0, *args_):
    
    if php_empty(lambda : id):
        id = get_the_ID()
    # end if
    replytoid = int(PHP_REQUEST["replytocom"]) if (php_isset(lambda : PHP_REQUEST["replytocom"])) else 0
    result = str("<input type='hidden' name='comment_post_ID' value='") + str(id) + str("' id='comment_post_ID' />\n")
    result += str("<input type='hidden' name='comment_parent' id='comment_parent' value='") + str(replytoid) + str("' />\n")
    #// 
    #// Filters the returned comment id fields.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $result    The HTML-formatted hidden id field comment elements.
    #// @param int    $id        The post ID.
    #// @param int    $replytoid The id of the comment being replied to.
    #//
    return apply_filters("comment_id_fields", result, id, replytoid)
# end def get_comment_id_fields
#// 
#// Outputs hidden input HTML for replying to comments.
#// 
#// @since 2.7.0
#// 
#// @param int $id Optional. Post ID. Default current post ID.
#//
def comment_id_fields(id=0, *args_):
    
    php_print(get_comment_id_fields(id))
# end def comment_id_fields
#// 
#// Displays text based on comment reply status.
#// 
#// Only affects users with JavaScript disabled.
#// 
#// @internal The $comment global must be present to allow template tags access to the current
#// comment. See https://core.trac.wordpress.org/changeset/36512.
#// 
#// @since 2.7.0
#// 
#// @global WP_Comment $comment Global comment object.
#// 
#// @param string $noreplytext  Optional. Text to display when not replying to a comment.
#// Default false.
#// @param string $replytext    Optional. Text to display when replying to a comment.
#// Default false. Accepts "%s" for the author of the comment
#// being replied to.
#// @param string $linktoparent Optional. Boolean to control making the author's name a link
#// to their comment. Default true.
#//
def comment_form_title(noreplytext=False, replytext=False, linktoparent=True, *args_):
    
    global comment
    php_check_if_defined("comment")
    if False == noreplytext:
        noreplytext = __("Leave a Reply")
    # end if
    if False == replytext:
        #// translators: %s: Author of the comment being replied to.
        replytext = __("Leave a Reply to %s")
    # end if
    replytoid = int(PHP_REQUEST["replytocom"]) if (php_isset(lambda : PHP_REQUEST["replytocom"])) else 0
    if 0 == replytoid:
        php_print(noreplytext)
    else:
        #// Sets the global so that template tags can be used in the comment form.
        comment = get_comment(replytoid)
        author = "<a href=\"#comment-" + get_comment_ID() + "\">" + get_comment_author(comment) + "</a>" if linktoparent else get_comment_author(comment)
        printf(replytext, author)
    # end if
# end def comment_form_title
#// 
#// Displays a list of comments.
#// 
#// Used in the comments.php template to list comments for a particular post.
#// 
#// @since 2.7.0
#// 
#// @see WP_Query->comments
#// 
#// @global WP_Query $wp_query           WordPress Query object.
#// @global int      $comment_alt
#// @global int      $comment_depth
#// @global int      $comment_thread_alt
#// @global bool     $overridden_cpage
#// @global bool     $in_comment_loop
#// 
#// @param string|array $args {
#// Optional. Formatting options.
#// 
#// @type object $walker            Instance of a Walker class to list comments. Default null.
#// @type int    $max_depth         The maximum comments depth. Default empty.
#// @type string $style             The style of list ordering. Default 'ul'. Accepts 'ul', 'ol'.
#// @type string $callback          Callback function to use. Default null.
#// @type string $end-callback      Callback function to use at the end. Default null.
#// @type string $type              Type of comments to list.
#// Default 'all'. Accepts 'all', 'comment', 'pingback', 'trackback', 'pings'.
#// @type int    $page              Page ID to list comments for. Default empty.
#// @type int    $per_page          Number of comments to list per page. Default empty.
#// @type int    $avatar_size       Height and width dimensions of the avatar size. Default 32.
#// @type bool   $reverse_top_level Ordering of the listed comments. If true, will display newest comments first.
#// @type bool   $reverse_children  Whether to reverse child comments in the list. Default null.
#// @type string $format            How to format the comments list.
#// Default 'html5' if the theme supports it. Accepts 'html5', 'xhtml'.
#// @type bool   $short_ping        Whether to output short pings. Default false.
#// @type bool   $echo              Whether to echo the output or return it. Default true.
#// }
#// @param WP_Comment[] $comments Optional. Array of WP_Comment objects.
#// @return void|string Void if 'echo' argument is true, or no comments to list.
#// Otherwise, HTML list of comments.
#//
def wp_list_comments(args=Array(), comments=None, *args_):
    
    global wp_query,comment_alt,comment_depth,comment_thread_alt,overridden_cpage,in_comment_loop
    php_check_if_defined("wp_query","comment_alt","comment_depth","comment_thread_alt","overridden_cpage","in_comment_loop")
    in_comment_loop = True
    comment_alt = 0
    comment_thread_alt = 0
    comment_depth = 1
    defaults = Array({"walker": None, "max_depth": "", "style": "ul", "callback": None, "end-callback": None, "type": "all", "page": "", "per_page": "", "avatar_size": 32, "reverse_top_level": None, "reverse_children": "", "format": "html5" if current_theme_supports("html5", "comment-list") else "xhtml", "short_ping": False, "echo": True})
    parsed_args = wp_parse_args(args, defaults)
    #// 
    #// Filters the arguments used in retrieving the comment list.
    #// 
    #// @since 4.0.0
    #// 
    #// @see wp_list_comments()
    #// 
    #// @param array $parsed_args An array of arguments for displaying comments.
    #//
    parsed_args = apply_filters("wp_list_comments_args", parsed_args)
    #// Figure out what comments we'll be looping through ($_comments).
    if None != comments:
        comments = comments
        if php_empty(lambda : comments):
            return
        # end if
        if "all" != parsed_args["type"]:
            comments_by_type = separate_comments(comments)
            if php_empty(lambda : comments_by_type[parsed_args["type"]]):
                return
            # end if
            _comments = comments_by_type[parsed_args["type"]]
        else:
            _comments = comments
        # end if
    else:
        #// 
        #// If 'page' or 'per_page' has been passed, and does not match what's in $wp_query,
        #// perform a separate comment query and allow Walker_Comment to paginate.
        #//
        if parsed_args["page"] or parsed_args["per_page"]:
            current_cpage = get_query_var("cpage")
            if (not current_cpage):
                current_cpage = 1 if "newest" == get_option("default_comments_page") else wp_query.max_num_comment_pages
            # end if
            current_per_page = get_query_var("comments_per_page")
            if parsed_args["page"] != current_cpage or parsed_args["per_page"] != current_per_page:
                comment_args = Array({"post_id": get_the_ID(), "orderby": "comment_date_gmt", "order": "ASC", "status": "approve"})
                if is_user_logged_in():
                    comment_args["include_unapproved"] = get_current_user_id()
                else:
                    unapproved_email = wp_get_unapproved_comment_author_email()
                    if unapproved_email:
                        comment_args["include_unapproved"] = Array(unapproved_email)
                    # end if
                # end if
                comments = get_comments(comment_args)
                if "all" != parsed_args["type"]:
                    comments_by_type = separate_comments(comments)
                    if php_empty(lambda : comments_by_type[parsed_args["type"]]):
                        return
                    # end if
                    _comments = comments_by_type[parsed_args["type"]]
                else:
                    _comments = comments
                # end if
            # end if
            pass
        else:
            if php_empty(lambda : wp_query.comments):
                return
            # end if
            if "all" != parsed_args["type"]:
                if php_empty(lambda : wp_query.comments_by_type):
                    wp_query.comments_by_type = separate_comments(wp_query.comments)
                # end if
                if php_empty(lambda : wp_query.comments_by_type[parsed_args["type"]]):
                    return
                # end if
                _comments = wp_query.comments_by_type[parsed_args["type"]]
            else:
                _comments = wp_query.comments
            # end if
            if wp_query.max_num_comment_pages:
                default_comments_page = get_option("default_comments_page")
                cpage = get_query_var("cpage")
                if "newest" == default_comments_page:
                    parsed_args["cpage"] = cpage
                    pass
                elif 1 == cpage:
                    parsed_args["cpage"] = ""
                else:
                    parsed_args["cpage"] = cpage
                # end if
                parsed_args["page"] = 0
                parsed_args["per_page"] = 0
            # end if
        # end if
    # end if
    if "" == parsed_args["per_page"] and get_option("page_comments"):
        parsed_args["per_page"] = get_query_var("comments_per_page")
    # end if
    if php_empty(lambda : parsed_args["per_page"]):
        parsed_args["per_page"] = 0
        parsed_args["page"] = 0
    # end if
    if "" == parsed_args["max_depth"]:
        if get_option("thread_comments"):
            parsed_args["max_depth"] = get_option("thread_comments_depth")
        else:
            parsed_args["max_depth"] = -1
        # end if
    # end if
    if "" == parsed_args["page"]:
        if php_empty(lambda : overridden_cpage):
            parsed_args["page"] = get_query_var("cpage")
        else:
            threaded = -1 != parsed_args["max_depth"]
            parsed_args["page"] = get_comment_pages_count(_comments, parsed_args["per_page"], threaded) if "newest" == get_option("default_comments_page") else 1
            set_query_var("cpage", parsed_args["page"])
        # end if
    # end if
    #// Validation check.
    parsed_args["page"] = php_intval(parsed_args["page"])
    if 0 == parsed_args["page"] and 0 != parsed_args["per_page"]:
        parsed_args["page"] = 1
    # end if
    if None == parsed_args["reverse_top_level"]:
        parsed_args["reverse_top_level"] = "desc" == get_option("comment_order")
    # end if
    wp_queue_comments_for_comment_meta_lazyload(_comments)
    if php_empty(lambda : parsed_args["walker"]):
        walker = php_new_class("Walker_Comment", lambda : Walker_Comment())
    else:
        walker = parsed_args["walker"]
    # end if
    output = walker.paged_walk(_comments, parsed_args["max_depth"], parsed_args["page"], parsed_args["per_page"], parsed_args)
    in_comment_loop = False
    if parsed_args["echo"]:
        php_print(output)
    else:
        return output
    # end if
# end def wp_list_comments
#// 
#// Outputs a complete commenting form for use within a template.
#// 
#// Most strings and form fields may be controlled through the $args array passed
#// into the function, while you may also choose to use the {@see 'comment_form_default_fields'}
#// filter to modify the array of default fields if you'd just like to add a new
#// one or remove a single field. All fields are also individually passed through
#// a filter of the {@see 'comment_form_field_$name'} where $name is the key used
#// in the array of fields.
#// 
#// @since 3.0.0
#// @since 4.1.0 Introduced the 'class_submit' argument.
#// @since 4.2.0 Introduced the 'submit_button' and 'submit_fields' arguments.
#// @since 4.4.0 Introduced the 'class_form', 'title_reply_before', 'title_reply_after',
#// 'cancel_reply_before', and 'cancel_reply_after' arguments.
#// @since 4.5.0 The 'author', 'email', and 'url' form fields are limited to 245, 100,
#// and 200 characters, respectively.
#// @since 4.6.0 Introduced the 'action' argument.
#// @since 4.9.6 Introduced the 'cookies' default comment field.
#// 
#// @param array       $args {
#// Optional. Default arguments and form fields to override.
#// 
#// @type array $fields {
#// Default comment fields, filterable by default via the {@see 'comment_form_default_fields'} hook.
#// 
#// @type string $author  Comment author field HTML.
#// @type string $email   Comment author email field HTML.
#// @type string $url     Comment author URL field HTML.
#// @type string $cookies Comment cookie opt-in field HTML.
#// }
#// @type string $comment_field        The comment textarea field HTML.
#// @type string $must_log_in          HTML element for a 'must be logged in to comment' message.
#// @type string $logged_in_as         HTML element for a 'logged in as [user]' message.
#// @type string $comment_notes_before HTML element for a message displayed before the comment fields
#// if the user is not logged in.
#// Default 'Your email address will not be published.'.
#// @type string $comment_notes_after  HTML element for a message displayed after the textarea field.
#// @type string $action               The comment form element action attribute. Default '/wp-comments-post.php'.
#// @type string $id_form              The comment form element id attribute. Default 'commentform'.
#// @type string $id_submit            The comment submit element id attribute. Default 'submit'.
#// @type string $class_form           The comment form element class attribute. Default 'comment-form'.
#// @type string $class_submit         The comment submit element class attribute. Default 'submit'.
#// @type string $name_submit          The comment submit element name attribute. Default 'submit'.
#// @type string $title_reply          The translatable 'reply' button label. Default 'Leave a Reply'.
#// @type string $title_reply_to       The translatable 'reply-to' button label. Default 'Leave a Reply to %s',
#// where %s is the author of the comment being replied to.
#// @type string $title_reply_before   HTML displayed before the comment form title.
#// Default: '<h3 id="reply-title" class="comment-reply-title">'.
#// @type string $title_reply_after    HTML displayed after the comment form title.
#// Default: '</h3>'.
#// @type string $cancel_reply_before  HTML displayed before the cancel reply link.
#// @type string $cancel_reply_after   HTML displayed after the cancel reply link.
#// @type string $cancel_reply_link    The translatable 'cancel reply' button label. Default 'Cancel reply'.
#// @type string $label_submit         The translatable 'submit' button label. Default 'Post a comment'.
#// @type string $submit_button        HTML format for the Submit button.
#// Default: '<input name="%1$s" type="submit" id="%2$s" class="%3$s" value="%4$s" />'.
#// @type string $submit_field         HTML format for the markup surrounding the Submit button and comment hidden
#// fields. Default: '<p class="form-submit">%1$s %2$s</p>', where %1$s is the
#// submit button markup and %2$s is the comment hidden fields.
#// @type string $format               The comment form format. Default 'xhtml'. Accepts 'xhtml', 'html5'.
#// }
#// @param int|WP_Post $post_id Post ID or WP_Post object to generate the form for. Default current post.
#//
def comment_form(args=Array(), post_id=None, *args_):
    
    if None == post_id:
        post_id = get_the_ID()
    # end if
    #// Exit the function when comments for the post are closed.
    if (not comments_open(post_id)):
        #// 
        #// Fires after the comment form if comments are closed.
        #// 
        #// @since 3.0.0
        #//
        do_action("comment_form_comments_closed")
        return
    # end if
    commenter = wp_get_current_commenter()
    user = wp_get_current_user()
    user_identity = user.display_name if user.exists() else ""
    args = wp_parse_args(args)
    if (not (php_isset(lambda : args["format"]))):
        args["format"] = "html5" if current_theme_supports("html5", "comment-form") else "xhtml"
    # end if
    req = get_option("require_name_email")
    html_req = " required='required'" if req else ""
    html5 = "html5" == args["format"]
    fields = Array({"author": php_sprintf("<p class=\"comment-form-author\">%s %s</p>", php_sprintf("<label for=\"author\">%s%s</label>", __("Name"), " <span class=\"required\">*</span>" if req else ""), php_sprintf("<input id=\"author\" name=\"author\" type=\"text\" value=\"%s\" size=\"30\" maxlength=\"245\"%s />", esc_attr(commenter["comment_author"]), html_req)), "email": php_sprintf("<p class=\"comment-form-email\">%s %s</p>", php_sprintf("<label for=\"email\">%s%s</label>", __("Email"), " <span class=\"required\">*</span>" if req else ""), php_sprintf("<input id=\"email\" name=\"email\" %s value=\"%s\" size=\"30\" maxlength=\"100\" aria-describedby=\"email-notes\"%s />", "type=\"email\"" if html5 else "type=\"text\"", esc_attr(commenter["comment_author_email"]), html_req)), "url": php_sprintf("<p class=\"comment-form-url\">%s %s</p>", php_sprintf("<label for=\"url\">%s</label>", __("Website")), php_sprintf("<input id=\"url\" name=\"url\" %s value=\"%s\" size=\"30\" maxlength=\"200\" />", "type=\"url\"" if html5 else "type=\"text\"", esc_attr(commenter["comment_author_url"])))})
    if has_action("set_comment_cookies", "wp_set_comment_cookies") and get_option("show_comments_cookies_opt_in"):
        consent = "" if php_empty(lambda : commenter["comment_author_email"]) else " checked=\"checked\""
        fields["cookies"] = php_sprintf("<p class=\"comment-form-cookies-consent\">%s %s</p>", php_sprintf("<input id=\"wp-comment-cookies-consent\" name=\"wp-comment-cookies-consent\" type=\"checkbox\" value=\"yes\"%s />", consent), php_sprintf("<label for=\"wp-comment-cookies-consent\">%s</label>", __("Save my name, email, and website in this browser for the next time I comment.")))
        #// Ensure that the passed fields include cookies consent.
        if (php_isset(lambda : args["fields"])) and (not (php_isset(lambda : args["fields"]["cookies"]))):
            args["fields"]["cookies"] = fields["cookies"]
        # end if
    # end if
    required_text = php_sprintf(" " + __("Required fields are marked %s"), "<span class=\"required\">*</span>")
    #// 
    #// Filters the default comment form fields.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string[] $fields Array of the default comment fields.
    #//
    fields = apply_filters("comment_form_default_fields", fields)
    defaults = Array({"fields": fields, "comment_field": php_sprintf("<p class=\"comment-form-comment\">%s %s</p>", php_sprintf("<label for=\"comment\">%s</label>", _x("Comment", "noun")), "<textarea id=\"comment\" name=\"comment\" cols=\"45\" rows=\"8\" maxlength=\"65525\" required=\"required\"></textarea>"), "must_log_in": php_sprintf("<p class=\"must-log-in\">%s</p>", php_sprintf(__("You must be <a href=\"%s\">logged in</a> to post a comment."), wp_login_url(apply_filters("the_permalink", get_permalink(post_id), post_id)))), "logged_in_as": php_sprintf("<p class=\"logged-in-as\">%s</p>", php_sprintf(__("<a href=\"%1$s\" aria-label=\"%2$s\">Logged in as %3$s</a>. <a href=\"%4$s\">Log out?</a>"), get_edit_user_link(), esc_attr(php_sprintf(__("Logged in as %s. Edit your profile."), user_identity)), user_identity, wp_logout_url(apply_filters("the_permalink", get_permalink(post_id), post_id)))), "comment_notes_before": php_sprintf("<p class=\"comment-notes\">%s%s</p>", php_sprintf("<span id=\"email-notes\">%s</span>", __("Your email address will not be published.")), required_text if req else ""), "comment_notes_after": "", "action": site_url("/wp-comments-post.php"), "id_form": "commentform", "id_submit": "submit", "class_form": "comment-form", "class_submit": "submit", "name_submit": "submit", "title_reply": __("Leave a Reply"), "title_reply_to": __("Leave a Reply to %s"), "title_reply_before": "<h3 id=\"reply-title\" class=\"comment-reply-title\">", "title_reply_after": "</h3>", "cancel_reply_before": " <small>", "cancel_reply_after": "</small>", "cancel_reply_link": __("Cancel reply"), "label_submit": __("Post Comment"), "submit_button": "<input name=\"%1$s\" type=\"submit\" id=\"%2$s\" class=\"%3$s\" value=\"%4$s\" />", "submit_field": "<p class=\"form-submit\">%1$s %2$s</p>", "format": "xhtml"})
    #// 
    #// Filters the comment form default arguments.
    #// 
    #// Use {@see 'comment_form_default_fields'} to filter the comment fields.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $defaults The default comment form arguments.
    #//
    args = wp_parse_args(args, apply_filters("comment_form_defaults", defaults))
    #// Ensure that the filtered args contain all required default values.
    args = php_array_merge(defaults, args)
    #// Remove `aria-describedby` from the email field if there's no associated description.
    if (php_isset(lambda : args["fields"]["email"])) and False == php_strpos(args["comment_notes_before"], "id=\"email-notes\""):
        args["fields"]["email"] = php_str_replace(" aria-describedby=\"email-notes\"", "", args["fields"]["email"])
    # end if
    #// 
    #// Fires before the comment form.
    #// 
    #// @since 3.0.0
    #//
    do_action("comment_form_before")
    php_print(" <div id=\"respond\" class=\"comment-respond\">\n        ")
    php_print(args["title_reply_before"])
    comment_form_title(args["title_reply"], args["title_reply_to"])
    php_print(args["cancel_reply_before"])
    cancel_comment_reply_link(args["cancel_reply_link"])
    php_print(args["cancel_reply_after"])
    php_print(args["title_reply_after"])
    if get_option("comment_registration") and (not is_user_logged_in()):
        php_print(args["must_log_in"])
        #// 
        #// Fires after the HTML-formatted 'must log in after' message in the comment form.
        #// 
        #// @since 3.0.0
        #//
        do_action("comment_form_must_log_in_after")
    else:
        printf("<form action=\"%s\" method=\"post\" id=\"%s\" class=\"%s\"%s>", esc_url(args["action"]), esc_attr(args["id_form"]), esc_attr(args["class_form"]), " novalidate" if html5 else "")
        #// 
        #// Fires at the top of the comment form, inside the form tag.
        #// 
        #// @since 3.0.0
        #//
        do_action("comment_form_top")
        if is_user_logged_in():
            #// 
            #// Filters the 'logged in' message for the comment form for display.
            #// 
            #// @since 3.0.0
            #// 
            #// @param string $args_logged_in The logged-in-as HTML-formatted message.
            #// @param array  $commenter      An array containing the comment author's
            #// username, email, and URL.
            #// @param string $user_identity  If the commenter is a registered user,
            #// the display name, blank otherwise.
            #//
            php_print(apply_filters("comment_form_logged_in", args["logged_in_as"], commenter, user_identity))
            #// 
            #// Fires after the is_user_logged_in() check in the comment form.
            #// 
            #// @since 3.0.0
            #// 
            #// @param array  $commenter     An array containing the comment author's
            #// username, email, and URL.
            #// @param string $user_identity If the commenter is a registered user,
            #// the display name, blank otherwise.
            #//
            do_action("comment_form_logged_in_after", commenter, user_identity)
        else:
            php_print(args["comment_notes_before"])
        # end if
        #// Prepare an array of all fields, including the textarea.
        comment_fields = Array({"comment": args["comment_field"]}) + args["fields"]
        #// 
        #// Filters the comment form fields, including the textarea.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array $comment_fields The comment fields.
        #//
        comment_fields = apply_filters("comment_form_fields", comment_fields)
        #// Get an array of field names, excluding the textarea.
        comment_field_keys = php_array_diff(php_array_keys(comment_fields), Array("comment"))
        #// Get the first and the last field name, excluding the textarea.
        first_field = reset(comment_field_keys)
        last_field = php_end(comment_field_keys)
        for name,field in comment_fields:
            if "comment" == name:
                #// 
                #// Filters the content of the comment textarea field for display.
                #// 
                #// @since 3.0.0
                #// 
                #// @param string $args_comment_field The content of the comment textarea field.
                #//
                php_print(apply_filters("comment_form_field_comment", field))
                php_print(args["comment_notes_after"])
            elif (not is_user_logged_in()):
                if first_field == name:
                    #// 
                    #// Fires before the comment fields in the comment form, excluding the textarea.
                    #// 
                    #// @since 3.0.0
                    #//
                    do_action("comment_form_before_fields")
                # end if
                #// 
                #// Filters a comment form field for display.
                #// 
                #// The dynamic portion of the filter hook, `$name`, refers to the name
                #// of the comment form field. Such as 'author', 'email', or 'url'.
                #// 
                #// @since 3.0.0
                #// 
                #// @param string $field The HTML-formatted output of the comment form field.
                #//
                php_print(apply_filters(str("comment_form_field_") + str(name), field) + "\n")
                if last_field == name:
                    #// 
                    #// Fires after the comment fields in the comment form, excluding the textarea.
                    #// 
                    #// @since 3.0.0
                    #//
                    do_action("comment_form_after_fields")
                # end if
            # end if
        # end for
        submit_button = php_sprintf(args["submit_button"], esc_attr(args["name_submit"]), esc_attr(args["id_submit"]), esc_attr(args["class_submit"]), esc_attr(args["label_submit"]))
        #// 
        #// Filters the submit button for the comment form to display.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string $submit_button HTML markup for the submit button.
        #// @param array  $args          Arguments passed to comment_form().
        #//
        submit_button = apply_filters("comment_form_submit_button", submit_button, args)
        submit_field = php_sprintf(args["submit_field"], submit_button, get_comment_id_fields(post_id))
        #// 
        #// Filters the submit field for the comment form to display.
        #// 
        #// The submit field includes the submit button, hidden fields for the
        #// comment form, and any wrapper markup.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string $submit_field HTML markup for the submit field.
        #// @param array  $args         Arguments passed to comment_form().
        #//
        php_print(apply_filters("comment_form_submit_field", submit_field, args))
        #// 
        #// Fires at the bottom of the comment form, inside the closing form tag.
        #// 
        #// @since 1.5.0
        #// 
        #// @param int $post_id The post ID.
        #//
        do_action("comment_form", post_id)
        php_print("</form>")
    # end if
    php_print(" </div><!-- #respond -->\n   ")
    #// 
    #// Fires after the comment form.
    #// 
    #// @since 3.0.0
    #//
    do_action("comment_form_after")
# end def comment_form
