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
#// REST API: WP_REST_Posts_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class to access posts via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Posts_Controller(WP_REST_Controller):
    #// 
    #// Post type.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    post_type = Array()
    #// 
    #// Instance of a post meta fields object.
    #// 
    #// @since 4.7.0
    #// @var WP_REST_Post_Meta_Fields
    #//
    meta = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $post_type Post type.
    #//
    def __init__(self, post_type_=None):
        
        
        self.post_type = post_type_
        self.namespace = "wp/v2"
        obj_ = get_post_type_object(post_type_)
        self.rest_base = obj_.rest_base if (not php_empty(lambda : obj_.rest_base)) else obj_.name
        self.meta = php_new_class("WP_REST_Post_Meta_Fields", lambda : WP_REST_Post_Meta_Fields(self.post_type))
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
        schema_ = self.get_item_schema()
        get_item_args_ = Array({"context": self.get_context_param(Array({"default": "view"}))})
        if (php_isset(lambda : schema_["properties"]["password"])):
            get_item_args_["password"] = Array({"description": __("The password for the post if it is password protected."), "type": "string"})
        # end if
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<id>[\\d]+)", Array({"args": Array({"id": Array({"description": __("Unique identifier for the object."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": get_item_args_}), Array({"methods": WP_REST_Server.EDITABLE, "callback": Array(self, "update_item"), "permission_callback": Array(self, "update_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE)}), Array({"methods": WP_REST_Server.DELETABLE, "callback": Array(self, "delete_item"), "permission_callback": Array(self, "delete_item_permissions_check"), "args": Array({"force": Array({"type": "boolean", "default": False, "description": __("Whether to bypass Trash and force deletion.")})})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks if a given request has access to read posts.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request_=None):
        
        
        post_type_ = get_post_type_object(self.post_type)
        if "edit" == request_["context"] and (not current_user_can(post_type_.cap.edit_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit posts in this post type."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Retrieves a collection of posts.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request_=None):
        
        
        #// Ensure a search string is set in case the orderby is set to 'relevance'.
        if (not php_empty(lambda : request_["orderby"])) and "relevance" == request_["orderby"] and php_empty(lambda : request_["search"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_no_search_term_defined", __("You need to define a search term to order by relevance."), Array({"status": 400})))
        # end if
        #// Ensure an include parameter is set in case the orderby is set to 'include'.
        if (not php_empty(lambda : request_["orderby"])) and "include" == request_["orderby"] and php_empty(lambda : request_["include"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_orderby_include_missing_include", __("You need to define an include parameter to order by include."), Array({"status": 400})))
        # end if
        #// Retrieve the list of registered collection query parameters.
        registered_ = self.get_collection_params()
        args_ = Array()
        #// 
        #// This array defines mappings between public API query parameters whose
        #// values are accepted as-passed, and their internal WP_Query parameter
        #// name equivalents (some are the same). Only values which are also
        #// present in $registered will be set.
        #//
        parameter_mappings_ = Array({"author": "author__in", "author_exclude": "author__not_in", "exclude": "post__not_in", "include": "post__in", "menu_order": "menu_order", "offset": "offset", "order": "order", "orderby": "orderby", "page": "paged", "parent": "post_parent__in", "parent_exclude": "post_parent__not_in", "search": "s", "slug": "post_name__in", "status": "post_status"})
        #// 
        #// For each known parameter which is both registered and present in the request,
        #// set the parameter's value on the query $args.
        #//
        for api_param_,wp_param_ in parameter_mappings_.items():
            if (php_isset(lambda : registered_[api_param_]) and php_isset(lambda : request_[api_param_])):
                args_[wp_param_] = request_[api_param_]
            # end if
        # end for
        #// Check for & assign any parameters which require special handling or setting.
        args_["date_query"] = Array()
        #// Set before into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered_["before"]) and php_isset(lambda : request_["before"])):
            args_["date_query"][0]["before"] = request_["before"]
        # end if
        #// Set after into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered_["after"]) and php_isset(lambda : request_["after"])):
            args_["date_query"][0]["after"] = request_["after"]
        # end if
        #// Ensure our per_page parameter overrides any provided posts_per_page filter.
        if (php_isset(lambda : registered_["per_page"])):
            args_["posts_per_page"] = request_["per_page"]
        # end if
        if (php_isset(lambda : registered_["sticky"]) and php_isset(lambda : request_["sticky"])):
            sticky_posts_ = get_option("sticky_posts", Array())
            if (not php_is_array(sticky_posts_)):
                sticky_posts_ = Array()
            # end if
            if request_["sticky"]:
                #// 
                #// As post__in will be used to only get sticky posts,
                #// we have to support the case where post__in was already
                #// specified.
                #//
                args_["post__in"] = php_array_intersect(sticky_posts_, args_["post__in"]) if args_["post__in"] else sticky_posts_
                #// 
                #// If we intersected, but there are no post ids in common,
                #// WP_Query won't return "no posts" for post__in = array()
                #// so we have to fake it a bit.
                #//
                if (not args_["post__in"]):
                    args_["post__in"] = Array(0)
                # end if
            elif sticky_posts_:
                #// 
                #// As post___not_in will be used to only get posts that
                #// are not sticky, we have to support the case where post__not_in
                #// was already specified.
                #//
                args_["post__not_in"] = php_array_merge(args_["post__not_in"], sticky_posts_)
            # end if
        # end if
        #// Force the post_type argument, since it's not a user input variable.
        args_["post_type"] = self.post_type
        #// 
        #// Filters the query arguments for a request.
        #// 
        #// Enables adding extra arguments or setting defaults for a post collection request.
        #// 
        #// @since 4.7.0
        #// 
        #// @link https://developer.wordpress.org/reference/classes/wp_query
        #// 
        #// @param array           $args    Key value array of query var to query value.
        #// @param WP_REST_Request $request The request used.
        #//
        args_ = apply_filters(str("rest_") + str(self.post_type) + str("_query"), args_, request_)
        query_args_ = self.prepare_items_query(args_, request_)
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        if (not php_empty(lambda : request_["tax_relation"])):
            query_args_["tax_query"] = Array({"relation": request_["tax_relation"]})
        # end if
        for taxonomy_ in taxonomies_:
            base_ = taxonomy_.rest_base if (not php_empty(lambda : taxonomy_.rest_base)) else taxonomy_.name
            tax_exclude_ = base_ + "_exclude"
            if (not php_empty(lambda : request_[base_])):
                query_args_["tax_query"][-1] = Array({"taxonomy": taxonomy_.name, "field": "term_id", "terms": request_[base_], "include_children": False})
            # end if
            if (not php_empty(lambda : request_[tax_exclude_])):
                query_args_["tax_query"][-1] = Array({"taxonomy": taxonomy_.name, "field": "term_id", "terms": request_[tax_exclude_], "include_children": False, "operator": "NOT IN"})
            # end if
        # end for
        posts_query_ = php_new_class("WP_Query", lambda : WP_Query())
        query_result_ = posts_query_.query(query_args_)
        #// Allow access to all password protected posts if the context is edit.
        if "edit" == request_["context"]:
            add_filter("post_password_required", "__return_false")
        # end if
        posts_ = Array()
        for post_ in query_result_:
            if (not self.check_read_permission(post_)):
                continue
            # end if
            data_ = self.prepare_item_for_response(post_, request_)
            posts_[-1] = self.prepare_response_for_collection(data_)
        # end for
        #// Reset filter.
        if "edit" == request_["context"]:
            remove_filter("post_password_required", "__return_false")
        # end if
        page_ = php_int(query_args_["paged"])
        total_posts_ = posts_query_.found_posts
        if total_posts_ < 1:
            query_args_["paged"] = None
            count_query_ = php_new_class("WP_Query", lambda : WP_Query())
            count_query_.query(query_args_)
            total_posts_ = count_query_.found_posts
        # end if
        max_pages_ = ceil(total_posts_ / php_int(posts_query_.query_vars["posts_per_page"]))
        if page_ > max_pages_ and total_posts_ > 0:
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_page_number", __("The page number requested is larger than the number of pages available."), Array({"status": 400})))
        # end if
        response_ = rest_ensure_response(posts_)
        response_.header("X-WP-Total", php_int(total_posts_))
        response_.header("X-WP-TotalPages", php_int(max_pages_))
        request_params_ = request_.get_query_params()
        base_ = add_query_arg(urlencode_deep(request_params_), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
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
    #// Get the post, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_Post|WP_Error Post object if ID is valid, WP_Error otherwise.
    #//
    def get_post(self, id_=None):
        
        
        error_ = php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post ID."), Array({"status": 404})))
        if php_int(id_) <= 0:
            return error_
        # end if
        post_ = get_post(php_int(id_))
        if php_empty(lambda : post_) or php_empty(lambda : post_.ID) or self.post_type != post_.post_type:
            return error_
        # end if
        return post_
    # end def get_post
    #// 
    #// Checks if a given request has access to read a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has read access for the item, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        post_ = self.get_post(request_["id"])
        if is_wp_error(post_):
            return post_
        # end if
        if "edit" == request_["context"] and post_ and (not self.check_update_permission(post_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        if post_ and (not php_empty(lambda : request_["password"])):
            #// Check post password, and return error if invalid.
            if (not hash_equals(post_.post_password, request_["password"])):
                return php_new_class("WP_Error", lambda : WP_Error("rest_post_incorrect_password", __("Incorrect post password."), Array({"status": 403})))
            # end if
        # end if
        #// Allow access to all password protected posts if the context is edit.
        if "edit" == request_["context"]:
            add_filter("post_password_required", "__return_false")
        # end if
        if post_:
            return self.check_read_permission(post_)
        # end if
        return True
    # end def get_item_permissions_check
    #// 
    #// Checks if the user can access password-protected content.
    #// 
    #// This method determines whether we need to override the regular password
    #// check in core with a filter.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post         $post    Post to check against.
    #// @param WP_REST_Request $request Request data to check.
    #// @return bool True if the user can access password-protected content, otherwise false.
    #//
    def can_access_password_content(self, post_=None, request_=None):
        
        
        if php_empty(lambda : post_.post_password):
            #// No filter required.
            return False
        # end if
        #// Edit context always gets access to password-protected posts.
        if "edit" == request_["context"]:
            return True
        # end if
        #// No password, no auth.
        if php_empty(lambda : request_["password"]):
            return False
        # end if
        #// Double-check the request password.
        return hash_equals(post_.post_password, request_["password"])
    # end def can_access_password_content
    #// 
    #// Retrieves a single post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request_=None):
        
        
        post_ = self.get_post(request_["id"])
        if is_wp_error(post_):
            return post_
        # end if
        data_ = self.prepare_item_for_response(post_, request_)
        response_ = rest_ensure_response(data_)
        if is_post_type_viewable(get_post_type_object(post_.post_type)):
            response_.link_header("alternate", get_permalink(post_.ID), Array({"type": "text/html"}))
        # end if
        return response_
    # end def get_item
    #// 
    #// Checks if a given request has access to create a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create items, WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request_=None):
        
        
        if (not php_empty(lambda : request_["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_exists", __("Cannot create existing post."), Array({"status": 400})))
        # end if
        post_type_ = get_post_type_object(self.post_type)
        if (not php_empty(lambda : request_["author"])) and get_current_user_id() != request_["author"] and (not current_user_can(post_type_.cap.edit_others_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit_others", __("Sorry, you are not allowed to create posts as this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not php_empty(lambda : request_["sticky"])) and (not current_user_can(post_type_.cap.edit_others_posts)) and (not current_user_can(post_type_.cap.publish_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_assign_sticky", __("Sorry, you are not allowed to make posts sticky."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not current_user_can(post_type_.cap.create_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_create", __("Sorry, you are not allowed to create posts as this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not self.check_assign_terms_permission(request_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_assign_term", __("Sorry, you are not allowed to assign the provided terms."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def create_item_permissions_check
    #// 
    #// Creates a single post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def create_item(self, request_=None):
        
        
        if (not php_empty(lambda : request_["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_exists", __("Cannot create existing post."), Array({"status": 400})))
        # end if
        prepared_post_ = self.prepare_item_for_database(request_)
        if is_wp_error(prepared_post_):
            return prepared_post_
        # end if
        prepared_post_.post_type = self.post_type
        post_id_ = wp_insert_post(wp_slash(prepared_post_), True)
        if is_wp_error(post_id_):
            if "db_insert_error" == post_id_.get_error_code():
                post_id_.add_data(Array({"status": 500}))
            else:
                post_id_.add_data(Array({"status": 400}))
            # end if
            return post_id_
        # end if
        post_ = get_post(post_id_)
        #// 
        #// Fires after a single post is created or updated via the REST API.
        #// 
        #// The dynamic portion of the hook name, `$this->post_type`, refers to the post type slug.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Post         $post     Inserted or updated post object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a post, false when updating.
        #//
        do_action(str("rest_insert_") + str(self.post_type), post_, request_, True)
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"]["sticky"])):
            if (not php_empty(lambda : request_["sticky"])):
                stick_post(post_id_)
            else:
                unstick_post(post_id_)
            # end if
        # end if
        if (not php_empty(lambda : schema_["properties"]["featured_media"])) and (php_isset(lambda : request_["featured_media"])):
            self.handle_featured_media(request_["featured_media"], post_id_)
        # end if
        if (not php_empty(lambda : schema_["properties"]["format"])) and (not php_empty(lambda : request_["format"])):
            set_post_format(post_, request_["format"])
        # end if
        if (not php_empty(lambda : schema_["properties"]["template"])) and (php_isset(lambda : request_["template"])):
            self.handle_template(request_["template"], post_id_, True)
        # end if
        terms_update_ = self.handle_terms(post_id_, request_)
        if is_wp_error(terms_update_):
            return terms_update_
        # end if
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], post_id_)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        post_ = get_post(post_id_)
        fields_update_ = self.update_additional_fields_for_object(post_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// 
        #// Fires after a single post is completely created or updated via the REST API.
        #// 
        #// The dynamic portion of the hook name, `$this->post_type`, refers to the post type slug.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_Post         $post     Inserted or updated post object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a post, false when updating.
        #//
        do_action(str("rest_after_insert_") + str(self.post_type), post_, request_, True)
        response_ = self.prepare_item_for_response(post_, request_)
        response_ = rest_ensure_response(response_)
        response_.set_status(201)
        response_.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, post_id_)))
        return response_
    # end def create_item
    #// 
    #// Checks if a given request has access to update a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def update_item_permissions_check(self, request_=None):
        
        
        post_ = self.get_post(request_["id"])
        if is_wp_error(post_):
            return post_
        # end if
        post_type_ = get_post_type_object(self.post_type)
        if post_ and (not self.check_update_permission(post_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit", __("Sorry, you are not allowed to edit this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not php_empty(lambda : request_["author"])) and get_current_user_id() != request_["author"] and (not current_user_can(post_type_.cap.edit_others_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit_others", __("Sorry, you are not allowed to update posts as this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not php_empty(lambda : request_["sticky"])) and (not current_user_can(post_type_.cap.edit_others_posts)) and (not current_user_can(post_type_.cap.publish_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_assign_sticky", __("Sorry, you are not allowed to make posts sticky."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not self.check_assign_terms_permission(request_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_assign_term", __("Sorry, you are not allowed to assign the provided terms."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def update_item_permissions_check
    #// 
    #// Updates a single post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def update_item(self, request_=None):
        
        
        valid_check_ = self.get_post(request_["id"])
        if is_wp_error(valid_check_):
            return valid_check_
        # end if
        post_ = self.prepare_item_for_database(request_)
        if is_wp_error(post_):
            return post_
        # end if
        #// Convert the post object to an array, otherwise wp_update_post() will expect non-escaped input.
        post_id_ = wp_update_post(wp_slash(post_), True)
        if is_wp_error(post_id_):
            if "db_update_error" == post_id_.get_error_code():
                post_id_.add_data(Array({"status": 500}))
            else:
                post_id_.add_data(Array({"status": 400}))
            # end if
            return post_id_
        # end if
        post_ = get_post(post_id_)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
        do_action(str("rest_insert_") + str(self.post_type), post_, request_, False)
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"]["format"])) and (not php_empty(lambda : request_["format"])):
            set_post_format(post_, request_["format"])
        # end if
        if (not php_empty(lambda : schema_["properties"]["featured_media"])) and (php_isset(lambda : request_["featured_media"])):
            self.handle_featured_media(request_["featured_media"], post_id_)
        # end if
        if (not php_empty(lambda : schema_["properties"]["sticky"])) and (php_isset(lambda : request_["sticky"])):
            if (not php_empty(lambda : request_["sticky"])):
                stick_post(post_id_)
            else:
                unstick_post(post_id_)
            # end if
        # end if
        if (not php_empty(lambda : schema_["properties"]["template"])) and (php_isset(lambda : request_["template"])):
            self.handle_template(request_["template"], post_.ID)
        # end if
        terms_update_ = self.handle_terms(post_.ID, request_)
        if is_wp_error(terms_update_):
            return terms_update_
        # end if
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], post_.ID)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        post_ = get_post(post_id_)
        fields_update_ = self.update_additional_fields_for_object(post_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// Filter is fired in WP_REST_Attachments_Controller subclass.
        if "attachment" == self.post_type:
            response_ = self.prepare_item_for_response(post_, request_)
            return rest_ensure_response(response_)
        # end if
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
        do_action(str("rest_after_insert_") + str(self.post_type), post_, request_, False)
        response_ = self.prepare_item_for_response(post_, request_)
        return rest_ensure_response(response_)
    # end def update_item
    #// 
    #// Checks if a given request has access to delete a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_item_permissions_check(self, request_=None):
        
        
        post_ = self.get_post(request_["id"])
        if is_wp_error(post_):
            return post_
        # end if
        if post_ and (not self.check_delete_permission(post_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("Sorry, you are not allowed to delete this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def delete_item_permissions_check
    #// 
    #// Deletes a single post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def delete_item(self, request_=None):
        
        
        post_ = self.get_post(request_["id"])
        if is_wp_error(post_):
            return post_
        # end if
        id_ = post_.ID
        force_ = php_bool(request_["force"])
        supports_trash_ = EMPTY_TRASH_DAYS > 0
        if "attachment" == post_.post_type:
            supports_trash_ = supports_trash_ and MEDIA_TRASH
        # end if
        #// 
        #// Filters whether a post is trashable.
        #// 
        #// The dynamic portion of the hook name, `$this->post_type`, refers to the post type slug.
        #// 
        #// Pass false to disable Trash support for the post.
        #// 
        #// @since 4.7.0
        #// 
        #// @param bool    $supports_trash Whether the post type support trashing.
        #// @param WP_Post $post           The Post object being considered for trashing support.
        #//
        supports_trash_ = apply_filters(str("rest_") + str(self.post_type) + str("_trashable"), supports_trash_, post_)
        if (not self.check_delete_permission(post_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_delete_post", __("Sorry, you are not allowed to delete this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        request_.set_param("context", "edit")
        #// If we're forcing, then delete permanently.
        if force_:
            previous_ = self.prepare_item_for_response(post_, request_)
            result_ = wp_delete_post(id_, True)
            response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
            response_.set_data(Array({"deleted": True, "previous": previous_.get_data()}))
        else:
            #// If we don't support trashing for this type, error out.
            if (not supports_trash_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("The post does not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
            # end if
            #// Otherwise, only trash if we haven't already.
            if "trash" == post_.post_status:
                return php_new_class("WP_Error", lambda : WP_Error("rest_already_trashed", __("The post has already been deleted."), Array({"status": 410})))
            # end if
            #// (Note that internally this falls through to `wp_delete_post()`
            #// if the Trash is disabled.)
            result_ = wp_trash_post(id_)
            post_ = get_post(id_)
            response_ = self.prepare_item_for_response(post_, request_)
        # end if
        if (not result_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The post cannot be deleted."), Array({"status": 500})))
        # end if
        #// 
        #// Fires immediately after a single post is deleted or trashed via the REST API.
        #// 
        #// They dynamic portion of the hook name, `$this->post_type`, refers to the post type slug.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Post          $post     The deleted or trashed post.
        #// @param WP_REST_Response $response The response data.
        #// @param WP_REST_Request  $request  The request sent to the API.
        #//
        do_action(str("rest_delete_") + str(self.post_type), post_, response_, request_)
        return response_
    # end def delete_item
    #// 
    #// Determines the allowed query_vars for a get_items() response and prepares
    #// them for WP_Query.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array           $prepared_args Optional. Prepared WP_Query arguments. Default empty array.
    #// @param WP_REST_Request $request       Optional. Full details about the request.
    #// @return array Items query arguments.
    #//
    def prepare_items_query(self, prepared_args_=None, request_=None):
        if prepared_args_ is None:
            prepared_args_ = Array()
        # end if
        if request_ is None:
            request_ = None
        # end if
        
        query_args_ = Array()
        for key_,value_ in prepared_args_.items():
            #// 
            #// Filters the query_vars used in get_items() for the constructed query.
            #// 
            #// The dynamic portion of the hook name, `$key`, refers to the query_var key.
            #// 
            #// @since 4.7.0
            #// 
            #// @param string $value The query_var value.
            #//
            query_args_[key_] = apply_filters(str("rest_query_var-") + str(key_), value_)
            pass
        # end for
        if "post" != self.post_type or (not (php_isset(lambda : query_args_["ignore_sticky_posts"]))):
            query_args_["ignore_sticky_posts"] = True
        # end if
        #// Map to proper WP_Query orderby param.
        if (php_isset(lambda : query_args_["orderby"])) and (php_isset(lambda : request_["orderby"])):
            orderby_mappings_ = Array({"id": "ID", "include": "post__in", "slug": "post_name", "include_slugs": "post_name__in"})
            if (php_isset(lambda : orderby_mappings_[request_["orderby"]])):
                query_args_["orderby"] = orderby_mappings_[request_["orderby"]]
            # end if
        # end if
        return query_args_
    # end def prepare_items_query
    #// 
    #// Checks the post_date_gmt or modified_gmt and prepare any post or
    #// modified date for single post output.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string      $date_gmt GMT publication time.
    #// @param string|null $date     Optional. Local publication time. Default null.
    #// @return string|null ISO8601/RFC3339 formatted datetime.
    #//
    def prepare_date_response(self, date_gmt_=None, date_=None):
        if date_ is None:
            date_ = None
        # end if
        
        #// Use the date if passed.
        if (php_isset(lambda : date_)):
            return mysql_to_rfc3339(date_)
        # end if
        #// Return null if $date_gmt is empty/zeros.
        if "0000-00-00 00:00:00" == date_gmt_:
            return None
        # end if
        #// Return the formatted datetime.
        return mysql_to_rfc3339(date_gmt_)
    # end def prepare_date_response
    #// 
    #// Prepares a single post for create or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return stdClass|WP_Error Post object or WP_Error.
    #//
    def prepare_item_for_database(self, request_=None):
        
        
        prepared_post_ = php_new_class("stdClass", lambda : stdClass())
        #// Post ID.
        if (php_isset(lambda : request_["id"])):
            existing_post_ = self.get_post(request_["id"])
            if is_wp_error(existing_post_):
                return existing_post_
            # end if
            prepared_post_.ID = existing_post_.ID
        # end if
        schema_ = self.get_item_schema()
        #// Post title.
        if (not php_empty(lambda : schema_["properties"]["title"])) and (php_isset(lambda : request_["title"])):
            if php_is_string(request_["title"]):
                prepared_post_.post_title = request_["title"]
            elif (not php_empty(lambda : request_["title"]["raw"])):
                prepared_post_.post_title = request_["title"]["raw"]
            # end if
        # end if
        #// Post content.
        if (not php_empty(lambda : schema_["properties"]["content"])) and (php_isset(lambda : request_["content"])):
            if php_is_string(request_["content"]):
                prepared_post_.post_content = request_["content"]
            elif (php_isset(lambda : request_["content"]["raw"])):
                prepared_post_.post_content = request_["content"]["raw"]
            # end if
        # end if
        #// Post excerpt.
        if (not php_empty(lambda : schema_["properties"]["excerpt"])) and (php_isset(lambda : request_["excerpt"])):
            if php_is_string(request_["excerpt"]):
                prepared_post_.post_excerpt = request_["excerpt"]
            elif (php_isset(lambda : request_["excerpt"]["raw"])):
                prepared_post_.post_excerpt = request_["excerpt"]["raw"]
            # end if
        # end if
        #// Post type.
        if php_empty(lambda : request_["id"]):
            #// Creating new post, use default type for the controller.
            prepared_post_.post_type = self.post_type
        else:
            #// Updating a post, use previous type.
            prepared_post_.post_type = get_post_type(request_["id"])
        # end if
        post_type_ = get_post_type_object(prepared_post_.post_type)
        #// Post status.
        if (not php_empty(lambda : schema_["properties"]["status"])) and (php_isset(lambda : request_["status"])):
            status_ = self.handle_status_param(request_["status"], post_type_)
            if is_wp_error(status_):
                return status_
            # end if
            prepared_post_.post_status = status_
        # end if
        #// Post date.
        if (not php_empty(lambda : schema_["properties"]["date"])) and (not php_empty(lambda : request_["date"])):
            current_date_ = get_post(prepared_post_.ID).post_date if (php_isset(lambda : prepared_post_.ID)) else False
            date_data_ = rest_get_date_with_gmt(request_["date"])
            if (not php_empty(lambda : date_data_)) and current_date_ != date_data_[0]:
                prepared_post_.post_date, prepared_post_.post_date_gmt = date_data_
                prepared_post_.edit_date = True
            # end if
        elif (not php_empty(lambda : schema_["properties"]["date_gmt"])) and (not php_empty(lambda : request_["date_gmt"])):
            current_date_ = get_post(prepared_post_.ID).post_date_gmt if (php_isset(lambda : prepared_post_.ID)) else False
            date_data_ = rest_get_date_with_gmt(request_["date_gmt"], True)
            if (not php_empty(lambda : date_data_)) and current_date_ != date_data_[1]:
                prepared_post_.post_date, prepared_post_.post_date_gmt = date_data_
                prepared_post_.edit_date = True
            # end if
        # end if
        #// Sending a null date or date_gmt value resets date and date_gmt to their
        #// default values (`0000-00-00 00:00:00`).
        if (not php_empty(lambda : schema_["properties"]["date_gmt"])) and request_.has_param("date_gmt") and None == request_["date_gmt"] or (not php_empty(lambda : schema_["properties"]["date"])) and request_.has_param("date") and None == request_["date"]:
            prepared_post_.post_date_gmt = None
            prepared_post_.post_date = None
        # end if
        #// Post slug.
        if (not php_empty(lambda : schema_["properties"]["slug"])) and (php_isset(lambda : request_["slug"])):
            prepared_post_.post_name = request_["slug"]
        # end if
        #// Author.
        if (not php_empty(lambda : schema_["properties"]["author"])) and (not php_empty(lambda : request_["author"])):
            post_author_ = php_int(request_["author"])
            if get_current_user_id() != post_author_:
                user_obj_ = get_userdata(post_author_)
                if (not user_obj_):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_author", __("Invalid author ID."), Array({"status": 400})))
                # end if
            # end if
            prepared_post_.post_author = post_author_
        # end if
        #// Post password.
        if (not php_empty(lambda : schema_["properties"]["password"])) and (php_isset(lambda : request_["password"])):
            prepared_post_.post_password = request_["password"]
            if "" != request_["password"]:
                if (not php_empty(lambda : schema_["properties"]["sticky"])) and (not php_empty(lambda : request_["sticky"])):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_field", __("A post can not be sticky and have a password."), Array({"status": 400})))
                # end if
                if (not php_empty(lambda : prepared_post_.ID)) and is_sticky(prepared_post_.ID):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_field", __("A sticky post can not be password protected."), Array({"status": 400})))
                # end if
            # end if
        # end if
        if (not php_empty(lambda : schema_["properties"]["sticky"])) and (not php_empty(lambda : request_["sticky"])):
            if (not php_empty(lambda : prepared_post_.ID)) and post_password_required(prepared_post_.ID):
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_field", __("A password protected post can not be set to sticky."), Array({"status": 400})))
            # end if
        # end if
        #// Parent.
        if (not php_empty(lambda : schema_["properties"]["parent"])) and (php_isset(lambda : request_["parent"])):
            if 0 == php_int(request_["parent"]):
                prepared_post_.post_parent = 0
            else:
                parent_ = get_post(php_int(request_["parent"]))
                if php_empty(lambda : parent_):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post parent ID."), Array({"status": 400})))
                # end if
                prepared_post_.post_parent = php_int(parent_.ID)
            # end if
        # end if
        #// Menu order.
        if (not php_empty(lambda : schema_["properties"]["menu_order"])) and (php_isset(lambda : request_["menu_order"])):
            prepared_post_.menu_order = php_int(request_["menu_order"])
        # end if
        #// Comment status.
        if (not php_empty(lambda : schema_["properties"]["comment_status"])) and (not php_empty(lambda : request_["comment_status"])):
            prepared_post_.comment_status = request_["comment_status"]
        # end if
        #// Ping status.
        if (not php_empty(lambda : schema_["properties"]["ping_status"])) and (not php_empty(lambda : request_["ping_status"])):
            prepared_post_.ping_status = request_["ping_status"]
        # end if
        if (not php_empty(lambda : schema_["properties"]["template"])):
            #// Force template to null so that it can be handled exclusively by the REST controller.
            prepared_post_.page_template = None
        # end if
        #// 
        #// Filters a post before it is inserted via the REST API.
        #// 
        #// The dynamic portion of the hook name, `$this->post_type`, refers to the post type slug.
        #// 
        #// @since 4.7.0
        #// 
        #// @param stdClass        $prepared_post An object representing a single post prepared
        #// for inserting or updating the database.
        #// @param WP_REST_Request $request       Request object.
        #//
        return apply_filters(str("rest_pre_insert_") + str(self.post_type), prepared_post_, request_)
    # end def prepare_item_for_database
    #// 
    #// Determines validity and normalizes the given status parameter.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string       $post_status Post status.
    #// @param WP_Post_Type $post_type   Post type.
    #// @return string|WP_Error Post status or WP_Error if lacking the proper permission.
    #//
    def handle_status_param(self, post_status_=None, post_type_=None):
        
        
        for case in Switch(post_status_):
            if case("draft"):
                pass
            # end if
            if case("pending"):
                break
            # end if
            if case("private"):
                if (not current_user_can(post_type_.cap.publish_posts)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_publish", __("Sorry, you are not allowed to create private posts in this post type."), Array({"status": rest_authorization_required_code()})))
                # end if
                break
            # end if
            if case("publish"):
                pass
            # end if
            if case("future"):
                if (not current_user_can(post_type_.cap.publish_posts)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_publish", __("Sorry, you are not allowed to publish posts in this post type."), Array({"status": rest_authorization_required_code()})))
                # end if
                break
            # end if
            if case():
                if (not get_post_status_object(post_status_)):
                    post_status_ = "draft"
                # end if
                break
            # end if
        # end for
        return post_status_
    # end def handle_status_param
    #// 
    #// Determines the featured media based on a request param.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int $featured_media Featured Media ID.
    #// @param int $post_id        Post ID.
    #// @return bool|WP_Error Whether the post thumbnail was successfully deleted, otherwise WP_Error.
    #//
    def handle_featured_media(self, featured_media_=None, post_id_=None):
        
        
        featured_media_ = php_int(featured_media_)
        if featured_media_:
            result_ = set_post_thumbnail(post_id_, featured_media_)
            if result_:
                return True
            else:
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_featured_media", __("Invalid featured media ID."), Array({"status": 400})))
            # end if
        else:
            return delete_post_thumbnail(post_id_)
        # end if
    # end def handle_featured_media
    #// 
    #// Check whether the template is valid for the given post.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string          $template Page template filename.
    #// @param WP_REST_Request $request  Request.
    #// @return bool|WP_Error True if template is still valid or if the same as existing value, or false if template not supported.
    #//
    def check_template(self, template_=None, request_=None):
        
        
        if (not template_):
            return True
        # end if
        if request_["id"]:
            current_template_ = get_page_template_slug(request_["id"])
        else:
            current_template_ = ""
        # end if
        #// Always allow for updating a post to the same template, even if that template is no longer supported.
        if template_ == current_template_:
            return True
        # end if
        #// If this is a create request, get_post() will return null and wp theme will fallback to the passed post type.
        allowed_templates_ = wp_get_theme().get_page_templates(get_post(request_["id"]), self.post_type)
        if (php_isset(lambda : allowed_templates_[template_])):
            return True
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not one of %2$s."), "template", php_implode(", ", php_array_keys(allowed_templates_)))))
    # end def check_template
    #// 
    #// Sets the template for a post.
    #// 
    #// @since 4.7.0
    #// @since 4.9.0 Added the `$validate` parameter.
    #// 
    #// @param string  $template Page template filename.
    #// @param integer $post_id  Post ID.
    #// @param bool    $validate Whether to validate that the template selected is valid.
    #//
    def handle_template(self, template_=None, post_id_=None, validate_=None):
        if validate_ is None:
            validate_ = False
        # end if
        
        if validate_ and (not php_array_key_exists(template_, wp_get_theme().get_page_templates(get_post(post_id_)))):
            template_ = ""
        # end if
        update_post_meta(post_id_, "_wp_page_template", template_)
    # end def handle_template
    #// 
    #// Updates the post's terms from a REST request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int             $post_id The post ID to update the terms form.
    #// @param WP_REST_Request $request The request object with post and terms data.
    #// @return null|WP_Error WP_Error on an error assigning any of the terms, otherwise null.
    #//
    def handle_terms(self, post_id_=None, request_=None):
        
        
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy_ in taxonomies_:
            base_ = taxonomy_.rest_base if (not php_empty(lambda : taxonomy_.rest_base)) else taxonomy_.name
            if (not (php_isset(lambda : request_[base_]))):
                continue
            # end if
            result_ = wp_set_object_terms(post_id_, request_[base_], taxonomy_.name)
            if is_wp_error(result_):
                return result_
            # end if
        # end for
    # end def handle_terms
    #// 
    #// Checks whether current user can assign all terms sent with the current request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request The request object with post and terms data.
    #// @return bool Whether the current user can assign the provided terms.
    #//
    def check_assign_terms_permission(self, request_=None):
        
        
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy_ in taxonomies_:
            base_ = taxonomy_.rest_base if (not php_empty(lambda : taxonomy_.rest_base)) else taxonomy_.name
            if (not (php_isset(lambda : request_[base_]))):
                continue
            # end if
            for term_id_ in request_[base_]:
                #// Invalid terms will be rejected later.
                if (not get_term(term_id_, taxonomy_.name)):
                    continue
                # end if
                if (not current_user_can("assign_term", php_int(term_id_))):
                    return False
                # end if
            # end for
        # end for
        return True
    # end def check_assign_terms_permission
    #// 
    #// Checks if a given post type can be viewed or managed.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post_Type|string $post_type Post type name or object.
    #// @return bool Whether the post type is allowed in REST.
    #//
    def check_is_post_type_allowed(self, post_type_=None):
        
        
        if (not php_is_object(post_type_)):
            post_type_ = get_post_type_object(post_type_)
        # end if
        if (not php_empty(lambda : post_type_)) and (not php_empty(lambda : post_type_.show_in_rest)):
            return True
        # end if
        return False
    # end def check_is_post_type_allowed
    #// 
    #// Checks if a post can be read.
    #// 
    #// Correctly handles posts with the inherit status.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return bool Whether the post can be read.
    #//
    def check_read_permission(self, post_=None):
        
        
        post_type_ = get_post_type_object(post_.post_type)
        if (not self.check_is_post_type_allowed(post_type_)):
            return False
        # end if
        #// Is the post readable?
        if "publish" == post_.post_status or current_user_can(post_type_.cap.read_post, post_.ID):
            return True
        # end if
        post_status_obj_ = get_post_status_object(post_.post_status)
        if post_status_obj_ and post_status_obj_.public:
            return True
        # end if
        #// Can we read the parent if we're inheriting?
        if "inherit" == post_.post_status and post_.post_parent > 0:
            parent_ = get_post(post_.post_parent)
            if parent_:
                return self.check_read_permission(parent_)
            # end if
        # end if
        #// 
        #// If there isn't a parent, but the status is set to inherit, assume
        #// it's published (as per get_post_status()).
        #//
        if "inherit" == post_.post_status:
            return True
        # end if
        return False
    # end def check_read_permission
    #// 
    #// Checks if a post can be edited.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return bool Whether the post can be edited.
    #//
    def check_update_permission(self, post_=None):
        
        
        post_type_ = get_post_type_object(post_.post_type)
        if (not self.check_is_post_type_allowed(post_type_)):
            return False
        # end if
        return current_user_can(post_type_.cap.edit_post, post_.ID)
    # end def check_update_permission
    #// 
    #// Checks if a post can be created.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return bool Whether the post can be created.
    #//
    def check_create_permission(self, post_=None):
        
        
        post_type_ = get_post_type_object(post_.post_type)
        if (not self.check_is_post_type_allowed(post_type_)):
            return False
        # end if
        return current_user_can(post_type_.cap.create_posts)
    # end def check_create_permission
    #// 
    #// Checks if a post can be deleted.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return bool Whether the post can be deleted.
    #//
    def check_delete_permission(self, post_=None):
        
        
        post_type_ = get_post_type_object(post_.post_type)
        if (not self.check_is_post_type_allowed(post_type_)):
            return False
        # end if
        return current_user_can(post_type_.cap.delete_post, post_.ID)
    # end def check_delete_permission
    #// 
    #// Prepares a single post output for response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post         $post    Post object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, post_=None, request_=None):
        
        global PHP_GLOBALS
        PHP_GLOBALS["post"] = post_
        setup_postdata(post_)
        fields_ = self.get_fields_for_response(request_)
        #// Base fields for every post.
        data_ = Array()
        if rest_is_field_included("id", fields_):
            data_["id"] = post_.ID
        # end if
        if rest_is_field_included("date", fields_):
            data_["date"] = self.prepare_date_response(post_.post_date_gmt, post_.post_date)
        # end if
        if rest_is_field_included("date_gmt", fields_):
            #// 
            #// For drafts, `post_date_gmt` may not be set, indicating that the date
            #// of the draft should be updated each time it is saved (see #38883).
            #// In this case, shim the value based on the `post_date` field
            #// with the site's timezone offset applied.
            #//
            if "0000-00-00 00:00:00" == post_.post_date_gmt:
                post_date_gmt_ = get_gmt_from_date(post_.post_date)
            else:
                post_date_gmt_ = post_.post_date_gmt
            # end if
            data_["date_gmt"] = self.prepare_date_response(post_date_gmt_)
        # end if
        if rest_is_field_included("guid", fields_):
            data_["guid"] = Array({"rendered": apply_filters("get_the_guid", post_.guid, post_.ID), "raw": post_.guid})
        # end if
        if rest_is_field_included("modified", fields_):
            data_["modified"] = self.prepare_date_response(post_.post_modified_gmt, post_.post_modified)
        # end if
        if rest_is_field_included("modified_gmt", fields_):
            #// 
            #// For drafts, `post_modified_gmt` may not be set (see `post_date_gmt` comments
            #// above). In this case, shim the value based on the `post_modified` field
            #// with the site's timezone offset applied.
            #//
            if "0000-00-00 00:00:00" == post_.post_modified_gmt:
                post_modified_gmt_ = gmdate("Y-m-d H:i:s", strtotime(post_.post_modified) - get_option("gmt_offset") * 3600)
            else:
                post_modified_gmt_ = post_.post_modified_gmt
            # end if
            data_["modified_gmt"] = self.prepare_date_response(post_modified_gmt_)
        # end if
        if rest_is_field_included("password", fields_):
            data_["password"] = post_.post_password
        # end if
        if rest_is_field_included("slug", fields_):
            data_["slug"] = post_.post_name
        # end if
        if rest_is_field_included("status", fields_):
            data_["status"] = post_.post_status
        # end if
        if rest_is_field_included("type", fields_):
            data_["type"] = post_.post_type
        # end if
        if rest_is_field_included("link", fields_):
            data_["link"] = get_permalink(post_.ID)
        # end if
        if rest_is_field_included("title", fields_):
            data_["title"] = Array()
        # end if
        if rest_is_field_included("title.raw", fields_):
            data_["title"]["raw"] = post_.post_title
        # end if
        if rest_is_field_included("title.rendered", fields_):
            add_filter("protected_title_format", Array(self, "protected_title_format"))
            data_["title"]["rendered"] = get_the_title(post_.ID)
            remove_filter("protected_title_format", Array(self, "protected_title_format"))
        # end if
        has_password_filter_ = False
        if self.can_access_password_content(post_, request_):
            #// Allow access to the post, permissions already checked before.
            add_filter("post_password_required", "__return_false")
            has_password_filter_ = True
        # end if
        if rest_is_field_included("content", fields_):
            data_["content"] = Array()
        # end if
        if rest_is_field_included("content.raw", fields_):
            data_["content"]["raw"] = post_.post_content
        # end if
        if rest_is_field_included("content.rendered", fields_):
            #// This filter is documented in wp-includes/post-template.php
            data_["content"]["rendered"] = "" if post_password_required(post_) else apply_filters("the_content", post_.post_content)
        # end if
        if rest_is_field_included("content.protected", fields_):
            data_["content"]["protected"] = php_bool(post_.post_password)
        # end if
        if rest_is_field_included("content.block_version", fields_):
            data_["content"]["block_version"] = block_version(post_.post_content)
        # end if
        if rest_is_field_included("excerpt", fields_):
            #// This filter is documented in wp-includes/post-template.php
            excerpt_ = apply_filters("get_the_excerpt", post_.post_excerpt, post_)
            #// This filter is documented in wp-includes/post-template.php
            excerpt_ = apply_filters("the_excerpt", excerpt_)
            data_["excerpt"] = Array({"raw": post_.post_excerpt, "rendered": "" if post_password_required(post_) else excerpt_, "protected": php_bool(post_.post_password)})
        # end if
        if has_password_filter_:
            #// Reset filter.
            remove_filter("post_password_required", "__return_false")
        # end if
        if rest_is_field_included("author", fields_):
            data_["author"] = php_int(post_.post_author)
        # end if
        if rest_is_field_included("featured_media", fields_):
            data_["featured_media"] = php_int(get_post_thumbnail_id(post_.ID))
        # end if
        if rest_is_field_included("parent", fields_):
            data_["parent"] = php_int(post_.post_parent)
        # end if
        if rest_is_field_included("menu_order", fields_):
            data_["menu_order"] = php_int(post_.menu_order)
        # end if
        if rest_is_field_included("comment_status", fields_):
            data_["comment_status"] = post_.comment_status
        # end if
        if rest_is_field_included("ping_status", fields_):
            data_["ping_status"] = post_.ping_status
        # end if
        if rest_is_field_included("sticky", fields_):
            data_["sticky"] = is_sticky(post_.ID)
        # end if
        if rest_is_field_included("template", fields_):
            template_ = get_page_template_slug(post_.ID)
            if template_:
                data_["template"] = template_
            else:
                data_["template"] = ""
            # end if
        # end if
        if rest_is_field_included("format", fields_):
            data_["format"] = get_post_format(post_.ID)
            #// Fill in blank post format.
            if php_empty(lambda : data_["format"]):
                data_["format"] = "standard"
            # end if
        # end if
        if rest_is_field_included("meta", fields_):
            data_["meta"] = self.meta.get_value(post_.ID, request_)
        # end if
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy_ in taxonomies_:
            base_ = taxonomy_.rest_base if (not php_empty(lambda : taxonomy_.rest_base)) else taxonomy_.name
            if rest_is_field_included(base_, fields_):
                terms_ = get_the_terms(post_, taxonomy_.name)
                data_[base_] = php_array_values(wp_list_pluck(terms_, "term_id")) if terms_ else Array()
            # end if
        # end for
        post_type_obj_ = get_post_type_object(post_.post_type)
        if is_post_type_viewable(post_type_obj_) and post_type_obj_.public:
            permalink_template_requested_ = rest_is_field_included("permalink_template", fields_)
            generated_slug_requested_ = rest_is_field_included("generated_slug", fields_)
            if permalink_template_requested_ or generated_slug_requested_:
                if (not php_function_exists("get_sample_permalink")):
                    php_include_file(ABSPATH + "wp-admin/includes/post.php", once=True)
                # end if
                sample_permalink_ = get_sample_permalink(post_.ID, post_.post_title, "")
                if permalink_template_requested_:
                    data_["permalink_template"] = sample_permalink_[0]
                # end if
                if generated_slug_requested_:
                    data_["generated_slug"] = sample_permalink_[1]
                # end if
            # end if
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        #// Wrap the data in a response object.
        response_ = rest_ensure_response(data_)
        links_ = self.prepare_links(post_)
        response_.add_links(links_)
        if (not php_empty(lambda : links_["self"]["href"])):
            actions_ = self.get_available_actions(post_, request_)
            self_ = links_["self"]["href"]
            for rel_ in actions_:
                response_.add_link(rel_, self_)
            # end for
        # end if
        #// 
        #// Filters the post data for a response.
        #// 
        #// The dynamic portion of the hook name, `$this->post_type`, refers to the post type slug.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_Post          $post     Post object.
        #// @param WP_REST_Request  $request  Request object.
        #//
        return apply_filters(str("rest_prepare_") + str(self.post_type), response_, post_, request_)
    # end def prepare_item_for_response
    #// 
    #// Overwrites the default protected title format.
    #// 
    #// By default, WordPress will show password protected posts with a title of
    #// "Protected: %s", as the REST API communicates the protected status of a post
    #// in a machine readable format, we remove the "Protected: " prefix.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string Protected title format.
    #//
    def protected_title_format(self):
        
        
        return "%s"
    # end def protected_title_format
    #// 
    #// Prepares links for the request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return array Links for the given post.
    #//
    def prepare_links(self, post_=None):
        
        
        base_ = php_sprintf("%s/%s", self.namespace, self.rest_base)
        #// Entity meta.
        links_ = Array({"self": Array({"href": rest_url(trailingslashit(base_) + post_.ID)})}, {"collection": Array({"href": rest_url(base_)})}, {"about": Array({"href": rest_url("wp/v2/types/" + self.post_type)})})
        if php_in_array(post_.post_type, Array("post", "page"), True) or post_type_supports(post_.post_type, "author") and (not php_empty(lambda : post_.post_author)):
            links_["author"] = Array({"href": rest_url("wp/v2/users/" + post_.post_author), "embeddable": True})
        # end if
        if php_in_array(post_.post_type, Array("post", "page"), True) or post_type_supports(post_.post_type, "comments"):
            replies_url_ = rest_url("wp/v2/comments")
            replies_url_ = add_query_arg("post", post_.ID, replies_url_)
            links_["replies"] = Array({"href": replies_url_, "embeddable": True})
        # end if
        if php_in_array(post_.post_type, Array("post", "page"), True) or post_type_supports(post_.post_type, "revisions"):
            revisions_ = wp_get_post_revisions(post_.ID, Array({"fields": "ids"}))
            revisions_count_ = php_count(revisions_)
            links_["version-history"] = Array({"href": rest_url(trailingslashit(base_) + post_.ID + "/revisions"), "count": revisions_count_})
            if revisions_count_ > 0:
                last_revision_ = php_array_shift(revisions_)
                links_["predecessor-version"] = Array({"href": rest_url(trailingslashit(base_) + post_.ID + "/revisions/" + last_revision_), "id": last_revision_})
            # end if
        # end if
        post_type_obj_ = get_post_type_object(post_.post_type)
        if post_type_obj_.hierarchical and (not php_empty(lambda : post_.post_parent)):
            links_["up"] = Array({"href": rest_url(trailingslashit(base_) + php_int(post_.post_parent)), "embeddable": True})
        # end if
        #// If we have a featured media, add that.
        featured_media_ = get_post_thumbnail_id(post_.ID)
        if featured_media_:
            image_url_ = rest_url("wp/v2/media/" + featured_media_)
            links_["https://api.w.org/featuredmedia"] = Array({"href": image_url_, "embeddable": True})
        # end if
        if (not php_in_array(post_.post_type, Array("attachment", "nav_menu_item", "revision"), True)):
            attachments_url_ = rest_url("wp/v2/media")
            attachments_url_ = add_query_arg("parent", post_.ID, attachments_url_)
            links_["https://api.w.org/attachment"] = Array({"href": attachments_url_})
        # end if
        taxonomies_ = get_object_taxonomies(post_.post_type)
        if (not php_empty(lambda : taxonomies_)):
            links_["https://api.w.org/term"] = Array()
            for tax_ in taxonomies_:
                taxonomy_obj_ = get_taxonomy(tax_)
                #// Skip taxonomies that are not public.
                if php_empty(lambda : taxonomy_obj_.show_in_rest):
                    continue
                # end if
                tax_base_ = taxonomy_obj_.rest_base if (not php_empty(lambda : taxonomy_obj_.rest_base)) else tax_
                terms_url_ = add_query_arg("post", post_.ID, rest_url("wp/v2/" + tax_base_))
                links_["https://api.w.org/term"][-1] = Array({"href": terms_url_, "taxonomy": tax_, "embeddable": True})
            # end for
        # end if
        return links_
    # end def prepare_links
    #// 
    #// Get the link relations available for the post and current user.
    #// 
    #// @since 4.9.8
    #// 
    #// @param WP_Post         $post    Post object.
    #// @param WP_REST_Request $request Request object.
    #// @return array List of link relations.
    #//
    def get_available_actions(self, post_=None, request_=None):
        
        
        if "edit" != request_["context"]:
            return Array()
        # end if
        rels_ = Array()
        post_type_ = get_post_type_object(post_.post_type)
        if "attachment" != self.post_type and current_user_can(post_type_.cap.publish_posts):
            rels_[-1] = "https://api.w.org/action-publish"
        # end if
        if current_user_can("unfiltered_html"):
            rels_[-1] = "https://api.w.org/action-unfiltered-html"
        # end if
        if "post" == post_type_.name:
            if current_user_can(post_type_.cap.edit_others_posts) and current_user_can(post_type_.cap.publish_posts):
                rels_[-1] = "https://api.w.org/action-sticky"
            # end if
        # end if
        if post_type_supports(post_type_.name, "author"):
            if current_user_can(post_type_.cap.edit_others_posts):
                rels_[-1] = "https://api.w.org/action-assign-author"
            # end if
        # end if
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for tax_ in taxonomies_:
            tax_base_ = tax_.rest_base if (not php_empty(lambda : tax_.rest_base)) else tax_.name
            create_cap_ = tax_.cap.edit_terms if is_taxonomy_hierarchical(tax_.name) else tax_.cap.assign_terms
            if current_user_can(create_cap_):
                rels_[-1] = "https://api.w.org/action-create-" + tax_base_
            # end if
            if current_user_can(tax_.cap.assign_terms):
                rels_[-1] = "https://api.w.org/action-assign-" + tax_base_
            # end if
        # end for
        return rels_
    # end def get_available_actions
    #// 
    #// Retrieves the post's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": self.post_type, "type": "object", "properties": Array({"date": Array({"description": __("The date the object was published, in the site's timezone."), "type": Array("string", "null"), "format": "date-time", "context": Array("view", "edit", "embed")})}, {"date_gmt": Array({"description": __("The date the object was published, as GMT."), "type": Array("string", "null"), "format": "date-time", "context": Array("view", "edit")})}, {"guid": Array({"description": __("The globally unique identifier for the object."), "type": "object", "context": Array("view", "edit"), "readonly": True, "properties": Array({"raw": Array({"description": __("GUID for the object, as it exists in the database."), "type": "string", "context": Array("edit"), "readonly": True})}, {"rendered": Array({"description": __("GUID for the object, transformed for display."), "type": "string", "context": Array("view", "edit"), "readonly": True})})})}, {"id": Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "edit", "embed"), "readonly": True})}, {"link": Array({"description": __("URL to the object."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed"), "readonly": True})}, {"modified": Array({"description": __("The date the object was last modified, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit"), "readonly": True})}, {"modified_gmt": Array({"description": __("The date the object was last modified, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the object unique to its type."), "type": "string", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": Array(self, "sanitize_slug")})})}, {"status": Array({"description": __("A named status for the object."), "type": "string", "enum": php_array_keys(get_post_stati(Array({"internal": False})))}, {"context": Array("view", "edit")})}, {"type": Array({"description": __("Type of Post for the object."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"password": Array({"description": __("A password to protect access to the content and excerpt."), "type": "string", "context": Array("edit")})})})
        post_type_obj_ = get_post_type_object(self.post_type)
        if is_post_type_viewable(post_type_obj_) and post_type_obj_.public:
            schema_["properties"]["permalink_template"] = Array({"description": __("Permalink template for the object."), "type": "string", "context": Array("edit"), "readonly": True})
            schema_["properties"]["generated_slug"] = Array({"description": __("Slug automatically generated from the object title."), "type": "string", "context": Array("edit"), "readonly": True})
        # end if
        if post_type_obj_.hierarchical:
            schema_["properties"]["parent"] = Array({"description": __("The ID for the parent of the object."), "type": "integer", "context": Array("view", "edit")})
        # end if
        post_type_attributes_ = Array("title", "editor", "author", "excerpt", "thumbnail", "comments", "revisions", "page-attributes", "post-formats", "custom-fields")
        fixed_schemas_ = Array({"post": Array("title", "editor", "author", "excerpt", "thumbnail", "comments", "revisions", "post-formats", "custom-fields"), "page": Array("title", "editor", "author", "excerpt", "thumbnail", "comments", "revisions", "page-attributes", "custom-fields"), "attachment": Array("title", "author", "comments", "revisions", "custom-fields")})
        for attribute_ in post_type_attributes_:
            if (php_isset(lambda : fixed_schemas_[self.post_type])) and (not php_in_array(attribute_, fixed_schemas_[self.post_type], True)):
                continue
            elif (not (php_isset(lambda : fixed_schemas_[self.post_type]))) and (not post_type_supports(self.post_type, attribute_)):
                continue
            # end if
            for case in Switch(attribute_):
                if case("title"):
                    schema_["properties"]["title"] = Array({"description": __("The title for the object."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Title for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML title for the object, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
                    break
                # end if
                if case("editor"):
                    schema_["properties"]["content"] = Array({"description": __("The content for the object."), "type": "object", "context": Array("view", "edit"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Content for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML content for the object, transformed for display."), "type": "string", "context": Array("view", "edit"), "readonly": True})}, {"block_version": Array({"description": __("Version of the content block format used by the object."), "type": "integer", "context": Array("edit"), "readonly": True})}, {"protected": Array({"description": __("Whether the content is protected with a password."), "type": "boolean", "context": Array("view", "edit", "embed"), "readonly": True})})})
                    break
                # end if
                if case("author"):
                    schema_["properties"]["author"] = Array({"description": __("The ID for the author of the object."), "type": "integer", "context": Array("view", "edit", "embed")})
                    break
                # end if
                if case("excerpt"):
                    schema_["properties"]["excerpt"] = Array({"description": __("The excerpt for the object."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Excerpt for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML excerpt for the object, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"protected": Array({"description": __("Whether the excerpt is protected with a password."), "type": "boolean", "context": Array("view", "edit", "embed"), "readonly": True})})})
                    break
                # end if
                if case("thumbnail"):
                    schema_["properties"]["featured_media"] = Array({"description": __("The ID of the featured media for the object."), "type": "integer", "context": Array("view", "edit", "embed")})
                    break
                # end if
                if case("comments"):
                    schema_["properties"]["comment_status"] = Array({"description": __("Whether or not comments are open on the object."), "type": "string", "enum": Array("open", "closed"), "context": Array("view", "edit")})
                    schema_["properties"]["ping_status"] = Array({"description": __("Whether or not the object can be pinged."), "type": "string", "enum": Array("open", "closed"), "context": Array("view", "edit")})
                    break
                # end if
                if case("page-attributes"):
                    schema_["properties"]["menu_order"] = Array({"description": __("The order of the object in relation to other object of its type."), "type": "integer", "context": Array("view", "edit")})
                    break
                # end if
                if case("post-formats"):
                    #// Get the native post formats and remove the array keys.
                    formats_ = php_array_values(get_post_format_slugs())
                    schema_["properties"]["format"] = Array({"description": __("The format for the object."), "type": "string", "enum": formats_, "context": Array("view", "edit")})
                    break
                # end if
                if case("custom-fields"):
                    schema_["properties"]["meta"] = self.meta.get_field_schema()
                    break
                # end if
            # end for
        # end for
        if "post" == self.post_type:
            schema_["properties"]["sticky"] = Array({"description": __("Whether or not the object should be treated as sticky."), "type": "boolean", "context": Array("view", "edit")})
        # end if
        schema_["properties"]["template"] = Array({"description": __("The theme file to use to display the object."), "type": "string", "context": Array("view", "edit"), "arg_options": Array({"validate_callback": Array(self, "check_template")})})
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy_ in taxonomies_:
            base_ = taxonomy_.rest_base if (not php_empty(lambda : taxonomy_.rest_base)) else taxonomy_.name
            if php_array_key_exists(base_, schema_["properties"]):
                taxonomy_field_name_with_conflict_ = "rest_base" if (not php_empty(lambda : taxonomy_.rest_base)) else "name"
                _doing_it_wrong("register_taxonomy", php_sprintf(__("The \"%1$s\" taxonomy \"%2$s\" property (%3$s) conflicts with an existing property on the REST API Posts Controller. Specify a custom \"rest_base\" when registering the taxonomy to avoid this error."), taxonomy_.name, taxonomy_field_name_with_conflict_, base_), "5.4.0")
            # end if
            schema_["properties"][base_] = Array({"description": php_sprintf(__("The terms assigned to the object in the %s taxonomy."), taxonomy_.name), "type": "array", "items": Array({"type": "integer"})}, {"context": Array("view", "edit")})
        # end for
        schema_links_ = self.get_schema_links()
        if schema_links_:
            schema_["links"] = schema_links_
        # end if
        #// Take a snapshot of which fields are in the schema pre-filtering.
        schema_fields_ = php_array_keys(schema_["properties"])
        #// 
        #// Filter the post's schema.
        #// 
        #// The dynamic portion of the filter, `$this->post_type`, refers to the
        #// post type slug for the controller.
        #// 
        #// @since 5.4.0
        #// 
        #// @param array $schema Item schema data.
        #//
        schema_ = apply_filters(str("rest_") + str(self.post_type) + str("_item_schema"), schema_)
        #// Emit a _doing_it_wrong warning if user tries to add new properties using this filter.
        new_fields_ = php_array_diff(php_array_keys(schema_["properties"]), schema_fields_)
        if php_count(new_fields_) > 0:
            _doing_it_wrong(__METHOD__, __("Please use register_rest_field to add new schema properties."), "5.4.0")
        # end if
        self.schema = schema_
        return self.add_additional_fields_schema(self.schema)
    # end def get_item_schema
    #// 
    #// Retrieve Link Description Objects that should be added to the Schema for the posts collection.
    #// 
    #// @since 4.9.8
    #// 
    #// @return array
    #//
    def get_schema_links(self):
        
        
        href_ = rest_url(str(self.namespace) + str("/") + str(self.rest_base) + str("/{id}"))
        links_ = Array()
        if "attachment" != self.post_type:
            links_[-1] = Array({"rel": "https://api.w.org/action-publish", "title": __("The current user can publish this post."), "href": href_, "targetSchema": Array({"type": "object", "properties": Array({"status": Array({"type": "string", "enum": Array("publish", "future")})})})})
        # end if
        links_[-1] = Array({"rel": "https://api.w.org/action-unfiltered-html", "title": __("The current user can post unfiltered HTML markup and JavaScript."), "href": href_, "targetSchema": Array({"type": "object", "properties": Array({"content": Array({"raw": Array({"type": "string"})})})})})
        if "post" == self.post_type:
            links_[-1] = Array({"rel": "https://api.w.org/action-sticky", "title": __("The current user can sticky this post."), "href": href_, "targetSchema": Array({"type": "object", "properties": Array({"sticky": Array({"type": "boolean"})})})})
        # end if
        if post_type_supports(self.post_type, "author"):
            links_[-1] = Array({"rel": "https://api.w.org/action-assign-author", "title": __("The current user can change the author on this post."), "href": href_, "targetSchema": Array({"type": "object", "properties": Array({"author": Array({"type": "integer"})})})})
        # end if
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for tax_ in taxonomies_:
            tax_base_ = tax_.rest_base if (not php_empty(lambda : tax_.rest_base)) else tax_.name
            #// translators: %s: Taxonomy name.
            assign_title_ = php_sprintf(__("The current user can assign terms in the %s taxonomy."), tax_.name)
            #// translators: %s: Taxonomy name.
            create_title_ = php_sprintf(__("The current user can create terms in the %s taxonomy."), tax_.name)
            links_[-1] = Array({"rel": "https://api.w.org/action-assign-" + tax_base_, "title": assign_title_, "href": href_, "targetSchema": Array({"type": "object", "properties": Array({tax_base_: Array({"type": "array", "items": Array({"type": "integer"})})})})})
            links_[-1] = Array({"rel": "https://api.w.org/action-create-" + tax_base_, "title": create_title_, "href": href_, "targetSchema": Array({"type": "object", "properties": Array({tax_base_: Array({"type": "array", "items": Array({"type": "integer"})})})})})
        # end for
        return links_
    # end def get_schema_links
    #// 
    #// Retrieves the query params for the posts collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Collection parameters.
    #//
    def get_collection_params(self):
        
        
        query_params_ = super().get_collection_params()
        query_params_["context"]["default"] = "view"
        query_params_["after"] = Array({"description": __("Limit response to posts published after a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        if post_type_supports(self.post_type, "author"):
            query_params_["author"] = Array({"description": __("Limit result set to posts assigned to specific authors."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
            query_params_["author_exclude"] = Array({"description": __("Ensure result set excludes posts assigned to specific authors."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        # end if
        query_params_["before"] = Array({"description": __("Limit response to posts published before a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        query_params_["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        if "page" == self.post_type or post_type_supports(self.post_type, "page-attributes"):
            query_params_["menu_order"] = Array({"description": __("Limit result set to posts with a specific menu_order value."), "type": "integer"})
        # end if
        query_params_["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params_["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "desc", "enum": Array("asc", "desc")})
        query_params_["orderby"] = Array({"description": __("Sort collection by object attribute."), "type": "string", "default": "date", "enum": Array("author", "date", "id", "include", "modified", "parent", "relevance", "slug", "include_slugs", "title")})
        if "page" == self.post_type or post_type_supports(self.post_type, "page-attributes"):
            query_params_["orderby"]["enum"][-1] = "menu_order"
        # end if
        post_type_ = get_post_type_object(self.post_type)
        if post_type_.hierarchical or "attachment" == self.post_type:
            query_params_["parent"] = Array({"description": __("Limit result set to items with particular parent IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
            query_params_["parent_exclude"] = Array({"description": __("Limit result set to all items except those of a particular parent ID."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        # end if
        query_params_["slug"] = Array({"description": __("Limit result set to posts with one or more specific slugs."), "type": "array", "items": Array({"type": "string"})}, {"sanitize_callback": "wp_parse_slug_list"})
        query_params_["status"] = Array({"default": "publish", "description": __("Limit result set to posts assigned one or more statuses."), "type": "array", "items": Array({"enum": php_array_merge(php_array_keys(get_post_stati()), Array("any")), "type": "string"})}, {"sanitize_callback": Array(self, "sanitize_post_statuses")})
        taxonomies_ = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        if (not php_empty(lambda : taxonomies_)):
            query_params_["tax_relation"] = Array({"description": __("Limit result set based on relationship between multiple taxonomies."), "type": "string", "enum": Array("AND", "OR")})
        # end if
        for taxonomy_ in taxonomies_:
            base_ = taxonomy_.rest_base if (not php_empty(lambda : taxonomy_.rest_base)) else taxonomy_.name
            query_params_[base_] = Array({"description": php_sprintf(__("Limit result set to all items that have the specified term assigned in the %s taxonomy."), base_), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
            query_params_[base_ + "_exclude"] = Array({"description": php_sprintf(__("Limit result set to all items except those that have the specified term assigned in the %s taxonomy."), base_), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        # end for
        if "post" == self.post_type:
            query_params_["sticky"] = Array({"description": __("Limit result set to items that are sticky."), "type": "boolean"})
        # end if
        #// 
        #// Filter collection parameters for the posts controller.
        #// 
        #// The dynamic part of the filter `$this->post_type` refers to the post
        #// type slug for the controller.
        #// 
        #// This filter registers the collection parameter, but does not map the
        #// collection parameter to an internal WP_Query parameter. Use the
        #// `rest_{$this->post_type}_query` filter to set WP_Query parameters.
        #// 
        #// @since 4.7.0
        #// 
        #// @param array        $query_params JSON Schema-formatted collection parameters.
        #// @param WP_Post_Type $post_type    Post type object.
        #//
        return apply_filters(str("rest_") + str(self.post_type) + str("_collection_params"), query_params_, post_type_)
    # end def get_collection_params
    #// 
    #// Sanitizes and validates the list of post statuses, including whether the
    #// user can query private statuses.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string|array    $statuses  One or more post statuses.
    #// @param WP_REST_Request $request   Full details about the request.
    #// @param string          $parameter Additional parameter to pass to validation.
    #// @return array|WP_Error A list of valid statuses, otherwise WP_Error object.
    #//
    def sanitize_post_statuses(self, statuses_=None, request_=None, parameter_=None):
        
        
        statuses_ = wp_parse_slug_list(statuses_)
        #// The default status is different in WP_REST_Attachments_Controller.
        attributes_ = request_.get_attributes()
        default_status_ = attributes_["args"]["status"]["default"]
        for status_ in statuses_:
            if status_ == default_status_:
                continue
            # end if
            post_type_obj_ = get_post_type_object(self.post_type)
            if current_user_can(post_type_obj_.cap.edit_posts) or "private" == status_ and current_user_can(post_type_obj_.cap.read_private_posts):
                result_ = rest_validate_request_arg(status_, request_, parameter_)
                if is_wp_error(result_):
                    return result_
                # end if
            else:
                return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_status", __("Status is forbidden."), Array({"status": rest_authorization_required_code()})))
            # end if
        # end for
        return statuses_
    # end def sanitize_post_statuses
# end class WP_REST_Posts_Controller
