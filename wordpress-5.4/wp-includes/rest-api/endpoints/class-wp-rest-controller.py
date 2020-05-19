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
#// REST API: WP_REST_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core base controller for managing and interacting with REST API items.
#// 
#// @since 4.7.0
#//
class WP_REST_Controller():
    #// 
    #// The namespace of this controller's route.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    namespace = Array()
    #// 
    #// The base of this controller's route.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    rest_base = Array()
    #// 
    #// Cached results of get_item_schema.
    #// 
    #// @since 5.3.0
    #// @var array
    #//
    schema = Array()
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        
        _doing_it_wrong("WP_REST_Controller::register_routes", php_sprintf(__("Method '%s' must be overridden."), __METHOD__), "4.7")
    # end def register_routes
    #// 
    #// Checks if a given request has access to get items.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def get_items_permissions_check
    #// 
    #// Retrieves a collection of items.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def get_items
    #// 
    #// Checks if a given request has access to get a specific item.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, WP_Error object otherwise.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def get_item_permissions_check
    #// 
    #// Retrieves one item from the collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def get_item
    #// 
    #// Checks if a given request has access to create items.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to create items, WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def create_item_permissions_check
    #// 
    #// Creates one item from the collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def create_item(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def create_item
    #// 
    #// Checks if a given request has access to update a specific item.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def update_item_permissions_check(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def update_item_permissions_check
    #// 
    #// Updates one item from the collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def update_item(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def update_item
    #// 
    #// Checks if a given request has access to delete a specific item.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to delete the item, WP_Error object otherwise.
    #//
    def delete_item_permissions_check(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def delete_item_permissions_check
    #// 
    #// Deletes one item from the collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def delete_item(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def delete_item
    #// 
    #// Prepares one item for create or update operation.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return object|WP_Error The prepared item, or WP_Error object on failure.
    #//
    def prepare_item_for_database(self, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def prepare_item_for_database
    #// 
    #// Prepares the item for the REST response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param mixed           $item    WordPress representation of the item.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def prepare_item_for_response(self, item_=None, request_=None):
        
        
        return php_new_class("WP_Error", lambda : WP_Error("invalid-method", php_sprintf(__("Method '%s' not implemented. Must be overridden in subclass."), __METHOD__), Array({"status": 405})))
    # end def prepare_item_for_response
    #// 
    #// Prepares a response for insertion into a collection.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Response $response Response object.
    #// @return array|mixed Response data, ready for insertion into collection data.
    #//
    def prepare_response_for_collection(self, response_=None):
        
        
        if (not type(response_).__name__ == "WP_REST_Response"):
            return response_
        # end if
        data_ = response_.get_data()
        server_ = rest_get_server()
        links_ = server_.get_compact_response_links(response_)
        if (not php_empty(lambda : links_)):
            data_["_links"] = links_
        # end if
        return data_
    # end def prepare_response_for_collection
    #// 
    #// Filters a response based on the context defined in the schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $data    Response data to fiter.
    #// @param string $context Context defined in the schema.
    #// @return array Filtered response.
    #//
    def filter_response_by_context(self, data_=None, context_=None):
        
        
        schema_ = self.get_item_schema()
        for key_,value_ in data_.items():
            if php_empty(lambda : schema_["properties"][key_]) or php_empty(lambda : schema_["properties"][key_]["context"]):
                continue
            # end if
            if (not php_in_array(context_, schema_["properties"][key_]["context"], True)):
                data_[key_] = None
                continue
            # end if
            if "object" == schema_["properties"][key_]["type"] and (not php_empty(lambda : schema_["properties"][key_]["properties"])):
                for attribute_,details_ in schema_["properties"][key_]["properties"].items():
                    if php_empty(lambda : details_["context"]):
                        continue
                    # end if
                    if (not php_in_array(context_, details_["context"], True)):
                        if (php_isset(lambda : data_[key_][attribute_])):
                            data_[key_][attribute_] = None
                        # end if
                    # end if
                # end for
            # end if
        # end for
        return data_
    # end def filter_response_by_context
    #// 
    #// Retrieves the item's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        
        return self.add_additional_fields_schema(Array())
    # end def get_item_schema
    #// 
    #// Retrieves the item's schema for display / public consumption purposes.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Public item schema data.
    #//
    def get_public_item_schema(self):
        
        
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"])):
            for property_ in schema_["properties"]:
                property_["arg_options"] = None
            # end for
        # end if
        return schema_
    # end def get_public_item_schema
    #// 
    #// Retrieves the query params for the collections.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Query parameters for the collection.
    #//
    def get_collection_params(self):
        
        
        return Array({"context": self.get_context_param(), "page": Array({"description": __("Current page of the collection."), "type": "integer", "default": 1, "sanitize_callback": "absint", "validate_callback": "rest_validate_request_arg", "minimum": 1})}, {"per_page": Array({"description": __("Maximum number of items to be returned in result set."), "type": "integer", "default": 10, "minimum": 1, "maximum": 100, "sanitize_callback": "absint", "validate_callback": "rest_validate_request_arg"})}, {"search": Array({"description": __("Limit results to those matching a string."), "type": "string", "sanitize_callback": "sanitize_text_field", "validate_callback": "rest_validate_request_arg"})})
    # end def get_collection_params
    #// 
    #// Retrieves the magical context param.
    #// 
    #// Ensures consistent descriptions between endpoints, and populates enum from schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $args Optional. Additional arguments for context parameter. Default empty array.
    #// @return array Context parameter details.
    #//
    def get_context_param(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        param_details_ = Array({"description": __("Scope under which the request is made; determines fields present in response."), "type": "string", "sanitize_callback": "sanitize_key", "validate_callback": "rest_validate_request_arg"})
        schema_ = self.get_item_schema()
        if php_empty(lambda : schema_["properties"]):
            return php_array_merge(param_details_, args_)
        # end if
        contexts_ = Array()
        for attributes_ in schema_["properties"]:
            if (not php_empty(lambda : attributes_["context"])):
                contexts_ = php_array_merge(contexts_, attributes_["context"])
            # end if
        # end for
        if (not php_empty(lambda : contexts_)):
            param_details_["enum"] = array_unique(contexts_)
            rsort(param_details_["enum"])
        # end if
        return php_array_merge(param_details_, args_)
    # end def get_context_param
    #// 
    #// Adds the values from additional fields to a data object.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array           $prepared Prepared response array.
    #// @param WP_REST_Request $request  Full details about the request.
    #// @return array Modified data object with additional fields.
    #//
    def add_additional_fields_to_object(self, prepared_=None, request_=None):
        
        
        additional_fields_ = self.get_additional_fields()
        requested_fields_ = self.get_fields_for_response(request_)
        for field_name_,field_options_ in additional_fields_.items():
            if (not field_options_["get_callback"]):
                continue
            # end if
            if (not php_in_array(field_name_, requested_fields_, True)):
                continue
            # end if
            prepared_[field_name_] = php_call_user_func(field_options_["get_callback"], prepared_, field_name_, request_, self.get_object_type())
        # end for
        return prepared_
    # end def add_additional_fields_to_object
    #// 
    #// Updates the values of additional fields added to a data object.
    #// 
    #// @since 4.7.0
    #// 
    #// @param object          $object  Data model like WP_Term or WP_Post.
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True on success, WP_Error object if a field cannot be updated.
    #//
    def update_additional_fields_for_object(self, object_=None, request_=None):
        
        
        additional_fields_ = self.get_additional_fields()
        for field_name_,field_options_ in additional_fields_.items():
            if (not field_options_["update_callback"]):
                continue
            # end if
            #// Don't run the update callbacks if the data wasn't passed in the request.
            if (not (php_isset(lambda : request_[field_name_]))):
                continue
            # end if
            result_ = php_call_user_func(field_options_["update_callback"], request_[field_name_], object_, field_name_, request_, self.get_object_type())
            if is_wp_error(result_):
                return result_
            # end if
        # end for
        return True
    # end def update_additional_fields_for_object
    #// 
    #// Adds the schema from additional fields to a schema array.
    #// 
    #// The type of object is inferred from the passed schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $schema Schema array.
    #// @return array Modified Schema array.
    #//
    def add_additional_fields_schema(self, schema_=None):
        
        
        if php_empty(lambda : schema_["title"]):
            return schema_
        # end if
        #// Can't use $this->get_object_type otherwise we cause an inf loop.
        object_type_ = schema_["title"]
        additional_fields_ = self.get_additional_fields(object_type_)
        for field_name_,field_options_ in additional_fields_.items():
            if (not field_options_["schema"]):
                continue
            # end if
            schema_["properties"][field_name_] = field_options_["schema"]
        # end for
        return schema_
    # end def add_additional_fields_schema
    #// 
    #// Retrieves all of the registered additional fields for a given object-type.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $object_type Optional. The object type.
    #// @return array Registered additional fields (if any), empty array if none or if the object type could
    #// not be inferred.
    #//
    def get_additional_fields(self, object_type_=None):
        if object_type_ is None:
            object_type_ = None
        # end if
        
        if (not object_type_):
            object_type_ = self.get_object_type()
        # end if
        if (not object_type_):
            return Array()
        # end if
        global wp_rest_additional_fields_
        php_check_if_defined("wp_rest_additional_fields_")
        if (not wp_rest_additional_fields_) or (not (php_isset(lambda : wp_rest_additional_fields_[object_type_]))):
            return Array()
        # end if
        return wp_rest_additional_fields_[object_type_]
    # end def get_additional_fields
    #// 
    #// Retrieves the object type this controller is responsible for managing.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string Object type for the controller.
    #//
    def get_object_type(self):
        
        
        schema_ = self.get_item_schema()
        if (not schema_) or (not (php_isset(lambda : schema_["title"]))):
            return None
        # end if
        return schema_["title"]
    # end def get_object_type
    #// 
    #// Gets an array of fields to be included on the response.
    #// 
    #// Included fields are based on item schema and `_fields=` request argument.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return array Fields to be included in the response.
    #//
    def get_fields_for_response(self, request_=None):
        
        
        schema_ = self.get_item_schema()
        properties_ = schema_["properties"] if (php_isset(lambda : schema_["properties"])) else Array()
        additional_fields_ = self.get_additional_fields()
        for field_name_,field_options_ in additional_fields_.items():
            #// For back-compat, include any field with an empty schema
            #// because it won't be present in $this->get_item_schema().
            if php_is_null(field_options_["schema"]):
                properties_[field_name_] = field_options_
            # end if
        # end for
        #// Exclude fields that specify a different context than the request context.
        context_ = request_["context"]
        if context_:
            for name_,options_ in properties_.items():
                if (not php_empty(lambda : options_["context"])) and (not php_in_array(context_, options_["context"], True)):
                    properties_[name_] = None
                # end if
            # end for
        # end if
        fields_ = php_array_keys(properties_)
        if (not (php_isset(lambda : request_["_fields"]))):
            return fields_
        # end if
        requested_fields_ = wp_parse_list(request_["_fields"])
        if 0 == php_count(requested_fields_):
            return fields_
        # end if
        #// Trim off outside whitespace from the comma delimited list.
        requested_fields_ = php_array_map("trim", requested_fields_)
        #// Always persist 'id', because it can be needed for add_additional_fields_to_object().
        if php_in_array("id", fields_, True):
            requested_fields_[-1] = "id"
        # end if
        def _closure_ca5b9235(response_fields_=None, field_=None):
            
            
            if php_in_array(field_, fields_, True):
                response_fields_[-1] = field_
                return response_fields_
            # end if
            #// Check for nested fields if $field is not a direct match.
            nested_fields_ = php_explode(".", field_)
            #// A nested field is included so long as its top-level property
            #// is present in the schema.
            if php_in_array(nested_fields_[0], fields_, True):
                response_fields_[-1] = field_
            # end if
            return response_fields_
        # end def _closure_ca5b9235
        #// Return the list of all requested fields which appear in the schema.
        response_fields_[-1] = field_
        nested_fields_ = php_explode(".", field_)
        response_fields_[-1] = field_
        return array_reduce(requested_fields_, (lambda *args, **kwargs: _closure_ca5b9235(*args, **kwargs)), Array())
    # end def get_fields_for_response
    #// 
    #// Retrieves an array of endpoint arguments from the item schema for the controller.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $method Optional. HTTP method of the request. The arguments for `CREATABLE` requests are
    #// checked for required values and may fall-back to a given default, this is not done
    #// on `EDITABLE` requests. Default WP_REST_Server::CREATABLE.
    #// @return array Endpoint arguments.
    #//
    def get_endpoint_args_for_item_schema(self, method_=None):
        if method_ is None:
            method_ = WP_REST_Server.CREATABLE
        # end if
        
        schema_ = self.get_item_schema()
        schema_properties_ = schema_["properties"] if (not php_empty(lambda : schema_["properties"])) else Array()
        endpoint_args_ = Array()
        for field_id_,params_ in schema_properties_.items():
            #// Arguments specified as `readonly` are not allowed to be set.
            if (not php_empty(lambda : params_["readonly"])):
                continue
            # end if
            endpoint_args_[field_id_] = Array({"validate_callback": "rest_validate_request_arg", "sanitize_callback": "rest_sanitize_request_arg"})
            if (php_isset(lambda : params_["description"])):
                endpoint_args_[field_id_]["description"] = params_["description"]
            # end if
            if WP_REST_Server.CREATABLE == method_ and (php_isset(lambda : params_["default"])):
                endpoint_args_[field_id_]["default"] = params_["default"]
            # end if
            if WP_REST_Server.CREATABLE == method_ and (not php_empty(lambda : params_["required"])):
                endpoint_args_[field_id_]["required"] = True
            # end if
            for schema_prop_ in Array("type", "format", "enum", "items", "properties", "additionalProperties"):
                if (php_isset(lambda : params_[schema_prop_])):
                    endpoint_args_[field_id_][schema_prop_] = params_[schema_prop_]
                # end if
            # end for
            #// Merge in any options provided by the schema property.
            if (php_isset(lambda : params_["arg_options"])):
                #// Only use required / default from arg_options on CREATABLE endpoints.
                if WP_REST_Server.CREATABLE != method_:
                    params_["arg_options"] = php_array_diff_key(params_["arg_options"], Array({"required": "", "default": ""}))
                # end if
                endpoint_args_[field_id_] = php_array_merge(endpoint_args_[field_id_], params_["arg_options"])
            # end if
        # end for
        return endpoint_args_
    # end def get_endpoint_args_for_item_schema
    #// 
    #// Sanitizes the slug value.
    #// 
    #// @since 4.7.0
    #// 
    #// @internal We can't use sanitize_title() directly, as the second
    #// parameter is the fallback title, which would end up being set to the
    #// request object.
    #// 
    #// @see https://github.com/WP-API/WP-API/issues/1585
    #// 
    #// @todo Remove this in favour of https://core.trac.wordpress.org/ticket/34659
    #// 
    #// @param string $slug Slug value passed in request.
    #// @return string Sanitized value for the slug.
    #//
    def sanitize_slug(self, slug_=None):
        
        
        return sanitize_title(slug_)
    # end def sanitize_slug
# end class WP_REST_Controller
