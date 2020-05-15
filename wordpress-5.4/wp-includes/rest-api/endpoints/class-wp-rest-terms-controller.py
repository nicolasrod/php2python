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
#// REST API: WP_REST_Terms_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to managed terms associated with a taxonomy via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Controller
#//
class WP_REST_Terms_Controller(WP_REST_Controller):
    taxonomy = Array()
    meta = Array()
    sort_column = Array()
    total_terms = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $taxonomy Taxonomy key.
    #//
    def __init__(self, taxonomy=None):
        
        self.taxonomy = taxonomy
        self.namespace = "wp/v2"
        tax_obj = get_taxonomy(taxonomy)
        self.rest_base = tax_obj.rest_base if (not php_empty(lambda : tax_obj.rest_base)) else tax_obj.name
        self.meta = php_new_class("WP_REST_Term_Meta_Fields", lambda : WP_REST_Term_Meta_Fields(taxonomy))
    # end def __init__
    #// 
    #// Registers the routes for the objects of the controller.
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        register_rest_route(self.namespace, "/" + self.rest_base, Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_items"), "permission_callback": Array(self, "get_items_permissions_check"), "args": self.get_collection_params()}), Array({"methods": WP_REST_Server.CREATABLE, "callback": Array(self, "create_item"), "permission_callback": Array(self, "create_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.CREATABLE)}), {"schema": Array(self, "get_public_item_schema")}))
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<id>[\\d]+)", Array({"args": Array({"id": Array({"description": __("Unique identifier for the term."), "type": "integer"})})}, Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "permission_callback": Array(self, "get_item_permissions_check"), "args": Array({"context": self.get_context_param(Array({"default": "view"}))})}), Array({"methods": WP_REST_Server.EDITABLE, "callback": Array(self, "update_item"), "permission_callback": Array(self, "update_item_permissions_check"), "args": self.get_endpoint_args_for_item_schema(WP_REST_Server.EDITABLE)}), Array({"methods": WP_REST_Server.DELETABLE, "callback": Array(self, "delete_item"), "permission_callback": Array(self, "delete_item_permissions_check"), "args": Array({"force": Array({"type": "boolean", "default": False, "description": __("Required to be true, as terms do not support trashing.")})})}), {"schema": Array(self, "get_public_item_schema")}))
    # end def register_routes
    #// 
    #// Checks if a request has access to read terms in the specified taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has read access, otherwise false or WP_Error object.
    #//
    def get_items_permissions_check(self, request=None):
        
        tax_obj = get_taxonomy(self.taxonomy)
        if (not tax_obj) or (not self.check_is_taxonomy_allowed(self.taxonomy)):
            return False
        # end if
        if "edit" == request["context"] and (not current_user_can(tax_obj.cap.edit_terms)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit terms in this taxonomy."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_items_permissions_check
    #// 
    #// Retrieves terms associated with a taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_items(self, request=None):
        
        #// Retrieve the list of registered collection query parameters.
        registered = self.get_collection_params()
        #// 
        #// This array defines mappings between public API query parameters whose
        #// values are accepted as-passed, and their internal WP_Query parameter
        #// name equivalents (some are the same). Only values which are also
        #// present in $registered will be set.
        #//
        parameter_mappings = Array({"exclude": "exclude", "include": "include", "order": "order", "orderby": "orderby", "post": "post", "hide_empty": "hide_empty", "per_page": "number", "search": "search", "slug": "slug"})
        prepared_args = Array({"taxonomy": self.taxonomy})
        #// 
        #// For each known parameter which is both registered and present in the request,
        #// set the parameter's value on the query $prepared_args.
        #//
        for api_param,wp_param in parameter_mappings:
            if (php_isset(lambda : registered[api_param]) and php_isset(lambda : request[api_param])):
                prepared_args[wp_param] = request[api_param]
            # end if
        # end for
        if (php_isset(lambda : prepared_args["orderby"])) and (php_isset(lambda : request["orderby"])):
            orderby_mappings = Array({"include_slugs": "slug__in"})
            if (php_isset(lambda : orderby_mappings[request["orderby"]])):
                prepared_args["orderby"] = orderby_mappings[request["orderby"]]
            # end if
        # end if
        if (php_isset(lambda : registered["offset"])) and (not php_empty(lambda : request["offset"])):
            prepared_args["offset"] = request["offset"]
        else:
            prepared_args["offset"] = request["page"] - 1 * prepared_args["number"]
        # end if
        taxonomy_obj = get_taxonomy(self.taxonomy)
        if taxonomy_obj.hierarchical and (php_isset(lambda : registered["parent"]) and php_isset(lambda : request["parent"])):
            if 0 == request["parent"]:
                #// Only query top-level terms.
                prepared_args["parent"] = 0
            else:
                if request["parent"]:
                    prepared_args["parent"] = request["parent"]
                # end if
            # end if
        # end if
        #// 
        #// Filters the query arguments before passing them to get_terms().
        #// 
        #// The dynamic portion of the hook name, `$this->taxonomy`, refers to the taxonomy slug.
        #// 
        #// Enables adding extra arguments or setting defaults for a terms
        #// collection request.
        #// 
        #// @since 4.7.0
        #// 
        #// @link https://developer.wordpress.org/reference/functions/get_terms
        #// 
        #// @param array           $prepared_args Array of arguments to be
        #// passed to get_terms().
        #// @param WP_REST_Request $request       The current request.
        #//
        prepared_args = apply_filters(str("rest_") + str(self.taxonomy) + str("_query"), prepared_args, request)
        if (not php_empty(lambda : prepared_args["post"])):
            query_result = wp_get_object_terms(prepared_args["post"], self.taxonomy, prepared_args)
            #// Used when calling wp_count_terms() below.
            prepared_args["object_ids"] = prepared_args["post"]
        else:
            query_result = get_terms(prepared_args)
        # end if
        count_args = prepared_args
        count_args["number"] = None
        count_args["offset"] = None
        total_terms = wp_count_terms(self.taxonomy, count_args)
        #// wp_count_terms() can return a falsy value when the term has no children.
        if (not total_terms):
            total_terms = 0
        # end if
        response = Array()
        for term in query_result:
            data = self.prepare_item_for_response(term, request)
            response[-1] = self.prepare_response_for_collection(data)
        # end for
        response = rest_ensure_response(response)
        #// Store pagination values for headers.
        per_page = int(prepared_args["number"])
        page = ceil(int(prepared_args["offset"]) / per_page + 1)
        response.header("X-WP-Total", int(total_terms))
        max_pages = ceil(total_terms / per_page)
        response.header("X-WP-TotalPages", int(max_pages))
        base = add_query_arg(urlencode_deep(request.get_query_params()), rest_url(self.namespace + "/" + self.rest_base))
        if page > 1:
            prev_page = page - 1
            if prev_page > max_pages:
                prev_page = max_pages
            # end if
            prev_link = add_query_arg("page", prev_page, base)
            response.link_header("prev", prev_link)
        # end if
        if max_pages > page:
            next_page = page + 1
            next_link = add_query_arg("page", next_page, base)
            response.link_header("next", next_link)
        # end if
        return response
    # end def get_items
    #// 
    #// Get the term, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_Term|WP_Error Term object if ID is valid, WP_Error otherwise.
    #//
    def get_term(self, id=None):
        
        error = php_new_class("WP_Error", lambda : WP_Error("rest_term_invalid", __("Term does not exist."), Array({"status": 404})))
        if (not self.check_is_taxonomy_allowed(self.taxonomy)):
            return error
        # end if
        if int(id) <= 0:
            return error
        # end if
        term = get_term(int(id), self.taxonomy)
        if php_empty(lambda : term) or term.taxonomy != self.taxonomy:
            return error
        # end if
        return term
    # end def get_term
    #// 
    #// Checks if a request has access to read or edit the specified term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has read access for the item, otherwise false or WP_Error object.
    #//
    def get_item_permissions_check(self, request=None):
        
        term = self.get_term(request["id"])
        if is_wp_error(term):
            return term
        # end if
        if "edit" == request["context"] and (not current_user_can("edit_term", term.term_id)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden_context", __("Sorry, you are not allowed to edit this term."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_item_permissions_check
    #// 
    #// Gets a single term from a taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def get_item(self, request=None):
        
        term = self.get_term(request["id"])
        if is_wp_error(term):
            return term
        # end if
        response = self.prepare_item_for_response(term, request)
        return rest_ensure_response(response)
    # end def get_item
    #// 
    #// Checks if a request has access to create a term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to create items, false or WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request=None):
        
        if (not self.check_is_taxonomy_allowed(self.taxonomy)):
            return False
        # end if
        taxonomy_obj = get_taxonomy(self.taxonomy)
        if is_taxonomy_hierarchical(self.taxonomy) and (not current_user_can(taxonomy_obj.cap.edit_terms)) or (not is_taxonomy_hierarchical(self.taxonomy)) and (not current_user_can(taxonomy_obj.cap.assign_terms)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_create", __("Sorry, you are not allowed to create terms in this taxonomy."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def create_item_permissions_check
    #// 
    #// Creates a single term in a taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def create_item(self, request=None):
        
        if (php_isset(lambda : request["parent"])):
            if (not is_taxonomy_hierarchical(self.taxonomy)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_taxonomy_not_hierarchical", __("Cannot set parent term, taxonomy is not hierarchical."), Array({"status": 400})))
            # end if
            parent = get_term(int(request["parent"]), self.taxonomy)
            if (not parent):
                return php_new_class("WP_Error", lambda : WP_Error("rest_term_invalid", __("Parent term does not exist."), Array({"status": 400})))
            # end if
        # end if
        prepared_term = self.prepare_item_for_database(request)
        term = wp_insert_term(wp_slash(prepared_term.name), self.taxonomy, wp_slash(prepared_term))
        if is_wp_error(term):
            #// 
            #// If we're going to inform the client that the term already exists,
            #// give them the identifier for future use.
            #//
            term_id = term.get_error_data("term_exists")
            if term_id:
                existing_term = get_term(term_id, self.taxonomy)
                term.add_data(existing_term.term_id, "term_exists")
                term.add_data(Array({"status": 400, "term_id": term_id}))
            # end if
            return term
        # end if
        term = get_term(term["term_id"], self.taxonomy)
        #// 
        #// Fires after a single term is created or updated via the REST API.
        #// 
        #// The dynamic portion of the hook name, `$this->taxonomy`, refers to the taxonomy slug.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Term         $term     Inserted or updated term object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a term, false when updating.
        #//
        do_action(str("rest_insert_") + str(self.taxonomy), term, request, True)
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], term.term_id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        fields_update = self.update_additional_fields_for_object(term, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// 
        #// Fires after a single term is completely created or updated via the REST API.
        #// 
        #// The dynamic portion of the hook name, `$this->taxonomy`, refers to the taxonomy slug.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_Term         $term     Inserted or updated term object.
        #// @param WP_REST_Request $request  Request object.
        #// @param bool            $creating True when creating a term, false when updating.
        #//
        do_action(str("rest_after_insert_") + str(self.taxonomy), term, request, True)
        response = self.prepare_item_for_response(term, request)
        response = rest_ensure_response(response)
        response.set_status(201)
        response.header("Location", rest_url(self.namespace + "/" + self.rest_base + "/" + term.term_id))
        return response
    # end def create_item
    #// 
    #// Checks if a request has access to update the specified term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to update the item, false or WP_Error object otherwise.
    #//
    def update_item_permissions_check(self, request=None):
        
        term = self.get_term(request["id"])
        if is_wp_error(term):
            return term
        # end if
        if (not current_user_can("edit_term", term.term_id)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_update", __("Sorry, you are not allowed to edit this term."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def update_item_permissions_check
    #// 
    #// Updates a single term from a taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def update_item(self, request=None):
        
        term = self.get_term(request["id"])
        if is_wp_error(term):
            return term
        # end if
        if (php_isset(lambda : request["parent"])):
            if (not is_taxonomy_hierarchical(self.taxonomy)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_taxonomy_not_hierarchical", __("Cannot set parent term, taxonomy is not hierarchical."), Array({"status": 400})))
            # end if
            parent = get_term(int(request["parent"]), self.taxonomy)
            if (not parent):
                return php_new_class("WP_Error", lambda : WP_Error("rest_term_invalid", __("Parent term does not exist."), Array({"status": 400})))
            # end if
        # end if
        prepared_term = self.prepare_item_for_database(request)
        #// Only update the term if we have something to update.
        if (not php_empty(lambda : prepared_term)):
            update = wp_update_term(term.term_id, term.taxonomy, wp_slash(prepared_term))
            if is_wp_error(update):
                return update
            # end if
        # end if
        term = get_term(term.term_id, self.taxonomy)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-terms-controller.php
        do_action(str("rest_insert_") + str(self.taxonomy), term, request, False)
        schema = self.get_item_schema()
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], term.term_id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        fields_update = self.update_additional_fields_for_object(term, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-terms-controller.php
        do_action(str("rest_after_insert_") + str(self.taxonomy), term, request, False)
        response = self.prepare_item_for_response(term, request)
        return rest_ensure_response(response)
    # end def update_item
    #// 
    #// Checks if a request has access to delete the specified term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to delete the item, otherwise false or WP_Error object.
    #//
    def delete_item_permissions_check(self, request=None):
        
        term = self.get_term(request["id"])
        if is_wp_error(term):
            return term
        # end if
        if (not current_user_can("delete_term", term.term_id)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("Sorry, you are not allowed to delete this term."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def delete_item_permissions_check
    #// 
    #// Deletes a single term from a taxonomy.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, or WP_Error object on failure.
    #//
    def delete_item(self, request=None):
        
        term = self.get_term(request["id"])
        if is_wp_error(term):
            return term
        # end if
        force = bool(request["force"]) if (php_isset(lambda : request["force"])) else False
        #// We don't support trashing for terms.
        if (not force):
            return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("Terms do not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
        # end if
        request.set_param("context", "view")
        previous = self.prepare_item_for_response(term, request)
        retval = wp_delete_term(term.term_id, term.taxonomy)
        if (not retval):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The term cannot be deleted."), Array({"status": 500})))
        # end if
        response = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        response.set_data(Array({"deleted": True, "previous": previous.get_data()}))
        #// 
        #// Fires after a single term is deleted via the REST API.
        #// 
        #// The dynamic portion of the hook name, `$this->taxonomy`, refers to the taxonomy slug.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Term          $term     The deleted term.
        #// @param WP_REST_Response $response The response data.
        #// @param WP_REST_Request  $request  The request sent to the API.
        #//
        do_action(str("rest_delete_") + str(self.taxonomy), term, response, request)
        return response
    # end def delete_item
    #// 
    #// Prepares a single term for create or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return object $prepared_term Term object.
    #//
    def prepare_item_for_database(self, request=None):
        
        prepared_term = php_new_class("stdClass", lambda : stdClass())
        schema = self.get_item_schema()
        if (php_isset(lambda : request["name"])) and (not php_empty(lambda : schema["properties"]["name"])):
            prepared_term.name = request["name"]
        # end if
        if (php_isset(lambda : request["slug"])) and (not php_empty(lambda : schema["properties"]["slug"])):
            prepared_term.slug = request["slug"]
        # end if
        if (php_isset(lambda : request["taxonomy"])) and (not php_empty(lambda : schema["properties"]["taxonomy"])):
            prepared_term.taxonomy = request["taxonomy"]
        # end if
        if (php_isset(lambda : request["description"])) and (not php_empty(lambda : schema["properties"]["description"])):
            prepared_term.description = request["description"]
        # end if
        if (php_isset(lambda : request["parent"])) and (not php_empty(lambda : schema["properties"]["parent"])):
            parent_term_id = 0
            requested_parent = int(request["parent"])
            if requested_parent:
                parent_term = get_term(requested_parent, self.taxonomy)
                if type(parent_term).__name__ == "WP_Term":
                    parent_term_id = parent_term.term_id
                # end if
            # end if
            prepared_term.parent = parent_term_id
        # end if
        #// 
        #// Filters term data before inserting term via the REST API.
        #// 
        #// The dynamic portion of the hook name, `$this->taxonomy`, refers to the taxonomy slug.
        #// 
        #// @since 4.7.0
        #// 
        #// @param object          $prepared_term Term object.
        #// @param WP_REST_Request $request       Request object.
        #//
        return apply_filters(str("rest_pre_insert_") + str(self.taxonomy), prepared_term, request)
    # end def prepare_item_for_database
    #// 
    #// Prepares a single term output for response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Term         $item    Term object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response $response Response object.
    #//
    def prepare_item_for_response(self, item=None, request=None):
        
        fields = self.get_fields_for_response(request)
        data = Array()
        if php_in_array("id", fields, True):
            data["id"] = int(item.term_id)
        # end if
        if php_in_array("count", fields, True):
            data["count"] = int(item.count)
        # end if
        if php_in_array("description", fields, True):
            data["description"] = item.description
        # end if
        if php_in_array("link", fields, True):
            data["link"] = get_term_link(item)
        # end if
        if php_in_array("name", fields, True):
            data["name"] = item.name
        # end if
        if php_in_array("slug", fields, True):
            data["slug"] = item.slug
        # end if
        if php_in_array("taxonomy", fields, True):
            data["taxonomy"] = item.taxonomy
        # end if
        if php_in_array("parent", fields, True):
            data["parent"] = int(item.parent)
        # end if
        if php_in_array("meta", fields, True):
            data["meta"] = self.meta.get_value(item.term_id, request)
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.add_additional_fields_to_object(data, request)
        data = self.filter_response_by_context(data, context)
        response = rest_ensure_response(data)
        response.add_links(self.prepare_links(item))
        #// 
        #// Filters a term item returned from the API.
        #// 
        #// The dynamic portion of the hook name, `$this->taxonomy`, refers to the taxonomy slug.
        #// 
        #// Allows modification of the term data right before it is returned.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response  $response  The response object.
        #// @param WP_Term           $item      The original term object.
        #// @param WP_REST_Request   $request   Request used to generate the response.
        #//
        return apply_filters(str("rest_prepare_") + str(self.taxonomy), response, item, request)
    # end def prepare_item_for_response
    #// 
    #// Prepares links for the request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Term $term Term object.
    #// @return array Links for the given term.
    #//
    def prepare_links(self, term=None):
        
        base = self.namespace + "/" + self.rest_base
        links = Array({"self": Array({"href": rest_url(trailingslashit(base) + term.term_id)})}, {"collection": Array({"href": rest_url(base)})}, {"about": Array({"href": rest_url(php_sprintf("wp/v2/taxonomies/%s", self.taxonomy))})})
        if term.parent:
            parent_term = get_term(int(term.parent), term.taxonomy)
            if parent_term:
                links["up"] = Array({"href": rest_url(trailingslashit(base) + parent_term.term_id), "embeddable": True})
            # end if
        # end if
        taxonomy_obj = get_taxonomy(term.taxonomy)
        if php_empty(lambda : taxonomy_obj.object_type):
            return links
        # end if
        post_type_links = Array()
        for type in taxonomy_obj.object_type:
            post_type_object = get_post_type_object(type)
            if php_empty(lambda : post_type_object.show_in_rest):
                continue
            # end if
            rest_base = post_type_object.rest_base if (not php_empty(lambda : post_type_object.rest_base)) else post_type_object.name
            post_type_links[-1] = Array({"href": add_query_arg(self.rest_base, term.term_id, rest_url(php_sprintf("wp/v2/%s", rest_base)))})
        # end for
        if (not php_empty(lambda : post_type_links)):
            links["https://api.w.org/post_type"] = post_type_links
        # end if
        return links
    # end def prepare_links
    #// 
    #// Retrieves the term's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema data.
    #//
    def get_item_schema(self):
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "tag" if "post_tag" == self.taxonomy else self.taxonomy, "type": "object", "properties": Array({"id": Array({"description": __("Unique identifier for the term."), "type": "integer", "context": Array("view", "embed", "edit"), "readonly": True})}, {"count": Array({"description": __("Number of published posts for the term."), "type": "integer", "context": Array("view", "edit"), "readonly": True})}, {"description": Array({"description": __("HTML description of the term."), "type": "string", "context": Array("view", "edit")})}, {"link": Array({"description": __("URL of the term."), "type": "string", "format": "uri", "context": Array("view", "embed", "edit"), "readonly": True})}, {"name": Array({"description": __("HTML title for the term."), "type": "string", "context": Array("view", "embed", "edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})}, {"required": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the term unique to its type."), "type": "string", "context": Array("view", "embed", "edit"), "arg_options": Array({"sanitize_callback": Array(self, "sanitize_slug")})})}, {"taxonomy": Array({"description": __("Type attribution for the term."), "type": "string", "enum": php_array_keys(get_taxonomies()), "context": Array("view", "embed", "edit"), "readonly": True})})})
        taxonomy = get_taxonomy(self.taxonomy)
        if taxonomy.hierarchical:
            schema["properties"]["parent"] = Array({"description": __("The parent term ID."), "type": "integer", "context": Array("view", "edit")})
        # end if
        schema["properties"]["meta"] = self.meta.get_field_schema()
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
        
        query_params = super().get_collection_params()
        taxonomy = get_taxonomy(self.taxonomy)
        query_params["context"]["default"] = "view"
        query_params["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        if (not taxonomy.hierarchical):
            query_params["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        # end if
        query_params["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "asc", "enum": Array("asc", "desc")})
        query_params["orderby"] = Array({"description": __("Sort collection by term attribute."), "type": "string", "default": "name", "enum": Array("id", "include", "name", "slug", "include_slugs", "term_group", "description", "count")})
        query_params["hide_empty"] = Array({"description": __("Whether to hide terms not assigned to any posts."), "type": "boolean", "default": False})
        if taxonomy.hierarchical:
            query_params["parent"] = Array({"description": __("Limit result set to terms assigned to a specific parent."), "type": "integer"})
        # end if
        query_params["post"] = Array({"description": __("Limit result set to terms assigned to a specific post."), "type": "integer", "default": None})
        query_params["slug"] = Array({"description": __("Limit result set to terms with one or more specific slugs."), "type": "array", "items": Array({"type": "string"})})
        #// 
        #// Filter collection parameters for the terms controller.
        #// 
        #// The dynamic part of the filter `$this->taxonomy` refers to the taxonomy
        #// slug for the controller.
        #// 
        #// This filter registers the collection parameter, but does not map the
        #// collection parameter to an internal WP_Term_Query parameter.  Use the
        #// `rest_{$this->taxonomy}_query` filter to set WP_Term_Query parameters.
        #// 
        #// @since 4.7.0
        #// 
        #// @param array       $query_params JSON Schema-formatted collection parameters.
        #// @param WP_Taxonomy $taxonomy     Taxonomy object.
        #//
        return apply_filters(str("rest_") + str(self.taxonomy) + str("_collection_params"), query_params, taxonomy)
    # end def get_collection_params
    #// 
    #// Checks that the taxonomy is valid.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $taxonomy Taxonomy to check.
    #// @return bool Whether the taxonomy is allowed for REST management.
    #//
    def check_is_taxonomy_allowed(self, taxonomy=None):
        
        taxonomy_obj = get_taxonomy(taxonomy)
        if taxonomy_obj and (not php_empty(lambda : taxonomy_obj.show_in_rest)):
            return True
        # end if
        return False
    # end def check_is_taxonomy_allowed
# end class WP_REST_Terms_Controller
