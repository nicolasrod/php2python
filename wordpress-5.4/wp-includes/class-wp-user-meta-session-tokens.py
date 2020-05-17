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
#// Session API: WP_User_Meta_Session_Tokens class
#// 
#// @package WordPress
#// @subpackage Session
#// @since 4.7.0
#// 
#// 
#// Meta-based user sessions token manager.
#// 
#// @since 4.0.0
#// 
#// @see WP_Session_Tokens
#//
class WP_User_Meta_Session_Tokens(WP_Session_Tokens):
    #// 
    #// Retrieves all sessions of the user.
    #// 
    #// @since 4.0.0
    #// 
    #// @return array Sessions of the user.
    #//
    def get_sessions(self):
        
        
        sessions_ = get_user_meta(self.user_id, "session_tokens", True)
        if (not php_is_array(sessions_)):
            return Array()
        # end if
        sessions_ = php_array_map(Array(self, "prepare_session"), sessions_)
        return php_array_filter(sessions_, Array(self, "is_still_valid"))
    # end def get_sessions
    #// 
    #// Converts an expiration to an array of session information.
    #// 
    #// @param mixed $session Session or expiration.
    #// @return array Session.
    #//
    def prepare_session(self, session_=None):
        
        
        if php_is_int(session_):
            return Array({"expiration": session_})
        # end if
        return session_
    # end def prepare_session
    #// 
    #// Retrieves a session based on its verifier (token hash).
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $verifier Verifier for the session to retrieve.
    #// @return array|null The session, or null if it does not exist
    #//
    def get_session(self, verifier_=None):
        
        
        sessions_ = self.get_sessions()
        if (php_isset(lambda : sessions_[verifier_])):
            return sessions_[verifier_]
        # end if
        return None
    # end def get_session
    #// 
    #// Updates a session based on its verifier (token hash).
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $verifier Verifier for the session to update.
    #// @param array  $session  Optional. Session. Omitting this argument destroys the session.
    #//
    def update_session(self, verifier_=None, session_=None):
        
        
        sessions_ = self.get_sessions()
        if session_:
            sessions_[verifier_] = session_
        else:
            sessions_[verifier_] = None
        # end if
        self.update_sessions(sessions_)
    # end def update_session
    #// 
    #// Updates the user's sessions in the usermeta table.
    #// 
    #// @since 4.0.0
    #// 
    #// @param array $sessions Sessions.
    #//
    def update_sessions(self, sessions_=None):
        
        
        if sessions_:
            update_user_meta(self.user_id, "session_tokens", sessions_)
        else:
            delete_user_meta(self.user_id, "session_tokens")
        # end if
    # end def update_sessions
    #// 
    #// Destroys all sessions for this user, except the single session with the given verifier.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $verifier Verifier of the session to keep.
    #//
    def destroy_other_sessions(self, verifier_=None):
        
        
        session_ = self.get_session(verifier_)
        self.update_sessions(Array({verifier_: session_}))
    # end def destroy_other_sessions
    #// 
    #// Destroys all session tokens for the user.
    #// 
    #// @since 4.0.0
    #//
    def destroy_all_sessions(self):
        
        
        self.update_sessions(Array())
    # end def destroy_all_sessions
    #// 
    #// Destroys all sessions for all users.
    #// 
    #// @since 4.0.0
    #//
    @classmethod
    def drop_sessions(self):
        
        
        delete_metadata("user", 0, "session_tokens", False, True)
    # end def drop_sessions
# end class WP_User_Meta_Session_Tokens
