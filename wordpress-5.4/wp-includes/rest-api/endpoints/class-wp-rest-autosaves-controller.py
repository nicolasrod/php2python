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
#// REST API: WP_REST_Autosaves_Controller class.
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 5.0.0
#// 
#// 
#// Core class used to access autosaves via the REST API.
#// 
#// @since 5.0.0
#// 
#// @see WP_REST_Revisions_Controller
#// @see WP_REST_Controller
#//
class WP_REST_Autosaves_Controller(WP_REST_Revisions_Controller):
    parent_post_type = Array()
    parent_controller = Array()
    revisions_controller = Array()
    parent_base = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $parent_post_type Post type of the parent.
    #//
    def __init__(self, parent_post_type=None):
        
        self.parent_post_type = parent_post_type
        post_type_object = get_post_type_object(parent_post_type)
        parent_controller = post_type_object.get_rest_controller()
        if (not parent_controller):
            parent_controller = php_new_class("WP_REST_Posts_Controller", lambda : WP_REST_Posts_Controller(parent_post_type))
        # end if
        self.parent_controller = parent_controller
        self.revisions_controller = php_new_class("WP_REST_Revisions_Controller", lambda : WP_REST_Revisions_Controller(parent_post_type))
        self.rest_namespace = "wp/v2"
        self.rest_base = "autosaves"
        self.parent_base = post_type_object.rest_base if (not php_empty(lambda : post_type_object.rest_base)) else post_type_object.name
    # end def __init__
    #// 
    #// Registers the routes for autosaves.
    #// 
    #// @since 5.0.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        register_rest_route(self.rest_namespace, "/" + self.parent_base + "/(?P<id>[\\d]+)/" + self.rest_base, Array({"args": Array({"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permissions_check"), "args": self.get_collection_params()}), Array({"methods": WP_REST_Server.CREATABLE, "callback": Array(self, "create_item"), "permission_callback": Array(self, "create_item_permissions_check"), "args": self.parent_controller.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE)}), {"schema": Array(self, "get_public_item_schema")}))
        register_rest_route(self.rest_namespace, "/" + self.parent_base + "/(?P<parent>[\\d]+)/" + self.rest_base + "/(?P<id>[\\d]+)", Array({"args": Array({"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer"})}, {"id": Array({"description": __("The ID for the object."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self.revisions_controller, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Get the parent post.
    #// 
    #// @since 5.0.0
    #// 
    #// @param int $parent_id Supplied ID.
    #// @return WP_Post|WP_Error Post object if ID is valid, WP_Error otherwise.
    #//
    def get_parent(self, parent_id=None):
        
        return self.revisions_controller.get_parent(parent_id)
    # end def get_parent
    #// 
    #// Checks if a given request has access to get autosaves.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request=None):
        
        parent = self.get_parent(request["id"])
        if is_wp_error(parent):
            return parent
        # end if
        parent_post_type_obj = get_post_type_object(parent.post_type)
        if (not current_user_can(parent_post_type_obj.cap.edit_post, parent.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read", __("Sorry, you are not allowed to view autosaves of this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Checks if a given request has access to create an autosave revision.
    #// 
    #// Autosave revisions inherit permissions from the parent post,
    #// check if the current user has permission to edit the post.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create the item, WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request=None):
        
        id = request.get_param("id")
        if php_empty(lambda : id):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid item ID."), Array({"status": 404})))
        # end if
        return self.parent_controller.update_item_permissions_check(request)
    # end def create_item_permissions_check
    #// 
    #// Creates, updates or deletes an autosave revision.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def create_item(self, request=None):
        
        if (not php_defined("DOING_AUTOSAVE")):
            php_define("DOING_AUTOSAVE", True)
        # end if
        post = get_post(request["id"])
        if is_wp_error(post):
            return post
        # end if
        prepared_post = self.parent_controller.prepare_item_for_database(request)
        prepared_post.ID = post.ID
        user_id = get_current_user_id()
        if "draft" == post.post_status or "auto-draft" == post.post_status and post.post_author == user_id:
            #// Draft posts for the same author: autosaving updates the post and does not create a revision.
            #// Convert the post object to an array and add slashes, wp_update_post() expects escaped array.
            autosave_id = wp_update_post(wp_slash(prepared_post), True)
        else:
            #// Non-draft posts: create or update the post autosave.
            autosave_id = self.create_post_autosave(prepared_post)
        # end if
        if is_wp_error(autosave_id):
            return autosave_id
        # end if
        autosave = get_post(autosave_id)
        request.set_param("context", "edit")
        response = self.prepare_item_for_response(autosave, request)
        response = rest_ensure_response(response)
        return response
    # end def create_item
    #// 
    #// Get the autosave, if the ID is valid.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_Post|WP_Error Revision post object if ID is valid, WP_Error otherwise.
    #//
    def get_item(self, request=None):
        
        parent_id = int(request.get_param("parent"))
        if parent_id <= 0:
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post parent ID."), Array({"status": 404})))
        # end if
        autosave = wp_get_post_autosave(parent_id)
        if (not autosave):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_no_autosave", __("There is no autosave revision for this post."), Array({"status": 404})))
        # end if
        response = self.prepare_item_for_response(autosave, request)
        return response
    # end def get_item
    #// 
    #// Gets a collection of autosaves using wp_get_post_autosave.
    #// 
    #// Contains the user's autosave, for empty if it doesn't exist.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request=None):
        
        parent = self.get_parent(request["id"])
        if is_wp_error(parent):
            return parent
        # end if
        response = Array()
        parent_id = parent.ID
        revisions = wp_get_post_revisions(parent_id, Array({"check_enabled": False}))
        for revision in revisions:
            if False != php_strpos(revision.post_name, str(parent_id) + str("-autosave")):
                data = self.prepare_item_for_response(revision, request)
                response[-1] = self.prepare_response_for_collection(data)
            # end if
        # end for
        return rest_ensure_response(response)
    # end def get_items
    #// 
    #// Retrieves the autosave's schema, conforming to JSON Schema.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema = self.revisions_controller.get_item_schema()
        schema["properties"]["preview_link"] = Array({"description": __("Preview link for the post."), "type": "string", "format": "uri", "context": Array("edit"), "readonly": True})
        self.schema = schema
        return self.add_additional_fields_schema(self.schema)
    # end def get_item_schema
    #// 
    #// Creates autosave for the specified post.
    #// 
    #// From wp-admin/post.php.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array $post_data Associative array containing the post data.
    #// @return mixed The autosave revision ID or WP_Error.
    #//
    def create_post_autosave(self, post_data=None):
        
        post_id = int(post_data["ID"])
        post = get_post(post_id)
        if is_wp_error(post):
            return post
        # end if
        user_id = get_current_user_id()
        #// Store one autosave per author. If there is already an autosave, overwrite it.
        old_autosave = wp_get_post_autosave(post_id, user_id)
        if old_autosave:
            new_autosave = _wp_post_revision_data(post_data, True)
            new_autosave["ID"] = old_autosave.ID
            new_autosave["post_author"] = user_id
            #// If the new autosave has the same content as the post, delete the autosave.
            autosave_is_different = False
            for field in php_array_intersect(php_array_keys(new_autosave), php_array_keys(_wp_post_revision_fields(post))):
                if normalize_whitespace(new_autosave[field]) != normalize_whitespace(post.field):
                    autosave_is_different = True
                    break
                # end if
            # end for
            if (not autosave_is_different):
                wp_delete_post_revision(old_autosave.ID)
                return php_new_class("WP_Error", lambda : WP_Error("rest_autosave_no_changes", __("There is nothing to save. The autosave and the post content are the same."), Array({"status": 400})))
            # end if
            #// This filter is documented in wp-admin/post.php
            do_action("wp_creating_autosave", new_autosave)
            #// wp_update_post() expects escaped array.
            return wp_update_post(wp_slash(new_autosave))
        # end if
        #// Create the new autosave as a special post revision.
        return _wp_put_post_revision(post_data, True)
    # end def create_post_autosave
    #// 
    #// Prepares the revision for the REST response.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_Post         $post    Post revision object.
    #// @param WP_REST_Request $request Request object.
    #// 
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, post=None, request=None):
        
        response = self.revisions_controller.prepare_item_for_response(post, request)
        fields = self.get_fields_for_response(request)
        if php_in_array("preview_link", fields, True):
            parent_id = wp_is_post_autosave(post)
            preview_post_id = post.ID if False == parent_id else parent_id
            preview_query_args = Array()
            if False != parent_id:
                preview_query_args["preview_id"] = parent_id
                preview_query_args["preview_nonce"] = wp_create_nonce("post_preview_" + parent_id)
            # end if
            response.data["preview_link"] = get_preview_post_link(preview_post_id, preview_query_args)
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        response.data = self.add_additional_fields_to_object(response.data, request)
        response.data = self.filter_response_by_context(response.data, context)
        #// 
        #// Filters a revision returned from the API.
        #// 
        #// Allows modification of the revision right before it is returned.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_Post          $post     The original revision object.
        #// @param WP_REST_Request  $request  Request used to generate the response.
        #//
        return apply_filters("rest_prepare_autosave", response, post, request)
    # end def prepare_item_for_response
    #// 
    #// Retrieves the query params for the autosaves collection.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Collection parameters.
    #//
    def get_collection_params(self):
        
        return Array({"context": self.get_context_param(Array({"default": "view"}))})
    # end def get_collection_params
# end class WP_REST_Autosaves_Controller
