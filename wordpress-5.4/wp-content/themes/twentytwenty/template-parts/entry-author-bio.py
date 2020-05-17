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
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if php_bool(get_the_author_meta("description")) and php_bool(get_theme_mod("show_author_bio", True)):
    php_print("""<div class=\"author-bio\">
    <div class=\"author-title-wrapper\">
    <div class=\"author-avatar vcard\">
    """)
    php_print(get_avatar(get_the_author_meta("ID"), 160))
    php_print("     </div>\n        <h2 class=\"author-title heading-size-4\">\n            ")
    printf(__("By %s", "twentytwenty"), esc_html(get_the_author()))
    php_print("""       </h2>
    </div><!-- .author-name -->
    <div class=\"author-description\">
    """)
    php_print(wp_kses_post(wpautop(get_the_author_meta("description"))))
    php_print("     <a class=\"author-link\" href=\"")
    php_print(esc_url(get_author_posts_url(get_the_author_meta("ID"))))
    php_print("\" rel=\"author\">\n         ")
    _e("View Archive <span aria-hidden=\"true\">&rarr;</span>", "twentytwenty")
    php_print("""       </a>
    </div><!-- .author-description -->
    </div><!-- .author-bio -->
    """)
# end if
