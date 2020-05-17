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
#// WordPress Plugin Install Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Retrieves plugin installer pages from the WordPress.org Plugins API.
#// 
#// It is possible for a plugin to override the Plugin API result with three
#// filters. Assume this is for plugins, which can extend on the Plugin Info to
#// offer more choices. This is very powerful and must be used with care when
#// overriding the filters.
#// 
#// The first filter, {@see 'plugins_api_args'}, is for the args and gives the action
#// as the second parameter. The hook for {@see 'plugins_api_args'} must ensure that
#// an object is returned.
#// 
#// The second filter, {@see 'plugins_api'}, allows a plugin to override the WordPress.org
#// Plugin Installation API entirely. If `$action` is 'query_plugins' or 'plugin_information',
#// an object MUST be passed. If `$action` is 'hot_tags' or 'hot_categories', an array MUST
#// be passed.
#// 
#// Finally, the third filter, {@see 'plugins_api_result'}, makes it possible to filter the
#// response object or array, depending on the `$action` type.
#// 
#// Supported arguments per action:
#// 
#// | Argument Name        | query_plugins | plugin_information | hot_tags | hot_categories |
#// | -------------------- | :-----------: | :----------------: | :------: | :------------: |
#// | `$slug`              | No            |  Yes               | No       | No             |
#// | `$per_page`          | Yes           |  No                | No       | No             |
#// | `$page`              | Yes           |  No                | No       | No             |
#// | `$number`            | No            |  No                | Yes      | Yes            |
#// | `$search`            | Yes           |  No                | No       | No             |
#// | `$tag`               | Yes           |  No                | No       | No             |
#// | `$author`            | Yes           |  No                | No       | No             |
#// | `$user`              | Yes           |  No                | No       | No             |
#// | `$browse`            | Yes           |  No                | No       | No             |
#// | `$locale`            | Yes           |  Yes               | No       | No             |
#// | `$installed_plugins` | Yes           |  No                | No       | No             |
#// | `$is_ssl`            | Yes           |  Yes               | No       | No             |
#// | `$fields`            | Yes           |  Yes               | No       | No             |
#// 
#// @since 2.7.0
#// 
#// @param string       $action API action to perform: 'query_plugins', 'plugin_information',
#// 'hot_tags' or 'hot_categories'.
#// @param array|object $args   {
#// Optional. Array or object of arguments to serialize for the Plugin Info API.
#// 
#// @type string  $slug              The plugin slug. Default empty.
#// @type int     $per_page          Number of plugins per page. Default 24.
#// @type int     $page              Number of current page. Default 1.
#// @type int     $number            Number of tags or categories to be queried.
#// @type string  $search            A search term. Default empty.
#// @type string  $tag               Tag to filter plugins. Default empty.
#// @type string  $author            Username of an plugin author to filter plugins. Default empty.
#// @type string  $user              Username to query for their favorites. Default empty.
#// @type string  $browse            Browse view: 'popular', 'new', 'beta', 'recommended'.
#// @type string  $locale            Locale to provide context-sensitive results. Default is the value
#// of get_locale().
#// @type string  $installed_plugins Installed plugins to provide context-sensitive results.
#// @type bool    $is_ssl            Whether links should be returned with https or not. Default false.
#// @type array   $fields            {
#// Array of fields which should or should not be returned.
#// 
#// @type bool $short_description Whether to return the plugin short description. Default true.
#// @type bool $description       Whether to return the plugin full description. Default false.
#// @type bool $sections          Whether to return the plugin readme sections: description, installation,
#// FAQ, screenshots, other notes, and changelog. Default false.
#// @type bool $tested            Whether to return the 'Compatible up to' value. Default true.
#// @type bool $requires          Whether to return the required WordPress version. Default true.
#// @type bool $requires_php      Whether to return the required PHP version. Default true.
#// @type bool $rating            Whether to return the rating in percent and total number of ratings.
#// Default true.
#// @type bool $ratings           Whether to return the number of rating for each star (1-5). Default true.
#// @type bool $downloaded        Whether to return the download count. Default true.
#// @type bool $downloadlink      Whether to return the download link for the package. Default true.
#// @type bool $last_updated      Whether to return the date of the last update. Default true.
#// @type bool $added             Whether to return the date when the plugin was added to the wordpress.org
#// repository. Default true.
#// @type bool $tags              Whether to return the assigned tags. Default true.
#// @type bool $compatibility     Whether to return the WordPress compatibility list. Default true.
#// @type bool $homepage          Whether to return the plugin homepage link. Default true.
#// @type bool $versions          Whether to return the list of all available versions. Default false.
#// @type bool $donate_link       Whether to return the donation link. Default true.
#// @type bool $reviews           Whether to return the plugin reviews. Default false.
#// @type bool $banners           Whether to return the banner images links. Default false.
#// @type bool $icons             Whether to return the icon links. Default false.
#// @type bool $active_installs   Whether to return the number of active installations. Default false.
#// @type bool $group             Whether to return the assigned group. Default false.
#// @type bool $contributors      Whether to return the list of contributors. Default false.
#// }
#// }
#// @return object|array|WP_Error Response object or array on success, WP_Error on failure. See the
#// {@link https://developer.wordpress.org/reference/functions/plugins_api/ function reference article}
#// for more information on the make-up of possible return values depending on the value of `$action`.
#//
def plugins_api(action_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    if php_is_array(args_):
        args_ = args_
    # end if
    if "query_plugins" == action_:
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
    #// Filters the WordPress.org Plugin Installation API arguments.
    #// 
    #// Important: An object MUST be returned to this filter.
    #// 
    #// @since 2.7.0
    #// 
    #// @param object $args   Plugin API arguments.
    #// @param string $action The type of information being requested from the Plugin Installation API.
    #//
    args_ = apply_filters("plugins_api_args", args_, action_)
    #// 
    #// Filters the response for the current WordPress.org Plugin Installation API request.
    #// 
    #// Passing a non-false value will effectively short-circuit the WordPress.org API request.
    #// 
    #// If `$action` is 'query_plugins' or 'plugin_information', an object MUST be passed.
    #// If `$action` is 'hot_tags' or 'hot_categories', an array should be passed.
    #// 
    #// @since 2.7.0
    #// 
    #// @param false|object|array $result The result object or array. Default false.
    #// @param string             $action The type of information being requested from the Plugin Installation API.
    #// @param object             $args   Plugin API arguments.
    #//
    res_ = apply_filters("plugins_api", False, action_, args_)
    if False == res_:
        url_ = "http://api.wordpress.org/plugins/info/1.2/"
        url_ = add_query_arg(Array({"action": action_, "request": args_}), url_)
        http_url_ = url_
        ssl_ = wp_http_supports(Array("ssl"))
        if ssl_:
            url_ = set_url_scheme(url_, "https")
        # end if
        http_args_ = Array({"timeout": 15, "user-agent": "WordPress/" + wp_version_ + "; " + home_url("/")})
        request_ = wp_remote_get(url_, http_args_)
        if ssl_ and is_wp_error(request_):
            trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
            request_ = wp_remote_get(http_url_, http_args_)
        # end if
        if is_wp_error(request_):
            res_ = php_new_class("WP_Error", lambda : WP_Error("plugins_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), request_.get_error_message()))
        else:
            res_ = php_json_decode(wp_remote_retrieve_body(request_), True)
            if php_is_array(res_):
                #// Object casting is required in order to match the info/1.0 format.
                res_ = res_
            elif None == res_:
                res_ = php_new_class("WP_Error", lambda : WP_Error("plugins_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), wp_remote_retrieve_body(request_)))
            # end if
            if (php_isset(lambda : res_.error)):
                res_ = php_new_class("WP_Error", lambda : WP_Error("plugins_api_failed", res_.error))
            # end if
        # end if
    elif (not is_wp_error(res_)):
        res_.external = True
    # end if
    #// 
    #// Filters the Plugin Installation API response results.
    #// 
    #// @since 2.7.0
    #// 
    #// @param object|WP_Error $res    Response object or WP_Error.
    #// @param string          $action The type of information being requested from the Plugin Installation API.
    #// @param object          $args   Plugin API arguments.
    #//
    return apply_filters("plugins_api_result", res_, action_, args_)
# end def plugins_api
#// 
#// Retrieve popular WordPress plugin tags.
#// 
#// @since 2.7.0
#// 
#// @param array $args
#// @return array
#//
def install_popular_tags(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    key_ = php_md5(serialize(args_))
    tags_ = get_site_transient("poptags_" + key_)
    if False != tags_:
        return tags_
    # end if
    tags_ = plugins_api("hot_tags", args_)
    if is_wp_error(tags_):
        return tags_
    # end if
    set_site_transient("poptags_" + key_, tags_, 3 * HOUR_IN_SECONDS)
    return tags_
# end def install_popular_tags
#// 
#// @since 2.7.0
#//
def install_dashboard(*_args_):
    
    
    php_print(" <p>\n       ")
    printf(__("Plugins extend and expand the functionality of WordPress. You may automatically install plugins from the <a href=\"%s\">WordPress Plugin Directory</a> or upload a plugin in .zip format by clicking the button at the top of this page."), __("https://wordpress.org/plugins/"))
    php_print(" </p>\n\n    ")
    display_plugins_table()
    php_print("\n   <div class=\"plugins-popular-tags-wrapper\">\n  <h2>")
    _e("Popular tags")
    php_print("</h2>\n  <p>")
    _e("You may also browse based on the most popular tags in the Plugin Directory:")
    php_print("</p>\n   ")
    api_tags_ = install_popular_tags()
    php_print("<p class=\"popular-tags\">")
    if is_wp_error(api_tags_):
        php_print(api_tags_.get_error_message())
    else:
        #// Set up the tags in a way which can be interpreted by wp_generate_tag_cloud().
        tags_ = Array()
        for tag_ in api_tags_:
            url_ = self_admin_url("plugin-install.php?tab=search&type=tag&s=" + urlencode(tag_["name"]))
            data_ = Array({"link": esc_url(url_), "name": tag_["name"], "slug": tag_["slug"], "id": sanitize_title_with_dashes(tag_["name"]), "count": tag_["count"]})
            tags_[tag_["name"]] = data_
        # end for
        php_print(wp_generate_tag_cloud(tags_, Array({"single_text": __("%s plugin"), "multiple_text": __("%s plugins")})))
    # end if
    php_print("</p><br class=\"clear\" /></div>")
# end def install_dashboard
#// 
#// Displays a search form for searching plugins.
#// 
#// @since 2.7.0
#// @since 4.6.0 The `$type_selector` parameter was deprecated.
#// 
#// @param bool $deprecated Not used.
#//
def install_search_form(deprecated_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = True
    # end if
    
    type_ = wp_unslash(PHP_REQUEST["type"]) if (php_isset(lambda : PHP_REQUEST["type"])) else "term"
    term_ = wp_unslash(PHP_REQUEST["s"]) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
    php_print(" <form class=\"search-form search-plugins\" method=\"get\">\n        <input type=\"hidden\" name=\"tab\" value=\"search\" />\n       <label class=\"screen-reader-text\" for=\"typeselector\">")
    _e("Search plugins by:")
    php_print("</label>\n       <select name=\"type\" id=\"typeselector\">\n            <option value=\"term\"")
    selected("term", type_)
    php_print(">")
    _e("Keyword")
    php_print("</option>\n          <option value=\"author\"")
    selected("author", type_)
    php_print(">")
    _e("Author")
    php_print("</option>\n          <option value=\"tag\"")
    selected("tag", type_)
    php_print(">")
    _ex("Tag", "Plugin Installer")
    php_print("</option>\n      </select>\n     <label><span class=\"screen-reader-text\">")
    _e("Search Plugins")
    php_print("</span>\n            <input type=\"search\" name=\"s\" value=\"")
    php_print(esc_attr(term_))
    php_print("\" class=\"wp-filter-search\" placeholder=\"")
    esc_attr_e("Search plugins...")
    php_print("\" />\n      </label>\n      ")
    submit_button(__("Search Plugins"), "hide-if-js", False, False, Array({"id": "search-submit"}))
    php_print(" </form>\n   ")
# end def install_search_form
#// 
#// Upload from zip
#// 
#// @since 2.8.0
#//
def install_plugins_upload(*_args_):
    
    
    php_print("<div class=\"upload-plugin\">\n  <p class=\"install-help\">")
    _e("If you have a plugin in a .zip format, you may install it by uploading it here.")
    php_print("</p>\n   <form method=\"post\" enctype=\"multipart/form-data\" class=\"wp-upload-form\" action=\"")
    php_print(self_admin_url("update.php?action=upload-plugin"))
    php_print("\">\n        ")
    wp_nonce_field("plugin-upload")
    php_print("     <label class=\"screen-reader-text\" for=\"pluginzip\">")
    _e("Plugin zip file")
    php_print("</label>\n       <input type=\"file\" id=\"pluginzip\" name=\"pluginzip\" />\n       ")
    submit_button(__("Install Now"), "", "install-plugin-submit", False)
    php_print(" </form>\n</div>\n   ")
# end def install_plugins_upload
#// 
#// Show a username form for the favorites page
#// 
#// @since 3.5.0
#//
def install_plugins_favorites_form(*_args_):
    
    
    user_ = get_user_option("wporg_favorites")
    action_ = "save_wporg_username_" + get_current_user_id()
    php_print(" <p class=\"install-help\">")
    _e("If you have marked plugins as favorites on WordPress.org, you can browse them here.")
    php_print("""</p>
    <form method=\"get\">
    <input type=\"hidden\" name=\"tab\" value=\"favorites\" />
    <p>
    <label for=\"user\">""")
    _e("Your WordPress.org username:")
    php_print("</label>\n           <input type=\"search\" id=\"user\" name=\"user\" value=\"")
    php_print(esc_attr(user_))
    php_print("\" />\n          <input type=\"submit\" class=\"button\" value=\"")
    esc_attr_e("Get Favorites")
    php_print("\" />\n          <input type=\"hidden\" id=\"wporg-username-nonce\" name=\"_wpnonce\" value=\"")
    php_print(esc_attr(wp_create_nonce(action_)))
    php_print("""\" />
    </p>
    </form>
    """)
# end def install_plugins_favorites_form
#// 
#// Display plugin content based on plugin list.
#// 
#// @since 2.7.0
#// 
#// @global WP_List_Table $wp_list_table
#//
def display_plugins_table(*_args_):
    
    
    global wp_list_table_
    php_check_if_defined("wp_list_table_")
    for case in Switch(current_filter()):
        if case("install_plugins_favorites"):
            if php_empty(lambda : PHP_REQUEST["user"]) and (not get_user_option("wporg_favorites")):
                return
            # end if
            break
        # end if
        if case("install_plugins_recommended"):
            php_print("<p>" + __("These suggestions are based on the plugins you and other users have installed.") + "</p>")
            break
        # end if
        if case("install_plugins_beta"):
            printf("<p>" + __("You are using a development version of WordPress. These feature plugins are also under development. <a href=\"%s\">Learn more</a>.") + "</p>", "https://make.wordpress.org/core/handbook/about/release-cycle/features-as-plugins/")
            break
        # end if
    # end for
    php_print(" <form id=\"plugin-filter\" method=\"post\">\n       ")
    wp_list_table_.display()
    php_print(" </form>\n   ")
# end def display_plugins_table
#// 
#// Determine the status we can perform on a plugin.
#// 
#// @since 3.0.0
#// 
#// @param  array|object $api  Data about the plugin retrieved from the API.
#// @param  bool         $loop Optional. Disable further loops. Default false.
#// @return array {
#// Plugin installation status data.
#// 
#// @type string $status  Status of a plugin. Could be one of 'install', 'update_available', 'latest_installed' or 'newer_installed'.
#// @type string $url     Plugin installation URL.
#// @type string $version The most recent version of the plugin.
#// @type string $file    Plugin filename relative to the plugins directory.
#// }
#//
def install_plugin_install_status(api_=None, loop_=None, *_args_):
    if loop_ is None:
        loop_ = False
    # end if
    
    #// This function is called recursively, $loop prevents further loops.
    if php_is_array(api_):
        api_ = api_
    # end if
    #// Default to a "new" plugin.
    status_ = "install"
    url_ = False
    update_file_ = False
    version_ = ""
    #// 
    #// Check to see if this plugin is known to be installed,
    #// and has an update awaiting it.
    #//
    update_plugins_ = get_site_transient("update_plugins")
    if (php_isset(lambda : update_plugins_.response)):
        for file_,plugin_ in update_plugins_.response:
            if plugin_.slug == api_.slug:
                status_ = "update_available"
                update_file_ = file_
                version_ = plugin_.new_version
                if current_user_can("update_plugins"):
                    url_ = wp_nonce_url(self_admin_url("update.php?action=upgrade-plugin&plugin=" + update_file_), "upgrade-plugin_" + update_file_)
                # end if
                break
            # end if
        # end for
    # end if
    if "install" == status_:
        if php_is_dir(WP_PLUGIN_DIR + "/" + api_.slug):
            installed_plugin_ = get_plugins("/" + api_.slug)
            if php_empty(lambda : installed_plugin_):
                if current_user_can("install_plugins"):
                    url_ = wp_nonce_url(self_admin_url("update.php?action=install-plugin&plugin=" + api_.slug), "install-plugin_" + api_.slug)
                # end if
            else:
                key_ = php_array_keys(installed_plugin_)
                #// Use the first plugin regardless of the name.
                #// Could have issues for multiple plugins in one directory if they share different version numbers.
                key_ = reset(key_)
                update_file_ = api_.slug + "/" + key_
                if php_version_compare(api_.version, installed_plugin_[key_]["Version"], "="):
                    status_ = "latest_installed"
                elif php_version_compare(api_.version, installed_plugin_[key_]["Version"], "<"):
                    status_ = "newer_installed"
                    version_ = installed_plugin_[key_]["Version"]
                else:
                    #// If the above update check failed, then that probably means that the update checker has out-of-date information, force a refresh.
                    if (not loop_):
                        delete_site_transient("update_plugins")
                        wp_update_plugins()
                        return install_plugin_install_status(api_, True)
                    # end if
                # end if
            # end if
        else:
            #// "install" & no directory with that slug.
            if current_user_can("install_plugins"):
                url_ = wp_nonce_url(self_admin_url("update.php?action=install-plugin&plugin=" + api_.slug), "install-plugin_" + api_.slug)
            # end if
        # end if
    # end if
    if (php_isset(lambda : PHP_REQUEST["from"])):
        url_ += "&amp;from=" + urlencode(wp_unslash(PHP_REQUEST["from"]))
    # end if
    file_ = update_file_
    return php_compact("status", "url", "version", "file")
# end def install_plugin_install_status
#// 
#// Display plugin information in dialog box form.
#// 
#// @since 2.7.0
#// 
#// @global string $tab
#//
def install_plugin_information(*_args_):
    
    
    global tab_
    php_check_if_defined("tab_")
    if php_empty(lambda : PHP_REQUEST["plugin"]):
        return
    # end if
    api_ = plugins_api("plugin_information", Array({"slug": wp_unslash(PHP_REQUEST["plugin"])}))
    if is_wp_error(api_):
        wp_die(api_)
    # end if
    plugins_allowedtags_ = Array({"a": Array({"href": Array(), "title": Array(), "target": Array()})}, {"abbr": Array({"title": Array()})}, {"acronym": Array({"title": Array()})}, {"code": Array(), "pre": Array(), "em": Array(), "strong": Array(), "div": Array({"class": Array()})}, {"span": Array({"class": Array()})}, {"p": Array(), "br": Array(), "ul": Array(), "ol": Array(), "li": Array(), "h1": Array(), "h2": Array(), "h3": Array(), "h4": Array(), "h5": Array(), "h6": Array(), "img": Array({"src": Array(), "class": Array(), "alt": Array()})}, {"blockquote": Array({"cite": True})})
    plugins_section_titles_ = Array({"description": _x("Description", "Plugin installer section title"), "installation": _x("Installation", "Plugin installer section title"), "faq": _x("FAQ", "Plugin installer section title"), "screenshots": _x("Screenshots", "Plugin installer section title"), "changelog": _x("Changelog", "Plugin installer section title"), "reviews": _x("Reviews", "Plugin installer section title"), "other_notes": _x("Other Notes", "Plugin installer section title")})
    #// Sanitize HTML.
    for section_name_,content_ in api_.sections:
        api_.sections[section_name_] = wp_kses(content_, plugins_allowedtags_)
    # end for
    for key_ in Array("version", "author", "requires", "tested", "homepage", "downloaded", "slug"):
        if (php_isset(lambda : api_.key_)):
            api_.key_ = wp_kses(api_.key_, plugins_allowedtags_)
        # end if
    # end for
    _tab_ = esc_attr(tab_)
    #// Default to the Description tab, Do not translate, API returns English.
    section_ = wp_unslash(PHP_REQUEST["section"]) if (php_isset(lambda : PHP_REQUEST["section"])) else "description"
    if php_empty(lambda : section_) or (not (php_isset(lambda : api_.sections[section_]))):
        section_titles_ = php_array_keys(api_.sections)
        section_ = reset(section_titles_)
    # end if
    iframe_header(__("Plugin Installation"))
    _with_banner_ = ""
    if (not php_empty(lambda : api_.banners)) and (not php_empty(lambda : api_.banners["low"])) or (not php_empty(lambda : api_.banners["high"])):
        _with_banner_ = "with-banner"
        low_ = api_.banners["high"] if php_empty(lambda : api_.banners["low"]) else api_.banners["low"]
        high_ = api_.banners["low"] if php_empty(lambda : api_.banners["high"]) else api_.banners["high"]
        php_print("     <style type=\"text/css\">\n         #plugin-information-title.with-banner {\n               background-image: url( ")
        php_print(esc_url(low_))
        php_print(""" );
        }
        @media only screen and ( -webkit-min-device-pixel-ratio: 1.5 ) {
        #plugin-information-title.with-banner {
        background-image: url( """)
        php_print(esc_url(high_))
        php_print(""" );
        }
        }
        </style>
        """)
    # end if
    php_print("<div id=\"plugin-information-scrollable\">")
    php_print(str("<div id='") + str(_tab_) + str("-title' class='") + str(_with_banner_) + str("'><div class='vignette'></div><h2>") + str(api_.name) + str("</h2></div>"))
    php_print(str("<div id='") + str(_tab_) + str("-tabs' class='") + str(_with_banner_) + str("'>\n"))
    for section_name_,content_ in api_.sections:
        if "reviews" == section_name_ and php_empty(lambda : api_.ratings) or 0 == array_sum(api_.ratings):
            continue
        # end if
        if (php_isset(lambda : plugins_section_titles_[section_name_])):
            title_ = plugins_section_titles_[section_name_]
        else:
            title_ = ucwords(php_str_replace("_", " ", section_name_))
        # end if
        class_ = " class=\"current\"" if section_name_ == section_ else ""
        href_ = add_query_arg(Array({"tab": tab_, "section": section_name_}))
        href_ = esc_url(href_)
        san_section_ = esc_attr(section_name_)
        php_print(str(" <a name='") + str(san_section_) + str("' href='") + str(href_) + str("' ") + str(class_) + str(">") + str(title_) + str("</a>\n"))
    # end for
    php_print("</div>\n")
    php_print("<div id=\"")
    php_print(_tab_)
    php_print("-content\" class='")
    php_print(_with_banner_)
    php_print("""'>
    <div class=\"fyi\">
    <ul>
    """)
    if (not php_empty(lambda : api_.version)):
        php_print("             <li><strong>")
        _e("Version:")
        php_print("</strong> ")
        php_print(api_.version)
        php_print("</li>\n          ")
    # end if
    if (not php_empty(lambda : api_.author)):
        php_print("             <li><strong>")
        _e("Author:")
        php_print("</strong> ")
        php_print(links_add_target(api_.author, "_blank"))
        php_print("</li>\n          ")
    # end if
    if (not php_empty(lambda : api_.last_updated)):
        php_print("             <li><strong>")
        _e("Last Updated:")
        php_print("</strong>\n                  ")
        #// translators: %s: Human-readable time difference.
        printf(__("%s ago"), human_time_diff(strtotime(api_.last_updated)))
        php_print("             </li>\n         ")
    # end if
    if (not php_empty(lambda : api_.requires)):
        php_print("             <li>\n                  <strong>")
        _e("Requires WordPress Version:")
        php_print("</strong>\n                  ")
        #// translators: %s: Version number.
        printf(__("%s or higher"), api_.requires)
        php_print("             </li>\n         ")
    # end if
    if (not php_empty(lambda : api_.tested)):
        php_print("             <li><strong>")
        _e("Compatible up to:")
        php_print("</strong> ")
        php_print(api_.tested)
        php_print("</li>\n          ")
    # end if
    if (not php_empty(lambda : api_.requires_php)):
        php_print("             <li>\n                  <strong>")
        _e("Requires PHP Version:")
        php_print("</strong>\n                  ")
        #// translators: %s: Version number.
        printf(__("%s or higher"), api_.requires_php)
        php_print("             </li>\n         ")
    # end if
    if (php_isset(lambda : api_.active_installs)):
        php_print("             <li><strong>")
        _e("Active Installations:")
        php_print("</strong>\n              ")
        if api_.active_installs >= 1000000:
            active_installs_millions_ = floor(api_.active_installs / 1000000)
            printf(_nx("%s+ Million", "%s+ Million", active_installs_millions_, "Active plugin installations"), number_format_i18n(active_installs_millions_))
        elif 0 == api_.active_installs:
            _ex("Less Than 10", "Active plugin installations")
        else:
            php_print(number_format_i18n(api_.active_installs) + "+")
        # end if
        php_print("             </li>\n         ")
    # end if
    if (not php_empty(lambda : api_.slug)) and php_empty(lambda : api_.external):
        php_print("             <li><a target=\"_blank\" href=\"")
        php_print(__("https://wordpress.org/plugins/") + api_.slug)
        php_print("/\">")
        _e("WordPress.org Plugin Page &#187;")
        php_print("</a></li>\n          ")
    # end if
    if (not php_empty(lambda : api_.homepage)):
        php_print("             <li><a target=\"_blank\" href=\"")
        php_print(esc_url(api_.homepage))
        php_print("\">")
        _e("Plugin Homepage &#187;")
        php_print("</a></li>\n          ")
    # end if
    if (not php_empty(lambda : api_.donate_link)) and php_empty(lambda : api_.contributors):
        php_print("             <li><a target=\"_blank\" href=\"")
        php_print(esc_url(api_.donate_link))
        php_print("\">")
        _e("Donate to this plugin &#187;")
        php_print("</a></li>\n          ")
    # end if
    php_print("     </ul>\n     ")
    if (not php_empty(lambda : api_.rating)):
        php_print("         <h3>")
        _e("Average Rating")
        php_print("</h3>\n          ")
        wp_star_rating(Array({"rating": api_.rating, "type": "percent", "number": api_.num_ratings}))
        php_print("         <p aria-hidden=\"true\" class=\"fyi-description\">\n                ")
        printf(_n("(based on %s rating)", "(based on %s ratings)", api_.num_ratings), number_format_i18n(api_.num_ratings))
        php_print("         </p>\n          ")
    # end if
    if (not php_empty(lambda : api_.ratings)) and array_sum(api_.ratings) > 0:
        php_print("         <h3>")
        _e("Reviews")
        php_print("</h3>\n          <p class=\"fyi-description\">")
        _e("Read all reviews on WordPress.org or write your own!")
        php_print("</p>\n           ")
        for key_,ratecount_ in api_.ratings:
            #// Avoid div-by-zero.
            _rating_ = ratecount_ / api_.num_ratings if api_.num_ratings else 0
            aria_label_ = esc_attr(php_sprintf(_n("Reviews with %1$d star: %2$s. Opens in a new tab.", "Reviews with %1$d stars: %2$s. Opens in a new tab.", key_), key_, number_format_i18n(ratecount_)))
            php_print("             <div class=\"counter-container\">\n                     <span class=\"counter-label\">\n                            ")
            printf("<a href=\"%s\" target=\"_blank\" aria-label=\"%s\">%s</a>", str("https://wordpress.org/support/plugin/") + str(api_.slug) + str("/reviews/?filter=") + str(key_), aria_label_, php_sprintf(_n("%d star", "%d stars", key_), key_))
            php_print("                     </span>\n                       <span class=\"counter-back\">\n                         <span class=\"counter-bar\" style=\"width: ")
            php_print(92 * _rating_)
            php_print("px;\"></span>\n                      </span>\n                   <span class=\"counter-count\" aria-hidden=\"true\">")
            php_print(number_format_i18n(ratecount_))
            php_print("</span>\n                </div>\n                ")
        # end for
    # end if
    if (not php_empty(lambda : api_.contributors)):
        php_print("         <h3>")
        _e("Contributors")
        php_print("</h3>\n          <ul class=\"contributors\">\n               ")
        for contrib_username_,contrib_details_ in api_.contributors:
            contrib_name_ = contrib_details_["display_name"]
            if (not contrib_name_):
                contrib_name_ = contrib_username_
            # end if
            contrib_name_ = esc_html(contrib_name_)
            contrib_profile_ = esc_url(contrib_details_["profile"])
            contrib_avatar_ = esc_url(add_query_arg("s", "36", contrib_details_["avatar"]))
            php_print(str("<li><a href='") + str(contrib_profile_) + str("' target='_blank'><img src='") + str(contrib_avatar_) + str("' width='18' height='18' alt='' />") + str(contrib_name_) + str("</a></li>"))
        # end for
        php_print("         </ul>\n                 ")
        if (not php_empty(lambda : api_.donate_link)):
            php_print("             <a target=\"_blank\" href=\"")
            php_print(esc_url(api_.donate_link))
            php_print("\">")
            _e("Donate to this plugin &#187;")
            php_print("</a>\n           ")
        # end if
        php_print("             ")
    # end if
    php_print(" </div>\n    <div id=\"section-holder\">\n   ")
    requires_php_ = api_.requires_php if (php_isset(lambda : api_.requires_php)) else None
    requires_wp_ = api_.requires if (php_isset(lambda : api_.requires)) else None
    compatible_php_ = is_php_version_compatible(requires_php_)
    compatible_wp_ = is_wp_version_compatible(requires_wp_)
    tested_wp_ = php_empty(lambda : api_.tested) or php_version_compare(get_bloginfo("version"), api_.tested, "<=")
    if (not compatible_php_):
        php_print("<div class=\"notice notice-error notice-alt\"><p>")
        _e("<strong>Error:</strong> This plugin <strong>requires a newer version of PHP</strong>.")
        if current_user_can("update_php"):
            printf(" " + __("<a href=\"%s\" target=\"_blank\">Click here to learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
            wp_update_php_annotation("</p><p><em>", "</em>")
        else:
            php_print("</p>")
        # end if
        php_print("</div>")
    # end if
    if (not tested_wp_):
        php_print("<div class=\"notice notice-warning notice-alt\"><p>")
        _e("<strong>Warning:</strong> This plugin <strong>has not been tested</strong> with your current version of WordPress.")
        php_print("</p></div>")
    elif (not compatible_wp_):
        php_print("<div class=\"notice notice-error notice-alt\"><p>")
        _e("<strong>Error:</strong> This plugin <strong>requires a newer version of WordPress</strong>.")
        if current_user_can("update_core"):
            printf(" " + __("<a href=\"%s\" target=\"_parent\">Click here to update WordPress</a>."), self_admin_url("update-core.php"))
        # end if
        php_print("</p></div>")
    # end if
    for section_name_,content_ in api_.sections:
        content_ = links_add_base_url(content_, "https://wordpress.org/plugins/" + api_.slug + "/")
        content_ = links_add_target(content_, "_blank")
        san_section_ = esc_attr(section_name_)
        display_ = "block" if section_name_ == section_ else "none"
        php_print(str(" <div id='section-") + str(san_section_) + str("' class='section' style='display: ") + str(display_) + str(";'>\n"))
        php_print(content_)
        php_print(" </div>\n")
    # end for
    php_print("</div>\n")
    php_print("</div>\n")
    php_print("</div>\n")
    #// #plugin-information-scrollable
    php_print(str("<div id='") + str(tab_) + str("-footer'>\n"))
    if (not php_empty(lambda : api_.download_link)) and current_user_can("install_plugins") or current_user_can("update_plugins"):
        status_ = install_plugin_install_status(api_)
        for case in Switch(status_["status"]):
            if case("install"):
                if status_["url"]:
                    if compatible_php_ and compatible_wp_:
                        php_print("<a data-slug=\"" + esc_attr(api_.slug) + "\" id=\"plugin_install_from_iframe\" class=\"button button-primary right\" href=\"" + status_["url"] + "\" target=\"_parent\">" + __("Install Now") + "</a>")
                    else:
                        printf("<button type=\"button\" class=\"button button-primary button-disabled right\" disabled=\"disabled\">%s</button>", _x("Cannot Install", "plugin"))
                    # end if
                # end if
                break
            # end if
            if case("update_available"):
                if status_["url"]:
                    if compatible_php_:
                        php_print("<a data-slug=\"" + esc_attr(api_.slug) + "\" data-plugin=\"" + esc_attr(status_["file"]) + "\" id=\"plugin_update_from_iframe\" class=\"button button-primary right\" href=\"" + status_["url"] + "\" target=\"_parent\">" + __("Install Update Now") + "</a>")
                    else:
                        printf("<button type=\"button\" class=\"button button-primary button-disabled right\" disabled=\"disabled\">%s</button>", _x("Cannot Update", "plugin"))
                    # end if
                # end if
                break
            # end if
            if case("newer_installed"):
                #// translators: %s: Plugin version.
                php_print("<a class=\"button button-primary right disabled\">" + php_sprintf(__("Newer Version (%s) Installed"), status_["version"]) + "</a>")
                break
            # end if
            if case("latest_installed"):
                php_print("<a class=\"button button-primary right disabled\">" + __("Latest Version Installed") + "</a>")
                break
            # end if
        # end for
    # end if
    php_print("</div>\n")
    iframe_footer()
    php_exit(0)
# end def install_plugin_information
