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
#// Server-side rendering of the `core/tag-cloud` block.
#// 
#// @package WordPress
#// 
#// 
#// Renders the `core/tag-cloud` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the tag cloud for selected taxonomy.
#//
def render_block_core_tag_cloud(attributes=None, *args_):
    
    class_ = str("wp-block-tag-cloud align") + str(attributes["align"]) if (php_isset(lambda : attributes["align"])) else "wp-block-tag-cloud"
    if (php_isset(lambda : attributes["className"])):
        class_ += " " + attributes["className"]
    # end if
    args = Array({"echo": False, "taxonomy": attributes["taxonomy"], "show_count": attributes["showTagCounts"]})
    tag_cloud = wp_tag_cloud(args)
    if (not tag_cloud):
        labels = get_taxonomy_labels(get_taxonomy(attributes["taxonomy"]))
        tag_cloud = esc_html(php_sprintf(__("Your site doesn&#8217;t have any %s, so there&#8217;s nothing to display here at the moment."), php_strtolower(labels.name)))
    # end if
    return php_sprintf("<p class=\"%1$s\">%2$s</p>", esc_attr(class_), tag_cloud)
# end def render_block_core_tag_cloud
#// 
#// Registers the `core/tag-cloud` block on server.
#//
def register_block_core_tag_cloud(*args_):
    
    register_block_type("core/tag-cloud", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"taxonomy": Array({"type": "string", "default": "post_tag"})}, {"showTagCounts": Array({"type": "boolean", "default": False})})}, {"render_callback": "render_block_core_tag_cloud"}))
# end def register_block_core_tag_cloud
add_action("init", "register_block_core_tag_cloud")
