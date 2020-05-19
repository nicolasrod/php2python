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
#// WordPress API for media display.
#// 
#// @package WordPress
#// @subpackage Media
#// 
#// 
#// Retrieve additional image sizes.
#// 
#// @since 4.7.0
#// 
#// @global array $_wp_additional_image_sizes
#// 
#// @return array Additional images size data.
#//
def wp_get_additional_image_sizes(*_args_):
    
    
    global _wp_additional_image_sizes_
    php_check_if_defined("_wp_additional_image_sizes_")
    if (not _wp_additional_image_sizes_):
        _wp_additional_image_sizes_ = Array()
    # end if
    return _wp_additional_image_sizes_
# end def wp_get_additional_image_sizes
#// 
#// Scale down the default size of an image.
#// 
#// This is so that the image is a better fit for the editor and theme.
#// 
#// The `$size` parameter accepts either an array or a string. The supported string
#// values are 'thumb' or 'thumbnail' for the given thumbnail size or defaults at
#// 128 width and 96 height in pixels. Also supported for the string value is
#// 'medium', 'medium_large' and 'full'. The 'full' isn't actually supported, but any value other
#// than the supported will result in the content_width size or 500 if that is
#// not set.
#// 
#// Finally, there is a filter named {@see 'editor_max_image_size'}, that will be
#// called on the calculated array for width and height, respectively.
#// 
#// @since 2.5.0
#// 
#// @global int   $content_width
#// 
#// @param int          $width   Width of the image in pixels.
#// @param int          $height  Height of the image in pixels.
#// @param string|array $size    Optional. Image size. Accepts any valid image size, or an array
#// of width and height values in pixels (in that order).
#// Default 'medium'.
#// @param string       $context Optional. Could be 'display' (like in a theme) or 'edit'
#// (like inserting into an editor). Default null.
#// @return int[] {
#// An array of width and height values.
#// 
#// @type int $0 The maximum width in pixels.
#// @type int $1 The maximum height in pixels.
#// }
#//
def image_constrain_size_for_editor(width_=None, height_=None, size_="medium", context_=None, *_args_):
    if context_ is None:
        context_ = None
    # end if
    
    global content_width_
    php_check_if_defined("content_width_")
    _wp_additional_image_sizes_ = wp_get_additional_image_sizes()
    if (not context_):
        context_ = "edit" if is_admin() else "display"
    # end if
    if php_is_array(size_):
        max_width_ = size_[0]
        max_height_ = size_[1]
    elif "thumb" == size_ or "thumbnail" == size_:
        max_width_ = php_intval(get_option("thumbnail_size_w"))
        max_height_ = php_intval(get_option("thumbnail_size_h"))
        #// Last chance thumbnail size defaults.
        if (not max_width_) and (not max_height_):
            max_width_ = 128
            max_height_ = 96
        # end if
    elif "medium" == size_:
        max_width_ = php_intval(get_option("medium_size_w"))
        max_height_ = php_intval(get_option("medium_size_h"))
    elif "medium_large" == size_:
        max_width_ = php_intval(get_option("medium_large_size_w"))
        max_height_ = php_intval(get_option("medium_large_size_h"))
        if php_intval(content_width_) > 0:
            max_width_ = php_min(php_intval(content_width_), max_width_)
        # end if
    elif "large" == size_:
        #// 
        #// We're inserting a large size image into the editor. If it's a really
        #// big image we'll scale it down to fit reasonably within the editor
        #// itself, and within the theme's content width if it's known. The user
        #// can resize it in the editor if they wish.
        #//
        max_width_ = php_intval(get_option("large_size_w"))
        max_height_ = php_intval(get_option("large_size_h"))
        if php_intval(content_width_) > 0:
            max_width_ = php_min(php_intval(content_width_), max_width_)
        # end if
    elif (not php_empty(lambda : _wp_additional_image_sizes_)) and php_in_array(size_, php_array_keys(_wp_additional_image_sizes_), True):
        max_width_ = php_intval(_wp_additional_image_sizes_[size_]["width"])
        max_height_ = php_intval(_wp_additional_image_sizes_[size_]["height"])
        #// Only in admin. Assume that theme authors know what they're doing.
        if php_intval(content_width_) > 0 and "edit" == context_:
            max_width_ = php_min(php_intval(content_width_), max_width_)
        # end if
    else:
        #// $size === 'full' has no constraint.
        max_width_ = width_
        max_height_ = height_
    # end if
    #// 
    #// Filters the maximum image size dimensions for the editor.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int[]        $max_image_size {
    #// An array of width and height values.
    #// 
    #// @type int $0 The maximum width in pixels.
    #// @type int $1 The maximum height in pixels.
    #// }
    #// @param string|array $size           Size of what the result image should be.
    #// @param string       $context        The context the image is being resized for.
    #// Possible values are 'display' (like in a theme)
    #// or 'edit' (like inserting into an editor).
    #//
    max_width_, max_height_ = apply_filters("editor_max_image_size", Array(max_width_, max_height_), size_, context_)
    return wp_constrain_dimensions(width_, height_, max_width_, max_height_)
# end def image_constrain_size_for_editor
#// 
#// Retrieve width and height attributes using given width and height values.
#// 
#// Both attributes are required in the sense that both parameters must have a
#// value, but are optional in that if you set them to false or null, then they
#// will not be added to the returned string.
#// 
#// You can set the value using a string, but it will only take numeric values.
#// If you wish to put 'px' after the numbers, then it will be stripped out of
#// the return.
#// 
#// @since 2.5.0
#// 
#// @param int|string $width  Image width in pixels.
#// @param int|string $height Image height in pixels.
#// @return string HTML attributes for width and, or height.
#//
def image_hwstring(width_=None, height_=None, *_args_):
    
    
    out_ = ""
    if width_:
        out_ += "width=\"" + php_intval(width_) + "\" "
    # end if
    if height_:
        out_ += "height=\"" + php_intval(height_) + "\" "
    # end if
    return out_
# end def image_hwstring
#// 
#// Scale an image to fit a particular size (such as 'thumb' or 'medium').
#// 
#// The URL might be the original image, or it might be a resized version. This
#// function won't create a new resized copy, it will just return an already
#// resized one if it exists.
#// 
#// A plugin may use the {@see 'image_downsize'} filter to hook into and offer image
#// resizing services for images. The hook must return an array with the same
#// elements that are normally returned from the function.
#// 
#// @since 2.5.0
#// 
#// @param int          $id   Attachment ID for image.
#// @param string|int[] $size Optional. Image size to scale to. Accepts any valid image size name,
#// or an array of width and height values in pixels (in that order).
#// Default 'medium'.
#// @return array|false {
#// Array of image data, or boolean false if no image is available.
#// 
#// @type string $0 Image source URL.
#// @type int    $1 Image width in pixels.
#// @type int    $2 Image height in pixels.
#// @type bool   $3 Whether the image is a resized image.
#// }
#//
def image_downsize(id_=None, size_="medium", *_args_):
    
    
    is_image_ = wp_attachment_is_image(id_)
    #// 
    #// Filters whether to preempt the output of image_downsize().
    #// 
    #// Returning a truthy value from the filter will effectively short-circuit
    #// down-sizing the image, returning that value instead.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool|array   $downsize Whether to short-circuit the image downsize.
    #// @param int          $id       Attachment ID for image.
    #// @param array|string $size     Requested size of image. Image size name, or array of width
    #// and height values (in that order).
    #//
    out_ = apply_filters("image_downsize", False, id_, size_)
    if out_:
        return out_
    # end if
    img_url_ = wp_get_attachment_url(id_)
    meta_ = wp_get_attachment_metadata(id_)
    width_ = 0
    height_ = 0
    is_intermediate_ = False
    img_url_basename_ = wp_basename(img_url_)
    #// If the file isn't an image, attempt to replace its URL with a rendered image from its meta.
    #// Otherwise, a non-image type could be returned.
    if (not is_image_):
        if (not php_empty(lambda : meta_["sizes"]["full"])):
            img_url_ = php_str_replace(img_url_basename_, meta_["sizes"]["full"]["file"], img_url_)
            img_url_basename_ = meta_["sizes"]["full"]["file"]
            width_ = meta_["sizes"]["full"]["width"]
            height_ = meta_["sizes"]["full"]["height"]
        else:
            return False
        # end if
    # end if
    #// Try for a new style intermediate size.
    intermediate_ = image_get_intermediate_size(id_, size_)
    if intermediate_:
        img_url_ = php_str_replace(img_url_basename_, intermediate_["file"], img_url_)
        width_ = intermediate_["width"]
        height_ = intermediate_["height"]
        is_intermediate_ = True
    elif "thumbnail" == size_:
        #// Fall back to the old thumbnail.
        thumb_file_ = wp_get_attachment_thumb_file(id_)
        info_ = None
        if thumb_file_:
            info_ = php_no_error(lambda: getimagesize(thumb_file_))
        # end if
        if thumb_file_ and info_:
            img_url_ = php_str_replace(img_url_basename_, wp_basename(thumb_file_), img_url_)
            width_ = info_[0]
            height_ = info_[1]
            is_intermediate_ = True
        # end if
    # end if
    if (not width_) and (not height_) and (php_isset(lambda : meta_["width"]) and php_isset(lambda : meta_["height"])):
        #// Any other type: use the real image.
        width_ = meta_["width"]
        height_ = meta_["height"]
    # end if
    if img_url_:
        #// We have the actual image size, but might need to further constrain it if content_width is narrower.
        width_, height_ = image_constrain_size_for_editor(width_, height_, size_)
        return Array(img_url_, width_, height_, is_intermediate_)
    # end if
    return False
# end def image_downsize
#// 
#// Register a new image size.
#// 
#// @since 2.9.0
#// 
#// @global array $_wp_additional_image_sizes Associative array of additional image sizes.
#// 
#// @param string     $name   Image size identifier.
#// @param int        $width  Optional. Image width in pixels. Default 0.
#// @param int        $height Optional. Image height in pixels. Default 0.
#// @param bool|array $crop   Optional. Image cropping behavior. If false, the image will be scaled (default),
#// If true, image will be cropped to the specified dimensions using center positions.
#// If an array, the image will be cropped using the array to specify the crop location.
#// Array values must be in the format: array( x_crop_position, y_crop_position ) where:
#// - x_crop_position accepts: 'left', 'center', or 'right'.
#// - y_crop_position accepts: 'top', 'center', or 'bottom'.
#//
def add_image_size(name_=None, width_=0, height_=0, crop_=None, *_args_):
    if crop_ is None:
        crop_ = False
    # end if
    
    global _wp_additional_image_sizes_
    php_check_if_defined("_wp_additional_image_sizes_")
    _wp_additional_image_sizes_[name_] = Array({"width": absint(width_), "height": absint(height_), "crop": crop_})
# end def add_image_size
#// 
#// Check if an image size exists.
#// 
#// @since 3.9.0
#// 
#// @param string $name The image size to check.
#// @return bool True if the image size exists, false if not.
#//
def has_image_size(name_=None, *_args_):
    
    
    sizes_ = wp_get_additional_image_sizes()
    return (php_isset(lambda : sizes_[name_]))
# end def has_image_size
#// 
#// Remove a new image size.
#// 
#// @since 3.9.0
#// 
#// @global array $_wp_additional_image_sizes
#// 
#// @param string $name The image size to remove.
#// @return bool True if the image size was successfully removed, false on failure.
#//
def remove_image_size(name_=None, *_args_):
    
    
    global _wp_additional_image_sizes_
    php_check_if_defined("_wp_additional_image_sizes_")
    if (php_isset(lambda : _wp_additional_image_sizes_[name_])):
        _wp_additional_image_sizes_[name_] = None
        return True
    # end if
    return False
# end def remove_image_size
#// 
#// Registers an image size for the post thumbnail.
#// 
#// @since 2.9.0
#// 
#// @see add_image_size() for details on cropping behavior.
#// 
#// @param int        $width  Image width in pixels.
#// @param int        $height Image height in pixels.
#// @param bool|array $crop   Optional. Whether to crop images to specified width and height or resize.
#// An array can specify positioning of the crop area. Default false.
#//
def set_post_thumbnail_size(width_=0, height_=0, crop_=None, *_args_):
    if crop_ is None:
        crop_ = False
    # end if
    
    add_image_size("post-thumbnail", width_, height_, crop_)
# end def set_post_thumbnail_size
#// 
#// Gets an img tag for an image attachment, scaling it down if requested.
#// 
#// The {@see 'get_image_tag_class'} filter allows for changing the class name for the
#// image without having to use regular expressions on the HTML content. The
#// parameters are: what WordPress will use for the class, the Attachment ID,
#// image align value, and the size the image should be.
#// 
#// The second filter, {@see 'get_image_tag'}, has the HTML content, which can then be
#// further manipulated by a plugin to change all attribute values and even HTML
#// content.
#// 
#// @since 2.5.0
#// 
#// @param int          $id    Attachment ID.
#// @param string       $alt   Image description for the alt attribute.
#// @param string       $title Image description for the title attribute.
#// @param string       $align Part of the class name for aligning the image.
#// @param string|array $size  Optional. Registered image size to retrieve a tag for. Accepts any
#// valid image size, or an array of width and height values in pixels
#// (in that order). Default 'medium'.
#// @return string HTML IMG element for given image attachment
#//
def get_image_tag(id_=None, alt_=None, title_=None, align_=None, size_="medium", *_args_):
    
    
    img_src_, width_, height_ = image_downsize(id_, size_)
    hwstring_ = image_hwstring(width_, height_)
    title_ = "title=\"" + esc_attr(title_) + "\" " if title_ else ""
    class_ = "align" + esc_attr(align_) + " size-" + esc_attr(size_) + " wp-image-" + id_
    #// 
    #// Filters the value of the attachment's image tag class attribute.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string       $class CSS class name or space-separated list of classes.
    #// @param int          $id    Attachment ID.
    #// @param string       $align Part of the class name for aligning the image.
    #// @param string|array $size  Size of image. Image size or array of width and height values (in that order).
    #// Default 'medium'.
    #//
    class_ = apply_filters("get_image_tag_class", class_, id_, align_, size_)
    html_ = "<img src=\"" + esc_attr(img_src_) + "\" alt=\"" + esc_attr(alt_) + "\" " + title_ + hwstring_ + "class=\"" + class_ + "\" />"
    #// 
    #// Filters the HTML content for the image tag.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string       $html  HTML content for the image.
    #// @param int          $id    Attachment ID.
    #// @param string       $alt   Image description for the alt attribute.
    #// @param string       $title Image description for the title attribute.
    #// @param string       $align Part of the class name for aligning the image.
    #// @param string|array $size  Size of image. Image size or array of width and height values (in that order).
    #// Default 'medium'.
    #//
    return apply_filters("get_image_tag", html_, id_, alt_, title_, align_, size_)
# end def get_image_tag
#// 
#// Calculates the new dimensions for a down-sampled image.
#// 
#// If either width or height are empty, no constraint is applied on
#// that dimension.
#// 
#// @since 2.5.0
#// 
#// @param int $current_width  Current width of the image.
#// @param int $current_height Current height of the image.
#// @param int $max_width      Optional. Max width in pixels to constrain to. Default 0.
#// @param int $max_height     Optional. Max height in pixels to constrain to. Default 0.
#// @return int[] {
#// An array of width and height values.
#// 
#// @type int $0 The width in pixels.
#// @type int $1 The height in pixels.
#// }
#//
def wp_constrain_dimensions(current_width_=None, current_height_=None, max_width_=0, max_height_=0, *_args_):
    
    
    if (not max_width_) and (not max_height_):
        return Array(current_width_, current_height_)
    # end if
    width_ratio_ = 1
    height_ratio_ = 1
    did_width_ = False
    did_height_ = False
    if max_width_ > 0 and current_width_ > 0 and current_width_ > max_width_:
        width_ratio_ = max_width_ / current_width_
        did_width_ = True
    # end if
    if max_height_ > 0 and current_height_ > 0 and current_height_ > max_height_:
        height_ratio_ = max_height_ / current_height_
        did_height_ = True
    # end if
    #// Calculate the larger/smaller ratios.
    smaller_ratio_ = php_min(width_ratio_, height_ratio_)
    larger_ratio_ = php_max(width_ratio_, height_ratio_)
    if php_int(round(current_width_ * larger_ratio_)) > max_width_ or php_int(round(current_height_ * larger_ratio_)) > max_height_:
        #// The larger ratio is too big. It would result in an overflow.
        ratio_ = smaller_ratio_
    else:
        #// The larger ratio fits, and is likely to be a more "snug" fit.
        ratio_ = larger_ratio_
    # end if
    #// Very small dimensions may result in 0, 1 should be the minimum.
    w_ = php_max(1, php_int(round(current_width_ * ratio_)))
    h_ = php_max(1, php_int(round(current_height_ * ratio_)))
    #// 
    #// Sometimes, due to rounding, we'll end up with a result like this:
    #// 465x700 in a 177x177 box is 117x176... a pixel short.
    #// We also have issues with recursive calls resulting in an ever-changing result.
    #// Constraining to the result of a constraint should yield the original result.
    #// Thus we look for dimensions that are one pixel shy of the max value and bump them up.
    #// 
    #// Note: $did_width means it is possible $smaller_ratio == $width_ratio.
    if did_width_ and w_ == max_width_ - 1:
        w_ = max_width_
        pass
    # end if
    #// Note: $did_height means it is possible $smaller_ratio == $height_ratio.
    if did_height_ and h_ == max_height_ - 1:
        h_ = max_height_
        pass
    # end if
    #// 
    #// Filters dimensions to constrain down-sampled images to.
    #// 
    #// @since 4.1.0
    #// 
    #// @param int[] $dimensions     {
    #// An array of width and height values.
    #// 
    #// @type int $0 The width in pixels.
    #// @type int $1 The height in pixels.
    #// }
    #// @param int   $current_width  The current width of the image.
    #// @param int   $current_height The current height of the image.
    #// @param int   $max_width      The maximum width permitted.
    #// @param int   $max_height     The maximum height permitted.
    #//
    return apply_filters("wp_constrain_dimensions", Array(w_, h_), current_width_, current_height_, max_width_, max_height_)
# end def wp_constrain_dimensions
#// 
#// Retrieves calculated resize dimensions for use in WP_Image_Editor.
#// 
#// Calculates dimensions and coordinates for a resized image that fits
#// within a specified width and height.
#// 
#// Cropping behavior is dependent on the value of $crop:
#// 1. If false (default), images will not be cropped.
#// 2. If an array in the form of array( x_crop_position, y_crop_position ):
#// - x_crop_position accepts 'left' 'center', or 'right'.
#// - y_crop_position accepts 'top', 'center', or 'bottom'.
#// Images will be cropped to the specified dimensions within the defined crop area.
#// 3. If true, images will be cropped to the specified dimensions using center positions.
#// 
#// @since 2.5.0
#// 
#// @param int        $orig_w Original width in pixels.
#// @param int        $orig_h Original height in pixels.
#// @param int        $dest_w New width in pixels.
#// @param int        $dest_h New height in pixels.
#// @param bool|array $crop   Optional. Whether to crop image to specified width and height or resize.
#// An array can specify positioning of the crop area. Default false.
#// @return array|false Returned array matches parameters for `imagecopyresampled()`. False on failure.
#//
def image_resize_dimensions(orig_w_=None, orig_h_=None, dest_w_=None, dest_h_=None, crop_=None, *_args_):
    if crop_ is None:
        crop_ = False
    # end if
    
    if orig_w_ <= 0 or orig_h_ <= 0:
        return False
    # end if
    #// At least one of $dest_w or $dest_h must be specific.
    if dest_w_ <= 0 and dest_h_ <= 0:
        return False
    # end if
    #// 
    #// Filters whether to preempt calculating the image resize dimensions.
    #// 
    #// Passing a non-null value to the filter will effectively short-circuit
    #// image_resize_dimensions(), returning that value instead.
    #// 
    #// @since 3.4.0
    #// 
    #// @param null|mixed $null   Whether to preempt output of the resize dimensions.
    #// @param int        $orig_w Original width in pixels.
    #// @param int        $orig_h Original height in pixels.
    #// @param int        $dest_w New width in pixels.
    #// @param int        $dest_h New height in pixels.
    #// @param bool|array $crop   Whether to crop image to specified width and height or resize.
    #// An array can specify positioning of the crop area. Default false.
    #//
    output_ = apply_filters("image_resize_dimensions", None, orig_w_, orig_h_, dest_w_, dest_h_, crop_)
    if None != output_:
        return output_
    # end if
    #// Stop if the destination size is larger than the original image dimensions.
    if php_empty(lambda : dest_h_):
        if orig_w_ < dest_w_:
            return False
        # end if
    elif php_empty(lambda : dest_w_):
        if orig_h_ < dest_h_:
            return False
        # end if
    else:
        if orig_w_ < dest_w_ and orig_h_ < dest_h_:
            return False
        # end if
    # end if
    if crop_:
        #// 
        #// Crop the largest possible portion of the original image that we can size to $dest_w x $dest_h.
        #// Note that the requested crop dimensions are used as a maximum bounding box for the original image.
        #// If the original image's width or height is less than the requested width or height
        #// only the greater one will be cropped.
        #// For example when the original image is 600x300, and the requested crop dimensions are 400x400,
        #// the resulting image will be 400x300.
        #//
        aspect_ratio_ = orig_w_ / orig_h_
        new_w_ = php_min(dest_w_, orig_w_)
        new_h_ = php_min(dest_h_, orig_h_)
        if (not new_w_):
            new_w_ = php_int(round(new_h_ * aspect_ratio_))
        # end if
        if (not new_h_):
            new_h_ = php_int(round(new_w_ / aspect_ratio_))
        # end if
        size_ratio_ = php_max(new_w_ / orig_w_, new_h_ / orig_h_)
        crop_w_ = round(new_w_ / size_ratio_)
        crop_h_ = round(new_h_ / size_ratio_)
        if (not php_is_array(crop_)) or php_count(crop_) != 2:
            crop_ = Array("center", "center")
        # end if
        x_, y_ = crop_
        if "left" == x_:
            s_x_ = 0
        elif "right" == x_:
            s_x_ = orig_w_ - crop_w_
        else:
            s_x_ = floor(orig_w_ - crop_w_ / 2)
        # end if
        if "top" == y_:
            s_y_ = 0
        elif "bottom" == y_:
            s_y_ = orig_h_ - crop_h_
        else:
            s_y_ = floor(orig_h_ - crop_h_ / 2)
        # end if
    else:
        #// Resize using $dest_w x $dest_h as a maximum bounding box.
        crop_w_ = orig_w_
        crop_h_ = orig_h_
        s_x_ = 0
        s_y_ = 0
        new_w_, new_h_ = wp_constrain_dimensions(orig_w_, orig_h_, dest_w_, dest_h_)
    # end if
    if wp_fuzzy_number_match(new_w_, orig_w_) and wp_fuzzy_number_match(new_h_, orig_h_):
        #// The new size has virtually the same dimensions as the original image.
        #// 
        #// Filters whether to proceed with making an image sub-size with identical dimensions
        #// with the original/source image. Differences of 1px may be due to rounding and are ignored.
        #// 
        #// @since 5.3.0
        #// 
        #// @param bool $proceed The filtered value.
        #// @param int  $orig_w  Original image width.
        #// @param int  $orig_h  Original image height.
        #//
        proceed_ = php_bool(apply_filters("wp_image_resize_identical_dimensions", False, orig_w_, orig_h_))
        if (not proceed_):
            return False
        # end if
    # end if
    #// The return array matches the parameters to imagecopyresampled().
    #// int dst_x, int dst_y, int src_x, int src_y, int dst_w, int dst_h, int src_w, int src_h
    return Array(0, 0, php_int(s_x_), php_int(s_y_), php_int(new_w_), php_int(new_h_), php_int(crop_w_), php_int(crop_h_))
# end def image_resize_dimensions
#// 
#// Resizes an image to make a thumbnail or intermediate size.
#// 
#// The returned array has the file size, the image width, and image height. The
#// {@see 'image_make_intermediate_size'} filter can be used to hook in and change the
#// values of the returned array. The only parameter is the resized file path.
#// 
#// @since 2.5.0
#// 
#// @param string $file   File path.
#// @param int    $width  Image width.
#// @param int    $height Image height.
#// @param bool   $crop   Optional. Whether to crop image to specified width and height or resize.
#// Default false.
#// @return array|false Metadata array on success. False if no image was created.
#//
def image_make_intermediate_size(file_=None, width_=None, height_=None, crop_=None, *_args_):
    if crop_ is None:
        crop_ = False
    # end if
    
    if width_ or height_:
        editor_ = wp_get_image_editor(file_)
        if is_wp_error(editor_) or is_wp_error(editor_.resize(width_, height_, crop_)):
            return False
        # end if
        resized_file_ = editor_.save()
        if (not is_wp_error(resized_file_)) and resized_file_:
            resized_file_["path"] = None
            return resized_file_
        # end if
    # end if
    return False
# end def image_make_intermediate_size
#// 
#// Helper function to test if aspect ratios for two images match.
#// 
#// @since 4.6.0
#// 
#// @param int $source_width  Width of the first image in pixels.
#// @param int $source_height Height of the first image in pixels.
#// @param int $target_width  Width of the second image in pixels.
#// @param int $target_height Height of the second image in pixels.
#// @return bool True if aspect ratios match within 1px. False if not.
#//
def wp_image_matches_ratio(source_width_=None, source_height_=None, target_width_=None, target_height_=None, *_args_):
    
    
    #// 
    #// To test for varying crops, we constrain the dimensions of the larger image
    #// to the dimensions of the smaller image and see if they match.
    #//
    if source_width_ > target_width_:
        constrained_size_ = wp_constrain_dimensions(source_width_, source_height_, target_width_)
        expected_size_ = Array(target_width_, target_height_)
    else:
        constrained_size_ = wp_constrain_dimensions(target_width_, target_height_, source_width_)
        expected_size_ = Array(source_width_, source_height_)
    # end if
    #// If the image dimensions are within 1px of the expected size, we consider it a match.
    matched_ = wp_fuzzy_number_match(constrained_size_[0], expected_size_[0]) and wp_fuzzy_number_match(constrained_size_[1], expected_size_[1])
    return matched_
# end def wp_image_matches_ratio
#// 
#// Retrieves the image's intermediate size (resized) path, width, and height.
#// 
#// The $size parameter can be an array with the width and height respectively.
#// If the size matches the 'sizes' metadata array for width and height, then it
#// will be used. If there is no direct match, then the nearest image size larger
#// than the specified size will be used. If nothing is found, then the function
#// will break out and return false.
#// 
#// The metadata 'sizes' is used for compatible sizes that can be used for the
#// parameter $size value.
#// 
#// The url path will be given, when the $size parameter is a string.
#// 
#// If you are passing an array for the $size, you should consider using
#// add_image_size() so that a cropped version is generated. It's much more
#// efficient than having to find the closest-sized image and then having the
#// browser scale down the image.
#// 
#// @since 2.5.0
#// 
#// @param int          $post_id Attachment ID.
#// @param array|string $size    Optional. Image size. Accepts any valid image size, or an array
#// of width and height values in pixels (in that order).
#// Default 'thumbnail'.
#// @return array|false $data {
#// Array of file relative path, width, and height on success. Additionally includes absolute
#// path and URL if registered size is passed to $size parameter. False on failure.
#// 
#// @type string $file   Image's path relative to uploads directory
#// @type int    $width  Width of image
#// @type int    $height Height of image
#// @type string $path   Image's absolute filesystem path.
#// @type string $url    Image's URL.
#// }
#//
def image_get_intermediate_size(post_id_=None, size_="thumbnail", *_args_):
    
    
    imagedata_ = wp_get_attachment_metadata(post_id_)
    if (not size_) or (not php_is_array(imagedata_)) or php_empty(lambda : imagedata_["sizes"]):
        return False
    # end if
    data_ = Array()
    #// Find the best match when '$size' is an array.
    if php_is_array(size_):
        candidates_ = Array()
        if (not (php_isset(lambda : imagedata_["file"]))) and (php_isset(lambda : imagedata_["sizes"]["full"])):
            imagedata_["height"] = imagedata_["sizes"]["full"]["height"]
            imagedata_["width"] = imagedata_["sizes"]["full"]["width"]
        # end if
        for _size_,data_ in imagedata_["sizes"].items():
            #// If there's an exact match to an existing image size, short circuit.
            if php_intval(data_["width"]) == php_intval(size_[0]) and php_intval(data_["height"]) == php_intval(size_[1]):
                candidates_[data_["width"] * data_["height"]] = data_
                break
            # end if
            #// If it's not an exact match, consider larger sizes with the same aspect ratio.
            if data_["width"] >= size_[0] and data_["height"] >= size_[1]:
                #// If '0' is passed to either size, we test ratios against the original file.
                if 0 == size_[0] or 0 == size_[1]:
                    same_ratio_ = wp_image_matches_ratio(data_["width"], data_["height"], imagedata_["width"], imagedata_["height"])
                else:
                    same_ratio_ = wp_image_matches_ratio(data_["width"], data_["height"], size_[0], size_[1])
                # end if
                if same_ratio_:
                    candidates_[data_["width"] * data_["height"]] = data_
                # end if
            # end if
        # end for
        if (not php_empty(lambda : candidates_)):
            #// Sort the array by size if we have more than one candidate.
            if 1 < php_count(candidates_):
                php_ksort(candidates_)
            # end if
            data_ = php_array_shift(candidates_)
            pass
        elif (not php_empty(lambda : imagedata_["sizes"]["thumbnail"])) and imagedata_["sizes"]["thumbnail"]["width"] >= size_[0] and imagedata_["sizes"]["thumbnail"]["width"] >= size_[1]:
            data_ = imagedata_["sizes"]["thumbnail"]
        else:
            return False
        # end if
        #// Constrain the width and height attributes to the requested values.
        data_["width"], data_["height"] = image_constrain_size_for_editor(data_["width"], data_["height"], size_)
    elif (not php_empty(lambda : imagedata_["sizes"][size_])):
        data_ = imagedata_["sizes"][size_]
    # end if
    #// If we still don't have a match at this point, return false.
    if php_empty(lambda : data_):
        return False
    # end if
    #// Include the full filesystem path of the intermediate file.
    if php_empty(lambda : data_["path"]) and (not php_empty(lambda : data_["file"])) and (not php_empty(lambda : imagedata_["file"])):
        file_url_ = wp_get_attachment_url(post_id_)
        data_["path"] = path_join(php_dirname(imagedata_["file"]), data_["file"])
        data_["url"] = path_join(php_dirname(file_url_), data_["file"])
    # end if
    #// 
    #// Filters the output of image_get_intermediate_size()
    #// 
    #// @since 4.4.0
    #// 
    #// @see image_get_intermediate_size()
    #// 
    #// @param array        $data    Array of file relative path, width, and height on success. May also include
    #// file absolute path and URL.
    #// @param int          $post_id The post_id of the image attachment
    #// @param string|array $size    Registered image size or flat array of initially-requested height and width
    #// dimensions (in that order).
    #//
    return apply_filters("image_get_intermediate_size", data_, post_id_, size_)
# end def image_get_intermediate_size
#// 
#// Gets the available intermediate image size names.
#// 
#// @since 3.0.0
#// 
#// @return string[] An array of image size names.
#//
def get_intermediate_image_sizes(*_args_):
    
    
    default_sizes_ = Array("thumbnail", "medium", "medium_large", "large")
    additional_sizes_ = wp_get_additional_image_sizes()
    if (not php_empty(lambda : additional_sizes_)):
        default_sizes_ = php_array_merge(default_sizes_, php_array_keys(additional_sizes_))
    # end if
    #// 
    #// Filters the list of intermediate image sizes.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string[] $default_sizes An array of intermediate image size names. Defaults
    #// are 'thumbnail', 'medium', 'medium_large', 'large'.
    #//
    return apply_filters("intermediate_image_sizes", default_sizes_)
# end def get_intermediate_image_sizes
#// 
#// Returns a normalized list of all currently registered image sub-sizes.
#// 
#// @since 5.3.0
#// @uses wp_get_additional_image_sizes()
#// @uses get_intermediate_image_sizes()
#// 
#// @return array Associative array of the registered image sub-sizes.
#//
def wp_get_registered_image_subsizes(*_args_):
    
    
    additional_sizes_ = wp_get_additional_image_sizes()
    all_sizes_ = Array()
    for size_name_ in get_intermediate_image_sizes():
        size_data_ = Array({"width": 0, "height": 0, "crop": False})
        if (php_isset(lambda : additional_sizes_[size_name_]["width"])):
            #// For sizes added by plugins and themes.
            size_data_["width"] = php_intval(additional_sizes_[size_name_]["width"])
        else:
            #// For default sizes set in options.
            size_data_["width"] = php_intval(get_option(str(size_name_) + str("_size_w")))
        # end if
        if (php_isset(lambda : additional_sizes_[size_name_]["height"])):
            size_data_["height"] = php_intval(additional_sizes_[size_name_]["height"])
        else:
            size_data_["height"] = php_intval(get_option(str(size_name_) + str("_size_h")))
        # end if
        if php_empty(lambda : size_data_["width"]) and php_empty(lambda : size_data_["height"]):
            continue
        # end if
        if (php_isset(lambda : additional_sizes_[size_name_]["crop"])):
            size_data_["crop"] = additional_sizes_[size_name_]["crop"]
        else:
            size_data_["crop"] = get_option(str(size_name_) + str("_crop"))
        # end if
        if (not php_is_array(size_data_["crop"])) or php_empty(lambda : size_data_["crop"]):
            size_data_["crop"] = php_bool(size_data_["crop"])
        # end if
        all_sizes_[size_name_] = size_data_
    # end for
    return all_sizes_
# end def wp_get_registered_image_subsizes
#// 
#// Retrieves an image to represent an attachment.
#// 
#// @since 2.5.0
#// 
#// @param int          $attachment_id Image attachment ID.
#// @param string|int[] $size          Optional. Image size. Accepts any valid image size name, or an array of width
#// and height values in pixels (in that order). Default 'thumbnail'.
#// @param bool         $icon          Optional. Whether the image should fall back to a mime type icon. Default false.
#// @return array|false {
#// Array of image data, or boolean false if no image is available.
#// 
#// @type string $0 Image source URL.
#// @type int    $1 Image width in pixels.
#// @type int    $2 Image height in pixels.
#// }
#//
def wp_get_attachment_image_src(attachment_id_=None, size_="thumbnail", icon_=None, *_args_):
    if icon_ is None:
        icon_ = False
    # end if
    
    #// Get a thumbnail or intermediate image if there is one.
    image_ = image_downsize(attachment_id_, size_)
    if (not image_):
        src_ = False
        if icon_:
            src_ = wp_mime_type_icon(attachment_id_)
            if src_:
                #// This filter is documented in wp-includes/post.php
                icon_dir_ = apply_filters("icon_dir", ABSPATH + WPINC + "/images/media")
                src_file_ = icon_dir_ + "/" + wp_basename(src_)
                width_, height_ = php_no_error(lambda: getimagesize(src_file_))
            # end if
        # end if
        if src_ and width_ and height_:
            image_ = Array(src_, width_, height_)
        # end if
    # end if
    #// 
    #// Filters the attachment image source result.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array|false  $image         {
    #// Array of image data, or boolean false if no image is available.
    #// 
    #// @type string $0 Image source URL.
    #// @type int    $1 Image width in pixels.
    #// @type int    $2 Image height in pixels.
    #// }
    #// @param int          $attachment_id Image attachment ID.
    #// @param string|int[] $size          Requested size of image. Image size name, or array of width
    #// and height values (in that order).
    #// @param bool         $icon          Whether the image should be treated as an icon.
    #//
    return apply_filters("wp_get_attachment_image_src", image_, attachment_id_, size_, icon_)
# end def wp_get_attachment_image_src
#// 
#// Get an HTML img element representing an image attachment
#// 
#// While `$size` will accept an array, it is better to register a size with
#// add_image_size() so that a cropped version is generated. It's much more
#// efficient than having to find the closest-sized image and then having the
#// browser scale down the image.
#// 
#// @since 2.5.0
#// 
#// @param int          $attachment_id Image attachment ID.
#// @param string|array $size          Optional. Image size. Accepts any valid image size, or an array of width
#// and height values in pixels (in that order). Default 'thumbnail'.
#// @param bool         $icon          Optional. Whether the image should be treated as an icon. Default false.
#// @param string|array $attr {
#// Optional. Attributes for the image markup.
#// 
#// @type string $src    Image attachment URL.
#// @type string $class  CSS class name or space-separated list of classes.
#// Default `attachment-$size_class size-$size_class`,
#// where `$size_class` is the image size being requested.
#// @type string $alt    Image description for the alt attribute.
#// @type string $srcset The 'srcset' attribute value.
#// @type string $sizes  The 'sizes' attribute value.
#// }
#// @return string HTML img element or empty string on failure.
#//
def wp_get_attachment_image(attachment_id_=None, size_="thumbnail", icon_=None, attr_="", *_args_):
    if icon_ is None:
        icon_ = False
    # end if
    
    html_ = ""
    image_ = wp_get_attachment_image_src(attachment_id_, size_, icon_)
    if image_:
        src_, width_, height_ = image_
        hwstring_ = image_hwstring(width_, height_)
        size_class_ = size_
        if php_is_array(size_class_):
            size_class_ = php_join("x", size_class_)
        # end if
        attachment_ = get_post(attachment_id_)
        default_attr_ = Array({"src": src_, "class": str("attachment-") + str(size_class_) + str(" size-") + str(size_class_), "alt": php_trim(strip_tags(get_post_meta(attachment_id_, "_wp_attachment_image_alt", True)))})
        attr_ = wp_parse_args(attr_, default_attr_)
        #// Generate 'srcset' and 'sizes' if not already present.
        if php_empty(lambda : attr_["srcset"]):
            image_meta_ = wp_get_attachment_metadata(attachment_id_)
            if php_is_array(image_meta_):
                size_array_ = Array(absint(width_), absint(height_))
                srcset_ = wp_calculate_image_srcset(size_array_, src_, image_meta_, attachment_id_)
                sizes_ = wp_calculate_image_sizes(size_array_, src_, image_meta_, attachment_id_)
                if srcset_ and sizes_ or (not php_empty(lambda : attr_["sizes"])):
                    attr_["srcset"] = srcset_
                    if php_empty(lambda : attr_["sizes"]):
                        attr_["sizes"] = sizes_
                    # end if
                # end if
            # end if
        # end if
        #// 
        #// Filters the list of attachment image attributes.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[]     $attr       Array of attribute values for the image markup, keyed by attribute name.
        #// See wp_get_attachment_image().
        #// @param WP_Post      $attachment Image attachment post.
        #// @param string|array $size       Requested size. Image size or array of width and height values
        #// (in that order). Default 'thumbnail'.
        #//
        attr_ = apply_filters("wp_get_attachment_image_attributes", attr_, attachment_, size_)
        attr_ = php_array_map("esc_attr", attr_)
        html_ = php_rtrim(str("<img ") + str(hwstring_))
        for name_,value_ in attr_.items():
            html_ += str(" ") + str(name_) + str("=") + "\"" + value_ + "\""
        # end for
        html_ += " />"
    # end if
    return html_
# end def wp_get_attachment_image
#// 
#// Get the URL of an image attachment.
#// 
#// @since 4.4.0
#// 
#// @param int          $attachment_id Image attachment ID.
#// @param string|array $size          Optional. Image size to retrieve. Accepts any valid image size, or an array
#// of width and height values in pixels (in that order). Default 'thumbnail'.
#// @param bool         $icon          Optional. Whether the image should be treated as an icon. Default false.
#// @return string|false Attachment URL or false if no image is available.
#//
def wp_get_attachment_image_url(attachment_id_=None, size_="thumbnail", icon_=None, *_args_):
    if icon_ is None:
        icon_ = False
    # end if
    
    image_ = wp_get_attachment_image_src(attachment_id_, size_, icon_)
    return image_["0"] if (php_isset(lambda : image_["0"])) else False
# end def wp_get_attachment_image_url
#// 
#// Get the attachment path relative to the upload directory.
#// 
#// @since 4.4.1
#// @access private
#// 
#// @param string $file Attachment file name.
#// @return string Attachment path relative to the upload directory.
#//
def _wp_get_attachment_relative_path(file_=None, *_args_):
    
    
    dirname_ = php_dirname(file_)
    if "." == dirname_:
        return ""
    # end if
    if False != php_strpos(dirname_, "wp-content/uploads"):
        #// Get the directory name relative to the upload directory (back compat for pre-2.7 uploads).
        dirname_ = php_substr(dirname_, php_strpos(dirname_, "wp-content/uploads") + 18)
        dirname_ = php_ltrim(dirname_, "/")
    # end if
    return dirname_
# end def _wp_get_attachment_relative_path
#// 
#// Get the image size as array from its meta data.
#// 
#// Used for responsive images.
#// 
#// @since 4.4.0
#// @access private
#// 
#// @param string $size_name  Image size. Accepts any valid image size name ('thumbnail', 'medium', etc.).
#// @param array  $image_meta The image meta data.
#// @return array|bool The image meta data as returned by `wp_get_attachment_metadata()`.
#//
def _wp_get_image_size_from_meta(size_name_=None, image_meta_=None, *_args_):
    
    
    if "full" == size_name_:
        return Array(absint(image_meta_["width"]), absint(image_meta_["height"]))
    elif (not php_empty(lambda : image_meta_["sizes"][size_name_])):
        return Array(absint(image_meta_["sizes"][size_name_]["width"]), absint(image_meta_["sizes"][size_name_]["height"]))
    # end if
    return False
# end def _wp_get_image_size_from_meta
#// 
#// Retrieves the value for an image attachment's 'srcset' attribute.
#// 
#// @since 4.4.0
#// 
#// @see wp_calculate_image_srcset()
#// 
#// @param int          $attachment_id Image attachment ID.
#// @param array|string $size          Optional. Image size. Accepts any valid image size, or an array of
#// width and height values in pixels (in that order). Default 'medium'.
#// @param array        $image_meta    Optional. The image meta data as returned by 'wp_get_attachment_metadata()'.
#// Default null.
#// @return string|bool A 'srcset' value string or false.
#//
def wp_get_attachment_image_srcset(attachment_id_=None, size_="medium", image_meta_=None, *_args_):
    if image_meta_ is None:
        image_meta_ = None
    # end if
    
    image_ = wp_get_attachment_image_src(attachment_id_, size_)
    if (not image_):
        return False
    # end if
    if (not php_is_array(image_meta_)):
        image_meta_ = wp_get_attachment_metadata(attachment_id_)
    # end if
    image_src_ = image_[0]
    size_array_ = Array(absint(image_[1]), absint(image_[2]))
    return wp_calculate_image_srcset(size_array_, image_src_, image_meta_, attachment_id_)
# end def wp_get_attachment_image_srcset
#// 
#// A helper function to calculate the image sources to include in a 'srcset' attribute.
#// 
#// @since 4.4.0
#// 
#// @param int[]  $size_array    {
#// An array of width and height values.
#// 
#// @type int $0 The width in pixels.
#// @type int $1 The height in pixels.
#// }
#// @param string $image_src     The 'src' of the image.
#// @param array  $image_meta    The image meta data as returned by 'wp_get_attachment_metadata()'.
#// @param int    $attachment_id Optional. The image attachment ID. Default 0.
#// @return string|bool          The 'srcset' attribute value. False on error or when only one source exists.
#//
def wp_calculate_image_srcset(size_array_=None, image_src_=None, image_meta_=None, attachment_id_=0, *_args_):
    
    
    #// 
    #// Let plugins pre-filter the image meta to be able to fix inconsistencies in the stored data.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array  $image_meta    The image meta data as returned by 'wp_get_attachment_metadata()'.
    #// @param int[]  $size_array    {
    #// An array of requested width and height values.
    #// 
    #// @type int $0 The width in pixels.
    #// @type int $1 The height in pixels.
    #// }
    #// @param string $image_src     The 'src' of the image.
    #// @param int    $attachment_id The image attachment ID or 0 if not supplied.
    #//
    image_meta_ = apply_filters("wp_calculate_image_srcset_meta", image_meta_, size_array_, image_src_, attachment_id_)
    if php_empty(lambda : image_meta_["sizes"]) or (not (php_isset(lambda : image_meta_["file"]))) or php_strlen(image_meta_["file"]) < 4:
        return False
    # end if
    image_sizes_ = image_meta_["sizes"]
    #// Get the width and height of the image.
    image_width_ = php_int(size_array_[0])
    image_height_ = php_int(size_array_[1])
    #// Bail early if error/no width.
    if image_width_ < 1:
        return False
    # end if
    image_basename_ = wp_basename(image_meta_["file"])
    #// 
    #// WordPress flattens animated GIFs into one frame when generating intermediate sizes.
    #// To avoid hiding animation in user content, if src is a full size GIF, a srcset attribute is not generated.
    #// If src is an intermediate size GIF, the full size is excluded from srcset to keep a flattened GIF from becoming animated.
    #//
    if (not (php_isset(lambda : image_sizes_["thumbnail"]["mime-type"]))) or "image/gif" != image_sizes_["thumbnail"]["mime-type"]:
        image_sizes_[-1] = Array({"width": image_meta_["width"], "height": image_meta_["height"], "file": image_basename_})
    elif php_strpos(image_src_, image_meta_["file"]):
        return False
    # end if
    #// Retrieve the uploads sub-directory from the full size image.
    dirname_ = _wp_get_attachment_relative_path(image_meta_["file"])
    if dirname_:
        dirname_ = trailingslashit(dirname_)
    # end if
    upload_dir_ = wp_get_upload_dir()
    image_baseurl_ = trailingslashit(upload_dir_["baseurl"]) + dirname_
    #// 
    #// If currently on HTTPS, prefer HTTPS URLs when we know they're supported by the domain
    #// (which is to say, when they share the domain name of the current request).
    #//
    if is_ssl() and "https" != php_substr(image_baseurl_, 0, 5) and php_parse_url(image_baseurl_, PHP_URL_HOST) == PHP_SERVER["HTTP_HOST"]:
        image_baseurl_ = set_url_scheme(image_baseurl_, "https")
    # end if
    #// 
    #// Images that have been edited in WordPress after being uploaded will
    #// contain a unique hash. Look for that hash and use it later to filter
    #// out images that are leftovers from previous versions.
    #//
    image_edited_ = php_preg_match("/-e[0-9]{13}/", wp_basename(image_src_), image_edit_hash_)
    #// 
    #// Filters the maximum image width to be included in a 'srcset' attribute.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int   $max_width  The maximum image width to be included in the 'srcset'. Default '2048'.
    #// @param int[] $size_array {
    #// An array of requested width and height values.
    #// 
    #// @type int $0 The width in pixels.
    #// @type int $1 The height in pixels.
    #// }
    #//
    max_srcset_image_width_ = apply_filters("max_srcset_image_width", 2048, size_array_)
    #// Array to hold URL candidates.
    sources_ = Array()
    #// 
    #// To make sure the ID matches our image src, we will check to see if any sizes in our attachment
    #// meta match our $image_src. If no matches are found we don't return a srcset to avoid serving
    #// an incorrect image. See #35045.
    #//
    src_matched_ = False
    #// 
    #// Loop through available images. Only use images that are resized
    #// versions of the same edit.
    #//
    for image_ in image_sizes_:
        is_src_ = False
        #// Check if image meta isn't corrupted.
        if (not php_is_array(image_)):
            continue
        # end if
        #// If the file name is part of the `src`, we've confirmed a match.
        if (not src_matched_) and False != php_strpos(image_src_, dirname_ + image_["file"]):
            src_matched_ = True
            is_src_ = True
        # end if
        #// Filter out images that are from previous edits.
        if image_edited_ and (not php_strpos(image_["file"], image_edit_hash_[0])):
            continue
        # end if
        #// 
        #// Filters out images that are wider than '$max_srcset_image_width' unless
        #// that file is in the 'src' attribute.
        #//
        if max_srcset_image_width_ and image_["width"] > max_srcset_image_width_ and (not is_src_):
            continue
        # end if
        #// If the image dimensions are within 1px of the expected size, use it.
        if wp_image_matches_ratio(image_width_, image_height_, image_["width"], image_["height"]):
            #// Add the URL, descriptor, and value to the sources array to be returned.
            source_ = Array({"url": image_baseurl_ + image_["file"], "descriptor": "w", "value": image_["width"]})
            #// The 'src' image has to be the first in the 'srcset', because of a bug in iOS8. See #35030.
            if is_src_:
                sources_ = Array({image_["width"]: source_}) + sources_
            else:
                sources_[image_["width"]] = source_
            # end if
        # end if
    # end for
    #// 
    #// Filters an image's 'srcset' sources.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array  $sources {
    #// One or more arrays of source data to include in the 'srcset'.
    #// 
    #// @type array $width {
    #// @type string $url        The URL of an image source.
    #// @type string $descriptor The descriptor type used in the image candidate string,
    #// either 'w' or 'x'.
    #// @type int    $value      The source width if paired with a 'w' descriptor, or a
    #// pixel density value if paired with an 'x' descriptor.
    #// }
    #// }
    #// @param array $size_array     {
    #// An array of requested width and height values.
    #// 
    #// @type int $0 The width in pixels.
    #// @type int $1 The height in pixels.
    #// }
    #// @param string $image_src     The 'src' of the image.
    #// @param array  $image_meta    The image meta data as returned by 'wp_get_attachment_metadata()'.
    #// @param int    $attachment_id Image attachment ID or 0.
    #//
    sources_ = apply_filters("wp_calculate_image_srcset", sources_, size_array_, image_src_, image_meta_, attachment_id_)
    #// Only return a 'srcset' value if there is more than one source.
    if (not src_matched_) or (not php_is_array(sources_)) or php_count(sources_) < 2:
        return False
    # end if
    srcset_ = ""
    for source_ in sources_:
        srcset_ += php_str_replace(" ", "%20", source_["url"]) + " " + source_["value"] + source_["descriptor"] + ", "
    # end for
    return php_rtrim(srcset_, ", ")
# end def wp_calculate_image_srcset
#// 
#// Retrieves the value for an image attachment's 'sizes' attribute.
#// 
#// @since 4.4.0
#// 
#// @see wp_calculate_image_sizes()
#// 
#// @param int          $attachment_id Image attachment ID.
#// @param array|string $size          Optional. Image size. Accepts any valid image size, or an array of width
#// and height values in pixels (in that order). Default 'medium'.
#// @param array        $image_meta    Optional. The image meta data as returned by 'wp_get_attachment_metadata()'.
#// Default null.
#// @return string|bool A valid source size value for use in a 'sizes' attribute or false.
#//
def wp_get_attachment_image_sizes(attachment_id_=None, size_="medium", image_meta_=None, *_args_):
    if image_meta_ is None:
        image_meta_ = None
    # end if
    
    image_ = wp_get_attachment_image_src(attachment_id_, size_)
    if (not image_):
        return False
    # end if
    if (not php_is_array(image_meta_)):
        image_meta_ = wp_get_attachment_metadata(attachment_id_)
    # end if
    image_src_ = image_[0]
    size_array_ = Array(absint(image_[1]), absint(image_[2]))
    return wp_calculate_image_sizes(size_array_, image_src_, image_meta_, attachment_id_)
# end def wp_get_attachment_image_sizes
#// 
#// Creates a 'sizes' attribute value for an image.
#// 
#// @since 4.4.0
#// 
#// @param array|string $size          Image size to retrieve. Accepts any valid image size, or an array
#// of width and height values in pixels (in that order). Default 'medium'.
#// @param string       $image_src     Optional. The URL to the image file. Default null.
#// @param array        $image_meta    Optional. The image meta data as returned by 'wp_get_attachment_metadata()'.
#// Default null.
#// @param int          $attachment_id Optional. Image attachment ID. Either `$image_meta` or `$attachment_id`
#// is needed when using the image size name as argument for `$size`. Default 0.
#// @return string|bool A valid source size value for use in a 'sizes' attribute or false.
#//
def wp_calculate_image_sizes(size_=None, image_src_=None, image_meta_=None, attachment_id_=0, *_args_):
    if image_src_ is None:
        image_src_ = None
    # end if
    if image_meta_ is None:
        image_meta_ = None
    # end if
    
    width_ = 0
    if php_is_array(size_):
        width_ = absint(size_[0])
    elif php_is_string(size_):
        if (not image_meta_) and attachment_id_:
            image_meta_ = wp_get_attachment_metadata(attachment_id_)
        # end if
        if php_is_array(image_meta_):
            size_array_ = _wp_get_image_size_from_meta(size_, image_meta_)
            if size_array_:
                width_ = absint(size_array_[0])
            # end if
        # end if
    # end if
    if (not width_):
        return False
    # end if
    #// Setup the default 'sizes' attribute.
    sizes_ = php_sprintf("(max-width: %1$dpx) 100vw, %1$dpx", width_)
    #// 
    #// Filters the output of 'wp_calculate_image_sizes()'.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string       $sizes         A source size value for use in a 'sizes' attribute.
    #// @param array|string $size          Requested size. Image size or array of width and height values
    #// in pixels (in that order).
    #// @param string|null  $image_src     The URL to the image file or null.
    #// @param array|null   $image_meta    The image meta data as returned by wp_get_attachment_metadata() or null.
    #// @param int          $attachment_id Image attachment ID of the original image or 0.
    #//
    return apply_filters("wp_calculate_image_sizes", sizes_, size_, image_src_, image_meta_, attachment_id_)
# end def wp_calculate_image_sizes
#// 
#// Filters 'img' elements in post content to add 'srcset' and 'sizes' attributes.
#// 
#// @since 4.4.0
#// 
#// @see wp_image_add_srcset_and_sizes()
#// 
#// @param string $content The raw post content to be filtered.
#// @return string Converted content with 'srcset' and 'sizes' attributes added to images.
#//
def wp_make_content_images_responsive(content_=None, *_args_):
    
    
    if (not preg_match_all("/<img [^>]+>/", content_, matches_)):
        return content_
    # end if
    selected_images_ = Array()
    attachment_ids_ = Array()
    for image_ in matches_[0]:
        if False == php_strpos(image_, " srcset=") and php_preg_match("/wp-image-([0-9]+)/i", image_, class_id_):
            attachment_id_ = absint(class_id_[1])
            if attachment_id_:
                #// 
                #// If exactly the same image tag is used more than once, overwrite it.
                #// All identical tags will be replaced later with 'str_replace()'.
                #//
                selected_images_[image_] = attachment_id_
                #// Overwrite the ID when the same image is included more than once.
                attachment_ids_[attachment_id_] = True
            # end if
        # end if
    # end for
    if php_count(attachment_ids_) > 1:
        #// 
        #// Warm the object cache with post and meta information for all found
        #// images to avoid making individual database calls.
        #//
        _prime_post_caches(php_array_keys(attachment_ids_), False, True)
    # end if
    for image_,attachment_id_ in selected_images_.items():
        image_meta_ = wp_get_attachment_metadata(attachment_id_)
        content_ = php_str_replace(image_, wp_image_add_srcset_and_sizes(image_, image_meta_, attachment_id_), content_)
    # end for
    return content_
# end def wp_make_content_images_responsive
#// 
#// Adds 'srcset' and 'sizes' attributes to an existing 'img' element.
#// 
#// @since 4.4.0
#// 
#// @see wp_calculate_image_srcset()
#// @see wp_calculate_image_sizes()
#// 
#// @param string $image         An HTML 'img' element to be filtered.
#// @param array  $image_meta    The image meta data as returned by 'wp_get_attachment_metadata()'.
#// @param int    $attachment_id Image attachment ID.
#// @return string Converted 'img' element with 'srcset' and 'sizes' attributes added.
#//
def wp_image_add_srcset_and_sizes(image_=None, image_meta_=None, attachment_id_=None, *_args_):
    
    
    #// Ensure the image meta exists.
    if php_empty(lambda : image_meta_["sizes"]):
        return image_
    # end if
    image_src_ = match_src_[1] if php_preg_match("/src=\"([^\"]+)\"/", image_, match_src_) else ""
    image_src_ = php_explode("?", image_src_)
    #// Return early if we couldn't get the image source.
    if (not image_src_):
        return image_
    # end if
    #// Bail early if an image has been inserted and later edited.
    if php_preg_match("/-e[0-9]{13}/", image_meta_["file"], img_edit_hash_) and php_strpos(wp_basename(image_src_), img_edit_hash_[0]) == False:
        return image_
    # end if
    width_ = php_int(match_width_[1]) if php_preg_match("/ width=\"([0-9]+)\"/", image_, match_width_) else 0
    height_ = php_int(match_height_[1]) if php_preg_match("/ height=\"([0-9]+)\"/", image_, match_height_) else 0
    if (not width_) or (not height_):
        #// 
        #// If attempts to parse the size value failed, attempt to use the image meta data to match
        #// the image file name from 'src' against the available sizes for an attachment.
        #//
        image_filename_ = wp_basename(image_src_)
        if wp_basename(image_meta_["file"]) == image_filename_:
            width_ = php_int(image_meta_["width"])
            height_ = php_int(image_meta_["height"])
        else:
            for image_size_data_ in image_meta_["sizes"]:
                if image_filename_ == image_size_data_["file"]:
                    width_ = php_int(image_size_data_["width"])
                    height_ = php_int(image_size_data_["height"])
                    break
                # end if
            # end for
        # end if
    # end if
    if (not width_) or (not height_):
        return image_
    # end if
    size_array_ = Array(width_, height_)
    srcset_ = wp_calculate_image_srcset(size_array_, image_src_, image_meta_, attachment_id_)
    if srcset_:
        #// Check if there is already a 'sizes' attribute.
        sizes_ = php_strpos(image_, " sizes=")
        if (not sizes_):
            sizes_ = wp_calculate_image_sizes(size_array_, image_src_, image_meta_, attachment_id_)
        # end if
    # end if
    if srcset_ and sizes_:
        #// Format the 'srcset' and 'sizes' string and escape attributes.
        attr_ = php_sprintf(" srcset=\"%s\"", esc_attr(srcset_))
        if php_is_string(sizes_):
            attr_ += php_sprintf(" sizes=\"%s\"", esc_attr(sizes_))
        # end if
        #// Add 'srcset' and 'sizes' attributes to the image markup.
        image_ = php_preg_replace("/<img ([^>]+?)[\\/ ]*>/", "<img $1" + attr_ + " />", image_)
    # end if
    return image_
# end def wp_image_add_srcset_and_sizes
#// 
#// Adds a 'wp-post-image' class to post thumbnails. Internal use only.
#// 
#// Uses the {@see 'begin_fetch_post_thumbnail_html'} and {@see 'end_fetch_post_thumbnail_html'}
#// action hooks to dynamically add/remove itself so as to only filter post thumbnails.
#// 
#// @ignore
#// @since 2.9.0
#// 
#// @param string[] $attr Array of thumbnail attributes including src, class, alt, title, keyed by attribute name.
#// @return string[] Modified array of attributes including the new 'wp-post-image' class.
#//
def _wp_post_thumbnail_class_filter(attr_=None, *_args_):
    
    
    attr_["class"] += " wp-post-image"
    return attr_
# end def _wp_post_thumbnail_class_filter
#// 
#// Adds '_wp_post_thumbnail_class_filter' callback to the 'wp_get_attachment_image_attributes'
#// filter hook. Internal use only.
#// 
#// @ignore
#// @since 2.9.0
#// 
#// @param string[] $attr Array of thumbnail attributes including src, class, alt, title, keyed by attribute name.
#//
def _wp_post_thumbnail_class_filter_add(attr_=None, *_args_):
    
    
    add_filter("wp_get_attachment_image_attributes", "_wp_post_thumbnail_class_filter")
# end def _wp_post_thumbnail_class_filter_add
#// 
#// Removes the '_wp_post_thumbnail_class_filter' callback from the 'wp_get_attachment_image_attributes'
#// filter hook. Internal use only.
#// 
#// @ignore
#// @since 2.9.0
#// 
#// @param string[] $attr Array of thumbnail attributes including src, class, alt, title, keyed by attribute name.
#//
def _wp_post_thumbnail_class_filter_remove(attr_=None, *_args_):
    
    
    remove_filter("wp_get_attachment_image_attributes", "_wp_post_thumbnail_class_filter")
# end def _wp_post_thumbnail_class_filter_remove
add_shortcode("wp_caption", "img_caption_shortcode")
add_shortcode("caption", "img_caption_shortcode")
#// 
#// Builds the Caption shortcode output.
#// 
#// Allows a plugin to replace the content that would otherwise be returned. The
#// filter is {@see 'img_caption_shortcode'} and passes an empty string, the attr
#// parameter and the content parameter values.
#// 
#// The supported attributes for the shortcode are 'id', 'caption_id', 'align',
#// 'width', 'caption', and 'class'.
#// 
#// @since 2.6.0
#// @since 3.9.0 The `class` attribute was added.
#// @since 5.1.0 The `caption_id` attribute was added.
#// 
#// @param array  $attr {
#// Attributes of the caption shortcode.
#// 
#// @type string $id         ID of the image and caption container element, i.e. `<figure>` or `<div>`.
#// @type string $caption_id ID of the caption element, i.e. `<figcaption>` or `<p>`.
#// @type string $align      Class name that aligns the caption. Default 'alignnone'. Accepts 'alignleft',
#// 'aligncenter', alignright', 'alignnone'.
#// @type int    $width      The width of the caption, in pixels.
#// @type string $caption    The caption text.
#// @type string $class      Additional class name(s) added to the caption container.
#// }
#// @param string $content Shortcode content.
#// @return string HTML content to display the caption.
#//
def img_caption_shortcode(attr_=None, content_=None, *_args_):
    if content_ is None:
        content_ = None
    # end if
    
    #// New-style shortcode with the caption inside the shortcode with the link and image tags.
    if (not (php_isset(lambda : attr_["caption"]))):
        if php_preg_match("#((?:<a [^>]+>\\s*)?<img [^>]+>(?:\\s*</a>)?)(.*)#is", content_, matches_):
            content_ = matches_[1]
            attr_["caption"] = php_trim(matches_[2])
        # end if
    elif php_strpos(attr_["caption"], "<") != False:
        attr_["caption"] = wp_kses(attr_["caption"], "post")
    # end if
    #// 
    #// Filters the default caption shortcode output.
    #// 
    #// If the filtered output isn't empty, it will be used instead of generating
    #// the default caption template.
    #// 
    #// @since 2.6.0
    #// 
    #// @see img_caption_shortcode()
    #// 
    #// @param string $output  The caption output. Default empty.
    #// @param array  $attr    Attributes of the caption shortcode.
    #// @param string $content The image element, possibly wrapped in a hyperlink.
    #//
    output_ = apply_filters("img_caption_shortcode", "", attr_, content_)
    if (not php_empty(lambda : output_)):
        return output_
    # end if
    atts_ = shortcode_atts(Array({"id": "", "caption_id": "", "align": "alignnone", "width": "", "caption": "", "class": ""}), attr_, "caption")
    atts_["width"] = php_int(atts_["width"])
    if atts_["width"] < 1 or php_empty(lambda : atts_["caption"]):
        return content_
    # end if
    id_ = ""
    caption_id_ = ""
    describedby_ = ""
    if atts_["id"]:
        atts_["id"] = sanitize_html_class(atts_["id"])
        id_ = "id=\"" + esc_attr(atts_["id"]) + "\" "
    # end if
    if atts_["caption_id"]:
        atts_["caption_id"] = sanitize_html_class(atts_["caption_id"])
    elif atts_["id"]:
        atts_["caption_id"] = "caption-" + php_str_replace("_", "-", atts_["id"])
    # end if
    if atts_["caption_id"]:
        caption_id_ = "id=\"" + esc_attr(atts_["caption_id"]) + "\" "
        describedby_ = "aria-describedby=\"" + esc_attr(atts_["caption_id"]) + "\" "
    # end if
    class_ = php_trim("wp-caption " + atts_["align"] + " " + atts_["class"])
    html5_ = current_theme_supports("html5", "caption")
    #// HTML5 captions never added the extra 10px to the image width.
    width_ = atts_["width"] if html5_ else 10 + atts_["width"]
    #// 
    #// Filters the width of an image's caption.
    #// 
    #// By default, the caption is 10 pixels greater than the width of the image,
    #// to prevent post content from running up against a floated image.
    #// 
    #// @since 3.7.0
    #// 
    #// @see img_caption_shortcode()
    #// 
    #// @param int    $width    Width of the caption in pixels. To remove this inline style,
    #// return zero.
    #// @param array  $atts     Attributes of the caption shortcode.
    #// @param string $content  The image element, possibly wrapped in a hyperlink.
    #//
    caption_width_ = apply_filters("img_caption_shortcode_width", width_, atts_, content_)
    style_ = ""
    if caption_width_:
        style_ = "style=\"width: " + php_int(caption_width_) + "px\" "
    # end if
    if html5_:
        html_ = php_sprintf("<figure %s%s%sclass=\"%s\">%s%s</figure>", id_, describedby_, style_, esc_attr(class_), do_shortcode(content_), php_sprintf("<figcaption %sclass=\"wp-caption-text\">%s</figcaption>", caption_id_, atts_["caption"]))
    else:
        html_ = php_sprintf("<div %s%sclass=\"%s\">%s%s</div>", id_, style_, esc_attr(class_), php_str_replace("<img ", "<img " + describedby_, do_shortcode(content_)), php_sprintf("<p %sclass=\"wp-caption-text\">%s</p>", caption_id_, atts_["caption"]))
    # end if
    return html_
# end def img_caption_shortcode
add_shortcode("gallery", "gallery_shortcode")
#// 
#// Builds the Gallery shortcode output.
#// 
#// This implements the functionality of the Gallery Shortcode for displaying
#// WordPress images on a post.
#// 
#// @since 2.5.0
#// 
#// @staticvar int $instance
#// 
#// @param array $attr {
#// Attributes of the gallery shortcode.
#// 
#// @type string       $order      Order of the images in the gallery. Default 'ASC'. Accepts 'ASC', 'DESC'.
#// @type string       $orderby    The field to use when ordering the images. Default 'menu_order ID'.
#// Accepts any valid SQL ORDERBY statement.
#// @type int          $id         Post ID.
#// @type string       $itemtag    HTML tag to use for each image in the gallery.
#// Default 'dl', or 'figure' when the theme registers HTML5 gallery support.
#// @type string       $icontag    HTML tag to use for each image's icon.
#// Default 'dt', or 'div' when the theme registers HTML5 gallery support.
#// @type string       $captiontag HTML tag to use for each image's caption.
#// Default 'dd', or 'figcaption' when the theme registers HTML5 gallery support.
#// @type int          $columns    Number of columns of images to display. Default 3.
#// @type string|array $size       Size of the images to display. Accepts any valid image size, or an array of width
#// and height values in pixels (in that order). Default 'thumbnail'.
#// @type string       $ids        A comma-separated list of IDs of attachments to display. Default empty.
#// @type string       $include    A comma-separated list of IDs of attachments to include. Default empty.
#// @type string       $exclude    A comma-separated list of IDs of attachments to exclude. Default empty.
#// @type string       $link       What to link each image to. Default empty (links to the attachment page).
#// Accepts 'file', 'none'.
#// }
#// @return string HTML content to display gallery.
#//
def gallery_shortcode(attr_=None, *_args_):
    
    
    post_ = get_post()
    instance_ = 0
    instance_ += 1
    if (not php_empty(lambda : attr_["ids"])):
        #// 'ids' is explicitly ordered, unless you specify otherwise.
        if php_empty(lambda : attr_["orderby"]):
            attr_["orderby"] = "post__in"
        # end if
        attr_["include"] = attr_["ids"]
    # end if
    #// 
    #// Filters the default gallery shortcode output.
    #// 
    #// If the filtered output isn't empty, it will be used instead of generating
    #// the default gallery template.
    #// 
    #// @since 2.5.0
    #// @since 4.2.0 The `$instance` parameter was added.
    #// 
    #// @see gallery_shortcode()
    #// 
    #// @param string $output   The gallery output. Default empty.
    #// @param array  $attr     Attributes of the gallery shortcode.
    #// @param int    $instance Unique numeric ID of this gallery shortcode instance.
    #//
    output_ = apply_filters("post_gallery", "", attr_, instance_)
    if (not php_empty(lambda : output_)):
        return output_
    # end if
    html5_ = current_theme_supports("html5", "gallery")
    atts_ = shortcode_atts(Array({"order": "ASC", "orderby": "menu_order ID", "id": post_.ID if post_ else 0, "itemtag": "figure" if html5_ else "dl", "icontag": "div" if html5_ else "dt", "captiontag": "figcaption" if html5_ else "dd", "columns": 3, "size": "thumbnail", "include": "", "exclude": "", "link": ""}), attr_, "gallery")
    id_ = php_intval(atts_["id"])
    if (not php_empty(lambda : atts_["include"])):
        _attachments_ = get_posts(Array({"include": atts_["include"], "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": atts_["order"], "orderby": atts_["orderby"]}))
        attachments_ = Array()
        for key_,val_ in _attachments_.items():
            attachments_[val_.ID] = _attachments_[key_]
        # end for
    elif (not php_empty(lambda : atts_["exclude"])):
        attachments_ = get_children(Array({"post_parent": id_, "exclude": atts_["exclude"], "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": atts_["order"], "orderby": atts_["orderby"]}))
    else:
        attachments_ = get_children(Array({"post_parent": id_, "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": atts_["order"], "orderby": atts_["orderby"]}))
    # end if
    if php_empty(lambda : attachments_):
        return ""
    # end if
    if is_feed():
        output_ = "\n"
        for att_id_,attachment_ in attachments_.items():
            output_ += wp_get_attachment_link(att_id_, atts_["size"], True) + "\n"
        # end for
        return output_
    # end if
    itemtag_ = tag_escape(atts_["itemtag"])
    captiontag_ = tag_escape(atts_["captiontag"])
    icontag_ = tag_escape(atts_["icontag"])
    valid_tags_ = wp_kses_allowed_html("post")
    if (not (php_isset(lambda : valid_tags_[itemtag_]))):
        itemtag_ = "dl"
    # end if
    if (not (php_isset(lambda : valid_tags_[captiontag_]))):
        captiontag_ = "dd"
    # end if
    if (not (php_isset(lambda : valid_tags_[icontag_]))):
        icontag_ = "dt"
    # end if
    columns_ = php_intval(atts_["columns"])
    itemwidth_ = floor(100 / columns_) if columns_ > 0 else 100
    float_ = "right" if is_rtl() else "left"
    selector_ = str("gallery-") + str(instance_)
    gallery_style_ = ""
    #// 
    #// Filters whether to print default gallery styles.
    #// 
    #// @since 3.1.0
    #// 
    #// @param bool $print Whether to print default gallery styles.
    #// Defaults to false if the theme supports HTML5 galleries.
    #// Otherwise, defaults to true.
    #//
    if apply_filters("use_default_gallery_style", (not html5_)):
        type_attr_ = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
        gallery_style_ = str("\n        <style") + str(type_attr_) + str(">\n           #") + str(selector_) + str(""" {\n              margin: auto;\n         }\n         #""") + str(selector_) + str(" .gallery-item {\n                float: ") + str(float_) + str(""";\n                margin-top: 10px;\n             text-align: center;\n               width: """) + str(itemwidth_) + str("%;\n           }\n         #") + str(selector_) + str(""" img {\n              border: 2px solid #cfcfcf;\n            }\n         #""") + str(selector_) + str(""" .gallery-caption {\n               margin-left: 0;\n           }\n         /* see gallery_shortcode() in wp-includes/media.php */\n        </style>\n      """)
    # end if
    size_class_ = sanitize_html_class(atts_["size"])
    gallery_div_ = str("<div id='") + str(selector_) + str("' class='gallery galleryid-") + str(id_) + str(" gallery-columns-") + str(columns_) + str(" gallery-size-") + str(size_class_) + str("'>")
    #// 
    #// Filters the default gallery shortcode CSS styles.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $gallery_style Default CSS styles and opening HTML div container
    #// for the gallery shortcode output.
    #//
    output_ = apply_filters("gallery_style", gallery_style_ + gallery_div_)
    i_ = 0
    for id_,attachment_ in attachments_.items():
        attr_ = Array({"aria-describedby": str(selector_) + str("-") + str(id_)}) if php_trim(attachment_.post_excerpt) else ""
        if (not php_empty(lambda : atts_["link"])) and "file" == atts_["link"]:
            image_output_ = wp_get_attachment_link(id_, atts_["size"], False, False, False, attr_)
        elif (not php_empty(lambda : atts_["link"])) and "none" == atts_["link"]:
            image_output_ = wp_get_attachment_image(id_, atts_["size"], False, attr_)
        else:
            image_output_ = wp_get_attachment_link(id_, atts_["size"], True, False, False, attr_)
        # end if
        image_meta_ = wp_get_attachment_metadata(id_)
        orientation_ = ""
        if (php_isset(lambda : image_meta_["height"]) and php_isset(lambda : image_meta_["width"])):
            orientation_ = "portrait" if image_meta_["height"] > image_meta_["width"] else "landscape"
        # end if
        output_ += str("<") + str(itemtag_) + str(" class='gallery-item'>")
        output_ += str("\n          <") + str(icontag_) + str(" class='gallery-icon ") + str(orientation_) + str("'>\n              ") + str(image_output_) + str("\n           </") + str(icontag_) + str(">")
        if captiontag_ and php_trim(attachment_.post_excerpt):
            output_ += str("\n              <") + str(captiontag_) + str(" class='wp-caption-text gallery-caption' id='") + str(selector_) + str("-") + str(id_) + str("'>\n                ") + wptexturize(attachment_.post_excerpt) + str("\n                </") + str(captiontag_) + str(">")
        # end if
        output_ += str("</") + str(itemtag_) + str(">")
        i_ += 1
        i_ += 1
        if (not html5_) and columns_ > 0 and 0 == i_ % columns_:
            output_ += "<br style=\"clear: both\" />"
        # end if
    # end for
    if (not html5_) and columns_ > 0 and 0 != i_ % columns_:
        output_ += "\n          <br style='clear: both' />"
    # end if
    output_ += "\n      </div>\n"
    return output_
# end def gallery_shortcode
#// 
#// Outputs the templates used by playlists.
#// 
#// @since 3.9.0
#//
def wp_underscore_playlist_templates(*_args_):
    
    
    php_print("""<script type=\"text/html\" id=\"tmpl-wp-playlist-current-item\">
    <# if ( data.image ) { #>
    <img src=\"{{ data.thumb.src }}\" alt=\"\" />
    <# } #>
    <div class=\"wp-playlist-caption\">
    <span class=\"wp-playlist-item-meta wp-playlist-item-title\">
    """)
    #// translators: %s: Playlist item title.
    php_printf(_x("&#8220;%s&#8221;", "playlist item title"), "{{ data.title }}")
    php_print("""       </span>
    <# if ( data.meta.album ) { #><span class=\"wp-playlist-item-meta wp-playlist-item-album\">{{ data.meta.album }}</span><# } #>
    <# if ( data.meta.artist ) { #><span class=\"wp-playlist-item-meta wp-playlist-item-artist\">{{ data.meta.artist }}</span><# } #>
    </div>
    </script>
    <script type=\"text/html\" id=\"tmpl-wp-playlist-item\">
    <div class=\"wp-playlist-item\">
    <a class=\"wp-playlist-caption\" href=\"{{ data.src }}\">
    {{ data.index ? ( data.index + '. ' ) : '' }}
    <# if ( data.caption ) { #>
    {{ data.caption }}
    <# } else { #>
    <span class=\"wp-playlist-item-title\">
    """)
    #// translators: %s: Playlist item title.
    php_printf(_x("&#8220;%s&#8221;", "playlist item title"), "{{{ data.title }}}")
    php_print("""               </span>
    <# if ( data.artists && data.meta.artist ) { #>
    <span class=\"wp-playlist-item-artist\"> &mdash; {{ data.meta.artist }}</span>
    <# } #>
    <# } #>
    </a>
    <# if ( data.meta.length_formatted ) { #>
    <div class=\"wp-playlist-item-length\">{{ data.meta.length_formatted }}</div>
    <# } #>
    </div>
    </script>
    """)
# end def wp_underscore_playlist_templates
#// 
#// Outputs and enqueue default scripts and styles for playlists.
#// 
#// @since 3.9.0
#// 
#// @param string $type Type of playlist. Accepts 'audio' or 'video'.
#//
def wp_playlist_scripts(type_=None, *_args_):
    
    
    wp_enqueue_style("wp-mediaelement")
    wp_enqueue_script("wp-playlist")
    php_print("<!--[if lt IE 9]><script>document.createElement('")
    php_print(esc_js(type_))
    php_print("');</script><![endif]-->\n   ")
    add_action("wp_footer", "wp_underscore_playlist_templates", 0)
    add_action("admin_footer", "wp_underscore_playlist_templates", 0)
# end def wp_playlist_scripts
#// 
#// Builds the Playlist shortcode output.
#// 
#// This implements the functionality of the playlist shortcode for displaying
#// a collection of WordPress audio or video files in a post.
#// 
#// @since 3.9.0
#// 
#// @global int $content_width
#// @staticvar int $instance
#// 
#// @param array $attr {
#// Array of default playlist attributes.
#// 
#// @type string  $type         Type of playlist to display. Accepts 'audio' or 'video'. Default 'audio'.
#// @type string  $order        Designates ascending or descending order of items in the playlist.
#// Accepts 'ASC', 'DESC'. Default 'ASC'.
#// @type string  $orderby      Any column, or columns, to sort the playlist. If $ids are
#// passed, this defaults to the order of the $ids array ('post__in').
#// Otherwise default is 'menu_order ID'.
#// @type int     $id           If an explicit $ids array is not present, this parameter
#// will determine which attachments are used for the playlist.
#// Default is the current post ID.
#// @type array   $ids          Create a playlist out of these explicit attachment IDs. If empty,
#// a playlist will be created from all $type attachments of $id.
#// Default empty.
#// @type array   $exclude      List of specific attachment IDs to exclude from the playlist. Default empty.
#// @type string  $style        Playlist style to use. Accepts 'light' or 'dark'. Default 'light'.
#// @type bool    $tracklist    Whether to show or hide the playlist. Default true.
#// @type bool    $tracknumbers Whether to show or hide the numbers next to entries in the playlist. Default true.
#// @type bool    $images       Show or hide the video or audio thumbnail (Featured Image/post
#// thumbnail). Default true.
#// @type bool    $artists      Whether to show or hide artist name in the playlist. Default true.
#// }
#// 
#// @return string Playlist output. Empty string if the passed type is unsupported.
#//
def wp_playlist_shortcode(attr_=None, *_args_):
    
    
    global content_width_
    php_check_if_defined("content_width_")
    post_ = get_post()
    instance_ = 0
    instance_ += 1
    if (not php_empty(lambda : attr_["ids"])):
        #// 'ids' is explicitly ordered, unless you specify otherwise.
        if php_empty(lambda : attr_["orderby"]):
            attr_["orderby"] = "post__in"
        # end if
        attr_["include"] = attr_["ids"]
    # end if
    #// 
    #// Filters the playlist output.
    #// 
    #// Passing a non-empty value to the filter will short-circuit generation
    #// of the default playlist output, returning the passed value instead.
    #// 
    #// @since 3.9.0
    #// @since 4.2.0 The `$instance` parameter was added.
    #// 
    #// @param string $output   Playlist output. Default empty.
    #// @param array  $attr     An array of shortcode attributes.
    #// @param int    $instance Unique numeric ID of this playlist shortcode instance.
    #//
    output_ = apply_filters("post_playlist", "", attr_, instance_)
    if (not php_empty(lambda : output_)):
        return output_
    # end if
    atts_ = shortcode_atts(Array({"type": "audio", "order": "ASC", "orderby": "menu_order ID", "id": post_.ID if post_ else 0, "include": "", "exclude": "", "style": "light", "tracklist": True, "tracknumbers": True, "images": True, "artists": True}), attr_, "playlist")
    id_ = php_intval(atts_["id"])
    if "audio" != atts_["type"]:
        atts_["type"] = "video"
    # end if
    args_ = Array({"post_status": "inherit", "post_type": "attachment", "post_mime_type": atts_["type"], "order": atts_["order"], "orderby": atts_["orderby"]})
    if (not php_empty(lambda : atts_["include"])):
        args_["include"] = atts_["include"]
        _attachments_ = get_posts(args_)
        attachments_ = Array()
        for key_,val_ in _attachments_.items():
            attachments_[val_.ID] = _attachments_[key_]
        # end for
    elif (not php_empty(lambda : atts_["exclude"])):
        args_["post_parent"] = id_
        args_["exclude"] = atts_["exclude"]
        attachments_ = get_children(args_)
    else:
        args_["post_parent"] = id_
        attachments_ = get_children(args_)
    # end if
    if php_empty(lambda : attachments_):
        return ""
    # end if
    if is_feed():
        output_ = "\n"
        for att_id_,attachment_ in attachments_.items():
            output_ += wp_get_attachment_link(att_id_) + "\n"
        # end for
        return output_
    # end if
    outer_ = 22
    #// Default padding and border of wrapper.
    default_width_ = 640
    default_height_ = 360
    theme_width_ = default_width_ if php_empty(lambda : content_width_) else content_width_ - outer_
    theme_height_ = default_height_ if php_empty(lambda : content_width_) else round(default_height_ * theme_width_ / default_width_)
    data_ = Array({"type": atts_["type"], "tracklist": wp_validate_boolean(atts_["tracklist"]), "tracknumbers": wp_validate_boolean(atts_["tracknumbers"]), "images": wp_validate_boolean(atts_["images"]), "artists": wp_validate_boolean(atts_["artists"])})
    tracks_ = Array()
    for attachment_ in attachments_:
        url_ = wp_get_attachment_url(attachment_.ID)
        ftype_ = wp_check_filetype(url_, wp_get_mime_types())
        track_ = Array({"src": url_, "type": ftype_["type"], "title": attachment_.post_title, "caption": attachment_.post_excerpt, "description": attachment_.post_content})
        track_["meta"] = Array()
        meta_ = wp_get_attachment_metadata(attachment_.ID)
        if (not php_empty(lambda : meta_)):
            for key_,label_ in wp_get_attachment_id3_keys(attachment_).items():
                if (not php_empty(lambda : meta_[key_])):
                    track_["meta"][key_] = meta_[key_]
                # end if
            # end for
            if "video" == atts_["type"]:
                if (not php_empty(lambda : meta_["width"])) and (not php_empty(lambda : meta_["height"])):
                    width_ = meta_["width"]
                    height_ = meta_["height"]
                    theme_height_ = round(height_ * theme_width_ / width_)
                else:
                    width_ = default_width_
                    height_ = default_height_
                # end if
                track_["dimensions"] = Array({"original": php_compact("width_", "height_"), "resized": Array({"width": theme_width_, "height": theme_height_})})
            # end if
        # end if
        if atts_["images"]:
            thumb_id_ = get_post_thumbnail_id(attachment_.ID)
            if (not php_empty(lambda : thumb_id_)):
                src_, width_, height_ = wp_get_attachment_image_src(thumb_id_, "full")
                track_["image"] = php_compact("src_", "width_", "height_")
                src_, width_, height_ = wp_get_attachment_image_src(thumb_id_, "thumbnail")
                track_["thumb"] = php_compact("src_", "width_", "height_")
            else:
                src_ = wp_mime_type_icon(attachment_.ID)
                width_ = 48
                height_ = 64
                track_["image"] = php_compact("src_", "width_", "height_")
                track_["thumb"] = php_compact("src_", "width_", "height_")
            # end if
        # end if
        tracks_[-1] = track_
    # end for
    data_["tracks"] = tracks_
    safe_type_ = esc_attr(atts_["type"])
    safe_style_ = esc_attr(atts_["style"])
    ob_start()
    if 1 == instance_:
        #// 
        #// Prints and enqueues playlist scripts, styles, and JavaScript templates.
        #// 
        #// @since 3.9.0
        #// 
        #// @param string $type  Type of playlist. Possible values are 'audio' or 'video'.
        #// @param string $style The 'theme' for the playlist. Core provides 'light' and 'dark'.
        #//
        do_action("wp_playlist_scripts", atts_["type"], atts_["style"])
    # end if
    php_print("<div class=\"wp-playlist wp-")
    php_print(safe_type_)
    php_print("-playlist wp-playlist-")
    php_print(safe_style_)
    php_print("\">\n    ")
    if "audio" == atts_["type"]:
        php_print(" <div class=\"wp-playlist-current-item\"></div>\n    ")
    # end if
    php_print(" <")
    php_print(safe_type_)
    php_print(" controls=\"controls\" preload=\"none\" width=\"\n               ")
    php_print(php_int(theme_width_))
    php_print(" \"\n    ")
    if "video" == safe_type_:
        php_print(" height=\"", php_int(theme_height_), "\"")
    # end if
    php_print(" ></")
    php_print(safe_type_)
    php_print(""">
    <div class=\"wp-playlist-next\"></div>
    <div class=\"wp-playlist-prev\"></div>
    <noscript>
    <ol>
    """)
    for att_id_,attachment_ in attachments_.items():
        php_printf("<li>%s</li>", wp_get_attachment_link(att_id_))
    # end for
    php_print(" </ol>\n </noscript>\n   <script type=\"application/json\" class=\"wp-playlist-script\">")
    php_print(wp_json_encode(data_))
    php_print("</script>\n</div>\n  ")
    return ob_get_clean()
# end def wp_playlist_shortcode
add_shortcode("playlist", "wp_playlist_shortcode")
#// 
#// Provides a No-JS Flash fallback as a last resort for audio / video.
#// 
#// @since 3.6.0
#// 
#// @param string $url The media element URL.
#// @return string Fallback HTML.
#//
def wp_mediaelement_fallback(url_=None, *_args_):
    
    
    #// 
    #// Filters the Mediaelement fallback output for no-JS.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $output Fallback output for no-JS.
    #// @param string $url    Media file URL.
    #//
    return apply_filters("wp_mediaelement_fallback", php_sprintf("<a href=\"%1$s\">%1$s</a>", esc_url(url_)), url_)
# end def wp_mediaelement_fallback
#// 
#// Returns a filtered list of supported audio formats.
#// 
#// @since 3.6.0
#// 
#// @return string[] Supported audio formats.
#//
def wp_get_audio_extensions(*_args_):
    
    
    #// 
    #// Filters the list of supported audio formats.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string[] $extensions An array of supported audio formats. Defaults are
    #// 'mp3', 'ogg', 'flac', 'm4a', 'wav'.
    #//
    return apply_filters("wp_audio_extensions", Array("mp3", "ogg", "flac", "m4a", "wav"))
# end def wp_get_audio_extensions
#// 
#// Returns useful keys to use to lookup data from an attachment's stored metadata.
#// 
#// @since 3.9.0
#// 
#// @param WP_Post $attachment The current attachment, provided for context.
#// @param string  $context    Optional. The context. Accepts 'edit', 'display'. Default 'display'.
#// @return string[] Key/value pairs of field keys to labels.
#//
def wp_get_attachment_id3_keys(attachment_=None, context_="display", *_args_):
    
    
    fields_ = Array({"artist": __("Artist"), "album": __("Album")})
    if "display" == context_:
        fields_["genre"] = __("Genre")
        fields_["year"] = __("Year")
        fields_["length_formatted"] = _x("Length", "video or audio")
    elif "js" == context_:
        fields_["bitrate"] = __("Bitrate")
        fields_["bitrate_mode"] = __("Bitrate Mode")
    # end if
    #// 
    #// Filters the editable list of keys to look up data from an attachment's metadata.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array   $fields     Key/value pairs of field keys to labels.
    #// @param WP_Post $attachment Attachment object.
    #// @param string  $context    The context. Accepts 'edit', 'display'. Default 'display'.
    #//
    return apply_filters("wp_get_attachment_id3_keys", fields_, attachment_, context_)
# end def wp_get_attachment_id3_keys
#// 
#// Builds the Audio shortcode output.
#// 
#// This implements the functionality of the Audio Shortcode for displaying
#// WordPress mp3s in a post.
#// 
#// @since 3.6.0
#// 
#// @staticvar int $instance
#// 
#// @param array  $attr {
#// Attributes of the audio shortcode.
#// 
#// @type string $src      URL to the source of the audio file. Default empty.
#// @type string $loop     The 'loop' attribute for the `<audio>` element. Default empty.
#// @type string $autoplay The 'autoplay' attribute for the `<audio>` element. Default empty.
#// @type string $preload  The 'preload' attribute for the `<audio>` element. Default 'none'.
#// @type string $class    The 'class' attribute for the `<audio>` element. Default 'wp-audio-shortcode'.
#// @type string $style    The 'style' attribute for the `<audio>` element. Default 'width: 100%;'.
#// }
#// @param string $content Shortcode content.
#// @return string|void HTML content to display audio.
#//
def wp_audio_shortcode(attr_=None, content_="", *_args_):
    
    
    post_id_ = get_the_ID() if get_post() else 0
    instance_ = 0
    instance_ += 1
    #// 
    #// Filters the default audio shortcode output.
    #// 
    #// If the filtered output isn't empty, it will be used instead of generating the default audio template.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $html     Empty variable to be replaced with shortcode markup.
    #// @param array  $attr     Attributes of the shortcode. @see wp_audio_shortcode()
    #// @param string $content  Shortcode content.
    #// @param int    $instance Unique numeric ID of this audio shortcode instance.
    #//
    override_ = apply_filters("wp_audio_shortcode_override", "", attr_, content_, instance_)
    if "" != override_:
        return override_
    # end if
    audio_ = None
    default_types_ = wp_get_audio_extensions()
    defaults_atts_ = Array({"src": "", "loop": "", "autoplay": "", "preload": "none", "class": "wp-audio-shortcode", "style": "width: 100%;"})
    for type_ in default_types_:
        defaults_atts_[type_] = ""
    # end for
    atts_ = shortcode_atts(defaults_atts_, attr_, "audio")
    primary_ = False
    if (not php_empty(lambda : atts_["src"])):
        type_ = wp_check_filetype(atts_["src"], wp_get_mime_types())
        if (not php_in_array(php_strtolower(type_["ext"]), default_types_, True)):
            return php_sprintf("<a class=\"wp-embedded-audio\" href=\"%s\">%s</a>", esc_url(atts_["src"]), esc_html(atts_["src"]))
        # end if
        primary_ = True
        array_unshift(default_types_, "src")
    else:
        for ext_ in default_types_:
            if (not php_empty(lambda : atts_[ext_])):
                type_ = wp_check_filetype(atts_[ext_], wp_get_mime_types())
                if php_strtolower(type_["ext"]) == ext_:
                    primary_ = True
                # end if
            # end if
        # end for
    # end if
    if (not primary_):
        audios_ = get_attached_media("audio", post_id_)
        if php_empty(lambda : audios_):
            return
        # end if
        audio_ = reset(audios_)
        atts_["src"] = wp_get_attachment_url(audio_.ID)
        if php_empty(lambda : atts_["src"]):
            return
        # end if
        array_unshift(default_types_, "src")
    # end if
    #// 
    #// Filters the media library used for the audio shortcode.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $library Media library used for the audio shortcode.
    #//
    library_ = apply_filters("wp_audio_shortcode_library", "mediaelement")
    if "mediaelement" == library_ and did_action("init"):
        wp_enqueue_style("wp-mediaelement")
        wp_enqueue_script("wp-mediaelement")
    # end if
    #// 
    #// Filters the class attribute for the audio shortcode output container.
    #// 
    #// @since 3.6.0
    #// @since 4.9.0 The `$atts` parameter was added.
    #// 
    #// @param string $class CSS class or list of space-separated classes.
    #// @param array  $atts  Array of audio shortcode attributes.
    #//
    atts_["class"] = apply_filters("wp_audio_shortcode_class", atts_["class"], atts_)
    html_atts_ = Array({"class": atts_["class"], "id": php_sprintf("audio-%d-%d", post_id_, instance_), "loop": wp_validate_boolean(atts_["loop"]), "autoplay": wp_validate_boolean(atts_["autoplay"]), "preload": atts_["preload"], "style": atts_["style"]})
    #// These ones should just be omitted altogether if they are blank.
    for a_ in Array("loop", "autoplay", "preload"):
        if php_empty(lambda : html_atts_[a_]):
            html_atts_[a_] = None
        # end if
    # end for
    attr_strings_ = Array()
    for k_,v_ in html_atts_.items():
        attr_strings_[-1] = k_ + "=\"" + esc_attr(v_) + "\""
    # end for
    html_ = ""
    if "mediaelement" == library_ and 1 == instance_:
        html_ += "<!--[if lt IE 9]><script>document.createElement('audio');</script><![endif]-->\n"
    # end if
    html_ += php_sprintf("<audio %s controls=\"controls\">", php_join(" ", attr_strings_))
    fileurl_ = ""
    source_ = "<source type=\"%s\" src=\"%s\" />"
    for fallback_ in default_types_:
        if (not php_empty(lambda : atts_[fallback_])):
            if php_empty(lambda : fileurl_):
                fileurl_ = atts_[fallback_]
            # end if
            type_ = wp_check_filetype(atts_[fallback_], wp_get_mime_types())
            url_ = add_query_arg("_", instance_, atts_[fallback_])
            html_ += php_sprintf(source_, type_["type"], esc_url(url_))
        # end if
    # end for
    if "mediaelement" == library_:
        html_ += wp_mediaelement_fallback(fileurl_)
    # end if
    html_ += "</audio>"
    #// 
    #// Filters the audio shortcode output.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $html    Audio shortcode HTML output.
    #// @param array  $atts    Array of audio shortcode attributes.
    #// @param string $audio   Audio file.
    #// @param int    $post_id Post ID.
    #// @param string $library Media library used for the audio shortcode.
    #//
    return apply_filters("wp_audio_shortcode", html_, atts_, audio_, post_id_, library_)
# end def wp_audio_shortcode
add_shortcode("audio", "wp_audio_shortcode")
#// 
#// Returns a filtered list of supported video formats.
#// 
#// @since 3.6.0
#// 
#// @return string[] List of supported video formats.
#//
def wp_get_video_extensions(*_args_):
    
    
    #// 
    #// Filters the list of supported video formats.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string[] $extensions An array of supported video formats. Defaults are
    #// 'mp4', 'm4v', 'webm', 'ogv', 'flv'.
    #//
    return apply_filters("wp_video_extensions", Array("mp4", "m4v", "webm", "ogv", "flv"))
# end def wp_get_video_extensions
#// 
#// Builds the Video shortcode output.
#// 
#// This implements the functionality of the Video Shortcode for displaying
#// WordPress mp4s in a post.
#// 
#// @since 3.6.0
#// 
#// @global int $content_width
#// @staticvar int $instance
#// 
#// @param array  $attr {
#// Attributes of the shortcode.
#// 
#// @type string $src      URL to the source of the video file. Default empty.
#// @type int    $height   Height of the video embed in pixels. Default 360.
#// @type int    $width    Width of the video embed in pixels. Default $content_width or 640.
#// @type string $poster   The 'poster' attribute for the `<video>` element. Default empty.
#// @type string $loop     The 'loop' attribute for the `<video>` element. Default empty.
#// @type string $autoplay The 'autoplay' attribute for the `<video>` element. Default empty.
#// @type string $preload  The 'preload' attribute for the `<video>` element.
#// Default 'metadata'.
#// @type string $class    The 'class' attribute for the `<video>` element.
#// Default 'wp-video-shortcode'.
#// }
#// @param string $content Shortcode content.
#// @return string|void HTML content to display video.
#//
def wp_video_shortcode(attr_=None, content_="", *_args_):
    
    
    global content_width_
    php_check_if_defined("content_width_")
    post_id_ = get_the_ID() if get_post() else 0
    instance_ = 0
    instance_ += 1
    #// 
    #// Filters the default video shortcode output.
    #// 
    #// If the filtered output isn't empty, it will be used instead of generating
    #// the default video template.
    #// 
    #// @since 3.6.0
    #// 
    #// @see wp_video_shortcode()
    #// 
    #// @param string $html     Empty variable to be replaced with shortcode markup.
    #// @param array  $attr     Attributes of the shortcode. @see wp_video_shortcode()
    #// @param string $content  Video shortcode content.
    #// @param int    $instance Unique numeric ID of this video shortcode instance.
    #//
    override_ = apply_filters("wp_video_shortcode_override", "", attr_, content_, instance_)
    if "" != override_:
        return override_
    # end if
    video_ = None
    default_types_ = wp_get_video_extensions()
    defaults_atts_ = Array({"src": "", "poster": "", "loop": "", "autoplay": "", "preload": "metadata", "width": 640, "height": 360, "class": "wp-video-shortcode"})
    for type_ in default_types_:
        defaults_atts_[type_] = ""
    # end for
    atts_ = shortcode_atts(defaults_atts_, attr_, "video")
    if is_admin():
        #// Shrink the video so it isn't huge in the admin.
        if atts_["width"] > defaults_atts_["width"]:
            atts_["height"] = round(atts_["height"] * defaults_atts_["width"] / atts_["width"])
            atts_["width"] = defaults_atts_["width"]
        # end if
    else:
        #// If the video is bigger than the theme.
        if (not php_empty(lambda : content_width_)) and atts_["width"] > content_width_:
            atts_["height"] = round(atts_["height"] * content_width_ / atts_["width"])
            atts_["width"] = content_width_
        # end if
    # end if
    is_vimeo_ = False
    is_youtube_ = False
    yt_pattern_ = "#^https?://(?:www\\.)?(?:youtube\\.com/watch|youtu\\.be/)#"
    vimeo_pattern_ = "#^https?://(.+\\.)?vimeo\\.com/.*#"
    primary_ = False
    if (not php_empty(lambda : atts_["src"])):
        is_vimeo_ = php_preg_match(vimeo_pattern_, atts_["src"])
        is_youtube_ = php_preg_match(yt_pattern_, atts_["src"])
        if (not is_youtube_) and (not is_vimeo_):
            type_ = wp_check_filetype(atts_["src"], wp_get_mime_types())
            if (not php_in_array(php_strtolower(type_["ext"]), default_types_, True)):
                return php_sprintf("<a class=\"wp-embedded-video\" href=\"%s\">%s</a>", esc_url(atts_["src"]), esc_html(atts_["src"]))
            # end if
        # end if
        if is_vimeo_:
            wp_enqueue_script("mediaelement-vimeo")
        # end if
        primary_ = True
        array_unshift(default_types_, "src")
    else:
        for ext_ in default_types_:
            if (not php_empty(lambda : atts_[ext_])):
                type_ = wp_check_filetype(atts_[ext_], wp_get_mime_types())
                if php_strtolower(type_["ext"]) == ext_:
                    primary_ = True
                # end if
            # end if
        # end for
    # end if
    if (not primary_):
        videos_ = get_attached_media("video", post_id_)
        if php_empty(lambda : videos_):
            return
        # end if
        video_ = reset(videos_)
        atts_["src"] = wp_get_attachment_url(video_.ID)
        if php_empty(lambda : atts_["src"]):
            return
        # end if
        array_unshift(default_types_, "src")
    # end if
    #// 
    #// Filters the media library used for the video shortcode.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $library Media library used for the video shortcode.
    #//
    library_ = apply_filters("wp_video_shortcode_library", "mediaelement")
    if "mediaelement" == library_ and did_action("init"):
        wp_enqueue_style("wp-mediaelement")
        wp_enqueue_script("wp-mediaelement")
        wp_enqueue_script("mediaelement-vimeo")
    # end if
    #// MediaElement.js has issues with some URL formats for Vimeo and YouTube,
    #// so update the URL to prevent the ME.js player from breaking.
    if "mediaelement" == library_:
        if is_youtube_:
            #// Remove `feature` query arg and force SSL - see #40866.
            atts_["src"] = remove_query_arg("feature", atts_["src"])
            atts_["src"] = set_url_scheme(atts_["src"], "https")
        elif is_vimeo_:
            #// Remove all query arguments and force SSL - see #40866.
            parsed_vimeo_url_ = wp_parse_url(atts_["src"])
            vimeo_src_ = "https://" + parsed_vimeo_url_["host"] + parsed_vimeo_url_["path"]
            #// Add loop param for mejs bug - see #40977, not needed after #39686.
            loop_ = "1" if atts_["loop"] else "0"
            atts_["src"] = add_query_arg("loop", loop_, vimeo_src_)
        # end if
    # end if
    #// 
    #// Filters the class attribute for the video shortcode output container.
    #// 
    #// @since 3.6.0
    #// @since 4.9.0 The `$atts` parameter was added.
    #// 
    #// @param string $class CSS class or list of space-separated classes.
    #// @param array  $atts  Array of video shortcode attributes.
    #//
    atts_["class"] = apply_filters("wp_video_shortcode_class", atts_["class"], atts_)
    html_atts_ = Array({"class": atts_["class"], "id": php_sprintf("video-%d-%d", post_id_, instance_), "width": absint(atts_["width"]), "height": absint(atts_["height"]), "poster": esc_url(atts_["poster"]), "loop": wp_validate_boolean(atts_["loop"]), "autoplay": wp_validate_boolean(atts_["autoplay"]), "preload": atts_["preload"]})
    #// These ones should just be omitted altogether if they are blank.
    for a_ in Array("poster", "loop", "autoplay", "preload"):
        if php_empty(lambda : html_atts_[a_]):
            html_atts_[a_] = None
        # end if
    # end for
    attr_strings_ = Array()
    for k_,v_ in html_atts_.items():
        attr_strings_[-1] = k_ + "=\"" + esc_attr(v_) + "\""
    # end for
    html_ = ""
    if "mediaelement" == library_ and 1 == instance_:
        html_ += "<!--[if lt IE 9]><script>document.createElement('video');</script><![endif]-->\n"
    # end if
    html_ += php_sprintf("<video %s controls=\"controls\">", php_join(" ", attr_strings_))
    fileurl_ = ""
    source_ = "<source type=\"%s\" src=\"%s\" />"
    for fallback_ in default_types_:
        if (not php_empty(lambda : atts_[fallback_])):
            if php_empty(lambda : fileurl_):
                fileurl_ = atts_[fallback_]
            # end if
            if "src" == fallback_ and is_youtube_:
                type_ = Array({"type": "video/youtube"})
            elif "src" == fallback_ and is_vimeo_:
                type_ = Array({"type": "video/vimeo"})
            else:
                type_ = wp_check_filetype(atts_[fallback_], wp_get_mime_types())
            # end if
            url_ = add_query_arg("_", instance_, atts_[fallback_])
            html_ += php_sprintf(source_, type_["type"], esc_url(url_))
        # end if
    # end for
    if (not php_empty(lambda : content_)):
        if False != php_strpos(content_, "\n"):
            content_ = php_str_replace(Array("\r\n", "\n", "    "), "", content_)
        # end if
        html_ += php_trim(content_)
    # end if
    if "mediaelement" == library_:
        html_ += wp_mediaelement_fallback(fileurl_)
    # end if
    html_ += "</video>"
    width_rule_ = ""
    if (not php_empty(lambda : atts_["width"])):
        width_rule_ = php_sprintf("width: %dpx;", atts_["width"])
    # end if
    output_ = php_sprintf("<div style=\"%s\" class=\"wp-video\">%s</div>", width_rule_, html_)
    #// 
    #// Filters the output of the video shortcode.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $output  Video shortcode HTML output.
    #// @param array  $atts    Array of video shortcode attributes.
    #// @param string $video   Video file.
    #// @param int    $post_id Post ID.
    #// @param string $library Media library used for the video shortcode.
    #//
    return apply_filters("wp_video_shortcode", output_, atts_, video_, post_id_, library_)
# end def wp_video_shortcode
add_shortcode("video", "wp_video_shortcode")
#// 
#// Displays previous image link that has the same post parent.
#// 
#// @since 2.5.0
#// 
#// @see adjacent_image_link()
#// 
#// @param string|array $size Optional. Image size. Accepts any valid image size, an array of width and
#// height values in pixels (in that order), 0, or 'none'. 0 or 'none' will
#// default to 'post_title' or `$text`. Default 'thumbnail'.
#// @param string       $text Optional. Link text. Default false.
#//
def previous_image_link(size_="thumbnail", text_=None, *_args_):
    if text_ is None:
        text_ = False
    # end if
    
    adjacent_image_link(True, size_, text_)
# end def previous_image_link
#// 
#// Displays next image link that has the same post parent.
#// 
#// @since 2.5.0
#// 
#// @see adjacent_image_link()
#// 
#// @param string|array $size Optional. Image size. Accepts any valid image size, an array of width and
#// height values in pixels (in that order), 0, or 'none'. 0 or 'none' will
#// default to 'post_title' or `$text`. Default 'thumbnail'.
#// @param string       $text Optional. Link text. Default false.
#//
def next_image_link(size_="thumbnail", text_=None, *_args_):
    if text_ is None:
        text_ = False
    # end if
    
    adjacent_image_link(False, size_, text_)
# end def next_image_link
#// 
#// Displays next or previous image link that has the same post parent.
#// 
#// Retrieves the current attachment object from the $post global.
#// 
#// @since 2.5.0
#// 
#// @param bool         $prev Optional. Whether to display the next (false) or previous (true) link. Default true.
#// @param string|array $size Optional. Image size. Accepts any valid image size, or an array of width and height
#// values in pixels (in that order). Default 'thumbnail'.
#// @param bool         $text Optional. Link text. Default false.
#//
def adjacent_image_link(prev_=None, size_="thumbnail", text_=None, *_args_):
    if prev_ is None:
        prev_ = True
    # end if
    if text_ is None:
        text_ = False
    # end if
    
    post_ = get_post()
    attachments_ = php_array_values(get_children(Array({"post_parent": post_.post_parent, "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": "ASC", "orderby": "menu_order ID"})))
    for k_,attachment_ in attachments_.items():
        if php_intval(attachment_.ID) == php_intval(post_.ID):
            break
        # end if
    # end for
    output_ = ""
    attachment_id_ = 0
    if attachments_:
        k_ = k_ - 1 if prev_ else k_ + 1
        if (php_isset(lambda : attachments_[k_])):
            attachment_id_ = attachments_[k_].ID
            output_ = wp_get_attachment_link(attachment_id_, size_, True, False, text_)
        # end if
    # end if
    adjacent_ = "previous" if prev_ else "next"
    #// 
    #// Filters the adjacent image link.
    #// 
    #// The dynamic portion of the hook name, `$adjacent`, refers to the type of adjacency,
    #// either 'next', or 'previous'.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $output        Adjacent image HTML markup.
    #// @param int    $attachment_id Attachment ID
    #// @param string $size          Image size.
    #// @param string $text          Link text.
    #//
    php_print(apply_filters(str(adjacent_) + str("_image_link"), output_, attachment_id_, size_, text_))
# end def adjacent_image_link
#// 
#// Retrieves taxonomies attached to given the attachment.
#// 
#// @since 2.5.0
#// @since 4.7.0 Introduced the `$output` parameter.
#// 
#// @param int|array|object $attachment Attachment ID, data array, or data object.
#// @param string           $output     Output type. 'names' to return an array of taxonomy names,
#// or 'objects' to return an array of taxonomy objects.
#// Default is 'names'.
#// @return string[]|WP_Taxonomy[] List of taxonomies or taxonomy names. Empty array on failure.
#//
def get_attachment_taxonomies(attachment_=None, output_="names", *_args_):
    
    
    if php_is_int(attachment_):
        attachment_ = get_post(attachment_)
    elif php_is_array(attachment_):
        attachment_ = attachment_
    # end if
    if (not php_is_object(attachment_)):
        return Array()
    # end if
    file_ = get_attached_file(attachment_.ID)
    filename_ = wp_basename(file_)
    objects_ = Array("attachment")
    if False != php_strpos(filename_, "."):
        objects_[-1] = "attachment:" + php_substr(filename_, php_strrpos(filename_, ".") + 1)
    # end if
    if (not php_empty(lambda : attachment_.post_mime_type)):
        objects_[-1] = "attachment:" + attachment_.post_mime_type
        if False != php_strpos(attachment_.post_mime_type, "/"):
            for token_ in php_explode("/", attachment_.post_mime_type):
                if (not php_empty(lambda : token_)):
                    objects_[-1] = str("attachment:") + str(token_)
                # end if
            # end for
        # end if
    # end if
    taxonomies_ = Array()
    for object_ in objects_:
        taxes_ = get_object_taxonomies(object_, output_)
        if taxes_:
            taxonomies_ = php_array_merge(taxonomies_, taxes_)
        # end if
    # end for
    if "names" == output_:
        taxonomies_ = array_unique(taxonomies_)
    # end if
    return taxonomies_
# end def get_attachment_taxonomies
#// 
#// Retrieves all of the taxonomies that are registered for attachments.
#// 
#// Handles mime-type-specific taxonomies such as attachment:image and attachment:video.
#// 
#// @since 3.5.0
#// @see get_taxonomies()
#// 
#// @param string $output Optional. The type of taxonomy output to return. Accepts 'names' or 'objects'.
#// Default 'names'.
#// @return string[]|WP_Taxonomy[] Array of names or objects of registered taxonomies for attachments.
#//
def get_taxonomies_for_attachments(output_="names", *_args_):
    
    
    taxonomies_ = Array()
    for taxonomy_ in get_taxonomies(Array(), "objects"):
        for object_type_ in taxonomy_.object_type:
            if "attachment" == object_type_ or 0 == php_strpos(object_type_, "attachment:"):
                if "names" == output_:
                    taxonomies_[-1] = taxonomy_.name
                else:
                    taxonomies_[taxonomy_.name] = taxonomy_
                # end if
                break
            # end if
        # end for
    # end for
    return taxonomies_
# end def get_taxonomies_for_attachments
#// 
#// Create new GD image resource with transparency support
#// 
#// @todo Deprecate if possible.
#// 
#// @since 2.9.0
#// 
#// @param int $width  Image width in pixels.
#// @param int $height Image height in pixels..
#// @return resource The GD image resource.
#//
def wp_imagecreatetruecolor(width_=None, height_=None, *_args_):
    
    
    img_ = imagecreatetruecolor(width_, height_)
    if php_is_resource(img_) and php_function_exists("imagealphablending") and php_function_exists("imagesavealpha"):
        imagealphablending(img_, False)
        imagesavealpha(img_, True)
    # end if
    return img_
# end def wp_imagecreatetruecolor
#// 
#// Based on a supplied width/height example, return the biggest possible dimensions based on the max width/height.
#// 
#// @since 2.9.0
#// 
#// @see wp_constrain_dimensions()
#// 
#// @param int $example_width  The width of an example embed.
#// @param int $example_height The height of an example embed.
#// @param int $max_width      The maximum allowed width.
#// @param int $max_height     The maximum allowed height.
#// @return int[] {
#// An array of maximum width and height values.
#// 
#// @type int $0 The maximum width in pixels.
#// @type int $1 The maximum height in pixels.
#// }
#//
def wp_expand_dimensions(example_width_=None, example_height_=None, max_width_=None, max_height_=None, *_args_):
    
    
    example_width_ = php_int(example_width_)
    example_height_ = php_int(example_height_)
    max_width_ = php_int(max_width_)
    max_height_ = php_int(max_height_)
    return wp_constrain_dimensions(example_width_ * 1000000, example_height_ * 1000000, max_width_, max_height_)
# end def wp_expand_dimensions
#// 
#// Determines the maximum upload size allowed in php.ini.
#// 
#// @since 2.5.0
#// 
#// @return int Allowed upload size.
#//
def wp_max_upload_size(*_args_):
    
    
    u_bytes_ = wp_convert_hr_to_bytes(php_ini_get("upload_max_filesize"))
    p_bytes_ = wp_convert_hr_to_bytes(php_ini_get("post_max_size"))
    #// 
    #// Filters the maximum upload size allowed in php.ini.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int $size    Max upload size limit in bytes.
    #// @param int $u_bytes Maximum upload filesize in bytes.
    #// @param int $p_bytes Maximum size of POST data in bytes.
    #//
    return apply_filters("upload_size_limit", php_min(u_bytes_, p_bytes_), u_bytes_, p_bytes_)
# end def wp_max_upload_size
#// 
#// Returns a WP_Image_Editor instance and loads file into it.
#// 
#// @since 3.5.0
#// 
#// @param string $path Path to the file to load.
#// @param array  $args Optional. Additional arguments for retrieving the image editor.
#// Default empty array.
#// @return WP_Image_Editor|WP_Error The WP_Image_Editor object if successful, an WP_Error
#// object otherwise.
#//
def wp_get_image_editor(path_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    args_["path"] = path_
    if (not (php_isset(lambda : args_["mime_type"]))):
        file_info_ = wp_check_filetype(args_["path"])
        #// If $file_info['type'] is false, then we let the editor attempt to
        #// figure out the file type, rather than forcing a failure based on extension.
        if (php_isset(lambda : file_info_)) and file_info_["type"]:
            args_["mime_type"] = file_info_["type"]
        # end if
    # end if
    implementation_ = _wp_image_editor_choose(args_)
    if implementation_:
        editor_ = php_new_class(implementation_, lambda : {**locals(), **globals()}[implementation_](path_))
        loaded_ = editor_.load()
        if is_wp_error(loaded_):
            return loaded_
        # end if
        return editor_
    # end if
    return php_new_class("WP_Error", lambda : WP_Error("image_no_editor", __("No editor could be selected.")))
# end def wp_get_image_editor
#// 
#// Tests whether there is an editor that supports a given mime type or methods.
#// 
#// @since 3.5.0
#// 
#// @param string|array $args Optional. Array of arguments to retrieve the image editor supports.
#// Default empty array.
#// @return bool True if an eligible editor is found; false otherwise.
#//
def wp_image_editor_supports(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    return php_bool(_wp_image_editor_choose(args_))
# end def wp_image_editor_supports
#// 
#// Tests which editors are capable of supporting the request.
#// 
#// @ignore
#// @since 3.5.0
#// 
#// @param array $args Optional. Array of arguments for choosing a capable editor. Default empty array.
#// @return string|false Class name for the first editor that claims to support the request. False if no
#// editor claims to support the request.
#//
def _wp_image_editor_choose(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    php_include_file(ABSPATH + WPINC + "/class-wp-image-editor.php", once=True)
    php_include_file(ABSPATH + WPINC + "/class-wp-image-editor-gd.php", once=True)
    php_include_file(ABSPATH + WPINC + "/class-wp-image-editor-imagick.php", once=True)
    #// 
    #// Filters the list of image editing library classes.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string[] $image_editors Array of available image editor class names. Defaults are
    #// 'WP_Image_Editor_Imagick', 'WP_Image_Editor_GD'.
    #//
    implementations_ = apply_filters("wp_image_editors", Array("WP_Image_Editor_Imagick", "WP_Image_Editor_GD"))
    for implementation_ in implementations_:
        if (not php_call_user_func(Array(implementation_, "test"), args_)):
            continue
        # end if
        if (php_isset(lambda : args_["mime_type"])) and (not php_call_user_func(Array(implementation_, "supports_mime_type"), args_["mime_type"])):
            continue
        # end if
        if (php_isset(lambda : args_["methods"])) and php_array_diff(args_["methods"], get_class_methods(implementation_)):
            continue
        # end if
        return implementation_
    # end for
    return False
# end def _wp_image_editor_choose
#// 
#// Prints default Plupload arguments.
#// 
#// @since 3.4.0
#//
def wp_plupload_default_settings(*_args_):
    
    
    wp_scripts_ = wp_scripts()
    data_ = wp_scripts_.get_data("wp-plupload", "data")
    if data_ and False != php_strpos(data_, "_wpPluploadSettings"):
        return
    # end if
    max_upload_size_ = wp_max_upload_size()
    allowed_extensions_ = php_array_keys(get_allowed_mime_types())
    extensions_ = Array()
    for extension_ in allowed_extensions_:
        extensions_ = php_array_merge(extensions_, php_explode("|", extension_))
    # end for
    #// 
    #// Since 4.9 the `runtimes` setting is hardcoded in our version of Plupload to `html5,html4`,
    #// and the `flash_swf_url` and `silverlight_xap_url` are not used.
    #//
    defaults_ = Array({"file_data_name": "async-upload", "url": admin_url("async-upload.php", "relative"), "filters": Array({"max_file_size": max_upload_size_ + "b", "mime_types": Array(Array({"extensions": php_implode(",", extensions_)}))})})
    #// 
    #// Currently only iOS Safari supports multiple files uploading,
    #// but iOS 7.x has a bug that prevents uploading of videos when enabled.
    #// See #29602.
    #//
    if wp_is_mobile() and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "OS 7_") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "like Mac OS X") != False:
        defaults_["multi_selection"] = False
    # end if
    #// 
    #// Filters the Plupload default settings.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $defaults Default Plupload settings array.
    #//
    defaults_ = apply_filters("plupload_default_settings", defaults_)
    params_ = Array({"action": "upload-attachment"})
    #// 
    #// Filters the Plupload default parameters.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $params Default Plupload parameters array.
    #//
    params_ = apply_filters("plupload_default_params", params_)
    params_["_wpnonce"] = wp_create_nonce("media-form")
    defaults_["multipart_params"] = params_
    settings_ = Array({"defaults": defaults_, "browser": Array({"mobile": wp_is_mobile(), "supported": _device_can_upload()})}, {"limitExceeded": is_multisite() and (not is_upload_space_available())})
    script_ = "var _wpPluploadSettings = " + wp_json_encode(settings_) + ";"
    if data_:
        script_ = str(data_) + str("\n") + str(script_)
    # end if
    wp_scripts_.add_data("wp-plupload", "data", script_)
# end def wp_plupload_default_settings
#// 
#// Prepares an attachment post object for JS, where it is expected
#// to be JSON-encoded and fit into an Attachment model.
#// 
#// @since 3.5.0
#// 
#// @param int|WP_Post $attachment Attachment ID or object.
#// @return array|void Array of attachment details.
#//
def wp_prepare_attachment_for_js(attachment_=None, *_args_):
    
    
    attachment_ = get_post(attachment_)
    if (not attachment_):
        return
    # end if
    if "attachment" != attachment_.post_type:
        return
    # end if
    meta_ = wp_get_attachment_metadata(attachment_.ID)
    if False != php_strpos(attachment_.post_mime_type, "/"):
        type_, subtype_ = php_explode("/", attachment_.post_mime_type)
    else:
        type_, subtype_ = Array(attachment_.post_mime_type, "")
    # end if
    attachment_url_ = wp_get_attachment_url(attachment_.ID)
    base_url_ = php_str_replace(wp_basename(attachment_url_), "", attachment_url_)
    response_ = Array({"id": attachment_.ID, "title": attachment_.post_title, "filename": wp_basename(get_attached_file(attachment_.ID)), "url": attachment_url_, "link": get_attachment_link(attachment_.ID), "alt": get_post_meta(attachment_.ID, "_wp_attachment_image_alt", True), "author": attachment_.post_author, "description": attachment_.post_content, "caption": attachment_.post_excerpt, "name": attachment_.post_name, "status": attachment_.post_status, "uploadedTo": attachment_.post_parent, "date": strtotime(attachment_.post_date_gmt) * 1000, "modified": strtotime(attachment_.post_modified_gmt) * 1000, "menuOrder": attachment_.menu_order, "mime": attachment_.post_mime_type, "type": type_, "subtype": subtype_, "icon": wp_mime_type_icon(attachment_.ID), "dateFormatted": mysql2date(__("F j, Y"), attachment_.post_date), "nonces": Array({"update": False, "delete": False, "edit": False})}, {"editLink": False, "meta": False})
    author_ = php_new_class("WP_User", lambda : WP_User(attachment_.post_author))
    if author_.exists():
        response_["authorName"] = html_entity_decode(author_.display_name, ENT_QUOTES, get_bloginfo("charset"))
    else:
        response_["authorName"] = __("(no author)")
    # end if
    if attachment_.post_parent:
        post_parent_ = get_post(attachment_.post_parent)
    else:
        post_parent_ = False
    # end if
    if post_parent_:
        parent_type_ = get_post_type_object(post_parent_.post_type)
        if parent_type_ and parent_type_.show_ui and current_user_can("edit_post", attachment_.post_parent):
            response_["uploadedToLink"] = get_edit_post_link(attachment_.post_parent, "raw")
        # end if
        if parent_type_ and current_user_can("read_post", attachment_.post_parent):
            response_["uploadedToTitle"] = post_parent_.post_title if post_parent_.post_title else __("(no title)")
        # end if
    # end if
    attached_file_ = get_attached_file(attachment_.ID)
    if (php_isset(lambda : meta_["filesize"])):
        bytes_ = meta_["filesize"]
    elif php_file_exists(attached_file_):
        bytes_ = filesize(attached_file_)
    else:
        bytes_ = ""
    # end if
    if bytes_:
        response_["filesizeInBytes"] = bytes_
        response_["filesizeHumanReadable"] = size_format(bytes_)
    # end if
    context_ = get_post_meta(attachment_.ID, "_wp_attachment_context", True)
    response_["context"] = context_ if context_ else ""
    if current_user_can("edit_post", attachment_.ID):
        response_["nonces"]["update"] = wp_create_nonce("update-post_" + attachment_.ID)
        response_["nonces"]["edit"] = wp_create_nonce("image_editor-" + attachment_.ID)
        response_["editLink"] = get_edit_post_link(attachment_.ID, "raw")
    # end if
    if current_user_can("delete_post", attachment_.ID):
        response_["nonces"]["delete"] = wp_create_nonce("delete-post_" + attachment_.ID)
    # end if
    if meta_ and "image" == type_ or (not php_empty(lambda : meta_["sizes"])):
        sizes_ = Array()
        #// This filter is documented in wp-admin/includes/media.php
        possible_sizes_ = apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")}))
        possible_sizes_["full"] = None
        #// 
        #// Loop through all potential sizes that may be chosen. Try to do this with some efficiency.
        #// First: run the image_downsize filter. If it returns something, we can use its data.
        #// If the filter does not return something, then image_downsize() is just an expensive way
        #// to check the image metadata, which we do second.
        #//
        for size_,label_ in possible_sizes_.items():
            #// This filter is documented in wp-includes/media.php
            downsize_ = apply_filters("image_downsize", False, attachment_.ID, size_)
            if downsize_:
                if php_empty(lambda : downsize_[3]):
                    continue
                # end if
                sizes_[size_] = Array({"height": downsize_[2], "width": downsize_[1], "url": downsize_[0], "orientation": "portrait" if downsize_[2] > downsize_[1] else "landscape"})
            elif (php_isset(lambda : meta_["sizes"][size_])):
                #// Nothing from the filter, so consult image metadata if we have it.
                size_meta_ = meta_["sizes"][size_]
                #// We have the actual image size, but might need to further constrain it if content_width is narrower.
                #// Thumbnail, medium, and full sizes are also checked against the site's height/width options.
                width_, height_ = image_constrain_size_for_editor(size_meta_["width"], size_meta_["height"], size_, "edit")
                sizes_[size_] = Array({"height": height_, "width": width_, "url": base_url_ + size_meta_["file"], "orientation": "portrait" if height_ > width_ else "landscape"})
            # end if
        # end for
        if "image" == type_:
            if (not php_empty(lambda : meta_["original_image"])):
                response_["originalImageURL"] = wp_get_original_image_url(attachment_.ID)
                response_["originalImageName"] = wp_basename(wp_get_original_image_path(attachment_.ID))
            # end if
            sizes_["full"] = Array({"url": attachment_url_})
            if (php_isset(lambda : meta_["height"]) and php_isset(lambda : meta_["width"])):
                sizes_["full"]["height"] = meta_["height"]
                sizes_["full"]["width"] = meta_["width"]
                sizes_["full"]["orientation"] = "portrait" if meta_["height"] > meta_["width"] else "landscape"
            # end if
            response_ = php_array_merge(response_, sizes_["full"])
        elif meta_["sizes"]["full"]["file"]:
            sizes_["full"] = Array({"url": base_url_ + meta_["sizes"]["full"]["file"], "height": meta_["sizes"]["full"]["height"], "width": meta_["sizes"]["full"]["width"], "orientation": "portrait" if meta_["sizes"]["full"]["height"] > meta_["sizes"]["full"]["width"] else "landscape"})
        # end if
        response_ = php_array_merge(response_, Array({"sizes": sizes_}))
    # end if
    if meta_ and "video" == type_:
        if (php_isset(lambda : meta_["width"])):
            response_["width"] = php_int(meta_["width"])
        # end if
        if (php_isset(lambda : meta_["height"])):
            response_["height"] = php_int(meta_["height"])
        # end if
    # end if
    if meta_ and "audio" == type_ or "video" == type_:
        if (php_isset(lambda : meta_["length_formatted"])):
            response_["fileLength"] = meta_["length_formatted"]
            response_["fileLengthHumanReadable"] = human_readable_duration(meta_["length_formatted"])
        # end if
        response_["meta"] = Array()
        for key_,label_ in wp_get_attachment_id3_keys(attachment_, "js").items():
            response_["meta"][key_] = False
            if (not php_empty(lambda : meta_[key_])):
                response_["meta"][key_] = meta_[key_]
            # end if
        # end for
        id_ = get_post_thumbnail_id(attachment_.ID)
        if (not php_empty(lambda : id_)):
            src_, width_, height_ = wp_get_attachment_image_src(id_, "full")
            response_["image"] = php_compact("src_", "width_", "height_")
            src_, width_, height_ = wp_get_attachment_image_src(id_, "thumbnail")
            response_["thumb"] = php_compact("src_", "width_", "height_")
        else:
            src_ = wp_mime_type_icon(attachment_.ID)
            width_ = 48
            height_ = 64
            response_["image"] = php_compact("src_", "width_", "height_")
            response_["thumb"] = php_compact("src_", "width_", "height_")
        # end if
    # end if
    if php_function_exists("get_compat_media_markup"):
        response_["compat"] = get_compat_media_markup(attachment_.ID, Array({"in_modal": True}))
    # end if
    #// 
    #// Filters the attachment data prepared for JavaScript.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array       $response   Array of prepared attachment data.
    #// @param WP_Post     $attachment Attachment object.
    #// @param array|false $meta       Array of attachment meta data, or false if there is none.
    #//
    return apply_filters("wp_prepare_attachment_for_js", response_, attachment_, meta_)
# end def wp_prepare_attachment_for_js
#// 
#// Enqueues all scripts, styles, settings, and templates necessary to use
#// all media JS APIs.
#// 
#// @since 3.5.0
#// 
#// @global int       $content_width
#// @global wpdb      $wpdb          WordPress database abstraction object.
#// @global WP_Locale $wp_locale     WordPress date and time locale object.
#// 
#// @param array $args {
#// Arguments for enqueuing media scripts.
#// 
#// @type int|WP_Post A post object or ID.
#// }
#//
def wp_enqueue_media(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Enqueue me just once per page, please.
    if did_action("wp_enqueue_media"):
        return
    # end if
    global content_width_
    global wpdb_
    global wp_locale_
    php_check_if_defined("content_width_","wpdb_","wp_locale_")
    defaults_ = Array({"post": None})
    args_ = wp_parse_args(args_, defaults_)
    #// We're going to pass the old thickbox media tabs to `media_upload_tabs`
    #// to ensure plugins will work. We will then unset those tabs.
    tabs_ = Array({"type": "", "type_url": "", "gallery": "", "library": ""})
    #// This filter is documented in wp-admin/includes/media.php
    tabs_ = apply_filters("media_upload_tabs", tabs_)
    tabs_["type"] = None
    tabs_["type_url"] = None
    tabs_["gallery"] = None
    tabs_["library"] = None
    props_ = Array({"link": get_option("image_default_link_type"), "align": get_option("image_default_align"), "size": get_option("image_default_size")})
    exts_ = php_array_merge(wp_get_audio_extensions(), wp_get_video_extensions())
    mimes_ = get_allowed_mime_types()
    ext_mimes_ = Array()
    for ext_ in exts_:
        for ext_preg_,mime_match_ in mimes_.items():
            if php_preg_match("#" + ext_ + "#i", ext_preg_):
                ext_mimes_[ext_] = mime_match_
                break
            # end if
        # end for
    # end for
    #// 
    #// Allows showing or hiding the "Create Audio Playlist" button in the media library.
    #// 
    #// By default, the "Create Audio Playlist" button will always be shown in
    #// the media library.  If this filter returns `null`, a query will be run
    #// to determine whether the media library contains any audio items.  This
    #// was the default behavior prior to version 4.8.0, but this query is
    #// expensive for large media libraries.
    #// 
    #// @since 4.7.4
    #// @since 4.8.0 The filter's default value is `true` rather than `null`.
    #// 
    #// @link https://core.trac.wordpress.org/ticket/31071
    #// 
    #// @param bool|null $show Whether to show the button, or `null` to decide based
    #// on whether any audio files exist in the media library.
    #//
    show_audio_playlist_ = apply_filters("media_library_show_audio_playlist", True)
    if None == show_audio_playlist_:
        show_audio_playlist_ = wpdb_.get_var(str("\n            SELECT ID\n         FROM ") + str(wpdb_.posts) + str("""\n          WHERE post_type = 'attachment'\n            AND post_mime_type LIKE 'audio%'\n          LIMIT 1\n       """))
    # end if
    #// 
    #// Allows showing or hiding the "Create Video Playlist" button in the media library.
    #// 
    #// By default, the "Create Video Playlist" button will always be shown in
    #// the media library.  If this filter returns `null`, a query will be run
    #// to determine whether the media library contains any video items.  This
    #// was the default behavior prior to version 4.8.0, but this query is
    #// expensive for large media libraries.
    #// 
    #// @since 4.7.4
    #// @since 4.8.0 The filter's default value is `true` rather than `null`.
    #// 
    #// @link https://core.trac.wordpress.org/ticket/31071
    #// 
    #// @param bool|null $show Whether to show the button, or `null` to decide based
    #// on whether any video files exist in the media library.
    #//
    show_video_playlist_ = apply_filters("media_library_show_video_playlist", True)
    if None == show_video_playlist_:
        show_video_playlist_ = wpdb_.get_var(str("\n            SELECT ID\n         FROM ") + str(wpdb_.posts) + str("""\n          WHERE post_type = 'attachment'\n            AND post_mime_type LIKE 'video%'\n          LIMIT 1\n       """))
    # end if
    #// 
    #// Allows overriding the list of months displayed in the media library.
    #// 
    #// By default (if this filter does not return an array), a query will be
    #// run to determine the months that have media items.  This query can be
    #// expensive for large media libraries, so it may be desirable for sites to
    #// override this behavior.
    #// 
    #// @since 4.7.4
    #// 
    #// @link https://core.trac.wordpress.org/ticket/31071
    #// 
    #// @param array|null $months An array of objects with `month` and `year`
    #// properties, or `null` (or any other non-array value)
    #// for default behavior.
    #//
    months_ = apply_filters("media_library_months_with_files", None)
    if (not php_is_array(months_)):
        months_ = wpdb_.get_results(wpdb_.prepare(str("\n           SELECT DISTINCT YEAR( post_date ) AS year, MONTH( post_date ) AS month\n            FROM ") + str(wpdb_.posts) + str("""\n          WHERE post_type = %s\n          ORDER BY post_date DESC\n       """), "attachment"))
    # end if
    for month_year_ in months_:
        month_year_.text = php_sprintf(__("%1$s %2$d"), wp_locale_.get_month(month_year_.month), month_year_.year)
    # end for
    settings_ = Array({"tabs": tabs_, "tabUrl": add_query_arg(Array({"chromeless": True}), admin_url("media-upload.php"))}, {"mimeTypes": wp_list_pluck(get_post_mime_types(), 0), "captions": (not apply_filters("disable_captions", "")), "nonce": Array({"sendToEditor": wp_create_nonce("media-send-to-editor")})}, {"post": Array({"id": 0})}, {"defaultProps": props_, "attachmentCounts": Array({"audio": 1 if show_audio_playlist_ else 0, "video": 1 if show_video_playlist_ else 0})}, {"oEmbedProxyUrl": rest_url("oembed/1.0/proxy"), "embedExts": exts_, "embedMimes": ext_mimes_, "contentWidth": content_width_, "months": months_, "mediaTrash": 1 if MEDIA_TRASH else 0})
    post_ = None
    if (php_isset(lambda : args_["post"])):
        post_ = get_post(args_["post"])
        settings_["post"] = Array({"id": post_.ID, "nonce": wp_create_nonce("update-post_" + post_.ID)})
        thumbnail_support_ = current_theme_supports("post-thumbnails", post_.post_type) and post_type_supports(post_.post_type, "thumbnail")
        if (not thumbnail_support_) and "attachment" == post_.post_type and post_.post_mime_type:
            if wp_attachment_is("audio", post_):
                thumbnail_support_ = post_type_supports("attachment:audio", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:audio")
            elif wp_attachment_is("video", post_):
                thumbnail_support_ = post_type_supports("attachment:video", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:video")
            # end if
        # end if
        if thumbnail_support_:
            featured_image_id_ = get_post_meta(post_.ID, "_thumbnail_id", True)
            settings_["post"]["featuredImageId"] = featured_image_id_ if featured_image_id_ else -1
        # end if
    # end if
    if post_:
        post_type_object_ = get_post_type_object(post_.post_type)
    else:
        post_type_object_ = get_post_type_object("post")
    # end if
    strings_ = Array({"mediaFrameDefaultTitle": __("Media"), "url": __("URL"), "addMedia": __("Add Media"), "search": __("Search"), "select": __("Select"), "cancel": __("Cancel"), "update": __("Update"), "replace": __("Replace"), "remove": __("Remove"), "back": __("Back"), "selected": __("%d selected"), "dragInfo": __("Drag and drop to reorder media files."), "uploadFilesTitle": __("Upload Files"), "uploadImagesTitle": __("Upload Images"), "mediaLibraryTitle": __("Media Library"), "insertMediaTitle": __("Add Media"), "createNewGallery": __("Create a new gallery"), "createNewPlaylist": __("Create a new playlist"), "createNewVideoPlaylist": __("Create a new video playlist"), "returnToLibrary": __("&#8592; Return to library"), "allMediaItems": __("All media items"), "allDates": __("All dates"), "noItemsFound": __("No items found."), "insertIntoPost": post_type_object_.labels.insert_into_item, "unattached": __("Unattached"), "mine": _x("Mine", "media items"), "trash": _x("Trash", "noun"), "uploadedToThisPost": post_type_object_.labels.uploaded_to_this_item, "warnDelete": __("You are about to permanently delete this item from your site.\nThis action cannot be undone.\n 'Cancel' to stop, 'OK' to delete."), "warnBulkDelete": __("You are about to permanently delete these items from your site.\nThis action cannot be undone.\n 'Cancel' to stop, 'OK' to delete."), "warnBulkTrash": __("You are about to trash these items.\n  'Cancel' to stop, 'OK' to delete."), "bulkSelect": __("Bulk Select"), "trashSelected": __("Move to Trash"), "restoreSelected": __("Restore from Trash"), "deletePermanently": __("Delete Permanently"), "apply": __("Apply"), "filterByDate": __("Filter by date"), "filterByType": __("Filter by type"), "searchLabel": __("Search"), "searchMediaLabel": __("Search Media"), "searchMediaPlaceholder": __("Search media items..."), "mediaFound": __("Number of media items found: %d"), "mediaFoundHasMoreResults": __("Number of media items displayed: %d. Scroll the page for more results."), "noMedia": __("No media items found."), "noMediaTryNewSearch": __("No media items found. Try a different search."), "attachmentDetails": __("Attachment Details"), "insertFromUrlTitle": __("Insert from URL"), "setFeaturedImageTitle": post_type_object_.labels.featured_image, "setFeaturedImage": post_type_object_.labels.set_featured_image, "createGalleryTitle": __("Create Gallery"), "editGalleryTitle": __("Edit Gallery"), "cancelGalleryTitle": __("&#8592; Cancel Gallery"), "insertGallery": __("Insert gallery"), "updateGallery": __("Update gallery"), "addToGallery": __("Add to gallery"), "addToGalleryTitle": __("Add to Gallery"), "reverseOrder": __("Reverse order"), "imageDetailsTitle": __("Image Details"), "imageReplaceTitle": __("Replace Image"), "imageDetailsCancel": __("Cancel Edit"), "editImage": __("Edit Image"), "chooseImage": __("Choose Image"), "selectAndCrop": __("Select and Crop"), "skipCropping": __("Skip Cropping"), "cropImage": __("Crop Image"), "cropYourImage": __("Crop your image"), "cropping": __("Cropping&hellip;"), "suggestedDimensions": __("Suggested image dimensions: %1$s by %2$s pixels."), "cropError": __("There has been an error cropping your image."), "audioDetailsTitle": __("Audio Details"), "audioReplaceTitle": __("Replace Audio"), "audioAddSourceTitle": __("Add Audio Source"), "audioDetailsCancel": __("Cancel Edit"), "videoDetailsTitle": __("Video Details"), "videoReplaceTitle": __("Replace Video"), "videoAddSourceTitle": __("Add Video Source"), "videoDetailsCancel": __("Cancel Edit"), "videoSelectPosterImageTitle": __("Select Poster Image"), "videoAddTrackTitle": __("Add Subtitles"), "playlistDragInfo": __("Drag and drop to reorder tracks."), "createPlaylistTitle": __("Create Audio Playlist"), "editPlaylistTitle": __("Edit Audio Playlist"), "cancelPlaylistTitle": __("&#8592; Cancel Audio Playlist"), "insertPlaylist": __("Insert audio playlist"), "updatePlaylist": __("Update audio playlist"), "addToPlaylist": __("Add to audio playlist"), "addToPlaylistTitle": __("Add to Audio Playlist"), "videoPlaylistDragInfo": __("Drag and drop to reorder videos."), "createVideoPlaylistTitle": __("Create Video Playlist"), "editVideoPlaylistTitle": __("Edit Video Playlist"), "cancelVideoPlaylistTitle": __("&#8592; Cancel Video Playlist"), "insertVideoPlaylist": __("Insert video playlist"), "updateVideoPlaylist": __("Update video playlist"), "addToVideoPlaylist": __("Add to video playlist"), "addToVideoPlaylistTitle": __("Add to Video Playlist"), "filterAttachments": __("Filter Media"), "attachmentsList": __("Media list")})
    #// 
    #// Filters the media view settings.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array   $settings List of media view settings.
    #// @param WP_Post $post     Post object.
    #//
    settings_ = apply_filters("media_view_settings", settings_, post_)
    #// 
    #// Filters the media view strings.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string[] $strings Array of media view strings keyed by the name they'll be referenced by in JavaScript.
    #// @param WP_Post  $post    Post object.
    #//
    strings_ = apply_filters("media_view_strings", strings_, post_)
    strings_["settings"] = settings_
    #// Ensure we enqueue media-editor first, that way media-views
    #// is registered internally before we try to localize it. See #24724.
    wp_enqueue_script("media-editor")
    wp_localize_script("media-views", "_wpMediaViewsL10n", strings_)
    wp_enqueue_script("media-audiovideo")
    wp_enqueue_style("media-views")
    if is_admin():
        wp_enqueue_script("mce-view")
        wp_enqueue_script("image-edit")
    # end if
    wp_enqueue_style("imgareaselect")
    wp_plupload_default_settings()
    php_include_file(ABSPATH + WPINC + "/media-template.php", once=True)
    add_action("admin_footer", "wp_print_media_templates")
    add_action("wp_footer", "wp_print_media_templates")
    add_action("customize_controls_print_footer_scripts", "wp_print_media_templates")
    #// 
    #// Fires at the conclusion of wp_enqueue_media().
    #// 
    #// @since 3.5.0
    #//
    do_action("wp_enqueue_media")
# end def wp_enqueue_media
#// 
#// Retrieves media attached to the passed post.
#// 
#// @since 3.6.0
#// 
#// @param string      $type Mime type.
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return WP_Post[] Array of media attached to the given post.
#//
def get_attached_media(type_=None, post_=0, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return Array()
    # end if
    args_ = Array({"post_parent": post_.ID, "post_type": "attachment", "post_mime_type": type_, "posts_per_page": -1, "orderby": "menu_order", "order": "ASC"})
    #// 
    #// Filters arguments used to retrieve media attached to the given post.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array   $args Post query arguments.
    #// @param string  $type Mime type of the desired media.
    #// @param WP_Post $post Post object.
    #//
    args_ = apply_filters("get_attached_media_args", args_, type_, post_)
    children_ = get_children(args_)
    #// 
    #// Filters the list of media attached to the given post.
    #// 
    #// @since 3.6.0
    #// 
    #// @param WP_Post[] $children Array of media attached to the given post.
    #// @param string    $type     Mime type of the media desired.
    #// @param WP_Post   $post     Post object.
    #//
    return apply_filters("get_attached_media", children_, type_, post_)
# end def get_attached_media
#// 
#// Check the content HTML for a audio, video, object, embed, or iframe tags.
#// 
#// @since 3.6.0
#// 
#// @param string   $content A string of HTML which might contain media elements.
#// @param string[] $types   An array of media types: 'audio', 'video', 'object', 'embed', or 'iframe'.
#// @return string[] Array of found HTML media elements.
#//
def get_media_embedded_in_content(content_=None, types_=None, *_args_):
    if types_ is None:
        types_ = None
    # end if
    
    html_ = Array()
    #// 
    #// Filters the embedded media types that are allowed to be returned from the content blob.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string[] $allowed_media_types An array of allowed media types. Default media types are
    #// 'audio', 'video', 'object', 'embed', and 'iframe'.
    #//
    allowed_media_types_ = apply_filters("media_embedded_in_content_allowed_types", Array("audio", "video", "object", "embed", "iframe"))
    if (not php_empty(lambda : types_)):
        if (not php_is_array(types_)):
            types_ = Array(types_)
        # end if
        allowed_media_types_ = php_array_intersect(allowed_media_types_, types_)
    # end if
    tags_ = php_implode("|", allowed_media_types_)
    if preg_match_all("#<(?P<tag>" + tags_ + ")[^<]*?(?:>[\\s\\S]*?<\\/(?P=tag)>|\\s*\\/>)#", content_, matches_):
        for match_ in matches_[0]:
            html_[-1] = match_
        # end for
    # end if
    return html_
# end def get_media_embedded_in_content
#// 
#// Retrieves galleries from the passed post's content.
#// 
#// @since 3.6.0
#// 
#// @param int|WP_Post $post Post ID or object.
#// @param bool        $html Optional. Whether to return HTML or data in the array. Default true.
#// @return array A list of arrays, each containing gallery data and srcs parsed
#// from the expanded shortcode.
#//
def get_post_galleries(post_=None, html_=None, *_args_):
    if html_ is None:
        html_ = True
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return Array()
    # end if
    if (not has_shortcode(post_.post_content, "gallery")):
        return Array()
    # end if
    galleries_ = Array()
    if preg_match_all("/" + get_shortcode_regex() + "/s", post_.post_content, matches_, PREG_SET_ORDER):
        for shortcode_ in matches_:
            if "gallery" == shortcode_[2]:
                srcs_ = Array()
                shortcode_attrs_ = shortcode_parse_atts(shortcode_[3])
                if (not php_is_array(shortcode_attrs_)):
                    shortcode_attrs_ = Array()
                # end if
                #// Specify the post id of the gallery we're viewing if the shortcode doesn't reference another post already.
                if (not (php_isset(lambda : shortcode_attrs_["id"]))):
                    shortcode_[3] += " id=\"" + php_intval(post_.ID) + "\""
                # end if
                gallery_ = do_shortcode_tag(shortcode_)
                if html_:
                    galleries_[-1] = gallery_
                else:
                    preg_match_all("#src=(['\"])(.+?)\\1#is", gallery_, src_, PREG_SET_ORDER)
                    if (not php_empty(lambda : src_)):
                        for s_ in src_:
                            srcs_[-1] = s_[2]
                        # end for
                    # end if
                    galleries_[-1] = php_array_merge(shortcode_attrs_, Array({"src": php_array_values(array_unique(srcs_))}))
                # end if
            # end if
        # end for
    # end if
    #// 
    #// Filters the list of all found galleries in the given post.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array   $galleries Associative array of all found post galleries.
    #// @param WP_Post $post      Post object.
    #//
    return apply_filters("get_post_galleries", galleries_, post_)
# end def get_post_galleries
#// 
#// Check a specified post's content for gallery and, if present, return the first
#// 
#// @since 3.6.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @param bool        $html Optional. Whether to return HTML or data. Default is true.
#// @return string|array Gallery data and srcs parsed from the expanded shortcode.
#//
def get_post_gallery(post_=0, html_=None, *_args_):
    if html_ is None:
        html_ = True
    # end if
    
    galleries_ = get_post_galleries(post_, html_)
    gallery_ = reset(galleries_)
    #// 
    #// Filters the first-found post gallery.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array       $gallery   The first-found post gallery.
    #// @param int|WP_Post $post      Post ID or object.
    #// @param array       $galleries Associative array of all found post galleries.
    #//
    return apply_filters("get_post_gallery", gallery_, post_, galleries_)
# end def get_post_gallery
#// 
#// Retrieve the image srcs from galleries from a post's content, if present
#// 
#// @since 3.6.0
#// 
#// @see get_post_galleries()
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global `$post`.
#// @return array A list of lists, each containing image srcs parsed.
#// from an expanded shortcode
#//
def get_post_galleries_images(post_=0, *_args_):
    
    
    galleries_ = get_post_galleries(post_, False)
    return wp_list_pluck(galleries_, "src")
# end def get_post_galleries_images
#// 
#// Checks a post's content for galleries and return the image srcs for the first found gallery
#// 
#// @since 3.6.0
#// 
#// @see get_post_gallery()
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global `$post`.
#// @return string[] A list of a gallery's image srcs in order.
#//
def get_post_gallery_images(post_=0, *_args_):
    
    
    gallery_ = get_post_gallery(post_, False)
    return Array() if php_empty(lambda : gallery_["src"]) else gallery_["src"]
# end def get_post_gallery_images
#// 
#// Maybe attempts to generate attachment metadata, if missing.
#// 
#// @since 3.9.0
#// 
#// @param WP_Post $attachment Attachment object.
#//
def wp_maybe_generate_attachment_metadata(attachment_=None, *_args_):
    
    
    if php_empty(lambda : attachment_) or php_empty(lambda : attachment_.ID):
        return
    # end if
    attachment_id_ = php_int(attachment_.ID)
    file_ = get_attached_file(attachment_id_)
    meta_ = wp_get_attachment_metadata(attachment_id_)
    if php_empty(lambda : meta_) and php_file_exists(file_):
        _meta_ = get_post_meta(attachment_id_)
        _lock_ = "wp_generating_att_" + attachment_id_
        if (not php_array_key_exists("_wp_attachment_metadata", _meta_)) and (not get_transient(_lock_)):
            set_transient(_lock_, file_)
            wp_update_attachment_metadata(attachment_id_, wp_generate_attachment_metadata(attachment_id_, file_))
            delete_transient(_lock_)
        # end if
    # end if
# end def wp_maybe_generate_attachment_metadata
#// 
#// Tries to convert an attachment URL into a post ID.
#// 
#// @since 4.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $url The URL to resolve.
#// @return int The found post ID, or 0 on failure.
#//
def attachment_url_to_postid(url_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    dir_ = wp_get_upload_dir()
    path_ = url_
    site_url_ = php_parse_url(dir_["url"])
    image_path_ = php_parse_url(path_)
    #// Force the protocols to match if needed.
    if (php_isset(lambda : image_path_["scheme"])) and image_path_["scheme"] != site_url_["scheme"]:
        path_ = php_str_replace(image_path_["scheme"], site_url_["scheme"], path_)
    # end if
    if 0 == php_strpos(path_, dir_["baseurl"] + "/"):
        path_ = php_substr(path_, php_strlen(dir_["baseurl"] + "/"))
    # end if
    sql_ = wpdb_.prepare(str("SELECT post_id, meta_value FROM ") + str(wpdb_.postmeta) + str(" WHERE meta_key = '_wp_attached_file' AND meta_value = %s"), path_)
    results_ = wpdb_.get_results(sql_)
    post_id_ = None
    if results_:
        #// Use the first available result, but prefer a case-sensitive match, if exists.
        post_id_ = reset(results_).post_id
        if php_count(results_) > 1:
            for result_ in results_:
                if path_ == result_.meta_value:
                    post_id_ = result_.post_id
                    break
                # end if
            # end for
        # end if
    # end if
    #// 
    #// Filters an attachment id found by URL.
    #// 
    #// @since 4.2.0
    #// 
    #// @param int|null $post_id The post_id (if any) found by the function.
    #// @param string   $url     The URL being looked up.
    #//
    return php_int(apply_filters("attachment_url_to_postid", post_id_, url_))
# end def attachment_url_to_postid
#// 
#// Returns the URLs for CSS files used in an iframe-sandbox'd TinyMCE media view.
#// 
#// @since 4.0.0
#// 
#// @return string[] The relevant CSS file URLs.
#//
def wpview_media_sandbox_styles(*_args_):
    
    
    version_ = "ver=" + get_bloginfo("version")
    mediaelement_ = includes_url(str("js/mediaelement/mediaelementplayer-legacy.min.css?") + str(version_))
    wpmediaelement_ = includes_url(str("js/mediaelement/wp-mediaelement.css?") + str(version_))
    return Array(mediaelement_, wpmediaelement_)
# end def wpview_media_sandbox_styles
#// 
#// Registers the personal data exporter for media.
#// 
#// @param array[] $exporters An array of personal data exporters, keyed by their ID.
#// @return array[] Updated array of personal data exporters.
#//
def wp_register_media_personal_data_exporter(exporters_=None, *_args_):
    
    
    exporters_["wordpress-media"] = Array({"exporter_friendly_name": __("WordPress Media"), "callback": "wp_media_personal_data_exporter"})
    return exporters_
# end def wp_register_media_personal_data_exporter
#// 
#// Finds and exports attachments associated with an email address.
#// 
#// @since 4.9.6
#// 
#// @param  string $email_address The attachment owner email address.
#// @param  int    $page          Attachment page.
#// @return array  $return        An array of personal data.
#//
def wp_media_personal_data_exporter(email_address_=None, page_=1, *_args_):
    
    
    #// Limit us to 50 attachments at a time to avoid timing out.
    number_ = 50
    page_ = php_int(page_)
    data_to_export_ = Array()
    user_ = get_user_by("email", email_address_)
    if False == user_:
        return Array({"data": data_to_export_, "done": True})
    # end if
    post_query_ = php_new_class("WP_Query", lambda : WP_Query(Array({"author": user_.ID, "posts_per_page": number_, "paged": page_, "post_type": "attachment", "post_status": "any", "orderby": "ID", "order": "ASC"})))
    for post_ in post_query_.posts:
        attachment_url_ = wp_get_attachment_url(post_.ID)
        if attachment_url_:
            post_data_to_export_ = Array(Array({"name": __("URL"), "value": attachment_url_}))
            data_to_export_[-1] = Array({"group_id": "media", "group_label": __("Media"), "group_description": __("User&#8217;s media data."), "item_id": str("post-") + str(post_.ID), "data": post_data_to_export_})
        # end if
    # end for
    done_ = post_query_.max_num_pages <= page_
    return Array({"data": data_to_export_, "done": done_})
# end def wp_media_personal_data_exporter
#// 
#// Add additional default image sub-sizes.
#// 
#// These sizes are meant to enhance the way WordPress displays images on the front-end on larger,
#// high-density devices. They make it possible to generate more suitable `srcset` and `sizes` attributes
#// when the users upload large images.
#// 
#// The sizes can be changed or removed by themes and plugins but that is not recommended.
#// The size "names" reflect the image dimensions, so changing the sizes would be quite misleading.
#// 
#// @since 5.3.0
#// @access private
#//
def _wp_add_additional_image_sizes(*_args_):
    
    
    #// 2x medium_large size.
    add_image_size("1536x1536", 1536, 1536)
    #// 2x large size.
    add_image_size("2048x2048", 2048, 2048)
# end def _wp_add_additional_image_sizes
