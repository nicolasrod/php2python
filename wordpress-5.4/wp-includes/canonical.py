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
#// Canonical API to handle WordPress Redirecting
#// 
#// Based on "Permalink Redirect" from Scott Yang and "Enforce www. Preference"
#// by Mark Jaquith
#// 
#// @package WordPress
#// @since 2.3.0
#// 
#// 
#// Redirects incoming links to the proper URL based on the site url.
#// 
#// Search engines consider www.somedomain.com and somedomain.com to be two
#// different URLs when they both go to the same location. This SEO enhancement
#// prevents penalty for duplicate content by redirecting all incoming links to
#// one or the other.
#// 
#// Prevents redirection for feeds, trackbacks, searches, and
#// admin URLs. Does not redirect on non-pretty-permalink-supporting IIS 7+,
#// page/post previews, WP admin, Trackbacks, robots.txt, favicon.ico, searches,
#// or on POST requests.
#// 
#// Will also attempt to find the correct link when a user enters a URL that does
#// not exist based on exact WordPress query. Will instead try to parse the URL
#// or query in an attempt to figure the correct page to go to.
#// 
#// @since 2.3.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// @global bool       $is_IIS
#// @global WP_Query   $wp_query   WordPress Query object.
#// @global wpdb       $wpdb       WordPress database abstraction object.
#// @global WP         $wp         Current WordPress environment instance.
#// 
#// @param string $requested_url Optional. The URL that was requested, used to
#// figure if redirect is needed.
#// @param bool $do_redirect Optional. Redirect to the new URL.
#// @return string|void The string of the URL, if redirect needed.
#//
def redirect_canonical(requested_url=None, do_redirect=True, *args_):
    
    global wp_rewrite,is_IIS,wp_query,wpdb,wp
    php_check_if_defined("wp_rewrite","is_IIS","wp_query","wpdb","wp")
    if (php_isset(lambda : PHP_SERVER["REQUEST_METHOD"])) and (not php_in_array(php_strtoupper(PHP_SERVER["REQUEST_METHOD"]), Array("GET", "HEAD"))):
        return
    # end if
    #// If we're not in wp-admin and the post has been published and preview nonce
    #// is non-existent or invalid then no need for preview in query.
    if is_preview() and get_query_var("p") and "publish" == get_post_status(get_query_var("p")):
        if (not (php_isset(lambda : PHP_REQUEST["preview_id"]))) or (not (php_isset(lambda : PHP_REQUEST["preview_nonce"]))) or (not wp_verify_nonce(PHP_REQUEST["preview_nonce"], "post_preview_" + php_int(PHP_REQUEST["preview_id"]))):
            wp_query.is_preview = False
        # end if
    # end if
    if is_trackback() or is_search() or is_admin() or is_preview() or is_robots() or is_favicon() or is_IIS and (not iis7_supports_permalinks()):
        return
    # end if
    if (not requested_url) and (php_isset(lambda : PHP_SERVER["HTTP_HOST"])):
        #// Build the URL in the address bar.
        requested_url = "https://" if is_ssl() else "http://"
        requested_url += PHP_SERVER["HTTP_HOST"]
        requested_url += PHP_SERVER["REQUEST_URI"]
    # end if
    original = php_no_error(lambda: php_parse_url(requested_url))
    if False == original:
        return
    # end if
    redirect = original
    redirect_url = False
    #// Notice fixing.
    if (not (php_isset(lambda : redirect["path"]))):
        redirect["path"] = ""
    # end if
    if (not (php_isset(lambda : redirect["query"]))):
        redirect["query"] = ""
    # end if
    #// 
    #// If the original URL ended with non-breaking spaces, they were almost
    #// certainly inserted by accident. Let's remove them, so the reader doesn't
    #// see a 404 error with no obvious cause.
    #//
    redirect["path"] = php_preg_replace("|(%C2%A0)+$|i", "", redirect["path"])
    #// It's not a preview, so remove it from URL.
    if get_query_var("preview"):
        redirect["query"] = remove_query_arg("preview", redirect["query"])
    # end if
    id = get_query_var("p")
    if is_feed() and id:
        redirect_url = get_post_comments_feed_link(id, get_query_var("feed"))
        if redirect_url:
            redirect["query"] = _remove_qs_args_if_not_in_url(redirect["query"], Array("p", "page_id", "attachment_id", "pagename", "name", "post_type", "feed"), redirect_url)
            redirect["path"] = php_parse_url(redirect_url, PHP_URL_PATH)
        # end if
    # end if
    if is_singular() and 1 > wp_query.post_count and id:
        vars = wpdb.get_results(wpdb.prepare(str("SELECT post_type, post_parent FROM ") + str(wpdb.posts) + str(" WHERE ID = %d"), id))
        if (not php_empty(lambda : vars[0])):
            vars = vars[0]
            if "revision" == vars.post_type and vars.post_parent > 0:
                id = vars.post_parent
            # end if
            redirect_url = get_permalink(id)
            if redirect_url:
                redirect["query"] = _remove_qs_args_if_not_in_url(redirect["query"], Array("p", "page_id", "attachment_id", "pagename", "name", "post_type"), redirect_url)
            # end if
        # end if
    # end if
    #// These tests give us a WP-generated permalink.
    if is_404():
        #// Redirect ?page_id, ?p=, ?attachment_id= to their respective URLs.
        id = php_max(get_query_var("p"), get_query_var("page_id"), get_query_var("attachment_id"))
        redirect_post = get_post(id) if id else False
        if redirect_post:
            post_type_obj = get_post_type_object(redirect_post.post_type)
            if post_type_obj.public and "auto-draft" != redirect_post.post_status:
                redirect_url = get_permalink(redirect_post)
                redirect["query"] = _remove_qs_args_if_not_in_url(redirect["query"], Array("p", "page_id", "attachment_id", "pagename", "name", "post_type"), redirect_url)
            # end if
        # end if
        if get_query_var("day") and get_query_var("monthnum") and get_query_var("year"):
            year = get_query_var("year")
            month = get_query_var("monthnum")
            day = get_query_var("day")
            date = php_sprintf("%04d-%02d-%02d", year, month, day)
            if (not wp_checkdate(month, day, year, date)):
                redirect_url = get_month_link(year, month)
                redirect["query"] = _remove_qs_args_if_not_in_url(redirect["query"], Array("year", "monthnum", "day"), redirect_url)
            # end if
        elif get_query_var("monthnum") and get_query_var("year") and 12 < get_query_var("monthnum"):
            redirect_url = get_year_link(get_query_var("year"))
            redirect["query"] = _remove_qs_args_if_not_in_url(redirect["query"], Array("year", "monthnum"), redirect_url)
        # end if
        if (not redirect_url):
            redirect_url = redirect_guess_404_permalink()
            if redirect_url:
                redirect["query"] = _remove_qs_args_if_not_in_url(redirect["query"], Array("page", "feed", "p", "page_id", "attachment_id", "pagename", "name", "post_type"), redirect_url)
            # end if
        # end if
        if get_query_var("page") and wp_query.post and False != php_strpos(wp_query.post.post_content, "<!--nextpage-->"):
            redirect["path"] = php_rtrim(redirect["path"], php_int(get_query_var("page")) + "/")
            redirect["query"] = remove_query_arg("page", redirect["query"])
            redirect_url = get_permalink(wp_query.post.ID)
        # end if
    elif php_is_object(wp_rewrite) and wp_rewrite.using_permalinks():
        #// Rewriting of old ?p=X, ?m=2004, ?m=200401, ?m=20040101.
        if is_attachment() and (not php_array_diff(php_array_keys(wp.query_vars), Array("attachment", "attachment_id"))) and (not redirect_url):
            if (not php_empty(lambda : PHP_REQUEST["attachment_id"])):
                redirect_url = get_attachment_link(get_query_var("attachment_id"))
                if redirect_url:
                    redirect["query"] = remove_query_arg("attachment_id", redirect["query"])
                # end if
            else:
                redirect_url = get_attachment_link()
            # end if
        elif is_single() and (not php_empty(lambda : PHP_REQUEST["p"])) and (not redirect_url):
            redirect_url = get_permalink(get_query_var("p"))
            if redirect_url:
                redirect["query"] = remove_query_arg(Array("p", "post_type"), redirect["query"])
            # end if
        elif is_single() and (not php_empty(lambda : PHP_REQUEST["name"])) and (not redirect_url):
            redirect_url = get_permalink(wp_query.get_queried_object_id())
            if redirect_url:
                redirect["query"] = remove_query_arg("name", redirect["query"])
            # end if
        elif is_page() and (not php_empty(lambda : PHP_REQUEST["page_id"])) and (not redirect_url):
            redirect_url = get_permalink(get_query_var("page_id"))
            if redirect_url:
                redirect["query"] = remove_query_arg("page_id", redirect["query"])
            # end if
        elif is_page() and (not is_feed()) and "page" == get_option("show_on_front") and get_queried_object_id() == get_option("page_on_front") and (not redirect_url):
            redirect_url = home_url("/")
        elif is_home() and (not php_empty(lambda : PHP_REQUEST["page_id"])) and "page" == get_option("show_on_front") and get_query_var("page_id") == get_option("page_for_posts") and (not redirect_url):
            redirect_url = get_permalink(get_option("page_for_posts"))
            if redirect_url:
                redirect["query"] = remove_query_arg("page_id", redirect["query"])
            # end if
        elif (not php_empty(lambda : PHP_REQUEST["m"])) and is_year() or is_month() or is_day():
            m = get_query_var("m")
            for case in Switch(php_strlen(m)):
                if case(4):
                    #// Yearly.
                    redirect_url = get_year_link(m)
                    break
                # end if
                if case(6):
                    #// Monthly.
                    redirect_url = get_month_link(php_substr(m, 0, 4), php_substr(m, 4, 2))
                    break
                # end if
                if case(8):
                    #// Daily.
                    redirect_url = get_day_link(php_substr(m, 0, 4), php_substr(m, 4, 2), php_substr(m, 6, 2))
                    break
                # end if
            # end for
            if redirect_url:
                redirect["query"] = remove_query_arg("m", redirect["query"])
            # end if
            pass
        elif is_day() and get_query_var("year") and get_query_var("monthnum") and (not php_empty(lambda : PHP_REQUEST["day"])):
            redirect_url = get_day_link(get_query_var("year"), get_query_var("monthnum"), get_query_var("day"))
            if redirect_url:
                redirect["query"] = remove_query_arg(Array("year", "monthnum", "day"), redirect["query"])
            # end if
        elif is_month() and get_query_var("year") and (not php_empty(lambda : PHP_REQUEST["monthnum"])):
            redirect_url = get_month_link(get_query_var("year"), get_query_var("monthnum"))
            if redirect_url:
                redirect["query"] = remove_query_arg(Array("year", "monthnum"), redirect["query"])
            # end if
        elif is_year() and (not php_empty(lambda : PHP_REQUEST["year"])):
            redirect_url = get_year_link(get_query_var("year"))
            if redirect_url:
                redirect["query"] = remove_query_arg("year", redirect["query"])
            # end if
        elif is_author() and (not php_empty(lambda : PHP_REQUEST["author"])) and php_preg_match("|^[0-9]+$|", PHP_REQUEST["author"]):
            author = get_userdata(get_query_var("author"))
            if False != author and wpdb.get_var(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE ") + str(wpdb.posts) + str(".post_author = %d AND ") + str(wpdb.posts) + str(".post_status = 'publish' LIMIT 1"), author.ID)):
                redirect_url = get_author_posts_url(author.ID, author.user_nicename)
                if redirect_url:
                    redirect["query"] = remove_query_arg("author", redirect["query"])
                # end if
            # end if
        elif is_category() or is_tag() or is_tax():
            #// Terms (tags/categories).
            term_count = 0
            for tax_query in wp_query.tax_query.queried_terms:
                term_count += php_count(tax_query["terms"])
            # end for
            obj = wp_query.get_queried_object()
            if term_count <= 1 and (not php_empty(lambda : obj.term_id)):
                tax_url = get_term_link(php_int(obj.term_id), obj.taxonomy)
                if tax_url and (not is_wp_error(tax_url)):
                    if (not php_empty(lambda : redirect["query"])):
                        #// Strip taxonomy query vars off the URL.
                        qv_remove = Array("term", "taxonomy")
                        if is_category():
                            qv_remove[-1] = "category_name"
                            qv_remove[-1] = "cat"
                        elif is_tag():
                            qv_remove[-1] = "tag"
                            qv_remove[-1] = "tag_id"
                        else:
                            #// Custom taxonomies will have a custom query var, remove those too.
                            tax_obj = get_taxonomy(obj.taxonomy)
                            if False != tax_obj.query_var:
                                qv_remove[-1] = tax_obj.query_var
                            # end if
                        # end if
                        rewrite_vars = php_array_diff(php_array_keys(wp_query.query), php_array_keys(PHP_REQUEST))
                        #// Check to see if all the query vars are coming from the rewrite, none are set via $_GET.
                        if (not php_array_diff(rewrite_vars, php_array_keys(PHP_REQUEST))):
                            #// Remove all of the per-tax query vars.
                            redirect["query"] = remove_query_arg(qv_remove, redirect["query"])
                            #// Create the destination URL for this taxonomy.
                            tax_url = php_parse_url(tax_url)
                            if (not php_empty(lambda : tax_url["query"])):
                                #// Taxonomy accessible via ?taxonomy=...&term=... or any custom query var.
                                parse_str(tax_url["query"], query_vars)
                                redirect["query"] = add_query_arg(query_vars, redirect["query"])
                            else:
                                #// Taxonomy is accessible via a "pretty URL".
                                redirect["path"] = tax_url["path"]
                            # end if
                        else:
                            #// Some query vars are set via $_GET. Unset those from $_GET that exist via the rewrite.
                            for _qv in qv_remove:
                                if (php_isset(lambda : rewrite_vars[_qv])):
                                    redirect["query"] = remove_query_arg(_qv, redirect["query"])
                                # end if
                            # end for
                        # end if
                    # end if
                # end if
            # end if
        elif is_single() and php_strpos(wp_rewrite.permalink_structure, "%category%") != False:
            cat = get_query_var("category_name")
            if cat:
                category = get_category_by_path(cat)
                if (not category) or is_wp_error(category) or (not has_term(category.term_id, "category", wp_query.get_queried_object_id())):
                    redirect_url = get_permalink(wp_query.get_queried_object_id())
                # end if
            # end if
        # end if
        #// Post paging.
        if is_singular() and get_query_var("page"):
            if (not redirect_url):
                redirect_url = get_permalink(get_queried_object_id())
            # end if
            page = get_query_var("page")
            if page > 1:
                if is_front_page():
                    redirect_url = trailingslashit(redirect_url) + user_trailingslashit(str(wp_rewrite.pagination_base) + str("/") + str(page), "paged")
                else:
                    redirect_url = trailingslashit(redirect_url) + user_trailingslashit(page, "single_paged")
                # end if
            # end if
            redirect["query"] = remove_query_arg("page", redirect["query"])
        # end if
        #// Paging and feeds.
        if get_query_var("paged") or is_feed() or get_query_var("cpage"):
            while True:
                
                if not (php_preg_match(str("#/") + str(wp_rewrite.pagination_base) + str("/?[0-9]+?(/+)?$#"), redirect["path"]) or php_preg_match("#/(comments/?)?(feed|rss|rdf|atom|rss2)(/+)?$#", redirect["path"]) or php_preg_match(str("#/") + str(wp_rewrite.comments_pagination_base) + str("-[0-9]+(/+)?$#"), redirect["path"])):
                    break
                # end if
                #// Strip off paging and feed.
                redirect["path"] = php_preg_replace(str("#/") + str(wp_rewrite.pagination_base) + str("/?[0-9]+?(/+)?$#"), "/", redirect["path"])
                #// Strip off any existing paging.
                redirect["path"] = php_preg_replace("#/(comments/?)?(feed|rss2?|rdf|atom)(/+|$)#", "/", redirect["path"])
                #// Strip off feed endings.
                redirect["path"] = php_preg_replace(str("#/") + str(wp_rewrite.comments_pagination_base) + str("-[0-9]+?(/+)?$#"), "/", redirect["path"])
                pass
            # end while
            addl_path = ""
            if is_feed() and php_in_array(get_query_var("feed"), wp_rewrite.feeds):
                addl_path = trailingslashit(addl_path) if (not php_empty(lambda : addl_path)) else ""
                if (not is_singular()) and get_query_var("withcomments"):
                    addl_path += "comments/"
                # end if
                if "rss" == get_default_feed() and "feed" == get_query_var("feed") or "rss" == get_query_var("feed"):
                    addl_path += user_trailingslashit("feed/" + "" if get_default_feed() == "rss2" else "rss2", "feed")
                else:
                    addl_path += user_trailingslashit("feed/" + "" if get_default_feed() == get_query_var("feed") or "feed" == get_query_var("feed") else get_query_var("feed"), "feed")
                # end if
                redirect["query"] = remove_query_arg("feed", redirect["query"])
            elif is_feed() and "old" == get_query_var("feed"):
                old_feed_files = Array({"wp-atom.php": "atom", "wp-commentsrss2.php": "comments_rss2", "wp-feed.php": get_default_feed(), "wp-rdf.php": "rdf", "wp-rss.php": "rss2", "wp-rss2.php": "rss2"})
                if (php_isset(lambda : old_feed_files[php_basename(redirect["path"])])):
                    redirect_url = get_feed_link(old_feed_files[php_basename(redirect["path"])])
                    wp_redirect(redirect_url, 301)
                    php_exit(0)
                # end if
            # end if
            if get_query_var("paged") > 0:
                paged = get_query_var("paged")
                redirect["query"] = remove_query_arg("paged", redirect["query"])
                if (not is_feed()):
                    if paged > 1 and (not is_single()):
                        addl_path = trailingslashit(addl_path) if (not php_empty(lambda : addl_path)) else "" + user_trailingslashit(str(wp_rewrite.pagination_base) + str("/") + str(paged), "paged")
                    elif (not is_single()):
                        addl_path = trailingslashit(addl_path) if (not php_empty(lambda : addl_path)) else ""
                    # end if
                elif paged > 1:
                    redirect["query"] = add_query_arg("paged", paged, redirect["query"])
                # end if
            # end if
            if get_option("page_comments") and "newest" == get_option("default_comments_page") and get_query_var("cpage") > 0 or "newest" != get_option("default_comments_page") and get_query_var("cpage") > 1:
                addl_path = trailingslashit(addl_path) if (not php_empty(lambda : addl_path)) else "" + user_trailingslashit(wp_rewrite.comments_pagination_base + "-" + get_query_var("cpage"), "commentpaged")
                redirect["query"] = remove_query_arg("cpage", redirect["query"])
            # end if
            redirect["path"] = user_trailingslashit(php_preg_replace("|/" + preg_quote(wp_rewrite.index, "|") + "/?$|", "/", redirect["path"]))
            #// Strip off trailing /index.php/.
            if (not php_empty(lambda : addl_path)) and wp_rewrite.using_index_permalinks() and php_strpos(redirect["path"], "/" + wp_rewrite.index + "/") == False:
                redirect["path"] = trailingslashit(redirect["path"]) + wp_rewrite.index + "/"
            # end if
            if (not php_empty(lambda : addl_path)):
                redirect["path"] = trailingslashit(redirect["path"]) + addl_path
            # end if
            redirect_url = redirect["scheme"] + "://" + redirect["host"] + redirect["path"]
        # end if
        if "wp-register.php" == php_basename(redirect["path"]):
            if is_multisite():
                #// This filter is documented in wp-login.php
                redirect_url = apply_filters("wp_signup_location", network_site_url("wp-signup.php"))
            else:
                redirect_url = wp_registration_url()
            # end if
            wp_redirect(redirect_url, 301)
            php_exit(0)
        # end if
    # end if
    #// Tack on any additional query vars.
    redirect["query"] = php_preg_replace("#^\\??&*?#", "", redirect["query"])
    if redirect_url and (not php_empty(lambda : redirect["query"])):
        parse_str(redirect["query"], _parsed_query)
        redirect = php_no_error(lambda: php_parse_url(redirect_url))
        if (not php_empty(lambda : _parsed_query["name"])) and (not php_empty(lambda : redirect["query"])):
            parse_str(redirect["query"], _parsed_redirect_query)
            if php_empty(lambda : _parsed_redirect_query["name"]):
                _parsed_query["name"] = None
            # end if
        # end if
        _parsed_query = php_array_combine(rawurlencode_deep(php_array_keys(_parsed_query)), rawurlencode_deep(php_array_values(_parsed_query)))
        redirect_url = add_query_arg(_parsed_query, redirect_url)
    # end if
    if redirect_url:
        redirect = php_no_error(lambda: php_parse_url(redirect_url))
    # end if
    #// www.example.com vs. example.com
    user_home = php_no_error(lambda: php_parse_url(home_url()))
    if (not php_empty(lambda : user_home["host"])):
        redirect["host"] = user_home["host"]
    # end if
    if php_empty(lambda : user_home["path"]):
        user_home["path"] = "/"
    # end if
    #// Handle ports.
    if (not php_empty(lambda : user_home["port"])):
        redirect["port"] = user_home["port"]
    else:
        redirect["port"] = None
    # end if
    #// Trailing /index.php.
    redirect["path"] = php_preg_replace("|/" + preg_quote(wp_rewrite.index, "|") + "/*?$|", "/", redirect["path"])
    punctuation_pattern = php_implode("|", php_array_map("preg_quote", Array(" ", "%20", "!", "%21", "\"", "%22", "'", "%27", "(", "%28", ")", "%29", ",", "%2C", ".", "%2E", ";", "%3B", "{", "%7B", "}", "%7D", "%E2%80%9C", "%E2%80%9D")))
    #// Remove trailing spaces and end punctuation from the path.
    redirect["path"] = php_preg_replace(str("#(") + str(punctuation_pattern) + str(")+$#"), "", redirect["path"])
    if (not php_empty(lambda : redirect["query"])):
        #// Remove trailing spaces and end punctuation from certain terminating query string args.
        redirect["query"] = php_preg_replace(str("#((^|&)(p|page_id|cat|tag)=[^&]*?)(") + str(punctuation_pattern) + str(")+$#"), "$1", redirect["query"])
        #// Clean up empty query strings.
        redirect["query"] = php_trim(php_preg_replace("#(^|&)(p|page_id|cat|tag)=?(&|$)#", "&", redirect["query"]), "&")
        #// Redirect obsolete feeds.
        redirect["query"] = php_preg_replace("#(^|&)feed=rss(&|$)#", "$1feed=rss2$2", redirect["query"])
        #// Remove redundant leading ampersands.
        redirect["query"] = php_preg_replace("#^\\??&*?#", "", redirect["query"])
    # end if
    #// Strip /index.php/ when we're not using PATHINFO permalinks.
    if (not wp_rewrite.using_index_permalinks()):
        redirect["path"] = php_str_replace("/" + wp_rewrite.index + "/", "/", redirect["path"])
    # end if
    #// Trailing slashes.
    if php_is_object(wp_rewrite) and wp_rewrite.using_permalinks() and (not is_404()) and (not is_front_page()) or is_front_page() and get_query_var("paged") > 1:
        user_ts_type = ""
        if get_query_var("paged") > 0:
            user_ts_type = "paged"
        else:
            for type in Array("single", "category", "page", "day", "month", "year", "home"):
                func = "is_" + type
                if php_call_user_func(func):
                    user_ts_type = type
                    break
                # end if
            # end for
        # end if
        redirect["path"] = user_trailingslashit(redirect["path"], user_ts_type)
    elif is_front_page():
        redirect["path"] = trailingslashit(redirect["path"])
    # end if
    #// Strip multiple slashes out of the URL.
    if php_strpos(redirect["path"], "//") > -1:
        redirect["path"] = php_preg_replace("|/+|", "/", redirect["path"])
    # end if
    #// Always trailing slash the Front Page URL.
    if trailingslashit(redirect["path"]) == trailingslashit(user_home["path"]):
        redirect["path"] = trailingslashit(redirect["path"])
    # end if
    #// Ignore differences in host capitalization, as this can lead to infinite redirects.
    #// Only redirect no-www <=> yes-www.
    if php_strtolower(original["host"]) == php_strtolower(redirect["host"]) or php_strtolower(original["host"]) != "www." + php_strtolower(redirect["host"]) and "www." + php_strtolower(original["host"]) != php_strtolower(redirect["host"]):
        redirect["host"] = original["host"]
    # end if
    compare_original = Array(original["host"], original["path"])
    if (not php_empty(lambda : original["port"])):
        compare_original[-1] = original["port"]
    # end if
    if (not php_empty(lambda : original["query"])):
        compare_original[-1] = original["query"]
    # end if
    compare_redirect = Array(redirect["host"], redirect["path"])
    if (not php_empty(lambda : redirect["port"])):
        compare_redirect[-1] = redirect["port"]
    # end if
    if (not php_empty(lambda : redirect["query"])):
        compare_redirect[-1] = redirect["query"]
    # end if
    if compare_original != compare_redirect:
        redirect_url = redirect["scheme"] + "://" + redirect["host"]
        if (not php_empty(lambda : redirect["port"])):
            redirect_url += ":" + redirect["port"]
        # end if
        redirect_url += redirect["path"]
        if (not php_empty(lambda : redirect["query"])):
            redirect_url += "?" + redirect["query"]
        # end if
    # end if
    if (not redirect_url) or redirect_url == requested_url:
        return
    # end if
    #// Hex encoded octets are case-insensitive.
    if False != php_strpos(requested_url, "%"):
        if (not php_function_exists("lowercase_octets")):
            #// 
            #// Converts the first hex-encoded octet match to lowercase.
            #// 
            #// @since 3.1.0
            #// @ignore
            #// 
            #// @param array $matches Hex-encoded octet matches for the requested URL.
            #// @return string Lowercased version of the first match.
            #//
            def lowercase_octets(matches=None, *args_):
                
                return php_strtolower(matches[0])
            # end def lowercase_octets
        # end if
        requested_url = preg_replace_callback("|%[a-fA-F0-9][a-fA-F0-9]|", "lowercase_octets", requested_url)
    # end if
    #// 
    #// Filters the canonical redirect URL.
    #// 
    #// Returning false to this filter will cancel the redirect.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $redirect_url  The redirect URL.
    #// @param string $requested_url The requested URL.
    #//
    redirect_url = apply_filters("redirect_canonical", redirect_url, requested_url)
    #// Yes, again -- in case the filter aborted the request.
    if (not redirect_url) or strip_fragment_from_url(redirect_url) == strip_fragment_from_url(requested_url):
        return
    # end if
    if do_redirect:
        #// Protect against chained redirects.
        if (not redirect_canonical(redirect_url, False)):
            wp_redirect(redirect_url, 301)
            php_exit(0)
        else:
            #// Debug.
            #// die("1: $redirect_url<br />2: " . redirect_canonical( $redirect_url, false ) );
            return
        # end if
    else:
        return redirect_url
    # end if
# end def redirect_canonical
#// 
#// Removes arguments from a query string if they are not present in a URL
#// DO NOT use this in plugin code.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @param string $query_string
#// @param array $args_to_check
#// @param string $url
#// @return string The altered query string
#//
def _remove_qs_args_if_not_in_url(query_string=None, args_to_check=None, url=None, *args_):
    
    parsed_url = php_no_error(lambda: php_parse_url(url))
    if (not php_empty(lambda : parsed_url["query"])):
        parse_str(parsed_url["query"], parsed_query)
        for qv in args_to_check:
            if (not (php_isset(lambda : parsed_query[qv]))):
                query_string = remove_query_arg(qv, query_string)
            # end if
        # end for
    else:
        query_string = remove_query_arg(args_to_check, query_string)
    # end if
    return query_string
# end def _remove_qs_args_if_not_in_url
#// 
#// Strips the #fragment from a URL, if one is present.
#// 
#// @since 4.4.0
#// 
#// @param string $url The URL to strip.
#// @return string The altered URL.
#//
def strip_fragment_from_url(url=None, *args_):
    
    parsed_url = php_no_error(lambda: php_parse_url(url))
    if (not php_empty(lambda : parsed_url["host"])):
        #// This mirrors code in redirect_canonical(). It does not handle every case.
        url = parsed_url["scheme"] + "://" + parsed_url["host"]
        if (not php_empty(lambda : parsed_url["port"])):
            url += ":" + parsed_url["port"]
        # end if
        if (not php_empty(lambda : parsed_url["path"])):
            url += parsed_url["path"]
        # end if
        if (not php_empty(lambda : parsed_url["query"])):
            url += "?" + parsed_url["query"]
        # end if
    # end if
    return url
# end def strip_fragment_from_url
#// 
#// Attempts to guess the correct URL based on query vars
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return string|false The correct URL if one is found. False on failure.
#//
def redirect_guess_404_permalink(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if get_query_var("name"):
        where = wpdb.prepare("post_name LIKE %s", wpdb.esc_like(get_query_var("name")) + "%")
        #// If any of post_type, year, monthnum, or day are set, use them to refine the query.
        if get_query_var("post_type"):
            where += wpdb.prepare(" AND post_type = %s", get_query_var("post_type"))
        else:
            where += " AND post_type IN ('" + php_implode("', '", get_post_types(Array({"public": True}))) + "')"
        # end if
        if get_query_var("year"):
            where += wpdb.prepare(" AND YEAR(post_date) = %d", get_query_var("year"))
        # end if
        if get_query_var("monthnum"):
            where += wpdb.prepare(" AND MONTH(post_date) = %d", get_query_var("monthnum"))
        # end if
        if get_query_var("day"):
            where += wpdb.prepare(" AND DAYOFMONTH(post_date) = %d", get_query_var("day"))
        # end if
        post_id = wpdb.get_var(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE ") + str(where) + str(" AND post_status = 'publish'"))
        if (not post_id):
            return False
        # end if
        if get_query_var("feed"):
            return get_post_comments_feed_link(post_id, get_query_var("feed"))
        elif get_query_var("page") and 1 < get_query_var("page"):
            return trailingslashit(get_permalink(post_id)) + user_trailingslashit(get_query_var("page"), "single_paged")
        else:
            return get_permalink(post_id)
        # end if
    # end if
    return False
# end def redirect_guess_404_permalink
#// 
#// Redirects a variety of shorthand URLs to the admin.
#// 
#// If a user visits example.com/admin, they'll be redirected to /wp-admin.
#// Visiting /login redirects to /wp-login.php, and so on.
#// 
#// @since 3.4.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#//
def wp_redirect_admin_locations(*args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not is_404() and wp_rewrite.using_permalinks()):
        return
    # end if
    admins = Array(home_url("wp-admin", "relative"), home_url("dashboard", "relative"), home_url("admin", "relative"), site_url("dashboard", "relative"), site_url("admin", "relative"))
    if php_in_array(untrailingslashit(PHP_SERVER["REQUEST_URI"]), admins):
        wp_redirect(admin_url())
        php_exit(0)
    # end if
    logins = Array(home_url("wp-login.php", "relative"), home_url("login", "relative"), site_url("login", "relative"))
    if php_in_array(untrailingslashit(PHP_SERVER["REQUEST_URI"]), logins):
        wp_redirect(wp_login_url())
        php_exit(0)
    # end if
# end def wp_redirect_admin_locations
