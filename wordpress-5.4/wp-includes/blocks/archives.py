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
#// Server-side rendering of the `core/archives` block.
#// 
#// @package WordPress
#// 
#// 
#// Renders the `core/archives` block on server.
#// 
#// @see WP_Widget_Archives
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the post content with archives added.
#//
def render_block_core_archives(attributes=None, *args_):
    
    show_post_count = (not php_empty(lambda : attributes["showPostCounts"]))
    class_ = "wp-block-archives"
    if (php_isset(lambda : attributes["align"])):
        class_ += str(" align") + str(attributes["align"])
    # end if
    if (php_isset(lambda : attributes["className"])):
        class_ += str(" ") + str(attributes["className"])
    # end if
    if (not php_empty(lambda : attributes["displayAsDropdown"])):
        class_ += " wp-block-archives-dropdown"
        dropdown_id = esc_attr(uniqid("wp-block-archives-"))
        title = __("Archives")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-archives.php
        dropdown_args = apply_filters("widget_archives_dropdown_args", Array({"type": "monthly", "format": "option", "show_post_count": show_post_count}))
        dropdown_args["echo"] = 0
        archives = wp_get_archives(dropdown_args)
        for case in Switch(dropdown_args["type"]):
            if case("yearly"):
                label = __("Select Year")
                break
            # end if
            if case("monthly"):
                label = __("Select Month")
                break
            # end if
            if case("daily"):
                label = __("Select Day")
                break
            # end if
            if case("weekly"):
                label = __("Select Week")
                break
            # end if
            if case():
                label = __("Select Post")
                break
            # end if
        # end for
        label = esc_attr(label)
        block_content = "<label class=\"screen-reader-text\" for=\"" + dropdown_id + "\">" + title + "</label>\n    <select id=\"" + dropdown_id + "\" name=\"archive-dropdown\" onchange=\"document.location.href=this.options[this.selectedIndex].value;\">\n <option value=\"\">" + label + "</option>" + archives + "</select>"
        return php_sprintf("<div class=\"%1$s\">%2$s</div>", esc_attr(class_), block_content)
    # end if
    class_ += " wp-block-archives-list"
    #// This filter is documented in wp-includes/widgets/class-wp-widget-archives.php
    archives_args = apply_filters("widget_archives_args", Array({"type": "monthly", "show_post_count": show_post_count}))
    archives_args["echo"] = 0
    archives = wp_get_archives(archives_args)
    classnames = esc_attr(class_)
    if php_empty(lambda : archives):
        return php_sprintf("<div class=\"%1$s\">%2$s</div>", classnames, __("No archives to show."))
    # end if
    return php_sprintf("<ul class=\"%1$s\">%2$s</ul>", classnames, archives)
# end def render_block_core_archives
#// 
#// Register archives block.
#//
def register_block_core_archives(*args_):
    
    register_block_type("core/archives", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"displayAsDropdown": Array({"type": "boolean", "default": False})}, {"showPostCounts": Array({"type": "boolean", "default": False})})}, {"render_callback": "render_block_core_archives"}))
# end def register_block_core_archives
add_action("init", "register_block_core_archives")
