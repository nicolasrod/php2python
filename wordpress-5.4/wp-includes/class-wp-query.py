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
    #// 
    #// Query vars set by the user
    #// 
    #// @since 1.5.0
    #// @var array
    #//
    query = Array()
    #// 
    #// Query vars, after parsing
    #// 
    #// @since 1.5.0
    #// @var array
    #//
    query_vars = Array()
    #// 
    #// Taxonomy query, as passed to get_tax_sql()
    #// 
    #// @since 3.1.0
    #// @var object WP_Tax_Query
    #//
    tax_query = Array()
    #// 
    #// Metadata query container
    #// 
    #// @since 3.2.0
    #// @var object WP_Meta_Query
    #//
    meta_query = False
    #// 
    #// Date query container
    #// 
    #// @since 3.7.0
    #// @var object WP_Date_Query
    #//
    date_query = False
    #// 
    #// Holds the data for a single object that is queried.
    #// 
    #// Holds the contents of a post, page, category, attachment.
    #// 
    #// @since 1.5.0
    #// @var object|array
    #//
    queried_object = Array()
    #// 
    #// The ID of the queried object.
    #// 
    #// @since 1.5.0
    #// @var int
    #//
    queried_object_id = Array()
    #// 
    #// Get post database query.
    #// 
    #// @since 2.0.1
    #// @var string
    #//
    request = Array()
    #// 
    #// List of posts.
    #// 
    #// @since 1.5.0
    #// @var array
    #//
    posts = Array()
    #// 
    #// The amount of posts for the current query.
    #// 
    #// @since 1.5.0
    #// @var int
    #//
    post_count = 0
    #// 
    #// Index of the current item in the loop.
    #// 
    #// @since 1.5.0
    #// @var int
    #//
    current_post = -1
    #// 
    #// Whether the loop has started and the caller is in the loop.
    #// 
    #// @since 2.0.0
    #// @var bool
    #//
    in_the_loop = False
    #// 
    #// The current post.
    #// 
    #// @since 1.5.0
    #// @var WP_Post
    #//
    post = Array()
    #// 
    #// The list of comments for current post.
    #// 
    #// @since 2.2.0
    #// @var array
    #//
    comments = Array()
    #// 
    #// The amount of comments for the posts.
    #// 
    #// @since 2.2.0
    #// @var int
    #//
    comment_count = 0
    #// 
    #// The index of the comment in the comment loop.
    #// 
    #// @since 2.2.0
    #// @var int
    #//
    current_comment = -1
    #// 
    #// Current comment ID.
    #// 
    #// @since 2.2.0
    #// @var int
    #//
    comment = Array()
    #// 
    #// The amount of found posts for the current query.
    #// 
    #// If limit clause was not used, equals $post_count.
    #// 
    #// @since 2.1.0
    #// @var int
    #//
    found_posts = 0
    #// 
    #// The amount of pages.
    #// 
    #// @since 2.1.0
    #// @var int
    #//
    max_num_pages = 0
    #// 
    #// The amount of comment pages.
    #// 
    #// @since 2.7.0
    #// @var int
    #//
    max_num_comment_pages = 0
    #// 
    #// Signifies whether the current query is for a single post.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_single = False
    #// 
    #// Signifies whether the current query is for a preview.
    #// 
    #// @since 2.0.0
    #// @var bool
    #//
    is_preview = False
    #// 
    #// Signifies whether the current query is for a page.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_page = False
    #// 
    #// Signifies whether the current query is for an archive.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_archive = False
    #// 
    #// Signifies whether the current query is for a date archive.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_date = False
    #// 
    #// Signifies whether the current query is for a year archive.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_year = False
    #// 
    #// Signifies whether the current query is for a month archive.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_month = False
    #// 
    #// Signifies whether the current query is for a day archive.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_day = False
    #// 
    #// Signifies whether the current query is for a specific time.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_time = False
    #// 
    #// Signifies whether the current query is for an author archive.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_author = False
    #// 
    #// Signifies whether the current query is for a category archive.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_category = False
    #// 
    #// Signifies whether the current query is for a tag archive.
    #// 
    #// @since 2.3.0
    #// @var bool
    #//
    is_tag = False
    #// 
    #// Signifies whether the current query is for a taxonomy archive.
    #// 
    #// @since 2.5.0
    #// @var bool
    #//
    is_tax = False
    #// 
    #// Signifies whether the current query is for a search.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_search = False
    #// 
    #// Signifies whether the current query is for a feed.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_feed = False
    #// 
    #// Signifies whether the current query is for a comment feed.
    #// 
    #// @since 2.2.0
    #// @var bool
    #//
    is_comment_feed = False
    #// 
    #// Signifies whether the current query is for trackback endpoint call.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_trackback = False
    #// 
    #// Signifies whether the current query is for the site homepage.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_home = False
    #// 
    #// Signifies whether the current query is for the Privacy Policy page.
    #// 
    #// @since 5.2.0
    #// @var bool
    #//
    is_privacy_policy = False
    #// 
    #// Signifies whether the current query couldn't find anything.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_404 = False
    #// 
    #// Signifies whether the current query is for an embed.
    #// 
    #// @since 4.4.0
    #// @var bool
    #//
    is_embed = False
    #// 
    #// Signifies whether the current query is for a paged result and not for the first page.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_paged = False
    #// 
    #// Signifies whether the current query is for an administrative interface page.
    #// 
    #// @since 1.5.0
    #// @var bool
    #//
    is_admin = False
    #// 
    #// Signifies whether the current query is for an attachment page.
    #// 
    #// @since 2.0.0
    #// @var bool
    #//
    is_attachment = False
    #// 
    #// Signifies whether the current query is for an existing single post of any post type
    #// (post, attachment, page, custom post types).
    #// 
    #// @since 2.1.0
    #// @var bool
    #//
    is_singular = False
    #// 
    #// Signifies whether the current query is for the robots.txt file.
    #// 
    #// @since 2.1.0
    #// @var bool
    #//
    is_robots = False
    #// 
    #// Signifies whether the current query is for the favicon.ico file.
    #// 
    #// @since 5.4.0
    #// @var bool
    #//
    is_favicon = False
    #// 
    #// Signifies whether the current query is for the page_for_posts page.
    #// 
    #// Basically, the homepage if the option isn't set for the static homepage.
    #// 
    #// @since 2.1.0
    #// @var bool
    #//
    is_posts_page = False
    #// 
    #// Signifies whether the current query is for a post type archive.
    #// 
    #// @since 3.1.0
    #// @var bool
    #//
    is_post_type_archive = False
    #// 
    #// Stores the ->query_vars state like md5(serialize( $this->query_vars ) ) so we know
    #// whether we have to re-parse because something has changed
    #// 
    #// @since 3.1.0
    #// @var bool|string
    #//
    query_vars_hash = False
    #// 
    #// Whether query vars have changed since the initial parse_query() call. Used to catch modifications to query vars made
    #// via pre_get_posts hooks.
    #// 
    #// @since 3.1.1
    #//
    query_vars_changed = True
    #// 
    #// Set if post thumbnails are cached
    #// 
    #// @since 3.2.0
    #// @var bool
    #//
    thumbnails_cached = False
    #// 
    #// Cached list of search stopwords.
    #// 
    #// @since 3.7.0
    #// @var array
    #//
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
    def fill_query_vars(self, array_=None):
        
        
        keys_ = Array("error", "m", "p", "post_parent", "subpost", "subpost_id", "attachment", "attachment_id", "name", "pagename", "page_id", "second", "minute", "hour", "day", "monthnum", "year", "w", "category_name", "tag", "cat", "tag_id", "author", "author_name", "feed", "tb", "paged", "meta_key", "meta_value", "preview", "s", "sentence", "title", "fields", "menu_order", "embed")
        for key_ in keys_:
            if (not (php_isset(lambda : array_[key_]))):
                array_[key_] = ""
            # end if
        # end for
        array_keys_ = Array("category__in", "category__not_in", "category__and", "post__in", "post__not_in", "post_name__in", "tag__in", "tag__not_in", "tag__and", "tag_slug__in", "tag_slug__and", "post_parent__in", "post_parent__not_in", "author__in", "author__not_in")
        for key_ in array_keys_:
            if (not (php_isset(lambda : array_[key_]))):
                array_[key_] = Array()
            # end if
        # end for
        return array_
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
    def parse_query(self, query_=""):
        
        
        if (not php_empty(lambda : query_)):
            self.init()
            self.query = wp_parse_args(query_)
            self.query_vars = self.query
        elif (not (php_isset(lambda : self.query))):
            self.query = self.query_vars
        # end if
        self.query_vars = self.fill_query_vars(self.query_vars)
        qv_ = self.query_vars
        self.query_vars_changed = True
        if (not php_empty(lambda : qv_["robots"])):
            self.is_robots = True
        elif (not php_empty(lambda : qv_["favicon"])):
            self.is_favicon = True
        # end if
        if (not php_is_scalar(qv_["p"])) or qv_["p"] < 0:
            qv_["p"] = 0
            qv_["error"] = "404"
        else:
            qv_["p"] = php_intval(qv_["p"])
        # end if
        qv_["page_id"] = absint(qv_["page_id"])
        qv_["year"] = absint(qv_["year"])
        qv_["monthnum"] = absint(qv_["monthnum"])
        qv_["day"] = absint(qv_["day"])
        qv_["w"] = absint(qv_["w"])
        qv_["m"] = php_preg_replace("|[^0-9]|", "", qv_["m"]) if php_is_scalar(qv_["m"]) else ""
        qv_["paged"] = absint(qv_["paged"])
        qv_["cat"] = php_preg_replace("|[^0-9,-]|", "", qv_["cat"])
        #// Comma-separated list of positive or negative integers.
        qv_["author"] = php_preg_replace("|[^0-9,-]|", "", qv_["author"])
        #// Comma-separated list of positive or negative integers.
        qv_["pagename"] = php_trim(qv_["pagename"])
        qv_["name"] = php_trim(qv_["name"])
        qv_["title"] = php_trim(qv_["title"])
        if "" != qv_["hour"]:
            qv_["hour"] = absint(qv_["hour"])
        # end if
        if "" != qv_["minute"]:
            qv_["minute"] = absint(qv_["minute"])
        # end if
        if "" != qv_["second"]:
            qv_["second"] = absint(qv_["second"])
        # end if
        if "" != qv_["menu_order"]:
            qv_["menu_order"] = absint(qv_["menu_order"])
        # end if
        #// Fairly insane upper bound for search string lengths.
        if (not php_is_scalar(qv_["s"])) or (not php_empty(lambda : qv_["s"])) and php_strlen(qv_["s"]) > 1600:
            qv_["s"] = ""
        # end if
        #// Compat. Map subpost to attachment.
        if "" != qv_["subpost"]:
            qv_["attachment"] = qv_["subpost"]
        # end if
        if "" != qv_["subpost_id"]:
            qv_["attachment_id"] = qv_["subpost_id"]
        # end if
        qv_["attachment_id"] = absint(qv_["attachment_id"])
        if "" != qv_["attachment"] or (not php_empty(lambda : qv_["attachment_id"])):
            self.is_single = True
            self.is_attachment = True
        elif "" != qv_["name"]:
            self.is_single = True
        elif qv_["p"]:
            self.is_single = True
        elif "" != qv_["hour"] and "" != qv_["minute"] and "" != qv_["second"] and "" != qv_["year"] and "" != qv_["monthnum"] and "" != qv_["day"]:
            #// If year, month, day, hour, minute, and second are set,
            #// a single post is being queried.
            self.is_single = True
        elif "" != qv_["pagename"] or (not php_empty(lambda : qv_["page_id"])):
            self.is_page = True
            self.is_single = False
        else:
            #// Look for archive queries. Dates, categories, authors, search, post type archives.
            if (php_isset(lambda : self.query["s"])):
                self.is_search = True
            # end if
            if "" != qv_["second"]:
                self.is_time = True
                self.is_date = True
            # end if
            if "" != qv_["minute"]:
                self.is_time = True
                self.is_date = True
            # end if
            if "" != qv_["hour"]:
                self.is_time = True
                self.is_date = True
            # end if
            if qv_["day"]:
                if (not self.is_date):
                    date_ = php_sprintf("%04d-%02d-%02d", qv_["year"], qv_["monthnum"], qv_["day"])
                    if qv_["monthnum"] and qv_["year"] and (not wp_checkdate(qv_["monthnum"], qv_["day"], qv_["year"], date_)):
                        qv_["error"] = "404"
                    else:
                        self.is_day = True
                        self.is_date = True
                    # end if
                # end if
            # end if
            if qv_["monthnum"]:
                if (not self.is_date):
                    if 12 < qv_["monthnum"]:
                        qv_["error"] = "404"
                    else:
                        self.is_month = True
                        self.is_date = True
                    # end if
                # end if
            # end if
            if qv_["year"]:
                if (not self.is_date):
                    self.is_year = True
                    self.is_date = True
                # end if
            # end if
            if qv_["m"]:
                self.is_date = True
                if php_strlen(qv_["m"]) > 9:
                    self.is_time = True
                elif php_strlen(qv_["m"]) > 7:
                    self.is_day = True
                elif php_strlen(qv_["m"]) > 5:
                    self.is_month = True
                else:
                    self.is_year = True
                # end if
            # end if
            if "" != qv_["w"]:
                self.is_date = True
            # end if
            self.query_vars_hash = False
            self.parse_tax_query(qv_)
            for tax_query_ in self.tax_query.queries:
                if (not php_is_array(tax_query_)):
                    continue
                # end if
                if (php_isset(lambda : tax_query_["operator"])) and "NOT IN" != tax_query_["operator"]:
                    for case in Switch(tax_query_["taxonomy"]):
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
            tax_query_ = None
            if php_empty(lambda : qv_["author"]) or "0" == qv_["author"]:
                self.is_author = False
            else:
                self.is_author = True
            # end if
            if "" != qv_["author_name"]:
                self.is_author = True
            # end if
            if (not php_empty(lambda : qv_["post_type"])) and (not php_is_array(qv_["post_type"])):
                post_type_obj_ = get_post_type_object(qv_["post_type"])
                if (not php_empty(lambda : post_type_obj_.has_archive)):
                    self.is_post_type_archive = True
                # end if
            # end if
            if self.is_post_type_archive or self.is_date or self.is_author or self.is_category or self.is_tag or self.is_tax:
                self.is_archive = True
            # end if
        # end if
        if "" != qv_["feed"]:
            self.is_feed = True
        # end if
        if "" != qv_["embed"]:
            self.is_embed = True
        # end if
        if "" != qv_["tb"]:
            self.is_trackback = True
        # end if
        if "" != qv_["paged"] and php_intval(qv_["paged"]) > 1:
            self.is_paged = True
        # end if
        #// If we're previewing inside the write screen.
        if "" != qv_["preview"]:
            self.is_preview = True
        # end if
        if is_admin():
            self.is_admin = True
        # end if
        if False != php_strpos(qv_["feed"], "comments-"):
            qv_["feed"] = php_str_replace("comments-", "", qv_["feed"])
            qv_["withcomments"] = 1
        # end if
        self.is_singular = self.is_single or self.is_page or self.is_attachment
        if self.is_feed and (not php_empty(lambda : qv_["withcomments"])) or php_empty(lambda : qv_["withoutcomments"]) and self.is_singular:
            self.is_comment_feed = True
        # end if
        if (not self.is_singular or self.is_archive or self.is_search or self.is_feed or php_defined("REST_REQUEST") and REST_REQUEST or self.is_trackback or self.is_404 or self.is_admin or self.is_robots or self.is_favicon):
            self.is_home = True
        # end if
        #// Correct `is_*` for 'page_on_front' and 'page_for_posts'.
        if self.is_home and "page" == get_option("show_on_front") and get_option("page_on_front"):
            _query_ = wp_parse_args(self.query)
            #// 'pagename' can be set and empty depending on matched rewrite rules. Ignore an empty 'pagename'.
            if (php_isset(lambda : _query_["pagename"])) and "" == _query_["pagename"]:
                _query_["pagename"] = None
            # end if
            _query_["embed"] = None
            if php_empty(lambda : _query_) or (not php_array_diff(php_array_keys(_query_), Array("preview", "page", "paged", "cpage"))):
                self.is_page = True
                self.is_home = False
                qv_["page_id"] = get_option("page_on_front")
                #// Correct <!--nextpage--> for 'page_on_front'.
                if (not php_empty(lambda : qv_["paged"])):
                    qv_["page"] = qv_["paged"]
                    qv_["paged"] = None
                # end if
            # end if
        # end if
        if "" != qv_["pagename"]:
            self.queried_object = get_page_by_path(qv_["pagename"])
            if self.queried_object and "attachment" == self.queried_object.post_type:
                if php_preg_match("/^[^%]*%(?:postname)%/", get_option("permalink_structure")):
                    #// See if we also have a post with the same slug.
                    post_ = get_page_by_path(qv_["pagename"], OBJECT, "post")
                    if post_:
                        self.queried_object = post_
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
        if qv_["page_id"]:
            if "page" == get_option("show_on_front") and get_option("page_for_posts") == qv_["page_id"]:
                self.is_page = False
                self.is_home = True
                self.is_posts_page = True
            # end if
            if get_option("wp_page_for_privacy_policy") == qv_["page_id"]:
                self.is_privacy_policy = True
            # end if
        # end if
        if (not php_empty(lambda : qv_["post_type"])):
            if php_is_array(qv_["post_type"]):
                qv_["post_type"] = php_array_map("sanitize_key", qv_["post_type"])
            else:
                qv_["post_type"] = sanitize_key(qv_["post_type"])
            # end if
        # end if
        if (not php_empty(lambda : qv_["post_status"])):
            if php_is_array(qv_["post_status"]):
                qv_["post_status"] = php_array_map("sanitize_key", qv_["post_status"])
            else:
                qv_["post_status"] = php_preg_replace("|[^a-z0-9_,-]|", "", qv_["post_status"])
            # end if
        # end if
        if self.is_posts_page and (not (php_isset(lambda : qv_["withcomments"]))) or (not qv_["withcomments"]):
            self.is_comment_feed = False
        # end if
        self.is_singular = self.is_single or self.is_page or self.is_attachment
        #// Done correcting `is_*` for 'page_on_front' and 'page_for_posts'.
        if "404" == qv_["error"]:
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
    def parse_tax_query(self, q_=None):
        
        
        if (not php_empty(lambda : q_["tax_query"])) and php_is_array(q_["tax_query"]):
            tax_query_ = q_["tax_query"]
        else:
            tax_query_ = Array()
        # end if
        if (not php_empty(lambda : q_["taxonomy"])) and (not php_empty(lambda : q_["term"])):
            tax_query_[-1] = Array({"taxonomy": q_["taxonomy"], "terms": Array(q_["term"]), "field": "slug"})
        # end if
        for taxonomy_,t_ in get_taxonomies(Array(), "objects").items():
            if "post_tag" == taxonomy_:
                continue
                pass
            # end if
            if t_.query_var and (not php_empty(lambda : q_[t_.query_var])):
                tax_query_defaults_ = Array({"taxonomy": taxonomy_, "field": "slug"})
                if (php_isset(lambda : t_.rewrite["hierarchical"])) and t_.rewrite["hierarchical"]:
                    q_[t_.query_var] = wp_basename(q_[t_.query_var])
                # end if
                term_ = q_[t_.query_var]
                if php_is_array(term_):
                    term_ = php_implode(",", term_)
                # end if
                if php_strpos(term_, "+") != False:
                    terms_ = php_preg_split("/[+]+/", term_)
                    for term_ in terms_:
                        tax_query_[-1] = php_array_merge(tax_query_defaults_, Array({"terms": Array(term_)}))
                    # end for
                else:
                    tax_query_[-1] = php_array_merge(tax_query_defaults_, Array({"terms": php_preg_split("/[,]+/", term_)}))
                # end if
            # end if
        # end for
        #// If query string 'cat' is an array, implode it.
        if php_is_array(q_["cat"]):
            q_["cat"] = php_implode(",", q_["cat"])
        # end if
        #// Category stuff.
        if (not php_empty(lambda : q_["cat"])) and (not self.is_singular):
            cat_in_ = Array()
            cat_not_in_ = Array()
            cat_array_ = php_preg_split("/[,\\s]+/", urldecode(q_["cat"]))
            cat_array_ = php_array_map("intval", cat_array_)
            q_["cat"] = php_implode(",", cat_array_)
            for cat_ in cat_array_:
                if cat_ > 0:
                    cat_in_[-1] = cat_
                elif cat_ < 0:
                    cat_not_in_[-1] = abs(cat_)
                # end if
            # end for
            if (not php_empty(lambda : cat_in_)):
                tax_query_[-1] = Array({"taxonomy": "category", "terms": cat_in_, "field": "term_id", "include_children": True})
            # end if
            if (not php_empty(lambda : cat_not_in_)):
                tax_query_[-1] = Array({"taxonomy": "category", "terms": cat_not_in_, "field": "term_id", "operator": "NOT IN", "include_children": True})
            # end if
            cat_array_ = None
            cat_in_ = None
            cat_not_in_ = None
        # end if
        if (not php_empty(lambda : q_["category__and"])) and 1 == php_count(q_["category__and"]):
            q_["category__and"] = q_["category__and"]
            if (not (php_isset(lambda : q_["category__in"]))):
                q_["category__in"] = Array()
            # end if
            q_["category__in"][-1] = absint(reset(q_["category__and"]))
            q_["category__and"] = None
        # end if
        if (not php_empty(lambda : q_["category__in"])):
            q_["category__in"] = php_array_map("absint", array_unique(q_["category__in"]))
            tax_query_[-1] = Array({"taxonomy": "category", "terms": q_["category__in"], "field": "term_id", "include_children": False})
        # end if
        if (not php_empty(lambda : q_["category__not_in"])):
            q_["category__not_in"] = php_array_map("absint", array_unique(q_["category__not_in"]))
            tax_query_[-1] = Array({"taxonomy": "category", "terms": q_["category__not_in"], "operator": "NOT IN", "include_children": False})
        # end if
        if (not php_empty(lambda : q_["category__and"])):
            q_["category__and"] = php_array_map("absint", array_unique(q_["category__and"]))
            tax_query_[-1] = Array({"taxonomy": "category", "terms": q_["category__and"], "field": "term_id", "operator": "AND", "include_children": False})
        # end if
        #// If query string 'tag' is array, implode it.
        if php_is_array(q_["tag"]):
            q_["tag"] = php_implode(",", q_["tag"])
        # end if
        #// Tag stuff.
        if "" != q_["tag"] and (not self.is_singular) and self.query_vars_changed:
            if php_strpos(q_["tag"], ",") != False:
                tags_ = php_preg_split("/[,\\r\\n\\t ]+/", q_["tag"])
                for tag_ in tags_:
                    tag_ = sanitize_term_field("slug", tag_, 0, "post_tag", "db")
                    q_["tag_slug__in"][-1] = tag_
                # end for
            elif php_preg_match("/[+\\r\\n\\t ]+/", q_["tag"]) or (not php_empty(lambda : q_["cat"])):
                tags_ = php_preg_split("/[+\\r\\n\\t ]+/", q_["tag"])
                for tag_ in tags_:
                    tag_ = sanitize_term_field("slug", tag_, 0, "post_tag", "db")
                    q_["tag_slug__and"][-1] = tag_
                # end for
            else:
                q_["tag"] = sanitize_term_field("slug", q_["tag"], 0, "post_tag", "db")
                q_["tag_slug__in"][-1] = q_["tag"]
            # end if
        # end if
        if (not php_empty(lambda : q_["tag_id"])):
            q_["tag_id"] = absint(q_["tag_id"])
            tax_query_[-1] = Array({"taxonomy": "post_tag", "terms": q_["tag_id"]})
        # end if
        if (not php_empty(lambda : q_["tag__in"])):
            q_["tag__in"] = php_array_map("absint", array_unique(q_["tag__in"]))
            tax_query_[-1] = Array({"taxonomy": "post_tag", "terms": q_["tag__in"]})
        # end if
        if (not php_empty(lambda : q_["tag__not_in"])):
            q_["tag__not_in"] = php_array_map("absint", array_unique(q_["tag__not_in"]))
            tax_query_[-1] = Array({"taxonomy": "post_tag", "terms": q_["tag__not_in"], "operator": "NOT IN"})
        # end if
        if (not php_empty(lambda : q_["tag__and"])):
            q_["tag__and"] = php_array_map("absint", array_unique(q_["tag__and"]))
            tax_query_[-1] = Array({"taxonomy": "post_tag", "terms": q_["tag__and"], "operator": "AND"})
        # end if
        if (not php_empty(lambda : q_["tag_slug__in"])):
            q_["tag_slug__in"] = php_array_map("sanitize_title_for_query", array_unique(q_["tag_slug__in"]))
            tax_query_[-1] = Array({"taxonomy": "post_tag", "terms": q_["tag_slug__in"], "field": "slug"})
        # end if
        if (not php_empty(lambda : q_["tag_slug__and"])):
            q_["tag_slug__and"] = php_array_map("sanitize_title_for_query", array_unique(q_["tag_slug__and"]))
            tax_query_[-1] = Array({"taxonomy": "post_tag", "terms": q_["tag_slug__and"], "field": "slug", "operator": "AND"})
        # end if
        self.tax_query = php_new_class("WP_Tax_Query", lambda : WP_Tax_Query(tax_query_))
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
    def parse_search(self, q_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        search_ = ""
        #// Added slashes screw with quote grouping when done early, so done later.
        q_["s"] = stripslashes(q_["s"])
        if php_empty(lambda : PHP_REQUEST["s"]) and self.is_main_query():
            q_["s"] = urldecode(q_["s"])
        # end if
        #// There are no line breaks in <input /> fields.
        q_["s"] = php_str_replace(Array("\r", "\n"), "", q_["s"])
        q_["search_terms_count"] = 1
        if (not php_empty(lambda : q_["sentence"])):
            q_["search_terms"] = Array(q_["s"])
        else:
            if preg_match_all("/\".*?(\"|$)|((?<=[\\t \",+])|^)[^\\t \",+]+/", q_["s"], matches_):
                q_["search_terms_count"] = php_count(matches_[0])
                q_["search_terms"] = self.parse_search_terms(matches_[0])
                #// If the search string has only short terms or stopwords, or is 10+ terms long, match it as sentence.
                if php_empty(lambda : q_["search_terms"]) or php_count(q_["search_terms"]) > 9:
                    q_["search_terms"] = Array(q_["s"])
                # end if
            else:
                q_["search_terms"] = Array(q_["s"])
            # end if
        # end if
        n_ = "" if (not php_empty(lambda : q_["exact"])) else "%"
        searchand_ = ""
        q_["search_orderby_title"] = Array()
        #// 
        #// Filters the prefix that indicates that a search term should be excluded from results.
        #// 
        #// @since 4.7.0
        #// 
        #// @param string $exclusion_prefix The prefix. Default '-'. Returning
        #// an empty value disables exclusions.
        #//
        exclusion_prefix_ = apply_filters("wp_query_search_exclusion_prefix", "-")
        for term_ in q_["search_terms"]:
            #// If there is an $exclusion_prefix, terms prefixed with it should be excluded.
            exclude_ = exclusion_prefix_ and php_substr(term_, 0, 1) == exclusion_prefix_
            if exclude_:
                like_op_ = "NOT LIKE"
                andor_op_ = "AND"
                term_ = php_substr(term_, 1)
            else:
                like_op_ = "LIKE"
                andor_op_ = "OR"
            # end if
            if n_ and (not exclude_):
                like_ = "%" + wpdb_.esc_like(term_) + "%"
                q_["search_orderby_title"][-1] = wpdb_.prepare(str(wpdb_.posts) + str(".post_title LIKE %s"), like_)
            # end if
            like_ = n_ + wpdb_.esc_like(term_) + n_
            search_ += wpdb_.prepare(str(searchand_) + str("((") + str(wpdb_.posts) + str(".post_title ") + str(like_op_) + str(" %s) ") + str(andor_op_) + str(" (") + str(wpdb_.posts) + str(".post_excerpt ") + str(like_op_) + str(" %s) ") + str(andor_op_) + str(" (") + str(wpdb_.posts) + str(".post_content ") + str(like_op_) + str(" %s))"), like_, like_, like_)
            searchand_ = " AND "
        # end for
        if (not php_empty(lambda : search_)):
            search_ = str(" AND (") + str(search_) + str(") ")
            if (not is_user_logged_in()):
                search_ += str(" AND (") + str(wpdb_.posts) + str(".post_password = '') ")
            # end if
        # end if
        return search_
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
    def parse_search_terms(self, terms_=None):
        
        
        strtolower_ = "mb_strtolower" if php_function_exists("mb_strtolower") else "strtolower"
        checked_ = Array()
        stopwords_ = self.get_search_stopwords()
        for term_ in terms_:
            #// Keep before/after spaces when term is for exact match.
            if php_preg_match("/^\".+\"$/", term_):
                term_ = php_trim(term_, "\"'")
            else:
                term_ = php_trim(term_, "\"' ")
            # end if
            #// Avoid single A-Z and single dashes.
            if (not term_) or 1 == php_strlen(term_) and php_preg_match("/^[a-z\\-]$/i", term_):
                continue
            # end if
            if php_in_array(php_call_user_func(strtolower_, term_), stopwords_, True):
                continue
            # end if
            checked_[-1] = term_
        # end for
        return checked_
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
        words_ = php_explode(",", _x("about,an,are,as,at,be,by,com,for,from,how,in,is,it,of,on,or,that,the,this,to,was,what,when,where,who,will,with,www", "Comma-separated list of search stopwords in your language"))
        stopwords_ = Array()
        for word_ in words_:
            word_ = php_trim(word_, "\r\n    ")
            if word_:
                stopwords_[-1] = word_
            # end if
        # end for
        #// 
        #// Filters stopwords used when parsing search terms.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string[] $stopwords Array of stopwords.
        #//
        self.stopwords = apply_filters("wp_search_stopwords", stopwords_)
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
    def parse_search_order(self, q_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if q_["search_terms_count"] > 1:
            num_terms_ = php_count(q_["search_orderby_title"])
            #// If the search terms contain negative queries, don't bother ordering by sentence matches.
            like_ = ""
            if (not php_preg_match("/(?:\\s|^)\\-/", q_["s"])):
                like_ = "%" + wpdb_.esc_like(q_["s"]) + "%"
            # end if
            search_orderby_ = ""
            #// Sentence match in 'post_title'.
            if like_:
                search_orderby_ += wpdb_.prepare(str("WHEN ") + str(wpdb_.posts) + str(".post_title LIKE %s THEN 1 "), like_)
            # end if
            #// Sanity limit, sort as sentence when more than 6 terms
            #// (few searches are longer than 6 terms and most titles are not).
            if num_terms_ < 7:
                #// All words in title.
                search_orderby_ += "WHEN " + php_implode(" AND ", q_["search_orderby_title"]) + " THEN 2 "
                #// Any word in title, not needed when $num_terms == 1.
                if num_terms_ > 1:
                    search_orderby_ += "WHEN " + php_implode(" OR ", q_["search_orderby_title"]) + " THEN 3 "
                # end if
            # end if
            #// Sentence match in 'post_content' and 'post_excerpt'.
            if like_:
                search_orderby_ += wpdb_.prepare(str("WHEN ") + str(wpdb_.posts) + str(".post_excerpt LIKE %s THEN 4 "), like_)
                search_orderby_ += wpdb_.prepare(str("WHEN ") + str(wpdb_.posts) + str(".post_content LIKE %s THEN 5 "), like_)
            # end if
            if search_orderby_:
                search_orderby_ = "(CASE " + search_orderby_ + "ELSE 6 END)"
            # end if
        else:
            #// Single word or sentence search.
            search_orderby_ = reset(q_["search_orderby_title"]) + " DESC"
        # end if
        return search_orderby_
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
    def parse_orderby(self, orderby_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// Used to filter values.
        allowed_keys_ = Array("post_name", "post_author", "post_date", "post_title", "post_modified", "post_parent", "post_type", "name", "author", "date", "title", "modified", "parent", "type", "ID", "menu_order", "comment_count", "rand", "post__in", "post_parent__in", "post_name__in")
        primary_meta_key_ = ""
        primary_meta_query_ = False
        meta_clauses_ = self.meta_query.get_clauses()
        if (not php_empty(lambda : meta_clauses_)):
            primary_meta_query_ = reset(meta_clauses_)
            if (not php_empty(lambda : primary_meta_query_["key"])):
                primary_meta_key_ = primary_meta_query_["key"]
                allowed_keys_[-1] = primary_meta_key_
            # end if
            allowed_keys_[-1] = "meta_value"
            allowed_keys_[-1] = "meta_value_num"
            allowed_keys_ = php_array_merge(allowed_keys_, php_array_keys(meta_clauses_))
        # end if
        #// If RAND() contains a seed value, sanitize and add to allowed keys.
        rand_with_seed_ = False
        if php_preg_match("/RAND\\(([0-9]+)\\)/i", orderby_, matches_):
            orderby_ = php_sprintf("RAND(%s)", php_intval(matches_[1]))
            allowed_keys_[-1] = orderby_
            rand_with_seed_ = True
        # end if
        if (not php_in_array(orderby_, allowed_keys_, True)):
            return False
        # end if
        orderby_clause_ = ""
        for case in Switch(orderby_):
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
                orderby_clause_ = str(wpdb_.posts) + str(".") + str(orderby_)
                break
            # end if
            if case("rand"):
                orderby_clause_ = "RAND()"
                break
            # end if
            if case(primary_meta_key_):
                pass
            # end if
            if case("meta_value"):
                if (not php_empty(lambda : primary_meta_query_["type"])):
                    orderby_clause_ = str("CAST(") + str(primary_meta_query_["alias"]) + str(".meta_value AS ") + str(primary_meta_query_["cast"]) + str(")")
                else:
                    orderby_clause_ = str(primary_meta_query_["alias"]) + str(".meta_value")
                # end if
                break
            # end if
            if case("meta_value_num"):
                orderby_clause_ = str(primary_meta_query_["alias"]) + str(".meta_value+0")
                break
            # end if
            if case("post__in"):
                if (not php_empty(lambda : self.query_vars["post__in"])):
                    orderby_clause_ = str("FIELD(") + str(wpdb_.posts) + str(".ID,") + php_implode(",", php_array_map("absint", self.query_vars["post__in"])) + ")"
                # end if
                break
            # end if
            if case("post_parent__in"):
                if (not php_empty(lambda : self.query_vars["post_parent__in"])):
                    orderby_clause_ = str("FIELD( ") + str(wpdb_.posts) + str(".post_parent,") + php_implode(", ", php_array_map("absint", self.query_vars["post_parent__in"])) + " )"
                # end if
                break
            # end if
            if case("post_name__in"):
                if (not php_empty(lambda : self.query_vars["post_name__in"])):
                    post_name__in_ = php_array_map("sanitize_title_for_query", self.query_vars["post_name__in"])
                    post_name__in_string_ = "'" + php_implode("','", post_name__in_) + "'"
                    orderby_clause_ = str("FIELD( ") + str(wpdb_.posts) + str(".post_name,") + post_name__in_string_ + " )"
                # end if
                break
            # end if
            if case():
                if php_array_key_exists(orderby_, meta_clauses_):
                    #// $orderby corresponds to a meta_query clause.
                    meta_clause_ = meta_clauses_[orderby_]
                    orderby_clause_ = str("CAST(") + str(meta_clause_["alias"]) + str(".meta_value AS ") + str(meta_clause_["cast"]) + str(")")
                elif rand_with_seed_:
                    orderby_clause_ = orderby_
                else:
                    #// Default: order by post field.
                    orderby_clause_ = str(wpdb_.posts) + str(".post_") + sanitize_key(orderby_)
                # end if
                break
            # end if
        # end for
        return orderby_clause_
    # end def parse_orderby
    #// 
    #// Parse an 'order' query variable and cast it to ASC or DESC as necessary.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $order The 'order' query variable.
    #// @return string The sanitized 'order' query variable.
    #//
    def parse_order(self, order_=None):
        
        
        if (not php_is_string(order_)) or php_empty(lambda : order_):
            return "DESC"
        # end if
        if "ASC" == php_strtoupper(order_):
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
        
        
        is_feed_ = self.is_feed
        self.init_query_flags()
        self.is_404 = True
        self.is_feed = is_feed_
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
    def get(self, query_var_=None, default_=""):
        
        
        if (php_isset(lambda : self.query_vars[query_var_])):
            return self.query_vars[query_var_]
        # end if
        return default_
    # end def get
    #// 
    #// Set query variable.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $query_var Query variable key.
    #// @param mixed  $value     Query variable value.
    #//
    def set(self, query_var_=None, value_=None):
        
        
        self.query_vars[query_var_] = value_
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
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
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
        q_ = self.query_vars
        #// Fill again in case 'pre_get_posts' unset some vars.
        q_ = self.fill_query_vars(q_)
        #// Parse meta query.
        self.meta_query = php_new_class("WP_Meta_Query", lambda : WP_Meta_Query())
        self.meta_query.parse_query_vars(q_)
        #// Set a flag if a 'pre_get_posts' hook changed the query vars.
        hash_ = php_md5(serialize(self.query_vars))
        if hash_ != self.query_vars_hash:
            self.query_vars_changed = True
            self.query_vars_hash = hash_
        # end if
        hash_ = None
        #// First let's clear some variables.
        distinct_ = ""
        whichauthor_ = ""
        whichmimetype_ = ""
        where_ = ""
        limits_ = ""
        join_ = ""
        search_ = ""
        groupby_ = ""
        post_status_join_ = False
        page_ = 1
        if (php_isset(lambda : q_["caller_get_posts"])):
            _deprecated_argument("WP_Query", "3.1.0", php_sprintf(__("%1$s is deprecated. Use %2$s instead."), "<code>caller_get_posts</code>", "<code>ignore_sticky_posts</code>"))
            if (not (php_isset(lambda : q_["ignore_sticky_posts"]))):
                q_["ignore_sticky_posts"] = q_["caller_get_posts"]
            # end if
        # end if
        if (not (php_isset(lambda : q_["ignore_sticky_posts"]))):
            q_["ignore_sticky_posts"] = False
        # end if
        if (not (php_isset(lambda : q_["suppress_filters"]))):
            q_["suppress_filters"] = False
        # end if
        if (not (php_isset(lambda : q_["cache_results"]))):
            if wp_using_ext_object_cache():
                q_["cache_results"] = False
            else:
                q_["cache_results"] = True
            # end if
        # end if
        if (not (php_isset(lambda : q_["update_post_term_cache"]))):
            q_["update_post_term_cache"] = True
        # end if
        if (not (php_isset(lambda : q_["lazy_load_term_meta"]))):
            q_["lazy_load_term_meta"] = q_["update_post_term_cache"]
        # end if
        if (not (php_isset(lambda : q_["update_post_meta_cache"]))):
            q_["update_post_meta_cache"] = True
        # end if
        if (not (php_isset(lambda : q_["post_type"]))):
            if self.is_search:
                q_["post_type"] = "any"
            else:
                q_["post_type"] = ""
            # end if
        # end if
        post_type_ = q_["post_type"]
        if php_empty(lambda : q_["posts_per_page"]):
            q_["posts_per_page"] = get_option("posts_per_page")
        # end if
        if (php_isset(lambda : q_["showposts"])) and q_["showposts"]:
            q_["showposts"] = php_int(q_["showposts"])
            q_["posts_per_page"] = q_["showposts"]
        # end if
        if (php_isset(lambda : q_["posts_per_archive_page"])) and 0 != q_["posts_per_archive_page"] and self.is_archive or self.is_search:
            q_["posts_per_page"] = q_["posts_per_archive_page"]
        # end if
        if (not (php_isset(lambda : q_["nopaging"]))):
            if -1 == q_["posts_per_page"]:
                q_["nopaging"] = True
            else:
                q_["nopaging"] = False
            # end if
        # end if
        if self.is_feed:
            #// This overrides 'posts_per_page'.
            if (not php_empty(lambda : q_["posts_per_rss"])):
                q_["posts_per_page"] = q_["posts_per_rss"]
            else:
                q_["posts_per_page"] = get_option("posts_per_rss")
            # end if
            q_["nopaging"] = False
        # end if
        q_["posts_per_page"] = php_int(q_["posts_per_page"])
        if q_["posts_per_page"] < -1:
            q_["posts_per_page"] = abs(q_["posts_per_page"])
        elif 0 == q_["posts_per_page"]:
            q_["posts_per_page"] = 1
        # end if
        if (not (php_isset(lambda : q_["comments_per_page"]))) or 0 == q_["comments_per_page"]:
            q_["comments_per_page"] = get_option("comments_per_page")
        # end if
        if self.is_home and php_empty(lambda : self.query) or "true" == q_["preview"] and "page" == get_option("show_on_front") and get_option("page_on_front"):
            self.is_page = True
            self.is_home = False
            q_["page_id"] = get_option("page_on_front")
        # end if
        if (php_isset(lambda : q_["page"])):
            q_["page"] = php_trim(q_["page"], "/")
            q_["page"] = absint(q_["page"])
        # end if
        #// If true, forcibly turns off SQL_CALC_FOUND_ROWS even when limits are present.
        if (php_isset(lambda : q_["no_found_rows"])):
            q_["no_found_rows"] = php_bool(q_["no_found_rows"])
        else:
            q_["no_found_rows"] = False
        # end if
        for case in Switch(q_["fields"]):
            if case("ids"):
                fields_ = str(wpdb_.posts) + str(".ID")
                break
            # end if
            if case("id=>parent"):
                fields_ = str(wpdb_.posts) + str(".ID, ") + str(wpdb_.posts) + str(".post_parent")
                break
            # end if
            if case():
                fields_ = str(wpdb_.posts) + str(".*")
            # end if
        # end for
        if "" != q_["menu_order"]:
            where_ += str(" AND ") + str(wpdb_.posts) + str(".menu_order = ") + q_["menu_order"]
        # end if
        #// The "m" parameter is meant for months but accepts datetimes of varying specificity.
        if q_["m"]:
            where_ += str(" AND YEAR(") + str(wpdb_.posts) + str(".post_date)=") + php_substr(q_["m"], 0, 4)
            if php_strlen(q_["m"]) > 5:
                where_ += str(" AND MONTH(") + str(wpdb_.posts) + str(".post_date)=") + php_substr(q_["m"], 4, 2)
            # end if
            if php_strlen(q_["m"]) > 7:
                where_ += str(" AND DAYOFMONTH(") + str(wpdb_.posts) + str(".post_date)=") + php_substr(q_["m"], 6, 2)
            # end if
            if php_strlen(q_["m"]) > 9:
                where_ += str(" AND HOUR(") + str(wpdb_.posts) + str(".post_date)=") + php_substr(q_["m"], 8, 2)
            # end if
            if php_strlen(q_["m"]) > 11:
                where_ += str(" AND MINUTE(") + str(wpdb_.posts) + str(".post_date)=") + php_substr(q_["m"], 10, 2)
            # end if
            if php_strlen(q_["m"]) > 13:
                where_ += str(" AND SECOND(") + str(wpdb_.posts) + str(".post_date)=") + php_substr(q_["m"], 12, 2)
            # end if
        # end if
        #// Handle the other individual date parameters.
        date_parameters_ = Array()
        if "" != q_["hour"]:
            date_parameters_["hour"] = q_["hour"]
        # end if
        if "" != q_["minute"]:
            date_parameters_["minute"] = q_["minute"]
        # end if
        if "" != q_["second"]:
            date_parameters_["second"] = q_["second"]
        # end if
        if q_["year"]:
            date_parameters_["year"] = q_["year"]
        # end if
        if q_["monthnum"]:
            date_parameters_["monthnum"] = q_["monthnum"]
        # end if
        if q_["w"]:
            date_parameters_["week"] = q_["w"]
        # end if
        if q_["day"]:
            date_parameters_["day"] = q_["day"]
        # end if
        if date_parameters_:
            date_query_ = php_new_class("WP_Date_Query", lambda : WP_Date_Query(Array(date_parameters_)))
            where_ += date_query_.get_sql()
        # end if
        date_parameters_ = None
        date_query_ = None
        #// Handle complex date queries.
        if (not php_empty(lambda : q_["date_query"])):
            self.date_query = php_new_class("WP_Date_Query", lambda : WP_Date_Query(q_["date_query"]))
            where_ += self.date_query.get_sql()
        # end if
        #// If we've got a post_type AND it's not "any" post_type.
        if (not php_empty(lambda : q_["post_type"])) and "any" != q_["post_type"]:
            for _post_type_ in q_["post_type"]:
                ptype_obj_ = get_post_type_object(_post_type_)
                if (not ptype_obj_) or (not ptype_obj_.query_var) or php_empty(lambda : q_[ptype_obj_.query_var]):
                    continue
                # end if
                if (not ptype_obj_.hierarchical):
                    #// Non-hierarchical post types can directly use 'name'.
                    q_["name"] = q_[ptype_obj_.query_var]
                else:
                    #// Hierarchical post types will operate through 'pagename'.
                    q_["pagename"] = q_[ptype_obj_.query_var]
                    q_["name"] = ""
                # end if
                break
            # end for
            ptype_obj_ = None
        # end if
        if "" != q_["title"]:
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_title = %s"), stripslashes(q_["title"]))
        # end if
        #// Parameters related to 'post_name'.
        if "" != q_["name"]:
            q_["name"] = sanitize_title_for_query(q_["name"])
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_name = '") + q_["name"] + "'"
        elif "" != q_["pagename"]:
            if (php_isset(lambda : self.queried_object_id)):
                reqpage_ = self.queried_object_id
            else:
                if "page" != q_["post_type"]:
                    for _post_type_ in q_["post_type"]:
                        ptype_obj_ = get_post_type_object(_post_type_)
                        if (not ptype_obj_) or (not ptype_obj_.hierarchical):
                            continue
                        # end if
                        reqpage_ = get_page_by_path(q_["pagename"], OBJECT, _post_type_)
                        if reqpage_:
                            break
                        # end if
                    # end for
                    ptype_obj_ = None
                else:
                    reqpage_ = get_page_by_path(q_["pagename"])
                # end if
                if (not php_empty(lambda : reqpage_)):
                    reqpage_ = reqpage_.ID
                else:
                    reqpage_ = 0
                # end if
            # end if
            page_for_posts_ = get_option("page_for_posts")
            if "page" != get_option("show_on_front") or php_empty(lambda : page_for_posts_) or reqpage_ != page_for_posts_:
                q_["pagename"] = sanitize_title_for_query(wp_basename(q_["pagename"]))
                q_["name"] = q_["pagename"]
                where_ += str(" AND (") + str(wpdb_.posts) + str(".ID = '") + str(reqpage_) + str("')")
                reqpage_obj_ = get_post(reqpage_)
                if php_is_object(reqpage_obj_) and "attachment" == reqpage_obj_.post_type:
                    self.is_attachment = True
                    post_type_ = "attachment"
                    q_["post_type"] = "attachment"
                    self.is_page = True
                    q_["attachment_id"] = reqpage_
                # end if
            # end if
        elif "" != q_["attachment"]:
            q_["attachment"] = sanitize_title_for_query(wp_basename(q_["attachment"]))
            q_["name"] = q_["attachment"]
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_name = '") + q_["attachment"] + "'"
        elif php_is_array(q_["post_name__in"]) and (not php_empty(lambda : q_["post_name__in"])):
            q_["post_name__in"] = php_array_map("sanitize_title_for_query", q_["post_name__in"])
            post_name__in_ = "'" + php_implode("','", q_["post_name__in"]) + "'"
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_name IN (") + str(post_name__in_) + str(")")
        # end if
        #// If an attachment is requested by number, let it supersede any post number.
        if q_["attachment_id"]:
            q_["p"] = absint(q_["attachment_id"])
        # end if
        #// If a post number is specified, load that post.
        if q_["p"]:
            where_ += str(" AND ") + str(wpdb_.posts) + str(".ID = ") + q_["p"]
        elif q_["post__in"]:
            post__in_ = php_implode(",", php_array_map("absint", q_["post__in"]))
            where_ += str(" AND ") + str(wpdb_.posts) + str(".ID IN (") + str(post__in_) + str(")")
        elif q_["post__not_in"]:
            post__not_in_ = php_implode(",", php_array_map("absint", q_["post__not_in"]))
            where_ += str(" AND ") + str(wpdb_.posts) + str(".ID NOT IN (") + str(post__not_in_) + str(")")
        # end if
        if php_is_numeric(q_["post_parent"]):
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_parent = %d "), q_["post_parent"])
        elif q_["post_parent__in"]:
            post_parent__in_ = php_implode(",", php_array_map("absint", q_["post_parent__in"]))
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_parent IN (") + str(post_parent__in_) + str(")")
        elif q_["post_parent__not_in"]:
            post_parent__not_in_ = php_implode(",", php_array_map("absint", q_["post_parent__not_in"]))
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_parent NOT IN (") + str(post_parent__not_in_) + str(")")
        # end if
        if q_["page_id"]:
            if "page" != get_option("show_on_front") or get_option("page_for_posts") != q_["page_id"]:
                q_["p"] = q_["page_id"]
                where_ = str(" AND ") + str(wpdb_.posts) + str(".ID = ") + q_["page_id"]
            # end if
        # end if
        #// If a search pattern is specified, load the posts that match.
        if php_strlen(q_["s"]):
            search_ = self.parse_search(q_)
        # end if
        if (not q_["suppress_filters"]):
            #// 
            #// Filters the search SQL that is used in the WHERE clause of WP_Query.
            #// 
            #// @since 3.0.0
            #// 
            #// @param string   $search Search SQL for WHERE clause.
            #// @param WP_Query $this   The current WP_Query object.
            #//
            search_ = apply_filters_ref_array("posts_search", Array(search_, self))
        # end if
        #// Taxonomies.
        if (not self.is_singular):
            self.parse_tax_query(q_)
            clauses_ = self.tax_query.get_sql(wpdb_.posts, "ID")
            join_ += clauses_["join"]
            where_ += clauses_["where"]
        # end if
        if self.is_tax:
            if php_empty(lambda : post_type_):
                #// Do a fully inclusive search for currently registered post types of queried taxonomies.
                post_type_ = Array()
                taxonomies_ = php_array_keys(self.tax_query.queried_terms)
                for pt_ in get_post_types(Array({"exclude_from_search": False})):
                    object_taxonomies_ = get_taxonomies_for_attachments() if "attachment" == pt_ else get_object_taxonomies(pt_)
                    if php_array_intersect(taxonomies_, object_taxonomies_):
                        post_type_[-1] = pt_
                    # end if
                # end for
                if (not post_type_):
                    post_type_ = "any"
                elif php_count(post_type_) == 1:
                    post_type_ = post_type_[0]
                # end if
                post_status_join_ = True
            elif php_in_array("attachment", post_type_):
                post_status_join_ = True
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
            if (not (php_isset(lambda : q_["taxonomy"]))):
                for queried_taxonomy_,queried_items_ in self.tax_query.queried_terms.items():
                    if php_empty(lambda : queried_items_["terms"][0]):
                        continue
                    # end if
                    if (not php_in_array(queried_taxonomy_, Array("category", "post_tag"))):
                        q_["taxonomy"] = queried_taxonomy_
                        if "slug" == queried_items_["field"]:
                            q_["term"] = queried_items_["terms"][0]
                        else:
                            q_["term_id"] = queried_items_["terms"][0]
                        # end if
                        break
                    # end if
                # end for
            # end if
            #// 'cat', 'category_name', 'tag_id'.
            for queried_taxonomy_,queried_items_ in self.tax_query.queried_terms.items():
                if php_empty(lambda : queried_items_["terms"][0]):
                    continue
                # end if
                if "category" == queried_taxonomy_:
                    the_cat_ = get_term_by(queried_items_["field"], queried_items_["terms"][0], "category")
                    if the_cat_:
                        self.set("cat", the_cat_.term_id)
                        self.set("category_name", the_cat_.slug)
                    # end if
                    the_cat_ = None
                # end if
                if "post_tag" == queried_taxonomy_:
                    the_tag_ = get_term_by(queried_items_["field"], queried_items_["terms"][0], "post_tag")
                    if the_tag_:
                        self.set("tag_id", the_tag_.term_id)
                    # end if
                    the_tag_ = None
                # end if
            # end for
        # end if
        if (not php_empty(lambda : self.tax_query.queries)) or (not php_empty(lambda : self.meta_query.queries)):
            groupby_ = str(wpdb_.posts) + str(".ID")
        # end if
        #// Author/user stuff.
        if (not php_empty(lambda : q_["author"])) and "0" != q_["author"]:
            q_["author"] = addslashes_gpc("" + urldecode(q_["author"]))
            authors_ = array_unique(php_array_map("intval", php_preg_split("/[,\\s]+/", q_["author"])))
            for author_ in authors_:
                key_ = "author__in" if author_ > 0 else "author__not_in"
                q_[key_][-1] = abs(author_)
            # end for
            q_["author"] = php_implode(",", authors_)
        # end if
        if (not php_empty(lambda : q_["author__not_in"])):
            author__not_in_ = php_implode(",", php_array_map("absint", array_unique(q_["author__not_in"])))
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_author NOT IN (") + str(author__not_in_) + str(") ")
        elif (not php_empty(lambda : q_["author__in"])):
            author__in_ = php_implode(",", php_array_map("absint", array_unique(q_["author__in"])))
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_author IN (") + str(author__in_) + str(") ")
        # end if
        #// Author stuff for nice URLs.
        if "" != q_["author_name"]:
            if php_strpos(q_["author_name"], "/") != False:
                q_["author_name"] = php_explode("/", q_["author_name"])
                if q_["author_name"][php_count(q_["author_name"]) - 1]:
                    q_["author_name"] = q_["author_name"][php_count(q_["author_name"]) - 1]
                    pass
                else:
                    q_["author_name"] = q_["author_name"][php_count(q_["author_name"]) - 2]
                    pass
                # end if
            # end if
            q_["author_name"] = sanitize_title_for_query(q_["author_name"])
            q_["author"] = get_user_by("slug", q_["author_name"])
            if q_["author"]:
                q_["author"] = q_["author"].ID
            # end if
            whichauthor_ += str(" AND (") + str(wpdb_.posts) + str(".post_author = ") + absint(q_["author"]) + ")"
        # end if
        #// Matching by comment count.
        if (php_isset(lambda : q_["comment_count"])):
            #// Numeric comment count is converted to array format.
            if php_is_numeric(q_["comment_count"]):
                q_["comment_count"] = Array({"value": php_intval(q_["comment_count"])})
            # end if
            if (php_isset(lambda : q_["comment_count"]["value"])):
                q_["comment_count"] = php_array_merge(Array({"compare": "="}), q_["comment_count"])
                #// Fallback for invalid compare operators is '='.
                compare_operators_ = Array("=", "!=", ">", ">=", "<", "<=")
                if (not php_in_array(q_["comment_count"]["compare"], compare_operators_, True)):
                    q_["comment_count"]["compare"] = "="
                # end if
                where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".comment_count ") + str(q_["comment_count"]["compare"]) + str(" %d"), q_["comment_count"]["value"])
            # end if
        # end if
        #// MIME-Type stuff for attachment browsing.
        if (php_isset(lambda : q_["post_mime_type"])) and "" != q_["post_mime_type"]:
            whichmimetype_ = wp_post_mime_type_where(q_["post_mime_type"], wpdb_.posts)
        # end if
        where_ += search_ + whichauthor_ + whichmimetype_
        if (not php_empty(lambda : self.meta_query.queries)):
            clauses_ = self.meta_query.get_sql("post", wpdb_.posts, "ID", self)
            join_ += clauses_["join"]
            where_ += clauses_["where"]
        # end if
        rand_ = (php_isset(lambda : q_["orderby"])) and "rand" == q_["orderby"]
        if (not (php_isset(lambda : q_["order"]))):
            q_["order"] = "" if rand_ else "DESC"
        else:
            q_["order"] = "" if rand_ else self.parse_order(q_["order"])
        # end if
        #// These values of orderby should ignore the 'order' parameter.
        force_asc_ = Array("post__in", "post_name__in", "post_parent__in")
        if (php_isset(lambda : q_["orderby"])) and php_in_array(q_["orderby"], force_asc_, True):
            q_["order"] = ""
        # end if
        #// Order by.
        if php_empty(lambda : q_["orderby"]):
            #// 
            #// Boolean false or empty array blanks out ORDER BY,
            #// while leaving the value unset or otherwise empty sets the default.
            #//
            if (php_isset(lambda : q_["orderby"])) and php_is_array(q_["orderby"]) or False == q_["orderby"]:
                orderby_ = ""
            else:
                orderby_ = str(wpdb_.posts) + str(".post_date ") + q_["order"]
            # end if
        elif "none" == q_["orderby"]:
            orderby_ = ""
        else:
            orderby_array_ = Array()
            if php_is_array(q_["orderby"]):
                for _orderby_,order_ in q_["orderby"].items():
                    orderby_ = addslashes_gpc(urldecode(_orderby_))
                    parsed_ = self.parse_orderby(orderby_)
                    if (not parsed_):
                        continue
                    # end if
                    orderby_array_[-1] = parsed_ + " " + self.parse_order(order_)
                # end for
                orderby_ = php_implode(", ", orderby_array_)
            else:
                q_["orderby"] = urldecode(q_["orderby"])
                q_["orderby"] = addslashes_gpc(q_["orderby"])
                for i_,orderby_ in php_explode(" ", q_["orderby"]).items():
                    parsed_ = self.parse_orderby(orderby_)
                    #// Only allow certain values for safety.
                    if (not parsed_):
                        continue
                    # end if
                    orderby_array_[-1] = parsed_
                # end for
                orderby_ = php_implode(" " + q_["order"] + ", ", orderby_array_)
                if php_empty(lambda : orderby_):
                    orderby_ = str(wpdb_.posts) + str(".post_date ") + q_["order"]
                elif (not php_empty(lambda : q_["order"])):
                    orderby_ += str(" ") + str(q_["order"])
                # end if
            # end if
        # end if
        #// Order search results by relevance only when another "orderby" is not specified in the query.
        if (not php_empty(lambda : q_["s"])):
            search_orderby_ = ""
            if (not php_empty(lambda : q_["search_orderby_title"])) and php_empty(lambda : q_["orderby"]) and (not self.is_feed) or (php_isset(lambda : q_["orderby"])) and "relevance" == q_["orderby"]:
                search_orderby_ = self.parse_search_order(q_)
            # end if
            if (not q_["suppress_filters"]):
                #// 
                #// Filters the ORDER BY used when ordering search results.
                #// 
                #// @since 3.7.0
                #// 
                #// @param string   $search_orderby The ORDER BY clause.
                #// @param WP_Query $this           The current WP_Query instance.
                #//
                search_orderby_ = apply_filters("posts_search_orderby", search_orderby_, self)
            # end if
            if search_orderby_:
                orderby_ = search_orderby_ + ", " + orderby_ if orderby_ else search_orderby_
            # end if
        # end if
        if php_is_array(post_type_) and php_count(post_type_) > 1:
            post_type_cap_ = "multiple_post_type"
        else:
            if php_is_array(post_type_):
                post_type_ = reset(post_type_)
            # end if
            post_type_object_ = get_post_type_object(post_type_)
            if php_empty(lambda : post_type_object_):
                post_type_cap_ = post_type_
            # end if
        # end if
        if (php_isset(lambda : q_["post_password"])):
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_password = %s"), q_["post_password"])
            if php_empty(lambda : q_["perm"]):
                q_["perm"] = "readable"
            # end if
        elif (php_isset(lambda : q_["has_password"])):
            where_ += php_sprintf(str(" AND ") + str(wpdb_.posts) + str(".post_password %s ''"), "!=" if q_["has_password"] else "=")
        # end if
        if (not php_empty(lambda : q_["comment_status"])):
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".comment_status = %s "), q_["comment_status"])
        # end if
        if (not php_empty(lambda : q_["ping_status"])):
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".ping_status = %s "), q_["ping_status"])
        # end if
        if "any" == post_type_:
            in_search_post_types_ = get_post_types(Array({"exclude_from_search": False}))
            if php_empty(lambda : in_search_post_types_):
                where_ += " AND 1=0 "
            else:
                where_ += str(" AND ") + str(wpdb_.posts) + str(".post_type IN ('") + php_join("', '", php_array_map("esc_sql", in_search_post_types_)) + "')"
            # end if
        elif (not php_empty(lambda : post_type_)) and php_is_array(post_type_):
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_type IN ('") + php_join("', '", esc_sql(post_type_)) + "')"
        elif (not php_empty(lambda : post_type_)):
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_type = %s"), post_type_)
            post_type_object_ = get_post_type_object(post_type_)
        elif self.is_attachment:
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_type = 'attachment'")
            post_type_object_ = get_post_type_object("attachment")
        elif self.is_page:
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_type = 'page'")
            post_type_object_ = get_post_type_object("page")
        else:
            where_ += str(" AND ") + str(wpdb_.posts) + str(".post_type = 'post'")
            post_type_object_ = get_post_type_object("post")
        # end if
        edit_cap_ = "edit_post"
        read_cap_ = "read_post"
        if (not php_empty(lambda : post_type_object_)):
            edit_others_cap_ = post_type_object_.cap.edit_others_posts
            read_private_cap_ = post_type_object_.cap.read_private_posts
        else:
            edit_others_cap_ = "edit_others_" + post_type_cap_ + "s"
            read_private_cap_ = "read_private_" + post_type_cap_ + "s"
        # end if
        user_id_ = get_current_user_id()
        q_status_ = Array()
        if (not php_empty(lambda : q_["post_status"])):
            statuswheres_ = Array()
            q_status_ = q_["post_status"]
            if (not php_is_array(q_status_)):
                q_status_ = php_explode(",", q_status_)
            # end if
            r_status_ = Array()
            p_status_ = Array()
            e_status_ = Array()
            if php_in_array("any", q_status_):
                for status_ in get_post_stati(Array({"exclude_from_search": True})):
                    if (not php_in_array(status_, q_status_)):
                        e_status_[-1] = str(wpdb_.posts) + str(".post_status <> '") + str(status_) + str("'")
                    # end if
                # end for
            else:
                for status_ in get_post_stati():
                    if php_in_array(status_, q_status_):
                        if "private" == status_:
                            p_status_[-1] = str(wpdb_.posts) + str(".post_status = '") + str(status_) + str("'")
                        else:
                            r_status_[-1] = str(wpdb_.posts) + str(".post_status = '") + str(status_) + str("'")
                        # end if
                    # end if
                # end for
            # end if
            if php_empty(lambda : q_["perm"]) or "readable" != q_["perm"]:
                r_status_ = php_array_merge(r_status_, p_status_)
                p_status_ = None
            # end if
            if (not php_empty(lambda : e_status_)):
                statuswheres_[-1] = "(" + php_join(" AND ", e_status_) + ")"
            # end if
            if (not php_empty(lambda : r_status_)):
                if (not php_empty(lambda : q_["perm"])) and "editable" == q_["perm"] and (not current_user_can(edit_others_cap_)):
                    statuswheres_[-1] = str("(") + str(wpdb_.posts) + str(".post_author = ") + str(user_id_) + str(" ") + "AND (" + php_join(" OR ", r_status_) + "))"
                else:
                    statuswheres_[-1] = "(" + php_join(" OR ", r_status_) + ")"
                # end if
            # end if
            if (not php_empty(lambda : p_status_)):
                if (not php_empty(lambda : q_["perm"])) and "readable" == q_["perm"] and (not current_user_can(read_private_cap_)):
                    statuswheres_[-1] = str("(") + str(wpdb_.posts) + str(".post_author = ") + str(user_id_) + str(" ") + "AND (" + php_join(" OR ", p_status_) + "))"
                else:
                    statuswheres_[-1] = "(" + php_join(" OR ", p_status_) + ")"
                # end if
            # end if
            if post_status_join_:
                join_ += str(" LEFT JOIN ") + str(wpdb_.posts) + str(" AS p2 ON (") + str(wpdb_.posts) + str(".post_parent = p2.ID) ")
                for index_,statuswhere_ in statuswheres_.items():
                    statuswheres_[index_] = str("(") + str(statuswhere_) + str(" OR (") + str(wpdb_.posts) + str(".post_status = 'inherit' AND ") + php_str_replace(wpdb_.posts, "p2", statuswhere_) + "))"
                # end for
            # end if
            where_status_ = php_implode(" OR ", statuswheres_)
            if (not php_empty(lambda : where_status_)):
                where_ += str(" AND (") + str(where_status_) + str(")")
            # end if
        elif (not self.is_singular):
            where_ += str(" AND (") + str(wpdb_.posts) + str(".post_status = 'publish'")
            #// Add public states.
            public_states_ = get_post_stati(Array({"public": True}))
            for state_ in public_states_:
                if "publish" == state_:
                    continue
                # end if
                where_ += str(" OR ") + str(wpdb_.posts) + str(".post_status = '") + str(state_) + str("'")
            # end for
            if self.is_admin:
                #// Add protected states that should show in the admin all list.
                admin_all_states_ = get_post_stati(Array({"protected": True, "show_in_admin_all_list": True}))
                for state_ in admin_all_states_:
                    where_ += str(" OR ") + str(wpdb_.posts) + str(".post_status = '") + str(state_) + str("'")
                # end for
            # end if
            if is_user_logged_in():
                #// Add private states that are limited to viewing by the author of a post or someone who has caps to read private states.
                private_states_ = get_post_stati(Array({"private": True}))
                for state_ in private_states_:
                    where_ += str(" OR ") + str(wpdb_.posts) + str(".post_status = '") + str(state_) + str("'") if current_user_can(read_private_cap_) else str(" OR ") + str(wpdb_.posts) + str(".post_author = ") + str(user_id_) + str(" AND ") + str(wpdb_.posts) + str(".post_status = '") + str(state_) + str("'")
                # end for
            # end if
            where_ += ")"
        # end if
        #// 
        #// Apply filters on where and join prior to paging so that any
        #// manipulations to them are reflected in the paging by day queries.
        #//
        if (not q_["suppress_filters"]):
            #// 
            #// Filters the WHERE clause of the query.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string   $where The WHERE clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            where_ = apply_filters_ref_array("posts_where", Array(where_, self))
            #// 
            #// Filters the JOIN clause of the query.
            #// 
            #// @since 1.5.0
            #// 
            #// @param string   $join  The JOIN clause of the query.
            #// @param WP_Query $this The WP_Query instance (passed by reference).
            #//
            join_ = apply_filters_ref_array("posts_join", Array(join_, self))
        # end if
        #// Paging.
        if php_empty(lambda : q_["nopaging"]) and (not self.is_singular):
            page_ = absint(q_["paged"])
            if (not page_):
                page_ = 1
            # end if
            #// If 'offset' is provided, it takes precedence over 'paged'.
            if (php_isset(lambda : q_["offset"])) and php_is_numeric(q_["offset"]):
                q_["offset"] = absint(q_["offset"])
                pgstrt_ = q_["offset"] + ", "
            else:
                pgstrt_ = absint(page_ - 1 * q_["posts_per_page"]) + ", "
            # end if
            limits_ = "LIMIT " + pgstrt_ + q_["posts_per_page"]
        # end if
        #// Comments feeds.
        if self.is_comment_feed and (not self.is_singular):
            if self.is_archive or self.is_search:
                cjoin_ = str("JOIN ") + str(wpdb_.posts) + str(" ON (") + str(wpdb_.comments) + str(".comment_post_ID = ") + str(wpdb_.posts) + str(".ID) ") + str(join_) + str(" ")
                cwhere_ = str("WHERE comment_approved = '1' ") + str(where_)
                cgroupby_ = str(wpdb_.comments) + str(".comment_id")
            else:
                #// Other non-singular, e.g. front.
                cjoin_ = str("JOIN ") + str(wpdb_.posts) + str(" ON ( ") + str(wpdb_.comments) + str(".comment_post_ID = ") + str(wpdb_.posts) + str(".ID )")
                cwhere_ = "WHERE ( post_status = 'publish' OR ( post_status = 'inherit' AND post_type = 'attachment' ) ) AND comment_approved = '1'"
                cgroupby_ = ""
            # end if
            if (not q_["suppress_filters"]):
                #// 
                #// Filters the JOIN clause of the comments feed query before sending.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string   $cjoin The JOIN clause of the query.
                #// @param WP_Query $this The WP_Query instance (passed by reference).
                #//
                cjoin_ = apply_filters_ref_array("comment_feed_join", Array(cjoin_, self))
                #// 
                #// Filters the WHERE clause of the comments feed query before sending.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string   $cwhere The WHERE clause of the query.
                #// @param WP_Query $this   The WP_Query instance (passed by reference).
                #//
                cwhere_ = apply_filters_ref_array("comment_feed_where", Array(cwhere_, self))
                #// 
                #// Filters the GROUP BY clause of the comments feed query before sending.
                #// 
                #// @since 2.2.0
                #// 
                #// @param string   $cgroupby The GROUP BY clause of the query.
                #// @param WP_Query $this     The WP_Query instance (passed by reference).
                #//
                cgroupby_ = apply_filters_ref_array("comment_feed_groupby", Array(cgroupby_, self))
                #// 
                #// Filters the ORDER BY clause of the comments feed query before sending.
                #// 
                #// @since 2.8.0
                #// 
                #// @param string   $corderby The ORDER BY clause of the query.
                #// @param WP_Query $this     The WP_Query instance (passed by reference).
                #//
                corderby_ = apply_filters_ref_array("comment_feed_orderby", Array("comment_date_gmt DESC", self))
                #// 
                #// Filters the LIMIT clause of the comments feed query before sending.
                #// 
                #// @since 2.8.0
                #// 
                #// @param string   $climits The JOIN clause of the query.
                #// @param WP_Query $this    The WP_Query instance (passed by reference).
                #//
                climits_ = apply_filters_ref_array("comment_feed_limits", Array("LIMIT " + get_option("posts_per_rss"), self))
            # end if
            cgroupby_ = "GROUP BY " + cgroupby_ if (not php_empty(lambda : cgroupby_)) else ""
            corderby_ = "ORDER BY " + corderby_ if (not php_empty(lambda : corderby_)) else ""
            climits_ = climits_ if (not php_empty(lambda : climits_)) else ""
            comments_ = wpdb_.get_results(str("SELECT ") + str(distinct_) + str(" ") + str(wpdb_.comments) + str(".* FROM ") + str(wpdb_.comments) + str(" ") + str(cjoin_) + str(" ") + str(cwhere_) + str(" ") + str(cgroupby_) + str(" ") + str(corderby_) + str(" ") + str(climits_))
            #// Convert to WP_Comment.
            self.comments = php_array_map("get_comment", comments_)
            self.comment_count = php_count(self.comments)
            post_ids_ = Array()
            for comment_ in self.comments:
                post_ids_[-1] = php_int(comment_.comment_post_ID)
            # end for
            post_ids_ = php_join(",", post_ids_)
            join_ = ""
            if post_ids_:
                where_ = str("AND ") + str(wpdb_.posts) + str(".ID IN (") + str(post_ids_) + str(") ")
            else:
                where_ = "AND 0"
            # end if
        # end if
        pieces_ = Array("where", "groupby", "join", "orderby", "distinct", "fields", "limits")
        #// 
        #// Apply post-paging filters on where and join. Only plugins that
        #// manipulate paging queries should use these hooks.
        #//
        if (not q_["suppress_filters"]):
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
            where_ = apply_filters_ref_array("posts_where_paged", Array(where_, self))
            #// 
            #// Filters the GROUP BY clause of the query.
            #// 
            #// @since 2.0.0
            #// 
            #// @param string   $groupby The GROUP BY clause of the query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            groupby_ = apply_filters_ref_array("posts_groupby", Array(groupby_, self))
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
            join_ = apply_filters_ref_array("posts_join_paged", Array(join_, self))
            #// 
            #// Filters the ORDER BY clause of the query.
            #// 
            #// @since 1.5.1
            #// 
            #// @param string   $orderby The ORDER BY clause of the query.
            #// @param WP_Query $this    The WP_Query instance (passed by reference).
            #//
            orderby_ = apply_filters_ref_array("posts_orderby", Array(orderby_, self))
            #// 
            #// Filters the DISTINCT clause of the query.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $distinct The DISTINCT clause of the query.
            #// @param WP_Query $this     The WP_Query instance (passed by reference).
            #//
            distinct_ = apply_filters_ref_array("posts_distinct", Array(distinct_, self))
            #// 
            #// Filters the LIMIT clause of the query.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $limits The LIMIT clause of the query.
            #// @param WP_Query $this   The WP_Query instance (passed by reference).
            #//
            limits_ = apply_filters_ref_array("post_limits", Array(limits_, self))
            #// 
            #// Filters the SELECT clause of the query.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $fields The SELECT clause of the query.
            #// @param WP_Query $this   The WP_Query instance (passed by reference).
            #//
            fields_ = apply_filters_ref_array("posts_fields", Array(fields_, self))
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
            clauses_ = apply_filters_ref_array("posts_clauses", Array(php_compact(pieces_), self))
            where_ = clauses_["where"] if (php_isset(lambda : clauses_["where"])) else ""
            groupby_ = clauses_["groupby"] if (php_isset(lambda : clauses_["groupby"])) else ""
            join_ = clauses_["join"] if (php_isset(lambda : clauses_["join"])) else ""
            orderby_ = clauses_["orderby"] if (php_isset(lambda : clauses_["orderby"])) else ""
            distinct_ = clauses_["distinct"] if (php_isset(lambda : clauses_["distinct"])) else ""
            fields_ = clauses_["fields"] if (php_isset(lambda : clauses_["fields"])) else ""
            limits_ = clauses_["limits"] if (php_isset(lambda : clauses_["limits"])) else ""
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
        do_action("posts_selection", where_ + groupby_ + orderby_ + limits_ + join_)
        #// 
        #// Filters again for the benefit of caching plugins.
        #// Regular plugins should use the hooks above.
        #//
        if (not q_["suppress_filters"]):
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
            where_ = apply_filters_ref_array("posts_where_request", Array(where_, self))
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
            groupby_ = apply_filters_ref_array("posts_groupby_request", Array(groupby_, self))
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
            join_ = apply_filters_ref_array("posts_join_request", Array(join_, self))
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
            orderby_ = apply_filters_ref_array("posts_orderby_request", Array(orderby_, self))
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
            distinct_ = apply_filters_ref_array("posts_distinct_request", Array(distinct_, self))
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
            fields_ = apply_filters_ref_array("posts_fields_request", Array(fields_, self))
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
            limits_ = apply_filters_ref_array("post_limits_request", Array(limits_, self))
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
            clauses_ = apply_filters_ref_array("posts_clauses_request", Array(php_compact(pieces_), self))
            where_ = clauses_["where"] if (php_isset(lambda : clauses_["where"])) else ""
            groupby_ = clauses_["groupby"] if (php_isset(lambda : clauses_["groupby"])) else ""
            join_ = clauses_["join"] if (php_isset(lambda : clauses_["join"])) else ""
            orderby_ = clauses_["orderby"] if (php_isset(lambda : clauses_["orderby"])) else ""
            distinct_ = clauses_["distinct"] if (php_isset(lambda : clauses_["distinct"])) else ""
            fields_ = clauses_["fields"] if (php_isset(lambda : clauses_["fields"])) else ""
            limits_ = clauses_["limits"] if (php_isset(lambda : clauses_["limits"])) else ""
        # end if
        if (not php_empty(lambda : groupby_)):
            groupby_ = "GROUP BY " + groupby_
        # end if
        if (not php_empty(lambda : orderby_)):
            orderby_ = "ORDER BY " + orderby_
        # end if
        found_rows_ = ""
        if (not q_["no_found_rows"]) and (not php_empty(lambda : limits_)):
            found_rows_ = "SQL_CALC_FOUND_ROWS"
        # end if
        old_request_ = str("SELECT ") + str(found_rows_) + str(" ") + str(distinct_) + str(" ") + str(fields_) + str(" FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" WHERE 1=1 ") + str(where_) + str(" ") + str(groupby_) + str(" ") + str(orderby_) + str(" ") + str(limits_)
        self.request = old_request_
        if (not q_["suppress_filters"]):
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
        if "ids" == q_["fields"]:
            if None == self.posts:
                self.posts = wpdb_.get_col(self.request)
            # end if
            self.posts = php_array_map("intval", self.posts)
            self.post_count = php_count(self.posts)
            self.set_found_posts(q_, limits_)
            return self.posts
        # end if
        if "id=>parent" == q_["fields"]:
            if None == self.posts:
                self.posts = wpdb_.get_results(self.request)
            # end if
            self.post_count = php_count(self.posts)
            self.set_found_posts(q_, limits_)
            r_ = Array()
            for key_,post_ in self.posts.items():
                self.posts[key_].ID = php_int(post_.ID)
                self.posts[key_].post_parent = php_int(post_.post_parent)
                r_[php_int(post_.ID)] = php_int(post_.post_parent)
            # end for
            return r_
        # end if
        if None == self.posts:
            split_the_query_ = old_request_ == self.request and str(wpdb_.posts) + str(".*") == fields_ and (not php_empty(lambda : limits_)) and q_["posts_per_page"] < 500
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
            split_the_query_ = apply_filters("split_the_query", split_the_query_, self)
            if split_the_query_:
                #// First get the IDs and then fill in the objects.
                self.request = str("SELECT ") + str(found_rows_) + str(" ") + str(distinct_) + str(" ") + str(wpdb_.posts) + str(".ID FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" WHERE 1=1 ") + str(where_) + str(" ") + str(groupby_) + str(" ") + str(orderby_) + str(" ") + str(limits_)
                #// 
                #// Filters the Post IDs SQL request before sending.
                #// 
                #// @since 3.4.0
                #// 
                #// @param string   $request The post ID request.
                #// @param WP_Query $this    The WP_Query instance.
                #//
                self.request = apply_filters("posts_request_ids", self.request, self)
                ids_ = wpdb_.get_col(self.request)
                if ids_:
                    self.posts = ids_
                    self.set_found_posts(q_, limits_)
                    _prime_post_caches(ids_, q_["update_post_term_cache"], q_["update_post_meta_cache"])
                else:
                    self.posts = Array()
                # end if
            else:
                self.posts = wpdb_.get_results(self.request)
                self.set_found_posts(q_, limits_)
            # end if
        # end if
        #// Convert to WP_Post objects.
        if self.posts:
            self.posts = php_array_map("get_post", self.posts)
        # end if
        if (not q_["suppress_filters"]):
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
            cjoin_ = apply_filters_ref_array("comment_feed_join", Array("", self))
            #// This filter is documented in wp-includes/query.php
            cwhere_ = apply_filters_ref_array("comment_feed_where", Array(str("WHERE comment_post_ID = '") + str(self.posts[0].ID) + str("' AND comment_approved = '1'"), self))
            #// This filter is documented in wp-includes/query.php
            cgroupby_ = apply_filters_ref_array("comment_feed_groupby", Array("", self))
            cgroupby_ = "GROUP BY " + cgroupby_ if (not php_empty(lambda : cgroupby_)) else ""
            #// This filter is documented in wp-includes/query.php
            corderby_ = apply_filters_ref_array("comment_feed_orderby", Array("comment_date_gmt DESC", self))
            corderby_ = "ORDER BY " + corderby_ if (not php_empty(lambda : corderby_)) else ""
            #// This filter is documented in wp-includes/query.php
            climits_ = apply_filters_ref_array("comment_feed_limits", Array("LIMIT " + get_option("posts_per_rss"), self))
            comments_request_ = str("SELECT ") + str(wpdb_.comments) + str(".* FROM ") + str(wpdb_.comments) + str(" ") + str(cjoin_) + str(" ") + str(cwhere_) + str(" ") + str(cgroupby_) + str(" ") + str(corderby_) + str(" ") + str(climits_)
            comments_ = wpdb_.get_results(comments_request_)
            #// Convert to WP_Comment.
            self.comments = php_array_map("get_comment", comments_)
            self.comment_count = php_count(self.comments)
        # end if
        #// Check post status to determine if post should be displayed.
        if (not php_empty(lambda : self.posts)) and self.is_single or self.is_page:
            status_ = get_post_status(self.posts[0])
            if "attachment" == self.posts[0].post_type and 0 == php_int(self.posts[0].post_parent):
                self.is_page = False
                self.is_single = True
                self.is_attachment = True
            # end if
            #// If the post_status was specifically requested, let it pass through.
            if (not php_in_array(status_, q_status_)):
                post_status_obj_ = get_post_status_object(status_)
                if post_status_obj_ and (not post_status_obj_.public):
                    if (not is_user_logged_in()):
                        #// User must be logged in to view unpublished posts.
                        self.posts = Array()
                    else:
                        if post_status_obj_.protected:
                            #// User must have edit permissions on the draft to preview.
                            if (not current_user_can(edit_cap_, self.posts[0].ID)):
                                self.posts = Array()
                            else:
                                self.is_preview = True
                                if "future" != status_:
                                    self.posts[0].post_date = current_time("mysql")
                                # end if
                            # end if
                        elif post_status_obj_.private:
                            if (not current_user_can(read_cap_, self.posts[0].ID)):
                                self.posts = Array()
                            # end if
                        else:
                            self.posts = Array()
                        # end if
                    # end if
                elif (not post_status_obj_):
                    #// Post status is not registered, assume it's not public.
                    if (not current_user_can(edit_cap_, self.posts[0].ID)):
                        self.posts = Array()
                    # end if
                # end if
            # end if
            if self.is_preview and self.posts and current_user_can(edit_cap_, self.posts[0].ID):
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
        sticky_posts_ = get_option("sticky_posts")
        if self.is_home and page_ <= 1 and php_is_array(sticky_posts_) and (not php_empty(lambda : sticky_posts_)) and (not q_["ignore_sticky_posts"]):
            num_posts_ = php_count(self.posts)
            sticky_offset_ = 0
            #// Loop over posts and relocate stickies to the front.
            i_ = 0
            while i_ < num_posts_:
                
                if php_in_array(self.posts[i_].ID, sticky_posts_):
                    sticky_post_ = self.posts[i_]
                    #// Remove sticky from current position.
                    array_splice(self.posts, i_, 1)
                    #// Move to front, after other stickies.
                    array_splice(self.posts, sticky_offset_, 0, Array(sticky_post_))
                    #// Increment the sticky offset. The next sticky will be placed at this offset.
                    sticky_offset_ += 1
                    #// Remove post from sticky posts array.
                    offset_ = php_array_search(sticky_post_.ID, sticky_posts_)
                    sticky_posts_[offset_] = None
                # end if
                i_ += 1
            # end while
            #// If any posts have been excluded specifically, Ignore those that are sticky.
            if (not php_empty(lambda : sticky_posts_)) and (not php_empty(lambda : q_["post__not_in"])):
                sticky_posts_ = php_array_diff(sticky_posts_, q_["post__not_in"])
            # end if
            #// Fetch sticky posts that weren't in the query results.
            if (not php_empty(lambda : sticky_posts_)):
                stickies_ = get_posts(Array({"post__in": sticky_posts_, "post_type": post_type_, "post_status": "publish", "nopaging": True}))
                for sticky_post_ in stickies_:
                    array_splice(self.posts, sticky_offset_, 0, Array(sticky_post_))
                    sticky_offset_ += 1
                # end for
            # end if
        # end if
        #// If comments have been fetched as part of the query, make sure comment meta lazy-loading is set up.
        if (not php_empty(lambda : self.comments)):
            wp_queue_comments_for_comment_meta_lazyload(self.comments)
        # end if
        if (not q_["suppress_filters"]):
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
            if q_["cache_results"]:
                update_post_caches(self.posts, post_type_, q_["update_post_term_cache"], q_["update_post_meta_cache"])
            # end if
            self.post = reset(self.posts)
        else:
            self.post_count = 0
            self.posts = Array()
        # end if
        if q_["lazy_load_term_meta"]:
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
    def set_found_posts(self, q_=None, limits_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// Bail if posts is an empty array. Continue if posts is an empty string,
        #// null, or false to accommodate caching plugins that fill posts later.
        if q_["no_found_rows"] or php_is_array(self.posts) and (not self.posts):
            return
        # end if
        if (not php_empty(lambda : limits_)):
            #// 
            #// Filters the query to run for retrieving the found posts.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string   $found_posts The query to run to find the found posts.
            #// @param WP_Query $this        The WP_Query instance (passed by reference).
            #//
            self.found_posts = wpdb_.get_var(apply_filters_ref_array("found_posts_query", Array("SELECT FOUND_ROWS()", self)))
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
        if (not php_empty(lambda : limits_)):
            self.max_num_pages = ceil(self.found_posts / q_["posts_per_page"])
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
        
        
        global post_
        php_check_if_defined("post_")
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
        post_ = self.next_post()
        self.setup_postdata(post_)
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
        
        
        global comment_
        php_check_if_defined("comment_")
        comment_ = self.next_comment()
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
    def query(self, query_=None):
        
        
        self.init()
        self.query = wp_parse_args(query_)
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
                    term_ = get_term(self.get("cat"), "category")
                elif self.get("category_name"):
                    term_ = get_term_by("slug", self.get("category_name"), "category")
                # end if
            elif self.is_tag:
                if self.get("tag_id"):
                    term_ = get_term(self.get("tag_id"), "post_tag")
                elif self.get("tag"):
                    term_ = get_term_by("slug", self.get("tag"), "post_tag")
                # end if
            else:
                #// For other tax queries, grab the first term from the first clause.
                if (not php_empty(lambda : self.tax_query.queried_terms)):
                    queried_taxonomies_ = php_array_keys(self.tax_query.queried_terms)
                    matched_taxonomy_ = reset(queried_taxonomies_)
                    query_ = self.tax_query.queried_terms[matched_taxonomy_]
                    if (not php_empty(lambda : query_["terms"])):
                        if "term_id" == query_["field"]:
                            term_ = get_term(reset(query_["terms"]), matched_taxonomy_)
                        else:
                            term_ = get_term_by(query_["field"], reset(query_["terms"]), matched_taxonomy_)
                        # end if
                    # end if
                # end if
            # end if
            if (not php_empty(lambda : term_)) and (not is_wp_error(term_)):
                self.queried_object = term_
                self.queried_object_id = php_int(term_.term_id)
                if self.is_category and "category" == self.queried_object.taxonomy:
                    _make_cat_compat(self.queried_object)
                # end if
            # end if
        elif self.is_post_type_archive:
            post_type_ = self.get("post_type")
            if php_is_array(post_type_):
                post_type_ = reset(post_type_)
            # end if
            self.queried_object = get_post_type_object(post_type_)
        elif self.is_posts_page:
            page_for_posts_ = get_option("page_for_posts")
            self.queried_object = get_post(page_for_posts_)
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
    def __init__(self, query_=""):
        
        
        if (not php_empty(lambda : query_)):
            self.query(query_)
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
    def __get(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return self.name_
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
    def __isset(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return (php_isset(lambda : self.name_))
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
    def __call(self, name_=None, arguments_=None):
        
        
        if php_in_array(name_, self.compat_methods):
            return self.name_(arguments_)
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
    def is_post_type_archive(self, post_types_=""):
        
        
        if php_empty(lambda : post_types_) or (not self.is_post_type_archive):
            return php_bool(self.is_post_type_archive)
        # end if
        post_type_ = self.get("post_type")
        if php_is_array(post_type_):
            post_type_ = reset(post_type_)
        # end if
        post_type_object_ = get_post_type_object(post_type_)
        return php_in_array(post_type_object_.name, post_types_)
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
    def is_attachment(self, attachment_=""):
        
        
        if (not self.is_attachment):
            return False
        # end if
        if php_empty(lambda : attachment_):
            return True
        # end if
        attachment_ = php_array_map("strval", attachment_)
        post_obj_ = self.get_queried_object()
        if php_in_array(php_str(post_obj_.ID), attachment_):
            return True
        elif php_in_array(post_obj_.post_title, attachment_):
            return True
        elif php_in_array(post_obj_.post_name, attachment_):
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
    def is_author(self, author_=""):
        
        
        if (not self.is_author):
            return False
        # end if
        if php_empty(lambda : author_):
            return True
        # end if
        author_obj_ = self.get_queried_object()
        author_ = php_array_map("strval", author_)
        if php_in_array(php_str(author_obj_.ID), author_):
            return True
        elif php_in_array(author_obj_.nickname, author_):
            return True
        elif php_in_array(author_obj_.user_nicename, author_):
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
    def is_category(self, category_=""):
        
        
        if (not self.is_category):
            return False
        # end if
        if php_empty(lambda : category_):
            return True
        # end if
        cat_obj_ = self.get_queried_object()
        category_ = php_array_map("strval", category_)
        if php_in_array(php_str(cat_obj_.term_id), category_):
            return True
        elif php_in_array(cat_obj_.name, category_):
            return True
        elif php_in_array(cat_obj_.slug, category_):
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
    def is_tag(self, tag_=""):
        
        
        if (not self.is_tag):
            return False
        # end if
        if php_empty(lambda : tag_):
            return True
        # end if
        tag_obj_ = self.get_queried_object()
        tag_ = php_array_map("strval", tag_)
        if php_in_array(php_str(tag_obj_.term_id), tag_):
            return True
        elif php_in_array(tag_obj_.name, tag_):
            return True
        elif php_in_array(tag_obj_.slug, tag_):
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
    def is_tax(self, taxonomy_="", term_=""):
        
        
        global wp_taxonomies_
        php_check_if_defined("wp_taxonomies_")
        if (not self.is_tax):
            return False
        # end if
        if php_empty(lambda : taxonomy_):
            return True
        # end if
        queried_object_ = self.get_queried_object()
        tax_array_ = php_array_intersect(php_array_keys(wp_taxonomies_), taxonomy_)
        term_array_ = term_
        #// Check that the taxonomy matches.
        if (not (php_isset(lambda : queried_object_.taxonomy)) and php_count(tax_array_) and php_in_array(queried_object_.taxonomy, tax_array_)):
            return False
        # end if
        #// Only a taxonomy provided.
        if php_empty(lambda : term_):
            return True
        # end if
        return (php_isset(lambda : queried_object_.term_id)) and php_count(php_array_intersect(Array(queried_object_.term_id, queried_object_.name, queried_object_.slug), term_array_))
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
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.5.0")
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
    def is_feed(self, feeds_=""):
        
        
        if php_empty(lambda : feeds_) or (not self.is_feed):
            return php_bool(self.is_feed)
        # end if
        qv_ = self.get("feed")
        if "feed" == qv_:
            qv_ = get_default_feed()
        # end if
        return php_in_array(qv_, feeds_)
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
    def is_page(self, page_=""):
        
        
        if (not self.is_page):
            return False
        # end if
        if php_empty(lambda : page_):
            return True
        # end if
        page_obj_ = self.get_queried_object()
        page_ = php_array_map("strval", page_)
        if php_in_array(php_str(page_obj_.ID), page_):
            return True
        elif php_in_array(page_obj_.post_title, page_):
            return True
        elif php_in_array(page_obj_.post_name, page_):
            return True
        else:
            for pagepath_ in page_:
                if (not php_strpos(pagepath_, "/")):
                    continue
                # end if
                pagepath_obj_ = get_page_by_path(pagepath_)
                if pagepath_obj_ and pagepath_obj_.ID == page_obj_.ID:
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
    def is_single(self, post_=""):
        
        
        if (not self.is_single):
            return False
        # end if
        if php_empty(lambda : post_):
            return True
        # end if
        post_obj_ = self.get_queried_object()
        post_ = php_array_map("strval", post_)
        if php_in_array(php_str(post_obj_.ID), post_):
            return True
        elif php_in_array(post_obj_.post_title, post_):
            return True
        elif php_in_array(post_obj_.post_name, post_):
            return True
        else:
            for postpath_ in post_:
                if (not php_strpos(postpath_, "/")):
                    continue
                # end if
                postpath_obj_ = get_page_by_path(postpath_, OBJECT, post_obj_.post_type)
                if postpath_obj_ and postpath_obj_.ID == post_obj_.ID:
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
    def is_singular(self, post_types_=""):
        
        
        if php_empty(lambda : post_types_) or (not self.is_singular):
            return php_bool(self.is_singular)
        # end if
        post_obj_ = self.get_queried_object()
        return php_in_array(post_obj_.post_type, post_types_)
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
        
        
        global wp_the_query_
        php_check_if_defined("wp_the_query_")
        return wp_the_query_ == self
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
    def setup_postdata(self, post_=None):
        
        
        global id_
        global authordata_
        global currentday_
        global currentmonth_
        global page_
        global pages_
        global multipage_
        global more_
        global numpages_
        php_check_if_defined("id_","authordata_","currentday_","currentmonth_","page_","pages_","multipage_","more_","numpages_")
        if (not type(post_).__name__ == "WP_Post"):
            post_ = get_post(post_)
        # end if
        if (not post_):
            return
        # end if
        elements_ = self.generate_postdata(post_)
        if False == elements_:
            return
        # end if
        id_ = elements_["id"]
        authordata_ = elements_["authordata"]
        currentday_ = elements_["currentday"]
        currentmonth_ = elements_["currentmonth"]
        page_ = elements_["page"]
        pages_ = elements_["pages"]
        multipage_ = elements_["multipage"]
        more_ = elements_["more"]
        numpages_ = elements_["numpages"]
        #// 
        #// Fires once the post data has been setup.
        #// 
        #// @since 2.8.0
        #// @since 4.1.0 Introduced `$this` parameter.
        #// 
        #// @param WP_Post  $post The Post object (passed by reference).
        #// @param WP_Query $this The current Query object (passed by reference).
        #//
        do_action_ref_array("the_post", Array(post_, self))
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
    def generate_postdata(self, post_=None):
        
        
        if (not type(post_).__name__ == "WP_Post"):
            post_ = get_post(post_)
        # end if
        if (not post_):
            return False
        # end if
        id_ = php_int(post_.ID)
        authordata_ = get_userdata(post_.post_author)
        currentday_ = mysql2date("d.m.y", post_.post_date, False)
        currentmonth_ = mysql2date("m", post_.post_date, False)
        numpages_ = 1
        multipage_ = 0
        page_ = self.get("page")
        if (not page_):
            page_ = 1
        # end if
        #// 
        #// Force full post content when viewing the permalink for the $post,
        #// or when on an RSS feed. Otherwise respect the 'more' tag.
        #//
        if get_queried_object_id() == post_.ID and self.is_page() or self.is_single():
            more_ = 1
        elif self.is_feed():
            more_ = 1
        else:
            more_ = 0
        # end if
        content_ = post_.post_content
        if False != php_strpos(content_, "<!--nextpage-->"):
            content_ = php_str_replace("\n<!--nextpage-->\n", "<!--nextpage-->", content_)
            content_ = php_str_replace("\n<!--nextpage-->", "<!--nextpage-->", content_)
            content_ = php_str_replace("<!--nextpage-->\n", "<!--nextpage-->", content_)
            #// Remove the nextpage block delimiters, to avoid invalid block structures in the split content.
            content_ = php_str_replace("<!-- wp:nextpage -->", "", content_)
            content_ = php_str_replace("<!-- /wp:nextpage -->", "", content_)
            #// Ignore nextpage at the beginning of the content.
            if 0 == php_strpos(content_, "<!--nextpage-->"):
                content_ = php_substr(content_, 15)
            # end if
            pages_ = php_explode("<!--nextpage-->", content_)
        else:
            pages_ = Array(post_.post_content)
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
        pages_ = apply_filters("content_pagination", pages_, post_)
        numpages_ = php_count(pages_)
        if numpages_ > 1:
            if page_ > 1:
                more_ = 1
            # end if
            multipage_ = 1
        else:
            multipage_ = 0
        # end if
        elements_ = php_compact("id_", "authordata_", "currentday_", "currentmonth_", "page_", "pages_", "multipage_", "more_", "numpages_")
        return elements_
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
    def lazyload_term_meta(self, check_=None, term_id_=None):
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.5.0")
        return check_
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
    def lazyload_comment_meta(self, check_=None, comment_id_=None):
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.5.0")
        return check_
    # end def lazyload_comment_meta
# end class WP_Query
