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
    def get_items_permissions_check(self, request_=None):
        
        
        if "edit" == request_["context"]:
            types_ = get_post_types(Array({"show_in_rest": True}), "objects")
            for type_ in types_:
                if current_user_can(type_.cap.edit_posts):
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
    def get_items(self, request_=None):
        
        
        data_ = Array()
        statuses_ = get_post_stati(Array({"internal": False}), "object")
        statuses_["trash"] = get_post_status_object("trash")
        for slug_,obj_ in statuses_.items():
            ret_ = self.check_read_permission(obj_)
            if (not ret_):
                continue
            # end if
            status_ = self.prepare_item_for_response(obj_, request_)
            data_[obj_.name] = self.prepare_response_for_collection(status_)
        # end for
        return rest_ensure_response(data_)
    # end def get_items
    #// 
    #// Checks if a given request has access to read a post status.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        status_ = get_post_status_object(request_["status"])
        if php_empty(lambda : status_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_status_invalid", __("Invalid status."), Array({"status": 404})))
        # end if
        check_ = self.check_read_permission(status_)
        if (not check_):
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
    def check_read_permission(self, status_=None):
        
        
        if True == status_.public:
            return True
        # end if
        if False == status_.internal or "trash" == status_.name:
            types_ = get_post_types(Array({"show_in_rest": True}), "objects")
            for type_ in types_:
                if current_user_can(type_.cap.edit_posts):
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
    def get_item(self, request_=None):
        
        
        obj_ = get_post_status_object(request_["status"])
        if php_empty(lambda : obj_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_status_invalid", __("Invalid status."), Array({"status": 404})))
        # end if
        data_ = self.prepare_item_for_response(obj_, request_)
        return rest_ensure_response(data_)
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
    def prepare_item_for_response(self, status_=None, request_=None):
        
        
        fields_ = self.get_fields_for_response(request_)
        data_ = Array()
        if php_in_array("name", fields_, True):
            data_["name"] = status_.label
        # end if
        if php_in_array("private", fields_, True):
            data_["private"] = php_bool(status_.private)
        # end if
        if php_in_array("protected", fields_, True):
            data_["protected"] = php_bool(status_.protected)
        # end if
        if php_in_array("public", fields_, True):
            data_["public"] = php_bool(status_.public)
        # end if
        if php_in_array("queryable", fields_, True):
            data_["queryable"] = php_bool(status_.publicly_queryable)
        # end if
        if php_in_array("show_in_list", fields_, True):
            data_["show_in_list"] = php_bool(status_.show_in_admin_all_list)
        # end if
        if php_in_array("slug", fields_, True):
            data_["slug"] = status_.name
        # end if
        if php_in_array("date_floating", fields_, True):
            data_["date_floating"] = status_.date_floating
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        response_ = rest_ensure_response(data_)
        if "publish" == status_.name:
            response_.add_link("archives", rest_url("wp/v2/posts"))
        else:
            response_.add_link("archives", add_query_arg("status", status_.name, rest_url("wp/v2/posts")))
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
        return apply_filters("rest_prepare_status", response_, status_, request_)
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
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "status", "type": "object", "properties": Array({"name": Array({"description": __("The title for the status."), "type": "string", "context": Array("embed", "view", "edit"), "readonly": True})}, {"private": Array({"description": __("Whether posts with this status should be private."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"protected": Array({"description": __("Whether posts with this status should be protected."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"public": Array({"description": __("Whether posts of this status should be shown in the front end of the site."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"queryable": Array({"description": __("Whether posts with this status should be publicly-queryable."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"show_in_list": Array({"description": __("Whether to include posts in the edit listing for their post type."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the status."), "type": "string", "context": Array("embed", "view", "edit"), "readonly": True})}, {"date_floating": Array({"description": __("Whether posts of this status may have floating published dates."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})})})
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
# end class WP_REST_Post_Statuses_Controller
