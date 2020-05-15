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
pass
php_print("<div class=\"site-branding\">\n\n    ")
if has_custom_logo():
    php_print("     <div class=\"site-logo\">")
    the_custom_logo()
    php_print("</div>\n ")
# end if
php_print(" ")
blog_info = get_bloginfo("name")
php_print(" ")
if (not php_empty(lambda : blog_info)):
    php_print("     ")
    if is_front_page() and is_home():
        php_print("         <h1 class=\"site-title\"><a href=\"")
        php_print(esc_url(home_url("/")))
        php_print("\" rel=\"home\">")
        bloginfo("name")
        php_print("</a></h1>\n      ")
    else:
        php_print("         <p class=\"site-title\"><a href=\"")
        php_print(esc_url(home_url("/")))
        php_print("\" rel=\"home\">")
        bloginfo("name")
        php_print("</a></p>\n       ")
    # end if
    php_print(" ")
# end if
php_print("\n   ")
description = get_bloginfo("description", "display")
if description or is_customize_preview():
    php_print("         <p class=\"site-description\">\n                ")
    php_print(description)
    php_print("         </p>\n  ")
# end if
php_print(" ")
if has_nav_menu("menu-1"):
    php_print("     <nav id=\"site-navigation\" class=\"main-navigation\" aria-label=\"")
    esc_attr_e("Top Menu", "twentynineteen")
    php_print("\">\n            ")
    wp_nav_menu(Array({"theme_location": "menu-1", "menu_class": "main-menu", "items_wrap": "<ul id=\"%1$s\" class=\"%2$s\">%3$s</ul>"}))
    php_print("     </nav><!-- #site-navigation -->\n   ")
# end if
php_print(" ")
if has_nav_menu("social"):
    php_print("     <nav class=\"social-navigation\" aria-label=\"")
    esc_attr_e("Social Links Menu", "twentynineteen")
    php_print("\">\n            ")
    wp_nav_menu(Array({"theme_location": "social", "menu_class": "social-links-menu", "link_before": "<span class=\"screen-reader-text\">", "link_after": "</span>" + twentynineteen_get_icon_svg("link"), "depth": 1}))
    php_print("     </nav><!-- .social-navigation -->\n ")
# end if
php_print("</div><!-- .site-branding -->\n")
