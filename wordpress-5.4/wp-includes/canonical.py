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
def redirect_canonical(requested_url_=None, do_redirect_=None, *_args_):
    
    
    global wp_rewrite_
    global is_IIS_
    global wp_query_
    global wpdb_
    global wp_
    php_check_if_defined("wp_rewrite_","is_IIS_","wp_query_","wpdb_","wp_")
    if (php_isset(lambda : PHP_SERVER["REQUEST_METHOD"])) and (not php_in_array(php_strtoupper(PHP_SERVER["REQUEST_METHOD"]), Array("GET", "HEAD"))):
        return
    # end if
    #// If we're not in wp-admin and the post has been published and preview nonce
    #// is non-existent or invalid then no need for preview in query.
    if is_preview() and get_query_var("p") and "publish" == get_post_status(get_query_var("p")):
        if (not (php_isset(lambda : PHP_REQUEST["preview_id"]))) or (not (php_isset(lambda : PHP_REQUEST["preview_nonce"]))) or (not wp_verify_nonce(PHP_REQUEST["preview_nonce"], "post_preview_" + php_int(PHP_REQUEST["preview_id"]))):
            wp_query_.is_preview = False
        # end if
    # end if
    if is_trackback() or is_search() or is_admin() or is_preview() or is_robots() or is_favicon() or is_IIS_ and (not iis7_supports_permalinks()):
        return
    # end if
    if (not requested_url_) and (php_isset(lambda : PHP_SERVER["HTTP_HOST"])):
        #// Build the URL in the address bar.
        requested_url_ = "https://" if is_ssl() else "http://"
        requested_url_ += PHP_SERVER["HTTP_HOST"]
        requested_url_ += PHP_SERVER["REQUEST_URI"]
    # end if
    original_ = php_no_error(lambda: php_parse_url(requested_url_))
    if False == original_:
        return
    # end if
    redirect_ = original_
    redirect_url_ = False
    #// Notice fixing.
    if (not (php_isset(lambda : redirect_["path"]))):
        redirect_["path"] = ""
    # end if
    if (not (php_isset(lambda : redirect_["query"]))):
        redirect_["query"] = ""
    # end if
    #// 
    #// If the original URL ended with non-breaking spaces, they were almost
    #// certainly inserted by accident. Let's remove them, so the reader doesn't
    #// see a 404 error with no obvious cause.
    #//
    redirect_["path"] = php_preg_replace("|(%C2%A0)+$|i", "", redirect_["path"])
    #// It's not a preview, so remove it from URL.
    if get_query_var("preview"):
        redirect_["query"] = remove_query_arg("preview", redirect_["query"])
    # end if
    id_ = get_query_var("p")
    if is_feed() and id_:
        redirect_url_ = get_post_comments_feed_link(id_, get_query_var("feed"))
        if redirect_url_:
            redirect_["query"] = _remove_qs_args_if_not_in_url(redirect_["query"], Array("p", "page_id", "attachment_id", "pagename", "name", "post_type", "feed"), redirect_url_)
            redirect_["path"] = php_parse_url(redirect_url_, PHP_URL_PATH)
        # end if
    # end if
    if is_singular() and 1 > wp_query_.post_count and id_:
        vars_ = wpdb_.get_results(wpdb_.prepare(str("SELECT post_type, post_parent FROM ") + str(wpdb_.posts) + str(" WHERE ID = %d"), id_))
        if (not php_empty(lambda : vars_[0])):
            vars_ = vars_[0]
            if "revision" == vars_.post_type and vars_.post_parent > 0:
                id_ = vars_.post_parent
            # end if
            redirect_url_ = get_permalink(id_)
            if redirect_url_:
                redirect_["query"] = _remove_qs_args_if_not_in_url(redirect_["query"], Array("p", "page_id", "attachment_id", "pagename", "name", "post_type"), redirect_url_)
            # end if
        # end if
    # end if
    #// These tests give us a WP-generated permalink.
    if is_404():
        #// Redirect ?page_id, ?p=, ?attachment_id= to their respective URLs.
        id_ = php_max(get_query_var("p"), get_query_var("page_id"), get_query_var("attachment_id"))
        redirect_post_ = get_post(id_) if id_ else False
        if redirect_post_:
            post_type_obj_ = get_post_type_object(redirect_post_.post_type)
            if post_type_obj_.public and "auto-draft" != redirect_post_.post_status:
                redirect_url_ = get_permalink(redirect_post_)
                redirect_["query"] = _remove_qs_args_if_not_in_url(redirect_["query"], Array("p", "page_id", "attachment_id", "pagename", "name", "post_type"), redirect_url_)
            # end if
        # end if
        if get_query_var("day") and get_query_var("monthnum") and get_query_var("year"):
            year_ = get_query_var("year")
            month_ = get_query_var("monthnum")
            day_ = get_query_var("day")
            date_ = php_sprintf("%04d-%02d-%02d", year_, month_, day_)
            if (not wp_checkdate(month_, day_, year_, date_)):
                redirect_url_ = get_month_link(year_, month_)
                redirect_["query"] = _remove_qs_args_if_not_in_url(redirect_["query"], Array("year", "monthnum", "day"), redirect_url_)
            # end if
        elif get_query_var("monthnum") and get_query_var("year") and 12 < get_query_var("monthnum"):
            redirect_url_ = get_year_link(get_query_var("year"))
            redirect_["query"] = _remove_qs_args_if_not_in_url(redirect_["query"], Array("year", "monthnum"), redirect_url_)
        # end if
        if (not redirect_url_):
            redirect_url_ = redirect_guess_404_permalink()
            if redirect_url_:
                redirect_["query"] = _remove_qs_args_if_not_in_url(redirect_["query"], Array("page", "feed", "p", "page_id", "attachment_id", "pagename", "name", "post_type"), redirect_url_)
            # end if
        # end if
        if get_query_var("page") and wp_query_.post and False != php_strpos(wp_query_.post.post_content, "<!--nextpage-->"):
            redirect_["path"] = php_rtrim(redirect_["path"], php_int(get_query_var("page")) + "/")
            redirect_["query"] = remove_query_arg("page", redirect_["query"])
            redirect_url_ = get_permalink(wp_query_.post.ID)
        # end if
    elif php_is_object(wp_rewrite_) and wp_rewrite_.using_permalinks():
        #// Rewriting of old ?p=X, ?m=2004, ?m=200401, ?m=20040101.
        if is_attachment() and (not php_array_diff(php_array_keys(wp_.query_vars), Array("attachment", "attachment_id"))) and (not redirect_url_):
            if (not php_empty(lambda : PHP_REQUEST["attachment_id"])):
                redirect_url_ = get_attachment_link(get_query_var("attachment_id"))
                if redirect_url_:
                    redirect_["query"] = remove_query_arg("attachment_id", redirect_["query"])
                # end if
            else:
                redirect_url_ = get_attachment_link()
            # end if
        elif is_single() and (not php_empty(lambda : PHP_REQUEST["p"])) and (not redirect_url_):
            redirect_url_ = get_permalink(get_query_var("p"))
            if redirect_url_:
                redirect_["query"] = remove_query_arg(Array("p", "post_type"), redirect_["query"])
            # end if
        elif is_single() and (not php_empty(lambda : PHP_REQUEST["name"])) and (not redirect_url_):
            redirect_url_ = get_permalink(wp_query_.get_queried_object_id())
            if redirect_url_:
                redirect_["query"] = remove_query_arg("name", redirect_["query"])
            # end if
        elif is_page() and (not php_empty(lambda : PHP_REQUEST["page_id"])) and (not redirect_url_):
            redirect_url_ = get_permalink(get_query_var("page_id"))
            if redirect_url_:
                redirect_["query"] = remove_query_arg("page_id", redirect_["query"])
            # end if
        elif is_page() and (not is_feed()) and "page" == get_option("show_on_front") and get_queried_object_id() == get_option("page_on_front") and (not redirect_url_):
            redirect_url_ = home_url("/")
        elif is_home() and (not php_empty(lambda : PHP_REQUEST["page_id"])) and "page" == get_option("show_on_front") and get_query_var("page_id") == get_option("page_for_posts") and (not redirect_url_):
            redirect_url_ = get_permalink(get_option("page_for_posts"))
            if redirect_url_:
                redirect_["query"] = remove_query_arg("page_id", redirect_["query"])
            # end if
        elif (not php_empty(lambda : PHP_REQUEST["m"])) and is_year() or is_month() or is_day():
            m_ = get_query_var("m")
            for case in Switch(php_strlen(m_)):
                if case(4):
                    #// Yearly.
                    redirect_url_ = get_year_link(m_)
                    break
                # end if
                if case(6):
                    #// Monthly.
                    redirect_url_ = get_month_link(php_substr(m_, 0, 4), php_substr(m_, 4, 2))
                    break
                # end if
                if case(8):
                    #// Daily.
                    redirect_url_ = get_day_link(php_substr(m_, 0, 4), php_substr(m_, 4, 2), php_substr(m_, 6, 2))
                    break
                # end if
            # end for
            if redirect_url_:
                redirect_["query"] = remove_query_arg("m", redirect_["query"])
            # end if
            pass
        elif is_day() and get_query_var("year") and get_query_var("monthnum") and (not php_empty(lambda : PHP_REQUEST["day"])):
            redirect_url_ = get_day_link(get_query_var("year"), get_query_var("monthnum"), get_query_var("day"))
            if redirect_url_:
                redirect_["query"] = remove_query_arg(Array("year", "monthnum", "day"), redirect_["query"])
            # end if
        elif is_month() and get_query_var("year") and (not php_empty(lambda : PHP_REQUEST["monthnum"])):
            redirect_url_ = get_month_link(get_query_var("year"), get_query_var("monthnum"))
            if redirect_url_:
                redirect_["query"] = remove_query_arg(Array("year", "monthnum"), redirect_["query"])
            # end if
        elif is_year() and (not php_empty(lambda : PHP_REQUEST["year"])):
            redirect_url_ = get_year_link(get_query_var("year"))
            if redirect_url_:
                redirect_["query"] = remove_query_arg("year", redirect_["query"])
            # end if
        elif is_author() and (not php_empty(lambda : PHP_REQUEST["author"])) and php_preg_match("|^[0-9]+$|", PHP_REQUEST["author"]):
            author_ = get_userdata(get_query_var("author"))
            if False != author_ and wpdb_.get_var(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE ") + str(wpdb_.posts) + str(".post_author = %d AND ") + str(wpdb_.posts) + str(".post_status = 'publish' LIMIT 1"), author_.ID)):
                redirect_url_ = get_author_posts_url(author_.ID, author_.user_nicename)
                if redirect_url_:
                    redirect_["query"] = remove_query_arg("author", redirect_["query"])
                # end if
            # end if
        elif is_category() or is_tag() or is_tax():
            #// Terms (tags/categories).
            term_count_ = 0
            for tax_query_ in wp_query_.tax_query.queried_terms:
                term_count_ += php_count(tax_query_["terms"])
            # end for
            obj_ = wp_query_.get_queried_object()
            if term_count_ <= 1 and (not php_empty(lambda : obj_.term_id)):
                tax_url_ = get_term_link(php_int(obj_.term_id), obj_.taxonomy)
                if tax_url_ and (not is_wp_error(tax_url_)):
                    if (not php_empty(lambda : redirect_["query"])):
                        #// Strip taxonomy query vars off the URL.
                        qv_remove_ = Array("term", "taxonomy")
                        if is_category():
                            qv_remove_[-1] = "category_name"
                            qv_remove_[-1] = "cat"
                        elif is_tag():
                            qv_remove_[-1] = "tag"
                            qv_remove_[-1] = "tag_id"
                        else:
                            #// Custom taxonomies will have a custom query var, remove those too.
                            tax_obj_ = get_taxonomy(obj_.taxonomy)
                            if False != tax_obj_.query_var:
                                qv_remove_[-1] = tax_obj_.query_var
                            # end if
                        # end if
                        rewrite_vars_ = php_array_diff(php_array_keys(wp_query_.query), php_array_keys(PHP_REQUEST))
                        #// Check to see if all the query vars are coming from the rewrite, none are set via $_GET.
                        if (not php_array_diff(rewrite_vars_, php_array_keys(PHP_REQUEST))):
                            #// Remove all of the per-tax query vars.
                            redirect_["query"] = remove_query_arg(qv_remove_, redirect_["query"])
                            #// Create the destination URL for this taxonomy.
                            tax_url_ = php_parse_url(tax_url_)
                            if (not php_empty(lambda : tax_url_["query"])):
                                #// Taxonomy accessible via ?taxonomy=...&term=... or any custom query var.
                                parse_str(tax_url_["query"], query_vars_)
                                redirect_["query"] = add_query_arg(query_vars_, redirect_["query"])
                            else:
                                #// Taxonomy is accessible via a "pretty URL".
                                redirect_["path"] = tax_url_["path"]
                            # end if
                        else:
                            #// Some query vars are set via $_GET. Unset those from $_GET that exist via the rewrite.
                            for _qv_ in qv_remove_:
                                if (php_isset(lambda : rewrite_vars_[_qv_])):
                                    redirect_["query"] = remove_query_arg(_qv_, redirect_["query"])
                                # end if
                            # end for
                        # end if
                    # end if
                # end if
            # end if
        elif is_single() and php_strpos(wp_rewrite_.permalink_structure, "%category%") != False:
            cat_ = get_query_var("category_name")
            if cat_:
                category_ = get_category_by_path(cat_)
                if (not category_) or is_wp_error(category_) or (not has_term(category_.term_id, "category", wp_query_.get_queried_object_id())):
                    redirect_url_ = get_permalink(wp_query_.get_queried_object_id())
                # end if
            # end if
        # end if
        #// Post paging.
        if is_singular() and get_query_var("page"):
            if (not redirect_url_):
                redirect_url_ = get_permalink(get_queried_object_id())
            # end if
            page_ = get_query_var("page")
            if page_ > 1:
                if is_front_page():
                    redirect_url_ = trailingslashit(redirect_url_) + user_trailingslashit(str(wp_rewrite_.pagination_base) + str("/") + str(page_), "paged")
                else:
                    redirect_url_ = trailingslashit(redirect_url_) + user_trailingslashit(page_, "single_paged")
                # end if
            # end if
            redirect_["query"] = remove_query_arg("page", redirect_["query"])
        # end if
        #// Paging and feeds.
        if get_query_var("paged") or is_feed() or get_query_var("cpage"):
            while True:
                
                if not (php_preg_match(str("#/") + str(wp_rewrite_.pagination_base) + str("/?[0-9]+?(/+)?$#"), redirect_["path"]) or php_preg_match("#/(comments/?)?(feed|rss|rdf|atom|rss2)(/+)?$#", redirect_["path"]) or php_preg_match(str("#/") + str(wp_rewrite_.comments_pagination_base) + str("-[0-9]+(/+)?$#"), redirect_["path"])):
                    break
                # end if
                #// Strip off paging and feed.
                redirect_["path"] = php_preg_replace(str("#/") + str(wp_rewrite_.pagination_base) + str("/?[0-9]+?(/+)?$#"), "/", redirect_["path"])
                #// Strip off any existing paging.
                redirect_["path"] = php_preg_replace("#/(comments/?)?(feed|rss2?|rdf|atom)(/+|$)#", "/", redirect_["path"])
                #// Strip off feed endings.
                redirect_["path"] = php_preg_replace(str("#/") + str(wp_rewrite_.comments_pagination_base) + str("-[0-9]+?(/+)?$#"), "/", redirect_["path"])
                pass
            # end while
            addl_path_ = ""
            if is_feed() and php_in_array(get_query_var("feed"), wp_rewrite_.feeds):
                addl_path_ = trailingslashit(addl_path_) if (not php_empty(lambda : addl_path_)) else ""
                if (not is_singular()) and get_query_var("withcomments"):
                    addl_path_ += "comments/"
                # end if
                if "rss" == get_default_feed() and "feed" == get_query_var("feed") or "rss" == get_query_var("feed"):
                    addl_path_ += user_trailingslashit("feed/" + "" if get_default_feed() == "rss2" else "rss2", "feed")
                else:
                    addl_path_ += user_trailingslashit("feed/" + "" if get_default_feed() == get_query_var("feed") or "feed" == get_query_var("feed") else get_query_var("feed"), "feed")
                # end if
                redirect_["query"] = remove_query_arg("feed", redirect_["query"])
            elif is_feed() and "old" == get_query_var("feed"):
                old_feed_files_ = Array({"wp-atom.php": "atom", "wp-commentsrss2.php": "comments_rss2", "wp-feed.php": get_default_feed(), "wp-rdf.php": "rdf", "wp-rss.php": "rss2", "wp-rss2.php": "rss2"})
                if (php_isset(lambda : old_feed_files_[php_basename(redirect_["path"])])):
                    redirect_url_ = get_feed_link(old_feed_files_[php_basename(redirect_["path"])])
                    wp_redirect(redirect_url_, 301)
                    php_exit(0)
                # end if
            # end if
            if get_query_var("paged") > 0:
                paged_ = get_query_var("paged")
                redirect_["query"] = remove_query_arg("paged", redirect_["query"])
                if (not is_feed()):
                    if paged_ > 1 and (not is_single()):
                        addl_path_ = trailingslashit(addl_path_) if (not php_empty(lambda : addl_path_)) else "" + user_trailingslashit(str(wp_rewrite_.pagination_base) + str("/") + str(paged_), "paged")
                    elif (not is_single()):
                        addl_path_ = trailingslashit(addl_path_) if (not php_empty(lambda : addl_path_)) else ""
                    # end if
                elif paged_ > 1:
                    redirect_["query"] = add_query_arg("paged", paged_, redirect_["query"])
                # end if
            # end if
            if get_option("page_comments") and "newest" == get_option("default_comments_page") and get_query_var("cpage") > 0 or "newest" != get_option("default_comments_page") and get_query_var("cpage") > 1:
                addl_path_ = trailingslashit(addl_path_) if (not php_empty(lambda : addl_path_)) else "" + user_trailingslashit(wp_rewrite_.comments_pagination_base + "-" + get_query_var("cpage"), "commentpaged")
                redirect_["query"] = remove_query_arg("cpage", redirect_["query"])
            # end if
            redirect_["path"] = user_trailingslashit(php_preg_replace("|/" + preg_quote(wp_rewrite_.index, "|") + "/?$|", "/", redirect_["path"]))
            #// Strip off trailing /index.php/.
            if (not php_empty(lambda : addl_path_)) and wp_rewrite_.using_index_permalinks() and php_strpos(redirect_["path"], "/" + wp_rewrite_.index + "/") == False:
                redirect_["path"] = trailingslashit(redirect_["path"]) + wp_rewrite_.index + "/"
            # end if
            if (not php_empty(lambda : addl_path_)):
                redirect_["path"] = trailingslashit(redirect_["path"]) + addl_path_
            # end if
            redirect_url_ = redirect_["scheme"] + "://" + redirect_["host"] + redirect_["path"]
        # end if
        if "wp-register.php" == php_basename(redirect_["path"]):
            if is_multisite():
                #// This filter is documented in wp-login.php
                redirect_url_ = apply_filters("wp_signup_location", network_site_url("wp-signup.php"))
            else:
                redirect_url_ = wp_registration_url()
            # end if
            wp_redirect(redirect_url_, 301)
            php_exit(0)
        # end if
    # end if
    #// Tack on any additional query vars.
    redirect_["query"] = php_preg_replace("#^\\??&*?#", "", redirect_["query"])
    if redirect_url_ and (not php_empty(lambda : redirect_["query"])):
        parse_str(redirect_["query"], _parsed_query_)
        redirect_ = php_no_error(lambda: php_parse_url(redirect_url_))
        if (not php_empty(lambda : _parsed_query_["name"])) and (not php_empty(lambda : redirect_["query"])):
            parse_str(redirect_["query"], _parsed_redirect_query_)
            if php_empty(lambda : _parsed_redirect_query_["name"]):
                _parsed_query_["name"] = None
            # end if
        # end if
        _parsed_query_ = php_array_combine(rawurlencode_deep(php_array_keys(_parsed_query_)), rawurlencode_deep(php_array_values(_parsed_query_)))
        redirect_url_ = add_query_arg(_parsed_query_, redirect_url_)
    # end if
    if redirect_url_:
        redirect_ = php_no_error(lambda: php_parse_url(redirect_url_))
    # end if
    #// www.example.com vs. example.com
    user_home_ = php_no_error(lambda: php_parse_url(home_url()))
    if (not php_empty(lambda : user_home_["host"])):
        redirect_["host"] = user_home_["host"]
    # end if
    if php_empty(lambda : user_home_["path"]):
        user_home_["path"] = "/"
    # end if
    #// Handle ports.
    if (not php_empty(lambda : user_home_["port"])):
        redirect_["port"] = user_home_["port"]
    else:
        redirect_["port"] = None
    # end if
    #// Trailing /index.php.
    redirect_["path"] = php_preg_replace("|/" + preg_quote(wp_rewrite_.index, "|") + "/*?$|", "/", redirect_["path"])
    punctuation_pattern_ = php_implode("|", php_array_map("preg_quote", Array(" ", "%20", "!", "%21", "\"", "%22", "'", "%27", "(", "%28", ")", "%29", ",", "%2C", ".", "%2E", ";", "%3B", "{", "%7B", "}", "%7D", "%E2%80%9C", "%E2%80%9D")))
    #// Remove trailing spaces and end punctuation from the path.
    redirect_["path"] = php_preg_replace(str("#(") + str(punctuation_pattern_) + str(")+$#"), "", redirect_["path"])
    if (not php_empty(lambda : redirect_["query"])):
        #// Remove trailing spaces and end punctuation from certain terminating query string args.
        redirect_["query"] = php_preg_replace(str("#((^|&)(p|page_id|cat|tag)=[^&]*?)(") + str(punctuation_pattern_) + str(")+$#"), "$1", redirect_["query"])
        #// Clean up empty query strings.
        redirect_["query"] = php_trim(php_preg_replace("#(^|&)(p|page_id|cat|tag)=?(&|$)#", "&", redirect_["query"]), "&")
        #// Redirect obsolete feeds.
        redirect_["query"] = php_preg_replace("#(^|&)feed=rss(&|$)#", "$1feed=rss2$2", redirect_["query"])
        #// Remove redundant leading ampersands.
        redirect_["query"] = php_preg_replace("#^\\??&*?#", "", redirect_["query"])
    # end if
    #// Strip /index.php/ when we're not using PATHINFO permalinks.
    if (not wp_rewrite_.using_index_permalinks()):
        redirect_["path"] = php_str_replace("/" + wp_rewrite_.index + "/", "/", redirect_["path"])
    # end if
    #// Trailing slashes.
    if php_is_object(wp_rewrite_) and wp_rewrite_.using_permalinks() and (not is_404()) and (not is_front_page()) or is_front_page() and get_query_var("paged") > 1:
        user_ts_type_ = ""
        if get_query_var("paged") > 0:
            user_ts_type_ = "paged"
        else:
            for type_ in Array("single", "category", "page", "day", "month", "year", "home"):
                func_ = "is_" + type_
                if php_call_user_func(func_):
                    user_ts_type_ = type_
                    break
                # end if
            # end for
        # end if
        redirect_["path"] = user_trailingslashit(redirect_["path"], user_ts_type_)
    elif is_front_page():
        redirect_["path"] = trailingslashit(redirect_["path"])
    # end if
    #// Strip multiple slashes out of the URL.
    if php_strpos(redirect_["path"], "//") > -1:
        redirect_["path"] = php_preg_replace("|/+|", "/", redirect_["path"])
    # end if
    #// Always trailing slash the Front Page URL.
    if trailingslashit(redirect_["path"]) == trailingslashit(user_home_["path"]):
        redirect_["path"] = trailingslashit(redirect_["path"])
    # end if
    #// Ignore differences in host capitalization, as this can lead to infinite redirects.
    #// Only redirect no-www <=> yes-www.
    if php_strtolower(original_["host"]) == php_strtolower(redirect_["host"]) or php_strtolower(original_["host"]) != "www." + php_strtolower(redirect_["host"]) and "www." + php_strtolower(original_["host"]) != php_strtolower(redirect_["host"]):
        redirect_["host"] = original_["host"]
    # end if
    compare_original_ = Array(original_["host"], original_["path"])
    if (not php_empty(lambda : original_["port"])):
        compare_original_[-1] = original_["port"]
    # end if
    if (not php_empty(lambda : original_["query"])):
        compare_original_[-1] = original_["query"]
    # end if
    compare_redirect_ = Array(redirect_["host"], redirect_["path"])
    if (not php_empty(lambda : redirect_["port"])):
        compare_redirect_[-1] = redirect_["port"]
    # end if
    if (not php_empty(lambda : redirect_["query"])):
        compare_redirect_[-1] = redirect_["query"]
    # end if
    if compare_original_ != compare_redirect_:
        redirect_url_ = redirect_["scheme"] + "://" + redirect_["host"]
        if (not php_empty(lambda : redirect_["port"])):
            redirect_url_ += ":" + redirect_["port"]
        # end if
        redirect_url_ += redirect_["path"]
        if (not php_empty(lambda : redirect_["query"])):
            redirect_url_ += "?" + redirect_["query"]
        # end if
    # end if
    if (not redirect_url_) or redirect_url_ == requested_url_:
        return
    # end if
    #// Hex encoded octets are case-insensitive.
    if False != php_strpos(requested_url_, "%"):
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
            def lowercase_octets(matches_=None, *_args_):
                if do_redirect_ is None:
                    do_redirect_ = True
                # end if
                
                return php_strtolower(matches_[0])
            # end def lowercase_octets
        # end if
        requested_url_ = preg_replace_callback("|%[a-fA-F0-9][a-fA-F0-9]|", "lowercase_octets", requested_url_)
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
    redirect_url_ = apply_filters("redirect_canonical", redirect_url_, requested_url_)
    #// Yes, again -- in case the filter aborted the request.
    if (not redirect_url_) or strip_fragment_from_url(redirect_url_) == strip_fragment_from_url(requested_url_):
        return
    # end if
    if do_redirect_:
        #// Protect against chained redirects.
        if (not redirect_canonical(redirect_url_, False)):
            wp_redirect(redirect_url_, 301)
            php_exit(0)
        else:
            #// Debug.
            #// die("1: $redirect_url<br />2: " . redirect_canonical( $redirect_url, false ) );
            return
        # end if
    else:
        return redirect_url_
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
def _remove_qs_args_if_not_in_url(query_string_=None, args_to_check_=None, url_=None, *_args_):
    
    
    parsed_url_ = php_no_error(lambda: php_parse_url(url_))
    if (not php_empty(lambda : parsed_url_["query"])):
        parse_str(parsed_url_["query"], parsed_query_)
        for qv_ in args_to_check_:
            if (not (php_isset(lambda : parsed_query_[qv_]))):
                query_string_ = remove_query_arg(qv_, query_string_)
            # end if
        # end for
    else:
        query_string_ = remove_query_arg(args_to_check_, query_string_)
    # end if
    return query_string_
# end def _remove_qs_args_if_not_in_url
#// 
#// Strips the #fragment from a URL, if one is present.
#// 
#// @since 4.4.0
#// 
#// @param string $url The URL to strip.
#// @return string The altered URL.
#//
def strip_fragment_from_url(url_=None, *_args_):
    
    
    parsed_url_ = php_no_error(lambda: php_parse_url(url_))
    if (not php_empty(lambda : parsed_url_["host"])):
        #// This mirrors code in redirect_canonical(). It does not handle every case.
        url_ = parsed_url_["scheme"] + "://" + parsed_url_["host"]
        if (not php_empty(lambda : parsed_url_["port"])):
            url_ += ":" + parsed_url_["port"]
        # end if
        if (not php_empty(lambda : parsed_url_["path"])):
            url_ += parsed_url_["path"]
        # end if
        if (not php_empty(lambda : parsed_url_["query"])):
            url_ += "?" + parsed_url_["query"]
        # end if
    # end if
    return url_
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
def redirect_guess_404_permalink(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if get_query_var("name"):
        where_ = wpdb_.prepare("post_name LIKE %s", wpdb_.esc_like(get_query_var("name")) + "%")
        #// If any of post_type, year, monthnum, or day are set, use them to refine the query.
        if get_query_var("post_type"):
            where_ += wpdb_.prepare(" AND post_type = %s", get_query_var("post_type"))
        else:
            where_ += " AND post_type IN ('" + php_implode("', '", get_post_types(Array({"public": True}))) + "')"
        # end if
        if get_query_var("year"):
            where_ += wpdb_.prepare(" AND YEAR(post_date) = %d", get_query_var("year"))
        # end if
        if get_query_var("monthnum"):
            where_ += wpdb_.prepare(" AND MONTH(post_date) = %d", get_query_var("monthnum"))
        # end if
        if get_query_var("day"):
            where_ += wpdb_.prepare(" AND DAYOFMONTH(post_date) = %d", get_query_var("day"))
        # end if
        post_id_ = wpdb_.get_var(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE ") + str(where_) + str(" AND post_status = 'publish'"))
        if (not post_id_):
            return False
        # end if
        if get_query_var("feed"):
            return get_post_comments_feed_link(post_id_, get_query_var("feed"))
        elif get_query_var("page") and 1 < get_query_var("page"):
            return trailingslashit(get_permalink(post_id_)) + user_trailingslashit(get_query_var("page"), "single_paged")
        else:
            return get_permalink(post_id_)
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
def wp_redirect_admin_locations(*_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not is_404() and wp_rewrite_.using_permalinks()):
        return
    # end if
    admins_ = Array(home_url("wp-admin", "relative"), home_url("dashboard", "relative"), home_url("admin", "relative"), site_url("dashboard", "relative"), site_url("admin", "relative"))
    if php_in_array(untrailingslashit(PHP_SERVER["REQUEST_URI"]), admins_):
        wp_redirect(admin_url())
        php_exit(0)
    # end if
    logins_ = Array(home_url("wp-login.php", "relative"), home_url("login", "relative"), site_url("login", "relative"))
    if php_in_array(untrailingslashit(PHP_SERVER["REQUEST_URI"]), logins_):
        wp_redirect(wp_login_url())
        php_exit(0)
    # end if
# end def wp_redirect_admin_locations
