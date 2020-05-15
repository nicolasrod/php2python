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
def _wp_post_revision_fields(post=Array(), deprecated=False, *args_):
    
    fields = None
    if (not php_is_array(post)):
        post = get_post(post, ARRAY_A)
    # end if
    if php_is_null(fields):
        #// Allow these to be versioned.
        fields = Array({"post_title": __("Title"), "post_content": __("Content"), "post_excerpt": __("Excerpt")})
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
    fields = apply_filters("_wp_post_revision_fields", fields, post)
    #// WP uses these internally either in versioning or elsewhere - they cannot be versioned.
    for protect in Array("ID", "post_name", "post_parent", "post_date", "post_date_gmt", "post_status", "post_type", "comment_count", "post_author"):
        fields[protect] = None
    # end for
    return fields
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
def _wp_post_revision_data(post=Array(), autosave=False, *args_):
    
    if (not php_is_array(post)):
        post = get_post(post, ARRAY_A)
    # end if
    fields = _wp_post_revision_fields(post)
    revision_data = Array()
    for field in php_array_intersect(php_array_keys(post), php_array_keys(fields)):
        revision_data[field] = post[field]
    # end for
    revision_data["post_parent"] = post["ID"]
    revision_data["post_status"] = "inherit"
    revision_data["post_type"] = "revision"
    revision_data["post_name"] = str(post["ID"]) + str("-autosave-v1") if autosave else str(post["ID"]) + str("-revision-v1")
    #// "1" is the revisioning system version.
    revision_data["post_date"] = post["post_modified"] if (php_isset(lambda : post["post_modified"])) else ""
    revision_data["post_date_gmt"] = post["post_modified_gmt"] if (php_isset(lambda : post["post_modified_gmt"])) else ""
    return revision_data
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
def wp_save_post_revision(post_id=None, *args_):
    
    if php_defined("DOING_AUTOSAVE") and DOING_AUTOSAVE:
        return
    # end if
    post = get_post(post_id)
    if (not post):
        return
    # end if
    if (not post_type_supports(post.post_type, "revisions")):
        return
    # end if
    if "auto-draft" == post.post_status:
        return
    # end if
    if (not wp_revisions_enabled(post)):
        return
    # end if
    #// 
    #// Compare the proposed update with the last stored revision verifying that
    #// they are different, unless a plugin tells us to always save regardless.
    #// If no previous revisions, save one.
    #//
    revisions = wp_get_post_revisions(post_id)
    if revisions:
        #// Grab the last revision, but not an autosave.
        for revision in revisions:
            if False != php_strpos(revision.post_name, str(revision.post_parent) + str("-revision")):
                last_revision = revision
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
        if (php_isset(lambda : last_revision)) and apply_filters("wp_save_post_revision_check_for_changes", True, last_revision, post):
            post_has_changed = False
            for field in php_array_keys(_wp_post_revision_fields(post)):
                if normalize_whitespace(post.field) != normalize_whitespace(last_revision.field):
                    post_has_changed = True
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
            post_has_changed = bool(apply_filters("wp_save_post_revision_post_has_changed", post_has_changed, last_revision, post))
            #// Don't save revision if post unchanged.
            if (not post_has_changed):
                return
            # end if
        # end if
    # end if
    return_ = _wp_put_post_revision(post)
    #// If a limit for the number of revisions to keep has been set,
    #// delete the oldest ones.
    revisions_to_keep = wp_revisions_to_keep(post)
    if revisions_to_keep < 0:
        return return_
    # end if
    revisions = wp_get_post_revisions(post_id, Array({"order": "ASC"}))
    delete = php_count(revisions) - revisions_to_keep
    if delete < 1:
        return return_
    # end if
    revisions = php_array_slice(revisions, 0, delete)
    i = 0
    while (php_isset(lambda : revisions[i])):
        
        if False != php_strpos(revisions[i].post_name, "autosave"):
            continue
        # end if
        wp_delete_post_revision(revisions[i].ID)
        i += 1
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
def wp_get_post_autosave(post_id=None, user_id=0, *args_):
    
    revisions = wp_get_post_revisions(post_id, Array({"check_enabled": False}))
    for revision in revisions:
        if False != php_strpos(revision.post_name, str(post_id) + str("-autosave")):
            if user_id and user_id != revision.post_author:
                continue
            # end if
            return revision
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
def wp_is_post_revision(post=None, *args_):
    
    post = wp_get_post_revision(post)
    if (not post):
        return False
    # end if
    return int(post.post_parent)
# end def wp_is_post_revision
#// 
#// Determines if the specified post is an autosave.
#// 
#// @since 2.6.0
#// 
#// @param int|WP_Post $post Post ID or post object.
#// @return int|false ID of autosave's parent on success, false if not a revision.
#//
def wp_is_post_autosave(post=None, *args_):
    
    post = wp_get_post_revision(post)
    if (not post):
        return False
    # end if
    if False != php_strpos(post.post_name, str(post.post_parent) + str("-autosave")):
        return int(post.post_parent)
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
def _wp_put_post_revision(post=None, autosave=False, *args_):
    
    if php_is_object(post):
        post = get_object_vars(post)
    elif (not php_is_array(post)):
        post = get_post(post, ARRAY_A)
    # end if
    if (not post) or php_empty(lambda : post["ID"]):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post ID.")))
    # end if
    if (php_isset(lambda : post["post_type"])) and "revision" == post["post_type"]:
        return php_new_class("WP_Error", lambda : WP_Error("post_type", __("Cannot create a revision of a revision")))
    # end if
    post = _wp_post_revision_data(post, autosave)
    post = wp_slash(post)
    #// Since data is from DB.
    revision_id = wp_insert_post(post)
    if is_wp_error(revision_id):
        return revision_id
    # end if
    if revision_id:
        #// 
        #// Fires once a revision has been saved.
        #// 
        #// @since 2.6.0
        #// 
        #// @param int $revision_id Post revision ID.
        #//
        do_action("_wp_put_post_revision", revision_id)
    # end if
    return revision_id
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
def wp_get_post_revision(post=None, output=OBJECT, filter="raw", *args_):
    
    revision = get_post(post, OBJECT, filter)
    if (not revision):
        return revision
    # end if
    if "revision" != revision.post_type:
        return None
    # end if
    if OBJECT == output:
        return revision
    elif ARRAY_A == output:
        _revision = get_object_vars(revision)
        return _revision
    elif ARRAY_N == output:
        _revision = php_array_values(get_object_vars(revision))
        return _revision
    # end if
    return revision
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
def wp_restore_post_revision(revision_id=None, fields=None, *args_):
    
    revision = wp_get_post_revision(revision_id, ARRAY_A)
    if (not revision):
        return revision
    # end if
    if (not php_is_array(fields)):
        fields = php_array_keys(_wp_post_revision_fields(revision))
    # end if
    update = Array()
    for field in php_array_intersect(php_array_keys(revision), fields):
        update[field] = revision[field]
    # end for
    if (not update):
        return False
    # end if
    update["ID"] = revision["post_parent"]
    update = wp_slash(update)
    #// Since data is from DB.
    post_id = wp_update_post(update)
    if (not post_id) or is_wp_error(post_id):
        return post_id
    # end if
    #// Update last edit user.
    update_post_meta(post_id, "_edit_last", get_current_user_id())
    #// 
    #// Fires after a post revision has been restored.
    #// 
    #// @since 2.6.0
    #// 
    #// @param int $post_id     Post ID.
    #// @param int $revision_id Post revision ID.
    #//
    do_action("wp_restore_post_revision", post_id, revision["ID"])
    return post_id
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
def wp_delete_post_revision(revision_id=None, *args_):
    
    revision = wp_get_post_revision(revision_id)
    if (not revision):
        return revision
    # end if
    delete = wp_delete_post(revision.ID)
    if delete:
        #// 
        #// Fires once a post revision has been deleted.
        #// 
        #// @since 2.6.0
        #// 
        #// @param int     $revision_id Post revision ID.
        #// @param WP_Post $revision    Post revision object.
        #//
        do_action("wp_delete_post_revision", revision.ID, revision)
    # end if
    return delete
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
def wp_get_post_revisions(post_id=0, args=None, *args_):
    
    post = get_post(post_id)
    if (not post) or php_empty(lambda : post.ID):
        return Array()
    # end if
    defaults = Array({"order": "DESC", "orderby": "date ID", "check_enabled": True})
    args = wp_parse_args(args, defaults)
    if args["check_enabled"] and (not wp_revisions_enabled(post)):
        return Array()
    # end if
    args = php_array_merge(args, Array({"post_parent": post.ID, "post_type": "revision", "post_status": "inherit"}))
    revisions = get_children(args)
    if (not revisions):
        return Array()
    # end if
    return revisions
# end def wp_get_post_revisions
#// 
#// Determine if revisions are enabled for a given post.
#// 
#// @since 3.6.0
#// 
#// @param WP_Post $post The post object.
#// @return bool True if number of revisions to keep isn't zero, false otherwise.
#//
def wp_revisions_enabled(post=None, *args_):
    
    return wp_revisions_to_keep(post) != 0
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
def wp_revisions_to_keep(post=None, *args_):
    
    num = WP_POST_REVISIONS
    if True == num:
        num = -1
    else:
        num = php_intval(num)
    # end if
    if (not post_type_supports(post.post_type, "revisions")):
        num = 0
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
    return int(apply_filters("wp_revisions_to_keep", num, post))
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
def _set_preview(post=None, *args_):
    
    if (not php_is_object(post)):
        return post
    # end if
    preview = wp_get_post_autosave(post.ID)
    if (not php_is_object(preview)):
        return post
    # end if
    preview = sanitize_post(preview)
    post.post_content = preview.post_content
    post.post_title = preview.post_title
    post.post_excerpt = preview.post_excerpt
    add_filter("get_the_terms", "_wp_preview_terms_filter", 10, 3)
    add_filter("get_post_metadata", "_wp_preview_post_thumbnail_filter", 10, 3)
    return post
# end def _set_preview
#// 
#// Filters the latest content for preview from the post autosave.
#// 
#// @since 2.7.0
#// @access private
#//
def _show_post_preview(*args_):
    
    if (php_isset(lambda : PHP_REQUEST["preview_id"])) and (php_isset(lambda : PHP_REQUEST["preview_nonce"])):
        id = int(PHP_REQUEST["preview_id"])
        if False == wp_verify_nonce(PHP_REQUEST["preview_nonce"], "post_preview_" + id):
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
def _wp_preview_terms_filter(terms=None, post_id=None, taxonomy=None, *args_):
    
    post = get_post()
    if (not post):
        return terms
    # end if
    if php_empty(lambda : PHP_REQUEST["post_format"]) or post.ID != post_id or "post_format" != taxonomy or "revision" == post.post_type:
        return terms
    # end if
    if "standard" == PHP_REQUEST["post_format"]:
        terms = Array()
    else:
        term = get_term_by("slug", "post-format-" + sanitize_key(PHP_REQUEST["post_format"]), "post_format")
        if term:
            terms = Array(term)
            pass
        # end if
    # end if
    return terms
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
def _wp_preview_post_thumbnail_filter(value=None, post_id=None, meta_key=None, *args_):
    
    post = get_post()
    if (not post):
        return value
    # end if
    if php_empty(lambda : PHP_REQUEST["_thumbnail_id"]) or php_empty(lambda : PHP_REQUEST["preview_id"]) or post.ID != post_id or "_thumbnail_id" != meta_key or "revision" == post.post_type or post_id != PHP_REQUEST["preview_id"]:
        return value
    # end if
    thumbnail_id = php_intval(PHP_REQUEST["_thumbnail_id"])
    if thumbnail_id <= 0:
        return ""
    # end if
    return php_strval(thumbnail_id)
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
def _wp_get_post_revision_version(revision=None, *args_):
    
    if php_is_object(revision):
        revision = get_object_vars(revision)
    elif (not php_is_array(revision)):
        return False
    # end if
    if php_preg_match("/^\\d+-(?:autosave|revision)-v(\\d+)$/", revision["post_name"], matches):
        return int(matches[1])
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
def _wp_upgrade_revisions_of_post(post=None, revisions=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Add post option exclusively.
    lock = str("revision-upgrade-") + str(post.ID)
    now = time()
    result = wpdb.query(wpdb.prepare(str("INSERT IGNORE INTO `") + str(wpdb.options) + str("` (`option_name`, `option_value`, `autoload`) VALUES (%s, %s, 'no') /* LOCK */"), lock, now))
    if (not result):
        #// If we couldn't get a lock, see how old the previous lock is.
        locked = get_option(lock)
        if (not locked):
            #// Can't write to the lock, and can't read the lock.
            #// Something broken has happened.
            return False
        # end if
        if locked > now - 3600:
            #// Lock is not too old: some other process may be upgrading this post. Bail.
            return False
        # end if
        pass
    # end if
    #// If we could get a lock, re-"add" the option to fire all the correct filters.
    update_option(lock, now)
    reset(revisions)
    add_last = True
    while True:
        this_revision = current(revisions)
        prev_revision = next(revisions)
        this_revision_version = _wp_get_post_revision_version(this_revision)
        #// Something terrible happened.
        if False == this_revision_version:
            continue
        # end if
        #// 1 is the latest revision version, so we're already up to date.
        #// No need to add a copy of the post as latest revision.
        if 0 < this_revision_version:
            add_last = False
            continue
        # end if
        #// Always update the revision version.
        update = Array({"post_name": php_preg_replace("/^(\\d+-(?:autosave|revision))[\\d-]*$/", "$1-v1", this_revision.post_name)})
        #// 
        #// If this revision is the oldest revision of the post, i.e. no $prev_revision,
        #// the correct post_author is probably $post->post_author, but that's only a good guess.
        #// Update the revision version only and Leave the author as-is.
        #//
        if prev_revision:
            prev_revision_version = _wp_get_post_revision_version(prev_revision)
            #// If the previous revision is already up to date, it no longer has the information we need :(
            if prev_revision_version < 1:
                update["post_author"] = prev_revision.post_author
            # end if
        # end if
        #// Upgrade this revision.
        result = wpdb.update(wpdb.posts, update, Array({"ID": this_revision.ID}))
        if result:
            wp_cache_delete(this_revision.ID, "posts")
        # end if
        
        if prev_revision:
            break
        # end if
    # end while
    delete_option(lock)
    #// Add a copy of the post as latest revision.
    if add_last:
        wp_save_post_revision(post.ID)
    # end if
    return True
# end def _wp_upgrade_revisions_of_post
