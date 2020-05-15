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
#// WordPress Image Editor
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Loads the WP image-editing interface.
#// 
#// @since 2.9.0
#// 
#// @param int         $post_id Attachment post ID.
#// @param bool|object $msg     Optional. Message to display for image editor updates or errors.
#// Default false.
#//
def wp_image_editor(post_id=None, msg=False, *args_):
    
    nonce = wp_create_nonce(str("image_editor-") + str(post_id))
    meta = wp_get_attachment_metadata(post_id)
    thumb = image_get_intermediate_size(post_id, "thumbnail")
    sub_sizes = (php_isset(lambda : meta["sizes"])) and php_is_array(meta["sizes"])
    note = ""
    if (php_isset(lambda : meta["width"]) and php_isset(lambda : meta["height"])):
        big = php_max(meta["width"], meta["height"])
    else:
        php_print(__("Image data does not exist. Please re-upload the image."))
        php_exit()
    # end if
    sizer = 400 / big if big > 400 else 1
    backup_sizes = get_post_meta(post_id, "_wp_attachment_backup_sizes", True)
    can_restore = False
    if (not php_empty(lambda : backup_sizes)) and (php_isset(lambda : backup_sizes["full-orig"]) and php_isset(lambda : meta["file"])):
        can_restore = wp_basename(meta["file"]) != backup_sizes["full-orig"]["file"]
    # end if
    if msg:
        if (php_isset(lambda : msg.error)):
            note = str("<div class='error'><p>") + str(msg.error) + str("</p></div>")
        elif (php_isset(lambda : msg.msg)):
            note = str("<div class='updated'><p>") + str(msg.msg) + str("</p></div>")
        # end if
    # end if
    php_print(" <div class=\"imgedit-wrap wp-clearfix\">\n  <div id=\"imgedit-panel-")
    php_print(post_id)
    php_print("""\">
    <div class=\"imgedit-settings\">
    <div class=\"imgedit-group\">
    <div class=\"imgedit-group-top\">
    <h2>""")
    _e("Scale Image")
    php_print("</h2>\n      <button type=\"button\" class=\"dashicons dashicons-editor-help imgedit-help-toggle\" onclick=\"imageEdit.toggleHelp(this);return false;\" aria-expanded=\"false\"><span class=\"screen-reader-text\">")
    esc_html_e("Scale Image Help")
    php_print("</span></button>\n       <div class=\"imgedit-help\">\n      <p>")
    _e("You can proportionally scale the original image. For best results, scaling should be done before you crop, flip, or rotate. Images can only be scaled down, not up.")
    php_print("</p>\n       </div>\n        ")
    if (php_isset(lambda : meta["width"]) and php_isset(lambda : meta["height"])):
        php_print("     <p>\n           ")
        printf(__("Original dimensions %s"), "<span class=\"imgedit-original-dimensions\">" + meta["width"] + " &times; " + meta["height"] + "</span>")
        php_print("     </p>\n      ")
    # end if
    php_print("""       <div class=\"imgedit-submit\">
    <fieldset class=\"imgedit-scale\">
    <legend>""")
    _e("New dimensions:")
    php_print("</legend>\n      <div class=\"nowrap\">\n        <label for=\"imgedit-scale-width-")
    php_print(post_id)
    php_print("\" class=\"screen-reader-text\">")
    _e("scale width")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-scale-width-")
    php_print(post_id)
    php_print("\" onkeyup=\"imageEdit.scaleChanged(")
    php_print(post_id)
    php_print(", 1, this)\" onblur=\"imageEdit.scaleChanged(")
    php_print(post_id)
    php_print(", 1, this)\" value=\"")
    php_print(meta["width"] if (php_isset(lambda : meta["width"])) else 0)
    php_print("\" />\n      <span class=\"imgedit-separator\" aria-hidden=\"true\">&times;</span>\n     <label for=\"imgedit-scale-height-")
    php_print(post_id)
    php_print("\" class=\"screen-reader-text\">")
    _e("scale height")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-scale-height-")
    php_print(post_id)
    php_print("\" onkeyup=\"imageEdit.scaleChanged(")
    php_print(post_id)
    php_print(", 0, this)\" onblur=\"imageEdit.scaleChanged(")
    php_print(post_id)
    php_print(", 0, this)\" value=\"")
    php_print(meta["height"] if (php_isset(lambda : meta["height"])) else 0)
    php_print("\" />\n      <span class=\"imgedit-scale-warn\" id=\"imgedit-scale-warn-")
    php_print(post_id)
    php_print("\">!</span>\n        <div class=\"imgedit-scale-button-wrapper\"><input id=\"imgedit-scale-button\" type=\"button\" onclick=\"imageEdit.action(")
    php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
    php_print(", 'scale')\" class=\"button button-primary\" value=\"")
    esc_attr_e("Scale")
    php_print("""\" /></div>
    </div>
    </fieldset>
    </div>
    </div>
    </div>
    """)
    if can_restore:
        php_print("""
        <div class=\"imgedit-group\">
        <div class=\"imgedit-group-top\">
        <h2><button type=\"button\" onclick=\"imageEdit.toggleHelp(this);\" class=\"button-link\">""")
        _e("Restore Original Image")
        php_print(""" <span class=\"dashicons dashicons-arrow-down imgedit-help-toggle\"></span></button></h2>
        <div class=\"imgedit-help imgedit-restore\">
        <p>
        """)
        _e("Discard any changes and restore the original image.")
        if (not php_defined("IMAGE_EDIT_OVERWRITE")) or (not IMAGE_EDIT_OVERWRITE):
            php_print(" " + __("Previously edited copies of the image will not be deleted."))
        # end if
        php_print("     </p>\n      <div class=\"imgedit-submit\">\n        <input type=\"button\" onclick=\"imageEdit.action(")
        php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
        php_print(", 'restore')\" class=\"button button-primary\" value=\"")
        esc_attr_e("Restore image")
        php_print("\" ")
        php_print(can_restore)
        php_print(""" />
        </div>
        </div>
        </div>
        </div>
        """)
    # end if
    php_print("""
    <div class=\"imgedit-group\">
    <div class=\"imgedit-group-top\">
    <h2>""")
    _e("Image Crop")
    php_print("</h2>\n      <button type=\"button\" class=\"dashicons dashicons-editor-help imgedit-help-toggle\" onclick=\"imageEdit.toggleHelp(this);return false;\" aria-expanded=\"false\"><span class=\"screen-reader-text\">")
    esc_html_e("Image Crop Help")
    php_print("""</span></button>
    <div class=\"imgedit-help\">
    <p>""")
    _e("To crop the image, click on it and drag to make your selection.")
    php_print("</p>\n\n     <p><strong>")
    _e("Crop Aspect Ratio")
    php_print("</strong><br />\n        ")
    _e("The aspect ratio is the relationship between the width and height. You can preserve the aspect ratio by holding down the shift key while resizing your selection. Use the input box to specify the aspect ratio, e.g. 1:1 (square), 4:3, 16:9, etc.")
    php_print("</p>\n\n     <p><strong>")
    _e("Crop Selection")
    php_print("</strong><br />\n        ")
    _e("Once you have made your selection, you can adjust it by entering the size in pixels. The minimum selection size is the thumbnail size as set in the Media settings.")
    php_print("""</p>
    </div>
    </div>
    <fieldset class=\"imgedit-crop-ratio\">
    <legend>""")
    _e("Aspect ratio:")
    php_print("</legend>\n      <div class=\"nowrap\">\n        <label for=\"imgedit-crop-width-")
    php_print(post_id)
    php_print("\" class=\"screen-reader-text\">")
    _e("crop ratio width")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-crop-width-")
    php_print(post_id)
    php_print("\" onkeyup=\"imageEdit.setRatioSelection(")
    php_print(post_id)
    php_print(", 0, this)\" onblur=\"imageEdit.setRatioSelection(")
    php_print(post_id)
    php_print(", 0, this)\" />\n        <span class=\"imgedit-separator\" aria-hidden=\"true\">:</span>\n       <label for=\"imgedit-crop-height-")
    php_print(post_id)
    php_print("\" class=\"screen-reader-text\">")
    _e("crop ratio height")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-crop-height-")
    php_print(post_id)
    php_print("\" onkeyup=\"imageEdit.setRatioSelection(")
    php_print(post_id)
    php_print(", 1, this)\" onblur=\"imageEdit.setRatioSelection(")
    php_print(post_id)
    php_print(""", 1, this)\" />
    </div>
    </fieldset>
    <fieldset id=\"imgedit-crop-sel-""")
    php_print(post_id)
    php_print("\" class=\"imgedit-crop-sel\">\n     <legend>")
    _e("Selection:")
    php_print("</legend>\n      <div class=\"nowrap\">\n        <label for=\"imgedit-sel-width-")
    php_print(post_id)
    php_print("\" class=\"screen-reader-text\">")
    _e("selection width")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-sel-width-")
    php_print(post_id)
    php_print("\" onkeyup=\"imageEdit.setNumSelection(")
    php_print(post_id)
    php_print(", this)\" onblur=\"imageEdit.setNumSelection(")
    php_print(post_id)
    php_print(", this)\" />\n       <span class=\"imgedit-separator\" aria-hidden=\"true\">&times;</span>\n     <label for=\"imgedit-sel-height-")
    php_print(post_id)
    php_print("\" class=\"screen-reader-text\">")
    _e("selection height")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-sel-height-")
    php_print(post_id)
    php_print("\" onkeyup=\"imageEdit.setNumSelection(")
    php_print(post_id)
    php_print(", this)\" onblur=\"imageEdit.setNumSelection(")
    php_print(post_id)
    php_print(""", this)\" />
    </div>
    </fieldset>
    </div>
    """)
    if thumb and sub_sizes:
        thumb_img = wp_constrain_dimensions(thumb["width"], thumb["height"], 160, 120)
        php_print("""
        <div class=\"imgedit-group imgedit-applyto\">
        <div class=\"imgedit-group-top\">
        <h2>""")
        _e("Thumbnail Settings")
        php_print("</h2>\n      <button type=\"button\" class=\"dashicons dashicons-editor-help imgedit-help-toggle\" onclick=\"imageEdit.toggleHelp(this);return false;\" aria-expanded=\"false\"><span class=\"screen-reader-text\">")
        esc_html_e("Thumbnail Settings Help")
        php_print("</span></button>\n       <div class=\"imgedit-help\">\n      <p>")
        _e("You can edit the image while preserving the thumbnail. For example, you may wish to have a square thumbnail that displays just a section of the image.")
        php_print("""</p>
        </div>
        </div>
        <figure class=\"imgedit-thumbnail-preview\">
        <img src=\"""")
        php_print(thumb["url"])
        php_print("\" width=\"")
        php_print(thumb_img[0])
        php_print("\" height=\"")
        php_print(thumb_img[1])
        php_print("\" class=\"imgedit-size-preview\" alt=\"\" draggable=\"false\" />\n      <figcaption class=\"imgedit-thumbnail-preview-caption\">")
        _e("Current thumbnail")
        php_print("""</figcaption>
        </figure>
        <div id=\"imgedit-save-target-""")
        php_print(post_id)
        php_print("\" class=\"imgedit-save-target\">\n  <fieldset>\n        <legend>")
        _e("Apply changes to:")
        php_print("""</legend>
        <span class=\"imgedit-label\">
        <input type=\"radio\" id=\"imgedit-target-all\" name=\"imgedit-target-""")
        php_print(post_id)
        php_print("\" value=\"all\" checked=\"checked\" />\n            <label for=\"imgedit-target-all\">")
        _e("All image sizes")
        php_print("""</label>
        </span>
        <span class=\"imgedit-label\">
        <input type=\"radio\" id=\"imgedit-target-thumbnail\" name=\"imgedit-target-""")
        php_print(post_id)
        php_print("\" value=\"thumbnail\" />\n          <label for=\"imgedit-target-thumbnail\">")
        _e("Thumbnail")
        php_print("""</label>
        </span>
        <span class=\"imgedit-label\">
        <input type=\"radio\" id=\"imgedit-target-nothumb\" name=\"imgedit-target-""")
        php_print(post_id)
        php_print("\" value=\"nothumb\" />\n            <label for=\"imgedit-target-nothumb\">")
        _e("All sizes except thumbnail")
        php_print("""</label>
        </span>
        </fieldset>
        </div>
        </div>
        """)
    # end if
    php_print("""
    </div>
    <div class=\"imgedit-panel-content wp-clearfix\">
    """)
    php_print(note)
    php_print("     <div class=\"imgedit-menu wp-clearfix\">\n          <button type=\"button\" onclick=\"imageEdit.handleCropToolClick( ")
    php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
    php_print(", this )\" class=\"imgedit-crop button disabled\" disabled>")
    esc_html_e("Crop")
    php_print("</button>\n          ")
    #// On some setups GD library does not provide imagerotate() - Ticket #11536.
    if wp_image_editor_supports(Array({"mime_type": get_post_mime_type(post_id), "methods": Array("rotate")})):
        note_no_rotate = ""
        php_print("             <button type=\"button\" class=\"imgedit-rleft button\" onclick=\"imageEdit.rotate( 90, ")
        php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
        php_print(", this)\">")
        esc_html_e("Rotate left")
        php_print("</button>\n              <button type=\"button\" class=\"imgedit-rright button\" onclick=\"imageEdit.rotate(-90, ")
        php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
        php_print(", this)\">")
        esc_html_e("Rotate right")
        php_print("</button>\n              ")
    else:
        note_no_rotate = "<p class=\"note-no-rotate\"><em>" + __("Image rotation is not supported by your web host.") + "</em></p>"
        php_print("             <button type=\"button\" class=\"imgedit-rleft button disabled\" disabled></button>\n                <button type=\"button\" class=\"imgedit-rright button disabled\" disabled></button>\n           ")
    # end if
    php_print("\n           <button type=\"button\" onclick=\"imageEdit.flip(1, ")
    php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
    php_print(", this)\" class=\"imgedit-flipv button\">")
    esc_html_e("Flip vertical")
    php_print("</button>\n          <button type=\"button\" onclick=\"imageEdit.flip(2, ")
    php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
    php_print(", this)\" class=\"imgedit-fliph button\">")
    esc_html_e("Flip horizontal")
    php_print("""</button>
    <br class=\"imgedit-undo-redo-separator\" />
    <button type=\"button\" id=\"image-undo-""")
    php_print(post_id)
    php_print("\" onclick=\"imageEdit.undo(")
    php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
    php_print(", this)\" class=\"imgedit-undo button disabled\" disabled>")
    esc_html_e("Undo")
    php_print("</button>\n          <button type=\"button\" id=\"image-redo-")
    php_print(post_id)
    php_print("\" onclick=\"imageEdit.redo(")
    php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
    php_print(", this)\" class=\"imgedit-redo button disabled\" disabled>")
    esc_html_e("Redo")
    php_print("</button>\n          ")
    php_print(note_no_rotate)
    php_print("     </div>\n\n      <input type=\"hidden\" id=\"imgedit-sizer-")
    php_print(post_id)
    php_print("\" value=\"")
    php_print(sizer)
    php_print("\" />\n      <input type=\"hidden\" id=\"imgedit-history-")
    php_print(post_id)
    php_print("\" value=\"\" />\n       <input type=\"hidden\" id=\"imgedit-undone-")
    php_print(post_id)
    php_print("\" value=\"0\" />\n      <input type=\"hidden\" id=\"imgedit-selection-")
    php_print(post_id)
    php_print("\" value=\"\" />\n       <input type=\"hidden\" id=\"imgedit-x-")
    php_print(post_id)
    php_print("\" value=\"")
    php_print(meta["width"] if (php_isset(lambda : meta["width"])) else 0)
    php_print("\" />\n      <input type=\"hidden\" id=\"imgedit-y-")
    php_print(post_id)
    php_print("\" value=\"")
    php_print(meta["height"] if (php_isset(lambda : meta["height"])) else 0)
    php_print("\" />\n\n        <div id=\"imgedit-crop-")
    php_print(post_id)
    php_print("\" class=\"imgedit-crop-wrap\">\n        <img id=\"image-preview-")
    php_print(post_id)
    php_print("\" onload=\"imageEdit.imgLoaded('")
    php_print(post_id)
    php_print("')\" src=\"")
    php_print(admin_url("admin-ajax.php", "relative"))
    php_print("?action=imgedit-preview&amp;_ajax_nonce=")
    php_print(nonce)
    php_print("&amp;postid=")
    php_print(post_id)
    php_print("&amp;rand=")
    php_print(rand(1, 99999))
    php_print("""\" alt=\"\" />
    </div>
    <div class=\"imgedit-submit\">
    <input type=\"button\" onclick=\"imageEdit.close(""")
    php_print(post_id)
    php_print(", 1)\" class=\"button imgedit-cancel-btn\" value=\"")
    esc_attr_e("Cancel")
    php_print("\" />\n          <input type=\"button\" onclick=\"imageEdit.save(")
    php_print(str(post_id) + str(", '") + str(nonce) + str("'"))
    php_print(")\" disabled=\"disabled\" class=\"button button-primary imgedit-submit-btn\" value=\"")
    esc_attr_e("Save")
    php_print("""\" />
    </div>
    </div>
    </div>
    <div class=\"imgedit-wait\" id=\"imgedit-wait-""")
    php_print(post_id)
    php_print("\"></div>\n  <div class=\"hidden\" id=\"imgedit-leaving-")
    php_print(post_id)
    php_print("\">")
    _e("There are unsaved changes that will be lost. 'OK' to continue, 'Cancel' to return to the Image Editor.")
    php_print("</div>\n </div>\n    ")
# end def wp_image_editor
#// 
#// Streams image in WP_Image_Editor to browser.
#// 
#// @since 2.9.0
#// 
#// @param WP_Image_Editor $image         The image editor instance.
#// @param string          $mime_type     The mime type of the image.
#// @param int             $attachment_id The image's attachment post ID.
#// @return bool True on success, false on failure.
#//
def wp_stream_image(image=None, mime_type=None, attachment_id=None, *args_):
    
    if type(image).__name__ == "WP_Image_Editor":
        #// 
        #// Filters the WP_Image_Editor instance for the image to be streamed to the browser.
        #// 
        #// @since 3.5.0
        #// 
        #// @param WP_Image_Editor $image         The image editor instance.
        #// @param int             $attachment_id The attachment post ID.
        #//
        image = apply_filters("image_editor_save_pre", image, attachment_id)
        if is_wp_error(image.stream(mime_type)):
            return False
        # end if
        return True
    else:
        #// translators: 1: $image, 2: WP_Image_Editor
        _deprecated_argument(__FUNCTION__, "3.5.0", php_sprintf(__("%1$s needs to be a %2$s object."), "$image", "WP_Image_Editor"))
        #// 
        #// Filters the GD image resource to be streamed to the browser.
        #// 
        #// @since 2.9.0
        #// @deprecated 3.5.0 Use {@see 'image_editor_save_pre'} instead.
        #// 
        #// @param resource $image         Image resource to be streamed.
        #// @param int      $attachment_id The attachment post ID.
        #//
        image = apply_filters_deprecated("image_save_pre", Array(image, attachment_id), "3.5.0", "image_editor_save_pre")
        for case in Switch(mime_type):
            if case("image/jpeg"):
                php_header("Content-Type: image/jpeg")
                return imagejpeg(image, None, 90)
            # end if
            if case("image/png"):
                php_header("Content-Type: image/png")
                return imagepng(image)
            # end if
            if case("image/gif"):
                php_header("Content-Type: image/gif")
                return imagegif(image)
            # end if
            if case():
                return False
            # end if
        # end for
    # end if
# end def wp_stream_image
#// 
#// Saves image to file.
#// 
#// @since 2.9.0
#// 
#// @param string          $filename  Name of the file to be saved.
#// @param WP_Image_Editor $image     The image editor instance.
#// @param string          $mime_type The mime type of the image.
#// @param int             $post_id   Attachment post ID.
#// @return bool True on success, false on failure.
#//
def wp_save_image_file(filename=None, image=None, mime_type=None, post_id=None, *args_):
    
    if type(image).__name__ == "WP_Image_Editor":
        #// This filter is documented in wp-admin/includes/image-edit.php
        image = apply_filters("image_editor_save_pre", image, post_id)
        #// 
        #// Filters whether to skip saving the image file.
        #// 
        #// Returning a non-null value will short-circuit the save method,
        #// returning that value instead.
        #// 
        #// @since 3.5.0
        #// 
        #// @param bool|null       $override  Value to return instead of saving. Default null.
        #// @param string          $filename  Name of the file to be saved.
        #// @param WP_Image_Editor $image     The image editor instance.
        #// @param string          $mime_type The mime type of the image.
        #// @param int             $post_id   Attachment post ID.
        #//
        saved = apply_filters("wp_save_image_editor_file", None, filename, image, mime_type, post_id)
        if None != saved:
            return saved
        # end if
        return image.save(filename, mime_type)
    else:
        #// translators: 1: $image, 2: WP_Image_Editor
        _deprecated_argument(__FUNCTION__, "3.5.0", php_sprintf(__("%1$s needs to be a %2$s object."), "$image", "WP_Image_Editor"))
        #// This filter is documented in wp-admin/includes/image-edit.php
        image = apply_filters_deprecated("image_save_pre", Array(image, post_id), "3.5.0", "image_editor_save_pre")
        #// 
        #// Filters whether to skip saving the image file.
        #// 
        #// Returning a non-null value will short-circuit the save method,
        #// returning that value instead.
        #// 
        #// @since 2.9.0
        #// @deprecated 3.5.0 Use {@see 'wp_save_image_editor_file'} instead.
        #// 
        #// @param mixed           $override  Value to return instead of saving. Default null.
        #// @param string          $filename  Name of the file to be saved.
        #// @param WP_Image_Editor $image     The image editor instance.
        #// @param string          $mime_type The mime type of the image.
        #// @param int             $post_id   Attachment post ID.
        #//
        saved = apply_filters_deprecated("wp_save_image_file", Array(None, filename, image, mime_type, post_id), "3.5.0", "wp_save_image_editor_file")
        if None != saved:
            return saved
        # end if
        for case in Switch(mime_type):
            if case("image/jpeg"):
                #// This filter is documented in wp-includes/class-wp-image-editor.php
                return imagejpeg(image, filename, apply_filters("jpeg_quality", 90, "edit_image"))
            # end if
            if case("image/png"):
                return imagepng(image, filename)
            # end if
            if case("image/gif"):
                return imagegif(image, filename)
            # end if
            if case():
                return False
            # end if
        # end for
    # end if
# end def wp_save_image_file
#// 
#// Image preview ratio. Internal use only.
#// 
#// @since 2.9.0
#// 
#// @ignore
#// @param int $w Image width in pixels.
#// @param int $h Image height in pixels.
#// @return float|int Image preview ratio.
#//
def _image_get_preview_ratio(w=None, h=None, *args_):
    
    max = php_max(w, h)
    return 400 / max if max > 400 else 1
# end def _image_get_preview_ratio
#// 
#// Returns an image resource. Internal use only.
#// 
#// @since 2.9.0
#// @deprecated 3.5.0 Use WP_Image_Editor::rotate()
#// @see WP_Image_Editor::rotate()
#// 
#// @ignore
#// @param resource  $img   Image resource.
#// @param float|int $angle Image rotation angle, in degrees.
#// @return resource|false GD image resource, false otherwise.
#//
def _rotate_image_resource(img=None, angle=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0", "WP_Image_Editor::rotate()")
    if php_function_exists("imagerotate"):
        rotated = imagerotate(img, angle, 0)
        if is_resource(rotated):
            imagedestroy(img)
            img = rotated
        # end if
    # end if
    return img
# end def _rotate_image_resource
#// 
#// Flips an image resource. Internal use only.
#// 
#// @since 2.9.0
#// @deprecated 3.5.0 Use WP_Image_Editor::flip()
#// @see WP_Image_Editor::flip()
#// 
#// @ignore
#// @param resource $img  Image resource.
#// @param bool     $horz Whether to flip horizontally.
#// @param bool     $vert Whether to flip vertically.
#// @return resource (maybe) flipped image resource.
#//
def _flip_image_resource(img=None, horz=None, vert=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0", "WP_Image_Editor::flip()")
    w = imagesx(img)
    h = imagesy(img)
    dst = wp_imagecreatetruecolor(w, h)
    if is_resource(dst):
        sx = w - 1 if vert else 0
        sy = h - 1 if horz else 0
        sw = -w if vert else w
        sh = -h if horz else h
        if imagecopyresampled(dst, img, 0, 0, sx, sy, w, h, sw, sh):
            imagedestroy(img)
            img = dst
        # end if
    # end if
    return img
# end def _flip_image_resource
#// 
#// Crops an image resource. Internal use only.
#// 
#// @since 2.9.0
#// 
#// @ignore
#// @param resource $img Image resource.
#// @param float    $x   Source point x-coordinate.
#// @param float    $y   Source point y-coordinate.
#// @param float    $w   Source width.
#// @param float    $h   Source height.
#// @return resource (maybe) cropped image resource.
#//
def _crop_image_resource(img=None, x=None, y=None, w=None, h=None, *args_):
    
    dst = wp_imagecreatetruecolor(w, h)
    if is_resource(dst):
        if imagecopy(dst, img, 0, 0, x, y, w, h):
            imagedestroy(img)
            img = dst
        # end if
    # end if
    return img
# end def _crop_image_resource
i += 1
#// 
#// Performs group of changes on Editor specified.
#// 
#// @since 2.9.0
#// 
#// @param WP_Image_Editor $image   WP_Image_Editor instance.
#// @param array           $changes Array of change operations.
#// @return WP_Image_Editor WP_Image_Editor instance with changes applied.
#//
def image_edit_apply_changes(image=None, changes=None, *args_):
    
    if is_resource(image):
        #// translators: 1: $image, 2: WP_Image_Editor
        _deprecated_argument(__FUNCTION__, "3.5.0", php_sprintf(__("%1$s needs to be a %2$s object."), "$image", "WP_Image_Editor"))
    # end if
    if (not php_is_array(changes)):
        return image
    # end if
    #// Expand change operations.
    for key,obj in changes:
        if (php_isset(lambda : obj.r)):
            obj.type = "rotate"
            obj.angle = obj.r
            obj.r = None
        elif (php_isset(lambda : obj.f)):
            obj.type = "flip"
            obj.axis = obj.f
            obj.f = None
        elif (php_isset(lambda : obj.c)):
            obj.type = "crop"
            obj.sel = obj.c
            obj.c = None
        # end if
        changes[key] = obj
    # end for
    #// Combine operations.
    if php_count(changes) > 1:
        filtered = Array(changes[0])
        i = 0
        j = 1
        c = php_count(changes)
        while j < c:
            
            combined = False
            if filtered[i].type == changes[j].type:
                for case in Switch(filtered[i].type):
                    if case("rotate"):
                        filtered[i].angle += changes[j].angle
                        combined = True
                        break
                    # end if
                    if case("flip"):
                        filtered[i].axis ^= changes[j].axis
                        combined = True
                        break
                    # end if
                # end for
            # end if
            if (not combined):
                i += 1
                filtered[i] = changes[j]
            # end if
            j += 1
        # end while
        changes = filtered
        filtered = None
    # end if
    #// Image resource before applying the changes.
    if type(image).__name__ == "WP_Image_Editor":
        #// 
        #// Filters the WP_Image_Editor instance before applying changes to the image.
        #// 
        #// @since 3.5.0
        #// 
        #// @param WP_Image_Editor $image   WP_Image_Editor instance.
        #// @param array           $changes Array of change operations.
        #//
        image = apply_filters("wp_image_editor_before_change", image, changes)
    elif is_resource(image):
        #// 
        #// Filters the GD image resource before applying changes to the image.
        #// 
        #// @since 2.9.0
        #// @deprecated 3.5.0 Use {@see 'wp_image_editor_before_change'} instead.
        #// 
        #// @param resource $image   GD image resource.
        #// @param array    $changes Array of change operations.
        #//
        image = apply_filters_deprecated("image_edit_before_change", Array(image, changes), "3.5.0", "wp_image_editor_before_change")
    # end if
    for operation in changes:
        for case in Switch(operation.type):
            if case("rotate"):
                if 0 != operation.angle:
                    if type(image).__name__ == "WP_Image_Editor":
                        image.rotate(operation.angle)
                    else:
                        image = _rotate_image_resource(image, operation.angle)
                    # end if
                # end if
                break
            # end if
            if case("flip"):
                if 0 != operation.axis:
                    if type(image).__name__ == "WP_Image_Editor":
                        image.flip(operation.axis & 1 != 0, operation.axis & 2 != 0)
                    else:
                        image = _flip_image_resource(image, operation.axis & 1 != 0, operation.axis & 2 != 0)
                    # end if
                # end if
                break
            # end if
            if case("crop"):
                sel = operation.sel
                if type(image).__name__ == "WP_Image_Editor":
                    size = image.get_size()
                    w = size["width"]
                    h = size["height"]
                    scale = 1 / _image_get_preview_ratio(w, h)
                    #// Discard preview scaling.
                    image.crop(sel.x * scale, sel.y * scale, sel.w * scale, sel.h * scale)
                else:
                    scale = 1 / _image_get_preview_ratio(imagesx(image), imagesy(image))
                    #// Discard preview scaling.
                    image = _crop_image_resource(image, sel.x * scale, sel.y * scale, sel.w * scale, sel.h * scale)
                # end if
                break
            # end if
        # end for
    # end for
    return image
# end def image_edit_apply_changes
#// 
#// Streams image in post to browser, along with enqueued changes
#// in `$_REQUEST['history']`.
#// 
#// @since 2.9.0
#// 
#// @param int $post_id Attachment post ID.
#// @return bool True on success, false on failure.
#//
def stream_preview_image(post_id=None, *args_):
    
    post = get_post(post_id)
    wp_raise_memory_limit("admin")
    img = wp_get_image_editor(_load_image_to_edit_path(post_id))
    if is_wp_error(img):
        return False
    # end if
    changes = php_json_decode(wp_unslash(PHP_REQUEST["history"])) if (not php_empty(lambda : PHP_REQUEST["history"])) else None
    if changes:
        img = image_edit_apply_changes(img, changes)
    # end if
    #// Scale the image.
    size = img.get_size()
    w = size["width"]
    h = size["height"]
    ratio = _image_get_preview_ratio(w, h)
    w2 = php_max(1, w * ratio)
    h2 = php_max(1, h * ratio)
    if is_wp_error(img.resize(w2, h2)):
        return False
    # end if
    return wp_stream_image(img, post.post_mime_type, post_id)
# end def stream_preview_image
#// 
#// Restores the metadata for a given attachment.
#// 
#// @since 2.9.0
#// 
#// @param int $post_id Attachment post ID.
#// @return stdClass Image restoration message object.
#//
def wp_restore_image(post_id=None, *args_):
    
    meta = wp_get_attachment_metadata(post_id)
    file = get_attached_file(post_id)
    backup_sizes = get_post_meta(post_id, "_wp_attachment_backup_sizes", True)
    old_backup_sizes = backup_sizes
    restored = False
    msg = php_new_class("stdClass", lambda : stdClass())
    if (not php_is_array(backup_sizes)):
        msg.error = __("Cannot load image metadata.")
        return msg
    # end if
    parts = pathinfo(file)
    suffix = time() + rand(100, 999)
    default_sizes = get_intermediate_image_sizes()
    if (php_isset(lambda : backup_sizes["full-orig"])) and php_is_array(backup_sizes["full-orig"]):
        data = backup_sizes["full-orig"]
        if parts["basename"] != data["file"]:
            if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE:
                #// Delete only if it's an edited image.
                if php_preg_match("/-e[0-9]{13}\\./", parts["basename"]):
                    wp_delete_file(file)
                # end if
            elif (php_isset(lambda : meta["width"]) and php_isset(lambda : meta["height"])):
                backup_sizes[str("full-") + str(suffix)] = Array({"width": meta["width"], "height": meta["height"], "file": parts["basename"]})
            # end if
        # end if
        restored_file = path_join(parts["dirname"], data["file"])
        restored = update_attached_file(post_id, restored_file)
        meta["file"] = _wp_relative_upload_path(restored_file)
        meta["width"] = data["width"]
        meta["height"] = data["height"]
    # end if
    for default_size in default_sizes:
        if (php_isset(lambda : backup_sizes[str(default_size) + str("-orig")])):
            data = backup_sizes[str(default_size) + str("-orig")]
            if (php_isset(lambda : meta["sizes"][default_size])) and meta["sizes"][default_size]["file"] != data["file"]:
                if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE:
                    #// Delete only if it's an edited image.
                    if php_preg_match("/-e[0-9]{13}-/", meta["sizes"][default_size]["file"]):
                        delete_file = path_join(parts["dirname"], meta["sizes"][default_size]["file"])
                        wp_delete_file(delete_file)
                    # end if
                else:
                    backup_sizes[str(default_size) + str("-") + str(suffix)] = meta["sizes"][default_size]
                # end if
            # end if
            meta["sizes"][default_size] = data
        else:
            meta["sizes"][default_size] = None
        # end if
    # end for
    if (not wp_update_attachment_metadata(post_id, meta)) or old_backup_sizes != backup_sizes and (not update_post_meta(post_id, "_wp_attachment_backup_sizes", backup_sizes)):
        msg.error = __("Cannot save image metadata.")
        return msg
    # end if
    if (not restored):
        msg.error = __("Image metadata is inconsistent.")
    else:
        msg.msg = __("Image restored successfully.")
    # end if
    return msg
# end def wp_restore_image
#// 
#// Saves image to post, along with enqueued changes
#// in `$_REQUEST['history']`.
#// 
#// @since 2.9.0
#// 
#// @param int $post_id Attachment post ID.
#// @return stdClass
#//
def wp_save_image(post_id=None, *args_):
    
    _wp_additional_image_sizes = wp_get_additional_image_sizes()
    return_ = php_new_class("stdClass", lambda : stdClass())
    success = False
    delete = False
    scaled = False
    nocrop = False
    post = get_post(post_id)
    img = wp_get_image_editor(_load_image_to_edit_path(post_id, "full"))
    if is_wp_error(img):
        return_.error = esc_js(__("Unable to create new image."))
        return return_
    # end if
    fwidth = php_intval(PHP_REQUEST["fwidth"]) if (not php_empty(lambda : PHP_REQUEST["fwidth"])) else 0
    fheight = php_intval(PHP_REQUEST["fheight"]) if (not php_empty(lambda : PHP_REQUEST["fheight"])) else 0
    target = php_preg_replace("/[^a-z0-9_-]+/i", "", PHP_REQUEST["target"]) if (not php_empty(lambda : PHP_REQUEST["target"])) else ""
    scale = (not php_empty(lambda : PHP_REQUEST["do"])) and "scale" == PHP_REQUEST["do"]
    if scale and fwidth > 0 and fheight > 0:
        size = img.get_size()
        sX = size["width"]
        sY = size["height"]
        #// Check if it has roughly the same w / h ratio.
        diff = round(sX / sY, 2) - round(fwidth / fheight, 2)
        if -0.1 < diff and diff < 0.1:
            #// Scale the full size image.
            if img.resize(fwidth, fheight):
                scaled = True
            # end if
        # end if
        if (not scaled):
            return_.error = esc_js(__("Error while saving the scaled image. Please reload the page and try again."))
            return return_
        # end if
    elif (not php_empty(lambda : PHP_REQUEST["history"])):
        changes = php_json_decode(wp_unslash(PHP_REQUEST["history"]))
        if changes:
            img = image_edit_apply_changes(img, changes)
        # end if
    else:
        return_.error = esc_js(__("Nothing to save, the image has not changed."))
        return return_
    # end if
    meta = wp_get_attachment_metadata(post_id)
    backup_sizes = get_post_meta(post.ID, "_wp_attachment_backup_sizes", True)
    if (not php_is_array(meta)):
        return_.error = esc_js(__("Image data does not exist. Please re-upload the image."))
        return return_
    # end if
    if (not php_is_array(backup_sizes)):
        backup_sizes = Array()
    # end if
    #// Generate new filename.
    path = get_attached_file(post_id)
    basename = pathinfo(path, PATHINFO_BASENAME)
    dirname = pathinfo(path, PATHINFO_DIRNAME)
    ext = pathinfo(path, PATHINFO_EXTENSION)
    filename = pathinfo(path, PATHINFO_FILENAME)
    suffix = time() + rand(100, 999)
    if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE and (php_isset(lambda : backup_sizes["full-orig"])) and backup_sizes["full-orig"]["file"] != basename:
        if "thumbnail" == target:
            new_path = str(dirname) + str("/") + str(filename) + str("-temp.") + str(ext)
        else:
            new_path = path
        # end if
    else:
        while True:
            
            if not (True):
                break
            # end if
            filename = php_preg_replace("/-e([0-9]+)$/", "", filename)
            filename += str("-e") + str(suffix)
            new_filename = str(filename) + str(".") + str(ext)
            new_path = str(dirname) + str("/") + str(new_filename)
            if php_file_exists(new_path):
                suffix += 1
            else:
                break
            # end if
        # end while
    # end if
    #// Save the full-size file, also needed to create sub-sizes.
    if (not wp_save_image_file(new_path, img, post.post_mime_type, post_id)):
        return_.error = esc_js(__("Unable to save the image."))
        return return_
    # end if
    if "nothumb" == target or "all" == target or "full" == target or scaled:
        tag = False
        if (php_isset(lambda : backup_sizes["full-orig"])):
            if (not php_defined("IMAGE_EDIT_OVERWRITE")) or (not IMAGE_EDIT_OVERWRITE) and backup_sizes["full-orig"]["file"] != basename:
                tag = str("full-") + str(suffix)
            # end if
        else:
            tag = "full-orig"
        # end if
        if tag:
            backup_sizes[tag] = Array({"width": meta["width"], "height": meta["height"], "file": basename})
        # end if
        success = path == new_path or update_attached_file(post_id, new_path)
        meta["file"] = _wp_relative_upload_path(new_path)
        size = img.get_size()
        meta["width"] = size["width"]
        meta["height"] = size["height"]
        if success and "nothumb" == target or "all" == target:
            sizes = get_intermediate_image_sizes()
            if "nothumb" == target:
                sizes = php_array_diff(sizes, Array("thumbnail"))
            # end if
        # end if
        return_.fw = meta["width"]
        return_.fh = meta["height"]
    elif "thumbnail" == target:
        sizes = Array("thumbnail")
        success = True
        delete = True
        nocrop = True
    # end if
    #// 
    #// We need to remove any existing resized image files because
    #// a new crop or rotate could generate different sizes (and hence, filenames),
    #// keeping the new resized images from overwriting the existing image files.
    #// https://core.trac.wordpress.org/ticket/32171
    #//
    if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE and (not php_empty(lambda : meta["sizes"])):
        for size in meta["sizes"]:
            if (not php_empty(lambda : size["file"])) and php_preg_match("/-e[0-9]{13}-/", size["file"]):
                delete_file = path_join(dirname, size["file"])
                wp_delete_file(delete_file)
            # end if
        # end for
    # end if
    if (php_isset(lambda : sizes)):
        _sizes = Array()
        for size in sizes:
            tag = False
            if (php_isset(lambda : meta["sizes"][size])):
                if (php_isset(lambda : backup_sizes[str(size) + str("-orig")])):
                    if (not php_defined("IMAGE_EDIT_OVERWRITE")) or (not IMAGE_EDIT_OVERWRITE) and backup_sizes[str(size) + str("-orig")]["file"] != meta["sizes"][size]["file"]:
                        tag = str(size) + str("-") + str(suffix)
                    # end if
                else:
                    tag = str(size) + str("-orig")
                # end if
                if tag:
                    backup_sizes[tag] = meta["sizes"][size]
                # end if
            # end if
            if (php_isset(lambda : _wp_additional_image_sizes[size])):
                width = php_intval(_wp_additional_image_sizes[size]["width"])
                height = php_intval(_wp_additional_image_sizes[size]["height"])
                crop = False if nocrop else _wp_additional_image_sizes[size]["crop"]
            else:
                height = get_option(str(size) + str("_size_h"))
                width = get_option(str(size) + str("_size_w"))
                crop = False if nocrop else get_option(str(size) + str("_crop"))
            # end if
            _sizes[size] = Array({"width": width, "height": height, "crop": crop})
        # end for
        meta["sizes"] = php_array_merge(meta["sizes"], img.multi_resize(_sizes))
    # end if
    img = None
    if success:
        wp_update_attachment_metadata(post_id, meta)
        update_post_meta(post_id, "_wp_attachment_backup_sizes", backup_sizes)
        if "thumbnail" == target or "all" == target or "full" == target:
            #// Check if it's an image edit from attachment edit screen.
            if (not php_empty(lambda : PHP_REQUEST["context"])) and "edit-attachment" == PHP_REQUEST["context"]:
                thumb_url = wp_get_attachment_image_src(post_id, Array(900, 600), True)
                return_.thumbnail = thumb_url[0]
            else:
                file_url = wp_get_attachment_url(post_id)
                if (not php_empty(lambda : meta["sizes"]["thumbnail"])):
                    thumb = meta["sizes"]["thumbnail"]
                    return_.thumbnail = path_join(php_dirname(file_url), thumb["file"])
                else:
                    return_.thumbnail = str(file_url) + str("?w=128&h=128")
                # end if
            # end if
        # end if
    else:
        delete = True
    # end if
    if delete:
        wp_delete_file(new_path)
    # end if
    return_.msg = esc_js(__("Image saved"))
    return return_
# end def wp_save_image
