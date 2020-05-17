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
#// WordPress Administration Revisions API
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.6.0
#// 
#// 
#// Get the revision UI diff.
#// 
#// @since 3.6.0
#// 
#// @param WP_Post|int $post         The post object or post ID.
#// @param int         $compare_from The revision ID to compare from.
#// @param int         $compare_to   The revision ID to come to.
#// 
#// @return array|bool Associative array of a post's revisioned fields and their diffs.
#// Or, false on failure.
#//
def wp_get_revision_ui_diff(post_=None, compare_from_=None, compare_to_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    if compare_from_:
        compare_from_ = get_post(compare_from_)
        if (not compare_from_):
            return False
        # end if
    else:
        #// If we're dealing with the first revision...
        compare_from_ = False
    # end if
    compare_to_ = get_post(compare_to_)
    if (not compare_to_):
        return False
    # end if
    #// If comparing revisions, make sure we're dealing with the right post parent.
    #// The parent post may be a 'revision' when revisions are disabled and we're looking at autosaves.
    if compare_from_ and compare_from_.post_parent != post_.ID and compare_from_.ID != post_.ID:
        return False
    # end if
    if compare_to_.post_parent != post_.ID and compare_to_.ID != post_.ID:
        return False
    # end if
    if compare_from_ and strtotime(compare_from_.post_date_gmt) > strtotime(compare_to_.post_date_gmt):
        temp_ = compare_from_
        compare_from_ = compare_to_
        compare_to_ = temp_
    # end if
    #// Add default title if title field is empty.
    if compare_from_ and php_empty(lambda : compare_from_.post_title):
        compare_from_.post_title = __("(no title)")
    # end if
    if php_empty(lambda : compare_to_.post_title):
        compare_to_.post_title = __("(no title)")
    # end if
    return_ = Array()
    for field_,name_ in _wp_post_revision_fields(post_):
        #// 
        #// Contextually filter a post revision field.
        #// 
        #// The dynamic portion of the hook name, `$field`, corresponds to each of the post
        #// fields of the revision object being iterated over in a foreach statement.
        #// 
        #// @since 3.6.0
        #// 
        #// @param string  $revision_field The current revision field to compare to or from.
        #// @param string  $field          The current revision field.
        #// @param WP_Post $compare_from   The revision post object to compare to or from.
        #// @param string  $context        The context of whether the current revision is the old
        #// or the new one. Values are 'to' or 'from'.
        #//
        content_from_ = apply_filters(str("_wp_post_revision_field_") + str(field_), compare_from_.field_, field_, compare_from_, "from") if compare_from_ else ""
        #// This filter is documented in wp-admin/includes/revision.php
        content_to_ = apply_filters(str("_wp_post_revision_field_") + str(field_), compare_to_.field_, field_, compare_to_, "to")
        args_ = Array({"show_split_view": True})
        #// 
        #// Filters revisions text diff options.
        #// 
        #// Filters the options passed to wp_text_diff() when viewing a post revision.
        #// 
        #// @since 4.1.0
        #// 
        #// @param array   $args {
        #// Associative array of options to pass to wp_text_diff().
        #// 
        #// @type bool $show_split_view True for split view (two columns), false for
        #// un-split view (single column). Default true.
        #// }
        #// @param string  $field        The current revision field.
        #// @param WP_Post $compare_from The revision post to compare from.
        #// @param WP_Post $compare_to   The revision post to compare to.
        #//
        args_ = apply_filters("revision_text_diff_options", args_, field_, compare_from_, compare_to_)
        diff_ = wp_text_diff(content_from_, content_to_, args_)
        if (not diff_) and "post_title" == field_:
            #// It's a better user experience to still show the Title, even if it didn't change.
            #// No, you didn't see this.
            diff_ = "<table class=\"diff\"><colgroup><col class=\"content diffsplit left\"><col class=\"content diffsplit middle\"><col class=\"content diffsplit right\"></colgroup><tbody><tr>"
            #// In split screen mode, show the title before/after side by side.
            if True == args_["show_split_view"]:
                diff_ += "<td>" + esc_html(compare_from_.post_title) + "</td><td></td><td>" + esc_html(compare_to_.post_title) + "</td>"
            else:
                diff_ += "<td>" + esc_html(compare_from_.post_title) + "</td>"
                #// In single column mode, only show the title once if unchanged.
                if compare_from_.post_title != compare_to_.post_title:
                    diff_ += "</tr><tr><td>" + esc_html(compare_to_.post_title) + "</td>"
                # end if
            # end if
            diff_ += "</tr></tbody>"
            diff_ += "</table>"
        # end if
        if diff_:
            return_[-1] = Array({"id": field_, "name": name_, "diff": diff_})
        # end if
    # end for
    #// 
    #// Filters the fields displayed in the post revision diff UI.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array[] $return       Array of revision UI fields. Each item is an array of id, name, and diff.
    #// @param WP_Post $compare_from The revision post to compare from.
    #// @param WP_Post $compare_to   The revision post to compare to.
    #//
    return apply_filters("wp_get_revision_ui_diff", return_, compare_from_, compare_to_)
# end def wp_get_revision_ui_diff
#// 
#// Prepare revisions for JavaScript.
#// 
#// @since 3.6.0
#// 
#// @param WP_Post|int $post                 The post object or post ID.
#// @param int         $selected_revision_id The selected revision ID.
#// @param int         $from                 Optional. The revision ID to compare from.
#// 
#// @return array An associative array of revision data and related settings.
#//
def wp_prepare_revisions_for_js(post_=None, selected_revision_id_=None, from_=None, *_args_):
    
    
    post_ = get_post(post_)
    authors_ = Array()
    now_gmt_ = time()
    revisions_ = wp_get_post_revisions(post_.ID, Array({"order": "ASC", "check_enabled": False}))
    #// If revisions are disabled, we only want autosaves and the current post.
    if (not wp_revisions_enabled(post_)):
        for revision_id_,revision_ in revisions_:
            if (not wp_is_post_autosave(revision_)):
                revisions_[revision_id_] = None
            # end if
        # end for
        revisions_ = Array({post_.ID: post_}) + revisions_
    # end if
    show_avatars_ = get_option("show_avatars")
    cache_users(wp_list_pluck(revisions_, "post_author"))
    can_restore_ = current_user_can("edit_post", post_.ID)
    current_id_ = False
    for revision_ in revisions_:
        modified_ = strtotime(revision_.post_modified)
        modified_gmt_ = strtotime(revision_.post_modified_gmt + " +0000")
        if can_restore_:
            restore_link_ = php_str_replace("&amp;", "&", wp_nonce_url(add_query_arg(Array({"revision": revision_.ID, "action": "restore"}), admin_url("revision.php")), str("restore-post_") + str(revision_.ID)))
        # end if
        if (not (php_isset(lambda : authors_[revision_.post_author]))):
            authors_[revision_.post_author] = Array({"id": php_int(revision_.post_author), "avatar": get_avatar(revision_.post_author, 32) if show_avatars_ else "", "name": get_the_author_meta("display_name", revision_.post_author)})
        # end if
        autosave_ = php_bool(wp_is_post_autosave(revision_))
        current_ = (not autosave_) and revision_.post_modified_gmt == post_.post_modified_gmt
        if current_ and (not php_empty(lambda : current_id_)):
            #// If multiple revisions have the same post_modified_gmt, highest ID is current.
            if current_id_ < revision_.ID:
                revisions_[current_id_]["current"] = False
                current_id_ = revision_.ID
            else:
                current_ = False
            # end if
        elif current_:
            current_id_ = revision_.ID
        # end if
        revisions_data_ = Array({"id": revision_.ID, "title": get_the_title(post_.ID), "author": authors_[revision_.post_author], "date": date_i18n(__("M j, Y @ H:i"), modified_), "dateShort": date_i18n(_x("j M @ H:i", "revision date short format"), modified_), "timeAgo": php_sprintf(__("%s ago"), human_time_diff(modified_gmt_, now_gmt_)), "autosave": autosave_, "current": current_, "restoreUrl": restore_link_ if can_restore_ else False})
        #// 
        #// Filters the array of revisions used on the revisions screen.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array   $revisions_data {
        #// The bootstrapped data for the revisions screen.
        #// 
        #// @type int        $id         Revision ID.
        #// @type string     $title      Title for the revision's parent WP_Post object.
        #// @type int        $author     Revision post author ID.
        #// @type string     $date       Date the revision was modified.
        #// @type string     $dateShort  Short-form version of the date the revision was modified.
        #// @type string     $timeAgo    GMT-aware amount of time ago the revision was modified.
        #// @type bool       $autosave   Whether the revision is an autosave.
        #// @type bool       $current    Whether the revision is both not an autosave and the post
        #// modified date matches the revision modified date (GMT-aware).
        #// @type bool|false $restoreUrl URL if the revision can be restored, false otherwise.
        #// }
        #// @param WP_Post $revision       The revision's WP_Post object.
        #// @param WP_Post $post           The revision's parent WP_Post object.
        #//
        revisions_[revision_.ID] = apply_filters("wp_prepare_revision_for_js", revisions_data_, revision_, post_)
    # end for
    #// 
    #// If we only have one revision, the initial revision is missing; This happens
    #// when we have an autsosave and the user has clicked 'View the Autosave'
    #//
    if 1 == sizeof(revisions_):
        revisions_[post_.ID] = Array({"id": post_.ID, "title": get_the_title(post_.ID), "author": authors_[post_.post_author], "date": date_i18n(__("M j, Y @ H:i"), strtotime(post_.post_modified)), "dateShort": date_i18n(_x("j M @ H:i", "revision date short format"), strtotime(post_.post_modified)), "timeAgo": php_sprintf(__("%s ago"), human_time_diff(strtotime(post_.post_modified_gmt), now_gmt_)), "autosave": False, "current": True, "restoreUrl": False})
        current_id_ = post_.ID
    # end if
    #// 
    #// If a post has been saved since the last revision (no revisioned fields
    #// were changed), we may not have a "current" revision. Mark the latest
    #// revision as "current".
    #//
    if php_empty(lambda : current_id_):
        if revisions_[revision_.ID]["autosave"]:
            revision_ = php_end(revisions_)
            while True:
                
                if not (revision_["autosave"]):
                    break
                # end if
                revision_ = php_prev(revisions_)
            # end while
            current_id_ = revision_["id"]
        else:
            current_id_ = revision_.ID
        # end if
        revisions_[current_id_]["current"] = True
    # end if
    #// Now, grab the initial diff.
    compare_two_mode_ = php_is_numeric(from_)
    if (not compare_two_mode_):
        found_ = php_array_search(selected_revision_id_, php_array_keys(revisions_))
        if found_:
            from_ = php_array_keys(php_array_slice(revisions_, found_ - 1, 1, True))
            from_ = reset(from_)
        else:
            from_ = 0
        # end if
    # end if
    from_ = absint(from_)
    diffs_ = Array(Array({"id": from_ + ":" + selected_revision_id_, "fields": wp_get_revision_ui_diff(post_.ID, from_, selected_revision_id_)}))
    return Array({"postId": post_.ID, "nonce": wp_create_nonce("revisions-ajax-nonce"), "revisionData": php_array_values(revisions_), "to": selected_revision_id_, "from": from_, "diffData": diffs_, "baseUrl": php_parse_url(admin_url("revision.php"), PHP_URL_PATH), "compareTwoMode": absint(compare_two_mode_), "revisionIds": php_array_keys(revisions_)})
# end def wp_prepare_revisions_for_js
#// 
#// Print JavaScript templates required for the revisions experience.
#// 
#// @since 4.1.0
#// 
#// @global WP_Post $post Global post object.
#//
def wp_print_revision_templates(*_args_):
    
    
    global post_
    php_check_if_defined("post_")
    php_print("""<script id=\"tmpl-revisions-frame\" type=\"text/html\">
    <div class=\"revisions-control-frame\"></div>
    <div class=\"revisions-diff-frame\"></div>
    </script>
    <script id=\"tmpl-revisions-buttons\" type=\"text/html\">
    <div class=\"revisions-previous\">
    <input class=\"button\" type=\"button\" value=\"""")
    php_print(esc_attr_x("Previous", "Button label for a previous revision"))
    php_print("""\" />
    </div>
    <div class=\"revisions-next\">
    <input class=\"button\" type=\"button\" value=\"""")
    php_print(esc_attr_x("Next", "Button label for a next revision"))
    php_print("""\" />
    </div>
    </script>
    <script id=\"tmpl-revisions-checkbox\" type=\"text/html\">
    <div class=\"revision-toggle-compare-mode\">
    <label>
    <input type=\"checkbox\" class=\"compare-two-revisions\"
    <#
if ( 'undefined' !== typeof data && data.model.attributes.compareTwoMode ) {
    #> checked=\"checked\"<#
    }
    #>
    />
    """)
    esc_html_e("Compare any two revisions")
    php_print("""           </label>
    </div>
    </script>
    <script id=\"tmpl-revisions-meta\" type=\"text/html\">
    <# if ( ! _.isUndefined( data.attributes ) ) { #>
    <div class=\"diff-title\">
    <# if ( 'from' === data.type ) { #>
    <strong>""")
    _ex("From:", "Followed by post revision info")
    php_print("</strong>\n              <# } else if ( 'to' === data.type ) { #>\n                  <strong>")
    _ex("To:", "Followed by post revision info")
    php_print("""</strong>
    <# } #>
    <div class=\"author-card<# if ( data.attributes.autosave ) { #> autosave<# } #>\">
    {{{ data.attributes.author.avatar }}}
    <div class=\"author-info\">
    <# if ( data.attributes.autosave ) { #>
    <span class=\"byline\">
    """)
    printf(__("Autosave by %s"), "<span class=\"author-name\">{{ data.attributes.author.name }}</span>")
    php_print("""                           </span>
    <# } else if ( data.attributes.current ) { #>
    <span class=\"byline\">
    """)
    printf(__("Current Revision by %s"), "<span class=\"author-name\">{{ data.attributes.author.name }}</span>")
    php_print("""                           </span>
    <# } else { #>
    <span class=\"byline\">
    """)
    printf(__("Revision by %s"), "<span class=\"author-name\">{{ data.attributes.author.name }}</span>")
    php_print("""                           </span>
    <# } #>
    <span class=\"time-ago\">{{ data.attributes.timeAgo }}</span>
    <span class=\"date\">({{ data.attributes.dateShort }})</span>
    </div>
    <# if ( 'to' === data.type && data.attributes.restoreUrl ) { #>
    <input  """)
    if wp_check_post_lock(post_.ID):
        php_print("                     disabled=\"disabled\"\n                 ")
    else:
        php_print("""                       <# if ( data.attributes.current ) { #>
        disabled=\"disabled\"
        <# } #>
        """)
    # end if
    php_print("                 <# if ( data.attributes.autosave ) { #>\n                       type=\"button\" class=\"restore-revision button button-primary\" value=\"")
    esc_attr_e("Restore This Autosave")
    php_print("\" />\n                  <# } else { #>\n                        type=\"button\" class=\"restore-revision button button-primary\" value=\"")
    esc_attr_e("Restore This Revision")
    php_print("""\" />
    <# } #>
    <# } #>
    </div>
    <# if ( 'tooltip' === data.type ) { #>
    <div class=\"revisions-tooltip-arrow\"><span></span></div>
    <# } #>
    <# } #>
    </script>
    <script id=\"tmpl-revisions-diff\" type=\"text/html\">
    <div class=\"loading-indicator\"><span class=\"spinner\"></span></div>
    <div class=\"diff-error\">""")
    _e("Sorry, something went wrong. The requested comparison could not be loaded.")
    php_print("""</div>
    <div class=\"diff\">
    <# _.each( data.fields, function( field ) { #>
    <h3>{{ field.name }}</h3>
    {{{ field.diff }}}
    <# }); #>
    </div>
    </script>
    """)
# end def wp_print_revision_templates
