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
def add_rewrite_rule(regex_=None, query_=None, after_="bottom", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    wp_rewrite_.add_rule(regex_, query_, after_)
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
def add_rewrite_tag(tag_=None, regex_=None, query_="", *_args_):
    
    
    #// Validate the tag's name.
    if php_strlen(tag_) < 3 or "%" != tag_[0] or "%" != tag_[php_strlen(tag_) - 1]:
        return
    # end if
    global wp_rewrite_
    global wp_
    php_check_if_defined("wp_rewrite_","wp_")
    if php_empty(lambda : query_):
        qv_ = php_trim(tag_, "%")
        wp_.add_query_var(qv_)
        query_ = qv_ + "="
    # end if
    wp_rewrite_.add_rewrite_tag(tag_, regex_, query_)
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
def remove_rewrite_tag(tag_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    wp_rewrite_.remove_rewrite_tag(tag_)
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
def add_permastruct(name_=None, struct_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    #// Back-compat for the old parameters: $with_front and $ep_mask.
    if (not php_is_array(args_)):
        args_ = Array({"with_front": args_})
    # end if
    if php_func_num_args() == 4:
        args_["ep_mask"] = php_func_get_arg(3)
    # end if
    wp_rewrite_.add_permastruct(name_, struct_, args_)
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
def remove_permastruct(name_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    wp_rewrite_.remove_permastruct(name_)
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
def add_feed(feedname_=None, function_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not php_in_array(feedname_, wp_rewrite_.feeds)):
        wp_rewrite_.feeds[-1] = feedname_
    # end if
    hook_ = "do_feed_" + feedname_
    #// Remove default function hook.
    remove_action(hook_, hook_)
    add_action(hook_, function_, 10, 2)
    return hook_
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
def flush_rewrite_rules(hard_=None, *_args_):
    if hard_ is None:
        hard_ = True
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if php_is_callable(Array(wp_rewrite_, "flush_rules")):
        wp_rewrite_.flush_rules(hard_)
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
def add_rewrite_endpoint(name_=None, places_=None, query_var_=None, *_args_):
    if query_var_ is None:
        query_var_ = True
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    wp_rewrite_.add_endpoint(name_, places_, query_var_)
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
def _wp_filter_taxonomy_base(base_=None, *_args_):
    
    
    if (not php_empty(lambda : base_)):
        base_ = php_preg_replace("|^/index\\.php/|", "", base_)
        base_ = php_trim(base_, "/")
    # end if
    return base_
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
def wp_resolve_numeric_slug_conflicts(query_vars_=None, *_args_):
    if query_vars_ is None:
        query_vars_ = Array()
    # end if
    
    if (not (php_isset(lambda : query_vars_["year"]))) and (not (php_isset(lambda : query_vars_["monthnum"]))) and (not (php_isset(lambda : query_vars_["day"]))):
        return query_vars_
    # end if
    #// Identify the 'postname' position in the permastruct array.
    permastructs_ = php_array_values(php_array_filter(php_explode("/", get_option("permalink_structure"))))
    postname_index_ = php_array_search("%postname%", permastructs_)
    if False == postname_index_:
        return query_vars_
    # end if
    #// 
    #// A numeric slug could be confused with a year, month, or day, depending on position. To account for
    #// the possibility of post pagination (eg 2015/2 for the second page of a post called '2015'), our
    #// `is_*` checks are generous: check for year-slug clashes when `is_year` *or* `is_month`, and check
    #// for month-slug clashes when `is_month` *or* `is_day`.
    #//
    compare_ = ""
    if 0 == postname_index_ and (php_isset(lambda : query_vars_["year"])) or (php_isset(lambda : query_vars_["monthnum"])):
        compare_ = "year"
    elif postname_index_ and "%year%" == permastructs_[postname_index_ - 1] and (php_isset(lambda : query_vars_["monthnum"])) or (php_isset(lambda : query_vars_["day"])):
        compare_ = "monthnum"
    elif postname_index_ and "%monthnum%" == permastructs_[postname_index_ - 1] and (php_isset(lambda : query_vars_["day"])):
        compare_ = "day"
    # end if
    if (not compare_):
        return query_vars_
    # end if
    #// This is the potentially clashing slug.
    value_ = query_vars_[compare_]
    post_ = get_page_by_path(value_, OBJECT, "post")
    if (not type(post_).__name__ == "WP_Post"):
        return query_vars_
    # end if
    #// If the date of the post doesn't match the date specified in the URL, resolve to the date archive.
    if php_preg_match("/^([0-9]{4})\\-([0-9]{2})/", post_.post_date, matches_) and (php_isset(lambda : query_vars_["year"])) and "monthnum" == compare_ or "day" == compare_:
        #// $matches[1] is the year the post was published.
        if php_intval(query_vars_["year"]) != php_intval(matches_[1]):
            return query_vars_
        # end if
        #// $matches[2] is the month the post was published.
        if "day" == compare_ and (php_isset(lambda : query_vars_["monthnum"])) and php_intval(query_vars_["monthnum"]) != php_intval(matches_[2]):
            return query_vars_
        # end if
    # end if
    #// 
    #// If the located post contains nextpage pagination, then the URL chunk following postname may be
    #// intended as the page number. Verify that it's a valid page before resolving to it.
    #//
    maybe_page_ = ""
    if "year" == compare_ and (php_isset(lambda : query_vars_["monthnum"])):
        maybe_page_ = query_vars_["monthnum"]
    elif "monthnum" == compare_ and (php_isset(lambda : query_vars_["day"])):
        maybe_page_ = query_vars_["day"]
    # end if
    #// Bug found in #11694 - 'page' was returning '/4'.
    maybe_page_ = php_int(php_trim(maybe_page_, "/"))
    post_page_count_ = php_substr_count(post_.post_content, "<!--nextpage-->") + 1
    #// If the post doesn't have multiple pages, but a 'page' candidate is found, resolve to the date archive.
    if 1 == post_page_count_ and maybe_page_:
        return query_vars_
    # end if
    #// If the post has multiple pages and the 'page' number isn't valid, resolve to the date archive.
    if post_page_count_ > 1 and maybe_page_ > post_page_count_:
        return query_vars_
    # end if
    #// If we've gotten to this point, we have a slug/date clash. First, adjust for nextpage.
    if "" != maybe_page_:
        query_vars_["page"] = php_intval(maybe_page_)
    # end if
    query_vars_["year"] = None
    query_vars_["monthnum"] = None
    query_vars_["day"] = None
    #// Then, set the identified post.
    query_vars_["name"] = post_.post_name
    #// Finally, return the modified query vars.
    return query_vars_
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
def url_to_postid(url_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    #// 
    #// Filters the URL to derive the post ID from.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $url The URL to derive the post ID from.
    #//
    url_ = apply_filters("url_to_postid", url_)
    url_host_ = php_str_replace("www.", "", php_parse_url(url_, PHP_URL_HOST))
    home_url_host_ = php_str_replace("www.", "", php_parse_url(home_url(), PHP_URL_HOST))
    #// Bail early if the URL does not belong to this site.
    if url_host_ and url_host_ != home_url_host_:
        return 0
    # end if
    #// First, check to see if there is a 'p=N' or 'page_id=N' to match against.
    if php_preg_match("#[?&](p|page_id|attachment_id)=(\\d+)#", url_, values_):
        id_ = absint(values_[2])
        if id_:
            return id_
        # end if
    # end if
    #// Get rid of the #anchor.
    url_split_ = php_explode("#", url_)
    url_ = url_split_[0]
    #// Get rid of URL ?query=string.
    url_split_ = php_explode("?", url_)
    url_ = url_split_[0]
    #// Set the correct URL scheme.
    scheme_ = php_parse_url(home_url(), PHP_URL_SCHEME)
    url_ = set_url_scheme(url_, scheme_)
    #// Add 'www.' if it is absent and should be there.
    if False != php_strpos(home_url(), "://www.") and False == php_strpos(url_, "://www."):
        url_ = php_str_replace("://", "://www.", url_)
    # end if
    #// Strip 'www.' if it is present and shouldn't be.
    if False == php_strpos(home_url(), "://www."):
        url_ = php_str_replace("://www.", "://", url_)
    # end if
    if php_trim(url_, "/") == home_url() and "page" == get_option("show_on_front"):
        page_on_front_ = get_option("page_on_front")
        if page_on_front_ and type(get_post(page_on_front_)).__name__ == "WP_Post":
            return php_int(page_on_front_)
        # end if
    # end if
    #// Check to see if we are using rewrite rules.
    rewrite_ = wp_rewrite_.wp_rewrite_rules()
    #// Not using rewrite rules, and 'p=N' and 'page_id=N' methods failed, so we're out of options.
    if php_empty(lambda : rewrite_):
        return 0
    # end if
    #// Strip 'index.php/' if we're not using path info permalinks.
    if (not wp_rewrite_.using_index_permalinks()):
        url_ = php_str_replace(wp_rewrite_.index + "/", "", url_)
    # end if
    if False != php_strpos(trailingslashit(url_), home_url("/")):
        #// Chop off http://domain.com/[path].
        url_ = php_str_replace(home_url(), "", url_)
    else:
        #// Chop off /path/to/blog.
        home_path_ = php_parse_url(home_url("/"))
        home_path_ = home_path_["path"] if (php_isset(lambda : home_path_["path"])) else ""
        url_ = php_preg_replace(php_sprintf("#^%s#", preg_quote(home_path_)), "", trailingslashit(url_))
    # end if
    #// Trim leading and lagging slashes.
    url_ = php_trim(url_, "/")
    request_ = url_
    post_type_query_vars_ = Array()
    for post_type_,t_ in get_post_types(Array(), "objects"):
        if (not php_empty(lambda : t_.query_var)):
            post_type_query_vars_[t_.query_var] = post_type_
        # end if
    # end for
    #// Look for matches.
    request_match_ = request_
    for match_,query_ in rewrite_:
        #// If the requesting file is the anchor of the match,
        #// prepend it to the path info.
        if (not php_empty(lambda : url_)) and url_ != request_ and php_strpos(match_, url_) == 0:
            request_match_ = url_ + "/" + request_
        # end if
        if php_preg_match(str("#^") + str(match_) + str("#"), request_match_, matches_):
            if wp_rewrite_.use_verbose_page_rules and php_preg_match("/pagename=\\$matches\\[([0-9]+)\\]/", query_, varmatch_):
                #// This is a verbose page match, let's check to be sure about it.
                page_ = get_page_by_path(matches_[varmatch_[1]])
                if (not page_):
                    continue
                # end if
                post_status_obj_ = get_post_status_object(page_.post_status)
                if (not post_status_obj_.public) and (not post_status_obj_.protected) and (not post_status_obj_.private) and post_status_obj_.exclude_from_search:
                    continue
                # end if
            # end if
            #// Got a match.
            #// Trim the query of everything up to the '?'.
            query_ = php_preg_replace("!^.+\\?!", "", query_)
            #// Substitute the substring matches into the query.
            query_ = addslashes(WP_MatchesMapRegex.apply(query_, matches_))
            #// Filter out non-public query vars.
            global wp_
            php_check_if_defined("wp_")
            parse_str(query_, query_vars_)
            query_ = Array()
            for key_,value_ in query_vars_:
                if php_in_array(key_, wp_.public_query_vars):
                    query_[key_] = value_
                    if (php_isset(lambda : post_type_query_vars_[key_])):
                        query_["post_type"] = post_type_query_vars_[key_]
                        query_["name"] = value_
                    # end if
                # end if
            # end for
            #// Resolve conflicts between posts with numeric slugs and date archive queries.
            query_ = wp_resolve_numeric_slug_conflicts(query_)
            #// Do the query.
            query_ = php_new_class("WP_Query", lambda : WP_Query(query_))
            if (not php_empty(lambda : query_.posts)) and query_.is_singular:
                return query_.post.ID
            else:
                return 0
            # end if
        # end if
    # end for
    return 0
# end def url_to_postid
