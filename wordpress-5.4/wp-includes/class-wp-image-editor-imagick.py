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
#// WordPress Imagick Image Editor
#// 
#// @package WordPress
#// @subpackage Image_Editor
#// 
#// 
#// WordPress Image Editor Class for Image Manipulation through Imagick PHP Module
#// 
#// @since 3.5.0
#// 
#// @see WP_Image_Editor
#//
class WP_Image_Editor_Imagick(WP_Image_Editor):
    #// 
    #// Imagick object.
    #// 
    #// @var Imagick
    #//
    image = Array()
    def __del__(self):
        
        
        if type(self.image).__name__ == "Imagick":
            #// We don't need the original in memory anymore.
            self.image.clear()
            self.image.destroy()
        # end if
    # end def __del__
    #// 
    #// Checks to see if current environment supports Imagick.
    #// 
    #// We require Imagick 2.2.0 or greater, based on whether the queryFormats()
    #// method can be called statically.
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
        
        #// First, test Imagick's extension and classes.
        if (not php_extension_loaded("imagick")) or (not php_class_exists("Imagick", False)) or (not php_class_exists("ImagickPixel", False)):
            return False
        # end if
        if php_version_compare(php_phpversion("imagick"), "2.2.0", "<"):
            return False
        # end if
        required_methods_ = Array("clear", "destroy", "valid", "getimage", "writeimage", "getimageblob", "getimagegeometry", "getimageformat", "setimageformat", "setimagecompression", "setimagecompressionquality", "setimagepage", "setoption", "scaleimage", "cropimage", "rotateimage", "flipimage", "flopimage", "readimage")
        #// Now, test for deep requirements within Imagick.
        if (not php_defined("imagick::COMPRESSION_JPEG")):
            return False
        # end if
        class_methods_ = php_array_map("strtolower", get_class_methods("Imagick"))
        if php_array_diff(required_methods_, class_methods_):
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
        
        
        imagick_extension_ = php_strtoupper(self.get_extension(mime_type_))
        if (not imagick_extension_):
            return False
        # end if
        #// setIteratorIndex is optional unless mime is an animated format.
        #// Here, we just say no if you are missing it and aren't loading a jpeg.
        if (not php_method_exists("Imagick", "setIteratorIndex")) and "image/jpeg" != mime_type_:
            return False
        # end if
        try: 
            #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
            return php_bool(php_no_error(lambda: Imagick.queryformats(imagick_extension_)))
        except Exception as e_:
            return False
        # end try
    # end def supports_mime_type
    #// 
    #// Loads image from $this->file into new Imagick Object.
    #// 
    #// @since 3.5.0
    #// 
    #// @return true|WP_Error True if loaded; WP_Error on failure.
    #//
    def load(self):
        
        
        if type(self.image).__name__ == "Imagick":
            return True
        # end if
        if (not php_is_file(self.file_)) and (not php_preg_match("|^https?://|", self.file_)):
            return php_new_class("WP_Error", lambda : WP_Error("error_loading_image", __("File doesn&#8217;t exist?"), self.file_))
        # end if
        #// 
        #// Even though Imagick uses less PHP memory than GD, set higher limit
        #// for users that have low PHP.ini limits.
        #//
        wp_raise_memory_limit("image")
        try: 
            self.image = php_new_class("Imagick", lambda : Imagick())
            file_extension_ = php_strtolower(pathinfo(self.file_, PATHINFO_EXTENSION))
            filename_ = self.file_
            if "pdf" == file_extension_:
                filename_ = self.pdf_setup()
            # end if
            #// Reading image after Imagick instantiation because `setResolution`
            #// only applies correctly before the image is read.
            self.image.readimage(filename_)
            if (not self.image.valid()):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_image", __("File is not an image."), self.file_))
            # end if
            #// Select the first frame to handle animated images properly.
            if php_is_callable(Array(self.image, "setIteratorIndex")):
                self.image.setiteratorindex(0)
            # end if
            self.mime_type = self.get_mime_type(self.image.getimageformat())
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_image", e_.getmessage(), self.file_))
        # end try
        updated_size_ = self.update_size()
        if is_wp_error(updated_size_):
            return updated_size_
        # end if
        return self.set_quality()
    # end def load
    #// 
    #// Sets Image Compression quality on a 1-100% scale.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int $quality Compression Quality. Range: [1,100]
    #// @return true|WP_Error True if set successfully; WP_Error on failure.
    #//
    def set_quality(self, quality_=None):
        
        
        quality_result_ = super().set_quality(quality_)
        if is_wp_error(quality_result_):
            return quality_result_
        else:
            quality_ = self.get_quality()
        # end if
        try: 
            if "image/jpeg" == self.mime_type:
                self.image.setimagecompressionquality(quality_)
                self.image.setimagecompression(imagick.COMPRESSION_JPEG)
            else:
                self.image.setimagecompressionquality(quality_)
            # end if
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_quality_error", e_.getmessage()))
        # end try
        return True
    # end def set_quality
    #// 
    #// Sets or updates current image size.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int $width
    #// @param int $height
    #// 
    #// @return true|WP_Error
    #//
    def update_size(self, width_=None, height_=None):
        
        
        size_ = None
        if (not width_) or (not height_):
            try: 
                size_ = self.image.getimagegeometry()
            except Exception as e_:
                return php_new_class("WP_Error", lambda : WP_Error("invalid_image", __("Could not read image size."), self.file_))
            # end try
        # end if
        if (not width_):
            width_ = size_["width"]
        # end if
        if (not height_):
            height_ = size_["height"]
        # end if
        return super().update_size(width_, height_)
    # end def update_size
    #// 
    #// Resizes current image.
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
    #// @return bool|WP_Error
    #//
    def resize(self, max_w_=None, max_h_=None, crop_=None):
        if crop_ is None:
            crop_ = False
        # end if
        
        if self.size["width"] == max_w_ and self.size["height"] == max_h_:
            return True
        # end if
        dims_ = image_resize_dimensions(self.size["width"], self.size["height"], max_w_, max_h_, crop_)
        if (not dims_):
            return php_new_class("WP_Error", lambda : WP_Error("error_getting_dimensions", __("Could not calculate resized image dimensions")))
        # end if
        dst_x_, dst_y_, src_x_, src_y_, dst_w_, dst_h_, src_w_, src_h_ = dims_
        if crop_:
            return self.crop(src_x_, src_y_, src_w_, src_h_, dst_w_, dst_h_)
        # end if
        #// Execute the resize.
        thumb_result_ = self.thumbnail_image(dst_w_, dst_h_)
        if is_wp_error(thumb_result_):
            return thumb_result_
        # end if
        return self.update_size(dst_w_, dst_h_)
    # end def resize
    #// 
    #// Efficiently resize the current image
    #// 
    #// This is a WordPress specific implementation of Imagick::thumbnailImage(),
    #// which resizes an image to given dimensions and removes any associated profiles.
    #// 
    #// @since 4.5.0
    #// 
    #// @param int    $dst_w       The destination width.
    #// @param int    $dst_h       The destination height.
    #// @param string $filter_name Optional. The Imagick filter to use when resizing. Default 'FILTER_TRIANGLE'.
    #// @param bool   $strip_meta  Optional. Strip all profiles, excluding color profiles, from the image. Default true.
    #// @return bool|WP_Error
    #//
    def thumbnail_image(self, dst_w_=None, dst_h_=None, filter_name_="FILTER_TRIANGLE", strip_meta_=None):
        if strip_meta_ is None:
            strip_meta_ = True
        # end if
        
        allowed_filters_ = Array("FILTER_POINT", "FILTER_BOX", "FILTER_TRIANGLE", "FILTER_HERMITE", "FILTER_HANNING", "FILTER_HAMMING", "FILTER_BLACKMAN", "FILTER_GAUSSIAN", "FILTER_QUADRATIC", "FILTER_CUBIC", "FILTER_CATROM", "FILTER_MITCHELL", "FILTER_LANCZOS", "FILTER_BESSEL", "FILTER_SINC")
        #// 
        #// Set the filter value if '$filter_name' name is in our whitelist and the related
        #// Imagick constant is defined or fall back to our default filter.
        #//
        if php_in_array(filter_name_, allowed_filters_, True) and php_defined("Imagick::" + filter_name_):
            filter_ = constant("Imagick::" + filter_name_)
        else:
            filter_ = Imagick.FILTER_TRIANGLE if php_defined("Imagick::FILTER_TRIANGLE") else False
        # end if
        #// 
        #// Filters whether to strip metadata from images when they're resized.
        #// 
        #// This filter only applies when resizing using the Imagick editor since GD
        #// always strips profiles by default.
        #// 
        #// @since 4.5.0
        #// 
        #// @param bool $strip_meta Whether to strip image metadata during resizing. Default true.
        #//
        if apply_filters("image_strip_meta", strip_meta_):
            self.strip_meta()
            pass
        # end if
        try: 
            #// 
            #// To be more efficient, resample large images to 5x the destination size before resizing
            #// whenever the output size is less that 1/3 of the original image size (1/3^2 ~= .111),
            #// unless we would be resampling to a scale smaller than 128x128.
            #//
            if php_is_callable(Array(self.image, "sampleImage")):
                resize_ratio_ = dst_w_ / self.size["width"] * dst_h_ / self.size["height"]
                sample_factor_ = 5
                if resize_ratio_ < 0.111 and dst_w_ * sample_factor_ > 128 and dst_h_ * sample_factor_ > 128:
                    self.image.sampleimage(dst_w_ * sample_factor_, dst_h_ * sample_factor_)
                # end if
            # end if
            #// 
            #// Use resizeImage() when it's available and a valid filter value is set.
            #// Otherwise, fall back to the scaleImage() method for resizing, which
            #// results in better image quality over resizeImage() with default filter
            #// settings and retains backward compatibility with pre 4.5 functionality.
            #//
            if php_is_callable(Array(self.image, "resizeImage")) and filter_:
                self.image.setoption("filter:support", "2.0")
                self.image.resizeimage(dst_w_, dst_h_, filter_, 1)
            else:
                self.image.scaleimage(dst_w_, dst_h_)
            # end if
            #// Set appropriate quality settings after resizing.
            if "image/jpeg" == self.mime_type:
                if php_is_callable(Array(self.image, "unsharpMaskImage")):
                    self.image.unsharpmaskimage(0.25, 0.25, 8, 0.065)
                # end if
                self.image.setoption("jpeg:fancy-upsampling", "off")
            # end if
            if "image/png" == self.mime_type:
                self.image.setoption("png:compression-filter", "5")
                self.image.setoption("png:compression-level", "9")
                self.image.setoption("png:compression-strategy", "1")
                self.image.setoption("png:exclude-chunk", "all")
            # end if
            #// 
            #// If alpha channel is not defined, set it opaque.
            #// 
            #// Note that Imagick::getImageAlphaChannel() is only available if Imagick
            #// has been compiled against ImageMagick version 6.4.0 or newer.
            #//
            if php_is_callable(Array(self.image, "getImageAlphaChannel")) and php_is_callable(Array(self.image, "setImageAlphaChannel")) and php_defined("Imagick::ALPHACHANNEL_UNDEFINED") and php_defined("Imagick::ALPHACHANNEL_OPAQUE"):
                if self.image.getimagealphachannel() == Imagick.ALPHACHANNEL_UNDEFINED:
                    self.image.setimagealphachannel(Imagick.ALPHACHANNEL_OPAQUE)
                # end if
            # end if
            #// Limit the bit depth of resized images to 8 bits per channel.
            if php_is_callable(Array(self.image, "getImageDepth")) and php_is_callable(Array(self.image, "setImageDepth")):
                if 8 < self.image.getimagedepth():
                    self.image.setimagedepth(8)
                # end if
            # end if
            if php_is_callable(Array(self.image, "setInterlaceScheme")) and php_defined("Imagick::INTERLACE_NO"):
                self.image.setinterlacescheme(Imagick.INTERLACE_NO)
            # end if
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_resize_error", e_.getmessage()))
        # end try
    # end def thumbnail_image
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
    #// maintain aspect ratio according to the provided dimension.
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
        orig_image_ = self.image.getimage()
        if (not (php_isset(lambda : size_data_["width"]))):
            size_data_["width"] = None
        # end if
        if (not (php_isset(lambda : size_data_["height"]))):
            size_data_["height"] = None
        # end if
        if (not (php_isset(lambda : size_data_["crop"]))):
            size_data_["crop"] = False
        # end if
        resized_ = self.resize(size_data_["width"], size_data_["height"], size_data_["crop"])
        if is_wp_error(resized_):
            saved_ = resized_
        else:
            saved_ = self._save(self.image)
            self.image.clear()
            self.image.destroy()
            self.image = None
        # end if
        self.size = orig_size_
        self.image = orig_image_
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
    #// @param int  $src_x The start x position to crop from.
    #// @param int  $src_y The start y position to crop from.
    #// @param int  $src_w The width to crop.
    #// @param int  $src_h The height to crop.
    #// @param int  $dst_w Optional. The destination width.
    #// @param int  $dst_h Optional. The destination height.
    #// @param bool $src_abs Optional. If the source crop points are absolute.
    #// @return bool|WP_Error
    #//
    def crop(self, src_x_=None, src_y_=None, src_w_=None, src_h_=None, dst_w_=None, dst_h_=None, src_abs_=None):
        if src_abs_ is None:
            src_abs_ = False
        # end if
        
        if src_abs_:
            src_w_ -= src_x_
            src_h_ -= src_y_
        # end if
        try: 
            self.image.cropimage(src_w_, src_h_, src_x_, src_y_)
            self.image.setimagepage(src_w_, src_h_, 0, 0)
            if dst_w_ or dst_h_:
                #// If destination width/height isn't specified,
                #// use same as width/height from source.
                if (not dst_w_):
                    dst_w_ = src_w_
                # end if
                if (not dst_h_):
                    dst_h_ = src_h_
                # end if
                thumb_result_ = self.thumbnail_image(dst_w_, dst_h_)
                if is_wp_error(thumb_result_):
                    return thumb_result_
                # end if
                return self.update_size()
            # end if
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_crop_error", e_.getmessage()))
        # end try
        return self.update_size()
    # end def crop
    #// 
    #// Rotates current image counter-clockwise by $angle.
    #// 
    #// @since 3.5.0
    #// 
    #// @param float $angle
    #// @return true|WP_Error
    #//
    def rotate(self, angle_=None):
        
        
        #// 
        #// $angle is 360-$angle because Imagick rotates clockwise
        #// (GD rotates counter-clockwise)
        #//
        try: 
            self.image.rotateimage(php_new_class("ImagickPixel", lambda : ImagickPixel("none")), 360 - angle_)
            #// Normalise EXIF orientation data so that display is consistent across devices.
            if php_is_callable(Array(self.image, "setImageOrientation")) and php_defined("Imagick::ORIENTATION_TOPLEFT"):
                self.image.setimageorientation(Imagick.ORIENTATION_TOPLEFT)
            # end if
            #// Since this changes the dimensions of the image, update the size.
            result_ = self.update_size()
            if is_wp_error(result_):
                return result_
            # end if
            self.image.setimagepage(self.size["width"], self.size["height"], 0, 0)
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_rotate_error", e_.getmessage()))
        # end try
        return True
    # end def rotate
    #// 
    #// Flips current image.
    #// 
    #// @since 3.5.0
    #// 
    #// @param bool $horz Flip along Horizontal Axis
    #// @param bool $vert Flip along Vertical Axis
    #// @return true|WP_Error
    #//
    def flip(self, horz_=None, vert_=None):
        
        
        try: 
            if horz_:
                self.image.flipimage()
            # end if
            if vert_:
                self.image.flopimage()
            # end if
            #// Normalise EXIF orientation data so that display is consistent across devices.
            if php_is_callable(Array(self.image, "setImageOrientation")) and php_defined("Imagick::ORIENTATION_TOPLEFT"):
                self.image.setimageorientation(Imagick.ORIENTATION_TOPLEFT)
            # end if
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_flip_error", e_.getmessage()))
        # end try
        return True
    # end def flip
    #// 
    #// Check if a JPEG image has EXIF Orientation tag and rotate it if needed.
    #// 
    #// As ImageMagick copies the EXIF data to the flipped/rotated image, proceed only
    #// if EXIF Orientation can be reset afterwards.
    #// 
    #// @since 5.3.0
    #// 
    #// @return bool|WP_Error True if the image was rotated. False if no EXIF data or if the image doesn't need rotation.
    #// WP_Error if error while rotating.
    #//
    def maybe_exif_rotate(self):
        
        
        if php_is_callable(Array(self.image, "setImageOrientation")) and php_defined("Imagick::ORIENTATION_TOPLEFT"):
            return super().maybe_exif_rotate()
        else:
            return php_new_class("WP_Error", lambda : WP_Error("write_exif_error", __("The image cannot be rotated because the embedded meta data cannot be updated.")))
        # end if
    # end def maybe_exif_rotate
    #// 
    #// Saves current image to file.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $destfilename
    #// @param string $mime_type
    #// @return array|WP_Error {'path'=>string, 'file'=>string, 'width'=>int, 'height'=>int, 'mime-type'=>string}
    #//
    def save(self, destfilename_=None, mime_type_=None):
        
        
        saved_ = self._save(self.image, destfilename_, mime_type_)
        if (not is_wp_error(saved_)):
            self.file_ = saved_["path"]
            self.mime_type = saved_["mime-type"]
            try: 
                self.image.setimageformat(php_strtoupper(self.get_extension(self.mime_type)))
            except Exception as e_:
                return php_new_class("WP_Error", lambda : WP_Error("image_save_error", e_.getmessage(), self.file_))
            # end try
        # end if
        return saved_
    # end def save
    #// 
    #// @param Imagick $image
    #// @param string $filename
    #// @param string $mime_type
    #// @return array|WP_Error
    #//
    def _save(self, image_=None, filename_=None, mime_type_=None):
        
        
        filename_, extension_, mime_type_ = self.get_output_format(filename_, mime_type_)
        if (not filename_):
            filename_ = self.generate_filename(None, None, extension_)
        # end if
        try: 
            #// Store initial format.
            orig_format_ = self.image.getimageformat()
            self.image.setimageformat(php_strtoupper(self.get_extension(mime_type_)))
            self.make_image(filename_, Array(image_, "writeImage"), Array(filename_))
            #// Reset original format.
            self.image.setimageformat(orig_format_)
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_save_error", e_.getmessage(), filename_))
        # end try
        #// Set correct file permissions.
        stat_ = stat(php_dirname(filename_))
        perms_ = stat_["mode"] & 438
        #// Same permissions as parent folder, strip off the executable bits.
        chmod(filename_, perms_)
        return Array({"path": filename_, "file": wp_basename(apply_filters("image_make_intermediate_size", filename_)), "width": self.size["width"], "height": self.size["height"], "mime-type": mime_type_})
    # end def _save
    #// 
    #// Streams current image to browser.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $mime_type The mime type of the image.
    #// @return bool|WP_Error True on success, WP_Error object on failure.
    #//
    def stream(self, mime_type_=None):
        
        
        filename_, extension_, mime_type_ = self.get_output_format(None, mime_type_)
        try: 
            #// Temporarily change format for stream.
            self.image.setimageformat(php_strtoupper(extension_))
            #// Output stream of image content.
            php_header(str("Content-Type: ") + str(mime_type_))
            php_print(self.image.getimageblob())
            #// Reset image to original format.
            self.image.setimageformat(self.get_extension(self.mime_type))
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_stream_error", e_.getmessage()))
        # end try
        return True
    # end def stream
    #// 
    #// Strips all image meta except color profiles from an image.
    #// 
    #// @since 4.5.0
    #// 
    #// @return true|WP_Error True if stripping metadata was successful. WP_Error object on error.
    #//
    def strip_meta(self):
        
        
        if (not php_is_callable(Array(self.image, "getImageProfiles"))):
            #// translators: %s: ImageMagick method name.
            return php_new_class("WP_Error", lambda : WP_Error("image_strip_meta_error", php_sprintf(__("%s is required to strip image meta."), "<code>Imagick::getImageProfiles()</code>")))
        # end if
        if (not php_is_callable(Array(self.image, "removeImageProfile"))):
            #// translators: %s: ImageMagick method name.
            return php_new_class("WP_Error", lambda : WP_Error("image_strip_meta_error", php_sprintf(__("%s is required to strip image meta."), "<code>Imagick::removeImageProfile()</code>")))
        # end if
        #// 
        #// Protect a few profiles from being stripped for the following reasons:
        #// 
        #// - icc:  Color profile information
        #// - icm:  Color profile information
        #// - iptc: Copyright data
        #// - exif: Orientation data
        #// - xmp:  Rights usage data
        #//
        protected_profiles_ = Array("icc", "icm", "iptc", "exif", "xmp")
        try: 
            #// Strip profiles.
            for key_,value_ in self.image.getimageprofiles("*", True):
                if (not php_in_array(key_, protected_profiles_, True)):
                    self.image.removeimageprofile(key_)
                # end if
            # end for
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("image_strip_meta_error", e_.getmessage()))
        # end try
        return True
    # end def strip_meta
    #// 
    #// Sets up Imagick for PDF processing.
    #// Increases rendering DPI and only loads first page.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string|WP_Error File to load or WP_Error on failure.
    #//
    def pdf_setup(self):
        
        
        try: 
            #// By default, PDFs are rendered in a very low resolution.
            #// We want the thumbnail to be readable, so increase the rendering DPI.
            self.image.setresolution(128, 128)
            #// When generating thumbnails from cropped PDF pages, Imagemagick uses the uncropped
            #// area (resulting in unnecessary whitespace) unless the following option is set.
            self.image.setoption("pdf:use-cropbox", True)
            #// Only load the first page.
            return self.file_ + "[0]"
        except Exception as e_:
            return php_new_class("WP_Error", lambda : WP_Error("pdf_setup_failed", e_.getmessage(), self.file_))
        # end try
    # end def pdf_setup
# end class WP_Image_Editor_Imagick
