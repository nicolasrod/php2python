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
#// Network API
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 5.1.0
#// 
#// 
#// Retrieves network data given a network ID or network object.
#// 
#// Network data will be cached and returned after being passed through a filter.
#// If the provided network is empty, the current network global will be used.
#// 
#// @since 4.6.0
#// 
#// @global WP_Network $current_site
#// 
#// @param WP_Network|int|null $network Optional. Network to retrieve. Default is the current network.
#// @return WP_Network|null The network object or null if not found.
#//
def get_network(network_=None, *_args_):
    
    
    global current_site_
    php_check_if_defined("current_site_")
    if php_empty(lambda : network_) and (php_isset(lambda : current_site_)):
        network_ = current_site_
    # end if
    if type(network_).__name__ == "WP_Network":
        _network_ = network_
    elif php_is_object(network_):
        _network_ = php_new_class("WP_Network", lambda : WP_Network(network_))
    else:
        _network_ = WP_Network.get_instance(network_)
    # end if
    if (not _network_):
        return None
    # end if
    #// 
    #// Fires after a network is retrieved.
    #// 
    #// @since 4.6.0
    #// 
    #// @param WP_Network $_network Network data.
    #//
    _network_ = apply_filters("get_network", _network_)
    return _network_
# end def get_network
#// 
#// Retrieves a list of networks.
#// 
#// @since 4.6.0
#// 
#// @param string|array $args Optional. Array or string of arguments. See WP_Network_Query::parse_query()
#// for information on accepted arguments. Default empty array.
#// @return array|int List of WP_Network objects, a list of network ids when 'fields' is set to 'ids',
#// or the number of networks when 'count' is passed as a query var.
#//
def get_networks(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    query_ = php_new_class("WP_Network_Query", lambda : WP_Network_Query())
    return query_.query(args_)
# end def get_networks
#// 
#// Removes a network from the object cache.
#// 
#// @since 4.6.0
#// 
#// @global bool $_wp_suspend_cache_invalidation
#// 
#// @param int|array $ids Network ID or an array of network IDs to remove from cache.
#//
def clean_network_cache(ids_=None, *_args_):
    
    
    global _wp_suspend_cache_invalidation_
    php_check_if_defined("_wp_suspend_cache_invalidation_")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation_)):
        return
    # end if
    for id_ in ids_:
        wp_cache_delete(id_, "networks")
        #// 
        #// Fires immediately after a network has been removed from the object cache.
        #// 
        #// @since 4.6.0
        #// 
        #// @param int $id Network ID.
        #//
        do_action("clean_network_cache", id_)
    # end for
    wp_cache_set("last_changed", php_microtime(), "networks")
# end def clean_network_cache
#// 
#// Updates the network cache of given networks.
#// 
#// Will add the networks in $networks to the cache. If network ID already exists
#// in the network cache then it will not be updated. The network is added to the
#// cache using the network group with the key using the ID of the networks.
#// 
#// @since 4.6.0
#// 
#// @param array $networks Array of network row objects.
#//
def update_network_cache(networks_=None, *_args_):
    
    
    for network_ in networks_:
        wp_cache_add(network_.id, network_, "networks")
    # end for
# end def update_network_cache
#// 
#// Adds any networks from the given IDs to the cache that do not already exist in cache.
#// 
#// @since 4.6.0
#// @access private
#// 
#// @see update_network_cache()
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $network_ids Array of network IDs.
#//
def _prime_network_caches(network_ids_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    non_cached_ids_ = _get_non_cached_ids(network_ids_, "networks")
    if (not php_empty(lambda : non_cached_ids_)):
        fresh_networks_ = wpdb_.get_results(php_sprintf(str("SELECT ") + str(wpdb_.site) + str(".* FROM ") + str(wpdb_.site) + str(" WHERE id IN (%s)"), join(",", php_array_map("intval", non_cached_ids_))))
        #// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
        update_network_cache(fresh_networks_)
    # end if
# end def _prime_network_caches
