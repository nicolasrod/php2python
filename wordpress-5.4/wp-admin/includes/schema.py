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
#// WordPress Administration Scheme API
#// 
#// Here we keep the DB structure and option values.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Declare these as global in case schema.php is included from a function.
#// 
#// @global wpdb   $wpdb            WordPress database abstraction object.
#// @global array  $wp_queries
#// @global string $charset_collate
#//
global wpdb_
global wp_queries_
global charset_collate_
php_check_if_defined("wpdb_","wp_queries_","charset_collate_")
#// 
#// The database character collate.
#//
charset_collate_ = wpdb_.get_charset_collate()
#// 
#// Retrieve the SQL for creating database tables.
#// 
#// @since 3.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $scope Optional. The tables for which to retrieve SQL. Can be all, global, ms_global, or blog tables. Defaults to all.
#// @param int $blog_id Optional. The site ID for which to retrieve SQL. Default is the current site ID.
#// @return string The SQL needed to create the requested tables.
#//
def wp_get_db_schema(scope_="all", blog_id_=None, *_args_):
    if blog_id_ is None:
        blog_id_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    charset_collate_ = wpdb_.get_charset_collate()
    if blog_id_ and blog_id_ != wpdb_.blogid:
        old_blog_id_ = wpdb_.set_blog_id(blog_id_)
    # end if
    #// Engage multisite if in the middle of turning it on from network.php.
    is_multisite_ = is_multisite() or php_defined("WP_INSTALLING_NETWORK") and WP_INSTALLING_NETWORK
    #// 
    #// Indexes have a maximum size of 767 bytes. Historically, we haven't need to be concerned about that.
    #// As of 4.2, however, we moved to utf8mb4, which uses 4 bytes per character. This means that an index which
    #// used to have room for floor(767/3) = 255 characters, now only has room for floor(767/4) = 191 characters.
    #//
    max_index_length_ = 191
    #// Blog-specific tables.
    blog_tables_ = str("CREATE TABLE ") + str(wpdb_.termmeta) + str(""" (\n meta_id bigint(20) unsigned NOT NULL auto_increment,\n  term_id bigint(20) unsigned NOT NULL default '0',\n meta_key varchar(255) default NULL,\n   meta_value longtext,\n  PRIMARY KEY  (meta_id),\n   KEY term_id (term_id),\n    KEY meta_key (meta_key(""") + str(max_index_length_) + str("))\n) ") + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.terms) + str(""" (\n term_id bigint(20) unsigned NOT NULL auto_increment,\n name varchar(200) NOT NULL default '',\n slug varchar(200) NOT NULL default '',\n term_group bigint(10) NOT NULL default 0,\n PRIMARY KEY  (term_id),\n KEY slug (slug(""") + str(max_index_length_) + str(")),\n KEY name (name(") + str(max_index_length_) + str("))\n) ") + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.term_taxonomy) + str(""" (\n term_taxonomy_id bigint(20) unsigned NOT NULL auto_increment,\n term_id bigint(20) unsigned NOT NULL default 0,\n taxonomy varchar(32) NOT NULL default '',\n description longtext NOT NULL,\n parent bigint(20) unsigned NOT NULL default 0,\n count bigint(20) NOT NULL default 0,\n PRIMARY KEY  (term_taxonomy_id),\n UNIQUE KEY term_id_taxonomy (term_id,taxonomy),\n KEY taxonomy (taxonomy)\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.term_relationships) + str(""" (\n object_id bigint(20) unsigned NOT NULL default 0,\n term_taxonomy_id bigint(20) unsigned NOT NULL default 0,\n term_order int(11) NOT NULL default 0,\n PRIMARY KEY  (object_id,term_taxonomy_id),\n KEY term_taxonomy_id (term_taxonomy_id)\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.commentmeta) + str(""" (\n    meta_id bigint(20) unsigned NOT NULL auto_increment,\n  comment_id bigint(20) unsigned NOT NULL default '0',\n  meta_key varchar(255) default NULL,\n   meta_value longtext,\n  PRIMARY KEY  (meta_id),\n   KEY comment_id (comment_id),\n  KEY meta_key (meta_key(""") + str(max_index_length_) + str("))\n) ") + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.comments) + str(""" (\n  comment_ID bigint(20) unsigned NOT NULL auto_increment,\n   comment_post_ID bigint(20) unsigned NOT NULL default '0',\n comment_author tinytext NOT NULL,\n comment_author_email varchar(100) NOT NULL default '',\n    comment_author_url varchar(200) NOT NULL default '',\n  comment_author_IP varchar(100) NOT NULL default '',\n   comment_date datetime NOT NULL default '0000-00-00 00:00:00',\n comment_date_gmt datetime NOT NULL default '0000-00-00 00:00:00',\n comment_content text NOT NULL,\n    comment_karma int(11) NOT NULL default '0',\n   comment_approved varchar(20) NOT NULL default '1',\n    comment_agent varchar(255) NOT NULL default '',\n   comment_type varchar(20) NOT NULL default '',\n comment_parent bigint(20) unsigned NOT NULL default '0',\n  user_id bigint(20) unsigned NOT NULL default '0',\n PRIMARY KEY  (comment_ID),\n    KEY comment_post_ID (comment_post_ID),\n    KEY comment_approved_date_gmt (comment_approved,comment_date_gmt),\n    KEY comment_date_gmt (comment_date_gmt),\n  KEY comment_parent (comment_parent),\n  KEY comment_author_email (comment_author_email(10))\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.links) + str(""" (\n  link_id bigint(20) unsigned NOT NULL auto_increment,\n  link_url varchar(255) NOT NULL default '',\n    link_name varchar(255) NOT NULL default '',\n   link_image varchar(255) NOT NULL default '',\n  link_target varchar(25) NOT NULL default '',\n  link_description varchar(255) NOT NULL default '',\n    link_visible varchar(20) NOT NULL default 'Y',\n    link_owner bigint(20) unsigned NOT NULL default '1',\n  link_rating int(11) NOT NULL default '0',\n link_updated datetime NOT NULL default '0000-00-00 00:00:00',\n link_rel varchar(255) NOT NULL default '',\n    link_notes mediumtext NOT NULL,\n   link_rss varchar(255) NOT NULL default '',\n    PRIMARY KEY  (link_id),\n   KEY link_visible (link_visible)\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.options) + str(""" (\n    option_id bigint(20) unsigned NOT NULL auto_increment,\n    option_name varchar(191) NOT NULL default '',\n option_value longtext NOT NULL,\n   autoload varchar(20) NOT NULL default 'yes',\n  PRIMARY KEY  (option_id),\n UNIQUE KEY option_name (option_name),\n KEY autoload (autoload)\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.postmeta) + str(""" (\n   meta_id bigint(20) unsigned NOT NULL auto_increment,\n  post_id bigint(20) unsigned NOT NULL default '0',\n meta_key varchar(255) default NULL,\n   meta_value longtext,\n  PRIMARY KEY  (meta_id),\n   KEY post_id (post_id),\n    KEY meta_key (meta_key(""") + str(max_index_length_) + str("))\n) ") + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.posts) + str(""" (\n ID bigint(20) unsigned NOT NULL auto_increment,\n   post_author bigint(20) unsigned NOT NULL default '0',\n post_date datetime NOT NULL default '0000-00-00 00:00:00',\n    post_date_gmt datetime NOT NULL default '0000-00-00 00:00:00',\n    post_content longtext NOT NULL,\n   post_title text NOT NULL,\n post_excerpt text NOT NULL,\n   post_status varchar(20) NOT NULL default 'publish',\n   comment_status varchar(20) NOT NULL default 'open',\n   ping_status varchar(20) NOT NULL default 'open',\n  post_password varchar(255) NOT NULL default '',\n   post_name varchar(200) NOT NULL default '',\n   to_ping text NOT NULL,\n    pinged text NOT NULL,\n post_modified datetime NOT NULL default '0000-00-00 00:00:00',\n    post_modified_gmt datetime NOT NULL default '0000-00-00 00:00:00',\n    post_content_filtered longtext NOT NULL,\n  post_parent bigint(20) unsigned NOT NULL default '0',\n guid varchar(255) NOT NULL default '',\n    menu_order int(11) NOT NULL default '0',\n  post_type varchar(20) NOT NULL default 'post',\n    post_mime_type varchar(100) NOT NULL default '',\n  comment_count bigint(20) NOT NULL default '0',\n    PRIMARY KEY  (ID),\n    KEY post_name (post_name(""") + str(max_index_length_) + str(""")),\n   KEY type_status_date (post_type,post_status,post_date,ID),\n    KEY post_parent (post_parent),\n    KEY post_author (post_author)\n) """) + str(charset_collate_) + str(";\n")
    #// Single site users table. The multisite flavor of the users table is handled below.
    users_single_table_ = str("CREATE TABLE ") + str(wpdb_.users) + str(""" (\n ID bigint(20) unsigned NOT NULL auto_increment,\n   user_login varchar(60) NOT NULL default '',\n   user_pass varchar(255) NOT NULL default '',\n   user_nicename varchar(50) NOT NULL default '',\n    user_email varchar(100) NOT NULL default '',\n  user_url varchar(100) NOT NULL default '',\n    user_registered datetime NOT NULL default '0000-00-00 00:00:00',\n  user_activation_key varchar(255) NOT NULL default '',\n user_status int(11) NOT NULL default '0',\n display_name varchar(250) NOT NULL default '',\n    PRIMARY KEY  (ID),\n    KEY user_login_key (user_login),\n  KEY user_nicename (user_nicename),\n    KEY user_email (user_email)\n) """) + str(charset_collate_) + str(";\n")
    #// Multisite users table.
    users_multi_table_ = str("CREATE TABLE ") + str(wpdb_.users) + str(""" (\n  ID bigint(20) unsigned NOT NULL auto_increment,\n   user_login varchar(60) NOT NULL default '',\n   user_pass varchar(255) NOT NULL default '',\n   user_nicename varchar(50) NOT NULL default '',\n    user_email varchar(100) NOT NULL default '',\n  user_url varchar(100) NOT NULL default '',\n    user_registered datetime NOT NULL default '0000-00-00 00:00:00',\n  user_activation_key varchar(255) NOT NULL default '',\n user_status int(11) NOT NULL default '0',\n display_name varchar(250) NOT NULL default '',\n    spam tinyint(2) NOT NULL default '0',\n deleted tinyint(2) NOT NULL default '0',\n  PRIMARY KEY  (ID),\n    KEY user_login_key (user_login),\n  KEY user_nicename (user_nicename),\n    KEY user_email (user_email)\n) """) + str(charset_collate_) + str(";\n")
    #// Usermeta.
    usermeta_table_ = str("CREATE TABLE ") + str(wpdb_.usermeta) + str(""" (\n  umeta_id bigint(20) unsigned NOT NULL auto_increment,\n user_id bigint(20) unsigned NOT NULL default '0',\n meta_key varchar(255) default NULL,\n   meta_value longtext,\n  PRIMARY KEY  (umeta_id),\n  KEY user_id (user_id),\n    KEY meta_key (meta_key(""") + str(max_index_length_) + str("))\n) ") + str(charset_collate_) + str(";\n")
    #// Global tables.
    if is_multisite_:
        global_tables_ = users_multi_table_ + usermeta_table_
    else:
        global_tables_ = users_single_table_ + usermeta_table_
    # end if
    #// Multisite global tables.
    ms_global_tables_ = str("CREATE TABLE ") + str(wpdb_.blogs) + str(""" (\n   blog_id bigint(20) NOT NULL auto_increment,\n   site_id bigint(20) NOT NULL default '0',\n  domain varchar(200) NOT NULL default '',\n  path varchar(100) NOT NULL default '',\n    registered datetime NOT NULL default '0000-00-00 00:00:00',\n   last_updated datetime NOT NULL default '0000-00-00 00:00:00',\n public tinyint(2) NOT NULL default '1',\n   archived tinyint(2) NOT NULL default '0',\n mature tinyint(2) NOT NULL default '0',\n   spam tinyint(2) NOT NULL default '0',\n deleted tinyint(2) NOT NULL default '0',\n  lang_id int(11) NOT NULL default '0',\n PRIMARY KEY  (blog_id),\n   KEY domain (domain(50),path(5)),\n  KEY lang_id (lang_id)\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.blogmeta) + str(""" (\n meta_id bigint(20) unsigned NOT NULL auto_increment,\n  blog_id bigint(20) NOT NULL default '0',\n  meta_key varchar(255) default NULL,\n   meta_value longtext,\n  PRIMARY KEY  (meta_id),\n   KEY meta_key (meta_key(""") + str(max_index_length_) + str(")),\n   KEY blog_id (blog_id)\n) ") + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.registration_log) + str(""" (\n   ID bigint(20) NOT NULL auto_increment,\n    email varchar(255) NOT NULL default '',\n   IP varchar(30) NOT NULL default '',\n   blog_id bigint(20) NOT NULL default '0',\n  date_registered datetime NOT NULL default '0000-00-00 00:00:00',\n  PRIMARY KEY  (ID),\n    KEY IP (IP)\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.site) + str(""" (\n   id bigint(20) NOT NULL auto_increment,\n    domain varchar(200) NOT NULL default '',\n  path varchar(100) NOT NULL default '',\n    PRIMARY KEY  (id),\n    KEY domain (domain(140),path(51))\n) """) + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.sitemeta) + str(""" (\n meta_id bigint(20) NOT NULL auto_increment,\n   site_id bigint(20) NOT NULL default '0',\n  meta_key varchar(255) default NULL,\n   meta_value longtext,\n  PRIMARY KEY  (meta_id),\n   KEY meta_key (meta_key(""") + str(max_index_length_) + str(")),\n   KEY site_id (site_id)\n) ") + str(charset_collate_) + str(";\nCREATE TABLE ") + str(wpdb_.signups) + str(""" (\n    signup_id bigint(20) NOT NULL auto_increment,\n domain varchar(200) NOT NULL default '',\n  path varchar(100) NOT NULL default '',\n    title longtext NOT NULL,\n  user_login varchar(60) NOT NULL default '',\n   user_email varchar(100) NOT NULL default '',\n  registered datetime NOT NULL default '0000-00-00 00:00:00',\n   activated datetime NOT NULL default '0000-00-00 00:00:00',\n    active tinyint(1) NOT NULL default '0',\n   activation_key varchar(50) NOT NULL default '',\n   meta longtext,\n    PRIMARY KEY  (signup_id),\n KEY activation_key (activation_key),\n  KEY user_email (user_email),\n  KEY user_login_email (user_login,user_email),\n KEY domain_path (domain(140),path(51))\n) """) + str(charset_collate_) + str(";")
    for case in Switch(scope_):
        if case("blog"):
            queries_ = blog_tables_
            break
        # end if
        if case("global"):
            queries_ = global_tables_
            if is_multisite_:
                queries_ += ms_global_tables_
            # end if
            break
        # end if
        if case("ms_global"):
            queries_ = ms_global_tables_
            break
        # end if
        if case("all"):
            pass
        # end if
        if case():
            queries_ = global_tables_ + blog_tables_
            if is_multisite_:
                queries_ += ms_global_tables_
            # end if
            break
        # end if
    # end for
    if (php_isset(lambda : old_blog_id_)):
        wpdb_.set_blog_id(old_blog_id_)
    # end if
    return queries_
# end def wp_get_db_schema
#// Populate for back compat.
wp_queries_ = wp_get_db_schema("all")
#// 
#// Create WordPress options and set the default values.
#// 
#// @since 1.5.0
#// @since 5.1.0 The $options parameter has been added.
#// 
#// @global wpdb $wpdb                  WordPress database abstraction object.
#// @global int  $wp_db_version         WordPress database version.
#// @global int  $wp_current_db_version The old (current) database version.
#// 
#// @param array $options Optional. Custom option $key => $value pairs to use. Default empty array.
#//
def populate_options(options_=None, *_args_):
    if options_ is None:
        options_ = Array()
    # end if
    
    global wpdb_
    global wp_db_version_
    global wp_current_db_version_
    php_check_if_defined("wpdb_","wp_db_version_","wp_current_db_version_")
    guessurl_ = wp_guess_url()
    #// 
    #// Fires before creating WordPress options and populating their default values.
    #// 
    #// @since 2.6.0
    #//
    do_action("populate_options")
    if php_ini_get("safe_mode"):
        #// Safe mode can break mkdir() so use a flat structure by default.
        uploads_use_yearmonth_folders_ = 0
    else:
        uploads_use_yearmonth_folders_ = 1
    # end if
    #// If WP_DEFAULT_THEME doesn't exist, fall back to the latest core default theme.
    stylesheet_ = WP_DEFAULT_THEME
    template_ = WP_DEFAULT_THEME
    theme_ = wp_get_theme(WP_DEFAULT_THEME)
    if (not theme_.exists()):
        theme_ = WP_Theme.get_core_default_theme()
    # end if
    #// If we can't find a core default theme, WP_DEFAULT_THEME is the best we can do.
    if theme_:
        stylesheet_ = theme_.get_stylesheet()
        template_ = theme_.get_template()
    # end if
    timezone_string_ = ""
    gmt_offset_ = 0
    #// 
    #// translators: default GMT offset or timezone string. Must be either a valid offset (-12 to 14)
    #// or a valid timezone string (America/New_York). See https://www.php.net/manual/en/timezones.php
    #// for all timezone strings supported by PHP.
    #//
    offset_or_tz_ = _x("0", "default GMT offset or timezone string")
    #// phpcs:ignore WordPress.WP.I18n.NoEmptyStrings
    if php_is_numeric(offset_or_tz_):
        gmt_offset_ = offset_or_tz_
    elif offset_or_tz_ and php_in_array(offset_or_tz_, timezone_identifiers_list()):
        timezone_string_ = offset_or_tz_
    # end if
    defaults_ = Array({"siteurl": guessurl_, "home": guessurl_, "blogname": __("My Site"), "blogdescription": __("Just another WordPress site"), "users_can_register": 0, "admin_email": "you@example.com", "start_of_week": _x("1", "start of week"), "use_balanceTags": 0, "use_smilies": 1, "require_name_email": 1, "comments_notify": 1, "posts_per_rss": 10, "rss_use_excerpt": 0, "mailserver_url": "mail.example.com", "mailserver_login": "login@example.com", "mailserver_pass": "password", "mailserver_port": 110, "default_category": 1, "default_comment_status": "open", "default_ping_status": "open", "default_pingback_flag": 1, "posts_per_page": 10, "date_format": __("F j, Y"), "time_format": __("g:i a"), "links_updated_date_format": __("F j, Y g:i a"), "comment_moderation": 0, "moderation_notify": 1, "permalink_structure": "", "rewrite_rules": "", "hack_file": 0, "blog_charset": "UTF-8", "moderation_keys": "", "active_plugins": Array(), "category_base": "", "ping_sites": "http://rpc.pingomatic.com/", "comment_max_links": 2, "gmt_offset": gmt_offset_, "default_email_category": 1, "recently_edited": "", "template": template_, "stylesheet": stylesheet_, "comment_whitelist": 1, "blacklist_keys": "", "comment_registration": 0, "html_type": "text/html", "use_trackback": 0, "default_role": "subscriber", "db_version": wp_db_version_, "uploads_use_yearmonth_folders": uploads_use_yearmonth_folders_, "upload_path": "", "blog_public": "1", "default_link_category": 2, "show_on_front": "posts", "tag_base": "", "show_avatars": "1", "avatar_rating": "G", "upload_url_path": "", "thumbnail_size_w": 150, "thumbnail_size_h": 150, "thumbnail_crop": 1, "medium_size_w": 300, "medium_size_h": 300, "avatar_default": "mystery", "large_size_w": 1024, "large_size_h": 1024, "image_default_link_type": "none", "image_default_size": "", "image_default_align": "", "close_comments_for_old_posts": 0, "close_comments_days_old": 14, "thread_comments": 1, "thread_comments_depth": 5, "page_comments": 0, "comments_per_page": 50, "default_comments_page": "newest", "comment_order": "asc", "sticky_posts": Array(), "widget_categories": Array(), "widget_text": Array(), "widget_rss": Array(), "uninstall_plugins": Array(), "timezone_string": timezone_string_, "page_for_posts": 0, "page_on_front": 0, "default_post_format": 0, "link_manager_enabled": 0, "finished_splitting_shared_terms": 1, "site_icon": 0, "medium_large_size_w": 768, "medium_large_size_h": 0, "wp_page_for_privacy_policy": 0, "show_comments_cookies_opt_in": 1, "admin_email_lifespan": time() + 6 * MONTH_IN_SECONDS})
    #// 3.3
    if (not is_multisite()):
        defaults_["initial_db_version"] = wp_current_db_version_ if (not php_empty(lambda : wp_current_db_version_)) and wp_current_db_version_ < wp_db_version_ else wp_db_version_
    # end if
    #// 3.0 multisite.
    if is_multisite():
        #// translators: %s: Network title.
        defaults_["blogdescription"] = php_sprintf(__("Just another %s site"), get_network().site_name)
        defaults_["permalink_structure"] = "/%year%/%monthnum%/%day%/%postname%/"
    # end if
    options_ = wp_parse_args(options_, defaults_)
    #// Set autoload to no for these options.
    fat_options_ = Array("moderation_keys", "recently_edited", "blacklist_keys", "uninstall_plugins")
    keys_ = "'" + php_implode("', '", php_array_keys(options_)) + "'"
    existing_options_ = wpdb_.get_col(str("SELECT option_name FROM ") + str(wpdb_.options) + str(" WHERE option_name in ( ") + str(keys_) + str(" )"))
    #// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
    insert_ = ""
    for option_,value_ in options_.items():
        if php_in_array(option_, existing_options_):
            continue
        # end if
        if php_in_array(option_, fat_options_):
            autoload_ = "no"
        else:
            autoload_ = "yes"
        # end if
        if php_is_array(value_):
            value_ = serialize(value_)
        # end if
        if (not php_empty(lambda : insert_)):
            insert_ += ", "
        # end if
        insert_ += wpdb_.prepare("(%s, %s, %s)", option_, value_, autoload_)
    # end for
    if (not php_empty(lambda : insert_)):
        wpdb_.query(str("INSERT INTO ") + str(wpdb_.options) + str(" (option_name, option_value, autoload) VALUES ") + insert_)
        pass
    # end if
    #// In case it is set, but blank, update "home".
    if (not __get_option("home")):
        update_option("home", guessurl_)
    # end if
    #// Delete unused options.
    unusedoptions_ = Array("blodotgsping_url", "bodyterminator", "emailtestonly", "phoneemail_separator", "smilies_directory", "subjectprefix", "use_bbcode", "use_blodotgsping", "use_phoneemail", "use_quicktags", "use_weblogsping", "weblogs_cache_file", "use_preview", "use_htmltrans", "smilies_directory", "fileupload_allowedusers", "use_phoneemail", "default_post_status", "default_post_category", "archive_mode", "time_difference", "links_minadminlevel", "links_use_adminlevels", "links_rating_type", "links_rating_char", "links_rating_ignore_zero", "links_rating_single_image", "links_rating_image0", "links_rating_image1", "links_rating_image2", "links_rating_image3", "links_rating_image4", "links_rating_image5", "links_rating_image6", "links_rating_image7", "links_rating_image8", "links_rating_image9", "links_recently_updated_time", "links_recently_updated_prepend", "links_recently_updated_append", "weblogs_cacheminutes", "comment_allowed_tags", "search_engine_friendly_urls", "default_geourl_lat", "default_geourl_lon", "use_default_geourl", "weblogs_xml_url", "new_users_can_blog", "_wpnonce", "_wp_http_referer", "Update", "action", "rich_editing", "autosave_interval", "deactivated_plugins", "can_compress_scripts", "page_uris", "update_core", "update_plugins", "update_themes", "doing_cron", "random_seed", "rss_excerpt_length", "secret", "use_linksupdate", "default_comment_status_page", "wporg_popular_tags", "what_to_show", "rss_language", "language", "enable_xmlrpc", "enable_app", "embed_autourls", "default_post_edit_rows", "gzipcompression", "advanced_edit")
    for option_ in unusedoptions_:
        delete_option(option_)
    # end for
    #// Delete obsolete magpie stuff.
    wpdb_.query(str("DELETE FROM ") + str(wpdb_.options) + str(" WHERE option_name REGEXP '^rss_[0-9a-f]{32}(_ts)?$'"))
    #// Clear expired transients.
    delete_expired_transients(True)
# end def populate_options
#// 
#// Execute WordPress role creation for the various WordPress versions.
#// 
#// @since 2.0.0
#//
def populate_roles(*_args_):
    
    
    populate_roles_160()
    populate_roles_210()
    populate_roles_230()
    populate_roles_250()
    populate_roles_260()
    populate_roles_270()
    populate_roles_280()
    populate_roles_300()
# end def populate_roles
#// 
#// Create the roles for WordPress 2.0
#// 
#// @since 2.0.0
#//
def populate_roles_160(*_args_):
    
    
    #// Add roles.
    add_role("administrator", "Administrator")
    add_role("editor", "Editor")
    add_role("author", "Author")
    add_role("contributor", "Contributor")
    add_role("subscriber", "Subscriber")
    #// Add caps for Administrator role.
    role_ = get_role("administrator")
    role_.add_cap("switch_themes")
    role_.add_cap("edit_themes")
    role_.add_cap("activate_plugins")
    role_.add_cap("edit_plugins")
    role_.add_cap("edit_users")
    role_.add_cap("edit_files")
    role_.add_cap("manage_options")
    role_.add_cap("moderate_comments")
    role_.add_cap("manage_categories")
    role_.add_cap("manage_links")
    role_.add_cap("upload_files")
    role_.add_cap("import")
    role_.add_cap("unfiltered_html")
    role_.add_cap("edit_posts")
    role_.add_cap("edit_others_posts")
    role_.add_cap("edit_published_posts")
    role_.add_cap("publish_posts")
    role_.add_cap("edit_pages")
    role_.add_cap("read")
    role_.add_cap("level_10")
    role_.add_cap("level_9")
    role_.add_cap("level_8")
    role_.add_cap("level_7")
    role_.add_cap("level_6")
    role_.add_cap("level_5")
    role_.add_cap("level_4")
    role_.add_cap("level_3")
    role_.add_cap("level_2")
    role_.add_cap("level_1")
    role_.add_cap("level_0")
    #// Add caps for Editor role.
    role_ = get_role("editor")
    role_.add_cap("moderate_comments")
    role_.add_cap("manage_categories")
    role_.add_cap("manage_links")
    role_.add_cap("upload_files")
    role_.add_cap("unfiltered_html")
    role_.add_cap("edit_posts")
    role_.add_cap("edit_others_posts")
    role_.add_cap("edit_published_posts")
    role_.add_cap("publish_posts")
    role_.add_cap("edit_pages")
    role_.add_cap("read")
    role_.add_cap("level_7")
    role_.add_cap("level_6")
    role_.add_cap("level_5")
    role_.add_cap("level_4")
    role_.add_cap("level_3")
    role_.add_cap("level_2")
    role_.add_cap("level_1")
    role_.add_cap("level_0")
    #// Add caps for Author role.
    role_ = get_role("author")
    role_.add_cap("upload_files")
    role_.add_cap("edit_posts")
    role_.add_cap("edit_published_posts")
    role_.add_cap("publish_posts")
    role_.add_cap("read")
    role_.add_cap("level_2")
    role_.add_cap("level_1")
    role_.add_cap("level_0")
    #// Add caps for Contributor role.
    role_ = get_role("contributor")
    role_.add_cap("edit_posts")
    role_.add_cap("read")
    role_.add_cap("level_1")
    role_.add_cap("level_0")
    #// Add caps for Subscriber role.
    role_ = get_role("subscriber")
    role_.add_cap("read")
    role_.add_cap("level_0")
# end def populate_roles_160
#// 
#// Create and modify WordPress roles for WordPress 2.1.
#// 
#// @since 2.1.0
#//
def populate_roles_210(*_args_):
    
    
    roles_ = Array("administrator", "editor")
    for role_ in roles_:
        role_ = get_role(role_)
        if php_empty(lambda : role_):
            continue
        # end if
        role_.add_cap("edit_others_pages")
        role_.add_cap("edit_published_pages")
        role_.add_cap("publish_pages")
        role_.add_cap("delete_pages")
        role_.add_cap("delete_others_pages")
        role_.add_cap("delete_published_pages")
        role_.add_cap("delete_posts")
        role_.add_cap("delete_others_posts")
        role_.add_cap("delete_published_posts")
        role_.add_cap("delete_private_posts")
        role_.add_cap("edit_private_posts")
        role_.add_cap("read_private_posts")
        role_.add_cap("delete_private_pages")
        role_.add_cap("edit_private_pages")
        role_.add_cap("read_private_pages")
    # end for
    role_ = get_role("administrator")
    if (not php_empty(lambda : role_)):
        role_.add_cap("delete_users")
        role_.add_cap("create_users")
    # end if
    role_ = get_role("author")
    if (not php_empty(lambda : role_)):
        role_.add_cap("delete_posts")
        role_.add_cap("delete_published_posts")
    # end if
    role_ = get_role("contributor")
    if (not php_empty(lambda : role_)):
        role_.add_cap("delete_posts")
    # end if
# end def populate_roles_210
#// 
#// Create and modify WordPress roles for WordPress 2.3.
#// 
#// @since 2.3.0
#//
def populate_roles_230(*_args_):
    
    
    role_ = get_role("administrator")
    if (not php_empty(lambda : role_)):
        role_.add_cap("unfiltered_upload")
    # end if
# end def populate_roles_230
#// 
#// Create and modify WordPress roles for WordPress 2.5.
#// 
#// @since 2.5.0
#//
def populate_roles_250(*_args_):
    
    
    role_ = get_role("administrator")
    if (not php_empty(lambda : role_)):
        role_.add_cap("edit_dashboard")
    # end if
# end def populate_roles_250
#// 
#// Create and modify WordPress roles for WordPress 2.6.
#// 
#// @since 2.6.0
#//
def populate_roles_260(*_args_):
    
    
    role_ = get_role("administrator")
    if (not php_empty(lambda : role_)):
        role_.add_cap("update_plugins")
        role_.add_cap("delete_plugins")
    # end if
# end def populate_roles_260
#// 
#// Create and modify WordPress roles for WordPress 2.7.
#// 
#// @since 2.7.0
#//
def populate_roles_270(*_args_):
    
    
    role_ = get_role("administrator")
    if (not php_empty(lambda : role_)):
        role_.add_cap("install_plugins")
        role_.add_cap("update_themes")
    # end if
# end def populate_roles_270
#// 
#// Create and modify WordPress roles for WordPress 2.8.
#// 
#// @since 2.8.0
#//
def populate_roles_280(*_args_):
    
    
    role_ = get_role("administrator")
    if (not php_empty(lambda : role_)):
        role_.add_cap("install_themes")
    # end if
# end def populate_roles_280
#// 
#// Create and modify WordPress roles for WordPress 3.0.
#// 
#// @since 3.0.0
#//
def populate_roles_300(*_args_):
    
    
    role_ = get_role("administrator")
    if (not php_empty(lambda : role_)):
        role_.add_cap("update_core")
        role_.add_cap("list_users")
        role_.add_cap("remove_users")
        role_.add_cap("promote_users")
        role_.add_cap("edit_theme_options")
        role_.add_cap("delete_themes")
        role_.add_cap("export")
    # end if
# end def populate_roles_300
if (not php_function_exists("install_network")):
    #// 
    #// Install Network.
    #// 
    #// @since 3.0.0
    #//
    def install_network(*_args_):
        
        
        if (not php_defined("WP_INSTALLING_NETWORK")):
            php_define("WP_INSTALLING_NETWORK", True)
        # end if
        dbDelta(wp_get_db_schema("global"))
    # end def install_network
# end if
#// 
#// Populate network settings.
#// 
#// @since 3.0.0
#// 
#// @global wpdb       $wpdb         WordPress database abstraction object.
#// @global object     $current_site
#// @global WP_Rewrite $wp_rewrite   WordPress rewrite component.
#// 
#// @param int    $network_id        ID of network to populate.
#// @param string $domain            The domain name for the network (eg. "example.com").
#// @param string $email             Email address for the network administrator.
#// @param string $site_name         The name of the network.
#// @param string $path              Optional. The path to append to the network's domain name. Default '/'.
#// @param bool   $subdomain_install Optional. Whether the network is a subdomain installation or a subdirectory installation.
#// Default false, meaning the network is a subdirectory installation.
#// @return bool|WP_Error True on success, or WP_Error on warning (with the installation otherwise successful,
#// so the error code must be checked) or failure.
#//
def populate_network(network_id_=1, domain_="", email_="", site_name_="", path_="/", subdomain_install_=None, *_args_):
    if subdomain_install_ is None:
        subdomain_install_ = False
    # end if
    
    global wpdb_
    global current_site_
    global wp_rewrite_
    php_check_if_defined("wpdb_","current_site_","wp_rewrite_")
    errors_ = php_new_class("WP_Error", lambda : WP_Error())
    if "" == domain_:
        errors_.add("empty_domain", __("You must provide a domain name."))
    # end if
    if "" == site_name_:
        errors_.add("empty_sitename", __("You must provide a name for your network of sites."))
    # end if
    #// Check for network collision.
    network_exists_ = False
    if is_multisite():
        if get_network(php_int(network_id_)):
            errors_.add("siteid_exists", __("The network already exists."))
        # end if
    else:
        if network_id_ == wpdb_.get_var(wpdb_.prepare(str("SELECT id FROM ") + str(wpdb_.site) + str(" WHERE id = %d"), network_id_)):
            errors_.add("siteid_exists", __("The network already exists."))
        # end if
    # end if
    if (not is_email(email_)):
        errors_.add("invalid_email", __("You must provide a valid email address."))
    # end if
    if errors_.has_errors():
        return errors_
    # end if
    if 1 == network_id_:
        wpdb_.insert(wpdb_.site, Array({"domain": domain_, "path": path_}))
        network_id_ = wpdb_.insert_id
    else:
        wpdb_.insert(wpdb_.site, Array({"domain": domain_, "path": path_, "id": network_id_}))
    # end if
    populate_network_meta(network_id_, Array({"admin_email": email_, "site_name": site_name_, "subdomain_install": subdomain_install_}))
    site_user_ = get_userdata(php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT meta_value FROM ") + str(wpdb_.sitemeta) + str(" WHERE meta_key = %s AND site_id = %d"), "admin_user_id", network_id_))))
    #// 
    #// When upgrading from single to multisite, assume the current site will
    #// become the main site of the network. When using populate_network()
    #// to create another network in an existing multisite environment, skip
    #// these steps since the main site of the new network has not yet been
    #// created.
    #//
    if (not is_multisite()):
        current_site_ = php_new_class("stdClass", lambda : stdClass())
        current_site_.domain = domain_
        current_site_.path = path_
        current_site_.site_name = ucfirst(domain_)
        wpdb_.insert(wpdb_.blogs, Array({"site_id": network_id_, "blog_id": 1, "domain": domain_, "path": path_, "registered": current_time("mysql")}))
        current_site_.blog_id = wpdb_.insert_id
        update_user_meta(site_user_.ID, "source_domain", domain_)
        update_user_meta(site_user_.ID, "primary_blog", current_site_.blog_id)
        if subdomain_install_:
            wp_rewrite_.set_permalink_structure("/%year%/%monthnum%/%day%/%postname%/")
        else:
            wp_rewrite_.set_permalink_structure("/blog/%year%/%monthnum%/%day%/%postname%/")
        # end if
        flush_rewrite_rules()
        if (not subdomain_install_):
            return True
        # end if
        vhost_ok_ = False
        errstr_ = ""
        hostname_ = php_substr(php_md5(time()), 0, 6) + "." + domain_
        #// Very random hostname!
        page_ = wp_remote_get("http://" + hostname_, Array({"timeout": 5, "httpversion": "1.1"}))
        if is_wp_error(page_):
            errstr_ = page_.get_error_message()
        elif 200 == wp_remote_retrieve_response_code(page_):
            vhost_ok_ = True
        # end if
        if (not vhost_ok_):
            msg_ = "<p><strong>" + __("Warning! Wildcard DNS may not be configured correctly!") + "</strong></p>"
            msg_ += "<p>" + php_sprintf(__("The installer attempted to contact a random hostname (%s) on your domain."), "<code>" + hostname_ + "</code>")
            if (not php_empty(lambda : errstr_)):
                #// translators: %s: Error message.
                msg_ += " " + php_sprintf(__("This resulted in an error message: %s"), "<code>" + errstr_ + "</code>")
            # end if
            msg_ += "</p>"
            msg_ += "<p>" + php_sprintf(__("To use a subdomain configuration, you must have a wildcard entry in your DNS. This usually means adding a %s hostname record pointing at your web server in your DNS configuration tool."), "<code>*</code>") + "</p>"
            msg_ += "<p>" + __("You can still use your site but any subdomain you create may not be accessible. If you know your DNS is correct, ignore this message.") + "</p>"
            return php_new_class("WP_Error", lambda : WP_Error("no_wildcard_dns", msg_))
        # end if
    # end if
    return True
# end def populate_network
#// 
#// Creates WordPress network meta and sets the default values.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb          WordPress database abstraction object.
#// @global int  $wp_db_version WordPress database version.
#// 
#// @param int   $network_id Network ID to populate meta for.
#// @param array $meta       Optional. Custom meta $key => $value pairs to use. Default empty array.
#//
def populate_network_meta(network_id_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    global wpdb_
    global wp_db_version_
    php_check_if_defined("wpdb_","wp_db_version_")
    network_id_ = php_int(network_id_)
    email_ = meta_["admin_email"] if (not php_empty(lambda : meta_["admin_email"])) else ""
    subdomain_install_ = php_int(meta_["subdomain_install"]) if (php_isset(lambda : meta_["subdomain_install"])) else 0
    #// If a user with the provided email does not exist, default to the current user as the new network admin.
    site_user_ = get_user_by("email", email_) if (not php_empty(lambda : email_)) else False
    if False == site_user_:
        site_user_ = wp_get_current_user()
    # end if
    if php_empty(lambda : email_):
        email_ = site_user_.user_email
    # end if
    template_ = get_option("template")
    stylesheet_ = get_option("stylesheet")
    allowed_themes_ = Array({stylesheet_: True})
    if template_ != stylesheet_:
        allowed_themes_[template_] = True
    # end if
    if WP_DEFAULT_THEME != stylesheet_ and WP_DEFAULT_THEME != template_:
        allowed_themes_[WP_DEFAULT_THEME] = True
    # end if
    #// If WP_DEFAULT_THEME doesn't exist, also whitelist the latest core default theme.
    if (not wp_get_theme(WP_DEFAULT_THEME).exists()):
        core_default_ = WP_Theme.get_core_default_theme()
        if core_default_:
            allowed_themes_[core_default_.get_stylesheet()] = True
        # end if
    # end if
    if php_function_exists("clean_network_cache"):
        clean_network_cache(network_id_)
    else:
        wp_cache_delete(network_id_, "networks")
    # end if
    wp_cache_delete("networks_have_paths", "site-options")
    if (not is_multisite()):
        site_admins_ = Array(site_user_.user_login)
        users_ = get_users(Array({"fields": Array("user_login"), "role": "administrator"}))
        if users_:
            for user_ in users_:
                site_admins_[-1] = user_.user_login
            # end for
            site_admins_ = array_unique(site_admins_)
        # end if
    else:
        site_admins_ = get_site_option("site_admins")
    # end if
    #// translators: Do not translate USERNAME, SITE_NAME, BLOG_URL, PASSWORD: those are placeholders.
    welcome_email_ = __("""Howdy USERNAME,
    Your new SITE_NAME site has been successfully set up at:
    BLOG_URL
    You can log in to the administrator account with the following information:
    Username: USERNAME
    Password: PASSWORD
    Log in here: BLOG_URLwp-login.php
    We hope you enjoy your new site. Thanks!
    --The Team @ SITE_NAME""")
    misc_exts_ = Array("jpg", "jpeg", "png", "gif", "mov", "avi", "mpg", "3gp", "3g2", "midi", "mid", "pdf", "doc", "ppt", "odt", "pptx", "docx", "pps", "ppsx", "xls", "xlsx", "key")
    audio_exts_ = wp_get_audio_extensions()
    video_exts_ = wp_get_video_extensions()
    upload_filetypes_ = array_unique(php_array_merge(misc_exts_, audio_exts_, video_exts_))
    sitemeta_ = Array({"site_name": __("My Network"), "admin_email": email_, "admin_user_id": site_user_.ID, "registration": "none", "upload_filetypes": php_implode(" ", upload_filetypes_), "blog_upload_space": 100, "fileupload_maxk": 1500, "site_admins": site_admins_, "allowedthemes": allowed_themes_, "illegal_names": Array("www", "web", "root", "admin", "main", "invite", "administrator", "files"), "wpmu_upgrade_site": wp_db_version_, "welcome_email": welcome_email_, "first_post": __("Welcome to %s. This is your first post. Edit or delete it, then start writing!"), "siteurl": get_option("siteurl") + "/", "add_new_users": "0", "upload_space_check_disabled": get_site_option("upload_space_check_disabled") if is_multisite() else "1", "subdomain_install": subdomain_install_, "global_terms_enabled": "1" if global_terms_enabled() else "0", "ms_files_rewriting": get_site_option("ms_files_rewriting") if is_multisite() else "0", "initial_db_version": get_option("initial_db_version"), "active_sitewide_plugins": Array(), "WPLANG": get_locale()})
    if (not subdomain_install_):
        sitemeta_["illegal_names"][-1] = "blog"
    # end if
    sitemeta_ = wp_parse_args(meta_, sitemeta_)
    #// 
    #// Filters meta for a network on creation.
    #// 
    #// @since 3.7.0
    #// 
    #// @param array $sitemeta   Associative array of network meta keys and values to be inserted.
    #// @param int   $network_id ID of network to populate.
    #//
    sitemeta_ = apply_filters("populate_network_meta", sitemeta_, network_id_)
    insert_ = ""
    for meta_key_,meta_value_ in sitemeta_.items():
        if php_is_array(meta_value_):
            meta_value_ = serialize(meta_value_)
        # end if
        if (not php_empty(lambda : insert_)):
            insert_ += ", "
        # end if
        insert_ += wpdb_.prepare("( %d, %s, %s)", network_id_, meta_key_, meta_value_)
    # end for
    wpdb_.query(str("INSERT INTO ") + str(wpdb_.sitemeta) + str(" ( site_id, meta_key, meta_value ) VALUES ") + insert_)
    pass
# end def populate_network_meta
#// 
#// Creates WordPress site meta and sets the default values.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int   $site_id Site ID to populate meta for.
#// @param array $meta    Optional. Custom meta $key => $value pairs to use. Default empty array.
#//
def populate_site_meta(site_id_=None, meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    site_id_ = php_int(site_id_)
    if (not is_site_meta_supported()):
        return
    # end if
    if php_empty(lambda : meta_):
        return
    # end if
    #// 
    #// Filters meta for a site on creation.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $meta    Associative array of site meta keys and values to be inserted.
    #// @param int   $site_id ID of site to populate.
    #//
    site_meta_ = apply_filters("populate_site_meta", meta_, site_id_)
    insert_ = ""
    for meta_key_,meta_value_ in site_meta_.items():
        if php_is_array(meta_value_):
            meta_value_ = serialize(meta_value_)
        # end if
        if (not php_empty(lambda : insert_)):
            insert_ += ", "
        # end if
        insert_ += wpdb_.prepare("( %d, %s, %s)", site_id_, meta_key_, meta_value_)
    # end for
    wpdb_.query(str("INSERT INTO ") + str(wpdb_.blogmeta) + str(" ( blog_id, meta_key, meta_value ) VALUES ") + insert_)
    #// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
    wp_cache_delete(site_id_, "blog_meta")
    wp_cache_set_sites_last_changed()
# end def populate_site_meta
