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
php_print("""<div class=\"site-branding\">
<div class=\"wrap\">
""")
the_custom_logo()
php_print("\n       <div class=\"site-branding-text\">\n            ")
if is_front_page():
    php_print("             <h1 class=\"site-title\"><a href=\"")
    php_print(esc_url(home_url("/")))
    php_print("\" rel=\"home\">")
    bloginfo("name")
    php_print("</a></h1>\n          ")
else:
    php_print("             <p class=\"site-title\"><a href=\"")
    php_print(esc_url(home_url("/")))
    php_print("\" rel=\"home\">")
    bloginfo("name")
    php_print("</a></p>\n           ")
# end if
php_print("\n           ")
description = get_bloginfo("description", "display")
if description or is_customize_preview():
    php_print("             <p class=\"site-description\">")
    php_print(description)
    php_print("</p>\n           ")
# end if
php_print("     </div><!-- .site-branding-text -->\n\n      ")
if twentyseventeen_is_frontpage() or is_home() and is_front_page() and (not has_nav_menu("top")):
    php_print("     <a href=\"#content\" class=\"menu-scroll-down\">")
    php_print(twentyseventeen_get_svg(Array({"icon": "arrow-right"})))
    php_print("<span class=\"screen-reader-text\">")
    _e("Scroll down to content", "twentyseventeen")
    php_print("</span></a>\n    ")
# end if
php_print("""
</div><!-- .wrap -->
</div><!-- .site-branding -->
""")
