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
def create_initial_post_types(*args_):
    
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
def get_attached_file(attachment_id=None, unfiltered=False, *args_):
    
    file = get_post_meta(attachment_id, "_wp_attached_file", True)
    #// If the file is relative, prepend upload dir.
    if file and 0 != php_strpos(file, "/") and (not php_preg_match("|^.:\\\\|", file)):
        uploads = wp_get_upload_dir()
        if False == uploads["error"]:
            file = uploads["basedir"] + str("/") + str(file)
        # end if
    # end if
    if unfiltered:
        return file
    # end if
    #// 
    #// Filters the attached file based on the given ID.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $file          Path to attached file.
    #// @param int    $attachment_id Attachment ID.
    #//
    return apply_filters("get_attached_file", file, attachment_id)
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
def update_attached_file(attachment_id=None, file=None, *args_):
    
    if (not get_post(attachment_id)):
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
    file = apply_filters("update_attached_file", file, attachment_id)
    file = _wp_relative_upload_path(file)
    if file:
        return update_post_meta(attachment_id, "_wp_attached_file", file)
    else:
        return delete_post_meta(attachment_id, "_wp_attached_file")
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
def _wp_relative_upload_path(path=None, *args_):
    
    new_path = path
    uploads = wp_get_upload_dir()
    if 0 == php_strpos(new_path, uploads["basedir"]):
        new_path = php_str_replace(uploads["basedir"], "", new_path)
        new_path = php_ltrim(new_path, "/")
    # end if
    #// 
    #// Filters the relative path to an uploaded file.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $new_path Relative path to the file.
    #// @param string $path     Full path to the file.
    #//
    return apply_filters("_wp_relative_upload_path", new_path, path)
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
def get_children(args="", output=OBJECT, *args_):
    
    kids = Array()
    if php_empty(lambda : args):
        if (php_isset(lambda : PHP_GLOBALS["post"])):
            args = Array({"post_parent": int(PHP_GLOBALS["post"].post_parent)})
        else:
            return kids
        # end if
    elif php_is_object(args):
        args = Array({"post_parent": int(args.post_parent)})
    elif php_is_numeric(args):
        args = Array({"post_parent": int(args)})
    # end if
    defaults = Array({"numberposts": -1, "post_type": "any", "post_status": "any", "post_parent": 0})
    parsed_args = wp_parse_args(args, defaults)
    children = get_posts(parsed_args)
    if (not children):
        return kids
    # end if
    if (not php_empty(lambda : parsed_args["fields"])):
        return children
    # end if
    update_post_cache(children)
    for key,child in children:
        kids[child.ID] = children[key]
    # end for
    if OBJECT == output:
        return kids
    elif ARRAY_A == output:
        weeuns = Array()
        for kid in kids:
            weeuns[kid.ID] = get_object_vars(kids[kid.ID])
        # end for
        return weeuns
    elif ARRAY_N == output:
        babes = Array()
        for kid in kids:
            babes[kid.ID] = php_array_values(get_object_vars(kids[kid.ID]))
        # end for
        return babes
    else:
        return kids
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
def get_extended(post=None, *args_):
    
    #// Match the new style more links.
    if php_preg_match("/<!--more(.*?)?-->/", post, matches):
        main, extended = php_explode(matches[0], post, 2)
        more_text = matches[1]
    else:
        main = post
        extended = ""
        more_text = ""
    # end if
    #// Leading and trailing whitespace.
    main = php_preg_replace("/^[\\s]*(.*)[\\s]*$/", "\\1", main)
    extended = php_preg_replace("/^[\\s]*(.*)[\\s]*$/", "\\1", extended)
    more_text = php_preg_replace("/^[\\s]*(.*)[\\s]*$/", "\\1", more_text)
    return Array({"main": main, "extended": extended, "more_text": more_text})
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
def get_post(post=None, output=OBJECT, filter="raw", *args_):
    
    if php_empty(lambda : post) and (php_isset(lambda : PHP_GLOBALS["post"])):
        post = PHP_GLOBALS["post"]
    # end if
    if type(post).__name__ == "WP_Post":
        _post = post
    elif php_is_object(post):
        if php_empty(lambda : post.filter):
            _post = sanitize_post(post, "raw")
            _post = php_new_class("WP_Post", lambda : WP_Post(_post))
        elif "raw" == post.filter:
            _post = php_new_class("WP_Post", lambda : WP_Post(post))
        else:
            _post = WP_Post.get_instance(post.ID)
        # end if
    else:
        _post = WP_Post.get_instance(post)
    # end if
    if (not _post):
        return None
    # end if
    _post = _post.filter(filter)
    if ARRAY_A == output:
        return _post.to_array()
    elif ARRAY_N == output:
        return php_array_values(_post.to_array())
    # end if
    return _post
# end def get_post
#// 
#// Retrieve ancestors of a post.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Post $post Post ID or post object.
#// @return int[] Ancestor IDs or empty array if none are found.
#//
def get_post_ancestors(post=None, *args_):
    
    post = get_post(post)
    if (not post) or php_empty(lambda : post.post_parent) or post.post_parent == post.ID:
        return Array()
    # end if
    ancestors = Array()
    id = post.post_parent
    ancestors[-1] = id
    while True:
        ancestor = get_post(id)
        if not (ancestor):
            break
        # end if
        #// Loop detection: If the ancestor has been seen before, break.
        if php_empty(lambda : ancestor.post_parent) or ancestor.post_parent == post.ID or php_in_array(ancestor.post_parent, ancestors):
            break
        # end if
        id = ancestor.post_parent
        ancestors[-1] = id
    # end while
    return ancestors
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
def get_post_field(field=None, post=None, context="display", *args_):
    
    post = get_post(post)
    if (not post):
        return ""
    # end if
    if (not (php_isset(lambda : post.field))):
        return ""
    # end if
    return sanitize_post_field(field, post.field, post.ID, context)
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
def get_post_mime_type(post=None, *args_):
    
    post = get_post(post)
    if php_is_object(post):
        return post.post_mime_type
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
def get_post_status(post=None, *args_):
    
    post = get_post(post)
    if (not php_is_object(post)):
        return False
    # end if
    if "attachment" == post.post_type:
        if "private" == post.post_status:
            return "private"
        # end if
        #// Unattached attachments are assumed to be published.
        if "inherit" == post.post_status and 0 == post.post_parent:
            return "publish"
        # end if
        #// Inherit status from the parent.
        if post.post_parent and post.ID != post.post_parent:
            parent_post_status = get_post_status(post.post_parent)
            if "trash" == parent_post_status:
                return get_post_meta(post.post_parent, "_wp_trash_meta_status", True)
            else:
                return parent_post_status
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
    return apply_filters("get_post_status", post.post_status, post)
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
def get_post_statuses(*args_):
    
    status = Array({"draft": __("Draft"), "pending": __("Pending Review"), "private": __("Private"), "publish": __("Published")})
    return status
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
def get_page_statuses(*args_):
    
    status = Array({"draft": __("Draft"), "private": __("Private"), "publish": __("Published")})
    return status
# end def get_page_statuses
#// 
#// Return statuses for privacy requests.
#// 
#// @since 4.9.6
#// @access private
#// 
#// @return array
#//
def _wp_privacy_statuses(*args_):
    
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
def register_post_status(post_status=None, args=Array(), *args_):
    
    global wp_post_statuses
    php_check_if_defined("wp_post_statuses")
    if (not php_is_array(wp_post_statuses)):
        wp_post_statuses = Array()
    # end if
    #// Args prefixed with an underscore are reserved for internal use.
    defaults = Array({"label": False, "label_count": False, "exclude_from_search": None, "_builtin": False, "public": None, "internal": None, "protected": None, "private": None, "publicly_queryable": None, "show_in_admin_status_list": None, "show_in_admin_all_list": None, "date_floating": None})
    args = wp_parse_args(args, defaults)
    args = args
    post_status = sanitize_key(post_status)
    args.name = post_status
    #// Set various defaults.
    if None == args.public and None == args.internal and None == args.protected and None == args.private:
        args.internal = True
    # end if
    if None == args.public:
        args.public = False
    # end if
    if None == args.private:
        args.private = False
    # end if
    if None == args.protected:
        args.protected = False
    # end if
    if None == args.internal:
        args.internal = False
    # end if
    if None == args.publicly_queryable:
        args.publicly_queryable = args.public
    # end if
    if None == args.exclude_from_search:
        args.exclude_from_search = args.internal
    # end if
    if None == args.show_in_admin_all_list:
        args.show_in_admin_all_list = (not args.internal)
    # end if
    if None == args.show_in_admin_status_list:
        args.show_in_admin_status_list = (not args.internal)
    # end if
    if None == args.date_floating:
        args.date_floating = False
    # end if
    if False == args.label:
        args.label = post_status
    # end if
    if False == args.label_count:
        #// phpcs:ignore WordPress.WP.I18n.NonSingularStringLiteralSingle,WordPress.WP.I18n.NonSingularStringLiteralPlural
        args.label_count = _n_noop(args.label, args.label)
    # end if
    wp_post_statuses[post_status] = args
    return args
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
def get_post_status_object(post_status=None, *args_):
    
    global wp_post_statuses
    php_check_if_defined("wp_post_statuses")
    if php_empty(lambda : wp_post_statuses[post_status]):
        return None
    # end if
    return wp_post_statuses[post_status]
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
def get_post_stati(args=Array(), output="names", operator="and", *args_):
    
    global wp_post_statuses
    php_check_if_defined("wp_post_statuses")
    field = "name" if "names" == output else False
    return wp_filter_object_list(wp_post_statuses, args, operator, field)
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
def is_post_type_hierarchical(post_type=None, *args_):
    
    if (not post_type_exists(post_type)):
        return False
    # end if
    post_type = get_post_type_object(post_type)
    return post_type.hierarchical
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
def post_type_exists(post_type=None, *args_):
    
    return bool(get_post_type_object(post_type))
# end def post_type_exists
#// 
#// Retrieves the post type of the current post or of a given post.
#// 
#// @since 2.1.0
#// 
#// @param int|WP_Post|null $post Optional. Post ID or post object. Default is global $post.
#// @return string|false          Post type on success, false on failure.
#//
def get_post_type(post=None, *args_):
    
    post = get_post(post)
    if post:
        return post.post_type
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
def get_post_type_object(post_type=None, *args_):
    
    global wp_post_types
    php_check_if_defined("wp_post_types")
    if (not is_scalar(post_type)) or php_empty(lambda : wp_post_types[post_type]):
        return None
    # end if
    return wp_post_types[post_type]
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
def get_post_types(args=Array(), output="names", operator="and", *args_):
    
    global wp_post_types
    php_check_if_defined("wp_post_types")
    field = "name" if "names" == output else False
    return wp_filter_object_list(wp_post_types, args, operator, field)
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
def register_post_type(post_type=None, args=Array(), *args_):
    
    global wp_post_types
    php_check_if_defined("wp_post_types")
    if (not php_is_array(wp_post_types)):
        wp_post_types = Array()
    # end if
    #// Sanitize post type name.
    post_type = sanitize_key(post_type)
    if php_empty(lambda : post_type) or php_strlen(post_type) > 20:
        _doing_it_wrong(__FUNCTION__, __("Post type names must be between 1 and 20 characters in length."), "4.2.0")
        return php_new_class("WP_Error", lambda : WP_Error("post_type_length_invalid", __("Post type names must be between 1 and 20 characters in length.")))
    # end if
    post_type_object = php_new_class("WP_Post_Type", lambda : WP_Post_Type(post_type, args))
    post_type_object.add_supports()
    post_type_object.add_rewrite_rules()
    post_type_object.register_meta_boxes()
    wp_post_types[post_type] = post_type_object
    post_type_object.add_hooks()
    post_type_object.register_taxonomies()
    #// 
    #// Fires after a post type is registered.
    #// 
    #// @since 3.3.0
    #// @since 4.6.0 Converted the `$post_type` parameter to accept a `WP_Post_Type` object.
    #// 
    #// @param string       $post_type        Post type.
    #// @param WP_Post_Type $post_type_object Arguments used to register the post type.
    #//
    do_action("registered_post_type", post_type, post_type_object)
    return post_type_object
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
def unregister_post_type(post_type=None, *args_):
    
    global wp_post_types
    php_check_if_defined("wp_post_types")
    if (not post_type_exists(post_type)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post_type", __("Invalid post type.")))
    # end if
    post_type_object = get_post_type_object(post_type)
    #// Do not allow unregistering internal post types.
    if post_type_object._builtin:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post_type", __("Unregistering a built-in post type is not allowed")))
    # end if
    post_type_object.remove_supports()
    post_type_object.remove_rewrite_rules()
    post_type_object.unregister_meta_boxes()
    post_type_object.remove_hooks()
    post_type_object.unregister_taxonomies()
    wp_post_types[post_type] = None
    #// 
    #// Fires after a post type was unregistered.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $post_type Post type key.
    #//
    do_action("unregistered_post_type", post_type)
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
def get_post_type_capabilities(args=None, *args_):
    
    if (not php_is_array(args.capability_type)):
        args.capability_type = Array(args.capability_type, args.capability_type + "s")
    # end if
    #// Singular base for meta capabilities, plural base for primitive capabilities.
    singular_base, plural_base = args.capability_type
    default_capabilities = Array({"edit_post": "edit_" + singular_base, "read_post": "read_" + singular_base, "delete_post": "delete_" + singular_base, "edit_posts": "edit_" + plural_base, "edit_others_posts": "edit_others_" + plural_base, "delete_posts": "delete_" + plural_base, "publish_posts": "publish_" + plural_base, "read_private_posts": "read_private_" + plural_base})
    #// Primitive capabilities used within map_meta_cap():
    if args.map_meta_cap:
        default_capabilities_for_mapping = Array({"read": "read", "delete_private_posts": "delete_private_" + plural_base, "delete_published_posts": "delete_published_" + plural_base, "delete_others_posts": "delete_others_" + plural_base, "edit_private_posts": "edit_private_" + plural_base, "edit_published_posts": "edit_published_" + plural_base})
        default_capabilities = php_array_merge(default_capabilities, default_capabilities_for_mapping)
    # end if
    capabilities = php_array_merge(default_capabilities, args.capabilities)
    #// Post creation capability simply maps to edit_posts by default:
    if (not (php_isset(lambda : capabilities["create_posts"]))):
        capabilities["create_posts"] = capabilities["edit_posts"]
    # end if
    #// Remember meta capabilities for future reference.
    if args.map_meta_cap:
        _post_type_meta_capabilities(capabilities)
    # end if
    return capabilities
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
def _post_type_meta_capabilities(capabilities=None, *args_):
    
    global post_type_meta_caps
    php_check_if_defined("post_type_meta_caps")
    for core,custom in capabilities:
        if php_in_array(core, Array("read_post", "delete_post", "edit_post")):
            post_type_meta_caps[custom] = core
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
def get_post_type_labels(post_type_object=None, *args_):
    
    nohier_vs_hier_defaults = Array({"name": Array(_x("Posts", "post type general name"), _x("Pages", "post type general name")), "singular_name": Array(_x("Post", "post type singular name"), _x("Page", "post type singular name")), "add_new": Array(_x("Add New", "post"), _x("Add New", "page")), "add_new_item": Array(__("Add New Post"), __("Add New Page")), "edit_item": Array(__("Edit Post"), __("Edit Page")), "new_item": Array(__("New Post"), __("New Page")), "view_item": Array(__("View Post"), __("View Page")), "view_items": Array(__("View Posts"), __("View Pages")), "search_items": Array(__("Search Posts"), __("Search Pages")), "not_found": Array(__("No posts found."), __("No pages found.")), "not_found_in_trash": Array(__("No posts found in Trash."), __("No pages found in Trash.")), "parent_item_colon": Array(None, __("Parent Page:")), "all_items": Array(__("All Posts"), __("All Pages")), "archives": Array(__("Post Archives"), __("Page Archives")), "attributes": Array(__("Post Attributes"), __("Page Attributes")), "insert_into_item": Array(__("Insert into post"), __("Insert into page")), "uploaded_to_this_item": Array(__("Uploaded to this post"), __("Uploaded to this page")), "featured_image": Array(_x("Featured image", "post"), _x("Featured image", "page")), "set_featured_image": Array(_x("Set featured image", "post"), _x("Set featured image", "page")), "remove_featured_image": Array(_x("Remove featured image", "post"), _x("Remove featured image", "page")), "use_featured_image": Array(_x("Use as featured image", "post"), _x("Use as featured image", "page")), "filter_items_list": Array(__("Filter posts list"), __("Filter pages list")), "items_list_navigation": Array(__("Posts list navigation"), __("Pages list navigation")), "items_list": Array(__("Posts list"), __("Pages list")), "item_published": Array(__("Post published."), __("Page published.")), "item_published_privately": Array(__("Post published privately."), __("Page published privately.")), "item_reverted_to_draft": Array(__("Post reverted to draft."), __("Page reverted to draft.")), "item_scheduled": Array(__("Post scheduled."), __("Page scheduled.")), "item_updated": Array(__("Post updated."), __("Page updated."))})
    nohier_vs_hier_defaults["menu_name"] = nohier_vs_hier_defaults["name"]
    labels = _get_custom_object_labels(post_type_object, nohier_vs_hier_defaults)
    post_type = post_type_object.name
    default_labels = copy.deepcopy(labels)
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
    labels = apply_filters(str("post_type_labels_") + str(post_type), labels)
    #// Ensure that the filtered labels contain all required default values.
    labels = php_array_merge(default_labels, labels)
    return labels
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
def _get_custom_object_labels(object=None, nohier_vs_hier_defaults=None, *args_):
    
    object.labels = object.labels
    if (php_isset(lambda : object.label)) and php_empty(lambda : object.labels["name"]):
        object.labels["name"] = object.label
    # end if
    if (not (php_isset(lambda : object.labels["singular_name"]))) and (php_isset(lambda : object.labels["name"])):
        object.labels["singular_name"] = object.labels["name"]
    # end if
    if (not (php_isset(lambda : object.labels["name_admin_bar"]))):
        object.labels["name_admin_bar"] = object.labels["singular_name"] if (php_isset(lambda : object.labels["singular_name"])) else object.name
    # end if
    if (not (php_isset(lambda : object.labels["menu_name"]))) and (php_isset(lambda : object.labels["name"])):
        object.labels["menu_name"] = object.labels["name"]
    # end if
    if (not (php_isset(lambda : object.labels["all_items"]))) and (php_isset(lambda : object.labels["menu_name"])):
        object.labels["all_items"] = object.labels["menu_name"]
    # end if
    if (not (php_isset(lambda : object.labels["archives"]))) and (php_isset(lambda : object.labels["all_items"])):
        object.labels["archives"] = object.labels["all_items"]
    # end if
    defaults = Array()
    for key,value in nohier_vs_hier_defaults:
        defaults[key] = value[1] if object.hierarchical else value[0]
    # end for
    labels = php_array_merge(defaults, object.labels)
    object.labels = object.labels
    return labels
# end def _get_custom_object_labels
#// 
#// Add submenus for post types.
#// 
#// @access private
#// @since 3.1.0
#//
def _add_post_type_submenus(*args_):
    
    for ptype in get_post_types(Array({"show_ui": True})):
        ptype_obj = get_post_type_object(ptype)
        #// Sub-menus only.
        if (not ptype_obj.show_in_menu) or True == ptype_obj.show_in_menu:
            continue
        # end if
        add_submenu_page(ptype_obj.show_in_menu, ptype_obj.labels.name, ptype_obj.labels.all_items, ptype_obj.cap.edit_posts, str("edit.php?post_type=") + str(ptype))
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
def add_post_type_support(post_type=None, feature=None, *args):
    
    global _wp_post_type_features
    php_check_if_defined("_wp_post_type_features")
    features = feature
    for feature in features:
        if args:
            _wp_post_type_features[post_type][feature] = args
        else:
            _wp_post_type_features[post_type][feature] = True
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
def remove_post_type_support(post_type=None, feature=None, *args_):
    
    global _wp_post_type_features
    php_check_if_defined("_wp_post_type_features")
    _wp_post_type_features[post_type][feature] = None
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
def get_all_post_type_supports(post_type=None, *args_):
    
    global _wp_post_type_features
    php_check_if_defined("_wp_post_type_features")
    if (php_isset(lambda : _wp_post_type_features[post_type])):
        return _wp_post_type_features[post_type]
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
def post_type_supports(post_type=None, feature=None, *args_):
    
    global _wp_post_type_features
    php_check_if_defined("_wp_post_type_features")
    return (php_isset(lambda : _wp_post_type_features[post_type][feature]))
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
def get_post_types_by_support(feature=None, operator="and", *args_):
    
    global _wp_post_type_features
    php_check_if_defined("_wp_post_type_features")
    features = php_array_fill_keys(feature, True)
    return php_array_keys(wp_filter_object_list(_wp_post_type_features, features, operator))
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
def set_post_type(post_id=0, post_type="post", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post_type = sanitize_post_field("post_type", post_type, post_id, "db")
    return_ = wpdb.update(wpdb.posts, Array({"post_type": post_type}), Array({"ID": post_id}))
    clean_post_cache(post_id)
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
def is_post_type_viewable(post_type=None, *args_):
    
    if is_scalar(post_type):
        post_type = get_post_type_object(post_type)
        if (not post_type):
            return False
        # end if
    # end if
    return post_type.publicly_queryable or post_type._builtin and post_type.public
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
def get_posts(args=None, *args_):
    
    defaults = Array({"numberposts": 5, "category": 0, "orderby": "date", "order": "DESC", "include": Array(), "exclude": Array(), "meta_key": "", "meta_value": "", "post_type": "post", "suppress_filters": True})
    parsed_args = wp_parse_args(args, defaults)
    if php_empty(lambda : parsed_args["post_status"]):
        parsed_args["post_status"] = "inherit" if "attachment" == parsed_args["post_type"] else "publish"
    # end if
    if (not php_empty(lambda : parsed_args["numberposts"])) and php_empty(lambda : parsed_args["posts_per_page"]):
        parsed_args["posts_per_page"] = parsed_args["numberposts"]
    # end if
    if (not php_empty(lambda : parsed_args["category"])):
        parsed_args["cat"] = parsed_args["category"]
    # end if
    if (not php_empty(lambda : parsed_args["include"])):
        incposts = wp_parse_id_list(parsed_args["include"])
        parsed_args["posts_per_page"] = php_count(incposts)
        #// Only the number of posts included.
        parsed_args["post__in"] = incposts
    elif (not php_empty(lambda : parsed_args["exclude"])):
        parsed_args["post__not_in"] = wp_parse_id_list(parsed_args["exclude"])
    # end if
    parsed_args["ignore_sticky_posts"] = True
    parsed_args["no_found_rows"] = True
    get_posts = php_new_class("WP_Query", lambda : WP_Query())
    return get_posts.query(parsed_args)
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
def add_post_meta(post_id=None, meta_key=None, meta_value=None, unique=False, *args_):
    
    #// Make sure meta is added to the post, not a revision.
    the_post = wp_is_post_revision(post_id)
    if the_post:
        post_id = the_post
    # end if
    return add_metadata("post", post_id, meta_key, meta_value, unique)
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
def delete_post_meta(post_id=None, meta_key=None, meta_value="", *args_):
    
    #// Make sure meta is added to the post, not a revision.
    the_post = wp_is_post_revision(post_id)
    if the_post:
        post_id = the_post
    # end if
    return delete_metadata("post", post_id, meta_key, meta_value)
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
def get_post_meta(post_id=None, key="", single=False, *args_):
    
    return get_metadata("post", post_id, key, single)
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
def update_post_meta(post_id=None, meta_key=None, meta_value=None, prev_value="", *args_):
    
    #// Make sure meta is added to the post, not a revision.
    the_post = wp_is_post_revision(post_id)
    if the_post:
        post_id = the_post
    # end if
    return update_metadata("post", post_id, meta_key, meta_value, prev_value)
# end def update_post_meta
#// 
#// Deletes everything from post meta matching the given meta key.
#// 
#// @since 2.3.0
#// 
#// @param string $post_meta_key Key to search for when deleting.
#// @return bool Whether the post meta key was deleted from the database.
#//
def delete_post_meta_by_key(post_meta_key=None, *args_):
    
    return delete_metadata("post", None, post_meta_key, "", True)
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
def register_post_meta(post_type=None, meta_key=None, args=None, *args_):
    
    args["object_subtype"] = post_type
    return register_meta("post", meta_key, args)
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
def unregister_post_meta(post_type=None, meta_key=None, *args_):
    
    return unregister_meta_key("post", meta_key, post_type)
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
def get_post_custom(post_id=0, *args_):
    
    post_id = absint(post_id)
    if (not post_id):
        post_id = get_the_ID()
    # end if
    return get_post_meta(post_id)
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
def get_post_custom_keys(post_id=0, *args_):
    
    custom = get_post_custom(post_id)
    if (not php_is_array(custom)):
        return
    # end if
    keys = php_array_keys(custom)
    if keys:
        return keys
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
def get_post_custom_values(key="", post_id=0, *args_):
    
    if (not key):
        return None
    # end if
    custom = get_post_custom(post_id)
    return custom[key] if (php_isset(lambda : custom[key])) else None
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
def is_sticky(post_id=0, *args_):
    
    post_id = absint(post_id)
    if (not post_id):
        post_id = get_the_ID()
    # end if
    stickies = get_option("sticky_posts")
    is_sticky = php_is_array(stickies) and php_in_array(post_id, stickies)
    #// 
    #// Filters whether a post is sticky.
    #// 
    #// @since 5.3.0
    #// 
    #// @param bool $is_sticky Whether a post is sticky.
    #// @param int  $post_id   Post ID.
    #//
    return apply_filters("is_sticky", is_sticky, post_id)
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
def sanitize_post(post=None, context="display", *args_):
    
    if php_is_object(post):
        #// Check if post already filtered for this context.
        if (php_isset(lambda : post.filter)) and context == post.filter:
            return post
        # end if
        if (not (php_isset(lambda : post.ID))):
            post.ID = 0
        # end if
        for field in php_array_keys(get_object_vars(post)):
            post.field = sanitize_post_field(field, post.field, post.ID, context)
        # end for
        post.filter = context
    elif php_is_array(post):
        #// Check if post already filtered for this context.
        if (php_isset(lambda : post["filter"])) and context == post["filter"]:
            return post
        # end if
        if (not (php_isset(lambda : post["ID"]))):
            post["ID"] = 0
        # end if
        for field in php_array_keys(post):
            post[field] = sanitize_post_field(field, post[field], post["ID"], context)
        # end for
        post["filter"] = context
    # end if
    return post
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
def sanitize_post_field(field=None, value=None, post_id=None, context="display", *args_):
    
    int_fields = Array("ID", "post_parent", "menu_order")
    if php_in_array(field, int_fields):
        value = int(value)
    # end if
    #// Fields which contain arrays of integers.
    array_int_fields = Array("ancestors")
    if php_in_array(field, array_int_fields):
        value = php_array_map("absint", value)
        return value
    # end if
    if "raw" == context:
        return value
    # end if
    prefixed = False
    if False != php_strpos(field, "post_"):
        prefixed = True
        field_no_prefix = php_str_replace("post_", "", field)
    # end if
    if "edit" == context:
        format_to_edit = Array("post_content", "post_excerpt", "post_title", "post_password")
        if prefixed:
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
            value = apply_filters(str("edit_") + str(field), value, post_id)
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
            value = apply_filters(str(field_no_prefix) + str("_edit_pre"), value, post_id)
        else:
            value = apply_filters(str("edit_post_") + str(field), value, post_id)
        # end if
        if php_in_array(field, format_to_edit):
            if "post_content" == field:
                value = format_to_edit(value, user_can_richedit())
            else:
                value = format_to_edit(value)
            # end if
        else:
            value = esc_attr(value)
        # end if
    elif "db" == context:
        if prefixed:
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
            value = apply_filters(str("pre_") + str(field), value)
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
            value = apply_filters(str(field_no_prefix) + str("_save_pre"), value)
        else:
            value = apply_filters(str("pre_post_") + str(field), value)
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
            value = apply_filters(str(field) + str("_pre"), value)
        # end if
    else:
        #// Use display filters by default.
        if prefixed:
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
            value = apply_filters(str(field), value, post_id, context)
        else:
            value = apply_filters(str("post_") + str(field), value, post_id, context)
        # end if
        if "attribute" == context:
            value = esc_attr(value)
        elif "js" == context:
            value = esc_js(value)
        # end if
    # end if
    return value
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
def stick_post(post_id=None, *args_):
    
    stickies = get_option("sticky_posts")
    if (not php_is_array(stickies)):
        stickies = Array(post_id)
    # end if
    if (not php_in_array(post_id, stickies)):
        stickies[-1] = post_id
    # end if
    updated = update_option("sticky_posts", stickies)
    if updated:
        #// 
        #// Fires once a post has been added to the sticky list.
        #// 
        #// @since 4.6.0
        #// 
        #// @param int $post_id ID of the post that was stuck.
        #//
        do_action("post_stuck", post_id)
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
def unstick_post(post_id=None, *args_):
    
    stickies = get_option("sticky_posts")
    if (not php_is_array(stickies)):
        return
    # end if
    if (not php_in_array(post_id, stickies)):
        return
    # end if
    offset = php_array_search(post_id, stickies)
    if False == offset:
        return
    # end if
    array_splice(stickies, offset, 1)
    updated = update_option("sticky_posts", stickies)
    if updated:
        #// 
        #// Fires once a post has been removed from the sticky list.
        #// 
        #// @since 4.6.0
        #// 
        #// @param int $post_id ID of the post that was unstuck.
        #//
        do_action("post_unstuck", post_id)
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
def _count_posts_cache_key(type="post", perm="", *args_):
    
    cache_key = "posts-" + type
    if "readable" == perm and is_user_logged_in():
        post_type_object = get_post_type_object(type)
        if post_type_object and (not current_user_can(post_type_object.cap.read_private_posts)):
            cache_key += "_" + perm + "_" + get_current_user_id()
        # end if
    # end if
    return cache_key
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
def wp_count_posts(type="post", perm="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not post_type_exists(type)):
        return php_new_class("stdClass", lambda : stdClass())
    # end if
    cache_key = _count_posts_cache_key(type, perm)
    counts = wp_cache_get(cache_key, "counts")
    if False != counts:
        #// This filter is documented in wp-includes/post.php
        return apply_filters("wp_count_posts", counts, type, perm)
    # end if
    query = str("SELECT post_status, COUNT( * ) AS num_posts FROM ") + str(wpdb.posts) + str(" WHERE post_type = %s")
    if "readable" == perm and is_user_logged_in():
        post_type_object = get_post_type_object(type)
        if (not current_user_can(post_type_object.cap.read_private_posts)):
            query += wpdb.prepare(" AND (post_status != 'private' OR ( post_author = %d AND post_status = 'private' ))", get_current_user_id())
        # end if
    # end if
    query += " GROUP BY post_status"
    results = wpdb.get_results(wpdb.prepare(query, type), ARRAY_A)
    counts = php_array_fill_keys(get_post_stati(), 0)
    for row in results:
        counts[row["post_status"]] = row["num_posts"]
    # end for
    counts = counts
    wp_cache_set(cache_key, counts, "counts")
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
    return apply_filters("wp_count_posts", counts, type, perm)
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
def wp_count_attachments(mime_type="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    and_ = wp_post_mime_type_where(mime_type)
    count = wpdb.get_results(str("SELECT post_mime_type, COUNT( * ) AS num_posts FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'attachment' AND post_status != 'trash' ") + str(and_) + str(" GROUP BY post_mime_type"), ARRAY_A)
    counts = Array()
    for row in count:
        counts[row["post_mime_type"]] = row["num_posts"]
    # end for
    counts["trash"] = wpdb.get_var(str("SELECT COUNT( * ) FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'attachment' AND post_status = 'trash' ") + str(and_))
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
    return apply_filters("wp_count_attachments", counts, mime_type)
# end def wp_count_attachments
#// 
#// Get default post mime types.
#// 
#// @since 2.9.0
#// @since 5.3.0 Added the 'Documents', 'Spreadsheets', and 'Archives' mime type groups.
#// 
#// @return array List of post mime types.
#//
def get_post_mime_types(*args_):
    
    post_mime_types = Array({"image": Array(__("Images"), __("Manage Images"), _n_noop("Image <span class=\"count\">(%s)</span>", "Images <span class=\"count\">(%s)</span>")), "audio": Array(__("Audio"), __("Manage Audio"), _n_noop("Audio <span class=\"count\">(%s)</span>", "Audio <span class=\"count\">(%s)</span>")), "video": Array(__("Video"), __("Manage Video"), _n_noop("Video <span class=\"count\">(%s)</span>", "Video <span class=\"count\">(%s)</span>")), "document": Array(__("Documents"), __("Manage Documents"), _n_noop("Document <span class=\"count\">(%s)</span>", "Documents <span class=\"count\">(%s)</span>")), "spreadsheet": Array(__("Spreadsheets"), __("Manage Spreadsheets"), _n_noop("Spreadsheet <span class=\"count\">(%s)</span>", "Spreadsheets <span class=\"count\">(%s)</span>")), "archive": Array(_x("Archives", "file type group"), __("Manage Archives"), _n_noop("Archive <span class=\"count\">(%s)</span>", "Archives <span class=\"count\">(%s)</span>"))})
    ext_types = wp_get_ext_types()
    mime_types = wp_get_mime_types()
    for group,labels in post_mime_types:
        if php_in_array(group, Array("image", "audio", "video")):
            continue
        # end if
        if (not (php_isset(lambda : ext_types[group]))):
            post_mime_types[group] = None
            continue
        # end if
        group_mime_types = Array()
        for extension in ext_types[group]:
            for exts,mime in mime_types:
                if php_preg_match("!^(" + exts + ")$!i", extension):
                    group_mime_types[-1] = mime
                    break
                # end if
            # end for
        # end for
        group_mime_types = php_implode(",", array_unique(group_mime_types))
        post_mime_types[group_mime_types] = labels
        post_mime_types[group] = None
    # end for
    #// 
    #// Filters the default list of post mime types.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $post_mime_types Default list of post mime types.
    #//
    return apply_filters("post_mime_types", post_mime_types)
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
def wp_match_mime_types(wildcard_mime_types=None, real_mime_types=None, *args_):
    
    matches = Array()
    if php_is_string(wildcard_mime_types):
        wildcard_mime_types = php_array_map("trim", php_explode(",", wildcard_mime_types))
    # end if
    if php_is_string(real_mime_types):
        real_mime_types = php_array_map("trim", php_explode(",", real_mime_types))
    # end if
    patternses = Array()
    wild = "[-._a-z0-9]*"
    for type in wildcard_mime_types:
        mimes = php_array_map("trim", php_explode(",", type))
        for mime in mimes:
            regex = php_str_replace("__wildcard__", wild, preg_quote(php_str_replace("*", "__wildcard__", mime)))
            patternses[-1][type] = str("^") + str(regex) + str("$")
            if False == php_strpos(mime, "/"):
                patternses[-1][type] = str("^") + str(regex) + str("/")
                patternses[-1][type] = regex
            # end if
        # end for
    # end for
    asort(patternses)
    for patterns in patternses:
        for type,pattern in patterns:
            for real in real_mime_types:
                if php_preg_match(str("#") + str(pattern) + str("#"), real) and php_empty(lambda : matches[type]) or False == php_array_search(real, matches[type]):
                    matches[type][-1] = real
                # end if
            # end for
        # end for
    # end for
    return matches
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
def wp_post_mime_type_where(post_mime_types=None, table_alias="", *args_):
    
    where = ""
    wildcards = Array("", "%", "%/%")
    if php_is_string(post_mime_types):
        post_mime_types = php_array_map("trim", php_explode(",", post_mime_types))
    # end if
    wheres = Array()
    for mime_type in post_mime_types:
        mime_type = php_preg_replace("/\\s/", "", mime_type)
        slashpos = php_strpos(mime_type, "/")
        if False != slashpos:
            mime_group = php_preg_replace("/[^-*.a-zA-Z0-9]/", "", php_substr(mime_type, 0, slashpos))
            mime_subgroup = php_preg_replace("/[^-*.+a-zA-Z0-9]/", "", php_substr(mime_type, slashpos + 1))
            if php_empty(lambda : mime_subgroup):
                mime_subgroup = "*"
            else:
                mime_subgroup = php_str_replace("/", "", mime_subgroup)
            # end if
            mime_pattern = str(mime_group) + str("/") + str(mime_subgroup)
        else:
            mime_pattern = php_preg_replace("/[^-*.a-zA-Z0-9]/", "", mime_type)
            if False == php_strpos(mime_pattern, "*"):
                mime_pattern += "/*"
            # end if
        # end if
        mime_pattern = php_preg_replace("/\\*+/", "%", mime_pattern)
        if php_in_array(mime_type, wildcards):
            return ""
        # end if
        if False != php_strpos(mime_pattern, "%"):
            wheres[-1] = str("post_mime_type LIKE '") + str(mime_pattern) + str("'") if php_empty(lambda : table_alias) else str(table_alias) + str(".post_mime_type LIKE '") + str(mime_pattern) + str("'")
        else:
            wheres[-1] = str("post_mime_type = '") + str(mime_pattern) + str("'") if php_empty(lambda : table_alias) else str(table_alias) + str(".post_mime_type = '") + str(mime_pattern) + str("'")
        # end if
    # end for
    if (not php_empty(lambda : wheres)):
        where = " AND (" + join(" OR ", wheres) + ") "
    # end if
    return where
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
def wp_delete_post(postid=0, force_delete=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.posts) + str(" WHERE ID = %d"), postid))
    if (not post):
        return post
    # end if
    post = get_post(post)
    if (not force_delete) and "post" == post.post_type or "page" == post.post_type and "trash" != get_post_status(postid) and EMPTY_TRASH_DAYS:
        return wp_trash_post(postid)
    # end if
    if "attachment" == post.post_type:
        return wp_delete_attachment(postid, force_delete)
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
    check = apply_filters("pre_delete_post", None, post, force_delete)
    if None != check:
        return check
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
    do_action("before_delete_post", postid)
    delete_post_meta(postid, "_wp_trash_meta_status")
    delete_post_meta(postid, "_wp_trash_meta_time")
    wp_delete_object_term_relationships(postid, get_object_taxonomies(post.post_type))
    parent_data = Array({"post_parent": post.post_parent})
    parent_where = Array({"post_parent": postid})
    if is_post_type_hierarchical(post.post_type):
        #// Point children of this page to its parent, also clean the cache of affected children.
        children_query = wpdb.prepare(str("SELECT * FROM ") + str(wpdb.posts) + str(" WHERE post_parent = %d AND post_type = %s"), postid, post.post_type)
        children = wpdb.get_results(children_query)
        if children:
            wpdb.update(wpdb.posts, parent_data, parent_where + Array({"post_type": post.post_type}))
        # end if
    # end if
    #// Do raw query. wp_get_post_revisions() is filtered.
    revision_ids = wpdb.get_col(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_parent = %d AND post_type = 'revision'"), postid))
    #// Use wp_delete_post (via wp_delete_post_revision) again. Ensures any meta/misplaced data gets cleaned up.
    for revision_id in revision_ids:
        wp_delete_post_revision(revision_id)
    # end for
    #// Point all attachments to this post up one level.
    wpdb.update(wpdb.posts, parent_data, parent_where + Array({"post_type": "attachment"}))
    wp_defer_comment_counting(True)
    comment_ids = wpdb.get_col(wpdb.prepare(str("SELECT comment_ID FROM ") + str(wpdb.comments) + str(" WHERE comment_post_ID = %d"), postid))
    for comment_id in comment_ids:
        wp_delete_comment(comment_id, True)
    # end for
    wp_defer_comment_counting(False)
    post_meta_ids = wpdb.get_col(wpdb.prepare(str("SELECT meta_id FROM ") + str(wpdb.postmeta) + str(" WHERE post_id = %d "), postid))
    for mid in post_meta_ids:
        delete_metadata_by_mid("post", mid)
    # end for
    #// 
    #// Fires immediately before a post is deleted from the database.
    #// 
    #// @since 1.2.0
    #// 
    #// @param int $postid Post ID.
    #//
    do_action("delete_post", postid)
    result = wpdb.delete(wpdb.posts, Array({"ID": postid}))
    if (not result):
        return False
    # end if
    #// 
    #// Fires immediately after a post is deleted from the database.
    #// 
    #// @since 2.2.0
    #// 
    #// @param int $postid Post ID.
    #//
    do_action("deleted_post", postid)
    clean_post_cache(post)
    if is_post_type_hierarchical(post.post_type) and children:
        for child in children:
            clean_post_cache(child)
        # end for
    # end if
    wp_clear_scheduled_hook("publish_future_post", Array(postid))
    #// 
    #// Fires after a post is deleted, at the conclusion of wp_delete_post().
    #// 
    #// @since 3.2.0
    #// 
    #// @see wp_delete_post()
    #// 
    #// @param int $postid Post ID.
    #//
    do_action("after_delete_post", postid)
    return post
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
def _reset_front_page_settings_for_post(post_id=None, *args_):
    
    post = get_post(post_id)
    if "page" == post.post_type:
        #// 
        #// If the page is defined in option page_on_front or post_for_posts,
        #// adjust the corresponding options.
        #//
        if get_option("page_on_front") == post.ID:
            update_option("show_on_front", "posts")
            update_option("page_on_front", 0)
        # end if
        if get_option("page_for_posts") == post.ID:
            update_option("page_for_posts", 0)
        # end if
    # end if
    unstick_post(post.ID)
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
def wp_trash_post(post_id=0, *args_):
    
    if (not EMPTY_TRASH_DAYS):
        return wp_delete_post(post_id, True)
    # end if
    post = get_post(post_id)
    if (not post):
        return post
    # end if
    if "trash" == post.post_status:
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
    check = apply_filters("pre_trash_post", None, post)
    if None != check:
        return check
    # end if
    #// 
    #// Fires before a post is sent to the Trash.
    #// 
    #// @since 3.3.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("wp_trash_post", post_id)
    add_post_meta(post_id, "_wp_trash_meta_status", post.post_status)
    add_post_meta(post_id, "_wp_trash_meta_time", time())
    post_updated = wp_update_post(Array({"ID": post_id, "post_status": "trash"}))
    if (not post_updated):
        return False
    # end if
    wp_trash_post_comments(post_id)
    #// 
    #// Fires after a post is sent to the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("trashed_post", post_id)
    return post
# end def wp_trash_post
#// 
#// Restore a post or page from the Trash.
#// 
#// @since 2.9.0
#// 
#// @param int $post_id Optional. Post ID. Default is ID of the global $post.
#// @return WP_Post|false|null Post data on success, false or null on failure.
#//
def wp_untrash_post(post_id=0, *args_):
    
    post = get_post(post_id)
    if (not post):
        return post
    # end if
    if "trash" != post.post_status:
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
    check = apply_filters("pre_untrash_post", None, post)
    if None != check:
        return check
    # end if
    #// 
    #// Fires before a post is restored from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrash_post", post_id)
    post_status = get_post_meta(post_id, "_wp_trash_meta_status", True)
    delete_post_meta(post_id, "_wp_trash_meta_status")
    delete_post_meta(post_id, "_wp_trash_meta_time")
    post_updated = wp_update_post(Array({"ID": post_id, "post_status": post_status}))
    if (not post_updated):
        return False
    # end if
    wp_untrash_post_comments(post_id)
    #// 
    #// Fires after a post is restored from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrashed_post", post_id)
    return post
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
def wp_trash_post_comments(post=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = get_post(post)
    if php_empty(lambda : post):
        return
    # end if
    post_id = post.ID
    #// 
    #// Fires before comments are sent to the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("trash_post_comments", post_id)
    comments = wpdb.get_results(wpdb.prepare(str("SELECT comment_ID, comment_approved FROM ") + str(wpdb.comments) + str(" WHERE comment_post_ID = %d"), post_id))
    if php_empty(lambda : comments):
        return
    # end if
    #// Cache current status for each comment.
    statuses = Array()
    for comment in comments:
        statuses[comment.comment_ID] = comment.comment_approved
    # end for
    add_post_meta(post_id, "_wp_trash_meta_comments_status", statuses)
    #// Set status for all comments to post-trashed.
    result = wpdb.update(wpdb.comments, Array({"comment_approved": "post-trashed"}), Array({"comment_post_ID": post_id}))
    clean_comment_cache(php_array_keys(statuses))
    #// 
    #// Fires after comments are sent to the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int   $post_id  Post ID.
    #// @param array $statuses Array of comment statuses.
    #//
    do_action("trashed_post_comments", post_id, statuses)
    return result
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
def wp_untrash_post_comments(post=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = get_post(post)
    if php_empty(lambda : post):
        return
    # end if
    post_id = post.ID
    statuses = get_post_meta(post_id, "_wp_trash_meta_comments_status", True)
    if php_empty(lambda : statuses):
        return True
    # end if
    #// 
    #// Fires before comments are restored for a post from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrash_post_comments", post_id)
    #// Restore each comment to its original status.
    group_by_status = Array()
    for comment_id,comment_status in statuses:
        group_by_status[comment_status][-1] = comment_id
    # end for
    for status,comments in group_by_status:
        #// Sanity check. This shouldn't happen.
        if "post-trashed" == status:
            status = "0"
        # end if
        comments_in = php_implode(", ", php_array_map("intval", comments))
        wpdb.query(wpdb.prepare(str("UPDATE ") + str(wpdb.comments) + str(" SET comment_approved = %s WHERE comment_ID IN (") + str(comments_in) + str(")"), status))
    # end for
    clean_comment_cache(php_array_keys(statuses))
    delete_post_meta(post_id, "_wp_trash_meta_comments_status")
    #// 
    #// Fires after comments are restored for a post from the Trash.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $post_id Post ID.
    #//
    do_action("untrashed_post_comments", post_id)
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
def wp_get_post_categories(post_id=0, args=Array(), *args_):
    
    post_id = int(post_id)
    defaults = Array({"fields": "ids"})
    args = wp_parse_args(args, defaults)
    cats = wp_get_object_terms(post_id, "category", args)
    return cats
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
def wp_get_post_tags(post_id=0, args=Array(), *args_):
    
    return wp_get_post_terms(post_id, "post_tag", args)
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
def wp_get_post_terms(post_id=0, taxonomy="post_tag", args=Array(), *args_):
    
    post_id = int(post_id)
    defaults = Array({"fields": "all"})
    args = wp_parse_args(args, defaults)
    tags = wp_get_object_terms(post_id, taxonomy, args)
    return tags
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
def wp_get_recent_posts(args=Array(), output=ARRAY_A, *args_):
    
    if php_is_numeric(args):
        _deprecated_argument(__FUNCTION__, "3.1.0", __("Passing an integer number of posts is deprecated. Pass an array of arguments instead."))
        args = Array({"numberposts": absint(args)})
    # end if
    #// Set default arguments.
    defaults = Array({"numberposts": 10, "offset": 0, "category": 0, "orderby": "post_date", "order": "DESC", "include": "", "exclude": "", "meta_key": "", "meta_value": "", "post_type": "post", "post_status": "draft, publish, future, pending, private", "suppress_filters": True})
    parsed_args = wp_parse_args(args, defaults)
    results = get_posts(parsed_args)
    #// Backward compatibility. Prior to 3.1 expected posts to be returned in array.
    if ARRAY_A == output:
        for key,result in results:
            results[key] = get_object_vars(result)
        # end for
        return results if results else Array()
    # end if
    return results if results else False
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
def wp_insert_post(postarr=None, wp_error=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    user_id = get_current_user_id()
    defaults = Array({"post_author": user_id, "post_content": "", "post_content_filtered": "", "post_title": "", "post_excerpt": "", "post_status": "draft", "post_type": "post", "comment_status": "", "ping_status": "", "post_password": "", "to_ping": "", "pinged": "", "post_parent": 0, "menu_order": 0, "guid": "", "import_id": 0, "context": ""})
    postarr = wp_parse_args(postarr, defaults)
    postarr["filter"] = None
    postarr = sanitize_post(postarr, "db")
    #// Are we updating or creating?
    post_ID = 0
    update = False
    guid = postarr["guid"]
    if (not php_empty(lambda : postarr["ID"])):
        update = True
        #// Get the post ID and GUID.
        post_ID = postarr["ID"]
        post_before = get_post(post_ID)
        if php_is_null(post_before):
            if wp_error:
                return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post ID.")))
            # end if
            return 0
        # end if
        guid = get_post_field("guid", post_ID)
        previous_status = get_post_field("post_status", post_ID)
    else:
        previous_status = "new"
    # end if
    post_type = "post" if php_empty(lambda : postarr["post_type"]) else postarr["post_type"]
    post_title = postarr["post_title"]
    post_content = postarr["post_content"]
    post_excerpt = postarr["post_excerpt"]
    if (php_isset(lambda : postarr["post_name"])):
        post_name = postarr["post_name"]
    elif update:
        #// For an update, don't modify the post_name if it wasn't supplied as an argument.
        post_name = post_before.post_name
    # end if
    maybe_empty = "attachment" != post_type and (not post_content) and (not post_title) and (not post_excerpt) and post_type_supports(post_type, "editor") and post_type_supports(post_type, "title") and post_type_supports(post_type, "excerpt")
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
    if apply_filters("wp_insert_post_empty_content", maybe_empty, postarr):
        if wp_error:
            return php_new_class("WP_Error", lambda : WP_Error("empty_content", __("Content, title, and excerpt are empty.")))
        else:
            return 0
        # end if
    # end if
    post_status = "draft" if php_empty(lambda : postarr["post_status"]) else postarr["post_status"]
    if "attachment" == post_type and (not php_in_array(post_status, Array("inherit", "private", "trash", "auto-draft"), True)):
        post_status = "inherit"
    # end if
    if (not php_empty(lambda : postarr["post_category"])):
        #// Filter out empty terms.
        post_category = php_array_filter(postarr["post_category"])
    # end if
    #// Make sure we set a valid category.
    if php_empty(lambda : post_category) or 0 == php_count(post_category) or (not php_is_array(post_category)):
        #// 'post' requires at least one category.
        if "post" == post_type and "auto-draft" != post_status:
            post_category = Array(get_option("default_category"))
        else:
            post_category = Array()
        # end if
    # end if
    #// 
    #// Don't allow contributors to set the post slug for pending review posts.
    #// 
    #// For new posts check the primitive capability, for updates check the meta capability.
    #//
    post_type_object = get_post_type_object(post_type)
    if (not update) and "pending" == post_status and (not current_user_can(post_type_object.cap.publish_posts)):
        post_name = ""
    elif update and "pending" == post_status and (not current_user_can("publish_post", post_ID)):
        post_name = ""
    # end if
    #// 
    #// Create a valid post name. Drafts and pending posts are allowed to have
    #// an empty post name.
    #//
    if php_empty(lambda : post_name):
        if (not php_in_array(post_status, Array("draft", "pending", "auto-draft"))):
            post_name = sanitize_title(post_title)
        else:
            post_name = ""
        # end if
    else:
        #// On updates, we need to check to see if it's using the old, fixed sanitization context.
        check_name = sanitize_title(post_name, "", "old-save")
        if update and php_strtolower(urlencode(post_name)) == check_name and get_post_field("post_name", post_ID) == check_name:
            post_name = check_name
        else:
            #// new post, or slug has changed.
            post_name = sanitize_title(post_name)
        # end if
    # end if
    #// 
    #// If the post date is empty (due to having been new or a draft) and status
    #// is not 'draft' or 'pending', set date to now.
    #//
    if php_empty(lambda : postarr["post_date"]) or "0000-00-00 00:00:00" == postarr["post_date"]:
        if php_empty(lambda : postarr["post_date_gmt"]) or "0000-00-00 00:00:00" == postarr["post_date_gmt"]:
            post_date = current_time("mysql")
        else:
            post_date = get_date_from_gmt(postarr["post_date_gmt"])
        # end if
    else:
        post_date = postarr["post_date"]
    # end if
    #// Validate the date.
    mm = php_substr(post_date, 5, 2)
    jj = php_substr(post_date, 8, 2)
    aa = php_substr(post_date, 0, 4)
    valid_date = wp_checkdate(mm, jj, aa, post_date)
    if (not valid_date):
        if wp_error:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_date", __("Invalid date.")))
        else:
            return 0
        # end if
    # end if
    if php_empty(lambda : postarr["post_date_gmt"]) or "0000-00-00 00:00:00" == postarr["post_date_gmt"]:
        if (not php_in_array(post_status, get_post_stati(Array({"date_floating": True})), True)):
            post_date_gmt = get_gmt_from_date(post_date)
        else:
            post_date_gmt = "0000-00-00 00:00:00"
        # end if
    else:
        post_date_gmt = postarr["post_date_gmt"]
    # end if
    if update or "0000-00-00 00:00:00" == post_date:
        post_modified = current_time("mysql")
        post_modified_gmt = current_time("mysql", 1)
    else:
        post_modified = post_date
        post_modified_gmt = post_date_gmt
    # end if
    if "attachment" != post_type:
        now = gmdate("Y-m-d H:i:s")
        if "publish" == post_status:
            if strtotime(post_date_gmt) - strtotime(now) >= MINUTE_IN_SECONDS:
                post_status = "future"
            # end if
        elif "future" == post_status:
            if strtotime(post_date_gmt) - strtotime(now) < MINUTE_IN_SECONDS:
                post_status = "publish"
            # end if
        # end if
    # end if
    #// Comment status.
    if php_empty(lambda : postarr["comment_status"]):
        if update:
            comment_status = "closed"
        else:
            comment_status = get_default_comment_status(post_type)
        # end if
    else:
        comment_status = postarr["comment_status"]
    # end if
    #// These variables are needed by compact() later.
    post_content_filtered = postarr["post_content_filtered"]
    post_author = postarr["post_author"] if (php_isset(lambda : postarr["post_author"])) else user_id
    ping_status = get_default_comment_status(post_type, "pingback") if php_empty(lambda : postarr["ping_status"]) else postarr["ping_status"]
    to_ping = sanitize_trackback_urls(postarr["to_ping"]) if (php_isset(lambda : postarr["to_ping"])) else ""
    pinged = postarr["pinged"] if (php_isset(lambda : postarr["pinged"])) else ""
    import_id = postarr["import_id"] if (php_isset(lambda : postarr["import_id"])) else 0
    #// 
    #// The 'wp_insert_post_parent' filter expects all variables to be present.
    #// Previously, these variables would have already been extracted
    #//
    if (php_isset(lambda : postarr["menu_order"])):
        menu_order = int(postarr["menu_order"])
    else:
        menu_order = 0
    # end if
    post_password = postarr["post_password"] if (php_isset(lambda : postarr["post_password"])) else ""
    if "private" == post_status:
        post_password = ""
    # end if
    if (php_isset(lambda : postarr["post_parent"])):
        post_parent = int(postarr["post_parent"])
    else:
        post_parent = 0
    # end if
    new_postarr = php_array_merge(Array({"ID": post_ID}), compact(php_array_diff(php_array_keys(defaults), Array("context", "filter"))))
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
    post_parent = apply_filters("wp_insert_post_parent", post_parent, post_ID, new_postarr, postarr)
    #// 
    #// If the post is being untrashed and it has a desired slug stored in post meta,
    #// reassign it.
    #//
    if "trash" == previous_status and "trash" != post_status:
        desired_post_slug = get_post_meta(post_ID, "_wp_desired_post_slug", True)
        if desired_post_slug:
            delete_post_meta(post_ID, "_wp_desired_post_slug")
            post_name = desired_post_slug
        # end if
    # end if
    #// If a trashed post has the desired slug, change it and let this post have it.
    if "trash" != post_status and post_name:
        #// 
        #// Filters whether or not to add a `__trashed` suffix to trashed posts that match the name of the updated post.
        #// 
        #// @since 5.4.0
        #// 
        #// @param bool   $add_trashed_suffix Whether to attempt to add the suffix.
        #// @param string $post_name          The name of the post being updated.
        #// @param int    $post_ID            Post ID.
        #//
        add_trashed_suffix = apply_filters("add_trashed_suffix_to_trashed_posts", True, post_name, post_ID)
        if add_trashed_suffix:
            wp_add_trashed_suffix_to_post_name_for_trashed_posts(post_name, post_ID)
        # end if
    # end if
    #// When trashing an existing post, change its slug to allow non-trashed posts to use it.
    if "trash" == post_status and "trash" != previous_status and "new" != previous_status:
        post_name = wp_add_trashed_suffix_to_post_name_for_post(post_ID)
    # end if
    post_name = wp_unique_post_slug(post_name, post_ID, post_status, post_type, post_parent)
    #// Don't unslash.
    post_mime_type = postarr["post_mime_type"] if (php_isset(lambda : postarr["post_mime_type"])) else ""
    #// Expected_slashed (everything!).
    data = compact("post_author", "post_date", "post_date_gmt", "post_content", "post_content_filtered", "post_title", "post_excerpt", "post_status", "post_type", "comment_status", "ping_status", "post_password", "post_name", "to_ping", "pinged", "post_modified", "post_modified_gmt", "post_parent", "menu_order", "post_mime_type", "guid")
    emoji_fields = Array("post_title", "post_content", "post_excerpt")
    for emoji_field in emoji_fields:
        if (php_isset(lambda : data[emoji_field])):
            charset = wpdb.get_col_charset(wpdb.posts, emoji_field)
            if "utf8" == charset:
                data[emoji_field] = wp_encode_emoji(data[emoji_field])
            # end if
        # end if
    # end for
    if "attachment" == post_type:
        #// 
        #// Filters attachment post data before it is updated in or added to the database.
        #// 
        #// @since 3.9.0
        #// 
        #// @param array $data    An array of sanitized attachment post data.
        #// @param array $postarr An array of unsanitized attachment post data.
        #//
        data = apply_filters("wp_insert_attachment_data", data, postarr)
    else:
        #// 
        #// Filters slashed post data just before it is inserted into the database.
        #// 
        #// @since 2.7.0
        #// 
        #// @param array $data    An array of slashed post data.
        #// @param array $postarr An array of sanitized, but otherwise unmodified post data.
        #//
        data = apply_filters("wp_insert_post_data", data, postarr)
    # end if
    data = wp_unslash(data)
    where = Array({"ID": post_ID})
    if update:
        #// 
        #// Fires immediately before an existing post is updated in the database.
        #// 
        #// @since 2.5.0
        #// 
        #// @param int   $post_ID Post ID.
        #// @param array $data    Array of unslashed post data.
        #//
        do_action("pre_post_update", post_ID, data)
        if False == wpdb.update(wpdb.posts, data, where):
            if wp_error:
                return php_new_class("WP_Error", lambda : WP_Error("db_update_error", __("Could not update post in the database"), wpdb.last_error))
            else:
                return 0
            # end if
        # end if
    else:
        #// If there is a suggested ID, use it if not already present.
        if (not php_empty(lambda : import_id)):
            import_id = int(import_id)
            if (not wpdb.get_var(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE ID = %d"), import_id))):
                data["ID"] = import_id
            # end if
        # end if
        if False == wpdb.insert(wpdb.posts, data):
            if wp_error:
                return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert post into the database"), wpdb.last_error))
            else:
                return 0
            # end if
        # end if
        post_ID = int(wpdb.insert_id)
        #// Use the newly generated $post_ID.
        where = Array({"ID": post_ID})
    # end if
    if php_empty(lambda : data["post_name"]) and (not php_in_array(data["post_status"], Array("draft", "pending", "auto-draft"))):
        data["post_name"] = wp_unique_post_slug(sanitize_title(data["post_title"], post_ID), post_ID, data["post_status"], post_type, post_parent)
        wpdb.update(wpdb.posts, Array({"post_name": data["post_name"]}), where)
        clean_post_cache(post_ID)
    # end if
    if is_object_in_taxonomy(post_type, "category"):
        wp_set_post_categories(post_ID, post_category)
    # end if
    if (php_isset(lambda : postarr["tags_input"])) and is_object_in_taxonomy(post_type, "post_tag"):
        wp_set_post_tags(post_ID, postarr["tags_input"])
    # end if
    #// New-style support for all custom taxonomies.
    if (not php_empty(lambda : postarr["tax_input"])):
        for taxonomy,tags in postarr["tax_input"]:
            taxonomy_obj = get_taxonomy(taxonomy)
            if (not taxonomy_obj):
                #// translators: %s: Taxonomy name.
                _doing_it_wrong(__FUNCTION__, php_sprintf(__("Invalid taxonomy: %s."), taxonomy), "4.4.0")
                continue
            # end if
            #// array = hierarchical, string = non-hierarchical.
            if php_is_array(tags):
                tags = php_array_filter(tags)
            # end if
            if current_user_can(taxonomy_obj.cap.assign_terms):
                wp_set_post_terms(post_ID, tags, taxonomy)
            # end if
        # end for
    # end if
    if (not php_empty(lambda : postarr["meta_input"])):
        for field,value in postarr["meta_input"]:
            update_post_meta(post_ID, field, value)
        # end for
    # end if
    current_guid = get_post_field("guid", post_ID)
    #// Set GUID.
    if (not update) and "" == current_guid:
        wpdb.update(wpdb.posts, Array({"guid": get_permalink(post_ID)}), where)
    # end if
    if "attachment" == postarr["post_type"]:
        if (not php_empty(lambda : postarr["file"])):
            update_attached_file(post_ID, postarr["file"])
        # end if
        if (not php_empty(lambda : postarr["context"])):
            add_post_meta(post_ID, "_wp_attachment_context", postarr["context"], True)
        # end if
    # end if
    #// Set or remove featured image.
    if (php_isset(lambda : postarr["_thumbnail_id"])):
        thumbnail_support = current_theme_supports("post-thumbnails", post_type) and post_type_supports(post_type, "thumbnail") or "revision" == post_type
        if (not thumbnail_support) and "attachment" == post_type and post_mime_type:
            if wp_attachment_is("audio", post_ID):
                thumbnail_support = post_type_supports("attachment:audio", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:audio")
            elif wp_attachment_is("video", post_ID):
                thumbnail_support = post_type_supports("attachment:video", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:video")
            # end if
        # end if
        if thumbnail_support:
            thumbnail_id = php_intval(postarr["_thumbnail_id"])
            if -1 == thumbnail_id:
                delete_post_thumbnail(post_ID)
            else:
                set_post_thumbnail(post_ID, thumbnail_id)
            # end if
        # end if
    # end if
    clean_post_cache(post_ID)
    post = get_post(post_ID)
    if (not php_empty(lambda : postarr["page_template"])):
        post.page_template = postarr["page_template"]
        page_templates = wp_get_theme().get_page_templates(post)
        if "default" != postarr["page_template"] and (not (php_isset(lambda : page_templates[postarr["page_template"]]))):
            if wp_error:
                return php_new_class("WP_Error", lambda : WP_Error("invalid_page_template", __("Invalid page template.")))
            # end if
            update_post_meta(post_ID, "_wp_page_template", "default")
        else:
            update_post_meta(post_ID, "_wp_page_template", postarr["page_template"])
        # end if
    # end if
    if "attachment" != postarr["post_type"]:
        wp_transition_post_status(data["post_status"], previous_status, post)
    else:
        if update:
            #// 
            #// Fires once an existing attachment has been updated.
            #// 
            #// @since 2.0.0
            #// 
            #// @param int $post_ID Attachment ID.
            #//
            do_action("edit_attachment", post_ID)
            post_after = get_post(post_ID)
            #// 
            #// Fires once an existing attachment has been updated.
            #// 
            #// @since 4.4.0
            #// 
            #// @param int     $post_ID      Post ID.
            #// @param WP_Post $post_after   Post object following the update.
            #// @param WP_Post $post_before  Post object before the update.
            #//
            do_action("attachment_updated", post_ID, post_after, post_before)
        else:
            #// 
            #// Fires once an attachment has been added.
            #// 
            #// @since 2.0.0
            #// 
            #// @param int $post_ID Attachment ID.
            #//
            do_action("add_attachment", post_ID)
        # end if
        return post_ID
    # end if
    if update:
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
        do_action(str("edit_post_") + str(post.post_type), post_ID, post)
        #// 
        #// Fires once an existing post has been updated.
        #// 
        #// @since 1.2.0
        #// 
        #// @param int     $post_ID Post ID.
        #// @param WP_Post $post    Post object.
        #//
        do_action("edit_post", post_ID, post)
        post_after = get_post(post_ID)
        #// 
        #// Fires once an existing post has been updated.
        #// 
        #// @since 3.0.0
        #// 
        #// @param int     $post_ID      Post ID.
        #// @param WP_Post $post_after   Post object following the update.
        #// @param WP_Post $post_before  Post object before the update.
        #//
        do_action("post_updated", post_ID, post_after, post_before)
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
    do_action(str("save_post_") + str(post.post_type), post_ID, post, update)
    #// 
    #// Fires once a post has been saved.
    #// 
    #// @since 1.5.0
    #// 
    #// @param int     $post_ID Post ID.
    #// @param WP_Post $post    Post object.
    #// @param bool    $update  Whether this is an existing post being updated or not.
    #//
    do_action("save_post", post_ID, post, update)
    #// 
    #// Fires once a post has been saved.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int     $post_ID Post ID.
    #// @param WP_Post $post    Post object.
    #// @param bool    $update  Whether this is an existing post being updated or not.
    #//
    do_action("wp_insert_post", post_ID, post, update)
    return post_ID
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
def wp_update_post(postarr=Array(), wp_error=False, *args_):
    
    if php_is_object(postarr):
        #// Non-escaped post was passed.
        postarr = get_object_vars(postarr)
        postarr = wp_slash(postarr)
    # end if
    #// First, get all of the original fields.
    post = get_post(postarr["ID"], ARRAY_A)
    if php_is_null(post):
        if wp_error:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post ID.")))
        # end if
        return 0
    # end if
    #// Escape data pulled from DB.
    post = wp_slash(post)
    #// Passed post category list overwrites existing category list if not empty.
    if (php_isset(lambda : postarr["post_category"])) and php_is_array(postarr["post_category"]) and 0 != php_count(postarr["post_category"]):
        post_cats = postarr["post_category"]
    else:
        post_cats = post["post_category"]
    # end if
    #// Drafts shouldn't be assigned a date unless explicitly done so by the user.
    if (php_isset(lambda : post["post_status"])) and php_in_array(post["post_status"], Array("draft", "pending", "auto-draft")) and php_empty(lambda : postarr["edit_date"]) and "0000-00-00 00:00:00" == post["post_date_gmt"]:
        clear_date = True
    else:
        clear_date = False
    # end if
    #// Merge old and new fields with new fields overwriting old ones.
    postarr = php_array_merge(post, postarr)
    postarr["post_category"] = post_cats
    if clear_date:
        postarr["post_date"] = current_time("mysql")
        postarr["post_date_gmt"] = ""
    # end if
    if "attachment" == postarr["post_type"]:
        return wp_insert_attachment(postarr, False, 0, wp_error)
    # end if
    #// Discard 'tags_input' parameter if it's the same as existing post tags.
    if (php_isset(lambda : postarr["tags_input"])) and is_object_in_taxonomy(postarr["post_type"], "post_tag"):
        tags = get_the_terms(postarr["ID"], "post_tag")
        tag_names = Array()
        if tags and (not is_wp_error(tags)):
            tag_names = wp_list_pluck(tags, "name")
        # end if
        if postarr["tags_input"] == tag_names:
            postarr["tags_input"] = None
        # end if
    # end if
    return wp_insert_post(postarr, wp_error)
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
def wp_publish_post(post=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = get_post(post)
    if (not post):
        return
    # end if
    if "publish" == post.post_status:
        return
    # end if
    wpdb.update(wpdb.posts, Array({"post_status": "publish"}), Array({"ID": post.ID}))
    clean_post_cache(post.ID)
    old_status = post.post_status
    post.post_status = "publish"
    wp_transition_post_status("publish", old_status, post)
    #// This action is documented in wp-includes/post.php
    do_action(str("edit_post_") + str(post.post_type), post.ID, post)
    #// This action is documented in wp-includes/post.php
    do_action("edit_post", post.ID, post)
    #// This action is documented in wp-includes/post.php
    do_action(str("save_post_") + str(post.post_type), post.ID, post, True)
    #// This action is documented in wp-includes/post.php
    do_action("save_post", post.ID, post, True)
    #// This action is documented in wp-includes/post.php
    do_action("wp_insert_post", post.ID, post, True)
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
def check_and_publish_future_post(post_id=None, *args_):
    
    post = get_post(post_id)
    if php_empty(lambda : post):
        return
    # end if
    if "future" != post.post_status:
        return
    # end if
    time = strtotime(post.post_date_gmt + " GMT")
    #// Uh oh, someone jumped the gun!
    if time > time():
        wp_clear_scheduled_hook("publish_future_post", Array(post_id))
        #// Clear anything else in the system.
        wp_schedule_single_event(time, "publish_future_post", Array(post_id))
        return
    # end if
    #// wp_publish_post() returns no meaningful value.
    wp_publish_post(post_id)
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
def wp_unique_post_slug(slug=None, post_ID=None, post_status=None, post_type=None, post_parent=None, *args_):
    
    if php_in_array(post_status, Array("draft", "pending", "auto-draft")) or "inherit" == post_status and "revision" == post_type or "user_request" == post_type:
        return slug
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
    override_slug = apply_filters("pre_wp_unique_post_slug", None, slug, post_ID, post_status, post_type, post_parent)
    if None != override_slug:
        return override_slug
    # end if
    global wpdb,wp_rewrite
    php_check_if_defined("wpdb","wp_rewrite")
    original_slug = slug
    feeds = wp_rewrite.feeds
    if (not php_is_array(feeds)):
        feeds = Array()
    # end if
    if "attachment" == post_type:
        #// Attachment slugs must be unique across all types.
        check_sql = str("SELECT post_name FROM ") + str(wpdb.posts) + str(" WHERE post_name = %s AND ID != %d LIMIT 1")
        post_name_check = wpdb.get_var(wpdb.prepare(check_sql, slug, post_ID))
        #// 
        #// Filters whether the post slug would make a bad attachment slug.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool   $bad_slug Whether the slug would be bad as an attachment slug.
        #// @param string $slug     The post slug.
        #//
        if post_name_check or php_in_array(slug, feeds) or "embed" == slug or apply_filters("wp_unique_post_slug_is_bad_attachment_slug", False, slug):
            suffix = 2
            while True:
                alt_post_name = _truncate_post_slug(slug, 200 - php_strlen(suffix) + 1) + str("-") + str(suffix)
                post_name_check = wpdb.get_var(wpdb.prepare(check_sql, alt_post_name, post_ID))
                suffix += 1
                
                if post_name_check:
                    break
                # end if
            # end while
            slug = alt_post_name
        # end if
    elif is_post_type_hierarchical(post_type):
        if "nav_menu_item" == post_type:
            return slug
        # end if
        #// 
        #// Page slugs must be unique within their own trees. Pages are in a separate
        #// namespace than posts so page slugs are allowed to overlap post slugs.
        #//
        check_sql = str("SELECT post_name FROM ") + str(wpdb.posts) + str(" WHERE post_name = %s AND post_type IN ( %s, 'attachment' ) AND ID != %d AND post_parent = %d LIMIT 1")
        post_name_check = wpdb.get_var(wpdb.prepare(check_sql, slug, post_type, post_ID, post_parent))
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
        if post_name_check or php_in_array(slug, feeds) or "embed" == slug or php_preg_match(str("@^(") + str(wp_rewrite.pagination_base) + str(")?\\d+$@"), slug) or apply_filters("wp_unique_post_slug_is_bad_hierarchical_slug", False, slug, post_type, post_parent):
            suffix = 2
            while True:
                alt_post_name = _truncate_post_slug(slug, 200 - php_strlen(suffix) + 1) + str("-") + str(suffix)
                post_name_check = wpdb.get_var(wpdb.prepare(check_sql, alt_post_name, post_type, post_ID, post_parent))
                suffix += 1
                
                if post_name_check:
                    break
                # end if
            # end while
            slug = alt_post_name
        # end if
    else:
        #// Post slugs must be unique across all posts.
        check_sql = str("SELECT post_name FROM ") + str(wpdb.posts) + str(" WHERE post_name = %s AND post_type = %s AND ID != %d LIMIT 1")
        post_name_check = wpdb.get_var(wpdb.prepare(check_sql, slug, post_type, post_ID))
        #// Prevent new post slugs that could result in URLs that conflict with date archives.
        post = get_post(post_ID)
        conflicts_with_date_archive = False
        if "post" == post_type and (not post) or post.post_name != slug and php_preg_match("/^[0-9]+$/", slug):
            slug_num = php_intval(slug)
            if slug_num:
                permastructs = php_array_values(php_array_filter(php_explode("/", get_option("permalink_structure"))))
                postname_index = php_array_search("%postname%", permastructs)
                #// 
                #// Potential date clashes are as follows:
                #// 
                #// - Any integer in the first permastruct position could be a year.
                #// - An integer between 1 and 12 that follows 'year' conflicts with 'monthnum'.
                #// - An integer between 1 and 31 that follows 'monthnum' conflicts with 'day'.
                #//
                if 0 == postname_index or postname_index and "%year%" == permastructs[postname_index - 1] and 13 > slug_num or postname_index and "%monthnum%" == permastructs[postname_index - 1] and 32 > slug_num:
                    conflicts_with_date_archive = True
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
        if post_name_check or php_in_array(slug, feeds) or "embed" == slug or conflicts_with_date_archive or apply_filters("wp_unique_post_slug_is_bad_flat_slug", False, slug, post_type):
            suffix = 2
            while True:
                alt_post_name = _truncate_post_slug(slug, 200 - php_strlen(suffix) + 1) + str("-") + str(suffix)
                post_name_check = wpdb.get_var(wpdb.prepare(check_sql, alt_post_name, post_type, post_ID))
                suffix += 1
                
                if post_name_check:
                    break
                # end if
            # end while
            slug = alt_post_name
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
    return apply_filters("wp_unique_post_slug", slug, post_ID, post_status, post_type, post_parent, original_slug)
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
def _truncate_post_slug(slug=None, length=200, *args_):
    
    if php_strlen(slug) > length:
        decoded_slug = urldecode(slug)
        if decoded_slug == slug:
            slug = php_substr(slug, 0, length)
        else:
            slug = utf8_uri_encode(decoded_slug, length)
        # end if
    # end if
    return php_rtrim(slug, "-")
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
def wp_add_post_tags(post_id=0, tags="", *args_):
    
    return wp_set_post_tags(post_id, tags, True)
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
def wp_set_post_tags(post_id=0, tags="", append=False, *args_):
    
    return wp_set_post_terms(post_id, tags, "post_tag", append)
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
def wp_set_post_terms(post_id=0, tags="", taxonomy="post_tag", append=False, *args_):
    
    post_id = int(post_id)
    if (not post_id):
        return False
    # end if
    if php_empty(lambda : tags):
        tags = Array()
    # end if
    if (not php_is_array(tags)):
        comma = _x(",", "tag delimiter")
        if "," != comma:
            tags = php_str_replace(comma, ",", tags)
        # end if
        tags = php_explode(",", php_trim(tags, " \n \r ,"))
    # end if
    #// 
    #// Hierarchical taxonomies must always pass IDs rather than names so that
    #// children with the same names but different parents aren't confused.
    #//
    if is_taxonomy_hierarchical(taxonomy):
        tags = array_unique(php_array_map("intval", tags))
    # end if
    return wp_set_object_terms(post_id, tags, taxonomy, append)
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
def wp_set_post_categories(post_ID=0, post_categories=Array(), append=False, *args_):
    
    post_ID = int(post_ID)
    post_type = get_post_type(post_ID)
    post_status = get_post_status(post_ID)
    #// If $post_categories isn't already an array, make it one:
    post_categories = post_categories
    if php_empty(lambda : post_categories):
        if "post" == post_type and "auto-draft" != post_status:
            post_categories = Array(get_option("default_category"))
            append = False
        else:
            post_categories = Array()
        # end if
    elif 1 == php_count(post_categories) and "" == reset(post_categories):
        return True
    # end if
    return wp_set_post_terms(post_ID, post_categories, "category", append)
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
def wp_transition_post_status(new_status=None, old_status=None, post=None, *args_):
    
    #// 
    #// Fires when a post is transitioned from one status to another.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string  $new_status New post status.
    #// @param string  $old_status Old post status.
    #// @param WP_Post $post       Post object.
    #//
    do_action("transition_post_status", new_status, old_status, post)
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
    do_action(str(old_status) + str("_to_") + str(new_status), post)
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
    do_action(str(new_status) + str("_") + str(post.post_type), post.ID, post)
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
def add_ping(post_id=None, uri=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    pung = php_trim(post.pinged)
    pung = php_preg_split("/\\s/", pung)
    if php_is_array(uri):
        pung = php_array_merge(pung, uri)
    else:
        pung[-1] = uri
    # end if
    new = php_implode("\n", pung)
    #// 
    #// Filters the new ping URL to add for the given post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $new New ping URL to add.
    #//
    new = apply_filters("add_ping", new)
    return_ = wpdb.update(wpdb.posts, Array({"pinged": new}), Array({"ID": post.ID}))
    clean_post_cache(post.ID)
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
def get_enclosed(post_id=None, *args_):
    
    custom_fields = get_post_custom(post_id)
    pung = Array()
    if (not php_is_array(custom_fields)):
        return pung
    # end if
    for key,val in custom_fields:
        if "enclosure" != key or (not php_is_array(val)):
            continue
        # end if
        for enc in val:
            enclosure = php_explode("\n", enc)
            pung[-1] = php_trim(enclosure[0])
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
    return apply_filters("get_enclosed", pung, post_id)
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
def get_pung(post_id=None, *args_):
    
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    pung = php_trim(post.pinged)
    pung = php_preg_split("/\\s/", pung)
    #// 
    #// Filters the list of already-pinged URLs for the given post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string[] $pung Array of URLs already pinged for the given post.
    #//
    return apply_filters("get_pung", pung)
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
def get_to_ping(post_id=None, *args_):
    
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    to_ping = sanitize_trackback_urls(post.to_ping)
    to_ping = php_preg_split("/\\s/", to_ping, -1, PREG_SPLIT_NO_EMPTY)
    #// 
    #// Filters the list of URLs yet to ping for the given post.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string[] $to_ping List of URLs yet to ping.
    #//
    return apply_filters("get_to_ping", to_ping)
# end def get_to_ping
#// 
#// Do trackbacks for a list of URLs.
#// 
#// @since 1.0.0
#// 
#// @param string $tb_list Comma separated list of URLs.
#// @param int    $post_id Post ID.
#//
def trackback_url_list(tb_list=None, post_id=None, *args_):
    
    if (not php_empty(lambda : tb_list)):
        #// Get post data.
        postdata = get_post(post_id, ARRAY_A)
        #// Form an excerpt.
        excerpt = strip_tags(postdata["post_excerpt"] if postdata["post_excerpt"] else postdata["post_content"])
        if php_strlen(excerpt) > 255:
            excerpt = php_substr(excerpt, 0, 252) + "&hellip;"
        # end if
        trackback_urls = php_explode(",", tb_list)
        for tb_url in trackback_urls:
            tb_url = php_trim(tb_url)
            trackback(tb_url, wp_unslash(postdata["post_title"]), excerpt, post_id)
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
def get_all_page_ids(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    page_ids = wp_cache_get("all_page_ids", "posts")
    if (not php_is_array(page_ids)):
        page_ids = wpdb.get_col(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'page'"))
        wp_cache_add("all_page_ids", page_ids, "posts")
    # end if
    return page_ids
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
def get_page(page=None, output=OBJECT, filter="raw", *args_):
    
    return get_post(page, output, filter)
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
def get_page_by_path(page_path=None, output=OBJECT, post_type="page", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    last_changed = wp_cache_get_last_changed("posts")
    hash = php_md5(page_path + serialize(post_type))
    cache_key = str("get_page_by_path:") + str(hash) + str(":") + str(last_changed)
    cached = wp_cache_get(cache_key, "posts")
    if False != cached:
        #// Special case: '0' is a bad `$page_path`.
        if "0" == cached or 0 == cached:
            return
        else:
            return get_post(cached, output)
        # end if
    # end if
    page_path = rawurlencode(urldecode(page_path))
    page_path = php_str_replace("%2F", "/", page_path)
    page_path = php_str_replace("%20", " ", page_path)
    parts = php_explode("/", php_trim(page_path, "/"))
    parts = php_array_map("sanitize_title_for_query", parts)
    escaped_parts = esc_sql(parts)
    in_string = "'" + php_implode("','", escaped_parts) + "'"
    if php_is_array(post_type):
        post_types = post_type
    else:
        post_types = Array(post_type, "attachment")
    # end if
    post_types = esc_sql(post_types)
    post_type_in_string = "'" + php_implode("','", post_types) + "'"
    sql = str("\n       SELECT ID, post_name, post_parent, post_type\n      FROM ") + str(wpdb.posts) + str("\n     WHERE post_name IN (") + str(in_string) + str(")\n      AND post_type IN (") + str(post_type_in_string) + str(")\n  ")
    pages = wpdb.get_results(sql, OBJECT_K)
    revparts = array_reverse(parts)
    foundid = 0
    for page in pages:
        if page.post_name == revparts[0]:
            count = 0
            p = page
            #// 
            #// Loop through the given path parts from right to left,
            #// ensuring each matches the post ancestry.
            #//
            while True:
                
                if not (0 != p.post_parent and (php_isset(lambda : pages[p.post_parent]))):
                    break
                # end if
                count += 1
                parent = pages[p.post_parent]
                if (not (php_isset(lambda : revparts[count]))) or parent.post_name != revparts[count]:
                    break
                # end if
                p = parent
            # end while
            if 0 == p.post_parent and php_count(revparts) == count + 1 and p.post_name == revparts[count]:
                foundid = page.ID
                if page.post_type == post_type:
                    break
                # end if
            # end if
        # end if
    # end for
    #// We cache misses as well as hits.
    wp_cache_set(cache_key, foundid, "posts")
    if foundid:
        return get_post(foundid, output)
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
def get_page_by_title(page_title=None, output=OBJECT, post_type="page", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_is_array(post_type):
        post_type = esc_sql(post_type)
        post_type_in_string = "'" + php_implode("','", post_type) + "'"
        sql = wpdb.prepare(str("\n          SELECT ID\n         FROM ") + str(wpdb.posts) + str("\n         WHERE post_title = %s\n         AND post_type IN (") + str(post_type_in_string) + str(")\n      "), page_title)
    else:
        sql = wpdb.prepare(str("\n          SELECT ID\n         FROM ") + str(wpdb.posts) + str("""\n           WHERE post_title = %s\n         AND post_type = %s\n        """), page_title, post_type)
    # end if
    page = wpdb.get_var(sql)
    if page:
        return get_post(page, output)
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
def get_page_children(page_id=None, pages=None, *args_):
    
    #// Build a hash of ID -> children.
    children = Array()
    for page in pages:
        children[php_intval(page.post_parent)][-1] = page
    # end for
    page_list = Array()
    #// Start the search by looking at immediate children.
    if (php_isset(lambda : children[page_id])):
        #// Always start at the end of the stack in order to preserve original `$pages` order.
        to_look = array_reverse(children[page_id])
        while True:
            
            if not (to_look):
                break
            # end if
            p = php_array_pop(to_look)
            page_list[-1] = p
            if (php_isset(lambda : children[p.ID])):
                for child in array_reverse(children[p.ID]):
                    #// Append to the `$to_look` stack to descend the tree.
                    to_look[-1] = child
                # end for
            # end if
        # end while
    # end if
    return page_list
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
def get_page_hierarchy(pages=None, page_id=0, *args_):
    
    if php_empty(lambda : pages):
        return Array()
    # end if
    children = Array()
    for p in pages:
        parent_id = php_intval(p.post_parent)
        children[parent_id][-1] = p
    # end for
    result = Array()
    _page_traverse_name(page_id, children, result)
    return result
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
def _page_traverse_name(page_id=None, children=None, result=None, *args_):
    
    if (php_isset(lambda : children[page_id])):
        for child in children[page_id]:
            result[child.ID] = child.post_name
            _page_traverse_name(child.ID, children, result)
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
def get_page_uri(page=0, *args_):
    
    if (not type(page).__name__ == "WP_Post"):
        page = get_post(page)
    # end if
    if (not page):
        return False
    # end if
    uri = page.post_name
    for parent in page.ancestors:
        parent = get_post(parent)
        if parent and parent.post_name:
            uri = parent.post_name + "/" + uri
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
    return apply_filters("get_page_uri", uri, page)
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
def get_pages(args=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    defaults = Array({"child_of": 0, "sort_order": "ASC", "sort_column": "post_title", "hierarchical": 1, "exclude": Array(), "include": Array(), "meta_key": "", "meta_value": "", "authors": "", "parent": -1, "exclude_tree": Array(), "number": "", "offset": 0, "post_type": "page", "post_status": "publish"})
    parsed_args = wp_parse_args(args, defaults)
    number = int(parsed_args["number"])
    offset = int(parsed_args["offset"])
    child_of = int(parsed_args["child_of"])
    hierarchical = parsed_args["hierarchical"]
    exclude = parsed_args["exclude"]
    meta_key = parsed_args["meta_key"]
    meta_value = parsed_args["meta_value"]
    parent = parsed_args["parent"]
    post_status = parsed_args["post_status"]
    #// Make sure the post type is hierarchical.
    hierarchical_post_types = get_post_types(Array({"hierarchical": True}))
    if (not php_in_array(parsed_args["post_type"], hierarchical_post_types)):
        return False
    # end if
    if parent > 0 and (not child_of):
        hierarchical = False
    # end if
    #// Make sure we have a valid post status.
    if (not php_is_array(post_status)):
        post_status = php_explode(",", post_status)
    # end if
    if php_array_diff(post_status, get_post_stati()):
        return False
    # end if
    #// $args can be whatever, only use the args defined in defaults to compute the key.
    key = php_md5(serialize(wp_array_slice_assoc(parsed_args, php_array_keys(defaults))))
    last_changed = wp_cache_get_last_changed("posts")
    cache_key = str("get_pages:") + str(key) + str(":") + str(last_changed)
    cache = wp_cache_get(cache_key, "posts")
    if False != cache:
        #// Convert to WP_Post instances.
        pages = php_array_map("get_post", cache)
        #// This filter is documented in wp-includes/post.php
        pages = apply_filters("get_pages", pages, parsed_args)
        return pages
    # end if
    inclusions = ""
    if (not php_empty(lambda : parsed_args["include"])):
        child_of = 0
        #// Ignore child_of, parent, exclude, meta_key, and meta_value params if using include.
        parent = -1
        exclude = ""
        meta_key = ""
        meta_value = ""
        hierarchical = False
        incpages = wp_parse_id_list(parsed_args["include"])
        if (not php_empty(lambda : incpages)):
            inclusions = " AND ID IN (" + php_implode(",", incpages) + ")"
        # end if
    # end if
    exclusions = ""
    if (not php_empty(lambda : exclude)):
        expages = wp_parse_id_list(exclude)
        if (not php_empty(lambda : expages)):
            exclusions = " AND ID NOT IN (" + php_implode(",", expages) + ")"
        # end if
    # end if
    author_query = ""
    if (not php_empty(lambda : parsed_args["authors"])):
        post_authors = wp_parse_list(parsed_args["authors"])
        if (not php_empty(lambda : post_authors)):
            for post_author in post_authors:
                #// Do we have an author id or an author login?
                if 0 == php_intval(post_author):
                    post_author = get_user_by("login", post_author)
                    if php_empty(lambda : post_author):
                        continue
                    # end if
                    if php_empty(lambda : post_author.ID):
                        continue
                    # end if
                    post_author = post_author.ID
                # end if
                if "" == author_query:
                    author_query = wpdb.prepare(" post_author = %d ", post_author)
                else:
                    author_query += wpdb.prepare(" OR post_author = %d ", post_author)
                # end if
            # end for
            if "" != author_query:
                author_query = str(" AND (") + str(author_query) + str(")")
            # end if
        # end if
    # end if
    join = ""
    where = str(exclusions) + str(" ") + str(inclusions) + str(" ")
    if "" != meta_key or "" != meta_value:
        join = str(" LEFT JOIN ") + str(wpdb.postmeta) + str(" ON ( ") + str(wpdb.posts) + str(".ID = ") + str(wpdb.postmeta) + str(".post_id )")
        #// meta_key and meta_value might be slashed.
        meta_key = wp_unslash(meta_key)
        meta_value = wp_unslash(meta_value)
        if "" != meta_key:
            where += wpdb.prepare(str(" AND ") + str(wpdb.postmeta) + str(".meta_key = %s"), meta_key)
        # end if
        if "" != meta_value:
            where += wpdb.prepare(str(" AND ") + str(wpdb.postmeta) + str(".meta_value = %s"), meta_value)
        # end if
    # end if
    if php_is_array(parent):
        post_parent__in = php_implode(",", php_array_map("absint", parent))
        if (not php_empty(lambda : post_parent__in)):
            where += str(" AND post_parent IN (") + str(post_parent__in) + str(")")
        # end if
    elif parent >= 0:
        where += wpdb.prepare(" AND post_parent = %d ", parent)
    # end if
    if 1 == php_count(post_status):
        where_post_type = wpdb.prepare("post_type = %s AND post_status = %s", parsed_args["post_type"], reset(post_status))
    else:
        post_status = php_implode("', '", post_status)
        where_post_type = wpdb.prepare(str("post_type = %s AND post_status IN ('") + str(post_status) + str("')"), parsed_args["post_type"])
    # end if
    orderby_array = Array()
    allowed_keys = Array("author", "post_author", "date", "post_date", "title", "post_title", "name", "post_name", "modified", "post_modified", "modified_gmt", "post_modified_gmt", "menu_order", "parent", "post_parent", "ID", "rand", "comment_count")
    for orderby in php_explode(",", parsed_args["sort_column"]):
        orderby = php_trim(orderby)
        if (not php_in_array(orderby, allowed_keys)):
            continue
        # end if
        for case in Switch(orderby):
            if case("menu_order"):
                break
            # end if
            if case("ID"):
                orderby = str(wpdb.posts) + str(".ID")
                break
            # end if
            if case("rand"):
                orderby = "RAND()"
                break
            # end if
            if case("comment_count"):
                orderby = str(wpdb.posts) + str(".comment_count")
                break
            # end if
            if case():
                if 0 == php_strpos(orderby, "post_"):
                    orderby = str(wpdb.posts) + str(".") + orderby
                else:
                    orderby = str(wpdb.posts) + str(".post_") + orderby
                # end if
            # end if
        # end for
        orderby_array[-1] = orderby
    # end for
    sort_column = php_implode(",", orderby_array) if (not php_empty(lambda : orderby_array)) else str(wpdb.posts) + str(".post_title")
    sort_order = php_strtoupper(parsed_args["sort_order"])
    if "" != sort_order and (not php_in_array(sort_order, Array("ASC", "DESC"))):
        sort_order = "ASC"
    # end if
    query = str("SELECT * FROM ") + str(wpdb.posts) + str(" ") + str(join) + str(" WHERE (") + str(where_post_type) + str(") ") + str(where) + str(" ")
    query += author_query
    query += " ORDER BY " + sort_column + " " + sort_order
    if (not php_empty(lambda : number)):
        query += " LIMIT " + offset + "," + number
    # end if
    pages = wpdb.get_results(query)
    if php_empty(lambda : pages):
        wp_cache_set(cache_key, Array(), "posts")
        #// This filter is documented in wp-includes/post.php
        pages = apply_filters("get_pages", Array(), parsed_args)
        return pages
    # end if
    #// Sanitize before caching so it'll only get done once.
    num_pages = php_count(pages)
    i = 0
    while i < num_pages:
        
        pages[i] = sanitize_post(pages[i], "raw")
        i += 1
    # end while
    #// Update cache.
    update_post_cache(pages)
    if child_of or hierarchical:
        pages = get_page_children(child_of, pages)
    # end if
    if (not php_empty(lambda : parsed_args["exclude_tree"])):
        exclude = wp_parse_id_list(parsed_args["exclude_tree"])
        for id in exclude:
            children = get_page_children(id, pages)
            for child in children:
                exclude[-1] = child.ID
            # end for
        # end for
        num_pages = php_count(pages)
        i = 0
        while i < num_pages:
            
            if php_in_array(pages[i].ID, exclude):
                pages[i] = None
            # end if
            i += 1
        # end while
    # end if
    page_structure = Array()
    for page in pages:
        page_structure[-1] = page.ID
    # end for
    wp_cache_set(cache_key, page_structure, "posts")
    #// Convert to WP_Post instances.
    pages = php_array_map("get_post", pages)
    #// 
    #// Filters the retrieved list of pages.
    #// 
    #// @since 2.1.0
    #// 
    #// @param WP_Post[] $pages       Array of page objects.
    #// @param array     $parsed_args Array of get_pages() arguments.
    #//
    return apply_filters("get_pages", pages, parsed_args)
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
def is_local_attachment(url=None, *args_):
    
    if php_strpos(url, home_url()) == False:
        return False
    # end if
    if php_strpos(url, home_url("/?attachment_id=")) != False:
        return True
    # end if
    id = url_to_postid(url)
    if id:
        post = get_post(id)
        if "attachment" == post.post_type:
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
def wp_insert_attachment(args=None, file=False, parent=0, wp_error=False, *args_):
    
    defaults = Array({"file": file, "post_parent": 0})
    data = wp_parse_args(args, defaults)
    if (not php_empty(lambda : parent)):
        data["post_parent"] = parent
    # end if
    data["post_type"] = "attachment"
    return wp_insert_post(data, wp_error)
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
def wp_delete_attachment(post_id=None, force_delete=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.posts) + str(" WHERE ID = %d"), post_id))
    if (not post):
        return post
    # end if
    post = get_post(post)
    if "attachment" != post.post_type:
        return False
    # end if
    if (not force_delete) and EMPTY_TRASH_DAYS and MEDIA_TRASH and "trash" != post.post_status:
        return wp_trash_post(post_id)
    # end if
    delete_post_meta(post_id, "_wp_trash_meta_status")
    delete_post_meta(post_id, "_wp_trash_meta_time")
    meta = wp_get_attachment_metadata(post_id)
    backup_sizes = get_post_meta(post.ID, "_wp_attachment_backup_sizes", True)
    file = get_attached_file(post_id)
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
    do_action("delete_attachment", post_id)
    wp_delete_object_term_relationships(post_id, Array("category", "post_tag"))
    wp_delete_object_term_relationships(post_id, get_object_taxonomies(post.post_type))
    #// Delete all for any posts.
    delete_metadata("post", None, "_thumbnail_id", post_id, True)
    wp_defer_comment_counting(True)
    comment_ids = wpdb.get_col(wpdb.prepare(str("SELECT comment_ID FROM ") + str(wpdb.comments) + str(" WHERE comment_post_ID = %d"), post_id))
    for comment_id in comment_ids:
        wp_delete_comment(comment_id, True)
    # end for
    wp_defer_comment_counting(False)
    post_meta_ids = wpdb.get_col(wpdb.prepare(str("SELECT meta_id FROM ") + str(wpdb.postmeta) + str(" WHERE post_id = %d "), post_id))
    for mid in post_meta_ids:
        delete_metadata_by_mid("post", mid)
    # end for
    #// This action is documented in wp-includes/post.php
    do_action("delete_post", post_id)
    result = wpdb.delete(wpdb.posts, Array({"ID": post_id}))
    if (not result):
        return False
    # end if
    #// This action is documented in wp-includes/post.php
    do_action("deleted_post", post_id)
    wp_delete_attachment_files(post_id, meta, backup_sizes, file)
    clean_post_cache(post)
    return post
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
def wp_delete_attachment_files(post_id=None, meta=None, backup_sizes=None, file=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    uploadpath = wp_get_upload_dir()
    deleted = True
    if (not php_empty(lambda : meta["thumb"])):
        #// Don't delete the thumb if another attachment uses it.
        if (not wpdb.get_row(wpdb.prepare(str("SELECT meta_id FROM ") + str(wpdb.postmeta) + str(" WHERE meta_key = '_wp_attachment_metadata' AND meta_value LIKE %s AND post_id <> %d"), "%" + wpdb.esc_like(meta["thumb"]) + "%", post_id))):
            thumbfile = php_str_replace(wp_basename(file), meta["thumb"], file)
            if (not php_empty(lambda : thumbfile)):
                thumbfile = path_join(uploadpath["basedir"], thumbfile)
                thumbdir = path_join(uploadpath["basedir"], php_dirname(file))
                if (not wp_delete_file_from_directory(thumbfile, thumbdir)):
                    deleted = False
                # end if
            # end if
        # end if
    # end if
    #// Remove intermediate and backup images if there are any.
    if (php_isset(lambda : meta["sizes"])) and php_is_array(meta["sizes"]):
        intermediate_dir = path_join(uploadpath["basedir"], php_dirname(file))
        for size,sizeinfo in meta["sizes"]:
            intermediate_file = php_str_replace(wp_basename(file), sizeinfo["file"], file)
            if (not php_empty(lambda : intermediate_file)):
                intermediate_file = path_join(uploadpath["basedir"], intermediate_file)
                if (not wp_delete_file_from_directory(intermediate_file, intermediate_dir)):
                    deleted = False
                # end if
            # end if
        # end for
    # end if
    if (not php_empty(lambda : meta["original_image"])):
        if php_empty(lambda : intermediate_dir):
            intermediate_dir = path_join(uploadpath["basedir"], php_dirname(file))
        # end if
        original_image = php_str_replace(wp_basename(file), meta["original_image"], file)
        if (not php_empty(lambda : original_image)):
            original_image = path_join(uploadpath["basedir"], original_image)
            if (not wp_delete_file_from_directory(original_image, intermediate_dir)):
                deleted = False
            # end if
        # end if
    # end if
    if php_is_array(backup_sizes):
        del_dir = path_join(uploadpath["basedir"], php_dirname(meta["file"]))
        for size in backup_sizes:
            del_file = path_join(php_dirname(meta["file"]), size["file"])
            if (not php_empty(lambda : del_file)):
                del_file = path_join(uploadpath["basedir"], del_file)
                if (not wp_delete_file_from_directory(del_file, del_dir)):
                    deleted = False
                # end if
            # end if
        # end for
    # end if
    if (not wp_delete_file_from_directory(file, uploadpath["basedir"])):
        deleted = False
    # end if
    return deleted
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
def wp_get_attachment_metadata(attachment_id=0, unfiltered=False, *args_):
    
    attachment_id = int(attachment_id)
    post = get_post(attachment_id)
    if (not post):
        return False
    # end if
    data = get_post_meta(post.ID, "_wp_attachment_metadata", True)
    if unfiltered:
        return data
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
    return apply_filters("wp_get_attachment_metadata", data, post.ID)
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
def wp_update_attachment_metadata(attachment_id=None, data=None, *args_):
    
    attachment_id = int(attachment_id)
    post = get_post(attachment_id)
    if (not post):
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
    data = apply_filters("wp_update_attachment_metadata", data, post.ID)
    if data:
        return update_post_meta(post.ID, "_wp_attachment_metadata", data)
    else:
        return delete_post_meta(post.ID, "_wp_attachment_metadata")
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
def wp_get_attachment_url(attachment_id=0, *args_):
    
    attachment_id = int(attachment_id)
    post = get_post(attachment_id)
    if (not post):
        return False
    # end if
    if "attachment" != post.post_type:
        return False
    # end if
    url = ""
    #// Get attached file.
    file = get_post_meta(post.ID, "_wp_attached_file", True)
    if file:
        #// Get upload directory.
        uploads = wp_get_upload_dir()
        if uploads and False == uploads["error"]:
            #// Check that the upload base exists in the file location.
            if 0 == php_strpos(file, uploads["basedir"]):
                #// Replace file location with url location.
                url = php_str_replace(uploads["basedir"], uploads["baseurl"], file)
            elif False != php_strpos(file, "wp-content/uploads"):
                #// Get the directory name relative to the basedir (back compat for pre-2.7 uploads).
                url = trailingslashit(uploads["baseurl"] + "/" + _wp_get_attachment_relative_path(file)) + wp_basename(file)
            else:
                #// It's a newly-uploaded file, therefore $file is relative to the basedir.
                url = uploads["baseurl"] + str("/") + str(file)
            # end if
        # end if
    # end if
    #// 
    #// If any of the above options failed, Fallback on the GUID as used pre-2.7,
    #// not recommended to rely upon this.
    #//
    if php_empty(lambda : url):
        url = get_the_guid(post.ID)
    # end if
    #// On SSL front end, URLs should be HTTPS.
    if is_ssl() and (not is_admin()) and "wp-login.php" != PHP_GLOBALS["pagenow"]:
        url = set_url_scheme(url)
    # end if
    #// 
    #// Filters the attachment URL.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $url           URL for the given attachment.
    #// @param int    $attachment_id Attachment post ID.
    #//
    url = apply_filters("wp_get_attachment_url", url, post.ID)
    if php_empty(lambda : url):
        return False
    # end if
    return url
# end def wp_get_attachment_url
#// 
#// Retrieves the caption for an attachment.
#// 
#// @since 4.6.0
#// 
#// @param int $post_id Optional. Attachment ID. Default is the ID of the global `$post`.
#// @return string|false False on failure. Attachment caption on success.
#//
def wp_get_attachment_caption(post_id=0, *args_):
    
    post_id = int(post_id)
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    if "attachment" != post.post_type:
        return False
    # end if
    caption = post.post_excerpt
    #// 
    #// Filters the attachment caption.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $caption Caption for the given attachment.
    #// @param int    $post_id Attachment ID.
    #//
    return apply_filters("wp_get_attachment_caption", caption, post.ID)
# end def wp_get_attachment_caption
#// 
#// Retrieve thumbnail for an attachment.
#// 
#// @since 2.1.0
#// 
#// @param int $post_id Optional. Attachment ID. Default 0.
#// @return string|false False on failure. Thumbnail file path on success.
#//
def wp_get_attachment_thumb_file(post_id=0, *args_):
    
    post_id = int(post_id)
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    imagedata = wp_get_attachment_metadata(post.ID)
    if (not php_is_array(imagedata)):
        return False
    # end if
    file = get_attached_file(post.ID)
    if (not php_empty(lambda : imagedata["thumb"])):
        thumbfile = php_str_replace(wp_basename(file), imagedata["thumb"], file)
        if php_file_exists(thumbfile):
            #// 
            #// Filters the attachment thumbnail file path.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string $thumbfile File path to the attachment thumbnail.
            #// @param int    $post_id   Attachment ID.
            #//
            return apply_filters("wp_get_attachment_thumb_file", thumbfile, post.ID)
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
def wp_get_attachment_thumb_url(post_id=0, *args_):
    
    post_id = int(post_id)
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    url = wp_get_attachment_url(post.ID)
    if (not url):
        return False
    # end if
    sized = image_downsize(post_id, "thumbnail")
    if sized:
        return sized[0]
    # end if
    thumb = wp_get_attachment_thumb_file(post.ID)
    if (not thumb):
        return False
    # end if
    url = php_str_replace(wp_basename(url), wp_basename(thumb), url)
    #// 
    #// Filters the attachment thumbnail URL.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $url     URL for the attachment thumbnail.
    #// @param int    $post_id Attachment ID.
    #//
    return apply_filters("wp_get_attachment_thumb_url", url, post.ID)
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
def wp_attachment_is(type=None, post=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    file = get_attached_file(post.ID)
    if (not file):
        return False
    # end if
    if 0 == php_strpos(post.post_mime_type, type + "/"):
        return True
    # end if
    check = wp_check_filetype(file)
    if php_empty(lambda : check["ext"]):
        return False
    # end if
    ext = check["ext"]
    if "import" != post.post_mime_type:
        return type == ext
    # end if
    for case in Switch(type):
        if case("image"):
            image_exts = Array("jpg", "jpeg", "jpe", "gif", "png")
            return php_in_array(ext, image_exts)
        # end if
        if case("audio"):
            return php_in_array(ext, wp_get_audio_extensions())
        # end if
        if case("video"):
            return php_in_array(ext, wp_get_video_extensions())
        # end if
        if case():
            return type == ext
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
def wp_attachment_is_image(post=None, *args_):
    
    return wp_attachment_is("image", post)
# end def wp_attachment_is_image
#// 
#// Retrieve the icon for a MIME type or attachment.
#// 
#// @since 2.1.0
#// 
#// @param string|int $mime MIME type or attachment ID.
#// @return string|false Icon, false otherwise.
#//
def wp_mime_type_icon(mime=0, *args_):
    
    if (not php_is_numeric(mime)):
        icon = wp_cache_get(str("mime_type_icon_") + str(mime))
    # end if
    post_id = 0
    if php_empty(lambda : icon):
        post_mimes = Array()
        if php_is_numeric(mime):
            mime = int(mime)
            post = get_post(mime)
            if post:
                post_id = int(post.ID)
                file = get_attached_file(post_id)
                ext = php_preg_replace("/^.+?\\.([^.]+)$/", "$1", file)
                if (not php_empty(lambda : ext)):
                    post_mimes[-1] = ext
                    ext_type = wp_ext2type(ext)
                    if ext_type:
                        post_mimes[-1] = ext_type
                    # end if
                # end if
                mime = post.post_mime_type
            else:
                mime = 0
            # end if
        else:
            post_mimes[-1] = mime
        # end if
        icon_files = wp_cache_get("icon_files")
        if (not php_is_array(icon_files)):
            #// 
            #// Filters the icon directory path.
            #// 
            #// @since 2.0.0
            #// 
            #// @param string $path Icon directory absolute path.
            #//
            icon_dir = apply_filters("icon_dir", ABSPATH + WPINC + "/images/media")
            #// 
            #// Filters the icon directory URI.
            #// 
            #// @since 2.0.0
            #// 
            #// @param string $uri Icon directory URI.
            #//
            icon_dir_uri = apply_filters("icon_dir_uri", includes_url("images/media"))
            #// 
            #// Filters the array of icon directory URIs.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string[] $uris Array of icon directory URIs keyed by directory absolute path.
            #//
            dirs = apply_filters("icon_dirs", Array({icon_dir: icon_dir_uri}))
            icon_files = Array()
            while True:
                
                if not (dirs):
                    break
                # end if
                keys = php_array_keys(dirs)
                dir = php_array_shift(keys)
                uri = php_array_shift(dirs)
                dh = php_opendir(dir)
                if dh:
                    while True:
                        file = php_readdir(dh)
                        if not (False != file):
                            break
                        # end if
                        file = wp_basename(file)
                        if php_substr(file, 0, 1) == ".":
                            continue
                        # end if
                        if (not php_in_array(php_strtolower(php_substr(file, -4)), Array(".png", ".gif", ".jpg"))):
                            if php_is_dir(str(dir) + str("/") + str(file)):
                                dirs[str(dir) + str("/") + str(file)] = str(uri) + str("/") + str(file)
                            # end if
                            continue
                        # end if
                        icon_files[str(dir) + str("/") + str(file)] = str(uri) + str("/") + str(file)
                    # end while
                    php_closedir(dh)
                # end if
            # end while
            wp_cache_add("icon_files", icon_files, "default", 600)
        # end if
        types = Array()
        #// Icon wp_basename - extension = MIME wildcard.
        for file,uri in icon_files:
            types[php_preg_replace("/^([^.]*).*$/", "$1", wp_basename(file))] = icon_files[file]
        # end for
        if (not php_empty(lambda : mime)):
            post_mimes[-1] = php_substr(mime, 0, php_strpos(mime, "/"))
            post_mimes[-1] = php_substr(mime, php_strpos(mime, "/") + 1)
            post_mimes[-1] = php_str_replace("/", "_", mime)
        # end if
        matches = wp_match_mime_types(php_array_keys(types), post_mimes)
        matches["default"] = Array("default")
        for match,wilds in matches:
            for wild in wilds:
                if (not (php_isset(lambda : types[wild]))):
                    continue
                # end if
                icon = types[wild]
                if (not php_is_numeric(mime)):
                    wp_cache_add(str("mime_type_icon_") + str(mime), icon)
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
    return apply_filters("wp_mime_type_icon", icon, mime, post_id)
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
def wp_check_for_changed_slugs(post_id=None, post=None, post_before=None, *args_):
    
    #// Don't bother if it hasn't changed.
    if post.post_name == post_before.post_name:
        return
    # end if
    #// We're only concerned with published, non-hierarchical objects.
    if (not "publish" == post.post_status or "attachment" == get_post_type(post) and "inherit" == post.post_status) or is_post_type_hierarchical(post.post_type):
        return
    # end if
    old_slugs = get_post_meta(post_id, "_wp_old_slug")
    #// If we haven't added this old slug before, add it now.
    if (not php_empty(lambda : post_before.post_name)) and (not php_in_array(post_before.post_name, old_slugs)):
        add_post_meta(post_id, "_wp_old_slug", post_before.post_name)
    # end if
    #// If the new slug was used previously, delete it from the list.
    if php_in_array(post.post_name, old_slugs):
        delete_post_meta(post_id, "_wp_old_slug", post.post_name)
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
def wp_check_for_changed_dates(post_id=None, post=None, post_before=None, *args_):
    
    previous_date = gmdate("Y-m-d", strtotime(post_before.post_date))
    new_date = gmdate("Y-m-d", strtotime(post.post_date))
    #// Don't bother if it hasn't changed.
    if new_date == previous_date:
        return
    # end if
    #// We're only concerned with published, non-hierarchical objects.
    if (not "publish" == post.post_status or "attachment" == get_post_type(post) and "inherit" == post.post_status) or is_post_type_hierarchical(post.post_type):
        return
    # end if
    old_dates = get_post_meta(post_id, "_wp_old_date")
    #// If we haven't added this old date before, add it now.
    if (not php_empty(lambda : previous_date)) and (not php_in_array(previous_date, old_dates)):
        add_post_meta(post_id, "_wp_old_date", previous_date)
    # end if
    #// If the new slug was used previously, delete it from the list.
    if php_in_array(new_date, old_dates):
        delete_post_meta(post_id, "_wp_old_date", new_date)
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
def get_private_posts_cap_sql(post_type=None, *args_):
    
    return get_posts_by_author_sql(post_type, False)
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
def get_posts_by_author_sql(post_type=None, full=True, post_author=None, public_only=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_is_array(post_type):
        post_types = post_type
    else:
        post_types = Array(post_type)
    # end if
    post_type_clauses = Array()
    for post_type in post_types:
        post_type_obj = get_post_type_object(post_type)
        if (not post_type_obj):
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
        cap = apply_filters_deprecated("pub_priv_sql_capability", Array(""), "3.2.0")
        if (not cap):
            cap = current_user_can(post_type_obj.cap.read_private_posts)
        # end if
        #// Only need to check the cap if $public_only is false.
        post_status_sql = "post_status = 'publish'"
        if False == public_only:
            if cap:
                #// Does the user have the capability to view private posts? Guess so.
                post_status_sql += " OR post_status = 'private'"
            elif is_user_logged_in():
                #// Users can view their own private posts.
                id = get_current_user_id()
                if None == post_author or (not full):
                    post_status_sql += str(" OR post_status = 'private' AND post_author = ") + str(id)
                elif id == int(post_author):
                    post_status_sql += " OR post_status = 'private'"
                # end if
                pass
            # end if
            pass
        # end if
        post_type_clauses[-1] = "( post_type = '" + post_type + str("' AND ( ") + str(post_status_sql) + str(" ) )")
    # end for
    if php_empty(lambda : post_type_clauses):
        return "WHERE 1 = 0" if full else "1 = 0"
    # end if
    sql = "( " + php_implode(" OR ", post_type_clauses) + " )"
    if None != post_author:
        sql += wpdb.prepare(" AND post_author = %d", post_author)
    # end if
    if full:
        sql = "WHERE " + sql
    # end if
    return sql
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
def get_lastpostdate(timezone="server", post_type="any", *args_):
    
    #// 
    #// Filters the most recent time that a post on the site was published.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string|false $date     Date the last post was published. False on failure.
    #// @param string       $timezone Location to use for getting the post published date.
    #// See get_lastpostdate() for accepted `$timezone` values.
    #//
    return apply_filters("get_lastpostdate", _get_last_post_time(timezone, "date", post_type), timezone)
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
def get_lastpostmodified(timezone="server", post_type="any", *args_):
    
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
    lastpostmodified = apply_filters("pre_get_lastpostmodified", False, timezone, post_type)
    if False != lastpostmodified:
        return lastpostmodified
    # end if
    lastpostmodified = _get_last_post_time(timezone, "modified", post_type)
    lastpostdate = get_lastpostdate(timezone)
    if lastpostdate > lastpostmodified:
        lastpostmodified = lastpostdate
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
    return apply_filters("get_lastpostmodified", lastpostmodified, timezone)
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
def _get_last_post_time(timezone=None, field=None, post_type="any", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not php_in_array(field, Array("date", "modified"))):
        return False
    # end if
    timezone = php_strtolower(timezone)
    key = str("lastpost") + str(field) + str(":") + str(timezone)
    if "any" != post_type:
        key += ":" + sanitize_key(post_type)
    # end if
    date = wp_cache_get(key, "timeinfo")
    if False != date:
        return date
    # end if
    if "any" == post_type:
        post_types = get_post_types(Array({"public": True}))
        array_walk(post_types, Array(wpdb, "escape_by_ref"))
        post_types = "'" + php_implode("', '", post_types) + "'"
    else:
        post_types = "'" + sanitize_key(post_type) + "'"
    # end if
    for case in Switch(timezone):
        if case("gmt"):
            date = wpdb.get_var(str("SELECT post_") + str(field) + str("_gmt FROM ") + str(wpdb.posts) + str(" WHERE post_status = 'publish' AND post_type IN (") + str(post_types) + str(") ORDER BY post_") + str(field) + str("_gmt DESC LIMIT 1"))
            break
        # end if
        if case("blog"):
            date = wpdb.get_var(str("SELECT post_") + str(field) + str(" FROM ") + str(wpdb.posts) + str(" WHERE post_status = 'publish' AND post_type IN (") + str(post_types) + str(") ORDER BY post_") + str(field) + str("_gmt DESC LIMIT 1"))
            break
        # end if
        if case("server"):
            add_seconds_server = gmdate("Z")
            date = wpdb.get_var(str("SELECT DATE_ADD(post_") + str(field) + str("_gmt, INTERVAL '") + str(add_seconds_server) + str("' SECOND) FROM ") + str(wpdb.posts) + str(" WHERE post_status = 'publish' AND post_type IN (") + str(post_types) + str(") ORDER BY post_") + str(field) + str("_gmt DESC LIMIT 1"))
            break
        # end if
    # end for
    if date:
        wp_cache_set(key, date, "timeinfo")
        return date
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
def update_post_cache(posts=None, *args_):
    
    if (not posts):
        return
    # end if
    for post in posts:
        wp_cache_add(post.ID, post, "posts")
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
def clean_post_cache(post=None, *args_):
    
    global _wp_suspend_cache_invalidation
    php_check_if_defined("_wp_suspend_cache_invalidation")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation)):
        return
    # end if
    post = get_post(post)
    if php_empty(lambda : post):
        return
    # end if
    wp_cache_delete(post.ID, "posts")
    wp_cache_delete(post.ID, "post_meta")
    clean_object_term_cache(post.ID, post.post_type)
    wp_cache_delete("wp_get_archives", "general")
    #// 
    #// Fires immediately after the given post's cache is cleaned.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int     $post_id Post ID.
    #// @param WP_Post $post    Post object.
    #//
    do_action("clean_post_cache", post.ID, post)
    if "page" == post.post_type:
        wp_cache_delete("all_page_ids", "posts")
        #// 
        #// Fires immediately after the given page's cache is cleaned.
        #// 
        #// @since 2.5.0
        #// 
        #// @param int $post_id Post ID.
        #//
        do_action("clean_page_cache", post.ID)
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
def update_post_caches(posts=None, post_type="post", update_term_cache=True, update_meta_cache=True, *args_):
    
    #// No point in doing all this work if we didn't match any posts.
    if (not posts):
        return
    # end if
    update_post_cache(posts)
    post_ids = Array()
    for post in posts:
        post_ids[-1] = post.ID
    # end for
    if (not post_type):
        post_type = "any"
    # end if
    if update_term_cache:
        if php_is_array(post_type):
            ptypes = post_type
        elif "any" == post_type:
            ptypes = Array()
            #// Just use the post_types in the supplied posts.
            for post in posts:
                ptypes[-1] = post.post_type
            # end for
            ptypes = array_unique(ptypes)
        else:
            ptypes = Array(post_type)
        # end if
        if (not php_empty(lambda : ptypes)):
            update_object_term_cache(post_ids, ptypes)
        # end if
    # end if
    if update_meta_cache:
        update_postmeta_cache(post_ids)
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
def update_postmeta_cache(post_ids=None, *args_):
    
    return update_meta_cache("post", post_ids)
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
def clean_attachment_cache(id=None, clean_terms=False, *args_):
    
    global _wp_suspend_cache_invalidation
    php_check_if_defined("_wp_suspend_cache_invalidation")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation)):
        return
    # end if
    id = int(id)
    wp_cache_delete(id, "posts")
    wp_cache_delete(id, "post_meta")
    if clean_terms:
        clean_object_term_cache(id, "attachment")
    # end if
    #// 
    #// Fires after the given attachment's cache is cleaned.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int $id Attachment ID.
    #//
    do_action("clean_attachment_cache", id)
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
def _transition_post_status(new_status=None, old_status=None, post=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if "publish" != old_status and "publish" == new_status:
        #// Reset GUID if transitioning to publish and it is empty.
        if "" == get_the_guid(post.ID):
            wpdb.update(wpdb.posts, Array({"guid": get_permalink(post.ID)}), Array({"ID": post.ID}))
        # end if
        #// 
        #// Fires when a post's status is transitioned from private to published.
        #// 
        #// @since 1.5.0
        #// @deprecated 2.3.0 Use {@see 'private_to_publish'} instead.
        #// 
        #// @param int $post_id Post ID.
        #//
        do_action_deprecated("private_to_published", Array(post.ID), "2.3.0", "private_to_publish")
    # end if
    #// If published posts changed clear the lastpostmodified cache.
    if "publish" == new_status or "publish" == old_status:
        for timezone in Array("server", "gmt", "blog"):
            wp_cache_delete(str("lastpostmodified:") + str(timezone), "timeinfo")
            wp_cache_delete(str("lastpostdate:") + str(timezone), "timeinfo")
            wp_cache_delete(str("lastpostdate:") + str(timezone) + str(":") + str(post.post_type), "timeinfo")
        # end for
    # end if
    if new_status != old_status:
        wp_cache_delete(_count_posts_cache_key(post.post_type), "counts")
        wp_cache_delete(_count_posts_cache_key(post.post_type, "readable"), "counts")
    # end if
    #// Always clears the hook in case the post status bounced from future to draft.
    wp_clear_scheduled_hook("publish_future_post", Array(post.ID))
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
def _future_post_hook(deprecated=None, post=None, *args_):
    
    wp_clear_scheduled_hook("publish_future_post", Array(post.ID))
    wp_schedule_single_event(strtotime(get_gmt_from_date(post.post_date) + " GMT"), "publish_future_post", Array(post.ID))
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
def _publish_post_hook(post_id=None, *args_):
    
    if php_defined("XMLRPC_REQUEST"):
        #// 
        #// Fires when _publish_post_hook() is called during an XML-RPC request.
        #// 
        #// @since 2.1.0
        #// 
        #// @param int $post_id Post ID.
        #//
        do_action("xmlrpc_publish_post", post_id)
    # end if
    if php_defined("WP_IMPORTING"):
        return
    # end if
    if get_option("default_pingback_flag"):
        add_post_meta(post_id, "_pingme", "1", True)
    # end if
    add_post_meta(post_id, "_encloseme", "1", True)
    to_ping = get_to_ping(post_id)
    if (not php_empty(lambda : to_ping)):
        add_post_meta(post_id, "_trackbackme", "1")
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
def wp_get_post_parent_id(post=None, *args_):
    
    post = get_post(post)
    if (not post) or is_wp_error(post):
        return False
    # end if
    return int(post.post_parent)
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
def wp_check_post_hierarchy_for_loops(post_parent=None, post_ID=None, *args_):
    
    #// Nothing fancy here - bail.
    if (not post_parent):
        return 0
    # end if
    #// New post can't cause a loop.
    if php_empty(lambda : post_ID):
        return post_parent
    # end if
    #// Can't be its own parent.
    if post_parent == post_ID:
        return 0
    # end if
    #// Now look for larger loops.
    loop = wp_find_hierarchy_loop("wp_get_post_parent_id", post_ID, post_parent)
    if (not loop):
        return post_parent
        pass
    # end if
    #// Setting $post_parent to the given value causes a loop.
    if (php_isset(lambda : loop[post_ID])):
        return 0
    # end if
    #// There's a loop, but it doesn't contain $post_ID. Break the loop.
    for loop_member in php_array_keys(loop):
        wp_update_post(Array({"ID": loop_member, "post_parent": 0}))
    # end for
    return post_parent
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
def set_post_thumbnail(post=None, thumbnail_id=None, *args_):
    
    post = get_post(post)
    thumbnail_id = absint(thumbnail_id)
    if post and thumbnail_id and get_post(thumbnail_id):
        if wp_get_attachment_image(thumbnail_id, "thumbnail"):
            return update_post_meta(post.ID, "_thumbnail_id", thumbnail_id)
        else:
            return delete_post_meta(post.ID, "_thumbnail_id")
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
def delete_post_thumbnail(post=None, *args_):
    
    post = get_post(post)
    if post:
        return delete_post_meta(post.ID, "_thumbnail_id")
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
def wp_delete_auto_drafts(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Cleanup old auto-drafts more than 7 days old.
    old_posts = wpdb.get_col(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_status = 'auto-draft' AND DATE_SUB( NOW(), INTERVAL 7 DAY ) > post_date"))
    for delete in old_posts:
        #// Force delete.
        wp_delete_post(delete, True)
    # end for
# end def wp_delete_auto_drafts
#// 
#// Queues posts for lazy-loading of term meta.
#// 
#// @since 4.5.0
#// 
#// @param array $posts Array of WP_Post objects.
#//
def wp_queue_posts_for_term_meta_lazyload(posts=None, *args_):
    
    post_type_taxonomies = Array()
    term_ids = Array()
    for post in posts:
        if (not type(post).__name__ == "WP_Post"):
            continue
        # end if
        if (not (php_isset(lambda : post_type_taxonomies[post.post_type]))):
            post_type_taxonomies[post.post_type] = get_object_taxonomies(post.post_type)
        # end if
        for taxonomy in post_type_taxonomies[post.post_type]:
            #// Term cache should already be primed by `update_post_term_cache()`.
            terms = get_object_term_cache(post.ID, taxonomy)
            if False != terms:
                for term in terms:
                    if (not (php_isset(lambda : term_ids[term.term_id]))):
                        term_ids[-1] = term.term_id
                    # end if
                # end for
            # end if
        # end for
    # end for
    if term_ids:
        lazyloader = wp_metadata_lazyloader()
        lazyloader.queue_objects("term", term_ids)
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
def _update_term_count_on_transition_post_status(new_status=None, old_status=None, post=None, *args_):
    
    #// Update counts for the post's terms.
    for taxonomy in get_object_taxonomies(post.post_type):
        tt_ids = wp_get_object_terms(post.ID, taxonomy, Array({"fields": "tt_ids"}))
        wp_update_term_count(tt_ids, taxonomy)
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
def _prime_post_caches(ids=None, update_term_cache=True, update_meta_cache=True, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    non_cached_ids = _get_non_cached_ids(ids, "posts")
    if (not php_empty(lambda : non_cached_ids)):
        fresh_posts = wpdb.get_results(php_sprintf(str("SELECT ") + str(wpdb.posts) + str(".* FROM ") + str(wpdb.posts) + str(" WHERE ID IN (%s)"), join(",", non_cached_ids)))
        update_post_caches(fresh_posts, "any", update_term_cache, update_meta_cache)
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
def wp_add_trashed_suffix_to_post_name_for_trashed_posts(post_name=None, post_ID=0, *args_):
    
    trashed_posts_with_desired_slug = get_posts(Array({"name": post_name, "post_status": "trash", "post_type": "any", "nopaging": True, "post__not_in": Array(post_ID)}))
    if (not php_empty(lambda : trashed_posts_with_desired_slug)):
        for _post in trashed_posts_with_desired_slug:
            wp_add_trashed_suffix_to_post_name_for_post(_post)
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
def wp_add_trashed_suffix_to_post_name_for_post(post=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post = get_post(post)
    if "__trashed" == php_substr(post.post_name, -9):
        return post.post_name
    # end if
    add_post_meta(post.ID, "_wp_desired_post_slug", post.post_name)
    post_name = _truncate_post_slug(post.post_name, 191) + "__trashed"
    wpdb.update(wpdb.posts, Array({"post_name": post_name}), Array({"ID": post.ID}))
    clean_post_cache(post.ID)
    return post_name
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
def _filter_query_attachment_filenames(clauses=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    remove_filter("posts_clauses", __FUNCTION__)
    #// Add a LEFT JOIN of the postmeta table so we don't trample existing JOINs.
    clauses["join"] += str(" LEFT JOIN ") + str(wpdb.postmeta) + str(" AS sq1 ON ( ") + str(wpdb.posts) + str(".ID = sq1.post_id AND sq1.meta_key = '_wp_attached_file' )")
    clauses["groupby"] = str(wpdb.posts) + str(".ID")
    clauses["where"] = php_preg_replace(str("/\\(") + str(wpdb.posts) + str(".post_content (NOT LIKE|LIKE) (\\'[^']+\\')\\)/"), "$0 OR ( sq1.meta_value $1 $2 )", clauses["where"])
    return clauses
# end def _filter_query_attachment_filenames
#// 
#// Sets the last changed time for the 'posts' cache group.
#// 
#// @since 5.0.0
#//
def wp_cache_set_posts_last_changed(*args_):
    
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
def get_available_post_mime_types(type="attachment", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    types = wpdb.get_col(wpdb.prepare(str("SELECT DISTINCT post_mime_type FROM ") + str(wpdb.posts) + str(" WHERE post_type = %s"), type))
    return types
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
def wp_get_original_image_path(attachment_id=None, unfiltered=False, *args_):
    
    if (not wp_attachment_is_image(attachment_id)):
        return False
    # end if
    image_meta = wp_get_attachment_metadata(attachment_id)
    image_file = get_attached_file(attachment_id, unfiltered)
    if php_empty(lambda : image_meta["original_image"]):
        original_image = image_file
    else:
        original_image = path_join(php_dirname(image_file), image_meta["original_image"])
    # end if
    #// 
    #// Filters the path to the original image.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $original_image Path to original image file.
    #// @param int    $attachment_id  Attachment ID.
    #//
    return apply_filters("wp_get_original_image_path", original_image, attachment_id)
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
def wp_get_original_image_url(attachment_id=None, *args_):
    
    if (not wp_attachment_is_image(attachment_id)):
        return False
    # end if
    image_url = wp_get_attachment_url(attachment_id)
    if php_empty(lambda : image_url):
        return False
    # end if
    image_meta = wp_get_attachment_metadata(attachment_id)
    if php_empty(lambda : image_meta["original_image"]):
        original_image_url = image_url
    else:
        original_image_url = path_join(php_dirname(image_url), image_meta["original_image"])
    # end if
    #// 
    #// Filters the URL to the original attachment image.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $original_image_url URL to original image.
    #// @param int    $attachment_id      Attachment ID.
    #//
    return apply_filters("wp_get_original_image_url", original_image_url, attachment_id)
# end def wp_get_original_image_url
