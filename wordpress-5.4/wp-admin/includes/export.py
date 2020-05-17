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
#// WordPress Export Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Version number for the export format.
#// 
#// Bump this when something changes that might affect compatibility.
#// 
#// @since 2.5.0
#//
php_define("WXR_VERSION", "1.2")
#// 
#// Generates the WXR export file for download.
#// 
#// Default behavior is to export all content, however, note that post content will only
#// be exported for post types with the `can_export` argument enabled. Any posts with the
#// 'auto-draft' status will be skipped.
#// 
#// @since 2.1.0
#// 
#// @global wpdb    $wpdb WordPress database abstraction object.
#// @global WP_Post $post Global post object.
#// 
#// @param array $args {
#// Optional. Arguments for generating the WXR export file for download. Default empty array.
#// 
#// @type string $content        Type of content to export. If set, only the post content of this post type
#// will be exported. Accepts 'all', 'post', 'page', 'attachment', or a defined
#// custom post. If an invalid custom post type is supplied, every post type for
#// which `can_export` is enabled will be exported instead. If a valid custom post
#// type is supplied but `can_export` is disabled, then 'posts' will be exported
#// instead. When 'all' is supplied, only post types with `can_export` enabled will
#// be exported. Default 'all'.
#// @type string $author         Author to export content for. Only used when `$content` is 'post', 'page', or
#// 'attachment'. Accepts false (all) or a specific author ID. Default false (all).
#// @type string $category       Category (slug) to export content for. Used only when `$content` is 'post'. If
#// set, only post content assigned to `$category` will be exported. Accepts false
#// or a specific category slug. Default is false (all categories).
#// @type string $start_date     Start date to export content from. Expected date format is 'Y-m-d'. Used only
#// when `$content` is 'post', 'page' or 'attachment'. Default false (since the
#// beginning of time).
#// @type string $end_date       End date to export content to. Expected date format is 'Y-m-d'. Used only when
#// `$content` is 'post', 'page' or 'attachment'. Default false (latest publish date).
#// @type string $status         Post status to export posts for. Used only when `$content` is 'post' or 'page'.
#// Accepts false (all statuses except 'auto-draft'), or a specific status, i.e.
#// 'publish', 'pending', 'draft', 'auto-draft', 'future', 'private', 'inherit', or
#// 'trash'. Default false (all statuses except 'auto-draft').
#// }
#//
def export_wp(args_=None, *_args_):
    
    
    global wpdb_
    global post_
    php_check_if_defined("wpdb_","post_")
    defaults_ = Array({"content": "all", "author": False, "category": False, "start_date": False, "end_date": False, "status": False})
    args_ = wp_parse_args(args_, defaults_)
    #// 
    #// Fires at the beginning of an export, before any headers are sent.
    #// 
    #// @since 2.3.0
    #// 
    #// @param array $args An array of export arguments.
    #//
    do_action("export_wp", args_)
    sitename_ = sanitize_key(get_bloginfo("name"))
    if (not php_empty(lambda : sitename_)):
        sitename_ += "."
    # end if
    date_ = gmdate("Y-m-d")
    wp_filename_ = sitename_ + "WordPress." + date_ + ".xml"
    #// 
    #// Filters the export filename.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $wp_filename The name of the file for download.
    #// @param string $sitename    The site name.
    #// @param string $date        Today's date, formatted.
    #//
    filename_ = apply_filters("export_wp_filename", wp_filename_, sitename_, date_)
    php_header("Content-Description: File Transfer")
    php_header("Content-Disposition: attachment; filename=" + filename_)
    php_header("Content-Type: text/xml; charset=" + get_option("blog_charset"), True)
    if "all" != args_["content"] and post_type_exists(args_["content"]):
        ptype_ = get_post_type_object(args_["content"])
        if (not ptype_.can_export):
            args_["content"] = "post"
        # end if
        where_ = wpdb_.prepare(str(wpdb_.posts) + str(".post_type = %s"), args_["content"])
    else:
        post_types_ = get_post_types(Array({"can_export": True}))
        esses_ = array_fill(0, php_count(post_types_), "%s")
        #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.UnfinishedPrepare
        where_ = wpdb_.prepare(str(wpdb_.posts) + str(".post_type IN (") + php_implode(",", esses_) + ")", post_types_)
    # end if
    if args_["status"] and "post" == args_["content"] or "page" == args_["content"]:
        where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_status = %s"), args_["status"])
    else:
        where_ += str(" AND ") + str(wpdb_.posts) + str(".post_status != 'auto-draft'")
    # end if
    join_ = ""
    if args_["category"] and "post" == args_["content"]:
        term_ = term_exists(args_["category"], "category")
        if term_:
            join_ = str("INNER JOIN ") + str(wpdb_.term_relationships) + str(" ON (") + str(wpdb_.posts) + str(".ID = ") + str(wpdb_.term_relationships) + str(".object_id)")
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.term_relationships) + str(".term_taxonomy_id = %d"), term_["term_taxonomy_id"])
        # end if
    # end if
    if "post" == args_["content"] or "page" == args_["content"] or "attachment" == args_["content"]:
        if args_["author"]:
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_author = %d"), args_["author"])
        # end if
        if args_["start_date"]:
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_date >= %s"), gmdate("Y-m-d", strtotime(args_["start_date"])))
        # end if
        if args_["end_date"]:
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.posts) + str(".post_date < %s"), gmdate("Y-m-d", strtotime("+1 month", strtotime(args_["end_date"]))))
        # end if
    # end if
    #// Grab a snapshot of post IDs, just in case it changes during the export.
    post_ids_ = wpdb_.get_col(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" WHERE ") + str(where_))
    #// 
    #// Get the requested terms ready, empty unless posts filtered by category
    #// or all content.
    #//
    cats_ = Array()
    tags_ = Array()
    terms_ = Array()
    if (php_isset(lambda : term_)) and term_:
        cat_ = get_term(term_["term_id"], "category")
        cats_ = Array({cat_.term_id: cat_})
        term_ = None
        cat_ = None
    elif "all" == args_["content"]:
        categories_ = get_categories(Array({"get": "all"}))
        tags_ = get_tags(Array({"get": "all"}))
        custom_taxonomies_ = get_taxonomies(Array({"_builtin": False}))
        custom_terms_ = get_terms(Array({"taxonomy": custom_taxonomies_, "get": "all"}))
        #// Put categories in order with no child going before its parent.
        while True:
            cat_ = php_array_shift(categories_)
            if not (cat_):
                break
            # end if
            if 0 == cat_.parent or (php_isset(lambda : cats_[cat_.parent])):
                cats_[cat_.term_id] = cat_
            else:
                categories_[-1] = cat_
            # end if
        # end while
        #// Put terms in order with no child going before its parent.
        while True:
            t_ = php_array_shift(custom_terms_)
            if not (t_):
                break
            # end if
            if 0 == t_.parent or (php_isset(lambda : terms_[t_.parent])):
                terms_[t_.term_id] = t_
            else:
                custom_terms_[-1] = t_
            # end if
        # end while
        categories_ = None
        custom_taxonomies_ = None
        custom_terms_ = None
    # end if
    #// 
    #// Wrap given string in XML CDATA tag.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $str String to wrap in XML CDATA tag.
    #// @return string
    #//
    def wxr_cdata(str_=None, *_args_):
        if args_ is None:
            args_ = Array()
        # end if
        
        if (not seems_utf8(str_)):
            str_ = utf8_encode(str_)
        # end if
        #// $str = ent2ncr(esc_html($str));
        str_ = "<![CDATA[" + php_str_replace("]]>", "]]]]><![CDATA[>", str_) + "]]>"
        return str_
    # end def wxr_cdata
    #// 
    #// Return the URL of the site
    #// 
    #// @since 2.5.0
    #// 
    #// @return string Site URL.
    #//
    def wxr_site_url(*_args_):
        
        
        if is_multisite():
            #// Multisite: the base URL.
            return network_home_url()
        else:
            #// WordPress (single site): the blog URL.
            return get_bloginfo_rss("url")
        # end if
    # end def wxr_site_url
    #// 
    #// Output a cat_name XML tag from a given category object
    #// 
    #// @since 2.1.0
    #// 
    #// @param object $category Category Object
    #//
    def wxr_cat_name(category_=None, *_args_):
        
        
        if php_empty(lambda : category_.name):
            return
        # end if
        php_print("<wp:cat_name>" + wxr_cdata(category_.name) + "</wp:cat_name>\n")
    # end def wxr_cat_name
    #// 
    #// Output a category_description XML tag from a given category object
    #// 
    #// @since 2.1.0
    #// 
    #// @param object $category Category Object
    #//
    def wxr_category_description(category_=None, *_args_):
        
        
        if php_empty(lambda : category_.description):
            return
        # end if
        php_print("<wp:category_description>" + wxr_cdata(category_.description) + "</wp:category_description>\n")
    # end def wxr_category_description
    #// 
    #// Output a tag_name XML tag from a given tag object
    #// 
    #// @since 2.3.0
    #// 
    #// @param object $tag Tag Object
    #//
    def wxr_tag_name(tag_=None, *_args_):
        
        
        if php_empty(lambda : tag_.name):
            return
        # end if
        php_print("<wp:tag_name>" + wxr_cdata(tag_.name) + "</wp:tag_name>\n")
    # end def wxr_tag_name
    #// 
    #// Output a tag_description XML tag from a given tag object
    #// 
    #// @since 2.3.0
    #// 
    #// @param object $tag Tag Object
    #//
    def wxr_tag_description(tag_=None, *_args_):
        
        
        if php_empty(lambda : tag_.description):
            return
        # end if
        php_print("<wp:tag_description>" + wxr_cdata(tag_.description) + "</wp:tag_description>\n")
    # end def wxr_tag_description
    #// 
    #// Output a term_name XML tag from a given term object
    #// 
    #// @since 2.9.0
    #// 
    #// @param object $term Term Object
    #//
    def wxr_term_name(term_=None, *_args_):
        
        
        if php_empty(lambda : term_.name):
            return
        # end if
        php_print("<wp:term_name>" + wxr_cdata(term_.name) + "</wp:term_name>\n")
    # end def wxr_term_name
    #// 
    #// Output a term_description XML tag from a given term object
    #// 
    #// @since 2.9.0
    #// 
    #// @param object $term Term Object
    #//
    def wxr_term_description(term_=None, *_args_):
        
        
        if php_empty(lambda : term_.description):
            return
        # end if
        php_print("     <wp:term_description>" + wxr_cdata(term_.description) + "</wp:term_description>\n")
    # end def wxr_term_description
    #// 
    #// Output term meta XML tags for a given term object.
    #// 
    #// @since 4.6.0
    #// 
    #// @param WP_Term $term Term object.
    #//
    def wxr_term_meta(term_=None, *_args_):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        termmeta_ = wpdb_.get_results(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.termmeta) + str(" WHERE term_id = %d"), term_.term_id))
        for meta_ in termmeta_:
            #// 
            #// Filters whether to selectively skip term meta used for WXR exports.
            #// 
            #// Returning a truthy value to the filter will skip the current meta
            #// object from being exported.
            #// 
            #// @since 4.6.0
            #// 
            #// @param bool   $skip     Whether to skip the current piece of term meta. Default false.
            #// @param string $meta_key Current meta key.
            #// @param object $meta     Current meta object.
            #//
            if (not apply_filters("wxr_export_skip_termmeta", False, meta_.meta_key, meta_)):
                printf("""      <wp:termmeta>
                <wp:meta_key>%s</wp:meta_key>
                <wp:meta_value>%s</wp:meta_value>
                </wp:termmeta>
                """, wxr_cdata(meta_.meta_key), wxr_cdata(meta_.meta_value))
            # end if
        # end for
    # end def wxr_term_meta
    #// 
    #// Output list of authors with posts
    #// 
    #// @since 3.1.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int[] $post_ids Optional. Array of post IDs to filter the query by.
    #//
    def wxr_authors_list(post_ids_=None, *_args_):
        if post_ids_ is None:
            post_ids_ = None
        # end if
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if (not php_empty(lambda : post_ids_)):
            post_ids_ = php_array_map("absint", post_ids_)
            and_ = "AND ID IN ( " + php_implode(", ", post_ids_) + ")"
        else:
            and_ = ""
        # end if
        authors_ = Array()
        results_ = wpdb_.get_results(str("SELECT DISTINCT post_author FROM ") + str(wpdb_.posts) + str(" WHERE post_status != 'auto-draft' ") + str(and_))
        for result_ in results_:
            authors_[-1] = get_userdata(result_.post_author)
        # end for
        authors_ = php_array_filter(authors_)
        for author_ in authors_:
            php_print(" <wp:author>")
            php_print("<wp:author_id>" + php_intval(author_.ID) + "</wp:author_id>")
            php_print("<wp:author_login>" + wxr_cdata(author_.user_login) + "</wp:author_login>")
            php_print("<wp:author_email>" + wxr_cdata(author_.user_email) + "</wp:author_email>")
            php_print("<wp:author_display_name>" + wxr_cdata(author_.display_name) + "</wp:author_display_name>")
            php_print("<wp:author_first_name>" + wxr_cdata(author_.first_name) + "</wp:author_first_name>")
            php_print("<wp:author_last_name>" + wxr_cdata(author_.last_name) + "</wp:author_last_name>")
            php_print("</wp:author>\n")
        # end for
    # end def wxr_authors_list
    #// 
    #// Output all navigation menu terms
    #// 
    #// @since 3.1.0
    #//
    def wxr_nav_menu_terms(*_args_):
        
        
        nav_menus_ = wp_get_nav_menus()
        if php_empty(lambda : nav_menus_) or (not php_is_array(nav_menus_)):
            return
        # end if
        for menu_ in nav_menus_:
            php_print(" <wp:term>")
            php_print("<wp:term_id>" + php_intval(menu_.term_id) + "</wp:term_id>")
            php_print("<wp:term_taxonomy>nav_menu</wp:term_taxonomy>")
            php_print("<wp:term_slug>" + wxr_cdata(menu_.slug) + "</wp:term_slug>")
            wxr_term_name(menu_)
            php_print("</wp:term>\n")
        # end for
    # end def wxr_nav_menu_terms
    #// 
    #// Output list of taxonomy terms, in XML tag format, associated with a post
    #// 
    #// @since 2.3.0
    #//
    def wxr_post_taxonomy(*_args_):
        
        
        post_ = get_post()
        taxonomies_ = get_object_taxonomies(post_.post_type)
        if php_empty(lambda : taxonomies_):
            return
        # end if
        terms_ = wp_get_object_terms(post_.ID, taxonomies_)
        for term_ in terms_:
            php_print(str("     <category domain=\"") + str(term_.taxonomy) + str("\" nicename=\"") + str(term_.slug) + str("\">") + wxr_cdata(term_.name) + "</category>\n")
        # end for
    # end def wxr_post_taxonomy
    #// 
    #// @param bool   $return_me
    #// @param string $meta_key
    #// @return bool
    #//
    def wxr_filter_postmeta(return_me_=None, meta_key_=None, *_args_):
        
        
        if "_edit_lock" == meta_key_:
            return_me_ = True
        # end if
        return return_me_
    # end def wxr_filter_postmeta
    add_filter("wxr_export_skip_postmeta", "wxr_filter_postmeta", 10, 2)
    php_print("<?xml version=\"1.0\" encoding=\"" + get_bloginfo("charset") + "\" ?>\n")
    php_print("""<!-- This is a WordPress eXtended RSS file generated by WordPress as an export of your site. -->
    <!-- It contains information about your site's posts, pages, comments, categories, and other content. -->
    <!-- You may use this file to transfer that content from one site to another. -->
    <!-- This file is not intended to serve as a complete backup of your site. -->
    <!-- To import this information into a WordPress site follow these steps: -->
    <!-- 1. Log in to that site as an administrator. -->
    <!-- 2. Go to Tools: Import in the WordPress admin panel. -->
    <!-- 3. Install the \"WordPress\" importer from the list. -->
    <!-- 4. Activate & Run Importer. -->
    <!-- 5. Upload this file using the form provided on that page. -->
    <!-- 6. You will first be asked to map the authors in this export file to users -->
    <!--    on the site. For each author, you may choose to map to an -->
    <!--    existing user on the site or to create a new user. -->
    <!-- 7. WordPress will then import each of the posts, pages, comments, categories, etc. -->
    <!--    contained in this file into your site. -->
    """)
    the_generator("export")
    php_print("<rss version=\"2.0\"\n   xmlns:excerpt=\"http://wordpress.org/export/")
    php_print(WXR_VERSION)
    php_print("""/excerpt/\"
    xmlns:content=\"http://purl.org/rss/1.0/modules/content/\"
    xmlns:wfw=\"http://wellformedweb.org/CommentAPI/\"
    xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
    xmlns:wp=\"http://wordpress.org/export/""")
    php_print(WXR_VERSION)
    php_print("""/\"
    >
    <channel>
    <title>""")
    bloginfo_rss("name")
    php_print("</title>\n   <link>")
    bloginfo_rss("url")
    php_print("</link>\n    <description>")
    bloginfo_rss("description")
    php_print("</description>\n <pubDate>")
    php_print(gmdate("D, d M Y H:i:s +0000"))
    php_print("</pubDate>\n <language>")
    bloginfo_rss("language")
    php_print("</language>\n    <wp:wxr_version>")
    php_print(WXR_VERSION)
    php_print("</wp:wxr_version>\n  <wp:base_site_url>")
    php_print(wxr_site_url())
    php_print("</wp:base_site_url>\n    <wp:base_blog_url>")
    bloginfo_rss("url")
    php_print("</wp:base_blog_url>\n\n  ")
    wxr_authors_list(post_ids_)
    php_print("\n   ")
    for c_ in cats_:
        php_print(" <wp:category>\n     <wp:term_id>")
        php_print(php_intval(c_.term_id))
        php_print("</wp:term_id>\n      <wp:category_nicename>")
        php_print(wxr_cdata(c_.slug))
        php_print("</wp:category_nicename>\n        <wp:category_parent>")
        php_print(wxr_cdata(cats_[c_.parent].slug if c_.parent else ""))
        php_print("</wp:category_parent>\n      ")
        wxr_cat_name(c_)
        wxr_category_description(c_)
        wxr_term_meta(c_)
        php_print(" </wp:category>\n    ")
    # end for
    php_print(" ")
    for t_ in tags_:
        php_print(" <wp:tag>\n      <wp:term_id>")
        php_print(php_intval(t_.term_id))
        php_print("</wp:term_id>\n      <wp:tag_slug>")
        php_print(wxr_cdata(t_.slug))
        php_print("</wp:tag_slug>\n     ")
        wxr_tag_name(t_)
        wxr_tag_description(t_)
        wxr_term_meta(t_)
        php_print(" </wp:tag>\n ")
    # end for
    php_print(" ")
    for t_ in terms_:
        php_print(" <wp:term>\n     <wp:term_id>")
        php_print(wxr_cdata(t_.term_id))
        php_print("</wp:term_id>\n      <wp:term_taxonomy>")
        php_print(wxr_cdata(t_.taxonomy))
        php_print("</wp:term_taxonomy>\n        <wp:term_slug>")
        php_print(wxr_cdata(t_.slug))
        php_print("</wp:term_slug>\n        <wp:term_parent>")
        php_print(wxr_cdata(terms_[t_.parent].slug if t_.parent else ""))
        php_print("</wp:term_parent>\n      ")
        wxr_term_name(t_)
        wxr_term_description(t_)
        wxr_term_meta(t_)
        php_print(" </wp:term>\n    ")
    # end for
    php_print(" ")
    if "all" == args_["content"]:
        wxr_nav_menu_terms()
    # end if
    php_print("\n   ")
    #// This action is documented in wp-includes/feed-rss2.php
    do_action("rss2_head")
    php_print("\n   ")
    if post_ids_:
        #// 
        #// @global WP_Query $wp_query WordPress Query object.
        #//
        global wp_query_
        php_check_if_defined("wp_query_")
        #// Fake being in the loop.
        wp_query_.in_the_loop = True
        #// Fetch 20 posts at a time rather than loading the entire table into memory.
        while True:
            next_posts_ = array_splice(post_ids_, 0, 20)
            if not (next_posts_):
                break
            # end if
            where_ = "WHERE ID IN (" + join(",", next_posts_) + ")"
            posts_ = wpdb_.get_results(str("SELECT * FROM ") + str(wpdb_.posts) + str(" ") + str(where_))
            #// Begin Loop.
            for post_ in posts_:
                setup_postdata(post_)
                #// This filter is documented in wp-includes/feed.php
                title_ = apply_filters("the_title_rss", post_.post_title)
                #// 
                #// Filters the post content used for WXR exports.
                #// 
                #// @since 2.5.0
                #// 
                #// @param string $post_content Content of the current post.
                #//
                content_ = wxr_cdata(apply_filters("the_content_export", post_.post_content))
                #// 
                #// Filters the post excerpt used for WXR exports.
                #// 
                #// @since 2.6.0
                #// 
                #// @param string $post_excerpt Excerpt for the current post.
                #//
                excerpt_ = wxr_cdata(apply_filters("the_excerpt_export", post_.post_excerpt))
                is_sticky_ = 1 if is_sticky(post_.ID) else 0
                php_print(" <item>\n        <title>")
                php_print(title_)
                php_print("</title>\n       <link>")
                the_permalink_rss()
                php_print("</link>\n        <pubDate>")
                php_print(mysql2date("D, d M Y H:i:s +0000", get_post_time("Y-m-d H:i:s", True), False))
                php_print("</pubDate>\n     <dc:creator>")
                php_print(wxr_cdata(get_the_author_meta("login")))
                php_print("</dc:creator>\n      <guid isPermaLink=\"false\">")
                the_guid()
                php_print("</guid>\n        <description></description>\n       <content:encoded>")
                php_print(content_)
                php_print("</content:encoded>\n     <excerpt:encoded>")
                php_print(excerpt_)
                php_print("</excerpt:encoded>\n     <wp:post_id>")
                php_print(php_intval(post_.ID))
                php_print("</wp:post_id>\n      <wp:post_date>")
                php_print(wxr_cdata(post_.post_date))
                php_print("</wp:post_date>\n        <wp:post_date_gmt>")
                php_print(wxr_cdata(post_.post_date_gmt))
                php_print("</wp:post_date_gmt>\n        <wp:comment_status>")
                php_print(wxr_cdata(post_.comment_status))
                php_print("</wp:comment_status>\n       <wp:ping_status>")
                php_print(wxr_cdata(post_.ping_status))
                php_print("</wp:ping_status>\n      <wp:post_name>")
                php_print(wxr_cdata(post_.post_name))
                php_print("</wp:post_name>\n        <wp:status>")
                php_print(wxr_cdata(post_.post_status))
                php_print("</wp:status>\n       <wp:post_parent>")
                php_print(php_intval(post_.post_parent))
                php_print("</wp:post_parent>\n      <wp:menu_order>")
                php_print(php_intval(post_.menu_order))
                php_print("</wp:menu_order>\n       <wp:post_type>")
                php_print(wxr_cdata(post_.post_type))
                php_print("</wp:post_type>\n        <wp:post_password>")
                php_print(wxr_cdata(post_.post_password))
                php_print("</wp:post_password>\n        <wp:is_sticky>")
                php_print(php_intval(is_sticky_))
                php_print("</wp:is_sticky>\n                ")
                if "attachment" == post_.post_type:
                    php_print("     <wp:attachment_url>")
                    php_print(wxr_cdata(wp_get_attachment_url(post_.ID)))
                    php_print("</wp:attachment_url>\n   ")
                # end if
                php_print("             ")
                wxr_post_taxonomy()
                php_print("             ")
                postmeta_ = wpdb_.get_results(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.postmeta) + str(" WHERE post_id = %d"), post_.ID))
                for meta_ in postmeta_:
                    #// 
                    #// Filters whether to selectively skip post meta used for WXR exports.
                    #// 
                    #// Returning a truthy value to the filter will skip the current meta
                    #// object from being exported.
                    #// 
                    #// @since 3.3.0
                    #// 
                    #// @param bool   $skip     Whether to skip the current post meta. Default false.
                    #// @param string $meta_key Current meta key.
                    #// @param object $meta     Current meta object.
                    #//
                    if apply_filters("wxr_export_skip_postmeta", False, meta_.meta_key, meta_):
                        continue
                    # end if
                    php_print("     <wp:postmeta>\n     <wp:meta_key>")
                    php_print(wxr_cdata(meta_.meta_key))
                    php_print("</wp:meta_key>\n     <wp:meta_value>")
                    php_print(wxr_cdata(meta_.meta_value))
                    php_print("</wp:meta_value>\n       </wp:postmeta>\n                    ")
                # end for
                _comments_ = wpdb_.get_results(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d AND comment_approved <> 'spam'"), post_.ID))
                comments_ = php_array_map("get_comment", _comments_)
                for c_ in comments_:
                    php_print("     <wp:comment>\n          <wp:comment_id>")
                    php_print(php_intval(c_.comment_ID))
                    php_print("</wp:comment_id>\n           <wp:comment_author>")
                    php_print(wxr_cdata(c_.comment_author))
                    php_print("</wp:comment_author>\n           <wp:comment_author_email>")
                    php_print(wxr_cdata(c_.comment_author_email))
                    php_print("</wp:comment_author_email>\n         <wp:comment_author_url>")
                    php_print(esc_url_raw(c_.comment_author_url))
                    php_print("</wp:comment_author_url>\n           <wp:comment_author_IP>")
                    php_print(wxr_cdata(c_.comment_author_IP))
                    php_print("</wp:comment_author_IP>\n            <wp:comment_date>")
                    php_print(wxr_cdata(c_.comment_date))
                    php_print("</wp:comment_date>\n         <wp:comment_date_gmt>")
                    php_print(wxr_cdata(c_.comment_date_gmt))
                    php_print("</wp:comment_date_gmt>\n         <wp:comment_content>")
                    php_print(wxr_cdata(c_.comment_content))
                    php_print("</wp:comment_content>\n          <wp:comment_approved>")
                    php_print(wxr_cdata(c_.comment_approved))
                    php_print("</wp:comment_approved>\n         <wp:comment_type>")
                    php_print(wxr_cdata(c_.comment_type))
                    php_print("</wp:comment_type>\n         <wp:comment_parent>")
                    php_print(php_intval(c_.comment_parent))
                    php_print("</wp:comment_parent>\n           <wp:comment_user_id>")
                    php_print(php_intval(c_.user_id))
                    php_print("</wp:comment_user_id>\n                  ")
                    c_meta_ = wpdb_.get_results(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.commentmeta) + str(" WHERE comment_id = %d"), c_.comment_ID))
                    for meta_ in c_meta_:
                        #// 
                        #// Filters whether to selectively skip comment meta used for WXR exports.
                        #// 
                        #// Returning a truthy value to the filter will skip the current meta
                        #// object from being exported.
                        #// 
                        #// @since 4.0.0
                        #// 
                        #// @param bool   $skip     Whether to skip the current comment meta. Default false.
                        #// @param string $meta_key Current meta key.
                        #// @param object $meta     Current meta object.
                        #//
                        if apply_filters("wxr_export_skip_commentmeta", False, meta_.meta_key, meta_):
                            continue
                        # end if
                        php_print(" <wp:commentmeta>\n  <wp:meta_key>")
                        php_print(wxr_cdata(meta_.meta_key))
                        php_print("</wp:meta_key>\n         <wp:meta_value>")
                        php_print(wxr_cdata(meta_.meta_value))
                        php_print("</wp:meta_value>\n           </wp:commentmeta>\n                 ")
                    # end for
                    php_print("     </wp:comment>\n         ")
                # end for
                php_print("     </item>\n               ")
            # end for
        # end while
    # end if
    php_print("</channel>\n</rss>\n ")
# end def export_wp
