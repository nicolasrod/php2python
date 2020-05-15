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
    def get_items_permissions_check(self, request=None):
        
        if "edit" == request["context"]:
            types = get_post_types(Array({"show_in_rest": True}), "objects")
            for type in types:
                if current_user_can(type.cap.edit_posts):
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
    def get_items(self, request=None):
        
        data = Array()
        types = get_post_types(Array({"show_in_rest": True}), "objects")
        for type in types:
            if "edit" == request["context"] and (not current_user_can(type.cap.edit_posts)):
                continue
            # end if
            post_type = self.prepare_item_for_response(type, request)
            data[type.name] = self.prepare_response_for_collection(post_type)
        # end for
        return rest_ensure_response(data)
    # end def get_items
    #// 
    #// Retrieves a specific post type.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request=None):
        
        obj = get_post_type_object(request["type"])
        if php_empty(lambda : obj):
            return php_new_class("WP_Error", lambda : WP_Error("rest_type_invalid", __("Invalid post type."), Array({"status": 404})))
        # end if
        if php_empty(lambda : obj.show_in_rest):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_type", __("Cannot view post type."), Array({"status": rest_authorization_required_code()})))
        # end if
        if "edit" == request["context"] and (not current_user_can(obj.cap.edit_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit posts in this post type."), Array({"status": rest_authorization_required_code()})))
        # end if
        data = self.prepare_item_for_response(obj, request)
        return rest_ensure_response(data)
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
    def prepare_item_for_response(self, post_type=None, request=None):
        
        taxonomies = wp_list_filter(get_object_taxonomies(post_type.name, "objects"), Array({"show_in_rest": True}))
        taxonomies = wp_list_pluck(taxonomies, "name")
        base = post_type.rest_base if (not php_empty(lambda : post_type.rest_base)) else post_type.name
        supports = get_all_post_type_supports(post_type.name)
        fields = self.get_fields_for_response(request)
        data = Array()
        if php_in_array("capabilities", fields, True):
            data["capabilities"] = post_type.cap
        # end if
        if php_in_array("description", fields, True):
            data["description"] = post_type.description
        # end if
        if php_in_array("hierarchical", fields, True):
            data["hierarchical"] = post_type.hierarchical
        # end if
        if php_in_array("viewable", fields, True):
            data["viewable"] = is_post_type_viewable(post_type)
        # end if
        if php_in_array("labels", fields, True):
            data["labels"] = post_type.labels
        # end if
        if php_in_array("name", fields, True):
            data["name"] = post_type.label
        # end if
        if php_in_array("slug", fields, True):
            data["slug"] = post_type.name
        # end if
        if php_in_array("supports", fields, True):
            data["supports"] = supports
        # end if
        if php_in_array("taxonomies", fields, True):
            data["taxonomies"] = php_array_values(taxonomies)
        # end if
        if php_in_array("rest_base", fields, True):
            data["rest_base"] = base
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        #// Wrap the data in a response object.
        response = rest_ensure_response(data)
        response.add_links(Array({"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})}, {"https://api.w.org/items": Array({"href": rest_url(php_sprintf("wp/v2/%s", base))})}))
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
        return apply_filters("rest_prepare_post_type", response, post_type, request)
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
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "type", "type": "object", "properties": Array({"capabilities": Array({"description": __("All capabilities used by the post type."), "type": "object", "context": Array("edit"), "readonly": True})}, {"description": Array({"description": __("A human-readable description of the post type."), "type": "string", "context": Array("view", "edit"), "readonly": True})}, {"hierarchical": Array({"description": __("Whether or not the post type should have children."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"viewable": Array({"description": __("Whether or not the post type can be viewed."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"labels": Array({"description": __("Human-readable labels for the post type for various contexts."), "type": "object", "context": Array("edit"), "readonly": True})}, {"name": Array({"description": __("The title for the post type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the post type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"supports": Array({"description": __("All features, supported by the post type."), "type": "object", "context": Array("edit"), "readonly": True})}, {"taxonomies": Array({"description": __("Taxonomies associated with post type."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("view", "edit"), "readonly": True})}, {"rest_base": Array({"description": __("REST base route for the post type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
        self.schema = schema
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
