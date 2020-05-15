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
    def check_reassign(self, value=None, request=None, param=None):
        
        if php_is_numeric(value):
            return value
        # end if
        if php_empty(lambda : value) or False == value or "false" == value:
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
    def get_items_permissions_check(self, request=None):
        
        #// Check if roles is specified in GET request and if user can list users.
        if (not php_empty(lambda : request["roles"])) and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_view", __("Sorry, you are not allowed to filter users by role."), Array({"status": rest_authorization_required_code()})))
        # end if
        if "edit" == request["context"] and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to list users."), Array({"status": rest_authorization_required_code()})))
        # end if
        if php_in_array(request["orderby"], Array("email", "registered_date"), True) and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_orderby", __("Sorry, you are not allowed to order users by this parameter."), Array({"status": rest_authorization_required_code()})))
        # end if
        if "authors" == request["who"]:
            types = get_post_types(Array({"show_in_rest": True}), "objects")
            for type in types:
                if post_type_supports(type.name, "author") and current_user_can(type.cap.edit_posts):
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
    def get_items(self, request=None):
        
        #// Retrieve the list of registered collection query parameters.
        registered = self.get_collection_params()
        #// 
        #// This array defines mappings between public API query parameters whose
        #// values are accepted as-passed, and their internal WP_Query parameter
        #// name equivalents (some are the same). Only values which are also
        #// present in $registered will be set.
        #//
        parameter_mappings = Array({"exclude": "exclude", "include": "include", "order": "order", "per_page": "number", "search": "search", "roles": "role__in", "slug": "nicename__in"})
        prepared_args = Array()
        #// 
        #// For each known parameter which is both registered and present in the request,
        #// set the parameter's value on the query $prepared_args.
        #//
        for api_param,wp_param in parameter_mappings:
            if (php_isset(lambda : registered[api_param]) and php_isset(lambda : request[api_param])):
                prepared_args[wp_param] = request[api_param]
            # end if
        # end for
        if (php_isset(lambda : registered["offset"])) and (not php_empty(lambda : request["offset"])):
            prepared_args["offset"] = request["offset"]
        else:
            prepared_args["offset"] = request["page"] - 1 * prepared_args["number"]
        # end if
        if (php_isset(lambda : registered["orderby"])):
            orderby_possibles = Array({"id": "ID", "include": "include", "name": "display_name", "registered_date": "registered", "slug": "user_nicename", "include_slugs": "nicename__in", "email": "user_email", "url": "user_url"})
            prepared_args["orderby"] = orderby_possibles[request["orderby"]]
        # end if
        if (php_isset(lambda : registered["who"])) and (not php_empty(lambda : request["who"])) and "authors" == request["who"]:
            prepared_args["who"] = "authors"
        elif (not current_user_can("list_users")):
            prepared_args["has_published_posts"] = get_post_types(Array({"show_in_rest": True}), "names")
        # end if
        if (not php_empty(lambda : prepared_args["search"])):
            prepared_args["search"] = "*" + prepared_args["search"] + "*"
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
        prepared_args = apply_filters("rest_user_query", prepared_args, request)
        query = php_new_class("WP_User_Query", lambda : WP_User_Query(prepared_args))
        users = Array()
        for user in query.results:
            data = self.prepare_item_for_response(user, request)
            users[-1] = self.prepare_response_for_collection(data)
        # end for
        response = rest_ensure_response(users)
        #// Store pagination values for headers then unset for count query.
        per_page = int(prepared_args["number"])
        page = ceil(int(prepared_args["offset"]) / per_page + 1)
        prepared_args["fields"] = "ID"
        total_users = query.get_total()
        if total_users < 1:
            prepared_args["number"] = None
            prepared_args["offset"] = None
            count_query = php_new_class("WP_User_Query", lambda : WP_User_Query(prepared_args))
            total_users = count_query.get_total()
        # end if
        response.header("X-WP-Total", int(total_users))
        max_pages = ceil(total_users / per_page)
        response.header("X-WP-TotalPages", int(max_pages))
        base = add_query_arg(urlencode_deep(request.get_query_params()), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
        if page > 1:
            prev_page = page - 1
            if prev_page > max_pages:
                prev_page = max_pages
            # end if
            prev_link = add_query_arg("page", prev_page, base)
            response.link_header("prev", prev_link)
        # end if
        if max_pages > page:
            next_page = page + 1
            next_link = add_query_arg("page", next_page, base)
            response.link_header("next", next_link)
        # end if
        return response
    # end def get_items
    #// 
    #// Get the user, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_User|WP_Error True if ID is valid, WP_Error otherwise.
    #//
    def get_user(self, id=None):
        
        error = php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_id", __("Invalid user ID."), Array({"status": 404})))
        if int(id) <= 0:
            return error
        # end if
        user = get_userdata(int(id))
        if php_empty(lambda : user) or (not user.exists()):
            return error
        # end if
        if is_multisite() and (not is_user_member_of_blog(user.ID)):
            return error
        # end if
        return user
    # end def get_user
    #// 
    #// Checks if a given request has access to read a user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, otherwise WP_Error object.
    #//
    def get_item_permissions_check(self, request=None):
        
        user = self.get_user(request["id"])
        if is_wp_error(user):
            return user
        # end if
        types = get_post_types(Array({"show_in_rest": True}), "names")
        if get_current_user_id() == user.ID:
            return True
        # end if
        if "edit" == request["context"] and (not current_user_can("list_users")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_view", __("Sorry, you are not allowed to list users."), Array({"status": rest_authorization_required_code()})))
        elif (not count_user_posts(user.ID, types)) and (not current_user_can("edit_user", user.ID)) and (not current_user_can("list_users")):
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
    def get_item(self, request=None):
        
        user = self.get_user(request["id"])
        if is_wp_error(user):
            return user
        # end if
        user = self.prepare_item_for_response(user, request)
        response = rest_ensure_response(user)
        return response
    # end def get_item
    #// 
    #// Retrieves the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_current_item(self, request=None):
        
        current_user_id = get_current_user_id()
        if php_empty(lambda : current_user_id):
            return php_new_class("WP_Error", lambda : WP_Error("rest_not_logged_in", __("You are not currently logged in."), Array({"status": 401})))
        # end if
        user = wp_get_current_user()
        response = self.prepare_item_for_response(user, request)
        response = rest_ensure_response(response)
        return response
    # end def get_current_item
    #// 
    #// Checks if a given request has access create users.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create items, WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request=None):
        
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
    def create_item(self, request=None):
        
        if (not php_empty(lambda : request["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_exists", __("Cannot create existing user."), Array({"status": 400})))
        # end if
        schema = self.get_item_schema()
        if (not php_empty(lambda : request["roles"])) and (not php_empty(lambda : schema["properties"]["roles"])):
            check_permission = self.check_role_update(request["id"], request["roles"])
            if is_wp_error(check_permission):
                return check_permission
            # end if
        # end if
        user = self.prepare_item_for_database(request)
        if is_multisite():
            ret = wpmu_validate_user_signup(user.user_login, user.user_email)
            if is_wp_error(ret["errors"]) and ret["errors"].has_errors():
                error = php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", __("Invalid user parameter(s)."), Array({"status": 400})))
                for code,messages in ret["errors"].errors:
                    for message in messages:
                        error.add(code, message)
                    # end for
                    error_data = error.get_error_data(code)
                    if error_data:
                        error.add_data(error_data, code)
                    # end if
                # end for
                return error
            # end if
        # end if
        if is_multisite():
            user_id = wpmu_create_user(user.user_login, user.user_pass, user.user_email)
            if (not user_id):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_create", __("Error creating new user."), Array({"status": 500})))
            # end if
            user.ID = user_id
            user_id = wp_update_user(wp_slash(user))
            if is_wp_error(user_id):
                return user_id
            # end if
            result = add_user_to_blog(get_site().id, user_id, "")
            if is_wp_error(result):
                return result
            # end if
        else:
            user_id = wp_insert_user(wp_slash(user))
            if is_wp_error(user_id):
                return user_id
            # end if
        # end if
        user = get_user_by("id", user_id)
        #// 
        #// Fires immediately after a user is created or updated via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_User         $user     Inserted or updated user object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a user, false when updating.
        #//
        do_action("rest_insert_user", user, request, True)
        if (not php_empty(lambda : request["roles"])) and (not php_empty(lambda : schema["properties"]["roles"])):
            php_array_map(Array(user, "add_role"), request["roles"])
        # end if
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], user_id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        user = get_user_by("id", user_id)
        fields_update = self.update_additional_fields_for_object(user, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// 
        #// Fires after a user is completely created or updated via the REST API.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_User         $user     Inserted or updated user object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a user, false when updating.
        #//
        do_action("rest_after_insert_user", user, request, True)
        response = self.prepare_item_for_response(user, request)
        response = rest_ensure_response(response)
        response.set_status(201)
        response.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, user_id)))
        return response
    # end def create_item
    #// 
    #// Checks if a given request has access to update a user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def update_item_permissions_check(self, request=None):
        
        user = self.get_user(request["id"])
        if is_wp_error(user):
            return user
        # end if
        if (not php_empty(lambda : request["roles"])):
            if (not current_user_can("promote_user", user.ID)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit_roles", __("Sorry, you are not allowed to edit roles of this user."), Array({"status": rest_authorization_required_code()})))
            # end if
            request_params = php_array_keys(request.get_params())
            sort(request_params)
            #// If only 'id' and 'roles' are specified (we are only trying to
            #// edit roles), then only the 'promote_user' cap is required.
            if Array("id", "roles") == request_params:
                return True
            # end if
        # end if
        if (not current_user_can("edit_user", user.ID)):
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
    def update_item(self, request=None):
        
        user = self.get_user(request["id"])
        if is_wp_error(user):
            return user
        # end if
        id = user.ID
        if (not user):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_id", __("Invalid user ID."), Array({"status": 404})))
        # end if
        owner_id = email_exists(request["email"])
        if owner_id and owner_id != id:
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_email", __("Invalid email address."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : request["username"])) and request["username"] != user.user_login:
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_argument", __("Username isn't editable."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : request["slug"])) and request["slug"] != user.user_nicename and get_user_by("slug", request["slug"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_slug", __("Invalid slug."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : request["roles"])):
            check_permission = self.check_role_update(id, request["roles"])
            if is_wp_error(check_permission):
                return check_permission
            # end if
        # end if
        user = self.prepare_item_for_database(request)
        #// Ensure we're operating on the same user we already checked.
        user.ID = id
        user_id = wp_update_user(wp_slash(user))
        if is_wp_error(user_id):
            return user_id
        # end if
        user = get_user_by("id", user_id)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-users-controller.php
        do_action("rest_insert_user", user, request, False)
        if (not php_empty(lambda : request["roles"])):
            php_array_map(Array(user, "add_role"), request["roles"])
        # end if
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        user = get_user_by("id", user_id)
        fields_update = self.update_additional_fields_for_object(user, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-users-controller.php
        do_action("rest_after_insert_user", user, request, False)
        response = self.prepare_item_for_response(user, request)
        response = rest_ensure_response(response)
        return response
    # end def update_item
    #// 
    #// Checks if a given request has access to update the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def update_current_item_permissions_check(self, request=None):
        
        request["id"] = get_current_user_id()
        return self.update_item_permissions_check(request)
    # end def update_current_item_permissions_check
    #// 
    #// Updates the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def update_current_item(self, request=None):
        
        request["id"] = get_current_user_id()
        return self.update_item(request)
    # end def update_current_item
    #// 
    #// Checks if a given request has access delete a user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_item_permissions_check(self, request=None):
        
        user = self.get_user(request["id"])
        if is_wp_error(user):
            return user
        # end if
        if (not current_user_can("delete_user", user.ID)):
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
    def delete_item(self, request=None):
        
        #// We don't support delete requests in multisite.
        if is_multisite():
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The user cannot be deleted."), Array({"status": 501})))
        # end if
        user = self.get_user(request["id"])
        if is_wp_error(user):
            return user
        # end if
        id = user.ID
        reassign = None if False == request["reassign"] else absint(request["reassign"])
        force = bool(request["force"]) if (php_isset(lambda : request["force"])) else False
        #// We don't support trashing for users.
        if (not force):
            return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("Users do not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
        # end if
        if (not php_empty(lambda : reassign)):
            if reassign == id or (not get_userdata(reassign)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_reassign", __("Invalid user ID for reassignment."), Array({"status": 400})))
            # end if
        # end if
        request.set_param("context", "edit")
        previous = self.prepare_item_for_response(user, request)
        #// Include user admin functions to get access to wp_delete_user().
        php_include_file(ABSPATH + "wp-admin/includes/user.php", once=True)
        result = wp_delete_user(id, reassign)
        if (not result):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The user cannot be deleted."), Array({"status": 500})))
        # end if
        response = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        response.set_data(Array({"deleted": True, "previous": previous.get_data()}))
        #// 
        #// Fires immediately after a user is deleted via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_User          $user     The user data.
        #// @param WP_REST_Response $response The response returned from the API.
        #// @param WP_REST_Request  $request  The request sent to the API.
        #//
        do_action("rest_delete_user", user, response, request)
        return response
    # end def delete_item
    #// 
    #// Checks if a given request has access to delete the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_current_item_permissions_check(self, request=None):
        
        request["id"] = get_current_user_id()
        return self.delete_item_permissions_check(request)
    # end def delete_current_item_permissions_check
    #// 
    #// Deletes the current user.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def delete_current_item(self, request=None):
        
        request["id"] = get_current_user_id()
        return self.delete_item(request)
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
    def prepare_item_for_response(self, user=None, request=None):
        
        data = Array()
        fields = self.get_fields_for_response(request)
        if php_in_array("id", fields, True):
            data["id"] = user.ID
        # end if
        if php_in_array("username", fields, True):
            data["username"] = user.user_login
        # end if
        if php_in_array("name", fields, True):
            data["name"] = user.display_name
        # end if
        if php_in_array("first_name", fields, True):
            data["first_name"] = user.first_name
        # end if
        if php_in_array("last_name", fields, True):
            data["last_name"] = user.last_name
        # end if
        if php_in_array("email", fields, True):
            data["email"] = user.user_email
        # end if
        if php_in_array("url", fields, True):
            data["url"] = user.user_url
        # end if
        if php_in_array("description", fields, True):
            data["description"] = user.description
        # end if
        if php_in_array("link", fields, True):
            data["link"] = get_author_posts_url(user.ID, user.user_nicename)
        # end if
        if php_in_array("locale", fields, True):
            data["locale"] = get_user_locale(user)
        # end if
        if php_in_array("nickname", fields, True):
            data["nickname"] = user.nickname
        # end if
        if php_in_array("slug", fields, True):
            data["slug"] = user.user_nicename
        # end if
        if php_in_array("roles", fields, True):
            #// Defensively call array_values() to ensure an array is returned.
            data["roles"] = php_array_values(user.roles)
        # end if
        if php_in_array("registered_date", fields, True):
            data["registered_date"] = gmdate("c", strtotime(user.user_registered))
        # end if
        if php_in_array("capabilities", fields, True):
            data["capabilities"] = user.allcaps
        # end if
        if php_in_array("extra_capabilities", fields, True):
            data["extra_capabilities"] = user.caps
        # end if
        if php_in_array("avatar_urls", fields, True):
            data["avatar_urls"] = rest_get_avatar_urls(user)
        # end if
        if php_in_array("meta", fields, True):
            data["meta"] = self.meta.get_value(user.ID, request)
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "embed"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        #// Wrap the data in a response object.
        response = rest_ensure_response(data)
        response.add_links(self.prepare_links(user))
        #// 
        #// Filters user data returned from the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_User          $user     User object used to create response.
        #// @param WP_REST_Request  $request  Request object.
        #//
        return apply_filters("rest_prepare_user", response, user, request)
    # end def prepare_item_for_response
    #// 
    #// Prepares links for the user request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $user User object.
    #// @return array Links for the given user.
    #//
    def prepare_links(self, user=None):
        
        links = Array({"self": Array({"href": rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, user.ID))})}, {"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})})
        return links
    # end def prepare_links
    #// 
    #// Prepares a single user for creation or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return object $prepared_user User object.
    #//
    def prepare_item_for_database(self, request=None):
        
        prepared_user = php_new_class("stdClass", lambda : stdClass())
        schema = self.get_item_schema()
        #// Required arguments.
        if (php_isset(lambda : request["email"])) and (not php_empty(lambda : schema["properties"]["email"])):
            prepared_user.user_email = request["email"]
        # end if
        if (php_isset(lambda : request["username"])) and (not php_empty(lambda : schema["properties"]["username"])):
            prepared_user.user_login = request["username"]
        # end if
        if (php_isset(lambda : request["password"])) and (not php_empty(lambda : schema["properties"]["password"])):
            prepared_user.user_pass = request["password"]
        # end if
        #// Optional arguments.
        if (php_isset(lambda : request["id"])):
            prepared_user.ID = absint(request["id"])
        # end if
        if (php_isset(lambda : request["name"])) and (not php_empty(lambda : schema["properties"]["name"])):
            prepared_user.display_name = request["name"]
        # end if
        if (php_isset(lambda : request["first_name"])) and (not php_empty(lambda : schema["properties"]["first_name"])):
            prepared_user.first_name = request["first_name"]
        # end if
        if (php_isset(lambda : request["last_name"])) and (not php_empty(lambda : schema["properties"]["last_name"])):
            prepared_user.last_name = request["last_name"]
        # end if
        if (php_isset(lambda : request["nickname"])) and (not php_empty(lambda : schema["properties"]["nickname"])):
            prepared_user.nickname = request["nickname"]
        # end if
        if (php_isset(lambda : request["slug"])) and (not php_empty(lambda : schema["properties"]["slug"])):
            prepared_user.user_nicename = request["slug"]
        # end if
        if (php_isset(lambda : request["description"])) and (not php_empty(lambda : schema["properties"]["description"])):
            prepared_user.description = request["description"]
        # end if
        if (php_isset(lambda : request["url"])) and (not php_empty(lambda : schema["properties"]["url"])):
            prepared_user.user_url = request["url"]
        # end if
        if (php_isset(lambda : request["locale"])) and (not php_empty(lambda : schema["properties"]["locale"])):
            prepared_user.locale = request["locale"]
        # end if
        #// Setting roles will be handled outside of this function.
        if (php_isset(lambda : request["roles"])):
            prepared_user.role = False
        # end if
        #// 
        #// Filters user data before insertion via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param object          $prepared_user User object.
        #// @param WP_REST_Request $request       Request object.
        #//
        return apply_filters("rest_pre_insert_user", prepared_user, request)
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
    def check_role_update(self, user_id=None, roles=None):
        
        global wp_roles
        php_check_if_defined("wp_roles")
        for role in roles:
            if (not (php_isset(lambda : wp_roles.role_objects[role]))):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_role", php_sprintf(__("The role %s does not exist."), role), Array({"status": 400})))
            # end if
            potential_role = wp_roles.role_objects[role]
            #// 
            #// Don't let anyone with 'edit_users' (admins) edit their own role to something without it.
            #// Multisite super admins can freely edit their blog roles -- they possess all caps.
            #//
            if (not is_multisite() and current_user_can("manage_sites")) and get_current_user_id() == user_id and (not potential_role.has_cap("edit_users")):
                return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_role", __("Sorry, you are not allowed to give users that role."), Array({"status": rest_authorization_required_code()})))
            # end if
            #// Include user admin functions to get access to get_editable_roles().
            php_include_file(ABSPATH + "wp-admin/includes/user.php", once=True)
            #// The new role must be editable by the logged-in user.
            editable_roles = get_editable_roles()
            if php_empty(lambda : editable_roles[role]):
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
    def check_username(self, value=None, request=None, param=None):
        
        username = str(value)
        if (not validate_username(username)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_username", __("Username contains invalid characters."), Array({"status": 400})))
        # end if
        #// This filter is documented in wp-includes/user.php
        illegal_logins = apply_filters("illegal_user_logins", Array())
        if php_in_array(php_strtolower(username), php_array_map("strtolower", illegal_logins), True):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_username", __("Sorry, that username is not allowed."), Array({"status": 400})))
        # end if
        return username
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
    def check_user_password(self, value=None, request=None, param=None):
        
        password = str(value)
        if php_empty(lambda : password):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_password", __("Passwords cannot be empty."), Array({"status": 400})))
        # end if
        if False != php_strpos(password, "\\"):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_invalid_password", __("Passwords cannot contain the \"\\\" character."), Array({"status": 400})))
        # end if
        return password
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
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "user", "type": "object", "properties": Array({"id": Array({"description": __("Unique identifier for the user."), "type": "integer", "context": Array("embed", "view", "edit"), "readonly": True})}, {"username": Array({"description": __("Login name for the user."), "type": "string", "context": Array("edit"), "required": True, "arg_options": Array({"sanitize_callback": Array(self, "check_username")})})}, {"name": Array({"description": __("Display name for the user."), "type": "string", "context": Array("embed", "view", "edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"first_name": Array({"description": __("First name for the user."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"last_name": Array({"description": __("Last name for the user."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"email": Array({"description": __("The email address for the user."), "type": "string", "format": "email", "context": Array("edit"), "required": True})}, {"url": Array({"description": __("URL of the user."), "type": "string", "format": "uri", "context": Array("embed", "view", "edit")})}, {"description": Array({"description": __("Description of the user."), "type": "string", "context": Array("embed", "view", "edit")})}, {"link": Array({"description": __("Author URL of the user."), "type": "string", "format": "uri", "context": Array("embed", "view", "edit"), "readonly": True})}, {"locale": Array({"description": __("Locale for the user."), "type": "string", "enum": php_array_merge(Array("", "en_US"), get_available_languages()), "context": Array("edit")})}, {"nickname": Array({"description": __("The nickname for the user."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"slug": Array({"description": __("An alphanumeric identifier for the user."), "type": "string", "context": Array("embed", "view", "edit"), "arg_options": Array({"sanitize_callback": Array(self, "sanitize_slug")})})}, {"registered_date": Array({"description": __("Registration date for the user."), "type": "string", "format": "date-time", "context": Array("edit"), "readonly": True})}, {"roles": Array({"description": __("Roles assigned to the user."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("edit")})}, {"password": Array({"description": __("Password for the user (never included)."), "type": "string", "context": Array(), "required": True, "arg_options": Array({"sanitize_callback": Array(self, "check_user_password")})})}, {"capabilities": Array({"description": __("All capabilities assigned to the user."), "type": "object", "context": Array("edit"), "readonly": True})}, {"extra_capabilities": Array({"description": __("Any extra capabilities assigned to the user."), "type": "object", "context": Array("edit"), "readonly": True})})})
        if get_option("show_avatars"):
            avatar_properties = Array()
            avatar_sizes = rest_get_avatar_sizes()
            for size in avatar_sizes:
                avatar_properties[size] = Array({"description": php_sprintf(__("Avatar URL with image size of %d pixels."), size), "type": "string", "format": "uri", "context": Array("embed", "view", "edit")})
            # end for
            schema["properties"]["avatar_urls"] = Array({"description": __("Avatar URLs for the user."), "type": "object", "context": Array("embed", "view", "edit"), "readonly": True, "properties": avatar_properties})
        # end if
        schema["properties"]["meta"] = self.meta.get_field_schema()
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
        
        query_params = super().get_collection_params()
        query_params["context"]["default"] = "view"
        query_params["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params["order"] = Array({"default": "asc", "description": __("Order sort attribute ascending or descending."), "enum": Array("asc", "desc"), "type": "string"})
        query_params["orderby"] = Array({"default": "name", "description": __("Sort collection by object attribute."), "enum": Array("id", "include", "name", "registered_date", "slug", "include_slugs", "email", "url"), "type": "string"})
        query_params["slug"] = Array({"description": __("Limit result set to users with one or more specific slugs."), "type": "array", "items": Array({"type": "string"})})
        query_params["roles"] = Array({"description": __("Limit result set to users matching at least one specific role provided. Accepts csv list or single role."), "type": "array", "items": Array({"type": "string"})})
        query_params["who"] = Array({"description": __("Limit result set to users who are considered authors."), "type": "string", "enum": Array("authors")})
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
        return apply_filters("rest_user_collection_params", query_params)
    # end def get_collection_params
# end class WP_REST_Users_Controller
