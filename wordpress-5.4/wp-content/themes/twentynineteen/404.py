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
#// The template for displaying 404 pages (not found)
#// 
#// @link https://codex.wordpress.org/Creating_an_Error_404_Page
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
get_header()
php_print("""
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\">
<div class=\"error-404 not-found\">
<header class=\"page-header\">
<h1 class=\"page-title\">""")
_e("Oops! That page can&rsquo;t be found.", "twentynineteen")
php_print("""</h1>
</header><!-- .page-header -->
<div class=\"page-content\">
<p>""")
_e("It looks like nothing was found at this location. Maybe try a search?", "twentynineteen")
php_print("</p>\n                   ")
get_search_form()
php_print("""               </div><!-- .page-content -->
</div><!-- .error-404 -->
</main><!-- #main -->
</div><!-- #primary -->
""")
get_footer()
