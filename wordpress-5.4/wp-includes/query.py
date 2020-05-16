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
#// WordPress Query API
#// 
#// The query API attempts to get which part of WordPress the user is on. It
#// also provides functionality for getting URL query information.
#// 
#// @link https://developer.wordpress.org/themes/basics/the-loop/ More information on The Loop.
#// 
#// @package WordPress
#// @subpackage Query
#// 
#// 
#// Retrieve variable in the WP_Query class.
#// 
#// @since 1.5.0
#// @since 3.9.0 The `$default` argument was introduced.
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string $var       The variable key to retrieve.
#// @param mixed  $default   Optional. Value to return if the query variable is not set. Default empty.
#// @return mixed Contents of the query variable.
#//
def get_query_var(var=None, default="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.get(var, default)
# end def get_query_var
#// 
#// Retrieve the currently-queried object.
#// 
#// Wrapper for WP_Query::get_queried_object().
#// 
#// @since 3.1.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return object Queried object.
#//
def get_queried_object(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.get_queried_object()
# end def get_queried_object
#// 
#// Retrieve ID of the current queried object.
#// 
#// Wrapper for WP_Query::get_queried_object_id().
#// 
#// @since 3.1.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return int ID of the queried object.
#//
def get_queried_object_id(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.get_queried_object_id()
# end def get_queried_object_id
#// 
#// Set query variable.
#// 
#// @since 2.2.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string $var   Query variable key.
#// @param mixed  $value Query variable value.
#//
def set_query_var(var=None, value=None, *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    wp_query.set(var, value)
# end def set_query_var
#// 
#// Sets up The Loop with query parameters.
#// 
#// Note: This function will completely override the main query and isn't intended for use
#// by plugins or themes. Its overly-simplistic approach to modifying the main query can be
#// problematic and should be avoided wherever possible. In most cases, there are better,
#// more performant options for modifying the main query such as via the {@see 'pre_get_posts'}
#// action within WP_Query.
#// 
#// This must not be used within the WordPress Loop.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param array|string $query Array or string of WP_Query arguments.
#// @return WP_Post[]|int[] Array of post objects or post IDs.
#//
def query_posts(query=None, *args_):
    global PHP_GLOBALS
    PHP_GLOBALS["wp_query"] = php_new_class("WP_Query", lambda : WP_Query())
    return PHP_GLOBALS["wp_query"].query(query)
# end def query_posts
#// 
#// Destroys the previous query and sets up a new query.
#// 
#// This should be used after query_posts() and before another query_posts().
#// This will remove obscure bugs that occur when the previous WP_Query object
#// is not destroyed properly before another is set up.
#// 
#// @since 2.3.0
#// 
#// @global WP_Query $wp_query     WordPress Query object.
#// @global WP_Query $wp_the_query Copy of the global WP_Query instance created during wp_reset_query().
#//
def wp_reset_query(*args_):
    global PHP_GLOBALS
    PHP_GLOBALS["wp_query"] = PHP_GLOBALS["wp_the_query"]
    wp_reset_postdata()
# end def wp_reset_query
#// 
#// After looping through a separate query, this function restores
#// the $post global to the current post in the main query.
#// 
#// @since 3.0.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#//
def wp_reset_postdata(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (php_isset(lambda : wp_query)):
        wp_query.reset_postdata()
    # end if
# end def wp_reset_postdata
#// 
#// Query type checks.
#// 
#// 
#// Determines whether the query is for an existing archive page.
#// 
#// Month, Year, Category, Author, Post Type archive...
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_archive(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_archive()
# end def is_archive
#// 
#// Determines whether the query is for an existing post type archive page.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.1.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string|string[] $post_types Optional. Post type or array of posts types
#// to check against. Default empty.
#// @return bool
#//
def is_post_type_archive(post_types="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_post_type_archive(post_types)
# end def is_post_type_archive
#// 
#// Determines whether the query is for an existing attachment page.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.0.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param int|string|int[]|string[] $attachment Optional. Attachment ID, title, slug, or array of such
#// to check against. Default empty.
#// @return bool
#//
def is_attachment(attachment="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_attachment(attachment)
# end def is_attachment
#// 
#// Determines whether the query is for an existing author archive page.
#// 
#// If the $author parameter is specified, this function will additionally
#// check if the query is for one of the authors specified.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param int|string|int[]|string[] $author Optional. User ID, nickname, nicename, or array of such
#// to check against. Default empty.
#// @return bool
#//
def is_author(author="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_author(author)
# end def is_author
#// 
#// Determines whether the query is for an existing category archive page.
#// 
#// If the $category parameter is specified, this function will additionally
#// check if the query is for one of the categories specified.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param int|string|int[]|string[] $category Optional. Category ID, name, slug, or array of such
#// to check against. Default empty.
#// @return bool
#//
def is_category(category="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_category(category)
# end def is_category
#// 
#// Determines whether the query is for an existing tag archive page.
#// 
#// If the $tag parameter is specified, this function will additionally
#// check if the query is for one of the tags specified.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.3.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param int|string|int[]|string[] $tag Optional. Tag ID, name, slug, or array of such
#// to check against. Default empty.
#// @return bool
#//
def is_tag(tag="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_tag(tag)
# end def is_tag
#// 
#// Determines whether the query is for an existing custom taxonomy archive page.
#// 
#// If the $taxonomy parameter is specified, this function will additionally
#// check if the query is for that specific $taxonomy.
#// 
#// If the $term parameter is specified in addition to the $taxonomy parameter,
#// this function will additionally check if the query is for one of the terms
#// specified.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string|string[]           $taxonomy Optional. Taxonomy slug or slugs to check against.
#// Default empty.
#// @param int|string|int[]|string[] $term     Optional. Term ID, name, slug, or array of such
#// to check against. Default empty.
#// @return bool True for custom taxonomy archive pages, false for built-in taxonomies
#// (category and tag archives).
#//
def is_tax(taxonomy="", term="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_tax(taxonomy, term)
# end def is_tax
#// 
#// Determines whether the query is for an existing date archive.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_date(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_date()
# end def is_date
#// 
#// Determines whether the query is for an existing day archive.
#// 
#// A conditional check to test whether the page is a date-based archive page displaying posts for the current day.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_day(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_day()
# end def is_day
#// 
#// Determines whether the query is for a feed.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string|string[] $feeds Optional. Feed type or array of feed types
#// to check against. Default empty.
#// @return bool
#//
def is_feed(feeds="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_feed(feeds)
# end def is_feed
#// 
#// Is the query for a comments feed?
#// 
#// @since 3.0.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_comment_feed(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_comment_feed()
# end def is_comment_feed
#// 
#// Determines whether the query is for the front page of the site.
#// 
#// This is for what is displayed at your site's main URL.
#// 
#// Depends on the site's "Front page displays" Reading Settings 'show_on_front' and 'page_on_front'.
#// 
#// If you set a static page for the front page of your site, this function will return
#// true when viewing that page.
#// 
#// Otherwise the same as @see is_home()
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool True, if front of site.
#//
def is_front_page(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_front_page()
# end def is_front_page
#// 
#// Determines whether the query is for the blog homepage.
#// 
#// The blog homepage is the page that shows the time-based blog content of the site.
#// 
#// is_home() is dependent on the site's "Front page displays" Reading Settings 'show_on_front'
#// and 'page_for_posts'.
#// 
#// If a static page is set for the front page of the site, this function will return true only
#// on the page you set as the "Posts page".
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @see is_front_page()
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool True if blog view homepage, otherwise false.
#//
def is_home(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_home()
# end def is_home
#// 
#// Determines whether the query is for the Privacy Policy page.
#// 
#// The Privacy Policy page is the page that shows the Privacy Policy content of the site.
#// 
#// is_privacy_policy() is dependent on the site's "Change your Privacy Policy page" Privacy Settings 'wp_page_for_privacy_policy'.
#// 
#// This function will return true only on the page you set as the "Privacy Policy page".
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 5.2.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_privacy_policy(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_privacy_policy()
# end def is_privacy_policy
#// 
#// Determines whether the query is for an existing month archive.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_month(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_month()
# end def is_month
#// 
#// Determines whether the query is for an existing single page.
#// 
#// If the $page parameter is specified, this function will additionally
#// check if the query is for one of the pages specified.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @see is_single()
#// @see is_singular()
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param int|string|int[]|string[] $page Optional. Page ID, title, slug, or array of such
#// to check against. Default empty.
#// @return bool Whether the query is for an existing single page.
#//
def is_page(page="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_page(page)
# end def is_page
#// 
#// Determines whether the query is for paged results and not for the first page.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_paged(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_paged()
# end def is_paged
#// 
#// Determines whether the query is for a post or page preview.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.0.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_preview(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_preview()
# end def is_preview
#// 
#// Is the query for the robots.txt file?
#// 
#// @since 2.1.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_robots(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_robots()
# end def is_robots
#// 
#// Is the query for the favicon.ico file?
#// 
#// @since 5.4.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_favicon(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_favicon()
# end def is_favicon
#// 
#// Determines whether the query is for a search.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_search(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_search()
# end def is_search
#// 
#// Determines whether the query is for an existing single post.
#// 
#// Works for any post type, except attachments and pages
#// 
#// If the $post parameter is specified, this function will additionally
#// check if the query is for one of the Posts specified.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @see is_page()
#// @see is_singular()
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param int|string|int[]|string[] $post Optional. Post ID, title, slug, or array of such
#// to check against. Default empty.
#// @return bool Whether the query is for an existing single post.
#//
def is_single(post="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_single(post)
# end def is_single
#// 
#// Determines whether the query is for an existing single post of any post type
#// (post, attachment, page, custom post types).
#// 
#// If the $post_types parameter is specified, this function will additionally
#// check if the query is for one of the Posts Types specified.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @see is_page()
#// @see is_single()
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string|string[] $post_types Optional. Post type or array of post types
#// to check against. Default empty.
#// @return bool Whether the query is for an existing single post
#// or any of the given post types.
#//
def is_singular(post_types="", *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_singular(post_types)
# end def is_singular
#// 
#// Determines whether the query is for a specific time.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_time(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_time()
# end def is_time
#// 
#// Determines whether the query is for a trackback endpoint call.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_trackback(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_trackback()
# end def is_trackback
#// 
#// Determines whether the query is for an existing year archive.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_year(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_year()
# end def is_year
#// 
#// Determines whether the query has resulted in a 404 (returns no results).
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_404(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_404()
# end def is_404
#// 
#// Is the query for an embedded post?
#// 
#// @since 4.4.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool Whether we're in an embedded post or not.
#//
def is_embed(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not (php_isset(lambda : wp_query))):
        _doing_it_wrong(__FUNCTION__, __("Conditional query tags do not work before the query is run. Before then, they always return false."), "3.1.0")
        return False
    # end if
    return wp_query.is_embed()
# end def is_embed
#// 
#// Determines whether the query is the main query.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.3.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def is_main_query(*args_):
    
    if "pre_get_posts" == current_filter():
        message = php_sprintf(__("In %1$s, use the %2$s method, not the %3$s function. See %4$s."), "<code>pre_get_posts</code>", "<code>WP_Query->is_main_query()</code>", "<code>is_main_query()</code>", __("https://codex.wordpress.org/Function_Reference/is_main_query"))
        _doing_it_wrong(__FUNCTION__, message, "3.7.0")
    # end if
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.is_main_query()
# end def is_main_query
#// 
#// The Loop. Post loop control.
#// 
#// 
#// Whether current WordPress query has results to loop over.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def have_posts(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.have_posts()
# end def have_posts
#// 
#// Determines whether the caller is in the Loop.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.0.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool True if caller is within loop, false if loop hasn't started or ended.
#//
def in_the_loop(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.in_the_loop
# end def in_the_loop
#// 
#// Rewind the loop posts.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#//
def rewind_posts(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    wp_query.rewind_posts()
# end def rewind_posts
#// 
#// Iterate the post index in the loop.
#// 
#// @since 1.5.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#//
def the_post(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    wp_query.the_post()
# end def the_post
#// 
#// Comments loop.
#// 
#// 
#// Whether there are comments to loop over.
#// 
#// @since 2.2.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return bool
#//
def have_comments(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.have_comments()
# end def have_comments
#// 
#// Iterate comment index in the comment loop.
#// 
#// @since 2.2.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @return object
#//
def the_comment(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return wp_query.the_comment()
# end def the_comment
#// 
#// Redirect old slugs to the correct permalink.
#// 
#// Attempts to find the current slug from the past slugs.
#// 
#// @since 2.1.0
#//
def wp_old_slug_redirect(*args_):
    
    if is_404() and "" != get_query_var("name"):
        #// Guess the current post type based on the query vars.
        if get_query_var("post_type"):
            post_type = get_query_var("post_type")
        elif get_query_var("attachment"):
            post_type = "attachment"
        elif get_query_var("pagename"):
            post_type = "page"
        else:
            post_type = "post"
        # end if
        if php_is_array(post_type):
            if php_count(post_type) > 1:
                return
            # end if
            post_type = reset(post_type)
        # end if
        #// Do not attempt redirect for hierarchical post types.
        if is_post_type_hierarchical(post_type):
            return
        # end if
        id = _find_post_by_old_slug(post_type)
        if (not id):
            id = _find_post_by_old_date(post_type)
        # end if
        #// 
        #// Filters the old slug redirect post ID.
        #// 
        #// @since 4.9.3
        #// 
        #// @param int $id The redirect post ID.
        #//
        id = apply_filters("old_slug_redirect_post_id", id)
        if (not id):
            return
        # end if
        link = get_permalink(id)
        if get_query_var("paged") > 1:
            link = user_trailingslashit(trailingslashit(link) + "page/" + get_query_var("paged"))
        elif is_embed():
            link = user_trailingslashit(trailingslashit(link) + "embed")
        # end if
        #// 
        #// Filters the old slug redirect URL.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $link The redirect URL.
        #//
        link = apply_filters("old_slug_redirect_url", link)
        if (not link):
            return
        # end if
        wp_redirect(link, 301)
        #// Permanent redirect.
        php_exit(0)
    # end if
# end def wp_old_slug_redirect
#// 
#// Find the post ID for redirecting an old slug.
#// 
#// @see wp_old_slug_redirect()
#// 
#// @since 4.9.3
#// @access private
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $post_type The current post type based on the query vars.
#// @return int $id The Post ID.
#//
def _find_post_by_old_slug(post_type=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    query = wpdb.prepare(str("SELECT post_id FROM ") + str(wpdb.postmeta) + str(", ") + str(wpdb.posts) + str(" WHERE ID = post_id AND post_type = %s AND meta_key = '_wp_old_slug' AND meta_value = %s"), post_type, get_query_var("name"))
    #// If year, monthnum, or day have been specified, make our query more precise
    #// just in case there are multiple identical _wp_old_slug values.
    if get_query_var("year"):
        query += wpdb.prepare(" AND YEAR(post_date) = %d", get_query_var("year"))
    # end if
    if get_query_var("monthnum"):
        query += wpdb.prepare(" AND MONTH(post_date) = %d", get_query_var("monthnum"))
    # end if
    if get_query_var("day"):
        query += wpdb.prepare(" AND DAYOFMONTH(post_date) = %d", get_query_var("day"))
    # end if
    id = php_int(wpdb.get_var(query))
    return id
# end def _find_post_by_old_slug
#// 
#// Find the post ID for redirecting an old date.
#// 
#// @see wp_old_slug_redirect()
#// 
#// @since 4.9.3
#// @access private
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $post_type The current post type based on the query vars.
#// @return int $id The Post ID.
#//
def _find_post_by_old_date(post_type=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    date_query = ""
    if get_query_var("year"):
        date_query += wpdb.prepare(" AND YEAR(pm_date.meta_value) = %d", get_query_var("year"))
    # end if
    if get_query_var("monthnum"):
        date_query += wpdb.prepare(" AND MONTH(pm_date.meta_value) = %d", get_query_var("monthnum"))
    # end if
    if get_query_var("day"):
        date_query += wpdb.prepare(" AND DAYOFMONTH(pm_date.meta_value) = %d", get_query_var("day"))
    # end if
    id = 0
    if date_query:
        id = php_int(wpdb.get_var(wpdb.prepare(str("SELECT post_id FROM ") + str(wpdb.postmeta) + str(" AS pm_date, ") + str(wpdb.posts) + str(" WHERE ID = post_id AND post_type = %s AND meta_key = '_wp_old_date' AND post_name = %s") + date_query, post_type, get_query_var("name"))))
        if (not id):
            #// Check to see if an old slug matches the old date.
            id = php_int(wpdb.get_var(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(", ") + str(wpdb.postmeta) + str(" AS pm_slug, ") + str(wpdb.postmeta) + str(" AS pm_date WHERE ID = pm_slug.post_id AND ID = pm_date.post_id AND post_type = %s AND pm_slug.meta_key = '_wp_old_slug' AND pm_slug.meta_value = %s AND pm_date.meta_key = '_wp_old_date'") + date_query, post_type, get_query_var("name"))))
        # end if
    # end if
    return id
# end def _find_post_by_old_date
#// 
#// Set up global post data.
#// 
#// @since 1.5.0
#// @since 4.4.0 Added the ability to pass a post ID to `$post`.
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param WP_Post|object|int $post WP_Post instance or Post ID/object.
#// @return bool True when finished.
#//
def setup_postdata(post=None, *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not php_empty(lambda : wp_query)) and type(wp_query).__name__ == "WP_Query":
        return wp_query.setup_postdata(post)
    # end if
    return False
# end def setup_postdata
#// 
#// Generates post data.
#// 
#// @since 5.2.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param WP_Post|object|int $post WP_Post instance or Post ID/object.
#// @return array|bool Elements of post, or false on failure.
#//
def generate_postdata(post=None, *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not php_empty(lambda : wp_query)) and type(wp_query).__name__ == "WP_Query":
        return wp_query.generate_postdata(post)
    # end if
    return False
# end def generate_postdata
