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
    file = None
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
    def __init__(self, file=None):
        
        self.file = file
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
    def test(self, args=Array()):
        
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
    def supports_mime_type(self, mime_type=None):
        
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
    def save(self, destfilename=None, mime_type=None):
        
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
    def resize(self, max_w=None, max_h=None, crop=False):
        
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
    def multi_resize(self, sizes=None):
        
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
    def crop(self, src_x=None, src_y=None, src_w=None, src_h=None, dst_w=None, dst_h=None, src_abs=False):
        
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
    def rotate(self, angle=None):
        
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
    def flip(self, horz=None, vert=None):
        
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
    def stream(self, mime_type=None):
        
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
    def update_size(self, width=None, height=None):
        
        self.size = Array({"width": php_int(width), "height": php_int(height)})
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
    def set_quality(self, quality=None):
        
        if None == quality:
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
            quality = apply_filters("wp_editor_set_quality", self.default_quality, self.mime_type)
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
                quality = apply_filters("jpeg_quality", quality, "image_resize")
            # end if
            if quality < 0 or quality > 100:
                quality = self.default_quality
            # end if
        # end if
        #// Allow 0, but squash to 1 due to identical images in GD, and for backward compatibility.
        if 0 == quality:
            quality = 1
        # end if
        if quality >= 1 and quality <= 100:
            self.quality = quality
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
    def get_output_format(self, filename=None, mime_type=None):
        
        new_ext = None
        #// By default, assume specified type takes priority.
        if mime_type:
            new_ext = self.get_extension(mime_type)
        # end if
        if filename:
            file_ext = php_strtolower(pathinfo(filename, PATHINFO_EXTENSION))
            file_mime = self.get_mime_type(file_ext)
        else:
            #// If no file specified, grab editor's current extension and mime-type.
            file_ext = php_strtolower(pathinfo(self.file, PATHINFO_EXTENSION))
            file_mime = self.mime_type
        # end if
        #// Check to see if specified mime-type is the same as type implied by
        #// file extension. If so, prefer extension from file.
        if (not mime_type) or file_mime == mime_type:
            mime_type = file_mime
            new_ext = file_ext
        # end if
        #// Double-check that the mime-type selected is supported by the editor.
        #// If not, choose a default instead.
        if (not self.supports_mime_type(mime_type)):
            #// 
            #// Filters default mime type prior to getting the file extension.
            #// 
            #// @see wp_get_mime_types()
            #// 
            #// @since 3.5.0
            #// 
            #// @param string $mime_type Mime type string.
            #//
            mime_type = apply_filters("image_editor_default_mime_type", self.default_mime_type)
            new_ext = self.get_extension(mime_type)
        # end if
        if filename:
            dir = pathinfo(filename, PATHINFO_DIRNAME)
            ext = pathinfo(filename, PATHINFO_EXTENSION)
            filename = trailingslashit(dir) + wp_basename(filename, str(".") + str(ext)) + str(".") + str(new_ext)
        # end if
        return Array(filename, new_ext, mime_type)
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
    def generate_filename(self, suffix=None, dest_path=None, extension=None):
        
        #// $suffix will be appended to the destination filename, just before the extension.
        if (not suffix):
            suffix = self.get_suffix()
        # end if
        dir = pathinfo(self.file, PATHINFO_DIRNAME)
        ext = pathinfo(self.file, PATHINFO_EXTENSION)
        name = wp_basename(self.file, str(".") + str(ext))
        new_ext = php_strtolower(extension if extension else ext)
        if (not is_null(dest_path)):
            _dest_path = php_realpath(dest_path)
            if _dest_path:
                dir = _dest_path
            # end if
        # end if
        return trailingslashit(dir) + str(name) + str("-") + str(suffix) + str(".") + str(new_ext)
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
        
        orientation = None
        if php_is_callable("exif_read_data") and "image/jpeg" == self.mime_type:
            exif_data = php_no_error(lambda: exif_read_data(self.file))
            if (not php_empty(lambda : exif_data["Orientation"])):
                orientation = php_int(exif_data["Orientation"])
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
        orientation = apply_filters("wp_image_maybe_exif_rotate", orientation, self.file)
        if (not orientation) or 1 == orientation:
            return False
        # end if
        for case in Switch(orientation):
            if case(2):
                #// Flip horizontally.
                result = self.flip(True, False)
                break
            # end if
            if case(3):
                #// Rotate 180 degrees or flip horizontally and vertically.
                #// Flipping seems faster and uses less resources.
                result = self.flip(True, True)
                break
            # end if
            if case(4):
                #// Flip vertically.
                result = self.flip(False, True)
                break
            # end if
            if case(5):
                #// Rotate 90 degrees counter-clockwise and flip vertically.
                result = self.rotate(90)
                if (not is_wp_error(result)):
                    result = self.flip(False, True)
                # end if
                break
            # end if
            if case(6):
                #// Rotate 90 degrees clockwise (270 counter-clockwise).
                result = self.rotate(270)
                break
            # end if
            if case(7):
                #// Rotate 90 degrees counter-clockwise and flip horizontally.
                result = self.rotate(90)
                if (not is_wp_error(result)):
                    result = self.flip(True, False)
                # end if
                break
            # end if
            if case(8):
                #// Rotate 90 degrees counter-clockwise.
                result = self.rotate(90)
                break
            # end if
        # end for
        return result
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
    def make_image(self, filename=None, function=None, arguments=None):
        
        stream = wp_is_stream(filename)
        if stream:
            ob_start()
        else:
            #// The directory containing the original file may no longer exist when using a replication plugin.
            wp_mkdir_p(php_dirname(filename))
        # end if
        result = call_user_func_array(function, arguments)
        if result and stream:
            contents = ob_get_contents()
            fp = fopen(filename, "w")
            if (not fp):
                ob_end_clean()
                return False
            # end if
            fwrite(fp, contents)
            php_fclose(fp)
        # end if
        if stream:
            ob_end_clean()
        # end if
        return result
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
    def get_mime_type(self, extension=None):
        
        if (not extension):
            return False
        # end if
        mime_types = wp_get_mime_types()
        extensions = php_array_keys(mime_types)
        for _extension in extensions:
            if php_preg_match(str("/") + str(extension) + str("/i"), _extension):
                return mime_types[_extension]
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
    def get_extension(self, mime_type=None):
        
        extensions = php_explode("|", php_array_search(mime_type, wp_get_mime_types()))
        if php_empty(lambda : extensions[0]):
            return False
        # end if
        return extensions[0]
    # end def get_extension
# end class WP_Image_Editor
