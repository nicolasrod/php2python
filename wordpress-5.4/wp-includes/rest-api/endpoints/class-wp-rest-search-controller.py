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
#// REST API: WP_REST_Search_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 5.0.0
#// 
#// 
#// Core class to search through all WordPress content via the REST API.
#// 
#// @since 5.0.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Search_Controller(WP_REST_Controller):
    PROP_ID = "id"
    PROP_TITLE = "title"
    PROP_URL = "url"
    PROP_TYPE = "type"
    PROP_SUBTYPE = "subtype"
    TYPE_ANY = "any"
    search_handlers = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array $search_handlers List of search handlers to use in the controller. Each search
    #// handler instance must extend the `WP_REST_Search_Handler` class.
    #//
    def __init__(self, search_handlers=None):
        
        self.namespace = "wp/v2"
        self.rest_base = "search"
        for search_handler in search_handlers:
            if (not type(search_handler).__name__ == "WP_REST_Search_Handler"):
                _doing_it_wrong(__METHOD__, php_sprintf(__("REST search handlers must extend the %s class."), "WP_REST_Search_Handler"), "5.0.0")
                continue
            # end if
            self.search_handlers[search_handler.get_type()] = search_handler
        # end for
    # end def __init__
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 5.0.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        register_rest_route(self.namespace, "/" + self.rest_base, Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permission_check"), "args": self.get_collection_params()}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks if a given request has access to search content.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has search access, WP_Error object otherwise.
    #//
    def get_items_permission_check(self, request=None):
        
        return True
    # end def get_items_permission_check
    #// 
    #// Retrieves a collection of search results.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request=None):
        
        handler = self.get_search_handler(request)
        if is_wp_error(handler):
            return handler
        # end if
        result = handler.search_items(request)
        if (not (php_isset(lambda : result[WP_REST_Search_Handler.RESULT_IDS]))) or (not php_is_array(result[WP_REST_Search_Handler.RESULT_IDS])) or (not (php_isset(lambda : result[WP_REST_Search_Handler.RESULT_TOTAL]))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_search_handler_error", __("Internal search handler error."), Array({"status": 500})))
        # end if
        ids = php_array_map("absint", result[WP_REST_Search_Handler.RESULT_IDS])
        results = Array()
        for id in ids:
            data = self.prepare_item_for_response(id, request)
            results[-1] = self.prepare_response_for_collection(data)
        # end for
        total = php_int(result[WP_REST_Search_Handler.RESULT_TOTAL])
        page = php_int(request["page"])
        per_page = php_int(request["per_page"])
        max_pages = ceil(total / per_page)
        if page > max_pages and total > 0:
            return php_new_class("WP_Error", lambda : WP_Error("rest_search_invalid_page_number", __("The page number requested is larger than the number of pages available."), Array({"status": 400})))
        # end if
        response = rest_ensure_response(results)
        response.header("X-WP-Total", total)
        response.header("X-WP-TotalPages", max_pages)
        request_params = request.get_query_params()
        base = add_query_arg(urlencode_deep(request_params), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
        if page > 1:
            prev_link = add_query_arg("page", page - 1, base)
            response.link_header("prev", prev_link)
        # end if
        if page < max_pages:
            next_link = add_query_arg("page", page + 1, base)
            response.link_header("next", next_link)
        # end if
        return response
    # end def get_items
    #// 
    #// Prepares a single search result for response.
    #// 
    #// @since 5.0.0
    #// 
    #// @param int             $id      ID of the item to prepare.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, id=None, request=None):
        
        handler = self.get_search_handler(request)
        if is_wp_error(handler):
            return php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        # end if
        fields = self.get_fields_for_response(request)
        data = handler.prepare_item(id, fields)
        data = self.add_additional_fields_to_object(data, request)
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.filter_response_by_context(data, context)
        response = rest_ensure_response(data)
        links = handler.prepare_item_links(id)
        links["collection"] = Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})
        response.add_links(links)
        return response
    # end def prepare_item_for_response
    #// 
    #// Retrieves the item schema, conforming to JSON Schema.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        types = Array()
        subtypes = Array()
        for search_handler in self.search_handlers:
            types[-1] = search_handler.get_type()
            subtypes = php_array_merge(subtypes, search_handler.get_subtypes())
        # end for
        types = array_unique(types)
        subtypes = array_unique(subtypes)
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "search-result", "type": "object", "properties": Array({self.PROP_ID: Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "embed"), "readonly": True})}, {self.PROP_TITLE: Array({"description": __("The title for the object."), "type": "string", "context": Array("view", "embed"), "readonly": True})}, {self.PROP_URL: Array({"description": __("URL to the object."), "type": "string", "format": "uri", "context": Array("view", "embed"), "readonly": True})}, {self.PROP_TYPE: Array({"description": __("Object type."), "type": "string", "enum": types, "context": Array("view", "embed"), "readonly": True})}, {self.PROP_SUBTYPE: Array({"description": __("Object subtype."), "type": "string", "enum": subtypes, "context": Array("view", "embed"), "readonly": True})})})
        self.schema = schema
        return self.add_additional_fields_schema(self.schema)
    # end def get_item_schema
    #// 
    #// Retrieves the query params for the search results collection.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Collection parameters.
    #//
    def get_collection_params(self):
        
        types = Array()
        subtypes = Array()
        for search_handler in self.search_handlers:
            types[-1] = search_handler.get_type()
            subtypes = php_array_merge(subtypes, search_handler.get_subtypes())
        # end for
        types = array_unique(types)
        subtypes = array_unique(subtypes)
        query_params = super().get_collection_params()
        query_params["context"]["default"] = "view"
        query_params[self.PROP_TYPE] = Array({"default": types[0], "description": __("Limit results to items of an object type."), "type": "string", "enum": types})
        query_params[self.PROP_SUBTYPE] = Array({"default": self.TYPE_ANY, "description": __("Limit results to items of one or more object subtypes."), "type": "array", "items": Array({"enum": php_array_merge(subtypes, Array(self.TYPE_ANY)), "type": "string"})}, {"sanitize_callback": Array(self, "sanitize_subtypes")})
        return query_params
    # end def get_collection_params
    #// 
    #// Sanitizes the list of subtypes, to ensure only subtypes of the passed type are included.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string|array    $subtypes  One or more subtypes.
    #// @param WP_REST_Request $request   Full details about the request.
    #// @param string          $parameter Parameter name.
    #// @return array|WP_Error List of valid subtypes, or WP_Error object on failure.
    #//
    def sanitize_subtypes(self, subtypes=None, request=None, parameter=None):
        
        subtypes = wp_parse_slug_list(subtypes)
        subtypes = rest_parse_request_arg(subtypes, request, parameter)
        if is_wp_error(subtypes):
            return subtypes
        # end if
        #// 'any' overrides any other subtype.
        if php_in_array(self.TYPE_ANY, subtypes, True):
            return Array(self.TYPE_ANY)
        # end if
        handler = self.get_search_handler(request)
        if is_wp_error(handler):
            return handler
        # end if
        return php_array_intersect(subtypes, handler.get_subtypes())
    # end def sanitize_subtypes
    #// 
    #// Gets the search handler to handle the current request.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Search_Handler|WP_Error Search handler for the request type, or WP_Error object on failure.
    #//
    def get_search_handler(self, request=None):
        
        type = request.get_param(self.PROP_TYPE)
        if (not type) or (not (php_isset(lambda : self.search_handlers[type]))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_search_invalid_type", __("Invalid type parameter."), Array({"status": 400})))
        # end if
        return self.search_handlers[type]
    # end def get_search_handler
# end class WP_REST_Search_Controller
