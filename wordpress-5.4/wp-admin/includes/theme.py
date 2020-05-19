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
#// WordPress Theme Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Remove a theme
#// 
#// @since 2.8.0
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param string $stylesheet Stylesheet of the theme to delete.
#// @param string $redirect   Redirect to page when complete.
#// @return bool|null|WP_Error True on success, false if `$stylesheet` is empty, WP_Error on failure.
#// Null if filesystem credentials are required to proceed.
#//
def delete_theme(stylesheet_=None, redirect_="", *_args_):
    
    
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    if php_empty(lambda : stylesheet_):
        return False
    # end if
    if php_empty(lambda : redirect_):
        redirect_ = wp_nonce_url("themes.php?action=delete&stylesheet=" + urlencode(stylesheet_), "delete-theme_" + stylesheet_)
    # end if
    ob_start()
    credentials_ = request_filesystem_credentials(redirect_)
    data_ = ob_get_clean()
    if False == credentials_:
        if (not php_empty(lambda : data_)):
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print(data_)
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        return
    # end if
    if (not WP_Filesystem(credentials_)):
        ob_start()
        #// Failed to connect. Error and request again.
        request_filesystem_credentials(redirect_, "", True)
        data_ = ob_get_clean()
        if (not php_empty(lambda : data_)):
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print(data_)
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        return
    # end if
    if (not php_is_object(wp_filesystem_)):
        return php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", __("Could not access filesystem.")))
    # end if
    if is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
        return php_new_class("WP_Error", lambda : WP_Error("fs_error", __("Filesystem error."), wp_filesystem_.errors))
    # end if
    #// Get the base plugin folder.
    themes_dir_ = wp_filesystem_.wp_themes_dir()
    if php_empty(lambda : themes_dir_):
        return php_new_class("WP_Error", lambda : WP_Error("fs_no_themes_dir", __("Unable to locate WordPress theme directory.")))
    # end if
    themes_dir_ = trailingslashit(themes_dir_)
    theme_dir_ = trailingslashit(themes_dir_ + stylesheet_)
    deleted_ = wp_filesystem_.delete(theme_dir_, True)
    if (not deleted_):
        return php_new_class("WP_Error", lambda : WP_Error("could_not_remove_theme", php_sprintf(__("Could not fully remove the theme %s."), stylesheet_)))
    # end if
    theme_translations_ = wp_get_installed_translations("themes")
    #// Remove language files, silently.
    if (not php_empty(lambda : theme_translations_[stylesheet_])):
        translations_ = theme_translations_[stylesheet_]
        for translation_,data_ in translations_.items():
            wp_filesystem_.delete(WP_LANG_DIR + "/themes/" + stylesheet_ + "-" + translation_ + ".po")
            wp_filesystem_.delete(WP_LANG_DIR + "/themes/" + stylesheet_ + "-" + translation_ + ".mo")
            json_translation_files_ = glob(WP_LANG_DIR + "/themes/" + stylesheet_ + "-" + translation_ + "-*.json")
            if json_translation_files_:
                php_array_map(Array(wp_filesystem_, "delete"), json_translation_files_)
            # end if
        # end for
    # end if
    #// Remove the theme from allowed themes on the network.
    if is_multisite():
        WP_Theme.network_disable_theme(stylesheet_)
    # end if
    #// Force refresh of theme update information.
    delete_site_transient("update_themes")
    return True
# end def delete_theme
#// 
#// Gets the page templates available in this theme.
#// 
#// @since 1.5.0
#// @since 4.7.0 Added the `$post_type` parameter.
#// 
#// @param WP_Post|null $post      Optional. The post being edited, provided for context.
#// @param string       $post_type Optional. Post type to get the templates for. Default 'page'.
#// @return string[] Array of template file names keyed by the template header name.
#//
def get_page_templates(post_=None, post_type_="page", *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    return php_array_flip(wp_get_theme().get_page_templates(post_, post_type_))
# end def get_page_templates
#// 
#// Tidies a filename for url display by the theme editor.
#// 
#// @since 2.9.0
#// @access private
#// 
#// @param string $fullpath Full path to the theme file
#// @param string $containingfolder Path of the theme parent folder
#// @return string
#//
def _get_template_edit_filename(fullpath_=None, containingfolder_=None, *_args_):
    
    
    return php_str_replace(php_dirname(php_dirname(containingfolder_)), "", fullpath_)
# end def _get_template_edit_filename
#// 
#// Check if there is an update for a theme available.
#// 
#// Will display link, if there is an update available.
#// 
#// @since 2.7.0
#// @see get_theme_update_available()
#// 
#// @param WP_Theme $theme Theme data object.
#//
def theme_update_available(theme_=None, *_args_):
    
    
    php_print(get_theme_update_available(theme_))
# end def theme_update_available
#// 
#// Retrieve the update link if there is a theme update available.
#// 
#// Will return a link if there is an update available.
#// 
#// @since 3.8.0
#// 
#// @staticvar object $themes_update
#// 
#// @param WP_Theme $theme WP_Theme object.
#// @return string|false HTML for the update link, or false if invalid info was passed.
#//
def get_theme_update_available(theme_=None, *_args_):
    
    
    themes_update_ = None
    if (not current_user_can("update_themes")):
        return False
    # end if
    if (not (php_isset(lambda : themes_update_))):
        themes_update_ = get_site_transient("update_themes")
    # end if
    if (not type(theme_).__name__ == "WP_Theme"):
        return False
    # end if
    stylesheet_ = theme_.get_stylesheet()
    html_ = ""
    if (php_isset(lambda : themes_update_.response[stylesheet_])):
        update_ = themes_update_.response[stylesheet_]
        theme_name_ = theme_.display("Name")
        details_url_ = add_query_arg(Array({"TB_iframe": "true", "width": 1024, "height": 800}), update_["url"])
        #// Theme browser inside WP? Replace this. Also, theme preview JS will override this on the available list.
        update_url_ = wp_nonce_url(admin_url("update.php?action=upgrade-theme&amp;theme=" + urlencode(stylesheet_)), "upgrade-theme_" + stylesheet_)
        if (not is_multisite()):
            if (not current_user_can("update_themes")):
                html_ = php_sprintf("<p><strong>" + __("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>.") + "</strong></p>", theme_name_, esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_name_, update_["new_version"]))), update_["new_version"])
            elif php_empty(lambda : update_["package"]):
                html_ = php_sprintf("<p><strong>" + __("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>. <em>Automatic update is unavailable for this theme.</em>") + "</strong></p>", theme_name_, esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_name_, update_["new_version"]))), update_["new_version"])
            else:
                html_ = php_sprintf("<p><strong>" + __("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\" %6$s>update now</a>.") + "</strong></p>", theme_name_, esc_url(details_url_), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_name_, update_["new_version"]))), update_["new_version"], update_url_, php_sprintf("aria-label=\"%s\" id=\"update-theme\" data-slug=\"%s\"", esc_attr(php_sprintf(__("Update %s now"), theme_name_)), stylesheet_))
            # end if
        # end if
    # end if
    return html_
# end def get_theme_update_available
#// 
#// Retrieve list of WordPress theme features (aka theme tags).
#// 
#// @since 3.1.0
#// 
#// @param bool $api Optional. Whether try to fetch tags from the WordPress.org API. Defaults to true.
#// @return array Array of features keyed by category with translations keyed by slug.
#//
def get_theme_feature_list(api_=None, *_args_):
    if api_ is None:
        api_ = True
    # end if
    
    #// Hard-coded list is used if API is not accessible.
    features_ = Array({__("Subject"): Array({"blog": __("Blog"), "e-commerce": __("E-Commerce"), "education": __("Education"), "entertainment": __("Entertainment"), "food-and-drink": __("Food & Drink"), "holiday": __("Holiday"), "news": __("News"), "photography": __("Photography"), "portfolio": __("Portfolio")})}, {__("Features"): Array({"accessibility-ready": __("Accessibility Ready"), "custom-background": __("Custom Background"), "custom-colors": __("Custom Colors"), "custom-header": __("Custom Header"), "custom-logo": __("Custom Logo"), "editor-style": __("Editor Style"), "featured-image-header": __("Featured Image Header"), "featured-images": __("Featured Images"), "footer-widgets": __("Footer Widgets"), "full-width-template": __("Full Width Template"), "post-formats": __("Post Formats"), "sticky-post": __("Sticky Post"), "theme-options": __("Theme Options")})}, {__("Layout"): Array({"grid-layout": __("Grid Layout"), "one-column": __("One Column"), "two-columns": __("Two Columns"), "three-columns": __("Three Columns"), "four-columns": __("Four Columns"), "left-sidebar": __("Left Sidebar"), "right-sidebar": __("Right Sidebar")})})
    if (not api_) or (not current_user_can("install_themes")):
        return features_
    # end if
    feature_list_ = get_site_transient("wporg_theme_feature_list")
    if (not feature_list_):
        set_site_transient("wporg_theme_feature_list", Array(), 3 * HOUR_IN_SECONDS)
    # end if
    if (not feature_list_):
        feature_list_ = themes_api("feature_list", Array())
        if is_wp_error(feature_list_):
            return features_
        # end if
    # end if
    if (not feature_list_):
        return features_
    # end if
    set_site_transient("wporg_theme_feature_list", feature_list_, 3 * HOUR_IN_SECONDS)
    category_translations_ = Array({"Layout": __("Layout"), "Features": __("Features"), "Subject": __("Subject")})
    #// Loop over the wp.org canonical list and apply translations.
    wporg_features_ = Array()
    for feature_category_,feature_items_ in feature_list_.items():
        if (php_isset(lambda : category_translations_[feature_category_])):
            feature_category_ = category_translations_[feature_category_]
        # end if
        wporg_features_[feature_category_] = Array()
        for feature_ in feature_items_:
            if (php_isset(lambda : features_[feature_category_][feature_])):
                wporg_features_[feature_category_][feature_] = features_[feature_category_][feature_]
            else:
                wporg_features_[feature_category_][feature_] = feature_
            # end if
        # end for
    # end for
    return wporg_features_
# end def get_theme_feature_list
#// 
#// Retrieves theme installer pages from the WordPress.org Themes API.
#// 
#// It is possible for a theme to override the Themes API result with three
#// filters. Assume this is for themes, which can extend on the Theme Info to
#// offer more choices. This is very powerful and must be used with care, when
#// overriding the filters.
#// 
#// The first filter, {@see 'themes_api_args'}, is for the args and gives the action
#// as the second parameter. The hook for {@see 'themes_api_args'} must ensure that
#// an object is returned.
#// 
#// The second filter, {@see 'themes_api'}, allows a plugin to override the WordPress.org
#// Theme API entirely. If `$action` is 'query_themes', 'theme_information', or 'feature_list',
#// an object MUST be passed. If `$action` is 'hot_tags', an array should be passed.
#// 
#// Finally, the third filter, {@see 'themes_api_result'}, makes it possible to filter the
#// response object or array, depending on the `$action` type.
#// 
#// Supported arguments per action:
#// 
#// | Argument Name      | 'query_themes' | 'theme_information' | 'hot_tags' | 'feature_list'   |
#// | -------------------| :------------: | :-----------------: | :--------: | :--------------: |
#// | `$slug`            | No             |  Yes                | No         | No               |
#// | `$per_page`        | Yes            |  No                 | No         | No               |
#// | `$page`            | Yes            |  No                 | No         | No               |
#// | `$number`          | No             |  No                 | Yes        | No               |
#// | `$search`          | Yes            |  No                 | No         | No               |
#// | `$tag`             | Yes            |  No                 | No         | No               |
#// | `$author`          | Yes            |  No                 | No         | No               |
#// | `$user`            | Yes            |  No                 | No         | No               |
#// | `$browse`          | Yes            |  No                 | No         | No               |
#// | `$locale`          | Yes            |  Yes                | No         | No               |
#// | `$fields`          | Yes            |  Yes                | No         | No               |
#// 
#// @since 2.8.0
#// 
#// @param string       $action API action to perform: 'query_themes', 'theme_information',
#// 'hot_tags' or 'feature_list'.
#// @param array|object $args   {
#// Optional. Array or object of arguments to serialize for the Themes API.
#// 
#// @type string  $slug     The theme slug. Default empty.
#// @type int     $per_page Number of themes per page. Default 24.
#// @type int     $page     Number of current page. Default 1.
#// @type int     $number   Number of tags to be queried.
#// @type string  $search   A search term. Default empty.
#// @type string  $tag      Tag to filter themes. Default empty.
#// @type string  $author   Username of an author to filter themes. Default empty.
#// @type string  $user     Username to query for their favorites. Default empty.
#// @type string  $browse   Browse view: 'featured', 'popular', 'updated', 'favorites'.
#// @type string  $locale   Locale to provide context-sensitive results. Default is the value of get_locale().
#// @type array   $fields   {
#// Array of fields which should or should not be returned.
#// 
#// @type bool $description        Whether to return the theme full description. Default false.
#// @type bool $sections           Whether to return the theme readme sections: description, installation,
#// FAQ, screenshots, other notes, and changelog. Default false.
#// @type bool $rating             Whether to return the rating in percent and total number of ratings.
#// Default false.
#// @type bool $ratings            Whether to return the number of rating for each star (1-5). Default false.
#// @type bool $downloaded         Whether to return the download count. Default false.
#// @type bool $downloadlink       Whether to return the download link for the package. Default false.
#// @type bool $last_updated       Whether to return the date of the last update. Default false.
#// @type bool $tags               Whether to return the assigned tags. Default false.
#// @type bool $homepage           Whether to return the theme homepage link. Default false.
#// @type bool $screenshots        Whether to return the screenshots. Default false.
#// @type int  $screenshot_count   Number of screenshots to return. Default 1.
#// @type bool $screenshot_url     Whether to return the URL of the first screenshot. Default false.
#// @type bool $photon_screenshots Whether to return the screenshots via Photon. Default false.
#// @type bool $template           Whether to return the slug of the parent theme. Default false.
#// @type bool $parent             Whether to return the slug, name and homepage of the parent theme. Default false.
#// @type bool $versions           Whether to return the list of all available versions. Default false.
#// @type bool $theme_url          Whether to return theme's URL. Default false.
#// @type bool $extended_author    Whether to return nicename or nicename and display name. Default false.
#// }
#// }
#// @return object|array|WP_Error Response object or array on success, WP_Error on failure. See the
#// {@link https://developer.wordpress.org/reference/functions/themes_api/ function reference article}
#// for more information on the make-up of possible return objects depending on the value of `$action`.
#//
def themes_api(action_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    if php_is_array(args_):
        args_ = args_
    # end if
    if "query_themes" == action_:
        if (not (php_isset(lambda : args_.per_page))):
            args_.per_page = 24
        # end if
    # end if
    if (not (php_isset(lambda : args_.locale))):
        args_.locale = get_user_locale()
    # end if
    if (not (php_isset(lambda : args_.wp_version))):
        args_.wp_version = php_substr(wp_version_, 0, 3)
        pass
    # end if
    #// 
    #// Filters arguments used to query for installer pages from the WordPress.org Themes API.
    #// 
    #// Important: An object MUST be returned to this filter.
    #// 
    #// @since 2.8.0
    #// 
    #// @param object $args   Arguments used to query for installer pages from the WordPress.org Themes API.
    #// @param string $action Requested action. Likely values are 'theme_information',
    #// 'feature_list', or 'query_themes'.
    #//
    args_ = apply_filters("themes_api_args", args_, action_)
    #// 
    #// Filters whether to override the WordPress.org Themes API.
    #// 
    #// Passing a non-false value will effectively short-circuit the WordPress.org API request.
    #// 
    #// If `$action` is 'query_themes', 'theme_information', or 'feature_list', an object MUST
    #// be passed. If `$action` is 'hot_tags', an array should be passed.
    #// 
    #// @since 2.8.0
    #// 
    #// @param false|object|array $override Whether to override the WordPress.org Themes API. Default false.
    #// @param string             $action   Requested action. Likely values are 'theme_information',
    #// 'feature_list', or 'query_themes'.
    #// @param object             $args     Arguments used to query for installer pages from the Themes API.
    #//
    res_ = apply_filters("themes_api", False, action_, args_)
    if (not res_):
        url_ = "http://api.wordpress.org/themes/info/1.2/"
        url_ = add_query_arg(Array({"action": action_, "request": args_}), url_)
        http_url_ = url_
        ssl_ = wp_http_supports(Array("ssl"))
        if ssl_:
            url_ = set_url_scheme(url_, "https")
        # end if
        http_args_ = Array({"user-agent": "WordPress/" + wp_version_ + "; " + home_url("/")})
        request_ = wp_remote_get(url_, http_args_)
        if ssl_ and is_wp_error(request_):
            if (not wp_doing_ajax()):
                trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
            # end if
            request_ = wp_remote_get(http_url_, http_args_)
        # end if
        if is_wp_error(request_):
            res_ = php_new_class("WP_Error", lambda : WP_Error("themes_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), request_.get_error_message()))
        else:
            res_ = php_json_decode(wp_remote_retrieve_body(request_), True)
            if php_is_array(res_):
                #// Object casting is required in order to match the info/1.0 format.
                res_ = res_
            elif None == res_:
                res_ = php_new_class("WP_Error", lambda : WP_Error("themes_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), wp_remote_retrieve_body(request_)))
            # end if
            if (php_isset(lambda : res_.error)):
                res_ = php_new_class("WP_Error", lambda : WP_Error("themes_api_failed", res_.error))
            # end if
        # end if
        #// Back-compat for info/1.2 API, upgrade the theme objects in query_themes to objects.
        if "query_themes" == action_:
            for i_,theme_ in res_.themes.items():
                res_.themes[i_] = theme_
            # end for
        # end if
        #// Back-compat for info/1.2 API, downgrade the feature_list result back to an array.
        if "feature_list" == action_:
            res_ = res_
        # end if
    # end if
    #// 
    #// Filters the returned WordPress.org Themes API response.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array|object|WP_Error $res    WordPress.org Themes API response.
    #// @param string                $action Requested action. Likely values are 'theme_information',
    #// 'feature_list', or 'query_themes'.
    #// @param object                $args   Arguments used to query for installer pages from the WordPress.org Themes API.
    #//
    return apply_filters("themes_api_result", res_, action_, args_)
# end def themes_api
#// 
#// Prepare themes for JavaScript.
#// 
#// @since 3.8.0
#// 
#// @param WP_Theme[] $themes Optional. Array of theme objects to prepare.
#// Defaults to all allowed themes.
#// 
#// @return array An associative array of theme data, sorted by name.
#//
def wp_prepare_themes_for_js(themes_=None, *_args_):
    if themes_ is None:
        themes_ = None
    # end if
    
    current_theme_ = get_stylesheet()
    #// 
    #// Filters theme data before it is prepared for JavaScript.
    #// 
    #// Passing a non-empty array will result in wp_prepare_themes_for_js() returning
    #// early with that value instead.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array           $prepared_themes An associative array of theme data. Default empty array.
    #// @param WP_Theme[]|null $themes          An array of theme objects to prepare, if any.
    #// @param string          $current_theme   The current theme slug.
    #//
    prepared_themes_ = apply_filters("pre_prepare_themes_for_js", Array(), themes_, current_theme_)
    if (not php_empty(lambda : prepared_themes_)):
        return prepared_themes_
    # end if
    #// Make sure the current theme is listed first.
    prepared_themes_[current_theme_] = Array()
    if None == themes_:
        themes_ = wp_get_themes(Array({"allowed": True}))
        if (not (php_isset(lambda : themes_[current_theme_]))):
            themes_[current_theme_] = wp_get_theme()
        # end if
    # end if
    updates_ = Array()
    if current_user_can("update_themes"):
        updates_transient_ = get_site_transient("update_themes")
        if (php_isset(lambda : updates_transient_.response)):
            updates_ = updates_transient_.response
        # end if
    # end if
    WP_Theme.sort_by_name(themes_)
    parents_ = Array()
    for theme_ in themes_:
        slug_ = theme_.get_stylesheet()
        encoded_slug_ = urlencode(slug_)
        parent_ = False
        if theme_.parent():
            parent_ = theme_.parent()
            parents_[slug_] = parent_.get_stylesheet()
            parent_ = parent_.display("Name")
        # end if
        customize_action_ = None
        if current_user_can("edit_theme_options") and current_user_can("customize"):
            customize_action_ = esc_url(add_query_arg(Array({"return": urlencode(esc_url_raw(remove_query_arg(wp_removable_query_args(), wp_unslash(PHP_SERVER["REQUEST_URI"]))))}), wp_customize_url(slug_)))
        # end if
        prepared_themes_[slug_] = Array({"id": slug_, "name": theme_.display("Name"), "screenshot": Array(theme_.get_screenshot()), "description": theme_.display("Description"), "author": theme_.display("Author", False, True), "authorAndUri": theme_.display("Author"), "version": theme_.display("Version"), "tags": theme_.display("Tags"), "parent": parent_, "active": slug_ == current_theme_, "hasUpdate": (php_isset(lambda : updates_[slug_])), "hasPackage": (php_isset(lambda : updates_[slug_])) and (not php_empty(lambda : updates_[slug_]["package"])), "update": get_theme_update_available(theme_), "actions": Array({"activate": wp_nonce_url(admin_url("themes.php?action=activate&amp;stylesheet=" + encoded_slug_), "switch-theme_" + slug_) if current_user_can("switch_themes") else None, "customize": customize_action_, "delete": wp_nonce_url(admin_url("themes.php?action=delete&amp;stylesheet=" + encoded_slug_), "delete-theme_" + slug_) if current_user_can("delete_themes") else None})})
    # end for
    #// Remove 'delete' action if theme has an active child.
    if (not php_empty(lambda : parents_)) and php_array_key_exists(current_theme_, parents_):
        prepared_themes_[parents_[current_theme_]]["actions"]["delete"] = None
    # end if
    #// 
    #// Filters the themes prepared for JavaScript, for themes.php.
    #// 
    #// Could be useful for changing the order, which is by name by default.
    #// 
    #// @since 3.8.0
    #// 
    #// @param array $prepared_themes Array of theme data.
    #//
    prepared_themes_ = apply_filters("wp_prepare_themes_for_js", prepared_themes_)
    prepared_themes_ = php_array_values(prepared_themes_)
    return php_array_filter(prepared_themes_)
# end def wp_prepare_themes_for_js
#// 
#// Print JS templates for the theme-browsing UI in the Customizer.
#// 
#// @since 4.2.0
#//
def customize_themes_print_templates(*_args_):
    
    
    php_print("""   <script type=\"text/html\" id=\"tmpl-customize-themes-details-view\">
    <div class=\"theme-backdrop\"></div>
    <div class=\"theme-wrap wp-clearfix\" role=\"document\">
    <div class=\"theme-header\">
    <button type=\"button\" class=\"left dashicons dashicons-no\"><span class=\"screen-reader-text\">""")
    _e("Show previous theme")
    php_print("</span></button>\n               <button type=\"button\" class=\"right dashicons dashicons-no\"><span class=\"screen-reader-text\">")
    _e("Show next theme")
    php_print("</span></button>\n               <button type=\"button\" class=\"close dashicons dashicons-no\"><span class=\"screen-reader-text\">")
    _e("Close details dialog")
    php_print("""</span></button>
    </div>
    <div class=\"theme-about wp-clearfix\">
    <div class=\"theme-screenshots\">
    <# if ( data.screenshot && data.screenshot[0] ) { #>
    <div class=\"screenshot\"><img src=\"{{ data.screenshot[0] }}\" alt=\"\" /></div>
    <# } else { #>
    <div class=\"screenshot blank\"></div>
    <# } #>
    </div>
    <div class=\"theme-info\">
    <# if ( data.active ) { #>
    <span class=\"current-label\">""")
    _e("Current Theme")
    php_print("""</span>
    <# } #>
    <h2 class=\"theme-name\">{{{ data.name }}}<span class=\"theme-version\">
    """)
    #// translators: %s: Theme version.
    printf(__("Version: %s"), "{{ data.version }}")
    php_print("                 </span></h2>\n                  <h3 class=\"theme-author\">\n                       ")
    #// translators: %s: Theme author link.
    printf(__("By %s"), "{{{ data.authorAndUri }}}")
    php_print("""                   </h3>
    <# if ( data.stars && 0 != data.num_ratings ) { #>
    <div class=\"theme-rating\">
    {{{ data.stars }}}
    <a class=\"num-ratings\" target=\"_blank\" href=\"{{ data.reviews_url }}\">
    """)
    printf("%1$s <span class=\"screen-reader-text\">%2$s</span>", php_sprintf(__("(%s ratings)"), "{{ data.num_ratings }}"), __("(opens in a new tab)"))
    php_print("""                           </a>
    </div>
    <# } #>
    <# if ( data.hasUpdate ) { #>
    <div class=\"notice notice-warning notice-alt notice-large\" data-slug=\"{{ data.id }}\">
    <h3 class=\"notice-title\">""")
    _e("Update Available")
    php_print("""</h3>
    {{{ data.update }}}
    </div>
    <# } #>
    <# if ( data.parent ) { #>
    <p class=\"parent-theme\">
    """)
    printf(__("This is a child theme of %s."), "<strong>{{{ data.parent }}}</strong>")
    php_print("""                       </p>
    <# } #>
    <p class=\"theme-description\">{{{ data.description }}}</p>
    <# if ( data.tags ) { #>
    <p class=\"theme-tags\"><span>""")
    _e("Tags:")
    php_print("""</span> {{{ data.tags }}}</p>
    <# } #>
    </div>
    </div>
    <div class=\"theme-actions\">
    <# if ( data.active ) { #>
    <button type=\"button\" class=\"button button-primary customize-theme\">""")
    _e("Customize")
    php_print("</button>\n              <# } else if ( 'installed' === data.type ) { #>\n                   ")
    if current_user_can("delete_themes"):
        php_print("                     <# if ( data.actions && data.actions['delete'] ) { #>\n                         <a href=\"{{{ data.actions['delete'] }}}\" data-slug=\"{{ data.id }}\" class=\"button button-secondary delete-theme\">")
        _e("Delete")
        php_print("</a>\n                       <# } #>\n                   ")
    # end if
    php_print("                 <button type=\"button\" class=\"button button-primary preview-theme\" data-slug=\"{{ data.id }}\">")
    _e("Live Preview")
    php_print("</button>\n              <# } else { #>\n                    <button type=\"button\" class=\"button theme-install\" data-slug=\"{{ data.id }}\">")
    _e("Install")
    php_print("</button>\n                  <button type=\"button\" class=\"button button-primary theme-install preview\" data-slug=\"{{ data.id }}\">")
    _e("Install &amp; Preview")
    php_print("""</button>
    <# } #>
    </div>
    </div>
    </script>
    """)
# end def customize_themes_print_templates
#// 
#// Determines whether a theme is technically active but was paused while
#// loading.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 5.2.0
#// 
#// @param string $theme Path to the theme directory relative to the themes directory.
#// @return bool True, if in the list of paused themes. False, not in the list.
#//
def is_theme_paused(theme_=None, *_args_):
    
    
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_themes"]))):
        return False
    # end if
    if get_stylesheet() != theme_ and get_template() != theme_:
        return False
    # end if
    return php_array_key_exists(theme_, PHP_GLOBALS["_paused_themes"])
# end def is_theme_paused
#// 
#// Gets the error that was recorded for a paused theme.
#// 
#// @since 5.2.0
#// 
#// @param string $theme Path to the theme directory relative to the themes
#// directory.
#// @return array|false Array of error information as it was returned by
#// `error_get_last()`, or false if none was recorded.
#//
def wp_get_theme_error(theme_=None, *_args_):
    
    
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_themes"]))):
        return False
    # end if
    if (not php_array_key_exists(theme_, PHP_GLOBALS["_paused_themes"])):
        return False
    # end if
    return PHP_GLOBALS["_paused_themes"][theme_]
# end def wp_get_theme_error
#// 
#// Tries to resume a single theme.
#// 
#// If a redirect was provided and a functions.php file was found, we first ensure that
#// functions.php file does not throw fatal errors anymore.
#// 
#// The way it works is by setting the redirection to the error before trying to
#// include the file. If the theme fails, then the redirection will not be overwritten
#// with the success message and the theme will not be resumed.
#// 
#// @since 5.2.0
#// 
#// @param string $theme    Single theme to resume.
#// @param string $redirect Optional. URL to redirect to. Default empty string.
#// @return bool|WP_Error True on success, false if `$theme` was not paused,
#// `WP_Error` on failure.
#//
def resume_theme(theme_=None, redirect_="", *_args_):
    
    
    extension_ = php_explode("/", theme_)
    #// 
    #// We'll override this later if the theme could be resumed without
    #// creating a fatal error.
    #//
    if (not php_empty(lambda : redirect_)):
        functions_path_ = ""
        if php_strpos(STYLESHEETPATH, extension_):
            functions_path_ = STYLESHEETPATH + "/functions.php"
        elif php_strpos(TEMPLATEPATH, extension_):
            functions_path_ = TEMPLATEPATH + "/functions.php"
        # end if
        if (not php_empty(lambda : functions_path_)):
            wp_redirect(add_query_arg("_error_nonce", wp_create_nonce("theme-resume-error_" + theme_), redirect_))
            #// Load the theme's functions.php to test whether it throws a fatal error.
            ob_start()
            if (not php_defined("WP_SANDBOX_SCRAPING")):
                php_define("WP_SANDBOX_SCRAPING", True)
            # end if
            php_include_file(functions_path_, once=False)
            ob_clean()
        # end if
    # end if
    result_ = wp_paused_themes().delete(extension_)
    if (not result_):
        return php_new_class("WP_Error", lambda : WP_Error("could_not_resume_theme", __("Could not resume the theme.")))
    # end if
    return True
# end def resume_theme
#// 
#// Renders an admin notice in case some themes have been paused due to errors.
#// 
#// @since 5.2.0
#//
def paused_themes_notice(*_args_):
    
    
    if "themes.php" == PHP_GLOBALS["pagenow"]:
        return
    # end if
    if (not current_user_can("resume_themes")):
        return
    # end if
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_themes"]))) or php_empty(lambda : PHP_GLOBALS["_paused_themes"]):
        return
    # end if
    printf("<div class=\"notice notice-error\"><p><strong>%s</strong><br>%s</p><p><a href=\"%s\">%s</a></p></div>", __("One or more themes failed to load properly."), __("You can find more details and make changes on the Themes screen."), esc_url(admin_url("themes.php")), __("Go to the Themes screen"))
# end def paused_themes_notice
