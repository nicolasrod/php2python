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
#// Site API: WP_Site class
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 4.5.0
#// 
#// 
#// Core class used for interacting with a multisite site.
#// 
#// This class is used during load to populate the `$current_blog` global and
#// setup the current site.
#// 
#// @since 4.5.0
#// 
#// @property int    $id
#// @property int    $network_id
#// @property string $blogname
#// @property string $siteurl
#// @property int    $post_count
#// @property string $home
#//
class WP_Site():
    blog_id = Array()
    domain = ""
    path = ""
    site_id = "0"
    registered = "0000-00-00 00:00:00"
    last_updated = "0000-00-00 00:00:00"
    public = "1"
    archived = "0"
    mature = "0"
    spam = "0"
    deleted = "0"
    lang_id = "0"
    #// 
    #// Retrieves a site from the database by its ID.
    #// 
    #// @since 4.5.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $site_id The ID of the site to retrieve.
    #// @return WP_Site|false The site's object if found. False if not.
    #//
    @classmethod
    def get_instance(self, site_id=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        site_id = php_int(site_id)
        if (not site_id):
            return False
        # end if
        _site = wp_cache_get(site_id, "sites")
        if False == _site:
            _site = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.blogs) + str(" WHERE blog_id = %d LIMIT 1"), site_id))
            if php_empty(lambda : _site) or is_wp_error(_site):
                _site = -1
            # end if
            wp_cache_add(site_id, _site, "sites")
        # end if
        if php_is_numeric(_site):
            return False
        # end if
        return php_new_class("WP_Site", lambda : WP_Site(_site))
    # end def get_instance
    #// 
    #// Creates a new WP_Site object.
    #// 
    #// Will populate object properties from the object provided and assign other
    #// default properties based on that information.
    #// 
    #// @since 4.5.0
    #// 
    #// @param WP_Site|object $site A site object.
    #//
    def __init__(self, site=None):
        
        for key,value in get_object_vars(site):
            self.key = value
        # end for
    # end def __init__
    #// 
    #// Converts an object to array.
    #// 
    #// @since 4.6.0
    #// 
    #// @return array Object as array.
    #//
    def to_array(self):
        
        return get_object_vars(self)
    # end def to_array
    #// 
    #// Getter.
    #// 
    #// Allows current multisite naming conventions when getting properties.
    #// Allows access to extended site properties.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $key Property to get.
    #// @return mixed Value of the property. Null if not available.
    #//
    def __get(self, key=None):
        
        for case in Switch(key):
            if case("id"):
                return php_int(self.blog_id)
            # end if
            if case("network_id"):
                return php_int(self.site_id)
            # end if
            if case("blogname"):
                pass
            # end if
            if case("siteurl"):
                pass
            # end if
            if case("post_count"):
                pass
            # end if
            if case("home"):
                pass
            # end if
            if case():
                #// Custom properties added by 'site_details' filter.
                if (not did_action("ms_loaded")):
                    return None
                # end if
                details = self.get_details()
                if (php_isset(lambda : details.key)):
                    return details.key
                # end if
            # end if
        # end for
        return None
    # end def __get
    #// 
    #// Isset-er.
    #// 
    #// Allows current multisite naming conventions when checking for properties.
    #// Checks for extended site properties.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $key Property to check if set.
    #// @return bool Whether the property is set.
    #//
    def __isset(self, key=None):
        
        for case in Switch(key):
            if case("id"):
                pass
            # end if
            if case("network_id"):
                return True
            # end if
            if case("blogname"):
                pass
            # end if
            if case("siteurl"):
                pass
            # end if
            if case("post_count"):
                pass
            # end if
            if case("home"):
                if (not did_action("ms_loaded")):
                    return False
                # end if
                return True
            # end if
            if case():
                #// Custom properties added by 'site_details' filter.
                if (not did_action("ms_loaded")):
                    return False
                # end if
                details = self.get_details()
                if (php_isset(lambda : details.key)):
                    return True
                # end if
            # end if
        # end for
        return False
    # end def __isset
    #// 
    #// Setter.
    #// 
    #// Allows current multisite naming conventions while setting properties.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $key   Property to set.
    #// @param mixed  $value Value to assign to the property.
    #//
    def __set(self, key=None, value=None):
        
        for case in Switch(key):
            if case("id"):
                self.blog_id = php_str(value)
                break
            # end if
            if case("network_id"):
                self.site_id = php_str(value)
                break
            # end if
            if case():
                self.key = value
            # end if
        # end for
    # end def __set
    #// 
    #// Retrieves the details for this site.
    #// 
    #// This method is used internally to lazy-load the extended properties of a site.
    #// 
    #// @since 4.6.0
    #// 
    #// @see WP_Site::__get()
    #// 
    #// @return stdClass A raw site object with all details included.
    #//
    def get_details(self):
        
        details = wp_cache_get(self.blog_id, "site-details")
        if False == details:
            switch_to_blog(self.blog_id)
            #// Create a raw copy of the object for backward compatibility with the filter below.
            details = php_new_class("stdClass", lambda : stdClass())
            for key,value in get_object_vars(self):
                details.key = value
            # end for
            details.blogname = get_option("blogname")
            details.siteurl = get_option("siteurl")
            details.post_count = get_option("post_count")
            details.home = get_option("home")
            restore_current_blog()
            wp_cache_set(self.blog_id, details, "site-details")
        # end if
        #// This filter is documented in wp-includes/ms-blogs.php
        details = apply_filters_deprecated("blog_details", Array(details), "4.7.0", "site_details")
        #// 
        #// Filters a site's extended properties.
        #// 
        #// @since 4.6.0
        #// 
        #// @param stdClass $details The site details.
        #//
        details = apply_filters("site_details", details)
        return details
    # end def get_details
# end class WP_Site
