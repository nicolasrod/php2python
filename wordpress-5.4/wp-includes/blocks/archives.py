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
def render_block_core_archives(attributes_=None, *_args_):
    
    
    show_post_count_ = (not php_empty(lambda : attributes_["showPostCounts"]))
    class_ = "wp-block-archives"
    if (php_isset(lambda : attributes_["align"])):
        class_ += str(" align") + str(attributes_["align"])
    # end if
    if (php_isset(lambda : attributes_["className"])):
        class_ += str(" ") + str(attributes_["className"])
    # end if
    if (not php_empty(lambda : attributes_["displayAsDropdown"])):
        class_ += " wp-block-archives-dropdown"
        dropdown_id_ = esc_attr(php_uniqid("wp-block-archives-"))
        title_ = __("Archives")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-archives.php
        dropdown_args_ = apply_filters("widget_archives_dropdown_args", Array({"type": "monthly", "format": "option", "show_post_count": show_post_count_}))
        dropdown_args_["echo"] = 0
        archives_ = wp_get_archives(dropdown_args_)
        for case in Switch(dropdown_args_["type"]):
            if case("yearly"):
                label_ = __("Select Year")
                break
            # end if
            if case("monthly"):
                label_ = __("Select Month")
                break
            # end if
            if case("daily"):
                label_ = __("Select Day")
                break
            # end if
            if case("weekly"):
                label_ = __("Select Week")
                break
            # end if
            if case():
                label_ = __("Select Post")
                break
            # end if
        # end for
        label_ = esc_attr(label_)
        block_content_ = "<label class=\"screen-reader-text\" for=\"" + dropdown_id_ + "\">" + title_ + "</label>\n <select id=\"" + dropdown_id_ + "\" name=\"archive-dropdown\" onchange=\"document.location.href=this.options[this.selectedIndex].value;\">\n    <option value=\"\">" + label_ + "</option>" + archives_ + "</select>"
        return php_sprintf("<div class=\"%1$s\">%2$s</div>", esc_attr(class_), block_content_)
    # end if
    class_ += " wp-block-archives-list"
    #// This filter is documented in wp-includes/widgets/class-wp-widget-archives.php
    archives_args_ = apply_filters("widget_archives_args", Array({"type": "monthly", "show_post_count": show_post_count_}))
    archives_args_["echo"] = 0
    archives_ = wp_get_archives(archives_args_)
    classnames_ = esc_attr(class_)
    if php_empty(lambda : archives_):
        return php_sprintf("<div class=\"%1$s\">%2$s</div>", classnames_, __("No archives to show."))
    # end if
    return php_sprintf("<ul class=\"%1$s\">%2$s</ul>", classnames_, archives_)
# end def render_block_core_archives
#// 
#// Register archives block.
#//
def register_block_core_archives(*_args_):
    
    
    register_block_type("core/archives", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"displayAsDropdown": Array({"type": "boolean", "default": False})}, {"showPostCounts": Array({"type": "boolean", "default": False})})}, {"render_callback": "render_block_core_archives"}))
# end def register_block_core_archives
add_action("init", "register_block_core_archives")
