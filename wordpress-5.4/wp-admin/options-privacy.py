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
#// Privacy Settings Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_privacy_options")):
    wp_die(__("Sorry, you are not allowed to manage privacy on this site."))
# end if
action = PHP_POST["action"] if (php_isset(lambda : PHP_POST["action"])) else ""
if (not php_empty(lambda : action)):
    check_admin_referer(action)
    if "set-privacy-page" == action:
        privacy_policy_page_id = int(PHP_POST["page_for_privacy_policy"]) if (php_isset(lambda : PHP_POST["page_for_privacy_policy"])) else 0
        update_option("wp_page_for_privacy_policy", privacy_policy_page_id)
        privacy_page_updated_message = __("Privacy Policy page updated successfully.")
        if privacy_policy_page_id:
            #// 
            #// Don't always link to the menu customizer:
            #// 
            #// - Unpublished pages can't be selected by default.
            #// - `WP_Customize_Nav_Menus::__construct()` checks the user's capabilities.
            #// - Themes might not "officially" support menus.
            #//
            if "publish" == get_post_status(privacy_policy_page_id) and current_user_can("edit_theme_options") and current_theme_supports("menus"):
                privacy_page_updated_message = php_sprintf(__("Privacy Policy page setting updated successfully. Remember to <a href=\"%s\">update your menus</a>!"), esc_url(add_query_arg("autofocus[panel]", "nav_menus", admin_url("customize.php"))))
            # end if
        # end if
        add_settings_error("page_for_privacy_policy", "page_for_privacy_policy", privacy_page_updated_message, "success")
    elif "create-privacy-page" == action:
        if (not php_class_exists("WP_Privacy_Policy_Content")):
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-policy-content.php", once=True)
        # end if
        privacy_policy_page_content = WP_Privacy_Policy_Content.get_default_content()
        privacy_policy_page_id = wp_insert_post(Array({"post_title": __("Privacy Policy"), "post_status": "draft", "post_type": "page", "post_content": privacy_policy_page_content}), True)
        if is_wp_error(privacy_policy_page_id):
            add_settings_error("page_for_privacy_policy", "page_for_privacy_policy", __("Unable to create a Privacy Policy page."), "error")
        else:
            update_option("wp_page_for_privacy_policy", privacy_policy_page_id)
            wp_redirect(admin_url("post.php?post=" + privacy_policy_page_id + "&action=edit"))
            php_exit(0)
        # end if
    # end if
# end if
#// If a Privacy Policy page ID is available, make sure the page actually exists. If not, display an error.
privacy_policy_page_exists = False
privacy_policy_page_id = int(get_option("wp_page_for_privacy_policy"))
if (not php_empty(lambda : privacy_policy_page_id)):
    privacy_policy_page = get_post(privacy_policy_page_id)
    if (not type(privacy_policy_page).__name__ == "WP_Post"):
        add_settings_error("page_for_privacy_policy", "page_for_privacy_policy", __("The currently selected Privacy Policy page does not exist. Please create or select a new page."), "error")
    else:
        if "trash" == privacy_policy_page.post_status:
            add_settings_error("page_for_privacy_policy", "page_for_privacy_policy", php_sprintf(__("The currently selected Privacy Policy page is in the Trash. Please create or select a new Privacy Policy page or <a href=\"%s\">restore the current page</a>."), "edit.php?post_status=trash&post_type=page"), "error")
        else:
            privacy_policy_page_exists = True
        # end if
    # end if
# end if
title = __("Privacy Settings")
parent_file = "options-general.php"
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n   <h1>")
php_print(title)
php_print("</h1>\n  <h2>")
_e("Privacy Policy Page")
php_print("</h2>\n  <p>\n       ")
_e("As a website owner, you may need to follow national or international privacy laws. For example, you may need to create and display a Privacy Policy.")
php_print("     ")
_e("If you already have a Privacy Policy page, please select it below. If not, please create one.")
php_print(" </p>\n  <p>\n       ")
_e("The new page will include help and suggestions for your Privacy Policy.")
php_print("     ")
_e("However, it is your responsibility to use those resources correctly, to provide the information that your Privacy Policy requires, and to keep that information current and accurate.")
php_print(" </p>\n  <p>\n       ")
_e("After your Privacy Policy page is set, we suggest that you edit it.")
php_print("     ")
_e("We would also suggest reviewing your Privacy Policy from time to time, especially after installing or updating any themes or plugins. There may be changes or new suggested information for you to consider adding to your policy.")
php_print(" </p>\n  ")
if privacy_policy_page_exists:
    edit_href = add_query_arg(Array({"post": privacy_policy_page_id, "action": "edit"}), admin_url("post.php"))
    view_href = get_permalink(privacy_policy_page_id)
    php_print("     <p class=\"tools-privacy-edit\"><strong>\n          ")
    if "publish" == get_post_status(privacy_policy_page_id):
        printf(__("<a href=\"%1$s\">Edit</a> or <a href=\"%2$s\">view</a> your Privacy Policy page content."), esc_url(edit_href), esc_url(view_href))
    else:
        printf(__("<a href=\"%1$s\">Edit</a> or <a href=\"%2$s\">preview</a> your Privacy Policy page content."), esc_url(edit_href), esc_url(view_href))
    # end if
    php_print("     </strong></p>\n     ")
# end if
php_print(" <p>\n       ")
printf(__("Need help putting together your new Privacy Policy page? <a href=\"%1$s\" %2$s>Check out our guide%3$s</a> for recommendations on what content to include, along with policies suggested by your plugins and theme."), esc_url(admin_url("privacy-policy-guide.php")), "", "")
php_print("""   </p>
<hr>
<table class=\"form-table tools-privacy-policy-page\" role=\"presentation\">
<tr>
<th scope=\"row\">
<label for=\"page_for_privacy_policy\">
""")
if privacy_policy_page_exists:
    _e("Change your Privacy Policy page")
else:
    _e("Select a Privacy Policy page")
# end if
php_print("""               </label>
</th>
<td>
""")
has_pages = bool(get_posts(Array({"post_type": "page", "posts_per_page": 1, "post_status": Array("publish", "draft")})))
if has_pages:
    php_print("                 <form method=\"post\" action=\"\">\n                        <input type=\"hidden\" name=\"action\" value=\"set-privacy-page\" />\n                      ")
    wp_dropdown_pages(Array({"name": "page_for_privacy_policy", "show_option_none": __("&mdash; Select &mdash;"), "option_none_value": "0", "selected": privacy_policy_page_id, "post_status": Array("draft", "publish")}))
    wp_nonce_field("set-privacy-page")
    submit_button(__("Use This Page"), "primary", "submit", False, Array({"id": "set-page"}))
    php_print("                 </form>\n               ")
# end if
php_print("""
<form class=\"wp-create-privacy-page\" method=\"post\" action=\"\">
<input type=\"hidden\" name=\"action\" value=\"create-privacy-page\" />
<span>
""")
if has_pages:
    _e("Or:")
else:
    _e("There are no pages.")
# end if
php_print("                 </span>\n                   ")
wp_nonce_field("create-privacy-page")
submit_button(__("Create New Page"), "primary", "submit", False, Array({"id": "create-page"}))
php_print("""               </form>
</td>
</tr>
</table>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
