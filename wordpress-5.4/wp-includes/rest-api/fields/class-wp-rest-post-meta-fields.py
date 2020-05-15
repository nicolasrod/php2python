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
#// REST API: WP_REST_Post_Meta_Fields class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to manage meta values for posts via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Meta_Fields
#//
class WP_REST_Post_Meta_Fields(WP_REST_Meta_Fields):
    post_type = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $post_type Post type to register fields for.
    #//
    def __init__(self, post_type=None):
        
        self.post_type = post_type
    # end def __init__
    #// 
    #// Retrieves the object meta type.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string The meta type.
    #//
    def get_meta_type(self):
        
        return "post"
    # end def get_meta_type
    #// 
    #// Retrieves the object meta subtype.
    #// 
    #// @since 4.9.8
    #// 
    #// @return string Subtype for the meta type, or empty string if no specific subtype.
    #//
    def get_meta_subtype(self):
        
        return self.post_type
    # end def get_meta_subtype
    #// 
    #// Retrieves the type for register_rest_field().
    #// 
    #// @since 4.7.0
    #// 
    #// @see register_rest_field()
    #// 
    #// @return string The REST field type.
    #//
    def get_rest_field_type(self):
        
        return self.post_type
    # end def get_rest_field_type
# end class WP_REST_Post_Meta_Fields
