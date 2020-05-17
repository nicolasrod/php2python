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
    #// 
    #// Post ID.
    #// 
    #// @since 3.5.0
    #// @var int
    #//
    ID = Array()
    #// 
    #// ID of post author.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_author = 0
    #// 
    #// The post's local publication time.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_date = "0000-00-00 00:00:00"
    #// 
    #// The post's GMT publication time.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_date_gmt = "0000-00-00 00:00:00"
    #// 
    #// The post's content.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_content = ""
    #// 
    #// The post's title.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_title = ""
    #// 
    #// The post's excerpt.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_excerpt = ""
    #// 
    #// The post's status.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_status = "publish"
    #// 
    #// Whether comments are allowed.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    comment_status = "open"
    #// 
    #// Whether pings are allowed.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    ping_status = "open"
    #// 
    #// The post's password in plain text.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_password = ""
    #// 
    #// The post's slug.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_name = ""
    #// 
    #// URLs queued to be pinged.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    to_ping = ""
    #// 
    #// URLs that have been pinged.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    pinged = ""
    #// 
    #// The post's local modified time.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_modified = "0000-00-00 00:00:00"
    #// 
    #// The post's GMT modified time.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_modified_gmt = "0000-00-00 00:00:00"
    #// 
    #// A utility DB field for post content.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_content_filtered = ""
    #// 
    #// ID of a post's parent post.
    #// 
    #// @since 3.5.0
    #// @var int
    #//
    post_parent = 0
    #// 
    #// The unique identifier for a post, not necessarily a URL, used as the feed GUID.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    guid = ""
    #// 
    #// A field used for ordering posts.
    #// 
    #// @since 3.5.0
    #// @var int
    #//
    menu_order = 0
    #// 
    #// The post's type, like post or page.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_type = "post"
    #// 
    #// An attachment's mime type.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    post_mime_type = ""
    #// 
    #// Cached comment count.
    #// 
    #// A numeric string, for compatibility reasons.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    comment_count = 0
    #// 
    #// Stores the post object's sanitization level.
    #// 
    #// Does not correspond to a DB field.
    #// 
    #// @since 3.5.0
    #// @var string
    #//
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
    def get_instance(self, post_id_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        post_id_ = php_int(post_id_)
        if (not post_id_):
            return False
        # end if
        _post_ = wp_cache_get(post_id_, "posts")
        if (not _post_):
            _post_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.posts) + str(" WHERE ID = %d LIMIT 1"), post_id_))
            if (not _post_):
                return False
            # end if
            _post_ = sanitize_post(_post_, "raw")
            wp_cache_add(_post_.ID, _post_, "posts")
        elif php_empty(lambda : _post_.filter):
            _post_ = sanitize_post(_post_, "raw")
        # end if
        return php_new_class("WP_Post", lambda : WP_Post(_post_))
    # end def get_instance
    #// 
    #// Constructor.
    #// 
    #// @since 3.5.0
    #// 
    #// @param WP_Post|object $post Post object.
    #//
    def __init__(self, post_=None):
        
        
        for key_,value_ in get_object_vars(post_):
            self.key_ = value_
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
    def __isset(self, key_=None):
        
        
        if "ancestors" == key_:
            return True
        # end if
        if "page_template" == key_:
            return True
        # end if
        if "post_category" == key_:
            return True
        # end if
        if "tags_input" == key_:
            return True
        # end if
        return metadata_exists("post", self.ID, key_)
    # end def __isset
    #// 
    #// Getter.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $key Key to get.
    #// @return mixed
    #//
    def __get(self, key_=None):
        
        
        if "page_template" == key_ and self.__isset(key_):
            return get_post_meta(self.ID, "_wp_page_template", True)
        # end if
        if "post_category" == key_:
            if is_object_in_taxonomy(self.post_type, "category"):
                terms_ = get_the_terms(self, "category")
            # end if
            if php_empty(lambda : terms_):
                return Array()
            # end if
            return wp_list_pluck(terms_, "term_id")
        # end if
        if "tags_input" == key_:
            if is_object_in_taxonomy(self.post_type, "post_tag"):
                terms_ = get_the_terms(self, "post_tag")
            # end if
            if php_empty(lambda : terms_):
                return Array()
            # end if
            return wp_list_pluck(terms_, "name")
        # end if
        #// Rest of the values need filtering.
        if "ancestors" == key_:
            value_ = get_post_ancestors(self)
        else:
            value_ = get_post_meta(self.ID, key_, True)
        # end if
        if self.filter:
            value_ = sanitize_post_field(key_, value_, self.ID, self.filter)
        # end if
        return value_
    # end def __get
    #// 
    #// {@Missing Summary}
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $filter Filter.
    #// @return array|bool|object|WP_Post
    #//
    def filter(self, filter_=None):
        
        
        if self.filter == filter_:
            return self
        # end if
        if "raw" == filter_:
            return self.get_instance(self.ID)
        # end if
        return sanitize_post(self, filter_)
    # end def filter
    #// 
    #// Convert object to array.
    #// 
    #// @since 3.5.0
    #// 
    #// @return array Object as array.
    #//
    def to_array(self):
        
        
        post_ = get_object_vars(self)
        for key_ in Array("ancestors", "page_template", "post_category", "tags_input"):
            if self.__isset(key_):
                post_[key_] = self.__get(key_)
            # end if
        # end for
        return post_
    # end def to_array
# end class WP_Post
