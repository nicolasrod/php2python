#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
pass
php_print("<!DOCTYPE html>\n<html ")
language_attributes()
php_print(" class=\"no-js no-svg\">\n<head>\n<meta charset=\"")
bloginfo("charset")
php_print("""\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<link rel=\"profile\" href=\"http://gmpg.org/xfn/11\">
""")
wp_head()
php_print("</head>\n\n<body ")
body_class()
php_print(">\n")
wp_body_open()
php_print("<div id=\"page\" class=\"site\">\n   <a class=\"skip-link screen-reader-text\" href=\"#content\">")
_e("Skip to content", "twentyseventeen")
php_print("""</a>
<header id=\"masthead\" class=\"site-header\" role=\"banner\">
""")
get_template_part("template-parts/header/header", "image")
php_print("\n       ")
if has_nav_menu("top"):
    php_print("         <div class=\"navigation-top\">\n                <div class=\"wrap\">\n                  ")
    get_template_part("template-parts/navigation/navigation", "top")
    php_print("             </div><!-- .wrap -->\n          </div><!-- .navigation-top -->\n        ")
# end if
php_print("""
</header><!-- #masthead -->
""")
#// 
#// If a regular post or page, and not the front page, show the featured image.
#// Using get_queried_object_id() here since the $post global may not be set before a call to the_post().
#//
if is_single() or is_page() and (not twentyseventeen_is_frontpage()) and has_post_thumbnail(get_queried_object_id()):
    php_print("<div class=\"single-featured-image-header\">")
    php_print(get_the_post_thumbnail(get_queried_object_id(), "twentyseventeen-featured-image"))
    php_print("</div><!-- .single-featured-image-header -->")
# end if
php_print("""
<div class=\"site-content-contain\">
<div id=\"content\" class=\"site-content\">
""")
