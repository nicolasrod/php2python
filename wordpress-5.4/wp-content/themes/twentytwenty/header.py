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
php_print("<!DOCTYPE html>\n\n<html class=\"no-js\" ")
language_attributes()
php_print(""">
<head>
<meta charset=\"""")
bloginfo("charset")
php_print("""\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" >
<link rel=\"profile\" href=\"https://gmpg.org/xfn/11\">
""")
wp_head()
php_print("""
</head>
<body """)
body_class()
php_print(">\n\n        ")
wp_body_open()
php_print("""
<header id=\"site-header\" class=\"header-footer-group\" role=\"banner\">
<div class=\"header-inner section-inner\">
<div class=\"header-titles-wrapper\">
""")
#// Check whether the header search is activated in the customizer.
enable_header_search_ = get_theme_mod("enable_header_search", True)
if True == enable_header_search_:
    php_print("""
    <button class=\"toggle search-toggle mobile-search-toggle\" data-toggle-target=\".search-modal\" data-toggle-body-class=\"showing-search-modal\" data-set-focus=\".search-modal .search-field\" aria-expanded=\"false\">
    <span class=\"toggle-inner\">
    <span class=\"toggle-icon\">
    """)
    twentytwenty_the_theme_svg("search")
    php_print("                             </span>\n                               <span class=\"toggle-text\">")
    _e("Search", "twentytwenty")
    php_print("""</span>
    </span>
    </button><!-- .search-toggle -->
    """)
# end if
php_print("""
<div class=\"header-titles\">
""")
#// Site title or logo.
twentytwenty_site_logo()
#// Site description.
twentytwenty_site_description()
php_print("""
</div><!-- .header-titles -->
<button class=\"toggle nav-toggle mobile-nav-toggle\" data-toggle-target=\".menu-modal\"  data-toggle-body-class=\"showing-menu-modal\" aria-expanded=\"false\" data-set-focus=\".close-nav-toggle\">
<span class=\"toggle-inner\">
<span class=\"toggle-icon\">
""")
twentytwenty_the_theme_svg("ellipsis")
php_print("                         </span>\n                           <span class=\"toggle-text\">")
_e("Menu", "twentytwenty")
php_print("""</span>
</span>
</button><!-- .nav-toggle -->
</div><!-- .header-titles-wrapper -->
<div class=\"header-navigation-wrapper\">
""")
if has_nav_menu("primary") or (not has_nav_menu("expanded")):
    php_print("\n                           <nav class=\"primary-menu-wrapper\" aria-label=\"")
    esc_attr_e("Horizontal", "twentytwenty")
    php_print("""\" role=\"navigation\">
    <ul class=\"primary-menu reset-list-style\">
    """)
    if has_nav_menu("primary"):
        wp_nav_menu(Array({"container": "", "items_wrap": "%3$s", "theme_location": "primary"}))
    elif (not has_nav_menu("expanded")):
        wp_list_pages(Array({"match_menu_classes": True, "show_sub_menu_icons": True, "title_li": False, "walker": php_new_class("TwentyTwenty_Walker_Page", lambda : TwentyTwenty_Walker_Page())}))
    # end if
    php_print("""
    </ul>
    </nav><!-- .primary-menu-wrapper -->
    """)
# end if
if True == enable_header_search_ or has_nav_menu("expanded"):
    php_print("""
    <div class=\"header-toggles hide-no-js\">
    """)
    if has_nav_menu("expanded"):
        php_print("""
        <div class=\"toggle-wrapper nav-toggle-wrapper has-expanded-menu\">
        <button class=\"toggle nav-toggle desktop-nav-toggle\" data-toggle-target=\".menu-modal\" data-toggle-body-class=\"showing-menu-modal\" aria-expanded=\"false\" data-set-focus=\".close-nav-toggle\">
        <span class=\"toggle-inner\">
        <span class=\"toggle-text\">""")
        _e("Menu", "twentytwenty")
        php_print("</span>\n                                        <span class=\"toggle-icon\">\n                                          ")
        twentytwenty_the_theme_svg("ellipsis")
        php_print("""                                       </span>
        </span>
        </button><!-- .nav-toggle -->
        </div><!-- .nav-toggle-wrapper -->
        """)
    # end if
    if True == enable_header_search_:
        php_print("""
        <div class=\"toggle-wrapper search-toggle-wrapper\">
        <button class=\"toggle search-toggle desktop-search-toggle\" data-toggle-target=\".search-modal\" data-toggle-body-class=\"showing-search-modal\" data-set-focus=\".search-modal .search-field\" aria-expanded=\"false\">
        <span class=\"toggle-inner\">
        """)
        twentytwenty_the_theme_svg("search")
        php_print("                                     <span class=\"toggle-text\">")
        _e("Search", "twentytwenty")
        php_print("""</span>
        </span>
        </button><!-- .search-toggle -->
        </div>
        """)
    # end if
    php_print("\n                       </div><!-- .header-toggles -->\n                        ")
# end if
php_print("""
</div><!-- .header-navigation-wrapper -->
</div><!-- .header-inner -->
""")
#// Output the search modal (if it is activated in the customizer).
if True == enable_header_search_:
    get_template_part("template-parts/modal-search")
# end if
php_print("""
</header><!-- #site-header -->
""")
#// Output the menu modal.
get_template_part("template-parts/modal-menu")
