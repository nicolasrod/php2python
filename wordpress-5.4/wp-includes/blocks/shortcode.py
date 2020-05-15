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
#// Server-side rendering of the `core/shortcode` block.
#// 
#// @package WordPress
#// 
#// 
#// Performs wpautop() on the shortcode block content.
#// 
#// @param array  $attributes The block attributes.
#// @param string $content    The block content.
#// 
#// @return string Returns the block content.
#//
def render_block_core_shortcode(attributes=None, content=None, *args_):
    
    return wpautop(content)
# end def render_block_core_shortcode
#// 
#// Registers the `core/shortcode` block on server.
#//
def register_block_core_shortcode(*args_):
    
    path = __DIR__ + "/shortcode/block.json"
    metadata = php_json_decode(php_file_get_contents(path), True)
    register_block_type(metadata["name"], php_array_merge(metadata, Array({"render_callback": "render_block_core_shortcode"})))
# end def register_block_core_shortcode
add_action("init", "register_block_core_shortcode")
