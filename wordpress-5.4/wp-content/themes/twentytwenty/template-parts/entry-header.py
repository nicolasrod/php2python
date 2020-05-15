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
#// Displays the post header
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
entry_header_classes = ""
if is_singular():
    entry_header_classes += " header-footer-group"
# end if
php_print("\n<header class=\"entry-header has-text-align-center")
php_print(esc_attr(entry_header_classes))
php_print("""\">
<div class=\"entry-header-inner section-inner medium\">
""")
#// 
#// Allow child themes and plugins to filter the display of the categories in the entry header.
#// 
#// @since Twenty Twenty 1.0
#// 
#// @param bool   Whether to show the categories in header, Default true.
#//
show_categories = apply_filters("twentytwenty_show_categories_in_entry_header", True)
if True == show_categories and has_category():
    php_print("\n           <div class=\"entry-categories\">\n              <span class=\"screen-reader-text\">")
    _e("Categories", "twentytwenty")
    php_print("</span>\n                <div class=\"entry-categories-inner\">\n                    ")
    the_category(" ")
    php_print("""               </div><!-- .entry-categories-inner -->
    </div><!-- .entry-categories -->
    """)
# end if
if is_singular():
    the_title("<h1 class=\"entry-title\">", "</h1>")
else:
    the_title("<h2 class=\"entry-title heading-size-1\"><a href=\"" + esc_url(get_permalink()) + "\">", "</a></h2>")
# end if
intro_text_width = ""
if is_singular():
    intro_text_width = " small"
else:
    intro_text_width = " thin"
# end if
if has_excerpt() and is_singular():
    php_print("\n           <div class=\"intro-text section-inner max-percentage")
    php_print(intro_text_width)
    pass
    php_print("\">\n                ")
    the_excerpt()
    php_print("         </div>\n\n          ")
# end if
#// Default to displaying the post meta.
twentytwenty_the_post_meta(get_the_ID(), "single-top")
php_print("""
</div><!-- .entry-header-inner -->
</header><!-- .entry-header -->
""")
