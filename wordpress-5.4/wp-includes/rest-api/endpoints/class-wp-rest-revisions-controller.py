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
    parent_post_type = Array()
    parent_controller = Array()
    parent_base = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $parent_post_type Post type of the parent.
    #//
    def __init__(self, parent_post_type=None):
        
        self.parent_post_type = parent_post_type
        self.namespace = "wp/v2"
        self.rest_base = "revisions"
        post_type_object = get_post_type_object(parent_post_type)
        self.parent_base = post_type_object.rest_base if (not php_empty(lambda : post_type_object.rest_base)) else post_type_object.name
        self.parent_controller = post_type_object.get_rest_controller()
        if (not self.parent_controller):
            self.parent_controller = php_new_class("WP_REST_Posts_Controller", lambda : WP_REST_Posts_Controller(parent_post_type))
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
    def get_parent(self, parent=None):
        
        error = php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_parent", __("Invalid post parent ID."), Array({"status": 404})))
        if int(parent) <= 0:
            return error
        # end if
        parent = get_post(int(parent))
        if php_empty(lambda : parent) or php_empty(lambda : parent.ID) or self.parent_post_type != parent.post_type:
            return error
        # end if
        return parent
    # end def get_parent
    #// 
    #// Checks if a given request has access to get revisions.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request=None):
        
        parent = self.get_parent(request["parent"])
        if is_wp_error(parent):
            return parent
        # end if
        parent_post_type_obj = get_post_type_object(parent.post_type)
        if (not current_user_can(parent_post_type_obj.cap.edit_post, parent.ID)):
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
    def get_revision(self, id=None):
        
        error = php_new_class("WP_Error", lambda : WP_Error("rest_post_invalid_id", __("Invalid revision ID."), Array({"status": 404})))
        if int(id) <= 0:
            return error
        # end if
        revision = get_post(int(id))
        if php_empty(lambda : revision) or php_empty(lambda : revision.ID) or "revision" != revision.post_type:
            return error
        # end if
        return revision
    # end def get_revision
    #// 
    #// Gets a collection of revisions.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request=None):
        
        parent = self.get_parent(request["parent"])
        if is_wp_error(parent):
            return parent
        # end if
        #// Ensure a search string is set in case the orderby is set to 'relevance'.
        if (not php_empty(lambda : request["orderby"])) and "relevance" == request["orderby"] and php_empty(lambda : request["search"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_no_search_term_defined", __("You need to define a search term to order by relevance."), Array({"status": 400})))
        # end if
        #// Ensure an include parameter is set in case the orderby is set to 'include'.
        if (not php_empty(lambda : request["orderby"])) and "include" == request["orderby"] and php_empty(lambda : request["include"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_orderby_include_missing_include", __("You need to define an include parameter to order by include."), Array({"status": 400})))
        # end if
        if wp_revisions_enabled(parent):
            registered = self.get_collection_params()
            args = Array({"post_parent": parent.ID, "post_type": "revision", "post_status": "inherit", "posts_per_page": -1, "orderby": "date ID", "order": "DESC", "suppress_filters": True})
            parameter_mappings = Array({"exclude": "post__not_in", "include": "post__in", "offset": "offset", "order": "order", "orderby": "orderby", "page": "paged", "per_page": "posts_per_page", "search": "s"})
            for api_param,wp_param in parameter_mappings:
                if (php_isset(lambda : registered[api_param]) and php_isset(lambda : request[api_param])):
                    args[wp_param] = request[api_param]
                # end if
            # end for
            #// For backward-compatibility, 'date' needs to resolve to 'date ID'.
            if (php_isset(lambda : args["orderby"])) and "date" == args["orderby"]:
                args["orderby"] = "date ID"
            # end if
            #// This filter is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
            args = apply_filters("rest_revision_query", args, request)
            query_args = self.prepare_items_query(args, request)
            revisions_query = php_new_class("WP_Query", lambda : WP_Query())
            revisions = revisions_query.query(query_args)
            offset = int(query_args["offset"]) if (php_isset(lambda : query_args["offset"])) else 0
            page = int(query_args["paged"])
            total_revisions = revisions_query.found_posts
            if total_revisions < 1:
                query_args["paged"] = None
                query_args["offset"] = None
                count_query = php_new_class("WP_Query", lambda : WP_Query())
                count_query.query(query_args)
                total_revisions = count_query.found_posts
            # end if
            if revisions_query.query_vars["posts_per_page"] > 0:
                max_pages = ceil(total_revisions / int(revisions_query.query_vars["posts_per_page"]))
            else:
                max_pages = 1 if total_revisions > 0 else 0
            # end if
            if total_revisions > 0:
                if offset >= total_revisions:
                    return php_new_class("WP_Error", lambda : WP_Error("rest_revision_invalid_offset_number", __("The offset number requested is larger than or equal to the number of available revisions."), Array({"status": 400})))
                elif (not offset) and page > max_pages:
                    return php_new_class("WP_Error", lambda : WP_Error("rest_revision_invalid_page_number", __("The page number requested is larger than the number of pages available."), Array({"status": 400})))
                # end if
            # end if
        else:
            revisions = Array()
            total_revisions = 0
            max_pages = 0
            page = int(request["page"])
        # end if
        response = Array()
        for revision in revisions:
            data = self.prepare_item_for_response(revision, request)
            response[-1] = self.prepare_response_for_collection(data)
        # end for
        response = rest_ensure_response(response)
        response.header("X-WP-Total", int(total_revisions))
        response.header("X-WP-TotalPages", int(max_pages))
        request_params = request.get_query_params()
        base = add_query_arg(urlencode_deep(request_params), rest_url(php_sprintf("%s/%s/%d/%s", self.namespace, self.parent_base, request["parent"], self.rest_base)))
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
    #// Checks if a given request has access to get a specific revision.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has read access for the item, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request=None):
        
        return self.get_items_permissions_check(request)
    # end def get_item_permissions_check
    #// 
    #// Retrieves one revision from the collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request=None):
        
        parent = self.get_parent(request["parent"])
        if is_wp_error(parent):
            return parent
        # end if
        parent_post_type = get_post_type_object(parent.post_type)
        if (not current_user_can(parent_post_type.cap.delete_post, parent.ID)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("Sorry, you are not allowed to delete revisions of this post."), Array({"status": rest_authorization_required_code()})))
        # end if
        revision = self.get_revision(request["id"])
        if is_wp_error(revision):
            return revision
        # end if
        response = self.prepare_item_for_response(revision, request)
        return rest_ensure_response(response)
    # end def get_item
    #// 
    #// Checks if a given request has access to delete a revision.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_item_permissions_check(self, request=None):
        
        parent = self.get_parent(request["parent"])
        if is_wp_error(parent):
            return parent
        # end if
        revision = self.get_revision(request["id"])
        if is_wp_error(revision):
            return revision
        # end if
        response = self.get_items_permissions_check(request)
        if (not response) or is_wp_error(response):
            return response
        # end if
        post_type = get_post_type_object("revision")
        if (not current_user_can(post_type.cap.delete_post, revision.ID)):
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
    def delete_item(self, request=None):
        
        revision = self.get_revision(request["id"])
        if is_wp_error(revision):
            return revision
        # end if
        force = bool(request["force"]) if (php_isset(lambda : request["force"])) else False
        #// We don't support trashing for revisions.
        if (not force):
            return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("Revisions do not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
        # end if
        previous = self.prepare_item_for_response(revision, request)
        result = wp_delete_post(request["id"], True)
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
        do_action("rest_delete_revision", result, request)
        if (not result):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The post cannot be deleted."), Array({"status": 500})))
        # end if
        response = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        response.set_data(Array({"deleted": True, "previous": previous.get_data()}))
        return response
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
    def prepare_items_query(self, prepared_args=Array(), request=None):
        
        query_args = Array()
        for key,value in prepared_args:
            #// This filter is documented in wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
            query_args[key] = apply_filters(str("rest_query_var-") + str(key), value)
            pass
        # end for
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
    #// Prepares the revision for the REST response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post         $post    Post revision object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, post=None, request=None):
        global PHP_GLOBALS
        PHP_GLOBALS["post"] = post
        setup_postdata(post)
        fields = self.get_fields_for_response(request)
        data = Array()
        if php_in_array("author", fields, True):
            data["author"] = int(post.post_author)
        # end if
        if php_in_array("date", fields, True):
            data["date"] = self.prepare_date_response(post.post_date_gmt, post.post_date)
        # end if
        if php_in_array("date_gmt", fields, True):
            data["date_gmt"] = self.prepare_date_response(post.post_date_gmt)
        # end if
        if php_in_array("id", fields, True):
            data["id"] = post.ID
        # end if
        if php_in_array("modified", fields, True):
            data["modified"] = self.prepare_date_response(post.post_modified_gmt, post.post_modified)
        # end if
        if php_in_array("modified_gmt", fields, True):
            data["modified_gmt"] = self.prepare_date_response(post.post_modified_gmt)
        # end if
        if php_in_array("parent", fields, True):
            data["parent"] = int(post.post_parent)
        # end if
        if php_in_array("slug", fields, True):
            data["slug"] = post.post_name
        # end if
        if php_in_array("guid", fields, True):
            data["guid"] = Array({"rendered": apply_filters("get_the_guid", post.guid, post.ID), "raw": post.guid})
        # end if
        if php_in_array("title", fields, True):
            data["title"] = Array({"raw": post.post_title, "rendered": get_the_title(post.ID)})
        # end if
        if php_in_array("content", fields, True):
            data["content"] = Array({"raw": post.post_content, "rendered": apply_filters("the_content", post.post_content)})
        # end if
        if php_in_array("excerpt", fields, True):
            data["excerpt"] = Array({"raw": post.post_excerpt, "rendered": self.prepare_excerpt_response(post.post_excerpt, post)})
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        response = rest_ensure_response(data)
        if (not php_empty(lambda : data["parent"])):
            response.add_link("parent", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.parent_base, data["parent"])))
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
        return apply_filters("rest_prepare_revision", response, post, request)
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
    def prepare_date_response(self, date_gmt=None, date=None):
        
        if "0000-00-00 00:00:00" == date_gmt:
            return None
        # end if
        if (php_isset(lambda : date)):
            return mysql_to_rfc3339(date)
        # end if
        return mysql_to_rfc3339(date_gmt)
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
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": str(self.parent_post_type) + str("-revision"), "type": "object", "properties": Array({"author": Array({"description": __("The ID for the author of the object."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"date": Array({"description": __("The date the object was published, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit", "embed")})}, {"date_gmt": Array({"description": __("The date the object was published, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"guid": Array({"description": __("GUID for the object, as it exists in the database."), "type": "string", "context": Array("view", "edit")})}, {"id": Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"modified": Array({"description": __("The date the object was last modified, in the site's timezone."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"modified_gmt": Array({"description": __("The date the object was last modified, as GMT."), "type": "string", "format": "date-time", "context": Array("view", "edit")})}, {"parent": Array({"description": __("The ID for the parent of the object."), "type": "integer", "context": Array("view", "edit", "embed")})}, {"slug": Array({"description": __("An alphanumeric identifier for the object unique to its type."), "type": "string", "context": Array("view", "edit", "embed")})})})
        parent_schema = self.parent_controller.get_item_schema()
        if (not php_empty(lambda : parent_schema["properties"]["title"])):
            schema["properties"]["title"] = parent_schema["properties"]["title"]
        # end if
        if (not php_empty(lambda : parent_schema["properties"]["content"])):
            schema["properties"]["content"] = parent_schema["properties"]["content"]
        # end if
        if (not php_empty(lambda : parent_schema["properties"]["excerpt"])):
            schema["properties"]["excerpt"] = parent_schema["properties"]["excerpt"]
        # end if
        if (not php_empty(lambda : parent_schema["properties"]["guid"])):
            schema["properties"]["guid"] = parent_schema["properties"]["guid"]
        # end if
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
        query_params["per_page"]["default"] = None
        query_params["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        query_params["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "desc", "enum": Array("asc", "desc")})
        query_params["orderby"] = Array({"description": __("Sort collection by object attribute."), "type": "string", "default": "date", "enum": Array("date", "id", "include", "relevance", "slug", "include_slugs", "title")})
        return query_params
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
    def prepare_excerpt_response(self, excerpt=None, post=None):
        
        #// This filter is documented in wp-includes/post-template.php
        excerpt = apply_filters("the_excerpt", excerpt, post)
        if php_empty(lambda : excerpt):
            return ""
        # end if
        return excerpt
    # end def prepare_excerpt_response
# end class WP_REST_Revisions_Controller
