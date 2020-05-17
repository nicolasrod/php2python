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
    #// 
    #// GD Resource.
    #// 
    #// @var resource
    #//
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
    def test(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if (not php_extension_loaded("gd")) or (not php_function_exists("gd_info")):
            return False
        # end if
        #// On some setups GD library does not provide imagerotate() - Ticket #11536.
        if (php_isset(lambda : args_["methods"])) and php_in_array("rotate", args_["methods"], True) and (not php_function_exists("imagerotate")):
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
    def supports_mime_type(self, mime_type_=None):
        
        
        image_types_ = imagetypes()
        for case in Switch(mime_type_):
            if case("image/jpeg"):
                return image_types_ & IMG_JPG != 0
            # end if
            if case("image/png"):
                return image_types_ & IMG_PNG != 0
            # end if
            if case("image/gif"):
                return image_types_ & IMG_GIF != 0
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
        if (not php_is_file(self.file_)) and (not php_preg_match("|^https?://|", self.file_)):
            return php_new_class("WP_Error", lambda : WP_Error("error_loading_image", __("File doesn&#8217;t exist?"), self.file_))
        # end if
        #// Set artificially high because GD uses uncompressed images in memory.
        wp_raise_memory_limit("image")
        self.image = php_no_error(lambda: imagecreatefromstring(php_file_get_contents(self.file_)))
        if (not is_resource(self.image)):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_image", __("File is not an image."), self.file_))
        # end if
        size_ = php_no_error(lambda: getimagesize(self.file_))
        if (not size_):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_image", __("Could not read image size."), self.file_))
        # end if
        if php_function_exists("imagealphablending") and php_function_exists("imagesavealpha"):
            imagealphablending(self.image, False)
            imagesavealpha(self.image, True)
        # end if
        self.update_size(size_[0], size_[1])
        self.mime_type = size_["mime"]
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
    def update_size(self, width_=None, height_=None):
        if width_ is None:
            width_ = False
        # end if
        if height_ is None:
            height_ = False
        # end if
        
        if (not width_):
            width_ = imagesx(self.image)
        # end if
        if (not height_):
            height_ = imagesy(self.image)
        # end if
        return super().update_size(width_, height_)
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
    def resize(self, max_w_=None, max_h_=None, crop_=None):
        if crop_ is None:
            crop_ = False
        # end if
        
        if self.size["width"] == max_w_ and self.size["height"] == max_h_:
            return True
        # end if
        resized_ = self._resize(max_w_, max_h_, crop_)
        if is_resource(resized_):
            imagedestroy(self.image)
            self.image = resized_
            return True
        elif is_wp_error(resized_):
            return resized_
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_resize_error", __("Image resize failed."), self.file_))
    # end def resize
    #// 
    #// @param int $max_w
    #// @param int $max_h
    #// @param bool|array $crop
    #// @return resource|WP_Error
    #//
    def _resize(self, max_w_=None, max_h_=None, crop_=None):
        if crop_ is None:
            crop_ = False
        # end if
        
        dims_ = image_resize_dimensions(self.size["width"], self.size["height"], max_w_, max_h_, crop_)
        if (not dims_):
            return php_new_class("WP_Error", lambda : WP_Error("error_getting_dimensions", __("Could not calculate resized image dimensions"), self.file_))
        # end if
        dst_x_, dst_y_, src_x_, src_y_, dst_w_, dst_h_, src_w_, src_h_ = dims_
        resized_ = wp_imagecreatetruecolor(dst_w_, dst_h_)
        imagecopyresampled(resized_, self.image, dst_x_, dst_y_, src_x_, src_y_, dst_w_, dst_h_, src_w_, src_h_)
        if is_resource(resized_):
            self.update_size(dst_w_, dst_h_)
            return resized_
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_resize_error", __("Image resize failed."), self.file_))
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
    def multi_resize(self, sizes_=None):
        
        
        metadata_ = Array()
        for size_,size_data_ in sizes_:
            meta_ = self.make_subsize(size_data_)
            if (not is_wp_error(meta_)):
                metadata_[size_] = meta_
            # end if
        # end for
        return metadata_
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
    def make_subsize(self, size_data_=None):
        
        
        if (not (php_isset(lambda : size_data_["width"]))) and (not (php_isset(lambda : size_data_["height"]))):
            return php_new_class("WP_Error", lambda : WP_Error("image_subsize_create_error", __("Cannot resize the image. Both width and height are not set.")))
        # end if
        orig_size_ = self.size
        if (not (php_isset(lambda : size_data_["width"]))):
            size_data_["width"] = None
        # end if
        if (not (php_isset(lambda : size_data_["height"]))):
            size_data_["height"] = None
        # end if
        if (not (php_isset(lambda : size_data_["crop"]))):
            size_data_["crop"] = False
        # end if
        resized_ = self._resize(size_data_["width"], size_data_["height"], size_data_["crop"])
        if is_wp_error(resized_):
            saved_ = resized_
        else:
            saved_ = self._save(resized_)
            imagedestroy(resized_)
        # end if
        self.size = orig_size_
        if (not is_wp_error(saved_)):
            saved_["path"] = None
        # end if
        return saved_
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
    def crop(self, src_x_=None, src_y_=None, src_w_=None, src_h_=None, dst_w_=None, dst_h_=None, src_abs_=None):
        if dst_w_ is None:
            dst_w_ = None
        # end if
        if dst_h_ is None:
            dst_h_ = None
        # end if
        if src_abs_ is None:
            src_abs_ = False
        # end if
        
        #// If destination width/height isn't specified,
        #// use same as width/height from source.
        if (not dst_w_):
            dst_w_ = src_w_
        # end if
        if (not dst_h_):
            dst_h_ = src_h_
        # end if
        dst_ = wp_imagecreatetruecolor(dst_w_, dst_h_)
        if src_abs_:
            src_w_ -= src_x_
            src_h_ -= src_y_
        # end if
        if php_function_exists("imageantialias"):
            imageantialias(dst_, True)
        # end if
        imagecopyresampled(dst_, self.image, 0, 0, src_x_, src_y_, dst_w_, dst_h_, src_w_, src_h_)
        if is_resource(dst_):
            imagedestroy(self.image)
            self.image = dst_
            self.update_size()
            return True
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_crop_error", __("Image crop failed."), self.file_))
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
    def rotate(self, angle_=None):
        
        
        if php_function_exists("imagerotate"):
            transparency_ = imagecolorallocatealpha(self.image, 255, 255, 255, 127)
            rotated_ = imagerotate(self.image, angle_, transparency_)
            if is_resource(rotated_):
                imagealphablending(rotated_, True)
                imagesavealpha(rotated_, True)
                imagedestroy(self.image)
                self.image = rotated_
                self.update_size()
                return True
            # end if
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_rotate_error", __("Image rotate failed."), self.file_))
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
    def flip(self, horz_=None, vert_=None):
        
        
        w_ = self.size["width"]
        h_ = self.size["height"]
        dst_ = wp_imagecreatetruecolor(w_, h_)
        if is_resource(dst_):
            sx_ = w_ - 1 if vert_ else 0
            sy_ = h_ - 1 if horz_ else 0
            sw_ = -w_ if vert_ else w_
            sh_ = -h_ if horz_ else h_
            if imagecopyresampled(dst_, self.image, 0, 0, sx_, sy_, w_, h_, sw_, sh_):
                imagedestroy(self.image)
                self.image = dst_
                return True
            # end if
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("image_flip_error", __("Image flip failed."), self.file_))
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
    def save(self, filename_=None, mime_type_=None):
        if filename_ is None:
            filename_ = None
        # end if
        if mime_type_ is None:
            mime_type_ = None
        # end if
        
        saved_ = self._save(self.image, filename_, mime_type_)
        if (not is_wp_error(saved_)):
            self.file_ = saved_["path"]
            self.mime_type = saved_["mime-type"]
        # end if
        return saved_
    # end def save
    #// 
    #// @param resource $image
    #// @param string|null $filename
    #// @param string|null $mime_type
    #// @return array|WP_Error
    #//
    def _save(self, image_=None, filename_=None, mime_type_=None):
        if filename_ is None:
            filename_ = None
        # end if
        if mime_type_ is None:
            mime_type_ = None
        # end if
        
        filename_, extension_, mime_type_ = self.get_output_format(filename_, mime_type_)
        if (not filename_):
            filename_ = self.generate_filename(None, None, extension_)
        # end if
        if "image/gif" == mime_type_:
            if (not self.make_image(filename_, "imagegif", Array(image_, filename_))):
                return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
            # end if
        elif "image/png" == mime_type_:
            #// Convert from full colors to index colors, like original PNG.
            if php_function_exists("imageistruecolor") and (not imageistruecolor(image_)):
                imagetruecolortopalette(image_, False, imagecolorstotal(image_))
            # end if
            if (not self.make_image(filename_, "imagepng", Array(image_, filename_))):
                return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
            # end if
        elif "image/jpeg" == mime_type_:
            if (not self.make_image(filename_, "imagejpeg", Array(image_, filename_, self.get_quality()))):
                return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
            # end if
        else:
            return php_new_class("WP_Error", lambda : WP_Error("image_save_error", __("Image Editor Save Failed")))
        # end if
        #// Set correct file permissions.
        stat_ = stat(php_dirname(filename_))
        perms_ = stat_["mode"] & 438
        #// Same permissions as parent folder, strip off the executable bits.
        chmod(filename_, perms_)
        #// 
        #// Filters the name of the saved image file.
        #// 
        #// @since 2.6.0
        #// 
        #// @param string $filename Name of the file.
        #//
        return Array({"path": filename_, "file": wp_basename(apply_filters("image_make_intermediate_size", filename_)), "width": self.size["width"], "height": self.size["height"], "mime-type": mime_type_})
    # end def _save
    #// 
    #// Returns stream of current image.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $mime_type The mime type of the image.
    #// @return bool True on success, false on failure.
    #//
    def stream(self, mime_type_=None):
        if mime_type_ is None:
            mime_type_ = None
        # end if
        
        filename_, extension_, mime_type_ = self.get_output_format(None, mime_type_)
        for case in Switch(mime_type_):
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
    def make_image(self, filename_=None, function_=None, arguments_=None):
        
        
        if wp_is_stream(filename_):
            arguments_[1] = None
        # end if
        return super().make_image(filename_, function_, arguments_)
    # end def make_image
# end class WP_Image_Editor_GD
