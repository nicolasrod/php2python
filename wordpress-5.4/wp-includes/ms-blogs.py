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
def wpmu_update_blogs_date(*args_):
    
    site_id = get_current_blog_id()
    update_blog_details(site_id, Array({"last_updated": current_time("mysql", True)}))
    #// 
    #// Fires after the blog details are updated.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int $blog_id Site ID.
    #//
    do_action("wpmu_blog_updated", site_id)
# end def wpmu_update_blogs_date
#// 
#// Get a full blog URL, given a blog id.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $blog_id Blog ID.
#// @return string Full URL of the blog if found. Empty string if not.
#//
def get_blogaddress_by_id(blog_id=None, *args_):
    
    bloginfo = get_site(int(blog_id))
    if php_empty(lambda : bloginfo):
        return ""
    # end if
    scheme = php_parse_url(bloginfo.home, PHP_URL_SCHEME)
    scheme = "http" if php_empty(lambda : scheme) else scheme
    return esc_url(scheme + "://" + bloginfo.domain + bloginfo.path)
# end def get_blogaddress_by_id
#// 
#// Get a full blog URL, given a blog name.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $blogname The (subdomain or directory) name
#// @return string
#//
def get_blogaddress_by_name(blogname=None, *args_):
    
    if is_subdomain_install():
        if "main" == blogname:
            blogname = "www"
        # end if
        url = php_rtrim(network_home_url(), "/")
        if (not php_empty(lambda : blogname)):
            url = php_preg_replace("|^([^\\.]+://)|", "${1}" + blogname + ".", url)
        # end if
    else:
        url = network_home_url(blogname)
    # end if
    return esc_url(url + "/")
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
def get_id_from_blogname(slug=None, *args_):
    
    current_network = get_network()
    slug = php_trim(slug, "/")
    if is_subdomain_install():
        domain = slug + "." + php_preg_replace("|^www\\.|", "", current_network.domain)
        path = current_network.path
    else:
        domain = current_network.domain
        path = current_network.path + slug + "/"
    # end if
    site_ids = get_sites(Array({"number": 1, "fields": "ids", "domain": domain, "path": path, "update_site_meta_cache": False}))
    if php_empty(lambda : site_ids):
        return None
    # end if
    return php_array_shift(site_ids)
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
def get_blog_details(fields=None, get_all=True, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_is_array(fields):
        if (php_isset(lambda : fields["blog_id"])):
            blog_id = fields["blog_id"]
        elif (php_isset(lambda : fields["domain"])) and (php_isset(lambda : fields["path"])):
            key = php_md5(fields["domain"] + fields["path"])
            blog = wp_cache_get(key, "blog-lookup")
            if False != blog:
                return blog
            # end if
            if php_substr(fields["domain"], 0, 4) == "www.":
                nowww = php_substr(fields["domain"], 4)
                blog = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.blogs) + str(" WHERE domain IN (%s,%s) AND path = %s ORDER BY CHAR_LENGTH(domain) DESC"), nowww, fields["domain"], fields["path"]))
            else:
                blog = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.blogs) + str(" WHERE domain = %s AND path = %s"), fields["domain"], fields["path"]))
            # end if
            if blog:
                wp_cache_set(blog.blog_id + "short", blog, "blog-details")
                blog_id = blog.blog_id
            else:
                return False
            # end if
        elif (php_isset(lambda : fields["domain"])) and is_subdomain_install():
            key = php_md5(fields["domain"])
            blog = wp_cache_get(key, "blog-lookup")
            if False != blog:
                return blog
            # end if
            if php_substr(fields["domain"], 0, 4) == "www.":
                nowww = php_substr(fields["domain"], 4)
                blog = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.blogs) + str(" WHERE domain IN (%s,%s) ORDER BY CHAR_LENGTH(domain) DESC"), nowww, fields["domain"]))
            else:
                blog = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.blogs) + str(" WHERE domain = %s"), fields["domain"]))
            # end if
            if blog:
                wp_cache_set(blog.blog_id + "short", blog, "blog-details")
                blog_id = blog.blog_id
            else:
                return False
            # end if
        else:
            return False
        # end if
    else:
        if (not fields):
            blog_id = get_current_blog_id()
        elif (not php_is_numeric(fields)):
            blog_id = get_id_from_blogname(fields)
        else:
            blog_id = fields
        # end if
    # end if
    blog_id = int(blog_id)
    all = "" if get_all else "short"
    details = wp_cache_get(blog_id + all, "blog-details")
    if details:
        if (not php_is_object(details)):
            if -1 == details:
                return False
            else:
                #// Clear old pre-serialized objects. Cache clients do better with that.
                wp_cache_delete(blog_id + all, "blog-details")
                details = None
            # end if
        else:
            return details
        # end if
    # end if
    #// Try the other cache.
    if get_all:
        details = wp_cache_get(blog_id + "short", "blog-details")
    else:
        details = wp_cache_get(blog_id, "blog-details")
        #// If short was requested and full cache is set, we can return.
        if details:
            if (not php_is_object(details)):
                if -1 == details:
                    return False
                else:
                    #// Clear old pre-serialized objects. Cache clients do better with that.
                    wp_cache_delete(blog_id, "blog-details")
                    details = None
                # end if
            else:
                return details
            # end if
        # end if
    # end if
    if php_empty(lambda : details):
        details = WP_Site.get_instance(blog_id)
        if (not details):
            #// Set the full cache.
            wp_cache_set(blog_id, -1, "blog-details")
            return False
        # end if
    # end if
    if (not type(details).__name__ == "WP_Site"):
        details = php_new_class("WP_Site", lambda : WP_Site(details))
    # end if
    if (not get_all):
        wp_cache_set(blog_id + all, details, "blog-details")
        return details
    # end if
    switch_to_blog(blog_id)
    details.blogname = get_option("blogname")
    details.siteurl = get_option("siteurl")
    details.post_count = get_option("post_count")
    details.home = get_option("home")
    restore_current_blog()
    #// 
    #// Filters a blog's details.
    #// 
    #// @since MU (3.0.0)
    #// @deprecated 4.7.0 Use {@see 'site_details'} instead.
    #// 
    #// @param object $details The blog details.
    #//
    details = apply_filters_deprecated("blog_details", Array(details), "4.7.0", "site_details")
    wp_cache_set(blog_id + all, details, "blog-details")
    key = php_md5(details.domain + details.path)
    wp_cache_set(key, details, "blog-lookup")
    return details
# end def get_blog_details
#// 
#// Clear the blog details cache.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $blog_id Optional. Blog ID. Defaults to current blog.
#//
def refresh_blog_details(blog_id=0, *args_):
    
    blog_id = int(blog_id)
    if (not blog_id):
        blog_id = get_current_blog_id()
    # end if
    clean_blog_cache(blog_id)
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
def update_blog_details(blog_id=None, details=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : details):
        return False
    # end if
    if php_is_object(details):
        details = get_object_vars(details)
    # end if
    site = wp_update_site(blog_id, details)
    if is_wp_error(site):
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
def clean_site_details_cache(site_id=0, *args_):
    
    site_id = int(site_id)
    if (not site_id):
        site_id = get_current_blog_id()
    # end if
    wp_cache_delete(site_id, "site-details")
    wp_cache_delete(site_id, "blog-details")
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
def get_blog_option(id=None, option=None, default=False, *args_):
    
    id = int(id)
    if php_empty(lambda : id):
        id = get_current_blog_id()
    # end if
    if get_current_blog_id() == id:
        return get_option(option, default)
    # end if
    switch_to_blog(id)
    value = get_option(option, default)
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
    return apply_filters(str("blog_option_") + str(option), value, id)
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
def add_blog_option(id=None, option=None, value=None, *args_):
    
    id = int(id)
    if php_empty(lambda : id):
        id = get_current_blog_id()
    # end if
    if get_current_blog_id() == id:
        return add_option(option, value)
    # end if
    switch_to_blog(id)
    return_ = add_option(option, value)
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
def delete_blog_option(id=None, option=None, *args_):
    
    id = int(id)
    if php_empty(lambda : id):
        id = get_current_blog_id()
    # end if
    if get_current_blog_id() == id:
        return delete_option(option)
    # end if
    switch_to_blog(id)
    return_ = delete_option(option)
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
def update_blog_option(id=None, option=None, value=None, deprecated=None, *args_):
    
    id = int(id)
    if None != deprecated:
        _deprecated_argument(__FUNCTION__, "3.1.0")
    # end if
    if get_current_blog_id() == id:
        return update_option(option, value)
    # end if
    switch_to_blog(id)
    return_ = update_option(option, value)
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
def switch_to_blog(new_blog_id=None, deprecated=None, *args_):
    global PHP_GLOBALS
    global wpdb
    php_check_if_defined("wpdb")
    prev_blog_id = get_current_blog_id()
    if php_empty(lambda : new_blog_id):
        new_blog_id = prev_blog_id
    # end if
    PHP_GLOBALS["_wp_switched_stack"][-1] = prev_blog_id
    #// 
    #// If we're switching to the same blog id that we're on,
    #// set the right vars, do the associated actions, but skip
    #// the extra unnecessary work
    #//
    if new_blog_id == prev_blog_id:
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
        do_action("switch_blog", new_blog_id, prev_blog_id, "switch")
        PHP_GLOBALS["switched"] = True
        return True
    # end if
    wpdb.set_blog_id(new_blog_id)
    PHP_GLOBALS["table_prefix"] = wpdb.get_blog_prefix()
    PHP_GLOBALS["blog_id"] = new_blog_id
    if php_function_exists("wp_cache_switch_to_blog"):
        wp_cache_switch_to_blog(new_blog_id)
    else:
        global wp_object_cache
        php_check_if_defined("wp_object_cache")
        if php_is_object(wp_object_cache) and (php_isset(lambda : wp_object_cache.global_groups)):
            global_groups = wp_object_cache.global_groups
        else:
            global_groups = False
        # end if
        wp_cache_init()
        if php_function_exists("wp_cache_add_global_groups"):
            if php_is_array(global_groups):
                wp_cache_add_global_groups(global_groups)
            else:
                wp_cache_add_global_groups(Array("users", "userlogins", "usermeta", "user_meta", "useremail", "userslugs", "site-transient", "site-options", "blog-lookup", "blog-details", "rss", "global-posts", "blog-id-cache", "networks", "sites", "site-details", "blog_meta"))
            # end if
            wp_cache_add_non_persistent_groups(Array("counts", "plugins"))
        # end if
    # end if
    #// This filter is documented in wp-includes/ms-blogs.php
    do_action("switch_blog", new_blog_id, prev_blog_id, "switch")
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
def restore_current_blog(*args_):
    global PHP_GLOBALS
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : PHP_GLOBALS["_wp_switched_stack"]):
        return False
    # end if
    new_blog_id = php_array_pop(PHP_GLOBALS["_wp_switched_stack"])
    prev_blog_id = get_current_blog_id()
    if new_blog_id == prev_blog_id:
        #// This filter is documented in wp-includes/ms-blogs.php
        do_action("switch_blog", new_blog_id, prev_blog_id, "restore")
        #// If we still have items in the switched stack, consider ourselves still 'switched'.
        PHP_GLOBALS["switched"] = (not php_empty(lambda : PHP_GLOBALS["_wp_switched_stack"]))
        return True
    # end if
    wpdb.set_blog_id(new_blog_id)
    PHP_GLOBALS["blog_id"] = new_blog_id
    PHP_GLOBALS["table_prefix"] = wpdb.get_blog_prefix()
    if php_function_exists("wp_cache_switch_to_blog"):
        wp_cache_switch_to_blog(new_blog_id)
    else:
        global wp_object_cache
        php_check_if_defined("wp_object_cache")
        if php_is_object(wp_object_cache) and (php_isset(lambda : wp_object_cache.global_groups)):
            global_groups = wp_object_cache.global_groups
        else:
            global_groups = False
        # end if
        wp_cache_init()
        if php_function_exists("wp_cache_add_global_groups"):
            if php_is_array(global_groups):
                wp_cache_add_global_groups(global_groups)
            else:
                wp_cache_add_global_groups(Array("users", "userlogins", "usermeta", "user_meta", "useremail", "userslugs", "site-transient", "site-options", "blog-lookup", "blog-details", "rss", "global-posts", "blog-id-cache", "networks", "sites", "site-details", "blog_meta"))
            # end if
            wp_cache_add_non_persistent_groups(Array("counts", "plugins"))
        # end if
    # end if
    #// This filter is documented in wp-includes/ms-blogs.php
    do_action("switch_blog", new_blog_id, prev_blog_id, "restore")
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
def wp_switch_roles_and_user(new_site_id=None, old_site_id=None, *args_):
    
    if new_site_id == old_site_id:
        return
    # end if
    if (not did_action("init")):
        return
    # end if
    wp_roles().for_site(new_site_id)
    wp_get_current_user().for_site(new_site_id)
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
def ms_is_switched(*args_):
    
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
def is_archived(id=None, *args_):
    
    return get_blog_status(id, "archived")
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
def update_archived(id=None, archived=None, *args_):
    
    update_blog_status(id, "archived", archived)
    return archived
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
def update_blog_status(blog_id=None, pref=None, value=None, deprecated=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if None != deprecated:
        _deprecated_argument(__FUNCTION__, "3.1.0")
    # end if
    if (not php_in_array(pref, Array("site_id", "domain", "path", "registered", "last_updated", "public", "archived", "mature", "spam", "deleted", "lang_id"))):
        return value
    # end if
    result = wp_update_site(blog_id, Array({pref: value}))
    if is_wp_error(result):
        return False
    # end if
    return value
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
def get_blog_status(id=None, pref=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    details = get_site(id)
    if details:
        return details.pref
    # end if
    return wpdb.get_var(wpdb.prepare(str("SELECT %s FROM ") + str(wpdb.blogs) + str(" WHERE blog_id = %d"), pref, id))
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
def get_last_updated(deprecated="", start=0, quantity=40, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "MU")
        pass
    # end if
    return wpdb.get_results(wpdb.prepare(str("SELECT blog_id, domain, path FROM ") + str(wpdb.blogs) + str(" WHERE site_id = %d AND public = '1' AND archived = '0' AND mature = '0' AND spam = '0' AND deleted = '0' AND last_updated != '0000-00-00 00:00:00' ORDER BY last_updated DESC limit %d, %d"), get_current_network_id(), start, quantity), ARRAY_A)
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
def _update_blog_date_on_post_publish(new_status=None, old_status=None, post=None, *args_):
    
    post_type_obj = get_post_type_object(post.post_type)
    if (not post_type_obj) or (not post_type_obj.public):
        return
    # end if
    if "publish" != new_status and "publish" != old_status:
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
def _update_blog_date_on_post_delete(post_id=None, *args_):
    
    post = get_post(post_id)
    post_type_obj = get_post_type_object(post.post_type)
    if (not post_type_obj) or (not post_type_obj.public):
        return
    # end if
    if "publish" != post.post_status:
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
def _update_posts_count_on_delete(post_id=None, *args_):
    
    post = get_post(post_id)
    if (not post) or "publish" != post.post_status or "post" != post.post_type:
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
def _update_posts_count_on_transition_post_status(new_status=None, old_status=None, post=None, *args_):
    
    if new_status == old_status:
        return
    # end if
    if "post" != get_post_type(post):
        return
    # end if
    if "publish" != new_status and "publish" != old_status:
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
def wp_count_sites(network_id=None, *args_):
    
    if php_empty(lambda : network_id):
        network_id = get_current_network_id()
    # end if
    counts = Array()
    args = Array({"network_id": network_id, "number": 1, "fields": "ids", "no_found_rows": False})
    q = php_new_class("WP_Site_Query", lambda : WP_Site_Query(args))
    counts["all"] = q.found_sites
    _args = args
    statuses = Array("public", "archived", "mature", "spam", "deleted")
    for status in statuses:
        _args = args
        _args[status] = 1
        q = php_new_class("WP_Site_Query", lambda : WP_Site_Query(_args))
        counts[status] = q.found_sites
    # end for
    return counts
# end def wp_count_sites
