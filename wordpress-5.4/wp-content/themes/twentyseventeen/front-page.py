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
#// The front page template file
#// 
#// If the user has selected a static page for their homepage, this is what will
#// appear.
#// Learn more: https://developer.wordpress.org/themes/basics/template-hierarchy
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// @version 1.0
#//
get_header()
php_print("""
<div id=\"primary\" class=\"content-area\">
<main id=\"main\" class=\"site-main\" role=\"main\">
""")
#// Show the selected front page content.
if have_posts():
    while True:
        
        if not (have_posts()):
            break
        # end if
        the_post()
        get_template_part("template-parts/page/content", "front-page")
    # end while
else:
    get_template_part("template-parts/post/content", "none")
# end if
php_print("\n       ")
#// Get each of our panels and show the post data.
if 0 != twentyseventeen_panel_count() or is_customize_preview():
    #// If we have pages to show.
    #// 
    #// Filter number of front page sections in Twenty Seventeen.
    #// 
    #// @since Twenty Seventeen 1.0
    #// 
    #// @param int $num_sections Number of front page sections.
    #//
    num_sections = apply_filters("twentyseventeen_front_page_sections", 4)
    global twentyseventeencounter
    php_check_if_defined("twentyseventeencounter")
    #// Create a setting and control for each of the sections available in the theme.
    i = 1
    while i < 1 + num_sections:
        
        twentyseventeencounter = i
        twentyseventeen_front_page_section(None, i)
        i += 1
    # end while
# end if
pass
php_print("""
</main><!-- #main -->
</div><!-- #primary -->
""")
get_footer()
