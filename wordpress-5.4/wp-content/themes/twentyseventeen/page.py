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
#// The template for displaying all pages
#// 
#// This is the template that displays all pages by default.
#// Please note that this is the WordPress construct of pages
#// and that other 'pages' on your WordPress site may use a
#// different template.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy
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
""")
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    get_template_part("template-parts/page/content", "page")
    #// If comments are open or we have at least one comment, load up the comment template.
    if comments_open() or get_comments_number():
        comments_template()
    # end if
# end while
pass
php_print("""
</main><!-- #main -->
</div><!-- #primary -->
</div><!-- .wrap -->
""")
get_footer()
