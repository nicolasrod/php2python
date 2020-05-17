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
#// REST API: WP_REST_Post_Types_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class to access post types via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Post_Types_Controller(WP_REST_Controller):
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #//
    def __init__(self):
        
        
        self.namespace = "wp/v2"
        self.rest_base = "types"
    # end def __init__
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        
        register_rest_route(self.namespace, "/" + self.rest_base, Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permissions_check"), "args": self.get_collection_params()}), {"schema": Array(self, "get_public_item_schema")}))
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<type>[\\w-]+)", Array({"args": Array({"type": Array({"description": __("An alphanumeric identifier for the post type."), "type": "string"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks whether a given request has permission to read types.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request_=None):
        
        
        if "edit" == request_["context"]:
            types_ = get_post_types(Array({"show_in_rest": True}), "objects")
            for type_ in types_:
                if current_user_can(type_.cap.edit_posts):
                    return True
                # end if
            # end for
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_view", __("Sorry, you are not allowed to edit posts in this post type."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Retrieves all public post types.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request_=None):
        
        
        data_ = Array()
        types_ = get_post_types(Array({"show_in_rest": True}), "objects")
        for type_ in types_:
            if "edit" == request_["context"] and (not current_user_can(type_.cap.edit_posts)):
                continue
            # end if
            post_type_ = self.prepare_item_for_response(type_, request_)
            data_[type_.name] = self.prepare_response_for_collection(post_type_)
        # end for
        return rest_ensure_response(data_)
    # end def get_items
    #// 
    #// Retrieves a specific post type.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request_=None):
        
        
        obj_ = get_post_type_object(request_["type"])
        if php_empty(lambda : obj_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_type_invalid", __("Invalid post type."), Array({"status": 404})))
        # end if
        if php_empty(lambda : obj_.show_in_rest):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_type", __("Cannot view post type."), Array({"status": rest_authorization_required_code()})))
        # end if
        if "edit" == request_["context"] and (not current_user_can(obj_.cap.edit_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit posts in this post type."), Array({"status": rest_authorization_required_code()})))
        # end if
        data_ = self.prepare_item_for_response(obj_, request_)
        return rest_ensure_response(data_)
    # end def get_item
    #// 
    #// Prepares a post type object for serialization.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post_Type    $post_type Post type object.
    #// @param WP_REST_Request $request   Full details about the request.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, post_type_=None, request_=None):
        
        
        taxonomies_ = wp_list_filter(get_object_taxonomies(post_type_.name, "objects"), Array({"show_in_rest": True}))
        taxonomies_ = wp_list_pluck(taxonomies_, "name")
        base_ = post_type_.rest_base if (not php_empty(lambda : post_type_.rest_base)) else post_type_.name
        supports_ = get_all_post_type_supports(post_type_.name)
        fields_ = self.get_fields_for_response(request_)
        data_ = Array()
        if php_in_array("capabilities", fields_, True):
            data_["capabilities"] = post_type_.cap
        # end if
        if php_in_array("description", fields_, True):
            data_["description"] = post_type_.description
        # end if
        if php_in_array("hierarchical", fields_, True):
            data_["hierarchical"] = post_type_.hierarchical
        # end if
        if php_in_array("viewable", fields_, True):
            data_["viewable"] = is_post_type_viewable(post_type_)
        # end if
        if php_in_array("labels", fields_, True):
            data_["labels"] = post_type_.labels
        # end if
        if php_in_array("name", fields_, True):
            data_["name"] = post_type_.label
        # end if
        if php_in_array("slug", fields_, True):
            data_["slug"] = post_type_.name
        # end if
        if php_in_array("supports", fields_, True):
            data_["supports"] = supports_
        # end if
        if php_in_array("taxonomies", fields_, True):
            data_["taxonomies"] = php_array_values(taxonomies_)
        # end if
        if php_in_array("rest_base", fields_, True):
            data_["rest_base"] = base_
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        #// Wrap the data in a response object.
        response_ = rest_ensure_response(data_)
        response_.add_links(Array({"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})}, {"https://api.w.org/items": Array({"href": rest_url(php_sprintf("wp/v2/%s", base_))})}))
        #// 
        #// Filters a post type returned from the API.
        #// 
        #// Allows modification of the post type data right before it is returned.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response  The response object.
        #// @param WP_Post_Type     $post_type The original post type object.
        #// @param WP_REST_Request  $request   Request used to generate the response.
        #//
        return apply_filters("rest_prepare_post_type", response_, post_type_, request_)
    # end def prepare_item_for_response
    #// 
    #// Retrieves the post type's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "type", "type": "object", "properties": Array({"capabilities": Array({"description": __("All capabilities used by the post type."), "type": "object", "context": Array("edit"), "readonly": True})}, {"description": Array({"description": __("A human-readable description of the post type."), "type": "string", "context": Array("view", "edit"), "readonly": True})}, {"hierarchical": Array({"description": __("Whether or not the post type should have children."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"viewable": Array({"description": __("Whether or not the post type can be viewed."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"labels": Array({"description": __("Human-readable labels for the post type for various contexts."), "type": "object", "context": Array("edit"), "readonly": True})}, {"name": Array({"description": __("The title for the post type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the post type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"supports": Array({"description": __("All features, supported by the post type."), "type": "object", "context": Array("edit"), "readonly": True})}, {"taxonomies": Array({"description": __("Taxonomies associated with post type."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("view", "edit"), "readonly": True})}, {"rest_base": Array({"description": __("REST base route for the post type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
        self.schema = schema_
        return self.add_additional_fields_schema(self.schema)
    # end def get_item_schema
    #// 
    #// Retrieves the query params for collections.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Collection parameters.
    #//
    def get_collection_params(self):
        
        
        return Array({"context": self.get_context_param(Array({"default": "view"}))})
    # end def get_collection_params
# end class WP_REST_Post_Types_Controller
