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
def wp_image_editor(post_id_=None, msg_=None, *_args_):
    if msg_ is None:
        msg_ = False
    # end if
    
    nonce_ = wp_create_nonce(str("image_editor-") + str(post_id_))
    meta_ = wp_get_attachment_metadata(post_id_)
    thumb_ = image_get_intermediate_size(post_id_, "thumbnail")
    sub_sizes_ = (php_isset(lambda : meta_["sizes"])) and php_is_array(meta_["sizes"])
    note_ = ""
    if (php_isset(lambda : meta_["width"]) and php_isset(lambda : meta_["height"])):
        big_ = php_max(meta_["width"], meta_["height"])
    else:
        php_print(__("Image data does not exist. Please re-upload the image."))
        php_exit()
    # end if
    sizer_ = 400 / big_ if big_ > 400 else 1
    backup_sizes_ = get_post_meta(post_id_, "_wp_attachment_backup_sizes", True)
    can_restore_ = False
    if (not php_empty(lambda : backup_sizes_)) and (php_isset(lambda : backup_sizes_["full-orig"]) and php_isset(lambda : meta_["file"])):
        can_restore_ = wp_basename(meta_["file"]) != backup_sizes_["full-orig"]["file"]
    # end if
    if msg_:
        if (php_isset(lambda : msg_.error)):
            note_ = str("<div class='error'><p>") + str(msg_.error) + str("</p></div>")
        elif (php_isset(lambda : msg_.msg)):
            note_ = str("<div class='updated'><p>") + str(msg_.msg) + str("</p></div>")
        # end if
    # end if
    php_print(" <div class=\"imgedit-wrap wp-clearfix\">\n  <div id=\"imgedit-panel-")
    php_print(post_id_)
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
    if (php_isset(lambda : meta_["width"]) and php_isset(lambda : meta_["height"])):
        php_print("     <p>\n           ")
        printf(__("Original dimensions %s"), "<span class=\"imgedit-original-dimensions\">" + meta_["width"] + " &times; " + meta_["height"] + "</span>")
        php_print("     </p>\n      ")
    # end if
    php_print("""       <div class=\"imgedit-submit\">
    <fieldset class=\"imgedit-scale\">
    <legend>""")
    _e("New dimensions:")
    php_print("</legend>\n      <div class=\"nowrap\">\n        <label for=\"imgedit-scale-width-")
    php_print(post_id_)
    php_print("\" class=\"screen-reader-text\">")
    _e("scale width")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-scale-width-")
    php_print(post_id_)
    php_print("\" onkeyup=\"imageEdit.scaleChanged(")
    php_print(post_id_)
    php_print(", 1, this)\" onblur=\"imageEdit.scaleChanged(")
    php_print(post_id_)
    php_print(", 1, this)\" value=\"")
    php_print(meta_["width"] if (php_isset(lambda : meta_["width"])) else 0)
    php_print("\" />\n      <span class=\"imgedit-separator\" aria-hidden=\"true\">&times;</span>\n     <label for=\"imgedit-scale-height-")
    php_print(post_id_)
    php_print("\" class=\"screen-reader-text\">")
    _e("scale height")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-scale-height-")
    php_print(post_id_)
    php_print("\" onkeyup=\"imageEdit.scaleChanged(")
    php_print(post_id_)
    php_print(", 0, this)\" onblur=\"imageEdit.scaleChanged(")
    php_print(post_id_)
    php_print(", 0, this)\" value=\"")
    php_print(meta_["height"] if (php_isset(lambda : meta_["height"])) else 0)
    php_print("\" />\n      <span class=\"imgedit-scale-warn\" id=\"imgedit-scale-warn-")
    php_print(post_id_)
    php_print("\">!</span>\n        <div class=\"imgedit-scale-button-wrapper\"><input id=\"imgedit-scale-button\" type=\"button\" onclick=\"imageEdit.action(")
    php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
    php_print(", 'scale')\" class=\"button button-primary\" value=\"")
    esc_attr_e("Scale")
    php_print("""\" /></div>
    </div>
    </fieldset>
    </div>
    </div>
    </div>
    """)
    if can_restore_:
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
        php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
        php_print(", 'restore')\" class=\"button button-primary\" value=\"")
        esc_attr_e("Restore image")
        php_print("\" ")
        php_print(can_restore_)
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
    php_print(post_id_)
    php_print("\" class=\"screen-reader-text\">")
    _e("crop ratio width")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-crop-width-")
    php_print(post_id_)
    php_print("\" onkeyup=\"imageEdit.setRatioSelection(")
    php_print(post_id_)
    php_print(", 0, this)\" onblur=\"imageEdit.setRatioSelection(")
    php_print(post_id_)
    php_print(", 0, this)\" />\n        <span class=\"imgedit-separator\" aria-hidden=\"true\">:</span>\n       <label for=\"imgedit-crop-height-")
    php_print(post_id_)
    php_print("\" class=\"screen-reader-text\">")
    _e("crop ratio height")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-crop-height-")
    php_print(post_id_)
    php_print("\" onkeyup=\"imageEdit.setRatioSelection(")
    php_print(post_id_)
    php_print(", 1, this)\" onblur=\"imageEdit.setRatioSelection(")
    php_print(post_id_)
    php_print(""", 1, this)\" />
    </div>
    </fieldset>
    <fieldset id=\"imgedit-crop-sel-""")
    php_print(post_id_)
    php_print("\" class=\"imgedit-crop-sel\">\n     <legend>")
    _e("Selection:")
    php_print("</legend>\n      <div class=\"nowrap\">\n        <label for=\"imgedit-sel-width-")
    php_print(post_id_)
    php_print("\" class=\"screen-reader-text\">")
    _e("selection width")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-sel-width-")
    php_print(post_id_)
    php_print("\" onkeyup=\"imageEdit.setNumSelection(")
    php_print(post_id_)
    php_print(", this)\" onblur=\"imageEdit.setNumSelection(")
    php_print(post_id_)
    php_print(", this)\" />\n       <span class=\"imgedit-separator\" aria-hidden=\"true\">&times;</span>\n     <label for=\"imgedit-sel-height-")
    php_print(post_id_)
    php_print("\" class=\"screen-reader-text\">")
    _e("selection height")
    php_print("</label>\n       <input type=\"text\" id=\"imgedit-sel-height-")
    php_print(post_id_)
    php_print("\" onkeyup=\"imageEdit.setNumSelection(")
    php_print(post_id_)
    php_print(", this)\" onblur=\"imageEdit.setNumSelection(")
    php_print(post_id_)
    php_print(""", this)\" />
    </div>
    </fieldset>
    </div>
    """)
    if thumb_ and sub_sizes_:
        thumb_img_ = wp_constrain_dimensions(thumb_["width"], thumb_["height"], 160, 120)
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
        php_print(thumb_["url"])
        php_print("\" width=\"")
        php_print(thumb_img_[0])
        php_print("\" height=\"")
        php_print(thumb_img_[1])
        php_print("\" class=\"imgedit-size-preview\" alt=\"\" draggable=\"false\" />\n      <figcaption class=\"imgedit-thumbnail-preview-caption\">")
        _e("Current thumbnail")
        php_print("""</figcaption>
        </figure>
        <div id=\"imgedit-save-target-""")
        php_print(post_id_)
        php_print("\" class=\"imgedit-save-target\">\n  <fieldset>\n        <legend>")
        _e("Apply changes to:")
        php_print("""</legend>
        <span class=\"imgedit-label\">
        <input type=\"radio\" id=\"imgedit-target-all\" name=\"imgedit-target-""")
        php_print(post_id_)
        php_print("\" value=\"all\" checked=\"checked\" />\n            <label for=\"imgedit-target-all\">")
        _e("All image sizes")
        php_print("""</label>
        </span>
        <span class=\"imgedit-label\">
        <input type=\"radio\" id=\"imgedit-target-thumbnail\" name=\"imgedit-target-""")
        php_print(post_id_)
        php_print("\" value=\"thumbnail\" />\n          <label for=\"imgedit-target-thumbnail\">")
        _e("Thumbnail")
        php_print("""</label>
        </span>
        <span class=\"imgedit-label\">
        <input type=\"radio\" id=\"imgedit-target-nothumb\" name=\"imgedit-target-""")
        php_print(post_id_)
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
    php_print(note_)
    php_print("     <div class=\"imgedit-menu wp-clearfix\">\n          <button type=\"button\" onclick=\"imageEdit.handleCropToolClick( ")
    php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
    php_print(", this )\" class=\"imgedit-crop button disabled\" disabled>")
    esc_html_e("Crop")
    php_print("</button>\n          ")
    #// On some setups GD library does not provide imagerotate() - Ticket #11536.
    if wp_image_editor_supports(Array({"mime_type": get_post_mime_type(post_id_), "methods": Array("rotate")})):
        note_no_rotate_ = ""
        php_print("             <button type=\"button\" class=\"imgedit-rleft button\" onclick=\"imageEdit.rotate( 90, ")
        php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
        php_print(", this)\">")
        esc_html_e("Rotate left")
        php_print("</button>\n              <button type=\"button\" class=\"imgedit-rright button\" onclick=\"imageEdit.rotate(-90, ")
        php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
        php_print(", this)\">")
        esc_html_e("Rotate right")
        php_print("</button>\n              ")
    else:
        note_no_rotate_ = "<p class=\"note-no-rotate\"><em>" + __("Image rotation is not supported by your web host.") + "</em></p>"
        php_print("             <button type=\"button\" class=\"imgedit-rleft button disabled\" disabled></button>\n                <button type=\"button\" class=\"imgedit-rright button disabled\" disabled></button>\n           ")
    # end if
    php_print("\n           <button type=\"button\" onclick=\"imageEdit.flip(1, ")
    php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
    php_print(", this)\" class=\"imgedit-flipv button\">")
    esc_html_e("Flip vertical")
    php_print("</button>\n          <button type=\"button\" onclick=\"imageEdit.flip(2, ")
    php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
    php_print(", this)\" class=\"imgedit-fliph button\">")
    esc_html_e("Flip horizontal")
    php_print("""</button>
    <br class=\"imgedit-undo-redo-separator\" />
    <button type=\"button\" id=\"image-undo-""")
    php_print(post_id_)
    php_print("\" onclick=\"imageEdit.undo(")
    php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
    php_print(", this)\" class=\"imgedit-undo button disabled\" disabled>")
    esc_html_e("Undo")
    php_print("</button>\n          <button type=\"button\" id=\"image-redo-")
    php_print(post_id_)
    php_print("\" onclick=\"imageEdit.redo(")
    php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
    php_print(", this)\" class=\"imgedit-redo button disabled\" disabled>")
    esc_html_e("Redo")
    php_print("</button>\n          ")
    php_print(note_no_rotate_)
    php_print("     </div>\n\n      <input type=\"hidden\" id=\"imgedit-sizer-")
    php_print(post_id_)
    php_print("\" value=\"")
    php_print(sizer_)
    php_print("\" />\n      <input type=\"hidden\" id=\"imgedit-history-")
    php_print(post_id_)
    php_print("\" value=\"\" />\n       <input type=\"hidden\" id=\"imgedit-undone-")
    php_print(post_id_)
    php_print("\" value=\"0\" />\n      <input type=\"hidden\" id=\"imgedit-selection-")
    php_print(post_id_)
    php_print("\" value=\"\" />\n       <input type=\"hidden\" id=\"imgedit-x-")
    php_print(post_id_)
    php_print("\" value=\"")
    php_print(meta_["width"] if (php_isset(lambda : meta_["width"])) else 0)
    php_print("\" />\n      <input type=\"hidden\" id=\"imgedit-y-")
    php_print(post_id_)
    php_print("\" value=\"")
    php_print(meta_["height"] if (php_isset(lambda : meta_["height"])) else 0)
    php_print("\" />\n\n        <div id=\"imgedit-crop-")
    php_print(post_id_)
    php_print("\" class=\"imgedit-crop-wrap\">\n        <img id=\"image-preview-")
    php_print(post_id_)
    php_print("\" onload=\"imageEdit.imgLoaded('")
    php_print(post_id_)
    php_print("')\" src=\"")
    php_print(admin_url("admin-ajax.php", "relative"))
    php_print("?action=imgedit-preview&amp;_ajax_nonce=")
    php_print(nonce_)
    php_print("&amp;postid=")
    php_print(post_id_)
    php_print("&amp;rand=")
    php_print(rand(1, 99999))
    php_print("""\" alt=\"\" />
    </div>
    <div class=\"imgedit-submit\">
    <input type=\"button\" onclick=\"imageEdit.close(""")
    php_print(post_id_)
    php_print(", 1)\" class=\"button imgedit-cancel-btn\" value=\"")
    esc_attr_e("Cancel")
    php_print("\" />\n          <input type=\"button\" onclick=\"imageEdit.save(")
    php_print(str(post_id_) + str(", '") + str(nonce_) + str("'"))
    php_print(")\" disabled=\"disabled\" class=\"button button-primary imgedit-submit-btn\" value=\"")
    esc_attr_e("Save")
    php_print("""\" />
    </div>
    </div>
    </div>
    <div class=\"imgedit-wait\" id=\"imgedit-wait-""")
    php_print(post_id_)
    php_print("\"></div>\n  <div class=\"hidden\" id=\"imgedit-leaving-")
    php_print(post_id_)
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
def wp_stream_image(image_=None, mime_type_=None, attachment_id_=None, *_args_):
    
    
    if type(image_).__name__ == "WP_Image_Editor":
        #// 
        #// Filters the WP_Image_Editor instance for the image to be streamed to the browser.
        #// 
        #// @since 3.5.0
        #// 
        #// @param WP_Image_Editor $image         The image editor instance.
        #// @param int             $attachment_id The attachment post ID.
        #//
        image_ = apply_filters("image_editor_save_pre", image_, attachment_id_)
        if is_wp_error(image_.stream(mime_type_)):
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
        image_ = apply_filters_deprecated("image_save_pre", Array(image_, attachment_id_), "3.5.0", "image_editor_save_pre")
        for case in Switch(mime_type_):
            if case("image/jpeg"):
                php_header("Content-Type: image/jpeg")
                return imagejpeg(image_, None, 90)
            # end if
            if case("image/png"):
                php_header("Content-Type: image/png")
                return imagepng(image_)
            # end if
            if case("image/gif"):
                php_header("Content-Type: image/gif")
                return imagegif(image_)
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
def wp_save_image_file(filename_=None, image_=None, mime_type_=None, post_id_=None, *_args_):
    
    
    if type(image_).__name__ == "WP_Image_Editor":
        #// This filter is documented in wp-admin/includes/image-edit.php
        image_ = apply_filters("image_editor_save_pre", image_, post_id_)
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
        saved_ = apply_filters("wp_save_image_editor_file", None, filename_, image_, mime_type_, post_id_)
        if None != saved_:
            return saved_
        # end if
        return image_.save(filename_, mime_type_)
    else:
        #// translators: 1: $image, 2: WP_Image_Editor
        _deprecated_argument(__FUNCTION__, "3.5.0", php_sprintf(__("%1$s needs to be a %2$s object."), "$image", "WP_Image_Editor"))
        #// This filter is documented in wp-admin/includes/image-edit.php
        image_ = apply_filters_deprecated("image_save_pre", Array(image_, post_id_), "3.5.0", "image_editor_save_pre")
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
        saved_ = apply_filters_deprecated("wp_save_image_file", Array(None, filename_, image_, mime_type_, post_id_), "3.5.0", "wp_save_image_editor_file")
        if None != saved_:
            return saved_
        # end if
        for case in Switch(mime_type_):
            if case("image/jpeg"):
                #// This filter is documented in wp-includes/class-wp-image-editor.php
                return imagejpeg(image_, filename_, apply_filters("jpeg_quality", 90, "edit_image"))
            # end if
            if case("image/png"):
                return imagepng(image_, filename_)
            # end if
            if case("image/gif"):
                return imagegif(image_, filename_)
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
def _image_get_preview_ratio(w_=None, h_=None, *_args_):
    
    
    max_ = php_max(w_, h_)
    return 400 / max_ if max_ > 400 else 1
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
def _rotate_image_resource(img_=None, angle_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.5.0", "WP_Image_Editor::rotate()")
    if php_function_exists("imagerotate"):
        rotated_ = imagerotate(img_, angle_, 0)
        if is_resource(rotated_):
            imagedestroy(img_)
            img_ = rotated_
        # end if
    # end if
    return img_
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
def _flip_image_resource(img_=None, horz_=None, vert_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.5.0", "WP_Image_Editor::flip()")
    w_ = imagesx(img_)
    h_ = imagesy(img_)
    dst_ = wp_imagecreatetruecolor(w_, h_)
    if is_resource(dst_):
        sx_ = w_ - 1 if vert_ else 0
        sy_ = h_ - 1 if horz_ else 0
        sw_ = -w_ if vert_ else w_
        sh_ = -h_ if horz_ else h_
        if imagecopyresampled(dst_, img_, 0, 0, sx_, sy_, w_, h_, sw_, sh_):
            imagedestroy(img_)
            img_ = dst_
        # end if
    # end if
    return img_
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
def _crop_image_resource(img_=None, x_=None, y_=None, w_=None, h_=None, *_args_):
    
    
    dst_ = wp_imagecreatetruecolor(w_, h_)
    if is_resource(dst_):
        if imagecopy(dst_, img_, 0, 0, x_, y_, w_, h_):
            imagedestroy(img_)
            img_ = dst_
        # end if
    # end if
    return img_
# end def _crop_image_resource
i_ += 1
#// 
#// Performs group of changes on Editor specified.
#// 
#// @since 2.9.0
#// 
#// @param WP_Image_Editor $image   WP_Image_Editor instance.
#// @param array           $changes Array of change operations.
#// @return WP_Image_Editor WP_Image_Editor instance with changes applied.
#//
def image_edit_apply_changes(image_=None, changes_=None, *_args_):
    
    
    if is_resource(image_):
        #// translators: 1: $image, 2: WP_Image_Editor
        _deprecated_argument(__FUNCTION__, "3.5.0", php_sprintf(__("%1$s needs to be a %2$s object."), "$image", "WP_Image_Editor"))
    # end if
    if (not php_is_array(changes_)):
        return image_
    # end if
    #// Expand change operations.
    for key_,obj_ in changes_:
        if (php_isset(lambda : obj_.r)):
            obj_.type = "rotate"
            obj_.angle = obj_.r
            obj_.r = None
        elif (php_isset(lambda : obj_.f)):
            obj_.type = "flip"
            obj_.axis = obj_.f
            obj_.f = None
        elif (php_isset(lambda : obj_.c)):
            obj_.type = "crop"
            obj_.sel = obj_.c
            obj_.c = None
        # end if
        changes_[key_] = obj_
    # end for
    #// Combine operations.
    if php_count(changes_) > 1:
        filtered_ = Array(changes_[0])
        i_ = 0
        j_ = 1
        c_ = php_count(changes_)
        while j_ < c_:
            
            combined_ = False
            if filtered_[i_].type == changes_[j_].type:
                for case in Switch(filtered_[i_].type):
                    if case("rotate"):
                        filtered_[i_].angle += changes_[j_].angle
                        combined_ = True
                        break
                    # end if
                    if case("flip"):
                        filtered_[i_].axis ^= changes_[j_].axis
                        combined_ = True
                        break
                    # end if
                # end for
            # end if
            if (not combined_):
                i_ += 1
                filtered_[i_] = changes_[j_]
            # end if
            j_ += 1
        # end while
        changes_ = filtered_
        filtered_ = None
    # end if
    #// Image resource before applying the changes.
    if type(image_).__name__ == "WP_Image_Editor":
        #// 
        #// Filters the WP_Image_Editor instance before applying changes to the image.
        #// 
        #// @since 3.5.0
        #// 
        #// @param WP_Image_Editor $image   WP_Image_Editor instance.
        #// @param array           $changes Array of change operations.
        #//
        image_ = apply_filters("wp_image_editor_before_change", image_, changes_)
    elif is_resource(image_):
        #// 
        #// Filters the GD image resource before applying changes to the image.
        #// 
        #// @since 2.9.0
        #// @deprecated 3.5.0 Use {@see 'wp_image_editor_before_change'} instead.
        #// 
        #// @param resource $image   GD image resource.
        #// @param array    $changes Array of change operations.
        #//
        image_ = apply_filters_deprecated("image_edit_before_change", Array(image_, changes_), "3.5.0", "wp_image_editor_before_change")
    # end if
    for operation_ in changes_:
        for case in Switch(operation_.type):
            if case("rotate"):
                if 0 != operation_.angle:
                    if type(image_).__name__ == "WP_Image_Editor":
                        image_.rotate(operation_.angle)
                    else:
                        image_ = _rotate_image_resource(image_, operation_.angle)
                    # end if
                # end if
                break
            # end if
            if case("flip"):
                if 0 != operation_.axis:
                    if type(image_).__name__ == "WP_Image_Editor":
                        image_.flip(operation_.axis & 1 != 0, operation_.axis & 2 != 0)
                    else:
                        image_ = _flip_image_resource(image_, operation_.axis & 1 != 0, operation_.axis & 2 != 0)
                    # end if
                # end if
                break
            # end if
            if case("crop"):
                sel_ = operation_.sel
                if type(image_).__name__ == "WP_Image_Editor":
                    size_ = image_.get_size()
                    w_ = size_["width"]
                    h_ = size_["height"]
                    scale_ = 1 / _image_get_preview_ratio(w_, h_)
                    #// Discard preview scaling.
                    image_.crop(sel_.x * scale_, sel_.y * scale_, sel_.w * scale_, sel_.h * scale_)
                else:
                    scale_ = 1 / _image_get_preview_ratio(imagesx(image_), imagesy(image_))
                    #// Discard preview scaling.
                    image_ = _crop_image_resource(image_, sel_.x * scale_, sel_.y * scale_, sel_.w * scale_, sel_.h * scale_)
                # end if
                break
            # end if
        # end for
    # end for
    return image_
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
def stream_preview_image(post_id_=None, *_args_):
    
    
    post_ = get_post(post_id_)
    wp_raise_memory_limit("admin")
    img_ = wp_get_image_editor(_load_image_to_edit_path(post_id_))
    if is_wp_error(img_):
        return False
    # end if
    changes_ = php_json_decode(wp_unslash(PHP_REQUEST["history"])) if (not php_empty(lambda : PHP_REQUEST["history"])) else None
    if changes_:
        img_ = image_edit_apply_changes(img_, changes_)
    # end if
    #// Scale the image.
    size_ = img_.get_size()
    w_ = size_["width"]
    h_ = size_["height"]
    ratio_ = _image_get_preview_ratio(w_, h_)
    w2_ = php_max(1, w_ * ratio_)
    h2_ = php_max(1, h_ * ratio_)
    if is_wp_error(img_.resize(w2_, h2_)):
        return False
    # end if
    return wp_stream_image(img_, post_.post_mime_type, post_id_)
# end def stream_preview_image
#// 
#// Restores the metadata for a given attachment.
#// 
#// @since 2.9.0
#// 
#// @param int $post_id Attachment post ID.
#// @return stdClass Image restoration message object.
#//
def wp_restore_image(post_id_=None, *_args_):
    
    
    meta_ = wp_get_attachment_metadata(post_id_)
    file_ = get_attached_file(post_id_)
    backup_sizes_ = get_post_meta(post_id_, "_wp_attachment_backup_sizes", True)
    old_backup_sizes_ = backup_sizes_
    restored_ = False
    msg_ = php_new_class("stdClass", lambda : stdClass())
    if (not php_is_array(backup_sizes_)):
        msg_.error = __("Cannot load image metadata.")
        return msg_
    # end if
    parts_ = pathinfo(file_)
    suffix_ = time() + rand(100, 999)
    default_sizes_ = get_intermediate_image_sizes()
    if (php_isset(lambda : backup_sizes_["full-orig"])) and php_is_array(backup_sizes_["full-orig"]):
        data_ = backup_sizes_["full-orig"]
        if parts_["basename"] != data_["file"]:
            if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE:
                #// Delete only if it's an edited image.
                if php_preg_match("/-e[0-9]{13}\\./", parts_["basename"]):
                    wp_delete_file(file_)
                # end if
            elif (php_isset(lambda : meta_["width"]) and php_isset(lambda : meta_["height"])):
                backup_sizes_[str("full-") + str(suffix_)] = Array({"width": meta_["width"], "height": meta_["height"], "file": parts_["basename"]})
            # end if
        # end if
        restored_file_ = path_join(parts_["dirname"], data_["file"])
        restored_ = update_attached_file(post_id_, restored_file_)
        meta_["file"] = _wp_relative_upload_path(restored_file_)
        meta_["width"] = data_["width"]
        meta_["height"] = data_["height"]
    # end if
    for default_size_ in default_sizes_:
        if (php_isset(lambda : backup_sizes_[str(default_size_) + str("-orig")])):
            data_ = backup_sizes_[str(default_size_) + str("-orig")]
            if (php_isset(lambda : meta_["sizes"][default_size_])) and meta_["sizes"][default_size_]["file"] != data_["file"]:
                if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE:
                    #// Delete only if it's an edited image.
                    if php_preg_match("/-e[0-9]{13}-/", meta_["sizes"][default_size_]["file"]):
                        delete_file_ = path_join(parts_["dirname"], meta_["sizes"][default_size_]["file"])
                        wp_delete_file(delete_file_)
                    # end if
                else:
                    backup_sizes_[str(default_size_) + str("-") + str(suffix_)] = meta_["sizes"][default_size_]
                # end if
            # end if
            meta_["sizes"][default_size_] = data_
        else:
            meta_["sizes"][default_size_] = None
        # end if
    # end for
    if (not wp_update_attachment_metadata(post_id_, meta_)) or old_backup_sizes_ != backup_sizes_ and (not update_post_meta(post_id_, "_wp_attachment_backup_sizes", backup_sizes_)):
        msg_.error = __("Cannot save image metadata.")
        return msg_
    # end if
    if (not restored_):
        msg_.error = __("Image metadata is inconsistent.")
    else:
        msg_.msg = __("Image restored successfully.")
    # end if
    return msg_
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
def wp_save_image(post_id_=None, *_args_):
    
    
    _wp_additional_image_sizes_ = wp_get_additional_image_sizes()
    return_ = php_new_class("stdClass", lambda : stdClass())
    success_ = False
    delete_ = False
    scaled_ = False
    nocrop_ = False
    post_ = get_post(post_id_)
    img_ = wp_get_image_editor(_load_image_to_edit_path(post_id_, "full"))
    if is_wp_error(img_):
        return_.error = esc_js(__("Unable to create new image."))
        return return_
    # end if
    fwidth_ = php_intval(PHP_REQUEST["fwidth"]) if (not php_empty(lambda : PHP_REQUEST["fwidth"])) else 0
    fheight_ = php_intval(PHP_REQUEST["fheight"]) if (not php_empty(lambda : PHP_REQUEST["fheight"])) else 0
    target_ = php_preg_replace("/[^a-z0-9_-]+/i", "", PHP_REQUEST["target"]) if (not php_empty(lambda : PHP_REQUEST["target"])) else ""
    scale_ = (not php_empty(lambda : PHP_REQUEST["do"])) and "scale" == PHP_REQUEST["do"]
    if scale_ and fwidth_ > 0 and fheight_ > 0:
        size_ = img_.get_size()
        sX_ = size_["width"]
        sY_ = size_["height"]
        #// Check if it has roughly the same w / h ratio.
        diff_ = round(sX_ / sY_, 2) - round(fwidth_ / fheight_, 2)
        if -0.1 < diff_ and diff_ < 0.1:
            #// Scale the full size image.
            if img_.resize(fwidth_, fheight_):
                scaled_ = True
            # end if
        # end if
        if (not scaled_):
            return_.error = esc_js(__("Error while saving the scaled image. Please reload the page and try again."))
            return return_
        # end if
    elif (not php_empty(lambda : PHP_REQUEST["history"])):
        changes_ = php_json_decode(wp_unslash(PHP_REQUEST["history"]))
        if changes_:
            img_ = image_edit_apply_changes(img_, changes_)
        # end if
    else:
        return_.error = esc_js(__("Nothing to save, the image has not changed."))
        return return_
    # end if
    meta_ = wp_get_attachment_metadata(post_id_)
    backup_sizes_ = get_post_meta(post_.ID, "_wp_attachment_backup_sizes", True)
    if (not php_is_array(meta_)):
        return_.error = esc_js(__("Image data does not exist. Please re-upload the image."))
        return return_
    # end if
    if (not php_is_array(backup_sizes_)):
        backup_sizes_ = Array()
    # end if
    #// Generate new filename.
    path_ = get_attached_file(post_id_)
    basename_ = pathinfo(path_, PATHINFO_BASENAME)
    dirname_ = pathinfo(path_, PATHINFO_DIRNAME)
    ext_ = pathinfo(path_, PATHINFO_EXTENSION)
    filename_ = pathinfo(path_, PATHINFO_FILENAME)
    suffix_ = time() + rand(100, 999)
    if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE and (php_isset(lambda : backup_sizes_["full-orig"])) and backup_sizes_["full-orig"]["file"] != basename_:
        if "thumbnail" == target_:
            new_path_ = str(dirname_) + str("/") + str(filename_) + str("-temp.") + str(ext_)
        else:
            new_path_ = path_
        # end if
    else:
        while True:
            
            if not (True):
                break
            # end if
            filename_ = php_preg_replace("/-e([0-9]+)$/", "", filename_)
            filename_ += str("-e") + str(suffix_)
            new_filename_ = str(filename_) + str(".") + str(ext_)
            new_path_ = str(dirname_) + str("/") + str(new_filename_)
            if php_file_exists(new_path_):
                suffix_ += 1
            else:
                break
            # end if
        # end while
    # end if
    #// Save the full-size file, also needed to create sub-sizes.
    if (not wp_save_image_file(new_path_, img_, post_.post_mime_type, post_id_)):
        return_.error = esc_js(__("Unable to save the image."))
        return return_
    # end if
    if "nothumb" == target_ or "all" == target_ or "full" == target_ or scaled_:
        tag_ = False
        if (php_isset(lambda : backup_sizes_["full-orig"])):
            if (not php_defined("IMAGE_EDIT_OVERWRITE")) or (not IMAGE_EDIT_OVERWRITE) and backup_sizes_["full-orig"]["file"] != basename_:
                tag_ = str("full-") + str(suffix_)
            # end if
        else:
            tag_ = "full-orig"
        # end if
        if tag_:
            backup_sizes_[tag_] = Array({"width": meta_["width"], "height": meta_["height"], "file": basename_})
        # end if
        success_ = path_ == new_path_ or update_attached_file(post_id_, new_path_)
        meta_["file"] = _wp_relative_upload_path(new_path_)
        size_ = img_.get_size()
        meta_["width"] = size_["width"]
        meta_["height"] = size_["height"]
        if success_ and "nothumb" == target_ or "all" == target_:
            sizes_ = get_intermediate_image_sizes()
            if "nothumb" == target_:
                sizes_ = php_array_diff(sizes_, Array("thumbnail"))
            # end if
        # end if
        return_.fw = meta_["width"]
        return_.fh = meta_["height"]
    elif "thumbnail" == target_:
        sizes_ = Array("thumbnail")
        success_ = True
        delete_ = True
        nocrop_ = True
    # end if
    #// 
    #// We need to remove any existing resized image files because
    #// a new crop or rotate could generate different sizes (and hence, filenames),
    #// keeping the new resized images from overwriting the existing image files.
    #// https://core.trac.wordpress.org/ticket/32171
    #//
    if php_defined("IMAGE_EDIT_OVERWRITE") and IMAGE_EDIT_OVERWRITE and (not php_empty(lambda : meta_["sizes"])):
        for size_ in meta_["sizes"]:
            if (not php_empty(lambda : size_["file"])) and php_preg_match("/-e[0-9]{13}-/", size_["file"]):
                delete_file_ = path_join(dirname_, size_["file"])
                wp_delete_file(delete_file_)
            # end if
        # end for
    # end if
    if (php_isset(lambda : sizes_)):
        _sizes_ = Array()
        for size_ in sizes_:
            tag_ = False
            if (php_isset(lambda : meta_["sizes"][size_])):
                if (php_isset(lambda : backup_sizes_[str(size_) + str("-orig")])):
                    if (not php_defined("IMAGE_EDIT_OVERWRITE")) or (not IMAGE_EDIT_OVERWRITE) and backup_sizes_[str(size_) + str("-orig")]["file"] != meta_["sizes"][size_]["file"]:
                        tag_ = str(size_) + str("-") + str(suffix_)
                    # end if
                else:
                    tag_ = str(size_) + str("-orig")
                # end if
                if tag_:
                    backup_sizes_[tag_] = meta_["sizes"][size_]
                # end if
            # end if
            if (php_isset(lambda : _wp_additional_image_sizes_[size_])):
                width_ = php_intval(_wp_additional_image_sizes_[size_]["width"])
                height_ = php_intval(_wp_additional_image_sizes_[size_]["height"])
                crop_ = False if nocrop_ else _wp_additional_image_sizes_[size_]["crop"]
            else:
                height_ = get_option(str(size_) + str("_size_h"))
                width_ = get_option(str(size_) + str("_size_w"))
                crop_ = False if nocrop_ else get_option(str(size_) + str("_crop"))
            # end if
            _sizes_[size_] = Array({"width": width_, "height": height_, "crop": crop_})
        # end for
        meta_["sizes"] = php_array_merge(meta_["sizes"], img_.multi_resize(_sizes_))
    # end if
    img_ = None
    if success_:
        wp_update_attachment_metadata(post_id_, meta_)
        update_post_meta(post_id_, "_wp_attachment_backup_sizes", backup_sizes_)
        if "thumbnail" == target_ or "all" == target_ or "full" == target_:
            #// Check if it's an image edit from attachment edit screen.
            if (not php_empty(lambda : PHP_REQUEST["context"])) and "edit-attachment" == PHP_REQUEST["context"]:
                thumb_url_ = wp_get_attachment_image_src(post_id_, Array(900, 600), True)
                return_.thumbnail = thumb_url_[0]
            else:
                file_url_ = wp_get_attachment_url(post_id_)
                if (not php_empty(lambda : meta_["sizes"]["thumbnail"])):
                    thumb_ = meta_["sizes"]["thumbnail"]
                    return_.thumbnail = path_join(php_dirname(file_url_), thumb_["file"])
                else:
                    return_.thumbnail = str(file_url_) + str("?w=128&h=128")
                # end if
            # end if
        # end if
    else:
        delete_ = True
    # end if
    if delete_:
        wp_delete_file(new_path_)
    # end if
    return_.msg = esc_js(__("Image saved"))
    return return_
# end def wp_save_image
