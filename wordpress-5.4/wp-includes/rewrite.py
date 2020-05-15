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
#// WordPress Rewrite API
#// 
#// @package WordPress
#// @subpackage Rewrite
#// 
#// 
#// Endpoint Mask for default, which is nothing.
#// 
#// @since 2.1.0
#//
php_define("EP_NONE", 0)
#// 
#// Endpoint Mask for Permalink.
#// 
#// @since 2.1.0
#//
php_define("EP_PERMALINK", 1)
#// 
#// Endpoint Mask for Attachment.
#// 
#// @since 2.1.0
#//
php_define("EP_ATTACHMENT", 2)
#// 
#// Endpoint Mask for date.
#// 
#// @since 2.1.0
#//
php_define("EP_DATE", 4)
#// 
#// Endpoint Mask for year
#// 
#// @since 2.1.0
#//
php_define("EP_YEAR", 8)
#// 
#// Endpoint Mask for month.
#// 
#// @since 2.1.0
#//
php_define("EP_MONTH", 16)
#// 
#// Endpoint Mask for day.
#// 
#// @since 2.1.0
#//
php_define("EP_DAY", 32)
#// 
#// Endpoint Mask for root.
#// 
#// @since 2.1.0
#//
php_define("EP_ROOT", 64)
#// 
#// Endpoint Mask for comments.
#// 
#// @since 2.1.0
#//
php_define("EP_COMMENTS", 128)
#// 
#// Endpoint Mask for searches.
#// 
#// @since 2.1.0
#//
php_define("EP_SEARCH", 256)
#// 
#// Endpoint Mask for categories.
#// 
#// @since 2.1.0
#//
php_define("EP_CATEGORIES", 512)
#// 
#// Endpoint Mask for tags.
#// 
#// @since 2.3.0
#//
php_define("EP_TAGS", 1024)
#// 
#// Endpoint Mask for authors.
#// 
#// @since 2.1.0
#//
php_define("EP_AUTHORS", 2048)
#// 
#// Endpoint Mask for pages.
#// 
#// @since 2.1.0
#//
php_define("EP_PAGES", 4096)
#// 
#// Endpoint Mask for all archive views.
#// 
#// @since 3.7.0
#//
php_define("EP_ALL_ARCHIVES", EP_DATE | EP_YEAR | EP_MONTH | EP_DAY | EP_CATEGORIES | EP_TAGS | EP_AUTHORS)
#// 
#// Endpoint Mask for everything.
#// 
#// @since 2.1.0
#//
php_define("EP_ALL", EP_PERMALINK | EP_ATTACHMENT | EP_ROOT | EP_COMMENTS | EP_SEARCH | EP_PAGES | EP_ALL_ARCHIVES)
#// 
#// Adds a rewrite rule that transforms a URL structure to a set of query vars.
#// 
#// Any value in the $after parameter that isn't 'bottom' will result in the rule
#// being placed at the top of the rewrite rules.
#// 
#// @since 2.1.0
#// @since 4.4.0 Array support was added to the `$query` parameter.
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string       $regex Regular expression to match request against.
#// @param string|array $query The corresponding query vars for this rewrite rule.
#// @param string       $after Optional. Priority of the new rule. Accepts 'top'
#// or 'bottom'. Default 'bottom'.
#//
def add_rewrite_rule(regex=None, query=None, after="bottom", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    wp_rewrite.add_rule(regex, query, after)
# end def add_rewrite_rule
#// 
#// Add a new rewrite tag (like %postname%).
#// 
#// The $query parameter is optional. If it is omitted you must ensure that
#// you call this on, or before, the {@see 'init'} hook. This is because $query defaults
#// to "$tag=", and for this to work a new query var has to be added.
#// 
#// @since 2.1.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// @global WP         $wp         Current WordPress environment instance.
#// 
#// @param string $tag   Name of the new rewrite tag.
#// @param string $regex Regular expression to substitute the tag for in rewrite rules.
#// @param string $query Optional. String to append to the rewritten query. Must end in '='. Default empty.
#//
def add_rewrite_tag(tag=None, regex=None, query="", *args_):
    
    #// Validate the tag's name.
    if php_strlen(tag) < 3 or "%" != tag[0] or "%" != tag[php_strlen(tag) - 1]:
        return
    # end if
    global wp_rewrite,wp
    php_check_if_defined("wp_rewrite","wp")
    if php_empty(lambda : query):
        qv = php_trim(tag, "%")
        wp.add_query_var(qv)
        query = qv + "="
    # end if
    wp_rewrite.add_rewrite_tag(tag, regex, query)
# end def add_rewrite_tag
#// 
#// Removes an existing rewrite tag (like %postname%).
#// 
#// @since 4.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $tag Name of the rewrite tag.
#//
def remove_rewrite_tag(tag=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    wp_rewrite.remove_rewrite_tag(tag)
# end def remove_rewrite_tag
#// 
#// Add permalink structure.
#// 
#// @since 3.0.0
#// 
#// @see WP_Rewrite::add_permastruct()
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $name   Name for permalink structure.
#// @param string $struct Permalink structure.
#// @param array  $args   Optional. Arguments for building the rules from the permalink structure,
#// see WP_Rewrite::add_permastruct() for full details. Default empty array.
#//
def add_permastruct(name=None, struct=None, args=Array(), *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    #// Back-compat for the old parameters: $with_front and $ep_mask.
    if (not php_is_array(args)):
        args = Array({"with_front": args})
    # end if
    if php_func_num_args() == 4:
        args["ep_mask"] = php_func_get_arg(3)
    # end if
    wp_rewrite.add_permastruct(name, struct, args)
# end def add_permastruct
#// 
#// Removes a permalink structure.
#// 
#// Can only be used to remove permastructs that were added using add_permastruct().
#// Built-in permastructs cannot be removed.
#// 
#// @since 4.5.0
#// 
#// @see WP_Rewrite::remove_permastruct()
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $name Name for permalink structure.
#//
def remove_permastruct(name=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    wp_rewrite.remove_permastruct(name)
# end def remove_permastruct
#// 
#// Add a new feed type like /atom1/.
#// 
#// @since 2.1.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string   $feedname Feed name.
#// @param callable $function Callback to run on feed display.
#// @return string Feed action name.
#//
def add_feed(feedname=None, function=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not php_in_array(feedname, wp_rewrite.feeds)):
        wp_rewrite.feeds[-1] = feedname
    # end if
    hook = "do_feed_" + feedname
    #// Remove default function hook.
    remove_action(hook, hook)
    add_action(hook, function, 10, 2)
    return hook
# end def add_feed
#// 
#// Remove rewrite rules and then recreate rewrite rules.
#// 
#// @since 3.0.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param bool $hard Whether to update .htaccess (hard flush) or just update
#// rewrite_rules transient (soft flush). Default is true (hard).
#//
def flush_rewrite_rules(hard=True, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if php_is_callable(Array(wp_rewrite, "flush_rules")):
        wp_rewrite.flush_rules(hard)
    # end if
# end def flush_rewrite_rules
#// 
#// Add an endpoint, like /trackback/.
#// 
#// Adding an endpoint creates extra rewrite rules for each of the matching
#// places specified by the provided bitmask. For example:
#// 
#// add_rewrite_endpoint( 'json', EP_PERMALINK | EP_PAGES );
#// 
#// will add a new rewrite rule ending with "json(/(.*))?/?$" for every permastruct
#// that describes a permalink (post) or page. This is rewritten to "json=$match"
#// where $match is the part of the URL matched by the endpoint regex (e.g. "foo" in
#// "[permalink]/json/foo/").
#// 
#// A new query var with the same name as the endpoint will also be created.
#// 
#// When specifying $places ensure that you are using the EP_* constants (or a
#// combination of them using the bitwise OR operator) as their values are not
#// guaranteed to remain static (especially `EP_ALL`).
#// 
#// Be sure to flush the rewrite rules - see flush_rewrite_rules() - when your plugin gets
#// activated and deactivated.
#// 
#// @since 2.1.0
#// @since 4.3.0 Added support for skipping query var registration by passing `false` to `$query_var`.
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string      $name      Name of the endpoint.
#// @param int         $places    Endpoint mask describing the places the endpoint should be added.
#// @param string|bool $query_var Name of the corresponding query variable. Pass `false` to skip registering a query_var
#// for this endpoint. Defaults to the value of `$name`.
#//
def add_rewrite_endpoint(name=None, places=None, query_var=True, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    wp_rewrite.add_endpoint(name, places, query_var)
# end def add_rewrite_endpoint
#// 
#// Filters the URL base for taxonomies.
#// 
#// To remove any manually prepended /index.php/.
#// 
#// @access private
#// @since 2.6.0
#// 
#// @param string $base The taxonomy base that we're going to filter
#// @return string
#//
def _wp_filter_taxonomy_base(base=None, *args_):
    
    if (not php_empty(lambda : base)):
        base = php_preg_replace("|^/index\\.php/|", "", base)
        base = php_trim(base, "/")
    # end if
    return base
# end def _wp_filter_taxonomy_base
#// 
#// Resolve numeric slugs that collide with date permalinks.
#// 
#// Permalinks of posts with numeric slugs can sometimes look to WP_Query::parse_query()
#// like a date archive, as when your permalink structure is `/%year%/%postname%/` and
#// a post with post_name '05' has the URL `/2015/05/`.
#// 
#// This function detects conflicts of this type and resolves them in favor of the
#// post permalink.
#// 
#// Note that, since 4.3.0, wp_unique_post_slug() prevents the creation of post slugs
#// that would result in a date archive conflict. The resolution performed in this
#// function is primarily for legacy content, as well as cases when the admin has changed
#// the site's permalink structure in a way that introduces URL conflicts.
#// 
#// @since 4.3.0
#// 
#// @param array $query_vars Optional. Query variables for setting up the loop, as determined in
#// WP::parse_request(). Default empty array.
#// @return array Returns the original array of query vars, with date/post conflicts resolved.
#//
def wp_resolve_numeric_slug_conflicts(query_vars=Array(), *args_):
    
    if (not (php_isset(lambda : query_vars["year"]))) and (not (php_isset(lambda : query_vars["monthnum"]))) and (not (php_isset(lambda : query_vars["day"]))):
        return query_vars
    # end if
    #// Identify the 'postname' position in the permastruct array.
    permastructs = php_array_values(php_array_filter(php_explode("/", get_option("permalink_structure"))))
    postname_index = php_array_search("%postname%", permastructs)
    if False == postname_index:
        return query_vars
    # end if
    #// 
    #// A numeric slug could be confused with a year, month, or day, depending on position. To account for
    #// the possibility of post pagination (eg 2015/2 for the second page of a post called '2015'), our
    #// `is_*` checks are generous: check for year-slug clashes when `is_year` *or* `is_month`, and check
    #// for month-slug clashes when `is_month` *or* `is_day`.
    #//
    compare = ""
    if 0 == postname_index and (php_isset(lambda : query_vars["year"])) or (php_isset(lambda : query_vars["monthnum"])):
        compare = "year"
    elif postname_index and "%year%" == permastructs[postname_index - 1] and (php_isset(lambda : query_vars["monthnum"])) or (php_isset(lambda : query_vars["day"])):
        compare = "monthnum"
    elif postname_index and "%monthnum%" == permastructs[postname_index - 1] and (php_isset(lambda : query_vars["day"])):
        compare = "day"
    # end if
    if (not compare):
        return query_vars
    # end if
    #// This is the potentially clashing slug.
    value = query_vars[compare]
    post = get_page_by_path(value, OBJECT, "post")
    if (not type(post).__name__ == "WP_Post"):
        return query_vars
    # end if
    #// If the date of the post doesn't match the date specified in the URL, resolve to the date archive.
    if php_preg_match("/^([0-9]{4})\\-([0-9]{2})/", post.post_date, matches) and (php_isset(lambda : query_vars["year"])) and "monthnum" == compare or "day" == compare:
        #// $matches[1] is the year the post was published.
        if php_intval(query_vars["year"]) != php_intval(matches[1]):
            return query_vars
        # end if
        #// $matches[2] is the month the post was published.
        if "day" == compare and (php_isset(lambda : query_vars["monthnum"])) and php_intval(query_vars["monthnum"]) != php_intval(matches[2]):
            return query_vars
        # end if
    # end if
    #// 
    #// If the located post contains nextpage pagination, then the URL chunk following postname may be
    #// intended as the page number. Verify that it's a valid page before resolving to it.
    #//
    maybe_page = ""
    if "year" == compare and (php_isset(lambda : query_vars["monthnum"])):
        maybe_page = query_vars["monthnum"]
    elif "monthnum" == compare and (php_isset(lambda : query_vars["day"])):
        maybe_page = query_vars["day"]
    # end if
    #// Bug found in #11694 - 'page' was returning '/4'.
    maybe_page = int(php_trim(maybe_page, "/"))
    post_page_count = php_substr_count(post.post_content, "<!--nextpage-->") + 1
    #// If the post doesn't have multiple pages, but a 'page' candidate is found, resolve to the date archive.
    if 1 == post_page_count and maybe_page:
        return query_vars
    # end if
    #// If the post has multiple pages and the 'page' number isn't valid, resolve to the date archive.
    if post_page_count > 1 and maybe_page > post_page_count:
        return query_vars
    # end if
    #// If we've gotten to this point, we have a slug/date clash. First, adjust for nextpage.
    if "" != maybe_page:
        query_vars["page"] = php_intval(maybe_page)
    # end if
    query_vars["year"] = None
    query_vars["monthnum"] = None
    query_vars["day"] = None
    #// Then, set the identified post.
    query_vars["name"] = post.post_name
    #// Finally, return the modified query vars.
    return query_vars
# end def wp_resolve_numeric_slug_conflicts
#// 
#// Examine a URL and try to determine the post ID it represents.
#// 
#// Checks are supposedly from the hosted site blog.
#// 
#// @since 1.0.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// @global WP         $wp         Current WordPress environment instance.
#// 
#// @param string $url Permalink to check.
#// @return int Post ID, or 0 on failure.
#//
def url_to_postid(url=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    #// 
    #// Filters the URL to derive the post ID from.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $url The URL to derive the post ID from.
    #//
    url = apply_filters("url_to_postid", url)
    url_host = php_str_replace("www.", "", php_parse_url(url, PHP_URL_HOST))
    home_url_host = php_str_replace("www.", "", php_parse_url(home_url(), PHP_URL_HOST))
    #// Bail early if the URL does not belong to this site.
    if url_host and url_host != home_url_host:
        return 0
    # end if
    #// First, check to see if there is a 'p=N' or 'page_id=N' to match against.
    if php_preg_match("#[?&](p|page_id|attachment_id)=(\\d+)#", url, values):
        id = absint(values[2])
        if id:
            return id
        # end if
    # end if
    #// Get rid of the #anchor.
    url_split = php_explode("#", url)
    url = url_split[0]
    #// Get rid of URL ?query=string.
    url_split = php_explode("?", url)
    url = url_split[0]
    #// Set the correct URL scheme.
    scheme = php_parse_url(home_url(), PHP_URL_SCHEME)
    url = set_url_scheme(url, scheme)
    #// Add 'www.' if it is absent and should be there.
    if False != php_strpos(home_url(), "://www.") and False == php_strpos(url, "://www."):
        url = php_str_replace("://", "://www.", url)
    # end if
    #// Strip 'www.' if it is present and shouldn't be.
    if False == php_strpos(home_url(), "://www."):
        url = php_str_replace("://www.", "://", url)
    # end if
    if php_trim(url, "/") == home_url() and "page" == get_option("show_on_front"):
        page_on_front = get_option("page_on_front")
        if page_on_front and type(get_post(page_on_front)).__name__ == "WP_Post":
            return int(page_on_front)
        # end if
    # end if
    #// Check to see if we are using rewrite rules.
    rewrite = wp_rewrite.wp_rewrite_rules()
    #// Not using rewrite rules, and 'p=N' and 'page_id=N' methods failed, so we're out of options.
    if php_empty(lambda : rewrite):
        return 0
    # end if
    #// Strip 'index.php/' if we're not using path info permalinks.
    if (not wp_rewrite.using_index_permalinks()):
        url = php_str_replace(wp_rewrite.index + "/", "", url)
    # end if
    if False != php_strpos(trailingslashit(url), home_url("/")):
        #// Chop off http://domain.com/[path].
        url = php_str_replace(home_url(), "", url)
    else:
        #// Chop off /path/to/blog.
        home_path = php_parse_url(home_url("/"))
        home_path = home_path["path"] if (php_isset(lambda : home_path["path"])) else ""
        url = php_preg_replace(php_sprintf("#^%s#", preg_quote(home_path)), "", trailingslashit(url))
    # end if
    #// Trim leading and lagging slashes.
    url = php_trim(url, "/")
    request = url
    post_type_query_vars = Array()
    for post_type,t in get_post_types(Array(), "objects"):
        if (not php_empty(lambda : t.query_var)):
            post_type_query_vars[t.query_var] = post_type
        # end if
    # end for
    #// Look for matches.
    request_match = request
    for match,query in rewrite:
        #// If the requesting file is the anchor of the match,
        #// prepend it to the path info.
        if (not php_empty(lambda : url)) and url != request and php_strpos(match, url) == 0:
            request_match = url + "/" + request
        # end if
        if php_preg_match(str("#^") + str(match) + str("#"), request_match, matches):
            if wp_rewrite.use_verbose_page_rules and php_preg_match("/pagename=\\$matches\\[([0-9]+)\\]/", query, varmatch):
                #// This is a verbose page match, let's check to be sure about it.
                page = get_page_by_path(matches[varmatch[1]])
                if (not page):
                    continue
                # end if
                post_status_obj = get_post_status_object(page.post_status)
                if (not post_status_obj.public) and (not post_status_obj.protected) and (not post_status_obj.private) and post_status_obj.exclude_from_search:
                    continue
                # end if
            # end if
            #// Got a match.
            #// Trim the query of everything up to the '?'.
            query = php_preg_replace("!^.+\\?!", "", query)
            #// Substitute the substring matches into the query.
            query = addslashes(WP_MatchesMapRegex.apply(query, matches))
            #// Filter out non-public query vars.
            global wp
            php_check_if_defined("wp")
            parse_str(query, query_vars)
            query = Array()
            for key,value in query_vars:
                if php_in_array(key, wp.public_query_vars):
                    query[key] = value
                    if (php_isset(lambda : post_type_query_vars[key])):
                        query["post_type"] = post_type_query_vars[key]
                        query["name"] = value
                    # end if
                # end if
            # end for
            #// Resolve conflicts between posts with numeric slugs and date archive queries.
            query = wp_resolve_numeric_slug_conflicts(query)
            #// Do the query.
            query = php_new_class("WP_Query", lambda : WP_Query(query))
            if (not php_empty(lambda : query.posts)) and query.is_singular:
                return query.post.ID
            else:
                return 0
            # end if
        # end if
    # end for
    return 0
# end def url_to_postid
