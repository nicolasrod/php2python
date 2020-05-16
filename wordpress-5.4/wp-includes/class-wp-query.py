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
#// Query API: WP_Query class
#// 
#// @package WordPress
#// @subpackage Query
#// @since 4.7.0
#// 
#// 
#// The WordPress Query class.
#// 
#// @link https://developer.wordpress.org/reference/classes/wp_query
#// 
#// @since 1.5.0
#// @since 4.5.0 Removed the `$comments_popup` property.
#//
class WP_Query():
    query = Array()
    query_vars = Array()
    tax_query = Array()
    meta_query = False
    date_query = False
    queried_object = Array()
    queried_object_id = Array()
    request = Array()
    posts = Array()
    post_count = 0
    current_post = -1
    in_the_loop = False
    post = Array()
    comments = Array()
    comment_count = 0
    current_comment = -1
    comment = Array()
    found_posts = 0
    max_num_pages = 0
    max_num_comment_pages = 0
    is_single = False
    is_preview = False
    is_page = False
    is_archive = False
    is_date = False
    is_year = False
    is_month = False
    is_day = False
    is_time = False
    is_author = False
    is_category = False
    is_tag = False
    is_tax = False
    is_search = False
    is_feed = False
    is_comment_feed = False
    is_trackback = False
    is_home = False
    is_privacy_policy = False
    is_404 = False
    is_embed = False
    is_paged = False
    is_admin = False
    is_attachment = False
    is_singular = False
    is_robots = False
    is_favicon = False
    is_posts_page = False
    is_post_type_archive = False
    query_vars_hash = False
    query_vars_changed = True
    thumbnails_cached = False
    stopwords = Array()
    compat_fields = Array("query_vars_hash", "query_vars_changed")
    compat_methods = Array("init_query_flags", "parse_tax_query")
    #// 
    #// Resets query flags to false.
    #// 
    #// The query flags are what page info WordPress was able to figure out.
    #// 
    #// @since 2.0.0
    #//
    def init_query_flags(self):
        
        self.is_single = False
        self.is_preview = False
        self.is_page = False
        self.is_archive = False
        self.is_date = False
        self.is_year = False
        self.is_month = False
        self.is_day = False
        self.is_time = False
        self.is_author = False
        self.is_category = False
        self.is_tag = False
        self.is_tax = False
        self.is_search = False
        self.is_feed = False
        self.is_comment_feed = False
        self.is_trackback = False
        self.is_home = False
        self.is_privacy_policy = False
        self.is_404 = False
        self.is_paged = False
        self.is_admin = False
        self.is_attachment = False
        self.is_singular = False
        self.is_robots = False
        self.is_favicon = False
        self.is_posts_page = False
        self.is_post_type_archive = False
    # end def init_query_flags
    #// 
    #// Initiates object properties and sets default values.
    #// 
    #// @since 1.5.0
    #//
    def init(self):
        
        self.posts = None
        self.query = None
        self.query_vars = Array()
        self.queried_object = None
        self.queried_object_id = None
        self.post_count = 0
        self.current_post = -1
        self.in_the_loop = False
        self.request = None
        self.post = None
        self.comments = None
        self.comment = None
        self.comment_count = 0
        self.current_comment = -1
        self.found_posts = 0
        self.max_num_pages = 0
        self.max_num_comment_pages = 0
        self.init_query_flags()
    # end def init
    #// 
    #// Reparse the query vars.
    #// 
    #// @since 1.5.0
    #//
    def parse_query_vars(self):
        
        self.parse_query()
    # end def parse_query_vars
    #// 
    #// Fills in the query variables, which do not exist within the parameter.
    #// 
    #// @since 2.1.0
    #// @since 4.5.0 Removed the `comments_popup` public query variable.
    #// 
    #// @param array $array Defined query variables.
    #// @return array Complete query variables with undefined ones filled in empty.
    #//
    def fill_query_vars(self, array=None):
        
        keys = Array("error", "m", "p", "post_parent", "subpost", "subpost_id", "attachment", "attachment_id", "name", "pagename", "page_id", "second", "minute", "hour", "day", "monthnum", "year", "w", "category_name", "tag", "cat", "tag_id", "author", "author_name", "feed", "tb", "paged", "meta_key", "meta_value", "preview", "s", "sentence", "title", "fields", "menu_order", "embed")
        for key in keys:
            if (not (php_isset(lambda : array[key]))):
                array[key] = ""
            # end if
        # end for
        array_keys = Array("category__in", "category__not_in", "category__and", "post__in", "post__not_in", "post_name__in", "tag__in", "tag__not_in", "tag__and", "tag_slug__in", "tag_slug__and", "post_parent__in", "post_parent__not_in", "author__in", "author__not_in")
        for key in array_keys:
            if (not (php_isset(lambda : array[key]))):
                array[key] = Array()
            # end if
        # end for
        return array
    # end def fill_query_vars
    #// 
    #// Parse a query string and set query type booleans.
    #// 
    #// @since 1.5.0
    #// @since 4.2.0 Introduced the ability to order by specific clauses of a `$meta_query`, by passing the clause's
    #// array key to `$orderby`.
    #// @since 4.4.0 Introduced `$post_name__in` and `$title` parameters. `$s` was updated to support excluded
    #// search terms, by prepending a hyphen.
    #// @since 4.5.0 Removed the `$comments_popup` parameter.
    #// Introduced the `$comment_status` and `$ping_status` parameters.
    #// Introduced `RAND(x)` syntax for `$orderby`, which allows an integer seed value to random sorts.
    #// @since 4.6.0 Added 'post_name__in' support for `$orderby`. Introduced the `$lazy_load_term_meta` argument.
    #// @since 4.9.0 Introduced the `$comment_count` parameter.
    #// @since 5.1.0 Introduced the `$meta_compare_key` parameter.
    #// @since 5.3.0 Introduced the `$meta_type_key` parameter.
    #// 
    #// @param string|array $query {
    #// Optional. Array or string of Query parameters.
    #// 
    #// @type int          $attachment_id           Attachment post ID. Used for 'attachment' post_type.
    #// @type int|string   $author                  Author ID, or comma-separated list of IDs.
    #// @type string       $author_name             User 'user_nicename'.
    #// @type array        $author__in              An array of author IDs to query from.
    #// @type array        $author__not_in          An array of author IDs not to query from.
    #// @type bool         $cache_results           Whether to cache post information. Default true.
    #// @type int|string   $cat                     Category ID or comma-separated list of IDs (this or any children).
    #// @type array        $category__and           An array of category IDs (AND in).
    #// @type array        $category__in            An array of category IDs (OR in, no children).
    #// @type array        $category__not_in        An array of category IDs (NOT in).
    #// @type string       $category_name           Use category slug (not name, this or any children).
    #// @type array|int    $comment_count           Filter results by comment count. Provide an integer to match
    #// comment count exactly. Provide an array with integer 'value'
    #// and 'compare' operator ('=', '!=', '>', '>=', '<', '<=' ) to
    #// compare against comment_count in a specific way.
    #// @type string       $comment_status          Comment status.
    #// @type int          $comments_per_page       The number of comments to return per page.
    #// Default 'comments_per_page' option.
    #// @type array        $date_query              An associative array of WP_Date_Query arguments.
    #// See WP_Date_Query::__construct().
    #// @type int          $day                     Day of the month. Default empty. Accepts numbers 1-31.
    #// @type bool         $exact                   Whether to search by exact keyword. Default false.
    #// @type string|array $fields                  Which fields to return. Single field or all fields (string),
    #// or array of fields. 'id=>parent' uses 'id' and 'post_parent'.
    #// Default all fields. Accepts 'ids', 'id=>parent'.
    #// @type int          $hour                    Hour of the day. Default empty. Accepts numbers 0-23.
    #// @type int|bool     $ignore_sticky_posts     Whether to ignore sticky posts or not. Setting this to false
    #// excludes stickies from 'post__in'. Accepts 1|true, 0|false.
    #// Default 0|false.
    #// @type int          $m                       Combination YearMonth. Accepts any four-digit year and month
    #// numbers 1-12. Default empty.
    #// @type string       $meta_compare            Comparison operator to test the 'meta_value'.
    #// @type string       $meta_compare_key        Comparison operator to test the 'meta_key'.
    #// @type string       $meta_key                Custom field key.
    #// @type array        $meta_query              An associative array of WP_Meta_Query arguments. See WP_Meta_Query.
    #// @type string       $meta_value              Custom field value.
    #// @type int          $meta_value_num          Custom field value number.
    #// @type string       $meta_type_key           Cast for 'meta_key'. See WP_Meta_Query::construct().
    #// @type int          $menu_order              The menu order of the posts.
    #// @type int          $monthnum                The two-digit month. Default empty. Accepts numbers 1-12.
    #// @type string       $name                    Post slug.
    #// @type bool         $nopaging                Show all posts (true) or paginate (false). Default false.
    #// @type bool         $no_found_rows           Whether to skip counting the total rows found. Enabling can improve
    #// performance. Default false.
    #// @type int          $offset                  The number of posts to offset before retrieval.
    #// @type string       $order                   Designates ascending or descending order of posts. Default 'DESC'.
    #// Accepts 'ASC', 'DESC'.
    #// @type string|array $orderby                 Sort retrieved posts by parameter. One or more options may be
    #// passed. To use 'meta_value', or 'meta_value_num',
    #// 'meta_key=keyname' must be also be defined. To sort by a
    #// specific `$meta_query` clause, use that clause's array key.
    #// Accepts 'none', 'name', 'author', 'date', 'title',
    #// 'modified', 'menu_order', 'parent', 'ID', 'rand',
    #// 'relevance', 'RAND(x)' (where 'x' is an integer seed value),
    #// 'comment_count', 'meta_value', 'meta_value_num', 'post__in',
    #// 'post_name__in', 'post_parent__in', and the array keys
    #// of `$meta_query`. Default is 'date', except when a search
    #// is being performed, when the default is 'relevance'.
    #// 
    #// @type int          $p                       Post ID.
    #// @type int          $page                    Show the number of posts that would show up on page X of a
    #// static front page.
    #// @type int          $paged                   The number of the current page.
    #// @type int          $page_id                 Page ID.
    #// @type string       $pagename                Page slug.
    #// @type string       $perm                    Show posts if user has the appropriate capability.
    #// @type string       $ping_status             Ping status.
    #// @type array        $post__in                An array of post IDs to retrieve, sticky posts will be included.
    #// @type array        $post__not_in            An array of post IDs not to retrieve. Note: a string of comma-
    #// separated IDs will NOT work.
    #// @type string       $post_mime_type          The mime type of the post. Used for 'attachment' post_type.
    #// @type array        $post_name__in           An array of post slugs that results must match.
    #// @type int          $post_parent             Page ID to retrieve child pages for. Use 0 to only retrieve
    #// top-level pages.
    #// @type array        $post_parent__in         An array containing parent page IDs to query child pages from.
    #// @type array        $post_parent__not_in     An array containing parent page IDs not to query child pages from.
    #// @type string|array $post_type               A post type slug (string) or array of post type slugs.
    #// Default 'any' if using 'tax_query'.
    #// @type string|array $post_status             A post status (string) or array of post statuses.
    #// @type int          $posts_per_page          The number of posts to query for. Use -1 to request all posts.
    #// @type int          $posts_per_archive_page  The number of posts to query for by archive page. Overrides
    #// 'posts_per_page' when is_archive(), or is_search() are true.
    #// @type string       $s                       Search keyword(s). Prepending a term with a hyphen will
    #// exclude posts matching that term. Eg, 'pillow -sofa' will
    #// return posts containing 'pillow' but not 'sofa'. The
    #// character used for exclusion can be modified using the
    #// the 'wp_query_search_exclusion_prefix' filter.
    #// @type int          $second                  Second of the minute. Default empty. Accepts numbers 0-60.
    #// @type bool         $sentence                Whether to search by phrase. Default false.
    #// @type bool         $suppress_filters        Whether to suppress filters. Default false.
    #// @type string       $tag                     Tag slug. Comma-separated (either), Plus-separated (all).
    #// @type array        $tag__and                An array of tag ids (AND in).
    #// @type array        $tag__in                 An array of tag ids (OR in).
    #// @type array        $tag__not_in             An array of tag ids (NOT in).
    #// @type int          $tag_id                  Tag id or comma-separated list of IDs.
    #// @type array        $tag_slug__and           An array of tag slugs (AND in).
    #// @type array        $tag_slug__in            An array of tag slugs (OR in). unless 'ignore_sticky_posts' is
    #// true. Note: a string of comma-separated IDs will NOT work.
    #// @type array        $tax_query               An associative array of WP_Tax_Query arguments.
    #// See WP_Tax_Query->queries.
    #// @type string       $title                   Post title.
    #// @type bool         $update_post_meta_cache  Whether to update the post meta cache. Default true.
    #// @type bool         $update_post_term_cache  Whether to update the post term cache. Default true.
    #// @type bool         $lazy_load_term_meta     Whether to lazy-load term meta. Setting to false will
    #// disable cache priming for term meta, so that each
    #// get_term_meta() call will hit the database.
    #// Defaults to the value of `$update_post_term_cache`.
    #// @type int          $w                       The week number of the year. Default empty. Accepts numbers 0-53.
    #// @type int          $year                    The four-digit year. Default empty. Accepts any four-digit year.
    #// }
    #//
    def parse_query(self, query=""):
        
        if (not php_empty(lambda : query)):
            self.init()
            self.query = wp_parse_args(query)
            self.query_vars = self.query
        elif (not (php_isset(lambda : self.query))):
            self.query = self.query_vars
        # end if
        self.query_vars = self.fill_query_vars(self.query_vars)
        qv = self.query_vars
        self.query_vars_changed = True
        if (not php_empty(lambda : qv["robots"])):
            self.is_robots = True
        elif (not php_empty(lambda : qv["favicon"])):
            self.is_favicon = True
        # end if
        if (not is_scalar(qv["p"])) or qv["p"] < 0:
            qv["p"] = 0
            qv["error"] = "404"
        else:
            qv["p"] = php_intval(qv["p"])
        # end if
        qv["page_id"] = absint(qv["page_id"])
        qv["year"] = absint(qv["year"])
        qv["monthnum"] = absint(qv["monthnum"])
        qv["day"] = absint(qv["day"])
        qv["w"] = absint(qv["w"])
        qv["m"] = php_preg_replace("|[^0-9]|", "", qv["m"]) if is_scalar(qv["m"]) else ""
        qv["paged"] = absint(qv["paged"])
        qv["cat"] = php_preg_replace("|[^0-9,-]|", "", qv["cat"])
        #// Comma-separated list of positive or negative integers.
        qv["author"] = php_preg_replace("|[^0-9,-]|", "", qv["author"])
        #// Comma-separated list of positive or negative integers.
        qv["pagename"] = php_trim(qv["pagename"])
        qv["name"] = php_trim(qv["name"])
        qv["title"] = php_trim(qv["title"])
        if "" != qv["hour"]:
            qv["hour"] = absint(qv["hour"])
        # end if
        if "" != qv["minute"]:
            qv["minute"] = absint(qv["minute"])
        # end if
        if "" != qv["second"]:
            qv["second"] = absint(qv["second"])
        # end if
        if "" != qv["menu_order"]:
            qv["menu_order"] = absint(qv["menu_order"])
        # end if
        #// Fairly insane upper bound for search string lengths.
        if (not is_scalar(qv["s"])) or (not php_empty(lambda : qv["s"])) and php_strlen(qv["s"]) > 1600:
            qv["s"] = ""
        # end if
        #// Compat. Map subpost to attachment.
        if "" != qv["subpost"]:
            qv["attachment"] = qv["subpost"]
        # end if
        if "" != qv["subpost_id"]:
            qv["attachment_id"] = qv["subpost_id"]
        # end if
        qv["attachment_id"] = absint(qv["attachment_id"])
        if "" != qv["attachment"] or (not php_empty(lambda : qv["attachment_id"])):
            self.is_single = True
            self.is_attachment = True
        elif "" != qv["name"]:
            self.is_single = True
        elif qv["p"]:
            self.is_single = True
        elif "" != qv["hour"] and "" != qv["minute"] and "" != qv["second"] and "" != qv["year"] and "" != qv["monthnum"] and "" != qv["day"]:
            #// If year, month, day, hour, minute, and second are set,
            #// a single post is being queried.
            self.is_single = True
        elif "" != qv["pagename"] or (not php_empty(lambda : qv["page_id"])):
            self.is_page = True
            self.is_single = False
        else:
            #// Look for archive queries. Dates, categories, authors, search, post type archives.
            if (php_isset(lambda : self.query["s"])):
                self.is_search = True
            # end if
            if "" != qv["second"]:
                self.is_time = True
                self.is_date = True
            # end if
            if "" != qv["minute"]:
                self.is_time = True
                self.is_date = True
            # end if
            if "" != qv["hour"]:
                self.is_time = True
                self.is_date = True
            # end if
            if qv["day"]:
                if (not self.is_date):
                    date = php_sprintf("%04d-%02d-%02d", qv["year"], qv["monthnum"], qv["day"])
                    if qv["monthnum"] and qv["year"] and (not wp_checkdate(qv["monthnum"], qv["day"], qv["year"], date)):
                        qv["error"] = "404"
                    else:
                        self.is_day = True
                        self.is_date = True
                    # end if
                # end if
            # end if
            if qv["monthnum"]:
                if (not self.is_date):
                    if 12 < qv["monthnum"]:
                        qv["error"] = "404"
                    else:
                        self.is_month = True
                        self.is_date = True
                    # end if
                # end if
            # end if
            if qv["year"]:
                if (not self.is_date):
                    self.is_year = True
                    self.is_date = True
                # end if
            # end if
            if qv["m"]:
                self.is_date = True
                if php_strlen(qv["m"]) > 9:
                    self.is_time = True
                elif php_strlen(qv["m"]) > 7:
                    self.is_day = True
                elif php_strlen(qv["m"]) > 5:
                    self.is_month = True
                else:
                    self.is_year = True
                # end if
            # end if
            if "" != qv["w"]:
                self.is_date = True
            # end if
            self.query_vars_hash = False
            self.parse_tax_query(qv)
            for tax_query in self.tax_query.queries:
                if (not php_is_array(tax_query)):
                    continue
                # end if
                if (php_isset(lambda : tax_query["operator"])) and "NOT IN" != tax_query["operator"]:
                    for case in Switch(tax_query["taxonomy"]):
                        if case("category"):
                            self.is_category = True
                            break
                        # end if
                        if case("post_tag"):
                            self.is_tag = True
                            break
                        # end if
                        if case():
                            self.is_tax = True
                        # end if
                    # end for
                # end if
            # end for
            tax_query = None
            if php_empty(lambda : qv["author"]) or "0" == qv["author"]:
                self.is_author = False
            else:
                self.is_author = True
            # end if
            if "" != qv["author_name"]:
                self.is_author = True
            # end if
            if (not php_empty(lambda : qv["post_type"])) and (not php_is_array(qv["post_type"])):
                post_type_obj = get_post_type_object(qv["post_type"])
                if (not php_empty(lambda : post_type_obj.has_archive)):
                    self.is_post_type_archive = True
                # end if
            # end if
            if self.is_post_type_archive or self.is_date or self.is_author or self.is_category or self.is_tag or self.is_tax:
                self.is_archive = True
            # end if
        # end if
        if "" != qv["feed"]:
            self.is_feed = True
        # end if
        if "" != qv["embed"]:
            self.is_embed = True
        # end if
        if "" != qv["tb"]:
            self.is_trackback = True
        # end if
        if "" != qv["paged"] and php_intval(qv["paged"]) > 1:
            self.is_paged = True
        # end if
        #// If we're previewing inside the write screen.
        if "" != qv["preview"]:
            self.is_preview = True
        # end if
        if is_admin():
            self.is_admin = True
        # end if
        if False != php_strpos(qv["feed"], "comments-"):
            qv["feed"] = php_str_replace("comments-", "", qv["feed"])
            qv["withcomments"] = 1
        # end if
        self.is_singular = self.is_single or self.is_page or self.is_attachment
        if self.is_feed and (not php_empty(lambda : qv["withcomments"])) or php_empty(lambda : qv["withoutcomments"]) and self.is_singular:
            self.is_comment_feed = True
        # end if
        if (not self.is_singular or self.is_archive or self.is_search or self.is_feed or php_defined("REST_REQUEST") and REST_REQUEST or self.is_trackback or self.is_404 or self.is_admin or self.is_robots or self.is_favicon):
            self.is_home = True
        # end if
        #// Correct `is_*` for 'page_on_front' and 'page_for_posts'.
        if self.is_home and "page" == get_option("show_on_front") and get_option("page_on_front"):
            _query = wp_parse_args(self.query)
            #// 'pagename' can be set and empty depending on matched rewrite rules. Ignore an empty 'pagename'.
            if (php_isset(lambda : _query["pagename"])) and "" == _query["pagename"]:
                _query["pagename"] = None
            # end if
            _query["embed"] = None
            if php_empty(lambda : _query) or (not php_array_diff(php_array_keys(_query), Array("preview", "page", "paged", "cpage"))):
                self.is_page = True
                self.is_home = False
                qv["page_id"] = get_option("page_on_front")
                #// Correct <!--nextpage--> for 'page_on_front'.
                if (not php_empty(lambda : qv["paged"])):
                    qv["page"] = qv["paged"]
                    qv["paged"] = None
                # end if
            # end if
        # end if
        if "" != qv["pagename"]:
            self.queried_object = get_page_by_path(qv["pagename"])
            if self.queried_object and "attachment" == self.queried_object.post_type:
                if php_preg_match("/^[^%]*%(?:postname)%/", get_option("permalink_structure")):
                    #// See if we also have a post with the same slug.
                    post = get_page_by_path(qv["pagename"], OBJECT, "post")
                    if post:
                        self.queried_object = post
                        self.is_page = False
                        self.is_single = True
                    # end if
                # end if
            # end if
            if (not php_empty(lambda : self.queried_object)):
                self.queried_object_id = php_int(self.queried_object.ID)
            else:
                self.queried_object = None
            # end if
            if "page" == get_option("show_on_front") and (php_isset(lambda : self.queried_object_id)) and get_option("page_for_posts") == self.queried_object_id:
                self.is_page = False
                self.is_home = True
                self.is_posts_page = True
            # end if
            if (php_isset(lambda : self.queried_object_id)) and get_option("wp_page_for_privacy_policy") == self.queried_object_id:
                self.is_privacy_policy = True
            # end if
        # end if
        if qv["page_id"]:
            if "page" == get_option("show_on_front") and get_option("page_for_posts") == qv["page_id"]:
                self.is_page = False
                self.is_home = True
                self.is_posts_page = True
            # end if
            if get_option("wp_page_for_privacy_policy") == qv["page_id"]:
                self.is_privacy_policy = True
            # end if
        # end if
        if (not php_empty(lambda : qv["post_type"])):
            if php_is_array(qv["post_type"]):
                qv["post_type"] = php_array_map("sanitize_key", qv["post_type"])
            else:
                qv["post_type"] = sanitize_key(qv["post_type"])
            # end if
        # end if
        if (not php_empty(lambda : qv["post_status"])):
            if php_is_array(qv["post_status"]):
                qv["post_status"] = php_array_map("sanitize_key", qv["post_status"])
            else:
                qv["post_status"] = php_preg_replace("|[^a-z0-9_,-]|", "", qv["post_status"])
            # end if
        # end if
        if self.is_posts_page and (not (php_isset(lambda : qv["withcomments"]))) or (not qv["withcomments"]):
            self.is_comment_feed = False
        # end if
        self.is_singular = self.is_single or self.is_page or self.is_attachment
        #// Done correcting `is_*` for 'page_on_front' and 'page_for_posts'.
        if "404" == qv["error"]:
            self.set_404()
        # end if
        self.is_embed = self.is_embed and self.is_singular or self.is_404
        self.query_vars_hash = php_md5(serialize(self.query_vars))
        self.query_vars_changed = False
        #// 
        #// Fires after the main query vars have been parsed.
        #// 
        #// @since 1.5.0
        #// 
        #// @param WP_Query $this The WP_Query instance (passed by reference).
        #//
        do_action_ref_array("parse_query", Array(self))
    # end def parse_query
    #// 
    #// Parses various taxonomy related query vars.
    #// 
    #// For BC, this method is not marked as protected. See [28987].
    #// 
    #// @since 3.1.0
    #// 
    #// @param array $q The query variables. Passed by reference.
    #//
    def parse_tax_query(self, q=None):
        
        if (not php_empty(lambda : q["tax_query"])) and php_is_array(q["tax_query"]):
            tax_query = q["tax_query"]
        else:
            tax_query = Array()
        # end if
        if (not php_empty(lambda : q["taxonomy"])) and (not php_empty(lambda : q["term"])):
            tax_query[-1] = Array({"taxonomy": q["taxonomy"], "terms": Array(q["term"]), "field": "slug"})
        # end if
        for taxonomy,t in get_taxonomies(Array(), "objects"):
            if "post_tag" == taxonomy:
                continue
                pass
            # end if
            if t.query_var and (not php_empty(lambda : q[t.query_var])):
                tax_query_defaults = Array({"taxonomy": taxonomy, "field": "slug"})
                if (php_isset(lambda : t.rewrite["hierarchical"])) and t.rewrite["hierarchical"]:
                    q[t.query_var] = wp_basename(q[t.query_var])
                # end if
                term = q[t.query_var]
                if php_is_array(term):
                    term = php_implode(",", term)
                # end if
                if php_strpos(term, "+") != False:
                    terms = php_preg_split("/[+]+/", term)
                    for term in terms:
                        tax_query[-1] = php_array_merge(tax_query_defaults, Array({"terms": Array(term)}))
                    # end for
                else:
                    tax_query[-1] = php_array_merge(tax_query_defaults, Array({"terms": php_preg_split("/[,]+/", term)}))
                # end if
            # end if
        # end for
        #// If query string 'cat' is an array, implode it.
        if php_is_array(q["cat"]):
            q["cat"] = php_implode(",", q["cat"])
        # end if
        #// Category stuff.
        if (not php_empty(lambda : q["cat"])) and (not self.is_singular):
            cat_in = Array()
            cat_not_in = Array()
            cat_array = php_preg_split("/[,\\s]+/", urldecode(q["cat"]))
            cat_array = php_array_map("intval", cat_array)
            q["cat"] = php_implode(",", cat_array)
            for cat in cat_array:
                if cat > 0:
                    cat_in[-1] = cat
                elif cat < 0:
                    cat_not_in[-1] = abs(cat)
                # end if
            # end for
            if (not php_empty(lambda : cat_in)):
                tax_query[-1] = Array({"taxonomy": "category", "terms": cat_in, "field": "term_id", "include_children": True})
            # end if
            if (not php_empty(lambda : cat_not_in)):
                tax_query[-1] = Array({"taxonomy": "category", "terms": cat_not_in, "field": "term_id", "operator": "NOT IN", "include_children": True})
            # end if
            cat_array = None
            cat_in = None
            cat_not_in = None
        # end if
        if (not php_empty(lambda : q["category__and"])) and 1 == php_count(q["category__and"]):
            q["category__and"] = q["category__and"]
            if (not (php_isset(lambda : q["category__in"]))):
                q["category__in"] = Array()
            # end if
            q["category__in"][-1] = absint(reset(q["category__and"]))
            q["category__and"] = None
        # end if
        if (not php_empty(lambda : q["category__in"])):
            q["category__in"] = php_array_map("absint", array_unique(q["category__in"]))
            tax_query[-1] = Array({"taxonomy": "category", "terms": q["category__in"], "field": "term_id", "include_children": False})
        # end if
        if (not php_empty(lambda : q["category__not_in"])):
            q["category__not_in"] = php_array_map("absint", array_unique(q["category__not_in"]))
            tax_query[-1] = Array({"taxonomy": "category", "terms": q["category__not_in"], "operator": "NOT IN", "include_children": False})
        # end if
        if (not php_empty(lambda : q["category__and"])):
            q["category__and"] = php_array_map("absint", array_unique(q["category__and"]))
            tax_query[-1] = Array({"taxonomy": "category", "terms": q["category__and"], "field": "term_id", "operator": "AND", "include_children": False})
        # end if
        #// If query string 'tag' is array, implode it.
        if php_is_array(q["tag"]):
            q["tag"] = php_implode(",", q["tag"])
        # end if
        #// Tag stuff.
        if "" != q["tag"] and (not self.is_singular) and self.query_vars_changed:
            if php_strpos(q["tag"], ",") != False:
                tags = php_preg_split("/[,\\r\\n\\t ]+/", q["tag"])
                for tag in tags:
                    tag = sanitize_term_field("slug", tag, 0, "post_tag", "db")
                    q["tag_slug__in"][-1] = tag
                # end for
            elif php_preg_match("/[+\\r\\n\\t ]+/", q["tag"]) or (not php_empty(lambda : q["cat"])):
                tags = php_preg_split("/[+\\r\\n\\t ]+/", q["tag"])
                for tag in tags:
                    tag = sanitize_term_field("slug", tag, 0, "post_tag", "db")
                    q["tag_slug__and"][-1] = tag
                # end for
            else:
                q["tag"] = sanitize_term_field("slug", q["tag"], 0, "post_tag", "db")
                q["tag_slug__in"][-1] = q["tag"]
            # end if
        # end if
        if (not php_empty(lambda : q["tag_id"])):
            q["tag_id"] = absint(q["tag_id"])
            tax_query[-1] = Array({"taxonomy": "post_tag", "terms": q["tag_id"]})
        # end if
        if (not php_empty(lambda : q["tag__in"])):
            q["tag__in"] = php_array_map("absint", array_unique(q["tag__in"]))
            tax_query[-1] = Array({"taxonomy": "post_tag", "terms": q["tag__in"]})
        # end if
        if (not php_empty(lambda : q["tag__not_in"])):
            q["tag__not_in"] = php_array_map("absint", array_unique(q["tag__not_in"]))
            tax_query[-1] = Array({"taxonomy": "post_tag", "terms": q["tag__not_in"], "operator": "NOT IN"})
        # end if
        if (not php_empty(lambda : q["tag__and"])):
            q["tag__and"] = php_array_map("absint", array_unique(q["tag__and"]))
            tax_query[-1] = Array({"taxonomy": "post_tag", "terms": q["tag__and"], "operator": "AND"})
        # end if
        if (not php_empty(lambda : q["tag_slug__in"])):
            q["tag_slug__in"] = php_array_map("sanitize_title_for_query", array_unique(q["tag_slug__in"]))
            tax_query[-1] = Array({"taxonomy": "post_tag", "terms": q["tag_slug__in"], "field": "slug"})
        # end if
        if (not php_empty(lambda : q["tag_slug__and"])):
            q["tag_slug__and"] = php_array_map("sanitize_title_for_query", array_unique(q["tag_slug__and"]))
            tax_query[-1] = Array({"taxonomy": "post_tag", "terms": q["tag_slug__and"], "field": "slug", "operator": "AND"})
        # end if
        self.tax_query = php_new_class("WP_Tax_Query", lambda : WP_Tax_Query(tax_query))
        #// 
        #// Fires after taxonomy-related query vars have been parsed.
        #// 
        #// @since 3.7.0
        #// 
        #// @param WP_Query $this The WP_Query instance.
        #//
        do_action("parse_tax_query", self)
    # end def parse_tax_query
    #// 
    #// Generates SQL for the WHERE clause based on passed search terms.
    #// 
    #// @since 3.7.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param array $q Query variables.
    #// @return string WHERE clause.
    #//
    def parse_search(self, q=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        search = ""
        #// Added slashes screw with quote grouping when done early, so done later.
        q["s"] = stripslashes(q["s"])
        if php_empty(lambda : PHP_REQUEST["s"]) and self.is_main_query():
            q["s"] = urldecode(q["s"])
        # end if
        #// There are no line breaks in <input /> fields.
        q["s"] = php_str_replace(Array("\r", "\n"), "", q["s"])
        q["search_terms_count"] = 1
        if (not php_empty(lambda : q["sentence"])):
            q["search_terms"] = Array(q["s"])
        else:
            if preg_match_all("/\".*?(\"|$)|((?<=[\\t \",+])|^)[^\\t \",+]+/", q["s"], matches):
                q["search_terms_count"] = php_count(matches[0])
                q["search_terms"] = self.parse_search_terms(matches[0])
                #// If the search string has only short terms or stopwords, or is 10+ terms long, match it as sentence.
                if php_empty(lambda : q["search_terms"]) or php_count(q["search_terms"]) > 9:
                    q["search_terms"] = Array(q["s"])
                # end if
            else:
                q["search_terms"] = Array(q["s"])
            # end if
        # end if
        n = "" if (not php_empty(lambda : q["exact"])) else "%"
        searchand = ""
        q["search_orderby_title"] = Array()
        #// 
        #// Filters the prefix that indicates that a search term should be excluded from results.
        #// 
        #// @since 4.7.0
        #// 
        #// @param string $exclusion_prefix The prefix. Default '-'. Returning
        #// an empty value disables exclusions.
        #//
        exclusion_prefix = apply_filters("wp_query_search_exclusion_prefix", "-")
        for term in q["search_terms"]:
            #// If there is an $exclusion_prefix, terms prefixed with it should be excluded.
            exclude = exclusion_prefix and php_substr(term, 0, 1) == exclusion_prefix
            if exclude:
                like_op = "NOT LIKE"
                andor_op = "AND"
                term = php_substr(term, 1)
            else:
                like_op = "LIKE"
                andor_op = "OR"
            # end if
            if n and (not exclude):
                like = "%" + wpdb.esc_like(term) + "%"
                q["search_orderby_title"][-1] = wpdb.prepare(str(wpdb.posts) + str(".post_title LIKE %s"), like)
            # end if
            like = n + wpdb.esc_like(term) + n
            search += wpdb.prepare(str(searchand) + str("((") + str(wpdb.posts) + str(".post_title ") + str(like_op) + str(" %s) ") + str(andor_op) + str(" (") + str(wpdb.posts) + str(".post_excerpt ") + str(like_op) + str(" %s) ") + str(andor_op) + str(" (") + str(wpdb.posts) + str(".post_content ") + str(like_op) + str(" %s))"), like, like, like)
            searchand = " AND "
        # end for
        if (not php_empty(lambda : search)):
            search = str(" AND (") + str(search) + str(") ")
            if (not is_user_logged_in()):
                search += str(" AND (") + str(wpdb.posts) + str(".post_password = '') ")
            # end if
        # end if
        return search
    # end def parse_search
    #// 
    #// Check if the terms are suitable for searching.
    #// 
    #// Uses an array of stopwords (terms) that are excluded from the separate
    #// term matching when searching for posts. The list of English stopwords is
    #// the approximate search engines list, and is translatable.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string[] $terms Array of terms to check.
    #// @return string[] Terms that are not stopwords.
    #//
    def parse_search_terms(self, terms=None):
        
        strtolower = "mb_strtolower" if php_function_exists("mb_strtolower") else "strtolower"
        checked = Array()
        stopwords = self.get_search_stopwords()
        for term in terms:
            #// Keep before/after spaces when term is for exact match.
            if php_preg_match("/^\".+\"$/", term):
                term = php_trim(term, "\"'")
            else:
                term = php_trim(term, "\"' ")
            # end if
            #// Avoid single A-Z and single dashes.
            if (not term) or 1 == php_strlen(term) and php_preg_match("/^[a-z\\-]$/i", term):
                continue
            # end if
            if php_in_array(php_call_user_func(strtolower, term), stopwords, True):
                continue
            # end if
            checked[-1] = term
        # end for
        return checked
    # end def parse_search_terms
    #// 
    #// Retrieve stopwords used when parsing search terms.
    #// 
    #// @since 3.7.0
    #// 
    #// @return string[] Stopwords.
    #//
    def get_search_stopwords(self):
        
        if (php_isset(lambda : self.stopwords)):
            return self.stopwords
        # end if
        #// 
        #// translators: This is a comma-separated list of very common words that should be excluded from a search,
        #// like a, an, and the. These are usually called "stopwords". You should not simply translate these individual
        #// words into your language. Instead, look for and provide commonly accepted stopwords in your language.
        #//
        words = php_explode(",", _x("about,an,are,as,at,be,by,com,for,from,how,in,is,it,of,on,or,that,the,this,to,was,what,when,where,who,will,with,www", "Comma-separated list of search stopwords in your language"))
        stopwords = Array()
        for word in words:
            word = php_trim(word, "\r\n  ")
            if word:
                stopwords[-1] = word
            # end if
        # end for
        #// 
        #// Filters stopwords used when parsing search terms.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string[] $stopwords Array of stopwords.
        #//
        self.stopwords = apply_filters("wp_search_stopwords", stopwords)
        return self.stopwords
    # end def get_search_stopwords
    #// 
    #// Generates SQL for the ORDER BY condition based on passed search terms.
    #// 
    #// @since 3.7.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param array $q Query variables.
    #// @return string ORDER BY clause.
    #//
    def parse_search_order(self, q=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        if q["search_terms_count"] > 1:
            num_terms = php_count(q["search_orderby_title"])
            #// If the search terms contain negative queries, don't bother ordering by sentence matches.
            like = ""
            if (not php_preg_match("/(?:\\s|^)\\-/", q["s"])):
                like = "%" + wpdb.esc_like(q["s"]) + "%"
            # end if
            search_orderby = ""
            #// Sentence match in 'post_title'.
            if like:
                search_orderby += wpdb.prepare(str("WHEN ") + str(wpdb.posts) + str(".post_title LIKE %s THEN 1 "), like)
            # end if
            #// Sanity limit, sort as sentence when more than 6 terms
            #// (few searches are longer than 6 terms and most titles are not).
            if num_terms < 7:
                #// All words in title.
                search_orderby += "WHEN " + php_implode(" AND ", q["search_orderby_title"]) + " THEN 2 "
                #// Any word in title, not needed when $num_terms == 1.
                if num_terms > 1:
                    search_orderby += "WHEN " + php_implode(" OR ", q["search_orderby_title"]) + " THEN 3 "
                # end if
            # end if
            #// Sentence match in 'post_content' and 'post_excerpt'.
            if like:
                search_orderby += wpdb.prepare(str("WHEN ") + str(wpdb.posts) + str(".post_excerpt LIKE %s THEN 4 "), like)
                search_orderby += wpdb.prepare(str("WHEN ") + str(wpdb.posts) + str(".post_content LIKE %s THEN 5 "), like)
            # end if
            if search_orderby:
                search_orderby = "(CASE " + search_orderby + "ELSE 6 END)"
            # end if
        else:
            #// Single word or sentence search.
            search_orderby = reset(q["search_orderby_title"]) + " DESC"
        # end if
        return search_orderby
    # end def parse_search_order
    #// 
    #// Converts the given orderby alias (if allowed) to a properly-prefixed value.
    #// 
    #// @since 4.0.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $orderby Alias for the field to order by.
    #// @return string|false Table-prefixed value to used in the ORDER clause. False otherwise.
    #//
    def parse_orderby(self, orderby=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// Used to filter values.
        allowed_keys = Array("post_name", "post_author", "post_date", "post_title", "post_modified", "post_parent", "post_type", "name", "author", "date", "title", "modified", "parent", "type", "ID", "menu_order", "comment_count", "rand", "post__in", "post_parent__in", "post_name__in")
        primary_meta_key = ""
        primary_meta_query = False
        meta_clauses = self.meta_query.get_clauses()
        if (not php_empty(lambda : meta_clauses)):
            primary_meta_query = reset(meta_clauses)
            if (not php_empty(lambda : primary_meta_query["key"])):
                primary_meta_key = primary_meta_query["key"]
                allowed_keys[-1] = primary_meta_key
            # end if
            allowed_keys[-1] = "meta_value"
            allowed_keys[-1] = "meta_value_num"
            allowed_keys = php_array_merge(allowed_keys, php_array_keys(meta_clauses))
        # end if
        #// If RAND() contains a seed value, sanitize and add to allowed keys.
        rand_with_seed = False
        if php_preg_match("/RAND\\(([0-9]+)\\)/i", orderby, matches):
            orderby = php_sprintf("RAND(%s)", php_intval(matches[1]))
            allowed_keys[-1] = orderby
            rand_with_seed = True
        # end if
        if (not php_in_array(orderby, allowed_keys, True)):
            return False
        # end if
        orderby_clause = ""
        for case in Switch(orderby):
            if case("post_name"):
                pass
            # end if
            if case("post_author"):
                pass
            # end if
            if case("post_date"):
                pass
            # end if
            if case("post_title"):
                pass
            # end if
            if case("post_modified"):
                pass
            # end if
            if case("post_parent"):
                pass
            # end if
            if case("post_type"):
                pass
            # end if
            if case("ID"):
                pass
            # end if
            if case("menu_order"):
                pass
            # end if
            if case("comment_count"):
                orderby_clause = str(wpdb.posts) + str(".") + str(orderby)
                break
            # end if
            if case("rand"):
                orderby_clause = "RAND()"
                break
            # end if
            if case(primary_meta_key):
                pass
            # end if
            if case("meta_value"):
                if (not php_empty(lambda : primary_meta_query["type"])):
                    orderby_clause = str("CAST(") + str(primary_meta_query["alias"]) + str(".meta_value AS ") + str(primary_meta_query["cast"]) + str(")")
                else:
                    orderby_clause = str(primary_meta_query["alias"]) + str(".meta_value")
                # end if
                break
            # end if
            if case("meta_value_num"):
                orderby_clause = str(primary_meta_query["alias"]) + str(".meta_value+0")
                break
            # end if
            if case("post__in"):
                if (not php_empty(lambda : self.query_vars["post__in"])):
                    orderby_clause = str("FIELD(") + str(wpdb.posts) + str(".ID,") + php_implode(",", php_array_map("absint", self.query_vars["post__in"])) + ")"
                # end if
                break
            # end if
            if case("post_parent__in"):
                if (not php_empty(lambda : self.query_vars["post_parent__in"])):
                    orderby_clause = str("FIELD( ") + str(wpdb.posts) + str(".post_parent,") + php_implode(", ", php_array_map("absint", self.query_vars["post_parent__in"])) + " )"
                # end if
                break
            # end if
            if case("post_name__in"):
                if (not php_empty(lambda : self.query_vars["post_name__in"])):
                    post_name__in = php_array_map("sanitize_title_for_query", self.query_vars["post_name__in"])
                    post_name__in_string = "'" + php_implode("','", post_name__in) + "'"
                    orderby_clause = str("FIELD( ") + str(wpdb.posts) + str(".post_name,") + post_name__in_string + " )"
                # end if
                break
            # end if
            if case():
                if php_array_key_exists(orderby, meta_clauses):
                    #// $orderby corresponds to a meta_query clause.
                    meta_clause = meta_clauses[orderby]
                    orderby_clause = str("CAST(") + str(meta_clause["alias"]) + str(".meta_value AS ") + str(meta_clause["cast"]) + str(")")
                elif rand_with_seed:
                    orderby_clause = orderby
                else:
                    #// Default: order by post field.
                    orderby_clause = str(wpdb.posts) + str(".post_") + sanitize_key(orderby)
                # end if
                break
            # end if
        # end for
        return orderby_clause
    # end def parse_orderby
    #// 
    #// Parse an 'order' query variable and cast it to ASC or DESC as necessary.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $order The 'order' query variable.
    #// @return string The sanitized 'order' query variable.
    #//
    def parse_order(self, order=None):
        
        if (not php_is_string(order)) or php_empty(lambda : order):
            return "DESC"
        # end if
        if "ASC" == php_strtoupper(order):
            return "ASC"
        else:
            return "DESC"
        # end if
    # end def parse_order
    #// 
    #// Sets the 404 property and saves whether query is feed.
    #// 
    #// @since 2.0.0
    #//
    def set_404(self):
        
        is_feed = self.is_feed
        self.init_query_flags()
        self.is_404 = True
        self.is_feed = is_feed
    # end def set_404
    #// 
    #// Retrieve query variable.
    #// 
    #// @since 1.5.0
    #// @since 3.9.0 The `$default` argument was introduced.
    #// 
    #// @param string $query_var Query variable key.
    #// @param mixed  $default   Optional. Value to return if the query variable is not set. Default empty.
    #// @return mixed Contents of the query variable.
    #//
    def get(self, query_var=None, default=""):
        
        if (php_isset(lambda : self.query_vars[query_var])):
            return self.query_vars[query_var]
        # end if
        return default
    # end def get
    #// 
    #// Set query variable.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $query_var Query variable key.
    #// @param mixed  $value     Query variable value.
    #//
    def set(self, query_var=None, value=None):
        
        self.query_vars[query_var] = value
    # end def set
    #// 
    #// Retrieves an array of posts based on query variables.
    #// 
    #// There are a few filters and actions that can be used to modify the post
    #// database query.
    #// 
    #// @since 1.5.0
    #// 
    #// @return WP_Post[]|int[] Array of post objects or post IDs.
    #//
    def get_posts(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        self.parse_query()
        #// 
        #// Fires after the query variable object is created, but before the actual query is run.
        #// 
        #// Note: If using conditional tags, use the method versions within the passed instance
        #// (e.g. $this->is_main_query() instead of is_main_query()). This is because the functions
        #// like is_main_query() test against the global $wp_query instance, not the passed one.
        #// 
        #// @since 2.0.0
        #// 
        #// @param WP_Query $this The WP_Query instance (passed by reference).
        #//
        do_action_ref_array("pre_get_posts", Array(self))
        #// Shorthand.
        q = self.query_vars
        #// Fill again in case 'pre_get_posts' unset some vars.
        q = self.fill_query_vars(q)
        #// Parse meta query.
        self.meta_query = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query())
        self.meta_query.parse_query_vars(q)
        #// Set a flag if a 'pre_get_posts' hook changed the query vars.
        hash = php_md5(serialize(self.query_vars))
        if hash != self.query_vars_hash:
            self.query_vars_changed = True
            self.query_vars_hash = hash
        # end if
        hash = None
        #// First let's clear some variables.
        distinct = ""
        whichauthor = ""
        whichmimetype = ""
        where = ""
        limits = ""
        join = ""
        search = ""
        groupby = ""
        post_status_join = False
        page = 1
        if (php_isset(lambda : q["caller_get_posts"])):
            _deprecated_argument("WP_Query", "3.1.0", php_sprintf(__("%1$s is deprecated. Use %2$s instead."), "<code>caller_get_posts</code>", "<code>ignore_sticky_posts</code>"))
            if (not (php_isset(lambda : q["ignore_sticky_posts"]))):
                q["ignore_sticky_posts"] = q["caller_get_posts"]
            # end if
        # end if
        if (not (php_isset(lambda : q["ignore_sticky_posts"]))):
            q["ignore_sticky_posts"] = False
        # end if
        if (not (php_isset(lambda : q["suppress_filters"]))):
            q["suppress_filters"] = False
        # end if
        if (not (php_isset(lambda : q["cache_results"]))):
            if wp_using_ext_object_cache():
                q["cache_results"] = False
            else:
                q["cache_results"] = True
            # end if
        # end if
        if (not (php_isset(lambda : q["update_post_term_cache"]))):
            q["update_post_term_cache"] = True
        # end if
        if (not (php_isset(lambda : q["lazy_load_term_meta"]))):
            q["lazy_load_term_meta"] = q["update_post_term_cache"]
        # end if
        if (not (php_isset(lambda : q["update_post_meta_cache"]))):
            q["update_post_meta_cache"] = True
        # end if
        if (not (php_isset(lambda : q["post_type"]))):
            if self.is_search:
                q["post_type"] = "any"
            else:
                q["post_type"] = ""
            # end if
        # end if
        post_type = q["post_type"]
        if php_empty(lambda : q["posts_per_page"]):
            q["posts_per_page"] = get_option("posts_per_page")
        # end if
        if (php_isset(lambda : q["showposts"])) and q["showposts"]:
            q["showposts"] = php_int(q["showposts"])
            q["posts_per_page"] = q["showposts"]
        # end if
        if (php_isset(lambda : q["posts_per_archive_page"])) and 0 != q["posts_per_archive_page"] and self.is_archive or self.is_search:
            q["posts_per_page"] = q["posts_per_archive_page"]
        # end if
        if (not (php_isset(lambda : q["nopaging"]))):
            if -1 == q["posts_per_page"]:
                q["nopaging"] = True
            else:
                q["nopaging"] = False
            # end if
        # end if
        if self.is_feed:
            #// This overrides 'posts_per_page'.
            if (not php_empty(lambda : q["posts_per_rss"])):
                q["posts_per_page"] = q["posts_per_rss"]
            else:
                q["posts_per_page"] = get_option("posts_per_rss")
            # end if
            q["nopaging"] = False
        # end if
        q["posts_per_page"] = php_int(q["posts_per_page"])
        if q["posts_per_page"] < -1:
            q["posts_per_page"] = abs(q["posts_per_page"])
        elif 0 == q["posts_per_page"]:
            q["posts_per_page"] = 1
        # end if
        if (not (php_isset(lambda : q["comments_per_page"]))) or 0 == q["comments_per_page"]:
            q["comments_per_page"] = get_option("comments_per_page")
        # end if
        if self.is_home and php_empty(lambda : self.query) or "true" == q["preview"] and "page" == get_option("show_on_front") and get_option("page_on_front"):
            self.is_page = True
            self.is_home = False
            q["page_id"] = get_option("page_on_front")
        # end if
        if (php_isset(lambda : q["page"])):
            q["page"] = php_trim(q["page"], "/")
            q["page"] = absint(q["page"])
        # end if
        #// If true, forcibly turns off SQL_CALC_FOUND_ROWS even when limits are present.
        if (php_isset(lambda : q["no_found_rows"])):
            q["no_found_rows"] = php_bool(q["no_found_rows"])
        else:
            q["no_found_rows"] = False
        # end if
        for case in Switch(q["fields"]):
            if case("ids"):
                fields = str(wpdb.posts) + str(".ID")
                break
            # end if
            if case("id=>parent"):
                fields = str(wpdb.posts) + str(".ID, ") + str(wpdb.posts) + str(".post_parent")
                break
            # end if
            if case():
                fields = str(wpdb.posts) + str(".*")
            # end if
        # end for
        if "" != q["menu_order"]:
            where += str(" AND ") + str(wpdb.posts) + str(".menu_order = ") + q["menu_order"]
        # end if
        #// The "m" parameter is meant for months but accepts datetimes of varying specificity.
        if q["m"]:
            where += str(" AND YEAR(") + str(wpdb.posts) + str(".post_date)=") + php_substr(q["m"], 0, 4)
            if php_strlen(q["m"]) > 5:
                where += str(" AND MONTH(") + str(wpdb.posts) + str(".post_date)=") + php_substr(q["m"], 4, 2)
            # end if
            if php_strlen(q["m"]) > 7:
                where += str(" AND DAYOFMONTH(") + str(wpdb.posts) + str(".post_date)=") + php_substr(q["m"], 6, 2)
            # end if
            if php_strlen(q["m"]) > 9:
                where += str(" AND HOUR(") + str(wpdb.posts) + str(".post_date)=") + php_substr(q["m"], 8, 2)
            # end if
            if php_strlen(q["m"]) > 11:
                where += str(" AND MINUTE(") + str(wpdb.posts) + str(".post_date)=") + php_substr(q["m"], 10, 2)
            # end if
            if php_strlen(q["m"]) > 13:
                where += str(" AND SECOND(") + str(wpdb.posts) + str(".post_date)=") + php_substr(q["m"], 12, 2)
            # end if
        # end if
        #// Handle the other individual date parameters.
        date_parameters = Array()
        if "" != q["hour"]:
            date_parameters["hour"] = q["hour"]
        # end if
        if "" != q["minute"]:
            date_parameters["minute"] = q["minute"]
        # end if
        if "" != q["second"]:
            date_parameters["second"] = q["second"]
        # end if
        if q["year"]:
            date_parameters["year"] = q["year"]
        # end if
        if q["monthnum"]:
            date_parameters["monthnum"] = q["monthnum"]
        # end if
        if q["w"]:
            date_parameters["week"] = q["w"]
        # end if
        if q["day"]:
            date_parameters["day"] = q["day"]
        # end if
        if date_parameters:
            date_query = php_new_class("WP_Date_Query", lambda : WP_Date_Query(Array(date_parameters)))
            where += date_query.get_sql()
        # end if
        date_parameters = None
        date_query = None
        #// Handle complex date queries.
        if (not php_empty(lambda : q["date_query"])):
            self.date_query = php_new_class("WP_Date_Query", lambda : WP_Date_Query(q["date_query"]))
            where += self.date_query.get_sql()
        # end if
        #// If we've got a post_type AND it's not "any" post_type.
        if (not php_empty(lambda : q["post_type"])) and "any" != q["post_type"]:
            for _post_type in q["post_type"]:
                ptype_obj = get_post_type_object(_post_type)
                if (not ptype_obj) or (not ptype_obj.query_var) or php_empty(lambda : q[ptype_obj.query_var]):
                    continue
                # end if
                if (not ptype_obj.hierarchical):
                    #// Non-hierarchical post types can directly use 'name'.
                    q["name"] = q[ptype_obj.query_var]
                else:
                    #// Hierarchical post types will operate through 'pagename'.
                    q["pagename"] = q[ptype_obj.query_var]
                    q["name"] = ""
                # end if
                break
            # end for
            ptype_obj = None
        # end if
        if "" != q["title"]:
            where += wpdb.prepare(str(" AND ") + str(wpdb.posts) + str(".post_title = %s"), stripslashes(q["title"]))
        # end if
        #// Parameters related to 'post_name'.
        if "" != q["name"]:
            q["name"] = sanitize_title_for_query(q["name"])
            where += str(" AND ") + str(wpdb.posts) + str(".post_name = '") + q["name"] + "'"
        elif "" != q["pagename"]:
            if (php_isset(lambda : self.queried_object_id)):
                reqpage = self.queried_object_id
            else:
                if "page" != q["post_type"]:
                    for _post_type in q["post_type"]:
                        ptype_obj = get_post_type_object(_post_type)
                        if (not ptype_obj) or (not ptype_obj.hierarchical):
                            continue
                        # end if
                        reqpage = get_page_by_path(q["pagename"], OBJECT, _post_type)
                        if reqpage:
                            break
                        # end if
                    # end for
                    ptype_obj = None
                else:
                    reqpage = get_page_by_path(q["pagename"])
                # end if
                if (not php_empty(lambda : reqpage)):
                    reqpage = reqpage.ID
                else:
                    reqpage = 0
                # end if
            # end if
            page_for_posts = get_option("page_for_posts")
            if "page" != get_option("show_on_front") or php_empty(lambda : page_for_posts) or reqpage != page_for_posts:
                q["pagename"] = sanitize_title_for_query(wp_basename(q["pagename"]))
                q["name"] = q["pagename"]
                where += str(" AND (") + str(wpdb.posts) + str(".ID = '") + str(reqpage) + str("')")
                reqpage_obj = get_post(reqpage)
                if php_is_object(reqpage_obj) and "attachment" == reqpage_obj.post_type:
                    self.is_attachment = True
                    post_type = "attachment"
                    q["post_type"] = "attachment"
                    self.is_page = True
                    q["attachment_id"] = reqpage
                # end if
            # end if
        elif "" != q["attachment"]:
            q["attachment"] = sanitize_title_for_query(wp_basename(q["attachment"]))
            q["name"] = q["attachment"]
            where += str(" AND ") + str(wpdb.posts) + str(".post_name = '") + q["attachment"] + "'"
        elif php_is_array(q["post_name__in"]) and (not php_empty(lambda : q["post_name__in"])):
            q["post_name__in"] = php_array_map("sanitize_title_for_query", q["post_name__in"])
            post_name__in = "'" + php_implode("','", q["post_name__in"]) + "'"
            where += str(" AND ") + str(wpdb.posts) + str(".post_name IN (") + str(post_name__in) + str(")")
        # end if
        #// If an attachment is requested by number, let it supersede any post number.
        if q["attachment_id"]:
            q["p"] = absint(q["attachment_id"])
        # end if
        #// If a post number is specified, load that post.
        if q["p"]:
            where += str(" AND ") + str(wpdb.posts) + str(".ID = ") + q["p"]
        elif q["post__in"]:
            post__in = php_implode(",", php_array_map("absint", q["post__in"]))
            where += str(" AND ") + str(wpdb.posts) + str(".ID IN (") + str(post__in) + str(")")
        elif q["post__not_in"]:
            post__not_in = php_implode(",", php_array_map("absint", q["post__not_in"]))
            where += str(" AND ") + str(wpdb.posts) + str(".ID NOT IN (") + str(post__not_in) + str(")")
        # end if
        if php_is_numeric(q["post_parent"]):
            where += wpdb.prepare(str(" AND ") + str(wpdb.posts) + str(".post_parent = %d "), q["post_parent"])
        elif q["post_parent__in"]:
            post_parent__in = php_implode(",", php_array_map("absint", q["post_parent__in"]))
            where += str(" AND ") + str(wpdb.posts) + str(".post_parent IN (") + str(post_parent__in) + str(")")
        elif q["post_parent__not_in"]:
            post_parent__not_in = php_implode(",", php_array_map("absint", q["post_parent__not_in"]))
            where += str(" AND ") + str(wpdb.posts) + str(".post_parent NOT IN (") + str(post_parent__not_in) + str(")")
        # end if
        if q["page_id"]:
            if "page" != get_option("show_on_front") or get_option("page_for_posts") != q["page_id"]:
                q["p"] = q["page_id"]
                where = str(" AND ") + str(wpdb.posts) + str(".ID = ") + q["page_id"]
            # end if
        # end if
        #// If a search pattern is specified, load the posts that match.
        if php_strlen(q["s"]):
            search = self.parse_search(q)
        # end if
        if (not q["suppress_filters"]):
            #// 
            #// Filters the search SQL that is used in the WHERE clause of WP_Query.
            #// 
            #// @since 3.0.0
            #// 
            #// @param string   $search Search SQL for WHERE clause.
            #// @param WP_Query $this   The current WP_Query object.
            #//
            search = apply_filters_ref_array("posts_search", Array(search, self))
        # end if
        #// Taxonomies.
        if (not self.is_singular):
            self.parse_tax_query(q)
            clauses = self.tax_query.get_sql(wpdb.posts, "ID")
            join += clauses["join"]
            where += clauses["where"]
        # end if
        if self.is_tax:
            if php_empty(lambda : post_type):
                #// Do a fully inclusive search for currently registered post types of queried taxonomies.
                post_type = Array()
                taxonomies = php_array_keys(self.tax_query.queried_terms)
                for pt in get_post_types(Array({"exclude_from_search": False})):
                    object_taxonomies = get_taxonomies_for_attachments() if "attachment" == pt else get_object_taxonomies(pt)
                    if php_array_intersect(taxonomies, object_taxonomies):
                        post_type[-1] = pt
                    # end if
                # end for
                if (not post_type):
                    post_type = "any"
                elif php_count(post_type) == 1:
                    post_type = post_type[0]
                # end if
                post_status_join = True
            elif php_in_array("attachment", post_type):
                post_status_join = True
            # end if
        # end if
        #// 
        #// Ensure that 'taxonomy', 'term', 'term_id', 'cat', and
        #// 'category_name' vars are set for backward compatibility.
        #//
        if (not php_empty(lambda : self.tax_query.queried_terms)):
            #// 
            #// Set 'taxonomy', 'term', and 'term_id' to the
            #// first taxonomy other than 'post_tag' or 'category'.
            #//
            if (not (php_isset(lambda : q["taxonomy"]))):
                for queried_taxonomy,queried_items in self.tax_query.queried_terms:
                    if php_empty(lambda : queried_items["terms"][0]):
                        continue
                    # end if
                    if (not php_in_array(queried_taxonomy, Array("category", "post_tag"))):
                        q["taxonomy"] = queried_taxonomy
                        if "slug" == queried_items["field"]:
                            q["term"] = queried_items["terms"][0]
                        else:
                            q["term_id"] = queried_items["terms"][0]
                        # end if
                        break
                    # end if
                # end for
            # end if
            #// 'cat', 'category_name', 'tag_id'.
            for queried_taxonomy,queried_items in self.tax_query.queried_terms:
                if php_empty(lambda : queried_items["terms"][0]):
                    continue
                # end if
                if "category" == queried_taxonomy:
                    the_cat = get_term_by(queried_items["field"], queried_items["terms"][0], "category")
                    if the_cat:
                        self.set("cat", the_cat.term_id)
                        self.set("category_name", the_cat.slug)
                    # end if
                    the_cat = None
                # end if
                if "post_tag" == queried_taxonomy:
                    the_tag = get_term_by(queried_items["field"], queried_items["terms"][0], "post_tag")
                    if the_tag:
                        self.set("tag_id", the_tag.term_id)
                    # end if
                    the_tag = None
                # end if
            # end for
        # end if
        if (not php_empty(lambda : self.tax_query.queries)) or (not php_empty(lambda : self.meta_query.queries)):
            groupby = str(wpdb.posts) + str(".ID")
        # end if
        #// Author/user stuff.
        if (not php_empty(lambda : q["author"])) and "0" != q["author"]:
            q["author"] = addslashes_gpc("" + urldecode(q["author"]))
            authors = array_unique(php_array_map("intval", php_preg_split("/[,\\s]+/", q["author"])))
            for author in authors:
                key = "author__in" if author > 0 else "author__not_in"
                q[key][-1] = abs(author)
            # end for
            q["author"] = php_implode(",", authors)
        # end if
        if (not php_empty(lambda : q["author__not_in"])):
            author__not_in = php_implode(",", php_array_map("absint", array_unique(q["author__not_in"])))
            where += str(" AND ") + str(wpdb.posts) + str(".post_author NOT IN (") + str(author__not_in) + str(") ")
        elif (not php_empty(lambda : q["author__in"])):
            author__in = php_implode(",", php_array_map("absint", array_unique(q["author__in"])))
            where += str(" AND ") + str(wpdb.posts) + str(".post_author IN (") + str(author__in) + str(") ")
        # end if
        #// Author stuff for nice URLs.
        if "" != q["author_name"]:
            if php_strpos(q["author_name"], "/") != False:
                q["author_name"] = php_explode("/", q["author_name"])
                if q["author_name"][php_count(q["author_name"]) - 1]:
                    q["author_name"] = q["author_name"][php_count(q["author_name"]) - 1]
                    pass
                else:
                    q["author_name"] = q["author_name"][php_count(q["author_name"]) - 2]
                    pass
                # end if
            # end if
            q["author_name"] = sanitize_title_for_query(q["author_name"])
            q["author"] = get_user_by("slug", q["author_name"])
            if q["author"]:
                q["author"] = q["author"].ID
            # end if
            whichauthor += str(" AND (") + str(wpdb.posts) + str(".post_author = ") + absint(q["author"]) + ")"
        # end if
        #// Matching by comment count.
        if (php_isset(lambda : q["comment_count"])):
            #// Numeric comment count is converted to array format.
            if php_is_numeric(q["comment_count"]):
                q["comment_count"] = Array({"value": php_intval(q["comment_count"])})
            # end if
            if (php_isset(lambda : q["comment_count"]["value"])):
                q["comment_count"] = php_array_merge(Array({"compare": "="}), q["comment_count"])
                #// Fallback for invalid compare operators is '='.
                compare_operators = Array("=", "!=", ">", ">=", "<", "<=")
                if (not php_in_array(q["comment_count"]["compare"], compare_operators, True)):
                    q["comment_count"]["compare"] = "="
                # end if
                where += wpdb.prepare(str(" AND ") + str(wpdb.posts) + str(".comment_count ") + str(q["comment_count"]["compare"]) + str(" %d"), q["comment_count"]["value"])
            # end if
        # end if
        #// MIME-Type stuff for attachment browsing.
        if (php_isset(lambda : q["post_mime_type"])) and "" != q["post_mime_type"]:
            whichmimetype = wp_post_mime_type_where(q["post_mime_type"], wpdb.posts)
        # end if
        where += search + whichauthor + whichmimetype
        if (not php_empty(lambda : self.meta_query.queries)):
            clauses = self.meta_query.get_sql("post", wpdb.posts, "ID", self)
            join += clauses["join"]
            where += clauses["where"]
        # end if
        rand = (php_isset(lambda : q["orderby"])) and "rand" == q["orderby"]
        if (not (php_isset(lambda : q["order"]))):
            q["order"] = "" if rand else "DESC"
        else:
            q["order"] = "" if rand else self.parse_order(q["order"])
        # end if
        #// These values of orderby should ignore the 'order' parameter.
        force_asc = Array("post__in", "post_name__in", "post_parent__in")
        if (php_isset(lambda : q["orderby"])) and php_in_array(q["orderby"], force_asc, True):
            q["order"] = ""
        # end if
        #// Order by.
        if php_empty(lambda : q["orderby"]):
            #// 
            #// Boolean false or empty array blanks out ORDER BY,
            #// while leaving the value unset or otherwise empty sets the default.
            #//
            if (php_isset(lambda : q["orderby"])) and php_is_array(q["orderby"]) or False == q["orderby"]:
                orderby = ""
            else:
                orderby = str(wpdb.posts) + str(".post_date ") + q["order"]
            # end if
        elif "none" == q["orderby"]:
            orderby = ""
        else:
            orderby_array = Array()
            if php_is_array(q["orderby"]):
                for _orderby,order in q["orderby"]:
                    orderby = addslashes_gpc(urldecode(_orderby))
                    parsed = self.parse_orderby(orderby)
                    if (not parsed):
                        continue
                    # end if
                    orderby_array[-1] = parsed + " " + self.parse_order(order)
                # end for
                orderby = php_implode(", ", orderby_array)
            else:
                q["orderby"] = urldecode(q["orderby"])
                q["orderby"] = addslashes_gpc(q["orderby"])
                for i,orderby in php_explode(" ", q["orderby"]):
                    parsed = self.parse_orderby(orderby)
                    #// Only allow certain values for safety.
                    if (not parsed):
                        continue
                    # end if
                    orderby_array[-1] = parsed
                # end for
                orderby = php_implode(" " + q["order"] + ", ", orderby_array)
                if php_empty(lambda : orderby):
                    orderby = str(wpdb.posts) + str(".post_date ") + q["order"]
                elif (not php_empty(lambda : q["order"])):
                    orderby += str(" ") + str(q["order"])
                # end if
            # end if
        # end if
        #// Order search results by relevance only when another "orderby" is not specified in the query.
        if (not php_empty(lambda : q["s"])):
            search_orderby = ""
            if (not php_empty(lambda : q["search_orderby_title"])) and php_empty(lambda : q["orderby"]) and (not self.is_feed) or (php_isset(lambda : q["orderby"])) and "relevance" == q["orderby"]:
                search_orderby = self.parse_search_order(q)
            # end if
            if (not q["suppress_filters"]):
                #// 
                #// Filters the ORDER BY used when ordering search results.
                #// 
                #// @since 3.7.0
                #// 
                #// @param string   $search_orderby The ORDER BY clause.
                #// @param WP_Query $this           The current WP_Query instance.
                #//
                search_orderby = apply_filters("posts_search_orderby", search_orderby, self)
            # end if
            if search_orderby:
                orderby = search_orderby + ", " + orderby if orderby else search_orderby
            # end if
        # end if
        if php_is_array(post_type) and php_count(post_type) > 1:
            post_type_cap = "multiple_post_type"
        else:
            if php_is_array(post_type):
                post_type = reset(post_type)
            # end if
            post_type_object = get_post_type_object(post_type)
            if php_empty(lambda : post_type_object):
                post_type_cap = post_type
            # end if
        # end if
        if (php_isset(lambda : q["post_password"])):
            where += wpdb.prepare(str(" AND ") + str(wpdb.posts) + str(".post_password = %s"), q["post_password"])
            if php_empty(lambda : q["perm"]):
                q["perm"] = "readable"
            # end if
        elif (php_isset(lambda : q["has_password"])):
            where += php_sprintf(str(" AND ") + str(wpdb.posts) + str(".post_password %s ''"), "!=" if q["has_password"] else "=")
        # end if
        if (not php_empty(lambda : q["comment_status"])):
            where += wpdb.prepare(str(" AND ") + str(wpdb.posts) + str(".comment_status = %s "), q["comment_status"])
        # end if
        if (not php_empty(lambda : q["ping_status"])):
            where += wpdb.prepare(str(" AND ") + str(wpdb.posts) + str(".ping_status = %s "), q["ping_status"])
        # end if
        if "any" == post_type:
            in_search_post_types = get_post_types(Array({"exclude_from_search": False}))
            if php_empty(lambda : in_search_post_types):
                where += " AND 1=0 "
            else:
                where += str(" AND ") + str(wpdb.posts) + str(".post_type IN ('") + join("', '", php_array_map("esc_sql", in_search_post_types)) + "')"
            # end if
        elif (not php_empty(lambda : post_type)) and php_is_array(post_type):
            where += str(" AND ") + str(wpdb.posts) + str(".post_type IN ('") + join("', '", esc_sql(post_type)) + "')"
        elif (not php_empty(lambda : post_type)):
            where += wpdb.prepare(str(" AND ") + str(wpdb.posts) + str(".post_type = %s"), post_type)
            post_type_object = get_post_type_object(post_type)
        elif self.is_attachment:
            where += str(" AND ") + str(wpdb.posts) + str(".post_type = 'attachment'")
            post_type_object = get_post_type_object("attachment")
        elif self.is_page:
            where += str(" AND ") + str(wpdb.posts) + str(".post_type = 'page'")
            post_type_object = get_post_type_object("page")
        else:
            where += str(" AND ") + str(wpdb.posts) + str(".post_type = 'post'")
            post_type_object = get_post_type_object("post")
        # end if
        edit_cap = "edit_post"
        read_cap = "read_post"
        if (not php_empty(lambda : post_type_object)):
            edit_others_cap = post_type_object.cap.edit_others_posts
            read_private_cap = post_type_object.cap.read_private_posts
        else:
            edit_others_cap = "edit_others_" + post_type_cap + "s"
            read_private_cap = "read_private_" + post_type_cap + "s"
        # end if
        user_id = get_current_user_id()
        q_status = Array()
        if (not php_empty(lambda : q["post_status"])):
            statuswheres = Array()
            q_status = q["post_status"]
            if (not php_is_array(q_status)):
                q_status = php_explode(",", q_status)
            # end if
            r_status = Array()
            p_status = Array()
            e_status = Array()
            if php_in_array("any", q_status):
                for status in get_post_stati(Array({"exclude_from_search": True})):
                    if (not php_in_array(status, q_status)):
                        e_status[-1] = str(wpdb.posts) + str(".post_status <> '") + str(status) + str("'")
                    # end if
                # end for
            else:
                for status in get_post_stati():
                    if php_in_array(status, q_status):
                        if "private" == status:
                            p_status[-1] = str(wpdb.posts) + str(".post_status = '") + str(status) + str("'")
                        else:
                            r_status[-1] = str(wpdb.posts) + str(".post_status = '") + str(status) + str("'")
                        # end if
                    # end if
                # end for
            # end if
            if php_empty(lambda : q["perm"]) or "readable" != q["perm"]:
                r_status = php_array_merge(r_status, p_status)
                p_status = None
            # end if
            if (not php_empty(lambda : e_status)):
                statuswheres[-1] = "(" + join(" AND ", e_status) + ")"
            # end if
            if (not php_empty(lambda : r_status)):
                if (not php_empty(lambda : q["perm"])) and "editable" == q["perm"] and (not current_user_can(edit_others_cap)):
                    statuswheres[-1] = str("(") + str(wpdb.posts) + str(".post_author = ") + str(user_id) + str(" ") + "AND (" + join(" OR ", r_status) + "))"
                else:
                    statuswheres[-1] = "(" + join(" OR ", r_status) + ")"
                # end if
            # end if
            if (not php_empty(lambda : p_status)):
                if (not php_empty(lambda : q["perm"])) and "readable" == q["perm"] and (not current_user_can(read_private_cap)):
                    statuswheres[-1] = str("(") + str(wpdb.posts) + str(".post_author = ") + str(user_id) + str(" ") + "AND (" + join(" OR ", p_status) + "))"
                else:
                    statuswheres[-1] = "(" + join(" OR ", p_status) + ")"
                # end if
            # end if
            if post_status_join:
                join += str(" LEFT JOIN ") + str(wpdb.posts) + str(" AS p2 ON (") + str(wpdb.posts) + str(".post_parent = p2.ID) ")
                for index,statuswhere in statuswheres:
                    statuswheres[index] = str("(") + str(statuswhere) + str(" OR (") + str(wpdb.posts) + str(".post_status = 'inherit' AND ") + php_str_replace(wpdb.posts, "p2", statuswhere) + "))"
                # end for
            # end if
            where_status = php_implode(" OR ", statuswheres)
            if (not php_empty(lambda : where_status)):
                where += str(" AND (") + str(where_status) + str(")")
            # end if
        elif (not self.is_singular):
            where += str(" AND (") + str(wpdb.posts) + str(".post_status = 'publish'")
            #// Add public states.
            public_states = get_post_stati(Array({"public": True}))
            for state in public_states:
                if "publish" == state:
                    continue
                # end if
                where += str(" OR ") + str(wpdb.posts) + str(".post_status = '") + str(state) + str("'")
            # end for
            if self.is_admin:
                #// Add protected states that should show in the admin all list.
                admin_all_states = get_post_stati(Array({"protected": True, "show_in_admin_all_list": True}))
                for state in admin_all_states:
                    where += str(" OR ") + str(wpdb.posts) + str(".post_status = '") + str(state) + str("'")
                # end for
            # end if
            if is_user_logged_in():
                #// Add private states that are limited to viewing by the author of a post or someone who has caps to read private states.
                private_states = get_post_stati(Array({"private": True}))
                for state in private_states:
                    where += str(" OR ") + str(wpdb.posts) + str(".post_status = '") + str(state) + str("'") if current_user_can(read_private_cap) else str(" OR ") + str(wpdb.posts) + str(".post_author = ") + str(user_id) + str(" AND ") + str(wpdb.posts) + str(".post_status = '") + str(state) + str("'")
                # end for
            # end if
            where += ")"
        # end if
        #// 
        #// Apply filters on where and join prior to paging so that any
        #// manipulations to them are reflected in the paging by day queries.
        #//
        if (not q["suppress_filters"]):
            #// 
            #// Filters the WHERE clause of the query.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string   $where The WHERE clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            where = apply_filters_ref_array("posts_where", Array(where, self))
            #// 
            #// Filters the JOIN clause of the query.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string   $join  The JOIN clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            join = apply_filters_ref_array("posts_join", Array(join, self))
        # end if
        #// Paging.
        if php_empty(lambda : q["nopaging"]) and (not self.is_singular):
            page = absint(q["paged"])
            if (not page):
                page = 1
            # end if
            #// If 'offset' is provided, it takes precedence over 'paged'.
            if (php_isset(lambda : q["offset"])) and php_is_numeric(q["offset"]):
                q["offset"] = absint(q["offset"])
                pgstrt = q["offset"] + ", "
            else:
                pgstrt = absint(page - 1 * q["posts_per_page"]) + ", "
            # end if
            limits = "LIMIT " + pgstrt + q["posts_per_page"]
        # end if
        #// Comments feeds.
        if self.is_comment_feed and (not self.is_singular):
            if self.is_archive or self.is_search:
                cjoin = str("JOIN ") + str(wpdb.posts) + str(" ON (") + str(wpdb.comments) + str(".comment_post_ID = ") + str(wpdb.posts) + str(".ID) ") + str(join) + str(" ")
                cwhere = str("WHERE comment_approved = '1' ") + str(where)
                cgroupby = str(wpdb.comments) + str(".comment_id")
            else:
                #// Other non-singular, e.g. front.
                cjoin = str("JOIN ") + str(wpdb.posts) + str(" ON ( ") + str(wpdb.comments) + str(".comment_post_ID = ") + str(wpdb.posts) + str(".ID )")
                cwhere = "WHERE ( post_status = 'publish' OR ( post_status = 'inherit' AND post_type = 'attachment' ) ) AND comment_approved = '1'"
                cgroupby = ""
            # end if
            if (not q["suppress_filters"]):
                #// 
                #// Filters the JOIN clause of the comments feed query before sending.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string   $cjoin The JOIN clause of the query.
                #// @param WP_Query $this The WP_Query instance (passed by reference).
                #//
                cjoin = apply_filters_ref_array("comment_feed_join", Array(cjoin, self))
                #// 
                #// Filters the WHERE clause of the comments feed query before sending.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string   $cwhere The WHERE clause of the query.
                #// @param WP_Query $this   The WP_Query instance (passed by reference).
                #//
                cwhere = apply_filters_ref_array("comment_feed_where", Array(cwhere, self))
                #// 
                #// Filters the GROUP BY clause of the comments feed query before sending.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string   $cgroupby The GROUP BY clause of the query.
                #// @param WP_Query $this     The WP_Query instance (passed by reference).
                #//
                cgroupby = apply_filters_ref_array("comment_feed_groupby", Array(cgroupby, self))
                #// 
                #// Filters the ORDER BY clause of the comments feed query before sending.
                #// 
                #// @since 2.8.0
                #// 
                #// @param string   $corderby The ORDER BY clause of the query.
                #// @param WP_Query $this     The WP_Query instance (passed by reference).
                #//
                corderby = apply_filters_ref_array("comment_feed_orderby", Array("comment_date_gmt DESC", self))
                #// 
                #// Filters the LIMIT clause of the comments feed query before sending.
                #// 
                #// @since 2.8.0
                #// 
                #// @param string   $climits The JOIN clause of the query.
                #// @param WP_Query $this    The WP_Query instance (passed by reference).
                #//
                climits = apply_filters_ref_array("comment_feed_limits", Array("LIMIT " + get_option("posts_per_rss"), self))
            # end if
            cgroupby = "GROUP BY " + cgroupby if (not php_empty(lambda : cgroupby)) else ""
            corderby = "ORDER BY " + corderby if (not php_empty(lambda : corderby)) else ""
            climits = climits if (not php_empty(lambda : climits)) else ""
            comments = wpdb.get_results(str("SELECT ") + str(distinct) + str(" ") + str(wpdb.comments) + str(".* FROM ") + str(wpdb.comments) + str(" ") + str(cjoin) + str(" ") + str(cwhere) + str(" ") + str(cgroupby) + str(" ") + str(corderby) + str(" ") + str(climits))
            #// Convert to WP_Comment.
            self.comments = php_array_map("get_comment", comments)
            self.comment_count = php_count(self.comments)
            post_ids = Array()
            for comment in self.comments:
                post_ids[-1] = php_int(comment.comment_post_ID)
            # end for
            post_ids = join(",", post_ids)
            join = ""
            if post_ids:
                where = str("AND ") + str(wpdb.posts) + str(".ID IN (") + str(post_ids) + str(") ")
            else:
                where = "AND 0"
            # end if
        # end if
        pieces = Array("where", "groupby", "join", "orderby", "distinct", "fields", "limits")
        #// 
        #// Apply post-paging filters on where and join. Only plugins that
        #// manipulate paging queries should use these hooks.
        #//
        if (not q["suppress_filters"]):
            #// 
            #// Filters the WHERE clause of the query.
            #// 
            #// Specifically for manipulating paging queries.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string   $where The WHERE clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            where = apply_filters_ref_array("posts_where_paged", Array(where, self))
            #// 
            #// Filters the GROUP BY clause of the query.
            #// 
            #// @since 2.0.0
            #// 
            #// @param string   $groupby The GROUP BY clause of the query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            groupby = apply_filters_ref_array("posts_groupby", Array(groupby, self))
            #// 
            #// Filters the JOIN clause of the query.
            #// 
            #// Specifically for manipulating paging queries.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string   $join  The JOIN clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            join = apply_filters_ref_array("posts_join_paged", Array(join, self))
            #// 
            #// Filters the ORDER BY clause of the query.
            #// 
            #// @since 1.5.1
            #// 
            #// @param string   $orderby The ORDER BY clause of the query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            orderby = apply_filters_ref_array("posts_orderby", Array(orderby, self))
            #// 
            #// Filters the DISTINCT clause of the query.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $distinct The DISTINCT clause of the query.
            #// @param WP_Query $this     The WP_Query instance (passed by reference).
            #//
            distinct = apply_filters_ref_array("posts_distinct", Array(distinct, self))
            #// 
            #// Filters the LIMIT clause of the query.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $limits The LIMIT clause of the query.
            #// @param WP_Query $this   The WP_Query instance (passed by reference).
            #//
            limits = apply_filters_ref_array("post_limits", Array(limits, self))
            #// 
            #// Filters the SELECT clause of the query.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $fields The SELECT clause of the query.
            #// @param WP_Query $this   The WP_Query instance (passed by reference).
            #//
            fields = apply_filters_ref_array("posts_fields", Array(fields, self))
            #// 
            #// Filters all query clauses at once, for convenience.
            #// 
            #// Covers the WHERE, GROUP BY, JOIN, ORDER BY, DISTINCT,
            #// fields (SELECT), and LIMITS clauses.
            #// 
            #// @since 3.1.0
            #// 
            #// @param string[] $clauses Associative array of the clauses for the query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            clauses = apply_filters_ref_array("posts_clauses", Array(compact(pieces), self))
            where = clauses["where"] if (php_isset(lambda : clauses["where"])) else ""
            groupby = clauses["groupby"] if (php_isset(lambda : clauses["groupby"])) else ""
            join = clauses["join"] if (php_isset(lambda : clauses["join"])) else ""
            orderby = clauses["orderby"] if (php_isset(lambda : clauses["orderby"])) else ""
            distinct = clauses["distinct"] if (php_isset(lambda : clauses["distinct"])) else ""
            fields = clauses["fields"] if (php_isset(lambda : clauses["fields"])) else ""
            limits = clauses["limits"] if (php_isset(lambda : clauses["limits"])) else ""
        # end if
        #// 
        #// Fires to announce the query's current selection parameters.
        #// 
        #// For use by caching plugins.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $selection The assembled selection query.
        #//
        do_action("posts_selection", where + groupby + orderby + limits + join)
        #// 
        #// Filters again for the benefit of caching plugins.
        #// Regular plugins should use the hooks above.
        #//
        if (not q["suppress_filters"]):
            #// 
            #// Filters the WHERE clause of the query.
            #// 
            #// For use by caching plugins.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string   $where The WHERE clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            where = apply_filters_ref_array("posts_where_request", Array(where, self))
            #// 
            #// Filters the GROUP BY clause of the query.
            #// 
            #// For use by caching plugins.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string   $groupby The GROUP BY clause of the query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            groupby = apply_filters_ref_array("posts_groupby_request", Array(groupby, self))
            #// 
            #// Filters the JOIN clause of the query.
            #// 
            #// For use by caching plugins.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string   $join  The JOIN clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            join = apply_filters_ref_array("posts_join_request", Array(join, self))
            #// 
            #// Filters the ORDER BY clause of the query.
            #// 
            #// For use by caching plugins.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string   $orderby The ORDER BY clause of the query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            orderby = apply_filters_ref_array("posts_orderby_request", Array(orderby, self))
            #// 
            #// Filters the DISTINCT clause of the query.
            #// 
            #// For use by caching plugins.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string   $distinct The DISTINCT clause of the query.
            #// @param WP_Query $this     The WP_Query instance (passed by reference).
            #//
            distinct = apply_filters_ref_array("posts_distinct_request", Array(distinct, self))
            #// 
            #// Filters the SELECT clause of the query.
            #// 
            #// For use by caching plugins.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string   $fields The SELECT clause of the query.
            #// @param WP_Query $this   The WP_Query instance (passed by reference).
            #//
            fields = apply_filters_ref_array("posts_fields_request", Array(fields, self))
            #// 
            #// Filters the LIMIT clause of the query.
            #// 
            #// For use by caching plugins.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string   $limits The LIMIT clause of the query.
            #// @param WP_Query $this   The WP_Query instance (passed by reference).
            #//
            limits = apply_filters_ref_array("post_limits_request", Array(limits, self))
            #// 
            #// Filters all query clauses at once, for convenience.
            #// 
            #// For use by caching plugins.
            #// 
            #// Covers the WHERE, GROUP BY, JOIN, ORDER BY, DISTINCT,
            #// fields (SELECT), and LIMITS clauses.
            #// 
            #// @since 3.1.0
            #// 
            #// @param string[] $pieces Associative array of the pieces of the query.
            #// @param WP_Query $this   The WP_Query instance (passed by reference).
            #//
            clauses = apply_filters_ref_array("posts_clauses_request", Array(compact(pieces), self))
            where = clauses["where"] if (php_isset(lambda : clauses["where"])) else ""
            groupby = clauses["groupby"] if (php_isset(lambda : clauses["groupby"])) else ""
            join = clauses["join"] if (php_isset(lambda : clauses["join"])) else ""
            orderby = clauses["orderby"] if (php_isset(lambda : clauses["orderby"])) else ""
            distinct = clauses["distinct"] if (php_isset(lambda : clauses["distinct"])) else ""
            fields = clauses["fields"] if (php_isset(lambda : clauses["fields"])) else ""
            limits = clauses["limits"] if (php_isset(lambda : clauses["limits"])) else ""
        # end if
        if (not php_empty(lambda : groupby)):
            groupby = "GROUP BY " + groupby
        # end if
        if (not php_empty(lambda : orderby)):
            orderby = "ORDER BY " + orderby
        # end if
        found_rows = ""
        if (not q["no_found_rows"]) and (not php_empty(lambda : limits)):
            found_rows = "SQL_CALC_FOUND_ROWS"
        # end if
        old_request = str("SELECT ") + str(found_rows) + str(" ") + str(distinct) + str(" ") + str(fields) + str(" FROM ") + str(wpdb.posts) + str(" ") + str(join) + str(" WHERE 1=1 ") + str(where) + str(" ") + str(groupby) + str(" ") + str(orderby) + str(" ") + str(limits)
        self.request = old_request
        if (not q["suppress_filters"]):
            #// 
            #// Filters the completed SQL query before sending.
            #// 
            #// @since 2.0.0
            #// 
            #// @param string   $request The complete SQL query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            self.request = apply_filters_ref_array("posts_request", Array(self.request, self))
        # end if
        #// 
        #// Filters the posts array before the query takes place.
        #// 
        #// Return a non-null value to bypass WordPress's default post queries.
        #// 
        #// Filtering functions that require pagination information are encouraged to set
        #// the `found_posts` and `max_num_pages` properties of the WP_Query object,
        #// passed to the filter by reference. If WP_Query does not perform a database
        #// query, it will not have enough information to generate these values itself.
        #// 
        #// @since 4.6.0
        #// 
        #// @param array|null $posts Return an array of post data to short-circuit WP's query,
        #// or null to allow WP to run its normal queries.
        #// @param WP_Query   $this  The WP_Query instance (passed by reference).
        #//
        self.posts = apply_filters_ref_array("posts_pre_query", Array(None, self))
        if "ids" == q["fields"]:
            if None == self.posts:
                self.posts = wpdb.get_col(self.request)
            # end if
            self.posts = php_array_map("intval", self.posts)
            self.post_count = php_count(self.posts)
            self.set_found_posts(q, limits)
            return self.posts
        # end if
        if "id=>parent" == q["fields"]:
            if None == self.posts:
                self.posts = wpdb.get_results(self.request)
            # end if
            self.post_count = php_count(self.posts)
            self.set_found_posts(q, limits)
            r = Array()
            for key,post in self.posts:
                self.posts[key].ID = php_int(post.ID)
                self.posts[key].post_parent = php_int(post.post_parent)
                r[php_int(post.ID)] = php_int(post.post_parent)
            # end for
            return r
        # end if
        if None == self.posts:
            split_the_query = old_request == self.request and str(wpdb.posts) + str(".*") == fields and (not php_empty(lambda : limits)) and q["posts_per_page"] < 500
            #// 
            #// Filters whether to split the query.
            #// 
            #// Splitting the query will cause it to fetch just the IDs of the found posts
            #// (and then individually fetch each post by ID), rather than fetching every
            #// complete row at once. One massive result vs. many small results.
            #// 
            #// @since 3.4.0
            #// 
            #// @param bool     $split_the_query Whether or not to split the query.
            #// @param WP_Query $this            The WP_Query instance.
            #//
            split_the_query = apply_filters("split_the_query", split_the_query, self)
            if split_the_query:
                #// First get the IDs and then fill in the objects.
                self.request = str("SELECT ") + str(found_rows) + str(" ") + str(distinct) + str(" ") + str(wpdb.posts) + str(".ID FROM ") + str(wpdb.posts) + str(" ") + str(join) + str(" WHERE 1=1 ") + str(where) + str(" ") + str(groupby) + str(" ") + str(orderby) + str(" ") + str(limits)
                #// 
                #// Filters the Post IDs SQL request before sending.
                #// 
                #// @since 3.4.0
                #// 
                #// @param string   $request The post ID request.
                #// @param WP_Query $this    The WP_Query instance.
                #//
                self.request = apply_filters("posts_request_ids", self.request, self)
                ids = wpdb.get_col(self.request)
                if ids:
                    self.posts = ids
                    self.set_found_posts(q, limits)
                    _prime_post_caches(ids, q["update_post_term_cache"], q["update_post_meta_cache"])
                else:
                    self.posts = Array()
                # end if
            else:
                self.posts = wpdb.get_results(self.request)
                self.set_found_posts(q, limits)
            # end if
        # end if
        #// Convert to WP_Post objects.
        if self.posts:
            self.posts = php_array_map("get_post", self.posts)
        # end if
        if (not q["suppress_filters"]):
            #// 
            #// Filters the raw post results array, prior to status checks.
            #// 
            #// @since 2.3.0
            #// 
            #// @param WP_Post[] $posts Array of post objects.
            #// @param WP_Query  $this  The WP_Query instance (passed by reference).
            #//
            self.posts = apply_filters_ref_array("posts_results", Array(self.posts, self))
        # end if
        if (not php_empty(lambda : self.posts)) and self.is_comment_feed and self.is_singular:
            #// This filter is documented in wp-includes/query.php
            cjoin = apply_filters_ref_array("comment_feed_join", Array("", self))
            #// This filter is documented in wp-includes/query.php
            cwhere = apply_filters_ref_array("comment_feed_where", Array(str("WHERE comment_post_ID = '") + str(self.posts[0].ID) + str("' AND comment_approved = '1'"), self))
            #// This filter is documented in wp-includes/query.php
            cgroupby = apply_filters_ref_array("comment_feed_groupby", Array("", self))
            cgroupby = "GROUP BY " + cgroupby if (not php_empty(lambda : cgroupby)) else ""
            #// This filter is documented in wp-includes/query.php
            corderby = apply_filters_ref_array("comment_feed_orderby", Array("comment_date_gmt DESC", self))
            corderby = "ORDER BY " + corderby if (not php_empty(lambda : corderby)) else ""
            #// This filter is documented in wp-includes/query.php
            climits = apply_filters_ref_array("comment_feed_limits", Array("LIMIT " + get_option("posts_per_rss"), self))
            comments_request = str("SELECT ") + str(wpdb.comments) + str(".* FROM ") + str(wpdb.comments) + str(" ") + str(cjoin) + str(" ") + str(cwhere) + str(" ") + str(cgroupby) + str(" ") + str(corderby) + str(" ") + str(climits)
            comments = wpdb.get_results(comments_request)
            #// Convert to WP_Comment.
            self.comments = php_array_map("get_comment", comments)
            self.comment_count = php_count(self.comments)
        # end if
        #// Check post status to determine if post should be displayed.
        if (not php_empty(lambda : self.posts)) and self.is_single or self.is_page:
            status = get_post_status(self.posts[0])
            if "attachment" == self.posts[0].post_type and 0 == php_int(self.posts[0].post_parent):
                self.is_page = False
                self.is_single = True
                self.is_attachment = True
            # end if
            #// If the post_status was specifically requested, let it pass through.
            if (not php_in_array(status, q_status)):
                post_status_obj = get_post_status_object(status)
                if post_status_obj and (not post_status_obj.public):
                    if (not is_user_logged_in()):
                        #// User must be logged in to view unpublished posts.
                        self.posts = Array()
                    else:
                        if post_status_obj.protected:
                            #// User must have edit permissions on the draft to preview.
                            if (not current_user_can(edit_cap, self.posts[0].ID)):
                                self.posts = Array()
                            else:
                                self.is_preview = True
                                if "future" != status:
                                    self.posts[0].post_date = current_time("mysql")
                                # end if
                            # end if
                        elif post_status_obj.private:
                            if (not current_user_can(read_cap, self.posts[0].ID)):
                                self.posts = Array()
                            # end if
                        else:
                            self.posts = Array()
                        # end if
                    # end if
                elif (not post_status_obj):
                    #// Post status is not registered, assume it's not public.
                    if (not current_user_can(edit_cap, self.posts[0].ID)):
                        self.posts = Array()
                    # end if
                # end if
            # end if
            if self.is_preview and self.posts and current_user_can(edit_cap, self.posts[0].ID):
                #// 
                #// Filters the single post for preview mode.
                #// 
                #// @since 2.7.0
                #// 
                #// @param WP_Post  $post_preview  The Post object.
                #// @param WP_Query $this          The WP_Query instance (passed by reference).
                #//
                self.posts[0] = get_post(apply_filters_ref_array("the_preview", Array(self.posts[0], self)))
            # end if
        # end if
        #// Put sticky posts at the top of the posts array.
        sticky_posts = get_option("sticky_posts")
        if self.is_home and page <= 1 and php_is_array(sticky_posts) and (not php_empty(lambda : sticky_posts)) and (not q["ignore_sticky_posts"]):
            num_posts = php_count(self.posts)
            sticky_offset = 0
            #// Loop over posts and relocate stickies to the front.
            i = 0
            while i < num_posts:
                
                if php_in_array(self.posts[i].ID, sticky_posts):
                    sticky_post = self.posts[i]
                    #// Remove sticky from current position.
                    array_splice(self.posts, i, 1)
                    #// Move to front, after other stickies.
                    array_splice(self.posts, sticky_offset, 0, Array(sticky_post))
                    #// Increment the sticky offset. The next sticky will be placed at this offset.
                    sticky_offset += 1
                    #// Remove post from sticky posts array.
                    offset = php_array_search(sticky_post.ID, sticky_posts)
                    sticky_posts[offset] = None
                # end if
                i += 1
            # end while
            #// If any posts have been excluded specifically, Ignore those that are sticky.
            if (not php_empty(lambda : sticky_posts)) and (not php_empty(lambda : q["post__not_in"])):
                sticky_posts = php_array_diff(sticky_posts, q["post__not_in"])
            # end if
            #// Fetch sticky posts that weren't in the query results.
            if (not php_empty(lambda : sticky_posts)):
                stickies = get_posts(Array({"post__in": sticky_posts, "post_type": post_type, "post_status": "publish", "nopaging": True}))
                for sticky_post in stickies:
                    array_splice(self.posts, sticky_offset, 0, Array(sticky_post))
                    sticky_offset += 1
                # end for
            # end if
        # end if
        #// If comments have been fetched as part of the query, make sure comment meta lazy-loading is set up.
        if (not php_empty(lambda : self.comments)):
            wp_queue_comments_for_comment_meta_lazyload(self.comments)
        # end if
        if (not q["suppress_filters"]):
            #// 
            #// Filters the array of retrieved posts after they've been fetched and
            #// internally processed.
            #// 
            #// @since 1.5.0
            #// 
            #// @param WP_Post[] $posts Array of post objects.
            #// @param WP_Query  $this The WP_Query instance (passed by reference).
            #//
            self.posts = apply_filters_ref_array("the_posts", Array(self.posts, self))
        # end if
        #// Ensure that any posts added/modified via one of the filters above are
        #// of the type WP_Post and are filtered.
        if self.posts:
            self.post_count = php_count(self.posts)
            self.posts = php_array_map("get_post", self.posts)
            if q["cache_results"]:
                update_post_caches(self.posts, post_type, q["update_post_term_cache"], q["update_post_meta_cache"])
            # end if
            self.post = reset(self.posts)
        else:
            self.post_count = 0
            self.posts = Array()
        # end if
        if q["lazy_load_term_meta"]:
            wp_queue_posts_for_term_meta_lazyload(self.posts)
        # end if
        return self.posts
    # end def get_posts
    #// 
    #// Set up the amount of found posts and the number of pages (if limit clause was used)
    #// for the current query.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array  $q      Query variables.
    #// @param string $limits LIMIT clauses of the query.
    #//
    def set_found_posts(self, q=None, limits=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// Bail if posts is an empty array. Continue if posts is an empty string,
        #// null, or false to accommodate caching plugins that fill posts later.
        if q["no_found_rows"] or php_is_array(self.posts) and (not self.posts):
            return
        # end if
        if (not php_empty(lambda : limits)):
            #// 
            #// Filters the query to run for retrieving the found posts.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $found_posts The query to run to find the found posts.
            #// @param WP_Query $this        The WP_Query instance (passed by reference).
            #//
            self.found_posts = wpdb.get_var(apply_filters_ref_array("found_posts_query", Array("SELECT FOUND_ROWS()", self)))
        else:
            if php_is_array(self.posts):
                self.found_posts = php_count(self.posts)
            else:
                if None == self.posts:
                    self.found_posts = 0
                else:
                    self.found_posts = 1
                # end if
            # end if
        # end if
        #// 
        #// Filters the number of found posts for the query.
        #// 
        #// @since 2.1.0
        #// 
        #// @param int      $found_posts The number of posts found.
        #// @param WP_Query $this        The WP_Query instance (passed by reference).
        #//
        self.found_posts = apply_filters_ref_array("found_posts", Array(self.found_posts, self))
        if (not php_empty(lambda : limits)):
            self.max_num_pages = ceil(self.found_posts / q["posts_per_page"])
        # end if
    # end def set_found_posts
    #// 
    #// Set up the next post and iterate current post index.
    #// 
    #// @since 1.5.0
    #// 
    #// @return WP_Post Next post.
    #//
    def next_post(self):
        
        self.current_post += 1
        self.post = self.posts[self.current_post]
        return self.post
    # end def next_post
    #// 
    #// Sets up the current post.
    #// 
    #// Retrieves the next post, sets up the post, sets the 'in the loop'
    #// property to true.
    #// 
    #// @since 1.5.0
    #// 
    #// @global WP_Post $post Global post object.
    #//
    def the_post(self):
        
        global post
        php_check_if_defined("post")
        self.in_the_loop = True
        if -1 == self.current_post:
            #// Loop has just started.
            #// 
            #// Fires once the loop is started.
            #// 
            #// @since 2.0.0
            #// 
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            do_action_ref_array("loop_start", Array(self))
        # end if
        post = self.next_post()
        self.setup_postdata(post)
    # end def the_post
    #// 
    #// Determines whether there are more posts available in the loop.
    #// 
    #// Calls the {@see 'loop_end'} action when the loop is complete.
    #// 
    #// @since 1.5.0
    #// 
    #// @return bool True if posts are available, false if end of loop.
    #//
    def have_posts(self):
        
        if self.current_post + 1 < self.post_count:
            return True
        elif self.current_post + 1 == self.post_count and self.post_count > 0:
            #// 
            #// Fires once the loop has ended.
            #// 
            #// @since 2.0.0
            #// 
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            do_action_ref_array("loop_end", Array(self))
            #// Do some cleaning up after the loop.
            self.rewind_posts()
        elif 0 == self.post_count:
            #// 
            #// Fires if no results are found in a post query.
            #// 
            #// @since 4.9.0
            #// 
            #// @param WP_Query $this The WP_Query instance.
            #//
            do_action("loop_no_results", self)
        # end if
        self.in_the_loop = False
        return False
    # end def have_posts
    #// 
    #// Rewind the posts and reset post index.
    #// 
    #// @since 1.5.0
    #//
    def rewind_posts(self):
        
        self.current_post = -1
        if self.post_count > 0:
            self.post = self.posts[0]
        # end if
    # end def rewind_posts
    #// 
    #// Iterate current comment index and return WP_Comment object.
    #// 
    #// @since 2.2.0
    #// 
    #// @return WP_Comment Comment object.
    #//
    def next_comment(self):
        
        self.current_comment += 1
        self.comment = self.comments[self.current_comment]
        return self.comment
    # end def next_comment
    #// 
    #// Sets up the current comment.
    #// 
    #// @since 2.2.0
    #// @global WP_Comment $comment Global comment object.
    #//
    def the_comment(self):
        
        global comment
        php_check_if_defined("comment")
        comment = self.next_comment()
        if 0 == self.current_comment:
            #// 
            #// Fires once the comment loop is started.
            #// 
            #// @since 2.2.0
            #//
            do_action("comment_loop_start")
        # end if
    # end def the_comment
    #// 
    #// Whether there are more comments available.
    #// 
    #// Automatically rewinds comments when finished.
    #// 
    #// @since 2.2.0
    #// 
    #// @return bool True, if more comments. False, if no more posts.
    #//
    def have_comments(self):
        
        if self.current_comment + 1 < self.comment_count:
            return True
        elif self.current_comment + 1 == self.comment_count:
            self.rewind_comments()
        # end if
        return False
    # end def have_comments
    #// 
    #// Rewind the comments, resets the comment index and comment to first.
    #// 
    #// @since 2.2.0
    #//
    def rewind_comments(self):
        
        self.current_comment = -1
        if self.comment_count > 0:
            self.comment = self.comments[0]
        # end if
    # end def rewind_comments
    #// 
    #// Sets up the WordPress query by parsing query string.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string|array $query URL query string or array of query arguments.
    #// @return WP_Post[]|int[] Array of post objects or post IDs.
    #//
    def query(self, query=None):
        
        self.init()
        self.query = wp_parse_args(query)
        self.query_vars = self.query
        return self.get_posts()
    # end def query
    #// 
    #// Retrieve queried object.
    #// 
    #// If queried object is not set, then the queried object will be set from
    #// the category, tag, taxonomy, posts page, single post, page, or author
    #// query variable. After it is set up, it will be returned.
    #// 
    #// @since 1.5.0
    #// 
    #// @return object
    #//
    def get_queried_object(self):
        
        if (php_isset(lambda : self.queried_object)):
            return self.queried_object
        # end if
        self.queried_object = None
        self.queried_object_id = None
        if self.is_category or self.is_tag or self.is_tax:
            if self.is_category:
                if self.get("cat"):
                    term = get_term(self.get("cat"), "category")
                elif self.get("category_name"):
                    term = get_term_by("slug", self.get("category_name"), "category")
                # end if
            elif self.is_tag:
                if self.get("tag_id"):
                    term = get_term(self.get("tag_id"), "post_tag")
                elif self.get("tag"):
                    term = get_term_by("slug", self.get("tag"), "post_tag")
                # end if
            else:
                #// For other tax queries, grab the first term from the first clause.
                if (not php_empty(lambda : self.tax_query.queried_terms)):
                    queried_taxonomies = php_array_keys(self.tax_query.queried_terms)
                    matched_taxonomy = reset(queried_taxonomies)
                    query = self.tax_query.queried_terms[matched_taxonomy]
                    if (not php_empty(lambda : query["terms"])):
                        if "term_id" == query["field"]:
                            term = get_term(reset(query["terms"]), matched_taxonomy)
                        else:
                            term = get_term_by(query["field"], reset(query["terms"]), matched_taxonomy)
                        # end if
                    # end if
                # end if
            # end if
            if (not php_empty(lambda : term)) and (not is_wp_error(term)):
                self.queried_object = term
                self.queried_object_id = php_int(term.term_id)
                if self.is_category and "category" == self.queried_object.taxonomy:
                    _make_cat_compat(self.queried_object)
                # end if
            # end if
        elif self.is_post_type_archive:
            post_type = self.get("post_type")
            if php_is_array(post_type):
                post_type = reset(post_type)
            # end if
            self.queried_object = get_post_type_object(post_type)
        elif self.is_posts_page:
            page_for_posts = get_option("page_for_posts")
            self.queried_object = get_post(page_for_posts)
            self.queried_object_id = php_int(self.queried_object.ID)
        elif self.is_singular and (not php_empty(lambda : self.post)):
            self.queried_object = self.post
            self.queried_object_id = php_int(self.post.ID)
        elif self.is_author:
            self.queried_object_id = php_int(self.get("author"))
            self.queried_object = get_userdata(self.queried_object_id)
        # end if
        return self.queried_object
    # end def get_queried_object
    #// 
    #// Retrieve ID of the current queried object.
    #// 
    #// @since 1.5.0
    #// 
    #// @return int
    #//
    def get_queried_object_id(self):
        
        self.get_queried_object()
        if (php_isset(lambda : self.queried_object_id)):
            return self.queried_object_id
        # end if
        return 0
    # end def get_queried_object_id
    #// 
    #// Constructor.
    #// 
    #// Sets up the WordPress query, if parameter is not empty.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string|array $query URL query string or array of vars.
    #//
    def __init__(self, query=""):
        
        if (not php_empty(lambda : query)):
            self.query(query)
        # end if
    # end def __init__
    #// 
    #// Make private properties readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to get.
    #// @return mixed Property.
    #//
    def __get(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return self.name
        # end if
    # end def __get
    #// 
    #// Make private properties checkable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to check if set.
    #// @return bool Whether the property is set.
    #//
    def __isset(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return (php_isset(lambda : self.name))
        # end if
    # end def __isset
    #// 
    #// Make private/protected methods readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string   $name      Method to call.
    #// @param array    $arguments Arguments to pass when calling.
    #// @return mixed|false Return value of the callback, false otherwise.
    #//
    def __call(self, name=None, arguments=None):
        
        if php_in_array(name, self.compat_methods):
            return self.name(arguments)
        # end if
        return False
    # end def __call
    #// 
    #// Is the query for an existing archive page?
    #// 
    #// Month, Year, Category, Author, Post Type archive...
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_archive(self):
        
        return php_bool(self.is_archive)
    # end def is_archive
    #// 
    #// Is the query for an existing post type archive page?
    #// 
    #// @since 3.1.0
    #// 
    #// @param string|string[] $post_types Optional. Post type or array of posts types
    #// to check against. Default empty.
    #// @return bool
    #//
    def is_post_type_archive(self, post_types=""):
        
        if php_empty(lambda : post_types) or (not self.is_post_type_archive):
            return php_bool(self.is_post_type_archive)
        # end if
        post_type = self.get("post_type")
        if php_is_array(post_type):
            post_type = reset(post_type)
        # end if
        post_type_object = get_post_type_object(post_type)
        return php_in_array(post_type_object.name, post_types)
    # end def is_post_type_archive
    #// 
    #// Is the query for an existing attachment page?
    #// 
    #// @since 3.1.0
    #// 
    #// @param int|string|int[]|string[] $attachment Optional. Attachment ID, title, slug, or array of such
    #// to check against. Default empty.
    #// @return bool
    #//
    def is_attachment(self, attachment=""):
        
        if (not self.is_attachment):
            return False
        # end if
        if php_empty(lambda : attachment):
            return True
        # end if
        attachment = php_array_map("strval", attachment)
        post_obj = self.get_queried_object()
        if php_in_array(php_str(post_obj.ID), attachment):
            return True
        elif php_in_array(post_obj.post_title, attachment):
            return True
        elif php_in_array(post_obj.post_name, attachment):
            return True
        # end if
        return False
    # end def is_attachment
    #// 
    #// Is the query for an existing author archive page?
    #// 
    #// If the $author parameter is specified, this function will additionally
    #// check if the query is for one of the authors specified.
    #// 
    #// @since 3.1.0
    #// 
    #// @param int|string|int[]|string[] $author Optional. User ID, nickname, nicename, or array of such
    #// to check against. Default empty.
    #// @return bool
    #//
    def is_author(self, author=""):
        
        if (not self.is_author):
            return False
        # end if
        if php_empty(lambda : author):
            return True
        # end if
        author_obj = self.get_queried_object()
        author = php_array_map("strval", author)
        if php_in_array(php_str(author_obj.ID), author):
            return True
        elif php_in_array(author_obj.nickname, author):
            return True
        elif php_in_array(author_obj.user_nicename, author):
            return True
        # end if
        return False
    # end def is_author
    #// 
    #// Is the query for an existing category archive page?
    #// 
    #// If the $category parameter is specified, this function will additionally
    #// check if the query is for one of the categories specified.
    #// 
    #// @since 3.1.0
    #// 
    #// @param int|string|int[]|string[] $category Optional. Category ID, name, slug, or array of such
    #// to check against. Default empty.
    #// @return bool
    #//
    def is_category(self, category=""):
        
        if (not self.is_category):
            return False
        # end if
        if php_empty(lambda : category):
            return True
        # end if
        cat_obj = self.get_queried_object()
        category = php_array_map("strval", category)
        if php_in_array(php_str(cat_obj.term_id), category):
            return True
        elif php_in_array(cat_obj.name, category):
            return True
        elif php_in_array(cat_obj.slug, category):
            return True
        # end if
        return False
    # end def is_category
    #// 
    #// Is the query for an existing tag archive page?
    #// 
    #// If the $tag parameter is specified, this function will additionally
    #// check if the query is for one of the tags specified.
    #// 
    #// @since 3.1.0
    #// 
    #// @param int|string|int[]|string[] $tag Optional. Tag ID, name, slug, or array of such
    #// to check against. Default empty.
    #// @return bool
    #//
    def is_tag(self, tag=""):
        
        if (not self.is_tag):
            return False
        # end if
        if php_empty(lambda : tag):
            return True
        # end if
        tag_obj = self.get_queried_object()
        tag = php_array_map("strval", tag)
        if php_in_array(php_str(tag_obj.term_id), tag):
            return True
        elif php_in_array(tag_obj.name, tag):
            return True
        elif php_in_array(tag_obj.slug, tag):
            return True
        # end if
        return False
    # end def is_tag
    #// 
    #// Is the query for an existing custom taxonomy archive page?
    #// 
    #// If the $taxonomy parameter is specified, this function will additionally
    #// check if the query is for that specific $taxonomy.
    #// 
    #// If the $term parameter is specified in addition to the $taxonomy parameter,
    #// this function will additionally check if the query is for one of the terms
    #// specified.
    #// 
    #// @since 3.1.0
    #// 
    #// @global array $wp_taxonomies
    #// 
    #// @param string|string[]           $taxonomy Optional. Taxonomy slug or slugs to check against.
    #// Default empty.
    #// @param int|string|int[]|string[] $term     Optional. Term ID, name, slug, or array of such
    #// to check against. Default empty.
    #// @return bool True for custom taxonomy archive pages, false for built-in taxonomies
    #// (category and tag archives).
    #//
    def is_tax(self, taxonomy="", term=""):
        
        global wp_taxonomies
        php_check_if_defined("wp_taxonomies")
        if (not self.is_tax):
            return False
        # end if
        if php_empty(lambda : taxonomy):
            return True
        # end if
        queried_object = self.get_queried_object()
        tax_array = php_array_intersect(php_array_keys(wp_taxonomies), taxonomy)
        term_array = term
        #// Check that the taxonomy matches.
        if (not (php_isset(lambda : queried_object.taxonomy)) and php_count(tax_array) and php_in_array(queried_object.taxonomy, tax_array)):
            return False
        # end if
        #// Only a taxonomy provided.
        if php_empty(lambda : term):
            return True
        # end if
        return (php_isset(lambda : queried_object.term_id)) and php_count(php_array_intersect(Array(queried_object.term_id, queried_object.name, queried_object.slug), term_array))
    # end def is_tax
    #// 
    #// Whether the current URL is within the comments popup window.
    #// 
    #// @since 3.1.0
    #// @deprecated 4.5.0
    #// 
    #// @return bool
    #//
    def is_comments_popup(self):
        
        _deprecated_function(__FUNCTION__, "4.5.0")
        return False
    # end def is_comments_popup
    #// 
    #// Is the query for an existing date archive?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_date(self):
        
        return php_bool(self.is_date)
    # end def is_date
    #// 
    #// Is the query for an existing day archive?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_day(self):
        
        return php_bool(self.is_day)
    # end def is_day
    #// 
    #// Is the query for a feed?
    #// 
    #// @since 3.1.0
    #// 
    #// @param string|string[] $feeds Optional. Feed type or array of feed types
    #// to check against. Default empty.
    #// @return bool
    #//
    def is_feed(self, feeds=""):
        
        if php_empty(lambda : feeds) or (not self.is_feed):
            return php_bool(self.is_feed)
        # end if
        qv = self.get("feed")
        if "feed" == qv:
            qv = get_default_feed()
        # end if
        return php_in_array(qv, feeds)
    # end def is_feed
    #// 
    #// Is the query for a comments feed?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_comment_feed(self):
        
        return php_bool(self.is_comment_feed)
    # end def is_comment_feed
    #// 
    #// Is the query for the front page of the site?
    #// 
    #// This is for what is displayed at your site's main URL.
    #// 
    #// Depends on the site's "Front page displays" Reading Settings 'show_on_front' and 'page_on_front'.
    #// 
    #// If you set a static page for the front page of your site, this function will return
    #// true when viewing that page.
    #// 
    #// Otherwise the same as @see WP_Query::is_home()
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool True, if front of site.
    #//
    def is_front_page(self):
        
        #// Most likely case.
        if "posts" == get_option("show_on_front") and self.is_home():
            return True
        elif "page" == get_option("show_on_front") and get_option("page_on_front") and self.is_page(get_option("page_on_front")):
            return True
        else:
            return False
        # end if
    # end def is_front_page
    #// 
    #// Is the query for the blog homepage?
    #// 
    #// This is the page which shows the time based blog content of your site.
    #// 
    #// Depends on the site's "Front page displays" Reading Settings 'show_on_front' and 'page_for_posts'.
    #// 
    #// If you set a static page for the front page of your site, this function will return
    #// true only on the page you set as the "Posts page".
    #// 
    #// @see WP_Query::is_front_page()
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool True if blog view homepage.
    #//
    def is_home(self):
        
        return php_bool(self.is_home)
    # end def is_home
    #// 
    #// Is the query for the Privacy Policy page?
    #// 
    #// This is the page which shows the Privacy Policy content of your site.
    #// 
    #// Depends on the site's "Change your Privacy Policy page" Privacy Settings 'wp_page_for_privacy_policy'.
    #// 
    #// This function will return true only on the page you set as the "Privacy Policy page".
    #// 
    #// @since 5.2.0
    #// 
    #// @return bool True, if Privacy Policy page.
    #//
    def is_privacy_policy(self):
        
        if get_option("wp_page_for_privacy_policy") and self.is_page(get_option("wp_page_for_privacy_policy")):
            return True
        else:
            return False
        # end if
    # end def is_privacy_policy
    #// 
    #// Is the query for an existing month archive?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_month(self):
        
        return php_bool(self.is_month)
    # end def is_month
    #// 
    #// Is the query for an existing single page?
    #// 
    #// If the $page parameter is specified, this function will additionally
    #// check if the query is for one of the pages specified.
    #// 
    #// @see WP_Query::is_single()
    #// @see WP_Query::is_singular()
    #// 
    #// @since 3.1.0
    #// 
    #// @param int|string|int[]|string[] $page Optional. Page ID, title, slug, path, or array of such
    #// to check against. Default empty.
    #// @return bool Whether the query is for an existing single page.
    #//
    def is_page(self, page=""):
        
        if (not self.is_page):
            return False
        # end if
        if php_empty(lambda : page):
            return True
        # end if
        page_obj = self.get_queried_object()
        page = php_array_map("strval", page)
        if php_in_array(php_str(page_obj.ID), page):
            return True
        elif php_in_array(page_obj.post_title, page):
            return True
        elif php_in_array(page_obj.post_name, page):
            return True
        else:
            for pagepath in page:
                if (not php_strpos(pagepath, "/")):
                    continue
                # end if
                pagepath_obj = get_page_by_path(pagepath)
                if pagepath_obj and pagepath_obj.ID == page_obj.ID:
                    return True
                # end if
            # end for
        # end if
        return False
    # end def is_page
    #// 
    #// Is the query for paged result and not for the first page?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_paged(self):
        
        return php_bool(self.is_paged)
    # end def is_paged
    #// 
    #// Is the query for a post or page preview?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_preview(self):
        
        return php_bool(self.is_preview)
    # end def is_preview
    #// 
    #// Is the query for the robots.txt file?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_robots(self):
        
        return php_bool(self.is_robots)
    # end def is_robots
    #// 
    #// Is the query for the favicon.ico file?
    #// 
    #// @since 5.4.0
    #// 
    #// @return bool
    #//
    def is_favicon(self):
        
        return php_bool(self.is_favicon)
    # end def is_favicon
    #// 
    #// Is the query for a search?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_search(self):
        
        return php_bool(self.is_search)
    # end def is_search
    #// 
    #// Is the query for an existing single post?
    #// 
    #// Works for any post type excluding pages.
    #// 
    #// If the $post parameter is specified, this function will additionally
    #// check if the query is for one of the Posts specified.
    #// 
    #// @see WP_Query::is_page()
    #// @see WP_Query::is_singular()
    #// 
    #// @since 3.1.0
    #// 
    #// @param int|string|int[]|string[] $post Optional. Post ID, title, slug, path, or array of such
    #// to check against. Default empty.
    #// @return bool Whether the query is for an existing single post.
    #//
    def is_single(self, post=""):
        
        if (not self.is_single):
            return False
        # end if
        if php_empty(lambda : post):
            return True
        # end if
        post_obj = self.get_queried_object()
        post = php_array_map("strval", post)
        if php_in_array(php_str(post_obj.ID), post):
            return True
        elif php_in_array(post_obj.post_title, post):
            return True
        elif php_in_array(post_obj.post_name, post):
            return True
        else:
            for postpath in post:
                if (not php_strpos(postpath, "/")):
                    continue
                # end if
                postpath_obj = get_page_by_path(postpath, OBJECT, post_obj.post_type)
                if postpath_obj and postpath_obj.ID == post_obj.ID:
                    return True
                # end if
            # end for
        # end if
        return False
    # end def is_single
    #// 
    #// Is the query for an existing single post of any post type (post, attachment, page,
    #// custom post types)?
    #// 
    #// If the $post_types parameter is specified, this function will additionally
    #// check if the query is for one of the Posts Types specified.
    #// 
    #// @see WP_Query::is_page()
    #// @see WP_Query::is_single()
    #// 
    #// @since 3.1.0
    #// 
    #// @param string|string[] $post_types Optional. Post type or array of post types
    #// to check against. Default empty.
    #// @return bool Whether the query is for an existing single post
    #// or any of the given post types.
    #//
    def is_singular(self, post_types=""):
        
        if php_empty(lambda : post_types) or (not self.is_singular):
            return php_bool(self.is_singular)
        # end if
        post_obj = self.get_queried_object()
        return php_in_array(post_obj.post_type, post_types)
    # end def is_singular
    #// 
    #// Is the query for a specific time?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_time(self):
        
        return php_bool(self.is_time)
    # end def is_time
    #// 
    #// Is the query for a trackback endpoint call?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_trackback(self):
        
        return php_bool(self.is_trackback)
    # end def is_trackback
    #// 
    #// Is the query for an existing year archive?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_year(self):
        
        return php_bool(self.is_year)
    # end def is_year
    #// 
    #// Is the query a 404 (returns no results)?
    #// 
    #// @since 3.1.0
    #// 
    #// @return bool
    #//
    def is_404(self):
        
        return php_bool(self.is_404)
    # end def is_404
    #// 
    #// Is the query for an embedded post?
    #// 
    #// @since 4.4.0
    #// 
    #// @return bool
    #//
    def is_embed(self):
        
        return php_bool(self.is_embed)
    # end def is_embed
    #// 
    #// Is the query the main query?
    #// 
    #// @since 3.3.0
    #// 
    #// @global WP_Query $wp_query WordPress Query object.
    #// 
    #// @return bool
    #//
    def is_main_query(self):
        
        global wp_the_query
        php_check_if_defined("wp_the_query")
        return wp_the_query == self
    # end def is_main_query
    #// 
    #// Set up global post data.
    #// 
    #// @since 4.1.0
    #// @since 4.4.0 Added the ability to pass a post ID to `$post`.
    #// 
    #// @global int     $id
    #// @global WP_User $authordata
    #// @global string  $currentday
    #// @global string  $currentmonth
    #// @global int     $page
    #// @global array   $pages
    #// @global int     $multipage
    #// @global int     $more
    #// @global int     $numpages
    #// 
    #// @param WP_Post|object|int $post WP_Post instance or Post ID/object.
    #// @return true True when finished.
    #//
    def setup_postdata(self, post=None):
        
        global id,authordata,currentday,currentmonth,page,pages,multipage,more,numpages
        php_check_if_defined("id","authordata","currentday","currentmonth","page","pages","multipage","more","numpages")
        if (not type(post).__name__ == "WP_Post"):
            post = get_post(post)
        # end if
        if (not post):
            return
        # end if
        elements = self.generate_postdata(post)
        if False == elements:
            return
        # end if
        id = elements["id"]
        authordata = elements["authordata"]
        currentday = elements["currentday"]
        currentmonth = elements["currentmonth"]
        page = elements["page"]
        pages = elements["pages"]
        multipage = elements["multipage"]
        more = elements["more"]
        numpages = elements["numpages"]
        #// 
        #// Fires once the post data has been setup.
        #// 
        #// @since 2.8.0
        #// @since 4.1.0 Introduced `$this` parameter.
        #// 
        #// @param WP_Post  $post The Post object (passed by reference).
        #// @param WP_Query $this The current Query object (passed by reference).
        #//
        do_action_ref_array("the_post", Array(post, self))
        return True
    # end def setup_postdata
    #// 
    #// Generate post data.
    #// 
    #// @since 5.2.0
    #// 
    #// @param WP_Post|object|int $post WP_Post instance or Post ID/object.
    #// @return array|bool $elements Elements of post or false on failure.
    #//
    def generate_postdata(self, post=None):
        
        if (not type(post).__name__ == "WP_Post"):
            post = get_post(post)
        # end if
        if (not post):
            return False
        # end if
        id = php_int(post.ID)
        authordata = get_userdata(post.post_author)
        currentday = mysql2date("d.m.y", post.post_date, False)
        currentmonth = mysql2date("m", post.post_date, False)
        numpages = 1
        multipage = 0
        page = self.get("page")
        if (not page):
            page = 1
        # end if
        #// 
        #// Force full post content when viewing the permalink for the $post,
        #// or when on an RSS feed. Otherwise respect the 'more' tag.
        #//
        if get_queried_object_id() == post.ID and self.is_page() or self.is_single():
            more = 1
        elif self.is_feed():
            more = 1
        else:
            more = 0
        # end if
        content = post.post_content
        if False != php_strpos(content, "<!--nextpage-->"):
            content = php_str_replace("\n<!--nextpage-->\n", "<!--nextpage-->", content)
            content = php_str_replace("\n<!--nextpage-->", "<!--nextpage-->", content)
            content = php_str_replace("<!--nextpage-->\n", "<!--nextpage-->", content)
            #// Remove the nextpage block delimiters, to avoid invalid block structures in the split content.
            content = php_str_replace("<!-- wp:nextpage -->", "", content)
            content = php_str_replace("<!-- /wp:nextpage -->", "", content)
            #// Ignore nextpage at the beginning of the content.
            if 0 == php_strpos(content, "<!--nextpage-->"):
                content = php_substr(content, 15)
            # end if
            pages = php_explode("<!--nextpage-->", content)
        else:
            pages = Array(post.post_content)
        # end if
        #// 
        #// Filters the "pages" derived from splitting the post content.
        #// 
        #// "Pages" are determined by splitting the post content based on the presence
        #// of `<!-- nextpage -->` tags.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[] $pages Array of "pages" from the post content split by `<!-- nextpage -->` tags.
        #// @param WP_Post  $post  Current post object.
        #//
        pages = apply_filters("content_pagination", pages, post)
        numpages = php_count(pages)
        if numpages > 1:
            if page > 1:
                more = 1
            # end if
            multipage = 1
        else:
            multipage = 0
        # end if
        elements = compact("id", "authordata", "currentday", "currentmonth", "page", "pages", "multipage", "more", "numpages")
        return elements
    # end def generate_postdata
    #// 
    #// After looping through a nested query, this function
    #// restores the $post global to the current post in this query.
    #// 
    #// @since 3.7.0
    #// 
    #// @global WP_Post $post Global post object.
    #//
    def reset_postdata(self):
        global PHP_GLOBALS
        if (not php_empty(lambda : self.post)):
            PHP_GLOBALS["post"] = self.post
            self.setup_postdata(self.post)
        # end if
    # end def reset_postdata
    #// 
    #// Lazyload term meta for posts in the loop.
    #// 
    #// @since 4.4.0
    #// @deprecated 4.5.0 See wp_queue_posts_for_term_meta_lazyload().
    #// 
    #// @param mixed $check
    #// @param int   $term_id
    #// @return mixed
    #//
    def lazyload_term_meta(self, check=None, term_id=None):
        
        _deprecated_function(__METHOD__, "4.5.0")
        return check
    # end def lazyload_term_meta
    #// 
    #// Lazyload comment meta for comments in the loop.
    #// 
    #// @since 4.4.0
    #// @deprecated 4.5.0 See wp_queue_comments_for_comment_meta_lazyload().
    #// 
    #// @param mixed $check
    #// @param int   $comment_id
    #// @return mixed
    #//
    def lazyload_comment_meta(self, check=None, comment_id=None):
        
        _deprecated_function(__METHOD__, "4.5.0")
        return check
    # end def lazyload_comment_meta
# end class WP_Query
