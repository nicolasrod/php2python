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
#// The template for displaying search results pages
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy/#search-result
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
get_header()
php_print("""
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\">
""")
if have_posts():
    php_print("""
    <header class=\"page-header\">
    <h1 class=\"page-title\">
    """)
    _e("Search results for: ", "twentynineteen")
    php_print("                 <span class=\"page-description\">")
    php_print(get_search_query())
    php_print("""</span>
    </h1>
    </header><!-- .page-header -->
    """)
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
        get_template_part("template-parts/content/content", "excerpt")
        pass
    # end while
    #// Previous/next page navigation.
    twentynineteen_the_posts_navigation()
    pass
else:
    get_template_part("template-parts/content/content", "none")
# end if
php_print("""       </main><!-- #main -->
</div><!-- #primary -->
""")
get_footer()
