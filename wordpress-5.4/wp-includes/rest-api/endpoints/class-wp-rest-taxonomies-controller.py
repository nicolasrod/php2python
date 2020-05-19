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
    def get_items_permissions_check(self, request_=None):
        
        
        if "edit" == request_["context"]:
            if (not php_empty(lambda : request_["type"])):
                taxonomies_ = get_object_taxonomies(request_["type"], "objects")
            else:
                taxonomies_ = get_taxonomies("", "objects")
            # end if
            for taxonomy_ in taxonomies_:
                if (not php_empty(lambda : taxonomy_.show_in_rest)) and current_user_can(taxonomy_.cap.assign_terms):
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
    def get_items(self, request_=None):
        
        
        #// Retrieve the list of registered collection query parameters.
        registered_ = self.get_collection_params()
        if (php_isset(lambda : registered_["type"])) and (not php_empty(lambda : request_["type"])):
            taxonomies_ = get_object_taxonomies(request_["type"], "objects")
        else:
            taxonomies_ = get_taxonomies("", "objects")
        # end if
        data_ = Array()
        for tax_type_,value_ in taxonomies_.items():
            if php_empty(lambda : value_.show_in_rest) or "edit" == request_["context"] and (not current_user_can(value_.cap.assign_terms)):
                continue
            # end if
            tax_ = self.prepare_item_for_response(value_, request_)
            tax_ = self.prepare_response_for_collection(tax_)
            data_[tax_type_] = tax_
        # end for
        if php_empty(lambda : data_):
            #// Response should still be returned as a JSON object when it is empty.
            data_ = data_
        # end if
        return rest_ensure_response(data_)
    # end def get_items
    #// 
    #// Checks if a given request has access to a taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has read access for the item, otherwise false or WP_Error object.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        tax_obj_ = get_taxonomy(request_["taxonomy"])
        if tax_obj_:
            if php_empty(lambda : tax_obj_.show_in_rest):
                return False
            # end if
            if "edit" == request_["context"] and (not current_user_can(tax_obj_.cap.assign_terms)):
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
    def get_item(self, request_=None):
        
        
        tax_obj_ = get_taxonomy(request_["taxonomy"])
        if php_empty(lambda : tax_obj_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_taxonomy_invalid", __("Invalid taxonomy."), Array({"status": 404})))
        # end if
        data_ = self.prepare_item_for_response(tax_obj_, request_)
        return rest_ensure_response(data_)
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
    def prepare_item_for_response(self, taxonomy_=None, request_=None):
        
        
        base_ = taxonomy_.rest_base if (not php_empty(lambda : taxonomy_.rest_base)) else taxonomy_.name
        fields_ = self.get_fields_for_response(request_)
        data_ = Array()
        if php_in_array("name", fields_, True):
            data_["name"] = taxonomy_.label
        # end if
        if php_in_array("slug", fields_, True):
            data_["slug"] = taxonomy_.name
        # end if
        if php_in_array("capabilities", fields_, True):
            data_["capabilities"] = taxonomy_.cap
        # end if
        if php_in_array("description", fields_, True):
            data_["description"] = taxonomy_.description
        # end if
        if php_in_array("labels", fields_, True):
            data_["labels"] = taxonomy_.labels
        # end if
        if php_in_array("types", fields_, True):
            data_["types"] = php_array_values(taxonomy_.object_type)
        # end if
        if php_in_array("show_cloud", fields_, True):
            data_["show_cloud"] = taxonomy_.show_tagcloud
        # end if
        if php_in_array("hierarchical", fields_, True):
            data_["hierarchical"] = taxonomy_.hierarchical
        # end if
        if php_in_array("rest_base", fields_, True):
            data_["rest_base"] = base_
        # end if
        if php_in_array("visibility", fields_, True):
            data_["visibility"] = Array({"public": php_bool(taxonomy_.public), "publicly_queryable": php_bool(taxonomy_.publicly_queryable), "show_admin_column": php_bool(taxonomy_.show_admin_column), "show_in_nav_menus": php_bool(taxonomy_.show_in_nav_menus), "show_in_quick_edit": php_bool(taxonomy_.show_in_quick_edit), "show_ui": php_bool(taxonomy_.show_ui)})
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        #// Wrap the data in a response object.
        response_ = rest_ensure_response(data_)
        response_.add_links(Array({"collection": Array({"href": rest_url(php_sprintf("%s/%s", self.namespace, self.rest_base))})}, {"https://api.w.org/items": Array({"href": rest_url(php_sprintf("wp/v2/%s", base_))})}))
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
        return apply_filters("rest_prepare_taxonomy", response_, taxonomy_, request_)
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
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "taxonomy", "type": "object", "properties": Array({"capabilities": Array({"description": __("All capabilities used by the taxonomy."), "type": "object", "context": Array("edit"), "readonly": True})}, {"description": Array({"description": __("A human-readable description of the taxonomy."), "type": "string", "context": Array("view", "edit"), "readonly": True})}, {"hierarchical": Array({"description": __("Whether or not the taxonomy should have children."), "type": "boolean", "context": Array("view", "edit"), "readonly": True})}, {"labels": Array({"description": __("Human-readable labels for the taxonomy for various contexts."), "type": "object", "context": Array("edit"), "readonly": True})}, {"name": Array({"description": __("The title for the taxonomy."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the taxonomy."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"show_cloud": Array({"description": __("Whether or not the term cloud should be displayed."), "type": "boolean", "context": Array("edit"), "readonly": True})}, {"types": Array({"description": __("Types associated with the taxonomy."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("view", "edit"), "readonly": True})}, {"rest_base": Array({"description": __("REST base route for the taxonomy."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})}, {"visibility": Array({"description": __("The visibility settings for the taxonomy."), "type": "object", "context": Array("edit"), "readonly": True, "properties": Array({"public": Array({"description": __("Whether a taxonomy is intended for use publicly either via the admin interface or by front-end users."), "type": "boolean"})}, {"publicly_queryable": Array({"description": __("Whether the taxonomy is publicly queryable."), "type": "boolean"})}, {"show_ui": Array({"description": __("Whether to generate a default UI for managing this taxonomy."), "type": "boolean"})}, {"show_admin_column": Array({"description": __("Whether to allow automatic creation of taxonomy columns on associated post-types table."), "type": "boolean"})}, {"show_in_nav_menus": Array({"description": __("Whether to make the taxonomy available for selection in navigation menus."), "type": "boolean"})}, {"show_in_quick_edit": Array({"description": __("Whether to show the taxonomy in the quick/bulk edit panel."), "type": "boolean"})})})})})
        self.schema = schema_
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
        
        
        new_params_ = Array()
        new_params_["context"] = self.get_context_param(Array({"default": "view"}))
        new_params_["type"] = Array({"description": __("Limit results to taxonomies associated with a specific post type."), "type": "string"})
        return new_params_
    # end def get_collection_params
# end class WP_REST_Taxonomies_Controller
