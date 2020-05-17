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
def get_sitestats(*_args_):
    
    
    stats_ = Array({"blogs": get_blog_count(), "users": get_user_count()})
    return stats_
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
def get_active_blog_for_user(user_id_=None, *_args_):
    
    
    blogs_ = get_blogs_of_user(user_id_)
    if php_empty(lambda : blogs_):
        return
    # end if
    if (not is_multisite()):
        return blogs_[get_current_blog_id()]
    # end if
    primary_blog_ = get_user_meta(user_id_, "primary_blog", True)
    first_blog_ = current(blogs_)
    if False != primary_blog_:
        if (not (php_isset(lambda : blogs_[primary_blog_]))):
            update_user_meta(user_id_, "primary_blog", first_blog_.userblog_id)
            primary_ = get_site(first_blog_.userblog_id)
        else:
            primary_ = get_site(primary_blog_)
        # end if
    else:
        #// TODO: Review this call to add_user_to_blog too - to get here the user must have a role on this blog?
        result_ = add_user_to_blog(first_blog_.userblog_id, user_id_, "subscriber")
        if (not is_wp_error(result_)):
            update_user_meta(user_id_, "primary_blog", first_blog_.userblog_id)
            primary_ = first_blog_
        # end if
    # end if
    if (not php_is_object(primary_)) or 1 == primary_.archived or 1 == primary_.spam or 1 == primary_.deleted:
        blogs_ = get_blogs_of_user(user_id_, True)
        #// If a user's primary blog is shut down, check their other blogs.
        ret_ = False
        if php_is_array(blogs_) and php_count(blogs_) > 0:
            for blog_id_,blog_ in blogs_:
                if get_current_network_id() != blog_.site_id:
                    continue
                # end if
                details_ = get_site(blog_id_)
                if php_is_object(details_) and 0 == details_.archived and 0 == details_.spam and 0 == details_.deleted:
                    ret_ = details_
                    if get_user_meta(user_id_, "primary_blog", True) != blog_id_:
                        update_user_meta(user_id_, "primary_blog", blog_id_)
                    # end if
                    if (not get_user_meta(user_id_, "source_domain", True)):
                        update_user_meta(user_id_, "source_domain", details_.domain)
                    # end if
                    break
                # end if
            # end for
        else:
            return
        # end if
        return ret_
    else:
        return primary_
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
def get_user_count(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    return get_network_option(network_id_, "user_count")
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
def get_blog_count(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    return get_network_option(network_id_, "blog_count")
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
def get_blog_post(blog_id_=None, post_id_=None, *_args_):
    
    
    switch_to_blog(blog_id_)
    post_ = get_post(post_id_)
    restore_current_blog()
    return post_
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
def add_user_to_blog(blog_id_=None, user_id_=None, role_=None, *_args_):
    
    
    switch_to_blog(blog_id_)
    user_ = get_userdata(user_id_)
    if (not user_):
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
    can_add_user_ = apply_filters("can_add_user_to_blog", True, user_id_, role_, blog_id_)
    if True != can_add_user_:
        restore_current_blog()
        if is_wp_error(can_add_user_):
            return can_add_user_
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("user_cannot_be_added", __("User cannot be added to this site.")))
    # end if
    if (not get_user_meta(user_id_, "primary_blog", True)):
        update_user_meta(user_id_, "primary_blog", blog_id_)
        site_ = get_site(blog_id_)
        update_user_meta(user_id_, "source_domain", site_.domain)
    # end if
    user_.set_role(role_)
    #// 
    #// Fires immediately after a user is added to a site.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int    $user_id User ID.
    #// @param string $role    User role.
    #// @param int    $blog_id Blog ID.
    #//
    do_action("add_user_to_blog", user_id_, role_, blog_id_)
    clean_user_cache(user_id_)
    wp_cache_delete(blog_id_ + "_user_count", "blog-details")
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
def remove_user_from_blog(user_id_=None, blog_id_=0, reassign_=0, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    switch_to_blog(blog_id_)
    user_id_ = php_int(user_id_)
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
    do_action("remove_user_from_blog", user_id_, blog_id_, reassign_)
    #// If being removed from the primary blog, set a new primary
    #// if the user is assigned to multiple blogs.
    primary_blog_ = get_user_meta(user_id_, "primary_blog", True)
    if primary_blog_ == blog_id_:
        new_id_ = ""
        new_domain_ = ""
        blogs_ = get_blogs_of_user(user_id_)
        for blog_ in blogs_:
            if blog_.userblog_id == blog_id_:
                continue
            # end if
            new_id_ = blog_.userblog_id
            new_domain_ = blog_.domain
            break
        # end for
        update_user_meta(user_id_, "primary_blog", new_id_)
        update_user_meta(user_id_, "source_domain", new_domain_)
    # end if
    #// wp_revoke_user( $user_id );
    user_ = get_userdata(user_id_)
    if (not user_):
        restore_current_blog()
        return php_new_class("WP_Error", lambda : WP_Error("user_does_not_exist", __("That user does not exist.")))
    # end if
    user_.remove_all_caps()
    blogs_ = get_blogs_of_user(user_id_)
    if php_count(blogs_) == 0:
        update_user_meta(user_id_, "primary_blog", "")
        update_user_meta(user_id_, "source_domain", "")
    # end if
    if reassign_:
        reassign_ = php_int(reassign_)
        post_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_author = %d"), user_id_))
        link_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT link_id FROM ") + str(wpdb_.links) + str(" WHERE link_owner = %d"), user_id_))
        if (not php_empty(lambda : post_ids_)):
            wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_author = %d WHERE post_author = %d"), reassign_, user_id_))
            php_array_walk(post_ids_, "clean_post_cache")
        # end if
        if (not php_empty(lambda : link_ids_)):
            wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.links) + str(" SET link_owner = %d WHERE link_owner = %d"), reassign_, user_id_))
            php_array_walk(link_ids_, "clean_bookmark_cache")
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
def get_blog_permalink(blog_id_=None, post_id_=None, *_args_):
    
    
    switch_to_blog(blog_id_)
    link_ = get_permalink(post_id_)
    restore_current_blog()
    return link_
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
def get_blog_id_from_url(domain_=None, path_="/", *_args_):
    
    
    domain_ = php_strtolower(domain_)
    path_ = php_strtolower(path_)
    id_ = wp_cache_get(php_md5(domain_ + path_), "blog-id-cache")
    if -1 == id_:
        #// Blog does not exist.
        return 0
    elif id_:
        return php_int(id_)
    # end if
    args_ = Array({"domain": domain_, "path": path_, "fields": "ids", "number": 1, "update_site_meta_cache": False})
    result_ = get_sites(args_)
    id_ = php_array_shift(result_)
    if (not id_):
        wp_cache_set(php_md5(domain_ + path_), -1, "blog-id-cache")
        return 0
    # end if
    wp_cache_set(php_md5(domain_ + path_), id_, "blog-id-cache")
    return id_
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
def is_email_address_unsafe(user_email_=None, *_args_):
    
    
    banned_names_ = get_site_option("banned_email_domains")
    if banned_names_ and (not php_is_array(banned_names_)):
        banned_names_ = php_explode("\n", banned_names_)
    # end if
    is_email_address_unsafe_ = False
    if banned_names_ and php_is_array(banned_names_) and False != php_strpos(user_email_, "@", 1):
        banned_names_ = php_array_map("strtolower", banned_names_)
        normalized_email_ = php_strtolower(user_email_)
        email_local_part_, email_domain_ = php_explode("@", normalized_email_)
        for banned_domain_ in banned_names_:
            if (not banned_domain_):
                continue
            # end if
            if email_domain_ == banned_domain_:
                is_email_address_unsafe_ = True
                break
            # end if
            dotted_domain_ = str(".") + str(banned_domain_)
            if php_substr(normalized_email_, -php_strlen(dotted_domain_)) == dotted_domain_:
                is_email_address_unsafe_ = True
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
    return apply_filters("is_email_address_unsafe", is_email_address_unsafe_, user_email_)
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
def wpmu_validate_user_signup(user_name_=None, user_email_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    errors_ = php_new_class("WP_Error", lambda : WP_Error())
    orig_username_ = user_name_
    user_name_ = php_preg_replace("/\\s+/", "", sanitize_user(user_name_, True))
    if user_name_ != orig_username_ or php_preg_match("/[^a-z0-9]/", user_name_):
        errors_.add("user_name", __("Usernames can only contain lowercase letters (a-z) and numbers."))
        user_name_ = orig_username_
    # end if
    user_email_ = sanitize_email(user_email_)
    if php_empty(lambda : user_name_):
        errors_.add("user_name", __("Please enter a username."))
    # end if
    illegal_names_ = get_site_option("illegal_names")
    if (not php_is_array(illegal_names_)):
        illegal_names_ = Array("www", "web", "root", "admin", "main", "invite", "administrator")
        add_site_option("illegal_names", illegal_names_)
    # end if
    if php_in_array(user_name_, illegal_names_):
        errors_.add("user_name", __("Sorry, that username is not allowed."))
    # end if
    #// This filter is documented in wp-includes/user.php
    illegal_logins_ = apply_filters("illegal_user_logins", Array())
    if php_in_array(php_strtolower(user_name_), php_array_map("strtolower", illegal_logins_), True):
        errors_.add("user_name", __("Sorry, that username is not allowed."))
    # end if
    if (not is_email(user_email_)):
        errors_.add("user_email", __("Please enter a valid email address."))
    elif is_email_address_unsafe(user_email_):
        errors_.add("user_email", __("You cannot use that email address to signup. We are having problems with them blocking some of our email. Please use another email provider."))
    # end if
    if php_strlen(user_name_) < 4:
        errors_.add("user_name", __("Username must be at least 4 characters."))
    # end if
    if php_strlen(user_name_) > 60:
        errors_.add("user_name", __("Username may not be longer than 60 characters."))
    # end if
    #// All numeric?
    if php_preg_match("/^[0-9]*$/", user_name_):
        errors_.add("user_name", __("Sorry, usernames must have letters too!"))
    # end if
    limited_email_domains_ = get_site_option("limited_email_domains")
    if php_is_array(limited_email_domains_) and (not php_empty(lambda : limited_email_domains_)):
        limited_email_domains_ = php_array_map("strtolower", limited_email_domains_)
        emaildomain_ = php_strtolower(php_substr(user_email_, 1 + php_strpos(user_email_, "@")))
        if (not php_in_array(emaildomain_, limited_email_domains_, True)):
            errors_.add("user_email", __("Sorry, that email address is not allowed!"))
        # end if
    # end if
    #// Check if the username has been used already.
    if username_exists(user_name_):
        errors_.add("user_name", __("Sorry, that username already exists!"))
    # end if
    #// Check if the email address has been used already.
    if email_exists(user_email_):
        errors_.add("user_email", __("Sorry, that email address is already used!"))
    # end if
    #// Has someone already signed up for this username?
    signup_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.signups) + str(" WHERE user_login = %s"), user_name_))
    if None != signup_:
        registered_at_ = mysql2date("U", signup_.registered)
        now_ = time()
        diff_ = now_ - registered_at_
        #// If registered more than two days ago, cancel registration and let this signup go through.
        if diff_ > 2 * DAY_IN_SECONDS:
            wpdb_.delete(wpdb_.signups, Array({"user_login": user_name_}))
        else:
            errors_.add("user_name", __("That username is currently reserved but may be available in a couple of days."))
        # end if
    # end if
    signup_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.signups) + str(" WHERE user_email = %s"), user_email_))
    if None != signup_:
        diff_ = time() - mysql2date("U", signup_.registered)
        #// If registered more than two days ago, cancel registration and let this signup go through.
        if diff_ > 2 * DAY_IN_SECONDS:
            wpdb_.delete(wpdb_.signups, Array({"user_email": user_email_}))
        else:
            errors_.add("user_email", __("That email address has already been used. Please check your inbox for an activation email. It will become available in a couple of days if you do nothing."))
        # end if
    # end if
    result_ = Array({"user_name": user_name_, "orig_username": orig_username_, "user_email": user_email_, "errors": errors_})
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
    return apply_filters("wpmu_validate_user_signup", result_)
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
def wpmu_validate_blog_signup(blogname_=None, blog_title_=None, user_="", *_args_):
    
    
    global wpdb_
    global domain_
    php_check_if_defined("wpdb_","domain_")
    current_network_ = get_network()
    base_ = current_network_.path
    blog_title_ = strip_tags(blog_title_)
    errors_ = php_new_class("WP_Error", lambda : WP_Error())
    illegal_names_ = get_site_option("illegal_names")
    if False == illegal_names_:
        illegal_names_ = Array("www", "web", "root", "admin", "main", "invite", "administrator")
        add_site_option("illegal_names", illegal_names_)
    # end if
    #// 
    #// On sub dir installations, some names are so illegal, only a filter can
    #// spring them from jail.
    #//
    if (not is_subdomain_install()):
        illegal_names_ = php_array_merge(illegal_names_, get_subdirectory_reserved_names())
    # end if
    if php_empty(lambda : blogname_):
        errors_.add("blogname", __("Please enter a site name."))
    # end if
    if php_preg_match("/[^a-z0-9]+/", blogname_):
        errors_.add("blogname", __("Site names can only contain lowercase letters (a-z) and numbers."))
    # end if
    if php_in_array(blogname_, illegal_names_):
        errors_.add("blogname", __("That name is not allowed."))
    # end if
    #// 
    #// Filters the minimum site name length required when validating a site signup.
    #// 
    #// @since 4.8.0
    #// 
    #// @param int $length The minimum site name length. Default 4.
    #//
    minimum_site_name_length_ = apply_filters("minimum_site_name_length", 4)
    if php_strlen(blogname_) < minimum_site_name_length_:
        #// translators: %s: Minimum site name length.
        errors_.add("blogname", php_sprintf(_n("Site name must be at least %s character.", "Site name must be at least %s characters.", minimum_site_name_length_), number_format_i18n(minimum_site_name_length_)))
    # end if
    #// Do not allow users to create a blog that conflicts with a page on the main blog.
    if (not is_subdomain_install()) and wpdb_.get_var(wpdb_.prepare("SELECT post_name FROM " + wpdb_.get_blog_prefix(current_network_.site_id) + "posts WHERE post_type = 'page' AND post_name = %s", blogname_)):
        errors_.add("blogname", __("Sorry, you may not use that site name."))
    # end if
    #// All numeric?
    if php_preg_match("/^[0-9]*$/", blogname_):
        errors_.add("blogname", __("Sorry, site names must have letters too!"))
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
    blogname_ = apply_filters("newblogname", blogname_)
    blog_title_ = wp_unslash(blog_title_)
    if php_empty(lambda : blog_title_):
        errors_.add("blog_title", __("Please enter a site title."))
    # end if
    #// Check if the domain/path has been used already.
    if is_subdomain_install():
        mydomain_ = blogname_ + "." + php_preg_replace("|^www\\.|", "", domain_)
        path_ = base_
    else:
        mydomain_ = str(domain_)
        path_ = base_ + blogname_ + "/"
    # end if
    if domain_exists(mydomain_, path_, current_network_.id):
        errors_.add("blogname", __("Sorry, that site already exists!"))
    # end if
    if username_exists(blogname_):
        if (not php_is_object(user_)) or php_is_object(user_) and user_.user_login != blogname_:
            errors_.add("blogname", __("Sorry, that site is reserved!"))
        # end if
    # end if
    #// Has someone already signed up for this domain?
    #// TODO: Check email too?
    signup_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.signups) + str(" WHERE domain = %s AND path = %s"), mydomain_, path_))
    if (not php_empty(lambda : signup_)):
        diff_ = time() - mysql2date("U", signup_.registered)
        #// If registered more than two days ago, cancel registration and let this signup go through.
        if diff_ > 2 * DAY_IN_SECONDS:
            wpdb_.delete(wpdb_.signups, Array({"domain": mydomain_, "path": path_}))
        else:
            errors_.add("blogname", __("That site is currently reserved but may be available in a couple days."))
        # end if
    # end if
    result_ = Array({"domain": mydomain_, "path": path_, "blogname": blogname_, "blog_title": blog_title_, "user": user_, "errors": errors_})
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
    return apply_filters("wpmu_validate_blog_signup", result_)
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
def wpmu_signup_blog(domain_=None, path_=None, title_=None, user_=None, user_email_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    key_ = php_substr(php_md5(time() + wp_rand() + domain_), 0, 16)
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
    meta_ = apply_filters("signup_site_meta", meta_, domain_, path_, title_, user_, user_email_, key_)
    wpdb_.insert(wpdb_.signups, Array({"domain": domain_, "path": path_, "title": title_, "user_login": user_, "user_email": user_email_, "registered": current_time("mysql", True), "activation_key": key_, "meta": serialize(meta_)}))
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
    do_action("after_signup_site", domain_, path_, title_, user_, user_email_, key_, meta_)
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
def wpmu_signup_user(user_=None, user_email_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Format data.
    user_ = php_preg_replace("/\\s+/", "", sanitize_user(user_, True))
    user_email_ = sanitize_email(user_email_)
    key_ = php_substr(php_md5(time() + wp_rand() + user_email_), 0, 16)
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
    meta_ = apply_filters("signup_user_meta", meta_, user_, user_email_, key_)
    wpdb_.insert(wpdb_.signups, Array({"domain": "", "path": "", "title": "", "user_login": user_, "user_email": user_email_, "registered": current_time("mysql", True), "activation_key": key_, "meta": serialize(meta_)}))
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
    do_action("after_signup_user", user_, user_email_, key_, meta_)
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
def wpmu_signup_blog_notification(domain_=None, path_=None, title_=None, user_login_=None, user_email_=None, key_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
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
    if (not apply_filters("wpmu_signup_blog_notification", domain_, path_, title_, user_login_, user_email_, key_, meta_)):
        return False
    # end if
    #// Send email with activation link.
    if (not is_subdomain_install()) or get_current_network_id() != 1:
        activate_url_ = network_site_url(str("wp-activate.php?key=") + str(key_))
    else:
        activate_url_ = str("http://") + str(domain_) + str(path_) + str("wp-activate.php?key=") + str(key_)
        pass
    # end if
    activate_url_ = esc_url(activate_url_)
    admin_email_ = get_site_option("admin_email")
    if "" == admin_email_:
        admin_email_ = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name_ = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers_ = str("From: \"") + str(from_name_) + str("\" <") + str(admin_email_) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    user_ = get_user_by("login", user_login_)
    switched_locale_ = switch_to_locale(get_user_locale(user_))
    message_ = php_sprintf(apply_filters("wpmu_signup_blog_notification_email", __("""To activate your blog, please click the following link:
    %1$s
    After you activate, you will receive *another email* with your login.
    After you activate, you can visit your site here:
    %2$s"""), domain_, path_, title_, user_login_, user_email_, key_, meta_), activate_url_, esc_url(str("http://") + str(domain_) + str(path_)), key_)
    subject_ = php_sprintf(apply_filters("wpmu_signup_blog_notification_subject", _x("[%1$s] Activate %2$s", "New site notification email subject"), domain_, path_, title_, user_login_, user_email_, key_, meta_), from_name_, esc_url("http://" + domain_ + path_))
    wp_mail(user_email_, wp_specialchars_decode(subject_), message_, message_headers_)
    if switched_locale_:
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
def wpmu_signup_user_notification(user_login_=None, user_email_=None, key_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
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
    if (not apply_filters("wpmu_signup_user_notification", user_login_, user_email_, key_, meta_)):
        return False
    # end if
    user_ = get_user_by("login", user_login_)
    switched_locale_ = switch_to_locale(get_user_locale(user_))
    #// Send email with activation link.
    admin_email_ = get_site_option("admin_email")
    if "" == admin_email_:
        admin_email_ = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name_ = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers_ = str("From: \"") + str(from_name_) + str("\" <") + str(admin_email_) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    message_ = php_sprintf(apply_filters("wpmu_signup_user_notification_email", __("""To activate your user, please click the following link:
    %s
    After you activate, you will receive *another email* with your login."""), user_login_, user_email_, key_, meta_), site_url(str("wp-activate.php?key=") + str(key_)))
    subject_ = php_sprintf(apply_filters("wpmu_signup_user_notification_subject", _x("[%1$s] Activate %2$s", "New user notification email subject"), user_login_, user_email_, key_, meta_), from_name_, user_login_)
    wp_mail(user_email_, wp_specialchars_decode(subject_), message_, message_headers_)
    if switched_locale_:
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
def wpmu_activate_signup(key_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    signup_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.signups) + str(" WHERE activation_key = %s"), key_))
    if php_empty(lambda : signup_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid activation key.")))
    # end if
    if signup_.active:
        if php_empty(lambda : signup_.domain):
            return php_new_class("WP_Error", lambda : WP_Error("already_active", __("The user is already active."), signup_))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("already_active", __("The site is already active."), signup_))
        # end if
    # end if
    meta_ = maybe_unserialize(signup_.meta)
    password_ = wp_generate_password(12, False)
    user_id_ = username_exists(signup_.user_login)
    if (not user_id_):
        user_id_ = wpmu_create_user(signup_.user_login, password_, signup_.user_email)
    else:
        user_already_exists_ = True
    # end if
    if (not user_id_):
        return php_new_class("WP_Error", lambda : WP_Error("create_user", __("Could not create user"), signup_))
    # end if
    now_ = current_time("mysql", True)
    if php_empty(lambda : signup_.domain):
        wpdb_.update(wpdb_.signups, Array({"active": 1, "activated": now_}), Array({"activation_key": key_}))
        if (php_isset(lambda : user_already_exists_)):
            return php_new_class("WP_Error", lambda : WP_Error("user_already_exists", __("That username is already activated."), signup_))
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
        do_action("wpmu_activate_user", user_id_, password_, meta_)
        return Array({"user_id": user_id_, "password": password_, "meta": meta_})
    # end if
    blog_id_ = wpmu_create_blog(signup_.domain, signup_.path, signup_.title, user_id_, meta_, get_current_network_id())
    #// TODO: What to do if we create a user but cannot create a blog?
    if is_wp_error(blog_id_):
        #// 
        #// If blog is taken, that means a previous attempt to activate this blog
        #// failed in between creating the blog and setting the activation flag.
        #// Let's just set the active flag and instruct the user to reset their password.
        #//
        if "blog_taken" == blog_id_.get_error_code():
            blog_id_.add_data(signup_)
            wpdb_.update(wpdb_.signups, Array({"active": 1, "activated": now_}), Array({"activation_key": key_}))
        # end if
        return blog_id_
    # end if
    wpdb_.update(wpdb_.signups, Array({"active": 1, "activated": now_}), Array({"activation_key": key_}))
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
    do_action("wpmu_activate_blog", blog_id_, user_id_, password_, signup_.title, meta_)
    return Array({"blog_id": blog_id_, "user_id": user_id_, "password": password_, "title": signup_.title, "meta": meta_})
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
def wpmu_create_user(user_name_=None, password_=None, email_=None, *_args_):
    
    
    user_name_ = php_preg_replace("/\\s+/", "", sanitize_user(user_name_, True))
    user_id_ = wp_create_user(user_name_, password_, email_)
    if is_wp_error(user_id_):
        return False
    # end if
    #// Newly created users have no roles or caps until they are added to a blog.
    delete_user_option(user_id_, "capabilities")
    delete_user_option(user_id_, "user_level")
    #// 
    #// Fires immediately after a new user is created.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int $user_id User ID.
    #//
    do_action("wpmu_new_user", user_id_)
    return user_id_
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
def wpmu_create_blog(domain_=None, path_=None, title_=None, user_id_=None, options_=None, network_id_=1, *_args_):
    if options_ is None:
        options_ = Array()
    # end if
    
    defaults_ = Array({"public": 0})
    options_ = wp_parse_args(options_, defaults_)
    title_ = strip_tags(title_)
    user_id_ = php_int(user_id_)
    #// Check if the domain has been used already. We should return an error message.
    if domain_exists(domain_, path_, network_id_):
        return php_new_class("WP_Error", lambda : WP_Error("blog_taken", __("Sorry, that site already exists!")))
    # end if
    if (not wp_installing()):
        wp_installing(True)
    # end if
    site_data_whitelist_ = Array("public", "archived", "mature", "spam", "deleted", "lang_id")
    site_data_ = php_array_merge(Array({"domain": domain_, "path": path_, "network_id": network_id_}), php_array_intersect_key(options_, php_array_flip(site_data_whitelist_)))
    #// Data to pass to wp_initialize_site().
    site_initialization_data_ = Array({"title": title_, "user_id": user_id_, "options": php_array_diff_key(options_, php_array_flip(site_data_whitelist_))})
    blog_id_ = wp_insert_site(php_array_merge(site_data_, site_initialization_data_))
    if is_wp_error(blog_id_):
        return blog_id_
    # end if
    wp_cache_set("last_changed", php_microtime(), "sites")
    return blog_id_
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
def newblog_notify_siteadmin(blog_id_=None, deprecated_="", *_args_):
    
    
    if php_is_object(blog_id_):
        blog_id_ = blog_id_.blog_id
    # end if
    if get_site_option("registrationnotification") != "yes":
        return False
    # end if
    email_ = get_site_option("admin_email")
    if is_email(email_) == False:
        return False
    # end if
    options_site_url_ = esc_url(network_admin_url("settings.php"))
    switch_to_blog(blog_id_)
    blogname_ = get_option("blogname")
    siteurl_ = site_url()
    restore_current_blog()
    msg_ = php_sprintf(__("""New Site: %1$s
    URL: %2$s
    Remote IP address: %3$s
    Disable these notifications: %4$s"""), blogname_, siteurl_, wp_unslash(PHP_SERVER["REMOTE_ADDR"]), options_site_url_)
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
    msg_ = apply_filters("newblog_notify_siteadmin", msg_, blog_id_)
    #// translators: New site notification email subject. %s: New site URL.
    wp_mail(email_, php_sprintf(__("New Site Registration: %s"), siteurl_), msg_)
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
def newuser_notify_siteadmin(user_id_=None, *_args_):
    
    
    if get_site_option("registrationnotification") != "yes":
        return False
    # end if
    email_ = get_site_option("admin_email")
    if is_email(email_) == False:
        return False
    # end if
    user_ = get_userdata(user_id_)
    options_site_url_ = esc_url(network_admin_url("settings.php"))
    msg_ = php_sprintf(__("""New User: %1$s
    Remote IP address: %2$s
    Disable these notifications: %3$s"""), user_.user_login, wp_unslash(PHP_SERVER["REMOTE_ADDR"]), options_site_url_)
    #// 
    #// Filters the message body of the new user activation email sent
    #// to the network administrator.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string  $msg  Email body.
    #// @param WP_User $user WP_User instance of the new user.
    #//
    msg_ = apply_filters("newuser_notify_siteadmin", msg_, user_)
    #// translators: New user notification email subject. %s: User login.
    wp_mail(email_, php_sprintf(__("New User Registration: %s"), user_.user_login), msg_)
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
def domain_exists(domain_=None, path_=None, network_id_=1, *_args_):
    
    
    path_ = trailingslashit(path_)
    args_ = Array({"network_id": network_id_, "domain": domain_, "path": path_, "fields": "ids", "number": 1, "update_site_meta_cache": False})
    result_ = get_sites(args_)
    result_ = php_array_shift(result_)
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
    return apply_filters("domain_exists", result_, domain_, path_, network_id_)
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
def wpmu_welcome_notification(blog_id_=None, user_id_=None, password_=None, title_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    current_network_ = get_network()
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
    if (not apply_filters("wpmu_welcome_notification", blog_id_, user_id_, password_, title_, meta_)):
        return False
    # end if
    user_ = get_userdata(user_id_)
    switched_locale_ = switch_to_locale(get_user_locale(user_))
    welcome_email_ = get_site_option("welcome_email")
    if False == welcome_email_:
        #// translators: Do not translate USERNAME, SITE_NAME, BLOG_URL, PASSWORD: those are placeholders.
        welcome_email_ = __("""Howdy USERNAME,
        Your new SITE_NAME site has been successfully set up at:
        BLOG_URL
        You can log in to the administrator account with the following information:
        Username: USERNAME
        Password: PASSWORD
        Log in here: BLOG_URLwp-login.php
        We hope you enjoy your new site. Thanks!
        --The Team @ SITE_NAME""")
    # end if
    url_ = get_blogaddress_by_id(blog_id_)
    welcome_email_ = php_str_replace("SITE_NAME", current_network_.site_name, welcome_email_)
    welcome_email_ = php_str_replace("BLOG_TITLE", title_, welcome_email_)
    welcome_email_ = php_str_replace("BLOG_URL", url_, welcome_email_)
    welcome_email_ = php_str_replace("USERNAME", user_.user_login, welcome_email_)
    welcome_email_ = php_str_replace("PASSWORD", password_, welcome_email_)
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
    welcome_email_ = apply_filters("update_welcome_email", welcome_email_, blog_id_, user_id_, password_, title_, meta_)
    admin_email_ = get_site_option("admin_email")
    if "" == admin_email_:
        admin_email_ = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name_ = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers_ = str("From: \"") + str(from_name_) + str("\" <") + str(admin_email_) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    message_ = welcome_email_
    if php_empty(lambda : current_network_.site_name):
        current_network_.site_name = "WordPress"
    # end if
    #// translators: New site notification email subject. 1: Network title, 2: New site title.
    subject_ = __("New %1$s Site: %2$s")
    #// 
    #// Filters the subject of the welcome email after site activation.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $subject Subject of the email.
    #//
    subject_ = apply_filters("update_welcome_subject", php_sprintf(subject_, current_network_.site_name, wp_unslash(title_)))
    wp_mail(user_.user_email, wp_specialchars_decode(subject_), message_, message_headers_)
    if switched_locale_:
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
def wpmu_welcome_user_notification(user_id_=None, password_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    current_network_ = get_network()
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
    if (not apply_filters("wpmu_welcome_user_notification", user_id_, password_, meta_)):
        return False
    # end if
    welcome_email_ = get_site_option("welcome_user_email")
    user_ = get_userdata(user_id_)
    switched_locale_ = switch_to_locale(get_user_locale(user_))
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
    welcome_email_ = apply_filters("update_welcome_user_email", welcome_email_, user_id_, password_, meta_)
    welcome_email_ = php_str_replace("SITE_NAME", current_network_.site_name, welcome_email_)
    welcome_email_ = php_str_replace("USERNAME", user_.user_login, welcome_email_)
    welcome_email_ = php_str_replace("PASSWORD", password_, welcome_email_)
    welcome_email_ = php_str_replace("LOGINLINK", wp_login_url(), welcome_email_)
    admin_email_ = get_site_option("admin_email")
    if "" == admin_email_:
        admin_email_ = "support@" + PHP_SERVER["SERVER_NAME"]
    # end if
    from_name_ = "WordPress" if get_site_option("site_name") == "" else esc_html(get_site_option("site_name"))
    message_headers_ = str("From: \"") + str(from_name_) + str("\" <") + str(admin_email_) + str(">\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
    message_ = welcome_email_
    if php_empty(lambda : current_network_.site_name):
        current_network_.site_name = "WordPress"
    # end if
    #// translators: New user notification email subject. 1: Network title, 2: New user login.
    subject_ = __("New %1$s User: %2$s")
    #// 
    #// Filters the subject of the welcome email after user activation.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $subject Subject of the email.
    #//
    subject_ = apply_filters("update_welcome_user_subject", php_sprintf(subject_, current_network_.site_name, user_.user_login))
    wp_mail(user_.user_email, wp_specialchars_decode(subject_), message_, message_headers_)
    if switched_locale_:
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
def get_current_site(*_args_):
    
    
    global current_site_
    php_check_if_defined("current_site_")
    return current_site_
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
def get_most_recent_post_of_user(user_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    user_blogs_ = get_blogs_of_user(php_int(user_id_))
    most_recent_post_ = Array()
    #// Walk through each blog and get the most recent post
    #// published by $user_id.
    for blog_ in user_blogs_:
        prefix_ = wpdb_.get_blog_prefix(blog_.userblog_id)
        recent_post_ = wpdb_.get_row(wpdb_.prepare(str("SELECT ID, post_date_gmt FROM ") + str(prefix_) + str("posts WHERE post_author = %d AND post_type = 'post' AND post_status = 'publish' ORDER BY post_date_gmt DESC LIMIT 1"), user_id_), ARRAY_A)
        #// Make sure we found a post.
        if (php_isset(lambda : recent_post_["ID"])):
            post_gmt_ts_ = strtotime(recent_post_["post_date_gmt"])
            #// 
            #// If this is the first post checked
            #// or if this post is newer than the current recent post,
            #// make it the new most recent post.
            #//
            if (not (php_isset(lambda : most_recent_post_["post_gmt_ts"]))) or post_gmt_ts_ > most_recent_post_["post_gmt_ts"]:
                most_recent_post_ = Array({"blog_id": blog_.userblog_id, "post_id": recent_post_["ID"], "post_date_gmt": recent_post_["post_date_gmt"], "post_gmt_ts": post_gmt_ts_})
            # end if
        # end if
    # end for
    return most_recent_post_
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
def check_upload_mimes(mimes_=None, *_args_):
    
    
    site_exts_ = php_explode(" ", get_site_option("upload_filetypes", "jpg jpeg png gif"))
    site_mimes_ = Array()
    for ext_ in site_exts_:
        for ext_pattern_,mime_ in mimes_:
            if "" != ext_ and False != php_strpos(ext_pattern_, ext_):
                site_mimes_[ext_pattern_] = mime_
            # end if
        # end for
    # end for
    return site_mimes_
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
def update_posts_count(deprecated_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    update_option("post_count", php_int(wpdb_.get_var(str("SELECT COUNT(ID) FROM ") + str(wpdb_.posts) + str(" WHERE post_status = 'publish' and post_type = 'post'"))))
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
def wpmu_log_new_registrations(blog_id_=None, user_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_is_object(blog_id_):
        blog_id_ = blog_id_.blog_id
    # end if
    if php_is_array(user_id_):
        user_id_ = user_id_["user_id"] if (not php_empty(lambda : user_id_["user_id"])) else 0
    # end if
    user_ = get_userdata(php_int(user_id_))
    if user_:
        wpdb_.insert(wpdb_.registration_log, Array({"email": user_.user_email, "IP": php_preg_replace("/[^0-9., ]/", "", wp_unslash(PHP_SERVER["REMOTE_ADDR"])), "blog_id": blog_id_, "date_registered": current_time("mysql")}))
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
def global_terms(term_id_=None, deprecated_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    global_terms_recurse_ = None
    if (not global_terms_enabled()):
        return term_id_
    # end if
    #// Prevent a race condition.
    recurse_start_ = False
    if None == global_terms_recurse_:
        recurse_start_ = True
        global_terms_recurse_ = 1
    elif 10 < global_terms_recurse_:
        global_terms_recurse_ += 1
        return term_id_
        global_terms_recurse_ += 1
    # end if
    term_id_ = php_intval(term_id_)
    c_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.terms) + str(" WHERE term_id = %d"), term_id_))
    global_id_ = wpdb_.get_var(wpdb_.prepare(str("SELECT cat_ID FROM ") + str(wpdb_.sitecategories) + str(" WHERE category_nicename = %s"), c_.slug))
    if None == global_id_:
        used_global_id_ = wpdb_.get_var(wpdb_.prepare(str("SELECT cat_ID FROM ") + str(wpdb_.sitecategories) + str(" WHERE cat_ID = %d"), c_.term_id))
        if None == used_global_id_:
            wpdb_.insert(wpdb_.sitecategories, Array({"cat_ID": term_id_, "cat_name": c_.name, "category_nicename": c_.slug}))
            global_id_ = wpdb_.insert_id
            if php_empty(lambda : global_id_):
                return term_id_
            # end if
        else:
            max_global_id_ = wpdb_.get_var(str("SELECT MAX(cat_ID) FROM ") + str(wpdb_.sitecategories))
            max_local_id_ = wpdb_.get_var(str("SELECT MAX(term_id) FROM ") + str(wpdb_.terms))
            new_global_id_ = php_max(max_global_id_, max_local_id_) + mt_rand(100, 400)
            wpdb_.insert(wpdb_.sitecategories, Array({"cat_ID": new_global_id_, "cat_name": c_.name, "category_nicename": c_.slug}))
            global_id_ = wpdb_.insert_id
        # end if
    elif global_id_ != term_id_:
        local_id_ = wpdb_.get_var(wpdb_.prepare(str("SELECT term_id FROM ") + str(wpdb_.terms) + str(" WHERE term_id = %d"), global_id_))
        if None != local_id_:
            global_terms(local_id_)
            if 10 < global_terms_recurse_:
                global_id_ = term_id_
            # end if
        # end if
    # end if
    if global_id_ != term_id_:
        if get_option("default_category") == term_id_:
            update_option("default_category", global_id_)
        # end if
        wpdb_.update(wpdb_.terms, Array({"term_id": global_id_}), Array({"term_id": term_id_}))
        wpdb_.update(wpdb_.term_taxonomy, Array({"term_id": global_id_}), Array({"term_id": term_id_}))
        wpdb_.update(wpdb_.term_taxonomy, Array({"parent": global_id_}), Array({"parent": term_id_}))
        clean_term_cache(term_id_)
    # end if
    if recurse_start_:
        global_terms_recurse_ = None
    # end if
    return global_id_
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
def redirect_this_site(deprecated_="", *_args_):
    
    
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
def upload_is_file_too_big(upload_=None, *_args_):
    
    
    if (not php_is_array(upload_)) or php_defined("WP_IMPORTING") or get_site_option("upload_space_check_disabled"):
        return upload_
    # end if
    if php_strlen(upload_["bits"]) > KB_IN_BYTES * get_site_option("fileupload_maxk", 1500):
        #// translators: %s: Maximum allowed file size in kilobytes.
        return php_sprintf(__("This file is too big. Files must be less than %s KB in size.") + "<br />", get_site_option("fileupload_maxk", 1500))
    # end if
    return upload_
# end def upload_is_file_too_big
#// 
#// Add a nonce field to the signup page.
#// 
#// @since MU (3.0.0)
#//
def signup_nonce_fields(*_args_):
    
    
    id_ = mt_rand()
    php_print(str("<input type='hidden' name='signup_form_id' value='") + str(id_) + str("' />"))
    wp_nonce_field("signup_form_" + id_, "_signup_form", False)
# end def signup_nonce_fields
#// 
#// Process the signup nonce created in signup_nonce_fields().
#// 
#// @since MU (3.0.0)
#// 
#// @param array $result
#// @return array
#//
def signup_nonce_check(result_=None, *_args_):
    
    
    if (not php_strpos(PHP_SERVER["PHP_SELF"], "wp-signup.php")):
        return result_
    # end if
    if (not wp_verify_nonce(PHP_POST["_signup_form"], "signup_form_" + PHP_POST["signup_form_id"])):
        result_["errors"].add("invalid_nonce", __("Unable to submit this form, please try again."))
    # end if
    return result_
# end def signup_nonce_check
#// 
#// Correct 404 redirects when NOBLOGREDIRECT is defined.
#// 
#// @since MU (3.0.0)
#//
def maybe_redirect_404(*_args_):
    
    
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
        destination_ = apply_filters("blog_redirect_404", NOBLOGREDIRECT)
        if destination_:
            if "%siteurl%" == destination_:
                destination_ = network_home_url()
            # end if
            wp_redirect(destination_)
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
def maybe_add_existing_user_to_blog(*_args_):
    
    
    if False == php_strpos(PHP_SERVER["REQUEST_URI"], "/newbloguser/"):
        return
    # end if
    parts_ = php_explode("/", PHP_SERVER["REQUEST_URI"])
    key_ = php_array_pop(parts_)
    if "" == key_:
        key_ = php_array_pop(parts_)
    # end if
    details_ = get_option("new_user_" + key_)
    if (not php_empty(lambda : details_)):
        delete_option("new_user_" + key_)
    # end if
    if php_empty(lambda : details_) or is_wp_error(add_existing_user_to_blog(details_)):
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
def add_existing_user_to_blog(details_=None, *_args_):
    if details_ is None:
        details_ = False
    # end if
    
    if php_is_array(details_):
        blog_id_ = get_current_blog_id()
        result_ = add_user_to_blog(blog_id_, details_["user_id"], details_["role"])
        #// 
        #// Fires immediately after an existing user is added to a site.
        #// 
        #// @since MU (3.0.0)
        #// 
        #// @param int           $user_id User ID.
        #// @param true|WP_Error $result  True on success or a WP_Error object if the user doesn't exist
        #// or could not be added.
        #//
        do_action("added_existing_user", details_["user_id"], result_)
        return result_
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
def add_new_user_to_blog(user_id_=None, password_=None, meta_=None, *_args_):
    
    
    if (not php_empty(lambda : meta_["add_to_blog"])):
        blog_id_ = meta_["add_to_blog"]
        role_ = meta_["new_role"]
        remove_user_from_blog(user_id_, get_network().site_id)
        #// Remove user from main blog.
        result_ = add_user_to_blog(blog_id_, user_id_, role_)
        if (not is_wp_error(result_)):
            update_user_meta(user_id_, "primary_blog", blog_id_)
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
def fix_phpmailer_messageid(phpmailer_=None, *_args_):
    
    
    phpmailer_.Hostname = get_network().domain
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
def is_user_spammy(user_=None, *_args_):
    if user_ is None:
        user_ = None
    # end if
    
    if (not type(user_).__name__ == "WP_User"):
        if user_:
            user_ = get_user_by("login", user_)
        else:
            user_ = wp_get_current_user()
        # end if
    # end if
    return user_ and (php_isset(lambda : user_.spam)) and 1 == user_.spam
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
def update_blog_public(old_value_=None, value_=None, *_args_):
    
    
    update_blog_status(get_current_blog_id(), "public", php_int(value_))
# end def update_blog_public
#// 
#// Check whether users can self-register, based on Network settings.
#// 
#// @since MU (3.0.0)
#// 
#// @return bool
#//
def users_can_register_signup_filter(*_args_):
    
    
    registration_ = get_site_option("registration")
    return "all" == registration_ or "user" == registration_
# end def users_can_register_signup_filter
#// 
#// Ensure that the welcome message is not empty. Currently unused.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $text
#// @return string
#//
def welcome_user_msg_filter(text_=None, *_args_):
    
    
    if (not text_):
        remove_filter("site_option_welcome_user_email", "welcome_user_msg_filter")
        #// translators: Do not translate USERNAME, PASSWORD, LOGINLINK, SITE_NAME: those are placeholders.
        text_ = __("""Howdy USERNAME,
        Your new account is set up.
        You can log in with the following information:
        Username: USERNAME
        Password: PASSWORD
        LOGINLINK
        Thanks!
        --The Team @ SITE_NAME""")
        update_site_option("welcome_user_email", text_)
    # end if
    return text_
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
def force_ssl_content(force_="", *_args_):
    
    
    forced_content_ = False
    if "" != force_:
        old_forced_ = forced_content_
        forced_content_ = force_
        return old_forced_
    # end if
    return forced_content_
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
def filter_SSL(url_=None, *_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    if (not php_is_string(url_)):
        return get_bloginfo("url")
        pass
    # end if
    if force_ssl_content() and is_ssl():
        url_ = set_url_scheme(url_, "https")
    # end if
    return url_
# end def filter_SSL
#// 
#// Schedule update of the network-wide counts for the current network.
#// 
#// @since 3.1.0
#//
def wp_schedule_update_network_counts(*_args_):
    
    
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
def wp_update_network_counts(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    wp_update_network_user_counts(network_id_)
    wp_update_network_site_counts(network_id_)
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
def wp_maybe_update_network_site_counts(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    is_small_network_ = (not wp_is_large_network("sites", network_id_))
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
    if (not apply_filters("enable_live_network_counts", is_small_network_, "sites")):
        return
    # end if
    wp_update_network_site_counts(network_id_)
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
def wp_maybe_update_network_user_counts(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    is_small_network_ = (not wp_is_large_network("users", network_id_))
    #// This filter is documented in wp-includes/ms-functions.php
    if (not apply_filters("enable_live_network_counts", is_small_network_, "users")):
        return
    # end if
    wp_update_network_user_counts(network_id_)
# end def wp_maybe_update_network_user_counts
#// 
#// Update the network-wide site count.
#// 
#// @since 3.7.0
#// @since 4.8.0 The `$network_id` parameter has been added.
#// 
#// @param int|null $network_id ID of the network. Default is the current network.
#//
def wp_update_network_site_counts(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    network_id_ = php_int(network_id_)
    if (not network_id_):
        network_id_ = get_current_network_id()
    # end if
    count_ = get_sites(Array({"network_id": network_id_, "spam": 0, "deleted": 0, "archived": 0, "count": True, "update_site_meta_cache": False}))
    update_network_option(network_id_, "blog_count", count_)
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
def wp_update_network_user_counts(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    count_ = wpdb_.get_var(str("SELECT COUNT(ID) as c FROM ") + str(wpdb_.users) + str(" WHERE spam = '0' AND deleted = '0'"))
    update_network_option(network_id_, "user_count", count_)
# end def wp_update_network_user_counts
#// 
#// Returns the space used by the current site.
#// 
#// @since 3.5.0
#// 
#// @return int Used space in megabytes.
#//
def get_space_used(*_args_):
    
    
    #// 
    #// Filters the amount of storage space used by the current site, in megabytes.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int|false $space_used The amount of used space, in megabytes. Default false.
    #//
    space_used_ = apply_filters("pre_get_space_used", False)
    if False == space_used_:
        upload_dir_ = wp_upload_dir()
        space_used_ = get_dirsize(upload_dir_["basedir"]) / MB_IN_BYTES
    # end if
    return space_used_
# end def get_space_used
#// 
#// Returns the upload quota for the current blog.
#// 
#// @since MU (3.0.0)
#// 
#// @return int Quota in megabytes
#//
def get_space_allowed(*_args_):
    
    
    space_allowed_ = get_option("blog_upload_space")
    if (not php_is_numeric(space_allowed_)):
        space_allowed_ = get_site_option("blog_upload_space")
    # end if
    if (not php_is_numeric(space_allowed_)):
        space_allowed_ = 100
    # end if
    #// 
    #// Filters the upload quota for the current site.
    #// 
    #// @since 3.7.0
    #// 
    #// @param int $space_allowed Upload quota in megabytes for the current blog.
    #//
    return apply_filters("get_space_allowed", space_allowed_)
# end def get_space_allowed
#// 
#// Determines if there is any upload space left in the current blog's quota.
#// 
#// @since 3.0.0
#// 
#// @return int of upload space available in bytes
#//
def get_upload_space_available(*_args_):
    
    
    allowed_ = get_space_allowed()
    if allowed_ < 0:
        allowed_ = 0
    # end if
    space_allowed_ = allowed_ * MB_IN_BYTES
    if get_site_option("upload_space_check_disabled"):
        return space_allowed_
    # end if
    space_used_ = get_space_used() * MB_IN_BYTES
    if space_allowed_ - space_used_ <= 0:
        return 0
    # end if
    return space_allowed_ - space_used_
# end def get_upload_space_available
#// 
#// Determines if there is any upload space left in the current blog's quota.
#// 
#// @since 3.0.0
#// @return bool True if space is available, false otherwise.
#//
def is_upload_space_available(*_args_):
    
    
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
def upload_size_limit_filter(size_=None, *_args_):
    
    
    fileupload_maxk_ = KB_IN_BYTES * get_site_option("fileupload_maxk", 1500)
    if get_site_option("upload_space_check_disabled"):
        return php_min(size_, fileupload_maxk_)
    # end if
    return php_min(size_, fileupload_maxk_, get_upload_space_available())
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
def wp_is_large_network(using_="sites", network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    network_id_ = php_int(network_id_)
    if (not network_id_):
        network_id_ = get_current_network_id()
    # end if
    if "users" == using_:
        count_ = get_user_count(network_id_)
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
        return apply_filters("wp_is_large_network", count_ > 10000, "users", count_, network_id_)
    # end if
    count_ = get_blog_count(network_id_)
    #// This filter is documented in wp-includes/ms-functions.php
    return apply_filters("wp_is_large_network", count_ > 10000, "sites", count_, network_id_)
# end def wp_is_large_network
#// 
#// Retrieves a list of reserved site on a sub-directory Multisite installation.
#// 
#// @since 4.4.0
#// 
#// @return string[] Array of reserved names.
#//
def get_subdirectory_reserved_names(*_args_):
    
    
    names_ = Array("page", "comments", "blog", "files", "feed", "wp-admin", "wp-content", "wp-includes", "wp-json", "embed")
    #// 
    #// Filters reserved site names on a sub-directory Multisite installation.
    #// 
    #// @since 3.0.0
    #// @since 4.4.0 'wp-admin', 'wp-content', 'wp-includes', 'wp-json', and 'embed' were added
    #// to the reserved names list.
    #// 
    #// @param string[] $subdirectory_reserved_names Array of reserved names.
    #//
    return apply_filters("subdirectory_reserved_names", names_)
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
def update_network_option_new_admin_email(old_value_=None, value_=None, *_args_):
    
    
    if get_site_option("admin_email") == value_ or (not is_email(value_)):
        return
    # end if
    hash_ = php_md5(value_ + time() + mt_rand())
    new_admin_email_ = Array({"hash": hash_, "newemail": value_})
    update_site_option("network_admin_hash", new_admin_email_)
    switched_locale_ = switch_to_locale(get_user_locale())
    #// translators: Do not translate USERNAME, ADMIN_URL, EMAIL, SITENAME, SITEURL: those are placeholders.
    email_text_ = __("""Howdy ###USERNAME###,
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
    content_ = apply_filters("new_network_admin_email_content", email_text_, new_admin_email_)
    current_user_ = wp_get_current_user()
    content_ = php_str_replace("###USERNAME###", current_user_.user_login, content_)
    content_ = php_str_replace("###ADMIN_URL###", esc_url(network_admin_url("settings.php?network_admin_hash=" + hash_)), content_)
    content_ = php_str_replace("###EMAIL###", value_, content_)
    content_ = php_str_replace("###SITENAME###", wp_specialchars_decode(get_site_option("site_name"), ENT_QUOTES), content_)
    content_ = php_str_replace("###SITEURL###", network_home_url(), content_)
    wp_mail(value_, php_sprintf(__("[%s] Network Admin Email Change Request"), wp_specialchars_decode(get_site_option("site_name"), ENT_QUOTES)), content_)
    if switched_locale_:
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
def wp_network_admin_email_change_notification(option_name_=None, new_email_=None, old_email_=None, network_id_=None, *_args_):
    
    
    send_ = True
    #// Don't send the notification to the default 'admin_email' value.
    if "you@example.com" == old_email_:
        send_ = False
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
    send_ = apply_filters("send_network_admin_email_change_email", send_, old_email_, new_email_, network_id_)
    if (not send_):
        return
    # end if
    #// translators: Do not translate OLD_EMAIL, NEW_EMAIL, SITENAME, SITEURL: those are placeholders.
    email_change_text_ = __("""Hi,
    This notice confirms that the network admin email address was changed on ###SITENAME###.
    The new network admin email address is ###NEW_EMAIL###.
    This email has been sent to ###OLD_EMAIL###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    email_change_email_ = Array({"to": old_email_, "subject": __("[%s] Network Admin Email Changed"), "message": email_change_text_, "headers": ""})
    #// Get network name.
    network_name_ = wp_specialchars_decode(get_site_option("site_name"), ENT_QUOTES)
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
    email_change_email_ = apply_filters("network_admin_email_change_email", email_change_email_, old_email_, new_email_, network_id_)
    email_change_email_["message"] = php_str_replace("###OLD_EMAIL###", old_email_, email_change_email_["message"])
    email_change_email_["message"] = php_str_replace("###NEW_EMAIL###", new_email_, email_change_email_["message"])
    email_change_email_["message"] = php_str_replace("###SITENAME###", network_name_, email_change_email_["message"])
    email_change_email_["message"] = php_str_replace("###SITEURL###", home_url(), email_change_email_["message"])
    wp_mail(email_change_email_["to"], php_sprintf(email_change_email_["subject"], network_name_), email_change_email_["message"], email_change_email_["headers"])
# end def wp_network_admin_email_change_notification
