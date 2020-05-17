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
def wp_crop_image(src_=None, src_x_=None, src_y_=None, src_w_=None, src_h_=None, dst_w_=None, dst_h_=None, src_abs_=None, dst_file_=None, *_args_):
    if src_abs_ is None:
        src_abs_ = False
    # end if
    if dst_file_ is None:
        dst_file_ = False
    # end if
    
    src_file_ = src_
    if php_is_numeric(src_):
        #// Handle int as attachment ID.
        src_file_ = get_attached_file(src_)
        if (not php_file_exists(src_file_)):
            #// If the file doesn't exist, attempt a URL fopen on the src link.
            #// This can occur with certain file replication plugins.
            src_ = _load_image_to_edit_path(src_, "full")
        else:
            src_ = src_file_
        # end if
    # end if
    editor_ = wp_get_image_editor(src_)
    if is_wp_error(editor_):
        return editor_
    # end if
    src_ = editor_.crop(src_x_, src_y_, src_w_, src_h_, dst_w_, dst_h_, src_abs_)
    if is_wp_error(src_):
        return src_
    # end if
    if (not dst_file_):
        dst_file_ = php_str_replace(wp_basename(src_file_), "cropped-" + wp_basename(src_file_), src_file_)
    # end if
    #// 
    #// The directory containing the original file may no longer exist when
    #// using a replication plugin.
    #//
    wp_mkdir_p(php_dirname(dst_file_))
    dst_file_ = php_dirname(dst_file_) + "/" + wp_unique_filename(php_dirname(dst_file_), wp_basename(dst_file_))
    result_ = editor_.save(dst_file_)
    if is_wp_error(result_):
        return result_
    # end if
    return dst_file_
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
def wp_get_missing_image_subsizes(attachment_id_=None, *_args_):
    
    
    if (not wp_attachment_is_image(attachment_id_)):
        return Array()
    # end if
    registered_sizes_ = wp_get_registered_image_subsizes()
    image_meta_ = wp_get_attachment_metadata(attachment_id_)
    #// Meta error?
    if php_empty(lambda : image_meta_):
        return registered_sizes_
    # end if
    #// Use the originally uploaded image dimensions as full_width and full_height.
    if (not php_empty(lambda : image_meta_["original_image"])):
        image_file_ = wp_get_original_image_path(attachment_id_)
        imagesize_ = php_no_error(lambda: getimagesize(image_file_))
    # end if
    if (not php_empty(lambda : imagesize_)):
        full_width_ = imagesize_[0]
        full_height_ = imagesize_[1]
    else:
        full_width_ = php_int(image_meta_["width"])
        full_height_ = php_int(image_meta_["height"])
    # end if
    possible_sizes_ = Array()
    #// Skip registered sizes that are too large for the uploaded image.
    for size_name_,size_data_ in registered_sizes_:
        if image_resize_dimensions(full_width_, full_height_, size_data_["width"], size_data_["height"], size_data_["crop"]):
            possible_sizes_[size_name_] = size_data_
        # end if
    # end for
    if php_empty(lambda : image_meta_["sizes"]):
        image_meta_["sizes"] = Array()
    # end if
    #// 
    #// Remove sizes that already exist. Only checks for matching "size names".
    #// It is possible that the dimensions for a particular size name have changed.
    #// For example the user has changed the values on the Settings -> Media screen.
    #// However we keep the old sub-sizes with the previous dimensions
    #// as the image may have been used in an older post.
    #//
    missing_sizes_ = php_array_diff_key(possible_sizes_, image_meta_["sizes"])
    #// 
    #// Filters the array of missing image sub-sizes for an uploaded image.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $missing_sizes Array with the missing image sub-sizes.
    #// @param array $image_meta    The image meta data.
    #// @param int   $attachment_id The image attachment post ID.
    #//
    return apply_filters("wp_get_missing_image_subsizes", missing_sizes_, image_meta_, attachment_id_)
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
def wp_update_image_subsizes(attachment_id_=None, *_args_):
    
    
    image_meta_ = wp_get_attachment_metadata(attachment_id_)
    image_file_ = wp_get_original_image_path(attachment_id_)
    if php_empty(lambda : image_meta_) or (not php_is_array(image_meta_)):
        #// Previously failed upload?
        #// If there is an uploaded file, make all sub-sizes and generate all of the attachment meta.
        if (not php_empty(lambda : image_file_)):
            image_meta_ = wp_create_image_subsizes(image_file_, attachment_id_)
        else:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_attachment", __("The attached file cannot be found.")))
        # end if
    else:
        missing_sizes_ = wp_get_missing_image_subsizes(attachment_id_)
        if php_empty(lambda : missing_sizes_):
            return image_meta_
        # end if
        #// This also updates the image meta.
        image_meta_ = _wp_make_subsizes(missing_sizes_, image_file_, image_meta_, attachment_id_)
    # end if
    #// This filter is documented in wp-admin/includes/image.php
    image_meta_ = apply_filters("wp_generate_attachment_metadata", image_meta_, attachment_id_, "update")
    #// Save the updated metadata.
    wp_update_attachment_metadata(attachment_id_, image_meta_)
    return image_meta_
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
def _wp_image_meta_replace_original(saved_data_=None, original_file_=None, image_meta_=None, attachment_id_=None, *_args_):
    
    
    new_file_ = saved_data_["path"]
    #// Update the attached file meta.
    update_attached_file(attachment_id_, new_file_)
    #// Width and height of the new image.
    image_meta_["width"] = saved_data_["width"]
    image_meta_["height"] = saved_data_["height"]
    #// Make the file path relative to the upload dir.
    image_meta_["file"] = _wp_relative_upload_path(new_file_)
    #// Store the original image file name in image_meta.
    image_meta_["original_image"] = wp_basename(original_file_)
    return image_meta_
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
def wp_create_image_subsizes(file_=None, attachment_id_=None, *_args_):
    
    
    imagesize_ = php_no_error(lambda: getimagesize(file_))
    if php_empty(lambda : imagesize_):
        #// File is not an image.
        return Array()
    # end if
    #// Default image meta.
    image_meta_ = Array({"width": imagesize_[0], "height": imagesize_[1], "file": _wp_relative_upload_path(file_), "sizes": Array()})
    #// Fetch additional metadata from EXIF/IPTC.
    exif_meta_ = wp_read_image_metadata(file_)
    if exif_meta_:
        image_meta_["image_meta"] = exif_meta_
    # end if
    #// Do not scale (large) PNG images. May result in sub-sizes that have greater file size than the original. See #48736.
    if "image/png" != imagesize_["mime"]:
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
        threshold_ = php_int(apply_filters("big_image_size_threshold", 2560, imagesize_, file_, attachment_id_))
        #// If the original image's dimensions are over the threshold,
        #// scale the image and use it as the "full" size.
        if threshold_ and image_meta_["width"] > threshold_ or image_meta_["height"] > threshold_:
            editor_ = wp_get_image_editor(file_)
            if is_wp_error(editor_):
                #// This image cannot be edited.
                return image_meta_
            # end if
            #// Resize the image.
            resized_ = editor_.resize(threshold_, threshold_)
            rotated_ = None
            #// If there is EXIF data, rotate according to EXIF Orientation.
            if (not is_wp_error(resized_)) and php_is_array(exif_meta_):
                resized_ = editor_.maybe_exif_rotate()
                rotated_ = resized_
            # end if
            if (not is_wp_error(resized_)):
                #// Append "-scaled" to the image file name. It will look like "my_image-scaled.jpg".
                #// This doesn't affect the sub-sizes names as they are generated from the original image (for best quality).
                saved_ = editor_.save(editor_.generate_filename("scaled"))
                if (not is_wp_error(saved_)):
                    image_meta_ = _wp_image_meta_replace_original(saved_, file_, image_meta_, attachment_id_)
                    #// If the image was rotated update the stored EXIF data.
                    if True == rotated_ and (not php_empty(lambda : image_meta_["image_meta"]["orientation"])):
                        image_meta_["image_meta"]["orientation"] = 1
                    # end if
                else:
                    pass
                # end if
            else:
                pass
            # end if
        elif (not php_empty(lambda : exif_meta_["orientation"])) and 1 != php_int(exif_meta_["orientation"]):
            #// Rotate the whole original image if there is EXIF data and "orientation" is not 1.
            editor_ = wp_get_image_editor(file_)
            if is_wp_error(editor_):
                #// This image cannot be edited.
                return image_meta_
            # end if
            #// Rotate the image.
            rotated_ = editor_.maybe_exif_rotate()
            if True == rotated_:
                #// Append `-rotated` to the image file name.
                saved_ = editor_.save(editor_.generate_filename("rotated"))
                if (not is_wp_error(saved_)):
                    image_meta_ = _wp_image_meta_replace_original(saved_, file_, image_meta_, attachment_id_)
                    #// Update the stored EXIF data.
                    if (not php_empty(lambda : image_meta_["image_meta"]["orientation"])):
                        image_meta_["image_meta"]["orientation"] = 1
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
    wp_update_attachment_metadata(attachment_id_, image_meta_)
    new_sizes_ = wp_get_registered_image_subsizes()
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
    new_sizes_ = apply_filters("intermediate_image_sizes_advanced", new_sizes_, image_meta_, attachment_id_)
    return _wp_make_subsizes(new_sizes_, file_, image_meta_, attachment_id_)
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
def _wp_make_subsizes(new_sizes_=None, file_=None, image_meta_=None, attachment_id_=None, *_args_):
    
    
    if php_empty(lambda : image_meta_) or (not php_is_array(image_meta_)):
        #// Not an image attachment.
        return Array()
    # end if
    #// Check if any of the new sizes already exist.
    if (php_isset(lambda : image_meta_["sizes"])) and php_is_array(image_meta_["sizes"]):
        for size_name_,size_meta_ in image_meta_["sizes"]:
            #// 
            #// Only checks "size name" so we don't override existing images even if the dimensions
            #// don't match the currently defined size with the same name.
            #// To change the behavior, unset changed/mismatched sizes in the `sizes` array in image meta.
            #//
            if php_array_key_exists(size_name_, new_sizes_):
                new_sizes_[size_name_] = None
            # end if
        # end for
    else:
        image_meta_["sizes"] = Array()
    # end if
    if php_empty(lambda : new_sizes_):
        #// Nothing to do...
        return image_meta_
    # end if
    #// 
    #// Sort the image sub-sizes in order of priority when creating them.
    #// This ensures there is an appropriate sub-size the user can access immediately
    #// even when there was an error and not all sub-sizes were created.
    #//
    priority_ = Array({"medium": None, "large": None, "thumbnail": None, "medium_large": None})
    new_sizes_ = php_array_filter(php_array_merge(priority_, new_sizes_))
    editor_ = wp_get_image_editor(file_)
    if is_wp_error(editor_):
        #// The image cannot be edited.
        return image_meta_
    # end if
    #// If stored EXIF data exists, rotate the source image before creating sub-sizes.
    if (not php_empty(lambda : image_meta_["image_meta"])):
        rotated_ = editor_.maybe_exif_rotate()
        if is_wp_error(rotated_):
            pass
        # end if
    # end if
    if php_method_exists(editor_, "make_subsize"):
        for new_size_name_,new_size_data_ in new_sizes_:
            new_size_meta_ = editor_.make_subsize(new_size_data_)
            if is_wp_error(new_size_meta_):
                pass
            else:
                #// Save the size meta value.
                image_meta_["sizes"][new_size_name_] = new_size_meta_
                wp_update_attachment_metadata(attachment_id_, image_meta_)
            # end if
        # end for
    else:
        #// Fall back to `$editor->multi_resize()`.
        created_sizes_ = editor_.multi_resize(new_sizes_)
        if (not php_empty(lambda : created_sizes_)):
            image_meta_["sizes"] = php_array_merge(image_meta_["sizes"], created_sizes_)
            wp_update_attachment_metadata(attachment_id_, image_meta_)
        # end if
    # end if
    return image_meta_
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
def wp_generate_attachment_metadata(attachment_id_=None, file_=None, *_args_):
    
    
    attachment_ = get_post(attachment_id_)
    metadata_ = Array()
    support_ = False
    mime_type_ = get_post_mime_type(attachment_)
    if php_preg_match("!^image/!", mime_type_) and file_is_displayable_image(file_):
        #// Make thumbnails and other intermediate sizes.
        metadata_ = wp_create_image_subsizes(file_, attachment_id_)
    elif wp_attachment_is("video", attachment_):
        metadata_ = wp_read_video_metadata(file_)
        support_ = current_theme_supports("post-thumbnails", "attachment:video") or post_type_supports("attachment:video", "thumbnail")
    elif wp_attachment_is("audio", attachment_):
        metadata_ = wp_read_audio_metadata(file_)
        support_ = current_theme_supports("post-thumbnails", "attachment:audio") or post_type_supports("attachment:audio", "thumbnail")
    # end if
    if support_ and (not php_empty(lambda : metadata_["image"]["data"])):
        #// Check for existing cover.
        hash_ = php_md5(metadata_["image"]["data"])
        posts_ = get_posts(Array({"fields": "ids", "post_type": "attachment", "post_mime_type": metadata_["image"]["mime"], "post_status": "inherit", "posts_per_page": 1, "meta_key": "_cover_hash", "meta_value": hash_}))
        exists_ = reset(posts_)
        if (not php_empty(lambda : exists_)):
            update_post_meta(attachment_id_, "_thumbnail_id", exists_)
        else:
            ext_ = ".jpg"
            for case in Switch(metadata_["image"]["mime"]):
                if case("image/gif"):
                    ext_ = ".gif"
                    break
                # end if
                if case("image/png"):
                    ext_ = ".png"
                    break
                # end if
            # end for
            basename_ = php_str_replace(".", "-", wp_basename(file_)) + "-image" + ext_
            uploaded_ = wp_upload_bits(basename_, "", metadata_["image"]["data"])
            if False == uploaded_["error"]:
                image_attachment_ = Array({"post_mime_type": metadata_["image"]["mime"], "post_type": "attachment", "post_content": ""})
                #// 
                #// Filters the parameters for the attachment thumbnail creation.
                #// 
                #// @since 3.9.0
                #// 
                #// @param array $image_attachment An array of parameters to create the thumbnail.
                #// @param array $metadata         Current attachment metadata.
                #// @param array $uploaded         An array containing the thumbnail path and url.
                #//
                image_attachment_ = apply_filters("attachment_thumbnail_args", image_attachment_, metadata_, uploaded_)
                sub_attachment_id_ = wp_insert_attachment(image_attachment_, uploaded_["file"])
                add_post_meta(sub_attachment_id_, "_cover_hash", hash_)
                attach_data_ = wp_generate_attachment_metadata(sub_attachment_id_, uploaded_["file"])
                wp_update_attachment_metadata(sub_attachment_id_, attach_data_)
                update_post_meta(attachment_id_, "_thumbnail_id", sub_attachment_id_)
            # end if
        # end if
    elif "application/pdf" == mime_type_:
        #// Try to create image thumbnails for PDFs.
        fallback_sizes_ = Array("thumbnail", "medium", "large")
        #// 
        #// Filters the image sizes generated for non-image mime types.
        #// 
        #// @since 4.7.0
        #// 
        #// @param string[] $fallback_sizes An array of image size names.
        #// @param array    $metadata       Current attachment metadata.
        #//
        fallback_sizes_ = apply_filters("fallback_intermediate_image_sizes", fallback_sizes_, metadata_)
        registered_sizes_ = wp_get_registered_image_subsizes()
        merged_sizes_ = php_array_intersect_key(registered_sizes_, php_array_flip(fallback_sizes_))
        #// Force thumbnails to be soft crops.
        if (php_isset(lambda : merged_sizes_["thumbnail"])) and php_is_array(merged_sizes_["thumbnail"]):
            merged_sizes_["thumbnail"]["crop"] = False
        # end if
        #// Only load PDFs in an image editor if we're processing sizes.
        if (not php_empty(lambda : merged_sizes_)):
            editor_ = wp_get_image_editor(file_)
            if (not is_wp_error(editor_)):
                #// No support for this type of file.
                #// 
                #// PDFs may have the same file filename as JPEGs.
                #// Ensure the PDF preview image does not overwrite any JPEG images that already exist.
                #//
                dirname_ = php_dirname(file_) + "/"
                ext_ = "." + pathinfo(file_, PATHINFO_EXTENSION)
                preview_file_ = dirname_ + wp_unique_filename(dirname_, wp_basename(file_, ext_) + "-pdf.jpg")
                uploaded_ = editor_.save(preview_file_, "image/jpeg")
                editor_ = None
                #// Resize based on the full size image, rather than the source.
                if (not is_wp_error(uploaded_)):
                    image_file_ = uploaded_["path"]
                    uploaded_["path"] = None
                    metadata_["sizes"] = Array({"full": uploaded_})
                    #// Save the meta data before any image post-processing errors could happen.
                    wp_update_attachment_metadata(attachment_id_, metadata_)
                    #// Create sub-sizes saving the image meta after each.
                    metadata_ = _wp_make_subsizes(merged_sizes_, image_file_, metadata_, attachment_id_)
                # end if
            # end if
        # end if
    # end if
    #// Remove the blob of binary data from the array.
    if metadata_:
        metadata_["image"]["data"] = None
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
    return apply_filters("wp_generate_attachment_metadata", metadata_, attachment_id_, "create")
# end def wp_generate_attachment_metadata
#// 
#// Convert a fraction string to a decimal.
#// 
#// @since 2.5.0
#// 
#// @param string $str
#// @return int|float
#//
def wp_exif_frac2dec(str_=None, *_args_):
    
    
    if False == php_strpos(str_, "/"):
        return str_
    # end if
    numerator_, denominator_ = php_explode("/", str_)
    if (not php_empty(lambda : denominator_)):
        return numerator_ / denominator_
    # end if
    return str_
# end def wp_exif_frac2dec
#// 
#// Convert the exif date format to a unix timestamp.
#// 
#// @since 2.5.0
#// 
#// @param string $str
#// @return int
#//
def wp_exif_date2ts(str_=None, *_args_):
    
    
    date_, time_ = php_explode(" ", php_trim(str_))
    y_, m_, d_ = php_explode(":", date_)
    return strtotime(str(y_) + str("-") + str(m_) + str("-") + str(d_) + str(" ") + str(time_))
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
def wp_read_image_metadata(file_=None, *_args_):
    
    
    if (not php_file_exists(file_)):
        return False
    # end if
    image_type_ = php_no_error(lambda: getimagesize(file_))
    #// 
    #// EXIF contains a bunch of data we'll probably never need formatted in ways
    #// that are difficult to use. We'll normalize it and just extract the fields
    #// that are likely to be useful. Fractions and numbers are converted to
    #// floats, dates to unix timestamps, and everything else to strings.
    #//
    meta_ = Array({"aperture": 0, "credit": "", "camera": "", "caption": "", "created_timestamp": 0, "copyright": "", "focal_length": 0, "iso": 0, "shutter_speed": 0, "title": "", "orientation": 0, "keywords": Array()})
    iptc_ = Array()
    #// 
    #// Read IPTC first, since it might contain data not available in exif such
    #// as caption, description etc.
    #//
    if php_is_callable("iptcparse"):
        php_no_error(lambda: getimagesize(file_, info_))
        if (not php_empty(lambda : info_["APP13"])):
            iptc_ = php_no_error(lambda: iptcparse(info_["APP13"]))
            #// Headline, "A brief synopsis of the caption".
            if (not php_empty(lambda : iptc_["2#105"][0])):
                meta_["title"] = php_trim(iptc_["2#105"][0])
                pass
            elif (not php_empty(lambda : iptc_["2#005"][0])):
                meta_["title"] = php_trim(iptc_["2#005"][0])
            # end if
            if (not php_empty(lambda : iptc_["2#120"][0])):
                #// Description / legacy caption.
                caption_ = php_trim(iptc_["2#120"][0])
                mbstring_binary_safe_encoding()
                caption_length_ = php_strlen(caption_)
                reset_mbstring_encoding()
                if php_empty(lambda : meta_["title"]) and caption_length_ < 80:
                    #// Assume the title is stored in 2:120 if it's short.
                    meta_["title"] = caption_
                # end if
                meta_["caption"] = caption_
            # end if
            if (not php_empty(lambda : iptc_["2#110"][0])):
                #// Credit.
                meta_["credit"] = php_trim(iptc_["2#110"][0])
            elif (not php_empty(lambda : iptc_["2#080"][0])):
                #// Creator / legacy byline.
                meta_["credit"] = php_trim(iptc_["2#080"][0])
            # end if
            if (not php_empty(lambda : iptc_["2#055"][0])) and (not php_empty(lambda : iptc_["2#060"][0])):
                #// Created date and time.
                meta_["created_timestamp"] = strtotime(iptc_["2#055"][0] + " " + iptc_["2#060"][0])
            # end if
            if (not php_empty(lambda : iptc_["2#116"][0])):
                #// Copyright.
                meta_["copyright"] = php_trim(iptc_["2#116"][0])
            # end if
            if (not php_empty(lambda : iptc_["2#025"][0])):
                #// Keywords array.
                meta_["keywords"] = php_array_values(iptc_["2#025"])
            # end if
        # end if
    # end if
    exif_ = Array()
    #// 
    #// Filters the image types to check for exif data.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $image_types Image types to check for exif data.
    #//
    exif_image_types_ = apply_filters("wp_read_image_metadata_types", Array(IMAGETYPE_JPEG, IMAGETYPE_TIFF_II, IMAGETYPE_TIFF_MM))
    if php_is_callable("exif_read_data") and php_in_array(image_type_, exif_image_types_, True):
        exif_ = php_no_error(lambda: exif_read_data(file_))
        if (not php_empty(lambda : exif_["ImageDescription"])):
            mbstring_binary_safe_encoding()
            description_length_ = php_strlen(exif_["ImageDescription"])
            reset_mbstring_encoding()
            if php_empty(lambda : meta_["title"]) and description_length_ < 80:
                #// Assume the title is stored in ImageDescription.
                meta_["title"] = php_trim(exif_["ImageDescription"])
            # end if
            if php_empty(lambda : meta_["caption"]) and (not php_empty(lambda : exif_["COMPUTED"]["UserComment"])):
                meta_["caption"] = php_trim(exif_["COMPUTED"]["UserComment"])
            # end if
            if php_empty(lambda : meta_["caption"]):
                meta_["caption"] = php_trim(exif_["ImageDescription"])
            # end if
        elif php_empty(lambda : meta_["caption"]) and (not php_empty(lambda : exif_["Comments"])):
            meta_["caption"] = php_trim(exif_["Comments"])
        # end if
        if php_empty(lambda : meta_["credit"]):
            if (not php_empty(lambda : exif_["Artist"])):
                meta_["credit"] = php_trim(exif_["Artist"])
            elif (not php_empty(lambda : exif_["Author"])):
                meta_["credit"] = php_trim(exif_["Author"])
            # end if
        # end if
        if php_empty(lambda : meta_["copyright"]) and (not php_empty(lambda : exif_["Copyright"])):
            meta_["copyright"] = php_trim(exif_["Copyright"])
        # end if
        if (not php_empty(lambda : exif_["FNumber"])):
            meta_["aperture"] = round(wp_exif_frac2dec(exif_["FNumber"]), 2)
        # end if
        if (not php_empty(lambda : exif_["Model"])):
            meta_["camera"] = php_trim(exif_["Model"])
        # end if
        if php_empty(lambda : meta_["created_timestamp"]) and (not php_empty(lambda : exif_["DateTimeDigitized"])):
            meta_["created_timestamp"] = wp_exif_date2ts(exif_["DateTimeDigitized"])
        # end if
        if (not php_empty(lambda : exif_["FocalLength"])):
            meta_["focal_length"] = php_str(wp_exif_frac2dec(exif_["FocalLength"]))
        # end if
        if (not php_empty(lambda : exif_["ISOSpeedRatings"])):
            meta_["iso"] = reset(exif_["ISOSpeedRatings"]) if php_is_array(exif_["ISOSpeedRatings"]) else exif_["ISOSpeedRatings"]
            meta_["iso"] = php_trim(meta_["iso"])
        # end if
        if (not php_empty(lambda : exif_["ExposureTime"])):
            meta_["shutter_speed"] = php_str(wp_exif_frac2dec(exif_["ExposureTime"]))
        # end if
        if (not php_empty(lambda : exif_["Orientation"])):
            meta_["orientation"] = exif_["Orientation"]
        # end if
    # end if
    for key_ in Array("title", "caption", "credit", "copyright", "camera", "iso"):
        if meta_[key_] and (not seems_utf8(meta_[key_])):
            meta_[key_] = utf8_encode(meta_[key_])
        # end if
    # end for
    for key_,keyword_ in meta_["keywords"]:
        if (not seems_utf8(keyword_)):
            meta_["keywords"][key_] = utf8_encode(keyword_)
        # end if
    # end for
    meta_ = wp_kses_post_deep(meta_)
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
    return apply_filters("wp_read_image_metadata", meta_, file_, image_type_, iptc_, exif_)
# end def wp_read_image_metadata
#// 
#// Validate that file is an image.
#// 
#// @since 2.5.0
#// 
#// @param string $path File path to test if valid image.
#// @return bool True if valid image, false if not valid image.
#//
def file_is_valid_image(path_=None, *_args_):
    
    
    size_ = php_no_error(lambda: getimagesize(path_))
    return (not php_empty(lambda : size_))
# end def file_is_valid_image
#// 
#// Validate that file is suitable for displaying within a web page.
#// 
#// @since 2.5.0
#// 
#// @param string $path File path to test.
#// @return bool True if suitable, false if not suitable.
#//
def file_is_displayable_image(path_=None, *_args_):
    
    
    displayable_image_types_ = Array(IMAGETYPE_GIF, IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_BMP, IMAGETYPE_ICO)
    info_ = php_no_error(lambda: getimagesize(path_))
    if php_empty(lambda : info_):
        result_ = False
    elif (not php_in_array(info_[2], displayable_image_types_, True)):
        result_ = False
    else:
        result_ = True
    # end if
    #// 
    #// Filters whether the current image is displayable in the browser.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool   $result Whether the image can be displayed. Default true.
    #// @param string $path   Path to the image.
    #//
    return apply_filters("file_is_displayable_image", result_, path_)
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
def load_image_to_edit(attachment_id_=None, mime_type_=None, size_="full", *_args_):
    
    
    filepath_ = _load_image_to_edit_path(attachment_id_, size_)
    if php_empty(lambda : filepath_):
        return False
    # end if
    for case in Switch(mime_type_):
        if case("image/jpeg"):
            image_ = imagecreatefromjpeg(filepath_)
            break
        # end if
        if case("image/png"):
            image_ = imagecreatefrompng(filepath_)
            break
        # end if
        if case("image/gif"):
            image_ = imagecreatefromgif(filepath_)
            break
        # end if
        if case():
            image_ = False
            break
        # end if
    # end for
    if is_resource(image_):
        #// 
        #// Filters the current image being loaded for editing.
        #// 
        #// @since 2.9.0
        #// 
        #// @param resource $image         Current image.
        #// @param string   $attachment_id Attachment ID.
        #// @param string   $size          Image size.
        #//
        image_ = apply_filters("load_image_to_edit", image_, attachment_id_, size_)
        if php_function_exists("imagealphablending") and php_function_exists("imagesavealpha"):
            imagealphablending(image_, False)
            imagesavealpha(image_, True)
        # end if
    # end if
    return image_
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
def _load_image_to_edit_path(attachment_id_=None, size_="full", *_args_):
    
    
    filepath_ = get_attached_file(attachment_id_)
    if filepath_ and php_file_exists(filepath_):
        if "full" != size_:
            data_ = image_get_intermediate_size(attachment_id_, size_)
            if data_:
                filepath_ = path_join(php_dirname(filepath_), data_["file"])
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
                filepath_ = apply_filters("load_image_to_edit_filesystempath", filepath_, attachment_id_, size_)
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
        filepath_ = apply_filters("load_image_to_edit_attachmenturl", wp_get_attachment_url(attachment_id_), attachment_id_, size_)
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
    return apply_filters("load_image_to_edit_path", filepath_, attachment_id_, size_)
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
def _copy_image_file(attachment_id_=None, *_args_):
    
    
    dst_file_ = get_attached_file(attachment_id_)
    src_file_ = dst_file_
    if (not php_file_exists(src_file_)):
        src_file_ = _load_image_to_edit_path(attachment_id_)
    # end if
    if src_file_:
        dst_file_ = php_str_replace(wp_basename(dst_file_), "copy-" + wp_basename(dst_file_), dst_file_)
        dst_file_ = php_dirname(dst_file_) + "/" + wp_unique_filename(php_dirname(dst_file_), wp_basename(dst_file_))
        #// 
        #// The directory containing the original file may no longer
        #// exist when using a replication plugin.
        #//
        wp_mkdir_p(php_dirname(dst_file_))
        if (not copy(src_file_, dst_file_)):
            dst_file_ = False
        # end if
    else:
        dst_file_ = False
    # end if
    return dst_file_
# end def _copy_image_file
