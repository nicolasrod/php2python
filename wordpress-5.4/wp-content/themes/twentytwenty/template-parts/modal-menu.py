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
php_print("""
<div class=\"menu-modal cover-modal header-footer-group\" data-modal-target-string=\".menu-modal\">
<div class=\"menu-modal-inner modal-inner\">
<div class=\"menu-wrapper section-inner\">
<div class=\"menu-top\">
<button class=\"toggle close-nav-toggle fill-children-current-color\" data-toggle-target=\".menu-modal\" data-toggle-body-class=\"showing-menu-modal\" aria-expanded=\"false\" data-set-focus=\".menu-modal\">
<span class=\"toggle-text\">""")
_e("Close Menu", "twentytwenty")
php_print("</span>\n                    ")
twentytwenty_the_theme_svg("cross")
php_print("             </button><!-- .nav-toggle -->\n\n               ")
mobile_menu_location_ = ""
#// If the mobile menu location is not set, use the primary and expanded locations as fallbacks, in that order.
if has_nav_menu("mobile"):
    mobile_menu_location_ = "mobile"
elif has_nav_menu("primary"):
    mobile_menu_location_ = "primary"
elif has_nav_menu("expanded"):
    mobile_menu_location_ = "expanded"
# end if
if has_nav_menu("expanded"):
    expanded_nav_classes_ = ""
    if "expanded" == mobile_menu_location_:
        expanded_nav_classes_ += " mobile-menu"
    # end if
    php_print("\n                   <nav class=\"expanded-menu")
    php_print(esc_attr(expanded_nav_classes_))
    php_print("\" aria-label=\"")
    esc_attr_e("Expanded", "twentytwenty")
    php_print("""\" role=\"navigation\">
    <ul class=\"modal-menu reset-list-style\">
    """)
    if has_nav_menu("expanded"):
        wp_nav_menu(Array({"container": "", "items_wrap": "%3$s", "show_toggles": True, "theme_location": "expanded"}))
    # end if
    php_print("""                       </ul>
    </nav>
    """)
# end if
if "expanded" != mobile_menu_location_:
    php_print("\n                   <nav class=\"mobile-menu\" aria-label=\"")
    esc_attr_e("Mobile", "twentytwenty")
    php_print("""\" role=\"navigation\">
    <ul class=\"modal-menu reset-list-style\">
    """)
    if mobile_menu_location_:
        wp_nav_menu(Array({"container": "", "items_wrap": "%3$s", "show_toggles": True, "theme_location": mobile_menu_location_}))
    else:
        wp_list_pages(Array({"match_menu_classes": True, "show_toggles": True, "title_li": False, "walker": php_new_class("TwentyTwenty_Walker_Page", lambda : TwentyTwenty_Walker_Page())}))
    # end if
    php_print("""
    </ul>
    </nav>
    """)
# end if
php_print("""
</div><!-- .menu-top -->
<div class=\"menu-bottom\">
""")
if has_nav_menu("social"):
    php_print("\n                   <nav aria-label=\"")
    esc_attr_e("Expanded Social links", "twentytwenty")
    php_print("""\" role=\"navigation\">
    <ul class=\"social-menu reset-list-style social-icons fill-children-current-color\">
    """)
    wp_nav_menu(Array({"theme_location": "social", "container": "", "container_class": "", "items_wrap": "%3$s", "menu_id": "", "menu_class": "", "depth": 1, "link_before": "<span class=\"screen-reader-text\">", "link_after": "</span>", "fallback_cb": ""}))
    php_print("""
    </ul>
    </nav><!-- .social-menu -->
    """)
# end if
php_print("""
</div><!-- .menu-bottom -->
</div><!-- .menu-wrapper -->
</div><!-- .menu-modal-inner -->
</div><!-- .menu-modal -->
""")
