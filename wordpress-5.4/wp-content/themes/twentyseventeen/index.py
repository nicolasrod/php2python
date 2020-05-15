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
#// The main template file
#// 
#// This is the most generic template file in a WordPress theme
#// and one of the two required files for a theme (the other being style.css).
#// It is used to display a page when nothing more specific matches a query.
#// E.g., it puts together the home page when no home.php file exists.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// @version 1.0
#//
get_header()
php_print("\n<div class=\"wrap\">\n ")
if is_home() and (not is_front_page()):
    php_print("     <header class=\"page-header\">\n            <h1 class=\"page-title\">")
    single_post_title()
    php_print("</h1>\n      </header>\n ")
else:
    php_print(" <header class=\"page-header\">\n        <h2 class=\"page-title\">")
    _e("Posts", "twentyseventeen")
    php_print("</h2>\n  </header>\n ")
# end if
php_print("""
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\" role=\"main\">
""")
if have_posts():
    #// Start the Loop.
    while True:
        
        if not (have_posts()):
            break
        # end if
        the_post()
        #// 
        #// Include the Post-Format-specific template for the content.
        #// If you want to override this in a child theme, then include a file
        #// called content-___.php (where ___ is the Post Format name) and that
        #// will be used instead.
        #//
        get_template_part("template-parts/post/content", get_post_format())
    # end while
    the_posts_pagination(Array({"prev_text": twentyseventeen_get_svg(Array({"icon": "arrow-left"})) + "<span class=\"screen-reader-text\">" + __("Previous page", "twentyseventeen") + "</span>"}, {"next_text": "<span class=\"screen-reader-text\">" + __("Next page", "twentyseventeen") + "</span>" + twentyseventeen_get_svg(Array({"icon": "arrow-right"}))}, {"before_page_number": "<span class=\"meta-nav screen-reader-text\">" + __("Page", "twentyseventeen") + " </span>"}))
else:
    get_template_part("template-parts/post/content", "none")
# end if
php_print("""
</main><!-- #main -->
</div><!-- #primary -->
""")
get_sidebar()
php_print("</div><!-- .wrap -->\n\n")
get_footer()
