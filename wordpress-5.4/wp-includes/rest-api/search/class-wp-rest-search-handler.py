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
#// REST API: WP_REST_Search_Handler class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 5.0.0
#// 
#// 
#// Core base class representing a search handler for an object type in the REST API.
#// 
#// @since 5.0.0
#//
class WP_REST_Search_Handler():
    RESULT_IDS = "ids"
    RESULT_TOTAL = "total"
    type = ""
    subtypes = Array()
    #// 
    #// Gets the object type managed by this search handler.
    #// 
    #// @since 5.0.0
    #// 
    #// @return string Object type identifier.
    #//
    def get_type(self):
        
        return self.type
    # end def get_type
    #// 
    #// Gets the object subtypes managed by this search handler.
    #// 
    #// @since 5.0.0
    #// 
    #// @return array Array of object subtype identifiers.
    #//
    def get_subtypes(self):
        
        return self.subtypes
    # end def get_subtypes
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
    def search_items(self, request=None):
        
        pass
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
    def prepare_item(self, id=None, fields=None):
        
        pass
    # end def prepare_item
    #// 
    #// Prepares links for the search result of a given ID.
    #// 
    #// @since 5.0.0
    #// 
    #// @param int $id Item ID.
    #// @return array Links for the given item.
    #//
    def prepare_item_links(self, id=None):
        
        pass
    # end def prepare_item_links
# end class WP_REST_Search_Handler
