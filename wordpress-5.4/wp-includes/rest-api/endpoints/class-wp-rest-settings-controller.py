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
#// REST API: WP_REST_Settings_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to manage a site's settings via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Settings_Controller(WP_REST_Controller):
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #//
    def __init__(self):
        
        self.namespace = "wp/v2"
        self.rest_base = "settings"
    # end def __init__
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        register_rest_route(self.namespace, "/" + self.rest_base, Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "args": Array(), "permission_callback": Array(self, "get_item_permissions_check")}), Array({"methods": WP_REST_Server.EDITABLE, "callback": Array(self, "update_item"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE), "permission_callback": Array(self, "get_item_permissions_check")}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks if a given request has access to read and manage settings.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool True if the request has read access for the item, otherwise false.
    #//
    def get_item_permissions_check(self, request=None):
        
        return current_user_can("manage_options")
    # end def get_item_permissions_check
    #// 
    #// Retrieves the settings.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return array|WP_Error Array on success, or WP_Error object on failure.
    #//
    def get_item(self, request=None):
        
        options = self.get_registered_options()
        response = Array()
        for name,args in options:
            #// 
            #// Filters the value of a setting recognized by the REST API.
            #// 
            #// Allow hijacking the setting value and overriding the built-in behavior by returning a
            #// non-null value.  The returned value will be presented as the setting value instead.
            #// 
            #// @since 4.7.0
            #// 
            #// @param mixed  $result Value to use for the requested setting. Can be a scalar
            #// matching the registered schema for the setting, or null to
            #// follow the default get_option() behavior.
            #// @param string $name   Setting name (as shown in REST API responses).
            #// @param array  $args   Arguments passed to register_setting() for this setting.
            #//
            response[name] = apply_filters("rest_pre_get_setting", None, name, args)
            if is_null(response[name]):
                #// Default to a null value as "null" in the response means "not set".
                response[name] = get_option(args["option_name"], args["schema"]["default"])
            # end if
            #// 
            #// Because get_option() is lossy, we have to
            #// cast values to the type they are registered with.
            #//
            response[name] = self.prepare_value(response[name], args["schema"])
        # end for
        return response
    # end def get_item
    #// 
    #// Prepares a value for output based off a schema array.
    #// 
    #// @since 4.7.0
    #// 
    #// @param mixed $value  Value to prepare.
    #// @param array $schema Schema to match.
    #// @return mixed The prepared value.
    #//
    def prepare_value(self, value=None, schema=None):
        
        #// 
        #// If the value is not valid by the schema, set the value to null.
        #// Null values are specifically non-destructive, so this will not cause
        #// overwriting the current invalid value to null.
        #//
        if is_wp_error(rest_validate_value_from_schema(value, schema)):
            return None
        # end if
        return rest_sanitize_value_from_schema(value, schema)
    # end def prepare_value
    #// 
    #// Updates settings for the settings object.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return array|WP_Error Array on success, or error object on failure.
    #//
    def update_item(self, request=None):
        
        options = self.get_registered_options()
        params = request.get_params()
        for name,args in options:
            if (not php_array_key_exists(name, params)):
                continue
            # end if
            #// 
            #// Filters whether to preempt a setting value update.
            #// 
            #// Allows hijacking the setting update logic and overriding the built-in behavior by
            #// returning true.
            #// 
            #// @since 4.7.0
            #// 
            #// @param bool   $result Whether to override the default behavior for updating the
            #// value of a setting.
            #// @param string $name   Setting name (as shown in REST API responses).
            #// @param mixed  $value  Updated setting value.
            #// @param array  $args   Arguments passed to register_setting() for this setting.
            #//
            updated = apply_filters("rest_pre_update_setting", False, name, request[name], args)
            if updated:
                continue
            # end if
            #// 
            #// A null value for an option would have the same effect as
            #// deleting the option from the database, and relying on the
            #// default value.
            #//
            if is_null(request[name]):
                #// 
                #// A null value is returned in the response for any option
                #// that has a non-scalar value.
                #// 
                #// To protect clients from accidentally including the null
                #// values from a response object in a request, we do not allow
                #// options with values that don't pass validation to be updated to null.
                #// Without this added protection a client could mistakenly
                #// delete all options that have invalid values from the
                #// database.
                #//
                if is_wp_error(rest_validate_value_from_schema(get_option(args["option_name"], False), args["schema"])):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_stored_value", php_sprintf(__("The %s property has an invalid stored value, and cannot be updated to null."), name), Array({"status": 500})))
                # end if
                delete_option(args["option_name"])
            else:
                update_option(args["option_name"], request[name])
            # end if
        # end for
        return self.get_item(request)
    # end def update_item
    #// 
    #// Retrieves all of the registered options for the Settings API.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Array of registered options.
    #//
    def get_registered_options(self):
        
        rest_options = Array()
        for name,args in get_registered_settings():
            if php_empty(lambda : args["show_in_rest"]):
                continue
            # end if
            rest_args = Array()
            if php_is_array(args["show_in_rest"]):
                rest_args = args["show_in_rest"]
            # end if
            defaults = Array({"name": rest_args["name"] if (not php_empty(lambda : rest_args["name"])) else name, "schema": Array()})
            rest_args = php_array_merge(defaults, rest_args)
            default_schema = Array({"type": None if php_empty(lambda : args["type"]) else args["type"], "description": "" if php_empty(lambda : args["description"]) else args["description"], "default": args["default"] if (php_isset(lambda : args["default"])) else None})
            rest_args["schema"] = php_array_merge(default_schema, rest_args["schema"])
            rest_args["option_name"] = name
            #// Skip over settings that don't have a defined type in the schema.
            if php_empty(lambda : rest_args["schema"]["type"]):
                continue
            # end if
            #// 
            #// Whitelist the supported types for settings, as we don't want invalid types
            #// to be updated with arbitrary values that we can't do decent sanitizing for.
            #//
            if (not php_in_array(rest_args["schema"]["type"], Array("number", "integer", "string", "boolean", "array", "object"), True)):
                continue
            # end if
            rest_args["schema"] = self.set_additional_properties_to_false(rest_args["schema"])
            rest_options[rest_args["name"]] = rest_args
        # end for
        return rest_options
    # end def get_registered_options
    #// 
    #// Retrieves the site setting schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        options = self.get_registered_options()
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "settings", "type": "object", "properties": Array()})
        for option_name,option in options:
            schema["properties"][option_name] = option["schema"]
            schema["properties"][option_name]["arg_options"] = Array({"sanitize_callback": Array(self, "sanitize_callback")})
        # end for
        self.schema = schema
        return self.add_additional_fields_schema(self.schema)
    # end def get_item_schema
    #// 
    #// Custom sanitize callback used for all options to allow the use of 'null'.
    #// 
    #// By default, the schema of settings will throw an error if a value is set to
    #// `null` as it's not a valid value for something like "type => string". We
    #// provide a wrapper sanitizer to whitelist the use of `null`.
    #// 
    #// @since 4.7.0
    #// 
    #// @param mixed           $value   The value for the setting.
    #// @param WP_REST_Request $request The request object.
    #// @param string          $param   The parameter name.
    #// @return mixed|WP_Error
    #//
    def sanitize_callback(self, value=None, request=None, param=None):
        
        if is_null(value):
            return value
        # end if
        return rest_parse_request_arg(value, request, param)
    # end def sanitize_callback
    #// 
    #// Recursively add additionalProperties = false to all objects in a schema.
    #// 
    #// This is need to restrict properties of objects in settings values to only
    #// registered items, as the REST API will allow additional properties by
    #// default.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $schema The schema array.
    #// @return array
    #//
    def set_additional_properties_to_false(self, schema=None):
        
        for case in Switch(schema["type"]):
            if case("object"):
                for key,child_schema in schema["properties"]:
                    schema["properties"][key] = self.set_additional_properties_to_false(child_schema)
                # end for
                schema["additionalProperties"] = False
                break
            # end if
            if case("array"):
                schema["items"] = self.set_additional_properties_to_false(schema["items"])
                break
            # end if
        # end for
        return schema
    # end def set_additional_properties_to_false
# end class WP_REST_Settings_Controller
