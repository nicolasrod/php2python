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
#// WordPress Feed API
#// 
#// Many of the functions used in here belong in The Loop, or The Loop for the
#// Feeds.
#// 
#// @package WordPress
#// @subpackage Feed
#// @since 2.1.0
#// 
#// 
#// RSS container for the bloginfo function.
#// 
#// You can retrieve anything that you can using the get_bloginfo() function.
#// Everything will be stripped of tags and characters converted, when the values
#// are retrieved for use in the feeds.
#// 
#// @since 1.5.1
#// @see get_bloginfo() For the list of possible values to display.
#// 
#// @param string $show See get_bloginfo() for possible values.
#// @return string
#//
def get_bloginfo_rss(show_="", *_args_):
    
    
    info_ = strip_tags(get_bloginfo(show_))
    #// 
    #// Filters the bloginfo for use in RSS feeds.
    #// 
    #// @since 2.2.0
    #// 
    #// @see convert_chars()
    #// @see get_bloginfo()
    #// 
    #// @param string $info Converted string value of the blog information.
    #// @param string $show The type of blog information to retrieve.
    #//
    return apply_filters("get_bloginfo_rss", convert_chars(info_), show_)
# end def get_bloginfo_rss
#// 
#// Display RSS container for the bloginfo function.
#// 
#// You can retrieve anything that you can using the get_bloginfo() function.
#// Everything will be stripped of tags and characters converted, when the values
#// are retrieved for use in the feeds.
#// 
#// @since 0.71
#// @see get_bloginfo() For the list of possible values to display.
#// 
#// @param string $show See get_bloginfo() for possible values.
#//
def bloginfo_rss(show_="", *_args_):
    
    
    #// 
    #// Filters the bloginfo for display in RSS feeds.
    #// 
    #// @since 2.1.0
    #// 
    #// @see get_bloginfo()
    #// 
    #// @param string $rss_container RSS container for the blog information.
    #// @param string $show          The type of blog information to retrieve.
    #//
    php_print(apply_filters("bloginfo_rss", get_bloginfo_rss(show_), show_))
# end def bloginfo_rss
#// 
#// Retrieve the default feed.
#// 
#// The default feed is 'rss2', unless a plugin changes it through the
#// {@see 'default_feed'} filter.
#// 
#// @since 2.5.0
#// 
#// @return string Default feed, or for example 'rss2', 'atom', etc.
#//
def get_default_feed(*_args_):
    
    
    #// 
    #// Filters the default feed type.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $feed_type Type of default feed. Possible values include 'rss2', 'atom'.
    #// Default 'rss2'.
    #//
    default_feed_ = apply_filters("default_feed", "rss2")
    return "rss2" if "rss" == default_feed_ else default_feed_
# end def get_default_feed
#// 
#// Retrieve the blog title for the feed title.
#// 
#// @since 2.2.0
#// @since 4.4.0 The optional `$sep` parameter was deprecated and renamed to `$deprecated`.
#// 
#// @param string $deprecated Unused..
#// @return string The document title.
#//
def get_wp_title_rss(deprecated_="&#8211;", *_args_):
    
    
    if "&#8211;" != deprecated_:
        #// translators: %s: 'document_title_separator' filter name.
        _deprecated_argument(__FUNCTION__, "4.4.0", php_sprintf(__("Use the %s filter instead."), "<code>document_title_separator</code>"))
    # end if
    #// 
    #// Filters the blog title for use as the feed title.
    #// 
    #// @since 2.2.0
    #// @since 4.4.0 The `$sep` parameter was deprecated and renamed to `$deprecated`.
    #// 
    #// @param string $title      The current blog title.
    #// @param string $deprecated Unused.
    #//
    return apply_filters("get_wp_title_rss", wp_get_document_title(), deprecated_)
# end def get_wp_title_rss
#// 
#// Display the blog title for display of the feed title.
#// 
#// @since 2.2.0
#// @since 4.4.0 The optional `$sep` parameter was deprecated and renamed to `$deprecated`.
#// 
#// @param string $deprecated Unused.
#//
def wp_title_rss(deprecated_="&#8211;", *_args_):
    
    
    if "&#8211;" != deprecated_:
        #// translators: %s: 'document_title_separator' filter name.
        _deprecated_argument(__FUNCTION__, "4.4.0", php_sprintf(__("Use the %s filter instead."), "<code>document_title_separator</code>"))
    # end if
    #// 
    #// Filters the blog title for display of the feed title.
    #// 
    #// @since 2.2.0
    #// @since 4.4.0 The `$sep` parameter was deprecated and renamed to `$deprecated`.
    #// 
    #// @see get_wp_title_rss()
    #// 
    #// @param string $wp_title_rss The current blog title.
    #// @param string $deprecated   Unused.
    #//
    php_print(apply_filters("wp_title_rss", get_wp_title_rss(), deprecated_))
# end def wp_title_rss
#// 
#// Retrieve the current post title for the feed.
#// 
#// @since 2.0.0
#// 
#// @return string Current post title.
#//
def get_the_title_rss(*_args_):
    
    
    title_ = get_the_title()
    #// 
    #// Filters the post title for use in a feed.
    #// 
    #// @since 1.2.0
    #// 
    #// @param string $title The current post title.
    #//
    title_ = apply_filters("the_title_rss", title_)
    return title_
# end def get_the_title_rss
#// 
#// Display the post title in the feed.
#// 
#// @since 0.71
#//
def the_title_rss(*_args_):
    
    
    php_print(get_the_title_rss())
# end def the_title_rss
#// 
#// Retrieve the post content for feeds.
#// 
#// @since 2.9.0
#// @see get_the_content()
#// 
#// @param string $feed_type The type of feed. rss2 | atom | rss | rdf
#// @return string The filtered content.
#//
def get_the_content_feed(feed_type_=None, *_args_):
    if feed_type_ is None:
        feed_type_ = None
    # end if
    
    if (not feed_type_):
        feed_type_ = get_default_feed()
    # end if
    #// This filter is documented in wp-includes/post-template.php
    content_ = apply_filters("the_content", get_the_content())
    content_ = php_str_replace("]]>", "]]&gt;", content_)
    #// 
    #// Filters the post content for use in feeds.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $content   The current post content.
    #// @param string $feed_type Type of feed. Possible values include 'rss2', 'atom'.
    #// Default 'rss2'.
    #//
    return apply_filters("the_content_feed", content_, feed_type_)
# end def get_the_content_feed
#// 
#// Display the post content for feeds.
#// 
#// @since 2.9.0
#// 
#// @param string $feed_type The type of feed. rss2 | atom | rss | rdf
#//
def the_content_feed(feed_type_=None, *_args_):
    if feed_type_ is None:
        feed_type_ = None
    # end if
    
    php_print(get_the_content_feed(feed_type_))
# end def the_content_feed
#// 
#// Display the post excerpt for the feed.
#// 
#// @since 0.71
#//
def the_excerpt_rss(*_args_):
    
    
    output_ = get_the_excerpt()
    #// 
    #// Filters the post excerpt for a feed.
    #// 
    #// @since 1.2.0
    #// 
    #// @param string $output The current post excerpt.
    #//
    php_print(apply_filters("the_excerpt_rss", output_))
# end def the_excerpt_rss
#// 
#// Display the permalink to the post for use in feeds.
#// 
#// @since 2.3.0
#//
def the_permalink_rss(*_args_):
    
    
    #// 
    #// Filters the permalink to the post for use in feeds.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $post_permalink The current post permalink.
    #//
    php_print(esc_url(apply_filters("the_permalink_rss", get_permalink())))
# end def the_permalink_rss
#// 
#// Outputs the link to the comments for the current post in an xml safe way
#// 
#// @since 3.0.0
#//
def comments_link_feed(*_args_):
    
    
    #// 
    #// Filters the comments permalink for the current post.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $comment_permalink The current comment permalink with
    #// '#comments' appended.
    #//
    php_print(esc_url(apply_filters("comments_link_feed", get_comments_link())))
# end def comments_link_feed
#// 
#// Display the feed GUID for the current comment.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Comment $comment_id Optional comment object or id. Defaults to global comment object.
#//
def comment_guid(comment_id_=None, *_args_):
    if comment_id_ is None:
        comment_id_ = None
    # end if
    
    php_print(esc_url(get_comment_guid(comment_id_)))
# end def comment_guid
#// 
#// Retrieve the feed GUID for the current comment.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Comment $comment_id Optional comment object or id. Defaults to global comment object.
#// @return string|false GUID for comment on success, false on failure.
#//
def get_comment_guid(comment_id_=None, *_args_):
    if comment_id_ is None:
        comment_id_ = None
    # end if
    
    comment_ = get_comment(comment_id_)
    if (not php_is_object(comment_)):
        return False
    # end if
    return get_the_guid(comment_.comment_post_ID) + "#comment-" + comment_.comment_ID
# end def get_comment_guid
#// 
#// Display the link to the comments.
#// 
#// @since 1.5.0
#// @since 4.4.0 Introduced the `$comment` argument.
#// 
#// @param int|WP_Comment $comment Optional. Comment object or id. Defaults to global comment object.
#//
def comment_link(comment_=None, *_args_):
    if comment_ is None:
        comment_ = None
    # end if
    
    #// 
    #// Filters the current comment's permalink.
    #// 
    #// @since 3.6.0
    #// 
    #// @see get_comment_link()
    #// 
    #// @param string $comment_permalink The current comment permalink.
    #//
    php_print(esc_url(apply_filters("comment_link", get_comment_link(comment_))))
# end def comment_link
#// 
#// Retrieve the current comment author for use in the feeds.
#// 
#// @since 2.0.0
#// 
#// @return string Comment Author
#//
def get_comment_author_rss(*_args_):
    
    
    #// 
    #// Filters the current comment author for use in a feed.
    #// 
    #// @since 1.5.0
    #// 
    #// @see get_comment_author()
    #// 
    #// @param string $comment_author The current comment author.
    #//
    return apply_filters("comment_author_rss", get_comment_author())
# end def get_comment_author_rss
#// 
#// Display the current comment author in the feed.
#// 
#// @since 1.0.0
#//
def comment_author_rss(*_args_):
    
    
    php_print(get_comment_author_rss())
# end def comment_author_rss
#// 
#// Display the current comment content for use in the feeds.
#// 
#// @since 1.0.0
#//
def comment_text_rss(*_args_):
    
    
    comment_text_ = get_comment_text()
    #// 
    #// Filters the current comment content for use in a feed.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $comment_text The content of the current comment.
    #//
    comment_text_ = apply_filters("comment_text_rss", comment_text_)
    php_print(comment_text_)
# end def comment_text_rss
#// 
#// Retrieve all of the post categories, formatted for use in feeds.
#// 
#// All of the categories for the current post in the feed loop, will be
#// retrieved and have feed markup added, so that they can easily be added to the
#// RSS2, Atom, or RSS1 and RSS0.91 RDF feeds.
#// 
#// @since 2.1.0
#// 
#// @param string $type Optional, default is the type returned by get_default_feed().
#// @return string All of the post categories for displaying in the feed.
#//
def get_the_category_rss(type_=None, *_args_):
    if type_ is None:
        type_ = None
    # end if
    
    if php_empty(lambda : type_):
        type_ = get_default_feed()
    # end if
    categories_ = get_the_category()
    tags_ = get_the_tags()
    the_list_ = ""
    cat_names_ = Array()
    filter_ = "rss"
    if "atom" == type_:
        filter_ = "raw"
    # end if
    if (not php_empty(lambda : categories_)):
        for category_ in categories_:
            cat_names_[-1] = sanitize_term_field("name", category_.name, category_.term_id, "category", filter_)
        # end for
    # end if
    if (not php_empty(lambda : tags_)):
        for tag_ in tags_:
            cat_names_[-1] = sanitize_term_field("name", tag_.name, tag_.term_id, "post_tag", filter_)
        # end for
    # end if
    cat_names_ = array_unique(cat_names_)
    for cat_name_ in cat_names_:
        if "rdf" == type_:
            the_list_ += str("      <dc:subject><![CDATA[") + str(cat_name_) + str("]]></dc:subject>\n")
        elif "atom" == type_:
            the_list_ += php_sprintf("<category scheme=\"%1$s\" term=\"%2$s\" />", esc_attr(get_bloginfo_rss("url")), esc_attr(cat_name_))
        else:
            the_list_ += "      <category><![CDATA[" + html_entity_decode(cat_name_, ENT_COMPAT, get_option("blog_charset")) + "]]></category>\n"
        # end if
    # end for
    #// 
    #// Filters all of the post categories for display in a feed.
    #// 
    #// @since 1.2.0
    #// 
    #// @param string $the_list All of the RSS post categories.
    #// @param string $type     Type of feed. Possible values include 'rss2', 'atom'.
    #// Default 'rss2'.
    #//
    return apply_filters("the_category_rss", the_list_, type_)
# end def get_the_category_rss
#// 
#// Display the post categories in the feed.
#// 
#// @since 0.71
#// @see get_the_category_rss() For better explanation.
#// 
#// @param string $type Optional, default is the type returned by get_default_feed().
#//
def the_category_rss(type_=None, *_args_):
    if type_ is None:
        type_ = None
    # end if
    
    php_print(get_the_category_rss(type_))
# end def the_category_rss
#// 
#// Display the HTML type based on the blog setting.
#// 
#// The two possible values are either 'xhtml' or 'html'.
#// 
#// @since 2.2.0
#//
def html_type_rss(*_args_):
    
    
    type_ = get_bloginfo("html_type")
    if php_strpos(type_, "xhtml") != False:
        type_ = "xhtml"
    else:
        type_ = "html"
    # end if
    php_print(type_)
# end def html_type_rss
#// 
#// Display the rss enclosure for the current post.
#// 
#// Uses the global $post to check whether the post requires a password and if
#// the user has the password for the post. If not then it will return before
#// displaying.
#// 
#// Also uses the function get_post_custom() to get the post's 'enclosure'
#// metadata field and parses the value to display the enclosure(s). The
#// enclosure(s) consist of enclosure HTML tag(s) with a URI and other
#// attributes.
#// 
#// @since 1.5.0
#//
def rss_enclosure(*_args_):
    
    
    if post_password_required():
        return
    # end if
    for key_,val_ in get_post_custom().items():
        if "enclosure" == key_:
            for enc_ in val_:
                enclosure_ = php_explode("\n", enc_)
                #// Only get the first element, e.g. 'audio/mpeg' from 'audio/mpeg mpga mp2 mp3'.
                t_ = php_preg_split("/[ \\t]/", php_trim(enclosure_[2]))
                type_ = t_[0]
                #// 
                #// Filters the RSS enclosure HTML link tag for the current post.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string $html_link_tag The HTML link tag with a URI and other attributes.
                #//
                php_print(apply_filters("rss_enclosure", "<enclosure url=\"" + esc_url(php_trim(enclosure_[0])) + "\" length=\"" + absint(php_trim(enclosure_[1])) + "\" type=\"" + esc_attr(type_) + "\" />" + "\n"))
            # end for
        # end if
    # end for
# end def rss_enclosure
#// 
#// Display the atom enclosure for the current post.
#// 
#// Uses the global $post to check whether the post requires a password and if
#// the user has the password for the post. If not then it will return before
#// displaying.
#// 
#// Also uses the function get_post_custom() to get the post's 'enclosure'
#// metadata field and parses the value to display the enclosure(s). The
#// enclosure(s) consist of link HTML tag(s) with a URI and other attributes.
#// 
#// @since 2.2.0
#//
def atom_enclosure(*_args_):
    
    
    if post_password_required():
        return
    # end if
    for key_,val_ in get_post_custom().items():
        if "enclosure" == key_:
            for enc_ in val_:
                enclosure_ = php_explode("\n", enc_)
                #// 
                #// Filters the atom enclosure HTML link tag for the current post.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string $html_link_tag The HTML link tag with a URI and other attributes.
                #//
                php_print(apply_filters("atom_enclosure", "<link href=\"" + esc_url(php_trim(enclosure_[0])) + "\" rel=\"enclosure\" length=\"" + absint(php_trim(enclosure_[1])) + "\" type=\"" + esc_attr(php_trim(enclosure_[2])) + "\" />" + "\n"))
            # end for
        # end if
    # end for
# end def atom_enclosure
#// 
#// Determine the type of a string of data with the data formatted.
#// 
#// Tell whether the type is text, html, or xhtml, per RFC 4287 section 3.1.
#// 
#// In the case of WordPress, text is defined as containing no markup,
#// xhtml is defined as "well formed", and html as tag soup (i.e., the rest).
#// 
#// Container div tags are added to xhtml values, per section 3.1.1.3.
#// 
#// @link http://www.atomenabled.org/developers/syndication/atom-format-spec.php#rfc.section.3.1
#// 
#// @since 2.5.0
#// 
#// @param string $data Input string
#// @return array array(type, value)
#//
def prep_atom_text_construct(data_=None, *_args_):
    
    
    if php_strpos(data_, "<") == False and php_strpos(data_, "&") == False:
        return Array("text", data_)
    # end if
    if (not php_function_exists("xml_parser_create")):
        trigger_error(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
        return Array("html", str("<![CDATA[") + str(data_) + str("]]>"))
    # end if
    parser_ = xml_parser_create()
    xml_parse(parser_, "<div>" + data_ + "</div>", True)
    code_ = xml_get_error_code(parser_)
    xml_parser_free(parser_)
    if (not code_):
        if php_strpos(data_, "<") == False:
            return Array("text", data_)
        else:
            data_ = str("<div xmlns='http://www.w3.org/1999/xhtml'>") + str(data_) + str("</div>")
            return Array("xhtml", data_)
        # end if
    # end if
    if php_strpos(data_, "]]>") == False:
        return Array("html", str("<![CDATA[") + str(data_) + str("]]>"))
    else:
        return Array("html", htmlspecialchars(data_))
    # end if
# end def prep_atom_text_construct
#// 
#// Displays Site Icon in atom feeds.
#// 
#// @since 4.3.0
#// 
#// @see get_site_icon_url()
#//
def atom_site_icon(*_args_):
    
    
    url_ = get_site_icon_url(32)
    if url_:
        php_print("<icon>" + convert_chars(url_) + "</icon>\n")
    # end if
# end def atom_site_icon
#// 
#// Displays Site Icon in RSS2.
#// 
#// @since 4.3.0
#//
def rss2_site_icon(*_args_):
    
    
    rss_title_ = get_wp_title_rss()
    if php_empty(lambda : rss_title_):
        rss_title_ = get_bloginfo_rss("name")
    # end if
    url_ = get_site_icon_url(32)
    if url_:
        php_print("\n<image>\n  <url>" + convert_chars(url_) + "</url>\n    <title>" + rss_title_ + "</title>\n <link>" + get_bloginfo_rss("url") + """</link>
        <width>32</width>
        <height>32</height>
        </image> """ + "\n")
    # end if
# end def rss2_site_icon
#// 
#// Returns the link for the currently displayed feed.
#// 
#// @since 5.3.0
#// 
#// @return string Correct link for the atom:self element.
#//
def get_self_link(*_args_):
    
    
    host_ = php_no_error(lambda: php_parse_url(home_url()))
    return set_url_scheme("http://" + host_["host"] + wp_unslash(PHP_SERVER["REQUEST_URI"]))
# end def get_self_link
#// 
#// Display the link for the currently displayed feed in a XSS safe way.
#// 
#// Generate a correct link for the atom:self element.
#// 
#// @since 2.5.0
#//
def self_link(*_args_):
    
    
    #// 
    #// Filters the current feed URL.
    #// 
    #// @since 3.6.0
    #// 
    #// @see set_url_scheme()
    #// @see wp_unslash()
    #// 
    #// @param string $feed_link The link for the feed with set URL scheme.
    #//
    php_print(esc_url(apply_filters("self_link", get_self_link())))
# end def self_link
#// 
#// Get the UTC time of the most recently modified post from WP_Query.
#// 
#// If viewing a comment feed, the time of the most recently modified
#// comment will be returned.
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @since 5.2.0
#// 
#// @param string $format Date format string to return the time in.
#// @return string|false The time in requested format, or false on failure.
#//
def get_feed_build_date(format_=None, *_args_):
    
    
    global wp_query_
    php_check_if_defined("wp_query_")
    datetime_ = False
    max_modified_time_ = False
    utc_ = php_new_class("DateTimeZone", lambda : DateTimeZone("UTC"))
    if (not php_empty(lambda : wp_query_)) and wp_query_.have_posts():
        #// Extract the post modified times from the posts.
        modified_times_ = wp_list_pluck(wp_query_.posts, "post_modified_gmt")
        #// If this is a comment feed, check those objects too.
        if wp_query_.is_comment_feed() and wp_query_.comment_count:
            #// Extract the comment modified times from the comments.
            comment_times_ = wp_list_pluck(wp_query_.comments, "comment_date_gmt")
            #// Add the comment times to the post times for comparison.
            modified_times_ = php_array_merge(modified_times_, comment_times_)
        # end if
        #// Determine the maximum modified time.
        datetime_ = date_create_immutable_from_format("Y-m-d H:i:s", php_max(modified_times_), utc_)
    # end if
    if False == datetime_:
        #// Fall back to last time any post was modified or published.
        datetime_ = date_create_immutable_from_format("Y-m-d H:i:s", get_lastpostmodified("GMT"), utc_)
    # end if
    if False != datetime_:
        max_modified_time_ = datetime_.format(format_)
    # end if
    #// 
    #// Filters the date the last post or comment in the query was modified.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string|false $max_modified_time Date the last post or comment was modified in the query, in UTC.
    #// False on failure.
    #// @param string       $format            The date format requested in get_feed_build_date().
    #//
    return apply_filters("get_feed_build_date", max_modified_time_, format_)
# end def get_feed_build_date
#// 
#// Return the content type for specified feed type.
#// 
#// @since 2.8.0
#// 
#// @param string $type Type of feed. Possible values include 'rss', rss2', 'atom', and 'rdf'.
#//
def feed_content_type(type_="", *_args_):
    
    
    if php_empty(lambda : type_):
        type_ = get_default_feed()
    # end if
    types_ = Array({"rss": "application/rss+xml", "rss2": "application/rss+xml", "rss-http": "text/xml", "atom": "application/atom+xml", "rdf": "application/rdf+xml"})
    content_type_ = types_[type_] if (not php_empty(lambda : types_[type_])) else "application/octet-stream"
    #// 
    #// Filters the content type for a specific feed type.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $content_type Content type indicating the type of data that a feed contains.
    #// @param string $type         Type of feed. Possible values include 'rss', rss2', 'atom', and 'rdf'.
    #//
    return apply_filters("feed_content_type", content_type_, type_)
# end def feed_content_type
#// 
#// Build SimplePie object based on RSS or Atom feed from URL.
#// 
#// @since 2.8.0
#// 
#// @param string|string[] $url URL of feed to retrieve. If an array of URLs, the feeds are merged
#// using SimplePie's multifeed feature.
#// See also {@link http://simplepie.org/wiki/faq/typical_multifeed_gotchas}
#// @return SimplePie|WP_Error SimplePie object on success or WP_Error object on failure.
#//
def fetch_feed(url_=None, *_args_):
    
    
    if (not php_class_exists("SimplePie", False)):
        php_include_file(ABSPATH + WPINC + "/class-simplepie.php", once=True)
    # end if
    php_include_file(ABSPATH + WPINC + "/class-wp-feed-cache.php", once=True)
    php_include_file(ABSPATH + WPINC + "/class-wp-feed-cache-transient.php", once=True)
    php_include_file(ABSPATH + WPINC + "/class-wp-simplepie-file.php", once=True)
    php_include_file(ABSPATH + WPINC + "/class-wp-simplepie-sanitize-kses.php", once=True)
    feed_ = php_new_class("SimplePie", lambda : SimplePie())
    feed_.set_sanitize_class("WP_SimplePie_Sanitize_KSES")
    #// We must manually overwrite $feed->sanitize because SimplePie's
    #// constructor sets it before we have a chance to set the sanitization class.
    feed_.sanitize = php_new_class("WP_SimplePie_Sanitize_KSES", lambda : WP_SimplePie_Sanitize_KSES())
    feed_.set_cache_class("WP_Feed_Cache")
    feed_.set_file_class("WP_SimplePie_File")
    feed_.set_feed_url(url_)
    #// This filter is documented in wp-includes/class-wp-feed-cache-transient.php
    feed_.set_cache_duration(apply_filters("wp_feed_cache_transient_lifetime", 12 * HOUR_IN_SECONDS, url_))
    #// 
    #// Fires just before processing the SimplePie feed object.
    #// 
    #// @since 3.0.0
    #// 
    #// @param SimplePie       $feed SimplePie feed object (passed by reference).
    #// @param string|string[] $url  URL of feed or array of URLs of feeds to retrieve.
    #//
    do_action_ref_array("wp_feed_options", Array(feed_, url_))
    feed_.init()
    feed_.set_output_encoding(get_option("blog_charset"))
    if feed_.error():
        return php_new_class("WP_Error", lambda : WP_Error("simplepie-error", feed_.error()))
    # end if
    return feed_
# end def fetch_feed
