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
#// The template for displaying Author info
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
if php_bool(get_the_author_meta("description")):
    php_print("""<div class=\"author-bio\">
    <h2 class=\"author-title\">
    <span class=\"author-heading\">
    """)
    printf(__("Published by %s", "twentynineteen"), esc_html(get_the_author()))
    php_print("""       </span>
    </h2>
    <p class=\"author-description\">
    """)
    the_author_meta("description")
    php_print("     <a class=\"author-link\" href=\"")
    php_print(esc_url(get_author_posts_url(get_the_author_meta("ID"))))
    php_print("\" rel=\"author\">\n         ")
    _e("View more posts", "twentynineteen")
    php_print("""       </a>
    </p><!-- .author-description -->
    </div><!-- .author-bio -->
    """)
# end if
