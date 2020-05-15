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
#// These functions are needed to load Multisite.
#// 
#// @since 3.0.0
#// 
#// @package WordPress
#// @subpackage Multisite
#// 
#// 
#// Whether a subdomain configuration is enabled.
#// 
#// @since 3.0.0
#// 
#// @return bool True if subdomain configuration is enabled, false otherwise.
#//
def is_subdomain_install(*args_):
    
    if php_defined("SUBDOMAIN_INSTALL"):
        return SUBDOMAIN_INSTALL
    # end if
    return php_defined("VHOST") and VHOST == "yes"
# end def is_subdomain_install
#// 
#// Returns array of network plugin files to be included in global scope.
#// 
#// The default directory is wp-content/plugins. To change the default directory
#// manually, define `WP_PLUGIN_DIR` and `WP_PLUGIN_URL` in `wp-config.php`.
#// 
#// @access private
#// @since 3.1.0
#// 
#// @return string[] Array of absolute paths to files to include.
#//
def wp_get_active_network_plugins(*args_):
    
    active_plugins = get_site_option("active_sitewide_plugins", Array())
    if php_empty(lambda : active_plugins):
        return Array()
    # end if
    plugins = Array()
    active_plugins = php_array_keys(active_plugins)
    sort(active_plugins)
    for plugin in active_plugins:
        if (not validate_file(plugin)) and ".php" == php_substr(plugin, -4) and php_file_exists(WP_PLUGIN_DIR + "/" + plugin):
            plugins[-1] = WP_PLUGIN_DIR + "/" + plugin
        # end if
    # end for
    return plugins
# end def wp_get_active_network_plugins
#// 
#// Checks status of current blog.
#// 
#// Checks if the blog is deleted, inactive, archived, or spammed.
#// 
#// Dies with a default message if the blog does not pass the check.
#// 
#// To change the default message when a blog does not pass the check,
#// use the wp-content/blog-deleted.php, blog-inactive.php and
#// blog-suspended.php drop-ins.
#// 
#// @since 3.0.0
#// 
#// @return true|string Returns true on success, or drop-in file to include.
#//
def ms_site_check(*args_):
    
    #// 
    #// Filters checking the status of the current blog.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool|null $check Whether to skip the blog status check. Default null.
    #//
    check = apply_filters("ms_site_check", None)
    if None != check:
        return True
    # end if
    #// Allow super admins to see blocked sites.
    if is_super_admin():
        return True
    # end if
    blog = get_site()
    if "1" == blog.deleted:
        if php_file_exists(WP_CONTENT_DIR + "/blog-deleted.php"):
            return WP_CONTENT_DIR + "/blog-deleted.php"
        else:
            wp_die(__("This site is no longer available."), "", Array({"response": 410}))
        # end if
    # end if
    if "2" == blog.deleted:
        if php_file_exists(WP_CONTENT_DIR + "/blog-inactive.php"):
            return WP_CONTENT_DIR + "/blog-inactive.php"
        else:
            admin_email = php_str_replace("@", " AT ", get_site_option("admin_email", "support@" + get_network().domain))
            wp_die(php_sprintf(__("This site has not been activated yet. If you are having problems activating your site, please contact %s."), php_sprintf("<a href=\"mailto:%1$s\">%1$s</a>", admin_email)))
        # end if
    # end if
    if "1" == blog.archived or "1" == blog.spam:
        if php_file_exists(WP_CONTENT_DIR + "/blog-suspended.php"):
            return WP_CONTENT_DIR + "/blog-suspended.php"
        else:
            wp_die(__("This site has been archived or suspended."), "", Array({"response": 410}))
        # end if
    # end if
    return True
# end def ms_site_check
#// 
#// Retrieve the closest matching network for a domain and path.
#// 
#// @since 3.9.0
#// 
#// @internal In 4.4.0, converted to a wrapper for WP_Network::get_by_path()
#// 
#// @param string   $domain   Domain to check.
#// @param string   $path     Path to check.
#// @param int|null $segments Path segments to use. Defaults to null, or the full path.
#// @return WP_Network|false Network object if successful. False when no network is found.
#//
def get_network_by_path(domain=None, path=None, segments=None, *args_):
    
    return WP_Network.get_by_path(domain, path, segments)
# end def get_network_by_path
#// 
#// Retrieves the closest matching site object by its domain and path.
#// 
#// This will not necessarily return an exact match for a domain and path. Instead, it
#// breaks the domain and path into pieces that are then used to match the closest
#// possibility from a query.
#// 
#// The intent of this method is to match a site object during bootstrap for a
#// requested site address
#// 
#// @since 3.9.0
#// @since 4.7.0 Updated to always return a `WP_Site` object.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string   $domain   Domain to check.
#// @param string   $path     Path to check.
#// @param int|null $segments Path segments to use. Defaults to null, or the full path.
#// @return WP_Site|false Site object if successful. False when no site is found.
#//
def get_site_by_path(domain=None, path=None, segments=None, *args_):
    
    path_segments = php_array_filter(php_explode("/", php_trim(path, "/")))
    #// 
    #// Filters the number of path segments to consider when searching for a site.
    #// 
    #// @since 3.9.0
    #// 
    #// @param int|null $segments The number of path segments to consider. WordPress by default looks at
    #// one path segment following the network path. The function default of
    #// null only makes sense when you know the requested path should match a site.
    #// @param string   $domain   The requested domain.
    #// @param string   $path     The requested path, in full.
    #//
    segments = apply_filters("site_by_path_segments_count", segments, domain, path)
    if None != segments and php_count(path_segments) > segments:
        path_segments = php_array_slice(path_segments, 0, segments)
    # end if
    paths = Array()
    while True:
        
        if not (php_count(path_segments)):
            break
        # end if
        paths[-1] = "/" + php_implode("/", path_segments) + "/"
        php_array_pop(path_segments)
    # end while
    paths[-1] = "/"
    #// 
    #// Determine a site by its domain and path.
    #// 
    #// This allows one to short-circuit the default logic, perhaps by
    #// replacing it with a routine that is more optimal for your setup.
    #// 
    #// Return null to avoid the short-circuit. Return false if no site
    #// can be found at the requested domain and path. Otherwise, return
    #// a site object.
    #// 
    #// @since 3.9.0
    #// 
    #// @param null|false|WP_Site $site     Site value to return by path. Default null
    #// to continue retrieving the site.
    #// @param string             $domain   The requested domain.
    #// @param string             $path     The requested path, in full.
    #// @param int|null           $segments The suggested number of paths to consult.
    #// Default null, meaning the entire path was to be consulted.
    #// @param string[]           $paths    The paths to search for, based on $path and $segments.
    #//
    pre = apply_filters("pre_get_site_by_path", None, domain, path, segments, paths)
    if None != pre:
        if False != pre and (not type(pre).__name__ == "WP_Site"):
            pre = php_new_class("WP_Site", lambda : WP_Site(pre))
        # end if
        return pre
    # end if
    #// 
    #// @todo
    #// Caching, etc. Consider alternative optimization routes,
    #// perhaps as an opt-in for plugins, rather than using the pre_* filter.
    #// For example: The segments filter can expand or ignore paths.
    #// If persistent caching is enabled, we could query the DB for a path <> '/'
    #// then cache whether we can just always ignore paths.
    #// 
    #// Either www or non-www is supported, not both. If a www domain is requested,
    #// query for both to provide the proper redirect.
    domains = Array(domain)
    if "www." == php_substr(domain, 0, 4):
        domains[-1] = php_substr(domain, 4)
    # end if
    args = Array({"number": 1, "update_site_meta_cache": False})
    if php_count(domains) > 1:
        args["domain__in"] = domains
        args["orderby"]["domain_length"] = "DESC"
    else:
        args["domain"] = php_array_shift(domains)
    # end if
    if php_count(paths) > 1:
        args["path__in"] = paths
        args["orderby"]["path_length"] = "DESC"
    else:
        args["path"] = php_array_shift(paths)
    # end if
    result = get_sites(args)
    site = php_array_shift(result)
    if site:
        return site
    # end if
    return False
# end def get_site_by_path
#// 
#// Identifies the network and site of a requested domain and path and populates the
#// corresponding network and site global objects as part of the multisite bootstrap process.
#// 
#// Prior to 4.6.0, this was a procedural block in `ms-settings.php`. It was wrapped into
#// a function to facilitate unit tests. It should not be used outside of core.
#// 
#// Usually, it's easier to query the site first, which then declares its network.
#// In limited situations, we either can or must find the network first.
#// 
#// If a network and site are found, a `true` response will be returned so that the
#// request can continue.
#// 
#// If neither a network or site is found, `false` or a URL string will be returned
#// so that either an error can be shown or a redirect can occur.
#// 
#// @since 4.6.0
#// @access private
#// 
#// @global WP_Network $current_site The current network.
#// @global WP_Site    $current_blog The current site.
#// 
#// @param string $domain    The requested domain.
#// @param string $path      The requested path.
#// @param bool   $subdomain Optional. Whether a subdomain (true) or subdirectory (false) configuration.
#// Default false.
#// @return bool|string True if bootstrap successfully populated `$current_blog` and `$current_site`.
#// False if bootstrap could not be properly completed.
#// Redirect URL if parts exist, but the request as a whole can not be fulfilled.
#//
def ms_load_current_site_and_network(domain=None, path=None, subdomain=False, *args_):
    
    global current_site,current_blog
    php_check_if_defined("current_site","current_blog")
    #// If the network is defined in wp-config.php, we can simply use that.
    if php_defined("DOMAIN_CURRENT_SITE") and php_defined("PATH_CURRENT_SITE"):
        current_site = php_new_class("stdClass", lambda : stdClass())
        current_site.id = SITE_ID_CURRENT_SITE if php_defined("SITE_ID_CURRENT_SITE") else 1
        current_site.domain = DOMAIN_CURRENT_SITE
        current_site.path = PATH_CURRENT_SITE
        if php_defined("BLOG_ID_CURRENT_SITE"):
            current_site.blog_id = BLOG_ID_CURRENT_SITE
        elif php_defined("BLOGID_CURRENT_SITE"):
            #// Deprecated.
            current_site.blog_id = BLOGID_CURRENT_SITE
        # end if
        if 0 == strcasecmp(current_site.domain, domain) and 0 == strcasecmp(current_site.path, path):
            current_blog = get_site_by_path(domain, path)
        elif "/" != current_site.path and 0 == strcasecmp(current_site.domain, domain) and 0 == php_stripos(path, current_site.path):
            #// If the current network has a path and also matches the domain and path of the request,
            #// we need to look for a site using the first path segment following the network's path.
            current_blog = get_site_by_path(domain, path, 1 + php_count(php_explode("/", php_trim(current_site.path, "/"))))
        else:
            #// Otherwise, use the first path segment (as usual).
            current_blog = get_site_by_path(domain, path, 1)
        # end if
    elif (not subdomain):
        #// 
        #// A "subdomain" installation can be re-interpreted to mean "can support any domain".
        #// If we're not dealing with one of these installations, then the important part is determining
        #// the network first, because we need the network's path to identify any sites.
        #//
        current_site = wp_cache_get("current_network", "site-options")
        if (not current_site):
            #// Are there even two networks installed?
            networks = get_networks(Array({"number": 2}))
            if php_count(networks) == 1:
                current_site = php_array_shift(networks)
                wp_cache_add("current_network", current_site, "site-options")
            elif php_empty(lambda : networks):
                #// A network not found hook should fire here.
                return False
            # end if
        # end if
        if php_empty(lambda : current_site):
            current_site = WP_Network.get_by_path(domain, path, 1)
        # end if
        if php_empty(lambda : current_site):
            #// 
            #// Fires when a network cannot be found based on the requested domain and path.
            #// 
            #// At the time of this action, the only recourse is to redirect somewhere
            #// and exit. If you want to declare a particular network, do so earlier.
            #// 
            #// @since 4.4.0
            #// 
            #// @param string $domain       The domain used to search for a network.
            #// @param string $path         The path used to search for a path.
            #//
            do_action("ms_network_not_found", domain, path)
            return False
        elif path == current_site.path:
            current_blog = get_site_by_path(domain, path)
        else:
            #// Search the network path + one more path segment (on top of the network path).
            current_blog = get_site_by_path(domain, path, php_substr_count(current_site.path, "/"))
        # end if
    else:
        #// Find the site by the domain and at most the first path segment.
        current_blog = get_site_by_path(domain, path, 1)
        if current_blog:
            current_site = WP_Network.get_instance(current_blog.site_id if current_blog.site_id else 1)
        else:
            #// If you don't have a site with the same domain/path as a network, you're pretty screwed, but:
            current_site = WP_Network.get_by_path(domain, path, 1)
        # end if
    # end if
    #// The network declared by the site trumps any constants.
    if current_blog and current_blog.site_id != current_site.id:
        current_site = WP_Network.get_instance(current_blog.site_id)
    # end if
    #// No network has been found, bail.
    if php_empty(lambda : current_site):
        #// This action is documented in wp-includes/ms-settings.php
        do_action("ms_network_not_found", domain, path)
        return False
    # end if
    #// During activation of a new subdomain, the requested site does not yet exist.
    if php_empty(lambda : current_blog) and wp_installing():
        current_blog = php_new_class("stdClass", lambda : stdClass())
        current_blog.blog_id = 1
        blog_id = 1
        current_blog.public = 1
    # end if
    #// No site has been found, bail.
    if php_empty(lambda : current_blog):
        #// We're going to redirect to the network URL, with some possible modifications.
        scheme = "https" if is_ssl() else "http"
        destination = str(scheme) + str("://") + str(current_site.domain) + str(current_site.path)
        #// 
        #// Fires when a network can be determined but a site cannot.
        #// 
        #// At the time of this action, the only recourse is to redirect somewhere
        #// and exit. If you want to declare a particular site, do so earlier.
        #// 
        #// @since 3.9.0
        #// 
        #// @param object $current_site The network that had been determined.
        #// @param string $domain       The domain used to search for a site.
        #// @param string $path         The path used to search for a site.
        #//
        do_action("ms_site_not_found", current_site, domain, path)
        if subdomain and (not php_defined("NOBLOGREDIRECT")):
            #// For a "subdomain" installation, redirect to the signup form specifically.
            destination += "wp-signup.php?new=" + php_str_replace("." + current_site.domain, "", domain)
        elif subdomain:
            #// 
            #// For a "subdomain" installation, the NOBLOGREDIRECT constant
            #// can be used to avoid a redirect to the signup form.
            #// Using the ms_site_not_found action is preferred to the constant.
            #//
            if "%siteurl%" != NOBLOGREDIRECT:
                destination = NOBLOGREDIRECT
            # end if
        elif 0 == strcasecmp(current_site.domain, domain):
            #// 
            #// If the domain we were searching for matches the network's domain,
            #// it's no use redirecting back to ourselves -- it'll cause a loop.
            #// As we couldn't find a site, we're simply not installed.
            #//
            return False
        # end if
        return destination
    # end if
    #// Figure out the current network's main site.
    if php_empty(lambda : current_site.blog_id):
        current_site.blog_id = get_main_site_id(current_site.id)
    # end if
    return True
# end def ms_load_current_site_and_network
#// 
#// Displays a failure message.
#// 
#// Used when a blog's tables do not exist. Checks for a missing $wpdb->site table as well.
#// 
#// @access private
#// @since 3.0.0
#// @since 4.4.0 The `$domain` and `$path` parameters were added.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $domain The requested domain for the error to reference.
#// @param string $path   The requested path for the error to reference.
#//
def ms_not_installed(domain=None, path=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not is_admin()):
        dead_db()
    # end if
    wp_load_translations_early()
    title = __("Error establishing a database connection")
    msg = "<h1>" + title + "</h1>"
    msg += "<p>" + __("If your site does not display, please contact the owner of this network.") + ""
    msg += " " + __("If you are the owner of this network please check that MySQL is running properly and all tables are error free.") + "</p>"
    query = wpdb.prepare("SHOW TABLES LIKE %s", wpdb.esc_like(wpdb.site))
    if (not wpdb.get_var(query)):
        msg += "<p>" + php_sprintf(__("<strong>Database tables are missing.</strong> This means that MySQL is not running, WordPress was not installed properly, or someone deleted %s. You really should look at your database now."), "<code>" + wpdb.site + "</code>") + "</p>"
    else:
        msg += "<p>" + php_sprintf(__("<strong>Could not find site %1$s.</strong> Searched for table %2$s in database %3$s. Is that right?"), "<code>" + php_rtrim(domain + path, "/") + "</code>", "<code>" + wpdb.blogs + "</code>", "<code>" + DB_NAME + "</code>") + "</p>"
    # end if
    msg += "<p><strong>" + __("What do I do now?") + "</strong> "
    msg += php_sprintf(__("Read the <a href=\"%s\" target=\"_blank\">bug report</a> page. Some of the guidelines there may help you figure out what went wrong."), __("https://wordpress.org/support/article/debugging-a-wordpress-network/"))
    msg += " " + __("If you&#8217;re still stuck with this message, then check that your database contains the following tables:") + "</p><ul>"
    for t,table in wpdb.tables("global"):
        if "sitecategories" == t:
            continue
        # end if
        msg += "<li>" + table + "</li>"
    # end for
    msg += "</ul>"
    wp_die(msg, title, Array({"response": 500}))
# end def ms_not_installed
#// 
#// This deprecated function formerly set the site_name property of the $current_site object.
#// 
#// This function simply returns the object, as before.
#// The bootstrap takes care of setting site_name.
#// 
#// @access private
#// @since 3.0.0
#// @deprecated 3.9.0 Use get_current_site() instead.
#// 
#// @param object $current_site
#// @return object
#//
def get_current_site_name(current_site=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.9.0", "get_current_site()")
    return current_site
# end def get_current_site_name
#// 
#// This deprecated function managed much of the site and network loading in multisite.
#// 
#// The current bootstrap code is now responsible for parsing the site and network load as
#// well as setting the global $current_site object.
#// 
#// @access private
#// @since 3.0.0
#// @deprecated 3.9.0
#// 
#// @global object $current_site
#// 
#// @return object
#//
def wpmu_current_site(*args_):
    
    global current_site
    php_check_if_defined("current_site")
    _deprecated_function(__FUNCTION__, "3.9.0")
    return current_site
# end def wpmu_current_site
#// 
#// Retrieve an object containing information about the requested network.
#// 
#// @since 3.9.0
#// @deprecated 4.7.0 Use `get_network()`
#// @see get_network()
#// 
#// @internal In 4.6.0, converted to use get_network()
#// 
#// @param object|int $network The network's database row or ID.
#// @return WP_Network|false Object containing network information if found, false if not.
#//
def wp_get_network(network=None, *args_):
    
    _deprecated_function(__FUNCTION__, "4.7.0", "get_network()")
    network = get_network(network)
    if None == network:
        return False
    # end if
    return network
# end def wp_get_network
