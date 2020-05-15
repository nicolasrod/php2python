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
#// Reusable blocks REST API: WP_REST_Blocks_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 5.0.0
#// 
#// 
#// Controller which provides a REST endpoint for the editor to read, create,
#// edit and delete reusable blocks. Blocks are stored as posts with the wp_block
#// post type.
#// 
#// @since 5.0.0
#// 
#// @see WP_REST_Posts_Controller
#// @see WP_REST_Controller
#//
class WP_REST_Blocks_Controller(WP_REST_Posts_Controller):
    #// 
    #// Checks if a block can be read.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_Post $post Post object that backs the block.
    #// @return bool Whether the block can be read.
    #//
    def check_read_permission(self, post=None):
        
        #// Ensure that the user is logged in and has the read_blocks capability.
        post_type = get_post_type_object(post.post_type)
        if (not current_user_can(post_type.cap.read_post, post.ID)):
            return False
        # end if
        return super().check_read_permission(post)
    # end def check_read_permission
    #// 
    #// Filters a response based on the context defined in the schema.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array  $data    Response data to fiter.
    #// @param string $context Context defined in the schema.
    #// @return array Filtered response.
    #//
    def filter_response_by_context(self, data=None, context=None):
        
        data = super().filter_response_by_context(data, context)
        data["title"]["rendered"] = None
        data["content"]["rendered"] = None
        return data
    # end def filter_response_by_context
    #// 
    #// Retrieves the block's schema, conforming to JSON Schema.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        #// Do not cache this schema because all properties are derived from parent controller.
        schema = super().get_item_schema()
        #// 
        #// Allow all contexts to access `title.raw` and `content.raw`. Clients always
        #// need the raw markup of a reusable block to do anything useful, e.g. parse
        #// it or display it in an editor.
        #//
        schema["properties"]["title"]["properties"]["raw"]["context"] = Array("view", "edit")
        schema["properties"]["content"]["properties"]["raw"]["context"] = Array("view", "edit")
        schema["properties"]["title"]["properties"]["rendered"] = None
        schema["properties"]["content"]["properties"]["rendered"] = None
        return schema
    # end def get_item_schema
# end class WP_REST_Blocks_Controller
