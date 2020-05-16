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
#// REST API: WP_REST_Comments_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core controller used to access comments via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Comments_Controller(WP_REST_Controller):
    meta = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #//
    def __init__(self):
        
        self.namespace = "wp/v2"
        self.rest_base = "comments"
        self.meta = php_new_class("WP_REST_Comment_Meta_Fields", lambda : WP_REST_Comment_Meta_Fields())
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
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<id>[\\d]+)", Array({"args": Array({"id": Array({"description": __("Unique identifier for the object."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))}, {"password": Array({"description": __("The password for the parent post of the comment (if the post is password protected)."), "type": "string"})})}), Array({"methods": WP_REST_Server.EDITABLE, "callback": Array(self, "update_item"), "permission_callback": Array(self, "update_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE)}), Array({"methods": WP_REST_Server.DELETABLE, "callback": Array(self, "delete_item"), "permission_callback": Array(self, "delete_item_permissions_check"), "args": Array({"force": Array({"type": "boolean", "default": False, "description": __("Whether to bypass Trash and force deletion.")})}, {"password": Array({"description": __("The password for the parent post of the comment (if the post is password protected)."), "type": "string"})})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks if a given request has access to read comments.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, error object otherwise.
    #//
    def get_items_permissions_check(self, request=None):
        
        if (not php_empty(lambda : request["post"])):
            for post_id in request["post"]:
                post = get_post(post_id)
                if (not php_empty(lambda : post_id)) and post and (not self.check_read_post_permission(post, request)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_post", __("Sorry, you are not allowed to read the post for this comment."), Array({"status": rest_authorization_required_code()})))
                elif 0 == post_id and (not current_user_can("moderate_comments")):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read", __("Sorry, you are not allowed to read comments without a post."), Array({"status": rest_authorization_required_code()})))
                # end if
            # end for
        # end if
        if (not php_empty(lambda : request["context"])) and "edit" == request["context"] and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit comments."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not current_user_can("edit_posts")):
            protected_params = Array("author", "author_exclude", "author_email", "type", "status")
            forbidden_params = Array()
            for param in protected_params:
                if "status" == param:
                    if "approve" != request[param]:
                        forbidden_params[-1] = param
                    # end if
                elif "type" == param:
                    if "comment" != request[param]:
                        forbidden_params[-1] = param
                    # end if
                elif (not php_empty(lambda : request[param])):
                    forbidden_params[-1] = param
                # end if
            # end for
            if (not php_empty(lambda : forbidden_params)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_param", php_sprintf(__("Query parameter not permitted: %s"), php_implode(", ", forbidden_params)), Array({"status": rest_authorization_required_code()})))
            # end if
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Retrieves a list of comment items.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or error object on failure.
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
        parameter_mappings = Array({"author": "author__in", "author_email": "author_email", "author_exclude": "author__not_in", "exclude": "comment__not_in", "include": "comment__in", "offset": "offset", "order": "order", "parent": "parent__in", "parent_exclude": "parent__not_in", "per_page": "number", "post": "post__in", "search": "search", "status": "status", "type": "type"})
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
        #// Ensure certain parameter values default to empty strings.
        for param in Array("author_email", "search"):
            if (not (php_isset(lambda : prepared_args[param]))):
                prepared_args[param] = ""
            # end if
        # end for
        if (php_isset(lambda : registered["orderby"])):
            prepared_args["orderby"] = self.normalize_query_param(request["orderby"])
        # end if
        prepared_args["no_found_rows"] = False
        prepared_args["date_query"] = Array()
        #// Set before into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered["before"]) and php_isset(lambda : request["before"])):
            prepared_args["date_query"][0]["before"] = request["before"]
        # end if
        #// Set after into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered["after"]) and php_isset(lambda : request["after"])):
            prepared_args["date_query"][0]["after"] = request["after"]
        # end if
        if (php_isset(lambda : registered["page"])) and php_empty(lambda : request["offset"]):
            prepared_args["offset"] = prepared_args["number"] * absint(request["page"]) - 1
        # end if
        #// 
        #// Filters arguments, before passing to WP_Comment_Query, when querying comments via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @link https://developer.wordpress.org/reference/classes/wp_comment_query
        #// 
        #// @param array           $prepared_args Array of arguments for WP_Comment_Query.
        #// @param WP_REST_Request $request       The current request.
        #//
        prepared_args = apply_filters("rest_comment_query", prepared_args, request)
        query = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
        query_result = query.query(prepared_args)
        comments = Array()
        for comment in query_result:
            if (not self.check_read_permission(comment, request)):
                continue
            # end if
            data = self.prepare_item_for_response(comment, request)
            comments[-1] = self.prepare_response_for_collection(data)
        # end for
        total_comments = php_int(query.found_comments)
        max_pages = php_int(query.max_num_pages)
        if total_comments < 1:
            prepared_args["number"] = None
            prepared_args["offset"] = None
            query = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
            prepared_args["count"] = True
            total_comments = query.query(prepared_args)
            max_pages = ceil(total_comments / request["per_page"])
        # end if
        response = rest_ensure_response(comments)
        response.header("X-WP-Total", total_comments)
        response.header("X-WP-TotalPages", max_pages)
        base = add_query_arg(urlencode_deep(request.get_query_params()), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
        if request["page"] > 1:
            prev_page = request["page"] - 1
            if prev_page > max_pages:
                prev_page = max_pages
            # end if
            prev_link = add_query_arg("page", prev_page, base)
            response.link_header("prev", prev_link)
        # end if
        if max_pages > request["page"]:
            next_page = request["page"] + 1
            next_link = add_query_arg("page", next_page, base)
            response.link_header("next", next_link)
        # end if
        return response
    # end def get_items
    #// 
    #// Get the comment, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_Comment|WP_Error Comment object if ID is valid, WP_Error otherwise.
    #//
    def get_comment(self, id=None):
        
        error = php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_id", __("Invalid comment ID."), Array({"status": 404})))
        if php_int(id) <= 0:
            return error
        # end if
        id = php_int(id)
        comment = get_comment(id)
        if php_empty(lambda : comment):
            return error
        # end if
        if (not php_empty(lambda : comment.comment_post_ID)):
            post = get_post(php_int(comment.comment_post_ID))
            if php_empty(lambda : post):
                return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post ID."), Array({"status": 404})))
            # end if
        # end if
        return comment
    # end def get_comment
    #// 
    #// Checks if a given request has access to read the comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, error object otherwise.
    #//
    def get_item_permissions_check(self, request=None):
        
        comment = self.get_comment(request["id"])
        if is_wp_error(comment):
            return comment
        # end if
        if (not php_empty(lambda : request["context"])) and "edit" == request["context"] and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit comments."), Array({"status": rest_authorization_required_code()})))
        # end if
        post = get_post(comment.comment_post_ID)
        if (not self.check_read_permission(comment, request)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read", __("Sorry, you are not allowed to read this comment."), Array({"status": rest_authorization_required_code()})))
        # end if
        if post and (not self.check_read_post_permission(post, request)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_post", __("Sorry, you are not allowed to read the post for this comment."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_item_permissions_check
    #// 
    #// Retrieves a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or error object on failure.
    #//
    def get_item(self, request=None):
        
        comment = self.get_comment(request["id"])
        if is_wp_error(comment):
            return comment
        # end if
        data = self.prepare_item_for_response(comment, request)
        response = rest_ensure_response(data)
        return response
    # end def get_item
    #// 
    #// Checks if a given request has access to create a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create items, error object otherwise.
    #//
    def create_item_permissions_check(self, request=None):
        
        if (not is_user_logged_in()):
            if get_option("comment_registration"):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_login_required", __("Sorry, you must be logged in to comment."), Array({"status": 401})))
            # end if
            #// 
            #// Filter whether comments can be created without authentication.
            #// 
            #// Enables creating comments for anonymous users.
            #// 
            #// @since 4.7.0
            #// 
            #// @param bool $allow_anonymous Whether to allow anonymous comments to
            #// be created. Default `false`.
            #// @param WP_REST_Request $request Request used to generate the
            #// response.
            #//
            allow_anonymous = apply_filters("rest_allow_anonymous_comments", False, request)
            if (not allow_anonymous):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_login_required", __("Sorry, you must be logged in to comment."), Array({"status": 401})))
            # end if
        # end if
        #// Limit who can set comment `author`, `author_ip` or `status` to anything other than the default.
        if (php_isset(lambda : request["author"])) and get_current_user_id() != request["author"] and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_author", php_sprintf(__("Sorry, you are not allowed to edit '%s' for comments."), "author"), Array({"status": rest_authorization_required_code()})))
        # end if
        if (php_isset(lambda : request["author_ip"])) and (not current_user_can("moderate_comments")):
            if php_empty(lambda : PHP_SERVER["REMOTE_ADDR"]) or request["author_ip"] != PHP_SERVER["REMOTE_ADDR"]:
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_author_ip", php_sprintf(__("Sorry, you are not allowed to edit '%s' for comments."), "author_ip"), Array({"status": rest_authorization_required_code()})))
            # end if
        # end if
        if (php_isset(lambda : request["status"])) and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_status", php_sprintf(__("Sorry, you are not allowed to edit '%s' for comments."), "status"), Array({"status": rest_authorization_required_code()})))
        # end if
        if php_empty(lambda : request["post"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_post_id", __("Sorry, you are not allowed to create this comment without a post."), Array({"status": 403})))
        # end if
        post = get_post(php_int(request["post"]))
        if (not post):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_post_id", __("Sorry, you are not allowed to create this comment without a post."), Array({"status": 403})))
        # end if
        if "draft" == post.post_status:
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_draft_post", __("Sorry, you are not allowed to create a comment on this post."), Array({"status": 403})))
        # end if
        if "trash" == post.post_status:
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_trash_post", __("Sorry, you are not allowed to create a comment on this post."), Array({"status": 403})))
        # end if
        if (not self.check_read_post_permission(post, request)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_post", __("Sorry, you are not allowed to read the post for this comment."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not comments_open(post.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_closed", __("Sorry, comments are closed for this item."), Array({"status": 403})))
        # end if
        return True
    # end def create_item_permissions_check
    #// 
    #// Creates a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or error object on failure.
    #//
    def create_item(self, request=None):
        
        if (not php_empty(lambda : request["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_exists", __("Cannot create existing comment."), Array({"status": 400})))
        # end if
        #// Do not allow comments to be created with a non-default type.
        if (not php_empty(lambda : request["type"])) and "comment" != request["type"]:
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_comment_type", __("Cannot create a comment with that type."), Array({"status": 400})))
        # end if
        prepared_comment = self.prepare_item_for_database(request)
        if is_wp_error(prepared_comment):
            return prepared_comment
        # end if
        prepared_comment["comment_type"] = ""
        #// 
        #// Do not allow a comment to be created with missing or empty
        #// comment_content. See wp_handle_comment_submission().
        #//
        if php_empty(lambda : prepared_comment["comment_content"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_content_invalid", __("Invalid comment content."), Array({"status": 400})))
        # end if
        #// Setting remaining values before wp_insert_comment so we can use wp_allow_comment().
        if (not (php_isset(lambda : prepared_comment["comment_date_gmt"]))):
            prepared_comment["comment_date_gmt"] = current_time("mysql", True)
        # end if
        #// Set author data if the user's logged in.
        missing_author = php_empty(lambda : prepared_comment["user_id"]) and php_empty(lambda : prepared_comment["comment_author"]) and php_empty(lambda : prepared_comment["comment_author_email"]) and php_empty(lambda : prepared_comment["comment_author_url"])
        if is_user_logged_in() and missing_author:
            user = wp_get_current_user()
            prepared_comment["user_id"] = user.ID
            prepared_comment["comment_author"] = user.display_name
            prepared_comment["comment_author_email"] = user.user_email
            prepared_comment["comment_author_url"] = user.user_url
        # end if
        #// Honor the discussion setting that requires a name and email address of the comment author.
        if get_option("require_name_email"):
            if php_empty(lambda : prepared_comment["comment_author"]) or php_empty(lambda : prepared_comment["comment_author_email"]):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_author_data_required", __("Creating a comment requires valid author name and email values."), Array({"status": 400})))
            # end if
        # end if
        if (not (php_isset(lambda : prepared_comment["comment_author_email"]))):
            prepared_comment["comment_author_email"] = ""
        # end if
        if (not (php_isset(lambda : prepared_comment["comment_author_url"]))):
            prepared_comment["comment_author_url"] = ""
        # end if
        if (not (php_isset(lambda : prepared_comment["comment_agent"]))):
            prepared_comment["comment_agent"] = ""
        # end if
        check_comment_lengths = wp_check_comment_data_max_lengths(prepared_comment)
        if is_wp_error(check_comment_lengths):
            error_code = check_comment_lengths.get_error_code()
            return php_new_class("WP_Error", lambda : WP_Error(error_code, __("Comment field exceeds maximum length allowed."), Array({"status": 400})))
        # end if
        prepared_comment["comment_approved"] = wp_allow_comment(prepared_comment, True)
        if is_wp_error(prepared_comment["comment_approved"]):
            error_code = prepared_comment["comment_approved"].get_error_code()
            error_message = prepared_comment["comment_approved"].get_error_message()
            if "comment_duplicate" == error_code:
                return php_new_class("WP_Error", lambda : WP_Error(error_code, error_message, Array({"status": 409})))
            # end if
            if "comment_flood" == error_code:
                return php_new_class("WP_Error", lambda : WP_Error(error_code, error_message, Array({"status": 400})))
            # end if
            return prepared_comment["comment_approved"]
        # end if
        #// 
        #// Filters a comment before it is inserted via the REST API.
        #// 
        #// Allows modification of the comment right before it is inserted via wp_insert_comment().
        #// Returning a WP_Error value from the filter will shortcircuit insertion and allow
        #// skipping further processing.
        #// 
        #// @since 4.7.0
        #// @since 4.8.0 `$prepared_comment` can now be a WP_Error to shortcircuit insertion.
        #// 
        #// @param array|WP_Error  $prepared_comment The prepared comment data for wp_insert_comment().
        #// @param WP_REST_Request $request          Request used to insert the comment.
        #//
        prepared_comment = apply_filters("rest_pre_insert_comment", prepared_comment, request)
        if is_wp_error(prepared_comment):
            return prepared_comment
        # end if
        comment_id = wp_insert_comment(wp_filter_comment(wp_slash(prepared_comment)))
        if (not comment_id):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_failed_create", __("Creating comment failed."), Array({"status": 500})))
        # end if
        if (php_isset(lambda : request["status"])):
            self.handle_status_param(request["status"], comment_id)
        # end if
        comment = get_comment(comment_id)
        #// 
        #// Fires after a comment is created or updated via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Comment      $comment  Inserted or updated comment object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a comment, false
        #// when updating.
        #//
        do_action("rest_insert_comment", comment, request, True)
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], comment_id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        fields_update = self.update_additional_fields_for_object(comment, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        context = "edit" if current_user_can("moderate_comments") else "view"
        request.set_param("context", context)
        #// 
        #// Fires completely after a comment is created or updated via the REST API.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_Comment      $comment  Inserted or updated comment object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a comment, false
        #// when updating.
        #//
        do_action("rest_after_insert_comment", comment, request, True)
        response = self.prepare_item_for_response(comment, request)
        response = rest_ensure_response(response)
        response.set_status(201)
        response.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, comment_id)))
        return response
    # end def create_item
    #// 
    #// Checks if a given REST request has access to update a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, error object otherwise.
    #//
    def update_item_permissions_check(self, request=None):
        
        comment = self.get_comment(request["id"])
        if is_wp_error(comment):
            return comment
        # end if
        if (not self.check_edit_permission(comment)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit", __("Sorry, you are not allowed to edit this comment."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def update_item_permissions_check
    #// 
    #// Updates a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or error object on failure.
    #//
    def update_item(self, request=None):
        
        comment = self.get_comment(request["id"])
        if is_wp_error(comment):
            return comment
        # end if
        id = comment.comment_ID
        if (php_isset(lambda : request["type"])) and get_comment_type(id) != request["type"]:
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_type", __("Sorry, you are not allowed to change the comment type."), Array({"status": 404})))
        # end if
        prepared_args = self.prepare_item_for_database(request)
        if is_wp_error(prepared_args):
            return prepared_args
        # end if
        if (not php_empty(lambda : prepared_args["comment_post_ID"])):
            post = get_post(prepared_args["comment_post_ID"])
            if php_empty(lambda : post):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_post_id", __("Invalid post ID."), Array({"status": 403})))
            # end if
        # end if
        if php_empty(lambda : prepared_args) and (php_isset(lambda : request["status"])):
            #// Only the comment status is being changed.
            change = self.handle_status_param(request["status"], id)
            if (not change):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_failed_edit", __("Updating comment status failed."), Array({"status": 500})))
            # end if
        elif (not php_empty(lambda : prepared_args)):
            if is_wp_error(prepared_args):
                return prepared_args
            # end if
            if (php_isset(lambda : prepared_args["comment_content"])) and php_empty(lambda : prepared_args["comment_content"]):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_content_invalid", __("Invalid comment content."), Array({"status": 400})))
            # end if
            prepared_args["comment_ID"] = id
            check_comment_lengths = wp_check_comment_data_max_lengths(prepared_args)
            if is_wp_error(check_comment_lengths):
                error_code = check_comment_lengths.get_error_code()
                return php_new_class("WP_Error", lambda : WP_Error(error_code, __("Comment field exceeds maximum length allowed."), Array({"status": 400})))
            # end if
            updated = wp_update_comment(wp_slash(prepared_args))
            if False == updated:
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_failed_edit", __("Updating comment failed."), Array({"status": 500})))
            # end if
            if (php_isset(lambda : request["status"])):
                self.handle_status_param(request["status"], id)
            # end if
        # end if
        comment = get_comment(id)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-comments-controller.php
        do_action("rest_insert_comment", comment, request, False)
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        fields_update = self.update_additional_fields_for_object(comment, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-comments-controller.php
        do_action("rest_after_insert_comment", comment, request, False)
        response = self.prepare_item_for_response(comment, request)
        return rest_ensure_response(response)
    # end def update_item
    #// 
    #// Checks if a given request has access to delete a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, error object otherwise.
    #//
    def delete_item_permissions_check(self, request=None):
        
        comment = self.get_comment(request["id"])
        if is_wp_error(comment):
            return comment
        # end if
        if (not self.check_edit_permission(comment)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("Sorry, you are not allowed to delete this comment."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def delete_item_permissions_check
    #// 
    #// Deletes a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or error object on failure.
    #//
    def delete_item(self, request=None):
        
        comment = self.get_comment(request["id"])
        if is_wp_error(comment):
            return comment
        # end if
        force = php_bool(request["force"]) if (php_isset(lambda : request["force"])) else False
        #// 
        #// Filters whether a comment can be trashed.
        #// 
        #// Return false to disable Trash support for the post.
        #// 
        #// @since 4.7.0
        #// 
        #// @param bool    $supports_trash Whether the post type support trashing.
        #// @param WP_Post $comment        The comment object being considered for trashing support.
        #//
        supports_trash = apply_filters("rest_comment_trashable", EMPTY_TRASH_DAYS > 0, comment)
        request.set_param("context", "edit")
        if force:
            previous = self.prepare_item_for_response(comment, request)
            result = wp_delete_comment(comment.comment_ID, True)
            response = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
            response.set_data(Array({"deleted": True, "previous": previous.get_data()}))
        else:
            #// If this type doesn't support trashing, error out.
            if (not supports_trash):
                return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("The comment does not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
            # end if
            if "trash" == comment.comment_approved:
                return php_new_class("WP_Error", lambda : WP_Error("rest_already_trashed", __("The comment has already been trashed."), Array({"status": 410})))
            # end if
            result = wp_trash_comment(comment.comment_ID)
            comment = get_comment(comment.comment_ID)
            response = self.prepare_item_for_response(comment, request)
        # end if
        if (not result):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The comment cannot be deleted."), Array({"status": 500})))
        # end if
        #// 
        #// Fires after a comment is deleted via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Comment       $comment  The deleted comment data.
        #// @param WP_REST_Response $response The response returned from the API.
        #// @param WP_REST_Request  $request  The request sent to the API.
        #//
        do_action("rest_delete_comment", comment, response, request)
        return response
    # end def delete_item
    #// 
    #// Prepares a single comment output for response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Comment      $comment Comment object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, comment=None, request=None):
        
        fields = self.get_fields_for_response(request)
        data = Array()
        if php_in_array("id", fields, True):
            data["id"] = php_int(comment.comment_ID)
        # end if
        if php_in_array("post", fields, True):
            data["post"] = php_int(comment.comment_post_ID)
        # end if
        if php_in_array("parent", fields, True):
            data["parent"] = php_int(comment.comment_parent)
        # end if
        if php_in_array("author", fields, True):
            data["author"] = php_int(comment.user_id)
        # end if
        if php_in_array("author_name", fields, True):
            data["author_name"] = comment.comment_author
        # end if
        if php_in_array("author_email", fields, True):
            data["author_email"] = comment.comment_author_email
        # end if
        if php_in_array("author_url", fields, True):
            data["author_url"] = comment.comment_author_url
        # end if
        if php_in_array("author_ip", fields, True):
            data["author_ip"] = comment.comment_author_IP
        # end if
        if php_in_array("author_user_agent", fields, True):
            data["author_user_agent"] = comment.comment_agent
        # end if
        if php_in_array("date", fields, True):
            data["date"] = mysql_to_rfc3339(comment.comment_date)
        # end if
        if php_in_array("date_gmt", fields, True):
            data["date_gmt"] = mysql_to_rfc3339(comment.comment_date_gmt)
        # end if
        if php_in_array("content", fields, True):
            data["content"] = Array({"rendered": apply_filters("comment_text", comment.comment_content, comment), "raw": comment.comment_content})
        # end if
        if php_in_array("link", fields, True):
            data["link"] = get_comment_link(comment)
        # end if
        if php_in_array("status", fields, True):
            data["status"] = self.prepare_status_response(comment.comment_approved)
        # end if
        if php_in_array("type", fields, True):
            data["type"] = get_comment_type(comment.comment_ID)
        # end if
        if php_in_array("author_avatar_urls", fields, True):
            data["author_avatar_urls"] = rest_get_avatar_urls(comment)
        # end if
        if php_in_array("meta", fields, True):
            data["meta"] = self.meta.get_value(comment.comment_ID, request)
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        #// Wrap the data in a response object.
        response = rest_ensure_response(data)
        response.add_links(self.prepare_links(comment))
        #// 
        #// Filters a comment returned from the API.
        #// 
        #// Allows modification of the comment right before it is returned.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response  $response The response object.
        #// @param WP_Comment        $comment  The original comment object.
        #// @param WP_REST_Request   $request  Request used to generate the response.
        #//
        return apply_filters("rest_prepare_comment", response, comment, request)
    # end def prepare_item_for_response
    #// 
    #// Prepares links for the request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Comment $comment Comment object.
    #// @return array Links for the given comment.
    #//
    def prepare_links(self, comment=None):
        
        links = Array({"self": Array({"href": rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, comment.comment_ID))})}, {"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})})
        if 0 != php_int(comment.user_id):
            links["author"] = Array({"href": rest_url("wp/v2/users/" + comment.user_id), "embeddable": True})
        # end if
        if 0 != php_int(comment.comment_post_ID):
            post = get_post(comment.comment_post_ID)
            if (not php_empty(lambda : post.ID)):
                obj = get_post_type_object(post.post_type)
                base = obj.rest_base if (not php_empty(lambda : obj.rest_base)) else obj.name
                links["up"] = Array({"href": rest_url("wp/v2/" + base + "/" + comment.comment_post_ID), "embeddable": True, "post_type": post.post_type})
            # end if
        # end if
        if 0 != php_int(comment.comment_parent):
            links["in-reply-to"] = Array({"href": rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, comment.comment_parent)), "embeddable": True})
        # end if
        #// Only grab one comment to verify the comment has children.
        comment_children = comment.get_children(Array({"number": 1, "count": True}))
        if (not php_empty(lambda : comment_children)):
            args = Array({"parent": comment.comment_ID})
            rest_url = add_query_arg(args, rest_url(self.namespace + "/" + self.rest_base))
            links["children"] = Array({"href": rest_url})
        # end if
        return links
    # end def prepare_links
    #// 
    #// Prepends internal property prefix to query parameters to match our response fields.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $query_param Query parameter.
    #// @return string The normalized query parameter.
    #//
    def normalize_query_param(self, query_param=None):
        
        prefix = "comment_"
        for case in Switch(query_param):
            if case("id"):
                normalized = prefix + "ID"
                break
            # end if
            if case("post"):
                normalized = prefix + "post_ID"
                break
            # end if
            if case("parent"):
                normalized = prefix + "parent"
                break
            # end if
            if case("include"):
                normalized = "comment__in"
                break
            # end if
            if case():
                normalized = prefix + query_param
                break
            # end if
        # end for
        return normalized
    # end def normalize_query_param
    #// 
    #// Checks comment_approved to set comment status for single comment output.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string|int $comment_approved comment status.
    #// @return string Comment status.
    #//
    def prepare_status_response(self, comment_approved=None):
        
        for case in Switch(comment_approved):
            if case("hold"):
                pass
            # end if
            if case("0"):
                status = "hold"
                break
            # end if
            if case("approve"):
                pass
            # end if
            if case("1"):
                status = "approved"
                break
            # end if
            if case("spam"):
                pass
            # end if
            if case("trash"):
                pass
            # end if
            if case():
                status = comment_approved
                break
            # end if
        # end for
        return status
    # end def prepare_status_response
    #// 
    #// Prepares a single comment to be inserted into the database.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return array|WP_Error Prepared comment, otherwise WP_Error object.
    #//
    def prepare_item_for_database(self, request=None):
        
        prepared_comment = Array()
        #// 
        #// Allow the comment_content to be set via the 'content' or
        #// the 'content.raw' properties of the Request object.
        #//
        if (php_isset(lambda : request["content"])) and php_is_string(request["content"]):
            prepared_comment["comment_content"] = request["content"]
        elif (php_isset(lambda : request["content"]["raw"])) and php_is_string(request["content"]["raw"]):
            prepared_comment["comment_content"] = request["content"]["raw"]
        # end if
        if (php_isset(lambda : request["post"])):
            prepared_comment["comment_post_ID"] = php_int(request["post"])
        # end if
        if (php_isset(lambda : request["parent"])):
            prepared_comment["comment_parent"] = request["parent"]
        # end if
        if (php_isset(lambda : request["author"])):
            user = php_new_class("WP_User", lambda : WP_User(request["author"]))
            if user.exists():
                prepared_comment["user_id"] = user.ID
                prepared_comment["comment_author"] = user.display_name
                prepared_comment["comment_author_email"] = user.user_email
                prepared_comment["comment_author_url"] = user.user_url
            else:
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_author_invalid", __("Invalid comment author ID."), Array({"status": 400})))
            # end if
        # end if
        if (php_isset(lambda : request["author_name"])):
            prepared_comment["comment_author"] = request["author_name"]
        # end if
        if (php_isset(lambda : request["author_email"])):
            prepared_comment["comment_author_email"] = request["author_email"]
        # end if
        if (php_isset(lambda : request["author_url"])):
            prepared_comment["comment_author_url"] = request["author_url"]
        # end if
        if (php_isset(lambda : request["author_ip"])) and current_user_can("moderate_comments"):
            prepared_comment["comment_author_IP"] = request["author_ip"]
        elif (not php_empty(lambda : PHP_SERVER["REMOTE_ADDR"])) and rest_is_ip_address(PHP_SERVER["REMOTE_ADDR"]):
            prepared_comment["comment_author_IP"] = PHP_SERVER["REMOTE_ADDR"]
        else:
            prepared_comment["comment_author_IP"] = "127.0.0.1"
        # end if
        if (not php_empty(lambda : request["author_user_agent"])):
            prepared_comment["comment_agent"] = request["author_user_agent"]
        elif request.get_header("user_agent"):
            prepared_comment["comment_agent"] = request.get_header("user_agent")
        # end if
        if (not php_empty(lambda : request["date"])):
            date_data = rest_get_date_with_gmt(request["date"])
            if (not php_empty(lambda : date_data)):
                prepared_comment["comment_date"], prepared_comment["comment_date_gmt"] = date_data
            # end if
        elif (not php_empty(lambda : request["date_gmt"])):
            date_data = rest_get_date_with_gmt(request["date_gmt"], True)
            if (not php_empty(lambda : date_data)):
                prepared_comment["comment_date"], prepared_comment["comment_date_gmt"] = date_data
            # end if
        # end if
        #// 
        #// Filters a comment after it is prepared for the database.
        #// 
        #// Allows modification of the comment right after it is prepared for the database.
        #// 
        #// @since 4.7.0
        #// 
        #// @param array           $prepared_comment The prepared comment data for `wp_insert_comment`.
        #// @param WP_REST_Request $request          The current request.
        #//
        return apply_filters("rest_preprocess_comment", prepared_comment, request)
    # end def prepare_item_for_database
    #// 
    #// Retrieves the comment's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array
    #//
    def get_item_schema(self):
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "comment", "type": "object", "properties": Array({"id": Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "edit", "embed"), "readonly": True})}, {"author": Array({"description": __("The ID of the user object, if author was a user."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"author_email": Array({"description": __("Email address for the object author."), "type": "string", "format": "email", "context": Array("edit"), "arg_options": Array({"sanitize_callback": Array(self, "check_comment_author_email"), "validate_callback": None})})}, {"author_ip": Array({"description": __("IP address for the object author."), "type": "string", "format": "ip", "context": Array("edit")})}, {"author_name": Array({"description": __("Display name for the object author."), "type": "string", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"author_url": Array({"description": __("URL for the object author."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed")})}, {"author_user_agent": Array({"description": __("User agent for the object author."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"content": Array({"description": __("The content for the object."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Content for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML content for the object, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})}, {"date": Array({"description": __("The date the object was published, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit", "embed")})}, {"date_gmt": Array({"description": __("The date the object was published, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"link": Array({"description": __("URL to the object."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed"), "readonly": True})}, {"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer", "context": Array("view", "edit", "embed"), "default": 0})}, {"post": Array({"description": __("The ID of the associated post object."), "type": "integer", "context": Array("view", "edit"), "default": 0})}, {"status": Array({"description": __("State of the object."), "type": "string", "context": Array("view", "edit"), "arg_options": Array({"sanitize_callback": "sanitize_key"})})}, {"type": Array({"description": __("Type of Comment for the object."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
        if get_option("show_avatars"):
            avatar_properties = Array()
            avatar_sizes = rest_get_avatar_sizes()
            for size in avatar_sizes:
                avatar_properties[size] = Array({"description": php_sprintf(__("Avatar URL with image size of %d pixels."), size), "type": "string", "format": "uri", "context": Array("embed", "view", "edit")})
            # end for
            schema["properties"]["author_avatar_urls"] = Array({"description": __("Avatar URLs for the object author."), "type": "object", "context": Array("view", "edit", "embed"), "readonly": True, "properties": avatar_properties})
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
    #// @return array Comments collection parameters.
    #//
    def get_collection_params(self):
        
        query_params = super().get_collection_params()
        query_params["context"]["default"] = "view"
        query_params["after"] = Array({"description": __("Limit response to comments published after a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        query_params["author"] = Array({"description": __("Limit result set to comments assigned to specific user IDs. Requires authorization."), "type": "array", "items": Array({"type": "integer"})})
        query_params["author_exclude"] = Array({"description": __("Ensure result set excludes comments assigned to specific user IDs. Requires authorization."), "type": "array", "items": Array({"type": "integer"})})
        query_params["author_email"] = Array({"default": None, "description": __("Limit result set to that from a specific author email. Requires authorization."), "format": "email", "type": "string"})
        query_params["before"] = Array({"description": __("Limit response to comments published before a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        query_params["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "desc", "enum": Array("asc", "desc")})
        query_params["orderby"] = Array({"description": __("Sort collection by object attribute."), "type": "string", "default": "date_gmt", "enum": Array("date", "date_gmt", "id", "include", "post", "parent", "type")})
        query_params["parent"] = Array({"default": Array(), "description": __("Limit result set to comments of specific parent IDs."), "type": "array", "items": Array({"type": "integer"})})
        query_params["parent_exclude"] = Array({"default": Array(), "description": __("Ensure result set excludes specific parent IDs."), "type": "array", "items": Array({"type": "integer"})})
        query_params["post"] = Array({"default": Array(), "description": __("Limit result set to comments assigned to specific post IDs."), "type": "array", "items": Array({"type": "integer"})})
        query_params["status"] = Array({"default": "approve", "description": __("Limit result set to comments assigned a specific status. Requires authorization."), "sanitize_callback": "sanitize_key", "type": "string", "validate_callback": "rest_validate_request_arg"})
        query_params["type"] = Array({"default": "comment", "description": __("Limit result set to comments assigned a specific type. Requires authorization."), "sanitize_callback": "sanitize_key", "type": "string", "validate_callback": "rest_validate_request_arg"})
        query_params["password"] = Array({"description": __("The password for the post if it is password protected."), "type": "string"})
        #// 
        #// Filter collection parameters for the comments controller.
        #// 
        #// This filter registers the collection parameter, but does not map the
        #// collection parameter to an internal WP_Comment_Query parameter. Use the
        #// `rest_comment_query` filter to set WP_Comment_Query parameters.
        #// 
        #// @since 4.7.0
        #// 
        #// @param array $query_params JSON Schema-formatted collection parameters.
        #//
        return apply_filters("rest_comment_collection_params", query_params)
    # end def get_collection_params
    #// 
    #// Sets the comment_status of a given comment object when creating or updating a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string|int $new_status New comment status.
    #// @param int        $comment_id Comment ID.
    #// @return bool Whether the status was changed.
    #//
    def handle_status_param(self, new_status=None, comment_id=None):
        
        old_status = wp_get_comment_status(comment_id)
        if new_status == old_status:
            return False
        # end if
        for case in Switch(new_status):
            if case("approved"):
                pass
            # end if
            if case("approve"):
                pass
            # end if
            if case("1"):
                changed = wp_set_comment_status(comment_id, "approve")
                break
            # end if
            if case("hold"):
                pass
            # end if
            if case("0"):
                changed = wp_set_comment_status(comment_id, "hold")
                break
            # end if
            if case("spam"):
                changed = wp_spam_comment(comment_id)
                break
            # end if
            if case("unspam"):
                changed = wp_unspam_comment(comment_id)
                break
            # end if
            if case("trash"):
                changed = wp_trash_comment(comment_id)
                break
            # end if
            if case("untrash"):
                changed = wp_untrash_comment(comment_id)
                break
            # end if
            if case():
                changed = False
                break
            # end if
        # end for
        return changed
    # end def handle_status_param
    #// 
    #// Checks if the post can be read.
    #// 
    #// Correctly handles posts with the inherit status.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post         $post    Post object.
    #// @param WP_REST_Request $request Request data to check.
    #// @return bool Whether post can be read.
    #//
    def check_read_post_permission(self, post=None, request=None):
        
        post_type = get_post_type_object(post.post_type)
        #// Return false if custom post type doesn't exist
        if (not post_type):
            return False
        # end if
        posts_controller = post_type.get_rest_controller()
        #// Ensure the posts controller is specifically a WP_REST_Posts_Controller instance
        #// before using methods specific to that controller.
        if (not type(posts_controller).__name__ == "WP_REST_Posts_Controller"):
            posts_controller = php_new_class("WP_REST_Posts_Controller", lambda : WP_REST_Posts_Controller(post.post_type))
        # end if
        has_password_filter = False
        #// Only check password if a specific post was queried for or a single comment
        requested_post = (not php_empty(lambda : request["post"])) and (not php_is_array(request["post"])) or 1 == php_count(request["post"])
        requested_comment = (not php_empty(lambda : request["id"]))
        if requested_post or requested_comment and posts_controller.can_access_password_content(post, request):
            add_filter("post_password_required", "__return_false")
            has_password_filter = True
        # end if
        if post_password_required(post):
            result = current_user_can(post_type.cap.edit_post, post.ID)
        else:
            result = posts_controller.check_read_permission(post)
        # end if
        if has_password_filter:
            remove_filter("post_password_required", "__return_false")
        # end if
        return result
    # end def check_read_post_permission
    #// 
    #// Checks if the comment can be read.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Comment      $comment Comment object.
    #// @param WP_REST_Request $request Request data to check.
    #// @return bool Whether the comment can be read.
    #//
    def check_read_permission(self, comment=None, request=None):
        
        if (not php_empty(lambda : comment.comment_post_ID)):
            post = get_post(comment.comment_post_ID)
            if post:
                if self.check_read_post_permission(post, request) and 1 == php_int(comment.comment_approved):
                    return True
                # end if
            # end if
        # end if
        if 0 == get_current_user_id():
            return False
        # end if
        if php_empty(lambda : comment.comment_post_ID) and (not current_user_can("moderate_comments")):
            return False
        # end if
        if (not php_empty(lambda : comment.user_id)) and get_current_user_id() == php_int(comment.user_id):
            return True
        # end if
        return current_user_can("edit_comment", comment.comment_ID)
    # end def check_read_permission
    #// 
    #// Checks if a comment can be edited or deleted.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Comment $comment Comment object.
    #// @return bool Whether the comment can be edited or deleted.
    #//
    def check_edit_permission(self, comment=None):
        
        if 0 == php_int(get_current_user_id()):
            return False
        # end if
        if current_user_can("moderate_comments"):
            return True
        # end if
        return current_user_can("edit_comment", comment.comment_ID)
    # end def check_edit_permission
    #// 
    #// Checks a comment author email for validity.
    #// 
    #// Accepts either a valid email address or empty string as a valid comment
    #// author email address. Setting the comment author email to an empty
    #// string is allowed when a comment is being updated.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string          $value   Author email value submitted.
    #// @param WP_REST_Request $request Full details about the request.
    #// @param string          $param   The parameter name.
    #// @return string|WP_Error The sanitized email address, if valid,
    #// otherwise an error.
    #//
    def check_comment_author_email(self, value=None, request=None, param=None):
        
        email = php_str(value)
        if php_empty(lambda : email):
            return email
        # end if
        check_email = rest_validate_request_arg(email, request, param)
        if is_wp_error(check_email):
            return check_email
        # end if
        return email
    # end def check_comment_author_email
# end class WP_REST_Comments_Controller
