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
    #// 
    #// Instance of a comment meta fields object.
    #// 
    #// @since 4.7.0
    #// @var WP_REST_Comment_Meta_Fields
    #//
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
    def get_items_permissions_check(self, request_=None):
        
        
        if (not php_empty(lambda : request_["post"])):
            for post_id_ in request_["post"]:
                post_ = get_post(post_id_)
                if (not php_empty(lambda : post_id_)) and post_ and (not self.check_read_post_permission(post_, request_)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_post", __("Sorry, you are not allowed to read the post for this comment."), Array({"status": rest_authorization_required_code()})))
                elif 0 == post_id_ and (not current_user_can("moderate_comments")):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read", __("Sorry, you are not allowed to read comments without a post."), Array({"status": rest_authorization_required_code()})))
                # end if
            # end for
        # end if
        if (not php_empty(lambda : request_["context"])) and "edit" == request_["context"] and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit comments."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not current_user_can("edit_posts")):
            protected_params_ = Array("author", "author_exclude", "author_email", "type", "status")
            forbidden_params_ = Array()
            for param_ in protected_params_:
                if "status" == param_:
                    if "approve" != request_[param_]:
                        forbidden_params_[-1] = param_
                    # end if
                elif "type" == param_:
                    if "comment" != request_[param_]:
                        forbidden_params_[-1] = param_
                    # end if
                elif (not php_empty(lambda : request_[param_])):
                    forbidden_params_[-1] = param_
                # end if
            # end for
            if (not php_empty(lambda : forbidden_params_)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_param", php_sprintf(__("Query parameter not permitted: %s"), php_implode(", ", forbidden_params_)), Array({"status": rest_authorization_required_code()})))
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
    def get_items(self, request_=None):
        
        
        #// Retrieve the list of registered collection query parameters.
        registered_ = self.get_collection_params()
        #// 
        #// This array defines mappings between public API query parameters whose
        #// values are accepted as-passed, and their internal WP_Query parameter
        #// name equivalents (some are the same). Only values which are also
        #// present in $registered will be set.
        #//
        parameter_mappings_ = Array({"author": "author__in", "author_email": "author_email", "author_exclude": "author__not_in", "exclude": "comment__not_in", "include": "comment__in", "offset": "offset", "order": "order", "parent": "parent__in", "parent_exclude": "parent__not_in", "per_page": "number", "post": "post__in", "search": "search", "status": "status", "type": "type"})
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
        #// Ensure certain parameter values default to empty strings.
        for param_ in Array("author_email", "search"):
            if (not (php_isset(lambda : prepared_args_[param_]))):
                prepared_args_[param_] = ""
            # end if
        # end for
        if (php_isset(lambda : registered_["orderby"])):
            prepared_args_["orderby"] = self.normalize_query_param(request_["orderby"])
        # end if
        prepared_args_["no_found_rows"] = False
        prepared_args_["date_query"] = Array()
        #// Set before into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered_["before"]) and php_isset(lambda : request_["before"])):
            prepared_args_["date_query"][0]["before"] = request_["before"]
        # end if
        #// Set after into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered_["after"]) and php_isset(lambda : request_["after"])):
            prepared_args_["date_query"][0]["after"] = request_["after"]
        # end if
        if (php_isset(lambda : registered_["page"])) and php_empty(lambda : request_["offset"]):
            prepared_args_["offset"] = prepared_args_["number"] * absint(request_["page"]) - 1
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
        prepared_args_ = apply_filters("rest_comment_query", prepared_args_, request_)
        query_ = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
        query_result_ = query_.query(prepared_args_)
        comments_ = Array()
        for comment_ in query_result_:
            if (not self.check_read_permission(comment_, request_)):
                continue
            # end if
            data_ = self.prepare_item_for_response(comment_, request_)
            comments_[-1] = self.prepare_response_for_collection(data_)
        # end for
        total_comments_ = php_int(query_.found_comments)
        max_pages_ = php_int(query_.max_num_pages)
        if total_comments_ < 1:
            prepared_args_["number"] = None
            prepared_args_["offset"] = None
            query_ = php_new_class("WP_Comment_Query", lambda : WP_Comment_Query())
            prepared_args_["count"] = True
            total_comments_ = query_.query(prepared_args_)
            max_pages_ = ceil(total_comments_ / request_["per_page"])
        # end if
        response_ = rest_ensure_response(comments_)
        response_.header("X-WP-Total", total_comments_)
        response_.header("X-WP-TotalPages", max_pages_)
        base_ = add_query_arg(urlencode_deep(request_.get_query_params()), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
        if request_["page"] > 1:
            prev_page_ = request_["page"] - 1
            if prev_page_ > max_pages_:
                prev_page_ = max_pages_
            # end if
            prev_link_ = add_query_arg("page", prev_page_, base_)
            response_.link_header("prev", prev_link_)
        # end if
        if max_pages_ > request_["page"]:
            next_page_ = request_["page"] + 1
            next_link_ = add_query_arg("page", next_page_, base_)
            response_.link_header("next", next_link_)
        # end if
        return response_
    # end def get_items
    #// 
    #// Get the comment, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_Comment|WP_Error Comment object if ID is valid, WP_Error otherwise.
    #//
    def get_comment(self, id_=None):
        
        
        error_ = php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_id", __("Invalid comment ID."), Array({"status": 404})))
        if php_int(id_) <= 0:
            return error_
        # end if
        id_ = php_int(id_)
        comment_ = get_comment(id_)
        if php_empty(lambda : comment_):
            return error_
        # end if
        if (not php_empty(lambda : comment_.comment_post_ID)):
            post_ = get_post(php_int(comment_.comment_post_ID))
            if php_empty(lambda : post_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post ID."), Array({"status": 404})))
            # end if
        # end if
        return comment_
    # end def get_comment
    #// 
    #// Checks if a given request has access to read the comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, error object otherwise.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        comment_ = self.get_comment(request_["id"])
        if is_wp_error(comment_):
            return comment_
        # end if
        if (not php_empty(lambda : request_["context"])) and "edit" == request_["context"] and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit comments."), Array({"status": rest_authorization_required_code()})))
        # end if
        post_ = get_post(comment_.comment_post_ID)
        if (not self.check_read_permission(comment_, request_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read", __("Sorry, you are not allowed to read this comment."), Array({"status": rest_authorization_required_code()})))
        # end if
        if post_ and (not self.check_read_post_permission(post_, request_)):
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
    def get_item(self, request_=None):
        
        
        comment_ = self.get_comment(request_["id"])
        if is_wp_error(comment_):
            return comment_
        # end if
        data_ = self.prepare_item_for_response(comment_, request_)
        response_ = rest_ensure_response(data_)
        return response_
    # end def get_item
    #// 
    #// Checks if a given request has access to create a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create items, error object otherwise.
    #//
    def create_item_permissions_check(self, request_=None):
        
        
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
            allow_anonymous_ = apply_filters("rest_allow_anonymous_comments", False, request_)
            if (not allow_anonymous_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_login_required", __("Sorry, you must be logged in to comment."), Array({"status": 401})))
            # end if
        # end if
        #// Limit who can set comment `author`, `author_ip` or `status` to anything other than the default.
        if (php_isset(lambda : request_["author"])) and get_current_user_id() != request_["author"] and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_author", php_sprintf(__("Sorry, you are not allowed to edit '%s' for comments."), "author"), Array({"status": rest_authorization_required_code()})))
        # end if
        if (php_isset(lambda : request_["author_ip"])) and (not current_user_can("moderate_comments")):
            if php_empty(lambda : PHP_SERVER["REMOTE_ADDR"]) or request_["author_ip"] != PHP_SERVER["REMOTE_ADDR"]:
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_author_ip", php_sprintf(__("Sorry, you are not allowed to edit '%s' for comments."), "author_ip"), Array({"status": rest_authorization_required_code()})))
            # end if
        # end if
        if (php_isset(lambda : request_["status"])) and (not current_user_can("moderate_comments")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_status", php_sprintf(__("Sorry, you are not allowed to edit '%s' for comments."), "status"), Array({"status": rest_authorization_required_code()})))
        # end if
        if php_empty(lambda : request_["post"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_post_id", __("Sorry, you are not allowed to create this comment without a post."), Array({"status": 403})))
        # end if
        post_ = get_post(php_int(request_["post"]))
        if (not post_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_post_id", __("Sorry, you are not allowed to create this comment without a post."), Array({"status": 403})))
        # end if
        if "draft" == post_.post_status:
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_draft_post", __("Sorry, you are not allowed to create a comment on this post."), Array({"status": 403})))
        # end if
        if "trash" == post_.post_status:
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_trash_post", __("Sorry, you are not allowed to create a comment on this post."), Array({"status": 403})))
        # end if
        if (not self.check_read_post_permission(post_, request_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read_post", __("Sorry, you are not allowed to read the post for this comment."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not comments_open(post_.ID)):
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
    def create_item(self, request_=None):
        
        
        if (not php_empty(lambda : request_["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_exists", __("Cannot create existing comment."), Array({"status": 400})))
        # end if
        #// Do not allow comments to be created with a non-default type.
        if (not php_empty(lambda : request_["type"])) and "comment" != request_["type"]:
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_comment_type", __("Cannot create a comment with that type."), Array({"status": 400})))
        # end if
        prepared_comment_ = self.prepare_item_for_database(request_)
        if is_wp_error(prepared_comment_):
            return prepared_comment_
        # end if
        prepared_comment_["comment_type"] = ""
        #// 
        #// Do not allow a comment to be created with missing or empty
        #// comment_content. See wp_handle_comment_submission().
        #//
        if php_empty(lambda : prepared_comment_["comment_content"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_content_invalid", __("Invalid comment content."), Array({"status": 400})))
        # end if
        #// Setting remaining values before wp_insert_comment so we can use wp_allow_comment().
        if (not (php_isset(lambda : prepared_comment_["comment_date_gmt"]))):
            prepared_comment_["comment_date_gmt"] = current_time("mysql", True)
        # end if
        #// Set author data if the user's logged in.
        missing_author_ = php_empty(lambda : prepared_comment_["user_id"]) and php_empty(lambda : prepared_comment_["comment_author"]) and php_empty(lambda : prepared_comment_["comment_author_email"]) and php_empty(lambda : prepared_comment_["comment_author_url"])
        if is_user_logged_in() and missing_author_:
            user_ = wp_get_current_user()
            prepared_comment_["user_id"] = user_.ID
            prepared_comment_["comment_author"] = user_.display_name
            prepared_comment_["comment_author_email"] = user_.user_email
            prepared_comment_["comment_author_url"] = user_.user_url
        # end if
        #// Honor the discussion setting that requires a name and email address of the comment author.
        if get_option("require_name_email"):
            if php_empty(lambda : prepared_comment_["comment_author"]) or php_empty(lambda : prepared_comment_["comment_author_email"]):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_author_data_required", __("Creating a comment requires valid author name and email values."), Array({"status": 400})))
            # end if
        # end if
        if (not (php_isset(lambda : prepared_comment_["comment_author_email"]))):
            prepared_comment_["comment_author_email"] = ""
        # end if
        if (not (php_isset(lambda : prepared_comment_["comment_author_url"]))):
            prepared_comment_["comment_author_url"] = ""
        # end if
        if (not (php_isset(lambda : prepared_comment_["comment_agent"]))):
            prepared_comment_["comment_agent"] = ""
        # end if
        check_comment_lengths_ = wp_check_comment_data_max_lengths(prepared_comment_)
        if is_wp_error(check_comment_lengths_):
            error_code_ = check_comment_lengths_.get_error_code()
            return php_new_class("WP_Error", lambda : WP_Error(error_code_, __("Comment field exceeds maximum length allowed."), Array({"status": 400})))
        # end if
        prepared_comment_["comment_approved"] = wp_allow_comment(prepared_comment_, True)
        if is_wp_error(prepared_comment_["comment_approved"]):
            error_code_ = prepared_comment_["comment_approved"].get_error_code()
            error_message_ = prepared_comment_["comment_approved"].get_error_message()
            if "comment_duplicate" == error_code_:
                return php_new_class("WP_Error", lambda : WP_Error(error_code_, error_message_, Array({"status": 409})))
            # end if
            if "comment_flood" == error_code_:
                return php_new_class("WP_Error", lambda : WP_Error(error_code_, error_message_, Array({"status": 400})))
            # end if
            return prepared_comment_["comment_approved"]
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
        prepared_comment_ = apply_filters("rest_pre_insert_comment", prepared_comment_, request_)
        if is_wp_error(prepared_comment_):
            return prepared_comment_
        # end if
        comment_id_ = wp_insert_comment(wp_filter_comment(wp_slash(prepared_comment_)))
        if (not comment_id_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_failed_create", __("Creating comment failed."), Array({"status": 500})))
        # end if
        if (php_isset(lambda : request_["status"])):
            self.handle_status_param(request_["status"], comment_id_)
        # end if
        comment_ = get_comment(comment_id_)
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
        do_action("rest_insert_comment", comment_, request_, True)
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], comment_id_)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        fields_update_ = self.update_additional_fields_for_object(comment_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        context_ = "edit" if current_user_can("moderate_comments") else "view"
        request_.set_param("context", context_)
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
        do_action("rest_after_insert_comment", comment_, request_, True)
        response_ = self.prepare_item_for_response(comment_, request_)
        response_ = rest_ensure_response(response_)
        response_.set_status(201)
        response_.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, comment_id_)))
        return response_
    # end def create_item
    #// 
    #// Checks if a given REST request has access to update a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, error object otherwise.
    #//
    def update_item_permissions_check(self, request_=None):
        
        
        comment_ = self.get_comment(request_["id"])
        if is_wp_error(comment_):
            return comment_
        # end if
        if (not self.check_edit_permission(comment_)):
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
    def update_item(self, request_=None):
        
        
        comment_ = self.get_comment(request_["id"])
        if is_wp_error(comment_):
            return comment_
        # end if
        id_ = comment_.comment_ID
        if (php_isset(lambda : request_["type"])) and get_comment_type(id_) != request_["type"]:
            return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_type", __("Sorry, you are not allowed to change the comment type."), Array({"status": 404})))
        # end if
        prepared_args_ = self.prepare_item_for_database(request_)
        if is_wp_error(prepared_args_):
            return prepared_args_
        # end if
        if (not php_empty(lambda : prepared_args_["comment_post_ID"])):
            post_ = get_post(prepared_args_["comment_post_ID"])
            if php_empty(lambda : post_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_invalid_post_id", __("Invalid post ID."), Array({"status": 403})))
            # end if
        # end if
        if php_empty(lambda : prepared_args_) and (php_isset(lambda : request_["status"])):
            #// Only the comment status is being changed.
            change_ = self.handle_status_param(request_["status"], id_)
            if (not change_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_failed_edit", __("Updating comment status failed."), Array({"status": 500})))
            # end if
        elif (not php_empty(lambda : prepared_args_)):
            if is_wp_error(prepared_args_):
                return prepared_args_
            # end if
            if (php_isset(lambda : prepared_args_["comment_content"])) and php_empty(lambda : prepared_args_["comment_content"]):
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_content_invalid", __("Invalid comment content."), Array({"status": 400})))
            # end if
            prepared_args_["comment_ID"] = id_
            check_comment_lengths_ = wp_check_comment_data_max_lengths(prepared_args_)
            if is_wp_error(check_comment_lengths_):
                error_code_ = check_comment_lengths_.get_error_code()
                return php_new_class("WP_Error", lambda : WP_Error(error_code_, __("Comment field exceeds maximum length allowed."), Array({"status": 400})))
            # end if
            updated_ = wp_update_comment(wp_slash(prepared_args_))
            if False == updated_:
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_failed_edit", __("Updating comment failed."), Array({"status": 500})))
            # end if
            if (php_isset(lambda : request_["status"])):
                self.handle_status_param(request_["status"], id_)
            # end if
        # end if
        comment_ = get_comment(id_)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-comments-controller.php
        do_action("rest_insert_comment", comment_, request_, False)
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], id_)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        fields_update_ = self.update_additional_fields_for_object(comment_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-comments-controller.php
        do_action("rest_after_insert_comment", comment_, request_, False)
        response_ = self.prepare_item_for_response(comment_, request_)
        return rest_ensure_response(response_)
    # end def update_item
    #// 
    #// Checks if a given request has access to delete a comment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, error object otherwise.
    #//
    def delete_item_permissions_check(self, request_=None):
        
        
        comment_ = self.get_comment(request_["id"])
        if is_wp_error(comment_):
            return comment_
        # end if
        if (not self.check_edit_permission(comment_)):
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
    def delete_item(self, request_=None):
        
        
        comment_ = self.get_comment(request_["id"])
        if is_wp_error(comment_):
            return comment_
        # end if
        force_ = php_bool(request_["force"]) if (php_isset(lambda : request_["force"])) else False
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
        supports_trash_ = apply_filters("rest_comment_trashable", EMPTY_TRASH_DAYS > 0, comment_)
        request_.set_param("context", "edit")
        if force_:
            previous_ = self.prepare_item_for_response(comment_, request_)
            result_ = wp_delete_comment(comment_.comment_ID, True)
            response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
            response_.set_data(Array({"deleted": True, "previous": previous_.get_data()}))
        else:
            #// If this type doesn't support trashing, error out.
            if (not supports_trash_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("The comment does not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
            # end if
            if "trash" == comment_.comment_approved:
                return php_new_class("WP_Error", lambda : WP_Error("rest_already_trashed", __("The comment has already been trashed."), Array({"status": 410})))
            # end if
            result_ = wp_trash_comment(comment_.comment_ID)
            comment_ = get_comment(comment_.comment_ID)
            response_ = self.prepare_item_for_response(comment_, request_)
        # end if
        if (not result_):
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
        do_action("rest_delete_comment", comment_, response_, request_)
        return response_
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
    def prepare_item_for_response(self, comment_=None, request_=None):
        
        
        fields_ = self.get_fields_for_response(request_)
        data_ = Array()
        if php_in_array("id", fields_, True):
            data_["id"] = php_int(comment_.comment_ID)
        # end if
        if php_in_array("post", fields_, True):
            data_["post"] = php_int(comment_.comment_post_ID)
        # end if
        if php_in_array("parent", fields_, True):
            data_["parent"] = php_int(comment_.comment_parent)
        # end if
        if php_in_array("author", fields_, True):
            data_["author"] = php_int(comment_.user_id)
        # end if
        if php_in_array("author_name", fields_, True):
            data_["author_name"] = comment_.comment_author
        # end if
        if php_in_array("author_email", fields_, True):
            data_["author_email"] = comment_.comment_author_email
        # end if
        if php_in_array("author_url", fields_, True):
            data_["author_url"] = comment_.comment_author_url
        # end if
        if php_in_array("author_ip", fields_, True):
            data_["author_ip"] = comment_.comment_author_IP
        # end if
        if php_in_array("author_user_agent", fields_, True):
            data_["author_user_agent"] = comment_.comment_agent
        # end if
        if php_in_array("date", fields_, True):
            data_["date"] = mysql_to_rfc3339(comment_.comment_date)
        # end if
        if php_in_array("date_gmt", fields_, True):
            data_["date_gmt"] = mysql_to_rfc3339(comment_.comment_date_gmt)
        # end if
        if php_in_array("content", fields_, True):
            data_["content"] = Array({"rendered": apply_filters("comment_text", comment_.comment_content, comment_), "raw": comment_.comment_content})
        # end if
        if php_in_array("link", fields_, True):
            data_["link"] = get_comment_link(comment_)
        # end if
        if php_in_array("status", fields_, True):
            data_["status"] = self.prepare_status_response(comment_.comment_approved)
        # end if
        if php_in_array("type", fields_, True):
            data_["type"] = get_comment_type(comment_.comment_ID)
        # end if
        if php_in_array("author_avatar_urls", fields_, True):
            data_["author_avatar_urls"] = rest_get_avatar_urls(comment_)
        # end if
        if php_in_array("meta", fields_, True):
            data_["meta"] = self.meta.get_value(comment_.comment_ID, request_)
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        #// Wrap the data in a response object.
        response_ = rest_ensure_response(data_)
        response_.add_links(self.prepare_links(comment_))
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
        return apply_filters("rest_prepare_comment", response_, comment_, request_)
    # end def prepare_item_for_response
    #// 
    #// Prepares links for the request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Comment $comment Comment object.
    #// @return array Links for the given comment.
    #//
    def prepare_links(self, comment_=None):
        
        
        links_ = Array({"self": Array({"href": rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, comment_.comment_ID))})}, {"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})})
        if 0 != php_int(comment_.user_id):
            links_["author"] = Array({"href": rest_url("wp/v2/users/" + comment_.user_id), "embeddable": True})
        # end if
        if 0 != php_int(comment_.comment_post_ID):
            post_ = get_post(comment_.comment_post_ID)
            if (not php_empty(lambda : post_.ID)):
                obj_ = get_post_type_object(post_.post_type)
                base_ = obj_.rest_base if (not php_empty(lambda : obj_.rest_base)) else obj_.name
                links_["up"] = Array({"href": rest_url("wp/v2/" + base_ + "/" + comment_.comment_post_ID), "embeddable": True, "post_type": post_.post_type})
            # end if
        # end if
        if 0 != php_int(comment_.comment_parent):
            links_["in-reply-to"] = Array({"href": rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, comment_.comment_parent)), "embeddable": True})
        # end if
        #// Only grab one comment to verify the comment has children.
        comment_children_ = comment_.get_children(Array({"number": 1, "count": True}))
        if (not php_empty(lambda : comment_children_)):
            args_ = Array({"parent": comment_.comment_ID})
            rest_url_ = add_query_arg(args_, rest_url(self.namespace + "/" + self.rest_base))
            links_["children"] = Array({"href": rest_url_})
        # end if
        return links_
    # end def prepare_links
    #// 
    #// Prepends internal property prefix to query parameters to match our response fields.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $query_param Query parameter.
    #// @return string The normalized query parameter.
    #//
    def normalize_query_param(self, query_param_=None):
        
        
        prefix_ = "comment_"
        for case in Switch(query_param_):
            if case("id"):
                normalized_ = prefix_ + "ID"
                break
            # end if
            if case("post"):
                normalized_ = prefix_ + "post_ID"
                break
            # end if
            if case("parent"):
                normalized_ = prefix_ + "parent"
                break
            # end if
            if case("include"):
                normalized_ = "comment__in"
                break
            # end if
            if case():
                normalized_ = prefix_ + query_param_
                break
            # end if
        # end for
        return normalized_
    # end def normalize_query_param
    #// 
    #// Checks comment_approved to set comment status for single comment output.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string|int $comment_approved comment status.
    #// @return string Comment status.
    #//
    def prepare_status_response(self, comment_approved_=None):
        
        
        for case in Switch(comment_approved_):
            if case("hold"):
                pass
            # end if
            if case("0"):
                status_ = "hold"
                break
            # end if
            if case("approve"):
                pass
            # end if
            if case("1"):
                status_ = "approved"
                break
            # end if
            if case("spam"):
                pass
            # end if
            if case("trash"):
                pass
            # end if
            if case():
                status_ = comment_approved_
                break
            # end if
        # end for
        return status_
    # end def prepare_status_response
    #// 
    #// Prepares a single comment to be inserted into the database.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return array|WP_Error Prepared comment, otherwise WP_Error object.
    #//
    def prepare_item_for_database(self, request_=None):
        
        
        prepared_comment_ = Array()
        #// 
        #// Allow the comment_content to be set via the 'content' or
        #// the 'content.raw' properties of the Request object.
        #//
        if (php_isset(lambda : request_["content"])) and php_is_string(request_["content"]):
            prepared_comment_["comment_content"] = request_["content"]
        elif (php_isset(lambda : request_["content"]["raw"])) and php_is_string(request_["content"]["raw"]):
            prepared_comment_["comment_content"] = request_["content"]["raw"]
        # end if
        if (php_isset(lambda : request_["post"])):
            prepared_comment_["comment_post_ID"] = php_int(request_["post"])
        # end if
        if (php_isset(lambda : request_["parent"])):
            prepared_comment_["comment_parent"] = request_["parent"]
        # end if
        if (php_isset(lambda : request_["author"])):
            user_ = php_new_class("WP_User", lambda : WP_User(request_["author"]))
            if user_.exists():
                prepared_comment_["user_id"] = user_.ID
                prepared_comment_["comment_author"] = user_.display_name
                prepared_comment_["comment_author_email"] = user_.user_email
                prepared_comment_["comment_author_url"] = user_.user_url
            else:
                return php_new_class("WP_Error", lambda : WP_Error("rest_comment_author_invalid", __("Invalid comment author ID."), Array({"status": 400})))
            # end if
        # end if
        if (php_isset(lambda : request_["author_name"])):
            prepared_comment_["comment_author"] = request_["author_name"]
        # end if
        if (php_isset(lambda : request_["author_email"])):
            prepared_comment_["comment_author_email"] = request_["author_email"]
        # end if
        if (php_isset(lambda : request_["author_url"])):
            prepared_comment_["comment_author_url"] = request_["author_url"]
        # end if
        if (php_isset(lambda : request_["author_ip"])) and current_user_can("moderate_comments"):
            prepared_comment_["comment_author_IP"] = request_["author_ip"]
        elif (not php_empty(lambda : PHP_SERVER["REMOTE_ADDR"])) and rest_is_ip_address(PHP_SERVER["REMOTE_ADDR"]):
            prepared_comment_["comment_author_IP"] = PHP_SERVER["REMOTE_ADDR"]
        else:
            prepared_comment_["comment_author_IP"] = "127.0.0.1"
        # end if
        if (not php_empty(lambda : request_["author_user_agent"])):
            prepared_comment_["comment_agent"] = request_["author_user_agent"]
        elif request_.get_header("user_agent"):
            prepared_comment_["comment_agent"] = request_.get_header("user_agent")
        # end if
        if (not php_empty(lambda : request_["date"])):
            date_data_ = rest_get_date_with_gmt(request_["date"])
            if (not php_empty(lambda : date_data_)):
                prepared_comment_["comment_date"], prepared_comment_["comment_date_gmt"] = date_data_
            # end if
        elif (not php_empty(lambda : request_["date_gmt"])):
            date_data_ = rest_get_date_with_gmt(request_["date_gmt"], True)
            if (not php_empty(lambda : date_data_)):
                prepared_comment_["comment_date"], prepared_comment_["comment_date_gmt"] = date_data_
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
        return apply_filters("rest_preprocess_comment", prepared_comment_, request_)
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
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "comment", "type": "object", "properties": Array({"id": Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "edit", "embed"), "readonly": True})}, {"author": Array({"description": __("The ID of the user object, if author was a user."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"author_email": Array({"description": __("Email address for the object author."), "type": "string", "format": "email", "context": Array("edit"), "arg_options": Array({"sanitize_callback": Array(self, "check_comment_author_email"), "validate_callback": None})})}, {"author_ip": Array({"description": __("IP address for the object author."), "type": "string", "format": "ip", "context": Array("edit")})}, {"author_name": Array({"description": __("Display name for the object author."), "type": "string", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"author_url": Array({"description": __("URL for the object author."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed")})}, {"author_user_agent": Array({"description": __("User agent for the object author."), "type": "string", "context": Array("edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})}, {"content": Array({"description": __("The content for the object."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Content for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML content for the object, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})}, {"date": Array({"description": __("The date the object was published, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit", "embed")})}, {"date_gmt": Array({"description": __("The date the object was published, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"link": Array({"description": __("URL to the object."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed"), "readonly": True})}, {"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer", "context": Array("view", "edit", "embed"), "default": 0})}, {"post": Array({"description": __("The ID of the associated post object."), "type": "integer", "context": Array("view", "edit"), "default": 0})}, {"status": Array({"description": __("State of the object."), "type": "string", "context": Array("view", "edit"), "arg_options": Array({"sanitize_callback": "sanitize_key"})})}, {"type": Array({"description": __("Type of Comment for the object."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
        if get_option("show_avatars"):
            avatar_properties_ = Array()
            avatar_sizes_ = rest_get_avatar_sizes()
            for size_ in avatar_sizes_:
                avatar_properties_[size_] = Array({"description": php_sprintf(__("Avatar URL with image size of %d pixels."), size_), "type": "string", "format": "uri", "context": Array("embed", "view", "edit")})
            # end for
            schema_["properties"]["author_avatar_urls"] = Array({"description": __("Avatar URLs for the object author."), "type": "object", "context": Array("view", "edit", "embed"), "readonly": True, "properties": avatar_properties_})
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
    #// @return array Comments collection parameters.
    #//
    def get_collection_params(self):
        
        
        query_params_ = super().get_collection_params()
        query_params_["context"]["default"] = "view"
        query_params_["after"] = Array({"description": __("Limit response to comments published after a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        query_params_["author"] = Array({"description": __("Limit result set to comments assigned to specific user IDs. Requires authorization."), "type": "array", "items": Array({"type": "integer"})})
        query_params_["author_exclude"] = Array({"description": __("Ensure result set excludes comments assigned to specific user IDs. Requires authorization."), "type": "array", "items": Array({"type": "integer"})})
        query_params_["author_email"] = Array({"default": None, "description": __("Limit result set to that from a specific author email. Requires authorization."), "format": "email", "type": "string"})
        query_params_["before"] = Array({"description": __("Limit response to comments published before a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        query_params_["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params_["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "desc", "enum": Array("asc", "desc")})
        query_params_["orderby"] = Array({"description": __("Sort collection by object attribute."), "type": "string", "default": "date_gmt", "enum": Array("date", "date_gmt", "id", "include", "post", "parent", "type")})
        query_params_["parent"] = Array({"default": Array(), "description": __("Limit result set to comments of specific parent IDs."), "type": "array", "items": Array({"type": "integer"})})
        query_params_["parent_exclude"] = Array({"default": Array(), "description": __("Ensure result set excludes specific parent IDs."), "type": "array", "items": Array({"type": "integer"})})
        query_params_["post"] = Array({"default": Array(), "description": __("Limit result set to comments assigned to specific post IDs."), "type": "array", "items": Array({"type": "integer"})})
        query_params_["status"] = Array({"default": "approve", "description": __("Limit result set to comments assigned a specific status. Requires authorization."), "sanitize_callback": "sanitize_key", "type": "string", "validate_callback": "rest_validate_request_arg"})
        query_params_["type"] = Array({"default": "comment", "description": __("Limit result set to comments assigned a specific type. Requires authorization."), "sanitize_callback": "sanitize_key", "type": "string", "validate_callback": "rest_validate_request_arg"})
        query_params_["password"] = Array({"description": __("The password for the post if it is password protected."), "type": "string"})
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
        return apply_filters("rest_comment_collection_params", query_params_)
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
    def handle_status_param(self, new_status_=None, comment_id_=None):
        
        
        old_status_ = wp_get_comment_status(comment_id_)
        if new_status_ == old_status_:
            return False
        # end if
        for case in Switch(new_status_):
            if case("approved"):
                pass
            # end if
            if case("approve"):
                pass
            # end if
            if case("1"):
                changed_ = wp_set_comment_status(comment_id_, "approve")
                break
            # end if
            if case("hold"):
                pass
            # end if
            if case("0"):
                changed_ = wp_set_comment_status(comment_id_, "hold")
                break
            # end if
            if case("spam"):
                changed_ = wp_spam_comment(comment_id_)
                break
            # end if
            if case("unspam"):
                changed_ = wp_unspam_comment(comment_id_)
                break
            # end if
            if case("trash"):
                changed_ = wp_trash_comment(comment_id_)
                break
            # end if
            if case("untrash"):
                changed_ = wp_untrash_comment(comment_id_)
                break
            # end if
            if case():
                changed_ = False
                break
            # end if
        # end for
        return changed_
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
    def check_read_post_permission(self, post_=None, request_=None):
        
        
        post_type_ = get_post_type_object(post_.post_type)
        #// Return false if custom post type doesn't exist
        if (not post_type_):
            return False
        # end if
        posts_controller_ = post_type_.get_rest_controller()
        #// Ensure the posts controller is specifically a WP_REST_Posts_Controller instance
        #// before using methods specific to that controller.
        if (not type(posts_controller_).__name__ == "WP_REST_Posts_Controller"):
            posts_controller_ = php_new_class("WP_REST_Posts_Controller", lambda : WP_REST_Posts_Controller(post_.post_type))
        # end if
        has_password_filter_ = False
        #// Only check password if a specific post was queried for or a single comment
        requested_post_ = (not php_empty(lambda : request_["post"])) and (not php_is_array(request_["post"])) or 1 == php_count(request_["post"])
        requested_comment_ = (not php_empty(lambda : request_["id"]))
        if requested_post_ or requested_comment_ and posts_controller_.can_access_password_content(post_, request_):
            add_filter("post_password_required", "__return_false")
            has_password_filter_ = True
        # end if
        if post_password_required(post_):
            result_ = current_user_can(post_type_.cap.edit_post, post_.ID)
        else:
            result_ = posts_controller_.check_read_permission(post_)
        # end if
        if has_password_filter_:
            remove_filter("post_password_required", "__return_false")
        # end if
        return result_
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
    def check_read_permission(self, comment_=None, request_=None):
        
        
        if (not php_empty(lambda : comment_.comment_post_ID)):
            post_ = get_post(comment_.comment_post_ID)
            if post_:
                if self.check_read_post_permission(post_, request_) and 1 == php_int(comment_.comment_approved):
                    return True
                # end if
            # end if
        # end if
        if 0 == get_current_user_id():
            return False
        # end if
        if php_empty(lambda : comment_.comment_post_ID) and (not current_user_can("moderate_comments")):
            return False
        # end if
        if (not php_empty(lambda : comment_.user_id)) and get_current_user_id() == php_int(comment_.user_id):
            return True
        # end if
        return current_user_can("edit_comment", comment_.comment_ID)
    # end def check_read_permission
    #// 
    #// Checks if a comment can be edited or deleted.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Comment $comment Comment object.
    #// @return bool Whether the comment can be edited or deleted.
    #//
    def check_edit_permission(self, comment_=None):
        
        
        if 0 == php_int(get_current_user_id()):
            return False
        # end if
        if current_user_can("moderate_comments"):
            return True
        # end if
        return current_user_can("edit_comment", comment_.comment_ID)
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
    def check_comment_author_email(self, value_=None, request_=None, param_=None):
        
        
        email_ = php_str(value_)
        if php_empty(lambda : email_):
            return email_
        # end if
        check_email_ = rest_validate_request_arg(email_, request_, param_)
        if is_wp_error(check_email_):
            return check_email_
        # end if
        return email_
    # end def check_comment_author_email
# end class WP_REST_Comments_Controller
