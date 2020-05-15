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
php_print("""
</div><!-- #content -->
<footer id=\"colophon\" class=\"site-footer\" role=\"contentinfo\">
<div class=\"wrap\">
""")
get_template_part("template-parts/footer/footer", "widgets")
if has_nav_menu("social"):
    php_print("                 <nav class=\"social-navigation\" role=\"navigation\" aria-label=\"")
    esc_attr_e("Footer Social Links Menu", "twentyseventeen")
    php_print("\">\n                        ")
    wp_nav_menu(Array({"theme_location": "social", "menu_class": "social-links-menu", "depth": 1, "link_before": "<span class=\"screen-reader-text\">", "link_after": "</span>" + twentyseventeen_get_svg(Array({"icon": "chain"}))}))
    php_print("                 </nav><!-- .social-navigation -->\n                 ")
# end if
get_template_part("template-parts/footer/site", "info")
php_print("""           </div><!-- .wrap -->
</footer><!-- #colophon -->
</div><!-- .site-content-contain -->
</div><!-- #page -->
""")
wp_footer()
php_print("""
</body>
</html>
""")
