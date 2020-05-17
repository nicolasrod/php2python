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
#// Deprecated functions from WordPress MU and the multisite feature. You shouldn't
#// use these functions and look for the alternatives instead. The functions will be
#// removed in a later version.
#// 
#// @package WordPress
#// @subpackage Deprecated
#// @since 3.0.0
#// 
#// 
#// Deprecated functions come here to die.
#// 
#// 
#// Get the "dashboard blog", the blog where users without a blog edit their profile data.
#// Dashboard blog functionality was removed in WordPress 3.1, replaced by the user admin.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.1.0 Use get_site()
#// @see get_site()
#// 
#// @return WP_Site Current site object.
#//
def get_dashboard_blog(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.1.0", "get_site()")
    blog_ = get_site_option("dashboard_blog")
    if blog_:
        return get_site(blog_)
    # end if
    return get_site(get_network().site_id)
# end def get_dashboard_blog
#// 
#// Generates a random password.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0 Use wp_generate_password()
#// @see wp_generate_password()
#// 
#// @param int $len Optional. The length of password to generate. Default 8.
#//
def generate_random_password(len_=8, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "wp_generate_password()")
    return wp_generate_password(len_)
# end def generate_random_password
#// 
#// Determine if user is a site admin.
#// 
#// Plugins should use is_multisite() instead of checking if this function exists
#// to determine if multisite is enabled.
#// 
#// This function must reside in a file included only if is_multisite() due to
#// legacy function_exists() checks to determine if multisite is enabled.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0 Use is_super_admin()
#// @see is_super_admin()
#// 
#// @param string $user_login Optional. Username for the user to check. Default empty.
#//
def is_site_admin(user_login_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "is_super_admin()")
    if php_empty(lambda : user_login_):
        user_id_ = get_current_user_id()
        if (not user_id_):
            return False
        # end if
    else:
        user_ = get_user_by("login", user_login_)
        if (not user_.exists()):
            return False
        # end if
        user_id_ = user_.ID
    # end if
    return is_super_admin(user_id_)
# end def is_site_admin
if (not php_function_exists("graceful_fail")):
    #// 
    #// Deprecated functionality to gracefully fail.
    #// 
    #// @since MU (3.0.0)
    #// @deprecated 3.0.0 Use wp_die()
    #// @see wp_die()
    #//
    def graceful_fail(message_=None, *_args_):
        
        
        _deprecated_function(__FUNCTION__, "3.0.0", "wp_die()")
        message_ = apply_filters("graceful_fail", message_)
        message_template_ = apply_filters("graceful_fail_template", """<!DOCTYPE html>
        <html xmlns=\"http://www.w3.org/1999/xhtml\"><head>
        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
        <title>Error!</title>
        <style type=\"text/css\">
        img {
        border: 0;
        }
        body {
        line-height: 1.6em; font-family: Georgia, serif; width: 390px; margin: auto;
        text-align: center;
        }
        .message {
        font-size: 22px;
        width: 350px;
        margin: auto;
        }
        </style>
        </head>
        <body>
        <p class=\"message\">%s</p>
        </body>
        </html>""")
        php_print(php_sprintf(message_template_, message_))
        php_exit()
    # end def graceful_fail
# end if
#// 
#// Deprecated functionality to retrieve user information.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0 Use get_user_by()
#// @see get_user_by()
#// 
#// @param string $username Username.
#//
def get_user_details(username_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "get_user_by()")
    return get_user_by("login", username_)
# end def get_user_details
#// 
#// Deprecated functionality to clear the global post cache.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0 Use clean_post_cache()
#// @see clean_post_cache()
#// 
#// @param int $post_id Post ID.
#//
def clear_global_post_cache(post_id_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "clean_post_cache()")
# end def clear_global_post_cache
#// 
#// Deprecated functionality to determin if the current site is the main site.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0 Use is_main_site()
#// @see is_main_site()
#//
def is_main_blog(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "is_main_site()")
    return is_main_site()
# end def is_main_blog
#// 
#// Deprecated functionality to validate an email address.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0 Use is_email()
#// @see is_email()
#// 
#// @param string $email        Email address to verify.
#// @param bool   $check_domain Deprecated.
#// @return string|bool Either false or the valid email address.
#//
def validate_email(email_=None, check_domain_=None, *_args_):
    if check_domain_ is None:
        check_domain_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "3.0.0", "is_email()")
    return is_email(email_, check_domain_)
# end def validate_email
#// 
#// Deprecated functionality to retrieve a list of all sites.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0 Use wp_get_sites()
#// @see wp_get_sites()
#// 
#// @param int    $start      Optional. Offset for retrieving the blog list. Default 0.
#// @param int    $num        Optional. Number of blogs to list. Default 10.
#// @param string $deprecated Unused.
#//
def get_blog_list(start_=0, num_=10, deprecated_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "wp_get_sites()")
    global wpdb_
    php_check_if_defined("wpdb_")
    blogs_ = wpdb_.get_results(wpdb_.prepare(str("SELECT blog_id, domain, path FROM ") + str(wpdb_.blogs) + str(" WHERE site_id = %d AND public = '1' AND archived = '0' AND mature = '0' AND spam = '0' AND deleted = '0' ORDER BY registered DESC"), get_current_network_id()), ARRAY_A)
    blog_list_ = Array()
    for details_ in blogs_:
        blog_list_[details_["blog_id"]] = details_
        blog_list_[details_["blog_id"]]["postcount"] = wpdb_.get_var("SELECT COUNT(ID) FROM " + wpdb_.get_blog_prefix(details_["blog_id"]) + "posts WHERE post_status='publish' AND post_type='post'")
    # end for
    if (not blog_list_):
        return Array()
    # end if
    if num_ == "all":
        return php_array_slice(blog_list_, start_, php_count(blog_list_))
    else:
        return php_array_slice(blog_list_, start_, num_)
    # end if
# end def get_blog_list
#// 
#// Deprecated functionality to retrieve a list of the most active sites.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.0.0
#// 
#// @param int  $num     Optional. Number of activate blogs to retrieve. Default 10.
#// @param bool $display Optional. Whether or not to display the most active blogs list. Default true.
#// @return array List of "most active" sites.
#//
def get_most_active_blogs(num_=10, display_=None, *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "3.0.0")
    blogs_ = get_blog_list(0, "all", False)
    #// $blog_id -> $details
    if php_is_array(blogs_):
        reset(blogs_)
        most_active_ = Array()
        blog_list_ = Array()
        for key_,details_ in blogs_:
            most_active_[details_["blog_id"]] = details_["postcount"]
            blog_list_[details_["blog_id"]] = details_
            pass
        # end for
        arsort(most_active_)
        reset(most_active_)
        t_ = Array()
        for key_,details_ in most_active_:
            t_[key_] = blog_list_[key_]
        # end for
        most_active_ = None
        most_active_ = t_
    # end if
    if display_:
        if php_is_array(most_active_):
            reset(most_active_)
            for key_,details_ in most_active_:
                url_ = esc_url("http://" + details_["domain"] + details_["path"])
                php_print("<li>" + details_["postcount"] + str(" <a href='") + str(url_) + str("'>") + str(url_) + str("</a></li>"))
            # end for
        # end if
    # end if
    return php_array_slice(most_active_, 0, num_)
# end def get_most_active_blogs
#// 
#// Redirect a user based on $_GET or $_POST arguments.
#// 
#// The function looks for redirect arguments in the following order:
#// 1) $_GET['ref']
#// 2) $_POST['ref']
#// 3) $_SERVER['HTTP_REFERER']
#// 4) $_GET['redirect']
#// 5) $_POST['redirect']
#// 6) $url
#// 
#// @since MU (3.0.0)
#// @deprecated 3.3.0 Use wp_redirect()
#// @see wp_redirect()
#// 
#// @param string $url Optional. Redirect URL. Default empty.
#//
def wpmu_admin_do_redirect(url_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_redirect()")
    ref_ = ""
    if (php_isset(lambda : PHP_REQUEST["ref"])) and (php_isset(lambda : PHP_POST["ref"])) and PHP_REQUEST["ref"] != PHP_POST["ref"]:
        wp_die(__("A variable mismatch has been detected."), __("Sorry, you are not allowed to view this item."), 400)
    elif (php_isset(lambda : PHP_POST["ref"])):
        ref_ = PHP_POST["ref"]
    elif (php_isset(lambda : PHP_REQUEST["ref"])):
        ref_ = PHP_REQUEST["ref"]
    # end if
    if ref_:
        ref_ = wpmu_admin_redirect_add_updated_param(ref_)
        wp_redirect(ref_)
        php_exit(0)
    # end if
    if (not php_empty(lambda : PHP_SERVER["HTTP_REFERER"])):
        wp_redirect(PHP_SERVER["HTTP_REFERER"])
        php_exit(0)
    # end if
    url_ = wpmu_admin_redirect_add_updated_param(url_)
    if (php_isset(lambda : PHP_REQUEST["redirect"])) and (php_isset(lambda : PHP_POST["redirect"])) and PHP_REQUEST["redirect"] != PHP_POST["redirect"]:
        wp_die(__("A variable mismatch has been detected."), __("Sorry, you are not allowed to view this item."), 400)
    elif (php_isset(lambda : PHP_REQUEST["redirect"])):
        if php_substr(PHP_REQUEST["redirect"], 0, 2) == "s_":
            url_ += "&action=blogs&s=" + esc_html(php_substr(PHP_REQUEST["redirect"], 2))
        # end if
    elif (php_isset(lambda : PHP_POST["redirect"])):
        url_ = wpmu_admin_redirect_add_updated_param(PHP_POST["redirect"])
    # end if
    wp_redirect(url_)
    php_exit(0)
# end def wpmu_admin_do_redirect
#// 
#// Adds an 'updated=true' argument to a URL.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.3.0 Use add_query_arg()
#// @see add_query_arg()
#// 
#// @param string $url Optional. Redirect URL. Default empty.
#// @return string
#//
def wpmu_admin_redirect_add_updated_param(url_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0", "add_query_arg()")
    if php_strpos(url_, "updated=true") == False:
        if php_strpos(url_, "?") == False:
            return url_ + "?updated=true"
        else:
            return url_ + "&updated=true"
        # end if
    # end if
    return url_
# end def wpmu_admin_redirect_add_updated_param
#// 
#// Get a numeric user ID from either an email address or a login.
#// 
#// A numeric string is considered to be an existing user ID
#// and is simply returned as such.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.6.0 Use get_user_by()
#// @see get_user_by()
#// 
#// @param string $string Either an email address or a login.
#// @return int
#//
def get_user_id_from_string(string_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.6.0", "get_user_by()")
    if is_email(string_):
        user_ = get_user_by("email", string_)
    elif php_is_numeric(string_):
        return string_
    else:
        user_ = get_user_by("login", string_)
    # end if
    if user_:
        return user_.ID
    # end if
    return 0
# end def get_user_id_from_string
#// 
#// Get a full blog URL, given a domain and a path.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.7.0
#// 
#// @param string $domain
#// @param string $path
#// @return string
#//
def get_blogaddress_by_domain(domain_=None, path_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.7.0")
    if is_subdomain_install():
        url_ = "http://" + domain_ + path_
    else:
        if domain_ != PHP_SERVER["HTTP_HOST"]:
            blogname_ = php_substr(domain_, 0, php_strpos(domain_, "."))
            url_ = "http://" + php_substr(domain_, php_strpos(domain_, ".") + 1) + path_
            #// We're not installing the main blog.
            if blogname_ != "www.":
                url_ += blogname_ + "/"
            # end if
        else:
            #// Main blog.
            url_ = "http://" + domain_ + path_
        # end if
    # end if
    return esc_url_raw(url_)
# end def get_blogaddress_by_domain
#// 
#// Create an empty blog.
#// 
#// @since MU (3.0.0)
#// @deprecated 4.4.0
#// 
#// @param string $domain       The new blog's domain.
#// @param string $path         The new blog's path.
#// @param string $weblog_title The new blog's title.
#// @param int    $site_id      Optional. Defaults to 1.
#// @return string|int The ID of the newly created blog
#//
def create_empty_blog(domain_=None, path_=None, weblog_title_=None, site_id_=1, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.4.0")
    if php_empty(lambda : path_):
        path_ = "/"
    # end if
    #// Check if the domain has been used already. We should return an error message.
    if domain_exists(domain_, path_, site_id_):
        return __("<strong>Error</strong>: Site URL already taken.")
    # end if
    #// 
    #// Need to back up wpdb table names, and create a new wp_blogs entry for new blog.
    #// Need to get blog_id from wp_blogs, and create new table names.
    #// Must restore table names at the end of function.
    #//
    blog_id_ = insert_blog(domain_, path_, site_id_)
    if (not blog_id_):
        return __("<strong>Error</strong>: Problem creating site entry.")
    # end if
    switch_to_blog(blog_id_)
    install_blog(blog_id_)
    restore_current_blog()
    return blog_id_
# end def create_empty_blog
#// 
#// Get the admin for a domain/path combination.
#// 
#// @since MU (3.0.0)
#// @deprecated 4.4.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $domain Optional. Network domain.
#// @param string $path   Optional. Network path.
#// @return array|false The network admins.
#//
def get_admin_users_for_domain(domain_="", path_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.4.0")
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not domain_):
        network_id_ = get_current_network_id()
    else:
        _networks_ = get_networks(Array({"fields": "ids", "number": 1, "domain": domain_, "path": path_}))
        network_id_ = php_array_shift(_networks_) if (not php_empty(lambda : _networks_)) else 0
    # end if
    if network_id_:
        return wpdb_.get_results(wpdb_.prepare(str("SELECT u.ID, u.user_login, u.user_pass FROM ") + str(wpdb_.users) + str(" AS u, ") + str(wpdb_.sitemeta) + str(" AS sm WHERE sm.meta_key = 'admin_user_id' AND u.ID = sm.meta_value AND sm.site_id = %d"), network_id_), ARRAY_A)
    # end if
    return False
# end def get_admin_users_for_domain
#// 
#// Return an array of sites for a network or networks.
#// 
#// @since 3.7.0
#// @deprecated 4.6.0 Use get_sites()
#// @see get_sites()
#// 
#// @param array $args {
#// Array of default arguments. Optional.
#// 
#// @type int|array $network_id A network ID or array of network IDs. Set to null to retrieve sites
#// from all networks. Defaults to current network ID.
#// @type int       $public     Retrieve public or non-public sites. Default null, for any.
#// @type int       $archived   Retrieve archived or non-archived sites. Default null, for any.
#// @type int       $mature     Retrieve mature or non-mature sites. Default null, for any.
#// @type int       $spam       Retrieve spam or non-spam sites. Default null, for any.
#// @type int       $deleted    Retrieve deleted or non-deleted sites. Default null, for any.
#// @type int       $limit      Number of sites to limit the query to. Default 100.
#// @type int       $offset     Exclude the first x sites. Used in combination with the $limit parameter. Default 0.
#// }
#// @return array[] An empty array if the installation is considered "large" via wp_is_large_network(). Otherwise,
#// an associative array of WP_Site data as arrays.
#//
def wp_get_sites(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    _deprecated_function(__FUNCTION__, "4.6.0", "get_sites()")
    if wp_is_large_network():
        return Array()
    # end if
    defaults_ = Array({"network_id": get_current_network_id(), "public": None, "archived": None, "mature": None, "spam": None, "deleted": None, "limit": 100, "offset": 0})
    args_ = wp_parse_args(args_, defaults_)
    #// Backward compatibility.
    if php_is_array(args_["network_id"]):
        args_["network__in"] = args_["network_id"]
        args_["network_id"] = None
    # end if
    if php_is_numeric(args_["limit"]):
        args_["number"] = args_["limit"]
        args_["limit"] = None
    elif (not args_["limit"]):
        args_["number"] = 0
        args_["limit"] = None
    # end if
    #// Make sure count is disabled.
    args_["count"] = False
    _sites_ = get_sites(args_)
    results_ = Array()
    for _site_ in _sites_:
        _site_ = get_site(_site_)
        results_[-1] = _site_.to_array()
    # end for
    return results_
# end def wp_get_sites
#// 
#// Check whether a usermeta key has to do with the current blog.
#// 
#// @since MU (3.0.0)
#// @deprecated 4.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $key
#// @param int    $user_id Optional. Defaults to current user.
#// @param int    $blog_id Optional. Defaults to current blog.
#// @return bool
#//
def is_user_option_local(key_=None, user_id_=0, blog_id_=0, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    _deprecated_function(__FUNCTION__, "4.9.0")
    current_user_ = wp_get_current_user()
    if blog_id_ == 0:
        blog_id_ = get_current_blog_id()
    # end if
    local_key_ = wpdb_.get_blog_prefix(blog_id_) + key_
    return (php_isset(lambda : current_user_.local_key_))
# end def is_user_option_local
#// 
#// Store basic site info in the blogs table.
#// 
#// This function creates a row in the wp_blogs table and returns
#// the new blog's ID. It is the first step in creating a new blog.
#// 
#// @since MU (3.0.0)
#// @deprecated 5.1.0 Use `wp_insert_site()`
#// @see wp_insert_site()
#// 
#// @param string $domain  The domain of the new site.
#// @param string $path    The path of the new site.
#// @param int    $site_id Unless you're running a multi-network install, be sure to set this value to 1.
#// @return int|false The ID of the new row
#//
def insert_blog(domain_=None, path_=None, site_id_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "5.1.0", "wp_insert_site()")
    data_ = Array({"domain": domain_, "path": path_, "site_id": site_id_})
    site_id_ = wp_insert_site(data_)
    if is_wp_error(site_id_):
        return False
    # end if
    clean_blog_cache(site_id_)
    return site_id_
# end def insert_blog
#// 
#// Install an empty blog.
#// 
#// Creates the new blog tables and options. If calling this function
#// directly, be sure to use switch_to_blog() first, so that $wpdb
#// points to the new blog.
#// 
#// @since MU (3.0.0)
#// @deprecated 5.1.0
#// 
#// @global wpdb     $wpdb     WordPress database abstraction object.
#// @global WP_Roles $wp_roles WordPress role management object.
#// 
#// @param int    $blog_id    The value returned by wp_insert_site().
#// @param string $blog_title The title of the new site.
#//
def install_blog(blog_id_=None, blog_title_="", *_args_):
    
    
    global wpdb_
    global wp_roles_
    php_check_if_defined("wpdb_","wp_roles_")
    _deprecated_function(__FUNCTION__, "5.1.0")
    #// Cast for security.
    blog_id_ = php_int(blog_id_)
    php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
    suppress_ = wpdb_.suppress_errors()
    if wpdb_.get_results(str("DESCRIBE ") + str(wpdb_.posts)):
        php_print("<h1>" + __("Already Installed") + "</h1><p>" + __("You appear to have already installed WordPress. To reinstall please clear your old database tables first.") + "</p></body></html>")
        php_exit()
    # end if
    wpdb_.suppress_errors(suppress_)
    url_ = get_blogaddress_by_id(blog_id_)
    #// Set everything up.
    make_db_current_silent("blog")
    populate_options()
    populate_roles()
    #// populate_roles() clears previous role definitions so we start over.
    wp_roles_ = php_new_class("WP_Roles", lambda : WP_Roles())
    siteurl_ = home_ = untrailingslashit(url_)
    if (not is_subdomain_install()):
        if "https" == php_parse_url(get_site_option("siteurl"), PHP_URL_SCHEME):
            siteurl_ = set_url_scheme(siteurl_, "https")
        # end if
        if "https" == php_parse_url(get_home_url(get_network().site_id), PHP_URL_SCHEME):
            home_ = set_url_scheme(home_, "https")
        # end if
    # end if
    update_option("siteurl", siteurl_)
    update_option("home", home_)
    if get_site_option("ms_files_rewriting"):
        update_option("upload_path", UPLOADBLOGSDIR + str("/") + str(blog_id_) + str("/files"))
    else:
        update_option("upload_path", get_blog_option(get_network().site_id, "upload_path"))
    # end if
    update_option("blogname", wp_unslash(blog_title_))
    update_option("admin_email", "")
    #// Remove all permissions.
    table_prefix_ = wpdb_.get_blog_prefix()
    delete_metadata("user", 0, table_prefix_ + "user_level", None, True)
    #// Delete all.
    delete_metadata("user", 0, table_prefix_ + "capabilities", None, True)
    pass
# end def install_blog
#// 
#// Set blog defaults.
#// 
#// This function creates a row in the wp_blogs table.
#// 
#// @since MU (3.0.0)
#// @deprecated MU
#// @deprecated Use wp_install_defaults()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $blog_id Ignored in this function.
#// @param int $user_id
#//
def install_blog_defaults(blog_id_=None, user_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    _deprecated_function(__FUNCTION__, "MU")
    php_include_file(ABSPATH + "wp-admin/includes/upgrade.php", once=True)
    suppress_ = wpdb_.suppress_errors()
    wp_install_defaults(user_id_)
    wpdb_.suppress_errors(suppress_)
# end def install_blog_defaults
#// 
#// Update the status of a user in the database.
#// 
#// Previously used in core to mark a user as spam or "ham" (not spam) in Multisite.
#// 
#// @since 3.0.0
#// @deprecated 5.3.0 Use wp_update_user()
#// @see wp_update_user()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $id         The user ID.
#// @param string $pref       The column in the wp_users table to update the user's status
#// in (presumably user_status, spam, or deleted).
#// @param int    $value      The new status for the user.
#// @param null   $deprecated Deprecated as of 3.0.2 and should not be used.
#// @return int   The initially passed $value.
#//
def update_user_status(id_=None, pref_=None, value_=None, deprecated_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    _deprecated_function(__FUNCTION__, "5.3.0", "wp_update_user()")
    if None != deprecated_:
        _deprecated_argument(__FUNCTION__, "3.0.2")
    # end if
    wpdb_.update(wpdb_.users, Array({sanitize_key(pref_): value_}), Array({"ID": id_}))
    user_ = php_new_class("WP_User", lambda : WP_User(id_))
    clean_user_cache(user_)
    if pref_ == "spam":
        if value_ == 1:
            #// This filter is documented in wp-includes/user.php
            do_action("make_spam_user", id_)
        else:
            #// This filter is documented in wp-includes/user.php
            do_action("make_ham_user", id_)
        # end if
    # end if
    return value_
# end def update_user_status
