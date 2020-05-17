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
#// Site API
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 5.1.0
#// 
#// 
#// Inserts a new site into the database.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $data {
#// Data for the new site that should be inserted.
#// 
#// @type string $domain       Site domain. Default empty string.
#// @type string $path         Site path. Default '/'.
#// @type int    $network_id   The site's network ID. Default is the current network ID.
#// @type string $registered   When the site was registered, in SQL datetime format. Default is
#// the current time.
#// @type string $last_updated When the site was last updated, in SQL datetime format. Default is
#// the value of $registered.
#// @type int    $public       Whether the site is public. Default 1.
#// @type int    $archived     Whether the site is archived. Default 0.
#// @type int    $mature       Whether the site is mature. Default 0.
#// @type int    $spam         Whether the site is spam. Default 0.
#// @type int    $deleted      Whether the site is deleted. Default 0.
#// @type int    $lang_id      The site's language ID. Currently unused. Default 0.
#// @type int    $user_id      User ID for the site administrator. Passed to the
#// `wp_initialize_site` hook.
#// @type string $title        Site title. Default is 'Site %d' where %d is the site ID. Passed
#// to the `wp_initialize_site` hook.
#// @type array  $options      Custom option $key => $value pairs to use. Default empty array. Passed
#// to the `wp_initialize_site` hook.
#// @type array  $meta         Custom site metadata $key => $value pairs to use. Default empty array.
#// Passed to the `wp_initialize_site` hook.
#// }
#// @return int|WP_Error The new site's ID on success, or error object on failure.
#//
def wp_insert_site(data_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    now_ = current_time("mysql", True)
    defaults_ = Array({"domain": "", "path": "/", "network_id": get_current_network_id(), "registered": now_, "last_updated": now_, "public": 1, "archived": 0, "mature": 0, "spam": 0, "deleted": 0, "lang_id": 0})
    prepared_data_ = wp_prepare_site_data(data_, defaults_)
    if is_wp_error(prepared_data_):
        return prepared_data_
    # end if
    if False == wpdb_.insert(wpdb_.blogs, prepared_data_):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert site into the database."), wpdb_.last_error))
    # end if
    clean_blog_cache(wpdb_.insert_id)
    new_site_ = get_site(wpdb_.insert_id)
    if (not new_site_):
        return php_new_class("WP_Error", lambda : WP_Error("get_site_error", __("Could not retrieve site data.")))
    # end if
    #// 
    #// Fires once a site has been inserted into the database.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $new_site New site object.
    #//
    do_action("wp_insert_site", new_site_)
    #// Extract the passed arguments that may be relevant for site initialization.
    args_ = php_array_diff_key(data_, defaults_)
    if (php_isset(lambda : args_["site_id"])):
        args_["site_id"] = None
    # end if
    #// 
    #// Fires when a site's initialization routine should be executed.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $new_site New site object.
    #// @param array   $args     Arguments for the initialization.
    #//
    do_action("wp_initialize_site", new_site_, args_)
    #// Only compute extra hook parameters if the deprecated hook is actually in use.
    if has_action("wpmu_new_blog"):
        user_id_ = args_["user_id"] if (not php_empty(lambda : args_["user_id"])) else 0
        meta_ = args_["options"] if (not php_empty(lambda : args_["options"])) else Array()
        #// WPLANG was passed with `$meta` to the `wpmu_new_blog` hook prior to 5.1.0.
        if (not php_array_key_exists("WPLANG", meta_)):
            meta_["WPLANG"] = get_network_option(new_site_.network_id, "WPLANG")
        # end if
        #// Rebuild the data expected by the `wpmu_new_blog` hook prior to 5.1.0 using whitelisted keys.
        #// The `$site_data_whitelist` matches the one used in `wpmu_create_blog()`.
        site_data_whitelist_ = Array("public", "archived", "mature", "spam", "deleted", "lang_id")
        meta_ = php_array_merge(php_array_intersect_key(data_, php_array_flip(site_data_whitelist_)), meta_)
        #// 
        #// Fires immediately after a new site is created.
        #// 
        #// @since MU (3.0.0)
        #// @deprecated 5.1.0 Use {@see 'wp_insert_site'} instead.
        #// 
        #// @param int    $site_id    Site ID.
        #// @param int    $user_id    User ID.
        #// @param string $domain     Site domain.
        #// @param string $path       Site path.
        #// @param int    $network_id Network ID. Only relevant on multi-network installations.
        #// @param array  $meta       Meta data. Used to set initial site options.
        #//
        do_action_deprecated("wpmu_new_blog", Array(new_site_.id, user_id_, new_site_.domain, new_site_.path, new_site_.network_id, meta_), "5.1.0", "wp_insert_site")
    # end if
    return php_int(new_site_.id)
# end def wp_insert_site
#// 
#// Updates a site in the database.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int   $site_id ID of the site that should be updated.
#// @param array $data    Site data to update. See {@see wp_insert_site()} for the list of supported keys.
#// @return int|WP_Error The updated site's ID on success, or error object on failure.
#//
def wp_update_site(site_id_=None, data_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : site_id_):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    old_site_ = get_site(site_id_)
    if (not old_site_):
        return php_new_class("WP_Error", lambda : WP_Error("site_not_exist", __("Site does not exist.")))
    # end if
    defaults_ = old_site_.to_array()
    defaults_["network_id"] = php_int(defaults_["site_id"])
    defaults_["last_updated"] = current_time("mysql", True)
    defaults_["blog_id"] = None
    defaults_["site_id"] = None
    data_ = wp_prepare_site_data(data_, defaults_, old_site_)
    if is_wp_error(data_):
        return data_
    # end if
    if False == wpdb_.update(wpdb_.blogs, data_, Array({"blog_id": old_site_.id})):
        return php_new_class("WP_Error", lambda : WP_Error("db_update_error", __("Could not update site in the database."), wpdb_.last_error))
    # end if
    clean_blog_cache(old_site_)
    new_site_ = get_site(old_site_.id)
    #// 
    #// Fires once a site has been updated in the database.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $new_site New site object.
    #// @param WP_Site $old_site Old site object.
    #//
    do_action("wp_update_site", new_site_, old_site_)
    return php_int(new_site_.id)
# end def wp_update_site
#// 
#// Deletes a site from the database.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $site_id ID of the site that should be deleted.
#// @return WP_Site|WP_Error The deleted site object on success, or error object on failure.
#//
def wp_delete_site(site_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : site_id_):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    old_site_ = get_site(site_id_)
    if (not old_site_):
        return php_new_class("WP_Error", lambda : WP_Error("site_not_exist", __("Site does not exist.")))
    # end if
    errors_ = php_new_class("WP_Error", lambda : WP_Error())
    #// 
    #// Fires before a site should be deleted from the database.
    #// 
    #// Plugins should amend the `$errors` object via its `WP_Error::add()` method. If any errors
    #// are present, the site will not be deleted.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Error $errors   Error object to add validation errors to.
    #// @param WP_Site  $old_site The site object to be deleted.
    #//
    do_action("wp_validate_site_deletion", errors_, old_site_)
    if (not php_empty(lambda : errors_.errors)):
        return errors_
    # end if
    #// 
    #// Fires before a site is deleted.
    #// 
    #// @since MU (3.0.0)
    #// @deprecated 5.1.0
    #// 
    #// @param int  $site_id The site ID.
    #// @param bool $drop    True if site's table should be dropped. Default is false.
    #//
    do_action_deprecated("delete_blog", Array(old_site_.id, True), "5.1.0")
    #// 
    #// Fires when a site's uninitialization routine should be executed.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $old_site Deleted site object.
    #//
    do_action("wp_uninitialize_site", old_site_)
    if is_site_meta_supported():
        blog_meta_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.blogmeta) + str(" WHERE blog_id = %d "), old_site_.id))
        for mid_ in blog_meta_ids_:
            delete_metadata_by_mid("blog", mid_)
        # end for
    # end if
    if False == wpdb_.delete(wpdb_.blogs, Array({"blog_id": old_site_.id})):
        return php_new_class("WP_Error", lambda : WP_Error("db_delete_error", __("Could not delete site from the database."), wpdb_.last_error))
    # end if
    clean_blog_cache(old_site_)
    #// 
    #// Fires once a site has been deleted from the database.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $old_site Deleted site object.
    #//
    do_action("wp_delete_site", old_site_)
    #// 
    #// Fires after the site is deleted from the network.
    #// 
    #// @since 4.8.0
    #// @deprecated 5.1.0
    #// 
    #// @param int  $site_id The site ID.
    #// @param bool $drop    True if site's tables should be dropped. Default is false.
    #//
    do_action_deprecated("deleted_blog", Array(old_site_.id, True), "5.1.0")
    return old_site_
# end def wp_delete_site
#// 
#// Retrieves site data given a site ID or site object.
#// 
#// Site data will be cached and returned after being passed through a filter.
#// If the provided site is empty, the current site global will be used.
#// 
#// @since 4.6.0
#// 
#// @param WP_Site|int|null $site Optional. Site to retrieve. Default is the current site.
#// @return WP_Site|null The site object or null if not found.
#//
def get_site(site_=None, *_args_):
    if site_ is None:
        site_ = None
    # end if
    
    if php_empty(lambda : site_):
        site_ = get_current_blog_id()
    # end if
    if type(site_).__name__ == "WP_Site":
        _site_ = site_
    elif php_is_object(site_):
        _site_ = php_new_class("WP_Site", lambda : WP_Site(site_))
    else:
        _site_ = WP_Site.get_instance(site_)
    # end if
    if (not _site_):
        return None
    # end if
    #// 
    #// Fires after a site is retrieved.
    #// 
    #// @since 4.6.0
    #// 
    #// @param WP_Site $_site Site data.
    #//
    _site_ = apply_filters("get_site", _site_)
    return _site_
# end def get_site
#// 
#// Adds any sites from the given ids to the cache that do not already exist in cache.
#// 
#// @since 4.6.0
#// @since 5.1.0 Introduced the `$update_meta_cache` parameter.
#// @access private
#// 
#// @see update_site_cache()
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $ids               ID list.
#// @param bool  $update_meta_cache Optional. Whether to update the meta cache. Default true.
#//
def _prime_site_caches(ids_=None, update_meta_cache_=None, *_args_):
    if update_meta_cache_ is None:
        update_meta_cache_ = True
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    non_cached_ids_ = _get_non_cached_ids(ids_, "sites")
    if (not php_empty(lambda : non_cached_ids_)):
        fresh_sites_ = wpdb_.get_results(php_sprintf(str("SELECT * FROM ") + str(wpdb_.blogs) + str(" WHERE blog_id IN (%s)"), join(",", php_array_map("intval", non_cached_ids_))))
        #// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
        update_site_cache(fresh_sites_, update_meta_cache_)
    # end if
# end def _prime_site_caches
#// 
#// Updates sites in cache.
#// 
#// @since 4.6.0
#// @since 5.1.0 Introduced the `$update_meta_cache` parameter.
#// 
#// @param array $sites             Array of site objects.
#// @param bool  $update_meta_cache Whether to update site meta cache. Default true.
#//
def update_site_cache(sites_=None, update_meta_cache_=None, *_args_):
    if update_meta_cache_ is None:
        update_meta_cache_ = True
    # end if
    
    if (not sites_):
        return
    # end if
    site_ids_ = Array()
    for site_ in sites_:
        site_ids_[-1] = site_.blog_id
        wp_cache_add(site_.blog_id, site_, "sites")
        wp_cache_add(site_.blog_id + "short", site_, "blog-details")
    # end for
    if update_meta_cache_:
        update_sitemeta_cache(site_ids_)
    # end if
# end def update_site_cache
#// 
#// Updates metadata cache for list of site IDs.
#// 
#// Performs SQL query to retrieve all metadata for the sites matching `$site_ids` and stores them in the cache.
#// Subsequent calls to `get_site_meta()` will not need to query the database.
#// 
#// @since 5.1.0
#// 
#// @param array $site_ids List of site IDs.
#// @return array|false Returns false if there is nothing to update. Returns an array of metadata on success.
#//
def update_sitemeta_cache(site_ids_=None, *_args_):
    
    
    #// Ensure this filter is hooked in even if the function is called early.
    if (not has_filter("update_blog_metadata_cache", "wp_check_site_meta_support_prefilter")):
        add_filter("update_blog_metadata_cache", "wp_check_site_meta_support_prefilter")
    # end if
    return update_meta_cache("blog", site_ids_)
# end def update_sitemeta_cache
#// 
#// Retrieves a list of sites matching requested arguments.
#// 
#// @since 4.6.0
#// @since 4.8.0 Introduced the 'lang_id', 'lang__in', and 'lang__not_in' parameters.
#// 
#// @see WP_Site_Query::parse_query()
#// 
#// @param string|array $args {
#// Optional. Array or query string of site query parameters. Default empty.
#// 
#// @type array        $site__in          Array of site IDs to include. Default empty.
#// @type array        $site__not_in      Array of site IDs to exclude. Default empty.
#// @type bool         $count             Whether to return a site count (true) or array of site objects.
#// Default false.
#// @type array        $date_query        Date query clauses to limit sites by. See WP_Date_Query.
#// Default null.
#// @type string       $fields            Site fields to return. Accepts 'ids' (returns an array of site IDs)
#// or empty (returns an array of complete site objects). Default empty.
#// @type int          $ID                A site ID to only return that site. Default empty.
#// @type int          $number            Maximum number of sites to retrieve. Default 100.
#// @type int          $offset            Number of sites to offset the query. Used to build LIMIT clause.
#// Default 0.
#// @type bool         $no_found_rows     Whether to disable the `SQL_CALC_FOUND_ROWS` query. Default true.
#// @type string|array $orderby           Site status or array of statuses. Accepts 'id', 'domain', 'path',
#// 'network_id', 'last_updated', 'registered', 'domain_length',
#// 'path_length', 'site__in' and 'network__in'. Also accepts false,
#// an empty array, or 'none' to disable `ORDER BY` clause.
#// Default 'id'.
#// @type string       $order             How to order retrieved sites. Accepts 'ASC', 'DESC'. Default 'ASC'.
#// @type int          $network_id        Limit results to those affiliated with a given network ID. If 0,
#// include all networks. Default 0.
#// @type array        $network__in       Array of network IDs to include affiliated sites for. Default empty.
#// @type array        $network__not_in   Array of network IDs to exclude affiliated sites for. Default empty.
#// @type string       $domain            Limit results to those affiliated with a given domain. Default empty.
#// @type array        $domain__in        Array of domains to include affiliated sites for. Default empty.
#// @type array        $domain__not_in    Array of domains to exclude affiliated sites for. Default empty.
#// @type string       $path              Limit results to those affiliated with a given path. Default empty.
#// @type array        $path__in          Array of paths to include affiliated sites for. Default empty.
#// @type array        $path__not_in      Array of paths to exclude affiliated sites for. Default empty.
#// @type int          $public            Limit results to public sites. Accepts '1' or '0'. Default empty.
#// @type int          $archived          Limit results to archived sites. Accepts '1' or '0'. Default empty.
#// @type int          $mature            Limit results to mature sites. Accepts '1' or '0'. Default empty.
#// @type int          $spam              Limit results to spam sites. Accepts '1' or '0'. Default empty.
#// @type int          $deleted           Limit results to deleted sites. Accepts '1' or '0'. Default empty.
#// @type int          $lang_id           Limit results to a language ID. Default empty.
#// @type array        $lang__in          Array of language IDs to include affiliated sites for. Default empty.
#// @type array        $lang__not_in      Array of language IDs to exclude affiliated sites for. Default empty.
#// @type string       $search            Search term(s) to retrieve matching sites for. Default empty.
#// @type array        $search_columns    Array of column names to be searched. Accepts 'domain' and 'path'.
#// Default empty array.
#// @type bool         $update_site_cache Whether to prime the cache for found sites. Default true.
#// }
#// @return array|int List of WP_Site objects, a list of site ids when 'fields' is set to 'ids',
#// or the number of sites when 'count' is passed as a query var.
#//
def get_sites(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    query_ = php_new_class("WP_Site_Query", lambda : WP_Site_Query())
    return query_.query(args_)
# end def get_sites
#// 
#// Prepares site data for insertion or update in the database.
#// 
#// @since 5.1.0
#// 
#// @param array        $data     Associative array of site data passed to the respective function.
#// See {@see wp_insert_site()} for the possibly included data.
#// @param array        $defaults Site data defaults to parse $data against.
#// @param WP_Site|null $old_site Optional. Old site object if an update, or null if an insertion.
#// Default null.
#// @return array|WP_Error Site data ready for a database transaction, or WP_Error in case a validation
#// error occurred.
#//
def wp_prepare_site_data(data_=None, defaults_=None, old_site_=None, *_args_):
    if old_site_ is None:
        old_site_ = None
    # end if
    
    #// Maintain backward-compatibility with `$site_id` as network ID.
    if (php_isset(lambda : data_["site_id"])):
        if (not php_empty(lambda : data_["site_id"])) and php_empty(lambda : data_["network_id"]):
            data_["network_id"] = data_["site_id"]
        # end if
        data_["site_id"] = None
    # end if
    #// 
    #// Filters passed site data in order to normalize it.
    #// 
    #// @since 5.1.0
    #// 
    #// @param array $data Associative array of site data passed to the respective function.
    #// See {@see wp_insert_site()} for the possibly included data.
    #//
    data_ = apply_filters("wp_normalize_site_data", data_)
    whitelist_ = Array("domain", "path", "network_id", "registered", "last_updated", "public", "archived", "mature", "spam", "deleted", "lang_id")
    data_ = php_array_intersect_key(wp_parse_args(data_, defaults_), php_array_flip(whitelist_))
    errors_ = php_new_class("WP_Error", lambda : WP_Error())
    #// 
    #// Fires when data should be validated for a site prior to inserting or updating in the database.
    #// 
    #// Plugins should amend the `$errors` object via its `WP_Error::add()` method.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Error     $errors   Error object to add validation errors to.
    #// @param array        $data     Associative array of complete site data. See {@see wp_insert_site()}
    #// for the included data.
    #// @param WP_Site|null $old_site The old site object if the data belongs to a site being updated,
    #// or null if it is a new site being inserted.
    #//
    do_action("wp_validate_site_data", errors_, data_, old_site_)
    if (not php_empty(lambda : errors_.errors)):
        return errors_
    # end if
    #// Prepare for database.
    data_["site_id"] = data_["network_id"]
    data_["network_id"] = None
    return data_
# end def wp_prepare_site_data
#// 
#// Normalizes data for a site prior to inserting or updating in the database.
#// 
#// @since 5.1.0
#// 
#// @param array $data Associative array of site data passed to the respective function.
#// See {@see wp_insert_site()} for the possibly included data.
#// @return array Normalized site data.
#//
def wp_normalize_site_data(data_=None, *_args_):
    
    
    #// Sanitize domain if passed.
    if php_array_key_exists("domain", data_):
        data_["domain"] = php_trim(data_["domain"])
        data_["domain"] = php_preg_replace("/\\s+/", "", sanitize_user(data_["domain"], True))
        if is_subdomain_install():
            data_["domain"] = php_str_replace("@", "", data_["domain"])
        # end if
    # end if
    #// Sanitize path if passed.
    if php_array_key_exists("path", data_):
        data_["path"] = trailingslashit("/" + php_trim(data_["path"], "/"))
    # end if
    #// Sanitize network ID if passed.
    if php_array_key_exists("network_id", data_):
        data_["network_id"] = php_int(data_["network_id"])
    # end if
    #// Sanitize status fields if passed.
    status_fields_ = Array("public", "archived", "mature", "spam", "deleted")
    for status_field_ in status_fields_:
        if php_array_key_exists(status_field_, data_):
            data_[status_field_] = php_int(data_[status_field_])
        # end if
    # end for
    #// Strip date fields if empty.
    date_fields_ = Array("registered", "last_updated")
    for date_field_ in date_fields_:
        if (not php_array_key_exists(date_field_, data_)):
            continue
        # end if
        if php_empty(lambda : data_[date_field_]) or "0000-00-00 00:00:00" == data_[date_field_]:
            data_[date_field_] = None
        # end if
    # end for
    return data_
# end def wp_normalize_site_data
#// 
#// Validates data for a site prior to inserting or updating in the database.
#// 
#// @since 5.1.0
#// 
#// @param WP_Error     $errors   Error object, passed by reference. Will contain validation errors if
#// any occurred.
#// @param array        $data     Associative array of complete site data. See {@see wp_insert_site()}
#// for the included data.
#// @param WP_Site|null $old_site The old site object if the data belongs to a site being updated,
#// or null if it is a new site being inserted.
#//
def wp_validate_site_data(errors_=None, data_=None, old_site_=None, *_args_):
    if old_site_ is None:
        old_site_ = None
    # end if
    
    #// A domain must always be present.
    if php_empty(lambda : data_["domain"]):
        errors_.add("site_empty_domain", __("Site domain must not be empty."))
    # end if
    #// A path must always be present.
    if php_empty(lambda : data_["path"]):
        errors_.add("site_empty_path", __("Site path must not be empty."))
    # end if
    #// A network ID must always be present.
    if php_empty(lambda : data_["network_id"]):
        errors_.add("site_empty_network_id", __("Site network ID must be provided."))
    # end if
    #// Both registration and last updated dates must always be present and valid.
    date_fields_ = Array("registered", "last_updated")
    for date_field_ in date_fields_:
        if php_empty(lambda : data_[date_field_]):
            errors_.add("site_empty_" + date_field_, __("Both registration and last updated dates must be provided."))
            break
        # end if
        #// Allow '0000-00-00 00:00:00', although it be stripped out at this point.
        if "0000-00-00 00:00:00" != data_[date_field_]:
            month_ = php_substr(data_[date_field_], 5, 2)
            day_ = php_substr(data_[date_field_], 8, 2)
            year_ = php_substr(data_[date_field_], 0, 4)
            valid_date_ = wp_checkdate(month_, day_, year_, data_[date_field_])
            if (not valid_date_):
                errors_.add("site_invalid_" + date_field_, __("Both registration and last updated dates must be valid dates."))
                break
            # end if
        # end if
    # end for
    if (not php_empty(lambda : errors_.errors)):
        return
    # end if
    #// If a new site, or domain/path/network ID have changed, ensure uniqueness.
    if (not old_site_) or data_["domain"] != old_site_.domain or data_["path"] != old_site_.path or data_["network_id"] != old_site_.network_id:
        if domain_exists(data_["domain"], data_["path"], data_["network_id"]):
            errors_.add("site_taken", __("Sorry, that site already exists!"))
        # end if
    # end if
# end def wp_validate_site_data
#// 
#// Runs the initialization routine for a given site.
#// 
#// This process includes creating the site's database tables and
#// populating them with defaults.
#// 
#// @since 5.1.0
#// 
#// @global wpdb     $wpdb     WordPress database abstraction object.
#// @global WP_Roles $wp_roles WordPress role management object.
#// 
#// @param int|WP_Site $site_id Site ID or object.
#// @param array       $args    {
#// Optional. Arguments to modify the initialization behavior.
#// 
#// @type int    $user_id Required. User ID for the site administrator.
#// @type string $title   Site title. Default is 'Site %d' where %d is the
#// site ID.
#// @type array  $options Custom option $key => $value pairs to use. Default
#// empty array.
#// @type array  $meta    Custom site metadata $key => $value pairs to use.
#// Default empty array.
#// }
#// @return bool|WP_Error True on success, or error object on failure.
#//
def wp_initialize_site(site_id_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wpdb_
    global wp_roles_
    php_check_if_defined("wpdb_","wp_roles_")
    if php_empty(lambda : site_id_):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    site_ = get_site(site_id_)
    if (not site_):
        return php_new_class("WP_Error", lambda : WP_Error("site_invalid_id", __("Site with the ID does not exist.")))
    # end if
    if wp_is_site_initialized(site_):
        return php_new_class("WP_Error", lambda : WP_Error("site_already_initialized", __("The site appears to be already initialized.")))
    # end if
    network_ = get_network(site_.network_id)
    if (not network_):
        network_ = get_network()
    # end if
    args_ = wp_parse_args(args_, Array({"user_id": 0, "title": php_sprintf(__("Site %d"), site_.id), "options": Array(), "meta": Array()}))
    #// 
    #// Filters the arguments for initializing a site.
    #// 
    #// @since 5.1.0
    #// 
    #// @param array      $args    Arguments to modify the initialization behavior.
    #// @param WP_Site    $site    Site that is being initialized.
    #// @param WP_Network $network Network that the site belongs to.
    #//
    args_ = apply_filters("wp_initialize_site_args", args_, site_, network_)
    orig_installing_ = wp_installing()
    if (not orig_installing_):
        wp_installing(True)
    # end if
    switch_ = False
    if get_current_blog_id() != site_.id:
        switch_ = True
        switch_to_blog(site_.id)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
    #// Set up the database tables.
    make_db_current_silent("blog")
    home_scheme_ = "http"
    siteurl_scheme_ = "http"
    if (not is_subdomain_install()):
        if "https" == php_parse_url(get_home_url(network_.site_id), PHP_URL_SCHEME):
            home_scheme_ = "https"
        # end if
        if "https" == php_parse_url(get_network_option(network_.id, "siteurl"), PHP_URL_SCHEME):
            siteurl_scheme_ = "https"
        # end if
    # end if
    #// Populate the site's options.
    populate_options(php_array_merge(Array({"home": untrailingslashit(home_scheme_ + "://" + site_.domain + site_.path), "siteurl": untrailingslashit(siteurl_scheme_ + "://" + site_.domain + site_.path), "blogname": wp_unslash(args_["title"]), "admin_email": "", "upload_path": UPLOADBLOGSDIR + str("/") + str(site_.id) + str("/files") if get_network_option(network_.id, "ms_files_rewriting") else get_blog_option(network_.site_id, "upload_path"), "blog_public": php_int(site_.public), "WPLANG": get_network_option(network_.id, "WPLANG")}), args_["options"]))
    #// Clean blog cache after populating options.
    clean_blog_cache(site_)
    #// Populate the site's roles.
    populate_roles()
    wp_roles_ = php_new_class("WP_Roles", lambda : WP_Roles())
    #// Populate metadata for the site.
    populate_site_meta(site_.id, args_["meta"])
    #// Remove all permissions that may exist for the site.
    table_prefix_ = wpdb_.get_blog_prefix()
    delete_metadata("user", 0, table_prefix_ + "user_level", None, True)
    #// Delete all.
    delete_metadata("user", 0, table_prefix_ + "capabilities", None, True)
    #// Delete all.
    #// Install default site content.
    wp_install_defaults(args_["user_id"])
    #// Set the site administrator.
    add_user_to_blog(site_.id, args_["user_id"], "administrator")
    if (not user_can(args_["user_id"], "manage_network")) and (not get_user_meta(args_["user_id"], "primary_blog", True)):
        update_user_meta(args_["user_id"], "primary_blog", site_.id)
    # end if
    if switch_:
        restore_current_blog()
    # end if
    wp_installing(orig_installing_)
    return True
# end def wp_initialize_site
#// 
#// Runs the uninitialization routine for a given site.
#// 
#// This process includes dropping the site's database tables and deleting its uploads directory.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Site $site_id Site ID or object.
#// @return bool|WP_Error True on success, or error object on failure.
#//
def wp_uninitialize_site(site_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : site_id_):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    site_ = get_site(site_id_)
    if (not site_):
        return php_new_class("WP_Error", lambda : WP_Error("site_invalid_id", __("Site with the ID does not exist.")))
    # end if
    if (not wp_is_site_initialized(site_)):
        return php_new_class("WP_Error", lambda : WP_Error("site_already_uninitialized", __("The site appears to be already uninitialized.")))
    # end if
    users_ = get_users(Array({"blog_id": site_.id, "fields": "ids"}))
    #// Remove users from the site.
    if (not php_empty(lambda : users_)):
        for user_id_ in users_:
            remove_user_from_blog(user_id_, site_.id)
        # end for
    # end if
    switch_ = False
    if get_current_blog_id() != site_.id:
        switch_ = True
        switch_to_blog(site_.id)
    # end if
    uploads_ = wp_get_upload_dir()
    tables_ = wpdb_.tables("blog")
    #// 
    #// Filters the tables to drop when the site is deleted.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string[] $tables  Array of names of the site tables to be dropped.
    #// @param int      $site_id The ID of the site to drop tables for.
    #//
    drop_tables_ = apply_filters("wpmu_drop_tables", tables_, site_.id)
    for table_ in drop_tables_:
        wpdb_.query(str("DROP TABLE IF EXISTS `") + str(table_) + str("`"))
        pass
    # end for
    #// 
    #// Filters the upload base directory to delete when the site is deleted.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $uploads['basedir'] Uploads path without subdirectory. @see wp_upload_dir()
    #// @param int    $site_id            The site ID.
    #//
    dir_ = apply_filters("wpmu_delete_blog_upload_dir", uploads_["basedir"], site_.id)
    dir_ = php_rtrim(dir_, DIRECTORY_SEPARATOR)
    top_dir_ = dir_
    stack_ = Array(dir_)
    index_ = 0
    while True:
        
        if not (index_ < php_count(stack_)):
            break
        # end if
        #// Get indexed directory from stack.
        dir_ = stack_[index_]
        #// phpcs:disable WordPress.PHP.NoSilencedErrors.Discouraged
        dh_ = php_no_error(lambda: php_opendir(dir_))
        if dh_:
            file_ = php_no_error(lambda: php_readdir(dh_))
            while True:
                
                if not (False != file_):
                    break
                # end if
                if "." == file_ or ".." == file_:
                    file_ = php_no_error(lambda: php_readdir(dh_))
                    continue
                # end if
                if php_no_error(lambda: php_is_dir(dir_ + DIRECTORY_SEPARATOR + file_)):
                    stack_[-1] = dir_ + DIRECTORY_SEPARATOR + file_
                elif php_no_error(lambda: php_is_file(dir_ + DIRECTORY_SEPARATOR + file_)):
                    php_no_error(lambda: unlink(dir_ + DIRECTORY_SEPARATOR + file_))
                # end if
                file_ = php_no_error(lambda: php_readdir(dh_))
            # end while
            php_no_error(lambda: php_closedir(dh_))
        # end if
        index_ += 1
    # end while
    stack_ = array_reverse(stack_)
    #// Last added directories are deepest.
    for dir_ in stack_:
        if dir_ != top_dir_:
            php_no_error(lambda: rmdir(dir_))
        # end if
    # end for
    #// phpcs:enable WordPress.PHP.NoSilencedErrors.Discouraged
    if switch_:
        restore_current_blog()
    # end if
    return True
# end def wp_uninitialize_site
#// 
#// Checks whether a site is initialized.
#// 
#// A site is considered initialized when its database tables are present.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Site $site_id Site ID or object.
#// @return bool True if the site is initialized, false otherwise.
#//
def wp_is_site_initialized(site_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_is_object(site_id_):
        site_id_ = site_id_.blog_id
    # end if
    site_id_ = php_int(site_id_)
    #// 
    #// Filters the check for whether a site is initialized before the database is accessed.
    #// 
    #// Returning a non-null value will effectively short-circuit the function, returning
    #// that value instead.
    #// 
    #// @since 5.1.0
    #// 
    #// @param bool|null $pre     The value to return instead. Default null
    #// to continue with the check.
    #// @param int       $site_id The site ID that is being checked.
    #//
    pre_ = apply_filters("pre_wp_is_site_initialized", None, site_id_)
    if None != pre_:
        return php_bool(pre_)
    # end if
    switch_ = False
    if get_current_blog_id() != site_id_:
        switch_ = True
        remove_action("switch_blog", "wp_switch_roles_and_user", 1)
        switch_to_blog(site_id_)
    # end if
    suppress_ = wpdb_.suppress_errors()
    result_ = php_bool(wpdb_.get_results(str("DESCRIBE ") + str(wpdb_.posts)))
    wpdb_.suppress_errors(suppress_)
    if switch_:
        restore_current_blog()
        add_action("switch_blog", "wp_switch_roles_and_user", 1, 2)
    # end if
    return result_
# end def wp_is_site_initialized
#// 
#// Clean the blog cache
#// 
#// @since 3.5.0
#// 
#// @global bool $_wp_suspend_cache_invalidation
#// 
#// @param WP_Site|int $blog The site object or ID to be cleared from cache.
#//
def clean_blog_cache(blog_=None, *_args_):
    
    
    global _wp_suspend_cache_invalidation_
    php_check_if_defined("_wp_suspend_cache_invalidation_")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation_)):
        return
    # end if
    if php_empty(lambda : blog_):
        return
    # end if
    blog_id_ = blog_
    blog_ = get_site(blog_id_)
    if (not blog_):
        if (not php_is_numeric(blog_id_)):
            return
        # end if
        #// Make sure a WP_Site object exists even when the site has been deleted.
        blog_ = php_new_class("WP_Site", lambda : WP_Site(Array({"blog_id": blog_id_, "domain": None, "path": None})))
    # end if
    blog_id_ = blog_.blog_id
    domain_path_key_ = php_md5(blog_.domain + blog_.path)
    wp_cache_delete(blog_id_, "sites")
    wp_cache_delete(blog_id_, "site-details")
    wp_cache_delete(blog_id_, "blog-details")
    wp_cache_delete(blog_id_ + "short", "blog-details")
    wp_cache_delete(domain_path_key_, "blog-lookup")
    wp_cache_delete(domain_path_key_, "blog-id-cache")
    wp_cache_delete(blog_id_, "blog_meta")
    #// 
    #// Fires immediately after a site has been removed from the object cache.
    #// 
    #// @since 4.6.0
    #// 
    #// @param int     $id              Blog ID.
    #// @param WP_Site $blog            Site object.
    #// @param string  $domain_path_key md5 hash of domain and path.
    #//
    do_action("clean_site_cache", blog_id_, blog_, domain_path_key_)
    wp_cache_set("last_changed", php_microtime(), "sites")
    #// 
    #// Fires after the blog details cache is cleared.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.9.0 Use {@see 'clean_site_cache'} instead.
    #// 
    #// @param int $blog_id Blog ID.
    #//
    do_action_deprecated("refresh_blog_details", Array(blog_id_), "4.9.0", "clean_site_cache")
# end def clean_blog_cache
#// 
#// Adds metadata to a site.
#// 
#// @since 5.1.0
#// 
#// @param int    $site_id    Site ID.
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Metadata value. Must be serializable if non-scalar.
#// @param bool   $unique     Optional. Whether the same key should not be added.
#// Default false.
#// @return int|false Meta ID on success, false on failure.
#//
def add_site_meta(site_id_=None, meta_key_=None, meta_value_=None, unique_=None, *_args_):
    if unique_ is None:
        unique_ = False
    # end if
    
    return add_metadata("blog", site_id_, meta_key_, meta_value_, unique_)
# end def add_site_meta
#// 
#// Removes metadata matching criteria from a site.
#// 
#// You can match based on the key, or key and value. Removing based on key and
#// value, will keep from removing duplicate metadata with the same key. It also
#// allows removing all metadata matching key, if needed.
#// 
#// @since 5.1.0
#// 
#// @param int    $site_id    Site ID.
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Optional. Metadata value. Must be serializable if
#// non-scalar. Default empty.
#// @return bool True on success, false on failure.
#//
def delete_site_meta(site_id_=None, meta_key_=None, meta_value_="", *_args_):
    
    
    return delete_metadata("blog", site_id_, meta_key_, meta_value_)
# end def delete_site_meta
#// 
#// Retrieves metadata for a site.
#// 
#// @since 5.1.0
#// 
#// @param int    $site_id Site ID.
#// @param string $key     Optional. The meta key to retrieve. By default, returns
#// data for all keys. Default empty.
#// @param bool   $single  Optional. Whether to return a single value. Default false.
#// @return mixed Will be an array if $single is false. Will be value of meta data
#// field if $single is true.
#//
def get_site_meta(site_id_=None, key_="", single_=None, *_args_):
    if single_ is None:
        single_ = False
    # end if
    
    return get_metadata("blog", site_id_, key_, single_)
# end def get_site_meta
#// 
#// Updates metadata for a site.
#// 
#// Use the $prev_value parameter to differentiate between meta fields with the
#// same key and site ID.
#// 
#// If the meta field for the site does not exist, it will be added.
#// 
#// @since 5.1.0
#// 
#// @param int    $site_id    Site ID.
#// @param string $meta_key   Metadata key.
#// @param mixed  $meta_value Metadata value. Must be serializable if non-scalar.
#// @param mixed  $prev_value Optional. Previous value to check before removing.
#// Default empty.
#// @return int|bool Meta ID if the key didn't exist, true on successful update,
#// false on failure.
#//
def update_site_meta(site_id_=None, meta_key_=None, meta_value_=None, prev_value_="", *_args_):
    
    
    return update_metadata("blog", site_id_, meta_key_, meta_value_, prev_value_)
# end def update_site_meta
#// 
#// Deletes everything from site meta matching meta key.
#// 
#// @since 5.1.0
#// 
#// @param string $meta_key Metadata key to search for when deleting.
#// @return bool Whether the site meta key was deleted from the database.
#//
def delete_site_meta_by_key(meta_key_=None, *_args_):
    
    
    return delete_metadata("blog", None, meta_key_, "", True)
# end def delete_site_meta_by_key
#// 
#// Updates the count of sites for a network based on a changed site.
#// 
#// @since 5.1.0
#// 
#// @param WP_Site      $new_site The site object that has been inserted, updated or deleted.
#// @param WP_Site|null $old_site Optional. If $new_site has been updated, this must be the previous
#// state of that site. Default null.
#//
def wp_maybe_update_network_site_counts_on_update(new_site_=None, old_site_=None, *_args_):
    if old_site_ is None:
        old_site_ = None
    # end if
    
    if None == old_site_:
        wp_maybe_update_network_site_counts(new_site_.network_id)
        return
    # end if
    if new_site_.network_id != old_site_.network_id:
        wp_maybe_update_network_site_counts(new_site_.network_id)
        wp_maybe_update_network_site_counts(old_site_.network_id)
    # end if
# end def wp_maybe_update_network_site_counts_on_update
#// 
#// Triggers actions on site status updates.
#// 
#// @since 5.1.0
#// 
#// @param WP_Site      $new_site The site object after the update.
#// @param WP_Site|null $old_site Optional. If $new_site has been updated, this must be the previous
#// state of that site. Default null.
#//
def wp_maybe_transition_site_statuses_on_update(new_site_=None, old_site_=None, *_args_):
    if old_site_ is None:
        old_site_ = None
    # end if
    
    site_id_ = new_site_.id
    #// Use the default values for a site if no previous state is given.
    if (not old_site_):
        old_site_ = php_new_class("WP_Site", lambda : WP_Site(php_new_class("stdClass", lambda : stdClass())))
    # end if
    if new_site_.spam != old_site_.spam:
        if 1 == new_site_.spam:
            #// 
            #// Fires when the 'spam' status is added to a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_spam_blog", site_id_)
        else:
            #// 
            #// Fires when the 'spam' status is removed from a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_ham_blog", site_id_)
        # end if
    # end if
    if new_site_.mature != old_site_.mature:
        if 1 == new_site_.mature:
            #// 
            #// Fires when the 'mature' status is added to a site.
            #// 
            #// @since 3.1.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("mature_blog", site_id_)
        else:
            #// 
            #// Fires when the 'mature' status is removed from a site.
            #// 
            #// @since 3.1.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("unmature_blog", site_id_)
        # end if
    # end if
    if new_site_.archived != old_site_.archived:
        if 1 == new_site_.archived:
            #// 
            #// Fires when the 'archived' status is added to a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("archive_blog", site_id_)
        else:
            #// 
            #// Fires when the 'archived' status is removed from a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("unarchive_blog", site_id_)
        # end if
    # end if
    if new_site_.deleted != old_site_.deleted:
        if 1 == new_site_.deleted:
            #// 
            #// Fires when the 'deleted' status is added to a site.
            #// 
            #// @since 3.5.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_delete_blog", site_id_)
        else:
            #// 
            #// Fires when the 'deleted' status is removed from a site.
            #// 
            #// @since 3.5.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_undelete_blog", site_id_)
        # end if
    # end if
    if new_site_.public != old_site_.public:
        #// 
        #// Fires after the current blog's 'public' setting is updated.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param int    $site_id Site ID.
        #// @param string $value   The value of the site status.
        #//
        do_action("update_blog_public", site_id_, new_site_.public)
    # end if
# end def wp_maybe_transition_site_statuses_on_update
#// 
#// Cleans the necessary caches after specific site data has been updated.
#// 
#// @since 5.1.0
#// 
#// @param WP_Site $new_site The site object after the update.
#// @param WP_Site $old_site The site obejct prior to the update.
#//
def wp_maybe_clean_new_site_cache_on_update(new_site_=None, old_site_=None, *_args_):
    
    
    if old_site_.domain != new_site_.domain or old_site_.path != new_site_.path:
        clean_blog_cache(new_site_)
    # end if
# end def wp_maybe_clean_new_site_cache_on_update
#// 
#// Updates the `blog_public` option for a given site ID.
#// 
#// @since 5.1.0
#// 
#// @param int    $site_id Site ID.
#// @param string $public  The value of the site status.
#//
def wp_update_blog_public_option_on_site_update(site_id_=None, public_=None, *_args_):
    
    
    #// Bail if the site's database tables do not exist (yet).
    if (not wp_is_site_initialized(site_id_)):
        return
    # end if
    update_blog_option(site_id_, "blog_public", public_)
# end def wp_update_blog_public_option_on_site_update
#// 
#// Sets the last changed time for the 'sites' cache group.
#// 
#// @since 5.1.0
#//
def wp_cache_set_sites_last_changed(*_args_):
    
    
    wp_cache_set("last_changed", php_microtime(), "sites")
# end def wp_cache_set_sites_last_changed
#// 
#// Aborts calls to site meta if it is not supported.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param mixed $check Skip-value for whether to proceed site meta function execution.
#// @return mixed Original value of $check, or false if site meta is not supported.
#//
def wp_check_site_meta_support_prefilter(check_=None, *_args_):
    
    
    if (not is_site_meta_supported()):
        #// translators: %s: Database table name.
        _doing_it_wrong(__FUNCTION__, php_sprintf(__("The %s table is not installed. Please run the network database upgrade."), PHP_GLOBALS["wpdb"].blogmeta), "5.1.0")
        return False
    # end if
    return check_
# end def wp_check_site_meta_support_prefilter
