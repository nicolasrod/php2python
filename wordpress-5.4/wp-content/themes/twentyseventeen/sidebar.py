#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// The sidebar containing the main widget area
#// 
#// @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// @version 1.0
#//
if (not is_active_sidebar("sidebar-1")):
    sys.exit(-1)
# end if
php_print("\n<aside id=\"secondary\" class=\"widget-area\" role=\"complementary\" aria-label=\"")
esc_attr_e("Blog Sidebar", "twentyseventeen")
php_print("\">\n    ")
dynamic_sidebar("sidebar-1")
php_print("</aside><!-- #secondary -->\n")
