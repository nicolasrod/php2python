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
#// Displays the next and previous post navigation in single posts.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
next_post = get_next_post()
prev_post = get_previous_post()
if next_post or prev_post:
    pagination_classes = ""
    if (not next_post):
        pagination_classes = " only-one only-prev"
    elif (not prev_post):
        pagination_classes = " only-one only-next"
    # end if
    php_print("\n   <nav class=\"pagination-single section-inner")
    php_print(esc_attr(pagination_classes))
    php_print("\" aria-label=\"")
    esc_attr_e("Post", "twentytwenty")
    php_print("""\" role=\"navigation\">
    <hr class=\"styled-separator is-style-wide\" aria-hidden=\"true\" />
    <div class=\"pagination-single-inner\">
    """)
    if prev_post:
        php_print("\n               <a class=\"previous-post\" href=\"")
        php_print(esc_url(get_permalink(prev_post.ID)))
        php_print("\">\n                    <span class=\"arrow\" aria-hidden=\"true\">&larr;</span>\n                  <span class=\"title\"><span class=\"title-inner\">")
        php_print(wp_kses_post(get_the_title(prev_post.ID)))
        php_print("""</span></span>
        </a>
        """)
    # end if
    if next_post:
        php_print("\n               <a class=\"next-post\" href=\"")
        php_print(esc_url(get_permalink(next_post.ID)))
        php_print("\">\n                    <span class=\"arrow\" aria-hidden=\"true\">&rarr;</span>\n                      <span class=\"title\"><span class=\"title-inner\">")
        php_print(wp_kses_post(get_the_title(next_post.ID)))
        php_print("</span></span>\n             </a>\n              ")
    # end if
    php_print("""
    </div><!-- .pagination-single-inner -->
    <hr class=\"styled-separator is-style-wide\" aria-hidden=\"true\" />
    </nav><!-- .pagination-single -->
    """)
# end if
