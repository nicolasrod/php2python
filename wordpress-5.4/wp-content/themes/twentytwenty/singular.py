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
#// The template for displaying single posts and pages.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
get_header()
php_print("""
<main id=\"site-content\" role=\"main\">
""")
if have_posts():
    while True:
        
        if not (have_posts()):
            break
        # end if
        the_post()
        get_template_part("template-parts/content", get_post_type())
    # end while
# end if
php_print("""
</main><!-- #site-content -->
""")
get_template_part("template-parts/footer-menus-widgets")
php_print("\n")
get_footer()
