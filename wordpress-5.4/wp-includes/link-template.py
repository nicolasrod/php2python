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
#// WordPress Link Template Functions
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// Displays the permalink for the current post.
#// 
#// @since 1.2.0
#// @since 4.4.0 Added the `$post` parameter.
#// 
#// @param int|WP_Post $post Optional. Post ID or post object. Default is the global `$post`.
#//
def the_permalink(post=0, *args_):
    
    #// 
    #// Filters the display of the permalink for the current post.
    #// 
    #// @since 1.5.0
    #// @since 4.4.0 Added the `$post` parameter.
    #// 
    #// @param string      $permalink The permalink for the current post.
    #// @param int|WP_Post $post      Post ID, WP_Post object, or 0. Default 0.
    #//
    php_print(esc_url(apply_filters("the_permalink", get_permalink(post), post)))
# end def the_permalink
#// 
#// Retrieves a trailing-slashed string if the site is set for adding trailing slashes.
#// 
#// Conditionally adds a trailing slash if the permalink structure has a trailing
#// slash, strips the trailing slash if not. The string is passed through the
#// {@see 'user_trailingslashit'} filter. Will remove trailing slash from string, if
#// site is not set to have them.
#// 
#// @since 2.2.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $string      URL with or without a trailing slash.
#// @param string $type_of_url Optional. The type of URL being considered (e.g. single, category, etc)
#// for use in the filter. Default empty string.
#// @return string The URL with the trailing slash appended or stripped.
#//
def user_trailingslashit(string=None, type_of_url="", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if wp_rewrite.use_trailing_slashes:
        string = trailingslashit(string)
    else:
        string = untrailingslashit(string)
    # end if
    #// 
    #// Filters the trailing-slashed string, depending on whether the site is set to use trailing slashes.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $string      URL with or without a trailing slash.
    #// @param string $type_of_url The type of URL being considered. Accepts 'single', 'single_trackback',
    #// 'single_feed', 'single_paged', 'commentpaged', 'paged', 'home', 'feed',
    #// 'category', 'page', 'year', 'month', 'day', 'post_type_archive'.
    #//
    return apply_filters("user_trailingslashit", string, type_of_url)
# end def user_trailingslashit
#// 
#// Displays the permalink anchor for the current post.
#// 
#// The permalink mode title will use the post title for the 'a' element 'id'
#// attribute. The id mode uses 'post-' with the post ID for the 'id' attribute.
#// 
#// @since 0.71
#// 
#// @param string $mode Optional. Permalink mode. Accepts 'title' or 'id'. Default 'id'.
#//
def permalink_anchor(mode="id", *args_):
    
    post = get_post()
    for case in Switch(php_strtolower(mode)):
        if case("title"):
            title = sanitize_title(post.post_title) + "-" + post.ID
            php_print("<a id=\"" + title + "\"></a>")
            break
        # end if
        if case("id"):
            pass
        # end if
        if case():
            php_print("<a id=\"post-" + post.ID + "\"></a>")
            break
        # end if
    # end for
# end def permalink_anchor
#// 
#// Retrieves the full permalink for the current post or post ID.
#// 
#// This function is an alias for get_permalink().
#// 
#// @since 3.9.0
#// 
#// @see get_permalink()
#// 
#// @param int|WP_Post $post      Optional. Post ID or post object. Default is the global `$post`.
#// @param bool        $leavename Optional. Whether to keep post name or page name. Default false.
#// 
#// @return string|false The permalink URL or false if post does not exist.
#//
def get_the_permalink(post=0, leavename=False, *args_):
    
    return get_permalink(post, leavename)
# end def get_the_permalink
#// 
#// Retrieves the full permalink for the current post or post ID.
#// 
#// @since 1.0.0
#// 
#// @param int|WP_Post $post      Optional. Post ID or post object. Default is the global `$post`.
#// @param bool        $leavename Optional. Whether to keep post name or page name. Default false.
#// @return string|false The permalink URL or false if post does not exist.
#//
def get_permalink(post=0, leavename=False, *args_):
    
    rewritecode = Array("%year%", "%monthnum%", "%day%", "%hour%", "%minute%", "%second%", "" if leavename else "%postname%", "%post_id%", "%category%", "%author%", "" if leavename else "%pagename%")
    if php_is_object(post) and (php_isset(lambda : post.filter)) and "sample" == post.filter:
        sample = True
    else:
        post = get_post(post)
        sample = False
    # end if
    if php_empty(lambda : post.ID):
        return False
    # end if
    if "page" == post.post_type:
        return get_page_link(post, leavename, sample)
    elif "attachment" == post.post_type:
        return get_attachment_link(post, leavename)
    elif php_in_array(post.post_type, get_post_types(Array({"_builtin": False}))):
        return get_post_permalink(post, leavename, sample)
    # end if
    permalink = get_option("permalink_structure")
    #// 
    #// Filters the permalink structure for a post before token replacement occurs.
    #// 
    #// Only applies to posts with post_type of 'post'.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string  $permalink The site's permalink structure.
    #// @param WP_Post $post      The post in question.
    #// @param bool    $leavename Whether to keep the post name.
    #//
    permalink = apply_filters("pre_post_link", permalink, post, leavename)
    if "" != permalink and (not php_in_array(post.post_status, Array("draft", "pending", "auto-draft", "future"))):
        category = ""
        if php_strpos(permalink, "%category%") != False:
            cats = get_the_category(post.ID)
            if cats:
                cats = wp_list_sort(cats, Array({"term_id": "ASC"}))
                #// 
                #// Filters the category that gets used in the %category% permalink token.
                #// 
                #// @since 3.5.0
                #// 
                #// @param WP_Term  $cat  The category to use in the permalink.
                #// @param array    $cats Array of all categories (WP_Term objects) associated with the post.
                #// @param WP_Post  $post The post in question.
                #//
                category_object = apply_filters("post_link_category", cats[0], cats, post)
                category_object = get_term(category_object, "category")
                category = category_object.slug
                if category_object.parent:
                    category = get_category_parents(category_object.parent, False, "/", True) + category
                # end if
            # end if
            #// Show default category in permalinks,
            #// without having to assign it explicitly.
            if php_empty(lambda : category):
                default_category = get_term(get_option("default_category"), "category")
                if default_category and (not is_wp_error(default_category)):
                    category = default_category.slug
                # end if
            # end if
        # end if
        author = ""
        if php_strpos(permalink, "%author%") != False:
            authordata = get_userdata(post.post_author)
            author = authordata.user_nicename
        # end if
        #// This is not an API call because the permalink is based on the stored post_date value,
        #// which should be parsed as local time regardless of the default PHP timezone.
        date = php_explode(" ", php_str_replace(Array("-", ":"), " ", post.post_date))
        rewritereplace = Array(date[0], date[1], date[2], date[3], date[4], date[5], post.post_name, post.ID, category, author, post.post_name)
        permalink = home_url(php_str_replace(rewritecode, rewritereplace, permalink))
        permalink = user_trailingslashit(permalink, "single")
    else:
        #// If they're not using the fancy permalink option.
        permalink = home_url("?p=" + post.ID)
    # end if
    #// 
    #// Filters the permalink for a post.
    #// 
    #// Only applies to posts with post_type of 'post'.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $permalink The post's permalink.
    #// @param WP_Post $post      The post in question.
    #// @param bool    $leavename Whether to keep the post name.
    #//
    return apply_filters("post_link", permalink, post, leavename)
# end def get_permalink
#// 
#// Retrieves the permalink for a post of a custom post type.
#// 
#// @since 3.0.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int|WP_Post $id        Optional. Post ID or post object. Default is the global `$post`.
#// @param bool        $leavename Optional, defaults to false. Whether to keep post name. Default false.
#// @param bool        $sample    Optional, defaults to false. Is it a sample permalink. Default false.
#// @return string|WP_Error The post permalink.
#//
def get_post_permalink(id=0, leavename=False, sample=False, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    post = get_post(id)
    if is_wp_error(post):
        return post
    # end if
    post_link = wp_rewrite.get_extra_permastruct(post.post_type)
    slug = post.post_name
    draft_or_pending = get_post_status(post) and php_in_array(get_post_status(post), Array("draft", "pending", "auto-draft", "future"))
    post_type = get_post_type_object(post.post_type)
    if post_type.hierarchical:
        slug = get_page_uri(post)
    # end if
    if (not php_empty(lambda : post_link)) and (not draft_or_pending) or sample:
        if (not leavename):
            post_link = php_str_replace(str("%") + str(post.post_type) + str("%"), slug, post_link)
        # end if
        post_link = home_url(user_trailingslashit(post_link))
    else:
        if post_type.query_var and (php_isset(lambda : post.post_status)) and (not draft_or_pending):
            post_link = add_query_arg(post_type.query_var, slug, "")
        else:
            post_link = add_query_arg(Array({"post_type": post.post_type, "p": post.ID}), "")
        # end if
        post_link = home_url(post_link)
    # end if
    #// 
    #// Filters the permalink for a post of a custom post type.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string  $post_link The post's permalink.
    #// @param WP_Post $post      The post in question.
    #// @param bool    $leavename Whether to keep the post name.
    #// @param bool    $sample    Is it a sample permalink.
    #//
    return apply_filters("post_type_link", post_link, post, leavename, sample)
# end def get_post_permalink
#// 
#// Retrieves the permalink for the current page or page ID.
#// 
#// Respects page_on_front. Use this one.
#// 
#// @since 1.5.0
#// 
#// @param int|WP_Post $post      Optional. Post ID or object. Default uses the global `$post`.
#// @param bool        $leavename Optional. Whether to keep the page name. Default false.
#// @param bool        $sample    Optional. Whether it should be treated as a sample permalink.
#// Default false.
#// @return string The page permalink.
#//
def get_page_link(post=False, leavename=False, sample=False, *args_):
    
    post = get_post(post)
    if "page" == get_option("show_on_front") and get_option("page_on_front") == post.ID:
        link = home_url("/")
    else:
        link = _get_page_link(post, leavename, sample)
    # end if
    #// 
    #// Filters the permalink for a page.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $link    The page's permalink.
    #// @param int    $post_id The ID of the page.
    #// @param bool   $sample  Is it a sample permalink.
    #//
    return apply_filters("page_link", link, post.ID, sample)
# end def get_page_link
#// 
#// Retrieves the page permalink.
#// 
#// Ignores page_on_front. Internal use only.
#// 
#// @since 2.1.0
#// @access private
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int|WP_Post $post      Optional. Post ID or object. Default uses the global `$post`.
#// @param bool        $leavename Optional. Whether to keep the page name. Default false.
#// @param bool        $sample    Optional. Whether it should be treated as a sample permalink.
#// Default false.
#// @return string The page permalink.
#//
def _get_page_link(post=False, leavename=False, sample=False, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    post = get_post(post)
    draft_or_pending = php_in_array(post.post_status, Array("draft", "pending", "auto-draft"))
    link = wp_rewrite.get_page_permastruct()
    if (not php_empty(lambda : link)) and (php_isset(lambda : post.post_status)) and (not draft_or_pending) or sample:
        if (not leavename):
            link = php_str_replace("%pagename%", get_page_uri(post), link)
        # end if
        link = home_url(link)
        link = user_trailingslashit(link, "page")
    else:
        link = home_url("?page_id=" + post.ID)
    # end if
    #// 
    #// Filters the permalink for a non-page_on_front page.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $link    The page's permalink.
    #// @param int    $post_id The ID of the page.
    #//
    return apply_filters("_get_page_link", link, post.ID)
# end def _get_page_link
#// 
#// Retrieves the permalink for an attachment.
#// 
#// This can be used in the WordPress Loop or outside of it.
#// 
#// @since 2.0.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int|object $post      Optional. Post ID or object. Default uses the global `$post`.
#// @param bool       $leavename Optional. Whether to keep the page name. Default false.
#// @return string The attachment permalink.
#//
def get_attachment_link(post=None, leavename=False, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    link = False
    post = get_post(post)
    parent = get_post(post.post_parent) if post.post_parent > 0 and post.post_parent != post.ID else False
    if parent and (not php_in_array(parent.post_type, get_post_types())):
        parent = False
    # end if
    if wp_rewrite.using_permalinks() and parent:
        if "page" == parent.post_type:
            parentlink = _get_page_link(post.post_parent)
            pass
        else:
            parentlink = get_permalink(post.post_parent)
        # end if
        if php_is_numeric(post.post_name) or False != php_strpos(get_option("permalink_structure"), "%category%"):
            name = "attachment/" + post.post_name
            pass
        else:
            name = post.post_name
        # end if
        if php_strpos(parentlink, "?") == False:
            link = user_trailingslashit(trailingslashit(parentlink) + "%postname%")
        # end if
        if (not leavename):
            link = php_str_replace("%postname%", name, link)
        # end if
    elif wp_rewrite.using_permalinks() and (not leavename):
        link = home_url(user_trailingslashit(post.post_name))
    # end if
    if (not link):
        link = home_url("/?attachment_id=" + post.ID)
    # end if
    #// 
    #// Filters the permalink for an attachment.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $link    The attachment's permalink.
    #// @param int    $post_id Attachment ID.
    #//
    return apply_filters("attachment_link", link, post.ID)
# end def get_attachment_link
#// 
#// Retrieves the permalink for the year archives.
#// 
#// @since 1.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int|false $year Integer of year. False for current year.
#// @return string The permalink for the specified year archive.
#//
def get_year_link(year=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not year):
        year = current_time("Y")
    # end if
    yearlink = wp_rewrite.get_year_permastruct()
    if (not php_empty(lambda : yearlink)):
        yearlink = php_str_replace("%year%", year, yearlink)
        yearlink = home_url(user_trailingslashit(yearlink, "year"))
    else:
        yearlink = home_url("?m=" + year)
    # end if
    #// 
    #// Filters the year archive permalink.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $yearlink Permalink for the year archive.
    #// @param int    $year     Year for the archive.
    #//
    return apply_filters("year_link", yearlink, year)
# end def get_year_link
#// 
#// Retrieves the permalink for the month archives with year.
#// 
#// @since 1.0.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int|false $year  Integer of year. False for current year.
#// @param int|false $month Integer of month. False for current month.
#// @return string The permalink for the specified month and year archive.
#//
def get_month_link(year=None, month=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not year):
        year = current_time("Y")
    # end if
    if (not month):
        month = current_time("m")
    # end if
    monthlink = wp_rewrite.get_month_permastruct()
    if (not php_empty(lambda : monthlink)):
        monthlink = php_str_replace("%year%", year, monthlink)
        monthlink = php_str_replace("%monthnum%", zeroise(php_intval(month), 2), monthlink)
        monthlink = home_url(user_trailingslashit(monthlink, "month"))
    else:
        monthlink = home_url("?m=" + year + zeroise(month, 2))
    # end if
    #// 
    #// Filters the month archive permalink.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $monthlink Permalink for the month archive.
    #// @param int    $year      Year for the archive.
    #// @param int    $month     The month for the archive.
    #//
    return apply_filters("month_link", monthlink, year, month)
# end def get_month_link
#// 
#// Retrieves the permalink for the day archives with year and month.
#// 
#// @since 1.0.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int|false $year  Integer of year. False for current year.
#// @param int|false $month Integer of month. False for current month.
#// @param int|false $day   Integer of day. False for current day.
#// @return string The permalink for the specified day, month, and year archive.
#//
def get_day_link(year=None, month=None, day=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not year):
        year = current_time("Y")
    # end if
    if (not month):
        month = current_time("m")
    # end if
    if (not day):
        day = current_time("j")
    # end if
    daylink = wp_rewrite.get_day_permastruct()
    if (not php_empty(lambda : daylink)):
        daylink = php_str_replace("%year%", year, daylink)
        daylink = php_str_replace("%monthnum%", zeroise(php_intval(month), 2), daylink)
        daylink = php_str_replace("%day%", zeroise(php_intval(day), 2), daylink)
        daylink = home_url(user_trailingslashit(daylink, "day"))
    else:
        daylink = home_url("?m=" + year + zeroise(month, 2) + zeroise(day, 2))
    # end if
    #// 
    #// Filters the day archive permalink.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $daylink Permalink for the day archive.
    #// @param int    $year    Year for the archive.
    #// @param int    $month   Month for the archive.
    #// @param int    $day     The day for the archive.
    #//
    return apply_filters("day_link", daylink, year, month, day)
# end def get_day_link
#// 
#// Displays the permalink for the feed type.
#// 
#// @since 3.0.0
#// 
#// @param string $anchor The link's anchor text.
#// @param string $feed   Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#//
def the_feed_link(anchor=None, feed="", *args_):
    
    link = "<a href=\"" + esc_url(get_feed_link(feed)) + "\">" + anchor + "</a>"
    #// 
    #// Filters the feed link anchor tag.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $link The complete anchor tag for a feed link.
    #// @param string $feed The feed type. Possible values include 'rss2', 'atom',
    #// or an empty string for the default feed type.
    #//
    php_print(apply_filters("the_feed_link", link, feed))
# end def the_feed_link
#// 
#// Retrieves the permalink for the feed type.
#// 
#// @since 1.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $feed Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string The feed permalink.
#//
def get_feed_link(feed="", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    permalink = wp_rewrite.get_feed_permastruct()
    if "" != permalink:
        if False != php_strpos(feed, "comments_"):
            feed = php_str_replace("comments_", "", feed)
            permalink = wp_rewrite.get_comment_feed_permastruct()
        # end if
        if get_default_feed() == feed:
            feed = ""
        # end if
        permalink = php_str_replace("%feed%", feed, permalink)
        permalink = php_preg_replace("#/+#", "/", str("/") + str(permalink))
        output = home_url(user_trailingslashit(permalink, "feed"))
    else:
        if php_empty(lambda : feed):
            feed = get_default_feed()
        # end if
        if False != php_strpos(feed, "comments_"):
            feed = php_str_replace("comments_", "comments-", feed)
        # end if
        output = home_url(str("?feed=") + str(feed))
    # end if
    #// 
    #// Filters the feed type permalink.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $output The feed permalink.
    #// @param string $feed   The feed type. Possible values include 'rss2', 'atom',
    #// or an empty string for the default feed type.
    #//
    return apply_filters("feed_link", output, feed)
# end def get_feed_link
#// 
#// Retrieves the permalink for the post comments feed.
#// 
#// @since 2.2.0
#// 
#// @param int    $post_id Optional. Post ID. Default is the ID of the global `$post`.
#// @param string $feed    Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string The permalink for the comments feed for the given post.
#//
def get_post_comments_feed_link(post_id=0, feed="", *args_):
    
    post_id = absint(post_id)
    if (not post_id):
        post_id = get_the_ID()
    # end if
    if php_empty(lambda : feed):
        feed = get_default_feed()
    # end if
    post = get_post(post_id)
    unattached = "attachment" == post.post_type and 0 == php_int(post.post_parent)
    if "" != get_option("permalink_structure"):
        if "page" == get_option("show_on_front") and get_option("page_on_front") == post_id:
            url = _get_page_link(post_id)
        else:
            url = get_permalink(post_id)
        # end if
        if unattached:
            url = home_url("/feed/")
            if get_default_feed() != feed:
                url += str(feed) + str("/")
            # end if
            url = add_query_arg("attachment_id", post_id, url)
        else:
            url = trailingslashit(url) + "feed"
            if get_default_feed() != feed:
                url += str("/") + str(feed)
            # end if
            url = user_trailingslashit(url, "single_feed")
        # end if
    else:
        if unattached:
            url = add_query_arg(Array({"feed": feed, "attachment_id": post_id}), home_url("/"))
        elif "page" == post.post_type:
            url = add_query_arg(Array({"feed": feed, "page_id": post_id}), home_url("/"))
        else:
            url = add_query_arg(Array({"feed": feed, "p": post_id}), home_url("/"))
        # end if
    # end if
    #// 
    #// Filters the post comments feed permalink.
    #// 
    #// @since 1.5.1
    #// 
    #// @param string $url Post comments feed permalink.
    #//
    return apply_filters("post_comments_feed_link", url)
# end def get_post_comments_feed_link
#// 
#// Displays the comment feed link for a post.
#// 
#// Prints out the comment feed link for a post. Link text is placed in the
#// anchor. If no link text is specified, default text is used. If no post ID is
#// specified, the current post is used.
#// 
#// @since 2.5.0
#// 
#// @param string $link_text Optional. Descriptive link text. Default 'Comments Feed'.
#// @param int    $post_id   Optional. Post ID. Default is the ID of the global `$post`.
#// @param string $feed      Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#//
def post_comments_feed_link(link_text="", post_id="", feed="", *args_):
    
    url = get_post_comments_feed_link(post_id, feed)
    if php_empty(lambda : link_text):
        link_text = __("Comments Feed")
    # end if
    link = "<a href=\"" + esc_url(url) + "\">" + link_text + "</a>"
    #// 
    #// Filters the post comment feed link anchor tag.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $link    The complete anchor tag for the comment feed link.
    #// @param int    $post_id Post ID.
    #// @param string $feed    The feed type. Possible values include 'rss2', 'atom',
    #// or an empty string for the default feed type.
    #//
    php_print(apply_filters("post_comments_feed_link_html", link, post_id, feed))
# end def post_comments_feed_link
#// 
#// Retrieves the feed link for a given author.
#// 
#// Returns a link to the feed for all posts by a given author. A specific feed
#// can be requested or left blank to get the default feed.
#// 
#// @since 2.5.0
#// 
#// @param int    $author_id Author ID.
#// @param string $feed      Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string Link to the feed for the author specified by $author_id.
#//
def get_author_feed_link(author_id=None, feed="", *args_):
    
    author_id = php_int(author_id)
    permalink_structure = get_option("permalink_structure")
    if php_empty(lambda : feed):
        feed = get_default_feed()
    # end if
    if "" == permalink_structure:
        link = home_url(str("?feed=") + str(feed) + str("&amp;author=") + author_id)
    else:
        link = get_author_posts_url(author_id)
        if get_default_feed() == feed:
            feed_link = "feed"
        else:
            feed_link = str("feed/") + str(feed)
        # end if
        link = trailingslashit(link) + user_trailingslashit(feed_link, "feed")
    # end if
    #// 
    #// Filters the feed link for a given author.
    #// 
    #// @since 1.5.1
    #// 
    #// @param string $link The author feed link.
    #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
    #//
    link = apply_filters("author_feed_link", link, feed)
    return link
# end def get_author_feed_link
#// 
#// Retrieves the feed link for a category.
#// 
#// Returns a link to the feed for all posts in a given category. A specific feed
#// can be requested or left blank to get the default feed.
#// 
#// @since 2.5.0
#// 
#// @param int    $cat_id Category ID.
#// @param string $feed   Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string Link to the feed for the category specified by $cat_id.
#//
def get_category_feed_link(cat_id=None, feed="", *args_):
    
    return get_term_feed_link(cat_id, "category", feed)
# end def get_category_feed_link
#// 
#// Retrieves the feed link for a term.
#// 
#// Returns a link to the feed for all posts in a given term. A specific feed
#// can be requested or left blank to get the default feed.
#// 
#// @since 3.0.0
#// 
#// @param int    $term_id  Term ID.
#// @param string $taxonomy Optional. Taxonomy of `$term_id`. Default 'category'.
#// @param string $feed     Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string|false Link to the feed for the term specified by $term_id and $taxonomy.
#//
def get_term_feed_link(term_id=None, taxonomy="category", feed="", *args_):
    
    term_id = php_int(term_id)
    term = get_term(term_id, taxonomy)
    if php_empty(lambda : term) or is_wp_error(term):
        return False
    # end if
    if php_empty(lambda : feed):
        feed = get_default_feed()
    # end if
    permalink_structure = get_option("permalink_structure")
    if "" == permalink_structure:
        if "category" == taxonomy:
            link = home_url(str("?feed=") + str(feed) + str("&amp;cat=") + str(term_id))
        elif "post_tag" == taxonomy:
            link = home_url(str("?feed=") + str(feed) + str("&amp;tag=") + str(term.slug))
        else:
            t = get_taxonomy(taxonomy)
            link = home_url(str("?feed=") + str(feed) + str("&amp;") + str(t.query_var) + str("=") + str(term.slug))
        # end if
    else:
        link = get_term_link(term_id, term.taxonomy)
        if get_default_feed() == feed:
            feed_link = "feed"
        else:
            feed_link = str("feed/") + str(feed)
        # end if
        link = trailingslashit(link) + user_trailingslashit(feed_link, "feed")
    # end if
    if "category" == taxonomy:
        #// 
        #// Filters the category feed link.
        #// 
        #// @since 1.5.1
        #// 
        #// @param string $link The category feed link.
        #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
        #//
        link = apply_filters("category_feed_link", link, feed)
    elif "post_tag" == taxonomy:
        #// 
        #// Filters the post tag feed link.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $link The tag feed link.
        #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
        #//
        link = apply_filters("tag_feed_link", link, feed)
    else:
        #// 
        #// Filters the feed link for a taxonomy other than 'category' or 'post_tag'.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $link     The taxonomy feed link.
        #// @param string $feed     Feed type. Possible values include 'rss2', 'atom'.
        #// @param string $taxonomy The taxonomy name.
        #//
        link = apply_filters("taxonomy_feed_link", link, feed, taxonomy)
    # end if
    return link
# end def get_term_feed_link
#// 
#// Retrieves the permalink for a tag feed.
#// 
#// @since 2.3.0
#// 
#// @param int    $tag_id Tag ID.
#// @param string $feed   Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string The feed permalink for the given tag.
#//
def get_tag_feed_link(tag_id=None, feed="", *args_):
    
    return get_term_feed_link(tag_id, "post_tag", feed)
# end def get_tag_feed_link
#// 
#// Retrieves the edit link for a tag.
#// 
#// @since 2.7.0
#// 
#// @param int    $tag_id   Tag ID.
#// @param string $taxonomy Optional. Taxonomy slug. Default 'post_tag'.
#// @return string The edit tag link URL for the given tag.
#//
def get_edit_tag_link(tag_id=None, taxonomy="post_tag", *args_):
    
    #// 
    #// Filters the edit link for a tag (or term in another taxonomy).
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $link The term edit link.
    #//
    return apply_filters("get_edit_tag_link", get_edit_term_link(tag_id, taxonomy))
# end def get_edit_tag_link
#// 
#// Displays or retrieves the edit link for a tag with formatting.
#// 
#// @since 2.7.0
#// 
#// @param string  $link   Optional. Anchor text. If empty, default is 'Edit This'. Default empty.
#// @param string  $before Optional. Display before edit link. Default empty.
#// @param string  $after  Optional. Display after edit link. Default empty.
#// @param WP_Term $tag    Optional. Term object. If null, the queried object will be inspected.
#// Default null.
#//
def edit_tag_link(link="", before="", after="", tag=None, *args_):
    
    link = edit_term_link(link, "", "", tag, False)
    #// 
    #// Filters the anchor tag for the edit link for a tag (or term in another taxonomy).
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $link The anchor tag for the edit link.
    #//
    php_print(before + apply_filters("edit_tag_link", link) + after)
# end def edit_tag_link
#// 
#// Retrieves the URL for editing a given term.
#// 
#// @since 3.1.0
#// @since 4.5.0 The `$taxonomy` parameter was made optional.
#// 
#// @param int    $term_id     Term ID.
#// @param string $taxonomy    Optional. Taxonomy. Defaults to the taxonomy of the term identified
#// by `$term_id`.
#// @param string $object_type Optional. The object type. Used to highlight the proper post type
#// menu on the linked page. Defaults to the first object_type associated
#// with the taxonomy.
#// @return string|null The edit term link URL for the given term, or null on failure.
#//
def get_edit_term_link(term_id=None, taxonomy="", object_type="", *args_):
    
    term = get_term(term_id, taxonomy)
    if (not term) or is_wp_error(term):
        return
    # end if
    tax = get_taxonomy(term.taxonomy)
    if (not tax) or (not current_user_can("edit_term", term.term_id)):
        return
    # end if
    args = Array({"taxonomy": taxonomy, "tag_ID": term.term_id})
    if object_type:
        args["post_type"] = object_type
    elif (not php_empty(lambda : tax.object_type)):
        args["post_type"] = reset(tax.object_type)
    # end if
    if tax.show_ui:
        location = add_query_arg(args, admin_url("term.php"))
    else:
        location = ""
    # end if
    #// 
    #// Filters the edit link for a term.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $location    The edit link.
    #// @param int    $term_id     Term ID.
    #// @param string $taxonomy    Taxonomy name.
    #// @param string $object_type The object type (eg. the post type).
    #//
    return apply_filters("get_edit_term_link", location, term_id, taxonomy, object_type)
# end def get_edit_term_link
#// 
#// Displays or retrieves the edit term link with formatting.
#// 
#// @since 3.1.0
#// 
#// @param string  $link   Optional. Anchor text. If empty, default is 'Edit This'. Default empty.
#// @param string  $before Optional. Display before edit link. Default empty.
#// @param string  $after  Optional. Display after edit link. Default empty.
#// @param WP_Term $term   Optional. Term object. If null, the queried object will be inspected. Default null.
#// @param bool    $echo   Optional. Whether or not to echo the return. Default true.
#// @return string|void HTML content.
#//
def edit_term_link(link="", before="", after="", term=None, echo=True, *args_):
    
    if is_null(term):
        term = get_queried_object()
    # end if
    if (not term):
        return
    # end if
    tax = get_taxonomy(term.taxonomy)
    if (not current_user_can("edit_term", term.term_id)):
        return
    # end if
    if php_empty(lambda : link):
        link = __("Edit This")
    # end if
    link = "<a href=\"" + get_edit_term_link(term.term_id, term.taxonomy) + "\">" + link + "</a>"
    #// 
    #// Filters the anchor tag for the edit link of a term.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $link    The anchor tag for the edit link.
    #// @param int    $term_id Term ID.
    #//
    link = before + apply_filters("edit_term_link", link, term.term_id) + after
    if echo:
        php_print(link)
    else:
        return link
    # end if
# end def edit_term_link
#// 
#// Retrieves the permalink for a search.
#// 
#// @since 3.0.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $query Optional. The query string to use. If empty the current query is used. Default empty.
#// @return string The search permalink.
#//
def get_search_link(query="", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if php_empty(lambda : query):
        search = get_search_query(False)
    else:
        search = stripslashes(query)
    # end if
    permastruct = wp_rewrite.get_search_permastruct()
    if php_empty(lambda : permastruct):
        link = home_url("?s=" + urlencode(search))
    else:
        search = urlencode(search)
        search = php_str_replace("%2F", "/", search)
        #// %2F(/) is not valid within a URL, send it un-encoded.
        link = php_str_replace("%search%", search, permastruct)
        link = home_url(user_trailingslashit(link, "search"))
    # end if
    #// 
    #// Filters the search permalink.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $link   Search permalink.
    #// @param string $search The URL-encoded search term.
    #//
    return apply_filters("search_link", link, search)
# end def get_search_link
#// 
#// Retrieves the permalink for the search results feed.
#// 
#// @since 2.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $search_query Optional. Search query. Default empty.
#// @param string $feed         Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string The search results feed permalink.
#//
def get_search_feed_link(search_query="", feed="", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    link = get_search_link(search_query)
    if php_empty(lambda : feed):
        feed = get_default_feed()
    # end if
    permastruct = wp_rewrite.get_search_permastruct()
    if php_empty(lambda : permastruct):
        link = add_query_arg("feed", feed, link)
    else:
        link = trailingslashit(link)
        link += str("feed/") + str(feed) + str("/")
    # end if
    #// 
    #// Filters the search feed link.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $link Search feed link.
    #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
    #// @param string $type The search type. One of 'posts' or 'comments'.
    #//
    return apply_filters("search_feed_link", link, feed, "posts")
# end def get_search_feed_link
#// 
#// Retrieves the permalink for the search results comments feed.
#// 
#// @since 2.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $search_query Optional. Search query. Default empty.
#// @param string $feed         Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string The comments feed search results permalink.
#//
def get_search_comments_feed_link(search_query="", feed="", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if php_empty(lambda : feed):
        feed = get_default_feed()
    # end if
    link = get_search_feed_link(search_query, feed)
    permastruct = wp_rewrite.get_search_permastruct()
    if php_empty(lambda : permastruct):
        link = add_query_arg("feed", "comments-" + feed, link)
    else:
        link = add_query_arg("withcomments", 1, link)
    # end if
    #// This filter is documented in wp-includes/link-template.php
    return apply_filters("search_feed_link", link, feed, "comments")
# end def get_search_comments_feed_link
#// 
#// Retrieves the permalink for a post type archive.
#// 
#// @since 3.1.0
#// @since 4.5.0 Support for posts was added.
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $post_type Post type.
#// @return string|false The post type archive permalink.
#//
def get_post_type_archive_link(post_type=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    post_type_obj = get_post_type_object(post_type)
    if (not post_type_obj):
        return False
    # end if
    if "post" == post_type:
        show_on_front = get_option("show_on_front")
        page_for_posts = get_option("page_for_posts")
        if "page" == show_on_front and page_for_posts:
            link = get_permalink(page_for_posts)
        else:
            link = get_home_url()
        # end if
        #// This filter is documented in wp-includes/link-template.php
        return apply_filters("post_type_archive_link", link, post_type)
    # end if
    if (not post_type_obj.has_archive):
        return False
    # end if
    if get_option("permalink_structure") and php_is_array(post_type_obj.rewrite):
        struct = post_type_obj.rewrite["slug"] if True == post_type_obj.has_archive else post_type_obj.has_archive
        if post_type_obj.rewrite["with_front"]:
            struct = wp_rewrite.front + struct
        else:
            struct = wp_rewrite.root + struct
        # end if
        link = home_url(user_trailingslashit(struct, "post_type_archive"))
    else:
        link = home_url("?post_type=" + post_type)
    # end if
    #// 
    #// Filters the post type archive permalink.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $link      The post type archive permalink.
    #// @param string $post_type Post type name.
    #//
    return apply_filters("post_type_archive_link", link, post_type)
# end def get_post_type_archive_link
#// 
#// Retrieves the permalink for a post type archive feed.
#// 
#// @since 3.1.0
#// 
#// @param string $post_type Post type
#// @param string $feed      Optional. Feed type. Possible values include 'rss2', 'atom'.
#// Default is the value of get_default_feed().
#// @return string|false The post type feed permalink.
#//
def get_post_type_archive_feed_link(post_type=None, feed="", *args_):
    
    default_feed = get_default_feed()
    if php_empty(lambda : feed):
        feed = default_feed
    # end if
    link = get_post_type_archive_link(post_type)
    if (not link):
        return False
    # end if
    post_type_obj = get_post_type_object(post_type)
    if get_option("permalink_structure") and php_is_array(post_type_obj.rewrite) and post_type_obj.rewrite["feeds"]:
        link = trailingslashit(link)
        link += "feed/"
        if feed != default_feed:
            link += str(feed) + str("/")
        # end if
    else:
        link = add_query_arg("feed", feed, link)
    # end if
    #// 
    #// Filters the post type archive feed link.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $link The post type archive feed link.
    #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
    #//
    return apply_filters("post_type_archive_feed_link", link, feed)
# end def get_post_type_archive_feed_link
#// 
#// Retrieves the URL used for the post preview.
#// 
#// Allows additional query args to be appended.
#// 
#// @since 4.4.0
#// 
#// @param int|WP_Post $post         Optional. Post ID or `WP_Post` object. Defaults to global `$post`.
#// @param array       $query_args   Optional. Array of additional query args to be appended to the link.
#// Default empty array.
#// @param string      $preview_link Optional. Base preview link to be used if it should differ from the
#// post permalink. Default empty.
#// @return string|null URL used for the post preview, or null if the post does not exist.
#//
def get_preview_post_link(post=None, query_args=Array(), preview_link="", *args_):
    
    post = get_post(post)
    if (not post):
        return
    # end if
    post_type_object = get_post_type_object(post.post_type)
    if is_post_type_viewable(post_type_object):
        if (not preview_link):
            preview_link = set_url_scheme(get_permalink(post))
        # end if
        query_args["preview"] = "true"
        preview_link = add_query_arg(query_args, preview_link)
    # end if
    #// 
    #// Filters the URL used for a post preview.
    #// 
    #// @since 2.0.5
    #// @since 4.0.0 Added the `$post` parameter.
    #// 
    #// @param string  $preview_link URL used for the post preview.
    #// @param WP_Post $post         Post object.
    #//
    return apply_filters("preview_post_link", preview_link, post)
# end def get_preview_post_link
#// 
#// Retrieves the edit post link for post.
#// 
#// Can be used within the WordPress loop or outside of it. Can be used with
#// pages, posts, attachments, and revisions.
#// 
#// @since 2.3.0
#// 
#// @param int|WP_Post $id      Optional. Post ID or post object. Default is the global `$post`.
#// @param string      $context Optional. How to output the '&' character. Default '&amp;'.
#// @return string|null The edit post link for the given post. null if the post type is invalid or does
#// not allow an editing UI.
#//
def get_edit_post_link(id=0, context="display", *args_):
    
    post = get_post(id)
    if (not post):
        return
    # end if
    if "revision" == post.post_type:
        action = ""
    elif "display" == context:
        action = "&amp;action=edit"
    else:
        action = "&action=edit"
    # end if
    post_type_object = get_post_type_object(post.post_type)
    if (not post_type_object):
        return
    # end if
    if (not current_user_can("edit_post", post.ID)):
        return
    # end if
    if post_type_object._edit_link:
        link = admin_url(php_sprintf(post_type_object._edit_link + action, post.ID))
    else:
        link = ""
    # end if
    #// 
    #// Filters the post edit link.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $link    The edit link.
    #// @param int    $post_id Post ID.
    #// @param string $context The link context. If set to 'display' then ampersands
    #// are encoded.
    #//
    return apply_filters("get_edit_post_link", link, post.ID, context)
# end def get_edit_post_link
#// 
#// Displays the edit post link for post.
#// 
#// @since 1.0.0
#// @since 4.4.0 The `$class` argument was added.
#// 
#// @param string      $text   Optional. Anchor text. If null, default is 'Edit This'. Default null.
#// @param string      $before Optional. Display before edit link. Default empty.
#// @param string      $after  Optional. Display after edit link. Default empty.
#// @param int|WP_Post $id     Optional. Post ID or post object. Default is the global `$post`.
#// @param string      $class  Optional. Add custom class to link. Default 'post-edit-link'.
#//
def edit_post_link(text=None, before="", after="", id=0, class_="post-edit-link", *args_):
    
    post = get_post(id)
    if (not post):
        return
    # end if
    url = get_edit_post_link(post.ID)
    if (not url):
        return
    # end if
    if None == text:
        text = __("Edit This")
    # end if
    link = "<a class=\"" + esc_attr(class_) + "\" href=\"" + esc_url(url) + "\">" + text + "</a>"
    #// 
    #// Filters the post edit link anchor tag.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $link    Anchor tag for the edit link.
    #// @param int    $post_id Post ID.
    #// @param string $text    Anchor text.
    #//
    php_print(before + apply_filters("edit_post_link", link, post.ID, text) + after)
# end def edit_post_link
#// 
#// Retrieves the delete posts link for post.
#// 
#// Can be used within the WordPress loop or outside of it, with any post type.
#// 
#// @since 2.9.0
#// 
#// @param int|WP_Post $id           Optional. Post ID or post object. Default is the global `$post`.
#// @param string      $deprecated   Not used.
#// @param bool        $force_delete Optional. Whether to bypass Trash and force deletion. Default false.
#// @return string|void The delete post link URL for the given post.
#//
def get_delete_post_link(id=0, deprecated="", force_delete=False, *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "3.0.0")
    # end if
    post = get_post(id)
    if (not post):
        return
    # end if
    post_type_object = get_post_type_object(post.post_type)
    if (not post_type_object):
        return
    # end if
    if (not current_user_can("delete_post", post.ID)):
        return
    # end if
    action = "delete" if force_delete or (not EMPTY_TRASH_DAYS) else "trash"
    delete_link = add_query_arg("action", action, admin_url(php_sprintf(post_type_object._edit_link, post.ID)))
    #// 
    #// Filters the post delete link.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $link         The delete link.
    #// @param int    $post_id      Post ID.
    #// @param bool   $force_delete Whether to bypass the Trash and force deletion. Default false.
    #//
    return apply_filters("get_delete_post_link", wp_nonce_url(delete_link, str(action) + str("-post_") + str(post.ID)), post.ID, force_delete)
# end def get_delete_post_link
#// 
#// Retrieves the edit comment link.
#// 
#// @since 2.3.0
#// 
#// @param int|WP_Comment $comment_id Optional. Comment ID or WP_Comment object.
#// @return string|void The edit comment link URL for the given comment.
#//
def get_edit_comment_link(comment_id=0, *args_):
    
    comment = get_comment(comment_id)
    if (not current_user_can("edit_comment", comment.comment_ID)):
        return
    # end if
    location = admin_url("comment.php?action=editcomment&amp;c=") + comment.comment_ID
    #// 
    #// Filters the comment edit link.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $location The edit link.
    #//
    return apply_filters("get_edit_comment_link", location)
# end def get_edit_comment_link
#// 
#// Displays the edit comment link with formatting.
#// 
#// @since 1.0.0
#// 
#// @param string $text   Optional. Anchor text. If null, default is 'Edit This'. Default null.
#// @param string $before Optional. Display before edit link. Default empty.
#// @param string $after  Optional. Display after edit link. Default empty.
#//
def edit_comment_link(text=None, before="", after="", *args_):
    
    comment = get_comment()
    if (not current_user_can("edit_comment", comment.comment_ID)):
        return
    # end if
    if None == text:
        text = __("Edit This")
    # end if
    link = "<a class=\"comment-edit-link\" href=\"" + esc_url(get_edit_comment_link(comment)) + "\">" + text + "</a>"
    #// 
    #// Filters the comment edit link anchor tag.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $link       Anchor tag for the edit link.
    #// @param int    $comment_id Comment ID.
    #// @param string $text       Anchor text.
    #//
    php_print(before + apply_filters("edit_comment_link", link, comment.comment_ID, text) + after)
# end def edit_comment_link
#// 
#// Displays the edit bookmark link.
#// 
#// @since 2.7.0
#// 
#// @param int|stdClass $link Optional. Bookmark ID. Default is the id of the current bookmark.
#// @return string|void The edit bookmark link URL.
#//
def get_edit_bookmark_link(link=0, *args_):
    
    link = get_bookmark(link)
    if (not current_user_can("manage_links")):
        return
    # end if
    location = admin_url("link.php?action=edit&amp;link_id=") + link.link_id
    #// 
    #// Filters the bookmark edit link.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $location The edit link.
    #// @param int    $link_id  Bookmark ID.
    #//
    return apply_filters("get_edit_bookmark_link", location, link.link_id)
# end def get_edit_bookmark_link
#// 
#// Displays the edit bookmark link anchor content.
#// 
#// @since 2.7.0
#// 
#// @param string $link     Optional. Anchor text. If empty, default is 'Edit This'. Default empty.
#// @param string $before   Optional. Display before edit link. Default empty.
#// @param string $after    Optional. Display after edit link. Default empty.
#// @param int    $bookmark Optional. Bookmark ID. Default is the current bookmark.
#//
def edit_bookmark_link(link="", before="", after="", bookmark=None, *args_):
    
    bookmark = get_bookmark(bookmark)
    if (not current_user_can("manage_links")):
        return
    # end if
    if php_empty(lambda : link):
        link = __("Edit This")
    # end if
    link = "<a href=\"" + esc_url(get_edit_bookmark_link(bookmark)) + "\">" + link + "</a>"
    #// 
    #// Filters the bookmark edit link anchor tag.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $link    Anchor tag for the edit link.
    #// @param int    $link_id Bookmark ID.
    #//
    php_print(before + apply_filters("edit_bookmark_link", link, bookmark.link_id) + after)
# end def edit_bookmark_link
#// 
#// Retrieves the edit user link.
#// 
#// @since 3.5.0
#// 
#// @param int $user_id Optional. User ID. Defaults to the current user.
#// @return string URL to edit user page or empty string.
#//
def get_edit_user_link(user_id=None, *args_):
    
    if (not user_id):
        user_id = get_current_user_id()
    # end if
    if php_empty(lambda : user_id) or (not current_user_can("edit_user", user_id)):
        return ""
    # end if
    user = get_userdata(user_id)
    if (not user):
        return ""
    # end if
    if get_current_user_id() == user.ID:
        link = get_edit_profile_url(user.ID)
    else:
        link = add_query_arg("user_id", user.ID, self_admin_url("user-edit.php"))
    # end if
    #// 
    #// Filters the user edit link.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $link    The edit link.
    #// @param int    $user_id User ID.
    #//
    return apply_filters("get_edit_user_link", link, user.ID)
# end def get_edit_user_link
#// 
#// Navigation links.
#// 
#// 
#// Retrieves the previous post that is adjacent to the current post.
#// 
#// @since 1.5.0
#// 
#// @param bool         $in_same_term   Optional. Whether post should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return null|string|WP_Post Post object if successful. Null if global $post is not set. Empty string if no
#// corresponding post exists.
#//
def get_previous_post(in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    return get_adjacent_post(in_same_term, excluded_terms, True, taxonomy)
# end def get_previous_post
#// 
#// Retrieves the next post that is adjacent to the current post.
#// 
#// @since 1.5.0
#// 
#// @param bool         $in_same_term   Optional. Whether post should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return null|string|WP_Post Post object if successful. Null if global $post is not set. Empty string if no
#// corresponding post exists.
#//
def get_next_post(in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    return get_adjacent_post(in_same_term, excluded_terms, False, taxonomy)
# end def get_next_post
#// 
#// Retrieves the adjacent post.
#// 
#// Can either be next or previous post.
#// 
#// @since 2.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param bool         $in_same_term   Optional. Whether post should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param bool         $previous       Optional. Whether to retrieve previous post. Default true
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return null|string|WP_Post Post object if successful. Null if global $post is not set. Empty string if no
#// corresponding post exists.
#//
def get_adjacent_post(in_same_term=False, excluded_terms="", previous=True, taxonomy="category", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = get_post()
    if (not post) or (not taxonomy_exists(taxonomy)):
        return None
    # end if
    current_post_date = post.post_date
    join = ""
    where = ""
    adjacent = "previous" if previous else "next"
    if (not php_empty(lambda : excluded_terms)) and (not php_is_array(excluded_terms)):
        #// Back-compat, $excluded_terms used to be $excluded_categories with IDs separated by " and ".
        if False != php_strpos(excluded_terms, " and "):
            _deprecated_argument(__FUNCTION__, "3.3.0", php_sprintf(__("Use commas instead of %s to separate excluded terms."), "'and'"))
            excluded_terms = php_explode(" and ", excluded_terms)
        else:
            excluded_terms = php_explode(",", excluded_terms)
        # end if
        excluded_terms = php_array_map("intval", excluded_terms)
    # end if
    #// 
    #// Filters the IDs of terms excluded from adjacent post queries.
    #// 
    #// The dynamic portion of the hook name, `$adjacent`, refers to the type
    #// of adjacency, 'next' or 'previous'.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $excluded_terms Array of excluded term IDs.
    #//
    excluded_terms = apply_filters(str("get_") + str(adjacent) + str("_post_excluded_terms"), excluded_terms)
    if in_same_term or (not php_empty(lambda : excluded_terms)):
        if in_same_term:
            join += str(" INNER JOIN ") + str(wpdb.term_relationships) + str(" AS tr ON p.ID = tr.object_id INNER JOIN ") + str(wpdb.term_taxonomy) + str(" tt ON tr.term_taxonomy_id = tt.term_taxonomy_id")
            where += wpdb.prepare("AND tt.taxonomy = %s", taxonomy)
            if (not is_object_in_taxonomy(post.post_type, taxonomy)):
                return ""
            # end if
            term_array = wp_get_object_terms(post.ID, taxonomy, Array({"fields": "ids"}))
            #// Remove any exclusions from the term array to include.
            term_array = php_array_diff(term_array, excluded_terms)
            term_array = php_array_map("intval", term_array)
            if (not term_array) or is_wp_error(term_array):
                return ""
            # end if
            where += " AND tt.term_id IN (" + php_implode(",", term_array) + ")"
        # end if
        if (not php_empty(lambda : excluded_terms)):
            where += str(" AND p.ID NOT IN ( SELECT tr.object_id FROM ") + str(wpdb.term_relationships) + str(" tr LEFT JOIN ") + str(wpdb.term_taxonomy) + str(" tt ON (tr.term_taxonomy_id = tt.term_taxonomy_id) WHERE tt.term_id IN (") + php_implode(",", php_array_map("intval", excluded_terms)) + ") )"
        # end if
    # end if
    #// 'post_status' clause depends on the current user.
    if is_user_logged_in():
        user_id = get_current_user_id()
        post_type_object = get_post_type_object(post.post_type)
        if php_empty(lambda : post_type_object):
            post_type_cap = post.post_type
            read_private_cap = "read_private_" + post_type_cap + "s"
        else:
            read_private_cap = post_type_object.cap.read_private_posts
        # end if
        #// 
        #// Results should include private posts belonging to the current user, or private posts where the
        #// current user has the 'read_private_posts' cap.
        #//
        private_states = get_post_stati(Array({"private": True}))
        where += " AND ( p.post_status = 'publish'"
        for state in private_states:
            if current_user_can(read_private_cap):
                where += wpdb.prepare(" OR p.post_status = %s", state)
            else:
                where += wpdb.prepare(" OR (p.post_author = %d AND p.post_status = %s)", user_id, state)
            # end if
        # end for
        where += " )"
    else:
        where += " AND p.post_status = 'publish'"
    # end if
    op = "<" if previous else ">"
    order = "DESC" if previous else "ASC"
    #// 
    #// Filters the JOIN clause in the SQL for an adjacent post query.
    #// 
    #// The dynamic portion of the hook name, `$adjacent`, refers to the type
    #// of adjacency, 'next' or 'previous'.
    #// 
    #// @since 2.5.0
    #// @since 4.4.0 Added the `$taxonomy` and `$post` parameters.
    #// 
    #// @param string  $join           The JOIN clause in the SQL.
    #// @param bool    $in_same_term   Whether post should be in a same taxonomy term.
    #// @param array   $excluded_terms Array of excluded term IDs.
    #// @param string  $taxonomy       Taxonomy. Used to identify the term used when `$in_same_term` is true.
    #// @param WP_Post $post           WP_Post object.
    #//
    join = apply_filters(str("get_") + str(adjacent) + str("_post_join"), join, in_same_term, excluded_terms, taxonomy, post)
    #// 
    #// Filters the WHERE clause in the SQL for an adjacent post query.
    #// 
    #// The dynamic portion of the hook name, `$adjacent`, refers to the type
    #// of adjacency, 'next' or 'previous'.
    #// 
    #// @since 2.5.0
    #// @since 4.4.0 Added the `$taxonomy` and `$post` parameters.
    #// 
    #// @param string  $where          The `WHERE` clause in the SQL.
    #// @param bool    $in_same_term   Whether post should be in a same taxonomy term.
    #// @param array   $excluded_terms Array of excluded term IDs.
    #// @param string  $taxonomy       Taxonomy. Used to identify the term used when `$in_same_term` is true.
    #// @param WP_Post $post           WP_Post object.
    #//
    where = apply_filters(str("get_") + str(adjacent) + str("_post_where"), wpdb.prepare(str("WHERE p.post_date ") + str(op) + str(" %s AND p.post_type = %s ") + str(where), current_post_date, post.post_type), in_same_term, excluded_terms, taxonomy, post)
    #// 
    #// Filters the ORDER BY clause in the SQL for an adjacent post query.
    #// 
    #// The dynamic portion of the hook name, `$adjacent`, refers to the type
    #// of adjacency, 'next' or 'previous'.
    #// 
    #// @since 2.5.0
    #// @since 4.4.0 Added the `$post` parameter.
    #// @since 4.9.0 Added the `$order` parameter.
    #// 
    #// @param string $order_by The `ORDER BY` clause in the SQL.
    #// @param WP_Post $post    WP_Post object.
    #// @param string  $order   Sort order. 'DESC' for previous post, 'ASC' for next.
    #//
    sort = apply_filters(str("get_") + str(adjacent) + str("_post_sort"), str("ORDER BY p.post_date ") + str(order) + str(" LIMIT 1"), post, order)
    query = str("SELECT p.ID FROM ") + str(wpdb.posts) + str(" AS p ") + str(join) + str(" ") + str(where) + str(" ") + str(sort)
    query_key = "adjacent_post_" + php_md5(query)
    result = wp_cache_get(query_key, "counts")
    if False != result:
        if result:
            result = get_post(result)
        # end if
        return result
    # end if
    result = wpdb.get_var(query)
    if None == result:
        result = ""
    # end if
    wp_cache_set(query_key, result, "counts")
    if result:
        result = get_post(result)
    # end if
    return result
# end def get_adjacent_post
#// 
#// Retrieves the adjacent post relational link.
#// 
#// Can either be next or previous post relational link.
#// 
#// @since 2.8.0
#// 
#// @param string       $title          Optional. Link title format. Default '%title'.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param bool         $previous       Optional. Whether to display link to previous or next post. Default true.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return string|void The adjacent post relational link URL.
#//
def get_adjacent_post_rel_link(title="%title", in_same_term=False, excluded_terms="", previous=True, taxonomy="category", *args_):
    
    post = get_post()
    if previous and is_attachment() and post:
        post = get_post(post.post_parent)
    else:
        post = get_adjacent_post(in_same_term, excluded_terms, previous, taxonomy)
    # end if
    if php_empty(lambda : post):
        return
    # end if
    post_title = the_title_attribute(Array({"echo": False, "post": post}))
    if php_empty(lambda : post_title):
        post_title = __("Previous Post") if previous else __("Next Post")
    # end if
    date = mysql2date(get_option("date_format"), post.post_date)
    title = php_str_replace("%title", post_title, title)
    title = php_str_replace("%date", date, title)
    link = "<link rel='prev' title='" if previous else "<link rel='next' title='"
    link += esc_attr(title)
    link += "' href='" + get_permalink(post) + "' />\n"
    adjacent = "previous" if previous else "next"
    #// 
    #// Filters the adjacent post relational link.
    #// 
    #// The dynamic portion of the hook name, `$adjacent`, refers to the type
    #// of adjacency, 'next' or 'previous'.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $link The relational link.
    #//
    return apply_filters(str(adjacent) + str("_post_rel_link"), link)
# end def get_adjacent_post_rel_link
#// 
#// Displays the relational links for the posts adjacent to the current post.
#// 
#// @since 2.8.0
#// 
#// @param string       $title          Optional. Link title format. Default '%title'.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#//
def adjacent_posts_rel_link(title="%title", in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    php_print(get_adjacent_post_rel_link(title, in_same_term, excluded_terms, True, taxonomy))
    php_print(get_adjacent_post_rel_link(title, in_same_term, excluded_terms, False, taxonomy))
# end def adjacent_posts_rel_link
#// 
#// Displays relational links for the posts adjacent to the current post for single post pages.
#// 
#// This is meant to be attached to actions like 'wp_head'. Do not call this directly in plugins
#// or theme templates.
#// 
#// @since 3.0.0
#// 
#// @see adjacent_posts_rel_link()
#//
def adjacent_posts_rel_link_wp_head(*args_):
    
    if (not is_single()) or is_attachment():
        return
    # end if
    adjacent_posts_rel_link()
# end def adjacent_posts_rel_link_wp_head
#// 
#// Displays the relational link for the next post adjacent to the current post.
#// 
#// @since 2.8.0
#// 
#// @see get_adjacent_post_rel_link()
#// 
#// @param string       $title          Optional. Link title format. Default '%title'.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#//
def next_post_rel_link(title="%title", in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    php_print(get_adjacent_post_rel_link(title, in_same_term, excluded_terms, False, taxonomy))
# end def next_post_rel_link
#// 
#// Displays the relational link for the previous post adjacent to the current post.
#// 
#// @since 2.8.0
#// 
#// @see get_adjacent_post_rel_link()
#// 
#// @param string       $title          Optional. Link title format. Default '%title'.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default true.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#//
def prev_post_rel_link(title="%title", in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    php_print(get_adjacent_post_rel_link(title, in_same_term, excluded_terms, True, taxonomy))
# end def prev_post_rel_link
#// 
#// Retrieves the boundary post.
#// 
#// Boundary being either the first or last post by publish date within the constraints specified
#// by $in_same_term or $excluded_terms.
#// 
#// @since 2.8.0
#// 
#// @param bool         $in_same_term   Optional. Whether returned post should be in a same taxonomy term.
#// Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs.
#// Default empty.
#// @param bool         $start          Optional. Whether to retrieve first or last post. Default true
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return null|array Array containing the boundary post object if successful, null otherwise.
#//
def get_boundary_post(in_same_term=False, excluded_terms="", start=True, taxonomy="category", *args_):
    
    post = get_post()
    if (not post) or (not is_single()) or is_attachment() or (not taxonomy_exists(taxonomy)):
        return None
    # end if
    query_args = Array({"posts_per_page": 1, "order": "ASC" if start else "DESC", "update_post_term_cache": False, "update_post_meta_cache": False})
    term_array = Array()
    if (not php_is_array(excluded_terms)):
        if (not php_empty(lambda : excluded_terms)):
            excluded_terms = php_explode(",", excluded_terms)
        else:
            excluded_terms = Array()
        # end if
    # end if
    if in_same_term or (not php_empty(lambda : excluded_terms)):
        if in_same_term:
            term_array = wp_get_object_terms(post.ID, taxonomy, Array({"fields": "ids"}))
        # end if
        if (not php_empty(lambda : excluded_terms)):
            excluded_terms = php_array_map("intval", excluded_terms)
            excluded_terms = php_array_diff(excluded_terms, term_array)
            inverse_terms = Array()
            for excluded_term in excluded_terms:
                inverse_terms[-1] = excluded_term * -1
            # end for
            excluded_terms = inverse_terms
        # end if
        query_args["tax_query"] = Array(Array({"taxonomy": taxonomy, "terms": php_array_merge(term_array, excluded_terms)}))
    # end if
    return get_posts(query_args)
# end def get_boundary_post
#// 
#// Retrieves the previous post link that is adjacent to the current post.
#// 
#// @since 3.7.0
#// 
#// @param string       $format         Optional. Link anchor format. Default '&laquo; %link'.
#// @param string       $link           Optional. Link permalink format. Default '%title'.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return string The link URL of the previous post in relation to the current post.
#//
def get_previous_post_link(format="&laquo; %link", link="%title", in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    return get_adjacent_post_link(format, link, in_same_term, excluded_terms, True, taxonomy)
# end def get_previous_post_link
#// 
#// Displays the previous post link that is adjacent to the current post.
#// 
#// @since 1.5.0
#// 
#// @see get_previous_post_link()
#// 
#// @param string       $format         Optional. Link anchor format. Default '&laquo; %link'.
#// @param string       $link           Optional. Link permalink format. Default '%title'.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#//
def previous_post_link(format="&laquo; %link", link="%title", in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    php_print(get_previous_post_link(format, link, in_same_term, excluded_terms, taxonomy))
# end def previous_post_link
#// 
#// Retrieves the next post link that is adjacent to the current post.
#// 
#// @since 3.7.0
#// 
#// @param string       $format         Optional. Link anchor format. Default '&laquo; %link'.
#// @param string       $link           Optional. Link permalink format. Default '%title'.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return string The link URL of the next post in relation to the current post.
#//
def get_next_post_link(format="%link &raquo;", link="%title", in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    return get_adjacent_post_link(format, link, in_same_term, excluded_terms, False, taxonomy)
# end def get_next_post_link
#// 
#// Displays the next post link that is adjacent to the current post.
#// 
#// @since 1.5.0
#// @see get_next_post_link()
#// 
#// @param string       $format         Optional. Link anchor format. Default '&laquo; %link'.
#// @param string       $link           Optional. Link permalink format. Default '%title'
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded term IDs. Default empty.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#//
def next_post_link(format="%link &raquo;", link="%title", in_same_term=False, excluded_terms="", taxonomy="category", *args_):
    
    php_print(get_next_post_link(format, link, in_same_term, excluded_terms, taxonomy))
# end def next_post_link
#// 
#// Retrieves the adjacent post link.
#// 
#// Can be either next post link or previous.
#// 
#// @since 3.7.0
#// 
#// @param string       $format         Link anchor format.
#// @param string       $link           Link permalink format.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded terms IDs. Default empty.
#// @param bool         $previous       Optional. Whether to display link to previous or next post. Default true.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#// @return string The link URL of the previous or next post in relation to the current post.
#//
def get_adjacent_post_link(format=None, link=None, in_same_term=False, excluded_terms="", previous=True, taxonomy="category", *args_):
    
    if previous and is_attachment():
        post = get_post(get_post().post_parent)
    else:
        post = get_adjacent_post(in_same_term, excluded_terms, previous, taxonomy)
    # end if
    if (not post):
        output = ""
    else:
        title = post.post_title
        if php_empty(lambda : post.post_title):
            title = __("Previous Post") if previous else __("Next Post")
        # end if
        #// This filter is documented in wp-includes/post-template.php
        title = apply_filters("the_title", title, post.ID)
        date = mysql2date(get_option("date_format"), post.post_date)
        rel = "prev" if previous else "next"
        string = "<a href=\"" + get_permalink(post) + "\" rel=\"" + rel + "\">"
        inlink = php_str_replace("%title", title, link)
        inlink = php_str_replace("%date", date, inlink)
        inlink = string + inlink + "</a>"
        output = php_str_replace("%link", inlink, format)
    # end if
    adjacent = "previous" if previous else "next"
    #// 
    #// Filters the adjacent post link.
    #// 
    #// The dynamic portion of the hook name, `$adjacent`, refers to the type
    #// of adjacency, 'next' or 'previous'.
    #// 
    #// @since 2.6.0
    #// @since 4.2.0 Added the `$adjacent` parameter.
    #// 
    #// @param string  $output   The adjacent post link.
    #// @param string  $format   Link anchor format.
    #// @param string  $link     Link permalink format.
    #// @param WP_Post $post     The adjacent post.
    #// @param string  $adjacent Whether the post is previous or next.
    #//
    return apply_filters(str(adjacent) + str("_post_link"), output, format, link, post, adjacent)
# end def get_adjacent_post_link
#// 
#// Displays the adjacent post link.
#// 
#// Can be either next post link or previous.
#// 
#// @since 2.5.0
#// 
#// @param string       $format         Link anchor format.
#// @param string       $link           Link permalink format.
#// @param bool         $in_same_term   Optional. Whether link should be in a same taxonomy term. Default false.
#// @param array|string $excluded_terms Optional. Array or comma-separated list of excluded category IDs. Default empty.
#// @param bool         $previous       Optional. Whether to display link to previous or next post. Default true.
#// @param string       $taxonomy       Optional. Taxonomy, if $in_same_term is true. Default 'category'.
#//
def adjacent_post_link(format=None, link=None, in_same_term=False, excluded_terms="", previous=True, taxonomy="category", *args_):
    
    php_print(get_adjacent_post_link(format, link, in_same_term, excluded_terms, previous, taxonomy))
# end def adjacent_post_link
#// 
#// Retrieves the link for a page number.
#// 
#// @since 1.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int  $pagenum Optional. Page number. Default 1.
#// @param bool $escape  Optional. Whether to escape the URL for display, with esc_url(). Defaults to true.
#// Otherwise, prepares the URL with esc_url_raw().
#// @return string The link URL for the given page number.
#//
def get_pagenum_link(pagenum=1, escape=True, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    pagenum = php_int(pagenum)
    request = remove_query_arg("paged")
    home_root = php_parse_url(home_url())
    home_root = home_root["path"] if (php_isset(lambda : home_root["path"])) else ""
    home_root = preg_quote(home_root, "|")
    request = php_preg_replace("|^" + home_root + "|i", "", request)
    request = php_preg_replace("|^/+|", "", request)
    if (not wp_rewrite.using_permalinks()) or is_admin():
        base = trailingslashit(get_bloginfo("url"))
        if pagenum > 1:
            result = add_query_arg("paged", pagenum, base + request)
        else:
            result = base + request
        # end if
    else:
        qs_regex = "|\\?.*?$|"
        php_preg_match(qs_regex, request, qs_match)
        if (not php_empty(lambda : qs_match[0])):
            query_string = qs_match[0]
            request = php_preg_replace(qs_regex, "", request)
        else:
            query_string = ""
        # end if
        request = php_preg_replace(str("|") + str(wp_rewrite.pagination_base) + str("/\\d+/?$|"), "", request)
        request = php_preg_replace("|^" + preg_quote(wp_rewrite.index, "|") + "|i", "", request)
        request = php_ltrim(request, "/")
        base = trailingslashit(get_bloginfo("url"))
        if wp_rewrite.using_index_permalinks() and pagenum > 1 or "" != request:
            base += wp_rewrite.index + "/"
        # end if
        if pagenum > 1:
            request = trailingslashit(request) if (not php_empty(lambda : request)) else request + user_trailingslashit(wp_rewrite.pagination_base + "/" + pagenum, "paged")
        # end if
        result = base + request + query_string
    # end if
    #// 
    #// Filters the page number link for the current request.
    #// 
    #// @since 2.5.0
    #// @since 5.2.0 Added the `$pagenum` argument.
    #// 
    #// @param string $result  The page number link.
    #// @param int    $pagenum The page number.
    #//
    result = apply_filters("get_pagenum_link", result, pagenum)
    if escape:
        return esc_url(result)
    else:
        return esc_url_raw(result)
    # end if
# end def get_pagenum_link
#// 
#// Retrieves the next posts page link.
#// 
#// Backported from 2.1.3 to 2.0.10.
#// 
#// @since 2.0.10
#// 
#// @global int $paged
#// 
#// @param int $max_page Optional. Max pages. Default 0.
#// @return string|void The link URL for next posts page.
#//
def get_next_posts_page_link(max_page=0, *args_):
    
    global paged
    php_check_if_defined("paged")
    if (not is_single()):
        if (not paged):
            paged = 1
        # end if
        nextpage = php_intval(paged) + 1
        if (not max_page) or max_page >= nextpage:
            return get_pagenum_link(nextpage)
        # end if
    # end if
# end def get_next_posts_page_link
#// 
#// Displays or retrieves the next posts page link.
#// 
#// @since 0.71
#// 
#// @param int   $max_page Optional. Max pages. Default 0.
#// @param bool  $echo     Optional. Whether to echo the link. Default true.
#// @return string|void The link URL for next posts page if `$echo = false`.
#//
def next_posts(max_page=0, echo=True, *args_):
    
    output = esc_url(get_next_posts_page_link(max_page))
    if echo:
        php_print(output)
    else:
        return output
    # end if
# end def next_posts
#// 
#// Retrieves the next posts page link.
#// 
#// @since 2.7.0
#// 
#// @global int      $paged
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string $label    Content for link text.
#// @param int    $max_page Optional. Max pages. Default 0.
#// @return string|void HTML-formatted next posts page link.
#//
def get_next_posts_link(label=None, max_page=0, *args_):
    
    global paged,wp_query
    php_check_if_defined("paged","wp_query")
    if (not max_page):
        max_page = wp_query.max_num_pages
    # end if
    if (not paged):
        paged = 1
    # end if
    nextpage = php_intval(paged) + 1
    if None == label:
        label = __("Next Page &raquo;")
    # end if
    if (not is_single()) and nextpage <= max_page:
        #// 
        #// Filters the anchor tag attributes for the next posts page link.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string $attributes Attributes for the anchor tag.
        #//
        attr = apply_filters("next_posts_link_attributes", "")
        return "<a href=\"" + next_posts(max_page, False) + str("\" ") + str(attr) + str(">") + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label) + "</a>"
    # end if
# end def get_next_posts_link
#// 
#// Displays the next posts page link.
#// 
#// @since 0.71
#// 
#// @param string $label    Content for link text.
#// @param int    $max_page Optional. Max pages. Default 0.
#//
def next_posts_link(label=None, max_page=0, *args_):
    
    php_print(get_next_posts_link(label, max_page))
# end def next_posts_link
#// 
#// Retrieves the previous posts page link.
#// 
#// Will only return string, if not on a single page or post.
#// 
#// Backported to 2.0.10 from 2.1.3.
#// 
#// @since 2.0.10
#// 
#// @global int $paged
#// 
#// @return string|void The link for the previous posts page.
#//
def get_previous_posts_page_link(*args_):
    
    global paged
    php_check_if_defined("paged")
    if (not is_single()):
        nextpage = php_intval(paged) - 1
        if nextpage < 1:
            nextpage = 1
        # end if
        return get_pagenum_link(nextpage)
    # end if
# end def get_previous_posts_page_link
#// 
#// Displays or retrieves the previous posts page link.
#// 
#// @since 0.71
#// 
#// @param bool $echo Optional. Whether to echo the link. Default true.
#// @return string|void The previous posts page link if `$echo = false`.
#//
def previous_posts(echo=True, *args_):
    
    output = esc_url(get_previous_posts_page_link())
    if echo:
        php_print(output)
    else:
        return output
    # end if
# end def previous_posts
#// 
#// Retrieves the previous posts page link.
#// 
#// @since 2.7.0
#// 
#// @global int $paged
#// 
#// @param string $label Optional. Previous page link text.
#// @return string|void HTML-formatted previous page link.
#//
def get_previous_posts_link(label=None, *args_):
    
    global paged
    php_check_if_defined("paged")
    if None == label:
        label = __("&laquo; Previous Page")
    # end if
    if (not is_single()) and paged > 1:
        #// 
        #// Filters the anchor tag attributes for the previous posts page link.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string $attributes Attributes for the anchor tag.
        #//
        attr = apply_filters("previous_posts_link_attributes", "")
        return "<a href=\"" + previous_posts(False) + str("\" ") + str(attr) + str(">") + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label) + "</a>"
    # end if
# end def get_previous_posts_link
#// 
#// Displays the previous posts page link.
#// 
#// @since 0.71
#// 
#// @param string $label Optional. Previous page link text.
#//
def previous_posts_link(label=None, *args_):
    
    php_print(get_previous_posts_link(label))
# end def previous_posts_link
#// 
#// Retrieves the post pages link navigation for previous and next pages.
#// 
#// @since 2.8.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string|array $args {
#// Optional. Arguments to build the post pages link navigation.
#// 
#// @type string $sep      Separator character. Default '&#8212;'.
#// @type string $prelabel Link text to display for the previous page link.
#// Default '&laquo; Previous Page'.
#// @type string $nxtlabel Link text to display for the next page link.
#// Default 'Next Page &raquo;'.
#// }
#// @return string The posts link navigation.
#//
def get_posts_nav_link(args=Array(), *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    return_ = ""
    if (not is_singular()):
        defaults = Array({"sep": " &#8212; ", "prelabel": __("&laquo; Previous Page"), "nxtlabel": __("Next Page &raquo;")})
        args = wp_parse_args(args, defaults)
        max_num_pages = wp_query.max_num_pages
        paged = get_query_var("paged")
        #// Only have sep if there's both prev and next results.
        if paged < 2 or paged >= max_num_pages:
            args["sep"] = ""
        # end if
        if max_num_pages > 1:
            return_ = get_previous_posts_link(args["prelabel"])
            return_ += php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", args["sep"])
            return_ += get_next_posts_link(args["nxtlabel"])
        # end if
    # end if
    return return_
# end def get_posts_nav_link
#// 
#// Displays the post pages link navigation for previous and next pages.
#// 
#// @since 0.71
#// 
#// @param string $sep      Optional. Separator for posts navigation links. Default empty.
#// @param string $prelabel Optional. Label for previous pages. Default empty.
#// @param string $nxtlabel Optional Label for next pages. Default empty.
#//
def posts_nav_link(sep="", prelabel="", nxtlabel="", *args_):
    
    args = php_array_filter(compact("sep", "prelabel", "nxtlabel"))
    php_print(get_posts_nav_link(args))
# end def posts_nav_link
#// 
#// Retrieves the navigation to next/previous post, when applicable.
#// 
#// @since 4.1.0
#// @since 4.4.0 Introduced the `in_same_term`, `excluded_terms`, and `taxonomy` arguments.
#// @since 5.3.0 Added the `aria_label` parameter.
#// 
#// @param array $args {
#// Optional. Default post navigation arguments. Default empty array.
#// 
#// @type string       $prev_text          Anchor text to display in the previous post link. Default '%title'.
#// @type string       $next_text          Anchor text to display in the next post link. Default '%title'.
#// @type bool         $in_same_term       Whether link should be in a same taxonomy term. Default false.
#// @type array|string $excluded_terms     Array or comma-separated list of excluded term IDs. Default empty.
#// @type string       $taxonomy           Taxonomy, if `$in_same_term` is true. Default 'category'.
#// @type string       $screen_reader_text Screen reader text for the nav element. Default 'Post navigation'.
#// @type string       $aria_label         ARIA label text for the nav element. Default 'Posts'.
#// }
#// @return string Markup for post links.
#//
def get_the_post_navigation(args=Array(), *args_):
    
    #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
    if (not php_empty(lambda : args["screen_reader_text"])) and php_empty(lambda : args["aria_label"]):
        args["aria_label"] = args["screen_reader_text"]
    # end if
    args = wp_parse_args(args, Array({"prev_text": "%title", "next_text": "%title", "in_same_term": False, "excluded_terms": "", "taxonomy": "category", "screen_reader_text": __("Post navigation"), "aria_label": __("Posts")}))
    navigation = ""
    previous = get_previous_post_link("<div class=\"nav-previous\">%link</div>", args["prev_text"], args["in_same_term"], args["excluded_terms"], args["taxonomy"])
    next = get_next_post_link("<div class=\"nav-next\">%link</div>", args["next_text"], args["in_same_term"], args["excluded_terms"], args["taxonomy"])
    #// Only add markup if there's somewhere to navigate to.
    if previous or next:
        navigation = _navigation_markup(previous + next, "post-navigation", args["screen_reader_text"], args["aria_label"])
    # end if
    return navigation
# end def get_the_post_navigation
#// 
#// Displays the navigation to next/previous post, when applicable.
#// 
#// @since 4.1.0
#// 
#// @param array $args Optional. See get_the_post_navigation() for available arguments.
#// Default empty array.
#//
def the_post_navigation(args=Array(), *args_):
    
    php_print(get_the_post_navigation(args))
# end def the_post_navigation
#// 
#// Returns the navigation to next/previous set of posts, when applicable.
#// 
#// @since 4.1.0
#// @since 5.3.0 Added the `aria_label` parameter.
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param array $args {
#// Optional. Default posts navigation arguments. Default empty array.
#// 
#// @type string $prev_text          Anchor text to display in the previous posts link.
#// Default 'Older posts'.
#// @type string $next_text          Anchor text to display in the next posts link.
#// Default 'Newer posts'.
#// @type string $screen_reader_text Screen reader text for the nav element.
#// Default 'Posts navigation'.
#// @type string $aria_label         ARIA label text for the nav element. Default 'Posts'.
#// }
#// @return string Markup for posts links.
#//
def get_the_posts_navigation(args=Array(), *args_):
    
    navigation = ""
    #// Don't print empty markup if there's only one page.
    if PHP_GLOBALS["wp_query"].max_num_pages > 1:
        #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
        if (not php_empty(lambda : args["screen_reader_text"])) and php_empty(lambda : args["aria_label"]):
            args["aria_label"] = args["screen_reader_text"]
        # end if
        args = wp_parse_args(args, Array({"prev_text": __("Older posts"), "next_text": __("Newer posts"), "screen_reader_text": __("Posts navigation"), "aria_label": __("Posts")}))
        next_link = get_previous_posts_link(args["next_text"])
        prev_link = get_next_posts_link(args["prev_text"])
        if prev_link:
            navigation += "<div class=\"nav-previous\">" + prev_link + "</div>"
        # end if
        if next_link:
            navigation += "<div class=\"nav-next\">" + next_link + "</div>"
        # end if
        navigation = _navigation_markup(navigation, "posts-navigation", args["screen_reader_text"], args["aria_label"])
    # end if
    return navigation
# end def get_the_posts_navigation
#// 
#// Displays the navigation to next/previous set of posts, when applicable.
#// 
#// @since 4.1.0
#// 
#// @param array $args Optional. See get_the_posts_navigation() for available arguments.
#// Default empty array.
#//
def the_posts_navigation(args=Array(), *args_):
    
    php_print(get_the_posts_navigation(args))
# end def the_posts_navigation
#// 
#// Retrieves a paginated navigation to next/previous set of posts, when applicable.
#// 
#// @since 4.1.0
#// @since 5.3.0 Added the `aria_label` parameter.
#// 
#// @param array $args {
#// Optional. Default pagination arguments, see paginate_links().
#// 
#// @type string $screen_reader_text Screen reader text for navigation element.
#// Default 'Posts navigation'.
#// @type string $aria_label         ARIA label text for the nav element. Default 'Posts'.
#// }
#// @return string Markup for pagination links.
#//
def get_the_posts_pagination(args=Array(), *args_):
    
    navigation = ""
    #// Don't print empty markup if there's only one page.
    if PHP_GLOBALS["wp_query"].max_num_pages > 1:
        #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
        if (not php_empty(lambda : args["screen_reader_text"])) and php_empty(lambda : args["aria_label"]):
            args["aria_label"] = args["screen_reader_text"]
        # end if
        args = wp_parse_args(args, Array({"mid_size": 1, "prev_text": _x("Previous", "previous set of posts"), "next_text": _x("Next", "next set of posts"), "screen_reader_text": __("Posts navigation"), "aria_label": __("Posts")}))
        #// Make sure we get a string back. Plain is the next best thing.
        if (php_isset(lambda : args["type"])) and "array" == args["type"]:
            args["type"] = "plain"
        # end if
        #// Set up paginated links.
        links = paginate_links(args)
        if links:
            navigation = _navigation_markup(links, "pagination", args["screen_reader_text"], args["aria_label"])
        # end if
    # end if
    return navigation
# end def get_the_posts_pagination
#// 
#// Displays a paginated navigation to next/previous set of posts, when applicable.
#// 
#// @since 4.1.0
#// 
#// @param array $args Optional. See get_the_posts_pagination() for available arguments.
#// Default empty array.
#//
def the_posts_pagination(args=Array(), *args_):
    
    php_print(get_the_posts_pagination(args))
# end def the_posts_pagination
#// 
#// Wraps passed links in navigational markup.
#// 
#// @since 4.1.0
#// @since 5.3.0 Added the `aria_label` parameter.
#// @access private
#// 
#// @param string $links              Navigational links.
#// @param string $class              Optional. Custom class for the nav element. Default: 'posts-navigation'.
#// @param string $screen_reader_text Optional. Screen reader text for the nav element. Default: 'Posts navigation'.
#// @param string $aria_label         Optional. ARIA label for the nav element. Default: same value as $screen_reader_text.
#// @return string Navigation template tag.
#//
def _navigation_markup(links=None, class_="posts-navigation", screen_reader_text="", aria_label="", *args_):
    
    if php_empty(lambda : screen_reader_text):
        screen_reader_text = __("Posts navigation")
    # end if
    if php_empty(lambda : aria_label):
        aria_label = screen_reader_text
    # end if
    template = """
    <nav class=\"navigation %1$s\" role=\"navigation\" aria-label=\"%4$s\">
    <h2 class=\"screen-reader-text\">%2$s</h2>
    <div class=\"nav-links\">%3$s</div>
    </nav>"""
    #// 
    #// Filters the navigation markup template.
    #// 
    #// Note: The filtered template HTML must contain specifiers for the navigation
    #// class (%1$s), the screen-reader-text value (%2$s), placement of the navigation
    #// links (%3$s), and ARIA label text if screen-reader-text does not fit that (%4$s):
    #// 
    #// <nav class="navigation %1$s" role="navigation" aria-label="%4$s">
    #// <h2 class="screen-reader-text">%2$s</h2>
    #// <div class="nav-links">%3$s</div>
    #// </nav>
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $template The default template.
    #// @param string $class    The class passed by the calling function.
    #// @return string Navigation template.
    #//
    template = apply_filters("navigation_markup_template", template, class_)
    return php_sprintf(template, sanitize_html_class(class_), esc_html(screen_reader_text), links, esc_html(aria_label))
# end def _navigation_markup
#// 
#// Retrieves the comments page number link.
#// 
#// @since 2.7.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int $pagenum  Optional. Page number. Default 1.
#// @param int $max_page Optional. The maximum number of comment pages. Default 0.
#// @return string The comments page number link URL.
#//
def get_comments_pagenum_link(pagenum=1, max_page=0, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    pagenum = php_int(pagenum)
    result = get_permalink()
    if "newest" == get_option("default_comments_page"):
        if pagenum != max_page:
            if wp_rewrite.using_permalinks():
                result = user_trailingslashit(trailingslashit(result) + wp_rewrite.comments_pagination_base + "-" + pagenum, "commentpaged")
            else:
                result = add_query_arg("cpage", pagenum, result)
            # end if
        # end if
    elif pagenum > 1:
        if wp_rewrite.using_permalinks():
            result = user_trailingslashit(trailingslashit(result) + wp_rewrite.comments_pagination_base + "-" + pagenum, "commentpaged")
        else:
            result = add_query_arg("cpage", pagenum, result)
        # end if
    # end if
    result += "#comments"
    #// 
    #// Filters the comments page number link for the current request.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $result The comments page number link.
    #//
    return apply_filters("get_comments_pagenum_link", result)
# end def get_comments_pagenum_link
#// 
#// Retrieves the link to the next comments page.
#// 
#// @since 2.7.1
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string $label    Optional. Label for link text. Default empty.
#// @param int    $max_page Optional. Max page. Default 0.
#// @return string|void HTML-formatted link for the next page of comments.
#//
def get_next_comments_link(label="", max_page=0, *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if (not is_singular()):
        return
    # end if
    page = get_query_var("cpage")
    if (not page):
        page = 1
    # end if
    nextpage = php_intval(page) + 1
    if php_empty(lambda : max_page):
        max_page = wp_query.max_num_comment_pages
    # end if
    if php_empty(lambda : max_page):
        max_page = get_comment_pages_count()
    # end if
    if nextpage > max_page:
        return
    # end if
    if php_empty(lambda : label):
        label = __("Newer Comments &raquo;")
    # end if
    #// 
    #// Filters the anchor tag attributes for the next comments page link.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $attributes Attributes for the anchor tag.
    #//
    return "<a href=\"" + esc_url(get_comments_pagenum_link(nextpage, max_page)) + "\" " + apply_filters("next_comments_link_attributes", "") + ">" + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label) + "</a>"
# end def get_next_comments_link
#// 
#// Displays the link to the next comments page.
#// 
#// @since 2.7.0
#// 
#// @param string $label    Optional. Label for link text. Default empty.
#// @param int    $max_page Optional. Max page. Default 0.
#//
def next_comments_link(label="", max_page=0, *args_):
    
    php_print(get_next_comments_link(label, max_page))
# end def next_comments_link
#// 
#// Retrieves the link to the previous comments page.
#// 
#// @since 2.7.1
#// 
#// @param string $label Optional. Label for comments link text. Default empty.
#// @return string|void HTML-formatted link for the previous page of comments.
#//
def get_previous_comments_link(label="", *args_):
    
    if (not is_singular()):
        return
    # end if
    page = get_query_var("cpage")
    if php_intval(page) <= 1:
        return
    # end if
    prevpage = php_intval(page) - 1
    if php_empty(lambda : label):
        label = __("&laquo; Older Comments")
    # end if
    #// 
    #// Filters the anchor tag attributes for the previous comments page link.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $attributes Attributes for the anchor tag.
    #//
    return "<a href=\"" + esc_url(get_comments_pagenum_link(prevpage)) + "\" " + apply_filters("previous_comments_link_attributes", "") + ">" + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label) + "</a>"
# end def get_previous_comments_link
#// 
#// Displays the link to the previous comments page.
#// 
#// @since 2.7.0
#// 
#// @param string $label Optional. Label for comments link text. Default empty.
#//
def previous_comments_link(label="", *args_):
    
    php_print(get_previous_comments_link(label))
# end def previous_comments_link
#// 
#// Displays or retrieves pagination links for the comments on the current post.
#// 
#// @see paginate_links()
#// @since 2.7.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string|array $args Optional args. See paginate_links(). Default empty array.
#// @return void|string|array Void if 'echo' argument is true and 'type' is not an array,
#// or if the query is not for an existing single post of any post type.
#// Otherwise, markup for comment page links or array of comment page links,
#// depending on 'type' argument.
#//
def paginate_comments_links(args=Array(), *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not is_singular()):
        return
    # end if
    page = get_query_var("cpage")
    if (not page):
        page = 1
    # end if
    max_page = get_comment_pages_count()
    defaults = Array({"base": add_query_arg("cpage", "%#%"), "format": "", "total": max_page, "current": page, "echo": True, "type": "plain", "add_fragment": "#comments"})
    if wp_rewrite.using_permalinks():
        defaults["base"] = user_trailingslashit(trailingslashit(get_permalink()) + wp_rewrite.comments_pagination_base + "-%#%", "commentpaged")
    # end if
    args = wp_parse_args(args, defaults)
    page_links = paginate_links(args)
    if args["echo"] and "array" != args["type"]:
        php_print(page_links)
    else:
        return page_links
    # end if
# end def paginate_comments_links
#// 
#// Retrieves navigation to next/previous set of comments, when applicable.
#// 
#// @since 4.4.0
#// @since 5.3.0 Added the `aria_label` parameter.
#// 
#// @param array $args {
#// Optional. Default comments navigation arguments.
#// 
#// @type string $prev_text          Anchor text to display in the previous comments link.
#// Default 'Older comments'.
#// @type string $next_text          Anchor text to display in the next comments link.
#// Default 'Newer comments'.
#// @type string $screen_reader_text Screen reader text for the nav element. Default 'Comments navigation'.
#// @type string $aria_label         ARIA label text for the nav element. Default 'Comments'.
#// }
#// @return string Markup for comments links.
#//
def get_the_comments_navigation(args=Array(), *args_):
    
    navigation = ""
    #// Are there comments to navigate through?
    if get_comment_pages_count() > 1:
        #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
        if (not php_empty(lambda : args["screen_reader_text"])) and php_empty(lambda : args["aria_label"]):
            args["aria_label"] = args["screen_reader_text"]
        # end if
        args = wp_parse_args(args, Array({"prev_text": __("Older comments"), "next_text": __("Newer comments"), "screen_reader_text": __("Comments navigation"), "aria_label": __("Comments")}))
        prev_link = get_previous_comments_link(args["prev_text"])
        next_link = get_next_comments_link(args["next_text"])
        if prev_link:
            navigation += "<div class=\"nav-previous\">" + prev_link + "</div>"
        # end if
        if next_link:
            navigation += "<div class=\"nav-next\">" + next_link + "</div>"
        # end if
        navigation = _navigation_markup(navigation, "comment-navigation", args["screen_reader_text"], args["aria_label"])
    # end if
    return navigation
# end def get_the_comments_navigation
#// 
#// Displays navigation to next/previous set of comments, when applicable.
#// 
#// @since 4.4.0
#// 
#// @param array $args See get_the_comments_navigation() for available arguments. Default empty array.
#//
def the_comments_navigation(args=Array(), *args_):
    
    php_print(get_the_comments_navigation(args))
# end def the_comments_navigation
#// 
#// Retrieves a paginated navigation to next/previous set of comments, when applicable.
#// 
#// @since 4.4.0
#// @since 5.3.0 Added the `aria_label` parameter.
#// 
#// @see paginate_comments_links()
#// 
#// @param array $args {
#// Optional. Default pagination arguments.
#// 
#// @type string $screen_reader_text Screen reader text for the nav element. Default 'Comments navigation'.
#// @type string $aria_label         ARIA label text for the nav element. Default 'Comments'.
#// }
#// @return string Markup for pagination links.
#//
def get_the_comments_pagination(args=Array(), *args_):
    
    navigation = ""
    #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
    if (not php_empty(lambda : args["screen_reader_text"])) and php_empty(lambda : args["aria_label"]):
        args["aria_label"] = args["screen_reader_text"]
    # end if
    args = wp_parse_args(args, Array({"screen_reader_text": __("Comments navigation"), "aria_label": __("Comments")}))
    args["echo"] = False
    #// Make sure we get a string back. Plain is the next best thing.
    if (php_isset(lambda : args["type"])) and "array" == args["type"]:
        args["type"] = "plain"
    # end if
    links = paginate_comments_links(args)
    if links:
        navigation = _navigation_markup(links, "comments-pagination", args["screen_reader_text"], args["aria_label"])
    # end if
    return navigation
# end def get_the_comments_pagination
#// 
#// Displays a paginated navigation to next/previous set of comments, when applicable.
#// 
#// @since 4.4.0
#// 
#// @param array $args See get_the_comments_pagination() for available arguments. Default empty array.
#//
def the_comments_pagination(args=Array(), *args_):
    
    php_print(get_the_comments_pagination(args))
# end def the_comments_pagination
#// 
#// Retrieves the URL for the current site where the front end is accessible.
#// 
#// Returns the 'home' option with the appropriate protocol. The protocol will be 'https'
#// if is_ssl() evaluates to true; otherwise, it will be the same as the 'home' option.
#// If `$scheme` is 'http' or 'https', is_ssl() is overridden.
#// 
#// @since 3.0.0
#// 
#// @param  string      $path   Optional. Path relative to the home URL. Default empty.
#// @param  string|null $scheme Optional. Scheme to give the home URL context. Accepts
#// 'http', 'https', 'relative', 'rest', or null. Default null.
#// @return string Home URL link with optional path appended.
#//
def home_url(path="", scheme=None, *args_):
    
    return get_home_url(None, path, scheme)
# end def home_url
#// 
#// Retrieves the URL for a given site where the front end is accessible.
#// 
#// Returns the 'home' option with the appropriate protocol. The protocol will be 'https'
#// if is_ssl() evaluates to true; otherwise, it will be the same as the 'home' option.
#// If `$scheme` is 'http' or 'https', is_ssl() is overridden.
#// 
#// @since 3.0.0
#// 
#// @global string $pagenow
#// 
#// @param  int         $blog_id Optional. Site ID. Default null (current site).
#// @param  string      $path    Optional. Path relative to the home URL. Default empty.
#// @param  string|null $scheme  Optional. Scheme to give the home URL context. Accepts
#// 'http', 'https', 'relative', 'rest', or null. Default null.
#// @return string Home URL link with optional path appended.
#//
def get_home_url(blog_id=None, path="", scheme=None, *args_):
    
    global pagenow
    php_check_if_defined("pagenow")
    orig_scheme = scheme
    if php_empty(lambda : blog_id) or (not is_multisite()):
        url = get_option("home")
    else:
        switch_to_blog(blog_id)
        url = get_option("home")
        restore_current_blog()
    # end if
    if (not php_in_array(scheme, Array("http", "https", "relative"))):
        if is_ssl() and (not is_admin()) and "wp-login.php" != pagenow:
            scheme = "https"
        else:
            scheme = php_parse_url(url, PHP_URL_SCHEME)
        # end if
    # end if
    url = set_url_scheme(url, scheme)
    if path and php_is_string(path):
        url += "/" + php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the home URL.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string      $url         The complete home URL including scheme and path.
    #// @param string      $path        Path relative to the home URL. Blank string if no path is specified.
    #// @param string|null $orig_scheme Scheme to give the home URL context. Accepts 'http', 'https',
    #// 'relative', 'rest', or null.
    #// @param int|null    $blog_id     Site ID, or null for the current site.
    #//
    return apply_filters("home_url", url, path, orig_scheme, blog_id)
# end def get_home_url
#// 
#// Retrieves the URL for the current site where WordPress application files
#// (e.g. wp-blog-header.php or the wp-admin/ folder) are accessible.
#// 
#// Returns the 'site_url' option with the appropriate protocol, 'https' if
#// is_ssl() and 'http' otherwise. If $scheme is 'http' or 'https', is_ssl() is
#// overridden.
#// 
#// @since 3.0.0
#// 
#// @param string $path   Optional. Path relative to the site URL. Default empty.
#// @param string $scheme Optional. Scheme to give the site URL context. See set_url_scheme().
#// @return string Site URL link with optional path appended.
#//
def site_url(path="", scheme=None, *args_):
    
    return get_site_url(None, path, scheme)
# end def site_url
#// 
#// Retrieves the URL for a given site where WordPress application files
#// (e.g. wp-blog-header.php or the wp-admin/ folder) are accessible.
#// 
#// Returns the 'site_url' option with the appropriate protocol, 'https' if
#// is_ssl() and 'http' otherwise. If `$scheme` is 'http' or 'https',
#// `is_ssl()` is overridden.
#// 
#// @since 3.0.0
#// 
#// @param int    $blog_id Optional. Site ID. Default null (current site).
#// @param string $path    Optional. Path relative to the site URL. Default empty.
#// @param string $scheme  Optional. Scheme to give the site URL context. Accepts
#// 'http', 'https', 'login', 'login_post', 'admin', or
#// 'relative'. Default null.
#// @return string Site URL link with optional path appended.
#//
def get_site_url(blog_id=None, path="", scheme=None, *args_):
    
    if php_empty(lambda : blog_id) or (not is_multisite()):
        url = get_option("siteurl")
    else:
        switch_to_blog(blog_id)
        url = get_option("siteurl")
        restore_current_blog()
    # end if
    url = set_url_scheme(url, scheme)
    if path and php_is_string(path):
        url += "/" + php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the site URL.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string      $url     The complete site URL including scheme and path.
    #// @param string      $path    Path relative to the site URL. Blank string if no path is specified.
    #// @param string|null $scheme  Scheme to give the site URL context. Accepts 'http', 'https', 'login',
    #// 'login_post', 'admin', 'relative' or null.
    #// @param int|null    $blog_id Site ID, or null for the current site.
    #//
    return apply_filters("site_url", url, path, scheme, blog_id)
# end def get_site_url
#// 
#// Retrieves the URL to the admin area for the current site.
#// 
#// @since 2.6.0
#// 
#// @param string $path   Optional path relative to the admin URL.
#// @param string $scheme The scheme to use. Default is 'admin', which obeys force_ssl_admin() and is_ssl().
#// 'http' or 'https' can be passed to force those schemes.
#// @return string Admin URL link with optional path appended.
#//
def admin_url(path="", scheme="admin", *args_):
    
    return get_admin_url(None, path, scheme)
# end def admin_url
#// 
#// Retrieves the URL to the admin area for a given site.
#// 
#// @since 3.0.0
#// 
#// @param int    $blog_id Optional. Site ID. Default null (current site).
#// @param string $path    Optional. Path relative to the admin URL. Default empty.
#// @param string $scheme  Optional. The scheme to use. Accepts 'http' or 'https',
#// to force those schemes. Default 'admin', which obeys
#// force_ssl_admin() and is_ssl().
#// @return string Admin URL link with optional path appended.
#//
def get_admin_url(blog_id=None, path="", scheme="admin", *args_):
    
    url = get_site_url(blog_id, "wp-admin/", scheme)
    if path and php_is_string(path):
        url += php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the admin area URL.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string   $url     The complete admin area URL including scheme and path.
    #// @param string   $path    Path relative to the admin area URL. Blank string if no path is specified.
    #// @param int|null $blog_id Site ID, or null for the current site.
    #//
    return apply_filters("admin_url", url, path, blog_id)
# end def get_admin_url
#// 
#// Retrieves the URL to the includes directory.
#// 
#// @since 2.6.0
#// 
#// @param string $path   Optional. Path relative to the includes URL. Default empty.
#// @param string $scheme Optional. Scheme to give the includes URL context. Accepts
#// 'http', 'https', or 'relative'. Default null.
#// @return string Includes URL link with optional path appended.
#//
def includes_url(path="", scheme=None, *args_):
    
    url = site_url("/" + WPINC + "/", scheme)
    if path and php_is_string(path):
        url += php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the URL to the includes directory.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $url  The complete URL to the includes directory including scheme and path.
    #// @param string $path Path relative to the URL to the wp-includes directory. Blank string
    #// if no path is specified.
    #//
    return apply_filters("includes_url", url, path)
# end def includes_url
#// 
#// Retrieves the URL to the content directory.
#// 
#// @since 2.6.0
#// 
#// @param string $path Optional. Path relative to the content URL. Default empty.
#// @return string Content URL link with optional path appended.
#//
def content_url(path="", *args_):
    
    url = set_url_scheme(WP_CONTENT_URL)
    if path and php_is_string(path):
        url += "/" + php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the URL to the content directory.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $url  The complete URL to the content directory including scheme and path.
    #// @param string $path Path relative to the URL to the content directory. Blank string
    #// if no path is specified.
    #//
    return apply_filters("content_url", url, path)
# end def content_url
#// 
#// Retrieves a URL within the plugins or mu-plugins directory.
#// 
#// Defaults to the plugins directory URL if no arguments are supplied.
#// 
#// @since 2.6.0
#// 
#// @param  string $path   Optional. Extra path appended to the end of the URL, including
#// the relative directory if $plugin is supplied. Default empty.
#// @param  string $plugin Optional. A full path to a file inside a plugin or mu-plugin.
#// The URL will be relative to its directory. Default empty.
#// Typically this is done by passing `__FILE__` as the argument.
#// @return string Plugins URL link with optional paths appended.
#//
def plugins_url(path="", plugin="", *args_):
    
    path = wp_normalize_path(path)
    plugin = wp_normalize_path(plugin)
    mu_plugin_dir = wp_normalize_path(WPMU_PLUGIN_DIR)
    if (not php_empty(lambda : plugin)) and 0 == php_strpos(plugin, mu_plugin_dir):
        url = WPMU_PLUGIN_URL
    else:
        url = WP_PLUGIN_URL
    # end if
    url = set_url_scheme(url)
    if (not php_empty(lambda : plugin)) and php_is_string(plugin):
        folder = php_dirname(plugin_basename(plugin))
        if "." != folder:
            url += "/" + php_ltrim(folder, "/")
        # end if
    # end if
    if path and php_is_string(path):
        url += "/" + php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the URL to the plugins directory.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $url    The complete URL to the plugins directory including scheme and path.
    #// @param string $path   Path relative to the URL to the plugins directory. Blank string
    #// if no path is specified.
    #// @param string $plugin The plugin file path to be relative to. Blank string if no plugin
    #// is specified.
    #//
    return apply_filters("plugins_url", url, path, plugin)
# end def plugins_url
#// 
#// Retrieves the site URL for the current network.
#// 
#// Returns the site URL with the appropriate protocol, 'https' if
#// is_ssl() and 'http' otherwise. If $scheme is 'http' or 'https', is_ssl() is
#// overridden.
#// 
#// @since 3.0.0
#// 
#// @see set_url_scheme()
#// 
#// @param string $path   Optional. Path relative to the site URL. Default empty.
#// @param string $scheme Optional. Scheme to give the site URL context. Accepts
#// 'http', 'https', or 'relative'. Default null.
#// @return string Site URL link with optional path appended.
#//
def network_site_url(path="", scheme=None, *args_):
    
    if (not is_multisite()):
        return site_url(path, scheme)
    # end if
    current_network = get_network()
    if "relative" == scheme:
        url = current_network.path
    else:
        url = set_url_scheme("http://" + current_network.domain + current_network.path, scheme)
    # end if
    if path and php_is_string(path):
        url += php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the network site URL.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string      $url    The complete network site URL including scheme and path.
    #// @param string      $path   Path relative to the network site URL. Blank string if
    #// no path is specified.
    #// @param string|null $scheme Scheme to give the URL context. Accepts 'http', 'https',
    #// 'relative' or null.
    #//
    return apply_filters("network_site_url", url, path, scheme)
# end def network_site_url
#// 
#// Retrieves the home URL for the current network.
#// 
#// Returns the home URL with the appropriate protocol, 'https' is_ssl()
#// and 'http' otherwise. If `$scheme` is 'http' or 'https', `is_ssl()` is
#// overridden.
#// 
#// @since 3.0.0
#// 
#// @param  string $path   Optional. Path relative to the home URL. Default empty.
#// @param  string $scheme Optional. Scheme to give the home URL context. Accepts
#// 'http', 'https', or 'relative'. Default null.
#// @return string Home URL link with optional path appended.
#//
def network_home_url(path="", scheme=None, *args_):
    
    if (not is_multisite()):
        return home_url(path, scheme)
    # end if
    current_network = get_network()
    orig_scheme = scheme
    if (not php_in_array(scheme, Array("http", "https", "relative"))):
        scheme = "https" if is_ssl() and (not is_admin()) else "http"
    # end if
    if "relative" == scheme:
        url = current_network.path
    else:
        url = set_url_scheme("http://" + current_network.domain + current_network.path, scheme)
    # end if
    if path and php_is_string(path):
        url += php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the network home URL.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string      $url         The complete network home URL including scheme and path.
    #// @param string      $path        Path relative to the network home URL. Blank string
    #// if no path is specified.
    #// @param string|null $orig_scheme Scheme to give the URL context. Accepts 'http', 'https',
    #// 'relative' or null.
    #//
    return apply_filters("network_home_url", url, path, orig_scheme)
# end def network_home_url
#// 
#// Retrieves the URL to the admin area for the network.
#// 
#// @since 3.0.0
#// 
#// @param string $path   Optional path relative to the admin URL. Default empty.
#// @param string $scheme Optional. The scheme to use. Default is 'admin', which obeys force_ssl_admin()
#// and is_ssl(). 'http' or 'https' can be passed to force those schemes.
#// @return string Admin URL link with optional path appended.
#//
def network_admin_url(path="", scheme="admin", *args_):
    
    if (not is_multisite()):
        return admin_url(path, scheme)
    # end if
    url = network_site_url("wp-admin/network/", scheme)
    if path and php_is_string(path):
        url += php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the network admin URL.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $url  The complete network admin URL including scheme and path.
    #// @param string $path Path relative to the network admin URL. Blank string if
    #// no path is specified.
    #//
    return apply_filters("network_admin_url", url, path)
# end def network_admin_url
#// 
#// Retrieves the URL to the admin area for the current user.
#// 
#// @since 3.0.0
#// 
#// @param string $path   Optional. Path relative to the admin URL. Default empty.
#// @param string $scheme Optional. The scheme to use. Default is 'admin', which obeys force_ssl_admin()
#// and is_ssl(). 'http' or 'https' can be passed to force those schemes.
#// @return string Admin URL link with optional path appended.
#//
def user_admin_url(path="", scheme="admin", *args_):
    
    url = network_site_url("wp-admin/user/", scheme)
    if path and php_is_string(path):
        url += php_ltrim(path, "/")
    # end if
    #// 
    #// Filters the user admin URL for the current user.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $url  The complete URL including scheme and path.
    #// @param string $path Path relative to the URL. Blank string if
    #// no path is specified.
    #//
    return apply_filters("user_admin_url", url, path)
# end def user_admin_url
#// 
#// Retrieves the URL to the admin area for either the current site or the network depending on context.
#// 
#// @since 3.1.0
#// 
#// @param string $path   Optional. Path relative to the admin URL. Default empty.
#// @param string $scheme Optional. The scheme to use. Default is 'admin', which obeys force_ssl_admin()
#// and is_ssl(). 'http' or 'https' can be passed to force those schemes.
#// @return string Admin URL link with optional path appended.
#//
def self_admin_url(path="", scheme="admin", *args_):
    
    if is_network_admin():
        url = network_admin_url(path, scheme)
    elif is_user_admin():
        url = user_admin_url(path, scheme)
    else:
        url = admin_url(path, scheme)
    # end if
    #// 
    #// Filters the admin URL for the current site or network depending on context.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $url    The complete URL including scheme and path.
    #// @param string $path   Path relative to the URL. Blank string if no path is specified.
    #// @param string $scheme The scheme to use.
    #//
    return apply_filters("self_admin_url", url, path, scheme)
# end def self_admin_url
#// 
#// Sets the scheme for a URL.
#// 
#// @since 3.4.0
#// @since 4.4.0 The 'rest' scheme was added.
#// 
#// @param string      $url    Absolute URL that includes a scheme
#// @param string|null $scheme Optional. Scheme to give $url. Currently 'http', 'https', 'login',
#// 'login_post', 'admin', 'relative', 'rest', 'rpc', or null. Default null.
#// @return string $url URL with chosen scheme.
#//
def set_url_scheme(url=None, scheme=None, *args_):
    
    orig_scheme = scheme
    if (not scheme):
        scheme = "https" if is_ssl() else "http"
    elif "admin" == scheme or "login" == scheme or "login_post" == scheme or "rpc" == scheme:
        scheme = "https" if is_ssl() or force_ssl_admin() else "http"
    elif "http" != scheme and "https" != scheme and "relative" != scheme:
        scheme = "https" if is_ssl() else "http"
    # end if
    url = php_trim(url)
    if php_substr(url, 0, 2) == "//":
        url = "http:" + url
    # end if
    if "relative" == scheme:
        url = php_ltrim(php_preg_replace("#^\\w+://[^/]*#", "", url))
        if "" != url and "/" == url[0]:
            url = "/" + php_ltrim(url, "/   \n\r ")
        # end if
    else:
        url = php_preg_replace("#^\\w+://#", scheme + "://", url)
    # end if
    #// 
    #// Filters the resulting URL after setting the scheme.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string      $url         The complete URL including scheme and path.
    #// @param string      $scheme      Scheme applied to the URL. One of 'http', 'https', or 'relative'.
    #// @param string|null $orig_scheme Scheme requested for the URL. One of 'http', 'https', 'login',
    #// 'login_post', 'admin', 'relative', 'rest', 'rpc', or null.
    #//
    return apply_filters("set_url_scheme", url, scheme, orig_scheme)
# end def set_url_scheme
#// 
#// Retrieves the URL to the user's dashboard.
#// 
#// If a user does not belong to any site, the global user dashboard is used. If the user
#// belongs to the current site, the dashboard for the current site is returned. If the user
#// cannot edit the current site, the dashboard to the user's primary site is returned.
#// 
#// @since 3.1.0
#// 
#// @param int    $user_id Optional. User ID. Defaults to current user.
#// @param string $path    Optional path relative to the dashboard. Use only paths known to
#// both site and user admins. Default empty.
#// @param string $scheme  The scheme to use. Default is 'admin', which obeys force_ssl_admin()
#// and is_ssl(). 'http' or 'https' can be passed to force those schemes.
#// @return string Dashboard URL link with optional path appended.
#//
def get_dashboard_url(user_id=0, path="", scheme="admin", *args_):
    
    user_id = php_int(user_id) if user_id else get_current_user_id()
    blogs = get_blogs_of_user(user_id)
    if is_multisite() and (not user_can(user_id, "manage_network")) and php_empty(lambda : blogs):
        url = user_admin_url(path, scheme)
    elif (not is_multisite()):
        url = admin_url(path, scheme)
    else:
        current_blog = get_current_blog_id()
        if current_blog and user_can(user_id, "manage_network") or php_in_array(current_blog, php_array_keys(blogs)):
            url = admin_url(path, scheme)
        else:
            active = get_active_blog_for_user(user_id)
            if active:
                url = get_admin_url(active.blog_id, path, scheme)
            else:
                url = user_admin_url(path, scheme)
            # end if
        # end if
    # end if
    #// 
    #// Filters the dashboard URL for a user.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $url     The complete URL including scheme and path.
    #// @param int    $user_id The user ID.
    #// @param string $path    Path relative to the URL. Blank string if no path is specified.
    #// @param string $scheme  Scheme to give the URL context. Accepts 'http', 'https', 'login',
    #// 'login_post', 'admin', 'relative' or null.
    #//
    return apply_filters("user_dashboard_url", url, user_id, path, scheme)
# end def get_dashboard_url
#// 
#// Retrieves the URL to the user's profile editor.
#// 
#// @since 3.1.0
#// 
#// @param int    $user_id Optional. User ID. Defaults to current user.
#// @param string $scheme  Optional. The scheme to use. Default is 'admin', which obeys force_ssl_admin()
#// and is_ssl(). 'http' or 'https' can be passed to force those schemes.
#// @return string Dashboard URL link with optional path appended.
#//
def get_edit_profile_url(user_id=0, scheme="admin", *args_):
    
    user_id = php_int(user_id) if user_id else get_current_user_id()
    if is_user_admin():
        url = user_admin_url("profile.php", scheme)
    elif is_network_admin():
        url = network_admin_url("profile.php", scheme)
    else:
        url = get_dashboard_url(user_id, "profile.php", scheme)
    # end if
    #// 
    #// Filters the URL for a user's profile editor.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $url     The complete URL including scheme and path.
    #// @param int    $user_id The user ID.
    #// @param string $scheme  Scheme to give the URL context. Accepts 'http', 'https', 'login',
    #// 'login_post', 'admin', 'relative' or null.
    #//
    return apply_filters("edit_profile_url", url, user_id, scheme)
# end def get_edit_profile_url
#// 
#// Returns the canonical URL for a post.
#// 
#// When the post is the same as the current requested page the function will handle the
#// pagination arguments too.
#// 
#// @since 4.6.0
#// 
#// @param int|WP_Post $post Optional. Post ID or object. Default is global `$post`.
#// @return string|false The canonical URL, or false if the post does not exist or has not
#// been published yet.
#//
def wp_get_canonical_url(post=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    if "publish" != post.post_status:
        return False
    # end if
    canonical_url = get_permalink(post)
    #// If a canonical is being generated for the current page, make sure it has pagination if needed.
    if get_queried_object_id() == post.ID:
        page = get_query_var("page", 0)
        if page >= 2:
            if "" == get_option("permalink_structure"):
                canonical_url = add_query_arg("page", page, canonical_url)
            else:
                canonical_url = trailingslashit(canonical_url) + user_trailingslashit(page, "single_paged")
            # end if
        # end if
        cpage = get_query_var("cpage", 0)
        if cpage:
            canonical_url = get_comments_pagenum_link(cpage)
        # end if
    # end if
    #// 
    #// Filters the canonical URL for a post.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string  $canonical_url The post's canonical URL.
    #// @param WP_Post $post          Post object.
    #//
    return apply_filters("get_canonical_url", canonical_url, post)
# end def wp_get_canonical_url
#// 
#// Outputs rel=canonical for singular queries.
#// 
#// @since 2.9.0
#// @since 4.6.0 Adjusted to use `wp_get_canonical_url()`.
#//
def rel_canonical(*args_):
    
    if (not is_singular()):
        return
    # end if
    id = get_queried_object_id()
    if 0 == id:
        return
    # end if
    url = wp_get_canonical_url(id)
    if (not php_empty(lambda : url)):
        php_print("<link rel=\"canonical\" href=\"" + esc_url(url) + "\" />" + "\n")
    # end if
# end def rel_canonical
#// 
#// Returns a shortlink for a post, page, attachment, or site.
#// 
#// This function exists to provide a shortlink tag that all themes and plugins can target.
#// A plugin must hook in to provide the actual shortlinks. Default shortlink support is
#// limited to providing ?p= style links for posts. Plugins can short-circuit this function
#// via the {@see 'pre_get_shortlink'} filter or filter the output via the {@see 'get_shortlink'}
#// filter.
#// 
#// @since 3.0.0
#// 
#// @param int    $id          Optional. A post or site id. Default is 0, which means the current post or site.
#// @param string $context     Optional. Whether the id is a 'site' id, 'post' id, or 'media' id. If 'post',
#// the post_type of the post is consulted. If 'query', the current query is consulted
#// to determine the id and context. Default 'post'.
#// @param bool   $allow_slugs Optional. Whether to allow post slugs in the shortlink. It is up to the plugin how
#// and whether to honor this. Default true.
#// @return string A shortlink or an empty string if no shortlink exists for the requested resource or if shortlinks
#// are not enabled.
#//
def wp_get_shortlink(id=0, context="post", allow_slugs=True, *args_):
    
    #// 
    #// Filters whether to preempt generating a shortlink for the given post.
    #// 
    #// Passing a truthy value to the filter will effectively short-circuit the
    #// shortlink-generation process, returning that value instead.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool|string $return      Short-circuit return value. Either false or a URL string.
    #// @param int         $id          Post ID, or 0 for the current post.
    #// @param string      $context     The context for the link. One of 'post' or 'query',
    #// @param bool        $allow_slugs Whether to allow post slugs in the shortlink.
    #//
    shortlink = apply_filters("pre_get_shortlink", False, id, context, allow_slugs)
    if False != shortlink:
        return shortlink
    # end if
    post_id = 0
    if "query" == context and is_singular():
        post_id = get_queried_object_id()
        post = get_post(post_id)
    elif "post" == context:
        post = get_post(id)
        if (not php_empty(lambda : post.ID)):
            post_id = post.ID
        # end if
    # end if
    shortlink = ""
    #// Return `?p=` link for all public post types.
    if (not php_empty(lambda : post_id)):
        post_type = get_post_type_object(post.post_type)
        if "page" == post.post_type and get_option("page_on_front") == post.ID and "page" == get_option("show_on_front"):
            shortlink = home_url("/")
        elif post_type.public:
            shortlink = home_url("?p=" + post_id)
        # end if
    # end if
    #// 
    #// Filters the shortlink for a post.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $shortlink   Shortlink URL.
    #// @param int    $id          Post ID, or 0 for the current post.
    #// @param string $context     The context for the link. One of 'post' or 'query',
    #// @param bool   $allow_slugs Whether to allow post slugs in the shortlink. Not used by default.
    #//
    return apply_filters("get_shortlink", shortlink, id, context, allow_slugs)
# end def wp_get_shortlink
#// 
#// Injects rel=shortlink into the head if a shortlink is defined for the current page.
#// 
#// Attached to the {@see 'wp_head'} action.
#// 
#// @since 3.0.0
#//
def wp_shortlink_wp_head(*args_):
    
    shortlink = wp_get_shortlink(0, "query")
    if php_empty(lambda : shortlink):
        return
    # end if
    php_print("<link rel='shortlink' href='" + esc_url(shortlink) + "' />\n")
# end def wp_shortlink_wp_head
#// 
#// Sends a Link: rel=shortlink header if a shortlink is defined for the current page.
#// 
#// Attached to the {@see 'wp'} action.
#// 
#// @since 3.0.0
#//
def wp_shortlink_header(*args_):
    
    if php_headers_sent():
        return
    # end if
    shortlink = wp_get_shortlink(0, "query")
    if php_empty(lambda : shortlink):
        return
    # end if
    php_header("Link: <" + shortlink + ">; rel=shortlink", False)
# end def wp_shortlink_header
#// 
#// Displays the shortlink for a post.
#// 
#// Must be called from inside "The Loop"
#// 
#// Call like the_shortlink( __( 'Shortlinkage FTW' ) )
#// 
#// @since 3.0.0
#// 
#// @param string $text   Optional The link text or HTML to be displayed. Defaults to 'This is the short link.'
#// @param string $title  Optional The tooltip for the link. Must be sanitized. Defaults to the sanitized post title.
#// @param string $before Optional HTML to display before the link. Default empty.
#// @param string $after  Optional HTML to display after the link. Default empty.
#//
def the_shortlink(text="", title="", before="", after="", *args_):
    
    post = get_post()
    if php_empty(lambda : text):
        text = __("This is the short link.")
    # end if
    if php_empty(lambda : title):
        title = the_title_attribute(Array({"echo": False}))
    # end if
    shortlink = wp_get_shortlink(post.ID)
    if (not php_empty(lambda : shortlink)):
        link = "<a rel=\"shortlink\" href=\"" + esc_url(shortlink) + "\" title=\"" + title + "\">" + text + "</a>"
        #// 
        #// Filters the short link anchor tag for a post.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $link      Shortlink anchor tag.
        #// @param string $shortlink Shortlink URL.
        #// @param string $text      Shortlink's text.
        #// @param string $title     Shortlink's title attribute.
        #//
        link = apply_filters("the_shortlink", link, shortlink, text, title)
        php_print(before, link, after)
    # end if
# end def the_shortlink
#// 
#// Retrieves the avatar URL.
#// 
#// @since 4.2.0
#// 
#// @param mixed $id_or_email The Gravatar to retrieve a URL for. Accepts a user_id, gravatar md5 hash,
#// user email, WP_User object, WP_Post object, or WP_Comment object.
#// @param array $args {
#// Optional. Arguments to return instead of the default arguments.
#// 
#// @type int    $size           Height and width of the avatar in pixels. Default 96.
#// @type string $default        URL for the default image or a default type. Accepts '404' (return
#// a 404 instead of a default image), 'retro' (8bit), 'monsterid' (monster),
#// 'wavatar' (cartoon face), 'indenticon' (the "quilt"), 'mystery', 'mm',
#// or 'mysteryman' (The Oyster Man), 'blank' (transparent GIF), or
#// 'gravatar_default' (the Gravatar logo). Default is the value of the
#// 'avatar_default' option, with a fallback of 'mystery'.
#// @type bool   $force_default  Whether to always show the default image, never the Gravatar. Default false.
#// @type string $rating         What rating to display avatars up to. Accepts 'G', 'PG', 'R', 'X', and are
#// judged in that order. Default is the value of the 'avatar_rating' option.
#// @type string $scheme         URL scheme to use. See set_url_scheme() for accepted values.
#// Default null.
#// @type array  $processed_args When the function returns, the value will be the processed/sanitized $args
#// plus a "found_avatar" guess. Pass as a reference. Default null.
#// }
#// @return string|false The URL of the avatar on success, false on failure.
#//
def get_avatar_url(id_or_email=None, args=None, *args_):
    
    args = get_avatar_data(id_or_email, args)
    return args["url"]
# end def get_avatar_url
#// 
#// Check if this comment type allows avatars to be retrieved.
#// 
#// @since 5.1.0
#// 
#// @param string $comment_type Comment type to check.
#// @return bool Whether the comment type is allowed for retrieving avatars.
#//
def is_avatar_comment_type(comment_type=None, *args_):
    
    #// 
    #// Filters the list of allowed comment types for retrieving avatars.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $types An array of content types. Default only contains 'comment'.
    #//
    allowed_comment_types = apply_filters("get_avatar_comment_types", Array("comment"))
    return php_in_array(comment_type, allowed_comment_types, True)
# end def is_avatar_comment_type
#// 
#// Retrieves default data about the avatar.
#// 
#// @since 4.2.0
#// 
#// @param mixed $id_or_email The Gravatar to retrieve. Accepts a user ID, Gravatar MD5 hash,
#// user email, WP_User object, WP_Post object, or WP_Comment object.
#// @param array $args {
#// Optional. Arguments to return instead of the default arguments.
#// 
#// @type int    $size           Height and width of the avatar image file in pixels. Default 96.
#// @type int    $height         Display height of the avatar in pixels. Defaults to $size.
#// @type int    $width          Display width of the avatar in pixels. Defaults to $size.
#// @type string $default        URL for the default image or a default type. Accepts '404' (return
#// a 404 instead of a default image), 'retro' (8bit), 'monsterid' (monster),
#// 'wavatar' (cartoon face), 'indenticon' (the "quilt"), 'mystery', 'mm',
#// or 'mysteryman' (The Oyster Man), 'blank' (transparent GIF), or
#// 'gravatar_default' (the Gravatar logo). Default is the value of the
#// 'avatar_default' option, with a fallback of 'mystery'.
#// @type bool   $force_default  Whether to always show the default image, never the Gravatar. Default false.
#// @type string $rating         What rating to display avatars up to. Accepts 'G', 'PG', 'R', 'X', and are
#// judged in that order. Default is the value of the 'avatar_rating' option.
#// @type string $scheme         URL scheme to use. See set_url_scheme() for accepted values.
#// Default null.
#// @type array  $processed_args When the function returns, the value will be the processed/sanitized $args
#// plus a "found_avatar" guess. Pass as a reference. Default null.
#// @type string $extra_attr     HTML attributes to insert in the IMG element. Is not sanitized. Default empty.
#// }
#// @return array {
#// Along with the arguments passed in `$args`, this will contain a couple of extra arguments.
#// 
#// @type bool   $found_avatar True if we were able to find an avatar for this user,
#// false or not set if we couldn't.
#// @type string $url          The URL of the avatar we found.
#// }
#//
def get_avatar_data(id_or_email=None, args=None, *args_):
    
    args = wp_parse_args(args, Array({"size": 96, "height": None, "width": None, "default": get_option("avatar_default", "mystery"), "force_default": False, "rating": get_option("avatar_rating"), "scheme": None, "processed_args": None, "extra_attr": ""}))
    if php_is_numeric(args["size"]):
        args["size"] = absint(args["size"])
        if (not args["size"]):
            args["size"] = 96
        # end if
    else:
        args["size"] = 96
    # end if
    if php_is_numeric(args["height"]):
        args["height"] = absint(args["height"])
        if (not args["height"]):
            args["height"] = args["size"]
        # end if
    else:
        args["height"] = args["size"]
    # end if
    if php_is_numeric(args["width"]):
        args["width"] = absint(args["width"])
        if (not args["width"]):
            args["width"] = args["size"]
        # end if
    else:
        args["width"] = args["size"]
    # end if
    if php_empty(lambda : args["default"]):
        args["default"] = get_option("avatar_default", "mystery")
    # end if
    for case in Switch(args["default"]):
        if case("mm"):
            pass
        # end if
        if case("mystery"):
            pass
        # end if
        if case("mysteryman"):
            args["default"] = "mm"
            break
        # end if
        if case("gravatar_default"):
            args["default"] = False
            break
        # end if
    # end for
    args["force_default"] = php_bool(args["force_default"])
    args["rating"] = php_strtolower(args["rating"])
    args["found_avatar"] = False
    #// 
    #// Filters whether to retrieve the avatar URL early.
    #// 
    #// Passing a non-null value in the 'url' member of the return array will
    #// effectively short circuit get_avatar_data(), passing the value through
    #// the {@see 'get_avatar_data'} filter and returning early.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array $args        Arguments passed to get_avatar_data(), after processing.
    #// @param mixed $id_or_email The Gravatar to retrieve. Accepts a user ID, Gravatar MD5 hash,
    #// user email, WP_User object, WP_Post object, or WP_Comment object.
    #//
    args = apply_filters("pre_get_avatar_data", args, id_or_email)
    if (php_isset(lambda : args["url"])):
        #// This filter is documented in wp-includes/link-template.php
        return apply_filters("get_avatar_data", args, id_or_email)
    # end if
    email_hash = ""
    user = False
    email = False
    if php_is_object(id_or_email) and (php_isset(lambda : id_or_email.comment_ID)):
        id_or_email = get_comment(id_or_email)
    # end if
    #// Process the user identifier.
    if php_is_numeric(id_or_email):
        user = get_user_by("id", absint(id_or_email))
    elif php_is_string(id_or_email):
        if php_strpos(id_or_email, "@md5.gravatar.com"):
            #// MD5 hash.
            email_hash = php_explode("@", id_or_email)
        else:
            #// Email address.
            email = id_or_email
        # end if
    elif type(id_or_email).__name__ == "WP_User":
        #// User object.
        user = id_or_email
    elif type(id_or_email).__name__ == "WP_Post":
        #// Post object.
        user = get_user_by("id", php_int(id_or_email.post_author))
    elif type(id_or_email).__name__ == "WP_Comment":
        if (not is_avatar_comment_type(get_comment_type(id_or_email))):
            args["url"] = False
            #// This filter is documented in wp-includes/link-template.php
            return apply_filters("get_avatar_data", args, id_or_email)
        # end if
        if (not php_empty(lambda : id_or_email.user_id)):
            user = get_user_by("id", php_int(id_or_email.user_id))
        # end if
        if (not user) or is_wp_error(user) and (not php_empty(lambda : id_or_email.comment_author_email)):
            email = id_or_email.comment_author_email
        # end if
    # end if
    if (not email_hash):
        if user:
            email = user.user_email
        # end if
        if email:
            email_hash = php_md5(php_strtolower(php_trim(email)))
        # end if
    # end if
    if email_hash:
        args["found_avatar"] = True
        gravatar_server = hexdec(email_hash[0]) % 3
    else:
        gravatar_server = rand(0, 2)
    # end if
    url_args = Array({"s": args["size"], "d": args["default"], "f": "y" if args["force_default"] else False, "r": args["rating"]})
    if is_ssl():
        url = "https://secure.gravatar.com/avatar/" + email_hash
    else:
        url = php_sprintf("http://%d.gravatar.com/avatar/%s", gravatar_server, email_hash)
    # end if
    url = add_query_arg(rawurlencode_deep(php_array_filter(url_args)), set_url_scheme(url, args["scheme"]))
    #// 
    #// Filters the avatar URL.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $url         The URL of the avatar.
    #// @param mixed  $id_or_email The Gravatar to retrieve. Accepts a user ID, Gravatar MD5 hash,
    #// user email, WP_User object, WP_Post object, or WP_Comment object.
    #// @param array  $args        Arguments passed to get_avatar_data(), after processing.
    #//
    args["url"] = apply_filters("get_avatar_url", url, id_or_email, args)
    #// 
    #// Filters the avatar data.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array $args        Arguments passed to get_avatar_data(), after processing.
    #// @param mixed $id_or_email The Gravatar to retrieve. Accepts a user ID, Gravatar MD5 hash,
    #// user email, WP_User object, WP_Post object, or WP_Comment object.
    #//
    return apply_filters("get_avatar_data", args, id_or_email)
# end def get_avatar_data
#// 
#// Retrieves the URL of a file in the theme.
#// 
#// Searches in the stylesheet directory before the template directory so themes
#// which inherit from a parent theme can just override one file.
#// 
#// @since 4.7.0
#// 
#// @param string $file Optional. File to search for in the stylesheet directory.
#// @return string The URL of the file.
#//
def get_theme_file_uri(file="", *args_):
    
    file = php_ltrim(file, "/")
    if php_empty(lambda : file):
        url = get_stylesheet_directory_uri()
    elif php_file_exists(get_stylesheet_directory() + "/" + file):
        url = get_stylesheet_directory_uri() + "/" + file
    else:
        url = get_template_directory_uri() + "/" + file
    # end if
    #// 
    #// Filters the URL to a file in the theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $url  The file URL.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("theme_file_uri", url, file)
# end def get_theme_file_uri
#// 
#// Retrieves the URL of a file in the parent theme.
#// 
#// @since 4.7.0
#// 
#// @param string $file Optional. File to return the URL for in the template directory.
#// @return string The URL of the file.
#//
def get_parent_theme_file_uri(file="", *args_):
    
    file = php_ltrim(file, "/")
    if php_empty(lambda : file):
        url = get_template_directory_uri()
    else:
        url = get_template_directory_uri() + "/" + file
    # end if
    #// 
    #// Filters the URL to a file in the parent theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $url  The file URL.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("parent_theme_file_uri", url, file)
# end def get_parent_theme_file_uri
#// 
#// Retrieves the path of a file in the theme.
#// 
#// Searches in the stylesheet directory before the template directory so themes
#// which inherit from a parent theme can just override one file.
#// 
#// @since 4.7.0
#// 
#// @param string $file Optional. File to search for in the stylesheet directory.
#// @return string The path of the file.
#//
def get_theme_file_path(file="", *args_):
    
    file = php_ltrim(file, "/")
    if php_empty(lambda : file):
        path = get_stylesheet_directory()
    elif php_file_exists(get_stylesheet_directory() + "/" + file):
        path = get_stylesheet_directory() + "/" + file
    else:
        path = get_template_directory() + "/" + file
    # end if
    #// 
    #// Filters the path to a file in the theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $path The file path.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("theme_file_path", path, file)
# end def get_theme_file_path
#// 
#// Retrieves the path of a file in the parent theme.
#// 
#// @since 4.7.0
#// 
#// @param string $file Optional. File to return the path for in the template directory.
#// @return string The path of the file.
#//
def get_parent_theme_file_path(file="", *args_):
    
    file = php_ltrim(file, "/")
    if php_empty(lambda : file):
        path = get_template_directory()
    else:
        path = get_template_directory() + "/" + file
    # end if
    #// 
    #// Filters the path to a file in the parent theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $path The file path.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("parent_theme_file_path", path, file)
# end def get_parent_theme_file_path
#// 
#// Retrieves the URL to the privacy policy page.
#// 
#// @since 4.9.6
#// 
#// @return string The URL to the privacy policy page. Empty string if it doesn't exist.
#//
def get_privacy_policy_url(*args_):
    
    url = ""
    policy_page_id = php_int(get_option("wp_page_for_privacy_policy"))
    if (not php_empty(lambda : policy_page_id)) and get_post_status(policy_page_id) == "publish":
        url = php_str(get_permalink(policy_page_id))
    # end if
    #// 
    #// Filters the URL of the privacy policy page.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $url            The URL to the privacy policy page. Empty string
    #// if it doesn't exist.
    #// @param int    $policy_page_id The ID of privacy policy page.
    #//
    return apply_filters("privacy_policy_url", url, policy_page_id)
# end def get_privacy_policy_url
#// 
#// Displays the privacy policy link with formatting, when applicable.
#// 
#// @since 4.9.6
#// 
#// @param string $before Optional. Display before privacy policy link. Default empty.
#// @param string $after  Optional. Display after privacy policy link. Default empty.
#//
def the_privacy_policy_link(before="", after="", *args_):
    
    php_print(get_the_privacy_policy_link(before, after))
# end def the_privacy_policy_link
#// 
#// Returns the privacy policy link with formatting, when applicable.
#// 
#// @since 4.9.6
#// 
#// @param string $before Optional. Display before privacy policy link. Default empty.
#// @param string $after  Optional. Display after privacy policy link. Default empty.
#// 
#// @return string Markup for the link and surrounding elements. Empty string if it
#// doesn't exist.
#//
def get_the_privacy_policy_link(before="", after="", *args_):
    
    link = ""
    privacy_policy_url = get_privacy_policy_url()
    policy_page_id = php_int(get_option("wp_page_for_privacy_policy"))
    page_title = get_the_title(policy_page_id) if policy_page_id else ""
    if privacy_policy_url and page_title:
        link = php_sprintf("<a class=\"privacy-policy-link\" href=\"%s\">%s</a>", esc_url(privacy_policy_url), esc_html(page_title))
    # end if
    #// 
    #// Filters the privacy policy link.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $link               The privacy policy link. Empty string if it
    #// doesn't exist.
    #// @param string $privacy_policy_url The URL of the privacy policy. Empty string
    #// if it doesn't exist.
    #//
    link = apply_filters("the_privacy_policy_link", link, privacy_policy_url)
    if link:
        return before + link + after
    # end if
    return ""
# end def get_the_privacy_policy_link
