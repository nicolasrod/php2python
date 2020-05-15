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
#// Server-side rendering of the `core/latest-posts` block.
#// 
#// @package WordPress
#// 
#// 
#// The excerpt length set by the Latest Posts core block
#// set at render time and used by the block itself.
#// 
#// @var int
#//
block_core_latest_posts_excerpt_length = 0
#// 
#// Callback for the excerpt_length filter used by
#// the Latest Posts block at render time.
#// 
#// @return int Returns the global $block_core_latest_posts_excerpt_length variable
#// to allow the excerpt_length filter respect the Latest Block setting.
#//
def block_core_latest_posts_get_excerpt_length(*args_):
    
    global block_core_latest_posts_excerpt_length
    php_check_if_defined("block_core_latest_posts_excerpt_length")
    return block_core_latest_posts_excerpt_length
# end def block_core_latest_posts_get_excerpt_length
#// 
#// Renders the `core/latest-posts` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the post content with latest posts added.
#//
def render_block_core_latest_posts(attributes=None, *args_):
    
    global block_core_latest_posts_excerpt_length
    php_check_if_defined("block_core_latest_posts_excerpt_length")
    args = Array({"posts_per_page": attributes["postsToShow"], "post_status": "publish", "order": attributes["order"], "orderby": attributes["orderBy"], "suppress_filters": False})
    block_core_latest_posts_excerpt_length = attributes["excerptLength"]
    add_filter("excerpt_length", "block_core_latest_posts_get_excerpt_length", 20)
    if (php_isset(lambda : attributes["categories"])):
        args["category"] = attributes["categories"]
    # end if
    recent_posts = get_posts(args)
    list_items_markup = ""
    for post in recent_posts:
        list_items_markup += "<li>"
        if attributes["displayFeaturedImage"] and has_post_thumbnail(post):
            image_style = ""
            if (php_isset(lambda : attributes["featuredImageSizeWidth"])):
                image_style += php_sprintf("max-width:%spx;", attributes["featuredImageSizeWidth"])
            # end if
            if (php_isset(lambda : attributes["featuredImageSizeHeight"])):
                image_style += php_sprintf("max-height:%spx;", attributes["featuredImageSizeHeight"])
            # end if
            image_classes = "wp-block-latest-posts__featured-image"
            if (php_isset(lambda : attributes["featuredImageAlign"])):
                image_classes += " align" + attributes["featuredImageAlign"]
            # end if
            list_items_markup += php_sprintf("<div class=\"%1$s\">%2$s</div>", image_classes, get_the_post_thumbnail(post, attributes["featuredImageSizeSlug"], Array({"style": image_style})))
        # end if
        title = get_the_title(post)
        if (not title):
            title = __("(no title)")
        # end if
        list_items_markup += php_sprintf("<a href=\"%1$s\">%2$s</a>", esc_url(get_permalink(post)), title)
        if (php_isset(lambda : attributes["displayPostDate"])) and attributes["displayPostDate"]:
            list_items_markup += php_sprintf("<time datetime=\"%1$s\" class=\"wp-block-latest-posts__post-date\">%2$s</time>", esc_attr(get_the_date("c", post)), esc_html(get_the_date("", post)))
        # end if
        if (php_isset(lambda : attributes["displayPostContent"])) and attributes["displayPostContent"] and (php_isset(lambda : attributes["displayPostContentRadio"])) and "excerpt" == attributes["displayPostContentRadio"]:
            trimmed_excerpt = get_the_excerpt(post)
            list_items_markup += php_sprintf("<div class=\"wp-block-latest-posts__post-excerpt\">%1$s", trimmed_excerpt)
            if php_strpos(trimmed_excerpt, " &hellip; ") != False:
                list_items_markup += php_sprintf("<a href=\"%1$s\">%2$s</a></div>", esc_url(get_permalink(post)), __("Read more"))
            else:
                list_items_markup += php_sprintf("</div>")
            # end if
        # end if
        if (php_isset(lambda : attributes["displayPostContent"])) and attributes["displayPostContent"] and (php_isset(lambda : attributes["displayPostContentRadio"])) and "full_post" == attributes["displayPostContentRadio"]:
            list_items_markup += php_sprintf("<div class=\"wp-block-latest-posts__post-full-content\">%1$s</div>", wp_kses_post(html_entity_decode(post.post_content, ENT_QUOTES, get_option("blog_charset"))))
        # end if
        list_items_markup += "</li>\n"
    # end for
    remove_filter("excerpt_length", "block_core_latest_posts_get_excerpt_length", 20)
    class_ = "wp-block-latest-posts wp-block-latest-posts__list"
    if (php_isset(lambda : attributes["align"])):
        class_ += " align" + attributes["align"]
    # end if
    if (php_isset(lambda : attributes["postLayout"])) and "grid" == attributes["postLayout"]:
        class_ += " is-grid"
    # end if
    if (php_isset(lambda : attributes["columns"])) and "grid" == attributes["postLayout"]:
        class_ += " columns-" + attributes["columns"]
    # end if
    if (php_isset(lambda : attributes["displayPostDate"])) and attributes["displayPostDate"]:
        class_ += " has-dates"
    # end if
    if (php_isset(lambda : attributes["className"])):
        class_ += " " + attributes["className"]
    # end if
    return php_sprintf("<ul class=\"%1$s\">%2$s</ul>", esc_attr(class_), list_items_markup)
# end def render_block_core_latest_posts
#// 
#// Registers the `core/latest-posts` block on server.
#//
def register_block_core_latest_posts(*args_):
    
    register_block_type("core/latest-posts", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"categories": Array({"type": "string"})}, {"postsToShow": Array({"type": "number", "default": 5})}, {"displayPostContent": Array({"type": "boolean", "default": False})}, {"displayPostContentRadio": Array({"type": "string", "default": "excerpt"})}, {"excerptLength": Array({"type": "number", "default": 55})}, {"displayPostDate": Array({"type": "boolean", "default": False})}, {"postLayout": Array({"type": "string", "default": "list"})}, {"columns": Array({"type": "number", "default": 3})}, {"order": Array({"type": "string", "default": "desc"})}, {"orderBy": Array({"type": "string", "default": "date"})}, {"displayFeaturedImage": Array({"type": "boolean", "default": False})}, {"featuredImageAlign": Array({"type": "string", "enum": Array("left", "center", "right")})}, {"featuredImageSizeSlug": Array({"type": "string", "default": "thumbnail"})}, {"featuredImageSizeWidth": Array({"type": "number", "default": None})}, {"featuredImageSizeHeight": Array({"type": "number", "default": None})})}, {"render_callback": "render_block_core_latest_posts"}))
# end def register_block_core_latest_posts
add_action("init", "register_block_core_latest_posts")
