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
#// REST API: WP_REST_Comment_Meta_Fields class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class to manage comment meta via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Meta_Fields
#//
class WP_REST_Comment_Meta_Fields(WP_REST_Meta_Fields):
    #// 
    #// Retrieves the object type for comment meta.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string The meta type.
    #//
    def get_meta_type(self):
        
        
        return "comment"
    # end def get_meta_type
    #// 
    #// Retrieves the object meta subtype.
    #// 
    #// @since 4.9.8
    #// 
    #// @return string 'comment' There are no subtypes.
    #//
    def get_meta_subtype(self):
        
        
        return "comment"
    # end def get_meta_subtype
    #// 
    #// Retrieves the type for register_rest_field() in the context of comments.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string The REST field type.
    #//
    def get_rest_field_type(self):
        
        
        return "comment"
    # end def get_rest_field_type
# end class WP_REST_Comment_Meta_Fields
