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
#// User API: WP_Role class
#// 
#// @package WordPress
#// @subpackage Users
#// @since 4.4.0
#// 
#// 
#// Core class used to extend the user roles API.
#// 
#// @since 2.0.0
#//
class WP_Role():
    #// 
    #// Role name.
    #// 
    #// @since 2.0.0
    #// @var string
    #//
    name = Array()
    #// 
    #// List of capabilities the role contains.
    #// 
    #// @since 2.0.0
    #// @var array
    #//
    capabilities = Array()
    #// 
    #// Constructor - Set up object properties.
    #// 
    #// The list of capabilities, must have the key as the name of the capability
    #// and the value a boolean of whether it is granted to the role.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role         Role name.
    #// @param bool[] $capabilities List of capabilities keyed by the capability name,
    #// e.g. array( 'edit_posts' => true, 'delete_posts' => false ).
    #//
    def __init__(self, role_=None, capabilities_=None):
        
        
        self.name = role_
        self.capabilities = capabilities_
    # end def __init__
    #// 
    #// Assign role a capability.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $cap Capability name.
    #// @param bool $grant Whether role has capability privilege.
    #//
    def add_cap(self, cap_=None, grant_=None):
        if grant_ is None:
            grant_ = True
        # end if
        
        self.capabilities[cap_] = grant_
        wp_roles().add_cap(self.name, cap_, grant_)
    # end def add_cap
    #// 
    #// Removes a capability from a role.
    #// 
    #// This is a container for WP_Roles::remove_cap() to remove the
    #// capability from the role. That is to say, that WP_Roles::remove_cap()
    #// implements the functionality, but it also makes sense to use this class,
    #// because you don't need to enter the role name.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $cap Capability name.
    #//
    def remove_cap(self, cap_=None):
        
        
        self.capabilities[cap_] = None
        wp_roles().remove_cap(self.name, cap_)
    # end def remove_cap
    #// 
    #// Determines whether the role has the given capability.
    #// 
    #// The capabilities is passed through the {@see 'role_has_cap'} filter.
    #// The first parameter for the hook is the list of capabilities the class
    #// has assigned. The second parameter is the capability name to look for.
    #// The third and final parameter for the hook is the role name.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $cap Capability name.
    #// @return bool True if the role has the given capability. False otherwise.
    #//
    def has_cap(self, cap_=None):
        
        
        #// 
        #// Filters which capabilities a role has.
        #// 
        #// @since 2.0.0
        #// 
        #// @param bool[] $capabilities Associative array of capabilities for the role.
        #// @param string $cap          Capability name.
        #// @param string $name         Role name.
        #//
        capabilities_ = apply_filters("role_has_cap", self.capabilities, cap_, self.name)
        if (not php_empty(lambda : capabilities_[cap_])):
            return capabilities_[cap_]
        else:
            return False
        # end if
    # end def has_cap
# end class WP_Role
