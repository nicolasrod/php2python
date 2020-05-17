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
#// Template loading functions.
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// Retrieve path to a template
#// 
#// Used to quickly retrieve the path of a template without including the file
#// extension. It will also check the parent theme, if the file exists, with
#// the use of locate_template(). Allows for more generic template location
#// without the use of the other get_*_template() functions.
#// 
#// @since 1.5.0
#// 
#// @param string $type      Filename without extension.
#// @param array  $templates An optional list of template candidates
#// @return string Full path to template file.
#//
def get_query_template(type_=None, templates_=None, *_args_):
    if templates_ is None:
        templates_ = Array()
    # end if
    
    type_ = php_preg_replace("|[^a-z0-9-]+|", "", type_)
    if php_empty(lambda : templates_):
        templates_ = Array(str(type_) + str(".php"))
    # end if
    #// 
    #// Filters the list of template filenames that are searched for when retrieving a template to use.
    #// 
    #// The last element in the array should always be the fallback template for this query type.
    #// 
    #// Possible values for `$type` include: 'index', '404', 'archive', 'author', 'category', 'tag', 'taxonomy', 'date',
    #// 'embed', 'home', 'frontpage', 'privacypolicy', 'page', 'paged', 'search', 'single', 'singular', and 'attachment'.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $templates A list of template candidates, in descending order of priority.
    #//
    templates_ = apply_filters(str(type_) + str("_template_hierarchy"), templates_)
    template_ = locate_template(templates_)
    #// 
    #// Filters the path of the queried template by type.
    #// 
    #// The dynamic portion of the hook name, `$type`, refers to the filename -- minus the file
    #// extension and any non-alphanumeric characters delimiting words -- of the file to load.
    #// This hook also applies to various types of files loaded as part of the Template Hierarchy.
    #// 
    #// Possible values for `$type` include: 'index', '404', 'archive', 'author', 'category', 'tag', 'taxonomy', 'date',
    #// 'embed', 'home', 'frontpage', 'privacypolicy', 'page', 'paged', 'search', 'single', 'singular', and 'attachment'.
    #// 
    #// @since 1.5.0
    #// @since 4.8.0 The `$type` and `$templates` parameters were added.
    #// 
    #// @param string $template  Path to the template. See locate_template().
    #// @param string $type      Sanitized filename without extension.
    #// @param array  $templates A list of template candidates, in descending order of priority.
    #//
    return apply_filters(str(type_) + str("_template"), template_, type_, templates_)
# end def get_query_template
#// 
#// Retrieve path of index template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'index'.
#// 
#// @since 3.0.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to index template file.
#//
def get_index_template(*_args_):
    
    
    return get_query_template("index")
# end def get_index_template
#// 
#// Retrieve path of 404 template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is '404'.
#// 
#// @since 1.5.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to 404 template file.
#//
def get_404_template(*_args_):
    
    
    return get_query_template("404")
# end def get_404_template
#// 
#// Retrieve path of archive template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'archive'.
#// 
#// @since 1.5.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to archive template file.
#//
def get_archive_template(*_args_):
    
    
    post_types_ = php_array_filter(get_query_var("post_type"))
    templates_ = Array()
    if php_count(post_types_) == 1:
        post_type_ = reset(post_types_)
        templates_[-1] = str("archive-") + str(post_type_) + str(".php")
    # end if
    templates_[-1] = "archive.php"
    return get_query_template("archive", templates_)
# end def get_archive_template
#// 
#// Retrieve path of post type archive template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'archive'.
#// 
#// @since 3.7.0
#// 
#// @see get_archive_template()
#// 
#// @return string Full path to archive template file.
#//
def get_post_type_archive_template(*_args_):
    
    
    post_type_ = get_query_var("post_type")
    if php_is_array(post_type_):
        post_type_ = reset(post_type_)
    # end if
    obj_ = get_post_type_object(post_type_)
    if (not type(obj_).__name__ == "WP_Post_Type") or (not obj_.has_archive):
        return ""
    # end if
    return get_archive_template()
# end def get_post_type_archive_template
#// 
#// Retrieve path of author template in current or parent template.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. author-{nicename}.php
#// 2. author-{id}.php
#// 3. author.php
#// 
#// An example of this is:
#// 
#// 1. author-john.php
#// 2. author-1.php
#// 3. author.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'author'.
#// 
#// @since 1.5.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to author template file.
#//
def get_author_template(*_args_):
    
    
    author_ = get_queried_object()
    templates_ = Array()
    if type(author_).__name__ == "WP_User":
        templates_[-1] = str("author-") + str(author_.user_nicename) + str(".php")
        templates_[-1] = str("author-") + str(author_.ID) + str(".php")
    # end if
    templates_[-1] = "author.php"
    return get_query_template("author", templates_)
# end def get_author_template
#// 
#// Retrieve path of category template in current or parent template.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. category-{slug}.php
#// 2. category-{id}.php
#// 3. category.php
#// 
#// An example of this is:
#// 
#// 1. category-news.php
#// 2. category-2.php
#// 3. category.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'category'.
#// 
#// @since 1.5.0
#// @since 4.7.0 The decoded form of `category-{slug}.php` was added to the top of the
#// template hierarchy when the category slug contains multibyte characters.
#// 
#// @see get_query_template()
#// 
#// @return string Full path to category template file.
#//
def get_category_template(*_args_):
    
    
    category_ = get_queried_object()
    templates_ = Array()
    if (not php_empty(lambda : category_.slug)):
        slug_decoded_ = urldecode(category_.slug)
        if slug_decoded_ != category_.slug:
            templates_[-1] = str("category-") + str(slug_decoded_) + str(".php")
        # end if
        templates_[-1] = str("category-") + str(category_.slug) + str(".php")
        templates_[-1] = str("category-") + str(category_.term_id) + str(".php")
    # end if
    templates_[-1] = "category.php"
    return get_query_template("category", templates_)
# end def get_category_template
#// 
#// Retrieve path of tag template in current or parent template.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. tag-{slug}.php
#// 2. tag-{id}.php
#// 3. tag.php
#// 
#// An example of this is:
#// 
#// 1. tag-wordpress.php
#// 2. tag-3.php
#// 3. tag.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'tag'.
#// 
#// @since 2.3.0
#// @since 4.7.0 The decoded form of `tag-{slug}.php` was added to the top of the
#// template hierarchy when the tag slug contains multibyte characters.
#// 
#// @see get_query_template()
#// 
#// @return string Full path to tag template file.
#//
def get_tag_template(*_args_):
    
    
    tag_ = get_queried_object()
    templates_ = Array()
    if (not php_empty(lambda : tag_.slug)):
        slug_decoded_ = urldecode(tag_.slug)
        if slug_decoded_ != tag_.slug:
            templates_[-1] = str("tag-") + str(slug_decoded_) + str(".php")
        # end if
        templates_[-1] = str("tag-") + str(tag_.slug) + str(".php")
        templates_[-1] = str("tag-") + str(tag_.term_id) + str(".php")
    # end if
    templates_[-1] = "tag.php"
    return get_query_template("tag", templates_)
# end def get_tag_template
#// 
#// Retrieve path of custom taxonomy term template in current or parent template.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. taxonomy-{taxonomy_slug}-{term_slug}.php
#// 2. taxonomy-{taxonomy_slug}.php
#// 3. taxonomy.php
#// 
#// An example of this is:
#// 
#// 1. taxonomy-location-texas.php
#// 2. taxonomy-location.php
#// 3. taxonomy.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'taxonomy'.
#// 
#// @since 2.5.0
#// @since 4.7.0 The decoded form of `taxonomy-{taxonomy_slug}-{term_slug}.php` was added to the top of the
#// template hierarchy when the term slug contains multibyte characters.
#// 
#// @see get_query_template()
#// 
#// @return string Full path to custom taxonomy term template file.
#//
def get_taxonomy_template(*_args_):
    
    
    term_ = get_queried_object()
    templates_ = Array()
    if (not php_empty(lambda : term_.slug)):
        taxonomy_ = term_.taxonomy
        slug_decoded_ = urldecode(term_.slug)
        if slug_decoded_ != term_.slug:
            templates_[-1] = str("taxonomy-") + str(taxonomy_) + str("-") + str(slug_decoded_) + str(".php")
        # end if
        templates_[-1] = str("taxonomy-") + str(taxonomy_) + str("-") + str(term_.slug) + str(".php")
        templates_[-1] = str("taxonomy-") + str(taxonomy_) + str(".php")
    # end if
    templates_[-1] = "taxonomy.php"
    return get_query_template("taxonomy", templates_)
# end def get_taxonomy_template
#// 
#// Retrieve path of date template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'date'.
#// 
#// @since 1.5.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to date template file.
#//
def get_date_template(*_args_):
    
    
    return get_query_template("date")
# end def get_date_template
#// 
#// Retrieve path of home template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'home'.
#// 
#// @since 1.5.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to home template file.
#//
def get_home_template(*_args_):
    
    
    templates_ = Array("home.php", "index.php")
    return get_query_template("home", templates_)
# end def get_home_template
#// 
#// Retrieve path of front page template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'frontpage'.
#// 
#// @since 3.0.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to front page template file.
#//
def get_front_page_template(*_args_):
    
    
    templates_ = Array("front-page.php")
    return get_query_template("frontpage", templates_)
# end def get_front_page_template
#// 
#// Retrieve path of Privacy Policy page template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'privacypolicy'.
#// 
#// @since 5.2.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to privacy policy template file.
#//
def get_privacy_policy_template(*_args_):
    
    
    templates_ = Array("privacy-policy.php")
    return get_query_template("privacypolicy", templates_)
# end def get_privacy_policy_template
#// 
#// Retrieve path of page template in current or parent template.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. {Page Template}.php
#// 2. page-{page_name}.php
#// 3. page-{id}.php
#// 4. page.php
#// 
#// An example of this is:
#// 
#// 1. page-templates/full-width.php
#// 2. page-about.php
#// 3. page-4.php
#// 4. page.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'page'.
#// 
#// @since 1.5.0
#// @since 4.7.0 The decoded form of `page-{page_name}.php` was added to the top of the
#// template hierarchy when the page name contains multibyte characters.
#// 
#// @see get_query_template()
#// 
#// @return string Full path to page template file.
#//
def get_page_template(*_args_):
    
    
    id_ = get_queried_object_id()
    template_ = get_page_template_slug()
    pagename_ = get_query_var("pagename")
    if (not pagename_) and id_:
        #// If a static page is set as the front page, $pagename will not be set.
        #// Retrieve it from the queried object.
        post_ = get_queried_object()
        if post_:
            pagename_ = post_.post_name
        # end if
    # end if
    templates_ = Array()
    if template_ and 0 == validate_file(template_):
        templates_[-1] = template_
    # end if
    if pagename_:
        pagename_decoded_ = urldecode(pagename_)
        if pagename_decoded_ != pagename_:
            templates_[-1] = str("page-") + str(pagename_decoded_) + str(".php")
        # end if
        templates_[-1] = str("page-") + str(pagename_) + str(".php")
    # end if
    if id_:
        templates_[-1] = str("page-") + str(id_) + str(".php")
    # end if
    templates_[-1] = "page.php"
    return get_query_template("page", templates_)
# end def get_page_template
#// 
#// Retrieve path of search template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'search'.
#// 
#// @since 1.5.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to search template file.
#//
def get_search_template(*_args_):
    
    
    return get_query_template("search")
# end def get_search_template
#// 
#// Retrieve path of single template in current or parent template. Applies to single Posts,
#// single Attachments, and single custom post types.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. {Post Type Template}.php
#// 2. single-{post_type}-{post_name}.php
#// 3. single-{post_type}.php
#// 4. single.php
#// 
#// An example of this is:
#// 
#// 1. templates/full-width.php
#// 2. single-post-hello-world.php
#// 3. single-post.php
#// 4. single.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'single'.
#// 
#// @since 1.5.0
#// @since 4.4.0 `single-{post_type}-{post_name}.php` was added to the top of the template hierarchy.
#// @since 4.7.0 The decoded form of `single-{post_type}-{post_name}.php` was added to the top of the
#// template hierarchy when the post name contains multibyte characters.
#// @since 4.7.0 `{Post Type Template}.php` was added to the top of the template hierarchy.
#// 
#// @see get_query_template()
#// 
#// @return string Full path to single template file.
#//
def get_single_template(*_args_):
    
    
    object_ = get_queried_object()
    templates_ = Array()
    if (not php_empty(lambda : object_.post_type)):
        template_ = get_page_template_slug(object_)
        if template_ and 0 == validate_file(template_):
            templates_[-1] = template_
        # end if
        name_decoded_ = urldecode(object_.post_name)
        if name_decoded_ != object_.post_name:
            templates_[-1] = str("single-") + str(object_.post_type) + str("-") + str(name_decoded_) + str(".php")
        # end if
        templates_[-1] = str("single-") + str(object_.post_type) + str("-") + str(object_.post_name) + str(".php")
        templates_[-1] = str("single-") + str(object_.post_type) + str(".php")
    # end if
    templates_[-1] = "single.php"
    return get_query_template("single", templates_)
# end def get_single_template
#// 
#// Retrieves an embed template path in the current or parent template.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. embed-{post_type}-{post_format}.php
#// 2. embed-{post_type}.php
#// 3. embed.php
#// 
#// An example of this is:
#// 
#// 1. embed-post-audio.php
#// 2. embed-post.php
#// 3. embed.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'embed'.
#// 
#// @since 4.5.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to embed template file.
#//
def get_embed_template(*_args_):
    
    
    object_ = get_queried_object()
    templates_ = Array()
    if (not php_empty(lambda : object_.post_type)):
        post_format_ = get_post_format(object_)
        if post_format_:
            templates_[-1] = str("embed-") + str(object_.post_type) + str("-") + str(post_format_) + str(".php")
        # end if
        templates_[-1] = str("embed-") + str(object_.post_type) + str(".php")
    # end if
    templates_[-1] = "embed.php"
    return get_query_template("embed", templates_)
# end def get_embed_template
#// 
#// Retrieves the path of the singular template in current or parent template.
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'singular'.
#// 
#// @since 4.3.0
#// 
#// @see get_query_template()
#// 
#// @return string Full path to singular template file
#//
def get_singular_template(*_args_):
    
    
    return get_query_template("singular")
# end def get_singular_template
#// 
#// Retrieve path of attachment template in current or parent template.
#// 
#// The hierarchy for this template looks like:
#// 
#// 1. {mime_type}-{sub_type}.php
#// 2. {sub_type}.php
#// 3. {mime_type}.php
#// 4. attachment.php
#// 
#// An example of this is:
#// 
#// 1. image-jpeg.php
#// 2. jpeg.php
#// 3. image.php
#// 4. attachment.php
#// 
#// The template hierarchy and template path are filterable via the {@see '$type_template_hierarchy'}
#// and {@see '$type_template'} dynamic hooks, where `$type` is 'attachment'.
#// 
#// @since 2.0.0
#// @since 4.3.0 The order of the mime type logic was reversed so the hierarchy is more logical.
#// 
#// @see get_query_template()
#// 
#// @global array $posts
#// 
#// @return string Full path to attachment template file.
#//
def get_attachment_template(*_args_):
    
    
    attachment_ = get_queried_object()
    templates_ = Array()
    if attachment_:
        if False != php_strpos(attachment_.post_mime_type, "/"):
            type_, subtype_ = php_explode("/", attachment_.post_mime_type)
        else:
            type_, subtype_ = Array(attachment_.post_mime_type, "")
        # end if
        if (not php_empty(lambda : subtype_)):
            templates_[-1] = str(type_) + str("-") + str(subtype_) + str(".php")
            templates_[-1] = str(subtype_) + str(".php")
        # end if
        templates_[-1] = str(type_) + str(".php")
    # end if
    templates_[-1] = "attachment.php"
    return get_query_template("attachment", templates_)
# end def get_attachment_template
#// 
#// Retrieve the name of the highest priority template file that exists.
#// 
#// Searches in the STYLESHEETPATH before TEMPLATEPATH and wp-includes/theme-compat
#// so that themes which inherit from a parent theme can just overload one file.
#// 
#// @since 2.7.0
#// 
#// @param string|array $template_names Template file(s) to search for, in order.
#// @param bool         $load           If true the template file will be loaded if it is found.
#// @param bool         $require_once   Whether to require_once or require. Default true. Has no effect if $load is false.
#// @return string The template filename if one is located.
#//
def locate_template(template_names_=None, load_=None, require_once_=None, *_args_):
    if load_ is None:
        load_ = False
    # end if
    if require_once_ is None:
        require_once_ = True
    # end if
    
    located_ = ""
    for template_name_ in template_names_:
        if (not template_name_):
            continue
        # end if
        if php_file_exists(STYLESHEETPATH + "/" + template_name_):
            located_ = STYLESHEETPATH + "/" + template_name_
            break
        elif php_file_exists(TEMPLATEPATH + "/" + template_name_):
            located_ = TEMPLATEPATH + "/" + template_name_
            break
        elif php_file_exists(ABSPATH + WPINC + "/theme-compat/" + template_name_):
            located_ = ABSPATH + WPINC + "/theme-compat/" + template_name_
            break
        # end if
    # end for
    if load_ and "" != located_:
        load_template(located_, require_once_)
    # end if
    return located_
# end def locate_template
#// 
#// Require the template file with WordPress environment.
#// 
#// The globals are set up for the template file to ensure that the WordPress
#// environment is available from within the function. The query variables are
#// also available.
#// 
#// @since 1.5.0
#// 
#// @global array      $posts
#// @global WP_Post    $post          Global post object.
#// @global bool       $wp_did_header
#// @global WP_Query   $wp_query      WordPress Query object.
#// @global WP_Rewrite $wp_rewrite    WordPress rewrite component.
#// @global wpdb       $wpdb          WordPress database abstraction object.
#// @global string     $wp_version
#// @global WP         $wp            Current WordPress environment instance.
#// @global int        $id
#// @global WP_Comment $comment       Global comment object.
#// @global int        $user_ID
#// 
#// @param string $_template_file Path to template file.
#// @param bool   $require_once   Whether to require_once or require. Default true.
#//
def load_template(_template_file_=None, require_once_=None, *_args_):
    if require_once_ is None:
        require_once_ = True
    # end if
    
    global posts_
    global post_
    global wp_did_header_
    global wp_query_
    global wp_rewrite_
    global wpdb_
    global wp_version_
    global wp_
    global id_
    global comment_
    global user_ID_
    php_check_if_defined("posts_","post_","wp_did_header_","wp_query_","wp_rewrite_","wpdb_","wp_version_","wp_","id_","comment_","user_ID_")
    if php_is_array(wp_query_.query_vars):
        #// 
        #// This use of extract() cannot be removed. There are many possible ways that
        #// templates could depend on variables that it creates existing, and no way to
        #// detect and deprecate it.
        #// 
        #// Passing the EXTR_SKIP flag is the safest option, ensuring globals and
        #// function variables cannot be overwritten.
        #// 
        #// phpcs:ignore WordPress.PHP.DontExtract.extract_extract
        extract(wp_query_.query_vars, EXTR_SKIP)
    # end if
    if (php_isset(lambda : s_)):
        s_ = esc_attr(s_)
    # end if
    if require_once_:
        php_include_file(_template_file_, once=True)
    else:
        php_include_file(_template_file_, once=False)
    # end if
# end def load_template
