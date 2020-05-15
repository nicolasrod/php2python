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
revision_id = absint(revision)
from_ = absint(from_) if php_is_numeric(from_) else None
if (not revision_id):
    revision_id = absint(to)
# end if
redirect = "edit.php"
for case in Switch(action):
    if case("restore"):
        revision = wp_get_post_revision(revision_id)
        if (not revision):
            break
        # end if
        if (not current_user_can("edit_post", revision.post_parent)):
            break
        # end if
        post = get_post(revision.post_parent)
        if (not post):
            break
        # end if
        #// Restore if revisions are enabled or this is an autosave.
        if (not wp_revisions_enabled(post)) and (not wp_is_post_autosave(revision)):
            redirect = "edit.php?post_type=" + post.post_type
            break
        # end if
        #// Don't allow revision restore when post is locked.
        if wp_check_post_lock(post.ID):
            break
        # end if
        check_admin_referer(str("restore-post_") + str(revision.ID))
        wp_restore_post_revision(revision.ID)
        redirect = add_query_arg(Array({"message": 5, "revision": revision.ID}), get_edit_post_link(post.ID, "url"))
        break
    # end if
    if case("view"):
        pass
    # end if
    if case("edit"):
        pass
    # end if
    if case():
        revision = wp_get_post_revision(revision_id)
        if (not revision):
            break
        # end if
        post = get_post(revision.post_parent)
        if (not post):
            break
        # end if
        if (not current_user_can("read_post", revision.ID)) or (not current_user_can("edit_post", revision.post_parent)):
            break
        # end if
        #// Revisions disabled and we're not looking at an autosave.
        if (not wp_revisions_enabled(post)) and (not wp_is_post_autosave(revision)):
            redirect = "edit.php?post_type=" + post.post_type
            break
        # end if
        post_edit_link = get_edit_post_link()
        post_title = "<a href=\"" + post_edit_link + "\">" + _draft_or_post_title() + "</a>"
        #// translators: %s: Post title.
        h1 = php_sprintf(__("Compare Revisions of &#8220;%s&#8221;"), post_title)
        return_to_post = "<a href=\"" + post_edit_link + "\">" + __("&larr; Return to editor") + "</a>"
        title = __("Revisions")
        redirect = False
        break
    # end if
# end for
#// Empty post_type means either malformed object found, or no valid parent was found.
if (not redirect) and php_empty(lambda : post.post_type):
    redirect = "edit.php"
# end if
if (not php_empty(lambda : redirect)):
    wp_redirect(redirect)
    php_exit(0)
# end if
#// This is so that the correct "Edit" menu item is selected.
if (not php_empty(lambda : post.post_type)) and "post" != post.post_type:
    parent_file = "edit.php?post_type=" + post.post_type
else:
    parent_file = "edit.php"
# end if
submenu_file = parent_file
wp_enqueue_script("revisions")
wp_localize_script("revisions", "_wpRevisionsSettings", wp_prepare_revisions_for_js(post, revision_id, from_))
#// Revisions Help Tab
revisions_overview = "<p>" + __("This screen is used for managing your content revisions.") + "</p>"
revisions_overview += "<p>" + __("Revisions are saved copies of your post or page, which are periodically created as you update your content. The red text on the left shows the content that was removed. The green text on the right shows the content that was added.") + "</p>"
revisions_overview += "<p>" + __("From this screen you can review, compare, and restore revisions:") + "</p>"
revisions_overview += "<ul><li>" + __("To navigate between revisions, <strong>drag the slider handle left or right</strong> or <strong>use the Previous or Next buttons</strong>.") + "</li>"
revisions_overview += "<li>" + __("Compare two different revisions by <strong>selecting the &#8220;Compare any two revisions&#8221; box</strong> to the side.") + "</li>"
revisions_overview += "<li>" + __("To restore a revision, <strong>click Restore This Revision</strong>.") + "</li></ul>"
get_current_screen().add_help_tab(Array({"id": "revisions-overview", "title": __("Overview"), "content": revisions_overview}))
revisions_sidebar = "<p><strong>" + __("For more information:") + "</strong></p>"
revisions_sidebar += "<p>" + __("<a href=\"https://wordpress.org/support/article/revisions/\">Revisions Management</a>") + "</p>"
revisions_sidebar += "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>"
get_current_screen().set_help_sidebar(revisions_sidebar)
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n <h1 class=\"long-header\">")
php_print(h1)
php_print("</h1>\n  ")
php_print(return_to_post)
php_print("</div>\n")
wp_print_revision_templates()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
