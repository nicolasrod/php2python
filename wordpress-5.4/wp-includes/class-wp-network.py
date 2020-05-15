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
#// Network API: WP_Network class
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 4.4.0
#// 
#// 
#// Core class used for interacting with a multisite network.
#// 
#// This class is used during load to populate the `$current_site` global and
#// setup the current network.
#// 
#// This class is most useful in WordPress multi-network installations where the
#// ability to interact with any network of sites is required.
#// 
#// @since 4.4.0
#// 
#// @property int $id
#// @property int $site_id
#//
class WP_Network():
    id = Array()
    domain = ""
    path = ""
    blog_id = "0"
    cookie_domain = ""
    site_name = ""
    #// 
    #// Retrieve a network from the database by its ID.
    #// 
    #// @since 4.4.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $network_id The ID of the network to retrieve.
    #// @return WP_Network|bool The network's object if found. False if not.
    #//
    @classmethod
    def get_instance(self, network_id=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        network_id = int(network_id)
        if (not network_id):
            return False
        # end if
        _network = wp_cache_get(network_id, "networks")
        if False == _network:
            _network = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.site) + str(" WHERE id = %d LIMIT 1"), network_id))
            if php_empty(lambda : _network) or is_wp_error(_network):
                _network = -1
            # end if
            wp_cache_add(network_id, _network, "networks")
        # end if
        if php_is_numeric(_network):
            return False
        # end if
        return php_new_class("WP_Network", lambda : WP_Network(_network))
    # end def get_instance
    #// 
    #// Create a new WP_Network object.
    #// 
    #// Will populate object properties from the object provided and assign other
    #// default properties based on that information.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Network|object $network A network object.
    #//
    def __init__(self, network=None):
        
        for key,value in get_object_vars(network):
            self.key = value
        # end for
        self._set_site_name()
        self._set_cookie_domain()
    # end def __init__
    #// 
    #// Getter.
    #// 
    #// Allows current multisite naming conventions when getting properties.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $key Property to get.
    #// @return mixed Value of the property. Null if not available.
    #//
    def __get(self, key=None):
        
        for case in Switch(key):
            if case("id"):
                return int(self.id)
            # end if
            if case("blog_id"):
                return str(self.get_main_site_id())
            # end if
            if case("site_id"):
                return self.get_main_site_id()
            # end if
        # end for
        return None
    # end def __get
    #// 
    #// Isset-er.
    #// 
    #// Allows current multisite naming conventions when checking for properties.
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
            if case("blog_id"):
                pass
            # end if
            if case("site_id"):
                return True
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
                self.id = int(value)
                break
            # end if
            if case("blog_id"):
                pass
            # end if
            if case("site_id"):
                self.blog_id = str(value)
                break
            # end if
            if case():
                self.key = value
            # end if
        # end for
    # end def __set
    #// 
    #// Returns the main site ID for the network.
    #// 
    #// Internal method used by the magic getter for the 'blog_id' and 'site_id'
    #// properties.
    #// 
    #// @since 4.9.0
    #// 
    #// @return int The ID of the main site.
    #//
    def get_main_site_id(self):
        
        #// 
        #// Filters the main site ID.
        #// 
        #// Returning a positive integer will effectively short-circuit the function.
        #// 
        #// @since 4.9.0
        #// 
        #// @param int|null   $main_site_id If a positive integer is returned, it is interpreted as the main site ID.
        #// @param WP_Network $network      The network object for which the main site was detected.
        #//
        main_site_id = int(apply_filters("pre_get_main_site_id", None, self))
        if 0 < main_site_id:
            return main_site_id
        # end if
        if 0 < int(self.blog_id):
            return int(self.blog_id)
        # end if
        if php_defined("DOMAIN_CURRENT_SITE") and php_defined("PATH_CURRENT_SITE") and DOMAIN_CURRENT_SITE == self.domain and PATH_CURRENT_SITE == self.path or php_defined("SITE_ID_CURRENT_SITE") and SITE_ID_CURRENT_SITE == self.id:
            if php_defined("BLOG_ID_CURRENT_SITE"):
                self.blog_id = str(BLOG_ID_CURRENT_SITE)
                return int(self.blog_id)
            # end if
            if php_defined("BLOGID_CURRENT_SITE"):
                #// Deprecated.
                self.blog_id = str(BLOGID_CURRENT_SITE)
                return int(self.blog_id)
            # end if
        # end if
        site = get_site()
        if site.domain == self.domain and site.path == self.path:
            main_site_id = int(site.id)
        else:
            cache_key = "network:" + self.id + ":main_site"
            main_site_id = wp_cache_get(cache_key, "site-options")
            if False == main_site_id:
                _sites = get_sites(Array({"fields": "ids", "number": 1, "domain": self.domain, "path": self.path, "network_id": self.id}))
                main_site_id = php_array_shift(_sites) if (not php_empty(lambda : _sites)) else 0
                wp_cache_add(cache_key, main_site_id, "site-options")
            # end if
        # end if
        self.blog_id = str(main_site_id)
        return int(self.blog_id)
    # end def get_main_site_id
    #// 
    #// Set the site name assigned to the network if one has not been populated.
    #// 
    #// @since 4.4.0
    #//
    def _set_site_name(self):
        
        if (not php_empty(lambda : self.site_name)):
            return
        # end if
        default = ucfirst(self.domain)
        self.site_name = get_network_option(self.id, "site_name", default)
    # end def _set_site_name
    #// 
    #// Set the cookie domain based on the network domain if one has
    #// not been populated.
    #// 
    #// @todo What if the domain of the network doesn't match the current site?
    #// 
    #// @since 4.4.0
    #//
    def _set_cookie_domain(self):
        
        if (not php_empty(lambda : self.cookie_domain)):
            return
        # end if
        self.cookie_domain = self.domain
        if "www." == php_substr(self.cookie_domain, 0, 4):
            self.cookie_domain = php_substr(self.cookie_domain, 4)
        # end if
    # end def _set_cookie_domain
    #// 
    #// Retrieve the closest matching network for a domain and path.
    #// 
    #// This will not necessarily return an exact match for a domain and path. Instead, it
    #// breaks the domain and path into pieces that are then used to match the closest
    #// possibility from a query.
    #// 
    #// The intent of this method is to match a network during bootstrap for a
    #// requested site address.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string   $domain   Domain to check.
    #// @param string   $path     Path to check.
    #// @param int|null $segments Path segments to use. Defaults to null, or the full path.
    #// @return WP_Network|bool Network object if successful. False when no network is found.
    #//
    @classmethod
    def get_by_path(self, domain="", path="", segments=None):
        
        domains = Array(domain)
        pieces = php_explode(".", domain)
        #// 
        #// It's possible one domain to search is 'com', but it might as well
        #// be 'localhost' or some other locally mapped domain.
        #//
        while True:
            
            if not (php_array_shift(pieces)):
                break
            # end if
            if (not php_empty(lambda : pieces)):
                domains[-1] = php_implode(".", pieces)
            # end if
        # end while
        #// 
        #// If we've gotten to this function during normal execution, there is
        #// more than one network installed. At this point, who knows how many
        #// we have. Attempt to optimize for the situation where networks are
        #// only domains, thus meaning paths never need to be considered.
        #// 
        #// This is a very basic optimization; anything further could have
        #// drawbacks depending on the setup, so this is best done per-installation.
        #//
        using_paths = True
        if wp_using_ext_object_cache():
            using_paths = wp_cache_get("networks_have_paths", "site-options")
            if False == using_paths:
                using_paths = get_networks(Array({"number": 1, "count": True, "path__not_in": "/"}))
                wp_cache_add("networks_have_paths", using_paths, "site-options")
            # end if
        # end if
        paths = Array()
        if using_paths:
            path_segments = php_array_filter(php_explode("/", php_trim(path, "/")))
            #// 
            #// Filters the number of path segments to consider when searching for a site.
            #// 
            #// @since 3.9.0
            #// 
            #// @param int|null $segments The number of path segments to consider. WordPress by default looks at
            #// one path segment. The function default of null only makes sense when you
            #// know the requested path should match a network.
            #// @param string   $domain   The requested domain.
            #// @param string   $path     The requested path, in full.
            #//
            segments = apply_filters("network_by_path_segments_count", segments, domain, path)
            if None != segments and php_count(path_segments) > segments:
                path_segments = php_array_slice(path_segments, 0, segments)
            # end if
            while True:
                
                if not (php_count(path_segments)):
                    break
                # end if
                paths[-1] = "/" + php_implode("/", path_segments) + "/"
                php_array_pop(path_segments)
            # end while
            paths[-1] = "/"
        # end if
        #// 
        #// Determine a network by its domain and path.
        #// 
        #// This allows one to short-circuit the default logic, perhaps by
        #// replacing it with a routine that is more optimal for your setup.
        #// 
        #// Return null to avoid the short-circuit. Return false if no network
        #// can be found at the requested domain and path. Otherwise, return
        #// an object from wp_get_network().
        #// 
        #// @since 3.9.0
        #// 
        #// @param null|bool|WP_Network $network  Network value to return by path. Default null
        #// to continue retrieving the network.
        #// @param string               $domain   The requested domain.
        #// @param string               $path     The requested path, in full.
        #// @param int|null             $segments The suggested number of paths to consult.
        #// Default null, meaning the entire path was to be consulted.
        #// @param string[]             $paths    Array of paths to search for, based on `$path` and `$segments`.
        #//
        pre = apply_filters("pre_get_network_by_path", None, domain, path, segments, paths)
        if None != pre:
            return pre
        # end if
        if (not using_paths):
            networks = get_networks(Array({"number": 1, "orderby": Array({"domain_length": "DESC"})}, {"domain__in": domains}))
            if (not php_empty(lambda : networks)):
                return php_array_shift(networks)
            # end if
            return False
        # end if
        networks = get_networks(Array({"orderby": Array({"domain_length": "DESC", "path_length": "DESC"})}, {"domain__in": domains, "path__in": paths}))
        #// 
        #// Domains are sorted by length of domain, then by length of path.
        #// The domain must match for the path to be considered. Otherwise,
        #// a network with the path of / will suffice.
        #//
        found = False
        for network in networks:
            if network.domain == domain or str("www.") + str(network.domain) == domain:
                if php_in_array(network.path, paths, True):
                    found = True
                    break
                # end if
            # end if
            if "/" == network.path:
                found = True
                break
            # end if
        # end for
        if True == found:
            return network
        # end if
        return False
    # end def get_by_path
# end class WP_Network
