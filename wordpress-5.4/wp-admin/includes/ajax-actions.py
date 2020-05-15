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
def wp_ajax_nopriv_heartbeat(*args_):
    
    response = Array()
    #// 'screen_id' is the same as $current_screen->id and the JS global 'pagenow'.
    if (not php_empty(lambda : PHP_POST["screen_id"])):
        screen_id = sanitize_key(PHP_POST["screen_id"])
    else:
        screen_id = "front"
    # end if
    if (not php_empty(lambda : PHP_POST["data"])):
        data = wp_unslash(PHP_POST["data"])
        #// 
        #// Filters Heartbeat Ajax response in no-privilege environments.
        #// 
        #// @since 3.6.0
        #// 
        #// @param array  $response  The no-priv Heartbeat response.
        #// @param array  $data      The $_POST data sent.
        #// @param string $screen_id The screen id.
        #//
        response = apply_filters("heartbeat_nopriv_received", response, data, screen_id)
    # end if
    #// 
    #// Filters Heartbeat Ajax response in no-privilege environments when no data is passed.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array  $response  The no-priv Heartbeat response.
    #// @param string $screen_id The screen id.
    #//
    response = apply_filters("heartbeat_nopriv_send", response, screen_id)
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
    do_action("heartbeat_nopriv_tick", response, screen_id)
    #// Send the current time according to the server.
    response["server_time"] = time()
    wp_send_json(response)
# end def wp_ajax_nopriv_heartbeat
#// 
#// GET-based Ajax handlers.
#// 
#// 
#// Ajax handler for fetching a list table.
#// 
#// @since 3.1.0
#//
def wp_ajax_fetch_list(*args_):
    
    list_class = PHP_REQUEST["list_args"]["class"]
    check_ajax_referer(str("fetch-list-") + str(list_class), "_ajax_fetch_list_nonce")
    wp_list_table = _get_list_table(list_class, Array({"screen": PHP_REQUEST["list_args"]["screen"]["id"]}))
    if (not wp_list_table):
        wp_die(0)
    # end if
    if (not wp_list_table.ajax_user_can()):
        wp_die(-1)
    # end if
    wp_list_table.ajax_response()
    wp_die(0)
# end def wp_ajax_fetch_list
#// 
#// Ajax handler for tag search.
#// 
#// @since 3.1.0
#//
def wp_ajax_ajax_tag_search(*args_):
    
    if (not (php_isset(lambda : PHP_REQUEST["tax"]))):
        wp_die(0)
    # end if
    taxonomy = sanitize_key(PHP_REQUEST["tax"])
    tax = get_taxonomy(taxonomy)
    if (not tax):
        wp_die(0)
    # end if
    if (not current_user_can(tax.cap.assign_terms)):
        wp_die(-1)
    # end if
    s = wp_unslash(PHP_REQUEST["q"])
    comma = _x(",", "tag delimiter")
    if "," != comma:
        s = php_str_replace(comma, ",", s)
    # end if
    if False != php_strpos(s, ","):
        s = php_explode(",", s)
        s = s[php_count(s) - 1]
    # end if
    s = php_trim(s)
    #// 
    #// Filters the minimum number of characters required to fire a tag search via Ajax.
    #// 
    #// @since 4.0.0
    #// 
    #// @param int         $characters The minimum number of characters required. Default 2.
    #// @param WP_Taxonomy $tax        The taxonomy object.
    #// @param string      $s          The search term.
    #//
    term_search_min_chars = int(apply_filters("term_search_min_chars", 2, tax, s))
    #// 
    #// Require $term_search_min_chars chars for matching (default: 2)
    #// ensure it's a non-negative, non-zero integer.
    #//
    if 0 == term_search_min_chars or php_strlen(s) < term_search_min_chars:
        wp_die()
    # end if
    results = get_terms(Array({"taxonomy": taxonomy, "name__like": s, "fields": "names", "hide_empty": False}))
    php_print(join("\n", results))
    wp_die()
# end def wp_ajax_ajax_tag_search
#// 
#// Ajax handler for compression testing.
#// 
#// @since 3.1.0
#//
def wp_ajax_wp_compression_test(*args_):
    
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
        force_gzip = php_defined("ENFORCE_GZIP") and ENFORCE_GZIP
        test_str = "\"wpCompressionTest Lorem ipsum dolor sit amet consectetuer mollis sapien urna ut a. Eu nonummy condimentum fringilla tempor pretium platea vel nibh netus Maecenas. Hac molestie amet justo quis pellentesque est ultrices interdum nibh Morbi. Cras mattis pretium Phasellus ante ipsum ipsum ut sociis Suspendisse Lorem. Ante et non molestie. Porta urna Vestibulum egestas id congue nibh eu risus gravida sit. Ac augue auctor Ut et non a elit massa id sodales. Elit eu Nulla at nibh adipiscing mattis lacus mauris at tempus. Netus nibh quis suscipit nec feugiat eget sed lorem et urna. Pellentesque lacus at ut massa consectetuer ligula ut auctor semper Pellentesque. Ut metus massa nibh quam Curabitur molestie nec mauris congue. Volutpat molestie elit justo facilisis neque ac risus Ut nascetur tristique. Vitae sit lorem tellus et quis Phasellus lacus tincidunt nunc Fusce. Pharetra wisi Suspendisse mus sagittis libero lacinia Integer consequat ac Phasellus. Et urna ac cursus tortor aliquam Aliquam amet tellus volutpat Vestibulum. Justo interdum condimentum In augue congue tellus sollicitudin Quisque quis nibh.\""
        if 1 == PHP_REQUEST["test"]:
            php_print(test_str)
            wp_die()
        elif 2 == PHP_REQUEST["test"]:
            if (not (php_isset(lambda : PHP_SERVER["HTTP_ACCEPT_ENCODING"]))):
                wp_die(-1)
            # end if
            if False != php_stripos(PHP_SERVER["HTTP_ACCEPT_ENCODING"], "deflate") and php_function_exists("gzdeflate") and (not force_gzip):
                php_header("Content-Encoding: deflate")
                out = gzdeflate(test_str, 1)
            elif False != php_stripos(PHP_SERVER["HTTP_ACCEPT_ENCODING"], "gzip") and php_function_exists("gzencode"):
                php_header("Content-Encoding: gzip")
                out = gzencode(test_str, 1)
            else:
                wp_die(-1)
            # end if
            php_print(out)
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
def wp_ajax_imgedit_preview(*args_):
    
    post_id = php_intval(PHP_REQUEST["postid"])
    if php_empty(lambda : post_id) or (not current_user_can("edit_post", post_id)):
        wp_die(-1)
    # end if
    check_ajax_referer(str("image_editor-") + str(post_id))
    php_include_file(ABSPATH + "wp-admin/includes/image-edit.php", once=False)
    if (not stream_preview_image(post_id)):
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
def wp_ajax_oembed_cache(*args_):
    
    PHP_GLOBALS["wp_embed"].cache_oembed(PHP_REQUEST["post"])
    wp_die(0)
# end def wp_ajax_oembed_cache
#// 
#// Ajax handler for user autocomplete.
#// 
#// @since 3.4.0
#//
def wp_ajax_autocomplete_user(*args_):
    
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
        type = PHP_REQUEST["autocomplete_type"]
    else:
        type = "add"
    # end if
    #// Check the desired field for value.
    #// Current allowed values are `user_email` and `user_login`.
    if (php_isset(lambda : PHP_REQUEST["autocomplete_field"])) and "user_email" == PHP_REQUEST["autocomplete_field"]:
        field = PHP_REQUEST["autocomplete_field"]
    else:
        field = "user_login"
    # end if
    #// Exclude current users of this blog.
    if (php_isset(lambda : PHP_REQUEST["site_id"])):
        id = absint(PHP_REQUEST["site_id"])
    else:
        id = get_current_blog_id()
    # end if
    include_blog_users = get_users(Array({"blog_id": id, "fields": "ID"})) if "search" == type else Array()
    exclude_blog_users = get_users(Array({"blog_id": id, "fields": "ID"})) if "add" == type else Array()
    users = get_users(Array({"blog_id": False, "search": "*" + PHP_REQUEST["term"] + "*", "include": include_blog_users, "exclude": exclude_blog_users, "search_columns": Array("user_login", "user_nicename", "user_email")}))
    for user in users:
        return_[-1] = Array({"label": php_sprintf(_x("%1$s (%2$s)", "user autocomplete result"), user.user_login, user.user_email), "value": user.field})
    # end for
    wp_die(wp_json_encode(return_))
# end def wp_ajax_autocomplete_user
#// 
#// Handles AJAX requests for community events
#// 
#// @since 4.8.0
#//
def wp_ajax_get_community_events(*args_):
    
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-community-events.php", once=True)
    check_ajax_referer("community_events")
    search = wp_unslash(PHP_POST["location"]) if (php_isset(lambda : PHP_POST["location"])) else ""
    timezone = wp_unslash(PHP_POST["timezone"]) if (php_isset(lambda : PHP_POST["timezone"])) else ""
    user_id = get_current_user_id()
    saved_location = get_user_option("community-events-location", user_id)
    events_client = php_new_class("WP_Community_Events", lambda : WP_Community_Events(user_id, saved_location))
    events = events_client.get_events(search, timezone)
    ip_changed = False
    if is_wp_error(events):
        wp_send_json_error(Array({"error": events.get_error_message()}))
    else:
        if php_empty(lambda : saved_location["ip"]) and (not php_empty(lambda : events["location"]["ip"])):
            ip_changed = True
        elif (php_isset(lambda : saved_location["ip"])) and (not php_empty(lambda : events["location"]["ip"])) and saved_location["ip"] != events["location"]["ip"]:
            ip_changed = True
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
        if ip_changed or search:
            update_user_option(user_id, "community-events-location", events["location"], True)
        # end if
        wp_send_json_success(events)
    # end if
# end def wp_ajax_get_community_events
#// 
#// Ajax handler for dashboard widgets.
#// 
#// @since 3.4.0
#//
def wp_ajax_dashboard_widgets(*args_):
    
    php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
    pagenow = PHP_REQUEST["pagenow"]
    if "dashboard-user" == pagenow or "dashboard-network" == pagenow or "dashboard" == pagenow:
        set_current_screen(pagenow)
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
def wp_ajax_logged_in(*args_):
    
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
def _wp_ajax_delete_comment_response(comment_id=None, delta=-1, *args_):
    
    total = int(PHP_POST["_total"]) if (php_isset(lambda : PHP_POST["_total"])) else 0
    per_page = int(PHP_POST["_per_page"]) if (php_isset(lambda : PHP_POST["_per_page"])) else 0
    page = int(PHP_POST["_page"]) if (php_isset(lambda : PHP_POST["_page"])) else 0
    url = esc_url_raw(PHP_POST["_url"]) if (php_isset(lambda : PHP_POST["_url"])) else ""
    #// JS didn't send us everything we need to know. Just die with success message.
    if (not total) or (not per_page) or (not page) or (not url):
        time = time()
        comment = get_comment(comment_id)
        comment_status = ""
        comment_link = ""
        if comment:
            comment_status = comment.comment_approved
        # end if
        if 1 == int(comment_status):
            comment_link = get_comment_link(comment)
        # end if
        counts = wp_count_comments()
        x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": comment_id, "supplemental": Array({"status": comment_status, "postId": comment.comment_post_ID if comment else "", "time": time, "in_moderation": counts.moderated, "i18n_comments_text": php_sprintf(_n("%s Comment", "%s Comments", counts.approved), number_format_i18n(counts.approved)), "i18n_moderation_text": php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", counts.moderated), number_format_i18n(counts.moderated)), "comment_link": comment_link})})))
        x.send()
    # end if
    total += delta
    if total < 0:
        total = 0
    # end if
    #// Only do the expensive stuff on a page-break, and about 1 other time per page.
    if 0 == total % per_page or 1 == mt_rand(1, per_page):
        post_id = 0
        #// What type of comment count are we looking for?
        status = "all"
        parsed = php_parse_url(url)
        if (php_isset(lambda : parsed["query"])):
            parse_str(parsed["query"], query_vars)
            if (not php_empty(lambda : query_vars["comment_status"])):
                status = query_vars["comment_status"]
            # end if
            if (not php_empty(lambda : query_vars["p"])):
                post_id = int(query_vars["p"])
            # end if
            if (not php_empty(lambda : query_vars["comment_type"])):
                type = query_vars["comment_type"]
            # end if
        # end if
        if php_empty(lambda : type):
            #// Only use the comment count if not filtering by a comment_type.
            comment_count = wp_count_comments(post_id)
            #// We're looking for a known type of comment count.
            if (php_isset(lambda : comment_count.status)):
                total = comment_count.status
            # end if
        # end if
        pass
    # end if
    #// The time since the last comment count.
    time = time()
    comment = get_comment(comment_id)
    counts = wp_count_comments()
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": comment_id, "supplemental": Array({"status": comment.comment_approved if comment else "", "postId": comment.comment_post_ID if comment else "", "total_items_i18n": php_sprintf(_n("%s item", "%s items", total), number_format_i18n(total)), "total_pages": ceil(total / per_page), "total_pages_i18n": number_format_i18n(ceil(total / per_page)), "total": total, "time": time, "in_moderation": counts.moderated, "i18n_moderation_text": php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", counts.moderated), number_format_i18n(counts.moderated))})})))
    x.send()
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
def _wp_ajax_add_hierarchical_term(*args_):
    
    action = PHP_POST["action"]
    taxonomy = get_taxonomy(php_substr(action, 4))
    check_ajax_referer(action, "_ajax_nonce-add-" + taxonomy.name)
    if (not current_user_can(taxonomy.cap.edit_terms)):
        wp_die(-1)
    # end if
    names = php_explode(",", PHP_POST["new" + taxonomy.name])
    parent = int(PHP_POST["new" + taxonomy.name + "_parent"]) if (php_isset(lambda : PHP_POST["new" + taxonomy.name + "_parent"])) else 0
    if 0 > parent:
        parent = 0
    # end if
    if "category" == taxonomy.name:
        post_category = PHP_POST["post_category"] if (php_isset(lambda : PHP_POST["post_category"])) else Array()
    else:
        post_category = PHP_POST["tax_input"][taxonomy.name] if (php_isset(lambda : PHP_POST["tax_input"])) and (php_isset(lambda : PHP_POST["tax_input"][taxonomy.name])) else Array()
    # end if
    checked_categories = php_array_map("absint", post_category)
    popular_ids = wp_popular_terms_checklist(taxonomy.name, 0, 10, False)
    for cat_name in names:
        cat_name = php_trim(cat_name)
        category_nicename = sanitize_title(cat_name)
        if "" == category_nicename:
            continue
        # end if
        cat_id = wp_insert_term(cat_name, taxonomy.name, Array({"parent": parent}))
        if (not cat_id) or is_wp_error(cat_id):
            continue
        else:
            cat_id = cat_id["term_id"]
        # end if
        checked_categories[-1] = cat_id
        if parent:
            continue
        # end if
        ob_start()
        wp_terms_checklist(0, Array({"taxonomy": taxonomy.name, "descendants_and_self": cat_id, "selected_cats": checked_categories, "popular_cats": popular_ids}))
        data = ob_get_clean()
        add = Array({"what": taxonomy.name, "id": cat_id, "data": php_str_replace(Array("\n", " "), "", data), "position": -1})
    # end for
    if parent:
        #// Foncy - replace the parent and all its children.
        parent = get_term(parent, taxonomy.name)
        term_id = parent.term_id
        while True:
            
            if not (parent.parent):
                break
            # end if
            #// Get the top parent.
            parent = get_term(parent.parent, taxonomy.name)
            if is_wp_error(parent):
                break
            # end if
            term_id = parent.term_id
        # end while
        ob_start()
        wp_terms_checklist(0, Array({"taxonomy": taxonomy.name, "descendants_and_self": term_id, "selected_cats": checked_categories, "popular_cats": popular_ids}))
        data = ob_get_clean()
        add = Array({"what": taxonomy.name, "id": term_id, "data": php_str_replace(Array("\n", "    "), "", data), "position": -1})
    # end if
    ob_start()
    wp_dropdown_categories(Array({"taxonomy": taxonomy.name, "hide_empty": 0, "name": "new" + taxonomy.name + "_parent", "orderby": "name", "hierarchical": 1, "show_option_none": "&mdash; " + taxonomy.labels.parent_item + " &mdash;"}))
    sup = ob_get_clean()
    add["supplemental"] = Array({"newcat_parent": sup})
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(add))
    x.send()
# end def _wp_ajax_add_hierarchical_term
#// 
#// Ajax handler for deleting a comment.
#// 
#// @since 3.1.0
#//
def wp_ajax_delete_comment(*args_):
    
    id = int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    comment = get_comment(id)
    if (not comment):
        wp_die(time())
    # end if
    if (not current_user_can("edit_comment", comment.comment_ID)):
        wp_die(-1)
    # end if
    check_ajax_referer(str("delete-comment_") + str(id))
    status = wp_get_comment_status(comment)
    delta = -1
    if (php_isset(lambda : PHP_POST["trash"])) and 1 == PHP_POST["trash"]:
        if "trash" == status:
            wp_die(time())
        # end if
        r = wp_trash_comment(comment)
    elif (php_isset(lambda : PHP_POST["untrash"])) and 1 == PHP_POST["untrash"]:
        if "trash" != status:
            wp_die(time())
        # end if
        r = wp_untrash_comment(comment)
        #// Undo trash, not in Trash.
        if (not (php_isset(lambda : PHP_POST["comment_status"]))) or "trash" != PHP_POST["comment_status"]:
            delta = 1
        # end if
    elif (php_isset(lambda : PHP_POST["spam"])) and 1 == PHP_POST["spam"]:
        if "spam" == status:
            wp_die(time())
        # end if
        r = wp_spam_comment(comment)
    elif (php_isset(lambda : PHP_POST["unspam"])) and 1 == PHP_POST["unspam"]:
        if "spam" != status:
            wp_die(time())
        # end if
        r = wp_unspam_comment(comment)
        #// Undo spam, not in spam.
        if (not (php_isset(lambda : PHP_POST["comment_status"]))) or "spam" != PHP_POST["comment_status"]:
            delta = 1
        # end if
    elif (php_isset(lambda : PHP_POST["delete"])) and 1 == PHP_POST["delete"]:
        r = wp_delete_comment(comment)
    else:
        wp_die(-1)
    # end if
    if r:
        #// Decide if we need to send back '1' or a more complicated response including page links and comment counts.
        _wp_ajax_delete_comment_response(comment.comment_ID, delta)
    # end if
    wp_die(0)
# end def wp_ajax_delete_comment
#// 
#// Ajax handler for deleting a tag.
#// 
#// @since 3.1.0
#//
def wp_ajax_delete_tag(*args_):
    
    tag_id = int(PHP_POST["tag_ID"])
    check_ajax_referer(str("delete-tag_") + str(tag_id))
    if (not current_user_can("delete_term", tag_id)):
        wp_die(-1)
    # end if
    taxonomy = PHP_POST["taxonomy"] if (not php_empty(lambda : PHP_POST["taxonomy"])) else "post_tag"
    tag = get_term(tag_id, taxonomy)
    if (not tag) or is_wp_error(tag):
        wp_die(1)
    # end if
    if wp_delete_term(tag_id, taxonomy):
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
def wp_ajax_delete_link(*args_):
    
    id = int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str("delete-bookmark_") + str(id))
    if (not current_user_can("manage_links")):
        wp_die(-1)
    # end if
    link = get_bookmark(id)
    if (not link) or is_wp_error(link):
        wp_die(1)
    # end if
    if wp_delete_link(id):
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
def wp_ajax_delete_meta(*args_):
    
    id = int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str("delete-meta_") + str(id))
    meta = get_metadata_by_mid("post", id)
    if (not meta):
        wp_die(1)
    # end if
    if is_protected_meta(meta.meta_key, "post") or (not current_user_can("delete_post_meta", meta.post_id, meta.meta_key)):
        wp_die(-1)
    # end if
    if delete_meta(meta.meta_id):
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
def wp_ajax_delete_post(action=None, *args_):
    
    if php_empty(lambda : action):
        action = "delete-post"
    # end if
    id = int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str(action) + str("_") + str(id))
    if (not current_user_can("delete_post", id)):
        wp_die(-1)
    # end if
    if (not get_post(id)):
        wp_die(1)
    # end if
    if wp_delete_post(id):
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
def wp_ajax_trash_post(action=None, *args_):
    
    if php_empty(lambda : action):
        action = "trash-post"
    # end if
    id = int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str(action) + str("_") + str(id))
    if (not current_user_can("delete_post", id)):
        wp_die(-1)
    # end if
    if (not get_post(id)):
        wp_die(1)
    # end if
    if "trash-post" == action:
        done = wp_trash_post(id)
    else:
        done = wp_untrash_post(id)
    # end if
    if done:
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
def wp_ajax_untrash_post(action=None, *args_):
    
    if php_empty(lambda : action):
        action = "untrash-post"
    # end if
    wp_ajax_trash_post(action)
# end def wp_ajax_untrash_post
#// 
#// Ajax handler to delete a page.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_delete_page(action=None, *args_):
    
    if php_empty(lambda : action):
        action = "delete-page"
    # end if
    id = int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    check_ajax_referer(str(action) + str("_") + str(id))
    if (not current_user_can("delete_page", id)):
        wp_die(-1)
    # end if
    if (not get_post(id)):
        wp_die(1)
    # end if
    if wp_delete_post(id):
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
def wp_ajax_dim_comment(*args_):
    
    id = int(PHP_POST["id"]) if (php_isset(lambda : PHP_POST["id"])) else 0
    comment = get_comment(id)
    if (not comment):
        x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": php_new_class("WP_Error", lambda : WP_Error("invalid_comment", php_sprintf(__("Comment %d does not exist"), id)))})))
        x.send()
    # end if
    if (not current_user_can("edit_comment", comment.comment_ID)) and (not current_user_can("moderate_comments")):
        wp_die(-1)
    # end if
    current = wp_get_comment_status(comment)
    if (php_isset(lambda : PHP_POST["new"])) and PHP_POST["new"] == current:
        wp_die(time())
    # end if
    check_ajax_referer(str("approve-comment_") + str(id))
    if php_in_array(current, Array("unapproved", "spam")):
        result = wp_set_comment_status(comment, "approve", True)
    else:
        result = wp_set_comment_status(comment, "hold", True)
    # end if
    if is_wp_error(result):
        x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "comment", "id": result})))
        x.send()
    # end if
    #// Decide if we need to send back '1' or a more complicated response including page links and comment counts.
    _wp_ajax_delete_comment_response(comment.comment_ID)
    wp_die(0)
# end def wp_ajax_dim_comment
#// 
#// Ajax handler for adding a link category.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_add_link_category(action=None, *args_):
    
    if php_empty(lambda : action):
        action = "add-link-category"
    # end if
    check_ajax_referer(action)
    tax = get_taxonomy("link_category")
    if (not current_user_can(tax.cap.manage_terms)):
        wp_die(-1)
    # end if
    names = php_explode(",", wp_unslash(PHP_POST["newcat"]))
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    for cat_name in names:
        cat_name = php_trim(cat_name)
        slug = sanitize_title(cat_name)
        if "" == slug:
            continue
        # end if
        cat_id = wp_insert_term(cat_name, "link_category")
        if (not cat_id) or is_wp_error(cat_id):
            continue
        else:
            cat_id = cat_id["term_id"]
        # end if
        cat_name = esc_html(cat_name)
        x.add(Array({"what": "link-category", "id": cat_id, "data": str("<li id='link-category-") + str(cat_id) + str("'><label for='in-link-category-") + str(cat_id) + str("' class='selectit'><input value='") + esc_attr(cat_id) + str("' type='checkbox' checked='checked' name='link_category[]' id='in-link-category-") + str(cat_id) + str("'/> ") + str(cat_name) + str("</label></li>"), "position": -1}))
    # end for
    x.send()
# end def wp_ajax_add_link_category
#// 
#// Ajax handler to add a tag.
#// 
#// @since 3.1.0
#//
def wp_ajax_add_tag(*args_):
    
    check_ajax_referer("add-tag", "_wpnonce_add-tag")
    taxonomy = PHP_POST["taxonomy"] if (not php_empty(lambda : PHP_POST["taxonomy"])) else "post_tag"
    tax = get_taxonomy(taxonomy)
    if (not current_user_can(tax.cap.edit_terms)):
        wp_die(-1)
    # end if
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    tag = wp_insert_term(PHP_POST["tag-name"], taxonomy, PHP_POST)
    if tag and (not is_wp_error(tag)):
        tag = get_term(tag["term_id"], taxonomy)
    # end if
    if (not tag) or is_wp_error(tag):
        message = __("An error has occurred. Please reload the page and try again.")
        if is_wp_error(tag) and tag.get_error_message():
            message = tag.get_error_message()
        # end if
        x.add(Array({"what": "taxonomy", "data": php_new_class("WP_Error", lambda : WP_Error("error", message))}))
        x.send()
    # end if
    wp_list_table = _get_list_table("WP_Terms_List_Table", Array({"screen": PHP_POST["screen"]}))
    level = 0
    noparents = ""
    if is_taxonomy_hierarchical(taxonomy):
        level = php_count(get_ancestors(tag.term_id, taxonomy, "taxonomy"))
        ob_start()
        wp_list_table.single_row(tag, level)
        noparents = ob_get_clean()
    # end if
    ob_start()
    wp_list_table.single_row(tag)
    parents = ob_get_clean()
    x.add(Array({"what": "taxonomy", "supplemental": compact("parents", "noparents")}))
    x.add(Array({"what": "term", "position": level, "supplemental": tag}))
    x.send()
# end def wp_ajax_add_tag
#// 
#// Ajax handler for getting a tagcloud.
#// 
#// @since 3.1.0
#//
def wp_ajax_get_tagcloud(*args_):
    
    if (not (php_isset(lambda : PHP_POST["tax"]))):
        wp_die(0)
    # end if
    taxonomy = sanitize_key(PHP_POST["tax"])
    tax = get_taxonomy(taxonomy)
    if (not tax):
        wp_die(0)
    # end if
    if (not current_user_can(tax.cap.assign_terms)):
        wp_die(-1)
    # end if
    tags = get_terms(Array({"taxonomy": taxonomy, "number": 45, "orderby": "count", "order": "DESC"}))
    if php_empty(lambda : tags):
        wp_die(tax.labels.not_found)
    # end if
    if is_wp_error(tags):
        wp_die(tags.get_error_message())
    # end if
    for key,tag in tags:
        tags[key].link = "#"
        tags[key].id = tag.term_id
    # end for
    #// We need raw tag names here, so don't filter the output.
    return_ = wp_generate_tag_cloud(tags, Array({"filter": 0, "format": "list"}))
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
def wp_ajax_get_comments(action=None, *args_):
    
    global post_id
    php_check_if_defined("post_id")
    if php_empty(lambda : action):
        action = "get-comments"
    # end if
    check_ajax_referer(action)
    if php_empty(lambda : post_id) and (not php_empty(lambda : PHP_REQUEST["p"])):
        id = absint(PHP_REQUEST["p"])
        if (not php_empty(lambda : id)):
            post_id = id
        # end if
    # end if
    if php_empty(lambda : post_id):
        wp_die(-1)
    # end if
    wp_list_table = _get_list_table("WP_Post_Comments_List_Table", Array({"screen": "edit-comments"}))
    if (not current_user_can("edit_post", post_id)):
        wp_die(-1)
    # end if
    wp_list_table.prepare_items()
    if (not wp_list_table.has_items()):
        wp_die(1)
    # end if
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    ob_start()
    for comment in wp_list_table.items:
        if (not current_user_can("edit_comment", comment.comment_ID)) and 0 == comment.comment_approved:
            continue
        # end if
        get_comment(comment)
        wp_list_table.single_row(comment)
    # end for
    comment_list_item = ob_get_clean()
    x.add(Array({"what": "comments", "data": comment_list_item}))
    x.send()
# end def wp_ajax_get_comments
#// 
#// Ajax handler for replying to a comment.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_replyto_comment(action=None, *args_):
    global PHP_POST
    if php_empty(lambda : action):
        action = "replyto-comment"
    # end if
    check_ajax_referer(action, "_ajax_nonce-replyto-comment")
    comment_post_ID = int(PHP_POST["comment_post_ID"])
    post = get_post(comment_post_ID)
    if (not post):
        wp_die(-1)
    # end if
    if (not current_user_can("edit_post", comment_post_ID)):
        wp_die(-1)
    # end if
    if php_empty(lambda : post.post_status):
        wp_die(1)
    elif php_in_array(post.post_status, Array("draft", "pending", "trash")):
        wp_die(__("Error: You are replying to a comment on a draft post."))
    # end if
    user = wp_get_current_user()
    if user.exists():
        user_ID = user.ID
        comment_author = wp_slash(user.display_name)
        comment_author_email = wp_slash(user.user_email)
        comment_author_url = wp_slash(user.user_url)
        comment_content = php_trim(PHP_POST["content"])
        comment_type = php_trim(PHP_POST["comment_type"]) if (php_isset(lambda : PHP_POST["comment_type"])) else ""
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
    if "" == comment_content:
        wp_die(__("Error: Please type a comment."))
    # end if
    comment_parent = 0
    if (php_isset(lambda : PHP_POST["comment_ID"])):
        comment_parent = absint(PHP_POST["comment_ID"])
    # end if
    comment_auto_approved = False
    commentdata = compact("comment_post_ID", "comment_author", "comment_author_email", "comment_author_url", "comment_content", "comment_type", "comment_parent", "user_ID")
    #// Automatically approve parent comment.
    if (not php_empty(lambda : PHP_POST["approve_parent"])):
        parent = get_comment(comment_parent)
        if parent and "0" == parent.comment_approved and parent.comment_post_ID == comment_post_ID:
            if (not current_user_can("edit_comment", parent.comment_ID)):
                wp_die(-1)
            # end if
            if wp_set_comment_status(parent, "approve"):
                comment_auto_approved = True
            # end if
        # end if
    # end if
    comment_id = wp_new_comment(commentdata)
    if is_wp_error(comment_id):
        wp_die(comment_id.get_error_message())
    # end if
    comment = get_comment(comment_id)
    if (not comment):
        wp_die(1)
    # end if
    position = int(PHP_POST["position"]) if (php_isset(lambda : PHP_POST["position"])) and int(PHP_POST["position"]) else "-1"
    ob_start()
    if (php_isset(lambda : PHP_REQUEST["mode"])) and "dashboard" == PHP_REQUEST["mode"]:
        php_include_file(ABSPATH + "wp-admin/includes/dashboard.php", once=True)
        _wp_dashboard_recent_comments_row(comment)
    else:
        if (php_isset(lambda : PHP_REQUEST["mode"])) and "single" == PHP_REQUEST["mode"]:
            wp_list_table = _get_list_table("WP_Post_Comments_List_Table", Array({"screen": "edit-comments"}))
        else:
            wp_list_table = _get_list_table("WP_Comments_List_Table", Array({"screen": "edit-comments"}))
        # end if
        wp_list_table.single_row(comment)
    # end if
    comment_list_item = ob_get_clean()
    response = Array({"what": "comment", "id": comment.comment_ID, "data": comment_list_item, "position": position})
    counts = wp_count_comments()
    response["supplemental"] = Array({"in_moderation": counts.moderated, "i18n_comments_text": php_sprintf(_n("%s Comment", "%s Comments", counts.approved), number_format_i18n(counts.approved)), "i18n_moderation_text": php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", counts.moderated), number_format_i18n(counts.moderated))})
    if comment_auto_approved:
        response["supplemental"]["parent_approved"] = parent.comment_ID
        response["supplemental"]["parent_post_id"] = parent.comment_post_ID
    # end if
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    x.add(response)
    x.send()
# end def wp_ajax_replyto_comment
#// 
#// Ajax handler for editing a comment.
#// 
#// @since 3.1.0
#//
def wp_ajax_edit_comment(*args_):
    global PHP_POST
    check_ajax_referer("replyto-comment", "_ajax_nonce-replyto-comment")
    comment_id = int(PHP_POST["comment_ID"])
    if (not current_user_can("edit_comment", comment_id)):
        wp_die(-1)
    # end if
    if "" == PHP_POST["content"]:
        wp_die(__("Error: Please type a comment."))
    # end if
    if (php_isset(lambda : PHP_POST["status"])):
        PHP_POST["comment_status"] = PHP_POST["status"]
    # end if
    edit_comment()
    position = int(PHP_POST["position"]) if (php_isset(lambda : PHP_POST["position"])) and int(PHP_POST["position"]) else "-1"
    checkbox = 1 if (php_isset(lambda : PHP_POST["checkbox"])) and True == PHP_POST["checkbox"] else 0
    wp_list_table = _get_list_table("WP_Comments_List_Table" if checkbox else "WP_Post_Comments_List_Table", Array({"screen": "edit-comments"}))
    comment = get_comment(comment_id)
    if php_empty(lambda : comment.comment_ID):
        wp_die(-1)
    # end if
    ob_start()
    wp_list_table.single_row(comment)
    comment_list_item = ob_get_clean()
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response())
    x.add(Array({"what": "edit_comment", "id": comment.comment_ID, "data": comment_list_item, "position": position}))
    x.send()
# end def wp_ajax_edit_comment
#// 
#// Ajax handler for adding a menu item.
#// 
#// @since 3.1.0
#//
def wp_ajax_add_menu_item(*args_):
    
    check_ajax_referer("add-menu_item", "menu-settings-column-nonce")
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
    #// For performance reasons, we omit some object properties from the checklist.
    #// The following is a hacky way to restore them when adding non-custom items.
    menu_items_data = Array()
    for menu_item_data in PHP_POST["menu-item"]:
        if (not php_empty(lambda : menu_item_data["menu-item-type"])) and "custom" != menu_item_data["menu-item-type"] and (not php_empty(lambda : menu_item_data["menu-item-object-id"])):
            for case in Switch(menu_item_data["menu-item-type"]):
                if case("post_type"):
                    _object = get_post(menu_item_data["menu-item-object-id"])
                    break
                # end if
                if case("post_type_archive"):
                    _object = get_post_type_object(menu_item_data["menu-item-object"])
                    break
                # end if
                if case("taxonomy"):
                    _object = get_term(menu_item_data["menu-item-object-id"], menu_item_data["menu-item-object"])
                    break
                # end if
            # end for
            _menu_items = php_array_map("wp_setup_nav_menu_item", Array(_object))
            _menu_item = reset(_menu_items)
            #// Restore the missing menu item properties.
            menu_item_data["menu-item-description"] = _menu_item.description
        # end if
        menu_items_data[-1] = menu_item_data
    # end for
    item_ids = wp_save_nav_menu_items(0, menu_items_data)
    if is_wp_error(item_ids):
        wp_die(0)
    # end if
    menu_items = Array()
    for menu_item_id in item_ids:
        menu_obj = get_post(menu_item_id)
        if (not php_empty(lambda : menu_obj.ID)):
            menu_obj = wp_setup_nav_menu_item(menu_obj)
            menu_obj.title = __("Menu Item") if php_empty(lambda : menu_obj.title) else menu_obj.title
            menu_obj.label = menu_obj.title
            #// Don't show "(pending)" in ajax-added items.
            menu_items[-1] = menu_obj
        # end if
    # end for
    #// This filter is documented in wp-admin/includes/nav-menu.php
    walker_class_name = apply_filters("wp_edit_nav_menu_walker", "Walker_Nav_Menu_Edit", PHP_POST["menu"])
    if (not php_class_exists(walker_class_name)):
        wp_die(0)
    # end if
    if (not php_empty(lambda : menu_items)):
        args = Array({"after": "", "before": "", "link_after": "", "link_before": "", "walker": php_new_class(walker_class_name, lambda : {**locals(), **globals()}[walker_class_name]())})
        php_print(walk_nav_menu_tree(menu_items, 0, args))
    # end if
    wp_die()
# end def wp_ajax_add_menu_item
#// 
#// Ajax handler for adding meta.
#// 
#// @since 3.1.0
#//
def wp_ajax_add_meta(*args_):
    
    check_ajax_referer("add-meta", "_ajax_nonce-add-meta")
    c = 0
    pid = int(PHP_POST["post_id"])
    post = get_post(pid)
    if (php_isset(lambda : PHP_POST["metakeyselect"])) or (php_isset(lambda : PHP_POST["metakeyinput"])):
        if (not current_user_can("edit_post", pid)):
            wp_die(-1)
        # end if
        if (php_isset(lambda : PHP_POST["metakeyselect"])) and "#NONE#" == PHP_POST["metakeyselect"] and php_empty(lambda : PHP_POST["metakeyinput"]):
            wp_die(1)
        # end if
        #// If the post is an autodraft, save the post as a draft and then attempt to save the meta.
        if "auto-draft" == post.post_status:
            post_data = Array()
            post_data["action"] = "draft"
            #// Warning fix.
            post_data["post_ID"] = pid
            post_data["post_type"] = post.post_type
            post_data["post_status"] = "draft"
            now = time()
            #// translators: 1: Post creation date, 2: Post creation time.
            post_data["post_title"] = php_sprintf(__("Draft created on %1$s at %2$s"), gmdate(__("F j, Y"), now), gmdate(__("g:i a"), now))
            pid = edit_post(post_data)
            if pid:
                if is_wp_error(pid):
                    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "meta", "data": pid})))
                    x.send()
                # end if
                mid = add_meta(pid)
                if (not mid):
                    wp_die(__("Please provide a custom field value."))
                # end if
            else:
                wp_die(0)
            # end if
        else:
            mid = add_meta(pid)
            if (not mid):
                wp_die(__("Please provide a custom field value."))
            # end if
        # end if
        meta = get_metadata_by_mid("post", mid)
        pid = int(meta.post_id)
        meta = get_object_vars(meta)
        x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "meta", "id": mid, "data": _list_meta_row(meta, c), "position": 1, "supplemental": Array({"postid": pid})})))
    else:
        #// Update?
        mid = int(key(PHP_POST["meta"]))
        key = wp_unslash(PHP_POST["meta"][mid]["key"])
        value = wp_unslash(PHP_POST["meta"][mid]["value"])
        if "" == php_trim(key):
            wp_die(__("Please provide a custom field name."))
        # end if
        meta = get_metadata_by_mid("post", mid)
        if (not meta):
            wp_die(0)
            pass
        # end if
        if is_protected_meta(meta.meta_key, "post") or is_protected_meta(key, "post") or (not current_user_can("edit_post_meta", meta.post_id, meta.meta_key)) or (not current_user_can("edit_post_meta", meta.post_id, key)):
            wp_die(-1)
        # end if
        if meta.meta_value != value or meta.meta_key != key:
            u = update_metadata_by_mid("post", mid, value, key)
            if (not u):
                wp_die(0)
                pass
            # end if
        # end if
        x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "meta", "id": mid, "old_id": mid, "data": _list_meta_row(Array({"meta_key": key, "meta_value": value, "meta_id": mid}), c)}, {"position": 0, "supplemental": Array({"postid": meta.post_id})})))
    # end if
    x.send()
# end def wp_ajax_add_meta
#// 
#// Ajax handler for adding a user.
#// 
#// @since 3.1.0
#// 
#// @param string $action Action to perform.
#//
def wp_ajax_add_user(action=None, *args_):
    
    if php_empty(lambda : action):
        action = "add-user"
    # end if
    check_ajax_referer(action)
    if (not current_user_can("create_users")):
        wp_die(-1)
    # end if
    user_id = edit_user()
    if (not user_id):
        wp_die(0)
    elif is_wp_error(user_id):
        x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "user", "id": user_id})))
        x.send()
    # end if
    user_object = get_userdata(user_id)
    wp_list_table = _get_list_table("WP_Users_List_Table")
    role = current(user_object.roles)
    x = php_new_class("WP_Ajax_Response", lambda : WP_Ajax_Response(Array({"what": "user", "id": user_id, "data": wp_list_table.single_row(user_object, "", role), "supplemental": Array({"show-link": php_sprintf(__("User %s added"), "<a href=\"#user-" + user_id + "\">" + user_object.user_login + "</a>"), "role": role})})))
    x.send()
# end def wp_ajax_add_user
#// 
#// Ajax handler for closed post boxes.
#// 
#// @since 3.1.0
#//
def wp_ajax_closed_postboxes(*args_):
    
    check_ajax_referer("closedpostboxes", "closedpostboxesnonce")
    closed = php_explode(",", PHP_POST["closed"]) if (php_isset(lambda : PHP_POST["closed"])) else Array()
    closed = php_array_filter(closed)
    hidden = php_explode(",", PHP_POST["hidden"]) if (php_isset(lambda : PHP_POST["hidden"])) else Array()
    hidden = php_array_filter(hidden)
    page = PHP_POST["page"] if (php_isset(lambda : PHP_POST["page"])) else ""
    if sanitize_key(page) != page:
        wp_die(0)
    # end if
    user = wp_get_current_user()
    if (not user):
        wp_die(-1)
    # end if
    if php_is_array(closed):
        update_user_option(user.ID, str("closedpostboxes_") + str(page), closed, True)
    # end if
    if php_is_array(hidden):
        #// Postboxes that are always shown.
        hidden = php_array_diff(hidden, Array("submitdiv", "linksubmitdiv", "manage-menu", "create-menu"))
        update_user_option(user.ID, str("metaboxhidden_") + str(page), hidden, True)
    # end if
    wp_die(1)
# end def wp_ajax_closed_postboxes
#// 
#// Ajax handler for hidden columns.
#// 
#// @since 3.1.0
#//
def wp_ajax_hidden_columns(*args_):
    
    check_ajax_referer("screen-options-nonce", "screenoptionnonce")
    page = PHP_POST["page"] if (php_isset(lambda : PHP_POST["page"])) else ""
    if sanitize_key(page) != page:
        wp_die(0)
    # end if
    user = wp_get_current_user()
    if (not user):
        wp_die(-1)
    # end if
    hidden = php_explode(",", PHP_POST["hidden"]) if (not php_empty(lambda : PHP_POST["hidden"])) else Array()
    update_user_option(user.ID, str("manage") + str(page) + str("columnshidden"), hidden, True)
    wp_die(1)
# end def wp_ajax_hidden_columns
#// 
#// Ajax handler for updating whether to display the welcome panel.
#// 
#// @since 3.1.0
#//
def wp_ajax_update_welcome_panel(*args_):
    
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
def wp_ajax_menu_get_metabox(*args_):
    
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
    if (php_isset(lambda : PHP_POST["item-type"])) and "post_type" == PHP_POST["item-type"]:
        type = "posttype"
        callback = "wp_nav_menu_item_post_type_meta_box"
        items = get_post_types(Array({"show_in_nav_menus": True}), "object")
    elif (php_isset(lambda : PHP_POST["item-type"])) and "taxonomy" == PHP_POST["item-type"]:
        type = "taxonomy"
        callback = "wp_nav_menu_item_taxonomy_meta_box"
        items = get_taxonomies(Array({"show_ui": True}), "object")
    # end if
    if (not php_empty(lambda : PHP_POST["item-object"])) and (php_isset(lambda : items[PHP_POST["item-object"]])):
        menus_meta_box_object = items[PHP_POST["item-object"]]
        #// This filter is documented in wp-admin/includes/nav-menu.php
        item = apply_filters("nav_menu_meta_box_object", menus_meta_box_object)
        box_args = Array({"id": "add-" + item.name, "title": item.labels.name, "callback": callback, "args": item})
        ob_start()
        callback(None, box_args)
        markup = ob_get_clean()
        php_print(wp_json_encode(Array({"replace-id": type + "-" + item.name, "markup": markup})))
    # end if
    wp_die()
# end def wp_ajax_menu_get_metabox
#// 
#// Ajax handler for internal linking.
#// 
#// @since 3.1.0
#//
def wp_ajax_wp_link_ajax(*args_):
    
    check_ajax_referer("internal-linking", "_ajax_linking_nonce")
    args = Array()
    if (php_isset(lambda : PHP_POST["search"])):
        args["s"] = wp_unslash(PHP_POST["search"])
    # end if
    if (php_isset(lambda : PHP_POST["term"])):
        args["s"] = wp_unslash(PHP_POST["term"])
    # end if
    args["pagenum"] = absint(PHP_POST["page"]) if (not php_empty(lambda : PHP_POST["page"])) else 1
    if (not php_class_exists("_WP_Editors", False)):
        php_include_file(ABSPATH + WPINC + "/class-wp-editor.php", once=False)
    # end if
    results = _WP_Editors.wp_link_query(args)
    if (not (php_isset(lambda : results))):
        wp_die(0)
    # end if
    php_print(wp_json_encode(results))
    php_print("\n")
    wp_die()
# end def wp_ajax_wp_link_ajax
#// 
#// Ajax handler for menu locations save.
#// 
#// @since 3.1.0
#//
def wp_ajax_menu_locations_save(*args_):
    
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
def wp_ajax_meta_box_order(*args_):
    
    check_ajax_referer("meta-box-order")
    order = PHP_POST["order"] if (php_isset(lambda : PHP_POST["order"])) else False
    page_columns = PHP_POST["page_columns"] if (php_isset(lambda : PHP_POST["page_columns"])) else "auto"
    if "auto" != page_columns:
        page_columns = int(page_columns)
    # end if
    page = PHP_POST["page"] if (php_isset(lambda : PHP_POST["page"])) else ""
    if sanitize_key(page) != page:
        wp_die(0)
    # end if
    user = wp_get_current_user()
    if (not user):
        wp_die(-1)
    # end if
    if order:
        update_user_option(user.ID, str("meta-box-order_") + str(page), order, True)
    # end if
    if page_columns:
        update_user_option(user.ID, str("screen_layout_") + str(page), page_columns, True)
    # end if
    wp_die(1)
# end def wp_ajax_meta_box_order
#// 
#// Ajax handler for menu quick searching.
#// 
#// @since 3.1.0
#//
def wp_ajax_menu_quick_search(*args_):
    
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
def wp_ajax_get_permalink(*args_):
    
    check_ajax_referer("getpermalink", "getpermalinknonce")
    post_id = php_intval(PHP_POST["post_id"]) if (php_isset(lambda : PHP_POST["post_id"])) else 0
    wp_die(get_preview_post_link(post_id))
# end def wp_ajax_get_permalink
#// 
#// Ajax handler to retrieve a sample permalink.
#// 
#// @since 3.1.0
#//
def wp_ajax_sample_permalink(*args_):
    
    check_ajax_referer("samplepermalink", "samplepermalinknonce")
    post_id = php_intval(PHP_POST["post_id"]) if (php_isset(lambda : PHP_POST["post_id"])) else 0
    title = PHP_POST["new_title"] if (php_isset(lambda : PHP_POST["new_title"])) else ""
    slug = PHP_POST["new_slug"] if (php_isset(lambda : PHP_POST["new_slug"])) else None
    wp_die(get_sample_permalink_html(post_id, title, slug))
# end def wp_ajax_sample_permalink
#// 
#// Ajax handler for Quick Edit saving a post from a list table.
#// 
#// @since 3.1.0
#// 
#// @global string $mode List table view mode.
#//
def wp_ajax_inline_save(*args_):
    
    global mode
    php_check_if_defined("mode")
    check_ajax_referer("inlineeditnonce", "_inline_edit")
    if (not (php_isset(lambda : PHP_POST["post_ID"]))) or (not int(PHP_POST["post_ID"])):
        wp_die()
    # end if
    post_ID = int(PHP_POST["post_ID"])
    if "page" == PHP_POST["post_type"]:
        if (not current_user_can("edit_page", post_ID)):
            wp_die(__("Sorry, you are not allowed to edit this page."))
        # end if
    else:
        if (not current_user_can("edit_post", post_ID)):
            wp_die(__("Sorry, you are not allowed to edit this post."))
        # end if
    # end if
    last = wp_check_post_lock(post_ID)
    if last:
        last_user = get_userdata(last)
        last_user_name = last_user.display_name if last_user else __("Someone")
        #// translators: %s: User's display name.
        msg_template = __("Saving is disabled: %s is currently editing this post.")
        if "page" == PHP_POST["post_type"]:
            #// translators: %s: User's display name.
            msg_template = __("Saving is disabled: %s is currently editing this page.")
        # end if
        printf(msg_template, esc_html(last_user_name))
        wp_die()
    # end if
    data = PHP_POST
    post = get_post(post_ID, ARRAY_A)
    #// Since it's coming from the database.
    post = wp_slash(post)
    data["content"] = post["post_content"]
    data["excerpt"] = post["post_excerpt"]
    #// Rename.
    data["user_ID"] = get_current_user_id()
    if (php_isset(lambda : data["post_parent"])):
        data["parent_id"] = data["post_parent"]
    # end if
    #// Status.
    if (php_isset(lambda : data["keep_private"])) and "private" == data["keep_private"]:
        data["visibility"] = "private"
        data["post_status"] = "private"
    else:
        data["post_status"] = data["_status"]
    # end if
    if php_empty(lambda : data["comment_status"]):
        data["comment_status"] = "closed"
    # end if
    if php_empty(lambda : data["ping_status"]):
        data["ping_status"] = "closed"
    # end if
    #// Exclude terms from taxonomies that are not supposed to appear in Quick Edit.
    if (not php_empty(lambda : data["tax_input"])):
        for taxonomy,terms in data["tax_input"]:
            tax_object = get_taxonomy(taxonomy)
            #// This filter is documented in wp-admin/includes/class-wp-posts-list-table.php
            if (not apply_filters("quick_edit_show_taxonomy", tax_object.show_in_quick_edit, taxonomy, post["post_type"])):
                data["tax_input"][taxonomy] = None
            # end if
        # end for
    # end if
    #// Hack: wp_unique_post_slug() doesn't work for drafts, so we will fake that our post is published.
    if (not php_empty(lambda : data["post_name"])) and php_in_array(post["post_status"], Array("draft", "pending")):
        post["post_status"] = "publish"
        data["post_name"] = wp_unique_post_slug(data["post_name"], post["ID"], post["post_status"], post["post_type"], post["post_parent"])
    # end if
    #// Update the post.
    edit_post()
    wp_list_table = _get_list_table("WP_Posts_List_Table", Array({"screen": PHP_POST["screen"]}))
    mode = "excerpt" if "excerpt" == PHP_POST["post_view"] else "list"
    level = 0
    if is_post_type_hierarchical(wp_list_table.screen.post_type):
        request_post = Array(get_post(PHP_POST["post_ID"]))
        parent = request_post[0].post_parent
        while True:
            
            if not (parent > 0):
                break
            # end if
            parent_post = get_post(parent)
            parent = parent_post.post_parent
            level += 1
        # end while
    # end if
    wp_list_table.display_rows(Array(get_post(PHP_POST["post_ID"])), level)
    wp_die()
# end def wp_ajax_inline_save
#// 
#// Ajax handler for quick edit saving for a term.
#// 
#// @since 3.1.0
#//
def wp_ajax_inline_save_tax(*args_):
    global PHP_POST
    check_ajax_referer("taxinlineeditnonce", "_inline_edit")
    taxonomy = sanitize_key(PHP_POST["taxonomy"])
    tax = get_taxonomy(taxonomy)
    if (not tax):
        wp_die(0)
    # end if
    if (not (php_isset(lambda : PHP_POST["tax_ID"]))) or (not int(PHP_POST["tax_ID"])):
        wp_die(-1)
    # end if
    id = int(PHP_POST["tax_ID"])
    if (not current_user_can("edit_term", id)):
        wp_die(-1)
    # end if
    wp_list_table = _get_list_table("WP_Terms_List_Table", Array({"screen": "edit-" + taxonomy}))
    tag = get_term(id, taxonomy)
    PHP_POST["description"] = tag.description
    updated = wp_update_term(id, taxonomy, PHP_POST)
    if updated and (not is_wp_error(updated)):
        tag = get_term(updated["term_id"], taxonomy)
        if (not tag) or is_wp_error(tag):
            if is_wp_error(tag) and tag.get_error_message():
                wp_die(tag.get_error_message())
            # end if
            wp_die(__("Item not updated."))
        # end if
    else:
        if is_wp_error(updated) and updated.get_error_message():
            wp_die(updated.get_error_message())
        # end if
        wp_die(__("Item not updated."))
    # end if
    level = 0
    parent = tag.parent
    while True:
        
        if not (parent > 0):
            break
        # end if
        parent_tag = get_term(parent, taxonomy)
        parent = parent_tag.parent
        level += 1
    # end while
    wp_list_table.single_row(tag, level)
    wp_die()
# end def wp_ajax_inline_save_tax
#// 
#// Ajax handler for querying posts for the Find Posts modal.
#// 
#// @see window.findPosts
#// 
#// @since 3.1.0
#//
def wp_ajax_find_posts(*args_):
    
    check_ajax_referer("find-posts")
    post_types = get_post_types(Array({"public": True}), "objects")
    post_types["attachment"] = None
    s = wp_unslash(PHP_POST["ps"])
    args = Array({"post_type": php_array_keys(post_types), "post_status": "any", "posts_per_page": 50})
    if "" != s:
        args["s"] = s
    # end if
    posts = get_posts(args)
    if (not posts):
        wp_send_json_error(__("No items found."))
    # end if
    html = "<table class=\"widefat\"><thead><tr><th class=\"found-radio\"><br /></th><th>" + __("Title") + "</th><th class=\"no-break\">" + __("Type") + "</th><th class=\"no-break\">" + __("Date") + "</th><th class=\"no-break\">" + __("Status") + "</th></tr></thead><tbody>"
    alt = ""
    for post in posts:
        title = post.post_title if php_trim(post.post_title) else __("(no title)")
        alt = "" if "alternate" == alt else "alternate"
        for case in Switch(post.post_status):
            if case("publish"):
                pass
            # end if
            if case("private"):
                stat = __("Published")
                break
            # end if
            if case("future"):
                stat = __("Scheduled")
                break
            # end if
            if case("pending"):
                stat = __("Pending Review")
                break
            # end if
            if case("draft"):
                stat = __("Draft")
                break
            # end if
        # end for
        if "0000-00-00 00:00:00" == post.post_date:
            time = ""
        else:
            #// translators: Date format in table columns, see https://www.php.net/date
            time = mysql2date(__("Y/m/d"), post.post_date)
        # end if
        html += "<tr class=\"" + php_trim("found-posts " + alt) + "\"><td class=\"found-radio\"><input type=\"radio\" id=\"found-" + post.ID + "\" name=\"found_post_id\" value=\"" + esc_attr(post.ID) + "\"></td>"
        html += "<td><label for=\"found-" + post.ID + "\">" + esc_html(title) + "</label></td><td class=\"no-break\">" + esc_html(post_types[post.post_type].labels.singular_name) + "</td><td class=\"no-break\">" + esc_html(time) + "</td><td class=\"no-break\">" + esc_html(stat) + " </td></tr>" + "\n\n"
    # end for
    html += "</tbody></table>"
    wp_send_json_success(html)
# end def wp_ajax_find_posts
#// 
#// Ajax handler for saving the widgets order.
#// 
#// @since 3.1.0
#//
def wp_ajax_widgets_order(*args_):
    
    check_ajax_referer("save-sidebar-widgets", "savewidgets")
    if (not current_user_can("edit_theme_options")):
        wp_die(-1)
    # end if
    PHP_POST["savewidgets"] = None
    PHP_POST["action"] = None
    #// Save widgets order for all sidebars.
    if php_is_array(PHP_POST["sidebars"]):
        sidebars = Array()
        for key,val in wp_unslash(PHP_POST["sidebars"]):
            sb = Array()
            if (not php_empty(lambda : val)):
                val = php_explode(",", val)
                for k,v in val:
                    if php_strpos(v, "widget-") == False:
                        continue
                    # end if
                    sb[k] = php_substr(v, php_strpos(v, "_") + 1)
                # end for
            # end if
            sidebars[key] = sb
        # end for
        wp_set_sidebars_widgets(sidebars)
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
def wp_ajax_save_widget(*args_):
    global PHP_POST
    global wp_registered_widgets,wp_registered_widget_controls,wp_registered_widget_updates
    php_check_if_defined("wp_registered_widgets","wp_registered_widget_controls","wp_registered_widget_updates")
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
    id_base = wp_unslash(PHP_POST["id_base"])
    widget_id = wp_unslash(PHP_POST["widget-id"])
    sidebar_id = PHP_POST["sidebar"]
    multi_number = int(PHP_POST["multi_number"]) if (not php_empty(lambda : PHP_POST["multi_number"])) else 0
    settings = PHP_POST["widget-" + id_base] if (php_isset(lambda : PHP_POST["widget-" + id_base])) and php_is_array(PHP_POST["widget-" + id_base]) else False
    error = "<p>" + __("An error has occurred. Please reload the page and try again.") + "</p>"
    sidebars = wp_get_sidebars_widgets()
    sidebar = sidebars[sidebar_id] if (php_isset(lambda : sidebars[sidebar_id])) else Array()
    #// Delete.
    if (php_isset(lambda : PHP_POST["delete_widget"])) and PHP_POST["delete_widget"]:
        if (not (php_isset(lambda : wp_registered_widgets[widget_id]))):
            wp_die(error)
        # end if
        sidebar = php_array_diff(sidebar, Array(widget_id))
        PHP_POST = Array({"sidebar": sidebar_id, "widget-" + id_base: Array(), "the-widget-id": widget_id, "delete_widget": "1"})
        #// This action is documented in wp-admin/widgets.php
        do_action("delete_widget", widget_id, sidebar_id, id_base)
    elif settings and php_preg_match("/__i__|%i%/", key(settings)):
        if (not multi_number):
            wp_die(error)
        # end if
        PHP_POST["widget-" + id_base] = Array({multi_number: reset(settings)})
        widget_id = id_base + "-" + multi_number
        sidebar[-1] = widget_id
    # end if
    PHP_POST["widget-id"] = sidebar
    for name,control in wp_registered_widget_updates:
        if name == id_base:
            if (not php_is_callable(control["callback"])):
                continue
            # end if
            ob_start()
            call_user_func_array(control["callback"], control["params"])
            ob_end_clean()
            break
        # end if
    # end for
    if (php_isset(lambda : PHP_POST["delete_widget"])) and PHP_POST["delete_widget"]:
        sidebars[sidebar_id] = sidebar
        wp_set_sidebars_widgets(sidebars)
        php_print(str("deleted:") + str(widget_id))
        wp_die()
    # end if
    if (not php_empty(lambda : PHP_POST["add_new"])):
        wp_die()
    # end if
    form = wp_registered_widget_controls[widget_id]
    if form:
        call_user_func_array(form["callback"], form["params"])
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
def wp_ajax_update_widget(*args_):
    
    global wp_customize
    php_check_if_defined("wp_customize")
    wp_customize.widgets.wp_ajax_update_widget()
# end def wp_ajax_update_widget
#// 
#// Ajax handler for removing inactive widgets.
#// 
#// @since 4.4.0
#//
def wp_ajax_delete_inactive_widgets(*args_):
    
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
    sidebars_widgets = wp_get_sidebars_widgets()
    for key,widget_id in sidebars_widgets["wp_inactive_widgets"]:
        pieces = php_explode("-", widget_id)
        multi_number = php_array_pop(pieces)
        id_base = php_implode("-", pieces)
        widget = get_option("widget_" + id_base)
        widget[multi_number] = None
        update_option("widget_" + id_base, widget)
        sidebars_widgets["wp_inactive_widgets"][key] = None
    # end for
    wp_set_sidebars_widgets(sidebars_widgets)
    wp_die()
# end def wp_ajax_delete_inactive_widgets
#// 
#// Ajax handler for creating missing image sub-sizes for just uploaded images.
#// 
#// @since 5.3.0
#//
def wp_ajax_media_create_image_subsizes(*args_):
    
    check_ajax_referer("media-form")
    if (not current_user_can("upload_files")):
        wp_send_json_error(Array({"message": __("Sorry, you are not allowed to upload files.")}))
    # end if
    if php_empty(lambda : PHP_POST["attachment_id"]):
        wp_send_json_error(Array({"message": __("Upload failed. Please reload and try again.")}))
    # end if
    attachment_id = int(PHP_POST["attachment_id"])
    if (not php_empty(lambda : PHP_POST["_wp_upload_failed_cleanup"])):
        #// Upload failed. Cleanup.
        if wp_attachment_is_image(attachment_id) and current_user_can("delete_post", attachment_id):
            attachment = get_post(attachment_id)
            #// Created at most 10 min ago.
            if attachment and time() - strtotime(attachment.post_date_gmt) < 600:
                wp_delete_attachment(attachment_id, True)
                wp_send_json_success()
            # end if
        # end if
    # end if
    #// Set a custom header with the attachment_id.
    #// Used by the browser/client to resume creating image sub-sizes after a PHP fatal error.
    if (not php_headers_sent()):
        php_header("X-WP-Upload-Attachment-ID: " + attachment_id)
    # end if
    #// This can still be pretty slow and cause timeout or out of memory errors.
    #// The js that handles the response would need to also handle HTTP 500 errors.
    wp_update_image_subsizes(attachment_id)
    if (not php_empty(lambda : PHP_POST["_legacy_support"])):
        #// The old (inline) uploader. Only needs the attachment_id.
        response = Array({"id": attachment_id})
    else:
        #// Media modal and Media Library grid view.
        response = wp_prepare_attachment_for_js(attachment_id)
        if (not response):
            wp_send_json_error(Array({"message": __("Upload failed.")}))
        # end if
    # end if
    #// At this point the image has been uploaded successfully.
    wp_send_json_success(response)
# end def wp_ajax_media_create_image_subsizes
#// 
#// Ajax handler for uploading attachments
#// 
#// @since 3.3.0
#//
def wp_ajax_upload_attachment(*args_):
    
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
        post_id = PHP_REQUEST["post_id"]
        if (not current_user_can("edit_post", post_id)):
            php_print(wp_json_encode(Array({"success": False, "data": Array({"message": __("Sorry, you are not allowed to attach files to this post."), "filename": esc_html(PHP_FILES["async-upload"]["name"])})})))
            wp_die()
        # end if
    else:
        post_id = None
    # end if
    post_data = _wp_get_allowed_postdata(_wp_translate_postdata(False, PHP_REQUEST["post_data"])) if (not php_empty(lambda : PHP_REQUEST["post_data"])) else Array()
    if is_wp_error(post_data):
        wp_die(post_data.get_error_message())
    # end if
    #// If the context is custom header or background, make sure the uploaded file is an image.
    if (php_isset(lambda : post_data["context"])) and php_in_array(post_data["context"], Array("custom-header", "custom-background")):
        wp_filetype = wp_check_filetype_and_ext(PHP_FILES["async-upload"]["tmp_name"], PHP_FILES["async-upload"]["name"])
        if (not wp_match_mime_types("image", wp_filetype["type"])):
            php_print(wp_json_encode(Array({"success": False, "data": Array({"message": __("The uploaded file is not a valid image. Please try again."), "filename": esc_html(PHP_FILES["async-upload"]["name"])})})))
            wp_die()
        # end if
    # end if
    attachment_id = media_handle_upload("async-upload", post_id, post_data)
    if is_wp_error(attachment_id):
        php_print(wp_json_encode(Array({"success": False, "data": Array({"message": attachment_id.get_error_message(), "filename": esc_html(PHP_FILES["async-upload"]["name"])})})))
        wp_die()
    # end if
    if (php_isset(lambda : post_data["context"])) and (php_isset(lambda : post_data["theme"])):
        if "custom-background" == post_data["context"]:
            update_post_meta(attachment_id, "_wp_attachment_is_custom_background", post_data["theme"])
        # end if
        if "custom-header" == post_data["context"]:
            update_post_meta(attachment_id, "_wp_attachment_is_custom_header", post_data["theme"])
        # end if
    # end if
    attachment = wp_prepare_attachment_for_js(attachment_id)
    if (not attachment):
        wp_die()
    # end if
    php_print(wp_json_encode(Array({"success": True, "data": attachment})))
    wp_die()
# end def wp_ajax_upload_attachment
#// 
#// Ajax handler for image editing.
#// 
#// @since 3.1.0
#//
def wp_ajax_image_editor(*args_):
    
    attachment_id = php_intval(PHP_POST["postid"])
    if php_empty(lambda : attachment_id) or (not current_user_can("edit_post", attachment_id)):
        wp_die(-1)
    # end if
    check_ajax_referer(str("image_editor-") + str(attachment_id))
    php_include_file(ABSPATH + "wp-admin/includes/image-edit.php", once=False)
    msg = False
    for case in Switch(PHP_POST["do"]):
        if case("save"):
            msg = wp_save_image(attachment_id)
            msg = wp_json_encode(msg)
            wp_die(msg)
            break
        # end if
        if case("scale"):
            msg = wp_save_image(attachment_id)
            break
        # end if
        if case("restore"):
            msg = wp_restore_image(attachment_id)
            break
        # end if
    # end for
    wp_image_editor(attachment_id, msg)
    wp_die()
# end def wp_ajax_image_editor
#// 
#// Ajax handler for setting the featured image.
#// 
#// @since 3.1.0
#//
def wp_ajax_set_post_thumbnail(*args_):
    
    json = (not php_empty(lambda : PHP_REQUEST["json"]))
    #// New-style request.
    post_ID = php_intval(PHP_POST["post_id"])
    if (not current_user_can("edit_post", post_ID)):
        wp_die(-1)
    # end if
    thumbnail_id = php_intval(PHP_POST["thumbnail_id"])
    if json:
        check_ajax_referer(str("update-post_") + str(post_ID))
    else:
        check_ajax_referer(str("set_post_thumbnail-") + str(post_ID))
    # end if
    if "-1" == thumbnail_id:
        if delete_post_thumbnail(post_ID):
            return_ = _wp_post_thumbnail_html(None, post_ID)
            wp_send_json_success(return_) if json else wp_die(return_)
        else:
            wp_die(0)
        # end if
    # end if
    if set_post_thumbnail(post_ID, thumbnail_id):
        return_ = _wp_post_thumbnail_html(thumbnail_id, post_ID)
        wp_send_json_success(return_) if json else wp_die(return_)
    # end if
    wp_die(0)
# end def wp_ajax_set_post_thumbnail
#// 
#// Ajax handler for retrieving HTML for the featured image.
#// 
#// @since 4.6.0
#//
def wp_ajax_get_post_thumbnail_html(*args_):
    
    post_ID = php_intval(PHP_POST["post_id"])
    check_ajax_referer(str("update-post_") + str(post_ID))
    if (not current_user_can("edit_post", post_ID)):
        wp_die(-1)
    # end if
    thumbnail_id = php_intval(PHP_POST["thumbnail_id"])
    #// For backward compatibility, -1 refers to no featured image.
    if -1 == thumbnail_id:
        thumbnail_id = None
    # end if
    return_ = _wp_post_thumbnail_html(thumbnail_id, post_ID)
    wp_send_json_success(return_)
# end def wp_ajax_get_post_thumbnail_html
#// 
#// Ajax handler for setting the featured image for an attachment.
#// 
#// @since 4.0.0
#// 
#// @see set_post_thumbnail()
#//
def wp_ajax_set_attachment_thumbnail(*args_):
    
    if php_empty(lambda : PHP_POST["urls"]) or (not php_is_array(PHP_POST["urls"])):
        wp_send_json_error()
    # end if
    thumbnail_id = int(PHP_POST["thumbnail_id"])
    if php_empty(lambda : thumbnail_id):
        wp_send_json_error()
    # end if
    post_ids = Array()
    #// For each URL, try to find its corresponding post ID.
    for url in PHP_POST["urls"]:
        post_id = attachment_url_to_postid(url)
        if (not php_empty(lambda : post_id)):
            post_ids[-1] = post_id
        # end if
    # end for
    if php_empty(lambda : post_ids):
        wp_send_json_error()
    # end if
    success = 0
    #// For each found attachment, set its thumbnail.
    for post_id in post_ids:
        if (not current_user_can("edit_post", post_id)):
            continue
        # end if
        if set_post_thumbnail(post_id, thumbnail_id):
            success += 1
        # end if
    # end for
    if 0 == success:
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
def wp_ajax_date_format(*args_):
    
    wp_die(date_i18n(sanitize_option("date_format", wp_unslash(PHP_POST["date"]))))
# end def wp_ajax_date_format
#// 
#// Ajax handler for time formatting.
#// 
#// @since 3.1.0
#//
def wp_ajax_time_format(*args_):
    
    wp_die(date_i18n(sanitize_option("time_format", wp_unslash(PHP_POST["date"]))))
# end def wp_ajax_time_format
#// 
#// Ajax handler for saving posts from the fullscreen editor.
#// 
#// @since 3.1.0
#// @deprecated 4.3.0
#//
def wp_ajax_wp_fullscreen_save_post(*args_):
    
    post_id = int(PHP_POST["post_ID"]) if (php_isset(lambda : PHP_POST["post_ID"])) else 0
    post = None
    if post_id:
        post = get_post(post_id)
    # end if
    check_ajax_referer("update-post_" + post_id, "_wpnonce")
    post_id = edit_post()
    if is_wp_error(post_id):
        wp_send_json_error()
    # end if
    if post:
        last_date = mysql2date(__("F j, Y"), post.post_modified)
        last_time = mysql2date(__("g:i a"), post.post_modified)
    else:
        last_date = date_i18n(__("F j, Y"))
        last_time = date_i18n(__("g:i a"))
    # end if
    last_id = get_post_meta(post_id, "_edit_last", True)
    if last_id:
        last_user = get_userdata(last_id)
        #// translators: 1: User's display name, 2: Date of last edit, 3: Time of last edit.
        last_edited = php_sprintf(__("Last edited by %1$s on %2$s at %3$s"), esc_html(last_user.display_name), last_date, last_time)
    else:
        #// translators: 1: Date of last edit, 2: Time of last edit.
        last_edited = php_sprintf(__("Last edited on %1$s at %2$s"), last_date, last_time)
    # end if
    wp_send_json_success(Array({"last_edited": last_edited}))
# end def wp_ajax_wp_fullscreen_save_post
#// 
#// Ajax handler for removing a post lock.
#// 
#// @since 3.1.0
#//
def wp_ajax_wp_remove_post_lock(*args_):
    
    if php_empty(lambda : PHP_POST["post_ID"]) or php_empty(lambda : PHP_POST["active_post_lock"]):
        wp_die(0)
    # end if
    post_id = int(PHP_POST["post_ID"])
    post = get_post(post_id)
    if (not post):
        wp_die(0)
    # end if
    check_ajax_referer("update-post_" + post_id)
    if (not current_user_can("edit_post", post_id)):
        wp_die(-1)
    # end if
    active_lock = php_array_map("absint", php_explode(":", PHP_POST["active_post_lock"]))
    if get_current_user_id() != active_lock[1]:
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
    new_lock = time() - apply_filters("wp_check_post_lock_window", 150) + 5 + ":" + active_lock[1]
    update_post_meta(post_id, "_edit_lock", new_lock, php_implode(":", active_lock))
    wp_die(1)
# end def wp_ajax_wp_remove_post_lock
#// 
#// Ajax handler for dismissing a WordPress pointer.
#// 
#// @since 3.1.0
#//
def wp_ajax_dismiss_wp_pointer(*args_):
    
    pointer = PHP_POST["pointer"]
    if sanitize_key(pointer) != pointer:
        wp_die(0)
    # end if
    #// check_ajax_referer( 'dismiss-pointer_' . $pointer );
    dismissed = php_array_filter(php_explode(",", str(get_user_meta(get_current_user_id(), "dismissed_wp_pointers", True))))
    if php_in_array(pointer, dismissed):
        wp_die(0)
    # end if
    dismissed[-1] = pointer
    dismissed = php_implode(",", dismissed)
    update_user_meta(get_current_user_id(), "dismissed_wp_pointers", dismissed)
    wp_die(1)
# end def wp_ajax_dismiss_wp_pointer
#// 
#// Ajax handler for getting an attachment.
#// 
#// @since 3.5.0
#//
def wp_ajax_get_attachment(*args_):
    
    if (not (php_isset(lambda : PHP_REQUEST["id"]))):
        wp_send_json_error()
    # end if
    id = absint(PHP_REQUEST["id"])
    if (not id):
        wp_send_json_error()
    # end if
    post = get_post(id)
    if (not post):
        wp_send_json_error()
    # end if
    if "attachment" != post.post_type:
        wp_send_json_error()
    # end if
    if (not current_user_can("upload_files")):
        wp_send_json_error()
    # end if
    attachment = wp_prepare_attachment_for_js(id)
    if (not attachment):
        wp_send_json_error()
    # end if
    wp_send_json_success(attachment)
# end def wp_ajax_get_attachment
#// 
#// Ajax handler for querying attachments.
#// 
#// @since 3.5.0
#//
def wp_ajax_query_attachments(*args_):
    
    if (not current_user_can("upload_files")):
        wp_send_json_error()
    # end if
    query = PHP_REQUEST["query"] if (php_isset(lambda : PHP_REQUEST["query"])) else Array()
    keys = Array("s", "order", "orderby", "posts_per_page", "paged", "post_mime_type", "post_parent", "author", "post__in", "post__not_in", "year", "monthnum")
    for t in get_taxonomies_for_attachments("objects"):
        if t.query_var and (php_isset(lambda : query[t.query_var])):
            keys[-1] = t.query_var
        # end if
    # end for
    query = php_array_intersect_key(query, php_array_flip(keys))
    query["post_type"] = "attachment"
    if MEDIA_TRASH and (not php_empty(lambda : PHP_REQUEST["query"]["post_status"])) and "trash" == PHP_REQUEST["query"]["post_status"]:
        query["post_status"] = "trash"
    else:
        query["post_status"] = "inherit"
    # end if
    if current_user_can(get_post_type_object("attachment").cap.read_private_posts):
        query["post_status"] += ",private"
    # end if
    #// Filter query clauses to include filenames.
    if (php_isset(lambda : query["s"])):
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
    query = apply_filters("ajax_query_attachments_args", query)
    query = php_new_class("WP_Query", lambda : WP_Query(query))
    posts = php_array_map("wp_prepare_attachment_for_js", query.posts)
    posts = php_array_filter(posts)
    wp_send_json_success(posts)
# end def wp_ajax_query_attachments
#// 
#// Ajax handler for updating attachment attributes.
#// 
#// @since 3.5.0
#//
def wp_ajax_save_attachment(*args_):
    
    if (not (php_isset(lambda : PHP_REQUEST["id"]))) or (not (php_isset(lambda : PHP_REQUEST["changes"]))):
        wp_send_json_error()
    # end if
    id = absint(PHP_REQUEST["id"])
    if (not id):
        wp_send_json_error()
    # end if
    check_ajax_referer("update-post_" + id, "nonce")
    if (not current_user_can("edit_post", id)):
        wp_send_json_error()
    # end if
    changes = PHP_REQUEST["changes"]
    post = get_post(id, ARRAY_A)
    if "attachment" != post["post_type"]:
        wp_send_json_error()
    # end if
    if (php_isset(lambda : changes["parent"])):
        post["post_parent"] = changes["parent"]
    # end if
    if (php_isset(lambda : changes["title"])):
        post["post_title"] = changes["title"]
    # end if
    if (php_isset(lambda : changes["caption"])):
        post["post_excerpt"] = changes["caption"]
    # end if
    if (php_isset(lambda : changes["description"])):
        post["post_content"] = changes["description"]
    # end if
    if MEDIA_TRASH and (php_isset(lambda : changes["status"])):
        post["post_status"] = changes["status"]
    # end if
    if (php_isset(lambda : changes["alt"])):
        alt = wp_unslash(changes["alt"])
        if get_post_meta(id, "_wp_attachment_image_alt", True) != alt:
            alt = wp_strip_all_tags(alt, True)
            update_post_meta(id, "_wp_attachment_image_alt", wp_slash(alt))
        # end if
    # end if
    if wp_attachment_is("audio", post["ID"]):
        changed = False
        id3data = wp_get_attachment_metadata(post["ID"])
        if (not php_is_array(id3data)):
            changed = True
            id3data = Array()
        # end if
        for key,label in wp_get_attachment_id3_keys(post, "edit"):
            if (php_isset(lambda : changes[key])):
                changed = True
                id3data[key] = sanitize_text_field(wp_unslash(changes[key]))
            # end if
        # end for
        if changed:
            wp_update_attachment_metadata(id, id3data)
        # end if
    # end if
    if MEDIA_TRASH and (php_isset(lambda : changes["status"])) and "trash" == changes["status"]:
        wp_delete_post(id)
    else:
        wp_update_post(post)
    # end if
    wp_send_json_success()
# end def wp_ajax_save_attachment
#// 
#// Ajax handler for saving backward compatible attachment attributes.
#// 
#// @since 3.5.0
#//
def wp_ajax_save_attachment_compat(*args_):
    
    if (not (php_isset(lambda : PHP_REQUEST["id"]))):
        wp_send_json_error()
    # end if
    id = absint(PHP_REQUEST["id"])
    if (not id):
        wp_send_json_error()
    # end if
    if php_empty(lambda : PHP_REQUEST["attachments"]) or php_empty(lambda : PHP_REQUEST["attachments"][id]):
        wp_send_json_error()
    # end if
    attachment_data = PHP_REQUEST["attachments"][id]
    check_ajax_referer("update-post_" + id, "nonce")
    if (not current_user_can("edit_post", id)):
        wp_send_json_error()
    # end if
    post = get_post(id, ARRAY_A)
    if "attachment" != post["post_type"]:
        wp_send_json_error()
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    post = apply_filters("attachment_fields_to_save", post, attachment_data)
    if (php_isset(lambda : post["errors"])):
        errors = post["errors"]
        post["errors"] = None
    # end if
    wp_update_post(post)
    for taxonomy in get_attachment_taxonomies(post):
        if (php_isset(lambda : attachment_data[taxonomy])):
            wp_set_object_terms(id, php_array_map("trim", php_preg_split("/,+/", attachment_data[taxonomy])), taxonomy, False)
        # end if
    # end for
    attachment = wp_prepare_attachment_for_js(id)
    if (not attachment):
        wp_send_json_error()
    # end if
    wp_send_json_success(attachment)
# end def wp_ajax_save_attachment_compat
#// 
#// Ajax handler for saving the attachment order.
#// 
#// @since 3.5.0
#//
def wp_ajax_save_attachment_order(*args_):
    
    if (not (php_isset(lambda : PHP_REQUEST["post_id"]))):
        wp_send_json_error()
    # end if
    post_id = absint(PHP_REQUEST["post_id"])
    if (not post_id):
        wp_send_json_error()
    # end if
    if php_empty(lambda : PHP_REQUEST["attachments"]):
        wp_send_json_error()
    # end if
    check_ajax_referer("update-post_" + post_id, "nonce")
    attachments = PHP_REQUEST["attachments"]
    if (not current_user_can("edit_post", post_id)):
        wp_send_json_error()
    # end if
    for attachment_id,menu_order in attachments:
        if (not current_user_can("edit_post", attachment_id)):
            continue
        # end if
        attachment = get_post(attachment_id)
        if (not attachment):
            continue
        # end if
        if "attachment" != attachment.post_type:
            continue
        # end if
        wp_update_post(Array({"ID": attachment_id, "menu_order": menu_order}))
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
def wp_ajax_send_attachment_to_editor(*args_):
    
    check_ajax_referer("media-send-to-editor", "nonce")
    attachment = wp_unslash(PHP_POST["attachment"])
    id = php_intval(attachment["id"])
    post = get_post(id)
    if (not post):
        wp_send_json_error()
    # end if
    if "attachment" != post.post_type:
        wp_send_json_error()
    # end if
    if current_user_can("edit_post", id):
        #// If this attachment is unattached, attach it. Primarily a back compat thing.
        insert_into_post_id = php_intval(PHP_POST["post_id"])
        if 0 == post.post_parent and insert_into_post_id:
            wp_update_post(Array({"ID": id, "post_parent": insert_into_post_id}))
        # end if
    # end if
    url = "" if php_empty(lambda : attachment["url"]) else attachment["url"]
    rel = php_strpos(url, "attachment_id") or get_attachment_link(id) == url
    remove_filter("media_send_to_editor", "image_media_send_to_editor")
    if "image" == php_substr(post.post_mime_type, 0, 5):
        align = attachment["align"] if (php_isset(lambda : attachment["align"])) else "none"
        size = attachment["image-size"] if (php_isset(lambda : attachment["image-size"])) else "medium"
        alt = attachment["image_alt"] if (php_isset(lambda : attachment["image_alt"])) else ""
        #// No whitespace-only captions.
        caption = attachment["post_excerpt"] if (php_isset(lambda : attachment["post_excerpt"])) else ""
        if "" == php_trim(caption):
            caption = ""
        # end if
        title = ""
        #// We no longer insert title tags into <img> tags, as they are redundant.
        html = get_image_send_to_editor(id, caption, title, align, url, rel, size, alt)
    elif wp_attachment_is("video", post) or wp_attachment_is("audio", post):
        html = stripslashes_deep(PHP_POST["html"])
    else:
        html = attachment["post_title"] if (php_isset(lambda : attachment["post_title"])) else ""
        rel = " rel=\"attachment wp-att-" + id + "\"" if rel else ""
        #// Hard-coded string, $id is already sanitized.
        if (not php_empty(lambda : url)):
            html = "<a href=\"" + esc_url(url) + "\"" + rel + ">" + html + "</a>"
        # end if
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    html = apply_filters("media_send_to_editor", html, id, attachment)
    wp_send_json_success(html)
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
def wp_ajax_send_link_to_editor(*args_):
    
    global post,wp_embed
    php_check_if_defined("post","wp_embed")
    check_ajax_referer("media-send-to-editor", "nonce")
    src = wp_unslash(PHP_POST["src"])
    if (not src):
        wp_send_json_error()
    # end if
    if (not php_strpos(src, "://")):
        src = "http://" + src
    # end if
    src = esc_url_raw(src)
    if (not src):
        wp_send_json_error()
    # end if
    link_text = php_trim(wp_unslash(PHP_POST["link_text"]))
    if (not link_text):
        link_text = wp_basename(src)
    # end if
    post = get_post(PHP_POST["post_id"] if (php_isset(lambda : PHP_POST["post_id"])) else 0)
    #// Ping WordPress for an embed.
    check_embed = wp_embed.run_shortcode("[embed]" + src + "[/embed]")
    #// Fallback that WordPress creates when no oEmbed was found.
    fallback = wp_embed.maybe_make_link(src)
    if check_embed != fallback:
        #// TinyMCE view for [embed] will parse this.
        html = "[embed]" + src + "[/embed]"
    elif link_text:
        html = "<a href=\"" + esc_url(src) + "\">" + link_text + "</a>"
    else:
        html = ""
    # end if
    #// Figure out what filter to run:
    type = "file"
    ext = php_preg_replace("/^.+?\\.([^.]+)$/", "$1", src)
    if ext:
        ext_type = wp_ext2type(ext)
        if "audio" == ext_type or "video" == ext_type:
            type = ext_type
        # end if
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    html = apply_filters(str(type) + str("_send_to_editor_url"), html, src, link_text)
    wp_send_json_success(html)
# end def wp_ajax_send_link_to_editor
#// 
#// Ajax handler for the Heartbeat API.
#// 
#// Runs when the user is logged in.
#// 
#// @since 3.6.0
#//
def wp_ajax_heartbeat(*args_):
    
    if php_empty(lambda : PHP_POST["_nonce"]):
        wp_send_json_error()
    # end if
    response = Array()
    data = Array()
    nonce_state = wp_verify_nonce(PHP_POST["_nonce"], "heartbeat-nonce")
    #// 'screen_id' is the same as $current_screen->id and the JS global 'pagenow'.
    if (not php_empty(lambda : PHP_POST["screen_id"])):
        screen_id = sanitize_key(PHP_POST["screen_id"])
    else:
        screen_id = "front"
    # end if
    if (not php_empty(lambda : PHP_POST["data"])):
        data = wp_unslash(PHP_POST["data"])
    # end if
    if 1 != nonce_state:
        #// 
        #// Filters the nonces to send to the New/Edit Post screen.
        #// 
        #// @since 4.3.0
        #// 
        #// @param array  $response  The Heartbeat response.
        #// @param array  $data      The $_POST data sent.
        #// @param string $screen_id The screen id.
        #//
        response = apply_filters("wp_refresh_nonces", response, data, screen_id)
        if False == nonce_state:
            #// User is logged in but nonces have expired.
            response["nonces_expired"] = True
            wp_send_json(response)
        # end if
    # end if
    if (not php_empty(lambda : data)):
        #// 
        #// Filters the Heartbeat response received.
        #// 
        #// @since 3.6.0
        #// 
        #// @param array  $response  The Heartbeat response.
        #// @param array  $data      The $_POST data sent.
        #// @param string $screen_id The screen id.
        #//
        response = apply_filters("heartbeat_received", response, data, screen_id)
    # end if
    #// 
    #// Filters the Heartbeat response sent.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array  $response  The Heartbeat response.
    #// @param string $screen_id The screen id.
    #//
    response = apply_filters("heartbeat_send", response, screen_id)
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
    do_action("heartbeat_tick", response, screen_id)
    #// Send the current time according to the server.
    response["server_time"] = time()
    wp_send_json(response)
# end def wp_ajax_heartbeat
#// 
#// Ajax handler for getting revision diffs.
#// 
#// @since 3.6.0
#//
def wp_ajax_get_revision_diffs(*args_):
    
    php_include_file(ABSPATH + "wp-admin/includes/revision.php", once=False)
    post = get_post(int(PHP_REQUEST["post_id"]))
    if (not post):
        wp_send_json_error()
    # end if
    if (not current_user_can("edit_post", post.ID)):
        wp_send_json_error()
    # end if
    #// Really just pre-loading the cache here.
    revisions = wp_get_post_revisions(post.ID, Array({"check_enabled": False}))
    if (not revisions):
        wp_send_json_error()
    # end if
    return_ = Array()
    set_time_limit(0)
    for compare_key in PHP_REQUEST["compare"]:
        compare_from, compare_to = php_explode(":", compare_key)
        #// from:to
        return_[-1] = Array({"id": compare_key, "fields": wp_get_revision_ui_diff(post, compare_from, compare_to)})
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
def wp_ajax_save_user_color_scheme(*args_):
    
    global _wp_admin_css_colors
    php_check_if_defined("_wp_admin_css_colors")
    check_ajax_referer("save-color-scheme", "nonce")
    color_scheme = sanitize_key(PHP_POST["color_scheme"])
    if (not (php_isset(lambda : _wp_admin_css_colors[color_scheme]))):
        wp_send_json_error()
    # end if
    previous_color_scheme = get_user_meta(get_current_user_id(), "admin_color", True)
    update_user_meta(get_current_user_id(), "admin_color", color_scheme)
    wp_send_json_success(Array({"previousScheme": "admin-color-" + previous_color_scheme, "currentScheme": "admin-color-" + color_scheme}))
# end def wp_ajax_save_user_color_scheme
#// 
#// Ajax handler for getting themes from themes_api().
#// 
#// @since 3.9.0
#// 
#// @global array $themes_allowedtags
#// @global array $theme_field_defaults
#//
def wp_ajax_query_themes(*args_):
    
    global themes_allowedtags,theme_field_defaults
    php_check_if_defined("themes_allowedtags","theme_field_defaults")
    if (not current_user_can("install_themes")):
        wp_send_json_error()
    # end if
    args = wp_parse_args(wp_unslash(PHP_REQUEST["request"]), Array({"per_page": 20, "fields": php_array_merge(theme_field_defaults, Array({"reviews_url": True}))}))
    if (php_isset(lambda : args["browse"])) and "favorites" == args["browse"] and (not (php_isset(lambda : args["user"]))):
        user = get_user_option("wporg_favorites")
        if user:
            args["user"] = user
        # end if
    # end if
    old_filter = args["browse"] if (php_isset(lambda : args["browse"])) else "search"
    #// This filter is documented in wp-admin/includes/class-wp-theme-install-list-table.php
    args = apply_filters("install_themes_table_api_args_" + old_filter, args)
    api = themes_api("query_themes", args)
    if is_wp_error(api):
        wp_send_json_error()
    # end if
    update_php = network_admin_url("update.php?action=install-theme")
    for theme in api.themes:
        theme.install_url = add_query_arg(Array({"theme": theme.slug, "_wpnonce": wp_create_nonce("install-theme_" + theme.slug)}), update_php)
        if current_user_can("switch_themes"):
            if is_multisite():
                theme.activate_url = add_query_arg(Array({"action": "enable", "_wpnonce": wp_create_nonce("enable-theme_" + theme.slug), "theme": theme.slug}), network_admin_url("themes.php"))
            else:
                theme.activate_url = add_query_arg(Array({"action": "activate", "_wpnonce": wp_create_nonce("switch-theme_" + theme.slug), "stylesheet": theme.slug}), admin_url("themes.php"))
            # end if
        # end if
        if (not is_multisite()) and current_user_can("edit_theme_options") and current_user_can("customize"):
            theme.customize_url = add_query_arg(Array({"return": urlencode(network_admin_url("theme-install.php", "relative"))}), wp_customize_url(theme.slug))
        # end if
        theme.name = wp_kses(theme.name, themes_allowedtags)
        theme.author = wp_kses(theme.author["display_name"], themes_allowedtags)
        theme.version = wp_kses(theme.version, themes_allowedtags)
        theme.description = wp_kses(theme.description, themes_allowedtags)
        theme.stars = wp_star_rating(Array({"rating": theme.rating, "type": "percent", "number": theme.num_ratings, "echo": False}))
        theme.num_ratings = number_format_i18n(theme.num_ratings)
        theme.preview_url = set_url_scheme(theme.preview_url)
    # end for
    wp_send_json_success(api)
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
def wp_ajax_parse_embed(*args_):
    
    global post,wp_embed,content_width
    php_check_if_defined("post","wp_embed","content_width")
    if php_empty(lambda : PHP_POST["shortcode"]):
        wp_send_json_error()
    # end if
    post_id = php_intval(PHP_POST["post_ID"]) if (php_isset(lambda : PHP_POST["post_ID"])) else 0
    if post_id > 0:
        post = get_post(post_id)
        if (not post) or (not current_user_can("edit_post", post.ID)):
            wp_send_json_error()
        # end if
        setup_postdata(post)
    elif (not current_user_can("edit_posts")):
        #// See WP_oEmbed_Controller::get_proxy_item_permissions_check().
        wp_send_json_error()
    # end if
    shortcode = wp_unslash(PHP_POST["shortcode"])
    php_preg_match("/" + get_shortcode_regex() + "/s", shortcode, matches)
    atts = shortcode_parse_atts(matches[3])
    if (not php_empty(lambda : matches[5])):
        url = matches[5]
    elif (not php_empty(lambda : atts["src"])):
        url = atts["src"]
    else:
        url = ""
    # end if
    parsed = False
    wp_embed.return_false_on_fail = True
    if 0 == post_id:
        #// 
        #// Refresh oEmbeds cached outside of posts that are past their TTL.
        #// Posts are excluded because they have separate logic for refreshing
        #// their post meta caches. See WP_Embed::cache_oembed().
        #//
        wp_embed.usecache = False
    # end if
    if is_ssl() and 0 == php_strpos(url, "http://"):
        #// Admin is ssl and the user pasted non-ssl URL.
        #// Check if the provider supports ssl embeds and use that for the preview.
        ssl_shortcode = php_preg_replace("%^(\\[embed[^\\]]*\\])http://%i", "$1https://", shortcode)
        parsed = wp_embed.run_shortcode(ssl_shortcode)
        if (not parsed):
            no_ssl_support = True
        # end if
    # end if
    #// Set $content_width so any embeds fit in the destination iframe.
    if (php_isset(lambda : PHP_POST["maxwidth"])) and php_is_numeric(PHP_POST["maxwidth"]) and PHP_POST["maxwidth"] > 0:
        if (not (php_isset(lambda : content_width))):
            content_width = php_intval(PHP_POST["maxwidth"])
        else:
            content_width = php_min(content_width, php_intval(PHP_POST["maxwidth"]))
        # end if
    # end if
    if url and (not parsed):
        parsed = wp_embed.run_shortcode(shortcode)
    # end if
    if (not parsed):
        wp_send_json_error(Array({"type": "not-embeddable", "message": php_sprintf(__("%s failed to embed."), "<code>" + esc_html(url) + "</code>")}))
    # end if
    if has_shortcode(parsed, "audio") or has_shortcode(parsed, "video"):
        styles = ""
        mce_styles = wpview_media_sandbox_styles()
        for style in mce_styles:
            styles += php_sprintf("<link rel=\"stylesheet\" href=\"%s\"/>", style)
        # end for
        html = do_shortcode(parsed)
        global wp_scripts
        php_check_if_defined("wp_scripts")
        if (not php_empty(lambda : wp_scripts)):
            wp_scripts.done = Array()
        # end if
        ob_start()
        wp_print_scripts(Array("mediaelement-vimeo", "wp-mediaelement"))
        scripts = ob_get_clean()
        parsed = styles + html + scripts
    # end if
    if (not php_empty(lambda : no_ssl_support)) or is_ssl() and php_preg_match("%<(iframe|script|embed) [^>]*src=\"http://%", parsed) or php_preg_match("%<link [^>]*href=\"http://%", parsed):
        #// Admin is ssl and the embed is not. Iframes, scripts, and other "active content" will be blocked.
        wp_send_json_error(Array({"type": "not-ssl", "message": __("This preview is unavailable in the editor.")}))
    # end if
    return_ = Array({"body": parsed, "attr": wp_embed.last_attr})
    if php_strpos(parsed, "class=\"wp-embedded-content"):
        if php_defined("SCRIPT_DEBUG") and SCRIPT_DEBUG:
            script_src = includes_url("js/wp-embed.js")
        else:
            script_src = includes_url("js/wp-embed.min.js")
        # end if
        return_["head"] = "<script src=\"" + script_src + "\"></script>"
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
def wp_ajax_parse_media_shortcode(*args_):
    
    global post,wp_scripts
    php_check_if_defined("post","wp_scripts")
    if php_empty(lambda : PHP_POST["shortcode"]):
        wp_send_json_error()
    # end if
    shortcode = wp_unslash(PHP_POST["shortcode"])
    if (not php_empty(lambda : PHP_POST["post_ID"])):
        post = get_post(int(PHP_POST["post_ID"]))
    # end if
    #// The embed shortcode requires a post.
    if (not post) or (not current_user_can("edit_post", post.ID)):
        if "embed" == shortcode:
            wp_send_json_error()
        # end if
    else:
        setup_postdata(post)
    # end if
    parsed = do_shortcode(shortcode)
    if php_empty(lambda : parsed):
        wp_send_json_error(Array({"type": "no-items", "message": __("No items found.")}))
    # end if
    head = ""
    styles = wpview_media_sandbox_styles()
    for style in styles:
        head += "<link type=\"text/css\" rel=\"stylesheet\" href=\"" + style + "\">"
    # end for
    if (not php_empty(lambda : wp_scripts)):
        wp_scripts.done = Array()
    # end if
    ob_start()
    php_print(parsed)
    if "playlist" == PHP_REQUEST["type"]:
        wp_underscore_playlist_templates()
        wp_print_scripts("wp-playlist")
    else:
        wp_print_scripts(Array("mediaelement-vimeo", "wp-mediaelement"))
    # end if
    wp_send_json_success(Array({"head": head, "body": ob_get_clean()}))
# end def wp_ajax_parse_media_shortcode
#// 
#// Ajax handler for destroying multiple open sessions for a user.
#// 
#// @since 4.1.0
#//
def wp_ajax_destroy_sessions(*args_):
    
    user = get_userdata(int(PHP_POST["user_id"]))
    if user:
        if (not current_user_can("edit_user", user.ID)):
            user = False
        elif (not wp_verify_nonce(PHP_POST["nonce"], "update-user_" + user.ID)):
            user = False
        # end if
    # end if
    if (not user):
        wp_send_json_error(Array({"message": __("Could not log out user sessions. Please try again.")}))
    # end if
    sessions = WP_Session_Tokens.get_instance(user.ID)
    if get_current_user_id() == user.ID:
        sessions.destroy_others(wp_get_session_token())
        message = __("You are now logged out everywhere else.")
    else:
        sessions.destroy_all()
        #// translators: %s: User's display name.
        message = php_sprintf(__("%s has been logged out."), user.display_name)
    # end if
    wp_send_json_success(Array({"message": message}))
# end def wp_ajax_destroy_sessions
#// 
#// Ajax handler for cropping an image.
#// 
#// @since 4.3.0
#//
def wp_ajax_crop_image(*args_):
    
    attachment_id = absint(PHP_POST["id"])
    check_ajax_referer("image_editor-" + attachment_id, "nonce")
    if php_empty(lambda : attachment_id) or (not current_user_can("edit_post", attachment_id)):
        wp_send_json_error()
    # end if
    context = php_str_replace("_", "-", PHP_POST["context"])
    data = php_array_map("absint", PHP_POST["cropDetails"])
    cropped = wp_crop_image(attachment_id, data["x1"], data["y1"], data["width"], data["height"], data["dst_width"], data["dst_height"])
    if (not cropped) or is_wp_error(cropped):
        wp_send_json_error(Array({"message": __("Image could not be processed.")}))
    # end if
    for case in Switch(context):
        if case("site-icon"):
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-icon.php", once=True)
            wp_site_icon = php_new_class("WP_Site_Icon", lambda : WP_Site_Icon())
            #// Skip creating a new attachment if the attachment is a Site Icon.
            if get_post_meta(attachment_id, "_wp_attachment_context", True) == context:
                #// Delete the temporary cropped file, we don't need it.
                wp_delete_file(cropped)
                #// Additional sizes in wp_prepare_attachment_for_js().
                add_filter("image_size_names_choose", Array(wp_site_icon, "additional_sizes"))
                break
            # end if
            #// This filter is documented in wp-admin/includes/class-custom-image-header.php
            cropped = apply_filters("wp_create_file_in_uploads", cropped, attachment_id)
            #// For replication.
            object = wp_site_icon.create_attachment_object(cropped, attachment_id)
            object["ID"] = None
            #// Update the attachment.
            add_filter("intermediate_image_sizes_advanced", Array(wp_site_icon, "additional_sizes"))
            attachment_id = wp_site_icon.insert_attachment(object, cropped)
            remove_filter("intermediate_image_sizes_advanced", Array(wp_site_icon, "additional_sizes"))
            #// Additional sizes in wp_prepare_attachment_for_js().
            add_filter("image_size_names_choose", Array(wp_site_icon, "additional_sizes"))
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
            do_action("wp_ajax_crop_image_pre_save", context, attachment_id, cropped)
            #// This filter is documented in wp-admin/includes/class-custom-image-header.php
            cropped = apply_filters("wp_create_file_in_uploads", cropped, attachment_id)
            #// For replication.
            parent_url = wp_get_attachment_url(attachment_id)
            url = php_str_replace(wp_basename(parent_url), wp_basename(cropped), parent_url)
            size = php_no_error(lambda: getimagesize(cropped))
            image_type = size["mime"] if size else "image/jpeg"
            object = Array({"post_title": wp_basename(cropped), "post_content": url, "post_mime_type": image_type, "guid": url, "context": context})
            attachment_id = wp_insert_attachment(object, cropped)
            metadata = wp_generate_attachment_metadata(attachment_id, cropped)
            #// 
            #// Filters the cropped image attachment metadata.
            #// 
            #// @since 4.3.0
            #// 
            #// @see wp_generate_attachment_metadata()
            #// 
            #// @param array $metadata Attachment metadata.
            #//
            metadata = apply_filters("wp_ajax_cropped_attachment_metadata", metadata)
            wp_update_attachment_metadata(attachment_id, metadata)
            #// 
            #// Filters the attachment ID for a cropped image.
            #// 
            #// @since 4.3.0
            #// 
            #// @param int    $attachment_id The attachment ID of the cropped image.
            #// @param string $context       The Customizer control requesting the cropped image.
            #//
            attachment_id = apply_filters("wp_ajax_cropped_attachment_id", attachment_id, context)
        # end if
    # end for
    wp_send_json_success(wp_prepare_attachment_for_js(attachment_id))
# end def wp_ajax_crop_image
#// 
#// Ajax handler for generating a password.
#// 
#// @since 4.4.0
#//
def wp_ajax_generate_password(*args_):
    
    wp_send_json_success(wp_generate_password(24))
# end def wp_ajax_generate_password
#// 
#// Ajax handler for saving the user's WordPress.org username.
#// 
#// @since 4.4.0
#//
def wp_ajax_save_wporg_username(*args_):
    
    if (not current_user_can("install_themes")) and (not current_user_can("install_plugins")):
        wp_send_json_error()
    # end if
    check_ajax_referer("save_wporg_username_" + get_current_user_id())
    username = wp_unslash(PHP_REQUEST["username"]) if (php_isset(lambda : PHP_REQUEST["username"])) else False
    if (not username):
        wp_send_json_error()
    # end if
    wp_send_json_success(update_user_meta(get_current_user_id(), "wporg_favorites", username))
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
def wp_ajax_install_theme(*args_):
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_theme_specified", "errorMessage": __("No theme specified.")}))
    # end if
    slug = sanitize_key(wp_unslash(PHP_POST["slug"]))
    status = Array({"install": "theme", "slug": slug})
    if (not current_user_can("install_themes")):
        status["errorMessage"] = __("Sorry, you are not allowed to install themes on this site.")
        wp_send_json_error(status)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    php_include_file(ABSPATH + "wp-admin/includes/theme.php", once=False)
    api = themes_api("theme_information", Array({"slug": slug, "fields": Array({"sections": False})}))
    if is_wp_error(api):
        status["errorMessage"] = api.get_error_message()
        wp_send_json_error(status)
    # end if
    skin = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(skin))
    result = upgrader.install(api.download_link)
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status["debug"] = skin.get_upgrade_messages()
    # end if
    if is_wp_error(result):
        status["errorCode"] = result.get_error_code()
        status["errorMessage"] = result.get_error_message()
        wp_send_json_error(status)
    elif is_wp_error(skin.result):
        status["errorCode"] = skin.result.get_error_code()
        status["errorMessage"] = skin.result.get_error_message()
        wp_send_json_error(status)
    elif skin.get_errors().has_errors():
        status["errorMessage"] = skin.get_error_messages()
        wp_send_json_error(status)
    elif php_is_null(result):
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        status["errorCode"] = "unable_to_connect_to_filesystem"
        status["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
            status["errorMessage"] = esc_html(wp_filesystem.errors.get_error_message())
        # end if
        wp_send_json_error(status)
    # end if
    status["themeName"] = wp_get_theme(slug).get("Name")
    if current_user_can("switch_themes"):
        if is_multisite():
            status["activateUrl"] = add_query_arg(Array({"action": "enable", "_wpnonce": wp_create_nonce("enable-theme_" + slug), "theme": slug}), network_admin_url("themes.php"))
        else:
            status["activateUrl"] = add_query_arg(Array({"action": "activate", "_wpnonce": wp_create_nonce("switch-theme_" + slug), "stylesheet": slug}), admin_url("themes.php"))
        # end if
    # end if
    if (not is_multisite()) and current_user_can("edit_theme_options") and current_user_can("customize"):
        status["customizeUrl"] = add_query_arg(Array({"return": urlencode(network_admin_url("theme-install.php", "relative"))}), wp_customize_url(slug))
    # end if
    #// 
    #// See WP_Theme_Install_List_Table::_get_theme_status() if we wanted to check
    #// on post-installation status.
    #//
    wp_send_json_success(status)
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
def wp_ajax_update_theme(*args_):
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_theme_specified", "errorMessage": __("No theme specified.")}))
    # end if
    stylesheet = php_preg_replace("/[^A-z0-9_\\-]/", "", wp_unslash(PHP_POST["slug"]))
    status = Array({"update": "theme", "slug": stylesheet, "oldVersion": "", "newVersion": ""})
    if (not current_user_can("update_themes")):
        status["errorMessage"] = __("Sorry, you are not allowed to update themes for this site.")
        wp_send_json_error(status)
    # end if
    theme = wp_get_theme(stylesheet)
    if theme.exists():
        status["oldVersion"] = theme.get("Version")
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    current = get_site_transient("update_themes")
    if php_empty(lambda : current):
        wp_update_themes()
    # end if
    skin = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader(skin))
    result = upgrader.bulk_upgrade(Array(stylesheet))
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status["debug"] = skin.get_upgrade_messages()
    # end if
    if is_wp_error(skin.result):
        status["errorCode"] = skin.result.get_error_code()
        status["errorMessage"] = skin.result.get_error_message()
        wp_send_json_error(status)
    elif skin.get_errors().has_errors():
        status["errorMessage"] = skin.get_error_messages()
        wp_send_json_error(status)
    elif php_is_array(result) and (not php_empty(lambda : result[stylesheet])):
        #// Theme is already at the latest version.
        if True == result[stylesheet]:
            status["errorMessage"] = upgrader.strings["up_to_date"]
            wp_send_json_error(status)
        # end if
        theme = wp_get_theme(stylesheet)
        if theme.exists():
            status["newVersion"] = theme.get("Version")
        # end if
        wp_send_json_success(status)
    elif False == result:
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        status["errorCode"] = "unable_to_connect_to_filesystem"
        status["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
            status["errorMessage"] = esc_html(wp_filesystem.errors.get_error_message())
        # end if
        wp_send_json_error(status)
    # end if
    #// An unhandled error occurred.
    status["errorMessage"] = __("Update failed.")
    wp_send_json_error(status)
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
def wp_ajax_delete_theme(*args_):
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_theme_specified", "errorMessage": __("No theme specified.")}))
    # end if
    stylesheet = php_preg_replace("/[^A-z0-9_\\-]/", "", wp_unslash(PHP_POST["slug"]))
    status = Array({"delete": "theme", "slug": stylesheet})
    if (not current_user_can("delete_themes")):
        status["errorMessage"] = __("Sorry, you are not allowed to delete themes on this site.")
        wp_send_json_error(status)
    # end if
    if (not wp_get_theme(stylesheet).exists()):
        status["errorMessage"] = __("The requested theme does not exist.")
        wp_send_json_error(status)
    # end if
    #// Check filesystem credentials. `delete_theme()` will bail otherwise.
    url = wp_nonce_url("themes.php?action=delete&stylesheet=" + urlencode(stylesheet), "delete-theme_" + stylesheet)
    ob_start()
    credentials = request_filesystem_credentials(url)
    ob_end_clean()
    if False == credentials or (not WP_Filesystem(credentials)):
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        status["errorCode"] = "unable_to_connect_to_filesystem"
        status["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
            status["errorMessage"] = esc_html(wp_filesystem.errors.get_error_message())
        # end if
        wp_send_json_error(status)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/theme.php", once=False)
    result = delete_theme(stylesheet)
    if is_wp_error(result):
        status["errorMessage"] = result.get_error_message()
        wp_send_json_error(status)
    elif False == result:
        status["errorMessage"] = __("Theme could not be deleted.")
        wp_send_json_error(status)
    # end if
    wp_send_json_success(status)
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
def wp_ajax_install_plugin(*args_):
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_plugin_specified", "errorMessage": __("No plugin specified.")}))
    # end if
    status = Array({"install": "plugin", "slug": sanitize_key(wp_unslash(PHP_POST["slug"]))})
    if (not current_user_can("install_plugins")):
        status["errorMessage"] = __("Sorry, you are not allowed to install plugins on this site.")
        wp_send_json_error(status)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    php_include_file(ABSPATH + "wp-admin/includes/plugin-install.php", once=False)
    api = plugins_api("plugin_information", Array({"slug": sanitize_key(wp_unslash(PHP_POST["slug"])), "fields": Array({"sections": False})}))
    if is_wp_error(api):
        status["errorMessage"] = api.get_error_message()
        wp_send_json_error(status)
    # end if
    status["pluginName"] = api.name
    skin = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(skin))
    result = upgrader.install(api.download_link)
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status["debug"] = skin.get_upgrade_messages()
    # end if
    if is_wp_error(result):
        status["errorCode"] = result.get_error_code()
        status["errorMessage"] = result.get_error_message()
        wp_send_json_error(status)
    elif is_wp_error(skin.result):
        status["errorCode"] = skin.result.get_error_code()
        status["errorMessage"] = skin.result.get_error_message()
        wp_send_json_error(status)
    elif skin.get_errors().has_errors():
        status["errorMessage"] = skin.get_error_messages()
        wp_send_json_error(status)
    elif php_is_null(result):
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        status["errorCode"] = "unable_to_connect_to_filesystem"
        status["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
            status["errorMessage"] = esc_html(wp_filesystem.errors.get_error_message())
        # end if
        wp_send_json_error(status)
    # end if
    install_status = install_plugin_install_status(api)
    pagenow = sanitize_key(PHP_POST["pagenow"]) if (php_isset(lambda : PHP_POST["pagenow"])) else ""
    #// If installation request is coming from import page, do not return network activation link.
    plugins_url = admin_url("plugins.php") if "import" == pagenow else network_admin_url("plugins.php")
    if current_user_can("activate_plugin", install_status["file"]) and is_plugin_inactive(install_status["file"]):
        status["activateUrl"] = add_query_arg(Array({"_wpnonce": wp_create_nonce("activate-plugin_" + install_status["file"]), "action": "activate", "plugin": install_status["file"]}), plugins_url)
    # end if
    if is_multisite() and current_user_can("manage_network_plugins") and "import" != pagenow:
        status["activateUrl"] = add_query_arg(Array({"networkwide": 1}), status["activateUrl"])
    # end if
    wp_send_json_success(status)
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
def wp_ajax_update_plugin(*args_):
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["plugin"]) or php_empty(lambda : PHP_POST["slug"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_plugin_specified", "errorMessage": __("No plugin specified.")}))
    # end if
    plugin = plugin_basename(sanitize_text_field(wp_unslash(PHP_POST["plugin"])))
    status = Array({"update": "plugin", "slug": sanitize_key(wp_unslash(PHP_POST["slug"])), "oldVersion": "", "newVersion": ""})
    if (not current_user_can("update_plugins")) or 0 != validate_file(plugin):
        status["errorMessage"] = __("Sorry, you are not allowed to update plugins for this site.")
        wp_send_json_error(status)
    # end if
    plugin_data = get_plugin_data(WP_PLUGIN_DIR + "/" + plugin)
    status["plugin"] = plugin
    status["pluginName"] = plugin_data["Name"]
    if plugin_data["Version"]:
        #// translators: %s: Plugin version.
        status["oldVersion"] = php_sprintf(__("Version %s"), plugin_data["Version"])
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    wp_update_plugins()
    skin = php_new_class("WP_Ajax_Upgrader_Skin", lambda : WP_Ajax_Upgrader_Skin())
    upgrader = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader(skin))
    result = upgrader.bulk_upgrade(Array(plugin))
    if php_defined("WP_DEBUG") and WP_DEBUG:
        status["debug"] = skin.get_upgrade_messages()
    # end if
    if is_wp_error(skin.result):
        status["errorCode"] = skin.result.get_error_code()
        status["errorMessage"] = skin.result.get_error_message()
        wp_send_json_error(status)
    elif skin.get_errors().has_errors():
        status["errorMessage"] = skin.get_error_messages()
        wp_send_json_error(status)
    elif php_is_array(result) and (not php_empty(lambda : result[plugin])):
        plugin_update_data = current(result)
        #// 
        #// If the `update_plugins` site transient is empty (e.g. when you update
        #// two plugins in quick succession before the transient repopulates),
        #// this may be the return.
        #// 
        #// Preferably something can be done to ensure `update_plugins` isn't empty.
        #// For now, surface some sort of error here.
        #//
        if True == plugin_update_data:
            status["errorMessage"] = __("Plugin update failed.")
            wp_send_json_error(status)
        # end if
        plugin_data = get_plugins("/" + result[plugin]["destination_name"])
        plugin_data = reset(plugin_data)
        if plugin_data["Version"]:
            #// translators: %s: Plugin version.
            status["newVersion"] = php_sprintf(__("Version %s"), plugin_data["Version"])
        # end if
        wp_send_json_success(status)
    elif False == result:
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        status["errorCode"] = "unable_to_connect_to_filesystem"
        status["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
            status["errorMessage"] = esc_html(wp_filesystem.errors.get_error_message())
        # end if
        wp_send_json_error(status)
    # end if
    #// An unhandled error occurred.
    status["errorMessage"] = __("Plugin update failed.")
    wp_send_json_error(status)
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
def wp_ajax_delete_plugin(*args_):
    
    check_ajax_referer("updates")
    if php_empty(lambda : PHP_POST["slug"]) or php_empty(lambda : PHP_POST["plugin"]):
        wp_send_json_error(Array({"slug": "", "errorCode": "no_plugin_specified", "errorMessage": __("No plugin specified.")}))
    # end if
    plugin = plugin_basename(sanitize_text_field(wp_unslash(PHP_POST["plugin"])))
    status = Array({"delete": "plugin", "slug": sanitize_key(wp_unslash(PHP_POST["slug"]))})
    if (not current_user_can("delete_plugins")) or 0 != validate_file(plugin):
        status["errorMessage"] = __("Sorry, you are not allowed to delete plugins for this site.")
        wp_send_json_error(status)
    # end if
    plugin_data = get_plugin_data(WP_PLUGIN_DIR + "/" + plugin)
    status["plugin"] = plugin
    status["pluginName"] = plugin_data["Name"]
    if is_plugin_active(plugin):
        status["errorMessage"] = __("You cannot delete a plugin while it is active on the main site.")
        wp_send_json_error(status)
    # end if
    #// Check filesystem credentials. `delete_plugins()` will bail otherwise.
    url = wp_nonce_url("plugins.php?action=delete-selected&verify-delete=1&checked[]=" + plugin, "bulk-plugins")
    ob_start()
    credentials = request_filesystem_credentials(url)
    ob_end_clean()
    if False == credentials or (not WP_Filesystem(credentials)):
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        status["errorCode"] = "unable_to_connect_to_filesystem"
        status["errorMessage"] = __("Unable to connect to the filesystem. Please confirm your credentials.")
        #// Pass through the error from WP_Filesystem if one was raised.
        if type(wp_filesystem).__name__ == "WP_Filesystem_Base" and is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
            status["errorMessage"] = esc_html(wp_filesystem.errors.get_error_message())
        # end if
        wp_send_json_error(status)
    # end if
    result = delete_plugins(Array(plugin))
    if is_wp_error(result):
        status["errorMessage"] = result.get_error_message()
        wp_send_json_error(status)
    elif False == result:
        status["errorMessage"] = __("Plugin could not be deleted.")
        wp_send_json_error(status)
    # end if
    wp_send_json_success(status)
# end def wp_ajax_delete_plugin
#// 
#// Ajax handler for searching plugins.
#// 
#// @since 4.6.0
#// 
#// @global string $s Search term.
#//
def wp_ajax_search_plugins(*args_):
    global PHP_SERVER, PHP_GLOBALS
    check_ajax_referer("updates")
    pagenow = sanitize_key(PHP_POST["pagenow"]) if (php_isset(lambda : PHP_POST["pagenow"])) else ""
    if "plugins-network" == pagenow or "plugins" == pagenow:
        set_current_screen(pagenow)
    # end if
    #// @var WP_Plugins_List_Table $wp_list_table
    wp_list_table = _get_list_table("WP_Plugins_List_Table", Array({"screen": get_current_screen()}))
    status = Array()
    if (not wp_list_table.ajax_user_can()):
        status["errorMessage"] = __("Sorry, you are not allowed to manage plugins for this site.")
        wp_send_json_error(status)
    # end if
    #// Set the correct requester, so pagination works.
    PHP_SERVER["REQUEST_URI"] = add_query_arg(php_array_diff_key(PHP_POST, Array({"_ajax_nonce": None, "action": None})), network_admin_url("plugins.php", "relative"))
    PHP_GLOBALS["s"] = wp_unslash(PHP_POST["s"])
    wp_list_table.prepare_items()
    ob_start()
    wp_list_table.display()
    status["count"] = php_count(wp_list_table.items)
    status["items"] = ob_get_clean()
    wp_send_json_success(status)
# end def wp_ajax_search_plugins
#// 
#// Ajax handler for searching plugins to install.
#// 
#// @since 4.6.0
#//
def wp_ajax_search_install_plugins(*args_):
    global PHP_SERVER
    check_ajax_referer("updates")
    pagenow = sanitize_key(PHP_POST["pagenow"]) if (php_isset(lambda : PHP_POST["pagenow"])) else ""
    if "plugin-install-network" == pagenow or "plugin-install" == pagenow:
        set_current_screen(pagenow)
    # end if
    #// @var WP_Plugin_Install_List_Table $wp_list_table
    wp_list_table = _get_list_table("WP_Plugin_Install_List_Table", Array({"screen": get_current_screen()}))
    status = Array()
    if (not wp_list_table.ajax_user_can()):
        status["errorMessage"] = __("Sorry, you are not allowed to manage plugins for this site.")
        wp_send_json_error(status)
    # end if
    #// Set the correct requester, so pagination works.
    PHP_SERVER["REQUEST_URI"] = add_query_arg(php_array_diff_key(PHP_POST, Array({"_ajax_nonce": None, "action": None})), network_admin_url("plugin-install.php", "relative"))
    wp_list_table.prepare_items()
    ob_start()
    wp_list_table.display()
    status["count"] = int(wp_list_table.get_pagination_arg("total_items"))
    status["items"] = ob_get_clean()
    wp_send_json_success(status)
# end def wp_ajax_search_install_plugins
#// 
#// Ajax handler for editing a theme or plugin file.
#// 
#// @since 4.9.0
#// @see wp_edit_theme_plugin_file()
#//
def wp_ajax_edit_theme_plugin_file(*args_):
    
    r = wp_edit_theme_plugin_file(wp_unslash(PHP_POST))
    #// Validation of args is done in wp_edit_theme_plugin_file().
    if is_wp_error(r):
        wp_send_json_error(php_array_merge(Array({"code": r.get_error_code(), "message": r.get_error_message()}), r.get_error_data()))
    else:
        wp_send_json_success(Array({"message": __("File edited successfully.")}))
    # end if
# end def wp_ajax_edit_theme_plugin_file
#// 
#// Ajax handler for exporting a user's personal data.
#// 
#// @since 4.9.6
#//
def wp_ajax_wp_privacy_export_personal_data(*args_):
    
    if php_empty(lambda : PHP_POST["id"]):
        wp_send_json_error(__("Missing request ID."))
    # end if
    request_id = int(PHP_POST["id"])
    if request_id < 1:
        wp_send_json_error(__("Invalid request ID."))
    # end if
    if (not current_user_can("export_others_personal_data")):
        wp_send_json_error(__("Sorry, you are not allowed to perform this action."))
    # end if
    check_ajax_referer("wp-privacy-export-personal-data-" + request_id, "security")
    #// Get the request.
    request = wp_get_user_request(request_id)
    if (not request) or "export_personal_data" != request.action_name:
        wp_send_json_error(__("Invalid request type."))
    # end if
    email_address = request.email
    if (not is_email(email_address)):
        wp_send_json_error(__("A valid email address must be given."))
    # end if
    if (not (php_isset(lambda : PHP_POST["exporter"]))):
        wp_send_json_error(__("Missing exporter index."))
    # end if
    exporter_index = int(PHP_POST["exporter"])
    if (not (php_isset(lambda : PHP_POST["page"]))):
        wp_send_json_error(__("Missing page index."))
    # end if
    page = int(PHP_POST["page"])
    send_as_email = "true" == PHP_POST["sendAsEmail"] if (php_isset(lambda : PHP_POST["sendAsEmail"])) else False
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
    exporters = apply_filters("wp_privacy_personal_data_exporters", Array())
    if (not php_is_array(exporters)):
        wp_send_json_error(__("An exporter has improperly used the registration filter."))
    # end if
    #// Do we have any registered exporters?
    if 0 < php_count(exporters):
        if exporter_index < 1:
            wp_send_json_error(__("Exporter index cannot be negative."))
        # end if
        if exporter_index > php_count(exporters):
            wp_send_json_error(__("Exporter index is out of range."))
        # end if
        if page < 1:
            wp_send_json_error(__("Page index cannot be less than one."))
        # end if
        exporter_keys = php_array_keys(exporters)
        exporter_key = exporter_keys[exporter_index - 1]
        exporter = exporters[exporter_key]
        if (not php_is_array(exporter)):
            wp_send_json_error(php_sprintf(__("Expected an array describing the exporter at index %s."), exporter_key))
        # end if
        if (not php_array_key_exists("exporter_friendly_name", exporter)):
            wp_send_json_error(php_sprintf(__("Exporter array at index %s does not include a friendly name."), exporter_key))
        # end if
        exporter_friendly_name = exporter["exporter_friendly_name"]
        if (not php_array_key_exists("callback", exporter)):
            wp_send_json_error(php_sprintf(__("Exporter does not include a callback: %s."), esc_html(exporter_friendly_name)))
        # end if
        if (not php_is_callable(exporter["callback"])):
            wp_send_json_error(php_sprintf(__("Exporter callback is not a valid callback: %s."), esc_html(exporter_friendly_name)))
        # end if
        callback = exporter["callback"]
        response = php_call_user_func(callback, email_address, page)
        if is_wp_error(response):
            wp_send_json_error(response)
        # end if
        if (not php_is_array(response)):
            wp_send_json_error(php_sprintf(__("Expected response as an array from exporter: %s."), esc_html(exporter_friendly_name)))
        # end if
        if (not php_array_key_exists("data", response)):
            wp_send_json_error(php_sprintf(__("Expected data in response array from exporter: %s."), esc_html(exporter_friendly_name)))
        # end if
        if (not php_is_array(response["data"])):
            wp_send_json_error(php_sprintf(__("Expected data array in response array from exporter: %s."), esc_html(exporter_friendly_name)))
        # end if
        if (not php_array_key_exists("done", response)):
            wp_send_json_error(php_sprintf(__("Expected done (boolean) in response array from exporter: %s."), esc_html(exporter_friendly_name)))
        # end if
    else:
        #// No exporters, so we're done.
        exporter_key = ""
        response = Array({"data": Array(), "done": True})
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
    response = apply_filters("wp_privacy_personal_data_export_page", response, exporter_index, email_address, page, request_id, send_as_email, exporter_key)
    if is_wp_error(response):
        wp_send_json_error(response)
    # end if
    wp_send_json_success(response)
# end def wp_ajax_wp_privacy_export_personal_data
#// 
#// Ajax handler for erasing personal data.
#// 
#// @since 4.9.6
#//
def wp_ajax_wp_privacy_erase_personal_data(*args_):
    
    if php_empty(lambda : PHP_POST["id"]):
        wp_send_json_error(__("Missing request ID."))
    # end if
    request_id = int(PHP_POST["id"])
    if request_id < 1:
        wp_send_json_error(__("Invalid request ID."))
    # end if
    #// Both capabilities are required to avoid confusion, see `_wp_personal_data_removal_page()`.
    if (not current_user_can("erase_others_personal_data")) or (not current_user_can("delete_users")):
        wp_send_json_error(__("Sorry, you are not allowed to perform this action."))
    # end if
    check_ajax_referer("wp-privacy-erase-personal-data-" + request_id, "security")
    #// Get the request.
    request = wp_get_user_request(request_id)
    if (not request) or "remove_personal_data" != request.action_name:
        wp_send_json_error(__("Invalid request type."))
    # end if
    email_address = request.email
    if (not is_email(email_address)):
        wp_send_json_error(__("Invalid email address in request."))
    # end if
    if (not (php_isset(lambda : PHP_POST["eraser"]))):
        wp_send_json_error(__("Missing eraser index."))
    # end if
    eraser_index = int(PHP_POST["eraser"])
    if (not (php_isset(lambda : PHP_POST["page"]))):
        wp_send_json_error(__("Missing page index."))
    # end if
    page = int(PHP_POST["page"])
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
    erasers = apply_filters("wp_privacy_personal_data_erasers", Array())
    #// Do we have any registered erasers?
    if 0 < php_count(erasers):
        if eraser_index < 1:
            wp_send_json_error(__("Eraser index cannot be less than one."))
        # end if
        if eraser_index > php_count(erasers):
            wp_send_json_error(__("Eraser index is out of range."))
        # end if
        if page < 1:
            wp_send_json_error(__("Page index cannot be less than one."))
        # end if
        eraser_keys = php_array_keys(erasers)
        eraser_key = eraser_keys[eraser_index - 1]
        eraser = erasers[eraser_key]
        if (not php_is_array(eraser)):
            #// translators: %d: Eraser array index.
            wp_send_json_error(php_sprintf(__("Expected an array describing the eraser at index %d."), eraser_index))
        # end if
        if (not php_array_key_exists("eraser_friendly_name", eraser)):
            #// translators: %d: Eraser array index.
            wp_send_json_error(php_sprintf(__("Eraser array at index %d does not include a friendly name."), eraser_index))
        # end if
        eraser_friendly_name = eraser["eraser_friendly_name"]
        if (not php_array_key_exists("callback", eraser)):
            wp_send_json_error(php_sprintf(__("Eraser does not include a callback: %s."), esc_html(eraser_friendly_name)))
        # end if
        if (not php_is_callable(eraser["callback"])):
            wp_send_json_error(php_sprintf(__("Eraser callback is not valid: %s."), esc_html(eraser_friendly_name)))
        # end if
        callback = eraser["callback"]
        response = php_call_user_func(callback, email_address, page)
        if is_wp_error(response):
            wp_send_json_error(response)
        # end if
        if (not php_is_array(response)):
            wp_send_json_error(php_sprintf(__("Did not receive array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name), eraser_index))
        # end if
        if (not php_array_key_exists("items_removed", response)):
            wp_send_json_error(php_sprintf(__("Expected items_removed key in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name), eraser_index))
        # end if
        if (not php_array_key_exists("items_retained", response)):
            wp_send_json_error(php_sprintf(__("Expected items_retained key in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name), eraser_index))
        # end if
        if (not php_array_key_exists("messages", response)):
            wp_send_json_error(php_sprintf(__("Expected messages key in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name), eraser_index))
        # end if
        if (not php_is_array(response["messages"])):
            wp_send_json_error(php_sprintf(__("Expected messages key to reference an array in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name), eraser_index))
        # end if
        if (not php_array_key_exists("done", response)):
            wp_send_json_error(php_sprintf(__("Expected done flag in response array from %1$s eraser (index %2$d)."), esc_html(eraser_friendly_name), eraser_index))
        # end if
    else:
        #// No erasers, so we're done.
        eraser_key = ""
        response = Array({"items_removed": False, "items_retained": False, "messages": Array(), "done": True})
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
    response = apply_filters("wp_privacy_personal_data_erasure_page", response, eraser_index, email_address, page, request_id, eraser_key)
    if is_wp_error(response):
        wp_send_json_error(response)
    # end if
    wp_send_json_success(response)
# end def wp_ajax_wp_privacy_erase_personal_data
#// 
#// Ajax handler for site health checks on server communication.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_dotorg_communication(*args_):
    
    check_ajax_referer("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health = WP_Site_Health.get_instance()
    wp_send_json_success(site_health.get_test_dotorg_communication())
# end def wp_ajax_health_check_dotorg_communication
#// 
#// Ajax handler for site health checks on debug mode.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_is_in_debug_mode(*args_):
    
    wp_verify_nonce("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health = WP_Site_Health.get_instance()
    wp_send_json_success(site_health.get_test_is_in_debug_mode())
# end def wp_ajax_health_check_is_in_debug_mode
#// 
#// Ajax handler for site health checks on background updates.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_background_updates(*args_):
    
    check_ajax_referer("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health = WP_Site_Health.get_instance()
    wp_send_json_success(site_health.get_test_background_updates())
# end def wp_ajax_health_check_background_updates
#// 
#// Ajax handler for site health checks on loopback requests.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_loopback_requests(*args_):
    
    check_ajax_referer("health-check-site-status")
    if (not current_user_can("view_site_health_checks")):
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Site_Health")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
    # end if
    site_health = WP_Site_Health.get_instance()
    wp_send_json_success(site_health.get_test_loopback_requests())
# end def wp_ajax_health_check_loopback_requests
#// 
#// Ajax handler for site health check to update the result status.
#// 
#// @since 5.2.0
#//
def wp_ajax_health_check_site_status_result(*args_):
    
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
def wp_ajax_health_check_get_sizes(*args_):
    
    check_ajax_referer("health-check-site-status-result")
    if (not current_user_can("view_site_health_checks")) or is_multisite():
        wp_send_json_error()
    # end if
    if (not php_class_exists("WP_Debug_Data")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-debug-data.php", once=True)
    # end if
    sizes_data = WP_Debug_Data.get_sizes()
    all_sizes = Array({"raw": 0})
    for name,value in sizes_data:
        name = sanitize_text_field(name)
        data = Array()
        if (php_isset(lambda : value["size"])):
            if php_is_string(value["size"]):
                data["size"] = sanitize_text_field(value["size"])
            else:
                data["size"] = int(value["size"])
            # end if
        # end if
        if (php_isset(lambda : value["debug"])):
            if php_is_string(value["debug"]):
                data["debug"] = sanitize_text_field(value["debug"])
            else:
                data["debug"] = int(value["debug"])
            # end if
        # end if
        if (not php_empty(lambda : value["raw"])):
            data["raw"] = int(value["raw"])
        # end if
        all_sizes[name] = data
    # end for
    if (php_isset(lambda : all_sizes["total_size"]["debug"])) and "not available" == all_sizes["total_size"]["debug"]:
        wp_send_json_error(all_sizes)
    # end if
    wp_send_json_success(all_sizes)
# end def wp_ajax_health_check_get_sizes
#// 
#// Ajax handler to renew the REST API nonce.
#// 
#// @since 5.3.0
#//
def wp_ajax_rest_nonce(*args_):
    
    php_print(wp_create_nonce("wp_rest"))
    php_exit()
# end def wp_ajax_rest_nonce
