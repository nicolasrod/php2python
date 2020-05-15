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
def wp_get_additional_image_sizes(*args_):
    
    global _wp_additional_image_sizes
    php_check_if_defined("_wp_additional_image_sizes")
    if (not _wp_additional_image_sizes):
        _wp_additional_image_sizes = Array()
    # end if
    return _wp_additional_image_sizes
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
def image_constrain_size_for_editor(width=None, height=None, size="medium", context=None, *args_):
    
    global content_width
    php_check_if_defined("content_width")
    _wp_additional_image_sizes = wp_get_additional_image_sizes()
    if (not context):
        context = "edit" if is_admin() else "display"
    # end if
    if php_is_array(size):
        max_width = size[0]
        max_height = size[1]
    elif "thumb" == size or "thumbnail" == size:
        max_width = php_intval(get_option("thumbnail_size_w"))
        max_height = php_intval(get_option("thumbnail_size_h"))
        #// Last chance thumbnail size defaults.
        if (not max_width) and (not max_height):
            max_width = 128
            max_height = 96
        # end if
    elif "medium" == size:
        max_width = php_intval(get_option("medium_size_w"))
        max_height = php_intval(get_option("medium_size_h"))
    elif "medium_large" == size:
        max_width = php_intval(get_option("medium_large_size_w"))
        max_height = php_intval(get_option("medium_large_size_h"))
        if php_intval(content_width) > 0:
            max_width = php_min(php_intval(content_width), max_width)
        # end if
    elif "large" == size:
        #// 
        #// We're inserting a large size image into the editor. If it's a really
        #// big image we'll scale it down to fit reasonably within the editor
        #// itself, and within the theme's content width if it's known. The user
        #// can resize it in the editor if they wish.
        #//
        max_width = php_intval(get_option("large_size_w"))
        max_height = php_intval(get_option("large_size_h"))
        if php_intval(content_width) > 0:
            max_width = php_min(php_intval(content_width), max_width)
        # end if
    elif (not php_empty(lambda : _wp_additional_image_sizes)) and php_in_array(size, php_array_keys(_wp_additional_image_sizes), True):
        max_width = php_intval(_wp_additional_image_sizes[size]["width"])
        max_height = php_intval(_wp_additional_image_sizes[size]["height"])
        #// Only in admin. Assume that theme authors know what they're doing.
        if php_intval(content_width) > 0 and "edit" == context:
            max_width = php_min(php_intval(content_width), max_width)
        # end if
    else:
        #// $size === 'full' has no constraint.
        max_width = width
        max_height = height
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
    max_width, max_height = apply_filters("editor_max_image_size", Array(max_width, max_height), size, context)
    return wp_constrain_dimensions(width, height, max_width, max_height)
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
def image_hwstring(width=None, height=None, *args_):
    
    out = ""
    if width:
        out += "width=\"" + php_intval(width) + "\" "
    # end if
    if height:
        out += "height=\"" + php_intval(height) + "\" "
    # end if
    return out
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
def image_downsize(id=None, size="medium", *args_):
    
    is_image = wp_attachment_is_image(id)
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
    out = apply_filters("image_downsize", False, id, size)
    if out:
        return out
    # end if
    img_url = wp_get_attachment_url(id)
    meta = wp_get_attachment_metadata(id)
    width = 0
    height = 0
    is_intermediate = False
    img_url_basename = wp_basename(img_url)
    #// If the file isn't an image, attempt to replace its URL with a rendered image from its meta.
    #// Otherwise, a non-image type could be returned.
    if (not is_image):
        if (not php_empty(lambda : meta["sizes"]["full"])):
            img_url = php_str_replace(img_url_basename, meta["sizes"]["full"]["file"], img_url)
            img_url_basename = meta["sizes"]["full"]["file"]
            width = meta["sizes"]["full"]["width"]
            height = meta["sizes"]["full"]["height"]
        else:
            return False
        # end if
    # end if
    #// Try for a new style intermediate size.
    intermediate = image_get_intermediate_size(id, size)
    if intermediate:
        img_url = php_str_replace(img_url_basename, intermediate["file"], img_url)
        width = intermediate["width"]
        height = intermediate["height"]
        is_intermediate = True
    elif "thumbnail" == size:
        #// Fall back to the old thumbnail.
        thumb_file = wp_get_attachment_thumb_file(id)
        info = None
        if thumb_file:
            info = php_no_error(lambda: getimagesize(thumb_file))
        # end if
        if thumb_file and info:
            img_url = php_str_replace(img_url_basename, wp_basename(thumb_file), img_url)
            width = info[0]
            height = info[1]
            is_intermediate = True
        # end if
    # end if
    if (not width) and (not height) and (php_isset(lambda : meta["width"]) and php_isset(lambda : meta["height"])):
        #// Any other type: use the real image.
        width = meta["width"]
        height = meta["height"]
    # end if
    if img_url:
        #// We have the actual image size, but might need to further constrain it if content_width is narrower.
        width, height = image_constrain_size_for_editor(width, height, size)
        return Array(img_url, width, height, is_intermediate)
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
def add_image_size(name=None, width=0, height=0, crop=False, *args_):
    
    global _wp_additional_image_sizes
    php_check_if_defined("_wp_additional_image_sizes")
    _wp_additional_image_sizes[name] = Array({"width": absint(width), "height": absint(height), "crop": crop})
# end def add_image_size
#// 
#// Check if an image size exists.
#// 
#// @since 3.9.0
#// 
#// @param string $name The image size to check.
#// @return bool True if the image size exists, false if not.
#//
def has_image_size(name=None, *args_):
    
    sizes = wp_get_additional_image_sizes()
    return (php_isset(lambda : sizes[name]))
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
def remove_image_size(name=None, *args_):
    
    global _wp_additional_image_sizes
    php_check_if_defined("_wp_additional_image_sizes")
    if (php_isset(lambda : _wp_additional_image_sizes[name])):
        _wp_additional_image_sizes[name] = None
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
def set_post_thumbnail_size(width=0, height=0, crop=False, *args_):
    
    add_image_size("post-thumbnail", width, height, crop)
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
def get_image_tag(id=None, alt=None, title=None, align=None, size="medium", *args_):
    
    img_src, width, height = image_downsize(id, size)
    hwstring = image_hwstring(width, height)
    title = "title=\"" + esc_attr(title) + "\" " if title else ""
    class_ = "align" + esc_attr(align) + " size-" + esc_attr(size) + " wp-image-" + id
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
    class_ = apply_filters("get_image_tag_class", class_, id, align, size)
    html = "<img src=\"" + esc_attr(img_src) + "\" alt=\"" + esc_attr(alt) + "\" " + title + hwstring + "class=\"" + class_ + "\" />"
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
    return apply_filters("get_image_tag", html, id, alt, title, align, size)
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
def wp_constrain_dimensions(current_width=None, current_height=None, max_width=0, max_height=0, *args_):
    
    if (not max_width) and (not max_height):
        return Array(current_width, current_height)
    # end if
    width_ratio = 1
    height_ratio = 1
    did_width = False
    did_height = False
    if max_width > 0 and current_width > 0 and current_width > max_width:
        width_ratio = max_width / current_width
        did_width = True
    # end if
    if max_height > 0 and current_height > 0 and current_height > max_height:
        height_ratio = max_height / current_height
        did_height = True
    # end if
    #// Calculate the larger/smaller ratios.
    smaller_ratio = php_min(width_ratio, height_ratio)
    larger_ratio = php_max(width_ratio, height_ratio)
    if int(round(current_width * larger_ratio)) > max_width or int(round(current_height * larger_ratio)) > max_height:
        #// The larger ratio is too big. It would result in an overflow.
        ratio = smaller_ratio
    else:
        #// The larger ratio fits, and is likely to be a more "snug" fit.
        ratio = larger_ratio
    # end if
    #// Very small dimensions may result in 0, 1 should be the minimum.
    w = php_max(1, int(round(current_width * ratio)))
    h = php_max(1, int(round(current_height * ratio)))
    #// 
    #// Sometimes, due to rounding, we'll end up with a result like this:
    #// 465x700 in a 177x177 box is 117x176... a pixel short.
    #// We also have issues with recursive calls resulting in an ever-changing result.
    #// Constraining to the result of a constraint should yield the original result.
    #// Thus we look for dimensions that are one pixel shy of the max value and bump them up.
    #// 
    #// Note: $did_width means it is possible $smaller_ratio == $width_ratio.
    if did_width and w == max_width - 1:
        w = max_width
        pass
    # end if
    #// Note: $did_height means it is possible $smaller_ratio == $height_ratio.
    if did_height and h == max_height - 1:
        h = max_height
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
    return apply_filters("wp_constrain_dimensions", Array(w, h), current_width, current_height, max_width, max_height)
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
def image_resize_dimensions(orig_w=None, orig_h=None, dest_w=None, dest_h=None, crop=False, *args_):
    
    if orig_w <= 0 or orig_h <= 0:
        return False
    # end if
    #// At least one of $dest_w or $dest_h must be specific.
    if dest_w <= 0 and dest_h <= 0:
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
    output = apply_filters("image_resize_dimensions", None, orig_w, orig_h, dest_w, dest_h, crop)
    if None != output:
        return output
    # end if
    #// Stop if the destination size is larger than the original image dimensions.
    if php_empty(lambda : dest_h):
        if orig_w < dest_w:
            return False
        # end if
    elif php_empty(lambda : dest_w):
        if orig_h < dest_h:
            return False
        # end if
    else:
        if orig_w < dest_w and orig_h < dest_h:
            return False
        # end if
    # end if
    if crop:
        #// 
        #// Crop the largest possible portion of the original image that we can size to $dest_w x $dest_h.
        #// Note that the requested crop dimensions are used as a maximum bounding box for the original image.
        #// If the original image's width or height is less than the requested width or height
        #// only the greater one will be cropped.
        #// For example when the original image is 600x300, and the requested crop dimensions are 400x400,
        #// the resulting image will be 400x300.
        #//
        aspect_ratio = orig_w / orig_h
        new_w = php_min(dest_w, orig_w)
        new_h = php_min(dest_h, orig_h)
        if (not new_w):
            new_w = int(round(new_h * aspect_ratio))
        # end if
        if (not new_h):
            new_h = int(round(new_w / aspect_ratio))
        # end if
        size_ratio = php_max(new_w / orig_w, new_h / orig_h)
        crop_w = round(new_w / size_ratio)
        crop_h = round(new_h / size_ratio)
        if (not php_is_array(crop)) or php_count(crop) != 2:
            crop = Array("center", "center")
        # end if
        x, y = crop
        if "left" == x:
            s_x = 0
        elif "right" == x:
            s_x = orig_w - crop_w
        else:
            s_x = floor(orig_w - crop_w / 2)
        # end if
        if "top" == y:
            s_y = 0
        elif "bottom" == y:
            s_y = orig_h - crop_h
        else:
            s_y = floor(orig_h - crop_h / 2)
        # end if
    else:
        #// Resize using $dest_w x $dest_h as a maximum bounding box.
        crop_w = orig_w
        crop_h = orig_h
        s_x = 0
        s_y = 0
        new_w, new_h = wp_constrain_dimensions(orig_w, orig_h, dest_w, dest_h)
    # end if
    if wp_fuzzy_number_match(new_w, orig_w) and wp_fuzzy_number_match(new_h, orig_h):
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
        proceed = bool(apply_filters("wp_image_resize_identical_dimensions", False, orig_w, orig_h))
        if (not proceed):
            return False
        # end if
    # end if
    #// The return array matches the parameters to imagecopyresampled().
    #// int dst_x, int dst_y, int src_x, int src_y, int dst_w, int dst_h, int src_w, int src_h
    return Array(0, 0, int(s_x), int(s_y), int(new_w), int(new_h), int(crop_w), int(crop_h))
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
def image_make_intermediate_size(file=None, width=None, height=None, crop=False, *args_):
    
    if width or height:
        editor = wp_get_image_editor(file)
        if is_wp_error(editor) or is_wp_error(editor.resize(width, height, crop)):
            return False
        # end if
        resized_file = editor.save()
        if (not is_wp_error(resized_file)) and resized_file:
            resized_file["path"] = None
            return resized_file
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
def wp_image_matches_ratio(source_width=None, source_height=None, target_width=None, target_height=None, *args_):
    
    #// 
    #// To test for varying crops, we constrain the dimensions of the larger image
    #// to the dimensions of the smaller image and see if they match.
    #//
    if source_width > target_width:
        constrained_size = wp_constrain_dimensions(source_width, source_height, target_width)
        expected_size = Array(target_width, target_height)
    else:
        constrained_size = wp_constrain_dimensions(target_width, target_height, source_width)
        expected_size = Array(source_width, source_height)
    # end if
    #// If the image dimensions are within 1px of the expected size, we consider it a match.
    matched = wp_fuzzy_number_match(constrained_size[0], expected_size[0]) and wp_fuzzy_number_match(constrained_size[1], expected_size[1])
    return matched
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
def image_get_intermediate_size(post_id=None, size="thumbnail", *args_):
    
    imagedata = wp_get_attachment_metadata(post_id)
    if (not size) or (not php_is_array(imagedata)) or php_empty(lambda : imagedata["sizes"]):
        return False
    # end if
    data = Array()
    #// Find the best match when '$size' is an array.
    if php_is_array(size):
        candidates = Array()
        if (not (php_isset(lambda : imagedata["file"]))) and (php_isset(lambda : imagedata["sizes"]["full"])):
            imagedata["height"] = imagedata["sizes"]["full"]["height"]
            imagedata["width"] = imagedata["sizes"]["full"]["width"]
        # end if
        for _size,data in imagedata["sizes"]:
            #// If there's an exact match to an existing image size, short circuit.
            if php_intval(data["width"]) == php_intval(size[0]) and php_intval(data["height"]) == php_intval(size[1]):
                candidates[data["width"] * data["height"]] = data
                break
            # end if
            #// If it's not an exact match, consider larger sizes with the same aspect ratio.
            if data["width"] >= size[0] and data["height"] >= size[1]:
                #// If '0' is passed to either size, we test ratios against the original file.
                if 0 == size[0] or 0 == size[1]:
                    same_ratio = wp_image_matches_ratio(data["width"], data["height"], imagedata["width"], imagedata["height"])
                else:
                    same_ratio = wp_image_matches_ratio(data["width"], data["height"], size[0], size[1])
                # end if
                if same_ratio:
                    candidates[data["width"] * data["height"]] = data
                # end if
            # end if
        # end for
        if (not php_empty(lambda : candidates)):
            #// Sort the array by size if we have more than one candidate.
            if 1 < php_count(candidates):
                ksort(candidates)
            # end if
            data = php_array_shift(candidates)
            pass
        elif (not php_empty(lambda : imagedata["sizes"]["thumbnail"])) and imagedata["sizes"]["thumbnail"]["width"] >= size[0] and imagedata["sizes"]["thumbnail"]["width"] >= size[1]:
            data = imagedata["sizes"]["thumbnail"]
        else:
            return False
        # end if
        #// Constrain the width and height attributes to the requested values.
        data["width"], data["height"] = image_constrain_size_for_editor(data["width"], data["height"], size)
    elif (not php_empty(lambda : imagedata["sizes"][size])):
        data = imagedata["sizes"][size]
    # end if
    #// If we still don't have a match at this point, return false.
    if php_empty(lambda : data):
        return False
    # end if
    #// Include the full filesystem path of the intermediate file.
    if php_empty(lambda : data["path"]) and (not php_empty(lambda : data["file"])) and (not php_empty(lambda : imagedata["file"])):
        file_url = wp_get_attachment_url(post_id)
        data["path"] = path_join(php_dirname(imagedata["file"]), data["file"])
        data["url"] = path_join(php_dirname(file_url), data["file"])
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
    return apply_filters("image_get_intermediate_size", data, post_id, size)
# end def image_get_intermediate_size
#// 
#// Gets the available intermediate image size names.
#// 
#// @since 3.0.0
#// 
#// @return string[] An array of image size names.
#//
def get_intermediate_image_sizes(*args_):
    
    default_sizes = Array("thumbnail", "medium", "medium_large", "large")
    additional_sizes = wp_get_additional_image_sizes()
    if (not php_empty(lambda : additional_sizes)):
        default_sizes = php_array_merge(default_sizes, php_array_keys(additional_sizes))
    # end if
    #// 
    #// Filters the list of intermediate image sizes.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string[] $default_sizes An array of intermediate image size names. Defaults
    #// are 'thumbnail', 'medium', 'medium_large', 'large'.
    #//
    return apply_filters("intermediate_image_sizes", default_sizes)
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
def wp_get_registered_image_subsizes(*args_):
    
    additional_sizes = wp_get_additional_image_sizes()
    all_sizes = Array()
    for size_name in get_intermediate_image_sizes():
        size_data = Array({"width": 0, "height": 0, "crop": False})
        if (php_isset(lambda : additional_sizes[size_name]["width"])):
            #// For sizes added by plugins and themes.
            size_data["width"] = php_intval(additional_sizes[size_name]["width"])
        else:
            #// For default sizes set in options.
            size_data["width"] = php_intval(get_option(str(size_name) + str("_size_w")))
        # end if
        if (php_isset(lambda : additional_sizes[size_name]["height"])):
            size_data["height"] = php_intval(additional_sizes[size_name]["height"])
        else:
            size_data["height"] = php_intval(get_option(str(size_name) + str("_size_h")))
        # end if
        if php_empty(lambda : size_data["width"]) and php_empty(lambda : size_data["height"]):
            continue
        # end if
        if (php_isset(lambda : additional_sizes[size_name]["crop"])):
            size_data["crop"] = additional_sizes[size_name]["crop"]
        else:
            size_data["crop"] = get_option(str(size_name) + str("_crop"))
        # end if
        if (not php_is_array(size_data["crop"])) or php_empty(lambda : size_data["crop"]):
            size_data["crop"] = bool(size_data["crop"])
        # end if
        all_sizes[size_name] = size_data
    # end for
    return all_sizes
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
def wp_get_attachment_image_src(attachment_id=None, size="thumbnail", icon=False, *args_):
    
    #// Get a thumbnail or intermediate image if there is one.
    image = image_downsize(attachment_id, size)
    if (not image):
        src = False
        if icon:
            src = wp_mime_type_icon(attachment_id)
            if src:
                #// This filter is documented in wp-includes/post.php
                icon_dir = apply_filters("icon_dir", ABSPATH + WPINC + "/images/media")
                src_file = icon_dir + "/" + wp_basename(src)
                width, height = php_no_error(lambda: getimagesize(src_file))
            # end if
        # end if
        if src and width and height:
            image = Array(src, width, height)
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
    return apply_filters("wp_get_attachment_image_src", image, attachment_id, size, icon)
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
def wp_get_attachment_image(attachment_id=None, size="thumbnail", icon=False, attr="", *args_):
    
    html = ""
    image = wp_get_attachment_image_src(attachment_id, size, icon)
    if image:
        src, width, height = image
        hwstring = image_hwstring(width, height)
        size_class = size
        if php_is_array(size_class):
            size_class = join("x", size_class)
        # end if
        attachment = get_post(attachment_id)
        default_attr = Array({"src": src, "class": str("attachment-") + str(size_class) + str(" size-") + str(size_class), "alt": php_trim(strip_tags(get_post_meta(attachment_id, "_wp_attachment_image_alt", True)))})
        attr = wp_parse_args(attr, default_attr)
        #// Generate 'srcset' and 'sizes' if not already present.
        if php_empty(lambda : attr["srcset"]):
            image_meta = wp_get_attachment_metadata(attachment_id)
            if php_is_array(image_meta):
                size_array = Array(absint(width), absint(height))
                srcset = wp_calculate_image_srcset(size_array, src, image_meta, attachment_id)
                sizes = wp_calculate_image_sizes(size_array, src, image_meta, attachment_id)
                if srcset and sizes or (not php_empty(lambda : attr["sizes"])):
                    attr["srcset"] = srcset
                    if php_empty(lambda : attr["sizes"]):
                        attr["sizes"] = sizes
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
        attr = apply_filters("wp_get_attachment_image_attributes", attr, attachment, size)
        attr = php_array_map("esc_attr", attr)
        html = php_rtrim(str("<img ") + str(hwstring))
        for name,value in attr:
            html += str(" ") + str(name) + str("=") + "\"" + value + "\""
        # end for
        html += " />"
    # end if
    return html
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
def wp_get_attachment_image_url(attachment_id=None, size="thumbnail", icon=False, *args_):
    
    image = wp_get_attachment_image_src(attachment_id, size, icon)
    return image["0"] if (php_isset(lambda : image["0"])) else False
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
def _wp_get_attachment_relative_path(file=None, *args_):
    
    dirname = php_dirname(file)
    if "." == dirname:
        return ""
    # end if
    if False != php_strpos(dirname, "wp-content/uploads"):
        #// Get the directory name relative to the upload directory (back compat for pre-2.7 uploads).
        dirname = php_substr(dirname, php_strpos(dirname, "wp-content/uploads") + 18)
        dirname = php_ltrim(dirname, "/")
    # end if
    return dirname
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
def _wp_get_image_size_from_meta(size_name=None, image_meta=None, *args_):
    
    if "full" == size_name:
        return Array(absint(image_meta["width"]), absint(image_meta["height"]))
    elif (not php_empty(lambda : image_meta["sizes"][size_name])):
        return Array(absint(image_meta["sizes"][size_name]["width"]), absint(image_meta["sizes"][size_name]["height"]))
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
def wp_get_attachment_image_srcset(attachment_id=None, size="medium", image_meta=None, *args_):
    
    image = wp_get_attachment_image_src(attachment_id, size)
    if (not image):
        return False
    # end if
    if (not php_is_array(image_meta)):
        image_meta = wp_get_attachment_metadata(attachment_id)
    # end if
    image_src = image[0]
    size_array = Array(absint(image[1]), absint(image[2]))
    return wp_calculate_image_srcset(size_array, image_src, image_meta, attachment_id)
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
def wp_calculate_image_srcset(size_array=None, image_src=None, image_meta=None, attachment_id=0, *args_):
    
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
    image_meta = apply_filters("wp_calculate_image_srcset_meta", image_meta, size_array, image_src, attachment_id)
    if php_empty(lambda : image_meta["sizes"]) or (not (php_isset(lambda : image_meta["file"]))) or php_strlen(image_meta["file"]) < 4:
        return False
    # end if
    image_sizes = image_meta["sizes"]
    #// Get the width and height of the image.
    image_width = int(size_array[0])
    image_height = int(size_array[1])
    #// Bail early if error/no width.
    if image_width < 1:
        return False
    # end if
    image_basename = wp_basename(image_meta["file"])
    #// 
    #// WordPress flattens animated GIFs into one frame when generating intermediate sizes.
    #// To avoid hiding animation in user content, if src is a full size GIF, a srcset attribute is not generated.
    #// If src is an intermediate size GIF, the full size is excluded from srcset to keep a flattened GIF from becoming animated.
    #//
    if (not (php_isset(lambda : image_sizes["thumbnail"]["mime-type"]))) or "image/gif" != image_sizes["thumbnail"]["mime-type"]:
        image_sizes[-1] = Array({"width": image_meta["width"], "height": image_meta["height"], "file": image_basename})
    elif php_strpos(image_src, image_meta["file"]):
        return False
    # end if
    #// Retrieve the uploads sub-directory from the full size image.
    dirname = _wp_get_attachment_relative_path(image_meta["file"])
    if dirname:
        dirname = trailingslashit(dirname)
    # end if
    upload_dir = wp_get_upload_dir()
    image_baseurl = trailingslashit(upload_dir["baseurl"]) + dirname
    #// 
    #// If currently on HTTPS, prefer HTTPS URLs when we know they're supported by the domain
    #// (which is to say, when they share the domain name of the current request).
    #//
    if is_ssl() and "https" != php_substr(image_baseurl, 0, 5) and php_parse_url(image_baseurl, PHP_URL_HOST) == PHP_SERVER["HTTP_HOST"]:
        image_baseurl = set_url_scheme(image_baseurl, "https")
    # end if
    #// 
    #// Images that have been edited in WordPress after being uploaded will
    #// contain a unique hash. Look for that hash and use it later to filter
    #// out images that are leftovers from previous versions.
    #//
    image_edited = php_preg_match("/-e[0-9]{13}/", wp_basename(image_src), image_edit_hash)
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
    max_srcset_image_width = apply_filters("max_srcset_image_width", 2048, size_array)
    #// Array to hold URL candidates.
    sources = Array()
    #// 
    #// To make sure the ID matches our image src, we will check to see if any sizes in our attachment
    #// meta match our $image_src. If no matches are found we don't return a srcset to avoid serving
    #// an incorrect image. See #35045.
    #//
    src_matched = False
    #// 
    #// Loop through available images. Only use images that are resized
    #// versions of the same edit.
    #//
    for image in image_sizes:
        is_src = False
        #// Check if image meta isn't corrupted.
        if (not php_is_array(image)):
            continue
        # end if
        #// If the file name is part of the `src`, we've confirmed a match.
        if (not src_matched) and False != php_strpos(image_src, dirname + image["file"]):
            src_matched = True
            is_src = True
        # end if
        #// Filter out images that are from previous edits.
        if image_edited and (not php_strpos(image["file"], image_edit_hash[0])):
            continue
        # end if
        #// 
        #// Filters out images that are wider than '$max_srcset_image_width' unless
        #// that file is in the 'src' attribute.
        #//
        if max_srcset_image_width and image["width"] > max_srcset_image_width and (not is_src):
            continue
        # end if
        #// If the image dimensions are within 1px of the expected size, use it.
        if wp_image_matches_ratio(image_width, image_height, image["width"], image["height"]):
            #// Add the URL, descriptor, and value to the sources array to be returned.
            source = Array({"url": image_baseurl + image["file"], "descriptor": "w", "value": image["width"]})
            #// The 'src' image has to be the first in the 'srcset', because of a bug in iOS8. See #35030.
            if is_src:
                sources = Array({image["width"]: source}) + sources
            else:
                sources[image["width"]] = source
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
    sources = apply_filters("wp_calculate_image_srcset", sources, size_array, image_src, image_meta, attachment_id)
    #// Only return a 'srcset' value if there is more than one source.
    if (not src_matched) or (not php_is_array(sources)) or php_count(sources) < 2:
        return False
    # end if
    srcset = ""
    for source in sources:
        srcset += php_str_replace(" ", "%20", source["url"]) + " " + source["value"] + source["descriptor"] + ", "
    # end for
    return php_rtrim(srcset, ", ")
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
def wp_get_attachment_image_sizes(attachment_id=None, size="medium", image_meta=None, *args_):
    
    image = wp_get_attachment_image_src(attachment_id, size)
    if (not image):
        return False
    # end if
    if (not php_is_array(image_meta)):
        image_meta = wp_get_attachment_metadata(attachment_id)
    # end if
    image_src = image[0]
    size_array = Array(absint(image[1]), absint(image[2]))
    return wp_calculate_image_sizes(size_array, image_src, image_meta, attachment_id)
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
def wp_calculate_image_sizes(size=None, image_src=None, image_meta=None, attachment_id=0, *args_):
    
    width = 0
    if php_is_array(size):
        width = absint(size[0])
    elif php_is_string(size):
        if (not image_meta) and attachment_id:
            image_meta = wp_get_attachment_metadata(attachment_id)
        # end if
        if php_is_array(image_meta):
            size_array = _wp_get_image_size_from_meta(size, image_meta)
            if size_array:
                width = absint(size_array[0])
            # end if
        # end if
    # end if
    if (not width):
        return False
    # end if
    #// Setup the default 'sizes' attribute.
    sizes = php_sprintf("(max-width: %1$dpx) 100vw, %1$dpx", width)
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
    return apply_filters("wp_calculate_image_sizes", sizes, size, image_src, image_meta, attachment_id)
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
def wp_make_content_images_responsive(content=None, *args_):
    
    if (not preg_match_all("/<img [^>]+>/", content, matches)):
        return content
    # end if
    selected_images = Array()
    attachment_ids = Array()
    for image in matches[0]:
        if False == php_strpos(image, " srcset=") and php_preg_match("/wp-image-([0-9]+)/i", image, class_id):
            attachment_id = absint(class_id[1])
            if attachment_id:
                #// 
                #// If exactly the same image tag is used more than once, overwrite it.
                #// All identical tags will be replaced later with 'str_replace()'.
                #//
                selected_images[image] = attachment_id
                #// Overwrite the ID when the same image is included more than once.
                attachment_ids[attachment_id] = True
            # end if
        # end if
    # end for
    if php_count(attachment_ids) > 1:
        #// 
        #// Warm the object cache with post and meta information for all found
        #// images to avoid making individual database calls.
        #//
        _prime_post_caches(php_array_keys(attachment_ids), False, True)
    # end if
    for image,attachment_id in selected_images:
        image_meta = wp_get_attachment_metadata(attachment_id)
        content = php_str_replace(image, wp_image_add_srcset_and_sizes(image, image_meta, attachment_id), content)
    # end for
    return content
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
def wp_image_add_srcset_and_sizes(image=None, image_meta=None, attachment_id=None, *args_):
    
    #// Ensure the image meta exists.
    if php_empty(lambda : image_meta["sizes"]):
        return image
    # end if
    image_src = match_src[1] if php_preg_match("/src=\"([^\"]+)\"/", image, match_src) else ""
    image_src = php_explode("?", image_src)
    #// Return early if we couldn't get the image source.
    if (not image_src):
        return image
    # end if
    #// Bail early if an image has been inserted and later edited.
    if php_preg_match("/-e[0-9]{13}/", image_meta["file"], img_edit_hash) and php_strpos(wp_basename(image_src), img_edit_hash[0]) == False:
        return image
    # end if
    width = int(match_width[1]) if php_preg_match("/ width=\"([0-9]+)\"/", image, match_width) else 0
    height = int(match_height[1]) if php_preg_match("/ height=\"([0-9]+)\"/", image, match_height) else 0
    if (not width) or (not height):
        #// 
        #// If attempts to parse the size value failed, attempt to use the image meta data to match
        #// the image file name from 'src' against the available sizes for an attachment.
        #//
        image_filename = wp_basename(image_src)
        if wp_basename(image_meta["file"]) == image_filename:
            width = int(image_meta["width"])
            height = int(image_meta["height"])
        else:
            for image_size_data in image_meta["sizes"]:
                if image_filename == image_size_data["file"]:
                    width = int(image_size_data["width"])
                    height = int(image_size_data["height"])
                    break
                # end if
            # end for
        # end if
    # end if
    if (not width) or (not height):
        return image
    # end if
    size_array = Array(width, height)
    srcset = wp_calculate_image_srcset(size_array, image_src, image_meta, attachment_id)
    if srcset:
        #// Check if there is already a 'sizes' attribute.
        sizes = php_strpos(image, " sizes=")
        if (not sizes):
            sizes = wp_calculate_image_sizes(size_array, image_src, image_meta, attachment_id)
        # end if
    # end if
    if srcset and sizes:
        #// Format the 'srcset' and 'sizes' string and escape attributes.
        attr = php_sprintf(" srcset=\"%s\"", esc_attr(srcset))
        if php_is_string(sizes):
            attr += php_sprintf(" sizes=\"%s\"", esc_attr(sizes))
        # end if
        #// Add 'srcset' and 'sizes' attributes to the image markup.
        image = php_preg_replace("/<img ([^>]+?)[\\/ ]*>/", "<img $1" + attr + " />", image)
    # end if
    return image
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
def _wp_post_thumbnail_class_filter(attr=None, *args_):
    
    attr["class"] += " wp-post-image"
    return attr
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
def _wp_post_thumbnail_class_filter_add(attr=None, *args_):
    
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
def _wp_post_thumbnail_class_filter_remove(attr=None, *args_):
    
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
def img_caption_shortcode(attr=None, content=None, *args_):
    
    #// New-style shortcode with the caption inside the shortcode with the link and image tags.
    if (not (php_isset(lambda : attr["caption"]))):
        if php_preg_match("#((?:<a [^>]+>\\s*)?<img [^>]+>(?:\\s*</a>)?)(.*)#is", content, matches):
            content = matches[1]
            attr["caption"] = php_trim(matches[2])
        # end if
    elif php_strpos(attr["caption"], "<") != False:
        attr["caption"] = wp_kses(attr["caption"], "post")
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
    output = apply_filters("img_caption_shortcode", "", attr, content)
    if (not php_empty(lambda : output)):
        return output
    # end if
    atts = shortcode_atts(Array({"id": "", "caption_id": "", "align": "alignnone", "width": "", "caption": "", "class": ""}), attr, "caption")
    atts["width"] = int(atts["width"])
    if atts["width"] < 1 or php_empty(lambda : atts["caption"]):
        return content
    # end if
    id = ""
    caption_id = ""
    describedby = ""
    if atts["id"]:
        atts["id"] = sanitize_html_class(atts["id"])
        id = "id=\"" + esc_attr(atts["id"]) + "\" "
    # end if
    if atts["caption_id"]:
        atts["caption_id"] = sanitize_html_class(atts["caption_id"])
    elif atts["id"]:
        atts["caption_id"] = "caption-" + php_str_replace("_", "-", atts["id"])
    # end if
    if atts["caption_id"]:
        caption_id = "id=\"" + esc_attr(atts["caption_id"]) + "\" "
        describedby = "aria-describedby=\"" + esc_attr(atts["caption_id"]) + "\" "
    # end if
    class_ = php_trim("wp-caption " + atts["align"] + " " + atts["class"])
    html5 = current_theme_supports("html5", "caption")
    #// HTML5 captions never added the extra 10px to the image width.
    width = atts["width"] if html5 else 10 + atts["width"]
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
    caption_width = apply_filters("img_caption_shortcode_width", width, atts, content)
    style = ""
    if caption_width:
        style = "style=\"width: " + int(caption_width) + "px\" "
    # end if
    if html5:
        html = php_sprintf("<figure %s%s%sclass=\"%s\">%s%s</figure>", id, describedby, style, esc_attr(class_), do_shortcode(content), php_sprintf("<figcaption %sclass=\"wp-caption-text\">%s</figcaption>", caption_id, atts["caption"]))
    else:
        html = php_sprintf("<div %s%sclass=\"%s\">%s%s</div>", id, style, esc_attr(class_), php_str_replace("<img ", "<img " + describedby, do_shortcode(content)), php_sprintf("<p %sclass=\"wp-caption-text\">%s</p>", caption_id, atts["caption"]))
    # end if
    return html
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
def gallery_shortcode(attr=None, *args_):
    
    post = get_post()
    instance = 0
    instance += 1
    if (not php_empty(lambda : attr["ids"])):
        #// 'ids' is explicitly ordered, unless you specify otherwise.
        if php_empty(lambda : attr["orderby"]):
            attr["orderby"] = "post__in"
        # end if
        attr["include"] = attr["ids"]
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
    output = apply_filters("post_gallery", "", attr, instance)
    if (not php_empty(lambda : output)):
        return output
    # end if
    html5 = current_theme_supports("html5", "gallery")
    atts = shortcode_atts(Array({"order": "ASC", "orderby": "menu_order ID", "id": post.ID if post else 0, "itemtag": "figure" if html5 else "dl", "icontag": "div" if html5 else "dt", "captiontag": "figcaption" if html5 else "dd", "columns": 3, "size": "thumbnail", "include": "", "exclude": "", "link": ""}), attr, "gallery")
    id = php_intval(atts["id"])
    if (not php_empty(lambda : atts["include"])):
        _attachments = get_posts(Array({"include": atts["include"], "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": atts["order"], "orderby": atts["orderby"]}))
        attachments = Array()
        for key,val in _attachments:
            attachments[val.ID] = _attachments[key]
        # end for
    elif (not php_empty(lambda : atts["exclude"])):
        attachments = get_children(Array({"post_parent": id, "exclude": atts["exclude"], "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": atts["order"], "orderby": atts["orderby"]}))
    else:
        attachments = get_children(Array({"post_parent": id, "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": atts["order"], "orderby": atts["orderby"]}))
    # end if
    if php_empty(lambda : attachments):
        return ""
    # end if
    if is_feed():
        output = "\n"
        for att_id,attachment in attachments:
            output += wp_get_attachment_link(att_id, atts["size"], True) + "\n"
        # end for
        return output
    # end if
    itemtag = tag_escape(atts["itemtag"])
    captiontag = tag_escape(atts["captiontag"])
    icontag = tag_escape(atts["icontag"])
    valid_tags = wp_kses_allowed_html("post")
    if (not (php_isset(lambda : valid_tags[itemtag]))):
        itemtag = "dl"
    # end if
    if (not (php_isset(lambda : valid_tags[captiontag]))):
        captiontag = "dd"
    # end if
    if (not (php_isset(lambda : valid_tags[icontag]))):
        icontag = "dt"
    # end if
    columns = php_intval(atts["columns"])
    itemwidth = floor(100 / columns) if columns > 0 else 100
    float = "right" if is_rtl() else "left"
    selector = str("gallery-") + str(instance)
    gallery_style = ""
    #// 
    #// Filters whether to print default gallery styles.
    #// 
    #// @since 3.1.0
    #// 
    #// @param bool $print Whether to print default gallery styles.
    #// Defaults to false if the theme supports HTML5 galleries.
    #// Otherwise, defaults to true.
    #//
    if apply_filters("use_default_gallery_style", (not html5)):
        type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
        gallery_style = str("\n     <style") + str(type_attr) + str(">\n            #") + str(selector) + str(""" {\n               margin: auto;\n         }\n         #""") + str(selector) + str(" .gallery-item {\n             float: ") + str(float) + str(""";\n             margin-top: 10px;\n             text-align: center;\n               width: """) + str(itemwidth) + str("%;\n            }\n         #") + str(selector) + str(""" img {\n               border: 2px solid #cfcfcf;\n            }\n         #""") + str(selector) + str(""" .gallery-caption {\n                margin-left: 0;\n           }\n         /* see gallery_shortcode() in wp-includes/media.php */\n        </style>\n      """)
    # end if
    size_class = sanitize_html_class(atts["size"])
    gallery_div = str("<div id='") + str(selector) + str("' class='gallery galleryid-") + str(id) + str(" gallery-columns-") + str(columns) + str(" gallery-size-") + str(size_class) + str("'>")
    #// 
    #// Filters the default gallery shortcode CSS styles.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $gallery_style Default CSS styles and opening HTML div container
    #// for the gallery shortcode output.
    #//
    output = apply_filters("gallery_style", gallery_style + gallery_div)
    i = 0
    for id,attachment in attachments:
        attr = Array({"aria-describedby": str(selector) + str("-") + str(id)}) if php_trim(attachment.post_excerpt) else ""
        if (not php_empty(lambda : atts["link"])) and "file" == atts["link"]:
            image_output = wp_get_attachment_link(id, atts["size"], False, False, False, attr)
        elif (not php_empty(lambda : atts["link"])) and "none" == atts["link"]:
            image_output = wp_get_attachment_image(id, atts["size"], False, attr)
        else:
            image_output = wp_get_attachment_link(id, atts["size"], True, False, False, attr)
        # end if
        image_meta = wp_get_attachment_metadata(id)
        orientation = ""
        if (php_isset(lambda : image_meta["height"]) and php_isset(lambda : image_meta["width"])):
            orientation = "portrait" if image_meta["height"] > image_meta["width"] else "landscape"
        # end if
        output += str("<") + str(itemtag) + str(" class='gallery-item'>")
        output += str("\n           <") + str(icontag) + str(" class='gallery-icon ") + str(orientation) + str("'>\n                ") + str(image_output) + str("\n            </") + str(icontag) + str(">")
        if captiontag and php_trim(attachment.post_excerpt):
            output += str("\n               <") + str(captiontag) + str(" class='wp-caption-text gallery-caption' id='") + str(selector) + str("-") + str(id) + str("'>\n               ") + wptexturize(attachment.post_excerpt) + str("\n             </") + str(captiontag) + str(">")
        # end if
        output += str("</") + str(itemtag) + str(">")
        i += 1
        if (not html5) and columns > 0 and 0 == i % columns:
            output += "<br style=\"clear: both\" />"
        # end if
    # end for
    if (not html5) and columns > 0 and 0 != i % columns:
        output += "\n           <br style='clear: both' />"
    # end if
    output += "\n       </div>\n"
    return output
# end def gallery_shortcode
#// 
#// Outputs the templates used by playlists.
#// 
#// @since 3.9.0
#//
def wp_underscore_playlist_templates(*args_):
    
    php_print("""<script type=\"text/html\" id=\"tmpl-wp-playlist-current-item\">
    <# if ( data.image ) { #>
    <img src=\"{{ data.thumb.src }}\" alt=\"\" />
    <# } #>
    <div class=\"wp-playlist-caption\">
    <span class=\"wp-playlist-item-meta wp-playlist-item-title\">
    """)
    #// translators: %s: Playlist item title.
    printf(_x("&#8220;%s&#8221;", "playlist item title"), "{{ data.title }}")
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
    printf(_x("&#8220;%s&#8221;", "playlist item title"), "{{{ data.title }}}")
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
def wp_playlist_scripts(type=None, *args_):
    
    wp_enqueue_style("wp-mediaelement")
    wp_enqueue_script("wp-playlist")
    php_print("<!--[if lt IE 9]><script>document.createElement('")
    php_print(esc_js(type))
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
def wp_playlist_shortcode(attr=None, *args_):
    
    global content_width
    php_check_if_defined("content_width")
    post = get_post()
    instance = 0
    instance += 1
    if (not php_empty(lambda : attr["ids"])):
        #// 'ids' is explicitly ordered, unless you specify otherwise.
        if php_empty(lambda : attr["orderby"]):
            attr["orderby"] = "post__in"
        # end if
        attr["include"] = attr["ids"]
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
    output = apply_filters("post_playlist", "", attr, instance)
    if (not php_empty(lambda : output)):
        return output
    # end if
    atts = shortcode_atts(Array({"type": "audio", "order": "ASC", "orderby": "menu_order ID", "id": post.ID if post else 0, "include": "", "exclude": "", "style": "light", "tracklist": True, "tracknumbers": True, "images": True, "artists": True}), attr, "playlist")
    id = php_intval(atts["id"])
    if "audio" != atts["type"]:
        atts["type"] = "video"
    # end if
    args = Array({"post_status": "inherit", "post_type": "attachment", "post_mime_type": atts["type"], "order": atts["order"], "orderby": atts["orderby"]})
    if (not php_empty(lambda : atts["include"])):
        args["include"] = atts["include"]
        _attachments = get_posts(args)
        attachments = Array()
        for key,val in _attachments:
            attachments[val.ID] = _attachments[key]
        # end for
    elif (not php_empty(lambda : atts["exclude"])):
        args["post_parent"] = id
        args["exclude"] = atts["exclude"]
        attachments = get_children(args)
    else:
        args["post_parent"] = id
        attachments = get_children(args)
    # end if
    if php_empty(lambda : attachments):
        return ""
    # end if
    if is_feed():
        output = "\n"
        for att_id,attachment in attachments:
            output += wp_get_attachment_link(att_id) + "\n"
        # end for
        return output
    # end if
    outer = 22
    #// Default padding and border of wrapper.
    default_width = 640
    default_height = 360
    theme_width = default_width if php_empty(lambda : content_width) else content_width - outer
    theme_height = default_height if php_empty(lambda : content_width) else round(default_height * theme_width / default_width)
    data = Array({"type": atts["type"], "tracklist": wp_validate_boolean(atts["tracklist"]), "tracknumbers": wp_validate_boolean(atts["tracknumbers"]), "images": wp_validate_boolean(atts["images"]), "artists": wp_validate_boolean(atts["artists"])})
    tracks = Array()
    for attachment in attachments:
        url = wp_get_attachment_url(attachment.ID)
        ftype = wp_check_filetype(url, wp_get_mime_types())
        track = Array({"src": url, "type": ftype["type"], "title": attachment.post_title, "caption": attachment.post_excerpt, "description": attachment.post_content})
        track["meta"] = Array()
        meta = wp_get_attachment_metadata(attachment.ID)
        if (not php_empty(lambda : meta)):
            for key,label in wp_get_attachment_id3_keys(attachment):
                if (not php_empty(lambda : meta[key])):
                    track["meta"][key] = meta[key]
                # end if
            # end for
            if "video" == atts["type"]:
                if (not php_empty(lambda : meta["width"])) and (not php_empty(lambda : meta["height"])):
                    width = meta["width"]
                    height = meta["height"]
                    theme_height = round(height * theme_width / width)
                else:
                    width = default_width
                    height = default_height
                # end if
                track["dimensions"] = Array({"original": compact("width", "height"), "resized": Array({"width": theme_width, "height": theme_height})})
            # end if
        # end if
        if atts["images"]:
            thumb_id = get_post_thumbnail_id(attachment.ID)
            if (not php_empty(lambda : thumb_id)):
                src, width, height = wp_get_attachment_image_src(thumb_id, "full")
                track["image"] = compact("src", "width", "height")
                src, width, height = wp_get_attachment_image_src(thumb_id, "thumbnail")
                track["thumb"] = compact("src", "width", "height")
            else:
                src = wp_mime_type_icon(attachment.ID)
                width = 48
                height = 64
                track["image"] = compact("src", "width", "height")
                track["thumb"] = compact("src", "width", "height")
            # end if
        # end if
        tracks[-1] = track
    # end for
    data["tracks"] = tracks
    safe_type = esc_attr(atts["type"])
    safe_style = esc_attr(atts["style"])
    ob_start()
    if 1 == instance:
        #// 
        #// Prints and enqueues playlist scripts, styles, and JavaScript templates.
        #// 
        #// @since 3.9.0
        #// 
        #// @param string $type  Type of playlist. Possible values are 'audio' or 'video'.
        #// @param string $style The 'theme' for the playlist. Core provides 'light' and 'dark'.
        #//
        do_action("wp_playlist_scripts", atts["type"], atts["style"])
    # end if
    php_print("<div class=\"wp-playlist wp-")
    php_print(safe_type)
    php_print("-playlist wp-playlist-")
    php_print(safe_style)
    php_print("\">\n    ")
    if "audio" == atts["type"]:
        php_print(" <div class=\"wp-playlist-current-item\"></div>\n    ")
    # end if
    php_print(" <")
    php_print(safe_type)
    php_print(" controls=\"controls\" preload=\"none\" width=\"\n               ")
    php_print(int(theme_width))
    php_print(" \"\n    ")
    if "video" == safe_type:
        php_print(" height=\"", int(theme_height), "\"")
    # end if
    php_print(" ></")
    php_print(safe_type)
    php_print(""">
    <div class=\"wp-playlist-next\"></div>
    <div class=\"wp-playlist-prev\"></div>
    <noscript>
    <ol>
    """)
    for att_id,attachment in attachments:
        printf("<li>%s</li>", wp_get_attachment_link(att_id))
    # end for
    php_print(" </ol>\n </noscript>\n   <script type=\"application/json\" class=\"wp-playlist-script\">")
    php_print(wp_json_encode(data))
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
def wp_mediaelement_fallback(url=None, *args_):
    
    #// 
    #// Filters the Mediaelement fallback output for no-JS.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $output Fallback output for no-JS.
    #// @param string $url    Media file URL.
    #//
    return apply_filters("wp_mediaelement_fallback", php_sprintf("<a href=\"%1$s\">%1$s</a>", esc_url(url)), url)
# end def wp_mediaelement_fallback
#// 
#// Returns a filtered list of supported audio formats.
#// 
#// @since 3.6.0
#// 
#// @return string[] Supported audio formats.
#//
def wp_get_audio_extensions(*args_):
    
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
def wp_get_attachment_id3_keys(attachment=None, context="display", *args_):
    
    fields = Array({"artist": __("Artist"), "album": __("Album")})
    if "display" == context:
        fields["genre"] = __("Genre")
        fields["year"] = __("Year")
        fields["length_formatted"] = _x("Length", "video or audio")
    elif "js" == context:
        fields["bitrate"] = __("Bitrate")
        fields["bitrate_mode"] = __("Bitrate Mode")
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
    return apply_filters("wp_get_attachment_id3_keys", fields, attachment, context)
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
def wp_audio_shortcode(attr=None, content="", *args_):
    
    post_id = get_the_ID() if get_post() else 0
    instance = 0
    instance += 1
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
    override = apply_filters("wp_audio_shortcode_override", "", attr, content, instance)
    if "" != override:
        return override
    # end if
    audio = None
    default_types = wp_get_audio_extensions()
    defaults_atts = Array({"src": "", "loop": "", "autoplay": "", "preload": "none", "class": "wp-audio-shortcode", "style": "width: 100%;"})
    for type in default_types:
        defaults_atts[type] = ""
    # end for
    atts = shortcode_atts(defaults_atts, attr, "audio")
    primary = False
    if (not php_empty(lambda : atts["src"])):
        type = wp_check_filetype(atts["src"], wp_get_mime_types())
        if (not php_in_array(php_strtolower(type["ext"]), default_types, True)):
            return php_sprintf("<a class=\"wp-embedded-audio\" href=\"%s\">%s</a>", esc_url(atts["src"]), esc_html(atts["src"]))
        # end if
        primary = True
        array_unshift(default_types, "src")
    else:
        for ext in default_types:
            if (not php_empty(lambda : atts[ext])):
                type = wp_check_filetype(atts[ext], wp_get_mime_types())
                if php_strtolower(type["ext"]) == ext:
                    primary = True
                # end if
            # end if
        # end for
    # end if
    if (not primary):
        audios = get_attached_media("audio", post_id)
        if php_empty(lambda : audios):
            return
        # end if
        audio = reset(audios)
        atts["src"] = wp_get_attachment_url(audio.ID)
        if php_empty(lambda : atts["src"]):
            return
        # end if
        array_unshift(default_types, "src")
    # end if
    #// 
    #// Filters the media library used for the audio shortcode.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $library Media library used for the audio shortcode.
    #//
    library = apply_filters("wp_audio_shortcode_library", "mediaelement")
    if "mediaelement" == library and did_action("init"):
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
    atts["class"] = apply_filters("wp_audio_shortcode_class", atts["class"], atts)
    html_atts = Array({"class": atts["class"], "id": php_sprintf("audio-%d-%d", post_id, instance), "loop": wp_validate_boolean(atts["loop"]), "autoplay": wp_validate_boolean(atts["autoplay"]), "preload": atts["preload"], "style": atts["style"]})
    #// These ones should just be omitted altogether if they are blank.
    for a in Array("loop", "autoplay", "preload"):
        if php_empty(lambda : html_atts[a]):
            html_atts[a] = None
        # end if
    # end for
    attr_strings = Array()
    for k,v in html_atts:
        attr_strings[-1] = k + "=\"" + esc_attr(v) + "\""
    # end for
    html = ""
    if "mediaelement" == library and 1 == instance:
        html += "<!--[if lt IE 9]><script>document.createElement('audio');</script><![endif]-->\n"
    # end if
    html += php_sprintf("<audio %s controls=\"controls\">", join(" ", attr_strings))
    fileurl = ""
    source = "<source type=\"%s\" src=\"%s\" />"
    for fallback in default_types:
        if (not php_empty(lambda : atts[fallback])):
            if php_empty(lambda : fileurl):
                fileurl = atts[fallback]
            # end if
            type = wp_check_filetype(atts[fallback], wp_get_mime_types())
            url = add_query_arg("_", instance, atts[fallback])
            html += php_sprintf(source, type["type"], esc_url(url))
        # end if
    # end for
    if "mediaelement" == library:
        html += wp_mediaelement_fallback(fileurl)
    # end if
    html += "</audio>"
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
    return apply_filters("wp_audio_shortcode", html, atts, audio, post_id, library)
# end def wp_audio_shortcode
add_shortcode("audio", "wp_audio_shortcode")
#// 
#// Returns a filtered list of supported video formats.
#// 
#// @since 3.6.0
#// 
#// @return string[] List of supported video formats.
#//
def wp_get_video_extensions(*args_):
    
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
def wp_video_shortcode(attr=None, content="", *args_):
    
    global content_width
    php_check_if_defined("content_width")
    post_id = get_the_ID() if get_post() else 0
    instance = 0
    instance += 1
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
    override = apply_filters("wp_video_shortcode_override", "", attr, content, instance)
    if "" != override:
        return override
    # end if
    video = None
    default_types = wp_get_video_extensions()
    defaults_atts = Array({"src": "", "poster": "", "loop": "", "autoplay": "", "preload": "metadata", "width": 640, "height": 360, "class": "wp-video-shortcode"})
    for type in default_types:
        defaults_atts[type] = ""
    # end for
    atts = shortcode_atts(defaults_atts, attr, "video")
    if is_admin():
        #// Shrink the video so it isn't huge in the admin.
        if atts["width"] > defaults_atts["width"]:
            atts["height"] = round(atts["height"] * defaults_atts["width"] / atts["width"])
            atts["width"] = defaults_atts["width"]
        # end if
    else:
        #// If the video is bigger than the theme.
        if (not php_empty(lambda : content_width)) and atts["width"] > content_width:
            atts["height"] = round(atts["height"] * content_width / atts["width"])
            atts["width"] = content_width
        # end if
    # end if
    is_vimeo = False
    is_youtube = False
    yt_pattern = "#^https?://(?:www\\.)?(?:youtube\\.com/watch|youtu\\.be/)#"
    vimeo_pattern = "#^https?://(.+\\.)?vimeo\\.com/.*#"
    primary = False
    if (not php_empty(lambda : atts["src"])):
        is_vimeo = php_preg_match(vimeo_pattern, atts["src"])
        is_youtube = php_preg_match(yt_pattern, atts["src"])
        if (not is_youtube) and (not is_vimeo):
            type = wp_check_filetype(atts["src"], wp_get_mime_types())
            if (not php_in_array(php_strtolower(type["ext"]), default_types, True)):
                return php_sprintf("<a class=\"wp-embedded-video\" href=\"%s\">%s</a>", esc_url(atts["src"]), esc_html(atts["src"]))
            # end if
        # end if
        if is_vimeo:
            wp_enqueue_script("mediaelement-vimeo")
        # end if
        primary = True
        array_unshift(default_types, "src")
    else:
        for ext in default_types:
            if (not php_empty(lambda : atts[ext])):
                type = wp_check_filetype(atts[ext], wp_get_mime_types())
                if php_strtolower(type["ext"]) == ext:
                    primary = True
                # end if
            # end if
        # end for
    # end if
    if (not primary):
        videos = get_attached_media("video", post_id)
        if php_empty(lambda : videos):
            return
        # end if
        video = reset(videos)
        atts["src"] = wp_get_attachment_url(video.ID)
        if php_empty(lambda : atts["src"]):
            return
        # end if
        array_unshift(default_types, "src")
    # end if
    #// 
    #// Filters the media library used for the video shortcode.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $library Media library used for the video shortcode.
    #//
    library = apply_filters("wp_video_shortcode_library", "mediaelement")
    if "mediaelement" == library and did_action("init"):
        wp_enqueue_style("wp-mediaelement")
        wp_enqueue_script("wp-mediaelement")
        wp_enqueue_script("mediaelement-vimeo")
    # end if
    #// MediaElement.js has issues with some URL formats for Vimeo and YouTube,
    #// so update the URL to prevent the ME.js player from breaking.
    if "mediaelement" == library:
        if is_youtube:
            #// Remove `feature` query arg and force SSL - see #40866.
            atts["src"] = remove_query_arg("feature", atts["src"])
            atts["src"] = set_url_scheme(atts["src"], "https")
        elif is_vimeo:
            #// Remove all query arguments and force SSL - see #40866.
            parsed_vimeo_url = wp_parse_url(atts["src"])
            vimeo_src = "https://" + parsed_vimeo_url["host"] + parsed_vimeo_url["path"]
            #// Add loop param for mejs bug - see #40977, not needed after #39686.
            loop = "1" if atts["loop"] else "0"
            atts["src"] = add_query_arg("loop", loop, vimeo_src)
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
    atts["class"] = apply_filters("wp_video_shortcode_class", atts["class"], atts)
    html_atts = Array({"class": atts["class"], "id": php_sprintf("video-%d-%d", post_id, instance), "width": absint(atts["width"]), "height": absint(atts["height"]), "poster": esc_url(atts["poster"]), "loop": wp_validate_boolean(atts["loop"]), "autoplay": wp_validate_boolean(atts["autoplay"]), "preload": atts["preload"]})
    #// These ones should just be omitted altogether if they are blank.
    for a in Array("poster", "loop", "autoplay", "preload"):
        if php_empty(lambda : html_atts[a]):
            html_atts[a] = None
        # end if
    # end for
    attr_strings = Array()
    for k,v in html_atts:
        attr_strings[-1] = k + "=\"" + esc_attr(v) + "\""
    # end for
    html = ""
    if "mediaelement" == library and 1 == instance:
        html += "<!--[if lt IE 9]><script>document.createElement('video');</script><![endif]-->\n"
    # end if
    html += php_sprintf("<video %s controls=\"controls\">", join(" ", attr_strings))
    fileurl = ""
    source = "<source type=\"%s\" src=\"%s\" />"
    for fallback in default_types:
        if (not php_empty(lambda : atts[fallback])):
            if php_empty(lambda : fileurl):
                fileurl = atts[fallback]
            # end if
            if "src" == fallback and is_youtube:
                type = Array({"type": "video/youtube"})
            elif "src" == fallback and is_vimeo:
                type = Array({"type": "video/vimeo"})
            else:
                type = wp_check_filetype(atts[fallback], wp_get_mime_types())
            # end if
            url = add_query_arg("_", instance, atts[fallback])
            html += php_sprintf(source, type["type"], esc_url(url))
        # end if
    # end for
    if (not php_empty(lambda : content)):
        if False != php_strpos(content, "\n"):
            content = php_str_replace(Array("\r\n", "\n", " "), "", content)
        # end if
        html += php_trim(content)
    # end if
    if "mediaelement" == library:
        html += wp_mediaelement_fallback(fileurl)
    # end if
    html += "</video>"
    width_rule = ""
    if (not php_empty(lambda : atts["width"])):
        width_rule = php_sprintf("width: %dpx;", atts["width"])
    # end if
    output = php_sprintf("<div style=\"%s\" class=\"wp-video\">%s</div>", width_rule, html)
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
    return apply_filters("wp_video_shortcode", output, atts, video, post_id, library)
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
def previous_image_link(size="thumbnail", text=False, *args_):
    
    adjacent_image_link(True, size, text)
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
def next_image_link(size="thumbnail", text=False, *args_):
    
    adjacent_image_link(False, size, text)
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
def adjacent_image_link(prev=True, size="thumbnail", text=False, *args_):
    
    post = get_post()
    attachments = php_array_values(get_children(Array({"post_parent": post.post_parent, "post_status": "inherit", "post_type": "attachment", "post_mime_type": "image", "order": "ASC", "orderby": "menu_order ID"})))
    for k,attachment in attachments:
        if php_intval(attachment.ID) == php_intval(post.ID):
            break
        # end if
    # end for
    output = ""
    attachment_id = 0
    if attachments:
        k = k - 1 if prev else k + 1
        if (php_isset(lambda : attachments[k])):
            attachment_id = attachments[k].ID
            output = wp_get_attachment_link(attachment_id, size, True, False, text)
        # end if
    # end if
    adjacent = "previous" if prev else "next"
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
    php_print(apply_filters(str(adjacent) + str("_image_link"), output, attachment_id, size, text))
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
def get_attachment_taxonomies(attachment=None, output="names", *args_):
    
    if php_is_int(attachment):
        attachment = get_post(attachment)
    elif php_is_array(attachment):
        attachment = attachment
    # end if
    if (not php_is_object(attachment)):
        return Array()
    # end if
    file = get_attached_file(attachment.ID)
    filename = wp_basename(file)
    objects = Array("attachment")
    if False != php_strpos(filename, "."):
        objects[-1] = "attachment:" + php_substr(filename, php_strrpos(filename, ".") + 1)
    # end if
    if (not php_empty(lambda : attachment.post_mime_type)):
        objects[-1] = "attachment:" + attachment.post_mime_type
        if False != php_strpos(attachment.post_mime_type, "/"):
            for token in php_explode("/", attachment.post_mime_type):
                if (not php_empty(lambda : token)):
                    objects[-1] = str("attachment:") + str(token)
                # end if
            # end for
        # end if
    # end if
    taxonomies = Array()
    for object in objects:
        taxes = get_object_taxonomies(object, output)
        if taxes:
            taxonomies = php_array_merge(taxonomies, taxes)
        # end if
    # end for
    if "names" == output:
        taxonomies = array_unique(taxonomies)
    # end if
    return taxonomies
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
def get_taxonomies_for_attachments(output="names", *args_):
    
    taxonomies = Array()
    for taxonomy in get_taxonomies(Array(), "objects"):
        for object_type in taxonomy.object_type:
            if "attachment" == object_type or 0 == php_strpos(object_type, "attachment:"):
                if "names" == output:
                    taxonomies[-1] = taxonomy.name
                else:
                    taxonomies[taxonomy.name] = taxonomy
                # end if
                break
            # end if
        # end for
    # end for
    return taxonomies
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
def wp_imagecreatetruecolor(width=None, height=None, *args_):
    
    img = imagecreatetruecolor(width, height)
    if is_resource(img) and php_function_exists("imagealphablending") and php_function_exists("imagesavealpha"):
        imagealphablending(img, False)
        imagesavealpha(img, True)
    # end if
    return img
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
def wp_expand_dimensions(example_width=None, example_height=None, max_width=None, max_height=None, *args_):
    
    example_width = int(example_width)
    example_height = int(example_height)
    max_width = int(max_width)
    max_height = int(max_height)
    return wp_constrain_dimensions(example_width * 1000000, example_height * 1000000, max_width, max_height)
# end def wp_expand_dimensions
#// 
#// Determines the maximum upload size allowed in php.ini.
#// 
#// @since 2.5.0
#// 
#// @return int Allowed upload size.
#//
def wp_max_upload_size(*args_):
    
    u_bytes = wp_convert_hr_to_bytes(php_ini_get("upload_max_filesize"))
    p_bytes = wp_convert_hr_to_bytes(php_ini_get("post_max_size"))
    #// 
    #// Filters the maximum upload size allowed in php.ini.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int $size    Max upload size limit in bytes.
    #// @param int $u_bytes Maximum upload filesize in bytes.
    #// @param int $p_bytes Maximum size of POST data in bytes.
    #//
    return apply_filters("upload_size_limit", php_min(u_bytes, p_bytes), u_bytes, p_bytes)
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
def wp_get_image_editor(path=None, args=Array(), *args_):
    
    args["path"] = path
    if (not (php_isset(lambda : args["mime_type"]))):
        file_info = wp_check_filetype(args["path"])
        #// If $file_info['type'] is false, then we let the editor attempt to
        #// figure out the file type, rather than forcing a failure based on extension.
        if (php_isset(lambda : file_info)) and file_info["type"]:
            args["mime_type"] = file_info["type"]
        # end if
    # end if
    implementation = _wp_image_editor_choose(args)
    if implementation:
        editor = php_new_class(implementation, lambda : {**locals(), **globals()}[implementation](path))
        loaded = editor.load()
        if is_wp_error(loaded):
            return loaded
        # end if
        return editor
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
def wp_image_editor_supports(args=Array(), *args_):
    
    return bool(_wp_image_editor_choose(args))
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
def _wp_image_editor_choose(args=Array(), *args_):
    
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
    implementations = apply_filters("wp_image_editors", Array("WP_Image_Editor_Imagick", "WP_Image_Editor_GD"))
    for implementation in implementations:
        if (not php_call_user_func(Array(implementation, "test"), args)):
            continue
        # end if
        if (php_isset(lambda : args["mime_type"])) and (not php_call_user_func(Array(implementation, "supports_mime_type"), args["mime_type"])):
            continue
        # end if
        if (php_isset(lambda : args["methods"])) and php_array_diff(args["methods"], get_class_methods(implementation)):
            continue
        # end if
        return implementation
    # end for
    return False
# end def _wp_image_editor_choose
#// 
#// Prints default Plupload arguments.
#// 
#// @since 3.4.0
#//
def wp_plupload_default_settings(*args_):
    
    wp_scripts = wp_scripts()
    data = wp_scripts.get_data("wp-plupload", "data")
    if data and False != php_strpos(data, "_wpPluploadSettings"):
        return
    # end if
    max_upload_size = wp_max_upload_size()
    allowed_extensions = php_array_keys(get_allowed_mime_types())
    extensions = Array()
    for extension in allowed_extensions:
        extensions = php_array_merge(extensions, php_explode("|", extension))
    # end for
    #// 
    #// Since 4.9 the `runtimes` setting is hardcoded in our version of Plupload to `html5,html4`,
    #// and the `flash_swf_url` and `silverlight_xap_url` are not used.
    #//
    defaults = Array({"file_data_name": "async-upload", "url": admin_url("async-upload.php", "relative"), "filters": Array({"max_file_size": max_upload_size + "b", "mime_types": Array(Array({"extensions": php_implode(",", extensions)}))})})
    #// 
    #// Currently only iOS Safari supports multiple files uploading,
    #// but iOS 7.x has a bug that prevents uploading of videos when enabled.
    #// See #29602.
    #//
    if wp_is_mobile() and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "OS 7_") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "like Mac OS X") != False:
        defaults["multi_selection"] = False
    # end if
    #// 
    #// Filters the Plupload default settings.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $defaults Default Plupload settings array.
    #//
    defaults = apply_filters("plupload_default_settings", defaults)
    params = Array({"action": "upload-attachment"})
    #// 
    #// Filters the Plupload default parameters.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $params Default Plupload parameters array.
    #//
    params = apply_filters("plupload_default_params", params)
    params["_wpnonce"] = wp_create_nonce("media-form")
    defaults["multipart_params"] = params
    settings = Array({"defaults": defaults, "browser": Array({"mobile": wp_is_mobile(), "supported": _device_can_upload()})}, {"limitExceeded": is_multisite() and (not is_upload_space_available())})
    script = "var _wpPluploadSettings = " + wp_json_encode(settings) + ";"
    if data:
        script = str(data) + str("\n") + str(script)
    # end if
    wp_scripts.add_data("wp-plupload", "data", script)
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
def wp_prepare_attachment_for_js(attachment=None, *args_):
    
    attachment = get_post(attachment)
    if (not attachment):
        return
    # end if
    if "attachment" != attachment.post_type:
        return
    # end if
    meta = wp_get_attachment_metadata(attachment.ID)
    if False != php_strpos(attachment.post_mime_type, "/"):
        type, subtype = php_explode("/", attachment.post_mime_type)
    else:
        type, subtype = Array(attachment.post_mime_type, "")
    # end if
    attachment_url = wp_get_attachment_url(attachment.ID)
    base_url = php_str_replace(wp_basename(attachment_url), "", attachment_url)
    response = Array({"id": attachment.ID, "title": attachment.post_title, "filename": wp_basename(get_attached_file(attachment.ID)), "url": attachment_url, "link": get_attachment_link(attachment.ID), "alt": get_post_meta(attachment.ID, "_wp_attachment_image_alt", True), "author": attachment.post_author, "description": attachment.post_content, "caption": attachment.post_excerpt, "name": attachment.post_name, "status": attachment.post_status, "uploadedTo": attachment.post_parent, "date": strtotime(attachment.post_date_gmt) * 1000, "modified": strtotime(attachment.post_modified_gmt) * 1000, "menuOrder": attachment.menu_order, "mime": attachment.post_mime_type, "type": type, "subtype": subtype, "icon": wp_mime_type_icon(attachment.ID), "dateFormatted": mysql2date(__("F j, Y"), attachment.post_date), "nonces": Array({"update": False, "delete": False, "edit": False})}, {"editLink": False, "meta": False})
    author = php_new_class("WP_User", lambda : WP_User(attachment.post_author))
    if author.exists():
        response["authorName"] = html_entity_decode(author.display_name, ENT_QUOTES, get_bloginfo("charset"))
    else:
        response["authorName"] = __("(no author)")
    # end if
    if attachment.post_parent:
        post_parent = get_post(attachment.post_parent)
    else:
        post_parent = False
    # end if
    if post_parent:
        parent_type = get_post_type_object(post_parent.post_type)
        if parent_type and parent_type.show_ui and current_user_can("edit_post", attachment.post_parent):
            response["uploadedToLink"] = get_edit_post_link(attachment.post_parent, "raw")
        # end if
        if parent_type and current_user_can("read_post", attachment.post_parent):
            response["uploadedToTitle"] = post_parent.post_title if post_parent.post_title else __("(no title)")
        # end if
    # end if
    attached_file = get_attached_file(attachment.ID)
    if (php_isset(lambda : meta["filesize"])):
        bytes = meta["filesize"]
    elif php_file_exists(attached_file):
        bytes = filesize(attached_file)
    else:
        bytes = ""
    # end if
    if bytes:
        response["filesizeInBytes"] = bytes
        response["filesizeHumanReadable"] = size_format(bytes)
    # end if
    context = get_post_meta(attachment.ID, "_wp_attachment_context", True)
    response["context"] = context if context else ""
    if current_user_can("edit_post", attachment.ID):
        response["nonces"]["update"] = wp_create_nonce("update-post_" + attachment.ID)
        response["nonces"]["edit"] = wp_create_nonce("image_editor-" + attachment.ID)
        response["editLink"] = get_edit_post_link(attachment.ID, "raw")
    # end if
    if current_user_can("delete_post", attachment.ID):
        response["nonces"]["delete"] = wp_create_nonce("delete-post_" + attachment.ID)
    # end if
    if meta and "image" == type or (not php_empty(lambda : meta["sizes"])):
        sizes = Array()
        #// This filter is documented in wp-admin/includes/media.php
        possible_sizes = apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")}))
        possible_sizes["full"] = None
        #// 
        #// Loop through all potential sizes that may be chosen. Try to do this with some efficiency.
        #// First: run the image_downsize filter. If it returns something, we can use its data.
        #// If the filter does not return something, then image_downsize() is just an expensive way
        #// to check the image metadata, which we do second.
        #//
        for size,label in possible_sizes:
            #// This filter is documented in wp-includes/media.php
            downsize = apply_filters("image_downsize", False, attachment.ID, size)
            if downsize:
                if php_empty(lambda : downsize[3]):
                    continue
                # end if
                sizes[size] = Array({"height": downsize[2], "width": downsize[1], "url": downsize[0], "orientation": "portrait" if downsize[2] > downsize[1] else "landscape"})
            elif (php_isset(lambda : meta["sizes"][size])):
                #// Nothing from the filter, so consult image metadata if we have it.
                size_meta = meta["sizes"][size]
                #// We have the actual image size, but might need to further constrain it if content_width is narrower.
                #// Thumbnail, medium, and full sizes are also checked against the site's height/width options.
                width, height = image_constrain_size_for_editor(size_meta["width"], size_meta["height"], size, "edit")
                sizes[size] = Array({"height": height, "width": width, "url": base_url + size_meta["file"], "orientation": "portrait" if height > width else "landscape"})
            # end if
        # end for
        if "image" == type:
            if (not php_empty(lambda : meta["original_image"])):
                response["originalImageURL"] = wp_get_original_image_url(attachment.ID)
                response["originalImageName"] = wp_basename(wp_get_original_image_path(attachment.ID))
            # end if
            sizes["full"] = Array({"url": attachment_url})
            if (php_isset(lambda : meta["height"]) and php_isset(lambda : meta["width"])):
                sizes["full"]["height"] = meta["height"]
                sizes["full"]["width"] = meta["width"]
                sizes["full"]["orientation"] = "portrait" if meta["height"] > meta["width"] else "landscape"
            # end if
            response = php_array_merge(response, sizes["full"])
        elif meta["sizes"]["full"]["file"]:
            sizes["full"] = Array({"url": base_url + meta["sizes"]["full"]["file"], "height": meta["sizes"]["full"]["height"], "width": meta["sizes"]["full"]["width"], "orientation": "portrait" if meta["sizes"]["full"]["height"] > meta["sizes"]["full"]["width"] else "landscape"})
        # end if
        response = php_array_merge(response, Array({"sizes": sizes}))
    # end if
    if meta and "video" == type:
        if (php_isset(lambda : meta["width"])):
            response["width"] = int(meta["width"])
        # end if
        if (php_isset(lambda : meta["height"])):
            response["height"] = int(meta["height"])
        # end if
    # end if
    if meta and "audio" == type or "video" == type:
        if (php_isset(lambda : meta["length_formatted"])):
            response["fileLength"] = meta["length_formatted"]
            response["fileLengthHumanReadable"] = human_readable_duration(meta["length_formatted"])
        # end if
        response["meta"] = Array()
        for key,label in wp_get_attachment_id3_keys(attachment, "js"):
            response["meta"][key] = False
            if (not php_empty(lambda : meta[key])):
                response["meta"][key] = meta[key]
            # end if
        # end for
        id = get_post_thumbnail_id(attachment.ID)
        if (not php_empty(lambda : id)):
            src, width, height = wp_get_attachment_image_src(id, "full")
            response["image"] = compact("src", "width", "height")
            src, width, height = wp_get_attachment_image_src(id, "thumbnail")
            response["thumb"] = compact("src", "width", "height")
        else:
            src = wp_mime_type_icon(attachment.ID)
            width = 48
            height = 64
            response["image"] = compact("src", "width", "height")
            response["thumb"] = compact("src", "width", "height")
        # end if
    # end if
    if php_function_exists("get_compat_media_markup"):
        response["compat"] = get_compat_media_markup(attachment.ID, Array({"in_modal": True}))
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
    return apply_filters("wp_prepare_attachment_for_js", response, attachment, meta)
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
def wp_enqueue_media(args=Array(), *args_):
    
    #// Enqueue me just once per page, please.
    if did_action("wp_enqueue_media"):
        return
    # end if
    global content_width,wpdb,wp_locale
    php_check_if_defined("content_width","wpdb","wp_locale")
    defaults = Array({"post": None})
    args = wp_parse_args(args, defaults)
    #// We're going to pass the old thickbox media tabs to `media_upload_tabs`
    #// to ensure plugins will work. We will then unset those tabs.
    tabs = Array({"type": "", "type_url": "", "gallery": "", "library": ""})
    #// This filter is documented in wp-admin/includes/media.php
    tabs = apply_filters("media_upload_tabs", tabs)
    tabs["type"] = None
    tabs["type_url"] = None
    tabs["gallery"] = None
    tabs["library"] = None
    props = Array({"link": get_option("image_default_link_type"), "align": get_option("image_default_align"), "size": get_option("image_default_size")})
    exts = php_array_merge(wp_get_audio_extensions(), wp_get_video_extensions())
    mimes = get_allowed_mime_types()
    ext_mimes = Array()
    for ext in exts:
        for ext_preg,mime_match in mimes:
            if php_preg_match("#" + ext + "#i", ext_preg):
                ext_mimes[ext] = mime_match
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
    show_audio_playlist = apply_filters("media_library_show_audio_playlist", True)
    if None == show_audio_playlist:
        show_audio_playlist = wpdb.get_var(str("\n          SELECT ID\n         FROM ") + str(wpdb.posts) + str("""\n           WHERE post_type = 'attachment'\n            AND post_mime_type LIKE 'audio%'\n          LIMIT 1\n       """))
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
    show_video_playlist = apply_filters("media_library_show_video_playlist", True)
    if None == show_video_playlist:
        show_video_playlist = wpdb.get_var(str("\n          SELECT ID\n         FROM ") + str(wpdb.posts) + str("""\n           WHERE post_type = 'attachment'\n            AND post_mime_type LIKE 'video%'\n          LIMIT 1\n       """))
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
    months = apply_filters("media_library_months_with_files", None)
    if (not php_is_array(months)):
        months = wpdb.get_results(wpdb.prepare(str("\n          SELECT DISTINCT YEAR( post_date ) AS year, MONTH( post_date ) AS month\n            FROM ") + str(wpdb.posts) + str("""\n           WHERE post_type = %s\n          ORDER BY post_date DESC\n       """), "attachment"))
    # end if
    for month_year in months:
        month_year.text = php_sprintf(__("%1$s %2$d"), wp_locale.get_month(month_year.month), month_year.year)
    # end for
    settings = Array({"tabs": tabs, "tabUrl": add_query_arg(Array({"chromeless": True}), admin_url("media-upload.php"))}, {"mimeTypes": wp_list_pluck(get_post_mime_types(), 0), "captions": (not apply_filters("disable_captions", "")), "nonce": Array({"sendToEditor": wp_create_nonce("media-send-to-editor")})}, {"post": Array({"id": 0})}, {"defaultProps": props, "attachmentCounts": Array({"audio": 1 if show_audio_playlist else 0, "video": 1 if show_video_playlist else 0})}, {"oEmbedProxyUrl": rest_url("oembed/1.0/proxy"), "embedExts": exts, "embedMimes": ext_mimes, "contentWidth": content_width, "months": months, "mediaTrash": 1 if MEDIA_TRASH else 0})
    post = None
    if (php_isset(lambda : args["post"])):
        post = get_post(args["post"])
        settings["post"] = Array({"id": post.ID, "nonce": wp_create_nonce("update-post_" + post.ID)})
        thumbnail_support = current_theme_supports("post-thumbnails", post.post_type) and post_type_supports(post.post_type, "thumbnail")
        if (not thumbnail_support) and "attachment" == post.post_type and post.post_mime_type:
            if wp_attachment_is("audio", post):
                thumbnail_support = post_type_supports("attachment:audio", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:audio")
            elif wp_attachment_is("video", post):
                thumbnail_support = post_type_supports("attachment:video", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:video")
            # end if
        # end if
        if thumbnail_support:
            featured_image_id = get_post_meta(post.ID, "_thumbnail_id", True)
            settings["post"]["featuredImageId"] = featured_image_id if featured_image_id else -1
        # end if
    # end if
    if post:
        post_type_object = get_post_type_object(post.post_type)
    else:
        post_type_object = get_post_type_object("post")
    # end if
    strings = Array({"mediaFrameDefaultTitle": __("Media"), "url": __("URL"), "addMedia": __("Add Media"), "search": __("Search"), "select": __("Select"), "cancel": __("Cancel"), "update": __("Update"), "replace": __("Replace"), "remove": __("Remove"), "back": __("Back"), "selected": __("%d selected"), "dragInfo": __("Drag and drop to reorder media files."), "uploadFilesTitle": __("Upload Files"), "uploadImagesTitle": __("Upload Images"), "mediaLibraryTitle": __("Media Library"), "insertMediaTitle": __("Add Media"), "createNewGallery": __("Create a new gallery"), "createNewPlaylist": __("Create a new playlist"), "createNewVideoPlaylist": __("Create a new video playlist"), "returnToLibrary": __("&#8592; Return to library"), "allMediaItems": __("All media items"), "allDates": __("All dates"), "noItemsFound": __("No items found."), "insertIntoPost": post_type_object.labels.insert_into_item, "unattached": __("Unattached"), "mine": _x("Mine", "media items"), "trash": _x("Trash", "noun"), "uploadedToThisPost": post_type_object.labels.uploaded_to_this_item, "warnDelete": __("You are about to permanently delete this item from your site.\nThis action cannot be undone.\n 'Cancel' to stop, 'OK' to delete."), "warnBulkDelete": __("You are about to permanently delete these items from your site.\nThis action cannot be undone.\n 'Cancel' to stop, 'OK' to delete."), "warnBulkTrash": __("You are about to trash these items.\n  'Cancel' to stop, 'OK' to delete."), "bulkSelect": __("Bulk Select"), "trashSelected": __("Move to Trash"), "restoreSelected": __("Restore from Trash"), "deletePermanently": __("Delete Permanently"), "apply": __("Apply"), "filterByDate": __("Filter by date"), "filterByType": __("Filter by type"), "searchLabel": __("Search"), "searchMediaLabel": __("Search Media"), "searchMediaPlaceholder": __("Search media items..."), "mediaFound": __("Number of media items found: %d"), "mediaFoundHasMoreResults": __("Number of media items displayed: %d. Scroll the page for more results."), "noMedia": __("No media items found."), "noMediaTryNewSearch": __("No media items found. Try a different search."), "attachmentDetails": __("Attachment Details"), "insertFromUrlTitle": __("Insert from URL"), "setFeaturedImageTitle": post_type_object.labels.featured_image, "setFeaturedImage": post_type_object.labels.set_featured_image, "createGalleryTitle": __("Create Gallery"), "editGalleryTitle": __("Edit Gallery"), "cancelGalleryTitle": __("&#8592; Cancel Gallery"), "insertGallery": __("Insert gallery"), "updateGallery": __("Update gallery"), "addToGallery": __("Add to gallery"), "addToGalleryTitle": __("Add to Gallery"), "reverseOrder": __("Reverse order"), "imageDetailsTitle": __("Image Details"), "imageReplaceTitle": __("Replace Image"), "imageDetailsCancel": __("Cancel Edit"), "editImage": __("Edit Image"), "chooseImage": __("Choose Image"), "selectAndCrop": __("Select and Crop"), "skipCropping": __("Skip Cropping"), "cropImage": __("Crop Image"), "cropYourImage": __("Crop your image"), "cropping": __("Cropping&hellip;"), "suggestedDimensions": __("Suggested image dimensions: %1$s by %2$s pixels."), "cropError": __("There has been an error cropping your image."), "audioDetailsTitle": __("Audio Details"), "audioReplaceTitle": __("Replace Audio"), "audioAddSourceTitle": __("Add Audio Source"), "audioDetailsCancel": __("Cancel Edit"), "videoDetailsTitle": __("Video Details"), "videoReplaceTitle": __("Replace Video"), "videoAddSourceTitle": __("Add Video Source"), "videoDetailsCancel": __("Cancel Edit"), "videoSelectPosterImageTitle": __("Select Poster Image"), "videoAddTrackTitle": __("Add Subtitles"), "playlistDragInfo": __("Drag and drop to reorder tracks."), "createPlaylistTitle": __("Create Audio Playlist"), "editPlaylistTitle": __("Edit Audio Playlist"), "cancelPlaylistTitle": __("&#8592; Cancel Audio Playlist"), "insertPlaylist": __("Insert audio playlist"), "updatePlaylist": __("Update audio playlist"), "addToPlaylist": __("Add to audio playlist"), "addToPlaylistTitle": __("Add to Audio Playlist"), "videoPlaylistDragInfo": __("Drag and drop to reorder videos."), "createVideoPlaylistTitle": __("Create Video Playlist"), "editVideoPlaylistTitle": __("Edit Video Playlist"), "cancelVideoPlaylistTitle": __("&#8592; Cancel Video Playlist"), "insertVideoPlaylist": __("Insert video playlist"), "updateVideoPlaylist": __("Update video playlist"), "addToVideoPlaylist": __("Add to video playlist"), "addToVideoPlaylistTitle": __("Add to Video Playlist"), "filterAttachments": __("Filter Media"), "attachmentsList": __("Media list")})
    #// 
    #// Filters the media view settings.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array   $settings List of media view settings.
    #// @param WP_Post $post     Post object.
    #//
    settings = apply_filters("media_view_settings", settings, post)
    #// 
    #// Filters the media view strings.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string[] $strings Array of media view strings keyed by the name they'll be referenced by in JavaScript.
    #// @param WP_Post  $post    Post object.
    #//
    strings = apply_filters("media_view_strings", strings, post)
    strings["settings"] = settings
    #// Ensure we enqueue media-editor first, that way media-views
    #// is registered internally before we try to localize it. See #24724.
    wp_enqueue_script("media-editor")
    wp_localize_script("media-views", "_wpMediaViewsL10n", strings)
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
def get_attached_media(type=None, post=0, *args_):
    
    post = get_post(post)
    if (not post):
        return Array()
    # end if
    args = Array({"post_parent": post.ID, "post_type": "attachment", "post_mime_type": type, "posts_per_page": -1, "orderby": "menu_order", "order": "ASC"})
    #// 
    #// Filters arguments used to retrieve media attached to the given post.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array   $args Post query arguments.
    #// @param string  $type Mime type of the desired media.
    #// @param WP_Post $post Post object.
    #//
    args = apply_filters("get_attached_media_args", args, type, post)
    children = get_children(args)
    #// 
    #// Filters the list of media attached to the given post.
    #// 
    #// @since 3.6.0
    #// 
    #// @param WP_Post[] $children Array of media attached to the given post.
    #// @param string    $type     Mime type of the media desired.
    #// @param WP_Post   $post     Post object.
    #//
    return apply_filters("get_attached_media", children, type, post)
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
def get_media_embedded_in_content(content=None, types=None, *args_):
    
    html = Array()
    #// 
    #// Filters the embedded media types that are allowed to be returned from the content blob.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string[] $allowed_media_types An array of allowed media types. Default media types are
    #// 'audio', 'video', 'object', 'embed', and 'iframe'.
    #//
    allowed_media_types = apply_filters("media_embedded_in_content_allowed_types", Array("audio", "video", "object", "embed", "iframe"))
    if (not php_empty(lambda : types)):
        if (not php_is_array(types)):
            types = Array(types)
        # end if
        allowed_media_types = php_array_intersect(allowed_media_types, types)
    # end if
    tags = php_implode("|", allowed_media_types)
    if preg_match_all("#<(?P<tag>" + tags + ")[^<]*?(?:>[\\s\\S]*?<\\/(?P=tag)>|\\s*\\/>)#", content, matches):
        for match in matches[0]:
            html[-1] = match
        # end for
    # end if
    return html
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
def get_post_galleries(post=None, html=True, *args_):
    
    post = get_post(post)
    if (not post):
        return Array()
    # end if
    if (not has_shortcode(post.post_content, "gallery")):
        return Array()
    # end if
    galleries = Array()
    if preg_match_all("/" + get_shortcode_regex() + "/s", post.post_content, matches, PREG_SET_ORDER):
        for shortcode in matches:
            if "gallery" == shortcode[2]:
                srcs = Array()
                shortcode_attrs = shortcode_parse_atts(shortcode[3])
                if (not php_is_array(shortcode_attrs)):
                    shortcode_attrs = Array()
                # end if
                #// Specify the post id of the gallery we're viewing if the shortcode doesn't reference another post already.
                if (not (php_isset(lambda : shortcode_attrs["id"]))):
                    shortcode[3] += " id=\"" + php_intval(post.ID) + "\""
                # end if
                gallery = do_shortcode_tag(shortcode)
                if html:
                    galleries[-1] = gallery
                else:
                    preg_match_all("#src=(['\"])(.+?)\\1#is", gallery, src, PREG_SET_ORDER)
                    if (not php_empty(lambda : src)):
                        for s in src:
                            srcs[-1] = s[2]
                        # end for
                    # end if
                    galleries[-1] = php_array_merge(shortcode_attrs, Array({"src": php_array_values(array_unique(srcs))}))
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
    return apply_filters("get_post_galleries", galleries, post)
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
def get_post_gallery(post=0, html=True, *args_):
    
    galleries = get_post_galleries(post, html)
    gallery = reset(galleries)
    #// 
    #// Filters the first-found post gallery.
    #// 
    #// @since 3.6.0
    #// 
    #// @param array       $gallery   The first-found post gallery.
    #// @param int|WP_Post $post      Post ID or object.
    #// @param array       $galleries Associative array of all found post galleries.
    #//
    return apply_filters("get_post_gallery", gallery, post, galleries)
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
def get_post_galleries_images(post=0, *args_):
    
    galleries = get_post_galleries(post, False)
    return wp_list_pluck(galleries, "src")
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
def get_post_gallery_images(post=0, *args_):
    
    gallery = get_post_gallery(post, False)
    return Array() if php_empty(lambda : gallery["src"]) else gallery["src"]
# end def get_post_gallery_images
#// 
#// Maybe attempts to generate attachment metadata, if missing.
#// 
#// @since 3.9.0
#// 
#// @param WP_Post $attachment Attachment object.
#//
def wp_maybe_generate_attachment_metadata(attachment=None, *args_):
    
    if php_empty(lambda : attachment) or php_empty(lambda : attachment.ID):
        return
    # end if
    attachment_id = int(attachment.ID)
    file = get_attached_file(attachment_id)
    meta = wp_get_attachment_metadata(attachment_id)
    if php_empty(lambda : meta) and php_file_exists(file):
        _meta = get_post_meta(attachment_id)
        _lock = "wp_generating_att_" + attachment_id
        if (not php_array_key_exists("_wp_attachment_metadata", _meta)) and (not get_transient(_lock)):
            set_transient(_lock, file)
            wp_update_attachment_metadata(attachment_id, wp_generate_attachment_metadata(attachment_id, file))
            delete_transient(_lock)
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
def attachment_url_to_postid(url=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    dir = wp_get_upload_dir()
    path = url
    site_url = php_parse_url(dir["url"])
    image_path = php_parse_url(path)
    #// Force the protocols to match if needed.
    if (php_isset(lambda : image_path["scheme"])) and image_path["scheme"] != site_url["scheme"]:
        path = php_str_replace(image_path["scheme"], site_url["scheme"], path)
    # end if
    if 0 == php_strpos(path, dir["baseurl"] + "/"):
        path = php_substr(path, php_strlen(dir["baseurl"] + "/"))
    # end if
    sql = wpdb.prepare(str("SELECT post_id, meta_value FROM ") + str(wpdb.postmeta) + str(" WHERE meta_key = '_wp_attached_file' AND meta_value = %s"), path)
    results = wpdb.get_results(sql)
    post_id = None
    if results:
        #// Use the first available result, but prefer a case-sensitive match, if exists.
        post_id = reset(results).post_id
        if php_count(results) > 1:
            for result in results:
                if path == result.meta_value:
                    post_id = result.post_id
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
    return int(apply_filters("attachment_url_to_postid", post_id, url))
# end def attachment_url_to_postid
#// 
#// Returns the URLs for CSS files used in an iframe-sandbox'd TinyMCE media view.
#// 
#// @since 4.0.0
#// 
#// @return string[] The relevant CSS file URLs.
#//
def wpview_media_sandbox_styles(*args_):
    
    version = "ver=" + get_bloginfo("version")
    mediaelement = includes_url(str("js/mediaelement/mediaelementplayer-legacy.min.css?") + str(version))
    wpmediaelement = includes_url(str("js/mediaelement/wp-mediaelement.css?") + str(version))
    return Array(mediaelement, wpmediaelement)
# end def wpview_media_sandbox_styles
#// 
#// Registers the personal data exporter for media.
#// 
#// @param array[] $exporters An array of personal data exporters, keyed by their ID.
#// @return array[] Updated array of personal data exporters.
#//
def wp_register_media_personal_data_exporter(exporters=None, *args_):
    
    exporters["wordpress-media"] = Array({"exporter_friendly_name": __("WordPress Media"), "callback": "wp_media_personal_data_exporter"})
    return exporters
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
def wp_media_personal_data_exporter(email_address=None, page=1, *args_):
    
    #// Limit us to 50 attachments at a time to avoid timing out.
    number = 50
    page = int(page)
    data_to_export = Array()
    user = get_user_by("email", email_address)
    if False == user:
        return Array({"data": data_to_export, "done": True})
    # end if
    post_query = php_new_class("WP_Query", lambda : WP_Query(Array({"author": user.ID, "posts_per_page": number, "paged": page, "post_type": "attachment", "post_status": "any", "orderby": "ID", "order": "ASC"})))
    for post in post_query.posts:
        attachment_url = wp_get_attachment_url(post.ID)
        if attachment_url:
            post_data_to_export = Array(Array({"name": __("URL"), "value": attachment_url}))
            data_to_export[-1] = Array({"group_id": "media", "group_label": __("Media"), "group_description": __("User&#8217;s media data."), "item_id": str("post-") + str(post.ID), "data": post_data_to_export})
        # end if
    # end for
    done = post_query.max_num_pages <= page
    return Array({"data": data_to_export, "done": done})
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
def _wp_add_additional_image_sizes(*args_):
    
    #// 2x medium_large size.
    add_image_size("1536x1536", 1536, 1536)
    #// 2x large size.
    add_image_size("2048x2048", 2048, 2048)
# end def _wp_add_additional_image_sizes
