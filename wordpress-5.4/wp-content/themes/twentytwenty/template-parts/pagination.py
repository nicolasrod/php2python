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
#// A template partial to output pagination for the Twenty Twenty default theme.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#// 
#// 
#// Translators:
#// This text contains HTML to allow the text to be shorter on small screens.
#// The text inside the span with the class nav-short will be hidden on small screens.
#//
prev_text_ = php_sprintf("%s <span class=\"nav-prev-text\">%s</span>", "<span aria-hidden=\"true\">&larr;</span>", __("Newer <span class=\"nav-short\">Posts</span>", "twentytwenty"))
next_text_ = php_sprintf("<span class=\"nav-next-text\">%s</span> %s", __("Older <span class=\"nav-short\">Posts</span>", "twentytwenty"), "<span aria-hidden=\"true\">&rarr;</span>")
posts_pagination_ = get_the_posts_pagination(Array({"mid_size": 1, "prev_text": prev_text_, "next_text": next_text_}))
#// If we're not outputting the previous page link, prepend a placeholder with `visibility: hidden` to take its place.
if php_strpos(posts_pagination_, "prev page-numbers") == False:
    posts_pagination_ = php_str_replace("<div class=\"nav-links\">", "<div class=\"nav-links\"><span class=\"prev page-numbers placeholder\" aria-hidden=\"true\">" + prev_text_ + "</span>", posts_pagination_)
# end if
#// If we're not outputting the next page link, append a placeholder with `visibility: hidden` to take its place.
if php_strpos(posts_pagination_, "next page-numbers") == False:
    posts_pagination_ = php_str_replace("</div>", "<span class=\"next page-numbers placeholder\" aria-hidden=\"true\">" + next_text_ + "</span></div>", posts_pagination_)
# end if
if posts_pagination_:
    php_print("""
    <div class=\"pagination-wrapper section-inner\">
    <hr class=\"styled-separator pagination-separator is-style-wide\" aria-hidden=\"true\" />
    """)
    php_print(posts_pagination_)
    pass
    php_print("""
    </div><!-- .pagination-wrapper -->
    """)
# end if
