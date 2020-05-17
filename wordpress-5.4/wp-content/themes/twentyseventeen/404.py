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
#// The template for displaying 404 pages (not found)
#// 
#// @link https://codex.wordpress.org/Creating_an_Error_404_Page
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// @version 1.0
#//
get_header()
php_print("""
<div class=\"wrap\">
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\" role=\"main\">
<section class=\"error-404 not-found\">
<header class=\"page-header\">
<h1 class=\"page-title\">""")
_e("Oops! That page can&rsquo;t be found.", "twentyseventeen")
php_print("""</h1>
</header><!-- .page-header -->
<div class=\"page-content\">
<p>""")
_e("It looks like nothing was found at this location. Maybe try a search?", "twentyseventeen")
php_print("</p>\n\n                 ")
get_search_form()
php_print("""
</div><!-- .page-content -->
</section><!-- .error-404 -->
</main><!-- #main -->
</div><!-- #primary -->
</div><!-- .wrap -->
""")
get_footer()
