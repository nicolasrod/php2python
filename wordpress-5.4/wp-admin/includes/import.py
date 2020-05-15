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
def get_importers(*args_):
    
    global wp_importers
    php_check_if_defined("wp_importers")
    if php_is_array(wp_importers):
        uasort(wp_importers, "_usort_by_first_member")
    # end if
    return wp_importers
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
def _usort_by_first_member(a=None, b=None, *args_):
    
    return strnatcasecmp(a[0], b[0])
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
def register_importer(id=None, name=None, description=None, callback=None, *args_):
    
    global wp_importers
    php_check_if_defined("wp_importers")
    if is_wp_error(callback):
        return callback
    # end if
    wp_importers[id] = Array(name, description, callback)
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
def wp_import_cleanup(id=None, *args_):
    
    wp_delete_attachment(id)
# end def wp_import_cleanup
#// 
#// Handle importer uploading and add attachment.
#// 
#// @since 2.0.0
#// 
#// @return array Uploaded file's details on success, error message on failure
#//
def wp_import_handle_upload(*args_):
    
    if (not (php_isset(lambda : PHP_FILES["import"]))):
        return Array({"error": php_sprintf(__("File is empty. Please upload something more substantial. This error could also be caused by uploads being disabled in your %1$s file or by %2$s being defined as smaller than %3$s in %1$s."), "php.ini", "post_max_size", "upload_max_filesize")})
    # end if
    overrides = Array({"test_form": False, "test_type": False})
    PHP_FILES["import"]["name"] += ".txt"
    upload = wp_handle_upload(PHP_FILES["import"], overrides)
    if (php_isset(lambda : upload["error"])):
        return upload
    # end if
    #// Construct the object array.
    object = Array({"post_title": wp_basename(upload["file"]), "post_content": upload["url"], "post_mime_type": upload["type"], "guid": upload["url"], "context": "import", "post_status": "private"})
    #// Save the data.
    id = wp_insert_attachment(object, upload["file"])
    #// 
    #// Schedule a cleanup for one day from now in case of failed
    #// import or missing wp_import_cleanup() call.
    #//
    wp_schedule_single_event(time() + DAY_IN_SECONDS, "importer_scheduled_cleanup", Array(id))
    return Array({"file": upload["file"], "id": id})
# end def wp_import_handle_upload
#// 
#// Returns a list from WordPress.org of popular importer plugins.
#// 
#// @since 3.5.0
#// 
#// @return array Importers with metadata for each.
#//
def wp_get_popular_importers(*args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    locale = get_user_locale()
    cache_key = "popular_importers_" + php_md5(locale + wp_version)
    popular_importers = get_site_transient(cache_key)
    if (not popular_importers):
        url = add_query_arg(Array({"locale": locale, "version": wp_version}), "http://api.wordpress.org/core/importers/1.1/")
        options = Array({"user-agent": "WordPress/" + wp_version + "; " + home_url("/")})
        if wp_http_supports(Array("ssl")):
            url = set_url_scheme(url, "https")
        # end if
        response = wp_remote_get(url, options)
        popular_importers = php_json_decode(wp_remote_retrieve_body(response), True)
        if php_is_array(popular_importers):
            set_site_transient(cache_key, popular_importers, 2 * DAY_IN_SECONDS)
        else:
            popular_importers = False
        # end if
    # end if
    if php_is_array(popular_importers):
        #// If the data was received as translated, return it as-is.
        if popular_importers["translated"]:
            return popular_importers["importers"]
        # end if
        for importer in popular_importers["importers"]:
            #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
            importer["description"] = translate(importer["description"])
            if "WordPress" != importer["name"]:
                #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
                importer["name"] = translate(importer["name"])
            # end if
        # end for
        return popular_importers["importers"]
    # end if
    return Array({"blogger": Array({"name": __("Blogger"), "description": __("Import posts, comments, and users from a Blogger blog."), "plugin-slug": "blogger-importer", "importer-id": "blogger"})}, {"wpcat2tag": Array({"name": __("Categories and Tags Converter"), "description": __("Convert existing categories to tags or tags to categories, selectively."), "plugin-slug": "wpcat2tag-importer", "importer-id": "wp-cat2tag"})}, {"livejournal": Array({"name": __("LiveJournal"), "description": __("Import posts from LiveJournal using their API."), "plugin-slug": "livejournal-importer", "importer-id": "livejournal"})}, {"movabletype": Array({"name": __("Movable Type and TypePad"), "description": __("Import posts and comments from a Movable Type or TypePad blog."), "plugin-slug": "movabletype-importer", "importer-id": "mt"})}, {"rss": Array({"name": __("RSS"), "description": __("Import posts from an RSS feed."), "plugin-slug": "rss-importer", "importer-id": "rss"})}, {"tumblr": Array({"name": __("Tumblr"), "description": __("Import posts &amp; media from Tumblr using their API."), "plugin-slug": "tumblr-importer", "importer-id": "tumblr"})}, {"wordpress": Array({"name": "WordPress", "description": __("Import posts, pages, comments, custom fields, categories, and tags from a WordPress export file."), "plugin-slug": "wordpress-importer", "importer-id": "wordpress"})})
# end def wp_get_popular_importers
