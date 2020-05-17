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
    #// 
    #// Site ID.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    blog_id = Array()
    #// 
    #// Domain of the site.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    domain = ""
    #// 
    #// Path of the site.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    path = ""
    #// 
    #// The ID of the site's parent network.
    #// 
    #// Named "site" vs. "network" for legacy reasons. An individual site's "site" is
    #// its network.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    site_id = "0"
    #// 
    #// The date on which the site was created or registered.
    #// 
    #// @since 4.5.0
    #// @var string Date in MySQL's datetime format.
    #//
    registered = "0000-00-00 00:00:00"
    #// 
    #// The date and time on which site settings were last updated.
    #// 
    #// @since 4.5.0
    #// @var string Date in MySQL's datetime format.
    #//
    last_updated = "0000-00-00 00:00:00"
    #// 
    #// Whether the site should be treated as public.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    public = "1"
    #// 
    #// Whether the site should be treated as archived.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    archived = "0"
    #// 
    #// Whether the site should be treated as mature.
    #// 
    #// Handling for this does not exist throughout WordPress core, but custom
    #// implementations exist that require the property to be present.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    mature = "0"
    #// 
    #// Whether the site should be treated as spam.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    spam = "0"
    #// 
    #// Whether the site should be treated as deleted.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    deleted = "0"
    #// 
    #// The language pack associated with this site.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
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
    def get_instance(self, site_id_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        site_id_ = php_int(site_id_)
        if (not site_id_):
            return False
        # end if
        _site_ = wp_cache_get(site_id_, "sites")
        if False == _site_:
            _site_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.blogs) + str(" WHERE blog_id = %d LIMIT 1"), site_id_))
            if php_empty(lambda : _site_) or is_wp_error(_site_):
                _site_ = -1
            # end if
            wp_cache_add(site_id_, _site_, "sites")
        # end if
        if php_is_numeric(_site_):
            return False
        # end if
        return php_new_class("WP_Site", lambda : WP_Site(_site_))
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
    def __init__(self, site_=None):
        
        
        for key_,value_ in get_object_vars(site_):
            self.key_ = value_
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
    def __get(self, key_=None):
        
        
        for case in Switch(key_):
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
                details_ = self.get_details()
                if (php_isset(lambda : details_.key_)):
                    return details_.key_
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
    def __isset(self, key_=None):
        
        
        for case in Switch(key_):
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
                details_ = self.get_details()
                if (php_isset(lambda : details_.key_)):
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
    def __set(self, key_=None, value_=None):
        
        
        for case in Switch(key_):
            if case("id"):
                self.blog_id = php_str(value_)
                break
            # end if
            if case("network_id"):
                self.site_id = php_str(value_)
                break
            # end if
            if case():
                self.key_ = value_
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
        
        
        details_ = wp_cache_get(self.blog_id, "site-details")
        if False == details_:
            switch_to_blog(self.blog_id)
            #// Create a raw copy of the object for backward compatibility with the filter below.
            details_ = php_new_class("stdClass", lambda : stdClass())
            for key_,value_ in get_object_vars(self):
                details_.key_ = value_
            # end for
            details_.blogname = get_option("blogname")
            details_.siteurl = get_option("siteurl")
            details_.post_count = get_option("post_count")
            details_.home = get_option("home")
            restore_current_blog()
            wp_cache_set(self.blog_id, details_, "site-details")
        # end if
        #// This filter is documented in wp-includes/ms-blogs.php
        details_ = apply_filters_deprecated("blog_details", Array(details_), "4.7.0", "site_details")
        #// 
        #// Filters a site's extended properties.
        #// 
        #// @since 4.6.0
        #// 
        #// @param stdClass $details The site details.
        #//
        details_ = apply_filters("site_details", details_)
        return details_
    # end def get_details
# end class WP_Site
