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
#// WordPress environment setup class.
#// 
#// @package WordPress
#// @since 2.0.0
#//
class WP():
    #// 
    #// Public query variables.
    #// 
    #// Long list of public query variables.
    #// 
    #// @since 2.0.0
    #// @var string[]
    #//
    public_query_vars = Array("m", "p", "posts", "w", "cat", "withcomments", "withoutcomments", "s", "search", "exact", "sentence", "calendar", "page", "paged", "more", "tb", "pb", "author", "order", "orderby", "year", "monthnum", "day", "hour", "minute", "second", "name", "category_name", "tag", "feed", "author_name", "pagename", "page_id", "error", "attachment", "attachment_id", "subpost", "subpost_id", "preview", "robots", "favicon", "taxonomy", "term", "cpage", "post_type", "embed")
    #// 
    #// Private query variables.
    #// 
    #// Long list of private query variables.
    #// 
    #// @since 2.0.0
    #// @var string[]
    #//
    private_query_vars = Array("offset", "posts_per_page", "posts_per_archive_page", "showposts", "nopaging", "post_type", "post_status", "category__in", "category__not_in", "category__and", "tag__in", "tag__not_in", "tag__and", "tag_slug__in", "tag_slug__and", "tag_id", "post_mime_type", "perm", "comments_per_page", "post__in", "post__not_in", "post_parent", "post_parent__in", "post_parent__not_in", "title", "fields")
    #// 
    #// Extra query variables set by the user.
    #// 
    #// @since 2.1.0
    #// @var array
    #//
    extra_query_vars = Array()
    #// 
    #// Query variables for setting up the WordPress Query Loop.
    #// 
    #// @since 2.0.0
    #// @var array
    #//
    query_vars = Array()
    #// 
    #// String parsed to set the query variables.
    #// 
    #// @since 2.0.0
    #// @var string
    #//
    query_string = Array()
    #// 
    #// The request path, e.g. 2015/05/06.
    #// 
    #// @since 2.0.0
    #// @var string
    #//
    request = Array()
    #// 
    #// Rewrite rule the request matched.
    #// 
    #// @since 2.0.0
    #// @var string
    #//
    matched_rule = Array()
    #// 
    #// Rewrite query the request matched.
    #// 
    #// @since 2.0.0
    #// @var string
    #//
    matched_query = Array()
    #// 
    #// Whether already did the permalink.
    #// 
    #// @since 2.0.0
    #// @var bool
    #//
    did_permalink = False
    #// 
    #// Add name to list of public query variables.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $qv Query variable name.
    #//
    def add_query_var(self, qv_=None):
        
        
        if (not php_in_array(qv_, self.public_query_vars)):
            self.public_query_vars[-1] = qv_
        # end if
    # end def add_query_var
    #// 
    #// Removes a query variable from a list of public query variables.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $name Query variable name.
    #//
    def remove_query_var(self, name_=None):
        
        
        self.public_query_vars = php_array_diff(self.public_query_vars, Array(name_))
    # end def remove_query_var
    #// 
    #// Set the value of a query variable.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $key Query variable name.
    #// @param mixed $value Query variable value.
    #//
    def set_query_var(self, key_=None, value_=None):
        
        
        self.query_vars[key_] = value_
    # end def set_query_var
    #// 
    #// Parse request to find correct WordPress query.
    #// 
    #// Sets up the query variables based on the request. There are also many
    #// filters and actions that can be used to further manipulate the result.
    #// 
    #// @since 2.0.0
    #// 
    #// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
    #// 
    #// @param array|string $extra_query_vars Set the extra query variables.
    #//
    def parse_request(self, extra_query_vars_=""):
        
        
        global wp_rewrite_
        php_check_if_defined("wp_rewrite_")
        #// 
        #// Filters whether to parse the request.
        #// 
        #// @since 3.5.0
        #// 
        #// @param bool         $bool             Whether or not to parse the request. Default true.
        #// @param WP           $this             Current WordPress environment instance.
        #// @param array|string $extra_query_vars Extra passed query variables.
        #//
        if (not apply_filters("do_parse_request", True, self, extra_query_vars_)):
            return
        # end if
        self.query_vars = Array()
        post_type_query_vars_ = Array()
        if php_is_array(extra_query_vars_):
            self.extra_query_vars = extra_query_vars_
        elif (not php_empty(lambda : extra_query_vars_)):
            parse_str(extra_query_vars_, self.extra_query_vars)
        # end if
        #// Process PATH_INFO, REQUEST_URI, and 404 for permalinks.
        #// Fetch the rewrite rules.
        rewrite_ = wp_rewrite_.wp_rewrite_rules()
        if (not php_empty(lambda : rewrite_)):
            #// If we match a rewrite rule, this will be cleared.
            error_ = "404"
            self.did_permalink = True
            pathinfo_ = PHP_SERVER["PATH_INFO"] if (php_isset(lambda : PHP_SERVER["PATH_INFO"])) else ""
            pathinfo_ = php_explode("?", pathinfo_)
            pathinfo_ = php_str_replace("%", "%25", pathinfo_)
            req_uri_ = php_explode("?", PHP_SERVER["REQUEST_URI"])
            self_ = PHP_SERVER["PHP_SELF"]
            home_path_ = php_trim(php_parse_url(home_url(), PHP_URL_PATH), "/")
            home_path_regex_ = php_sprintf("|^%s|i", preg_quote(home_path_, "|"))
            #// 
            #// Trim path info from the end and the leading home path from the front.
            #// For path info requests, this leaves us with the requesting filename, if any.
            #// For 404 requests, this leaves us with the requested permalink.
            #//
            req_uri_ = php_str_replace(pathinfo_, "", req_uri_)
            req_uri_ = php_trim(req_uri_, "/")
            req_uri_ = php_preg_replace(home_path_regex_, "", req_uri_)
            req_uri_ = php_trim(req_uri_, "/")
            pathinfo_ = php_trim(pathinfo_, "/")
            pathinfo_ = php_preg_replace(home_path_regex_, "", pathinfo_)
            pathinfo_ = php_trim(pathinfo_, "/")
            self_ = php_trim(self_, "/")
            self_ = php_preg_replace(home_path_regex_, "", self_)
            self_ = php_trim(self_, "/")
            #// The requested permalink is in $pathinfo for path info requests and
            #// $req_uri for other requests.
            if (not php_empty(lambda : pathinfo_)) and (not php_preg_match("|^.*" + wp_rewrite_.index + "$|", pathinfo_)):
                requested_path_ = pathinfo_
            else:
                #// If the request uri is the index, blank it out so that we don't try to match it against a rule.
                if req_uri_ == wp_rewrite_.index:
                    req_uri_ = ""
                # end if
                requested_path_ = req_uri_
            # end if
            requested_file_ = req_uri_
            self.request = requested_path_
            #// Look for matches.
            request_match_ = requested_path_
            if php_empty(lambda : request_match_):
                #// An empty request could only match against ^$ regex.
                if (php_isset(lambda : rewrite_["$"])):
                    self.matched_rule = "$"
                    query_ = rewrite_["$"]
                    matches_ = Array("")
                # end if
            else:
                for match_,query_ in rewrite_.items():
                    #// If the requested file is the anchor of the match, prepend it to the path info.
                    if (not php_empty(lambda : requested_file_)) and php_strpos(match_, requested_file_) == 0 and requested_file_ != requested_path_:
                        request_match_ = requested_file_ + "/" + requested_path_
                    # end if
                    if php_preg_match(str("#^") + str(match_) + str("#"), request_match_, matches_) or php_preg_match(str("#^") + str(match_) + str("#"), urldecode(request_match_), matches_):
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
                        self.matched_rule = match_
                        break
                    # end if
                # end for
            # end if
            if (php_isset(lambda : self.matched_rule)):
                #// Trim the query of everything up to the '?'.
                query_ = php_preg_replace("!^.+\\?!", "", query_)
                #// Substitute the substring matches into the query.
                query_ = addslashes(WP_MatchesMapRegex.apply(query_, matches_))
                self.matched_query = query_
                #// Parse the query.
                parse_str(query_, perma_query_vars_)
                #// If we're processing a 404 request, clear the error var since we found something.
                if "404" == error_:
                    error_ = None
                    PHP_REQUEST["error"] = None
                # end if
            # end if
            #// If req_uri is empty or if it is a request for ourself, unset error.
            if php_empty(lambda : requested_path_) or requested_file_ == self_ or php_strpos(PHP_SERVER["PHP_SELF"], "wp-admin/") != False:
                error_ = None
                PHP_REQUEST["error"] = None
                if (php_isset(lambda : perma_query_vars_)) and php_strpos(PHP_SERVER["PHP_SELF"], "wp-admin/") != False:
                    perma_query_vars_ = None
                # end if
                self.did_permalink = False
            # end if
        # end if
        #// 
        #// Filters the query variables whitelist before processing.
        #// 
        #// Allows (publicly allowed) query vars to be added, removed, or changed prior
        #// to executing the query. Needed to allow custom rewrite rules using your own arguments
        #// to work, or any other custom query variables you want to be publicly available.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string[] $public_query_vars The array of whitelisted query variable names.
        #//
        self.public_query_vars = apply_filters("query_vars", self.public_query_vars)
        for post_type_,t_ in get_post_types(Array(), "objects").items():
            if is_post_type_viewable(t_) and t_.query_var:
                post_type_query_vars_[t_.query_var] = post_type_
            # end if
        # end for
        for wpvar_ in self.public_query_vars:
            if (php_isset(lambda : self.extra_query_vars[wpvar_])):
                self.query_vars[wpvar_] = self.extra_query_vars[wpvar_]
            elif (php_isset(lambda : PHP_REQUEST[wpvar_])) and (php_isset(lambda : PHP_POST[wpvar_])) and PHP_REQUEST[wpvar_] != PHP_POST[wpvar_]:
                wp_die(__("A variable mismatch has been detected."), __("Sorry, you are not allowed to view this item."), 400)
            elif (php_isset(lambda : PHP_POST[wpvar_])):
                self.query_vars[wpvar_] = PHP_POST[wpvar_]
            elif (php_isset(lambda : PHP_REQUEST[wpvar_])):
                self.query_vars[wpvar_] = PHP_REQUEST[wpvar_]
            elif (php_isset(lambda : perma_query_vars_[wpvar_])):
                self.query_vars[wpvar_] = perma_query_vars_[wpvar_]
            # end if
            if (not php_empty(lambda : self.query_vars[wpvar_])):
                if (not php_is_array(self.query_vars[wpvar_])):
                    self.query_vars[wpvar_] = php_str(self.query_vars[wpvar_])
                else:
                    for vkey_,v_ in self.query_vars[wpvar_].items():
                        if php_is_scalar(v_):
                            self.query_vars[wpvar_][vkey_] = php_str(v_)
                        # end if
                    # end for
                # end if
                if (php_isset(lambda : post_type_query_vars_[wpvar_])):
                    self.query_vars["post_type"] = post_type_query_vars_[wpvar_]
                    self.query_vars["name"] = self.query_vars[wpvar_]
                # end if
            # end if
        # end for
        #// Convert urldecoded spaces back into '+'.
        for taxonomy_,t_ in get_taxonomies(Array(), "objects").items():
            if t_.query_var and (php_isset(lambda : self.query_vars[t_.query_var])):
                self.query_vars[t_.query_var] = php_str_replace(" ", "+", self.query_vars[t_.query_var])
            # end if
        # end for
        #// Don't allow non-publicly queryable taxonomies to be queried from the front end.
        if (not is_admin()):
            for taxonomy_,t_ in get_taxonomies(Array({"publicly_queryable": False}), "objects").items():
                #// 
                #// Disallow when set to the 'taxonomy' query var.
                #// Non-publicly queryable taxonomies cannot register custom query vars. See register_taxonomy().
                #//
                if (php_isset(lambda : self.query_vars["taxonomy"])) and taxonomy_ == self.query_vars["taxonomy"]:
                    self.query_vars["taxonomy"] = None
                    self.query_vars["term"] = None
                # end if
            # end for
        # end if
        #// Limit publicly queried post_types to those that are 'publicly_queryable'.
        if (php_isset(lambda : self.query_vars["post_type"])):
            queryable_post_types_ = get_post_types(Array({"publicly_queryable": True}))
            if (not php_is_array(self.query_vars["post_type"])):
                if (not php_in_array(self.query_vars["post_type"], queryable_post_types_)):
                    self.query_vars["post_type"] = None
                # end if
            else:
                self.query_vars["post_type"] = php_array_intersect(self.query_vars["post_type"], queryable_post_types_)
            # end if
        # end if
        #// Resolve conflicts between posts with numeric slugs and date archive queries.
        self.query_vars = wp_resolve_numeric_slug_conflicts(self.query_vars)
        for var_ in self.private_query_vars:
            if (php_isset(lambda : self.extra_query_vars[var_])):
                self.query_vars[var_] = self.extra_query_vars[var_]
            # end if
        # end for
        if (php_isset(lambda : error_)):
            self.query_vars["error"] = error_
        # end if
        #// 
        #// Filters the array of parsed query variables.
        #// 
        #// @since 2.1.0
        #// 
        #// @param array $query_vars The array of requested query variables.
        #//
        self.query_vars = apply_filters("request", self.query_vars)
        #// 
        #// Fires once all query variables for the current request have been parsed.
        #// 
        #// @since 2.1.0
        #// 
        #// @param WP $this Current WordPress environment instance (passed by reference).
        #//
        do_action_ref_array("parse_request", Array(self))
    # end def parse_request
    #// 
    #// Sends additional HTTP headers for caching, content type, etc.
    #// 
    #// Sets the Content-Type header. Sets the 'error' status (if passed) and optionally exits.
    #// If showing a feed, it will also send Last-Modified, ETag, and 304 status if needed.
    #// 
    #// @since 2.0.0
    #// @since 4.4.0 `X-Pingback` header is added conditionally after posts have been queried in handle_404().
    #//
    def send_headers(self):
        
        
        headers_ = Array()
        status_ = None
        exit_required_ = False
        if is_user_logged_in():
            headers_ = php_array_merge(headers_, wp_get_nocache_headers())
        # end if
        if (not php_empty(lambda : self.query_vars["error"])):
            status_ = php_int(self.query_vars["error"])
            if 404 == status_:
                if (not is_user_logged_in()):
                    headers_ = php_array_merge(headers_, wp_get_nocache_headers())
                # end if
                headers_["Content-Type"] = get_option("html_type") + "; charset=" + get_option("blog_charset")
            elif php_in_array(status_, Array(403, 500, 502, 503)):
                exit_required_ = True
            # end if
        elif php_empty(lambda : self.query_vars["feed"]):
            headers_["Content-Type"] = get_option("html_type") + "; charset=" + get_option("blog_charset")
        else:
            #// Set the correct content type for feeds.
            type_ = self.query_vars["feed"]
            if "feed" == self.query_vars["feed"]:
                type_ = get_default_feed()
            # end if
            headers_["Content-Type"] = feed_content_type(type_) + "; charset=" + get_option("blog_charset")
            #// We're showing a feed, so WP is indeed the only thing that last changed.
            if (not php_empty(lambda : self.query_vars["withcomments"])) or False != php_strpos(self.query_vars["feed"], "comments-") or php_empty(lambda : self.query_vars["withoutcomments"]) and (not php_empty(lambda : self.query_vars["p"])) or (not php_empty(lambda : self.query_vars["name"])) or (not php_empty(lambda : self.query_vars["page_id"])) or (not php_empty(lambda : self.query_vars["pagename"])) or (not php_empty(lambda : self.query_vars["attachment"])) or (not php_empty(lambda : self.query_vars["attachment_id"])):
                wp_last_modified_ = mysql2date("D, d M Y H:i:s", get_lastcommentmodified("GMT"), False)
            else:
                wp_last_modified_ = mysql2date("D, d M Y H:i:s", get_lastpostmodified("GMT"), False)
            # end if
            if (not wp_last_modified_):
                wp_last_modified_ = gmdate("D, d M Y H:i:s")
            # end if
            wp_last_modified_ += " GMT"
            wp_etag_ = "\"" + php_md5(wp_last_modified_) + "\""
            headers_["Last-Modified"] = wp_last_modified_
            headers_["ETag"] = wp_etag_
            #// Support for conditional GET.
            if (php_isset(lambda : PHP_SERVER["HTTP_IF_NONE_MATCH"])):
                client_etag_ = wp_unslash(PHP_SERVER["HTTP_IF_NONE_MATCH"])
            else:
                client_etag_ = False
            # end if
            client_last_modified_ = "" if php_empty(lambda : PHP_SERVER["HTTP_IF_MODIFIED_SINCE"]) else php_trim(PHP_SERVER["HTTP_IF_MODIFIED_SINCE"])
            #// If string is empty, return 0. If not, attempt to parse into a timestamp.
            client_modified_timestamp_ = strtotime(client_last_modified_) if client_last_modified_ else 0
            #// Make a timestamp for our most recent modification..
            wp_modified_timestamp_ = strtotime(wp_last_modified_)
            if client_modified_timestamp_ >= wp_modified_timestamp_ and client_etag_ == wp_etag_ if client_last_modified_ and client_etag_ else client_modified_timestamp_ >= wp_modified_timestamp_ or client_etag_ == wp_etag_:
                status_ = 304
                exit_required_ = True
            # end if
        # end if
        #// 
        #// Filters the HTTP headers before they're sent to the browser.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $headers Associative array of headers to be sent.
        #// @param WP       $this    Current WordPress environment instance.
        #//
        headers_ = apply_filters("wp_headers", headers_, self)
        if (not php_empty(lambda : status_)):
            status_header(status_)
        # end if
        #// If Last-Modified is set to false, it should not be sent (no-cache situation).
        if (php_isset(lambda : headers_["Last-Modified"])) and False == headers_["Last-Modified"]:
            headers_["Last-Modified"] = None
            if (not php_headers_sent()):
                php_header_remove("Last-Modified")
            # end if
        # end if
        if (not php_headers_sent()):
            for name_,field_value_ in headers_.items():
                php_header(str(name_) + str(": ") + str(field_value_))
            # end for
        # end if
        if exit_required_:
            php_exit(0)
        # end if
        #// 
        #// Fires once the requested HTTP headers for caching, content type, etc. have been sent.
        #// 
        #// @since 2.1.0
        #// 
        #// @param WP $this Current WordPress environment instance (passed by reference).
        #//
        do_action_ref_array("send_headers", Array(self))
    # end def send_headers
    #// 
    #// Sets the query string property based off of the query variable property.
    #// 
    #// The {@see 'query_string'} filter is deprecated, but still works. Plugins should
    #// use the {@see 'request'} filter instead.
    #// 
    #// @since 2.0.0
    #//
    def build_query_string(self):
        
        
        self.query_string = ""
        for wpvar_ in php_array_keys(self.query_vars):
            if "" != self.query_vars[wpvar_]:
                self.query_string += "" if php_strlen(self.query_string) < 1 else "&"
                if (not php_is_scalar(self.query_vars[wpvar_])):
                    continue
                # end if
                self.query_string += wpvar_ + "=" + rawurlencode(self.query_vars[wpvar_])
            # end if
        # end for
        if has_filter("query_string"):
            #// Don't bother filtering and parsing if no plugins are hooked in.
            #// 
            #// Filters the query string before parsing.
            #// 
            #// @since 1.5.0
            #// @deprecated 2.1.0 Use {@see 'query_vars'} or {@see 'request'} filters instead.
            #// 
            #// @param string $query_string The query string to modify.
            #//
            self.query_string = apply_filters_deprecated("query_string", Array(self.query_string), "2.1.0", "query_vars, request")
            parse_str(self.query_string, self.query_vars)
        # end if
    # end def build_query_string
    #// 
    #// Set up the WordPress Globals.
    #// 
    #// The query_vars property will be extracted to the GLOBALS. So care should
    #// be taken when naming global variables that might interfere with the
    #// WordPress environment.
    #// 
    #// @since 2.0.0
    #// 
    #// @global WP_Query     $wp_query     WordPress Query object.
    #// @global string       $query_string Query string for the loop.
    #// @global array        $posts        The found posts.
    #// @global WP_Post|null $post         The current post, if available.
    #// @global string       $request      The SQL statement for the request.
    #// @global int          $more         Only set, if single page or post.
    #// @global int          $single       If single page or post. Only set, if single page or post.
    #// @global WP_User      $authordata   Only set, if author archive.
    #//
    def register_globals(self):
        
        global PHP_GLOBALS
        global wp_query_
        php_check_if_defined("wp_query_")
        #// Extract updated query vars back into global namespace.
        for key_,value_ in wp_query_.query_vars.items():
            PHP_GLOBALS[key_] = value_
        # end for
        PHP_GLOBALS["query_string"] = self.query_string
        PHP_GLOBALS["posts"] = wp_query_.posts
        PHP_GLOBALS["post"] = wp_query_.post if (php_isset(lambda : wp_query_.post)) else None
        PHP_GLOBALS["request"] = wp_query_.request
        if wp_query_.is_single() or wp_query_.is_page():
            PHP_GLOBALS["more"] = 1
            PHP_GLOBALS["single"] = 1
        # end if
        if wp_query_.is_author() and (php_isset(lambda : wp_query_.post)):
            PHP_GLOBALS["authordata"] = get_userdata(wp_query_.post.post_author)
        # end if
    # end def register_globals
    #// 
    #// Set up the current user.
    #// 
    #// @since 2.0.0
    #//
    def init(self):
        
        
        wp_get_current_user()
    # end def init
    #// 
    #// Set up the Loop based on the query variables.
    #// 
    #// @since 2.0.0
    #// 
    #// @global WP_Query $wp_the_query WordPress Query object.
    #//
    def query_posts(self):
        
        
        global wp_the_query_
        php_check_if_defined("wp_the_query_")
        self.build_query_string()
        wp_the_query_.query(self.query_vars)
    # end def query_posts
    #// 
    #// Set the Headers for 404, if nothing is found for requested URL.
    #// 
    #// Issue a 404 if a request doesn't match any posts and doesn't match
    #// any object (e.g. an existing-but-empty category, tag, author) and a 404 was not already
    #// issued, and if the request was not a search or the homepage.
    #// 
    #// Otherwise, issue a 200.
    #// 
    #// This sets headers after posts have been queried. handle_404() really means "handle status."
    #// By inspecting the result of querying posts, seemingly successful requests can be switched to
    #// a 404 so that canonical redirection logic can kick in.
    #// 
    #// @since 2.0.0
    #// 
    #// @global WP_Query $wp_query WordPress Query object.
    #//
    def handle_404(self):
        
        
        global wp_query_
        php_check_if_defined("wp_query_")
        #// 
        #// Filters whether to short-circuit default header status handling.
        #// 
        #// Returning a non-false value from the filter will short-circuit the handling
        #// and return early.
        #// 
        #// @since 4.5.0
        #// 
        #// @param bool     $preempt  Whether to short-circuit default header status handling. Default false.
        #// @param WP_Query $wp_query WordPress Query object.
        #//
        if False != apply_filters("pre_handle_404", False, wp_query_):
            return
        # end if
        #// If we've already issued a 404, bail.
        if is_404():
            return
        # end if
        #// Never 404 for the admin, robots, favicon, or if we found posts.
        if is_admin() or is_robots() or is_favicon() or wp_query_.posts:
            success_ = True
            if is_singular():
                p_ = False
                if type(wp_query_.post).__name__ == "WP_Post":
                    p_ = copy.deepcopy(wp_query_.post)
                # end if
                #// Only set X-Pingback for single posts that allow pings.
                if p_ and pings_open(p_) and (not php_headers_sent()):
                    php_header("X-Pingback: " + get_bloginfo("pingback_url", "display"))
                # end if
                #// Check for paged content that exceeds the max number of pages.
                next_ = "<!--nextpage-->"
                if p_ and False != php_strpos(p_.post_content, next_) and (not php_empty(lambda : self.query_vars["page"])):
                    page_ = php_trim(self.query_vars["page"], "/")
                    success_ = php_int(page_) <= php_substr_count(p_.post_content, next_) + 1
                # end if
            # end if
            if success_:
                status_header(200)
                return
            # end if
        # end if
        #// We will 404 for paged queries, as no posts were found.
        if (not is_paged()):
            #// Don't 404 for authors without posts as long as they matched an author on this site.
            author_ = get_query_var("author")
            if is_author() and php_is_numeric(author_) and author_ > 0 and is_user_member_of_blog(author_):
                status_header(200)
                return
            # end if
            #// Don't 404 for these queries if they matched an object.
            if is_tag() or is_category() or is_tax() or is_post_type_archive() and get_queried_object():
                status_header(200)
                return
            # end if
            #// Don't 404 for these queries either.
            if is_home() or is_search() or is_feed():
                status_header(200)
                return
            # end if
        # end if
        #// Guess it's time to 404.
        wp_query_.set_404()
        status_header(404)
        nocache_headers()
    # end def handle_404
    #// 
    #// Sets up all of the variables required by the WordPress environment.
    #// 
    #// The action {@see 'wp'} has one parameter that references the WP object. It
    #// allows for accessing the properties and methods to further manipulate the
    #// object.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string|array $query_args Passed to parse_request().
    #//
    def main(self, query_args_=""):
        
        
        self.init()
        self.parse_request(query_args_)
        self.send_headers()
        self.query_posts()
        self.handle_404()
        self.register_globals()
        #// 
        #// Fires once the WordPress environment has been set up.
        #// 
        #// @since 2.1.0
        #// 
        #// @param WP $this Current WordPress environment instance (passed by reference).
        #//
        do_action_ref_array("wp", Array(self))
    # end def main
# end class WP
