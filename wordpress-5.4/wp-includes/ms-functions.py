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
#// Multisite WordPress API
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// 
#// Gets the network's site and user counts.
#// 
#// @since MU (3.0.0)
#// 
#// @return int[] {
#// Site and user count for the network.
#// 
#// @type int $blogs Number of sites on the network.
#// @type int $users Number of users on the network.
#// }
#//
def get_sitestats(*args_):
    
    stats = Array({"blogs": get_blog_count(), "users": get_user_count()})
    return stats
# end def get_sitestats
#// 
#// Get one of a user's active blogs
#// 
#// Returns the user's primary blog, if they have one and
#// it is active. If it's inactive, function returns another
#// active blog of the user. If none are found, the user
#// is added as a Subscriber to the Dashboard Blog and that blog
#// is returned.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $user_id The unique ID of the user
#// @return WP_Site|void The blog object
#//
def get_active_blog_for_user(user_id=None, *args_):
    
    blogs = get_blogs_of_user(user_id)
    if php_empty(lambda : blogs):
        return
    # end if
    if (not is_multisite()):
        return blogs[get_current_blog_id()]
    # end if
    primary_blog = get_user_meta(user_id, "primary_blog", True)
    first_blog = current(blogs)
    if False != primary_blog:
        if (not (php_isset(lambda : blogs[primary_blog]))):
            update_user_meta(user_id, "primary_blog", first_blog.userblog_id)
            primary = get_site(first_blog.userblog_id)
        else:
            primary = get_site(primary_blog)
        # end if
    else:
        #// TODO: Review this call to add_user_to_blog too - to get here the user must have a role on this blog?
        result = add_user_to_blog(first_blog.userblog_id, user_id, "subscriber")
        if (not is_wp_error(result)):
            update_user_meta(user_id, "primary_blog", first_blog.userblog_id)
            primary = first_blog
        # end if
    # end if
    if (not php_is_object(primary)) or 1 == primary.archived or 1 == primary.spam or 1 == primary.deleted:
        blogs = get_blogs_of_user(user_id, True)
        #// If a user's primary blog is shut down, check their other blogs.
        ret = False
        if php_is_array(blogs) and php_count(blogs) > 0:
            for blog_id,blog in blogs:
                if get_current_network_id() != blog.site_id:
                    continue
                # end if
                details = get_site(blog_id)
                if php_is_object(details) and 0 == details.archived and 0 == details.spam and 0 == details.deleted:
                    ret = details
                    if get_user_meta(user_id, "primary_blog", True) != blog_id:
                        update_user_meta(user_id, "primary_blog", blog_id)
                    # end if
                    if (not get_user_meta(user_id, "source_domain", True)):
                        update_user_meta(user_id, "source_domain", details.domain)
                    # end if
                    break
                # end if
            # end for
        else:
            return
        # end if
        return ret
    else:
        return primary
    # end if
# end def get_active_blog_for_user
#// 
#// The number of active users in your installation.
#// 
#// The count is cached and updated twice daily. This is not a live count.
#// 
#// @since MU (3.0.0)
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#// @return int Number of active users on the network.
#//
def get_user_count(network_id=None, *args_):
    
    return get_network_option(network_id, "user_count")
# end def get_user_count
#// 
#// The number of active sites on your installation.
#// 
#// The count is cached and updated twice daily. This is not a live count.
#// 
#// @since MU (3.0.0)
#// @since 3.7.0 The `$network_id` parameter has been deprecated.
#// @since 4.8.0 The `$network_id` parameter is now being used.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#// @return int Number of active sites on the network.
#//
def get_blog_count(network_id=None, *args_):
    
    return get_network_option(network_id, "blog_count")
# end def get_blog_count
#// 
#// Get a blog post from any site on the network.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $blog_id ID of the blog.
#// @param int $post_id ID of the post being looked for.
#// @return WP_Post|null WP_Post on success or null on failure
#//
def get_blog_post(blog_id=None, post_id=None, *args_):
    
    switch_to_blog(blog_id)
    post = get_post(post_id)
    restore_current_blog()
    return post
# end def get_blog_post
#// 
#// Adds a user to a blog.
#// 
#// Use the {@see 'add_user_to_blog'} action to fire an event when users are added to a blog.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $blog_id ID of the blog the user is being added to.
#// @param int    $user_id ID of the user being added.
#// @param string $role    The role you want the user to have
#// @return true|WP_Error True on success or a WP_Error object if the user doesn't exist
#// or could not be added.
#//
def add_user_to_blog(blog_id=None, user_id=None, role=None, *args_):
    
    switch_to_blog(blog_id)
    user = get_userdata(user_id)
    if (not user):
        restore_current_blog()
        return php_new_class("WP_Error", lambda : WP_Error("user_does_not_exist", __("The requested user does not exist.")))
    # end if
    #// 
    #// Filters whether a user should be added to a site.
    #// 
    #// @since 4.9.0
    #// 
    #// @param bool|WP_Error $retval  True if the user should be added to the site, false
    #// or error object otherwise.
    #// @param int           $user_id User ID.
    #// @param string        $role    User role.
    #// @param int           $blog_id Site ID.
    #//
    can_add_user = apply_filters("can_add_user_to_blog", True, user_id, role, blog_id)
    if True != can_add_user:
        restore_current_blog()
        if is_wp_error(can_add_user):
            return can_add_user
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("user_cannot_be_added", __("User cannot be added to this site.")))
    # end if
    if (not get_user_meta(user_id, "primary_blog", True)):
        update_user_meta(user_id, "primary_blog", blog_id)
        site = get_site(blog_id)
        update_user_meta(user_id, "source_domain", site.domain)
    # end if
    user.set_role(role)
    #// 
    #// Fires immediately after a user is added to a site.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int    $user_id User ID.
    #// @param string $role    User role.
    #// @param int    $blog_id Blog ID.
    #//
    do_action("add_user_to_blog", user_id, role, blog_id)
    clean_user_cache(user_id)
    wp_cache_delete(blog_id + "_user_count", "blog-details")
    restore_current_blog()
    return True
# end def add_user_to_blog
#// 
#// Remove a user from a blog.
#// 
#// Use the {@see 'remove_user_from_blog'} action to fire an event when
#// users are removed from a blog.
#// 
#// Accepts an optional `$reassign` parameter, if you want to
#// reassign the user's blog posts to another user upon removal.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $user_id  ID of the user being removed.
#// @param int $blog_id  Optional. ID of the blog the user is being removed from. Default 0.
#// @param int $reassign Optional. ID of the user to whom to reassign posts. Default 0.
#// @return true|WP_Error True on success or a WP_Error object if the user doesn't exist.
#//
def remove_user_from_blog(user_id=None, blog_id=0, reassign=0, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    switch_to_blog(blog_id)
    user_id = php_int(user_id)
    #// 
    #// Fires before a user is removed from a site.
    #// 
    #// @since MU (3.0.0)
    #// @since 5.4.0 Added the `$reassign` parameter.
    #// 
    #// @param int $user_id  ID of the user being removed.
    #// @param int $blog_id  ID of the blog the user is being removed from.
    #// @param int $reassign ID of the user to whom to reassign posts.
    #//
    do_action("remove_user_from_blog", user_id, blog_id, reassign)
    #// If being removed from the primary blog, set a new primary
    #// if the user is assigned to multiple blogs.
    primary_blog = get_user_meta(user_id, "primary_blog", True)
    if primary_blog == blog_id:
        new_id = ""
        new_domain = ""
        blogs = get_blogs_of_user(user_id)
        for blog in blogs:
            if blog.userblog_id == blog_id:
                continue
            # end if
            new_id = blog.userblog_id
            new_domain = blog.domain
            break
        # end for
        update_user_meta(user_id, "primary_blog", new_id)
        update_user_meta(user_id, "source_domain", new_domain)
    # end if
    #// wp_revoke_user( $user_id );
    user = get_userdata(user_id)
    if (not user):
        restore_current_blog()
        return php_new_class("WP_Error", lambda : WP_Error("user_does_not_exist", __("That user does not exist.")))
    # end if
    user.remove_all_caps()
    blogs = get_blogs_of_user(user_id)
    if php_count(blogs) == 0:
        update_user_meta(user_id, "primary_blog", "")
        update_user_meta(user_id, "source_domain", "")
    # end if
    if reassign:
        reassign = php_int(reassign)
        post_ids = wpdb.get_col(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_author = %d"), user_id))
        link_ids = wpdb.get_col(wpdb.prepare(str("SELECT link_id FROM ") + str(wpdb.links) + str(" WHERE link_owner = %d"), user_id))
        if (not php_empty(lambda : post_ids)):
            wpdb.query(wpdb.prepare(str("UPDATE ") + str(wpdb.posts) + str(" SET post_author = %d WHERE post_author = %d"), reassign, user_id))
            array_walk(post_ids, "clean_post_cache")
        # end if
        if (not php_empty(lambda : link_ids)):
            wpdb.query(wpdb.prepare(str("UPDATE ") + str(wpdb.links) + str(" SET link_owner = %d WHERE link_owner = %d"), reassign, user_id))
            array_walk(link_ids, "clean_bookmark_cache")
        # end if
    # end if
    restore_current_blog()
    return True
# end def remove_user_from_blog
#// 
#// Get the permalink for a post on another blog.
#// 
#// @since MU (3.0.0) 1.0
#// 
#// @param int $blog_id ID of the source blog.
#// @param int $post_id ID of the desired post.
#// @return string The post's permalink
#//
def get_blog_permalink(blog_id=None, post_id=None, *args_):
    
    switch_to_blog(blog_id)
    link = get_permalink(post_id)
    restore_current_blog()
    return link
# end def get_blog_permalink
#// 
#// Get a blog's numeric ID from its URL.
#// 
#// On a subdirectory installation like example.com/blog1/,
#// $domain will be the root 'example.com' and $path the
#// subdirectory '/blog1/'. With subdomains like blog1.example.com,
#// $domain is 'blog1.example.com' and $path is '/'.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $domain
#// @param string $path   Optional. Not required for subdomain installations.
#// @return int 0 if no blog found, otherwise the ID of the matching blog
#//
def get_blog_id_from_url(domain=None, path="/", *args_):
    
    domain = php_strtolower(domain)
    path = php_strtolower(path)
    id = wp_cache_get(php_md5(domain + path), "blog-id-cache")
    if -1 == id:
        #// Blog does not exist.
        return 0
    elif id:
        return php_int(id)
    # end if
    args = Array({"domain": domain, "path": path, "fields": "ids", "number": 1, "update_site_meta_cache": False})
    result = get_sites(args)
    id = php_array_shift(result)
    if (not id):
        wp_cache_set(php_md5(domain + path), -1, "blog-id-cache")
        return 0
    # end if
    wp_cache_set(php_md5(domain + path), id, "blog-id-cache")
    return id
# end def get_blog_id_from_url
#// 
#// Admin functions.
#// 
#// 
#// Checks an email address against a list of banned domains.
#// 
#// This function checks against the Banned Email Domains list
#// at wp-admin/network/settings.php. The check is only run on
#// self-registrations; user creation at wp-admin/network/users.php
#// bypasses this check.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $user_email The email provided by the user at registration.
#// @return bool Returns true when the email address is banned.
#//
def is_email_address_unsafe(user_email=None, *args_):
    
    banned_names = get_site_option("banned_email_domains")
    if banned_names and (not php_is_array(banned_names)):
        banned_names = php_explode("\n", banned_names)
    # end if
    is_email_address_unsafe = False
    if banned_names and php_is_array(banned_names) and False != php_strpos(user_email, "@", 1):
        banned_names = php_array_map("strtolower", banned_names)
        normalized_email = php_strtolower(user_email)
        email_local_part, email_domain = php_explode("@", normalized_email)
        for banned_domain in banned_names:
            if (not banned_domain):
                continue
            # end if
            if email_domain == banned_domain:
                is_email_address_unsafe = True
                break
            # end if
            dotted_domain = str(".") + str(banned_domain)
            if php_substr(normalized_email, -php_strlen(dotted_domain)) == dotted_domain:
                is_email_address_unsafe = True
                break
            # end if
        # end for
    # end if
    #// 
    #// Filters whether an email address is unsafe.
    #// 
    #// @since 3.5.0
    #// 
    #// @param bool   $is_email_address_unsafe Whether the email address is "unsafe". Default false.
    #// @param string $user_email              User email address.
    #//
    return apply_filters("is_email_address_unsafe", is_email_address_unsafe, user_email)
# end def is_email_address_unsafe
#// 
#// Sanitize and validate data required for a user sign-up.
#// 
#// Verifies the validity and uniqueness of user names and user email addresses,
#// and checks email addresses against admin-provided domain whitelists and blacklists.
#// 
#// The {@see 'wpmu_validate_user_signup'} hook provides an easy way to modify the sign-up
#// process. The value $result, which is passed to the hook, contains both the user-provided
#// info and the error messages created by the function. {@see 'wpmu_validate_user_signup'}
#// allows you to process the data in any way you'd like, and unset the relevant errors if
#// necessary.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $user_name  The login name provided by the user.
#// @param string $user_email The email provided by the user.
#// @return array {
#// The array of user name, email, and the error messages.
#// 
#// @type string   $user_name     Sanitized and unique username.
#// @type string   $orig_username Original username.
#// @type string   $user_email    User email address.
#// @type WP_Error $errors        WP_Error object containing any errors found.
#// }
#//
def wpmu_validate_user_signup(user_name=None, user_email=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    errors = php_new_class("WP_Error", lambda : WP_Error())
    orig_username = user_name
    user_name = php_preg_replace("/\\s+/", "", sanitize_user(user_name, True))
    if user_name != orig_username or php_preg_match("/[^a-z0-9]/", user_name):
        errors.add("user_name", __("Usernames can only contain lowercase letters (a-z) and numbers."))
        user_name = orig_username
    # end if
    user_email = sanitize_email(user_email)
    if php_empty(lambda : user_name):
        errors.add("user_name", __("Please enter a username."))
    # end if
    illegal_names = get_site_option("illegal_names")
    if (not php_is_array(illegal_names)):
        illegal_names = Array("www", "web", "root", "admin", "main", "invite", "administrator")
        add_site_option("illegal_names", illegal_names)
    # end if
    if php_in_array(user_name, illegal_names):
        errors.add("user_name", __("Sorry, that username is not allowed."))
    # end if
    #// This filter is documented in wp-includes/user.php
    illegal_logins = apply_filters("illegal_user_logins", Array())
    if php_in_array(php_strtolower(user_name), php_array_map("strtolower", illegal_logins), True):
        errors.add("user_name", __("Sorry, that username is not allowed."))
    # end if
    if (not is_email(user_email)):
        errors.add("user_email", __("Please enter a valid email address."))
    elif is_email_address_unsafe(user_email):
        errors.add("user_email", __("You cannot use that email address to signup. We are having problems with them blocking some of our email. Please use another email provider."))
    # end if
    if php_strlen(user_name) < 4:
        errors.add("user_name", __("Username must be at least 4 characters."))
    # end if
    if php_strlen(user_name) > 60:
        errors.add("user_name", __("Username may not be longer than 60 characters."))
    # end if
    #// All numeric?
    if php_preg_match("/^[0-9]*$/", user_name):
        errors.add("user_name", __("Sorry, usernames must have letters too!"))
    # end if
    limited_email_domains = get_site_option("limited_email_domains")
    if php_is_array(limited_email_domains) and (not php_empty(lambda : limited_email_domains)):
        limited_email_domains = php_array_map("strtolower", limited_email_domains)
        emaildomain = php_strtolower(php_substr(user_email, 1 + php_strpos(user_email, "@")))
        if (not php_in_array(emaildomain, limited_email_domains, True)):
            errors.add("user_email", __("Sorry, that email address is not allowed!"))
        # end if
    # end if
    #// Check if the username has been used already.
    if username_exists(user_name):
        errors.add("user_name", __("Sorry, that username already exists!"))
    # end if
    #// Check if the email address has been used already.
    if email_exists(user_email):
        errors.add("user_email", __("Sorry, that email address is already used!"))
    # end if
    #// Has someone already signed up for this username?
    signup = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.signups) + str(" WHERE user_login = %s"), user_name))
    if None != signup:
        registered_at = mysql2date("U", signup.registered)
        now = time()
        diff = now - registered_at
        #// If registered more than two days ago, cancel registration and let this signup go through.
        if diff > 2 * DAY_IN_SECONDS:
            wpdb.delete(wpdb.signups, Array({"user_login": user_name}))
        else:
            errors.add("user_name", __("That username is currently reserved but may be available in a couple of days."))
        # end if
    # end if
    signup = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.signups) + str(" WHERE user_email = %s"), user_email))
    if None != signup:
        diff = time() - mysql2date("U", signup.registered)
        #// If registered more than two days ago, cancel registration and let this signup go through.
        if diff > 2 * DAY_IN_SECONDS:
            wpdb.delete(wpdb.signups, Array({"user_email": user_email}))
        else:
            errors.add("user_email", __("That email address has already been used. Please check your inbox for an activation email. It will become available in a couple of days if you do nothing."))
        # end if
    # end if
    result = Array({"user_name": user_name, "orig_username": orig_username, "user_email": user_email, "errors": errors})
    #// 
    #// Filters the validated user registration details.
    #// 
    #// This does not allow you to override the username or email of the user during
    #// registration. The values are solely used for validation and error handling.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param array $result {
    #// The array of user name, email, and the error messages.
    #// 
    #// @type string   $user_name     Sanitized and unique username.
    #// @type string   $orig_username Original username.
    #// @type string   $user_email    User email address.
    #// @type WP_Error $errors        WP_Error object containing any errors found.
    #// }
    #//
    return apply_filters("wpmu_validate_user_signup", result)
# end def wpmu_validate_user_signup
#// 
#// Processes new site registrations.
#// 
#// Checks the data provided by the user during blog signup. Verifies
#// the validity and uniqueness of blog paths and domains.
#// 
#// This function prevents the current user from registering a new site
#// with a blogname equivalent to another user's login name. Passing the
#// $user parameter to the function, where $user is the other user, is
#// effectively an override of this limitation.
#// 
#// Filter {@see 'wpmu_validate_blog_signup'} if you want to modify
#// the way that WordPress validates new site signups.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb   $wpdb   WordPress database abstraction object.
#// @global string $domain
#// 
#// @param string         $blogname   The blog name provided by the user. Must be unique.
#// @param string         $blog_title The blog title provided by the user.
#// @param WP_User|string $user       Optional. The user object to check against the new site name.
#// @return array {
#// Array of domain, path, blog name, blog title, user and error messages.
#// 
#// @type string         $domain     Domain for the site.
#// @type string         $path       Path for the site. Used in subdirectory installations.
#// @type string         $blogname   The unique site name (slug).
#// @type string         $blog_title Blog title.
#// @type string|WP_User $user       By default, an empty string. A user object if provided.
#// @type WP_Error       $errors     WP_Error containing any errors found.
#// }
#//
def wpmu_validate_blog_signup(blogname=None, blog_title=None, user="", *args_):
    
    global wpdb,domain
    php_check_if_defined("wpdb","domain")
    current_network = get_network()
    base = current_network.path
    blog_title = strip_tags(blog_title)
    errors = php_new_class("WP_Error", lambda : WP_Error())
    illegal_names = get_site_option("illegal_names")
    if False == illegal_names:
        illegal_names = Array("www", "web", "root", "admin", "main", "invite", "administrator")
        add_site_option("illegal_names", illegal_names)
    # end if
    #// 
    #// On sub dir installations, some names are so illegal, only a filter can
    #// spring them from jail.
    #//
    if (not is_subdomain_install()):
        illegal_names = php_array_merge(illegal_names, get_subdirectory_reserved_names())
    # end if
    if php_empty(lambda : blogname):
        errors.add("blogname", __("Please enter a site name."))
    # end if
    if php_preg_match("/[^a-z0-9]+/", blogname):
        errors.add("blogname", __("Site names can only contain lowercase letters (a-z) and numbers."))
    # end if
    if php_in_array(blogname, illegal_names):
        errors.add("blogname", __("That name is not allowed."))
    # end if
    #// 
    #// Filters the minimum site name length required when validating a site signup.
    #// 
    #// @since 4.8.0
    #// 
    #// @param int $length The minimum site name length. Default 4.
    #//
    minimum_site_name_length = apply_filters("minimum_site_name_length", 4)
    if php_strlen(blogname) < minimum_site_name_length:
        #// translators: %s: Minimum site name length.
        errors.add("blogname", php_sprintf(_n("Site name must be at least %s character.", "Site name must be at least %s characters.", minimum_site_name_length), number_format_i18n(minimum_site_name_length)))
    # end if
    #// Do not allow users to create a blog that conflicts with a page on the main blog.
    if (not is_subdomain_install()) and wpdb.get_var(wpdb.prepare("SELECT post_name FROM " + wpdb.get_blog_prefix(current_network.site_id) + "posts WHERE post_type = 'page' AND post_name = %s", blogname)):
        errors.add("blogname", __("Sorry, you may not use that site name."))
    # end if
    #// All numeric?
    if php_preg_match("/^[0-9]*$/", blogname):
        errors.add("blogname", __("Sorry, site names must have letters too!"))
    # end if
    #// 
    #// Filters the new site name during registration.
    #// 
    #// The name is the site's subdomain or the site's subdirectory
    #// path depending on the network settings.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $blogname Site name.
    #//
    blogname = apply_filters("newblogname", blogname)
    blog_title = wp_unslash(blog_title)
    if php_empty(lambda : blog_title):
        errors.add("blog_title", __("Please enter a site title."))
    # end if
    #// Check if the domain/path has been used already.
    if is_subdomain_install():
        mydomain = blogname + "." + php_preg_replace("|^www\\.|", "", domain)
        path = base
    else:
        mydomain = str(domain)
        path = base + blogname + "/"
    # end if
    if domain_exists(mydomain, path, current_network.id):
        errors.add("blogname", __("Sorry, that site already exists!"))
    # end if
    if username_exists(blogname):
        if (not php_is_object(user)) or php_is_object(user) and user.user_login != blogname:
            errors.add("blogname", __("Sorry, that site is reserved!"))
        # end if
    # end if
    #// Has someone already signed up for this domain?
    #// TODO: Check email too?
    signup = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.signups) + str(" WHERE domain = %s AND path = %s"), mydomain, path))
    if (not php_empty(lambda : signup)):
        diff = time() - mysql2date("U", signup.registered)
        #// If registered more than two days ago, cancel registration and let this signup go through.
        if diff > 2 * DAY_IN_SECONDS:
            wpdb.delete(wpdb.signups, Array({"domain": mydomain, "path": path}))
        else:
            errors.add("blogname", __("That site is currently reserved but may be available in a couple days."))
        # end if
    # end if
    result = Array({"domain": mydomain, "path": path, "blogname": blogname, "blog_title": blog_title, "user": user, "errors": errors})
    #// 
    #// Filters site details and error messages following registration.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param array $result {
    #// Array of domain, path, blog name, blog title, user and error messages.
    #// 
    #// @type string         $domain     Domain for the site.
    #// @type string         $path       Path for the site. Used in subdirectory installations.
    #// @type string         $blogname   The unique site name (slug).
    #// @type string         $blog_title Blog title.
    #// @type string|WP_User $user       By default, an empty string. A user object if provided.
    #// @type WP_Error       $errors     WP_Error containing any errors found.
    #// }
    #//
    return apply_filters("wpmu_validate_blog_signup", result)
# end def wpmu_validate_blog_signup
#// 
#// Record site signup information for future activation.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $domain     The requested domain.
#// @param string $path       The requested path.
#// @param string $title      The requested site title.
#// @param string $user       The user's requested login name.
#// @param string $user_email The user's email address.
#// @param array  $meta       Optional. Signup meta data. By default, contains the requested privacy setting and lang_id.
#//
def wpmu_signup_blog(domain=None, path=None, title=None, user=None, user_email=None, meta=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    key = php_substr(php_md5(time() + wp_rand() + domain), 0, 16)
    #// 
    #// Filters the metadata for a site signup.
    #// 
    #// The metadata will be serialized prior to storing it in the database.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array  $meta       Signup meta data. Default empty array.
    #// @param string $domain     The requested domain.
    #// @param string $path       The requested path.
    #// @param string $title      The requested site title.
    #// @param string $user       The user's requested login name.
    #// @param string $user_email The user's email address.
    #// @param string $key        The user's activation key.
    #//
    meta = apply_filters("signup_site_meta", meta, domain, path, title, user, user_email, key)
    wpdb.insert(wpdb.signups, Array({"domain": domain, "path": path, "title": title, "user_login": user, "user_email": user_email, "registered": current_time("mysql", True), "activation_key": key, "meta": serialize(meta)}))
    #// 
    #// Fires after site signup information has been written to the database.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $domain     The requested domain.
    #// @param string $path       The requested path.
    #// @param string $title      The requested site title.
    #// @param string $user       The user's requested login name.
    #// @param string $user_email The user's email address.
    #// @param string $key        The user's activation key.
    #// @param array  $meta       Signup meta data. By default, contains the requested privacy setting and lang_id.
    #//
    do_action("after_signup_site", domain, path, title, user, user_email, key, meta)
# end def wpmu_signup_blog
#// 
#// Record user signup information for future activation.
#// 
#// This function is used when user registration is open but
#// new site registration is not.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $user       The user's requested login name.
#// @param string $user_email The user's email address.
#// @param array  $meta       Optional. Signup meta data. Default empty array.
#//
def wpmu_signup_user(user=None, user_email=None, meta=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Format data.
    user = php_preg_replace("/\\s+/", "", sanitize_user(user, True))
    user_email = sanitize_email(user_email)
    key = php_substr(php_md5(time() + wp_rand() + user_email), 0, 16)
    #// 
    #// Filters the metadata for a user signup.
    #// 
    #// The metadata will be serialized prior to storing it in the database.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array  $meta       Signup meta data. Default empty array.
    #// @param string $user       The user's requested login name.
    #// @param string $user_email The user's email address.
    #// @param string $key        The user's activation key.
    #//
    meta = apply_filters("signup_user_meta", meta, user, user_email, key)
    wpdb.insert(wpdb.signups, Array({"domain": "", "path": "", "title": "", "user_login": user, "user_email": user_email, "registered": current_time("mysql", True), "activation_key": key, "meta": serialize(meta)}))
    #// 
    #// Fires after a user's signup information has been written to the database.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $user       The user's requested login name.
    #// @param string $user_email The user's email address.
    #// @param string $key        The user's activation key.
    #// @param array  $meta       Signup meta data. Default empty array.
    #//
    do_action("after_signup_user", user, user_email, key, meta)
# end def wpmu_signup_user
#// 
#// Send a confirmation request email to a user when they sign up for a new site. The new site will not become active
#// until the confirmation link is clicked.
#// 
#// This is the notification function used when site registration
#// is enabled.
#// 
#// Filter {@see 'wpmu_signup_blog_notification'} to bypass this function or
#// replace it with your own notification behavior.
#// 
#// Filter {@see 'wpmu_signup_blog_notification_email'} and
#// {@see 'wpmu_signup_blog_notification_subject'} to change the content
#// and subject line of the email sent to newly registered users.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $domain     The new blog domain.
#// @param string $path       The new blog path.
#// @param string $title      The site title.
#// @param string $user_login The user's login name.
#// @param string $user_email The user's email address.
#// @param string $key        The activation key created in wpmu_signup_blog()
#// @param array  $meta       Optional. Signup meta data. By default, contains the requested privacy setting and lang_id.
#// @return bool
#//
def wpmu_signup_blog_notification(domain=None, path=None, title=None, user_login=None, user_email=None, key=None, meta=Array(), *args_):
    
    #// 
    #// Filters whether to bypass the new site email notification.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string|bool $domain     Site domain.
    #// @param string      $path       Site path.
    #// @param string      $title      Site title.
    #// @param string      $user_login User login name.
    #// @param string      $user_email User email address.
    #// @param string      $key        Activation key created in wpmu_signup_blog().
    #// @param array       $meta       Signup meta data. By default, contains the requested privacy setting and lang_id.
    #//
    if (not apply_filters("wpmu_signup_blog_notification", domain, path, title, user_login, user_email, key, meta)):
        return False
    # end if
    #// Send email with activation link.
    if (not is_subdomain_install()) or get_current_network_id() != 1:
        activate_url = network_site_url(str("wp-activate.php?key=") + str(key))
    else:
        activate_url = str("http://") + str(domain) + str(path) + str("wp-activate.php?key=") + str(key)
        pass
    # end if
    activate_url = esc_url(activate_url)
    admin_email = get_site_option("admin_email")
    if "" == admin_email:
        admin_email = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers = str("From: \"") + str(from_name) + str("\" <") + str(admin_email) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    user = get_user_by("login", user_login)
    switched_locale = switch_to_locale(get_user_locale(user))
    message = php_sprintf(apply_filters("wpmu_signup_blog_notification_email", __("""To activate your blog, please click the following link:
    %1$s
    After you activate, you will receive *another email* with your login.
    After you activate, you can visit your site here:
    %2$s"""), domain, path, title, user_login, user_email, key, meta), activate_url, esc_url(str("http://") + str(domain) + str(path)), key)
    subject = php_sprintf(apply_filters("wpmu_signup_blog_notification_subject", _x("[%1$s] Activate %2$s", "New site notification email subject"), domain, path, title, user_login, user_email, key, meta), from_name, esc_url("http://" + domain + path))
    wp_mail(user_email, wp_specialchars_decode(subject), message, message_headers)
    if switched_locale:
        restore_previous_locale()
    # end if
    return True
# end def wpmu_signup_blog_notification
#// 
#// Send a confirmation request email to a user when they sign up for a new user account (without signing up for a site
#// at the same time). The user account will not become active until the confirmation link is clicked.
#// 
#// This is the notification function used when no new site has
#// been requested.
#// 
#// Filter {@see 'wpmu_signup_user_notification'} to bypass this function or
#// replace it with your own notification behavior.
#// 
#// Filter {@see 'wpmu_signup_user_notification_email'} and
#// {@see 'wpmu_signup_user_notification_subject'} to change the content
#// and subject line of the email sent to newly registered users.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $user_login The user's login name.
#// @param string $user_email The user's email address.
#// @param string $key        The activation key created in wpmu_signup_user()
#// @param array  $meta       Optional. Signup meta data. Default empty array.
#// @return bool
#//
def wpmu_signup_user_notification(user_login=None, user_email=None, key=None, meta=Array(), *args_):
    
    #// 
    #// Filters whether to bypass the email notification for new user sign-up.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $user_login User login name.
    #// @param string $user_email User email address.
    #// @param string $key        Activation key created in wpmu_signup_user().
    #// @param array  $meta       Signup meta data. Default empty array.
    #//
    if (not apply_filters("wpmu_signup_user_notification", user_login, user_email, key, meta)):
        return False
    # end if
    user = get_user_by("login", user_login)
    switched_locale = switch_to_locale(get_user_locale(user))
    #// Send email with activation link.
    admin_email = get_site_option("admin_email")
    if "" == admin_email:
        admin_email = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers = str("From: \"") + str(from_name) + str("\" <") + str(admin_email) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    message = php_sprintf(apply_filters("wpmu_signup_user_notification_email", __("""To activate your user, please click the following link:
    %s
    After you activate, you will receive *another email* with your login."""), user_login, user_email, key, meta), site_url(str("wp-activate.php?key=") + str(key)))
    subject = php_sprintf(apply_filters("wpmu_signup_user_notification_subject", _x("[%1$s] Activate %2$s", "New user notification email subject"), user_login, user_email, key, meta), from_name, user_login)
    wp_mail(user_email, wp_specialchars_decode(subject), message, message_headers)
    if switched_locale:
        restore_previous_locale()
    # end if
    return True
# end def wpmu_signup_user_notification
#// 
#// Activate a signup.
#// 
#// Hook to {@see 'wpmu_activate_user'} or {@see 'wpmu_activate_blog'} for events
#// that should happen only when users or sites are self-created (since
#// those actions are not called when users and sites are created
#// by a Super Admin).
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $key The activation key provided to the user.
#// @return array|WP_Error An array containing information about the activated user and/or blog
#//
def wpmu_activate_signup(key=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    signup = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.signups) + str(" WHERE activation_key = %s"), key))
    if php_empty(lambda : signup):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid activation key.")))
    # end if
    if signup.active:
        if php_empty(lambda : signup.domain):
            return php_new_class("WP_Error", lambda : WP_Error("already_active", __("The user is already active."), signup))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("already_active", __("The site is already active."), signup))
        # end if
    # end if
    meta = maybe_unserialize(signup.meta)
    password = wp_generate_password(12, False)
    user_id = username_exists(signup.user_login)
    if (not user_id):
        user_id = wpmu_create_user(signup.user_login, password, signup.user_email)
    else:
        user_already_exists = True
    # end if
    if (not user_id):
        return php_new_class("WP_Error", lambda : WP_Error("create_user", __("Could not create user"), signup))
    # end if
    now = current_time("mysql", True)
    if php_empty(lambda : signup.domain):
        wpdb.update(wpdb.signups, Array({"active": 1, "activated": now}), Array({"activation_key": key}))
        if (php_isset(lambda : user_already_exists)):
            return php_new_class("WP_Error", lambda : WP_Error("user_already_exists", __("That username is already activated."), signup))
        # end if
        #// 
        #// Fires immediately after a new user is activated.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param int    $user_id  User ID.
        #// @param string $password User password.
        #// @param array  $meta     Signup meta data.
        #//
        do_action("wpmu_activate_user", user_id, password, meta)
        return Array({"user_id": user_id, "password": password, "meta": meta})
    # end if
    blog_id = wpmu_create_blog(signup.domain, signup.path, signup.title, user_id, meta, get_current_network_id())
    #// TODO: What to do if we create a user but cannot create a blog?
    if is_wp_error(blog_id):
        #// 
        #// If blog is taken, that means a previous attempt to activate this blog
        #// failed in between creating the blog and setting the activation flag.
        #// Let's just set the active flag and instruct the user to reset their password.
        #//
        if "blog_taken" == blog_id.get_error_code():
            blog_id.add_data(signup)
            wpdb.update(wpdb.signups, Array({"active": 1, "activated": now}), Array({"activation_key": key}))
        # end if
        return blog_id
    # end if
    wpdb.update(wpdb.signups, Array({"active": 1, "activated": now}), Array({"activation_key": key}))
    #// 
    #// Fires immediately after a site is activated.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int    $blog_id       Blog ID.
    #// @param int    $user_id       User ID.
    #// @param int    $password      User password.
    #// @param string $signup_title  Site title.
    #// @param array  $meta          Signup meta data. By default, contains the requested privacy setting and lang_id.
    #//
    do_action("wpmu_activate_blog", blog_id, user_id, password, signup.title, meta)
    return Array({"blog_id": blog_id, "user_id": user_id, "password": password, "title": signup.title, "meta": meta})
# end def wpmu_activate_signup
#// 
#// Create a user.
#// 
#// This function runs when a user self-registers as well as when
#// a Super Admin creates a new user. Hook to {@see 'wpmu_new_user'} for events
#// that should affect all new users, but only on Multisite (otherwise
#// use {@see'user_register'}).
#// 
#// @since MU (3.0.0)
#// 
#// @param string $user_name The new user's login name.
#// @param string $password  The new user's password.
#// @param string $email     The new user's email address.
#// @return int|false Returns false on failure, or int $user_id on success
#//
def wpmu_create_user(user_name=None, password=None, email=None, *args_):
    
    user_name = php_preg_replace("/\\s+/", "", sanitize_user(user_name, True))
    user_id = wp_create_user(user_name, password, email)
    if is_wp_error(user_id):
        return False
    # end if
    #// Newly created users have no roles or caps until they are added to a blog.
    delete_user_option(user_id, "capabilities")
    delete_user_option(user_id, "user_level")
    #// 
    #// Fires immediately after a new user is created.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int $user_id User ID.
    #//
    do_action("wpmu_new_user", user_id)
    return user_id
# end def wpmu_create_user
#// 
#// Create a site.
#// 
#// This function runs when a user self-registers a new site as well
#// as when a Super Admin creates a new site. Hook to {@see 'wpmu_new_blog'}
#// for events that should affect all new sites.
#// 
#// On subdirectory installations, $domain is the same as the main site's
#// domain, and the path is the subdirectory name (eg 'example.com'
#// and '/blog1/'). On subdomain installations, $domain is the new subdomain +
#// root domain (eg 'blog1.example.com'), and $path is '/'.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $domain     The new site's domain.
#// @param string $path       The new site's path.
#// @param string $title      The new site's title.
#// @param int    $user_id    The user ID of the new site's admin.
#// @param array  $options    Optional. Array of key=>value pairs used to set initial site options.
#// If valid status keys are included ('public', 'archived', 'mature',
#// 'spam', 'deleted', or 'lang_id') the given site status(es) will be
#// updated. Otherwise, keys and values will be used to set options for
#// the new site. Default empty array.
#// @param int    $network_id Optional. Network ID. Only relevant on multi-network installations.
#// @return int|WP_Error Returns WP_Error object on failure, the new site ID on success.
#//
def wpmu_create_blog(domain=None, path=None, title=None, user_id=None, options=Array(), network_id=1, *args_):
    
    defaults = Array({"public": 0})
    options = wp_parse_args(options, defaults)
    title = strip_tags(title)
    user_id = php_int(user_id)
    #// Check if the domain has been used already. We should return an error message.
    if domain_exists(domain, path, network_id):
        return php_new_class("WP_Error", lambda : WP_Error("blog_taken", __("Sorry, that site already exists!")))
    # end if
    if (not wp_installing()):
        wp_installing(True)
    # end if
    site_data_whitelist = Array("public", "archived", "mature", "spam", "deleted", "lang_id")
    site_data = php_array_merge(Array({"domain": domain, "path": path, "network_id": network_id}), php_array_intersect_key(options, php_array_flip(site_data_whitelist)))
    #// Data to pass to wp_initialize_site().
    site_initialization_data = Array({"title": title, "user_id": user_id, "options": php_array_diff_key(options, php_array_flip(site_data_whitelist))})
    blog_id = wp_insert_site(php_array_merge(site_data, site_initialization_data))
    if is_wp_error(blog_id):
        return blog_id
    # end if
    wp_cache_set("last_changed", php_microtime(), "sites")
    return blog_id
# end def wpmu_create_blog
#// 
#// Notifies the network admin that a new site has been activated.
#// 
#// Filter {@see 'newblog_notify_siteadmin'} to change the content of
#// the notification email.
#// 
#// @since MU (3.0.0)
#// @since 5.1.0 $blog_id now supports input from the {@see 'wp_initialize_site'} action.
#// 
#// @param WP_Site|int $blog_id    The new site's object or ID.
#// @param string      $deprecated Not used.
#// @return bool
#//
def newblog_notify_siteadmin(blog_id=None, deprecated="", *args_):
    
    if php_is_object(blog_id):
        blog_id = blog_id.blog_id
    # end if
    if get_site_option("registrationnotification") != "yes":
        return False
    # end if
    email = get_site_option("admin_email")
    if is_email(email) == False:
        return False
    # end if
    options_site_url = esc_url(network_admin_url("settings.php"))
    switch_to_blog(blog_id)
    blogname = get_option("blogname")
    siteurl = site_url()
    restore_current_blog()
    msg = php_sprintf(__("""New Site: %1$s
    URL: %2$s
    Remote IP address: %3$s
    Disable these notifications: %4$s"""), blogname, siteurl, wp_unslash(PHP_SERVER["REMOTE_ADDR"]), options_site_url)
    #// 
    #// Filters the message body of the new site activation email sent
    #// to the network administrator.
    #// 
    #// @since MU (3.0.0)
    #// @since 5.4.0 The `$blog_id` parameter was added.
    #// 
    #// @param string $msg     Email body.
    #// @param int    $blog_id The new site's ID.
    #//
    msg = apply_filters("newblog_notify_siteadmin", msg, blog_id)
    #// translators: New site notification email subject. %s: New site URL.
    wp_mail(email, php_sprintf(__("New Site Registration: %s"), siteurl), msg)
    return True
# end def newblog_notify_siteadmin
#// 
#// Notifies the network admin that a new user has been activated.
#// 
#// Filter {@see 'newuser_notify_siteadmin'} to change the content of
#// the notification email.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $user_id The new user's ID.
#// @return bool
#//
def newuser_notify_siteadmin(user_id=None, *args_):
    
    if get_site_option("registrationnotification") != "yes":
        return False
    # end if
    email = get_site_option("admin_email")
    if is_email(email) == False:
        return False
    # end if
    user = get_userdata(user_id)
    options_site_url = esc_url(network_admin_url("settings.php"))
    msg = php_sprintf(__("""New User: %1$s
    Remote IP address: %2$s
    Disable these notifications: %3$s"""), user.user_login, wp_unslash(PHP_SERVER["REMOTE_ADDR"]), options_site_url)
    #// 
    #// Filters the message body of the new user activation email sent
    #// to the network administrator.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string  $msg  Email body.
    #// @param WP_User $user WP_User instance of the new user.
    #//
    msg = apply_filters("newuser_notify_siteadmin", msg, user)
    #// translators: New user notification email subject. %s: User login.
    wp_mail(email, php_sprintf(__("New User Registration: %s"), user.user_login), msg)
    return True
# end def newuser_notify_siteadmin
#// 
#// Checks whether a site name is already taken.
#// 
#// The name is the site's subdomain or the site's subdirectory
#// path depending on the network settings.
#// 
#// Used during the new site registration process to ensure
#// that each site name is unique.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $domain     The domain to be checked.
#// @param string $path       The path to be checked.
#// @param int    $network_id Optional. Network ID. Relevant only on multi-network installations.
#// @return int|null The site ID if the site name exists, null otherwise.
#//
def domain_exists(domain=None, path=None, network_id=1, *args_):
    
    path = trailingslashit(path)
    args = Array({"network_id": network_id, "domain": domain, "path": path, "fields": "ids", "number": 1, "update_site_meta_cache": False})
    result = get_sites(args)
    result = php_array_shift(result)
    #// 
    #// Filters whether a site name is taken.
    #// 
    #// The name is the site's subdomain or the site's subdirectory
    #// path depending on the network settings.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int|null $result     The site ID if the site name exists, null otherwise.
    #// @param string   $domain     Domain to be checked.
    #// @param string   $path       Path to be checked.
    #// @param int      $network_id Network ID. Relevant only on multi-network installations.
    #//
    return apply_filters("domain_exists", result, domain, path, network_id)
# end def domain_exists
#// 
#// Notify a user that their blog activation has been successful.
#// 
#// Filter {@see 'wpmu_welcome_notification'} to disable or bypass.
#// 
#// Filter {@see 'update_welcome_email'} and {@see 'update_welcome_subject'} to
#// modify the content and subject line of the notification email.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $blog_id  Blog ID.
#// @param int    $user_id  User ID.
#// @param string $password User password.
#// @param string $title    Site title.
#// @param array  $meta     Optional. Signup meta data. By default, contains the requested privacy setting and lang_id.
#// @return bool
#//
def wpmu_welcome_notification(blog_id=None, user_id=None, password=None, title=None, meta=Array(), *args_):
    
    current_network = get_network()
    #// 
    #// Filters whether to bypass the welcome email after site activation.
    #// 
    #// Returning false disables the welcome email.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int|bool $blog_id  Blog ID.
    #// @param int      $user_id  User ID.
    #// @param string   $password User password.
    #// @param string   $title    Site title.
    #// @param array    $meta     Signup meta data. By default, contains the requested privacy setting and lang_id.
    #//
    if (not apply_filters("wpmu_welcome_notification", blog_id, user_id, password, title, meta)):
        return False
    # end if
    user = get_userdata(user_id)
    switched_locale = switch_to_locale(get_user_locale(user))
    welcome_email = get_site_option("welcome_email")
    if False == welcome_email:
        #// translators: Do not translate USERNAME, SITE_NAME, BLOG_URL, PASSWORD: those are placeholders.
        welcome_email = __("""Howdy USERNAME,
        Your new SITE_NAME site has been successfully set up at:
        BLOG_URL
        You can log in to the administrator account with the following information:
        Username: USERNAME
        Password: PASSWORD
        Log in here: BLOG_URLwp-login.php
        We hope you enjoy your new site. Thanks!
        --The Team @ SITE_NAME""")
    # end if
    url = get_blogaddress_by_id(blog_id)
    welcome_email = php_str_replace("SITE_NAME", current_network.site_name, welcome_email)
    welcome_email = php_str_replace("BLOG_TITLE", title, welcome_email)
    welcome_email = php_str_replace("BLOG_URL", url, welcome_email)
    welcome_email = php_str_replace("USERNAME", user.user_login, welcome_email)
    welcome_email = php_str_replace("PASSWORD", password, welcome_email)
    #// 
    #// Filters the content of the welcome email after site activation.
    #// 
    #// Content should be formatted for transmission via wp_mail().
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $welcome_email Message body of the email.
    #// @param int    $blog_id       Blog ID.
    #// @param int    $user_id       User ID.
    #// @param string $password      User password.
    #// @param string $title         Site title.
    #// @param array  $meta          Signup meta data. By default, contains the requested privacy setting and lang_id.
    #//
    welcome_email = apply_filters("update_welcome_email", welcome_email, blog_id, user_id, password, title, meta)
    admin_email = get_site_option("admin_email")
    if "" == admin_email:
        admin_email = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers = str("From: \"") + str(from_name) + str("\" <") + str(admin_email) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    message = welcome_email
    if php_empty(lambda : current_network.site_name):
        current_network.site_name = "WordPress"
    # end if
    #// translators: New site notification email subject. 1: Network title, 2: New site title.
    subject = __("New %1$s Site: %2$s")
    #// 
    #// Filters the subject of the welcome email after site activation.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $subject Subject of the email.
    #//
    subject = apply_filters("update_welcome_subject", php_sprintf(subject, current_network.site_name, wp_unslash(title)))
    wp_mail(user.user_email, wp_specialchars_decode(subject), message, message_headers)
    if switched_locale:
        restore_previous_locale()
    # end if
    return True
# end def wpmu_welcome_notification
#// 
#// Notify a user that their account activation has been successful.
#// 
#// Filter {@see 'wpmu_welcome_user_notification'} to disable or bypass.
#// 
#// Filter {@see 'update_welcome_user_email'} and {@see 'update_welcome_user_subject'} to
#// modify the content and subject line of the notification email.
#// 
#// @since MU (3.0.0)
#// 
#// @param int    $user_id  User ID.
#// @param string $password User password.
#// @param array  $meta     Optional. Signup meta data. Default empty array.
#// @return bool
#//
def wpmu_welcome_user_notification(user_id=None, password=None, meta=Array(), *args_):
    
    current_network = get_network()
    #// 
    #// Filters whether to bypass the welcome email after user activation.
    #// 
    #// Returning false disables the welcome email.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int    $user_id  User ID.
    #// @param string $password User password.
    #// @param array  $meta     Signup meta data. Default empty array.
    #//
    if (not apply_filters("wpmu_welcome_user_notification", user_id, password, meta)):
        return False
    # end if
    welcome_email = get_site_option("welcome_user_email")
    user = get_userdata(user_id)
    switched_locale = switch_to_locale(get_user_locale(user))
    #// 
    #// Filters the content of the welcome email after user activation.
    #// 
    #// Content should be formatted for transmission via wp_mail().
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $welcome_email The message body of the account activation success email.
    #// @param int    $user_id       User ID.
    #// @param string $password      User password.
    #// @param array  $meta          Signup meta data. Default empty array.
    #//
    welcome_email = apply_filters("update_welcome_user_email", welcome_email, user_id, password, meta)
    welcome_email = php_str_replace("SITE_NAME", current_network.site_name, welcome_email)
    welcome_email = php_str_replace("USERNAME", user.user_login, welcome_email)
    welcome_email = php_str_replace("PASSWORD", password, welcome_email)
    welcome_email = php_str_replace("LOGINLINK", wp_login_url(), welcome_email)
    admin_email = get_site_option("admin_email")
    if "" == admin_email:
        admin_email = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers = str("From: \"") + str(from_name) + str("\" <") + str(admin_email) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    message = welcome_email
    if php_empty(lambda : current_network.site_name):
        current_network.site_name = "WordPress"
    # end if
    #// translators: New user notification email subject. 1: Network title, 2: New user login.
    subject = __("New %1$s User: %2$s")
    #// 
    #// Filters the subject of the welcome email after user activation.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $subject Subject of the email.
    #//
    subject = apply_filters("update_welcome_user_subject", php_sprintf(subject, current_network.site_name, user.user_login))
    wp_mail(user.user_email, wp_specialchars_decode(subject), message, message_headers)
    if switched_locale:
        restore_previous_locale()
    # end if
    return True
# end def wpmu_welcome_user_notification
#// 
#// Get the current network.
#// 
#// Returns an object containing the 'id', 'domain', 'path', and 'site_name'
#// properties of the network being viewed.
#// 
#// @see wpmu_current_site()
#// 
#// @since MU (3.0.0)
#// 
#// @global WP_Network $current_site
#// 
#// @return WP_Network
#//
def get_current_site(*args_):
    
    global current_site
    php_check_if_defined("current_site")
    return current_site
# end def get_current_site
#// 
#// Get a user's most recent post.
#// 
#// Walks through each of a user's blogs to find the post with
#// the most recent post_date_gmt.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $user_id
#// @return array Contains the blog_id, post_id, post_date_gmt, and post_gmt_ts
#//
def get_most_recent_post_of_user(user_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    user_blogs = get_blogs_of_user(php_int(user_id))
    most_recent_post = Array()
    #// Walk through each blog and get the most recent post
    #// published by $user_id.
    for blog in user_blogs:
        prefix = wpdb.get_blog_prefix(blog.userblog_id)
        recent_post = wpdb.get_row(wpdb.prepare(str("SELECT ID, post_date_gmt FROM ") + str(prefix) + str("posts WHERE post_author = %d AND post_type = 'post' AND post_status = 'publish' ORDER BY post_date_gmt DESC LIMIT 1"), user_id), ARRAY_A)
        #// Make sure we found a post.
        if (php_isset(lambda : recent_post["ID"])):
            post_gmt_ts = strtotime(recent_post["post_date_gmt"])
            #// 
            #// If this is the first post checked
            #// or if this post is newer than the current recent post,
            #// make it the new most recent post.
            #//
            if (not (php_isset(lambda : most_recent_post["post_gmt_ts"]))) or post_gmt_ts > most_recent_post["post_gmt_ts"]:
                most_recent_post = Array({"blog_id": blog.userblog_id, "post_id": recent_post["ID"], "post_date_gmt": recent_post["post_date_gmt"], "post_gmt_ts": post_gmt_ts})
            # end if
        # end if
    # end for
    return most_recent_post
# end def get_most_recent_post_of_user
#// 
#// Misc functions.
#// 
#// 
#// Check an array of MIME types against a whitelist.
#// 
#// WordPress ships with a set of allowed upload filetypes,
#// which is defined in wp-includes/functions.php in
#// get_allowed_mime_types(). This function is used to filter
#// that list against the filetype whitelist provided by Multisite
#// Super Admins at wp-admin/network/settings.php.
#// 
#// @since MU (3.0.0)
#// 
#// @param array $mimes
#// @return array
#//
def check_upload_mimes(mimes=None, *args_):
    
    site_exts = php_explode(" ", get_site_option("upload_filetypes", "jpg jpeg png gif"))
    site_mimes = Array()
    for ext in site_exts:
        for ext_pattern,mime in mimes:
            if "" != ext and False != php_strpos(ext_pattern, ext):
                site_mimes[ext_pattern] = mime
            # end if
        # end for
    # end for
    return site_mimes
# end def check_upload_mimes
#// 
#// Update a blog's post count.
#// 
#// WordPress MS stores a blog's post count as an option so as
#// to avoid extraneous COUNTs when a blog's details are fetched
#// with get_site(). This function is called when posts are published
#// or unpublished to make sure the count stays current.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $deprecated Not used.
#//
def update_posts_count(deprecated="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    update_option("post_count", php_int(wpdb.get_var(str("SELECT COUNT(ID) FROM ") + str(wpdb.posts) + str(" WHERE post_status = 'publish' and post_type = 'post'"))))
# end def update_posts_count
#// 
#// Logs the user email, IP, and registration date of a new site.
#// 
#// @since MU (3.0.0)
#// @since 5.1.0 Parameters now support input from the {@see 'wp_initialize_site'} action.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param WP_Site|int $blog_id The new site's object or ID.
#// @param int|array   $user_id User ID, or array of arguments including 'user_id'.
#//
def wpmu_log_new_registrations(blog_id=None, user_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_is_object(blog_id):
        blog_id = blog_id.blog_id
    # end if
    if php_is_array(user_id):
        user_id = user_id["user_id"] if (not php_empty(lambda : user_id["user_id"])) else 0
    # end if
    user = get_userdata(php_int(user_id))
    if user:
        wpdb.insert(wpdb.registration_log, Array({"email": user.user_email, "IP": php_preg_replace("/[^0-9., ]/", "", wp_unslash(PHP_SERVER["REMOTE_ADDR"])), "blog_id": blog_id, "date_registered": current_time("mysql")}))
    # end if
# end def wpmu_log_new_registrations
#// 
#// Maintains a canonical list of terms by syncing terms created for each blog with the global terms table.
#// 
#// @since 3.0.0
#// 
#// @see term_id_filter
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// @staticvar int $global_terms_recurse
#// 
#// @param int    $term_id    An ID for a term on the current blog.
#// @param string $deprecated Not used.
#// @return int An ID from the global terms table mapped from $term_id.
#//
def global_terms(term_id=None, deprecated="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    global_terms_recurse = None
    if (not global_terms_enabled()):
        return term_id
    # end if
    #// Prevent a race condition.
    recurse_start = False
    if None == global_terms_recurse:
        recurse_start = True
        global_terms_recurse = 1
    elif 10 < global_terms_recurse:
        return term_id
        global_terms_recurse += 1
    # end if
    term_id = php_intval(term_id)
    c = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.terms) + str(" WHERE term_id = %d"), term_id))
    global_id = wpdb.get_var(wpdb.prepare(str("SELECT cat_ID FROM ") + str(wpdb.sitecategories) + str(" WHERE category_nicename = %s"), c.slug))
    if None == global_id:
        used_global_id = wpdb.get_var(wpdb.prepare(str("SELECT cat_ID FROM ") + str(wpdb.sitecategories) + str(" WHERE cat_ID = %d"), c.term_id))
        if None == used_global_id:
            wpdb.insert(wpdb.sitecategories, Array({"cat_ID": term_id, "cat_name": c.name, "category_nicename": c.slug}))
            global_id = wpdb.insert_id
            if php_empty(lambda : global_id):
                return term_id
            # end if
        else:
            max_global_id = wpdb.get_var(str("SELECT MAX(cat_ID) FROM ") + str(wpdb.sitecategories))
            max_local_id = wpdb.get_var(str("SELECT MAX(term_id) FROM ") + str(wpdb.terms))
            new_global_id = php_max(max_global_id, max_local_id) + mt_rand(100, 400)
            wpdb.insert(wpdb.sitecategories, Array({"cat_ID": new_global_id, "cat_name": c.name, "category_nicename": c.slug}))
            global_id = wpdb.insert_id
        # end if
    elif global_id != term_id:
        local_id = wpdb.get_var(wpdb.prepare(str("SELECT term_id FROM ") + str(wpdb.terms) + str(" WHERE term_id = %d"), global_id))
        if None != local_id:
            global_terms(local_id)
            if 10 < global_terms_recurse:
                global_id = term_id
            # end if
        # end if
    # end if
    if global_id != term_id:
        if get_option("default_category") == term_id:
            update_option("default_category", global_id)
        # end if
        wpdb.update(wpdb.terms, Array({"term_id": global_id}), Array({"term_id": term_id}))
        wpdb.update(wpdb.term_taxonomy, Array({"term_id": global_id}), Array({"term_id": term_id}))
        wpdb.update(wpdb.term_taxonomy, Array({"parent": global_id}), Array({"parent": term_id}))
        clean_term_cache(term_id)
    # end if
    if recurse_start:
        global_terms_recurse = None
    # end if
    return global_id
# end def global_terms
#// 
#// Ensure that the current site's domain is listed in the allowed redirect host list.
#// 
#// @see wp_validate_redirect()
#// @since MU (3.0.0)
#// 
#// @param array|string $deprecated Not used.
#// @return string[] {
#// An array containing the current site's domain.
#// 
#// @type string $0 The current site's domain.
#// }
#//
def redirect_this_site(deprecated="", *args_):
    
    return Array(get_network().domain)
# end def redirect_this_site
#// 
#// Check whether an upload is too big.
#// 
#// @since MU (3.0.0)
#// 
#// @blessed
#// 
#// @param array $upload
#// @return string|array If the upload is under the size limit, $upload is returned. Otherwise returns an error message.
#//
def upload_is_file_too_big(upload=None, *args_):
    
    if (not php_is_array(upload)) or php_defined("WP_IMPORTING") or get_site_option("upload_space_check_disabled"):
        return upload
    # end if
    if php_strlen(upload["bits"]) > KB_IN_BYTES * get_site_option("fileupload_maxk", 1500):
        #// translators: %s: Maximum allowed file size in kilobytes.
        return php_sprintf(__("This file is too big. Files must be less than %s KB in size.") + "<br />", get_site_option("fileupload_maxk", 1500))
    # end if
    return upload
# end def upload_is_file_too_big
#// 
#// Add a nonce field to the signup page.
#// 
#// @since MU (3.0.0)
#//
def signup_nonce_fields(*args_):
    
    id = mt_rand()
    php_print(str("<input type='hidden' name='signup_form_id' value='") + str(id) + str("' />"))
    wp_nonce_field("signup_form_" + id, "_signup_form", False)
# end def signup_nonce_fields
#// 
#// Process the signup nonce created in signup_nonce_fields().
#// 
#// @since MU (3.0.0)
#// 
#// @param array $result
#// @return array
#//
def signup_nonce_check(result=None, *args_):
    
    if (not php_strpos(PHP_SERVER["PHP_SELF"], "wp-signup.php")):
        return result
    # end if
    if (not wp_verify_nonce(PHP_POST["_signup_form"], "signup_form_" + PHP_POST["signup_form_id"])):
        result["errors"].add("invalid_nonce", __("Unable to submit this form, please try again."))
    # end if
    return result
# end def signup_nonce_check
#// 
#// Correct 404 redirects when NOBLOGREDIRECT is defined.
#// 
#// @since MU (3.0.0)
#//
def maybe_redirect_404(*args_):
    
    if is_main_site() and is_404() and php_defined("NOBLOGREDIRECT"):
        #// 
        #// Filters the redirect URL for 404s on the main site.
        #// 
        #// The filter is only evaluated if the NOBLOGREDIRECT constant is defined.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $no_blog_redirect The redirect URL defined in NOBLOGREDIRECT.
        #//
        destination = apply_filters("blog_redirect_404", NOBLOGREDIRECT)
        if destination:
            if "%siteurl%" == destination:
                destination = network_home_url()
            # end if
            wp_redirect(destination)
            php_exit(0)
        # end if
    # end if
# end def maybe_redirect_404
#// 
#// Add a new user to a blog by visiting /newbloguser/{key}/.
#// 
#// This will only work when the user's details are saved as an option
#// keyed as 'new_user_{key}', where '{key}' is a hash generated for the user to be
#// added, as when a user is invited through the regular WP Add User interface.
#// 
#// @since MU (3.0.0)
#//
def maybe_add_existing_user_to_blog(*args_):
    
    if False == php_strpos(PHP_SERVER["REQUEST_URI"], "/newbloguser/"):
        return
    # end if
    parts = php_explode("/", PHP_SERVER["REQUEST_URI"])
    key = php_array_pop(parts)
    if "" == key:
        key = php_array_pop(parts)
    # end if
    details = get_option("new_user_" + key)
    if (not php_empty(lambda : details)):
        delete_option("new_user_" + key)
    # end if
    if php_empty(lambda : details) or is_wp_error(add_existing_user_to_blog(details)):
        wp_die(php_sprintf(__("An error occurred adding you to this site. Back to the <a href=\"%s\">homepage</a>."), home_url()))
    # end if
    wp_die(php_sprintf(__("You have been added to this site. Please visit the <a href=\"%1$s\">homepage</a> or <a href=\"%2$s\">log in</a> using your username and password."), home_url(), admin_url()), __("WordPress &rsaquo; Success"), Array({"response": 200}))
# end def maybe_add_existing_user_to_blog
#// 
#// Add a user to a blog based on details from maybe_add_existing_user_to_blog().
#// 
#// @since MU (3.0.0)
#// 
#// @param array $details User details.
#// @return true|WP_Error|void True on success or a WP_Error object if the user doesn't exist
#// or could not be added. Void if $details array was not provided.
#//
def add_existing_user_to_blog(details=False, *args_):
    
    if php_is_array(details):
        blog_id = get_current_blog_id()
        result = add_user_to_blog(blog_id, details["user_id"], details["role"])
        #// 
        #// Fires immediately after an existing user is added to a site.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param int           $user_id User ID.
        #// @param true|WP_Error $result  True on success or a WP_Error object if the user doesn't exist
        #// or could not be added.
        #//
        do_action("added_existing_user", details["user_id"], result)
        return result
    # end if
# end def add_existing_user_to_blog
#// 
#// Adds a newly created user to the appropriate blog
#// 
#// To add a user in general, use add_user_to_blog(). This function
#// is specifically hooked into the {@see 'wpmu_activate_user'} action.
#// 
#// @since MU (3.0.0)
#// @see add_user_to_blog()
#// 
#// @param int    $user_id  User ID.
#// @param string $password User password. Ignored.
#// @param array  $meta     Signup meta data.
#//
def add_new_user_to_blog(user_id=None, password=None, meta=None, *args_):
    
    if (not php_empty(lambda : meta["add_to_blog"])):
        blog_id = meta["add_to_blog"]
        role = meta["new_role"]
        remove_user_from_blog(user_id, get_network().site_id)
        #// Remove user from main blog.
        result = add_user_to_blog(blog_id, user_id, role)
        if (not is_wp_error(result)):
            update_user_meta(user_id, "primary_blog", blog_id)
        # end if
    # end if
# end def add_new_user_to_blog
#// 
#// Correct From host on outgoing mail to match the site domain
#// 
#// @since MU (3.0.0)
#// 
#// @param PHPMailer $phpmailer The PHPMailer instance (passed by reference).
#//
def fix_phpmailer_messageid(phpmailer=None, *args_):
    
    phpmailer.Hostname = get_network().domain
# end def fix_phpmailer_messageid
#// 
#// Check to see whether a user is marked as a spammer, based on user login.
#// 
#// @since MU (3.0.0)
#// 
#// @param string|WP_User $user Optional. Defaults to current user. WP_User object,
#// or user login name as a string.
#// @return bool
#//
def is_user_spammy(user=None, *args_):
    
    if (not type(user).__name__ == "WP_User"):
        if user:
            user = get_user_by("login", user)
        else:
            user = wp_get_current_user()
        # end if
    # end if
    return user and (php_isset(lambda : user.spam)) and 1 == user.spam
# end def is_user_spammy
#// 
#// Update this blog's 'public' setting in the global blogs table.
#// 
#// Public blogs have a setting of 1, private blogs are 0.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $old_value
#// @param int $value     The new public value
#//
def update_blog_public(old_value=None, value=None, *args_):
    
    update_blog_status(get_current_blog_id(), "public", php_int(value))
# end def update_blog_public
#// 
#// Check whether users can self-register, based on Network settings.
#// 
#// @since MU (3.0.0)
#// 
#// @return bool
#//
def users_can_register_signup_filter(*args_):
    
    registration = get_site_option("registration")
    return "all" == registration or "user" == registration
# end def users_can_register_signup_filter
#// 
#// Ensure that the welcome message is not empty. Currently unused.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $text
#// @return string
#//
def welcome_user_msg_filter(text=None, *args_):
    
    if (not text):
        remove_filter("site_option_welcome_user_email", "welcome_user_msg_filter")
        #// translators: Do not translate USERNAME, PASSWORD, LOGINLINK, SITE_NAME: those are placeholders.
        text = __("""Howdy USERNAME,
        Your new account is set up.
        You can log in with the following information:
        Username: USERNAME
        Password: PASSWORD
        LOGINLINK
        Thanks!
        --The Team @ SITE_NAME""")
        update_site_option("welcome_user_email", text)
    # end if
    return text
# end def welcome_user_msg_filter
#// 
#// Whether to force SSL on content.
#// 
#// @since 2.8.5
#// 
#// @staticvar bool $forced_content
#// 
#// @param bool $force
#// @return bool True if forced, false if not forced.
#//
def force_ssl_content(force="", *args_):
    
    forced_content = False
    if "" != force:
        old_forced = forced_content
        forced_content = force
        return old_forced
    # end if
    return forced_content
# end def force_ssl_content
#// 
#// Formats a URL to use https.
#// 
#// Useful as a filter.
#// 
#// @since 2.8.5
#// 
#// @param string $url URL
#// @return string URL with https as the scheme
#//
def filter_SSL(url=None, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    if (not php_is_string(url)):
        return get_bloginfo("url")
        pass
    # end if
    if force_ssl_content() and is_ssl():
        url = set_url_scheme(url, "https")
    # end if
    return url
# end def filter_SSL
#// 
#// Schedule update of the network-wide counts for the current network.
#// 
#// @since 3.1.0
#//
def wp_schedule_update_network_counts(*args_):
    
    if (not is_main_site()):
        return
    # end if
    if (not wp_next_scheduled("update_network_counts")) and (not wp_installing()):
        wp_schedule_event(time(), "twicedaily", "update_network_counts")
    # end if
# end def wp_schedule_update_network_counts
#// 
#// Update the network-wide counts for the current network.
#// 
#// @since 3.1.0
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#//
def wp_update_network_counts(network_id=None, *args_):
    
    wp_update_network_user_counts(network_id)
    wp_update_network_site_counts(network_id)
# end def wp_update_network_counts
#// 
#// Update the count of sites for the current network.
#// 
#// If enabled through the {@see 'enable_live_network_counts'} filter, update the sites count
#// on a network when a site is created or its status is updated.
#// 
#// @since 3.7.0
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#//
def wp_maybe_update_network_site_counts(network_id=None, *args_):
    
    is_small_network = (not wp_is_large_network("sites", network_id))
    #// 
    #// Filters whether to update network site or user counts when a new site is created.
    #// 
    #// @since 3.7.0
    #// 
    #// @see wp_is_large_network()
    #// 
    #// @param bool   $small_network Whether the network is considered small.
    #// @param string $context       Context. Either 'users' or 'sites'.
    #//
    if (not apply_filters("enable_live_network_counts", is_small_network, "sites")):
        return
    # end if
    wp_update_network_site_counts(network_id)
# end def wp_maybe_update_network_site_counts
#// 
#// Update the network-wide users count.
#// 
#// If enabled through the {@see 'enable_live_network_counts'} filter, update the users count
#// on a network when a user is created or its status is updated.
#// 
#// @since 3.7.0
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#//
def wp_maybe_update_network_user_counts(network_id=None, *args_):
    
    is_small_network = (not wp_is_large_network("users", network_id))
    #// This filter is documented in wp-includes/ms-functions.php
    if (not apply_filters("enable_live_network_counts", is_small_network, "users")):
        return
    # end if
    wp_update_network_user_counts(network_id)
# end def wp_maybe_update_network_user_counts
#// 
#// Update the network-wide site count.
#// 
#// @since 3.7.0
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#//
def wp_update_network_site_counts(network_id=None, *args_):
    
    network_id = php_int(network_id)
    if (not network_id):
        network_id = get_current_network_id()
    # end if
    count = get_sites(Array({"network_id": network_id, "spam": 0, "deleted": 0, "archived": 0, "count": True, "update_site_meta_cache": False}))
    update_network_option(network_id, "blog_count", count)
# end def wp_update_network_site_counts
#// 
#// Update the network-wide user count.
#// 
#// @since 3.7.0
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#//
def wp_update_network_user_counts(network_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    count = wpdb.get_var(str("SELECT COUNT(ID) as c FROM ") + str(wpdb.users) + str(" WHERE spam = '0' AND deleted = '0'"))
    update_network_option(network_id, "user_count", count)
# end def wp_update_network_user_counts
#// 
#// Returns the space used by the current site.
#// 
#// @since 3.5.0
#// 
#// @return int Used space in megabytes.
#//
def get_space_used(*args_):
    
    #// 
    #// Filters the amount of storage space used by the current site, in megabytes.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int|false $space_used The amount of used space, in megabytes. Default false.
    #//
    space_used = apply_filters("pre_get_space_used", False)
    if False == space_used:
        upload_dir = wp_upload_dir()
        space_used = get_dirsize(upload_dir["basedir"]) / MB_IN_BYTES
    # end if
    return space_used
# end def get_space_used
#// 
#// Returns the upload quota for the current blog.
#// 
#// @since MU (3.0.0)
#// 
#// @return int Quota in megabytes
#//
def get_space_allowed(*args_):
    
    space_allowed = get_option("blog_upload_space")
    if (not php_is_numeric(space_allowed)):
        space_allowed = get_site_option("blog_upload_space")
    # end if
    if (not php_is_numeric(space_allowed)):
        space_allowed = 100
    # end if
    #// 
    #// Filters the upload quota for the current site.
    #// 
    #// @since 3.7.0
    #// 
    #// @param int $space_allowed Upload quota in megabytes for the current blog.
    #//
    return apply_filters("get_space_allowed", space_allowed)
# end def get_space_allowed
#// 
#// Determines if there is any upload space left in the current blog's quota.
#// 
#// @since 3.0.0
#// 
#// @return int of upload space available in bytes
#//
def get_upload_space_available(*args_):
    
    allowed = get_space_allowed()
    if allowed < 0:
        allowed = 0
    # end if
    space_allowed = allowed * MB_IN_BYTES
    if get_site_option("upload_space_check_disabled"):
        return space_allowed
    # end if
    space_used = get_space_used() * MB_IN_BYTES
    if space_allowed - space_used <= 0:
        return 0
    # end if
    return space_allowed - space_used
# end def get_upload_space_available
#// 
#// Determines if there is any upload space left in the current blog's quota.
#// 
#// @since 3.0.0
#// @return bool True if space is available, false otherwise.
#//
def is_upload_space_available(*args_):
    
    if get_site_option("upload_space_check_disabled"):
        return True
    # end if
    return php_bool(get_upload_space_available())
# end def is_upload_space_available
#// 
#// Filters the maximum upload file size allowed, in bytes.
#// 
#// @since 3.0.0
#// 
#// @param  int $size Upload size limit in bytes.
#// @return int       Upload size limit in bytes.
#//
def upload_size_limit_filter(size=None, *args_):
    
    fileupload_maxk = KB_IN_BYTES * get_site_option("fileupload_maxk", 1500)
    if get_site_option("upload_space_check_disabled"):
        return php_min(size, fileupload_maxk)
    # end if
    return php_min(size, fileupload_maxk, get_upload_space_available())
# end def upload_size_limit_filter
#// 
#// Whether or not we have a large network.
#// 
#// The default criteria for a large network is either more than 10,000 users or more than 10,000 sites.
#// Plugins can alter this criteria using the {@see 'wp_is_large_network'} filter.
#// 
#// @since 3.3.0
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @param string   $using      'sites or 'users'. Default is 'sites'.
#// @param int|null $network_id ID of the network. Default is the current network.
#// @return bool True if the network meets the criteria for large. False otherwise.
#//
def wp_is_large_network(using="sites", network_id=None, *args_):
    
    network_id = php_int(network_id)
    if (not network_id):
        network_id = get_current_network_id()
    # end if
    if "users" == using:
        count = get_user_count(network_id)
        #// 
        #// Filters whether the network is considered large.
        #// 
        #// @since 3.3.0
        #// @since 4.8.0 The `$network_id` parameter has been added.
        #// 
        #// @param bool   $is_large_network Whether the network has more than 10000 users or sites.
        #// @param string $component        The component to count. Accepts 'users', or 'sites'.
        #// @param int    $count            The count of items for the component.
        #// @param int    $network_id       The ID of the network being checked.
        #//
        return apply_filters("wp_is_large_network", count > 10000, "users", count, network_id)
    # end if
    count = get_blog_count(network_id)
    #// This filter is documented in wp-includes/ms-functions.php
    return apply_filters("wp_is_large_network", count > 10000, "sites", count, network_id)
# end def wp_is_large_network
#// 
#// Retrieves a list of reserved site on a sub-directory Multisite installation.
#// 
#// @since 4.4.0
#// 
#// @return string[] Array of reserved names.
#//
def get_subdirectory_reserved_names(*args_):
    
    names = Array("page", "comments", "blog", "files", "feed", "wp-admin", "wp-content", "wp-includes", "wp-json", "embed")
    #// 
    #// Filters reserved site names on a sub-directory Multisite installation.
    #// 
    #// @since 3.0.0
    #// @since 4.4.0 'wp-admin', 'wp-content', 'wp-includes', 'wp-json', and 'embed' were added
    #// to the reserved names list.
    #// 
    #// @param string[] $subdirectory_reserved_names Array of reserved names.
    #//
    return apply_filters("subdirectory_reserved_names", names)
# end def get_subdirectory_reserved_names
#// 
#// Send a confirmation request email when a change of network admin email address is attempted.
#// 
#// The new network admin address will not become active until confirmed.
#// 
#// @since 4.9.0
#// 
#// @param string $old_value The old network admin email address.
#// @param string $value     The proposed new network admin email address.
#//
def update_network_option_new_admin_email(old_value=None, value=None, *args_):
    
    if get_site_option("admin_email") == value or (not is_email(value)):
        return
    # end if
    hash = php_md5(value + time() + mt_rand())
    new_admin_email = Array({"hash": hash, "newemail": value})
    update_site_option("network_admin_hash", new_admin_email)
    switched_locale = switch_to_locale(get_user_locale())
    #// translators: Do not translate USERNAME, ADMIN_URL, EMAIL, SITENAME, SITEURL: those are placeholders.
    email_text = __("""Howdy ###USERNAME###,
    You recently requested to have the network admin email address on
    your network changed.
    If this is correct, please click on the following link to change it:
    ###ADMIN_URL###
    You can safely ignore and delete this email if you do not want to
    take this action.
    This email has been sent to ###EMAIL###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    #// 
    #// Filters the text of the email sent when a change of network admin email address is attempted.
    #// 
    #// The following strings have a special meaning and will get replaced dynamically:
    #// ###USERNAME###  The current user's username.
    #// ###ADMIN_URL### The link to click on to confirm the email change.
    #// ###EMAIL###     The proposed new network admin email address.
    #// ###SITENAME###  The name of the network.
    #// ###SITEURL###   The URL to the network.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $email_text      Text in the email.
    #// @param array  $new_admin_email {
    #// Data relating to the new network admin email address.
    #// 
    #// @type string $hash     The secure hash used in the confirmation link URL.
    #// @type string $newemail The proposed new network admin email address.
    #// }
    #//
    content = apply_filters("new_network_admin_email_content", email_text, new_admin_email)
    current_user = wp_get_current_user()
    content = php_str_replace("###USERNAME###", current_user.user_login, content)
    content = php_str_replace("###ADMIN_URL###", esc_url(network_admin_url("settings.php?network_admin_hash=" + hash)), content)
    content = php_str_replace("###EMAIL###", value, content)
    content = php_str_replace("###SITENAME###", wp_specialchars_decode(get_site_option("site_name"), ENT_QUOTES), content)
    content = php_str_replace("###SITEURL###", network_home_url(), content)
    wp_mail(value, php_sprintf(__("[%s] Network Admin Email Change Request"), wp_specialchars_decode(get_site_option("site_name"), ENT_QUOTES)), content)
    if switched_locale:
        restore_previous_locale()
    # end if
# end def update_network_option_new_admin_email
#// 
#// Send an email to the old network admin email address when the network admin email address changes.
#// 
#// @since 4.9.0
#// 
#// @param string $option_name The relevant database option name.
#// @param string $new_email   The new network admin email address.
#// @param string $old_email   The old network admin email address.
#// @param int    $network_id  ID of the network.
#//
def wp_network_admin_email_change_notification(option_name=None, new_email=None, old_email=None, network_id=None, *args_):
    
    send = True
    #// Don't send the notification to the default 'admin_email' value.
    if "you@example.com" == old_email:
        send = False
    # end if
    #// 
    #// Filters whether to send the network admin email change notification email.
    #// 
    #// @since 4.9.0
    #// 
    #// @param bool   $send       Whether to send the email notification.
    #// @param string $old_email  The old network admin email address.
    #// @param string $new_email  The new network admin email address.
    #// @param int    $network_id ID of the network.
    #//
    send = apply_filters("send_network_admin_email_change_email", send, old_email, new_email, network_id)
    if (not send):
        return
    # end if
    #// translators: Do not translate OLD_EMAIL, NEW_EMAIL, SITENAME, SITEURL: those are placeholders.
    email_change_text = __("""Hi,
    This notice confirms that the network admin email address was changed on ###SITENAME###.
    The new network admin email address is ###NEW_EMAIL###.
    This email has been sent to ###OLD_EMAIL###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    email_change_email = Array({"to": old_email, "subject": __("[%s] Network Admin Email Changed"), "message": email_change_text, "headers": ""})
    #// Get network name.
    network_name = wp_specialchars_decode(get_site_option("site_name"), ENT_QUOTES)
    #// 
    #// Filters the contents of the email notification sent when the network admin email address is changed.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $email_change_email {
    #// Used to build wp_mail().
    #// 
    #// @type string $to      The intended recipient.
    #// @type string $subject The subject of the email.
    #// @type string $message The content of the email.
    #// The following strings have a special meaning and will get replaced dynamically:
    #// - ###OLD_EMAIL### The old network admin email address.
    #// - ###NEW_EMAIL### The new network admin email address.
    #// - ###SITENAME###  The name of the network.
    #// - ###SITEURL###   The URL to the site.
    #// @type string $headers Headers.
    #// }
    #// @param string $old_email  The old network admin email address.
    #// @param string $new_email  The new network admin email address.
    #// @param int    $network_id ID of the network.
    #//
    email_change_email = apply_filters("network_admin_email_change_email", email_change_email, old_email, new_email, network_id)
    email_change_email["message"] = php_str_replace("###OLD_EMAIL###", old_email, email_change_email["message"])
    email_change_email["message"] = php_str_replace("###NEW_EMAIL###", new_email, email_change_email["message"])
    email_change_email["message"] = php_str_replace("###SITENAME###", network_name, email_change_email["message"])
    email_change_email["message"] = php_str_replace("###SITEURL###", home_url(), email_change_email["message"])
    wp_mail(email_change_email["to"], php_sprintf(email_change_email["subject"], network_name), email_change_email["message"], email_change_email["headers"])
# end def wp_network_admin_email_change_notification
