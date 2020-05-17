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
#// REST API: WP_REST_Users_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to manage users via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Users_Controller(WP_REST_Controller):
    #// 
    #// Instance of a user meta fields object.
    #// 
    #// @since 4.7.0
    #// @var WP_REST_User_Meta_Fields
    #//
    meta = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #//
    def __init__(self):
        
        
        self.namespace = "wp/v2"
        self.rest_base = "users"
        self.meta = php_new_class("WP_REST_User_Meta_Fields", lambda : WP_REST_User_Meta_Fields())
    # end def __init__
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        
        register_rest_route(self.namespace, "/" + self.rest_base, Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permissions_check"), "args": self.get_collection_params()}), Array({"methods": WP_REST_Server.CREATABLE, "callback": Array(self, "create_item"), "permission_callback": Array(self, "create_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.CREATABLE)}), {"schema": Array(self, "get_public_item_schema")}))
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<id>[\\d]+)", Array({"args": Array({"id": Array({"description": __("Unique identifier for the user."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), Array({"methods": WP_REST_Server.EDITABLE, "callback": Array(self, "update_item"), "permission_callback": Array(self, "update_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE)}), Array({"methods": WP_REST_Server.DELETABLE, "callback": Array(self, "delete_item"), "permission_callback": Array(self, "delete_item_permissions_check"), "args": Array({"force": Array({"type": "boolean", "default": False, "description": __("Required to be true, as users do not support trashing.")})}, {"reassign": Array({"type": "integer", "description": __("Reassign the deleted user's posts and links to this user ID."), "required": True, "sanitize_callback": Array(self, "check_reassign")})})}), {"schema": Array(self, "get_public_item_schema")}))
        register_rest_route(self.namespace, "/" + self.rest_base + "/me", Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_current_item"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), Array({"methods": WP_REST_Server.EDITABLE, "callback": Array(self, "update_current_item"), "permission_callback": Array(self, "update_current_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE)}), Array({"methods": WP_REST_Server.DELETABLE, "callback": Array(self, "delete_current_item"), "permission_callback": Array(self, "delete_current_item_permissions_check"), "args": Array({"force": Array({"type": "boolean", "default": False, "description": __("Required to be true, as users do not support trashing.")})}, {"reassign": Array({"type": "integer", "description": __("Reassign the deleted user's posts and links to this user ID."), "required": True, "sanitize_callback": Array(self, "check_reassign")})})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks for a valid value for the reassign parameter when deleting users.
    #// 
    #// The value can be an integer, 'false', false, or ''.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int|bool        $value   The value passed to the reassign parameter.
    #// @param WP_REST_Request $request Full details about the request.
    #// @param string          $param   The parameter that is being sanitized.
    #// 
    #// @return int|bool|WP_Error
    #//
    def check_reassign(self, value_=None, request_=None, param_=None):
        
        
        if php_is_numeric(value_):
            return value_
        # end if
        if php_empty(lambda : value_) or False == value_ or "false" == value_:
            return False
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", __("Invalid user parameter(s)."), Array({"status": 400})))
    # end def check_reassign
    #// 
    #// Permissions check for getting all users.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, otherwise WP_Error object.
    #//
    def get_items_permissions_check(self, request_=None):
        
        
        #// Check if roles is specified in GET request and if user can list users.
        if (not php_empty(lambda : request_["roles"])) and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_view", __("Sorry, you are not allowed to filter users by role."), Array({"status": rest_authorization_required_code()})))
        # end if
        if "edit" == request_["context"] and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to list users."), Array({"status": rest_authorization_required_code()})))
        # end if
        if php_in_array(request_["orderby"], Array("email", "registered_date"), True) and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_orderby", __("Sorry, you are not allowed to order users by this parameter."), Array({"status": rest_authorization_required_code()})))
        # end if
        if "authors" == request_["who"]:
            types_ = get_post_types(Array({"show_in_rest": True}), "objects")
            for type_ in types_:
                if post_type_supports(type_.name, "author") and current_user_can(type_.cap.edit_posts):
                    return True
                # end if
            # end for
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_who", __("Sorry, you are not allowed to query users by this parameter."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Retrieves all users.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request_=None):
        
        
        #// Retrieve the list of registered collection query parameters.
        registered_ = self.get_collection_params()
        #// 
        #// This array defines mappings between public API query parameters whose
        #// values are accepted as-passed, and their internal WP_Query parameter
        #// name equivalents (some are the same). Only values which are also
        #// present in $registered will be set.
        #//
        parameter_mappings_ = Array({"exclude": "exclude", "include": "include", "order": "order", "per_page": "number", "search": "search", "roles": "role__in", "slug": "nicename__in"})
        prepared_args_ = Array()
        #// 
        #// For each known parameter which is both registered and present in the request,
        #// set the parameter's value on the query $prepared_args.
        #//
        for api_param_,wp_param_ in parameter_mappings_:
            if (php_isset(lambda : registered_[api_param_]) and php_isset(lambda : request_[api_param_])):
                prepared_args_[wp_param_] = request_[api_param_]
            # end if
        # end for
        if (php_isset(lambda : registered_["offset"])) and (not php_empty(lambda : request_["offset"])):
            prepared_args_["offset"] = request_["offset"]
        else:
            prepared_args_["offset"] = request_["page"] - 1 * prepared_args_["number"]
        # end if
        if (php_isset(lambda : registered_["orderby"])):
            orderby_possibles_ = Array({"id": "ID", "include": "include", "name": "display_name", "registered_date": "registered", "slug": "user_nicename", "include_slugs": "nicename__in", "email": "user_email", "url": "user_url"})
            prepared_args_["orderby"] = orderby_possibles_[request_["orderby"]]
        # end if
        if (php_isset(lambda : registered_["who"])) and (not php_empty(lambda : request_["who"])) and "authors" == request_["who"]:
            prepared_args_["who"] = "authors"
        elif (not current_user_can("list_users")):
            prepared_args_["has_published_posts"] = get_post_types(Array({"show_in_rest": True}), "names")
        # end if
        if (not php_empty(lambda : prepared_args_["search"])):
            prepared_args_["search"] = "*" + prepared_args_["search"] + "*"
        # end if
        #// 
        #// Filters WP_User_Query arguments when querying users via the REST API.
        #// 
        #// @link https://developer.wordpress.org/reference/classes/wp_user_query
        #// 
        #// @since 4.7.0
        #// 
        #// @param array           $prepared_args Array of arguments for WP_User_Query.
        #// @param WP_REST_Request $request       The current request.
        #//
        prepared_args_ = apply_filters("rest_user_query", prepared_args_, request_)
        query_ = php_new_class("WP_User_Query", lambda : WP_User_Query(prepared_args_))
        users_ = Array()
        for user_ in query_.results:
            data_ = self.prepare_item_for_response(user_, request_)
            users_[-1] = self.prepare_response_for_collection(data_)
        # end for
        response_ = rest_ensure_response(users_)
        #// Store pagination values for headers then unset for count query.
        per_page_ = php_int(prepared_args_["number"])
        page_ = ceil(php_int(prepared_args_["offset"]) / per_page_ + 1)
        prepared_args_["fields"] = "ID"
        total_users_ = query_.get_total()
        if total_users_ < 1:
            prepared_args_["number"] = None
            prepared_args_["offset"] = None
            count_query_ = php_new_class("WP_User_Query", lambda : WP_User_Query(prepared_args_))
            total_users_ = count_query_.get_total()
        # end if
        response_.header("X-WP-Total", php_int(total_users_))
        max_pages_ = ceil(total_users_ / per_page_)
        response_.header("X-WP-TotalPages", php_int(max_pages_))
        base_ = add_query_arg(urlencode_deep(request_.get_query_params()), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
        if page_ > 1:
            prev_page_ = page_ - 1
            if prev_page_ > max_pages_:
                prev_page_ = max_pages_
            # end if
            prev_link_ = add_query_arg("page", prev_page_, base_)
            response_.link_header("prev", prev_link_)
        # end if
        if max_pages_ > page_:
            next_page_ = page_ + 1
            next_link_ = add_query_arg("page", next_page_, base_)
            response_.link_header("next", next_link_)
        # end if
        return response_
    # end def get_items
    #// 
    #// Get the user, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_User|WP_Error True if ID is valid, WP_Error otherwise.
    #//
    def get_user(self, id_=None):
        
        
        error_ = php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_id", __("Invalid user ID."), Array({"status": 404})))
        if php_int(id_) <= 0:
            return error_
        # end if
        user_ = get_userdata(php_int(id_))
        if php_empty(lambda : user_) or (not user_.exists()):
            return error_
        # end if
        if is_multisite() and (not is_user_member_of_blog(user_.ID)):
            return error_
        # end if
        return user_
    # end def get_user
    #// 
    #// Checks if a given request has access to read a user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, otherwise WP_Error object.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        user_ = self.get_user(request_["id"])
        if is_wp_error(user_):
            return user_
        # end if
        types_ = get_post_types(Array({"show_in_rest": True}), "names")
        if get_current_user_id() == user_.ID:
            return True
        # end if
        if "edit" == request_["context"] and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_view", __("Sorry, you are not allowed to list users."), Array({"status": rest_authorization_required_code()})))
        elif (not count_user_posts(user_.ID, types_)) and (not current_user_can("edit_user", user_.ID)) and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_view", __("Sorry, you are not allowed to list users."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_item_permissions_check
    #// 
    #// Retrieves a single user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request_=None):
        
        
        user_ = self.get_user(request_["id"])
        if is_wp_error(user_):
            return user_
        # end if
        user_ = self.prepare_item_for_response(user_, request_)
        response_ = rest_ensure_response(user_)
        return response_
    # end def get_item
    #// 
    #// Retrieves the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_current_item(self, request_=None):
        
        
        current_user_id_ = get_current_user_id()
        if php_empty(lambda : current_user_id_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_not_logged_in", __("You are not currently logged in."), Array({"status": 401})))
        # end if
        user_ = wp_get_current_user()
        response_ = self.prepare_item_for_response(user_, request_)
        response_ = rest_ensure_response(response_)
        return response_
    # end def get_current_item
    #// 
    #// Checks if a given request has access create users.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create items, WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request_=None):
        
        
        if (not current_user_can("create_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_create_user", __("Sorry, you are not allowed to create new users."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def create_item_permissions_check
    #// 
    #// Creates a single user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def create_item(self, request_=None):
        
        
        if (not php_empty(lambda : request_["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_exists", __("Cannot create existing user."), Array({"status": 400})))
        # end if
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : request_["roles"])) and (not php_empty(lambda : schema_["properties"]["roles"])):
            check_permission_ = self.check_role_update(request_["id"], request_["roles"])
            if is_wp_error(check_permission_):
                return check_permission_
            # end if
        # end if
        user_ = self.prepare_item_for_database(request_)
        if is_multisite():
            ret_ = wpmu_validate_user_signup(user_.user_login, user_.user_email)
            if is_wp_error(ret_["errors"]) and ret_["errors"].has_errors():
                error_ = php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", __("Invalid user parameter(s)."), Array({"status": 400})))
                for code_,messages_ in ret_["errors"].errors:
                    for message_ in messages_:
                        error_.add(code_, message_)
                    # end for
                    error_data_ = error_.get_error_data(code_)
                    if error_data_:
                        error_.add_data(error_data_, code_)
                    # end if
                # end for
                return error_
            # end if
        # end if
        if is_multisite():
            user_id_ = wpmu_create_user(user_.user_login, user_.user_pass, user_.user_email)
            if (not user_id_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_create", __("Error creating new user."), Array({"status": 500})))
            # end if
            user_.ID = user_id_
            user_id_ = wp_update_user(wp_slash(user_))
            if is_wp_error(user_id_):
                return user_id_
            # end if
            result_ = add_user_to_blog(get_site().id, user_id_, "")
            if is_wp_error(result_):
                return result_
            # end if
        else:
            user_id_ = wp_insert_user(wp_slash(user_))
            if is_wp_error(user_id_):
                return user_id_
            # end if
        # end if
        user_ = get_user_by("id", user_id_)
        #// 
        #// Fires immediately after a user is created or updated via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_User         $user     Inserted or updated user object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a user, false when updating.
        #//
        do_action("rest_insert_user", user_, request_, True)
        if (not php_empty(lambda : request_["roles"])) and (not php_empty(lambda : schema_["properties"]["roles"])):
            php_array_map(Array(user_, "add_role"), request_["roles"])
        # end if
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], user_id_)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        user_ = get_user_by("id", user_id_)
        fields_update_ = self.update_additional_fields_for_object(user_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// 
        #// Fires after a user is completely created or updated via the REST API.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_User         $user     Inserted or updated user object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a user, false when updating.
        #//
        do_action("rest_after_insert_user", user_, request_, True)
        response_ = self.prepare_item_for_response(user_, request_)
        response_ = rest_ensure_response(response_)
        response_.set_status(201)
        response_.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, user_id_)))
        return response_
    # end def create_item
    #// 
    #// Checks if a given request has access to update a user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def update_item_permissions_check(self, request_=None):
        
        
        user_ = self.get_user(request_["id"])
        if is_wp_error(user_):
            return user_
        # end if
        if (not php_empty(lambda : request_["roles"])):
            if (not current_user_can("promote_user", user_.ID)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit_roles", __("Sorry, you are not allowed to edit roles of this user."), Array({"status": rest_authorization_required_code()})))
            # end if
            request_params_ = php_array_keys(request_.get_params())
            sort(request_params_)
            #// If only 'id' and 'roles' are specified (we are only trying to
            #// edit roles), then only the 'promote_user' cap is required.
            if Array("id", "roles") == request_params_:
                return True
            # end if
        # end if
        if (not current_user_can("edit_user", user_.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit", __("Sorry, you are not allowed to edit this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def update_item_permissions_check
    #// 
    #// Updates a single user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def update_item(self, request_=None):
        
        
        user_ = self.get_user(request_["id"])
        if is_wp_error(user_):
            return user_
        # end if
        id_ = user_.ID
        if (not user_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_id", __("Invalid user ID."), Array({"status": 404})))
        # end if
        owner_id_ = email_exists(request_["email"])
        if owner_id_ and owner_id_ != id_:
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_email", __("Invalid email address."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : request_["username"])) and request_["username"] != user_.user_login:
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_argument", __("Username isn't editable."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : request_["slug"])) and request_["slug"] != user_.user_nicename and get_user_by("slug", request_["slug"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_slug", __("Invalid slug."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : request_["roles"])):
            check_permission_ = self.check_role_update(id_, request_["roles"])
            if is_wp_error(check_permission_):
                return check_permission_
            # end if
        # end if
        user_ = self.prepare_item_for_database(request_)
        #// Ensure we're operating on the same user we already checked.
        user_.ID = id_
        user_id_ = wp_update_user(wp_slash(user_))
        if is_wp_error(user_id_):
            return user_id_
        # end if
        user_ = get_user_by("id", user_id_)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-users-controller.php
        do_action("rest_insert_user", user_, request_, False)
        if (not php_empty(lambda : request_["roles"])):
            php_array_map(Array(user_, "add_role"), request_["roles"])
        # end if
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], id_)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        user_ = get_user_by("id", user_id_)
        fields_update_ = self.update_additional_fields_for_object(user_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-users-controller.php
        do_action("rest_after_insert_user", user_, request_, False)
        response_ = self.prepare_item_for_response(user_, request_)
        response_ = rest_ensure_response(response_)
        return response_
    # end def update_item
    #// 
    #// Checks if a given request has access to update the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def update_current_item_permissions_check(self, request_=None):
        
        
        request_["id"] = get_current_user_id()
        return self.update_item_permissions_check(request_)
    # end def update_current_item_permissions_check
    #// 
    #// Updates the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def update_current_item(self, request_=None):
        
        
        request_["id"] = get_current_user_id()
        return self.update_item(request_)
    # end def update_current_item
    #// 
    #// Checks if a given request has access delete a user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_item_permissions_check(self, request_=None):
        
        
        user_ = self.get_user(request_["id"])
        if is_wp_error(user_):
            return user_
        # end if
        if (not current_user_can("delete_user", user_.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_delete", __("Sorry, you are not allowed to delete this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def delete_item_permissions_check
    #// 
    #// Deletes a single user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def delete_item(self, request_=None):
        
        
        #// We don't support delete requests in multisite.
        if is_multisite():
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The user cannot be deleted."), Array({"status": 501})))
        # end if
        user_ = self.get_user(request_["id"])
        if is_wp_error(user_):
            return user_
        # end if
        id_ = user_.ID
        reassign_ = None if False == request_["reassign"] else absint(request_["reassign"])
        force_ = php_bool(request_["force"]) if (php_isset(lambda : request_["force"])) else False
        #// We don't support trashing for users.
        if (not force_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("Users do not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
        # end if
        if (not php_empty(lambda : reassign_)):
            if reassign_ == id_ or (not get_userdata(reassign_)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_reassign", __("Invalid user ID for reassignment."), Array({"status": 400})))
            # end if
        # end if
        request_.set_param("context", "edit")
        previous_ = self.prepare_item_for_response(user_, request_)
        #// Include user admin functions to get access to wp_delete_user().
        php_include_file(ABSPATH + "wp-admin/includes/user.php", once=True)
        result_ = wp_delete_user(id_, reassign_)
        if (not result_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The user cannot be deleted."), Array({"status": 500})))
        # end if
        response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        response_.set_data(Array({"deleted": True, "previous": previous_.get_data()}))
        #// 
        #// Fires immediately after a user is deleted via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_User          $user     The user data.
        #// @param WP_REST_Response $response The response returned from the API.
        #// @param WP_REST_Request  $request  The request sent to the API.
        #//
        do_action("rest_delete_user", user_, response_, request_)
        return response_
    # end def delete_item
    #// 
    #// Checks if a given request has access to delete the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_current_item_permissions_check(self, request_=None):
        
        
        request_["id"] = get_current_user_id()
        return self.delete_item_permissions_check(request_)
    # end def delete_current_item_permissions_check
    #// 
    #// Deletes the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def delete_current_item(self, request_=None):
        
        
        request_["id"] = get_current_user_id()
        return self.delete_item(request_)
    # end def delete_current_item
    #// 
    #// Prepares a single user output for response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_User         $user    User object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, user_=None, request_=None):
        
        
        data_ = Array()
        fields_ = self.get_fields_for_response(request_)
        if php_in_array("id", fields_, True):
            data_["id"] = user_.ID
        # end if
        if php_in_array("username", fields_, True):
            data_["username"] = user_.user_login
        # end if
        if php_in_array("name", fields_, True):
            data_["name"] = user_.display_name
        # end if
        if php_in_array("first_name", fields_, True):
            data_["first_name"] = user_.first_name
        # end if
        if php_in_array("last_name", fields_, True):
            data_["last_name"] = user_.last_name
        # end if
        if php_in_array("email", fields_, True):
            data_["email"] = user_.user_email
        # end if
        if php_in_array("url", fields_, True):
            data_["url"] = user_.user_url
        # end if
        if php_in_array("description", fields_, True):
            data_["description"] = user_.description
        # end if
        if php_in_array("link", fields_, True):
            data_["link"] = get_author_posts_url(user_.ID, user_.user_nicename)
        # end if
        if php_in_array("locale", fields_, True):
            data_["locale"] = get_user_locale(user_)
        # end if
        if php_in_array("nickname", fields_, True):
            data_["nickname"] = user_.nickname
        # end if
        if php_in_array("slug", fields_, True):
            data_["slug"] = user_.user_nicename
        # end if
        if php_in_array("roles", fields_, True):
            #// Defensively call array_values() to ensure an array is returned.
            data_["roles"] = php_array_values(user_.roles)
        # end if
        if php_in_array("registered_date", fields_, True):
            data_["registered_date"] = gmdate("c", strtotime(user_.user_registered))
        # end if
        if php_in_array("capabilities", fields_, True):
            data_["capabilities"] = user_.allcaps
        # end if
        if php_in_array("extra_capabilities", fields_, True):
            data_["extra_capabilities"] = user_.caps
        # end if
        if php_in_array("avatar_urls", fields_, True):
            data_["avatar_urls"] = rest_get_avatar_urls(user_)
        # end if
        if php_in_array("meta", fields_, True):
            data_["meta"] = self.meta.get_value(user_.ID, request_)
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "embed"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        #// Wrap the data in a response object.
        response_ = rest_ensure_response(data_)
        response_.add_links(self.prepare_links(user_))
        #// 
        #// Filters user data returned from the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_User          $user     User object used to create response.
        #// @param WP_REST_Request  $request  Request object.
        #//
        return apply_filters("rest_prepare_user", response_, user_, request_)
    # end def prepare_item_for_response
    #// 
    #// Prepares links for the user request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $user User object.
    #// @return array Links for the given user.
    #//
    def prepare_links(self, user_=None):
        
        
        links_ = Array({"self": Array({"href": rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, user_.ID))})}, {"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})})
        return links_
    # end def prepare_links
    #// 
    #// Prepares a single user for creation or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return object $prepared_user User object.
    #//
    def prepare_item_for_database(self, request_=None):
        
        
        prepared_user_ = php_new_class("stdClass", lambda : stdClass())
        schema_ = self.get_item_schema()
        #// Required arguments.
        if (php_isset(lambda : request_["email"])) and (not php_empty(lambda : schema_["properties"]["email"])):
            prepared_user_.user_email = request_["email"]
        # end if
        if (php_isset(lambda : request_["username"])) and (not php_empty(lambda : schema_["properties"]["username"])):
            prepared_user_.user_login = request_["username"]
        # end if
        if (php_isset(lambda : request_["password"])) and (not php_empty(lambda : schema_["properties"]["password"])):
            prepared_user_.user_pass = request_["password"]
        # end if
        #// Optional arguments.
        if (php_isset(lambda : request_["id"])):
            prepared_user_.ID = absint(request_["id"])
        # end if
        if (php_isset(lambda : request_["name"])) and (not php_empty(lambda : schema_["properties"]["name"])):
            prepared_user_.display_name = request_["name"]
        # end if
        if (php_isset(lambda : request_["first_name"])) and (not php_empty(lambda : schema_["properties"]["first_name"])):
            prepared_user_.first_name = request_["first_name"]
        # end if
        if (php_isset(lambda : request_["last_name"])) and (not php_empty(lambda : schema_["properties"]["last_name"])):
            prepared_user_.last_name = request_["last_name"]
        # end if
        if (php_isset(lambda : request_["nickname"])) and (not php_empty(lambda : schema_["properties"]["nickname"])):
            prepared_user_.nickname = request_["nickname"]
        # end if
        if (php_isset(lambda : request_["slug"])) and (not php_empty(lambda : schema_["properties"]["slug"])):
            prepared_user_.user_nicename = request_["slug"]
        # end if
        if (php_isset(lambda : request_["description"])) and (not php_empty(lambda : schema_["properties"]["description"])):
            prepared_user_.description = request_["description"]
        # end if
        if (php_isset(lambda : request_["url"])) and (not php_empty(lambda : schema_["properties"]["url"])):
            prepared_user_.user_url = request_["url"]
        # end if
        if (php_isset(lambda : request_["locale"])) and (not php_empty(lambda : schema_["properties"]["locale"])):
            prepared_user_.locale = request_["locale"]
        # end if
        #// Setting roles will be handled outside of this function.
        if (php_isset(lambda : request_["roles"])):
            prepared_user_.role = False
        # end if
        #// 
        #// Filters user data before insertion via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param object          $prepared_user User object.
        #// @param WP_REST_Request $request       Request object.
        #//
        return apply_filters("rest_pre_insert_user", prepared_user_, request_)
    # end def prepare_item_for_database
    #// 
    #// Determines if the current user is allowed to make the desired roles change.
    #// 
    #// @since 4.7.0
    #// 
    #// @param integer $user_id User ID.
    #// @param array   $roles   New user roles.
    #// @return true|WP_Error True if the current user is allowed to make the role change,
    #// otherwise a WP_Error object.
    #//
    def check_role_update(self, user_id_=None, roles_=None):
        
        
        global wp_roles_
        php_check_if_defined("wp_roles_")
        for role_ in roles_:
            if (not (php_isset(lambda : wp_roles_.role_objects[role_]))):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_role", php_sprintf(__("The role %s does not exist."), role_), Array({"status": 400})))
            # end if
            potential_role_ = wp_roles_.role_objects[role_]
            #// 
            #// Don't let anyone with 'edit_users' (admins) edit their own role to something without it.
            #// Multisite super admins can freely edit their blog roles -- they possess all caps.
            #//
            if (not is_multisite() and current_user_can("manage_sites")) and get_current_user_id() == user_id_ and (not potential_role_.has_cap("edit_users")):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_role", __("Sorry, you are not allowed to give users that role."), Array({"status": rest_authorization_required_code()})))
            # end if
            #// Include user admin functions to get access to get_editable_roles().
            php_include_file(ABSPATH + "wp-admin/includes/user.php", once=True)
            #// The new role must be editable by the logged-in user.
            editable_roles_ = get_editable_roles()
            if php_empty(lambda : editable_roles_[role_]):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_role", __("Sorry, you are not allowed to give users that role."), Array({"status": 403})))
            # end if
        # end for
        return True
    # end def check_role_update
    #// 
    #// Check a username for the REST API.
    #// 
    #// Performs a couple of checks like edit_user() in wp-admin/includes/user.php.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string          $value   The username submitted in the request.
    #// @param WP_REST_Request $request Full details about the request.
    #// @param string          $param   The parameter name.
    #// @return string|WP_Error The sanitized username, if valid, otherwise an error.
    #//
    def check_username(self, value_=None, request_=None, param_=None):
        
        
        username_ = php_str(value_)
        if (not validate_username(username_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_username", __("Username contains invalid characters."), Array({"status": 400})))
        # end if
        #// This filter is documented in wp-includes/user.php
        illegal_logins_ = apply_filters("illegal_user_logins", Array())
        if php_in_array(php_strtolower(username_), php_array_map("strtolower", illegal_logins_), True):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_username", __("Sorry, that username is not allowed."), Array({"status": 400})))
        # end if
        return username_
    # end def check_username
    #// 
    #// Check a user password for the REST API.
    #// 
    #// Performs a couple of checks like edit_user() in wp-admin/includes/user.php.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string          $value   The password submitted in the request.
    #// @param WP_REST_Request $request Full details about the request.
    #// @param string          $param   The parameter name.
    #// @return string|WP_Error The sanitized password, if valid, otherwise an error.
    #//
    def check_user_password(self, value_=None, request_=None, param_=None):
        
        
        password_ = php_str(value_)
        if php_empty(lambda : password_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_password", __("Passwords cannot be empty."), Array({"status": 400})))
        # end if
        if False != php_strpos(password_, "\\"):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_password", __("Passwords cannot contain the \"\\\" character."), Array({"status": 400})))
        # end if
        return password_
    # end def check_user_password
    #// 
    #// Retrieves the user's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "user", "type": "object", "properties": Array({"id": Array({"description": __("Unique identifier for the user."), "type": "integer", "context": Array("embed", "view", "edit"), "readonly": True})}, {"username": Array({"description": __("Login name for the user."), "type": "string", "context": Array("edit"), "required": True, "arg_options": Array({"sanitize_callback": Array(self, "check_username")})})}, {"name": Array({"description": __("Display name for the user."), "type": "string", "context": Array("embed", "view", "edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"first_name": Array({"description": __("First name for the user."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"last_name": Array({"description": __("Last name for the user."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"email": Array({"description": __("The email address for the user."), "type": "string", "format": "email", "context": Array("edit"), "required": True})}, {"url": Array({"description": __("URL of the user."), "type": "string", "format": "uri", "context": Array("embed", "view", "edit")})}, {"description": Array({"description": __("Description of the user."), "type": "string", "context": Array("embed", "view", "edit")})}, {"link": Array({"description": __("Author URL of the user."), "type": "string", "format": "uri", "context": Array("embed", "view", "edit"), "readonly": True})}, {"locale": Array({"description": __("Locale for the user."), "type": "string", "enum": php_array_merge(Array("", "en_US"), get_available_languages()), "context": Array("edit")})}, {"nickname": Array({"description": __("The nickname for the user."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"slug": Array({"description": __("An alphanumeric identifier for the user."), "type": "string", "context": Array("embed", "view", "edit"), "arg_options": Array({"sanitize_callback": Array(self, "sanitize_slug")})})}, {"registered_date": Array({"description": __("Registration date for the user."), "type": "string", "format": "date-time", "context": Array("edit"), "readonly": True})}, {"roles": Array({"description": __("Roles assigned to the user."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("edit")})}, {"password": Array({"description": __("Password for the user (never included)."), "type": "string", "context": Array(), "required": True, "arg_options": Array({"sanitize_callback": Array(self, "check_user_password")})})}, {"capabilities": Array({"description": __("All capabilities assigned to the user."), "type": "object", "context": Array("edit"), "readonly": True})}, {"extra_capabilities": Array({"description": __("Any extra capabilities assigned to the user."), "type": "object", "context": Array("edit"), "readonly": True})})})
        if get_option("show_avatars"):
            avatar_properties_ = Array()
            avatar_sizes_ = rest_get_avatar_sizes()
            for size_ in avatar_sizes_:
                avatar_properties_[size_] = Array({"description": php_sprintf(__("Avatar URL with image size of %d pixels."), size_), "type": "string", "format": "uri", "context": Array("embed", "view", "edit")})
            # end for
            schema_["properties"]["avatar_urls"] = Array({"description": __("Avatar URLs for the user."), "type": "object", "context": Array("embed", "view", "edit"), "readonly": True, "properties": avatar_properties_})
        # end if
        schema_["properties"]["meta"] = self.meta.get_field_schema()
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
        
        
        query_params_ = super().get_collection_params()
        query_params_["context"]["default"] = "view"
        query_params_["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params_["order"] = Array({"default": "asc", "description": __("Order sort attribute ascending or descending."), "enum": Array("asc", "desc"), "type": "string"})
        query_params_["orderby"] = Array({"default": "name", "description": __("Sort collection by object attribute."), "enum": Array("id", "include", "name", "registered_date", "slug", "include_slugs", "email", "url"), "type": "string"})
        query_params_["slug"] = Array({"description": __("Limit result set to users with one or more specific slugs."), "type": "array", "items": Array({"type": "string"})})
        query_params_["roles"] = Array({"description": __("Limit result set to users matching at least one specific role provided. Accepts csv list or single role."), "type": "array", "items": Array({"type": "string"})})
        query_params_["who"] = Array({"description": __("Limit result set to users who are considered authors."), "type": "string", "enum": Array("authors")})
        #// 
        #// Filter collection parameters for the users controller.
        #// 
        #// This filter registers the collection parameter, but does not map the
        #// collection parameter to an internal WP_User_Query parameter.  Use the
        #// `rest_user_query` filter to set WP_User_Query arguments.
        #// 
        #// @since 4.7.0
        #// 
        #// @param array $query_params JSON Schema-formatted collection parameters.
        #//
        return apply_filters("rest_user_collection_params", query_params_)
    # end def get_collection_params
# end class WP_REST_Users_Controller
