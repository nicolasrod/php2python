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
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// @version 1.0
#//
get_header()
php_print("""
<div class=\"wrap\">
<header class=\"page-header\">
""")
if have_posts():
    php_print("         <h1 class=\"page-title\">\n         ")
    #// translators: Search query.
    php_printf(__("Search Results for: %s", "twentyseventeen"), "<span>" + get_search_query() + "</span>")
    php_print("         </h1>\n     ")
else:
    php_print("         <h1 class=\"page-title\">")
    _e("Nothing Found", "twentyseventeen")
    php_print("</h1>\n      ")
# end if
php_print("""   </header><!-- .page-header -->
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
        #// Run the loop for the search to output the results.
        #// If you want to overload this in a child theme then include a file
        #// called content-search.php and that will be used instead.
        #//
        get_template_part("template-parts/post/content", "excerpt")
    # end while
    #// End the loop.
    the_posts_pagination(Array({"prev_text": twentyseventeen_get_svg(Array({"icon": "arrow-left"})) + "<span class=\"screen-reader-text\">" + __("Previous page", "twentyseventeen") + "</span>"}, {"next_text": "<span class=\"screen-reader-text\">" + __("Next page", "twentyseventeen") + "</span>" + twentyseventeen_get_svg(Array({"icon": "arrow-right"}))}, {"before_page_number": "<span class=\"meta-nav screen-reader-text\">" + __("Page", "twentyseventeen") + " </span>"}))
else:
    php_print("\n           <p>")
    _e("Sorry, but nothing matched your search terms. Please try again with some different keywords.", "twentyseventeen")
    php_print("</p>\n           ")
    get_search_form()
# end if
php_print("""
</main><!-- #main -->
</div><!-- #primary -->
""")
get_sidebar()
php_print("</div><!-- .wrap -->\n\n")
get_footer()
