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
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
get_header()
php_print("""
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\">
""")
if have_posts():
    #// Load posts loop.
    while True:
        
        if not (have_posts()):
            break
        # end if
        the_post()
        get_template_part("template-parts/content/content")
    # end while
    #// Previous/next page navigation.
    twentynineteen_the_posts_navigation()
else:
    #// If no content, include the "No posts found" template.
    get_template_part("template-parts/content/content", "none")
# end if
php_print("""
</main><!-- .site-main -->
</div><!-- .content-area -->
""")
get_footer()
