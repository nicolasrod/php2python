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
#// Server-side rendering of the `core/latest-comments` block.
#// 
#// @package WordPress
#// 
#// 
#// Get the post title.
#// 
#// The post title is fetched and if it is blank then a default string is
#// returned.
#// 
#// Copied from `wp-admin/includes/template.php`, but we can't include that
#// file because:
#// 
#// 1. It causes bugs with test fixture generation and strange Docker 255 error
#// codes.
#// 2. It's in the admin; ideally we *shouldn't* be including files from the
#// admin for a block's output. It's a very small/simple function as well,
#// so duplicating it isn't too terrible.
#// 
#// @since 3.3.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string The post title if set; "(no title)" if no title is set.
#//
def wp_latest_comments_draft_or_post_title(post=0, *args_):
    
    title = get_the_title(post)
    if php_empty(lambda : title):
        title = __("(no title)")
    # end if
    return esc_html(title)
# end def wp_latest_comments_draft_or_post_title
#// 
#// Renders the `core/latest-comments` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the post content with latest comments added.
#//
def render_block_core_latest_comments(attributes=Array(), *args_):
    
    #// This filter is documented in wp-includes/widgets/class-wp-widget-recent-comments.php.
    comments = get_comments(apply_filters("widget_comments_args", Array({"number": attributes["commentsToShow"], "status": "approve", "post_status": "publish"})))
    list_items_markup = ""
    if (not php_empty(lambda : comments)):
        #// Prime the cache for associated posts. This is copied from \WP_Widget_Recent_Comments::widget().
        post_ids = array_unique(wp_list_pluck(comments, "comment_post_ID"))
        _prime_post_caches(post_ids, php_strpos(get_option("permalink_structure"), "%category%"), False)
        for comment in comments:
            list_items_markup += "<li class=\"wp-block-latest-comments__comment\">"
            if attributes["displayAvatar"]:
                avatar = get_avatar(comment, 48, "", "", Array({"class": "wp-block-latest-comments__comment-avatar"}))
                if avatar:
                    list_items_markup += avatar
                # end if
            # end if
            list_items_markup += "<article>"
            list_items_markup += "<footer class=\"wp-block-latest-comments__comment-meta\">"
            author_url = get_comment_author_url(comment)
            if php_empty(lambda : author_url) and (not php_empty(lambda : comment.user_id)):
                author_url = get_author_posts_url(comment.user_id)
            # end if
            author_markup = ""
            if author_url:
                author_markup += "<a class=\"wp-block-latest-comments__comment-author\" href=\"" + esc_url(author_url) + "\">" + get_comment_author(comment) + "</a>"
            else:
                author_markup += "<span class=\"wp-block-latest-comments__comment-author\">" + get_comment_author(comment) + "</span>"
            # end if
            #// `_draft_or_post_title` calls `esc_html()` so we don't need to wrap that call in
            #// `esc_html`.
            post_title = "<a class=\"wp-block-latest-comments__comment-link\" href=\"" + esc_url(get_comment_link(comment)) + "\">" + wp_latest_comments_draft_or_post_title(comment.comment_post_ID) + "</a>"
            list_items_markup += php_sprintf(__("%1$s on %2$s"), author_markup, post_title)
            if attributes["displayDate"]:
                list_items_markup += php_sprintf("<time datetime=\"%1$s\" class=\"wp-block-latest-comments__comment-date\">%2$s</time>", esc_attr(get_comment_date("c", comment)), date_i18n(get_option("date_format"), get_comment_date("U", comment)))
            # end if
            list_items_markup += "</footer>"
            if attributes["displayExcerpt"]:
                list_items_markup += "<div class=\"wp-block-latest-comments__comment-excerpt\">" + wpautop(get_comment_excerpt(comment)) + "</div>"
            # end if
            list_items_markup += "</article></li>"
        # end for
    # end if
    class_ = "wp-block-latest-comments"
    if (not php_empty(lambda : attributes["className"])):
        class_ += " " + attributes["className"]
    # end if
    if (php_isset(lambda : attributes["align"])):
        class_ += str(" align") + str(attributes["align"])
    # end if
    if attributes["displayAvatar"]:
        class_ += " has-avatars"
    # end if
    if attributes["displayDate"]:
        class_ += " has-dates"
    # end if
    if attributes["displayExcerpt"]:
        class_ += " has-excerpts"
    # end if
    if php_empty(lambda : comments):
        class_ += " no-comments"
    # end if
    classnames = esc_attr(class_)
    return php_sprintf("<ol class=\"%1$s\">%2$s</ol>", classnames, list_items_markup) if (not php_empty(lambda : comments)) else php_sprintf("<div class=\"%1$s\">%2$s</div>", classnames, __("No comments to show."))
# end def render_block_core_latest_comments
#// 
#// Registers the `core/latest-comments` block.
#//
def register_block_core_latest_comments(*args_):
    
    register_block_type("core/latest-comments", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"commentsToShow": Array({"type": "number", "default": 5, "minimum": 1, "maximum": 100})}, {"displayAvatar": Array({"type": "boolean", "default": True})}, {"displayDate": Array({"type": "boolean", "default": True})}, {"displayExcerpt": Array({"type": "boolean", "default": True})})}, {"render_callback": "render_block_core_latest_comments"}))
# end def register_block_core_latest_comments
add_action("init", "register_block_core_latest_comments")
