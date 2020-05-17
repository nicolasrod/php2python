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
#// Site/blog functions that work with the blogs table and related data.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since MU (3.0.0)
#//
php_include_file(ABSPATH + WPINC + "/ms-site.php", once=True)
php_include_file(ABSPATH + WPINC + "/ms-network.php", once=True)
#// 
#// Update the last_updated field for the current site.
#// 
#// @since MU (3.0.0)
#//
def wpmu_update_blogs_date(*_args_):
    
    
    site_id_ = get_current_blog_id()
    update_blog_details(site_id_, Array({"last_updated": current_time("mysql", True)}))
    #// 
    #// Fires after the blog details are updated.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int $blog_id Site ID.
    #//
    do_action("wpmu_blog_updated", site_id_)
# end def wpmu_update_blogs_date
#// 
#// Get a full blog URL, given a blog id.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $blog_id Blog ID.
#// @return string Full URL of the blog if found. Empty string if not.
#//
def get_blogaddress_by_id(blog_id_=None, *_args_):
    
    
    bloginfo_ = get_site(php_int(blog_id_))
    if php_empty(lambda : bloginfo_):
        return ""
    # end if
    scheme_ = php_parse_url(bloginfo_.home, PHP_URL_SCHEME)
    scheme_ = "http" if php_empty(lambda : scheme_) else scheme_
    return esc_url(scheme_ + "://" + bloginfo_.domain + bloginfo_.path)
# end def get_blogaddress_by_id
#// 
#// Get a full blog URL, given a blog name.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $blogname The (subdomain or directory) name
#// @return string
#//
def get_blogaddress_by_name(blogname_=None, *_args_):
    
    
    if is_subdomain_install():
        if "main" == blogname_:
            blogname_ = "www"
        # end if
        url_ = php_rtrim(network_home_url(), "/")
        if (not php_empty(lambda : blogname_)):
            url_ = php_preg_replace("|^([^\\.]+://)|", "${1}" + blogname_ + ".", url_)
        # end if
    else:
        url_ = network_home_url(blogname_)
    # end if
    return esc_url(url_ + "/")
# end def get_blogaddress_by_name
#// 
#// Retrieves a sites ID given its (subdomain or directory) slug.
#// 
#// @since MU (3.0.0)
#// @since 4.7.0 Converted to use `get_sites()`.
#// 
#// @param string $slug A site's slug.
#// @return int|null The site ID, or null if no site is found for the given slug.
#//
def get_id_from_blogname(slug_=None, *_args_):
    
    
    current_network_ = get_network()
    slug_ = php_trim(slug_, "/")
    if is_subdomain_install():
        domain_ = slug_ + "." + php_preg_replace("|^www\\.|", "", current_network_.domain)
        path_ = current_network_.path
    else:
        domain_ = current_network_.domain
        path_ = current_network_.path + slug_ + "/"
    # end if
    site_ids_ = get_sites(Array({"number": 1, "fields": "ids", "domain": domain_, "path": path_, "update_site_meta_cache": False}))
    if php_empty(lambda : site_ids_):
        return None
    # end if
    return php_array_shift(site_ids_)
# end def get_id_from_blogname
#// 
#// Retrieve the details for a blog from the blogs table and blog options.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|string|array $fields  Optional. A blog ID, a blog slug, or an array of fields to query against.
#// If not specified the current blog ID is used.
#// @param bool             $get_all Whether to retrieve all details or only the details in the blogs table.
#// Default is true.
#// @return WP_Site|false Blog details on success. False on failure.
#//
def get_blog_details(fields_=None, get_all_=None, *_args_):
    if get_all_ is None:
        get_all_ = True
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_is_array(fields_):
        if (php_isset(lambda : fields_["blog_id"])):
            blog_id_ = fields_["blog_id"]
        elif (php_isset(lambda : fields_["domain"])) and (php_isset(lambda : fields_["path"])):
            key_ = php_md5(fields_["domain"] + fields_["path"])
            blog_ = wp_cache_get(key_, "blog-lookup")
            if False != blog_:
                return blog_
            # end if
            if php_substr(fields_["domain"], 0, 4) == "www.":
                nowww_ = php_substr(fields_["domain"], 4)
                blog_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.blogs) + str(" WHERE domain IN (%s,%s) AND path = %s ORDER BY CHAR_LENGTH(domain) DESC"), nowww_, fields_["domain"], fields_["path"]))
            else:
                blog_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.blogs) + str(" WHERE domain = %s AND path = %s"), fields_["domain"], fields_["path"]))
            # end if
            if blog_:
                wp_cache_set(blog_.blog_id + "short", blog_, "blog-details")
                blog_id_ = blog_.blog_id
            else:
                return False
            # end if
        elif (php_isset(lambda : fields_["domain"])) and is_subdomain_install():
            key_ = php_md5(fields_["domain"])
            blog_ = wp_cache_get(key_, "blog-lookup")
            if False != blog_:
                return blog_
            # end if
            if php_substr(fields_["domain"], 0, 4) == "www.":
                nowww_ = php_substr(fields_["domain"], 4)
                blog_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.blogs) + str(" WHERE domain IN (%s,%s) ORDER BY CHAR_LENGTH(domain) DESC"), nowww_, fields_["domain"]))
            else:
                blog_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.blogs) + str(" WHERE domain = %s"), fields_["domain"]))
            # end if
            if blog_:
                wp_cache_set(blog_.blog_id + "short", blog_, "blog-details")
                blog_id_ = blog_.blog_id
            else:
                return False
            # end if
        else:
            return False
        # end if
    else:
        if (not fields_):
            blog_id_ = get_current_blog_id()
        elif (not php_is_numeric(fields_)):
            blog_id_ = get_id_from_blogname(fields_)
        else:
            blog_id_ = fields_
        # end if
    # end if
    blog_id_ = php_int(blog_id_)
    all_ = "" if get_all_ else "short"
    details_ = wp_cache_get(blog_id_ + all_, "blog-details")
    if details_:
        if (not php_is_object(details_)):
            if -1 == details_:
                return False
            else:
                #// Clear old pre-serialized objects. Cache clients do better with that.
                wp_cache_delete(blog_id_ + all_, "blog-details")
                details_ = None
            # end if
        else:
            return details_
        # end if
    # end if
    #// Try the other cache.
    if get_all_:
        details_ = wp_cache_get(blog_id_ + "short", "blog-details")
    else:
        details_ = wp_cache_get(blog_id_, "blog-details")
        #// If short was requested and full cache is set, we can return.
        if details_:
            if (not php_is_object(details_)):
                if -1 == details_:
                    return False
                else:
                    #// Clear old pre-serialized objects. Cache clients do better with that.
                    wp_cache_delete(blog_id_, "blog-details")
                    details_ = None
                # end if
            else:
                return details_
            # end if
        # end if
    # end if
    if php_empty(lambda : details_):
        details_ = WP_Site.get_instance(blog_id_)
        if (not details_):
            #// Set the full cache.
            wp_cache_set(blog_id_, -1, "blog-details")
            return False
        # end if
    # end if
    if (not type(details_).__name__ == "WP_Site"):
        details_ = php_new_class("WP_Site", lambda : WP_Site(details_))
    # end if
    if (not get_all_):
        wp_cache_set(blog_id_ + all_, details_, "blog-details")
        return details_
    # end if
    switch_to_blog(blog_id_)
    details_.blogname = get_option("blogname")
    details_.siteurl = get_option("siteurl")
    details_.post_count = get_option("post_count")
    details_.home = get_option("home")
    restore_current_blog()
    #// 
    #// Filters a blog's details.
    #// 
    #// @since MU (3.0.0)
    #// @deprecated 4.7.0 Use {@see 'site_details'} instead.
    #// 
    #// @param object $details The blog details.
    #//
    details_ = apply_filters_deprecated("blog_details", Array(details_), "4.7.0", "site_details")
    wp_cache_set(blog_id_ + all_, details_, "blog-details")
    key_ = php_md5(details_.domain + details_.path)
    wp_cache_set(key_, details_, "blog-lookup")
    return details_
# end def get_blog_details
#// 
#// Clear the blog details cache.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $blog_id Optional. Blog ID. Defaults to current blog.
#//
def refresh_blog_details(blog_id_=0, *_args_):
    
    
    blog_id_ = php_int(blog_id_)
    if (not blog_id_):
        blog_id_ = get_current_blog_id()
    # end if
    clean_blog_cache(blog_id_)
# end def refresh_blog_details
#// 
#// Update the details for a blog. Updates the blogs table for a given blog id.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int   $blog_id Blog ID.
#// @param array $details Array of details keyed by blogs table field names.
#// @return bool True if update succeeds, false otherwise.
#//
def update_blog_details(blog_id_=None, details_=None, *_args_):
    if details_ is None:
        details_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : details_):
        return False
    # end if
    if php_is_object(details_):
        details_ = get_object_vars(details_)
    # end if
    site_ = wp_update_site(blog_id_, details_)
    if is_wp_error(site_):
        return False
    # end if
    return True
# end def update_blog_details
#// 
#// Cleans the site details cache for a site.
#// 
#// @since 4.7.4
#// 
#// @param int $site_id Optional. Site ID. Default is the current site ID.
#//
def clean_site_details_cache(site_id_=0, *_args_):
    
    
    site_id_ = php_int(site_id_)
    if (not site_id_):
        site_id_ = get_current_blog_id()
    # end if
    wp_cache_delete(site_id_, "site-details")
    wp_cache_delete(site_id_, "blog-details")
# end def clean_site_details_cache
#// 
#// Retrieve option value for a given blog id based on name of option.
#// 
#// If the option does not exist or does not have a value, then the return value
#// will be false. This is useful to check whether you need to install an option
#// and is commonly used during installation of plugin options and to test
#// whether upgrading is required.
#// 
#// If the option was serialized then it will be unserialized when it is returned.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $id      A blog ID. Can be null to refer to the current blog.
#// @param string $option  Name of option to retrieve. Expected to not be SQL-escaped.
#// @param mixed  $default Optional. Default value to return if the option does not exist.
#// @return mixed Value set for the option.
#//
def get_blog_option(id_=None, option_=None, default_=None, *_args_):
    if default_ is None:
        default_ = False
    # end if
    
    id_ = php_int(id_)
    if php_empty(lambda : id_):
        id_ = get_current_blog_id()
    # end if
    if get_current_blog_id() == id_:
        return get_option(option_, default_)
    # end if
    switch_to_blog(id_)
    value_ = get_option(option_, default_)
    restore_current_blog()
    #// 
    #// Filters a blog option value.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the blog option name.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string  $value The option value.
    #// @param int     $id    Blog ID.
    #//
    return apply_filters(str("blog_option_") + str(option_), value_, id_)
# end def get_blog_option
#// 
#// Add a new option for a given blog id.
#// 
#// You do not need to serialize values. If the value needs to be serialized, then
#// it will be serialized before it is inserted into the database. Remember,
#// resources can not be serialized or added as an option.
#// 
#// You can create options without values and then update the values later.
#// Existing options will not be updated and checks are performed to ensure that you
#// aren't adding a protected WordPress option. Care should be taken to not name
#// options the same as the ones which are protected.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $id     A blog ID. Can be null to refer to the current blog.
#// @param string $option Name of option to add. Expected to not be SQL-escaped.
#// @param mixed  $value  Optional. Option value, can be anything. Expected to not be SQL-escaped.
#// @return bool False if option was not added and true if option was added.
#//
def add_blog_option(id_=None, option_=None, value_=None, *_args_):
    
    
    id_ = php_int(id_)
    if php_empty(lambda : id_):
        id_ = get_current_blog_id()
    # end if
    if get_current_blog_id() == id_:
        return add_option(option_, value_)
    # end if
    switch_to_blog(id_)
    return_ = add_option(option_, value_)
    restore_current_blog()
    return return_
# end def add_blog_option
#// 
#// Removes option by name for a given blog id. Prevents removal of protected WordPress options.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $id     A blog ID. Can be null to refer to the current blog.
#// @param string $option Name of option to remove. Expected to not be SQL-escaped.
#// @return bool True, if option is successfully deleted. False on failure.
#//
def delete_blog_option(id_=None, option_=None, *_args_):
    
    
    id_ = php_int(id_)
    if php_empty(lambda : id_):
        id_ = get_current_blog_id()
    # end if
    if get_current_blog_id() == id_:
        return delete_option(option_)
    # end if
    switch_to_blog(id_)
    return_ = delete_option(option_)
    restore_current_blog()
    return return_
# end def delete_blog_option
#// 
#// Update an option for a particular blog.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $id         The blog id.
#// @param string $option     The option key.
#// @param mixed  $value      The option value.
#// @param mixed  $deprecated Not used.
#// @return bool True on success, false on failure.
#//
def update_blog_option(id_=None, option_=None, value_=None, deprecated_=None, *_args_):
    
    
    id_ = php_int(id_)
    if None != deprecated_:
        _deprecated_argument(__FUNCTION__, "3.1.0")
    # end if
    if get_current_blog_id() == id_:
        return update_option(option_, value_)
    # end if
    switch_to_blog(id_)
    return_ = update_option(option_, value_)
    restore_current_blog()
    return return_
# end def update_blog_option
#// 
#// Switch the current blog.
#// 
#// This function is useful if you need to pull posts, or other information,
#// from other blogs. You can switch back afterwards using restore_current_blog().
#// 
#// Things that aren't switched:
#// - plugins. See #14941
#// 
#// @see restore_current_blog()
#// @since MU (3.0.0)
#// 
#// @global wpdb            $wpdb               WordPress database abstraction object.
#// @global int             $blog_id
#// @global array           $_wp_switched_stack
#// @global bool            $switched
#// @global string          $table_prefix
#// @global WP_Object_Cache $wp_object_cache
#// 
#// @param int  $new_blog_id The ID of the blog to switch to. Default: current blog.
#// @param bool $deprecated  Not used.
#// @return true Always returns true.
#//
def switch_to_blog(new_blog_id_=None, deprecated_=None, *_args_):
    
    global PHP_GLOBALS
    global wpdb_
    php_check_if_defined("wpdb_")
    prev_blog_id_ = get_current_blog_id()
    if php_empty(lambda : new_blog_id_):
        new_blog_id_ = prev_blog_id_
    # end if
    PHP_GLOBALS["_wp_switched_stack"][-1] = prev_blog_id_
    #// 
    #// If we're switching to the same blog id that we're on,
    #// set the right vars, do the associated actions, but skip
    #// the extra unnecessary work
    #//
    if new_blog_id_ == prev_blog_id_:
        #// 
        #// Fires when the blog is switched.
        #// 
        #// @since MU (3.0.0)
        #// @since 5.4.0 The `$context` parameter was added.
        #// 
        #// @param int    $new_blog_id  New blog ID.
        #// @param int    $prev_blog_id Previous blog ID.
        #// @param string $context      Additional context. Accepts 'switch' when called from switch_to_blog()
        #// or 'restore' when called from restore_current_blog().
        #//
        do_action("switch_blog", new_blog_id_, prev_blog_id_, "switch")
        PHP_GLOBALS["switched"] = True
        return True
    # end if
    wpdb_.set_blog_id(new_blog_id_)
    PHP_GLOBALS["table_prefix"] = wpdb_.get_blog_prefix()
    PHP_GLOBALS["blog_id"] = new_blog_id_
    if php_function_exists("wp_cache_switch_to_blog"):
        wp_cache_switch_to_blog(new_blog_id_)
    else:
        global wp_object_cache_
        php_check_if_defined("wp_object_cache_")
        if php_is_object(wp_object_cache_) and (php_isset(lambda : wp_object_cache_.global_groups)):
            global_groups_ = wp_object_cache_.global_groups
        else:
            global_groups_ = False
        # end if
        wp_cache_init()
        if php_function_exists("wp_cache_add_global_groups"):
            if php_is_array(global_groups_):
                wp_cache_add_global_groups(global_groups_)
            else:
                wp_cache_add_global_groups(Array("users", "userlogins", "usermeta", "user_meta", "useremail", "userslugs", "site-transient", "site-options", "blog-lookup", "blog-details", "rss", "global-posts", "blog-id-cache", "networks", "sites", "site-details", "blog_meta"))
            # end if
            wp_cache_add_non_persistent_groups(Array("counts", "plugins"))
        # end if
    # end if
    #// This filter is documented in wp-includes/ms-blogs.php
    do_action("switch_blog", new_blog_id_, prev_blog_id_, "switch")
    PHP_GLOBALS["switched"] = True
    return True
# end def switch_to_blog
#// 
#// Restore the current blog, after calling switch_to_blog().
#// 
#// @see switch_to_blog()
#// @since MU (3.0.0)
#// 
#// @global wpdb            $wpdb               WordPress database abstraction object.
#// @global array           $_wp_switched_stack
#// @global int             $blog_id
#// @global bool            $switched
#// @global string          $table_prefix
#// @global WP_Object_Cache $wp_object_cache
#// 
#// @return bool True on success, false if we're already on the current blog.
#//
def restore_current_blog(*_args_):
    
    global PHP_GLOBALS
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : PHP_GLOBALS["_wp_switched_stack"]):
        return False
    # end if
    new_blog_id_ = php_array_pop(PHP_GLOBALS["_wp_switched_stack"])
    prev_blog_id_ = get_current_blog_id()
    if new_blog_id_ == prev_blog_id_:
        #// This filter is documented in wp-includes/ms-blogs.php
        do_action("switch_blog", new_blog_id_, prev_blog_id_, "restore")
        #// If we still have items in the switched stack, consider ourselves still 'switched'.
        PHP_GLOBALS["switched"] = (not php_empty(lambda : PHP_GLOBALS["_wp_switched_stack"]))
        return True
    # end if
    wpdb_.set_blog_id(new_blog_id_)
    PHP_GLOBALS["blog_id"] = new_blog_id_
    PHP_GLOBALS["table_prefix"] = wpdb_.get_blog_prefix()
    if php_function_exists("wp_cache_switch_to_blog"):
        wp_cache_switch_to_blog(new_blog_id_)
    else:
        global wp_object_cache_
        php_check_if_defined("wp_object_cache_")
        if php_is_object(wp_object_cache_) and (php_isset(lambda : wp_object_cache_.global_groups)):
            global_groups_ = wp_object_cache_.global_groups
        else:
            global_groups_ = False
        # end if
        wp_cache_init()
        if php_function_exists("wp_cache_add_global_groups"):
            if php_is_array(global_groups_):
                wp_cache_add_global_groups(global_groups_)
            else:
                wp_cache_add_global_groups(Array("users", "userlogins", "usermeta", "user_meta", "useremail", "userslugs", "site-transient", "site-options", "blog-lookup", "blog-details", "rss", "global-posts", "blog-id-cache", "networks", "sites", "site-details", "blog_meta"))
            # end if
            wp_cache_add_non_persistent_groups(Array("counts", "plugins"))
        # end if
    # end if
    #// This filter is documented in wp-includes/ms-blogs.php
    do_action("switch_blog", new_blog_id_, prev_blog_id_, "restore")
    #// If we still have items in the switched stack, consider ourselves still 'switched'.
    PHP_GLOBALS["switched"] = (not php_empty(lambda : PHP_GLOBALS["_wp_switched_stack"]))
    return True
# end def restore_current_blog
#// 
#// Switches the initialized roles and current user capabilities to another site.
#// 
#// @since 4.9.0
#// 
#// @param int $new_site_id New site ID.
#// @param int $old_site_id Old site ID.
#//
def wp_switch_roles_and_user(new_site_id_=None, old_site_id_=None, *_args_):
    
    
    if new_site_id_ == old_site_id_:
        return
    # end if
    if (not did_action("init")):
        return
    # end if
    wp_roles().for_site(new_site_id_)
    wp_get_current_user().for_site(new_site_id_)
# end def wp_switch_roles_and_user
#// 
#// Determines if switch_to_blog() is in effect
#// 
#// @since 3.5.0
#// 
#// @global array $_wp_switched_stack
#// 
#// @return bool True if switched, false otherwise.
#//
def ms_is_switched(*_args_):
    
    
    return (not php_empty(lambda : PHP_GLOBALS["_wp_switched_stack"]))
# end def ms_is_switched
#// 
#// Check if a particular blog is archived.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $id Blog ID.
#// @return string Whether the blog is archived or not.
#//
def is_archived(id_=None, *_args_):
    
    
    return get_blog_status(id_, "archived")
# end def is_archived
#// 
#// Update the 'archived' status of a particular blog.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $id       Blog ID.
#// @param string $archived The new status.
#// @return string $archived
#//
def update_archived(id_=None, archived_=None, *_args_):
    
    
    update_blog_status(id_, "archived", archived_)
    return archived_
# end def update_archived
#// 
#// Update a blog details field.
#// 
#// @since MU (3.0.0)
#// @since 5.1.0 Use wp_update_site() internally.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $blog_id    Blog ID.
#// @param string $pref       Field name.
#// @param string $value      Field value.
#// @param null   $deprecated Not used.
#// @return string|false $value
#//
def update_blog_status(blog_id_=None, pref_=None, value_=None, deprecated_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if None != deprecated_:
        _deprecated_argument(__FUNCTION__, "3.1.0")
    # end if
    if (not php_in_array(pref_, Array("site_id", "domain", "path", "registered", "last_updated", "public", "archived", "mature", "spam", "deleted", "lang_id"))):
        return value_
    # end if
    result_ = wp_update_site(blog_id_, Array({pref_: value_}))
    if is_wp_error(result_):
        return False
    # end if
    return value_
# end def update_blog_status
#// 
#// Get a blog details field.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $id   Blog ID.
#// @param string $pref Field name.
#// @return bool|string|null $value
#//
def get_blog_status(id_=None, pref_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    details_ = get_site(id_)
    if details_:
        return details_.pref_
    # end if
    return wpdb_.get_var(wpdb_.prepare(str("SELECT %s FROM ") + str(wpdb_.blogs) + str(" WHERE blog_id = %d"), pref_, id_))
# end def get_blog_status
#// 
#// Get a list of most recently updated blogs.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param mixed $deprecated Not used.
#// @param int   $start      Optional. Number of blogs to offset the query. Used to build LIMIT clause.
#// Can be used for pagination. Default 0.
#// @param int   $quantity   Optional. The maximum number of blogs to retrieve. Default 40.
#// @return array The list of blogs.
#//
def get_last_updated(deprecated_="", start_=0, quantity_=40, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(__FUNCTION__, "MU")
        pass
    # end if
    return wpdb_.get_results(wpdb_.prepare(str("SELECT blog_id, domain, path FROM ") + str(wpdb_.blogs) + str(" WHERE site_id = %d AND public = '1' AND archived = '0' AND mature = '0' AND spam = '0' AND deleted = '0' AND last_updated != '0000-00-00 00:00:00' ORDER BY last_updated DESC limit %d, %d"), get_current_network_id(), start_, quantity_), ARRAY_A)
# end def get_last_updated
#// 
#// Handler for updating the site's last updated date when a post is published or
#// an already published post is changed.
#// 
#// @since 3.3.0
#// 
#// @param string  $new_status The new post status.
#// @param string  $old_status The old post status.
#// @param WP_Post $post       Post object.
#//
def _update_blog_date_on_post_publish(new_status_=None, old_status_=None, post_=None, *_args_):
    
    
    post_type_obj_ = get_post_type_object(post_.post_type)
    if (not post_type_obj_) or (not post_type_obj_.public):
        return
    # end if
    if "publish" != new_status_ and "publish" != old_status_:
        return
    # end if
    #// Post was freshly published, published post was saved, or published post was unpublished.
    wpmu_update_blogs_date()
# end def _update_blog_date_on_post_publish
#// 
#// Handler for updating the current site's last updated date when a published
#// post is deleted.
#// 
#// @since 3.4.0
#// 
#// @param int $post_id Post ID
#//
def _update_blog_date_on_post_delete(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    post_type_obj_ = get_post_type_object(post_.post_type)
    if (not post_type_obj_) or (not post_type_obj_.public):
        return
    # end if
    if "publish" != post_.post_status:
        return
    # end if
    wpmu_update_blogs_date()
# end def _update_blog_date_on_post_delete
#// 
#// Handler for updating the current site's posts count when a post is deleted.
#// 
#// @since 4.0.0
#// 
#// @param int $post_id Post ID.
#//
def _update_posts_count_on_delete(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_) or "publish" != post_.post_status or "post" != post_.post_type:
        return
    # end if
    update_posts_count()
# end def _update_posts_count_on_delete
#// 
#// Handler for updating the current site's posts count when a post status changes.
#// 
#// @since 4.0.0
#// @since 4.9.0 Added the `$post` parameter.
#// 
#// @param string  $new_status The status the post is changing to.
#// @param string  $old_status The status the post is changing from.
#// @param WP_Post $post       Post object
#//
def _update_posts_count_on_transition_post_status(new_status_=None, old_status_=None, post_=None, *_args_):
    
    
    if new_status_ == old_status_:
        return
    # end if
    if "post" != get_post_type(post_):
        return
    # end if
    if "publish" != new_status_ and "publish" != old_status_:
        return
    # end if
    update_posts_count()
# end def _update_posts_count_on_transition_post_status
#// 
#// Count number of sites grouped by site status.
#// 
#// @since 5.3.0
#// 
#// @param int $network_id Optional. The network to get counts for. Default is the current network ID.
#// @return int[] {
#// Numbers of sites grouped by site status.
#// 
#// @type int $all      The total number of sites.
#// @type int $public   The number of public sites.
#// @type int $archived The number of archived sites.
#// @type int $mature   The number of mature sites.
#// @type int $spam     The number of spam sites.
#// @type int $deleted  The number of deleted sites.
#// }
#//
def wp_count_sites(network_id_=None, *_args_):
    
    
    if php_empty(lambda : network_id_):
        network_id_ = get_current_network_id()
    # end if
    counts_ = Array()
    args_ = Array({"network_id": network_id_, "number": 1, "fields": "ids", "no_found_rows": False})
    q_ = php_new_class("WP_Site_Query", lambda : WP_Site_Query(args_))
    counts_["all"] = q_.found_sites
    _args_ = args_
    statuses_ = Array("public", "archived", "mature", "spam", "deleted")
    for status_ in statuses_:
        _args_ = args_
        _args_[status_] = 1
        q_ = php_new_class("WP_Site_Query", lambda : WP_Site_Query(_args_))
        counts_[status_] = q_.found_sites
    # end for
    return counts_
# end def wp_count_sites
