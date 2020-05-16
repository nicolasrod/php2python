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
#// REST API: WP_REST_Taxonomies_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to manage taxonomies via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Taxonomies_Controller(WP_REST_Controller):
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #//
    def __init__(self):
        
        self.namespace = "wp/v2"
        self.rest_base = "taxonomies"
    # end def __init__
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        register_rest_route(self.namespace, "/" + self.rest_base, Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permissions_check"), "args": self.get_collection_params()}), {"schema": Array(self, "get_public_item_schema")}))
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<taxonomy>[\\w-]+)", Array({"args": Array({"taxonomy": Array({"description": __("An alphanumeric identifier for the taxonomy."), "type": "string"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks whether a given request has permission to read taxonomies.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_items_permissions_check(self, request=None):
        
        if "edit" == request["context"]:
            if (not php_empty(lambda : request["type"])):
                taxonomies = get_object_taxonomies(request["type"], "objects")
            else:
                taxonomies = get_taxonomies("", "objects")
            # end if
            for taxonomy in taxonomies:
                if (not php_empty(lambda : taxonomy.show_in_rest)) and current_user_can(taxonomy.cap.assign_terms):
                    return True
                # end if
            # end for
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_view", __("Sorry, you are not allowed to manage terms in this taxonomy."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Retrieves all public taxonomies.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request=None):
        
        #// Retrieve the list of registered collection query parameters.
        registered = self.get_collection_params()
        if (php_isset(lambda : registered["type"])) and (not php_empty(lambda : request["type"])):
            taxonomies = get_object_taxonomies(request["type"], "objects")
        else:
            taxonomies = get_taxonomies("", "objects")
        # end if
        data = Array()
        for tax_type,value in taxonomies:
            if php_empty(lambda : value.show_in_rest) or "edit" == request["context"] and (not current_user_can(value.cap.assign_terms)):
                continue
            # end if
            tax = self.prepare_item_for_response(value, request)
            tax = self.prepare_response_for_collection(tax)
            data[tax_type] = tax
        # end for
        if php_empty(lambda : data):
            #// Response should still be returned as a JSON object when it is empty.
            data = data
        # end if
        return rest_ensure_response(data)
    # end def get_items
    #// 
    #// Checks if a given request has access to a taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, otherwise false or WP_Error object.
    #//
    def get_item_permissions_check(self, request=None):
        
        tax_obj = get_taxonomy(request["taxonomy"])
        if tax_obj:
            if php_empty(lambda : tax_obj.show_in_rest):
                return False
            # end if
            if "edit" == request["context"] and (not current_user_can(tax_obj.cap.assign_terms)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to manage terms in this taxonomy."), Array({"status": rest_authorization_required_code()})))
            # end if
        # end if
        return True
    # end def get_item_permissions_check
    #// 
    #// Retrieves a specific taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request=None):
        
        tax_obj = get_taxonomy(request["taxonomy"])
        if php_empty(lambda : tax_obj):
            return php_new_class("WP_Error", lambda : WP_Error("rest_taxonomy_invalid", __("Invalid taxonomy."), Array({"status": 404})))
        # end if
        data = self.prepare_item_for_response(tax_obj, request)
        return rest_ensure_response(data)
    # end def get_item
    #// 
    #// Prepares a taxonomy object for serialization.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Taxonomy     $taxonomy Taxonomy data.
    #// @param WP_REST_Request $request  Full details about the request.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, taxonomy=None, request=None):
        
        base = taxonomy.rest_base if (not php_empty(lambda : taxonomy.rest_base)) else taxonomy.name
        fields = self.get_fields_for_response(request)
        data = Array()
        if php_in_array("name", fields, True):
            data["name"] = taxonomy.label
        # end if
        if php_in_array("slug", fields, True):
            data["slug"] = taxonomy.name
        # end if
        if php_in_array("capabilities", fields, True):
            data["capabilities"] = taxonomy.cap
        # end if
        if php_in_array("description", fields, True):
            data["description"] = taxonomy.description
        # end if
        if php_in_array("labels", fields, True):
            data["labels"] = taxonomy.labels
        # end if
        if php_in_array("types", fields, True):
            data["types"] = php_array_values(taxonomy.object_type)
        # end if
        if php_in_array("show_cloud", fields, True):
            data["show_cloud"] = taxonomy.show_tagcloud
        # end if
        if php_in_array("hierarchical", fields, True):
            data["hierarchical"] = taxonomy.hierarchical
        # end if
        if php_in_array("rest_base", fields, True):
            data["rest_base"] = base
        # end if
        if php_in_array("visibility", fields, True):
            data["visibility"] = Array({"public": php_bool(taxonomy.public), "publicly_queryable": php_bool(taxonomy.publicly_queryable), "show_admin_column": php_bool(taxonomy.show_admin_column), "show_in_nav_menus": php_bool(taxonomy.show_in_nav_menus), "show_in_quick_edit": php_bool(taxonomy.show_in_quick_edit), "show_ui": php_bool(taxonomy.show_ui)})
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        #// Wrap the data in a response object.
        response = rest_ensure_response(data)
        response.add_links(Array({"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})}, {"https://api.w.org/items": Array({"href": rest_url(php_sprintf("wp/v2/%s", base))})}))
        #// 
        #// Filters a taxonomy returned from the REST API.
        #// 
        #// Allows modification of the taxonomy data right before it is returned.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_Taxonomy      $item     The original taxonomy object.
        #// @param WP_REST_Request  $request  Request used to generate the response.
        #//
        return apply_filters("rest_prepare_taxonomy", response, taxonomy, request)
    # end def prepare_item_for_response
    #// 
    #// Retrieves the taxonomy's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "taxonomy", "type": "object", "properties": Array({"capabilities": Array({"description": __("All capabilities used by the taxonomy."), "type": "object", "context": Array("edit"), "readonly": True})}, {"description": Array({"description": __("A human-readable description of the taxonomy."), "type": "string", "context": Array("view", "edit"), "readonly": True})}, {"hierarchical": Array({"description": __("Whether or not the taxonomy should have children."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"labels": Array({"description": __("Human-readable labels for the taxonomy for various contexts."), "type": "object", "context": Array("edit"), "readonly": True})}, {"name": Array({"description": __("The title for the taxonomy."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the taxonomy."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"show_cloud": Array({"description": __("Whether or not the term cloud should be displayed."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"types": Array({"description": __("Types associated with the taxonomy."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("view", "edit"), "readonly": True})}, {"rest_base": Array({"description": __("REST base route for the taxonomy."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"visibility": Array({"description": __("The visibility settings for the taxonomy."), "type": "object", "context": Array("edit"), "readonly": True, "properties": Array({"public": Array({"description": __("Whether a taxonomy is intended for use publicly either via the admin interface or by front-end users."), "type": "boolean"})}, {"publicly_queryable": Array({"description": __("Whether the taxonomy is publicly queryable."), "type": "boolean"})}, {"show_ui": Array({"description": __("Whether to generate a default UI for managing this taxonomy."), "type": "boolean"})}, {"show_admin_column": Array({"description": __("Whether to allow automatic creation of taxonomy columns on associated post-types table."), "type": "boolean"})}, {"show_in_nav_menus": Array({"description": __("Whether to make the taxonomy available for selection in navigation menus."), "type": "boolean"})}, {"show_in_quick_edit": Array({"description": __("Whether to show the taxonomy in the quick/bulk edit panel."), "type": "boolean"})})})})})
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
        
        new_params = Array()
        new_params["context"] = self.get_context_param(Array({"default": "view"}))
        new_params["type"] = Array({"description": __("Limit results to taxonomies associated with a specific post type."), "type": "string"})
        return new_params
    # end def get_collection_params
# end class WP_REST_Taxonomies_Controller
