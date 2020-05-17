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
#// WordPress Post Thumbnail Template Functions.
#// 
#// Support for post thumbnails.
#// Theme's functions.php must call add_theme_support( 'post-thumbnails' ) to use these.
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// Determines whether a post has an image attached.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.9.0
#// @since 4.4.0 `$post` can be a post ID or WP_Post object.
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global `$post`.
#// @return bool Whether the post has an image attached.
#//
def has_post_thumbnail(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    thumbnail_id_ = get_post_thumbnail_id(post_)
    has_thumbnail_ = php_bool(thumbnail_id_)
    #// 
    #// Filters whether a post has a post thumbnail.
    #// 
    #// @since 5.1.0
    #// 
    #// @param bool             $has_thumbnail true if the post has a post thumbnail, otherwise false.
    #// @param int|WP_Post|null $post          Post ID or WP_Post object. Default is global `$post`.
    #// @param int|string       $thumbnail_id  Post thumbnail ID or empty string.
    #//
    return php_bool(apply_filters("has_post_thumbnail", has_thumbnail_, post_, thumbnail_id_))
# end def has_post_thumbnail
#// 
#// Retrieve post thumbnail ID.
#// 
#// @since 2.9.0
#// @since 4.4.0 `$post` can be a post ID or WP_Post object.
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global `$post`.
#// @return int|string Post thumbnail ID or empty string if the post does not exist.
#//
def get_post_thumbnail_id(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return ""
    # end if
    return php_int(get_post_meta(post_.ID, "_thumbnail_id", True))
# end def get_post_thumbnail_id
#// 
#// Display the post thumbnail.
#// 
#// When a theme adds 'post-thumbnail' support, a special 'post-thumbnail' image size
#// is registered, which differs from the 'thumbnail' image size managed via the
#// Settings > Media screen.
#// 
#// When using the_post_thumbnail() or related functions, the 'post-thumbnail' image
#// size is used by default, though a different size can be specified instead as needed.
#// 
#// @since 2.9.0
#// 
#// @see get_the_post_thumbnail()
#// 
#// @param string|array $size Optional. Image size to use. Accepts any valid image size, or
#// an array of width and height values in pixels (in that order).
#// Default 'post-thumbnail'.
#// @param string|array $attr Optional. Query string or array of attributes. Default empty.
#//
def the_post_thumbnail(size_="post-thumbnail", attr_="", *_args_):
    
    
    php_print(get_the_post_thumbnail(None, size_, attr_))
# end def the_post_thumbnail
#// 
#// Update cache for thumbnails in the current loop.
#// 
#// @since 3.2.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param WP_Query $wp_query Optional. A WP_Query instance. Defaults to the $wp_query global.
#//
def update_post_thumbnail_cache(wp_query_=None, *_args_):
    if wp_query_ is None:
        wp_query_ = None
    # end if
    
    if (not wp_query_):
        wp_query_ = PHP_GLOBALS["wp_query"]
    # end if
    if wp_query_.thumbnails_cached:
        return
    # end if
    thumb_ids_ = Array()
    for post_ in wp_query_.posts:
        id_ = get_post_thumbnail_id(post_.ID)
        if id_:
            thumb_ids_[-1] = id_
        # end if
    # end for
    if (not php_empty(lambda : thumb_ids_)):
        _prime_post_caches(thumb_ids_, False, True)
    # end if
    wp_query_.thumbnails_cached = True
# end def update_post_thumbnail_cache
#// 
#// Retrieve the post thumbnail.
#// 
#// When a theme adds 'post-thumbnail' support, a special 'post-thumbnail' image size
#// is registered, which differs from the 'thumbnail' image size managed via the
#// Settings > Media screen.
#// 
#// When using the_post_thumbnail() or related functions, the 'post-thumbnail' image
#// size is used by default, though a different size can be specified instead as needed.
#// 
#// @since 2.9.0
#// @since 4.4.0 `$post` can be a post ID or WP_Post object.
#// 
#// @param int|WP_Post  $post Optional. Post ID or WP_Post object.  Default is global `$post`.
#// @param string|array $size Optional. Image size to use. Accepts any valid image size, or
#// an array of width and height values in pixels (in that order).
#// Default 'post-thumbnail'.
#// @param string|array $attr Optional. Query string or array of attributes. Default empty.
#// @return string The post thumbnail image tag.
#//
def get_the_post_thumbnail(post_=None, size_="post-thumbnail", attr_="", *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return ""
    # end if
    post_thumbnail_id_ = get_post_thumbnail_id(post_)
    #// 
    #// Filters the post thumbnail size.
    #// 
    #// @since 2.9.0
    #// @since 4.9.0 Added the `$post_id` parameter.
    #// 
    #// @param string|array $size    The post thumbnail size. Image size or array of width and height
    #// values (in that order). Default 'post-thumbnail'.
    #// @param int          $post_id The post ID.
    #//
    size_ = apply_filters("post_thumbnail_size", size_, post_.ID)
    if post_thumbnail_id_:
        #// 
        #// Fires before fetching the post thumbnail HTML.
        #// 
        #// Provides "just in time" filtering of all filters in wp_get_attachment_image().
        #// 
        #// @since 2.9.0
        #// 
        #// @param int          $post_id           The post ID.
        #// @param string       $post_thumbnail_id The post thumbnail ID.
        #// @param string|array $size              The post thumbnail size. Image size or array of width
        #// and height values (in that order). Default 'post-thumbnail'.
        #//
        do_action("begin_fetch_post_thumbnail_html", post_.ID, post_thumbnail_id_, size_)
        if in_the_loop():
            update_post_thumbnail_cache()
        # end if
        html_ = wp_get_attachment_image(post_thumbnail_id_, size_, False, attr_)
        #// 
        #// Fires after fetching the post thumbnail HTML.
        #// 
        #// @since 2.9.0
        #// 
        #// @param int          $post_id           The post ID.
        #// @param string       $post_thumbnail_id The post thumbnail ID.
        #// @param string|array $size              The post thumbnail size. Image size or array of width
        #// and height values (in that order). Default 'post-thumbnail'.
        #//
        do_action("end_fetch_post_thumbnail_html", post_.ID, post_thumbnail_id_, size_)
    else:
        html_ = ""
    # end if
    #// 
    #// Filters the post thumbnail HTML.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string       $html              The post thumbnail HTML.
    #// @param int          $post_id           The post ID.
    #// @param string       $post_thumbnail_id The post thumbnail ID.
    #// @param string|array $size              The post thumbnail size. Image size or array of width and height
    #// values (in that order). Default 'post-thumbnail'.
    #// @param string       $attr              Query string of attributes.
    #//
    return apply_filters("post_thumbnail_html", html_, post_.ID, post_thumbnail_id_, size_, attr_)
# end def get_the_post_thumbnail
#// 
#// Return the post thumbnail URL.
#// 
#// @since 4.4.0
#// 
#// @param int|WP_Post  $post Optional. Post ID or WP_Post object.  Default is global `$post`.
#// @param string|array $size Optional. Registered image size to retrieve the source for or a flat
#// array of height and width dimensions. Default 'post-thumbnail'.
#// @return string|false Post thumbnail URL or false if no URL is available.
#//
def get_the_post_thumbnail_url(post_=None, size_="post-thumbnail", *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_thumbnail_id_ = get_post_thumbnail_id(post_)
    if (not post_thumbnail_id_):
        return False
    # end if
    return wp_get_attachment_image_url(post_thumbnail_id_, size_)
# end def get_the_post_thumbnail_url
#// 
#// Display the post thumbnail URL.
#// 
#// @since 4.4.0
#// 
#// @param string|array $size Optional. Image size to use. Accepts any valid image size,
#// or an array of width and height values in pixels (in that order).
#// Default 'post-thumbnail'.
#//
def the_post_thumbnail_url(size_="post-thumbnail", *_args_):
    
    
    url_ = get_the_post_thumbnail_url(None, size_)
    if url_:
        php_print(esc_url(url_))
    # end if
# end def the_post_thumbnail_url
#// 
#// Returns the post thumbnail caption.
#// 
#// @since 4.6.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global `$post`.
#// @return string Post thumbnail caption.
#//
def get_the_post_thumbnail_caption(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_thumbnail_id_ = get_post_thumbnail_id(post_)
    if (not post_thumbnail_id_):
        return ""
    # end if
    caption_ = wp_get_attachment_caption(post_thumbnail_id_)
    if (not caption_):
        caption_ = ""
    # end if
    return caption_
# end def get_the_post_thumbnail_caption
#// 
#// Displays the post thumbnail caption.
#// 
#// @since 4.6.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global `$post`.
#//
def the_post_thumbnail_caption(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    #// 
    #// Filters the displayed post thumbnail caption.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $caption Caption for the given attachment.
    #//
    php_print(apply_filters("the_post_thumbnail_caption", get_the_post_thumbnail_caption(post_)))
# end def the_post_thumbnail_caption
