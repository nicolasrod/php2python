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
#// Core User API
#// 
#// @package WordPress
#// @subpackage Users
#// 
#// 
#// Authenticates and logs a user in with 'remember' capability.
#// 
#// The credentials is an array that has 'user_login', 'user_password', and
#// 'remember' indices. If the credentials is not given, then the log in form
#// will be assumed and used if set.
#// 
#// The various authentication cookies will be set by this function and will be
#// set for a longer period depending on if the 'remember' credential is set to
#// true.
#// 
#// Note: wp_signon() doesn't handle setting the current user. This means that if the
#// function is called before the {@see 'init'} hook is fired, is_user_logged_in() will
#// evaluate as false until that point. If is_user_logged_in() is needed in conjunction
#// with wp_signon(), wp_set_current_user() should be called explicitly.
#// 
#// @since 2.5.0
#// 
#// @global string $auth_secure_cookie
#// 
#// @param array       $credentials   Optional. User info in order to sign on.
#// @param string|bool $secure_cookie Optional. Whether to use secure cookie.
#// @return WP_User|WP_Error WP_User on success, WP_Error on failure.
#//
def wp_signon(credentials_=None, secure_cookie_="", *_args_):
    if credentials_ is None:
        credentials_ = Array()
    # end if
    
    if php_empty(lambda : credentials_):
        credentials_ = Array()
        #// Back-compat for plugins passing an empty string.
        if (not php_empty(lambda : PHP_POST["log"])):
            credentials_["user_login"] = wp_unslash(PHP_POST["log"])
        # end if
        if (not php_empty(lambda : PHP_POST["pwd"])):
            credentials_["user_password"] = PHP_POST["pwd"]
        # end if
        if (not php_empty(lambda : PHP_POST["rememberme"])):
            credentials_["remember"] = PHP_POST["rememberme"]
        # end if
    # end if
    if (not php_empty(lambda : credentials_["remember"])):
        credentials_["remember"] = True
    else:
        credentials_["remember"] = False
    # end if
    #// 
    #// Fires before the user is authenticated.
    #// 
    #// The variables passed to the callbacks are passed by reference,
    #// and can be modified by callback functions.
    #// 
    #// @since 1.5.1
    #// 
    #// @todo Decide whether to deprecate the wp_authenticate action.
    #// 
    #// @param string $user_login    Username (passed by reference).
    #// @param string $user_password User password (passed by reference).
    #//
    do_action_ref_array("wp_authenticate", Array(credentials_["user_login"], credentials_["user_password"]))
    if "" == secure_cookie_:
        secure_cookie_ = is_ssl()
    # end if
    #// 
    #// Filters whether to use a secure sign-on cookie.
    #// 
    #// @since 3.1.0
    #// 
    #// @param bool  $secure_cookie Whether to use a secure sign-on cookie.
    #// @param array $credentials {
    #// Array of entered sign-on data.
    #// 
    #// @type string $user_login    Username.
    #// @type string $user_password Password entered.
    #// @type bool   $remember      Whether to 'remember' the user. Increases the time
    #// that the cookie will be kept. Default false.
    #// }
    #//
    secure_cookie_ = apply_filters("secure_signon_cookie", secure_cookie_, credentials_)
    global auth_secure_cookie_
    php_check_if_defined("auth_secure_cookie_")
    #// XXX ugly hack to pass this to wp_authenticate_cookie().
    auth_secure_cookie_ = secure_cookie_
    add_filter("authenticate", "wp_authenticate_cookie", 30, 3)
    user_ = wp_authenticate(credentials_["user_login"], credentials_["user_password"])
    if is_wp_error(user_):
        return user_
    # end if
    wp_set_auth_cookie(user_.ID, credentials_["remember"], secure_cookie_)
    #// 
    #// Fires after the user has successfully logged in.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $user_login Username.
    #// @param WP_User $user       WP_User object of the logged-in user.
    #//
    do_action("wp_login", user_.user_login, user_)
    return user_
# end def wp_signon
#// 
#// Authenticate a user, confirming the username and password are valid.
#// 
#// @since 2.8.0
#// 
#// @param WP_User|WP_Error|null $user     WP_User or WP_Error object from a previous callback. Default null.
#// @param string                $username Username for authentication.
#// @param string                $password Password for authentication.
#// @return WP_User|WP_Error WP_User on success, WP_Error on failure.
#//
def wp_authenticate_username_password(user_=None, username_=None, password_=None, *_args_):
    
    
    if type(user_).__name__ == "WP_User":
        return user_
    # end if
    if php_empty(lambda : username_) or php_empty(lambda : password_):
        if is_wp_error(user_):
            return user_
        # end if
        error_ = php_new_class("WP_Error", lambda : WP_Error())
        if php_empty(lambda : username_):
            error_.add("empty_username", __("<strong>Error</strong>: The username field is empty."))
        # end if
        if php_empty(lambda : password_):
            error_.add("empty_password", __("<strong>Error</strong>: The password field is empty."))
        # end if
        return error_
    # end if
    user_ = get_user_by("login", username_)
    if (not user_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_username", __("Unknown username. Check again or try your email address.")))
    # end if
    #// 
    #// Filters whether the given user can be authenticated with the provided $password.
    #// 
    #// @since 2.5.0
    #// 
    #// @param WP_User|WP_Error $user     WP_User or WP_Error object if a previous
    #// callback failed authentication.
    #// @param string           $password Password to check against the user.
    #//
    user_ = apply_filters("wp_authenticate_user", user_, password_)
    if is_wp_error(user_):
        return user_
    # end if
    if (not wp_check_password(password_, user_.user_pass, user_.ID)):
        return php_new_class("WP_Error", lambda : WP_Error("incorrect_password", php_sprintf(__("<strong>Error</strong>: The password you entered for the username %s is incorrect."), "<strong>" + username_ + "</strong>") + " <a href=\"" + wp_lostpassword_url() + "\">" + __("Lost your password?") + "</a>"))
    # end if
    return user_
# end def wp_authenticate_username_password
#// 
#// Authenticates a user using the email and password.
#// 
#// @since 4.5.0
#// 
#// @param WP_User|WP_Error|null $user     WP_User or WP_Error object if a previous
#// callback failed authentication.
#// @param string                $email    Email address for authentication.
#// @param string                $password Password for authentication.
#// @return WP_User|WP_Error WP_User on success, WP_Error on failure.
#//
def wp_authenticate_email_password(user_=None, email_=None, password_=None, *_args_):
    
    
    if type(user_).__name__ == "WP_User":
        return user_
    # end if
    if php_empty(lambda : email_) or php_empty(lambda : password_):
        if is_wp_error(user_):
            return user_
        # end if
        error_ = php_new_class("WP_Error", lambda : WP_Error())
        if php_empty(lambda : email_):
            #// Uses 'empty_username' for back-compat with wp_signon().
            error_.add("empty_username", __("<strong>Error</strong>: The email field is empty."))
        # end if
        if php_empty(lambda : password_):
            error_.add("empty_password", __("<strong>Error</strong>: The password field is empty."))
        # end if
        return error_
    # end if
    if (not is_email(email_)):
        return user_
    # end if
    user_ = get_user_by("email", email_)
    if (not user_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_email", __("Unknown email address. Check again or try your username.")))
    # end if
    #// This filter is documented in wp-includes/user.php
    user_ = apply_filters("wp_authenticate_user", user_, password_)
    if is_wp_error(user_):
        return user_
    # end if
    if (not wp_check_password(password_, user_.user_pass, user_.ID)):
        return php_new_class("WP_Error", lambda : WP_Error("incorrect_password", php_sprintf(__("<strong>Error</strong>: The password you entered for the email address %s is incorrect."), "<strong>" + email_ + "</strong>") + " <a href=\"" + wp_lostpassword_url() + "\">" + __("Lost your password?") + "</a>"))
    # end if
    return user_
# end def wp_authenticate_email_password
#// 
#// Authenticate the user using the WordPress auth cookie.
#// 
#// @since 2.8.0
#// 
#// @global string $auth_secure_cookie
#// 
#// @param WP_User|WP_Error|null $user     WP_User or WP_Error object from a previous callback. Default null.
#// @param string                $username Username. If not empty, cancels the cookie authentication.
#// @param string                $password Password. If not empty, cancels the cookie authentication.
#// @return WP_User|WP_Error WP_User on success, WP_Error on failure.
#//
def wp_authenticate_cookie(user_=None, username_=None, password_=None, *_args_):
    
    
    if type(user_).__name__ == "WP_User":
        return user_
    # end if
    if php_empty(lambda : username_) and php_empty(lambda : password_):
        user_id_ = wp_validate_auth_cookie()
        if user_id_:
            return php_new_class("WP_User", lambda : WP_User(user_id_))
        # end if
        global auth_secure_cookie_
        php_check_if_defined("auth_secure_cookie_")
        if auth_secure_cookie_:
            auth_cookie_ = SECURE_AUTH_COOKIE
        else:
            auth_cookie_ = AUTH_COOKIE
        # end if
        if (not php_empty(lambda : PHP_COOKIE[auth_cookie_])):
            return php_new_class("WP_Error", lambda : WP_Error("expired_session", __("Please log in again.")))
        # end if
        pass
    # end if
    return user_
# end def wp_authenticate_cookie
#// 
#// For Multisite blogs, check if the authenticated user has been marked as a
#// spammer, or if the user's primary blog has been marked as spam.
#// 
#// @since 3.7.0
#// 
#// @param WP_User|WP_Error|null $user WP_User or WP_Error object from a previous callback. Default null.
#// @return WP_User|WP_Error WP_User on success, WP_Error if the user is considered a spammer.
#//
def wp_authenticate_spam_check(user_=None, *_args_):
    
    
    if type(user_).__name__ == "WP_User" and is_multisite():
        #// 
        #// Filters whether the user has been marked as a spammer.
        #// 
        #// @since 3.7.0
        #// 
        #// @param bool    $spammed Whether the user is considered a spammer.
        #// @param WP_User $user    User to check against.
        #//
        spammed_ = apply_filters("check_is_user_spammed", is_user_spammy(user_), user_)
        if spammed_:
            return php_new_class("WP_Error", lambda : WP_Error("spammer_account", __("<strong>Error</strong>: Your account has been marked as a spammer.")))
        # end if
    # end if
    return user_
# end def wp_authenticate_spam_check
#// 
#// Validates the logged-in cookie.
#// 
#// Checks the logged-in cookie if the previous auth cookie could not be
#// validated and parsed.
#// 
#// This is a callback for the {@see 'determine_current_user'} filter, rather than API.
#// 
#// @since 3.9.0
#// 
#// @param int|bool $user_id The user ID (or false) as received from
#// the `determine_current_user` filter.
#// @return int|false User ID if validated, false otherwise. If a user ID from
#// an earlier filter callback is received, that value is returned.
#//
def wp_validate_logged_in_cookie(user_id_=None, *_args_):
    
    
    if user_id_:
        return user_id_
    # end if
    if is_blog_admin() or is_network_admin() or php_empty(lambda : PHP_COOKIE[LOGGED_IN_COOKIE]):
        return False
    # end if
    return wp_validate_auth_cookie(PHP_COOKIE[LOGGED_IN_COOKIE], "logged_in")
# end def wp_validate_logged_in_cookie
#// 
#// Number of posts user has written.
#// 
#// @since 3.0.0
#// @since 4.1.0 Added `$post_type` argument.
#// @since 4.3.0 Added `$public_only` argument. Added the ability to pass an array
#// of post types to `$post_type`.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int          $userid      User ID.
#// @param array|string $post_type   Optional. Single post type or array of post types to count the number of posts for. Default 'post'.
#// @param bool         $public_only Optional. Whether to only return counts for public posts. Default false.
#// @return string Number of posts the user has written in this post type.
#//
def count_user_posts(userid_=None, post_type_="post", public_only_=None, *_args_):
    if public_only_ is None:
        public_only_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    where_ = get_posts_by_author_sql(post_type_, True, userid_, public_only_)
    count_ = wpdb_.get_var(str("SELECT COUNT(*) FROM ") + str(wpdb_.posts) + str(" ") + str(where_))
    #// 
    #// Filters the number of posts a user has written.
    #// 
    #// @since 2.7.0
    #// @since 4.1.0 Added `$post_type` argument.
    #// @since 4.3.1 Added `$public_only` argument.
    #// 
    #// @param int          $count       The user's post count.
    #// @param int          $userid      User ID.
    #// @param string|array $post_type   Single post type or array of post types to count the number of posts for.
    #// @param bool         $public_only Whether to limit counted posts to public posts.
    #//
    return apply_filters("get_usernumposts", count_, userid_, post_type_, public_only_)
# end def count_user_posts
#// 
#// Number of posts written by a list of users.
#// 
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int[]           $users       Array of user IDs.
#// @param string|string[] $post_type   Optional. Single post type or array of post types to check. Defaults to 'post'.
#// @param bool            $public_only Optional. Only return counts for public posts.  Defaults to false.
#// @return string[] Amount of posts each user has written, as strings, keyed by user ID.
#//
def count_many_users_posts(users_=None, post_type_="post", public_only_=None, *_args_):
    if public_only_ is None:
        public_only_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    count_ = Array()
    if php_empty(lambda : users_) or (not php_is_array(users_)):
        return count_
    # end if
    userlist_ = php_implode(",", php_array_map("absint", users_))
    where_ = get_posts_by_author_sql(post_type_, True, None, public_only_)
    result_ = wpdb_.get_results(str("SELECT post_author, COUNT(*) FROM ") + str(wpdb_.posts) + str(" ") + str(where_) + str(" AND post_author IN (") + str(userlist_) + str(") GROUP BY post_author"), ARRAY_N)
    for row_ in result_:
        count_[row_[0]] = row_[1]
    # end for
    for id_ in users_:
        if (not (php_isset(lambda : count_[id_]))):
            count_[id_] = 0
        # end if
    # end for
    return count_
# end def count_many_users_posts
#// 
#// User option functions.
#// 
#// 
#// Get the current user's ID
#// 
#// @since MU (3.0.0)
#// 
#// @return int The current user's ID, or 0 if no user is logged in.
#//
def get_current_user_id(*_args_):
    
    
    if (not php_function_exists("wp_get_current_user")):
        return 0
    # end if
    user_ = wp_get_current_user()
    return php_int(user_.ID) if (php_isset(lambda : user_.ID)) else 0
# end def get_current_user_id
#// 
#// Retrieve user option that can be either per Site or per Network.
#// 
#// If the user ID is not given, then the current user will be used instead. If
#// the user ID is given, then the user data will be retrieved. The filter for
#// the result, will also pass the original option name and finally the user data
#// object as the third parameter.
#// 
#// The option will first check for the per site name and then the per Network name.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $option     User option name.
#// @param int    $user       Optional. User ID.
#// @param string $deprecated Use get_option() to check for an option in the options table.
#// @return mixed User option value on success, false on failure.
#//
def get_user_option(option_=None, user_=0, deprecated_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(__FUNCTION__, "3.0.0")
    # end if
    if php_empty(lambda : user_):
        user_ = get_current_user_id()
    # end if
    user_ = get_userdata(user_)
    if (not user_):
        return False
    # end if
    prefix_ = wpdb_.get_blog_prefix()
    if user_.has_prop(prefix_ + option_):
        #// Blog-specific.
        result_ = user_.get(prefix_ + option_)
    elif user_.has_prop(option_):
        #// User-specific and cross-blog.
        result_ = user_.get(option_)
    else:
        result_ = False
    # end if
    #// 
    #// Filters a specific user option value.
    #// 
    #// The dynamic portion of the hook name, `$option`, refers to the user option name.
    #// 
    #// @since 2.5.0
    #// 
    #// @param mixed   $result Value for the user's option.
    #// @param string  $option Name of the option being retrieved.
    #// @param WP_User $user   WP_User object of the user whose option is being retrieved.
    #//
    return apply_filters(str("get_user_option_") + str(option_), result_, option_, user_)
# end def get_user_option
#// 
#// Update user option with global blog capability.
#// 
#// User options are just like user metadata except that they have support for
#// global blog options. If the 'global' parameter is false, which it is by default
#// it will prepend the WordPress table prefix to the option name.
#// 
#// Deletes the user option if $newvalue is empty.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $user_id     User ID.
#// @param string $option_name User option name.
#// @param mixed  $newvalue    User option value.
#// @param bool   $global      Optional. Whether option name is global or blog specific.
#// Default false (blog specific).
#// @return int|bool User meta ID if the option didn't exist, true on successful update,
#// false on failure.
#//
def update_user_option(user_id_=None, option_name_=None, newvalue_=None, global_=None, *_args_):
    if global_ is None:
        global_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not global_):
        option_name_ = wpdb_.get_blog_prefix() + option_name_
    # end if
    return update_user_meta(user_id_, option_name_, newvalue_)
# end def update_user_option
#// 
#// Delete user option with global blog capability.
#// 
#// User options are just like user metadata except that they have support for
#// global blog options. If the 'global' parameter is false, which it is by default
#// it will prepend the WordPress table prefix to the option name.
#// 
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $user_id     User ID
#// @param string $option_name User option name.
#// @param bool   $global      Optional. Whether option name is global or blog specific.
#// Default false (blog specific).
#// @return bool True on success, false on failure.
#//
def delete_user_option(user_id_=None, option_name_=None, global_=None, *_args_):
    if global_ is None:
        global_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not global_):
        option_name_ = wpdb_.get_blog_prefix() + option_name_
    # end if
    return delete_user_meta(user_id_, option_name_)
# end def delete_user_option
#// 
#// Retrieve list of users matching criteria.
#// 
#// @since 3.1.0
#// 
#// @see WP_User_Query
#// 
#// @param array $args Optional. Arguments to retrieve users. See WP_User_Query::prepare_query().
#// for more information on accepted arguments.
#// @return array List of users.
#//
def get_users(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    args_ = wp_parse_args(args_)
    args_["count_total"] = False
    user_search_ = php_new_class("WP_User_Query", lambda : WP_User_Query(args_))
    return user_search_.get_results()
# end def get_users
#// 
#// Get the sites a user belongs to.
#// 
#// @since 3.0.0
#// @since 4.7.0 Converted to use `get_sites()`.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int  $user_id User ID
#// @param bool $all     Whether to retrieve all sites, or only sites that are not
#// marked as deleted, archived, or spam.
#// @return array A list of the user's sites. An empty array if the user doesn't exist
#// or belongs to no sites.
#//
def get_blogs_of_user(user_id_=None, all_=None, *_args_):
    if all_ is None:
        all_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    user_id_ = php_int(user_id_)
    #// Logged out users can't have sites.
    if php_empty(lambda : user_id_):
        return Array()
    # end if
    #// 
    #// Filters the list of a user's sites before it is populated.
    #// 
    #// Passing a non-null value to the filter will effectively short circuit
    #// get_blogs_of_user(), returning that value instead.
    #// 
    #// @since 4.6.0
    #// 
    #// @param null|array $sites   An array of site objects of which the user is a member.
    #// @param int        $user_id User ID.
    #// @param bool       $all     Whether the returned array should contain all sites, including
    #// those marked 'deleted', 'archived', or 'spam'. Default false.
    #//
    sites_ = apply_filters("pre_get_blogs_of_user", None, user_id_, all_)
    if None != sites_:
        return sites_
    # end if
    keys_ = get_user_meta(user_id_)
    if php_empty(lambda : keys_):
        return Array()
    # end if
    if (not is_multisite()):
        site_id_ = get_current_blog_id()
        sites_ = Array({site_id_: php_new_class("stdClass", lambda : stdClass())})
        sites_[site_id_].userblog_id = site_id_
        sites_[site_id_].blogname = get_option("blogname")
        sites_[site_id_].domain = ""
        sites_[site_id_].path = ""
        sites_[site_id_].site_id = 1
        sites_[site_id_].siteurl = get_option("siteurl")
        sites_[site_id_].archived = 0
        sites_[site_id_].spam = 0
        sites_[site_id_].deleted = 0
        return sites_
    # end if
    site_ids_ = Array()
    if (php_isset(lambda : keys_[wpdb_.base_prefix + "capabilities"])) and php_defined("MULTISITE"):
        site_ids_[-1] = 1
        keys_[wpdb_.base_prefix + "capabilities"] = None
    # end if
    keys_ = php_array_keys(keys_)
    for key_ in keys_:
        if "capabilities" != php_substr(key_, -12):
            continue
        # end if
        if wpdb_.base_prefix and 0 != php_strpos(key_, wpdb_.base_prefix):
            continue
        # end if
        site_id_ = php_str_replace(Array(wpdb_.base_prefix, "_capabilities"), "", key_)
        if (not php_is_numeric(site_id_)):
            continue
        # end if
        site_ids_[-1] = php_int(site_id_)
    # end for
    sites_ = Array()
    if (not php_empty(lambda : site_ids_)):
        args_ = Array({"number": "", "site__in": site_ids_, "update_site_meta_cache": False})
        if (not all_):
            args_["archived"] = 0
            args_["spam"] = 0
            args_["deleted"] = 0
        # end if
        _sites_ = get_sites(args_)
        for site_ in _sites_:
            sites_[site_.id] = Array({"userblog_id": site_.id, "blogname": site_.blogname, "domain": site_.domain, "path": site_.path, "site_id": site_.network_id, "siteurl": site_.siteurl, "archived": site_.archived, "mature": site_.mature, "spam": site_.spam, "deleted": site_.deleted})
        # end for
    # end if
    #// 
    #// Filters the list of sites a user belongs to.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param array $sites   An array of site objects belonging to the user.
    #// @param int   $user_id User ID.
    #// @param bool  $all     Whether the returned sites array should contain all sites, including
    #// those marked 'deleted', 'archived', or 'spam'. Default false.
    #//
    return apply_filters("get_blogs_of_user", sites_, user_id_, all_)
# end def get_blogs_of_user
#// 
#// Find out whether a user is a member of a given blog.
#// 
#// @since MU (3.0.0)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $user_id Optional. The unique ID of the user. Defaults to the current user.
#// @param int $blog_id Optional. ID of the blog to check. Defaults to the current site.
#// @return bool
#//
def is_user_member_of_blog(user_id_=0, blog_id_=0, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    user_id_ = php_int(user_id_)
    blog_id_ = php_int(blog_id_)
    if php_empty(lambda : user_id_):
        user_id_ = get_current_user_id()
    # end if
    #// Technically not needed, but does save calls to get_site() and get_user_meta()
    #// in the event that the function is called when a user isn't logged in.
    if php_empty(lambda : user_id_):
        return False
    else:
        user_ = get_userdata(user_id_)
        if (not type(user_).__name__ == "WP_User"):
            return False
        # end if
    # end if
    if (not is_multisite()):
        return True
    # end if
    if php_empty(lambda : blog_id_):
        blog_id_ = get_current_blog_id()
    # end if
    blog_ = get_site(blog_id_)
    if (not blog_) or (not (php_isset(lambda : blog_.domain))) or blog_.archived or blog_.spam or blog_.deleted:
        return False
    # end if
    keys_ = get_user_meta(user_id_)
    if php_empty(lambda : keys_):
        return False
    # end if
    #// No underscore before capabilities in $base_capabilities_key.
    base_capabilities_key_ = wpdb_.base_prefix + "capabilities"
    site_capabilities_key_ = wpdb_.base_prefix + blog_id_ + "_capabilities"
    if (php_isset(lambda : keys_[base_capabilities_key_])) and 1 == blog_id_:
        return True
    # end if
    if (php_isset(lambda : keys_[site_capabilities_key_])):
        return True
    # end if
    return False
# end def is_user_member_of_blog
#// 
#// Adds meta data to a user.
#// 
#// @since 3.0.0
#// 
#// @param int    $user_id    User ID.
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Metadata value.
#// @param bool   $unique     Optional. Whether the same key should not be added. Default false.
#// @return int|false Meta ID on success, false on failure.
#//
def add_user_meta(user_id_=None, meta_key_=None, meta_value_=None, unique_=None, *_args_):
    if unique_ is None:
        unique_ = False
    # end if
    
    return add_metadata("user", user_id_, meta_key_, meta_value_, unique_)
# end def add_user_meta
#// 
#// Remove metadata matching criteria from a user.
#// 
#// You can match based on the key, or key and value. Removing based on key and
#// value, will keep from removing duplicate metadata with the same key. It also
#// allows removing all metadata matching key, if needed.
#// 
#// @since 3.0.0
#// @link https://developer.wordpress.org/reference/functions/delete_user_meta
#// 
#// @param int    $user_id    User ID
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Optional. Metadata value.
#// @return bool True on success, false on failure.
#//
def delete_user_meta(user_id_=None, meta_key_=None, meta_value_="", *_args_):
    
    
    return delete_metadata("user", user_id_, meta_key_, meta_value_)
# end def delete_user_meta
#// 
#// Retrieve user meta field for a user.
#// 
#// @since 3.0.0
#// @link https://developer.wordpress.org/reference/functions/get_user_meta
#// 
#// @param int    $user_id User ID.
#// @param string $key     Optional. The meta key to retrieve. By default, returns data for all keys.
#// @param bool   $single  Whether to return a single value.
#// @return mixed Will be an array if $single is false. Will be value of meta data field if $single is true.
#//
def get_user_meta(user_id_=None, key_="", single_=None, *_args_):
    if single_ is None:
        single_ = False
    # end if
    
    return get_metadata("user", user_id_, key_, single_)
# end def get_user_meta
#// 
#// Update user meta field based on user ID.
#// 
#// Use the $prev_value parameter to differentiate between meta fields with the
#// same key and user ID.
#// 
#// If the meta field for the user does not exist, it will be added.
#// 
#// @since 3.0.0
#// @link https://developer.wordpress.org/reference/functions/update_user_meta
#// 
#// @param int    $user_id    User ID.
#// @param string $meta_key   Metadata key.
#// @param mixed  $meta_value Metadata value.
#// @param mixed  $prev_value Optional. Previous value to check before removing.
#// @return int|bool Meta ID if the key didn't exist, true on successful update, false on failure.
#//
def update_user_meta(user_id_=None, meta_key_=None, meta_value_=None, prev_value_="", *_args_):
    
    
    return update_metadata("user", user_id_, meta_key_, meta_value_, prev_value_)
# end def update_user_meta
#// 
#// Count number of users who have each of the user roles.
#// 
#// Assumes there are neither duplicated nor orphaned capabilities meta_values.
#// Assumes role names are unique phrases. Same assumption made by WP_User_Query::prepare_query()
#// Using $strategy = 'time' this is CPU-intensive and should handle around 10^7 users.
#// Using $strategy = 'memory' this is memory-intensive and should handle around 10^5 users, but see WP Bug #12257.
#// 
#// @since 3.0.0
#// @since 4.4.0 The number of users with no role is now included in the `none` element.
#// @since 4.9.0 The `$site_id` parameter was added to support multisite.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string   $strategy Optional. The computational strategy to use when counting the users.
#// Accepts either 'time' or 'memory'. Default 'time'.
#// @param int|null $site_id  Optional. The site ID to count users for. Defaults to the current site.
#// @return array {
#// User counts.
#// 
#// @type int   $total_users Total number of users on the site.
#// @type int[] $avail_roles Array of user counts keyed by user role.
#// }
#//
def count_users(strategy_="time", site_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Initialize.
    if (not site_id_):
        site_id_ = get_current_blog_id()
    # end if
    #// 
    #// Filter the user count before queries are run. Return a non-null value to cause count_users()
    #// to return early.
    #// 
    #// @since 5.1.0
    #// 
    #// @param null|string $result   The value to return instead. Default null to continue with the query.
    #// @param string      $strategy Optional. The computational strategy to use when counting the users.
    #// Accepts either 'time' or 'memory'. Default 'time'.
    #// @param int|null    $site_id  Optional. The site ID to count users for. Defaults to the current site.
    #//
    pre_ = apply_filters("pre_count_users", None, strategy_, site_id_)
    if None != pre_:
        return pre_
    # end if
    blog_prefix_ = wpdb_.get_blog_prefix(site_id_)
    result_ = Array()
    if "time" == strategy_:
        if is_multisite() and get_current_blog_id() != site_id_:
            switch_to_blog(site_id_)
            avail_roles_ = wp_roles().get_names()
            restore_current_blog()
        else:
            avail_roles_ = wp_roles().get_names()
        # end if
        #// Build a CPU-intensive query that will return concise information.
        select_count_ = Array()
        for this_role_,name_ in avail_roles_:
            select_count_[-1] = wpdb_.prepare("COUNT(NULLIF(`meta_value` LIKE %s, false))", "%" + wpdb_.esc_like("\"" + this_role_ + "\"") + "%")
        # end for
        select_count_[-1] = "COUNT(NULLIF(`meta_value` = 'a:0:{}', false))"
        select_count_ = php_implode(", ", select_count_)
        #// Add the meta_value index to the selection list, then run the query.
        row_ = wpdb_.get_row(str("\n            SELECT ") + str(select_count_) + str(", COUNT(*)\n          FROM ") + str(wpdb_.usermeta) + str("\n         INNER JOIN ") + str(wpdb_.users) + str(" ON user_id = ID\n          WHERE meta_key = '") + str(blog_prefix_) + str("capabilities'\n     "), ARRAY_N)
        #// Run the previous loop again to associate results with role names.
        col_ = 0
        role_counts_ = Array()
        for this_role_,name_ in avail_roles_:
            count_ = php_int(row_[col_])
            col_ += 1
            col_ += 1
            if count_ > 0:
                role_counts_[this_role_] = count_
            # end if
        # end for
        role_counts_["none"] = php_int(row_[col_])
        col_ += 1
        col_ += 1
        #// Get the meta_value index from the end of the result set.
        total_users_ = php_int(row_[col_])
        result_["total_users"] = total_users_
        result_["avail_roles"] = role_counts_
    else:
        avail_roles_ = Array({"none": 0})
        users_of_blog_ = wpdb_.get_col(str("\n          SELECT meta_value\n         FROM ") + str(wpdb_.usermeta) + str("\n         INNER JOIN ") + str(wpdb_.users) + str(" ON user_id = ID\n          WHERE meta_key = '") + str(blog_prefix_) + str("capabilities'\n     "))
        for caps_meta_ in users_of_blog_:
            b_roles_ = maybe_unserialize(caps_meta_)
            if (not php_is_array(b_roles_)):
                continue
            # end if
            if php_empty(lambda : b_roles_):
                avail_roles_["none"] += 1
            # end if
            for b_role_,val_ in b_roles_:
                if (php_isset(lambda : avail_roles_[b_role_])):
                    avail_roles_[b_role_] += 1
                else:
                    avail_roles_[b_role_] = 1
                # end if
            # end for
        # end for
        result_["total_users"] = php_count(users_of_blog_)
        result_["avail_roles"] = avail_roles_
    # end if
    return result_
# end def count_users
#// 
#// Private helper functions.
#// 
#// 
#// Set up global user vars.
#// 
#// Used by wp_set_current_user() for back compat. Might be deprecated in the future.
#// 
#// @since 2.0.4
#// 
#// @global string  $user_login    The user username for logging in
#// @global WP_User $userdata      User data.
#// @global int     $user_level    The level of the user
#// @global int     $user_ID       The ID of the user
#// @global string  $user_email    The email address of the user
#// @global string  $user_url      The url in the user's profile
#// @global string  $user_identity The display name of the user
#// 
#// @param int $for_user_id Optional. User ID to set up global data. Default 0.
#//
def setup_userdata(for_user_id_=0, *_args_):
    
    
    global user_login_
    global userdata_
    global user_level_
    global user_ID_
    global user_email_
    global user_url_
    global user_identity_
    php_check_if_defined("user_login_","userdata_","user_level_","user_ID_","user_email_","user_url_","user_identity_")
    if (not for_user_id_):
        for_user_id_ = get_current_user_id()
    # end if
    user_ = get_userdata(for_user_id_)
    if (not user_):
        user_ID_ = 0
        user_level_ = 0
        userdata_ = None
        user_login_ = ""
        user_email_ = ""
        user_url_ = ""
        user_identity_ = ""
        return
    # end if
    user_ID_ = php_int(user_.ID)
    user_level_ = php_int(user_.user_level)
    userdata_ = user_
    user_login_ = user_.user_login
    user_email_ = user_.user_email
    user_url_ = user_.user_url
    user_identity_ = user_.display_name
# end def setup_userdata
#// 
#// Create dropdown HTML content of users.
#// 
#// The content can either be displayed, which it is by default or retrieved by
#// setting the 'echo' argument. The 'include' and 'exclude' arguments do not
#// need to be used; all users will be displayed in that case. Only one can be
#// used, either 'include' or 'exclude', but not both.
#// 
#// The available arguments are as follows:
#// 
#// @since 2.3.0
#// @since 4.5.0 Added the 'display_name_with_login' value for 'show'.
#// @since 4.7.0 Added the `$role`, `$role__in`, and `$role__not_in` parameters.
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments to generate a drop-down of users.
#// See WP_User_Query::prepare_query() for additional available arguments.
#// 
#// @type string       $show_option_all         Text to show as the drop-down default (all).
#// Default empty.
#// @type string       $show_option_none        Text to show as the drop-down default when no
#// users were found. Default empty.
#// @type int|string   $option_none_value       Value to use for $show_option_non when no users
#// were found. Default -1.
#// @type string       $hide_if_only_one_author Whether to skip generating the drop-down
#// if only one user was found. Default empty.
#// @type string       $orderby                 Field to order found users by. Accepts user fields.
#// Default 'display_name'.
#// @type string       $order                   Whether to order users in ascending or descending
#// order. Accepts 'ASC' (ascending) or 'DESC' (descending).
#// Default 'ASC'.
#// @type array|string $include                 Array or comma-separated list of user IDs to include.
#// Default empty.
#// @type array|string $exclude                 Array or comma-separated list of user IDs to exclude.
#// Default empty.
#// @type bool|int     $multi                   Whether to skip the ID attribute on the 'select' element.
#// Accepts 1|true or 0|false. Default 0|false.
#// @type string       $show                    User data to display. If the selected item is empty
#// then the 'user_login' will be displayed in parentheses.
#// Accepts any user field, or 'display_name_with_login' to show
#// the display name with user_login in parentheses.
#// Default 'display_name'.
#// @type int|bool     $echo                    Whether to echo or return the drop-down. Accepts 1|true (echo)
#// or 0|false (return). Default 1|true.
#// @type int          $selected                Which user ID should be selected. Default 0.
#// @type bool         $include_selected        Whether to always include the selected user ID in the drop-
#// down. Default false.
#// @type string       $name                    Name attribute of select element. Default 'user'.
#// @type string       $id                      ID attribute of the select element. Default is the value of $name.
#// @type string       $class                   Class attribute of the select element. Default empty.
#// @type int          $blog_id                 ID of blog (Multisite only). Default is ID of the current blog.
#// @type string       $who                     Which type of users to query. Accepts only an empty string or
#// 'authors'. Default empty.
#// @type string|array $role                    An array or a comma-separated list of role names that users must
#// match to be included in results. Note that this is an inclusive
#// list: users must match *each* role. Default empty.
#// @type array        $role__in                An array of role names. Matched users must have at least one of
#// these roles. Default empty array.
#// @type array        $role__not_in            An array of role names to exclude. Users matching one or more of
#// these roles will not be included in results. Default empty array.
#// }
#// @return string HTML dropdown list of users.
#//
def wp_dropdown_users(args_="", *_args_):
    
    
    defaults_ = Array({"show_option_all": "", "show_option_none": "", "hide_if_only_one_author": "", "orderby": "display_name", "order": "ASC", "include": "", "exclude": "", "multi": 0, "show": "display_name", "echo": 1, "selected": 0, "name": "user", "class": "", "id": "", "blog_id": get_current_blog_id(), "who": "", "include_selected": False, "option_none_value": -1, "role": "", "role__in": Array(), "role__not_in": Array()})
    defaults_["selected"] = get_query_var("author") if is_author() else 0
    parsed_args_ = wp_parse_args(args_, defaults_)
    query_args_ = wp_array_slice_assoc(parsed_args_, Array("blog_id", "include", "exclude", "orderby", "order", "who", "role", "role__in", "role__not_in"))
    fields_ = Array("ID", "user_login")
    show_ = parsed_args_["show"] if (not php_empty(lambda : parsed_args_["show"])) else "display_name"
    if "display_name_with_login" == show_:
        fields_[-1] = "display_name"
    else:
        fields_[-1] = show_
    # end if
    query_args_["fields"] = fields_
    show_option_all_ = parsed_args_["show_option_all"]
    show_option_none_ = parsed_args_["show_option_none"]
    option_none_value_ = parsed_args_["option_none_value"]
    #// 
    #// Filters the query arguments for the list of users in the dropdown.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $query_args  The query arguments for get_users().
    #// @param array $parsed_args The arguments passed to wp_dropdown_users() combined with the defaults.
    #//
    query_args_ = apply_filters("wp_dropdown_users_args", query_args_, parsed_args_)
    users_ = get_users(query_args_)
    output_ = ""
    if (not php_empty(lambda : users_)) and php_empty(lambda : parsed_args_["hide_if_only_one_author"]) or php_count(users_) > 1:
        name_ = esc_attr(parsed_args_["name"])
        if parsed_args_["multi"] and (not parsed_args_["id"]):
            id_ = ""
        else:
            id_ = " id='" + esc_attr(parsed_args_["id"]) + "'" if parsed_args_["id"] else str(" id='") + str(name_) + str("'")
        # end if
        output_ = str("<select name='") + str(name_) + str("'") + str(id_) + str(" class='") + parsed_args_["class"] + "'>\n"
        if show_option_all_:
            output_ += str("    <option value='0'>") + str(show_option_all_) + str("</option>\n")
        # end if
        if show_option_none_:
            _selected_ = selected(option_none_value_, parsed_args_["selected"], False)
            output_ += "    <option value='" + esc_attr(option_none_value_) + str("'") + str(_selected_) + str(">") + str(show_option_none_) + str("</option>\n")
        # end if
        if parsed_args_["include_selected"] and parsed_args_["selected"] > 0:
            found_selected_ = False
            parsed_args_["selected"] = php_int(parsed_args_["selected"])
            for user_ in users_:
                user_.ID = php_int(user_.ID)
                if user_.ID == parsed_args_["selected"]:
                    found_selected_ = True
                # end if
            # end for
            if (not found_selected_):
                users_[-1] = get_userdata(parsed_args_["selected"])
            # end if
        # end if
        for user_ in users_:
            if "display_name_with_login" == show_:
                #// translators: 1: User's display name, 2: User login.
                display_ = php_sprintf(_x("%1$s (%2$s)", "user dropdown"), user_.display_name, user_.user_login)
            elif (not php_empty(lambda : user_.show_)):
                display_ = user_.show_
            else:
                display_ = "(" + user_.user_login + ")"
            # end if
            _selected_ = selected(user_.ID, parsed_args_["selected"], False)
            output_ += str("    <option value='") + str(user_.ID) + str("'") + str(_selected_) + str(">") + esc_html(display_) + "</option>\n"
        # end for
        output_ += "</select>"
    # end if
    #// 
    #// Filters the wp_dropdown_users() HTML output.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $output HTML output generated by wp_dropdown_users().
    #//
    html_ = apply_filters("wp_dropdown_users", output_)
    if parsed_args_["echo"]:
        php_print(html_)
    # end if
    return html_
# end def wp_dropdown_users
#// 
#// Sanitize user field based on context.
#// 
#// Possible context values are:  'raw', 'edit', 'db', 'display', 'attribute' and 'js'. The
#// 'display' context is used by default. 'attribute' and 'js' contexts are treated like 'display'
#// when calling filters.
#// 
#// @since 2.3.0
#// 
#// @param string $field   The user Object field name.
#// @param mixed  $value   The user Object value.
#// @param int    $user_id User ID.
#// @param string $context How to sanitize user fields. Looks for 'raw', 'edit', 'db', 'display',
#// 'attribute' and 'js'.
#// @return mixed Sanitized value.
#//
def sanitize_user_field(field_=None, value_=None, user_id_=None, context_=None, *_args_):
    
    
    int_fields_ = Array("ID")
    if php_in_array(field_, int_fields_):
        value_ = php_int(value_)
    # end if
    if "raw" == context_:
        return value_
    # end if
    if (not php_is_string(value_)) and (not php_is_numeric(value_)):
        return value_
    # end if
    prefixed_ = False != php_strpos(field_, "user_")
    if "edit" == context_:
        if prefixed_:
            #// This filter is documented in wp-includes/post.php
            value_ = apply_filters(str("edit_") + str(field_), value_, user_id_)
        else:
            #// 
            #// Filters a user field value in the 'edit' context.
            #// 
            #// The dynamic portion of the hook name, `$field`, refers to the prefixed user
            #// field being filtered, such as 'user_login', 'user_email', 'first_name', etc.
            #// 
            #// @since 2.9.0
            #// 
            #// @param mixed $value   Value of the prefixed user field.
            #// @param int   $user_id User ID.
            #//
            value_ = apply_filters(str("edit_user_") + str(field_), value_, user_id_)
        # end if
        if "description" == field_:
            value_ = esc_html(value_)
            pass
        else:
            value_ = esc_attr(value_)
        # end if
    elif "db" == context_:
        if prefixed_:
            #// This filter is documented in wp-includes/post.php
            value_ = apply_filters(str("pre_") + str(field_), value_)
        else:
            #// 
            #// Filters the value of a user field in the 'db' context.
            #// 
            #// The dynamic portion of the hook name, `$field`, refers to the prefixed user
            #// field being filtered, such as 'user_login', 'user_email', 'first_name', etc.
            #// 
            #// @since 2.9.0
            #// 
            #// @param mixed $value Value of the prefixed user field.
            #//
            value_ = apply_filters(str("pre_user_") + str(field_), value_)
        # end if
    else:
        #// Use display filters by default.
        if prefixed_:
            #// This filter is documented in wp-includes/post.php
            value_ = apply_filters(str(field_), value_, user_id_, context_)
        else:
            #// 
            #// Filters the value of a user field in a standard context.
            #// 
            #// The dynamic portion of the hook name, `$field`, refers to the prefixed user
            #// field being filtered, such as 'user_login', 'user_email', 'first_name', etc.
            #// 
            #// @since 2.9.0
            #// 
            #// @param mixed  $value   The user object value to sanitize.
            #// @param int    $user_id User ID.
            #// @param string $context The context to filter within.
            #//
            value_ = apply_filters(str("user_") + str(field_), value_, user_id_, context_)
        # end if
    # end if
    if "user_url" == field_:
        value_ = esc_url(value_)
    # end if
    if "attribute" == context_:
        value_ = esc_attr(value_)
    elif "js" == context_:
        value_ = esc_js(value_)
    # end if
    return value_
# end def sanitize_user_field
#// 
#// Update all user caches
#// 
#// @since 3.0.0
#// 
#// @param WP_User $user User object to be cached
#// @return bool|null Returns false on failure.
#//
def update_user_caches(user_=None, *_args_):
    
    
    if type(user_).__name__ == "WP_User":
        if (not user_.exists()):
            return False
        # end if
        user_ = user_.data
    # end if
    wp_cache_add(user_.ID, user_, "users")
    wp_cache_add(user_.user_login, user_.ID, "userlogins")
    wp_cache_add(user_.user_email, user_.ID, "useremail")
    wp_cache_add(user_.user_nicename, user_.ID, "userslugs")
# end def update_user_caches
#// 
#// Clean all user caches
#// 
#// @since 3.0.0
#// @since 4.4.0 'clean_user_cache' action was added.
#// 
#// @param WP_User|int $user User object or ID to be cleaned from the cache
#//
def clean_user_cache(user_=None, *_args_):
    
    
    if php_is_numeric(user_):
        user_ = php_new_class("WP_User", lambda : WP_User(user_))
    # end if
    if (not user_.exists()):
        return
    # end if
    wp_cache_delete(user_.ID, "users")
    wp_cache_delete(user_.user_login, "userlogins")
    wp_cache_delete(user_.user_email, "useremail")
    wp_cache_delete(user_.user_nicename, "userslugs")
    #// 
    #// Fires immediately after the given user's cache is cleaned.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int     $user_id User ID.
    #// @param WP_User $user    User object.
    #//
    do_action("clean_user_cache", user_.ID, user_)
# end def clean_user_cache
#// 
#// Determines whether the given username exists.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.0.0
#// 
#// @param string $username Username.
#// @return int|false The user's ID on success, and false on failure.
#//
def username_exists(username_=None, *_args_):
    
    
    user_ = get_user_by("login", username_)
    if user_:
        user_id_ = user_.ID
    else:
        user_id_ = False
    # end if
    #// 
    #// Filters whether the given username exists or not.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int|false $user_id  The user's ID on success, and false on failure.
    #// @param string    $username Username to check.
    #//
    return apply_filters("username_exists", user_id_, username_)
# end def username_exists
#// 
#// Determines whether the given email exists.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.1.0
#// 
#// @param string $email Email.
#// @return int|false The user's ID on success, and false on failure.
#//
def email_exists(email_=None, *_args_):
    
    
    user_ = get_user_by("email", email_)
    if user_:
        return user_.ID
    # end if
    return False
# end def email_exists
#// 
#// Checks whether a username is valid.
#// 
#// @since 2.0.1
#// @since 4.4.0 Empty sanitized usernames are now considered invalid
#// 
#// @param string $username Username.
#// @return bool Whether username given is valid
#//
def validate_username(username_=None, *_args_):
    
    
    sanitized_ = sanitize_user(username_, True)
    valid_ = sanitized_ == username_ and (not php_empty(lambda : sanitized_))
    #// 
    #// Filters whether the provided username is valid or not.
    #// 
    #// @since 2.0.1
    #// 
    #// @param bool   $valid    Whether given username is valid.
    #// @param string $username Username to check.
    #//
    return apply_filters("validate_username", valid_, username_)
# end def validate_username
#// 
#// Insert a user into the database.
#// 
#// Most of the `$userdata` array fields have filters associated with the values. Exceptions are
#// 'ID', 'rich_editing', 'syntax_highlighting', 'comment_shortcuts', 'admin_color', 'use_ssl',
#// 'user_registered', 'user_activation_key', 'spam', and 'role'. The filters have the prefix
#// 'pre_user_' followed by the field name. An example using 'description' would have the filter
#// called 'pre_user_description' that can be hooked into.
#// 
#// @since 2.0.0
#// @since 3.6.0 The `aim`, `jabber`, and `yim` fields were removed as default user contact
#// methods for new installations. See wp_get_user_contact_methods().
#// @since 4.7.0 The user's locale can be passed to `$userdata`.
#// @since 5.3.0 The `user_activation_key` field can be passed to `$userdata`.
#// @since 5.3.0 The `spam` field can be passed to `$userdata` (Multisite only).
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array|object|WP_User $userdata {
#// An array, object, or WP_User object of user data arguments.
#// 
#// @type int    $ID                   User ID. If supplied, the user will be updated.
#// @type string $user_pass            The plain-text user password.
#// @type string $user_login           The user's login username.
#// @type string $user_nicename        The URL-friendly user name.
#// @type string $user_url             The user URL.
#// @type string $user_email           The user email address.
#// @type string $display_name         The user's display name.
#// Default is the user's username.
#// @type string $nickname             The user's nickname.
#// Default is the user's username.
#// @type string $first_name           The user's first name. For new users, will be used
#// to build the first part of the user's display name
#// if `$display_name` is not specified.
#// @type string $last_name            The user's last name. For new users, will be used
#// to build the second part of the user's display name
#// if `$display_name` is not specified.
#// @type string $description          The user's biographical description.
#// @type string $rich_editing         Whether to enable the rich-editor for the user.
#// Accepts 'true' or 'false' as a string literal,
#// not boolean. Default 'true'.
#// @type string $syntax_highlighting  Whether to enable the rich code editor for the user.
#// Accepts 'true' or 'false' as a string literal,
#// not boolean. Default 'true'.
#// @type string $comment_shortcuts    Whether to enable comment moderation keyboard
#// shortcuts for the user. Accepts 'true' or 'false'
#// as a string literal, not boolean. Default 'false'.
#// @type string $admin_color          Admin color scheme for the user. Default 'fresh'.
#// @type bool   $use_ssl              Whether the user should always access the admin over
#// https. Default false.
#// @type string $user_registered      Date the user registered. Format is 'Y-m-d H:i:s'.
#// @type string $user_activation_key  Password reset key. Default empty.
#// @type bool   $spam                 Multisite only. Whether the user is marked as spam.
#// Default false.
#// @type string $show_admin_bar_front Whether to display the Admin Bar for the user
#// on the site's front end. Accepts 'true' or 'false'
#// as a string literal, not boolean. Default 'true'.
#// @type string $role                 User's role.
#// @type string $locale               User's locale. Default empty.
#// }
#// @return int|WP_Error The newly created user's ID or a WP_Error object if the user could not
#// be created.
#//
def wp_insert_user(userdata_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if type(userdata_).__name__ == "stdClass":
        userdata_ = get_object_vars(userdata_)
    elif type(userdata_).__name__ == "WP_User":
        userdata_ = userdata_.to_array()
    # end if
    #// Are we updating or creating?
    if (not php_empty(lambda : userdata_["ID"])):
        ID_ = php_int(userdata_["ID"])
        update_ = True
        old_user_data_ = get_userdata(ID_)
        if (not old_user_data_):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_user_id", __("Invalid user ID.")))
        # end if
        #// hashed in wp_update_user(), plaintext if called directly.
        user_pass_ = userdata_["user_pass"] if (not php_empty(lambda : userdata_["user_pass"])) else old_user_data_.user_pass
    else:
        update_ = False
        #// Hash the password.
        user_pass_ = wp_hash_password(userdata_["user_pass"])
    # end if
    sanitized_user_login_ = sanitize_user(userdata_["user_login"], True)
    #// 
    #// Filters a username after it has been sanitized.
    #// 
    #// This filter is called before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $sanitized_user_login Username after it has been sanitized.
    #//
    pre_user_login_ = apply_filters("pre_user_login", sanitized_user_login_)
    #// Remove any non-printable chars from the login string to see if we have ended up with an empty username.
    user_login_ = php_trim(pre_user_login_)
    #// user_login must be between 0 and 60 characters.
    if php_empty(lambda : user_login_):
        return php_new_class("WP_Error", lambda : WP_Error("empty_user_login", __("Cannot create a user with an empty login name.")))
    elif php_mb_strlen(user_login_) > 60:
        return php_new_class("WP_Error", lambda : WP_Error("user_login_too_long", __("Username may not be longer than 60 characters.")))
    # end if
    if (not update_) and username_exists(user_login_):
        return php_new_class("WP_Error", lambda : WP_Error("existing_user_login", __("Sorry, that username already exists!")))
    # end if
    #// 
    #// Filters the list of blacklisted usernames.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $usernames Array of blacklisted usernames.
    #//
    illegal_logins_ = apply_filters("illegal_user_logins", Array())
    if php_in_array(php_strtolower(user_login_), php_array_map("strtolower", illegal_logins_), True):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_username", __("Sorry, that username is not allowed.")))
    # end if
    #// 
    #// If a nicename is provided, remove unsafe user characters before using it.
    #// Otherwise build a nicename from the user_login.
    #//
    if (not php_empty(lambda : userdata_["user_nicename"])):
        user_nicename_ = sanitize_user(userdata_["user_nicename"], True)
        if php_mb_strlen(user_nicename_) > 50:
            return php_new_class("WP_Error", lambda : WP_Error("user_nicename_too_long", __("Nicename may not be longer than 50 characters.")))
        # end if
    else:
        user_nicename_ = php_mb_substr(user_login_, 0, 50)
    # end if
    user_nicename_ = sanitize_title(user_nicename_)
    #// 
    #// Filters a user's nicename before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $user_nicename The user's nicename.
    #//
    user_nicename_ = apply_filters("pre_user_nicename", user_nicename_)
    user_nicename_check_ = wpdb_.get_var(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.users) + str(" WHERE user_nicename = %s AND user_login != %s LIMIT 1"), user_nicename_, user_login_))
    if user_nicename_check_:
        suffix_ = 2
        while True:
            
            if not (user_nicename_check_):
                break
            # end if
            #// user_nicename allows 50 chars. Subtract one for a hyphen, plus the length of the suffix.
            base_length_ = 49 - php_mb_strlen(suffix_)
            alt_user_nicename_ = php_mb_substr(user_nicename_, 0, base_length_) + str("-") + str(suffix_)
            user_nicename_check_ = wpdb_.get_var(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.users) + str(" WHERE user_nicename = %s AND user_login != %s LIMIT 1"), alt_user_nicename_, user_login_))
            suffix_ += 1
        # end while
        user_nicename_ = alt_user_nicename_
    # end if
    raw_user_email_ = "" if php_empty(lambda : userdata_["user_email"]) else userdata_["user_email"]
    #// 
    #// Filters a user's email before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $raw_user_email The user's email.
    #//
    user_email_ = apply_filters("pre_user_email", raw_user_email_)
    #// 
    #// If there is no update, just check for `email_exists`. If there is an update,
    #// check if current email and new email are the same, or not, and check `email_exists`
    #// accordingly.
    #//
    if (not update_) or (not php_empty(lambda : old_user_data_)) and 0 != strcasecmp(user_email_, old_user_data_.user_email) and (not php_defined("WP_IMPORTING")) and email_exists(user_email_):
        return php_new_class("WP_Error", lambda : WP_Error("existing_user_email", __("Sorry, that email address is already used!")))
    # end if
    raw_user_url_ = "" if php_empty(lambda : userdata_["user_url"]) else userdata_["user_url"]
    #// 
    #// Filters a user's URL before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $raw_user_url The user's URL.
    #//
    user_url_ = apply_filters("pre_user_url", raw_user_url_)
    user_registered_ = gmdate("Y-m-d H:i:s") if php_empty(lambda : userdata_["user_registered"]) else userdata_["user_registered"]
    user_activation_key_ = "" if php_empty(lambda : userdata_["user_activation_key"]) else userdata_["user_activation_key"]
    if (not php_empty(lambda : userdata_["spam"])) and (not is_multisite()):
        return php_new_class("WP_Error", lambda : WP_Error("no_spam", __("Sorry, marking a user as spam is only supported on Multisite.")))
    # end if
    spam_ = 0 if php_empty(lambda : userdata_["spam"]) else php_bool(userdata_["spam"])
    #// Store values to save in user meta.
    meta_ = Array()
    nickname_ = user_login_ if php_empty(lambda : userdata_["nickname"]) else userdata_["nickname"]
    #// 
    #// Filters a user's nickname before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $nickname The user's nickname.
    #//
    meta_["nickname"] = apply_filters("pre_user_nickname", nickname_)
    first_name_ = "" if php_empty(lambda : userdata_["first_name"]) else userdata_["first_name"]
    #// 
    #// Filters a user's first name before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $first_name The user's first name.
    #//
    meta_["first_name"] = apply_filters("pre_user_first_name", first_name_)
    last_name_ = "" if php_empty(lambda : userdata_["last_name"]) else userdata_["last_name"]
    #// 
    #// Filters a user's last name before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $last_name The user's last name.
    #//
    meta_["last_name"] = apply_filters("pre_user_last_name", last_name_)
    if php_empty(lambda : userdata_["display_name"]):
        if update_:
            display_name_ = user_login_
        elif meta_["first_name"] and meta_["last_name"]:
            #// translators: 1: User's first name, 2: Last name.
            display_name_ = php_sprintf(_x("%1$s %2$s", "Display name based on first name and last name"), meta_["first_name"], meta_["last_name"])
        elif meta_["first_name"]:
            display_name_ = meta_["first_name"]
        elif meta_["last_name"]:
            display_name_ = meta_["last_name"]
        else:
            display_name_ = user_login_
        # end if
    else:
        display_name_ = userdata_["display_name"]
    # end if
    #// 
    #// Filters a user's display name before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $display_name The user's display name.
    #//
    display_name_ = apply_filters("pre_user_display_name", display_name_)
    description_ = "" if php_empty(lambda : userdata_["description"]) else userdata_["description"]
    #// 
    #// Filters a user's description before the user is created or updated.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $description The user's description.
    #//
    meta_["description"] = apply_filters("pre_user_description", description_)
    meta_["rich_editing"] = "true" if php_empty(lambda : userdata_["rich_editing"]) else userdata_["rich_editing"]
    meta_["syntax_highlighting"] = "true" if php_empty(lambda : userdata_["syntax_highlighting"]) else userdata_["syntax_highlighting"]
    meta_["comment_shortcuts"] = "false" if php_empty(lambda : userdata_["comment_shortcuts"]) or "false" == userdata_["comment_shortcuts"] else "true"
    admin_color_ = "fresh" if php_empty(lambda : userdata_["admin_color"]) else userdata_["admin_color"]
    meta_["admin_color"] = php_preg_replace("|[^a-z0-9 _.\\-@]|i", "", admin_color_)
    meta_["use_ssl"] = 0 if php_empty(lambda : userdata_["use_ssl"]) else php_bool(userdata_["use_ssl"])
    meta_["show_admin_bar_front"] = "true" if php_empty(lambda : userdata_["show_admin_bar_front"]) else userdata_["show_admin_bar_front"]
    meta_["locale"] = userdata_["locale"] if (php_isset(lambda : userdata_["locale"])) else ""
    compacted_ = php_compact("user_pass", "user_nicename", "user_email", "user_url", "user_registered", "user_activation_key", "display_name")
    data_ = wp_unslash(compacted_)
    if (not update_):
        data_ = data_ + php_compact("user_login")
    # end if
    if is_multisite():
        data_ = data_ + php_compact("spam")
    # end if
    #// 
    #// Filters user data before the record is created or updated.
    #// 
    #// It only includes data in the wp_users table wp_user, not any user metadata.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array    $data {
    #// Values and keys for the user.
    #// 
    #// @type string $user_login      The user's login. Only included if $update == false
    #// @type string $user_pass       The user's password.
    #// @type string $user_email      The user's email.
    #// @type string $user_url        The user's url.
    #// @type string $user_nicename   The user's nice name. Defaults to a URL-safe version of user's login
    #// @type string $display_name    The user's display name.
    #// @type string $user_registered MySQL timestamp describing the moment when the user registered. Defaults to
    #// the current UTC timestamp.
    #// }
    #// @param bool     $update Whether the user is being updated rather than created.
    #// @param int|null $id     ID of the user to be updated, or NULL if the user is being created.
    #//
    data_ = apply_filters("wp_pre_insert_user_data", data_, update_, php_int(ID_) if update_ else None)
    if php_empty(lambda : data_) or (not php_is_array(data_)):
        return php_new_class("WP_Error", lambda : WP_Error("empty_data", __("Not enough data to create this user.")))
    # end if
    if update_:
        if user_email_ != old_user_data_.user_email:
            data_["user_activation_key"] = ""
        # end if
        wpdb_.update(wpdb_.users, data_, php_compact("ID"))
        user_id_ = php_int(ID_)
    else:
        wpdb_.insert(wpdb_.users, data_)
        user_id_ = php_int(wpdb_.insert_id)
    # end if
    user_ = php_new_class("WP_User", lambda : WP_User(user_id_))
    #// 
    #// Filters a user's meta values and keys immediately after the user is created or updated
    #// and before any user meta is inserted or updated.
    #// 
    #// Does not include contact methods. These are added using `wp_get_user_contact_methods( $user )`.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $meta {
    #// Default meta values and keys for the user.
    #// 
    #// @type string   $nickname             The user's nickname. Default is the user's username.
    #// @type string   $first_name           The user's first name.
    #// @type string   $last_name            The user's last name.
    #// @type string   $description          The user's description.
    #// @type string   $rich_editing         Whether to enable the rich-editor for the user. Default 'true'.
    #// @type string   $syntax_highlighting  Whether to enable the rich code editor for the user. Default 'true'.
    #// @type string   $comment_shortcuts    Whether to enable keyboard shortcuts for the user. Default 'false'.
    #// @type string   $admin_color          The color scheme for a user's admin screen. Default 'fresh'.
    #// @type int|bool $use_ssl              Whether to force SSL on the user's admin area. 0|false if SSL
    #// is not forced.
    #// @type string   $show_admin_bar_front Whether to show the admin bar on the front end for the user.
    #// Default 'true'.
    #// @type string   $locale               User's locale. Default empty.
    #// }
    #// @param WP_User $user   User object.
    #// @param bool    $update Whether the user is being updated rather than created.
    #//
    meta_ = apply_filters("insert_user_meta", meta_, user_, update_)
    #// Update user meta.
    for key_,value_ in meta_:
        update_user_meta(user_id_, key_, value_)
    # end for
    for key_,value_ in wp_get_user_contact_methods(user_):
        if (php_isset(lambda : userdata_[key_])):
            update_user_meta(user_id_, key_, userdata_[key_])
        # end if
    # end for
    if (php_isset(lambda : userdata_["role"])):
        user_.set_role(userdata_["role"])
    elif (not update_):
        user_.set_role(get_option("default_role"))
    # end if
    clean_user_cache(user_id_)
    if update_:
        #// 
        #// Fires immediately after an existing user is updated.
        #// 
        #// @since 2.0.0
        #// 
        #// @param int     $user_id       User ID.
        #// @param WP_User $old_user_data Object containing user's data prior to update.
        #//
        do_action("profile_update", user_id_, old_user_data_)
        if (php_isset(lambda : userdata_["spam"])) and userdata_["spam"] != old_user_data_.spam:
            if 1 == userdata_["spam"]:
                #// 
                #// Fires after the user is marked as a SPAM user.
                #// 
                #// @since 3.0.0
                #// 
                #// @param int $user_id ID of the user marked as SPAM.
                #//
                do_action("make_spam_user", user_id_)
            else:
                #// 
                #// Fires after the user is marked as a HAM user. Opposite of SPAM.
                #// 
                #// @since 3.0.0
                #// 
                #// @param int $user_id ID of the user marked as HAM.
                #//
                do_action("make_ham_user", user_id_)
            # end if
        # end if
    else:
        #// 
        #// Fires immediately after a new user is registered.
        #// 
        #// @since 1.5.0
        #// 
        #// @param int $user_id User ID.
        #//
        do_action("user_register", user_id_)
    # end if
    return user_id_
# end def wp_insert_user
#// 
#// Update a user in the database.
#// 
#// It is possible to update a user's password by specifying the 'user_pass'
#// value in the $userdata parameter array.
#// 
#// If current user's password is being updated, then the cookies will be
#// cleared.
#// 
#// @since 2.0.0
#// 
#// @see wp_insert_user() For what fields can be set in $userdata.
#// 
#// @param array|object|WP_User $userdata An array of user data or a user object of type stdClass or WP_User.
#// @return int|WP_Error The updated user's ID or a WP_Error object if the user could not be updated.
#//
def wp_update_user(userdata_=None, *_args_):
    
    
    if type(userdata_).__name__ == "stdClass":
        userdata_ = get_object_vars(userdata_)
    elif type(userdata_).__name__ == "WP_User":
        userdata_ = userdata_.to_array()
    # end if
    ID_ = php_int(userdata_["ID"]) if (php_isset(lambda : userdata_["ID"])) else 0
    if (not ID_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_user_id", __("Invalid user ID.")))
    # end if
    #// First, get all of the original fields.
    user_obj_ = get_userdata(ID_)
    if (not user_obj_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_user_id", __("Invalid user ID.")))
    # end if
    user_ = user_obj_.to_array()
    #// Add additional custom fields.
    for key_ in _get_additional_user_keys(user_obj_):
        user_[key_] = get_user_meta(ID_, key_, True)
    # end for
    #// Escape data pulled from DB.
    user_ = add_magic_quotes(user_)
    if (not php_empty(lambda : userdata_["user_pass"])) and userdata_["user_pass"] != user_obj_.user_pass:
        #// If password is changing, hash it now.
        plaintext_pass_ = userdata_["user_pass"]
        userdata_["user_pass"] = wp_hash_password(userdata_["user_pass"])
        #// 
        #// Filters whether to send the password change email.
        #// 
        #// @since 4.3.0
        #// 
        #// @see wp_insert_user() For `$user` and `$userdata` fields.
        #// 
        #// @param bool  $send     Whether to send the email.
        #// @param array $user     The original user array.
        #// @param array $userdata The updated user array.
        #//
        send_password_change_email_ = apply_filters("send_password_change_email", True, user_, userdata_)
    # end if
    if (php_isset(lambda : userdata_["user_email"])) and user_["user_email"] != userdata_["user_email"]:
        #// 
        #// Filters whether to send the email change email.
        #// 
        #// @since 4.3.0
        #// 
        #// @see wp_insert_user() For `$user` and `$userdata` fields.
        #// 
        #// @param bool  $send     Whether to send the email.
        #// @param array $user     The original user array.
        #// @param array $userdata The updated user array.
        #//
        send_email_change_email_ = apply_filters("send_email_change_email", True, user_, userdata_)
    # end if
    clean_user_cache(user_obj_)
    #// Merge old and new fields with new fields overwriting old ones.
    userdata_ = php_array_merge(user_, userdata_)
    user_id_ = wp_insert_user(userdata_)
    if (not is_wp_error(user_id_)):
        blog_name_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        switched_locale_ = False
        if (not php_empty(lambda : send_password_change_email_)) or (not php_empty(lambda : send_email_change_email_)):
            switched_locale_ = switch_to_locale(get_user_locale(user_id_))
        # end if
        if (not php_empty(lambda : send_password_change_email_)):
            #// translators: Do not translate USERNAME, ADMIN_EMAIL, EMAIL, SITENAME, SITEURL: those are placeholders.
            pass_change_text_ = __("""Hi ###USERNAME###,
            This notice confirms that your password was changed on ###SITENAME###.
            If you did not change your password, please contact the Site Administrator at
            ###ADMIN_EMAIL###
            This email has been sent to ###EMAIL###
            Regards,
            All at ###SITENAME###
            ###SITEURL###""")
            pass_change_email_ = Array({"to": user_["user_email"], "subject": __("[%s] Password Changed"), "message": pass_change_text_, "headers": ""})
            #// 
            #// Filters the contents of the email sent when the user's password is changed.
            #// 
            #// @since 4.3.0
            #// 
            #// @param array $pass_change_email {
            #// Used to build wp_mail().
            #// @type string $to      The intended recipients. Add emails in a comma separated string.
            #// @type string $subject The subject of the email.
            #// @type string $message The content of the email.
            #// The following strings have a special meaning and will get replaced dynamically:
            #// - ###USERNAME###    The current user's username.
            #// - ###ADMIN_EMAIL### The admin email in case this was unexpected.
            #// - ###EMAIL###       The user's email address.
            #// - ###SITENAME###    The name of the site.
            #// - ###SITEURL###     The URL to the site.
            #// @type string $headers Headers. Add headers in a newline (\r\n) separated string.
            #// }
            #// @param array $user     The original user array.
            #// @param array $userdata The updated user array.
            #//
            pass_change_email_ = apply_filters("password_change_email", pass_change_email_, user_, userdata_)
            pass_change_email_["message"] = php_str_replace("###USERNAME###", user_["user_login"], pass_change_email_["message"])
            pass_change_email_["message"] = php_str_replace("###ADMIN_EMAIL###", get_option("admin_email"), pass_change_email_["message"])
            pass_change_email_["message"] = php_str_replace("###EMAIL###", user_["user_email"], pass_change_email_["message"])
            pass_change_email_["message"] = php_str_replace("###SITENAME###", blog_name_, pass_change_email_["message"])
            pass_change_email_["message"] = php_str_replace("###SITEURL###", home_url(), pass_change_email_["message"])
            wp_mail(pass_change_email_["to"], php_sprintf(pass_change_email_["subject"], blog_name_), pass_change_email_["message"], pass_change_email_["headers"])
        # end if
        if (not php_empty(lambda : send_email_change_email_)):
            #// translators: Do not translate USERNAME, ADMIN_EMAIL, NEW_EMAIL, EMAIL, SITENAME, SITEURL: those are placeholders.
            email_change_text_ = __("""Hi ###USERNAME###,
            This notice confirms that your email address on ###SITENAME### was changed to ###NEW_EMAIL###.
            If you did not change your email, please contact the Site Administrator at
            ###ADMIN_EMAIL###
            This email has been sent to ###EMAIL###
            Regards,
            All at ###SITENAME###
            ###SITEURL###""")
            email_change_email_ = Array({"to": user_["user_email"], "subject": __("[%s] Email Changed"), "message": email_change_text_, "headers": ""})
            #// 
            #// Filters the contents of the email sent when the user's email is changed.
            #// 
            #// @since 4.3.0
            #// 
            #// @param array $email_change_email {
            #// Used to build wp_mail().
            #// @type string $to      The intended recipients.
            #// @type string $subject The subject of the email.
            #// @type string $message The content of the email.
            #// The following strings have a special meaning and will get replaced dynamically:
            #// - ###USERNAME###    The current user's username.
            #// - ###ADMIN_EMAIL### The admin email in case this was unexpected.
            #// - ###NEW_EMAIL###   The new email address.
            #// - ###EMAIL###       The old email address.
            #// - ###SITENAME###    The name of the site.
            #// - ###SITEURL###     The URL to the site.
            #// @type string $headers Headers.
            #// }
            #// @param array $user The original user array.
            #// @param array $userdata The updated user array.
            #//
            email_change_email_ = apply_filters("email_change_email", email_change_email_, user_, userdata_)
            email_change_email_["message"] = php_str_replace("###USERNAME###", user_["user_login"], email_change_email_["message"])
            email_change_email_["message"] = php_str_replace("###ADMIN_EMAIL###", get_option("admin_email"), email_change_email_["message"])
            email_change_email_["message"] = php_str_replace("###NEW_EMAIL###", userdata_["user_email"], email_change_email_["message"])
            email_change_email_["message"] = php_str_replace("###EMAIL###", user_["user_email"], email_change_email_["message"])
            email_change_email_["message"] = php_str_replace("###SITENAME###", blog_name_, email_change_email_["message"])
            email_change_email_["message"] = php_str_replace("###SITEURL###", home_url(), email_change_email_["message"])
            wp_mail(email_change_email_["to"], php_sprintf(email_change_email_["subject"], blog_name_), email_change_email_["message"], email_change_email_["headers"])
        # end if
        if switched_locale_:
            restore_previous_locale()
        # end if
    # end if
    #// Update the cookies if the password changed.
    current_user_ = wp_get_current_user()
    if current_user_.ID == ID_:
        if (php_isset(lambda : plaintext_pass_)):
            wp_clear_auth_cookie()
            #// Here we calculate the expiration length of the current auth cookie and compare it to the default expiration.
            #// If it's greater than this, then we know the user checked 'Remember Me' when they logged in.
            logged_in_cookie_ = wp_parse_auth_cookie("", "logged_in")
            #// This filter is documented in wp-includes/pluggable.php
            default_cookie_life_ = apply_filters("auth_cookie_expiration", 2 * DAY_IN_SECONDS, ID_, False)
            remember_ = False
            if False != logged_in_cookie_ and logged_in_cookie_["expiration"] - time() > default_cookie_life_:
                remember_ = True
            # end if
            wp_set_auth_cookie(ID_, remember_)
        # end if
    # end if
    return user_id_
# end def wp_update_user
#// 
#// A simpler way of inserting a user into the database.
#// 
#// Creates a new user with just the username, password, and email. For more
#// complex user creation use wp_insert_user() to specify more information.
#// 
#// @since 2.0.0
#// @see wp_insert_user() More complete way to create a new user
#// 
#// @param string $username The user's username.
#// @param string $password The user's password.
#// @param string $email    Optional. The user's email. Default empty.
#// @return int|WP_Error The newly created user's ID or a WP_Error object if the user could not
#// be created.
#//
def wp_create_user(username_=None, password_=None, email_="", *_args_):
    
    
    user_login_ = wp_slash(username_)
    user_email_ = wp_slash(email_)
    user_pass_ = password_
    userdata_ = php_compact("user_login", "user_email", "user_pass")
    return wp_insert_user(userdata_)
# end def wp_create_user
#// 
#// Returns a list of meta keys to be (maybe) populated in wp_update_user().
#// 
#// The list of keys returned via this function are dependent on the presence
#// of those keys in the user meta data to be set.
#// 
#// @since 3.3.0
#// @access private
#// 
#// @param WP_User $user WP_User instance.
#// @return string[] List of user keys to be populated in wp_update_user().
#//
def _get_additional_user_keys(user_=None, *_args_):
    
    
    keys_ = Array("first_name", "last_name", "nickname", "description", "rich_editing", "syntax_highlighting", "comment_shortcuts", "admin_color", "use_ssl", "show_admin_bar_front", "locale")
    return php_array_merge(keys_, php_array_keys(wp_get_user_contact_methods(user_)))
# end def _get_additional_user_keys
#// 
#// Set up the user contact methods.
#// 
#// Default contact methods were removed in 3.6. A filter dictates contact methods.
#// 
#// @since 3.7.0
#// 
#// @param WP_User $user Optional. WP_User object.
#// @return string[] Array of contact method labels keyed by contact method.
#//
def wp_get_user_contact_methods(user_=None, *_args_):
    
    
    methods_ = Array()
    if get_site_option("initial_db_version") < 23588:
        methods_ = Array({"aim": __("AIM"), "yim": __("Yahoo IM"), "jabber": __("Jabber / Google Talk")})
    # end if
    #// 
    #// Filters the user contact methods.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string[] $methods Array of contact method labels keyed by contact method.
    #// @param WP_User  $user    WP_User object.
    #//
    return apply_filters("user_contactmethods", methods_, user_)
# end def wp_get_user_contact_methods
#// 
#// The old private function for setting up user contact methods.
#// 
#// Use wp_get_user_contact_methods() instead.
#// 
#// @since 2.9.0
#// @access private
#// 
#// @param WP_User $user Optional. WP_User object. Default null.
#// @return string[] Array of contact method labels keyed by contact method.
#//
def _wp_get_user_contactmethods(user_=None, *_args_):
    
    
    return wp_get_user_contact_methods(user_)
# end def _wp_get_user_contactmethods
#// 
#// Gets the text suggesting how to create strong passwords.
#// 
#// @since 4.1.0
#// 
#// @return string The password hint text.
#//
def wp_get_password_hint(*_args_):
    
    
    hint_ = __("Hint: The password should be at least twelve characters long. To make it stronger, use upper and lower case letters, numbers, and symbols like ! \" ? $ % ^ &amp; ).")
    #// 
    #// Filters the text describing the site's password complexity policy.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $hint The password hint text.
    #//
    return apply_filters("password_hint", hint_)
# end def wp_get_password_hint
#// 
#// Creates, stores, then returns a password reset key for user.
#// 
#// @since 4.4.0
#// 
#// @global PasswordHash $wp_hasher Portable PHP password hashing framework.
#// 
#// @param WP_User $user User to retrieve password reset key for.
#// 
#// @return string|WP_Error Password reset key on success. WP_Error on error.
#//
def get_password_reset_key(user_=None, *_args_):
    
    
    global wp_hasher_
    php_check_if_defined("wp_hasher_")
    if (not type(user_).__name__ == "WP_User"):
        return php_new_class("WP_Error", lambda : WP_Error("invalidcombo", __("<strong>Error</strong>: There is no account with that username or email address.")))
    # end if
    #// 
    #// Fires before a new password is retrieved.
    #// 
    #// Use the {@see 'retrieve_password'} hook instead.
    #// 
    #// @since 1.5.0
    #// @deprecated 1.5.1 Misspelled. Use {@see 'retrieve_password'} hook instead.
    #// 
    #// @param string $user_login The user login name.
    #//
    do_action_deprecated("retreive_password", Array(user_.user_login), "1.5.1", "retrieve_password")
    #// 
    #// Fires before a new password is retrieved.
    #// 
    #// @since 1.5.1
    #// 
    #// @param string $user_login The user login name.
    #//
    do_action("retrieve_password", user_.user_login)
    allow_ = True
    if is_multisite() and is_user_spammy(user_):
        allow_ = False
    # end if
    #// 
    #// Filters whether to allow a password to be reset.
    #// 
    #// @since 2.7.0
    #// 
    #// @param bool $allow         Whether to allow the password to be reset. Default true.
    #// @param int  $user_data->ID The ID of the user attempting to reset a password.
    #//
    allow_ = apply_filters("allow_password_reset", allow_, user_.ID)
    if (not allow_):
        return php_new_class("WP_Error", lambda : WP_Error("no_password_reset", __("Password reset is not allowed for this user")))
    elif is_wp_error(allow_):
        return allow_
    # end if
    #// Generate something random for a password reset key.
    key_ = wp_generate_password(20, False)
    #// 
    #// Fires when a password reset key is generated.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $user_login The username for the user.
    #// @param string $key        The generated password reset key.
    #//
    do_action("retrieve_password_key", user_.user_login, key_)
    #// Now insert the key, hashed, into the DB.
    if php_empty(lambda : wp_hasher_):
        php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
        wp_hasher_ = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
    # end if
    hashed_ = time() + ":" + wp_hasher_.hashpassword(key_)
    key_saved_ = wp_update_user(Array({"ID": user_.ID, "user_activation_key": hashed_}))
    if is_wp_error(key_saved_):
        return key_saved_
    # end if
    return key_
# end def get_password_reset_key
#// 
#// Retrieves a user row based on password reset key and login
#// 
#// A key is considered 'expired' if it exactly matches the value of the
#// user_activation_key field, rather than being matched after going through the
#// hashing process. This field is now hashed; old values are no longer accepted
#// but have a different WP_Error code so good user feedback can be provided.
#// 
#// @since 3.1.0
#// 
#// @global wpdb         $wpdb      WordPress database object for queries.
#// @global PasswordHash $wp_hasher Portable PHP password hashing framework instance.
#// 
#// @param string $key       Hash to validate sending user's password.
#// @param string $login     The user login.
#// @return WP_User|WP_Error WP_User object on success, WP_Error object for invalid or expired keys.
#//
def check_password_reset_key(key_=None, login_=None, *_args_):
    
    
    global wpdb_
    global wp_hasher_
    php_check_if_defined("wpdb_","wp_hasher_")
    key_ = php_preg_replace("/[^a-z0-9]/i", "", key_)
    if php_empty(lambda : key_) or (not php_is_string(key_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid key.")))
    # end if
    if php_empty(lambda : login_) or (not php_is_string(login_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid key.")))
    # end if
    user_ = get_user_by("login", login_)
    if (not user_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid key.")))
    # end if
    if php_empty(lambda : wp_hasher_):
        php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
        wp_hasher_ = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
    # end if
    #// 
    #// Filters the expiration time of password reset keys.
    #// 
    #// @since 4.3.0
    #// 
    #// @param int $expiration The expiration time in seconds.
    #//
    expiration_duration_ = apply_filters("password_reset_expiration", DAY_IN_SECONDS)
    if False != php_strpos(user_.user_activation_key, ":"):
        pass_request_time_, pass_key_ = php_explode(":", user_.user_activation_key, 2)
        expiration_time_ = pass_request_time_ + expiration_duration_
    else:
        pass_key_ = user_.user_activation_key
        expiration_time_ = False
    # end if
    if (not pass_key_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid key.")))
    # end if
    hash_is_correct_ = wp_hasher_.checkpassword(key_, pass_key_)
    if hash_is_correct_ and expiration_time_ and time() < expiration_time_:
        return user_
    elif hash_is_correct_ and expiration_time_:
        #// Key has an expiration time that's passed.
        return php_new_class("WP_Error", lambda : WP_Error("expired_key", __("Invalid key.")))
    # end if
    if hash_equals(user_.user_activation_key, key_) or hash_is_correct_ and (not expiration_time_):
        return_ = php_new_class("WP_Error", lambda : WP_Error("expired_key", __("Invalid key.")))
        user_id_ = user_.ID
        #// 
        #// Filters the return value of check_password_reset_key() when an
        #// old-style key is used.
        #// 
        #// @since 3.7.0 Previously plain-text keys were stored in the database.
        #// @since 4.3.0 Previously key hashes were stored without an expiration time.
        #// 
        #// @param WP_Error $return  A WP_Error object denoting an expired key.
        #// Return a WP_User object to validate the key.
        #// @param int      $user_id The matched user ID.
        #//
        return apply_filters("password_reset_key_expired", return_, user_id_)
    # end if
    return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid key.")))
# end def check_password_reset_key
#// 
#// Handles resetting the user's password.
#// 
#// @since 2.5.0
#// 
#// @param WP_User $user     The user
#// @param string $new_pass New password for the user in plaintext
#//
def reset_password(user_=None, new_pass_=None, *_args_):
    
    
    #// 
    #// Fires before the user's password is reset.
    #// 
    #// @since 1.5.0
    #// 
    #// @param WP_User $user     The user.
    #// @param string  $new_pass New user password.
    #//
    do_action("password_reset", user_, new_pass_)
    wp_set_password(new_pass_, user_.ID)
    update_user_option(user_.ID, "default_password_nag", False, True)
    #// 
    #// Fires after the user's password is reset.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_User $user     The user.
    #// @param string  $new_pass New user password.
    #//
    do_action("after_password_reset", user_, new_pass_)
# end def reset_password
#// 
#// Handles registering a new user.
#// 
#// @since 2.5.0
#// 
#// @param string $user_login User's username for logging in
#// @param string $user_email User's email address to send password and add
#// @return int|WP_Error Either user's ID or error on failure.
#//
def register_new_user(user_login_=None, user_email_=None, *_args_):
    
    
    errors_ = php_new_class("WP_Error", lambda : WP_Error())
    sanitized_user_login_ = sanitize_user(user_login_)
    #// 
    #// Filters the email address of a user being registered.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $user_email The email address of the new user.
    #//
    user_email_ = apply_filters("user_registration_email", user_email_)
    #// Check the username.
    if "" == sanitized_user_login_:
        errors_.add("empty_username", __("<strong>Error</strong>: Please enter a username."))
    elif (not validate_username(user_login_)):
        errors_.add("invalid_username", __("<strong>Error</strong>: This username is invalid because it uses illegal characters. Please enter a valid username."))
        sanitized_user_login_ = ""
    elif username_exists(sanitized_user_login_):
        errors_.add("username_exists", __("<strong>Error</strong>: This username is already registered. Please choose another one."))
    else:
        #// This filter is documented in wp-includes/user.php
        illegal_user_logins_ = apply_filters("illegal_user_logins", Array())
        if php_in_array(php_strtolower(sanitized_user_login_), php_array_map("strtolower", illegal_user_logins_), True):
            errors_.add("invalid_username", __("<strong>Error</strong>: Sorry, that username is not allowed."))
        # end if
    # end if
    #// Check the email address.
    if "" == user_email_:
        errors_.add("empty_email", __("<strong>Error</strong>: Please type your email address."))
    elif (not is_email(user_email_)):
        errors_.add("invalid_email", __("<strong>Error</strong>: The email address isn&#8217;t correct."))
        user_email_ = ""
    elif email_exists(user_email_):
        errors_.add("email_exists", __("<strong>Error</strong>: This email is already registered, please choose another one."))
    # end if
    #// 
    #// Fires when submitting registration form data, before the user is created.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string   $sanitized_user_login The submitted username after being sanitized.
    #// @param string   $user_email           The submitted email.
    #// @param WP_Error $errors               Contains any errors with submitted username and email,
    #// e.g., an empty field, an invalid username or email,
    #// or an existing username or email.
    #//
    do_action("register_post", sanitized_user_login_, user_email_, errors_)
    #// 
    #// Filters the errors encountered when a new user is being registered.
    #// 
    #// The filtered WP_Error object may, for example, contain errors for an invalid
    #// or existing username or email address. A WP_Error object should always returned,
    #// but may or may not contain errors.
    #// 
    #// If any errors are present in $errors, this will abort the user's registration.
    #// 
    #// @since 2.1.0
    #// 
    #// @param WP_Error $errors               A WP_Error object containing any errors encountered
    #// during registration.
    #// @param string   $sanitized_user_login User's username after it has been sanitized.
    #// @param string   $user_email           User's email.
    #//
    errors_ = apply_filters("registration_errors", errors_, sanitized_user_login_, user_email_)
    if errors_.has_errors():
        return errors_
    # end if
    user_pass_ = wp_generate_password(12, False)
    user_id_ = wp_create_user(sanitized_user_login_, user_pass_, user_email_)
    if (not user_id_) or is_wp_error(user_id_):
        errors_.add("registerfail", php_sprintf(__("<strong>Error</strong>: Couldn&#8217;t register you&hellip; please contact the <a href=\"mailto:%s\">webmaster</a> !"), get_option("admin_email")))
        return errors_
    # end if
    update_user_option(user_id_, "default_password_nag", True, True)
    #// Set up the password change nag.
    #// 
    #// Fires after a new user registration has been recorded.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int $user_id ID of the newly registered user.
    #//
    do_action("register_new_user", user_id_)
    return user_id_
# end def register_new_user
#// 
#// Initiates email notifications related to the creation of new users.
#// 
#// Notifications are sent both to the site admin and to the newly created user.
#// 
#// @since 4.4.0
#// @since 4.6.0 Converted the `$notify` parameter to accept 'user' for sending
#// notifications only to the user created.
#// 
#// @param int    $user_id ID of the newly created user.
#// @param string $notify  Optional. Type of notification that should happen. Accepts 'admin'
#// or an empty string (admin only), 'user', or 'both' (admin and user).
#// Default 'both'.
#//
def wp_send_new_user_notifications(user_id_=None, notify_="both", *_args_):
    
    
    wp_new_user_notification(user_id_, None, notify_)
# end def wp_send_new_user_notifications
#// 
#// Retrieve the current session token from the logged_in cookie.
#// 
#// @since 4.0.0
#// 
#// @return string Token.
#//
def wp_get_session_token(*_args_):
    
    
    cookie_ = wp_parse_auth_cookie("", "logged_in")
    return cookie_["token"] if (not php_empty(lambda : cookie_["token"])) else ""
# end def wp_get_session_token
#// 
#// Retrieve a list of sessions for the current user.
#// 
#// @since 4.0.0
#// @return array Array of sessions.
#//
def wp_get_all_sessions(*_args_):
    
    
    manager_ = WP_Session_Tokens.get_instance(get_current_user_id())
    return manager_.get_all()
# end def wp_get_all_sessions
#// 
#// Remove the current session token from the database.
#// 
#// @since 4.0.0
#//
def wp_destroy_current_session(*_args_):
    
    
    token_ = wp_get_session_token()
    if token_:
        manager_ = WP_Session_Tokens.get_instance(get_current_user_id())
        manager_.destroy(token_)
    # end if
# end def wp_destroy_current_session
#// 
#// Remove all but the current session token for the current user for the database.
#// 
#// @since 4.0.0
#//
def wp_destroy_other_sessions(*_args_):
    
    
    token_ = wp_get_session_token()
    if token_:
        manager_ = WP_Session_Tokens.get_instance(get_current_user_id())
        manager_.destroy_others(token_)
    # end if
# end def wp_destroy_other_sessions
#// 
#// Remove all session tokens for the current user from the database.
#// 
#// @since 4.0.0
#//
def wp_destroy_all_sessions(*_args_):
    
    
    manager_ = WP_Session_Tokens.get_instance(get_current_user_id())
    manager_.destroy_all()
# end def wp_destroy_all_sessions
#// 
#// Get the user IDs of all users with no role on this site.
#// 
#// @since 4.4.0
#// @since 4.9.0 The `$site_id` parameter was added to support multisite.
#// 
#// @param int|null $site_id Optional. The site ID to get users with no role for. Defaults to the current site.
#// @return string[] Array of user IDs as strings.
#//
def wp_get_users_with_no_role(site_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not site_id_):
        site_id_ = get_current_blog_id()
    # end if
    prefix_ = wpdb_.get_blog_prefix(site_id_)
    if is_multisite() and get_current_blog_id() != site_id_:
        switch_to_blog(site_id_)
        role_names_ = wp_roles().get_names()
        restore_current_blog()
    else:
        role_names_ = wp_roles().get_names()
    # end if
    regex_ = php_implode("|", php_array_keys(role_names_))
    regex_ = php_preg_replace("/[^a-zA-Z_\\|-]/", "", regex_)
    users_ = wpdb_.get_col(wpdb_.prepare(str("\n        SELECT user_id\n        FROM ") + str(wpdb_.usermeta) + str("\n     WHERE meta_key = '") + str(prefix_) + str("capabilities'\n      AND meta_value NOT REGEXP %s\n  "), regex_))
    return users_
# end def wp_get_users_with_no_role
#// 
#// Retrieves the current user object.
#// 
#// Will set the current user, if the current user is not set. The current user
#// will be set to the logged-in person. If no user is logged-in, then it will
#// set the current user to 0, which is invalid and won't have any permissions.
#// 
#// This function is used by the pluggable functions wp_get_current_user() and
#// get_currentuserinfo(), the latter of which is deprecated but used for backward
#// compatibility.
#// 
#// @since 4.5.0
#// @access private
#// 
#// @see wp_get_current_user()
#// @global WP_User $current_user Checks if the current user is set.
#// 
#// @return WP_User Current WP_User instance.
#//
def _wp_get_current_user(*_args_):
    
    
    global current_user_
    php_check_if_defined("current_user_")
    if (not php_empty(lambda : current_user_)):
        if type(current_user_).__name__ == "WP_User":
            return current_user_
        # end if
        #// Upgrade stdClass to WP_User.
        if php_is_object(current_user_) and (php_isset(lambda : current_user_.ID)):
            cur_id_ = current_user_.ID
            current_user_ = None
            wp_set_current_user(cur_id_)
            return current_user_
        # end if
        #// $current_user has a junk value. Force to WP_User with ID 0.
        current_user_ = None
        wp_set_current_user(0)
        return current_user_
    # end if
    if php_defined("XMLRPC_REQUEST") and XMLRPC_REQUEST:
        wp_set_current_user(0)
        return current_user_
    # end if
    #// 
    #// Filters the current user.
    #// 
    #// The default filters use this to determine the current user from the
    #// request's cookies, if available.
    #// 
    #// Returning a value of false will effectively short-circuit setting
    #// the current user.
    #// 
    #// @since 3.9.0
    #// 
    #// @param int|bool $user_id User ID if one has been determined, false otherwise.
    #//
    user_id_ = apply_filters("determine_current_user", False)
    if (not user_id_):
        wp_set_current_user(0)
        return current_user_
    # end if
    wp_set_current_user(user_id_)
    return current_user_
# end def _wp_get_current_user
#// 
#// Send a confirmation request email when a change of user email address is attempted.
#// 
#// @since 3.0.0
#// @since 4.9.0 This function was moved from wp-admin/includes/ms.php so it's no longer Multisite specific.
#// 
#// @global WP_Error $errors WP_Error object.
#//
def send_confirmation_on_profile_email(*_args_):
    
    global PHP_POST
    global errors_
    php_check_if_defined("errors_")
    current_user_ = wp_get_current_user()
    if (not php_is_object(errors_)):
        errors_ = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    if current_user_.ID != PHP_POST["user_id"]:
        return False
    # end if
    if current_user_.user_email != PHP_POST["email"]:
        if (not is_email(PHP_POST["email"])):
            errors_.add("user_email", __("<strong>Error</strong>: The email address isn&#8217;t correct."), Array({"form-field": "email"}))
            return
        # end if
        if email_exists(PHP_POST["email"]):
            errors_.add("user_email", __("<strong>Error</strong>: The email address is already used."), Array({"form-field": "email"}))
            delete_user_meta(current_user_.ID, "_new_email")
            return
        # end if
        hash_ = php_md5(PHP_POST["email"] + time() + wp_rand())
        new_user_email_ = Array({"hash": hash_, "newemail": PHP_POST["email"]})
        update_user_meta(current_user_.ID, "_new_email", new_user_email_)
        sitename_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        #// translators: Do not translate USERNAME, ADMIN_URL, EMAIL, SITENAME, SITEURL: those are placeholders.
        email_text_ = __("""Howdy ###USERNAME###,
        You recently requested to have the email address on your account changed.
        If this is correct, please click on the following link to change it:
        ###ADMIN_URL###
        You can safely ignore and delete this email if you do not want to
        take this action.
        This email has been sent to ###EMAIL###
        Regards,
        All at ###SITENAME###
        ###SITEURL###""")
        #// 
        #// Filters the text of the email sent when a change of user email address is attempted.
        #// 
        #// The following strings have a special meaning and will get replaced dynamically:
        #// ###USERNAME###  The current user's username.
        #// ###ADMIN_URL### The link to click on to confirm the email change.
        #// ###EMAIL###     The new email.
        #// ###SITENAME###  The name of the site.
        #// ###SITEURL###   The URL to the site.
        #// 
        #// @since MU (3.0.0)
        #// @since 4.9.0 This filter is no longer Multisite specific.
        #// 
        #// @param string $email_text     Text in the email.
        #// @param array  $new_user_email {
        #// Data relating to the new user email address.
        #// 
        #// @type string $hash     The secure hash used in the confirmation link URL.
        #// @type string $newemail The proposed new email address.
        #// }
        #//
        content_ = apply_filters("new_user_email_content", email_text_, new_user_email_)
        content_ = php_str_replace("###USERNAME###", current_user_.user_login, content_)
        content_ = php_str_replace("###ADMIN_URL###", esc_url(admin_url("profile.php?newuseremail=" + hash_)), content_)
        content_ = php_str_replace("###EMAIL###", PHP_POST["email"], content_)
        content_ = php_str_replace("###SITENAME###", sitename_, content_)
        content_ = php_str_replace("###SITEURL###", home_url(), content_)
        #// translators: New email address notification email subject. %s: Site title.
        wp_mail(PHP_POST["email"], php_sprintf(__("[%s] Email Change Request"), sitename_), content_)
        PHP_POST["email"] = current_user_.user_email
    # end if
# end def send_confirmation_on_profile_email
#// 
#// Adds an admin notice alerting the user to check for confirmation request email
#// after email address change.
#// 
#// @since 3.0.0
#// @since 4.9.0 This function was moved from wp-admin/includes/ms.php so it's no longer Multisite specific.
#// 
#// @global string $pagenow
#//
def new_user_email_admin_notice(*_args_):
    
    
    global pagenow_
    php_check_if_defined("pagenow_")
    if "profile.php" == pagenow_ and (php_isset(lambda : PHP_REQUEST["updated"])):
        email_ = get_user_meta(get_current_user_id(), "_new_email", True)
        if email_:
            #// translators: %s: New email address.
            php_print("<div class=\"notice notice-info\"><p>" + php_sprintf(__("Your email address has not been updated yet. Please check your inbox at %s for a confirmation email."), "<code>" + esc_html(email_["newemail"]) + "</code>") + "</p></div>")
        # end if
    # end if
# end def new_user_email_admin_notice
#// 
#// Get all user privacy request types.
#// 
#// @since 4.9.6
#// @access private
#// 
#// @return array List of core privacy action types.
#//
def _wp_privacy_action_request_types(*_args_):
    
    
    return Array("export_personal_data", "remove_personal_data")
# end def _wp_privacy_action_request_types
#// 
#// Registers the personal data exporter for users.
#// 
#// @since 4.9.6
#// 
#// @param array $exporters  An array of personal data exporters.
#// @return array An array of personal data exporters.
#//
def wp_register_user_personal_data_exporter(exporters_=None, *_args_):
    
    
    exporters_["wordpress-user"] = Array({"exporter_friendly_name": __("WordPress User"), "callback": "wp_user_personal_data_exporter"})
    return exporters_
# end def wp_register_user_personal_data_exporter
#// 
#// Finds and exports personal data associated with an email address from the user and user_meta table.
#// 
#// @since 4.9.6
#// @since 5.4.0 Added 'Community Events Location' group to the export data.
#// @since 5.4.0 Added 'Session Tokens' group to the export data.
#// 
#// @param string $email_address  The user's email address.
#// @return array An array of personal data.
#//
def wp_user_personal_data_exporter(email_address_=None, *_args_):
    
    
    email_address_ = php_trim(email_address_)
    data_to_export_ = Array()
    user_ = get_user_by("email", email_address_)
    if (not user_):
        return Array({"data": Array(), "done": True})
    # end if
    user_meta_ = get_user_meta(user_.ID)
    user_props_to_export_ = Array({"ID": __("User ID"), "user_login": __("User Login Name"), "user_nicename": __("User Nice Name"), "user_email": __("User Email"), "user_url": __("User URL"), "user_registered": __("User Registration Date"), "display_name": __("User Display Name"), "nickname": __("User Nickname"), "first_name": __("User First Name"), "last_name": __("User Last Name"), "description": __("User Description")})
    user_data_to_export_ = Array()
    for key_,name_ in user_props_to_export_:
        value_ = ""
        for case in Switch(key_):
            if case("ID"):
                pass
            # end if
            if case("user_login"):
                pass
            # end if
            if case("user_nicename"):
                pass
            # end if
            if case("user_email"):
                pass
            # end if
            if case("user_url"):
                pass
            # end if
            if case("user_registered"):
                pass
            # end if
            if case("display_name"):
                value_ = user_.data.key_
                break
            # end if
            if case("nickname"):
                pass
            # end if
            if case("first_name"):
                pass
            # end if
            if case("last_name"):
                pass
            # end if
            if case("description"):
                value_ = user_meta_[key_][0]
                break
            # end if
        # end for
        if (not php_empty(lambda : value_)):
            user_data_to_export_[-1] = Array({"name": name_, "value": value_})
        # end if
    # end for
    #// Get the list of reserved names.
    reserved_names_ = php_array_values(user_props_to_export_)
    #// 
    #// Filter to extend the user's profile data for the privacy exporter.
    #// 
    #// @since 5.4.0
    #// 
    #// @param array    $additional_user_profile_data {
    #// An array of name-value pairs of additional user data items. Default empty array.
    #// 
    #// @type string $name  The user-facing name of an item name-value pair,e.g. 'IP Address'.
    #// @type string $value The user-facing value of an item data pair, e.g. '50.60.70.0'.
    #// }
    #// @param WP_User  $user           The user whose data is being exported.
    #// @param string[] $reserved_names An array of reserved names. Any item in `$additional_user_data`
    #// that uses one of these for its `name` will not be included in the export.
    #//
    _extra_data_ = apply_filters("wp_privacy_additional_user_profile_data", Array(), user_, reserved_names_)
    if php_is_array(_extra_data_) and (not php_empty(lambda : _extra_data_)):
        #// Remove items that use reserved names.
        extra_data_ = php_array_filter(_extra_data_, (lambda item_=None:  (not php_in_array(item_["name"], reserved_names_, True))))
        if php_count(extra_data_) != php_count(_extra_data_):
            _doing_it_wrong(__FUNCTION__, php_sprintf(__("Filter %s returned items with reserved names."), "<code>wp_privacy_additional_user_profile_data</code>"), "5.4.0")
        # end if
        if (not php_empty(lambda : extra_data_)):
            user_data_to_export_ = php_array_merge(user_data_to_export_, extra_data_)
        # end if
    # end if
    data_to_export_[-1] = Array({"group_id": "user", "group_label": __("User"), "group_description": __("User&#8217;s profile data."), "item_id": str("user-") + str(user_.ID), "data": user_data_to_export_})
    if (php_isset(lambda : user_meta_["community-events-location"])):
        location_ = maybe_unserialize(user_meta_["community-events-location"][0])
        location_props_to_export_ = Array({"description": __("City"), "country": __("Country"), "latitude": __("Latitude"), "longitude": __("Longitude"), "ip": __("IP")})
        location_data_to_export_ = Array()
        for key_,name_ in location_props_to_export_:
            if (not php_empty(lambda : location_[key_])):
                location_data_to_export_[-1] = Array({"name": name_, "value": location_[key_]})
            # end if
        # end for
        data_to_export_[-1] = Array({"group_id": "community-events-location", "group_label": __("Community Events Location"), "group_description": __("User&#8217;s location data used for the Community Events in the WordPress Events and News dashboard widget."), "item_id": str("community-events-location-") + str(user_.ID), "data": location_data_to_export_})
    # end if
    if (php_isset(lambda : user_meta_["session_tokens"])):
        session_tokens_ = maybe_unserialize(user_meta_["session_tokens"][0])
        session_tokens_props_to_export_ = Array({"expiration": __("Expiration"), "ip": __("IP"), "ua": __("User Agent"), "login": __("Last Login")})
        for token_key_,session_token_ in session_tokens_:
            session_tokens_data_to_export_ = Array()
            for key_,name_ in session_tokens_props_to_export_:
                if (not php_empty(lambda : session_token_[key_])):
                    value_ = session_token_[key_]
                    if php_in_array(key_, Array("expiration", "login")):
                        value_ = date_i18n("F d, Y H:i A", value_)
                    # end if
                    session_tokens_data_to_export_[-1] = Array({"name": name_, "value": value_})
                # end if
            # end for
            data_to_export_[-1] = Array({"group_id": "session-tokens", "group_label": __("Session Tokens"), "group_description": __("User&#8217;s Session Tokens data."), "item_id": str("session-tokens-") + str(user_.ID) + str("-") + str(token_key_), "data": session_tokens_data_to_export_})
        # end for
    # end if
    return Array({"data": data_to_export_, "done": True})
# end def wp_user_personal_data_exporter
#// 
#// Update log when privacy request is confirmed.
#// 
#// @since 4.9.6
#// @access private
#// 
#// @param int $request_id ID of the request.
#//
def _wp_privacy_account_request_confirmed(request_id_=None, *_args_):
    
    
    request_ = wp_get_user_request(request_id_)
    if (not request_):
        return
    # end if
    if (not php_in_array(request_.status, Array("request-pending", "request-failed"), True)):
        return
    # end if
    update_post_meta(request_id_, "_wp_user_request_confirmed_timestamp", time())
    wp_update_post(Array({"ID": request_id_, "post_status": "request-confirmed"}))
# end def _wp_privacy_account_request_confirmed
#// 
#// Notify the site administrator via email when a request is confirmed.
#// 
#// Without this, the admin would have to manually check the site to see if any
#// action was needed on their part yet.
#// 
#// @since 4.9.6
#// 
#// @param int $request_id The ID of the request.
#//
def _wp_privacy_send_request_confirmation_notification(request_id_=None, *_args_):
    
    
    request_ = wp_get_user_request(request_id_)
    if (not php_is_a(request_, "WP_User_Request")) or "request-confirmed" != request_.status:
        return
    # end if
    already_notified_ = php_bool(get_post_meta(request_id_, "_wp_admin_notified", True))
    if already_notified_:
        return
    # end if
    if "export_personal_data" == request_.action_name:
        manage_url_ = admin_url("export-personal-data.php")
    elif "remove_personal_data" == request_.action_name:
        manage_url_ = admin_url("erase-personal-data.php")
    # end if
    action_description_ = wp_user_request_action_description(request_.action_name)
    #// 
    #// Filters the recipient of the data request confirmation notification.
    #// 
    #// In a Multisite environment, this will default to the email address of the
    #// network admin because, by default, single site admins do not have the
    #// capabilities required to process requests. Some networks may wish to
    #// delegate those capabilities to a single-site admin, or a dedicated person
    #// responsible for managing privacy requests.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string          $admin_email The email address of the notification recipient.
    #// @param WP_User_Request $request     The request that is initiating the notification.
    #//
    admin_email_ = apply_filters("user_request_confirmed_email_to", get_site_option("admin_email"), request_)
    email_data_ = Array({"request": request_, "user_email": request_.email, "description": action_description_, "manage_url": manage_url_, "sitename": wp_specialchars_decode(get_option("blogname"), ENT_QUOTES), "siteurl": home_url(), "admin_email": admin_email_})
    #// translators: Do not translate SITENAME, USER_EMAIL, DESCRIPTION, MANAGE_URL, SITEURL; those are placeholders.
    email_text_ = __("""Howdy,
    A user data privacy request has been confirmed on ###SITENAME###:
    User: ###USER_EMAIL###
    Request: ###DESCRIPTION###
    You can view and manage these data privacy requests here:
    ###MANAGE_URL###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    #// 
    #// Filters the body of the user request confirmation email.
    #// 
    #// The email is sent to an administrator when an user request is confirmed.
    #// The following strings have a special meaning and will get replaced dynamically:
    #// 
    #// ###SITENAME###    The name of the site.
    #// ###USER_EMAIL###  The user email for the request.
    #// ###DESCRIPTION### Description of the action being performed so the user knows what the email is for.
    #// ###MANAGE_URL###  The URL to manage requests.
    #// ###SITEURL###     The URL to the site.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $email_text Text in the email.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request     User request object.
    #// @type string          $user_email  The email address confirming a request
    #// @type string          $description Description of the action being performed so the user knows what the email is for.
    #// @type string          $manage_url  The link to click manage privacy requests of this type.
    #// @type string          $sitename    The site name sending the mail.
    #// @type string          $siteurl     The site URL sending the mail.
    #// @type string          $admin_email The administrator email receiving the mail.
    #// }
    #//
    content_ = apply_filters("user_confirmed_action_email_content", email_text_, email_data_)
    content_ = php_str_replace("###SITENAME###", email_data_["sitename"], content_)
    content_ = php_str_replace("###USER_EMAIL###", email_data_["user_email"], content_)
    content_ = php_str_replace("###DESCRIPTION###", email_data_["description"], content_)
    content_ = php_str_replace("###MANAGE_URL###", esc_url_raw(email_data_["manage_url"]), content_)
    content_ = php_str_replace("###SITEURL###", esc_url_raw(email_data_["siteurl"]), content_)
    subject_ = php_sprintf(__("[%1$s] Action Confirmed: %2$s"), email_data_["sitename"], action_description_)
    #// 
    #// Filters the subject of the user request confirmation email.
    #// 
    #// @since 4.9.8
    #// 
    #// @param string $subject    The email subject.
    #// @param string $sitename   The name of the site.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request     User request object.
    #// @type string          $user_email  The email address confirming a request
    #// @type string          $description Description of the action being performed so the user knows what the email is for.
    #// @type string          $manage_url  The link to click manage privacy requests of this type.
    #// @type string          $sitename    The site name sending the mail.
    #// @type string          $siteurl     The site URL sending the mail.
    #// @type string          $admin_email The administrator email receiving the mail.
    #// }
    #//
    subject_ = apply_filters("user_request_confirmed_email_subject", subject_, email_data_["sitename"], email_data_)
    headers_ = ""
    #// 
    #// Filters the headers of the user request confirmation email.
    #// 
    #// @since 5.4.0
    #// 
    #// @param string|array $headers    The email headers.
    #// @param string       $subject    The email subject.
    #// @param string       $content    The email content.
    #// @param int          $request_id The request ID.
    #// @param array        $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request     User request object.
    #// @type string          $user_email  The email address confirming a request
    #// @type string          $description Description of the action being performed so the user knows what the email is for.
    #// @type string          $manage_url  The link to click manage privacy requests of this type.
    #// @type string          $sitename    The site name sending the mail.
    #// @type string          $siteurl     The site URL sending the mail.
    #// @type string          $admin_email The administrator email receiving the mail.
    #// }
    #//
    headers_ = apply_filters("user_request_confirmed_email_headers", headers_, subject_, content_, request_id_, email_data_)
    email_sent_ = wp_mail(email_data_["admin_email"], subject_, content_, headers_)
    if email_sent_:
        update_post_meta(request_id_, "_wp_admin_notified", True)
    # end if
# end def _wp_privacy_send_request_confirmation_notification
#// 
#// Notify the user when their erasure request is fulfilled.
#// 
#// Without this, the user would never know if their data was actually erased.
#// 
#// @since 4.9.6
#// 
#// @param int $request_id The privacy request post ID associated with this request.
#//
def _wp_privacy_send_erasure_fulfillment_notification(request_id_=None, *_args_):
    
    
    request_ = wp_get_user_request(request_id_)
    if (not php_is_a(request_, "WP_User_Request")) or "request-completed" != request_.status:
        return
    # end if
    already_notified_ = php_bool(get_post_meta(request_id_, "_wp_user_notified", True))
    if already_notified_:
        return
    # end if
    #// Localize message content for user; fallback to site default for visitors.
    if (not php_empty(lambda : request_.user_id)):
        locale_ = get_user_locale(request_.user_id)
    else:
        locale_ = get_locale()
    # end if
    switched_locale_ = switch_to_locale(locale_)
    #// 
    #// Filters the recipient of the data erasure fulfillment notification.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string          $user_email The email address of the notification recipient.
    #// @param WP_User_Request $request    The request that is initiating the notification.
    #//
    user_email_ = apply_filters("user_erasure_fulfillment_email_to", request_.email, request_)
    email_data_ = Array({"request": request_, "message_recipient": user_email_, "privacy_policy_url": get_privacy_policy_url(), "sitename": wp_specialchars_decode(get_option("blogname"), ENT_QUOTES), "siteurl": home_url()})
    subject_ = php_sprintf(__("[%s] Erasure Request Fulfilled"), email_data_["sitename"])
    #// 
    #// Filters the subject of the email sent when an erasure request is completed.
    #// 
    #// @since 4.9.8
    #// 
    #// @param string $subject    The email subject.
    #// @param string $sitename   The name of the site.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request            User request object.
    #// @type string          $message_recipient  The address that the email will be sent to. Defaults
    #// to the value of `$request->email`, but can be changed
    #// by the `user_erasure_fulfillment_email_to` filter.
    #// @type string          $privacy_policy_url Privacy policy URL.
    #// @type string          $sitename           The site name sending the mail.
    #// @type string          $siteurl            The site URL sending the mail.
    #// }
    #//
    subject_ = apply_filters("user_erasure_complete_email_subject", subject_, email_data_["sitename"], email_data_)
    if php_empty(lambda : email_data_["privacy_policy_url"]):
        #// translators: Do not translate SITENAME, SITEURL; those are placeholders.
        email_text_ = __("""Howdy,
        Your request to erase your personal data on ###SITENAME### has been completed.
        If you have any follow-up questions or concerns, please contact the site administrator.
        Regards,
        All at ###SITENAME###
        ###SITEURL###""")
    else:
        #// translators: Do not translate SITENAME, SITEURL, PRIVACY_POLICY_URL; those are placeholders.
        email_text_ = __("""Howdy,
        Your request to erase your personal data on ###SITENAME### has been completed.
        If you have any follow-up questions or concerns, please contact the site administrator.
        For more information, you can also read our privacy policy: ###PRIVACY_POLICY_URL###
        Regards,
        All at ###SITENAME###
        ###SITEURL###""")
    # end if
    #// 
    #// Filters the body of the data erasure fulfillment notification.
    #// 
    #// The email is sent to a user when a their data erasure request is fulfilled
    #// by an administrator.
    #// 
    #// The following strings have a special meaning and will get replaced dynamically:
    #// 
    #// ###SITENAME###           The name of the site.
    #// ###PRIVACY_POLICY_URL### Privacy policy page URL.
    #// ###SITEURL###            The URL to the site.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $email_text Text in the email.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request            User request object.
    #// @type string          $message_recipient  The address that the email will be sent to. Defaults
    #// to the value of `$request->email`, but can be changed
    #// by the `user_erasure_fulfillment_email_to` filter.
    #// @type string          $privacy_policy_url Privacy policy URL.
    #// @type string          $sitename           The site name sending the mail.
    #// @type string          $siteurl            The site URL sending the mail.
    #// }
    #//
    content_ = apply_filters("user_confirmed_action_email_content", email_text_, email_data_)
    content_ = php_str_replace("###SITENAME###", email_data_["sitename"], content_)
    content_ = php_str_replace("###PRIVACY_POLICY_URL###", email_data_["privacy_policy_url"], content_)
    content_ = php_str_replace("###SITEURL###", esc_url_raw(email_data_["siteurl"]), content_)
    headers_ = ""
    #// 
    #// Filters the headers of the data erasure fulfillment notification.
    #// 
    #// @since 5.4.0
    #// 
    #// @param string|array $headers    The email headers.
    #// @param string       $subject    The email subject.
    #// @param string       $content    The email content.
    #// @param int          $request_id The request ID.
    #// @param array        $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request            User request object.
    #// @type string          $message_recipient  The address that the email will be sent to. Defaults
    #// to the value of `$request->email`, but can be changed
    #// by the `user_erasure_fulfillment_email_to` filter.
    #// @type string          $privacy_policy_url Privacy policy URL.
    #// @type string          $sitename           The site name sending the mail.
    #// @type string          $siteurl            The site URL sending the mail.
    #// }
    #//
    headers_ = apply_filters("user_erasure_complete_email_headers", headers_, subject_, content_, request_id_, email_data_)
    email_sent_ = wp_mail(user_email_, subject_, content_, headers_)
    if switched_locale_:
        restore_previous_locale()
    # end if
    if email_sent_:
        update_post_meta(request_id_, "_wp_user_notified", True)
    # end if
# end def _wp_privacy_send_erasure_fulfillment_notification
#// 
#// Return request confirmation message HTML.
#// 
#// @since 4.9.6
#// @access private
#// 
#// @param int $request_id The request ID being confirmed.
#// @return string $message The confirmation message.
#//
def _wp_privacy_account_request_confirmed_message(request_id_=None, *_args_):
    
    
    request_ = wp_get_user_request(request_id_)
    message_ = "<p class=\"success\">" + __("Action has been confirmed.") + "</p>"
    message_ += "<p>" + __("The site administrator has been notified and will fulfill your request as soon as possible.") + "</p>"
    if request_ and php_in_array(request_.action_name, _wp_privacy_action_request_types(), True):
        if "export_personal_data" == request_.action_name:
            message_ = "<p class=\"success\">" + __("Thanks for confirming your export request.") + "</p>"
            message_ += "<p>" + __("The site administrator has been notified. You will receive a link to download your export via email when they fulfill your request.") + "</p>"
        elif "remove_personal_data" == request_.action_name:
            message_ = "<p class=\"success\">" + __("Thanks for confirming your erasure request.") + "</p>"
            message_ += "<p>" + __("The site administrator has been notified. You will receive an email confirmation when they erase your data.") + "</p>"
        # end if
    # end if
    #// 
    #// Filters the message displayed to a user when they confirm a data request.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $message    The message to the user.
    #// @param int    $request_id The ID of the request being confirmed.
    #//
    message_ = apply_filters("user_request_action_confirmed_message", message_, request_id_)
    return message_
# end def _wp_privacy_account_request_confirmed_message
#// 
#// Create and log a user request to perform a specific action.
#// 
#// Requests are stored inside a post type named `user_request` since they can apply to both
#// users on the site, or guests without a user account.
#// 
#// @since 4.9.6
#// 
#// @param string $email_address User email address. This can be the address of a registered or non-registered user.
#// @param string $action_name   Name of the action that is being confirmed. Required.
#// @param array  $request_data  Misc data you want to send with the verification request and pass to the actions once the request is confirmed.
#// @return int|WP_Error Returns the request ID if successful, or a WP_Error object on failure.
#//
def wp_create_user_request(email_address_="", action_name_="", request_data_=None, *_args_):
    if request_data_ is None:
        request_data_ = Array()
    # end if
    
    email_address_ = sanitize_email(email_address_)
    action_name_ = sanitize_key(action_name_)
    if (not is_email(email_address_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_email", __("Invalid email address.")))
    # end if
    if (not action_name_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_action", __("Invalid action name.")))
    # end if
    user_ = get_user_by("email", email_address_)
    user_id_ = user_.ID if user_ and (not is_wp_error(user_)) else 0
    #// Check for duplicates.
    requests_query_ = php_new_class("WP_Query", lambda : WP_Query(Array({"post_type": "user_request", "post_name__in": Array(action_name_), "title": email_address_, "post_status": Array("request-pending", "request-confirmed"), "fields": "ids"})))
    if requests_query_.found_posts:
        return php_new_class("WP_Error", lambda : WP_Error("duplicate_request", __("An incomplete request for this email address already exists.")))
    # end if
    request_id_ = wp_insert_post(Array({"post_author": user_id_, "post_name": action_name_, "post_title": email_address_, "post_content": wp_json_encode(request_data_), "post_status": "request-pending", "post_type": "user_request", "post_date": current_time("mysql", False), "post_date_gmt": current_time("mysql", True)}), True)
    return request_id_
# end def wp_create_user_request
#// 
#// Get action description from the name and return a string.
#// 
#// @since 4.9.6
#// 
#// @param string $action_name Action name of the request.
#// @return string Human readable action name.
#//
def wp_user_request_action_description(action_name_=None, *_args_):
    
    
    for case in Switch(action_name_):
        if case("export_personal_data"):
            description_ = __("Export Personal Data")
            break
        # end if
        if case("remove_personal_data"):
            description_ = __("Erase Personal Data")
            break
        # end if
        if case():
            #// translators: %s: Action name.
            description_ = php_sprintf(__("Confirm the \"%s\" action"), action_name_)
            break
        # end if
    # end for
    #// 
    #// Filters the user action description.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $description The default description.
    #// @param string $action_name The name of the request.
    #//
    return apply_filters("user_request_action_description", description_, action_name_)
# end def wp_user_request_action_description
#// 
#// Send a confirmation request email to confirm an action.
#// 
#// If the request is not already pending, it will be updated.
#// 
#// @since 4.9.6
#// 
#// @param string $request_id ID of the request created via wp_create_user_request().
#// @return bool|WP_Error True on success, `WP_Error` on failure.
#//
def wp_send_user_request(request_id_=None, *_args_):
    
    
    request_id_ = absint(request_id_)
    request_ = wp_get_user_request(request_id_)
    if (not request_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_request", __("Invalid user request.")))
    # end if
    #// Localize message content for user; fallback to site default for visitors.
    if (not php_empty(lambda : request_.user_id)):
        locale_ = get_user_locale(request_.user_id)
    else:
        locale_ = get_locale()
    # end if
    switched_locale_ = switch_to_locale(locale_)
    email_data_ = Array({"request": request_, "email": request_.email, "description": wp_user_request_action_description(request_.action_name), "confirm_url": add_query_arg(Array({"action": "confirmaction", "request_id": request_id_, "confirm_key": wp_generate_user_request_key(request_id_)}), wp_login_url())}, {"sitename": wp_specialchars_decode(get_option("blogname"), ENT_QUOTES), "siteurl": home_url()})
    #// translators: Do not translate DESCRIPTION, CONFIRM_URL, SITENAME, SITEURL: those are placeholders.
    email_text_ = __("""Howdy,
    A request has been made to perform the following action on your account:
    ###DESCRIPTION###
    To confirm this, please click on the following link:
    ###CONFIRM_URL###
    You can safely ignore and delete this email if you do not want to
    take this action.
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    #// 
    #// Filters the text of the email sent when an account action is attempted.
    #// 
    #// The following strings have a special meaning and will get replaced dynamically:
    #// 
    #// ###DESCRIPTION### Description of the action being performed so the user knows what the email is for.
    #// ###CONFIRM_URL### The link to click on to confirm the account action.
    #// ###SITENAME###    The name of the site.
    #// ###SITEURL###     The URL to the site.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $email_text Text in the email.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request     User request object.
    #// @type string          $email       The email address this is being sent to.
    #// @type string          $description Description of the action being performed so the user knows what the email is for.
    #// @type string          $confirm_url The link to click on to confirm the account action.
    #// @type string          $sitename    The site name sending the mail.
    #// @type string          $siteurl     The site URL sending the mail.
    #// }
    #//
    content_ = apply_filters("user_request_action_email_content", email_text_, email_data_)
    content_ = php_str_replace("###DESCRIPTION###", email_data_["description"], content_)
    content_ = php_str_replace("###CONFIRM_URL###", esc_url_raw(email_data_["confirm_url"]), content_)
    content_ = php_str_replace("###EMAIL###", email_data_["email"], content_)
    content_ = php_str_replace("###SITENAME###", email_data_["sitename"], content_)
    content_ = php_str_replace("###SITEURL###", esc_url_raw(email_data_["siteurl"]), content_)
    #// translators: Confirm privacy data request notification email subject. 1: Site title, 2: Name of the action.
    subject_ = php_sprintf(__("[%1$s] Confirm Action: %2$s"), email_data_["sitename"], email_data_["description"])
    #// 
    #// Filters the subject of the email sent when an account action is attempted.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $subject    The email subject.
    #// @param string $sitename   The name of the site.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request     User request object.
    #// @type string          $email       The email address this is being sent to.
    #// @type string          $description Description of the action being performed so the user knows what the email is for.
    #// @type string          $confirm_url The link to click on to confirm the account action.
    #// @type string          $sitename    The site name sending the mail.
    #// @type string          $siteurl     The site URL sending the mail.
    #// }
    #//
    subject_ = apply_filters("user_request_action_email_subject", subject_, email_data_["sitename"], email_data_)
    headers_ = ""
    #// 
    #// Filters the headers of the email sent when an account action is attempted.
    #// 
    #// @since 5.4.0
    #// 
    #// @param string|array $headers    The email headers.
    #// @param string       $subject    The email subject.
    #// @param string       $content    The email content.
    #// @param int          $request_id The request ID.
    #// @param array        $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request     User request object.
    #// @type string          $email       The email address this is being sent to.
    #// @type string          $description Description of the action being performed so the user knows what the email is for.
    #// @type string          $confirm_url The link to click on to confirm the account action.
    #// @type string          $sitename    The site name sending the mail.
    #// @type string          $siteurl     The site URL sending the mail.
    #// }
    #//
    headers_ = apply_filters("user_request_action_email_headers", headers_, subject_, content_, request_id_, email_data_)
    email_sent_ = wp_mail(email_data_["email"], subject_, content_, headers_)
    if switched_locale_:
        restore_previous_locale()
    # end if
    if (not email_sent_):
        return php_new_class("WP_Error", lambda : WP_Error("privacy_email_error", __("Unable to send personal data export confirmation email.")))
    # end if
    return True
# end def wp_send_user_request
#// 
#// Returns a confirmation key for a user action and stores the hashed version for future comparison.
#// 
#// @since 4.9.6
#// 
#// @param int $request_id Request ID.
#// @return string Confirmation key.
#//
def wp_generate_user_request_key(request_id_=None, *_args_):
    
    
    global wp_hasher_
    php_check_if_defined("wp_hasher_")
    #// Generate something random for a confirmation key.
    key_ = wp_generate_password(20, False)
    #// Return the key, hashed.
    if php_empty(lambda : wp_hasher_):
        php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
        wp_hasher_ = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
    # end if
    wp_update_post(Array({"ID": request_id_, "post_status": "request-pending", "post_password": wp_hasher_.hashpassword(key_)}))
    return key_
# end def wp_generate_user_request_key
#// 
#// Validate a user request by comparing the key with the request's key.
#// 
#// @since 4.9.6
#// 
#// @param string $request_id ID of the request being confirmed.
#// @param string $key        Provided key to validate.
#// @return bool|WP_Error True on success, WP_Error on failure.
#//
def wp_validate_user_request_key(request_id_=None, key_=None, *_args_):
    
    
    global wp_hasher_
    php_check_if_defined("wp_hasher_")
    request_id_ = absint(request_id_)
    request_ = wp_get_user_request(request_id_)
    if (not request_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_request", __("Invalid request.")))
    # end if
    if (not php_in_array(request_.status, Array("request-pending", "request-failed"), True)):
        return php_new_class("WP_Error", lambda : WP_Error("expired_link", __("This link has expired.")))
    # end if
    if php_empty(lambda : key_):
        return php_new_class("WP_Error", lambda : WP_Error("missing_key", __("Missing confirm key.")))
    # end if
    if php_empty(lambda : wp_hasher_):
        php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
        wp_hasher_ = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
    # end if
    key_request_time_ = request_.modified_timestamp
    saved_key_ = request_.confirm_key
    if (not saved_key_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid key.")))
    # end if
    if (not key_request_time_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid action.")))
    # end if
    #// 
    #// Filters the expiration time of confirm keys.
    #// 
    #// @since 4.9.6
    #// 
    #// @param int $expiration The expiration time in seconds.
    #//
    expiration_duration_ = php_int(apply_filters("user_request_key_expiration", DAY_IN_SECONDS))
    expiration_time_ = key_request_time_ + expiration_duration_
    if (not wp_hasher_.checkpassword(key_, saved_key_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_key", __("Invalid key.")))
    # end if
    if (not expiration_time_) or time() > expiration_time_:
        return php_new_class("WP_Error", lambda : WP_Error("expired_key", __("The confirmation email has expired.")))
    # end if
    return True
# end def wp_validate_user_request_key
#// 
#// Return the user request object for the specified request ID.
#// 
#// @since 4.9.6
#// 
#// @param int $request_id The ID of the user request.
#// @return WP_User_Request|false
#//
def wp_get_user_request(request_id_=None, *_args_):
    
    
    request_id_ = absint(request_id_)
    post_ = get_post(request_id_)
    if (not post_) or "user_request" != post_.post_type:
        return False
    # end if
    return php_new_class("WP_User_Request", lambda : WP_User_Request(post_))
# end def wp_get_user_request
