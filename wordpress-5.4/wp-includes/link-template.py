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
def the_permalink(post_=0, *_args_):
    
    
    #// 
    #// Filters the display of the permalink for the current post.
    #// 
    #// @since 1.5.0
    #// @since 4.4.0 Added the `$post` parameter.
    #// 
    #// @param string      $permalink The permalink for the current post.
    #// @param int|WP_Post $post      Post ID, WP_Post object, or 0. Default 0.
    #//
    php_print(esc_url(apply_filters("the_permalink", get_permalink(post_), post_)))
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
def user_trailingslashit(string_=None, type_of_url_="", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if wp_rewrite_.use_trailing_slashes:
        string_ = trailingslashit(string_)
    else:
        string_ = untrailingslashit(string_)
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
    return apply_filters("user_trailingslashit", string_, type_of_url_)
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
def permalink_anchor(mode_="id", *_args_):
    
    
    post_ = get_post()
    for case in Switch(php_strtolower(mode_)):
        if case("title"):
            title_ = sanitize_title(post_.post_title) + "-" + post_.ID
            php_print("<a id=\"" + title_ + "\"></a>")
            break
        # end if
        if case("id"):
            pass
        # end if
        if case():
            php_print("<a id=\"post-" + post_.ID + "\"></a>")
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
def get_the_permalink(post_=0, leavename_=None, *_args_):
    if leavename_ is None:
        leavename_ = False
    # end if
    
    return get_permalink(post_, leavename_)
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
def get_permalink(post_=0, leavename_=None, *_args_):
    if leavename_ is None:
        leavename_ = False
    # end if
    
    rewritecode_ = Array("%year%", "%monthnum%", "%day%", "%hour%", "%minute%", "%second%", "" if leavename_ else "%postname%", "%post_id%", "%category%", "%author%", "" if leavename_ else "%pagename%")
    if php_is_object(post_) and (php_isset(lambda : post_.filter)) and "sample" == post_.filter:
        sample_ = True
    else:
        post_ = get_post(post_)
        sample_ = False
    # end if
    if php_empty(lambda : post_.ID):
        return False
    # end if
    if "page" == post_.post_type:
        return get_page_link(post_, leavename_, sample_)
    elif "attachment" == post_.post_type:
        return get_attachment_link(post_, leavename_)
    elif php_in_array(post_.post_type, get_post_types(Array({"_builtin": False}))):
        return get_post_permalink(post_, leavename_, sample_)
    # end if
    permalink_ = get_option("permalink_structure")
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
    permalink_ = apply_filters("pre_post_link", permalink_, post_, leavename_)
    if "" != permalink_ and (not php_in_array(post_.post_status, Array("draft", "pending", "auto-draft", "future"))):
        category_ = ""
        if php_strpos(permalink_, "%category%") != False:
            cats_ = get_the_category(post_.ID)
            if cats_:
                cats_ = wp_list_sort(cats_, Array({"term_id": "ASC"}))
                #// 
                #// Filters the category that gets used in the %category% permalink token.
                #// 
                #// @since 3.5.0
                #// 
                #// @param WP_Term  $cat  The category to use in the permalink.
                #// @param array    $cats Array of all categories (WP_Term objects) associated with the post.
                #// @param WP_Post  $post The post in question.
                #//
                category_object_ = apply_filters("post_link_category", cats_[0], cats_, post_)
                category_object_ = get_term(category_object_, "category")
                category_ = category_object_.slug
                if category_object_.parent:
                    category_ = get_category_parents(category_object_.parent, False, "/", True) + category_
                # end if
            # end if
            #// Show default category in permalinks,
            #// without having to assign it explicitly.
            if php_empty(lambda : category_):
                default_category_ = get_term(get_option("default_category"), "category")
                if default_category_ and (not is_wp_error(default_category_)):
                    category_ = default_category_.slug
                # end if
            # end if
        # end if
        author_ = ""
        if php_strpos(permalink_, "%author%") != False:
            authordata_ = get_userdata(post_.post_author)
            author_ = authordata_.user_nicename
        # end if
        #// This is not an API call because the permalink is based on the stored post_date value,
        #// which should be parsed as local time regardless of the default PHP timezone.
        date_ = php_explode(" ", php_str_replace(Array("-", ":"), " ", post_.post_date))
        rewritereplace_ = Array(date_[0], date_[1], date_[2], date_[3], date_[4], date_[5], post_.post_name, post_.ID, category_, author_, post_.post_name)
        permalink_ = home_url(php_str_replace(rewritecode_, rewritereplace_, permalink_))
        permalink_ = user_trailingslashit(permalink_, "single")
    else:
        #// If they're not using the fancy permalink option.
        permalink_ = home_url("?p=" + post_.ID)
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
    return apply_filters("post_link", permalink_, post_, leavename_)
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
def get_post_permalink(id_=0, leavename_=None, sample_=None, *_args_):
    if leavename_ is None:
        leavename_ = False
    # end if
    if sample_ is None:
        sample_ = False
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    post_ = get_post(id_)
    if is_wp_error(post_):
        return post_
    # end if
    post_link_ = wp_rewrite_.get_extra_permastruct(post_.post_type)
    slug_ = post_.post_name
    draft_or_pending_ = get_post_status(post_) and php_in_array(get_post_status(post_), Array("draft", "pending", "auto-draft", "future"))
    post_type_ = get_post_type_object(post_.post_type)
    if post_type_.hierarchical:
        slug_ = get_page_uri(post_)
    # end if
    if (not php_empty(lambda : post_link_)) and (not draft_or_pending_) or sample_:
        if (not leavename_):
            post_link_ = php_str_replace(str("%") + str(post_.post_type) + str("%"), slug_, post_link_)
        # end if
        post_link_ = home_url(user_trailingslashit(post_link_))
    else:
        if post_type_.query_var and (php_isset(lambda : post_.post_status)) and (not draft_or_pending_):
            post_link_ = add_query_arg(post_type_.query_var, slug_, "")
        else:
            post_link_ = add_query_arg(Array({"post_type": post_.post_type, "p": post_.ID}), "")
        # end if
        post_link_ = home_url(post_link_)
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
    return apply_filters("post_type_link", post_link_, post_, leavename_, sample_)
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
def get_page_link(post_=None, leavename_=None, sample_=None, *_args_):
    if post_ is None:
        post_ = False
    # end if
    if leavename_ is None:
        leavename_ = False
    # end if
    if sample_ is None:
        sample_ = False
    # end if
    
    post_ = get_post(post_)
    if "page" == get_option("show_on_front") and get_option("page_on_front") == post_.ID:
        link_ = home_url("/")
    else:
        link_ = _get_page_link(post_, leavename_, sample_)
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
    return apply_filters("page_link", link_, post_.ID, sample_)
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
def _get_page_link(post_=None, leavename_=None, sample_=None, *_args_):
    if post_ is None:
        post_ = False
    # end if
    if leavename_ is None:
        leavename_ = False
    # end if
    if sample_ is None:
        sample_ = False
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    post_ = get_post(post_)
    draft_or_pending_ = php_in_array(post_.post_status, Array("draft", "pending", "auto-draft"))
    link_ = wp_rewrite_.get_page_permastruct()
    if (not php_empty(lambda : link_)) and (php_isset(lambda : post_.post_status)) and (not draft_or_pending_) or sample_:
        if (not leavename_):
            link_ = php_str_replace("%pagename%", get_page_uri(post_), link_)
        # end if
        link_ = home_url(link_)
        link_ = user_trailingslashit(link_, "page")
    else:
        link_ = home_url("?page_id=" + post_.ID)
    # end if
    #// 
    #// Filters the permalink for a non-page_on_front page.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $link    The page's permalink.
    #// @param int    $post_id The ID of the page.
    #//
    return apply_filters("_get_page_link", link_, post_.ID)
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
def get_attachment_link(post_=None, leavename_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    if leavename_ is None:
        leavename_ = False
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    link_ = False
    post_ = get_post(post_)
    parent_ = get_post(post_.post_parent) if post_.post_parent > 0 and post_.post_parent != post_.ID else False
    if parent_ and (not php_in_array(parent_.post_type, get_post_types())):
        parent_ = False
    # end if
    if wp_rewrite_.using_permalinks() and parent_:
        if "page" == parent_.post_type:
            parentlink_ = _get_page_link(post_.post_parent)
            pass
        else:
            parentlink_ = get_permalink(post_.post_parent)
        # end if
        if php_is_numeric(post_.post_name) or False != php_strpos(get_option("permalink_structure"), "%category%"):
            name_ = "attachment/" + post_.post_name
            pass
        else:
            name_ = post_.post_name
        # end if
        if php_strpos(parentlink_, "?") == False:
            link_ = user_trailingslashit(trailingslashit(parentlink_) + "%postname%")
        # end if
        if (not leavename_):
            link_ = php_str_replace("%postname%", name_, link_)
        # end if
    elif wp_rewrite_.using_permalinks() and (not leavename_):
        link_ = home_url(user_trailingslashit(post_.post_name))
    # end if
    if (not link_):
        link_ = home_url("/?attachment_id=" + post_.ID)
    # end if
    #// 
    #// Filters the permalink for an attachment.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $link    The attachment's permalink.
    #// @param int    $post_id Attachment ID.
    #//
    return apply_filters("attachment_link", link_, post_.ID)
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
def get_year_link(year_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not year_):
        year_ = current_time("Y")
    # end if
    yearlink_ = wp_rewrite_.get_year_permastruct()
    if (not php_empty(lambda : yearlink_)):
        yearlink_ = php_str_replace("%year%", year_, yearlink_)
        yearlink_ = home_url(user_trailingslashit(yearlink_, "year"))
    else:
        yearlink_ = home_url("?m=" + year_)
    # end if
    #// 
    #// Filters the year archive permalink.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $yearlink Permalink for the year archive.
    #// @param int    $year     Year for the archive.
    #//
    return apply_filters("year_link", yearlink_, year_)
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
def get_month_link(year_=None, month_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not year_):
        year_ = current_time("Y")
    # end if
    if (not month_):
        month_ = current_time("m")
    # end if
    monthlink_ = wp_rewrite_.get_month_permastruct()
    if (not php_empty(lambda : monthlink_)):
        monthlink_ = php_str_replace("%year%", year_, monthlink_)
        monthlink_ = php_str_replace("%monthnum%", zeroise(php_intval(month_), 2), monthlink_)
        monthlink_ = home_url(user_trailingslashit(monthlink_, "month"))
    else:
        monthlink_ = home_url("?m=" + year_ + zeroise(month_, 2))
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
    return apply_filters("month_link", monthlink_, year_, month_)
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
def get_day_link(year_=None, month_=None, day_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not year_):
        year_ = current_time("Y")
    # end if
    if (not month_):
        month_ = current_time("m")
    # end if
    if (not day_):
        day_ = current_time("j")
    # end if
    daylink_ = wp_rewrite_.get_day_permastruct()
    if (not php_empty(lambda : daylink_)):
        daylink_ = php_str_replace("%year%", year_, daylink_)
        daylink_ = php_str_replace("%monthnum%", zeroise(php_intval(month_), 2), daylink_)
        daylink_ = php_str_replace("%day%", zeroise(php_intval(day_), 2), daylink_)
        daylink_ = home_url(user_trailingslashit(daylink_, "day"))
    else:
        daylink_ = home_url("?m=" + year_ + zeroise(month_, 2) + zeroise(day_, 2))
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
    return apply_filters("day_link", daylink_, year_, month_, day_)
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
def the_feed_link(anchor_=None, feed_="", *_args_):
    
    
    link_ = "<a href=\"" + esc_url(get_feed_link(feed_)) + "\">" + anchor_ + "</a>"
    #// 
    #// Filters the feed link anchor tag.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $link The complete anchor tag for a feed link.
    #// @param string $feed The feed type. Possible values include 'rss2', 'atom',
    #// or an empty string for the default feed type.
    #//
    php_print(apply_filters("the_feed_link", link_, feed_))
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
def get_feed_link(feed_="", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    permalink_ = wp_rewrite_.get_feed_permastruct()
    if "" != permalink_:
        if False != php_strpos(feed_, "comments_"):
            feed_ = php_str_replace("comments_", "", feed_)
            permalink_ = wp_rewrite_.get_comment_feed_permastruct()
        # end if
        if get_default_feed() == feed_:
            feed_ = ""
        # end if
        permalink_ = php_str_replace("%feed%", feed_, permalink_)
        permalink_ = php_preg_replace("#/+#", "/", str("/") + str(permalink_))
        output_ = home_url(user_trailingslashit(permalink_, "feed"))
    else:
        if php_empty(lambda : feed_):
            feed_ = get_default_feed()
        # end if
        if False != php_strpos(feed_, "comments_"):
            feed_ = php_str_replace("comments_", "comments-", feed_)
        # end if
        output_ = home_url(str("?feed=") + str(feed_))
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
    return apply_filters("feed_link", output_, feed_)
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
def get_post_comments_feed_link(post_id_=0, feed_="", *_args_):
    
    
    post_id_ = absint(post_id_)
    if (not post_id_):
        post_id_ = get_the_ID()
    # end if
    if php_empty(lambda : feed_):
        feed_ = get_default_feed()
    # end if
    post_ = get_post(post_id_)
    unattached_ = "attachment" == post_.post_type and 0 == php_int(post_.post_parent)
    if "" != get_option("permalink_structure"):
        if "page" == get_option("show_on_front") and get_option("page_on_front") == post_id_:
            url_ = _get_page_link(post_id_)
        else:
            url_ = get_permalink(post_id_)
        # end if
        if unattached_:
            url_ = home_url("/feed/")
            if get_default_feed() != feed_:
                url_ += str(feed_) + str("/")
            # end if
            url_ = add_query_arg("attachment_id", post_id_, url_)
        else:
            url_ = trailingslashit(url_) + "feed"
            if get_default_feed() != feed_:
                url_ += str("/") + str(feed_)
            # end if
            url_ = user_trailingslashit(url_, "single_feed")
        # end if
    else:
        if unattached_:
            url_ = add_query_arg(Array({"feed": feed_, "attachment_id": post_id_}), home_url("/"))
        elif "page" == post_.post_type:
            url_ = add_query_arg(Array({"feed": feed_, "page_id": post_id_}), home_url("/"))
        else:
            url_ = add_query_arg(Array({"feed": feed_, "p": post_id_}), home_url("/"))
        # end if
    # end if
    #// 
    #// Filters the post comments feed permalink.
    #// 
    #// @since 1.5.1
    #// 
    #// @param string $url Post comments feed permalink.
    #//
    return apply_filters("post_comments_feed_link", url_)
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
def post_comments_feed_link(link_text_="", post_id_="", feed_="", *_args_):
    
    
    url_ = get_post_comments_feed_link(post_id_, feed_)
    if php_empty(lambda : link_text_):
        link_text_ = __("Comments Feed")
    # end if
    link_ = "<a href=\"" + esc_url(url_) + "\">" + link_text_ + "</a>"
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
    php_print(apply_filters("post_comments_feed_link_html", link_, post_id_, feed_))
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
def get_author_feed_link(author_id_=None, feed_="", *_args_):
    
    
    author_id_ = php_int(author_id_)
    permalink_structure_ = get_option("permalink_structure")
    if php_empty(lambda : feed_):
        feed_ = get_default_feed()
    # end if
    if "" == permalink_structure_:
        link_ = home_url(str("?feed=") + str(feed_) + str("&amp;author=") + author_id_)
    else:
        link_ = get_author_posts_url(author_id_)
        if get_default_feed() == feed_:
            feed_link_ = "feed"
        else:
            feed_link_ = str("feed/") + str(feed_)
        # end if
        link_ = trailingslashit(link_) + user_trailingslashit(feed_link_, "feed")
    # end if
    #// 
    #// Filters the feed link for a given author.
    #// 
    #// @since 1.5.1
    #// 
    #// @param string $link The author feed link.
    #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
    #//
    link_ = apply_filters("author_feed_link", link_, feed_)
    return link_
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
def get_category_feed_link(cat_id_=None, feed_="", *_args_):
    
    
    return get_term_feed_link(cat_id_, "category", feed_)
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
def get_term_feed_link(term_id_=None, taxonomy_="category", feed_="", *_args_):
    
    
    term_id_ = php_int(term_id_)
    term_ = get_term(term_id_, taxonomy_)
    if php_empty(lambda : term_) or is_wp_error(term_):
        return False
    # end if
    if php_empty(lambda : feed_):
        feed_ = get_default_feed()
    # end if
    permalink_structure_ = get_option("permalink_structure")
    if "" == permalink_structure_:
        if "category" == taxonomy_:
            link_ = home_url(str("?feed=") + str(feed_) + str("&amp;cat=") + str(term_id_))
        elif "post_tag" == taxonomy_:
            link_ = home_url(str("?feed=") + str(feed_) + str("&amp;tag=") + str(term_.slug))
        else:
            t_ = get_taxonomy(taxonomy_)
            link_ = home_url(str("?feed=") + str(feed_) + str("&amp;") + str(t_.query_var) + str("=") + str(term_.slug))
        # end if
    else:
        link_ = get_term_link(term_id_, term_.taxonomy)
        if get_default_feed() == feed_:
            feed_link_ = "feed"
        else:
            feed_link_ = str("feed/") + str(feed_)
        # end if
        link_ = trailingslashit(link_) + user_trailingslashit(feed_link_, "feed")
    # end if
    if "category" == taxonomy_:
        #// 
        #// Filters the category feed link.
        #// 
        #// @since 1.5.1
        #// 
        #// @param string $link The category feed link.
        #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
        #//
        link_ = apply_filters("category_feed_link", link_, feed_)
    elif "post_tag" == taxonomy_:
        #// 
        #// Filters the post tag feed link.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $link The tag feed link.
        #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
        #//
        link_ = apply_filters("tag_feed_link", link_, feed_)
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
        link_ = apply_filters("taxonomy_feed_link", link_, feed_, taxonomy_)
    # end if
    return link_
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
def get_tag_feed_link(tag_id_=None, feed_="", *_args_):
    
    
    return get_term_feed_link(tag_id_, "post_tag", feed_)
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
def get_edit_tag_link(tag_id_=None, taxonomy_="post_tag", *_args_):
    
    
    #// 
    #// Filters the edit link for a tag (or term in another taxonomy).
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $link The term edit link.
    #//
    return apply_filters("get_edit_tag_link", get_edit_term_link(tag_id_, taxonomy_))
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
def edit_tag_link(link_="", before_="", after_="", tag_=None, *_args_):
    if tag_ is None:
        tag_ = None
    # end if
    
    link_ = edit_term_link(link_, "", "", tag_, False)
    #// 
    #// Filters the anchor tag for the edit link for a tag (or term in another taxonomy).
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $link The anchor tag for the edit link.
    #//
    php_print(before_ + apply_filters("edit_tag_link", link_) + after_)
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
def get_edit_term_link(term_id_=None, taxonomy_="", object_type_="", *_args_):
    
    
    term_ = get_term(term_id_, taxonomy_)
    if (not term_) or is_wp_error(term_):
        return
    # end if
    tax_ = get_taxonomy(term_.taxonomy)
    if (not tax_) or (not current_user_can("edit_term", term_.term_id)):
        return
    # end if
    args_ = Array({"taxonomy": taxonomy_, "tag_ID": term_.term_id})
    if object_type_:
        args_["post_type"] = object_type_
    elif (not php_empty(lambda : tax_.object_type)):
        args_["post_type"] = reset(tax_.object_type)
    # end if
    if tax_.show_ui:
        location_ = add_query_arg(args_, admin_url("term.php"))
    else:
        location_ = ""
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
    return apply_filters("get_edit_term_link", location_, term_id_, taxonomy_, object_type_)
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
def edit_term_link(link_="", before_="", after_="", term_=None, echo_=None, *_args_):
    if term_ is None:
        term_ = None
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    if php_is_null(term_):
        term_ = get_queried_object()
    # end if
    if (not term_):
        return
    # end if
    tax_ = get_taxonomy(term_.taxonomy)
    if (not current_user_can("edit_term", term_.term_id)):
        return
    # end if
    if php_empty(lambda : link_):
        link_ = __("Edit This")
    # end if
    link_ = "<a href=\"" + get_edit_term_link(term_.term_id, term_.taxonomy) + "\">" + link_ + "</a>"
    #// 
    #// Filters the anchor tag for the edit link of a term.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $link    The anchor tag for the edit link.
    #// @param int    $term_id Term ID.
    #//
    link_ = before_ + apply_filters("edit_term_link", link_, term_.term_id) + after_
    if echo_:
        php_print(link_)
    else:
        return link_
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
def get_search_link(query_="", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if php_empty(lambda : query_):
        search_ = get_search_query(False)
    else:
        search_ = stripslashes(query_)
    # end if
    permastruct_ = wp_rewrite_.get_search_permastruct()
    if php_empty(lambda : permastruct_):
        link_ = home_url("?s=" + urlencode(search_))
    else:
        search_ = urlencode(search_)
        search_ = php_str_replace("%2F", "/", search_)
        #// %2F(/) is not valid within a URL, send it un-encoded.
        link_ = php_str_replace("%search%", search_, permastruct_)
        link_ = home_url(user_trailingslashit(link_, "search"))
    # end if
    #// 
    #// Filters the search permalink.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $link   Search permalink.
    #// @param string $search The URL-encoded search term.
    #//
    return apply_filters("search_link", link_, search_)
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
def get_search_feed_link(search_query_="", feed_="", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    link_ = get_search_link(search_query_)
    if php_empty(lambda : feed_):
        feed_ = get_default_feed()
    # end if
    permastruct_ = wp_rewrite_.get_search_permastruct()
    if php_empty(lambda : permastruct_):
        link_ = add_query_arg("feed", feed_, link_)
    else:
        link_ = trailingslashit(link_)
        link_ += str("feed/") + str(feed_) + str("/")
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
    return apply_filters("search_feed_link", link_, feed_, "posts")
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
def get_search_comments_feed_link(search_query_="", feed_="", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if php_empty(lambda : feed_):
        feed_ = get_default_feed()
    # end if
    link_ = get_search_feed_link(search_query_, feed_)
    permastruct_ = wp_rewrite_.get_search_permastruct()
    if php_empty(lambda : permastruct_):
        link_ = add_query_arg("feed", "comments-" + feed_, link_)
    else:
        link_ = add_query_arg("withcomments", 1, link_)
    # end if
    #// This filter is documented in wp-includes/link-template.php
    return apply_filters("search_feed_link", link_, feed_, "comments")
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
def get_post_type_archive_link(post_type_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    post_type_obj_ = get_post_type_object(post_type_)
    if (not post_type_obj_):
        return False
    # end if
    if "post" == post_type_:
        show_on_front_ = get_option("show_on_front")
        page_for_posts_ = get_option("page_for_posts")
        if "page" == show_on_front_ and page_for_posts_:
            link_ = get_permalink(page_for_posts_)
        else:
            link_ = get_home_url()
        # end if
        #// This filter is documented in wp-includes/link-template.php
        return apply_filters("post_type_archive_link", link_, post_type_)
    # end if
    if (not post_type_obj_.has_archive):
        return False
    # end if
    if get_option("permalink_structure") and php_is_array(post_type_obj_.rewrite):
        struct_ = post_type_obj_.rewrite["slug"] if True == post_type_obj_.has_archive else post_type_obj_.has_archive
        if post_type_obj_.rewrite["with_front"]:
            struct_ = wp_rewrite_.front + struct_
        else:
            struct_ = wp_rewrite_.root + struct_
        # end if
        link_ = home_url(user_trailingslashit(struct_, "post_type_archive"))
    else:
        link_ = home_url("?post_type=" + post_type_)
    # end if
    #// 
    #// Filters the post type archive permalink.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $link      The post type archive permalink.
    #// @param string $post_type Post type name.
    #//
    return apply_filters("post_type_archive_link", link_, post_type_)
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
def get_post_type_archive_feed_link(post_type_=None, feed_="", *_args_):
    
    
    default_feed_ = get_default_feed()
    if php_empty(lambda : feed_):
        feed_ = default_feed_
    # end if
    link_ = get_post_type_archive_link(post_type_)
    if (not link_):
        return False
    # end if
    post_type_obj_ = get_post_type_object(post_type_)
    if get_option("permalink_structure") and php_is_array(post_type_obj_.rewrite) and post_type_obj_.rewrite["feeds"]:
        link_ = trailingslashit(link_)
        link_ += "feed/"
        if feed_ != default_feed_:
            link_ += str(feed_) + str("/")
        # end if
    else:
        link_ = add_query_arg("feed", feed_, link_)
    # end if
    #// 
    #// Filters the post type archive feed link.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $link The post type archive feed link.
    #// @param string $feed Feed type. Possible values include 'rss2', 'atom'.
    #//
    return apply_filters("post_type_archive_feed_link", link_, feed_)
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
def get_preview_post_link(post_=None, query_args_=None, preview_link_="", *_args_):
    if post_ is None:
        post_ = None
    # end if
    if query_args_ is None:
        query_args_ = Array()
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return
    # end if
    post_type_object_ = get_post_type_object(post_.post_type)
    if is_post_type_viewable(post_type_object_):
        if (not preview_link_):
            preview_link_ = set_url_scheme(get_permalink(post_))
        # end if
        query_args_["preview"] = "true"
        preview_link_ = add_query_arg(query_args_, preview_link_)
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
    return apply_filters("preview_post_link", preview_link_, post_)
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
def get_edit_post_link(id_=0, context_="display", *_args_):
    
    
    post_ = get_post(id_)
    if (not post_):
        return
    # end if
    if "revision" == post_.post_type:
        action_ = ""
    elif "display" == context_:
        action_ = "&amp;action=edit"
    else:
        action_ = "&action=edit"
    # end if
    post_type_object_ = get_post_type_object(post_.post_type)
    if (not post_type_object_):
        return
    # end if
    if (not current_user_can("edit_post", post_.ID)):
        return
    # end if
    if post_type_object_._edit_link:
        link_ = admin_url(php_sprintf(post_type_object_._edit_link + action_, post_.ID))
    else:
        link_ = ""
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
    return apply_filters("get_edit_post_link", link_, post_.ID, context_)
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
def edit_post_link(text_=None, before_="", after_="", id_=0, class_="post-edit-link", *_args_):
    if text_ is None:
        text_ = None
    # end if
    
    post_ = get_post(id_)
    if (not post_):
        return
    # end if
    url_ = get_edit_post_link(post_.ID)
    if (not url_):
        return
    # end if
    if None == text_:
        text_ = __("Edit This")
    # end if
    link_ = "<a class=\"" + esc_attr(class_) + "\" href=\"" + esc_url(url_) + "\">" + text_ + "</a>"
    #// 
    #// Filters the post edit link anchor tag.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $link    Anchor tag for the edit link.
    #// @param int    $post_id Post ID.
    #// @param string $text    Anchor text.
    #//
    php_print(before_ + apply_filters("edit_post_link", link_, post_.ID, text_) + after_)
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
def get_delete_post_link(id_=0, deprecated_="", force_delete_=None, *_args_):
    if force_delete_ is None:
        force_delete_ = False
    # end if
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(__FUNCTION__, "3.0.0")
    # end if
    post_ = get_post(id_)
    if (not post_):
        return
    # end if
    post_type_object_ = get_post_type_object(post_.post_type)
    if (not post_type_object_):
        return
    # end if
    if (not current_user_can("delete_post", post_.ID)):
        return
    # end if
    action_ = "delete" if force_delete_ or (not EMPTY_TRASH_DAYS) else "trash"
    delete_link_ = add_query_arg("action", action_, admin_url(php_sprintf(post_type_object_._edit_link, post_.ID)))
    #// 
    #// Filters the post delete link.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $link         The delete link.
    #// @param int    $post_id      Post ID.
    #// @param bool   $force_delete Whether to bypass the Trash and force deletion. Default false.
    #//
    return apply_filters("get_delete_post_link", wp_nonce_url(delete_link_, str(action_) + str("-post_") + str(post_.ID)), post_.ID, force_delete_)
# end def get_delete_post_link
#// 
#// Retrieves the edit comment link.
#// 
#// @since 2.3.0
#// 
#// @param int|WP_Comment $comment_id Optional. Comment ID or WP_Comment object.
#// @return string|void The edit comment link URL for the given comment.
#//
def get_edit_comment_link(comment_id_=0, *_args_):
    
    
    comment_ = get_comment(comment_id_)
    if (not current_user_can("edit_comment", comment_.comment_ID)):
        return
    # end if
    location_ = admin_url("comment.php?action=editcomment&amp;c=") + comment_.comment_ID
    #// 
    #// Filters the comment edit link.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $location The edit link.
    #//
    return apply_filters("get_edit_comment_link", location_)
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
def edit_comment_link(text_=None, before_="", after_="", *_args_):
    if text_ is None:
        text_ = None
    # end if
    
    comment_ = get_comment()
    if (not current_user_can("edit_comment", comment_.comment_ID)):
        return
    # end if
    if None == text_:
        text_ = __("Edit This")
    # end if
    link_ = "<a class=\"comment-edit-link\" href=\"" + esc_url(get_edit_comment_link(comment_)) + "\">" + text_ + "</a>"
    #// 
    #// Filters the comment edit link anchor tag.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $link       Anchor tag for the edit link.
    #// @param int    $comment_id Comment ID.
    #// @param string $text       Anchor text.
    #//
    php_print(before_ + apply_filters("edit_comment_link", link_, comment_.comment_ID, text_) + after_)
# end def edit_comment_link
#// 
#// Displays the edit bookmark link.
#// 
#// @since 2.7.0
#// 
#// @param int|stdClass $link Optional. Bookmark ID. Default is the id of the current bookmark.
#// @return string|void The edit bookmark link URL.
#//
def get_edit_bookmark_link(link_=0, *_args_):
    
    
    link_ = get_bookmark(link_)
    if (not current_user_can("manage_links")):
        return
    # end if
    location_ = admin_url("link.php?action=edit&amp;link_id=") + link_.link_id
    #// 
    #// Filters the bookmark edit link.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $location The edit link.
    #// @param int    $link_id  Bookmark ID.
    #//
    return apply_filters("get_edit_bookmark_link", location_, link_.link_id)
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
def edit_bookmark_link(link_="", before_="", after_="", bookmark_=None, *_args_):
    if bookmark_ is None:
        bookmark_ = None
    # end if
    
    bookmark_ = get_bookmark(bookmark_)
    if (not current_user_can("manage_links")):
        return
    # end if
    if php_empty(lambda : link_):
        link_ = __("Edit This")
    # end if
    link_ = "<a href=\"" + esc_url(get_edit_bookmark_link(bookmark_)) + "\">" + link_ + "</a>"
    #// 
    #// Filters the bookmark edit link anchor tag.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $link    Anchor tag for the edit link.
    #// @param int    $link_id Bookmark ID.
    #//
    php_print(before_ + apply_filters("edit_bookmark_link", link_, bookmark_.link_id) + after_)
# end def edit_bookmark_link
#// 
#// Retrieves the edit user link.
#// 
#// @since 3.5.0
#// 
#// @param int $user_id Optional. User ID. Defaults to the current user.
#// @return string URL to edit user page or empty string.
#//
def get_edit_user_link(user_id_=None, *_args_):
    if user_id_ is None:
        user_id_ = None
    # end if
    
    if (not user_id_):
        user_id_ = get_current_user_id()
    # end if
    if php_empty(lambda : user_id_) or (not current_user_can("edit_user", user_id_)):
        return ""
    # end if
    user_ = get_userdata(user_id_)
    if (not user_):
        return ""
    # end if
    if get_current_user_id() == user_.ID:
        link_ = get_edit_profile_url(user_.ID)
    else:
        link_ = add_query_arg("user_id", user_.ID, self_admin_url("user-edit.php"))
    # end if
    #// 
    #// Filters the user edit link.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $link    The edit link.
    #// @param int    $user_id User ID.
    #//
    return apply_filters("get_edit_user_link", link_, user_.ID)
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
def get_previous_post(in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    return get_adjacent_post(in_same_term_, excluded_terms_, True, taxonomy_)
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
def get_next_post(in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    return get_adjacent_post(in_same_term_, excluded_terms_, False, taxonomy_)
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
def get_adjacent_post(in_same_term_=None, excluded_terms_="", previous_=None, taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    if previous_ is None:
        previous_ = True
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post()
    if (not post_) or (not taxonomy_exists(taxonomy_)):
        return None
    # end if
    current_post_date_ = post_.post_date
    join_ = ""
    where_ = ""
    adjacent_ = "previous" if previous_ else "next"
    if (not php_empty(lambda : excluded_terms_)) and (not php_is_array(excluded_terms_)):
        #// Back-compat, $excluded_terms used to be $excluded_categories with IDs separated by " and ".
        if False != php_strpos(excluded_terms_, " and "):
            _deprecated_argument(__FUNCTION__, "3.3.0", php_sprintf(__("Use commas instead of %s to separate excluded terms."), "'and'"))
            excluded_terms_ = php_explode(" and ", excluded_terms_)
        else:
            excluded_terms_ = php_explode(",", excluded_terms_)
        # end if
        excluded_terms_ = php_array_map("intval", excluded_terms_)
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
    excluded_terms_ = apply_filters(str("get_") + str(adjacent_) + str("_post_excluded_terms"), excluded_terms_)
    if in_same_term_ or (not php_empty(lambda : excluded_terms_)):
        if in_same_term_:
            join_ += str(" INNER JOIN ") + str(wpdb_.term_relationships) + str(" AS tr ON p.ID = tr.object_id INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" tt ON tr.term_taxonomy_id = tt.term_taxonomy_id")
            where_ += wpdb_.prepare("AND tt.taxonomy = %s", taxonomy_)
            if (not is_object_in_taxonomy(post_.post_type, taxonomy_)):
                return ""
            # end if
            term_array_ = wp_get_object_terms(post_.ID, taxonomy_, Array({"fields": "ids"}))
            #// Remove any exclusions from the term array to include.
            term_array_ = php_array_diff(term_array_, excluded_terms_)
            term_array_ = php_array_map("intval", term_array_)
            if (not term_array_) or is_wp_error(term_array_):
                return ""
            # end if
            where_ += " AND tt.term_id IN (" + php_implode(",", term_array_) + ")"
        # end if
        if (not php_empty(lambda : excluded_terms_)):
            where_ += str(" AND p.ID NOT IN ( SELECT tr.object_id FROM ") + str(wpdb_.term_relationships) + str(" tr LEFT JOIN ") + str(wpdb_.term_taxonomy) + str(" tt ON (tr.term_taxonomy_id = tt.term_taxonomy_id) WHERE tt.term_id IN (") + php_implode(",", php_array_map("intval", excluded_terms_)) + ") )"
        # end if
    # end if
    #// 'post_status' clause depends on the current user.
    if is_user_logged_in():
        user_id_ = get_current_user_id()
        post_type_object_ = get_post_type_object(post_.post_type)
        if php_empty(lambda : post_type_object_):
            post_type_cap_ = post_.post_type
            read_private_cap_ = "read_private_" + post_type_cap_ + "s"
        else:
            read_private_cap_ = post_type_object_.cap.read_private_posts
        # end if
        #// 
        #// Results should include private posts belonging to the current user, or private posts where the
        #// current user has the 'read_private_posts' cap.
        #//
        private_states_ = get_post_stati(Array({"private": True}))
        where_ += " AND ( p.post_status = 'publish'"
        for state_ in private_states_:
            if current_user_can(read_private_cap_):
                where_ += wpdb_.prepare(" OR p.post_status = %s", state_)
            else:
                where_ += wpdb_.prepare(" OR (p.post_author = %d AND p.post_status = %s)", user_id_, state_)
            # end if
        # end for
        where_ += " )"
    else:
        where_ += " AND p.post_status = 'publish'"
    # end if
    op_ = "<" if previous_ else ">"
    order_ = "DESC" if previous_ else "ASC"
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
    join_ = apply_filters(str("get_") + str(adjacent_) + str("_post_join"), join_, in_same_term_, excluded_terms_, taxonomy_, post_)
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
    where_ = apply_filters(str("get_") + str(adjacent_) + str("_post_where"), wpdb_.prepare(str("WHERE p.post_date ") + str(op_) + str(" %s AND p.post_type = %s ") + str(where_), current_post_date_, post_.post_type), in_same_term_, excluded_terms_, taxonomy_, post_)
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
    sort_ = apply_filters(str("get_") + str(adjacent_) + str("_post_sort"), str("ORDER BY p.post_date ") + str(order_) + str(" LIMIT 1"), post_, order_)
    query_ = str("SELECT p.ID FROM ") + str(wpdb_.posts) + str(" AS p ") + str(join_) + str(" ") + str(where_) + str(" ") + str(sort_)
    query_key_ = "adjacent_post_" + php_md5(query_)
    result_ = wp_cache_get(query_key_, "counts")
    if False != result_:
        if result_:
            result_ = get_post(result_)
        # end if
        return result_
    # end if
    result_ = wpdb_.get_var(query_)
    if None == result_:
        result_ = ""
    # end if
    wp_cache_set(query_key_, result_, "counts")
    if result_:
        result_ = get_post(result_)
    # end if
    return result_
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
def get_adjacent_post_rel_link(title_="%title", in_same_term_=None, excluded_terms_="", previous_=None, taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    if previous_ is None:
        previous_ = True
    # end if
    
    post_ = get_post()
    if previous_ and is_attachment() and post_:
        post_ = get_post(post_.post_parent)
    else:
        post_ = get_adjacent_post(in_same_term_, excluded_terms_, previous_, taxonomy_)
    # end if
    if php_empty(lambda : post_):
        return
    # end if
    post_title_ = the_title_attribute(Array({"echo": False, "post": post_}))
    if php_empty(lambda : post_title_):
        post_title_ = __("Previous Post") if previous_ else __("Next Post")
    # end if
    date_ = mysql2date(get_option("date_format"), post_.post_date)
    title_ = php_str_replace("%title", post_title_, title_)
    title_ = php_str_replace("%date", date_, title_)
    link_ = "<link rel='prev' title='" if previous_ else "<link rel='next' title='"
    link_ += esc_attr(title_)
    link_ += "' href='" + get_permalink(post_) + "' />\n"
    adjacent_ = "previous" if previous_ else "next"
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
    return apply_filters(str(adjacent_) + str("_post_rel_link"), link_)
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
def adjacent_posts_rel_link(title_="%title", in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    php_print(get_adjacent_post_rel_link(title_, in_same_term_, excluded_terms_, True, taxonomy_))
    php_print(get_adjacent_post_rel_link(title_, in_same_term_, excluded_terms_, False, taxonomy_))
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
def adjacent_posts_rel_link_wp_head(*_args_):
    
    
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
def next_post_rel_link(title_="%title", in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    php_print(get_adjacent_post_rel_link(title_, in_same_term_, excluded_terms_, False, taxonomy_))
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
def prev_post_rel_link(title_="%title", in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    php_print(get_adjacent_post_rel_link(title_, in_same_term_, excluded_terms_, True, taxonomy_))
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
def get_boundary_post(in_same_term_=None, excluded_terms_="", start_=None, taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    if start_ is None:
        start_ = True
    # end if
    
    post_ = get_post()
    if (not post_) or (not is_single()) or is_attachment() or (not taxonomy_exists(taxonomy_)):
        return None
    # end if
    query_args_ = Array({"posts_per_page": 1, "order": "ASC" if start_ else "DESC", "update_post_term_cache": False, "update_post_meta_cache": False})
    term_array_ = Array()
    if (not php_is_array(excluded_terms_)):
        if (not php_empty(lambda : excluded_terms_)):
            excluded_terms_ = php_explode(",", excluded_terms_)
        else:
            excluded_terms_ = Array()
        # end if
    # end if
    if in_same_term_ or (not php_empty(lambda : excluded_terms_)):
        if in_same_term_:
            term_array_ = wp_get_object_terms(post_.ID, taxonomy_, Array({"fields": "ids"}))
        # end if
        if (not php_empty(lambda : excluded_terms_)):
            excluded_terms_ = php_array_map("intval", excluded_terms_)
            excluded_terms_ = php_array_diff(excluded_terms_, term_array_)
            inverse_terms_ = Array()
            for excluded_term_ in excluded_terms_:
                inverse_terms_[-1] = excluded_term_ * -1
            # end for
            excluded_terms_ = inverse_terms_
        # end if
        query_args_["tax_query"] = Array(Array({"taxonomy": taxonomy_, "terms": php_array_merge(term_array_, excluded_terms_)}))
    # end if
    return get_posts(query_args_)
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
def get_previous_post_link(format_="&laquo; %link", link_="%title", in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    return get_adjacent_post_link(format_, link_, in_same_term_, excluded_terms_, True, taxonomy_)
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
def previous_post_link(format_="&laquo; %link", link_="%title", in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    php_print(get_previous_post_link(format_, link_, in_same_term_, excluded_terms_, taxonomy_))
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
def get_next_post_link(format_="%link &raquo;", link_="%title", in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    return get_adjacent_post_link(format_, link_, in_same_term_, excluded_terms_, False, taxonomy_)
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
def next_post_link(format_="%link &raquo;", link_="%title", in_same_term_=None, excluded_terms_="", taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    
    php_print(get_next_post_link(format_, link_, in_same_term_, excluded_terms_, taxonomy_))
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
def get_adjacent_post_link(format_=None, link_=None, in_same_term_=None, excluded_terms_="", previous_=None, taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    if previous_ is None:
        previous_ = True
    # end if
    
    if previous_ and is_attachment():
        post_ = get_post(get_post().post_parent)
    else:
        post_ = get_adjacent_post(in_same_term_, excluded_terms_, previous_, taxonomy_)
    # end if
    if (not post_):
        output_ = ""
    else:
        title_ = post_.post_title
        if php_empty(lambda : post_.post_title):
            title_ = __("Previous Post") if previous_ else __("Next Post")
        # end if
        #// This filter is documented in wp-includes/post-template.php
        title_ = apply_filters("the_title", title_, post_.ID)
        date_ = mysql2date(get_option("date_format"), post_.post_date)
        rel_ = "prev" if previous_ else "next"
        string_ = "<a href=\"" + get_permalink(post_) + "\" rel=\"" + rel_ + "\">"
        inlink_ = php_str_replace("%title", title_, link_)
        inlink_ = php_str_replace("%date", date_, inlink_)
        inlink_ = string_ + inlink_ + "</a>"
        output_ = php_str_replace("%link", inlink_, format_)
    # end if
    adjacent_ = "previous" if previous_ else "next"
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
    return apply_filters(str(adjacent_) + str("_post_link"), output_, format_, link_, post_, adjacent_)
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
def adjacent_post_link(format_=None, link_=None, in_same_term_=None, excluded_terms_="", previous_=None, taxonomy_="category", *_args_):
    if in_same_term_ is None:
        in_same_term_ = False
    # end if
    if previous_ is None:
        previous_ = True
    # end if
    
    php_print(get_adjacent_post_link(format_, link_, in_same_term_, excluded_terms_, previous_, taxonomy_))
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
def get_pagenum_link(pagenum_=1, escape_=None, *_args_):
    if escape_ is None:
        escape_ = True
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    pagenum_ = php_int(pagenum_)
    request_ = remove_query_arg("paged")
    home_root_ = php_parse_url(home_url())
    home_root_ = home_root_["path"] if (php_isset(lambda : home_root_["path"])) else ""
    home_root_ = preg_quote(home_root_, "|")
    request_ = php_preg_replace("|^" + home_root_ + "|i", "", request_)
    request_ = php_preg_replace("|^/+|", "", request_)
    if (not wp_rewrite_.using_permalinks()) or is_admin():
        base_ = trailingslashit(get_bloginfo("url"))
        if pagenum_ > 1:
            result_ = add_query_arg("paged", pagenum_, base_ + request_)
        else:
            result_ = base_ + request_
        # end if
    else:
        qs_regex_ = "|\\?.*?$|"
        php_preg_match(qs_regex_, request_, qs_match_)
        if (not php_empty(lambda : qs_match_[0])):
            query_string_ = qs_match_[0]
            request_ = php_preg_replace(qs_regex_, "", request_)
        else:
            query_string_ = ""
        # end if
        request_ = php_preg_replace(str("|") + str(wp_rewrite_.pagination_base) + str("/\\d+/?$|"), "", request_)
        request_ = php_preg_replace("|^" + preg_quote(wp_rewrite_.index, "|") + "|i", "", request_)
        request_ = php_ltrim(request_, "/")
        base_ = trailingslashit(get_bloginfo("url"))
        if wp_rewrite_.using_index_permalinks() and pagenum_ > 1 or "" != request_:
            base_ += wp_rewrite_.index + "/"
        # end if
        if pagenum_ > 1:
            request_ = trailingslashit(request_) if (not php_empty(lambda : request_)) else request_ + user_trailingslashit(wp_rewrite_.pagination_base + "/" + pagenum_, "paged")
        # end if
        result_ = base_ + request_ + query_string_
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
    result_ = apply_filters("get_pagenum_link", result_, pagenum_)
    if escape_:
        return esc_url(result_)
    else:
        return esc_url_raw(result_)
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
def get_next_posts_page_link(max_page_=0, *_args_):
    
    
    global paged_
    php_check_if_defined("paged_")
    if (not is_single()):
        if (not paged_):
            paged_ = 1
        # end if
        nextpage_ = php_intval(paged_) + 1
        if (not max_page_) or max_page_ >= nextpage_:
            return get_pagenum_link(nextpage_)
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
def next_posts(max_page_=0, echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    output_ = esc_url(get_next_posts_page_link(max_page_))
    if echo_:
        php_print(output_)
    else:
        return output_
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
def get_next_posts_link(label_=None, max_page_=0, *_args_):
    if label_ is None:
        label_ = None
    # end if
    
    global paged_
    global wp_query_
    php_check_if_defined("paged_","wp_query_")
    if (not max_page_):
        max_page_ = wp_query_.max_num_pages
    # end if
    if (not paged_):
        paged_ = 1
    # end if
    nextpage_ = php_intval(paged_) + 1
    if None == label_:
        label_ = __("Next Page &raquo;")
    # end if
    if (not is_single()) and nextpage_ <= max_page_:
        #// 
        #// Filters the anchor tag attributes for the next posts page link.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string $attributes Attributes for the anchor tag.
        #//
        attr_ = apply_filters("next_posts_link_attributes", "")
        return "<a href=\"" + next_posts(max_page_, False) + str("\" ") + str(attr_) + str(">") + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label_) + "</a>"
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
def next_posts_link(label_=None, max_page_=0, *_args_):
    if label_ is None:
        label_ = None
    # end if
    
    php_print(get_next_posts_link(label_, max_page_))
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
def get_previous_posts_page_link(*_args_):
    
    
    global paged_
    php_check_if_defined("paged_")
    if (not is_single()):
        nextpage_ = php_intval(paged_) - 1
        if nextpage_ < 1:
            nextpage_ = 1
        # end if
        return get_pagenum_link(nextpage_)
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
def previous_posts(echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    output_ = esc_url(get_previous_posts_page_link())
    if echo_:
        php_print(output_)
    else:
        return output_
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
def get_previous_posts_link(label_=None, *_args_):
    if label_ is None:
        label_ = None
    # end if
    
    global paged_
    php_check_if_defined("paged_")
    if None == label_:
        label_ = __("&laquo; Previous Page")
    # end if
    if (not is_single()) and paged_ > 1:
        #// 
        #// Filters the anchor tag attributes for the previous posts page link.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string $attributes Attributes for the anchor tag.
        #//
        attr_ = apply_filters("previous_posts_link_attributes", "")
        return "<a href=\"" + previous_posts(False) + str("\" ") + str(attr_) + str(">") + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label_) + "</a>"
    # end if
# end def get_previous_posts_link
#// 
#// Displays the previous posts page link.
#// 
#// @since 0.71
#// 
#// @param string $label Optional. Previous page link text.
#//
def previous_posts_link(label_=None, *_args_):
    if label_ is None:
        label_ = None
    # end if
    
    php_print(get_previous_posts_link(label_))
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
def get_posts_nav_link(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_query_
    php_check_if_defined("wp_query_")
    return_ = ""
    if (not is_singular()):
        defaults_ = Array({"sep": " &#8212; ", "prelabel": __("&laquo; Previous Page"), "nxtlabel": __("Next Page &raquo;")})
        args_ = wp_parse_args(args_, defaults_)
        max_num_pages_ = wp_query_.max_num_pages
        paged_ = get_query_var("paged")
        #// Only have sep if there's both prev and next results.
        if paged_ < 2 or paged_ >= max_num_pages_:
            args_["sep"] = ""
        # end if
        if max_num_pages_ > 1:
            return_ = get_previous_posts_link(args_["prelabel"])
            return_ += php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", args_["sep"])
            return_ += get_next_posts_link(args_["nxtlabel"])
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
def posts_nav_link(sep_="", prelabel_="", nxtlabel_="", *_args_):
    
    
    args_ = php_array_filter(php_compact("sep_", "prelabel_", "nxtlabel_"))
    php_print(get_posts_nav_link(args_))
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
def get_the_post_navigation(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
    if (not php_empty(lambda : args_["screen_reader_text"])) and php_empty(lambda : args_["aria_label"]):
        args_["aria_label"] = args_["screen_reader_text"]
    # end if
    args_ = wp_parse_args(args_, Array({"prev_text": "%title", "next_text": "%title", "in_same_term": False, "excluded_terms": "", "taxonomy": "category", "screen_reader_text": __("Post navigation"), "aria_label": __("Posts")}))
    navigation_ = ""
    previous_ = get_previous_post_link("<div class=\"nav-previous\">%link</div>", args_["prev_text"], args_["in_same_term"], args_["excluded_terms"], args_["taxonomy"])
    next_ = get_next_post_link("<div class=\"nav-next\">%link</div>", args_["next_text"], args_["in_same_term"], args_["excluded_terms"], args_["taxonomy"])
    #// Only add markup if there's somewhere to navigate to.
    if previous_ or next_:
        navigation_ = _navigation_markup(previous_ + next_, "post-navigation", args_["screen_reader_text"], args_["aria_label"])
    # end if
    return navigation_
# end def get_the_post_navigation
#// 
#// Displays the navigation to next/previous post, when applicable.
#// 
#// @since 4.1.0
#// 
#// @param array $args Optional. See get_the_post_navigation() for available arguments.
#// Default empty array.
#//
def the_post_navigation(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    php_print(get_the_post_navigation(args_))
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
def get_the_posts_navigation(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    navigation_ = ""
    #// Don't print empty markup if there's only one page.
    if PHP_GLOBALS["wp_query"].max_num_pages > 1:
        #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
        if (not php_empty(lambda : args_["screen_reader_text"])) and php_empty(lambda : args_["aria_label"]):
            args_["aria_label"] = args_["screen_reader_text"]
        # end if
        args_ = wp_parse_args(args_, Array({"prev_text": __("Older posts"), "next_text": __("Newer posts"), "screen_reader_text": __("Posts navigation"), "aria_label": __("Posts")}))
        next_link_ = get_previous_posts_link(args_["next_text"])
        prev_link_ = get_next_posts_link(args_["prev_text"])
        if prev_link_:
            navigation_ += "<div class=\"nav-previous\">" + prev_link_ + "</div>"
        # end if
        if next_link_:
            navigation_ += "<div class=\"nav-next\">" + next_link_ + "</div>"
        # end if
        navigation_ = _navigation_markup(navigation_, "posts-navigation", args_["screen_reader_text"], args_["aria_label"])
    # end if
    return navigation_
# end def get_the_posts_navigation
#// 
#// Displays the navigation to next/previous set of posts, when applicable.
#// 
#// @since 4.1.0
#// 
#// @param array $args Optional. See get_the_posts_navigation() for available arguments.
#// Default empty array.
#//
def the_posts_navigation(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    php_print(get_the_posts_navigation(args_))
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
def get_the_posts_pagination(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    navigation_ = ""
    #// Don't print empty markup if there's only one page.
    if PHP_GLOBALS["wp_query"].max_num_pages > 1:
        #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
        if (not php_empty(lambda : args_["screen_reader_text"])) and php_empty(lambda : args_["aria_label"]):
            args_["aria_label"] = args_["screen_reader_text"]
        # end if
        args_ = wp_parse_args(args_, Array({"mid_size": 1, "prev_text": _x("Previous", "previous set of posts"), "next_text": _x("Next", "next set of posts"), "screen_reader_text": __("Posts navigation"), "aria_label": __("Posts")}))
        #// Make sure we get a string back. Plain is the next best thing.
        if (php_isset(lambda : args_["type"])) and "array" == args_["type"]:
            args_["type"] = "plain"
        # end if
        #// Set up paginated links.
        links_ = paginate_links(args_)
        if links_:
            navigation_ = _navigation_markup(links_, "pagination", args_["screen_reader_text"], args_["aria_label"])
        # end if
    # end if
    return navigation_
# end def get_the_posts_pagination
#// 
#// Displays a paginated navigation to next/previous set of posts, when applicable.
#// 
#// @since 4.1.0
#// 
#// @param array $args Optional. See get_the_posts_pagination() for available arguments.
#// Default empty array.
#//
def the_posts_pagination(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    php_print(get_the_posts_pagination(args_))
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
def _navigation_markup(links_=None, class_="posts-navigation", screen_reader_text_="", aria_label_="", *_args_):
    
    
    if php_empty(lambda : screen_reader_text_):
        screen_reader_text_ = __("Posts navigation")
    # end if
    if php_empty(lambda : aria_label_):
        aria_label_ = screen_reader_text_
    # end if
    template_ = """
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
    template_ = apply_filters("navigation_markup_template", template_, class_)
    return php_sprintf(template_, sanitize_html_class(class_), esc_html(screen_reader_text_), links_, esc_html(aria_label_))
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
def get_comments_pagenum_link(pagenum_=1, max_page_=0, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    pagenum_ = php_int(pagenum_)
    result_ = get_permalink()
    if "newest" == get_option("default_comments_page"):
        if pagenum_ != max_page_:
            if wp_rewrite_.using_permalinks():
                result_ = user_trailingslashit(trailingslashit(result_) + wp_rewrite_.comments_pagination_base + "-" + pagenum_, "commentpaged")
            else:
                result_ = add_query_arg("cpage", pagenum_, result_)
            # end if
        # end if
    elif pagenum_ > 1:
        if wp_rewrite_.using_permalinks():
            result_ = user_trailingslashit(trailingslashit(result_) + wp_rewrite_.comments_pagination_base + "-" + pagenum_, "commentpaged")
        else:
            result_ = add_query_arg("cpage", pagenum_, result_)
        # end if
    # end if
    result_ += "#comments"
    #// 
    #// Filters the comments page number link for the current request.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $result The comments page number link.
    #//
    return apply_filters("get_comments_pagenum_link", result_)
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
def get_next_comments_link(label_="", max_page_=0, *_args_):
    
    
    global wp_query_
    php_check_if_defined("wp_query_")
    if (not is_singular()):
        return
    # end if
    page_ = get_query_var("cpage")
    if (not page_):
        page_ = 1
    # end if
    nextpage_ = php_intval(page_) + 1
    if php_empty(lambda : max_page_):
        max_page_ = wp_query_.max_num_comment_pages
    # end if
    if php_empty(lambda : max_page_):
        max_page_ = get_comment_pages_count()
    # end if
    if nextpage_ > max_page_:
        return
    # end if
    if php_empty(lambda : label_):
        label_ = __("Newer Comments &raquo;")
    # end if
    #// 
    #// Filters the anchor tag attributes for the next comments page link.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $attributes Attributes for the anchor tag.
    #//
    return "<a href=\"" + esc_url(get_comments_pagenum_link(nextpage_, max_page_)) + "\" " + apply_filters("next_comments_link_attributes", "") + ">" + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label_) + "</a>"
# end def get_next_comments_link
#// 
#// Displays the link to the next comments page.
#// 
#// @since 2.7.0
#// 
#// @param string $label    Optional. Label for link text. Default empty.
#// @param int    $max_page Optional. Max page. Default 0.
#//
def next_comments_link(label_="", max_page_=0, *_args_):
    
    
    php_print(get_next_comments_link(label_, max_page_))
# end def next_comments_link
#// 
#// Retrieves the link to the previous comments page.
#// 
#// @since 2.7.1
#// 
#// @param string $label Optional. Label for comments link text. Default empty.
#// @return string|void HTML-formatted link for the previous page of comments.
#//
def get_previous_comments_link(label_="", *_args_):
    
    
    if (not is_singular()):
        return
    # end if
    page_ = get_query_var("cpage")
    if php_intval(page_) <= 1:
        return
    # end if
    prevpage_ = php_intval(page_) - 1
    if php_empty(lambda : label_):
        label_ = __("&laquo; Older Comments")
    # end if
    #// 
    #// Filters the anchor tag attributes for the previous comments page link.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $attributes Attributes for the anchor tag.
    #//
    return "<a href=\"" + esc_url(get_comments_pagenum_link(prevpage_)) + "\" " + apply_filters("previous_comments_link_attributes", "") + ">" + php_preg_replace("/&([^#])(?![a-z]{1,8};)/i", "&#038;$1", label_) + "</a>"
# end def get_previous_comments_link
#// 
#// Displays the link to the previous comments page.
#// 
#// @since 2.7.0
#// 
#// @param string $label Optional. Label for comments link text. Default empty.
#//
def previous_comments_link(label_="", *_args_):
    
    
    php_print(get_previous_comments_link(label_))
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
def paginate_comments_links(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not is_singular()):
        return
    # end if
    page_ = get_query_var("cpage")
    if (not page_):
        page_ = 1
    # end if
    max_page_ = get_comment_pages_count()
    defaults_ = Array({"base": add_query_arg("cpage", "%#%"), "format": "", "total": max_page_, "current": page_, "echo": True, "type": "plain", "add_fragment": "#comments"})
    if wp_rewrite_.using_permalinks():
        defaults_["base"] = user_trailingslashit(trailingslashit(get_permalink()) + wp_rewrite_.comments_pagination_base + "-%#%", "commentpaged")
    # end if
    args_ = wp_parse_args(args_, defaults_)
    page_links_ = paginate_links(args_)
    if args_["echo"] and "array" != args_["type"]:
        php_print(page_links_)
    else:
        return page_links_
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
def get_the_comments_navigation(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    navigation_ = ""
    #// Are there comments to navigate through?
    if get_comment_pages_count() > 1:
        #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
        if (not php_empty(lambda : args_["screen_reader_text"])) and php_empty(lambda : args_["aria_label"]):
            args_["aria_label"] = args_["screen_reader_text"]
        # end if
        args_ = wp_parse_args(args_, Array({"prev_text": __("Older comments"), "next_text": __("Newer comments"), "screen_reader_text": __("Comments navigation"), "aria_label": __("Comments")}))
        prev_link_ = get_previous_comments_link(args_["prev_text"])
        next_link_ = get_next_comments_link(args_["next_text"])
        if prev_link_:
            navigation_ += "<div class=\"nav-previous\">" + prev_link_ + "</div>"
        # end if
        if next_link_:
            navigation_ += "<div class=\"nav-next\">" + next_link_ + "</div>"
        # end if
        navigation_ = _navigation_markup(navigation_, "comment-navigation", args_["screen_reader_text"], args_["aria_label"])
    # end if
    return navigation_
# end def get_the_comments_navigation
#// 
#// Displays navigation to next/previous set of comments, when applicable.
#// 
#// @since 4.4.0
#// 
#// @param array $args See get_the_comments_navigation() for available arguments. Default empty array.
#//
def the_comments_navigation(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    php_print(get_the_comments_navigation(args_))
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
def get_the_comments_pagination(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    navigation_ = ""
    #// Make sure the nav element has an aria-label attribute: fallback to the screen reader text.
    if (not php_empty(lambda : args_["screen_reader_text"])) and php_empty(lambda : args_["aria_label"]):
        args_["aria_label"] = args_["screen_reader_text"]
    # end if
    args_ = wp_parse_args(args_, Array({"screen_reader_text": __("Comments navigation"), "aria_label": __("Comments")}))
    args_["echo"] = False
    #// Make sure we get a string back. Plain is the next best thing.
    if (php_isset(lambda : args_["type"])) and "array" == args_["type"]:
        args_["type"] = "plain"
    # end if
    links_ = paginate_comments_links(args_)
    if links_:
        navigation_ = _navigation_markup(links_, "comments-pagination", args_["screen_reader_text"], args_["aria_label"])
    # end if
    return navigation_
# end def get_the_comments_pagination
#// 
#// Displays a paginated navigation to next/previous set of comments, when applicable.
#// 
#// @since 4.4.0
#// 
#// @param array $args See get_the_comments_pagination() for available arguments. Default empty array.
#//
def the_comments_pagination(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    php_print(get_the_comments_pagination(args_))
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
def home_url(path_="", scheme_=None, *_args_):
    if scheme_ is None:
        scheme_ = None
    # end if
    
    return get_home_url(None, path_, scheme_)
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
def get_home_url(blog_id_=None, path_="", scheme_=None, *_args_):
    if blog_id_ is None:
        blog_id_ = None
    # end if
    if scheme_ is None:
        scheme_ = None
    # end if
    
    global pagenow_
    php_check_if_defined("pagenow_")
    orig_scheme_ = scheme_
    if php_empty(lambda : blog_id_) or (not is_multisite()):
        url_ = get_option("home")
    else:
        switch_to_blog(blog_id_)
        url_ = get_option("home")
        restore_current_blog()
    # end if
    if (not php_in_array(scheme_, Array("http", "https", "relative"))):
        if is_ssl() and (not is_admin()) and "wp-login.php" != pagenow_:
            scheme_ = "https"
        else:
            scheme_ = php_parse_url(url_, PHP_URL_SCHEME)
        # end if
    # end if
    url_ = set_url_scheme(url_, scheme_)
    if path_ and php_is_string(path_):
        url_ += "/" + php_ltrim(path_, "/")
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
    return apply_filters("home_url", url_, path_, orig_scheme_, blog_id_)
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
def site_url(path_="", scheme_=None, *_args_):
    if scheme_ is None:
        scheme_ = None
    # end if
    
    return get_site_url(None, path_, scheme_)
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
def get_site_url(blog_id_=None, path_="", scheme_=None, *_args_):
    if blog_id_ is None:
        blog_id_ = None
    # end if
    if scheme_ is None:
        scheme_ = None
    # end if
    
    if php_empty(lambda : blog_id_) or (not is_multisite()):
        url_ = get_option("siteurl")
    else:
        switch_to_blog(blog_id_)
        url_ = get_option("siteurl")
        restore_current_blog()
    # end if
    url_ = set_url_scheme(url_, scheme_)
    if path_ and php_is_string(path_):
        url_ += "/" + php_ltrim(path_, "/")
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
    return apply_filters("site_url", url_, path_, scheme_, blog_id_)
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
def admin_url(path_="", scheme_="admin", *_args_):
    
    
    return get_admin_url(None, path_, scheme_)
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
def get_admin_url(blog_id_=None, path_="", scheme_="admin", *_args_):
    if blog_id_ is None:
        blog_id_ = None
    # end if
    
    url_ = get_site_url(blog_id_, "wp-admin/", scheme_)
    if path_ and php_is_string(path_):
        url_ += php_ltrim(path_, "/")
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
    return apply_filters("admin_url", url_, path_, blog_id_)
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
def includes_url(path_="", scheme_=None, *_args_):
    if scheme_ is None:
        scheme_ = None
    # end if
    
    url_ = site_url("/" + WPINC + "/", scheme_)
    if path_ and php_is_string(path_):
        url_ += php_ltrim(path_, "/")
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
    return apply_filters("includes_url", url_, path_)
# end def includes_url
#// 
#// Retrieves the URL to the content directory.
#// 
#// @since 2.6.0
#// 
#// @param string $path Optional. Path relative to the content URL. Default empty.
#// @return string Content URL link with optional path appended.
#//
def content_url(path_="", *_args_):
    
    
    url_ = set_url_scheme(WP_CONTENT_URL)
    if path_ and php_is_string(path_):
        url_ += "/" + php_ltrim(path_, "/")
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
    return apply_filters("content_url", url_, path_)
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
def plugins_url(path_="", plugin_="", *_args_):
    
    
    path_ = wp_normalize_path(path_)
    plugin_ = wp_normalize_path(plugin_)
    mu_plugin_dir_ = wp_normalize_path(WPMU_PLUGIN_DIR)
    if (not php_empty(lambda : plugin_)) and 0 == php_strpos(plugin_, mu_plugin_dir_):
        url_ = WPMU_PLUGIN_URL
    else:
        url_ = WP_PLUGIN_URL
    # end if
    url_ = set_url_scheme(url_)
    if (not php_empty(lambda : plugin_)) and php_is_string(plugin_):
        folder_ = php_dirname(plugin_basename(plugin_))
        if "." != folder_:
            url_ += "/" + php_ltrim(folder_, "/")
        # end if
    # end if
    if path_ and php_is_string(path_):
        url_ += "/" + php_ltrim(path_, "/")
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
    return apply_filters("plugins_url", url_, path_, plugin_)
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
def network_site_url(path_="", scheme_=None, *_args_):
    if scheme_ is None:
        scheme_ = None
    # end if
    
    if (not is_multisite()):
        return site_url(path_, scheme_)
    # end if
    current_network_ = get_network()
    if "relative" == scheme_:
        url_ = current_network_.path
    else:
        url_ = set_url_scheme("http://" + current_network_.domain + current_network_.path, scheme_)
    # end if
    if path_ and php_is_string(path_):
        url_ += php_ltrim(path_, "/")
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
    return apply_filters("network_site_url", url_, path_, scheme_)
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
def network_home_url(path_="", scheme_=None, *_args_):
    if scheme_ is None:
        scheme_ = None
    # end if
    
    if (not is_multisite()):
        return home_url(path_, scheme_)
    # end if
    current_network_ = get_network()
    orig_scheme_ = scheme_
    if (not php_in_array(scheme_, Array("http", "https", "relative"))):
        scheme_ = "https" if is_ssl() and (not is_admin()) else "http"
    # end if
    if "relative" == scheme_:
        url_ = current_network_.path
    else:
        url_ = set_url_scheme("http://" + current_network_.domain + current_network_.path, scheme_)
    # end if
    if path_ and php_is_string(path_):
        url_ += php_ltrim(path_, "/")
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
    return apply_filters("network_home_url", url_, path_, orig_scheme_)
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
def network_admin_url(path_="", scheme_="admin", *_args_):
    
    
    if (not is_multisite()):
        return admin_url(path_, scheme_)
    # end if
    url_ = network_site_url("wp-admin/network/", scheme_)
    if path_ and php_is_string(path_):
        url_ += php_ltrim(path_, "/")
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
    return apply_filters("network_admin_url", url_, path_)
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
def user_admin_url(path_="", scheme_="admin", *_args_):
    
    
    url_ = network_site_url("wp-admin/user/", scheme_)
    if path_ and php_is_string(path_):
        url_ += php_ltrim(path_, "/")
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
    return apply_filters("user_admin_url", url_, path_)
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
def self_admin_url(path_="", scheme_="admin", *_args_):
    
    
    if is_network_admin():
        url_ = network_admin_url(path_, scheme_)
    elif is_user_admin():
        url_ = user_admin_url(path_, scheme_)
    else:
        url_ = admin_url(path_, scheme_)
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
    return apply_filters("self_admin_url", url_, path_, scheme_)
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
def set_url_scheme(url_=None, scheme_=None, *_args_):
    if scheme_ is None:
        scheme_ = None
    # end if
    
    orig_scheme_ = scheme_
    if (not scheme_):
        scheme_ = "https" if is_ssl() else "http"
    elif "admin" == scheme_ or "login" == scheme_ or "login_post" == scheme_ or "rpc" == scheme_:
        scheme_ = "https" if is_ssl() or force_ssl_admin() else "http"
    elif "http" != scheme_ and "https" != scheme_ and "relative" != scheme_:
        scheme_ = "https" if is_ssl() else "http"
    # end if
    url_ = php_trim(url_)
    if php_substr(url_, 0, 2) == "//":
        url_ = "http:" + url_
    # end if
    if "relative" == scheme_:
        url_ = php_ltrim(php_preg_replace("#^\\w+://[^/]*#", "", url_))
        if "" != url_ and "/" == url_[0]:
            url_ = "/" + php_ltrim(url_, "/     \n\r ")
        # end if
    else:
        url_ = php_preg_replace("#^\\w+://#", scheme_ + "://", url_)
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
    return apply_filters("set_url_scheme", url_, scheme_, orig_scheme_)
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
def get_dashboard_url(user_id_=0, path_="", scheme_="admin", *_args_):
    
    
    user_id_ = php_int(user_id_) if user_id_ else get_current_user_id()
    blogs_ = get_blogs_of_user(user_id_)
    if is_multisite() and (not user_can(user_id_, "manage_network")) and php_empty(lambda : blogs_):
        url_ = user_admin_url(path_, scheme_)
    elif (not is_multisite()):
        url_ = admin_url(path_, scheme_)
    else:
        current_blog_ = get_current_blog_id()
        if current_blog_ and user_can(user_id_, "manage_network") or php_in_array(current_blog_, php_array_keys(blogs_)):
            url_ = admin_url(path_, scheme_)
        else:
            active_ = get_active_blog_for_user(user_id_)
            if active_:
                url_ = get_admin_url(active_.blog_id, path_, scheme_)
            else:
                url_ = user_admin_url(path_, scheme_)
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
    return apply_filters("user_dashboard_url", url_, user_id_, path_, scheme_)
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
def get_edit_profile_url(user_id_=0, scheme_="admin", *_args_):
    
    
    user_id_ = php_int(user_id_) if user_id_ else get_current_user_id()
    if is_user_admin():
        url_ = user_admin_url("profile.php", scheme_)
    elif is_network_admin():
        url_ = network_admin_url("profile.php", scheme_)
    else:
        url_ = get_dashboard_url(user_id_, "profile.php", scheme_)
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
    return apply_filters("edit_profile_url", url_, user_id_, scheme_)
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
def wp_get_canonical_url(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    if "publish" != post_.post_status:
        return False
    # end if
    canonical_url_ = get_permalink(post_)
    #// If a canonical is being generated for the current page, make sure it has pagination if needed.
    if get_queried_object_id() == post_.ID:
        page_ = get_query_var("page", 0)
        if page_ >= 2:
            if "" == get_option("permalink_structure"):
                canonical_url_ = add_query_arg("page", page_, canonical_url_)
            else:
                canonical_url_ = trailingslashit(canonical_url_) + user_trailingslashit(page_, "single_paged")
            # end if
        # end if
        cpage_ = get_query_var("cpage", 0)
        if cpage_:
            canonical_url_ = get_comments_pagenum_link(cpage_)
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
    return apply_filters("get_canonical_url", canonical_url_, post_)
# end def wp_get_canonical_url
#// 
#// Outputs rel=canonical for singular queries.
#// 
#// @since 2.9.0
#// @since 4.6.0 Adjusted to use `wp_get_canonical_url()`.
#//
def rel_canonical(*_args_):
    
    
    if (not is_singular()):
        return
    # end if
    id_ = get_queried_object_id()
    if 0 == id_:
        return
    # end if
    url_ = wp_get_canonical_url(id_)
    if (not php_empty(lambda : url_)):
        php_print("<link rel=\"canonical\" href=\"" + esc_url(url_) + "\" />" + "\n")
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
def wp_get_shortlink(id_=0, context_="post", allow_slugs_=None, *_args_):
    if allow_slugs_ is None:
        allow_slugs_ = True
    # end if
    
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
    shortlink_ = apply_filters("pre_get_shortlink", False, id_, context_, allow_slugs_)
    if False != shortlink_:
        return shortlink_
    # end if
    post_id_ = 0
    if "query" == context_ and is_singular():
        post_id_ = get_queried_object_id()
        post_ = get_post(post_id_)
    elif "post" == context_:
        post_ = get_post(id_)
        if (not php_empty(lambda : post_.ID)):
            post_id_ = post_.ID
        # end if
    # end if
    shortlink_ = ""
    #// Return `?p=` link for all public post types.
    if (not php_empty(lambda : post_id_)):
        post_type_ = get_post_type_object(post_.post_type)
        if "page" == post_.post_type and get_option("page_on_front") == post_.ID and "page" == get_option("show_on_front"):
            shortlink_ = home_url("/")
        elif post_type_.public:
            shortlink_ = home_url("?p=" + post_id_)
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
    return apply_filters("get_shortlink", shortlink_, id_, context_, allow_slugs_)
# end def wp_get_shortlink
#// 
#// Injects rel=shortlink into the head if a shortlink is defined for the current page.
#// 
#// Attached to the {@see 'wp_head'} action.
#// 
#// @since 3.0.0
#//
def wp_shortlink_wp_head(*_args_):
    
    
    shortlink_ = wp_get_shortlink(0, "query")
    if php_empty(lambda : shortlink_):
        return
    # end if
    php_print("<link rel='shortlink' href='" + esc_url(shortlink_) + "' />\n")
# end def wp_shortlink_wp_head
#// 
#// Sends a Link: rel=shortlink header if a shortlink is defined for the current page.
#// 
#// Attached to the {@see 'wp'} action.
#// 
#// @since 3.0.0
#//
def wp_shortlink_header(*_args_):
    
    
    if php_headers_sent():
        return
    # end if
    shortlink_ = wp_get_shortlink(0, "query")
    if php_empty(lambda : shortlink_):
        return
    # end if
    php_header("Link: <" + shortlink_ + ">; rel=shortlink", False)
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
def the_shortlink(text_="", title_="", before_="", after_="", *_args_):
    
    
    post_ = get_post()
    if php_empty(lambda : text_):
        text_ = __("This is the short link.")
    # end if
    if php_empty(lambda : title_):
        title_ = the_title_attribute(Array({"echo": False}))
    # end if
    shortlink_ = wp_get_shortlink(post_.ID)
    if (not php_empty(lambda : shortlink_)):
        link_ = "<a rel=\"shortlink\" href=\"" + esc_url(shortlink_) + "\" title=\"" + title_ + "\">" + text_ + "</a>"
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
        link_ = apply_filters("the_shortlink", link_, shortlink_, text_, title_)
        php_print(before_, link_, after_)
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
def get_avatar_url(id_or_email_=None, args_=None, *_args_):
    if args_ is None:
        args_ = None
    # end if
    
    args_ = get_avatar_data(id_or_email_, args_)
    return args_["url"]
# end def get_avatar_url
#// 
#// Check if this comment type allows avatars to be retrieved.
#// 
#// @since 5.1.0
#// 
#// @param string $comment_type Comment type to check.
#// @return bool Whether the comment type is allowed for retrieving avatars.
#//
def is_avatar_comment_type(comment_type_=None, *_args_):
    
    
    #// 
    #// Filters the list of allowed comment types for retrieving avatars.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $types An array of content types. Default only contains 'comment'.
    #//
    allowed_comment_types_ = apply_filters("get_avatar_comment_types", Array("comment"))
    return php_in_array(comment_type_, allowed_comment_types_, True)
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
def get_avatar_data(id_or_email_=None, args_=None, *_args_):
    if args_ is None:
        args_ = None
    # end if
    
    args_ = wp_parse_args(args_, Array({"size": 96, "height": None, "width": None, "default": get_option("avatar_default", "mystery"), "force_default": False, "rating": get_option("avatar_rating"), "scheme": None, "processed_args": None, "extra_attr": ""}))
    if php_is_numeric(args_["size"]):
        args_["size"] = absint(args_["size"])
        if (not args_["size"]):
            args_["size"] = 96
        # end if
    else:
        args_["size"] = 96
    # end if
    if php_is_numeric(args_["height"]):
        args_["height"] = absint(args_["height"])
        if (not args_["height"]):
            args_["height"] = args_["size"]
        # end if
    else:
        args_["height"] = args_["size"]
    # end if
    if php_is_numeric(args_["width"]):
        args_["width"] = absint(args_["width"])
        if (not args_["width"]):
            args_["width"] = args_["size"]
        # end if
    else:
        args_["width"] = args_["size"]
    # end if
    if php_empty(lambda : args_["default"]):
        args_["default"] = get_option("avatar_default", "mystery")
    # end if
    for case in Switch(args_["default"]):
        if case("mm"):
            pass
        # end if
        if case("mystery"):
            pass
        # end if
        if case("mysteryman"):
            args_["default"] = "mm"
            break
        # end if
        if case("gravatar_default"):
            args_["default"] = False
            break
        # end if
    # end for
    args_["force_default"] = php_bool(args_["force_default"])
    args_["rating"] = php_strtolower(args_["rating"])
    args_["found_avatar"] = False
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
    args_ = apply_filters("pre_get_avatar_data", args_, id_or_email_)
    if (php_isset(lambda : args_["url"])):
        #// This filter is documented in wp-includes/link-template.php
        return apply_filters("get_avatar_data", args_, id_or_email_)
    # end if
    email_hash_ = ""
    user_ = False
    email_ = False
    if php_is_object(id_or_email_) and (php_isset(lambda : id_or_email_.comment_ID)):
        id_or_email_ = get_comment(id_or_email_)
    # end if
    #// Process the user identifier.
    if php_is_numeric(id_or_email_):
        user_ = get_user_by("id", absint(id_or_email_))
    elif php_is_string(id_or_email_):
        if php_strpos(id_or_email_, "@md5.gravatar.com"):
            #// MD5 hash.
            email_hash_ = php_explode("@", id_or_email_)
        else:
            #// Email address.
            email_ = id_or_email_
        # end if
    elif type(id_or_email_).__name__ == "WP_User":
        #// User object.
        user_ = id_or_email_
    elif type(id_or_email_).__name__ == "WP_Post":
        #// Post object.
        user_ = get_user_by("id", php_int(id_or_email_.post_author))
    elif type(id_or_email_).__name__ == "WP_Comment":
        if (not is_avatar_comment_type(get_comment_type(id_or_email_))):
            args_["url"] = False
            #// This filter is documented in wp-includes/link-template.php
            return apply_filters("get_avatar_data", args_, id_or_email_)
        # end if
        if (not php_empty(lambda : id_or_email_.user_id)):
            user_ = get_user_by("id", php_int(id_or_email_.user_id))
        # end if
        if (not user_) or is_wp_error(user_) and (not php_empty(lambda : id_or_email_.comment_author_email)):
            email_ = id_or_email_.comment_author_email
        # end if
    # end if
    if (not email_hash_):
        if user_:
            email_ = user_.user_email
        # end if
        if email_:
            email_hash_ = php_md5(php_strtolower(php_trim(email_)))
        # end if
    # end if
    if email_hash_:
        args_["found_avatar"] = True
        gravatar_server_ = hexdec(email_hash_[0]) % 3
    else:
        gravatar_server_ = rand(0, 2)
    # end if
    url_args_ = Array({"s": args_["size"], "d": args_["default"], "f": "y" if args_["force_default"] else False, "r": args_["rating"]})
    if is_ssl():
        url_ = "https://secure.gravatar.com/avatar/" + email_hash_
    else:
        url_ = php_sprintf("http://%d.gravatar.com/avatar/%s", gravatar_server_, email_hash_)
    # end if
    url_ = add_query_arg(rawurlencode_deep(php_array_filter(url_args_)), set_url_scheme(url_, args_["scheme"]))
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
    args_["url"] = apply_filters("get_avatar_url", url_, id_or_email_, args_)
    #// 
    #// Filters the avatar data.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array $args        Arguments passed to get_avatar_data(), after processing.
    #// @param mixed $id_or_email The Gravatar to retrieve. Accepts a user ID, Gravatar MD5 hash,
    #// user email, WP_User object, WP_Post object, or WP_Comment object.
    #//
    return apply_filters("get_avatar_data", args_, id_or_email_)
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
def get_theme_file_uri(file_="", *_args_):
    
    
    file_ = php_ltrim(file_, "/")
    if php_empty(lambda : file_):
        url_ = get_stylesheet_directory_uri()
    elif php_file_exists(get_stylesheet_directory() + "/" + file_):
        url_ = get_stylesheet_directory_uri() + "/" + file_
    else:
        url_ = get_template_directory_uri() + "/" + file_
    # end if
    #// 
    #// Filters the URL to a file in the theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $url  The file URL.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("theme_file_uri", url_, file_)
# end def get_theme_file_uri
#// 
#// Retrieves the URL of a file in the parent theme.
#// 
#// @since 4.7.0
#// 
#// @param string $file Optional. File to return the URL for in the template directory.
#// @return string The URL of the file.
#//
def get_parent_theme_file_uri(file_="", *_args_):
    
    
    file_ = php_ltrim(file_, "/")
    if php_empty(lambda : file_):
        url_ = get_template_directory_uri()
    else:
        url_ = get_template_directory_uri() + "/" + file_
    # end if
    #// 
    #// Filters the URL to a file in the parent theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $url  The file URL.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("parent_theme_file_uri", url_, file_)
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
def get_theme_file_path(file_="", *_args_):
    
    
    file_ = php_ltrim(file_, "/")
    if php_empty(lambda : file_):
        path_ = get_stylesheet_directory()
    elif php_file_exists(get_stylesheet_directory() + "/" + file_):
        path_ = get_stylesheet_directory() + "/" + file_
    else:
        path_ = get_template_directory() + "/" + file_
    # end if
    #// 
    #// Filters the path to a file in the theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $path The file path.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("theme_file_path", path_, file_)
# end def get_theme_file_path
#// 
#// Retrieves the path of a file in the parent theme.
#// 
#// @since 4.7.0
#// 
#// @param string $file Optional. File to return the path for in the template directory.
#// @return string The path of the file.
#//
def get_parent_theme_file_path(file_="", *_args_):
    
    
    file_ = php_ltrim(file_, "/")
    if php_empty(lambda : file_):
        path_ = get_template_directory()
    else:
        path_ = get_template_directory() + "/" + file_
    # end if
    #// 
    #// Filters the path to a file in the parent theme.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $path The file path.
    #// @param string $file The requested file to search for.
    #//
    return apply_filters("parent_theme_file_path", path_, file_)
# end def get_parent_theme_file_path
#// 
#// Retrieves the URL to the privacy policy page.
#// 
#// @since 4.9.6
#// 
#// @return string The URL to the privacy policy page. Empty string if it doesn't exist.
#//
def get_privacy_policy_url(*_args_):
    
    
    url_ = ""
    policy_page_id_ = php_int(get_option("wp_page_for_privacy_policy"))
    if (not php_empty(lambda : policy_page_id_)) and get_post_status(policy_page_id_) == "publish":
        url_ = php_str(get_permalink(policy_page_id_))
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
    return apply_filters("privacy_policy_url", url_, policy_page_id_)
# end def get_privacy_policy_url
#// 
#// Displays the privacy policy link with formatting, when applicable.
#// 
#// @since 4.9.6
#// 
#// @param string $before Optional. Display before privacy policy link. Default empty.
#// @param string $after  Optional. Display after privacy policy link. Default empty.
#//
def the_privacy_policy_link(before_="", after_="", *_args_):
    
    
    php_print(get_the_privacy_policy_link(before_, after_))
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
def get_the_privacy_policy_link(before_="", after_="", *_args_):
    
    
    link_ = ""
    privacy_policy_url_ = get_privacy_policy_url()
    policy_page_id_ = php_int(get_option("wp_page_for_privacy_policy"))
    page_title_ = get_the_title(policy_page_id_) if policy_page_id_ else ""
    if privacy_policy_url_ and page_title_:
        link_ = php_sprintf("<a class=\"privacy-policy-link\" href=\"%s\">%s</a>", esc_url(privacy_policy_url_), esc_html(page_title_))
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
    link_ = apply_filters("the_privacy_policy_link", link_, privacy_policy_url_)
    if link_:
        return before_ + link_ + after_
    # end if
    return ""
# end def get_the_privacy_policy_link
