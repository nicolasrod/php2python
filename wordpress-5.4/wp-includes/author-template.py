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
#// Author Template functions for use in themes.
#// 
#// These functions must be used within the WordPress Loop.
#// 
#// @link https://codex.wordpress.org/Author_Templates
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// Retrieve the author of the current post.
#// 
#// @since 1.5.0
#// 
#// @global object $authordata The current author's DB object.
#// 
#// @param string $deprecated Deprecated.
#// @return string|null The author's display name.
#//
def get_the_author(deprecated="", *args_):
    
    global authordata
    php_check_if_defined("authordata")
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.1.0")
    # end if
    #// 
    #// Filters the display name of the current post's author.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $authordata->display_name The author's display name.
    #//
    return apply_filters("the_author", authordata.display_name if php_is_object(authordata) else None)
# end def get_the_author
#// 
#// Display the name of the author of the current post.
#// 
#// The behavior of this function is based off of old functionality predating
#// get_the_author(). This function is not deprecated, but is designed to echo
#// the value from get_the_author() and as an result of any old theme that might
#// still use the old behavior will also pass the value from get_the_author().
#// 
#// The normal, expected behavior of this function is to echo the author and not
#// return it. However, backward compatibility has to be maintained.
#// 
#// @since 0.71
#// @see get_the_author()
#// @link https://developer.wordpress.org/reference/functions/the_author
#// 
#// @param string $deprecated      Deprecated.
#// @param bool   $deprecated_echo Deprecated. Use get_the_author(). Echo the string or return it.
#// @return string|null The author's display name, from get_the_author().
#//
def the_author(deprecated="", deprecated_echo=True, *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.1.0")
    # end if
    if True != deprecated_echo:
        _deprecated_argument(__FUNCTION__, "1.5.0", php_sprintf(__("Use %s instead if you do not want the value echoed."), "<code>get_the_author()</code>"))
    # end if
    if deprecated_echo:
        php_print(get_the_author())
    # end if
    return get_the_author()
# end def the_author
#// 
#// Retrieve the author who last edited the current post.
#// 
#// @since 2.8.0
#// 
#// @return string|void The author's display name.
#//
def get_the_modified_author(*args_):
    
    last_id = get_post_meta(get_post().ID, "_edit_last", True)
    if last_id:
        last_user = get_userdata(last_id)
        #// 
        #// Filters the display name of the author who last edited the current post.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $last_user->display_name The author's display name.
        #//
        return apply_filters("the_modified_author", last_user.display_name)
    # end if
# end def get_the_modified_author
#// 
#// Display the name of the author who last edited the current post,
#// if the author's ID is available.
#// 
#// @since 2.8.0
#// 
#// @see get_the_author()
#//
def the_modified_author(*args_):
    
    php_print(get_the_modified_author())
# end def the_modified_author
#// 
#// Retrieves the requested data of the author of the current post.
#// 
#// Valid values for the `$field` parameter include:
#// 
#// - admin_color
#// - aim
#// - comment_shortcuts
#// - description
#// - display_name
#// - first_name
#// - ID
#// - jabber
#// - last_name
#// - nickname
#// - plugins_last_view
#// - plugins_per_page
#// - rich_editing
#// - syntax_highlighting
#// - user_activation_key
#// - user_description
#// - user_email
#// - user_firstname
#// - user_lastname
#// - user_level
#// - user_login
#// - user_nicename
#// - user_pass
#// - user_registered
#// - user_status
#// - user_url
#// - yim
#// 
#// @since 2.8.0
#// 
#// @global object $authordata The current author's DB object.
#// 
#// @param string    $field   Optional. The user field to retrieve. Default empty.
#// @param int|false $user_id Optional. User ID.
#// @return string The author's field from the current author's DB object, otherwise an empty string.
#//
def get_the_author_meta(field="", user_id=False, *args_):
    
    original_user_id = user_id
    if (not user_id):
        global authordata
        php_check_if_defined("authordata")
        user_id = authordata.ID if (php_isset(lambda : authordata.ID)) else 0
    else:
        authordata = get_userdata(user_id)
    # end if
    if php_in_array(field, Array("login", "pass", "nicename", "email", "url", "registered", "activation_key", "status")):
        field = "user_" + field
    # end if
    value = authordata.field if (php_isset(lambda : authordata.field)) else ""
    #// 
    #// Filters the value of the requested user metadata.
    #// 
    #// The filter name is dynamic and depends on the $field parameter of the function.
    #// 
    #// @since 2.8.0
    #// @since 4.3.0 The `$original_user_id` parameter was added.
    #// 
    #// @param string    $value            The value of the metadata.
    #// @param int       $user_id          The user ID for the value.
    #// @param int|false $original_user_id The original user ID, as passed to the function.
    #//
    return apply_filters(str("get_the_author_") + str(field), value, user_id, original_user_id)
# end def get_the_author_meta
#// 
#// Outputs the field from the user's DB object. Defaults to current post's author.
#// 
#// @since 2.8.0
#// 
#// @param string    $field   Selects the field of the users record. See get_the_author_meta()
#// for the list of possible fields.
#// @param int|false $user_id Optional. User ID.
#// 
#// @see get_the_author_meta()
#//
def the_author_meta(field="", user_id=False, *args_):
    
    author_meta = get_the_author_meta(field, user_id)
    #// 
    #// The value of the requested user metadata.
    #// 
    #// The filter name is dynamic and depends on the $field parameter of the function.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string    $author_meta The value of the metadata.
    #// @param int|false $user_id     The user ID.
    #//
    php_print(apply_filters(str("the_author_") + str(field), author_meta, user_id))
# end def the_author_meta
#// 
#// Retrieve either author's link or author's name.
#// 
#// If the author has a home page set, return an HTML link, otherwise just return the
#// author's name.
#// 
#// @since 3.0.0
#// 
#// @return string|null An HTML link if the author's url exist in user meta,
#// else the result of get_the_author().
#//
def get_the_author_link(*args_):
    
    if get_the_author_meta("url"):
        return php_sprintf("<a href=\"%1$s\" title=\"%2$s\" rel=\"author external\">%3$s</a>", esc_url(get_the_author_meta("url")), esc_attr(php_sprintf(__("Visit %s&#8217;s website"), get_the_author())), get_the_author())
    else:
        return get_the_author()
    # end if
# end def get_the_author_link
#// 
#// Display either author's link or author's name.
#// 
#// If the author has a home page set, echo an HTML link, otherwise just echo the
#// author's name.
#// 
#// @link https://developer.wordpress.org/reference/functions/the_author_link
#// 
#// @since 2.1.0
#//
def the_author_link(*args_):
    
    php_print(get_the_author_link())
# end def the_author_link
#// 
#// Retrieve the number of posts by the author of the current post.
#// 
#// @since 1.5.0
#// 
#// @return int The number of posts by the author.
#//
def get_the_author_posts(*args_):
    
    post = get_post()
    if (not post):
        return 0
    # end if
    return count_user_posts(post.post_author, post.post_type)
# end def get_the_author_posts
#// 
#// Display the number of posts by the author of the current post.
#// 
#// @link https://developer.wordpress.org/reference/functions/the_author_posts
#// @since 0.71
#//
def the_author_posts(*args_):
    
    php_print(get_the_author_posts())
# end def the_author_posts
#// 
#// Retrieves an HTML link to the author page of the current post's author.
#// 
#// Returns an HTML-formatted link using get_author_posts_url().
#// 
#// @since 4.4.0
#// 
#// @global object $authordata The current author's DB object.
#// 
#// @return string An HTML link to the author page, or an empty string if $authordata isn't defined.
#//
def get_the_author_posts_link(*args_):
    
    global authordata
    php_check_if_defined("authordata")
    if (not php_is_object(authordata)):
        return ""
    # end if
    link = php_sprintf("<a href=\"%1$s\" title=\"%2$s\" rel=\"author\">%3$s</a>", esc_url(get_author_posts_url(authordata.ID, authordata.user_nicename)), esc_attr(php_sprintf(__("Posts by %s"), get_the_author())), get_the_author())
    #// 
    #// Filters the link to the author page of the author of the current post.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $link HTML link.
    #//
    return apply_filters("the_author_posts_link", link)
# end def get_the_author_posts_link
#// 
#// Displays an HTML link to the author page of the current post's author.
#// 
#// @since 1.2.0
#// @since 4.4.0 Converted into a wrapper for get_the_author_posts_link()
#// 
#// @param string $deprecated Unused.
#//
def the_author_posts_link(deprecated="", *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.1.0")
    # end if
    php_print(get_the_author_posts_link())
# end def the_author_posts_link
#// 
#// Retrieve the URL to the author page for the user with the ID provided.
#// 
#// @since 2.1.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int    $author_id       Author ID.
#// @param string $author_nicename Optional. The author's nicename (slug). Default empty.
#// @return string The URL to the author's page.
#//
def get_author_posts_url(author_id=None, author_nicename="", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    auth_ID = php_int(author_id)
    link = wp_rewrite.get_author_permastruct()
    if php_empty(lambda : link):
        file = home_url("/")
        link = file + "?author=" + auth_ID
    else:
        if "" == author_nicename:
            user = get_userdata(author_id)
            if (not php_empty(lambda : user.user_nicename)):
                author_nicename = user.user_nicename
            # end if
        # end if
        link = php_str_replace("%author%", author_nicename, link)
        link = home_url(user_trailingslashit(link))
    # end if
    #// 
    #// Filters the URL to the author's page.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $link            The URL to the author's page.
    #// @param int    $author_id       The author's id.
    #// @param string $author_nicename The author's nice name.
    #//
    link = apply_filters("author_link", link, author_id, author_nicename)
    return link
# end def get_author_posts_url
#// 
#// List all the authors of the site, with several options available.
#// 
#// @link https://developer.wordpress.org/reference/functions/wp_list_authors
#// 
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string|array $args {
#// Optional. Array or string of default arguments.
#// 
#// @type string       $orderby       How to sort the authors. Accepts 'nicename', 'email', 'url', 'registered',
#// 'user_nicename', 'user_email', 'user_url', 'user_registered', 'name',
#// 'display_name', 'post_count', 'ID', 'meta_value', 'user_login'. Default 'name'.
#// @type string       $order         Sorting direction for $orderby. Accepts 'ASC', 'DESC'. Default 'ASC'.
#// @type int          $number        Maximum authors to return or display. Default empty (all authors).
#// @type bool         $optioncount   Show the count in parenthesis next to the author's name. Default false.
#// @type bool         $exclude_admin Whether to exclude the 'admin' account, if it exists. Default true.
#// @type bool         $show_fullname Whether to show the author's full name. Default false.
#// @type bool         $hide_empty    Whether to hide any authors with no posts. Default true.
#// @type string       $feed          If not empty, show a link to the author's feed and use this text as the alt
#// parameter of the link. Default empty.
#// @type string       $feed_image    If not empty, show a link to the author's feed and use this image URL as
#// clickable anchor. Default empty.
#// @type string       $feed_type     The feed type to link to. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @type bool         $echo          Whether to output the result or instead return it. Default true.
#// @type string       $style         If 'list', each author is wrapped in an `<li>` element, otherwise the authors
#// will be separated by commas.
#// @type bool         $html          Whether to list the items in HTML form or plaintext. Default true.
#// @type array|string $exclude       Array or comma/space-separated list of author IDs to exclude. Default empty.
#// @type array|string $include       Array or comma/space-separated list of author IDs to include. Default empty.
#// }
#// @return void|string Void if 'echo' argument is true, list of authors if 'echo' is false.
#//
def wp_list_authors(args="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    defaults = Array({"orderby": "name", "order": "ASC", "number": "", "optioncount": False, "exclude_admin": True, "show_fullname": False, "hide_empty": True, "feed": "", "feed_image": "", "feed_type": "", "echo": True, "style": "list", "html": True, "exclude": "", "include": ""})
    args = wp_parse_args(args, defaults)
    return_ = ""
    query_args = wp_array_slice_assoc(args, Array("orderby", "order", "number", "exclude", "include"))
    query_args["fields"] = "ids"
    authors = get_users(query_args)
    author_count = Array()
    for row in wpdb.get_results(str("SELECT DISTINCT post_author, COUNT(ID) AS count FROM ") + str(wpdb.posts) + str(" WHERE ") + get_private_posts_cap_sql("post") + " GROUP BY post_author"):
        author_count[row.post_author] = row.count
    # end for
    for author_id in authors:
        posts = author_count[author_id] if (php_isset(lambda : author_count[author_id])) else 0
        if (not posts) and args["hide_empty"]:
            continue
        # end if
        author = get_userdata(author_id)
        if args["exclude_admin"] and "admin" == author.display_name:
            continue
        # end if
        if args["show_fullname"] and author.first_name and author.last_name:
            name = str(author.first_name) + str(" ") + str(author.last_name)
        else:
            name = author.display_name
        # end if
        if (not args["html"]):
            return_ += name + ", "
            continue
            pass
        # end if
        if "list" == args["style"]:
            return_ += "<li>"
        # end if
        link = php_sprintf("<a href=\"%1$s\" title=\"%2$s\">%3$s</a>", get_author_posts_url(author.ID, author.user_nicename), esc_attr(php_sprintf(__("Posts by %s"), author.display_name)), name)
        if (not php_empty(lambda : args["feed_image"])) or (not php_empty(lambda : args["feed"])):
            link += " "
            if php_empty(lambda : args["feed_image"]):
                link += "("
            # end if
            link += "<a href=\"" + get_author_feed_link(author.ID, args["feed_type"]) + "\""
            alt = ""
            if (not php_empty(lambda : args["feed"])):
                alt = " alt=\"" + esc_attr(args["feed"]) + "\""
                name = args["feed"]
            # end if
            link += ">"
            if (not php_empty(lambda : args["feed_image"])):
                link += "<img src=\"" + esc_url(args["feed_image"]) + "\" style=\"border: none;\"" + alt + " />"
            else:
                link += name
            # end if
            link += "</a>"
            if php_empty(lambda : args["feed_image"]):
                link += ")"
            # end if
        # end if
        if args["optioncount"]:
            link += " (" + posts + ")"
        # end if
        return_ += link
        return_ += "</li>" if "list" == args["style"] else ", "
    # end for
    return_ = php_rtrim(return_, ", ")
    if args["echo"]:
        php_print(return_)
    else:
        return return_
    # end if
# end def wp_list_authors
#// 
#// Determines whether this site has more than one author.
#// 
#// Checks to see if more than one author has published posts.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return bool Whether or not we have more than one author
#//
def is_multi_author(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    is_multi_author = get_transient("is_multi_author")
    if False == is_multi_author:
        rows = wpdb.get_col(str("SELECT DISTINCT post_author FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'post' AND post_status = 'publish' LIMIT 2"))
        is_multi_author = 1 if 1 < php_count(rows) else 0
        set_transient("is_multi_author", is_multi_author)
    # end if
    #// 
    #// Filters whether the site has more than one author with published posts.
    #// 
    #// @since 3.2.0
    #// 
    #// @param bool $is_multi_author Whether $is_multi_author should evaluate as true.
    #//
    return apply_filters("is_multi_author", php_bool(is_multi_author))
# end def is_multi_author
#// 
#// Helper function to clear the cache for number of authors.
#// 
#// @since 3.2.0
#// @access private
#//
def __clear_multi_author_cache(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    delete_transient("is_multi_author")
# end def __clear_multi_author_cache
