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
#// Displays the featured image
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if has_post_thumbnail() and (not post_password_required()):
    featured_media_inner_classes = ""
    #// Make the featured media thinner on archive pages.
    if (not is_singular()):
        featured_media_inner_classes += " medium"
    # end if
    php_print("""
    <figure class=\"featured-media\">
    <div class=\"featured-media-inner section-inner""")
    php_print(featured_media_inner_classes)
    pass
    php_print("\">\n\n          ")
    the_post_thumbnail()
    caption = get_the_post_thumbnail_caption()
    if caption:
        php_print("\n               <figcaption class=\"wp-caption-text\">")
        php_print(esc_html(caption))
        php_print("</figcaption>\n\n                ")
    # end if
    php_print("""
    </div><!-- .featured-media-inner -->
    </figure><!-- .featured-media -->
    """)
# end if
