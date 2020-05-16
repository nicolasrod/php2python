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
def delete_theme(stylesheet=None, redirect="", *args_):
    
    global wp_filesystem
    php_check_if_defined("wp_filesystem")
    if php_empty(lambda : stylesheet):
        return False
    # end if
    if php_empty(lambda : redirect):
        redirect = wp_nonce_url("themes.php?action=delete&stylesheet=" + urlencode(stylesheet), "delete-theme_" + stylesheet)
    # end if
    ob_start()
    credentials = request_filesystem_credentials(redirect)
    data = ob_get_clean()
    if False == credentials:
        if (not php_empty(lambda : data)):
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print(data)
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        return
    # end if
    if (not WP_Filesystem(credentials)):
        ob_start()
        #// Failed to connect. Error and request again.
        request_filesystem_credentials(redirect, "", True)
        data = ob_get_clean()
        if (not php_empty(lambda : data)):
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print(data)
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        return
    # end if
    if (not php_is_object(wp_filesystem)):
        return php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", __("Could not access filesystem.")))
    # end if
    if is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
        return php_new_class("WP_Error", lambda : WP_Error("fs_error", __("Filesystem error."), wp_filesystem.errors))
    # end if
    #// Get the base plugin folder.
    themes_dir = wp_filesystem.wp_themes_dir()
    if php_empty(lambda : themes_dir):
        return php_new_class("WP_Error", lambda : WP_Error("fs_no_themes_dir", __("Unable to locate WordPress theme directory.")))
    # end if
    themes_dir = trailingslashit(themes_dir)
    theme_dir = trailingslashit(themes_dir + stylesheet)
    deleted = wp_filesystem.delete(theme_dir, True)
    if (not deleted):
        return php_new_class("WP_Error", lambda : WP_Error("could_not_remove_theme", php_sprintf(__("Could not fully remove the theme %s."), stylesheet)))
    # end if
    theme_translations = wp_get_installed_translations("themes")
    #// Remove language files, silently.
    if (not php_empty(lambda : theme_translations[stylesheet])):
        translations = theme_translations[stylesheet]
        for translation,data in translations:
            wp_filesystem.delete(WP_LANG_DIR + "/themes/" + stylesheet + "-" + translation + ".po")
            wp_filesystem.delete(WP_LANG_DIR + "/themes/" + stylesheet + "-" + translation + ".mo")
            json_translation_files = glob(WP_LANG_DIR + "/themes/" + stylesheet + "-" + translation + "-*.json")
            if json_translation_files:
                php_array_map(Array(wp_filesystem, "delete"), json_translation_files)
            # end if
        # end for
    # end if
    #// Remove the theme from allowed themes on the network.
    if is_multisite():
        WP_Theme.network_disable_theme(stylesheet)
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
def get_page_templates(post=None, post_type="page", *args_):
    
    return php_array_flip(wp_get_theme().get_page_templates(post, post_type))
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
def _get_template_edit_filename(fullpath=None, containingfolder=None, *args_):
    
    return php_str_replace(php_dirname(php_dirname(containingfolder)), "", fullpath)
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
def theme_update_available(theme=None, *args_):
    
    php_print(get_theme_update_available(theme))
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
def get_theme_update_available(theme=None, *args_):
    
    get_theme_update_available.themes_update = None
    if (not current_user_can("update_themes")):
        return False
    # end if
    if (not (php_isset(lambda : get_theme_update_available.themes_update))):
        get_theme_update_available.themes_update = get_site_transient("update_themes")
    # end if
    if (not type(theme).__name__ == "WP_Theme"):
        return False
    # end if
    stylesheet = theme.get_stylesheet()
    html = ""
    if (php_isset(lambda : get_theme_update_available.themes_update.response[stylesheet])):
        update = get_theme_update_available.themes_update.response[stylesheet]
        theme_name = theme.display("Name")
        details_url = add_query_arg(Array({"TB_iframe": "true", "width": 1024, "height": 800}), update["url"])
        #// Theme browser inside WP? Replace this. Also, theme preview JS will override this on the available list.
        update_url = wp_nonce_url(admin_url("update.php?action=upgrade-theme&amp;theme=" + urlencode(stylesheet)), "upgrade-theme_" + stylesheet)
        if (not is_multisite()):
            if (not current_user_can("update_themes")):
                html = php_sprintf("<p><strong>" + __("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>.") + "</strong></p>", theme_name, esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_name, update["new_version"]))), update["new_version"])
            elif php_empty(lambda : update["package"]):
                html = php_sprintf("<p><strong>" + __("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a>. <em>Automatic update is unavailable for this theme.</em>") + "</strong></p>", theme_name, esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_name, update["new_version"]))), update["new_version"])
            else:
                html = php_sprintf("<p><strong>" + __("There is a new version of %1$s available. <a href=\"%2$s\" %3$s>View version %4$s details</a> or <a href=\"%5$s\" %6$s>update now</a>.") + "</strong></p>", theme_name, esc_url(details_url), php_sprintf("class=\"thickbox open-plugin-details-modal\" aria-label=\"%s\"", esc_attr(php_sprintf(__("View %1$s version %2$s details"), theme_name, update["new_version"]))), update["new_version"], update_url, php_sprintf("aria-label=\"%s\" id=\"update-theme\" data-slug=\"%s\"", esc_attr(php_sprintf(__("Update %s now"), theme_name)), stylesheet))
            # end if
        # end if
    # end if
    return html
# end def get_theme_update_available
#// 
#// Retrieve list of WordPress theme features (aka theme tags).
#// 
#// @since 3.1.0
#// 
#// @param bool $api Optional. Whether try to fetch tags from the WordPress.org API. Defaults to true.
#// @return array Array of features keyed by category with translations keyed by slug.
#//
def get_theme_feature_list(api=True, *args_):
    
    #// Hard-coded list is used if API is not accessible.
    features = Array({__("Subject"): Array({"blog": __("Blog"), "e-commerce": __("E-Commerce"), "education": __("Education"), "entertainment": __("Entertainment"), "food-and-drink": __("Food & Drink"), "holiday": __("Holiday"), "news": __("News"), "photography": __("Photography"), "portfolio": __("Portfolio")})}, {__("Features"): Array({"accessibility-ready": __("Accessibility Ready"), "custom-background": __("Custom Background"), "custom-colors": __("Custom Colors"), "custom-header": __("Custom Header"), "custom-logo": __("Custom Logo"), "editor-style": __("Editor Style"), "featured-image-header": __("Featured Image Header"), "featured-images": __("Featured Images"), "footer-widgets": __("Footer Widgets"), "full-width-template": __("Full Width Template"), "post-formats": __("Post Formats"), "sticky-post": __("Sticky Post"), "theme-options": __("Theme Options")})}, {__("Layout"): Array({"grid-layout": __("Grid Layout"), "one-column": __("One Column"), "two-columns": __("Two Columns"), "three-columns": __("Three Columns"), "four-columns": __("Four Columns"), "left-sidebar": __("Left Sidebar"), "right-sidebar": __("Right Sidebar")})})
    if (not api) or (not current_user_can("install_themes")):
        return features
    # end if
    feature_list = get_site_transient("wporg_theme_feature_list")
    if (not feature_list):
        set_site_transient("wporg_theme_feature_list", Array(), 3 * HOUR_IN_SECONDS)
    # end if
    if (not feature_list):
        feature_list = themes_api("feature_list", Array())
        if is_wp_error(feature_list):
            return features
        # end if
    # end if
    if (not feature_list):
        return features
    # end if
    set_site_transient("wporg_theme_feature_list", feature_list, 3 * HOUR_IN_SECONDS)
    category_translations = Array({"Layout": __("Layout"), "Features": __("Features"), "Subject": __("Subject")})
    #// Loop over the wp.org canonical list and apply translations.
    wporg_features = Array()
    for feature_category,feature_items in feature_list:
        if (php_isset(lambda : category_translations[feature_category])):
            feature_category = category_translations[feature_category]
        # end if
        wporg_features[feature_category] = Array()
        for feature in feature_items:
            if (php_isset(lambda : features[feature_category][feature])):
                wporg_features[feature_category][feature] = features[feature_category][feature]
            else:
                wporg_features[feature_category][feature] = feature
            # end if
        # end for
    # end for
    return wporg_features
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
def themes_api(action=None, args=Array(), *args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    if php_is_array(args):
        args = args
    # end if
    if "query_themes" == action:
        if (not (php_isset(lambda : args.per_page))):
            args.per_page = 24
        # end if
    # end if
    if (not (php_isset(lambda : args.locale))):
        args.locale = get_user_locale()
    # end if
    if (not (php_isset(lambda : args.wp_version))):
        args.wp_version = php_substr(wp_version, 0, 3)
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
    args = apply_filters("themes_api_args", args, action)
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
    res = apply_filters("themes_api", False, action, args)
    if (not res):
        url = "http://api.wordpress.org/themes/info/1.2/"
        url = add_query_arg(Array({"action": action, "request": args}), url)
        http_url = url
        ssl = wp_http_supports(Array("ssl"))
        if ssl:
            url = set_url_scheme(url, "https")
        # end if
        http_args = Array({"user-agent": "WordPress/" + wp_version + "; " + home_url("/")})
        request = wp_remote_get(url, http_args)
        if ssl and is_wp_error(request):
            if (not wp_doing_ajax()):
                trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
            # end if
            request = wp_remote_get(http_url, http_args)
        # end if
        if is_wp_error(request):
            res = php_new_class("WP_Error", lambda : WP_Error("themes_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), request.get_error_message()))
        else:
            res = php_json_decode(wp_remote_retrieve_body(request), True)
            if php_is_array(res):
                #// Object casting is required in order to match the info/1.0 format.
                res = res
            elif None == res:
                res = php_new_class("WP_Error", lambda : WP_Error("themes_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), wp_remote_retrieve_body(request)))
            # end if
            if (php_isset(lambda : res.error)):
                res = php_new_class("WP_Error", lambda : WP_Error("themes_api_failed", res.error))
            # end if
        # end if
        #// Back-compat for info/1.2 API, upgrade the theme objects in query_themes to objects.
        if "query_themes" == action:
            for i,theme in res.themes:
                res.themes[i] = theme
            # end for
        # end if
        #// Back-compat for info/1.2 API, downgrade the feature_list result back to an array.
        if "feature_list" == action:
            res = res
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
    return apply_filters("themes_api_result", res, action, args)
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
def wp_prepare_themes_for_js(themes=None, *args_):
    
    current_theme = get_stylesheet()
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
    prepared_themes = apply_filters("pre_prepare_themes_for_js", Array(), themes, current_theme)
    if (not php_empty(lambda : prepared_themes)):
        return prepared_themes
    # end if
    #// Make sure the current theme is listed first.
    prepared_themes[current_theme] = Array()
    if None == themes:
        themes = wp_get_themes(Array({"allowed": True}))
        if (not (php_isset(lambda : themes[current_theme]))):
            themes[current_theme] = wp_get_theme()
        # end if
    # end if
    updates = Array()
    if current_user_can("update_themes"):
        updates_transient = get_site_transient("update_themes")
        if (php_isset(lambda : updates_transient.response)):
            updates = updates_transient.response
        # end if
    # end if
    WP_Theme.sort_by_name(themes)
    parents = Array()
    for theme in themes:
        slug = theme.get_stylesheet()
        encoded_slug = urlencode(slug)
        parent = False
        if theme.parent():
            parent = theme.parent()
            parents[slug] = parent.get_stylesheet()
            parent = parent.display("Name")
        # end if
        customize_action = None
        if current_user_can("edit_theme_options") and current_user_can("customize"):
            customize_action = esc_url(add_query_arg(Array({"return": urlencode(esc_url_raw(remove_query_arg(wp_removable_query_args(), wp_unslash(PHP_SERVER["REQUEST_URI"]))))}), wp_customize_url(slug)))
        # end if
        prepared_themes[slug] = Array({"id": slug, "name": theme.display("Name"), "screenshot": Array(theme.get_screenshot()), "description": theme.display("Description"), "author": theme.display("Author", False, True), "authorAndUri": theme.display("Author"), "version": theme.display("Version"), "tags": theme.display("Tags"), "parent": parent, "active": slug == current_theme, "hasUpdate": (php_isset(lambda : updates[slug])), "hasPackage": (php_isset(lambda : updates[slug])) and (not php_empty(lambda : updates[slug]["package"])), "update": get_theme_update_available(theme), "actions": Array({"activate": wp_nonce_url(admin_url("themes.php?action=activate&amp;stylesheet=" + encoded_slug), "switch-theme_" + slug) if current_user_can("switch_themes") else None, "customize": customize_action, "delete": wp_nonce_url(admin_url("themes.php?action=delete&amp;stylesheet=" + encoded_slug), "delete-theme_" + slug) if current_user_can("delete_themes") else None})})
    # end for
    #// Remove 'delete' action if theme has an active child.
    if (not php_empty(lambda : parents)) and php_array_key_exists(current_theme, parents):
        prepared_themes[parents[current_theme]]["actions"]["delete"] = None
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
    prepared_themes = apply_filters("wp_prepare_themes_for_js", prepared_themes)
    prepared_themes = php_array_values(prepared_themes)
    return php_array_filter(prepared_themes)
# end def wp_prepare_themes_for_js
#// 
#// Print JS templates for the theme-browsing UI in the Customizer.
#// 
#// @since 4.2.0
#//
def customize_themes_print_templates(*args_):
    
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
def is_theme_paused(theme=None, *args_):
    
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_themes"]))):
        return False
    # end if
    if get_stylesheet() != theme and get_template() != theme:
        return False
    # end if
    return php_array_key_exists(theme, PHP_GLOBALS["_paused_themes"])
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
def wp_get_theme_error(theme=None, *args_):
    
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_themes"]))):
        return False
    # end if
    if (not php_array_key_exists(theme, PHP_GLOBALS["_paused_themes"])):
        return False
    # end if
    return PHP_GLOBALS["_paused_themes"][theme]
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
def resume_theme(theme=None, redirect="", *args_):
    
    extension = php_explode("/", theme)
    #// 
    #// We'll override this later if the theme could be resumed without
    #// creating a fatal error.
    #//
    if (not php_empty(lambda : redirect)):
        functions_path = ""
        if php_strpos(STYLESHEETPATH, extension):
            functions_path = STYLESHEETPATH + "/functions.php"
        elif php_strpos(TEMPLATEPATH, extension):
            functions_path = TEMPLATEPATH + "/functions.php"
        # end if
        if (not php_empty(lambda : functions_path)):
            wp_redirect(add_query_arg("_error_nonce", wp_create_nonce("theme-resume-error_" + theme), redirect))
            #// Load the theme's functions.php to test whether it throws a fatal error.
            ob_start()
            if (not php_defined("WP_SANDBOX_SCRAPING")):
                php_define("WP_SANDBOX_SCRAPING", True)
            # end if
            php_include_file(functions_path, once=False)
            ob_clean()
        # end if
    # end if
    result = wp_paused_themes().delete(extension)
    if (not result):
        return php_new_class("WP_Error", lambda : WP_Error("could_not_resume_theme", __("Could not resume the theme.")))
    # end if
    return True
# end def resume_theme
#// 
#// Renders an admin notice in case some themes have been paused due to errors.
#// 
#// @since 5.2.0
#//
def paused_themes_notice(*args_):
    
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
