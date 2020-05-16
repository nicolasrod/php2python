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
#// WP_User_Request class.
#// 
#// Represents user request data loaded from a WP_Post object.
#// 
#// @since 4.9.6
#//
class WP_User_Request():
    ID = 0
    user_id = 0
    email = ""
    action_name = ""
    status = ""
    created_timestamp = None
    modified_timestamp = None
    confirmed_timestamp = None
    completed_timestamp = None
    request_data = Array()
    confirm_key = ""
    #// 
    #// Constructor.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_Post|object $post Post object.
    #//
    def __init__(self, post=None):
        
        self.ID = post.ID
        self.user_id = post.post_author
        self.email = post.post_title
        self.action_name = post.post_name
        self.status = post.post_status
        self.created_timestamp = strtotime(post.post_date_gmt)
        self.modified_timestamp = strtotime(post.post_modified_gmt)
        self.confirmed_timestamp = php_int(get_post_meta(post.ID, "_wp_user_request_confirmed_timestamp", True))
        self.completed_timestamp = php_int(get_post_meta(post.ID, "_wp_user_request_completed_timestamp", True))
        self.request_data = php_json_decode(post.post_content, True)
        self.confirm_key = post.post_password
    # end def __init__
# end class WP_User_Request
