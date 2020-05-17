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
#// REST API: WP_REST_Revisions_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to access revisions via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Revisions_Controller(WP_REST_Controller):
    #// 
    #// Parent post type.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    parent_post_type = Array()
    #// 
    #// Parent controller.
    #// 
    #// @since 4.7.0
    #// @var WP_REST_Controller
    #//
    parent_controller = Array()
    #// 
    #// The base of the parent controller's route.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    parent_base = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $parent_post_type Post type of the parent.
    #//
    def __init__(self, parent_post_type_=None):
        
        
        self.parent_post_type = parent_post_type_
        self.namespace = "wp/v2"
        self.rest_base = "revisions"
        post_type_object_ = get_post_type_object(parent_post_type_)
        self.parent_base = post_type_object_.rest_base if (not php_empty(lambda : post_type_object_.rest_base)) else post_type_object_.name
        self.parent_controller = post_type_object_.get_rest_controller()
        if (not self.parent_controller):
            self.parent_controller = php_new_class("WP_REST_Posts_Controller", lambda : WP_REST_Posts_Controller(parent_post_type_))
        # end if
    # end def __init__
    #// 
    #// Registers the routes for revisions based on post types supporting revisions.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        
        register_rest_route(self.namespace, "/" + self.parent_base + "/(?P<parent>[\\d]+)/" + self.rest_base, Array({"args": Array({"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permissions_check"), "args": self.get_collection_params()}), {"schema": Array(self, "get_public_item_schema")}))
        register_rest_route(self.namespace, "/" + self.parent_base + "/(?P<parent>[\\d]+)/" + self.rest_base + "/(?P<id>[\\d]+)", Array({"args": Array({"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer"})}, {"id": Array({"description": __("Unique identifier for the object."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), Array({"methods": WP_REST_Server.DELETABLE, "callback": Array(self, "delete_item"), "permission_callback": Array(self, "delete_item_permissions_check"), "args": Array({"force": Array({"type": "boolean", "default": False, "description": __("Required to be true, as revisions do not support trashing.")})})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Get the parent post, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $parent Supplied ID.
    #// @return WP_Post|WP_Error Post object if ID is valid, WP_Error otherwise.
    #//
    def get_parent(self, parent_=None):
        
        
        error_ = php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_parent", __("Invalid post parent ID."), Array({"status": 404})))
        if php_int(parent_) <= 0:
            return error_
        # end if
        parent_ = get_post(php_int(parent_))
        if php_empty(lambda : parent_) or php_empty(lambda : parent_.ID) or self.parent_post_type != parent_.post_type:
            return error_
        # end if
        return parent_
    # end def get_parent
    #// 
    #// Checks if a given request has access to get revisions.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request_=None):
        
        
        parent_ = self.get_parent(request_["parent"])
        if is_wp_error(parent_):
            return parent_
        # end if
        parent_post_type_obj_ = get_post_type_object(parent_.post_type)
        if (not current_user_can(parent_post_type_obj_.cap.edit_post, parent_.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_read", __("Sorry, you are not allowed to view revisions of this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Get the revision, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_Post|WP_Error Revision post object if ID is valid, WP_Error otherwise.
    #//
    def get_revision(self, id_=None):
        
        
        error_ = php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid revision ID."), Array({"status": 404})))
        if php_int(id_) <= 0:
            return error_
        # end if
        revision_ = get_post(php_int(id_))
        if php_empty(lambda : revision_) or php_empty(lambda : revision_.ID) or "revision" != revision_.post_type:
            return error_
        # end if
        return revision_
    # end def get_revision
    #// 
    #// Gets a collection of revisions.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request_=None):
        
        
        parent_ = self.get_parent(request_["parent"])
        if is_wp_error(parent_):
            return parent_
        # end if
        #// Ensure a search string is set in case the orderby is set to 'relevance'.
        if (not php_empty(lambda : request_["orderby"])) and "relevance" == request_["orderby"] and php_empty(lambda : request_["search"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_no_search_term_defined", __("You need to define a search term to order by relevance."), Array({"status": 400})))
        # end if
        #// Ensure an include parameter is set in case the orderby is set to 'include'.
        if (not php_empty(lambda : request_["orderby"])) and "include" == request_["orderby"] and php_empty(lambda : request_["include"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_orderby_include_missing_include", __("You need to define an include parameter to order by include."), Array({"status": 400})))
        # end if
        if wp_revisions_enabled(parent_):
            registered_ = self.get_collection_params()
            args_ = Array({"post_parent": parent_.ID, "post_type": "revision", "post_status": "inherit", "posts_per_page": -1, "orderby": "date ID", "order": "DESC", "suppress_filters": True})
            parameter_mappings_ = Array({"exclude": "post__not_in", "include": "post__in", "offset": "offset", "order": "order", "orderby": "orderby", "page": "paged", "per_page": "posts_per_page", "search": "s"})
            for api_param_,wp_param_ in parameter_mappings_:
                if (php_isset(lambda : registered_[api_param_]) and php_isset(lambda : request_[api_param_])):
                    args_[wp_param_] = request_[api_param_]
                # end if
            # end for
            #// For backward-compatibility, 'date' needs to resolve to 'date ID'.
            if (php_isset(lambda : args_["orderby"])) and "date" == args_["orderby"]:
                args_["orderby"] = "date ID"
            # end if
            #// This filter is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
            args_ = apply_filters("rest_revision_query", args_, request_)
            query_args_ = self.prepare_items_query(args_, request_)
            revisions_query_ = php_new_class("WP_Query", lambda : WP_Query())
            revisions_ = revisions_query_.query(query_args_)
            offset_ = php_int(query_args_["offset"]) if (php_isset(lambda : query_args_["offset"])) else 0
            page_ = php_int(query_args_["paged"])
            total_revisions_ = revisions_query_.found_posts
            if total_revisions_ < 1:
                query_args_["paged"] = None
                query_args_["offset"] = None
                count_query_ = php_new_class("WP_Query", lambda : WP_Query())
                count_query_.query(query_args_)
                total_revisions_ = count_query_.found_posts
            # end if
            if revisions_query_.query_vars["posts_per_page"] > 0:
                max_pages_ = ceil(total_revisions_ / php_int(revisions_query_.query_vars["posts_per_page"]))
            else:
                max_pages_ = 1 if total_revisions_ > 0 else 0
            # end if
            if total_revisions_ > 0:
                if offset_ >= total_revisions_:
                    return php_new_class("WP_Error", lambda : WP_Error("rest_revision_invalid_offset_number", __("The offset number requested is larger than or equal to the number of available revisions."), Array({"status": 400})))
                elif (not offset_) and page_ > max_pages_:
                    return php_new_class("WP_Error", lambda : WP_Error("rest_revision_invalid_page_number", __("The page number requested is larger than the number of pages available."), Array({"status": 400})))
                # end if
            # end if
        else:
            revisions_ = Array()
            total_revisions_ = 0
            max_pages_ = 0
            page_ = php_int(request_["page"])
        # end if
        response_ = Array()
        for revision_ in revisions_:
            data_ = self.prepare_item_for_response(revision_, request_)
            response_[-1] = self.prepare_response_for_collection(data_)
        # end for
        response_ = rest_ensure_response(response_)
        response_.header("X-WP-Total", php_int(total_revisions_))
        response_.header("X-WP-TotalPages", php_int(max_pages_))
        request_params_ = request_.get_query_params()
        base_ = add_query_arg(urlencode_deep(request_params_), rest_url(php_sprintf("%s/%s/%d/%s", self.namespace, self.parent_base, request_["parent"], self.rest_base)))
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
    #// Checks if a given request has access to get a specific revision.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has read access for the item, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        return self.get_items_permissions_check(request_)
    # end def get_item_permissions_check
    #// 
    #// Retrieves one revision from the collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request_=None):
        
        
        parent_ = self.get_parent(request_["parent"])
        if is_wp_error(parent_):
            return parent_
        # end if
        parent_post_type_ = get_post_type_object(parent_.post_type)
        if (not current_user_can(parent_post_type_.cap.delete_post, parent_.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("Sorry, you are not allowed to delete revisions of this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        revision_ = self.get_revision(request_["id"])
        if is_wp_error(revision_):
            return revision_
        # end if
        response_ = self.prepare_item_for_response(revision_, request_)
        return rest_ensure_response(response_)
    # end def get_item
    #// 
    #// Checks if a given request has access to delete a revision.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_item_permissions_check(self, request_=None):
        
        
        parent_ = self.get_parent(request_["parent"])
        if is_wp_error(parent_):
            return parent_
        # end if
        revision_ = self.get_revision(request_["id"])
        if is_wp_error(revision_):
            return revision_
        # end if
        response_ = self.get_items_permissions_check(request_)
        if (not response_) or is_wp_error(response_):
            return response_
        # end if
        post_type_ = get_post_type_object("revision")
        if (not current_user_can(post_type_.cap.delete_post, revision_.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("Sorry, you are not allowed to delete this revision."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def delete_item_permissions_check
    #// 
    #// Deletes a single revision.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True on success, or WP_Error object on failure.
    #//
    def delete_item(self, request_=None):
        
        
        revision_ = self.get_revision(request_["id"])
        if is_wp_error(revision_):
            return revision_
        # end if
        force_ = php_bool(request_["force"]) if (php_isset(lambda : request_["force"])) else False
        #// We don't support trashing for revisions.
        if (not force_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("Revisions do not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
        # end if
        previous_ = self.prepare_item_for_response(revision_, request_)
        result_ = wp_delete_post(request_["id"], True)
        #// 
        #// Fires after a revision is deleted via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Post|false|null $result The revision object (if it was deleted or moved to the Trash successfully)
        #// or false or null (failure). If the revision was moved to the Trash, $result represents
        #// its new state; if it was deleted, $result represents its state before deletion.
        #// @param WP_REST_Request $request The request sent to the API.
        #//
        do_action("rest_delete_revision", result_, request_)
        if (not result_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The post cannot be deleted."), Array({"status": 500})))
        # end if
        response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        response_.set_data(Array({"deleted": True, "previous": previous_.get_data()}))
        return response_
    # end def delete_item
    #// 
    #// Determines the allowed query_vars for a get_items() response and prepares
    #// them for WP_Query.
    #// 
    #// @since 5.0.0
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
        for key_,value_ in prepared_args_:
            #// This filter is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
            query_args_[key_] = apply_filters(str("rest_query_var-") + str(key_), value_)
            pass
        # end for
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
    #// Prepares the revision for the REST response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post         $post    Post revision object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, post_=None, request_=None):
        
        global PHP_GLOBALS
        PHP_GLOBALS["post"] = post_
        setup_postdata(post_)
        fields_ = self.get_fields_for_response(request_)
        data_ = Array()
        if php_in_array("author", fields_, True):
            data_["author"] = php_int(post_.post_author)
        # end if
        if php_in_array("date", fields_, True):
            data_["date"] = self.prepare_date_response(post_.post_date_gmt, post_.post_date)
        # end if
        if php_in_array("date_gmt", fields_, True):
            data_["date_gmt"] = self.prepare_date_response(post_.post_date_gmt)
        # end if
        if php_in_array("id", fields_, True):
            data_["id"] = post_.ID
        # end if
        if php_in_array("modified", fields_, True):
            data_["modified"] = self.prepare_date_response(post_.post_modified_gmt, post_.post_modified)
        # end if
        if php_in_array("modified_gmt", fields_, True):
            data_["modified_gmt"] = self.prepare_date_response(post_.post_modified_gmt)
        # end if
        if php_in_array("parent", fields_, True):
            data_["parent"] = php_int(post_.post_parent)
        # end if
        if php_in_array("slug", fields_, True):
            data_["slug"] = post_.post_name
        # end if
        if php_in_array("guid", fields_, True):
            data_["guid"] = Array({"rendered": apply_filters("get_the_guid", post_.guid, post_.ID), "raw": post_.guid})
        # end if
        if php_in_array("title", fields_, True):
            data_["title"] = Array({"raw": post_.post_title, "rendered": get_the_title(post_.ID)})
        # end if
        if php_in_array("content", fields_, True):
            data_["content"] = Array({"raw": post_.post_content, "rendered": apply_filters("the_content", post_.post_content)})
        # end if
        if php_in_array("excerpt", fields_, True):
            data_["excerpt"] = Array({"raw": post_.post_excerpt, "rendered": self.prepare_excerpt_response(post_.post_excerpt, post_)})
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        response_ = rest_ensure_response(data_)
        if (not php_empty(lambda : data_["parent"])):
            response_.add_link("parent", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.parent_base, data_["parent"])))
        # end if
        #// 
        #// Filters a revision returned from the API.
        #// 
        #// Allows modification of the revision right before it is returned.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_Post          $post     The original revision object.
        #// @param WP_REST_Request  $request  Request used to generate the response.
        #//
        return apply_filters("rest_prepare_revision", response_, post_, request_)
    # end def prepare_item_for_response
    #// 
    #// Checks the post_date_gmt or modified_gmt and prepare any post or
    #// modified date for single post output.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string      $date_gmt GMT publication time.
    #// @param string|null $date     Optional. Local publication time. Default null.
    #// @return string|null ISO8601/RFC3339 formatted datetime, otherwise null.
    #//
    def prepare_date_response(self, date_gmt_=None, date_=None):
        if date_ is None:
            date_ = None
        # end if
        
        if "0000-00-00 00:00:00" == date_gmt_:
            return None
        # end if
        if (php_isset(lambda : date_)):
            return mysql_to_rfc3339(date_)
        # end if
        return mysql_to_rfc3339(date_gmt_)
    # end def prepare_date_response
    #// 
    #// Retrieves the revision's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": str(self.parent_post_type) + str("-revision"), "type": "object", "properties": Array({"author": Array({"description": __("The ID for the author of the object."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"date": Array({"description": __("The date the object was published, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit", "embed")})}, {"date_gmt": Array({"description": __("The date the object was published, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"guid": Array({"description": __("GUID for the object, as it exists in the database."), "type": "string", "context": Array("view", "edit")})}, {"id": Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"modified": Array({"description": __("The date the object was last modified, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"modified_gmt": Array({"description": __("The date the object was last modified, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"slug": Array({"description": __("An alphanumeric identifier for the object unique to its type."), "type": "string", "context": Array("view", "edit", "embed")})})})
        parent_schema_ = self.parent_controller.get_item_schema()
        if (not php_empty(lambda : parent_schema_["properties"]["title"])):
            schema_["properties"]["title"] = parent_schema_["properties"]["title"]
        # end if
        if (not php_empty(lambda : parent_schema_["properties"]["content"])):
            schema_["properties"]["content"] = parent_schema_["properties"]["content"]
        # end if
        if (not php_empty(lambda : parent_schema_["properties"]["excerpt"])):
            schema_["properties"]["excerpt"] = parent_schema_["properties"]["excerpt"]
        # end if
        if (not php_empty(lambda : parent_schema_["properties"]["guid"])):
            schema_["properties"]["guid"] = parent_schema_["properties"]["guid"]
        # end if
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
        query_params_["per_page"]["default"] = None
        query_params_["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params_["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "desc", "enum": Array("asc", "desc")})
        query_params_["orderby"] = Array({"description": __("Sort collection by object attribute."), "type": "string", "default": "date", "enum": Array("date", "id", "include", "relevance", "slug", "include_slugs", "title")})
        return query_params_
    # end def get_collection_params
    #// 
    #// Checks the post excerpt and prepare it for single post output.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string  $excerpt The post excerpt.
    #// @param WP_Post $post    Post revision object.
    #// @return string Prepared excerpt or empty string.
    #//
    def prepare_excerpt_response(self, excerpt_=None, post_=None):
        
        
        #// This filter is documented in wp-includes/post-template.php
        excerpt_ = apply_filters("the_excerpt", excerpt_, post_)
        if php_empty(lambda : excerpt_):
            return ""
        # end if
        return excerpt_
    # end def prepare_excerpt_response
# end class WP_REST_Revisions_Controller
