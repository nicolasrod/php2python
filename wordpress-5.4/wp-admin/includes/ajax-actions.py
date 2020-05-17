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
#// Administration API: Core Ajax handlers
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 2.1.0
#// 
#// 
#// No-privilege Ajax handlers.
#// 
#// 
#// Ajax handler for the Heartbeat API in
#// the no-privilege context.
#// 
#// Runs when the user is not logged in.
#// 
#// @since 3.6.0
#//
def wp_ajax_nopriv_heartbeat(*_args_):
    
    
    response_ = Array()
    #// 'screen_id' is the same as $current_screen->id and the JS global 'pagenow'.
    if (not php_empty(lambda : PHP_POST["screen_id"])):
        screen_id_ = sanitize_key(PHP_POST["screen_id"])
    else:
        screen_id_ = "front"
    # end if
    if (not php_empty(lambda : PHP_POST["data"])):
        data_ = wp_unslash(PHP_POST["data"])
        #// 
        #// Filters Heartbeat Ajax response in no-privilege environments.
        #// 
        #// @since 3.6.0
        #// 
        #// @param array  $response  The no-priv Heartbeat response.
        #// @param array  $data      The $_POST data sent.
        #// @param string $screen_id The screen id.
        #//
        response_ = apply_filters("heartbeat_nopriv_received", response_, data_, screen_id_)
    # end if
    #// 
    #// Filters Heartbeat Ajax response in no-privilege environments when no data is passed.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array  $response  The no-priv Heartbeat response.
    #// @param string $screen_id The screen id.
    #//
    response_ = apply_filters("heartbeat_nopriv_send", response_, screen_id_)
    #// 
    #// Fires when Heartbeat ticks in no-privilege environments.
    #// 
    #// Allows the transport to be easily replaced with long-polling.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array  $response  The no-priv Heartbeat response.
    #// @param string $screen_id The screen id.
    #//
    do_action("heartbeat_nopriv_tick", response_, screen_id_)
    #// Send the current time according to the server.
    response_["server_time"] = time()
    wp_send_json(response_)
# end def wp_ajax_nopriv_heartbeat
#// 
#// GET-based Ajax handlers.
#// 
#// 
#// Ajax handler for fetching a list table.
#// 
#// @since 3.1.0
#//
def wp_ajax_fetch_list(*_args_):
    
    
    list_class_ = PHP_REQUEST["list_args"]["class"]
    check_ajax_referer(str("fetch-list-") + str(list_class_), "_ajax_fetch_list_nonce")
    wp_list_table_ = _get_list_table(list_class_, Array({"screen": PHP_REQUEST["list_args"]["screen"]["id"]}))
    if (not wp_list_table_):
        wp_die(0)
    # end if
    if (not wp_list_table_.ajax_user_can()):
        wp_die(-1)
    # end if
    wp_list_table_.ajax_response()
    wp_die(0)
# end def wp_ajax_fetch_list
#// 
#// Ajax handler for tag search.
#// 
#// @since 3.1.0
#//
def wp_ajax_ajax_tag_search(*_args_):
    
    
    if (not (php_isset(lambda : PHP_REQUEST["tax"]))):
        wp_die(0)
    # end if
    taxonomy_ = sanitize_key(PHP_REQUEST["tax"])
    tax_ = get_taxonomy(taxonomy_)
    if (not tax_):
        wp_die(0)
    # end if
    if (not current_user_can(tax_.cap.assign_terms)):
        wp_die(-1)
    # end if
    s_ = wp_unslash(PHP_REQUEST["q"])
    comma_ = _x(",", "tag delimiter")
    if "," != comma_:
        s_ = php_str_replace(comma_, ",", s_)
    # end if
    if False != php_strpos(s_, ","):
        s_ = php_explode(",", s_)
        s_ = s_[php_count(s_) - 1]
    # end if
    s_ = php_trim(s_)
    #// 
    #// Filters the minimum number of characters required to fire a tag search via Ajax.
    #// 
    #// @since 4.0.0
    #// 
    #// @param int         $characters The minimum number of characters required. Default 2.
    #// @param WP_Taxonomy $tax        The taxonomy object.
    #// @param string      $s          The search term.
    #//
    term_search_min_chars_ = php_int(apply_filters("term_search_min_chars", 2, tax_, s_))
    #// 
    #// Require $term_search_min_chars chars for matching (default: 2)
    #// ensure it's a non-negative, non-zero integer.
    #//
    if 0 == term_search_min_chars_ or php_strlen(s_) < term_search_min_chars_:
        wp_die()
    # end if
    results_ = get_terms(Array({"taxonomy": taxonomy_, "name__like": s_, "fields": "names", "hide_empty": False}))
    php_print(join("\n", results_))
    wp_die()
# end def wp_ajax_ajax_tag_search
#// 
#// Ajax handler for compression testing.
#// 
#// @since 3.1.0
#//
def wp_ajax_wp_compression_test(*_args_):
    
    
    if (not current_user_can("manage_options")):
        wp_die(-1)
    # end if
    if php_ini_get("zlib.output_compression") or "ob_gzhandler" == php_ini_get("output_handler"):
        update_site_option("can_compress_scripts", 0)
        wp_die(0)
    # end if
    if (php_isset(lambda : PHP_REQUEST["test"])):
        php_header("Expires: Wed, 11 Jan 1984 05:00:00 GMT")
        php_header("Last-Modified: " + gmdate("D, d M Y H:i:s") + " GMT")
        php_header("Cache-Control: no-cache, must-revalidate, max-age=0")
        php_header("Content-Type: application/javascript; charset=UTF-8")
        force_gzip_ = php_defined("ENFORCE_GZIP") and ENFORCE_GZIP
        test_str_ = "\"wpCompressionTest Lorem ipsum dolor sit amet consectetuer mollis sapien urna ut a. Eu nonummy condimentum fringilla tempor pretium platea vel nibh netus Maecenas. Hac molestie amet justo quis pellentesque est ultrices interdum nibh Morbi. Cras mattis pretium Phasellus ante ipsum ipsum ut sociis Suspendisse Lorem. Ante et non molestie. Porta urna Vestibulum egestas id congue nibh eu risus gravida sit. Ac augue auctor Ut et non a elit massa id sodales. Elit eu Nulla at nibh adipiscing mattis lacus mauris at tempus. Netus nibh quis suscipit nec feugiat eget sed lorem et urna. Pellentesque lacus at ut massa consectetuer ligula ut auctor semper Pellentesque. Ut metus massa nibh quam Curabitur molestie nec mauris congue. Volutpat molestie elit justo facilisis neque ac risus Ut nascetur tristique. Vitae sit lorem tellus et quis Phasellus lacus tincidunt nunc Fusce. Pharetra wisi Suspendisse mus sagittis libero lacinia Integer consequat ac Phasellus. Et urna ac cursus tortor aliquam Aliquam amet tellus volutpat Vestibulum. Justo interdum condimentum In augue congue tellus sollicitudin Quisque quis nibh.\""
        if 1 == PHP_REQUEST["test"]:
            php_print(test_str_)
            wp_die()
        elif 2 == PHP_REQUEST["test"]:
            if (not (php_isset(lambda : PHP_SERVER["HTTP_ACCEPT_ENCODING"]))):
                wp_die(-1)
            # end if
            if False != php_stripos(PHP_SERVER["HTTP_ACCEPT_ENCODING"], "deflate") and php_function_exists("gzdeflate") and (not force_gzip_):
                php_header("Content-Encoding: deflate")
                out_ = gzdeflate(test_str_, 1)
            elif False != php_stripos(PHP_SERVER["HTTP_ACCEPT_ENCODING"], "gzip") and php_function_exists("gzencode"):
                php_header("Content-Encoding: gzip")
                out_ = gzencode(test_str_, 1)
            else:
                wp_die(-1)
            # end if
            php_print(out_)
            wp_die()
        elif "no" == PHP_REQUEST["test"]:
            check_ajax_referer("update_can_compress_scripts")
            update_site_option("can_compress_scripts", 0)
        elif "yes" == PHP_REQUEST["test"]:
            check_ajax_referer("update_can_compress_scripts")
            update_site_option("can_compress_scripts", 1)
        # end if
    # end if
    wp_die(0)
# end def wp_ajax_wp_compression_test
#// 
#// Ajax handler for image editor previews.
#// 
#// @since 3.1.0
#//
def wp_ajax_imgedit_preview(*_args_):
    
    
    post_id_ = php_intval(PHP_REQUEST["postid"])
    if php_empty(lambda : post_id_) or (not current_user_can("edit_post", post_id_)):
        wp_die(-1)
    # end if
    check_ajax_referer(str("image_editor-") + str(post_id_))
    php_include_file(ABSPATH + "wp-admin/includes/image-edit.php", once=False)
    if (not stream_preview_image(post_id_)):
        wp_die(-1)
    # end if
    wp_die()
# end def wp_ajax_imgedit_preview
#// 
#// Ajax handler for oEmbed caching.
#// 
#// @since 3.1.0
#// 
#// @global WP_Embed $wp_embed
#//
def wp_ajax_oembed_cache(*_args_):
    
    
    PHP_GLOBALS["wp_embed"].cache_oembed(PHP_REQUEST["post"])
    wp_die(0)
# end def wp_ajax_oembed_cache
#// 
#// Ajax handler for user autocomplete.
#// 
#// @since 3.4.0
#//
def wp_ajax_autocomplete_user(*_args_):
    
    
    if (not is_multisite()) or (not current_user_can("promote_users")) or wp_is_large_network("users"):
        wp_die(-1)
    # end if
    #// This filter is documented in wp-admin/user-new.php
    if (not current_user_can("manage_network_users")) and (not apply_filters("autocomplete_users_for_site_admins", False)):
        wp_die(-1)
    # end if
    return_ = Array()
    #// Check the type of request.
    #// Current allowed values are `add` and `search`.
    if (php_isset(lambda : PHP_REQUEST["autocomplete_type"])) and "search" == PHP_REQUEST["autocomplete_type"]:
        type_ = PHP_REQUEST["autocomplete_type"]
    else:
        type_ = "add"
    # end if
    #// Check the desired field for value.
    #// Current allowed values are `user_email` and `user_login`.
    if (php_isset(lambda : PHP_REQUEST["autocomplete_field"])) and "user_email" == PHP_REQUEST["autocomplete_field"]:
        field_ = PHP_REQUEST["autocomplete_field"]
    else:
        field_ = "user_login"
    # end if
    #// Exclude current users of this blog.
    if (php_isset(lambda : PHP_REQUEST["site_id"])):
        id_ = absint(PHP_REQUEST["site_id"])
    else:
        id_ = get_current_blog_id()
    # end if
    include_blog_users_ = get_users(Array({"blog_id": id_, "fields": "ID"})) if "search" == type_ else Array()
    exclude_blog_users_ = get_users(Array({"blog_id": id_, "fields": "ID"})) if "add" == type_ else Array()
    users_ = get_users(Array({"blog_id": False, "search": "*" + PHP_REQUEST["term"] + "*", "include": include_blog_users_, "exclude": exclude_blog_users_, "search_columns": Array("user_login", "user_nicename", "user_email")}))
    for user_ in users_:
        return_[-1] = Array({"label": php_sprintf(_x("%1$s (%2$s)", "user autocomplete result"), user_.user_login, user_.user_email), "value": user_.field_})
    # end for
    wp_die(wp_json_encode(return_))
# end def wp_ajax_autocomplete_user
#// 
#// Handles AJAX requests for community events
#// 
#// @since 4.8.0
#//
def wp_ajax_get_community_events(*_args_):
    
    
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-community-events.php", once=True)
    check_ajax_referer("community_events")
    search_ = wp_unslash(PHP_POST["location"]) if (php_isset(lambda : PHP_POST["location"])) else ""
    timezone_ = wp_unslash(PHP_POST["timezone"]) if (php_isset(lambda : PHP_POST["timezone"])) else ""
    user_id_ = get_current_user_id()
    saved_location_ = get_user_option("community-events-location", user_id_)
    events_client_ = php_new_class("WP_Community_Events", lambda : WP_Community_Events(user_id_, saved_location_))
    events_ = events_client_.get_events(search_, timezone_)
    ip_changed_ = False
    if is_wp_error(events_):
        wp_send_json_error(Array({"error": events_.get_error_message()}))
    else:
        if php_empty(lambda : saved_location_["ip"]) and (not php_empty(lambda : events_["location"]["ip"])):
            ip_changed_ = True
        elif (php_isset(lambda : saved_location_["ip"])) and (not php_empty(lambda : events_["location"]["ip"])) and saved_location_["ip"] != events_["location"]["ip"]:
            ip_changed_ = True
        # end if
        #// 
        #// The location should only be updated when it changes. The API doesn't always return
        #// a full location; sometimes it's missing the description or country. The location
        #// that was saved during the initial request is known to be good and complete, though.
        #// It should be left intact until the user explicitly changes it (either by manually
        #// searching for a new location, or by changing their IP address).
        #// 
        #// If the location was updated with an incomplete response from the API, then it could
        #// break assumptions that the UI makes (e.g., that there will always be a description
        #// that corresponds to a latitude/longitude location).
        #// 
        #// The location is stored network-wide, so that the user doesn't have to set it on each site.
        #//
        if ip_changed_ or search_:
            update_user_option(user_id_, "community-events-location", events_["location"], True)
        # end if
        wp_send_json_success(events_)
    # end if
# end def wp_ajax_get_community_events
#// 
#// Ajax handler for dashboard widgets.
#// 
#// @since 3.4.0
#//
def wp_ajax_dashboard_widgets(*_args_):
    
    
    php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
    pagenow_ = PHP_REQUEST["pagenow"]
    if "dashboard-user" == pagenow_ or "dashboard-network" == pagenow_ or "dashboard" == pagenow_:
        set_current_screen(pagenow_)
    # end if
    for case in Switch(PHP_REQUEST["widget"]):
        if case("dashboard_primary"):
            wp_dashboard_primary()
            break
        # end if
    # end for
    wp_die()
# end def wp_ajax_dashboard_widgets
#// 
#// Ajax handler for Customizer preview logged-in status.
#// 
#// @since 3.4.0
#//
def wp_ajax_logged_in(*_args_):
    
    
    wp_die(1)
# end def wp_ajax_logged_in
#// 
#// Ajax helpers.
#// 
#// 
#// Sends back current comment total and new page links if they need to be updated.
#// 
#// Contrary to normal success Ajax response ("1"), die with time() on success.
#// 
#// @access private
#// @since 2.7.0
#// 
#// @param int $comment_id
#// @param int $delta
#//
def _wp_ajax_delete_comment_response(comment_id_=None, delta_=None, *_args_):
    if delta_ is None:
        delta_ = -1
    # end if
    
    total_ = php_int(PHP_POST["_total"]) if (php_isset(lambda : PHP_POST["_total"])) else 0
    per_page_ = php_int(PHP_POST["_per_page"]) if (php_isset(lambda : PHP_POST["_per_page"])) else 0
    page_ = php_int(PHP_POST["_page"]) if (php_isset(lambda : PHP_POST["_page"])) else 0
    url_ = esc_url_raw(PHP_POST["_url"]) if (php_isset(lambda : PHP_POST["_url"])) else ""
    #// JS didn't send us everything we need to know. Just die with success message.
    if (not total_) or (not per_page_) or (not page_) or (not url_):
        time_ = time()
        comment_ = get_comment(comment_id_)
        comment_status_ = ""
        comment_link_ = ""
        if comment_:
            comment_status_ = comment_.comment_approved
        # end if
        if 1 == php_int(comment_status_):
            comment_link_ = get_comment_link(comment_)
        # end if
        counts_ = wp_count_comments()
        x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": comment_id_, "supplemental": Array({"status": comment_status_, "postId": comment_.comment_post_ID if comment_ else "", "time": time_, "in_moderation": counts_.moderated, "i18n_comments_text": php_sprintf(_n("%s Comment", "%s Comments", counts_.approved), number_format_i18n(counts_.approved)), "i18n_moderation_text": php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", counts_.moderated), number_format_i18n(counts_.moderated)), "comment_link": comment_link_})})))
        x_.send()
    # end if
    total_ += delta_
    if total_ < 0:
        total_ = 0
    # end if
    #// Only do the expensive stuff on a page-break, and about 1 other time per page.
    if 0 == total_ % per_page_ or 1 == mt_rand(1, per_page_):
        post_id_ = 0
        #// What type of comment count are we looking for?
        status_ = "all"
        parsed_ = php_parse_url(url_)
        if (php_isset(lambda : parsed_["query"])):
            parse_str(parsed_["query"], query_vars_)
            if (not php_empty(lambda : query_vars_["comment_status"])):
                status_ = query_vars_["comment_status"]
            # end if
            if (not php_empty(lambda : query_vars_["p"])):
                post_id_ = php_int(query_vars_["p"])
            # end if
            if (not php_empty(lambda : query_vars_["comment_type"])):
                type_ = query_vars_["comment_type"]
            # end if
        # end if
        if php_empty(lambda : type_):
            #// Only use the comment count if not filtering by a comment_type.
            comment_count_ = wp_count_comments(post_id_)
            #// We're looking for a known type of comment count.
            if (php_isset(lambda : comment_count_.status_)):
                total_ = comment_count_.status_
            # end if
        # end if
        pass
    # end if
    #// The time since the last comment count.
    time_ = time()
    comment_ = get_comment(comment_id_)
    counts_ = wp_count_comments()
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": comment_id_, "supplemental": Array({"status": comment_.comment_approved if comment_ else "", "postId": comment_.comment_post_ID if comment_ else "", "total_items_i18n": php_sprintf(_n("%s item", "%s items", total_), number_format_i18n(total_)), "total_pages": ceil(total_ / per_page_), "total_pages_i18n": number_format_i18n(ceil(total_ / per_page_)), "total": total_, "time": time_, "in_moderation": counts_.moderated, "i18n_moderation_text": php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", counts_.moderated), number_format_i18n(counts_.moderated))})})))
    x_.send()
# end def _wp_ajax_delete_comment_response
#// 
#// POST-based Ajax handlers.
#// 
#// 
#// Ajax handler for adding a hierarchical term.
#// 
#// @access private
#// @since 3.1.0
#//
def _wp_ajax_add_hierarchical_term(*_args_):
    
    
    action_ = PHP_POST["action"]
    taxonomy_ = get_taxonomy(php_substr(action_, 4))
    check_ajax_referer(action_, "_ajax_nonce-add-" + taxonomy_.name)
    if (not current_user_can(taxonomy_.cap.edit_terms)):
        wp_die(-1)
    # end if
    names_ = php_explode(",", PHP_POST["new" + taxonomy_.name])
    parent_ = php_int(PHP_POST["new" + taxonomy_.name + "_parent"]) if (php_isset(lambda : PHP_POST["new" + taxonomy_.name + "_parent"])) else 0
    if 0 > parent_:
        parent_ = 0
    # end if
    if "category" == taxonomy_.name:
        post_category_ = PHP_POST["post_category"] if (php_isset(lambda : PHP_POST["post_category"])) else Array()
    else:
        post_category_ = PHP_POST["tax_input"][taxonomy_.name] if (php_isset(lambda : PHP_POST["tax_input"])) and (php_isset(lambda : PHP_POST["tax_input"][taxonomy_.name])) else Array()
    # end if
    checked_categories_ = php_array_map("absint", post_category_)
    popular_ids_ = wp_popular_terms_checklist(taxonomy_.name, 0, 10, False)
    for cat_name_ in names_:
        cat_name_ = php_trim(cat_name_)
        category_nicename_ = sanitize_title(cat_name_)
        if "" == category_nicename_:
            continue
        # end if
        cat_id_ = wp_insert_term(cat_name_, taxonomy_.name, Array({"parent": parent_}))
        if (not cat_id_) or is_wp_error(cat_id_):
            continue
        else:
            cat_id_ = cat_id_["term_id"]
        # end if
        checked_categories_[-1] = cat_id_
        if parent_:
            continue
        # end if
        ob_start()
        wp_terms_checklist(0, Array({"taxonomy": taxonomy_.name, "descendants_and_self": cat_id_, "selected_cats": checked_categories_, "popular_cats": popular_ids_}))
        data_ = ob_get_clean()
        add_ = Array({"what": taxonomy_.name, "id": cat_id_, "data": php_str_replace(Array("\n", "  "), "", data_), "position": -1})
    # end for
    if parent_:
        #// Foncy - replace the parent and all its children.
        parent_ = get_term(parent_, taxonomy_.name)
        term_id_ = parent_.term_id
        while True:
            
            if not (parent_.parent):
                break
            # end if
            #// Get the top parent.
            parent_ = get_term(parent_.parent, taxonomy_.name)
            if is_wp_error(parent_):
                break
            # end if
            term_id_ = parent_.term_id
        # end while
        ob_start()
        wp_terms_checklist(0, Array({"taxonomy": taxonomy_.name, "descendants_and_self": term_id_, "selected_cats": checked_categories_, "popular_cats": popular_ids_}))
        data_ = ob_get_clean()
        add_ = Array({"what": taxonomy_.name, "id": term_id_, "data": php_str_replace(Array("\n", " "), "", data_), "position": -1})
    # end if
    ob_start()
    wp_dropdown_categories(Array({"taxonomy": taxonomy_.name, "hide_empty": 0, "name": "new" + taxonomy_.name + "_parent", "orderby": "name", "hierarchical": 1, "show_option_none": "&mdash; " + taxonomy_.labels.parent_item + " &mdash;"}))
    sup_ = ob_get_clean()
    add_["supplemental"] = Array({"newcat_parent": sup_})
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(add_))
    x_.send()
# end def _wp_ajax_add_hierarchical_term
#// 
#// Ajax handler for deleting a comment.
#// 
#// @since 3.1.0
#//
def wp_ajax_delete_comment(*_args_):
    
    
    id_ = php_int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    comment_ = get_comment(id_)
    if (not comment_):
        wp_die(time())
    # end if
    if (not current_user_can("edit_comment", comment_.comment_ID)):
        wp_die(-1)
    # end if
    check_ajax_referer(str("delete-comment_") + str(id_))
    status_ = wp_get_comment_status(comment_)
    delta_ = -1
    if (php_isset(lambda : PHP_POST["trash"])) and 1 == PHP_POST["trash"]:
        if "trash" == status_:
            wp_die(time())
        # end if
        r_ = wp_trash_comment(comment_)
    elif (php_isset(lambda : PHP_POST["untrash"])) and 1 == PHP_POST["untrash"]:
        if "trash" != status_:
            wp_die(time())
        # end if
        r_ = wp_untrash_comment(comment_)
        #// Undo trash, not in Trash.
        if (not (php_isset(lambda : PHP_POST["comment_status"]))) or "trash" != PHP_POST["comment_status"]:
            delta_ = 1
        # end if
    elif (php_isset(lambda : PHP_POST["spam"])) and 1 == PHP_POST["spam"]:
        if "spam" == status_:
            wp_die(time())
        # end if
        r_ = wp_spam_comment(comment_)
    elif (php_isset(lambda : PHP_POST["unspam"])) and 1 == PHP_POST["unspam"]:
        if "spam" != status_:
            wp_die(time())
        # end if
        r_ = wp_unspam_comment(comment_)
        #// Undo spam, not in spam.
        if (not (php_isset(lambda : PHP_POST["comment_status"]))) or "spam" != PHP_POST["comment_status"]:
            delta_ = 1
        # end if
    elif (php_isset(lambda : PHP_POST["delete"])) and 1 == PHP_POST["delete"]:
        r_ = wp_delete_comment(comment_)
    else:
        wp_die(-1)
    # end if
    if r_:
        #// Decide if we need to send back '1' or a more complicated response including page links and comment counts.
        _wp_ajax_delete_comment_response(comment_.comment_ID, delta_)
    # end if
    wp_die(0)
# end def wp_ajax_delete_comment
#// 
#// Ajax handler for deleting a tag.
#// 
#// @since 3.1.0
#//
def wp_ajax_delete_tag(*_args_):
    
    
    tag_id_ = php_int(PHP_POST["tag_ID"])
    check_ajax_referer(str("delete-tag_") + str(tag_id_))
    if (not current_user_can("delete_term", tag_id_)):
        wp_die(-1)
    # end if
    taxonomy_ = PHP_POST["taxonomy"] if (not php_empty(lambda : PHP_POST["taxonomy"])) else "post_tag"
    tag_ = get_term(tag_id_, taxonomy_)
    if (not tag_) or is_wp_error(tag_):
        wp_die(1)
    # end if
    if wp_delete_term(tag_id_, taxonomy_):
        wp_die(1)
    else:
        wp_die(0)
    # end if
# end def wp_ajax_delete_tag
#// 
#// Ajax handler for deleting a link.
#// 
#// @since 3.1.0
#//
def wp_ajax_delete_link(*_args_):
    
    
    id_ = php_int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str("delete-bookmark_") + str(id_))
    if (not current_user_can("manage_links")):
        wp_die(-1)
    # end if
    link_ = get_bookmark(id_)
    if (not link_) or is_wp_error(link_):
        wp_die(1)
    # end if
    if wp_delete_link(id_):
        wp_die(1)
    else:
        wp_die(0)
    # end if
# end def wp_ajax_delete_link
#// 
#// Ajax handler for deleting meta.
#// 
#// @since 3.1.0
#//
def wp_ajax_delete_meta(*_args_):
    
    
    id_ = php_int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str("delete-meta_") + str(id_))
    meta_ = get_metadata_by_mid("post", id_)
    if (not meta_):
        wp_die(1)
    # end if
    if is_protected_meta(meta_.meta_key, "post") or (not current_user_can("delete_post_meta", meta_.post_id, meta_.meta_key)):
        wp_die(-1)
    # end if
    if delete_meta(meta_.meta_id):
        wp_die(1)
    # end if
    wp_die(0)
# end def wp_ajax_delete_meta
#// 
#// Ajax handler for deleting a post.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_delete_post(action_=None, *_args_):
    
    
    if php_empty(lambda : action_):
        action_ = "delete-post"
    # end if
    id_ = php_int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str(action_) + str("_") + str(id_))
    if (not current_user_can("delete_post", id_)):
        wp_die(-1)
    # end if
    if (not get_post(id_)):
        wp_die(1)
    # end if
    if wp_delete_post(id_):
        wp_die(1)
    else:
        wp_die(0)
    # end if
# end def wp_ajax_delete_post
#// 
#// Ajax handler for sending a post to the Trash.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_trash_post(action_=None, *_args_):
    
    
    if php_empty(lambda : action_):
        action_ = "trash-post"
    # end if
    id_ = php_int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str(action_) + str("_") + str(id_))
    if (not current_user_can("delete_post", id_)):
        wp_die(-1)
    # end if
    if (not get_post(id_)):
        wp_die(1)
    # end if
    if "trash-post" == action_:
        done_ = wp_trash_post(id_)
    else:
        done_ = wp_untrash_post(id_)
    # end if
    if done_:
        wp_die(1)
    # end if
    wp_die(0)
# end def wp_ajax_trash_post
#// 
#// Ajax handler to restore a post from the Trash.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_untrash_post(action_=None, *_args_):
    
    
    if php_empty(lambda : action_):
        action_ = "untrash-post"
    # end if
    wp_ajax_trash_post(action_)
# end def wp_ajax_untrash_post
#// 
#// Ajax handler to delete a page.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_delete_page(action_=None, *_args_):
    
    
    if php_empty(lambda : action_):
        action_ = "delete-page"
    # end if
    id_ = php_int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str(action_) + str("_") + str(id_))
    if (not current_user_can("delete_page", id_)):
        wp_die(-1)
    # end if
    if (not get_post(id_)):
        wp_die(1)
    # end if
    if wp_delete_post(id_):
        wp_die(1)
    else:
        wp_die(0)
    # end if
# end def wp_ajax_delete_page
#// 
#// Ajax handler to dim a comment.
#// 
#// @since 3.1.0
#//
def wp_ajax_dim_comment(*_args_):
    
    
    id_ = php_int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    comment_ = get_comment(id_)
    if (not comment_):
        x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": php_new_class("WP_Error", lambda : WP_Error("invalid_comment", php_sprintf(__("Comment %d does not exist"), id_)))})))
        x_.send()
    # end if
    if (not current_user_can("edit_comment", comment_.comment_ID)) and (not current_user_can("moderate_comments")):
        wp_die(-1)
    # end if
    current_ = wp_get_comment_status(comment_)
    if (php_isset(lambda : PHP_POST["new"])) and PHP_POST["new"] == current_:
        wp_die(time())
    # end if
    check_ajax_referer(str("approve-comment_") + str(id_))
    if php_in_array(current_, Array("unapproved", "spam")):
        result_ = wp_set_comment_status(comment_, "approve", True)
    else:
        result_ = wp_set_comment_status(comment_, "hold", True)
    # end if
    if is_wp_error(result_):
        x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": result_})))
        x_.send()
    # end if
    #// Decide if we need to send back '1' or a more complicated response including page links and comment counts.
    _wp_ajax_delete_comment_response(comment_.comment_ID)
    wp_die(0)
# end def wp_ajax_dim_comment
#// 
#// Ajax handler for adding a link category.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_add_link_category(action_=None, *_args_):
    
    
    if php_empty(lambda : action_):
        action_ = "add-link-category"
    # end if
    check_ajax_referer(action_)
    tax_ = get_taxonomy("link_category")
    if (not current_user_can(tax_.cap.manage_terms)):
        wp_die(-1)
    # end if
    names_ = php_explode(",", wp_unslash(PHP_POST["newcat"]))
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    for cat_name_ in names_:
        cat_name_ = php_trim(cat_name_)
        slug_ = sanitize_title(cat_name_)
        if "" == slug_:
            continue
        # end if
        cat_id_ = wp_insert_term(cat_name_, "link_category")
        if (not cat_id_) or is_wp_error(cat_id_):
            continue
        else:
            cat_id_ = cat_id_["term_id"]
        # end if
        cat_name_ = esc_html(cat_name_)
        x_.add(Array({"what": "link-category", "id": cat_id_, "data": str("<li id='link-category-") + str(cat_id_) + str("'><label for='in-link-category-") + str(cat_id_) + str("' class='selectit'><input value='") + esc_attr(cat_id_) + str("' type='checkbox' checked='checked' name='link_category[]' id='in-link-category-") + str(cat_id_) + str("'/> ") + str(cat_name_) + str("</label></li>"), "position": -1}))
    # end for
    x_.send()
# end def wp_ajax_add_link_category
#// 
#// Ajax handler to add a tag.
#// 
#// @since 3.1.0
#//
def wp_ajax_add_tag(*_args_):
    
    
    check_ajax_referer("add-tag", "_wpnonce_add-tag")
    taxonomy_ = PHP_POST["taxonomy"] if (not php_empty(lambda : PHP_POST["taxonomy"])) else "post_tag"
    tax_ = get_taxonomy(taxonomy_)
    if (not current_user_can(tax_.cap.edit_terms)):
        wp_die(-1)
    # end if
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    tag_ = wp_insert_term(PHP_POST["tag-name"], taxonomy_, PHP_POST)
    if tag_ and (not is_wp_error(tag_)):
        tag_ = get_term(tag_["term_id"], taxonomy_)
    # end if
    if (not tag_) or is_wp_error(tag_):
        message_ = __("An error has occurred. Please reload the page and try again.")
        if is_wp_error(tag_) and tag_.get_error_message():
            message_ = tag_.get_error_message()
        # end if
        x_.add(Array({"what": "taxonomy", "data": php_new_class("WP_Error", lambda : WP_Error("error", message_))}))
        x_.send()
    # end if
    wp_list_table_ = _get_list_table("WP_Terms_List_Table", Array({"screen": PHP_POST["screen"]}))
    level_ = 0
    noparents_ = ""
    if is_taxonomy_hierarchical(taxonomy_):
        level_ = php_count(get_ancestors(tag_.term_id, taxonomy_, "taxonomy"))
        ob_start()
        wp_list_table_.single_row(tag_, level_)
        noparents_ = ob_get_clean()
    # end if
    ob_start()
    wp_list_table_.single_row(tag_)
    parents_ = ob_get_clean()
    x_.add(Array({"what": "taxonomy", "supplemental": php_compact("parents", "noparents")}))
    x_.add(Array({"what": "term", "position": level_, "supplemental": tag_}))
    x_.send()
# end def wp_ajax_add_tag
#// 
#// Ajax handler for getting a tagcloud.
#// 
#// @since 3.1.0
#//
def wp_ajax_get_tagcloud(*_args_):
    
    
    if (not (php_isset(lambda : PHP_POST["tax"]))):
        wp_die(0)
    # end if
    taxonomy_ = sanitize_key(PHP_POST["tax"])
    tax_ = get_taxonomy(taxonomy_)
    if (not tax_):
        wp_die(0)
    # end if
    if (not current_user_can(tax_.cap.assign_terms)):
        wp_die(-1)
    # end if
    tags_ = get_terms(Array({"taxonomy": taxonomy_, "number": 45, "orderby": "count", "order": "DESC"}))
    if php_empty(lambda : tags_):
        wp_die(tax_.labels.not_found)
    # end if
    if is_wp_error(tags_):
        wp_die(tags_.get_error_message())
    # end if
    for key_,tag_ in tags_:
        tags_[key_].link = "#"
        tags_[key_].id = tag_.term_id
    # end for
    #// We need raw tag names here, so don't filter the output.
    return_ = wp_generate_tag_cloud(tags_, Array({"filter": 0, "format": "list"}))
    if php_empty(lambda : return_):
        wp_die(0)
    # end if
    php_print(return_)
    wp_die()
# end def wp_ajax_get_tagcloud
#// 
#// Ajax handler for getting comments.
#// 
#// @since 3.1.0
#// 
#// @global int           $post_id
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_get_comments(action_=None, *_args_):
    
    
    global post_id_
    php_check_if_defined("post_id_")
    if php_empty(lambda : action_):
        action_ = "get-comments"
    # end if
    check_ajax_referer(action_)
    if php_empty(lambda : post_id_) and (not php_empty(lambda : PHP_REQUEST["p"])):
        id_ = absint(PHP_REQUEST["p"])
        if (not php_empty(lambda : id_)):
            post_id_ = id_
        # end if
    # end if
    if php_empty(lambda : post_id_):
        wp_die(-1)
    # end if
    wp_list_table_ = _get_list_table("WP_Post_Comments_List_Table", Array({"screen": "edit-comments"}))
    if (not current_user_can("edit_post", post_id_)):
        wp_die(-1)
    # end if
    wp_list_table_.prepare_items()
    if (not wp_list_table_.has_items()):
        wp_die(1)
    # end if
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    ob_start()
    for comment_ in wp_list_table_.items:
        if (not current_user_can("edit_comment", comment_.comment_ID)) and 0 == comment_.comment_approved:
            continue
        # end if
        get_comment(comment_)
        wp_list_table_.single_row(comment_)
    # end for
    comment_list_item_ = ob_get_clean()
    x_.add(Array({"what": "comments", "data": comment_list_item_}))
    x_.send()
# end def wp_ajax_get_comments
#// 
#// Ajax handler for replying to a comment.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_replyto_comment(action_=None, *_args_):
    
    global PHP_POST
    if php_empty(lambda : action_):
        action_ = "replyto-comment"
    # end if
    check_ajax_referer(action_, "_ajax_nonce-replyto-comment")
    comment_post_ID_ = php_int(PHP_POST["comment_post_ID"])
    post_ = get_post(comment_post_ID_)
    if (not post_):
        wp_die(-1)
    # end if
    if (not current_user_can("edit_post", comment_post_ID_)):
        wp_die(-1)
    # end if
    if php_empty(lambda : post_.post_status):
        wp_die(1)
    elif php_in_array(post_.post_status, Array("draft", "pending", "trash")):
        wp_die(__("Error: You are replying to a comment on a draft post."))
    # end if
    user_ = wp_get_current_user()
    if user_.exists():
        user_ID_ = user_.ID
        comment_author_ = wp_slash(user_.display_name)
        comment_author_email_ = wp_slash(user_.user_email)
        comment_author_url_ = wp_slash(user_.user_url)
        comment_content_ = php_trim(PHP_POST["content"])
        comment_type_ = php_trim(PHP_POST["comment_type"]) if (php_isset(lambda : PHP_POST["comment_type"])) else ""
        if current_user_can("unfiltered_html"):
            if (not (php_isset(lambda : PHP_POST["_wp_unfiltered_html_comment"]))):
                PHP_POST["_wp_unfiltered_html_comment"] = ""
            # end if
            if wp_create_nonce("unfiltered-html-comment") != PHP_POST["_wp_unfiltered_html_comment"]:
                kses_remove_filters()
                #// Start with a clean slate.
                kses_init_filters()
                #// Set up the filters.
                remove_filter("pre_comment_content", "wp_filter_post_kses")
                add_filter("pre_comment_content", "wp_filter_kses")
            # end if
        # end if
    else:
        wp_die(__("Sorry, you must be logged in to reply to a comment."))
    # end if
    if "" == comment_content_:
        wp_die(__("Error: Please type a comment."))
    # end if
    comment_parent_ = 0
    if (php_isset(lambda : PHP_POST["comment_ID"])):
        comment_parent_ = absint(PHP_POST["comment_ID"])
    # end if
    comment_auto_approved_ = False
    commentdata_ = php_compact("comment_post_ID", "comment_author", "comment_author_email", "comment_author_url", "comment_content", "comment_type", "comment_parent", "user_ID")
    #// Automatically approve parent comment.
    if (not php_empty(lambda : PHP_POST["approve_parent"])):
        parent_ = get_comment(comment_parent_)
        if parent_ and "0" == parent_.comment_approved and parent_.comment_post_ID == comment_post_ID_:
            if (not current_user_can("edit_comment", parent_.comment_ID)):
                wp_die(-1)
            # end if
            if wp_set_comment_status(parent_, "approve"):
                comment_auto_approved_ = True
            # end if
        # end if
    # end if
    comment_id_ = wp_new_comment(commentdata_)
    if is_wp_error(comment_id_):
        wp_die(comment_id_.get_error_message())
    # end if
    comment_ = get_comment(comment_id_)
    if (not comment_):
        wp_die(1)
    # end if
    position_ = php_int(PHP_POST["position"]) if (php_isset(lambda : PHP_POST["position"])) and php_int(PHP_POST["position"]) else "-1"
    ob_start()
    if (php_isset(lambda : PHP_REQUEST["mode"])) and "dashboard" == PHP_REQUEST["mode"]:
        php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
        _wp_dashboard_recent_comments_row(comment_)
    else:
        if (php_isset(lambda : PHP_REQUEST["mode"])) and "single" == PHP_REQUEST["mode"]:
            wp_list_table_ = _get_list_table("WP_Post_Comments_List_Table", Array({"screen": "edit-comments"}))
        else:
            wp_list_table_ = _get_list_table("WP_Comments_List_Table", Array({"screen": "edit-comments"}))
        # end if
        wp_list_table_.single_row(comment_)
    # end if
    comment_list_item_ = ob_get_clean()
    response_ = Array({"what": "comment", "id": comment_.comment_ID, "data": comment_list_item_, "position": position_})
    counts_ = wp_count_comments()
    response_["supplemental"] = Array({"in_moderation": counts_.moderated, "i18n_comments_text": php_sprintf(_n("%s Comment", "%s Comments", counts_.approved), number_format_i18n(counts_.approved)), "i18n_moderation_text": php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", counts_.moderated), number_format_i18n(counts_.moderated))})
    if comment_auto_approved_:
        response_["supplemental"]["parent_approved"] = parent_.comment_ID
        response_["supplemental"]["parent_post_id"] = parent_.comment_post_ID
    # end if
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    x_.add(response_)
    x_.send()
# end def wp_ajax_replyto_comment
#// 
#// Ajax handler for editing a comment.
#// 
#// @since 3.1.0
#//
def wp_ajax_edit_comment(*_args_):
    
    global PHP_POST
    check_ajax_referer("replyto-comment", "_ajax_nonce-replyto-comment")
    comment_id_ = php_int(PHP_POST["comment_ID"])
    if (not current_user_can("edit_comment", comment_id_)):
        wp_die(-1)
    # end if
    if "" == PHP_POST["content"]:
        wp_die(__("Error: Please type a comment."))
    # end if
    if (php_isset(lambda : PHP_POST["status"])):
        PHP_POST["comment_status"] = PHP_POST["status"]
    # end if
    edit_comment()
    position_ = php_int(PHP_POST["position"]) if (php_isset(lambda : PHP_POST["position"])) and php_int(PHP_POST["position"]) else "-1"
    checkbox_ = 1 if (php_isset(lambda : PHP_POST["checkbox"])) and True == PHP_POST["checkbox"] else 0
    wp_list_table_ = _get_list_table("WP_Comments_List_Table" if checkbox_ else "WP_Post_Comments_List_Table", Array({"screen": "edit-comments"}))
    comment_ = get_comment(comment_id_)
    if php_empty(lambda : comment_.comment_ID):
        wp_die(-1)
    # end if
    ob_start()
    wp_list_table_.single_row(comment_)
    comment_list_item_ = ob_get_clean()
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    x_.add(Array({"what": "edit_comment", "id": comment_.comment_ID, "data": comment_list_item_, "position": position_}))
    x_.send()
# end def wp_ajax_edit_comment
#// 
#// Ajax handler for adding a menu item.
#// 
#// @since 3.1.0
#//
def wp_ajax_add_menu_item(*_args_):
    
    
    check_ajax_referer("add-menu_item", "menu-settings-column-nonce")
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
    #// For performance reasons, we omit some object properties from the checklist.
    #// The following is a hacky way to restore them when adding non-custom items.
    menu_items_data_ = Array()
    for menu_item_data_ in PHP_POST["menu-item"]:
        if (not php_empty(lambda : menu_item_data_["menu-item-type"])) and "custom" != menu_item_data_["menu-item-type"] and (not php_empty(lambda : menu_item_data_["menu-item-object-id"])):
            for case in Switch(menu_item_data_["menu-item-type"]):
                if case("post_type"):
                    _object_ = get_post(menu_item_data_["menu-item-object-id"])
                    break
                # end if
                if case("post_type_archive"):
                    _object_ = get_post_type_object(menu_item_data_["menu-item-object"])
                    break
                # end if
                if case("taxonomy"):
                    _object_ = get_term(menu_item_data_["menu-item-object-id"], menu_item_data_["menu-item-object"])
                    break
                # end if
            # end for
            _menu_items_ = php_array_map("wp_setup_nav_menu_item", Array(_object_))
            _menu_item_ = reset(_menu_items_)
            #// Restore the missing menu item properties.
            menu_item_data_["menu-item-description"] = _menu_item_.description
        # end if
        menu_items_data_[-1] = menu_item_data_
    # end for
    item_ids_ = wp_save_nav_menu_items(0, menu_items_data_)
    if is_wp_error(item_ids_):
        wp_die(0)
    # end if
    menu_items_ = Array()
    for menu_item_id_ in item_ids_:
        menu_obj_ = get_post(menu_item_id_)
        if (not php_empty(lambda : menu_obj_.ID)):
            menu_obj_ = wp_setup_nav_menu_item(menu_obj_)
            menu_obj_.title = __("Menu Item") if php_empty(lambda : menu_obj_.title) else menu_obj_.title
            menu_obj_.label = menu_obj_.title
            #// Don't show "(pending)" in ajax-added items.
            menu_items_[-1] = menu_obj_
        # end if
    # end for
    #// This filter is documented in wp-admin/includes/nav-menu.php
    walker_class_name_ = apply_filters("wp_edit_nav_menu_walker", "Walker_Nav_Menu_Edit", PHP_POST["menu"])
    if (not php_class_exists(walker_class_name_)):
        wp_die(0)
    # end if
    if (not php_empty(lambda : menu_items_)):
        args_ = Array({"after": "", "before": "", "link_after": "", "link_before": "", "walker": php_new_class(walker_class_name_, lambda : {**locals(), **globals()}[walker_class_name_]())})
        php_print(walk_nav_menu_tree(menu_items_, 0, args_))
    # end if
    wp_die()
# end def wp_ajax_add_menu_item
#// 
#// Ajax handler for adding meta.
#// 
#// @since 3.1.0
#//
def wp_ajax_add_meta(*_args_):
    
    
    check_ajax_referer("add-meta", "_ajax_nonce-add-meta")
    c_ = 0
    pid_ = php_int(PHP_POST["post_id"])
    post_ = get_post(pid_)
    if (php_isset(lambda : PHP_POST["metakeyselect"])) or (php_isset(lambda : PHP_POST["metakeyinput"])):
        if (not current_user_can("edit_post", pid_)):
            wp_die(-1)
        # end if
        if (php_isset(lambda : PHP_POST["metakeyselect"])) and "#NONE#" == PHP_POST["metakeyselect"] and php_empty(lambda : PHP_POST["metakeyinput"]):
            wp_die(1)
        # end if
        #// If the post is an autodraft, save the post as a draft and then attempt to save the meta.
        if "auto-draft" == post_.post_status:
            post_data_ = Array()
            post_data_["action"] = "draft"
            #// Warning fix.
            post_data_["post_ID"] = pid_
            post_data_["post_type"] = post_.post_type
            post_data_["post_status"] = "draft"
            now_ = time()
            #// translators: 1: Post creation date, 2: Post creation time.
            post_data_["post_title"] = php_sprintf(__("Draft created on %1$s at %2$s"), gmdate(__("F j, Y"), now_), gmdate(__("g:i a"), now_))
            pid_ = edit_post(post_data_)
            if pid_:
                if is_wp_error(pid_):
                    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "meta", "data": pid_})))
                    x_.send()
                # end if
                mid_ = add_meta(pid_)
                if (not mid_):
                    wp_die(__("Please provide a custom field value."))
                # end if
            else:
                wp_die(0)
            # end if
        else:
            mid_ = add_meta(pid_)
            if (not mid_):
                wp_die(__("Please provide a custom field value."))
            # end if
        # end if
        meta_ = get_metadata_by_mid("post", mid_)
        pid_ = php_int(meta_.post_id)
        meta_ = get_object_vars(meta_)
        x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "meta", "id": mid_, "data": _list_meta_row(meta_, c_), "position": 1, "supplemental": Array({"postid": pid_})})))
    else:
        #// Update?
        mid_ = php_int(key(PHP_POST["meta"]))
        key_ = wp_unslash(PHP_POST["meta"][mid_]["key"])
        value_ = wp_unslash(PHP_POST["meta"][mid_]["value"])
        if "" == php_trim(key_):
            wp_die(__("Please provide a custom field name."))
        # end if
        meta_ = get_metadata_by_mid("post", mid_)
        if (not meta_):
            wp_die(0)
            pass
        # end if
        if is_protected_meta(meta_.meta_key, "post") or is_protected_meta(key_, "post") or (not current_user_can("edit_post_meta", meta_.post_id, meta_.meta_key)) or (not current_user_can("edit_post_meta", meta_.post_id, key_)):
            wp_die(-1)
        # end if
        if meta_.meta_value != value_ or meta_.meta_key != key_:
            u_ = update_metadata_by_mid("post", mid_, value_, key_)
            if (not u_):
                wp_die(0)
                pass
            # end if
        # end if
        x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "meta", "id": mid_, "old_id": mid_, "data": _list_meta_row(Array({"meta_key": key_, "meta_value": value_, "meta_id": mid_}), c_)}, {"position": 0, "supplemental": Array({"postid": meta_.post_id})})))
    # end if
    x_.send()
# end def wp_ajax_add_meta
#// 
#// Ajax handler for adding a user.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_add_user(action_=None, *_args_):
    
    
    if php_empty(lambda : action_):
        action_ = "add-user"
    # end if
    check_ajax_referer(action_)
    if (not current_user_can("create_users")):
        wp_die(-1)
    # end if
    user_id_ = edit_user()
    if (not user_id_):
        wp_die(0)
    elif is_wp_error(user_id_):
        x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "user", "id": user_id_})))
        x_.send()
    # end if
    user_object_ = get_userdata(user_id_)
    wp_list_table_ = _get_list_table("WP_Users_List_Table")
    role_ = current(user_object_.roles)
    x_ = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "user", "id": user_id_, "data": wp_list_table_.single_row(user_object_, "", role_), "supplemental": Array({"show-link": php_sprintf(__("User %s added"), "<a href=\"#user-" + user_id_ + "\">" + user_object_.user_login + "</a>"), "role": role_})})))
    x_.send()
# end def wp_ajax_add_user
#// 
#// Ajax handler for closed post boxes.
#// 
#// @since 3.1.0
#//
def wp_ajax_closed_postboxes(*_args_):
    
    
    check_ajax_referer("closedpostboxes", "closedpostboxesnonce")
    closed_ = php_explode(",", PHP_POST["closed"]) if (php_isset(lambda : PHP_POST["closed"])) else Array()
    closed_ = php_array_filter(closed_)
    hidden_ = php_explode(",", PHP_POST["hidden"]) if (php_isset(lambda : PHP_POST["hidden"])) else Array()
    hidden_ = php_array_filter(hidden_)
    page_ = PHP_POST["page"] if (php_isset(lambda : PHP_POST["page"])) else ""
    if sanitize_key(page_) != page_:
        wp_die(0)
    # end if
    user_ = wp_get_current_user()
    if (not user_):
        wp_die(-1)
    # end if
    if php_is_array(closed_):
        update_user_option(user_.ID, str("closedpostboxes_") + str(page_), closed_, True)
    # end if
    if php_is_array(hidden_):
        #// Postboxes that are always shown.
        hidden_ = php_array_diff(hidden_, Array("submitdiv", "linksubmitdiv", "manage-menu", "create-menu"))
        update_user_option(user_.ID, str("metaboxhidden_") + str(page_), hidden_, True)
    # end if
    wp_die(1)
# end def wp_ajax_closed_postboxes
#// 
#// Ajax handler for hidden columns.
#// 
#// @since 3.1.0
#//
def wp_ajax_hidden_columns(*_args_):
    
    
    check_ajax_referer("screen-options-nonce", "screenoptionnonce")
    page_ = PHP_POST["page"] if (php_isset(lambda : PHP_POST["page"])) else ""
    if sanitize_key(page_) != page_:
        wp_die(0)
    # end if
    user_ = wp_get_current_user()
    if (not user_):
        wp_die(-1)
    # end if
    hidden_ = php_explode(",", PHP_POST["hidden"]) if (not php_empty(lambda : PHP_POST["hidden"])) else Array()
    update_user_option(user_.ID, str("manage") + str(page_) + str("columnshidden"), hidden_, True)
    wp_die(1)
# end def wp_ajax_hidden_columns
#// 
#// Ajax handler for updating whether to display the welcome panel.
#// 
#// @since 3.1.0
#//
def wp_ajax_update_welcome_panel(*_args_):
    
    
    check_ajax_referer("welcome-panel-nonce", "welcomepanelnonce")
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    update_user_meta(get_current_user_id(), "show_welcome_panel", 0 if php_empty(lambda : PHP_POST["visible"]) else 1)
    wp_die(1)
# end def wp_ajax_update_welcome_panel
#// 
#// Ajax handler for retrieving menu meta boxes.
#// 
#// @since 3.1.0
#//
def wp_ajax_menu_get_metabox(*_args_):
    
    
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
    if (php_isset(lambda : PHP_POST["item-type"])) and "post_type" == PHP_POST["item-type"]:
        type_ = "posttype"
        callback_ = "wp_nav_menu_item_post_type_meta_box"
        items_ = get_post_types(Array({"show_in_nav_menus": True}), "object")
    elif (php_isset(lambda : PHP_POST["item-type"])) and "taxonomy" == PHP_POST["item-type"]:
        type_ = "taxonomy"
        callback_ = "wp_nav_menu_item_taxonomy_meta_box"
        items_ = get_taxonomies(Array({"show_ui": True}), "object")
    # end if
    if (not php_empty(lambda : PHP_POST["item-object"])) and (php_isset(lambda : items_[PHP_POST["item-object"]])):
        menus_meta_box_object_ = items_[PHP_POST["item-object"]]
        #// This filter is documented in wp-admin/includes/nav-menu.php
        item_ = apply_filters("nav_menu_meta_box_object", menus_meta_box_object_)
        box_args_ = Array({"id": "add-" + item_.name, "title": item_.labels.name, "callback": callback_, "args": item_})
        ob_start()
        callback_(None, box_args_)
        markup_ = ob_get_clean()
        php_print(wp_json_encode(Array({"replace-id": type_ + "-" + item_.name, "markup": markup_})))
    # end if
    wp_die()
# end def wp_ajax_menu_get_metabox
#// 
#// Ajax handler for internal linking.
#// 
#// @since 3.1.0
#//
def wp_ajax_wp_link_ajax(*_args_):
    
    
    check_ajax_referer("internal-linking", "_ajax_linking_nonce")
    args_ = Array()
    if (php_isset(lambda : PHP_POST["search"])):
        args_["s"] = wp_unslash(PHP_POST["search"])
    # end if
    if (php_isset(lambda : PHP_POST["term"])):
        args_["s"] = wp_unslash(PHP_POST["term"])
    # end if
    args_["pagenum"] = absint(PHP_POST["page"]) if (not php_empty(lambda : PHP_POST["page"])) else 1
    if (not php_class_exists("_WP_Editors", False)):
        php_include_file(ABSPATH + WPINC + "/class-wp-editor.php", once=False)
    # end if
    results_ = _WP_Editors.wp_link_query(args_)
    if (not (php_isset(lambda : results_))):
        wp_die(0)
    # end if
    php_print(wp_json_encode(results_))
    php_print("\n")
    wp_die()
# end def wp_ajax_wp_link_ajax
#// 
#// Ajax handler for menu locations save.
#// 
#// @since 3.1.0
#//
def wp_ajax_menu_locations_save(*_args_):
    
    
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    check_ajax_referer("add-menu_item", "menu-settings-column-nonce")
    if (not (php_isset(lambda : PHP_POST["menu-locations"]))):
        wp_die(0)
    # end if
    set_theme_mod("nav_menu_locations", php_array_map("absint", PHP_POST["menu-locations"]))
    wp_die(1)
# end def wp_ajax_menu_locations_save
#// 
#// Ajax handler for saving the meta box order.
#// 
#// @since 3.1.0
#//
def wp_ajax_meta_box_order(*_args_):
    
    
    check_ajax_referer("meta-box-order")
    order_ = PHP_POST["order"] if (php_isset(lambda : PHP_POST["order"])) else False
    page_columns_ = PHP_POST["page_columns"] if (php_isset(lambda : PHP_POST["page_columns"])) else "auto"
    if "auto" != page_columns_:
        page_columns_ = php_int(page_columns_)
    # end if
    page_ = PHP_POST["page"] if (php_isset(lambda : PHP_POST["page"])) else ""
    if sanitize_key(page_) != page_:
        wp_die(0)
    # end if
    user_ = wp_get_current_user()
    if (not user_):
        wp_die(-1)
    # end if
    if order_:
        update_user_option(user_.ID, str("meta-box-order_") + str(page_), order_, True)
    # end if
    if page_columns_:
        update_user_option(user_.ID, str("screen_layout_") + str(page_), page_columns_, True)
    # end if
    wp_die(1)
# end def wp_ajax_meta_box_order
#// 
#// Ajax handler for menu quick searching.
#// 
#// @since 3.1.0
#//
def wp_ajax_menu_quick_search(*_args_):
    
    
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
    _wp_ajax_menu_quick_search(PHP_POST)
    wp_die()
# end def wp_ajax_menu_quick_search
#// 
#// Ajax handler to retrieve a permalink.
#// 
#// @since 3.1.0
#//
def wp_ajax_get_permalink(*_args_):
    
    
    check_ajax_referer("getpermalink", "getpermalinknonce")
    post_id_ = php_intval(PHP_POST["post_id"]) if (php_isset(lambda : PHP_POST["post_id"])) else 0
    wp_die(get_preview_post_link(post_id_))
# end def wp_ajax_get_permalink
#// 
#// Ajax handler to retrieve a sample permalink.
#// 
#// @since 3.1.0
#//
def wp_ajax_sample_permalink(*_args_):
    
    
    check_ajax_referer("samplepermalink", "samplepermalinknonce")
    post_id_ = php_intval(PHP_POST["post_id"]) if (php_isset(lambda : PHP_POST["post_id"])) else 0
    title_ = PHP_POST["new_title"] if (php_isset(lambda : PHP_POST["new_title"])) else ""
    slug_ = PHP_POST["new_slug"] if (php_isset(lambda : PHP_POST["new_slug"])) else None
    wp_die(get_sample_permalink_html(post_id_, title_, slug_))
# end def wp_ajax_sample_permalink
#// 
#// Ajax handler for Quick Edit saving a post from a list table.
#// 
#// @since 3.1.0
#// 
#// @global string $mode List table view mode.
#//
def wp_ajax_inline_save(*_args_):
    
    
    global mode_
    php_check_if_defined("mode_")
    check_ajax_referer("inlineeditnonce", "_inline_edit")
    if (not (php_isset(lambda : PHP_POST["post_ID"]))) or (not php_int(PHP_POST["post_ID"])):
        wp_die()
    # end if
    post_ID_ = php_int(PHP_POST["post_ID"])
    if "page" == PHP_POST["post_type"]:
        if (not current_user_can("edit_page", post_ID_)):
            wp_die(__("Sorry, you are not allowed to edit this page."))
        # end if
    else:
        if (not current_user_can("edit_post", post_ID_)):
            wp_die(__("Sorry, you are not allowed to edit this post."))
        # end if
    # end if
    last_ = wp_check_post_lock(post_ID_)
    if last_:
        last_user_ = get_userdata(last_)
        last_user_name_ = last_user_.display_name if last_user_ else __("Someone")
        #// translators: %s: User's display name.
        msg_template_ = __("Saving is disabled: %s is currently editing this post.")
        if "page" == PHP_POST["post_type"]:
            #// translators: %s: User's display name.
            msg_template_ = __("Saving is disabled: %s is currently editing this page.")
        # end if
        printf(msg_template_, esc_html(last_user_name_))
        wp_die()
    # end if
    data_ = PHP_POST
    post_ = get_post(post_ID_, ARRAY_A)
    #// Since it's coming from the database.
    post_ = wp_slash(post_)
    data_["content"] = post_["post_content"]
    data_["excerpt"] = post_["post_excerpt"]
    #// Rename.
    data_["user_ID"] = get_current_user_id()
    if (php_isset(lambda : data_["post_parent"])):
        data_["parent_id"] = data_["post_parent"]
    # end if
    #// Status.
    if (php_isset(lambda : data_["keep_private"])) and "private" == data_["keep_private"]:
        data_["visibility"] = "private"
        data_["post_status"] = "private"
    else:
        data_["post_status"] = data_["_status"]
    # end if
    if php_empty(lambda : data_["comment_status"]):
        data_["comment_status"] = "closed"
    # end if
    if php_empty(lambda : data_["ping_status"]):
        data_["ping_status"] = "closed"
    # end if
    #// Exclude terms from taxonomies that are not supposed to appear in Quick Edit.
    if (not php_empty(lambda : data_["tax_input"])):
        for taxonomy_,terms_ in data_["tax_input"]:
            tax_object_ = get_taxonomy(taxonomy_)
            #// This filter is documented in wp-admin/includes/class-wp-posts-list-table.php
            if (not apply_filters("quick_edit_show_taxonomy", tax_object_.show_in_quick_edit, taxonomy_, post_["post_type"])):
                data_["tax_input"][taxonomy_] = None
            # end if
        # end for
    # end if
    #// Hack: wp_unique_post_slug() doesn't work for drafts, so we will fake that our post is published.
    if (not php_empty(lambda : data_["post_name"])) and php_in_array(post_["post_status"], Array("draft", "pending")):
        post_["post_status"] = "publish"
        data_["post_name"] = wp_unique_post_slug(data_["post_name"], post_["ID"], post_["post_status"], post_["post_type"], post_["post_parent"])
    # end if
    #// Update the post.
    edit_post()
    wp_list_table_ = _get_list_table("WP_Posts_List_Table", Array({"screen": PHP_POST["screen"]}))
    mode_ = "excerpt" if "excerpt" == PHP_POST["post_view"] else "list"
    level_ = 0
    if is_post_type_hierarchical(wp_list_table_.screen.post_type):
        request_post_ = Array(get_post(PHP_POST["post_ID"]))
        parent_ = request_post_[0].post_parent
        while True:
            
            if not (parent_ > 0):
                break
            # end if
            parent_post_ = get_post(parent_)
            parent_ = parent_post_.post_parent
            level_ += 1
        # end while
    # end if
    wp_list_table_.display_rows(Array(get_post(PHP_POST["post_ID"])), level_)
    wp_die()
# end def wp_ajax_inline_save
#// 
#// Ajax handler for quick edit saving for a term.
#// 
#// @since 3.1.0
#//
def wp_ajax_inline_save_tax(*_args_):
    
    global PHP_POST
    check_ajax_referer("taxinlineeditnonce", "_inline_edit")
    taxonomy_ = sanitize_key(PHP_POST["taxonomy"])
    tax_ = get_taxonomy(taxonomy_)
    if (not tax_):
        wp_die(0)
    # end if
    if (not (php_isset(lambda : PHP_POST["tax_ID"]))) or (not php_int(PHP_POST["tax_ID"])):
        wp_die(-1)
    # end if
    id_ = php_int(PHP_POST["tax_ID"])
    if (not current_user_can("edit_term", id_)):
        wp_die(-1)
    # end if
    wp_list_table_ = _get_list_table("WP_Terms_List_Table", Array({"screen": "edit-" + taxonomy_}))
    tag_ = get_term(id_, taxonomy_)
    PHP_POST["description"] = tag_.description
    updated_ = wp_update_term(id_, taxonomy_, PHP_POST)
    if updated_ and (not is_wp_error(updated_)):
        tag_ = get_term(updated_["term_id"], taxonomy_)
        if (not tag_) or is_wp_error(tag_):
            if is_wp_error(tag_) and tag_.get_error_message():
                wp_die(tag_.get_error_message())
            # end if
            wp_die(__("Item not updated."))
        # end if
    else:
        if is_wp_error(updated_) and updated_.get_error_message():
            wp_die(updated_.get_error_message())
        # end if
        wp_die(__("Item not updated."))
    # end if
    level_ = 0
    parent_ = tag_.parent
    while True:
        
        if not (parent_ > 0):
            break
        # end if
        parent_tag_ = get_term(parent_, taxonomy_)
        parent_ = parent_tag_.parent
        level_ += 1
    # end while
    wp_list_table_.single_row(tag_, level_)
    wp_die()
# end def wp_ajax_inline_save_tax
#// 
#// Ajax handler for querying posts for the Find Posts modal.
#// 
#// @see window.findPosts
#// 
#// @since 3.1.0
#//
def wp_ajax_find_posts(*_args_):
    
    
    check_ajax_referer("find-posts")
    post_types_ = get_post_types(Array({"public": True}), "objects")
    post_types_["attachment"] = None
    s_ = wp_unslash(PHP_POST["ps"])
    args_ = Array({"post_type": php_array_keys(post_types_), "post_status": "any", "posts_per_page": 50})
    if "" != s_:
        args_["s"] = s_
    # end if
    posts_ = get_posts(args_)
    if (not posts_):
        wp_send_json_error(__("No items found."))
    # end if
    html_ = "<table class=\"widefat\"><thead><tr><th class=\"found-radio\"><br /></th><th>" + __("Title") + "</th><th class=\"no-break\">" + __("Type") + "</th><th class=\"no-break\">" + __("Date") + "</th><th class=\"no-break\">" + __("Status") + "</th></tr></thead><tbody>"
    alt_ = ""
    for post_ in posts_:
        title_ = post_.post_title if php_trim(post_.post_title) else __("(no title)")
        alt_ = "" if "alternate" == alt_ else "alternate"
        for case in Switch(post_.post_status):
            if case("publish"):
                pass
            # end if
            if case("private"):
                stat_ = __("Published")
                break
            # end if
            if case("future"):
                stat_ = __("Scheduled")
                break
            # end if
            if case("pending"):
                stat_ = __("Pending Review")
                break
            # end if
            if case("draft"):
                stat_ = __("Draft")
                break
            # end if
        # end for
        if "0000-00-00 00:00:00" == post_.post_date:
            time_ = ""
        else:
            #// translators: Date format in table columns, see https://www.php.net/date
            time_ = mysql2date(__("Y/m/d"), post_.post_date)
        # end if
        html_ += "<tr class=\"" + php_trim("found-posts " + alt_) + "\"><td class=\"found-radio\"><input type=\"radio\" id=\"found-" + post_.ID + "\" name=\"found_post_id\" value=\"" + esc_attr(post_.ID) + "\"></td>"
        html_ += "<td><label for=\"found-" + post_.ID + "\">" + esc_html(title_) + "</label></td><td class=\"no-break\">" + esc_html(post_types_[post_.post_type].labels.singular_name) + "</td><td class=\"no-break\">" + esc_html(time_) + "</td><td class=\"no-break\">" + esc_html(stat_) + " </td></tr>" + "\n\n"
    # end for
    html_ += "</tbody></table>"
    wp_send_json_success(html_)
# end def wp_ajax_find_posts
#// 
#// Ajax handler for saving the widgets order.
#// 
#// @since 3.1.0
#//
def wp_ajax_widgets_order(*_args_):
    
    
    check_ajax_referer("save-sidebar-widgets", "savewidgets")
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    PHP_POST["savewidgets"] = None
    PHP_POST["action"] = None
    #// Save widgets order for all sidebars.
    if php_is_array(PHP_POST["sidebars"]):
        sidebars_ = Array()
        for key_,val_ in wp_unslash(PHP_POST["sidebars"]):
            sb_ = Array()
            if (not php_empty(lambda : val_)):
                val_ = php_explode(",", val_)
                for k_,v_ in val_:
                    if php_strpos(v_, "widget-") == False:
                        continue
                    # end if
                    sb_[k_] = php_substr(v_, php_strpos(v_, "_") + 1)
                # end for
            # end if
            sidebars_[key_] = sb_
        # end for
        wp_set_sidebars_widgets(sidebars_)
        wp_die(1)
    # end if
    wp_die(-1)
# end def wp_ajax_widgets_order
#// 
#// Ajax handler for saving a widget.
#// 
#// @since 3.1.0
#// 
#// @global array $wp_registered_widgets
#// @global array $wp_registered_widget_controls
#// @global array $wp_registered_widget_updates
#//
def wp_ajax_save_widget(*_args_):
    
    global PHP_POST
    global wp_registered_widgets_
    global wp_registered_widget_controls_
    global wp_registered_widget_updates_
    php_check_if_defined("wp_registered_widgets_","wp_registered_widget_controls_","wp_registered_widget_updates_")
    check_ajax_referer("save-sidebar-widgets", "savewidgets")
    if (not current_user_can("edit_theme_options")) or (not (php_isset(lambda : PHP_POST["id_base"]))):
        wp_die(-1)
    # end if
    PHP_POST["savewidgets"] = None
    PHP_POST["action"] = None
    #// 
    #// Fires early when editing the widgets displayed in sidebars.
    #// 
    #// @since 2.8.0
    #//
    do_action("load-widgets.php")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// 
    #// Fires early when editing the widgets displayed in sidebars.
    #// 
    #// @since 2.8.0
    #//
    do_action("widgets.php")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/widgets.php
    do_action("sidebar_admin_setup")
    id_base_ = wp_unslash(PHP_POST["id_base"])
    widget_id_ = wp_unslash(PHP_POST["widget-id"])
    sidebar_id_ = PHP_POST["sidebar"]
    multi_number_ = php_int(PHP_POST["multi_number"]) if (not php_empty(lambda : PHP_POST["multi_number"])) else 0
    settings_ = PHP_POST["widget-" + id_base_] if (php_isset(lambda : PHP_POST["widget-" + id_base_])) and php_is_array(PHP_POST["widget-" + id_base_]) else False
    error_ = "<p>" + __("An error has occurred. Please reload the page and try again.") + "</p>"
    sidebars_ = wp_get_sidebars_widgets()
    sidebar_ = sidebars_[sidebar_id_] if (php_isset(lambda : sidebars_[sidebar_id_])) else Array()
    #// Delete.
    if (php_isset(lambda : PHP_POST["delete_widget"])) and PHP_POST["delete_widget"]:
        if (not (php_isset(lambda : wp_registered_widgets_[widget_id_]))):
            wp_die(error_)
        # end if
        sidebar_ = php_array_diff(sidebar_, Array(widget_id_))
        PHP_POST = Array({"sidebar": sidebar_id_, "widget-" + id_base_: Array(), "the-widget-id": widget_id_, "delete_widget": "1"})
        #// This action is documented in wp-admin/widgets.php
        do_action("delete_widget", widget_id_, sidebar_id_, id_base_)
    elif settings_ and php_preg_match("/__i__|%i%/", key(settings_)):
        if (not multi_number_):
            wp_die(error_)
        # end if
        PHP_POST["widget-" + id_base_] = Array({multi_number_: reset(settings_)})
        widget_id_ = id_base_ + "-" + multi_number_
        sidebar_[-1] = widget_id_
    # end if
    PHP_POST["widget-id"] = sidebar_
    for name_,control_ in wp_registered_widget_updates_:
        if name_ == id_base_:
            if (not php_is_callable(control_["callback"])):
                continue
            # end if
            ob_start()
            call_user_func_array(control_["callback"], control_["params"])
            ob_end_clean()
            break
        # end if
    # end for
    if (php_isset(lambda : PHP_POST["delete_widget"])) and PHP_POST["delete_widget"]:
        sidebars_[sidebar_id_] = sidebar_
        wp_set_sidebars_widgets(sidebars_)
        php_print(str("deleted:") + str(widget_id_))
        wp_die()
    # end if
    if (not php_empty(lambda : PHP_POST["add_new"])):
        wp_die()
    # end if
    form_ = wp_registered_widget_controls_[widget_id_]
    if form_:
        call_user_func_array(form_["callback"], form_["params"])
    # end if
    wp_die()
# end def wp_ajax_save_widget
#// 
#// Ajax handler for saving a widget.
#// 
#// @since 3.9.0
#// 
#// @global WP_Customize_Manager $wp_customize
#//
def wp_ajax_update_widget(*_args_):
    
    
    global wp_customize_
    php_check_if_defined("wp_customize_")
    wp_customize_.widgets.wp_ajax_update_widget()
# end def wp_ajax_update_widget
#// 
#// Ajax handler for removing inactive widgets.
#// 
#// @since 4.4.0
#//
def wp_ajax_delete_inactive_widgets(*_args_):
    
    
    check_ajax_referer("remove-inactive-widgets", "removeinactivewidgets")
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    PHP_POST["removeinactivewidgets"] = None
    PHP_POST["action"] = None
    #// This action is documented in wp-admin/includes/ajax-actions.php
    do_action("load-widgets.php")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/includes/ajax-actions.php
    do_action("widgets.php")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/widgets.php
    do_action("sidebar_admin_setup")
    sidebars_widgets_ = wp_get_sidebars_widgets()
    for key_,widget_id_ in sidebars_widgets_["wp_inactive_widgets"]:
        pieces_ = php_explode("-", widget_id_)
        multi_number_ = php_array_pop(pieces_)
        id_base_ = php_implode("-", pieces_)
        widget_ = get_option("widget_" + id_base_)
        widget_[multi_number_] = None
        update_option("widget_" + id_base_, widget_)
        sidebars_widgets_["wp_inactive_widgets"][key_] = None
    # end for
    wp_set_sidebars_widgets(sidebars_widgets_)
    wp_die()
# end def wp_ajax_delete_inactive_widgets
#// 
#// Ajax handler for creating missing image sub-sizes for just uploaded images.
#// 
#// @since 5.3.0
#//
def wp_ajax_media_create_image_subsizes(*_args_):
    
    
    check_ajax_referer("media-form")
    if (not current_user_can("upload_files")):
        wp_send_json_error(Array({"message": __("Sorry, you are not allowed to upload files.")}))
    # end if
    if php_empty(lambda : PHP_POST["attachment_id"]):
        wp_send_json_error(Array({"message": __("Upload failed. Please reload and try again.")}))
    # end if
    attachment_id_ = php_int(PHP_POST["attachment_id"])
    if (not php_empty(lambda : PHP_POST["_wp_upload_failed_cleanup"])):
        #// Upload failed. Cleanup.
        if wp_attachment_is_image(attachment_id_) and current_user_can("delete_post", attachment_id_):
            attachment_ = get_post(attachment_id_)
            #// Created at most 10 min ago.
            if attachment_ and time() - strtotime(attachment_.post_date_gmt) < 600:
                wp_delete_attachment(attachment_id_, True)
                wp_send_json_success()
            # end if
        # end if
    # end if
    #// Set a custom header with the attachment_id.
    #// Used by the browser/client to resume creating image sub-sizes after a PHP fatal error.
    if (not php_headers_sent()):
        php_header("X-WP-Upload-Attachment-ID: " + attachment_id_)
    # end if
    #// This can still be pretty slow and cause timeout or out of memory errors.
    #// The js that handles the response would need to also handle HTTP 500 errors.
    wp_update_image_subsizes(attachment_id_)
    if (not php_empty(lambda : PHP_POST["_legacy_support"])):
        #// The old (inline) uploader. Only needs the attachment_id.
        response_ = Array({"id": attachment_id_})
    else:
        #// Media modal and Media Library grid view.
        response_ = wp_prepare_attachment_for_js(attachment_id_)
        if (not response_):
            wp_send_json_error(Array({"message": __("Upload failed.")}))
        # end if
    # end if
    #// At this point the image has been uploaded successfully.
    wp_send_json_success(response_)
# end def wp_ajax_media_create_image_subsizes
#// 
#// Ajax handler for uploading attachments
#// 
#// @since 3.3.0
#//
def wp_ajax_upload_attachment(*_args_):
    
    
    check_ajax_referer("media-form")
    #// 
    #// This function does not use wp_send_json_success() / wp_send_json_error()
    #// as the html4 Plupload handler requires a text/html content-type for older IE.
    #// See https://core.trac.wordpress.org/ticket/31037
    #//
    if (not current_user_can("upload_files")):
        php_print(wp_json_encode(Array({"success": False, "data": Array({"message": __("Sorry, you are not allowed to upload files."), "filename": esc_html(PHP_FILES["async-upload"]["name"])})})))
        wp_die()
    # end if
    if (php_isset(lambda : PHP_REQUEST["post_id"])):
        post_id_ = PHP_REQUEST["post_id"]
        if (not current_user_can("edit_post", post_id_)):
            php_print(wp_json_encode(Array({"success": False, "data": Array({"message": __("Sorry, you are not allowed to attach files to this post."), "filename": esc_html(PHP_FILES["async-upload"]["name"])})})))
            wp_die()
        # end if
    else:
        post_id_ = None
    # end if
    post_data_ = _wp_get_allowed_postdata(_wp_translate_postdata(False, PHP_REQUEST["post_data"])) if (not php_empty(lambda : PHP_REQUEST["post_data"])) else Array()
    if is_wp_error(post_data_):
        wp_die(post_data_.get_error_message())
    # end if
    #// If the context is custom header or background, make sure the uploaded file is an image.
    if (php_isset(lambda : post_data_["context"])) and php_in_array(post_data_["context"], Array("custom-header", "custom-background")):
        wp_filetype_ = wp_check_filetype_and_ext(PHP_FILES["async-upload"]["tmp_name"], PHP_FILES["async-upload"]["name"])
        if (not wp_match_mime_types("image", wp_filetype_["type"])):
            php_print(wp_json_encode(Array({"success": False, "data": Array({"message": __("The uploaded file is not a valid image. Please try again."), "filename": esc_html(PHP_FILES["async-upload"]["name"])})})))
            wp_die()
        # end if
    # end if
    attachment_id_ = media_handle_upload("async-upload", post_id_, post_data_)
    if is_wp_error(attachment_id_):
        php_print(wp_json_encode(Array({"success": False, "data": Array({"message": attachment_id_.get_error_message(), "filename": esc_html(PHP_FILES["async-upload"]["name"])})})))
        wp_die()
    # end if
    if (php_isset(lambda : post_data_["context"])) and (php_isset(lambda : post_data_["theme"])):
        if "custom-background" == post_data_["context"]:
            update_post_meta(attachment_id_, "_wp_attachment_is_custom_background", post_data_["theme"])
        # end if
        if "custom-header" == post_data_["context"]:
            update_post_meta(attachment_id_, "_wp_attachment_is_custom_header", post_data_["theme"])
        # end if
    # end if
    attachment_ = wp_prepare_attachment_for_js(attachment_id_)
    if (not attachment_):
        wp_die()
    # end if
    php_print(wp_json_encode(Array({"success": True, "data": attachment_})))
    wp_die()
# end def wp_ajax_upload_attachment
#// 
#// Ajax handler for image editing.
#// 
#// @since 3.1.0
#//
def wp_ajax_image_editor(*_args_):
    
    
    attachment_id_ = php_intval(PHP_POST["postid"])
    if php_empty(lambda : attachment_id_) or (not current_user_can("edit_post", attachment_id_)):
        wp_die(-1)
    # end if
    check_ajax_referer(str("image_editor-") + str(attachment_id_))
    php_include_file(ABSPATH + "wp-admin/includes/image-edit.php", once=False)
    msg_ = False
    for case in Switch(PHP_POST["do"]):
        if case("save"):
            msg_ = wp_save_image(attachment_id_)
            msg_ = wp_json_encode(msg_)
            wp_die(msg_)
            break
        # end if
        if case("scale"):
            msg_ = wp_save_image(attachment_id_)
            break
        # end if
        if case("restore"):
            msg_ = wp_restore_image(attachment_id_)
            break
        # end if
    # end for
    wp_image_editor(attachment_id_, msg_)
    wp_die()
# end def wp_ajax_image_editor
#// 
#// Ajax handler for setting the featured image.
#// 
#// @since 3.1.0
#//
def wp_ajax_set_post_thumbnail(*_args_):
    
    
    json_ = (not php_empty(lambda : PHP_REQUEST["json"]))
    #// New-style request.
    post_ID_ = php_intval(PHP_POST["post_id"])
    if (not current_user_can("edit_post", post_ID_)):
        wp_die(-1)
    # end if
    thumbnail_id_ = php_intval(PHP_POST["thumbnail_id"])
    if json_:
        check_ajax_referer(str("update-post_") + str(post_ID_))
    else:
        check_ajax_referer(str("set_post_thumbnail-") + str(post_ID_))
    # end if
    if "-1" == thumbnail_id_:
        if delete_post_thumbnail(post_ID_):
            return_ = _wp_post_thumbnail_html(None, post_ID_)
            wp_send_json_success(return_) if json_ else wp_die(return_)
        else:
            wp_die(0)
        # end if
    # end if
    if set_post_thumbnail(post_ID_, thumbnail_id_):
        return_ = _wp_post_thumbnail_html(thumbnail_id_, post_ID_)
        wp_send_json_success(return_) if json_ else wp_die(return_)
    # end if
    wp_die(0)
# end def wp_ajax_set_post_thumbnail
#// 
#// Ajax handler for retrieving HTML for the featured image.
#// 
#// @since 4.6.0
#//
def wp_ajax_get_post_thumbnail_html(*_args_):
    
    
    post_ID_ = php_intval(PHP_POST["post_id"])
    check_ajax_referer(str("update-post_") + str(post_ID_))
    if (not current_user_can("edit_post", post_ID_)):
        wp_die(-1)
    # end if
    thumbnail_id_ = php_intval(PHP_POST["thumbnail_id"])
    #// For backward compatibility, -1 refers to no featured image.
    if -1 == thumbnail_id_:
        thumbnail_id_ = None
    # end if
    return_ = _wp_post_thumbnail_html(thumbnail_id_, post_ID_)
    wp_send_json_success(return_)
# end def wp_ajax_get_post_thumbnail_html
#// 
#// Ajax handler for setting the featured image for an attachment.
#// 
#// @since 4.0.0
#// 
#// @see set_post_thumbnail()
#//
def wp_ajax_set_attachment_thumbnail(*_args_):
    
    
    if php_empty(lambda : PHP_POST["urls"]) or (not php_is_array(PHP_POST["urls"])):
        wp_send_json_error()
    # end if
    thumbnail_id_ = php_int(PHP_POST["thumbnail_id"])
    if php_empty(lambda : thumbnail_id_):
        wp_send_json_error()
    # end if
    post_ids_ = Array()
    #// For each URL, try to find its corresponding post ID.
    for url_ in PHP_POST["urls"]:
        post_id_ = attachment_url_to_postid(url_)
        if (not php_empty(lambda : post_id_)):
            post_ids_[-1] = post_id_
        # end if
    # end for
    if php_empty(lambda : post_ids_):
        wp_send_json_error()
    # end if
    success_ = 0
    #// For each found attachment, set its thumbnail.
    for post_id_ in post_ids_:
        if (not current_user_can("edit_post", post_id_)):
            continue
        # end if
        if set_post_thumbnail(post_id_, thumbnail_id_):
            success_ += 1
        # end if
    # end for
    if 0 == success_:
        wp_send_json_error()
    else:
        wp_send_json_success()
    # end if
    wp_send_json_error()
# end def wp_ajax_set_attachment_thumbnail
#// 
#// Ajax handler for date formatting.
#// 
#// @since 3.1.0
#//
def wp_ajax_date_format(*_args_):
    
    
    wp_die(date_i18n(sanitize_option("date_format", wp_unslash(PHP_POST["date"]))))
# end def wp_ajax_date_format
#// 
#// Ajax handler for time formatting.
#// 
#// @since 3.1.0
#//
def wp_ajax_time_format(*_args_):
    
    
    wp_die(date_i18n(sanitize_option("time_format", wp_unslash(PHP_POST["date"]))))
# end def wp_ajax_time_format
#// 
#// Ajax handler for saving posts from the fullscreen editor.
#// 
#// @since 3.1.0
#// @deprecated 4.3.0
#//
def wp_ajax_wp_fullscreen_save_post(*_args_):
    
    
    post_id_ = php_int(PHP_POST["post_ID"]) if (php_isset(lambda : PHP_POST["post_ID"])) else 0
    post_ = None
    if post_id_:
        post_ = get_post(post_id_)
    # end if
    check_ajax_referer("update-post_" + post_id_, "_wpnonce")
    post_id_ = edit_post()
    if is_wp_error(post_id_):
        wp_send_json_error()
    # end if
    if post_:
        last_date_ = mysql2date(__("F j, Y"), post_.post_modified)
        last_time_ = mysql2date(__("g:i a"), post_.post_modified)
    else:
        last_date_ = date_i18n(__("F j, Y"))
        last_time_ = date_i18n(__("g:i a"))
    # end if
    last_id_ = get_post_meta(post_id_, "_edit_last", True)
    if last_id_:
        last_user_ = get_userdata(last_id_)
        #// translators: 1: User's display name, 2: Date of last edit, 3: Time of last edit.
        last_edited_ = php_sprintf(__("Last edited by %1$s on %2$s at %3$s"), esc_html(last_user_.display_name), last_date_, last_time_)
    else:
        #// translators: 1: Date of last edit, 2: Time of last edit.
        last_edited_ = php_sprintf(__("Last edited on %1$s at %2$s"), last_date_, last_time_)
    # end if
    wp_send_json_success(Array({"last_edited": last_edited_}))
# end def wp_ajax_wp_fullscreen_save_post
#// 
#// Ajax handler for removing a post lock.
#// 
#// @since 3.1.0
#//
def wp_ajax_wp_remove_post_lock(*_args_):
    
    
    if php_empty(lambda : PHP_POST["post_ID"]) or php_empty(lambda : PHP_POST["active_post_lock"]):
        wp_die(0)
    # end if
    post_id_ = php_int(PHP_POST["post_ID"])
    post_ = get_post(post_id_)
    if (not post_):
        wp_die(0)
    # end if
    check_ajax_referer("update-post_" + post_id_)
    if (not current_user_can("edit_post", post_id_)):
        wp_die(-1)
    # end if
    active_lock_ = php_array_map("absint", php_explode(":", PHP_POST["active_post_lock"]))
    if get_current_user_id() != active_lock_[1]:
        wp_die(0)
    # end if
    #// 
    #// Filters the post lock window duration.
    #// 
    #// @since 3.3.0
    #// 
    #// @param int $interval The interval in seconds the post lock duration
    #// should last, plus 5 seconds. Default 150.
    #//
    new_lock_ = time() - apply_filters("wp_check_post_lock_window", 150) + 5 + ":" + active_lock_[1]
    update_post_meta(post_id_, "_edit_lock", new_lock_, php_implode(":", active_lock_))
    wp_die(1)
# end def wp_ajax_wp_remove_post_lock
#// 
#// Ajax handler for dismissing a WordPress pointer.
#// 
#// @since 3.1.0
#//
def wp_ajax_dismiss_wp_pointer(*_args_):
    
    
    pointer_ = PHP_POST["pointer"]
    if sanitize_key(pointer_) != pointer_:
        wp_die(0)
    # end if
    #// check_ajax_referer( 'dismiss-pointer_' . $pointer );
    dismissed_ = php_array_filter(php_explode(",", php_str(get_user_meta(get_current_user_id(), "dismissed_wp_pointers", True))))
    if php_in_array(pointer_, dismissed_):
        wp_die(0)
    # end if
    dismissed_[-1] = pointer_
    dismissed_ = php_implode(",", dismissed_)
    update_user_meta(get_current_user_id(), "dismissed_wp_pointers", dismissed_)
    wp_die(1)
# end def wp_ajax_dismiss_wp_pointer
#// 
#// Ajax handler for getting an attachment.
#// 
#// @since 3.5.0
#//
def wp_ajax_get_attachment(*_args_):
    
    
    if (not (php_isset(lambda : PHP_REQUEST["id"]))):
        wp_send_json_error()
    # end if
    id_ = absint(PHP_REQUEST["id"])
    if (not id_):
        wp_send_json_error()
    # end if
    post_ = get_post(id_)
    if (not post_):
        wp_send_json_error()
    # end if
    if "attachment" != post_.post_type:
        wp_send_json_error()
    # end if
    if (not current_user_can("upload_files")):
        wp_send_json_error()
    # end if
    attachment_ = wp_prepare_attachment_for_js(id_)
    if (not attachment_):
        wp_send_json_error()
    # end if
    wp_send_json_success(attachment_)
# end def wp_ajax_get_attachment
#// 
#// Ajax handler for querying attachments.
#// 
#// @since 3.5.0
#//
def wp_ajax_query_attachments(*_args_):
    
    
    if (not current_user_can("upload_files")):
        wp_send_json_error()
    # end if
    query_ = PHP_REQUEST["query"] if (php_isset(lambda : PHP_REQUEST["query"])) else Array()
    keys_ = Array("s", "order", "orderby", "posts_per_page", "paged", "post_mime_type", "post_parent", "author", "post__in", "post__not_in", "year", "monthnum")
    for t_ in get_taxonomies_for_attachments("objects"):
        if t_.query_var and (php_isset(lambda : query_[t_.query_var])):
            keys_[-1] = t_.query_var
        # end if
    # end for
    query_ = php_array_intersect_key(query_, php_array_flip(keys_))
    query_["post_type"] = "attachment"
    if MEDIA_TRASH and (not php_empty(lambda : PHP_REQUEST["query"]["post_status"])) and "trash" == PHP_REQUEST["query"]["post_status"]:
        query_["post_status"] = "trash"
    else:
        query_["post_status"] = "inherit"
    # end if
    if current_user_can(get_post_type_object("attachment").cap.read_private_posts):
        query_["post_status"] += ",private"
    # end if
    #// Filter query clauses to include filenames.
    if (php_isset(lambda : query_["s"])):
        add_filter("posts_clauses", "_filter_query_attachment_filenames")
    # end if
    #// 
    #// Filters the arguments passed to WP_Query during an Ajax
    #// call for querying attachments.
    #// 
    #// @since 3.7.0
    #// 
    #// @see WP_Query::parse_query()
    #// 
    #// @param array $query An array of query variables.
    #//
    query_ = apply_filters("ajax_query_attachments_args", query_)
    query_ = php_new_class("WP_Query", lambda : WP_Query(query_))
    posts_ = php_array_map("wp_prepare_attachment_for_js", query_.posts)
    posts_ = php_array_filter(posts_)
    wp_send_json_success(posts_)
# end def wp_ajax_query_attachments
#// 
#// Ajax handler for updating attachment attributes.
#// 
#// @since 3.5.0
#//
def wp_ajax_save_attachment(*_args_):
    
    
    if (not (php_isset(lambda : PHP_REQUEST["id"]))) or (not (php_isset(lambda : PHP_REQUEST["changes"]))):
        wp_send_json_error()
    # end if
    id_ = absint(PHP_REQUEST["id"])
    if (not id_):
        wp_send_json_error()
    # end if
    check_ajax_referer("update-post_" + id_, "nonce")
    if (not current_user_can("edit_post", id_)):
        wp_send_json_error()
    # end if
    changes_ = PHP_REQUEST["changes"]
    post_ = get_post(id_, ARRAY_A)
    if "attachment" != post_["post_type"]:
        wp_send_json_error()
    # end if
    if (php_isset(lambda : changes_["parent"])):
        post_["post_parent"] = changes_["parent"]
    # end if
    if (php_isset(lambda : changes_["title"])):
        post_["post_title"] = changes_["title"]
    # end if
    if (php_isset(lambda : changes_["caption"])):
        post_["post_excerpt"] = changes_["caption"]
    # end if
    if (php_isset(lambda : changes_["description"])):
        post_["post_content"] = changes_["description"]
    # end if
    if MEDIA_TRASH and (php_isset(lambda : changes_["status"])):
        post_["post_status"] = changes_["status"]
    # end if
    if (php_isset(lambda : changes_["alt"])):
        alt_ = wp_unslash(changes_["alt"])
        if get_post_meta(id_, "_wp_attachment_image_alt", True) != alt_:
            alt_ = wp_strip_all_tags(alt_, True)
            update_post_meta(id_, "_wp_attachment_image_alt", wp_slash(alt_))
        # end if
    # end if
    if wp_attachment_is("audio", post_["ID"]):
        changed_ = False
        id3data_ = wp_get_attachment_metadata(post_["ID"])
        if (not php_is_array(id3data_)):
            changed_ = True
            id3data_ = Array()
        # end if
        for key_,label_ in wp_get_attachment_id3_keys(post_, "edit"):
            if (php_isset(lambda : changes_[key_])):
                changed_ = True
                id3data_[key_] = sanitize_text_field(wp_unslash(changes_[key_]))
            # end if
        # end for
        if changed_:
            wp_update_attachment_metadata(id_, id3data_)
        # end if
    # end if
    if MEDIA_TRASH and (php_isset(lambda : changes_["status"])) and "trash" == changes_["status"]:
        wp_delete_post(id_)
    else:
        wp_update_post(post_)
    # end if
    wp_send_json_success()
# end def wp_ajax_save_attachment
#// 
#// Ajax handler for saving backward compatible attachment attributes.
#// 
#// @since 3.5.0
#//
def wp_ajax_save_attachment_compat(*_args_):
    
    
    if (not (php_isset(lambda : PHP_REQUEST["id"]))):
        wp_send_json_error()
    # end if
    id_ = absint(PHP_REQUEST["id"])
    if (not id_):
        wp_send_json_error()
    # end if
    if php_empty(lambda : PHP_REQUEST["attachments"]) or php_empty(lambda : PHP_REQUEST["attachments"][id_]):
        wp_send_json_error()
    # end if
    attachment_data_ = PHP_REQUEST["attachments"][id_]
    check_ajax_referer("update-post_" + id_, "nonce")
    if (not current_user_can("edit_post", id_)):
        wp_send_json_error()
    # end if
    post_ = get_post(id_, ARRAY_A)
    if "attachment" != post_["post_type"]:
        wp_send_json_error()
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    post_ = apply_filters("attachment_fields_to_save", post_, attachment_data_)
    if (php_isset(lambda : post_["errors"])):
        errors_ = post_["errors"]
        post_["errors"] = None
    # end if
    wp_update_post(post_)
    for taxonomy_ in get_attachment_taxonomies(post_):
        if (php_isset(lambda : attachment_data_[taxonomy_])):
            wp_set_object_terms(id_, php_array_map("trim", php_preg_split("/,+/", attachment_data_[taxonomy_])), taxonomy_, False)
        # end if
    # end for
    attachment_ = wp_prepare_attachment_for_js(id_)
    if (not attachment_):
        wp_send_json_error()
    # end if
    wp_send_json_success(attachment_)
# end def wp_ajax_save_attachment_compat
#// 
#// Ajax handler for saving the attachment order.
#// 
#// @since 3.5.0
#//
def wp_ajax_save_attachment_order(*_args_):
    
    
    if (not (php_isset(lambda : PHP_REQUEST["post_id"]))):
        wp_send_json_error()
    # end if
    post_id_ = absint(PHP_REQUEST["post_id"])
    if (not post_id_):
        wp_send_json_error()
    # end if
    if php_empty(lambda : PHP_REQUEST["attachments"]):
        wp_send_json_error()
    # end if
    check_ajax_referer("update-post_" + post_id_, "nonce")
    attachments_ = PHP_REQUEST["attachments"]
    if (not current_user_can("edit_post", post_id_)):
        wp_send_json_error()
    # end if
    for attachment_id_,menu_order_ in attachments_:
        if (not current_user_can("edit_post", attachment_id_)):
            continue
        # end if
        attachment_ = get_post(attachment_id_)
        if (not attachment_):
            continue
        # end if
        if "attachment" != attachment_.post_type:
            continue
        # end if
        wp_update_post(Array({"ID": attachment_id_, "menu_order": menu_order_}))
    # end for
    wp_send_json_success()
# end def wp_ajax_save_attachment_order
#// 
#// Ajax handler for sending an attachment to the editor.
#// 
#// Generates the HTML to send an attachment to the editor.
#// Backward compatible with the {@see 'media_send_to_editor'} filter
#// and the chain of filters that follow.
#// 
#// @since 3.5.0
#//
def wp_ajax_send_attachment_to_editor(*_args_):
    
    
    check_ajax_referer("media-send-to-editor", "nonce")
    attachment_ = wp_unslash(PHP_POST["attachment"])
    id_ = php_intval(attachment_["id"])
    post_ = get_post(id_)
    if (not post_):
        wp_send_json_error()
    # end if
    if "attachment" != post_.post_type:
        wp_send_json_error()
    # end if
    if current_user_can("edit_post", id_):
        #// If this attachment is unattached, attach it. Primarily a back compat thing.
        insert_into_post_id_ = php_intval(PHP_POST["post_id"])
        if 0 == post_.post_parent and insert_into_post_id_:
            wp_update_post(Array({"ID": id_, "post_parent": insert_into_post_id_}))
        # end if
    # end if
    url_ = "" if php_empty(lambda : attachment_["url"]) else attachment_["url"]
    rel_ = php_strpos(url_, "attachment_id") or get_attachment_link(id_) == url_
    remove_filter("media_send_to_editor", "image_media_send_to_editor")
    if "image" == php_substr(post_.post_mime_type, 0, 5):
        align_ = attachment_["align"] if (php_isset(lambda : attachment_["align"])) else "none"
        size_ = attachment_["image-size"] if (php_isset(lambda : attachment_["image-size"])) else "medium"
        alt_ = attachment_["image_alt"] if (php_isset(lambda : attachment_["image_alt"])) else ""
        #// No whitespace-only captions.
        caption_ = attachment_["post_excerpt"] if (php_isset(lambda : attachment_["post_excerpt"])) else ""
        if "" == php_trim(caption_):
            caption_ = ""
        # end if
        title_ = ""
        #// We no longer insert title tags into <img> tags, as they are redundant.
        html_ = get_image_send_to_editor(id_, caption_, title_, align_, url_, rel_, size_, alt_)
    elif wp_attachment_is("video", post_) or wp_attachment_is("audio", post_):
        html_ = stripslashes_deep(PHP_POST["html"])
    else:
        html_ = attachment_["post_title"] if (php_isset(lambda : attachment_["post_title"])) else ""
        rel_ = " rel=\"attachment wp-att-" + id_ + "\"" if rel_ else ""
        #// Hard-coded string, $id is already sanitized.
        if (not php_empty(lambda : url_)):
            html_ = "<a href=\"" + esc_url(url_) + "\"" + rel_ + ">" + html_ + "</a>"
        # end if
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    html_ = apply_filters("media_send_to_editor", html_, id_, attachment_)
    wp_send_json_success(html_)
# end def wp_ajax_send_attachment_to_editor
#// 
#// Ajax handler for sending a link to the editor.
#// 
#// Generates the HTML to send a non-image embed link to the editor.
#// 
#// Backward compatible with the following filters:
#// - file_send_to_editor_url
#// - audio_send_to_editor_url
#// - video_send_to_editor_url
#// 
#// @since 3.5.0
#// 
#// @global WP_Post  $post     Global post object.
#// @global WP_Embed $wp_embed
#//
def wp_ajax_send_link_to_editor(*_args_):
    
    
    global post_
    global wp_embed_
    php_check_if_defined("post_","wp_embed_")
    check_ajax_referer("media-send-to-editor", "nonce")
    src_ = wp_unslash(PHP_POST["src"])
    if (not src_):
        wp_send_json_error()
    # end if
    if (not php_strpos(src_, "://")):
        src_ = "http://" + src_
    # end if
    src_ = esc_url_raw(src_)
    if (not src_):
        wp_send_json_error()
    # end if
    link_text_ = php_trim(wp_unslash(PHP_POST["link_text"]))
    if (not link_text_):
        link_text_ = wp_basename(src_)
    # end if
    post_ = get_post(PHP_POST["post_id"] if (php_isset(lambda : PHP_POST["post_id"])) else 0)
    #// Ping WordPress for an embed.
    check_embed_ = wp_embed_.run_shortcode("[embed]" + src_ + "[/embed]")
    #// Fallback that WordPress creates when no oEmbed was found.
    fallback_ = wp_embed_.maybe_make_link(src_)
    if check_embed_ != fallback_:
        #// TinyMCE view for [embed] will parse this.
        html_ = "[embed]" + src_ + "[/embed]"
    elif link_text_:
        html_ = "<a href=\"" + esc_url(src_) + "\">" + link_text_ + "</a>"
    else:
        html_ = ""
    # end if
    #// Figure out what filter to run:
    type_ = "file"
    ext_ = php_preg_replace("/^.+?\\.([^.]+)$/", "$1", src_)
    if ext_:
        ext_type_ = wp_ext2type(ext_)
        if "audio" == ext_type_ or "video" == ext_type_:
            type_ = ext_type_
        # end if
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    html_ = apply_filters(str(type_) + str("_send_to_editor_url"), html_, src_, link_text_)
    wp_send_json_success(html_)
# end def wp_ajax_send_link_to_editor
#// 
#// Ajax handler for the Heartbeat API.
#// 
#// Runs when the user is logged in.
#// 
#// @since 3.6.0
#//
def wp_ajax_heartbeat(*_args_):
    
    
    if php_empty(lambda : PHP_POST["_nonce"]):
        wp_send_json_error()
    # end if
    response_ = Array()
    data_ = Array()
    nonce_state_ = wp_verify_nonce(PHP_POST["_nonce"], "heartbeat-nonce")
    #// 'screen_id' is the same as $current_screen->id and the JS global 'pagenow'.
    if (not php_empty(lambda : PHP_POST["screen_id"])):
        screen_id_ = sanitize_key(PHP_POST["screen_id"])
    else:
        screen_id_ = "front"
    # end if
    if (not php_empty(lambda : PHP_POST["data"])):
        data_ = wp_unslash(PHP_POST["data"])
    # end if
    if 1 != nonce_state_:
        #// 
        #// Filters the nonces to send to the New/Edit Post screen.
        #// 
        #// @since 4.3.0
        #// 
        #// @param array  $response  The Heartbeat response.
        #// @param array  $data      The $_POST data sent.
        #// @param string $screen_id The screen id.
        #//
        response_ = apply_filters("wp_refresh_nonces", response_, data_, screen_id_)
        if False == nonce_state_:
            #// User is logged in but nonces have expired.
            response_["nonces_expired"] = True
            wp_send_json(response_)
        # end if
    # end if
    if (not php_empty(lambda : data_)):
        #// 
        #// Filters the Heartbeat response received.
        #// 
        #// @since 3.6.0
        #// 
        #// @param array  $response  The Heartbeat response.
        #// @param array  $data      The $_POST data sent.
        #// @param string $screen_id The screen id.
        #//
        response_ = apply_filters("heartbeat_received", response_, data_, screen_id_)
    # end if
    #// 
    #// Filters the Heartbeat response sent.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array  $response  The Heartbeat response.
    #// @param string $screen_id The screen id.
    #//
    response_ = apply_filters("heartbeat_send", response_, screen_id_)
    #// 
    #// Fires when Heartbeat ticks in logged-in environments.
    #// 
    #// Allows the transport to be easily replaced with long-polling.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array  $response  The Heartbeat response.
    #// @param string $screen_id The screen id.
    #//
    do_action("heartbeat_tick", response_, screen_id_)
    #// Send the current time according to the server.
    response_["server_time"] = time()
    wp_send_json(response_)
# end def wp_ajax_heartbeat
#// 
#// Ajax handler for getting revision diffs.
#// 
#// @since 3.6.0
#//
def wp_ajax_get_revision_diffs(*_args_):
    
    
    php_include_file(ABSPATH + "wp-admin/includes/revision.php", once=False)
    post_ = get_post(php_int(PHP_REQUEST["post_id"]))
    if (not post_):
        wp_send_json_error()
    # end if
    if (not current_user_can("edit_post", post_.ID)):
        wp_send_json_error()
    # end if
    #// Really just pre-loading the cache here.
    revisions_ = wp_get_post_revisions(post_.ID, Array({"check_enabled": False}))
    if (not revisions_):
        wp_send_json_error()
    # end if
    return_ = Array()
    set_time_limit(0)
    for compare_key_ in PHP_REQUEST["compare"]:
        compare_from_, compare_to_ = php_explode(":", compare_key_)
        #// from:to
        return_[-1] = Array({"id": compare_key_, "fields": wp_get_revision_ui_diff(post_, compare_from_, compare_to_)})
    # end for
    wp_send_json_success(return_)
# end def wp_ajax_get_revision_diffs
#// 
#// Ajax handler for auto-saving the selected color scheme for
#// a user's own profile.
#// 
#// @since 3.8.0
#// 
#// @global array $_wp_admin_css_colors
#//
def wp_ajax_save_user_color_scheme(*_args_):
    
    
    global _wp_admin_css_colors_
    php_check_if_defined("_wp_admin_css_colors_")
    check_ajax_referer("save-color-scheme", "nonce")
    color_scheme_ = sanitize_key(PHP_POST["color_scheme"])
    if (not (php_isset(lambda : _wp_admin_css_colors_[color_scheme_]))):
        wp_send_json_error()
    # end if
    previous_color_scheme_ = get_user_meta(get_current_user_id(), "admin_color", True)
    update_user_meta(get_current_user_id(), "admin_color", color_scheme_)
    wp_send_json_success(Array({"previousScheme": "admin-color-" + previous_color_scheme_, "currentScheme": "admin-color-" + color_scheme_}))
# end def wp_ajax_save_user_color_scheme
#// 
#// Ajax handler for getting themes from themes_api().
#// 
#// @since 3.9.0
#// 
#// @global array $themes_allowedtags
#// @global array $theme_field_defaults
#//
def wp_ajax_query_themes(*_args_):
    
    
    global themes_allowedtags_
    global theme_field_defaults_
    php_check_if_defined("themes_allowedtags_","theme_field_defaults_")
    if (not current_user_can("install_themes")):
        wp_send_json_error()
    # end if
    args_ = wp_parse_args(wp_unslash(PHP_REQUEST["request"]), Array({"per_page": 20, "fields": php_array_merge(theme_field_defaults_, Array({"reviews_url": True}))}))
    if (php_isset(lambda : args_["browse"])) and "favorites" == args_["browse"] and (not (php_isset(lambda : args_["user"]))):
        user_ = get_user_option("wporg_favorites")
        if user_:
            args_["user"] = user_
        # end if
    # end if
    old_filter_ = args_["browse"] if (php_isset(lambda : args_["browse"])) else "search"
    #// This filter is documented in wp-admin/includes/class-wp-theme-install-list-table.php
    args_ = apply_filters("install_themes_table_api_args_" + old_filter_, args_)
    api_ = themes_api("query_themes", args_)
    if is_wp_error(api_):
        wp_send_json_error()
    # end if
    update_php_ = network_admin_url("update.php?action=install-theme")
    for theme_ in api_.themes:
        theme_.install_url = add_query_arg(Array({"theme": theme_.slug, "_wpnonce": wp_create_nonce("install-theme_" + theme_.slug)}), update_php_)
        if current_user_can("switch_themes"):
            if is_multisite():
                theme_.activate_url = add_query_arg(Array({"action": "enable", "_wpnonce": wp_create_nonce("enable-theme_" + theme_.slug), "theme": theme_.slug}), network_admin_url("themes.php"))
            else:
                theme_.activate_url = add_query_arg(Array({"action": "activate", "_wpnonce": wp_create_nonce("switch-theme_" + theme_.slug), "stylesheet": theme_.slug}), admin_url("themes.php"))
            # end if
        # end if
        if (not is_multisite()) and current_user_can("edit_theme_options") and current_user_can("customize"):
            theme_.customize_url = add_query_arg(Array({"return": urlencode(network_admin_url("theme-install.php", "relative"))}), wp_customize_url(theme_.slug))
        # end if
        theme_.name = wp_kses(theme_.name, themes_allowedtags_)
        theme_.author = wp_kses(theme_.author["display_name"], themes_allowedtags_)
        theme_.version = wp_kses(theme_.version, themes_allowedtags_)
        theme_.description = wp_kses(theme_.description, themes_allowedtags_)
        theme_.stars = wp_star_rating(Array({"rating": theme_.rating, "type": "percent", "number": theme_.num_ratings, "echo": False}))
        theme_.num_ratings = number_format_i18n(theme_.num_ratings)
        theme_.preview_url = set_url_scheme(theme_.preview_url)
    # end for
    wp_send_json_success(api_)
# end def wp_ajax_query_themes
#// 
#// Apply [embed] Ajax handlers to a string.
#// 
#// @since 4.0.0
#// 
#// @global WP_Post    $post       Global post object.
#// @global WP_Embed   $wp_embed   Embed API instance.
#// @global WP_Scripts $wp_scripts
#// @global int        $content_width
#//
def wp_ajax_parse_embed(*_args_):
    
    
    global post_
    global wp_embed_
    global content_width_
    php_check_if_defined("post_","wp_embed_","content_width_")
    if php_empty(lambda : PHP_POST["shortcode"]):
        wp_send_json_error()
    # end if
    post_id_ = php_intval(PHP_POST["post_ID"]) if (php_isset(lambda : PHP_POST["post_ID"])) else 0
    if post_id_ > 0:
        post_ = get_post(post_id_)
        if (not post_) or (not current_user_can("edit_post", post_.ID)):
            wp_send_json_error()
        # end if
        setup_postdata(post_)
    elif (not current_user_can("edit_posts")):
        #// See WP_oEmbed_Controller::get_proxy_item_permissions_check().
        wp_send_json_error()
    # end if
    shortcode_ = wp_unslash(PHP_POST["shortcode"])
    php_preg_match("/" + get_shortcode_regex() + "/s", shortcode_, matches_)
    atts_ = shortcode_parse_atts(matches_[3])
    if (not php_empty(lambda : matches_[5])):
        url_ = matches_[5]
    elif (not php_empty(lambda : atts_["src"])):
        url_ = atts_["src"]
    else:
        url_ = ""
    # end if
    parsed_ = False
    wp_embed_.return_false_on_fail = True
    if 0 == post_id_:
        #// 
        #// Refresh oEmbeds cached outside of posts that are past their TTL.
        #// Posts are excluded because they have separate logic for refreshing
        #// their post meta caches. See WP_Embed::cache_oembed().
        #//
        wp_embed_.usecache = False
    # end if
    if is_ssl() and 0 == php_strpos(url_, "http://"):
        #// Admin is ssl and the user pasted non-ssl URL.
        #// Check if the provider supports ssl embeds and use that for the preview.
        ssl_shortcode_ = php_preg_replace("%^(\\[embed[^\\]]*\\])http://%i", "$1https://", shortcode_)
        parsed_ = wp_embed_.run_shortcode(ssl_shortcode_)
        if (not parsed_):
            no_ssl_support_ = True
        # end if
    # end if
    #// Set $content_width so any embeds fit in the destination iframe.
    if (php_isset(lambda : PHP_POST["maxwidth"])) and php_is_numeric(PHP_POST["maxwidth"]) and PHP_POST["maxwidth"] > 0:
        if (not (php_isset(lambda : content_width_))):
            content_width_ = php_intval(PHP_POST["maxwidth"])
        else:
            content_width_ = php_min(content_width_, php_intval(PHP_POST["maxwidth"]))
        # end if
    # end if
    if url_ and (not parsed_):
        parsed_ = wp_embed_.run_shortcode(shortcode_)
    # end if
    if (not parsed_):
        wp_send_json_error(Array({"type": "not-embeddable", "message": php_sprintf(__("%s failed to embed."), "<code>" + esc_html(url_) + "</code>")}))
    # end if
    if has_shortcode(parsed_, "audio") or has_shortcode(parsed_, "video"):
        styles_ = ""
        mce_styles_ = wpview_media_sandbox_styles()
        for style_ in mce_styles_:
            styles_ += php_sprintf("<link rel=\"stylesheet\" href=\"%s\"/>", style_)
        # end for
        html_ = do_shortcode(parsed_)
        global wp_scripts_
        php_check_if_defined("wp_scripts_")
        if (not php_empty(lambda : wp_scripts_)):
            wp_scripts_.done = Array()
        # end if
        ob_start()
        wp_print_scripts(Array("mediaelement-vimeo", "wp-mediaelement"))
        scripts_ = ob_get_clean()
        parsed_ = styles_ + html_ + scripts_
    # end if
    if (not php_empty(lambda : no_ssl_support_)) or is_ssl() and php_preg_match("%<(iframe|script|embed) [^>]*src=\"http://%", parsed_) or php_preg_match("%<link [^>]*href=\"http://%", parsed_):
        #// Admin is ssl and the embed is not. Iframes, scripts, and other "active content" will be blocked.
        wp_send_json_error(Array({"type": "not-ssl", "message": __("This preview is unavailable in the editor.")}))
    # end if
    return_ = Array({"body": parsed_, "attr": wp_embed_.last_attr})
    if php_strpos(parsed_, "class=\"wp-embedded-content"):
        if php_defined("SCRIPT_DEBUG") and SCRIPT_DEBUG:
            script_src_ = includes_url("js/wp-embed.js")
        else:
            script_src_ = includes_url("js/wp-embed.min.js")
        # end if
        return_["head"] = "<script src=\"" + script_src_ + "\"></script>"
        return_["sandbox"] = True
    # end if
    wp_send_json_success(return_)
# end def wp_ajax_parse_embed
#// 
#// @since 4.0.0
#// 
#// @global WP_Post    $post       Global post object.
#// @global WP_Scripts $wp_scripts
#//
def wp_ajax_parse_media_shortcode(*_args_):
    
    
    global post_
    global wp_scripts_
    php_check_if_defined("post_","wp_scripts_")
    if php_empty(lambda : PHP_POST["shortcode"]):
        wp_send_json_error()
    # end if
    shortcode_ = wp_unslash(PHP_POST["shortcode"])
    if (not php_empty(lambda : PHP_POST["post_ID"])):
        post_ = get_post(php_int(PHP_POST["post_ID"]))
    # end if
    #// The embed shortcode requires a post.
    if (not post_) or (not current_user_can("edit_post", post_.ID)):
        if "embed" == shortcode_:
            wp_send_json_error()
        # end if
    else:
        setup_postdata(post_)
    # end if
    parsed_ = do_shortcode(shortcode_)
    if php_empty(lambda : parsed_):
        wp_send_json_error(Array({"type": "no-items", "message": __("No items found.")}))
    # end if
    head_ = ""
    styles_ = wpview_media_sandbox_styles()
    for style_ in styles_:
        head_ += "<link type=\"text/css\" rel=\"stylesheet\" href=\"" + style_ + "\">"
    # end for
    if (not php_empty(lambda : wp_scripts_)):
        wp_scripts_.done = Array()
    # end if
    ob_start()
    php_print(parsed_)
    if "playlist" == PHP_REQUEST["type"]:
        wp_underscore_playlist_templates()
        wp_print_scripts("wp-playlist")
    else:
        wp_print_scripts(Array("mediaelement-vimeo", "wp-mediaelement"))
    # end if
    wp_send_json_success(Array({"head": head_, "body": ob_get_clean()}))
# end def wp_ajax_parse_media_shortcode
#// 
#// Ajax handler for destroying multiple open sessions for a user.
#// 
#// @since 4.1.0
#//
def wp_ajax_destroy_sessions(*_args_):
    
    
    user_ = get_userdata(php_int(PHP_POST["user_id"]))
    if user_:
        if (not current_user_can("edit_user", user_.ID)):
            user_ = False
        elif (not wp_verify_nonce(PHP_POST["nonce"], "update-user_" + user_.ID)):
            user_ = False
        # end if
    # end if
    if (not user_):
        wp_send_json_error(Array({"message": __("Could not log out user sessions. Please try again.")}))
    # end if
    sessions_ = WP_Session_Tokens.get_instance(user_.ID)
    if get_current_user_id() == user_.ID:
        sessions_.destroy_others(wp_get_session_token())
        message_ = __("You are now logged out everywhere else.")
    else:
        sessions_.destroy_all()
        #// translators: %s: User's display name.
        message_ = php_sprintf(__("%s has been logged out."), user_.display_name)
    # end if
    wp_send_json_success(Array({"message": message_}))
# end def wp_ajax_destroy_sessions
#// 
#// Ajax handler for cropping an image.
#// 
#// @since 4.3.0
#//
def wp_ajax_crop_image(*_args_):
    
    
    attachment_id_ = absint(PHP_POST["id"])
    check_ajax_referer("image_editor-" + attachment_id_, "nonce")
    if php_empty(lambda : attachment_id_) or (not current_user_can("edit_post", attachment_id_)):
        wp_send_json_error()
    # end if
    context_ = php_str_replace("_", "-", PHP_POST["context"])
    data_ = php_array_map("absint", PHP_POST["cropDetails"])
    cropped_ = wp_crop_image(attachment_id_, data_["x1"], data_["y1"], data_["width"], data_["height"], data_["dst_width"], data_["dst_height"])
    if (not cropped_) or is_wp_error(cropped_):
        wp_send_json_error(Array({"message": __("Image could not be processed.")}))
    # end if
    for case in Switch(context_):
        if case("site-icon"):
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-icon.php", once=True)
            wp_site_icon_ = php_new_class("WP_Site_Icon", lambda : WP_Site_Icon())
            #// Skip creating a new attachment if the attachment is a Site Icon.
            if get_post_meta(attachment_id_, "_wp_attachment_context", True) == context_:
                #// Delete the temporary cropped file, we don't need it.
                wp_delete_file(cropped_)
                #// Additional sizes in wp_prepare_attachment_for_js().
                add_filter("image_size_names_choose", Array(wp_site_icon_, "additional_sizes"))
                break
            # end if
            #// This filter is documented in wp-admin/includes/class-custom-image-header.php
            cropped_ = apply_filters("wp_create_file_in_uploads", cropped_, attachment_id_)
            #// For replication.
            object_ = wp_site_icon_.create_attachment_object(cropped_, attachment_id_)
            object_["ID"] = None
            #// Update the attachment.
            add_filter("intermediate_image_sizes_advanced", Array(wp_site_icon_, "additional_sizes"))
            attachment_id_ = wp_site_icon_.insert_attachment(object_, cropped_)
            remove_filter("intermediate_image_sizes_advanced", Array(wp_site_icon_, "additional_sizes"))
            #// Additional sizes in wp_prepare_attachment_for_js().
            add_filter("image_size_names_choose", Array(wp_site_icon_, "additional_sizes"))
            break
        # end if
        if case():
            #// 
            #// Fires before a cropped image is saved.
            #// 
            #// Allows to add filters to modify the way a cropped image is saved.
            #// 
            #// @since 4.3.0
            #// 
            #// @param string $context       The Customizer control requesting the cropped image.
            #// @param int    $attachment_id The attachment ID of the original image.
            #// @param string $cropped       Path to the cropped image file.
            #//
            do_action("wp_ajax_crop_image_pre_save", context_, attachment_id_, cropped_)
            #// This filter is documented in wp-admin/includes/class-custom-image-header.php
            cropped_ = apply_filters("wp_create_file_in_uploads", cropped_, attachment_id_)
            #// For replication.
            parent_url_ = wp_get_attachment_url(attachment_id_)
            url_ = php_str_replace(wp_basename(parent_url_), wp_basename(cropped_), parent_url_)
            size_ = php_no_error(lambda: getimagesize(cropped_))
            image_type_ = size_["mime"] if size_ else "image/jpeg"
            object_ = Array({"post_title": wp_basename(cropped_), "post_content": url_, "post_mime_type": image_type_, "guid": url_, "context": context_})
            attachment_id_ = wp_insert_attachment(object_, cropped_)
            metadata_ = wp_generate_attachment_metadata(attachment_id_, cropped_)
            #// 
            #// Filters the cropped image attachment metadata.
            #// 
            #// @since 4.3.0
            #// 
            #// @see wp_generate_attachment_metadata()
            #// 
            #// @param array $metadata Attachment metadata.
            #//
            metadata_ = apply_filters("wp_ajax_cropped_attachment_metadata", metadata_)
            wp_update_attachment_metadata(attachment_id_, metadata_)
            #// 
            #// Filters the attachment ID for a cropped image.
            #// 
            #// @since 4.3.0
            #// 
            #// @param int    $attachment_id The attachment ID of the cropped image.
            #// @param string $context       The Customizer control requesting the cropped image.
            #//
            attachment_id_ = apply_filters("wp_ajax_cropped_attachment_id", attachment_id_, context_)
        # end if
    # end for
    wp_send_json_success(wp_prepare_attachment_for_js(attachment_id_))
# end def wp_ajax_crop_image
#// 
#// Ajax handler for generating a password.
#// 
#// @since 4.4.0
#//
def wp_ajax_generate_password(*_args_):
    
    
    wp_send_json_success(wp_generate_password(24))
# end def wp_ajax_generate_password
#// 
#// Ajax handler for saving the user's WordPress.org username.
#// 
#// @since 4.4.0
#//
def wp_ajax_save_wporg_username(*_args_):
    
    
    if (not current_user_can("install_themes")) and (not current_user_can("install_plugins")):
        wp_send_json_error()
    # end if
    check_ajax_referer("save_wporg_username_" + get_current_user_id())
    username_ = wp_unslash(PHP_REQUEST["username"]) if (php_isset(lambda : PHP_REQUEST["username"])) else False
    if (not username_):
        wp_send_json_error()
    # end if
    wp_send_json_success(update_user_meta(get_current_user_id(), "wporg_favorites", username_))
# end def wp_ajax_save_wporg_username
#// 
#// Ajax handler for installing a theme.
#// 
#// @since 4.6.0
#// 
#// @see Theme_Upgrader
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#//
def wp_ajax_install_theme(*_args_):
    
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_theme_specified", "errorMessage": __("No theme specified.")}))
    # end if
    slug_ = sanitize_key(wp_unslash(PHP_POST["slug"]))
    status_ = Array({"install": "theme", "slug": slug_})
    if (not current_user_can("install_themes")):
        status_["errorMessage"] = __("Sorry, you are not allowed to install themes on this site.")
        wp_send_json_error(status_)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    php_include_file(ABSPATH + "wp-admin/includes/theme.php", once=False)
    api_ = themes_api("theme_information", Array({"slug": slug_, "fields": Array({"sections": False})}))
    if is_wp_error(api_):
        status_["errorMessage"] = api_.get_error_message()
        wp_send_json_error(status_)
    # end if
    skin_ = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader_ = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(skin_))
    result_ = upgrader_.install(api_.download_link)
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status_["debug"] = skin_.get_upgrade_messages()
    # end if
    if is_wp_error(result_):
        status_["errorCode"] = result_.get_error_code()
        status_["errorMessage"] = result_.get_error_message()
        wp_send_json_error(status_)
    elif is_wp_error(skin_.result):
        status_["errorCode"] = skin_.result.get_error_code()
        status_["errorMessage"] = skin_.result.get_error_message()
        wp_send_json_error(status_)
    elif skin_.get_errors().has_errors():
        status_["errorMessage"] = skin_.get_error_messages()
        wp_send_json_error(status_)
    elif is_null(result_):
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        status_["errorCode"] = "unable_to_connect_to_filesystem"
        status_["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem_).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
            status_["errorMessage"] = esc_html(wp_filesystem_.errors.get_error_message())
        # end if
        wp_send_json_error(status_)
    # end if
    status_["themeName"] = wp_get_theme(slug_).get("Name")
    if current_user_can("switch_themes"):
        if is_multisite():
            status_["activateUrl"] = add_query_arg(Array({"action": "enable", "_wpnonce": wp_create_nonce("enable-theme_" + slug_), "theme": slug_}), network_admin_url("themes.php"))
        else:
            status_["activateUrl"] = add_query_arg(Array({"action": "activate", "_wpnonce": wp_create_nonce("switch-theme_" + slug_), "stylesheet": slug_}), admin_url("themes.php"))
        # end if
    # end if
    if (not is_multisite()) and current_user_can("edit_theme_options") and current_user_can("customize"):
        status_["customizeUrl"] = add_query_arg(Array({"return": urlencode(network_admin_url("theme-install.php", "relative"))}), wp_customize_url(slug_))
    # end if
    #// 
    #// See WP_Theme_Install_List_Table::_get_theme_status() if we wanted to check
    #// on post-installation status.
    #//
    wp_send_json_success(status_)
# end def wp_ajax_install_theme
#// 
#// Ajax handler for updating a theme.
#// 
#// @since 4.6.0
#// 
#// @see Theme_Upgrader
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#//
def wp_ajax_update_theme(*_args_):
    
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_theme_specified", "errorMessage": __("No theme specified.")}))
    # end if
    stylesheet_ = php_preg_replace("/[^A-z0-9_\\-]/", "", wp_unslash(PHP_POST["slug"]))
    status_ = Array({"update": "theme", "slug": stylesheet_, "oldVersion": "", "newVersion": ""})
    if (not current_user_can("update_themes")):
        status_["errorMessage"] = __("Sorry, you are not allowed to update themes for this site.")
        wp_send_json_error(status_)
    # end if
    theme_ = wp_get_theme(stylesheet_)
    if theme_.exists():
        status_["oldVersion"] = theme_.get("Version")
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    current_ = get_site_transient("update_themes")
    if php_empty(lambda : current_):
        wp_update_themes()
    # end if
    skin_ = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader_ = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(skin_))
    result_ = upgrader_.bulk_upgrade(Array(stylesheet_))
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status_["debug"] = skin_.get_upgrade_messages()
    # end if
    if is_wp_error(skin_.result):
        status_["errorCode"] = skin_.result.get_error_code()
        status_["errorMessage"] = skin_.result.get_error_message()
        wp_send_json_error(status_)
    elif skin_.get_errors().has_errors():
        status_["errorMessage"] = skin_.get_error_messages()
        wp_send_json_error(status_)
    elif php_is_array(result_) and (not php_empty(lambda : result_[stylesheet_])):
        #// Theme is already at the latest version.
        if True == result_[stylesheet_]:
            status_["errorMessage"] = upgrader_.strings["up_to_date"]
            wp_send_json_error(status_)
        # end if
        theme_ = wp_get_theme(stylesheet_)
        if theme_.exists():
            status_["newVersion"] = theme_.get("Version")
        # end if
        wp_send_json_success(status_)
    elif False == result_:
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        status_["errorCode"] = "unable_to_connect_to_filesystem"
        status_["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem_).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
            status_["errorMessage"] = esc_html(wp_filesystem_.errors.get_error_message())
        # end if
        wp_send_json_error(status_)
    # end if
    #// An unhandled error occurred.
    status_["errorMessage"] = __("Update failed.")
    wp_send_json_error(status_)
# end def wp_ajax_update_theme
#// 
#// Ajax handler for deleting a theme.
#// 
#// @since 4.6.0
#// 
#// @see delete_theme()
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#//
def wp_ajax_delete_theme(*_args_):
    
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_theme_specified", "errorMessage": __("No theme specified.")}))
    # end if
    stylesheet_ = php_preg_replace("/[^A-z0-9_\\-]/", "", wp_unslash(PHP_POST["slug"]))
    status_ = Array({"delete": "theme", "slug": stylesheet_})
    if (not current_user_can("delete_themes")):
        status_["errorMessage"] = __("Sorry, you are not allowed to delete themes on this site.")
        wp_send_json_error(status_)
    # end if
    if (not wp_get_theme(stylesheet_).exists()):
        status_["errorMessage"] = __("The requested theme does not exist.")
        wp_send_json_error(status_)
    # end if
    #// Check filesystem credentials. `delete_theme()` will bail otherwise.
    url_ = wp_nonce_url("themes.php?action=delete&stylesheet=" + urlencode(stylesheet_), "delete-theme_" + stylesheet_)
    ob_start()
    credentials_ = request_filesystem_credentials(url_)
    ob_end_clean()
    if False == credentials_ or (not WP_Filesystem(credentials_)):
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        status_["errorCode"] = "unable_to_connect_to_filesystem"
        status_["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem_).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
            status_["errorMessage"] = esc_html(wp_filesystem_.errors.get_error_message())
        # end if
        wp_send_json_error(status_)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/theme.php", once=False)
    result_ = delete_theme(stylesheet_)
    if is_wp_error(result_):
        status_["errorMessage"] = result_.get_error_message()
        wp_send_json_error(status_)
    elif False == result_:
        status_["errorMessage"] = __("Theme could not be deleted.")
        wp_send_json_error(status_)
    # end if
    wp_send_json_success(status_)
# end def wp_ajax_delete_theme
#// 
#// Ajax handler for installing a plugin.
#// 
#// @since 4.6.0
#// 
#// @see Plugin_Upgrader
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#//
def wp_ajax_install_plugin(*_args_):
    
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_plugin_specified", "errorMessage": __("No plugin specified.")}))
    # end if
    status_ = Array({"install": "plugin", "slug": sanitize_key(wp_unslash(PHP_POST["slug"]))})
    if (not current_user_can("install_plugins")):
        status_["errorMessage"] = __("Sorry, you are not allowed to install plugins on this site.")
        wp_send_json_error(status_)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    php_include_file(ABSPATH + "wp-admin/includes/plugin-install.php", once=False)
    api_ = plugins_api("plugin_information", Array({"slug": sanitize_key(wp_unslash(PHP_POST["slug"])), "fields": Array({"sections": False})}))
    if is_wp_error(api_):
        status_["errorMessage"] = api_.get_error_message()
        wp_send_json_error(status_)
    # end if
    status_["pluginName"] = api_.name
    skin_ = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader_ = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(skin_))
    result_ = upgrader_.install(api_.download_link)
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status_["debug"] = skin_.get_upgrade_messages()
    # end if
    if is_wp_error(result_):
        status_["errorCode"] = result_.get_error_code()
        status_["errorMessage"] = result_.get_error_message()
        wp_send_json_error(status_)
    elif is_wp_error(skin_.result):
        status_["errorCode"] = skin_.result.get_error_code()
        status_["errorMessage"] = skin_.result.get_error_message()
        wp_send_json_error(status_)
    elif skin_.get_errors().has_errors():
        status_["errorMessage"] = skin_.get_error_messages()
        wp_send_json_error(status_)
    elif is_null(result_):
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        status_["errorCode"] = "unable_to_connect_to_filesystem"
        status_["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem_).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
            status_["errorMessage"] = esc_html(wp_filesystem_.errors.get_error_message())
        # end if
        wp_send_json_error(status_)
    # end if
    install_status_ = install_plugin_install_status(api_)
    pagenow_ = sanitize_key(PHP_POST["pagenow"]) if (php_isset(lambda : PHP_POST["pagenow"])) else ""
    #// If installation request is coming from import page, do not return network activation link.
    plugins_url_ = admin_url("plugins.php") if "import" == pagenow_ else network_admin_url("plugins.php")
    if current_user_can("activate_plugin", install_status_["file"]) and is_plugin_inactive(install_status_["file"]):
        status_["activateUrl"] = add_query_arg(Array({"_wpnonce": wp_create_nonce("activate-plugin_" + install_status_["file"]), "action": "activate", "plugin": install_status_["file"]}), plugins_url_)
    # end if
    if is_multisite() and current_user_can("manage_network_plugins") and "import" != pagenow_:
        status_["activateUrl"] = add_query_arg(Array({"networkwide": 1}), status_["activateUrl"])
    # end if
    wp_send_json_success(status_)
# end def wp_ajax_install_plugin
#// 
#// Ajax handler for updating a plugin.
#// 
#// @since 4.2.0
#// 
#// @see Plugin_Upgrader
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#//
def wp_ajax_update_plugin(*_args_):
    
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["plugin"]) or php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_plugin_specified", "errorMessage": __("No plugin specified.")}))
    # end if
    plugin_ = plugin_basename(sanitize_text_field(wp_unslash(PHP_POST["plugin"])))
    status_ = Array({"update": "plugin", "slug": sanitize_key(wp_unslash(PHP_POST["slug"])), "oldVersion": "", "newVersion": ""})
    if (not current_user_can("update_plugins")) or 0 != validate_file(plugin_):
        status_["errorMessage"] = __("Sorry, you are not allowed to update plugins for this site.")
        wp_send_json_error(status_)
    # end if
    plugin_data_ = get_plugin_data(WP_PLUGIN_DIR + "/" + plugin_)
    status_["plugin"] = plugin_
    status_["pluginName"] = plugin_data_["Name"]
    if plugin_data_["Version"]:
        #// translators: %s: Plugin version.
        status_["oldVersion"] = php_sprintf(__("Version %s"), plugin_data_["Version"])
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    wp_update_plugins()
    skin_ = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader_ = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(skin_))
    result_ = upgrader_.bulk_upgrade(Array(plugin_))
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status_["debug"] = skin_.get_upgrade_messages()
    # end if
    if is_wp_error(skin_.result):
        status_["errorCode"] = skin_.result.get_error_code()
        status_["errorMessage"] = skin_.result.get_error_message()
        wp_send_json_error(status_)
    elif skin_.get_errors().has_errors():
        status_["errorMessage"] = skin_.get_error_messages()
        wp_send_json_error(status_)
    elif php_is_array(result_) and (not php_empty(lambda : result_[plugin_])):
        plugin_update_data_ = current(result_)
        #// 
        #// If the `update_plugins` site transient is empty (e.g. when you update
        #// two plugins in quick succession before the transient repopulates),
        #// this may be the return.
        #// 
        #// Preferably something can be done to ensure `update_plugins` isn't empty.
        #// For now, surface some sort of error here.
        #//
        if True == plugin_update_data_:
            status_["errorMessage"] = __("Plugin update failed.")
            wp_send_json_error(status_)
        # end if
        plugin_data_ = get_plugins("/" + result_[plugin_]["destination_name"])
        plugin_data_ = reset(plugin_data_)
        if plugin_data_["Version"]:
            #// translators: %s: Plugin version.
            status_["newVersion"] = php_sprintf(__("Version %s"), plugin_data_["Version"])
        # end if
        wp_send_json_success(status_)
    elif False == result_:
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        status_["errorCode"] = "unable_to_connect_to_filesystem"
        status_["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem_).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
            status_["errorMessage"] = esc_html(wp_filesystem_.errors.get_error_message())
        # end if
        wp_send_json_error(status_)
    # end if
    #// An unhandled error occurred.
    status_["errorMessage"] = __("Plugin update failed.")
    wp_send_json_error(status_)
# end def wp_ajax_update_plugin
#// 
#// Ajax handler for deleting a plugin.
#// 
#// @since 4.6.0
#// 
#// @see delete_plugins()
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#//
def wp_ajax_delete_plugin(*_args_):
    
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]) or php_empty(lambda : PHP_POST["plugin"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_plugin_specified", "errorMessage": __("No plugin specified.")}))
    # end if
    plugin_ = plugin_basename(sanitize_text_field(wp_unslash(PHP_POST["plugin"])))
    status_ = Array({"delete": "plugin", "slug": sanitize_key(wp_unslash(PHP_POST["slug"]))})
    if (not current_user_can("delete_plugins")) or 0 != validate_file(plugin_):
        status_["errorMessage"] = __("Sorry, you are not allowed to delete plugins for this site.")
        wp_send_json_error(status_)
    # end if
    plugin_data_ = get_plugin_data(WP_PLUGIN_DIR + "/" + plugin_)
    status_["plugin"] = plugin_
    status_["pluginName"] = plugin_data_["Name"]
    if is_plugin_active(plugin_):
        status_["errorMessage"] = __("You cannot delete a plugin while it is active on the main site.")
        wp_send_json_error(status_)
    # end if
    #// Check filesystem credentials. `delete_plugins()` will bail otherwise.
    url_ = wp_nonce_url("plugins.php?action=delete-selected&verify-delete=1&checked[]=" + plugin_, "bulk-plugins")
    ob_start()
    credentials_ = request_filesystem_credentials(url_)
    ob_end_clean()
    if False == credentials_ or (not WP_Filesystem(credentials_)):
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        status_["errorCode"] = "unable_to_connect_to_filesystem"
        status_["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem_).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
            status_["errorMessage"] = esc_html(wp_filesystem_.errors.get_error_message())
        # end if
        wp_send_json_error(status_)
    # end if
    result_ = delete_plugins(Array(plugin_))
    if is_wp_error(result_):
        status_["errorMessage"] = result_.get_error_message()
        wp_send_json_error(status_)
    elif False == result_:
        status_["errorMessage"] = __("Plugin could not be deleted.")
        wp_send_json_error(status_)
    # end if
    wp_send_json_success(status_)
# end def wp_ajax_delete_plugin
#// 
#// Ajax handler for searching plugins.
#// 
#// @since 4.6.0
#// 
#// @global string $s Search term.
#//
def wp_ajax_search_plugins(*_args_):
    
    global PHP_SERVER, PHP_GLOBALS
    check_ajax_referer("updates")
    pagenow_ = sanitize_key(PHP_POST["pagenow"]) if (php_isset(lambda : PHP_POST["pagenow"])) else ""
    if "plugins-network" == pagenow_ or "plugins" == pagenow_:
        set_current_screen(pagenow_)
    # end if
    #// @var WP_Plugins_List_Table $wp_list_table
    wp_list_table_ = _get_list_table("WP_Plugins_List_Table", Array({"screen": get_current_screen()}))
    status_ = Array()
    if (not wp_list_table_.ajax_user_can()):
        status_["errorMessage"] = __("Sorry, you are not allowed to manage plugins for this site.")
        wp_send_json_error(status_)
    # end if
    #// Set the correct requester, so pagination works.
    PHP_SERVER["REQUEST_URI"] = add_query_arg(php_array_diff_key(PHP_POST, Array({"_ajax_nonce": None, "action": None})), network_admin_url("plugins.php", "relative"))
    PHP_GLOBALS["s"] = wp_unslash(PHP_POST["s"])
    wp_list_table_.prepare_items()
    ob_start()
    wp_list_table_.display()
    status_["count"] = php_count(wp_list_table_.items)
    status_["items"] = ob_get_clean()
    wp_send_json_success(status_)
# end def wp_ajax_search_plugins
#// 
#// Ajax handler for searching plugins to install.
#// 
#// @since 4.6.0
#//
def wp_ajax_search_install_plugins(*_args_):
    
    global PHP_SERVER
    check_ajax_referer("updates")
    pagenow_ = sanitize_key(PHP_POST["pagenow"]) if (php_isset(lambda : PHP_POST["pagenow"])) else ""
    if "plugin-install-network" == pagenow_ or "plugin-install" == pagenow_:
        set_current_screen(pagenow_)
    # end if
    #// @var WP_Plugin_Install_List_Table $wp_list_table
    wp_list_table_ = _get_list_table("WP_Plugin_Install_List_Table", Array({"screen": get_current_screen()}))
    status_ = Array()
    if (not wp_list_table_.ajax_user_can()):
        status_["errorMessage"] = __("Sorry, you are not allowed to manage plugins for this site.")
        wp_send_json_error(status_)
    # end if
    #// Set the correct requester, so pagination works.
    PHP_SERVER["REQUEST_URI"] = add_query_arg(php_array_diff_key(PHP_POST, Array({"_ajax_nonce": None, "action": None})), network_admin_url("plugin-install.php", "relative"))
    wp_list_table_.prepare_items()
    ob_start()
    wp_list_table_.display()
    status_["count"] = php_int(wp_list_table_.get_pagination_arg("total_items"))
    status_["items"] = ob_get_clean()
    wp_send_json_success(status_)
# end def wp_ajax_search_install_plugins
#// 
#// Ajax handler for editing a theme or plugin file.
#// 
#// @since 4.9.0
#// @see wp_edit_theme_plugin_file()
#//
def wp_ajax_edit_theme_plugin_file(*_args_):
    
    
    r_ = wp_edit_theme_plugin_file(wp_unslash(PHP_POST))
    #// Validation of args is done in wp_edit_theme_plugin_file().
    if is_wp_error(r_):
        wp_send_json_error(php_array_merge(Array({"code": r_.get_error_code(), "message": r_.get_error_message()}), r_.get_error_data()))
    else:
        wp_send_json_success(Array({"message": __("File edited successfully.")}))
    # end if
# end def wp_ajax_edit_theme_plugin_file
#// 
#// Ajax handler for exporting a user's personal data.
#// 
#// @since 4.9.6
#//
def wp_ajax_wp_privacy_export_personal_data(*_args_):
    
    
    if php_empty(lambda : PHP_POST["id"]):
        wp_send_json_error(__("Missing request ID."))
    # end if
    request_id_ = php_int(PHP_POST["id"])
    if request_id_ < 1:
        wp_send_json_error(__("Invalid request ID."))
    # end if
    if (not current_user_can("export_others_personal_data")):
        wp_send_json_error(__("Sorry, you are not allowed to perform this action."))
    # end if
    check_ajax_referer("wp-privacy-export-personal-data-" + request_id_, "security")
    #// Get the request.
    request_ = wp_get_user_request(request_id_)
    if (not request_) or "export_personal_data" != request_.action_name:
        wp_send_json_error(__("Invalid request type."))
    # end if
    email_address_ = request_.email
    if (not is_email(email_address_)):
        wp_send_json_error(__("A valid email address must be given."))
    # end if
    if (not (php_isset(lambda : PHP_POST["exporter"]))):
        wp_send_json_error(__("Missing exporter index."))
    # end if
    exporter_index_ = php_int(PHP_POST["exporter"])
    if (not (php_isset(lambda : PHP_POST["page"]))):
        wp_send_json_error(__("Missing page index."))
    # end if
    page_ = php_int(PHP_POST["page"])
    send_as_email_ = "true" == PHP_POST["sendAsEmail"] if (php_isset(lambda : PHP_POST["sendAsEmail"])) else False
    #// 
    #// Filters the array of exporter callbacks.
    #// 
    #// @since 4.9.6
    #// 
    #// @param array $args {
    #// An array of callable exporters of personal data. Default empty array.
    #// 
    #// @type array {
    #// Array of personal data exporters.
    #// 
    #// @type string $callback               Callable exporter function that accepts an
    #// email address and a page and returns an array
    #// of name => value pairs of personal data.
    #// @type string $exporter_friendly_name Translated user facing friendly name for the
    #// exporter.
    #// }
    #// }
    #//
    exporters_ = apply_filters("wp_privacy_personal_data_exporters", Array())
    if (not php_is_array(exporters_)):
        wp_send_json_error(__("An exporter has improperly used the registration filter."))
    # end if
    #// Do we have any registered exporters?
    if 0 < php_count(exporters_):
        if exporter_index_ < 1:
            wp_send_json_error(__("Exporter index cannot be negative."))
        # end if
        if exporter_index_ > php_count(exporters_):
            wp_send_json_error(__("Exporter index is out of range."))
        # end if
        if page_ < 1:
            wp_send_json_error(__("Page index cannot be less than one."))
        # end if
        exporter_keys_ = php_array_keys(exporters_)
        exporter_key_ = exporter_keys_[exporter_index_ - 1]
        exporter_ = exporters_[exporter_key_]
        if (not php_is_array(exporter_)):
            wp_send_json_error(php_sprintf(__("Expected an array describing the exporter at index %s."), exporter_key_))
        # end if
        if (not php_array_key_exists("exporter_friendly_name", exporter_)):
            wp_send_json_error(php_sprintf(__("Exporter array at index %s does not include a friendly name."), exporter_key_))
        # end if
        exporter_friendly_name_ = exporter_["exporter_friendly_name"]
        if (not php_array_key_exists("callback", exporter_)):
            wp_send_json_error(php_sprintf(__("Exporter does not include a callback: %s."), esc_html(exporter_friendly_name_)))
        # end if
        if (not php_is_callable(exporter_["callback"])):
            wp_send_json_error(php_sprintf(__("Exporter callback is not a valid callback: %s."), esc_html(exporter_friendly_name_)))
        # end if
        callback_ = exporter_["callback"]
        response_ = php_call_user_func(callback_, email_address_, page_)
        if is_wp_error(response_):
            wp_send_json_error(response_)
        # end if
        if (not php_is_array(response_)):
            wp_send_json_error(php_sprintf(__("Expected response as an array from exporter: %s."), esc_html(exporter_friendly_name_)))
        # end if
        if (not php_array_key_exists("data", response_)):
            wp_send_json_error(php_sprintf(__("Expected data in response array from exporter: %s."), esc_html(exporter_friendly_name_)))
        # end if
        if (not php_is_array(response_["data"])):
            wp_send_json_error(php_sprintf(__("Expected data array in response array from exporter: %s."), esc_html(exporter_friendly_name_)))
        # end if
        if (not php_array_key_exists("done", response_)):
            wp_send_json_error(php_sprintf(__("Expected done (boolean) in response array from exporter: %s."), esc_html(exporter_friendly_name_)))
        # end if
    else:
        #// No exporters, so we're done.
        exporter_key_ = ""
        response_ = Array({"data": Array(), "done": True})
    # end if
    #// 
    #// Filters a page of personal data exporter data. Used to build the export report.
    #// 
    #// Allows the export response to be consumed by destinations in addition to Ajax.
    #// 
    #// @since 4.9.6
    #// 
    #// @param array  $response        The personal data for the given exporter and page.
    #// @param int    $exporter_index  The index of the exporter that provided this data.
    #// @param string $email_address   The email address associated with this personal data.
    #// @param int    $page            The page for this response.
    #// @param int    $request_id      The privacy request post ID associated with this request.
    #// @param bool   $send_as_email   Whether the final results of the export should be emailed to the user.
    #// @param string $exporter_key    The key (slug) of the exporter that provided this data.
    #//
    response_ = apply_filters("wp_privacy_personal_data_export_page", response_, exporter_index_, email_address_, page_, request_id_, send_as_email_, exporter_key_)
    if is_wp_error(response_):
        wp_send_json_error(response_)
    # end if
    wp_send_json_success(response_)
# end def wp_ajax_wp_privacy_export_personal_data
#// 
#// Ajax handler for erasing personal data.
#// 
#// @since 4.9.6
#//
def wp_ajax_wp_privacy_erase_personal_data(*_args_):
    
    
    if php_empty(lambda : PHP_POST["id"]):
        wp_send_json_error(__("Missing request ID."))
    # end if
    request_id_ = php_int(PHP_POST["id"])
    if request_id_ < 1:
        wp_send_json_error(__("Invalid request ID."))
    # end if
    #// Both capabilities are required to avoid confusion, see `_wp_personal_data_removal_page()`.
    if (not current_user_can("erase_others_personal_data")) or (not current_user_can("delete_users")):
        wp_send_json_error(__("Sorry, you are not allowed to perform this action."))
    # end if
    check_ajax_referer("wp-privacy-erase-personal-data-" + request_id_, "security")
    #// Get the request.
    request_ = wp_get_user_request(request_id_)
    if (not request_) or "remove_personal_data" != request_.action_name:
        wp_send_json_error(__("Invalid request type."))
    # end if
    email_address_ = request_.email
    if (not is_email(email_address_)):
        wp_send_json_error(__("Invalid email address in request."))
    # end if
    if (not (php_isset(lambda : PHP_POST["eraser"]))):
        wp_send_json_error(__("Missing eraser index."))
    # end if
    eraser_index_ = php_int(PHP_POST["eraser"])
    if (not (php_isset(lambda : PHP_POST["page"]))):
        wp_send_json_error(__("Missing page index."))
    # end if
    page_ = php_int(PHP_POST["page"])
    #// 
    #// Filters the array of personal data eraser callbacks.
    #// 
    #// @since 4.9.6
    #// 
    #// @param array $args {
    #// An array of callable erasers of personal data. Default empty array.
    #// 
    #// @type array {
    #// Array of personal data exporters.
    #// 
    #// @type string $callback               Callable eraser that accepts an email address and
    #// a page and returns an array with boolean values for
    #// whether items were removed or retained and any messages
    #// from the eraser, as well as if additional pages are
    #// available.
    #// @type string $exporter_friendly_name Translated user facing friendly name for the eraser.
    #// }
    #// }
    #//
    erasers_ = apply_filters("wp_privacy_personal_data_erasers", Array())
    #// Do we have any registered erasers?
    if 0 < php_count(erasers_):
        if eraser_index_ < 1:
            wp_send_json_error(__("Eraser index cannot be less than one."))
        # end if
        if eraser_index_ > php_count(erasers_):
            wp_send_json_error(__("Eraser index is out of range."))
        # end if
        if page_ < 1:
            wp_send_json_error(__("Page index cannot be less than one."))
        # end if
        eraser_keys_ = php_array_keys(erasers_)
        eraser_key_ = eraser_keys_[eraser_index_ - 1]
        eraser_ = erasers_[eraser_key_]
        if (not php_is_array(eraser_)):
            #// translators: %d: Eraser array index.
            wp_send_json_error(php_sprintf(__("Expected an array describing the eraser at index %d."), eraser_index_))
        # end if
        if (not php_array_key_exists("eraser_friendly_name", eraser_)):
            #// translators: %d: Eraser array index.
            wp_send_json_error(php_sprintf(__("Eraser array at index %d does not include a friendly name."), eraser_index_))
        # end if
        eraser_friendly_name_ = eraser_["eraser_friendly_name"]
        if (not php_array_key_exists("callback", eraser_)):
            wp_send_json_error(php_sprintf(__("Eraser does not include a callback: %s."), esc_html(eraser_friendly_name_)))
        # end if
        if (not php_is_callable(eraser_["callback"])):
            wp_send_json_error(php_sprintf(__("Eraser callback is not valid: %s."), esc_html(eraser_friendly_name_)))
        # end if
        callback_ = eraser_["callback"]
        response_ = php_call_user_func(callback_, email_address_, page_)
        if is_wp_error(response_):
            wp_send_json_error(response_)
        # end if
        if (not php_is_array(response_)):
            wp_send_json_error(php_sprintf(__("Did not receive array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name_), eraser_index_))
        # end if
        if (not php_array_key_exists("items_removed", response_)):
            wp_send_json_error(php_sprintf(__("Expected items_removed key in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name_), eraser_index_))
        # end if
        if (not php_array_key_exists("items_retained", response_)):
            wp_send_json_error(php_sprintf(__("Expected items_retained key in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name_), eraser_index_))
        # end if
        if (not php_array_key_exists("messages", response_)):
            wp_send_json_error(php_sprintf(__("Expected messages key in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name_), eraser_index_))
        # end if
        if (not php_is_array(response_["messages"])):
            wp_send_json_error(php_sprintf(__("Expected messages key to reference an array in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name_), eraser_index_))
        # end if
        if (not php_array_key_exists("done", response_)):
            wp_send_json_error(php_sprintf(__("Expected done flag in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name_), eraser_index_))
        # end if
    else:
        #// No erasers, so we're done.
        eraser_key_ = ""
        response_ = Array({"items_removed": False, "items_retained": False, "messages": Array(), "done": True})
    # end if
    #// 
    #// Filters a page of personal data eraser data.
    #// 
    #// Allows the erasure response to be consumed by destinations in addition to Ajax.
    #// 
    #// @since 4.9.6
    #// 
    #// @param array  $response        The personal data for the given exporter and page.
    #// @param int    $eraser_index    The index of the eraser that provided this data.
    #// @param string $email_address   The email address associated with this personal data.
    #// @param int    $page            The page for this response.
    #// @param int    $request_id      The privacy request post ID associated with this request.
    #// @param string $eraser_key      The key (slug) of the eraser that provided this data.
    #//
    response_ = apply_filters("wp_privacy_personal_data_erasure_page", response_, eraser_index_, email_address_, page_, request_id_, eraser_key_)
    if is_wp_error(response_):
        wp_send_json_error(response_)
    # end if
    wp_send_json_success(response_)
# end def wp_ajax_wp_privacy_erase_personal_data
#// 
#// Ajax handler for site health checks on server communication.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_dotorg_communication(*_args_):
    
    
    check_ajax_referer("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health_ = WP_Site_Health.get_instance()
    wp_send_json_success(site_health_.get_test_dotorg_communication())
# end def wp_ajax_health_check_dotorg_communication
#// 
#// Ajax handler for site health checks on debug mode.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_is_in_debug_mode(*_args_):
    
    
    wp_verify_nonce("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health_ = WP_Site_Health.get_instance()
    wp_send_json_success(site_health_.get_test_is_in_debug_mode())
# end def wp_ajax_health_check_is_in_debug_mode
#// 
#// Ajax handler for site health checks on background updates.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_background_updates(*_args_):
    
    
    check_ajax_referer("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health_ = WP_Site_Health.get_instance()
    wp_send_json_success(site_health_.get_test_background_updates())
# end def wp_ajax_health_check_background_updates
#// 
#// Ajax handler for site health checks on loopback requests.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_loopback_requests(*_args_):
    
    
    check_ajax_referer("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health_ = WP_Site_Health.get_instance()
    wp_send_json_success(site_health_.get_test_loopback_requests())
# end def wp_ajax_health_check_loopback_requests
#// 
#// Ajax handler for site health check to update the result status.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_site_status_result(*_args_):
    
    
    check_ajax_referer("health-check-site-status-result")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    set_transient("health-check-site-status-result", wp_json_encode(PHP_POST["counts"]))
    wp_send_json_success()
# end def wp_ajax_health_check_site_status_result
#// 
#// Ajax handler for site health check to get directories and database sizes.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_get_sizes(*_args_):
    
    
    check_ajax_referer("health-check-site-status-result")
    if (not current_user_can("view_site_health_checks")) or is_multisite():
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Debug_Data")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-debug-data.php", once=True)
    # end if
    sizes_data_ = WP_Debug_Data.get_sizes()
    all_sizes_ = Array({"raw": 0})
    for name_,value_ in sizes_data_:
        name_ = sanitize_text_field(name_)
        data_ = Array()
        if (php_isset(lambda : value_["size"])):
            if php_is_string(value_["size"]):
                data_["size"] = sanitize_text_field(value_["size"])
            else:
                data_["size"] = php_int(value_["size"])
            # end if
        # end if
        if (php_isset(lambda : value_["debug"])):
            if php_is_string(value_["debug"]):
                data_["debug"] = sanitize_text_field(value_["debug"])
            else:
                data_["debug"] = php_int(value_["debug"])
            # end if
        # end if
        if (not php_empty(lambda : value_["raw"])):
            data_["raw"] = php_int(value_["raw"])
        # end if
        all_sizes_[name_] = data_
    # end for
    if (php_isset(lambda : all_sizes_["total_size"]["debug"])) and "not available" == all_sizes_["total_size"]["debug"]:
        wp_send_json_error(all_sizes_)
    # end if
    wp_send_json_success(all_sizes_)
# end def wp_ajax_health_check_get_sizes
#// 
#// Ajax handler to renew the REST API nonce.
#// 
#// @since 5.3.0
#//
def wp_ajax_rest_nonce(*_args_):
    
    
    php_print(wp_create_nonce("wp_rest"))
    php_exit()
# end def wp_ajax_rest_nonce
