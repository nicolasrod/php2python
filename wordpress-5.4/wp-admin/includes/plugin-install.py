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
def plugins_api(action=None, args=Array(), *args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    if php_is_array(args):
        args = args
    # end if
    if "query_plugins" == action:
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
    #// Filters the WordPress.org Plugin Installation API arguments.
    #// 
    #// Important: An object MUST be returned to this filter.
    #// 
    #// @since 2.7.0
    #// 
    #// @param object $args   Plugin API arguments.
    #// @param string $action The type of information being requested from the Plugin Installation API.
    #//
    args = apply_filters("plugins_api_args", args, action)
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
    res = apply_filters("plugins_api", False, action, args)
    if False == res:
        url = "http://api.wordpress.org/plugins/info/1.2/"
        url = add_query_arg(Array({"action": action, "request": args}), url)
        http_url = url
        ssl = wp_http_supports(Array("ssl"))
        if ssl:
            url = set_url_scheme(url, "https")
        # end if
        http_args = Array({"timeout": 15, "user-agent": "WordPress/" + wp_version + "; " + home_url("/")})
        request = wp_remote_get(url, http_args)
        if ssl and is_wp_error(request):
            trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
            request = wp_remote_get(http_url, http_args)
        # end if
        if is_wp_error(request):
            res = php_new_class("WP_Error", lambda : WP_Error("plugins_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), request.get_error_message()))
        else:
            res = php_json_decode(wp_remote_retrieve_body(request), True)
            if php_is_array(res):
                #// Object casting is required in order to match the info/1.0 format.
                res = res
            elif None == res:
                res = php_new_class("WP_Error", lambda : WP_Error("plugins_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), wp_remote_retrieve_body(request)))
            # end if
            if (php_isset(lambda : res.error)):
                res = php_new_class("WP_Error", lambda : WP_Error("plugins_api_failed", res.error))
            # end if
        # end if
    elif (not is_wp_error(res)):
        res.external = True
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
    return apply_filters("plugins_api_result", res, action, args)
# end def plugins_api
#// 
#// Retrieve popular WordPress plugin tags.
#// 
#// @since 2.7.0
#// 
#// @param array $args
#// @return array
#//
def install_popular_tags(args=Array(), *args_):
    
    key = php_md5(serialize(args))
    tags = get_site_transient("poptags_" + key)
    if False != tags:
        return tags
    # end if
    tags = plugins_api("hot_tags", args)
    if is_wp_error(tags):
        return tags
    # end if
    set_site_transient("poptags_" + key, tags, 3 * HOUR_IN_SECONDS)
    return tags
# end def install_popular_tags
#// 
#// @since 2.7.0
#//
def install_dashboard(*args_):
    
    php_print(" <p>\n       ")
    printf(__("Plugins extend and expand the functionality of WordPress. You may automatically install plugins from the <a href=\"%s\">WordPress Plugin Directory</a> or upload a plugin in .zip format by clicking the button at the top of this page."), __("https://wordpress.org/plugins/"))
    php_print(" </p>\n\n    ")
    display_plugins_table()
    php_print("\n   <div class=\"plugins-popular-tags-wrapper\">\n  <h2>")
    _e("Popular tags")
    php_print("</h2>\n  <p>")
    _e("You may also browse based on the most popular tags in the Plugin Directory:")
    php_print("</p>\n   ")
    api_tags = install_popular_tags()
    php_print("<p class=\"popular-tags\">")
    if is_wp_error(api_tags):
        php_print(api_tags.get_error_message())
    else:
        #// Set up the tags in a way which can be interpreted by wp_generate_tag_cloud().
        tags = Array()
        for tag in api_tags:
            url = self_admin_url("plugin-install.php?tab=search&type=tag&s=" + urlencode(tag["name"]))
            data = Array({"link": esc_url(url), "name": tag["name"], "slug": tag["slug"], "id": sanitize_title_with_dashes(tag["name"]), "count": tag["count"]})
            tags[tag["name"]] = data
        # end for
        php_print(wp_generate_tag_cloud(tags, Array({"single_text": __("%s plugin"), "multiple_text": __("%s plugins")})))
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
def install_search_form(deprecated=True, *args_):
    
    type = wp_unslash(PHP_REQUEST["type"]) if (php_isset(lambda : PHP_REQUEST["type"])) else "term"
    term = wp_unslash(PHP_REQUEST["s"]) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
    php_print(" <form class=\"search-form search-plugins\" method=\"get\">\n        <input type=\"hidden\" name=\"tab\" value=\"search\" />\n       <label class=\"screen-reader-text\" for=\"typeselector\">")
    _e("Search plugins by:")
    php_print("</label>\n       <select name=\"type\" id=\"typeselector\">\n            <option value=\"term\"")
    selected("term", type)
    php_print(">")
    _e("Keyword")
    php_print("</option>\n          <option value=\"author\"")
    selected("author", type)
    php_print(">")
    _e("Author")
    php_print("</option>\n          <option value=\"tag\"")
    selected("tag", type)
    php_print(">")
    _ex("Tag", "Plugin Installer")
    php_print("</option>\n      </select>\n     <label><span class=\"screen-reader-text\">")
    _e("Search Plugins")
    php_print("</span>\n            <input type=\"search\" name=\"s\" value=\"")
    php_print(esc_attr(term))
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
def install_plugins_upload(*args_):
    
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
def install_plugins_favorites_form(*args_):
    
    user = get_user_option("wporg_favorites")
    action = "save_wporg_username_" + get_current_user_id()
    php_print(" <p class=\"install-help\">")
    _e("If you have marked plugins as favorites on WordPress.org, you can browse them here.")
    php_print("""</p>
    <form method=\"get\">
    <input type=\"hidden\" name=\"tab\" value=\"favorites\" />
    <p>
    <label for=\"user\">""")
    _e("Your WordPress.org username:")
    php_print("</label>\n           <input type=\"search\" id=\"user\" name=\"user\" value=\"")
    php_print(esc_attr(user))
    php_print("\" />\n          <input type=\"submit\" class=\"button\" value=\"")
    esc_attr_e("Get Favorites")
    php_print("\" />\n          <input type=\"hidden\" id=\"wporg-username-nonce\" name=\"_wpnonce\" value=\"")
    php_print(esc_attr(wp_create_nonce(action)))
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
def display_plugins_table(*args_):
    
    global wp_list_table
    php_check_if_defined("wp_list_table")
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
    wp_list_table.display()
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
def install_plugin_install_status(api=None, loop=False, *args_):
    
    #// This function is called recursively, $loop prevents further loops.
    if php_is_array(api):
        api = api
    # end if
    #// Default to a "new" plugin.
    status = "install"
    url = False
    update_file = False
    version = ""
    #// 
    #// Check to see if this plugin is known to be installed,
    #// and has an update awaiting it.
    #//
    update_plugins = get_site_transient("update_plugins")
    if (php_isset(lambda : update_plugins.response)):
        for file,plugin in update_plugins.response:
            if plugin.slug == api.slug:
                status = "update_available"
                update_file = file
                version = plugin.new_version
                if current_user_can("update_plugins"):
                    url = wp_nonce_url(self_admin_url("update.php?action=upgrade-plugin&plugin=" + update_file), "upgrade-plugin_" + update_file)
                # end if
                break
            # end if
        # end for
    # end if
    if "install" == status:
        if php_is_dir(WP_PLUGIN_DIR + "/" + api.slug):
            installed_plugin = get_plugins("/" + api.slug)
            if php_empty(lambda : installed_plugin):
                if current_user_can("install_plugins"):
                    url = wp_nonce_url(self_admin_url("update.php?action=install-plugin&plugin=" + api.slug), "install-plugin_" + api.slug)
                # end if
            else:
                key = php_array_keys(installed_plugin)
                #// Use the first plugin regardless of the name.
                #// Could have issues for multiple plugins in one directory if they share different version numbers.
                key = reset(key)
                update_file = api.slug + "/" + key
                if php_version_compare(api.version, installed_plugin[key]["Version"], "="):
                    status = "latest_installed"
                elif php_version_compare(api.version, installed_plugin[key]["Version"], "<"):
                    status = "newer_installed"
                    version = installed_plugin[key]["Version"]
                else:
                    #// If the above update check failed, then that probably means that the update checker has out-of-date information, force a refresh.
                    if (not loop):
                        delete_site_transient("update_plugins")
                        wp_update_plugins()
                        return install_plugin_install_status(api, True)
                    # end if
                # end if
            # end if
        else:
            #// "install" & no directory with that slug.
            if current_user_can("install_plugins"):
                url = wp_nonce_url(self_admin_url("update.php?action=install-plugin&plugin=" + api.slug), "install-plugin_" + api.slug)
            # end if
        # end if
    # end if
    if (php_isset(lambda : PHP_REQUEST["from"])):
        url += "&amp;from=" + urlencode(wp_unslash(PHP_REQUEST["from"]))
    # end if
    file = update_file
    return compact("status", "url", "version", "file")
# end def install_plugin_install_status
#// 
#// Display plugin information in dialog box form.
#// 
#// @since 2.7.0
#// 
#// @global string $tab
#//
def install_plugin_information(*args_):
    
    global tab
    php_check_if_defined("tab")
    if php_empty(lambda : PHP_REQUEST["plugin"]):
        return
    # end if
    api = plugins_api("plugin_information", Array({"slug": wp_unslash(PHP_REQUEST["plugin"])}))
    if is_wp_error(api):
        wp_die(api)
    # end if
    plugins_allowedtags = Array({"a": Array({"href": Array(), "title": Array(), "target": Array()})}, {"abbr": Array({"title": Array()})}, {"acronym": Array({"title": Array()})}, {"code": Array(), "pre": Array(), "em": Array(), "strong": Array(), "div": Array({"class": Array()})}, {"span": Array({"class": Array()})}, {"p": Array(), "br": Array(), "ul": Array(), "ol": Array(), "li": Array(), "h1": Array(), "h2": Array(), "h3": Array(), "h4": Array(), "h5": Array(), "h6": Array(), "img": Array({"src": Array(), "class": Array(), "alt": Array()})}, {"blockquote": Array({"cite": True})})
    plugins_section_titles = Array({"description": _x("Description", "Plugin installer section title"), "installation": _x("Installation", "Plugin installer section title"), "faq": _x("FAQ", "Plugin installer section title"), "screenshots": _x("Screenshots", "Plugin installer section title"), "changelog": _x("Changelog", "Plugin installer section title"), "reviews": _x("Reviews", "Plugin installer section title"), "other_notes": _x("Other Notes", "Plugin installer section title")})
    #// Sanitize HTML.
    for section_name,content in api.sections:
        api.sections[section_name] = wp_kses(content, plugins_allowedtags)
    # end for
    for key in Array("version", "author", "requires", "tested", "homepage", "downloaded", "slug"):
        if (php_isset(lambda : api.key)):
            api.key = wp_kses(api.key, plugins_allowedtags)
        # end if
    # end for
    _tab = esc_attr(tab)
    #// Default to the Description tab, Do not translate, API returns English.
    section = wp_unslash(PHP_REQUEST["section"]) if (php_isset(lambda : PHP_REQUEST["section"])) else "description"
    if php_empty(lambda : section) or (not (php_isset(lambda : api.sections[section]))):
        section_titles = php_array_keys(api.sections)
        section = reset(section_titles)
    # end if
    iframe_header(__("Plugin Installation"))
    _with_banner = ""
    if (not php_empty(lambda : api.banners)) and (not php_empty(lambda : api.banners["low"])) or (not php_empty(lambda : api.banners["high"])):
        _with_banner = "with-banner"
        low = api.banners["high"] if php_empty(lambda : api.banners["low"]) else api.banners["low"]
        high = api.banners["low"] if php_empty(lambda : api.banners["high"]) else api.banners["high"]
        php_print("     <style type=\"text/css\">\n         #plugin-information-title.with-banner {\n               background-image: url( ")
        php_print(esc_url(low))
        php_print(""" );
        }
        @media only screen and ( -webkit-min-device-pixel-ratio: 1.5 ) {
        #plugin-information-title.with-banner {
        background-image: url( """)
        php_print(esc_url(high))
        php_print(""" );
        }
        }
        </style>
        """)
    # end if
    php_print("<div id=\"plugin-information-scrollable\">")
    php_print(str("<div id='") + str(_tab) + str("-title' class='") + str(_with_banner) + str("'><div class='vignette'></div><h2>") + str(api.name) + str("</h2></div>"))
    php_print(str("<div id='") + str(_tab) + str("-tabs' class='") + str(_with_banner) + str("'>\n"))
    for section_name,content in api.sections:
        if "reviews" == section_name and php_empty(lambda : api.ratings) or 0 == array_sum(api.ratings):
            continue
        # end if
        if (php_isset(lambda : plugins_section_titles[section_name])):
            title = plugins_section_titles[section_name]
        else:
            title = ucwords(php_str_replace("_", " ", section_name))
        # end if
        class_ = " class=\"current\"" if section_name == section else ""
        href = add_query_arg(Array({"tab": tab, "section": section_name}))
        href = esc_url(href)
        san_section = esc_attr(section_name)
        php_print(str(" <a name='") + str(san_section) + str("' href='") + str(href) + str("' ") + str(class_) + str(">") + str(title) + str("</a>\n"))
    # end for
    php_print("</div>\n")
    php_print("<div id=\"")
    php_print(_tab)
    php_print("-content\" class='")
    php_print(_with_banner)
    php_print("""'>
    <div class=\"fyi\">
    <ul>
    """)
    if (not php_empty(lambda : api.version)):
        php_print("             <li><strong>")
        _e("Version:")
        php_print("</strong> ")
        php_print(api.version)
        php_print("</li>\n          ")
    # end if
    if (not php_empty(lambda : api.author)):
        php_print("             <li><strong>")
        _e("Author:")
        php_print("</strong> ")
        php_print(links_add_target(api.author, "_blank"))
        php_print("</li>\n          ")
    # end if
    if (not php_empty(lambda : api.last_updated)):
        php_print("             <li><strong>")
        _e("Last Updated:")
        php_print("</strong>\n                  ")
        #// translators: %s: Human-readable time difference.
        printf(__("%s ago"), human_time_diff(strtotime(api.last_updated)))
        php_print("             </li>\n         ")
    # end if
    if (not php_empty(lambda : api.requires)):
        php_print("             <li>\n                  <strong>")
        _e("Requires WordPress Version:")
        php_print("</strong>\n                  ")
        #// translators: %s: Version number.
        printf(__("%s or higher"), api.requires)
        php_print("             </li>\n         ")
    # end if
    if (not php_empty(lambda : api.tested)):
        php_print("             <li><strong>")
        _e("Compatible up to:")
        php_print("</strong> ")
        php_print(api.tested)
        php_print("</li>\n          ")
    # end if
    if (not php_empty(lambda : api.requires_php)):
        php_print("             <li>\n                  <strong>")
        _e("Requires PHP Version:")
        php_print("</strong>\n                  ")
        #// translators: %s: Version number.
        printf(__("%s or higher"), api.requires_php)
        php_print("             </li>\n         ")
    # end if
    if (php_isset(lambda : api.active_installs)):
        php_print("             <li><strong>")
        _e("Active Installations:")
        php_print("</strong>\n              ")
        if api.active_installs >= 1000000:
            active_installs_millions = floor(api.active_installs / 1000000)
            printf(_nx("%s+ Million", "%s+ Million", active_installs_millions, "Active plugin installations"), number_format_i18n(active_installs_millions))
        elif 0 == api.active_installs:
            _ex("Less Than 10", "Active plugin installations")
        else:
            php_print(number_format_i18n(api.active_installs) + "+")
        # end if
        php_print("             </li>\n         ")
    # end if
    if (not php_empty(lambda : api.slug)) and php_empty(lambda : api.external):
        php_print("             <li><a target=\"_blank\" href=\"")
        php_print(__("https://wordpress.org/plugins/") + api.slug)
        php_print("/\">")
        _e("WordPress.org Plugin Page &#187;")
        php_print("</a></li>\n          ")
    # end if
    if (not php_empty(lambda : api.homepage)):
        php_print("             <li><a target=\"_blank\" href=\"")
        php_print(esc_url(api.homepage))
        php_print("\">")
        _e("Plugin Homepage &#187;")
        php_print("</a></li>\n          ")
    # end if
    if (not php_empty(lambda : api.donate_link)) and php_empty(lambda : api.contributors):
        php_print("             <li><a target=\"_blank\" href=\"")
        php_print(esc_url(api.donate_link))
        php_print("\">")
        _e("Donate to this plugin &#187;")
        php_print("</a></li>\n          ")
    # end if
    php_print("     </ul>\n     ")
    if (not php_empty(lambda : api.rating)):
        php_print("         <h3>")
        _e("Average Rating")
        php_print("</h3>\n          ")
        wp_star_rating(Array({"rating": api.rating, "type": "percent", "number": api.num_ratings}))
        php_print("         <p aria-hidden=\"true\" class=\"fyi-description\">\n                ")
        printf(_n("(based on %s rating)", "(based on %s ratings)", api.num_ratings), number_format_i18n(api.num_ratings))
        php_print("         </p>\n          ")
    # end if
    if (not php_empty(lambda : api.ratings)) and array_sum(api.ratings) > 0:
        php_print("         <h3>")
        _e("Reviews")
        php_print("</h3>\n          <p class=\"fyi-description\">")
        _e("Read all reviews on WordPress.org or write your own!")
        php_print("</p>\n           ")
        for key,ratecount in api.ratings:
            #// Avoid div-by-zero.
            _rating = ratecount / api.num_ratings if api.num_ratings else 0
            aria_label = esc_attr(php_sprintf(_n("Reviews with %1$d star: %2$s. Opens in a new tab.", "Reviews with %1$d stars: %2$s. Opens in a new tab.", key), key, number_format_i18n(ratecount)))
            php_print("             <div class=\"counter-container\">\n                     <span class=\"counter-label\">\n                            ")
            printf("<a href=\"%s\" target=\"_blank\" aria-label=\"%s\">%s</a>", str("https://wordpress.org/support/plugin/") + str(api.slug) + str("/reviews/?filter=") + str(key), aria_label, php_sprintf(_n("%d star", "%d stars", key), key))
            php_print("                     </span>\n                       <span class=\"counter-back\">\n                         <span class=\"counter-bar\" style=\"width: ")
            php_print(92 * _rating)
            php_print("px;\"></span>\n                      </span>\n                   <span class=\"counter-count\" aria-hidden=\"true\">")
            php_print(number_format_i18n(ratecount))
            php_print("</span>\n                </div>\n                ")
        # end for
    # end if
    if (not php_empty(lambda : api.contributors)):
        php_print("         <h3>")
        _e("Contributors")
        php_print("</h3>\n          <ul class=\"contributors\">\n               ")
        for contrib_username,contrib_details in api.contributors:
            contrib_name = contrib_details["display_name"]
            if (not contrib_name):
                contrib_name = contrib_username
            # end if
            contrib_name = esc_html(contrib_name)
            contrib_profile = esc_url(contrib_details["profile"])
            contrib_avatar = esc_url(add_query_arg("s", "36", contrib_details["avatar"]))
            php_print(str("<li><a href='") + str(contrib_profile) + str("' target='_blank'><img src='") + str(contrib_avatar) + str("' width='18' height='18' alt='' />") + str(contrib_name) + str("</a></li>"))
        # end for
        php_print("         </ul>\n                 ")
        if (not php_empty(lambda : api.donate_link)):
            php_print("             <a target=\"_blank\" href=\"")
            php_print(esc_url(api.donate_link))
            php_print("\">")
            _e("Donate to this plugin &#187;")
            php_print("</a>\n           ")
        # end if
        php_print("             ")
    # end if
    php_print(" </div>\n    <div id=\"section-holder\">\n   ")
    requires_php = api.requires_php if (php_isset(lambda : api.requires_php)) else None
    requires_wp = api.requires if (php_isset(lambda : api.requires)) else None
    compatible_php = is_php_version_compatible(requires_php)
    compatible_wp = is_wp_version_compatible(requires_wp)
    tested_wp = php_empty(lambda : api.tested) or php_version_compare(get_bloginfo("version"), api.tested, "<=")
    if (not compatible_php):
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
    if (not tested_wp):
        php_print("<div class=\"notice notice-warning notice-alt\"><p>")
        _e("<strong>Warning:</strong> This plugin <strong>has not been tested</strong> with your current version of WordPress.")
        php_print("</p></div>")
    elif (not compatible_wp):
        php_print("<div class=\"notice notice-error notice-alt\"><p>")
        _e("<strong>Error:</strong> This plugin <strong>requires a newer version of WordPress</strong>.")
        if current_user_can("update_core"):
            printf(" " + __("<a href=\"%s\" target=\"_parent\">Click here to update WordPress</a>."), self_admin_url("update-core.php"))
        # end if
        php_print("</p></div>")
    # end if
    for section_name,content in api.sections:
        content = links_add_base_url(content, "https://wordpress.org/plugins/" + api.slug + "/")
        content = links_add_target(content, "_blank")
        san_section = esc_attr(section_name)
        display = "block" if section_name == section else "none"
        php_print(str(" <div id='section-") + str(san_section) + str("' class='section' style='display: ") + str(display) + str(";'>\n"))
        php_print(content)
        php_print(" </div>\n")
    # end for
    php_print("</div>\n")
    php_print("</div>\n")
    php_print("</div>\n")
    #// #plugin-information-scrollable
    php_print(str("<div id='") + str(tab) + str("-footer'>\n"))
    if (not php_empty(lambda : api.download_link)) and current_user_can("install_plugins") or current_user_can("update_plugins"):
        status = install_plugin_install_status(api)
        for case in Switch(status["status"]):
            if case("install"):
                if status["url"]:
                    if compatible_php and compatible_wp:
                        php_print("<a data-slug=\"" + esc_attr(api.slug) + "\" id=\"plugin_install_from_iframe\" class=\"button button-primary right\" href=\"" + status["url"] + "\" target=\"_parent\">" + __("Install Now") + "</a>")
                    else:
                        printf("<button type=\"button\" class=\"button button-primary button-disabled right\" disabled=\"disabled\">%s</button>", _x("Cannot Install", "plugin"))
                    # end if
                # end if
                break
            # end if
            if case("update_available"):
                if status["url"]:
                    if compatible_php:
                        php_print("<a data-slug=\"" + esc_attr(api.slug) + "\" data-plugin=\"" + esc_attr(status["file"]) + "\" id=\"plugin_update_from_iframe\" class=\"button button-primary right\" href=\"" + status["url"] + "\" target=\"_parent\">" + __("Install Update Now") + "</a>")
                    else:
                        printf("<button type=\"button\" class=\"button button-primary button-disabled right\" disabled=\"disabled\">%s</button>", _x("Cannot Update", "plugin"))
                    # end if
                # end if
                break
            # end if
            if case("newer_installed"):
                #// translators: %s: Plugin version.
                php_print("<a class=\"button button-primary right disabled\">" + php_sprintf(__("Newer Version (%s) Installed"), status["version"]) + "</a>")
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
