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
#// WP_User_Request class.
#// 
#// Represents user request data loaded from a WP_Post object.
#// 
#// @since 4.9.6
#//
class WP_User_Request():
    #// 
    #// Request ID.
    #// 
    #// @var int
    #//
    ID = 0
    #// 
    #// User ID.
    #// 
    #// @var int
    #//
    user_id = 0
    #// 
    #// User email.
    #// 
    #// @var int
    #//
    email = ""
    #// 
    #// Action name.
    #// 
    #// @var string
    #//
    action_name = ""
    #// 
    #// Current status.
    #// 
    #// @var string
    #//
    status = ""
    #// 
    #// Timestamp this request was created.
    #// 
    #// @var int|null
    #//
    created_timestamp = None
    #// 
    #// Timestamp this request was last modified.
    #// 
    #// @var int|null
    #//
    modified_timestamp = None
    #// 
    #// Timestamp this request was confirmed.
    #// 
    #// @var int
    #//
    confirmed_timestamp = None
    #// 
    #// Timestamp this request was completed.
    #// 
    #// @var int
    #//
    completed_timestamp = None
    #// 
    #// Misc data assigned to this request.
    #// 
    #// @var array
    #//
    request_data = Array()
    #// 
    #// Key used to confirm this request.
    #// 
    #// @var string
    #//
    confirm_key = ""
    #// 
    #// Constructor.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_Post|object $post Post object.
    #//
    def __init__(self, post_=None):
        
        
        self.ID = post_.ID
        self.user_id = post_.post_author
        self.email = post_.post_title
        self.action_name = post_.post_name
        self.status = post_.post_status
        self.created_timestamp = strtotime(post_.post_date_gmt)
        self.modified_timestamp = strtotime(post_.post_modified_gmt)
        self.confirmed_timestamp = php_int(get_post_meta(post_.ID, "_wp_user_request_confirmed_timestamp", True))
        self.completed_timestamp = php_int(get_post_meta(post_.ID, "_wp_user_request_completed_timestamp", True))
        self.request_data = php_json_decode(post_.post_content, True)
        self.confirm_key = post_.post_password
    # end def __init__
# end class WP_User_Request
