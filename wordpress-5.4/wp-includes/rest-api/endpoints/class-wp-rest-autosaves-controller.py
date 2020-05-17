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
    #// 
    #// Parent post type.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    parent_post_type = Array()
    #// 
    #// Parent post controller.
    #// 
    #// @since 5.0.0
    #// @var WP_REST_Controller
    #//
    parent_controller = Array()
    #// 
    #// Revision controller.
    #// 
    #// @since 5.0.0
    #// @var WP_REST_Controller
    #//
    revisions_controller = Array()
    #// 
    #// The base of the parent controller's route.
    #// 
    #// @since 5.0.0
    #// @var string
    #//
    parent_base = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $parent_post_type Post type of the parent.
    #//
    def __init__(self, parent_post_type_=None):
        
        
        self.parent_post_type = parent_post_type_
        post_type_object_ = get_post_type_object(parent_post_type_)
        parent_controller_ = post_type_object_.get_rest_controller()
        if (not parent_controller_):
            parent_controller_ = php_new_class("WP_REST_Posts_Controller", lambda : WP_REST_Posts_Controller(parent_post_type_))
        # end if
        self.parent_controller = parent_controller_
        self.revisions_controller = php_new_class("WP_REST_Revisions_Controller", lambda : WP_REST_Revisions_Controller(parent_post_type_))
        self.rest_namespace = "wp/v2"
        self.rest_base = "autosaves"
        self.parent_base = post_type_object_.rest_base if (not php_empty(lambda : post_type_object_.rest_base)) else post_type_object_.name
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
    def get_parent(self, parent_id_=None):
        
        
        return self.revisions_controller.get_parent(parent_id_)
    # end def get_parent
    #// 
    #// Checks if a given request has access to get autosaves.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request_=None):
        
        
        parent_ = self.get_parent(request_["id"])
        if is_wp_error(parent_):
            return parent_
        # end if
        parent_post_type_obj_ = get_post_type_object(parent_.post_type)
        if (not current_user_can(parent_post_type_obj_.cap.edit_post, parent_.ID)):
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
    def create_item_permissions_check(self, request_=None):
        
        
        id_ = request_.get_param("id")
        if php_empty(lambda : id_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid item ID."), Array({"status": 404})))
        # end if
        return self.parent_controller.update_item_permissions_check(request_)
    # end def create_item_permissions_check
    #// 
    #// Creates, updates or deletes an autosave revision.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def create_item(self, request_=None):
        
        
        if (not php_defined("DOING_AUTOSAVE")):
            php_define("DOING_AUTOSAVE", True)
        # end if
        post_ = get_post(request_["id"])
        if is_wp_error(post_):
            return post_
        # end if
        prepared_post_ = self.parent_controller.prepare_item_for_database(request_)
        prepared_post_.ID = post_.ID
        user_id_ = get_current_user_id()
        if "draft" == post_.post_status or "auto-draft" == post_.post_status and post_.post_author == user_id_:
            #// Draft posts for the same author: autosaving updates the post and does not create a revision.
            #// Convert the post object to an array and add slashes, wp_update_post() expects escaped array.
            autosave_id_ = wp_update_post(wp_slash(prepared_post_), True)
        else:
            #// Non-draft posts: create or update the post autosave.
            autosave_id_ = self.create_post_autosave(prepared_post_)
        # end if
        if is_wp_error(autosave_id_):
            return autosave_id_
        # end if
        autosave_ = get_post(autosave_id_)
        request_.set_param("context", "edit")
        response_ = self.prepare_item_for_response(autosave_, request_)
        response_ = rest_ensure_response(response_)
        return response_
    # end def create_item
    #// 
    #// Get the autosave, if the ID is valid.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_Post|WP_Error Revision post object if ID is valid, WP_Error otherwise.
    #//
    def get_item(self, request_=None):
        
        
        parent_id_ = php_int(request_.get_param("parent"))
        if parent_id_ <= 0:
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post parent ID."), Array({"status": 404})))
        # end if
        autosave_ = wp_get_post_autosave(parent_id_)
        if (not autosave_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_no_autosave", __("There is no autosave revision for this post."), Array({"status": 404})))
        # end if
        response_ = self.prepare_item_for_response(autosave_, request_)
        return response_
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
    def get_items(self, request_=None):
        
        
        parent_ = self.get_parent(request_["id"])
        if is_wp_error(parent_):
            return parent_
        # end if
        response_ = Array()
        parent_id_ = parent_.ID
        revisions_ = wp_get_post_revisions(parent_id_, Array({"check_enabled": False}))
        for revision_ in revisions_:
            if False != php_strpos(revision_.post_name, str(parent_id_) + str("-autosave")):
                data_ = self.prepare_item_for_response(revision_, request_)
                response_[-1] = self.prepare_response_for_collection(data_)
            # end if
        # end for
        return rest_ensure_response(response_)
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
        schema_ = self.revisions_controller.get_item_schema()
        schema_["properties"]["preview_link"] = Array({"description": __("Preview link for the post."), "type": "string", "format": "uri", "context": Array("edit"), "readonly": True})
        self.schema = schema_
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
    def create_post_autosave(self, post_data_=None):
        
        
        post_id_ = php_int(post_data_["ID"])
        post_ = get_post(post_id_)
        if is_wp_error(post_):
            return post_
        # end if
        user_id_ = get_current_user_id()
        #// Store one autosave per author. If there is already an autosave, overwrite it.
        old_autosave_ = wp_get_post_autosave(post_id_, user_id_)
        if old_autosave_:
            new_autosave_ = _wp_post_revision_data(post_data_, True)
            new_autosave_["ID"] = old_autosave_.ID
            new_autosave_["post_author"] = user_id_
            #// If the new autosave has the same content as the post, delete the autosave.
            autosave_is_different_ = False
            for field_ in php_array_intersect(php_array_keys(new_autosave_), php_array_keys(_wp_post_revision_fields(post_))):
                if normalize_whitespace(new_autosave_[field_]) != normalize_whitespace(post_.field_):
                    autosave_is_different_ = True
                    break
                # end if
            # end for
            if (not autosave_is_different_):
                wp_delete_post_revision(old_autosave_.ID)
                return php_new_class("WP_Error", lambda : WP_Error("rest_autosave_no_changes", __("There is nothing to save. The autosave and the post content are the same."), Array({"status": 400})))
            # end if
            #// This filter is documented in wp-admin/post.php
            do_action("wp_creating_autosave", new_autosave_)
            #// wp_update_post() expects escaped array.
            return wp_update_post(wp_slash(new_autosave_))
        # end if
        #// Create the new autosave as a special post revision.
        return _wp_put_post_revision(post_data_, True)
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
    def prepare_item_for_response(self, post_=None, request_=None):
        
        
        response_ = self.revisions_controller.prepare_item_for_response(post_, request_)
        fields_ = self.get_fields_for_response(request_)
        if php_in_array("preview_link", fields_, True):
            parent_id_ = wp_is_post_autosave(post_)
            preview_post_id_ = post_.ID if False == parent_id_ else parent_id_
            preview_query_args_ = Array()
            if False != parent_id_:
                preview_query_args_["preview_id"] = parent_id_
                preview_query_args_["preview_nonce"] = wp_create_nonce("post_preview_" + parent_id_)
            # end if
            response_.data["preview_link"] = get_preview_post_link(preview_post_id_, preview_query_args_)
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        response_.data = self.add_additional_fields_to_object(response_.data, request_)
        response_.data = self.filter_response_by_context(response_.data, context_)
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
        return apply_filters("rest_prepare_autosave", response_, post_, request_)
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
