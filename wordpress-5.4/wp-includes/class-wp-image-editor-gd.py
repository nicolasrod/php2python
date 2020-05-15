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
#// WordPress GD Image Editor
#// 
#// @package WordPress
#// @subpackage Image_Editor
#// 
#// 
#// WordPress Image Editor Class for Image Manipulation through GD
#// 
#// @since 3.5.0
#// 
#// @see WP_Image_Editor
#//
class WP_Image_Editor_GD(WP_Image_Editor):
    image = Array()
    def __del__(self):
        
        if self.image:
            #// We don't need the original in memory anymore.
            imagedestroy(self.image)
        # end if
    # end def __del__
    #// 
    #// Checks to see if current environment supports GD.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array $args
    #// @return bool
    #//
    @classmethod
    def test(self, args=Array()):
        
        if (not php_extension_loaded("gd")) or (not php_function_exists("gd_info")):
            return False
        # end if
        #// On some setups GD library does not provide imagerotate() - Ticket #11536.
        if (php_isset(lambda : args["methods"])) and php_in_array("rotate", args["methods"], True) and (not php_function_exists("imagerotate")):
            return False
        # end if
        return True
    # end def test
    #// 
    #// Checks to see if editor supports the mime-type specified.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $mime_type
    #// @return bool
    #//
    @classmethod
    def supports_mime_type(self, mime_type=None):
        
        image_types = imagetypes()
        for case in Switch(mime_type):
            if case("image/jpeg"):
                return image_types & IMG_JPG != 0
            # end if
            if case("image/png"):
                return image_types & IMG_PNG != 0
            # end if
            if case("image/gif"):
                return image_types & IMG_GIF != 0
            # end if
        # end for
        return False
    # end def supports_mime_type
    #// 
    #// Loads image from $this->file into new GD Resource.
    #// 
    #// @since 3.5.0
    #// 
    #// @return bool|WP_Error True if loaded successfully; WP_Error on failure.
    #//
    def load(self):
        
        if self.image:
            return True
        # end if
        if (not php_is_file(self.file)) and (not php_preg_match("|^https?://|", self.file)):
            return php_new_class("WP_Error", lambda : WP_Error("error_loading_image", __("File doesn&#8217;t exist?"), self.file))
        # end if
        #// Set artificially high because GD uses uncompressed images in memory.
        wp_raise_memory_limit("image")
        self.image = php_no_error(lambda: imagecreatefromstring(php_file_get_contents(self.file)))
        if (not is_resource(self.image)):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_image", __("File is not an image."), self.file))
        # end if
        size = php_no_error(lambda: getimagesize(self.file))
        if (not size):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_image", __("Could not read image size."), self.file))
        # end if
        if php_function_exists("imagealphablending") and php_function_exists("imagesavealpha"):
            imagealphablending(self.image, False)
            imagesavealpha(self.image, True)
        # end if
        self.update_size(size[0], size[1])
        self.mime_type = size["mime"]
        return self.set_quality()
    # end def load
    #// 
    #// Sets or updates current image size.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int $width
    #// @param int $height
    #// @return true
    #//
    def update_size(self, width=False, height=False):
        
        if (not width):
            width = imagesx(self.image)
        # end if
        if (not height):
            height = imagesy(self.image)
        # end if
        return super().update_size(width, height)
    # end def update_size
    #// 
    #// Resizes current image.
    #// Wraps _resize, since _resize returns a GD Resource.
    #// 
    #// At minimum, either a height or width must be provided.
    #// If one of the two is set to null, the resize will
    #// maintain aspect ratio according to the provided dimension.
    #// 
    #// @since 3.5.0
    #// 
    #// @param  int|null $max_w Image width.
    #// @param  int|null $max_h Image height.
    #// @param  bool     $crop
    #// @return true|WP_Error
    #//
    def resize(self, max_w=None, max_h=None, crop=False):
        
        if self.size["width"] == max_w and self.size["height"] == max_h:
            return True
        # end if
        resized = self._resize(max_w, max_h, crop)
        if is_resource(resized):
            imagedestroy(self.image)
            self.image = resized
            return True
        elif is_wp_error(resized):
            return resized
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_resize_error", __("Image resize failed."), self.file))
    # end def resize
    #// 
    #// @param int $max_w
    #// @param int $max_h
    #// @param bool|array $crop
    #// @return resource|WP_Error
    #//
    def _resize(self, max_w=None, max_h=None, crop=False):
        
        dims = image_resize_dimensions(self.size["width"], self.size["height"], max_w, max_h, crop)
        if (not dims):
            return php_new_class("WP_Error", lambda : WP_Error("error_getting_dimensions", __("Could not calculate resized image dimensions"), self.file))
        # end if
        dst_x, dst_y, src_x, src_y, dst_w, dst_h, src_w, src_h = dims
        resized = wp_imagecreatetruecolor(dst_w, dst_h)
        imagecopyresampled(resized, self.image, dst_x, dst_y, src_x, src_y, dst_w, dst_h, src_w, src_h)
        if is_resource(resized):
            self.update_size(dst_w, dst_h)
            return resized
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_resize_error", __("Image resize failed."), self.file))
    # end def _resize
    #// 
    #// Create multiple smaller images from a single source.
    #// 
    #// Attempts to create all sub-sizes and returns the meta data at the end. This
    #// may result in the server running out of resources. When it fails there may be few
    #// "orphaned" images left over as the meta data is never returned and saved.
    #// 
    #// As of 5.3.0 the preferred way to do this is with `make_subsize()`. It creates
    #// the new images one at a time and allows for the meta data to be saved after
    #// each new image is created.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array $sizes {
    #// An array of image size data arrays.
    #// 
    #// Either a height or width must be provided.
    #// If one of the two is set to null, the resize will
    #// maintain aspect ratio according to the source image.
    #// 
    #// @type array $size {
    #// Array of height, width values, and whether to crop.
    #// 
    #// @type int  $width  Image width. Optional if `$height` is specified.
    #// @type int  $height Image height. Optional if `$width` is specified.
    #// @type bool $crop   Optional. Whether to crop the image. Default false.
    #// }
    #// }
    #// @return array An array of resized images' metadata by size.
    #//
    def multi_resize(self, sizes=None):
        
        metadata = Array()
        for size,size_data in sizes:
            meta = self.make_subsize(size_data)
            if (not is_wp_error(meta)):
                metadata[size] = meta
            # end if
        # end for
        return metadata
    # end def multi_resize
    #// 
    #// Create an image sub-size and return the image meta data value for it.
    #// 
    #// @since 5.3.0
    #// 
    #// @param array $size_data {
    #// Array of size data.
    #// 
    #// @type int  $width  The maximum width in pixels.
    #// @type int  $height The maximum height in pixels.
    #// @type bool $crop   Whether to crop the image to exact dimensions.
    #// }
    #// @return array|WP_Error The image data array for inclusion in the `sizes` array in the image meta,
    #// WP_Error object on error.
    #//
    def make_subsize(self, size_data=None):
        
        if (not (php_isset(lambda : size_data["width"]))) and (not (php_isset(lambda : size_data["height"]))):
            return php_new_class("WP_Error", lambda : WP_Error("image_subsize_create_error", __("Cannot resize the image. Both width and height are not set.")))
        # end if
        orig_size = self.size
        if (not (php_isset(lambda : size_data["width"]))):
            size_data["width"] = None
        # end if
        if (not (php_isset(lambda : size_data["height"]))):
            size_data["height"] = None
        # end if
        if (not (php_isset(lambda : size_data["crop"]))):
            size_data["crop"] = False
        # end if
        resized = self._resize(size_data["width"], size_data["height"], size_data["crop"])
        if is_wp_error(resized):
            saved = resized
        else:
            saved = self._save(resized)
            imagedestroy(resized)
        # end if
        self.size = orig_size
        if (not is_wp_error(saved)):
            saved["path"] = None
        # end if
        return saved
    # end def make_subsize
    #// 
    #// Crops Image.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int  $src_x   The start x position to crop from.
    #// @param int  $src_y   The start y position to crop from.
    #// @param int  $src_w   The width to crop.
    #// @param int  $src_h   The height to crop.
    #// @param int  $dst_w   Optional. The destination width.
    #// @param int  $dst_h   Optional. The destination height.
    #// @param bool $src_abs Optional. If the source crop points are absolute.
    #// @return bool|WP_Error
    #//
    def crop(self, src_x=None, src_y=None, src_w=None, src_h=None, dst_w=None, dst_h=None, src_abs=False):
        
        #// If destination width/height isn't specified,
        #// use same as width/height from source.
        if (not dst_w):
            dst_w = src_w
        # end if
        if (not dst_h):
            dst_h = src_h
        # end if
        dst = wp_imagecreatetruecolor(dst_w, dst_h)
        if src_abs:
            src_w -= src_x
            src_h -= src_y
        # end if
        if php_function_exists("imageantialias"):
            imageantialias(dst, True)
        # end if
        imagecopyresampled(dst, self.image, 0, 0, src_x, src_y, dst_w, dst_h, src_w, src_h)
        if is_resource(dst):
            imagedestroy(self.image)
            self.image = dst
            self.update_size()
            return True
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_crop_error", __("Image crop failed."), self.file))
    # end def crop
    #// 
    #// Rotates current image counter-clockwise by $angle.
    #// Ported from image-edit.php
    #// 
    #// @since 3.5.0
    #// 
    #// @param float $angle
    #// @return true|WP_Error
    #//
    def rotate(self, angle=None):
        
        if php_function_exists("imagerotate"):
            transparency = imagecolorallocatealpha(self.image, 255, 255, 255, 127)
            rotated = imagerotate(self.image, angle, transparency)
            if is_resource(rotated):
                imagealphablending(rotated, True)
                imagesavealpha(rotated, True)
                imagedestroy(self.image)
                self.image = rotated
                self.update_size()
                return True
            # end if
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_rotate_error", __("Image rotate failed."), self.file))
    # end def rotate
    #// 
    #// Flips current image.
    #// 
    #// @since 3.5.0
    #// 
    #// @param bool $horz Flip along Horizontal Axis.
    #// @param bool $vert Flip along Vertical Axis.
    #// @return true|WP_Error
    #//
    def flip(self, horz=None, vert=None):
        
        w = self.size["width"]
        h = self.size["height"]
        dst = wp_imagecreatetruecolor(w, h)
        if is_resource(dst):
            sx = w - 1 if vert else 0
            sy = h - 1 if horz else 0
            sw = -w if vert else w
            sh = -h if horz else h
            if imagecopyresampled(dst, self.image, 0, 0, sx, sy, w, h, sw, sh):
                imagedestroy(self.image)
                self.image = dst
                return True
            # end if
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_flip_error", __("Image flip failed."), self.file))
    # end def flip
    #// 
    #// Saves current in-memory image to file.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string|null $filename
    #// @param string|null $mime_type
    #// @return array|WP_Error {'path'=>string, 'file'=>string, 'width'=>int, 'height'=>int, 'mime-type'=>string}
    #//
    def save(self, filename=None, mime_type=None):
        
        saved = self._save(self.image, filename, mime_type)
        if (not is_wp_error(saved)):
            self.file = saved["path"]
            self.mime_type = saved["mime-type"]
        # end if
        return saved
    # end def save
    #// 
    #// @param resource $image
    #// @param string|null $filename
    #// @param string|null $mime_type
    #// @return array|WP_Error
    #//
    def _save(self, image=None, filename=None, mime_type=None):
        
        filename, extension, mime_type = self.get_output_format(filename, mime_type)
        if (not filename):
            filename = self.generate_filename(None, None, extension)
        # end if
        if "image/gif" == mime_type:
            if (not self.make_image(filename, "imagegif", Array(image, filename))):
                return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
            # end if
        elif "image/png" == mime_type:
            #// Convert from full colors to index colors, like original PNG.
            if php_function_exists("imageistruecolor") and (not imageistruecolor(image)):
                imagetruecolortopalette(image, False, imagecolorstotal(image))
            # end if
            if (not self.make_image(filename, "imagepng", Array(image, filename))):
                return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
            # end if
        elif "image/jpeg" == mime_type:
            if (not self.make_image(filename, "imagejpeg", Array(image, filename, self.get_quality()))):
                return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
            # end if
        else:
            return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
        # end if
        #// Set correct file permissions.
        stat = stat(php_dirname(filename))
        perms = stat["mode"] & 438
        #// Same permissions as parent folder, strip off the executable bits.
        chmod(filename, perms)
        #// 
        #// Filters the name of the saved image file.
        #// 
        #// @since 2.6.0
        #// 
        #// @param string $filename Name of the file.
        #//
        return Array({"path": filename, "file": wp_basename(apply_filters("image_make_intermediate_size", filename)), "width": self.size["width"], "height": self.size["height"], "mime-type": mime_type})
    # end def _save
    #// 
    #// Returns stream of current image.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $mime_type The mime type of the image.
    #// @return bool True on success, false on failure.
    #//
    def stream(self, mime_type=None):
        
        filename, extension, mime_type = self.get_output_format(None, mime_type)
        for case in Switch(mime_type):
            if case("image/png"):
                php_header("Content-Type: image/png")
                return imagepng(self.image)
            # end if
            if case("image/gif"):
                php_header("Content-Type: image/gif")
                return imagegif(self.image)
            # end if
            if case():
                php_header("Content-Type: image/jpeg")
                return imagejpeg(self.image, None, self.get_quality())
            # end if
        # end for
    # end def stream
    #// 
    #// Either calls editor's save function or handles file as a stream.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string|stream $filename
    #// @param callable $function
    #// @param array $arguments
    #// @return bool
    #//
    def make_image(self, filename=None, function=None, arguments=None):
        
        if wp_is_stream(filename):
            arguments[1] = None
        # end if
        return super().make_image(filename, function, arguments)
    # end def make_image
# end class WP_Image_Editor_GD
