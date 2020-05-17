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
#// Server-side rendering of the `core/block` block.
#// 
#// @package WordPress
#// 
#// 
#// Renders the `core/block` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Rendered HTML of the referenced block.
#//
def render_block_core_block(attributes_=None, *_args_):
    
    
    if php_empty(lambda : attributes_["ref"]):
        return ""
    # end if
    reusable_block_ = get_post(attributes_["ref"])
    if (not reusable_block_) or "wp_block" != reusable_block_.post_type:
        return ""
    # end if
    if "publish" != reusable_block_.post_status or (not php_empty(lambda : reusable_block_.post_password)):
        return ""
    # end if
    return do_blocks(reusable_block_.post_content)
# end def render_block_core_block
#// 
#// Registers the `core/block` block.
#//
def register_block_core_block(*_args_):
    
    
    register_block_type("core/block", Array({"attributes": Array({"ref": Array({"type": "number"})})}, {"render_callback": "render_block_core_block"}))
# end def register_block_core_block
add_action("init", "register_block_core_block")
