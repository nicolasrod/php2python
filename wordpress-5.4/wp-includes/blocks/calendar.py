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
def render_block_core_calendar(attributes_=None, *_args_):
    
    
    global monthnum_
    global year_
    php_check_if_defined("monthnum_","year_")
    previous_monthnum_ = monthnum_
    previous_year_ = year_
    if (php_isset(lambda : attributes_["month"])) and (php_isset(lambda : attributes_["year"])):
        permalink_structure_ = get_option("permalink_structure")
        if php_strpos(permalink_structure_, "%monthnum%") != False and php_strpos(permalink_structure_, "%year%") != False:
            #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
            monthnum_ = attributes_["month"]
            #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
            year_ = attributes_["year"]
        # end if
    # end if
    custom_class_name_ = "" if php_empty(lambda : attributes_["className"]) else " " + attributes_["className"]
    align_class_name_ = "" if php_empty(lambda : attributes_["align"]) else " " + str("align") + str(attributes_["align"])
    output_ = php_sprintf("<div class=\"%1$s\">%2$s</div>", esc_attr("wp-block-calendar" + custom_class_name_ + align_class_name_), get_calendar(True, False))
    #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
    monthnum_ = previous_monthnum_
    #// phpcs:ignore WordPress.WP.GlobalVariablesOverride.OverrideProhibited
    year_ = previous_year_
    return output_
# end def render_block_core_calendar
#// 
#// Registers the `core/calendar` block on server.
#//
def register_block_core_calendar(*_args_):
    
    
    register_block_type("core/calendar", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"month": Array({"type": "integer"})}, {"year": Array({"type": "integer"})})}, {"render_callback": "render_block_core_calendar"}))
# end def register_block_core_calendar
add_action("init", "register_block_core_calendar")
