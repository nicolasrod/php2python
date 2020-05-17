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
#// Revisions administration panel
#// 
#// Requires wp-admin/includes/revision.php.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 2.6.0
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/revision.php", once=False)
#// 
#// @global int    $revision Optional. The revision ID.
#// @global string $action   The action to take.
#// Accepts 'restore', 'view' or 'edit'.
#// @global int    $from     The revision to compare from.
#// @global int    $to       Optional, required if revision missing. The revision to compare to.
#//
wp_reset_vars(Array("revision", "action", "from", "to"))
revision_id_ = absint(revision_)
from_ = absint(from_) if php_is_numeric(from_) else None
if (not revision_id_):
    revision_id_ = absint(to_)
# end if
redirect_ = "edit.php"
for case in Switch(action_):
    if case("restore"):
        revision_ = wp_get_post_revision(revision_id_)
        if (not revision_):
            break
        # end if
        if (not current_user_can("edit_post", revision_.post_parent)):
            break
        # end if
        post_ = get_post(revision_.post_parent)
        if (not post_):
            break
        # end if
        #// Restore if revisions are enabled or this is an autosave.
        if (not wp_revisions_enabled(post_)) and (not wp_is_post_autosave(revision_)):
            redirect_ = "edit.php?post_type=" + post_.post_type
            break
        # end if
        #// Don't allow revision restore when post is locked.
        if wp_check_post_lock(post_.ID):
            break
        # end if
        check_admin_referer(str("restore-post_") + str(revision_.ID))
        wp_restore_post_revision(revision_.ID)
        redirect_ = add_query_arg(Array({"message": 5, "revision": revision_.ID}), get_edit_post_link(post_.ID, "url"))
        break
    # end if
    if case("view"):
        pass
    # end if
    if case("edit"):
        pass
    # end if
    if case():
        revision_ = wp_get_post_revision(revision_id_)
        if (not revision_):
            break
        # end if
        post_ = get_post(revision_.post_parent)
        if (not post_):
            break
        # end if
        if (not current_user_can("read_post", revision_.ID)) or (not current_user_can("edit_post", revision_.post_parent)):
            break
        # end if
        #// Revisions disabled and we're not looking at an autosave.
        if (not wp_revisions_enabled(post_)) and (not wp_is_post_autosave(revision_)):
            redirect_ = "edit.php?post_type=" + post_.post_type
            break
        # end if
        post_edit_link_ = get_edit_post_link()
        post_title_ = "<a href=\"" + post_edit_link_ + "\">" + _draft_or_post_title() + "</a>"
        #// translators: %s: Post title.
        h1_ = php_sprintf(__("Compare Revisions of &#8220;%s&#8221;"), post_title_)
        return_to_post_ = "<a href=\"" + post_edit_link_ + "\">" + __("&larr; Return to editor") + "</a>"
        title_ = __("Revisions")
        redirect_ = False
        break
    # end if
# end for
#// Empty post_type means either malformed object found, or no valid parent was found.
if (not redirect_) and php_empty(lambda : post_.post_type):
    redirect_ = "edit.php"
# end if
if (not php_empty(lambda : redirect_)):
    wp_redirect(redirect_)
    php_exit(0)
# end if
#// This is so that the correct "Edit" menu item is selected.
if (not php_empty(lambda : post_.post_type)) and "post" != post_.post_type:
    parent_file_ = "edit.php?post_type=" + post_.post_type
else:
    parent_file_ = "edit.php"
# end if
submenu_file_ = parent_file_
wp_enqueue_script("revisions")
wp_localize_script("revisions", "_wpRevisionsSettings", wp_prepare_revisions_for_js(post_, revision_id_, from_))
#// Revisions Help Tab
revisions_overview_ = "<p>" + __("This screen is used for managing your content revisions.") + "</p>"
revisions_overview_ += "<p>" + __("Revisions are saved copies of your post or page, which are periodically created as you update your content. The red text on the left shows the content that was removed. The green text on the right shows the content that was added.") + "</p>"
revisions_overview_ += "<p>" + __("From this screen you can review, compare, and restore revisions:") + "</p>"
revisions_overview_ += "<ul><li>" + __("To navigate between revisions, <strong>drag the slider handle left or right</strong> or <strong>use the Previous or Next buttons</strong>.") + "</li>"
revisions_overview_ += "<li>" + __("Compare two different revisions by <strong>selecting the &#8220;Compare any two revisions&#8221; box</strong> to the side.") + "</li>"
revisions_overview_ += "<li>" + __("To restore a revision, <strong>click Restore This Revision</strong>.") + "</li></ul>"
get_current_screen().add_help_tab(Array({"id": "revisions-overview", "title": __("Overview"), "content": revisions_overview_}))
revisions_sidebar_ = "<p><strong>" + __("For more information:") + "</strong></p>"
revisions_sidebar_ += "<p>" + __("<a href=\"https://wordpress.org/support/article/revisions/\">Revisions Management</a>") + "</p>"
revisions_sidebar_ += "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>"
get_current_screen().set_help_sidebar(revisions_sidebar_)
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n <h1 class=\"long-header\">")
php_print(h1_)
php_print("</h1>\n  ")
php_print(return_to_post_)
php_print("</div>\n")
wp_print_revision_templates()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
