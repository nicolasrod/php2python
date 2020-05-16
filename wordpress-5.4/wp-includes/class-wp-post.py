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
#// Post API: WP_Post class
#// 
#// @package WordPress
#// @subpackage Post
#// @since 4.4.0
#// 
#// 
#// Core class used to implement the WP_Post object.
#// 
#// @since 3.5.0
#// 
#// @property string $page_template
#// 
#// @property-read array  $ancestors
#// @property-read int    $post_category
#// @property-read string $tag_input
#//
class WP_Post():
    ID = Array()
    post_author = 0
    post_date = "0000-00-00 00:00:00"
    post_date_gmt = "0000-00-00 00:00:00"
    post_content = ""
    post_title = ""
    post_excerpt = ""
    post_status = "publish"
    comment_status = "open"
    ping_status = "open"
    post_password = ""
    post_name = ""
    to_ping = ""
    pinged = ""
    post_modified = "0000-00-00 00:00:00"
    post_modified_gmt = "0000-00-00 00:00:00"
    post_content_filtered = ""
    post_parent = 0
    guid = ""
    menu_order = 0
    post_type = "post"
    post_mime_type = ""
    comment_count = 0
    filter = Array()
    #// 
    #// Retrieve WP_Post instance.
    #// 
    #// @since 3.5.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $post_id Post ID.
    #// @return WP_Post|false Post object, false otherwise.
    #//
    @classmethod
    def get_instance(self, post_id=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        post_id = php_int(post_id)
        if (not post_id):
            return False
        # end if
        _post = wp_cache_get(post_id, "posts")
        if (not _post):
            _post = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.posts) + str(" WHERE ID = %d LIMIT 1"), post_id))
            if (not _post):
                return False
            # end if
            _post = sanitize_post(_post, "raw")
            wp_cache_add(_post.ID, _post, "posts")
        elif php_empty(lambda : _post.filter):
            _post = sanitize_post(_post, "raw")
        # end if
        return php_new_class("WP_Post", lambda : WP_Post(_post))
    # end def get_instance
    #// 
    #// Constructor.
    #// 
    #// @since 3.5.0
    #// 
    #// @param WP_Post|object $post Post object.
    #//
    def __init__(self, post=None):
        
        for key,value in get_object_vars(post):
            self.key = value
        # end for
    # end def __init__
    #// 
    #// Isset-er.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $key Property to check if set.
    #// @return bool
    #//
    def __isset(self, key=None):
        
        if "ancestors" == key:
            return True
        # end if
        if "page_template" == key:
            return True
        # end if
        if "post_category" == key:
            return True
        # end if
        if "tags_input" == key:
            return True
        # end if
        return metadata_exists("post", self.ID, key)
    # end def __isset
    #// 
    #// Getter.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $key Key to get.
    #// @return mixed
    #//
    def __get(self, key=None):
        
        if "page_template" == key and self.__isset(key):
            return get_post_meta(self.ID, "_wp_page_template", True)
        # end if
        if "post_category" == key:
            if is_object_in_taxonomy(self.post_type, "category"):
                terms = get_the_terms(self, "category")
            # end if
            if php_empty(lambda : terms):
                return Array()
            # end if
            return wp_list_pluck(terms, "term_id")
        # end if
        if "tags_input" == key:
            if is_object_in_taxonomy(self.post_type, "post_tag"):
                terms = get_the_terms(self, "post_tag")
            # end if
            if php_empty(lambda : terms):
                return Array()
            # end if
            return wp_list_pluck(terms, "name")
        # end if
        #// Rest of the values need filtering.
        if "ancestors" == key:
            value = get_post_ancestors(self)
        else:
            value = get_post_meta(self.ID, key, True)
        # end if
        if self.filter:
            value = sanitize_post_field(key, value, self.ID, self.filter)
        # end if
        return value
    # end def __get
    #// 
    #// {@Missing Summary}
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $filter Filter.
    #// @return array|bool|object|WP_Post
    #//
    def filter(self, filter=None):
        
        if self.filter == filter:
            return self
        # end if
        if "raw" == filter:
            return self.get_instance(self.ID)
        # end if
        return sanitize_post(self, filter)
    # end def filter
    #// 
    #// Convert object to array.
    #// 
    #// @since 3.5.0
    #// 
    #// @return array Object as array.
    #//
    def to_array(self):
        
        post = get_object_vars(self)
        for key in Array("ancestors", "page_template", "post_category", "tags_input"):
            if self.__isset(key):
                post[key] = self.__get(key)
            # end if
        # end for
        return post
    # end def to_array
# end class WP_Post
