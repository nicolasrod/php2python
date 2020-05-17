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
#// REST API: WP_REST_User_Meta_Fields class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core class used to manage meta values for users via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Meta_Fields
#//
class WP_REST_User_Meta_Fields(WP_REST_Meta_Fields):
    #// 
    #// Retrieves the object meta type.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string The user meta type.
    #//
    def get_meta_type(self):
        
        
        return "user"
    # end def get_meta_type
    #// 
    #// Retrieves the object meta subtype.
    #// 
    #// @since 4.9.8
    #// 
    #// @return string 'user' There are no subtypes.
    #//
    def get_meta_subtype(self):
        
        
        return "user"
    # end def get_meta_subtype
    #// 
    #// Retrieves the type for register_rest_field().
    #// 
    #// @since 4.7.0
    #// 
    #// @return string The user REST field type.
    #//
    def get_rest_field_type(self):
        
        
        return "user"
    # end def get_rest_field_type
# end class WP_REST_User_Meta_Fields
