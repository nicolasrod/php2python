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
php_print("\n")
if is_active_sidebar("sidebar-2") or is_active_sidebar("sidebar-3"):
    php_print("\n   <aside class=\"widget-area\" role=\"complementary\" aria-label=\"")
    esc_attr_e("Footer", "twentyseventeen")
    php_print("\">\n        ")
    if is_active_sidebar("sidebar-2"):
        php_print("         <div class=\"widget-column footer-widget-1\">\n             ")
        dynamic_sidebar("sidebar-2")
        php_print("         </div>\n            ")
    # end if
    if is_active_sidebar("sidebar-3"):
        php_print("         <div class=\"widget-column footer-widget-2\">\n             ")
        dynamic_sidebar("sidebar-3")
        php_print("         </div>\n        ")
    # end if
    php_print(" </aside><!-- .widget-area -->\n\n")
# end if
