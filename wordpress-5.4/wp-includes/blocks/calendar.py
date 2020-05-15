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
#// Server-side rendering of the `core/calendar` block.
#// 
#// @package WordPress
#// 
#// 
#// Renders the `core/calendar` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the block content.
#//
def render_block_core_calendar(attributes=None, *args_):
    
    global monthnum,year
    php_check_if_defined("monthnum","year")
    previous_monthnum = monthnum
    previous_year = year
    if (php_isset(lambda : attributes["month"])) and (php_isset(lambda : attributes["year"])):
        permalink_structure = get_option("permalink_structure")
        if php_strpos(permalink_structure, "%monthnum%") != False and php_strpos(permalink_structure, "%year%") != False:
            #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
            monthnum = attributes["month"]
            #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
            year = attributes["year"]
        # end if
    # end if
    custom_class_name = "" if php_empty(lambda : attributes["className"]) else " " + attributes["className"]
    align_class_name = "" if php_empty(lambda : attributes["align"]) else " " + str("align") + str(attributes["align"])
    output = php_sprintf("<div class=\"%1$s\">%2$s</div>", esc_attr("wp-block-calendar" + custom_class_name + align_class_name), get_calendar(True, False))
    #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
    monthnum = previous_monthnum
    #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
    year = previous_year
    return output
# end def render_block_core_calendar
#// 
#// Registers the `core/calendar` block on server.
#//
def register_block_core_calendar(*args_):
    
    register_block_type("core/calendar", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"month": Array({"type": "integer"})}, {"year": Array({"type": "integer"})})}, {"render_callback": "render_block_core_calendar"}))
# end def register_block_core_calendar
add_action("init", "register_block_core_calendar")
