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
#// Class for providing debug data based on a users WordPress environment.
#// 
#// @package WordPress
#// @subpackage Site_Health
#// @since 5.2.0
#//
class WP_Debug_Data():
    #// 
    #// Calls all core functions to check for updates.
    #// 
    #// @since 5.2.0
    #//
    def check_for_updates(self):
        
        wp_version_check()
        wp_update_plugins()
        wp_update_themes()
    # end def check_for_updates
    #// 
    #// Static function for generating site debug data when required.
    #// 
    #// @since 5.2.0
    #// 
    #// @throws ImagickException
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @return array The debug data for the site.
    #//
    def debug_data(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// Save few function calls.
        upload_dir = wp_upload_dir()
        permalink_structure = get_option("permalink_structure")
        is_ssl = is_ssl()
        users_can_register = get_option("users_can_register")
        default_comment_status = get_option("default_comment_status")
        is_multisite = is_multisite()
        core_version = get_bloginfo("version")
        core_updates = get_core_updates()
        core_update_needed = ""
        for core,update in core_updates:
            if "upgrade" == update.response:
                #// translators: %s: Latest WordPress version number.
                core_update_needed = " " + php_sprintf(__("(Latest version: %s)"), update.version)
            else:
                core_update_needed = ""
            # end if
        # end for
        #// Set up the array that holds all debug information.
        info = Array()
        info["wp-core"] = Array({"label": __("WordPress"), "fields": Array({"version": Array({"label": __("Version"), "value": core_version + core_update_needed, "debug": core_version})}, {"site_language": Array({"label": __("Site Language"), "value": get_locale()})}, {"user_language": Array({"label": __("User Language"), "value": get_user_locale()})}, {"timezone": Array({"label": __("Timezone"), "value": wp_timezone_string()})}, {"home_url": Array({"label": __("Home URL"), "value": get_bloginfo("url"), "private": True})}, {"site_url": Array({"label": __("Site URL"), "value": get_bloginfo("wpurl"), "private": True})}, {"permalink": Array({"label": __("Permalink structure"), "value": permalink_structure if permalink_structure else __("No permalink structure set"), "debug": permalink_structure})}, {"https_status": Array({"label": __("Is this site using HTTPS?"), "value": __("Yes") if is_ssl else __("No"), "debug": is_ssl})}, {"user_registration": Array({"label": __("Can anyone register on this site?"), "value": __("Yes") if users_can_register else __("No"), "debug": users_can_register})}, {"default_comment_status": Array({"label": __("Default comment status"), "value": _x("Open", "comment status") if "open" == default_comment_status else _x("Closed", "comment status"), "debug": default_comment_status})}, {"multisite": Array({"label": __("Is this a multisite?"), "value": __("Yes") if is_multisite else __("No"), "debug": is_multisite})})})
        if (not is_multisite):
            info["wp-paths-sizes"] = Array({"label": __("Directories and Sizes"), "fields": Array()})
        # end if
        info["wp-dropins"] = Array({"label": __("Drop-ins"), "show_count": True, "description": php_sprintf(__("Drop-ins are single files, found in the %s directory, that replace or enhance WordPress features in ways that are not possible for traditional plugins."), "<code>" + php_str_replace(ABSPATH, "", WP_CONTENT_DIR) + "</code>"), "fields": Array()})
        info["wp-active-theme"] = Array({"label": __("Active Theme"), "fields": Array()})
        info["wp-parent-theme"] = Array({"label": __("Parent Theme"), "fields": Array()})
        info["wp-themes-inactive"] = Array({"label": __("Inactive Themes"), "show_count": True, "fields": Array()})
        info["wp-mu-plugins"] = Array({"label": __("Must Use Plugins"), "show_count": True, "fields": Array()})
        info["wp-plugins-active"] = Array({"label": __("Active Plugins"), "show_count": True, "fields": Array()})
        info["wp-plugins-inactive"] = Array({"label": __("Inactive Plugins"), "show_count": True, "fields": Array()})
        info["wp-media"] = Array({"label": __("Media Handling"), "fields": Array()})
        info["wp-server"] = Array({"label": __("Server"), "description": __("The options shown below relate to your server setup. If changes are required, you may need your web host&#8217;s assistance."), "fields": Array()})
        info["wp-database"] = Array({"label": __("Database"), "fields": Array()})
        #// Check if WP_DEBUG_LOG is set.
        wp_debug_log_value = __("Disabled")
        if php_is_string(WP_DEBUG_LOG):
            wp_debug_log_value = WP_DEBUG_LOG
        elif WP_DEBUG_LOG:
            wp_debug_log_value = __("Enabled")
        # end if
        #// Check CONCATENATE_SCRIPTS.
        if php_defined("CONCATENATE_SCRIPTS"):
            concatenate_scripts = __("Enabled") if CONCATENATE_SCRIPTS else __("Disabled")
            concatenate_scripts_debug = "true" if CONCATENATE_SCRIPTS else "false"
        else:
            concatenate_scripts = __("Undefined")
            concatenate_scripts_debug = "undefined"
        # end if
        #// Check COMPRESS_SCRIPTS.
        if php_defined("COMPRESS_SCRIPTS"):
            compress_scripts = __("Enabled") if COMPRESS_SCRIPTS else __("Disabled")
            compress_scripts_debug = "true" if COMPRESS_SCRIPTS else "false"
        else:
            compress_scripts = __("Undefined")
            compress_scripts_debug = "undefined"
        # end if
        #// Check COMPRESS_CSS.
        if php_defined("COMPRESS_CSS"):
            compress_css = __("Enabled") if COMPRESS_CSS else __("Disabled")
            compress_css_debug = "true" if COMPRESS_CSS else "false"
        else:
            compress_css = __("Undefined")
            compress_css_debug = "undefined"
        # end if
        #// Check WP_LOCAL_DEV.
        if php_defined("WP_LOCAL_DEV"):
            wp_local_dev = __("Enabled") if WP_LOCAL_DEV else __("Disabled")
            wp_local_dev_debug = "true" if WP_LOCAL_DEV else "false"
        else:
            wp_local_dev = __("Undefined")
            wp_local_dev_debug = "undefined"
        # end if
        info["wp-constants"] = Array({"label": __("WordPress Constants"), "description": __("These settings alter where and how parts of WordPress are loaded."), "fields": Array({"ABSPATH": Array({"label": "ABSPATH", "value": ABSPATH, "private": True})}, {"WP_HOME": Array({"label": "WP_HOME", "value": WP_HOME if php_defined("WP_HOME") else __("Undefined"), "debug": WP_HOME if php_defined("WP_HOME") else "undefined"})}, {"WP_SITEURL": Array({"label": "WP_SITEURL", "value": WP_SITEURL if php_defined("WP_SITEURL") else __("Undefined"), "debug": WP_SITEURL if php_defined("WP_SITEURL") else "undefined"})}, {"WP_CONTENT_DIR": Array({"label": "WP_CONTENT_DIR", "value": WP_CONTENT_DIR})}, {"WP_PLUGIN_DIR": Array({"label": "WP_PLUGIN_DIR", "value": WP_PLUGIN_DIR})}, {"WP_MAX_MEMORY_LIMIT": Array({"label": "WP_MAX_MEMORY_LIMIT", "value": WP_MAX_MEMORY_LIMIT})}, {"WP_DEBUG": Array({"label": "WP_DEBUG", "value": __("Enabled") if WP_DEBUG else __("Disabled"), "debug": WP_DEBUG})}, {"WP_DEBUG_DISPLAY": Array({"label": "WP_DEBUG_DISPLAY", "value": __("Enabled") if WP_DEBUG_DISPLAY else __("Disabled"), "debug": WP_DEBUG_DISPLAY})}, {"WP_DEBUG_LOG": Array({"label": "WP_DEBUG_LOG", "value": wp_debug_log_value, "debug": WP_DEBUG_LOG})}, {"SCRIPT_DEBUG": Array({"label": "SCRIPT_DEBUG", "value": __("Enabled") if SCRIPT_DEBUG else __("Disabled"), "debug": SCRIPT_DEBUG})}, {"WP_CACHE": Array({"label": "WP_CACHE", "value": __("Enabled") if WP_CACHE else __("Disabled"), "debug": WP_CACHE})}, {"CONCATENATE_SCRIPTS": Array({"label": "CONCATENATE_SCRIPTS", "value": concatenate_scripts, "debug": concatenate_scripts_debug})}, {"COMPRESS_SCRIPTS": Array({"label": "COMPRESS_SCRIPTS", "value": compress_scripts, "debug": compress_scripts_debug})}, {"COMPRESS_CSS": Array({"label": "COMPRESS_CSS", "value": compress_css, "debug": compress_css_debug})}, {"WP_LOCAL_DEV": Array({"label": "WP_LOCAL_DEV", "value": wp_local_dev, "debug": wp_local_dev_debug})}, {"DB_CHARSET": Array({"label": "DB_CHARSET", "value": DB_CHARSET if php_defined("DB_CHARSET") else __("Undefined"), "debug": DB_CHARSET if php_defined("DB_CHARSET") else "undefined"})}, {"DB_COLLATE": Array({"label": "DB_COLLATE", "value": DB_COLLATE if php_defined("DB_COLLATE") else __("Undefined"), "debug": DB_COLLATE if php_defined("DB_COLLATE") else "undefined"})})})
        is_writable_abspath = wp_is_writable(ABSPATH)
        is_writable_wp_content_dir = wp_is_writable(WP_CONTENT_DIR)
        is_writable_upload_dir = wp_is_writable(upload_dir["basedir"])
        is_writable_wp_plugin_dir = wp_is_writable(WP_PLUGIN_DIR)
        is_writable_template_directory = wp_is_writable(get_template_directory() + "/..")
        info["wp-filesystem"] = Array({"label": __("Filesystem Permissions"), "description": __("Shows whether WordPress is able to write to the directories it needs access to."), "fields": Array({"wordpress": Array({"label": __("The main WordPress directory"), "value": __("Writable") if is_writable_abspath else __("Not writable"), "debug": "writable" if is_writable_abspath else "not writable"})}, {"wp-content": Array({"label": __("The wp-content directory"), "value": __("Writable") if is_writable_wp_content_dir else __("Not writable"), "debug": "writable" if is_writable_wp_content_dir else "not writable"})}, {"uploads": Array({"label": __("The uploads directory"), "value": __("Writable") if is_writable_upload_dir else __("Not writable"), "debug": "writable" if is_writable_upload_dir else "not writable"})}, {"plugins": Array({"label": __("The plugins directory"), "value": __("Writable") if is_writable_wp_plugin_dir else __("Not writable"), "debug": "writable" if is_writable_wp_plugin_dir else "not writable"})}, {"themes": Array({"label": __("The themes directory"), "value": __("Writable") if is_writable_template_directory else __("Not writable"), "debug": "writable" if is_writable_template_directory else "not writable"})})})
        #// Conditionally add debug information for multisite setups.
        if is_multisite():
            network_query = php_new_class("WP_Network_Query", lambda : WP_Network_Query())
            network_ids = network_query.query(Array({"fields": "ids", "number": 100, "no_found_rows": False}))
            site_count = 0
            for network_id in network_ids:
                site_count += get_blog_count(network_id)
            # end for
            info["wp-core"]["fields"]["user_count"] = Array({"label": __("User count"), "value": get_user_count()})
            info["wp-core"]["fields"]["site_count"] = Array({"label": __("Site count"), "value": site_count})
            info["wp-core"]["fields"]["network_count"] = Array({"label": __("Network count"), "value": network_query.found_networks})
        else:
            user_count = count_users()
            info["wp-core"]["fields"]["user_count"] = Array({"label": __("User count"), "value": user_count["total_users"]})
        # end if
        #// WordPress features requiring processing.
        wp_dotorg = wp_remote_get("https://wordpress.org", Array({"timeout": 10}))
        if (not is_wp_error(wp_dotorg)):
            info["wp-core"]["fields"]["dotorg_communication"] = Array({"label": __("Communication with WordPress.org"), "value": __("WordPress.org is reachable"), "debug": "true"})
        else:
            info["wp-core"]["fields"]["dotorg_communication"] = Array({"label": __("Communication with WordPress.org"), "value": php_sprintf(__("Unable to reach WordPress.org at %1$s: %2$s"), gethostbyname("wordpress.org"), wp_dotorg.get_error_message()), "debug": wp_dotorg.get_error_message()})
        # end if
        #// Remove accordion for Directories and Sizes if in Multisite.
        if (not is_multisite):
            loading = __("Loading&hellip;")
            info["wp-paths-sizes"]["fields"] = Array({"wordpress_path": Array({"label": __("WordPress directory location"), "value": untrailingslashit(ABSPATH)})}, {"wordpress_size": Array({"label": __("WordPress directory size"), "value": loading, "debug": "loading..."})}, {"uploads_path": Array({"label": __("Uploads directory location"), "value": upload_dir["basedir"]})}, {"uploads_size": Array({"label": __("Uploads directory size"), "value": loading, "debug": "loading..."})}, {"themes_path": Array({"label": __("Themes directory location"), "value": get_theme_root()})}, {"themes_size": Array({"label": __("Themes directory size"), "value": loading, "debug": "loading..."})}, {"plugins_path": Array({"label": __("Plugins directory location"), "value": WP_PLUGIN_DIR})}, {"plugins_size": Array({"label": __("Plugins directory size"), "value": loading, "debug": "loading..."})}, {"database_size": Array({"label": __("Database size"), "value": loading, "debug": "loading..."})}, {"total_size": Array({"label": __("Total installation size"), "value": loading, "debug": "loading..."})})
        # end if
        #// Get a list of all drop-in replacements.
        dropins = get_dropins()
        #// Get dropins descriptions.
        dropin_descriptions = _get_dropins()
        #// Spare few function calls.
        not_available = __("Not available")
        for dropin_key,dropin in dropins:
            info["wp-dropins"]["fields"][sanitize_text_field(dropin_key)] = Array({"label": dropin_key, "value": dropin_descriptions[dropin_key][0], "debug": "true"})
        # end for
        #// Populate the media fields.
        info["wp-media"]["fields"]["image_editor"] = Array({"label": __("Active editor"), "value": _wp_image_editor_choose()})
        #// Get ImageMagic information, if available.
        if php_class_exists("Imagick"):
            #// Save the Imagick instance for later use.
            imagick = php_new_class("Imagick", lambda : Imagick())
            imagick_version = imagick.getversion()
        else:
            imagick_version = __("Not available")
        # end if
        info["wp-media"]["fields"]["imagick_module_version"] = Array({"label": __("ImageMagick version number"), "value": imagick_version["versionNumber"] if php_is_array(imagick_version) else imagick_version})
        info["wp-media"]["fields"]["imagemagick_version"] = Array({"label": __("ImageMagick version string"), "value": imagick_version["versionString"] if php_is_array(imagick_version) else imagick_version})
        #// If Imagick is used as our editor, provide some more information about its limitations.
        if "WP_Image_Editor_Imagick" == _wp_image_editor_choose() and (php_isset(lambda : imagick)) and type(imagick).__name__ == "Imagick":
            limits = Array({"area": size_format(imagick.getresourcelimit(imagick.RESOURCETYPE_AREA)) if php_defined("imagick::RESOURCETYPE_AREA") else not_available, "disk": imagick.getresourcelimit(imagick.RESOURCETYPE_DISK) if php_defined("imagick::RESOURCETYPE_DISK") else not_available, "file": imagick.getresourcelimit(imagick.RESOURCETYPE_FILE) if php_defined("imagick::RESOURCETYPE_FILE") else not_available, "map": size_format(imagick.getresourcelimit(imagick.RESOURCETYPE_MAP)) if php_defined("imagick::RESOURCETYPE_MAP") else not_available, "memory": size_format(imagick.getresourcelimit(imagick.RESOURCETYPE_MEMORY)) if php_defined("imagick::RESOURCETYPE_MEMORY") else not_available, "thread": imagick.getresourcelimit(imagick.RESOURCETYPE_THREAD) if php_defined("imagick::RESOURCETYPE_THREAD") else not_available})
            limits_debug = Array({"imagick::RESOURCETYPE_AREA": size_format(imagick.getresourcelimit(imagick.RESOURCETYPE_AREA)) if php_defined("imagick::RESOURCETYPE_AREA") else "not available", "imagick::RESOURCETYPE_DISK": imagick.getresourcelimit(imagick.RESOURCETYPE_DISK) if php_defined("imagick::RESOURCETYPE_DISK") else "not available", "imagick::RESOURCETYPE_FILE": imagick.getresourcelimit(imagick.RESOURCETYPE_FILE) if php_defined("imagick::RESOURCETYPE_FILE") else "not available", "imagick::RESOURCETYPE_MAP": size_format(imagick.getresourcelimit(imagick.RESOURCETYPE_MAP)) if php_defined("imagick::RESOURCETYPE_MAP") else "not available", "imagick::RESOURCETYPE_MEMORY": size_format(imagick.getresourcelimit(imagick.RESOURCETYPE_MEMORY)) if php_defined("imagick::RESOURCETYPE_MEMORY") else "not available", "imagick::RESOURCETYPE_THREAD": imagick.getresourcelimit(imagick.RESOURCETYPE_THREAD) if php_defined("imagick::RESOURCETYPE_THREAD") else "not available"})
            info["wp-media"]["fields"]["imagick_limits"] = Array({"label": __("Imagick Resource Limits"), "value": limits, "debug": limits_debug})
        # end if
        #// Get GD information, if available.
        if php_function_exists("gd_info"):
            gd = gd_info()
        else:
            gd = False
        # end if
        info["wp-media"]["fields"]["gd_version"] = Array({"label": __("GD version"), "value": gd["GD Version"] if php_is_array(gd) else not_available, "debug": gd["GD Version"] if php_is_array(gd) else "not available"})
        #// Get Ghostscript information, if available.
        if php_function_exists("exec"):
            gs = exec("gs --version")
            if php_empty(lambda : gs):
                gs = not_available
                gs_debug = "not available"
            else:
                gs_debug = gs
            # end if
        else:
            gs = __("Unable to determine if Ghostscript is installed")
            gs_debug = "unknown"
        # end if
        info["wp-media"]["fields"]["ghostscript_version"] = Array({"label": __("Ghostscript version"), "value": gs, "debug": gs_debug})
        #// Populate the server debug fields.
        if php_function_exists("php_uname"):
            server_architecture = php_sprintf("%s %s %s", php_uname("s"), php_uname("r"), php_uname("m"))
        else:
            server_architecture = "unknown"
        # end if
        if php_function_exists("phpversion"):
            php_version_debug = php_phpversion()
            #// Whether PHP supports 64-bit.
            php64bit = PHP_INT_SIZE * 8 == 64
            php_version = php_sprintf("%s %s", php_version_debug, __("(Supports 64bit values)") if php64bit else __("(Does not support 64bit values)"))
            if php64bit:
                php_version_debug += " 64bit"
            # end if
        else:
            php_version = __("Unable to determine PHP version")
            php_version_debug = "unknown"
        # end if
        if php_function_exists("php_sapi_name"):
            php_sapi = php_php_sapi_name()
        else:
            php_sapi = "unknown"
        # end if
        info["wp-server"]["fields"]["server_architecture"] = Array({"label": __("Server architecture"), "value": server_architecture if "unknown" != server_architecture else __("Unable to determine server architecture"), "debug": server_architecture})
        info["wp-server"]["fields"]["httpd_software"] = Array({"label": __("Web server"), "value": PHP_SERVER["SERVER_SOFTWARE"] if (php_isset(lambda : PHP_SERVER["SERVER_SOFTWARE"])) else __("Unable to determine what web server software is used"), "debug": PHP_SERVER["SERVER_SOFTWARE"] if (php_isset(lambda : PHP_SERVER["SERVER_SOFTWARE"])) else "unknown"})
        info["wp-server"]["fields"]["php_version"] = Array({"label": __("PHP version"), "value": php_version, "debug": php_version_debug})
        info["wp-server"]["fields"]["php_sapi"] = Array({"label": __("PHP SAPI"), "value": php_sapi if "unknown" != php_sapi else __("Unable to determine PHP SAPI"), "debug": php_sapi})
        #// Some servers disable `ini_set()` and `ini_get()`, we check this before trying to get configuration values.
        if (not php_function_exists("ini_get")):
            info["wp-server"]["fields"]["ini_get"] = Array({"label": __("Server settings"), "value": php_sprintf(__("Unable to determine some settings, as the %s function has been disabled."), "ini_get()"), "debug": "ini_get() is disabled"})
        else:
            info["wp-server"]["fields"]["max_input_variables"] = Array({"label": __("PHP max input variables"), "value": php_ini_get("max_input_vars")})
            info["wp-server"]["fields"]["time_limit"] = Array({"label": __("PHP time limit"), "value": php_ini_get("max_execution_time")})
            info["wp-server"]["fields"]["memory_limit"] = Array({"label": __("PHP memory limit"), "value": php_ini_get("memory_limit")})
            info["wp-server"]["fields"]["max_input_time"] = Array({"label": __("Max input time"), "value": php_ini_get("max_input_time")})
            info["wp-server"]["fields"]["upload_max_size"] = Array({"label": __("Upload max filesize"), "value": php_ini_get("upload_max_filesize")})
            info["wp-server"]["fields"]["php_post_max_size"] = Array({"label": __("PHP post max size"), "value": php_ini_get("post_max_size")})
        # end if
        if php_function_exists("curl_version"):
            curl = curl_version()
            info["wp-server"]["fields"]["curl_version"] = Array({"label": __("cURL version"), "value": php_sprintf("%s %s", curl["version"], curl["ssl_version"])})
        else:
            info["wp-server"]["fields"]["curl_version"] = Array({"label": __("cURL version"), "value": not_available, "debug": "not available"})
        # end if
        #// SUHOSIN.
        suhosin_loaded = php_extension_loaded("suhosin") or php_defined("SUHOSIN_PATCH") and constant("SUHOSIN_PATCH")
        info["wp-server"]["fields"]["suhosin"] = Array({"label": __("Is SUHOSIN installed?"), "value": __("Yes") if suhosin_loaded else __("No"), "debug": suhosin_loaded})
        #// Imagick.
        imagick_loaded = php_extension_loaded("imagick")
        info["wp-server"]["fields"]["imagick_availability"] = Array({"label": __("Is the Imagick library available?"), "value": __("Yes") if imagick_loaded else __("No"), "debug": imagick_loaded})
        #// Check if a .htaccess file exists.
        if php_is_file(ABSPATH + ".htaccess"):
            #// If the file exists, grab the content of it.
            htaccess_content = php_file_get_contents(ABSPATH + ".htaccess")
            #// Filter away the core WordPress rules.
            filtered_htaccess_content = php_trim(php_preg_replace("/\\# BEGIN WordPress[\\s\\S]+?# END WordPress/si", "", htaccess_content))
            filtered_htaccess_content = (not php_empty(lambda : filtered_htaccess_content))
            if filtered_htaccess_content:
                #// translators: %s: .htaccess
                htaccess_rules_string = php_sprintf(__("Custom rules have been added to your %s file."), ".htaccess")
            else:
                #// translators: %s: .htaccess
                htaccess_rules_string = php_sprintf(__("Your %s file contains only core WordPress features."), ".htaccess")
            # end if
            info["wp-server"]["fields"]["htaccess_extra_rules"] = Array({"label": __(".htaccess rules"), "value": htaccess_rules_string, "debug": filtered_htaccess_content})
        # end if
        #// Populate the database debug fields.
        if is_resource(wpdb.dbh):
            #// Old mysql extension.
            extension = "mysql"
        elif php_is_object(wpdb.dbh):
            #// mysqli or PDO.
            extension = get_class(wpdb.dbh)
        else:
            #// Unknown sql extension.
            extension = None
        # end if
        server = wpdb.get_var("SELECT VERSION()")
        if (php_isset(lambda : wpdb.use_mysqli)) and wpdb.use_mysqli:
            client_version = wpdb.dbh.client_info
        else:
            #// phpcs:ignore WordPress.DB.RestrictedFunctions.mysql_mysql_get_client_info,PHPCompatibility.Extensions.RemovedExtensions.mysql_DeprecatedRemoved
            if php_preg_match("|[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{1,2}|", mysql_get_client_info(), matches):
                client_version = matches[0]
            else:
                client_version = None
            # end if
        # end if
        info["wp-database"]["fields"]["extension"] = Array({"label": __("Extension"), "value": extension})
        info["wp-database"]["fields"]["server_version"] = Array({"label": __("Server version"), "value": server})
        info["wp-database"]["fields"]["client_version"] = Array({"label": __("Client version"), "value": client_version})
        info["wp-database"]["fields"]["database_user"] = Array({"label": __("Database username"), "value": wpdb.dbuser, "private": True})
        info["wp-database"]["fields"]["database_host"] = Array({"label": __("Database host"), "value": wpdb.dbhost, "private": True})
        info["wp-database"]["fields"]["database_name"] = Array({"label": __("Database name"), "value": wpdb.dbname, "private": True})
        info["wp-database"]["fields"]["database_prefix"] = Array({"label": __("Table prefix"), "value": wpdb.prefix, "private": True})
        info["wp-database"]["fields"]["database_charset"] = Array({"label": __("Database charset"), "value": wpdb.charset, "private": True})
        info["wp-database"]["fields"]["database_collate"] = Array({"label": __("Database collation"), "value": wpdb.collate, "private": True})
        #// List must use plugins if there are any.
        mu_plugins = get_mu_plugins()
        for plugin_path,plugin in mu_plugins:
            plugin_version = plugin["Version"]
            plugin_author = plugin["Author"]
            plugin_version_string = __("No version or author information is available.")
            plugin_version_string_debug = "author: (undefined), version: (undefined)"
            if (not php_empty(lambda : plugin_version)) and (not php_empty(lambda : plugin_author)):
                #// translators: 1: Plugin version number. 2: Plugin author name.
                plugin_version_string = php_sprintf(__("Version %1$s by %2$s"), plugin_version, plugin_author)
                plugin_version_string_debug = php_sprintf("version: %s, author: %s", plugin_version, plugin_author)
            else:
                if (not php_empty(lambda : plugin_author)):
                    #// translators: %s: Plugin author name.
                    plugin_version_string = php_sprintf(__("By %s"), plugin_author)
                    plugin_version_string_debug = php_sprintf("author: %s, version: (undefined)", plugin_author)
                # end if
                if (not php_empty(lambda : plugin_version)):
                    #// translators: %s: Plugin version number.
                    plugin_version_string = php_sprintf(__("Version %s"), plugin_version)
                    plugin_version_string_debug = php_sprintf("author: (undefined), version: %s", plugin_version)
                # end if
            # end if
            info["wp-mu-plugins"]["fields"][sanitize_text_field(plugin["Name"])] = Array({"label": plugin["Name"], "value": plugin_version_string, "debug": plugin_version_string_debug})
        # end for
        #// List all available plugins.
        plugins = get_plugins()
        plugin_updates = get_plugin_updates()
        for plugin_path,plugin in plugins:
            plugin_part = "wp-plugins-active" if is_plugin_active(plugin_path) else "wp-plugins-inactive"
            plugin_version = plugin["Version"]
            plugin_author = plugin["Author"]
            plugin_version_string = __("No version or author information is available.")
            plugin_version_string_debug = "author: (undefined), version: (undefined)"
            if (not php_empty(lambda : plugin_version)) and (not php_empty(lambda : plugin_author)):
                #// translators: 1: Plugin version number. 2: Plugin author name.
                plugin_version_string = php_sprintf(__("Version %1$s by %2$s"), plugin_version, plugin_author)
                plugin_version_string_debug = php_sprintf("version: %s, author: %s", plugin_version, plugin_author)
            else:
                if (not php_empty(lambda : plugin_author)):
                    #// translators: %s: Plugin author name.
                    plugin_version_string = php_sprintf(__("By %s"), plugin_author)
                    plugin_version_string_debug = php_sprintf("author: %s, version: (undefined)", plugin_author)
                # end if
                if (not php_empty(lambda : plugin_version)):
                    #// translators: %s: Plugin version number.
                    plugin_version_string = php_sprintf(__("Version %s"), plugin_version)
                    plugin_version_string_debug = php_sprintf("author: (undefined), version: %s", plugin_version)
                # end if
            # end if
            if php_array_key_exists(plugin_path, plugin_updates):
                #// translators: %s: Latest plugin version number.
                plugin_version_string += " " + php_sprintf(__("(Latest version: %s)"), plugin_updates[plugin_path].update.new_version)
                plugin_version_string_debug += php_sprintf(" (latest version: %s)", plugin_updates[plugin_path].update.new_version)
            # end if
            info[plugin_part]["fields"][sanitize_text_field(plugin["Name"])] = Array({"label": plugin["Name"], "value": plugin_version_string, "debug": plugin_version_string_debug})
        # end for
        #// Populate the section for the currently active theme.
        global _wp_theme_features
        php_check_if_defined("_wp_theme_features")
        theme_features = Array()
        if (not php_empty(lambda : _wp_theme_features)):
            for feature,options in _wp_theme_features:
                theme_features[-1] = feature
            # end for
        # end if
        active_theme = wp_get_theme()
        theme_updates = get_theme_updates()
        active_theme_version = active_theme.version
        active_theme_version_debug = active_theme_version
        if php_array_key_exists(active_theme.stylesheet, theme_updates):
            theme_update_new_version = theme_updates[active_theme.stylesheet].update["new_version"]
            #// translators: %s: Latest theme version number.
            active_theme_version += " " + php_sprintf(__("(Latest version: %s)"), theme_update_new_version)
            active_theme_version_debug += php_sprintf(" (latest version: %s)", theme_update_new_version)
        # end if
        active_theme_author_uri = active_theme.display("AuthorURI")
        if active_theme.parent_theme:
            active_theme_parent_theme = php_sprintf(__("%1$s (%2$s)"), active_theme.parent_theme, active_theme.template)
            active_theme_parent_theme_debug = php_sprintf("%s (%s)", active_theme.parent_theme, active_theme.template)
        else:
            active_theme_parent_theme = __("None")
            active_theme_parent_theme_debug = "none"
        # end if
        info["wp-active-theme"]["fields"] = Array({"name": Array({"label": __("Name"), "value": php_sprintf(__("%1$s (%2$s)"), active_theme.name, active_theme.stylesheet)})}, {"version": Array({"label": __("Version"), "value": active_theme_version, "debug": active_theme_version_debug})}, {"author": Array({"label": __("Author"), "value": wp_kses(active_theme.author, Array())})}, {"author_website": Array({"label": __("Author website"), "value": active_theme_author_uri if active_theme_author_uri else __("Undefined"), "debug": active_theme_author_uri if active_theme_author_uri else "(undefined)"})}, {"parent_theme": Array({"label": __("Parent theme"), "value": active_theme_parent_theme, "debug": active_theme_parent_theme_debug})}, {"theme_features": Array({"label": __("Theme features"), "value": php_implode(", ", theme_features)})}, {"theme_path": Array({"label": __("Theme directory location"), "value": get_stylesheet_directory()})})
        parent_theme = active_theme.parent()
        if parent_theme:
            parent_theme_version = parent_theme.version
            parent_theme_version_debug = parent_theme_version
            if php_array_key_exists(parent_theme.stylesheet, theme_updates):
                parent_theme_update_new_version = theme_updates[parent_theme.stylesheet].update["new_version"]
                #// translators: %s: Latest theme version number.
                parent_theme_version += " " + php_sprintf(__("(Latest version: %s)"), parent_theme_update_new_version)
                parent_theme_version_debug += php_sprintf(" (latest version: %s)", parent_theme_update_new_version)
            # end if
            parent_theme_author_uri = parent_theme.display("AuthorURI")
            info["wp-parent-theme"]["fields"] = Array({"name": Array({"label": __("Name"), "value": php_sprintf(__("%1$s (%2$s)"), parent_theme.name, parent_theme.stylesheet)})}, {"version": Array({"label": __("Version"), "value": parent_theme_version, "debug": parent_theme_version_debug})}, {"author": Array({"label": __("Author"), "value": wp_kses(parent_theme.author, Array())})}, {"author_website": Array({"label": __("Author website"), "value": parent_theme_author_uri if parent_theme_author_uri else __("Undefined"), "debug": parent_theme_author_uri if parent_theme_author_uri else "(undefined)"})}, {"theme_path": Array({"label": __("Theme directory location"), "value": get_template_directory()})})
        # end if
        #// Populate a list of all themes available in the install.
        all_themes = wp_get_themes()
        for theme_slug,theme in all_themes:
            #// Exclude the currently active theme from the list of all themes.
            if active_theme.stylesheet == theme_slug:
                continue
            # end if
            #// Exclude the currently active parent theme from the list of all themes.
            if (not php_empty(lambda : parent_theme)) and parent_theme.stylesheet == theme_slug:
                continue
            # end if
            theme_version = theme.version
            theme_author = theme.author
            #// Sanitize.
            theme_author = wp_kses(theme_author, Array())
            theme_version_string = __("No version or author information is available.")
            theme_version_string_debug = "undefined"
            if (not php_empty(lambda : theme_version)) and (not php_empty(lambda : theme_author)):
                #// translators: 1: Theme version number. 2: Theme author name.
                theme_version_string = php_sprintf(__("Version %1$s by %2$s"), theme_version, theme_author)
                theme_version_string_debug = php_sprintf("version: %s, author: %s", theme_version, theme_author)
            else:
                if (not php_empty(lambda : theme_author)):
                    #// translators: %s: Theme author name.
                    theme_version_string = php_sprintf(__("By %s"), theme_author)
                    theme_version_string_debug = php_sprintf("author: %s, version: (undefined)", theme_author)
                # end if
                if (not php_empty(lambda : theme_version)):
                    #// translators: %s: Theme version number.
                    theme_version_string = php_sprintf(__("Version %s"), theme_version)
                    theme_version_string_debug = php_sprintf("author: (undefined), version: %s", theme_version)
                # end if
            # end if
            if php_array_key_exists(theme_slug, theme_updates):
                #// translators: %s: Latest theme version number.
                theme_version_string += " " + php_sprintf(__("(Latest version: %s)"), theme_updates[theme_slug].update["new_version"])
                theme_version_string_debug += php_sprintf(" (latest version: %s)", theme_updates[theme_slug].update["new_version"])
            # end if
            info["wp-themes-inactive"]["fields"][sanitize_text_field(theme.name)] = Array({"label": php_sprintf(__("%1$s (%2$s)"), theme.name, theme_slug), "value": theme_version_string, "debug": theme_version_string_debug})
        # end for
        #// Add more filesystem checks.
        if php_defined("WPMU_PLUGIN_DIR") and php_is_dir(WPMU_PLUGIN_DIR):
            is_writable_wpmu_plugin_dir = wp_is_writable(WPMU_PLUGIN_DIR)
            info["wp-filesystem"]["fields"]["mu-plugins"] = Array({"label": __("The must use plugins directory"), "value": __("Writable") if is_writable_wpmu_plugin_dir else __("Not writable"), "debug": "writable" if is_writable_wpmu_plugin_dir else "not writable"})
        # end if
        #// 
        #// Add or modify the debug information.
        #// 
        #// Plugin or themes may wish to introduce their own debug information without creating additional admin pages
        #// they can utilize this filter to introduce their own sections or add more data to existing sections.
        #// 
        #// Array keys for sections added by core are all prefixed with `wp-`, plugins and themes should use their own slug as
        #// a prefix, both for consistency as well as avoiding key collisions. Note that the array keys are used as labels
        #// for the copied data.
        #// 
        #// All strings are expected to be plain text except $description that can contain inline HTML tags (see below).
        #// 
        #// @since 5.2.0
        #// 
        #// @param array $args {
        #// The debug information to be added to the core information page.
        #// 
        #// This is an associative multi-dimensional array, up to three levels deep. The topmost array holds the sections.
        #// Each section has a `$fields` associative array (see below), and each `$value` in `$fields` can be
        #// another associative array of name/value pairs when there is more structured data to display.
        #// 
        #// @type string  $label        The title for this section of the debug output.
        #// @type string  $description  Optional. A description for your information section which may contain basic HTML
        #// markup, inline tags only as it is outputted in a paragraph.
        #// @type boolean $show_count   Optional. If set to `true` the amount of fields will be included in the title for
        #// this section.
        #// @type boolean $private      Optional. If set to `true` the section and all associated fields will be excluded
        #// from the copied data.
        #// @type array   $fields {
        #// An associative array containing the data to be displayed.
        #// 
        #// @type string  $label    The label for this piece of information.
        #// @type string  $value    The output that is displayed for this field. Text should be translated. Can be
        #// an associative array that is displayed as name/value pairs.
        #// @type string  $debug    Optional. The output that is used for this field when the user copies the data.
        #// It should be more concise and not translated. If not set, the content of `$value` is used.
        #// Note that the array keys are used as labels for the copied data.
        #// @type boolean $private  Optional. If set to `true` the field will not be included in the copied data
        #// allowing you to show, for example, API keys here.
        #// }
        #// }
        #//
        info = apply_filters("debug_information", info)
        return info
    # end def debug_data
    #// 
    #// Format the information gathered for debugging, in a manner suitable for copying to a forum or support ticket.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $info_array Information gathered from the `WP_Debug_Data::debug_data` function.
    #// @param string $type      The data type to return, either 'info' or 'debug'.
    #// @return string The formatted data.
    #//
    @classmethod
    def format(self, info_array=None, type=None):
        
        return_ = "`\n"
        for section,details in info_array:
            #// Skip this section if there are no fields, or the section has been declared as private.
            if php_empty(lambda : details["fields"]) or (php_isset(lambda : details["private"])) and details["private"]:
                continue
            # end if
            section_label = section if "debug" == type else details["label"]
            return_ += php_sprintf("### %s%s ###\n\n", section_label, php_sprintf(" (%d)", php_count(details["fields"])) if (php_isset(lambda : details["show_count"])) and details["show_count"] else "")
            for field_name,field in details["fields"]:
                if (php_isset(lambda : field["private"])) and True == field["private"]:
                    continue
                # end if
                if "debug" == type and (php_isset(lambda : field["debug"])):
                    debug_data = field["debug"]
                else:
                    debug_data = field["value"]
                # end if
                #// Can be array, one level deep only.
                if php_is_array(debug_data):
                    value = ""
                    for sub_field_name,sub_field_value in debug_data:
                        value += php_sprintf("\n    %s: %s", sub_field_name, sub_field_value)
                    # end for
                elif php_is_bool(debug_data):
                    value = "true" if debug_data else "false"
                elif php_empty(lambda : debug_data) and "0" != debug_data:
                    value = "undefined"
                else:
                    value = debug_data
                # end if
                if "debug" == type:
                    label = field_name
                else:
                    label = field["label"]
                # end if
                return_ += php_sprintf("%s: %s\n", label, value)
            # end for
            return_ += "\n"
        # end for
        return_ += "`"
        return return_
    # end def format
    #// 
    #// Fetch the total size of all the database tables for the active database user.
    #// 
    #// @since 5.2.0
    #// 
    #// @return int The size of the database, in bytes.
    #//
    @classmethod
    def get_database_size(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        size = 0
        rows = wpdb.get_results("SHOW TABLE STATUS", ARRAY_A)
        if wpdb.num_rows > 0:
            for row in rows:
                size += row["Data_length"] + row["Index_length"]
            # end for
        # end if
        return int(size)
    # end def get_database_size
    #// 
    #// Fetch the sizes of the WordPress directories: `wordpress` (ABSPATH), `plugins`, `themes`, and `uploads`.
    #// Intended to supplement the array returned by `WP_Debug_Data::debug_data()`.
    #// 
    #// @since 5.2.0
    #// 
    #// @return array The sizes of the directories, also the database size and total installation size.
    #//
    @classmethod
    def get_sizes(self):
        
        size_db = self.get_database_size()
        upload_dir = wp_get_upload_dir()
        #// 
        #// We will be using the PHP max execution time to prevent the size calculations
        #// from causing a timeout. The default value is 30 seconds, and some
        #// hosts do not allow you to read configuration values.
        #//
        if php_function_exists("ini_get"):
            max_execution_time = php_ini_get("max_execution_time")
        # end if
        #// The max_execution_time defaults to 0 when PHP runs from cli.
        #// We still want to limit it below.
        if php_empty(lambda : max_execution_time):
            max_execution_time = 30
        # end if
        if max_execution_time > 20:
            #// If the max_execution_time is set to lower than 20 seconds, reduce it a bit to prevent
            #// edge-case timeouts that may happen after the size loop has finished running.
            max_execution_time -= 2
        # end if
        #// Go through the various installation directories and calculate their sizes.
        #// No trailing slashes.
        paths = Array({"wordpress_size": untrailingslashit(ABSPATH), "themes_size": get_theme_root(), "plugins_size": WP_PLUGIN_DIR, "uploads_size": upload_dir["basedir"]})
        exclude = paths
        exclude["wordpress_size"] = None
        exclude = php_array_values(exclude)
        size_total = 0
        all_sizes = Array()
        #// Loop over all the directories we want to gather the sizes for.
        for name,path in paths:
            dir_size = None
            #// Default to timeout.
            results = Array({"path": path, "raw": 0})
            if php_microtime(True) - WP_START_TIMESTAMP < max_execution_time:
                if "wordpress_size" == name:
                    dir_size = recurse_dirsize(path, exclude, max_execution_time)
                else:
                    dir_size = recurse_dirsize(path, None, max_execution_time)
                # end if
            # end if
            if False == dir_size:
                #// Error reading.
                results["size"] = __("The size cannot be calculated. The directory is not accessible. Usually caused by invalid permissions.")
                results["debug"] = "not accessible"
                #// Stop total size calculation.
                size_total = None
            elif None == dir_size:
                #// Timeout.
                results["size"] = __("The directory size calculation has timed out. Usually caused by a very large number of sub-directories and files.")
                results["debug"] = "timeout while calculating size"
                #// Stop total size calculation.
                size_total = None
            else:
                if None != size_total:
                    size_total += dir_size
                # end if
                results["raw"] = dir_size
                results["size"] = size_format(dir_size, 2)
                results["debug"] = results["size"] + str(" (") + str(dir_size) + str(" bytes)")
            # end if
            all_sizes[name] = results
        # end for
        if size_db > 0:
            database_size = size_format(size_db, 2)
            all_sizes["database_size"] = Array({"raw": size_db, "size": database_size, "debug": database_size + str(" (") + str(size_db) + str(" bytes)")})
        else:
            all_sizes["database_size"] = Array({"size": __("Not available"), "debug": "not available"})
        # end if
        if None != size_total and size_db > 0:
            total_size = size_total + size_db
            total_size_mb = size_format(total_size, 2)
            all_sizes["total_size"] = Array({"raw": total_size, "size": total_size_mb, "debug": total_size_mb + str(" (") + str(total_size) + str(" bytes)")})
        else:
            all_sizes["total_size"] = Array({"size": __("Total size is not available. Some errors were encountered when determining the size of your installation."), "debug": "not available"})
        # end if
        return all_sizes
    # end def get_sizes
# end class WP_Debug_Data
