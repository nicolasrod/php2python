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
#// Block Renderer REST API: WP_REST_Block_Renderer_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 5.0.0
#// 
#// 
#// Controller which provides REST endpoint for rendering a block.
#// 
#// @since 5.0.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Block_Renderer_Controller(WP_REST_Controller):
    #// 
    #// Constructs the controller.
    #// 
    #// @since 5.0.0
    #//
    def __init__(self):
        
        
        self.namespace = "wp/v2"
        self.rest_base = "block-renderer"
    # end def __init__
    #// 
    #// Registers the necessary REST API routes, one for each dynamic block.
    #// 
    #// @since 5.0.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        
        block_types_ = WP_Block_Type_Registry.get_instance().get_all_registered()
        for block_type_ in block_types_:
            if (not block_type_.is_dynamic()):
                continue
            # end if
            register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<name>" + block_type_.name + ")", Array({"args": Array({"name": Array({"description": __("Unique registered name for the block."), "type": "string"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))}, {"attributes": Array({"description": php_sprintf(__("Attributes for %s block"), block_type_.name), "type": "object", "additionalProperties": False, "properties": block_type_.get_attributes(), "default": Array()})}, {"post_id": Array({"description": __("ID of the post context."), "type": "integer"})})}), {"schema": Array(self, "get_public_item_schema")}))
        # end for
    # end def register_routes
    #// 
    #// Checks if a given request has access to read blocks.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        global post_
        php_check_if_defined("post_")
        post_id_ = php_intval(request_["post_id"]) if (php_isset(lambda : request_["post_id"])) else 0
        if 0 < post_id_:
            post_ = get_post(post_id_)
            if (not post_) or (not current_user_can("edit_post", post_.ID)):
                return php_new_class("WP_Error", lambda : WP_Error("block_cannot_read", __("Sorry, you are not allowed to read blocks of this post."), Array({"status": rest_authorization_required_code()})))
            # end if
        else:
            if (not current_user_can("edit_posts")):
                return php_new_class("WP_Error", lambda : WP_Error("block_cannot_read", __("Sorry, you are not allowed to read blocks as this user."), Array({"status": rest_authorization_required_code()})))
            # end if
        # end if
        return True
    # end def get_item_permissions_check
    #// 
    #// Returns block output from block's registered render_callback.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request_=None):
        
        
        global post_
        php_check_if_defined("post_")
        post_id_ = php_intval(request_["post_id"]) if (php_isset(lambda : request_["post_id"])) else 0
        if 0 < post_id_:
            post_ = get_post(post_id_)
            #// Set up postdata since this will be needed if post_id was set.
            setup_postdata(post_)
        # end if
        registry_ = WP_Block_Type_Registry.get_instance()
        if None == registry_.get_registered(request_["name"]):
            return php_new_class("WP_Error", lambda : WP_Error("block_invalid", __("Invalid block."), Array({"status": 404})))
        # end if
        attributes_ = request_.get_param("attributes")
        #// Create an array representation simulating the output of parse_blocks.
        block_ = Array({"blockName": request_["name"], "attrs": attributes_, "innerHTML": "", "innerContent": Array()})
        #// Render using render_block to ensure all relevant filters are used.
        data_ = Array({"rendered": render_block(block_)})
        return rest_ensure_response(data_)
    # end def get_item
    #// 
    #// Retrieves block's output schema, conforming to JSON Schema.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        
        if self.schema:
            return self.schema
        # end if
        self.schema = Array({"$schema": "http://json-schema.org/schema#", "title": "rendered-block", "type": "object", "properties": Array({"rendered": Array({"description": __("The rendered block."), "type": "string", "required": True, "context": Array("edit")})})})
        return self.schema
    # end def get_item_schema
# end class WP_REST_Block_Renderer_Controller
