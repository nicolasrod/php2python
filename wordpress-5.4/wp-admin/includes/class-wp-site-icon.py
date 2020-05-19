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
#// Administration API: WP_Site_Icon class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.3.0
#// 
#// 
#// Core class used to implement site icon functionality.
#// 
#// @since 4.3.0
#//
class WP_Site_Icon():
    #// 
    #// The minimum size of the site icon.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    min_size = 512
    #// 
    #// The size to which to crop the image so that we can display it in the UI nicely.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    page_crop = 512
    #// 
    #// List of site icon sizes.
    #// 
    #// @since 4.3.0
    #// @var int[]
    #//
    site_icon_sizes = Array(270, 192, 180, 32)
    #// 
    #// Registers actions and filters.
    #// 
    #// @since 4.3.0
    #//
    def __init__(self):
        
        
        add_action("delete_attachment", Array(self, "delete_attachment_data"))
        add_filter("get_post_metadata", Array(self, "get_post_metadata"), 10, 4)
    # end def __init__
    #// 
    #// Creates an attachment 'object'.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string $cropped              Cropped image URL.
    #// @param int    $parent_attachment_id Attachment ID of parent image.
    #// @return array Attachment object.
    #//
    def create_attachment_object(self, cropped_=None, parent_attachment_id_=None):
        
        
        parent_ = get_post(parent_attachment_id_)
        parent_url_ = wp_get_attachment_url(parent_.ID)
        url_ = php_str_replace(wp_basename(parent_url_), wp_basename(cropped_), parent_url_)
        size_ = php_no_error(lambda: getimagesize(cropped_))
        image_type_ = size_["mime"] if size_ else "image/jpeg"
        object_ = Array({"ID": parent_attachment_id_, "post_title": wp_basename(cropped_), "post_content": url_, "post_mime_type": image_type_, "guid": url_, "context": "site-icon"})
        return object_
    # end def create_attachment_object
    #// 
    #// Inserts an attachment.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array  $object Attachment object.
    #// @param string $file   File path of the attached image.
    #// @return int           Attachment ID
    #//
    def insert_attachment(self, object_=None, file_=None):
        
        
        attachment_id_ = wp_insert_attachment(object_, file_)
        metadata_ = wp_generate_attachment_metadata(attachment_id_, file_)
        #// 
        #// Filters the site icon attachment metadata.
        #// 
        #// @since 4.3.0
        #// 
        #// @see wp_generate_attachment_metadata()
        #// 
        #// @param array $metadata Attachment metadata.
        #//
        metadata_ = apply_filters("site_icon_attachment_metadata", metadata_)
        wp_update_attachment_metadata(attachment_id_, metadata_)
        return attachment_id_
    # end def insert_attachment
    #// 
    #// Adds additional sizes to be made when creating the site icon images.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array[] $sizes Array of arrays containing information for additional sizes.
    #// @return array[] Array of arrays containing additional image sizes.
    #//
    def additional_sizes(self, sizes_=None):
        if sizes_ is None:
            sizes_ = Array()
        # end if
        
        only_crop_sizes_ = Array()
        #// 
        #// Filters the different dimensions that a site icon is saved in.
        #// 
        #// @since 4.3.0
        #// 
        #// @param int[] $site_icon_sizes Array of sizes available for the Site Icon.
        #//
        self.site_icon_sizes = apply_filters("site_icon_image_sizes", self.site_icon_sizes)
        #// Use a natural sort of numbers.
        natsort(self.site_icon_sizes)
        self.site_icon_sizes = php_array_reverse(self.site_icon_sizes)
        #// Ensure that we only resize the image into sizes that allow cropping.
        for name_,size_array_ in sizes_.items():
            if (php_isset(lambda : size_array_["crop"])):
                only_crop_sizes_[name_] = size_array_
            # end if
        # end for
        for size_ in self.site_icon_sizes:
            if size_ < self.min_size:
                only_crop_sizes_["site_icon-" + size_] = Array({"width ": size_, "height": size_, "crop": True})
            # end if
        # end for
        return only_crop_sizes_
    # end def additional_sizes
    #// 
    #// Adds Site Icon sizes to the array of image sizes on demand.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string[] $sizes Array of image size names.
    #// @return string[] Array of image size names.
    #//
    def intermediate_image_sizes(self, sizes_=None):
        if sizes_ is None:
            sizes_ = Array()
        # end if
        
        #// This filter is documented in wp-admin/includes/class-wp-site-icon.php
        self.site_icon_sizes = apply_filters("site_icon_image_sizes", self.site_icon_sizes)
        for size_ in self.site_icon_sizes:
            sizes_[-1] = "site_icon-" + size_
        # end for
        return sizes_
    # end def intermediate_image_sizes
    #// 
    #// Deletes the Site Icon when the image file is deleted.
    #// 
    #// @since 4.3.0
    #// 
    #// @param int $post_id Attachment ID.
    #//
    def delete_attachment_data(self, post_id_=None):
        
        
        site_icon_id_ = get_option("site_icon")
        if site_icon_id_ and post_id_ == site_icon_id_:
            delete_option("site_icon")
        # end if
    # end def delete_attachment_data
    #// 
    #// Adds custom image sizes when meta data for an image is requested, that happens to be used as Site Icon.
    #// 
    #// @since 4.3.0
    #// 
    #// @param null|array|string $value    The value get_metadata() should return a single metadata value, or an
    #// array of values.
    #// @param int               $post_id  Post ID.
    #// @param string            $meta_key Meta key.
    #// @param string|array      $single   Meta value, or an array of values.
    #// @return array|null|string The attachment metadata value, array of values, or null.
    #//
    def get_post_metadata(self, value_=None, post_id_=None, meta_key_=None, single_=None):
        
        
        if single_ and "_wp_attachment_backup_sizes" == meta_key_:
            site_icon_id_ = get_option("site_icon")
            if post_id_ == site_icon_id_:
                add_filter("intermediate_image_sizes", Array(self, "intermediate_image_sizes"))
            # end if
        # end if
        return value_
    # end def get_post_metadata
# end class WP_Site_Icon
