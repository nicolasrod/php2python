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
#// Session API: WP_Session_Tokens class
#// 
#// @package WordPress
#// @subpackage Session
#// @since 4.7.0
#// 
#// 
#// Abstract class for managing user session tokens.
#// 
#// @since 4.0.0
#//
class WP_Session_Tokens():
    #// 
    #// User ID.
    #// 
    #// @since 4.0.0
    #// @var int User ID.
    #//
    user_id = Array()
    #// 
    #// Protected constructor. Use the `get_instance()` method to get the instance.
    #// 
    #// @since 4.0.0
    #// 
    #// @param int $user_id User whose session to manage.
    #//
    def __init__(self, user_id_=None):
        
        
        self.user_id = user_id_
    # end def __init__
    #// 
    #// Retrieves a session manager instance for a user.
    #// 
    #// This method contains a {@see 'session_token_manager'} filter, allowing a plugin to swap out
    #// the session manager for a subclass of `WP_Session_Tokens`.
    #// 
    #// @since 4.0.0
    #// 
    #// @param int $user_id User whose session to manage.
    #// @return WP_Session_Tokens The session object, which is by default an instance of
    #// the `WP_User_Meta_Session_Tokens` class.
    #//
    def get_instance(self, user_id_=None):
        
        
        #// 
        #// Filters the class name for the session token manager.
        #// 
        #// @since 4.0.0
        #// 
        #// @param string $session Name of class to use as the manager.
        #// Default 'WP_User_Meta_Session_Tokens'.
        #//
        manager_ = apply_filters("session_token_manager", "WP_User_Meta_Session_Tokens")
        return php_new_class(manager_, lambda : {**locals(), **globals()}[manager_](user_id_))
    # end def get_instance
    #// 
    #// Hashes the given session token for storage.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $token Session token to hash.
    #// @return string A hash of the session token (a verifier).
    #//
    def hash_token(self, token_=None):
        
        
        #// If ext/hash is not present, use sha1() instead.
        if php_function_exists("hash"):
            return hash("sha256", token_)
        else:
            return sha1(token_)
        # end if
    # end def hash_token
    #// 
    #// Retrieves a user's session for the given token.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $token Session token.
    #// @return array|null The session, or null if it does not exist.
    #//
    def get(self, token_=None):
        
        
        verifier_ = self.hash_token(token_)
        return self.get_session(verifier_)
    # end def get
    #// 
    #// Validates the given session token for authenticity and validity.
    #// 
    #// Checks that the given token is present and hasn't expired.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $token Token to verify.
    #// @return bool Whether the token is valid for the user.
    #//
    def verify(self, token_=None):
        
        
        verifier_ = self.hash_token(token_)
        return php_bool(self.get_session(verifier_))
    # end def verify
    #// 
    #// Generates a session token and attaches session information to it.
    #// 
    #// A session token is a long, random string. It is used in a cookie
    #// to link that cookie to an expiration time and to ensure the cookie
    #// becomes invalidated when the user logs out.
    #// 
    #// This function generates a token and stores it with the associated
    #// expiration time (and potentially other session information via the
    #// {@see 'attach_session_information'} filter).
    #// 
    #// @since 4.0.0
    #// 
    #// @param int $expiration Session expiration timestamp.
    #// @return string Session token.
    #//
    def create(self, expiration_=None):
        
        
        #// 
        #// Filters the information attached to the newly created session.
        #// 
        #// Can be used to attach further information to a session.
        #// 
        #// @since 4.0.0
        #// 
        #// @param array $session Array of extra data.
        #// @param int   $user_id User ID.
        #//
        session_ = apply_filters("attach_session_information", Array(), self.user_id)
        session_["expiration"] = expiration_
        #// IP address.
        if (not php_empty(lambda : PHP_SERVER["REMOTE_ADDR"])):
            session_["ip"] = PHP_SERVER["REMOTE_ADDR"]
        # end if
        #// User-agent.
        if (not php_empty(lambda : PHP_SERVER["HTTP_USER_AGENT"])):
            session_["ua"] = wp_unslash(PHP_SERVER["HTTP_USER_AGENT"])
        # end if
        #// Timestamp.
        session_["login"] = time()
        token_ = wp_generate_password(43, False, False)
        self.update(token_, session_)
        return token_
    # end def create
    #// 
    #// Updates the data for the session with the given token.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $token Session token to update.
    #// @param array  $session Session information.
    #//
    def update(self, token_=None, session_=None):
        
        
        verifier_ = self.hash_token(token_)
        self.update_session(verifier_, session_)
    # end def update
    #// 
    #// Destroys the session with the given token.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $token Session token to destroy.
    #//
    def destroy(self, token_=None):
        
        
        verifier_ = self.hash_token(token_)
        self.update_session(verifier_, None)
    # end def destroy
    #// 
    #// Destroys all sessions for this user except the one with the given token (presumably the one in use).
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $token_to_keep Session token to keep.
    #//
    def destroy_others(self, token_to_keep_=None):
        
        
        verifier_ = self.hash_token(token_to_keep_)
        session_ = self.get_session(verifier_)
        if session_:
            self.destroy_other_sessions(verifier_)
        else:
            self.destroy_all_sessions()
        # end if
    # end def destroy_others
    #// 
    #// Determines whether a session is still valid, based on its expiration timestamp.
    #// 
    #// @since 4.0.0
    #// 
    #// @param array $session Session to check.
    #// @return bool Whether session is valid.
    #//
    def is_still_valid(self, session_=None):
        
        
        return session_["expiration"] >= time()
    # end def is_still_valid
    #// 
    #// Destroys all sessions for a user.
    #// 
    #// @since 4.0.0
    #//
    def destroy_all(self):
        
        
        self.destroy_all_sessions()
    # end def destroy_all
    #// 
    #// Destroys all sessions for all users.
    #// 
    #// @since 4.0.0
    #//
    def destroy_all_for_all_users(self):
        
        
        #// This filter is documented in wp-includes/class-wp-session-tokens.php
        manager_ = apply_filters("session_token_manager", "WP_User_Meta_Session_Tokens")
        php_call_user_func(Array(manager_, "drop_sessions"))
    # end def destroy_all_for_all_users
    #// 
    #// Retrieves all sessions for a user.
    #// 
    #// @since 4.0.0
    #// 
    #// @return array Sessions for a user.
    #//
    def get_all(self):
        
        
        return php_array_values(self.get_sessions())
    # end def get_all
    #// 
    #// Retrieves all sessions of the user.
    #// 
    #// @since 4.0.0
    #// 
    #// @return array Sessions of the user.
    #//
    def get_sessions(self):
        
        
        pass
    # end def get_sessions
    #// 
    #// Retrieves a session based on its verifier (token hash).
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $verifier Verifier for the session to retrieve.
    #// @return array|null The session, or null if it does not exist.
    #//
    def get_session(self, verifier_=None):
        
        
        pass
    # end def get_session
    #// 
    #// Updates a session based on its verifier (token hash).
    #// 
    #// Omitting the second argument destroys the session.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $verifier Verifier for the session to update.
    #// @param array  $session  Optional. Session. Omitting this argument destroys the session.
    #//
    def update_session(self, verifier_=None, session_=None):
        if session_ is None:
            session_ = None
        # end if
        
        pass
    # end def update_session
    #// 
    #// Destroys all sessions for this user, except the single session with the given verifier.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $verifier Verifier of the session to keep.
    #//
    def destroy_other_sessions(self, verifier_=None):
        
        
        pass
    # end def destroy_other_sessions
    #// 
    #// Destroys all sessions for the user.
    #// 
    #// @since 4.0.0
    #//
    def destroy_all_sessions(self):
        
        
        pass
    # end def destroy_all_sessions
    #// 
    #// Destroys all sessions for all users.
    #// 
    #// @since 4.0.0
    #//
    @classmethod
    def drop_sessions(self):
        
        
        pass
    # end def drop_sessions
# end class WP_Session_Tokens
