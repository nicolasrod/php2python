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
#// REST API: WP_REST_Themes_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 5.0.0
#// 
#// 
#// Core class used to manage themes via the REST API.
#// 
#// @since 5.0.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Themes_Controller(WP_REST_Controller):
    #// 
    #// Constructor.
    #// 
    #// @since 5.0.0
    #//
    def __init__(self):
        
        
        self.namespace = "wp/v2"
        self.rest_base = "themes"
    # end def __init__
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 5.0.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        
        register_rest_route(self.namespace, "/" + self.rest_base, Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permissions_check"), "args": self.get_collection_params()}), {"schema": Array(self, "get_item_schema")}))
    # end def register_routes
    #// 
    #// Checks if a given request has access to read the theme.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, otherwise WP_Error object.
    #//
    def get_items_permissions_check(self, request_=None):
        
        
        if current_user_can("edit_posts"):
            return True
        # end if
        for post_type_ in get_post_types(Array({"show_in_rest": True}), "objects"):
            if current_user_can(post_type_.cap.edit_posts):
                return True
            # end if
        # end for
        return php_new_class("WP_Error", lambda : WP_Error("rest_user_cannot_view", __("Sorry, you are not allowed to view themes."), Array({"status": rest_authorization_required_code()})))
    # end def get_items_permissions_check
    #// 
    #// Retrieves a collection of themes.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request_=None):
        
        
        #// Retrieve the list of registered collection query parameters.
        registered_ = self.get_collection_params()
        themes_ = Array()
        if (php_isset(lambda : registered_["status"]) and php_isset(lambda : request_["status"])) and php_in_array("active", request_["status"], True):
            active_theme_ = wp_get_theme()
            active_theme_ = self.prepare_item_for_response(active_theme_, request_)
            themes_[-1] = self.prepare_response_for_collection(active_theme_)
        # end if
        response_ = rest_ensure_response(themes_)
        response_.header("X-WP-Total", php_count(themes_))
        response_.header("X-WP-TotalPages", php_count(themes_))
        return response_
    # end def get_items
    #// 
    #// Prepares a single theme output for response.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_Theme        $theme   Theme object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, theme_=None, request_=None):
        
        
        data_ = Array()
        fields_ = self.get_fields_for_response(request_)
        if php_in_array("theme_supports", fields_, True):
            item_schemas_ = self.get_item_schema()
            theme_supports_ = item_schemas_["properties"]["theme_supports"]["properties"]
            for name_,schema_ in theme_supports_:
                if "formats" == name_:
                    continue
                # end if
                if (not current_theme_supports(name_)):
                    data_["theme_supports"][name_] = False
                    continue
                # end if
                if "boolean" == schema_["type"]:
                    data_["theme_supports"][name_] = True
                    continue
                # end if
                support_ = get_theme_support(name_)
                if php_is_array(support_):
                    #// None of the Core theme supports have variadic args.
                    support_ = support_[0]
                    #// Core multi-type theme-support schema definitions always list boolean first.
                    if php_is_array(schema_["type"]) and "boolean" == schema_["type"][0]:
                        #// Pass the non-boolean type through to the sanitizer, which cannot itself
                        #// determine the intended type if the value is invalid (for example if an
                        #// object includes non-safelisted properties).
                        schema_["type"] = schema_["type"][1]
                    # end if
                # end if
                data_["theme_supports"][name_] = rest_sanitize_value_from_schema(support_, schema_)
            # end for
            formats_ = get_theme_support("post-formats")
            formats_ = php_array_values(formats_[0]) if php_is_array(formats_) else Array()
            formats_ = php_array_merge(Array("standard"), formats_)
            data_["theme_supports"]["formats"] = formats_
        # end if
        data_ = self.add_additional_fields_to_object(data_, request_)
        #// Wrap the data in a response object.
        response_ = rest_ensure_response(data_)
        #// 
        #// Filters theme data returned from the REST API.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_Theme         $theme    Theme object used to create response.
        #// @param WP_REST_Request  $request  Request object.
        #//
        return apply_filters("rest_prepare_theme", response_, theme_, request_)
    # end def prepare_item_for_response
    #// 
    #// Retrieves the theme's schema, conforming to JSON Schema.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "theme", "type": "object", "properties": Array({"theme_supports": Array({"description": __("Features supported by this theme."), "type": "object", "readonly": True, "properties": Array({"align-wide": Array({"description": __("Whether theme opts in to wide alignment CSS class."), "type": "boolean"})}, {"automatic-feed-links": Array({"description": __("Whether posts and comments RSS feed links are added to head."), "type": "boolean"})}, {"custom-header": Array({"description": __("Custom header if defined by the theme."), "type": Array("boolean", "object"), "properties": Array({"default-image": Array({"type": "string", "format": "uri"})}, {"random-default": Array({"type": "boolean"})}, {"width": Array({"type": "integer"})}, {"height": Array({"type": "integer"})}, {"flex-height": Array({"type": "boolean"})}, {"flex-width": Array({"type": "boolean"})}, {"default-text-color": Array({"type": "string"})}, {"header-text": Array({"type": "boolean"})}, {"uploads": Array({"type": "boolean"})}, {"video": Array({"type": "boolean"})})}, {"additionalProperties": False})}, {"custom-background": Array({"description": __("Custom background if defined by the theme."), "type": Array("boolean", "object"), "properties": Array({"default-image": Array({"type": "string", "format": "uri"})}, {"default-preset": Array({"type": "string", "enum": Array("default", "fill", "fit", "repeat", "custom")})}, {"default-position-x": Array({"type": "string", "enum": Array("left", "center", "right")})}, {"default-position-y": Array({"type": "string", "enum": Array("left", "center", "right")})}, {"default-size": Array({"type": "string", "enum": Array("auto", "contain", "cover")})}, {"default-repeat": Array({"type": "string", "enum": Array("repeat-x", "repeat-y", "repeat", "no-repeat")})}, {"default-attachment": Array({"type": "string", "enum": Array("scroll", "fixed")})}, {"default-color": Array({"type": "string"})})}, {"additionalProperties": False})}, {"custom-logo": Array({"description": __("Custom logo if defined by the theme."), "type": Array("boolean", "object"), "properties": Array({"width": Array({"type": "integer"})}, {"height": Array({"type": "integer"})}, {"flex-width": Array({"type": "boolean"})}, {"flex-height": Array({"type": "boolean"})}, {"header-text": Array({"type": "array", "items": Array({"type": "string"})})})}, {"additionalProperties": False})}, {"customize-selective-refresh-widgets": Array({"description": __("Whether the theme enables Selective Refresh for Widgets being managed with the Customizer."), "type": "boolean"})}, {"dark-editor-style": Array({"description": __("Whether theme opts in to the dark editor style UI."), "type": "boolean"})}, {"disable-custom-colors": Array({"description": __("Whether the theme disables custom colors."), "type": "boolean"})}, {"disable-custom-font-sizes": Array({"description": __("Whether the theme disables custom font sizes."), "type": "boolean"})}, {"disable-custom-gradients": Array({"description": __("Whether the theme disables custom gradients."), "type": "boolean"})}, {"editor-color-palette": Array({"description": __("Custom color palette if defined by the theme."), "type": Array("boolean", "array"), "items": Array({"type": "object", "properties": Array({"name": Array({"type": "string"})}, {"slug": Array({"type": "string"})}, {"color": Array({"type": "string"})})}, {"additionalProperties": False})})}, {"editor-font-sizes": Array({"description": __("Custom font sizes if defined by the theme."), "type": Array("boolean", "array"), "items": Array({"type": "object", "properties": Array({"name": Array({"type": "string"})}, {"size": Array({"type": "number"})}, {"slug": Array({"type": "string"})})}, {"additionalProperties": False})})}, {"editor-gradient-presets": Array({"description": __("Custom gradient presets if defined by the theme."), "type": Array("boolean", "array"), "items": Array({"type": "object", "properties": Array({"name": Array({"type": "string"})}, {"gradient": Array({"type": "string"})}, {"slug": Array({"type": "string"})})}, {"additionalProperties": False})})}, {"editor-styles": Array({"description": __("Whether theme opts in to the editor styles CSS wrapper."), "type": "boolean"})}, {"formats": Array({"description": __("Post formats supported."), "type": "array", "items": Array({"type": "string", "enum": get_post_format_slugs()})})}, {"html5": Array({"description": __("Allows use of html5 markup for search forms, comment forms, comment lists, gallery, and caption."), "type": Array("boolean", "array"), "items": Array({"type": "string", "enum": Array("search-form", "comment-form", "comment-list", "gallery", "caption", "script", "style")})})}, {"post-thumbnails": Array({"description": __("Whether the theme supports post thumbnails."), "type": Array("boolean", "array"), "items": Array({"type": "string"})})}, {"responsive-embeds": Array({"description": __("Whether the theme supports responsive embedded content."), "type": "boolean"})}, {"title-tag": Array({"description": __("Whether the theme can manage the document title tag."), "type": "boolean"})}, {"wp-block-styles": Array({"description": __("Whether theme opts in to default WordPress block styles for viewing."), "type": "boolean"})})})})})
        self.schema = schema_
        return self.add_additional_fields_schema(self.schema)
    # end def get_item_schema
    #// 
    #// Retrieves the search params for the themes collection.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Collection parameters.
    #//
    def get_collection_params(self):
        
        
        query_params_ = super().get_collection_params()
        query_params_["status"] = Array({"description": __("Limit result set to themes assigned one or more statuses."), "type": "array", "items": Array({"enum": Array("active"), "type": "string"})}, {"required": True, "sanitize_callback": Array(self, "sanitize_theme_status")})
        #// 
        #// Filter collection parameters for the themes controller.
        #// 
        #// @since 5.0.0
        #// 
        #// @param array $query_params JSON Schema-formatted collection parameters.
        #//
        return apply_filters("rest_themes_collection_params", query_params_)
    # end def get_collection_params
    #// 
    #// Sanitizes and validates the list of theme status.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string|array    $statuses  One or more theme statuses.
    #// @param WP_REST_Request $request   Full details about the request.
    #// @param string          $parameter Additional parameter to pass to validation.
    #// @return array|WP_Error A list of valid statuses, otherwise WP_Error object.
    #//
    def sanitize_theme_status(self, statuses_=None, request_=None, parameter_=None):
        
        
        statuses_ = wp_parse_slug_list(statuses_)
        for status_ in statuses_:
            result_ = rest_validate_request_arg(status_, request_, parameter_)
            if is_wp_error(result_):
                return result_
            # end if
        # end for
        return statuses_
    # end def sanitize_theme_status
# end class WP_REST_Themes_Controller
