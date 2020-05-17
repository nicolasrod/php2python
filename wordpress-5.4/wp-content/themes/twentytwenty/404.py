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
#// The template for displaying the 404 template in the Twenty Twenty theme.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
get_header()
php_print("""
<main id=\"site-content\" role=\"main\">
<div class=\"section-inner thin error404-content\">
<h1 class=\"entry-title\">""")
_e("Page Not Found", "twentytwenty")
php_print("</h1>\n\n        <div class=\"intro-text\"><p>")
_e("The page you were looking for could not be found. It might have been removed, renamed, or did not exist in the first place.", "twentytwenty")
php_print("</p></div>\n\n       ")
get_search_form(Array({"label": __("404 not found", "twentytwenty")}))
php_print("""
</div><!-- .section-inner -->
</main><!-- #site-content -->
""")
get_template_part("template-parts/footer-menus-widgets")
php_print("\n")
get_footer()
