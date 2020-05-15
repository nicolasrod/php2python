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
#// WordPress environment setup class.
#// 
#// @package WordPress
#// @since 2.0.0
#//
class WP():
    public_query_vars = Array("m", "p", "posts", "w", "cat", "withcomments", "withoutcomments", "s", "search", "exact", "sentence", "calendar", "page", "paged", "more", "tb", "pb", "author", "order", "orderby", "year", "monthnum", "day", "hour", "minute", "second", "name", "category_name", "tag", "feed", "author_name", "pagename", "page_id", "error", "attachment", "attachment_id", "subpost", "subpost_id", "preview", "robots", "favicon", "taxonomy", "term", "cpage", "post_type", "embed")
    private_query_vars = Array("offset", "posts_per_page", "posts_per_archive_page", "showposts", "nopaging", "post_type", "post_status", "category__in", "category__not_in", "category__and", "tag__in", "tag__not_in", "tag__and", "tag_slug__in", "tag_slug__and", "tag_id", "post_mime_type", "perm", "comments_per_page", "post__in", "post__not_in", "post_parent", "post_parent__in", "post_parent__not_in", "title", "fields")
    extra_query_vars = Array()
    query_vars = Array()
    query_string = Array()
    request = Array()
    matched_rule = Array()
    matched_query = Array()
    did_permalink = False
    #// 
    #// Add name to list of public query variables.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $qv Query variable name.
    #//
    def add_query_var(self, qv=None):
        
        if (not php_in_array(qv, self.public_query_vars)):
            self.public_query_vars[-1] = qv
        # end if
    # end def add_query_var
    #// 
    #// Removes a query variable from a list of public query variables.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $name Query variable name.
    #//
    def remove_query_var(self, name=None):
        
        self.public_query_vars = php_array_diff(self.public_query_vars, Array(name))
    # end def remove_query_var
    #// 
    #// Set the value of a query variable.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $key Query variable name.
    #// @param mixed $value Query variable value.
    #//
    def set_query_var(self, key=None, value=None):
        
        self.query_vars[key] = value
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
    def parse_request(self, extra_query_vars=""):
        global self
        global wp_rewrite
        php_check_if_defined("wp_rewrite")
        #// 
        #// Filters whether to parse the request.
        #// 
        #// @since 3.5.0
        #// 
        #// @param bool         $bool             Whether or not to parse the request. Default true.
        #// @param WP           $this             Current WordPress environment instance.
        #// @param array|string $extra_query_vars Extra passed query variables.
        #//
        if (not apply_filters("do_parse_request", True, self, extra_query_vars)):
            return
        # end if
        self.query_vars = Array()
        post_type_query_vars = Array()
        if php_is_array(extra_query_vars):
            self.extra_query_vars = extra_query_vars
        elif (not php_empty(lambda : extra_query_vars)):
            parse_str(extra_query_vars, self.extra_query_vars)
        # end if
        #// Process PATH_INFO, REQUEST_URI, and 404 for permalinks.
        #// Fetch the rewrite rules.
        rewrite = wp_rewrite.wp_rewrite_rules()
        if (not php_empty(lambda : rewrite)):
            #// If we match a rewrite rule, this will be cleared.
            error = "404"
            self.did_permalink = True
            pathinfo = PHP_SERVER["PATH_INFO"] if (php_isset(lambda : PHP_SERVER["PATH_INFO"])) else ""
            pathinfo = php_explode("?", pathinfo)
            pathinfo = php_str_replace("%", "%25", pathinfo)
            req_uri = php_explode("?", PHP_SERVER["REQUEST_URI"])
            self = PHP_SERVER["PHP_SELF"]
            home_path = php_trim(php_parse_url(home_url(), PHP_URL_PATH), "/")
            home_path_regex = php_sprintf("|^%s|i", preg_quote(home_path, "|"))
            #// 
            #// Trim path info from the end and the leading home path from the front.
            #// For path info requests, this leaves us with the requesting filename, if any.
            #// For 404 requests, this leaves us with the requested permalink.
            #//
            req_uri = php_str_replace(pathinfo, "", req_uri)
            req_uri = php_trim(req_uri, "/")
            req_uri = php_preg_replace(home_path_regex, "", req_uri)
            req_uri = php_trim(req_uri, "/")
            pathinfo = php_trim(pathinfo, "/")
            pathinfo = php_preg_replace(home_path_regex, "", pathinfo)
            pathinfo = php_trim(pathinfo, "/")
            self = php_trim(self, "/")
            self = php_preg_replace(home_path_regex, "", self)
            self = php_trim(self, "/")
            #// The requested permalink is in $pathinfo for path info requests and
            #// $req_uri for other requests.
            if (not php_empty(lambda : pathinfo)) and (not php_preg_match("|^.*" + wp_rewrite.index + "$|", pathinfo)):
                requested_path = pathinfo
            else:
                #// If the request uri is the index, blank it out so that we don't try to match it against a rule.
                if req_uri == wp_rewrite.index:
                    req_uri = ""
                # end if
                requested_path = req_uri
            # end if
            requested_file = req_uri
            self.request = requested_path
            #// Look for matches.
            request_match = requested_path
            if php_empty(lambda : request_match):
                #// An empty request could only match against ^$ regex.
                if (php_isset(lambda : rewrite["$"])):
                    self.matched_rule = "$"
                    query = rewrite["$"]
                    matches = Array("")
                # end if
            else:
                for match,query in rewrite:
                    #// If the requested file is the anchor of the match, prepend it to the path info.
                    if (not php_empty(lambda : requested_file)) and php_strpos(match, requested_file) == 0 and requested_file != requested_path:
                        request_match = requested_file + "/" + requested_path
                    # end if
                    if php_preg_match(str("#^") + str(match) + str("#"), request_match, matches) or php_preg_match(str("#^") + str(match) + str("#"), urldecode(request_match), matches):
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
                        self.matched_rule = match
                        break
                    # end if
                # end for
            # end if
            if (php_isset(lambda : self.matched_rule)):
                #// Trim the query of everything up to the '?'.
                query = php_preg_replace("!^.+\\?!", "", query)
                #// Substitute the substring matches into the query.
                query = addslashes(WP_MatchesMapRegex.apply(query, matches))
                self.matched_query = query
                #// Parse the query.
                parse_str(query, perma_query_vars)
                #// If we're processing a 404 request, clear the error var since we found something.
                if "404" == error:
                    error = None
                    PHP_REQUEST["error"] = None
                # end if
            # end if
            #// If req_uri is empty or if it is a request for ourself, unset error.
            if php_empty(lambda : requested_path) or requested_file == self or php_strpos(PHP_SERVER["PHP_SELF"], "wp-admin/") != False:
                error = None
                PHP_REQUEST["error"] = None
                if (php_isset(lambda : perma_query_vars)) and php_strpos(PHP_SERVER["PHP_SELF"], "wp-admin/") != False:
                    perma_query_vars = None
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
        for post_type,t in get_post_types(Array(), "objects"):
            if is_post_type_viewable(t) and t.query_var:
                post_type_query_vars[t.query_var] = post_type
            # end if
        # end for
        for wpvar in self.public_query_vars:
            if (php_isset(lambda : self.extra_query_vars[wpvar])):
                self.query_vars[wpvar] = self.extra_query_vars[wpvar]
            elif (php_isset(lambda : PHP_REQUEST[wpvar])) and (php_isset(lambda : PHP_POST[wpvar])) and PHP_REQUEST[wpvar] != PHP_POST[wpvar]:
                wp_die(__("A variable mismatch has been detected."), __("Sorry, you are not allowed to view this item."), 400)
            elif (php_isset(lambda : PHP_POST[wpvar])):
                self.query_vars[wpvar] = PHP_POST[wpvar]
            elif (php_isset(lambda : PHP_REQUEST[wpvar])):
                self.query_vars[wpvar] = PHP_REQUEST[wpvar]
            elif (php_isset(lambda : perma_query_vars[wpvar])):
                self.query_vars[wpvar] = perma_query_vars[wpvar]
            # end if
            if (not php_empty(lambda : self.query_vars[wpvar])):
                if (not php_is_array(self.query_vars[wpvar])):
                    self.query_vars[wpvar] = str(self.query_vars[wpvar])
                else:
                    for vkey,v in self.query_vars[wpvar]:
                        if is_scalar(v):
                            self.query_vars[wpvar][vkey] = str(v)
                        # end if
                    # end for
                # end if
                if (php_isset(lambda : post_type_query_vars[wpvar])):
                    self.query_vars["post_type"] = post_type_query_vars[wpvar]
                    self.query_vars["name"] = self.query_vars[wpvar]
                # end if
            # end if
        # end for
        #// Convert urldecoded spaces back into '+'.
        for taxonomy,t in get_taxonomies(Array(), "objects"):
            if t.query_var and (php_isset(lambda : self.query_vars[t.query_var])):
                self.query_vars[t.query_var] = php_str_replace(" ", "+", self.query_vars[t.query_var])
            # end if
        # end for
        #// Don't allow non-publicly queryable taxonomies to be queried from the front end.
        if (not is_admin()):
            for taxonomy,t in get_taxonomies(Array({"publicly_queryable": False}), "objects"):
                #// 
                #// Disallow when set to the 'taxonomy' query var.
                #// Non-publicly queryable taxonomies cannot register custom query vars. See register_taxonomy().
                #//
                if (php_isset(lambda : self.query_vars["taxonomy"])) and taxonomy == self.query_vars["taxonomy"]:
                    self.query_vars["taxonomy"] = None
                    self.query_vars["term"] = None
                # end if
            # end for
        # end if
        #// Limit publicly queried post_types to those that are 'publicly_queryable'.
        if (php_isset(lambda : self.query_vars["post_type"])):
            queryable_post_types = get_post_types(Array({"publicly_queryable": True}))
            if (not php_is_array(self.query_vars["post_type"])):
                if (not php_in_array(self.query_vars["post_type"], queryable_post_types)):
                    self.query_vars["post_type"] = None
                # end if
            else:
                self.query_vars["post_type"] = php_array_intersect(self.query_vars["post_type"], queryable_post_types)
            # end if
        # end if
        #// Resolve conflicts between posts with numeric slugs and date archive queries.
        self.query_vars = wp_resolve_numeric_slug_conflicts(self.query_vars)
        for var in self.private_query_vars:
            if (php_isset(lambda : self.extra_query_vars[var])):
                self.query_vars[var] = self.extra_query_vars[var]
            # end if
        # end for
        if (php_isset(lambda : error)):
            self.query_vars["error"] = error
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
        
        headers = Array()
        status = None
        exit_required = False
        if is_user_logged_in():
            headers = php_array_merge(headers, wp_get_nocache_headers())
        # end if
        if (not php_empty(lambda : self.query_vars["error"])):
            status = int(self.query_vars["error"])
            if 404 == status:
                if (not is_user_logged_in()):
                    headers = php_array_merge(headers, wp_get_nocache_headers())
                # end if
                headers["Content-Type"] = get_option("html_type") + "; charset=" + get_option("blog_charset")
            elif php_in_array(status, Array(403, 500, 502, 503)):
                exit_required = True
            # end if
        elif php_empty(lambda : self.query_vars["feed"]):
            headers["Content-Type"] = get_option("html_type") + "; charset=" + get_option("blog_charset")
        else:
            #// Set the correct content type for feeds.
            type = self.query_vars["feed"]
            if "feed" == self.query_vars["feed"]:
                type = get_default_feed()
            # end if
            headers["Content-Type"] = feed_content_type(type) + "; charset=" + get_option("blog_charset")
            #// We're showing a feed, so WP is indeed the only thing that last changed.
            if (not php_empty(lambda : self.query_vars["withcomments"])) or False != php_strpos(self.query_vars["feed"], "comments-") or php_empty(lambda : self.query_vars["withoutcomments"]) and (not php_empty(lambda : self.query_vars["p"])) or (not php_empty(lambda : self.query_vars["name"])) or (not php_empty(lambda : self.query_vars["page_id"])) or (not php_empty(lambda : self.query_vars["pagename"])) or (not php_empty(lambda : self.query_vars["attachment"])) or (not php_empty(lambda : self.query_vars["attachment_id"])):
                wp_last_modified = mysql2date("D, d M Y H:i:s", get_lastcommentmodified("GMT"), False)
            else:
                wp_last_modified = mysql2date("D, d M Y H:i:s", get_lastpostmodified("GMT"), False)
            # end if
            if (not wp_last_modified):
                wp_last_modified = gmdate("D, d M Y H:i:s")
            # end if
            wp_last_modified += " GMT"
            wp_etag = "\"" + php_md5(wp_last_modified) + "\""
            headers["Last-Modified"] = wp_last_modified
            headers["ETag"] = wp_etag
            #// Support for conditional GET.
            if (php_isset(lambda : PHP_SERVER["HTTP_IF_NONE_MATCH"])):
                client_etag = wp_unslash(PHP_SERVER["HTTP_IF_NONE_MATCH"])
            else:
                client_etag = False
            # end if
            client_last_modified = "" if php_empty(lambda : PHP_SERVER["HTTP_IF_MODIFIED_SINCE"]) else php_trim(PHP_SERVER["HTTP_IF_MODIFIED_SINCE"])
            #// If string is empty, return 0. If not, attempt to parse into a timestamp.
            client_modified_timestamp = strtotime(client_last_modified) if client_last_modified else 0
            #// Make a timestamp for our most recent modification..
            wp_modified_timestamp = strtotime(wp_last_modified)
            if client_modified_timestamp >= wp_modified_timestamp and client_etag == wp_etag if client_last_modified and client_etag else client_modified_timestamp >= wp_modified_timestamp or client_etag == wp_etag:
                status = 304
                exit_required = True
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
        headers = apply_filters("wp_headers", headers, self)
        if (not php_empty(lambda : status)):
            status_header(status)
        # end if
        #// If Last-Modified is set to false, it should not be sent (no-cache situation).
        if (php_isset(lambda : headers["Last-Modified"])) and False == headers["Last-Modified"]:
            headers["Last-Modified"] = None
            if (not php_headers_sent()):
                php_header_remove("Last-Modified")
            # end if
        # end if
        if (not php_headers_sent()):
            for name,field_value in headers:
                php_header(str(name) + str(": ") + str(field_value))
            # end for
        # end if
        if exit_required:
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
        for wpvar in php_array_keys(self.query_vars):
            if "" != self.query_vars[wpvar]:
                self.query_string += "" if php_strlen(self.query_string) < 1 else "&"
                if (not is_scalar(self.query_vars[wpvar])):
                    continue
                # end if
                self.query_string += wpvar + "=" + rawurlencode(self.query_vars[wpvar])
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
        global wp_query
        php_check_if_defined("wp_query")
        #// Extract updated query vars back into global namespace.
        for key,value in wp_query.query_vars:
            PHP_GLOBALS[key] = value
        # end for
        PHP_GLOBALS["query_string"] = self.query_string
        PHP_GLOBALS["posts"] = wp_query.posts
        PHP_GLOBALS["post"] = wp_query.post if (php_isset(lambda : wp_query.post)) else None
        PHP_GLOBALS["request"] = wp_query.request
        if wp_query.is_single() or wp_query.is_page():
            PHP_GLOBALS["more"] = 1
            PHP_GLOBALS["single"] = 1
        # end if
        if wp_query.is_author() and (php_isset(lambda : wp_query.post)):
            PHP_GLOBALS["authordata"] = get_userdata(wp_query.post.post_author)
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
        
        global wp_the_query
        php_check_if_defined("wp_the_query")
        self.build_query_string()
        wp_the_query.query(self.query_vars)
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
        
        global wp_query
        php_check_if_defined("wp_query")
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
        if False != apply_filters("pre_handle_404", False, wp_query):
            return
        # end if
        #// If we've already issued a 404, bail.
        if is_404():
            return
        # end if
        #// Never 404 for the admin, robots, favicon, or if we found posts.
        if is_admin() or is_robots() or is_favicon() or wp_query.posts:
            success = True
            if is_singular():
                p = False
                if type(wp_query.post).__name__ == "WP_Post":
                    p = copy.deepcopy(wp_query.post)
                # end if
                #// Only set X-Pingback for single posts that allow pings.
                if p and pings_open(p) and (not php_headers_sent()):
                    php_header("X-Pingback: " + get_bloginfo("pingback_url", "display"))
                # end if
                #// Check for paged content that exceeds the max number of pages.
                next = "<!--nextpage-->"
                if p and False != php_strpos(p.post_content, next) and (not php_empty(lambda : self.query_vars["page"])):
                    page = php_trim(self.query_vars["page"], "/")
                    success = int(page) <= php_substr_count(p.post_content, next) + 1
                # end if
            # end if
            if success:
                status_header(200)
                return
            # end if
        # end if
        #// We will 404 for paged queries, as no posts were found.
        if (not is_paged()):
            #// Don't 404 for authors without posts as long as they matched an author on this site.
            author = get_query_var("author")
            if is_author() and php_is_numeric(author) and author > 0 and is_user_member_of_blog(author):
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
        wp_query.set_404()
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
    def main(self, query_args=""):
        
        self.init()
        self.parse_request(query_args)
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
