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
#// Base WordPress Image Editor
#// 
#// @package WordPress
#// @subpackage Image_Editor
#// 
#// 
#// Base image editor class from which implementations extend
#// 
#// @since 3.5.0
#//
class WP_Image_Editor():
    file_ = None
    size = None
    mime_type = None
    default_mime_type = "image/jpeg"
    quality = False
    default_quality = 82
    #// 
    #// Each instance handles a single file.
    #// 
    #// @param string $file Path to the file to load.
    #//
    def __init__(self, file_=None):
        
        
        self.file_ = file_
    # end def __init__
    #// 
    #// Checks to see if current environment supports the editor chosen.
    #// Must be overridden in a subclass.
    #// 
    #// @since 3.5.0
    #// 
    #// @abstract
    #// 
    #// @param array $args
    #// @return bool
    #//
    @classmethod
    def test(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        return False
    # end def test
    #// 
    #// Checks to see if editor supports the mime-type specified.
    #// Must be overridden in a subclass.
    #// 
    #// @since 3.5.0
    #// 
    #// @abstract
    #// 
    #// @param string $mime_type
    #// @return bool
    #//
    @classmethod
    def supports_mime_type(self, mime_type_=None):
        
        
        return False
    # end def supports_mime_type
    #// 
    #// Loads image from $this->file into editor.
    #// 
    #// @since 3.5.0
    #// @abstract
    #// 
    #// @return bool|WP_Error True if loaded; WP_Error on failure.
    #//
    def load(self):
        
        
        pass
    # end def load
    #// 
    #// Saves current image to file.
    #// 
    #// @since 3.5.0
    #// @abstract
    #// 
    #// @param string $destfilename
    #// @param string $mime_type
    #// @return array|WP_Error {'path'=>string, 'file'=>string, 'width'=>int, 'height'=>int, 'mime-type'=>string}
    #//
    def save(self, destfilename_=None, mime_type_=None):
        if destfilename_ is None:
            destfilename_ = None
        # end if
        if mime_type_ is None:
            mime_type_ = None
        # end if
        
        pass
    # end def save
    #// 
    #// Resizes current image.
    #// 
    #// At minimum, either a height or width must be provided.
    #// If one of the two is set to null, the resize will
    #// maintain aspect ratio according to the provided dimension.
    #// 
    #// @since 3.5.0
    #// @abstract
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
        
        pass
    # end def resize
    #// 
    #// Resize multiple images from a single source.
    #// 
    #// @since 3.5.0
    #// @abstract
    #// 
    #// @param array $sizes {
    #// An array of image size arrays. Default sizes are 'small', 'medium', 'large'.
    #// 
    #// @type array $size {
    #// @type int  $width  Image width.
    #// @type int  $height Image height.
    #// @type bool $crop   Optional. Whether to crop the image. Default false.
    #// }
    #// }
    #// @return array An array of resized images metadata by size.
    #//
    def multi_resize(self, sizes_=None):
        
        
        pass
    # end def multi_resize
    #// 
    #// Crops Image.
    #// 
    #// @since 3.5.0
    #// @abstract
    #// 
    #// @param int $src_x The start x position to crop from.
    #// @param int $src_y The start y position to crop from.
    #// @param int $src_w The width to crop.
    #// @param int $src_h The height to crop.
    #// @param int $dst_w Optional. The destination width.
    #// @param int $dst_h Optional. The destination height.
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
        
        pass
    # end def crop
    #// 
    #// Rotates current image counter-clockwise by $angle.
    #// 
    #// @since 3.5.0
    #// @abstract
    #// 
    #// @param float $angle
    #// @return bool|WP_Error
    #//
    def rotate(self, angle_=None):
        
        
        pass
    # end def rotate
    #// 
    #// Flips current image.
    #// 
    #// @since 3.5.0
    #// @abstract
    #// 
    #// @param bool $horz Flip along Horizontal Axis
    #// @param bool $vert Flip along Vertical Axis
    #// @return bool|WP_Error
    #//
    def flip(self, horz_=None, vert_=None):
        
        
        pass
    # end def flip
    #// 
    #// Streams current image to browser.
    #// 
    #// @since 3.5.0
    #// @abstract
    #// 
    #// @param string $mime_type The mime type of the image.
    #// @return bool|WP_Error True on success, WP_Error object or false on failure.
    #//
    def stream(self, mime_type_=None):
        if mime_type_ is None:
            mime_type_ = None
        # end if
        
        pass
    # end def stream
    #// 
    #// Gets dimensions of image.
    #// 
    #// @since 3.5.0
    #// 
    #// @return array {
    #// Dimensions of the image.
    #// 
    #// @type int $width  The image width.
    #// @type int $height The image height.
    #// }
    #//
    def get_size(self):
        
        
        return self.size
    # end def get_size
    #// 
    #// Sets current image size.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int $width
    #// @param int $height
    #// @return true
    #//
    def update_size(self, width_=None, height_=None):
        if width_ is None:
            width_ = None
        # end if
        if height_ is None:
            height_ = None
        # end if
        
        self.size = Array({"width": php_int(width_), "height": php_int(height_)})
        return True
    # end def update_size
    #// 
    #// Gets the Image Compression quality on a 1-100% scale.
    #// 
    #// @since 4.0.0
    #// 
    #// @return int $quality Compression Quality. Range: [1,100]
    #//
    def get_quality(self):
        
        
        if (not self.quality):
            self.set_quality()
        # end if
        return self.quality
    # end def get_quality
    #// 
    #// Sets Image Compression quality on a 1-100% scale.
    #// 
    #// @since 3.5.0
    #// 
    #// @param int $quality Compression Quality. Range: [1,100]
    #// @return true|WP_Error True if set successfully; WP_Error on failure.
    #//
    def set_quality(self, quality_=None):
        if quality_ is None:
            quality_ = None
        # end if
        
        if None == quality_:
            #// 
            #// Filters the default image compression quality setting.
            #// 
            #// Applies only during initial editor instantiation, or when set_quality() is run
            #// manually without the `$quality` argument.
            #// 
            #// set_quality() has priority over the filter.
            #// 
            #// @since 3.5.0
            #// 
            #// @param int    $quality   Quality level between 1 (low) and 100 (high).
            #// @param string $mime_type Image mime type.
            #//
            quality_ = apply_filters("wp_editor_set_quality", self.default_quality, self.mime_type)
            if "image/jpeg" == self.mime_type:
                #// 
                #// Filters the JPEG compression quality for backward-compatibility.
                #// 
                #// Applies only during initial editor instantiation, or when set_quality() is run
                #// manually without the `$quality` argument.
                #// 
                #// set_quality() has priority over the filter.
                #// 
                #// The filter is evaluated under two contexts: 'image_resize', and 'edit_image',
                #// (when a JPEG image is saved to file).
                #// 
                #// @since 2.5.0
                #// 
                #// @param int    $quality Quality level between 0 (low) and 100 (high) of the JPEG.
                #// @param string $context Context of the filter.
                #//
                quality_ = apply_filters("jpeg_quality", quality_, "image_resize")
            # end if
            if quality_ < 0 or quality_ > 100:
                quality_ = self.default_quality
            # end if
        # end if
        #// Allow 0, but squash to 1 due to identical images in GD, and for backward compatibility.
        if 0 == quality_:
            quality_ = 1
        # end if
        if quality_ >= 1 and quality_ <= 100:
            self.quality = quality_
            return True
        else:
            return php_new_class("WP_Error", lambda : WP_Error("invalid_image_quality", __("Attempted to set image quality outside of the range [1,100].")))
        # end if
    # end def set_quality
    #// 
    #// Returns preferred mime-type and extension based on provided
    #// file's extension and mime, or current file's extension and mime.
    #// 
    #// Will default to $this->default_mime_type if requested is not supported.
    #// 
    #// Provides corrected filename only if filename is provided.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $filename
    #// @param string $mime_type
    #// @return array { filename|null, extension, mime-type }
    #//
    def get_output_format(self, filename_=None, mime_type_=None):
        if filename_ is None:
            filename_ = None
        # end if
        if mime_type_ is None:
            mime_type_ = None
        # end if
        
        new_ext_ = None
        #// By default, assume specified type takes priority.
        if mime_type_:
            new_ext_ = self.get_extension(mime_type_)
        # end if
        if filename_:
            file_ext_ = php_strtolower(pathinfo(filename_, PATHINFO_EXTENSION))
            file_mime_ = self.get_mime_type(file_ext_)
        else:
            #// If no file specified, grab editor's current extension and mime-type.
            file_ext_ = php_strtolower(pathinfo(self.file_, PATHINFO_EXTENSION))
            file_mime_ = self.mime_type
        # end if
        #// Check to see if specified mime-type is the same as type implied by
        #// file extension. If so, prefer extension from file.
        if (not mime_type_) or file_mime_ == mime_type_:
            mime_type_ = file_mime_
            new_ext_ = file_ext_
        # end if
        #// Double-check that the mime-type selected is supported by the editor.
        #// If not, choose a default instead.
        if (not self.supports_mime_type(mime_type_)):
            #// 
            #// Filters default mime type prior to getting the file extension.
            #// 
            #// @see wp_get_mime_types()
            #// 
            #// @since 3.5.0
            #// 
            #// @param string $mime_type Mime type string.
            #//
            mime_type_ = apply_filters("image_editor_default_mime_type", self.default_mime_type)
            new_ext_ = self.get_extension(mime_type_)
        # end if
        if filename_:
            dir_ = pathinfo(filename_, PATHINFO_DIRNAME)
            ext_ = pathinfo(filename_, PATHINFO_EXTENSION)
            filename_ = trailingslashit(dir_) + wp_basename(filename_, str(".") + str(ext_)) + str(".") + str(new_ext_)
        # end if
        return Array(filename_, new_ext_, mime_type_)
    # end def get_output_format
    #// 
    #// Builds an output filename based on current file, and adding proper suffix
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $suffix
    #// @param string $dest_path
    #// @param string $extension
    #// @return string filename
    #//
    def generate_filename(self, suffix_=None, dest_path_=None, extension_=None):
        if suffix_ is None:
            suffix_ = None
        # end if
        if dest_path_ is None:
            dest_path_ = None
        # end if
        if extension_ is None:
            extension_ = None
        # end if
        
        #// $suffix will be appended to the destination filename, just before the extension.
        if (not suffix_):
            suffix_ = self.get_suffix()
        # end if
        dir_ = pathinfo(self.file_, PATHINFO_DIRNAME)
        ext_ = pathinfo(self.file_, PATHINFO_EXTENSION)
        name_ = wp_basename(self.file_, str(".") + str(ext_))
        new_ext_ = php_strtolower(extension_ if extension_ else ext_)
        if (not php_is_null(dest_path_)):
            _dest_path_ = php_realpath(dest_path_)
            if _dest_path_:
                dir_ = _dest_path_
            # end if
        # end if
        return trailingslashit(dir_) + str(name_) + str("-") + str(suffix_) + str(".") + str(new_ext_)
    # end def generate_filename
    #// 
    #// Builds and returns proper suffix for file based on height and width.
    #// 
    #// @since 3.5.0
    #// 
    #// @return string|false suffix
    #//
    def get_suffix(self):
        
        
        if (not self.get_size()):
            return False
        # end if
        return str(self.size["width"]) + str("x") + str(self.size["height"])
    # end def get_suffix
    #// 
    #// Check if a JPEG image has EXIF Orientation tag and rotate it if needed.
    #// 
    #// @since 5.3.0
    #// 
    #// @return bool|WP_Error True if the image was rotated. False if not rotated (no EXIF data or the image doesn't need to be rotated).
    #// WP_Error if error while rotating.
    #//
    def maybe_exif_rotate(self):
        
        
        orientation_ = None
        if php_is_callable("exif_read_data") and "image/jpeg" == self.mime_type:
            exif_data_ = php_no_error(lambda: exif_read_data(self.file_))
            if (not php_empty(lambda : exif_data_["Orientation"])):
                orientation_ = php_int(exif_data_["Orientation"])
            # end if
        # end if
        #// 
        #// Filters the `$orientation` value to correct it before rotating or to prevemnt rotating the image.
        #// 
        #// @since 5.3.0
        #// 
        #// @param int    $orientation EXIF Orientation value as retrieved from the image file.
        #// @param string $file        Path to the image file.
        #//
        orientation_ = apply_filters("wp_image_maybe_exif_rotate", orientation_, self.file_)
        if (not orientation_) or 1 == orientation_:
            return False
        # end if
        for case in Switch(orientation_):
            if case(2):
                #// Flip horizontally.
                result_ = self.flip(True, False)
                break
            # end if
            if case(3):
                #// Rotate 180 degrees or flip horizontally and vertically.
                #// Flipping seems faster and uses less resources.
                result_ = self.flip(True, True)
                break
            # end if
            if case(4):
                #// Flip vertically.
                result_ = self.flip(False, True)
                break
            # end if
            if case(5):
                #// Rotate 90 degrees counter-clockwise and flip vertically.
                result_ = self.rotate(90)
                if (not is_wp_error(result_)):
                    result_ = self.flip(False, True)
                # end if
                break
            # end if
            if case(6):
                #// Rotate 90 degrees clockwise (270 counter-clockwise).
                result_ = self.rotate(270)
                break
            # end if
            if case(7):
                #// Rotate 90 degrees counter-clockwise and flip horizontally.
                result_ = self.rotate(90)
                if (not is_wp_error(result_)):
                    result_ = self.flip(True, False)
                # end if
                break
            # end if
            if case(8):
                #// Rotate 90 degrees counter-clockwise.
                result_ = self.rotate(90)
                break
            # end if
        # end for
        return result_
    # end def maybe_exif_rotate
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
        
        
        stream_ = wp_is_stream(filename_)
        if stream_:
            ob_start()
        else:
            #// The directory containing the original file may no longer exist when using a replication plugin.
            wp_mkdir_p(php_dirname(filename_))
        # end if
        result_ = call_user_func_array(function_, arguments_)
        if result_ and stream_:
            contents_ = ob_get_contents()
            fp_ = fopen(filename_, "w")
            if (not fp_):
                ob_end_clean()
                return False
            # end if
            fwrite(fp_, contents_)
            php_fclose(fp_)
        # end if
        if stream_:
            ob_end_clean()
        # end if
        return result_
    # end def make_image
    #// 
    #// Returns first matched mime-type from extension,
    #// as mapped from wp_get_mime_types()
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $extension
    #// @return string|false
    #//
    def get_mime_type(self, extension_=None):
        if extension_ is None:
            extension_ = None
        # end if
        
        if (not extension_):
            return False
        # end if
        mime_types_ = wp_get_mime_types()
        extensions_ = php_array_keys(mime_types_)
        for _extension_ in extensions_:
            if php_preg_match(str("/") + str(extension_) + str("/i"), _extension_):
                return mime_types_[_extension_]
            # end if
        # end for
        return False
    # end def get_mime_type
    #// 
    #// Returns first matched extension from Mime-type,
    #// as mapped from wp_get_mime_types()
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $mime_type
    #// @return string|false
    #//
    def get_extension(self, mime_type_=None):
        if mime_type_ is None:
            mime_type_ = None
        # end if
        
        extensions_ = php_explode("|", php_array_search(mime_type_, wp_get_mime_types()))
        if php_empty(lambda : extensions_[0]):
            return False
        # end if
        return extensions_[0]
    # end def get_extension
# end class WP_Image_Editor
