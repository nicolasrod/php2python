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
#// Post revision functions.
#// 
#// @package WordPress
#// @subpackage Post_Revisions
#// 
#// 
#// Determines which fields of posts are to be saved in revisions.
#// 
#// @since 2.6.0
#// @since 4.5.0 A `WP_Post` object can now be passed to the `$post` parameter.
#// @since 4.5.0 The optional `$autosave` parameter was deprecated and renamed to `$deprecated`.
#// @access private
#// 
#// @staticvar array $fields
#// 
#// @param array|WP_Post $post       Optional. A post array or a WP_Post object being processed
#// for insertion as a post revision. Default empty array.
#// @param bool          $deprecated Not used.
#// @return array Array of fields that can be versioned.
#//
def _wp_post_revision_fields(post_=None, deprecated_=None, *_args_):
    if post_ is None:
        post_ = Array()
    # end if
    if deprecated_ is None:
        deprecated_ = False
    # end if
    
    fields_ = None
    if (not php_is_array(post_)):
        post_ = get_post(post_, ARRAY_A)
    # end if
    if is_null(fields_):
        #// Allow these to be versioned.
        fields_ = Array({"post_title": __("Title"), "post_content": __("Content"), "post_excerpt": __("Excerpt")})
    # end if
    #// 
    #// Filters the list of fields saved in post revisions.
    #// 
    #// Included by default: 'post_title', 'post_content' and 'post_excerpt'.
    #// 
    #// Disallowed fields: 'ID', 'post_name', 'post_parent', 'post_date',
    #// 'post_date_gmt', 'post_status', 'post_type', 'comment_count',
    #// and 'post_author'.
    #// 
    #// @since 2.6.0
    #// @since 4.5.0 The `$post` parameter was added.
    #// 
    #// @param array $fields List of fields to revision. Contains 'post_title',
    #// 'post_content', and 'post_excerpt' by default.
    #// @param array $post   A post array being processed for insertion as a post revision.
    #//
    fields_ = apply_filters("_wp_post_revision_fields", fields_, post_)
    #// WP uses these internally either in versioning or elsewhere - they cannot be versioned.
    for protect_ in Array("ID", "post_name", "post_parent", "post_date", "post_date_gmt", "post_status", "post_type", "comment_count", "post_author"):
        fields_[protect_] = None
    # end for
    return fields_
# end def _wp_post_revision_fields
#// 
#// Returns a post array ready to be inserted into the posts table as a post revision.
#// 
#// @since 4.5.0
#// @access private
#// 
#// @param array|WP_Post $post     Optional. A post array or a WP_Post object to be processed
#// for insertion as a post revision. Default empty array.
#// @param bool          $autosave Optional. Is the revision an autosave? Default false.
#// @return array Post array ready to be inserted as a post revision.
#//
def _wp_post_revision_data(post_=None, autosave_=None, *_args_):
    if post_ is None:
        post_ = Array()
    # end if
    if autosave_ is None:
        autosave_ = False
    # end if
    
    if (not php_is_array(post_)):
        post_ = get_post(post_, ARRAY_A)
    # end if
    fields_ = _wp_post_revision_fields(post_)
    revision_data_ = Array()
    for field_ in php_array_intersect(php_array_keys(post_), php_array_keys(fields_)):
        revision_data_[field_] = post_[field_]
    # end for
    revision_data_["post_parent"] = post_["ID"]
    revision_data_["post_status"] = "inherit"
    revision_data_["post_type"] = "revision"
    revision_data_["post_name"] = str(post_["ID"]) + str("-autosave-v1") if autosave_ else str(post_["ID"]) + str("-revision-v1")
    #// "1" is the revisioning system version.
    revision_data_["post_date"] = post_["post_modified"] if (php_isset(lambda : post_["post_modified"])) else ""
    revision_data_["post_date_gmt"] = post_["post_modified_gmt"] if (php_isset(lambda : post_["post_modified_gmt"])) else ""
    return revision_data_
# end def _wp_post_revision_data
#// 
#// Creates a revision for the current version of a post.
#// 
#// Typically used immediately after a post update, as every update is a revision,
#// and the most recent revision always matches the current post.
#// 
#// @since 2.6.0
#// 
#// @param int $post_id The ID of the post to save as a revision.
#// @return int|WP_Error|void Void or 0 if error, new revision ID, if success.
#//
def wp_save_post_revision(post_id_=None, *_args_):
    
    
    if php_defined("DOING_AUTOSAVE") and DOING_AUTOSAVE:
        return
    # end if
    post_ = get_post(post_id_)
    if (not post_):
        return
    # end if
    if (not post_type_supports(post_.post_type, "revisions")):
        return
    # end if
    if "auto-draft" == post_.post_status:
        return
    # end if
    if (not wp_revisions_enabled(post_)):
        return
    # end if
    #// 
    #// Compare the proposed update with the last stored revision verifying that
    #// they are different, unless a plugin tells us to always save regardless.
    #// If no previous revisions, save one.
    #//
    revisions_ = wp_get_post_revisions(post_id_)
    if revisions_:
        #// Grab the last revision, but not an autosave.
        for revision_ in revisions_:
            if False != php_strpos(revision_.post_name, str(revision_.post_parent) + str("-revision")):
                last_revision_ = revision_
                break
            # end if
        # end for
        #// 
        #// Filters whether the post has changed since the last revision.
        #// 
        #// By default a revision is saved only if one of the revisioned fields has changed.
        #// This filter can override that so a revision is saved even if nothing has changed.
        #// 
        #// @since 3.6.0
        #// 
        #// @param bool    $check_for_changes Whether to check for changes before saving a new revision.
        #// Default true.
        #// @param WP_Post $last_revision     The last revision post object.
        #// @param WP_Post $post              The post object.
        #//
        if (php_isset(lambda : last_revision_)) and apply_filters("wp_save_post_revision_check_for_changes", True, last_revision_, post_):
            post_has_changed_ = False
            for field_ in php_array_keys(_wp_post_revision_fields(post_)):
                if normalize_whitespace(post_.field_) != normalize_whitespace(last_revision_.field_):
                    post_has_changed_ = True
                    break
                # end if
            # end for
            #// 
            #// Filters whether a post has changed.
            #// 
            #// By default a revision is saved only if one of the revisioned fields has changed.
            #// This filter allows for additional checks to determine if there were changes.
            #// 
            #// @since 4.1.0
            #// 
            #// @param bool    $post_has_changed Whether the post has changed.
            #// @param WP_Post $last_revision    The last revision post object.
            #// @param WP_Post $post             The post object.
            #//
            post_has_changed_ = php_bool(apply_filters("wp_save_post_revision_post_has_changed", post_has_changed_, last_revision_, post_))
            #// Don't save revision if post unchanged.
            if (not post_has_changed_):
                return
            # end if
        # end if
    # end if
    return_ = _wp_put_post_revision(post_)
    #// If a limit for the number of revisions to keep has been set,
    #// delete the oldest ones.
    revisions_to_keep_ = wp_revisions_to_keep(post_)
    if revisions_to_keep_ < 0:
        return return_
    # end if
    revisions_ = wp_get_post_revisions(post_id_, Array({"order": "ASC"}))
    delete_ = php_count(revisions_) - revisions_to_keep_
    if delete_ < 1:
        return return_
    # end if
    revisions_ = php_array_slice(revisions_, 0, delete_)
    i_ = 0
    while (php_isset(lambda : revisions_[i_])):
        
        if False != php_strpos(revisions_[i_].post_name, "autosave"):
            continue
        # end if
        wp_delete_post_revision(revisions_[i_].ID)
        i_ += 1
    # end while
    return return_
# end def wp_save_post_revision
#// 
#// Retrieve the autosaved data of the specified post.
#// 
#// Returns a post object containing the information that was autosaved for the
#// specified post. If the optional $user_id is passed, returns the autosave for that user
#// otherwise returns the latest autosave.
#// 
#// @since 2.6.0
#// 
#// @param int $post_id The post ID.
#// @param int $user_id Optional The post author ID.
#// @return WP_Post|false The autosaved data or false on failure or when no autosave exists.
#//
def wp_get_post_autosave(post_id_=None, user_id_=0, *_args_):
    
    
    revisions_ = wp_get_post_revisions(post_id_, Array({"check_enabled": False}))
    for revision_ in revisions_:
        if False != php_strpos(revision_.post_name, str(post_id_) + str("-autosave")):
            if user_id_ and user_id_ != revision_.post_author:
                continue
            # end if
            return revision_
        # end if
    # end for
    return False
# end def wp_get_post_autosave
#// 
#// Determines if the specified post is a revision.
#// 
#// @since 2.6.0
#// 
#// @param int|WP_Post $post Post ID or post object.
#// @return int|false ID of revision's parent on success, false if not a revision.
#//
def wp_is_post_revision(post_=None, *_args_):
    
    
    post_ = wp_get_post_revision(post_)
    if (not post_):
        return False
    # end if
    return php_int(post_.post_parent)
# end def wp_is_post_revision
#// 
#// Determines if the specified post is an autosave.
#// 
#// @since 2.6.0
#// 
#// @param int|WP_Post $post Post ID or post object.
#// @return int|false ID of autosave's parent on success, false if not a revision.
#//
def wp_is_post_autosave(post_=None, *_args_):
    
    
    post_ = wp_get_post_revision(post_)
    if (not post_):
        return False
    # end if
    if False != php_strpos(post_.post_name, str(post_.post_parent) + str("-autosave")):
        return php_int(post_.post_parent)
    # end if
    return False
# end def wp_is_post_autosave
#// 
#// Inserts post data into the posts table as a post revision.
#// 
#// @since 2.6.0
#// @access private
#// 
#// @param int|WP_Post|array|null $post     Post ID, post object OR post array.
#// @param bool                   $autosave Optional. Is the revision an autosave?
#// @return int|WP_Error WP_Error or 0 if error, new revision ID if success.
#//
def _wp_put_post_revision(post_=None, autosave_=None, *_args_):
    if autosave_ is None:
        autosave_ = False
    # end if
    
    if php_is_object(post_):
        post_ = get_object_vars(post_)
    elif (not php_is_array(post_)):
        post_ = get_post(post_, ARRAY_A)
    # end if
    if (not post_) or php_empty(lambda : post_["ID"]):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post ID.")))
    # end if
    if (php_isset(lambda : post_["post_type"])) and "revision" == post_["post_type"]:
        return php_new_class("WP_Error", lambda : WP_Error("post_type", __("Cannot create a revision of a revision")))
    # end if
    post_ = _wp_post_revision_data(post_, autosave_)
    post_ = wp_slash(post_)
    #// Since data is from DB.
    revision_id_ = wp_insert_post(post_)
    if is_wp_error(revision_id_):
        return revision_id_
    # end if
    if revision_id_:
        #// 
        #// Fires once a revision has been saved.
        #// 
        #// @since 2.6.0
        #// 
        #// @param int $revision_id Post revision ID.
        #//
        do_action("_wp_put_post_revision", revision_id_)
    # end if
    return revision_id_
# end def _wp_put_post_revision
#// 
#// Gets a post revision.
#// 
#// @since 2.6.0
#// 
#// @param int|WP_Post $post   The post ID or object.
#// @param string      $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Post object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string      $filter Optional sanitation filter. See sanitize_post().
#// @return WP_Post|array|null WP_Post (or array) on success, or null on failure.
#//
def wp_get_post_revision(post_=None, output_=None, filter_="raw", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    revision_ = get_post(post_, OBJECT, filter_)
    if (not revision_):
        return revision_
    # end if
    if "revision" != revision_.post_type:
        return None
    # end if
    if OBJECT == output_:
        return revision_
    elif ARRAY_A == output_:
        _revision_ = get_object_vars(revision_)
        return _revision_
    elif ARRAY_N == output_:
        _revision_ = php_array_values(get_object_vars(revision_))
        return _revision_
    # end if
    return revision_
# end def wp_get_post_revision
#// 
#// Restores a post to the specified revision.
#// 
#// Can restore a past revision using all fields of the post revision, or only selected fields.
#// 
#// @since 2.6.0
#// 
#// @param int|WP_Post $revision_id Revision ID or revision object.
#// @param array       $fields      Optional. What fields to restore from. Defaults to all.
#// @return int|false|null Null if error, false if no fields to restore, (int) post ID if success.
#//
def wp_restore_post_revision(revision_id_=None, fields_=None, *_args_):
    
    
    revision_ = wp_get_post_revision(revision_id_, ARRAY_A)
    if (not revision_):
        return revision_
    # end if
    if (not php_is_array(fields_)):
        fields_ = php_array_keys(_wp_post_revision_fields(revision_))
    # end if
    update_ = Array()
    for field_ in php_array_intersect(php_array_keys(revision_), fields_):
        update_[field_] = revision_[field_]
    # end for
    if (not update_):
        return False
    # end if
    update_["ID"] = revision_["post_parent"]
    update_ = wp_slash(update_)
    #// Since data is from DB.
    post_id_ = wp_update_post(update_)
    if (not post_id_) or is_wp_error(post_id_):
        return post_id_
    # end if
    #// Update last edit user.
    update_post_meta(post_id_, "_edit_last", get_current_user_id())
    #// 
    #// Fires after a post revision has been restored.
    #// 
    #// @since 2.6.0
    #// 
    #// @param int $post_id     Post ID.
    #// @param int $revision_id Post revision ID.
    #//
    do_action("wp_restore_post_revision", post_id_, revision_["ID"])
    return post_id_
# end def wp_restore_post_revision
#// 
#// Deletes a revision.
#// 
#// Deletes the row from the posts table corresponding to the specified revision.
#// 
#// @since 2.6.0
#// 
#// @param int|WP_Post $revision_id Revision ID or revision object.
#// @return array|false|WP_Post|WP_Error|null Null or WP_Error if error, deleted post if success.
#//
def wp_delete_post_revision(revision_id_=None, *_args_):
    
    
    revision_ = wp_get_post_revision(revision_id_)
    if (not revision_):
        return revision_
    # end if
    delete_ = wp_delete_post(revision_.ID)
    if delete_:
        #// 
        #// Fires once a post revision has been deleted.
        #// 
        #// @since 2.6.0
        #// 
        #// @param int     $revision_id Post revision ID.
        #// @param WP_Post $revision    Post revision object.
        #//
        do_action("wp_delete_post_revision", revision_.ID, revision_)
    # end if
    return delete_
# end def wp_delete_post_revision
#// 
#// Returns all revisions of specified post.
#// 
#// @since 2.6.0
#// 
#// @see get_children()
#// 
#// @param int|WP_Post $post_id Optional. Post ID or WP_Post object. Default is global `$post`.
#// @param array|null  $args    Optional. Arguments for retrieving post revisions. Default null.
#// @return array An array of revisions, or an empty array if none.
#//
def wp_get_post_revisions(post_id_=0, args_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_) or php_empty(lambda : post_.ID):
        return Array()
    # end if
    defaults_ = Array({"order": "DESC", "orderby": "date ID", "check_enabled": True})
    args_ = wp_parse_args(args_, defaults_)
    if args_["check_enabled"] and (not wp_revisions_enabled(post_)):
        return Array()
    # end if
    args_ = php_array_merge(args_, Array({"post_parent": post_.ID, "post_type": "revision", "post_status": "inherit"}))
    revisions_ = get_children(args_)
    if (not revisions_):
        return Array()
    # end if
    return revisions_
# end def wp_get_post_revisions
#// 
#// Determine if revisions are enabled for a given post.
#// 
#// @since 3.6.0
#// 
#// @param WP_Post $post The post object.
#// @return bool True if number of revisions to keep isn't zero, false otherwise.
#//
def wp_revisions_enabled(post_=None, *_args_):
    
    
    return wp_revisions_to_keep(post_) != 0
# end def wp_revisions_enabled
#// 
#// Determine how many revisions to retain for a given post.
#// 
#// By default, an infinite number of revisions are kept.
#// 
#// The constant WP_POST_REVISIONS can be set in wp-config to specify the limit
#// of revisions to keep.
#// 
#// @since 3.6.0
#// 
#// @param WP_Post $post The post object.
#// @return int The number of revisions to keep.
#//
def wp_revisions_to_keep(post_=None, *_args_):
    
    
    num_ = WP_POST_REVISIONS
    if True == num_:
        num_ = -1
    else:
        num_ = php_intval(num_)
    # end if
    if (not post_type_supports(post_.post_type, "revisions")):
        num_ = 0
    # end if
    #// 
    #// Filters the number of revisions to save for the given post.
    #// 
    #// Overrides the value of WP_POST_REVISIONS.
    #// 
    #// @since 3.6.0
    #// 
    #// @param int     $num  Number of revisions to store.
    #// @param WP_Post $post Post object.
    #//
    return php_int(apply_filters("wp_revisions_to_keep", num_, post_))
# end def wp_revisions_to_keep
#// 
#// Sets up the post object for preview based on the post autosave.
#// 
#// @since 2.7.0
#// @access private
#// 
#// @param WP_Post $post
#// @return WP_Post|false
#//
def _set_preview(post_=None, *_args_):
    
    
    if (not php_is_object(post_)):
        return post_
    # end if
    preview_ = wp_get_post_autosave(post_.ID)
    if (not php_is_object(preview_)):
        return post_
    # end if
    preview_ = sanitize_post(preview_)
    post_.post_content = preview_.post_content
    post_.post_title = preview_.post_title
    post_.post_excerpt = preview_.post_excerpt
    add_filter("get_the_terms", "_wp_preview_terms_filter", 10, 3)
    add_filter("get_post_metadata", "_wp_preview_post_thumbnail_filter", 10, 3)
    return post_
# end def _set_preview
#// 
#// Filters the latest content for preview from the post autosave.
#// 
#// @since 2.7.0
#// @access private
#//
def _show_post_preview(*_args_):
    
    
    if (php_isset(lambda : PHP_REQUEST["preview_id"])) and (php_isset(lambda : PHP_REQUEST["preview_nonce"])):
        id_ = php_int(PHP_REQUEST["preview_id"])
        if False == wp_verify_nonce(PHP_REQUEST["preview_nonce"], "post_preview_" + id_):
            wp_die(__("Sorry, you are not allowed to preview drafts."), 403)
        # end if
        add_filter("the_preview", "_set_preview")
    # end if
# end def _show_post_preview
#// 
#// Filters terms lookup to set the post format.
#// 
#// @since 3.6.0
#// @access private
#// 
#// @param array  $terms
#// @param int    $post_id
#// @param string $taxonomy
#// @return array
#//
def _wp_preview_terms_filter(terms_=None, post_id_=None, taxonomy_=None, *_args_):
    
    
    post_ = get_post()
    if (not post_):
        return terms_
    # end if
    if php_empty(lambda : PHP_REQUEST["post_format"]) or post_.ID != post_id_ or "post_format" != taxonomy_ or "revision" == post_.post_type:
        return terms_
    # end if
    if "standard" == PHP_REQUEST["post_format"]:
        terms_ = Array()
    else:
        term_ = get_term_by("slug", "post-format-" + sanitize_key(PHP_REQUEST["post_format"]), "post_format")
        if term_:
            terms_ = Array(term_)
            pass
        # end if
    # end if
    return terms_
# end def _wp_preview_terms_filter
#// 
#// Filters post thumbnail lookup to set the post thumbnail.
#// 
#// @since 4.6.0
#// @access private
#// 
#// @param null|array|string $value    The value to return - a single metadata value, or an array of values.
#// @param int               $post_id  Post ID.
#// @param string            $meta_key Meta key.
#// @return null|array The default return value or the post thumbnail meta array.
#//
def _wp_preview_post_thumbnail_filter(value_=None, post_id_=None, meta_key_=None, *_args_):
    
    
    post_ = get_post()
    if (not post_):
        return value_
    # end if
    if php_empty(lambda : PHP_REQUEST["_thumbnail_id"]) or php_empty(lambda : PHP_REQUEST["preview_id"]) or post_.ID != post_id_ or "_thumbnail_id" != meta_key_ or "revision" == post_.post_type or post_id_ != PHP_REQUEST["preview_id"]:
        return value_
    # end if
    thumbnail_id_ = php_intval(PHP_REQUEST["_thumbnail_id"])
    if thumbnail_id_ <= 0:
        return ""
    # end if
    return php_strval(thumbnail_id_)
# end def _wp_preview_post_thumbnail_filter
#// 
#// Gets the post revision version.
#// 
#// @since 3.6.0
#// @access private
#// 
#// @param WP_Post $revision
#// @return int|false
#//
def _wp_get_post_revision_version(revision_=None, *_args_):
    
    
    if php_is_object(revision_):
        revision_ = get_object_vars(revision_)
    elif (not php_is_array(revision_)):
        return False
    # end if
    if php_preg_match("/^\\d+-(?:autosave|revision)-v(\\d+)$/", revision_["post_name"], matches_):
        return php_int(matches_[1])
    # end if
    return 0
# end def _wp_get_post_revision_version
#// 
#// Upgrade the revisions author, add the current post as a revision and set the revisions version to 1
#// 
#// @since 3.6.0
#// @access private
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param WP_Post $post      Post object
#// @param array   $revisions Current revisions of the post
#// @return bool true if the revisions were upgraded, false if problems
#//
def _wp_upgrade_revisions_of_post(post_=None, revisions_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Add post option exclusively.
    lock_ = str("revision-upgrade-") + str(post_.ID)
    now_ = time()
    result_ = wpdb_.query(wpdb_.prepare(str("INSERT IGNORE INTO `") + str(wpdb_.options) + str("` (`option_name`, `option_value`, `autoload`) VALUES (%s, %s, 'no') /* LOCK */"), lock_, now_))
    if (not result_):
        #// If we couldn't get a lock, see how old the previous lock is.
        locked_ = get_option(lock_)
        if (not locked_):
            #// Can't write to the lock, and can't read the lock.
            #// Something broken has happened.
            return False
        # end if
        if locked_ > now_ - 3600:
            #// Lock is not too old: some other process may be upgrading this post. Bail.
            return False
        # end if
        pass
    # end if
    #// If we could get a lock, re-"add" the option to fire all the correct filters.
    update_option(lock_, now_)
    reset(revisions_)
    add_last_ = True
    while True:
        this_revision_ = current(revisions_)
        prev_revision_ = next(revisions_)
        this_revision_version_ = _wp_get_post_revision_version(this_revision_)
        #// Something terrible happened.
        if False == this_revision_version_:
            continue
        # end if
        #// 1 is the latest revision version, so we're already up to date.
        #// No need to add a copy of the post as latest revision.
        if 0 < this_revision_version_:
            add_last_ = False
            continue
        # end if
        #// Always update the revision version.
        update_ = Array({"post_name": php_preg_replace("/^(\\d+-(?:autosave|revision))[\\d-]*$/", "$1-v1", this_revision_.post_name)})
        #// 
        #// If this revision is the oldest revision of the post, i.e. no $prev_revision,
        #// the correct post_author is probably $post->post_author, but that's only a good guess.
        #// Update the revision version only and Leave the author as-is.
        #//
        if prev_revision_:
            prev_revision_version_ = _wp_get_post_revision_version(prev_revision_)
            #// If the previous revision is already up to date, it no longer has the information we need :(
            if prev_revision_version_ < 1:
                update_["post_author"] = prev_revision_.post_author
            # end if
        # end if
        #// Upgrade this revision.
        result_ = wpdb_.update(wpdb_.posts, update_, Array({"ID": this_revision_.ID}))
        if result_:
            wp_cache_delete(this_revision_.ID, "posts")
        # end if
        
        if prev_revision_:
            break
        # end if
    # end while
    delete_option(lock_)
    #// Add a copy of the post as latest revision.
    if add_last_:
        wp_save_post_revision(post_.ID)
    # end if
    return True
# end def _wp_upgrade_revisions_of_post
