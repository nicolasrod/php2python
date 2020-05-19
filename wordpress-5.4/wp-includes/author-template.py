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
def get_the_author(deprecated_="", *_args_):
    
    
    global authordata_
    php_check_if_defined("authordata_")
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.1.0")
    # end if
    #// 
    #// Filters the display name of the current post's author.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $authordata->display_name The author's display name.
    #//
    return apply_filters("the_author", authordata_.display_name if php_is_object(authordata_) else None)
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
def the_author(deprecated_="", deprecated_echo_=None, *_args_):
    if deprecated_echo_ is None:
        deprecated_echo_ = True
    # end if
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.1.0")
    # end if
    if True != deprecated_echo_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "1.5.0", php_sprintf(__("Use %s instead if you do not want the value echoed."), "<code>get_the_author()</code>"))
    # end if
    if deprecated_echo_:
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
def get_the_modified_author(*_args_):
    
    
    last_id_ = get_post_meta(get_post().ID, "_edit_last", True)
    if last_id_:
        last_user_ = get_userdata(last_id_)
        #// 
        #// Filters the display name of the author who last edited the current post.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $last_user->display_name The author's display name.
        #//
        return apply_filters("the_modified_author", last_user_.display_name)
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
def the_modified_author(*_args_):
    
    
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
def get_the_author_meta(field_="", user_id_=None, *_args_):
    if user_id_ is None:
        user_id_ = False
    # end if
    
    original_user_id_ = user_id_
    if (not user_id_):
        global authordata_
        php_check_if_defined("authordata_")
        user_id_ = authordata_.ID if (php_isset(lambda : authordata_.ID)) else 0
    else:
        authordata_ = get_userdata(user_id_)
    # end if
    if php_in_array(field_, Array("login", "pass", "nicename", "email", "url", "registered", "activation_key", "status")):
        field_ = "user_" + field_
    # end if
    value_ = authordata_.field_ if (php_isset(lambda : authordata_.field_)) else ""
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
    return apply_filters(str("get_the_author_") + str(field_), value_, user_id_, original_user_id_)
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
def the_author_meta(field_="", user_id_=None, *_args_):
    if user_id_ is None:
        user_id_ = False
    # end if
    
    author_meta_ = get_the_author_meta(field_, user_id_)
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
    php_print(apply_filters(str("the_author_") + str(field_), author_meta_, user_id_))
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
def get_the_author_link(*_args_):
    
    
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
def the_author_link(*_args_):
    
    
    php_print(get_the_author_link())
# end def the_author_link
#// 
#// Retrieve the number of posts by the author of the current post.
#// 
#// @since 1.5.0
#// 
#// @return int The number of posts by the author.
#//
def get_the_author_posts(*_args_):
    
    
    post_ = get_post()
    if (not post_):
        return 0
    # end if
    return count_user_posts(post_.post_author, post_.post_type)
# end def get_the_author_posts
#// 
#// Display the number of posts by the author of the current post.
#// 
#// @link https://developer.wordpress.org/reference/functions/the_author_posts
#// @since 0.71
#//
def the_author_posts(*_args_):
    
    
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
def get_the_author_posts_link(*_args_):
    
    
    global authordata_
    php_check_if_defined("authordata_")
    if (not php_is_object(authordata_)):
        return ""
    # end if
    link_ = php_sprintf("<a href=\"%1$s\" title=\"%2$s\" rel=\"author\">%3$s</a>", esc_url(get_author_posts_url(authordata_.ID, authordata_.user_nicename)), esc_attr(php_sprintf(__("Posts by %s"), get_the_author())), get_the_author())
    #// 
    #// Filters the link to the author page of the author of the current post.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $link HTML link.
    #//
    return apply_filters("the_author_posts_link", link_)
# end def get_the_author_posts_link
#// 
#// Displays an HTML link to the author page of the current post's author.
#// 
#// @since 1.2.0
#// @since 4.4.0 Converted into a wrapper for get_the_author_posts_link()
#// 
#// @param string $deprecated Unused.
#//
def the_author_posts_link(deprecated_="", *_args_):
    
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.1.0")
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
def get_author_posts_url(author_id_=None, author_nicename_="", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    auth_ID_ = php_int(author_id_)
    link_ = wp_rewrite_.get_author_permastruct()
    if php_empty(lambda : link_):
        file_ = home_url("/")
        link_ = file_ + "?author=" + auth_ID_
    else:
        if "" == author_nicename_:
            user_ = get_userdata(author_id_)
            if (not php_empty(lambda : user_.user_nicename)):
                author_nicename_ = user_.user_nicename
            # end if
        # end if
        link_ = php_str_replace("%author%", author_nicename_, link_)
        link_ = home_url(user_trailingslashit(link_))
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
    link_ = apply_filters("author_link", link_, author_id_, author_nicename_)
    return link_
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
def wp_list_authors(args_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    defaults_ = Array({"orderby": "name", "order": "ASC", "number": "", "optioncount": False, "exclude_admin": True, "show_fullname": False, "hide_empty": True, "feed": "", "feed_image": "", "feed_type": "", "echo": True, "style": "list", "html": True, "exclude": "", "include": ""})
    args_ = wp_parse_args(args_, defaults_)
    return_ = ""
    query_args_ = wp_array_slice_assoc(args_, Array("orderby", "order", "number", "exclude", "include"))
    query_args_["fields"] = "ids"
    authors_ = get_users(query_args_)
    author_count_ = Array()
    for row_ in wpdb_.get_results(str("SELECT DISTINCT post_author, COUNT(ID) AS count FROM ") + str(wpdb_.posts) + str(" WHERE ") + get_private_posts_cap_sql("post") + " GROUP BY post_author"):
        author_count_[row_.post_author] = row_.count
    # end for
    for author_id_ in authors_:
        posts_ = author_count_[author_id_] if (php_isset(lambda : author_count_[author_id_])) else 0
        if (not posts_) and args_["hide_empty"]:
            continue
        # end if
        author_ = get_userdata(author_id_)
        if args_["exclude_admin"] and "admin" == author_.display_name:
            continue
        # end if
        if args_["show_fullname"] and author_.first_name and author_.last_name:
            name_ = str(author_.first_name) + str(" ") + str(author_.last_name)
        else:
            name_ = author_.display_name
        # end if
        if (not args_["html"]):
            return_ += name_ + ", "
            continue
            pass
        # end if
        if "list" == args_["style"]:
            return_ += "<li>"
        # end if
        link_ = php_sprintf("<a href=\"%1$s\" title=\"%2$s\">%3$s</a>", get_author_posts_url(author_.ID, author_.user_nicename), esc_attr(php_sprintf(__("Posts by %s"), author_.display_name)), name_)
        if (not php_empty(lambda : args_["feed_image"])) or (not php_empty(lambda : args_["feed"])):
            link_ += " "
            if php_empty(lambda : args_["feed_image"]):
                link_ += "("
            # end if
            link_ += "<a href=\"" + get_author_feed_link(author_.ID, args_["feed_type"]) + "\""
            alt_ = ""
            if (not php_empty(lambda : args_["feed"])):
                alt_ = " alt=\"" + esc_attr(args_["feed"]) + "\""
                name_ = args_["feed"]
            # end if
            link_ += ">"
            if (not php_empty(lambda : args_["feed_image"])):
                link_ += "<img src=\"" + esc_url(args_["feed_image"]) + "\" style=\"border: none;\"" + alt_ + " />"
            else:
                link_ += name_
            # end if
            link_ += "</a>"
            if php_empty(lambda : args_["feed_image"]):
                link_ += ")"
            # end if
        # end if
        if args_["optioncount"]:
            link_ += " (" + posts_ + ")"
        # end if
        return_ += link_
        return_ += "</li>" if "list" == args_["style"] else ", "
    # end for
    return_ = php_rtrim(return_, ", ")
    if args_["echo"]:
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
def is_multi_author(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    is_multi_author_ = get_transient("is_multi_author")
    if False == is_multi_author_:
        rows_ = wpdb_.get_col(str("SELECT DISTINCT post_author FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'post' AND post_status = 'publish' LIMIT 2"))
        is_multi_author_ = 1 if 1 < php_count(rows_) else 0
        set_transient("is_multi_author", is_multi_author_)
    # end if
    #// 
    #// Filters whether the site has more than one author with published posts.
    #// 
    #// @since 3.2.0
    #// 
    #// @param bool $is_multi_author Whether $is_multi_author should evaluate as true.
    #//
    return apply_filters("is_multi_author", php_bool(is_multi_author_))
# end def is_multi_author
#// 
#// Helper function to clear the cache for number of authors.
#// 
#// @since 3.2.0
#// @access private
#//
def __clear_multi_author_cache(*_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    delete_transient("is_multi_author")
# end def __clear_multi_author_cache
