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
#// REST API: WP_REST_Post_Search_Handler class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 5.0.0
#// 
#// 
#// Core class representing a search handler for posts in the REST API.
#// 
#// @since 5.0.0
#// 
#// @see WP_REST_Search_Handler
#//
class WP_REST_Post_Search_Handler(WP_REST_Search_Handler):
    #// 
    #// Constructor.
    #// 
    #// @since 5.0.0
    #//
    def __init__(self):
        
        
        self.type = "post"
        #// Support all public post types except attachments.
        self.subtypes = php_array_diff(php_array_values(get_post_types(Array({"public": True, "show_in_rest": True}), "names")), Array("attachment"))
    # end def __init__
    #// 
    #// Searches the object type content for a given search request.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_REST_Request $request Full REST request.
    #// @return array Associative array containing an `WP_REST_Search_Handler::RESULT_IDS` containing
    #// an array of found IDs and `WP_REST_Search_Handler::RESULT_TOTAL` containing the
    #// total count for the matching search results.
    #//
    def search_items(self, request_=None):
        
        
        #// Get the post types to search for the current request.
        post_types_ = request_[WP_REST_Search_Controller.PROP_SUBTYPE]
        if php_in_array(WP_REST_Search_Controller.TYPE_ANY, post_types_, True):
            post_types_ = self.subtypes
        # end if
        query_args_ = Array({"post_type": post_types_, "post_status": "publish", "paged": php_int(request_["page"]), "posts_per_page": php_int(request_["per_page"]), "ignore_sticky_posts": True, "fields": "ids"})
        if (not php_empty(lambda : request_["search"])):
            query_args_["s"] = request_["search"]
        # end if
        #// 
        #// Filters the query arguments for a search request.
        #// 
        #// Enables adding extra arguments or setting defaults for a post search request.
        #// 
        #// @since 5.1.0
        #// 
        #// @param array           $query_args Key value array of query var to query value.
        #// @param WP_REST_Request $request    The request used.
        #//
        query_args_ = apply_filters("rest_post_search_query", query_args_, request_)
        query_ = php_new_class("WP_Query", lambda : WP_Query())
        found_ids_ = query_.query(query_args_)
        total_ = query_.found_posts
        return Array({self.RESULT_IDS: found_ids_, self.RESULT_TOTAL: total_})
    # end def search_items
    #// 
    #// Prepares the search result for a given ID.
    #// 
    #// @since 5.0.0
    #// 
    #// @param int   $id     Item ID.
    #// @param array $fields Fields to include for the item.
    #// @return array Associative array containing all fields for the item.
    #//
    def prepare_item(self, id_=None, fields_=None):
        
        
        post_ = get_post(id_)
        data_ = Array()
        if php_in_array(WP_REST_Search_Controller.PROP_ID, fields_, True):
            data_[WP_REST_Search_Controller.PROP_ID] = php_int(post_.ID)
        # end if
        if php_in_array(WP_REST_Search_Controller.PROP_TITLE, fields_, True):
            if post_type_supports(post_.post_type, "title"):
                add_filter("protected_title_format", Array(self, "protected_title_format"))
                data_[WP_REST_Search_Controller.PROP_TITLE] = get_the_title(post_.ID)
                remove_filter("protected_title_format", Array(self, "protected_title_format"))
            else:
                data_[WP_REST_Search_Controller.PROP_TITLE] = ""
            # end if
        # end if
        if php_in_array(WP_REST_Search_Controller.PROP_URL, fields_, True):
            data_[WP_REST_Search_Controller.PROP_URL] = get_permalink(post_.ID)
        # end if
        if php_in_array(WP_REST_Search_Controller.PROP_TYPE, fields_, True):
            data_[WP_REST_Search_Controller.PROP_TYPE] = self.type
        # end if
        if php_in_array(WP_REST_Search_Controller.PROP_SUBTYPE, fields_, True):
            data_[WP_REST_Search_Controller.PROP_SUBTYPE] = post_.post_type
        # end if
        return data_
    # end def prepare_item
    #// 
    #// Prepares links for the search result of a given ID.
    #// 
    #// @since 5.0.0
    #// 
    #// @param int $id Item ID.
    #// @return array Links for the given item.
    #//
    def prepare_item_links(self, id_=None):
        
        
        post_ = get_post(id_)
        links_ = Array()
        item_route_ = self.detect_rest_item_route(post_)
        if (not php_empty(lambda : item_route_)):
            links_["self"] = Array({"href": rest_url(item_route_), "embeddable": True})
        # end if
        links_["about"] = Array({"href": rest_url("wp/v2/types/" + post_.post_type)})
        return links_
    # end def prepare_item_links
    #// 
    #// Overwrites the default protected title format.
    #// 
    #// By default, WordPress will show password protected posts with a title of
    #// "Protected: %s". As the REST API communicates the protected status of a post
    #// in a machine readable format, we remove the "Protected: " prefix.
    #// 
    #// @since 5.0.0
    #// 
    #// @return string Protected title format.
    #//
    def protected_title_format(self):
        
        
        return "%s"
    # end def protected_title_format
    #// 
    #// Attempts to detect the route to access a single item.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_Post $post Post object.
    #// @return string REST route relative to the REST base URI, or empty string if unknown.
    #//
    def detect_rest_item_route(self, post_=None):
        
        
        post_type_ = get_post_type_object(post_.post_type)
        if (not post_type_):
            return ""
        # end if
        #// It's currently impossible to detect the REST URL from a custom controller.
        if (not php_empty(lambda : post_type_.rest_controller_class)) and "WP_REST_Posts_Controller" != post_type_.rest_controller_class:
            return ""
        # end if
        namespace_ = "wp/v2"
        rest_base_ = post_type_.rest_base if (not php_empty(lambda : post_type_.rest_base)) else post_type_.name
        return php_sprintf("%s/%s/%d", namespace_, rest_base_, post_.ID)
    # end def detect_rest_item_route
# end class WP_REST_Post_Search_Handler
