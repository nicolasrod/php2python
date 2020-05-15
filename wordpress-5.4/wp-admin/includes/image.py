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
#// File contains all the administration image manipulation functions.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Crop an Image to a given size.
#// 
#// @since 2.1.0
#// 
#// @param string|int $src The source file or Attachment ID.
#// @param int $src_x The start x position to crop from.
#// @param int $src_y The start y position to crop from.
#// @param int $src_w The width to crop.
#// @param int $src_h The height to crop.
#// @param int $dst_w The destination width.
#// @param int $dst_h The destination height.
#// @param int $src_abs Optional. If the source crop points are absolute.
#// @param string $dst_file Optional. The destination file to write to.
#// @return string|WP_Error New filepath on success, WP_Error on failure.
#//
def wp_crop_image(src=None, src_x=None, src_y=None, src_w=None, src_h=None, dst_w=None, dst_h=None, src_abs=False, dst_file=False, *args_):
    
    src_file = src
    if php_is_numeric(src):
        #// Handle int as attachment ID.
        src_file = get_attached_file(src)
        if (not php_file_exists(src_file)):
            #// If the file doesn't exist, attempt a URL fopen on the src link.
            #// This can occur with certain file replication plugins.
            src = _load_image_to_edit_path(src, "full")
        else:
            src = src_file
        # end if
    # end if
    editor = wp_get_image_editor(src)
    if is_wp_error(editor):
        return editor
    # end if
    src = editor.crop(src_x, src_y, src_w, src_h, dst_w, dst_h, src_abs)
    if is_wp_error(src):
        return src
    # end if
    if (not dst_file):
        dst_file = php_str_replace(wp_basename(src_file), "cropped-" + wp_basename(src_file), src_file)
    # end if
    #// 
    #// The directory containing the original file may no longer exist when
    #// using a replication plugin.
    #//
    wp_mkdir_p(php_dirname(dst_file))
    dst_file = php_dirname(dst_file) + "/" + wp_unique_filename(php_dirname(dst_file), wp_basename(dst_file))
    result = editor.save(dst_file)
    if is_wp_error(result):
        return result
    # end if
    return dst_file
# end def wp_crop_image
#// 
#// Compare the existing image sub-sizes (as saved in the attachment meta)
#// to the currently registered image sub-sizes, and return the difference.
#// 
#// Registered sub-sizes that are larger than the image are skipped.
#// 
#// @since 5.3.0
#// 
#// @param int $attachment_id The image attachment post ID.
#// @return array An array of the image sub-sizes that are currently defined but don't exist for this image.
#//
def wp_get_missing_image_subsizes(attachment_id=None, *args_):
    
    if (not wp_attachment_is_image(attachment_id)):
        return Array()
    # end if
    registered_sizes = wp_get_registered_image_subsizes()
    image_meta = wp_get_attachment_metadata(attachment_id)
    #// Meta error?
    if php_empty(lambda : image_meta):
        return registered_sizes
    # end if
    #// Use the originally uploaded image dimensions as full_width and full_height.
    if (not php_empty(lambda : image_meta["original_image"])):
        image_file = wp_get_original_image_path(attachment_id)
        imagesize = php_no_error(lambda: getimagesize(image_file))
    # end if
    if (not php_empty(lambda : imagesize)):
        full_width = imagesize[0]
        full_height = imagesize[1]
    else:
        full_width = int(image_meta["width"])
        full_height = int(image_meta["height"])
    # end if
    possible_sizes = Array()
    #// Skip registered sizes that are too large for the uploaded image.
    for size_name,size_data in registered_sizes:
        if image_resize_dimensions(full_width, full_height, size_data["width"], size_data["height"], size_data["crop"]):
            possible_sizes[size_name] = size_data
        # end if
    # end for
    if php_empty(lambda : image_meta["sizes"]):
        image_meta["sizes"] = Array()
    # end if
    #// 
    #// Remove sizes that already exist. Only checks for matching "size names".
    #// It is possible that the dimensions for a particular size name have changed.
    #// For example the user has changed the values on the Settings -> Media screen.
    #// However we keep the old sub-sizes with the previous dimensions
    #// as the image may have been used in an older post.
    #//
    missing_sizes = php_array_diff_key(possible_sizes, image_meta["sizes"])
    #// 
    #// Filters the array of missing image sub-sizes for an uploaded image.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $missing_sizes Array with the missing image sub-sizes.
    #// @param array $image_meta    The image meta data.
    #// @param int   $attachment_id The image attachment post ID.
    #//
    return apply_filters("wp_get_missing_image_subsizes", missing_sizes, image_meta, attachment_id)
# end def wp_get_missing_image_subsizes
#// 
#// If any of the currently registered image sub-sizes are missing,
#// create them and update the image meta data.
#// 
#// @since 5.3.0
#// 
#// @param int $attachment_id The image attachment post ID.
#// @return array|WP_Error The updated image meta data array or WP_Error object
#// if both the image meta and the attached file are missing.
#//
def wp_update_image_subsizes(attachment_id=None, *args_):
    
    image_meta = wp_get_attachment_metadata(attachment_id)
    image_file = wp_get_original_image_path(attachment_id)
    if php_empty(lambda : image_meta) or (not php_is_array(image_meta)):
        #// Previously failed upload?
        #// If there is an uploaded file, make all sub-sizes and generate all of the attachment meta.
        if (not php_empty(lambda : image_file)):
            image_meta = wp_create_image_subsizes(image_file, attachment_id)
        else:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_attachment", __("The attached file cannot be found.")))
        # end if
    else:
        missing_sizes = wp_get_missing_image_subsizes(attachment_id)
        if php_empty(lambda : missing_sizes):
            return image_meta
        # end if
        #// This also updates the image meta.
        image_meta = _wp_make_subsizes(missing_sizes, image_file, image_meta, attachment_id)
    # end if
    #// This filter is documented in wp-admin/includes/image.php
    image_meta = apply_filters("wp_generate_attachment_metadata", image_meta, attachment_id, "update")
    #// Save the updated metadata.
    wp_update_attachment_metadata(attachment_id, image_meta)
    return image_meta
# end def wp_update_image_subsizes
#// 
#// Updates the attached file and image meta data when the original image was edited.
#// 
#// @since 5.3.0
#// @access private
#// 
#// @param array  $saved_data    The data returned from WP_Image_Editor after successfully saving an image.
#// @param string $original_file Path to the original file.
#// @param array  $image_meta    The image meta data.
#// @param int    $attachment_id The attachment post ID.
#// @return array The updated image meta data.
#//
def _wp_image_meta_replace_original(saved_data=None, original_file=None, image_meta=None, attachment_id=None, *args_):
    
    new_file = saved_data["path"]
    #// Update the attached file meta.
    update_attached_file(attachment_id, new_file)
    #// Width and height of the new image.
    image_meta["width"] = saved_data["width"]
    image_meta["height"] = saved_data["height"]
    #// Make the file path relative to the upload dir.
    image_meta["file"] = _wp_relative_upload_path(new_file)
    #// Store the original image file name in image_meta.
    image_meta["original_image"] = wp_basename(original_file)
    return image_meta
# end def _wp_image_meta_replace_original
#// 
#// Creates image sub-sizes, adds the new data to the image meta `sizes` array, and updates the image metadata.
#// 
#// Intended for use after an image is uploaded. Saves/updates the image metadata after each
#// sub-size is created. If there was an error, it is added to the returned image metadata array.
#// 
#// @since 5.3.0
#// 
#// @param string $file          Full path to the image file.
#// @param int    $attachment_id Attachment Id to process.
#// @return array The image attachment meta data.
#//
def wp_create_image_subsizes(file=None, attachment_id=None, *args_):
    
    imagesize = php_no_error(lambda: getimagesize(file))
    if php_empty(lambda : imagesize):
        #// File is not an image.
        return Array()
    # end if
    #// Default image meta.
    image_meta = Array({"width": imagesize[0], "height": imagesize[1], "file": _wp_relative_upload_path(file), "sizes": Array()})
    #// Fetch additional metadata from EXIF/IPTC.
    exif_meta = wp_read_image_metadata(file)
    if exif_meta:
        image_meta["image_meta"] = exif_meta
    # end if
    #// Do not scale (large) PNG images. May result in sub-sizes that have greater file size than the original. See #48736.
    if "image/png" != imagesize["mime"]:
        #// 
        #// Filters the "BIG image" threshold value.
        #// 
        #// If the original image width or height is above the threshold, it will be scaled down. The threshold is
        #// used as max width and max height. The scaled down image will be used as the largest available size, including
        #// the `_wp_attached_file` post meta value.
        #// 
        #// Returning `false` from the filter callback will disable the scaling.
        #// 
        #// @since 5.3.0
        #// 
        #// @param int    $threshold     The threshold value in pixels. Default 2560.
        #// @param array  $imagesize     {
        #// Indexed array of the image width and height in pixels.
        #// 
        #// @type int $0 The image width.
        #// @type int $1 The image height.
        #// }
        #// @param string $file          Full path to the uploaded image file.
        #// @param int    $attachment_id Attachment post ID.
        #//
        threshold = int(apply_filters("big_image_size_threshold", 2560, imagesize, file, attachment_id))
        #// If the original image's dimensions are over the threshold,
        #// scale the image and use it as the "full" size.
        if threshold and image_meta["width"] > threshold or image_meta["height"] > threshold:
            editor = wp_get_image_editor(file)
            if is_wp_error(editor):
                #// This image cannot be edited.
                return image_meta
            # end if
            #// Resize the image.
            resized = editor.resize(threshold, threshold)
            rotated = None
            #// If there is EXIF data, rotate according to EXIF Orientation.
            if (not is_wp_error(resized)) and php_is_array(exif_meta):
                resized = editor.maybe_exif_rotate()
                rotated = resized
            # end if
            if (not is_wp_error(resized)):
                #// Append "-scaled" to the image file name. It will look like "my_image-scaled.jpg".
                #// This doesn't affect the sub-sizes names as they are generated from the original image (for best quality).
                saved = editor.save(editor.generate_filename("scaled"))
                if (not is_wp_error(saved)):
                    image_meta = _wp_image_meta_replace_original(saved, file, image_meta, attachment_id)
                    #// If the image was rotated update the stored EXIF data.
                    if True == rotated and (not php_empty(lambda : image_meta["image_meta"]["orientation"])):
                        image_meta["image_meta"]["orientation"] = 1
                    # end if
                else:
                    pass
                # end if
            else:
                pass
            # end if
        elif (not php_empty(lambda : exif_meta["orientation"])) and 1 != int(exif_meta["orientation"]):
            #// Rotate the whole original image if there is EXIF data and "orientation" is not 1.
            editor = wp_get_image_editor(file)
            if is_wp_error(editor):
                #// This image cannot be edited.
                return image_meta
            # end if
            #// Rotate the image.
            rotated = editor.maybe_exif_rotate()
            if True == rotated:
                #// Append `-rotated` to the image file name.
                saved = editor.save(editor.generate_filename("rotated"))
                if (not is_wp_error(saved)):
                    image_meta = _wp_image_meta_replace_original(saved, file, image_meta, attachment_id)
                    #// Update the stored EXIF data.
                    if (not php_empty(lambda : image_meta["image_meta"]["orientation"])):
                        image_meta["image_meta"]["orientation"] = 1
                    # end if
                else:
                    pass
                # end if
            # end if
        # end if
    # end if
    #// 
    #// Initial save of the new metadata.
    #// At this point the file was uploaded and moved to the uploads directory
    #// but the image sub-sizes haven't been created yet and the `sizes` array is empty.
    #//
    wp_update_attachment_metadata(attachment_id, image_meta)
    new_sizes = wp_get_registered_image_subsizes()
    #// 
    #// Filters the image sizes automatically generated when uploading an image.
    #// 
    #// @since 2.9.0
    #// @since 4.4.0 Added the `$image_meta` argument.
    #// @since 5.3.0 Added the `$attachment_id` argument.
    #// 
    #// @param array $new_sizes     Associative array of image sizes to be created.
    #// @param array $image_meta    The image meta data: width, height, file, sizes, etc.
    #// @param int   $attachment_id The attachment post ID for the image.
    #//
    new_sizes = apply_filters("intermediate_image_sizes_advanced", new_sizes, image_meta, attachment_id)
    return _wp_make_subsizes(new_sizes, file, image_meta, attachment_id)
# end def wp_create_image_subsizes
#// 
#// Low-level function to create image sub-sizes.
#// 
#// Updates the image meta after each sub-size is created.
#// Errors are stored in the returned image metadata array.
#// 
#// @since 5.3.0
#// @access private
#// 
#// @param array  $new_sizes     Array defining what sizes to create.
#// @param string $file          Full path to the image file.
#// @param array  $image_meta    The attachment meta data array.
#// @param int    $attachment_id Attachment Id to process.
#// @return array The attachment meta data with updated `sizes` array. Includes an array of errors encountered while resizing.
#//
def _wp_make_subsizes(new_sizes=None, file=None, image_meta=None, attachment_id=None, *args_):
    
    if php_empty(lambda : image_meta) or (not php_is_array(image_meta)):
        #// Not an image attachment.
        return Array()
    # end if
    #// Check if any of the new sizes already exist.
    if (php_isset(lambda : image_meta["sizes"])) and php_is_array(image_meta["sizes"]):
        for size_name,size_meta in image_meta["sizes"]:
            #// 
            #// Only checks "size name" so we don't override existing images even if the dimensions
            #// don't match the currently defined size with the same name.
            #// To change the behavior, unset changed/mismatched sizes in the `sizes` array in image meta.
            #//
            if php_array_key_exists(size_name, new_sizes):
                new_sizes[size_name] = None
            # end if
        # end for
    else:
        image_meta["sizes"] = Array()
    # end if
    if php_empty(lambda : new_sizes):
        #// Nothing to do...
        return image_meta
    # end if
    #// 
    #// Sort the image sub-sizes in order of priority when creating them.
    #// This ensures there is an appropriate sub-size the user can access immediately
    #// even when there was an error and not all sub-sizes were created.
    #//
    priority = Array({"medium": None, "large": None, "thumbnail": None, "medium_large": None})
    new_sizes = php_array_filter(php_array_merge(priority, new_sizes))
    editor = wp_get_image_editor(file)
    if is_wp_error(editor):
        #// The image cannot be edited.
        return image_meta
    # end if
    #// If stored EXIF data exists, rotate the source image before creating sub-sizes.
    if (not php_empty(lambda : image_meta["image_meta"])):
        rotated = editor.maybe_exif_rotate()
        if is_wp_error(rotated):
            pass
        # end if
    # end if
    if php_method_exists(editor, "make_subsize"):
        for new_size_name,new_size_data in new_sizes:
            new_size_meta = editor.make_subsize(new_size_data)
            if is_wp_error(new_size_meta):
                pass
            else:
                #// Save the size meta value.
                image_meta["sizes"][new_size_name] = new_size_meta
                wp_update_attachment_metadata(attachment_id, image_meta)
            # end if
        # end for
    else:
        #// Fall back to `$editor->multi_resize()`.
        created_sizes = editor.multi_resize(new_sizes)
        if (not php_empty(lambda : created_sizes)):
            image_meta["sizes"] = php_array_merge(image_meta["sizes"], created_sizes)
            wp_update_attachment_metadata(attachment_id, image_meta)
        # end if
    # end if
    return image_meta
# end def _wp_make_subsizes
#// 
#// Generate attachment meta data and create image sub-sizes for images.
#// 
#// @since 2.1.0
#// 
#// @param int $attachment_id Attachment Id to process.
#// @param string $file Filepath of the Attached image.
#// @return mixed Metadata for attachment.
#//
def wp_generate_attachment_metadata(attachment_id=None, file=None, *args_):
    
    attachment = get_post(attachment_id)
    metadata = Array()
    support = False
    mime_type = get_post_mime_type(attachment)
    if php_preg_match("!^image/!", mime_type) and file_is_displayable_image(file):
        #// Make thumbnails and other intermediate sizes.
        metadata = wp_create_image_subsizes(file, attachment_id)
    elif wp_attachment_is("video", attachment):
        metadata = wp_read_video_metadata(file)
        support = current_theme_supports("post-thumbnails", "attachment:video") or post_type_supports("attachment:video", "thumbnail")
    elif wp_attachment_is("audio", attachment):
        metadata = wp_read_audio_metadata(file)
        support = current_theme_supports("post-thumbnails", "attachment:audio") or post_type_supports("attachment:audio", "thumbnail")
    # end if
    if support and (not php_empty(lambda : metadata["image"]["data"])):
        #// Check for existing cover.
        hash = php_md5(metadata["image"]["data"])
        posts = get_posts(Array({"fields": "ids", "post_type": "attachment", "post_mime_type": metadata["image"]["mime"], "post_status": "inherit", "posts_per_page": 1, "meta_key": "_cover_hash", "meta_value": hash}))
        exists = reset(posts)
        if (not php_empty(lambda : exists)):
            update_post_meta(attachment_id, "_thumbnail_id", exists)
        else:
            ext = ".jpg"
            for case in Switch(metadata["image"]["mime"]):
                if case("image/gif"):
                    ext = ".gif"
                    break
                # end if
                if case("image/png"):
                    ext = ".png"
                    break
                # end if
            # end for
            basename = php_str_replace(".", "-", wp_basename(file)) + "-image" + ext
            uploaded = wp_upload_bits(basename, "", metadata["image"]["data"])
            if False == uploaded["error"]:
                image_attachment = Array({"post_mime_type": metadata["image"]["mime"], "post_type": "attachment", "post_content": ""})
                #// 
                #// Filters the parameters for the attachment thumbnail creation.
                #// 
                #// @since 3.9.0
                #// 
                #// @param array $image_attachment An array of parameters to create the thumbnail.
                #// @param array $metadata         Current attachment metadata.
                #// @param array $uploaded         An array containing the thumbnail path and url.
                #//
                image_attachment = apply_filters("attachment_thumbnail_args", image_attachment, metadata, uploaded)
                sub_attachment_id = wp_insert_attachment(image_attachment, uploaded["file"])
                add_post_meta(sub_attachment_id, "_cover_hash", hash)
                attach_data = wp_generate_attachment_metadata(sub_attachment_id, uploaded["file"])
                wp_update_attachment_metadata(sub_attachment_id, attach_data)
                update_post_meta(attachment_id, "_thumbnail_id", sub_attachment_id)
            # end if
        # end if
    elif "application/pdf" == mime_type:
        #// Try to create image thumbnails for PDFs.
        fallback_sizes = Array("thumbnail", "medium", "large")
        #// 
        #// Filters the image sizes generated for non-image mime types.
        #// 
        #// @since 4.7.0
        #// 
        #// @param string[] $fallback_sizes An array of image size names.
        #// @param array    $metadata       Current attachment metadata.
        #//
        fallback_sizes = apply_filters("fallback_intermediate_image_sizes", fallback_sizes, metadata)
        registered_sizes = wp_get_registered_image_subsizes()
        merged_sizes = php_array_intersect_key(registered_sizes, php_array_flip(fallback_sizes))
        #// Force thumbnails to be soft crops.
        if (php_isset(lambda : merged_sizes["thumbnail"])) and php_is_array(merged_sizes["thumbnail"]):
            merged_sizes["thumbnail"]["crop"] = False
        # end if
        #// Only load PDFs in an image editor if we're processing sizes.
        if (not php_empty(lambda : merged_sizes)):
            editor = wp_get_image_editor(file)
            if (not is_wp_error(editor)):
                #// No support for this type of file.
                #// 
                #// PDFs may have the same file filename as JPEGs.
                #// Ensure the PDF preview image does not overwrite any JPEG images that already exist.
                #//
                dirname = php_dirname(file) + "/"
                ext = "." + pathinfo(file, PATHINFO_EXTENSION)
                preview_file = dirname + wp_unique_filename(dirname, wp_basename(file, ext) + "-pdf.jpg")
                uploaded = editor.save(preview_file, "image/jpeg")
                editor = None
                #// Resize based on the full size image, rather than the source.
                if (not is_wp_error(uploaded)):
                    image_file = uploaded["path"]
                    uploaded["path"] = None
                    metadata["sizes"] = Array({"full": uploaded})
                    #// Save the meta data before any image post-processing errors could happen.
                    wp_update_attachment_metadata(attachment_id, metadata)
                    #// Create sub-sizes saving the image meta after each.
                    metadata = _wp_make_subsizes(merged_sizes, image_file, metadata, attachment_id)
                # end if
            # end if
        # end if
    # end if
    #// Remove the blob of binary data from the array.
    if metadata:
        metadata["image"]["data"] = None
    # end if
    #// 
    #// Filters the generated attachment meta data.
    #// 
    #// @since 2.1.0
    #// @since 5.3.0 The `$context` parameter was added.
    #// 
    #// @param array  $metadata      An array of attachment meta data.
    #// @param int    $attachment_id Current attachment ID.
    #// @param string $context       Additional context. Can be 'create' when metadata was initially created for new attachment
    #// or 'update' when the metadata was updated.
    #//
    return apply_filters("wp_generate_attachment_metadata", metadata, attachment_id, "create")
# end def wp_generate_attachment_metadata
#// 
#// Convert a fraction string to a decimal.
#// 
#// @since 2.5.0
#// 
#// @param string $str
#// @return int|float
#//
def wp_exif_frac2dec(str=None, *args_):
    
    if False == php_strpos(str, "/"):
        return str
    # end if
    numerator, denominator = php_explode("/", str)
    if (not php_empty(lambda : denominator)):
        return numerator / denominator
    # end if
    return str
# end def wp_exif_frac2dec
#// 
#// Convert the exif date format to a unix timestamp.
#// 
#// @since 2.5.0
#// 
#// @param string $str
#// @return int
#//
def wp_exif_date2ts(str=None, *args_):
    
    date, time = php_explode(" ", php_trim(str))
    y, m, d = php_explode(":", date)
    return strtotime(str(y) + str("-") + str(m) + str("-") + str(d) + str(" ") + str(time))
# end def wp_exif_date2ts
#// 
#// Get extended image metadata, exif or iptc as available.
#// 
#// Retrieves the EXIF metadata aperture, credit, camera, caption, copyright, iso
#// created_timestamp, focal_length, shutter_speed, and title.
#// 
#// The IPTC metadata that is retrieved is APP13, credit, byline, created date
#// and time, caption, copyright, and title. Also includes FNumber, Model,
#// DateTimeDigitized, FocalLength, ISOSpeedRatings, and ExposureTime.
#// 
#// @todo Try other exif libraries if available.
#// @since 2.5.0
#// 
#// @param string $file
#// @return bool|array False on failure. Image metadata array on success.
#//
def wp_read_image_metadata(file=None, *args_):
    
    if (not php_file_exists(file)):
        return False
    # end if
    image_type = php_no_error(lambda: getimagesize(file))
    #// 
    #// EXIF contains a bunch of data we'll probably never need formatted in ways
    #// that are difficult to use. We'll normalize it and just extract the fields
    #// that are likely to be useful. Fractions and numbers are converted to
    #// floats, dates to unix timestamps, and everything else to strings.
    #//
    meta = Array({"aperture": 0, "credit": "", "camera": "", "caption": "", "created_timestamp": 0, "copyright": "", "focal_length": 0, "iso": 0, "shutter_speed": 0, "title": "", "orientation": 0, "keywords": Array()})
    iptc = Array()
    #// 
    #// Read IPTC first, since it might contain data not available in exif such
    #// as caption, description etc.
    #//
    if php_is_callable("iptcparse"):
        php_no_error(lambda: getimagesize(file, info))
        if (not php_empty(lambda : info["APP13"])):
            iptc = php_no_error(lambda: iptcparse(info["APP13"]))
            #// Headline, "A brief synopsis of the caption".
            if (not php_empty(lambda : iptc["2#105"][0])):
                meta["title"] = php_trim(iptc["2#105"][0])
                pass
            elif (not php_empty(lambda : iptc["2#005"][0])):
                meta["title"] = php_trim(iptc["2#005"][0])
            # end if
            if (not php_empty(lambda : iptc["2#120"][0])):
                #// Description / legacy caption.
                caption = php_trim(iptc["2#120"][0])
                mbstring_binary_safe_encoding()
                caption_length = php_strlen(caption)
                reset_mbstring_encoding()
                if php_empty(lambda : meta["title"]) and caption_length < 80:
                    #// Assume the title is stored in 2:120 if it's short.
                    meta["title"] = caption
                # end if
                meta["caption"] = caption
            # end if
            if (not php_empty(lambda : iptc["2#110"][0])):
                #// Credit.
                meta["credit"] = php_trim(iptc["2#110"][0])
            elif (not php_empty(lambda : iptc["2#080"][0])):
                #// Creator / legacy byline.
                meta["credit"] = php_trim(iptc["2#080"][0])
            # end if
            if (not php_empty(lambda : iptc["2#055"][0])) and (not php_empty(lambda : iptc["2#060"][0])):
                #// Created date and time.
                meta["created_timestamp"] = strtotime(iptc["2#055"][0] + " " + iptc["2#060"][0])
            # end if
            if (not php_empty(lambda : iptc["2#116"][0])):
                #// Copyright.
                meta["copyright"] = php_trim(iptc["2#116"][0])
            # end if
            if (not php_empty(lambda : iptc["2#025"][0])):
                #// Keywords array.
                meta["keywords"] = php_array_values(iptc["2#025"])
            # end if
        # end if
    # end if
    exif = Array()
    #// 
    #// Filters the image types to check for exif data.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $image_types Image types to check for exif data.
    #//
    exif_image_types = apply_filters("wp_read_image_metadata_types", Array(IMAGETYPE_JPEG, IMAGETYPE_TIFF_II, IMAGETYPE_TIFF_MM))
    if php_is_callable("exif_read_data") and php_in_array(image_type, exif_image_types, True):
        exif = php_no_error(lambda: exif_read_data(file))
        if (not php_empty(lambda : exif["ImageDescription"])):
            mbstring_binary_safe_encoding()
            description_length = php_strlen(exif["ImageDescription"])
            reset_mbstring_encoding()
            if php_empty(lambda : meta["title"]) and description_length < 80:
                #// Assume the title is stored in ImageDescription.
                meta["title"] = php_trim(exif["ImageDescription"])
            # end if
            if php_empty(lambda : meta["caption"]) and (not php_empty(lambda : exif["COMPUTED"]["UserComment"])):
                meta["caption"] = php_trim(exif["COMPUTED"]["UserComment"])
            # end if
            if php_empty(lambda : meta["caption"]):
                meta["caption"] = php_trim(exif["ImageDescription"])
            # end if
        elif php_empty(lambda : meta["caption"]) and (not php_empty(lambda : exif["Comments"])):
            meta["caption"] = php_trim(exif["Comments"])
        # end if
        if php_empty(lambda : meta["credit"]):
            if (not php_empty(lambda : exif["Artist"])):
                meta["credit"] = php_trim(exif["Artist"])
            elif (not php_empty(lambda : exif["Author"])):
                meta["credit"] = php_trim(exif["Author"])
            # end if
        # end if
        if php_empty(lambda : meta["copyright"]) and (not php_empty(lambda : exif["Copyright"])):
            meta["copyright"] = php_trim(exif["Copyright"])
        # end if
        if (not php_empty(lambda : exif["FNumber"])):
            meta["aperture"] = round(wp_exif_frac2dec(exif["FNumber"]), 2)
        # end if
        if (not php_empty(lambda : exif["Model"])):
            meta["camera"] = php_trim(exif["Model"])
        # end if
        if php_empty(lambda : meta["created_timestamp"]) and (not php_empty(lambda : exif["DateTimeDigitized"])):
            meta["created_timestamp"] = wp_exif_date2ts(exif["DateTimeDigitized"])
        # end if
        if (not php_empty(lambda : exif["FocalLength"])):
            meta["focal_length"] = str(wp_exif_frac2dec(exif["FocalLength"]))
        # end if
        if (not php_empty(lambda : exif["ISOSpeedRatings"])):
            meta["iso"] = reset(exif["ISOSpeedRatings"]) if php_is_array(exif["ISOSpeedRatings"]) else exif["ISOSpeedRatings"]
            meta["iso"] = php_trim(meta["iso"])
        # end if
        if (not php_empty(lambda : exif["ExposureTime"])):
            meta["shutter_speed"] = str(wp_exif_frac2dec(exif["ExposureTime"]))
        # end if
        if (not php_empty(lambda : exif["Orientation"])):
            meta["orientation"] = exif["Orientation"]
        # end if
    # end if
    for key in Array("title", "caption", "credit", "copyright", "camera", "iso"):
        if meta[key] and (not seems_utf8(meta[key])):
            meta[key] = utf8_encode(meta[key])
        # end if
    # end for
    for key,keyword in meta["keywords"]:
        if (not seems_utf8(keyword)):
            meta["keywords"][key] = utf8_encode(keyword)
        # end if
    # end for
    meta = wp_kses_post_deep(meta)
    #// 
    #// Filters the array of meta data read from an image's exif data.
    #// 
    #// @since 2.5.0
    #// @since 4.4.0 The `$iptc` parameter was added.
    #// @since 5.0.0 The `$exif` parameter was added.
    #// 
    #// @param array  $meta       Image meta data.
    #// @param string $file       Path to image file.
    #// @param int    $image_type Type of image, one of the `IMAGETYPE_XXX` constants.
    #// @param array  $iptc       IPTC data.
    #// @param array  $exif       EXIF data.
    #//
    return apply_filters("wp_read_image_metadata", meta, file, image_type, iptc, exif)
# end def wp_read_image_metadata
#// 
#// Validate that file is an image.
#// 
#// @since 2.5.0
#// 
#// @param string $path File path to test if valid image.
#// @return bool True if valid image, false if not valid image.
#//
def file_is_valid_image(path=None, *args_):
    
    size = php_no_error(lambda: getimagesize(path))
    return (not php_empty(lambda : size))
# end def file_is_valid_image
#// 
#// Validate that file is suitable for displaying within a web page.
#// 
#// @since 2.5.0
#// 
#// @param string $path File path to test.
#// @return bool True if suitable, false if not suitable.
#//
def file_is_displayable_image(path=None, *args_):
    
    displayable_image_types = Array(IMAGETYPE_GIF, IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_BMP, IMAGETYPE_ICO)
    info = php_no_error(lambda: getimagesize(path))
    if php_empty(lambda : info):
        result = False
    elif (not php_in_array(info[2], displayable_image_types, True)):
        result = False
    else:
        result = True
    # end if
    #// 
    #// Filters whether the current image is displayable in the browser.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool   $result Whether the image can be displayed. Default true.
    #// @param string $path   Path to the image.
    #//
    return apply_filters("file_is_displayable_image", result, path)
# end def file_is_displayable_image
#// 
#// Load an image resource for editing.
#// 
#// @since 2.9.0
#// 
#// @param string $attachment_id Attachment ID.
#// @param string $mime_type Image mime type.
#// @param string $size Optional. Image size, defaults to 'full'.
#// @return resource|false The resulting image resource on success, false on failure.
#//
def load_image_to_edit(attachment_id=None, mime_type=None, size="full", *args_):
    
    filepath = _load_image_to_edit_path(attachment_id, size)
    if php_empty(lambda : filepath):
        return False
    # end if
    for case in Switch(mime_type):
        if case("image/jpeg"):
            image = imagecreatefromjpeg(filepath)
            break
        # end if
        if case("image/png"):
            image = imagecreatefrompng(filepath)
            break
        # end if
        if case("image/gif"):
            image = imagecreatefromgif(filepath)
            break
        # end if
        if case():
            image = False
            break
        # end if
    # end for
    if is_resource(image):
        #// 
        #// Filters the current image being loaded for editing.
        #// 
        #// @since 2.9.0
        #// 
        #// @param resource $image         Current image.
        #// @param string   $attachment_id Attachment ID.
        #// @param string   $size          Image size.
        #//
        image = apply_filters("load_image_to_edit", image, attachment_id, size)
        if php_function_exists("imagealphablending") and php_function_exists("imagesavealpha"):
            imagealphablending(image, False)
            imagesavealpha(image, True)
        # end if
    # end if
    return image
# end def load_image_to_edit
#// 
#// Retrieve the path or url of an attachment's attached file.
#// 
#// If the attached file is not present on the local filesystem (usually due to replication plugins),
#// then the url of the file is returned if url fopen is supported.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @param string $attachment_id Attachment ID.
#// @param string $size Optional. Image size, defaults to 'full'.
#// @return string|false File path or url on success, false on failure.
#//
def _load_image_to_edit_path(attachment_id=None, size="full", *args_):
    
    filepath = get_attached_file(attachment_id)
    if filepath and php_file_exists(filepath):
        if "full" != size:
            data = image_get_intermediate_size(attachment_id, size)
            if data:
                filepath = path_join(php_dirname(filepath), data["file"])
                #// 
                #// Filters the path to the current image.
                #// 
                #// The filter is evaluated for all image sizes except 'full'.
                #// 
                #// @since 3.1.0
                #// 
                #// @param string $path          Path to the current image.
                #// @param string $attachment_id Attachment ID.
                #// @param string $size          Size of the image.
                #//
                filepath = apply_filters("load_image_to_edit_filesystempath", filepath, attachment_id, size)
            # end if
        # end if
    elif php_function_exists("fopen") and php_ini_get("allow_url_fopen"):
        #// 
        #// Filters the image URL if not in the local filesystem.
        #// 
        #// The filter is only evaluated if fopen is enabled on the server.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $image_url     Current image URL.
        #// @param string $attachment_id Attachment ID.
        #// @param string $size          Size of the image.
        #//
        filepath = apply_filters("load_image_to_edit_attachmenturl", wp_get_attachment_url(attachment_id), attachment_id, size)
    # end if
    #// 
    #// Filters the returned path or URL of the current image.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string|bool $filepath      File path or URL to current image, or false.
    #// @param string      $attachment_id Attachment ID.
    #// @param string      $size          Size of the image.
    #//
    return apply_filters("load_image_to_edit_path", filepath, attachment_id, size)
# end def _load_image_to_edit_path
#// 
#// Copy an existing image file.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @param string $attachment_id Attachment ID.
#// @return string|false New file path on success, false on failure.
#//
def _copy_image_file(attachment_id=None, *args_):
    
    dst_file = get_attached_file(attachment_id)
    src_file = dst_file
    if (not php_file_exists(src_file)):
        src_file = _load_image_to_edit_path(attachment_id)
    # end if
    if src_file:
        dst_file = php_str_replace(wp_basename(dst_file), "copy-" + wp_basename(dst_file), dst_file)
        dst_file = php_dirname(dst_file) + "/" + wp_unique_filename(php_dirname(dst_file), wp_basename(dst_file))
        #// 
        #// The directory containing the original file may no longer
        #// exist when using a replication plugin.
        #//
        wp_mkdir_p(php_dirname(dst_file))
        if (not copy(src_file, dst_file)):
            dst_file = False
        # end if
    else:
        dst_file = False
    # end if
    return dst_file
# end def _copy_image_file
