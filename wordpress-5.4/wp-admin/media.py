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
#// Media management action handler.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
parent_file = "upload.php"
submenu_file = "upload.php"
wp_reset_vars(Array("action"))
for case in Switch(action):
    if case("editattachment"):
        attachment_id = int(PHP_POST["attachment_id"])
        check_admin_referer("media-form")
        if (not current_user_can("edit_post", attachment_id)):
            wp_die(__("Sorry, you are not allowed to edit this attachment."))
        # end if
        errors = media_upload_form_handler()
        if php_empty(lambda : errors):
            location = "media.php"
            referer = wp_get_original_referer()
            if referer:
                if False != php_strpos(referer, "upload.php") or url_to_postid(referer) == attachment_id:
                    location = referer
                # end if
            # end if
            if False != php_strpos(location, "upload.php"):
                location = remove_query_arg("message", location)
                location = add_query_arg("posted", attachment_id, location)
            elif False != php_strpos(location, "media.php"):
                location = add_query_arg("message", "updated", location)
            # end if
            wp_redirect(location)
            php_exit(0)
        # end if
    # end if
    if case("edit"):
        title = __("Edit Media")
        if php_empty(lambda : errors):
            errors = None
        # end if
        if php_empty(lambda : PHP_REQUEST["attachment_id"]):
            wp_redirect(admin_url("upload.php"))
            php_exit(0)
        # end if
        att_id = int(PHP_REQUEST["attachment_id"])
        if (not current_user_can("edit_post", att_id)):
            wp_die(__("Sorry, you are not allowed to edit this attachment."))
        # end if
        att = get_post(att_id)
        if php_empty(lambda : att.ID):
            wp_die(__("You attempted to edit an attachment that doesn&#8217;t exist. Perhaps it was deleted?"))
        # end if
        if "attachment" != att.post_type:
            wp_die(__("You attempted to edit an item that isn&#8217;t an attachment. Please go back and try again."))
        # end if
        if "trash" == att.post_status:
            wp_die(__("You can&#8217;t edit this attachment because it is in the Trash. Please move it out of the Trash and try again."))
        # end if
        add_filter("attachment_fields_to_edit", "media_single_attachment_fields_to_edit", 10, 2)
        wp_enqueue_script("wp-ajax-response")
        wp_enqueue_script("image-edit")
        wp_enqueue_style("imgareaselect")
        get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen allows you to edit fields for metadata in a file within the media library.") + "</p>" + "<p>" + __("For images only, you can click on Edit Image under the thumbnail to expand out an inline image editor with icons for cropping, rotating, or flipping the image as well as for undoing and redoing. The boxes on the right give you more options for scaling the image, for cropping it, and for cropping the thumbnail in a different way than you crop the original image. You can click on Help in those boxes to get more information.") + "</p>" + "<p>" + __("Note that you crop the image by clicking on it (the Crop icon is already selected) and dragging the cropping frame to select the desired part. Then click Save to retain the cropping.") + "</p>" + "<p>" + __("Remember to click Update Media to save metadata entered or changed.") + "</p>"}))
        get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/edit-media/\">Documentation on Edit Media</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
        php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
        parent_file = "upload.php"
        message = ""
        class_ = ""
        if (php_isset(lambda : PHP_REQUEST["message"])):
            for case in Switch(PHP_REQUEST["message"]):
                if case("updated"):
                    message = __("Media file updated.")
                    class_ = "updated"
                    break
                # end if
            # end for
        # end if
        if message:
            php_print(str("<div id='message' class='") + str(class_) + str("'><p>") + str(message) + str("</p></div>\n"))
        # end if
        php_print("""
        <div class=\"wrap\">
        <h1 class=\"wp-heading-inline\">
        """)
        php_print(esc_html(title))
        php_print("</h1>\n\n        ")
        if current_user_can("upload_files"):
            php_print(" <a href=\"media-new.php\" class=\"page-title-action\">")
            php_print(esc_html_x("Add New", "file"))
            php_print("</a>\n")
        # end if
        php_print("""
        <hr class=\"wp-header-end\">
        <form method=\"post\" class=\"media-upload-form\" id=\"media-single-form\">
        <p class=\"submit\" style=\"padding-bottom: 0;\">
        """)
        submit_button(__("Update Media"), "primary", "save", False)
        php_print("""   </p>
        <div class=\"media-single\">
        <div id=\"media-item-""")
        php_print(att_id)
        php_print("\" class=\"media-item\">\n       ")
        php_print(get_media_item(att_id, Array({"toggle": False, "send": False, "delete": False, "show_title": False, "errors": errors[att_id] if (not php_empty(lambda : errors[att_id])) else None})))
        php_print("""   </div>
        </div>
        """)
        submit_button(__("Update Media"), "primary", "save")
        php_print(" <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
        php_print(esc_attr(post_id) if (php_isset(lambda : post_id)) else "")
        php_print("\" />\n  <input type=\"hidden\" name=\"attachment_id\" id=\"attachment_id\" value=\"")
        php_print(esc_attr(att_id))
        php_print("\" />\n  <input type=\"hidden\" name=\"action\" value=\"editattachment\" />\n        ")
        wp_original_referer_field(True, "previous")
        php_print("     ")
        wp_nonce_field("media-form")
        php_print("""
        </form>
        </div>
        """)
        php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
        php_exit(0)
    # end if
    if case():
        wp_redirect(admin_url("upload.php"))
        php_exit(0)
    # end if
# end for
