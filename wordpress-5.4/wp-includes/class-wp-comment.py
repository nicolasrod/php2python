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
#// Comment API: WP_Comment class
#// 
#// @package WordPress
#// @subpackage Comments
#// @since 4.4.0
#// 
#// 
#// Core class used to organize comments as instantiated objects with defined members.
#// 
#// @since 4.4.0
#//
class WP_Comment():
    #// 
    #// Comment ID.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    comment_ID = Array()
    #// 
    #// ID of the post the comment is associated with.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    comment_post_ID = 0
    #// 
    #// Comment author name.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_author = ""
    #// 
    #// Comment author email address.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_author_email = ""
    #// 
    #// Comment author URL.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_author_url = ""
    #// 
    #// Comment author IP address (IPv4 format).
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_author_IP = ""
    #// 
    #// Comment date in YYYY-MM-DD HH:MM:SS format.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_date = "0000-00-00 00:00:00"
    #// 
    #// Comment GMT date in YYYY-MM-DD HH::MM:SS format.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_date_gmt = "0000-00-00 00:00:00"
    #// 
    #// Comment content.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_content = Array()
    #// 
    #// Comment karma count.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    comment_karma = 0
    #// 
    #// Comment approval status.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_approved = "1"
    #// 
    #// Comment author HTTP user agent.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_agent = ""
    #// 
    #// Comment type.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    comment_type = ""
    #// 
    #// Parent comment ID.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    comment_parent = 0
    #// 
    #// Comment author ID.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    user_id = 0
    #// 
    #// Comment children.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    children = Array()
    #// 
    #// Whether children have been populated for this comment object.
    #// 
    #// @since 4.4.0
    #// @var bool
    #//
    populated_children = False
    #// 
    #// Post fields.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    post_fields = Array("post_author", "post_date", "post_date_gmt", "post_content", "post_title", "post_excerpt", "post_status", "comment_status", "ping_status", "post_name", "to_ping", "pinged", "post_modified", "post_modified_gmt", "post_content_filtered", "post_parent", "guid", "menu_order", "post_type", "post_mime_type", "comment_count")
    #// 
    #// Retrieves a WP_Comment instance.
    #// 
    #// @since 4.4.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $id Comment ID.
    #// @return WP_Comment|false Comment object, otherwise false.
    #//
    @classmethod
    def get_instance(self, id_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        comment_id_ = php_int(id_)
        if (not comment_id_):
            return False
        # end if
        _comment_ = wp_cache_get(comment_id_, "comment")
        if (not _comment_):
            _comment_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_ID = %d LIMIT 1"), comment_id_))
            if (not _comment_):
                return False
            # end if
            wp_cache_add(_comment_.comment_ID, _comment_, "comment")
        # end if
        return php_new_class("WP_Comment", lambda : WP_Comment(_comment_))
    # end def get_instance
    #// 
    #// Constructor.
    #// 
    #// Populates properties with object vars.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Comment $comment Comment object.
    #//
    def __init__(self, comment_=None):
        
        
        for key_,value_ in get_object_vars(comment_):
            self.key_ = value_
        # end for
    # end def __init__
    #// 
    #// Convert object to array.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Object as array.
    #//
    def to_array(self):
        
        
        return get_object_vars(self)
    # end def to_array
    #// 
    #// Get the children of a comment.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $args {
    #// Array of arguments used to pass to get_comments() and determine format.
    #// 
    #// @type string $format        Return value format. 'tree' for a hierarchical tree, 'flat' for a flattened array.
    #// Default 'tree'.
    #// @type string $status        Comment status to limit results by. Accepts 'hold' (`comment_status=0`),
    #// 'approve' (`comment_status=1`), 'all', or a custom comment status.
    #// Default 'all'.
    #// @type string $hierarchical  Whether to include comment descendants in the results.
    #// 'threaded' returns a tree, with each comment's children
    #// stored in a `children` property on the `WP_Comment` object.
    #// 'flat' returns a flat array of found comments plus their children.
    #// Pass `false` to leave out descendants.
    #// The parameter is ignored (forced to `false`) when `$fields` is 'ids' or 'counts'.
    #// Accepts 'threaded', 'flat', or false. Default: 'threaded'.
    #// @type string|array $orderby Comment status or array of statuses. To use 'meta_value'
    #// or 'meta_value_num', `$meta_key` must also be defined.
    #// To sort by a specific `$meta_query` clause, use that
    #// clause's array key. Accepts 'comment_agent',
    #// 'comment_approved', 'comment_author',
    #// 'comment_author_email', 'comment_author_IP',
    #// 'comment_author_url', 'comment_content', 'comment_date',
    #// 'comment_date_gmt', 'comment_ID', 'comment_karma',
    #// 'comment_parent', 'comment_post_ID', 'comment_type',
    #// 'user_id', 'comment__in', 'meta_value', 'meta_value_num',
    #// the value of $meta_key, and the array keys of
    #// `$meta_query`. Also accepts false, an empty array, or
    #// 'none' to disable `ORDER BY` clause.
    #// }
    #// @return WP_Comment[] Array of `WP_Comment` objects.
    #//
    def get_children(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"format": "tree", "status": "all", "hierarchical": "threaded", "orderby": ""})
        _args_ = wp_parse_args(args_, defaults_)
        _args_["parent"] = self.comment_ID
        if php_is_null(self.children):
            if self.populated_children:
                self.children = Array()
            else:
                self.children = get_comments(_args_)
            # end if
        # end if
        if "flat" == _args_["format"]:
            children_ = Array()
            for child_ in self.children:
                child_args_ = _args_
                child_args_["format"] = "flat"
                child_args_["parent"] = None
                children_ = php_array_merge(children_, Array(child_), child_.get_children(child_args_))
            # end for
        else:
            children_ = self.children
        # end if
        return children_
    # end def get_children
    #// 
    #// Add a child to the comment.
    #// 
    #// Used by `WP_Comment_Query` when bulk-filling descendants.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Comment $child Child comment.
    #//
    def add_child(self, child_=None):
        
        
        self.children[child_.comment_ID] = child_
    # end def add_child
    #// 
    #// Get a child comment by ID.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int $child_id ID of the child.
    #// @return WP_Comment|bool Returns the comment object if found, otherwise false.
    #//
    def get_child(self, child_id_=None):
        
        
        if (php_isset(lambda : self.children[child_id_])):
            return self.children[child_id_]
        # end if
        return False
    # end def get_child
    #// 
    #// Set the 'populated_children' flag.
    #// 
    #// This flag is important for ensuring that calling `get_children()` on a childless comment will not trigger
    #// unneeded database queries.
    #// 
    #// @since 4.4.0
    #// 
    #// @param bool $set Whether the comment's children have already been populated.
    #//
    def populated_children(self, set_=None):
        
        
        self.populated_children = php_bool(set_)
    # end def populated_children
    #// 
    #// Check whether a non-public property is set.
    #// 
    #// If `$name` matches a post field, the comment post will be loaded and the post's value checked.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $name Property name.
    #// @return bool
    #//
    def __isset(self, name_=None):
        
        
        if php_in_array(name_, self.post_fields) and 0 != php_int(self.comment_post_ID):
            post_ = get_post(self.comment_post_ID)
            return property_exists(post_, name_)
        # end if
    # end def __isset
    #// 
    #// Magic getter.
    #// 
    #// If `$name` matches a post field, the comment post will be loaded and the post's value returned.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $name
    #// @return mixed
    #//
    def __get(self, name_=None):
        
        
        if php_in_array(name_, self.post_fields):
            post_ = get_post(self.comment_post_ID)
            return post_.name_
        # end if
    # end def __get
# end class WP_Comment
