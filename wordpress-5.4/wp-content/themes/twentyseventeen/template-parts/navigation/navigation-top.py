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
php_print("<nav id=\"site-navigation\" class=\"main-navigation\" role=\"navigation\" aria-label=\"")
esc_attr_e("Top Menu", "twentyseventeen")
php_print("\">\n    <button class=\"menu-toggle\" aria-controls=\"top-menu\" aria-expanded=\"false\">\n     ")
php_print(twentyseventeen_get_svg(Array({"icon": "bars"})))
php_print(twentyseventeen_get_svg(Array({"icon": "close"})))
_e("Menu", "twentyseventeen")
php_print(" </button>\n\n   ")
wp_nav_menu(Array({"theme_location": "top", "menu_id": "top-menu"}))
php_print("\n   ")
if twentyseventeen_is_frontpage() or is_home() and is_front_page() and has_custom_header():
    php_print("     <a href=\"#content\" class=\"menu-scroll-down\">")
    php_print(twentyseventeen_get_svg(Array({"icon": "arrow-right"})))
    php_print("<span class=\"screen-reader-text\">")
    _e("Scroll down to content", "twentyseventeen")
    php_print("</span></a>\n    ")
# end if
php_print("</nav><!-- #site-navigation -->\n")
