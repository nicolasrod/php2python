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
#// Displays the footer widget area
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#//
if is_active_sidebar("sidebar-1"):
    php_print("\n   <aside class=\"widget-area\" role=\"complementary\" aria-label=\"")
    esc_attr_e("Footer", "twentynineteen")
    php_print("\">\n        ")
    if is_active_sidebar("sidebar-1"):
        php_print("                 <div class=\"widget-column footer-widget-1\">\n                 ")
        dynamic_sidebar("sidebar-1")
        php_print("                 </div>\n                ")
    # end if
    php_print(" </aside><!-- .widget-area -->\n\n")
# end if
