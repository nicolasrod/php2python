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
def wp_latest_comments_draft_or_post_title(post_=0, *_args_):
    
    
    title_ = get_the_title(post_)
    if php_empty(lambda : title_):
        title_ = __("(no title)")
    # end if
    return esc_html(title_)
# end def wp_latest_comments_draft_or_post_title
#// 
#// Renders the `core/latest-comments` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the post content with latest comments added.
#//
def render_block_core_latest_comments(attributes_=None, *_args_):
    if attributes_ is None:
        attributes_ = Array()
    # end if
    
    #// This filter is documented in wp-includes/widgets/class-wp-widget-recent-comments.php.
    comments_ = get_comments(apply_filters("widget_comments_args", Array({"number": attributes_["commentsToShow"], "status": "approve", "post_status": "publish"})))
    list_items_markup_ = ""
    if (not php_empty(lambda : comments_)):
        #// Prime the cache for associated posts. This is copied from \WP_Widget_Recent_Comments::widget().
        post_ids_ = array_unique(wp_list_pluck(comments_, "comment_post_ID"))
        _prime_post_caches(post_ids_, php_strpos(get_option("permalink_structure"), "%category%"), False)
        for comment_ in comments_:
            list_items_markup_ += "<li class=\"wp-block-latest-comments__comment\">"
            if attributes_["displayAvatar"]:
                avatar_ = get_avatar(comment_, 48, "", "", Array({"class": "wp-block-latest-comments__comment-avatar"}))
                if avatar_:
                    list_items_markup_ += avatar_
                # end if
            # end if
            list_items_markup_ += "<article>"
            list_items_markup_ += "<footer class=\"wp-block-latest-comments__comment-meta\">"
            author_url_ = get_comment_author_url(comment_)
            if php_empty(lambda : author_url_) and (not php_empty(lambda : comment_.user_id)):
                author_url_ = get_author_posts_url(comment_.user_id)
            # end if
            author_markup_ = ""
            if author_url_:
                author_markup_ += "<a class=\"wp-block-latest-comments__comment-author\" href=\"" + esc_url(author_url_) + "\">" + get_comment_author(comment_) + "</a>"
            else:
                author_markup_ += "<span class=\"wp-block-latest-comments__comment-author\">" + get_comment_author(comment_) + "</span>"
            # end if
            #// `_draft_or_post_title` calls `esc_html()` so we don't need to wrap that call in
            #// `esc_html`.
            post_title_ = "<a class=\"wp-block-latest-comments__comment-link\" href=\"" + esc_url(get_comment_link(comment_)) + "\">" + wp_latest_comments_draft_or_post_title(comment_.comment_post_ID) + "</a>"
            list_items_markup_ += php_sprintf(__("%1$s on %2$s"), author_markup_, post_title_)
            if attributes_["displayDate"]:
                list_items_markup_ += php_sprintf("<time datetime=\"%1$s\" class=\"wp-block-latest-comments__comment-date\">%2$s</time>", esc_attr(get_comment_date("c", comment_)), date_i18n(get_option("date_format"), get_comment_date("U", comment_)))
            # end if
            list_items_markup_ += "</footer>"
            if attributes_["displayExcerpt"]:
                list_items_markup_ += "<div class=\"wp-block-latest-comments__comment-excerpt\">" + wpautop(get_comment_excerpt(comment_)) + "</div>"
            # end if
            list_items_markup_ += "</article></li>"
        # end for
    # end if
    class_ = "wp-block-latest-comments"
    if (not php_empty(lambda : attributes_["className"])):
        class_ += " " + attributes_["className"]
    # end if
    if (php_isset(lambda : attributes_["align"])):
        class_ += str(" align") + str(attributes_["align"])
    # end if
    if attributes_["displayAvatar"]:
        class_ += " has-avatars"
    # end if
    if attributes_["displayDate"]:
        class_ += " has-dates"
    # end if
    if attributes_["displayExcerpt"]:
        class_ += " has-excerpts"
    # end if
    if php_empty(lambda : comments_):
        class_ += " no-comments"
    # end if
    classnames_ = esc_attr(class_)
    return php_sprintf("<ol class=\"%1$s\">%2$s</ol>", classnames_, list_items_markup_) if (not php_empty(lambda : comments_)) else php_sprintf("<div class=\"%1$s\">%2$s</div>", classnames_, __("No comments to show."))
# end def render_block_core_latest_comments
#// 
#// Registers the `core/latest-comments` block.
#//
def register_block_core_latest_comments(*_args_):
    
    
    register_block_type("core/latest-comments", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"commentsToShow": Array({"type": "number", "default": 5, "minimum": 1, "maximum": 100})}, {"displayAvatar": Array({"type": "boolean", "default": True})}, {"displayDate": Array({"type": "boolean", "default": True})}, {"displayExcerpt": Array({"type": "boolean", "default": True})})}, {"render_callback": "render_block_core_latest_comments"}))
# end def register_block_core_latest_comments
add_action("init", "register_block_core_latest_comments")
