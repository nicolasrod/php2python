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
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
get_header()
php_print("""
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\">
""")
#// Start the Loop.
while True:
    
    if not (have_posts()):
        break
    # end if
    the_post()
    get_template_part("template-parts/content/content", "single")
    if is_singular("attachment"):
        #// Parent post navigation.
        the_post_navigation(Array({"prev_text": php_sprintf(__("<span class=\"meta-nav\">Published in</span><span class=\"post-title\">%s</span>", "twentynineteen"), "%title")}))
    elif is_singular("post"):
        #// Previous/next post navigation.
        the_post_navigation(Array({"next_text": "<span class=\"meta-nav\" aria-hidden=\"true\">" + __("Next Post", "twentynineteen") + "</span> " + "<span class=\"screen-reader-text\">" + __("Next post:", "twentynineteen") + "</span> <br/>" + "<span class=\"post-title\">%title</span>", "prev_text": "<span class=\"meta-nav\" aria-hidden=\"true\">" + __("Previous Post", "twentynineteen") + "</span> " + "<span class=\"screen-reader-text\">" + __("Previous post:", "twentynineteen") + "</span> <br/>" + "<span class=\"post-title\">%title</span>"}))
    # end if
    #// If comments are open or we have at least one comment, load up the comment template.
    if comments_open() or get_comments_number():
        comments_template()
    # end if
# end while
pass
php_print("""
</main><!-- #main -->
</div><!-- #primary -->
""")
get_footer()
