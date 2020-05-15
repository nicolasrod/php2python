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
#// Displays the menus and widgets at the end of the main element.
#// Visually, this output is presented as part of the footer element.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
has_footer_menu = has_nav_menu("footer")
has_social_menu = has_nav_menu("social")
has_sidebar_1 = is_active_sidebar("sidebar-1")
has_sidebar_2 = is_active_sidebar("sidebar-2")
#// Only output the container if there are elements to display.
if has_footer_menu or has_social_menu or has_sidebar_1 or has_sidebar_2:
    php_print("""
    <div class=\"footer-nav-widgets-wrapper header-footer-group\">
    <div class=\"footer-inner section-inner\">
    """)
    footer_top_classes = ""
    footer_top_classes += " has-footer-menu" if has_footer_menu else ""
    footer_top_classes += " has-social-menu" if has_social_menu else ""
    if has_footer_menu or has_social_menu:
        php_print("             <div class=\"footer-top")
        php_print(footer_top_classes)
        pass
        php_print("\">\n                    ")
        if has_footer_menu:
            php_print("\n                       <nav aria-label=\"")
            esc_attr_e("Footer", "twentytwenty")
            php_print("""\" role=\"navigation\" class=\"footer-menu-wrapper\">
            <ul class=\"footer-menu reset-list-style\">
            """)
            wp_nav_menu(Array({"container": "", "depth": 1, "items_wrap": "%3$s", "theme_location": "footer"}))
            php_print("""                           </ul>
            </nav><!-- .site-nav -->
            """)
        # end if
        php_print("                 ")
        if has_social_menu:
            php_print("\n                       <nav aria-label=\"")
            esc_attr_e("Social links", "twentytwenty")
            php_print("""\" class=\"footer-social-wrapper\">
            <ul class=\"social-menu footer-social reset-list-style social-icons fill-children-current-color\">
            """)
            wp_nav_menu(Array({"theme_location": "social", "container": "", "container_class": "", "items_wrap": "%3$s", "menu_id": "", "menu_class": "", "depth": 1, "link_before": "<span class=\"screen-reader-text\">", "link_after": "</span>", "fallback_cb": ""}))
            php_print("""
            </ul><!-- .footer-social -->
            </nav><!-- .footer-social-wrapper -->
            """)
        # end if
        php_print("             </div><!-- .footer-top -->\n\n          ")
    # end if
    php_print("\n           ")
    if has_sidebar_1 or has_sidebar_2:
        php_print("""
        <aside class=\"footer-widgets-outer-wrapper\" role=\"complementary\">
        <div class=\"footer-widgets-wrapper\">
        """)
        if has_sidebar_1:
            php_print("\n                           <div class=\"footer-widgets column-one grid-item\">\n                               ")
            dynamic_sidebar("sidebar-1")
            php_print("                         </div>\n\n                      ")
        # end if
        php_print("\n                       ")
        if has_sidebar_2:
            php_print("\n                           <div class=\"footer-widgets column-two grid-item\">\n                               ")
            dynamic_sidebar("sidebar-2")
            php_print("                         </div>\n\n                      ")
        # end if
        php_print("""
        </div><!-- .footer-widgets-wrapper -->
        </aside><!-- .footer-widgets-outer-wrapper -->
        """)
    # end if
    php_print("""
    </div><!-- .footer-inner -->
    </div><!-- .footer-nav-widgets-wrapper -->
    """)
# end if
