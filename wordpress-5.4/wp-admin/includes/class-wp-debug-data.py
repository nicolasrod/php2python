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
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// Save few function calls.
        upload_dir_ = wp_upload_dir()
        permalink_structure_ = get_option("permalink_structure")
        is_ssl_ = is_ssl()
        users_can_register_ = get_option("users_can_register")
        default_comment_status_ = get_option("default_comment_status")
        is_multisite_ = is_multisite()
        core_version_ = get_bloginfo("version")
        core_updates_ = get_core_updates()
        core_update_needed_ = ""
        for core_,update_ in core_updates_:
            if "upgrade" == update_.response:
                #// translators: %s: Latest WordPress version number.
                core_update_needed_ = " " + php_sprintf(__("(Latest version: %s)"), update_.version)
            else:
                core_update_needed_ = ""
            # end if
        # end for
        #// Set up the array that holds all debug information.
        info_ = Array()
        info_["wp-core"] = Array({"label": __("WordPress"), "fields": Array({"version": Array({"label": __("Version"), "value": core_version_ + core_update_needed_, "debug": core_version_})}, {"site_language": Array({"label": __("Site Language"), "value": get_locale()})}, {"user_language": Array({"label": __("User Language"), "value": get_user_locale()})}, {"timezone": Array({"label": __("Timezone"), "value": wp_timezone_string()})}, {"home_url": Array({"label": __("Home URL"), "value": get_bloginfo("url"), "private": True})}, {"site_url": Array({"label": __("Site URL"), "value": get_bloginfo("wpurl"), "private": True})}, {"permalink": Array({"label": __("Permalink structure"), "value": permalink_structure_ if permalink_structure_ else __("No permalink structure set"), "debug": permalink_structure_})}, {"https_status": Array({"label": __("Is this site using HTTPS?"), "value": __("Yes") if is_ssl_ else __("No"), "debug": is_ssl_})}, {"user_registration": Array({"label": __("Can anyone register on this site?"), "value": __("Yes") if users_can_register_ else __("No"), "debug": users_can_register_})}, {"default_comment_status": Array({"label": __("Default comment status"), "value": _x("Open", "comment status") if "open" == default_comment_status_ else _x("Closed", "comment status"), "debug": default_comment_status_})}, {"multisite": Array({"label": __("Is this a multisite?"), "value": __("Yes") if is_multisite_ else __("No"), "debug": is_multisite_})})})
        if (not is_multisite_):
            info_["wp-paths-sizes"] = Array({"label": __("Directories and Sizes"), "fields": Array()})
        # end if
        info_["wp-dropins"] = Array({"label": __("Drop-ins"), "show_count": True, "description": php_sprintf(__("Drop-ins are single files, found in the %s directory, that replace or enhance WordPress features in ways that are not possible for traditional plugins."), "<code>" + php_str_replace(ABSPATH, "", WP_CONTENT_DIR) + "</code>"), "fields": Array()})
        info_["wp-active-theme"] = Array({"label": __("Active Theme"), "fields": Array()})
        info_["wp-parent-theme"] = Array({"label": __("Parent Theme"), "fields": Array()})
        info_["wp-themes-inactive"] = Array({"label": __("Inactive Themes"), "show_count": True, "fields": Array()})
        info_["wp-mu-plugins"] = Array({"label": __("Must Use Plugins"), "show_count": True, "fields": Array()})
        info_["wp-plugins-active"] = Array({"label": __("Active Plugins"), "show_count": True, "fields": Array()})
        info_["wp-plugins-inactive"] = Array({"label": __("Inactive Plugins"), "show_count": True, "fields": Array()})
        info_["wp-media"] = Array({"label": __("Media Handling"), "fields": Array()})
        info_["wp-server"] = Array({"label": __("Server"), "description": __("The options shown below relate to your server setup. If changes are required, you may need your web host&#8217;s assistance."), "fields": Array()})
        info_["wp-database"] = Array({"label": __("Database"), "fields": Array()})
        #// Check if WP_DEBUG_LOG is set.
        wp_debug_log_value_ = __("Disabled")
        if php_is_string(WP_DEBUG_LOG):
            wp_debug_log_value_ = WP_DEBUG_LOG
        elif WP_DEBUG_LOG:
            wp_debug_log_value_ = __("Enabled")
        # end if
        #// Check CONCATENATE_SCRIPTS.
        if php_defined("CONCATENATE_SCRIPTS"):
            concatenate_scripts_ = __("Enabled") if CONCATENATE_SCRIPTS else __("Disabled")
            concatenate_scripts_debug_ = "true" if CONCATENATE_SCRIPTS else "false"
        else:
            concatenate_scripts_ = __("Undefined")
            concatenate_scripts_debug_ = "undefined"
        # end if
        #// Check COMPRESS_SCRIPTS.
        if php_defined("COMPRESS_SCRIPTS"):
            compress_scripts_ = __("Enabled") if COMPRESS_SCRIPTS else __("Disabled")
            compress_scripts_debug_ = "true" if COMPRESS_SCRIPTS else "false"
        else:
            compress_scripts_ = __("Undefined")
            compress_scripts_debug_ = "undefined"
        # end if
        #// Check COMPRESS_CSS.
        if php_defined("COMPRESS_CSS"):
            compress_css_ = __("Enabled") if COMPRESS_CSS else __("Disabled")
            compress_css_debug_ = "true" if COMPRESS_CSS else "false"
        else:
            compress_css_ = __("Undefined")
            compress_css_debug_ = "undefined"
        # end if
        #// Check WP_LOCAL_DEV.
        if php_defined("WP_LOCAL_DEV"):
            wp_local_dev_ = __("Enabled") if WP_LOCAL_DEV else __("Disabled")
            wp_local_dev_debug_ = "true" if WP_LOCAL_DEV else "false"
        else:
            wp_local_dev_ = __("Undefined")
            wp_local_dev_debug_ = "undefined"
        # end if
        info_["wp-constants"] = Array({"label": __("WordPress Constants"), "description": __("These settings alter where and how parts of WordPress are loaded."), "fields": Array({"ABSPATH": Array({"label": "ABSPATH", "value": ABSPATH, "private": True})}, {"WP_HOME": Array({"label": "WP_HOME", "value": WP_HOME if php_defined("WP_HOME") else __("Undefined"), "debug": WP_HOME if php_defined("WP_HOME") else "undefined"})}, {"WP_SITEURL": Array({"label": "WP_SITEURL", "value": WP_SITEURL if php_defined("WP_SITEURL") else __("Undefined"), "debug": WP_SITEURL if php_defined("WP_SITEURL") else "undefined"})}, {"WP_CONTENT_DIR": Array({"label": "WP_CONTENT_DIR", "value": WP_CONTENT_DIR})}, {"WP_PLUGIN_DIR": Array({"label": "WP_PLUGIN_DIR", "value": WP_PLUGIN_DIR})}, {"WP_MAX_MEMORY_LIMIT": Array({"label": "WP_MAX_MEMORY_LIMIT", "value": WP_MAX_MEMORY_LIMIT})}, {"WP_DEBUG": Array({"label": "WP_DEBUG", "value": __("Enabled") if WP_DEBUG else __("Disabled"), "debug": WP_DEBUG})}, {"WP_DEBUG_DISPLAY": Array({"label": "WP_DEBUG_DISPLAY", "value": __("Enabled") if WP_DEBUG_DISPLAY else __("Disabled"), "debug": WP_DEBUG_DISPLAY})}, {"WP_DEBUG_LOG": Array({"label": "WP_DEBUG_LOG", "value": wp_debug_log_value_, "debug": WP_DEBUG_LOG})}, {"SCRIPT_DEBUG": Array({"label": "SCRIPT_DEBUG", "value": __("Enabled") if SCRIPT_DEBUG else __("Disabled"), "debug": SCRIPT_DEBUG})}, {"WP_CACHE": Array({"label": "WP_CACHE", "value": __("Enabled") if WP_CACHE else __("Disabled"), "debug": WP_CACHE})}, {"CONCATENATE_SCRIPTS": Array({"label": "CONCATENATE_SCRIPTS", "value": concatenate_scripts_, "debug": concatenate_scripts_debug_})}, {"COMPRESS_SCRIPTS": Array({"label": "COMPRESS_SCRIPTS", "value": compress_scripts_, "debug": compress_scripts_debug_})}, {"COMPRESS_CSS": Array({"label": "COMPRESS_CSS", "value": compress_css_, "debug": compress_css_debug_})}, {"WP_LOCAL_DEV": Array({"label": "WP_LOCAL_DEV", "value": wp_local_dev_, "debug": wp_local_dev_debug_})}, {"DB_CHARSET": Array({"label": "DB_CHARSET", "value": DB_CHARSET if php_defined("DB_CHARSET") else __("Undefined"), "debug": DB_CHARSET if php_defined("DB_CHARSET") else "undefined"})}, {"DB_COLLATE": Array({"label": "DB_COLLATE", "value": DB_COLLATE if php_defined("DB_COLLATE") else __("Undefined"), "debug": DB_COLLATE if php_defined("DB_COLLATE") else "undefined"})})})
        is_writable_abspath_ = wp_is_writable(ABSPATH)
        is_writable_wp_content_dir_ = wp_is_writable(WP_CONTENT_DIR)
        is_writable_upload_dir_ = wp_is_writable(upload_dir_["basedir"])
        is_writable_wp_plugin_dir_ = wp_is_writable(WP_PLUGIN_DIR)
        is_writable_template_directory_ = wp_is_writable(get_template_directory() + "/..")
        info_["wp-filesystem"] = Array({"label": __("Filesystem Permissions"), "description": __("Shows whether WordPress is able to write to the directories it needs access to."), "fields": Array({"wordpress": Array({"label": __("The main WordPress directory"), "value": __("Writable") if is_writable_abspath_ else __("Not writable"), "debug": "writable" if is_writable_abspath_ else "not writable"})}, {"wp-content": Array({"label": __("The wp-content directory"), "value": __("Writable") if is_writable_wp_content_dir_ else __("Not writable"), "debug": "writable" if is_writable_wp_content_dir_ else "not writable"})}, {"uploads": Array({"label": __("The uploads directory"), "value": __("Writable") if is_writable_upload_dir_ else __("Not writable"), "debug": "writable" if is_writable_upload_dir_ else "not writable"})}, {"plugins": Array({"label": __("The plugins directory"), "value": __("Writable") if is_writable_wp_plugin_dir_ else __("Not writable"), "debug": "writable" if is_writable_wp_plugin_dir_ else "not writable"})}, {"themes": Array({"label": __("The themes directory"), "value": __("Writable") if is_writable_template_directory_ else __("Not writable"), "debug": "writable" if is_writable_template_directory_ else "not writable"})})})
        #// Conditionally add debug information for multisite setups.
        if is_multisite():
            network_query_ = php_new_class("WP_Network_Query", lambda : WP_Network_Query())
            network_ids_ = network_query_.query(Array({"fields": "ids", "number": 100, "no_found_rows": False}))
            site_count_ = 0
            for network_id_ in network_ids_:
                site_count_ += get_blog_count(network_id_)
            # end for
            info_["wp-core"]["fields"]["user_count"] = Array({"label": __("User count"), "value": get_user_count()})
            info_["wp-core"]["fields"]["site_count"] = Array({"label": __("Site count"), "value": site_count_})
            info_["wp-core"]["fields"]["network_count"] = Array({"label": __("Network count"), "value": network_query_.found_networks})
        else:
            user_count_ = count_users()
            info_["wp-core"]["fields"]["user_count"] = Array({"label": __("User count"), "value": user_count_["total_users"]})
        # end if
        #// WordPress features requiring processing.
        wp_dotorg_ = wp_remote_get("https://wordpress.org", Array({"timeout": 10}))
        if (not is_wp_error(wp_dotorg_)):
            info_["wp-core"]["fields"]["dotorg_communication"] = Array({"label": __("Communication with WordPress.org"), "value": __("WordPress.org is reachable"), "debug": "true"})
        else:
            info_["wp-core"]["fields"]["dotorg_communication"] = Array({"label": __("Communication with WordPress.org"), "value": php_sprintf(__("Unable to reach WordPress.org at %1$s: %2$s"), gethostbyname("wordpress.org"), wp_dotorg_.get_error_message()), "debug": wp_dotorg_.get_error_message()})
        # end if
        #// Remove accordion for Directories and Sizes if in Multisite.
        if (not is_multisite_):
            loading_ = __("Loading&hellip;")
            info_["wp-paths-sizes"]["fields"] = Array({"wordpress_path": Array({"label": __("WordPress directory location"), "value": untrailingslashit(ABSPATH)})}, {"wordpress_size": Array({"label": __("WordPress directory size"), "value": loading_, "debug": "loading..."})}, {"uploads_path": Array({"label": __("Uploads directory location"), "value": upload_dir_["basedir"]})}, {"uploads_size": Array({"label": __("Uploads directory size"), "value": loading_, "debug": "loading..."})}, {"themes_path": Array({"label": __("Themes directory location"), "value": get_theme_root()})}, {"themes_size": Array({"label": __("Themes directory size"), "value": loading_, "debug": "loading..."})}, {"plugins_path": Array({"label": __("Plugins directory location"), "value": WP_PLUGIN_DIR})}, {"plugins_size": Array({"label": __("Plugins directory size"), "value": loading_, "debug": "loading..."})}, {"database_size": Array({"label": __("Database size"), "value": loading_, "debug": "loading..."})}, {"total_size": Array({"label": __("Total installation size"), "value": loading_, "debug": "loading..."})})
        # end if
        #// Get a list of all drop-in replacements.
        dropins_ = get_dropins()
        #// Get dropins descriptions.
        dropin_descriptions_ = _get_dropins()
        #// Spare few function calls.
        not_available_ = __("Not available")
        for dropin_key_,dropin_ in dropins_:
            info_["wp-dropins"]["fields"][sanitize_text_field(dropin_key_)] = Array({"label": dropin_key_, "value": dropin_descriptions_[dropin_key_][0], "debug": "true"})
        # end for
        #// Populate the media fields.
        info_["wp-media"]["fields"]["image_editor"] = Array({"label": __("Active editor"), "value": _wp_image_editor_choose()})
        #// Get ImageMagic information, if available.
        if php_class_exists("Imagick"):
            #// Save the Imagick instance for later use.
            imagick_ = php_new_class("Imagick", lambda : Imagick())
            imagick_version_ = imagick_.getversion()
        else:
            imagick_version_ = __("Not available")
        # end if
        info_["wp-media"]["fields"]["imagick_module_version"] = Array({"label": __("ImageMagick version number"), "value": imagick_version_["versionNumber"] if php_is_array(imagick_version_) else imagick_version_})
        info_["wp-media"]["fields"]["imagemagick_version"] = Array({"label": __("ImageMagick version string"), "value": imagick_version_["versionString"] if php_is_array(imagick_version_) else imagick_version_})
        #// If Imagick is used as our editor, provide some more information about its limitations.
        if "WP_Image_Editor_Imagick" == _wp_image_editor_choose() and (php_isset(lambda : imagick_)) and type(imagick_).__name__ == "Imagick":
            limits_ = Array({"area": size_format(imagick_.getresourcelimit(imagick.RESOURCETYPE_AREA)) if php_defined("imagick::RESOURCETYPE_AREA") else not_available_, "disk": imagick_.getresourcelimit(imagick.RESOURCETYPE_DISK) if php_defined("imagick::RESOURCETYPE_DISK") else not_available_, "file": imagick_.getresourcelimit(imagick.RESOURCETYPE_FILE) if php_defined("imagick::RESOURCETYPE_FILE") else not_available_, "map": size_format(imagick_.getresourcelimit(imagick.RESOURCETYPE_MAP)) if php_defined("imagick::RESOURCETYPE_MAP") else not_available_, "memory": size_format(imagick_.getresourcelimit(imagick.RESOURCETYPE_MEMORY)) if php_defined("imagick::RESOURCETYPE_MEMORY") else not_available_, "thread": imagick_.getresourcelimit(imagick.RESOURCETYPE_THREAD) if php_defined("imagick::RESOURCETYPE_THREAD") else not_available_})
            limits_debug_ = Array({"imagick::RESOURCETYPE_AREA": size_format(imagick_.getresourcelimit(imagick.RESOURCETYPE_AREA)) if php_defined("imagick::RESOURCETYPE_AREA") else "not available", "imagick::RESOURCETYPE_DISK": imagick_.getresourcelimit(imagick.RESOURCETYPE_DISK) if php_defined("imagick::RESOURCETYPE_DISK") else "not available", "imagick::RESOURCETYPE_FILE": imagick_.getresourcelimit(imagick.RESOURCETYPE_FILE) if php_defined("imagick::RESOURCETYPE_FILE") else "not available", "imagick::RESOURCETYPE_MAP": size_format(imagick_.getresourcelimit(imagick.RESOURCETYPE_MAP)) if php_defined("imagick::RESOURCETYPE_MAP") else "not available", "imagick::RESOURCETYPE_MEMORY": size_format(imagick_.getresourcelimit(imagick.RESOURCETYPE_MEMORY)) if php_defined("imagick::RESOURCETYPE_MEMORY") else "not available", "imagick::RESOURCETYPE_THREAD": imagick_.getresourcelimit(imagick.RESOURCETYPE_THREAD) if php_defined("imagick::RESOURCETYPE_THREAD") else "not available"})
            info_["wp-media"]["fields"]["imagick_limits"] = Array({"label": __("Imagick Resource Limits"), "value": limits_, "debug": limits_debug_})
        # end if
        #// Get GD information, if available.
        if php_function_exists("gd_info"):
            gd_ = gd_info()
        else:
            gd_ = False
        # end if
        info_["wp-media"]["fields"]["gd_version"] = Array({"label": __("GD version"), "value": gd_["GD Version"] if php_is_array(gd_) else not_available_, "debug": gd_["GD Version"] if php_is_array(gd_) else "not available"})
        #// Get Ghostscript information, if available.
        if php_function_exists("exec"):
            gs_ = exec("gs --version")
            if php_empty(lambda : gs_):
                gs_ = not_available_
                gs_debug_ = "not available"
            else:
                gs_debug_ = gs_
            # end if
        else:
            gs_ = __("Unable to determine if Ghostscript is installed")
            gs_debug_ = "unknown"
        # end if
        info_["wp-media"]["fields"]["ghostscript_version"] = Array({"label": __("Ghostscript version"), "value": gs_, "debug": gs_debug_})
        #// Populate the server debug fields.
        if php_function_exists("php_uname"):
            server_architecture_ = php_sprintf("%s %s %s", php_uname("s"), php_uname("r"), php_uname("m"))
        else:
            server_architecture_ = "unknown"
        # end if
        if php_function_exists("phpversion"):
            php_version_debug_ = php_phpversion()
            #// Whether PHP supports 64-bit.
            php64bit_ = PHP_INT_SIZE * 8 == 64
            php_version_ = php_sprintf("%s %s", php_version_debug_, __("(Supports 64bit values)") if php64bit_ else __("(Does not support 64bit values)"))
            if php64bit_:
                php_version_debug_ += " 64bit"
            # end if
        else:
            php_version_ = __("Unable to determine PHP version")
            php_version_debug_ = "unknown"
        # end if
        if php_function_exists("php_sapi_name"):
            php_sapi_ = php_php_sapi_name()
        else:
            php_sapi_ = "unknown"
        # end if
        info_["wp-server"]["fields"]["server_architecture"] = Array({"label": __("Server architecture"), "value": server_architecture_ if "unknown" != server_architecture_ else __("Unable to determine server architecture"), "debug": server_architecture_})
        info_["wp-server"]["fields"]["httpd_software"] = Array({"label": __("Web server"), "value": PHP_SERVER["SERVER_SOFTWARE"] if (php_isset(lambda : PHP_SERVER["SERVER_SOFTWARE"])) else __("Unable to determine what web server software is used"), "debug": PHP_SERVER["SERVER_SOFTWARE"] if (php_isset(lambda : PHP_SERVER["SERVER_SOFTWARE"])) else "unknown"})
        info_["wp-server"]["fields"]["php_version"] = Array({"label": __("PHP version"), "value": php_version_, "debug": php_version_debug_})
        info_["wp-server"]["fields"]["php_sapi"] = Array({"label": __("PHP SAPI"), "value": php_sapi_ if "unknown" != php_sapi_ else __("Unable to determine PHP SAPI"), "debug": php_sapi_})
        #// Some servers disable `ini_set()` and `ini_get()`, we check this before trying to get configuration values.
        if (not php_function_exists("ini_get")):
            info_["wp-server"]["fields"]["ini_get"] = Array({"label": __("Server settings"), "value": php_sprintf(__("Unable to determine some settings, as the %s function has been disabled."), "ini_get()"), "debug": "ini_get() is disabled"})
        else:
            info_["wp-server"]["fields"]["max_input_variables"] = Array({"label": __("PHP max input variables"), "value": php_ini_get("max_input_vars")})
            info_["wp-server"]["fields"]["time_limit"] = Array({"label": __("PHP time limit"), "value": php_ini_get("max_execution_time")})
            info_["wp-server"]["fields"]["memory_limit"] = Array({"label": __("PHP memory limit"), "value": php_ini_get("memory_limit")})
            info_["wp-server"]["fields"]["max_input_time"] = Array({"label": __("Max input time"), "value": php_ini_get("max_input_time")})
            info_["wp-server"]["fields"]["upload_max_size"] = Array({"label": __("Upload max filesize"), "value": php_ini_get("upload_max_filesize")})
            info_["wp-server"]["fields"]["php_post_max_size"] = Array({"label": __("PHP post max size"), "value": php_ini_get("post_max_size")})
        # end if
        if php_function_exists("curl_version"):
            curl_ = curl_version()
            info_["wp-server"]["fields"]["curl_version"] = Array({"label": __("cURL version"), "value": php_sprintf("%s %s", curl_["version"], curl_["ssl_version"])})
        else:
            info_["wp-server"]["fields"]["curl_version"] = Array({"label": __("cURL version"), "value": not_available_, "debug": "not available"})
        # end if
        #// SUHOSIN.
        suhosin_loaded_ = php_extension_loaded("suhosin") or php_defined("SUHOSIN_PATCH") and constant("SUHOSIN_PATCH")
        info_["wp-server"]["fields"]["suhosin"] = Array({"label": __("Is SUHOSIN installed?"), "value": __("Yes") if suhosin_loaded_ else __("No"), "debug": suhosin_loaded_})
        #// Imagick.
        imagick_loaded_ = php_extension_loaded("imagick")
        info_["wp-server"]["fields"]["imagick_availability"] = Array({"label": __("Is the Imagick library available?"), "value": __("Yes") if imagick_loaded_ else __("No"), "debug": imagick_loaded_})
        #// Check if a .htaccess file exists.
        if php_is_file(ABSPATH + ".htaccess"):
            #// If the file exists, grab the content of it.
            htaccess_content_ = php_file_get_contents(ABSPATH + ".htaccess")
            #// Filter away the core WordPress rules.
            filtered_htaccess_content_ = php_trim(php_preg_replace("/\\# BEGIN WordPress[\\s\\S]+?# END WordPress/si", "", htaccess_content_))
            filtered_htaccess_content_ = (not php_empty(lambda : filtered_htaccess_content_))
            if filtered_htaccess_content_:
                #// translators: %s: .htaccess
                htaccess_rules_string_ = php_sprintf(__("Custom rules have been added to your %s file."), ".htaccess")
            else:
                #// translators: %s: .htaccess
                htaccess_rules_string_ = php_sprintf(__("Your %s file contains only core WordPress features."), ".htaccess")
            # end if
            info_["wp-server"]["fields"]["htaccess_extra_rules"] = Array({"label": __(".htaccess rules"), "value": htaccess_rules_string_, "debug": filtered_htaccess_content_})
        # end if
        #// Populate the database debug fields.
        if is_resource(wpdb_.dbh):
            #// Old mysql extension.
            extension_ = "mysql"
        elif php_is_object(wpdb_.dbh):
            #// mysqli or PDO.
            extension_ = get_class(wpdb_.dbh)
        else:
            #// Unknown sql extension.
            extension_ = None
        # end if
        server_ = wpdb_.get_var("SELECT VERSION()")
        if (php_isset(lambda : wpdb_.use_mysqli)) and wpdb_.use_mysqli:
            client_version_ = wpdb_.dbh.client_info
        else:
            #// phpcs:ignore WordPress.DB.RestrictedFunctions.mysql_mysql_get_client_info,PHPCompatibility.Extensions.RemovedExtensions.mysql_DeprecatedRemoved
            if php_preg_match("|[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{1,2}|", mysql_get_client_info(), matches_):
                client_version_ = matches_[0]
            else:
                client_version_ = None
            # end if
        # end if
        info_["wp-database"]["fields"]["extension"] = Array({"label": __("Extension"), "value": extension_})
        info_["wp-database"]["fields"]["server_version"] = Array({"label": __("Server version"), "value": server_})
        info_["wp-database"]["fields"]["client_version"] = Array({"label": __("Client version"), "value": client_version_})
        info_["wp-database"]["fields"]["database_user"] = Array({"label": __("Database username"), "value": wpdb_.dbuser, "private": True})
        info_["wp-database"]["fields"]["database_host"] = Array({"label": __("Database host"), "value": wpdb_.dbhost, "private": True})
        info_["wp-database"]["fields"]["database_name"] = Array({"label": __("Database name"), "value": wpdb_.dbname, "private": True})
        info_["wp-database"]["fields"]["database_prefix"] = Array({"label": __("Table prefix"), "value": wpdb_.prefix, "private": True})
        info_["wp-database"]["fields"]["database_charset"] = Array({"label": __("Database charset"), "value": wpdb_.charset, "private": True})
        info_["wp-database"]["fields"]["database_collate"] = Array({"label": __("Database collation"), "value": wpdb_.collate, "private": True})
        #// List must use plugins if there are any.
        mu_plugins_ = get_mu_plugins()
        for plugin_path_,plugin_ in mu_plugins_:
            plugin_version_ = plugin_["Version"]
            plugin_author_ = plugin_["Author"]
            plugin_version_string_ = __("No version or author information is available.")
            plugin_version_string_debug_ = "author: (undefined), version: (undefined)"
            if (not php_empty(lambda : plugin_version_)) and (not php_empty(lambda : plugin_author_)):
                #// translators: 1: Plugin version number. 2: Plugin author name.
                plugin_version_string_ = php_sprintf(__("Version %1$s by %2$s"), plugin_version_, plugin_author_)
                plugin_version_string_debug_ = php_sprintf("version: %s, author: %s", plugin_version_, plugin_author_)
            else:
                if (not php_empty(lambda : plugin_author_)):
                    #// translators: %s: Plugin author name.
                    plugin_version_string_ = php_sprintf(__("By %s"), plugin_author_)
                    plugin_version_string_debug_ = php_sprintf("author: %s, version: (undefined)", plugin_author_)
                # end if
                if (not php_empty(lambda : plugin_version_)):
                    #// translators: %s: Plugin version number.
                    plugin_version_string_ = php_sprintf(__("Version %s"), plugin_version_)
                    plugin_version_string_debug_ = php_sprintf("author: (undefined), version: %s", plugin_version_)
                # end if
            # end if
            info_["wp-mu-plugins"]["fields"][sanitize_text_field(plugin_["Name"])] = Array({"label": plugin_["Name"], "value": plugin_version_string_, "debug": plugin_version_string_debug_})
        # end for
        #// List all available plugins.
        plugins_ = get_plugins()
        plugin_updates_ = get_plugin_updates()
        for plugin_path_,plugin_ in plugins_:
            plugin_part_ = "wp-plugins-active" if is_plugin_active(plugin_path_) else "wp-plugins-inactive"
            plugin_version_ = plugin_["Version"]
            plugin_author_ = plugin_["Author"]
            plugin_version_string_ = __("No version or author information is available.")
            plugin_version_string_debug_ = "author: (undefined), version: (undefined)"
            if (not php_empty(lambda : plugin_version_)) and (not php_empty(lambda : plugin_author_)):
                #// translators: 1: Plugin version number. 2: Plugin author name.
                plugin_version_string_ = php_sprintf(__("Version %1$s by %2$s"), plugin_version_, plugin_author_)
                plugin_version_string_debug_ = php_sprintf("version: %s, author: %s", plugin_version_, plugin_author_)
            else:
                if (not php_empty(lambda : plugin_author_)):
                    #// translators: %s: Plugin author name.
                    plugin_version_string_ = php_sprintf(__("By %s"), plugin_author_)
                    plugin_version_string_debug_ = php_sprintf("author: %s, version: (undefined)", plugin_author_)
                # end if
                if (not php_empty(lambda : plugin_version_)):
                    #// translators: %s: Plugin version number.
                    plugin_version_string_ = php_sprintf(__("Version %s"), plugin_version_)
                    plugin_version_string_debug_ = php_sprintf("author: (undefined), version: %s", plugin_version_)
                # end if
            # end if
            if php_array_key_exists(plugin_path_, plugin_updates_):
                #// translators: %s: Latest plugin version number.
                plugin_version_string_ += " " + php_sprintf(__("(Latest version: %s)"), plugin_updates_[plugin_path_].update.new_version)
                plugin_version_string_debug_ += php_sprintf(" (latest version: %s)", plugin_updates_[plugin_path_].update.new_version)
            # end if
            info_[plugin_part_]["fields"][sanitize_text_field(plugin_["Name"])] = Array({"label": plugin_["Name"], "value": plugin_version_string_, "debug": plugin_version_string_debug_})
        # end for
        #// Populate the section for the currently active theme.
        global _wp_theme_features_
        php_check_if_defined("_wp_theme_features_")
        theme_features_ = Array()
        if (not php_empty(lambda : _wp_theme_features_)):
            for feature_,options_ in _wp_theme_features_:
                theme_features_[-1] = feature_
            # end for
        # end if
        active_theme_ = wp_get_theme()
        theme_updates_ = get_theme_updates()
        active_theme_version_ = active_theme_.version
        active_theme_version_debug_ = active_theme_version_
        if php_array_key_exists(active_theme_.stylesheet, theme_updates_):
            theme_update_new_version_ = theme_updates_[active_theme_.stylesheet].update["new_version"]
            #// translators: %s: Latest theme version number.
            active_theme_version_ += " " + php_sprintf(__("(Latest version: %s)"), theme_update_new_version_)
            active_theme_version_debug_ += php_sprintf(" (latest version: %s)", theme_update_new_version_)
        # end if
        active_theme_author_uri_ = active_theme_.display("AuthorURI")
        if active_theme_.parent_theme:
            active_theme_parent_theme_ = php_sprintf(__("%1$s (%2$s)"), active_theme_.parent_theme, active_theme_.template)
            active_theme_parent_theme_debug_ = php_sprintf("%s (%s)", active_theme_.parent_theme, active_theme_.template)
        else:
            active_theme_parent_theme_ = __("None")
            active_theme_parent_theme_debug_ = "none"
        # end if
        info_["wp-active-theme"]["fields"] = Array({"name": Array({"label": __("Name"), "value": php_sprintf(__("%1$s (%2$s)"), active_theme_.name, active_theme_.stylesheet)})}, {"version": Array({"label": __("Version"), "value": active_theme_version_, "debug": active_theme_version_debug_})}, {"author": Array({"label": __("Author"), "value": wp_kses(active_theme_.author, Array())})}, {"author_website": Array({"label": __("Author website"), "value": active_theme_author_uri_ if active_theme_author_uri_ else __("Undefined"), "debug": active_theme_author_uri_ if active_theme_author_uri_ else "(undefined)"})}, {"parent_theme": Array({"label": __("Parent theme"), "value": active_theme_parent_theme_, "debug": active_theme_parent_theme_debug_})}, {"theme_features": Array({"label": __("Theme features"), "value": php_implode(", ", theme_features_)})}, {"theme_path": Array({"label": __("Theme directory location"), "value": get_stylesheet_directory()})})
        parent_theme_ = active_theme_.parent()
        if parent_theme_:
            parent_theme_version_ = parent_theme_.version
            parent_theme_version_debug_ = parent_theme_version_
            if php_array_key_exists(parent_theme_.stylesheet, theme_updates_):
                parent_theme_update_new_version_ = theme_updates_[parent_theme_.stylesheet].update["new_version"]
                #// translators: %s: Latest theme version number.
                parent_theme_version_ += " " + php_sprintf(__("(Latest version: %s)"), parent_theme_update_new_version_)
                parent_theme_version_debug_ += php_sprintf(" (latest version: %s)", parent_theme_update_new_version_)
            # end if
            parent_theme_author_uri_ = parent_theme_.display("AuthorURI")
            info_["wp-parent-theme"]["fields"] = Array({"name": Array({"label": __("Name"), "value": php_sprintf(__("%1$s (%2$s)"), parent_theme_.name, parent_theme_.stylesheet)})}, {"version": Array({"label": __("Version"), "value": parent_theme_version_, "debug": parent_theme_version_debug_})}, {"author": Array({"label": __("Author"), "value": wp_kses(parent_theme_.author, Array())})}, {"author_website": Array({"label": __("Author website"), "value": parent_theme_author_uri_ if parent_theme_author_uri_ else __("Undefined"), "debug": parent_theme_author_uri_ if parent_theme_author_uri_ else "(undefined)"})}, {"theme_path": Array({"label": __("Theme directory location"), "value": get_template_directory()})})
        # end if
        #// Populate a list of all themes available in the install.
        all_themes_ = wp_get_themes()
        for theme_slug_,theme_ in all_themes_:
            #// Exclude the currently active theme from the list of all themes.
            if active_theme_.stylesheet == theme_slug_:
                continue
            # end if
            #// Exclude the currently active parent theme from the list of all themes.
            if (not php_empty(lambda : parent_theme_)) and parent_theme_.stylesheet == theme_slug_:
                continue
            # end if
            theme_version_ = theme_.version
            theme_author_ = theme_.author
            #// Sanitize.
            theme_author_ = wp_kses(theme_author_, Array())
            theme_version_string_ = __("No version or author information is available.")
            theme_version_string_debug_ = "undefined"
            if (not php_empty(lambda : theme_version_)) and (not php_empty(lambda : theme_author_)):
                #// translators: 1: Theme version number. 2: Theme author name.
                theme_version_string_ = php_sprintf(__("Version %1$s by %2$s"), theme_version_, theme_author_)
                theme_version_string_debug_ = php_sprintf("version: %s, author: %s", theme_version_, theme_author_)
            else:
                if (not php_empty(lambda : theme_author_)):
                    #// translators: %s: Theme author name.
                    theme_version_string_ = php_sprintf(__("By %s"), theme_author_)
                    theme_version_string_debug_ = php_sprintf("author: %s, version: (undefined)", theme_author_)
                # end if
                if (not php_empty(lambda : theme_version_)):
                    #// translators: %s: Theme version number.
                    theme_version_string_ = php_sprintf(__("Version %s"), theme_version_)
                    theme_version_string_debug_ = php_sprintf("author: (undefined), version: %s", theme_version_)
                # end if
            # end if
            if php_array_key_exists(theme_slug_, theme_updates_):
                #// translators: %s: Latest theme version number.
                theme_version_string_ += " " + php_sprintf(__("(Latest version: %s)"), theme_updates_[theme_slug_].update["new_version"])
                theme_version_string_debug_ += php_sprintf(" (latest version: %s)", theme_updates_[theme_slug_].update["new_version"])
            # end if
            info_["wp-themes-inactive"]["fields"][sanitize_text_field(theme_.name)] = Array({"label": php_sprintf(__("%1$s (%2$s)"), theme_.name, theme_slug_), "value": theme_version_string_, "debug": theme_version_string_debug_})
        # end for
        #// Add more filesystem checks.
        if php_defined("WPMU_PLUGIN_DIR") and php_is_dir(WPMU_PLUGIN_DIR):
            is_writable_wpmu_plugin_dir_ = wp_is_writable(WPMU_PLUGIN_DIR)
            info_["wp-filesystem"]["fields"]["mu-plugins"] = Array({"label": __("The must use plugins directory"), "value": __("Writable") if is_writable_wpmu_plugin_dir_ else __("Not writable"), "debug": "writable" if is_writable_wpmu_plugin_dir_ else "not writable"})
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
        info_ = apply_filters("debug_information", info_)
        return info_
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
    def format(self, info_array_=None, type_=None):
        
        
        return_ = "`\n"
        for section_,details_ in info_array_:
            #// Skip this section if there are no fields, or the section has been declared as private.
            if php_empty(lambda : details_["fields"]) or (php_isset(lambda : details_["private"])) and details_["private"]:
                continue
            # end if
            section_label_ = section_ if "debug" == type_ else details_["label"]
            return_ += php_sprintf("### %s%s ###\n\n", section_label_, php_sprintf(" (%d)", php_count(details_["fields"])) if (php_isset(lambda : details_["show_count"])) and details_["show_count"] else "")
            for field_name_,field_ in details_["fields"]:
                if (php_isset(lambda : field_["private"])) and True == field_["private"]:
                    continue
                # end if
                if "debug" == type_ and (php_isset(lambda : field_["debug"])):
                    debug_data_ = field_["debug"]
                else:
                    debug_data_ = field_["value"]
                # end if
                #// Can be array, one level deep only.
                if php_is_array(debug_data_):
                    value_ = ""
                    for sub_field_name_,sub_field_value_ in debug_data_:
                        value_ += php_sprintf("\n   %s: %s", sub_field_name_, sub_field_value_)
                    # end for
                elif php_is_bool(debug_data_):
                    value_ = "true" if debug_data_ else "false"
                elif php_empty(lambda : debug_data_) and "0" != debug_data_:
                    value_ = "undefined"
                else:
                    value_ = debug_data_
                # end if
                if "debug" == type_:
                    label_ = field_name_
                else:
                    label_ = field_["label"]
                # end if
                return_ += php_sprintf("%s: %s\n", label_, value_)
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
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        size_ = 0
        rows_ = wpdb_.get_results("SHOW TABLE STATUS", ARRAY_A)
        if wpdb_.num_rows > 0:
            for row_ in rows_:
                size_ += row_["Data_length"] + row_["Index_length"]
            # end for
        # end if
        return php_int(size_)
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
        
        
        size_db_ = self.get_database_size()
        upload_dir_ = wp_get_upload_dir()
        #// 
        #// We will be using the PHP max execution time to prevent the size calculations
        #// from causing a timeout. The default value is 30 seconds, and some
        #// hosts do not allow you to read configuration values.
        #//
        if php_function_exists("ini_get"):
            max_execution_time_ = php_ini_get("max_execution_time")
        # end if
        #// The max_execution_time defaults to 0 when PHP runs from cli.
        #// We still want to limit it below.
        if php_empty(lambda : max_execution_time_):
            max_execution_time_ = 30
        # end if
        if max_execution_time_ > 20:
            #// If the max_execution_time is set to lower than 20 seconds, reduce it a bit to prevent
            #// edge-case timeouts that may happen after the size loop has finished running.
            max_execution_time_ -= 2
        # end if
        #// Go through the various installation directories and calculate their sizes.
        #// No trailing slashes.
        paths_ = Array({"wordpress_size": untrailingslashit(ABSPATH), "themes_size": get_theme_root(), "plugins_size": WP_PLUGIN_DIR, "uploads_size": upload_dir_["basedir"]})
        exclude_ = paths_
        exclude_["wordpress_size"] = None
        exclude_ = php_array_values(exclude_)
        size_total_ = 0
        all_sizes_ = Array()
        #// Loop over all the directories we want to gather the sizes for.
        for name_,path_ in paths_:
            dir_size_ = None
            #// Default to timeout.
            results_ = Array({"path": path_, "raw": 0})
            if php_microtime(True) - WP_START_TIMESTAMP < max_execution_time_:
                if "wordpress_size" == name_:
                    dir_size_ = recurse_dirsize(path_, exclude_, max_execution_time_)
                else:
                    dir_size_ = recurse_dirsize(path_, None, max_execution_time_)
                # end if
            # end if
            if False == dir_size_:
                #// Error reading.
                results_["size"] = __("The size cannot be calculated. The directory is not accessible. Usually caused by invalid permissions.")
                results_["debug"] = "not accessible"
                #// Stop total size calculation.
                size_total_ = None
            elif None == dir_size_:
                #// Timeout.
                results_["size"] = __("The directory size calculation has timed out. Usually caused by a very large number of sub-directories and files.")
                results_["debug"] = "timeout while calculating size"
                #// Stop total size calculation.
                size_total_ = None
            else:
                if None != size_total_:
                    size_total_ += dir_size_
                # end if
                results_["raw"] = dir_size_
                results_["size"] = size_format(dir_size_, 2)
                results_["debug"] = results_["size"] + str(" (") + str(dir_size_) + str(" bytes)")
            # end if
            all_sizes_[name_] = results_
        # end for
        if size_db_ > 0:
            database_size_ = size_format(size_db_, 2)
            all_sizes_["database_size"] = Array({"raw": size_db_, "size": database_size_, "debug": database_size_ + str(" (") + str(size_db_) + str(" bytes)")})
        else:
            all_sizes_["database_size"] = Array({"size": __("Not available"), "debug": "not available"})
        # end if
        if None != size_total_ and size_db_ > 0:
            total_size_ = size_total_ + size_db_
            total_size_mb_ = size_format(total_size_, 2)
            all_sizes_["total_size"] = Array({"raw": total_size_, "size": total_size_mb_, "debug": total_size_mb_ + str(" (") + str(total_size_) + str(" bytes)")})
        else:
            all_sizes_["total_size"] = Array({"size": __("Total size is not available. Some errors were encountered when determining the size of your installation."), "debug": "not available"})
        # end if
        return all_sizes_
    # end def get_sizes
# end class WP_Debug_Data
