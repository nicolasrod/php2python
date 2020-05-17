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
#// The template for displaying all single posts
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy/#single-post
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
#// Start the Loop.
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    get_template_part("template-parts/post/content", get_post_format())
    #// If comments are open or we have at least one comment, load up the comment template.
    if comments_open() or get_comments_number():
        comments_template()
    # end if
    the_post_navigation(Array({"prev_text": "<span class=\"screen-reader-text\">" + __("Previous Post", "twentyseventeen") + "</span><span aria-hidden=\"true\" class=\"nav-subtitle\">" + __("Previous", "twentyseventeen") + "</span> <span class=\"nav-title\"><span class=\"nav-title-icon-wrapper\">" + twentyseventeen_get_svg(Array({"icon": "arrow-left"})) + "</span>%title</span>"}, {"next_text": "<span class=\"screen-reader-text\">" + __("Next Post", "twentyseventeen") + "</span><span aria-hidden=\"true\" class=\"nav-subtitle\">" + __("Next", "twentyseventeen") + "</span> <span class=\"nav-title\">%title<span class=\"nav-title-icon-wrapper\">" + twentyseventeen_get_svg(Array({"icon": "arrow-right"})) + "</span></span>"}))
# end while
pass
php_print("""
</main><!-- #main -->
</div><!-- #primary -->
""")
get_sidebar()
php_print("</div><!-- .wrap -->\n\n")
get_footer()
