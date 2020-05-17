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
    def check_read_permission(self, post_=None):
        
        
        #// Ensure that the user is logged in and has the read_blocks capability.
        post_type_ = get_post_type_object(post_.post_type)
        if (not current_user_can(post_type_.cap.read_post, post_.ID)):
            return False
        # end if
        return super().check_read_permission(post_)
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
    def filter_response_by_context(self, data_=None, context_=None):
        
        
        data_ = super().filter_response_by_context(data_, context_)
        data_["title"]["rendered"] = None
        data_["content"]["rendered"] = None
        return data_
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
        schema_ = super().get_item_schema()
        #// 
        #// Allow all contexts to access `title.raw` and `content.raw`. Clients always
        #// need the raw markup of a reusable block to do anything useful, e.g. parse
        #// it or display it in an editor.
        #//
        schema_["properties"]["title"]["properties"]["raw"]["context"] = Array("view", "edit")
        schema_["properties"]["content"]["properties"]["raw"]["context"] = Array("view", "edit")
        schema_["properties"]["title"]["properties"]["rendered"] = None
        schema_["properties"]["content"]["properties"]["rendered"] = None
        return schema_
    # end def get_item_schema
# end class WP_REST_Blocks_Controller
