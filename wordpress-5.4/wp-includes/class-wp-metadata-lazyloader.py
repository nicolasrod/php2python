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
#// Meta API: WP_Metadata_Lazyloader class
#// 
#// @package WordPress
#// @subpackage Meta
#// @since 4.5.0
#// 
#// 
#// Core class used for lazy-loading object metadata.
#// 
#// When loading many objects of a given type, such as posts in a WP_Query loop, it often makes
#// sense to prime various metadata caches at the beginning of the loop. This means fetching all
#// relevant metadata with a single database query, a technique that has the potential to improve
#// performance dramatically in some cases.
#// 
#// In cases where the given metadata may not even be used in the loop, we can improve performance
#// even more by only priming the metadata cache for affected items the first time a piece of metadata
#// is requested - ie, by lazy-loading it. So, for example, comment meta may not be loaded into the
#// cache in the comments section of a post until the first time get_comment_meta() is called in the
#// context of the comment loop.
#// 
#// WP uses the WP_Metadata_Lazyloader class to queue objects for metadata cache priming. The class
#// then detects the relevant get_*_meta() function call, and queries the metadata of all queued objects.
#// 
#// Do not access this class directly. Use the wp_metadata_lazyloader() function.
#// 
#// @since 4.5.0
#//
class WP_Metadata_Lazyloader():
    #// 
    #// Pending objects queue.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    pending_objects = Array()
    #// 
    #// Settings for supported object types.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    settings = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.5.0
    #//
    def __init__(self):
        
        
        self.settings = Array({"term": Array({"filter": "get_term_metadata", "callback": Array(self, "lazyload_term_meta")})}, {"comment": Array({"filter": "get_comment_metadata", "callback": Array(self, "lazyload_comment_meta")})})
    # end def __init__
    #// 
    #// Adds objects to the metadata lazy-load queue.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $object_type Type of object whose meta is to be lazy-loaded. Accepts 'term' or 'comment'.
    #// @param array  $object_ids  Array of object IDs.
    #// @return bool|WP_Error True on success, WP_Error on failure.
    #//
    def queue_objects(self, object_type_=None, object_ids_=None):
        
        
        if (not (php_isset(lambda : self.settings[object_type_]))):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_object_type", __("Invalid object type.")))
        # end if
        type_settings_ = self.settings[object_type_]
        if (not (php_isset(lambda : self.pending_objects[object_type_]))):
            self.pending_objects[object_type_] = Array()
        # end if
        for object_id_ in object_ids_:
            #// Keyed by ID for faster lookup.
            if (not (php_isset(lambda : self.pending_objects[object_type_][object_id_]))):
                self.pending_objects[object_type_][object_id_] = 1
            # end if
        # end for
        add_filter(type_settings_["filter"], type_settings_["callback"])
        #// 
        #// Fires after objects are added to the metadata lazy-load queue.
        #// 
        #// @since 4.5.0
        #// 
        #// @param array                  $object_ids  Array of object IDs.
        #// @param string                 $object_type Type of object being queued.
        #// @param WP_Metadata_Lazyloader $lazyloader  The lazy-loader object.
        #//
        do_action("metadata_lazyloader_queued_objects", object_ids_, object_type_, self)
    # end def queue_objects
    #// 
    #// Resets lazy-load queue for a given object type.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $object_type Object type. Accepts 'comment' or 'term'.
    #// @return bool|WP_Error True on success, WP_Error on failure.
    #//
    def reset_queue(self, object_type_=None):
        
        
        if (not (php_isset(lambda : self.settings[object_type_]))):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_object_type", __("Invalid object type.")))
        # end if
        type_settings_ = self.settings[object_type_]
        self.pending_objects[object_type_] = Array()
        remove_filter(type_settings_["filter"], type_settings_["callback"])
    # end def reset_queue
    #// 
    #// Lazy-loads term meta for queued terms.
    #// 
    #// This method is public so that it can be used as a filter callback. As a rule, there
    #// is no need to invoke it directly.
    #// 
    #// @since 4.5.0
    #// 
    #// @param mixed $check The `$check` param passed from the 'get_term_metadata' hook.
    #// @return mixed In order not to short-circuit `get_metadata()`. Generally, this is `null`, but it could be
    #// another value if filtered by a plugin.
    #//
    def lazyload_term_meta(self, check_=None):
        
        
        if (not php_empty(lambda : self.pending_objects["term"])):
            update_termmeta_cache(php_array_keys(self.pending_objects["term"]))
            #// No need to run again for this set of terms.
            self.reset_queue("term")
        # end if
        return check_
    # end def lazyload_term_meta
    #// 
    #// Lazy-loads comment meta for queued comments.
    #// 
    #// This method is public so that it can be used as a filter callback. As a rule, there is no need to invoke it
    #// directly, from either inside or outside the `WP_Query` object.
    #// 
    #// @since 4.5.0
    #// 
    #// @param mixed $check The `$check` param passed from the {@see 'get_comment_metadata'} hook.
    #// @return mixed The original value of `$check`, so as not to short-circuit `get_comment_metadata()`.
    #//
    def lazyload_comment_meta(self, check_=None):
        
        
        if (not php_empty(lambda : self.pending_objects["comment"])):
            update_meta_cache("comment", php_array_keys(self.pending_objects["comment"]))
            #// No need to run again for this set of comments.
            self.reset_queue("comment")
        # end if
        return check_
    # end def lazyload_comment_meta
# end class WP_Metadata_Lazyloader
