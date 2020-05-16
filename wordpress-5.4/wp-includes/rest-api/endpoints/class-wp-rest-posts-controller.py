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
    post_type = Array()
    meta = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $post_type Post type.
    #//
    def __init__(self, post_type=None):
        
        self.post_type = post_type
        self.namespace = "wp/v2"
        obj = get_post_type_object(post_type)
        self.rest_base = obj.rest_base if (not php_empty(lambda : obj.rest_base)) else obj.name
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
        schema = self.get_item_schema()
        get_item_args = Array({"context": self.get_context_param(Array({"default": "view"}))})
        if (php_isset(lambda : schema["properties"]["password"])):
            get_item_args["password"] = Array({"description": __("The password for the post if it is password protected."), "type": "string"})
        # end if
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<id>[\\d]+)", Array({"args": Array({"id": Array({"description": __("Unique identifier for the object."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": get_item_args}), Array({"methods": WP_REST_Server.EDITABLE, "callback": Array(self, "update_item"), "permission_callback": Array(self, "update_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE)}), Array({"methods": WP_REST_Server.DELETABLE, "callback": Array(self, "delete_item"), "permission_callback": Array(self, "delete_item_permissions_check"), "args": Array({"force": Array({"type": "boolean", "default": False, "description": __("Whether to bypass Trash and force deletion.")})})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks if a given request has access to read posts.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request=None):
        
        post_type = get_post_type_object(self.post_type)
        if "edit" == request["context"] and (not current_user_can(post_type.cap.edit_posts)):
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
    def get_items(self, request=None):
        
        #// Ensure a search string is set in case the orderby is set to 'relevance'.
        if (not php_empty(lambda : request["orderby"])) and "relevance" == request["orderby"] and php_empty(lambda : request["search"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_no_search_term_defined", __("You need to define a search term to order by relevance."), Array({"status": 400})))
        # end if
        #// Ensure an include parameter is set in case the orderby is set to 'include'.
        if (not php_empty(lambda : request["orderby"])) and "include" == request["orderby"] and php_empty(lambda : request["include"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_orderby_include_missing_include", __("You need to define an include parameter to order by include."), Array({"status": 400})))
        # end if
        #// Retrieve the list of registered collection query parameters.
        registered = self.get_collection_params()
        args = Array()
        #// 
        #// This array defines mappings between public API query parameters whose
        #// values are accepted as-passed, and their internal WP_Query parameter
        #// name equivalents (some are the same). Only values which are also
        #// present in $registered will be set.
        #//
        parameter_mappings = Array({"author": "author__in", "author_exclude": "author__not_in", "exclude": "post__not_in", "include": "post__in", "menu_order": "menu_order", "offset": "offset", "order": "order", "orderby": "orderby", "page": "paged", "parent": "post_parent__in", "parent_exclude": "post_parent__not_in", "search": "s", "slug": "post_name__in", "status": "post_status"})
        #// 
        #// For each known parameter which is both registered and present in the request,
        #// set the parameter's value on the query $args.
        #//
        for api_param,wp_param in parameter_mappings:
            if (php_isset(lambda : registered[api_param]) and php_isset(lambda : request[api_param])):
                args[wp_param] = request[api_param]
            # end if
        # end for
        #// Check for & assign any parameters which require special handling or setting.
        args["date_query"] = Array()
        #// Set before into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered["before"]) and php_isset(lambda : request["before"])):
            args["date_query"][0]["before"] = request["before"]
        # end if
        #// Set after into date query. Date query must be specified as an array of an array.
        if (php_isset(lambda : registered["after"]) and php_isset(lambda : request["after"])):
            args["date_query"][0]["after"] = request["after"]
        # end if
        #// Ensure our per_page parameter overrides any provided posts_per_page filter.
        if (php_isset(lambda : registered["per_page"])):
            args["posts_per_page"] = request["per_page"]
        # end if
        if (php_isset(lambda : registered["sticky"]) and php_isset(lambda : request["sticky"])):
            sticky_posts = get_option("sticky_posts", Array())
            if (not php_is_array(sticky_posts)):
                sticky_posts = Array()
            # end if
            if request["sticky"]:
                #// 
                #// As post__in will be used to only get sticky posts,
                #// we have to support the case where post__in was already
                #// specified.
                #//
                args["post__in"] = php_array_intersect(sticky_posts, args["post__in"]) if args["post__in"] else sticky_posts
                #// 
                #// If we intersected, but there are no post ids in common,
                #// WP_Query won't return "no posts" for post__in = array()
                #// so we have to fake it a bit.
                #//
                if (not args["post__in"]):
                    args["post__in"] = Array(0)
                # end if
            elif sticky_posts:
                #// 
                #// As post___not_in will be used to only get posts that
                #// are not sticky, we have to support the case where post__not_in
                #// was already specified.
                #//
                args["post__not_in"] = php_array_merge(args["post__not_in"], sticky_posts)
            # end if
        # end if
        #// Force the post_type argument, since it's not a user input variable.
        args["post_type"] = self.post_type
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
        args = apply_filters(str("rest_") + str(self.post_type) + str("_query"), args, request)
        query_args = self.prepare_items_query(args, request)
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        if (not php_empty(lambda : request["tax_relation"])):
            query_args["tax_query"] = Array({"relation": request["tax_relation"]})
        # end if
        for taxonomy in taxonomies:
            base = taxonomy.rest_base if (not php_empty(lambda : taxonomy.rest_base)) else taxonomy.name
            tax_exclude = base + "_exclude"
            if (not php_empty(lambda : request[base])):
                query_args["tax_query"][-1] = Array({"taxonomy": taxonomy.name, "field": "term_id", "terms": request[base], "include_children": False})
            # end if
            if (not php_empty(lambda : request[tax_exclude])):
                query_args["tax_query"][-1] = Array({"taxonomy": taxonomy.name, "field": "term_id", "terms": request[tax_exclude], "include_children": False, "operator": "NOT IN"})
            # end if
        # end for
        posts_query = php_new_class("WP_Query", lambda : WP_Query())
        query_result = posts_query.query(query_args)
        #// Allow access to all password protected posts if the context is edit.
        if "edit" == request["context"]:
            add_filter("post_password_required", "__return_false")
        # end if
        posts = Array()
        for post in query_result:
            if (not self.check_read_permission(post)):
                continue
            # end if
            data = self.prepare_item_for_response(post, request)
            posts[-1] = self.prepare_response_for_collection(data)
        # end for
        #// Reset filter.
        if "edit" == request["context"]:
            remove_filter("post_password_required", "__return_false")
        # end if
        page = php_int(query_args["paged"])
        total_posts = posts_query.found_posts
        if total_posts < 1:
            query_args["paged"] = None
            count_query = php_new_class("WP_Query", lambda : WP_Query())
            count_query.query(query_args)
            total_posts = count_query.found_posts
        # end if
        max_pages = ceil(total_posts / php_int(posts_query.query_vars["posts_per_page"]))
        if page > max_pages and total_posts > 0:
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_page_number", __("The page number requested is larger than the number of pages available."), Array({"status": 400})))
        # end if
        response = rest_ensure_response(posts)
        response.header("X-WP-Total", php_int(total_posts))
        response.header("X-WP-TotalPages", php_int(max_pages))
        request_params = request.get_query_params()
        base = add_query_arg(urlencode_deep(request_params), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
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
    #// Get the post, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_Post|WP_Error Post object if ID is valid, WP_Error otherwise.
    #//
    def get_post(self, id=None):
        
        error = php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post ID."), Array({"status": 404})))
        if php_int(id) <= 0:
            return error
        # end if
        post = get_post(php_int(id))
        if php_empty(lambda : post) or php_empty(lambda : post.ID) or self.post_type != post.post_type:
            return error
        # end if
        return post
    # end def get_post
    #// 
    #// Checks if a given request has access to read a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has read access for the item, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request=None):
        
        post = self.get_post(request["id"])
        if is_wp_error(post):
            return post
        # end if
        if "edit" == request["context"] and post and (not self.check_update_permission(post)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        if post and (not php_empty(lambda : request["password"])):
            #// Check post password, and return error if invalid.
            if (not hash_equals(post.post_password, request["password"])):
                return php_new_class("WP_Error", lambda : WP_Error("rest_post_incorrect_password", __("Incorrect post password."), Array({"status": 403})))
            # end if
        # end if
        #// Allow access to all password protected posts if the context is edit.
        if "edit" == request["context"]:
            add_filter("post_password_required", "__return_false")
        # end if
        if post:
            return self.check_read_permission(post)
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
    def can_access_password_content(self, post=None, request=None):
        
        if php_empty(lambda : post.post_password):
            #// No filter required.
            return False
        # end if
        #// Edit context always gets access to password-protected posts.
        if "edit" == request["context"]:
            return True
        # end if
        #// No password, no auth.
        if php_empty(lambda : request["password"]):
            return False
        # end if
        #// Double-check the request password.
        return hash_equals(post.post_password, request["password"])
    # end def can_access_password_content
    #// 
    #// Retrieves a single post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request=None):
        
        post = self.get_post(request["id"])
        if is_wp_error(post):
            return post
        # end if
        data = self.prepare_item_for_response(post, request)
        response = rest_ensure_response(data)
        if is_post_type_viewable(get_post_type_object(post.post_type)):
            response.link_header("alternate", get_permalink(post.ID), Array({"type": "text/html"}))
        # end if
        return response
    # end def get_item
    #// 
    #// Checks if a given request has access to create a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create items, WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request=None):
        
        if (not php_empty(lambda : request["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_exists", __("Cannot create existing post."), Array({"status": 400})))
        # end if
        post_type = get_post_type_object(self.post_type)
        if (not php_empty(lambda : request["author"])) and get_current_user_id() != request["author"] and (not current_user_can(post_type.cap.edit_others_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit_others", __("Sorry, you are not allowed to create posts as this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not php_empty(lambda : request["sticky"])) and (not current_user_can(post_type.cap.edit_others_posts)) and (not current_user_can(post_type.cap.publish_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_assign_sticky", __("Sorry, you are not allowed to make posts sticky."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not current_user_can(post_type.cap.create_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_create", __("Sorry, you are not allowed to create posts as this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not self.check_assign_terms_permission(request)):
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
    def create_item(self, request=None):
        
        if (not php_empty(lambda : request["id"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_post_exists", __("Cannot create existing post."), Array({"status": 400})))
        # end if
        prepared_post = self.prepare_item_for_database(request)
        if is_wp_error(prepared_post):
            return prepared_post
        # end if
        prepared_post.post_type = self.post_type
        post_id = wp_insert_post(wp_slash(prepared_post), True)
        if is_wp_error(post_id):
            if "db_insert_error" == post_id.get_error_code():
                post_id.add_data(Array({"status": 500}))
            else:
                post_id.add_data(Array({"status": 400}))
            # end if
            return post_id
        # end if
        post = get_post(post_id)
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
        do_action(str("rest_insert_") + str(self.post_type), post, request, True)
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"]["sticky"])):
            if (not php_empty(lambda : request["sticky"])):
                stick_post(post_id)
            else:
                unstick_post(post_id)
            # end if
        # end if
        if (not php_empty(lambda : schema["properties"]["featured_media"])) and (php_isset(lambda : request["featured_media"])):
            self.handle_featured_media(request["featured_media"], post_id)
        # end if
        if (not php_empty(lambda : schema["properties"]["format"])) and (not php_empty(lambda : request["format"])):
            set_post_format(post, request["format"])
        # end if
        if (not php_empty(lambda : schema["properties"]["template"])) and (php_isset(lambda : request["template"])):
            self.handle_template(request["template"], post_id, True)
        # end if
        terms_update = self.handle_terms(post_id, request)
        if is_wp_error(terms_update):
            return terms_update
        # end if
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], post_id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        post = get_post(post_id)
        fields_update = self.update_additional_fields_for_object(post, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
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
        do_action(str("rest_after_insert_") + str(self.post_type), post, request, True)
        response = self.prepare_item_for_response(post, request)
        response = rest_ensure_response(response)
        response.set_status(201)
        response.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, post_id)))
        return response
    # end def create_item
    #// 
    #// Checks if a given request has access to update a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def update_item_permissions_check(self, request=None):
        
        post = self.get_post(request["id"])
        if is_wp_error(post):
            return post
        # end if
        post_type = get_post_type_object(self.post_type)
        if post and (not self.check_update_permission(post)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit", __("Sorry, you are not allowed to edit this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not php_empty(lambda : request["author"])) and get_current_user_id() != request["author"] and (not current_user_can(post_type.cap.edit_others_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit_others", __("Sorry, you are not allowed to update posts as this user."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not php_empty(lambda : request["sticky"])) and (not current_user_can(post_type.cap.edit_others_posts)) and (not current_user_can(post_type.cap.publish_posts)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_assign_sticky", __("Sorry, you are not allowed to make posts sticky."), Array({"status": rest_authorization_required_code()})))
        # end if
        if (not self.check_assign_terms_permission(request)):
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
    def update_item(self, request=None):
        
        valid_check = self.get_post(request["id"])
        if is_wp_error(valid_check):
            return valid_check
        # end if
        post = self.prepare_item_for_database(request)
        if is_wp_error(post):
            return post
        # end if
        #// Convert the post object to an array, otherwise wp_update_post() will expect non-escaped input.
        post_id = wp_update_post(wp_slash(post), True)
        if is_wp_error(post_id):
            if "db_update_error" == post_id.get_error_code():
                post_id.add_data(Array({"status": 500}))
            else:
                post_id.add_data(Array({"status": 400}))
            # end if
            return post_id
        # end if
        post = get_post(post_id)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
        do_action(str("rest_insert_") + str(self.post_type), post, request, False)
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"]["format"])) and (not php_empty(lambda : request["format"])):
            set_post_format(post, request["format"])
        # end if
        if (not php_empty(lambda : schema["properties"]["featured_media"])) and (php_isset(lambda : request["featured_media"])):
            self.handle_featured_media(request["featured_media"], post_id)
        # end if
        if (not php_empty(lambda : schema["properties"]["sticky"])) and (php_isset(lambda : request["sticky"])):
            if (not php_empty(lambda : request["sticky"])):
                stick_post(post_id)
            else:
                unstick_post(post_id)
            # end if
        # end if
        if (not php_empty(lambda : schema["properties"]["template"])) and (php_isset(lambda : request["template"])):
            self.handle_template(request["template"], post.ID)
        # end if
        terms_update = self.handle_terms(post.ID, request)
        if is_wp_error(terms_update):
            return terms_update
        # end if
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], post.ID)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        post = get_post(post_id)
        fields_update = self.update_additional_fields_for_object(post, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// Filter is fired in WP_REST_Attachments_Controller subclass.
        if "attachment" == self.post_type:
            response = self.prepare_item_for_response(post, request)
            return rest_ensure_response(response)
        # end if
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
        do_action(str("rest_after_insert_") + str(self.post_type), post, request, False)
        response = self.prepare_item_for_response(post, request)
        return rest_ensure_response(response)
    # end def update_item
    #// 
    #// Checks if a given request has access to delete a post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_item_permissions_check(self, request=None):
        
        post = self.get_post(request["id"])
        if is_wp_error(post):
            return post
        # end if
        if post and (not self.check_delete_permission(post)):
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
    def delete_item(self, request=None):
        
        post = self.get_post(request["id"])
        if is_wp_error(post):
            return post
        # end if
        id = post.ID
        force = php_bool(request["force"])
        supports_trash = EMPTY_TRASH_DAYS > 0
        if "attachment" == post.post_type:
            supports_trash = supports_trash and MEDIA_TRASH
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
        supports_trash = apply_filters(str("rest_") + str(self.post_type) + str("_trashable"), supports_trash, post)
        if (not self.check_delete_permission(post)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_delete_post", __("Sorry, you are not allowed to delete this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        request.set_param("context", "edit")
        #// If we're forcing, then delete permanently.
        if force:
            previous = self.prepare_item_for_response(post, request)
            result = wp_delete_post(id, True)
            response = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
            response.set_data(Array({"deleted": True, "previous": previous.get_data()}))
        else:
            #// If we don't support trashing for this type, error out.
            if (not supports_trash):
                return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("The post does not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
            # end if
            #// Otherwise, only trash if we haven't already.
            if "trash" == post.post_status:
                return php_new_class("WP_Error", lambda : WP_Error("rest_already_trashed", __("The post has already been deleted."), Array({"status": 410})))
            # end if
            #// (Note that internally this falls through to `wp_delete_post()`
            #// if the Trash is disabled.)
            result = wp_trash_post(id)
            post = get_post(id)
            response = self.prepare_item_for_response(post, request)
        # end if
        if (not result):
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
        do_action(str("rest_delete_") + str(self.post_type), post, response, request)
        return response
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
    def prepare_items_query(self, prepared_args=Array(), request=None):
        
        query_args = Array()
        for key,value in prepared_args:
            #// 
            #// Filters the query_vars used in get_items() for the constructed query.
            #// 
            #// The dynamic portion of the hook name, `$key`, refers to the query_var key.
            #// 
            #// @since 4.7.0
            #// 
            #// @param string $value The query_var value.
            #//
            query_args[key] = apply_filters(str("rest_query_var-") + str(key), value)
            pass
        # end for
        if "post" != self.post_type or (not (php_isset(lambda : query_args["ignore_sticky_posts"]))):
            query_args["ignore_sticky_posts"] = True
        # end if
        #// Map to proper WP_Query orderby param.
        if (php_isset(lambda : query_args["orderby"])) and (php_isset(lambda : request["orderby"])):
            orderby_mappings = Array({"id": "ID", "include": "post__in", "slug": "post_name", "include_slugs": "post_name__in"})
            if (php_isset(lambda : orderby_mappings[request["orderby"]])):
                query_args["orderby"] = orderby_mappings[request["orderby"]]
            # end if
        # end if
        return query_args
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
    def prepare_date_response(self, date_gmt=None, date=None):
        
        #// Use the date if passed.
        if (php_isset(lambda : date)):
            return mysql_to_rfc3339(date)
        # end if
        #// Return null if $date_gmt is empty/zeros.
        if "0000-00-00 00:00:00" == date_gmt:
            return None
        # end if
        #// Return the formatted datetime.
        return mysql_to_rfc3339(date_gmt)
    # end def prepare_date_response
    #// 
    #// Prepares a single post for create or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return stdClass|WP_Error Post object or WP_Error.
    #//
    def prepare_item_for_database(self, request=None):
        
        prepared_post = php_new_class("stdClass", lambda : stdClass())
        #// Post ID.
        if (php_isset(lambda : request["id"])):
            existing_post = self.get_post(request["id"])
            if is_wp_error(existing_post):
                return existing_post
            # end if
            prepared_post.ID = existing_post.ID
        # end if
        schema = self.get_item_schema()
        #// Post title.
        if (not php_empty(lambda : schema["properties"]["title"])) and (php_isset(lambda : request["title"])):
            if php_is_string(request["title"]):
                prepared_post.post_title = request["title"]
            elif (not php_empty(lambda : request["title"]["raw"])):
                prepared_post.post_title = request["title"]["raw"]
            # end if
        # end if
        #// Post content.
        if (not php_empty(lambda : schema["properties"]["content"])) and (php_isset(lambda : request["content"])):
            if php_is_string(request["content"]):
                prepared_post.post_content = request["content"]
            elif (php_isset(lambda : request["content"]["raw"])):
                prepared_post.post_content = request["content"]["raw"]
            # end if
        # end if
        #// Post excerpt.
        if (not php_empty(lambda : schema["properties"]["excerpt"])) and (php_isset(lambda : request["excerpt"])):
            if php_is_string(request["excerpt"]):
                prepared_post.post_excerpt = request["excerpt"]
            elif (php_isset(lambda : request["excerpt"]["raw"])):
                prepared_post.post_excerpt = request["excerpt"]["raw"]
            # end if
        # end if
        #// Post type.
        if php_empty(lambda : request["id"]):
            #// Creating new post, use default type for the controller.
            prepared_post.post_type = self.post_type
        else:
            #// Updating a post, use previous type.
            prepared_post.post_type = get_post_type(request["id"])
        # end if
        post_type = get_post_type_object(prepared_post.post_type)
        #// Post status.
        if (not php_empty(lambda : schema["properties"]["status"])) and (php_isset(lambda : request["status"])):
            status = self.handle_status_param(request["status"], post_type)
            if is_wp_error(status):
                return status
            # end if
            prepared_post.post_status = status
        # end if
        #// Post date.
        if (not php_empty(lambda : schema["properties"]["date"])) and (not php_empty(lambda : request["date"])):
            current_date = get_post(prepared_post.ID).post_date if (php_isset(lambda : prepared_post.ID)) else False
            date_data = rest_get_date_with_gmt(request["date"])
            if (not php_empty(lambda : date_data)) and current_date != date_data[0]:
                prepared_post.post_date, prepared_post.post_date_gmt = date_data
                prepared_post.edit_date = True
            # end if
        elif (not php_empty(lambda : schema["properties"]["date_gmt"])) and (not php_empty(lambda : request["date_gmt"])):
            current_date = get_post(prepared_post.ID).post_date_gmt if (php_isset(lambda : prepared_post.ID)) else False
            date_data = rest_get_date_with_gmt(request["date_gmt"], True)
            if (not php_empty(lambda : date_data)) and current_date != date_data[1]:
                prepared_post.post_date, prepared_post.post_date_gmt = date_data
                prepared_post.edit_date = True
            # end if
        # end if
        #// Sending a null date or date_gmt value resets date and date_gmt to their
        #// default values (`0000-00-00 00:00:00`).
        if (not php_empty(lambda : schema["properties"]["date_gmt"])) and request.has_param("date_gmt") and None == request["date_gmt"] or (not php_empty(lambda : schema["properties"]["date"])) and request.has_param("date") and None == request["date"]:
            prepared_post.post_date_gmt = None
            prepared_post.post_date = None
        # end if
        #// Post slug.
        if (not php_empty(lambda : schema["properties"]["slug"])) and (php_isset(lambda : request["slug"])):
            prepared_post.post_name = request["slug"]
        # end if
        #// Author.
        if (not php_empty(lambda : schema["properties"]["author"])) and (not php_empty(lambda : request["author"])):
            post_author = php_int(request["author"])
            if get_current_user_id() != post_author:
                user_obj = get_userdata(post_author)
                if (not user_obj):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_author", __("Invalid author ID."), Array({"status": 400})))
                # end if
            # end if
            prepared_post.post_author = post_author
        # end if
        #// Post password.
        if (not php_empty(lambda : schema["properties"]["password"])) and (php_isset(lambda : request["password"])):
            prepared_post.post_password = request["password"]
            if "" != request["password"]:
                if (not php_empty(lambda : schema["properties"]["sticky"])) and (not php_empty(lambda : request["sticky"])):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_field", __("A post can not be sticky and have a password."), Array({"status": 400})))
                # end if
                if (not php_empty(lambda : prepared_post.ID)) and is_sticky(prepared_post.ID):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_field", __("A sticky post can not be password protected."), Array({"status": 400})))
                # end if
            # end if
        # end if
        if (not php_empty(lambda : schema["properties"]["sticky"])) and (not php_empty(lambda : request["sticky"])):
            if (not php_empty(lambda : prepared_post.ID)) and post_password_required(prepared_post.ID):
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_field", __("A password protected post can not be set to sticky."), Array({"status": 400})))
            # end if
        # end if
        #// Parent.
        if (not php_empty(lambda : schema["properties"]["parent"])) and (php_isset(lambda : request["parent"])):
            if 0 == php_int(request["parent"]):
                prepared_post.post_parent = 0
            else:
                parent = get_post(php_int(request["parent"]))
                if php_empty(lambda : parent):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid post parent ID."), Array({"status": 400})))
                # end if
                prepared_post.post_parent = php_int(parent.ID)
            # end if
        # end if
        #// Menu order.
        if (not php_empty(lambda : schema["properties"]["menu_order"])) and (php_isset(lambda : request["menu_order"])):
            prepared_post.menu_order = php_int(request["menu_order"])
        # end if
        #// Comment status.
        if (not php_empty(lambda : schema["properties"]["comment_status"])) and (not php_empty(lambda : request["comment_status"])):
            prepared_post.comment_status = request["comment_status"]
        # end if
        #// Ping status.
        if (not php_empty(lambda : schema["properties"]["ping_status"])) and (not php_empty(lambda : request["ping_status"])):
            prepared_post.ping_status = request["ping_status"]
        # end if
        if (not php_empty(lambda : schema["properties"]["template"])):
            #// Force template to null so that it can be handled exclusively by the REST controller.
            prepared_post.page_template = None
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
        return apply_filters(str("rest_pre_insert_") + str(self.post_type), prepared_post, request)
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
    def handle_status_param(self, post_status=None, post_type=None):
        
        for case in Switch(post_status):
            if case("draft"):
                pass
            # end if
            if case("pending"):
                break
            # end if
            if case("private"):
                if (not current_user_can(post_type.cap.publish_posts)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_publish", __("Sorry, you are not allowed to create private posts in this post type."), Array({"status": rest_authorization_required_code()})))
                # end if
                break
            # end if
            if case("publish"):
                pass
            # end if
            if case("future"):
                if (not current_user_can(post_type.cap.publish_posts)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_publish", __("Sorry, you are not allowed to publish posts in this post type."), Array({"status": rest_authorization_required_code()})))
                # end if
                break
            # end if
            if case():
                if (not get_post_status_object(post_status)):
                    post_status = "draft"
                # end if
                break
            # end if
        # end for
        return post_status
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
    def handle_featured_media(self, featured_media=None, post_id=None):
        
        featured_media = php_int(featured_media)
        if featured_media:
            result = set_post_thumbnail(post_id, featured_media)
            if result:
                return True
            else:
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_featured_media", __("Invalid featured media ID."), Array({"status": 400})))
            # end if
        else:
            return delete_post_thumbnail(post_id)
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
    def check_template(self, template=None, request=None):
        
        if (not template):
            return True
        # end if
        if request["id"]:
            current_template = get_page_template_slug(request["id"])
        else:
            current_template = ""
        # end if
        #// Always allow for updating a post to the same template, even if that template is no longer supported.
        if template == current_template:
            return True
        # end if
        #// If this is a create request, get_post() will return null and wp theme will fallback to the passed post type.
        allowed_templates = wp_get_theme().get_page_templates(get_post(request["id"]), self.post_type)
        if (php_isset(lambda : allowed_templates[template])):
            return True
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not one of %2$s."), "template", php_implode(", ", php_array_keys(allowed_templates)))))
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
    def handle_template(self, template=None, post_id=None, validate=False):
        
        if validate and (not php_array_key_exists(template, wp_get_theme().get_page_templates(get_post(post_id)))):
            template = ""
        # end if
        update_post_meta(post_id, "_wp_page_template", template)
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
    def handle_terms(self, post_id=None, request=None):
        
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy in taxonomies:
            base = taxonomy.rest_base if (not php_empty(lambda : taxonomy.rest_base)) else taxonomy.name
            if (not (php_isset(lambda : request[base]))):
                continue
            # end if
            result = wp_set_object_terms(post_id, request[base], taxonomy.name)
            if is_wp_error(result):
                return result
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
    def check_assign_terms_permission(self, request=None):
        
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy in taxonomies:
            base = taxonomy.rest_base if (not php_empty(lambda : taxonomy.rest_base)) else taxonomy.name
            if (not (php_isset(lambda : request[base]))):
                continue
            # end if
            for term_id in request[base]:
                #// Invalid terms will be rejected later.
                if (not get_term(term_id, taxonomy.name)):
                    continue
                # end if
                if (not current_user_can("assign_term", php_int(term_id))):
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
    def check_is_post_type_allowed(self, post_type=None):
        
        if (not php_is_object(post_type)):
            post_type = get_post_type_object(post_type)
        # end if
        if (not php_empty(lambda : post_type)) and (not php_empty(lambda : post_type.show_in_rest)):
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
    def check_read_permission(self, post=None):
        
        post_type = get_post_type_object(post.post_type)
        if (not self.check_is_post_type_allowed(post_type)):
            return False
        # end if
        #// Is the post readable?
        if "publish" == post.post_status or current_user_can(post_type.cap.read_post, post.ID):
            return True
        # end if
        post_status_obj = get_post_status_object(post.post_status)
        if post_status_obj and post_status_obj.public:
            return True
        # end if
        #// Can we read the parent if we're inheriting?
        if "inherit" == post.post_status and post.post_parent > 0:
            parent = get_post(post.post_parent)
            if parent:
                return self.check_read_permission(parent)
            # end if
        # end if
        #// 
        #// If there isn't a parent, but the status is set to inherit, assume
        #// it's published (as per get_post_status()).
        #//
        if "inherit" == post.post_status:
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
    def check_update_permission(self, post=None):
        
        post_type = get_post_type_object(post.post_type)
        if (not self.check_is_post_type_allowed(post_type)):
            return False
        # end if
        return current_user_can(post_type.cap.edit_post, post.ID)
    # end def check_update_permission
    #// 
    #// Checks if a post can be created.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return bool Whether the post can be created.
    #//
    def check_create_permission(self, post=None):
        
        post_type = get_post_type_object(post.post_type)
        if (not self.check_is_post_type_allowed(post_type)):
            return False
        # end if
        return current_user_can(post_type.cap.create_posts)
    # end def check_create_permission
    #// 
    #// Checks if a post can be deleted.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return bool Whether the post can be deleted.
    #//
    def check_delete_permission(self, post=None):
        
        post_type = get_post_type_object(post.post_type)
        if (not self.check_is_post_type_allowed(post_type)):
            return False
        # end if
        return current_user_can(post_type.cap.delete_post, post.ID)
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
    def prepare_item_for_response(self, post=None, request=None):
        global PHP_GLOBALS, self
        PHP_GLOBALS["post"] = post
        setup_postdata(post)
        fields = self.get_fields_for_response(request)
        #// Base fields for every post.
        data = Array()
        if rest_is_field_included("id", fields):
            data["id"] = post.ID
        # end if
        if rest_is_field_included("date", fields):
            data["date"] = self.prepare_date_response(post.post_date_gmt, post.post_date)
        # end if
        if rest_is_field_included("date_gmt", fields):
            #// 
            #// For drafts, `post_date_gmt` may not be set, indicating that the date
            #// of the draft should be updated each time it is saved (see #38883).
            #// In this case, shim the value based on the `post_date` field
            #// with the site's timezone offset applied.
            #//
            if "0000-00-00 00:00:00" == post.post_date_gmt:
                post_date_gmt = get_gmt_from_date(post.post_date)
            else:
                post_date_gmt = post.post_date_gmt
            # end if
            data["date_gmt"] = self.prepare_date_response(post_date_gmt)
        # end if
        if rest_is_field_included("guid", fields):
            data["guid"] = Array({"rendered": apply_filters("get_the_guid", post.guid, post.ID), "raw": post.guid})
        # end if
        if rest_is_field_included("modified", fields):
            data["modified"] = self.prepare_date_response(post.post_modified_gmt, post.post_modified)
        # end if
        if rest_is_field_included("modified_gmt", fields):
            #// 
            #// For drafts, `post_modified_gmt` may not be set (see `post_date_gmt` comments
            #// above). In this case, shim the value based on the `post_modified` field
            #// with the site's timezone offset applied.
            #//
            if "0000-00-00 00:00:00" == post.post_modified_gmt:
                post_modified_gmt = gmdate("Y-m-d H:i:s", strtotime(post.post_modified) - get_option("gmt_offset") * 3600)
            else:
                post_modified_gmt = post.post_modified_gmt
            # end if
            data["modified_gmt"] = self.prepare_date_response(post_modified_gmt)
        # end if
        if rest_is_field_included("password", fields):
            data["password"] = post.post_password
        # end if
        if rest_is_field_included("slug", fields):
            data["slug"] = post.post_name
        # end if
        if rest_is_field_included("status", fields):
            data["status"] = post.post_status
        # end if
        if rest_is_field_included("type", fields):
            data["type"] = post.post_type
        # end if
        if rest_is_field_included("link", fields):
            data["link"] = get_permalink(post.ID)
        # end if
        if rest_is_field_included("title", fields):
            data["title"] = Array()
        # end if
        if rest_is_field_included("title.raw", fields):
            data["title"]["raw"] = post.post_title
        # end if
        if rest_is_field_included("title.rendered", fields):
            add_filter("protected_title_format", Array(self, "protected_title_format"))
            data["title"]["rendered"] = get_the_title(post.ID)
            remove_filter("protected_title_format", Array(self, "protected_title_format"))
        # end if
        has_password_filter = False
        if self.can_access_password_content(post, request):
            #// Allow access to the post, permissions already checked before.
            add_filter("post_password_required", "__return_false")
            has_password_filter = True
        # end if
        if rest_is_field_included("content", fields):
            data["content"] = Array()
        # end if
        if rest_is_field_included("content.raw", fields):
            data["content"]["raw"] = post.post_content
        # end if
        if rest_is_field_included("content.rendered", fields):
            #// This filter is documented in wp-includes/post-template.php
            data["content"]["rendered"] = "" if post_password_required(post) else apply_filters("the_content", post.post_content)
        # end if
        if rest_is_field_included("content.protected", fields):
            data["content"]["protected"] = php_bool(post.post_password)
        # end if
        if rest_is_field_included("content.block_version", fields):
            data["content"]["block_version"] = block_version(post.post_content)
        # end if
        if rest_is_field_included("excerpt", fields):
            #// This filter is documented in wp-includes/post-template.php
            excerpt = apply_filters("get_the_excerpt", post.post_excerpt, post)
            #// This filter is documented in wp-includes/post-template.php
            excerpt = apply_filters("the_excerpt", excerpt)
            data["excerpt"] = Array({"raw": post.post_excerpt, "rendered": "" if post_password_required(post) else excerpt, "protected": php_bool(post.post_password)})
        # end if
        if has_password_filter:
            #// Reset filter.
            remove_filter("post_password_required", "__return_false")
        # end if
        if rest_is_field_included("author", fields):
            data["author"] = php_int(post.post_author)
        # end if
        if rest_is_field_included("featured_media", fields):
            data["featured_media"] = php_int(get_post_thumbnail_id(post.ID))
        # end if
        if rest_is_field_included("parent", fields):
            data["parent"] = php_int(post.post_parent)
        # end if
        if rest_is_field_included("menu_order", fields):
            data["menu_order"] = php_int(post.menu_order)
        # end if
        if rest_is_field_included("comment_status", fields):
            data["comment_status"] = post.comment_status
        # end if
        if rest_is_field_included("ping_status", fields):
            data["ping_status"] = post.ping_status
        # end if
        if rest_is_field_included("sticky", fields):
            data["sticky"] = is_sticky(post.ID)
        # end if
        if rest_is_field_included("template", fields):
            template = get_page_template_slug(post.ID)
            if template:
                data["template"] = template
            else:
                data["template"] = ""
            # end if
        # end if
        if rest_is_field_included("format", fields):
            data["format"] = get_post_format(post.ID)
            #// Fill in blank post format.
            if php_empty(lambda : data["format"]):
                data["format"] = "standard"
            # end if
        # end if
        if rest_is_field_included("meta", fields):
            data["meta"] = self.meta.get_value(post.ID, request)
        # end if
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy in taxonomies:
            base = taxonomy.rest_base if (not php_empty(lambda : taxonomy.rest_base)) else taxonomy.name
            if rest_is_field_included(base, fields):
                terms = get_the_terms(post, taxonomy.name)
                data[base] = php_array_values(wp_list_pluck(terms, "term_id")) if terms else Array()
            # end if
        # end for
        post_type_obj = get_post_type_object(post.post_type)
        if is_post_type_viewable(post_type_obj) and post_type_obj.public:
            permalink_template_requested = rest_is_field_included("permalink_template", fields)
            generated_slug_requested = rest_is_field_included("generated_slug", fields)
            if permalink_template_requested or generated_slug_requested:
                if (not php_function_exists("get_sample_permalink")):
                    php_include_file(ABSPATH + "wp-admin/includes/post.php", once=True)
                # end if
                sample_permalink = get_sample_permalink(post.ID, post.post_title, "")
                if permalink_template_requested:
                    data["permalink_template"] = sample_permalink[0]
                # end if
                if generated_slug_requested:
                    data["generated_slug"] = sample_permalink[1]
                # end if
            # end if
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        #// Wrap the data in a response object.
        response = rest_ensure_response(data)
        links = self.prepare_links(post)
        response.add_links(links)
        if (not php_empty(lambda : links["self"]["href"])):
            actions = self.get_available_actions(post, request)
            self = links["self"]["href"]
            for rel in actions:
                response.add_link(rel, self)
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
        return apply_filters(str("rest_prepare_") + str(self.post_type), response, post, request)
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
    def prepare_links(self, post=None):
        
        base = php_sprintf("%s/%s", self.namespace, self.rest_base)
        #// Entity meta.
        links = Array({"self": Array({"href": rest_url(trailingslashit(base) + post.ID)})}, {"collection": Array({"href": rest_url(base)})}, {"about": Array({"href": rest_url("wp/v2/types/" + self.post_type)})})
        if php_in_array(post.post_type, Array("post", "page"), True) or post_type_supports(post.post_type, "author") and (not php_empty(lambda : post.post_author)):
            links["author"] = Array({"href": rest_url("wp/v2/users/" + post.post_author), "embeddable": True})
        # end if
        if php_in_array(post.post_type, Array("post", "page"), True) or post_type_supports(post.post_type, "comments"):
            replies_url = rest_url("wp/v2/comments")
            replies_url = add_query_arg("post", post.ID, replies_url)
            links["replies"] = Array({"href": replies_url, "embeddable": True})
        # end if
        if php_in_array(post.post_type, Array("post", "page"), True) or post_type_supports(post.post_type, "revisions"):
            revisions = wp_get_post_revisions(post.ID, Array({"fields": "ids"}))
            revisions_count = php_count(revisions)
            links["version-history"] = Array({"href": rest_url(trailingslashit(base) + post.ID + "/revisions"), "count": revisions_count})
            if revisions_count > 0:
                last_revision = php_array_shift(revisions)
                links["predecessor-version"] = Array({"href": rest_url(trailingslashit(base) + post.ID + "/revisions/" + last_revision), "id": last_revision})
            # end if
        # end if
        post_type_obj = get_post_type_object(post.post_type)
        if post_type_obj.hierarchical and (not php_empty(lambda : post.post_parent)):
            links["up"] = Array({"href": rest_url(trailingslashit(base) + php_int(post.post_parent)), "embeddable": True})
        # end if
        #// If we have a featured media, add that.
        featured_media = get_post_thumbnail_id(post.ID)
        if featured_media:
            image_url = rest_url("wp/v2/media/" + featured_media)
            links["https://api.w.org/featuredmedia"] = Array({"href": image_url, "embeddable": True})
        # end if
        if (not php_in_array(post.post_type, Array("attachment", "nav_menu_item", "revision"), True)):
            attachments_url = rest_url("wp/v2/media")
            attachments_url = add_query_arg("parent", post.ID, attachments_url)
            links["https://api.w.org/attachment"] = Array({"href": attachments_url})
        # end if
        taxonomies = get_object_taxonomies(post.post_type)
        if (not php_empty(lambda : taxonomies)):
            links["https://api.w.org/term"] = Array()
            for tax in taxonomies:
                taxonomy_obj = get_taxonomy(tax)
                #// Skip taxonomies that are not public.
                if php_empty(lambda : taxonomy_obj.show_in_rest):
                    continue
                # end if
                tax_base = taxonomy_obj.rest_base if (not php_empty(lambda : taxonomy_obj.rest_base)) else tax
                terms_url = add_query_arg("post", post.ID, rest_url("wp/v2/" + tax_base))
                links["https://api.w.org/term"][-1] = Array({"href": terms_url, "taxonomy": tax, "embeddable": True})
            # end for
        # end if
        return links
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
    def get_available_actions(self, post=None, request=None):
        
        if "edit" != request["context"]:
            return Array()
        # end if
        rels = Array()
        post_type = get_post_type_object(post.post_type)
        if "attachment" != self.post_type and current_user_can(post_type.cap.publish_posts):
            rels[-1] = "https://api.w.org/action-publish"
        # end if
        if current_user_can("unfiltered_html"):
            rels[-1] = "https://api.w.org/action-unfiltered-html"
        # end if
        if "post" == post_type.name:
            if current_user_can(post_type.cap.edit_others_posts) and current_user_can(post_type.cap.publish_posts):
                rels[-1] = "https://api.w.org/action-sticky"
            # end if
        # end if
        if post_type_supports(post_type.name, "author"):
            if current_user_can(post_type.cap.edit_others_posts):
                rels[-1] = "https://api.w.org/action-assign-author"
            # end if
        # end if
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for tax in taxonomies:
            tax_base = tax.rest_base if (not php_empty(lambda : tax.rest_base)) else tax.name
            create_cap = tax.cap.edit_terms if is_taxonomy_hierarchical(tax.name) else tax.cap.assign_terms
            if current_user_can(create_cap):
                rels[-1] = "https://api.w.org/action-create-" + tax_base
            # end if
            if current_user_can(tax.cap.assign_terms):
                rels[-1] = "https://api.w.org/action-assign-" + tax_base
            # end if
        # end for
        return rels
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
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": self.post_type, "type": "object", "properties": Array({"date": Array({"description": __("The date the object was published, in the site's timezone."), "type": Array("string", "null"), "format": "date-time", "context": Array("view", "edit", "embed")})}, {"date_gmt": Array({"description": __("The date the object was published, as GMT."), "type": Array("string", "null"), "format": "date-time", "context": Array("view", "edit")})}, {"guid": Array({"description": __("The globally unique identifier for the object."), "type": "object", "context": Array("view", "edit"), "readonly": True, "properties": Array({"raw": Array({"description": __("GUID for the object, as it exists in the database."), "type": "string", "context": Array("edit"), "readonly": True})}, {"rendered": Array({"description": __("GUID for the object, transformed for display."), "type": "string", "context": Array("view", "edit"), "readonly": True})})})}, {"id": Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "edit", "embed"), "readonly": True})}, {"link": Array({"description": __("URL to the object."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed"), "readonly": True})}, {"modified": Array({"description": __("The date the object was last modified, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit"), "readonly": True})}, {"modified_gmt": Array({"description": __("The date the object was last modified, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the object unique to its type."), "type": "string", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": Array(self, "sanitize_slug")})})}, {"status": Array({"description": __("A named status for the object."), "type": "string", "enum": php_array_keys(get_post_stati(Array({"internal": False})))}, {"context": Array("view", "edit")})}, {"type": Array({"description": __("Type of Post for the object."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"password": Array({"description": __("A password to protect access to the content and excerpt."), "type": "string", "context": Array("edit")})})})
        post_type_obj = get_post_type_object(self.post_type)
        if is_post_type_viewable(post_type_obj) and post_type_obj.public:
            schema["properties"]["permalink_template"] = Array({"description": __("Permalink template for the object."), "type": "string", "context": Array("edit"), "readonly": True})
            schema["properties"]["generated_slug"] = Array({"description": __("Slug automatically generated from the object title."), "type": "string", "context": Array("edit"), "readonly": True})
        # end if
        if post_type_obj.hierarchical:
            schema["properties"]["parent"] = Array({"description": __("The ID for the parent of the object."), "type": "integer", "context": Array("view", "edit")})
        # end if
        post_type_attributes = Array("title", "editor", "author", "excerpt", "thumbnail", "comments", "revisions", "page-attributes", "post-formats", "custom-fields")
        fixed_schemas = Array({"post": Array("title", "editor", "author", "excerpt", "thumbnail", "comments", "revisions", "post-formats", "custom-fields"), "page": Array("title", "editor", "author", "excerpt", "thumbnail", "comments", "revisions", "page-attributes", "custom-fields"), "attachment": Array("title", "author", "comments", "revisions", "custom-fields")})
        for attribute in post_type_attributes:
            if (php_isset(lambda : fixed_schemas[self.post_type])) and (not php_in_array(attribute, fixed_schemas[self.post_type], True)):
                continue
            elif (not (php_isset(lambda : fixed_schemas[self.post_type]))) and (not post_type_supports(self.post_type, attribute)):
                continue
            # end if
            for case in Switch(attribute):
                if case("title"):
                    schema["properties"]["title"] = Array({"description": __("The title for the object."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Title for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML title for the object, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
                    break
                # end if
                if case("editor"):
                    schema["properties"]["content"] = Array({"description": __("The content for the object."), "type": "object", "context": Array("view", "edit"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Content for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML content for the object, transformed for display."), "type": "string", "context": Array("view", "edit"), "readonly": True})}, {"block_version": Array({"description": __("Version of the content block format used by the object."), "type": "integer", "context": Array("edit"), "readonly": True})}, {"protected": Array({"description": __("Whether the content is protected with a password."), "type": "boolean", "context": Array("view", "edit", "embed"), "readonly": True})})})
                    break
                # end if
                if case("author"):
                    schema["properties"]["author"] = Array({"description": __("The ID for the author of the object."), "type": "integer", "context": Array("view", "edit", "embed")})
                    break
                # end if
                if case("excerpt"):
                    schema["properties"]["excerpt"] = Array({"description": __("The excerpt for the object."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Excerpt for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML excerpt for the object, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"protected": Array({"description": __("Whether the excerpt is protected with a password."), "type": "boolean", "context": Array("view", "edit", "embed"), "readonly": True})})})
                    break
                # end if
                if case("thumbnail"):
                    schema["properties"]["featured_media"] = Array({"description": __("The ID of the featured media for the object."), "type": "integer", "context": Array("view", "edit", "embed")})
                    break
                # end if
                if case("comments"):
                    schema["properties"]["comment_status"] = Array({"description": __("Whether or not comments are open on the object."), "type": "string", "enum": Array("open", "closed"), "context": Array("view", "edit")})
                    schema["properties"]["ping_status"] = Array({"description": __("Whether or not the object can be pinged."), "type": "string", "enum": Array("open", "closed"), "context": Array("view", "edit")})
                    break
                # end if
                if case("page-attributes"):
                    schema["properties"]["menu_order"] = Array({"description": __("The order of the object in relation to other object of its type."), "type": "integer", "context": Array("view", "edit")})
                    break
                # end if
                if case("post-formats"):
                    #// Get the native post formats and remove the array keys.
                    formats = php_array_values(get_post_format_slugs())
                    schema["properties"]["format"] = Array({"description": __("The format for the object."), "type": "string", "enum": formats, "context": Array("view", "edit")})
                    break
                # end if
                if case("custom-fields"):
                    schema["properties"]["meta"] = self.meta.get_field_schema()
                    break
                # end if
            # end for
        # end for
        if "post" == self.post_type:
            schema["properties"]["sticky"] = Array({"description": __("Whether or not the object should be treated as sticky."), "type": "boolean", "context": Array("view", "edit")})
        # end if
        schema["properties"]["template"] = Array({"description": __("The theme file to use to display the object."), "type": "string", "context": Array("view", "edit"), "arg_options": Array({"validate_callback": Array(self, "check_template")})})
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for taxonomy in taxonomies:
            base = taxonomy.rest_base if (not php_empty(lambda : taxonomy.rest_base)) else taxonomy.name
            if php_array_key_exists(base, schema["properties"]):
                taxonomy_field_name_with_conflict = "rest_base" if (not php_empty(lambda : taxonomy.rest_base)) else "name"
                _doing_it_wrong("register_taxonomy", php_sprintf(__("The \"%1$s\" taxonomy \"%2$s\" property (%3$s) conflicts with an existing property on the REST API Posts Controller. Specify a custom \"rest_base\" when registering the taxonomy to avoid this error."), taxonomy.name, taxonomy_field_name_with_conflict, base), "5.4.0")
            # end if
            schema["properties"][base] = Array({"description": php_sprintf(__("The terms assigned to the object in the %s taxonomy."), taxonomy.name), "type": "array", "items": Array({"type": "integer"})}, {"context": Array("view", "edit")})
        # end for
        schema_links = self.get_schema_links()
        if schema_links:
            schema["links"] = schema_links
        # end if
        #// Take a snapshot of which fields are in the schema pre-filtering.
        schema_fields = php_array_keys(schema["properties"])
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
        schema = apply_filters(str("rest_") + str(self.post_type) + str("_item_schema"), schema)
        #// Emit a _doing_it_wrong warning if user tries to add new properties using this filter.
        new_fields = php_array_diff(php_array_keys(schema["properties"]), schema_fields)
        if php_count(new_fields) > 0:
            _doing_it_wrong(__METHOD__, __("Please use register_rest_field to add new schema properties."), "5.4.0")
        # end if
        self.schema = schema
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
        
        href = rest_url(str(self.namespace) + str("/") + str(self.rest_base) + str("/{id}"))
        links = Array()
        if "attachment" != self.post_type:
            links[-1] = Array({"rel": "https://api.w.org/action-publish", "title": __("The current user can publish this post."), "href": href, "targetSchema": Array({"type": "object", "properties": Array({"status": Array({"type": "string", "enum": Array("publish", "future")})})})})
        # end if
        links[-1] = Array({"rel": "https://api.w.org/action-unfiltered-html", "title": __("The current user can post unfiltered HTML markup and JavaScript."), "href": href, "targetSchema": Array({"type": "object", "properties": Array({"content": Array({"raw": Array({"type": "string"})})})})})
        if "post" == self.post_type:
            links[-1] = Array({"rel": "https://api.w.org/action-sticky", "title": __("The current user can sticky this post."), "href": href, "targetSchema": Array({"type": "object", "properties": Array({"sticky": Array({"type": "boolean"})})})})
        # end if
        if post_type_supports(self.post_type, "author"):
            links[-1] = Array({"rel": "https://api.w.org/action-assign-author", "title": __("The current user can change the author on this post."), "href": href, "targetSchema": Array({"type": "object", "properties": Array({"author": Array({"type": "integer"})})})})
        # end if
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        for tax in taxonomies:
            tax_base = tax.rest_base if (not php_empty(lambda : tax.rest_base)) else tax.name
            #// translators: %s: Taxonomy name.
            assign_title = php_sprintf(__("The current user can assign terms in the %s taxonomy."), tax.name)
            #// translators: %s: Taxonomy name.
            create_title = php_sprintf(__("The current user can create terms in the %s taxonomy."), tax.name)
            links[-1] = Array({"rel": "https://api.w.org/action-assign-" + tax_base, "title": assign_title, "href": href, "targetSchema": Array({"type": "object", "properties": Array({tax_base: Array({"type": "array", "items": Array({"type": "integer"})})})})})
            links[-1] = Array({"rel": "https://api.w.org/action-create-" + tax_base, "title": create_title, "href": href, "targetSchema": Array({"type": "object", "properties": Array({tax_base: Array({"type": "array", "items": Array({"type": "integer"})})})})})
        # end for
        return links
    # end def get_schema_links
    #// 
    #// Retrieves the query params for the posts collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Collection parameters.
    #//
    def get_collection_params(self):
        
        query_params = super().get_collection_params()
        query_params["context"]["default"] = "view"
        query_params["after"] = Array({"description": __("Limit response to posts published after a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        if post_type_supports(self.post_type, "author"):
            query_params["author"] = Array({"description": __("Limit result set to posts assigned to specific authors."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
            query_params["author_exclude"] = Array({"description": __("Ensure result set excludes posts assigned to specific authors."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        # end if
        query_params["before"] = Array({"description": __("Limit response to posts published before a given ISO8601 compliant date."), "type": "string", "format": "date-time"})
        query_params["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        if "page" == self.post_type or post_type_supports(self.post_type, "page-attributes"):
            query_params["menu_order"] = Array({"description": __("Limit result set to posts with a specific menu_order value."), "type": "integer"})
        # end if
        query_params["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "desc", "enum": Array("asc", "desc")})
        query_params["orderby"] = Array({"description": __("Sort collection by object attribute."), "type": "string", "default": "date", "enum": Array("author", "date", "id", "include", "modified", "parent", "relevance", "slug", "include_slugs", "title")})
        if "page" == self.post_type or post_type_supports(self.post_type, "page-attributes"):
            query_params["orderby"]["enum"][-1] = "menu_order"
        # end if
        post_type = get_post_type_object(self.post_type)
        if post_type.hierarchical or "attachment" == self.post_type:
            query_params["parent"] = Array({"description": __("Limit result set to items with particular parent IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
            query_params["parent_exclude"] = Array({"description": __("Limit result set to all items except those of a particular parent ID."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        # end if
        query_params["slug"] = Array({"description": __("Limit result set to posts with one or more specific slugs."), "type": "array", "items": Array({"type": "string"})}, {"sanitize_callback": "wp_parse_slug_list"})
        query_params["status"] = Array({"default": "publish", "description": __("Limit result set to posts assigned one or more statuses."), "type": "array", "items": Array({"enum": php_array_merge(php_array_keys(get_post_stati()), Array("any")), "type": "string"})}, {"sanitize_callback": Array(self, "sanitize_post_statuses")})
        taxonomies = wp_list_filter(get_object_taxonomies(self.post_type, "objects"), Array({"show_in_rest": True}))
        if (not php_empty(lambda : taxonomies)):
            query_params["tax_relation"] = Array({"description": __("Limit result set based on relationship between multiple taxonomies."), "type": "string", "enum": Array("AND", "OR")})
        # end if
        for taxonomy in taxonomies:
            base = taxonomy.rest_base if (not php_empty(lambda : taxonomy.rest_base)) else taxonomy.name
            query_params[base] = Array({"description": php_sprintf(__("Limit result set to all items that have the specified term assigned in the %s taxonomy."), base), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
            query_params[base + "_exclude"] = Array({"description": php_sprintf(__("Limit result set to all items except those that have the specified term assigned in the %s taxonomy."), base), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        # end for
        if "post" == self.post_type:
            query_params["sticky"] = Array({"description": __("Limit result set to items that are sticky."), "type": "boolean"})
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
        return apply_filters(str("rest_") + str(self.post_type) + str("_collection_params"), query_params, post_type)
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
    def sanitize_post_statuses(self, statuses=None, request=None, parameter=None):
        
        statuses = wp_parse_slug_list(statuses)
        #// The default status is different in WP_REST_Attachments_Controller.
        attributes = request.get_attributes()
        default_status = attributes["args"]["status"]["default"]
        for status in statuses:
            if status == default_status:
                continue
            # end if
            post_type_obj = get_post_type_object(self.post_type)
            if current_user_can(post_type_obj.cap.edit_posts) or "private" == status and current_user_can(post_type_obj.cap.read_private_posts):
                result = rest_validate_request_arg(status, request, parameter)
                if is_wp_error(result):
                    return result
                # end if
            else:
                return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_status", __("Status is forbidden."), Array({"status": rest_authorization_required_code()})))
            # end if
        # end for
        return statuses
    # end def sanitize_post_statuses
# end class WP_REST_Posts_Controller
