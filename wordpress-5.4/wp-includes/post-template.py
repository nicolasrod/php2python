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
#// WordPress Post Template Functions.
#// 
#// Gets content for the current post in the loop.
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// Display the ID of the current item in the WordPress Loop.
#// 
#// @since 0.71
#//
def the_ID(*_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    php_print(get_the_ID())
# end def the_ID
#// 
#// Retrieve the ID of the current item in the WordPress Loop.
#// 
#// @since 2.1.0
#// 
#// @return int|false The ID of the current item in the WordPress Loop. False if $post is not set.
#//
def get_the_ID(*_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    post_ = get_post()
    return post_.ID if (not php_empty(lambda : post_)) else False
# end def get_the_ID
#// 
#// Display or retrieve the current post title with optional markup.
#// 
#// @since 0.71
#// 
#// @param string $before Optional. Markup to prepend to the title. Default empty.
#// @param string $after  Optional. Markup to append to the title. Default empty.
#// @param bool   $echo   Optional. Whether to echo or return the title. Default true for echo.
#// @return void|string Void if `$echo` argument is true, current post title if `$echo` is false.
#//
def the_title(before_="", after_="", echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    title_ = get_the_title()
    if php_strlen(title_) == 0:
        return
    # end if
    title_ = before_ + title_ + after_
    if echo_:
        php_print(title_)
    else:
        return title_
    # end if
# end def the_title
#// 
#// Sanitize the current title when retrieving or displaying.
#// 
#// Works like the_title(), except the parameters can be in a string or
#// an array. See the function for what can be override in the $args parameter.
#// 
#// The title before it is displayed will have the tags stripped and esc_attr()
#// before it is passed to the user or displayed. The default as with the_title(),
#// is to display the title.
#// 
#// @since 2.3.0
#// 
#// @param string|array $args {
#// Title attribute arguments. Optional.
#// 
#// @type string  $before Markup to prepend to the title. Default empty.
#// @type string  $after  Markup to append to the title. Default empty.
#// @type bool    $echo   Whether to echo or return the title. Default true for echo.
#// @type WP_Post $post   Current post object to retrieve the title for.
#// }
#// @return void|string Void if 'echo' argument is true, the title attribute if 'echo' is false.
#//
def the_title_attribute(args_="", *_args_):
    
    
    defaults_ = Array({"before": "", "after": "", "echo": True, "post": get_post()})
    parsed_args_ = wp_parse_args(args_, defaults_)
    title_ = get_the_title(parsed_args_["post"])
    if php_strlen(title_) == 0:
        return
    # end if
    title_ = parsed_args_["before"] + title_ + parsed_args_["after"]
    title_ = esc_attr(strip_tags(title_))
    if parsed_args_["echo"]:
        php_print(title_)
    else:
        return title_
    # end if
# end def the_title_attribute
#// 
#// Retrieve post title.
#// 
#// If the post is protected and the visitor is not an admin, then "Protected"
#// will be displayed before the post title. If the post is private, then
#// "Private" will be located before the post title.
#// 
#// @since 0.71
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string
#//
def get_the_title(post_=0, *_args_):
    
    
    post_ = get_post(post_)
    title_ = post_.post_title if (php_isset(lambda : post_.post_title)) else ""
    id_ = post_.ID if (php_isset(lambda : post_.ID)) else 0
    if (not is_admin()):
        if (not php_empty(lambda : post_.post_password)):
            #// translators: %s: Protected post title.
            prepend_ = __("Protected: %s")
            #// 
            #// Filters the text prepended to the post title for protected posts.
            #// 
            #// The filter is only applied on the front end.
            #// 
            #// @since 2.8.0
            #// 
            #// @param string  $prepend Text displayed before the post title.
            #// Default 'Protected: %s'.
            #// @param WP_Post $post    Current post object.
            #//
            protected_title_format_ = apply_filters("protected_title_format", prepend_, post_)
            title_ = php_sprintf(protected_title_format_, title_)
        elif (php_isset(lambda : post_.post_status)) and "private" == post_.post_status:
            #// translators: %s: Private post title.
            prepend_ = __("Private: %s")
            #// 
            #// Filters the text prepended to the post title of private posts.
            #// 
            #// The filter is only applied on the front end.
            #// 
            #// @since 2.8.0
            #// 
            #// @param string  $prepend Text displayed before the post title.
            #// Default 'Private: %s'.
            #// @param WP_Post $post    Current post object.
            #//
            private_title_format_ = apply_filters("private_title_format", prepend_, post_)
            title_ = php_sprintf(private_title_format_, title_)
        # end if
    # end if
    #// 
    #// Filters the post title.
    #// 
    #// @since 0.71
    #// 
    #// @param string $title The post title.
    #// @param int    $id    The post ID.
    #//
    return apply_filters("the_title", title_, id_)
# end def get_the_title
#// 
#// Display the Post Global Unique Identifier (guid).
#// 
#// The guid will appear to be a link, but should not be used as a link to the
#// post. The reason you should not use it as a link, is because of moving the
#// blog across domains.
#// 
#// URL is escaped to make it XML-safe.
#// 
#// @since 1.5.0
#// 
#// @param int|WP_Post $post Optional. Post ID or post object. Default is global $post.
#//
def the_guid(post_=0, *_args_):
    
    
    post_ = get_post(post_)
    guid_ = get_the_guid(post_) if (php_isset(lambda : post_.guid)) else ""
    id_ = post_.ID if (php_isset(lambda : post_.ID)) else 0
    #// 
    #// Filters the escaped Global Unique Identifier (guid) of the post.
    #// 
    #// @since 4.2.0
    #// 
    #// @see get_the_guid()
    #// 
    #// @param string $guid Escaped Global Unique Identifier (guid) of the post.
    #// @param int    $id   The post ID.
    #//
    php_print(apply_filters("the_guid", guid_, id_))
# end def the_guid
#// 
#// Retrieve the Post Global Unique Identifier (guid).
#// 
#// The guid will appear to be a link, but should not be used as an link to the
#// post. The reason you should not use it as a link, is because of moving the
#// blog across domains.
#// 
#// @since 1.5.0
#// 
#// @param int|WP_Post $post Optional. Post ID or post object. Default is global $post.
#// @return string
#//
def get_the_guid(post_=0, *_args_):
    
    
    post_ = get_post(post_)
    guid_ = post_.guid if (php_isset(lambda : post_.guid)) else ""
    id_ = post_.ID if (php_isset(lambda : post_.ID)) else 0
    #// 
    #// Filters the Global Unique Identifier (guid) of the post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $guid Global Unique Identifier (guid) of the post.
    #// @param int    $id   The post ID.
    #//
    return apply_filters("get_the_guid", guid_, id_)
# end def get_the_guid
#// 
#// Display the post content.
#// 
#// @since 0.71
#// 
#// @param string $more_link_text Optional. Content for when there is more text.
#// @param bool   $strip_teaser   Optional. Strip teaser content before the more text. Default is false.
#//
def the_content(more_link_text_=None, strip_teaser_=None, *_args_):
    if more_link_text_ is None:
        more_link_text_ = None
    # end if
    if strip_teaser_ is None:
        strip_teaser_ = False
    # end if
    
    content_ = get_the_content(more_link_text_, strip_teaser_)
    #// 
    #// Filters the post content.
    #// 
    #// @since 0.71
    #// 
    #// @param string $content Content of the current post.
    #//
    content_ = apply_filters("the_content", content_)
    content_ = php_str_replace("]]>", "]]&gt;", content_)
    php_print(content_)
# end def the_content
#// 
#// Retrieve the post content.
#// 
#// @since 0.71
#// @since 5.2.0 Added the `$post` parameter.
#// 
#// @global int   $page      Page number of a single post/page.
#// @global int   $more      Boolean indicator for whether single post/page is being viewed.
#// @global bool  $preview   Whether post/page is in preview mode.
#// @global array $pages     Array of all pages in post/page. Each array element contains
#// part of the content separated by the `<!--nextpage-->` tag.
#// @global int   $multipage Boolean indicator for whether multiple pages are in play.
#// 
#// @param string             $more_link_text Optional. Content for when there is more text.
#// @param bool               $strip_teaser   Optional. Strip teaser content before the more text. Default is false.
#// @param WP_Post|object|int $post           Optional. WP_Post instance or Post ID/object. Default is null.
#// @return string
#//
def get_the_content(more_link_text_=None, strip_teaser_=None, post_=None, *_args_):
    if more_link_text_ is None:
        more_link_text_ = None
    # end if
    if strip_teaser_ is None:
        strip_teaser_ = False
    # end if
    if post_ is None:
        post_ = None
    # end if
    
    global page_
    global more_
    global preview_
    global pages_
    global multipage_
    php_check_if_defined("page_","more_","preview_","pages_","multipage_")
    _post_ = get_post(post_)
    if (not type(_post_).__name__ == "WP_Post"):
        return ""
    # end if
    if None == post_:
        elements_ = php_compact("page_", "more_", "preview_", "pages_", "multipage_")
    else:
        elements_ = generate_postdata(_post_)
    # end if
    if None == more_link_text_:
        more_link_text_ = php_sprintf("<span aria-label=\"%1$s\">%2$s</span>", php_sprintf(__("Continue reading %s"), the_title_attribute(Array({"echo": False, "post": _post_}))), __("(more&hellip;)"))
    # end if
    output_ = ""
    has_teaser_ = False
    #// If post password required and it doesn't match the cookie.
    if post_password_required(_post_):
        return get_the_password_form(_post_)
    # end if
    #// If the requested page doesn't exist.
    if elements_["page"] > php_count(elements_["pages"]):
        #// Give them the highest numbered page that DOES exist.
        elements_["page"] = php_count(elements_["pages"])
    # end if
    page_no_ = elements_["page"]
    content_ = elements_["pages"][page_no_ - 1]
    if php_preg_match("/<!--more(.*?)?-->/", content_, matches_):
        if has_block("more", content_):
            #// Remove the core/more block delimiters. They will be left over after $content is split up.
            content_ = php_preg_replace("/<!-- \\/?wp:more(.*?) -->/", "", content_)
        # end if
        content_ = php_explode(matches_[0], content_, 2)
        if (not php_empty(lambda : matches_[1])) and (not php_empty(lambda : more_link_text_)):
            more_link_text_ = strip_tags(wp_kses_no_null(php_trim(matches_[1])))
        # end if
        has_teaser_ = True
    else:
        content_ = Array(content_)
    # end if
    if False != php_strpos(_post_.post_content, "<!--noteaser-->") and (not elements_["multipage"]) or 1 == elements_["page"]:
        strip_teaser_ = True
    # end if
    teaser_ = content_[0]
    if elements_["more"] and strip_teaser_ and has_teaser_:
        teaser_ = ""
    # end if
    output_ += teaser_
    if php_count(content_) > 1:
        if elements_["more"]:
            output_ += "<span id=\"more-" + _post_.ID + "\"></span>" + content_[1]
        else:
            if (not php_empty(lambda : more_link_text_)):
                #// 
                #// Filters the Read More link text.
                #// 
                #// @since 2.8.0
                #// 
                #// @param string $more_link_element Read More link element.
                #// @param string $more_link_text    Read More text.
                #//
                output_ += apply_filters("the_content_more_link", " <a href=\"" + get_permalink(_post_) + str("#more-") + str(_post_.ID) + str("\" class=\"more-link\">") + str(more_link_text_) + str("</a>"), more_link_text_)
            # end if
            output_ = force_balance_tags(output_)
        # end if
    # end if
    return output_
# end def get_the_content
#// 
#// Display the post excerpt.
#// 
#// @since 0.71
#//
def the_excerpt(*_args_):
    
    
    #// 
    #// Filters the displayed post excerpt.
    #// 
    #// @since 0.71
    #// 
    #// @see get_the_excerpt()
    #// 
    #// @param string $post_excerpt The post excerpt.
    #//
    php_print(apply_filters("the_excerpt", get_the_excerpt()))
# end def the_excerpt
#// 
#// Retrieves the post excerpt.
#// 
#// @since 0.71
#// @since 4.5.0 Introduced the `$post` parameter.
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string Post excerpt.
#//
def get_the_excerpt(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    if php_is_bool(post_):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.3.0")
    # end if
    post_ = get_post(post_)
    if php_empty(lambda : post_):
        return ""
    # end if
    if post_password_required(post_):
        return __("There is no excerpt because this is a protected post.")
    # end if
    #// 
    #// Filters the retrieved post excerpt.
    #// 
    #// @since 1.2.0
    #// @since 4.5.0 Introduced the `$post` parameter.
    #// 
    #// @param string  $post_excerpt The post excerpt.
    #// @param WP_Post $post         Post object.
    #//
    return apply_filters("get_the_excerpt", post_.post_excerpt, post_)
# end def get_the_excerpt
#// 
#// Determines whether the post has a custom excerpt.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.3.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return bool True if the post has a custom excerpt, false otherwise.
#//
def has_excerpt(post_=0, *_args_):
    
    
    post_ = get_post(post_)
    return (not php_empty(lambda : post_.post_excerpt))
# end def has_excerpt
#// 
#// Displays the classes for the post container element.
#// 
#// @since 2.7.0
#// 
#// @param string|array $class   One or more classes to add to the class list.
#// @param int|WP_Post  $post_id Optional. Post ID or post object. Defaults to the global `$post`.
#//
def post_class(class_="", post_id_=None, *_args_):
    if post_id_ is None:
        post_id_ = None
    # end if
    
    #// Separates classes with a single space, collates classes for post DIV.
    php_print("class=\"" + php_join(" ", get_post_class(class_, post_id_)) + "\"")
# end def post_class
#// 
#// Retrieves an array of the class names for the post container element.
#// 
#// The class names are many. If the post is a sticky, then the 'sticky'
#// class name. The class 'hentry' is always added to each post. If the post has a
#// post thumbnail, 'has-post-thumbnail' is added as a class. For each taxonomy that
#// the post belongs to, a class will be added of the format '{$taxonomy}-{$slug}' -
#// eg 'category-foo' or 'my_custom_taxonomy-bar'.
#// 
#// The 'post_tag' taxonomy is a special
#// case; the class has the 'tag-' prefix instead of 'post_tag-'. All class names are
#// passed through the filter, {@see 'post_class'}, with the list of class names, followed by
#// $class parameter value, with the post ID as the last parameter.
#// 
#// @since 2.7.0
#// @since 4.2.0 Custom taxonomy class names were added.
#// 
#// @param string|string[] $class   Space-separated string or array of class names to add to the class list.
#// @param int|WP_Post     $post_id Optional. Post ID or post object.
#// @return string[] Array of class names.
#//
def get_post_class(class_="", post_id_=None, *_args_):
    if post_id_ is None:
        post_id_ = None
    # end if
    
    post_ = get_post(post_id_)
    classes_ = Array()
    if class_:
        if (not php_is_array(class_)):
            class_ = php_preg_split("#\\s+#", class_)
        # end if
        classes_ = php_array_map("esc_attr", class_)
    else:
        #// Ensure that we always coerce class to being an array.
        class_ = Array()
    # end if
    if (not post_):
        return classes_
    # end if
    classes_[-1] = "post-" + post_.ID
    if (not is_admin()):
        classes_[-1] = post_.post_type
    # end if
    classes_[-1] = "type-" + post_.post_type
    classes_[-1] = "status-" + post_.post_status
    #// Post Format.
    if post_type_supports(post_.post_type, "post-formats"):
        post_format_ = get_post_format(post_.ID)
        if post_format_ and (not is_wp_error(post_format_)):
            classes_[-1] = "format-" + sanitize_html_class(post_format_)
        else:
            classes_[-1] = "format-standard"
        # end if
    # end if
    post_password_required_ = post_password_required(post_.ID)
    #// Post requires password.
    if post_password_required_:
        classes_[-1] = "post-password-required"
    elif (not php_empty(lambda : post_.post_password)):
        classes_[-1] = "post-password-protected"
    # end if
    #// Post thumbnails.
    if current_theme_supports("post-thumbnails") and has_post_thumbnail(post_.ID) and (not is_attachment(post_)) and (not post_password_required_):
        classes_[-1] = "has-post-thumbnail"
    # end if
    #// Sticky for Sticky Posts.
    if is_sticky(post_.ID):
        if is_home() and (not is_paged()):
            classes_[-1] = "sticky"
        elif is_admin():
            classes_[-1] = "status-sticky"
        # end if
    # end if
    #// hentry for hAtom compliance.
    classes_[-1] = "hentry"
    #// All public taxonomies.
    taxonomies_ = get_taxonomies(Array({"public": True}))
    for taxonomy_ in taxonomies_:
        if is_object_in_taxonomy(post_.post_type, taxonomy_):
            for term_ in get_the_terms(post_.ID, taxonomy_):
                if php_empty(lambda : term_.slug):
                    continue
                # end if
                term_class_ = sanitize_html_class(term_.slug, term_.term_id)
                if php_is_numeric(term_class_) or (not php_trim(term_class_, "-")):
                    term_class_ = term_.term_id
                # end if
                #// 'post_tag' uses the 'tag' prefix for backward compatibility.
                if "post_tag" == taxonomy_:
                    classes_[-1] = "tag-" + term_class_
                else:
                    classes_[-1] = sanitize_html_class(taxonomy_ + "-" + term_class_, taxonomy_ + "-" + term_.term_id)
                # end if
            # end for
        # end if
    # end for
    classes_ = php_array_map("esc_attr", classes_)
    #// 
    #// Filters the list of CSS class names for the current post.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string[] $classes An array of post class names.
    #// @param string[] $class   An array of additional class names added to the post.
    #// @param int      $post_id The post ID.
    #//
    classes_ = apply_filters("post_class", classes_, class_, post_.ID)
    return array_unique(classes_)
# end def get_post_class
#// 
#// Displays the class names for the body element.
#// 
#// @since 2.8.0
#// 
#// @param string|string[] $class Space-separated string or array of class names to add to the class list.
#//
def body_class(class_="", *_args_):
    
    
    #// Separates class names with a single space, collates class names for body element.
    php_print("class=\"" + php_join(" ", get_body_class(class_)) + "\"")
# end def body_class
#// 
#// Retrieves an array of the class names for the body element.
#// 
#// @since 2.8.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string|string[] $class Space-separated string or array of class names to add to the class list.
#// @return string[] Array of class names.
#//
def get_body_class(class_="", *_args_):
    
    
    global wp_query_
    php_check_if_defined("wp_query_")
    classes_ = Array()
    if is_rtl():
        classes_[-1] = "rtl"
    # end if
    if is_front_page():
        classes_[-1] = "home"
    # end if
    if is_home():
        classes_[-1] = "blog"
    # end if
    if is_privacy_policy():
        classes_[-1] = "privacy-policy"
    # end if
    if is_archive():
        classes_[-1] = "archive"
    # end if
    if is_date():
        classes_[-1] = "date"
    # end if
    if is_search():
        classes_[-1] = "search"
        classes_[-1] = "search-results" if wp_query_.posts else "search-no-results"
    # end if
    if is_paged():
        classes_[-1] = "paged"
    # end if
    if is_attachment():
        classes_[-1] = "attachment"
    # end if
    if is_404():
        classes_[-1] = "error404"
    # end if
    if is_singular():
        post_id_ = wp_query_.get_queried_object_id()
        post_ = wp_query_.get_queried_object()
        post_type_ = post_.post_type
        if is_page_template():
            classes_[-1] = str(post_type_) + str("-template")
            template_slug_ = get_page_template_slug(post_id_)
            template_parts_ = php_explode("/", template_slug_)
            for part_ in template_parts_:
                classes_[-1] = str(post_type_) + str("-template-") + sanitize_html_class(php_str_replace(Array(".", "/"), "-", php_basename(part_, ".php")))
            # end for
            classes_[-1] = str(post_type_) + str("-template-") + sanitize_html_class(php_str_replace(".", "-", template_slug_))
        else:
            classes_[-1] = str(post_type_) + str("-template-default")
        # end if
        if is_single():
            classes_[-1] = "single"
            if (php_isset(lambda : post_.post_type)):
                classes_[-1] = "single-" + sanitize_html_class(post_.post_type, post_id_)
                classes_[-1] = "postid-" + post_id_
                #// Post Format.
                if post_type_supports(post_.post_type, "post-formats"):
                    post_format_ = get_post_format(post_.ID)
                    if post_format_ and (not is_wp_error(post_format_)):
                        classes_[-1] = "single-format-" + sanitize_html_class(post_format_)
                    else:
                        classes_[-1] = "single-format-standard"
                    # end if
                # end if
            # end if
        # end if
        if is_attachment():
            mime_type_ = get_post_mime_type(post_id_)
            mime_prefix_ = Array("application/", "image/", "text/", "audio/", "video/", "music/")
            classes_[-1] = "attachmentid-" + post_id_
            classes_[-1] = "attachment-" + php_str_replace(mime_prefix_, "", mime_type_)
        elif is_page():
            classes_[-1] = "page"
            page_id_ = wp_query_.get_queried_object_id()
            post_ = get_post(page_id_)
            classes_[-1] = "page-id-" + page_id_
            if get_pages(Array({"parent": page_id_, "number": 1})):
                classes_[-1] = "page-parent"
            # end if
            if post_.post_parent:
                classes_[-1] = "page-child"
                classes_[-1] = "parent-pageid-" + post_.post_parent
            # end if
        # end if
    elif is_archive():
        if is_post_type_archive():
            classes_[-1] = "post-type-archive"
            post_type_ = get_query_var("post_type")
            if php_is_array(post_type_):
                post_type_ = reset(post_type_)
            # end if
            classes_[-1] = "post-type-archive-" + sanitize_html_class(post_type_)
        elif is_author():
            author_ = wp_query_.get_queried_object()
            classes_[-1] = "author"
            if (php_isset(lambda : author_.user_nicename)):
                classes_[-1] = "author-" + sanitize_html_class(author_.user_nicename, author_.ID)
                classes_[-1] = "author-" + author_.ID
            # end if
        elif is_category():
            cat_ = wp_query_.get_queried_object()
            classes_[-1] = "category"
            if (php_isset(lambda : cat_.term_id)):
                cat_class_ = sanitize_html_class(cat_.slug, cat_.term_id)
                if php_is_numeric(cat_class_) or (not php_trim(cat_class_, "-")):
                    cat_class_ = cat_.term_id
                # end if
                classes_[-1] = "category-" + cat_class_
                classes_[-1] = "category-" + cat_.term_id
            # end if
        elif is_tag():
            tag_ = wp_query_.get_queried_object()
            classes_[-1] = "tag"
            if (php_isset(lambda : tag_.term_id)):
                tag_class_ = sanitize_html_class(tag_.slug, tag_.term_id)
                if php_is_numeric(tag_class_) or (not php_trim(tag_class_, "-")):
                    tag_class_ = tag_.term_id
                # end if
                classes_[-1] = "tag-" + tag_class_
                classes_[-1] = "tag-" + tag_.term_id
            # end if
        elif is_tax():
            term_ = wp_query_.get_queried_object()
            if (php_isset(lambda : term_.term_id)):
                term_class_ = sanitize_html_class(term_.slug, term_.term_id)
                if php_is_numeric(term_class_) or (not php_trim(term_class_, "-")):
                    term_class_ = term_.term_id
                # end if
                classes_[-1] = "tax-" + sanitize_html_class(term_.taxonomy)
                classes_[-1] = "term-" + term_class_
                classes_[-1] = "term-" + term_.term_id
            # end if
        # end if
    # end if
    if is_user_logged_in():
        classes_[-1] = "logged-in"
    # end if
    if is_admin_bar_showing():
        classes_[-1] = "admin-bar"
        classes_[-1] = "no-customize-support"
    # end if
    if current_theme_supports("custom-background") and get_background_color() != get_theme_support("custom-background", "default-color") or get_background_image():
        classes_[-1] = "custom-background"
    # end if
    if has_custom_logo():
        classes_[-1] = "wp-custom-logo"
    # end if
    if current_theme_supports("responsive-embeds"):
        classes_[-1] = "wp-embed-responsive"
    # end if
    page_ = wp_query_.get("page")
    if (not page_) or page_ < 2:
        page_ = wp_query_.get("paged")
    # end if
    if page_ and page_ > 1 and (not is_404()):
        classes_[-1] = "paged-" + page_
        if is_single():
            classes_[-1] = "single-paged-" + page_
        elif is_page():
            classes_[-1] = "page-paged-" + page_
        elif is_category():
            classes_[-1] = "category-paged-" + page_
        elif is_tag():
            classes_[-1] = "tag-paged-" + page_
        elif is_date():
            classes_[-1] = "date-paged-" + page_
        elif is_author():
            classes_[-1] = "author-paged-" + page_
        elif is_search():
            classes_[-1] = "search-paged-" + page_
        elif is_post_type_archive():
            classes_[-1] = "post-type-paged-" + page_
        # end if
    # end if
    if (not php_empty(lambda : class_)):
        if (not php_is_array(class_)):
            class_ = php_preg_split("#\\s+#", class_)
        # end if
        classes_ = php_array_merge(classes_, class_)
    else:
        #// Ensure that we always coerce class to being an array.
        class_ = Array()
    # end if
    classes_ = php_array_map("esc_attr", classes_)
    #// 
    #// Filters the list of CSS body class names for the current post or page.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string[] $classes An array of body class names.
    #// @param string[] $class   An array of additional class names added to the body.
    #//
    classes_ = apply_filters("body_class", classes_, class_)
    return array_unique(classes_)
# end def get_body_class
#// 
#// Whether post requires password and correct password has been provided.
#// 
#// @since 2.7.0
#// 
#// @param int|WP_Post|null $post An optional post. Global $post used if not provided.
#// @return bool false if a password is not required or the correct password cookie is present, true otherwise.
#//
def post_password_required(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if php_empty(lambda : post_.post_password):
        #// This filter is documented in wp-includes/post-template.php
        return apply_filters("post_password_required", False, post_)
    # end if
    if (not (php_isset(lambda : PHP_COOKIE["wp-postpass_" + COOKIEHASH]))):
        #// This filter is documented in wp-includes/post-template.php
        return apply_filters("post_password_required", True, post_)
    # end if
    php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
    hasher_ = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
    hash_ = wp_unslash(PHP_COOKIE["wp-postpass_" + COOKIEHASH])
    if 0 != php_strpos(hash_, "$P$B"):
        required_ = True
    else:
        required_ = (not hasher_.checkpassword(post_.post_password, hash_))
    # end if
    #// 
    #// Filters whether a post requires the user to supply a password.
    #// 
    #// @since 4.7.0
    #// 
    #// @param bool    $required Whether the user needs to supply a password. True if password has not been
    #// provided or is incorrect, false if password has been supplied or is not required.
    #// @param WP_Post $post     Post data.
    #//
    return apply_filters("post_password_required", required_, post_)
# end def post_password_required
#// 
#// Page Template Functions for usage in Themes.
#// 
#// 
#// The formatted output of a list of pages.
#// 
#// Displays page links for paginated posts (i.e. including the `<!--nextpage-->`
#// Quicktag one or more times). This tag must be within The Loop.
#// 
#// @since 1.2.0
#// @since 5.1.0 Added the `aria_current` argument.
#// 
#// @global int $page
#// @global int $numpages
#// @global int $multipage
#// @global int $more
#// 
#// @param string|array $args {
#// Optional. Array or string of default arguments.
#// 
#// @type string       $before           HTML or text to prepend to each link. Default is `<p> Pages:`.
#// @type string       $after            HTML or text to append to each link. Default is `</p>`.
#// @type string       $link_before      HTML or text to prepend to each link, inside the `<a>` tag.
#// Also prepended to the current item, which is not linked. Default empty.
#// @type string       $link_after       HTML or text to append to each Pages link inside the `<a>` tag.
#// Also appended to the current item, which is not linked. Default empty.
#// @type string       $aria_current     The value for the aria-current attribute. Possible values are 'page',
#// 'step', 'location', 'date', 'time', 'true', 'false'. Default is 'page'.
#// @type string       $next_or_number   Indicates whether page numbers should be used. Valid values are number
#// and next. Default is 'number'.
#// @type string       $separator        Text between pagination links. Default is ' '.
#// @type string       $nextpagelink     Link text for the next page link, if available. Default is 'Next Page'.
#// @type string       $previouspagelink Link text for the previous page link, if available. Default is 'Previous Page'.
#// @type string       $pagelink         Format string for page numbers. The % in the parameter string will be
#// replaced with the page number, so 'Page %' generates "Page 1", "Page 2", etc.
#// Defaults to '%', just the page number.
#// @type int|bool     $echo             Whether to echo or not. Accepts 1|true or 0|false. Default 1|true.
#// }
#// @return string Formatted output in HTML.
#//
def wp_link_pages(args_="", *_args_):
    
    
    global page_
    global numpages_
    global multipage_
    global more_
    php_check_if_defined("page_","numpages_","multipage_","more_")
    defaults_ = Array({"before": "<p class=\"post-nav-links\">" + __("Pages:"), "after": "</p>", "link_before": "", "link_after": "", "aria_current": "page", "next_or_number": "number", "separator": " ", "nextpagelink": __("Next page"), "previouspagelink": __("Previous page"), "pagelink": "%", "echo": 1})
    parsed_args_ = wp_parse_args(args_, defaults_)
    #// 
    #// Filters the arguments used in retrieving page links for paginated posts.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $parsed_args An array of arguments for page links for paginated posts.
    #//
    parsed_args_ = apply_filters("wp_link_pages_args", parsed_args_)
    output_ = ""
    if multipage_:
        if "number" == parsed_args_["next_or_number"]:
            output_ += parsed_args_["before"]
            i_ = 1
            while i_ <= numpages_:
                
                link_ = parsed_args_["link_before"] + php_str_replace("%", i_, parsed_args_["pagelink"]) + parsed_args_["link_after"]
                if i_ != page_ or (not more_) and 1 == page_:
                    link_ = _wp_link_page(i_) + link_ + "</a>"
                elif i_ == page_:
                    link_ = "<span class=\"post-page-numbers current\" aria-current=\"" + esc_attr(parsed_args_["aria_current"]) + "\">" + link_ + "</span>"
                # end if
                #// 
                #// Filters the HTML output of individual page number links.
                #// 
                #// @since 3.6.0
                #// 
                #// @param string $link The page number HTML output.
                #// @param int    $i    Page number for paginated posts' page links.
                #//
                link_ = apply_filters("wp_link_pages_link", link_, i_)
                #// Use the custom links separator beginning with the second link.
                output_ += " " if 1 == i_ else parsed_args_["separator"]
                output_ += link_
                i_ += 1
            # end while
            output_ += parsed_args_["after"]
        elif more_:
            output_ += parsed_args_["before"]
            prev_ = page_ - 1
            if prev_ > 0:
                link_ = _wp_link_page(prev_) + parsed_args_["link_before"] + parsed_args_["previouspagelink"] + parsed_args_["link_after"] + "</a>"
                #// This filter is documented in wp-includes/post-template.php
                output_ += apply_filters("wp_link_pages_link", link_, prev_)
            # end if
            next_ = page_ + 1
            if next_ <= numpages_:
                if prev_:
                    output_ += parsed_args_["separator"]
                # end if
                link_ = _wp_link_page(next_) + parsed_args_["link_before"] + parsed_args_["nextpagelink"] + parsed_args_["link_after"] + "</a>"
                #// This filter is documented in wp-includes/post-template.php
                output_ += apply_filters("wp_link_pages_link", link_, next_)
            # end if
            output_ += parsed_args_["after"]
        # end if
    # end if
    #// 
    #// Filters the HTML output of page links for paginated posts.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $output HTML output of paginated posts' page links.
    #// @param array  $args   An array of arguments.
    #//
    html_ = apply_filters("wp_link_pages", output_, args_)
    if parsed_args_["echo"]:
        php_print(html_)
    # end if
    return html_
# end def wp_link_pages
#// 
#// Helper function for wp_link_pages().
#// 
#// @since 3.1.0
#// @access private
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int $i Page number.
#// @return string Link.
#//
def _wp_link_page(i_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    post_ = get_post()
    query_args_ = Array()
    if 1 == i_:
        url_ = get_permalink()
    else:
        if "" == get_option("permalink_structure") or php_in_array(post_.post_status, Array("draft", "pending")):
            url_ = add_query_arg("page", i_, get_permalink())
        elif "page" == get_option("show_on_front") and get_option("page_on_front") == post_.ID:
            url_ = trailingslashit(get_permalink()) + user_trailingslashit(str(wp_rewrite_.pagination_base) + str("/") + i_, "single_paged")
        else:
            url_ = trailingslashit(get_permalink()) + user_trailingslashit(i_, "single_paged")
        # end if
    # end if
    if is_preview():
        if "draft" != post_.post_status and (php_isset(lambda : PHP_REQUEST["preview_id"]) and php_isset(lambda : PHP_REQUEST["preview_nonce"])):
            query_args_["preview_id"] = wp_unslash(PHP_REQUEST["preview_id"])
            query_args_["preview_nonce"] = wp_unslash(PHP_REQUEST["preview_nonce"])
        # end if
        url_ = get_preview_post_link(post_, query_args_, url_)
    # end if
    return "<a href=\"" + esc_url(url_) + "\" class=\"post-page-numbers\">"
# end def _wp_link_page
#// 
#// Post-meta: Custom per-post fields.
#// 
#// 
#// Retrieve post custom meta data field.
#// 
#// @since 1.5.0
#// 
#// @param string $key Meta data key name.
#// @return array|string|false Array of values, or single value if only one element exists.
#// False if the key does not exist.
#//
def post_custom(key_="", *_args_):
    
    
    custom_ = get_post_custom()
    if (not (php_isset(lambda : custom_[key_]))):
        return False
    elif 1 == php_count(custom_[key_]):
        return custom_[key_][0]
    else:
        return custom_[key_]
    # end if
# end def post_custom
#// 
#// Display a list of post custom fields.
#// 
#// @since 1.2.0
#// 
#// @internal This will probably change at some point...
#//
def the_meta(*_args_):
    
    
    keys_ = get_post_custom_keys()
    if keys_:
        li_html_ = ""
        for key_ in keys_:
            keyt_ = php_trim(key_)
            if is_protected_meta(keyt_, "post"):
                continue
            # end if
            values_ = php_array_map("trim", get_post_custom_values(key_))
            value_ = php_implode(", ", values_)
            html_ = php_sprintf("<li><span class='post-meta-key'>%s</span> %s</li>\n", php_sprintf(_x("%s:", "Post custom field name"), key_), value_)
            #// 
            #// Filters the HTML output of the li element in the post custom fields list.
            #// 
            #// @since 2.2.0
            #// 
            #// @param string $html  The HTML output for the li element.
            #// @param string $key   Meta key.
            #// @param string $value Meta value.
            #//
            li_html_ += apply_filters("the_meta_key", html_, key_, value_)
        # end for
        if li_html_:
            php_print(str("<ul class='post-meta'>\n") + str(li_html_) + str("</ul>\n"))
        # end if
    # end if
# end def the_meta
#// 
#// Pages.
#// 
#// 
#// Retrieve or display a list of pages as a dropdown (select list).
#// 
#// @since 2.1.0
#// @since 4.2.0 The `$value_field` argument was added.
#// @since 4.3.0 The `$class` argument was added.
#// 
#// @see get_pages()
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments to generate a page dropdown. See `get_pages()` for additional arguments.
#// 
#// @type int          $depth                 Maximum depth. Default 0.
#// @type int          $child_of              Page ID to retrieve child pages of. Default 0.
#// @type int|string   $selected              Value of the option that should be selected. Default 0.
#// @type bool|int     $echo                  Whether to echo or return the generated markup. Accepts 0, 1,
#// or their bool equivalents. Default 1.
#// @type string       $name                  Value for the 'name' attribute of the select element.
#// Default 'page_id'.
#// @type string       $id                    Value for the 'id' attribute of the select element.
#// @type string       $class                 Value for the 'class' attribute of the select element. Default: none.
#// Defaults to the value of `$name`.
#// @type string       $show_option_none      Text to display for showing no pages. Default empty (does not display).
#// @type string       $show_option_no_change Text to display for "no change" option. Default empty (does not display).
#// @type string       $option_none_value     Value to use when no page is selected. Default empty.
#// @type string       $value_field           Post field used to populate the 'value' attribute of the option
#// elements. Accepts any valid post field. Default 'ID'.
#// }
#// @return string HTML dropdown list of pages.
#//
def wp_dropdown_pages(args_="", *_args_):
    
    
    defaults_ = Array({"depth": 0, "child_of": 0, "selected": 0, "echo": 1, "name": "page_id", "id": "", "class": "", "show_option_none": "", "show_option_no_change": "", "option_none_value": "", "value_field": "ID"})
    parsed_args_ = wp_parse_args(args_, defaults_)
    pages_ = get_pages(parsed_args_)
    output_ = ""
    #// Back-compat with old system where both id and name were based on $name argument.
    if php_empty(lambda : parsed_args_["id"]):
        parsed_args_["id"] = parsed_args_["name"]
    # end if
    if (not php_empty(lambda : pages_)):
        class_ = ""
        if (not php_empty(lambda : parsed_args_["class"])):
            class_ = " class='" + esc_attr(parsed_args_["class"]) + "'"
        # end if
        output_ = "<select name='" + esc_attr(parsed_args_["name"]) + "'" + class_ + " id='" + esc_attr(parsed_args_["id"]) + "'>\n"
        if parsed_args_["show_option_no_change"]:
            output_ += "    <option value=\"-1\">" + parsed_args_["show_option_no_change"] + "</option>\n"
        # end if
        if parsed_args_["show_option_none"]:
            output_ += "    <option value=\"" + esc_attr(parsed_args_["option_none_value"]) + "\">" + parsed_args_["show_option_none"] + "</option>\n"
        # end if
        output_ += walk_page_dropdown_tree(pages_, parsed_args_["depth"], parsed_args_)
        output_ += "</select>\n"
    # end if
    #// 
    #// Filters the HTML output of a list of pages as a drop down.
    #// 
    #// @since 2.1.0
    #// @since 4.4.0 `$parsed_args` and `$pages` added as arguments.
    #// 
    #// @param string    $output      HTML output for drop down list of pages.
    #// @param array     $parsed_args The parsed arguments array.
    #// @param WP_Post[] $pages       Array of the page objects.
    #//
    html_ = apply_filters("wp_dropdown_pages", output_, parsed_args_, pages_)
    if parsed_args_["echo"]:
        php_print(html_)
    # end if
    return html_
# end def wp_dropdown_pages
#// 
#// Retrieve or display a list of pages (or hierarchical post type items) in list (li) format.
#// 
#// @since 1.5.0
#// @since 4.7.0 Added the `item_spacing` argument.
#// 
#// @see get_pages()
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments to generate a list of pages. See `get_pages()` for additional arguments.
#// 
#// @type int          $child_of     Display only the sub-pages of a single page by ID. Default 0 (all pages).
#// @type string       $authors      Comma-separated list of author IDs. Default empty (all authors).
#// @type string       $date_format  PHP date format to use for the listed pages. Relies on the 'show_date' parameter.
#// Default is the value of 'date_format' option.
#// @type int          $depth        Number of levels in the hierarchy of pages to include in the generated list.
#// Accepts -1 (any depth), 0 (all pages), 1 (top-level pages only), and n (pages to
#// the given n depth). Default 0.
#// @type bool         $echo         Whether or not to echo the list of pages. Default true.
#// @type string       $exclude      Comma-separated list of page IDs to exclude. Default empty.
#// @type array        $include      Comma-separated list of page IDs to include. Default empty.
#// @type string       $link_after   Text or HTML to follow the page link label. Default null.
#// @type string       $link_before  Text or HTML to precede the page link label. Default null.
#// @type string       $post_type    Post type to query for. Default 'page'.
#// @type string|array $post_status  Comma-separated list or array of post statuses to include. Default 'publish'.
#// @type string       $show_date    Whether to display the page publish or modified date for each page. Accepts
#// 'modified' or any other value. An empty value hides the date. Default empty.
#// @type string       $sort_column  Comma-separated list of column names to sort the pages by. Accepts 'post_author',
#// 'post_date', 'post_title', 'post_name', 'post_modified', 'post_modified_gmt',
#// 'menu_order', 'post_parent', 'ID', 'rand', or 'comment_count'. Default 'post_title'.
#// @type string       $title_li     List heading. Passing a null or empty value will result in no heading, and the list
#// will not be wrapped with unordered list `<ul>` tags. Default 'Pages'.
#// @type string       $item_spacing Whether to preserve whitespace within the menu's HTML. Accepts 'preserve' or 'discard'.
#// Default 'preserve'.
#// @type Walker       $walker       Walker instance to use for listing pages. Default empty (Walker_Page).
#// }
#// @return void|string Void if 'echo' argument is true, HTML list of pages if 'echo' is false.
#//
def wp_list_pages(args_="", *_args_):
    
    
    defaults_ = Array({"depth": 0, "show_date": "", "date_format": get_option("date_format"), "child_of": 0, "exclude": "", "title_li": __("Pages"), "echo": 1, "authors": "", "sort_column": "menu_order, post_title", "link_before": "", "link_after": "", "item_spacing": "preserve", "walker": ""})
    parsed_args_ = wp_parse_args(args_, defaults_)
    if (not php_in_array(parsed_args_["item_spacing"], Array("preserve", "discard"), True)):
        #// Invalid value, fall back to default.
        parsed_args_["item_spacing"] = defaults_["item_spacing"]
    # end if
    output_ = ""
    current_page_ = 0
    #// Sanitize, mostly to keep spaces out.
    parsed_args_["exclude"] = php_preg_replace("/[^0-9,]/", "", parsed_args_["exclude"])
    #// Allow plugins to filter an array of excluded pages (but don't put a nullstring into the array).
    exclude_array_ = php_explode(",", parsed_args_["exclude"]) if parsed_args_["exclude"] else Array()
    #// 
    #// Filters the array of pages to exclude from the pages list.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string[] $exclude_array An array of page IDs to exclude.
    #//
    parsed_args_["exclude"] = php_implode(",", apply_filters("wp_list_pages_excludes", exclude_array_))
    parsed_args_["hierarchical"] = 0
    #// Query pages.
    pages_ = get_pages(parsed_args_)
    if (not php_empty(lambda : pages_)):
        if parsed_args_["title_li"]:
            output_ += "<li class=\"pagenav\">" + parsed_args_["title_li"] + "<ul>"
        # end if
        global wp_query_
        php_check_if_defined("wp_query_")
        if is_page() or is_attachment() or wp_query_.is_posts_page:
            current_page_ = get_queried_object_id()
        elif is_singular():
            queried_object_ = get_queried_object()
            if is_post_type_hierarchical(queried_object_.post_type):
                current_page_ = queried_object_.ID
            # end if
        # end if
        output_ += walk_page_tree(pages_, parsed_args_["depth"], current_page_, parsed_args_)
        if parsed_args_["title_li"]:
            output_ += "</ul></li>"
        # end if
    # end if
    #// 
    #// Filters the HTML output of the pages to list.
    #// 
    #// @since 1.5.1
    #// @since 4.4.0 `$pages` added as arguments.
    #// 
    #// @see wp_list_pages()
    #// 
    #// @param string    $output      HTML output of the pages list.
    #// @param array     $parsed_args An array of page-listing arguments.
    #// @param WP_Post[] $pages       Array of the page objects.
    #//
    html_ = apply_filters("wp_list_pages", output_, parsed_args_, pages_)
    if parsed_args_["echo"]:
        php_print(html_)
    else:
        return html_
    # end if
# end def wp_list_pages
#// 
#// Displays or retrieves a list of pages with an optional home link.
#// 
#// The arguments are listed below and part of the arguments are for wp_list_pages() function.
#// Check that function for more info on those arguments.
#// 
#// @since 2.7.0
#// @since 4.4.0 Added `menu_id`, `container`, `before`, `after`, and `walker` arguments.
#// @since 4.7.0 Added the `item_spacing` argument.
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments to generate a page menu. See `wp_list_pages()` for additional arguments.
#// 
#// @type string          $sort_column  How to sort the list of pages. Accepts post column names.
#// Default 'menu_order, post_title'.
#// @type string          $menu_id      ID for the div containing the page list. Default is empty string.
#// @type string          $menu_class   Class to use for the element containing the page list. Default 'menu'.
#// @type string          $container    Element to use for the element containing the page list. Default 'div'.
#// @type bool            $echo         Whether to echo the list or return it. Accepts true (echo) or false (return).
#// Default true.
#// @type int|bool|string $show_home    Whether to display the link to the home page. Can just enter the text
#// you'd like shown for the home link. 1|true defaults to 'Home'.
#// @type string          $link_before  The HTML or text to prepend to $show_home text. Default empty.
#// @type string          $link_after   The HTML or text to append to $show_home text. Default empty.
#// @type string          $before       The HTML or text to prepend to the menu. Default is '<ul>'.
#// @type string          $after        The HTML or text to append to the menu. Default is '</ul>'.
#// @type string          $item_spacing Whether to preserve whitespace within the menu's HTML. Accepts 'preserve'
#// or 'discard'. Default 'discard'.
#// @type Walker          $walker       Walker instance to use for listing pages. Default empty (Walker_Page).
#// }
#// @return void|string Void if 'echo' argument is true, HTML menu if 'echo' is false.
#//
def wp_page_menu(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"sort_column": "menu_order, post_title", "menu_id": "", "menu_class": "menu", "container": "div", "echo": True, "link_before": "", "link_after": "", "before": "<ul>", "after": "</ul>", "item_spacing": "discard", "walker": ""})
    args_ = wp_parse_args(args_, defaults_)
    if (not php_in_array(args_["item_spacing"], Array("preserve", "discard"))):
        #// Invalid value, fall back to default.
        args_["item_spacing"] = defaults_["item_spacing"]
    # end if
    if "preserve" == args_["item_spacing"]:
        t_ = "  "
        n_ = "\n"
    else:
        t_ = ""
        n_ = ""
    # end if
    #// 
    #// Filters the arguments used to generate a page-based menu.
    #// 
    #// @since 2.7.0
    #// 
    #// @see wp_page_menu()
    #// 
    #// @param array $args An array of page menu arguments.
    #//
    args_ = apply_filters("wp_page_menu_args", args_)
    menu_ = ""
    list_args_ = args_
    #// Show Home in the menu.
    if (not php_empty(lambda : args_["show_home"])):
        if True == args_["show_home"] or "1" == args_["show_home"] or 1 == args_["show_home"]:
            text_ = __("Home")
        else:
            text_ = args_["show_home"]
        # end if
        class_ = ""
        if is_front_page() and (not is_paged()):
            class_ = "class=\"current_page_item\""
        # end if
        menu_ += "<li " + class_ + "><a href=\"" + home_url("/") + "\">" + args_["link_before"] + text_ + args_["link_after"] + "</a></li>"
        #// If the front page is a page, add it to the exclude list.
        if get_option("show_on_front") == "page":
            if (not php_empty(lambda : list_args_["exclude"])):
                list_args_["exclude"] += ","
            else:
                list_args_["exclude"] = ""
            # end if
            list_args_["exclude"] += get_option("page_on_front")
        # end if
    # end if
    list_args_["echo"] = False
    list_args_["title_li"] = ""
    menu_ += wp_list_pages(list_args_)
    container_ = sanitize_text_field(args_["container"])
    #// Fallback in case `wp_nav_menu()` was called without a container.
    if php_empty(lambda : container_):
        container_ = "div"
    # end if
    if menu_:
        #// wp_nav_menu() doesn't set before and after.
        if (php_isset(lambda : args_["fallback_cb"])) and "wp_page_menu" == args_["fallback_cb"] and "ul" != container_:
            args_["before"] = str("<ul>") + str(n_)
            args_["after"] = "</ul>"
        # end if
        menu_ = args_["before"] + menu_ + args_["after"]
    # end if
    attrs_ = ""
    if (not php_empty(lambda : args_["menu_id"])):
        attrs_ += " id=\"" + esc_attr(args_["menu_id"]) + "\""
    # end if
    if (not php_empty(lambda : args_["menu_class"])):
        attrs_ += " class=\"" + esc_attr(args_["menu_class"]) + "\""
    # end if
    menu_ = str("<") + str(container_) + str(attrs_) + str(">") + menu_ + str("</") + str(container_) + str(">") + str(n_)
    #// 
    #// Filters the HTML output of a page-based menu.
    #// 
    #// @since 2.7.0
    #// 
    #// @see wp_page_menu()
    #// 
    #// @param string $menu The HTML output.
    #// @param array  $args An array of arguments.
    #//
    menu_ = apply_filters("wp_page_menu", menu_, args_)
    if args_["echo"]:
        php_print(menu_)
    else:
        return menu_
    # end if
# end def wp_page_menu
#// 
#// Page helpers.
#// 
#// 
#// Retrieve HTML list content for page list.
#// 
#// @uses Walker_Page to create HTML list content.
#// @since 2.1.0
#// 
#// @param array $pages
#// @param int   $depth
#// @param int   $current_page
#// @param array $r
#// @return string
#//
def walk_page_tree(pages_=None, depth_=None, current_page_=None, r_=None, *_args_):
    
    
    if php_empty(lambda : r_["walker"]):
        walker_ = php_new_class("Walker_Page", lambda : Walker_Page())
    else:
        walker_ = r_["walker"]
    # end if
    for page_ in pages_:
        if page_.post_parent:
            r_["pages_with_children"][page_.post_parent] = True
        # end if
    # end for
    return walker_.walk(pages_, depth_, r_, current_page_)
# end def walk_page_tree
#// 
#// Retrieve HTML dropdown (select) content for page list.
#// 
#// @since 2.1.0
#// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
#// to the function signature.
#// 
#// @uses Walker_PageDropdown to create HTML dropdown content.
#// @see Walker_PageDropdown::walk() for parameters and return description.
#// 
#// @return string
#//
def walk_page_dropdown_tree(*args_):
    
    
    if php_empty(lambda : args_[2]["walker"]):
        #// The user's options are the third parameter.
        walker_ = php_new_class("Walker_PageDropdown", lambda : Walker_PageDropdown())
    else:
        walker_ = args_[2]["walker"]
    # end if
    return walker_.walk(args_)
# end def walk_page_dropdown_tree
#// 
#// Attachments.
#// 
#// 
#// Display an attachment page link using an image or icon.
#// 
#// @since 2.0.0
#// 
#// @param int|WP_Post $id Optional. Post ID or post object.
#// @param bool        $fullsize     Optional, default is false. Whether to use full size.
#// @param bool        $deprecated   Deprecated. Not used.
#// @param bool        $permalink    Optional, default is false. Whether to include permalink.
#//
def the_attachment_link(id_=0, fullsize_=None, deprecated_=None, permalink_=None, *_args_):
    if fullsize_ is None:
        fullsize_ = False
    # end if
    if deprecated_ is None:
        deprecated_ = False
    # end if
    if permalink_ is None:
        permalink_ = False
    # end if
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.5.0")
    # end if
    if fullsize_:
        php_print(wp_get_attachment_link(id_, "full", permalink_))
    else:
        php_print(wp_get_attachment_link(id_, "thumbnail", permalink_))
    # end if
# end def the_attachment_link
#// 
#// Retrieve an attachment page link using an image or icon, if possible.
#// 
#// @since 2.5.0
#// @since 4.4.0 The `$id` parameter can now accept either a post ID or `WP_Post` object.
#// 
#// @param int|WP_Post  $id        Optional. Post ID or post object.
#// @param string|array $size      Optional. Image size. Accepts any valid image size, or an array
#// of width and height values in pixels (in that order).
#// Default 'thumbnail'.
#// @param bool         $permalink Optional, Whether to add permalink to image. Default false.
#// @param bool         $icon      Optional. Whether the attachment is an icon. Default false.
#// @param string|false $text      Optional. Link text to use. Activated by passing a string, false otherwise.
#// Default false.
#// @param array|string $attr      Optional. Array or string of attributes. Default empty.
#// @return string HTML content.
#//
def wp_get_attachment_link(id_=0, size_="thumbnail", permalink_=None, icon_=None, text_=None, attr_="", *_args_):
    if permalink_ is None:
        permalink_ = False
    # end if
    if icon_ is None:
        icon_ = False
    # end if
    if text_ is None:
        text_ = False
    # end if
    
    _post_ = get_post(id_)
    if php_empty(lambda : _post_) or "attachment" != _post_.post_type or (not wp_get_attachment_url(_post_.ID)):
        return __("Missing Attachment")
    # end if
    url_ = wp_get_attachment_url(_post_.ID)
    if permalink_:
        url_ = get_attachment_link(_post_.ID)
    # end if
    if text_:
        link_text_ = text_
    elif size_ and "none" != size_:
        link_text_ = wp_get_attachment_image(_post_.ID, size_, icon_, attr_)
    else:
        link_text_ = ""
    # end if
    if "" == php_trim(link_text_):
        link_text_ = _post_.post_title
    # end if
    if "" == php_trim(link_text_):
        link_text_ = esc_html(pathinfo(get_attached_file(_post_.ID), PATHINFO_FILENAME))
    # end if
    #// 
    #// Filters a retrieved attachment page link.
    #// 
    #// @since 2.7.0
    #// @since 5.1.0 Added the $attr parameter.
    #// 
    #// @param string       $link_html The page link HTML output.
    #// @param int          $id        Post ID.
    #// @param string|array $size      Size of the image. Image size or array of width and height values (in that order).
    #// Default 'thumbnail'.
    #// @param bool         $permalink Whether to add permalink to image. Default false.
    #// @param bool         $icon      Whether to include an icon. Default false.
    #// @param string|bool  $text      If string, will be link text. Default false.
    #// @param array|string $attr      Array or string of attributes. Default empty.
    #//
    return apply_filters("wp_get_attachment_link", "<a href='" + esc_url(url_) + str("'>") + str(link_text_) + str("</a>"), id_, size_, permalink_, icon_, text_, attr_)
# end def wp_get_attachment_link
#// 
#// Wrap attachment in paragraph tag before content.
#// 
#// @since 2.0.0
#// 
#// @param string $content
#// @return string
#//
def prepend_attachment(content_=None, *_args_):
    
    
    post_ = get_post()
    if php_empty(lambda : post_.post_type) or "attachment" != post_.post_type:
        return content_
    # end if
    if wp_attachment_is("video", post_):
        meta_ = wp_get_attachment_metadata(get_the_ID())
        atts_ = Array({"src": wp_get_attachment_url()})
        if (not php_empty(lambda : meta_["width"])) and (not php_empty(lambda : meta_["height"])):
            atts_["width"] = php_int(meta_["width"])
            atts_["height"] = php_int(meta_["height"])
        # end if
        if has_post_thumbnail():
            atts_["poster"] = wp_get_attachment_url(get_post_thumbnail_id())
        # end if
        p_ = wp_video_shortcode(atts_)
    elif wp_attachment_is("audio", post_):
        p_ = wp_audio_shortcode(Array({"src": wp_get_attachment_url()}))
    else:
        p_ = "<p class=\"attachment\">"
        #// Show the medium sized image representation of the attachment if available, and link to the raw file.
        p_ += wp_get_attachment_link(0, "medium", False)
        p_ += "</p>"
    # end if
    #// 
    #// Filters the attachment markup to be prepended to the post content.
    #// 
    #// @since 2.0.0
    #// 
    #// @see prepend_attachment()
    #// 
    #// @param string $p The attachment HTML output.
    #//
    p_ = apply_filters("prepend_attachment", p_)
    return str(p_) + str("\n") + str(content_)
# end def prepend_attachment
#// 
#// Misc.
#// 
#// 
#// Retrieve protected post password form content.
#// 
#// @since 1.0.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string HTML content for password form for password protected post.
#//
def get_the_password_form(post_=0, *_args_):
    
    
    post_ = get_post(post_)
    label_ = "pwbox-" + rand() if php_empty(lambda : post_.ID) else post_.ID
    output_ = "<form action=\"" + esc_url(site_url("wp-login.php?action=postpass", "login_post")) + "\" class=\"post-password-form\" method=\"post\">\n <p>" + __("This content is password protected. To view it please enter your password below:") + "</p>\n <p><label for=\"" + label_ + "\">" + __("Password:") + " <input name=\"post_password\" id=\"" + label_ + "\" type=\"password\" size=\"20\" /></label> <input type=\"submit\" name=\"Submit\" value=\"" + esc_attr_x("Enter", "post password form") + "\" /></p></form>\n    "
    #// 
    #// Filters the HTML output for the protected post password form.
    #// 
    #// If modifying the password field, please note that the core database schema
    #// limits the password field to 20 characters regardless of the value of the
    #// size attribute in the form input.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $output The password form HTML output.
    #//
    return apply_filters("the_password_form", output_)
# end def get_the_password_form
#// 
#// Determines whether currently in a page template.
#// 
#// This template tag allows you to determine if you are in a page template.
#// You can optionally provide a template filename or array of template filenames
#// and then the check will be specific to that template.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.5.0
#// @since 4.2.0 The `$template` parameter was changed to also accept an array of page templates.
#// @since 4.7.0 Now works with any post type, not just pages.
#// 
#// @param string|array $template The specific template filename or array of templates to match.
#// @return bool True on success, false on failure.
#//
def is_page_template(template_="", *_args_):
    
    
    if (not is_singular()):
        return False
    # end if
    page_template_ = get_page_template_slug(get_queried_object_id())
    if php_empty(lambda : template_):
        return php_bool(page_template_)
    # end if
    if template_ == page_template_:
        return True
    # end if
    if php_is_array(template_):
        if php_in_array("default", template_, True) and (not page_template_) or php_in_array(page_template_, template_, True):
            return True
        # end if
    # end if
    return "default" == template_ and (not page_template_)
# end def is_page_template
#// 
#// Get the specific template filename for a given post.
#// 
#// @since 3.4.0
#// @since 4.7.0 Now works with any post type, not just pages.
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string|false Page template filename. Returns an empty string when the default page template
#// is in use. Returns false if the post does not exist.
#//
def get_page_template_slug(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    template_ = get_post_meta(post_.ID, "_wp_page_template", True)
    if (not template_) or "default" == template_:
        return ""
    # end if
    return template_
# end def get_page_template_slug
#// 
#// Retrieve formatted date timestamp of a revision (linked to that revisions's page).
#// 
#// @since 2.6.0
#// 
#// @param int|object $revision Revision ID or revision object.
#// @param bool       $link     Optional, default is true. Link to revisions's page?
#// @return string|false i18n formatted datetimestamp or localized 'Current Revision'.
#//
def wp_post_revision_title(revision_=None, link_=None, *_args_):
    if link_ is None:
        link_ = True
    # end if
    
    revision_ = get_post(revision_)
    if (not revision_):
        return revision_
    # end if
    if (not php_in_array(revision_.post_type, Array("post", "page", "revision"))):
        return False
    # end if
    #// translators: Revision date format, see https://www.php.net/date
    datef_ = _x("F j, Y @ H:i:s", "revision date format")
    #// translators: %s: Revision date.
    autosavef_ = __("%s [Autosave]")
    #// translators: %s: Revision date.
    currentf_ = __("%s [Current Revision]")
    date_ = date_i18n(datef_, strtotime(revision_.post_modified))
    edit_link_ = get_edit_post_link(revision_.ID)
    if link_ and current_user_can("edit_post", revision_.ID) and edit_link_:
        date_ = str("<a href='") + str(edit_link_) + str("'>") + str(date_) + str("</a>")
    # end if
    if (not wp_is_post_revision(revision_)):
        date_ = php_sprintf(currentf_, date_)
    elif wp_is_post_autosave(revision_):
        date_ = php_sprintf(autosavef_, date_)
    # end if
    return date_
# end def wp_post_revision_title
#// 
#// Retrieve formatted date timestamp of a revision (linked to that revisions's page).
#// 
#// @since 3.6.0
#// 
#// @param int|object $revision Revision ID or revision object.
#// @param bool       $link     Optional, default is true. Link to revisions's page?
#// @return string|false gravatar, user, i18n formatted datetimestamp or localized 'Current Revision'.
#//
def wp_post_revision_title_expanded(revision_=None, link_=None, *_args_):
    if link_ is None:
        link_ = True
    # end if
    
    revision_ = get_post(revision_)
    if (not revision_):
        return revision_
    # end if
    if (not php_in_array(revision_.post_type, Array("post", "page", "revision"))):
        return False
    # end if
    author_ = get_the_author_meta("display_name", revision_.post_author)
    #// translators: Revision date format, see https://www.php.net/date
    datef_ = _x("F j, Y @ H:i:s", "revision date format")
    gravatar_ = get_avatar(revision_.post_author, 24)
    date_ = date_i18n(datef_, strtotime(revision_.post_modified))
    edit_link_ = get_edit_post_link(revision_.ID)
    if link_ and current_user_can("edit_post", revision_.ID) and edit_link_:
        date_ = str("<a href='") + str(edit_link_) + str("'>") + str(date_) + str("</a>")
    # end if
    revision_date_author_ = php_sprintf(__("%1$s %2$s, %3$s ago (%4$s)"), gravatar_, author_, human_time_diff(strtotime(revision_.post_modified_gmt)), date_)
    #// translators: %s: Revision date with author avatar.
    autosavef_ = __("%s [Autosave]")
    #// translators: %s: Revision date with author avatar.
    currentf_ = __("%s [Current Revision]")
    if (not wp_is_post_revision(revision_)):
        revision_date_author_ = php_sprintf(currentf_, revision_date_author_)
    elif wp_is_post_autosave(revision_):
        revision_date_author_ = php_sprintf(autosavef_, revision_date_author_)
    # end if
    #// 
    #// Filters the formatted author and date for a revision.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string  $revision_date_author The formatted string.
    #// @param WP_Post $revision             The revision object.
    #// @param bool    $link                 Whether to link to the revisions page, as passed into
    #// wp_post_revision_title_expanded().
    #//
    return apply_filters("wp_post_revision_title_expanded", revision_date_author_, revision_, link_)
# end def wp_post_revision_title_expanded
#// 
#// Display a list of a post's revisions.
#// 
#// Can output either a UL with edit links or a TABLE with diff interface, and
#// restore action links.
#// 
#// @since 2.6.0
#// 
#// @param int|WP_Post $post_id Optional. Post ID or WP_Post object. Default is global $post.
#// @param string      $type    'all' (default), 'revision' or 'autosave'
#//
def wp_list_post_revisions(post_id_=0, type_="all", *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_):
        return
    # end if
    #// $args array with (parent, format, right, left, type) deprecated since 3.6.
    if php_is_array(type_):
        type_ = type_["type"] if (not php_empty(lambda : type_["type"])) else type_
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.6.0")
    # end if
    revisions_ = wp_get_post_revisions(post_.ID)
    if (not revisions_):
        return
    # end if
    rows_ = ""
    for revision_ in revisions_:
        if (not current_user_can("read_post", revision_.ID)):
            continue
        # end if
        is_autosave_ = wp_is_post_autosave(revision_)
        if "revision" == type_ and is_autosave_ or "autosave" == type_ and (not is_autosave_):
            continue
        # end if
        rows_ += "  <li>" + wp_post_revision_title_expanded(revision_) + "</li>\n"
    # end for
    php_print("<div class='hide-if-js'><p>" + __("JavaScript must be enabled to use this feature.") + "</p></div>\n")
    php_print("<ul class='post-revisions hide-if-no-js'>\n")
    php_print(rows_)
    php_print("</ul>")
# end def wp_list_post_revisions
