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
def _wp_translate_postdata(update_=None, post_data_=None, *_args_):
    if update_ is None:
        update_ = False
    # end if
    if post_data_ is None:
        post_data_ = None
    # end if
    
    if php_empty(lambda : post_data_):
        post_data_ = PHP_POST
    # end if
    if update_:
        post_data_["ID"] = php_int(post_data_["post_ID"])
    # end if
    ptype_ = get_post_type_object(post_data_["post_type"])
    if update_ and (not current_user_can("edit_post", post_data_["ID"])):
        if "page" == post_data_["post_type"]:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to edit pages as this user.")))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to edit posts as this user.")))
        # end if
    elif (not update_) and (not current_user_can(ptype_.cap.create_posts)):
        if "page" == post_data_["post_type"]:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to create pages as this user.")))
        else:
            return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to create posts as this user.")))
        # end if
    # end if
    if (php_isset(lambda : post_data_["content"])):
        post_data_["post_content"] = post_data_["content"]
    # end if
    if (php_isset(lambda : post_data_["excerpt"])):
        post_data_["post_excerpt"] = post_data_["excerpt"]
    # end if
    if (php_isset(lambda : post_data_["parent_id"])):
        post_data_["post_parent"] = php_int(post_data_["parent_id"])
    # end if
    if (php_isset(lambda : post_data_["trackback_url"])):
        post_data_["to_ping"] = post_data_["trackback_url"]
    # end if
    post_data_["user_ID"] = get_current_user_id()
    if (not php_empty(lambda : post_data_["post_author_override"])):
        post_data_["post_author"] = php_int(post_data_["post_author_override"])
    else:
        if (not php_empty(lambda : post_data_["post_author"])):
            post_data_["post_author"] = php_int(post_data_["post_author"])
        else:
            post_data_["post_author"] = php_int(post_data_["user_ID"])
        # end if
    # end if
    if (php_isset(lambda : post_data_["user_ID"])) and post_data_["post_author"] != post_data_["user_ID"] and (not current_user_can(ptype_.cap.edit_others_posts)):
        if update_:
            if "page" == post_data_["post_type"]:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to edit pages as this user.")))
            else:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to edit posts as this user.")))
            # end if
        else:
            if "page" == post_data_["post_type"]:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_pages", __("Sorry, you are not allowed to create pages as this user.")))
            else:
                return php_new_class("WP_Error", lambda : WP_Error("edit_others_posts", __("Sorry, you are not allowed to create posts as this user.")))
            # end if
        # end if
    # end if
    if (not php_empty(lambda : post_data_["post_status"])):
        post_data_["post_status"] = sanitize_key(post_data_["post_status"])
        #// No longer an auto-draft.
        if "auto-draft" == post_data_["post_status"]:
            post_data_["post_status"] = "draft"
        # end if
        if (not get_post_status_object(post_data_["post_status"])):
            post_data_["post_status"] = None
        # end if
    # end if
    #// What to do based on which button they pressed.
    if (php_isset(lambda : post_data_["saveasdraft"])) and "" != post_data_["saveasdraft"]:
        post_data_["post_status"] = "draft"
    # end if
    if (php_isset(lambda : post_data_["saveasprivate"])) and "" != post_data_["saveasprivate"]:
        post_data_["post_status"] = "private"
    # end if
    if (php_isset(lambda : post_data_["publish"])) and "" != post_data_["publish"] and (not (php_isset(lambda : post_data_["post_status"]))) or "private" != post_data_["post_status"]:
        post_data_["post_status"] = "publish"
    # end if
    if (php_isset(lambda : post_data_["advanced"])) and "" != post_data_["advanced"]:
        post_data_["post_status"] = "draft"
    # end if
    if (php_isset(lambda : post_data_["pending"])) and "" != post_data_["pending"]:
        post_data_["post_status"] = "pending"
    # end if
    if (php_isset(lambda : post_data_["ID"])):
        post_id_ = post_data_["ID"]
    else:
        post_id_ = False
    # end if
    previous_status_ = get_post_field("post_status", post_id_) if post_id_ else False
    if (php_isset(lambda : post_data_["post_status"])) and "private" == post_data_["post_status"] and (not current_user_can(ptype_.cap.publish_posts)):
        post_data_["post_status"] = previous_status_ if previous_status_ else "pending"
    # end if
    published_statuses_ = Array("publish", "future")
    #// Posts 'submitted for approval' are submitted to $_POST the same as if they were being published.
    #// Change status from 'publish' to 'pending' if user lacks permissions to publish or to resave published posts.
    if (php_isset(lambda : post_data_["post_status"])) and php_in_array(post_data_["post_status"], published_statuses_) and (not current_user_can(ptype_.cap.publish_posts)):
        if (not php_in_array(previous_status_, published_statuses_)) or (not current_user_can("edit_post", post_id_)):
            post_data_["post_status"] = "pending"
        # end if
    # end if
    if (not (php_isset(lambda : post_data_["post_status"]))):
        post_data_["post_status"] = "draft" if "auto-draft" == previous_status_ else previous_status_
    # end if
    if (php_isset(lambda : post_data_["post_password"])) and (not current_user_can(ptype_.cap.publish_posts)):
        post_data_["post_password"] = None
    # end if
    if (not (php_isset(lambda : post_data_["comment_status"]))):
        post_data_["comment_status"] = "closed"
    # end if
    if (not (php_isset(lambda : post_data_["ping_status"]))):
        post_data_["ping_status"] = "closed"
    # end if
    for timeunit_ in Array("aa", "mm", "jj", "hh", "mn"):
        if (not php_empty(lambda : post_data_["hidden_" + timeunit_])) and post_data_["hidden_" + timeunit_] != post_data_[timeunit_]:
            post_data_["edit_date"] = "1"
            break
        # end if
    # end for
    if (not php_empty(lambda : post_data_["edit_date"])):
        aa_ = post_data_["aa"]
        mm_ = post_data_["mm"]
        jj_ = post_data_["jj"]
        hh_ = post_data_["hh"]
        mn_ = post_data_["mn"]
        ss_ = post_data_["ss"]
        aa_ = gmdate("Y") if aa_ <= 0 else aa_
        mm_ = gmdate("n") if mm_ <= 0 else mm_
        jj_ = 31 if jj_ > 31 else jj_
        jj_ = gmdate("j") if jj_ <= 0 else jj_
        hh_ = hh_ - 24 if hh_ > 23 else hh_
        mn_ = mn_ - 60 if mn_ > 59 else mn_
        ss_ = ss_ - 60 if ss_ > 59 else ss_
        post_data_["post_date"] = php_sprintf("%04d-%02d-%02d %02d:%02d:%02d", aa_, mm_, jj_, hh_, mn_, ss_)
        valid_date_ = wp_checkdate(mm_, jj_, aa_, post_data_["post_date"])
        if (not valid_date_):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_date", __("Invalid date.")))
        # end if
        post_data_["post_date_gmt"] = get_gmt_from_date(post_data_["post_date"])
    # end if
    if (php_isset(lambda : post_data_["post_category"])):
        category_object_ = get_taxonomy("category")
        if (not current_user_can(category_object_.cap.assign_terms)):
            post_data_["post_category"] = None
        # end if
    # end if
    return post_data_
# end def _wp_translate_postdata
#// 
#// Returns only allowed post data fields
#// 
#// @since 5.0.1
#// 
#// @param array $post_data Array of post data. Defaults to the contents of $_POST.
#// @return array|WP_Error Array of post data on success, WP_Error on failure.
#//
def _wp_get_allowed_postdata(post_data_=None, *_args_):
    if post_data_ is None:
        post_data_ = None
    # end if
    
    if php_empty(lambda : post_data_):
        post_data_ = PHP_POST
    # end if
    #// Pass through errors.
    if is_wp_error(post_data_):
        return post_data_
    # end if
    return php_array_diff_key(post_data_, php_array_flip(Array("meta_input", "file", "guid")))
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
def edit_post(post_data_=None, *_args_):
    if post_data_ is None:
        post_data_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : post_data_):
        post_data_ = PHP_POST
    # end if
    post_data_["filter"] = None
    post_ID_ = php_int(post_data_["post_ID"])
    post_ = get_post(post_ID_)
    post_data_["post_type"] = post_.post_type
    post_data_["post_mime_type"] = post_.post_mime_type
    if (not php_empty(lambda : post_data_["post_status"])):
        post_data_["post_status"] = sanitize_key(post_data_["post_status"])
        if "inherit" == post_data_["post_status"]:
            post_data_["post_status"] = None
        # end if
    # end if
    ptype_ = get_post_type_object(post_data_["post_type"])
    if (not current_user_can("edit_post", post_ID_)):
        if "page" == post_data_["post_type"]:
            wp_die(__("Sorry, you are not allowed to edit this page."))
        else:
            wp_die(__("Sorry, you are not allowed to edit this post."))
        # end if
    # end if
    if post_type_supports(ptype_.name, "revisions"):
        revisions_ = wp_get_post_revisions(post_ID_, Array({"order": "ASC", "posts_per_page": 1}))
        revision_ = current(revisions_)
        #// Check if the revisions have been upgraded.
        if revisions_ and _wp_get_post_revision_version(revision_) < 1:
            _wp_upgrade_revisions_of_post(post_, wp_get_post_revisions(post_ID_))
        # end if
    # end if
    if (php_isset(lambda : post_data_["visibility"])):
        for case in Switch(post_data_["visibility"]):
            if case("public"):
                post_data_["post_password"] = ""
                break
            # end if
            if case("password"):
                post_data_["sticky"] = None
                break
            # end if
            if case("private"):
                post_data_["post_status"] = "private"
                post_data_["post_password"] = ""
                post_data_["sticky"] = None
                break
            # end if
        # end for
    # end if
    post_data_ = _wp_translate_postdata(True, post_data_)
    if is_wp_error(post_data_):
        wp_die(post_data_.get_error_message())
    # end if
    translated_ = _wp_get_allowed_postdata(post_data_)
    #// Post formats.
    if (php_isset(lambda : post_data_["post_format"])):
        set_post_format(post_ID_, post_data_["post_format"])
    # end if
    format_meta_urls_ = Array("url", "link_url", "quote_source_url")
    for format_meta_url_ in format_meta_urls_:
        keyed_ = "_format_" + format_meta_url_
        if (php_isset(lambda : post_data_[keyed_])):
            update_post_meta(post_ID_, keyed_, wp_slash(esc_url_raw(wp_unslash(post_data_[keyed_]))))
        # end if
    # end for
    format_keys_ = Array("quote", "quote_source_name", "image", "gallery", "audio_embed", "video_embed")
    for key_ in format_keys_:
        keyed_ = "_format_" + key_
        if (php_isset(lambda : post_data_[keyed_])):
            if current_user_can("unfiltered_html"):
                update_post_meta(post_ID_, keyed_, post_data_[keyed_])
            else:
                update_post_meta(post_ID_, keyed_, wp_filter_post_kses(post_data_[keyed_]))
            # end if
        # end if
    # end for
    if "attachment" == post_data_["post_type"] and php_preg_match("#^(audio|video)/#", post_data_["post_mime_type"]):
        id3data_ = wp_get_attachment_metadata(post_ID_)
        if (not php_is_array(id3data_)):
            id3data_ = Array()
        # end if
        for key_,label_ in wp_get_attachment_id3_keys(post_, "edit").items():
            if (php_isset(lambda : post_data_["id3_" + key_])):
                id3data_[key_] = sanitize_text_field(wp_unslash(post_data_["id3_" + key_]))
            # end if
        # end for
        wp_update_attachment_metadata(post_ID_, id3data_)
    # end if
    #// Meta stuff.
    if (php_isset(lambda : post_data_["meta"])) and post_data_["meta"]:
        for key_,value_ in post_data_["meta"].items():
            meta_ = get_post_meta_by_id(key_)
            if (not meta_):
                continue
            # end if
            if meta_.post_id != post_ID_:
                continue
            # end if
            if is_protected_meta(meta_.meta_key, "post") or (not current_user_can("edit_post_meta", post_ID_, meta_.meta_key)):
                continue
            # end if
            if is_protected_meta(value_["key"], "post") or (not current_user_can("edit_post_meta", post_ID_, value_["key"])):
                continue
            # end if
            update_meta(key_, value_["key"], value_["value"])
        # end for
    # end if
    if (php_isset(lambda : post_data_["deletemeta"])) and post_data_["deletemeta"]:
        for key_,value_ in post_data_["deletemeta"].items():
            meta_ = get_post_meta_by_id(key_)
            if (not meta_):
                continue
            # end if
            if meta_.post_id != post_ID_:
                continue
            # end if
            if is_protected_meta(meta_.meta_key, "post") or (not current_user_can("delete_post_meta", post_ID_, meta_.meta_key)):
                continue
            # end if
            delete_meta(key_)
        # end for
    # end if
    #// Attachment stuff.
    if "attachment" == post_data_["post_type"]:
        if (php_isset(lambda : post_data_["_wp_attachment_image_alt"])):
            image_alt_ = wp_unslash(post_data_["_wp_attachment_image_alt"])
            if get_post_meta(post_ID_, "_wp_attachment_image_alt", True) != image_alt_:
                image_alt_ = wp_strip_all_tags(image_alt_, True)
                #// update_post_meta() expects slashed.
                update_post_meta(post_ID_, "_wp_attachment_image_alt", wp_slash(image_alt_))
            # end if
        # end if
        attachment_data_ = post_data_["attachments"][post_ID_] if (php_isset(lambda : post_data_["attachments"][post_ID_])) else Array()
        #// This filter is documented in wp-admin/includes/media.php
        translated_ = apply_filters("attachment_fields_to_save", translated_, attachment_data_)
    # end if
    #// Convert taxonomy input to term IDs, to avoid ambiguity.
    if (php_isset(lambda : post_data_["tax_input"])):
        for taxonomy_,terms_ in post_data_["tax_input"].items():
            tax_object_ = get_taxonomy(taxonomy_)
            if tax_object_ and (php_isset(lambda : tax_object_.meta_box_sanitize_cb)):
                translated_["tax_input"][taxonomy_] = call_user_func_array(tax_object_.meta_box_sanitize_cb, Array(taxonomy_, terms_))
            # end if
        # end for
    # end if
    add_meta(post_ID_)
    update_post_meta(post_ID_, "_edit_last", get_current_user_id())
    success_ = wp_update_post(translated_)
    #// If the save failed, see if we can sanity check the main fields and try again.
    if (not success_) and php_is_callable(Array(wpdb_, "strip_invalid_text_for_column")):
        fields_ = Array("post_title", "post_content", "post_excerpt")
        for field_ in fields_:
            if (php_isset(lambda : translated_[field_])):
                translated_[field_] = wpdb_.strip_invalid_text_for_column(wpdb_.posts, field_, translated_[field_])
            # end if
        # end for
        wp_update_post(translated_)
    # end if
    #// Now that we have an ID we can fix any attachment anchor hrefs.
    _fix_attachment_links(post_ID_)
    wp_set_post_lock(post_ID_)
    if current_user_can(ptype_.cap.edit_others_posts) and current_user_can(ptype_.cap.publish_posts):
        if (not php_empty(lambda : post_data_["sticky"])):
            stick_post(post_ID_)
        else:
            unstick_post(post_ID_)
        # end if
    # end if
    return post_ID_
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
def bulk_edit_posts(post_data_=None, *_args_):
    if post_data_ is None:
        post_data_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : post_data_):
        post_data_ = PHP_POST
    # end if
    if (php_isset(lambda : post_data_["post_type"])):
        ptype_ = get_post_type_object(post_data_["post_type"])
    else:
        ptype_ = get_post_type_object("post")
    # end if
    if (not current_user_can(ptype_.cap.edit_posts)):
        if "page" == ptype_.name:
            wp_die(__("Sorry, you are not allowed to edit pages."))
        else:
            wp_die(__("Sorry, you are not allowed to edit posts."))
        # end if
    # end if
    if -1 == post_data_["_status"]:
        post_data_["post_status"] = None
        post_data_["post_status"] = None
    else:
        post_data_["post_status"] = post_data_["_status"]
    # end if
    post_data_["_status"] = None
    if (not php_empty(lambda : post_data_["post_status"])):
        post_data_["post_status"] = sanitize_key(post_data_["post_status"])
        if "inherit" == post_data_["post_status"]:
            post_data_["post_status"] = None
        # end if
    # end if
    post_IDs_ = php_array_map("intval", post_data_["post"])
    reset_ = Array("post_author", "post_status", "post_password", "post_parent", "page_template", "comment_status", "ping_status", "keep_private", "tax_input", "post_category", "sticky", "post_format")
    for field_ in reset_:
        if (php_isset(lambda : post_data_[field_])) and "" == post_data_[field_] or -1 == post_data_[field_]:
            post_data_[field_] = None
        # end if
    # end for
    if (php_isset(lambda : post_data_["post_category"])):
        if php_is_array(post_data_["post_category"]) and (not php_empty(lambda : post_data_["post_category"])):
            new_cats_ = php_array_map("absint", post_data_["post_category"])
        else:
            post_data_["post_category"] = None
        # end if
    # end if
    tax_input_ = Array()
    if (php_isset(lambda : post_data_["tax_input"])):
        for tax_name_,terms_ in post_data_["tax_input"].items():
            if php_empty(lambda : terms_):
                continue
            # end if
            if is_taxonomy_hierarchical(tax_name_):
                tax_input_[tax_name_] = php_array_map("absint", terms_)
            else:
                comma_ = _x(",", "tag delimiter")
                if "," != comma_:
                    terms_ = php_str_replace(comma_, ",", terms_)
                # end if
                tax_input_[tax_name_] = php_explode(",", php_trim(terms_, " \n  \r ,"))
            # end if
        # end for
    # end if
    if (php_isset(lambda : post_data_["post_parent"])) and php_int(post_data_["post_parent"]):
        parent_ = php_int(post_data_["post_parent"])
        pages_ = wpdb_.get_results(str("SELECT ID, post_parent FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'page'"))
        children_ = Array()
        i_ = 0
        while i_ < 50 and parent_ > 0:
            
            children_[-1] = parent_
            for page_ in pages_:
                if page_.ID == parent_:
                    parent_ = page_.post_parent
                    break
                # end if
            # end for
            i_ += 1
        # end while
    # end if
    updated_ = Array()
    skipped_ = Array()
    locked_ = Array()
    shared_post_data_ = post_data_
    for post_ID_ in post_IDs_:
        #// Start with fresh post data with each iteration.
        post_data_ = shared_post_data_
        post_type_object_ = get_post_type_object(get_post_type(post_ID_))
        if (not (php_isset(lambda : post_type_object_))) or (php_isset(lambda : children_)) and php_in_array(post_ID_, children_) or (not current_user_can("edit_post", post_ID_)):
            skipped_[-1] = post_ID_
            continue
        # end if
        if wp_check_post_lock(post_ID_):
            locked_[-1] = post_ID_
            continue
        # end if
        post_ = get_post(post_ID_)
        tax_names_ = get_object_taxonomies(post_)
        for tax_name_ in tax_names_:
            taxonomy_obj_ = get_taxonomy(tax_name_)
            if (php_isset(lambda : tax_input_[tax_name_])) and current_user_can(taxonomy_obj_.cap.assign_terms):
                new_terms_ = tax_input_[tax_name_]
            else:
                new_terms_ = Array()
            # end if
            if taxonomy_obj_.hierarchical:
                current_terms_ = wp_get_object_terms(post_ID_, tax_name_, Array({"fields": "ids"}))
            else:
                current_terms_ = wp_get_object_terms(post_ID_, tax_name_, Array({"fields": "names"}))
            # end if
            post_data_["tax_input"][tax_name_] = php_array_merge(current_terms_, new_terms_)
        # end for
        if (php_isset(lambda : new_cats_)) and php_in_array("category", tax_names_):
            cats_ = wp_get_post_categories(post_ID_)
            post_data_["post_category"] = array_unique(php_array_merge(cats_, new_cats_))
            post_data_["tax_input"]["category"] = None
        # end if
        post_data_["post_ID"] = post_ID_
        post_data_["post_type"] = post_.post_type
        post_data_["post_mime_type"] = post_.post_mime_type
        for field_ in Array("comment_status", "ping_status", "post_author"):
            if (not (php_isset(lambda : post_data_[field_]))):
                post_data_[field_] = post_.field_
            # end if
        # end for
        post_data_ = _wp_translate_postdata(True, post_data_)
        if is_wp_error(post_data_):
            skipped_[-1] = post_ID_
            continue
        # end if
        post_data_ = _wp_get_allowed_postdata(post_data_)
        if (php_isset(lambda : shared_post_data_["post_format"])):
            set_post_format(post_ID_, shared_post_data_["post_format"])
        # end if
        post_data_["tax_input"]["post_format"] = None
        updated_[-1] = wp_update_post(post_data_)
        if (php_isset(lambda : post_data_["sticky"])) and current_user_can(ptype_.cap.edit_others_posts):
            if "sticky" == post_data_["sticky"]:
                stick_post(post_ID_)
            else:
                unstick_post(post_ID_)
            # end if
        # end if
    # end for
    return Array({"updated": updated_, "skipped": skipped_, "locked": locked_})
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
def get_default_post_to_edit(post_type_="post", create_in_db_=None, *_args_):
    if create_in_db_ is None:
        create_in_db_ = False
    # end if
    
    post_title_ = ""
    if (not php_empty(lambda : PHP_REQUEST["post_title"])):
        post_title_ = esc_html(wp_unslash(PHP_REQUEST["post_title"]))
    # end if
    post_content_ = ""
    if (not php_empty(lambda : PHP_REQUEST["content"])):
        post_content_ = esc_html(wp_unslash(PHP_REQUEST["content"]))
    # end if
    post_excerpt_ = ""
    if (not php_empty(lambda : PHP_REQUEST["excerpt"])):
        post_excerpt_ = esc_html(wp_unslash(PHP_REQUEST["excerpt"]))
    # end if
    if create_in_db_:
        post_id_ = wp_insert_post(Array({"post_title": __("Auto Draft"), "post_type": post_type_, "post_status": "auto-draft"}))
        post_ = get_post(post_id_)
        if current_theme_supports("post-formats") and post_type_supports(post_.post_type, "post-formats") and get_option("default_post_format"):
            set_post_format(post_, get_option("default_post_format"))
        # end if
        #// Schedule auto-draft cleanup.
        if (not wp_next_scheduled("wp_scheduled_auto_draft_delete")):
            wp_schedule_event(time(), "daily", "wp_scheduled_auto_draft_delete")
        # end if
    else:
        post_ = php_new_class("stdClass", lambda : stdClass())
        post_.ID = 0
        post_.post_author = ""
        post_.post_date = ""
        post_.post_date_gmt = ""
        post_.post_password = ""
        post_.post_name = ""
        post_.post_type = post_type_
        post_.post_status = "draft"
        post_.to_ping = ""
        post_.pinged = ""
        post_.comment_status = get_default_comment_status(post_type_)
        post_.ping_status = get_default_comment_status(post_type_, "pingback")
        post_.post_pingback = get_option("default_pingback_flag")
        post_.post_category = get_option("default_category")
        post_.page_template = "default"
        post_.post_parent = 0
        post_.menu_order = 0
        post_ = php_new_class("WP_Post", lambda : WP_Post(post_))
    # end if
    #// 
    #// Filters the default post content initially used in the "Write Post" form.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $post_content Default post content.
    #// @param WP_Post $post         Post object.
    #//
    post_.post_content = php_str(apply_filters("default_content", post_content_, post_))
    #// 
    #// Filters the default post title initially used in the "Write Post" form.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $post_title Default post title.
    #// @param WP_Post $post       Post object.
    #//
    post_.post_title = php_str(apply_filters("default_title", post_title_, post_))
    #// 
    #// Filters the default post excerpt initially used in the "Write Post" form.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string  $post_excerpt Default post excerpt.
    #// @param WP_Post $post         Post object.
    #//
    post_.post_excerpt = php_str(apply_filters("default_excerpt", post_excerpt_, post_))
    return post_
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
def post_exists(title_=None, content_="", date_="", type_="", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_title_ = wp_unslash(sanitize_post_field("post_title", title_, 0, "db"))
    post_content_ = wp_unslash(sanitize_post_field("post_content", content_, 0, "db"))
    post_date_ = wp_unslash(sanitize_post_field("post_date", date_, 0, "db"))
    post_type_ = wp_unslash(sanitize_post_field("post_type", type_, 0, "db"))
    query_ = str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE 1=1")
    args_ = Array()
    if (not php_empty(lambda : date_)):
        query_ += " AND post_date = %s"
        args_[-1] = post_date_
    # end if
    if (not php_empty(lambda : title_)):
        query_ += " AND post_title = %s"
        args_[-1] = post_title_
    # end if
    if (not php_empty(lambda : content_)):
        query_ += " AND post_content = %s"
        args_[-1] = post_content_
    # end if
    if (not php_empty(lambda : type_)):
        query_ += " AND post_type = %s"
        args_[-1] = post_type_
    # end if
    if (not php_empty(lambda : args_)):
        return php_int(wpdb_.get_var(wpdb_.prepare(query_, args_)))
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
def wp_write_post(*_args_):
    
    global PHP_POST
    if (php_isset(lambda : PHP_POST["post_type"])):
        ptype_ = get_post_type_object(PHP_POST["post_type"])
    else:
        ptype_ = get_post_type_object("post")
    # end if
    if (not current_user_can(ptype_.cap.edit_posts)):
        if "page" == ptype_.name:
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
    translated_ = _wp_translate_postdata(False)
    if is_wp_error(translated_):
        return translated_
    # end if
    translated_ = _wp_get_allowed_postdata(translated_)
    #// Create the post.
    post_ID_ = wp_insert_post(translated_)
    if is_wp_error(post_ID_):
        return post_ID_
    # end if
    if php_empty(lambda : post_ID_):
        return 0
    # end if
    add_meta(post_ID_)
    add_post_meta(post_ID_, "_edit_last", PHP_GLOBALS["current_user"].ID)
    #// Now that we have an ID we can fix any attachment anchor hrefs.
    _fix_attachment_links(post_ID_)
    wp_set_post_lock(post_ID_)
    return post_ID_
# end def wp_write_post
#// 
#// Calls wp_write_post() and handles the errors.
#// 
#// @since 2.0.0
#// 
#// @return int|null
#//
def write_post(*_args_):
    
    
    result_ = wp_write_post()
    if is_wp_error(result_):
        wp_die(result_.get_error_message())
    else:
        return result_
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
def add_meta(post_ID_=None, *_args_):
    
    
    post_ID_ = php_int(post_ID_)
    metakeyselect_ = wp_unslash(php_trim(PHP_POST["metakeyselect"])) if (php_isset(lambda : PHP_POST["metakeyselect"])) else ""
    metakeyinput_ = wp_unslash(php_trim(PHP_POST["metakeyinput"])) if (php_isset(lambda : PHP_POST["metakeyinput"])) else ""
    metavalue_ = PHP_POST["metavalue"] if (php_isset(lambda : PHP_POST["metavalue"])) else ""
    if php_is_string(metavalue_):
        metavalue_ = php_trim(metavalue_)
    # end if
    if "#NONE#" != metakeyselect_ and (not php_empty(lambda : metakeyselect_)) or (not php_empty(lambda : metakeyinput_)):
        #// 
        #// We have a key/value pair. If both the select and the input
        #// for the key have data, the input takes precedence.
        #//
        if "#NONE#" != metakeyselect_:
            metakey_ = metakeyselect_
        # end if
        if metakeyinput_:
            metakey_ = metakeyinput_
            pass
        # end if
        if is_protected_meta(metakey_, "post") or (not current_user_can("add_post_meta", post_ID_, metakey_)):
            return False
        # end if
        metakey_ = wp_slash(metakey_)
        return add_post_meta(post_ID_, metakey_, metavalue_)
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
def delete_meta(mid_=None, *_args_):
    
    
    return delete_metadata_by_mid("post", mid_)
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
def get_meta_keys(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    keys_ = wpdb_.get_col(str("\n           SELECT meta_key\n           FROM ") + str(wpdb_.postmeta) + str("\n         GROUP BY meta_key\n         ORDER BY meta_key"))
    return keys_
# end def get_meta_keys
#// 
#// Get post meta data by meta ID.
#// 
#// @since 2.1.0
#// 
#// @param int $mid
#// @return object|bool
#//
def get_post_meta_by_id(mid_=None, *_args_):
    
    
    return get_metadata_by_mid("post", mid_)
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
def has_meta(postid_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    return wpdb_.get_results(wpdb_.prepare(str("SELECT meta_key, meta_value, meta_id, post_id\n         FROM ") + str(wpdb_.postmeta) + str(" WHERE post_id = %d\n          ORDER BY meta_key,meta_id"), postid_), ARRAY_A)
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
def update_meta(meta_id_=None, meta_key_=None, meta_value_=None, *_args_):
    
    
    meta_key_ = wp_unslash(meta_key_)
    meta_value_ = wp_unslash(meta_value_)
    return update_metadata_by_mid("post", meta_id_, meta_value_, meta_key_)
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
def _fix_attachment_links(post_=None, *_args_):
    
    
    post_ = get_post(post_, ARRAY_A)
    content_ = post_["post_content"]
    #// Don't run if no pretty permalinks or post is not published, scheduled, or privately published.
    if (not get_option("permalink_structure")) or (not php_in_array(post_["post_status"], Array("publish", "future", "private"))):
        return
    # end if
    #// Short if there aren't any links or no '?attachment_id=' strings (strpos cannot be zero).
    if (not php_strpos(content_, "?attachment_id=")) or (not preg_match_all("/<a ([^>]+)>[\\s\\S]+?<\\/a>/", content_, link_matches_)):
        return
    # end if
    site_url_ = get_bloginfo("url")
    site_url_ = php_substr(site_url_, php_int(php_strpos(site_url_, "://")))
    #// Remove the http(s).
    replace_ = ""
    for key_,value_ in link_matches_[1].items():
        if (not php_strpos(value_, "?attachment_id=")) or (not php_strpos(value_, "wp-att-")) or (not php_preg_match("/href=([\"'])[^\"']*\\?attachment_id=(\\d+)[^\"']*\\1/", value_, url_match_)) or (not php_preg_match("/rel=[\"'][^\"']*wp-att-(\\d+)/", value_, rel_match_)):
            continue
        # end if
        quote_ = url_match_[1]
        #// The quote (single or double).
        url_id_ = php_int(url_match_[2])
        rel_id_ = php_int(rel_match_[1])
        if (not url_id_) or (not rel_id_) or url_id_ != rel_id_ or php_strpos(url_match_[0], site_url_) == False:
            continue
        # end if
        link_ = link_matches_[0][key_]
        replace_ = php_str_replace(url_match_[0], "href=" + quote_ + get_attachment_link(url_id_) + quote_, link_)
        content_ = php_str_replace(link_, replace_, content_)
    # end for
    if replace_:
        post_["post_content"] = content_
        #// Escape data pulled from DB.
        post_ = add_magic_quotes(post_)
        return wp_update_post(post_)
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
def get_available_post_statuses(type_="post", *_args_):
    
    
    stati_ = wp_count_posts(type_)
    return php_array_keys(get_object_vars(stati_))
# end def get_available_post_statuses
#// 
#// Run the wp query to fetch the posts for listing on the edit posts page
#// 
#// @since 2.5.0
#// 
#// @param array|bool $q Array of query variables to use to build the query or false to use $_GET superglobal.
#// @return array
#//
def wp_edit_posts_query(q_=None, *_args_):
    if q_ is None:
        q_ = False
    # end if
    
    if False == q_:
        q_ = PHP_REQUEST
    # end if
    q_["m"] = php_int(q_["m"]) if (php_isset(lambda : q_["m"])) else 0
    q_["cat"] = php_int(q_["cat"]) if (php_isset(lambda : q_["cat"])) else 0
    post_stati_ = get_post_stati()
    if (php_isset(lambda : q_["post_type"])) and php_in_array(q_["post_type"], get_post_types()):
        post_type_ = q_["post_type"]
    else:
        post_type_ = "post"
    # end if
    avail_post_stati_ = get_available_post_statuses(post_type_)
    post_status_ = ""
    perm_ = ""
    if (php_isset(lambda : q_["post_status"])) and php_in_array(q_["post_status"], post_stati_):
        post_status_ = q_["post_status"]
        perm_ = "readable"
    # end if
    orderby_ = ""
    if (php_isset(lambda : q_["orderby"])):
        orderby_ = q_["orderby"]
    elif (php_isset(lambda : q_["post_status"])) and php_in_array(q_["post_status"], Array("pending", "draft")):
        orderby_ = "modified"
    # end if
    order_ = ""
    if (php_isset(lambda : q_["order"])):
        order_ = q_["order"]
    elif (php_isset(lambda : q_["post_status"])) and "pending" == q_["post_status"]:
        order_ = "ASC"
    # end if
    per_page_ = str("edit_") + str(post_type_) + str("_per_page")
    posts_per_page_ = php_int(get_user_option(per_page_))
    if php_empty(lambda : posts_per_page_) or posts_per_page_ < 1:
        posts_per_page_ = 20
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
    posts_per_page_ = apply_filters(str("edit_") + str(post_type_) + str("_per_page"), posts_per_page_)
    #// 
    #// Filters the number of posts displayed per page when specifically listing "posts".
    #// 
    #// @since 2.8.0
    #// 
    #// @param int    $posts_per_page Number of posts to be displayed. Default 20.
    #// @param string $post_type      The post type.
    #//
    posts_per_page_ = apply_filters("edit_posts_per_page", posts_per_page_, post_type_)
    query_ = php_compact("post_type_", "post_status_", "perm_", "order_", "orderby_", "posts_per_page_")
    #// Hierarchical types require special args.
    if is_post_type_hierarchical(post_type_) and php_empty(lambda : orderby_):
        query_["orderby"] = "menu_order title"
        query_["order"] = "asc"
        query_["posts_per_page"] = -1
        query_["posts_per_archive_page"] = -1
        query_["fields"] = "id=>parent"
    # end if
    if (not php_empty(lambda : q_["show_sticky"])):
        query_["post__in"] = get_option("sticky_posts")
    # end if
    wp(query_)
    return avail_post_stati_
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
def wp_edit_attachments_query_vars(q_=None, *_args_):
    if q_ is None:
        q_ = False
    # end if
    
    if False == q_:
        q_ = PHP_REQUEST
    # end if
    q_["m"] = php_int(q_["m"]) if (php_isset(lambda : q_["m"])) else 0
    q_["cat"] = php_int(q_["cat"]) if (php_isset(lambda : q_["cat"])) else 0
    q_["post_type"] = "attachment"
    post_type_ = get_post_type_object("attachment")
    states_ = "inherit"
    if current_user_can(post_type_.cap.read_private_posts):
        states_ += ",private"
    # end if
    q_["post_status"] = "trash" if (php_isset(lambda : q_["status"])) and "trash" == q_["status"] else states_
    q_["post_status"] = "trash" if (php_isset(lambda : q_["attachment-filter"])) and "trash" == q_["attachment-filter"] else states_
    media_per_page_ = php_int(get_user_option("upload_per_page"))
    if php_empty(lambda : media_per_page_) or media_per_page_ < 1:
        media_per_page_ = 20
    # end if
    #// 
    #// Filters the number of items to list per page when listing media items.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $media_per_page Number of media to list. Default 20.
    #//
    q_["posts_per_page"] = apply_filters("upload_per_page", media_per_page_)
    post_mime_types_ = get_post_mime_types()
    if (php_isset(lambda : q_["post_mime_type"])) and (not php_array_intersect(q_["post_mime_type"], php_array_keys(post_mime_types_))):
        q_["post_mime_type"] = None
    # end if
    for type_ in php_array_keys(post_mime_types_):
        if (php_isset(lambda : q_["attachment-filter"])) and str("post_mime_type:") + str(type_) == q_["attachment-filter"]:
            q_["post_mime_type"] = type_
            break
        # end if
    # end for
    if (php_isset(lambda : q_["detached"])) or (php_isset(lambda : q_["attachment-filter"])) and "detached" == q_["attachment-filter"]:
        q_["post_parent"] = 0
    # end if
    if (php_isset(lambda : q_["mine"])) or (php_isset(lambda : q_["attachment-filter"])) and "mine" == q_["attachment-filter"]:
        q_["author"] = get_current_user_id()
    # end if
    #// Filter query clauses to include filenames.
    if (php_isset(lambda : q_["s"])):
        add_filter("posts_clauses", "_filter_query_attachment_filenames")
    # end if
    return q_
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
def wp_edit_attachments_query(q_=None, *_args_):
    if q_ is None:
        q_ = False
    # end if
    
    wp(wp_edit_attachments_query_vars(q_))
    post_mime_types_ = get_post_mime_types()
    avail_post_mime_types_ = get_available_post_mime_types("attachment")
    return Array(post_mime_types_, avail_post_mime_types_)
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
def postbox_classes(box_id_=None, screen_id_=None, *_args_):
    
    
    if (php_isset(lambda : PHP_REQUEST["edit"])) and PHP_REQUEST["edit"] == box_id_:
        classes_ = Array("")
    elif get_user_option("closedpostboxes_" + screen_id_):
        closed_ = get_user_option("closedpostboxes_" + screen_id_)
        if (not php_is_array(closed_)):
            classes_ = Array("")
        else:
            classes_ = Array("closed") if php_in_array(box_id_, closed_) else Array("")
        # end if
    else:
        classes_ = Array("")
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
    classes_ = apply_filters(str("postbox_classes_") + str(screen_id_) + str("_") + str(box_id_), classes_)
    return php_implode(" ", classes_)
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
def get_sample_permalink(id_=None, title_=None, name_=None, *_args_):
    if title_ is None:
        title_ = None
    # end if
    if name_ is None:
        name_ = None
    # end if
    
    post_ = get_post(id_)
    if (not post_):
        return Array("", "")
    # end if
    ptype_ = get_post_type_object(post_.post_type)
    original_status_ = post_.post_status
    original_date_ = post_.post_date
    original_name_ = post_.post_name
    #// Hack: get_permalink() would return ugly permalink for drafts, so we will fake that our post is published.
    if php_in_array(post_.post_status, Array("draft", "pending", "future")):
        post_.post_status = "publish"
        post_.post_name = sanitize_title(post_.post_name if post_.post_name else post_.post_title, post_.ID)
    # end if
    #// If the user wants to set a new name -- override the current one.
    #// Note: if empty name is supplied -- use the title instead, see #6072.
    if (not php_is_null(name_)):
        post_.post_name = sanitize_title(name_ if name_ else title_, post_.ID)
    # end if
    post_.post_name = wp_unique_post_slug(post_.post_name, post_.ID, post_.post_status, post_.post_type, post_.post_parent)
    post_.filter = "sample"
    permalink_ = get_permalink(post_, True)
    #// Replace custom post_type token with generic pagename token for ease of use.
    permalink_ = php_str_replace(str("%") + str(post_.post_type) + str("%"), "%pagename%", permalink_)
    #// Handle page hierarchy.
    if ptype_.hierarchical:
        uri_ = get_page_uri(post_)
        if uri_:
            uri_ = untrailingslashit(uri_)
            uri_ = php_strrev(php_stristr(php_strrev(uri_), "/"))
            uri_ = untrailingslashit(uri_)
        # end if
        #// This filter is documented in wp-admin/edit-tag-form.php
        uri_ = apply_filters("editable_slug", uri_, post_)
        if (not php_empty(lambda : uri_)):
            uri_ += "/"
        # end if
        permalink_ = php_str_replace("%pagename%", str(uri_) + str("%pagename%"), permalink_)
    # end if
    #// This filter is documented in wp-admin/edit-tag-form.php
    permalink_ = Array(permalink_, apply_filters("editable_slug", post_.post_name, post_))
    post_.post_status = original_status_
    post_.post_date = original_date_
    post_.post_name = original_name_
    post_.filter = None
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
    return apply_filters("get_sample_permalink", permalink_, post_.ID, title_, name_, post_)
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
def get_sample_permalink_html(id_=None, new_title_=None, new_slug_=None, *_args_):
    if new_title_ is None:
        new_title_ = None
    # end if
    if new_slug_ is None:
        new_slug_ = None
    # end if
    
    post_ = get_post(id_)
    if (not post_):
        return ""
    # end if
    permalink_, post_name_ = get_sample_permalink(post_.ID, new_title_, new_slug_)
    view_link_ = False
    preview_target_ = ""
    if current_user_can("read_post", post_.ID):
        if "draft" == post_.post_status or php_empty(lambda : post_.post_name):
            view_link_ = get_preview_post_link(post_)
            preview_target_ = str(" target='wp-preview-") + str(post_.ID) + str("'")
        else:
            if "publish" == post_.post_status or "attachment" == post_.post_type:
                view_link_ = get_permalink(post_)
            else:
                #// Allow non-published (private, future) to be viewed at a pretty permalink, in case $post->post_name is set.
                view_link_ = php_str_replace(Array("%pagename%", "%postname%"), post_.post_name, permalink_)
            # end if
        # end if
    # end if
    #// Permalinks without a post/page name placeholder don't have anything to edit.
    if False == php_strpos(permalink_, "%postname%") and False == php_strpos(permalink_, "%pagename%"):
        return_ = "<strong>" + __("Permalink:") + "</strong>\n"
        if False != view_link_:
            display_link_ = urldecode(view_link_)
            return_ += "<a id=\"sample-permalink\" href=\"" + esc_url(view_link_) + "\"" + preview_target_ + ">" + esc_html(display_link_) + "</a>\n"
        else:
            return_ += "<span id=\"sample-permalink\">" + permalink_ + "</span>\n"
        # end if
        #// Encourage a pretty permalink setting.
        if "" == get_option("permalink_structure") and current_user_can("manage_options") and (not "page" == get_option("show_on_front") and get_option("page_on_front") == id_):
            return_ += "<span id=\"change-permalinks\"><a href=\"options-permalink.php\" class=\"button button-small\" target=\"_blank\">" + __("Change Permalinks") + "</a></span>\n"
        # end if
    else:
        if php_mb_strlen(post_name_) > 34:
            post_name_abridged_ = php_mb_substr(post_name_, 0, 16) + "&hellip;" + php_mb_substr(post_name_, -16)
        else:
            post_name_abridged_ = post_name_
        # end if
        post_name_html_ = "<span id=\"editable-post-name\">" + esc_html(post_name_abridged_) + "</span>"
        display_link_ = php_str_replace(Array("%pagename%", "%postname%"), post_name_html_, esc_html(urldecode(permalink_)))
        return_ = "<strong>" + __("Permalink:") + "</strong>\n"
        return_ += "<span id=\"sample-permalink\"><a href=\"" + esc_url(view_link_) + "\"" + preview_target_ + ">" + display_link_ + "</a></span>\n"
        return_ += "&lrm;"
        #// Fix bi-directional text display defect in RTL languages.
        return_ += "<span id=\"edit-slug-buttons\"><button type=\"button\" class=\"edit-slug button button-small hide-if-no-js\" aria-label=\"" + __("Edit permalink") + "\">" + __("Edit") + "</button></span>\n"
        return_ += "<span id=\"editable-post-name-full\">" + esc_html(post_name_) + "</span>\n"
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
    return_ = apply_filters("get_sample_permalink_html", return_, post_.ID, new_title_, new_slug_, post_)
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
def _wp_post_thumbnail_html(thumbnail_id_=None, post_=None, *_args_):
    if thumbnail_id_ is None:
        thumbnail_id_ = None
    # end if
    if post_ is None:
        post_ = None
    # end if
    
    _wp_additional_image_sizes_ = wp_get_additional_image_sizes()
    post_ = get_post(post_)
    post_type_object_ = get_post_type_object(post_.post_type)
    set_thumbnail_link_ = "<p class=\"hide-if-no-js\"><a href=\"%s\" id=\"set-post-thumbnail\"%s class=\"thickbox\">%s</a></p>"
    upload_iframe_src_ = get_upload_iframe_src("image", post_.ID)
    content_ = php_sprintf(set_thumbnail_link_, esc_url(upload_iframe_src_), "", esc_html(post_type_object_.labels.set_featured_image))
    if thumbnail_id_ and get_post(thumbnail_id_):
        size_ = "post-thumbnail" if (php_isset(lambda : _wp_additional_image_sizes_["post-thumbnail"])) else Array(266, 266)
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
        size_ = apply_filters("admin_post_thumbnail_size", size_, thumbnail_id_, post_)
        thumbnail_html_ = wp_get_attachment_image(thumbnail_id_, size_)
        if (not php_empty(lambda : thumbnail_html_)):
            content_ = php_sprintf(set_thumbnail_link_, esc_url(upload_iframe_src_), " aria-describedby=\"set-post-thumbnail-desc\"", thumbnail_html_)
            content_ += "<p class=\"hide-if-no-js howto\" id=\"set-post-thumbnail-desc\">" + __("Click the image to edit or update") + "</p>"
            content_ += "<p class=\"hide-if-no-js\"><a href=\"#\" id=\"remove-post-thumbnail\">" + esc_html(post_type_object_.labels.remove_featured_image) + "</a></p>"
        # end if
    # end if
    content_ += "<input type=\"hidden\" id=\"_thumbnail_id\" name=\"_thumbnail_id\" value=\"" + esc_attr(thumbnail_id_ if thumbnail_id_ else "-1") + "\" />"
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
    return apply_filters("admin_post_thumbnail_html", content_, post_.ID, thumbnail_id_)
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
def wp_check_post_lock(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    lock_ = get_post_meta(post_.ID, "_edit_lock", True)
    if (not lock_):
        return False
    # end if
    lock_ = php_explode(":", lock_)
    time_ = lock_[0]
    user_ = lock_[1] if (php_isset(lambda : lock_[1])) else get_post_meta(post_.ID, "_edit_last", True)
    if (not get_userdata(user_)):
        return False
    # end if
    #// This filter is documented in wp-admin/includes/ajax-actions.php
    time_window_ = apply_filters("wp_check_post_lock_window", 150)
    if time_ and time_ > time() - time_window_ and get_current_user_id() != user_:
        return user_
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
def wp_set_post_lock(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    if (not post_):
        return False
    # end if
    user_id_ = get_current_user_id()
    if 0 == user_id_:
        return False
    # end if
    now_ = time()
    lock_ = str(now_) + str(":") + str(user_id_)
    update_post_meta(post_.ID, "_edit_lock", lock_)
    return Array(now_, user_id_)
# end def wp_set_post_lock
#// 
#// Outputs the HTML for the notice to say that someone else is editing or has taken over editing of this post.
#// 
#// @since 2.8.5
#//
def _admin_notice_post_locked(*_args_):
    
    
    post_ = get_post()
    if (not post_):
        return
    # end if
    user_ = None
    user_id_ = wp_check_post_lock(post_.ID)
    if user_id_:
        user_ = get_userdata(user_id_)
    # end if
    if user_:
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
        if (not apply_filters("show_post_locked_dialog", True, post_, user_)):
            return
        # end if
        locked_ = True
    else:
        locked_ = False
    # end if
    sendback_ = wp_get_referer()
    if locked_ and sendback_ and False == php_strpos(sendback_, "post.php") and False == php_strpos(sendback_, "post-new.php"):
        sendback_text_ = __("Go back")
    else:
        sendback_ = admin_url("edit.php")
        if "post" != post_.post_type:
            sendback_ = add_query_arg("post_type", post_.post_type, sendback_)
        # end if
        sendback_text_ = get_post_type_object(post_.post_type).labels.all_items
    # end if
    hidden_ = "" if locked_ else " hidden"
    php_print(" <div id=\"post-lock-dialog\" class=\"notification-dialog-wrap")
    php_print(hidden_)
    php_print("""\">
    <div class=\"notification-dialog-background\"></div>
    <div class=\"notification-dialog\">
    """)
    if locked_:
        query_args_ = Array()
        if get_post_type_object(post_.post_type).public:
            if "publish" == post_.post_status or user_.ID != post_.post_author:
                #// Latest content is in autosave.
                nonce_ = wp_create_nonce("post_preview_" + post_.ID)
                query_args_["preview_id"] = post_.ID
                query_args_["preview_nonce"] = nonce_
            # end if
        # end if
        preview_link_ = get_preview_post_link(post_.ID, query_args_)
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
        override_ = apply_filters("override_post_lock", True, post_, user_)
        tab_last_ = "" if override_ else " wp-tab-last"
        php_print("     <div class=\"post-locked-message\">\n       <div class=\"post-locked-avatar\">")
        php_print(get_avatar(user_.ID, 64))
        php_print("</div>\n     <p class=\"currently-editing wp-tab-first\" tabindex=\"0\">\n       ")
        if override_:
            #// translators: %s: User's display name.
            php_printf(__("%s is already editing this post. Do you want to take over?"), esc_html(user_.display_name))
        else:
            #// translators: %s: User's display name.
            php_printf(__("%s is already editing this post."), esc_html(user_.display_name))
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
        do_action("post_locked_dialog", post_, user_)
        php_print("     <p>\n       <a class=\"button\" href=\"")
        php_print(esc_url(sendback_))
        php_print("\">")
        php_print(sendback_text_)
        php_print("</a>\n       ")
        if preview_link_:
            php_print("     <a class=\"button")
            php_print(tab_last_)
            php_print("\" href=\"")
            php_print(esc_url(preview_link_))
            php_print("\">")
            _e("Preview")
            php_print("</a>\n           ")
        # end if
        #// Allow plugins to prevent some users overriding the post lock.
        if override_:
            php_print(" <a class=\"button button-primary wp-tab-last\" href=\"")
            php_print(esc_url(add_query_arg("get-post-lock", "1", wp_nonce_url(get_edit_post_link(post_.ID, "url"), "lock-post_" + post_.ID))))
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
        do_action("post_lock_lost_dialog", post_)
        php_print("         <p><a class=\"button button-primary wp-tab-last\" href=\"")
        php_print(esc_url(sendback_))
        php_print("\">")
        php_print(sendback_text_)
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
def wp_create_post_autosave(post_data_=None, *_args_):
    
    
    if php_is_numeric(post_data_):
        post_id_ = post_data_
        post_data_ = PHP_POST
    else:
        post_id_ = php_int(post_data_["post_ID"])
    # end if
    post_data_ = _wp_translate_postdata(True, post_data_)
    if is_wp_error(post_data_):
        return post_data_
    # end if
    post_data_ = _wp_get_allowed_postdata(post_data_)
    post_author_ = get_current_user_id()
    #// Store one autosave per author. If there is already an autosave, overwrite it.
    old_autosave_ = wp_get_post_autosave(post_id_, post_author_)
    if old_autosave_:
        new_autosave_ = _wp_post_revision_data(post_data_, True)
        new_autosave_["ID"] = old_autosave_.ID
        new_autosave_["post_author"] = post_author_
        post_ = get_post(post_id_)
        #// If the new autosave has the same content as the post, delete the autosave.
        autosave_is_different_ = False
        for field_ in php_array_intersect(php_array_keys(new_autosave_), php_array_keys(_wp_post_revision_fields(post_))):
            if normalize_whitespace(new_autosave_[field_]) != normalize_whitespace(post_.field_):
                autosave_is_different_ = True
                break
            # end if
        # end for
        if (not autosave_is_different_):
            wp_delete_post_revision(old_autosave_.ID)
            return 0
        # end if
        #// 
        #// Fires before an autosave is stored.
        #// 
        #// @since 4.1.0
        #// 
        #// @param array $new_autosave Post array - the autosave that is about to be saved.
        #//
        do_action("wp_creating_autosave", new_autosave_)
        return wp_update_post(new_autosave_)
    # end if
    #// _wp_put_post_revision() expects unescaped.
    post_data_ = wp_unslash(post_data_)
    #// Otherwise create the new autosave as a special post revision.
    return _wp_put_post_revision(post_data_, True)
# end def wp_create_post_autosave
#// 
#// Saves a draft or manually autosaves for the purpose of showing a post preview.
#// 
#// @since 2.7.0
#// 
#// @return string URL to redirect to show the preview.
#//
def post_preview(*_args_):
    
    global PHP_POST
    post_ID_ = php_int(PHP_POST["post_ID"])
    PHP_POST["ID"] = post_ID_
    post_ = get_post(post_ID_)
    if (not post_):
        wp_die(__("Sorry, you are not allowed to edit this post."))
    # end if
    if (not current_user_can("edit_post", post_.ID)):
        wp_die(__("Sorry, you are not allowed to edit this post."))
    # end if
    is_autosave_ = False
    if (not wp_check_post_lock(post_.ID)) and get_current_user_id() == post_.post_author and "draft" == post_.post_status or "auto-draft" == post_.post_status:
        saved_post_id_ = edit_post()
    else:
        is_autosave_ = True
        if (php_isset(lambda : PHP_POST["post_status"])) and "auto-draft" == PHP_POST["post_status"]:
            PHP_POST["post_status"] = "draft"
        # end if
        saved_post_id_ = wp_create_post_autosave(post_.ID)
    # end if
    if is_wp_error(saved_post_id_):
        wp_die(saved_post_id_.get_error_message())
    # end if
    query_args_ = Array()
    if is_autosave_ and saved_post_id_:
        query_args_["preview_id"] = post_.ID
        query_args_["preview_nonce"] = wp_create_nonce("post_preview_" + post_.ID)
        if (php_isset(lambda : PHP_POST["post_format"])):
            query_args_["post_format"] = "standard" if php_empty(lambda : PHP_POST["post_format"]) else sanitize_key(PHP_POST["post_format"])
        # end if
        if (php_isset(lambda : PHP_POST["_thumbnail_id"])):
            query_args_["_thumbnail_id"] = "-1" if php_intval(PHP_POST["_thumbnail_id"]) <= 0 else php_intval(PHP_POST["_thumbnail_id"])
        # end if
    # end if
    return get_preview_post_link(post_, query_args_)
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
def wp_autosave(post_data_=None, *_args_):
    
    
    #// Back-compat.
    if (not php_defined("DOING_AUTOSAVE")):
        php_define("DOING_AUTOSAVE", True)
    # end if
    post_id_ = php_int(post_data_["post_id"])
    post_data_["ID"] = post_id_
    post_data_["post_ID"] = post_id_
    if False == wp_verify_nonce(post_data_["_wpnonce"], "update-post_" + post_id_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_nonce", __("Error while saving.")))
    # end if
    post_ = get_post(post_id_)
    if (not current_user_can("edit_post", post_.ID)):
        return php_new_class("WP_Error", lambda : WP_Error("edit_posts", __("Sorry, you are not allowed to edit this item.")))
    # end if
    if "auto-draft" == post_.post_status:
        post_data_["post_status"] = "draft"
    # end if
    if "page" != post_data_["post_type"] and (not php_empty(lambda : post_data_["catslist"])):
        post_data_["post_category"] = php_explode(",", post_data_["catslist"])
    # end if
    if (not wp_check_post_lock(post_.ID)) and get_current_user_id() == post_.post_author and "auto-draft" == post_.post_status or "draft" == post_.post_status:
        #// Drafts and auto-drafts are just overwritten by autosave for the same user if the post is not locked.
        return edit_post(wp_slash(post_data_))
    else:
        #// Non-drafts or other users' drafts are not overwritten.
        #// The autosave is stored in a special post revision for each user.
        return wp_create_post_autosave(wp_slash(post_data_))
    # end if
# end def wp_autosave
#// 
#// Redirect to previous page.
#// 
#// @since 2.7.0
#// 
#// @param int $post_id Optional. Post ID.
#//
def redirect_post(post_id_="", *_args_):
    
    
    if (php_isset(lambda : PHP_POST["save"])) or (php_isset(lambda : PHP_POST["publish"])):
        status_ = get_post_status(post_id_)
        if (php_isset(lambda : PHP_POST["publish"])):
            for case in Switch(status_):
                if case("pending"):
                    message_ = 8
                    break
                # end if
                if case("future"):
                    message_ = 9
                    break
                # end if
                if case():
                    message_ = 6
                # end if
            # end for
        else:
            message_ = 10 if "draft" == status_ else 1
        # end if
        location_ = add_query_arg("message", message_, get_edit_post_link(post_id_, "url"))
    elif (php_isset(lambda : PHP_POST["addmeta"])) and PHP_POST["addmeta"]:
        location_ = add_query_arg("message", 2, wp_get_referer())
        location_ = php_explode("#", location_)
        location_ = location_[0] + "#postcustom"
    elif (php_isset(lambda : PHP_POST["deletemeta"])) and PHP_POST["deletemeta"]:
        location_ = add_query_arg("message", 3, wp_get_referer())
        location_ = php_explode("#", location_)
        location_ = location_[0] + "#postcustom"
    else:
        location_ = add_query_arg("message", 4, get_edit_post_link(post_id_, "url"))
    # end if
    #// 
    #// Filters the post redirect destination URL.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $location The destination URL.
    #// @param int    $post_id  The post ID.
    #//
    wp_redirect(apply_filters("redirect_post_location", location_, post_id_))
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
def taxonomy_meta_box_sanitize_cb_checkboxes(taxonomy_=None, terms_=None, *_args_):
    
    
    return php_array_map("intval", terms_)
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
def taxonomy_meta_box_sanitize_cb_input(taxonomy_=None, terms_=None, *_args_):
    
    
    #// 
    #// Assume that a 'tax_input' string is a comma-separated list of term names.
    #// Some languages may use a character other than a comma as a delimiter, so we standardize on
    #// commas before parsing the list.
    #//
    if (not php_is_array(terms_)):
        comma_ = _x(",", "tag delimiter")
        if "," != comma_:
            terms_ = php_str_replace(comma_, ",", terms_)
        # end if
        terms_ = php_explode(",", php_trim(terms_, " \n \r ,"))
    # end if
    clean_terms_ = Array()
    for term_ in terms_:
        #// Empty terms are invalid input.
        if php_empty(lambda : term_):
            continue
        # end if
        _term_ = get_terms(Array({"taxonomy": taxonomy_, "name": term_, "fields": "ids", "hide_empty": False}))
        if (not php_empty(lambda : _term_)):
            clean_terms_[-1] = php_intval(_term_[0])
        else:
            #// No existing term was found, so pass the string. A new term will be created.
            clean_terms_[-1] = term_
        # end if
    # end for
    return clean_terms_
# end def taxonomy_meta_box_sanitize_cb_input
#// 
#// Return whether the post can be edited in the block editor.
#// 
#// @since 5.0.0
#// 
#// @param int|WP_Post $post Post ID or WP_Post object.
#// @return bool Whether the post can be edited in the block editor.
#//
def use_block_editor_for_post(post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    #// We're in the meta box loader, so don't use the block editor.
    if (php_isset(lambda : PHP_REQUEST["meta-box-loader"])):
        check_admin_referer("meta-box-loader", "meta-box-loader-nonce")
        return False
    # end if
    #// The posts page can't be edited in the block editor.
    if absint(get_option("page_for_posts")) == post_.ID and php_empty(lambda : post_.post_content):
        return False
    # end if
    use_block_editor_ = use_block_editor_for_post_type(post_.post_type)
    #// 
    #// Filter whether a post is able to be edited in the block editor.
    #// 
    #// @since 5.0.0
    #// 
    #// @param bool    $use_block_editor Whether the post can be edited or not.
    #// @param WP_Post $post             The post being checked.
    #//
    return apply_filters("use_block_editor_for_post", use_block_editor_, post_)
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
def use_block_editor_for_post_type(post_type_=None, *_args_):
    
    
    if (not post_type_exists(post_type_)):
        return False
    # end if
    if (not post_type_supports(post_type_, "editor")):
        return False
    # end if
    post_type_object_ = get_post_type_object(post_type_)
    if post_type_object_ and (not post_type_object_.show_in_rest):
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
    return apply_filters("use_block_editor_for_post_type", True, post_type_)
# end def use_block_editor_for_post_type
#// 
#// Returns all the block categories that will be shown in the block editor.
#// 
#// @since 5.0.0
#// 
#// @param WP_Post $post Post object.
#// @return array[] Array of block categories.
#//
def get_block_categories(post_=None, *_args_):
    
    
    default_categories_ = Array(Array({"slug": "common", "title": __("Common Blocks"), "icon": None}), Array({"slug": "formatting", "title": __("Formatting"), "icon": None}), Array({"slug": "layout", "title": __("Layout Elements"), "icon": None}), Array({"slug": "widgets", "title": __("Widgets"), "icon": None}), Array({"slug": "embed", "title": __("Embeds"), "icon": None}), Array({"slug": "reusable", "title": __("Reusable Blocks"), "icon": None}))
    #// 
    #// Filter the default array of block categories.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array[] $default_categories Array of block categories.
    #// @param WP_Post $post               Post being loaded.
    #//
    return apply_filters("block_categories", default_categories_, post_)
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
def get_block_editor_server_block_settings(*_args_):
    
    
    block_registry_ = WP_Block_Type_Registry.get_instance()
    blocks_ = Array()
    keys_to_pick_ = Array("title", "description", "icon", "category", "keywords", "parent", "supports", "attributes", "styles")
    for block_name_,block_type_ in block_registry_.get_all_registered().items():
        for key_ in keys_to_pick_:
            if (not (php_isset(lambda : block_type_.key_))):
                continue
            # end if
            if (not (php_isset(lambda : blocks_[block_name_]))):
                blocks_[block_name_] = Array()
            # end if
            blocks_[block_name_][key_] = block_type_.key_
        # end for
    # end for
    return blocks_
# end def get_block_editor_server_block_settings
#// 
#// Renders the meta boxes forms.
#// 
#// @since 5.0.0
#//
def the_block_editor_meta_boxes(*_args_):
    
    
    global post_
    global current_screen_
    global wp_meta_boxes_
    php_check_if_defined("post_","current_screen_","wp_meta_boxes_")
    #// Handle meta box state.
    _original_meta_boxes_ = wp_meta_boxes_
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
    wp_meta_boxes_ = apply_filters("filter_block_editor_meta_boxes", wp_meta_boxes_)
    locations_ = Array("side", "normal", "advanced")
    priorities_ = Array("high", "sorted", "core", "default", "low")
    pass
    php_print(" <form class=\"metabox-base-form\">\n    ")
    the_block_editor_meta_box_post_form_hidden_fields(post_)
    php_print(" </form>\n   <form id=\"toggle-custom-fields-form\" method=\"post\" action=\"")
    php_print(esc_attr(admin_url("post.php")))
    php_print("\">\n        ")
    wp_nonce_field("toggle-custom-fields")
    php_print("     <input type=\"hidden\" name=\"action\" value=\"toggle-custom-fields\" />\n  </form>\n   ")
    for location_ in locations_:
        php_print("     <form class=\"metabox-location-")
        php_print(esc_attr(location_))
        php_print("""\" onsubmit=\"return false;\">
        <div id=\"poststuff\" class=\"sidebar-open\">
        <div id=\"postbox-container-2\" class=\"postbox-container\">
        """)
        do_meta_boxes(current_screen_, location_, post_)
        php_print("""               </div>
        </div>
        </form>
        """)
    # end for
    php_print(" ")
    meta_boxes_per_location_ = Array()
    for location_ in locations_:
        meta_boxes_per_location_[location_] = Array()
        if (not (php_isset(lambda : wp_meta_boxes_[current_screen_.id][location_]))):
            continue
        # end if
        for priority_ in priorities_:
            if (not (php_isset(lambda : wp_meta_boxes_[current_screen_.id][location_][priority_]))):
                continue
            # end if
            meta_boxes_ = wp_meta_boxes_[current_screen_.id][location_][priority_]
            for meta_box_ in meta_boxes_:
                if False == meta_box_ or (not meta_box_["title"]):
                    continue
                # end if
                #// If a meta box is just here for back compat, don't show it in the block editor.
                if (php_isset(lambda : meta_box_["args"]["__back_compat_meta_box"])) and meta_box_["args"]["__back_compat_meta_box"]:
                    continue
                # end if
                meta_boxes_per_location_[location_][-1] = Array({"id": meta_box_["id"], "title": meta_box_["title"]})
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
    script_ = "window._wpLoadBlockEditor.then( function() {\n       wp.data.dispatch( 'core/edit-post' ).setAvailableMetaBoxesPerLocation( " + wp_json_encode(meta_boxes_per_location_) + " );\n    } );"
    wp_add_inline_script("wp-edit-post", script_)
    #// 
    #// When `wp-edit-post` is output in the `<head>`, the inline script needs to be manually printed. Otherwise,
    #// meta boxes will not display because inline scripts for `wp-edit-post` will not be printed again after this point.
    #//
    if wp_script_is("wp-edit-post", "done"):
        php_printf("""<script type='text/javascript'>
        %s
        </script>
        """, php_trim(script_))
    # end if
    #// 
    #// If the 'postcustom' meta box is enabled, then we need to perform some
    #// extra initialization on it.
    #//
    enable_custom_fields_ = php_bool(get_user_meta(get_current_user_id(), "enable_custom_fields", True))
    if enable_custom_fields_:
        script_ = str("""( function( $ ) {\n            if ( $('#postcustom').length ) {\n              $( '#the-list' ).wpList( {\n                    addBefore: function( s ) {\n                        s.data += '&post_id=""") + str(post_.ID) + str("""';\n                      return s;\n                 },\n                    addAfter: function() {\n                        $('table#list-table').show();\n                 }\n             });\n           }\n     } )( jQuery );""")
        wp_enqueue_script("wp-lists")
        wp_add_inline_script("wp-lists", script_)
    # end if
    #// Reset meta box data.
    wp_meta_boxes_ = _original_meta_boxes_
# end def the_block_editor_meta_boxes
#// 
#// Renders the hidden form required for the meta boxes form.
#// 
#// @since 5.0.0
#// 
#// @param WP_Post $post Current post object.
#//
def the_block_editor_meta_box_post_form_hidden_fields(post_=None, *_args_):
    
    
    form_extra_ = ""
    if "auto-draft" == post_.post_status:
        form_extra_ += "<input type='hidden' id='auto_draft' name='auto_draft' value='1' />"
    # end if
    form_action_ = "editpost"
    nonce_action_ = "update-post_" + post_.ID
    form_extra_ += "<input type='hidden' id='post_ID' name='post_ID' value='" + esc_attr(post_.ID) + "' />"
    referer_ = wp_get_referer()
    current_user_ = wp_get_current_user()
    user_id_ = current_user_.ID
    wp_nonce_field(nonce_action_)
    #// 
    #// Some meta boxes hook into these actions to add hidden input fields in the classic post form. For backwards
    #// compatibility, we can capture the output from these actions, and extract the hidden input fields.
    #//
    ob_start()
    #// This filter is documented in wp-admin/edit-form-advanced.php
    do_action("edit_form_after_title", post_)
    #// This filter is documented in wp-admin/edit-form-advanced.php
    do_action("edit_form_advanced", post_)
    classic_output_ = ob_get_clean()
    classic_elements_ = wp_html_split(classic_output_)
    hidden_inputs_ = ""
    for element_ in classic_elements_:
        if 0 != php_strpos(element_, "<input "):
            continue
        # end if
        if php_preg_match("/\\stype=['\"]hidden['\"]\\s/", element_):
            php_print(element_)
        # end if
    # end for
    php_print(" <input type=\"hidden\" id=\"user-id\" name=\"user_ID\" value=\"")
    php_print(php_int(user_id_))
    php_print("\" />\n  <input type=\"hidden\" id=\"hiddenaction\" name=\"action\" value=\"")
    php_print(esc_attr(form_action_))
    php_print("\" />\n  <input type=\"hidden\" id=\"originalaction\" name=\"originalaction\" value=\"")
    php_print(esc_attr(form_action_))
    php_print("\" />\n  <input type=\"hidden\" id=\"post_type\" name=\"post_type\" value=\"")
    php_print(esc_attr(post_.post_type))
    php_print("\" />\n  <input type=\"hidden\" id=\"original_post_status\" name=\"original_post_status\" value=\"")
    php_print(esc_attr(post_.post_status))
    php_print("\" />\n  <input type=\"hidden\" id=\"referredby\" name=\"referredby\" value=\"")
    php_print(esc_url(referer_) if referer_ else "")
    php_print("\" />\n\n    ")
    if "draft" != get_post_status(post_):
        wp_original_referer_field(True, "previous")
    # end if
    php_print(form_extra_)
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
    do_action("block_editor_meta_box_hidden_fields", post_)
# end def the_block_editor_meta_box_post_form_hidden_fields
