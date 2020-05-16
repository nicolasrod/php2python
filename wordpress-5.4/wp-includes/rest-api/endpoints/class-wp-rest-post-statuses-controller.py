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
#// REST API: WP_REST_Post_Statuses_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to access post statuses via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Post_Statuses_Controller(WP_REST_Controller):
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #//
    def __init__(self):
        
        self.namespace = "wp/v2"
        self.rest_base = "statuses"
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
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<status>[\\w-]+)", Array({"args": Array({"status": Array({"description": __("An alphanumeric identifier for the status."), "type": "string"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks whether a given request has permission to read post statuses.
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
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_view", __("Sorry, you are not allowed to manage post statuses."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Retrieves all post statuses, depending on user context.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request=None):
        
        data = Array()
        statuses = get_post_stati(Array({"internal": False}), "object")
        statuses["trash"] = get_post_status_object("trash")
        for slug,obj in statuses:
            ret = self.check_read_permission(obj)
            if (not ret):
                continue
            # end if
            status = self.prepare_item_for_response(obj, request)
            data[obj.name] = self.prepare_response_for_collection(status)
        # end for
        return rest_ensure_response(data)
    # end def get_items
    #// 
    #// Checks if a given request has access to read a post status.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request=None):
        
        status = get_post_status_object(request["status"])
        if php_empty(lambda : status):
            return php_new_class("WP_Error", lambda : WP_Error("rest_status_invalid", __("Invalid status."), Array({"status": 404})))
        # end if
        check = self.check_read_permission(status)
        if (not check):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_status", __("Cannot view status."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_item_permissions_check
    #// 
    #// Checks whether a given post status should be visible.
    #// 
    #// @since 4.7.0
    #// 
    #// @param object $status Post status.
    #// @return bool True if the post status is visible, otherwise false.
    #//
    def check_read_permission(self, status=None):
        
        if True == status.public:
            return True
        # end if
        if False == status.internal or "trash" == status.name:
            types = get_post_types(Array({"show_in_rest": True}), "objects")
            for type in types:
                if current_user_can(type.cap.edit_posts):
                    return True
                # end if
            # end for
        # end if
        return False
    # end def check_read_permission
    #// 
    #// Retrieves a specific post status.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request=None):
        
        obj = get_post_status_object(request["status"])
        if php_empty(lambda : obj):
            return php_new_class("WP_Error", lambda : WP_Error("rest_status_invalid", __("Invalid status."), Array({"status": 404})))
        # end if
        data = self.prepare_item_for_response(obj, request)
        return rest_ensure_response(data)
    # end def get_item
    #// 
    #// Prepares a post status object for serialization.
    #// 
    #// @since 4.7.0
    #// 
    #// @param stdClass        $status  Post status data.
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response Post status data.
    #//
    def prepare_item_for_response(self, status=None, request=None):
        
        fields = self.get_fields_for_response(request)
        data = Array()
        if php_in_array("name", fields, True):
            data["name"] = status.label
        # end if
        if php_in_array("private", fields, True):
            data["private"] = php_bool(status.private)
        # end if
        if php_in_array("protected", fields, True):
            data["protected"] = php_bool(status.protected)
        # end if
        if php_in_array("public", fields, True):
            data["public"] = php_bool(status.public)
        # end if
        if php_in_array("queryable", fields, True):
            data["queryable"] = php_bool(status.publicly_queryable)
        # end if
        if php_in_array("show_in_list", fields, True):
            data["show_in_list"] = php_bool(status.show_in_admin_all_list)
        # end if
        if php_in_array("slug", fields, True):
            data["slug"] = status.name
        # end if
        if php_in_array("date_floating", fields, True):
            data["date_floating"] = status.date_floating
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        response = rest_ensure_response(data)
        if "publish" == status.name:
            response.add_link("archives", rest_url("wp/v2/posts"))
        else:
            response.add_link("archives", add_query_arg("status", status.name, rest_url("wp/v2/posts")))
        # end if
        #// 
        #// Filters a status returned from the REST API.
        #// 
        #// Allows modification of the status data right before it is returned.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param object           $status   The original status object.
        #// @param WP_REST_Request  $request  Request used to generate the response.
        #//
        return apply_filters("rest_prepare_status", response, status, request)
    # end def prepare_item_for_response
    #// 
    #// Retrieves the post status' schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "status", "type": "object", "properties": Array({"name": Array({"description": __("The title for the status."), "type": "string", "context": Array("embed", "view", "edit"), "readonly": True})}, {"private": Array({"description": __("Whether posts with this status should be private."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"protected": Array({"description": __("Whether posts with this status should be protected."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"public": Array({"description": __("Whether posts of this status should be shown in the front end of the site."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"queryable": Array({"description": __("Whether posts with this status should be publicly-queryable."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"show_in_list": Array({"description": __("Whether to include posts in the edit listing for their post type."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the status."), "type": "string", "context": Array("embed", "view", "edit"), "readonly": True})}, {"date_floating": Array({"description": __("Whether posts of this status may have floating published dates."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})})})
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
# end class WP_REST_Post_Statuses_Controller
