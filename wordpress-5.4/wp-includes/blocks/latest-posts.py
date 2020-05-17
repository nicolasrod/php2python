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
block_core_latest_posts_excerpt_length_ = 0
#// 
#// Callback for the excerpt_length filter used by
#// the Latest Posts block at render time.
#// 
#// @return int Returns the global $block_core_latest_posts_excerpt_length variable
#// to allow the excerpt_length filter respect the Latest Block setting.
#//
def block_core_latest_posts_get_excerpt_length(*_args_):
    
    
    global block_core_latest_posts_excerpt_length_
    php_check_if_defined("block_core_latest_posts_excerpt_length_")
    return block_core_latest_posts_excerpt_length_
# end def block_core_latest_posts_get_excerpt_length
#// 
#// Renders the `core/latest-posts` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the post content with latest posts added.
#//
def render_block_core_latest_posts(attributes_=None, *_args_):
    
    
    global block_core_latest_posts_excerpt_length_
    php_check_if_defined("block_core_latest_posts_excerpt_length_")
    args_ = Array({"posts_per_page": attributes_["postsToShow"], "post_status": "publish", "order": attributes_["order"], "orderby": attributes_["orderBy"], "suppress_filters": False})
    block_core_latest_posts_excerpt_length_ = attributes_["excerptLength"]
    add_filter("excerpt_length", "block_core_latest_posts_get_excerpt_length", 20)
    if (php_isset(lambda : attributes_["categories"])):
        args_["category"] = attributes_["categories"]
    # end if
    recent_posts_ = get_posts(args_)
    list_items_markup_ = ""
    for post_ in recent_posts_:
        list_items_markup_ += "<li>"
        if attributes_["displayFeaturedImage"] and has_post_thumbnail(post_):
            image_style_ = ""
            if (php_isset(lambda : attributes_["featuredImageSizeWidth"])):
                image_style_ += php_sprintf("max-width:%spx;", attributes_["featuredImageSizeWidth"])
            # end if
            if (php_isset(lambda : attributes_["featuredImageSizeHeight"])):
                image_style_ += php_sprintf("max-height:%spx;", attributes_["featuredImageSizeHeight"])
            # end if
            image_classes_ = "wp-block-latest-posts__featured-image"
            if (php_isset(lambda : attributes_["featuredImageAlign"])):
                image_classes_ += " align" + attributes_["featuredImageAlign"]
            # end if
            list_items_markup_ += php_sprintf("<div class=\"%1$s\">%2$s</div>", image_classes_, get_the_post_thumbnail(post_, attributes_["featuredImageSizeSlug"], Array({"style": image_style_})))
        # end if
        title_ = get_the_title(post_)
        if (not title_):
            title_ = __("(no title)")
        # end if
        list_items_markup_ += php_sprintf("<a href=\"%1$s\">%2$s</a>", esc_url(get_permalink(post_)), title_)
        if (php_isset(lambda : attributes_["displayPostDate"])) and attributes_["displayPostDate"]:
            list_items_markup_ += php_sprintf("<time datetime=\"%1$s\" class=\"wp-block-latest-posts__post-date\">%2$s</time>", esc_attr(get_the_date("c", post_)), esc_html(get_the_date("", post_)))
        # end if
        if (php_isset(lambda : attributes_["displayPostContent"])) and attributes_["displayPostContent"] and (php_isset(lambda : attributes_["displayPostContentRadio"])) and "excerpt" == attributes_["displayPostContentRadio"]:
            trimmed_excerpt_ = get_the_excerpt(post_)
            list_items_markup_ += php_sprintf("<div class=\"wp-block-latest-posts__post-excerpt\">%1$s", trimmed_excerpt_)
            if php_strpos(trimmed_excerpt_, " &hellip; ") != False:
                list_items_markup_ += php_sprintf("<a href=\"%1$s\">%2$s</a></div>", esc_url(get_permalink(post_)), __("Read more"))
            else:
                list_items_markup_ += php_sprintf("</div>")
            # end if
        # end if
        if (php_isset(lambda : attributes_["displayPostContent"])) and attributes_["displayPostContent"] and (php_isset(lambda : attributes_["displayPostContentRadio"])) and "full_post" == attributes_["displayPostContentRadio"]:
            list_items_markup_ += php_sprintf("<div class=\"wp-block-latest-posts__post-full-content\">%1$s</div>", wp_kses_post(html_entity_decode(post_.post_content, ENT_QUOTES, get_option("blog_charset"))))
        # end if
        list_items_markup_ += "</li>\n"
    # end for
    remove_filter("excerpt_length", "block_core_latest_posts_get_excerpt_length", 20)
    class_ = "wp-block-latest-posts wp-block-latest-posts__list"
    if (php_isset(lambda : attributes_["align"])):
        class_ += " align" + attributes_["align"]
    # end if
    if (php_isset(lambda : attributes_["postLayout"])) and "grid" == attributes_["postLayout"]:
        class_ += " is-grid"
    # end if
    if (php_isset(lambda : attributes_["columns"])) and "grid" == attributes_["postLayout"]:
        class_ += " columns-" + attributes_["columns"]
    # end if
    if (php_isset(lambda : attributes_["displayPostDate"])) and attributes_["displayPostDate"]:
        class_ += " has-dates"
    # end if
    if (php_isset(lambda : attributes_["className"])):
        class_ += " " + attributes_["className"]
    # end if
    return php_sprintf("<ul class=\"%1$s\">%2$s</ul>", esc_attr(class_), list_items_markup_)
# end def render_block_core_latest_posts
#// 
#// Registers the `core/latest-posts` block on server.
#//
def register_block_core_latest_posts(*_args_):
    
    
    register_block_type("core/latest-posts", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"categories": Array({"type": "string"})}, {"postsToShow": Array({"type": "number", "default": 5})}, {"displayPostContent": Array({"type": "boolean", "default": False})}, {"displayPostContentRadio": Array({"type": "string", "default": "excerpt"})}, {"excerptLength": Array({"type": "number", "default": 55})}, {"displayPostDate": Array({"type": "boolean", "default": False})}, {"postLayout": Array({"type": "string", "default": "list"})}, {"columns": Array({"type": "number", "default": 3})}, {"order": Array({"type": "string", "default": "desc"})}, {"orderBy": Array({"type": "string", "default": "date"})}, {"displayFeaturedImage": Array({"type": "boolean", "default": False})}, {"featuredImageAlign": Array({"type": "string", "enum": Array("left", "center", "right")})}, {"featuredImageSizeSlug": Array({"type": "string", "default": "thumbnail"})}, {"featuredImageSizeWidth": Array({"type": "number", "default": None})}, {"featuredImageSizeHeight": Array({"type": "number", "default": None})})}, {"render_callback": "render_block_core_latest_posts"}))
# end def register_block_core_latest_posts
add_action("init", "register_block_core_latest_posts")
