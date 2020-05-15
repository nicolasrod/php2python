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
#// User API: WP_User class
#// 
#// @package WordPress
#// @subpackage Users
#// @since 4.4.0
#// 
#// 
#// Core class used to implement the WP_User object.
#// 
#// @since 2.0.0
#// 
#// @property string $nickname
#// @property string $description
#// @property string $user_description
#// @property string $first_name
#// @property string $user_firstname
#// @property string $last_name
#// @property string $user_lastname
#// @property string $user_login
#// @property string $user_pass
#// @property string $user_nicename
#// @property string $user_email
#// @property string $user_url
#// @property string $user_registered
#// @property string $user_activation_key
#// @property string $user_status
#// @property int    $user_level
#// @property string $display_name
#// @property string $spam
#// @property string $deleted
#// @property string $locale
#// @property string $rich_editing
#// @property string $syntax_highlighting
#//
class WP_User():
    data = Array()
    ID = 0
    caps = Array()
    cap_key = Array()
    roles = Array()
    allcaps = Array()
    filter = None
    site_id = 0
    back_compat_keys = Array()
    #// 
    #// Constructor.
    #// 
    #// Retrieves the userdata and passes it to WP_User::init().
    #// 
    #// @since 2.0.0
    #// 
    #// @param int|string|stdClass|WP_User $id User's ID, a WP_User object, or a user object from the DB.
    #// @param string $name Optional. User's username
    #// @param int $site_id Optional Site ID, defaults to current site.
    #//
    def __init__(self, id=0, name="", site_id=""):
        
        if (not (php_isset(lambda : self.back_compat_keys))):
            prefix = PHP_GLOBALS["wpdb"].prefix
            self.back_compat_keys = Array({"user_firstname": "first_name", "user_lastname": "last_name", "user_description": "description", "user_level": prefix + "user_level", prefix + "usersettings": prefix + "user-settings", prefix + "usersettingstime": prefix + "user-settings-time"})
        # end if
        if type(id).__name__ == "WP_User":
            self.init(id.data, site_id)
            return
        elif php_is_object(id):
            self.init(id, site_id)
            return
        # end if
        if (not php_empty(lambda : id)) and (not php_is_numeric(id)):
            name = id
            id = 0
        # end if
        if id:
            data = self.get_data_by("id", id)
        else:
            data = self.get_data_by("login", name)
        # end if
        if data:
            self.init(data, site_id)
        else:
            self.data = php_new_class("stdClass", lambda : stdClass())
        # end if
    # end def __init__
    #// 
    #// Sets up object properties, including capabilities.
    #// 
    #// @since 3.3.0
    #// 
    #// @param object $data    User DB row object.
    #// @param int    $site_id Optional. The site ID to initialize for.
    #//
    def init(self, data=None, site_id=""):
        
        self.data = data
        self.ID = int(data.ID)
        self.for_site(site_id)
    # end def init
    #// 
    #// Return only the main user fields
    #// 
    #// @since 3.3.0
    #// @since 4.4.0 Added 'ID' as an alias of 'id' for the `$field` parameter.
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $field The field to query against: 'id', 'ID', 'slug', 'email' or 'login'.
    #// @param string|int $value The field value
    #// @return object|false Raw user object
    #//
    @classmethod
    def get_data_by(self, field=None, value=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// 'ID' is an alias of 'id'.
        if "ID" == field:
            field = "id"
        # end if
        if "id" == field:
            #// Make sure the value is numeric to avoid casting objects, for example,
            #// to int 1.
            if (not php_is_numeric(value)):
                return False
            # end if
            value = php_intval(value)
            if value < 1:
                return False
            # end if
        else:
            value = php_trim(value)
        # end if
        if (not value):
            return False
        # end if
        for case in Switch(field):
            if case("id"):
                user_id = value
                db_field = "ID"
                break
            # end if
            if case("slug"):
                user_id = wp_cache_get(value, "userslugs")
                db_field = "user_nicename"
                break
            # end if
            if case("email"):
                user_id = wp_cache_get(value, "useremail")
                db_field = "user_email"
                break
            # end if
            if case("login"):
                value = sanitize_user(value)
                user_id = wp_cache_get(value, "userlogins")
                db_field = "user_login"
                break
            # end if
            if case():
                return False
            # end if
        # end for
        if False != user_id:
            user = wp_cache_get(user_id, "users")
            if user:
                return user
            # end if
        # end if
        user = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.users) + str(" WHERE ") + str(db_field) + str(" = %s LIMIT 1"), value))
        if (not user):
            return False
        # end if
        update_user_caches(user)
        return user
    # end def get_data_by
    #// 
    #// Magic method for checking the existence of a certain custom field.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $key User meta key to check if set.
    #// @return bool Whether the given user meta key is set.
    #//
    def __isset(self, key=None):
        
        if "id" == key:
            _deprecated_argument("WP_User->id", "2.1.0", php_sprintf(__("Use %s instead."), "<code>WP_User->ID</code>"))
            key = "ID"
        # end if
        if (php_isset(lambda : self.data.key)):
            return True
        # end if
        if (php_isset(lambda : self.back_compat_keys[key])):
            key = self.back_compat_keys[key]
        # end if
        return metadata_exists("user", self.ID, key)
    # end def __isset
    #// 
    #// Magic method for accessing custom fields.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $key User meta key to retrieve.
    #// @return mixed Value of the given user meta key (if set). If `$key` is 'id', the user ID.
    #//
    def __get(self, key=None):
        
        if "id" == key:
            _deprecated_argument("WP_User->id", "2.1.0", php_sprintf(__("Use %s instead."), "<code>WP_User->ID</code>"))
            return self.ID
        # end if
        if (php_isset(lambda : self.data.key)):
            value = self.data.key
        else:
            if (php_isset(lambda : self.back_compat_keys[key])):
                key = self.back_compat_keys[key]
            # end if
            value = get_user_meta(self.ID, key, True)
        # end if
        if self.filter:
            value = sanitize_user_field(key, value, self.ID, self.filter)
        # end if
        return value
    # end def __get
    #// 
    #// Magic method for setting custom user fields.
    #// 
    #// This method does not update custom fields in the database. It only stores
    #// the value on the WP_User instance.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $key   User meta key.
    #// @param mixed  $value User meta value.
    #//
    def __set(self, key=None, value=None):
        
        if "id" == key:
            _deprecated_argument("WP_User->id", "2.1.0", php_sprintf(__("Use %s instead."), "<code>WP_User->ID</code>"))
            self.ID = value
            return
        # end if
        self.data.key = value
    # end def __set
    #// 
    #// Magic method for unsetting a certain custom field.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key User meta key to unset.
    #//
    def __unset(self, key=None):
        
        if "id" == key:
            _deprecated_argument("WP_User->id", "2.1.0", php_sprintf(__("Use %s instead."), "<code>WP_User->ID</code>"))
        # end if
        if (php_isset(lambda : self.data.key)):
            self.data.key = None
        # end if
        if (php_isset(lambda : self.back_compat_keys[key])):
            self.back_compat_keys[key] = None
        # end if
    # end def __unset
    #// 
    #// Determine whether the user exists in the database.
    #// 
    #// @since 3.4.0
    #// 
    #// @return bool True if user exists in the database, false if not.
    #//
    def exists(self):
        
        return (not php_empty(lambda : self.ID))
    # end def exists
    #// 
    #// Retrieve the value of a property or meta key.
    #// 
    #// Retrieves from the users and usermeta table.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $key Property
    #// @return mixed
    #//
    def get(self, key=None):
        
        return self.__get(key)
    # end def get
    #// 
    #// Determine whether a property or meta key is set
    #// 
    #// Consults the users and usermeta tables.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $key Property
    #// @return bool
    #//
    def has_prop(self, key=None):
        
        return self.__isset(key)
    # end def has_prop
    #// 
    #// Return an array representation.
    #// 
    #// @since 3.5.0
    #// 
    #// @return array Array representation.
    #//
    def to_array(self):
        
        return get_object_vars(self.data)
    # end def to_array
    #// 
    #// Makes private/protected methods readable for backward compatibility.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string   $name      Method to call.
    #// @param array    $arguments Arguments to pass when calling.
    #// @return mixed|false Return value of the callback, false otherwise.
    #//
    def __call(self, name=None, arguments=None):
        
        if "_init_caps" == name:
            return self._init_caps(arguments)
        # end if
        return False
    # end def __call
    #// 
    #// Set up capability object properties.
    #// 
    #// Will set the value for the 'cap_key' property to current database table
    #// prefix, followed by 'capabilities'. Will then check to see if the
    #// property matching the 'cap_key' exists and is an array. If so, it will be
    #// used.
    #// 
    #// @since 2.1.0
    #// @deprecated 4.9.0 Use WP_User::for_site()
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $cap_key Optional capability key
    #//
    def _init_caps(self, cap_key=""):
        
        global wpdb
        php_check_if_defined("wpdb")
        _deprecated_function(__METHOD__, "4.9.0", "WP_User::for_site()")
        if php_empty(lambda : cap_key):
            self.cap_key = wpdb.get_blog_prefix(self.site_id) + "capabilities"
        else:
            self.cap_key = cap_key
        # end if
        self.caps = self.get_caps_data()
        self.get_role_caps()
    # end def _init_caps
    #// 
    #// Retrieves all of the capabilities of the roles of the user, and merges them with individual user capabilities.
    #// 
    #// All of the capabilities of the roles of the user are merged with the user's individual capabilities. This means
    #// that the user can be denied specific capabilities that their role might have, but the user is specifically denied.
    #// 
    #// @since 2.0.0
    #// 
    #// @return bool[] Array of key/value pairs where keys represent a capability name and boolean values
    #// represent whether the user has that capability.
    #//
    def get_role_caps(self):
        
        switch_site = False
        if is_multisite() and get_current_blog_id() != self.site_id:
            switch_site = True
            switch_to_blog(self.site_id)
        # end if
        wp_roles = wp_roles()
        #// Filter out caps that are not role names and assign to $this->roles.
        if php_is_array(self.caps):
            self.roles = php_array_filter(php_array_keys(self.caps), Array(wp_roles, "is_role"))
        # end if
        #// Build $allcaps from role caps, overlay user's $caps.
        self.allcaps = Array()
        for role in self.roles:
            the_role = wp_roles.get_role(role)
            self.allcaps = php_array_merge(self.allcaps, the_role.capabilities)
        # end for
        self.allcaps = php_array_merge(self.allcaps, self.caps)
        if switch_site:
            restore_current_blog()
        # end if
        return self.allcaps
    # end def get_role_caps
    #// 
    #// Add role to user.
    #// 
    #// Updates the user's meta data option with capabilities and roles.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name.
    #//
    def add_role(self, role=None):
        
        if php_empty(lambda : role):
            return
        # end if
        self.caps[role] = True
        update_user_meta(self.ID, self.cap_key, self.caps)
        self.get_role_caps()
        self.update_user_level_from_caps()
        #// 
        #// Fires immediately after the user has been given a new role.
        #// 
        #// @since 4.3.0
        #// 
        #// @param int    $user_id The user ID.
        #// @param string $role    The new role.
        #//
        do_action("add_user_role", self.ID, role)
    # end def add_role
    #// 
    #// Remove role from user.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name.
    #//
    def remove_role(self, role=None):
        
        if (not php_in_array(role, self.roles)):
            return
        # end if
        self.caps[role] = None
        update_user_meta(self.ID, self.cap_key, self.caps)
        self.get_role_caps()
        self.update_user_level_from_caps()
        #// 
        #// Fires immediately after a role as been removed from a user.
        #// 
        #// @since 4.3.0
        #// 
        #// @param int    $user_id The user ID.
        #// @param string $role    The removed role.
        #//
        do_action("remove_user_role", self.ID, role)
    # end def remove_role
    #// 
    #// Set the role of the user.
    #// 
    #// This will remove the previous roles of the user and assign the user the
    #// new one. You can set the role to an empty string and it will remove all
    #// of the roles from the user.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $role Role name.
    #//
    def set_role(self, role=None):
        
        if 1 == php_count(self.roles) and current(self.roles) == role:
            return
        # end if
        for oldrole in self.roles:
            self.caps[oldrole] = None
        # end for
        old_roles = self.roles
        if (not php_empty(lambda : role)):
            self.caps[role] = True
            self.roles = Array({role: True})
        else:
            self.roles = False
        # end if
        update_user_meta(self.ID, self.cap_key, self.caps)
        self.get_role_caps()
        self.update_user_level_from_caps()
        #// 
        #// Fires after the user's role has changed.
        #// 
        #// @since 2.9.0
        #// @since 3.6.0 Added $old_roles to include an array of the user's previous roles.
        #// 
        #// @param int      $user_id   The user ID.
        #// @param string   $role      The new role.
        #// @param string[] $old_roles An array of the user's previous roles.
        #//
        do_action("set_user_role", self.ID, role, old_roles)
    # end def set_role
    #// 
    #// Choose the maximum level the user has.
    #// 
    #// Will compare the level from the $item parameter against the $max
    #// parameter. If the item is incorrect, then just the $max parameter value
    #// will be returned.
    #// 
    #// Used to get the max level based on the capabilities the user has. This
    #// is also based on roles, so if the user is assigned the Administrator role
    #// then the capability 'level_10' will exist and the user will get that
    #// value.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int $max Max level of user.
    #// @param string $item Level capability name.
    #// @return int Max Level.
    #//
    def level_reduction(self, max=None, item=None):
        
        if php_preg_match("/^level_(10|[0-9])$/i", item, matches):
            level = php_intval(matches[1])
            return php_max(max, level)
        else:
            return max
        # end if
    # end def level_reduction
    #// 
    #// Update the maximum user level for the user.
    #// 
    #// Updates the 'user_level' user metadata (includes prefix that is the
    #// database table prefix) with the maximum user level. Gets the value from
    #// the all of the capabilities that the user has.
    #// 
    #// @since 2.0.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #//
    def update_user_level_from_caps(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        self.user_level = array_reduce(php_array_keys(self.allcaps), Array(self, "level_reduction"), 0)
        update_user_meta(self.ID, wpdb.get_blog_prefix() + "user_level", self.user_level)
    # end def update_user_level_from_caps
    #// 
    #// Add capability and grant or deny access to capability.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $cap Capability name.
    #// @param bool $grant Whether to grant capability to user.
    #//
    def add_cap(self, cap=None, grant=True):
        
        self.caps[cap] = grant
        update_user_meta(self.ID, self.cap_key, self.caps)
        self.get_role_caps()
        self.update_user_level_from_caps()
    # end def add_cap
    #// 
    #// Remove capability from user.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $cap Capability name.
    #//
    def remove_cap(self, cap=None):
        
        if (not (php_isset(lambda : self.caps[cap]))):
            return
        # end if
        self.caps[cap] = None
        update_user_meta(self.ID, self.cap_key, self.caps)
        self.get_role_caps()
        self.update_user_level_from_caps()
    # end def remove_cap
    #// 
    #// Remove all of the capabilities of the user.
    #// 
    #// @since 2.1.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #//
    def remove_all_caps(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        self.caps = Array()
        delete_user_meta(self.ID, self.cap_key)
        delete_user_meta(self.ID, wpdb.get_blog_prefix() + "user_level")
        self.get_role_caps()
    # end def remove_all_caps
    #// 
    #// Returns whether the user has the specified capability.
    #// 
    #// This function also accepts an ID of an object to check against if the capability is a meta capability. Meta
    #// capabilities such as `edit_post` and `edit_user` are capabilities used by the `map_meta_cap()` function to
    #// map to primitive capabilities that a user or role has, such as `edit_posts` and `edit_others_posts`.
    #// 
    #// Example usage:
    #// 
    #// $user->has_cap( 'edit_posts' );
    #// $user->has_cap( 'edit_post', $post->ID );
    #// $user->has_cap( 'edit_post_meta', $post->ID, $meta_key );
    #// 
    #// While checking against a role in place of a capability is supported in part, this practice is discouraged as it
    #// may produce unreliable results.
    #// 
    #// @since 2.0.0
    #// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
    #// by adding it to the function signature.
    #// 
    #// @see map_meta_cap()
    #// 
    #// @param string $cap     Capability name.
    #// @param mixed  ...$args Optional further parameters, typically starting with an object ID.
    #// @return bool Whether the user has the given capability, or, if an object ID is passed, whether the user has
    #// the given capability for that object.
    #//
    def has_cap(self, cap=None, *args):
        
        if php_is_numeric(cap):
            _deprecated_argument(__FUNCTION__, "2.0.0", __("Usage of user levels is deprecated. Use capabilities instead."))
            cap = self.translate_level_to_cap(cap)
        # end if
        caps = map_meta_cap(cap, self.ID, args)
        #// Multisite super admin has all caps by definition, Unless specifically denied.
        if is_multisite() and is_super_admin(self.ID):
            if php_in_array("do_not_allow", caps):
                return False
            # end if
            return True
        # end if
        #// Maintain BC for the argument passed to the "user_has_cap" filter.
        args = php_array_merge(Array(cap, self.ID), args)
        #// 
        #// Dynamically filter a user's capabilities.
        #// 
        #// @since 2.0.0
        #// @since 3.7.0 Added the `$user` parameter.
        #// 
        #// @param bool[]   $allcaps Array of key/value pairs where keys represent a capability name and boolean values
        #// represent whether the user has that capability.
        #// @param string[] $caps    Required primitive capabilities for the requested capability.
        #// @param array    $args {
        #// Arguments that accompany the requested capability check.
        #// 
        #// @type string    $0 Requested capability.
        #// @type int       $1 Concerned user ID.
        #// @type mixed  ...$2 Optional second and further parameters, typically object ID.
        #// }
        #// @param WP_User  $user    The user object.
        #//
        capabilities = apply_filters("user_has_cap", self.allcaps, caps, args, self)
        #// Everyone is allowed to exist.
        capabilities["exist"] = True
        capabilities["do_not_allow"] = None
        #// Must have ALL requested caps.
        for cap in caps:
            if php_empty(lambda : capabilities[cap]):
                return False
            # end if
        # end for
        return True
    # end def has_cap
    #// 
    #// Convert numeric level to level capability name.
    #// 
    #// Prepends 'level_' to level number.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int $level Level number, 1 to 10.
    #// @return string
    #//
    def translate_level_to_cap(self, level=None):
        
        return "level_" + level
    # end def translate_level_to_cap
    #// 
    #// Set the site to operate on. Defaults to the current site.
    #// 
    #// @since 3.0.0
    #// @deprecated 4.9.0 Use WP_User::for_site()
    #// 
    #// @param int $blog_id Optional. Site ID, defaults to current site.
    #//
    def for_blog(self, blog_id=""):
        
        _deprecated_function(__METHOD__, "4.9.0", "WP_User::for_site()")
        self.for_site(blog_id)
    # end def for_blog
    #// 
    #// Sets the site to operate on. Defaults to the current site.
    #// 
    #// @since 4.9.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $site_id Site ID to initialize user capabilities for. Default is the current site.
    #//
    def for_site(self, site_id=""):
        
        global wpdb
        php_check_if_defined("wpdb")
        if (not php_empty(lambda : site_id)):
            self.site_id = absint(site_id)
        else:
            self.site_id = get_current_blog_id()
        # end if
        self.cap_key = wpdb.get_blog_prefix(self.site_id) + "capabilities"
        self.caps = self.get_caps_data()
        self.get_role_caps()
    # end def for_site
    #// 
    #// Gets the ID of the site for which the user's capabilities are currently initialized.
    #// 
    #// @since 4.9.0
    #// 
    #// @return int Site ID.
    #//
    def get_site_id(self):
        
        return self.site_id
    # end def get_site_id
    #// 
    #// Gets the available user capabilities data.
    #// 
    #// @since 4.9.0
    #// 
    #// @return bool[] List of capabilities keyed by the capability name,
    #// e.g. array( 'edit_posts' => true, 'delete_posts' => false ).
    #//
    def get_caps_data(self):
        
        caps = get_user_meta(self.ID, self.cap_key, True)
        if (not php_is_array(caps)):
            return Array()
        # end if
        return caps
    # end def get_caps_data
# end class WP_User
