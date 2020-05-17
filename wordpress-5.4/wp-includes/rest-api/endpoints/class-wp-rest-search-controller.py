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
    #// 
    #// Search handlers used by the controller.
    #// 
    #// @since 5.0.0
    #// @var array
    #//
    search_handlers = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array $search_handlers List of search handlers to use in the controller. Each search
    #// handler instance must extend the `WP_REST_Search_Handler` class.
    #//
    def __init__(self, search_handlers_=None):
        
        
        self.namespace = "wp/v2"
        self.rest_base = "search"
        for search_handler_ in search_handlers_:
            if (not type(search_handler_).__name__ == "WP_REST_Search_Handler"):
                _doing_it_wrong(__METHOD__, php_sprintf(__("REST search handlers must extend the %s class."), "WP_REST_Search_Handler"), "5.0.0")
                continue
            # end if
            self.search_handlers[search_handler_.get_type()] = search_handler_
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
    def get_items_permission_check(self, request_=None):
        
        
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
    def get_items(self, request_=None):
        
        
        handler_ = self.get_search_handler(request_)
        if is_wp_error(handler_):
            return handler_
        # end if
        result_ = handler_.search_items(request_)
        if (not (php_isset(lambda : result_[WP_REST_Search_Handler.RESULT_IDS]))) or (not php_is_array(result_[WP_REST_Search_Handler.RESULT_IDS])) or (not (php_isset(lambda : result_[WP_REST_Search_Handler.RESULT_TOTAL]))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_search_handler_error", __("Internal search handler error."), Array({"status": 500})))
        # end if
        ids_ = php_array_map("absint", result_[WP_REST_Search_Handler.RESULT_IDS])
        results_ = Array()
        for id_ in ids_:
            data_ = self.prepare_item_for_response(id_, request_)
            results_[-1] = self.prepare_response_for_collection(data_)
        # end for
        total_ = php_int(result_[WP_REST_Search_Handler.RESULT_TOTAL])
        page_ = php_int(request_["page"])
        per_page_ = php_int(request_["per_page"])
        max_pages_ = ceil(total_ / per_page_)
        if page_ > max_pages_ and total_ > 0:
            return php_new_class("WP_Error", lambda : WP_Error("rest_search_invalid_page_number", __("The page number requested is larger than the number of pages available."), Array({"status": 400})))
        # end if
        response_ = rest_ensure_response(results_)
        response_.header("X-WP-Total", total_)
        response_.header("X-WP-TotalPages", max_pages_)
        request_params_ = request_.get_query_params()
        base_ = add_query_arg(urlencode_deep(request_params_), rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base)))
        if page_ > 1:
            prev_link_ = add_query_arg("page", page_ - 1, base_)
            response_.link_header("prev", prev_link_)
        # end if
        if page_ < max_pages_:
            next_link_ = add_query_arg("page", page_ + 1, base_)
            response_.link_header("next", next_link_)
        # end if
        return response_
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
    def prepare_item_for_response(self, id_=None, request_=None):
        
        
        handler_ = self.get_search_handler(request_)
        if is_wp_error(handler_):
            return php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        # end if
        fields_ = self.get_fields_for_response(request_)
        data_ = handler_.prepare_item(id_, fields_)
        data_ = self.add_additional_fields_to_object(data_, request_)
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.filter_response_by_context(data_, context_)
        response_ = rest_ensure_response(data_)
        links_ = handler_.prepare_item_links(id_)
        links_["collection"] = Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})
        response_.add_links(links_)
        return response_
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
        types_ = Array()
        subtypes_ = Array()
        for search_handler_ in self.search_handlers:
            types_[-1] = search_handler_.get_type()
            subtypes_ = php_array_merge(subtypes_, search_handler_.get_subtypes())
        # end for
        types_ = array_unique(types_)
        subtypes_ = array_unique(subtypes_)
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "search-result", "type": "object", "properties": Array({self.PROP_ID: Array({"description": __("Unique identifier for the object."), "type": "integer", "context": Array("view", "embed"), "readonly": True})}, {self.PROP_TITLE: Array({"description": __("The title for the object."), "type": "string", "context": Array("view", "embed"), "readonly": True})}, {self.PROP_URL: Array({"description": __("URL to the object."), "type": "string", "format": "uri", "context": Array("view", "embed"), "readonly": True})}, {self.PROP_TYPE: Array({"description": __("Object type."), "type": "string", "enum": types_, "context": Array("view", "embed"), "readonly": True})}, {self.PROP_SUBTYPE: Array({"description": __("Object subtype."), "type": "string", "enum": subtypes_, "context": Array("view", "embed"), "readonly": True})})})
        self.schema = schema_
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
        
        
        types_ = Array()
        subtypes_ = Array()
        for search_handler_ in self.search_handlers:
            types_[-1] = search_handler_.get_type()
            subtypes_ = php_array_merge(subtypes_, search_handler_.get_subtypes())
        # end for
        types_ = array_unique(types_)
        subtypes_ = array_unique(subtypes_)
        query_params_ = super().get_collection_params()
        query_params_["context"]["default"] = "view"
        query_params_[self.PROP_TYPE] = Array({"default": types_[0], "description": __("Limit results to items of an object type."), "type": "string", "enum": types_})
        query_params_[self.PROP_SUBTYPE] = Array({"default": self.TYPE_ANY, "description": __("Limit results to items of one or more object subtypes."), "type": "array", "items": Array({"enum": php_array_merge(subtypes_, Array(self.TYPE_ANY)), "type": "string"})}, {"sanitize_callback": Array(self, "sanitize_subtypes")})
        return query_params_
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
    def sanitize_subtypes(self, subtypes_=None, request_=None, parameter_=None):
        
        
        subtypes_ = wp_parse_slug_list(subtypes_)
        subtypes_ = rest_parse_request_arg(subtypes_, request_, parameter_)
        if is_wp_error(subtypes_):
            return subtypes_
        # end if
        #// 'any' overrides any other subtype.
        if php_in_array(self.TYPE_ANY, subtypes_, True):
            return Array(self.TYPE_ANY)
        # end if
        handler_ = self.get_search_handler(request_)
        if is_wp_error(handler_):
            return handler_
        # end if
        return php_array_intersect(subtypes_, handler_.get_subtypes())
    # end def sanitize_subtypes
    #// 
    #// Gets the search handler to handle the current request.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Search_Handler|WP_Error Search handler for the request type, or WP_Error object on failure.
    #//
    def get_search_handler(self, request_=None):
        
        
        type_ = request_.get_param(self.PROP_TYPE)
        if (not type_) or (not (php_isset(lambda : self.search_handlers[type_]))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_search_invalid_type", __("Invalid type parameter."), Array({"status": 400})))
        # end if
        return self.search_handlers[type_]
    # end def get_search_handler
# end class WP_REST_Search_Controller
