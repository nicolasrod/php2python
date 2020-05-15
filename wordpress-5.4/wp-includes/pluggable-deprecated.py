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
#// Deprecated pluggable functions from past WordPress versions. You shouldn't use these
#// functions and look for the alternatives instead. The functions will be removed in a
#// later version.
#// 
#// Deprecated warnings are also thrown if one of these functions is being defined by a plugin.
#// 
#// @package WordPress
#// @subpackage Deprecated
#// @see pluggable.php
#// 
#// 
#// Deprecated functions come here to die.
#//
if (not php_function_exists("set_current_user")):
    #// 
    #// Changes the current user by ID or name.
    #// 
    #// Set $id to null and specify a name if you do not know a user's ID.
    #// 
    #// @since 2.0.1
    #// @deprecated 3.0.0 Use wp_set_current_user()
    #// @see wp_set_current_user()
    #// 
    #// @param int|null $id User ID.
    #// @param string $name Optional. The user's username
    #// @return WP_User returns wp_set_current_user()
    #//
    def set_current_user(id=None, name="", *args_):
        
        _deprecated_function(__FUNCTION__, "3.0.0", "wp_set_current_user()")
        return wp_set_current_user(id, name)
    # end def set_current_user
# end if
if (not php_function_exists("get_currentuserinfo")):
    #// 
    #// Populate global variables with information about the currently logged in user.
    #// 
    #// @since 0.71
    #// @deprecated 4.5.0 Use wp_get_current_user()
    #// @see wp_get_current_user()
    #// 
    #// @return bool|WP_User False on XMLRPC Request and invalid auth cookie, WP_User instance otherwise.
    #//
    def get_currentuserinfo(*args_):
        
        _deprecated_function(__FUNCTION__, "4.5.0", "wp_get_current_user()")
        return _wp_get_current_user()
    # end def get_currentuserinfo
# end if
if (not php_function_exists("get_userdatabylogin")):
    #// 
    #// Retrieve user info by login name.
    #// 
    #// @since 0.71
    #// @deprecated 3.3.0 Use get_user_by()
    #// @see get_user_by()
    #// 
    #// @param string $user_login User's username
    #// @return bool|object False on failure, User DB row object
    #//
    def get_userdatabylogin(user_login=None, *args_):
        
        _deprecated_function(__FUNCTION__, "3.3.0", "get_user_by('login')")
        return get_user_by("login", user_login)
    # end def get_userdatabylogin
# end if
if (not php_function_exists("get_user_by_email")):
    #// 
    #// Retrieve user info by email.
    #// 
    #// @since 2.5.0
    #// @deprecated 3.3.0 Use get_user_by()
    #// @see get_user_by()
    #// 
    #// @param string $email User's email address
    #// @return bool|object False on failure, User DB row object
    #//
    def get_user_by_email(email=None, *args_):
        
        _deprecated_function(__FUNCTION__, "3.3.0", "get_user_by('email')")
        return get_user_by("email", email)
    # end def get_user_by_email
# end if
if (not php_function_exists("wp_setcookie")):
    #// 
    #// Sets a cookie for a user who just logged in. This function is deprecated.
    #// 
    #// @since 1.5.0
    #// @deprecated 2.5.0 Use wp_set_auth_cookie()
    #// @see wp_set_auth_cookie()
    #// 
    #// @param string $username The user's username
    #// @param string $password Optional. The user's password
    #// @param bool $already_md5 Optional. Whether the password has already been through MD5
    #// @param string $home Optional. Will be used instead of COOKIEPATH if set
    #// @param string $siteurl Optional. Will be used instead of SITECOOKIEPATH if set
    #// @param bool $remember Optional. Remember that the user is logged in
    #//
    def wp_setcookie(username=None, password="", already_md5=False, home="", siteurl="", remember=False, *args_):
        
        _deprecated_function(__FUNCTION__, "2.5.0", "wp_set_auth_cookie()")
        user = get_user_by("login", username)
        wp_set_auth_cookie(user.ID, remember)
    # end def wp_setcookie
else:
    _deprecated_function("wp_setcookie", "2.5.0", "wp_set_auth_cookie()")
# end if
if (not php_function_exists("wp_clearcookie")):
    #// 
    #// Clears the authentication cookie, logging the user out. This function is deprecated.
    #// 
    #// @since 1.5.0
    #// @deprecated 2.5.0 Use wp_clear_auth_cookie()
    #// @see wp_clear_auth_cookie()
    #//
    def wp_clearcookie(*args_):
        
        _deprecated_function(__FUNCTION__, "2.5.0", "wp_clear_auth_cookie()")
        wp_clear_auth_cookie()
    # end def wp_clearcookie
else:
    _deprecated_function("wp_clearcookie", "2.5.0", "wp_clear_auth_cookie()")
# end if
if (not php_function_exists("wp_get_cookie_login")):
    #// 
    #// Gets the user cookie login. This function is deprecated.
    #// 
    #// This function is deprecated and should no longer be extended as it won't be
    #// used anywhere in WordPress. Also, plugins shouldn't use it either.
    #// 
    #// @since 2.0.3
    #// @deprecated 2.5.0
    #// 
    #// @return bool Always returns false
    #//
    def wp_get_cookie_login(*args_):
        
        _deprecated_function(__FUNCTION__, "2.5.0")
        return False
    # end def wp_get_cookie_login
else:
    _deprecated_function("wp_get_cookie_login", "2.5.0")
# end if
if (not php_function_exists("wp_login")):
    #// 
    #// Checks a users login information and logs them in if it checks out. This function is deprecated.
    #// 
    #// Use the global $error to get the reason why the login failed. If the username
    #// is blank, no error will be set, so assume blank username on that case.
    #// 
    #// Plugins extending this function should also provide the global $error and set
    #// what the error is, so that those checking the global for why there was a
    #// failure can utilize it later.
    #// 
    #// @since 1.2.2
    #// @deprecated 2.5.0 Use wp_signon()
    #// @see wp_signon()
    #// 
    #// @global string $error Error when false is returned
    #// 
    #// @param string $username   User's username
    #// @param string $password   User's password
    #// @param string $deprecated Not used
    #// @return bool True on successful check, false on login failure.
    #//
    def wp_login(username=None, password=None, deprecated="", *args_):
        
        _deprecated_function(__FUNCTION__, "2.5.0", "wp_signon()")
        global error
        php_check_if_defined("error")
        user = wp_authenticate(username, password)
        if (not is_wp_error(user)):
            return True
        # end if
        error = user.get_error_message()
        return False
    # end def wp_login
else:
    _deprecated_function("wp_login", "2.5.0", "wp_signon()")
# end if
#// 
#// WordPress AtomPub API implementation.
#// 
#// Originally stored in wp-app.php, and later wp-includes/class-wp-atom-server.php.
#// It is kept here in case a plugin directly referred to the class.
#// 
#// @since 2.2.0
#// @deprecated 3.5.0
#// 
#// @link https://wordpress.org/plugins/atom-publishing-protocol
#//
if (not php_class_exists("wp_atom_server", False)):
    class wp_atom_server():
        def __call(self, name=None, arguments=None):
            
            _deprecated_function(__CLASS__ + "::" + name, "3.5.0", "the Atom Publishing Protocol plugin")
        # end def __call
        @classmethod
        def __callstatic(self, name=None, arguments=None):
            
            _deprecated_function(__CLASS__ + "::" + name, "3.5.0", "the Atom Publishing Protocol plugin")
        # end def __callstatic
    # end class wp_atom_server
# end if
