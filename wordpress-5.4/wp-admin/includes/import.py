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
#// WordPress Administration Importer API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Retrieve list of importers.
#// 
#// @since 2.0.0
#// 
#// @global array $wp_importers
#// @return array
#//
def get_importers(*_args_):
    
    
    global wp_importers_
    php_check_if_defined("wp_importers_")
    if php_is_array(wp_importers_):
        uasort(wp_importers_, "_usort_by_first_member")
    # end if
    return wp_importers_
# end def get_importers
#// 
#// Sorts a multidimensional array by first member of each top level member
#// 
#// Used by uasort() as a callback, should not be used directly.
#// 
#// @since 2.9.0
#// @access private
#// 
#// @param array $a
#// @param array $b
#// @return int
#//
def _usort_by_first_member(a_=None, b_=None, *_args_):
    
    
    return strnatcasecmp(a_[0], b_[0])
# end def _usort_by_first_member
#// 
#// Register importer for WordPress.
#// 
#// @since 2.0.0
#// 
#// @global array $wp_importers
#// 
#// @param string   $id          Importer tag. Used to uniquely identify importer.
#// @param string   $name        Importer name and title.
#// @param string   $description Importer description.
#// @param callable $callback    Callback to run.
#// @return WP_Error Returns WP_Error when $callback is WP_Error.
#//
def register_importer(id_=None, name_=None, description_=None, callback_=None, *_args_):
    
    
    global wp_importers_
    php_check_if_defined("wp_importers_")
    if is_wp_error(callback_):
        return callback_
    # end if
    wp_importers_[id_] = Array(name_, description_, callback_)
# end def register_importer
#// 
#// Cleanup importer.
#// 
#// Removes attachment based on ID.
#// 
#// @since 2.0.0
#// 
#// @param string $id Importer ID.
#//
def wp_import_cleanup(id_=None, *_args_):
    
    
    wp_delete_attachment(id_)
# end def wp_import_cleanup
#// 
#// Handle importer uploading and add attachment.
#// 
#// @since 2.0.0
#// 
#// @return array Uploaded file's details on success, error message on failure
#//
def wp_import_handle_upload(*_args_):
    
    
    if (not (php_isset(lambda : PHP_FILES["import"]))):
        return Array({"error": php_sprintf(__("File is empty. Please upload something more substantial. This error could also be caused by uploads being disabled in your %1$s file or by %2$s being defined as smaller than %3$s in %1$s."), "php.ini", "post_max_size", "upload_max_filesize")})
    # end if
    overrides_ = Array({"test_form": False, "test_type": False})
    PHP_FILES["import"]["name"] += ".txt"
    upload_ = wp_handle_upload(PHP_FILES["import"], overrides_)
    if (php_isset(lambda : upload_["error"])):
        return upload_
    # end if
    #// Construct the object array.
    object_ = Array({"post_title": wp_basename(upload_["file"]), "post_content": upload_["url"], "post_mime_type": upload_["type"], "guid": upload_["url"], "context": "import", "post_status": "private"})
    #// Save the data.
    id_ = wp_insert_attachment(object_, upload_["file"])
    #// 
    #// Schedule a cleanup for one day from now in case of failed
    #// import or missing wp_import_cleanup() call.
    #//
    wp_schedule_single_event(time() + DAY_IN_SECONDS, "importer_scheduled_cleanup", Array(id_))
    return Array({"file": upload_["file"], "id": id_})
# end def wp_import_handle_upload
#// 
#// Returns a list from WordPress.org of popular importer plugins.
#// 
#// @since 3.5.0
#// 
#// @return array Importers with metadata for each.
#//
def wp_get_popular_importers(*_args_):
    
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    locale_ = get_user_locale()
    cache_key_ = "popular_importers_" + php_md5(locale_ + wp_version_)
    popular_importers_ = get_site_transient(cache_key_)
    if (not popular_importers_):
        url_ = add_query_arg(Array({"locale": locale_, "version": wp_version_}), "http://api.wordpress.org/core/importers/1.1/")
        options_ = Array({"user-agent": "WordPress/" + wp_version_ + "; " + home_url("/")})
        if wp_http_supports(Array("ssl")):
            url_ = set_url_scheme(url_, "https")
        # end if
        response_ = wp_remote_get(url_, options_)
        popular_importers_ = php_json_decode(wp_remote_retrieve_body(response_), True)
        if php_is_array(popular_importers_):
            set_site_transient(cache_key_, popular_importers_, 2 * DAY_IN_SECONDS)
        else:
            popular_importers_ = False
        # end if
    # end if
    if php_is_array(popular_importers_):
        #// If the data was received as translated, return it as-is.
        if popular_importers_["translated"]:
            return popular_importers_["importers"]
        # end if
        for importer_ in popular_importers_["importers"]:
            #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
            importer_["description"] = translate(importer_["description"])
            if "WordPress" != importer_["name"]:
                #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
                importer_["name"] = translate(importer_["name"])
            # end if
        # end for
        return popular_importers_["importers"]
    # end if
    return Array({"blogger": Array({"name": __("Blogger"), "description": __("Import posts, comments, and users from a Blogger blog."), "plugin-slug": "blogger-importer", "importer-id": "blogger"})}, {"wpcat2tag": Array({"name": __("Categories and Tags Converter"), "description": __("Convert existing categories to tags or tags to categories, selectively."), "plugin-slug": "wpcat2tag-importer", "importer-id": "wp-cat2tag"})}, {"livejournal": Array({"name": __("LiveJournal"), "description": __("Import posts from LiveJournal using their API."), "plugin-slug": "livejournal-importer", "importer-id": "livejournal"})}, {"movabletype": Array({"name": __("Movable Type and TypePad"), "description": __("Import posts and comments from a Movable Type or TypePad blog."), "plugin-slug": "movabletype-importer", "importer-id": "mt"})}, {"rss": Array({"name": __("RSS"), "description": __("Import posts from an RSS feed."), "plugin-slug": "rss-importer", "importer-id": "rss"})}, {"tumblr": Array({"name": __("Tumblr"), "description": __("Import posts &amp; media from Tumblr using their API."), "plugin-slug": "tumblr-importer", "importer-id": "tumblr"})}, {"wordpress": Array({"name": "WordPress", "description": __("Import posts, pages, comments, custom fields, categories, and tags from a WordPress export file."), "plugin-slug": "wordpress-importer", "importer-id": "wordpress"})})
# end def wp_get_popular_importers
