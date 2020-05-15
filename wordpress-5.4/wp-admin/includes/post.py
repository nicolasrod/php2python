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
#// WordPress Post Administration API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Rename $_POST data from form names to DB post columns.
#// 
#// Manipulates $_POST directly.
#// 
#// @since 2.6.0
#// 
#// @param bool $update Are we updating a pre-existing post?
#// @param array $post_data Array of post data. Defaults to the contents of $_POST.
#// @return array|WP_Error Array of post data on success, WP_Error on failure.
#//
def _wp_translate_postdata(update=False, post_data=None, *args_):
    
    if php_empty(lambda : post_data):
        post_data = PHP_POST
    # end if
    if update:
        post_data["ID"] = int(post_data["post_ID"])
    # end if
    ptype = get_post_type_object(post_data["post_type"])
    if update and (not current_user_can("edit_post", post_data["ID"])):
        if "page" == post_data["post_type"]:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to edit pages as this user.")))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to edit posts as this user.")))
        # end if
    elif (not update) and (not current_user_can(ptype.cap.create_posts)):
        if "page" == post_data["post_type"]:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to create pages as this user.")))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to create posts as this user.")))
        # end if
    # end if
    if (php_isset(lambda : post_data["content"])):
        post_data["post_content"] = post_data["content"]
    # end if
    if (php_isset(lambda : post_data["excerpt"])):
        post_data["post_excerpt"] = post_data["excerpt"]
    # end if
    if (php_isset(lambda : post_data["parent_id"])):
        post_data["post_parent"] = int(post_data["parent_id"])
    # end if
    if (php_isset(lambda : post_data["trackback_url"])):
        post_data["to_ping"] = post_data["trackback_url"]
    # end if
    post_data["user_ID"] = get_current_user_id()
    if (not php_empty(lambda : post_data["post_author_override"])):
        post_data["post_author"] = int(post_data["post_author_override"])
    else:
        if (not php_empty(lambda : post_data["post_author"])):
            post_data["post_author"] = int(post_data["post_author"])
        else:
            post_data["post_author"] = int(post_data["user_ID"])
        # end if
    # end if
    if (php_isset(lambda : post_data["user_ID"])) and post_data["post_author"] != post_data["user_ID"] and (not current_user_can(ptype.cap.edit_others_posts)):
        if update:
            if "page" == post_data["post_type"]:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to edit pages as this user.")))
            else:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to edit posts as this user.")))
            # end if
        else:
            if "page" == post_data["post_type"]:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to create pages as this user.")))
            else:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to create posts as this user.")))
            # end if
        # end if
    # end if
    if (not php_empty(lambda : post_data["post_status"])):
        post_data["post_status"] = sanitize_key(post_data["post_status"])
        #// No longer an auto-draft.
        if "auto-draft" == post_data["post_status"]:
            post_data["post_status"] = "draft"
        # end if
        if (not get_post_status_object(post_data["post_status"])):
            post_data["post_status"] = None
        # end if
    # end if
    #// What to do based on which button they pressed.
    if (php_isset(lambda : post_data["saveasdraft"])) and "" != post_data["saveasdraft"]:
        post_data["post_status"] = "draft"
    # end if
    if (php_isset(lambda : post_data["saveasprivate"])) and "" != post_data["saveasprivate"]:
        post_data["post_status"] = "private"
    # end if
    if (php_isset(lambda : post_data["publish"])) and "" != post_data["publish"] and (not (php_isset(lambda : post_data["post_status"]))) or "private" != post_data["post_status"]:
        post_data["post_status"] = "publish"
    # end if
    if (php_isset(lambda : post_data["advanced"])) and "" != post_data["advanced"]:
        post_data["post_status"] = "draft"
    # end if
    if (php_isset(lambda : post_data["pending"])) and "" != post_data["pending"]:
        post_data["post_status"] = "pending"
    # end if
    if (php_isset(lambda : post_data["ID"])):
        post_id = post_data["ID"]
    else:
        post_id = False
    # end if
    previous_status = get_post_field("post_status", post_id) if post_id else False
    if (php_isset(lambda : post_data["post_status"])) and "private" == post_data["post_status"] and (not current_user_can(ptype.cap.publish_posts)):
        post_data["post_status"] = previous_status if previous_status else "pending"
    # end if
    published_statuses = Array("publish", "future")
    #// Posts 'submitted for approval' are submitted to $_POST the same as if they were being published.
    #// Change status from 'publish' to 'pending' if user lacks permissions to publish or to resave published posts.
    if (php_isset(lambda : post_data["post_status"])) and php_in_array(post_data["post_status"], published_statuses) and (not current_user_can(ptype.cap.publish_posts)):
        if (not php_in_array(previous_status, published_statuses)) or (not current_user_can("edit_post", post_id)):
            post_data["post_status"] = "pending"
        # end if
    # end if
    if (not (php_isset(lambda : post_data["post_status"]))):
        post_data["post_status"] = "draft" if "auto-draft" == previous_status else previous_status
    # end if
    if (php_isset(lambda : post_data["post_password"])) and (not current_user_can(ptype.cap.publish_posts)):
        post_data["post_password"] = None
    # end if
    if (not (php_isset(lambda : post_data["comment_status"]))):
        post_data["comment_status"] = "closed"
    # end if
    if (not (php_isset(lambda : post_data["ping_status"]))):
        post_data["ping_status"] = "closed"
    # end if
    for timeunit in Array("aa", "mm", "jj", "hh", "mn"):
        if (not php_empty(lambda : post_data["hidden_" + timeunit])) and post_data["hidden_" + timeunit] != post_data[timeunit]:
            post_data["edit_date"] = "1"
            break
        # end if
    # end for
    if (not php_empty(lambda : post_data["edit_date"])):
        aa = post_data["aa"]
        mm = post_data["mm"]
        jj = post_data["jj"]
        hh = post_data["hh"]
        mn = post_data["mn"]
        ss = post_data["ss"]
        aa = gmdate("Y") if aa <= 0 else aa
        mm = gmdate("n") if mm <= 0 else mm
        jj = 31 if jj > 31 else jj
        jj = gmdate("j") if jj <= 0 else jj
        hh = hh - 24 if hh > 23 else hh
        mn = mn - 60 if mn > 59 else mn
        ss = ss - 60 if ss > 59 else ss
        post_data["post_date"] = php_sprintf("%04d-%02d-%02d %02d:%02d:%02d", aa, mm, jj, hh, mn, ss)
        valid_date = wp_checkdate(mm, jj, aa, post_data["post_date"])
        if (not valid_date):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_date", __("Invalid date.")))
        # end if
        post_data["post_date_gmt"] = get_gmt_from_date(post_data["post_date"])
    # end if
    if (php_isset(lambda : post_data["post_category"])):
        category_object = get_taxonomy("category")
        if (not current_user_can(category_object.cap.assign_terms)):
            post_data["post_category"] = None
        # end if
    # end if
    return post_data
# end def _wp_translate_postdata
#// 
#// Returns only allowed post data fields
#// 
#// @since 5.0.1
#// 
#// @param array $post_data Array of post data. Defaults to the contents of $_POST.
#// @return array|WP_Error Array of post data on success, WP_Error on failure.
#//
def _wp_get_allowed_postdata(post_data=None, *args_):
    
    if php_empty(lambda : post_data):
        post_data = PHP_POST
    # end if
    #// Pass through errors.
    if is_wp_error(post_data):
        return post_data
    # end if
    return php_array_diff_key(post_data, php_array_flip(Array("meta_input", "file", "guid")))
# end def _wp_get_allowed_postdata
#// 
#// Update an existing post with values provided in $_POST.
#// 
#// @since 1.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $post_data Optional.
#// @return int Post ID.
#//
def edit_post(post_data=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : post_data):
        post_data = PHP_POST
    # end if
    post_data["filter"] = None
    post_ID = int(post_data["post_ID"])
    post = get_post(post_ID)
    post_data["post_type"] = post.post_type
    post_data["post_mime_type"] = post.post_mime_type
    if (not php_empty(lambda : post_data["post_status"])):
        post_data["post_status"] = sanitize_key(post_data["post_status"])
        if "inherit" == post_data["post_status"]:
            post_data["post_status"] = None
        # end if
    # end if
    ptype = get_post_type_object(post_data["post_type"])
    if (not current_user_can("edit_post", post_ID)):
        if "page" == post_data["post_type"]:
            wp_die(__("Sorry, you are not allowed to edit this page."))
        else:
            wp_die(__("Sorry, you are not allowed to edit this post."))
        # end if
    # end if
    if post_type_supports(ptype.name, "revisions"):
        revisions = wp_get_post_revisions(post_ID, Array({"order": "ASC", "posts_per_page": 1}))
        revision = current(revisions)
        #// Check if the revisions have been upgraded.
        if revisions and _wp_get_post_revision_version(revision) < 1:
            _wp_upgrade_revisions_of_post(post, wp_get_post_revisions(post_ID))
        # end if
    # end if
    if (php_isset(lambda : post_data["visibility"])):
        for case in Switch(post_data["visibility"]):
            if case("public"):
                post_data["post_password"] = ""
                break
            # end if
            if case("password"):
                post_data["sticky"] = None
                break
            # end if
            if case("private"):
                post_data["post_status"] = "private"
                post_data["post_password"] = ""
                post_data["sticky"] = None
                break
            # end if
        # end for
    # end if
    post_data = _wp_translate_postdata(True, post_data)
    if is_wp_error(post_data):
        wp_die(post_data.get_error_message())
    # end if
    translated = _wp_get_allowed_postdata(post_data)
    #// Post formats.
    if (php_isset(lambda : post_data["post_format"])):
        set_post_format(post_ID, post_data["post_format"])
    # end if
    format_meta_urls = Array("url", "link_url", "quote_source_url")
    for format_meta_url in format_meta_urls:
        keyed = "_format_" + format_meta_url
        if (php_isset(lambda : post_data[keyed])):
            update_post_meta(post_ID, keyed, wp_slash(esc_url_raw(wp_unslash(post_data[keyed]))))
        # end if
    # end for
    format_keys = Array("quote", "quote_source_name", "image", "gallery", "audio_embed", "video_embed")
    for key in format_keys:
        keyed = "_format_" + key
        if (php_isset(lambda : post_data[keyed])):
            if current_user_can("unfiltered_html"):
                update_post_meta(post_ID, keyed, post_data[keyed])
            else:
                update_post_meta(post_ID, keyed, wp_filter_post_kses(post_data[keyed]))
            # end if
        # end if
    # end for
    if "attachment" == post_data["post_type"] and php_preg_match("#^(audio|video)/#", post_data["post_mime_type"]):
        id3data = wp_get_attachment_metadata(post_ID)
        if (not php_is_array(id3data)):
            id3data = Array()
        # end if
        for key,label in wp_get_attachment_id3_keys(post, "edit"):
            if (php_isset(lambda : post_data["id3_" + key])):
                id3data[key] = sanitize_text_field(wp_unslash(post_data["id3_" + key]))
            # end if
        # end for
        wp_update_attachment_metadata(post_ID, id3data)
    # end if
    #// Meta stuff.
    if (php_isset(lambda : post_data["meta"])) and post_data["meta"]:
        for key,value in post_data["meta"]:
            meta = get_post_meta_by_id(key)
            if (not meta):
                continue
            # end if
            if meta.post_id != post_ID:
                continue
            # end if
            if is_protected_meta(meta.meta_key, "post") or (not current_user_can("edit_post_meta", post_ID, meta.meta_key)):
                continue
            # end if
            if is_protected_meta(value["key"], "post") or (not current_user_can("edit_post_meta", post_ID, value["key"])):
                continue
            # end if
            update_meta(key, value["key"], value["value"])
        # end for
    # end if
    if (php_isset(lambda : post_data["deletemeta"])) and post_data["deletemeta"]:
        for key,value in post_data["deletemeta"]:
            meta = get_post_meta_by_id(key)
            if (not meta):
                continue
            # end if
            if meta.post_id != post_ID:
                continue
            # end if
            if is_protected_meta(meta.meta_key, "post") or (not current_user_can("delete_post_meta", post_ID, meta.meta_key)):
                continue
            # end if
            delete_meta(key)
        # end for
    # end if
    #// Attachment stuff.
    if "attachment" == post_data["post_type"]:
        if (php_isset(lambda : post_data["_wp_attachment_image_alt"])):
            image_alt = wp_unslash(post_data["_wp_attachment_image_alt"])
            if get_post_meta(post_ID, "_wp_attachment_image_alt", True) != image_alt:
                image_alt = wp_strip_all_tags(image_alt, True)
                #// update_post_meta() expects slashed.
                update_post_meta(post_ID, "_wp_attachment_image_alt", wp_slash(image_alt))
            # end if
        # end if
        attachment_data = post_data["attachments"][post_ID] if (php_isset(lambda : post_data["attachments"][post_ID])) else Array()
        #// This filter is documented in wp-admin/includes/media.php
        translated = apply_filters("attachment_fields_to_save", translated, attachment_data)
    # end if
    #// Convert taxonomy input to term IDs, to avoid ambiguity.
    if (php_isset(lambda : post_data["tax_input"])):
        for taxonomy,terms in post_data["tax_input"]:
            tax_object = get_taxonomy(taxonomy)
            if tax_object and (php_isset(lambda : tax_object.meta_box_sanitize_cb)):
                translated["tax_input"][taxonomy] = call_user_func_array(tax_object.meta_box_sanitize_cb, Array(taxonomy, terms))
            # end if
        # end for
    # end if
    add_meta(post_ID)
    update_post_meta(post_ID, "_edit_last", get_current_user_id())
    success = wp_update_post(translated)
    #// If the save failed, see if we can sanity check the main fields and try again.
    if (not success) and php_is_callable(Array(wpdb, "strip_invalid_text_for_column")):
        fields = Array("post_title", "post_content", "post_excerpt")
        for field in fields:
            if (php_isset(lambda : translated[field])):
                translated[field] = wpdb.strip_invalid_text_for_column(wpdb.posts, field, translated[field])
            # end if
        # end for
        wp_update_post(translated)
    # end if
    #// Now that we have an ID we can fix any attachment anchor hrefs.
    _fix_attachment_links(post_ID)
    wp_set_post_lock(post_ID)
    if current_user_can(ptype.cap.edit_others_posts) and current_user_can(ptype.cap.publish_posts):
        if (not php_empty(lambda : post_data["sticky"])):
            stick_post(post_ID)
        else:
            unstick_post(post_ID)
        # end if
    # end if
    return post_ID
# end def edit_post
#// 
#// Process the post data for the bulk editing of posts.
#// 
#// Updates all bulk edited posts/pages, adding (but not removing) tags and
#// categories. Skips pages when they would be their own parent or child.
#// 
#// @since 2.7.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $post_data Optional, the array of post data to process if not provided will use $_POST superglobal.
#// @return array
#//
def bulk_edit_posts(post_data=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_empty(lambda : post_data):
        post_data = PHP_POST
    # end if
    if (php_isset(lambda : post_data["post_type"])):
        ptype = get_post_type_object(post_data["post_type"])
    else:
        ptype = get_post_type_object("post")
    # end if
    if (not current_user_can(ptype.cap.edit_posts)):
        if "page" == ptype.name:
            wp_die(__("Sorry, you are not allowed to edit pages."))
        else:
            wp_die(__("Sorry, you are not allowed to edit posts."))
        # end if
    # end if
    if -1 == post_data["_status"]:
        post_data["post_status"] = None
        post_data["post_status"] = None
    else:
        post_data["post_status"] = post_data["_status"]
    # end if
    post_data["_status"] = None
    if (not php_empty(lambda : post_data["post_status"])):
        post_data["post_status"] = sanitize_key(post_data["post_status"])
        if "inherit" == post_data["post_status"]:
            post_data["post_status"] = None
        # end if
    # end if
    post_IDs = php_array_map("intval", post_data["post"])
    reset = Array("post_author", "post_status", "post_password", "post_parent", "page_template", "comment_status", "ping_status", "keep_private", "tax_input", "post_category", "sticky", "post_format")
    for field in reset:
        if (php_isset(lambda : post_data[field])) and "" == post_data[field] or -1 == post_data[field]:
            post_data[field] = None
        # end if
    # end for
    if (php_isset(lambda : post_data["post_category"])):
        if php_is_array(post_data["post_category"]) and (not php_empty(lambda : post_data["post_category"])):
            new_cats = php_array_map("absint", post_data["post_category"])
        else:
            post_data["post_category"] = None
        # end if
    # end if
    tax_input = Array()
    if (php_isset(lambda : post_data["tax_input"])):
        for tax_name,terms in post_data["tax_input"]:
            if php_empty(lambda : terms):
                continue
            # end if
            if is_taxonomy_hierarchical(tax_name):
                tax_input[tax_name] = php_array_map("absint", terms)
            else:
                comma = _x(",", "tag delimiter")
                if "," != comma:
                    terms = php_str_replace(comma, ",", terms)
                # end if
                tax_input[tax_name] = php_explode(",", php_trim(terms, " \n \r ,"))
            # end if
        # end for
    # end if
    if (php_isset(lambda : post_data["post_parent"])) and int(post_data["post_parent"]):
        parent = int(post_data["post_parent"])
        pages = wpdb.get_results(str("SELECT ID, post_parent FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'page'"))
        children = Array()
        i = 0
        while i < 50 and parent > 0:
            
            children[-1] = parent
            for page in pages:
                if page.ID == parent:
                    parent = page.post_parent
                    break
                # end if
            # end for
            i += 1
        # end while
    # end if
    updated = Array()
    skipped = Array()
    locked = Array()
    shared_post_data = post_data
    for post_ID in post_IDs:
        #// Start with fresh post data with each iteration.
        post_data = shared_post_data
        post_type_object = get_post_type_object(get_post_type(post_ID))
        if (not (php_isset(lambda : post_type_object))) or (php_isset(lambda : children)) and php_in_array(post_ID, children) or (not current_user_can("edit_post", post_ID)):
            skipped[-1] = post_ID
            continue
        # end if
        if wp_check_post_lock(post_ID):
            locked[-1] = post_ID
            continue
        # end if
        post = get_post(post_ID)
        tax_names = get_object_taxonomies(post)
        for tax_name in tax_names:
            taxonomy_obj = get_taxonomy(tax_name)
            if (php_isset(lambda : tax_input[tax_name])) and current_user_can(taxonomy_obj.cap.assign_terms):
                new_terms = tax_input[tax_name]
            else:
                new_terms = Array()
            # end if
            if taxonomy_obj.hierarchical:
                current_terms = wp_get_object_terms(post_ID, tax_name, Array({"fields": "ids"}))
            else:
                current_terms = wp_get_object_terms(post_ID, tax_name, Array({"fields": "names"}))
            # end if
            post_data["tax_input"][tax_name] = php_array_merge(current_terms, new_terms)
        # end for
        if (php_isset(lambda : new_cats)) and php_in_array("category", tax_names):
            cats = wp_get_post_categories(post_ID)
            post_data["post_category"] = array_unique(php_array_merge(cats, new_cats))
            post_data["tax_input"]["category"] = None
        # end if
        post_data["post_ID"] = post_ID
        post_data["post_type"] = post.post_type
        post_data["post_mime_type"] = post.post_mime_type
        for field in Array("comment_status", "ping_status", "post_author"):
            if (not (php_isset(lambda : post_data[field]))):
                post_data[field] = post.field
            # end if
        # end for
        post_data = _wp_translate_postdata(True, post_data)
        if is_wp_error(post_data):
            skipped[-1] = post_ID
            continue
        # end if
        post_data = _wp_get_allowed_postdata(post_data)
        if (php_isset(lambda : shared_post_data["post_format"])):
            set_post_format(post_ID, shared_post_data["post_format"])
        # end if
        post_data["tax_input"]["post_format"] = None
        updated[-1] = wp_update_post(post_data)
        if (php_isset(lambda : post_data["sticky"])) and current_user_can(ptype.cap.edit_others_posts):
            if "sticky" == post_data["sticky"]:
                stick_post(post_ID)
            else:
                unstick_post(post_ID)
            # end if
        # end if
    # end for
    return Array({"updated": updated, "skipped": skipped, "locked": locked})
# end def bulk_edit_posts
#// 
#// Default post information to use when populating the "Write Post" form.
#// 
#// @since 2.0.0
#// 
#// @param string $post_type    Optional. A post type string. Default 'post'.
#// @param bool   $create_in_db Optional. Whether to insert the post into database. Default false.
#// @return WP_Post Post object containing all the default post data as attributes
#//
def get_default_post_to_edit(post_type="post", create_in_db=False, *args_):
    
    post_title = ""
    if (not php_empty(lambda : PHP_REQUEST["post_title"])):
        post_title = esc_html(wp_unslash(PHP_REQUEST["post_title"]))
    # end if
    post_content = ""
    if (not php_empty(lambda : PHP_REQUEST["content"])):
        post_content = esc_html(wp_unslash(PHP_REQUEST["content"]))
    # end if
    post_excerpt = ""
    if (not php_empty(lambda : PHP_REQUEST["excerpt"])):
        post_excerpt = esc_html(wp_unslash(PHP_REQUEST["excerpt"]))
    # end if
    if create_in_db:
        post_id = wp_insert_post(Array({"post_title": __("Auto Draft"), "post_type": post_type, "post_status": "auto-draft"}))
        post = get_post(post_id)
        if current_theme_supports("post-formats") and post_type_supports(post.post_type, "post-formats") and get_option("default_post_format"):
            set_post_format(post, get_option("default_post_format"))
        # end if
        #// Schedule auto-draft cleanup.
        if (not wp_next_scheduled("wp_scheduled_auto_draft_delete")):
            wp_schedule_event(time(), "daily", "wp_scheduled_auto_draft_delete")
        # end if
    else:
        post = php_new_class("stdClass", lambda : stdClass())
        post.ID = 0
        post.post_author = ""
        post.post_date = ""
        post.post_date_gmt = ""
        post.post_password = ""
        post.post_name = ""
        post.post_type = post_type
        post.post_status = "draft"
        post.to_ping = ""
        post.pinged = ""
        post.comment_status = get_default_comment_status(post_type)
        post.ping_status = get_default_comment_status(post_type, "pingback")
        post.post_pingback = get_option("default_pingback_flag")
        post.post_category = get_option("default_category")
        post.page_template = "default"
        post.post_parent = 0
        post.menu_order = 0
        post = php_new_class("WP_Post", lambda : WP_Post(post))
    # end if
    #// 
    #// Filters the default post content initially used in the "Write Post" form.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $post_content Default post content.
    #// @param WP_Post $post         Post object.
    #//
    post.post_content = str(apply_filters("default_content", post_content, post))
    #// 
    #// Filters the default post title initially used in the "Write Post" form.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $post_title Default post title.
    #// @param WP_Post $post       Post object.
    #//
    post.post_title = str(apply_filters("default_title", post_title, post))
    #// 
    #// Filters the default post excerpt initially used in the "Write Post" form.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $post_excerpt Default post excerpt.
    #// @param WP_Post $post         Post object.
    #//
    post.post_excerpt = str(apply_filters("default_excerpt", post_excerpt, post))
    return post
# end def get_default_post_to_edit
#// 
#// Determines if a post exists based on title, content, date and type.
#// 
#// @since 2.0.0
#// @since 5.2.0 Added the `$type` parameter.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $title   Post title.
#// @param string $content Optional post content.
#// @param string $date    Optional post date.
#// @param string $type    Optional post type.
#// @return int Post ID if post exists, 0 otherwise.
#//
def post_exists(title=None, content="", date="", type="", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post_title = wp_unslash(sanitize_post_field("post_title", title, 0, "db"))
    post_content = wp_unslash(sanitize_post_field("post_content", content, 0, "db"))
    post_date = wp_unslash(sanitize_post_field("post_date", date, 0, "db"))
    post_type = wp_unslash(sanitize_post_field("post_type", type, 0, "db"))
    query = str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE 1=1")
    args = Array()
    if (not php_empty(lambda : date)):
        query += " AND post_date = %s"
        args[-1] = post_date
    # end if
    if (not php_empty(lambda : title)):
        query += " AND post_title = %s"
        args[-1] = post_title
    # end if
    if (not php_empty(lambda : content)):
        query += " AND post_content = %s"
        args[-1] = post_content
    # end if
    if (not php_empty(lambda : type)):
        query += " AND post_type = %s"
        args[-1] = post_type
    # end if
    if (not php_empty(lambda : args)):
        return int(wpdb.get_var(wpdb.prepare(query, args)))
    # end if
    return 0
# end def post_exists
#// 
#// Creates a new post from the "Write Post" form using $_POST information.
#// 
#// @since 2.1.0
#// 
#// @global WP_User $current_user
#// 
#// @return int|WP_Error
#//
def wp_write_post(*args_):
    global PHP_POST
    if (php_isset(lambda : PHP_POST["post_type"])):
        ptype = get_post_type_object(PHP_POST["post_type"])
    else:
        ptype = get_post_type_object("post")
    # end if
    if (not current_user_can(ptype.cap.edit_posts)):
        if "page" == ptype.name:
            return php_new_class("WP_Error", lambda : WP_Error("edit_pages", __("Sorry, you are not allowed to create pages on this site.")))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("edit_posts", __("Sorry, you are not allowed to create posts or drafts on this site.")))
        # end if
    # end if
    PHP_POST["post_mime_type"] = ""
    PHP_POST["filter"] = None
    #// Edit, don't write, if we have a post ID.
    if (php_isset(lambda : PHP_POST["post_ID"])):
        return edit_post()
    # end if
    if (php_isset(lambda : PHP_POST["visibility"])):
        for case in Switch(PHP_POST["visibility"]):
            if case("public"):
                PHP_POST["post_password"] = ""
                break
            # end if
            if case("password"):
                PHP_POST["sticky"] = None
                break
            # end if
            if case("private"):
                PHP_POST["post_status"] = "private"
                PHP_POST["post_password"] = ""
                PHP_POST["sticky"] = None
                break
            # end if
        # end for
    # end if
    translated = _wp_translate_postdata(False)
    if is_wp_error(translated):
        return translated
    # end if
    translated = _wp_get_allowed_postdata(translated)
    #// Create the post.
    post_ID = wp_insert_post(translated)
    if is_wp_error(post_ID):
        return post_ID
    # end if
    if php_empty(lambda : post_ID):
        return 0
    # end if
    add_meta(post_ID)
    add_post_meta(post_ID, "_edit_last", PHP_GLOBALS["current_user"].ID)
    #// Now that we have an ID we can fix any attachment anchor hrefs.
    _fix_attachment_links(post_ID)
    wp_set_post_lock(post_ID)
    return post_ID
# end def wp_write_post
#// 
#// Calls wp_write_post() and handles the errors.
#// 
#// @since 2.0.0
#// 
#// @return int|null
#//
def write_post(*args_):
    
    result = wp_write_post()
    if is_wp_error(result):
        wp_die(result.get_error_message())
    else:
        return result
    # end if
# end def write_post
#// 
#// Post Meta.
#// 
#// 
#// Add post meta data defined in $_POST superglobal for post with given ID.
#// 
#// @since 1.2.0
#// 
#// @param int $post_ID
#// @return int|bool
#//
def add_meta(post_ID=None, *args_):
    
    post_ID = int(post_ID)
    metakeyselect = wp_unslash(php_trim(PHP_POST["metakeyselect"])) if (php_isset(lambda : PHP_POST["metakeyselect"])) else ""
    metakeyinput = wp_unslash(php_trim(PHP_POST["metakeyinput"])) if (php_isset(lambda : PHP_POST["metakeyinput"])) else ""
    metavalue = PHP_POST["metavalue"] if (php_isset(lambda : PHP_POST["metavalue"])) else ""
    if php_is_string(metavalue):
        metavalue = php_trim(metavalue)
    # end if
    if "#NONE#" != metakeyselect and (not php_empty(lambda : metakeyselect)) or (not php_empty(lambda : metakeyinput)):
        #// 
        #// We have a key/value pair. If both the select and the input
        #// for the key have data, the input takes precedence.
        #//
        if "#NONE#" != metakeyselect:
            metakey = metakeyselect
        # end if
        if metakeyinput:
            metakey = metakeyinput
            pass
        # end if
        if is_protected_meta(metakey, "post") or (not current_user_can("add_post_meta", post_ID, metakey)):
            return False
        # end if
        metakey = wp_slash(metakey)
        return add_post_meta(post_ID, metakey, metavalue)
    # end if
    return False
# end def add_meta
#// 
#// Delete post meta data by meta ID.
#// 
#// @since 1.2.0
#// 
#// @param int $mid
#// @return bool
#//
def delete_meta(mid=None, *args_):
    
    return delete_metadata_by_mid("post", mid)
# end def delete_meta
#// 
#// Get a list of previously defined keys.
#// 
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return mixed
#//
def get_meta_keys(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    keys = wpdb.get_col(str("\n         SELECT meta_key\n           FROM ") + str(wpdb.postmeta) + str("\n          GROUP BY meta_key\n         ORDER BY meta_key"))
    return keys
# end def get_meta_keys
#// 
#// Get post meta data by meta ID.
#// 
#// @since 2.1.0
#// 
#// @param int $mid
#// @return object|bool
#//
def get_post_meta_by_id(mid=None, *args_):
    
    return get_metadata_by_mid("post", mid)
# end def get_post_meta_by_id
#// 
#// Get meta data for the given post ID.
#// 
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $postid
#// @return mixed
#//
def has_meta(postid=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    return wpdb.get_results(wpdb.prepare(str("SELECT meta_key, meta_value, meta_id, post_id\n           FROM ") + str(wpdb.postmeta) + str(" WHERE post_id = %d\n           ORDER BY meta_key,meta_id"), postid), ARRAY_A)
# end def has_meta
#// 
#// Update post meta data by meta ID.
#// 
#// @since 1.2.0
#// 
#// @param int    $meta_id
#// @param string $meta_key Expect Slashed
#// @param string $meta_value Expect Slashed
#// @return bool
#//
def update_meta(meta_id=None, meta_key=None, meta_value=None, *args_):
    
    meta_key = wp_unslash(meta_key)
    meta_value = wp_unslash(meta_value)
    return update_metadata_by_mid("post", meta_id, meta_value, meta_key)
# end def update_meta
#// 
#// Private.
#// 
#// 
#// Replace hrefs of attachment anchors with up-to-date permalinks.
#// 
#// @since 2.3.0
#// @access private
#// 
#// @param int|object $post Post ID or post object.
#// @return void|int|WP_Error Void if nothing fixed. 0 or WP_Error on update failure. The post ID on update success.
#//
def _fix_attachment_links(post=None, *args_):
    
    post = get_post(post, ARRAY_A)
    content = post["post_content"]
    #// Don't run if no pretty permalinks or post is not published, scheduled, or privately published.
    if (not get_option("permalink_structure")) or (not php_in_array(post["post_status"], Array("publish", "future", "private"))):
        return
    # end if
    #// Short if there aren't any links or no '?attachment_id=' strings (strpos cannot be zero).
    if (not php_strpos(content, "?attachment_id=")) or (not preg_match_all("/<a ([^>]+)>[\\s\\S]+?<\\/a>/", content, link_matches)):
        return
    # end if
    site_url = get_bloginfo("url")
    site_url = php_substr(site_url, int(php_strpos(site_url, "://")))
    #// Remove the http(s).
    replace = ""
    for key,value in link_matches[1]:
        if (not php_strpos(value, "?attachment_id=")) or (not php_strpos(value, "wp-att-")) or (not php_preg_match("/href=([\"'])[^\"']*\\?attachment_id=(\\d+)[^\"']*\\1/", value, url_match)) or (not php_preg_match("/rel=[\"'][^\"']*wp-att-(\\d+)/", value, rel_match)):
            continue
        # end if
        quote = url_match[1]
        #// The quote (single or double).
        url_id = int(url_match[2])
        rel_id = int(rel_match[1])
        if (not url_id) or (not rel_id) or url_id != rel_id or php_strpos(url_match[0], site_url) == False:
            continue
        # end if
        link = link_matches[0][key]
        replace = php_str_replace(url_match[0], "href=" + quote + get_attachment_link(url_id) + quote, link)
        content = php_str_replace(link, replace, content)
    # end for
    if replace:
        post["post_content"] = content
        #// Escape data pulled from DB.
        post = add_magic_quotes(post)
        return wp_update_post(post)
    # end if
# end def _fix_attachment_links
#// 
#// Get all the possible statuses for a post_type
#// 
#// @since 2.5.0
#// 
#// @param string $type The post_type you want the statuses for. Default 'post'.
#// @return string[] An array of all the statuses for the supplied post type.
#//
def get_available_post_statuses(type="post", *args_):
    
    stati = wp_count_posts(type)
    return php_array_keys(get_object_vars(stati))
# end def get_available_post_statuses
#// 
#// Run the wp query to fetch the posts for listing on the edit posts page
#// 
#// @since 2.5.0
#// 
#// @param array|bool $q Array of query variables to use to build the query or false to use $_GET superglobal.
#// @return array
#//
def wp_edit_posts_query(q=False, *args_):
    
    if False == q:
        q = PHP_REQUEST
    # end if
    q["m"] = int(q["m"]) if (php_isset(lambda : q["m"])) else 0
    q["cat"] = int(q["cat"]) if (php_isset(lambda : q["cat"])) else 0
    post_stati = get_post_stati()
    if (php_isset(lambda : q["post_type"])) and php_in_array(q["post_type"], get_post_types()):
        post_type = q["post_type"]
    else:
        post_type = "post"
    # end if
    avail_post_stati = get_available_post_statuses(post_type)
    post_status = ""
    perm = ""
    if (php_isset(lambda : q["post_status"])) and php_in_array(q["post_status"], post_stati):
        post_status = q["post_status"]
        perm = "readable"
    # end if
    orderby = ""
    if (php_isset(lambda : q["orderby"])):
        orderby = q["orderby"]
    elif (php_isset(lambda : q["post_status"])) and php_in_array(q["post_status"], Array("pending", "draft")):
        orderby = "modified"
    # end if
    order = ""
    if (php_isset(lambda : q["order"])):
        order = q["order"]
    elif (php_isset(lambda : q["post_status"])) and "pending" == q["post_status"]:
        order = "ASC"
    # end if
    per_page = str("edit_") + str(post_type) + str("_per_page")
    posts_per_page = int(get_user_option(per_page))
    if php_empty(lambda : posts_per_page) or posts_per_page < 1:
        posts_per_page = 20
    # end if
    #// 
    #// Filters the number of items per page to show for a specific 'per_page' type.
    #// 
    #// The dynamic portion of the hook name, `$post_type`, refers to the post type.
    #// 
    #// Some examples of filter hooks generated here include: 'edit_attachment_per_page',
    #// 'edit_post_per_page', 'edit_page_per_page', etc.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int $posts_per_page Number of posts to display per page for the given post
    #// type. Default 20.
    #//
    posts_per_page = apply_filters(str("edit_") + str(post_type) + str("_per_page"), posts_per_page)
    #// 
    #// Filters the number of posts displayed per page when specifically listing "posts".
    #// 
    #// @since 2.8.0
    #// 
    #// @param int    $posts_per_page Number of posts to be displayed. Default 20.
    #// @param string $post_type      The post type.
    #//
    posts_per_page = apply_filters("edit_posts_per_page", posts_per_page, post_type)
    query = compact("post_type", "post_status", "perm", "order", "orderby", "posts_per_page")
    #// Hierarchical types require special args.
    if is_post_type_hierarchical(post_type) and php_empty(lambda : orderby):
        query["orderby"] = "menu_order title"
        query["order"] = "asc"
        query["posts_per_page"] = -1
        query["posts_per_archive_page"] = -1
        query["fields"] = "id=>parent"
    # end if
    if (not php_empty(lambda : q["show_sticky"])):
        query["post__in"] = get_option("sticky_posts")
    # end if
    wp(query)
    return avail_post_stati
# end def wp_edit_posts_query
#// 
#// Get the query variables for the current attachments request.
#// 
#// @since 4.2.0
#// 
#// @param array|false $q Optional. Array of query variables to use to build the query or false
#// to use $_GET superglobal. Default false.
#// @return array The parsed query vars.
#//
def wp_edit_attachments_query_vars(q=False, *args_):
    
    if False == q:
        q = PHP_REQUEST
    # end if
    q["m"] = int(q["m"]) if (php_isset(lambda : q["m"])) else 0
    q["cat"] = int(q["cat"]) if (php_isset(lambda : q["cat"])) else 0
    q["post_type"] = "attachment"
    post_type = get_post_type_object("attachment")
    states = "inherit"
    if current_user_can(post_type.cap.read_private_posts):
        states += ",private"
    # end if
    q["post_status"] = "trash" if (php_isset(lambda : q["status"])) and "trash" == q["status"] else states
    q["post_status"] = "trash" if (php_isset(lambda : q["attachment-filter"])) and "trash" == q["attachment-filter"] else states
    media_per_page = int(get_user_option("upload_per_page"))
    if php_empty(lambda : media_per_page) or media_per_page < 1:
        media_per_page = 20
    # end if
    #// 
    #// Filters the number of items to list per page when listing media items.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $media_per_page Number of media to list. Default 20.
    #//
    q["posts_per_page"] = apply_filters("upload_per_page", media_per_page)
    post_mime_types = get_post_mime_types()
    if (php_isset(lambda : q["post_mime_type"])) and (not php_array_intersect(q["post_mime_type"], php_array_keys(post_mime_types))):
        q["post_mime_type"] = None
    # end if
    for type in php_array_keys(post_mime_types):
        if (php_isset(lambda : q["attachment-filter"])) and str("post_mime_type:") + str(type) == q["attachment-filter"]:
            q["post_mime_type"] = type
            break
        # end if
    # end for
    if (php_isset(lambda : q["detached"])) or (php_isset(lambda : q["attachment-filter"])) and "detached" == q["attachment-filter"]:
        q["post_parent"] = 0
    # end if
    if (php_isset(lambda : q["mine"])) or (php_isset(lambda : q["attachment-filter"])) and "mine" == q["attachment-filter"]:
        q["author"] = get_current_user_id()
    # end if
    #// Filter query clauses to include filenames.
    if (php_isset(lambda : q["s"])):
        add_filter("posts_clauses", "_filter_query_attachment_filenames")
    # end if
    return q
# end def wp_edit_attachments_query_vars
#// 
#// Executes a query for attachments. An array of WP_Query arguments
#// can be passed in, which will override the arguments set by this function.
#// 
#// @since 2.5.0
#// 
#// @param array|false $q Array of query variables to use to build the query or false to use $_GET superglobal.
#// @return array
#//
def wp_edit_attachments_query(q=False, *args_):
    
    wp(wp_edit_attachments_query_vars(q))
    post_mime_types = get_post_mime_types()
    avail_post_mime_types = get_available_post_mime_types("attachment")
    return Array(post_mime_types, avail_post_mime_types)
# end def wp_edit_attachments_query
#// 
#// Returns the list of classes to be used by a meta box.
#// 
#// @since 2.5.0
#// 
#// @param string $box_id    Meta box ID (used in the 'id' attribute for the meta box).
#// @param string $screen_id The screen on which the meta box is shown.
#// @return string Space-separated string of class names.
#//
def postbox_classes(box_id=None, screen_id=None, *args_):
    
    if (php_isset(lambda : PHP_REQUEST["edit"])) and PHP_REQUEST["edit"] == box_id:
        classes = Array("")
    elif get_user_option("closedpostboxes_" + screen_id):
        closed = get_user_option("closedpostboxes_" + screen_id)
        if (not php_is_array(closed)):
            classes = Array("")
        else:
            classes = Array("closed") if php_in_array(box_id, closed) else Array("")
        # end if
    else:
        classes = Array("")
    # end if
    #// 
    #// Filters the postbox classes for a specific screen and box ID combo.
    #// 
    #// The dynamic portions of the hook name, `$screen_id` and `$box_id`, refer to
    #// the screen ID and meta box ID, respectively.
    #// 
    #// @since 3.2.0
    #// 
    #// @param string[] $classes An array of postbox classes.
    #//
    classes = apply_filters(str("postbox_classes_") + str(screen_id) + str("_") + str(box_id), classes)
    return php_implode(" ", classes)
# end def postbox_classes
#// 
#// Get a sample permalink based off of the post name.
#// 
#// @since 2.5.0
#// 
#// @param int    $id    Post ID or post object.
#// @param string $title Optional. Title to override the post's current title when generating the post name. Default null.
#// @param string $name  Optional. Name to override the post name. Default null.
#// @return array {
#// Array containing the sample permalink with placeholder for the post name, and the post name.
#// 
#// @type string $0 The permalink with placeholder for the post name.
#// @type string $1 The post name.
#// }
#//
def get_sample_permalink(id=None, title=None, name=None, *args_):
    
    post = get_post(id)
    if (not post):
        return Array("", "")
    # end if
    ptype = get_post_type_object(post.post_type)
    original_status = post.post_status
    original_date = post.post_date
    original_name = post.post_name
    #// Hack: get_permalink() would return ugly permalink for drafts, so we will fake that our post is published.
    if php_in_array(post.post_status, Array("draft", "pending", "future")):
        post.post_status = "publish"
        post.post_name = sanitize_title(post.post_name if post.post_name else post.post_title, post.ID)
    # end if
    #// If the user wants to set a new name -- override the current one.
    #// Note: if empty name is supplied -- use the title instead, see #6072.
    if (not php_is_null(name)):
        post.post_name = sanitize_title(name if name else title, post.ID)
    # end if
    post.post_name = wp_unique_post_slug(post.post_name, post.ID, post.post_status, post.post_type, post.post_parent)
    post.filter = "sample"
    permalink = get_permalink(post, True)
    #// Replace custom post_type token with generic pagename token for ease of use.
    permalink = php_str_replace(str("%") + str(post.post_type) + str("%"), "%pagename%", permalink)
    #// Handle page hierarchy.
    if ptype.hierarchical:
        uri = get_page_uri(post)
        if uri:
            uri = untrailingslashit(uri)
            uri = php_strrev(php_stristr(php_strrev(uri), "/"))
            uri = untrailingslashit(uri)
        # end if
        #// This filter is documented in wp-admin/edit-tag-form.php
        uri = apply_filters("editable_slug", uri, post)
        if (not php_empty(lambda : uri)):
            uri += "/"
        # end if
        permalink = php_str_replace("%pagename%", str(uri) + str("%pagename%"), permalink)
    # end if
    #// This filter is documented in wp-admin/edit-tag-form.php
    permalink = Array(permalink, apply_filters("editable_slug", post.post_name, post))
    post.post_status = original_status
    post.post_date = original_date
    post.post_name = original_name
    post.filter = None
    #// 
    #// Filters the sample permalink.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array   $permalink {
    #// Array containing the sample permalink with placeholder for the post name, and the post name.
    #// 
    #// @type string $0 The permalink with placeholder for the post name.
    #// @type string $1 The post name.
    #// }
    #// @param int     $post_id   Post ID.
    #// @param string  $title     Post title.
    #// @param string  $name      Post name (slug).
    #// @param WP_Post $post      Post object.
    #//
    return apply_filters("get_sample_permalink", permalink, post.ID, title, name, post)
# end def get_sample_permalink
#// 
#// Returns the HTML of the sample permalink slug editor.
#// 
#// @since 2.5.0
#// 
#// @param int    $id        Post ID or post object.
#// @param string $new_title Optional. New title. Default null.
#// @param string $new_slug  Optional. New slug. Default null.
#// @return string The HTML of the sample permalink slug editor.
#//
def get_sample_permalink_html(id=None, new_title=None, new_slug=None, *args_):
    
    post = get_post(id)
    if (not post):
        return ""
    # end if
    permalink, post_name = get_sample_permalink(post.ID, new_title, new_slug)
    view_link = False
    preview_target = ""
    if current_user_can("read_post", post.ID):
        if "draft" == post.post_status or php_empty(lambda : post.post_name):
            view_link = get_preview_post_link(post)
            preview_target = str(" target='wp-preview-") + str(post.ID) + str("'")
        else:
            if "publish" == post.post_status or "attachment" == post.post_type:
                view_link = get_permalink(post)
            else:
                #// Allow non-published (private, future) to be viewed at a pretty permalink, in case $post->post_name is set.
                view_link = php_str_replace(Array("%pagename%", "%postname%"), post.post_name, permalink)
            # end if
        # end if
    # end if
    #// Permalinks without a post/page name placeholder don't have anything to edit.
    if False == php_strpos(permalink, "%postname%") and False == php_strpos(permalink, "%pagename%"):
        return_ = "<strong>" + __("Permalink:") + "</strong>\n"
        if False != view_link:
            display_link = urldecode(view_link)
            return_ += "<a id=\"sample-permalink\" href=\"" + esc_url(view_link) + "\"" + preview_target + ">" + esc_html(display_link) + "</a>\n"
        else:
            return_ += "<span id=\"sample-permalink\">" + permalink + "</span>\n"
        # end if
        #// Encourage a pretty permalink setting.
        if "" == get_option("permalink_structure") and current_user_can("manage_options") and (not "page" == get_option("show_on_front") and get_option("page_on_front") == id):
            return_ += "<span id=\"change-permalinks\"><a href=\"options-permalink.php\" class=\"button button-small\" target=\"_blank\">" + __("Change Permalinks") + "</a></span>\n"
        # end if
    else:
        if php_mb_strlen(post_name) > 34:
            post_name_abridged = php_mb_substr(post_name, 0, 16) + "&hellip;" + php_mb_substr(post_name, -16)
        else:
            post_name_abridged = post_name
        # end if
        post_name_html = "<span id=\"editable-post-name\">" + esc_html(post_name_abridged) + "</span>"
        display_link = php_str_replace(Array("%pagename%", "%postname%"), post_name_html, esc_html(urldecode(permalink)))
        return_ = "<strong>" + __("Permalink:") + "</strong>\n"
        return_ += "<span id=\"sample-permalink\"><a href=\"" + esc_url(view_link) + "\"" + preview_target + ">" + display_link + "</a></span>\n"
        return_ += "&lrm;"
        #// Fix bi-directional text display defect in RTL languages.
        return_ += "<span id=\"edit-slug-buttons\"><button type=\"button\" class=\"edit-slug button button-small hide-if-no-js\" aria-label=\"" + __("Edit permalink") + "\">" + __("Edit") + "</button></span>\n"
        return_ += "<span id=\"editable-post-name-full\">" + esc_html(post_name) + "</span>\n"
    # end if
    #// 
    #// Filters the sample permalink HTML markup.
    #// 
    #// @since 2.9.0
    #// @since 4.4.0 Added `$post` parameter.
    #// 
    #// @param string  $return    Sample permalink HTML markup.
    #// @param int     $post_id   Post ID.
    #// @param string  $new_title New sample permalink title.
    #// @param string  $new_slug  New sample permalink slug.
    #// @param WP_Post $post      Post object.
    #//
    return_ = apply_filters("get_sample_permalink_html", return_, post.ID, new_title, new_slug, post)
    return return_
# end def get_sample_permalink_html
#// 
#// Output HTML for the post thumbnail meta-box.
#// 
#// @since 2.9.0
#// 
#// @param int $thumbnail_id ID of the attachment used for thumbnail
#// @param int|WP_Post $post Optional. The post ID or object associated with the thumbnail, defaults to global $post.
#// @return string html
#//
def _wp_post_thumbnail_html(thumbnail_id=None, post=None, *args_):
    
    _wp_additional_image_sizes = wp_get_additional_image_sizes()
    post = get_post(post)
    post_type_object = get_post_type_object(post.post_type)
    set_thumbnail_link = "<p class=\"hide-if-no-js\"><a href=\"%s\" id=\"set-post-thumbnail\"%s class=\"thickbox\">%s</a></p>"
    upload_iframe_src = get_upload_iframe_src("image", post.ID)
    content = php_sprintf(set_thumbnail_link, esc_url(upload_iframe_src), "", esc_html(post_type_object.labels.set_featured_image))
    if thumbnail_id and get_post(thumbnail_id):
        size = "post-thumbnail" if (php_isset(lambda : _wp_additional_image_sizes["post-thumbnail"])) else Array(266, 266)
        #// 
        #// Filters the size used to display the post thumbnail image in the 'Featured image' meta box.
        #// 
        #// Note: When a theme adds 'post-thumbnail' support, a special 'post-thumbnail'
        #// image size is registered, which differs from the 'thumbnail' image size
        #// managed via the Settings > Media screen. See the `$size` parameter description
        #// for more information on default values.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string|array $size         Post thumbnail image size to display in the meta box. Accepts any valid
        #// image size, or an array of width and height values in pixels (in that order).
        #// If the 'post-thumbnail' size is set, default is 'post-thumbnail'. Otherwise,
        #// default is an array with 266 as both the height and width values.
        #// @param int          $thumbnail_id Post thumbnail attachment ID.
        #// @param WP_Post      $post         The post object associated with the thumbnail.
        #//
        size = apply_filters("admin_post_thumbnail_size", size, thumbnail_id, post)
        thumbnail_html = wp_get_attachment_image(thumbnail_id, size)
        if (not php_empty(lambda : thumbnail_html)):
            content = php_sprintf(set_thumbnail_link, esc_url(upload_iframe_src), " aria-describedby=\"set-post-thumbnail-desc\"", thumbnail_html)
            content += "<p class=\"hide-if-no-js howto\" id=\"set-post-thumbnail-desc\">" + __("Click the image to edit or update") + "</p>"
            content += "<p class=\"hide-if-no-js\"><a href=\"#\" id=\"remove-post-thumbnail\">" + esc_html(post_type_object.labels.remove_featured_image) + "</a></p>"
        # end if
    # end if
    content += "<input type=\"hidden\" id=\"_thumbnail_id\" name=\"_thumbnail_id\" value=\"" + esc_attr(thumbnail_id if thumbnail_id else "-1") + "\" />"
    #// 
    #// Filters the admin post thumbnail HTML markup to return.
    #// 
    #// @since 2.9.0
    #// @since 3.5.0 Added the `$post_id` parameter.
    #// @since 4.6.0 Added the `$thumbnail_id` parameter.
    #// 
    #// @param string   $content      Admin post thumbnail HTML markup.
    #// @param int      $post_id      Post ID.
    #// @param int|null $thumbnail_id Thumbnail attachment ID, or null if there isn't one.
    #//
    return apply_filters("admin_post_thumbnail_html", content, post.ID, thumbnail_id)
# end def _wp_post_thumbnail_html
#// 
#// Check to see if the post is currently being edited by another user.
#// 
#// @since 2.5.0
#// 
#// @param int $post_id ID of the post to check for editing.
#// @return int|false ID of the user with lock. False if the post does not exist, post is not locked,
#// the user with lock does not exist, or the post is locked by current user.
#//
def wp_check_post_lock(post_id=None, *args_):
    
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    lock = get_post_meta(post.ID, "_edit_lock", True)
    if (not lock):
        return False
    # end if
    lock = php_explode(":", lock)
    time = lock[0]
    user = lock[1] if (php_isset(lambda : lock[1])) else get_post_meta(post.ID, "_edit_last", True)
    if (not get_userdata(user)):
        return False
    # end if
    #// This filter is documented in wp-admin/includes/ajax-actions.php
    time_window = apply_filters("wp_check_post_lock_window", 150)
    if time and time > time() - time_window and get_current_user_id() != user:
        return user
    # end if
    return False
# end def wp_check_post_lock
#// 
#// Mark the post as currently being edited by the current user
#// 
#// @since 2.5.0
#// 
#// @param int $post_id ID of the post being edited.
#// @return array|false Array of the lock time and user ID. False if the post does not exist, or
#// there is no current user.
#//
def wp_set_post_lock(post_id=None, *args_):
    
    post = get_post(post_id)
    if (not post):
        return False
    # end if
    user_id = get_current_user_id()
    if 0 == user_id:
        return False
    # end if
    now = time()
    lock = str(now) + str(":") + str(user_id)
    update_post_meta(post.ID, "_edit_lock", lock)
    return Array(now, user_id)
# end def wp_set_post_lock
#// 
#// Outputs the HTML for the notice to say that someone else is editing or has taken over editing of this post.
#// 
#// @since 2.8.5
#//
def _admin_notice_post_locked(*args_):
    
    post = get_post()
    if (not post):
        return
    # end if
    user = None
    user_id = wp_check_post_lock(post.ID)
    if user_id:
        user = get_userdata(user_id)
    # end if
    if user:
        #// 
        #// Filters whether to show the post locked dialog.
        #// 
        #// Returning false from the filter will prevent the dialog from being displayed.
        #// 
        #// @since 3.6.0
        #// 
        #// @param bool    $display Whether to display the dialog. Default true.
        #// @param WP_Post $post    Post object.
        #// @param WP_User $user    The user with the lock for the post.
        #//
        if (not apply_filters("show_post_locked_dialog", True, post, user)):
            return
        # end if
        locked = True
    else:
        locked = False
    # end if
    sendback = wp_get_referer()
    if locked and sendback and False == php_strpos(sendback, "post.php") and False == php_strpos(sendback, "post-new.php"):
        sendback_text = __("Go back")
    else:
        sendback = admin_url("edit.php")
        if "post" != post.post_type:
            sendback = add_query_arg("post_type", post.post_type, sendback)
        # end if
        sendback_text = get_post_type_object(post.post_type).labels.all_items
    # end if
    hidden = "" if locked else " hidden"
    php_print(" <div id=\"post-lock-dialog\" class=\"notification-dialog-wrap")
    php_print(hidden)
    php_print("""\">
    <div class=\"notification-dialog-background\"></div>
    <div class=\"notification-dialog\">
    """)
    if locked:
        query_args = Array()
        if get_post_type_object(post.post_type).public:
            if "publish" == post.post_status or user.ID != post.post_author:
                #// Latest content is in autosave.
                nonce = wp_create_nonce("post_preview_" + post.ID)
                query_args["preview_id"] = post.ID
                query_args["preview_nonce"] = nonce
            # end if
        # end if
        preview_link = get_preview_post_link(post.ID, query_args)
        #// 
        #// Filters whether to allow the post lock to be overridden.
        #// 
        #// Returning false from the filter will disable the ability
        #// to override the post lock.
        #// 
        #// @since 3.6.0
        #// 
        #// @param bool    $override Whether to allow the post lock to be overridden. Default true.
        #// @param WP_Post $post     Post object.
        #// @param WP_User $user     The user with the lock for the post.
        #//
        override = apply_filters("override_post_lock", True, post, user)
        tab_last = "" if override else " wp-tab-last"
        php_print("     <div class=\"post-locked-message\">\n       <div class=\"post-locked-avatar\">")
        php_print(get_avatar(user.ID, 64))
        php_print("</div>\n     <p class=\"currently-editing wp-tab-first\" tabindex=\"0\">\n       ")
        if override:
            #// translators: %s: User's display name.
            printf(__("%s is already editing this post. Do you want to take over?"), esc_html(user.display_name))
        else:
            #// translators: %s: User's display name.
            printf(__("%s is already editing this post."), esc_html(user.display_name))
        # end if
        php_print("     </p>\n      ")
        #// 
        #// Fires inside the post locked dialog before the buttons are displayed.
        #// 
        #// @since 3.6.0
        #// @since 5.4.0 The $user parameter was added.
        #// 
        #// @param WP_Post $post Post object.
        #// @param WP_User $user The user with the lock for the post.
        #//
        do_action("post_locked_dialog", post, user)
        php_print("     <p>\n       <a class=\"button\" href=\"")
        php_print(esc_url(sendback))
        php_print("\">")
        php_print(sendback_text)
        php_print("</a>\n       ")
        if preview_link:
            php_print("     <a class=\"button")
            php_print(tab_last)
            php_print("\" href=\"")
            php_print(esc_url(preview_link))
            php_print("\">")
            _e("Preview")
            php_print("</a>\n           ")
        # end if
        #// Allow plugins to prevent some users overriding the post lock.
        if override:
            php_print(" <a class=\"button button-primary wp-tab-last\" href=\"")
            php_print(esc_url(add_query_arg("get-post-lock", "1", wp_nonce_url(get_edit_post_link(post.ID, "url"), "lock-post_" + post.ID))))
            php_print("\">")
            _e("Take over")
            php_print("</a>\n           ")
        # end if
        php_print("     </p>\n      </div>\n        ")
    else:
        php_print("""       <div class=\"post-taken-over\">
        <div class=\"post-locked-avatar\"></div>
        <p class=\"wp-tab-first\" tabindex=\"0\">
        <span class=\"currently-editing\"></span><br />
        <span class=\"locked-saving hidden\"><img src=\"""")
        php_print(esc_url(admin_url("images/spinner-2x.gif")))
        php_print("\" width=\"16\" height=\"16\" alt=\"\" /> ")
        _e("Saving revision&hellip;")
        php_print("</span>\n            <span class=\"locked-saved hidden\">")
        _e("Your latest changes were saved as a revision.")
        php_print("</span>\n            </p>\n          ")
        #// 
        #// Fires inside the dialog displayed when a user has lost the post lock.
        #// 
        #// @since 3.6.0
        #// 
        #// @param WP_Post $post Post object.
        #//
        do_action("post_lock_lost_dialog", post)
        php_print("         <p><a class=\"button button-primary wp-tab-last\" href=\"")
        php_print(esc_url(sendback))
        php_print("\">")
        php_print(sendback_text)
        php_print("</a></p>\n       </div>\n        ")
    # end if
    php_print(" </div>\n    </div>\n    ")
# end def _admin_notice_post_locked
#// 
#// Creates autosave data for the specified post from $_POST data.
#// 
#// @since 2.6.0
#// 
#// @param array|int $post_data Associative array containing the post data or int post ID.
#// @return int|WP_Error The autosave revision ID. WP_Error or 0 on error.
#//
def wp_create_post_autosave(post_data=None, *args_):
    
    if php_is_numeric(post_data):
        post_id = post_data
        post_data = PHP_POST
    else:
        post_id = int(post_data["post_ID"])
    # end if
    post_data = _wp_translate_postdata(True, post_data)
    if is_wp_error(post_data):
        return post_data
    # end if
    post_data = _wp_get_allowed_postdata(post_data)
    post_author = get_current_user_id()
    #// Store one autosave per author. If there is already an autosave, overwrite it.
    old_autosave = wp_get_post_autosave(post_id, post_author)
    if old_autosave:
        new_autosave = _wp_post_revision_data(post_data, True)
        new_autosave["ID"] = old_autosave.ID
        new_autosave["post_author"] = post_author
        post = get_post(post_id)
        #// If the new autosave has the same content as the post, delete the autosave.
        autosave_is_different = False
        for field in php_array_intersect(php_array_keys(new_autosave), php_array_keys(_wp_post_revision_fields(post))):
            if normalize_whitespace(new_autosave[field]) != normalize_whitespace(post.field):
                autosave_is_different = True
                break
            # end if
        # end for
        if (not autosave_is_different):
            wp_delete_post_revision(old_autosave.ID)
            return 0
        # end if
        #// 
        #// Fires before an autosave is stored.
        #// 
        #// @since 4.1.0
        #// 
        #// @param array $new_autosave Post array - the autosave that is about to be saved.
        #//
        do_action("wp_creating_autosave", new_autosave)
        return wp_update_post(new_autosave)
    # end if
    #// _wp_put_post_revision() expects unescaped.
    post_data = wp_unslash(post_data)
    #// Otherwise create the new autosave as a special post revision.
    return _wp_put_post_revision(post_data, True)
# end def wp_create_post_autosave
#// 
#// Saves a draft or manually autosaves for the purpose of showing a post preview.
#// 
#// @since 2.7.0
#// 
#// @return string URL to redirect to show the preview.
#//
def post_preview(*args_):
    global PHP_POST
    post_ID = int(PHP_POST["post_ID"])
    PHP_POST["ID"] = post_ID
    post = get_post(post_ID)
    if (not post):
        wp_die(__("Sorry, you are not allowed to edit this post."))
    # end if
    if (not current_user_can("edit_post", post.ID)):
        wp_die(__("Sorry, you are not allowed to edit this post."))
    # end if
    is_autosave = False
    if (not wp_check_post_lock(post.ID)) and get_current_user_id() == post.post_author and "draft" == post.post_status or "auto-draft" == post.post_status:
        saved_post_id = edit_post()
    else:
        is_autosave = True
        if (php_isset(lambda : PHP_POST["post_status"])) and "auto-draft" == PHP_POST["post_status"]:
            PHP_POST["post_status"] = "draft"
        # end if
        saved_post_id = wp_create_post_autosave(post.ID)
    # end if
    if is_wp_error(saved_post_id):
        wp_die(saved_post_id.get_error_message())
    # end if
    query_args = Array()
    if is_autosave and saved_post_id:
        query_args["preview_id"] = post.ID
        query_args["preview_nonce"] = wp_create_nonce("post_preview_" + post.ID)
        if (php_isset(lambda : PHP_POST["post_format"])):
            query_args["post_format"] = "standard" if php_empty(lambda : PHP_POST["post_format"]) else sanitize_key(PHP_POST["post_format"])
        # end if
        if (php_isset(lambda : PHP_POST["_thumbnail_id"])):
            query_args["_thumbnail_id"] = "-1" if php_intval(PHP_POST["_thumbnail_id"]) <= 0 else php_intval(PHP_POST["_thumbnail_id"])
        # end if
    # end if
    return get_preview_post_link(post, query_args)
# end def post_preview
#// 
#// Save a post submitted with XHR
#// 
#// Intended for use with heartbeat and autosave.js
#// 
#// @since 3.9.0
#// 
#// @param array $post_data Associative array of the submitted post data.
#// @return mixed The value 0 or WP_Error on failure. The saved post ID on success.
#// The ID can be the draft post_id or the autosave revision post_id.
#//
def wp_autosave(post_data=None, *args_):
    
    #// Back-compat.
    if (not php_defined("DOING_AUTOSAVE")):
        php_define("DOING_AUTOSAVE", True)
    # end if
    post_id = int(post_data["post_id"])
    post_data["ID"] = post_id
    post_data["post_ID"] = post_id
    if False == wp_verify_nonce(post_data["_wpnonce"], "update-post_" + post_id):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_nonce", __("Error while saving.")))
    # end if
    post = get_post(post_id)
    if (not current_user_can("edit_post", post.ID)):
        return php_new_class("WP_Error", lambda : WP_Error("edit_posts", __("Sorry, you are not allowed to edit this item.")))
    # end if
    if "auto-draft" == post.post_status:
        post_data["post_status"] = "draft"
    # end if
    if "page" != post_data["post_type"] and (not php_empty(lambda : post_data["catslist"])):
        post_data["post_category"] = php_explode(",", post_data["catslist"])
    # end if
    if (not wp_check_post_lock(post.ID)) and get_current_user_id() == post.post_author and "auto-draft" == post.post_status or "draft" == post.post_status:
        #// Drafts and auto-drafts are just overwritten by autosave for the same user if the post is not locked.
        return edit_post(wp_slash(post_data))
    else:
        #// Non-drafts or other users' drafts are not overwritten.
        #// The autosave is stored in a special post revision for each user.
        return wp_create_post_autosave(wp_slash(post_data))
    # end if
# end def wp_autosave
#// 
#// Redirect to previous page.
#// 
#// @since 2.7.0
#// 
#// @param int $post_id Optional. Post ID.
#//
def redirect_post(post_id="", *args_):
    
    if (php_isset(lambda : PHP_POST["save"])) or (php_isset(lambda : PHP_POST["publish"])):
        status = get_post_status(post_id)
        if (php_isset(lambda : PHP_POST["publish"])):
            for case in Switch(status):
                if case("pending"):
                    message = 8
                    break
                # end if
                if case("future"):
                    message = 9
                    break
                # end if
                if case():
                    message = 6
                # end if
            # end for
        else:
            message = 10 if "draft" == status else 1
        # end if
        location = add_query_arg("message", message, get_edit_post_link(post_id, "url"))
    elif (php_isset(lambda : PHP_POST["addmeta"])) and PHP_POST["addmeta"]:
        location = add_query_arg("message", 2, wp_get_referer())
        location = php_explode("#", location)
        location = location[0] + "#postcustom"
    elif (php_isset(lambda : PHP_POST["deletemeta"])) and PHP_POST["deletemeta"]:
        location = add_query_arg("message", 3, wp_get_referer())
        location = php_explode("#", location)
        location = location[0] + "#postcustom"
    else:
        location = add_query_arg("message", 4, get_edit_post_link(post_id, "url"))
    # end if
    #// 
    #// Filters the post redirect destination URL.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $location The destination URL.
    #// @param int    $post_id  The post ID.
    #//
    wp_redirect(apply_filters("redirect_post_location", location, post_id))
    php_exit(0)
# end def redirect_post
#// 
#// Sanitizes POST values from a checkbox taxonomy metabox.
#// 
#// @since 5.1.0
#// 
#// @param string $taxonomy The taxonomy name.
#// @param array  $terms    Raw term data from the 'tax_input' field.
#// @return int[] Array of sanitized term IDs.
#//
def taxonomy_meta_box_sanitize_cb_checkboxes(taxonomy=None, terms=None, *args_):
    
    return php_array_map("intval", terms)
# end def taxonomy_meta_box_sanitize_cb_checkboxes
#// 
#// Sanitizes POST values from an input taxonomy metabox.
#// 
#// @since 5.1.0
#// 
#// @param string       $taxonomy The taxonomy name.
#// @param array|string $terms    Raw term data from the 'tax_input' field.
#// @return array
#//
def taxonomy_meta_box_sanitize_cb_input(taxonomy=None, terms=None, *args_):
    
    #// 
    #// Assume that a 'tax_input' string is a comma-separated list of term names.
    #// Some languages may use a character other than a comma as a delimiter, so we standardize on
    #// commas before parsing the list.
    #//
    if (not php_is_array(terms)):
        comma = _x(",", "tag delimiter")
        if "," != comma:
            terms = php_str_replace(comma, ",", terms)
        # end if
        terms = php_explode(",", php_trim(terms, " \n   \r ,"))
    # end if
    clean_terms = Array()
    for term in terms:
        #// Empty terms are invalid input.
        if php_empty(lambda : term):
            continue
        # end if
        _term = get_terms(Array({"taxonomy": taxonomy, "name": term, "fields": "ids", "hide_empty": False}))
        if (not php_empty(lambda : _term)):
            clean_terms[-1] = php_intval(_term[0])
        else:
            #// No existing term was found, so pass the string. A new term will be created.
            clean_terms[-1] = term
        # end if
    # end for
    return clean_terms
# end def taxonomy_meta_box_sanitize_cb_input
#// 
#// Return whether the post can be edited in the block editor.
#// 
#// @since 5.0.0
#// 
#// @param int|WP_Post $post Post ID or WP_Post object.
#// @return bool Whether the post can be edited in the block editor.
#//
def use_block_editor_for_post(post=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    #// We're in the meta box loader, so don't use the block editor.
    if (php_isset(lambda : PHP_REQUEST["meta-box-loader"])):
        check_admin_referer("meta-box-loader", "meta-box-loader-nonce")
        return False
    # end if
    #// The posts page can't be edited in the block editor.
    if absint(get_option("page_for_posts")) == post.ID and php_empty(lambda : post.post_content):
        return False
    # end if
    use_block_editor = use_block_editor_for_post_type(post.post_type)
    #// 
    #// Filter whether a post is able to be edited in the block editor.
    #// 
    #// @since 5.0.0
    #// 
    #// @param bool    $use_block_editor Whether the post can be edited or not.
    #// @param WP_Post $post             The post being checked.
    #//
    return apply_filters("use_block_editor_for_post", use_block_editor, post)
# end def use_block_editor_for_post
#// 
#// Return whether a post type is compatible with the block editor.
#// 
#// The block editor depends on the REST API, and if the post type is not shown in the
#// REST API, then it won't work with the block editor.
#// 
#// @since 5.0.0
#// 
#// @param string $post_type The post type.
#// @return bool Whether the post type can be edited with the block editor.
#//
def use_block_editor_for_post_type(post_type=None, *args_):
    
    if (not post_type_exists(post_type)):
        return False
    # end if
    if (not post_type_supports(post_type, "editor")):
        return False
    # end if
    post_type_object = get_post_type_object(post_type)
    if post_type_object and (not post_type_object.show_in_rest):
        return False
    # end if
    #// 
    #// Filter whether a post is able to be edited in the block editor.
    #// 
    #// @since 5.0.0
    #// 
    #// @param bool   $use_block_editor  Whether the post type can be edited or not. Default true.
    #// @param string $post_type         The post type being checked.
    #//
    return apply_filters("use_block_editor_for_post_type", True, post_type)
# end def use_block_editor_for_post_type
#// 
#// Returns all the block categories that will be shown in the block editor.
#// 
#// @since 5.0.0
#// 
#// @param WP_Post $post Post object.
#// @return array[] Array of block categories.
#//
def get_block_categories(post=None, *args_):
    
    default_categories = Array(Array({"slug": "common", "title": __("Common Blocks"), "icon": None}), Array({"slug": "formatting", "title": __("Formatting"), "icon": None}), Array({"slug": "layout", "title": __("Layout Elements"), "icon": None}), Array({"slug": "widgets", "title": __("Widgets"), "icon": None}), Array({"slug": "embed", "title": __("Embeds"), "icon": None}), Array({"slug": "reusable", "title": __("Reusable Blocks"), "icon": None}))
    #// 
    #// Filter the default array of block categories.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array[] $default_categories Array of block categories.
    #// @param WP_Post $post               Post being loaded.
    #//
    return apply_filters("block_categories", default_categories, post)
# end def get_block_categories
#// 
#// Prepares server-registered blocks for the block editor.
#// 
#// Returns an associative array of registered block data keyed by block name. Data includes properties
#// of a block relevant for client registration.
#// 
#// @since 5.0.0
#// 
#// @return array An associative array of registered block data.
#//
def get_block_editor_server_block_settings(*args_):
    
    block_registry = WP_Block_Type_Registry.get_instance()
    blocks = Array()
    keys_to_pick = Array("title", "description", "icon", "category", "keywords", "parent", "supports", "attributes", "styles")
    for block_name,block_type in block_registry.get_all_registered():
        for key in keys_to_pick:
            if (not (php_isset(lambda : block_type.key))):
                continue
            # end if
            if (not (php_isset(lambda : blocks[block_name]))):
                blocks[block_name] = Array()
            # end if
            blocks[block_name][key] = block_type.key
        # end for
    # end for
    return blocks
# end def get_block_editor_server_block_settings
#// 
#// Renders the meta boxes forms.
#// 
#// @since 5.0.0
#//
def the_block_editor_meta_boxes(*args_):
    
    global post,current_screen,wp_meta_boxes
    php_check_if_defined("post","current_screen","wp_meta_boxes")
    #// Handle meta box state.
    _original_meta_boxes = wp_meta_boxes
    #// 
    #// Fires right before the meta boxes are rendered.
    #// 
    #// This allows for the filtering of meta box data, that should already be
    #// present by this point. Do not use as a means of adding meta box data.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array $wp_meta_boxes Global meta box state.
    #//
    wp_meta_boxes = apply_filters("filter_block_editor_meta_boxes", wp_meta_boxes)
    locations = Array("side", "normal", "advanced")
    priorities = Array("high", "sorted", "core", "default", "low")
    pass
    php_print(" <form class=\"metabox-base-form\">\n    ")
    the_block_editor_meta_box_post_form_hidden_fields(post)
    php_print(" </form>\n   <form id=\"toggle-custom-fields-form\" method=\"post\" action=\"")
    php_print(esc_attr(admin_url("post.php")))
    php_print("\">\n        ")
    wp_nonce_field("toggle-custom-fields")
    php_print("     <input type=\"hidden\" name=\"action\" value=\"toggle-custom-fields\" />\n  </form>\n   ")
    for location in locations:
        php_print("     <form class=\"metabox-location-")
        php_print(esc_attr(location))
        php_print("""\" onsubmit=\"return false;\">
        <div id=\"poststuff\" class=\"sidebar-open\">
        <div id=\"postbox-container-2\" class=\"postbox-container\">
        """)
        do_meta_boxes(current_screen, location, post)
        php_print("""               </div>
        </div>
        </form>
        """)
    # end for
    php_print(" ")
    meta_boxes_per_location = Array()
    for location in locations:
        meta_boxes_per_location[location] = Array()
        if (not (php_isset(lambda : wp_meta_boxes[current_screen.id][location]))):
            continue
        # end if
        for priority in priorities:
            if (not (php_isset(lambda : wp_meta_boxes[current_screen.id][location][priority]))):
                continue
            # end if
            meta_boxes = wp_meta_boxes[current_screen.id][location][priority]
            for meta_box in meta_boxes:
                if False == meta_box or (not meta_box["title"]):
                    continue
                # end if
                #// If a meta box is just here for back compat, don't show it in the block editor.
                if (php_isset(lambda : meta_box["args"]["__back_compat_meta_box"])) and meta_box["args"]["__back_compat_meta_box"]:
                    continue
                # end if
                meta_boxes_per_location[location][-1] = Array({"id": meta_box["id"], "title": meta_box["title"]})
            # end for
        # end for
    # end for
    #// 
    #// Sadly we probably can not add this data directly into editor settings.
    #// 
    #// Some meta boxes need admin_head to fire for meta box registry.
    #// admin_head fires after admin_enqueue_scripts, which is where we create our
    #// editor instance.
    #//
    script = "window._wpLoadBlockEditor.then( function() {\n        wp.data.dispatch( 'core/edit-post' ).setAvailableMetaBoxesPerLocation( " + wp_json_encode(meta_boxes_per_location) + " );\n } );"
    wp_add_inline_script("wp-edit-post", script)
    #// 
    #// When `wp-edit-post` is output in the `<head>`, the inline script needs to be manually printed. Otherwise,
    #// meta boxes will not display because inline scripts for `wp-edit-post` will not be printed again after this point.
    #//
    if wp_script_is("wp-edit-post", "done"):
        printf("""<script type='text/javascript'>
        %s
        </script>
        """, php_trim(script))
    # end if
    #// 
    #// If the 'postcustom' meta box is enabled, then we need to perform some
    #// extra initialization on it.
    #//
    enable_custom_fields = bool(get_user_meta(get_current_user_id(), "enable_custom_fields", True))
    if enable_custom_fields:
        script = str("""( function( $ ) {\n         if ( $('#postcustom').length ) {\n              $( '#the-list' ).wpList( {\n                    addBefore: function( s ) {\n                        s.data += '&post_id=""") + str(post.ID) + str("""';\n                       return s;\n                 },\n                    addAfter: function() {\n                        $('table#list-table').show();\n                 }\n             });\n           }\n     } )( jQuery );""")
        wp_enqueue_script("wp-lists")
        wp_add_inline_script("wp-lists", script)
    # end if
    #// Reset meta box data.
    wp_meta_boxes = _original_meta_boxes
# end def the_block_editor_meta_boxes
#// 
#// Renders the hidden form required for the meta boxes form.
#// 
#// @since 5.0.0
#// 
#// @param WP_Post $post Current post object.
#//
def the_block_editor_meta_box_post_form_hidden_fields(post=None, *args_):
    
    form_extra = ""
    if "auto-draft" == post.post_status:
        form_extra += "<input type='hidden' id='auto_draft' name='auto_draft' value='1' />"
    # end if
    form_action = "editpost"
    nonce_action = "update-post_" + post.ID
    form_extra += "<input type='hidden' id='post_ID' name='post_ID' value='" + esc_attr(post.ID) + "' />"
    referer = wp_get_referer()
    current_user = wp_get_current_user()
    user_id = current_user.ID
    wp_nonce_field(nonce_action)
    #// 
    #// Some meta boxes hook into these actions to add hidden input fields in the classic post form. For backwards
    #// compatibility, we can capture the output from these actions, and extract the hidden input fields.
    #//
    ob_start()
    #// This filter is documented in wp-admin/edit-form-advanced.php
    do_action("edit_form_after_title", post)
    #// This filter is documented in wp-admin/edit-form-advanced.php
    do_action("edit_form_advanced", post)
    classic_output = ob_get_clean()
    classic_elements = wp_html_split(classic_output)
    hidden_inputs = ""
    for element in classic_elements:
        if 0 != php_strpos(element, "<input "):
            continue
        # end if
        if php_preg_match("/\\stype=['\"]hidden['\"]\\s/", element):
            php_print(element)
        # end if
    # end for
    php_print(" <input type=\"hidden\" id=\"user-id\" name=\"user_ID\" value=\"")
    php_print(int(user_id))
    php_print("\" />\n  <input type=\"hidden\" id=\"hiddenaction\" name=\"action\" value=\"")
    php_print(esc_attr(form_action))
    php_print("\" />\n  <input type=\"hidden\" id=\"originalaction\" name=\"originalaction\" value=\"")
    php_print(esc_attr(form_action))
    php_print("\" />\n  <input type=\"hidden\" id=\"post_type\" name=\"post_type\" value=\"")
    php_print(esc_attr(post.post_type))
    php_print("\" />\n  <input type=\"hidden\" id=\"original_post_status\" name=\"original_post_status\" value=\"")
    php_print(esc_attr(post.post_status))
    php_print("\" />\n  <input type=\"hidden\" id=\"referredby\" name=\"referredby\" value=\"")
    php_print(esc_url(referer) if referer else "")
    php_print("\" />\n\n    ")
    if "draft" != get_post_status(post):
        wp_original_referer_field(True, "previous")
    # end if
    php_print(form_extra)
    wp_nonce_field("meta-box-order", "meta-box-order-nonce", False)
    wp_nonce_field("closedpostboxes", "closedpostboxesnonce", False)
    #// Permalink title nonce.
    wp_nonce_field("samplepermalink", "samplepermalinknonce", False)
    #// 
    #// Add hidden input fields to the meta box save form.
    #// 
    #// Hook into this action to print `<input type="hidden" ... />` fields, which will be POSTed back to
    #// the server when meta boxes are saved.
    #// 
    #// @since 5.0.0
    #// 
    #// @param WP_Post $post The post that is being edited.
    #//
    do_action("block_editor_meta_box_hidden_fields", post)
# end def the_block_editor_meta_box_post_form_hidden_fields
