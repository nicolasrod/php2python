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
    #// 
    #// Taxonomy key.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    taxonomy = Array()
    #// 
    #// Instance of a term meta fields object.
    #// 
    #// @since 4.7.0
    #// @var WP_REST_Term_Meta_Fields
    #//
    meta = Array()
    #// 
    #// Column to have the terms be sorted by.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    sort_column = Array()
    #// 
    #// Number of terms that were found.
    #// 
    #// @since 4.7.0
    #// @var int
    #//
    total_terms = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $taxonomy Taxonomy key.
    #//
    def __init__(self, taxonomy_=None):
        
        
        self.taxonomy = taxonomy_
        self.namespace = "wp/v2"
        tax_obj_ = get_taxonomy(taxonomy_)
        self.rest_base = tax_obj_.rest_base if (not php_empty(lambda : tax_obj_.rest_base)) else tax_obj_.name
        self.meta = php_new_class("WP_REST_Term_Meta_Fields", lambda : WP_REST_Term_Meta_Fields(taxonomy_))
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
    def get_items_permissions_check(self, request_=None):
        
        
        tax_obj_ = get_taxonomy(self.taxonomy)
        if (not tax_obj_) or (not self.check_is_taxonomy_allowed(self.taxonomy)):
            return False
        # end if
        if "edit" == request_["context"] and (not current_user_can(tax_obj_.cap.edit_terms)):
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
    def get_items(self, request_=None):
        
        
        #// Retrieve the list of registered collection query parameters.
        registered_ = self.get_collection_params()
        #// 
        #// This array defines mappings between public API query parameters whose
        #// values are accepted as-passed, and their internal WP_Query parameter
        #// name equivalents (some are the same). Only values which are also
        #// present in $registered will be set.
        #//
        parameter_mappings_ = Array({"exclude": "exclude", "include": "include", "order": "order", "orderby": "orderby", "post": "post", "hide_empty": "hide_empty", "per_page": "number", "search": "search", "slug": "slug"})
        prepared_args_ = Array({"taxonomy": self.taxonomy})
        #// 
        #// For each known parameter which is both registered and present in the request,
        #// set the parameter's value on the query $prepared_args.
        #//
        for api_param_,wp_param_ in parameter_mappings_.items():
            if (php_isset(lambda : registered_[api_param_]) and php_isset(lambda : request_[api_param_])):
                prepared_args_[wp_param_] = request_[api_param_]
            # end if
        # end for
        if (php_isset(lambda : prepared_args_["orderby"])) and (php_isset(lambda : request_["orderby"])):
            orderby_mappings_ = Array({"include_slugs": "slug__in"})
            if (php_isset(lambda : orderby_mappings_[request_["orderby"]])):
                prepared_args_["orderby"] = orderby_mappings_[request_["orderby"]]
            # end if
        # end if
        if (php_isset(lambda : registered_["offset"])) and (not php_empty(lambda : request_["offset"])):
            prepared_args_["offset"] = request_["offset"]
        else:
            prepared_args_["offset"] = request_["page"] - 1 * prepared_args_["number"]
        # end if
        taxonomy_obj_ = get_taxonomy(self.taxonomy)
        if taxonomy_obj_.hierarchical and (php_isset(lambda : registered_["parent"]) and php_isset(lambda : request_["parent"])):
            if 0 == request_["parent"]:
                #// Only query top-level terms.
                prepared_args_["parent"] = 0
            else:
                if request_["parent"]:
                    prepared_args_["parent"] = request_["parent"]
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
        prepared_args_ = apply_filters(str("rest_") + str(self.taxonomy) + str("_query"), prepared_args_, request_)
        if (not php_empty(lambda : prepared_args_["post"])):
            query_result_ = wp_get_object_terms(prepared_args_["post"], self.taxonomy, prepared_args_)
            #// Used when calling wp_count_terms() below.
            prepared_args_["object_ids"] = prepared_args_["post"]
        else:
            query_result_ = get_terms(prepared_args_)
        # end if
        count_args_ = prepared_args_
        count_args_["number"] = None
        count_args_["offset"] = None
        total_terms_ = wp_count_terms(self.taxonomy, count_args_)
        #// wp_count_terms() can return a falsy value when the term has no children.
        if (not total_terms_):
            total_terms_ = 0
        # end if
        response_ = Array()
        for term_ in query_result_:
            data_ = self.prepare_item_for_response(term_, request_)
            response_[-1] = self.prepare_response_for_collection(data_)
        # end for
        response_ = rest_ensure_response(response_)
        #// Store pagination values for headers.
        per_page_ = php_int(prepared_args_["number"])
        page_ = ceil(php_int(prepared_args_["offset"]) / per_page_ + 1)
        response_.header("X-WP-Total", php_int(total_terms_))
        max_pages_ = ceil(total_terms_ / per_page_)
        response_.header("X-WP-TotalPages", php_int(max_pages_))
        base_ = add_query_arg(urlencode_deep(request_.get_query_params()), rest_url(self.namespace + "/" + self.rest_base))
        if page_ > 1:
            prev_page_ = page_ - 1
            if prev_page_ > max_pages_:
                prev_page_ = max_pages_
            # end if
            prev_link_ = add_query_arg("page", prev_page_, base_)
            response_.link_header("prev", prev_link_)
        # end if
        if max_pages_ > page_:
            next_page_ = page_ + 1
            next_link_ = add_query_arg("page", next_page_, base_)
            response_.link_header("next", next_link_)
        # end if
        return response_
    # end def get_items
    #// 
    #// Get the term, if the ID is valid.
    #// 
    #// @since 4.7.2
    #// 
    #// @param int $id Supplied ID.
    #// @return WP_Term|WP_Error Term object if ID is valid, WP_Error otherwise.
    #//
    def get_term(self, id_=None):
        
        
        error_ = php_new_class("WP_Error", lambda : WP_Error("rest_term_invalid", __("Term does not exist."), Array({"status": 404})))
        if (not self.check_is_taxonomy_allowed(self.taxonomy)):
            return error_
        # end if
        if php_int(id_) <= 0:
            return error_
        # end if
        term_ = get_term(php_int(id_), self.taxonomy)
        if php_empty(lambda : term_) or term_.taxonomy != self.taxonomy:
            return error_
        # end if
        return term_
    # end def get_term
    #// 
    #// Checks if a request has access to read or edit the specified term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has read access for the item, otherwise false or WP_Error object.
    #//
    def get_item_permissions_check(self, request_=None):
        
        
        term_ = self.get_term(request_["id"])
        if is_wp_error(term_):
            return term_
        # end if
        if "edit" == request_["context"] and (not current_user_can("edit_term", term_.term_id)):
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
    def get_item(self, request_=None):
        
        
        term_ = self.get_term(request_["id"])
        if is_wp_error(term_):
            return term_
        # end if
        response_ = self.prepare_item_for_response(term_, request_)
        return rest_ensure_response(response_)
    # end def get_item
    #// 
    #// Checks if a request has access to create a term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to create items, false or WP_Error object otherwise.
    #//
    def create_item_permissions_check(self, request_=None):
        
        
        if (not self.check_is_taxonomy_allowed(self.taxonomy)):
            return False
        # end if
        taxonomy_obj_ = get_taxonomy(self.taxonomy)
        if is_taxonomy_hierarchical(self.taxonomy) and (not current_user_can(taxonomy_obj_.cap.edit_terms)) or (not is_taxonomy_hierarchical(self.taxonomy)) and (not current_user_can(taxonomy_obj_.cap.assign_terms)):
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
    def create_item(self, request_=None):
        
        
        if (php_isset(lambda : request_["parent"])):
            if (not is_taxonomy_hierarchical(self.taxonomy)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_taxonomy_not_hierarchical", __("Cannot set parent term, taxonomy is not hierarchical."), Array({"status": 400})))
            # end if
            parent_ = get_term(php_int(request_["parent"]), self.taxonomy)
            if (not parent_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_term_invalid", __("Parent term does not exist."), Array({"status": 400})))
            # end if
        # end if
        prepared_term_ = self.prepare_item_for_database(request_)
        term_ = wp_insert_term(wp_slash(prepared_term_.name), self.taxonomy, wp_slash(prepared_term_))
        if is_wp_error(term_):
            #// 
            #// If we're going to inform the client that the term already exists,
            #// give them the identifier for future use.
            #//
            term_id_ = term_.get_error_data("term_exists")
            if term_id_:
                existing_term_ = get_term(term_id_, self.taxonomy)
                term_.add_data(existing_term_.term_id, "term_exists")
                term_.add_data(Array({"status": 400, "term_id": term_id_}))
            # end if
            return term_
        # end if
        term_ = get_term(term_["term_id"], self.taxonomy)
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
        do_action(str("rest_insert_") + str(self.taxonomy), term_, request_, True)
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], term_.term_id)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        fields_update_ = self.update_additional_fields_for_object(term_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
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
        do_action(str("rest_after_insert_") + str(self.taxonomy), term_, request_, True)
        response_ = self.prepare_item_for_response(term_, request_)
        response_ = rest_ensure_response(response_)
        response_.set_status(201)
        response_.header("Location", rest_url(self.namespace + "/" + self.rest_base + "/" + term_.term_id))
        return response_
    # end def create_item
    #// 
    #// Checks if a request has access to update the specified term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to update the item, false or WP_Error object otherwise.
    #//
    def update_item_permissions_check(self, request_=None):
        
        
        term_ = self.get_term(request_["id"])
        if is_wp_error(term_):
            return term_
        # end if
        if (not current_user_can("edit_term", term_.term_id)):
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
    def update_item(self, request_=None):
        
        
        term_ = self.get_term(request_["id"])
        if is_wp_error(term_):
            return term_
        # end if
        if (php_isset(lambda : request_["parent"])):
            if (not is_taxonomy_hierarchical(self.taxonomy)):
                return php_new_class("WP_Error", lambda : WP_Error("rest_taxonomy_not_hierarchical", __("Cannot set parent term, taxonomy is not hierarchical."), Array({"status": 400})))
            # end if
            parent_ = get_term(php_int(request_["parent"]), self.taxonomy)
            if (not parent_):
                return php_new_class("WP_Error", lambda : WP_Error("rest_term_invalid", __("Parent term does not exist."), Array({"status": 400})))
            # end if
        # end if
        prepared_term_ = self.prepare_item_for_database(request_)
        #// Only update the term if we have something to update.
        if (not php_empty(lambda : prepared_term_)):
            update_ = wp_update_term(term_.term_id, term_.taxonomy, wp_slash(prepared_term_))
            if is_wp_error(update_):
                return update_
            # end if
        # end if
        term_ = get_term(term_.term_id, self.taxonomy)
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-terms-controller.php
        do_action(str("rest_insert_") + str(self.taxonomy), term_, request_, False)
        schema_ = self.get_item_schema()
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], term_.term_id)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        fields_update_ = self.update_additional_fields_for_object(term_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-terms-controller.php
        do_action(str("rest_after_insert_") + str(self.taxonomy), term_, request_, False)
        response_ = self.prepare_item_for_response(term_, request_)
        return rest_ensure_response(response_)
    # end def update_item
    #// 
    #// Checks if a request has access to delete the specified term.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return bool|WP_Error True if the request has access to delete the item, otherwise false or WP_Error object.
    #//
    def delete_item_permissions_check(self, request_=None):
        
        
        term_ = self.get_term(request_["id"])
        if is_wp_error(term_):
            return term_
        # end if
        if (not current_user_can("delete_term", term_.term_id)):
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
    def delete_item(self, request_=None):
        
        
        term_ = self.get_term(request_["id"])
        if is_wp_error(term_):
            return term_
        # end if
        force_ = php_bool(request_["force"]) if (php_isset(lambda : request_["force"])) else False
        #// We don't support trashing for terms.
        if (not force_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_trash_not_supported", php_sprintf(__("Terms do not support trashing. Set '%s' to delete."), "force=true"), Array({"status": 501})))
        # end if
        request_.set_param("context", "view")
        previous_ = self.prepare_item_for_response(term_, request_)
        retval_ = wp_delete_term(term_.term_id, term_.taxonomy)
        if (not retval_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_delete", __("The term cannot be deleted."), Array({"status": 500})))
        # end if
        response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
        response_.set_data(Array({"deleted": True, "previous": previous_.get_data()}))
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
        do_action(str("rest_delete_") + str(self.taxonomy), term_, response_, request_)
        return response_
    # end def delete_item
    #// 
    #// Prepares a single term for create or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return object $prepared_term Term object.
    #//
    def prepare_item_for_database(self, request_=None):
        
        
        prepared_term_ = php_new_class("stdClass", lambda : stdClass())
        schema_ = self.get_item_schema()
        if (php_isset(lambda : request_["name"])) and (not php_empty(lambda : schema_["properties"]["name"])):
            prepared_term_.name = request_["name"]
        # end if
        if (php_isset(lambda : request_["slug"])) and (not php_empty(lambda : schema_["properties"]["slug"])):
            prepared_term_.slug = request_["slug"]
        # end if
        if (php_isset(lambda : request_["taxonomy"])) and (not php_empty(lambda : schema_["properties"]["taxonomy"])):
            prepared_term_.taxonomy = request_["taxonomy"]
        # end if
        if (php_isset(lambda : request_["description"])) and (not php_empty(lambda : schema_["properties"]["description"])):
            prepared_term_.description = request_["description"]
        # end if
        if (php_isset(lambda : request_["parent"])) and (not php_empty(lambda : schema_["properties"]["parent"])):
            parent_term_id_ = 0
            requested_parent_ = php_int(request_["parent"])
            if requested_parent_:
                parent_term_ = get_term(requested_parent_, self.taxonomy)
                if type(parent_term_).__name__ == "WP_Term":
                    parent_term_id_ = parent_term_.term_id
                # end if
            # end if
            prepared_term_.parent = parent_term_id_
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
        return apply_filters(str("rest_pre_insert_") + str(self.taxonomy), prepared_term_, request_)
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
    def prepare_item_for_response(self, item_=None, request_=None):
        
        
        fields_ = self.get_fields_for_response(request_)
        data_ = Array()
        if php_in_array("id", fields_, True):
            data_["id"] = php_int(item_.term_id)
        # end if
        if php_in_array("count", fields_, True):
            data_["count"] = php_int(item_.count)
        # end if
        if php_in_array("description", fields_, True):
            data_["description"] = item_.description
        # end if
        if php_in_array("link", fields_, True):
            data_["link"] = get_term_link(item_)
        # end if
        if php_in_array("name", fields_, True):
            data_["name"] = item_.name
        # end if
        if php_in_array("slug", fields_, True):
            data_["slug"] = item_.slug
        # end if
        if php_in_array("taxonomy", fields_, True):
            data_["taxonomy"] = item_.taxonomy
        # end if
        if php_in_array("parent", fields_, True):
            data_["parent"] = php_int(item_.parent)
        # end if
        if php_in_array("meta", fields_, True):
            data_["meta"] = self.meta.get_value(item_.term_id, request_)
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.add_additional_fields_to_object(data_, request_)
        data_ = self.filter_response_by_context(data_, context_)
        response_ = rest_ensure_response(data_)
        response_.add_links(self.prepare_links(item_))
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
        return apply_filters(str("rest_prepare_") + str(self.taxonomy), response_, item_, request_)
    # end def prepare_item_for_response
    #// 
    #// Prepares links for the request.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Term $term Term object.
    #// @return array Links for the given term.
    #//
    def prepare_links(self, term_=None):
        
        
        base_ = self.namespace + "/" + self.rest_base
        links_ = Array({"self": Array({"href": rest_url(trailingslashit(base_) + term_.term_id)})}, {"collection": Array({"href": rest_url(base_)})}, {"about": Array({"href": rest_url(php_sprintf("wp/v2/taxonomies/%s", self.taxonomy))})})
        if term_.parent:
            parent_term_ = get_term(php_int(term_.parent), term_.taxonomy)
            if parent_term_:
                links_["up"] = Array({"href": rest_url(trailingslashit(base_) + parent_term_.term_id), "embeddable": True})
            # end if
        # end if
        taxonomy_obj_ = get_taxonomy(term_.taxonomy)
        if php_empty(lambda : taxonomy_obj_.object_type):
            return links_
        # end if
        post_type_links_ = Array()
        for type_ in taxonomy_obj_.object_type:
            post_type_object_ = get_post_type_object(type_)
            if php_empty(lambda : post_type_object_.show_in_rest):
                continue
            # end if
            rest_base_ = post_type_object_.rest_base if (not php_empty(lambda : post_type_object_.rest_base)) else post_type_object_.name
            post_type_links_[-1] = Array({"href": add_query_arg(self.rest_base, term_.term_id, rest_url(php_sprintf("wp/v2/%s", rest_base_)))})
        # end for
        if (not php_empty(lambda : post_type_links_)):
            links_["https://api.w.org/post_type"] = post_type_links_
        # end if
        return links_
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
        schema_ = Array({"$schema": "http://json-schema.org/draft-04/schema#", "title": "tag" if "post_tag" == self.taxonomy else self.taxonomy, "type": "object", "properties": Array({"id": Array({"description": __("Unique identifier for the term."), "type": "integer", "context": Array("view", "embed", "edit"), "readonly": True})}, {"count": Array({"description": __("Number of published posts for the term."), "type": "integer", "context": Array("view", "edit"), "readonly": True})}, {"description": Array({"description": __("HTML description of the term."), "type": "string", "context": Array("view", "edit")})}, {"link": Array({"description": __("URL of the term."), "type": "string", "format": "uri", "context": Array("view", "embed", "edit"), "readonly": True})}, {"name": Array({"description": __("HTML title for the term."), "type": "string", "context": Array("view", "embed", "edit"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})}, {"required": True})}, {"slug": Array({"description": __("An alphanumeric identifier for the term unique to its type."), "type": "string", "context": Array("view", "embed", "edit"), "arg_options": Array({"sanitize_callback": Array(self, "sanitize_slug")})})}, {"taxonomy": Array({"description": __("Type attribution for the term."), "type": "string", "enum": php_array_keys(get_taxonomies()), "context": Array("view", "embed", "edit"), "readonly": True})})})
        taxonomy_ = get_taxonomy(self.taxonomy)
        if taxonomy_.hierarchical:
            schema_["properties"]["parent"] = Array({"description": __("The parent term ID."), "type": "integer", "context": Array("view", "edit")})
        # end if
        schema_["properties"]["meta"] = self.meta.get_field_schema()
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
        
        
        query_params_ = super().get_collection_params()
        taxonomy_ = get_taxonomy(self.taxonomy)
        query_params_["context"]["default"] = "view"
        query_params_["exclude"] = Array({"description": __("Ensure result set excludes specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        query_params_["include"] = Array({"description": __("Limit result set to specific IDs."), "type": "array", "items": Array({"type": "integer"})}, {"default": Array()})
        if (not taxonomy_.hierarchical):
            query_params_["offset"] = Array({"description": __("Offset the result set by a specific number of items."), "type": "integer"})
        # end if
        query_params_["order"] = Array({"description": __("Order sort attribute ascending or descending."), "type": "string", "default": "asc", "enum": Array("asc", "desc")})
        query_params_["orderby"] = Array({"description": __("Sort collection by term attribute."), "type": "string", "default": "name", "enum": Array("id", "include", "name", "slug", "include_slugs", "term_group", "description", "count")})
        query_params_["hide_empty"] = Array({"description": __("Whether to hide terms not assigned to any posts."), "type": "boolean", "default": False})
        if taxonomy_.hierarchical:
            query_params_["parent"] = Array({"description": __("Limit result set to terms assigned to a specific parent."), "type": "integer"})
        # end if
        query_params_["post"] = Array({"description": __("Limit result set to terms assigned to a specific post."), "type": "integer", "default": None})
        query_params_["slug"] = Array({"description": __("Limit result set to terms with one or more specific slugs."), "type": "array", "items": Array({"type": "string"})})
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
        return apply_filters(str("rest_") + str(self.taxonomy) + str("_collection_params"), query_params_, taxonomy_)
    # end def get_collection_params
    #// 
    #// Checks that the taxonomy is valid.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $taxonomy Taxonomy to check.
    #// @return bool Whether the taxonomy is allowed for REST management.
    #//
    def check_is_taxonomy_allowed(self, taxonomy_=None):
        
        
        taxonomy_obj_ = get_taxonomy(taxonomy_)
        if taxonomy_obj_ and (not php_empty(lambda : taxonomy_obj_.show_in_rest)):
            return True
        # end if
        return False
    # end def check_is_taxonomy_allowed
# end class WP_REST_Terms_Controller
