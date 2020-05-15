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
#// Twenty Twenty SVG Icon helper functions
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if (not php_function_exists("twentytwenty_the_theme_svg")):
    #// 
    #// Output and Get Theme SVG.
    #// Output and get the SVG markup for an icon in the TwentyTwenty_SVG_Icons class.
    #// 
    #// @param string $svg_name The name of the icon.
    #// @param string $group The group the icon belongs to.
    #// @param string $color Color code.
    #//
    def twentytwenty_the_theme_svg(svg_name=None, group="ui", color="", *args_):
        
        php_print(twentytwenty_get_theme_svg(svg_name, group, color))
        pass
    # end def twentytwenty_the_theme_svg
# end if
if (not php_function_exists("twentytwenty_get_theme_svg")):
    #// 
    #// Get information about the SVG icon.
    #// 
    #// @param string $svg_name The name of the icon.
    #// @param string $group The group the icon belongs to.
    #// @param string $color Color code.
    #//
    def twentytwenty_get_theme_svg(svg_name=None, group="ui", color="", *args_):
        
        #// Make sure that only our allowed tags and attributes are included.
        svg = wp_kses(TwentyTwenty_SVG_Icons.get_svg(svg_name, group, color), Array({"svg": Array({"class": True, "xmlns": True, "width": True, "height": True, "viewbox": True, "aria-hidden": True, "role": True, "focusable": True})}, {"path": Array({"fill": True, "fill-rule": True, "d": True, "transform": True})}, {"polygon": Array({"fill": True, "fill-rule": True, "points": True, "transform": True, "focusable": True})}))
        if (not svg):
            return False
        # end if
        return svg
    # end def twentytwenty_get_theme_svg
# end if
