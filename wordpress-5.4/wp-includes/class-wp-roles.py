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
#// User API: WP_Roles class
#// 
#// @package WordPress
#// @subpackage Users
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a user roles API.
#// 
#// The role option is simple, the structure is organized by role name that store
#// the name in value of the 'name' key. The capabilities are stored as an array
#// in the value of the 'capability' key.
#// 
#// array (
#// 'rolename' => array (
#// 'name' => 'rolename',
#// 'capabilities' => array()
#// )
#// )
#// 
#// @since 2.0.0
#//
class WP_Roles():
    #// 
    #// List of roles and capabilities.
    #// 
    #// @since 2.0.0
    #// @var array[]
    #//
    roles = Array()
    #// 
    #// List of the role objects.
    #// 
    #// @since 2.0.0
    #// @var WP_Role[]
    #//
    role_objects = Array()
    #// 
    #// List of role names.
    #// 
    #// @since 2.0.0
    #// @var string[]
    #//
    role_names = Array()
    #// 
    #// Option name for storing role list.
    #// 
    #// @since 2.0.0
    #// @var string
    #//
    role_key = Array()
    #// 
    #// Whether to use the database for retrieval and storage.
    #// 
    #// @since 2.1.0
    #// @var bool
    #//
    use_db = True
    #// 
    #// The site ID the roles are initialized for.
    #// 
    #// @since 4.9.0
    #// @var int
    #//
    site_id = 0
    #// 
    #// Constructor
    #// 
    #// @since 2.0.0
    #// @since 4.9.0 The `$site_id` argument was added.
    #// 
    #// @global array $wp_user_roles Used to set the 'roles' property value.
    #// 
    #// @param int $site_id Site ID to initialize roles for. Default is the current site.
    #//
    def __init__(self, site_id_=None):
        
        
        global wp_user_roles_
        php_check_if_defined("wp_user_roles_")
        self.use_db = php_empty(lambda : wp_user_roles_)
        self.for_site(site_id_)
    # end def __init__
    #// 
    #// Make private/protected methods readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string   $name      Method to call.
    #// @param array    $arguments Arguments to pass when calling.
    #// @return mixed|false Return value of the callback, false otherwise.
    #//
    def __call(self, name_=None, arguments_=None):
        
        
        if "_init" == name_:
            return self._init(arguments_)
        # end if
        return False
    # end def __call
    #// 
    #// Set up the object properties.
    #// 
    #// The role key is set to the current prefix for the $wpdb object with
    #// 'user_roles' appended. If the $wp_user_roles global is set, then it will
    #// be used and the role option will not be updated or used.
    #// 
    #// @since 2.1.0
    #// @deprecated 4.9.0 Use WP_Roles::for_site()
    #//
    def _init(self):
        
        
        _deprecated_function(__METHOD__, "4.9.0", "WP_Roles::for_site()")
        self.for_site()
    # end def _init
    #// 
    #// Reinitialize the object
    #// 
    #// Recreates the role objects. This is typically called only by switch_to_blog()
    #// after switching wpdb to a new site ID.
    #// 
    #// @since 3.5.0
    #// @deprecated 4.7.0 Use WP_Roles::for_site()
    #//
    def reinit(self):
        
        
        _deprecated_function(__METHOD__, "4.7.0", "WP_Roles::for_site()")
        self.for_site()
    # end def reinit
    #// 
    #// Add role name with capabilities to list.
    #// 
    #// Updates the list of roles, if the role doesn't already exist.
    #// 
    #// The capabilities are defined in the following format `array( 'read' => true );`
    #// To explicitly deny a role a capability you set the value for that capability to false.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role         Role name.
    #// @param string $display_name Role display name.
    #// @param bool[] $capabilities List of capabilities keyed by the capability name,
    #// e.g. array( 'edit_posts' => true, 'delete_posts' => false ).
    #// @return WP_Role|void WP_Role object, if role is added.
    #//
    def add_role(self, role_=None, display_name_=None, capabilities_=None):
        if capabilities_ is None:
            capabilities_ = Array()
        # end if
        
        if php_empty(lambda : role_) or (php_isset(lambda : self.roles[role_])):
            return
        # end if
        self.roles[role_] = Array({"name": display_name_, "capabilities": capabilities_})
        if self.use_db:
            update_option(self.role_key, self.roles)
        # end if
        self.role_objects[role_] = php_new_class("WP_Role", lambda : WP_Role(role_, capabilities_))
        self.role_names[role_] = display_name_
        return self.role_objects[role_]
    # end def add_role
    #// 
    #// Remove role by name.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name.
    #//
    def remove_role(self, role_=None):
        
        
        if (not (php_isset(lambda : self.role_objects[role_]))):
            return
        # end if
        self.role_objects[role_] = None
        self.role_names[role_] = None
        self.roles[role_] = None
        if self.use_db:
            update_option(self.role_key, self.roles)
        # end if
        if get_option("default_role") == role_:
            update_option("default_role", "subscriber")
        # end if
    # end def remove_role
    #// 
    #// Add capability to role.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name.
    #// @param string $cap Capability name.
    #// @param bool $grant Optional, default is true. Whether role is capable of performing capability.
    #//
    def add_cap(self, role_=None, cap_=None, grant_=None):
        if grant_ is None:
            grant_ = True
        # end if
        
        if (not (php_isset(lambda : self.roles[role_]))):
            return
        # end if
        self.roles[role_]["capabilities"][cap_] = grant_
        if self.use_db:
            update_option(self.role_key, self.roles)
        # end if
    # end def add_cap
    #// 
    #// Remove capability from role.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name.
    #// @param string $cap Capability name.
    #//
    def remove_cap(self, role_=None, cap_=None):
        
        
        if (not (php_isset(lambda : self.roles[role_]))):
            return
        # end if
        self.roles[role_]["capabilities"][cap_] = None
        if self.use_db:
            update_option(self.role_key, self.roles)
        # end if
    # end def remove_cap
    #// 
    #// Retrieve role object by name.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name.
    #// @return WP_Role|null WP_Role object if found, null if the role does not exist.
    #//
    def get_role(self, role_=None):
        
        
        if (php_isset(lambda : self.role_objects[role_])):
            return self.role_objects[role_]
        else:
            return None
        # end if
    # end def get_role
    #// 
    #// Retrieve list of role names.
    #// 
    #// @since 2.0.0
    #// 
    #// @return string[] List of role names.
    #//
    def get_names(self):
        
        
        return self.role_names
    # end def get_names
    #// 
    #// Whether role name is currently in the list of available roles.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name to look up.
    #// @return bool
    #//
    def is_role(self, role_=None):
        
        
        return (php_isset(lambda : self.role_names[role_]))
    # end def is_role
    #// 
    #// Initializes all of the available roles.
    #// 
    #// @since 4.9.0
    #//
    def init_roles(self):
        
        
        if php_empty(lambda : self.roles):
            return
        # end if
        self.role_objects = Array()
        self.role_names = Array()
        for role_ in php_array_keys(self.roles):
            self.role_objects[role_] = php_new_class("WP_Role", lambda : WP_Role(role_, self.roles[role_]["capabilities"]))
            self.role_names[role_] = self.roles[role_]["name"]
        # end for
        #// 
        #// After the roles have been initialized, allow plugins to add their own roles.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Roles $this A reference to the WP_Roles object.
        #//
        do_action("wp_roles_init", self)
    # end def init_roles
    #// 
    #// Sets the site to operate on. Defaults to the current site.
    #// 
    #// @since 4.9.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $site_id Site ID to initialize roles for. Default is the current site.
    #//
    def for_site(self, site_id_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if (not php_empty(lambda : site_id_)):
            self.site_id = absint(site_id_)
        else:
            self.site_id = get_current_blog_id()
        # end if
        self.role_key = wpdb_.get_blog_prefix(self.site_id) + "user_roles"
        if (not php_empty(lambda : self.roles)) and (not self.use_db):
            return
        # end if
        self.roles = self.get_roles_data()
        self.init_roles()
    # end def for_site
    #// 
    #// Gets the ID of the site for which roles are currently initialized.
    #// 
    #// @since 4.9.0
    #// 
    #// @return int Site ID.
    #//
    def get_site_id(self):
        
        
        return self.site_id
    # end def get_site_id
    #// 
    #// Gets the available roles data.
    #// 
    #// @since 4.9.0
    #// 
    #// @global array $wp_user_roles Used to set the 'roles' property value.
    #// 
    #// @return array Roles array.
    #//
    def get_roles_data(self):
        
        
        global wp_user_roles_
        php_check_if_defined("wp_user_roles_")
        if (not php_empty(lambda : wp_user_roles_)):
            return wp_user_roles_
        # end if
        if is_multisite() and get_current_blog_id() != self.site_id:
            remove_action("switch_blog", "wp_switch_roles_and_user", 1)
            roles_ = get_blog_option(self.site_id, self.role_key, Array())
            add_action("switch_blog", "wp_switch_roles_and_user", 1, 2)
            return roles_
        # end if
        return get_option(self.role_key, Array())
    # end def get_roles_data
# end class WP_Roles
