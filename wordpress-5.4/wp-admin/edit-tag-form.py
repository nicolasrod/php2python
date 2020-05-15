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
#// Edit tag form for inclusion in administration panels.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Don't load directly.
if (not php_defined("ABSPATH")):
    php_print("-1")
    php_exit()
# end if
#// Back compat hooks.
if "category" == taxonomy:
    #// 
    #// Fires before the Edit Category form.
    #// 
    #// @since 2.1.0
    #// @deprecated 3.0.0 Use {@see '{$taxonomy}_pre_edit_form'} instead.
    #// 
    #// @param WP_Term $tag Current category term object.
    #//
    do_action_deprecated("edit_category_form_pre", Array(tag), "3.0.0", "{$taxonomy}_pre_edit_form")
elif "link_category" == taxonomy:
    #// 
    #// Fires before the Edit Link Category form.
    #// 
    #// @since 2.3.0
    #// @deprecated 3.0.0 Use {@see '{$taxonomy}_pre_edit_form'} instead.
    #// 
    #// @param WP_Term $tag Current link category term object.
    #//
    do_action_deprecated("edit_link_category_form_pre", Array(tag), "3.0.0", "{$taxonomy}_pre_edit_form")
else:
    #// 
    #// Fires before the Edit Tag form.
    #// 
    #// @since 2.5.0
    #// @deprecated 3.0.0 Use {@see '{$taxonomy}_pre_edit_form'} instead.
    #// 
    #// @param WP_Term $tag Current tag term object.
    #//
    do_action_deprecated("edit_tag_form_pre", Array(tag), "3.0.0", "{$taxonomy}_pre_edit_form")
# end if
#// 
#// Use with caution, see https://developer.wordpress.org/reference/functions/wp_reset_vars
#//
wp_reset_vars(Array("wp_http_referer"))
wp_http_referer = remove_query_arg(Array("action", "message", "tag_ID"), wp_http_referer)
#// Also used by Edit Tags
php_include_file(ABSPATH + "wp-admin/includes/edit-tag-messages.php", once=True)
#// 
#// Fires before the Edit Term form for all taxonomies.
#// 
#// The dynamic portion of the hook name, `$taxonomy`, refers to
#// the taxonomy slug.
#// 
#// @since 3.0.0
#// 
#// @param WP_Term $tag      Current taxonomy term object.
#// @param string  $taxonomy Current $taxonomy slug.
#//
do_action(str(taxonomy) + str("_pre_edit_form"), tag, taxonomy)
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(tax.labels.edit_item)
php_print("</h1>\n\n")
class_ = "error" if (php_isset(lambda : msg)) and 5 == msg else "success"
if message:
    php_print("<div id=\"message\" class=\"notice notice-")
    php_print(class_)
    php_print("\">\n    <p><strong>")
    php_print(message)
    php_print("</strong></p>\n  ")
    if wp_http_referer:
        php_print(" <p><a href=\"")
        php_print(esc_url(wp_validate_redirect(esc_url_raw(wp_http_referer), admin_url("term.php?taxonomy=" + taxonomy))))
        php_print("\">\n        ")
        php_print(esc_html(tax.labels.back_to_items))
        php_print(" </a></p>\n  ")
    # end if
    php_print("</div>\n ")
# end if
php_print("""
<div id=\"ajax-response\"></div>
<form name=\"edittag\" id=\"edittag\" method=\"post\" action=\"edit-tags.php\" class=\"validate\"
""")
#// 
#// Fires inside the Edit Term form tag.
#// 
#// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
#// 
#// @since 3.7.0
#//
do_action(str(taxonomy) + str("_term_edit_form_tag"))
php_print(">\n<input type=\"hidden\" name=\"action\" value=\"editedtag\"/>\n<input type=\"hidden\" name=\"tag_ID\" value=\"")
php_print(esc_attr(tag_ID))
php_print("\"/>\n<input type=\"hidden\" name=\"taxonomy\" value=\"")
php_print(esc_attr(taxonomy))
php_print("\"/>\n")
wp_original_referer_field(True, "previous")
wp_nonce_field("update-tag_" + tag_ID)
#// 
#// Fires at the beginning of the Edit Term form.
#// 
#// At this point, the required hidden fields and nonces have already been output.
#// 
#// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
#// 
#// @since 4.5.0
#// 
#// @param WP_Term $tag      Current taxonomy term object.
#// @param string  $taxonomy Current $taxonomy slug.
#//
do_action(str(taxonomy) + str("_term_edit_form_top"), tag, taxonomy)
tag_name_value = ""
if (php_isset(lambda : tag.name)):
    tag_name_value = esc_attr(tag.name)
# end if
php_print(" <table class=\"form-table\" role=\"presentation\">\n        <tr class=\"form-field form-required term-name-wrap\">\n            <th scope=\"row\"><label for=\"name\">")
_ex("Name", "term name")
php_print("</label></th>\n          <td><input name=\"name\" id=\"name\" type=\"text\" value=\"")
php_print(tag_name_value)
php_print("\" size=\"40\" aria-required=\"true\" />\n           <p class=\"description\">")
_e("The name is how it appears on your site.")
php_print("</p></td>\n      </tr>\n")
if (not global_terms_enabled()):
    php_print("     <tr class=\"form-field term-slug-wrap\">\n          <th scope=\"row\"><label for=\"slug\">")
    _e("Slug")
    php_print("</label></th>\n          ")
    #// 
    #// Filters the editable slug.
    #// 
    #// Note: This is a multi-use hook in that it is leveraged both for editable
    #// post URIs and term slugs.
    #// 
    #// @since 2.6.0
    #// @since 4.4.0 The `$tag` parameter was added.
    #// 
    #// @param string          $slug The editable slug. Will be either a term slug or post URI depending
    #// upon the context in which it is evaluated.
    #// @param WP_Term|WP_Post $tag  Term or WP_Post object.
    #//
    slug = apply_filters("editable_slug", tag.slug, tag) if (php_isset(lambda : tag.slug)) else ""
    php_print("         <td><input name=\"slug\" id=\"slug\" type=\"text\" value=\"")
    php_print(esc_attr(slug))
    php_print("\" size=\"40\" />\n          <p class=\"description\">")
    _e("The &#8220;slug&#8221; is the URL-friendly version of the name. It is usually all lowercase and contains only letters, numbers, and hyphens.")
    php_print("</p></td>\n      </tr>\n")
# end if
if is_taxonomy_hierarchical(taxonomy):
    php_print("     <tr class=\"form-field term-parent-wrap\">\n            <th scope=\"row\"><label for=\"parent\">")
    php_print(esc_html(tax.labels.parent_item))
    php_print("</label></th>\n          <td>\n              ")
    dropdown_args = Array({"hide_empty": 0, "hide_if_empty": False, "taxonomy": taxonomy, "name": "parent", "orderby": "name", "selected": tag.parent, "exclude_tree": tag.term_id, "hierarchical": True, "show_option_none": __("None")})
    #// This filter is documented in wp-admin/edit-tags.php
    dropdown_args = apply_filters("taxonomy_parent_dropdown_args", dropdown_args, taxonomy, "edit")
    wp_dropdown_categories(dropdown_args)
    php_print("             ")
    if "category" == taxonomy:
        php_print("                 <p class=\"description\">")
        _e("Categories, unlike tags, can have a hierarchy. You might have a Jazz category, and under that have children categories for Bebop and Big Band. Totally optional.")
        php_print("</p>\n               ")
    else:
        php_print("                 <p class=\"description\">")
        _e("Assign a parent term to create a hierarchy. The term Jazz, for example, would be the parent of Bebop and Big Band.")
        php_print("</p>\n               ")
    # end if
    php_print("         </td>\n     </tr>\n")
# end if
pass
php_print("     <tr class=\"form-field term-description-wrap\">\n           <th scope=\"row\"><label for=\"description\">")
_e("Description")
php_print("</label></th>\n          <td><textarea name=\"description\" id=\"description\" rows=\"5\" cols=\"50\" class=\"large-text\">")
php_print(tag.description)
pass
php_print("</textarea>\n            <p class=\"description\">")
_e("The description is not prominent by default; however, some themes may show it.")
php_print("</p></td>\n      </tr>\n     ")
#// Back compat hooks.
if "category" == taxonomy:
    #// 
    #// Fires after the Edit Category form fields are displayed.
    #// 
    #// @since 2.9.0
    #// @deprecated 3.0.0 Use {@see '{$taxonomy}_edit_form_fields'} instead.
    #// 
    #// @param WP_Term $tag Current category term object.
    #//
    do_action_deprecated("edit_category_form_fields", Array(tag), "3.0.0", "{$taxonomy}_edit_form_fields")
elif "link_category" == taxonomy:
    #// 
    #// Fires after the Edit Link Category form fields are displayed.
    #// 
    #// @since 2.9.0
    #// @deprecated 3.0.0 Use {@see '{$taxonomy}_edit_form_fields'} instead.
    #// 
    #// @param WP_Term $tag Current link category term object.
    #//
    do_action_deprecated("edit_link_category_form_fields", Array(tag), "3.0.0", "{$taxonomy}_edit_form_fields")
else:
    #// 
    #// Fires after the Edit Tag form fields are displayed.
    #// 
    #// @since 2.9.0
    #// @deprecated 3.0.0 Use {@see '{$taxonomy}_edit_form_fields'} instead.
    #// 
    #// @param WP_Term $tag Current tag term object.
    #//
    do_action_deprecated("edit_tag_form_fields", Array(tag), "3.0.0", "{$taxonomy}_edit_form_fields")
# end if
#// 
#// Fires after the Edit Term form fields are displayed.
#// 
#// The dynamic portion of the hook name, `$taxonomy`, refers to
#// the taxonomy slug.
#// 
#// @since 3.0.0
#// 
#// @param WP_Term $tag      Current taxonomy term object.
#// @param string  $taxonomy Current taxonomy slug.
#//
do_action(str(taxonomy) + str("_edit_form_fields"), tag, taxonomy)
php_print(" </table>\n")
#// Back compat hooks.
if "category" == taxonomy:
    #// This action is documented in wp-admin/edit-tags.php
    do_action_deprecated("edit_category_form", Array(tag), "3.0.0", "{$taxonomy}_add_form")
elif "link_category" == taxonomy:
    #// This action is documented in wp-admin/edit-tags.php
    do_action_deprecated("edit_link_category_form", Array(tag), "3.0.0", "{$taxonomy}_add_form")
else:
    #// 
    #// Fires at the end of the Edit Term form.
    #// 
    #// @since 2.5.0
    #// @deprecated 3.0.0 Use {@see '{$taxonomy}_edit_form'} instead.
    #// 
    #// @param WP_Term $tag Current taxonomy term object.
    #//
    do_action_deprecated("edit_tag_form", Array(tag), "3.0.0", "{$taxonomy}_edit_form")
# end if
#// 
#// Fires at the end of the Edit Term form for all taxonomies.
#// 
#// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
#// 
#// @since 3.0.0
#// 
#// @param WP_Term $tag      Current taxonomy term object.
#// @param string  $taxonomy Current taxonomy slug.
#//
do_action(str(taxonomy) + str("_edit_form"), tag, taxonomy)
php_print("""
<div class=\"edit-tag-actions\">
""")
submit_button(__("Update"), "primary", None, False)
php_print("\n   ")
if current_user_can("delete_term", tag.term_id):
    php_print("     <span id=\"delete-link\">\n         <a class=\"delete\" href=\"")
    php_print(admin_url(wp_nonce_url(str("edit-tags.php?action=delete&taxonomy=") + str(taxonomy) + str("&tag_ID=") + str(tag.term_id), "delete-tag_" + tag.term_id)))
    php_print("\">")
    _e("Delete")
    php_print("</a>\n       </span>\n   ")
# end if
php_print("""
</div>
</form>
</div>
""")
if (not wp_is_mobile()):
    php_print("""<script type=\"text/javascript\">
try{document.forms.edittag.name.focus();}catch(e){}
    </script>
    """)
# end if
