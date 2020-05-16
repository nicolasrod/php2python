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
def wp_insert_site(data=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    now = current_time("mysql", True)
    defaults = Array({"domain": "", "path": "/", "network_id": get_current_network_id(), "registered": now, "last_updated": now, "public": 1, "archived": 0, "mature": 0, "spam": 0, "deleted": 0, "lang_id": 0})
    prepared_data = wp_prepare_site_data(data, defaults)
    if is_wp_error(prepared_data):
        return prepared_data
    # end if
    if False == wpdb.insert(wpdb.blogs, prepared_data):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert site into the database."), wpdb.last_error))
    # end if
    clean_blog_cache(wpdb.insert_id)
    new_site = get_site(wpdb.insert_id)
    if (not new_site):
        return php_new_class("WP_Error", lambda : WP_Error("get_site_error", __("Could not retrieve site data.")))
    # end if
    #// 
    #// Fires once a site has been inserted into the database.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $new_site New site object.
    #//
    do_action("wp_insert_site", new_site)
    #// Extract the passed arguments that may be relevant for site initialization.
    args = php_array_diff_key(data, defaults)
    if (php_isset(lambda : args["site_id"])):
        args["site_id"] = None
    # end if
    #// 
    #// Fires when a site's initialization routine should be executed.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $new_site New site object.
    #// @param array   $args     Arguments for the initialization.
    #//
    do_action("wp_initialize_site", new_site, args)
    #// Only compute extra hook parameters if the deprecated hook is actually in use.
    if has_action("wpmu_new_blog"):
        user_id = args["user_id"] if (not php_empty(lambda : args["user_id"])) else 0
        meta = args["options"] if (not php_empty(lambda : args["options"])) else Array()
        #// WPLANG was passed with `$meta` to the `wpmu_new_blog` hook prior to 5.1.0.
        if (not php_array_key_exists("WPLANG", meta)):
            meta["WPLANG"] = get_network_option(new_site.network_id, "WPLANG")
        # end if
        #// Rebuild the data expected by the `wpmu_new_blog` hook prior to 5.1.0 using whitelisted keys.
        #// The `$site_data_whitelist` matches the one used in `wpmu_create_blog()`.
        site_data_whitelist = Array("public", "archived", "mature", "spam", "deleted", "lang_id")
        meta = php_array_merge(php_array_intersect_key(data, php_array_flip(site_data_whitelist)), meta)
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
        do_action_deprecated("wpmu_new_blog", Array(new_site.id, user_id, new_site.domain, new_site.path, new_site.network_id, meta), "5.1.0", "wp_insert_site")
    # end if
    return php_int(new_site.id)
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
def wp_update_site(site_id=None, data=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : site_id):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    old_site = get_site(site_id)
    if (not old_site):
        return php_new_class("WP_Error", lambda : WP_Error("site_not_exist", __("Site does not exist.")))
    # end if
    defaults = old_site.to_array()
    defaults["network_id"] = php_int(defaults["site_id"])
    defaults["last_updated"] = current_time("mysql", True)
    defaults["blog_id"] = None
    defaults["site_id"] = None
    data = wp_prepare_site_data(data, defaults, old_site)
    if is_wp_error(data):
        return data
    # end if
    if False == wpdb.update(wpdb.blogs, data, Array({"blog_id": old_site.id})):
        return php_new_class("WP_Error", lambda : WP_Error("db_update_error", __("Could not update site in the database."), wpdb.last_error))
    # end if
    clean_blog_cache(old_site)
    new_site = get_site(old_site.id)
    #// 
    #// Fires once a site has been updated in the database.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $new_site New site object.
    #// @param WP_Site $old_site Old site object.
    #//
    do_action("wp_update_site", new_site, old_site)
    return php_int(new_site.id)
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
def wp_delete_site(site_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : site_id):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    old_site = get_site(site_id)
    if (not old_site):
        return php_new_class("WP_Error", lambda : WP_Error("site_not_exist", __("Site does not exist.")))
    # end if
    errors = php_new_class("WP_Error", lambda : WP_Error())
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
    do_action("wp_validate_site_deletion", errors, old_site)
    if (not php_empty(lambda : errors.errors)):
        return errors
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
    do_action_deprecated("delete_blog", Array(old_site.id, True), "5.1.0")
    #// 
    #// Fires when a site's uninitialization routine should be executed.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $old_site Deleted site object.
    #//
    do_action("wp_uninitialize_site", old_site)
    if is_site_meta_supported():
        blog_meta_ids = wpdb.get_col(wpdb.prepare(str("SELECT meta_id FROM ") + str(wpdb.blogmeta) + str(" WHERE blog_id = %d "), old_site.id))
        for mid in blog_meta_ids:
            delete_metadata_by_mid("blog", mid)
        # end for
    # end if
    if False == wpdb.delete(wpdb.blogs, Array({"blog_id": old_site.id})):
        return php_new_class("WP_Error", lambda : WP_Error("db_delete_error", __("Could not delete site from the database."), wpdb.last_error))
    # end if
    clean_blog_cache(old_site)
    #// 
    #// Fires once a site has been deleted from the database.
    #// 
    #// @since 5.1.0
    #// 
    #// @param WP_Site $old_site Deleted site object.
    #//
    do_action("wp_delete_site", old_site)
    #// 
    #// Fires after the site is deleted from the network.
    #// 
    #// @since 4.8.0
    #// @deprecated 5.1.0
    #// 
    #// @param int  $site_id The site ID.
    #// @param bool $drop    True if site's tables should be dropped. Default is false.
    #//
    do_action_deprecated("deleted_blog", Array(old_site.id, True), "5.1.0")
    return old_site
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
def get_site(site=None, *args_):
    
    if php_empty(lambda : site):
        site = get_current_blog_id()
    # end if
    if type(site).__name__ == "WP_Site":
        _site = site
    elif php_is_object(site):
        _site = php_new_class("WP_Site", lambda : WP_Site(site))
    else:
        _site = WP_Site.get_instance(site)
    # end if
    if (not _site):
        return None
    # end if
    #// 
    #// Fires after a site is retrieved.
    #// 
    #// @since 4.6.0
    #// 
    #// @param WP_Site $_site Site data.
    #//
    _site = apply_filters("get_site", _site)
    return _site
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
def _prime_site_caches(ids=None, update_meta_cache=True, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    non_cached_ids = _get_non_cached_ids(ids, "sites")
    if (not php_empty(lambda : non_cached_ids)):
        fresh_sites = wpdb.get_results(php_sprintf(str("SELECT * FROM ") + str(wpdb.blogs) + str(" WHERE blog_id IN (%s)"), join(",", php_array_map("intval", non_cached_ids))))
        #// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
        update_site_cache(fresh_sites, update_meta_cache)
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
def update_site_cache(sites=None, update_meta_cache=True, *args_):
    
    if (not sites):
        return
    # end if
    site_ids = Array()
    for site in sites:
        site_ids[-1] = site.blog_id
        wp_cache_add(site.blog_id, site, "sites")
        wp_cache_add(site.blog_id + "short", site, "blog-details")
    # end for
    if update_meta_cache:
        update_sitemeta_cache(site_ids)
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
def update_sitemeta_cache(site_ids=None, *args_):
    
    #// Ensure this filter is hooked in even if the function is called early.
    if (not has_filter("update_blog_metadata_cache", "wp_check_site_meta_support_prefilter")):
        add_filter("update_blog_metadata_cache", "wp_check_site_meta_support_prefilter")
    # end if
    return update_meta_cache("blog", site_ids)
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
def get_sites(args=Array(), *args_):
    
    query = php_new_class("WP_Site_Query", lambda : WP_Site_Query())
    return query.query(args)
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
def wp_prepare_site_data(data=None, defaults=None, old_site=None, *args_):
    
    #// Maintain backward-compatibility with `$site_id` as network ID.
    if (php_isset(lambda : data["site_id"])):
        if (not php_empty(lambda : data["site_id"])) and php_empty(lambda : data["network_id"]):
            data["network_id"] = data["site_id"]
        # end if
        data["site_id"] = None
    # end if
    #// 
    #// Filters passed site data in order to normalize it.
    #// 
    #// @since 5.1.0
    #// 
    #// @param array $data Associative array of site data passed to the respective function.
    #// See {@see wp_insert_site()} for the possibly included data.
    #//
    data = apply_filters("wp_normalize_site_data", data)
    whitelist = Array("domain", "path", "network_id", "registered", "last_updated", "public", "archived", "mature", "spam", "deleted", "lang_id")
    data = php_array_intersect_key(wp_parse_args(data, defaults), php_array_flip(whitelist))
    errors = php_new_class("WP_Error", lambda : WP_Error())
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
    do_action("wp_validate_site_data", errors, data, old_site)
    if (not php_empty(lambda : errors.errors)):
        return errors
    # end if
    #// Prepare for database.
    data["site_id"] = data["network_id"]
    data["network_id"] = None
    return data
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
def wp_normalize_site_data(data=None, *args_):
    
    #// Sanitize domain if passed.
    if php_array_key_exists("domain", data):
        data["domain"] = php_trim(data["domain"])
        data["domain"] = php_preg_replace("/\\s+/", "", sanitize_user(data["domain"], True))
        if is_subdomain_install():
            data["domain"] = php_str_replace("@", "", data["domain"])
        # end if
    # end if
    #// Sanitize path if passed.
    if php_array_key_exists("path", data):
        data["path"] = trailingslashit("/" + php_trim(data["path"], "/"))
    # end if
    #// Sanitize network ID if passed.
    if php_array_key_exists("network_id", data):
        data["network_id"] = php_int(data["network_id"])
    # end if
    #// Sanitize status fields if passed.
    status_fields = Array("public", "archived", "mature", "spam", "deleted")
    for status_field in status_fields:
        if php_array_key_exists(status_field, data):
            data[status_field] = php_int(data[status_field])
        # end if
    # end for
    #// Strip date fields if empty.
    date_fields = Array("registered", "last_updated")
    for date_field in date_fields:
        if (not php_array_key_exists(date_field, data)):
            continue
        # end if
        if php_empty(lambda : data[date_field]) or "0000-00-00 00:00:00" == data[date_field]:
            data[date_field] = None
        # end if
    # end for
    return data
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
def wp_validate_site_data(errors=None, data=None, old_site=None, *args_):
    
    #// A domain must always be present.
    if php_empty(lambda : data["domain"]):
        errors.add("site_empty_domain", __("Site domain must not be empty."))
    # end if
    #// A path must always be present.
    if php_empty(lambda : data["path"]):
        errors.add("site_empty_path", __("Site path must not be empty."))
    # end if
    #// A network ID must always be present.
    if php_empty(lambda : data["network_id"]):
        errors.add("site_empty_network_id", __("Site network ID must be provided."))
    # end if
    #// Both registration and last updated dates must always be present and valid.
    date_fields = Array("registered", "last_updated")
    for date_field in date_fields:
        if php_empty(lambda : data[date_field]):
            errors.add("site_empty_" + date_field, __("Both registration and last updated dates must be provided."))
            break
        # end if
        #// Allow '0000-00-00 00:00:00', although it be stripped out at this point.
        if "0000-00-00 00:00:00" != data[date_field]:
            month = php_substr(data[date_field], 5, 2)
            day = php_substr(data[date_field], 8, 2)
            year = php_substr(data[date_field], 0, 4)
            valid_date = wp_checkdate(month, day, year, data[date_field])
            if (not valid_date):
                errors.add("site_invalid_" + date_field, __("Both registration and last updated dates must be valid dates."))
                break
            # end if
        # end if
    # end for
    if (not php_empty(lambda : errors.errors)):
        return
    # end if
    #// If a new site, or domain/path/network ID have changed, ensure uniqueness.
    if (not old_site) or data["domain"] != old_site.domain or data["path"] != old_site.path or data["network_id"] != old_site.network_id:
        if domain_exists(data["domain"], data["path"], data["network_id"]):
            errors.add("site_taken", __("Sorry, that site already exists!"))
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
def wp_initialize_site(site_id=None, args=Array(), *args_):
    
    global wpdb,wp_roles
    php_check_if_defined("wpdb","wp_roles")
    if php_empty(lambda : site_id):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    site = get_site(site_id)
    if (not site):
        return php_new_class("WP_Error", lambda : WP_Error("site_invalid_id", __("Site with the ID does not exist.")))
    # end if
    if wp_is_site_initialized(site):
        return php_new_class("WP_Error", lambda : WP_Error("site_already_initialized", __("The site appears to be already initialized.")))
    # end if
    network = get_network(site.network_id)
    if (not network):
        network = get_network()
    # end if
    args = wp_parse_args(args, Array({"user_id": 0, "title": php_sprintf(__("Site %d"), site.id), "options": Array(), "meta": Array()}))
    #// 
    #// Filters the arguments for initializing a site.
    #// 
    #// @since 5.1.0
    #// 
    #// @param array      $args    Arguments to modify the initialization behavior.
    #// @param WP_Site    $site    Site that is being initialized.
    #// @param WP_Network $network Network that the site belongs to.
    #//
    args = apply_filters("wp_initialize_site_args", args, site, network)
    orig_installing = wp_installing()
    if (not orig_installing):
        wp_installing(True)
    # end if
    switch = False
    if get_current_blog_id() != site.id:
        switch = True
        switch_to_blog(site.id)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
    #// Set up the database tables.
    make_db_current_silent("blog")
    home_scheme = "http"
    siteurl_scheme = "http"
    if (not is_subdomain_install()):
        if "https" == php_parse_url(get_home_url(network.site_id), PHP_URL_SCHEME):
            home_scheme = "https"
        # end if
        if "https" == php_parse_url(get_network_option(network.id, "siteurl"), PHP_URL_SCHEME):
            siteurl_scheme = "https"
        # end if
    # end if
    #// Populate the site's options.
    populate_options(php_array_merge(Array({"home": untrailingslashit(home_scheme + "://" + site.domain + site.path), "siteurl": untrailingslashit(siteurl_scheme + "://" + site.domain + site.path), "blogname": wp_unslash(args["title"]), "admin_email": "", "upload_path": UPLOADBLOGSDIR + str("/") + str(site.id) + str("/files") if get_network_option(network.id, "ms_files_rewriting") else get_blog_option(network.site_id, "upload_path"), "blog_public": php_int(site.public), "WPLANG": get_network_option(network.id, "WPLANG")}), args["options"]))
    #// Clean blog cache after populating options.
    clean_blog_cache(site)
    #// Populate the site's roles.
    populate_roles()
    wp_roles = php_new_class("WP_Roles", lambda : WP_Roles())
    #// Populate metadata for the site.
    populate_site_meta(site.id, args["meta"])
    #// Remove all permissions that may exist for the site.
    table_prefix = wpdb.get_blog_prefix()
    delete_metadata("user", 0, table_prefix + "user_level", None, True)
    #// Delete all.
    delete_metadata("user", 0, table_prefix + "capabilities", None, True)
    #// Delete all.
    #// Install default site content.
    wp_install_defaults(args["user_id"])
    #// Set the site administrator.
    add_user_to_blog(site.id, args["user_id"], "administrator")
    if (not user_can(args["user_id"], "manage_network")) and (not get_user_meta(args["user_id"], "primary_blog", True)):
        update_user_meta(args["user_id"], "primary_blog", site.id)
    # end if
    if switch:
        restore_current_blog()
    # end if
    wp_installing(orig_installing)
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
def wp_uninitialize_site(site_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : site_id):
        return php_new_class("WP_Error", lambda : WP_Error("site_empty_id", __("Site ID must not be empty.")))
    # end if
    site = get_site(site_id)
    if (not site):
        return php_new_class("WP_Error", lambda : WP_Error("site_invalid_id", __("Site with the ID does not exist.")))
    # end if
    if (not wp_is_site_initialized(site)):
        return php_new_class("WP_Error", lambda : WP_Error("site_already_uninitialized", __("The site appears to be already uninitialized.")))
    # end if
    users = get_users(Array({"blog_id": site.id, "fields": "ids"}))
    #// Remove users from the site.
    if (not php_empty(lambda : users)):
        for user_id in users:
            remove_user_from_blog(user_id, site.id)
        # end for
    # end if
    switch = False
    if get_current_blog_id() != site.id:
        switch = True
        switch_to_blog(site.id)
    # end if
    uploads = wp_get_upload_dir()
    tables = wpdb.tables("blog")
    #// 
    #// Filters the tables to drop when the site is deleted.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string[] $tables  Array of names of the site tables to be dropped.
    #// @param int      $site_id The ID of the site to drop tables for.
    #//
    drop_tables = apply_filters("wpmu_drop_tables", tables, site.id)
    for table in drop_tables:
        wpdb.query(str("DROP TABLE IF EXISTS `") + str(table) + str("`"))
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
    dir = apply_filters("wpmu_delete_blog_upload_dir", uploads["basedir"], site.id)
    dir = php_rtrim(dir, DIRECTORY_SEPARATOR)
    top_dir = dir
    stack = Array(dir)
    index = 0
    while True:
        
        if not (index < php_count(stack)):
            break
        # end if
        #// Get indexed directory from stack.
        dir = stack[index]
        #// phpcs:disable WordPress.PHP.NoSilencedErrors.Discouraged
        dh = php_no_error(lambda: php_opendir(dir))
        if dh:
            file = php_no_error(lambda: php_readdir(dh))
            while True:
                
                if not (False != file):
                    break
                # end if
                if "." == file or ".." == file:
                    file = php_no_error(lambda: php_readdir(dh))
                    continue
                # end if
                if php_no_error(lambda: php_is_dir(dir + DIRECTORY_SEPARATOR + file)):
                    stack[-1] = dir + DIRECTORY_SEPARATOR + file
                elif php_no_error(lambda: php_is_file(dir + DIRECTORY_SEPARATOR + file)):
                    php_no_error(lambda: unlink(dir + DIRECTORY_SEPARATOR + file))
                # end if
                file = php_no_error(lambda: php_readdir(dh))
            # end while
            php_no_error(lambda: php_closedir(dh))
        # end if
        index += 1
    # end while
    stack = array_reverse(stack)
    #// Last added directories are deepest.
    for dir in stack:
        if dir != top_dir:
            php_no_error(lambda: rmdir(dir))
        # end if
    # end for
    #// phpcs:enable WordPress.PHP.NoSilencedErrors.Discouraged
    if switch:
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
def wp_is_site_initialized(site_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_is_object(site_id):
        site_id = site_id.blog_id
    # end if
    site_id = php_int(site_id)
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
    pre = apply_filters("pre_wp_is_site_initialized", None, site_id)
    if None != pre:
        return php_bool(pre)
    # end if
    switch = False
    if get_current_blog_id() != site_id:
        switch = True
        remove_action("switch_blog", "wp_switch_roles_and_user", 1)
        switch_to_blog(site_id)
    # end if
    suppress = wpdb.suppress_errors()
    result = php_bool(wpdb.get_results(str("DESCRIBE ") + str(wpdb.posts)))
    wpdb.suppress_errors(suppress)
    if switch:
        restore_current_blog()
        add_action("switch_blog", "wp_switch_roles_and_user", 1, 2)
    # end if
    return result
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
def clean_blog_cache(blog=None, *args_):
    
    global _wp_suspend_cache_invalidation
    php_check_if_defined("_wp_suspend_cache_invalidation")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation)):
        return
    # end if
    if php_empty(lambda : blog):
        return
    # end if
    blog_id = blog
    blog = get_site(blog_id)
    if (not blog):
        if (not php_is_numeric(blog_id)):
            return
        # end if
        #// Make sure a WP_Site object exists even when the site has been deleted.
        blog = php_new_class("WP_Site", lambda : WP_Site(Array({"blog_id": blog_id, "domain": None, "path": None})))
    # end if
    blog_id = blog.blog_id
    domain_path_key = php_md5(blog.domain + blog.path)
    wp_cache_delete(blog_id, "sites")
    wp_cache_delete(blog_id, "site-details")
    wp_cache_delete(blog_id, "blog-details")
    wp_cache_delete(blog_id + "short", "blog-details")
    wp_cache_delete(domain_path_key, "blog-lookup")
    wp_cache_delete(domain_path_key, "blog-id-cache")
    wp_cache_delete(blog_id, "blog_meta")
    #// 
    #// Fires immediately after a site has been removed from the object cache.
    #// 
    #// @since 4.6.0
    #// 
    #// @param int     $id              Blog ID.
    #// @param WP_Site $blog            Site object.
    #// @param string  $domain_path_key md5 hash of domain and path.
    #//
    do_action("clean_site_cache", blog_id, blog, domain_path_key)
    wp_cache_set("last_changed", php_microtime(), "sites")
    #// 
    #// Fires after the blog details cache is cleared.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.9.0 Use {@see 'clean_site_cache'} instead.
    #// 
    #// @param int $blog_id Blog ID.
    #//
    do_action_deprecated("refresh_blog_details", Array(blog_id), "4.9.0", "clean_site_cache")
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
def add_site_meta(site_id=None, meta_key=None, meta_value=None, unique=False, *args_):
    
    return add_metadata("blog", site_id, meta_key, meta_value, unique)
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
def delete_site_meta(site_id=None, meta_key=None, meta_value="", *args_):
    
    return delete_metadata("blog", site_id, meta_key, meta_value)
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
def get_site_meta(site_id=None, key="", single=False, *args_):
    
    return get_metadata("blog", site_id, key, single)
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
def update_site_meta(site_id=None, meta_key=None, meta_value=None, prev_value="", *args_):
    
    return update_metadata("blog", site_id, meta_key, meta_value, prev_value)
# end def update_site_meta
#// 
#// Deletes everything from site meta matching meta key.
#// 
#// @since 5.1.0
#// 
#// @param string $meta_key Metadata key to search for when deleting.
#// @return bool Whether the site meta key was deleted from the database.
#//
def delete_site_meta_by_key(meta_key=None, *args_):
    
    return delete_metadata("blog", None, meta_key, "", True)
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
def wp_maybe_update_network_site_counts_on_update(new_site=None, old_site=None, *args_):
    
    if None == old_site:
        wp_maybe_update_network_site_counts(new_site.network_id)
        return
    # end if
    if new_site.network_id != old_site.network_id:
        wp_maybe_update_network_site_counts(new_site.network_id)
        wp_maybe_update_network_site_counts(old_site.network_id)
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
def wp_maybe_transition_site_statuses_on_update(new_site=None, old_site=None, *args_):
    
    site_id = new_site.id
    #// Use the default values for a site if no previous state is given.
    if (not old_site):
        old_site = php_new_class("WP_Site", lambda : WP_Site(php_new_class("stdClass", lambda : stdClass())))
    # end if
    if new_site.spam != old_site.spam:
        if 1 == new_site.spam:
            #// 
            #// Fires when the 'spam' status is added to a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_spam_blog", site_id)
        else:
            #// 
            #// Fires when the 'spam' status is removed from a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_ham_blog", site_id)
        # end if
    # end if
    if new_site.mature != old_site.mature:
        if 1 == new_site.mature:
            #// 
            #// Fires when the 'mature' status is added to a site.
            #// 
            #// @since 3.1.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("mature_blog", site_id)
        else:
            #// 
            #// Fires when the 'mature' status is removed from a site.
            #// 
            #// @since 3.1.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("unmature_blog", site_id)
        # end if
    # end if
    if new_site.archived != old_site.archived:
        if 1 == new_site.archived:
            #// 
            #// Fires when the 'archived' status is added to a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("archive_blog", site_id)
        else:
            #// 
            #// Fires when the 'archived' status is removed from a site.
            #// 
            #// @since MU (3.0.0)
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("unarchive_blog", site_id)
        # end if
    # end if
    if new_site.deleted != old_site.deleted:
        if 1 == new_site.deleted:
            #// 
            #// Fires when the 'deleted' status is added to a site.
            #// 
            #// @since 3.5.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_delete_blog", site_id)
        else:
            #// 
            #// Fires when the 'deleted' status is removed from a site.
            #// 
            #// @since 3.5.0
            #// 
            #// @param int $site_id Site ID.
            #//
            do_action("make_undelete_blog", site_id)
        # end if
    # end if
    if new_site.public != old_site.public:
        #// 
        #// Fires after the current blog's 'public' setting is updated.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param int    $site_id Site ID.
        #// @param string $value   The value of the site status.
        #//
        do_action("update_blog_public", site_id, new_site.public)
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
def wp_maybe_clean_new_site_cache_on_update(new_site=None, old_site=None, *args_):
    
    if old_site.domain != new_site.domain or old_site.path != new_site.path:
        clean_blog_cache(new_site)
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
def wp_update_blog_public_option_on_site_update(site_id=None, public=None, *args_):
    
    #// Bail if the site's database tables do not exist (yet).
    if (not wp_is_site_initialized(site_id)):
        return
    # end if
    update_blog_option(site_id, "blog_public", public)
# end def wp_update_blog_public_option_on_site_update
#// 
#// Sets the last changed time for the 'sites' cache group.
#// 
#// @since 5.1.0
#//
def wp_cache_set_sites_last_changed(*args_):
    
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
def wp_check_site_meta_support_prefilter(check=None, *args_):
    
    if (not is_site_meta_supported()):
        #// translators: %s: Database table name.
        _doing_it_wrong(__FUNCTION__, php_sprintf(__("The %s table is not installed. Please run the network database upgrade."), PHP_GLOBALS["wpdb"].blogmeta), "5.1.0")
        return False
    # end if
    return check
# end def wp_check_site_meta_support_prefilter
