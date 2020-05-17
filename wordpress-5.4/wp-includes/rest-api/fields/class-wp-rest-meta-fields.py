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
    def get_value(self, object_id_=None, request_=None):
        
        
        fields_ = self.get_registered_fields()
        response_ = Array()
        for meta_key_,args_ in fields_:
            name_ = args_["name"]
            all_values_ = get_metadata(self.get_meta_type(), object_id_, meta_key_, False)
            if args_["single"]:
                if php_empty(lambda : all_values_):
                    value_ = args_["schema"]["default"]
                else:
                    value_ = all_values_[0]
                # end if
                value_ = self.prepare_value_for_response(value_, request_, args_)
            else:
                value_ = Array()
                for row_ in all_values_:
                    value_[-1] = self.prepare_value_for_response(row_, request_, args_)
                # end for
            # end if
            response_[name_] = value_
        # end for
        return response_
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
    def prepare_value_for_response(self, value_=None, request_=None, args_=None):
        
        
        if (not php_empty(lambda : args_["prepare_callback"])):
            value_ = php_call_user_func(args_["prepare_callback"], value_, request_, args_)
        # end if
        return value_
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
    def update_value(self, meta_=None, object_id_=None):
        
        
        fields_ = self.get_registered_fields()
        for meta_key_,args_ in fields_:
            name_ = args_["name"]
            if (not php_array_key_exists(name_, meta_)):
                continue
            # end if
            #// 
            #// A null value means reset the field, which is essentially deleting it
            #// from the database and then relying on the default value.
            #//
            if php_is_null(meta_[name_]):
                args_ = self.get_registered_fields()[meta_key_]
                if args_["single"]:
                    current_ = get_metadata(self.get_meta_type(), object_id_, meta_key_, True)
                    if is_wp_error(rest_validate_value_from_schema(current_, args_["schema"])):
                        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_stored_value", php_sprintf(__("The %s property has an invalid stored value, and cannot be updated to null."), name_), Array({"status": 500})))
                    # end if
                # end if
                result_ = self.delete_meta_value(object_id_, meta_key_, name_)
                if is_wp_error(result_):
                    return result_
                # end if
                continue
            # end if
            value_ = meta_[name_]
            if (not args_["single"]) and php_is_array(value_) and php_count(php_array_filter(value_, "is_null")):
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_stored_value", php_sprintf(__("The %s property has an invalid stored value, and cannot be updated to null."), name_), Array({"status": 500})))
            # end if
            is_valid_ = rest_validate_value_from_schema(value_, args_["schema"], "meta." + name_)
            if is_wp_error(is_valid_):
                is_valid_.add_data(Array({"status": 400}))
                return is_valid_
            # end if
            value_ = rest_sanitize_value_from_schema(value_, args_["schema"])
            if args_["single"]:
                result_ = self.update_meta_value(object_id_, meta_key_, name_, value_)
            else:
                result_ = self.update_multi_meta_value(object_id_, meta_key_, name_, value_)
            # end if
            if is_wp_error(result_):
                return result_
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
    def delete_meta_value(self, object_id_=None, meta_key_=None, name_=None):
        
        
        meta_type_ = self.get_meta_type()
        if (not current_user_can(str("delete_") + str(meta_type_) + str("_meta"), object_id_, meta_key_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", php_sprintf(__("Sorry, you are not allowed to edit the %s custom field."), name_), Array({"key": name_, "status": rest_authorization_required_code()})))
        # end if
        if (not delete_metadata(meta_type_, object_id_, wp_slash(meta_key_))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", __("Could not delete meta value from database."), Array({"key": name_, "status": WP_Http.INTERNAL_SERVER_ERROR})))
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
    def update_multi_meta_value(self, object_id_=None, meta_key_=None, name_=None, values_=None):
        
        
        meta_type_ = self.get_meta_type()
        if (not current_user_can(str("edit_") + str(meta_type_) + str("_meta"), object_id_, meta_key_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_update", php_sprintf(__("Sorry, you are not allowed to edit the %s custom field."), name_), Array({"key": name_, "status": rest_authorization_required_code()})))
        # end if
        current_ = get_metadata(meta_type_, object_id_, meta_key_, False)
        to_remove_ = current_
        to_add_ = values_
        for add_key_,value_ in to_add_:
            remove_keys_ = php_array_keys(to_remove_, value_, True)
            if php_empty(lambda : remove_keys_):
                continue
            # end if
            if php_count(remove_keys_) > 1:
                continue
            # end if
            remove_key_ = remove_keys_[0]
            to_remove_[remove_key_] = None
            to_add_[add_key_] = None
        # end for
        #// 
        #// `delete_metadata` removes _all_ instances of the value, so only call once. Otherwise,
        #// `delete_metadata` will return false for subsequent calls of the same value.
        #// Use serialization to produce a predictable string that can be used by array_unique.
        #//
        to_remove_ = php_array_map("maybe_unserialize", array_unique(php_array_map("maybe_serialize", to_remove_)))
        for value_ in to_remove_:
            if (not delete_metadata(meta_type_, object_id_, wp_slash(meta_key_), wp_slash(value_))):
                return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", php_sprintf(__("Could not update the meta value of %s in database."), meta_key_), Array({"key": name_, "status": WP_Http.INTERNAL_SERVER_ERROR})))
            # end if
        # end for
        for value_ in to_add_:
            if (not add_metadata(meta_type_, object_id_, wp_slash(meta_key_), wp_slash(value_))):
                return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", php_sprintf(__("Could not update the meta value of %s in database."), meta_key_), Array({"key": name_, "status": WP_Http.INTERNAL_SERVER_ERROR})))
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
    def update_meta_value(self, object_id_=None, meta_key_=None, name_=None, value_=None):
        
        
        meta_type_ = self.get_meta_type()
        if (not current_user_can(str("edit_") + str(meta_type_) + str("_meta"), object_id_, meta_key_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_update", php_sprintf(__("Sorry, you are not allowed to edit the %s custom field."), name_), Array({"key": name_, "status": rest_authorization_required_code()})))
        # end if
        #// Do the exact same check for a duplicate value as in update_metadata() to avoid update_metadata() returning false.
        old_value_ = get_metadata(meta_type_, object_id_, meta_key_)
        subtype_ = get_object_subtype(meta_type_, object_id_)
        args_ = self.get_registered_fields()[meta_key_]
        if 1 == php_count(old_value_):
            sanitized_ = sanitize_meta(meta_key_, value_, meta_type_, subtype_)
            if php_in_array(args_["type"], Array("string", "number", "integer", "boolean"), True):
                #// The return value of get_metadata will always be a string for scalar types.
                sanitized_ = php_str(sanitized_)
            # end if
            if sanitized_ == old_value_[0]:
                return True
            # end if
        # end if
        if (not update_metadata(meta_type_, object_id_, wp_slash(meta_key_), wp_slash_strings_only(value_))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_meta_database_error", php_sprintf(__("Could not update the meta value of %s in database."), meta_key_), Array({"key": name_, "status": WP_Http.INTERNAL_SERVER_ERROR})))
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
        
        
        registered_ = Array()
        meta_type_ = self.get_meta_type()
        meta_subtype_ = self.get_meta_subtype()
        meta_keys_ = get_registered_meta_keys(meta_type_)
        if (not php_empty(lambda : meta_subtype_)):
            meta_keys_ = php_array_merge(meta_keys_, get_registered_meta_keys(meta_type_, meta_subtype_))
        # end if
        for name_,args_ in meta_keys_:
            if php_empty(lambda : args_["show_in_rest"]):
                continue
            # end if
            rest_args_ = Array()
            if php_is_array(args_["show_in_rest"]):
                rest_args_ = args_["show_in_rest"]
            # end if
            default_args_ = Array({"name": name_, "single": args_["single"], "type": args_["type"] if (not php_empty(lambda : args_["type"])) else None, "schema": Array(), "prepare_callback": Array(self, "prepare_value")})
            default_schema_ = Array({"type": default_args_["type"], "description": "" if php_empty(lambda : args_["description"]) else args_["description"], "default": args_["default"] if (php_isset(lambda : args_["default"])) else None})
            rest_args_ = php_array_merge(default_args_, rest_args_)
            rest_args_["schema"] = php_array_merge(default_schema_, rest_args_["schema"])
            type_ = rest_args_["type"] if (not php_empty(lambda : rest_args_["type"])) else None
            type_ = rest_args_["schema"]["type"] if (not php_empty(lambda : rest_args_["schema"]["type"])) else type_
            if None == rest_args_["schema"]["default"]:
                rest_args_["schema"]["default"] = static.get_empty_value_for_type(type_)
            # end if
            rest_args_["schema"] = self.default_additional_properties_to_false(rest_args_["schema"])
            if (not php_in_array(type_, Array("string", "boolean", "integer", "number", "array", "object"), True)):
                continue
            # end if
            if php_empty(lambda : rest_args_["single"]):
                rest_args_["schema"] = Array({"type": "array", "items": rest_args_["schema"]})
            # end if
            registered_[name_] = rest_args_
        # end for
        return registered_
    # end def get_registered_fields
    #// 
    #// Retrieves the object's meta schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Field schema data.
    #//
    def get_field_schema(self):
        
        
        fields_ = self.get_registered_fields()
        schema_ = Array({"description": __("Meta fields."), "type": "object", "context": Array("view", "edit"), "properties": Array(), "arg_options": Array({"sanitize_callback": None, "validate_callback": Array(self, "check_meta_is_array")})})
        for args_ in fields_:
            schema_["properties"][args_["name"]] = args_["schema"]
        # end for
        return schema_
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
    def prepare_value(self, value_=None, request_=None, args_=None):
        
        
        if args_["single"]:
            schema_ = args_["schema"]
        else:
            schema_ = args_["schema"]["items"]
        # end if
        if "" == value_ and php_in_array(schema_["type"], Array("boolean", "integer", "number"), True):
            value_ = static.get_empty_value_for_type(schema_["type"])
        # end if
        if is_wp_error(rest_validate_value_from_schema(value_, schema_)):
            return None
        # end if
        return rest_sanitize_value_from_schema(value_, schema_)
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
    def check_meta_is_array(self, value_=None, request_=None, param_=None):
        
        
        if (not php_is_array(value_)):
            return False
        # end if
        return value_
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
    def default_additional_properties_to_false(self, schema_=None):
        
        
        for case in Switch(schema_["type"]):
            if case("object"):
                for key_,child_schema_ in schema_["properties"]:
                    schema_["properties"][key_] = self.default_additional_properties_to_false(child_schema_)
                # end for
                if (not (php_isset(lambda : schema_["additionalProperties"]))):
                    schema_["additionalProperties"] = False
                # end if
                break
            # end if
            if case("array"):
                schema_["items"] = self.default_additional_properties_to_false(schema_["items"])
                break
            # end if
        # end for
        return schema_
    # end def default_additional_properties_to_false
    #// 
    #// Gets the empty value for a schema type.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $type The schema type.
    #// @return mixed
    #//
    def get_empty_value_for_type(self, type_=None):
        
        
        for case in Switch(type_):
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
