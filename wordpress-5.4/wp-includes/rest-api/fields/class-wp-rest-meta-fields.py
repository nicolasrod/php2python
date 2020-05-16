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
#// REST API: WP_REST_Meta_Fields class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class to manage meta values for an object via the REST API.
#// 
#// @since 4.7.0
#//
class WP_REST_Meta_Fields():
    #// 
    #// Retrieves the object meta type.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string One of 'post', 'comment', 'term', 'user', or anything
    #// else supported by `_get_meta_table()`.
    #//
    def get_meta_type(self):
        
        pass
    # end def get_meta_type
    #// 
    #// Retrieves the object meta subtype.
    #// 
    #// @since 4.9.8
    #// 
    #// @return string Subtype for the meta type, or empty string if no specific subtype.
    #//
    def get_meta_subtype(self):
        
        return ""
    # end def get_meta_subtype
    #// 
    #// Retrieves the object type for register_rest_field().
    #// 
    #// @since 4.7.0
    #// 
    #// @return string The REST field type, such as post type name, taxonomy name, 'comment', or `user`.
    #//
    def get_rest_field_type(self):
        
        pass
    # end def get_rest_field_type
    #// 
    #// Registers the meta field.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_field()
    #//
    def register_field(self):
        
        register_rest_field(self.get_rest_field_type(), "meta", Array({"get_callback": Array(self, "get_value"), "update_callback": Array(self, "update_value"), "schema": self.get_field_schema()}))
    # end def register_field
    #// 
    #// Retrieves the meta field value.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int             $object_id Object ID to fetch meta for.
    #// @param WP_REST_Request $request   Full details about the request.
    #// @return object|WP_Error Object containing the meta values by name, otherwise WP_Error object.
    #//
    def get_value(self, object_id=None, request=None):
        
        fields = self.get_registered_fields()
        response = Array()
        for meta_key,args in fields:
            name = args["name"]
            all_values = get_metadata(self.get_meta_type(), object_id, meta_key, False)
            if args["single"]:
                if php_empty(lambda : all_values):
                    value = args["schema"]["default"]
                else:
                    value = all_values[0]
                # end if
                value = self.prepare_value_for_response(value, request, args)
            else:
                value = Array()
                for row in all_values:
                    value[-1] = self.prepare_value_for_response(row, request, args)
                # end for
            # end if
            response[name] = value
        # end for
        return response
    # end def get_value
    #// 
    #// Prepares a meta value for a response.
    #// 
    #// This is required because some native types cannot be stored correctly
    #// in the database, such as booleans. We need to cast back to the relevant
    #// type before passing back to JSON.
    #// 
    #// @since 4.7.0
    #// 
    #// @param mixed           $value   Meta value to prepare.
    #// @param WP_REST_Request $request Current request object.
    #// @param array           $args    Options for the field.
    #// @return mixed Prepared value.
    #//
    def prepare_value_for_response(self, value=None, request=None, args=None):
        
        if (not php_empty(lambda : args["prepare_callback"])):
            value = php_call_user_func(args["prepare_callback"], value, request, args)
        # end if
        return value
    # end def prepare_value_for_response
    #// 
    #// Updates meta values.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $meta      Array of meta parsed from the request.
    #// @param int   $object_id Object ID to fetch meta for.
    #// @return null|WP_Error Null on success, WP_Error object on failure.
    #//
    def update_value(self, meta=None, object_id=None):
        
        fields = self.get_registered_fields()
        for meta_key,args in fields:
            name = args["name"]
            if (not php_array_key_exists(name, meta)):
                continue
            # end if
            #// 
            #// A null value means reset the field, which is essentially deleting it
            #// from the database and then relying on the default value.
            #//
            if is_null(meta[name]):
                args = self.get_registered_fields()[meta_key]
                if args["single"]:
                    current = get_metadata(self.get_meta_type(), object_id, meta_key, True)
                    if is_wp_error(rest_validate_value_from_schema(current, args["schema"])):
                        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_stored_value", php_sprintf(__("The %s property has an invalid stored value, and cannot be updated to null."), name), Array({"status": 500})))
                    # end if
                # end if
                result = self.delete_meta_value(object_id, meta_key, name)
                if is_wp_error(result):
                    return result
                # end if
                continue
            # end if
            value = meta[name]
            if (not args["single"]) and php_is_array(value) and php_count(php_array_filter(value, "is_null")):
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_stored_value", php_sprintf(__("The %s property has an invalid stored value, and cannot be updated to null."), name), Array({"status": 500})))
            # end if
            is_valid = rest_validate_value_from_schema(value, args["schema"], "meta." + name)
            if is_wp_error(is_valid):
                is_valid.add_data(Array({"status": 400}))
                return is_valid
            # end if
            value = rest_sanitize_value_from_schema(value, args["schema"])
            if args["single"]:
                result = self.update_meta_value(object_id, meta_key, name, value)
            else:
                result = self.update_multi_meta_value(object_id, meta_key, name, value)
            # end if
            if is_wp_error(result):
                return result
            # end if
        # end for
        return None
    # end def update_value
    #// 
    #// Deletes a meta value for an object.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int    $object_id Object ID the field belongs to.
    #// @param string $meta_key  Key for the field.
    #// @param string $name      Name for the field that is exposed in the REST API.
    #// @return bool|WP_Error True if meta field is deleted, WP_Error otherwise.
    #//
    def delete_meta_value(self, object_id=None, meta_key=None, name=None):
        
        meta_type = self.get_meta_type()
        if (not current_user_can(str("delete_") + str(meta_type) + str("_meta"), object_id, meta_key)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", php_sprintf(__("Sorry, you are not allowed to edit the %s custom field."), name), Array({"key": name, "status": rest_authorization_required_code()})))
        # end if
        if (not delete_metadata(meta_type, object_id, wp_slash(meta_key))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", __("Could not delete meta value from database."), Array({"key": name, "status": WP_Http.INTERNAL_SERVER_ERROR})))
        # end if
        return True
    # end def delete_meta_value
    #// 
    #// Updates multiple meta values for an object.
    #// 
    #// Alters the list of values in the database to match the list of provided values.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int    $object_id Object ID to update.
    #// @param string $meta_key  Key for the custom field.
    #// @param string $name      Name for the field that is exposed in the REST API.
    #// @param array  $values    List of values to update to.
    #// @return bool|WP_Error True if meta fields are updated, WP_Error otherwise.
    #//
    def update_multi_meta_value(self, object_id=None, meta_key=None, name=None, values=None):
        
        meta_type = self.get_meta_type()
        if (not current_user_can(str("edit_") + str(meta_type) + str("_meta"), object_id, meta_key)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_update", php_sprintf(__("Sorry, you are not allowed to edit the %s custom field."), name), Array({"key": name, "status": rest_authorization_required_code()})))
        # end if
        current = get_metadata(meta_type, object_id, meta_key, False)
        to_remove = current
        to_add = values
        for add_key,value in to_add:
            remove_keys = php_array_keys(to_remove, value, True)
            if php_empty(lambda : remove_keys):
                continue
            # end if
            if php_count(remove_keys) > 1:
                continue
            # end if
            remove_key = remove_keys[0]
            to_remove[remove_key] = None
            to_add[add_key] = None
        # end for
        #// 
        #// `delete_metadata` removes _all_ instances of the value, so only call once. Otherwise,
        #// `delete_metadata` will return false for subsequent calls of the same value.
        #// Use serialization to produce a predictable string that can be used by array_unique.
        #//
        to_remove = php_array_map("maybe_unserialize", array_unique(php_array_map("maybe_serialize", to_remove)))
        for value in to_remove:
            if (not delete_metadata(meta_type, object_id, wp_slash(meta_key), wp_slash(value))):
                return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", php_sprintf(__("Could not update the meta value of %s in database."), meta_key), Array({"key": name, "status": WP_Http.INTERNAL_SERVER_ERROR})))
            # end if
        # end for
        for value in to_add:
            if (not add_metadata(meta_type, object_id, wp_slash(meta_key), wp_slash(value))):
                return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", php_sprintf(__("Could not update the meta value of %s in database."), meta_key), Array({"key": name, "status": WP_Http.INTERNAL_SERVER_ERROR})))
            # end if
        # end for
        return True
    # end def update_multi_meta_value
    #// 
    #// Updates a meta value for an object.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int    $object_id Object ID to update.
    #// @param string $meta_key  Key for the custom field.
    #// @param string $name      Name for the field that is exposed in the REST API.
    #// @param mixed  $value     Updated value.
    #// @return bool|WP_Error True if the meta field was updated, WP_Error otherwise.
    #//
    def update_meta_value(self, object_id=None, meta_key=None, name=None, value=None):
        
        meta_type = self.get_meta_type()
        if (not current_user_can(str("edit_") + str(meta_type) + str("_meta"), object_id, meta_key)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_update", php_sprintf(__("Sorry, you are not allowed to edit the %s custom field."), name), Array({"key": name, "status": rest_authorization_required_code()})))
        # end if
        #// Do the exact same check for a duplicate value as in update_metadata() to avoid update_metadata() returning false.
        old_value = get_metadata(meta_type, object_id, meta_key)
        subtype = get_object_subtype(meta_type, object_id)
        args = self.get_registered_fields()[meta_key]
        if 1 == php_count(old_value):
            sanitized = sanitize_meta(meta_key, value, meta_type, subtype)
            if php_in_array(args["type"], Array("string", "number", "integer", "boolean"), True):
                #// The return value of get_metadata will always be a string for scalar types.
                sanitized = php_str(sanitized)
            # end if
            if sanitized == old_value[0]:
                return True
            # end if
        # end if
        if (not update_metadata(meta_type, object_id, wp_slash(meta_key), wp_slash_strings_only(value))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", php_sprintf(__("Could not update the meta value of %s in database."), meta_key), Array({"key": name, "status": WP_Http.INTERNAL_SERVER_ERROR})))
        # end if
        return True
    # end def update_meta_value
    #// 
    #// Retrieves all the registered meta fields.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Registered fields.
    #//
    def get_registered_fields(self):
        
        registered = Array()
        meta_type = self.get_meta_type()
        meta_subtype = self.get_meta_subtype()
        meta_keys = get_registered_meta_keys(meta_type)
        if (not php_empty(lambda : meta_subtype)):
            meta_keys = php_array_merge(meta_keys, get_registered_meta_keys(meta_type, meta_subtype))
        # end if
        for name,args in meta_keys:
            if php_empty(lambda : args["show_in_rest"]):
                continue
            # end if
            rest_args = Array()
            if php_is_array(args["show_in_rest"]):
                rest_args = args["show_in_rest"]
            # end if
            default_args = Array({"name": name, "single": args["single"], "type": args["type"] if (not php_empty(lambda : args["type"])) else None, "schema": Array(), "prepare_callback": Array(self, "prepare_value")})
            default_schema = Array({"type": default_args["type"], "description": "" if php_empty(lambda : args["description"]) else args["description"], "default": args["default"] if (php_isset(lambda : args["default"])) else None})
            rest_args = php_array_merge(default_args, rest_args)
            rest_args["schema"] = php_array_merge(default_schema, rest_args["schema"])
            type = rest_args["type"] if (not php_empty(lambda : rest_args["type"])) else None
            type = rest_args["schema"]["type"] if (not php_empty(lambda : rest_args["schema"]["type"])) else type
            if None == rest_args["schema"]["default"]:
                rest_args["schema"]["default"] = static.get_empty_value_for_type(type)
            # end if
            rest_args["schema"] = self.default_additional_properties_to_false(rest_args["schema"])
            if (not php_in_array(type, Array("string", "boolean", "integer", "number", "array", "object"), True)):
                continue
            # end if
            if php_empty(lambda : rest_args["single"]):
                rest_args["schema"] = Array({"type": "array", "items": rest_args["schema"]})
            # end if
            registered[name] = rest_args
        # end for
        return registered
    # end def get_registered_fields
    #// 
    #// Retrieves the object's meta schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Field schema data.
    #//
    def get_field_schema(self):
        
        fields = self.get_registered_fields()
        schema = Array({"description": __("Meta fields."), "type": "object", "context": Array("view", "edit"), "properties": Array(), "arg_options": Array({"sanitize_callback": None, "validate_callback": Array(self, "check_meta_is_array")})})
        for args in fields:
            schema["properties"][args["name"]] = args["schema"]
        # end for
        return schema
    # end def get_field_schema
    #// 
    #// Prepares a meta value for output.
    #// 
    #// Default preparation for meta fields. Override by passing the
    #// `prepare_callback` in your `show_in_rest` options.
    #// 
    #// @since 4.7.0
    #// 
    #// @param mixed           $value   Meta value from the database.
    #// @param WP_REST_Request $request Request object.
    #// @param array           $args    REST-specific options for the meta key.
    #// @return mixed Value prepared for output. If a non-JsonSerializable object, null.
    #//
    @classmethod
    def prepare_value(self, value=None, request=None, args=None):
        
        if args["single"]:
            schema = args["schema"]
        else:
            schema = args["schema"]["items"]
        # end if
        if "" == value and php_in_array(schema["type"], Array("boolean", "integer", "number"), True):
            value = static.get_empty_value_for_type(schema["type"])
        # end if
        if is_wp_error(rest_validate_value_from_schema(value, schema)):
            return None
        # end if
        return rest_sanitize_value_from_schema(value, schema)
    # end def prepare_value
    #// 
    #// Check the 'meta' value of a request is an associative array.
    #// 
    #// @since 4.7.0
    #// 
    #// @param mixed           $value   The meta value submitted in the request.
    #// @param WP_REST_Request $request Full details about the request.
    #// @param string          $param   The parameter name.
    #// @return array|false The meta array, if valid, false otherwise.
    #//
    def check_meta_is_array(self, value=None, request=None, param=None):
        
        if (not php_is_array(value)):
            return False
        # end if
        return value
    # end def check_meta_is_array
    #// 
    #// Recursively add additionalProperties = false to all objects in a schema if no additionalProperties setting
    #// is specified.
    #// 
    #// This is needed to restrict properties of objects in meta values to only
    #// registered items, as the REST API will allow additional properties by
    #// default.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $schema The schema array.
    #// @return array
    #//
    def default_additional_properties_to_false(self, schema=None):
        
        for case in Switch(schema["type"]):
            if case("object"):
                for key,child_schema in schema["properties"]:
                    schema["properties"][key] = self.default_additional_properties_to_false(child_schema)
                # end for
                if (not (php_isset(lambda : schema["additionalProperties"]))):
                    schema["additionalProperties"] = False
                # end if
                break
            # end if
            if case("array"):
                schema["items"] = self.default_additional_properties_to_false(schema["items"])
                break
            # end if
        # end for
        return schema
    # end def default_additional_properties_to_false
    #// 
    #// Gets the empty value for a schema type.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $type The schema type.
    #// @return mixed
    #//
    def get_empty_value_for_type(self, type=None):
        
        for case in Switch(type):
            if case("string"):
                return ""
            # end if
            if case("boolean"):
                return False
            # end if
            if case("integer"):
                return 0
            # end if
            if case("number"):
                return 0
            # end if
            if case("array"):
                pass
            # end if
            if case("object"):
                return Array()
            # end if
            if case():
                return None
            # end if
        # end for
    # end def get_empty_value_for_type
# end class WP_REST_Meta_Fields
