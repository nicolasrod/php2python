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
#// Core Post API
#// 
#// @package WordPress
#// @subpackage Post
#// 
#// 
#// Post Type registration.
#// 
#// 
#// Creates the initial post types when 'init' action is fired.
#// 
#// See {@see 'init'}.
#// 
#// @since 2.9.0
#//
def create_initial_post_types(*_args_):
    
    
    register_post_type("post", Array({"labels": Array({"name_admin_bar": _x("Post", "add new from admin bar")})}, {"public": True, "_builtin": True, "_edit_link": "post.php?post=%d", "capability_type": "post", "map_meta_cap": True, "menu_position": 5, "menu_icon": "dashicons-admin-post", "hierarchical": False, "rewrite": False, "query_var": False, "delete_with_user": True, "supports": Array("title", "editor", "author", "thumbnail", "excerpt", "trackbacks", "custom-fields", "comments", "revisions", "post-formats"), "show_in_rest": True, "rest_base": "posts", "rest_controller_class": "WP_REST_Posts_Controller"}))
    register_post_type("page", Array({"labels": Array({"name_admin_bar": _x("Page", "add new from admin bar")})}, {"public": True, "publicly_queryable": False, "_builtin": True, "_edit_link": "post.php?post=%d", "capability_type": "page", "map_meta_cap": True, "menu_position": 20, "menu_icon": "dashicons-admin-page", "hierarchical": True, "rewrite": False, "query_var": False, "delete_with_user": True, "supports": Array("title", "editor", "author", "thumbnail", "page-attributes", "custom-fields", "comments", "revisions"), "show_in_rest": True, "rest_base": "pages", "rest_controller_class": "WP_REST_Posts_Controller"}))
    register_post_type("attachment", Array({"labels": Array({"name": _x("Media", "post type general name"), "name_admin_bar": _x("Media", "add new from admin bar"), "add_new": _x("Add New", "add new media"), "edit_item": __("Edit Media"), "view_item": __("View Attachment Page"), "attributes": __("Attachment Attributes")})}, {"public": True, "show_ui": True, "_builtin": True, "_edit_link": "post.php?post=%d", "capability_type": "post", "capabilities": Array({"create_posts": "upload_files"})}, {"map_meta_cap": True, "menu_icon": "dashicons-admin-media", "hierarchical": False, "rewrite": False, "query_var": False, "show_in_nav_menus": False, "delete_with_user": True, "supports": Array("title", "author", "comments"), "show_in_rest": True, "rest_base": "media", "rest_controller_class": "WP_REST_Attachments_Controller"}))
    add_post_type_support("attachment:audio", "thumbnail")
    add_post_type_support("attachment:video", "thumbnail")
    register_post_type("revision", Array({"labels": Array({"name": __("Revisions"), "singular_name": __("Revision")})}, {"public": False, "_builtin": True, "_edit_link": "revision.php?revision=%d", "capability_type": "post", "map_meta_cap": True, "hierarchical": False, "rewrite": False, "query_var": False, "can_export": False, "delete_with_user": True, "supports": Array("author")}))
    register_post_type("nav_menu_item", Array({"labels": Array({"name": __("Navigation Menu Items"), "singular_name": __("Navigation Menu Item")})}, {"public": False, "_builtin": True, "hierarchical": False, "rewrite": False, "delete_with_user": False, "query_var": False}))
    register_post_type("custom_css", Array({"labels": Array({"name": __("Custom CSS"), "singular_name": __("Custom CSS")})}, {"public": False, "hierarchical": False, "rewrite": False, "query_var": False, "delete_with_user": False, "can_export": True, "_builtin": True, "supports": Array("title", "revisions"), "capabilities": Array({"delete_posts": "edit_theme_options", "delete_post": "edit_theme_options", "delete_published_posts": "edit_theme_options", "delete_private_posts": "edit_theme_options", "delete_others_posts": "edit_theme_options", "edit_post": "edit_css", "edit_posts": "edit_css", "edit_others_posts": "edit_css", "edit_published_posts": "edit_css", "read_post": "read", "read_private_posts": "read", "publish_posts": "edit_theme_options"})}))
    register_post_type("customize_changeset", Array({"labels": Array({"name": _x("Changesets", "post type general name"), "singular_name": _x("Changeset", "post type singular name"), "menu_name": _x("Changesets", "admin menu"), "name_admin_bar": _x("Changeset", "add new on admin bar"), "add_new": _x("Add New", "Customize Changeset"), "add_new_item": __("Add New Changeset"), "new_item": __("New Changeset"), "edit_item": __("Edit Changeset"), "view_item": __("View Changeset"), "all_items": __("All Changesets"), "search_items": __("Search Changesets"), "not_found": __("No changesets found."), "not_found_in_trash": __("No changesets found in Trash.")})}, {"public": False, "_builtin": True, "map_meta_cap": True, "hierarchical": False, "rewrite": False, "query_var": False, "can_export": False, "delete_with_user": False, "supports": Array("title", "author"), "capability_type": "customize_changeset", "capabilities": Array({"create_posts": "customize", "delete_others_posts": "customize", "delete_post": "customize", "delete_posts": "customize", "delete_private_posts": "customize", "delete_published_posts": "customize", "edit_others_posts": "customize", "edit_post": "customize", "edit_posts": "customize", "edit_private_posts": "customize", "edit_published_posts": "do_not_allow", "publish_posts": "customize", "read": "read", "read_post": "customize", "read_private_posts": "customize"})}))
    register_post_type("oembed_cache", Array({"labels": Array({"name": __("oEmbed Responses"), "singular_name": __("oEmbed Response")})}, {"public": False, "hierarchical": False, "rewrite": False, "query_var": False, "delete_with_user": False, "can_export": False, "_builtin": True, "supports": Array()}))
    register_post_type("user_request", Array({"labels": Array({"name": __("User Requests"), "singular_name": __("User Request")})}, {"public": False, "_builtin": True, "hierarchical": False, "rewrite": False, "query_var": False, "can_export": False, "delete_with_user": False, "supports": Array()}))
    register_post_type("wp_block", Array({"labels": Array({"name": _x("Blocks", "post type general name"), "singular_name": _x("Block", "post type singular name"), "menu_name": _x("Blocks", "admin menu"), "name_admin_bar": _x("Block", "add new on admin bar"), "add_new": _x("Add New", "Block"), "add_new_item": __("Add New Block"), "new_item": __("New Block"), "edit_item": __("Edit Block"), "view_item": __("View Block"), "all_items": __("All Blocks"), "search_items": __("Search Blocks"), "not_found": __("No blocks found."), "not_found_in_trash": __("No blocks found in Trash."), "filter_items_list": __("Filter blocks list"), "items_list_navigation": __("Blocks list navigation"), "items_list": __("Blocks list"), "item_published": __("Block published."), "item_published_privately": __("Block published privately."), "item_reverted_to_draft": __("Block reverted to draft."), "item_scheduled": __("Block scheduled."), "item_updated": __("Block updated.")})}, {"public": False, "_builtin": True, "show_ui": True, "show_in_menu": False, "rewrite": False, "show_in_rest": True, "rest_base": "blocks", "rest_controller_class": "WP_REST_Blocks_Controller", "capability_type": "block", "capabilities": Array({"read": "edit_posts", "create_posts": "publish_posts", "edit_posts": "edit_posts", "edit_published_posts": "edit_published_posts", "delete_published_posts": "delete_published_posts", "edit_others_posts": "edit_others_posts", "delete_others_posts": "delete_others_posts"})}, {"map_meta_cap": True, "supports": Array("title", "editor")}))
    register_post_status("publish", Array({"label": _x("Published", "post status"), "public": True, "_builtin": True, "label_count": _n_noop("Published <span class=\"count\">(%s)</span>", "Published <span class=\"count\">(%s)</span>")}))
    register_post_status("future", Array({"label": _x("Scheduled", "post status"), "protected": True, "_builtin": True, "label_count": _n_noop("Scheduled <span class=\"count\">(%s)</span>", "Scheduled <span class=\"count\">(%s)</span>")}))
    register_post_status("draft", Array({"label": _x("Draft", "post status"), "protected": True, "_builtin": True, "label_count": _n_noop("Draft <span class=\"count\">(%s)</span>", "Drafts <span class=\"count\">(%s)</span>"), "date_floating": True}))
    register_post_status("pending", Array({"label": _x("Pending", "post status"), "protected": True, "_builtin": True, "label_count": _n_noop("Pending <span class=\"count\">(%s)</span>", "Pending <span class=\"count\">(%s)</span>"), "date_floating": True}))
    register_post_status("private", Array({"label": _x("Private", "post status"), "private": True, "_builtin": True, "label_count": _n_noop("Private <span class=\"count\">(%s)</span>", "Private <span class=\"count\">(%s)</span>")}))
    register_post_status("trash", Array({"label": _x("Trash", "post status"), "internal": True, "_builtin": True, "label_count": _n_noop("Trash <span class=\"count\">(%s)</span>", "Trash <span class=\"count\">(%s)</span>"), "show_in_admin_status_list": True}))
    register_post_status("auto-draft", Array({"label": "auto-draft", "internal": True, "_builtin": True, "date_floating": True}))
    register_post_status("inherit", Array({"label": "inherit", "internal": True, "_builtin": True, "exclude_from_search": False}))
    register_post_status("request-pending", Array({"label": _x("Pending", "request status"), "internal": True, "_builtin": True, "label_count": _n_noop("Pending <span class=\"count\">(%s)</span>", "Pending <span class=\"count\">(%s)</span>"), "exclude_from_search": False}))
    register_post_status("request-confirmed", Array({"label": _x("Confirmed", "request status"), "internal": True, "_builtin": True, "label_count": _n_noop("Confirmed <span class=\"count\">(%s)</span>", "Confirmed <span class=\"count\">(%s)</span>"), "exclude_from_search": False}))
    register_post_status("request-failed", Array({"label": _x("Failed", "request status"), "internal": True, "_builtin": True, "label_count": _n_noop("Failed <span class=\"count\">(%s)</span>", "Failed <span class=\"count\">(%s)</span>"), "exclude_from_search": False}))
    register_post_status("request-completed", Array({"label": _x("Completed", "request status"), "internal": True, "_builtin": True, "label_count": _n_noop("Completed <span class=\"count\">(%s)</span>", "Completed <span class=\"count\">(%s)</span>"), "exclude_from_search": False}))
# end def create_initial_post_types
#// 
#// Retrieve attached file path based on attachment ID.
#// 
#// By default the path will go through the 'get_attached_file' filter, but
#// passing a true to the $unfiltered argument of get_attached_file() will
#// return the file path unfiltered.
#// 
#// The function works by getting the single post meta name, named
#// '_wp_attached_file' and returning it. This is a convenience function to
#// prevent looking up the meta name and provide a mechanism for sending the
#// attached filename through a filter.
#// 
#// @since 2.0.0
#// 
#// @param int  $attachment_id Attachment ID.
#// @param bool $unfiltered    Optional. Whether to apply filters. Default false.
#// @return string|false The file path to where the attached file should be, false otherwise.
#//
def get_attached_file(attachment_id_=None, unfiltered_=None, *_args_):
    if unfiltered_ is None:
        unfiltered_ = False
    # end if
    
    file_ = get_post_meta(attachment_id_, "_wp_attached_file", True)
    #// If the file is relative, prepend upload dir.
    if file_ and 0 != php_strpos(file_, "/") and (not php_preg_match("|^.:\\\\|", file_)):
        uploads_ = wp_get_upload_dir()
        if False == uploads_["error"]:
            file_ = uploads_["basedir"] + str("/") + str(file_)
        # end if
    # end if
    if unfiltered_:
        return file_
    # end if
    #// 
    #// Filters the attached file based on the given ID.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $file          Path to attached file.
    #// @param int    $attachment_id Attachment ID.
    #//
    return apply_filters("get_attached_file", file_, attachment_id_)
# end def get_attached_file
#// 
#// Update attachment file path based on attachment ID.
#// 
#// Used to update the file path of the attachment, which uses post meta name
#// '_wp_attached_file' to store the path of the attachment.
#// 
#// @since 2.1.0
#// 
#// @param int    $attachment_id Attachment ID.
#// @param string $file          File path for the attachment.
#// @return bool True on success, false on failure.
#//
def update_attached_file(attachment_id_=None, file_=None, *_args_):
    
    
    if (not get_post(attachment_id_)):
        return False
    # end if
    #// 
    #// Filters the path to the attached file to update.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $file          Path to the attached file to update.
    #// @param int    $attachment_id Attachment ID.
    #//
    file_ = apply_filters("update_attached_file", file_, attachment_id_)
    file_ = _wp_relative_upload_path(file_)
    if file_:
        return update_post_meta(attachment_id_, "_wp_attached_file", file_)
    else:
        return delete_post_meta(attachment_id_, "_wp_attached_file")
    # end if
# end def update_attached_file
#// 
#// Return relative path to an uploaded file.
#// 
#// The path is relative to the current upload dir.
#// 
#// @since 2.9.0
#// @access private
#// 
#// @param string $path Full path to the file.
#// @return string Relative path on success, unchanged path on failure.
#//
def _wp_relative_upload_path(path_=None, *_args_):
    
    
    new_path_ = path_
    uploads_ = wp_get_upload_dir()
    if 0 == php_strpos(new_path_, uploads_["basedir"]):
        new_path_ = php_str_replace(uploads_["basedir"], "", new_path_)
        new_path_ = php_ltrim(new_path_, "/")
    # end if
    #// 
    #// Filters the relative path to an uploaded file.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $new_path Relative path to the file.
    #// @param string $path     Full path to the file.
    #//
    return apply_filters("_wp_relative_upload_path", new_path_, path_)
# end def _wp_relative_upload_path
#// 
#// Retrieve all children of the post parent ID.
#// 
#// Normally, without any enhancements, the children would apply to pages. In the
#// context of the inner workings of WordPress, pages, posts, and attachments
#// share the same table, so therefore the functionality could apply to any one
#// of them. It is then noted that while this function does not work on posts, it
#// does not mean that it won't work on posts. It is recommended that you know
#// what context you wish to retrieve the children of.
#// 
#// Attachments may also be made the child of a post, so if that is an accurate
#// statement (which needs to be verified), it would then be possible to get
#// all of the attachments for a post. Attachments have since changed since
#// version 2.5, so this is most likely inaccurate, but serves generally as an
#// example of what is possible.
#// 
#// The arguments listed as defaults are for this function and also of the
#// get_posts() function. The arguments are combined with the get_children defaults
#// and are then passed to the get_posts() function, which accepts additional arguments.
#// You can replace the defaults in this function, listed below and the additional
#// arguments listed in the get_posts() function.
#// 
#// The 'post_parent' is the most important argument and important attention
#// needs to be paid to the $args parameter. If you pass either an object or an
#// integer (number), then just the 'post_parent' is grabbed and everything else
#// is lost. If you don't specify any arguments, then it is assumed that you are
#// in The Loop and the post parent will be grabbed for from the current post.
#// 
#// The 'post_parent' argument is the ID to get the children. The 'numberposts'
#// is the amount of posts to retrieve that has a default of '-1', which is
#// used to get all of the posts. Giving a number higher than 0 will only
#// retrieve that amount of posts.
#// 
#// The 'post_type' and 'post_status' arguments can be used to choose what
#// criteria of posts to retrieve. The 'post_type' can be anything, but WordPress
#// post types are 'post', 'pages', and 'attachments'. The 'post_status'
#// argument will accept any post status within the write administration panels.
#// 
#// @since 2.0.0
#// 
#// @see get_posts()
#// @todo Check validity of description.
#// 
#// @global WP_Post $post Global post object.
#// 
#// @param mixed  $args   Optional. User defined arguments for replacing the defaults. Default empty.
#// @param string $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Post object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @return WP_Post[]|int[] Array of post objects or post IDs.
#//
def get_children(args_="", output_=None, *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    kids_ = Array()
    if php_empty(lambda : args_):
        if (php_isset(lambda : PHP_GLOBALS["post"])):
            args_ = Array({"post_parent": php_int(PHP_GLOBALS["post"].post_parent)})
        else:
            return kids_
        # end if
    elif php_is_object(args_):
        args_ = Array({"post_parent": php_int(args_.post_parent)})
    elif php_is_numeric(args_):
        args_ = Array({"post_parent": php_int(args_)})
    # end if
    defaults_ = Array({"numberposts": -1, "post_type": "any", "post_status": "any", "post_parent": 0})
    parsed_args_ = wp_parse_args(args_, defaults_)
    children_ = get_posts(parsed_args_)
    if (not children_):
        return kids_
    # end if
    if (not php_empty(lambda : parsed_args_["fields"])):
        return children_
    # end if
    update_post_cache(children_)
    for key_,child_ in children_.items():
        kids_[child_.ID] = children_[key_]
    # end for
    if OBJECT == output_:
        return kids_
    elif ARRAY_A == output_:
        weeuns_ = Array()
        for kid_ in kids_:
            weeuns_[kid_.ID] = get_object_vars(kids_[kid_.ID])
        # end for
        return weeuns_
    elif ARRAY_N == output_:
        babes_ = Array()
        for kid_ in kids_:
            babes_[kid_.ID] = php_array_values(get_object_vars(kids_[kid_.ID]))
        # end for
        return babes_
    else:
        return kids_
    # end if
# end def get_children
#// 
#// Get extended entry info (<!--more-->).
#// 
#// There should not be any space after the second dash and before the word
#// 'more'. There can be text or space(s) after the word 'more', but won't be
#// referenced.
#// 
#// The returned array has 'main', 'extended', and 'more_text' keys. Main has the text before
#// the `<!--more-->`. The 'extended' key has the content after the
#// `<!--more-->` comment. The 'more_text' key has the custom "Read More" text.
#// 
#// @since 1.0.0
#// 
#// @param string $post Post content.
#// @return string[] {
#// Extended entry info.
#// 
#// @type string $main      Content before the more tag.
#// @type string $extended  Content after the more tag.
#// @type string $more_text Custom read more text, or empty string.
#// }
#//
def get_extended(post_=None, *_args_):
    
    
    #// Match the new style more links.
    if php_preg_match("/<!--more(.*?)?-->/", post_, matches_):
        main_, extended_ = php_explode(matches_[0], post_, 2)
        more_text_ = matches_[1]
    else:
        main_ = post_
        extended_ = ""
        more_text_ = ""
    # end if
    #// Leading and trailing whitespace.
    main_ = php_preg_replace("/^[\\s]*(.*)[\\s]*$/", "\\1", main_)
    extended_ = php_preg_replace("/^[\\s]*(.*)[\\s]*$/", "\\1", extended_)
    more_text_ = php_preg_replace("/^[\\s]*(.*)[\\s]*$/", "\\1", more_text_)
    return Array({"main": main_, "extended": extended_, "more_text": more_text_})
# end def get_extended
#// 
#// Retrieves post data given a post ID or post object.
#// 
#// See sanitize_post() for optional $filter values. Also, the parameter
#// `$post`, must be given as a variable, since it is passed by reference.
#// 
#// @since 1.5.1
#// 
#// @global WP_Post $post Global post object.
#// 
#// @param int|WP_Post|null $post   Optional. Post ID or post object. Defaults to global $post.
#// @param string           $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Post object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string           $filter Optional. Type of filter to apply. Accepts 'raw', 'edit', 'db',
#// or 'display'. Default 'raw'.
#// @return WP_Post|array|null Type corresponding to $output on success or null on failure.
#// When $output is OBJECT, a `WP_Post` instance is returned.
#//
def get_post(post_=None, output_=None, filter_="raw", *_args_):
    if post_ is None:
        post_ = None
    # end if
    if output_ is None:
        output_ = OBJECT
    # end if
    
    if php_empty(lambda : post_) and (php_isset(lambda : PHP_GLOBALS["post"])):
        post_ = PHP_GLOBALS["post"]
    # end if
    if type(post_).__name__ == "WP_Post":
        _post_ = post_
    elif php_is_object(post_):
        if php_empty(lambda : post_.filter):
            _post_ = sanitize_post(post_, "raw")
            _post_ = php_new_class("WP_Post", lambda : WP_Post(_post_))
        elif "raw" == post_.filter:
            _post_ = php_new_class("WP_Post", lambda : WP_Post(post_))
        else:
            _post_ = WP_Post.get_instance(post_.ID)
        # end if
    else:
        _post_ = WP_Post.get_instance(post_)
    # end if
    if (not _post_):
        return None
    # end if
    _post_ = _post_.filter(filter_)
    if ARRAY_A == output_:
        return _post_.to_array()
    elif ARRAY_N == output_:
        return php_array_values(_post_.to_array())
    # end if
    return _post_
# end def get_post
#// 
#// Retrieve ancestors of a post.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Post $post Post ID or post object.
#// @return int[] Ancestor IDs or empty array if none are found.
#//
def get_post_ancestors(post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_) or php_empty(lambda : post_.post_parent) or post_.post_parent == post_.ID:
        return Array()
    # end if
    ancestors_ = Array()
    id_ = post_.post_parent
    ancestors_[-1] = id_
    while True:
        ancestor_ = get_post(id_)
        if not (ancestor_):
            break
        # end if
        #// Loop detection: If the ancestor has been seen before, break.
        if php_empty(lambda : ancestor_.post_parent) or ancestor_.post_parent == post_.ID or php_in_array(ancestor_.post_parent, ancestors_):
            break
        # end if
        id_ = ancestor_.post_parent
        ancestors_[-1] = id_
    # end while
    return ancestors_
# end def get_post_ancestors
#// 
#// Retrieve data from a post field based on Post ID.
#// 
#// Examples of the post field will be, 'post_type', 'post_status', 'post_content',
#// etc and based off of the post object property or key names.
#// 
#// The context values are based off of the taxonomy filter functions and
#// supported values are found within those functions.
#// 
#// @since 2.3.0
#// @since 4.5.0 The `$post` parameter was made optional.
#// 
#// @see sanitize_post_field()
#// 
#// @param string      $field   Post field name.
#// @param int|WP_Post $post    Optional. Post ID or post object. Defaults to global $post.
#// @param string      $context Optional. How to filter the field. Accepts 'raw', 'edit', 'db',
#// or 'display'. Default 'display'.
#// @return string The value of the post field on success, empty string on failure.
#//
def get_post_field(field_=None, post_=None, context_="display", *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return ""
    # end if
    if (not (php_isset(lambda : post_.field_))):
        return ""
    # end if
    return sanitize_post_field(field_, post_.field_, post_.ID, context_)
# end def get_post_field
#// 
#// Retrieve the mime type of an attachment based on the ID.
#// 
#// This function can be used with any post type, but it makes more sense with
#// attachments.
#// 
#// @since 2.0.0
#// 
#// @param int|WP_Post $post Optional. Post ID or post object. Defaults to global $post.
#// @return string|false The mime type on success, false on failure.
#//
def get_post_mime_type(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if php_is_object(post_):
        return post_.post_mime_type
    # end if
    return False
# end def get_post_mime_type
#// 
#// Retrieve the post status based on the post ID.
#// 
#// If the post ID is of an attachment, then the parent post status will be given
#// instead.
#// 
#// @since 2.0.0
#// 
#// @param int|WP_Post $post Optional. Post ID or post object. Defaults to global $post..
#// @return string|false Post status on success, false on failure.
#//
def get_post_status(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not php_is_object(post_)):
        return False
    # end if
    if "attachment" == post_.post_type:
        if "private" == post_.post_status:
            return "private"
        # end if
        #// Unattached attachments are assumed to be published.
        if "inherit" == post_.post_status and 0 == post_.post_parent:
            return "publish"
        # end if
        #// Inherit status from the parent.
        if post_.post_parent and post_.ID != post_.post_parent:
            parent_post_status_ = get_post_status(post_.post_parent)
            if "trash" == parent_post_status_:
                return get_post_meta(post_.post_parent, "_wp_trash_meta_status", True)
            else:
                return parent_post_status_
            # end if
        # end if
    # end if
    #// 
    #// Filters the post status.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string  $post_status The post status.
    #// @param WP_Post $post        The post object.
    #//
    return apply_filters("get_post_status", post_.post_status, post_)
# end def get_post_status
#// 
#// Retrieve all of the WordPress supported post statuses.
#// 
#// Posts have a limited set of valid status values, this provides the
#// post_status values and descriptions.
#// 
#// @since 2.5.0
#// 
#// @return string[] Array of post status labels keyed by their status.
#//
def get_post_statuses(*_args_):
    
    
    status_ = Array({"draft": __("Draft"), "pending": __("Pending Review"), "private": __("Private"), "publish": __("Published")})
    return status_
# end def get_post_statuses
#// 
#// Retrieve all of the WordPress support page statuses.
#// 
#// Pages have a limited set of valid status values, this provides the
#// post_status values and descriptions.
#// 
#// @since 2.5.0
#// 
#// @return string[] Array of page status labels keyed by their status.
#//
def get_page_statuses(*_args_):
    
    
    status_ = Array({"draft": __("Draft"), "private": __("Private"), "publish": __("Published")})
    return status_
# end def get_page_statuses
#// 
#// Return statuses for privacy requests.
#// 
#// @since 4.9.6
#// @access private
#// 
#// @return array
#//
def _wp_privacy_statuses(*_args_):
    
    
    return Array({"request-pending": __("Pending"), "request-confirmed": __("Confirmed"), "request-failed": __("Failed"), "request-completed": __("Completed")})
# end def _wp_privacy_statuses
#// 
#// Register a post status. Do not use before init.
#// 
#// A simple function for creating or modifying a post status based on the
#// parameters given. The function will accept an array (second optional
#// parameter), along with a string for the post status name.
#// 
#// Arguments prefixed with an _underscore shouldn't be used by plugins and themes.
#// 
#// @since 3.0.0
#// @global array $wp_post_statuses Inserts new post status object into the list
#// 
#// @param string $post_status Name of the post status.
#// @param array|string $args {
#// Optional. Array or string of post status arguments.
#// 
#// @type bool|string $label                     A descriptive name for the post status marked
#// for translation. Defaults to value of $post_status.
#// @type bool|array  $label_count               Descriptive text to use for nooped plurals.
#// Default array of $label, twice.
#// @type bool        $exclude_from_search       Whether to exclude posts with this post status
#// from search results. Default is value of $internal.
#// @type bool        $_builtin                  Whether the status is built-in. Core-use only.
#// Default false.
#// @type bool        $public                    Whether posts of this status should be shown
#// in the front end of the site. Default false.
#// @type bool        $internal                  Whether the status is for internal use only.
#// Default false.
#// @type bool        $protected                 Whether posts with this status should be protected.
#// Default false.
#// @type bool        $private                   Whether posts with this status should be private.
#// Default false.
#// @type bool        $publicly_queryable        Whether posts with this status should be publicly-
#// queryable. Default is value of $public.
#// @type bool        $show_in_admin_all_list    Whether to include posts in the edit listing for
#// their post type. Default is the opposite value
#// of $internal.
#// @type bool        $show_in_admin_status_list Show in the list of statuses with post counts at
#// the top of the edit listings,
#// e.g. All (12) | Published (9) | My Custom Status (2)
#// Default is the opposite value of $internal.
#// @type bool        $date_floating             Whether the post has a floating creation date.
#// Default to false.
#// }
#// @return object
#//
def register_post_status(post_status_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_post_statuses_
    php_check_if_defined("wp_post_statuses_")
    if (not php_is_array(wp_post_statuses_)):
        wp_post_statuses_ = Array()
    # end if
    #// Args prefixed with an underscore are reserved for internal use.
    defaults_ = Array({"label": False, "label_count": False, "exclude_from_search": None, "_builtin": False, "public": None, "internal": None, "protected": None, "private": None, "publicly_queryable": None, "show_in_admin_status_list": None, "show_in_admin_all_list": None, "date_floating": None})
    args_ = wp_parse_args(args_, defaults_)
    args_ = args_
    post_status_ = sanitize_key(post_status_)
    args_.name = post_status_
    #// Set various defaults.
    if None == args_.public and None == args_.internal and None == args_.protected and None == args_.private:
        args_.internal = True
    # end if
    if None == args_.public:
        args_.public = False
    # end if
    if None == args_.private:
        args_.private = False
    # end if
    if None == args_.protected:
        args_.protected = False
    # end if
    if None == args_.internal:
        args_.internal = False
    # end if
    if None == args_.publicly_queryable:
        args_.publicly_queryable = args_.public
    # end if
    if None == args_.exclude_from_search:
        args_.exclude_from_search = args_.internal
    # end if
    if None == args_.show_in_admin_all_list:
        args_.show_in_admin_all_list = (not args_.internal)
    # end if
    if None == args_.show_in_admin_status_list:
        args_.show_in_admin_status_list = (not args_.internal)
    # end if
    if None == args_.date_floating:
        args_.date_floating = False
    # end if
    if False == args_.label:
        args_.label = post_status_
    # end if
    if False == args_.label_count:
        #// phpcs:ignore WordPress.WP.I18n.NonSingularStringLiteralSingle,WordPress.WP.I18n.NonSingularStringLiteralPlural
        args_.label_count = _n_noop(args_.label, args_.label)
    # end if
    wp_post_statuses_[post_status_] = args_
    return args_
# end def register_post_status
#// 
#// Retrieve a post status object by name.
#// 
#// @since 3.0.0
#// 
#// @global array $wp_post_statuses List of post statuses.
#// 
#// @see register_post_status()
#// 
#// @param string $post_status The name of a registered post status.
#// @return object|null A post status object.
#//
def get_post_status_object(post_status_=None, *_args_):
    
    
    global wp_post_statuses_
    php_check_if_defined("wp_post_statuses_")
    if php_empty(lambda : wp_post_statuses_[post_status_]):
        return None
    # end if
    return wp_post_statuses_[post_status_]
# end def get_post_status_object
#// 
#// Get a list of post statuses.
#// 
#// @since 3.0.0
#// 
#// @global array $wp_post_statuses List of post statuses.
#// 
#// @see register_post_status()
#// 
#// @param array|string $args     Optional. Array or string of post status arguments to compare against
#// properties of the global `$wp_post_statuses objects`. Default empty array.
#// @param string       $output   Optional. The type of output to return, either 'names' or 'objects'. Default 'names'.
#// @param string       $operator Optional. The logical operation to perform. 'or' means only one element
#// from the array needs to match; 'and' means all elements must match.
#// Default 'and'.
#// @return array A list of post status names or objects.
#//
def get_post_stati(args_=None, output_="names", operator_="and", *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_post_statuses_
    php_check_if_defined("wp_post_statuses_")
    field_ = "name" if "names" == output_ else False
    return wp_filter_object_list(wp_post_statuses_, args_, operator_, field_)
# end def get_post_stati
#// 
#// Whether the post type is hierarchical.
#// 
#// A false return value might also mean that the post type does not exist.
#// 
#// @since 3.0.0
#// 
#// @see get_post_type_object()
#// 
#// @param string $post_type Post type name
#// @return bool Whether post type is hierarchical.
#//
def is_post_type_hierarchical(post_type_=None, *_args_):
    
    
    if (not post_type_exists(post_type_)):
        return False
    # end if
    post_type_ = get_post_type_object(post_type_)
    return post_type_.hierarchical
# end def is_post_type_hierarchical
#// 
#// Determines whether a post type is registered.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.0.0
#// 
#// @see get_post_type_object()
#// 
#// @param string $post_type Post type name.
#// @return bool Whether post type is registered.
#//
def post_type_exists(post_type_=None, *_args_):
    
    
    return php_bool(get_post_type_object(post_type_))
# end def post_type_exists
#// 
#// Retrieves the post type of the current post or of a given post.
#// 
#// @since 2.1.0
#// 
#// @param int|WP_Post|null $post Optional. Post ID or post object. Default is global $post.
#// @return string|false          Post type on success, false on failure.
#//
def get_post_type(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if post_:
        return post_.post_type
    # end if
    return False
# end def get_post_type
#// 
#// Retrieves a post type object by name.
#// 
#// @since 3.0.0
#// @since 4.6.0 Object returned is now an instance of `WP_Post_Type`.
#// 
#// @global array $wp_post_types List of post types.
#// 
#// @see register_post_type()
#// 
#// @param string $post_type The name of a registered post type.
#// @return WP_Post_Type|null WP_Post_Type object if it exists, null otherwise.
#//
def get_post_type_object(post_type_=None, *_args_):
    
    
    global wp_post_types_
    php_check_if_defined("wp_post_types_")
    if (not php_is_scalar(post_type_)) or php_empty(lambda : wp_post_types_[post_type_]):
        return None
    # end if
    return wp_post_types_[post_type_]
# end def get_post_type_object
#// 
#// Get a list of all registered post type objects.
#// 
#// @since 2.9.0
#// 
#// @global array $wp_post_types List of post types.
#// 
#// @see register_post_type() for accepted arguments.
#// 
#// @param array|string $args     Optional. An array of key => value arguments to match against
#// the post type objects. Default empty array.
#// @param string       $output   Optional. The type of output to return. Accepts post type 'names'
#// or 'objects'. Default 'names'.
#// @param string       $operator Optional. The logical operation to perform. 'or' means only one
#// element from the array needs to match; 'and' means all elements
#// must match; 'not' means no elements may match. Default 'and'.
#// @return string[]|WP_Post_Type[] An array of post type names or objects.
#//
def get_post_types(args_=None, output_="names", operator_="and", *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_post_types_
    php_check_if_defined("wp_post_types_")
    field_ = "name" if "names" == output_ else False
    return wp_filter_object_list(wp_post_types_, args_, operator_, field_)
# end def get_post_types
#// 
#// Registers a post type.
#// 
#// Note: Post type registrations should not be hooked before the
#// {@see 'init'} action. Also, any taxonomy connections should be
#// registered via the `$taxonomies` argument to ensure consistency
#// when hooks such as {@see 'parse_query'} or {@see 'pre_get_posts'}
#// are used.
#// 
#// Post types can support any number of built-in core features such
#// as meta boxes, custom fields, post thumbnails, post statuses,
#// comments, and more. See the `$supports` argument for a complete
#// list of supported features.
#// 
#// @since 2.9.0
#// @since 3.0.0 The `show_ui` argument is now enforced on the new post screen.
#// @since 4.4.0 The `show_ui` argument is now enforced on the post type listing
#// screen and post editing screen.
#// @since 4.6.0 Post type object returned is now an instance of `WP_Post_Type`.
#// @since 4.7.0 Introduced `show_in_rest`, `rest_base` and `rest_controller_class`
#// arguments to register the post type in REST API.
#// @since 5.3.0 The `supports` argument will now accept an array of arguments for a feature.
#// .
#// @global array $wp_post_types List of post types.
#// 
#// @param string $post_type Post type key. Must not exceed 20 characters and may
#// only contain lowercase alphanumeric characters, dashes,
#// and underscores. See sanitize_key().
#// @param array|string $args {
#// Array or string of arguments for registering a post type.
#// 
#// @type string      $label                 Name of the post type shown in the menu. Usually plural.
#// Default is value of $labels['name'].
#// @type array       $labels                An array of labels for this post type. If not set, post
#// labels are inherited for non-hierarchical types and page
#// labels for hierarchical ones. See get_post_type_labels() for a full
#// list of supported labels.
#// @type string      $description           A short descriptive summary of what the post type is.
#// Default empty.
#// @type bool        $public                Whether a post type is intended for use publicly either via
#// the admin interface or by front-end users. While the default
#// settings of $exclude_from_search, $publicly_queryable, $show_ui,
#// and $show_in_nav_menus are inherited from public, each does not
#// rely on this relationship and controls a very specific intention.
#// Default false.
#// @type bool        $hierarchical          Whether the post type is hierarchical (e.g. page). Default false.
#// @type bool        $exclude_from_search   Whether to exclude posts with this post type from front end search
#// results. Default is the opposite value of $public.
#// @type bool        $publicly_queryable    Whether queries can be performed on the front end for the post type
#// as part of parse_request(). Endpoints would include:
#// ?post_type={post_type_key}
#// ?{post_type_key}={single_post_slug}
#// ?{post_type_query_var}={single_post_slug}
#// If not set, the default is inherited from $public.
#// @type bool        $show_ui               Whether to generate and allow a UI for managing this post type in the
#// admin. Default is value of $public.
#// @type bool|string $show_in_menu          Where to show the post type in the admin menu. To work, $show_ui
#// must be true. If true, the post type is shown in its own top level
#// menu. If false, no menu is shown. If a string of an existing top
#// level menu (eg. 'tools.php' or 'edit.php?post_type=page'), the post
#// type will be placed as a sub-menu of that.
#// Default is value of $show_ui.
#// @type bool        $show_in_nav_menus     Makes this post type available for selection in navigation menus.
#// Default is value of $public.
#// @type bool        $show_in_admin_bar     Makes this post type available via the admin bar. Default is value
#// of $show_in_menu.
#// @type bool        $show_in_rest          Whether to include the post type in the REST API. Set this to true
#// for the post type to be available in the block editor.
#// @type string      $rest_base             To change the base url of REST API route. Default is $post_type.
#// @type string      $rest_controller_class REST API Controller class name. Default is 'WP_REST_Posts_Controller'.
#// @type int         $menu_position         The position in the menu order the post type should appear. To work,
#// $show_in_menu must be true. Default null (at the bottom).
#// @type string      $menu_icon             The url to the icon to be used for this menu. Pass a base64-encoded
#// SVG using a data URI, which will be colored to match the color scheme
#// -- this should begin with 'data:image/svg+xml;base64,'. Pass the name
#// of a Dashicons helper class to use a font icon, e.g.
#// 'dashicons-chart-pie'. Pass 'none' to leave div.wp-menu-image empty
#// so an icon can be added via CSS. Defaults to use the posts icon.
#// @type string      $capability_type       The string to use to build the read, edit, and delete capabilities.
#// May be passed as an array to allow for alternative plurals when using
#// this argument as a base to construct the capabilities, e.g.
#// array('story', 'stories'). Default 'post'.
#// @type array       $capabilities          Array of capabilities for this post type. $capability_type is used
#// as a base to construct capabilities by default.
#// See get_post_type_capabilities().
#// @type bool        $map_meta_cap          Whether to use the internal default meta capability handling.
#// Default false.
#// @type array       $supports              Core feature(s) the post type supports. Serves as an alias for calling
#// add_post_type_support() directly. Core features include 'title',
#// 'editor', 'comments', 'revisions', 'trackbacks', 'author', 'excerpt',
#// 'page-attributes', 'thumbnail', 'custom-fields', and 'post-formats'.
#// Additionally, the 'revisions' feature dictates whether the post type
#// will store revisions, and the 'comments' feature dictates whether the
#// comments count will show on the edit screen. A feature can also be
#// specified as an array of arguments to provide additional information
#// about supporting that feature. Example: `array( 'my_feature', array(
#// 'field' => 'value' ) )`. Default is an array containing 'title' and
#// 'editor'.
#// @type callable    $register_meta_box_cb  Provide a callback function that sets up the meta boxes for the
#// edit form. Do remove_meta_box() and add_meta_box() calls in the
#// callback. Default null.
#// @type array       $taxonomies            An array of taxonomy identifiers that will be registered for the
#// post type. Taxonomies can be registered later with register_taxonomy()
#// or register_taxonomy_for_object_type().
#// Default empty array.
#// @type bool|string $has_archive           Whether there should be post type archives, or if a string, the
#// archive slug to use. Will generate the proper rewrite rules if
#// $rewrite is enabled. Default false.
#// @type bool|array  $rewrite              {
#// Triggers the handling of rewrites for this post type. To prevent rewrite, set to false.
#// Defaults to true, using $post_type as slug. To specify rewrite rules, an array can be
#// passed with any of these keys:
#// 
#// @type string $slug       Customize the permastruct slug. Defaults to $post_type key.
#// @type bool   $with_front Whether the permastruct should be prepended with WP_Rewrite::$front.
#// Default true.
#// @type bool   $feeds      Whether the feed permastruct should be built for this post type.
#// Default is value of $has_archive.
#// @type bool   $pages      Whether the permastruct should provide for pagination. Default true.
#// @type const  $ep_mask    Endpoint mask to assign. If not specified and permalink_epmask is set,
#// inherits from $permalink_epmask. If not specified and permalink_epmask
#// is not set, defaults to EP_PERMALINK.
#// }
#// @type string|bool $query_var             Sets the query_var key for this post type. Defaults to $post_type
#// key. If false, a post type cannot be loaded at
#// ?{query_var}={post_slug}. If specified as a string, the query
#// ?{query_var_string}={post_slug} will be valid.
#// @type bool        $can_export            Whether to allow this post type to be exported. Default true.
#// @type bool        $delete_with_user      Whether to delete posts of this type when deleting a user. If true,
#// posts of this type belonging to the user will be moved to Trash
#// when then user is deleted. If false, posts of this type belonging
#// to the user will *not* be trashed or deleted. If not set (the default),
#// posts are trashed if post_type_supports('author'). Otherwise posts
#// are not trashed or deleted. Default null.
#// @type bool        $_builtin              FOR INTERNAL USE ONLY! True if this post type is a native or
#// "built-in" post_type. Default false.
#// @type string      $_edit_link            FOR INTERNAL USE ONLY! URL segment to use for edit link of
#// this post type. Default 'post.php?post=%d'.
#// }
#// @return WP_Post_Type|WP_Error The registered post type object on success,
#// WP_Error object on failure.
#//
def register_post_type(post_type_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_post_types_
    php_check_if_defined("wp_post_types_")
    if (not php_is_array(wp_post_types_)):
        wp_post_types_ = Array()
    # end if
    #// Sanitize post type name.
    post_type_ = sanitize_key(post_type_)
    if php_empty(lambda : post_type_) or php_strlen(post_type_) > 20:
        _doing_it_wrong(inspect.currentframe().f_code.co_name, __("Post type names must be between 1 and 20 characters in length."), "4.2.0")
        return php_new_class("WP_Error", lambda : WP_Error("post_type_length_invalid", __("Post type names must be between 1 and 20 characters in length.")))
    # end if
    post_type_object_ = php_new_class("WP_Post_Type", lambda : WP_Post_Type(post_type_, args_))
    post_type_object_.add_supports()
    post_type_object_.add_rewrite_rules()
    post_type_object_.register_meta_boxes()
    wp_post_types_[post_type_] = post_type_object_
    post_type_object_.add_hooks()
    post_type_object_.register_taxonomies()
    #// 
    #// Fires after a post type is registered.
    #// 
    #// @since 3.3.0
    #// @since 4.6.0 Converted the `$post_type` parameter to accept a `WP_Post_Type` object.
    #// 
    #// @param string       $post_type        Post type.
    #// @param WP_Post_Type $post_type_object Arguments used to register the post type.
    #//
    do_action("registered_post_type", post_type_, post_type_object_)
    return post_type_object_
# end def register_post_type
#// 
#// Unregisters a post type.
#// 
#// Can not be used to unregister built-in post types.
#// 
#// @since 4.5.0
#// 
#// @global array $wp_post_types List of post types.
#// 
#// @param string $post_type Post type to unregister.
#// @return bool|WP_Error True on success, WP_Error on failure or if the post type doesn't exist.
#//
def unregister_post_type(post_type_=None, *_args_):
    
    
    global wp_post_types_
    php_check_if_defined("wp_post_types_")
    if (not post_type_exists(post_type_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post_type", __("Invalid post type.")))
    # end if
    post_type_object_ = get_post_type_object(post_type_)
    #// Do not allow unregistering internal post types.
    if post_type_object_._builtin:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post_type", __("Unregistering a built-in post type is not allowed")))
    # end if
    post_type_object_.remove_supports()
    post_type_object_.remove_rewrite_rules()
    post_type_object_.unregister_meta_boxes()
    post_type_object_.remove_hooks()
    post_type_object_.unregister_taxonomies()
    wp_post_types_[post_type_] = None
    #// 
    #// Fires after a post type was unregistered.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $post_type Post type key.
    #//
    do_action("unregistered_post_type", post_type_)
    return True
# end def unregister_post_type
#// 
#// Build an object with all post type capabilities out of a post type object
#// 
#// Post type capabilities use the 'capability_type' argument as a base, if the
#// capability is not set in the 'capabilities' argument array or if the
#// 'capabilities' argument is not supplied.
#// 
#// The capability_type argument can optionally be registered as an array, with
#// the first value being singular and the second plural, e.g. array('story, 'stories')
#// Otherwise, an 's' will be added to the value for the plural form. After
#// registration, capability_type will always be a string of the singular value.
#// 
#// By default, eight keys are accepted as part of the capabilities array:
#// 
#// - edit_post, read_post, and delete_post are meta capabilities, which are then
#// generally mapped to corresponding primitive capabilities depending on the
#// context, which would be the post being edited/read/deleted and the user or
#// role being checked. Thus these capabilities would generally not be granted
#// directly to users or roles.
#// 
#// - edit_posts - Controls whether objects of this post type can be edited.
#// - edit_others_posts - Controls whether objects of this type owned by other users
#// can be edited. If the post type does not support an author, then this will
#// behave like edit_posts.
#// - delete_posts - Controls whether objects of this post type can be deleted.
#// - publish_posts - Controls publishing objects of this post type.
#// - read_private_posts - Controls whether private objects can be read.
#// 
#// These five primitive capabilities are checked in core in various locations.
#// There are also six other primitive capabilities which are not referenced
#// directly in core, except in map_meta_cap(), which takes the three aforementioned
#// meta capabilities and translates them into one or more primitive capabilities
#// that must then be checked against the user or role, depending on the context.
#// 
#// - read - Controls whether objects of this post type can be read.
#// - delete_private_posts - Controls whether private objects can be deleted.
#// - delete_published_posts - Controls whether published objects can be deleted.
#// - delete_others_posts - Controls whether objects owned by other users can be
#// can be deleted. If the post type does not support an author, then this will
#// behave like delete_posts.
#// - edit_private_posts - Controls whether private objects can be edited.
#// - edit_published_posts - Controls whether published objects can be edited.
#// 
#// These additional capabilities are only used in map_meta_cap(). Thus, they are
#// only assigned by default if the post type is registered with the 'map_meta_cap'
#// argument set to true (default is false).
#// 
#// @since 3.0.0
#// @since 5.4.0 'delete_posts' is included in default capabilities.
#// 
#// @see register_post_type()
#// @see map_meta_cap()
#// 
#// @param object $args Post type registration arguments.
#// @return object Object with all the capabilities as member variables.
#//
def get_post_type_capabilities(args_=None, *_args_):
    
    
    if (not php_is_array(args_.capability_type)):
        args_.capability_type = Array(args_.capability_type, args_.capability_type + "s")
    # end if
    #// Singular base for meta capabilities, plural base for primitive capabilities.
    singular_base_, plural_base_ = args_.capability_type
    default_capabilities_ = Array({"edit_post": "edit_" + singular_base_, "read_post": "read_" + singular_base_, "delete_post": "delete_" + singular_base_, "edit_posts": "edit_" + plural_base_, "edit_others_posts": "edit_others_" + plural_base_, "delete_posts": "delete_" + plural_base_, "publish_posts": "publish_" + plural_base_, "read_private_posts": "read_private_" + plural_base_})
    #// Primitive capabilities used within map_meta_cap():
    if args_.map_meta_cap:
        default_capabilities_for_mapping_ = Array({"read": "read", "delete_private_posts": "delete_private_" + plural_base_, "delete_published_posts": "delete_published_" + plural_base_, "delete_others_posts": "delete_others_" + plural_base_, "edit_private_posts": "edit_private_" + plural_base_, "edit_published_posts": "edit_published_" + plural_base_})
        default_capabilities_ = php_array_merge(default_capabilities_, default_capabilities_for_mapping_)
    # end if
    capabilities_ = php_array_merge(default_capabilities_, args_.capabilities)
    #// Post creation capability simply maps to edit_posts by default:
    if (not (php_isset(lambda : capabilities_["create_posts"]))):
        capabilities_["create_posts"] = capabilities_["edit_posts"]
    # end if
    #// Remember meta capabilities for future reference.
    if args_.map_meta_cap:
        _post_type_meta_capabilities(capabilities_)
    # end if
    return capabilities_
# end def get_post_type_capabilities
#// 
#// Store or return a list of post type meta caps for map_meta_cap().
#// 
#// @since 3.1.0
#// @access private
#// 
#// @global array $post_type_meta_caps Used to store meta capabilities.
#// 
#// @param string[] $capabilities Post type meta capabilities.
#//
def _post_type_meta_capabilities(capabilities_=None, *_args_):
    if capabilities_ is None:
        capabilities_ = None
    # end if
    
    global post_type_meta_caps_
    php_check_if_defined("post_type_meta_caps_")
    for core_,custom_ in capabilities_.items():
        if php_in_array(core_, Array("read_post", "delete_post", "edit_post")):
            post_type_meta_caps_[custom_] = core_
        # end if
    # end for
# end def _post_type_meta_capabilities
#// 
#// Builds an object with all post type labels out of a post type object.
#// 
#// Accepted keys of the label array in the post type object:
#// 
#// - `name` - General name for the post type, usually plural. The same and overridden
#// by `$post_type_object->label`. Default is 'Posts' / 'Pages'.
#// - `singular_name` - Name for one object of this post type. Default is 'Post' / 'Page'.
#// - `add_new` - Default is 'Add New' for both hierarchical and non-hierarchical types.
#// When internationalizing this string, please use a {@link https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/#disambiguation-by-context gettext context}
#// matching your post type. Example: `_x( 'Add New', 'product', 'textdomain' );`.
#// - `add_new_item` - Label for adding a new singular item. Default is 'Add New Post' / 'Add New Page'.
#// - `edit_item` - Label for editing a singular item. Default is 'Edit Post' / 'Edit Page'.
#// - `new_item` - Label for the new item page title. Default is 'New Post' / 'New Page'.
#// - `view_item` - Label for viewing a singular item. Default is 'View Post' / 'View Page'.
#// - `view_items` - Label for viewing post type archives. Default is 'View Posts' / 'View Pages'.
#// - `search_items` - Label for searching plural items. Default is 'Search Posts' / 'Search Pages'.
#// - `not_found` - Label used when no items are found. Default is 'No posts found' / 'No pages found'.
#// - `not_found_in_trash` - Label used when no items are in the Trash. Default is 'No posts found in Trash'
#// 'No pages found in Trash'.
#// - `parent_item_colon` - Label used to prefix parents of hierarchical items. Not used on non-hierarchical
#// post types. Default is 'Parent Page:'.
#// - `all_items` - Label to signify all items in a submenu link. Default is 'All Posts' / 'All Pages'.
#// - `archives` - Label for archives in nav menus. Default is 'Post Archives' / 'Page Archives'.
#// - `attributes` - Label for the attributes meta box. Default is 'Post Attributes' / 'Page Attributes'.
#// - `insert_into_item` - Label for the media frame button. Default is 'Insert into post' / 'Insert into page'.
#// - `uploaded_to_this_item` - Label for the media frame filter. Default is 'Uploaded to this post'
#// 'Uploaded to this page'.
#// - `featured_image` - Label for the featured image meta box title. Default is 'Featured image'.
#// - `set_featured_image` - Label for setting the featured image. Default is 'Set featured image'.
#// - `remove_featured_image` - Label for removing the featured image. Default is 'Remove featured image'.
#// - `use_featured_image` - Label in the media frame for using a featured image. Default is 'Use as featured image'.
#// - `menu_name` - Label for the menu name. Default is the same as `name`.
#// - `filter_items_list` - Label for the table views hidden heading. Default is 'Filter posts list'
#// 'Filter pages list'.
#// - `items_list_navigation` - Label for the table pagination hidden heading. Default is 'Posts list navigation'
#// 'Pages list navigation'.
#// - `items_list` - Label for the table hidden heading. Default is 'Posts list' / 'Pages list'.
#// - `item_published` - Label used when an item is published. Default is 'Post published.' / 'Page published.'
#// - `item_published_privately` - Label used when an item is published with private visibility.
#// Default is 'Post published privately.' / 'Page published privately.'
#// - `item_reverted_to_draft` - Label used when an item is switched to a draft.
#// Default is 'Post reverted to draft.' / 'Page reverted to draft.'
#// - `item_scheduled` - Label used when an item is scheduled for publishing. Default is 'Post scheduled.'
#// 'Page scheduled.'
#// - `item_updated` - Label used when an item is updated. Default is 'Post updated.' / 'Page updated.'
#// 
#// Above, the first default value is for non-hierarchical post types (like posts)
#// and the second one is for hierarchical post types (like pages).
#// 
#// Note: To set labels used in post type admin notices, see the {@see 'post_updated_messages'} filter.
#// 
#// @since 3.0.0
#// @since 4.3.0 Added the `featured_image`, `set_featured_image`, `remove_featured_image`,
#// and `use_featured_image` labels.
#// @since 4.4.0 Added the `archives`, `insert_into_item`, `uploaded_to_this_item`, `filter_items_list`,
#// `items_list_navigation`, and `items_list` labels.
#// @since 4.6.0 Converted the `$post_type` parameter to accept a `WP_Post_Type` object.
#// @since 4.7.0 Added the `view_items` and `attributes` labels.
#// @since 5.0.0 Added the `item_published`, `item_published_privately`, `item_reverted_to_draft`,
#// `item_scheduled`, and `item_updated` labels.
#// 
#// @access private
#// 
#// @param object|WP_Post_Type $post_type_object Post type object.
#// @return object Object with all the labels as member variables.
#//
def get_post_type_labels(post_type_object_=None, *_args_):
    
    
    nohier_vs_hier_defaults_ = Array({"name": Array(_x("Posts", "post type general name"), _x("Pages", "post type general name")), "singular_name": Array(_x("Post", "post type singular name"), _x("Page", "post type singular name")), "add_new": Array(_x("Add New", "post"), _x("Add New", "page")), "add_new_item": Array(__("Add New Post"), __("Add New Page")), "edit_item": Array(__("Edit Post"), __("Edit Page")), "new_item": Array(__("New Post"), __("New Page")), "view_item": Array(__("View Post"), __("View Page")), "view_items": Array(__("View Posts"), __("View Pages")), "search_items": Array(__("Search Posts"), __("Search Pages")), "not_found": Array(__("No posts found."), __("No pages found.")), "not_found_in_trash": Array(__("No posts found in Trash."), __("No pages found in Trash.")), "parent_item_colon": Array(None, __("Parent Page:")), "all_items": Array(__("All Posts"), __("All Pages")), "archives": Array(__("Post Archives"), __("Page Archives")), "attributes": Array(__("Post Attributes"), __("Page Attributes")), "insert_into_item": Array(__("Insert into post"), __("Insert into page")), "uploaded_to_this_item": Array(__("Uploaded to this post"), __("Uploaded to this page")), "featured_image": Array(_x("Featured image", "post"), _x("Featured image", "page")), "set_featured_image": Array(_x("Set featured image", "post"), _x("Set featured image", "page")), "remove_featured_image": Array(_x("Remove featured image", "post"), _x("Remove featured image", "page")), "use_featured_image": Array(_x("Use as featured image", "post"), _x("Use as featured image", "page")), "filter_items_list": Array(__("Filter posts list"), __("Filter pages list")), "items_list_navigation": Array(__("Posts list navigation"), __("Pages list navigation")), "items_list": Array(__("Posts list"), __("Pages list")), "item_published": Array(__("Post published."), __("Page published.")), "item_published_privately": Array(__("Post published privately."), __("Page published privately.")), "item_reverted_to_draft": Array(__("Post reverted to draft."), __("Page reverted to draft.")), "item_scheduled": Array(__("Post scheduled."), __("Page scheduled.")), "item_updated": Array(__("Post updated."), __("Page updated."))})
    nohier_vs_hier_defaults_["menu_name"] = nohier_vs_hier_defaults_["name"]
    labels_ = _get_custom_object_labels(post_type_object_, nohier_vs_hier_defaults_)
    post_type_ = post_type_object_.name
    default_labels_ = copy.deepcopy(labels_)
    #// 
    #// Filters the labels of a specific post type.
    #// 
    #// The dynamic portion of the hook name, `$post_type`, refers to
    #// the post type slug.
    #// 
    #// @since 3.5.0
    #// 
    #// @see get_post_type_labels() for the full list of labels.
    #// 
    #// @param object $labels Object with labels for the post type as member variables.
    #//
    labels_ = apply_filters(str("post_type_labels_") + str(post_type_), labels_)
    #// Ensure that the filtered labels contain all required default values.
    labels_ = php_array_merge(default_labels_, labels_)
    return labels_
# end def get_post_type_labels
#// 
#// Build an object with custom-something object (post type, taxonomy) labels
#// out of a custom-something object
#// 
#// @since 3.0.0
#// @access private
#// 
#// @param object $object                  A custom-something object.
#// @param array  $nohier_vs_hier_defaults Hierarchical vs non-hierarchical default labels.
#// @return object Object containing labels for the given custom-something object.
#//
def _get_custom_object_labels(object_=None, nohier_vs_hier_defaults_=None, *_args_):
    
    
    object_.labels = object_.labels
    if (php_isset(lambda : object_.label)) and php_empty(lambda : object_.labels["name"]):
        object_.labels["name"] = object_.label
    # end if
    if (not (php_isset(lambda : object_.labels["singular_name"]))) and (php_isset(lambda : object_.labels["name"])):
        object_.labels["singular_name"] = object_.labels["name"]
    # end if
    if (not (php_isset(lambda : object_.labels["name_admin_bar"]))):
        object_.labels["name_admin_bar"] = object_.labels["singular_name"] if (php_isset(lambda : object_.labels["singular_name"])) else object_.name
    # end if
    if (not (php_isset(lambda : object_.labels["menu_name"]))) and (php_isset(lambda : object_.labels["name"])):
        object_.labels["menu_name"] = object_.labels["name"]
    # end if
    if (not (php_isset(lambda : object_.labels["all_items"]))) and (php_isset(lambda : object_.labels["menu_name"])):
        object_.labels["all_items"] = object_.labels["menu_name"]
    # end if
    if (not (php_isset(lambda : object_.labels["archives"]))) and (php_isset(lambda : object_.labels["all_items"])):
        object_.labels["archives"] = object_.labels["all_items"]
    # end if
    defaults_ = Array()
    for key_,value_ in nohier_vs_hier_defaults_.items():
        defaults_[key_] = value_[1] if object_.hierarchical else value_[0]
    # end for
    labels_ = php_array_merge(defaults_, object_.labels)
    object_.labels = object_.labels
    return labels_
# end def _get_custom_object_labels
#// 
#// Add submenus for post types.
#// 
#// @access private
#// @since 3.1.0
#//
def _add_post_type_submenus(*_args_):
    
    
    for ptype_ in get_post_types(Array({"show_ui": True})):
        ptype_obj_ = get_post_type_object(ptype_)
        #// Sub-menus only.
        if (not ptype_obj_.show_in_menu) or True == ptype_obj_.show_in_menu:
            continue
        # end if
        add_submenu_page(ptype_obj_.show_in_menu, ptype_obj_.labels.name, ptype_obj_.labels.all_items, ptype_obj_.cap.edit_posts, str("edit.php?post_type=") + str(ptype_))
    # end for
# end def _add_post_type_submenus
#// 
#// Registers support of certain features for a post type.
#// 
#// All core features are directly associated with a functional area of the edit
#// screen, such as the editor or a meta box. Features include: 'title', 'editor',
#// 'comments', 'revisions', 'trackbacks', 'author', 'excerpt', 'page-attributes',
#// 'thumbnail', 'custom-fields', and 'post-formats'.
#// 
#// Additionally, the 'revisions' feature dictates whether the post type will
#// store revisions, and the 'comments' feature dictates whether the comments
#// count will show on the edit screen.
#// 
#// A third, optional parameter can also be passed along with a feature to provide
#// additional information about supporting that feature.
#// 
#// Example usage:
#// 
#// add_post_type_support( 'my_post_type', 'comments' );
#// add_post_type_support( 'my_post_type', array(
#// 'author', 'excerpt',
#// ) );
#// add_post_type_support( 'my_post_type', 'my_feature', array(
#// 'field' => 'value',
#// ) );
#// 
#// @since 3.0.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @global array $_wp_post_type_features
#// 
#// @param string       $post_type The post type for which to add the feature.
#// @param string|array $feature   The feature being added, accepts an array of
#// feature strings or a single string.
#// @param mixed        ...$args   Optional extra arguments to pass along with certain features.
#//
def add_post_type_support(post_type_=None, feature_=None, *args_):
    
    
    global _wp_post_type_features_
    php_check_if_defined("_wp_post_type_features_")
    features_ = feature_
    for feature_ in features_:
        if args_:
            _wp_post_type_features_[post_type_][feature_] = args_
        else:
            _wp_post_type_features_[post_type_][feature_] = True
        # end if
    # end for
# end def add_post_type_support
#// 
#// Remove support for a feature from a post type.
#// 
#// @since 3.0.0
#// 
#// @global array $_wp_post_type_features
#// 
#// @param string $post_type The post type for which to remove the feature.
#// @param string $feature   The feature being removed.
#//
def remove_post_type_support(post_type_=None, feature_=None, *_args_):
    
    
    global _wp_post_type_features_
    php_check_if_defined("_wp_post_type_features_")
    _wp_post_type_features_[post_type_][feature_] = None
# end def remove_post_type_support
#// 
#// Get all the post type features
#// 
#// @since 3.4.0
#// 
#// @global array $_wp_post_type_features
#// 
#// @param string $post_type The post type.
#// @return array Post type supports list.
#//
def get_all_post_type_supports(post_type_=None, *_args_):
    
    
    global _wp_post_type_features_
    php_check_if_defined("_wp_post_type_features_")
    if (php_isset(lambda : _wp_post_type_features_[post_type_])):
        return _wp_post_type_features_[post_type_]
    # end if
    return Array()
# end def get_all_post_type_supports
#// 
#// Check a post type's support for a given feature.
#// 
#// @since 3.0.0
#// 
#// @global array $_wp_post_type_features
#// 
#// @param string $post_type The post type being checked.
#// @param string $feature   The feature being checked.
#// @return bool Whether the post type supports the given feature.
#//
def post_type_supports(post_type_=None, feature_=None, *_args_):
    
    
    global _wp_post_type_features_
    php_check_if_defined("_wp_post_type_features_")
    return (php_isset(lambda : _wp_post_type_features_[post_type_][feature_]))
# end def post_type_supports
#// 
#// Retrieves a list of post type names that support a specific feature.
#// 
#// @since 4.5.0
#// 
#// @global array $_wp_post_type_features Post type features
#// 
#// @param array|string $feature  Single feature or an array of features the post types should support.
#// @param string       $operator Optional. The logical operation to perform. 'or' means
#// only one element from the array needs to match; 'and'
#// means all elements must match; 'not' means no elements may
#// match. Default 'and'.
#// @return string[] A list of post type names.
#//
def get_post_types_by_support(feature_=None, operator_="and", *_args_):
    
    
    global _wp_post_type_features_
    php_check_if_defined("_wp_post_type_features_")
    features_ = php_array_fill_keys(feature_, True)
    return php_array_keys(wp_filter_object_list(_wp_post_type_features_, features_, operator_))
# end def get_post_types_by_support
#// 
#// Update the post type for the post ID.
#// 
#// The page or post cache will be cleaned for the post ID.
#// 
#// @since 2.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $post_id   Optional. Post ID to change post type. Default 0.
#// @param string $post_type Optional. Post type. Accepts 'post' or 'page' to
#// name a few. Default 'post'.
#// @return int|false Amount of rows changed. Should be 1 for success and 0 for failure.
#//
def set_post_type(post_id_=0, post_type_="post", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_type_ = sanitize_post_field("post_type", post_type_, post_id_, "db")
    return_ = wpdb_.update(wpdb_.posts, Array({"post_type": post_type_}), Array({"ID": post_id_}))
    clean_post_cache(post_id_)
    return return_
# end def set_post_type
#// 
#// Determines whether a post type is considered "viewable".
#// 
#// For built-in post types such as posts and pages, the 'public' value will be evaluated.
#// For all others, the 'publicly_queryable' value will be used.
#// 
#// @since 4.4.0
#// @since 4.5.0 Added the ability to pass a post type name in addition to object.
#// @since 4.6.0 Converted the `$post_type` parameter to accept a `WP_Post_Type` object.
#// 
#// @param string|WP_Post_Type $post_type Post type name or object.
#// @return bool Whether the post type should be considered viewable.
#//
def is_post_type_viewable(post_type_=None, *_args_):
    
    
    if php_is_scalar(post_type_):
        post_type_ = get_post_type_object(post_type_)
        if (not post_type_):
            return False
        # end if
    # end if
    return post_type_.publicly_queryable or post_type_._builtin and post_type_.public
# end def is_post_type_viewable
#// 
#// Retrieves an array of the latest posts, or posts matching the given criteria.
#// 
#// The defaults are as follows:
#// 
#// @since 1.2.0
#// 
#// @see WP_Query::parse_query()
#// 
#// @param array $args {
#// Optional. Arguments to retrieve posts. See WP_Query::parse_query() for all
#// available arguments.
#// 
#// @type int        $numberposts      Total number of posts to retrieve. Is an alias of $posts_per_page
#// in WP_Query. Accepts -1 for all. Default 5.
#// @type int|string $category         Category ID or comma-separated list of IDs (this or any children).
#// Is an alias of $cat in WP_Query. Default 0.
#// @type array      $include          An array of post IDs to retrieve, sticky posts will be included.
#// Is an alias of $post__in in WP_Query. Default empty array.
#// @type array      $exclude          An array of post IDs not to retrieve. Default empty array.
#// @type bool       $suppress_filters Whether to suppress filters. Default true.
#// }
#// @return WP_Post[]|int[] Array of post objects or post IDs.
#//
def get_posts(args_=None, *_args_):
    if args_ is None:
        args_ = None
    # end if
    
    defaults_ = Array({"numberposts": 5, "category": 0, "orderby": "date", "order": "DESC", "include": Array(), "exclude": Array(), "meta_key": "", "meta_value": "", "post_type": "post", "suppress_filters": True})
    parsed_args_ = wp_parse_args(args_, defaults_)
    if php_empty(lambda : parsed_args_["post_status"]):
        parsed_args_["post_status"] = "inherit" if "attachment" == parsed_args_["post_type"] else "publish"
    # end if
    if (not php_empty(lambda : parsed_args_["numberposts"])) and php_empty(lambda : parsed_args_["posts_per_page"]):
        parsed_args_["posts_per_page"] = parsed_args_["numberposts"]
    # end if
    if (not php_empty(lambda : parsed_args_["category"])):
        parsed_args_["cat"] = parsed_args_["category"]
    # end if
    if (not php_empty(lambda : parsed_args_["include"])):
        incposts_ = wp_parse_id_list(parsed_args_["include"])
        parsed_args_["posts_per_page"] = php_count(incposts_)
        #// Only the number of posts included.
        parsed_args_["post__in"] = incposts_
    elif (not php_empty(lambda : parsed_args_["exclude"])):
        parsed_args_["post__not_in"] = wp_parse_id_list(parsed_args_["exclude"])
    # end if
    parsed_args_["ignore_sticky_posts"] = True
    parsed_args_["no_found_rows"] = True
    get_posts_ = php_new_class("WP_Query", lambda : WP_Query())
    return get_posts_.query(parsed_args_)
# end def get_posts
#// 
#// Post meta functions.
#// 
#// 
#// Adds a meta field to the given post.
#// 
#// Post meta data is called "Custom Fields" on the Administration Screen.
#// 
#// @since 1.5.0
#// 
#// @param int    $post_id    Post ID.
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Metadata value. Must be serializable if non-scalar.
#// @param bool   $unique     Optional. Whether the same key should not be added.
#// Default false.
#// @return int|false Meta ID on success, false on failure.
#//
def add_post_meta(post_id_=None, meta_key_=None, meta_value_=None, unique_=None, *_args_):
    if unique_ is None:
        unique_ = False
    # end if
    
    #// Make sure meta is added to the post, not a revision.
    the_post_ = wp_is_post_revision(post_id_)
    if the_post_:
        post_id_ = the_post_
    # end if
    return add_metadata("post", post_id_, meta_key_, meta_value_, unique_)
# end def add_post_meta
#// 
#// Deletes a post meta field for the given post ID.
#// 
#// You can match based on the key, or key and value. Removing based on key and
#// value, will keep from removing duplicate metadata with the same key. It also
#// allows removing all metadata matching the key, if needed.
#// 
#// @since 1.5.0
#// 
#// @param int    $post_id    Post ID.
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Optional. Metadata value. Must be serializable if
#// non-scalar. Default empty.
#// @return bool True on success, false on failure.
#//
def delete_post_meta(post_id_=None, meta_key_=None, meta_value_="", *_args_):
    
    
    #// Make sure meta is added to the post, not a revision.
    the_post_ = wp_is_post_revision(post_id_)
    if the_post_:
        post_id_ = the_post_
    # end if
    return delete_metadata("post", post_id_, meta_key_, meta_value_)
# end def delete_post_meta
#// 
#// Retrieves a post meta field for the given post ID.
#// 
#// @since 1.5.0
#// 
#// @param int    $post_id Post ID.
#// @param string $key     Optional. The meta key to retrieve. By default, returns
#// data for all keys. Default empty.
#// @param bool   $single  Optional. If true, returns only the first value for the specified meta key.
#// This parameter has no effect if $key is not specified. Default false.
#// @return mixed Will be an array if $single is false. Will be value of the meta
#// field if $single is true.
#//
def get_post_meta(post_id_=None, key_="", single_=None, *_args_):
    if single_ is None:
        single_ = False
    # end if
    
    return get_metadata("post", post_id_, key_, single_)
# end def get_post_meta
#// 
#// Updates a post meta field based on the given post ID.
#// 
#// Use the `$prev_value` parameter to differentiate between meta fields with the
#// same key and post ID.
#// 
#// If the meta field for the post does not exist, it will be added and its ID returned.
#// 
#// Can be used in place of add_post_meta().
#// 
#// @since 1.5.0
#// 
#// @param int    $post_id    Post ID.
#// @param string $meta_key   Metadata key.
#// @param mixed  $meta_value Metadata value. Must be serializable if non-scalar.
#// @param mixed  $prev_value Optional. Previous value to check before updating.
#// @return int|bool The new meta field ID if a field with the given key didn't exist and was
#// therefore added, true on successful update, false on failure.
#//
def update_post_meta(post_id_=None, meta_key_=None, meta_value_=None, prev_value_="", *_args_):
    
    
    #// Make sure meta is added to the post, not a revision.
    the_post_ = wp_is_post_revision(post_id_)
    if the_post_:
        post_id_ = the_post_
    # end if
    return update_metadata("post", post_id_, meta_key_, meta_value_, prev_value_)
# end def update_post_meta
#// 
#// Deletes everything from post meta matching the given meta key.
#// 
#// @since 2.3.0
#// 
#// @param string $post_meta_key Key to search for when deleting.
#// @return bool Whether the post meta key was deleted from the database.
#//
def delete_post_meta_by_key(post_meta_key_=None, *_args_):
    
    
    return delete_metadata("post", None, post_meta_key_, "", True)
# end def delete_post_meta_by_key
#// 
#// Registers a meta key for posts.
#// 
#// @since 4.9.8
#// 
#// @param string $post_type Post type to register a meta key for. Pass an empty string
#// to register the meta key across all existing post types.
#// @param string $meta_key  The meta key to register.
#// @param array  $args      Data used to describe the meta key when registered. See
#// {@see register_meta()} for a list of supported arguments.
#// @return bool True if the meta key was successfully registered, false if not.
#//
def register_post_meta(post_type_=None, meta_key_=None, args_=None, *_args_):
    
    
    args_["object_subtype"] = post_type_
    return register_meta("post", meta_key_, args_)
# end def register_post_meta
#// 
#// Unregisters a meta key for posts.
#// 
#// @since 4.9.8
#// 
#// @param string $post_type Post type the meta key is currently registered for. Pass
#// an empty string if the meta key is registered across all
#// existing post types.
#// @param string $meta_key  The meta key to unregister.
#// @return bool True on success, false if the meta key was not previously registered.
#//
def unregister_post_meta(post_type_=None, meta_key_=None, *_args_):
    
    
    return unregister_meta_key("post", meta_key_, post_type_)
# end def unregister_post_meta
#// 
#// Retrieve post meta fields, based on post ID.
#// 
#// The post meta fields are retrieved from the cache where possible,
#// so the function is optimized to be called more than once.
#// 
#// @since 1.2.0
#// 
#// @param int $post_id Optional. Post ID. Default is ID of the global $post.
#// @return array Post meta for the given post.
#//
def get_post_custom(post_id_=0, *_args_):
    
    
    post_id_ = absint(post_id_)
    if (not post_id_):
        post_id_ = get_the_ID()
    # end if
    return get_post_meta(post_id_)
# end def get_post_custom
#// 
#// Retrieve meta field names for a post.
#// 
#// If there are no meta fields, then nothing (null) will be returned.
#// 
#// @since 1.2.0
#// 
#// @param int $post_id Optional. Post ID. Default is ID of the global $post.
#// @return array|void Array of the keys, if retrieved.
#//
def get_post_custom_keys(post_id_=0, *_args_):
    
    
    custom_ = get_post_custom(post_id_)
    if (not php_is_array(custom_)):
        return
    # end if
    keys_ = php_array_keys(custom_)
    if keys_:
        return keys_
    # end if
# end def get_post_custom_keys
#// 
#// Retrieve values for a custom post field.
#// 
#// The parameters must not be considered optional. All of the post meta fields
#// will be retrieved and only the meta field key values returned.
#// 
#// @since 1.2.0
#// 
#// @param string $key     Optional. Meta field key. Default empty.
#// @param int    $post_id Optional. Post ID. Default is ID of the global $post.
#// @return array|null Meta field values.
#//
def get_post_custom_values(key_="", post_id_=0, *_args_):
    
    
    if (not key_):
        return None
    # end if
    custom_ = get_post_custom(post_id_)
    return custom_[key_] if (php_isset(lambda : custom_[key_])) else None
# end def get_post_custom_values
#// 
#// Determines whether a post is sticky.
#// 
#// Sticky posts should remain at the top of The Loop. If the post ID is not
#// given, then The Loop ID for the current post will be used.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.7.0
#// 
#// @param int $post_id Optional. Post ID. Default is ID of the global $post.
#// @return bool Whether post is sticky.
#//
def is_sticky(post_id_=0, *_args_):
    
    
    post_id_ = absint(post_id_)
    if (not post_id_):
        post_id_ = get_the_ID()
    # end if
    stickies_ = get_option("sticky_posts")
    is_sticky_ = php_is_array(stickies_) and php_in_array(post_id_, stickies_)
    #// 
    #// Filters whether a post is sticky.
    #// 
    #// @since 5.3.0
    #// 
    #// @param bool $is_sticky Whether a post is sticky.
    #// @param int  $post_id   Post ID.
    #//
    return apply_filters("is_sticky", is_sticky_, post_id_)
# end def is_sticky
#// 
#// Sanitize every post field.
#// 
#// If the context is 'raw', then the post object or array will get minimal
#// sanitization of the integer fields.
#// 
#// @since 2.3.0
#// 
#// @see sanitize_post_field()
#// 
#// @param object|WP_Post|array $post    The Post Object or Array
#// @param string               $context Optional. How to sanitize post fields.
#// Accepts 'raw', 'edit', 'db', or 'display'.
#// Default 'display'.
#// @return object|WP_Post|array The now sanitized Post Object or Array (will be the
#// same type as $post).
#//
def sanitize_post(post_=None, context_="display", *_args_):
    
    
    if php_is_object(post_):
        #// Check if post already filtered for this context.
        if (php_isset(lambda : post_.filter)) and context_ == post_.filter:
            return post_
        # end if
        if (not (php_isset(lambda : post_.ID))):
            post_.ID = 0
        # end if
        for field_ in php_array_keys(get_object_vars(post_)):
            post_.field_ = sanitize_post_field(field_, post_.field_, post_.ID, context_)
        # end for
        post_.filter = context_
    elif php_is_array(post_):
        #// Check if post already filtered for this context.
        if (php_isset(lambda : post_["filter"])) and context_ == post_["filter"]:
            return post_
        # end if
        if (not (php_isset(lambda : post_["ID"]))):
            post_["ID"] = 0
        # end if
        for field_ in php_array_keys(post_):
            post_[field_] = sanitize_post_field(field_, post_[field_], post_["ID"], context_)
        # end for
        post_["filter"] = context_
    # end if
    return post_
# end def sanitize_post
#// 
#// Sanitize post field based on context.
#// 
#// Possible context values are:  'raw', 'edit', 'db', 'display', 'attribute' and
#// 'js'. The 'display' context is used by default. 'attribute' and 'js' contexts
#// are treated like 'display' when calling filters.
#// 
#// @since 2.3.0
#// @since 4.4.0 Like `sanitize_post()`, `$context` defaults to 'display'.
#// 
#// @param string $field   The Post Object field name.
#// @param mixed  $value   The Post Object value.
#// @param int    $post_id Post ID.
#// @param string $context Optional. How to sanitize post fields. Looks for 'raw', 'edit',
#// 'db', 'display', 'attribute' and 'js'. Default 'display'.
#// @return mixed Sanitized value.
#//
def sanitize_post_field(field_=None, value_=None, post_id_=None, context_="display", *_args_):
    
    
    int_fields_ = Array("ID", "post_parent", "menu_order")
    if php_in_array(field_, int_fields_):
        value_ = php_int(value_)
    # end if
    #// Fields which contain arrays of integers.
    array_int_fields_ = Array("ancestors")
    if php_in_array(field_, array_int_fields_):
        value_ = php_array_map("absint", value_)
        return value_
    # end if
    if "raw" == context_:
        return value_
    # end if
    prefixed_ = False
    if False != php_strpos(field_, "post_"):
        prefixed_ = True
        field_no_prefix_ = php_str_replace("post_", "", field_)
    # end if
    if "edit" == context_:
        format_to_edit_ = Array("post_content", "post_excerpt", "post_title", "post_password")
        if prefixed_:
            #// 
            #// Filters the value of a specific post field to edit.
            #// 
            #// The dynamic portion of the hook name, `$field`, refers to the post
            #// field name.
            #// 
            #// @since 2.3.0
            #// 
            #// @param mixed $value   Value of the post field.
            #// @param int   $post_id Post ID.
            #//
            value_ = apply_filters(str("edit_") + str(field_), value_, post_id_)
            #// 
            #// Filters the value of a specific post field to edit.
            #// 
            #// The dynamic portion of the hook name, `$field_no_prefix`, refers to
            #// the post field name.
            #// 
            #// @since 2.3.0
            #// 
            #// @param mixed $value   Value of the post field.
            #// @param int   $post_id Post ID.
            #//
            value_ = apply_filters(str(field_no_prefix_) + str("_edit_pre"), value_, post_id_)
        else:
            value_ = apply_filters(str("edit_post_") + str(field_), value_, post_id_)
        # end if
        if php_in_array(field_, format_to_edit_):
            if "post_content" == field_:
                value_ = format_to_edit(value_, user_can_richedit())
            else:
                value_ = format_to_edit(value_)
            # end if
        else:
            value_ = esc_attr(value_)
        # end if
    elif "db" == context_:
        if prefixed_:
            #// 
            #// Filters the value of a specific post field before saving.
            #// 
            #// The dynamic portion of the hook name, `$field`, refers to the post
            #// field name.
            #// 
            #// @since 2.3.0
            #// 
            #// @param mixed $value Value of the post field.
            #//
            value_ = apply_filters(str("pre_") + str(field_), value_)
            #// 
            #// Filters the value of a specific field before saving.
            #// 
            #// The dynamic portion of the hook name, `$field_no_prefix`, refers
            #// to the post field name.
            #// 
            #// @since 2.3.0
            #// 
            #// @param mixed $value Value of the post field.
            #//
            value_ = apply_filters(str(field_no_prefix_) + str("_save_pre"), value_)
        else:
            value_ = apply_filters(str("pre_post_") + str(field_), value_)
            #// 
            #// Filters the value of a specific post field before saving.
            #// 
            #// The dynamic portion of the hook name, `$field`, refers to the post
            #// field name.
            #// 
            #// @since 2.3.0
            #// 
            #// @param mixed $value Value of the post field.
            #//
            value_ = apply_filters(str(field_) + str("_pre"), value_)
        # end if
    else:
        #// Use display filters by default.
        if prefixed_:
            #// 
            #// Filters the value of a specific post field for display.
            #// 
            #// The dynamic portion of the hook name, `$field`, refers to the post
            #// field name.
            #// 
            #// @since 2.3.0
            #// 
            #// @param mixed  $value   Value of the prefixed post field.
            #// @param int    $post_id Post ID.
            #// @param string $context Context for how to sanitize the field. Possible
            #// values include 'raw', 'edit', 'db', 'display',
            #// 'attribute' and 'js'.
            #//
            value_ = apply_filters(str(field_), value_, post_id_, context_)
        else:
            value_ = apply_filters(str("post_") + str(field_), value_, post_id_, context_)
        # end if
        if "attribute" == context_:
            value_ = esc_attr(value_)
        elif "js" == context_:
            value_ = esc_js(value_)
        # end if
    # end if
    return value_
# end def sanitize_post_field
#// 
#// Make a post sticky.
#// 
#// Sticky posts should be displayed at the top of the front page.
#// 
#// @since 2.7.0
#// 
#// @param int $post_id Post ID.
#//
def stick_post(post_id_=None, *_args_):
    
    
    stickies_ = get_option("sticky_posts")
    if (not php_is_array(stickies_)):
        stickies_ = Array(post_id_)
    # end if
    if (not php_in_array(post_id_, stickies_)):
        stickies_[-1] = post_id_
    # end if
    updated_ = update_option("sticky_posts", stickies_)
    if updated_:
        #// 
        #// Fires once a post has been added to the sticky list.
        #// 
        #// @since 4.6.0
        #// 
        #// @param int $post_id ID of the post that was stuck.
        #//
        do_action("post_stuck", post_id_)
    # end if
# end def stick_post
#// 
#// Un-stick a post.
#// 
#// Sticky posts should be displayed at the top of the front page.
#// 
#// @since 2.7.0
#// 
#// @param int $post_id Post ID.
#//
def unstick_post(post_id_=None, *_args_):
    
    
    stickies_ = get_option("sticky_posts")
    if (not php_is_array(stickies_)):
        return
    # end if
    if (not php_in_array(post_id_, stickies_)):
        return
    # end if
    offset_ = php_array_search(post_id_, stickies_)
    if False == offset_:
        return
    # end if
    array_splice(stickies_, offset_, 1)
    updated_ = update_option("sticky_posts", stickies_)
    if updated_:
        #// 
        #// Fires once a post has been removed from the sticky list.
        #// 
        #// @since 4.6.0
        #// 
        #// @param int $post_id ID of the post that was unstuck.
        #//
        do_action("post_unstuck", post_id_)
    # end if
# end def unstick_post
#// 
#// Return the cache key for wp_count_posts() based on the passed arguments.
#// 
#// @since 3.9.0
#// @access private
#// 
#// @param string $type Optional. Post type to retrieve count Default 'post'.
#// @param string $perm Optional. 'readable' or empty. Default empty.
#// @return string The cache key.
#//
def _count_posts_cache_key(type_="post", perm_="", *_args_):
    
    
    cache_key_ = "posts-" + type_
    if "readable" == perm_ and is_user_logged_in():
        post_type_object_ = get_post_type_object(type_)
        if post_type_object_ and (not current_user_can(post_type_object_.cap.read_private_posts)):
            cache_key_ += "_" + perm_ + "_" + get_current_user_id()
        # end if
    # end if
    return cache_key_
# end def _count_posts_cache_key
#// 
#// Count number of posts of a post type and if user has permissions to view.
#// 
#// This function provides an efficient method of finding the amount of post's
#// type a blog has. Another method is to count the amount of items in
#// get_posts(), but that method has a lot of overhead with doing so. Therefore,
#// when developing for 2.5+, use this function instead.
#// 
#// The $perm parameter checks for 'readable' value and if the user can read
#// private posts, it will display that for the user that is signed in.
#// 
#// @since 2.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $type Optional. Post type to retrieve count. Default 'post'.
#// @param string $perm Optional. 'readable' or empty. Default empty.
#// @return object Number of posts for each status.
#//
def wp_count_posts(type_="post", perm_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not post_type_exists(type_)):
        return php_new_class("stdClass", lambda : stdClass())
    # end if
    cache_key_ = _count_posts_cache_key(type_, perm_)
    counts_ = wp_cache_get(cache_key_, "counts")
    if False != counts_:
        #// This filter is documented in wp-includes/post.php
        return apply_filters("wp_count_posts", counts_, type_, perm_)
    # end if
    query_ = str("SELECT post_status, COUNT( * ) AS num_posts FROM ") + str(wpdb_.posts) + str(" WHERE post_type = %s")
    if "readable" == perm_ and is_user_logged_in():
        post_type_object_ = get_post_type_object(type_)
        if (not current_user_can(post_type_object_.cap.read_private_posts)):
            query_ += wpdb_.prepare(" AND (post_status != 'private' OR ( post_author = %d AND post_status = 'private' ))", get_current_user_id())
        # end if
    # end if
    query_ += " GROUP BY post_status"
    results_ = wpdb_.get_results(wpdb_.prepare(query_, type_), ARRAY_A)
    counts_ = php_array_fill_keys(get_post_stati(), 0)
    for row_ in results_:
        counts_[row_["post_status"]] = row_["num_posts"]
    # end for
    counts_ = counts_
    wp_cache_set(cache_key_, counts_, "counts")
    #// 
    #// Modify returned post counts by status for the current post type.
    #// 
    #// @since 3.7.0
    #// 
    #// @param object $counts An object containing the current post_type's post
    #// counts by status.
    #// @param string $type   Post type.
    #// @param string $perm   The permission to determine if the posts are 'readable'
    #// by the current user.
    #//
    return apply_filters("wp_count_posts", counts_, type_, perm_)
# end def wp_count_posts
#// 
#// Count number of attachments for the mime type(s).
#// 
#// If you set the optional mime_type parameter, then an array will still be
#// returned, but will only have the item you are looking for. It does not give
#// you the number of attachments that are children of a post. You can get that
#// by counting the number of children that post has.
#// 
#// @since 2.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string|array $mime_type Optional. Array or comma-separated list of
#// MIME patterns. Default empty.
#// @return object An object containing the attachment counts by mime type.
#//
def wp_count_attachments(mime_type_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    and_ = wp_post_mime_type_where(mime_type_)
    count_ = wpdb_.get_results(str("SELECT post_mime_type, COUNT( * ) AS num_posts FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'attachment' AND post_status != 'trash' ") + str(and_) + str(" GROUP BY post_mime_type"), ARRAY_A)
    counts_ = Array()
    for row_ in count_:
        counts_[row_["post_mime_type"]] = row_["num_posts"]
    # end for
    counts_["trash"] = wpdb_.get_var(str("SELECT COUNT( * ) FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'attachment' AND post_status = 'trash' ") + str(and_))
    #// 
    #// Modify returned attachment counts by mime type.
    #// 
    #// @since 3.7.0
    #// 
    #// @param object $counts    An object containing the attachment counts by
    #// mime type.
    #// @param string $mime_type The mime type pattern used to filter the attachments
    #// counted.
    #//
    return apply_filters("wp_count_attachments", counts_, mime_type_)
# end def wp_count_attachments
#// 
#// Get default post mime types.
#// 
#// @since 2.9.0
#// @since 5.3.0 Added the 'Documents', 'Spreadsheets', and 'Archives' mime type groups.
#// 
#// @return array List of post mime types.
#//
def get_post_mime_types(*_args_):
    
    
    post_mime_types_ = Array({"image": Array(__("Images"), __("Manage Images"), _n_noop("Image <span class=\"count\">(%s)</span>", "Images <span class=\"count\">(%s)</span>")), "audio": Array(__("Audio"), __("Manage Audio"), _n_noop("Audio <span class=\"count\">(%s)</span>", "Audio <span class=\"count\">(%s)</span>")), "video": Array(__("Video"), __("Manage Video"), _n_noop("Video <span class=\"count\">(%s)</span>", "Video <span class=\"count\">(%s)</span>")), "document": Array(__("Documents"), __("Manage Documents"), _n_noop("Document <span class=\"count\">(%s)</span>", "Documents <span class=\"count\">(%s)</span>")), "spreadsheet": Array(__("Spreadsheets"), __("Manage Spreadsheets"), _n_noop("Spreadsheet <span class=\"count\">(%s)</span>", "Spreadsheets <span class=\"count\">(%s)</span>")), "archive": Array(_x("Archives", "file type group"), __("Manage Archives"), _n_noop("Archive <span class=\"count\">(%s)</span>", "Archives <span class=\"count\">(%s)</span>"))})
    ext_types_ = wp_get_ext_types()
    mime_types_ = wp_get_mime_types()
    for group_,labels_ in post_mime_types_.items():
        if php_in_array(group_, Array("image", "audio", "video")):
            continue
        # end if
        if (not (php_isset(lambda : ext_types_[group_]))):
            post_mime_types_[group_] = None
            continue
        # end if
        group_mime_types_ = Array()
        for extension_ in ext_types_[group_]:
            for exts_,mime_ in mime_types_.items():
                if php_preg_match("!^(" + exts_ + ")$!i", extension_):
                    group_mime_types_[-1] = mime_
                    break
                # end if
            # end for
        # end for
        group_mime_types_ = php_implode(",", array_unique(group_mime_types_))
        post_mime_types_[group_mime_types_] = labels_
        post_mime_types_[group_] = None
    # end for
    #// 
    #// Filters the default list of post mime types.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $post_mime_types Default list of post mime types.
    #//
    return apply_filters("post_mime_types", post_mime_types_)
# end def get_post_mime_types
#// 
#// Check a MIME-Type against a list.
#// 
#// If the wildcard_mime_types parameter is a string, it must be comma separated
#// list. If the real_mime_types is a string, it is also comma separated to
#// create the list.
#// 
#// @since 2.5.0
#// 
#// @param string|array $wildcard_mime_types Mime types, e.g. audio/mpeg or image (same as image/*)
#// or flash (same as *flash*).
#// @param string|array $real_mime_types     Real post mime type values.
#// @return array array(wildcard=>array(real types)).
#//
def wp_match_mime_types(wildcard_mime_types_=None, real_mime_types_=None, *_args_):
    
    
    matches_ = Array()
    if php_is_string(wildcard_mime_types_):
        wildcard_mime_types_ = php_array_map("trim", php_explode(",", wildcard_mime_types_))
    # end if
    if php_is_string(real_mime_types_):
        real_mime_types_ = php_array_map("trim", php_explode(",", real_mime_types_))
    # end if
    patternses_ = Array()
    wild_ = "[-._a-z0-9]*"
    for type_ in wildcard_mime_types_:
        mimes_ = php_array_map("trim", php_explode(",", type_))
        for mime_ in mimes_:
            regex_ = php_str_replace("__wildcard__", wild_, preg_quote(php_str_replace("*", "__wildcard__", mime_)))
            patternses_[-1][type_] = str("^") + str(regex_) + str("$")
            if False == php_strpos(mime_, "/"):
                patternses_[-1][type_] = str("^") + str(regex_) + str("/")
                patternses_[-1][type_] = regex_
            # end if
        # end for
    # end for
    asort(patternses_)
    for patterns_ in patternses_:
        for type_,pattern_ in patterns_.items():
            for real_ in real_mime_types_:
                if php_preg_match(str("#") + str(pattern_) + str("#"), real_) and php_empty(lambda : matches_[type_]) or False == php_array_search(real_, matches_[type_]):
                    matches_[type_][-1] = real_
                # end if
            # end for
        # end for
    # end for
    return matches_
# end def wp_match_mime_types
#// 
#// Convert MIME types into SQL.
#// 
#// @since 2.5.0
#// 
#// @param string|array $post_mime_types List of mime types or comma separated string
#// of mime types.
#// @param string       $table_alias     Optional. Specify a table alias, if needed.
#// Default empty.
#// @return string The SQL AND clause for mime searching.
#//
def wp_post_mime_type_where(post_mime_types_=None, table_alias_="", *_args_):
    
    
    where_ = ""
    wildcards_ = Array("", "%", "%/%")
    if php_is_string(post_mime_types_):
        post_mime_types_ = php_array_map("trim", php_explode(",", post_mime_types_))
    # end if
    wheres_ = Array()
    for mime_type_ in post_mime_types_:
        mime_type_ = php_preg_replace("/\\s/", "", mime_type_)
        slashpos_ = php_strpos(mime_type_, "/")
        if False != slashpos_:
            mime_group_ = php_preg_replace("/[^-*.a-zA-Z0-9]/", "", php_substr(mime_type_, 0, slashpos_))
            mime_subgroup_ = php_preg_replace("/[^-*.+a-zA-Z0-9]/", "", php_substr(mime_type_, slashpos_ + 1))
            if php_empty(lambda : mime_subgroup_):
                mime_subgroup_ = "*"
            else:
                mime_subgroup_ = php_str_replace("/", "", mime_subgroup_)
            # end if
            mime_pattern_ = str(mime_group_) + str("/") + str(mime_subgroup_)
        else:
            mime_pattern_ = php_preg_replace("/[^-*.a-zA-Z0-9]/", "", mime_type_)
            if False == php_strpos(mime_pattern_, "*"):
                mime_pattern_ += "/*"
            # end if
        # end if
        mime_pattern_ = php_preg_replace("/\\*+/", "%", mime_pattern_)
        if php_in_array(mime_type_, wildcards_):
            return ""
        # end if
        if False != php_strpos(mime_pattern_, "%"):
            wheres_[-1] = str("post_mime_type LIKE '") + str(mime_pattern_) + str("'") if php_empty(lambda : table_alias_) else str(table_alias_) + str(".post_mime_type LIKE '") + str(mime_pattern_) + str("'")
        else:
            wheres_[-1] = str("post_mime_type = '") + str(mime_pattern_) + str("'") if php_empty(lambda : table_alias_) else str(table_alias_) + str(".post_mime_type = '") + str(mime_pattern_) + str("'")
        # end if
    # end for
    if (not php_empty(lambda : wheres_)):
        where_ = " AND (" + php_join(" OR ", wheres_) + ") "
    # end if
    return where_
# end def wp_post_mime_type_where
#// 
#// Trash or delete a post or page.
#// 
#// When the post and page is permanently deleted, everything that is tied to
#// it is deleted also. This includes comments, post meta fields, and terms
#// associated with the post.
#// 
#// The post or page is moved to Trash instead of permanently deleted unless
#// Trash is disabled, item is already in the Trash, or $force_delete is true.
#// 
#// @since 1.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// @see wp_delete_attachment()
#// @see wp_trash_post()
#// 
#// @param int  $postid       Optional. Post ID. Default 0.
#// @param bool $force_delete Optional. Whether to bypass Trash and force deletion.
#// Default false.
#// @return WP_Post|false|null Post data on success, false or null on failure.
#//
def wp_delete_post(postid_=0, force_delete_=None, *_args_):
    if force_delete_ is None:
        force_delete_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.posts) + str(" WHERE ID = %d"), postid_))
    if (not post_):
        return post_
    # end if
    post_ = get_post(post_)
    if (not force_delete_) and "post" == post_.post_type or "page" == post_.post_type and "trash" != get_post_status(postid_) and EMPTY_TRASH_DAYS:
        return wp_trash_post(postid_)
    # end if
    if "attachment" == post_.post_type:
        return wp_delete_attachment(postid_, force_delete_)
    # end if
    #// 
    #// Filters whether a post deletion should take place.
    #// 
    #// @since 4.4.0
    #// 
    #// @param bool|null $delete       Whether to go forward with deletion.
    #// @param WP_Post   $post         Post object.
    #// @param bool      $force_delete Whether to bypass the Trash.
    #//
    check_ = apply_filters("pre_delete_post", None, post_, force_delete_)
    if None != check_:
        return check_
    # end if
    #// 
    #// Fires before a post is deleted, at the start of wp_delete_post().
    #// 
    #// @since 3.2.0
    #// 
    #// @see wp_delete_post()
    #// 
    #// @param int $postid Post ID.
    #//
    do_action("before_delete_post", postid_)
    delete_post_meta(postid_, "_wp_trash_meta_status")
    delete_post_meta(postid_, "_wp_trash_meta_time")
    wp_delete_object_term_relationships(postid_, get_object_taxonomies(post_.post_type))
    parent_data_ = Array({"post_parent": post_.post_parent})
    parent_where_ = Array({"post_parent": postid_})
    if is_post_type_hierarchical(post_.post_type):
        #// Point children of this page to its parent, also clean the cache of affected children.
        children_query_ = wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.posts) + str(" WHERE post_parent = %d AND post_type = %s"), postid_, post_.post_type)
        children_ = wpdb_.get_results(children_query_)
        if children_:
            wpdb_.update(wpdb_.posts, parent_data_, parent_where_ + Array({"post_type": post_.post_type}))
        # end if
    # end if
    #// Do raw query. wp_get_post_revisions() is filtered.
    revision_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_parent = %d AND post_type = 'revision'"), postid_))
    #// Use wp_delete_post (via wp_delete_post_revision) again. Ensures any meta/misplaced data gets cleaned up.
    for revision_id_ in revision_ids_:
        wp_delete_post_revision(revision_id_)
    # end for
    #// Point all attachments to this post up one level.
    wpdb_.update(wpdb_.posts, parent_data_, parent_where_ + Array({"post_type": "attachment"}))
    wp_defer_comment_counting(True)
    comment_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT comment_ID FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d"), postid_))
    for comment_id_ in comment_ids_:
        wp_delete_comment(comment_id_, True)
    # end for
    wp_defer_comment_counting(False)
    post_meta_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.postmeta) + str(" WHERE post_id = %d "), postid_))
    for mid_ in post_meta_ids_:
        delete_metadata_by_mid("post", mid_)
    # end for
    #// 
    #// Fires immediately before a post is deleted from the database.
    #// 
    #// @since 1.2.0
    #// 
    #// @param int $postid Post ID.
    #//
    do_action("delete_post", postid_)
    result_ = wpdb_.delete(wpdb_.posts, Array({"ID": postid_}))
    if (not result_):
        return False
    # end if
    #// 
    #// Fires immediately after a post is deleted from the database.
    #// 
    #// @since 2.2.0
    #// 
    #// @param int $postid Post ID.
    #//
    do_action("deleted_post", postid_)
    clean_post_cache(post_)
    if is_post_type_hierarchical(post_.post_type) and children_:
        for child_ in children_:
            clean_post_cache(child_)
        # end for
    # end if
    wp_clear_scheduled_hook("publish_future_post", Array(postid_))
    #// 
    #// Fires after a post is deleted, at the conclusion of wp_delete_post().
    #// 
    #// @since 3.2.0
    #// 
    #// @see wp_delete_post()
    #// 
    #// @param int $postid Post ID.
    #//
    do_action("after_delete_post", postid_)
    return post_
# end def wp_delete_post
#// 
#// Reset the page_on_front, show_on_front, and page_for_post settings when
#// a linked page is deleted or trashed.
#// 
#// Also ensures the post is no longer sticky.
#// 
#// @since 3.7.0
#// @access private
#// 
#// @param int $post_id Post ID.
#//
def _reset_front_page_settings_for_post(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if "page" == post_.post_type:
        #// 
        #// If the page is defined in option page_on_front or post_for_posts,
        #// adjust the corresponding options.
        #//
        if get_option("page_on_front") == post_.ID:
            update_option("show_on_front", "posts")
            update_option("page_on_front", 0)
        # end if
        if get_option("page_for_posts") == post_.ID:
            update_option("page_for_posts", 0)
        # end if
    # end if
    unstick_post(post_.ID)
# end def _reset_front_page_settings_for_post
#// 
#// Move a post or page to the Trash
#// 
#// If Trash is disabled, the post or page is permanently deleted.
#// 
#// @since 2.9.0
#// 
#// @see wp_delete_post()
#// 
#// @param int $post_id Optional. Post ID. Default is ID of the global $post
#// if EMPTY_TRASH_DAYS equals true.
#// @return WP_Post|false|null Post data on success, false or null on failure.
#//
def wp_trash_post(post_id_=0, *_args_):
    
    
    if (not EMPTY_TRASH_DAYS):
        return wp_delete_post(post_id_, True)
    # end if
    post_ = get_post(post_id_)
    if (not post_):
        return post_
    # end if
    if "trash" == post_.post_status:
        return False
    # end if
    #// 
    #// Filters whether a post trashing should take place.
    #// 
    #// @since 4.9.0
    #// 
    #// @param bool|null $trash Whether to go forward with trashing.
    #// @param WP_Post   $post  Post object.
    #//
    check_ = apply_filters("pre_trash_post", None, post_)
    if None != check_:
        return check_
    # end if
    #// 
    #// Fires before a post is sent to the Trash.
    #// 
    #// @since 3.3.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("wp_trash_post", post_id_)
    add_post_meta(post_id_, "_wp_trash_meta_status", post_.post_status)
    add_post_meta(post_id_, "_wp_trash_meta_time", time())
    post_updated_ = wp_update_post(Array({"ID": post_id_, "post_status": "trash"}))
    if (not post_updated_):
        return False
    # end if
    wp_trash_post_comments(post_id_)
    #// 
    #// Fires after a post is sent to the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("trashed_post", post_id_)
    return post_
# end def wp_trash_post
#// 
#// Restore a post or page from the Trash.
#// 
#// @since 2.9.0
#// 
#// @param int $post_id Optional. Post ID. Default is ID of the global $post.
#// @return WP_Post|false|null Post data on success, false or null on failure.
#//
def wp_untrash_post(post_id_=0, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_):
        return post_
    # end if
    if "trash" != post_.post_status:
        return False
    # end if
    #// 
    #// Filters whether a post untrashing should take place.
    #// 
    #// @since 4.9.0
    #// 
    #// @param bool|null $untrash Whether to go forward with untrashing.
    #// @param WP_Post   $post    Post object.
    #//
    check_ = apply_filters("pre_untrash_post", None, post_)
    if None != check_:
        return check_
    # end if
    #// 
    #// Fires before a post is restored from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrash_post", post_id_)
    post_status_ = get_post_meta(post_id_, "_wp_trash_meta_status", True)
    delete_post_meta(post_id_, "_wp_trash_meta_status")
    delete_post_meta(post_id_, "_wp_trash_meta_time")
    post_updated_ = wp_update_post(Array({"ID": post_id_, "post_status": post_status_}))
    if (not post_updated_):
        return False
    # end if
    wp_untrash_post_comments(post_id_)
    #// 
    #// Fires after a post is restored from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrashed_post", post_id_)
    return post_
# end def wp_untrash_post
#// 
#// Moves comments for a post to the Trash.
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Post|null $post Optional. Post ID or post object. Defaults to global $post.
#// @return mixed|void False on failure.
#//
def wp_trash_post_comments(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_)
    if php_empty(lambda : post_):
        return
    # end if
    post_id_ = post_.ID
    #// 
    #// Fires before comments are sent to the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("trash_post_comments", post_id_)
    comments_ = wpdb_.get_results(wpdb_.prepare(str("SELECT comment_ID, comment_approved FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d"), post_id_))
    if php_empty(lambda : comments_):
        return
    # end if
    #// Cache current status for each comment.
    statuses_ = Array()
    for comment_ in comments_:
        statuses_[comment_.comment_ID] = comment_.comment_approved
    # end for
    add_post_meta(post_id_, "_wp_trash_meta_comments_status", statuses_)
    #// Set status for all comments to post-trashed.
    result_ = wpdb_.update(wpdb_.comments, Array({"comment_approved": "post-trashed"}), Array({"comment_post_ID": post_id_}))
    clean_comment_cache(php_array_keys(statuses_))
    #// 
    #// Fires after comments are sent to the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int   $post_id  Post ID.
    #// @param array $statuses Array of comment statuses.
    #//
    do_action("trashed_post_comments", post_id_, statuses_)
    return result_
# end def wp_trash_post_comments
#// 
#// Restore comments for a post from the Trash.
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Post|null $post Optional. Post ID or post object. Defaults to global $post.
#// @return true|void
#//
def wp_untrash_post_comments(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_)
    if php_empty(lambda : post_):
        return
    # end if
    post_id_ = post_.ID
    statuses_ = get_post_meta(post_id_, "_wp_trash_meta_comments_status", True)
    if php_empty(lambda : statuses_):
        return True
    # end if
    #// 
    #// Fires before comments are restored for a post from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrash_post_comments", post_id_)
    #// Restore each comment to its original status.
    group_by_status_ = Array()
    for comment_id_,comment_status_ in statuses_.items():
        group_by_status_[comment_status_][-1] = comment_id_
    # end for
    for status_,comments_ in group_by_status_.items():
        #// Sanity check. This shouldn't happen.
        if "post-trashed" == status_:
            status_ = "0"
        # end if
        comments_in_ = php_implode(", ", php_array_map("intval", comments_))
        wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.comments) + str(" SET comment_approved = %s WHERE comment_ID IN (") + str(comments_in_) + str(")"), status_))
    # end for
    clean_comment_cache(php_array_keys(statuses_))
    delete_post_meta(post_id_, "_wp_trash_meta_comments_status")
    #// 
    #// Fires after comments are restored for a post from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrashed_post_comments", post_id_)
# end def wp_untrash_post_comments
#// 
#// Retrieve the list of categories for a post.
#// 
#// Compatibility layer for themes and plugins. Also an easy layer of abstraction
#// away from the complexity of the taxonomy layer.
#// 
#// @since 2.1.0
#// 
#// @see wp_get_object_terms()
#// 
#// @param int   $post_id Optional. The Post ID. Does not default to the ID of the
#// global $post. Default 0.
#// @param array $args    Optional. Category query parameters. Default empty array.
#// See WP_Term_Query::__construct() for supported arguments.
#// @return array|WP_Error List of categories. If the `$fields` argument passed via `$args` is 'all' or
#// 'all_with_object_id', an array of WP_Term objects will be returned. If `$fields`
#// is 'ids', an array of category ids. If `$fields` is 'names', an array of category names.
#// WP_Error object if 'category' taxonomy doesn't exist.
#//
def wp_get_post_categories(post_id_=0, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    post_id_ = php_int(post_id_)
    defaults_ = Array({"fields": "ids"})
    args_ = wp_parse_args(args_, defaults_)
    cats_ = wp_get_object_terms(post_id_, "category", args_)
    return cats_
# end def wp_get_post_categories
#// 
#// Retrieve the tags for a post.
#// 
#// There is only one default for this function, called 'fields' and by default
#// is set to 'all'. There are other defaults that can be overridden in
#// wp_get_object_terms().
#// 
#// @since 2.3.0
#// 
#// @param int   $post_id Optional. The Post ID. Does not default to the ID of the
#// global $post. Default 0.
#// @param array $args    Optional. Tag query parameters. Default empty array.
#// See WP_Term_Query::__construct() for supported arguments.
#// @return array|WP_Error Array of WP_Term objects on success or empty array if no tags were found.
#// WP_Error object if 'post_tag' taxonomy doesn't exist.
#//
def wp_get_post_tags(post_id_=0, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    return wp_get_post_terms(post_id_, "post_tag", args_)
# end def wp_get_post_tags
#// 
#// Retrieves the terms for a post.
#// 
#// @since 2.8.0
#// 
#// @param int          $post_id  Optional. The Post ID. Does not default to the ID of the
#// global $post. Default 0.
#// @param string|array $taxonomy Optional. The taxonomy slug or array of slugs for which
#// to retrieve terms. Default 'post_tag'.
#// @param array        $args     {
#// Optional. Term query parameters. See WP_Term_Query::__construct() for supported arguments.
#// 
#// @type string $fields Term fields to retrieve. Default 'all'.
#// }
#// @return array|WP_Error Array of WP_Term objects on success or empty array if no terms were found.
#// WP_Error object if `$taxonomy` doesn't exist.
#//
def wp_get_post_terms(post_id_=0, taxonomy_="post_tag", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    post_id_ = php_int(post_id_)
    defaults_ = Array({"fields": "all"})
    args_ = wp_parse_args(args_, defaults_)
    tags_ = wp_get_object_terms(post_id_, taxonomy_, args_)
    return tags_
# end def wp_get_post_terms
#// 
#// Retrieve a number of recent posts.
#// 
#// @since 1.0.0
#// 
#// @see get_posts()
#// 
#// @param array  $args   Optional. Arguments to retrieve posts. Default empty array.
#// @param string $output Optional. The required return type. One of OBJECT or ARRAY_A, which correspond to
#// a WP_Post object or an associative array, respectively. Default ARRAY_A.
#// @return array|false Array of recent posts, where the type of each element is determined by $output parameter.
#// Empty array on failure.
#//
def wp_get_recent_posts(args_=None, output_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    if output_ is None:
        output_ = ARRAY_A
    # end if
    
    if php_is_numeric(args_):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "3.1.0", __("Passing an integer number of posts is deprecated. Pass an array of arguments instead."))
        args_ = Array({"numberposts": absint(args_)})
    # end if
    #// Set default arguments.
    defaults_ = Array({"numberposts": 10, "offset": 0, "category": 0, "orderby": "post_date", "order": "DESC", "include": "", "exclude": "", "meta_key": "", "meta_value": "", "post_type": "post", "post_status": "draft, publish, future, pending, private", "suppress_filters": True})
    parsed_args_ = wp_parse_args(args_, defaults_)
    results_ = get_posts(parsed_args_)
    #// Backward compatibility. Prior to 3.1 expected posts to be returned in array.
    if ARRAY_A == output_:
        for key_,result_ in results_.items():
            results_[key_] = get_object_vars(result_)
        # end for
        return results_ if results_ else Array()
    # end if
    return results_ if results_ else False
# end def wp_get_recent_posts
#// 
#// Insert or update a post.
#// 
#// If the $postarr parameter has 'ID' set to a value, then post will be updated.
#// 
#// You can set the post date manually, by setting the values for 'post_date'
#// and 'post_date_gmt' keys. You can close the comments or open the comments by
#// setting the value for 'comment_status' key.
#// 
#// @since 1.0.0
#// @since 4.2.0 Support was added for encoding emoji in the post title, content, and excerpt.
#// @since 4.4.0 A 'meta_input' array can now be passed to `$postarr` to add post meta data.
#// 
#// @see sanitize_post()
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $postarr {
#// An array of elements that make up a post to update or insert.
#// 
#// @type int    $ID                    The post ID. If equal to something other than 0,
#// the post with that ID will be updated. Default 0.
#// @type int    $post_author           The ID of the user who added the post. Default is
#// the current user ID.
#// @type string $post_date             The date of the post. Default is the current time.
#// @type string $post_date_gmt         The date of the post in the GMT timezone. Default is
#// the value of `$post_date`.
#// @type mixed  $post_content          The post content. Default empty.
#// @type string $post_content_filtered The filtered post content. Default empty.
#// @type string $post_title            The post title. Default empty.
#// @type string $post_excerpt          The post excerpt. Default empty.
#// @type string $post_status           The post status. Default 'draft'.
#// @type string $post_type             The post type. Default 'post'.
#// @type string $comment_status        Whether the post can accept comments. Accepts 'open' or 'closed'.
#// Default is the value of 'default_comment_status' option.
#// @type string $ping_status           Whether the post can accept pings. Accepts 'open' or 'closed'.
#// Default is the value of 'default_ping_status' option.
#// @type string $post_password         The password to access the post. Default empty.
#// @type string $post_name             The post name. Default is the sanitized post title
#// when creating a new post.
#// @type string $to_ping               Space or carriage return-separated list of URLs to ping.
#// Default empty.
#// @type string $pinged                Space or carriage return-separated list of URLs that have
#// been pinged. Default empty.
#// @type string $post_modified         The date when the post was last modified. Default is
#// the current time.
#// @type string $post_modified_gmt     The date when the post was last modified in the GMT
#// timezone. Default is the current time.
#// @type int    $post_parent           Set this for the post it belongs to, if any. Default 0.
#// @type int    $menu_order            The order the post should be displayed in. Default 0.
#// @type string $post_mime_type        The mime type of the post. Default empty.
#// @type string $guid                  Global Unique ID for referencing the post. Default empty.
#// @type array  $post_category         Array of category IDs.
#// Defaults to value of the 'default_category' option.
#// @type array  $tags_input            Array of tag names, slugs, or IDs. Default empty.
#// @type array  $tax_input             Array of taxonomy terms keyed by their taxonomy name. Default empty.
#// @type array  $meta_input            Array of post meta values keyed by their post meta key. Default empty.
#// }
#// @param bool  $wp_error Optional. Whether to return a WP_Error on failure. Default false.
#// @return int|WP_Error The post ID on success. The value 0 or WP_Error on failure.
#//
def wp_insert_post(postarr_=None, wp_error_=None, *_args_):
    if wp_error_ is None:
        wp_error_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    user_id_ = get_current_user_id()
    defaults_ = Array({"post_author": user_id_, "post_content": "", "post_content_filtered": "", "post_title": "", "post_excerpt": "", "post_status": "draft", "post_type": "post", "comment_status": "", "ping_status": "", "post_password": "", "to_ping": "", "pinged": "", "post_parent": 0, "menu_order": 0, "guid": "", "import_id": 0, "context": ""})
    postarr_ = wp_parse_args(postarr_, defaults_)
    postarr_["filter"] = None
    postarr_ = sanitize_post(postarr_, "db")
    #// Are we updating or creating?
    post_ID_ = 0
    update_ = False
    guid_ = postarr_["guid"]
    if (not php_empty(lambda : postarr_["ID"])):
        update_ = True
        #// Get the post ID and GUID.
        post_ID_ = postarr_["ID"]
        post_before_ = get_post(post_ID_)
        if php_is_null(post_before_):
            if wp_error_:
                return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post ID.")))
            # end if
            return 0
        # end if
        guid_ = get_post_field("guid", post_ID_)
        previous_status_ = get_post_field("post_status", post_ID_)
    else:
        previous_status_ = "new"
    # end if
    post_type_ = "post" if php_empty(lambda : postarr_["post_type"]) else postarr_["post_type"]
    post_title_ = postarr_["post_title"]
    post_content_ = postarr_["post_content"]
    post_excerpt_ = postarr_["post_excerpt"]
    if (php_isset(lambda : postarr_["post_name"])):
        post_name_ = postarr_["post_name"]
    elif update_:
        #// For an update, don't modify the post_name if it wasn't supplied as an argument.
        post_name_ = post_before_.post_name
    # end if
    maybe_empty_ = "attachment" != post_type_ and (not post_content_) and (not post_title_) and (not post_excerpt_) and post_type_supports(post_type_, "editor") and post_type_supports(post_type_, "title") and post_type_supports(post_type_, "excerpt")
    #// 
    #// Filters whether the post should be considered "empty".
    #// 
    #// The post is considered "empty" if both:
    #// 1. The post type supports the title, editor, and excerpt fields
    #// 2. The title, editor, and excerpt fields are all empty
    #// 
    #// Returning a truthy value to the filter will effectively short-circuit
    #// the new post being inserted, returning 0. If $wp_error is true, a WP_Error
    #// will be returned instead.
    #// 
    #// @since 3.3.0
    #// 
    #// @param bool  $maybe_empty Whether the post should be considered "empty".
    #// @param array $postarr     Array of post data.
    #//
    if apply_filters("wp_insert_post_empty_content", maybe_empty_, postarr_):
        if wp_error_:
            return php_new_class("WP_Error", lambda : WP_Error("empty_content", __("Content, title, and excerpt are empty.")))
        else:
            return 0
        # end if
    # end if
    post_status_ = "draft" if php_empty(lambda : postarr_["post_status"]) else postarr_["post_status"]
    if "attachment" == post_type_ and (not php_in_array(post_status_, Array("inherit", "private", "trash", "auto-draft"), True)):
        post_status_ = "inherit"
    # end if
    if (not php_empty(lambda : postarr_["post_category"])):
        #// Filter out empty terms.
        post_category_ = php_array_filter(postarr_["post_category"])
    # end if
    #// Make sure we set a valid category.
    if php_empty(lambda : post_category_) or 0 == php_count(post_category_) or (not php_is_array(post_category_)):
        #// 'post' requires at least one category.
        if "post" == post_type_ and "auto-draft" != post_status_:
            post_category_ = Array(get_option("default_category"))
        else:
            post_category_ = Array()
        # end if
    # end if
    #// 
    #// Don't allow contributors to set the post slug for pending review posts.
    #// 
    #// For new posts check the primitive capability, for updates check the meta capability.
    #//
    post_type_object_ = get_post_type_object(post_type_)
    if (not update_) and "pending" == post_status_ and (not current_user_can(post_type_object_.cap.publish_posts)):
        post_name_ = ""
    elif update_ and "pending" == post_status_ and (not current_user_can("publish_post", post_ID_)):
        post_name_ = ""
    # end if
    #// 
    #// Create a valid post name. Drafts and pending posts are allowed to have
    #// an empty post name.
    #//
    if php_empty(lambda : post_name_):
        if (not php_in_array(post_status_, Array("draft", "pending", "auto-draft"))):
            post_name_ = sanitize_title(post_title_)
        else:
            post_name_ = ""
        # end if
    else:
        #// On updates, we need to check to see if it's using the old, fixed sanitization context.
        check_name_ = sanitize_title(post_name_, "", "old-save")
        if update_ and php_strtolower(urlencode(post_name_)) == check_name_ and get_post_field("post_name", post_ID_) == check_name_:
            post_name_ = check_name_
        else:
            #// new post, or slug has changed.
            post_name_ = sanitize_title(post_name_)
        # end if
    # end if
    #// 
    #// If the post date is empty (due to having been new or a draft) and status
    #// is not 'draft' or 'pending', set date to now.
    #//
    if php_empty(lambda : postarr_["post_date"]) or "0000-00-00 00:00:00" == postarr_["post_date"]:
        if php_empty(lambda : postarr_["post_date_gmt"]) or "0000-00-00 00:00:00" == postarr_["post_date_gmt"]:
            post_date_ = current_time("mysql")
        else:
            post_date_ = get_date_from_gmt(postarr_["post_date_gmt"])
        # end if
    else:
        post_date_ = postarr_["post_date"]
    # end if
    #// Validate the date.
    mm_ = php_substr(post_date_, 5, 2)
    jj_ = php_substr(post_date_, 8, 2)
    aa_ = php_substr(post_date_, 0, 4)
    valid_date_ = wp_checkdate(mm_, jj_, aa_, post_date_)
    if (not valid_date_):
        if wp_error_:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_date", __("Invalid date.")))
        else:
            return 0
        # end if
    # end if
    if php_empty(lambda : postarr_["post_date_gmt"]) or "0000-00-00 00:00:00" == postarr_["post_date_gmt"]:
        if (not php_in_array(post_status_, get_post_stati(Array({"date_floating": True})), True)):
            post_date_gmt_ = get_gmt_from_date(post_date_)
        else:
            post_date_gmt_ = "0000-00-00 00:00:00"
        # end if
    else:
        post_date_gmt_ = postarr_["post_date_gmt"]
    # end if
    if update_ or "0000-00-00 00:00:00" == post_date_:
        post_modified_ = current_time("mysql")
        post_modified_gmt_ = current_time("mysql", 1)
    else:
        post_modified_ = post_date_
        post_modified_gmt_ = post_date_gmt_
    # end if
    if "attachment" != post_type_:
        now_ = gmdate("Y-m-d H:i:s")
        if "publish" == post_status_:
            if strtotime(post_date_gmt_) - strtotime(now_) >= MINUTE_IN_SECONDS:
                post_status_ = "future"
            # end if
        elif "future" == post_status_:
            if strtotime(post_date_gmt_) - strtotime(now_) < MINUTE_IN_SECONDS:
                post_status_ = "publish"
            # end if
        # end if
    # end if
    #// Comment status.
    if php_empty(lambda : postarr_["comment_status"]):
        if update_:
            comment_status_ = "closed"
        else:
            comment_status_ = get_default_comment_status(post_type_)
        # end if
    else:
        comment_status_ = postarr_["comment_status"]
    # end if
    #// These variables are needed by compact() later.
    post_content_filtered_ = postarr_["post_content_filtered"]
    post_author_ = postarr_["post_author"] if (php_isset(lambda : postarr_["post_author"])) else user_id_
    ping_status_ = get_default_comment_status(post_type_, "pingback") if php_empty(lambda : postarr_["ping_status"]) else postarr_["ping_status"]
    to_ping_ = sanitize_trackback_urls(postarr_["to_ping"]) if (php_isset(lambda : postarr_["to_ping"])) else ""
    pinged_ = postarr_["pinged"] if (php_isset(lambda : postarr_["pinged"])) else ""
    import_id_ = postarr_["import_id"] if (php_isset(lambda : postarr_["import_id"])) else 0
    #// 
    #// The 'wp_insert_post_parent' filter expects all variables to be present.
    #// Previously, these variables would have already been extracted
    #//
    if (php_isset(lambda : postarr_["menu_order"])):
        menu_order_ = php_int(postarr_["menu_order"])
    else:
        menu_order_ = 0
    # end if
    post_password_ = postarr_["post_password"] if (php_isset(lambda : postarr_["post_password"])) else ""
    if "private" == post_status_:
        post_password_ = ""
    # end if
    if (php_isset(lambda : postarr_["post_parent"])):
        post_parent_ = php_int(postarr_["post_parent"])
    else:
        post_parent_ = 0
    # end if
    new_postarr_ = php_array_merge(Array({"ID": post_ID_}), php_compact(php_array_diff(php_array_keys(defaults_), Array("context_", "filter"))))
    #// 
    #// Filters the post parent -- used to check for and prevent hierarchy loops.
    #// 
    #// @since 3.1.0
    #// 
    #// @param int   $post_parent Post parent ID.
    #// @param int   $post_ID     Post ID.
    #// @param array $new_postarr Array of parsed post data.
    #// @param array $postarr     Array of sanitized, but otherwise unmodified post data.
    #//
    post_parent_ = apply_filters("wp_insert_post_parent", post_parent_, post_ID_, new_postarr_, postarr_)
    #// 
    #// If the post is being untrashed and it has a desired slug stored in post meta,
    #// reassign it.
    #//
    if "trash" == previous_status_ and "trash" != post_status_:
        desired_post_slug_ = get_post_meta(post_ID_, "_wp_desired_post_slug", True)
        if desired_post_slug_:
            delete_post_meta(post_ID_, "_wp_desired_post_slug")
            post_name_ = desired_post_slug_
        # end if
    # end if
    #// If a trashed post has the desired slug, change it and let this post have it.
    if "trash" != post_status_ and post_name_:
        #// 
        #// Filters whether or not to add a `__trashed` suffix to trashed posts that match the name of the updated post.
        #// 
        #// @since 5.4.0
        #// 
        #// @param bool   $add_trashed_suffix Whether to attempt to add the suffix.
        #// @param string $post_name          The name of the post being updated.
        #// @param int    $post_ID            Post ID.
        #//
        add_trashed_suffix_ = apply_filters("add_trashed_suffix_to_trashed_posts", True, post_name_, post_ID_)
        if add_trashed_suffix_:
            wp_add_trashed_suffix_to_post_name_for_trashed_posts(post_name_, post_ID_)
        # end if
    # end if
    #// When trashing an existing post, change its slug to allow non-trashed posts to use it.
    if "trash" == post_status_ and "trash" != previous_status_ and "new" != previous_status_:
        post_name_ = wp_add_trashed_suffix_to_post_name_for_post(post_ID_)
    # end if
    post_name_ = wp_unique_post_slug(post_name_, post_ID_, post_status_, post_type_, post_parent_)
    #// Don't unslash.
    post_mime_type_ = postarr_["post_mime_type"] if (php_isset(lambda : postarr_["post_mime_type"])) else ""
    #// Expected_slashed (everything!).
    data_ = php_compact("post_author_", "post_date_", "post_date_gmt_", "post_content_", "post_content_filtered_", "post_title_", "post_excerpt_", "post_status_", "post_type_", "comment_status_", "ping_status_", "post_password_", "post_name_", "to_ping_", "pinged_", "post_modified_", "post_modified_gmt_", "post_parent_", "menu_order_", "post_mime_type_", "guid_")
    emoji_fields_ = Array("post_title", "post_content", "post_excerpt")
    for emoji_field_ in emoji_fields_:
        if (php_isset(lambda : data_[emoji_field_])):
            charset_ = wpdb_.get_col_charset(wpdb_.posts, emoji_field_)
            if "utf8" == charset_:
                data_[emoji_field_] = wp_encode_emoji(data_[emoji_field_])
            # end if
        # end if
    # end for
    if "attachment" == post_type_:
        #// 
        #// Filters attachment post data before it is updated in or added to the database.
        #// 
        #// @since 3.9.0
        #// 
        #// @param array $data    An array of sanitized attachment post data.
        #// @param array $postarr An array of unsanitized attachment post data.
        #//
        data_ = apply_filters("wp_insert_attachment_data", data_, postarr_)
    else:
        #// 
        #// Filters slashed post data just before it is inserted into the database.
        #// 
        #// @since 2.7.0
        #// 
        #// @param array $data    An array of slashed post data.
        #// @param array $postarr An array of sanitized, but otherwise unmodified post data.
        #//
        data_ = apply_filters("wp_insert_post_data", data_, postarr_)
    # end if
    data_ = wp_unslash(data_)
    where_ = Array({"ID": post_ID_})
    if update_:
        #// 
        #// Fires immediately before an existing post is updated in the database.
        #// 
        #// @since 2.5.0
        #// 
        #// @param int   $post_ID Post ID.
        #// @param array $data    Array of unslashed post data.
        #//
        do_action("pre_post_update", post_ID_, data_)
        if False == wpdb_.update(wpdb_.posts, data_, where_):
            if wp_error_:
                return php_new_class("WP_Error", lambda : WP_Error("db_update_error", __("Could not update post in the database"), wpdb_.last_error))
            else:
                return 0
            # end if
        # end if
    else:
        #// If there is a suggested ID, use it if not already present.
        if (not php_empty(lambda : import_id_)):
            import_id_ = php_int(import_id_)
            if (not wpdb_.get_var(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE ID = %d"), import_id_))):
                data_["ID"] = import_id_
            # end if
        # end if
        if False == wpdb_.insert(wpdb_.posts, data_):
            if wp_error_:
                return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert post into the database"), wpdb_.last_error))
            else:
                return 0
            # end if
        # end if
        post_ID_ = php_int(wpdb_.insert_id)
        #// Use the newly generated $post_ID.
        where_ = Array({"ID": post_ID_})
    # end if
    if php_empty(lambda : data_["post_name"]) and (not php_in_array(data_["post_status"], Array("draft", "pending", "auto-draft"))):
        data_["post_name"] = wp_unique_post_slug(sanitize_title(data_["post_title"], post_ID_), post_ID_, data_["post_status"], post_type_, post_parent_)
        wpdb_.update(wpdb_.posts, Array({"post_name": data_["post_name"]}), where_)
        clean_post_cache(post_ID_)
    # end if
    if is_object_in_taxonomy(post_type_, "category"):
        wp_set_post_categories(post_ID_, post_category_)
    # end if
    if (php_isset(lambda : postarr_["tags_input"])) and is_object_in_taxonomy(post_type_, "post_tag"):
        wp_set_post_tags(post_ID_, postarr_["tags_input"])
    # end if
    #// New-style support for all custom taxonomies.
    if (not php_empty(lambda : postarr_["tax_input"])):
        for taxonomy_,tags_ in postarr_["tax_input"].items():
            taxonomy_obj_ = get_taxonomy(taxonomy_)
            if (not taxonomy_obj_):
                #// translators: %s: Taxonomy name.
                _doing_it_wrong(inspect.currentframe().f_code.co_name, php_sprintf(__("Invalid taxonomy: %s."), taxonomy_), "4.4.0")
                continue
            # end if
            #// array = hierarchical, string = non-hierarchical.
            if php_is_array(tags_):
                tags_ = php_array_filter(tags_)
            # end if
            if current_user_can(taxonomy_obj_.cap.assign_terms):
                wp_set_post_terms(post_ID_, tags_, taxonomy_)
            # end if
        # end for
    # end if
    if (not php_empty(lambda : postarr_["meta_input"])):
        for field_,value_ in postarr_["meta_input"].items():
            update_post_meta(post_ID_, field_, value_)
        # end for
    # end if
    current_guid_ = get_post_field("guid", post_ID_)
    #// Set GUID.
    if (not update_) and "" == current_guid_:
        wpdb_.update(wpdb_.posts, Array({"guid": get_permalink(post_ID_)}), where_)
    # end if
    if "attachment" == postarr_["post_type"]:
        if (not php_empty(lambda : postarr_["file"])):
            update_attached_file(post_ID_, postarr_["file"])
        # end if
        if (not php_empty(lambda : postarr_["context"])):
            add_post_meta(post_ID_, "_wp_attachment_context", postarr_["context"], True)
        # end if
    # end if
    #// Set or remove featured image.
    if (php_isset(lambda : postarr_["_thumbnail_id"])):
        thumbnail_support_ = current_theme_supports("post-thumbnails", post_type_) and post_type_supports(post_type_, "thumbnail") or "revision" == post_type_
        if (not thumbnail_support_) and "attachment" == post_type_ and post_mime_type_:
            if wp_attachment_is("audio", post_ID_):
                thumbnail_support_ = post_type_supports("attachment:audio", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:audio")
            elif wp_attachment_is("video", post_ID_):
                thumbnail_support_ = post_type_supports("attachment:video", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:video")
            # end if
        # end if
        if thumbnail_support_:
            thumbnail_id_ = php_intval(postarr_["_thumbnail_id"])
            if -1 == thumbnail_id_:
                delete_post_thumbnail(post_ID_)
            else:
                set_post_thumbnail(post_ID_, thumbnail_id_)
            # end if
        # end if
    # end if
    clean_post_cache(post_ID_)
    post_ = get_post(post_ID_)
    if (not php_empty(lambda : postarr_["page_template"])):
        post_.page_template = postarr_["page_template"]
        page_templates_ = wp_get_theme().get_page_templates(post_)
        if "default" != postarr_["page_template"] and (not (php_isset(lambda : page_templates_[postarr_["page_template"]]))):
            if wp_error_:
                return php_new_class("WP_Error", lambda : WP_Error("invalid_page_template", __("Invalid page template.")))
            # end if
            update_post_meta(post_ID_, "_wp_page_template", "default")
        else:
            update_post_meta(post_ID_, "_wp_page_template", postarr_["page_template"])
        # end if
    # end if
    if "attachment" != postarr_["post_type"]:
        wp_transition_post_status(data_["post_status"], previous_status_, post_)
    else:
        if update_:
            #// 
            #// Fires once an existing attachment has been updated.
            #// 
            #// @since 2.0.0
            #// 
            #// @param int $post_ID Attachment ID.
            #//
            do_action("edit_attachment", post_ID_)
            post_after_ = get_post(post_ID_)
            #// 
            #// Fires once an existing attachment has been updated.
            #// 
            #// @since 4.4.0
            #// 
            #// @param int     $post_ID      Post ID.
            #// @param WP_Post $post_after   Post object following the update.
            #// @param WP_Post $post_before  Post object before the update.
            #//
            do_action("attachment_updated", post_ID_, post_after_, post_before_)
        else:
            #// 
            #// Fires once an attachment has been added.
            #// 
            #// @since 2.0.0
            #// 
            #// @param int $post_ID Attachment ID.
            #//
            do_action("add_attachment", post_ID_)
        # end if
        return post_ID_
    # end if
    if update_:
        #// 
        #// Fires once an existing post has been updated.
        #// 
        #// The dynamic portion of the hook name, `$post->post_type`, refers to
        #// the post type slug.
        #// 
        #// @since 5.1.0
        #// 
        #// @param int     $post_ID Post ID.
        #// @param WP_Post $post    Post object.
        #//
        do_action(str("edit_post_") + str(post_.post_type), post_ID_, post_)
        #// 
        #// Fires once an existing post has been updated.
        #// 
        #// @since 1.2.0
        #// 
        #// @param int     $post_ID Post ID.
        #// @param WP_Post $post    Post object.
        #//
        do_action("edit_post", post_ID_, post_)
        post_after_ = get_post(post_ID_)
        #// 
        #// Fires once an existing post has been updated.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int     $post_ID      Post ID.
        #// @param WP_Post $post_after   Post object following the update.
        #// @param WP_Post $post_before  Post object before the update.
        #//
        do_action("post_updated", post_ID_, post_after_, post_before_)
    # end if
    #// 
    #// Fires once a post has been saved.
    #// 
    #// The dynamic portion of the hook name, `$post->post_type`, refers to
    #// the post type slug.
    #// 
    #// @since 3.7.0
    #// 
    #// @param int     $post_ID Post ID.
    #// @param WP_Post $post    Post object.
    #// @param bool    $update  Whether this is an existing post being updated or not.
    #//
    do_action(str("save_post_") + str(post_.post_type), post_ID_, post_, update_)
    #// 
    #// Fires once a post has been saved.
    #// 
    #// @since 1.5.0
    #// 
    #// @param int     $post_ID Post ID.
    #// @param WP_Post $post    Post object.
    #// @param bool    $update  Whether this is an existing post being updated or not.
    #//
    do_action("save_post", post_ID_, post_, update_)
    #// 
    #// Fires once a post has been saved.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int     $post_ID Post ID.
    #// @param WP_Post $post    Post object.
    #// @param bool    $update  Whether this is an existing post being updated or not.
    #//
    do_action("wp_insert_post", post_ID_, post_, update_)
    return post_ID_
# end def wp_insert_post
#// 
#// Update a post with new post data.
#// 
#// The date does not have to be set for drafts. You can set the date and it will
#// not be overridden.
#// 
#// @since 1.0.0
#// 
#// @param array|object $postarr  Optional. Post data. Arrays are expected to be escaped,
#// objects are not. Default array.
#// @param bool         $wp_error Optional. Allow return of WP_Error on failure. Default false.
#// @return int|WP_Error The post ID on success. The value 0 or WP_Error on failure.
#//
def wp_update_post(postarr_=None, wp_error_=None, *_args_):
    if postarr_ is None:
        postarr_ = Array()
    # end if
    if wp_error_ is None:
        wp_error_ = False
    # end if
    
    if php_is_object(postarr_):
        #// Non-escaped post was passed.
        postarr_ = get_object_vars(postarr_)
        postarr_ = wp_slash(postarr_)
    # end if
    #// First, get all of the original fields.
    post_ = get_post(postarr_["ID"], ARRAY_A)
    if php_is_null(post_):
        if wp_error_:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post ID.")))
        # end if
        return 0
    # end if
    #// Escape data pulled from DB.
    post_ = wp_slash(post_)
    #// Passed post category list overwrites existing category list if not empty.
    if (php_isset(lambda : postarr_["post_category"])) and php_is_array(postarr_["post_category"]) and 0 != php_count(postarr_["post_category"]):
        post_cats_ = postarr_["post_category"]
    else:
        post_cats_ = post_["post_category"]
    # end if
    #// Drafts shouldn't be assigned a date unless explicitly done so by the user.
    if (php_isset(lambda : post_["post_status"])) and php_in_array(post_["post_status"], Array("draft", "pending", "auto-draft")) and php_empty(lambda : postarr_["edit_date"]) and "0000-00-00 00:00:00" == post_["post_date_gmt"]:
        clear_date_ = True
    else:
        clear_date_ = False
    # end if
    #// Merge old and new fields with new fields overwriting old ones.
    postarr_ = php_array_merge(post_, postarr_)
    postarr_["post_category"] = post_cats_
    if clear_date_:
        postarr_["post_date"] = current_time("mysql")
        postarr_["post_date_gmt"] = ""
    # end if
    if "attachment" == postarr_["post_type"]:
        return wp_insert_attachment(postarr_, False, 0, wp_error_)
    # end if
    #// Discard 'tags_input' parameter if it's the same as existing post tags.
    if (php_isset(lambda : postarr_["tags_input"])) and is_object_in_taxonomy(postarr_["post_type"], "post_tag"):
        tags_ = get_the_terms(postarr_["ID"], "post_tag")
        tag_names_ = Array()
        if tags_ and (not is_wp_error(tags_)):
            tag_names_ = wp_list_pluck(tags_, "name")
        # end if
        if postarr_["tags_input"] == tag_names_:
            postarr_["tags_input"] = None
        # end if
    # end if
    return wp_insert_post(postarr_, wp_error_)
# end def wp_update_post
#// 
#// Publish a post by transitioning the post status.
#// 
#// @since 2.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Post $post Post ID or post object.
#//
def wp_publish_post(post_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_)
    if (not post_):
        return
    # end if
    if "publish" == post_.post_status:
        return
    # end if
    wpdb_.update(wpdb_.posts, Array({"post_status": "publish"}), Array({"ID": post_.ID}))
    clean_post_cache(post_.ID)
    old_status_ = post_.post_status
    post_.post_status = "publish"
    wp_transition_post_status("publish", old_status_, post_)
    #// This action is documented in wp-includes/post.php
    do_action(str("edit_post_") + str(post_.post_type), post_.ID, post_)
    #// This action is documented in wp-includes/post.php
    do_action("edit_post", post_.ID, post_)
    #// This action is documented in wp-includes/post.php
    do_action(str("save_post_") + str(post_.post_type), post_.ID, post_, True)
    #// This action is documented in wp-includes/post.php
    do_action("save_post", post_.ID, post_, True)
    #// This action is documented in wp-includes/post.php
    do_action("wp_insert_post", post_.ID, post_, True)
# end def wp_publish_post
#// 
#// Publish future post and make sure post ID has future post status.
#// 
#// Invoked by cron 'publish_future_post' event. This safeguard prevents cron
#// from publishing drafts, etc.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Post $post_id Post ID or post object.
#//
def check_and_publish_future_post(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if php_empty(lambda : post_):
        return
    # end if
    if "future" != post_.post_status:
        return
    # end if
    time_ = strtotime(post_.post_date_gmt + " GMT")
    #// Uh oh, someone jumped the gun!
    if time_ > time():
        wp_clear_scheduled_hook("publish_future_post", Array(post_id_))
        #// Clear anything else in the system.
        wp_schedule_single_event(time_, "publish_future_post", Array(post_id_))
        return
    # end if
    #// wp_publish_post() returns no meaningful value.
    wp_publish_post(post_id_)
# end def check_and_publish_future_post
#// 
#// Computes a unique slug for the post, when given the desired slug and some post details.
#// 
#// @since 2.8.0
#// 
#// @global wpdb       $wpdb       WordPress database abstraction object.
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $slug        The desired slug (post_name).
#// @param int    $post_ID     Post ID.
#// @param string $post_status No uniqueness checks are made if the post is still draft or pending.
#// @param string $post_type   Post type.
#// @param int    $post_parent Post parent ID.
#// @return string Unique slug for the post, based on $post_name (with a -1, -2, etc. suffix)
#//
def wp_unique_post_slug(slug_=None, post_ID_=None, post_status_=None, post_type_=None, post_parent_=None, *_args_):
    
    
    if php_in_array(post_status_, Array("draft", "pending", "auto-draft")) or "inherit" == post_status_ and "revision" == post_type_ or "user_request" == post_type_:
        return slug_
    # end if
    #// 
    #// Filters the post slug before it is generated to be unique.
    #// 
    #// Returning a non-null value will short-circuit the
    #// unique slug generation, returning the passed value instead.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string|null $override_slug Short-circuit return value.
    #// @param string      $slug          The desired slug (post_name).
    #// @param int         $post_ID       Post ID.
    #// @param string      $post_status   The post status.
    #// @param string      $post_type     Post type.
    #// @param int         $post_parent   Post parent ID.
    #//
    override_slug_ = apply_filters("pre_wp_unique_post_slug", None, slug_, post_ID_, post_status_, post_type_, post_parent_)
    if None != override_slug_:
        return override_slug_
    # end if
    global wpdb_
    global wp_rewrite_
    php_check_if_defined("wpdb_","wp_rewrite_")
    original_slug_ = slug_
    feeds_ = wp_rewrite_.feeds
    if (not php_is_array(feeds_)):
        feeds_ = Array()
    # end if
    if "attachment" == post_type_:
        #// Attachment slugs must be unique across all types.
        check_sql_ = str("SELECT post_name FROM ") + str(wpdb_.posts) + str(" WHERE post_name = %s AND ID != %d LIMIT 1")
        post_name_check_ = wpdb_.get_var(wpdb_.prepare(check_sql_, slug_, post_ID_))
        #// 
        #// Filters whether the post slug would make a bad attachment slug.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool   $bad_slug Whether the slug would be bad as an attachment slug.
        #// @param string $slug     The post slug.
        #//
        if post_name_check_ or php_in_array(slug_, feeds_) or "embed" == slug_ or apply_filters("wp_unique_post_slug_is_bad_attachment_slug", False, slug_):
            suffix_ = 2
            while True:
                alt_post_name_ = _truncate_post_slug(slug_, 200 - php_strlen(suffix_) + 1) + str("-") + str(suffix_)
                post_name_check_ = wpdb_.get_var(wpdb_.prepare(check_sql_, alt_post_name_, post_ID_))
                suffix_ += 1
                
                if post_name_check_:
                    break
                # end if
            # end while
            slug_ = alt_post_name_
        # end if
    elif is_post_type_hierarchical(post_type_):
        if "nav_menu_item" == post_type_:
            return slug_
        # end if
        #// 
        #// Page slugs must be unique within their own trees. Pages are in a separate
        #// namespace than posts so page slugs are allowed to overlap post slugs.
        #//
        check_sql_ = str("SELECT post_name FROM ") + str(wpdb_.posts) + str(" WHERE post_name = %s AND post_type IN ( %s, 'attachment' ) AND ID != %d AND post_parent = %d LIMIT 1")
        post_name_check_ = wpdb_.get_var(wpdb_.prepare(check_sql_, slug_, post_type_, post_ID_, post_parent_))
        #// 
        #// Filters whether the post slug would make a bad hierarchical post slug.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool   $bad_slug    Whether the post slug would be bad in a hierarchical post context.
        #// @param string $slug        The post slug.
        #// @param string $post_type   Post type.
        #// @param int    $post_parent Post parent ID.
        #//
        if post_name_check_ or php_in_array(slug_, feeds_) or "embed" == slug_ or php_preg_match(str("@^(") + str(wp_rewrite_.pagination_base) + str(")?\\d+$@"), slug_) or apply_filters("wp_unique_post_slug_is_bad_hierarchical_slug", False, slug_, post_type_, post_parent_):
            suffix_ = 2
            while True:
                alt_post_name_ = _truncate_post_slug(slug_, 200 - php_strlen(suffix_) + 1) + str("-") + str(suffix_)
                post_name_check_ = wpdb_.get_var(wpdb_.prepare(check_sql_, alt_post_name_, post_type_, post_ID_, post_parent_))
                suffix_ += 1
                
                if post_name_check_:
                    break
                # end if
            # end while
            slug_ = alt_post_name_
        # end if
    else:
        #// Post slugs must be unique across all posts.
        check_sql_ = str("SELECT post_name FROM ") + str(wpdb_.posts) + str(" WHERE post_name = %s AND post_type = %s AND ID != %d LIMIT 1")
        post_name_check_ = wpdb_.get_var(wpdb_.prepare(check_sql_, slug_, post_type_, post_ID_))
        #// Prevent new post slugs that could result in URLs that conflict with date archives.
        post_ = get_post(post_ID_)
        conflicts_with_date_archive_ = False
        if "post" == post_type_ and (not post_) or post_.post_name != slug_ and php_preg_match("/^[0-9]+$/", slug_):
            slug_num_ = php_intval(slug_)
            if slug_num_:
                permastructs_ = php_array_values(php_array_filter(php_explode("/", get_option("permalink_structure"))))
                postname_index_ = php_array_search("%postname%", permastructs_)
                #// 
                #// Potential date clashes are as follows:
                #// 
                #// - Any integer in the first permastruct position could be a year.
                #// - An integer between 1 and 12 that follows 'year' conflicts with 'monthnum'.
                #// - An integer between 1 and 31 that follows 'monthnum' conflicts with 'day'.
                #//
                if 0 == postname_index_ or postname_index_ and "%year%" == permastructs_[postname_index_ - 1] and 13 > slug_num_ or postname_index_ and "%monthnum%" == permastructs_[postname_index_ - 1] and 32 > slug_num_:
                    conflicts_with_date_archive_ = True
                # end if
            # end if
        # end if
        #// 
        #// Filters whether the post slug would be bad as a flat slug.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool   $bad_slug  Whether the post slug would be bad as a flat slug.
        #// @param string $slug      The post slug.
        #// @param string $post_type Post type.
        #//
        if post_name_check_ or php_in_array(slug_, feeds_) or "embed" == slug_ or conflicts_with_date_archive_ or apply_filters("wp_unique_post_slug_is_bad_flat_slug", False, slug_, post_type_):
            suffix_ = 2
            while True:
                alt_post_name_ = _truncate_post_slug(slug_, 200 - php_strlen(suffix_) + 1) + str("-") + str(suffix_)
                post_name_check_ = wpdb_.get_var(wpdb_.prepare(check_sql_, alt_post_name_, post_type_, post_ID_))
                suffix_ += 1
                
                if post_name_check_:
                    break
                # end if
            # end while
            slug_ = alt_post_name_
        # end if
    # end if
    #// 
    #// Filters the unique post slug.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $slug          The post slug.
    #// @param int    $post_ID       Post ID.
    #// @param string $post_status   The post status.
    #// @param string $post_type     Post type.
    #// @param int    $post_parent   Post parent ID
    #// @param string $original_slug The original post slug.
    #//
    return apply_filters("wp_unique_post_slug", slug_, post_ID_, post_status_, post_type_, post_parent_, original_slug_)
# end def wp_unique_post_slug
#// 
#// Truncate a post slug.
#// 
#// @since 3.6.0
#// @access private
#// 
#// @see utf8_uri_encode()
#// 
#// @param string $slug   The slug to truncate.
#// @param int    $length Optional. Max length of the slug. Default 200 (characters).
#// @return string The truncated slug.
#//
def _truncate_post_slug(slug_=None, length_=200, *_args_):
    
    
    if php_strlen(slug_) > length_:
        decoded_slug_ = urldecode(slug_)
        if decoded_slug_ == slug_:
            slug_ = php_substr(slug_, 0, length_)
        else:
            slug_ = utf8_uri_encode(decoded_slug_, length_)
        # end if
    # end if
    return php_rtrim(slug_, "-")
# end def _truncate_post_slug
#// 
#// Add tags to a post.
#// 
#// @see wp_set_post_tags()
#// 
#// @since 2.3.0
#// 
#// @param int          $post_id Optional. The Post ID. Does not default to the ID of the global $post.
#// @param string|array $tags    Optional. An array of tags to set for the post, or a string of tags
#// separated by commas. Default empty.
#// @return array|false|WP_Error Array of affected term IDs. WP_Error or false on failure.
#//
def wp_add_post_tags(post_id_=0, tags_="", *_args_):
    
    
    return wp_set_post_tags(post_id_, tags_, True)
# end def wp_add_post_tags
#// 
#// Set the tags for a post.
#// 
#// @since 2.3.0
#// 
#// @see wp_set_object_terms()
#// 
#// @param int          $post_id Optional. The Post ID. Does not default to the ID of the global $post.
#// @param string|array $tags    Optional. An array of tags to set for the post, or a string of tags
#// separated by commas. Default empty.
#// @param bool         $append  Optional. If true, don't delete existing tags, just add on. If false,
#// replace the tags with the new tags. Default false.
#// @return array|false|WP_Error Array of term taxonomy IDs of affected terms. WP_Error or false on failure.
#//
def wp_set_post_tags(post_id_=0, tags_="", append_=None, *_args_):
    if append_ is None:
        append_ = False
    # end if
    
    return wp_set_post_terms(post_id_, tags_, "post_tag", append_)
# end def wp_set_post_tags
#// 
#// Set the terms for a post.
#// 
#// @since 2.8.0
#// 
#// @see wp_set_object_terms()
#// 
#// @param int          $post_id  Optional. The Post ID. Does not default to the ID of the global $post.
#// @param string|array $tags     Optional. An array of terms to set for the post, or a string of terms
#// separated by commas. Hierarchical taxonomies must always pass IDs rather
#// than names so that children with the same names but different parents
#// aren't confused. Default empty.
#// @param string       $taxonomy Optional. Taxonomy name. Default 'post_tag'.
#// @param bool         $append   Optional. If true, don't delete existing terms, just add on. If false,
#// replace the terms with the new terms. Default false.
#// @return array|false|WP_Error Array of term taxonomy IDs of affected terms. WP_Error or false on failure.
#//
def wp_set_post_terms(post_id_=0, tags_="", taxonomy_="post_tag", append_=None, *_args_):
    if append_ is None:
        append_ = False
    # end if
    
    post_id_ = php_int(post_id_)
    if (not post_id_):
        return False
    # end if
    if php_empty(lambda : tags_):
        tags_ = Array()
    # end if
    if (not php_is_array(tags_)):
        comma_ = _x(",", "tag delimiter")
        if "," != comma_:
            tags_ = php_str_replace(comma_, ",", tags_)
        # end if
        tags_ = php_explode(",", php_trim(tags_, " \n   \r ,"))
    # end if
    #// 
    #// Hierarchical taxonomies must always pass IDs rather than names so that
    #// children with the same names but different parents aren't confused.
    #//
    if is_taxonomy_hierarchical(taxonomy_):
        tags_ = array_unique(php_array_map("intval", tags_))
    # end if
    return wp_set_object_terms(post_id_, tags_, taxonomy_, append_)
# end def wp_set_post_terms
#// 
#// Set categories for a post.
#// 
#// If the post categories parameter is not set, then the default category is
#// going used.
#// 
#// @since 2.1.0
#// 
#// @param int       $post_ID         Optional. The Post ID. Does not default to the ID
#// of the global $post. Default 0.
#// @param array|int $post_categories Optional. List of category IDs, or the ID of a single category.
#// Default empty array.
#// @param bool      $append          If true, don't delete existing categories, just add on.
#// If false, replace the categories with the new categories.
#// @return array|false|WP_Error Array of term taxonomy IDs of affected categories. WP_Error or false on failure.
#//
def wp_set_post_categories(post_ID_=0, post_categories_=None, append_=None, *_args_):
    if post_categories_ is None:
        post_categories_ = Array()
    # end if
    if append_ is None:
        append_ = False
    # end if
    
    post_ID_ = php_int(post_ID_)
    post_type_ = get_post_type(post_ID_)
    post_status_ = get_post_status(post_ID_)
    #// If $post_categories isn't already an array, make it one:
    post_categories_ = post_categories_
    if php_empty(lambda : post_categories_):
        if "post" == post_type_ and "auto-draft" != post_status_:
            post_categories_ = Array(get_option("default_category"))
            append_ = False
        else:
            post_categories_ = Array()
        # end if
    elif 1 == php_count(post_categories_) and "" == reset(post_categories_):
        return True
    # end if
    return wp_set_post_terms(post_ID_, post_categories_, "category", append_)
# end def wp_set_post_categories
#// 
#// Fires actions related to the transitioning of a post's status.
#// 
#// When a post is saved, the post status is "transitioned" from one status to another,
#// though this does not always mean the status has actually changed before and after
#// the save. This function fires a number of action hooks related to that transition:
#// the generic {@see 'transition_post_status'} action, as well as the dynamic hooks
#// {@see '$old_status_to_$new_status'} and {@see '$new_status_$post->post_type'}. Note
#// that the function does not transition the post object in the database.
#// 
#// For instance: When publishing a post for the first time, the post status may transition
#// from 'draft' – or some other status – to 'publish'. However, if a post is already
#// published and is simply being updated, the "old" and "new" statuses may both be 'publish'
#// before and after the transition.
#// 
#// @since 2.3.0
#// 
#// @param string  $new_status Transition to this post status.
#// @param string  $old_status Previous post status.
#// @param WP_Post $post Post data.
#//
def wp_transition_post_status(new_status_=None, old_status_=None, post_=None, *_args_):
    
    
    #// 
    #// Fires when a post is transitioned from one status to another.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string  $new_status New post status.
    #// @param string  $old_status Old post status.
    #// @param WP_Post $post       Post object.
    #//
    do_action("transition_post_status", new_status_, old_status_, post_)
    #// 
    #// Fires when a post is transitioned from one status to another.
    #// 
    #// The dynamic portions of the hook name, `$new_status` and `$old status`,
    #// refer to the old and new post statuses, respectively.
    #// 
    #// @since 2.3.0
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action(str(old_status_) + str("_to_") + str(new_status_), post_)
    #// 
    #// Fires when a post is transitioned from one status to another.
    #// 
    #// The dynamic portions of the hook name, `$new_status` and `$post->post_type`,
    #// refer to the new post status and post type, respectively.
    #// 
    #// Please note: When this action is hooked using a particular post status (like
    #// 'publish', as `publish_{$post->post_type}`), it will fire both when a post is
    #// first transitioned to that status from something else, as well as upon
    #// subsequent post updates (old and new status are both the same).
    #// 
    #// Therefore, if you are looking to only fire a callback when a post is first
    #// transitioned to a status, use the {@see 'transition_post_status'} hook instead.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int     $post_id Post ID.
    #// @param WP_Post $post    Post object.
    #//
    do_action(str(new_status_) + str("_") + str(post_.post_type), post_.ID, post_)
# end def wp_transition_post_status
#// 
#// Comment, trackback, and pingback functions.
#// 
#// 
#// Add a URL to those already pinged.
#// 
#// @since 1.5.0
#// @since 4.7.0 `$post_id` can be a WP_Post object.
#// @since 4.7.0 `$uri` can be an array of URIs.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|WP_Post  $post_id Post object or ID.
#// @param string|array $uri     Ping URI or array of URIs.
#// @return int|false How many rows were updated.
#//
def add_ping(post_id_=None, uri_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    pung_ = php_trim(post_.pinged)
    pung_ = php_preg_split("/\\s/", pung_)
    if php_is_array(uri_):
        pung_ = php_array_merge(pung_, uri_)
    else:
        pung_[-1] = uri_
    # end if
    new_ = php_implode("\n", pung_)
    #// 
    #// Filters the new ping URL to add for the given post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $new New ping URL to add.
    #//
    new_ = apply_filters("add_ping", new_)
    return_ = wpdb_.update(wpdb_.posts, Array({"pinged": new_}), Array({"ID": post_.ID}))
    clean_post_cache(post_.ID)
    return return_
# end def add_ping
#// 
#// Retrieve enclosures already enclosed for a post.
#// 
#// @since 1.5.0
#// 
#// @param int $post_id Post ID.
#// @return string[] Array of enclosures for the given post.
#//
def get_enclosed(post_id_=None, *_args_):
    
    
    custom_fields_ = get_post_custom(post_id_)
    pung_ = Array()
    if (not php_is_array(custom_fields_)):
        return pung_
    # end if
    for key_,val_ in custom_fields_.items():
        if "enclosure" != key_ or (not php_is_array(val_)):
            continue
        # end if
        for enc_ in val_:
            enclosure_ = php_explode("\n", enc_)
            pung_[-1] = php_trim(enclosure_[0])
        # end for
    # end for
    #// 
    #// Filters the list of enclosures already enclosed for the given post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string[] $pung    Array of enclosures for the given post.
    #// @param int      $post_id Post ID.
    #//
    return apply_filters("get_enclosed", pung_, post_id_)
# end def get_enclosed
#// 
#// Retrieve URLs already pinged for a post.
#// 
#// @since 1.5.0
#// 
#// @since 4.7.0 `$post_id` can be a WP_Post object.
#// 
#// @param int|WP_Post $post_id Post ID or object.
#// @return bool|string[] Array of URLs already pinged for the given post, false if the post is not found.
#//
def get_pung(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    pung_ = php_trim(post_.pinged)
    pung_ = php_preg_split("/\\s/", pung_)
    #// 
    #// Filters the list of already-pinged URLs for the given post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string[] $pung Array of URLs already pinged for the given post.
    #//
    return apply_filters("get_pung", pung_)
# end def get_pung
#// 
#// Retrieve URLs that need to be pinged.
#// 
#// @since 1.5.0
#// @since 4.7.0 `$post_id` can be a WP_Post object.
#// 
#// @param int|WP_Post $post_id Post Object or ID
#// @param string[] List of URLs yet to ping.
#//
def get_to_ping(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    to_ping_ = sanitize_trackback_urls(post_.to_ping)
    to_ping_ = php_preg_split("/\\s/", to_ping_, -1, PREG_SPLIT_NO_EMPTY)
    #// 
    #// Filters the list of URLs yet to ping for the given post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string[] $to_ping List of URLs yet to ping.
    #//
    return apply_filters("get_to_ping", to_ping_)
# end def get_to_ping
#// 
#// Do trackbacks for a list of URLs.
#// 
#// @since 1.0.0
#// 
#// @param string $tb_list Comma separated list of URLs.
#// @param int    $post_id Post ID.
#//
def trackback_url_list(tb_list_=None, post_id_=None, *_args_):
    
    
    if (not php_empty(lambda : tb_list_)):
        #// Get post data.
        postdata_ = get_post(post_id_, ARRAY_A)
        #// Form an excerpt.
        excerpt_ = strip_tags(postdata_["post_excerpt"] if postdata_["post_excerpt"] else postdata_["post_content"])
        if php_strlen(excerpt_) > 255:
            excerpt_ = php_substr(excerpt_, 0, 252) + "&hellip;"
        # end if
        trackback_urls_ = php_explode(",", tb_list_)
        for tb_url_ in trackback_urls_:
            tb_url_ = php_trim(tb_url_)
            trackback(tb_url_, wp_unslash(postdata_["post_title"]), excerpt_, post_id_)
        # end for
    # end if
# end def trackback_url_list
#// 
#// Page functions.
#// 
#// 
#// Get a list of page IDs.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return string[] List of page IDs as strings.
#//
def get_all_page_ids(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    page_ids_ = wp_cache_get("all_page_ids", "posts")
    if (not php_is_array(page_ids_)):
        page_ids_ = wpdb_.get_col(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'page'"))
        wp_cache_add("all_page_ids", page_ids_, "posts")
    # end if
    return page_ids_
# end def get_all_page_ids
#// 
#// Retrieves page data given a page ID or page object.
#// 
#// Use get_post() instead of get_page().
#// 
#// @since 1.5.1
#// @deprecated 3.5.0 Use get_post()
#// 
#// @param int|WP_Post $page   Page object or page ID. Passed by reference.
#// @param string      $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Post object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string      $filter Optional. How the return value should be filtered. Accepts 'raw',
#// 'edit', 'db', 'display'. Default 'raw'.
#// @return WP_Post|array|null WP_Post or array on success, null on failure.
#//
def get_page(page_=None, output_=None, filter_="raw", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    return get_post(page_, output_, filter_)
# end def get_page
#// 
#// Retrieves a page given its path.
#// 
#// @since 2.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string       $page_path Page path.
#// @param string       $output    Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Post object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string|array $post_type Optional. Post type or array of post types. Default 'page'.
#// @return WP_Post|array|null WP_Post (or array) on success, or null on failure.
#//
def get_page_by_path(page_path_=None, output_=None, post_type_="page", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    last_changed_ = wp_cache_get_last_changed("posts")
    hash_ = php_md5(page_path_ + serialize(post_type_))
    cache_key_ = str("get_page_by_path:") + str(hash_) + str(":") + str(last_changed_)
    cached_ = wp_cache_get(cache_key_, "posts")
    if False != cached_:
        #// Special case: '0' is a bad `$page_path`.
        if "0" == cached_ or 0 == cached_:
            return
        else:
            return get_post(cached_, output_)
        # end if
    # end if
    page_path_ = rawurlencode(urldecode(page_path_))
    page_path_ = php_str_replace("%2F", "/", page_path_)
    page_path_ = php_str_replace("%20", " ", page_path_)
    parts_ = php_explode("/", php_trim(page_path_, "/"))
    parts_ = php_array_map("sanitize_title_for_query", parts_)
    escaped_parts_ = esc_sql(parts_)
    in_string_ = "'" + php_implode("','", escaped_parts_) + "'"
    if php_is_array(post_type_):
        post_types_ = post_type_
    else:
        post_types_ = Array(post_type_, "attachment")
    # end if
    post_types_ = esc_sql(post_types_)
    post_type_in_string_ = "'" + php_implode("','", post_types_) + "'"
    sql_ = str("\n      SELECT ID, post_name, post_parent, post_type\n      FROM ") + str(wpdb_.posts) + str("\n        WHERE post_name IN (") + str(in_string_) + str(")\n     AND post_type IN (") + str(post_type_in_string_) + str(")\n ")
    pages_ = wpdb_.get_results(sql_, OBJECT_K)
    revparts_ = php_array_reverse(parts_)
    foundid_ = 0
    for page_ in pages_:
        if page_.post_name == revparts_[0]:
            count_ = 0
            p_ = page_
            #// 
            #// Loop through the given path parts from right to left,
            #// ensuring each matches the post ancestry.
            #//
            while True:
                
                if not (0 != p_.post_parent and (php_isset(lambda : pages_[p_.post_parent]))):
                    break
                # end if
                count_ += 1
                parent_ = pages_[p_.post_parent]
                if (not (php_isset(lambda : revparts_[count_]))) or parent_.post_name != revparts_[count_]:
                    break
                # end if
                p_ = parent_
            # end while
            if 0 == p_.post_parent and php_count(revparts_) == count_ + 1 and p_.post_name == revparts_[count_]:
                foundid_ = page_.ID
                if page_.post_type == post_type_:
                    break
                # end if
            # end if
        # end if
    # end for
    #// We cache misses as well as hits.
    wp_cache_set(cache_key_, foundid_, "posts")
    if foundid_:
        return get_post(foundid_, output_)
    # end if
# end def get_page_by_path
#// 
#// Retrieve a page given its title.
#// 
#// If more than one post uses the same title, the post with the smallest ID will be returned.
#// Be careful: in case of more than one post having the same title, it will check the oldest
#// publication date, not the smallest ID.
#// 
#// Because this function uses the MySQL '=' comparison, $page_title will usually be matched
#// as case-insensitive with default collation.
#// 
#// @since 2.1.0
#// @since 3.0.0 The `$post_type` parameter was added.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string       $page_title Page title.
#// @param string       $output     Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Post object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string|array $post_type  Optional. Post type or array of post types. Default 'page'.
#// @return WP_Post|array|null WP_Post (or array) on success, or null on failure.
#//
def get_page_by_title(page_title_=None, output_=None, post_type_="page", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_is_array(post_type_):
        post_type_ = esc_sql(post_type_)
        post_type_in_string_ = "'" + php_implode("','", post_type_) + "'"
        sql_ = wpdb_.prepare(str("\n            SELECT ID\n         FROM ") + str(wpdb_.posts) + str("\n            WHERE post_title = %s\n         AND post_type IN (") + str(post_type_in_string_) + str(")\n     "), page_title_)
    else:
        sql_ = wpdb_.prepare(str("\n            SELECT ID\n         FROM ") + str(wpdb_.posts) + str("""\n          WHERE post_title = %s\n         AND post_type = %s\n        """), page_title_, post_type_)
    # end if
    page_ = wpdb_.get_var(sql_)
    if page_:
        return get_post(page_, output_)
    # end if
# end def get_page_by_title
#// 
#// Identify descendants of a given page ID in a list of page objects.
#// 
#// Descendants are identified from the `$pages` array passed to the function. No database queries are performed.
#// 
#// @since 1.5.1
#// 
#// @param int   $page_id Page ID.
#// @param array $pages   List of page objects from which descendants should be identified.
#// @return array List of page children.
#//
def get_page_children(page_id_=None, pages_=None, *_args_):
    
    
    #// Build a hash of ID -> children.
    children_ = Array()
    for page_ in pages_:
        children_[php_intval(page_.post_parent)][-1] = page_
    # end for
    page_list_ = Array()
    #// Start the search by looking at immediate children.
    if (php_isset(lambda : children_[page_id_])):
        #// Always start at the end of the stack in order to preserve original `$pages` order.
        to_look_ = php_array_reverse(children_[page_id_])
        while True:
            
            if not (to_look_):
                break
            # end if
            p_ = php_array_pop(to_look_)
            page_list_[-1] = p_
            if (php_isset(lambda : children_[p_.ID])):
                for child_ in php_array_reverse(children_[p_.ID]):
                    #// Append to the `$to_look` stack to descend the tree.
                    to_look_[-1] = child_
                # end for
            # end if
        # end while
    # end if
    return page_list_
# end def get_page_children
#// 
#// Order the pages with children under parents in a flat list.
#// 
#// It uses auxiliary structure to hold parent-children relationships and
#// runs in O(N) complexity
#// 
#// @since 2.0.0
#// 
#// @param WP_Post[] $pages   Posts array (passed by reference).
#// @param int       $page_id Optional. Parent page ID. Default 0.
#// @return string[] Array of post names keyed by ID and arranged by hierarchy. Children immediately follow their parents.
#//
def get_page_hierarchy(pages_=None, page_id_=0, *_args_):
    
    
    if php_empty(lambda : pages_):
        return Array()
    # end if
    children_ = Array()
    for p_ in pages_:
        parent_id_ = php_intval(p_.post_parent)
        children_[parent_id_][-1] = p_
    # end for
    result_ = Array()
    _page_traverse_name(page_id_, children_, result_)
    return result_
# end def get_page_hierarchy
#// 
#// Traverse and return all the nested children post names of a root page.
#// 
#// $children contains parent-children relations
#// 
#// @since 2.9.0
#// @access private
#// 
#// @see _page_traverse_name()
#// 
#// @param int      $page_id  Page ID.
#// @param array    $children Parent-children relations (passed by reference).
#// @param string[] $result   Array of page names keyed by ID (passed by reference).
#//
def _page_traverse_name(page_id_=None, children_=None, result_=None, *_args_):
    
    
    if (php_isset(lambda : children_[page_id_])):
        for child_ in children_[page_id_]:
            result_[child_.ID] = child_.post_name
            _page_traverse_name(child_.ID, children_, result_)
        # end for
    # end if
# end def _page_traverse_name
#// 
#// Build the URI path for a page.
#// 
#// Sub pages will be in the "directory" under the parent page post name.
#// 
#// @since 1.5.0
#// @since 4.6.0 The `$page` parameter was made optional.
#// 
#// @param WP_Post|object|int $page Optional. Page ID or WP_Post object. Default is global $post.
#// @return string|false Page URI, false on error.
#//
def get_page_uri(page_=0, *_args_):
    
    
    if (not type(page_).__name__ == "WP_Post"):
        page_ = get_post(page_)
    # end if
    if (not page_):
        return False
    # end if
    uri_ = page_.post_name
    for parent_ in page_.ancestors:
        parent_ = get_post(parent_)
        if parent_ and parent_.post_name:
            uri_ = parent_.post_name + "/" + uri_
        # end if
    # end for
    #// 
    #// Filters the URI for a page.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string  $uri  Page URI.
    #// @param WP_Post $page Page object.
    #//
    return apply_filters("get_page_uri", uri_, page_)
# end def get_page_uri
#// 
#// Retrieve a list of pages (or hierarchical post type items).
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @since 1.5.0
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments to retrieve pages.
#// 
#// @type int          $child_of     Page ID to return child and grandchild pages of. Note: The value
#// of `$hierarchical` has no bearing on whether `$child_of` returns
#// hierarchical results. Default 0, or no restriction.
#// @type string       $sort_order   How to sort retrieved pages. Accepts 'ASC', 'DESC'. Default 'ASC'.
#// @type string       $sort_column  What columns to sort pages by, comma-separated. Accepts 'post_author',
#// 'post_date', 'post_title', 'post_name', 'post_modified', 'menu_order',
#// 'post_modified_gmt', 'post_parent', 'ID', 'rand', 'comment_count'.
#// 'post_' can be omitted for any values that start with it.
#// Default 'post_title'.
#// @type bool         $hierarchical Whether to return pages hierarchically. If false in conjunction with
#// `$child_of` also being false, both arguments will be disregarded.
#// Default true.
#// @type array        $exclude      Array of page IDs to exclude. Default empty array.
#// @type array        $include      Array of page IDs to include. Cannot be used with `$child_of`,
#// `$parent`, `$exclude`, `$meta_key`, `$meta_value`, or `$hierarchical`.
#// Default empty array.
#// @type string       $meta_key     Only include pages with this meta key. Default empty.
#// @type string       $meta_value   Only include pages with this meta value. Requires `$meta_key`.
#// Default empty.
#// @type string       $authors      A comma-separated list of author IDs. Default empty.
#// @type int          $parent       Page ID to return direct children of. Default -1, or no restriction.
#// @type string|array $exclude_tree Comma-separated string or array of page IDs to exclude.
#// Default empty array.
#// @type int          $number       The number of pages to return. Default 0, or all pages.
#// @type int          $offset       The number of pages to skip before returning. Requires `$number`.
#// Default 0.
#// @type string       $post_type    The post type to query. Default 'page'.
#// @type string|array $post_status  A comma-separated list or array of post statuses to include.
#// Default 'publish'.
#// }
#// @return array|false List of pages matching defaults or `$args`.
#//
def get_pages(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    defaults_ = Array({"child_of": 0, "sort_order": "ASC", "sort_column": "post_title", "hierarchical": 1, "exclude": Array(), "include": Array(), "meta_key": "", "meta_value": "", "authors": "", "parent": -1, "exclude_tree": Array(), "number": "", "offset": 0, "post_type": "page", "post_status": "publish"})
    parsed_args_ = wp_parse_args(args_, defaults_)
    number_ = php_int(parsed_args_["number"])
    offset_ = php_int(parsed_args_["offset"])
    child_of_ = php_int(parsed_args_["child_of"])
    hierarchical_ = parsed_args_["hierarchical"]
    exclude_ = parsed_args_["exclude"]
    meta_key_ = parsed_args_["meta_key"]
    meta_value_ = parsed_args_["meta_value"]
    parent_ = parsed_args_["parent"]
    post_status_ = parsed_args_["post_status"]
    #// Make sure the post type is hierarchical.
    hierarchical_post_types_ = get_post_types(Array({"hierarchical": True}))
    if (not php_in_array(parsed_args_["post_type"], hierarchical_post_types_)):
        return False
    # end if
    if parent_ > 0 and (not child_of_):
        hierarchical_ = False
    # end if
    #// Make sure we have a valid post status.
    if (not php_is_array(post_status_)):
        post_status_ = php_explode(",", post_status_)
    # end if
    if php_array_diff(post_status_, get_post_stati()):
        return False
    # end if
    #// $args can be whatever, only use the args defined in defaults to compute the key.
    key_ = php_md5(serialize(wp_array_slice_assoc(parsed_args_, php_array_keys(defaults_))))
    last_changed_ = wp_cache_get_last_changed("posts")
    cache_key_ = str("get_pages:") + str(key_) + str(":") + str(last_changed_)
    cache_ = wp_cache_get(cache_key_, "posts")
    if False != cache_:
        #// Convert to WP_Post instances.
        pages_ = php_array_map("get_post", cache_)
        #// This filter is documented in wp-includes/post.php
        pages_ = apply_filters("get_pages", pages_, parsed_args_)
        return pages_
    # end if
    inclusions_ = ""
    if (not php_empty(lambda : parsed_args_["include"])):
        child_of_ = 0
        #// Ignore child_of, parent, exclude, meta_key, and meta_value params if using include.
        parent_ = -1
        exclude_ = ""
        meta_key_ = ""
        meta_value_ = ""
        hierarchical_ = False
        incpages_ = wp_parse_id_list(parsed_args_["include"])
        if (not php_empty(lambda : incpages_)):
            inclusions_ = " AND ID IN (" + php_implode(",", incpages_) + ")"
        # end if
    # end if
    exclusions_ = ""
    if (not php_empty(lambda : exclude_)):
        expages_ = wp_parse_id_list(exclude_)
        if (not php_empty(lambda : expages_)):
            exclusions_ = " AND ID NOT IN (" + php_implode(",", expages_) + ")"
        # end if
    # end if
    author_query_ = ""
    if (not php_empty(lambda : parsed_args_["authors"])):
        post_authors_ = wp_parse_list(parsed_args_["authors"])
        if (not php_empty(lambda : post_authors_)):
            for post_author_ in post_authors_:
                #// Do we have an author id or an author login?
                if 0 == php_intval(post_author_):
                    post_author_ = get_user_by("login", post_author_)
                    if php_empty(lambda : post_author_):
                        continue
                    # end if
                    if php_empty(lambda : post_author_.ID):
                        continue
                    # end if
                    post_author_ = post_author_.ID
                # end if
                if "" == author_query_:
                    author_query_ = wpdb_.prepare(" post_author = %d ", post_author_)
                else:
                    author_query_ += wpdb_.prepare(" OR post_author = %d ", post_author_)
                # end if
            # end for
            if "" != author_query_:
                author_query_ = str(" AND (") + str(author_query_) + str(")")
            # end if
        # end if
    # end if
    join_ = ""
    where_ = str(exclusions_) + str(" ") + str(inclusions_) + str(" ")
    if "" != meta_key_ or "" != meta_value_:
        join_ = str(" LEFT JOIN ") + str(wpdb_.postmeta) + str(" ON ( ") + str(wpdb_.posts) + str(".ID = ") + str(wpdb_.postmeta) + str(".post_id )")
        #// meta_key and meta_value might be slashed.
        meta_key_ = wp_unslash(meta_key_)
        meta_value_ = wp_unslash(meta_value_)
        if "" != meta_key_:
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.postmeta) + str(".meta_key = %s"), meta_key_)
        # end if
        if "" != meta_value_:
            where_ += wpdb_.prepare(str(" AND ") + str(wpdb_.postmeta) + str(".meta_value = %s"), meta_value_)
        # end if
    # end if
    if php_is_array(parent_):
        post_parent__in_ = php_implode(",", php_array_map("absint", parent_))
        if (not php_empty(lambda : post_parent__in_)):
            where_ += str(" AND post_parent IN (") + str(post_parent__in_) + str(")")
        # end if
    elif parent_ >= 0:
        where_ += wpdb_.prepare(" AND post_parent = %d ", parent_)
    # end if
    if 1 == php_count(post_status_):
        where_post_type_ = wpdb_.prepare("post_type = %s AND post_status = %s", parsed_args_["post_type"], reset(post_status_))
    else:
        post_status_ = php_implode("', '", post_status_)
        where_post_type_ = wpdb_.prepare(str("post_type = %s AND post_status IN ('") + str(post_status_) + str("')"), parsed_args_["post_type"])
    # end if
    orderby_array_ = Array()
    allowed_keys_ = Array("author", "post_author", "date", "post_date", "title", "post_title", "name", "post_name", "modified", "post_modified", "modified_gmt", "post_modified_gmt", "menu_order", "parent", "post_parent", "ID", "rand", "comment_count")
    for orderby_ in php_explode(",", parsed_args_["sort_column"]):
        orderby_ = php_trim(orderby_)
        if (not php_in_array(orderby_, allowed_keys_)):
            continue
        # end if
        for case in Switch(orderby_):
            if case("menu_order"):
                break
            # end if
            if case("ID"):
                orderby_ = str(wpdb_.posts) + str(".ID")
                break
            # end if
            if case("rand"):
                orderby_ = "RAND()"
                break
            # end if
            if case("comment_count"):
                orderby_ = str(wpdb_.posts) + str(".comment_count")
                break
            # end if
            if case():
                if 0 == php_strpos(orderby_, "post_"):
                    orderby_ = str(wpdb_.posts) + str(".") + orderby_
                else:
                    orderby_ = str(wpdb_.posts) + str(".post_") + orderby_
                # end if
            # end if
        # end for
        orderby_array_[-1] = orderby_
    # end for
    sort_column_ = php_implode(",", orderby_array_) if (not php_empty(lambda : orderby_array_)) else str(wpdb_.posts) + str(".post_title")
    sort_order_ = php_strtoupper(parsed_args_["sort_order"])
    if "" != sort_order_ and (not php_in_array(sort_order_, Array("ASC", "DESC"))):
        sort_order_ = "ASC"
    # end if
    query_ = str("SELECT * FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" WHERE (") + str(where_post_type_) + str(") ") + str(where_) + str(" ")
    query_ += author_query_
    query_ += " ORDER BY " + sort_column_ + " " + sort_order_
    if (not php_empty(lambda : number_)):
        query_ += " LIMIT " + offset_ + "," + number_
    # end if
    pages_ = wpdb_.get_results(query_)
    if php_empty(lambda : pages_):
        wp_cache_set(cache_key_, Array(), "posts")
        #// This filter is documented in wp-includes/post.php
        pages_ = apply_filters("get_pages", Array(), parsed_args_)
        return pages_
    # end if
    #// Sanitize before caching so it'll only get done once.
    num_pages_ = php_count(pages_)
    i_ = 0
    while i_ < num_pages_:
        
        pages_[i_] = sanitize_post(pages_[i_], "raw")
        i_ += 1
    # end while
    #// Update cache.
    update_post_cache(pages_)
    if child_of_ or hierarchical_:
        pages_ = get_page_children(child_of_, pages_)
    # end if
    if (not php_empty(lambda : parsed_args_["exclude_tree"])):
        exclude_ = wp_parse_id_list(parsed_args_["exclude_tree"])
        for id_ in exclude_:
            children_ = get_page_children(id_, pages_)
            for child_ in children_:
                exclude_[-1] = child_.ID
            # end for
        # end for
        num_pages_ = php_count(pages_)
        i_ = 0
        while i_ < num_pages_:
            
            if php_in_array(pages_[i_].ID, exclude_):
                pages_[i_] = None
            # end if
            i_ += 1
        # end while
    # end if
    page_structure_ = Array()
    for page_ in pages_:
        page_structure_[-1] = page_.ID
    # end for
    wp_cache_set(cache_key_, page_structure_, "posts")
    #// Convert to WP_Post instances.
    pages_ = php_array_map("get_post", pages_)
    #// 
    #// Filters the retrieved list of pages.
    #// 
    #// @since 2.1.0
    #// 
    #// @param WP_Post[] $pages       Array of page objects.
    #// @param array     $parsed_args Array of get_pages() arguments.
    #//
    return apply_filters("get_pages", pages_, parsed_args_)
# end def get_pages
#// 
#// Attachment functions.
#// 
#// 
#// Determines whether an attachment URI is local and really an attachment.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.0.0
#// 
#// @param string $url URL to check
#// @return bool True on success, false on failure.
#//
def is_local_attachment(url_=None, *_args_):
    
    
    if php_strpos(url_, home_url()) == False:
        return False
    # end if
    if php_strpos(url_, home_url("/?attachment_id=")) != False:
        return True
    # end if
    id_ = url_to_postid(url_)
    if id_:
        post_ = get_post(id_)
        if "attachment" == post_.post_type:
            return True
        # end if
    # end if
    return False
# end def is_local_attachment
#// 
#// Insert an attachment.
#// 
#// If you set the 'ID' in the $args parameter, it will mean that you are
#// updating and attempt to update the attachment. You can also set the
#// attachment name or title by setting the key 'post_name' or 'post_title'.
#// 
#// You can set the dates for the attachment manually by setting the 'post_date'
#// and 'post_date_gmt' keys' values.
#// 
#// By default, the comments will use the default settings for whether the
#// comments are allowed. You can close them manually or keep them open by
#// setting the value for the 'comment_status' key.
#// 
#// @since 2.0.0
#// @since 4.7.0 Added the `$wp_error` parameter to allow a WP_Error to be returned on failure.
#// 
#// @see wp_insert_post()
#// 
#// @param string|array $args     Arguments for inserting an attachment.
#// @param string       $file     Optional. Filename.
#// @param int          $parent   Optional. Parent post ID.
#// @param bool         $wp_error Optional. Whether to return a WP_Error on failure. Default false.
#// @return int|WP_Error The attachment ID on success. The value 0 or WP_Error on failure.
#//
def wp_insert_attachment(args_=None, file_=None, parent_=0, wp_error_=None, *_args_):
    if file_ is None:
        file_ = False
    # end if
    if wp_error_ is None:
        wp_error_ = False
    # end if
    
    defaults_ = Array({"file": file_, "post_parent": 0})
    data_ = wp_parse_args(args_, defaults_)
    if (not php_empty(lambda : parent_)):
        data_["post_parent"] = parent_
    # end if
    data_["post_type"] = "attachment"
    return wp_insert_post(data_, wp_error_)
# end def wp_insert_attachment
#// 
#// Trash or delete an attachment.
#// 
#// When an attachment is permanently deleted, the file will also be removed.
#// Deletion removes all post meta fields, taxonomy, comments, etc. associated
#// with the attachment (except the main post).
#// 
#// The attachment is moved to the Trash instead of permanently deleted unless Trash
#// for media is disabled, item is already in the Trash, or $force_delete is true.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int  $post_id      Attachment ID.
#// @param bool $force_delete Optional. Whether to bypass Trash and force deletion.
#// Default false.
#// @return WP_Post|false|null Post data on success, false or null on failure.
#//
def wp_delete_attachment(post_id_=None, force_delete_=None, *_args_):
    if force_delete_ is None:
        force_delete_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.posts) + str(" WHERE ID = %d"), post_id_))
    if (not post_):
        return post_
    # end if
    post_ = get_post(post_)
    if "attachment" != post_.post_type:
        return False
    # end if
    if (not force_delete_) and EMPTY_TRASH_DAYS and MEDIA_TRASH and "trash" != post_.post_status:
        return wp_trash_post(post_id_)
    # end if
    delete_post_meta(post_id_, "_wp_trash_meta_status")
    delete_post_meta(post_id_, "_wp_trash_meta_time")
    meta_ = wp_get_attachment_metadata(post_id_)
    backup_sizes_ = get_post_meta(post_.ID, "_wp_attachment_backup_sizes", True)
    file_ = get_attached_file(post_id_)
    if is_multisite():
        delete_transient("dirsize_cache")
    # end if
    #// 
    #// Fires before an attachment is deleted, at the start of wp_delete_attachment().
    #// 
    #// @since 2.0.0
    #// 
    #// @param int $post_id Attachment ID.
    #//
    do_action("delete_attachment", post_id_)
    wp_delete_object_term_relationships(post_id_, Array("category", "post_tag"))
    wp_delete_object_term_relationships(post_id_, get_object_taxonomies(post_.post_type))
    #// Delete all for any posts.
    delete_metadata("post", None, "_thumbnail_id", post_id_, True)
    wp_defer_comment_counting(True)
    comment_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT comment_ID FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d"), post_id_))
    for comment_id_ in comment_ids_:
        wp_delete_comment(comment_id_, True)
    # end for
    wp_defer_comment_counting(False)
    post_meta_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.postmeta) + str(" WHERE post_id = %d "), post_id_))
    for mid_ in post_meta_ids_:
        delete_metadata_by_mid("post", mid_)
    # end for
    #// This action is documented in wp-includes/post.php
    do_action("delete_post", post_id_)
    result_ = wpdb_.delete(wpdb_.posts, Array({"ID": post_id_}))
    if (not result_):
        return False
    # end if
    #// This action is documented in wp-includes/post.php
    do_action("deleted_post", post_id_)
    wp_delete_attachment_files(post_id_, meta_, backup_sizes_, file_)
    clean_post_cache(post_)
    return post_
# end def wp_delete_attachment
#// 
#// Deletes all files that belong to the given attachment.
#// 
#// @since 4.9.7
#// 
#// @param int    $post_id      Attachment ID.
#// @param array  $meta         The attachment's meta data.
#// @param array  $backup_sizes The meta data for the attachment's backup images.
#// @param string $file         Absolute path to the attachment's file.
#// @return bool True on success, false on failure.
#//
def wp_delete_attachment_files(post_id_=None, meta_=None, backup_sizes_=None, file_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    uploadpath_ = wp_get_upload_dir()
    deleted_ = True
    if (not php_empty(lambda : meta_["thumb"])):
        #// Don't delete the thumb if another attachment uses it.
        if (not wpdb_.get_row(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.postmeta) + str(" WHERE meta_key = '_wp_attachment_metadata' AND meta_value LIKE %s AND post_id <> %d"), "%" + wpdb_.esc_like(meta_["thumb"]) + "%", post_id_))):
            thumbfile_ = php_str_replace(wp_basename(file_), meta_["thumb"], file_)
            if (not php_empty(lambda : thumbfile_)):
                thumbfile_ = path_join(uploadpath_["basedir"], thumbfile_)
                thumbdir_ = path_join(uploadpath_["basedir"], php_dirname(file_))
                if (not wp_delete_file_from_directory(thumbfile_, thumbdir_)):
                    deleted_ = False
                # end if
            # end if
        # end if
    # end if
    #// Remove intermediate and backup images if there are any.
    if (php_isset(lambda : meta_["sizes"])) and php_is_array(meta_["sizes"]):
        intermediate_dir_ = path_join(uploadpath_["basedir"], php_dirname(file_))
        for size_,sizeinfo_ in meta_["sizes"].items():
            intermediate_file_ = php_str_replace(wp_basename(file_), sizeinfo_["file"], file_)
            if (not php_empty(lambda : intermediate_file_)):
                intermediate_file_ = path_join(uploadpath_["basedir"], intermediate_file_)
                if (not wp_delete_file_from_directory(intermediate_file_, intermediate_dir_)):
                    deleted_ = False
                # end if
            # end if
        # end for
    # end if
    if (not php_empty(lambda : meta_["original_image"])):
        if php_empty(lambda : intermediate_dir_):
            intermediate_dir_ = path_join(uploadpath_["basedir"], php_dirname(file_))
        # end if
        original_image_ = php_str_replace(wp_basename(file_), meta_["original_image"], file_)
        if (not php_empty(lambda : original_image_)):
            original_image_ = path_join(uploadpath_["basedir"], original_image_)
            if (not wp_delete_file_from_directory(original_image_, intermediate_dir_)):
                deleted_ = False
            # end if
        # end if
    # end if
    if php_is_array(backup_sizes_):
        del_dir_ = path_join(uploadpath_["basedir"], php_dirname(meta_["file"]))
        for size_ in backup_sizes_:
            del_file_ = path_join(php_dirname(meta_["file"]), size_["file"])
            if (not php_empty(lambda : del_file_)):
                del_file_ = path_join(uploadpath_["basedir"], del_file_)
                if (not wp_delete_file_from_directory(del_file_, del_dir_)):
                    deleted_ = False
                # end if
            # end if
        # end for
    # end if
    if (not wp_delete_file_from_directory(file_, uploadpath_["basedir"])):
        deleted_ = False
    # end if
    return deleted_
# end def wp_delete_attachment_files
#// 
#// Retrieve attachment meta field for attachment ID.
#// 
#// @since 2.1.0
#// 
#// @param int  $attachment_id Attachment post ID. Defaults to global $post.
#// @param bool $unfiltered    Optional. If true, filters are not run. Default false.
#// @return mixed Attachment meta field. False on failure.
#//
def wp_get_attachment_metadata(attachment_id_=0, unfiltered_=None, *_args_):
    if unfiltered_ is None:
        unfiltered_ = False
    # end if
    
    attachment_id_ = php_int(attachment_id_)
    post_ = get_post(attachment_id_)
    if (not post_):
        return False
    # end if
    data_ = get_post_meta(post_.ID, "_wp_attachment_metadata", True)
    if unfiltered_:
        return data_
    # end if
    #// 
    #// Filters the attachment meta data.
    #// 
    #// @since 2.1.0
    #// 
    #// @param array|bool $data          Array of meta data for the given attachment, or false
    #// if the object does not exist.
    #// @param int        $attachment_id Attachment post ID.
    #//
    return apply_filters("wp_get_attachment_metadata", data_, post_.ID)
# end def wp_get_attachment_metadata
#// 
#// Update metadata for an attachment.
#// 
#// @since 2.1.0
#// 
#// @param int   $attachment_id Attachment post ID.
#// @param array $data          Attachment meta data.
#// @return int|bool False if $post is invalid.
#//
def wp_update_attachment_metadata(attachment_id_=None, data_=None, *_args_):
    
    
    attachment_id_ = php_int(attachment_id_)
    post_ = get_post(attachment_id_)
    if (not post_):
        return False
    # end if
    #// 
    #// Filters the updated attachment meta data.
    #// 
    #// @since 2.1.0
    #// 
    #// @param array $data          Array of updated attachment meta data.
    #// @param int   $attachment_id Attachment post ID.
    #//
    data_ = apply_filters("wp_update_attachment_metadata", data_, post_.ID)
    if data_:
        return update_post_meta(post_.ID, "_wp_attachment_metadata", data_)
    else:
        return delete_post_meta(post_.ID, "_wp_attachment_metadata")
    # end if
# end def wp_update_attachment_metadata
#// 
#// Retrieve the URL for an attachment.
#// 
#// @since 2.1.0
#// 
#// @global string $pagenow
#// 
#// @param int $attachment_id Optional. Attachment post ID. Defaults to global $post.
#// @return string|false Attachment URL, otherwise false.
#//
def wp_get_attachment_url(attachment_id_=0, *_args_):
    
    
    attachment_id_ = php_int(attachment_id_)
    post_ = get_post(attachment_id_)
    if (not post_):
        return False
    # end if
    if "attachment" != post_.post_type:
        return False
    # end if
    url_ = ""
    #// Get attached file.
    file_ = get_post_meta(post_.ID, "_wp_attached_file", True)
    if file_:
        #// Get upload directory.
        uploads_ = wp_get_upload_dir()
        if uploads_ and False == uploads_["error"]:
            #// Check that the upload base exists in the file location.
            if 0 == php_strpos(file_, uploads_["basedir"]):
                #// Replace file location with url location.
                url_ = php_str_replace(uploads_["basedir"], uploads_["baseurl"], file_)
            elif False != php_strpos(file_, "wp-content/uploads"):
                #// Get the directory name relative to the basedir (back compat for pre-2.7 uploads).
                url_ = trailingslashit(uploads_["baseurl"] + "/" + _wp_get_attachment_relative_path(file_)) + wp_basename(file_)
            else:
                #// It's a newly-uploaded file, therefore $file is relative to the basedir.
                url_ = uploads_["baseurl"] + str("/") + str(file_)
            # end if
        # end if
    # end if
    #// 
    #// If any of the above options failed, Fallback on the GUID as used pre-2.7,
    #// not recommended to rely upon this.
    #//
    if php_empty(lambda : url_):
        url_ = get_the_guid(post_.ID)
    # end if
    #// On SSL front end, URLs should be HTTPS.
    if is_ssl() and (not is_admin()) and "wp-login.php" != PHP_GLOBALS["pagenow"]:
        url_ = set_url_scheme(url_)
    # end if
    #// 
    #// Filters the attachment URL.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $url           URL for the given attachment.
    #// @param int    $attachment_id Attachment post ID.
    #//
    url_ = apply_filters("wp_get_attachment_url", url_, post_.ID)
    if php_empty(lambda : url_):
        return False
    # end if
    return url_
# end def wp_get_attachment_url
#// 
#// Retrieves the caption for an attachment.
#// 
#// @since 4.6.0
#// 
#// @param int $post_id Optional. Attachment ID. Default is the ID of the global `$post`.
#// @return string|false False on failure. Attachment caption on success.
#//
def wp_get_attachment_caption(post_id_=0, *_args_):
    
    
    post_id_ = php_int(post_id_)
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    if "attachment" != post_.post_type:
        return False
    # end if
    caption_ = post_.post_excerpt
    #// 
    #// Filters the attachment caption.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $caption Caption for the given attachment.
    #// @param int    $post_id Attachment ID.
    #//
    return apply_filters("wp_get_attachment_caption", caption_, post_.ID)
# end def wp_get_attachment_caption
#// 
#// Retrieve thumbnail for an attachment.
#// 
#// @since 2.1.0
#// 
#// @param int $post_id Optional. Attachment ID. Default 0.
#// @return string|false False on failure. Thumbnail file path on success.
#//
def wp_get_attachment_thumb_file(post_id_=0, *_args_):
    
    
    post_id_ = php_int(post_id_)
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    imagedata_ = wp_get_attachment_metadata(post_.ID)
    if (not php_is_array(imagedata_)):
        return False
    # end if
    file_ = get_attached_file(post_.ID)
    if (not php_empty(lambda : imagedata_["thumb"])):
        thumbfile_ = php_str_replace(wp_basename(file_), imagedata_["thumb"], file_)
        if php_file_exists(thumbfile_):
            #// 
            #// Filters the attachment thumbnail file path.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string $thumbfile File path to the attachment thumbnail.
            #// @param int    $post_id   Attachment ID.
            #//
            return apply_filters("wp_get_attachment_thumb_file", thumbfile_, post_.ID)
        # end if
    # end if
    return False
# end def wp_get_attachment_thumb_file
#// 
#// Retrieve URL for an attachment thumbnail.
#// 
#// @since 2.1.0
#// 
#// @param int $post_id Optional. Attachment ID. Default 0.
#// @return string|false False on failure. Thumbnail URL on success.
#//
def wp_get_attachment_thumb_url(post_id_=0, *_args_):
    
    
    post_id_ = php_int(post_id_)
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    url_ = wp_get_attachment_url(post_.ID)
    if (not url_):
        return False
    # end if
    sized_ = image_downsize(post_id_, "thumbnail")
    if sized_:
        return sized_[0]
    # end if
    thumb_ = wp_get_attachment_thumb_file(post_.ID)
    if (not thumb_):
        return False
    # end if
    url_ = php_str_replace(wp_basename(url_), wp_basename(thumb_), url_)
    #// 
    #// Filters the attachment thumbnail URL.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $url     URL for the attachment thumbnail.
    #// @param int    $post_id Attachment ID.
    #//
    return apply_filters("wp_get_attachment_thumb_url", url_, post_.ID)
# end def wp_get_attachment_thumb_url
#// 
#// Verifies an attachment is of a given type.
#// 
#// @since 4.2.0
#// 
#// @param string      $type Attachment type. Accepts 'image', 'audio', or 'video'.
#// @param int|WP_Post $post Optional. Attachment ID or object. Default is global $post.
#// @return bool True if one of the accepted types, false otherwise.
#//
def wp_attachment_is(type_=None, post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    file_ = get_attached_file(post_.ID)
    if (not file_):
        return False
    # end if
    if 0 == php_strpos(post_.post_mime_type, type_ + "/"):
        return True
    # end if
    check_ = wp_check_filetype(file_)
    if php_empty(lambda : check_["ext"]):
        return False
    # end if
    ext_ = check_["ext"]
    if "import" != post_.post_mime_type:
        return type_ == ext_
    # end if
    for case in Switch(type_):
        if case("image"):
            image_exts_ = Array("jpg", "jpeg", "jpe", "gif", "png")
            return php_in_array(ext_, image_exts_)
        # end if
        if case("audio"):
            return php_in_array(ext_, wp_get_audio_extensions())
        # end if
        if case("video"):
            return php_in_array(ext_, wp_get_video_extensions())
        # end if
        if case():
            return type_ == ext_
        # end if
    # end for
# end def wp_attachment_is
#// 
#// Determines whether an attachment is an image.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.1.0
#// @since 4.2.0 Modified into wrapper for wp_attachment_is() and
#// allowed WP_Post object to be passed.
#// 
#// @param int|WP_Post $post Optional. Attachment ID or object. Default is global $post.
#// @return bool Whether the attachment is an image.
#//
def wp_attachment_is_image(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    return wp_attachment_is("image", post_)
# end def wp_attachment_is_image
#// 
#// Retrieve the icon for a MIME type or attachment.
#// 
#// @since 2.1.0
#// 
#// @param string|int $mime MIME type or attachment ID.
#// @return string|false Icon, false otherwise.
#//
def wp_mime_type_icon(mime_=0, *_args_):
    
    
    if (not php_is_numeric(mime_)):
        icon_ = wp_cache_get(str("mime_type_icon_") + str(mime_))
    # end if
    post_id_ = 0
    if php_empty(lambda : icon_):
        post_mimes_ = Array()
        if php_is_numeric(mime_):
            mime_ = php_int(mime_)
            post_ = get_post(mime_)
            if post_:
                post_id_ = php_int(post_.ID)
                file_ = get_attached_file(post_id_)
                ext_ = php_preg_replace("/^.+?\\.([^.]+)$/", "$1", file_)
                if (not php_empty(lambda : ext_)):
                    post_mimes_[-1] = ext_
                    ext_type_ = wp_ext2type(ext_)
                    if ext_type_:
                        post_mimes_[-1] = ext_type_
                    # end if
                # end if
                mime_ = post_.post_mime_type
            else:
                mime_ = 0
            # end if
        else:
            post_mimes_[-1] = mime_
        # end if
        icon_files_ = wp_cache_get("icon_files")
        if (not php_is_array(icon_files_)):
            #// 
            #// Filters the icon directory path.
            #// 
            #// @since 2.0.0
            #// 
            #// @param string $path Icon directory absolute path.
            #//
            icon_dir_ = apply_filters("icon_dir", ABSPATH + WPINC + "/images/media")
            #// 
            #// Filters the icon directory URI.
            #// 
            #// @since 2.0.0
            #// 
            #// @param string $uri Icon directory URI.
            #//
            icon_dir_uri_ = apply_filters("icon_dir_uri", includes_url("images/media"))
            #// 
            #// Filters the array of icon directory URIs.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string[] $uris Array of icon directory URIs keyed by directory absolute path.
            #//
            dirs_ = apply_filters("icon_dirs", Array({icon_dir_: icon_dir_uri_}))
            icon_files_ = Array()
            while True:
                
                if not (dirs_):
                    break
                # end if
                keys_ = php_array_keys(dirs_)
                dir_ = php_array_shift(keys_)
                uri_ = php_array_shift(dirs_)
                dh_ = php_opendir(dir_)
                if dh_:
                    while True:
                        file_ = php_readdir(dh_)
                        if not (False != file_):
                            break
                        # end if
                        file_ = wp_basename(file_)
                        if php_substr(file_, 0, 1) == ".":
                            continue
                        # end if
                        if (not php_in_array(php_strtolower(php_substr(file_, -4)), Array(".png", ".gif", ".jpg"))):
                            if php_is_dir(str(dir_) + str("/") + str(file_)):
                                dirs_[str(dir_) + str("/") + str(file_)] = str(uri_) + str("/") + str(file_)
                            # end if
                            continue
                        # end if
                        icon_files_[str(dir_) + str("/") + str(file_)] = str(uri_) + str("/") + str(file_)
                    # end while
                    php_closedir(dh_)
                # end if
            # end while
            wp_cache_add("icon_files", icon_files_, "default", 600)
        # end if
        types_ = Array()
        #// Icon wp_basename - extension = MIME wildcard.
        for file_,uri_ in icon_files_.items():
            types_[php_preg_replace("/^([^.]*).*$/", "$1", wp_basename(file_))] = icon_files_[file_]
        # end for
        if (not php_empty(lambda : mime_)):
            post_mimes_[-1] = php_substr(mime_, 0, php_strpos(mime_, "/"))
            post_mimes_[-1] = php_substr(mime_, php_strpos(mime_, "/") + 1)
            post_mimes_[-1] = php_str_replace("/", "_", mime_)
        # end if
        matches_ = wp_match_mime_types(php_array_keys(types_), post_mimes_)
        matches_["default"] = Array("default")
        for match_,wilds_ in matches_.items():
            for wild_ in wilds_:
                if (not (php_isset(lambda : types_[wild_]))):
                    continue
                # end if
                icon_ = types_[wild_]
                if (not php_is_numeric(mime_)):
                    wp_cache_add(str("mime_type_icon_") + str(mime_), icon_)
                # end if
                break
            # end for
        # end for
    # end if
    #// 
    #// Filters the mime type icon.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $icon    Path to the mime type icon.
    #// @param string $mime    Mime type.
    #// @param int    $post_id Attachment ID. Will equal 0 if the function passed
    #// the mime type.
    #//
    return apply_filters("wp_mime_type_icon", icon_, mime_, post_id_)
# end def wp_mime_type_icon
#// 
#// Check for changed slugs for published post objects and save the old slug.
#// 
#// The function is used when a post object of any type is updated,
#// by comparing the current and previous post objects.
#// 
#// If the slug was changed and not already part of the old slugs then it will be
#// added to the post meta field ('_wp_old_slug') for storing old slugs for that
#// post.
#// 
#// The most logically usage of this function is redirecting changed post objects, so
#// that those that linked to an changed post will be redirected to the new post.
#// 
#// @since 2.1.0
#// 
#// @param int     $post_id     Post ID.
#// @param WP_Post $post        The Post Object
#// @param WP_Post $post_before The Previous Post Object
#//
def wp_check_for_changed_slugs(post_id_=None, post_=None, post_before_=None, *_args_):
    
    
    #// Don't bother if it hasn't changed.
    if post_.post_name == post_before_.post_name:
        return
    # end if
    #// We're only concerned with published, non-hierarchical objects.
    if (not "publish" == post_.post_status or "attachment" == get_post_type(post_) and "inherit" == post_.post_status) or is_post_type_hierarchical(post_.post_type):
        return
    # end if
    old_slugs_ = get_post_meta(post_id_, "_wp_old_slug")
    #// If we haven't added this old slug before, add it now.
    if (not php_empty(lambda : post_before_.post_name)) and (not php_in_array(post_before_.post_name, old_slugs_)):
        add_post_meta(post_id_, "_wp_old_slug", post_before_.post_name)
    # end if
    #// If the new slug was used previously, delete it from the list.
    if php_in_array(post_.post_name, old_slugs_):
        delete_post_meta(post_id_, "_wp_old_slug", post_.post_name)
    # end if
# end def wp_check_for_changed_slugs
#// 
#// Check for changed dates for published post objects and save the old date.
#// 
#// The function is used when a post object of any type is updated,
#// by comparing the current and previous post objects.
#// 
#// If the date was changed and not already part of the old dates then it will be
#// added to the post meta field ('_wp_old_date') for storing old dates for that
#// post.
#// 
#// The most logically usage of this function is redirecting changed post objects, so
#// that those that linked to an changed post will be redirected to the new post.
#// 
#// @since 4.9.3
#// 
#// @param int     $post_id     Post ID.
#// @param WP_Post $post        The Post Object
#// @param WP_Post $post_before The Previous Post Object
#//
def wp_check_for_changed_dates(post_id_=None, post_=None, post_before_=None, *_args_):
    
    
    previous_date_ = gmdate("Y-m-d", strtotime(post_before_.post_date))
    new_date_ = gmdate("Y-m-d", strtotime(post_.post_date))
    #// Don't bother if it hasn't changed.
    if new_date_ == previous_date_:
        return
    # end if
    #// We're only concerned with published, non-hierarchical objects.
    if (not "publish" == post_.post_status or "attachment" == get_post_type(post_) and "inherit" == post_.post_status) or is_post_type_hierarchical(post_.post_type):
        return
    # end if
    old_dates_ = get_post_meta(post_id_, "_wp_old_date")
    #// If we haven't added this old date before, add it now.
    if (not php_empty(lambda : previous_date_)) and (not php_in_array(previous_date_, old_dates_)):
        add_post_meta(post_id_, "_wp_old_date", previous_date_)
    # end if
    #// If the new slug was used previously, delete it from the list.
    if php_in_array(new_date_, old_dates_):
        delete_post_meta(post_id_, "_wp_old_date", new_date_)
    # end if
# end def wp_check_for_changed_dates
#// 
#// Retrieve the private post SQL based on capability.
#// 
#// This function provides a standardized way to appropriately select on the
#// post_status of a post type. The function will return a piece of SQL code
#// that can be added to a WHERE clause; this SQL is constructed to allow all
#// published posts, and all private posts to which the user has access.
#// 
#// @since 2.2.0
#// @since 4.3.0 Added the ability to pass an array to `$post_type`.
#// 
#// @param string|array $post_type Single post type or an array of post types. Currently only supports 'post' or 'page'.
#// @return string SQL code that can be added to a where clause.
#//
def get_private_posts_cap_sql(post_type_=None, *_args_):
    
    
    return get_posts_by_author_sql(post_type_, False)
# end def get_private_posts_cap_sql
#// 
#// Retrieve the post SQL based on capability, author, and type.
#// 
#// @since 3.0.0
#// @since 4.3.0 Introduced the ability to pass an array of post types to `$post_type`.
#// 
#// @see get_private_posts_cap_sql()
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string|string[] $post_type   Single post type or an array of post types.
#// @param bool            $full        Optional. Returns a full WHERE statement instead of just
#// an 'andalso' term. Default true.
#// @param int             $post_author Optional. Query posts having a single author ID. Default null.
#// @param bool            $public_only Optional. Only return public posts. Skips cap checks for
#// $current_user.  Default false.
#// @return string SQL WHERE code that can be added to a query.
#//
def get_posts_by_author_sql(post_type_=None, full_=None, post_author_=None, public_only_=None, *_args_):
    if full_ is None:
        full_ = True
    # end if
    if post_author_ is None:
        post_author_ = None
    # end if
    if public_only_ is None:
        public_only_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_is_array(post_type_):
        post_types_ = post_type_
    else:
        post_types_ = Array(post_type_)
    # end if
    post_type_clauses_ = Array()
    for post_type_ in post_types_:
        post_type_obj_ = get_post_type_object(post_type_)
        if (not post_type_obj_):
            continue
        # end if
        #// 
        #// Filters the capability to read private posts for a custom post type
        #// when generating SQL for getting posts by author.
        #// 
        #// @since 2.2.0
        #// @deprecated 3.2.0 The hook transitioned from "somewhat useless" to "totally useless".
        #// 
        #// @param string $cap Capability.
        #//
        cap_ = apply_filters_deprecated("pub_priv_sql_capability", Array(""), "3.2.0")
        if (not cap_):
            cap_ = current_user_can(post_type_obj_.cap.read_private_posts)
        # end if
        #// Only need to check the cap if $public_only is false.
        post_status_sql_ = "post_status = 'publish'"
        if False == public_only_:
            if cap_:
                #// Does the user have the capability to view private posts? Guess so.
                post_status_sql_ += " OR post_status = 'private'"
            elif is_user_logged_in():
                #// Users can view their own private posts.
                id_ = get_current_user_id()
                if None == post_author_ or (not full_):
                    post_status_sql_ += str(" OR post_status = 'private' AND post_author = ") + str(id_)
                elif id_ == php_int(post_author_):
                    post_status_sql_ += " OR post_status = 'private'"
                # end if
                pass
            # end if
            pass
        # end if
        post_type_clauses_[-1] = "( post_type = '" + post_type_ + str("' AND ( ") + str(post_status_sql_) + str(" ) )")
    # end for
    if php_empty(lambda : post_type_clauses_):
        return "WHERE 1 = 0" if full_ else "1 = 0"
    # end if
    sql_ = "( " + php_implode(" OR ", post_type_clauses_) + " )"
    if None != post_author_:
        sql_ += wpdb_.prepare(" AND post_author = %d", post_author_)
    # end if
    if full_:
        sql_ = "WHERE " + sql_
    # end if
    return sql_
# end def get_posts_by_author_sql
#// 
#// Retrieves the most recent time that a post on the site was published.
#// 
#// The server timezone is the default and is the difference between GMT and
#// server time. The 'blog' value is the date when the last post was posted. The
#// 'gmt' is when the last post was posted in GMT formatted date.
#// 
#// @since 0.71
#// @since 4.4.0 The `$post_type` argument was added.
#// 
#// @param string $timezone  Optional. The timezone for the timestamp. Accepts 'server', 'blog', or 'gmt'.
#// 'server' uses the server's internal timezone.
#// 'blog' uses the `post_date` field, which proxies to the timezone set for the site.
#// 'gmt' uses the `post_date_gmt` field.
#// Default 'server'.
#// @param string $post_type Optional. The post type to check. Default 'any'.
#// @return string The date of the last post, or false on failure.
#//
def get_lastpostdate(timezone_="server", post_type_="any", *_args_):
    
    
    #// 
    #// Filters the most recent time that a post on the site was published.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string|false $date     Date the last post was published. False on failure.
    #// @param string       $timezone Location to use for getting the post published date.
    #// See get_lastpostdate() for accepted `$timezone` values.
    #//
    return apply_filters("get_lastpostdate", _get_last_post_time(timezone_, "date", post_type_), timezone_)
# end def get_lastpostdate
#// 
#// Get the most recent time that a post on the site was modified.
#// 
#// The server timezone is the default and is the difference between GMT and
#// server time. The 'blog' value is just when the last post was modified. The
#// 'gmt' is when the last post was modified in GMT time.
#// 
#// @since 1.2.0
#// @since 4.4.0 The `$post_type` argument was added.
#// 
#// @param string $timezone  Optional. The timezone for the timestamp. See get_lastpostdate()
#// for information on accepted values.
#// Default 'server'.
#// @param string $post_type Optional. The post type to check. Default 'any'.
#// @return string The timestamp in 'Y-m-d H:i:s' format, or false on failure.
#//
def get_lastpostmodified(timezone_="server", post_type_="any", *_args_):
    
    
    #// 
    #// Pre-filter the return value of get_lastpostmodified() before the query is run.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string|false $lastpostmodified The most recent time that a post was modified, in 'Y-m-d H:i:s' format, or
    #// false. Returning anything other than false will short-circuit the function.
    #// @param string       $timezone         Location to use for getting the post modified date.
    #// See get_lastpostdate() for accepted `$timezone` values.
    #// @param string       $post_type        The post type to check.
    #//
    lastpostmodified_ = apply_filters("pre_get_lastpostmodified", False, timezone_, post_type_)
    if False != lastpostmodified_:
        return lastpostmodified_
    # end if
    lastpostmodified_ = _get_last_post_time(timezone_, "modified", post_type_)
    lastpostdate_ = get_lastpostdate(timezone_)
    if lastpostdate_ > lastpostmodified_:
        lastpostmodified_ = lastpostdate_
    # end if
    #// 
    #// Filters the most recent time that a post was modified.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string|false $lastpostmodified The most recent time that a post was modified, in 'Y-m-d H:i:s' format.
    #// False on failure.
    #// @param string       $timezone         Location to use for getting the post modified date.
    #// See get_lastpostdate() for accepted `$timezone` values.
    #//
    return apply_filters("get_lastpostmodified", lastpostmodified_, timezone_)
# end def get_lastpostmodified
#// 
#// Gets the timestamp of the last time any post was modified or published.
#// 
#// @since 3.1.0
#// @since 4.4.0 The `$post_type` argument was added.
#// @access private
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $timezone  The timezone for the timestamp. See get_lastpostdate().
#// for information on accepted values.
#// @param string $field     Post field to check. Accepts 'date' or 'modified'.
#// @param string $post_type Optional. The post type to check. Default 'any'.
#// @return string|false The timestamp in 'Y-m-d H:i:s' format, or false on failure.
#//
def _get_last_post_time(timezone_=None, field_=None, post_type_="any", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_in_array(field_, Array("date", "modified"))):
        return False
    # end if
    timezone_ = php_strtolower(timezone_)
    key_ = str("lastpost") + str(field_) + str(":") + str(timezone_)
    if "any" != post_type_:
        key_ += ":" + sanitize_key(post_type_)
    # end if
    date_ = wp_cache_get(key_, "timeinfo")
    if False != date_:
        return date_
    # end if
    if "any" == post_type_:
        post_types_ = get_post_types(Array({"public": True}))
        php_array_walk(post_types_, Array(wpdb_, "escape_by_ref"))
        post_types_ = "'" + php_implode("', '", post_types_) + "'"
    else:
        post_types_ = "'" + sanitize_key(post_type_) + "'"
    # end if
    for case in Switch(timezone_):
        if case("gmt"):
            date_ = wpdb_.get_var(str("SELECT post_") + str(field_) + str("_gmt FROM ") + str(wpdb_.posts) + str(" WHERE post_status = 'publish' AND post_type IN (") + str(post_types_) + str(") ORDER BY post_") + str(field_) + str("_gmt DESC LIMIT 1"))
            break
        # end if
        if case("blog"):
            date_ = wpdb_.get_var(str("SELECT post_") + str(field_) + str(" FROM ") + str(wpdb_.posts) + str(" WHERE post_status = 'publish' AND post_type IN (") + str(post_types_) + str(") ORDER BY post_") + str(field_) + str("_gmt DESC LIMIT 1"))
            break
        # end if
        if case("server"):
            add_seconds_server_ = gmdate("Z")
            date_ = wpdb_.get_var(str("SELECT DATE_ADD(post_") + str(field_) + str("_gmt, INTERVAL '") + str(add_seconds_server_) + str("' SECOND) FROM ") + str(wpdb_.posts) + str(" WHERE post_status = 'publish' AND post_type IN (") + str(post_types_) + str(") ORDER BY post_") + str(field_) + str("_gmt DESC LIMIT 1"))
            break
        # end if
    # end for
    if date_:
        wp_cache_set(key_, date_, "timeinfo")
        return date_
    # end if
    return False
# end def _get_last_post_time
#// 
#// Updates posts in cache.
#// 
#// @since 1.5.1
#// 
#// @param WP_Post[] $posts Array of post objects (passed by reference).
#//
def update_post_cache(posts_=None, *_args_):
    
    
    if (not posts_):
        return
    # end if
    for post_ in posts_:
        wp_cache_add(post_.ID, post_, "posts")
    # end for
# end def update_post_cache
#// 
#// Will clean the post in the cache.
#// 
#// Cleaning means delete from the cache of the post. Will call to clean the term
#// object cache associated with the post ID.
#// 
#// This function not run if $_wp_suspend_cache_invalidation is not empty. See
#// wp_suspend_cache_invalidation().
#// 
#// @since 2.0.0
#// 
#// @global bool $_wp_suspend_cache_invalidation
#// 
#// @param int|WP_Post $post Post ID or post object to remove from the cache.
#//
def clean_post_cache(post_=None, *_args_):
    
    
    global _wp_suspend_cache_invalidation_
    php_check_if_defined("_wp_suspend_cache_invalidation_")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation_)):
        return
    # end if
    post_ = get_post(post_)
    if php_empty(lambda : post_):
        return
    # end if
    wp_cache_delete(post_.ID, "posts")
    wp_cache_delete(post_.ID, "post_meta")
    clean_object_term_cache(post_.ID, post_.post_type)
    wp_cache_delete("wp_get_archives", "general")
    #// 
    #// Fires immediately after the given post's cache is cleaned.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int     $post_id Post ID.
    #// @param WP_Post $post    Post object.
    #//
    do_action("clean_post_cache", post_.ID, post_)
    if "page" == post_.post_type:
        wp_cache_delete("all_page_ids", "posts")
        #// 
        #// Fires immediately after the given page's cache is cleaned.
        #// 
        #// @since 2.5.0
        #// 
        #// @param int $post_id Post ID.
        #//
        do_action("clean_page_cache", post_.ID)
    # end if
    wp_cache_set("last_changed", php_microtime(), "posts")
# end def clean_post_cache
#// 
#// Call major cache updating functions for list of Post objects.
#// 
#// @since 1.5.0
#// 
#// @param WP_Post[] $posts             Array of Post objects
#// @param string    $post_type         Optional. Post type. Default 'post'.
#// @param bool      $update_term_cache Optional. Whether to update the term cache. Default true.
#// @param bool      $update_meta_cache Optional. Whether to update the meta cache. Default true.
#//
def update_post_caches(posts_=None, post_type_="post", update_term_cache_=None, update_meta_cache_=None, *_args_):
    if update_term_cache_ is None:
        update_term_cache_ = True
    # end if
    if update_meta_cache_ is None:
        update_meta_cache_ = True
    # end if
    
    #// No point in doing all this work if we didn't match any posts.
    if (not posts_):
        return
    # end if
    update_post_cache(posts_)
    post_ids_ = Array()
    for post_ in posts_:
        post_ids_[-1] = post_.ID
    # end for
    if (not post_type_):
        post_type_ = "any"
    # end if
    if update_term_cache_:
        if php_is_array(post_type_):
            ptypes_ = post_type_
        elif "any" == post_type_:
            ptypes_ = Array()
            #// Just use the post_types in the supplied posts.
            for post_ in posts_:
                ptypes_[-1] = post_.post_type
            # end for
            ptypes_ = array_unique(ptypes_)
        else:
            ptypes_ = Array(post_type_)
        # end if
        if (not php_empty(lambda : ptypes_)):
            update_object_term_cache(post_ids_, ptypes_)
        # end if
    # end if
    if update_meta_cache_:
        update_postmeta_cache(post_ids_)
    # end if
# end def update_post_caches
#// 
#// Updates metadata cache for list of post IDs.
#// 
#// Performs SQL query to retrieve the metadata for the post IDs and updates the
#// metadata cache for the posts. Therefore, the functions, which call this
#// function, do not need to perform SQL queries on their own.
#// 
#// @since 2.1.0
#// 
#// @param int[] $post_ids Array of post IDs.
#// @return array|false Returns false if there is nothing to update or an array
#// of metadata.
#//
def update_postmeta_cache(post_ids_=None, *_args_):
    
    
    return update_meta_cache("post", post_ids_)
# end def update_postmeta_cache
#// 
#// Will clean the attachment in the cache.
#// 
#// Cleaning means delete from the cache. Optionally will clean the term
#// object cache associated with the attachment ID.
#// 
#// This function will not run if $_wp_suspend_cache_invalidation is not empty.
#// 
#// @since 3.0.0
#// 
#// @global bool $_wp_suspend_cache_invalidation
#// 
#// @param int  $id          The attachment ID in the cache to clean.
#// @param bool $clean_terms Optional. Whether to clean terms cache. Default false.
#//
def clean_attachment_cache(id_=None, clean_terms_=None, *_args_):
    if clean_terms_ is None:
        clean_terms_ = False
    # end if
    
    global _wp_suspend_cache_invalidation_
    php_check_if_defined("_wp_suspend_cache_invalidation_")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation_)):
        return
    # end if
    id_ = php_int(id_)
    wp_cache_delete(id_, "posts")
    wp_cache_delete(id_, "post_meta")
    if clean_terms_:
        clean_object_term_cache(id_, "attachment")
    # end if
    #// 
    #// Fires after the given attachment's cache is cleaned.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int $id Attachment ID.
    #//
    do_action("clean_attachment_cache", id_)
# end def clean_attachment_cache
#// 
#// Hooks.
#// 
#// 
#// Hook for managing future post transitions to published.
#// 
#// @since 2.3.0
#// @access private
#// 
#// @see wp_clear_scheduled_hook()
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string  $new_status New post status.
#// @param string  $old_status Previous post status.
#// @param WP_Post $post       Post object.
#//
def _transition_post_status(new_status_=None, old_status_=None, post_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if "publish" != old_status_ and "publish" == new_status_:
        #// Reset GUID if transitioning to publish and it is empty.
        if "" == get_the_guid(post_.ID):
            wpdb_.update(wpdb_.posts, Array({"guid": get_permalink(post_.ID)}), Array({"ID": post_.ID}))
        # end if
        #// 
        #// Fires when a post's status is transitioned from private to published.
        #// 
        #// @since 1.5.0
        #// @deprecated 2.3.0 Use {@see 'private_to_publish'} instead.
        #// 
        #// @param int $post_id Post ID.
        #//
        do_action_deprecated("private_to_published", Array(post_.ID), "2.3.0", "private_to_publish")
    # end if
    #// If published posts changed clear the lastpostmodified cache.
    if "publish" == new_status_ or "publish" == old_status_:
        for timezone_ in Array("server", "gmt", "blog"):
            wp_cache_delete(str("lastpostmodified:") + str(timezone_), "timeinfo")
            wp_cache_delete(str("lastpostdate:") + str(timezone_), "timeinfo")
            wp_cache_delete(str("lastpostdate:") + str(timezone_) + str(":") + str(post_.post_type), "timeinfo")
        # end for
    # end if
    if new_status_ != old_status_:
        wp_cache_delete(_count_posts_cache_key(post_.post_type), "counts")
        wp_cache_delete(_count_posts_cache_key(post_.post_type, "readable"), "counts")
    # end if
    #// Always clears the hook in case the post status bounced from future to draft.
    wp_clear_scheduled_hook("publish_future_post", Array(post_.ID))
# end def _transition_post_status
#// 
#// Hook used to schedule publication for a post marked for the future.
#// 
#// The $post properties used and must exist are 'ID' and 'post_date_gmt'.
#// 
#// @since 2.3.0
#// @access private
#// 
#// @param int     $deprecated Not used. Can be set to null. Never implemented. Not marked
#// as deprecated with _deprecated_argument() as it conflicts with
#// wp_transition_post_status() and the default filter for _future_post_hook().
#// @param WP_Post $post       Post object.
#//
def _future_post_hook(deprecated_=None, post_=None, *_args_):
    
    
    wp_clear_scheduled_hook("publish_future_post", Array(post_.ID))
    wp_schedule_single_event(strtotime(get_gmt_from_date(post_.post_date) + " GMT"), "publish_future_post", Array(post_.ID))
# end def _future_post_hook
#// 
#// Hook to schedule pings and enclosures when a post is published.
#// 
#// Uses XMLRPC_REQUEST and WP_IMPORTING constants.
#// 
#// @since 2.3.0
#// @access private
#// 
#// @param int $post_id The ID in the database table of the post being published.
#//
def _publish_post_hook(post_id_=None, *_args_):
    
    
    if php_defined("XMLRPC_REQUEST"):
        #// 
        #// Fires when _publish_post_hook() is called during an XML-RPC request.
        #// 
        #// @since 2.1.0
        #// 
        #// @param int $post_id Post ID.
        #//
        do_action("xmlrpc_publish_post", post_id_)
    # end if
    if php_defined("WP_IMPORTING"):
        return
    # end if
    if get_option("default_pingback_flag"):
        add_post_meta(post_id_, "_pingme", "1", True)
    # end if
    add_post_meta(post_id_, "_encloseme", "1", True)
    to_ping_ = get_to_ping(post_id_)
    if (not php_empty(lambda : to_ping_)):
        add_post_meta(post_id_, "_trackbackme", "1")
    # end if
    if (not wp_next_scheduled("do_pings")):
        wp_schedule_single_event(time(), "do_pings")
    # end if
# end def _publish_post_hook
#// 
#// Returns the ID of the post's parent.
#// 
#// @since 3.1.0
#// 
#// @param int|WP_Post $post Post ID or post object. Defaults to global $post.
#// @return int|false Post parent ID (which can be 0 if there is no parent), or false if the post does not exist.
#//
def wp_get_post_parent_id(post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_) or is_wp_error(post_):
        return False
    # end if
    return php_int(post_.post_parent)
# end def wp_get_post_parent_id
#// 
#// Check the given subset of the post hierarchy for hierarchy loops.
#// 
#// Prevents loops from forming and breaks those that it finds. Attached
#// to the {@see 'wp_insert_post_parent'} filter.
#// 
#// @since 3.1.0
#// 
#// @see wp_find_hierarchy_loop()
#// 
#// @param int $post_parent ID of the parent for the post we're checking.
#// @param int $post_ID     ID of the post we're checking.
#// @return int The new post_parent for the post, 0 otherwise.
#//
def wp_check_post_hierarchy_for_loops(post_parent_=None, post_ID_=None, *_args_):
    
    
    #// Nothing fancy here - bail.
    if (not post_parent_):
        return 0
    # end if
    #// New post can't cause a loop.
    if php_empty(lambda : post_ID_):
        return post_parent_
    # end if
    #// Can't be its own parent.
    if post_parent_ == post_ID_:
        return 0
    # end if
    #// Now look for larger loops.
    loop_ = wp_find_hierarchy_loop("wp_get_post_parent_id", post_ID_, post_parent_)
    if (not loop_):
        return post_parent_
        pass
    # end if
    #// Setting $post_parent to the given value causes a loop.
    if (php_isset(lambda : loop_[post_ID_])):
        return 0
    # end if
    #// There's a loop, but it doesn't contain $post_ID. Break the loop.
    for loop_member_ in php_array_keys(loop_):
        wp_update_post(Array({"ID": loop_member_, "post_parent": 0}))
    # end for
    return post_parent_
# end def wp_check_post_hierarchy_for_loops
#// 
#// Sets the post thumbnail (featured image) for the given post.
#// 
#// @since 3.1.0
#// 
#// @param int|WP_Post $post         Post ID or post object where thumbnail should be attached.
#// @param int         $thumbnail_id Thumbnail to attach.
#// @return int|bool True on success, false on failure.
#//
def set_post_thumbnail(post_=None, thumbnail_id_=None, *_args_):
    
    
    post_ = get_post(post_)
    thumbnail_id_ = absint(thumbnail_id_)
    if post_ and thumbnail_id_ and get_post(thumbnail_id_):
        if wp_get_attachment_image(thumbnail_id_, "thumbnail"):
            return update_post_meta(post_.ID, "_thumbnail_id", thumbnail_id_)
        else:
            return delete_post_meta(post_.ID, "_thumbnail_id")
        # end if
    # end if
    return False
# end def set_post_thumbnail
#// 
#// Removes the thumbnail (featured image) from the given post.
#// 
#// @since 3.3.0
#// 
#// @param int|WP_Post $post Post ID or post object from which the thumbnail should be removed.
#// @return bool True on success, false on failure.
#//
def delete_post_thumbnail(post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if post_:
        return delete_post_meta(post_.ID, "_thumbnail_id")
    # end if
    return False
# end def delete_post_thumbnail
#// 
#// Delete auto-drafts for new posts that are > 7 days old.
#// 
#// @since 3.4.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def wp_delete_auto_drafts(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Cleanup old auto-drafts more than 7 days old.
    old_posts_ = wpdb_.get_col(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_status = 'auto-draft' AND DATE_SUB( NOW(), INTERVAL 7 DAY ) > post_date"))
    for delete_ in old_posts_:
        #// Force delete.
        wp_delete_post(delete_, True)
    # end for
# end def wp_delete_auto_drafts
#// 
#// Queues posts for lazy-loading of term meta.
#// 
#// @since 4.5.0
#// 
#// @param array $posts Array of WP_Post objects.
#//
def wp_queue_posts_for_term_meta_lazyload(posts_=None, *_args_):
    
    
    post_type_taxonomies_ = Array()
    term_ids_ = Array()
    for post_ in posts_:
        if (not type(post_).__name__ == "WP_Post"):
            continue
        # end if
        if (not (php_isset(lambda : post_type_taxonomies_[post_.post_type]))):
            post_type_taxonomies_[post_.post_type] = get_object_taxonomies(post_.post_type)
        # end if
        for taxonomy_ in post_type_taxonomies_[post_.post_type]:
            #// Term cache should already be primed by `update_post_term_cache()`.
            terms_ = get_object_term_cache(post_.ID, taxonomy_)
            if False != terms_:
                for term_ in terms_:
                    if (not (php_isset(lambda : term_ids_[term_.term_id]))):
                        term_ids_[-1] = term_.term_id
                    # end if
                # end for
            # end if
        # end for
    # end for
    if term_ids_:
        lazyloader_ = wp_metadata_lazyloader()
        lazyloader_.queue_objects("term", term_ids_)
    # end if
# end def wp_queue_posts_for_term_meta_lazyload
#// 
#// Update the custom taxonomies' term counts when a post's status is changed.
#// 
#// For example, default posts term counts (for custom taxonomies) don't include
#// private / draft posts.
#// 
#// @since 3.3.0
#// @access private
#// 
#// @param string  $new_status New post status.
#// @param string  $old_status Old post status.
#// @param WP_Post $post       Post object.
#//
def _update_term_count_on_transition_post_status(new_status_=None, old_status_=None, post_=None, *_args_):
    
    
    #// Update counts for the post's terms.
    for taxonomy_ in get_object_taxonomies(post_.post_type):
        tt_ids_ = wp_get_object_terms(post_.ID, taxonomy_, Array({"fields": "tt_ids"}))
        wp_update_term_count(tt_ids_, taxonomy_)
    # end for
# end def _update_term_count_on_transition_post_status
#// 
#// Adds any posts from the given ids to the cache that do not already exist in cache
#// 
#// @since 3.4.0
#// @access private
#// 
#// @see update_post_caches()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $ids               ID list.
#// @param bool  $update_term_cache Optional. Whether to update the term cache. Default true.
#// @param bool  $update_meta_cache Optional. Whether to update the meta cache. Default true.
#//
def _prime_post_caches(ids_=None, update_term_cache_=None, update_meta_cache_=None, *_args_):
    if update_term_cache_ is None:
        update_term_cache_ = True
    # end if
    if update_meta_cache_ is None:
        update_meta_cache_ = True
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    non_cached_ids_ = _get_non_cached_ids(ids_, "posts")
    if (not php_empty(lambda : non_cached_ids_)):
        fresh_posts_ = wpdb_.get_results(php_sprintf(str("SELECT ") + str(wpdb_.posts) + str(".* FROM ") + str(wpdb_.posts) + str(" WHERE ID IN (%s)"), php_join(",", non_cached_ids_)))
        update_post_caches(fresh_posts_, "any", update_term_cache_, update_meta_cache_)
    # end if
# end def _prime_post_caches
#// 
#// Adds a suffix if any trashed posts have a given slug.
#// 
#// Store its desired (i.e. current) slug so it can try to reclaim it
#// if the post is untrashed.
#// 
#// For internal use.
#// 
#// @since 4.5.0
#// @access private
#// 
#// @param string $post_name Slug.
#// @param string $post_ID   Optional. Post ID that should be ignored. Default 0.
#//
def wp_add_trashed_suffix_to_post_name_for_trashed_posts(post_name_=None, post_ID_=0, *_args_):
    
    
    trashed_posts_with_desired_slug_ = get_posts(Array({"name": post_name_, "post_status": "trash", "post_type": "any", "nopaging": True, "post__not_in": Array(post_ID_)}))
    if (not php_empty(lambda : trashed_posts_with_desired_slug_)):
        for _post_ in trashed_posts_with_desired_slug_:
            wp_add_trashed_suffix_to_post_name_for_post(_post_)
        # end for
    # end if
# end def wp_add_trashed_suffix_to_post_name_for_trashed_posts
#// 
#// Adds a trashed suffix for a given post.
#// 
#// Store its desired (i.e. current) slug so it can try to reclaim it
#// if the post is untrashed.
#// 
#// For internal use.
#// 
#// @since 4.5.0
#// @access private
#// 
#// @param WP_Post $post The post.
#// @return string New slug for the post.
#//
def wp_add_trashed_suffix_to_post_name_for_post(post_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ = get_post(post_)
    if "__trashed" == php_substr(post_.post_name, -9):
        return post_.post_name
    # end if
    add_post_meta(post_.ID, "_wp_desired_post_slug", post_.post_name)
    post_name_ = _truncate_post_slug(post_.post_name, 191) + "__trashed"
    wpdb_.update(wpdb_.posts, Array({"post_name": post_name_}), Array({"ID": post_.ID}))
    clean_post_cache(post_.ID)
    return post_name_
# end def wp_add_trashed_suffix_to_post_name_for_post
#// 
#// Filter the SQL clauses of an attachment query to include filenames.
#// 
#// @since 4.7.0
#// @access private
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string[] $clauses An array including WHERE, GROUP BY, JOIN, ORDER BY,
#// DISTINCT, fields (SELECT), and LIMITS clauses.
#// @return string[] The modified array of clauses.
#//
def _filter_query_attachment_filenames(clauses_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    remove_filter("posts_clauses", inspect.currentframe().f_code.co_name)
    #// Add a LEFT JOIN of the postmeta table so we don't trample existing JOINs.
    clauses_["join"] += str(" LEFT JOIN ") + str(wpdb_.postmeta) + str(" AS sq1 ON ( ") + str(wpdb_.posts) + str(".ID = sq1.post_id AND sq1.meta_key = '_wp_attached_file' )")
    clauses_["groupby"] = str(wpdb_.posts) + str(".ID")
    clauses_["where"] = php_preg_replace(str("/\\(") + str(wpdb_.posts) + str(".post_content (NOT LIKE|LIKE) (\\'[^']+\\')\\)/"), "$0 OR ( sq1.meta_value $1 $2 )", clauses_["where"])
    return clauses_
# end def _filter_query_attachment_filenames
#// 
#// Sets the last changed time for the 'posts' cache group.
#// 
#// @since 5.0.0
#//
def wp_cache_set_posts_last_changed(*_args_):
    
    
    wp_cache_set("last_changed", php_microtime(), "posts")
# end def wp_cache_set_posts_last_changed
#// 
#// Get all available post MIME types for a given post type.
#// 
#// @since 2.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $type
#// @return mixed
#//
def get_available_post_mime_types(type_="attachment", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    types_ = wpdb_.get_col(wpdb_.prepare(str("SELECT DISTINCT post_mime_type FROM ") + str(wpdb_.posts) + str(" WHERE post_type = %s"), type_))
    return types_
# end def get_available_post_mime_types
#// 
#// Retrieves the path to an uploaded image file.
#// 
#// Similar to `get_attached_file()` however some images may have been processed after uploading
#// to make them suitable for web use. In this case the attached "full" size file is usually replaced
#// with a scaled down version of the original image. This function always returns the path
#// to the originally uploaded image file.
#// 
#// @since 5.3.0
#// @since 5.4.0 Added the `$unfiltered` parameter.
#// 
#// @param int  $attachment_id Attachment ID.
#// @param bool $unfiltered Optional. Passed through to `get_attached_file()`. Default false.
#// @return string|false Path to the original image file or false if the attachment is not an image.
#//
def wp_get_original_image_path(attachment_id_=None, unfiltered_=None, *_args_):
    if unfiltered_ is None:
        unfiltered_ = False
    # end if
    
    if (not wp_attachment_is_image(attachment_id_)):
        return False
    # end if
    image_meta_ = wp_get_attachment_metadata(attachment_id_)
    image_file_ = get_attached_file(attachment_id_, unfiltered_)
    if php_empty(lambda : image_meta_["original_image"]):
        original_image_ = image_file_
    else:
        original_image_ = path_join(php_dirname(image_file_), image_meta_["original_image"])
    # end if
    #// 
    #// Filters the path to the original image.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $original_image Path to original image file.
    #// @param int    $attachment_id  Attachment ID.
    #//
    return apply_filters("wp_get_original_image_path", original_image_, attachment_id_)
# end def wp_get_original_image_path
#// 
#// Retrieve the URL to an original attachment image.
#// 
#// Similar to `wp_get_attachment_url()` however some images may have been
#// processed after uploading. In this case this function returns the URL
#// to the originally uploaded image file.
#// 
#// @since 5.3.0
#// 
#// @param int $attachment_id Attachment post ID.
#// @return string|false Attachment image URL, false on error or if the attachment is not an image.
#//
def wp_get_original_image_url(attachment_id_=None, *_args_):
    
    
    if (not wp_attachment_is_image(attachment_id_)):
        return False
    # end if
    image_url_ = wp_get_attachment_url(attachment_id_)
    if php_empty(lambda : image_url_):
        return False
    # end if
    image_meta_ = wp_get_attachment_metadata(attachment_id_)
    if php_empty(lambda : image_meta_["original_image"]):
        original_image_url_ = image_url_
    else:
        original_image_url_ = path_join(php_dirname(image_url_), image_meta_["original_image"])
    # end if
    #// 
    #// Filters the URL to the original attachment image.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $original_image_url URL to original image.
    #// @param int    $attachment_id      Attachment ID.
    #//
    return apply_filters("wp_get_original_image_url", original_image_url_, attachment_id_)
# end def wp_get_original_image_url
