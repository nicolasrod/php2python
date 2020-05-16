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
    namespace = Array()
    rest_base = Array()
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
    def get_items_permissions_check(self, request=None):
        
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
    def get_items(self, request=None):
        
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
    def get_item_permissions_check(self, request=None):
        
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
    def get_item(self, request=None):
        
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
    def create_item_permissions_check(self, request=None):
        
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
    def create_item(self, request=None):
        
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
    def update_item_permissions_check(self, request=None):
        
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
    def update_item(self, request=None):
        
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
    def delete_item_permissions_check(self, request=None):
        
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
    def delete_item(self, request=None):
        
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
    def prepare_item_for_database(self, request=None):
        
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
    def prepare_item_for_response(self, item=None, request=None):
        
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
    def prepare_response_for_collection(self, response=None):
        
        if (not type(response).__name__ == "WP_REST_Response"):
            return response
        # end if
        data = response.get_data()
        server = rest_get_server()
        links = server.get_compact_response_links(response)
        if (not php_empty(lambda : links)):
            data["_links"] = links
        # end if
        return data
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
    def filter_response_by_context(self, data=None, context=None):
        
        schema = self.get_item_schema()
        for key,value in data:
            if php_empty(lambda : schema["properties"][key]) or php_empty(lambda : schema["properties"][key]["context"]):
                continue
            # end if
            if (not php_in_array(context, schema["properties"][key]["context"], True)):
                data[key] = None
                continue
            # end if
            if "object" == schema["properties"][key]["type"] and (not php_empty(lambda : schema["properties"][key]["properties"])):
                for attribute,details in schema["properties"][key]["properties"]:
                    if php_empty(lambda : details["context"]):
                        continue
                    # end if
                    if (not php_in_array(context, details["context"], True)):
                        if (php_isset(lambda : data[key][attribute])):
                            data[key][attribute] = None
                        # end if
                    # end if
                # end for
            # end if
        # end for
        return data
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
        
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"])):
            for property in schema["properties"]:
                property["arg_options"] = None
            # end for
        # end if
        return schema
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
    def get_context_param(self, args=Array()):
        
        param_details = Array({"description": __("Scope under which the request is made; determines fields present in response."), "type": "string", "sanitize_callback": "sanitize_key", "validate_callback": "rest_validate_request_arg"})
        schema = self.get_item_schema()
        if php_empty(lambda : schema["properties"]):
            return php_array_merge(param_details, args)
        # end if
        contexts = Array()
        for attributes in schema["properties"]:
            if (not php_empty(lambda : attributes["context"])):
                contexts = php_array_merge(contexts, attributes["context"])
            # end if
        # end for
        if (not php_empty(lambda : contexts)):
            param_details["enum"] = array_unique(contexts)
            rsort(param_details["enum"])
        # end if
        return php_array_merge(param_details, args)
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
    def add_additional_fields_to_object(self, prepared=None, request=None):
        
        additional_fields = self.get_additional_fields()
        requested_fields = self.get_fields_for_response(request)
        for field_name,field_options in additional_fields:
            if (not field_options["get_callback"]):
                continue
            # end if
            if (not php_in_array(field_name, requested_fields, True)):
                continue
            # end if
            prepared[field_name] = php_call_user_func(field_options["get_callback"], prepared, field_name, request, self.get_object_type())
        # end for
        return prepared
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
    def update_additional_fields_for_object(self, object=None, request=None):
        
        additional_fields = self.get_additional_fields()
        for field_name,field_options in additional_fields:
            if (not field_options["update_callback"]):
                continue
            # end if
            #// Don't run the update callbacks if the data wasn't passed in the request.
            if (not (php_isset(lambda : request[field_name]))):
                continue
            # end if
            result = php_call_user_func(field_options["update_callback"], request[field_name], object, field_name, request, self.get_object_type())
            if is_wp_error(result):
                return result
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
    def add_additional_fields_schema(self, schema=None):
        
        if php_empty(lambda : schema["title"]):
            return schema
        # end if
        #// Can't use $this->get_object_type otherwise we cause an inf loop.
        object_type = schema["title"]
        additional_fields = self.get_additional_fields(object_type)
        for field_name,field_options in additional_fields:
            if (not field_options["schema"]):
                continue
            # end if
            schema["properties"][field_name] = field_options["schema"]
        # end for
        return schema
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
    def get_additional_fields(self, object_type=None):
        
        if (not object_type):
            object_type = self.get_object_type()
        # end if
        if (not object_type):
            return Array()
        # end if
        global wp_rest_additional_fields
        php_check_if_defined("wp_rest_additional_fields")
        if (not wp_rest_additional_fields) or (not (php_isset(lambda : wp_rest_additional_fields[object_type]))):
            return Array()
        # end if
        return wp_rest_additional_fields[object_type]
    # end def get_additional_fields
    #// 
    #// Retrieves the object type this controller is responsible for managing.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string Object type for the controller.
    #//
    def get_object_type(self):
        
        schema = self.get_item_schema()
        if (not schema) or (not (php_isset(lambda : schema["title"]))):
            return None
        # end if
        return schema["title"]
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
    def get_fields_for_response(self, request=None):
        
        schema = self.get_item_schema()
        properties = schema["properties"] if (php_isset(lambda : schema["properties"])) else Array()
        additional_fields = self.get_additional_fields()
        for field_name,field_options in additional_fields:
            #// For back-compat, include any field with an empty schema
            #// because it won't be present in $this->get_item_schema().
            if is_null(field_options["schema"]):
                properties[field_name] = field_options
            # end if
        # end for
        #// Exclude fields that specify a different context than the request context.
        context = request["context"]
        if context:
            for name,options in properties:
                if (not php_empty(lambda : options["context"])) and (not php_in_array(context, options["context"], True)):
                    properties[name] = None
                # end if
            # end for
        # end if
        fields = php_array_keys(properties)
        if (not (php_isset(lambda : request["_fields"]))):
            return fields
        # end if
        requested_fields = wp_parse_list(request["_fields"])
        if 0 == php_count(requested_fields):
            return fields
        # end if
        #// Trim off outside whitespace from the comma delimited list.
        requested_fields = php_array_map("trim", requested_fields)
        #// Always persist 'id', because it can be needed for add_additional_fields_to_object().
        if php_in_array("id", fields, True):
            requested_fields[-1] = "id"
        # end if
        def _closure_e88d4eee(response_fields = None, field = None):
            
            if php_in_array(field, fields, True):
                response_fields[-1] = field
                return response_fields
            # end if
            #// Check for nested fields if $field is not a direct match.
            nested_fields = php_explode(".", field)
            #// A nested field is included so long as its top-level property
            #// is present in the schema.
            if php_in_array(nested_fields[0], fields, True):
                response_fields[-1] = field
            # end if
            return response_fields
        # end def _closure_e88d4eee
        #// Return the list of all requested fields which appear in the schema.
        response_fields[-1] = field
        nested_fields = php_explode(".", field)
        response_fields[-1] = field
        return array_reduce(requested_fields, (lambda *args, **kwargs: _closure_e88d4eee(*args, **kwargs)), Array())
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
    def get_endpoint_args_for_item_schema(self, method=WP_REST_Server.CREATABLE):
        
        schema = self.get_item_schema()
        schema_properties = schema["properties"] if (not php_empty(lambda : schema["properties"])) else Array()
        endpoint_args = Array()
        for field_id,params in schema_properties:
            #// Arguments specified as `readonly` are not allowed to be set.
            if (not php_empty(lambda : params["readonly"])):
                continue
            # end if
            endpoint_args[field_id] = Array({"validate_callback": "rest_validate_request_arg", "sanitize_callback": "rest_sanitize_request_arg"})
            if (php_isset(lambda : params["description"])):
                endpoint_args[field_id]["description"] = params["description"]
            # end if
            if WP_REST_Server.CREATABLE == method and (php_isset(lambda : params["default"])):
                endpoint_args[field_id]["default"] = params["default"]
            # end if
            if WP_REST_Server.CREATABLE == method and (not php_empty(lambda : params["required"])):
                endpoint_args[field_id]["required"] = True
            # end if
            for schema_prop in Array("type", "format", "enum", "items", "properties", "additionalProperties"):
                if (php_isset(lambda : params[schema_prop])):
                    endpoint_args[field_id][schema_prop] = params[schema_prop]
                # end if
            # end for
            #// Merge in any options provided by the schema property.
            if (php_isset(lambda : params["arg_options"])):
                #// Only use required / default from arg_options on CREATABLE endpoints.
                if WP_REST_Server.CREATABLE != method:
                    params["arg_options"] = php_array_diff_key(params["arg_options"], Array({"required": "", "default": ""}))
                # end if
                endpoint_args[field_id] = php_array_merge(endpoint_args[field_id], params["arg_options"])
            # end if
        # end for
        return endpoint_args
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
    def sanitize_slug(self, slug=None):
        
        return sanitize_title(slug)
    # end def sanitize_slug
# end class WP_REST_Controller
