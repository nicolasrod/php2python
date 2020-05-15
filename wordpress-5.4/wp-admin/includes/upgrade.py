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
#// WordPress Upgrade API
#// 
#// Most of the functions are pluggable and can be overwritten.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Include user installation customization script.
if php_file_exists(WP_CONTENT_DIR + "/install.php"):
    php_include_file(WP_CONTENT_DIR + "/install.php", once=False)
# end if
#// WordPress Administration API
php_include_file(ABSPATH + "wp-admin/includes/admin.php", once=True)
#// WordPress Schema API
php_include_file(ABSPATH + "wp-admin/includes/schema.php", once=True)
if (not php_function_exists("wp_install")):
    #// 
    #// Installs the site.
    #// 
    #// Runs the required functions to set up and populate the database,
    #// including primary admin user and initial options.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $blog_title    Site title.
    #// @param string $user_name     User's username.
    #// @param string $user_email    User's email.
    #// @param bool   $public        Whether site is public.
    #// @param string $deprecated    Optional. Not used.
    #// @param string $user_password Optional. User's chosen password. Default empty (random password).
    #// @param string $language      Optional. Language chosen. Default empty.
    #// @return array {
    #// Data for the newly installed site.
    #// 
    #// @type string $url              The URL of the site.
    #// @type int    $user_id          The ID of the site owner.
    #// @type string $password         The password of the site owner, if their user account didn't already exist.
    #// @type string $password_message The explanatory message regarding the password.
    #// }
    #//
    def wp_install(blog_title=None, user_name=None, user_email=None, public=None, deprecated="", user_password="", language="", *args_):
        
        if (not php_empty(lambda : deprecated)):
            _deprecated_argument(__FUNCTION__, "2.6.0")
        # end if
        wp_check_mysql_version()
        wp_cache_flush()
        make_db_current_silent()
        populate_options()
        populate_roles()
        update_option("blogname", blog_title)
        update_option("admin_email", user_email)
        update_option("blog_public", public)
        #// Freshness of site - in the future, this could get more specific about actions taken, perhaps.
        update_option("fresh_site", 1)
        if language:
            update_option("WPLANG", language)
        # end if
        guessurl = wp_guess_url()
        update_option("siteurl", guessurl)
        #// If not a public site, don't ping.
        if (not public):
            update_option("default_pingback_flag", 0)
        # end if
        #// 
        #// Create default user. If the user already exists, the user tables are
        #// being shared among sites. Just set the role in that case.
        #//
        user_id = username_exists(user_name)
        user_password = php_trim(user_password)
        email_password = False
        user_created = False
        if (not user_id) and php_empty(lambda : user_password):
            user_password = wp_generate_password(12, False)
            message = __("<strong><em>Note that password</em></strong> carefully! It is a <em>random</em> password that was generated just for you.")
            user_id = wp_create_user(user_name, user_password, user_email)
            update_user_option(user_id, "default_password_nag", True, True)
            email_password = True
            user_created = True
        elif (not user_id):
            #// Password has been provided.
            message = "<em>" + __("Your chosen password.") + "</em>"
            user_id = wp_create_user(user_name, user_password, user_email)
            user_created = True
        else:
            message = __("User already exists. Password inherited.")
        # end if
        user = php_new_class("WP_User", lambda : WP_User(user_id))
        user.set_role("administrator")
        if user_created:
            user.user_url = guessurl
            wp_update_user(user)
        # end if
        wp_install_defaults(user_id)
        wp_install_maybe_enable_pretty_permalinks()
        flush_rewrite_rules()
        wp_new_blog_notification(blog_title, guessurl, user_id, user_password if email_password else __("The password you chose during installation."))
        wp_cache_flush()
        #// 
        #// Fires after a site is fully installed.
        #// 
        #// @since 3.9.0
        #// 
        #// @param WP_User $user The site owner.
        #//
        do_action("wp_install", user)
        return Array({"url": guessurl, "user_id": user_id, "password": user_password, "password_message": message})
    # end def wp_install
# end if
if (not php_function_exists("wp_install_defaults")):
    #// 
    #// Creates the initial content for a newly-installed site.
    #// 
    #// Adds the default "Uncategorized" category, the first post (with comment),
    #// first page, and default widgets for default theme for the current version.
    #// 
    #// @since 2.1.0
    #// 
    #// @global wpdb       $wpdb         WordPress database abstraction object.
    #// @global WP_Rewrite $wp_rewrite   WordPress rewrite component.
    #// @global string     $table_prefix
    #// 
    #// @param int $user_id User ID.
    #//
    def wp_install_defaults(user_id=None, *args_):
        
        global wpdb,wp_rewrite,table_prefix
        php_check_if_defined("wpdb","wp_rewrite","table_prefix")
        #// Default category.
        cat_name = __("Uncategorized")
        #// translators: Default category slug.
        cat_slug = sanitize_title(_x("Uncategorized", "Default category slug"))
        if global_terms_enabled():
            cat_id = wpdb.get_var(wpdb.prepare(str("SELECT cat_ID FROM ") + str(wpdb.sitecategories) + str(" WHERE category_nicename = %s"), cat_slug))
            if None == cat_id:
                wpdb.insert(wpdb.sitecategories, Array({"cat_ID": 0, "cat_name": cat_name, "category_nicename": cat_slug, "last_updated": current_time("mysql", True)}))
                cat_id = wpdb.insert_id
            # end if
            update_option("default_category", cat_id)
        else:
            cat_id = 1
        # end if
        wpdb.insert(wpdb.terms, Array({"term_id": cat_id, "name": cat_name, "slug": cat_slug, "term_group": 0}))
        wpdb.insert(wpdb.term_taxonomy, Array({"term_id": cat_id, "taxonomy": "category", "description": "", "parent": 0, "count": 1}))
        cat_tt_id = wpdb.insert_id
        #// First post.
        now = current_time("mysql")
        now_gmt = current_time("mysql", 1)
        first_post_guid = get_option("home") + "/?p=1"
        if is_multisite():
            first_post = get_site_option("first_post")
            if (not first_post):
                first_post = "<!-- wp:paragraph -->\n<p>" + __("Welcome to %s. This is your first post. Edit or delete it, then start writing!") + "</p>\n<!-- /wp:paragraph -->"
            # end if
            first_post = php_sprintf(first_post, php_sprintf("<a href=\"%s\">%s</a>", esc_url(network_home_url()), get_network().site_name))
            #// Back-compat for pre-4.4.
            first_post = php_str_replace("SITE_URL", esc_url(network_home_url()), first_post)
            first_post = php_str_replace("SITE_NAME", get_network().site_name, first_post)
        else:
            first_post = "<!-- wp:paragraph -->\n<p>" + __("Welcome to WordPress. This is your first post. Edit or delete it, then start writing!") + "</p>\n<!-- /wp:paragraph -->"
        # end if
        wpdb.insert(wpdb.posts, Array({"post_author": user_id, "post_date": now, "post_date_gmt": now_gmt, "post_content": first_post, "post_excerpt": "", "post_title": __("Hello world!"), "post_name": sanitize_title(_x("hello-world", "Default post slug")), "post_modified": now, "post_modified_gmt": now_gmt, "guid": first_post_guid, "comment_count": 1, "to_ping": "", "pinged": "", "post_content_filtered": ""}))
        wpdb.insert(wpdb.term_relationships, Array({"term_taxonomy_id": cat_tt_id, "object_id": 1}))
        #// Default comment.
        if is_multisite():
            first_comment_author = get_site_option("first_comment_author")
            first_comment_email = get_site_option("first_comment_email")
            first_comment_url = get_site_option("first_comment_url", network_home_url())
            first_comment = get_site_option("first_comment")
        # end if
        first_comment_author = first_comment_author if (not php_empty(lambda : first_comment_author)) else __("A WordPress Commenter")
        first_comment_email = first_comment_email if (not php_empty(lambda : first_comment_email)) else "wapuu@wordpress.example"
        first_comment_url = first_comment_url if (not php_empty(lambda : first_comment_url)) else "https://wordpress.org/"
        first_comment = first_comment if (not php_empty(lambda : first_comment)) else __("Hi, this is a comment.\nTo get started with moderating, editing, and deleting comments, please visit the Comments screen in the dashboard.\nCommenter avatars come from <a href=\"https://gravatar.com\">Gravatar</a>.")
        wpdb.insert(wpdb.comments, Array({"comment_post_ID": 1, "comment_author": first_comment_author, "comment_author_email": first_comment_email, "comment_author_url": first_comment_url, "comment_date": now, "comment_date_gmt": now_gmt, "comment_content": first_comment}))
        #// First page.
        if is_multisite():
            first_page = get_site_option("first_page")
        # end if
        if php_empty(lambda : first_page):
            first_page = "<!-- wp:paragraph -->\n<p>"
            #// translators: First page content.
            first_page += __("This is an example page. It's different from a blog post because it will stay in one place and will show up in your site navigation (in most themes). Most people start with an About page that introduces them to potential site visitors. It might say something like this:")
            first_page += """</p>
            <!-- /wp:paragraph -->
            """
            first_page += "<!-- wp:quote -->\n<blockquote class=\"wp-block-quote\"><p>"
            #// translators: First page content.
            first_page += __("Hi there! I'm a bike messenger by day, aspiring actor by night, and this is my website. I live in Los Angeles, have a great dog named Jack, and I like pi&#241;a coladas. (And gettin' caught in the rain.)")
            first_page += """</p></blockquote>
            <!-- /wp:quote -->
            """
            first_page += "<!-- wp:paragraph -->\n<p>"
            #// translators: First page content.
            first_page += __("...or something like this:")
            first_page += """</p>
            <!-- /wp:paragraph -->
            """
            first_page += "<!-- wp:quote -->\n<blockquote class=\"wp-block-quote\"><p>"
            #// translators: First page content.
            first_page += __("The XYZ Doohickey Company was founded in 1971, and has been providing quality doohickeys to the public ever since. Located in Gotham City, XYZ employs over 2,000 people and does all kinds of awesome things for the Gotham community.")
            first_page += """</p></blockquote>
            <!-- /wp:quote -->
            """
            first_page += "<!-- wp:paragraph -->\n<p>"
            first_page += php_sprintf(__("As a new WordPress user, you should go to <a href=\"%s\">your dashboard</a> to delete this page and create new pages for your content. Have fun!"), admin_url())
            first_page += "</p>\n<!-- /wp:paragraph -->"
        # end if
        first_post_guid = get_option("home") + "/?page_id=2"
        wpdb.insert(wpdb.posts, Array({"post_author": user_id, "post_date": now, "post_date_gmt": now_gmt, "post_content": first_page, "post_excerpt": "", "comment_status": "closed", "post_title": __("Sample Page"), "post_name": __("sample-page"), "post_modified": now, "post_modified_gmt": now_gmt, "guid": first_post_guid, "post_type": "page", "to_ping": "", "pinged": "", "post_content_filtered": ""}))
        wpdb.insert(wpdb.postmeta, Array({"post_id": 2, "meta_key": "_wp_page_template", "meta_value": "default"}))
        #// Privacy Policy page.
        if is_multisite():
            #// Disable by default unless the suggested content is provided.
            privacy_policy_content = get_site_option("default_privacy_policy_content")
        else:
            if (not php_class_exists("WP_Privacy_Policy_Content")):
                php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-policy-content.php", once=False)
            # end if
            privacy_policy_content = WP_Privacy_Policy_Content.get_default_content()
        # end if
        if (not php_empty(lambda : privacy_policy_content)):
            privacy_policy_guid = get_option("home") + "/?page_id=3"
            wpdb.insert(wpdb.posts, Array({"post_author": user_id, "post_date": now, "post_date_gmt": now_gmt, "post_content": privacy_policy_content, "post_excerpt": "", "comment_status": "closed", "post_title": __("Privacy Policy"), "post_name": __("privacy-policy"), "post_modified": now, "post_modified_gmt": now_gmt, "guid": privacy_policy_guid, "post_type": "page", "post_status": "draft", "to_ping": "", "pinged": "", "post_content_filtered": ""}))
            wpdb.insert(wpdb.postmeta, Array({"post_id": 3, "meta_key": "_wp_page_template", "meta_value": "default"}))
            update_option("wp_page_for_privacy_policy", 3)
        # end if
        #// Set up default widgets for default theme.
        update_option("widget_search", Array({2: Array({"title": ""})}, {"_multiwidget": 1}))
        update_option("widget_recent-posts", Array({2: Array({"title": "", "number": 5})}, {"_multiwidget": 1}))
        update_option("widget_recent-comments", Array({2: Array({"title": "", "number": 5})}, {"_multiwidget": 1}))
        update_option("widget_archives", Array({2: Array({"title": "", "count": 0, "dropdown": 0})}, {"_multiwidget": 1}))
        update_option("widget_categories", Array({2: Array({"title": "", "count": 0, "hierarchical": 0, "dropdown": 0})}, {"_multiwidget": 1}))
        update_option("widget_meta", Array({2: Array({"title": ""})}, {"_multiwidget": 1}))
        update_option("sidebars_widgets", Array({"wp_inactive_widgets": Array(), "sidebar-1": Array({0: "search-2", 1: "recent-posts-2", 2: "recent-comments-2"})}, {"sidebar-2": Array({0: "archives-2", 1: "categories-2", 2: "meta-2"})}, {"array_version": 3}))
        if (not is_multisite()):
            update_user_meta(user_id, "show_welcome_panel", 1)
        elif (not is_super_admin(user_id)) and (not metadata_exists("user", user_id, "show_welcome_panel")):
            update_user_meta(user_id, "show_welcome_panel", 2)
        # end if
        if is_multisite():
            #// Flush rules to pick up the new page.
            wp_rewrite.init()
            wp_rewrite.flush_rules()
            user = php_new_class("WP_User", lambda : WP_User(user_id))
            wpdb.update(wpdb.options, Array({"option_value": user.user_email}), Array({"option_name": "admin_email"}))
            #// Remove all perms except for the login user.
            wpdb.query(wpdb.prepare(str("DELETE FROM ") + str(wpdb.usermeta) + str(" WHERE user_id != %d AND meta_key = %s"), user_id, table_prefix + "user_level"))
            wpdb.query(wpdb.prepare(str("DELETE FROM ") + str(wpdb.usermeta) + str(" WHERE user_id != %d AND meta_key = %s"), user_id, table_prefix + "capabilities"))
            #// Delete any caps that snuck into the previously active blog. (Hardcoded to blog 1 for now.)
            #// TODO: Get previous_blog_id.
            if (not is_super_admin(user_id)) and 1 != user_id:
                wpdb.delete(wpdb.usermeta, Array({"user_id": user_id, "meta_key": wpdb.base_prefix + "1_capabilities"}))
            # end if
        # end if
    # end def wp_install_defaults
# end if
#// 
#// Maybe enable pretty permalinks on installation.
#// 
#// If after enabling pretty permalinks don't work, fallback to query-string permalinks.
#// 
#// @since 4.2.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @return bool Whether pretty permalinks are enabled. False otherwise.
#//
def wp_install_maybe_enable_pretty_permalinks(*args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    #// Bail if a permalink structure is already enabled.
    if get_option("permalink_structure"):
        return True
    # end if
    #// 
    #// The Permalink structures to attempt.
    #// 
    #// The first is designed for mod_rewrite or nginx rewriting.
    #// 
    #// The second is PATHINFO-based permalinks for web server configurations
    #// without a true rewrite module enabled.
    #//
    permalink_structures = Array("/%year%/%monthnum%/%day%/%postname%/", "/index.php/%year%/%monthnum%/%day%/%postname%/")
    for permalink_structure in permalink_structures:
        wp_rewrite.set_permalink_structure(permalink_structure)
        #// 
        #// Flush rules with the hard option to force refresh of the web-server's
        #// rewrite config file (e.g. .htaccess or web.config).
        #//
        wp_rewrite.flush_rules(True)
        test_url = ""
        #// Test against a real WordPress post.
        first_post = get_page_by_path(sanitize_title(_x("hello-world", "Default post slug")), OBJECT, "post")
        if first_post:
            test_url = get_permalink(first_post.ID)
        # end if
        #// 
        #// Send a request to the site, and check whether
        #// the 'x-pingback' header is returned as expected.
        #// 
        #// Uses wp_remote_get() instead of wp_remote_head() because web servers
        #// can block head requests.
        #//
        response = wp_remote_get(test_url, Array({"timeout": 5}))
        x_pingback_header = wp_remote_retrieve_header(response, "x-pingback")
        pretty_permalinks = x_pingback_header and get_bloginfo("pingback_url") == x_pingback_header
        if pretty_permalinks:
            return True
        # end if
    # end for
    #// 
    #// If it makes it this far, pretty permalinks failed.
    #// Fallback to query-string permalinks.
    #//
    wp_rewrite.set_permalink_structure("")
    wp_rewrite.flush_rules(True)
    return False
# end def wp_install_maybe_enable_pretty_permalinks
if (not php_function_exists("wp_new_blog_notification")):
    #// 
    #// Notifies the site admin that the setup is complete.
    #// 
    #// Sends an email with wp_mail to the new administrator that the site setup is complete,
    #// and provides them with a record of their login credentials.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $blog_title Site title.
    #// @param string $blog_url   Site url.
    #// @param int    $user_id    User ID.
    #// @param string $password   User's Password.
    #//
    def wp_new_blog_notification(blog_title=None, blog_url=None, user_id=None, password=None, *args_):
        
        user = php_new_class("WP_User", lambda : WP_User(user_id))
        email = user.user_email
        name = user.user_login
        login_url = wp_login_url()
        message = php_sprintf(__("""Your new WordPress site has been successfully set up at:
        %1$s
        You can log in to the administrator account with the following information:
        Username: %2$s
        Password: %3$s
        Log in here: %4$s
        We hope you enjoy your new site. Thanks!
        --The WordPress Team
        https://wordpress.org/
        """), blog_url, name, password, login_url)
        wp_mail(email, __("New WordPress Site"), message)
    # end def wp_new_blog_notification
# end if
if (not php_function_exists("wp_upgrade")):
    #// 
    #// Runs WordPress Upgrade functions.
    #// 
    #// Upgrades the database if needed during a site update.
    #// 
    #// @since 2.1.0
    #// 
    #// @global int  $wp_current_db_version The old (current) database version.
    #// @global int  $wp_db_version         The new database version.
    #// @global wpdb $wpdb                  WordPress database abstraction object.
    #//
    def wp_upgrade(*args_):
        
        global wp_current_db_version,wp_db_version,wpdb
        php_check_if_defined("wp_current_db_version","wp_db_version","wpdb")
        wp_current_db_version = __get_option("db_version")
        #// We are up to date. Nothing to do.
        if wp_db_version == wp_current_db_version:
            return
        # end if
        if (not is_blog_installed()):
            return
        # end if
        wp_check_mysql_version()
        wp_cache_flush()
        pre_schema_upgrade()
        make_db_current_silent()
        upgrade_all()
        if is_multisite() and is_main_site():
            upgrade_network()
        # end if
        wp_cache_flush()
        if is_multisite():
            update_site_meta(get_current_blog_id(), "db_version", wp_db_version)
            update_site_meta(get_current_blog_id(), "db_last_updated", php_microtime())
        # end if
        #// 
        #// Fires after a site is fully upgraded.
        #// 
        #// @since 3.9.0
        #// 
        #// @param int $wp_db_version         The new $wp_db_version.
        #// @param int $wp_current_db_version The old (current) $wp_db_version.
        #//
        do_action("wp_upgrade", wp_db_version, wp_current_db_version)
    # end def wp_upgrade
# end if
#// 
#// Functions to be called in installation and upgrade scripts.
#// 
#// Contains conditional checks to determine which upgrade scripts to run,
#// based on database version and WP version being updated-to.
#// 
#// @ignore
#// @since 1.0.1
#// 
#// @global int $wp_current_db_version The old (current) database version.
#// @global int $wp_db_version         The new database version.
#//
def upgrade_all(*args_):
    
    global wp_current_db_version,wp_db_version
    php_check_if_defined("wp_current_db_version","wp_db_version")
    wp_current_db_version = __get_option("db_version")
    #// We are up to date. Nothing to do.
    if wp_db_version == wp_current_db_version:
        return
    # end if
    #// If the version is not set in the DB, try to guess the version.
    if php_empty(lambda : wp_current_db_version):
        wp_current_db_version = 0
        #// If the template option exists, we have 1.5.
        template = __get_option("template")
        if (not php_empty(lambda : template)):
            wp_current_db_version = 2541
        # end if
    # end if
    if wp_current_db_version < 6039:
        upgrade_230_options_table()
    # end if
    populate_options()
    if wp_current_db_version < 2541:
        upgrade_100()
        upgrade_101()
        upgrade_110()
        upgrade_130()
    # end if
    if wp_current_db_version < 3308:
        upgrade_160()
    # end if
    if wp_current_db_version < 4772:
        upgrade_210()
    # end if
    if wp_current_db_version < 4351:
        upgrade_old_slugs()
    # end if
    if wp_current_db_version < 5539:
        upgrade_230()
    # end if
    if wp_current_db_version < 6124:
        upgrade_230_old_tables()
    # end if
    if wp_current_db_version < 7499:
        upgrade_250()
    # end if
    if wp_current_db_version < 7935:
        upgrade_252()
    # end if
    if wp_current_db_version < 8201:
        upgrade_260()
    # end if
    if wp_current_db_version < 8989:
        upgrade_270()
    # end if
    if wp_current_db_version < 10360:
        upgrade_280()
    # end if
    if wp_current_db_version < 11958:
        upgrade_290()
    # end if
    if wp_current_db_version < 15260:
        upgrade_300()
    # end if
    if wp_current_db_version < 19389:
        upgrade_330()
    # end if
    if wp_current_db_version < 20080:
        upgrade_340()
    # end if
    if wp_current_db_version < 22422:
        upgrade_350()
    # end if
    if wp_current_db_version < 25824:
        upgrade_370()
    # end if
    if wp_current_db_version < 26148:
        upgrade_372()
    # end if
    if wp_current_db_version < 26691:
        upgrade_380()
    # end if
    if wp_current_db_version < 29630:
        upgrade_400()
    # end if
    if wp_current_db_version < 33055:
        upgrade_430()
    # end if
    if wp_current_db_version < 33056:
        upgrade_431()
    # end if
    if wp_current_db_version < 35700:
        upgrade_440()
    # end if
    if wp_current_db_version < 36686:
        upgrade_450()
    # end if
    if wp_current_db_version < 37965:
        upgrade_460()
    # end if
    if wp_current_db_version < 44719:
        upgrade_510()
    # end if
    if wp_current_db_version < 45744:
        upgrade_530()
    # end if
    maybe_disable_link_manager()
    maybe_disable_automattic_widgets()
    update_option("db_version", wp_db_version)
    update_option("db_upgraded", True)
# end def upgrade_all
#// 
#// Execute changes made in WordPress 1.0.
#// 
#// @ignore
#// @since 1.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_100(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Get the title and ID of every post, post_name to check if it already has a value.
    posts = wpdb.get_results(str("SELECT ID, post_title, post_name FROM ") + str(wpdb.posts) + str(" WHERE post_name = ''"))
    if posts:
        for post in posts:
            if "" == post.post_name:
                newtitle = sanitize_title(post.post_title)
                wpdb.query(wpdb.prepare(str("UPDATE ") + str(wpdb.posts) + str(" SET post_name = %s WHERE ID = %d"), newtitle, post.ID))
            # end if
        # end for
    # end if
    categories = wpdb.get_results(str("SELECT cat_ID, cat_name, category_nicename FROM ") + str(wpdb.categories))
    for category in categories:
        if "" == category.category_nicename:
            newtitle = sanitize_title(category.cat_name)
            wpdb.update(wpdb.categories, Array({"category_nicename": newtitle}), Array({"cat_ID": category.cat_ID}))
        # end if
    # end for
    sql = str("UPDATE ") + str(wpdb.options) + str("""\n        SET option_value = REPLACE(option_value, 'wp-links/links-images/', 'wp-images/links/')\n        WHERE option_name LIKE %s\n     AND option_value LIKE %s""")
    wpdb.query(wpdb.prepare(sql, wpdb.esc_like("links_rating_image") + "%", wpdb.esc_like("wp-links/links-images/") + "%"))
    done_ids = wpdb.get_results(str("SELECT DISTINCT post_id FROM ") + str(wpdb.post2cat))
    if done_ids:
        done_posts = Array()
        for done_id in done_ids:
            done_posts[-1] = done_id.post_id
        # end for
        catwhere = " AND ID NOT IN (" + php_implode(",", done_posts) + ")"
    else:
        catwhere = ""
    # end if
    allposts = wpdb.get_results(str("SELECT ID, post_category FROM ") + str(wpdb.posts) + str(" WHERE post_category != '0' ") + str(catwhere))
    if allposts:
        for post in allposts:
            #// Check to see if it's already been imported.
            cat = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.post2cat) + str(" WHERE post_id = %d AND category_id = %d"), post.ID, post.post_category))
            if (not cat) and 0 != post.post_category:
                #// If there's no result.
                wpdb.insert(wpdb.post2cat, Array({"post_id": post.ID, "category_id": post.post_category}))
            # end if
        # end for
    # end if
# end def upgrade_100
#// 
#// Execute changes made in WordPress 1.0.1.
#// 
#// @ignore
#// @since 1.0.1
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_101(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Clean up indices, add a few.
    add_clean_index(wpdb.posts, "post_name")
    add_clean_index(wpdb.posts, "post_status")
    add_clean_index(wpdb.categories, "category_nicename")
    add_clean_index(wpdb.comments, "comment_approved")
    add_clean_index(wpdb.comments, "comment_post_ID")
    add_clean_index(wpdb.links, "link_category")
    add_clean_index(wpdb.links, "link_visible")
# end def upgrade_101
#// 
#// Execute changes made in WordPress 1.2.
#// 
#// @ignore
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_110(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Set user_nicename.
    users = wpdb.get_results(str("SELECT ID, user_nickname, user_nicename FROM ") + str(wpdb.users))
    for user in users:
        if "" == user.user_nicename:
            newname = sanitize_title(user.user_nickname)
            wpdb.update(wpdb.users, Array({"user_nicename": newname}), Array({"ID": user.ID}))
        # end if
    # end for
    users = wpdb.get_results(str("SELECT ID, user_pass from ") + str(wpdb.users))
    for row in users:
        if (not php_preg_match("/^[A-Fa-f0-9]{32}$/", row.user_pass)):
            wpdb.update(wpdb.users, Array({"user_pass": php_md5(row.user_pass)}), Array({"ID": row.ID}))
        # end if
    # end for
    #// Get the GMT offset, we'll use that later on.
    all_options = get_alloptions_110()
    time_difference = all_options.time_difference
    server_time = time() + gmdate("Z")
    weblogger_time = server_time + time_difference * HOUR_IN_SECONDS
    gmt_time = time()
    diff_gmt_server = gmt_time - server_time / HOUR_IN_SECONDS
    diff_weblogger_server = weblogger_time - server_time / HOUR_IN_SECONDS
    diff_gmt_weblogger = diff_gmt_server - diff_weblogger_server
    gmt_offset = -diff_gmt_weblogger
    #// Add a gmt_offset option, with value $gmt_offset.
    add_option("gmt_offset", gmt_offset)
    #// 
    #// Check if we already set the GMT fields. If we did, then
    #// MAX(post_date_gmt) can't be '0000-00-00 00:00:00'.
    #// <michel_v> I just slapped myself silly for not thinking about it earlier.
    #//
    got_gmt_fields = (not wpdb.get_var(str("SELECT MAX(post_date_gmt) FROM ") + str(wpdb.posts)) == "0000-00-00 00:00:00")
    if (not got_gmt_fields):
        #// Add or subtract time to all dates, to get GMT dates.
        add_hours = php_intval(diff_gmt_weblogger)
        add_minutes = php_intval(60 * diff_gmt_weblogger - add_hours)
        wpdb.query(str("UPDATE ") + str(wpdb.posts) + str(" SET post_date_gmt = DATE_ADD(post_date, INTERVAL '") + str(add_hours) + str(":") + str(add_minutes) + str("' HOUR_MINUTE)"))
        wpdb.query(str("UPDATE ") + str(wpdb.posts) + str(" SET post_modified = post_date"))
        wpdb.query(str("UPDATE ") + str(wpdb.posts) + str(" SET post_modified_gmt = DATE_ADD(post_modified, INTERVAL '") + str(add_hours) + str(":") + str(add_minutes) + str("' HOUR_MINUTE) WHERE post_modified != '0000-00-00 00:00:00'"))
        wpdb.query(str("UPDATE ") + str(wpdb.comments) + str(" SET comment_date_gmt = DATE_ADD(comment_date, INTERVAL '") + str(add_hours) + str(":") + str(add_minutes) + str("' HOUR_MINUTE)"))
        wpdb.query(str("UPDATE ") + str(wpdb.users) + str(" SET user_registered = DATE_ADD(user_registered, INTERVAL '") + str(add_hours) + str(":") + str(add_minutes) + str("' HOUR_MINUTE)"))
    # end if
# end def upgrade_110
#// 
#// Execute changes made in WordPress 1.5.
#// 
#// @ignore
#// @since 1.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_130(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// Remove extraneous backslashes.
    posts = wpdb.get_results(str("SELECT ID, post_title, post_content, post_excerpt, guid, post_date, post_name, post_status, post_author FROM ") + str(wpdb.posts))
    if posts:
        for post in posts:
            post_content = addslashes(deslash(post.post_content))
            post_title = addslashes(deslash(post.post_title))
            post_excerpt = addslashes(deslash(post.post_excerpt))
            if php_empty(lambda : post.guid):
                guid = get_permalink(post.ID)
            else:
                guid = post.guid
            # end if
            wpdb.update(wpdb.posts, compact("post_title", "post_content", "post_excerpt", "guid"), Array({"ID": post.ID}))
        # end for
    # end if
    #// Remove extraneous backslashes.
    comments = wpdb.get_results(str("SELECT comment_ID, comment_author, comment_content FROM ") + str(wpdb.comments))
    if comments:
        for comment in comments:
            comment_content = deslash(comment.comment_content)
            comment_author = deslash(comment.comment_author)
            wpdb.update(wpdb.comments, compact("comment_content", "comment_author"), Array({"comment_ID": comment.comment_ID}))
        # end for
    # end if
    #// Remove extraneous backslashes.
    links = wpdb.get_results(str("SELECT link_id, link_name, link_description FROM ") + str(wpdb.links))
    if links:
        for link in links:
            link_name = deslash(link.link_name)
            link_description = deslash(link.link_description)
            wpdb.update(wpdb.links, compact("link_name", "link_description"), Array({"link_id": link.link_id}))
        # end for
    # end if
    active_plugins = __get_option("active_plugins")
    #// 
    #// If plugins are not stored in an array, they're stored in the old
    #// newline separated format. Convert to new format.
    #//
    if (not php_is_array(active_plugins)):
        active_plugins = php_explode("\n", php_trim(active_plugins))
        update_option("active_plugins", active_plugins)
    # end if
    #// Obsolete tables.
    wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "optionvalues")
    wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "optiontypes")
    wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "optiongroups")
    wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "optiongroup_options")
    #// Update comments table to use comment_type.
    wpdb.query(str("UPDATE ") + str(wpdb.comments) + str(" SET comment_type='trackback', comment_content = REPLACE(comment_content, '<trackback />', '') WHERE comment_content LIKE '<trackback />%'"))
    wpdb.query(str("UPDATE ") + str(wpdb.comments) + str(" SET comment_type='pingback', comment_content = REPLACE(comment_content, '<pingback />', '') WHERE comment_content LIKE '<pingback />%'"))
    #// Some versions have multiple duplicate option_name rows with the same values.
    options = wpdb.get_results(str("SELECT option_name, COUNT(option_name) AS dupes FROM `") + str(wpdb.options) + str("` GROUP BY option_name"))
    for option in options:
        if 1 != option.dupes:
            #// Could this be done in the query?
            limit = option.dupes - 1
            dupe_ids = wpdb.get_col(wpdb.prepare(str("SELECT option_id FROM ") + str(wpdb.options) + str(" WHERE option_name = %s LIMIT %d"), option.option_name, limit))
            if dupe_ids:
                dupe_ids = join(",", dupe_ids)
                wpdb.query(str("DELETE FROM ") + str(wpdb.options) + str(" WHERE option_id IN (") + str(dupe_ids) + str(")"))
            # end if
        # end if
    # end for
    make_site_theme()
# end def upgrade_130
#// 
#// Execute changes made in WordPress 2.0.
#// 
#// @ignore
#// @since 2.0.0
#// 
#// @global wpdb $wpdb                  WordPress database abstraction object.
#// @global int  $wp_current_db_version The old (current) database version.
#//
def upgrade_160(*args_):
    
    global wpdb,wp_current_db_version
    php_check_if_defined("wpdb","wp_current_db_version")
    populate_roles_160()
    users = wpdb.get_results(str("SELECT * FROM ") + str(wpdb.users))
    for user in users:
        if (not php_empty(lambda : user.user_firstname)):
            update_user_meta(user.ID, "first_name", wp_slash(user.user_firstname))
        # end if
        if (not php_empty(lambda : user.user_lastname)):
            update_user_meta(user.ID, "last_name", wp_slash(user.user_lastname))
        # end if
        if (not php_empty(lambda : user.user_nickname)):
            update_user_meta(user.ID, "nickname", wp_slash(user.user_nickname))
        # end if
        if (not php_empty(lambda : user.user_level)):
            update_user_meta(user.ID, wpdb.prefix + "user_level", user.user_level)
        # end if
        if (not php_empty(lambda : user.user_icq)):
            update_user_meta(user.ID, "icq", wp_slash(user.user_icq))
        # end if
        if (not php_empty(lambda : user.user_aim)):
            update_user_meta(user.ID, "aim", wp_slash(user.user_aim))
        # end if
        if (not php_empty(lambda : user.user_msn)):
            update_user_meta(user.ID, "msn", wp_slash(user.user_msn))
        # end if
        if (not php_empty(lambda : user.user_yim)):
            update_user_meta(user.ID, "yim", wp_slash(user.user_icq))
        # end if
        if (not php_empty(lambda : user.user_description)):
            update_user_meta(user.ID, "description", wp_slash(user.user_description))
        # end if
        if (php_isset(lambda : user.user_idmode)):
            idmode = user.user_idmode
            if "nickname" == idmode:
                id = user.user_nickname
            # end if
            if "login" == idmode:
                id = user.user_login
            # end if
            if "firstname" == idmode:
                id = user.user_firstname
            # end if
            if "lastname" == idmode:
                id = user.user_lastname
            # end if
            if "namefl" == idmode:
                id = user.user_firstname + " " + user.user_lastname
            # end if
            if "namelf" == idmode:
                id = user.user_lastname + " " + user.user_firstname
            # end if
            if (not idmode):
                id = user.user_nickname
            # end if
            wpdb.update(wpdb.users, Array({"display_name": id}), Array({"ID": user.ID}))
        # end if
        #// FIXME: RESET_CAPS is temporary code to reset roles and caps if flag is set.
        caps = get_user_meta(user.ID, wpdb.prefix + "capabilities")
        if php_empty(lambda : caps) or php_defined("RESET_CAPS"):
            level = get_user_meta(user.ID, wpdb.prefix + "user_level", True)
            role = translate_level_to_role(level)
            update_user_meta(user.ID, wpdb.prefix + "capabilities", Array({role: True}))
        # end if
    # end for
    old_user_fields = Array("user_firstname", "user_lastname", "user_icq", "user_aim", "user_msn", "user_yim", "user_idmode", "user_ip", "user_domain", "user_browser", "user_description", "user_nickname", "user_level")
    wpdb.hide_errors()
    for old in old_user_fields:
        wpdb.query(str("ALTER TABLE ") + str(wpdb.users) + str(" DROP ") + str(old))
    # end for
    wpdb.show_errors()
    #// Populate comment_count field of posts table.
    comments = wpdb.get_results(str("SELECT comment_post_ID, COUNT(*) as c FROM ") + str(wpdb.comments) + str(" WHERE comment_approved = '1' GROUP BY comment_post_ID"))
    if php_is_array(comments):
        for comment in comments:
            wpdb.update(wpdb.posts, Array({"comment_count": comment.c}), Array({"ID": comment.comment_post_ID}))
        # end for
    # end if
    #// 
    #// Some alpha versions used a post status of object instead of attachment
    #// and put the mime type in post_type instead of post_mime_type.
    #//
    if wp_current_db_version > 2541 and wp_current_db_version <= 3091:
        objects = wpdb.get_results(str("SELECT ID, post_type FROM ") + str(wpdb.posts) + str(" WHERE post_status = 'object'"))
        for object in objects:
            wpdb.update(wpdb.posts, Array({"post_status": "attachment", "post_mime_type": object.post_type, "post_type": ""}), Array({"ID": object.ID}))
            meta = get_post_meta(object.ID, "imagedata", True)
            if (not php_empty(lambda : meta["file"])):
                update_attached_file(object.ID, meta["file"])
            # end if
        # end for
    # end if
# end def upgrade_160
#// 
#// Execute changes made in WordPress 2.1.
#// 
#// @ignore
#// @since 2.1.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_210(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 3506:
        #// Update status and type.
        posts = wpdb.get_results(str("SELECT ID, post_status FROM ") + str(wpdb.posts))
        if (not php_empty(lambda : posts)):
            for post in posts:
                status = post.post_status
                type = "post"
                if "static" == status:
                    status = "publish"
                    type = "page"
                elif "attachment" == status:
                    status = "inherit"
                    type = "attachment"
                # end if
                wpdb.query(wpdb.prepare(str("UPDATE ") + str(wpdb.posts) + str(" SET post_status = %s, post_type = %s WHERE ID = %d"), status, type, post.ID))
            # end for
        # end if
    # end if
    if wp_current_db_version < 3845:
        populate_roles_210()
    # end if
    if wp_current_db_version < 3531:
        #// Give future posts a post_status of future.
        now = gmdate("Y-m-d H:i:59")
        wpdb.query(str("UPDATE ") + str(wpdb.posts) + str(" SET post_status = 'future' WHERE post_status = 'publish' AND post_date_gmt > '") + str(now) + str("'"))
        posts = wpdb.get_results(str("SELECT ID, post_date FROM ") + str(wpdb.posts) + str(" WHERE post_status ='future'"))
        if (not php_empty(lambda : posts)):
            for post in posts:
                wp_schedule_single_event(mysql2date("U", post.post_date, False), "publish_future_post", Array(post.ID))
            # end for
        # end if
    # end if
# end def upgrade_210
#// 
#// Execute changes made in WordPress 2.3.
#// 
#// @ignore
#// @since 2.3.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_230(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 5200:
        populate_roles_230()
    # end if
    #// Convert categories to terms.
    tt_ids = Array()
    have_tags = False
    categories = wpdb.get_results(str("SELECT * FROM ") + str(wpdb.categories) + str(" ORDER BY cat_ID"))
    for category in categories:
        term_id = int(category.cat_ID)
        name = category.cat_name
        description = category.category_description
        slug = category.category_nicename
        parent = category.category_parent
        term_group = 0
        #// Associate terms with the same slug in a term group and make slugs unique.
        exists = wpdb.get_results(wpdb.prepare(str("SELECT term_id, term_group FROM ") + str(wpdb.terms) + str(" WHERE slug = %s"), slug))
        if exists:
            term_group = exists[0].term_group
            id = exists[0].term_id
            num = 2
            while True:
                alt_slug = slug + str("-") + str(num)
                num += 1
                slug_check = wpdb.get_var(wpdb.prepare(str("SELECT slug FROM ") + str(wpdb.terms) + str(" WHERE slug = %s"), alt_slug))
                
                if slug_check:
                    break
                # end if
            # end while
            slug = alt_slug
            if php_empty(lambda : term_group):
                term_group = wpdb.get_var(str("SELECT MAX(term_group) FROM ") + str(wpdb.terms) + str(" GROUP BY term_group")) + 1
                wpdb.query(wpdb.prepare(str("UPDATE ") + str(wpdb.terms) + str(" SET term_group = %d WHERE term_id = %d"), term_group, id))
            # end if
        # end if
        wpdb.query(wpdb.prepare(str("INSERT INTO ") + str(wpdb.terms) + str(" (term_id, name, slug, term_group) VALUES\n        (%d, %s, %s, %d)"), term_id, name, slug, term_group))
        count = 0
        if (not php_empty(lambda : category.category_count)):
            count = int(category.category_count)
            taxonomy = "category"
            wpdb.query(wpdb.prepare(str("INSERT INTO ") + str(wpdb.term_taxonomy) + str(" (term_id, taxonomy, description, parent, count) VALUES ( %d, %s, %s, %d, %d)"), term_id, taxonomy, description, parent, count))
            tt_ids[term_id][taxonomy] = int(wpdb.insert_id)
        # end if
        if (not php_empty(lambda : category.link_count)):
            count = int(category.link_count)
            taxonomy = "link_category"
            wpdb.query(wpdb.prepare(str("INSERT INTO ") + str(wpdb.term_taxonomy) + str(" (term_id, taxonomy, description, parent, count) VALUES ( %d, %s, %s, %d, %d)"), term_id, taxonomy, description, parent, count))
            tt_ids[term_id][taxonomy] = int(wpdb.insert_id)
        # end if
        if (not php_empty(lambda : category.tag_count)):
            have_tags = True
            count = int(category.tag_count)
            taxonomy = "post_tag"
            wpdb.insert(wpdb.term_taxonomy, compact("term_id", "taxonomy", "description", "parent", "count"))
            tt_ids[term_id][taxonomy] = int(wpdb.insert_id)
        # end if
        if php_empty(lambda : count):
            count = 0
            taxonomy = "category"
            wpdb.insert(wpdb.term_taxonomy, compact("term_id", "taxonomy", "description", "parent", "count"))
            tt_ids[term_id][taxonomy] = int(wpdb.insert_id)
        # end if
    # end for
    select = "post_id, category_id"
    if have_tags:
        select += ", rel_type"
    # end if
    posts = wpdb.get_results(str("SELECT ") + str(select) + str(" FROM ") + str(wpdb.post2cat) + str(" GROUP BY post_id, category_id"))
    for post in posts:
        post_id = int(post.post_id)
        term_id = int(post.category_id)
        taxonomy = "category"
        if (not php_empty(lambda : post.rel_type)) and "tag" == post.rel_type:
            taxonomy = "tag"
        # end if
        tt_id = tt_ids[term_id][taxonomy]
        if php_empty(lambda : tt_id):
            continue
        # end if
        wpdb.insert(wpdb.term_relationships, Array({"object_id": post_id, "term_taxonomy_id": tt_id}))
    # end for
    #// < 3570 we used linkcategories. >= 3570 we used categories and link2cat.
    if wp_current_db_version < 3570:
        #// 
        #// Create link_category terms for link categories. Create a map of link
        #// category IDs to link_category terms.
        #//
        link_cat_id_map = Array()
        default_link_cat = 0
        tt_ids = Array()
        link_cats = wpdb.get_results("SELECT cat_id, cat_name FROM " + wpdb.prefix + "linkcategories")
        for category in link_cats:
            cat_id = int(category.cat_id)
            term_id = 0
            name = wp_slash(category.cat_name)
            slug = sanitize_title(name)
            term_group = 0
            #// Associate terms with the same slug in a term group and make slugs unique.
            exists = wpdb.get_results(wpdb.prepare(str("SELECT term_id, term_group FROM ") + str(wpdb.terms) + str(" WHERE slug = %s"), slug))
            if exists:
                term_group = exists[0].term_group
                term_id = exists[0].term_id
            # end if
            if php_empty(lambda : term_id):
                wpdb.insert(wpdb.terms, compact("name", "slug", "term_group"))
                term_id = int(wpdb.insert_id)
            # end if
            link_cat_id_map[cat_id] = term_id
            default_link_cat = term_id
            wpdb.insert(wpdb.term_taxonomy, Array({"term_id": term_id, "taxonomy": "link_category", "description": "", "parent": 0, "count": 0}))
            tt_ids[term_id] = int(wpdb.insert_id)
        # end for
        #// Associate links to categories.
        links = wpdb.get_results(str("SELECT link_id, link_category FROM ") + str(wpdb.links))
        if (not php_empty(lambda : links)):
            for link in links:
                if 0 == link.link_category:
                    continue
                # end if
                if (not (php_isset(lambda : link_cat_id_map[link.link_category]))):
                    continue
                # end if
                term_id = link_cat_id_map[link.link_category]
                tt_id = tt_ids[term_id]
                if php_empty(lambda : tt_id):
                    continue
                # end if
                wpdb.insert(wpdb.term_relationships, Array({"object_id": link.link_id, "term_taxonomy_id": tt_id}))
            # end for
        # end if
        #// Set default to the last category we grabbed during the upgrade loop.
        update_option("default_link_category", default_link_cat)
    else:
        links = wpdb.get_results(str("SELECT link_id, category_id FROM ") + str(wpdb.link2cat) + str(" GROUP BY link_id, category_id"))
        for link in links:
            link_id = int(link.link_id)
            term_id = int(link.category_id)
            taxonomy = "link_category"
            tt_id = tt_ids[term_id][taxonomy]
            if php_empty(lambda : tt_id):
                continue
            # end if
            wpdb.insert(wpdb.term_relationships, Array({"object_id": link_id, "term_taxonomy_id": tt_id}))
        # end for
    # end if
    if wp_current_db_version < 4772:
        #// Obsolete linkcategories table.
        wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "linkcategories")
    # end if
    #// Recalculate all counts.
    terms = wpdb.get_results(str("SELECT term_taxonomy_id, taxonomy FROM ") + str(wpdb.term_taxonomy))
    for term in terms:
        if "post_tag" == term.taxonomy or "category" == term.taxonomy:
            count = wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_relationships) + str(", ") + str(wpdb.posts) + str(" WHERE ") + str(wpdb.posts) + str(".ID = ") + str(wpdb.term_relationships) + str(".object_id AND post_status = 'publish' AND post_type = 'post' AND term_taxonomy_id = %d"), term.term_taxonomy_id))
        else:
            count = wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_relationships) + str(" WHERE term_taxonomy_id = %d"), term.term_taxonomy_id))
        # end if
        wpdb.update(wpdb.term_taxonomy, Array({"count": count}), Array({"term_taxonomy_id": term.term_taxonomy_id}))
    # end for
# end def upgrade_230
#// 
#// Remove old options from the database.
#// 
#// @ignore
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_230_options_table(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    old_options_fields = Array("option_can_override", "option_type", "option_width", "option_height", "option_description", "option_admin_level")
    wpdb.hide_errors()
    for old in old_options_fields:
        wpdb.query(str("ALTER TABLE ") + str(wpdb.options) + str(" DROP ") + str(old))
    # end for
    wpdb.show_errors()
# end def upgrade_230_options_table
#// 
#// Remove old categories, link2cat, and post2cat database tables.
#// 
#// @ignore
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_230_old_tables(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "categories")
    wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "link2cat")
    wpdb.query("DROP TABLE IF EXISTS " + wpdb.prefix + "post2cat")
# end def upgrade_230_old_tables
#// 
#// Upgrade old slugs made in version 2.2.
#// 
#// @ignore
#// @since 2.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_old_slugs(*args_):
    
    #// Upgrade people who were using the Redirect Old Slugs plugin.
    global wpdb
    php_check_if_defined("wpdb")
    wpdb.query(str("UPDATE ") + str(wpdb.postmeta) + str(" SET meta_key = '_wp_old_slug' WHERE meta_key = 'old_slug'"))
# end def upgrade_old_slugs
#// 
#// Execute changes made in WordPress 2.5.0.
#// 
#// @ignore
#// @since 2.5.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_250(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    if wp_current_db_version < 6689:
        populate_roles_250()
    # end if
# end def upgrade_250
#// 
#// Execute changes made in WordPress 2.5.2.
#// 
#// @ignore
#// @since 2.5.2
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_252(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    wpdb.query(str("UPDATE ") + str(wpdb.users) + str(" SET user_activation_key = ''"))
# end def upgrade_252
#// 
#// Execute changes made in WordPress 2.6.
#// 
#// @ignore
#// @since 2.6.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_260(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    if wp_current_db_version < 8000:
        populate_roles_260()
    # end if
# end def upgrade_260
#// 
#// Execute changes made in WordPress 2.7.
#// 
#// @ignore
#// @since 2.7.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_270(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 8980:
        populate_roles_270()
    # end if
    #// Update post_date for unpublished posts with empty timestamp.
    if wp_current_db_version < 8921:
        wpdb.query(str("UPDATE ") + str(wpdb.posts) + str(" SET post_date = post_modified WHERE post_date = '0000-00-00 00:00:00'"))
    # end if
# end def upgrade_270
#// 
#// Execute changes made in WordPress 2.8.
#// 
#// @ignore
#// @since 2.8.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_280(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 10360:
        populate_roles_280()
    # end if
    if is_multisite():
        start = 0
        while True:
            rows = wpdb.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb.options) + str(" ORDER BY option_id LIMIT ") + str(start) + str(", 20"))
            if not (rows):
                break
            # end if
            for row in rows:
                value = row.option_value
                if (not php_no_error(lambda: unserialize(value))):
                    value = stripslashes(value)
                # end if
                if value != row.option_value:
                    update_option(row.option_name, value)
                # end if
            # end for
            start += 20
        # end while
        clean_blog_cache(get_current_blog_id())
    # end if
# end def upgrade_280
#// 
#// Execute changes made in WordPress 2.9.
#// 
#// @ignore
#// @since 2.9.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_290(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    if wp_current_db_version < 11958:
        #// Previously, setting depth to 1 would redundantly disable threading,
        #// but now 2 is the minimum depth to avoid confusion.
        if get_option("thread_comments_depth") == "1":
            update_option("thread_comments_depth", 2)
            update_option("thread_comments", 0)
        # end if
    # end if
# end def upgrade_290
#// 
#// Execute changes made in WordPress 3.0.
#// 
#// @ignore
#// @since 3.0.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_300(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 15093:
        populate_roles_300()
    # end if
    if wp_current_db_version < 14139 and is_multisite() and is_main_site() and (not php_defined("MULTISITE")) and get_site_option("siteurl") == False:
        add_site_option("siteurl", "")
    # end if
    #// 3.0 screen options key name changes.
    if wp_should_upgrade_global_tables():
        sql = str("DELETE FROM ") + str(wpdb.usermeta) + str("""\n          WHERE meta_key LIKE %s\n            OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key = 'manageedittagscolumnshidden'\n           OR meta_key = 'managecategoriescolumnshidden'\n         OR meta_key = 'manageedit-tagscolumnshidden'\n          OR meta_key = 'manageeditcolumnshidden'\n           OR meta_key = 'categories_per_page'\n           OR meta_key = 'edit_tags_per_page'""")
        prefix = wpdb.esc_like(wpdb.base_prefix)
        wpdb.query(wpdb.prepare(sql, prefix + "%" + wpdb.esc_like("meta-box-hidden") + "%", prefix + "%" + wpdb.esc_like("closedpostboxes") + "%", prefix + "%" + wpdb.esc_like("manage-") + "%" + wpdb.esc_like("-columns-hidden") + "%", prefix + "%" + wpdb.esc_like("meta-box-order") + "%", prefix + "%" + wpdb.esc_like("metaboxorder") + "%", prefix + "%" + wpdb.esc_like("screen_layout") + "%"))
    # end if
# end def upgrade_300
#// 
#// Execute changes made in WordPress 3.3.
#// 
#// @ignore
#// @since 3.3.0
#// 
#// @global int   $wp_current_db_version The old (current) database version.
#// @global wpdb  $wpdb                  WordPress database abstraction object.
#// @global array $wp_registered_widgets
#// @global array $sidebars_widgets
#//
def upgrade_330(*args_):
    
    global wp_current_db_version,wpdb,wp_registered_widgets,sidebars_widgets
    php_check_if_defined("wp_current_db_version","wpdb","wp_registered_widgets","sidebars_widgets")
    if wp_current_db_version < 19061 and wp_should_upgrade_global_tables():
        wpdb.query(str("DELETE FROM ") + str(wpdb.usermeta) + str(" WHERE meta_key IN ('show_admin_bar_admin', 'plugins_last_view')"))
    # end if
    if wp_current_db_version >= 11548:
        return
    # end if
    sidebars_widgets = get_option("sidebars_widgets", Array())
    _sidebars_widgets = Array()
    if (php_isset(lambda : sidebars_widgets["wp_inactive_widgets"])) or php_empty(lambda : sidebars_widgets):
        sidebars_widgets["array_version"] = 3
    elif (not (php_isset(lambda : sidebars_widgets["array_version"]))):
        sidebars_widgets["array_version"] = 1
    # end if
    for case in Switch(sidebars_widgets["array_version"]):
        if case(1):
            for index,sidebar in sidebars_widgets:
                if php_is_array(sidebar):
                    for i,name in sidebar:
                        id = php_strtolower(name)
                        if (php_isset(lambda : wp_registered_widgets[id])):
                            _sidebars_widgets[index][i] = id
                            continue
                        # end if
                        id = sanitize_title(name)
                        if (php_isset(lambda : wp_registered_widgets[id])):
                            _sidebars_widgets[index][i] = id
                            continue
                        # end if
                        found = False
                        for widget_id,widget in wp_registered_widgets:
                            if php_strtolower(widget["name"]) == php_strtolower(name):
                                _sidebars_widgets[index][i] = widget["id"]
                                found = True
                                break
                            elif sanitize_title(widget["name"]) == sanitize_title(name):
                                _sidebars_widgets[index][i] = widget["id"]
                                found = True
                                break
                            # end if
                        # end for
                        if found:
                            continue
                        # end if
                        _sidebars_widgets[index][i] = None
                    # end for
                # end if
            # end for
            _sidebars_widgets["array_version"] = 2
            sidebars_widgets = _sidebars_widgets
            _sidebars_widgets = None
        # end if
        if case(2):
            sidebars_widgets = retrieve_widgets()
            sidebars_widgets["array_version"] = 3
            update_option("sidebars_widgets", sidebars_widgets)
        # end if
    # end for
# end def upgrade_330
#// 
#// Execute changes made in WordPress 3.4.
#// 
#// @ignore
#// @since 3.4.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_340(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 19798:
        wpdb.hide_errors()
        wpdb.query(str("ALTER TABLE ") + str(wpdb.options) + str(" DROP COLUMN blog_id"))
        wpdb.show_errors()
    # end if
    if wp_current_db_version < 19799:
        wpdb.hide_errors()
        wpdb.query(str("ALTER TABLE ") + str(wpdb.comments) + str(" DROP INDEX comment_approved"))
        wpdb.show_errors()
    # end if
    if wp_current_db_version < 20022 and wp_should_upgrade_global_tables():
        wpdb.query(str("DELETE FROM ") + str(wpdb.usermeta) + str(" WHERE meta_key = 'themes_last_view'"))
    # end if
    if wp_current_db_version < 20080:
        if "yes" == wpdb.get_var(str("SELECT autoload FROM ") + str(wpdb.options) + str(" WHERE option_name = 'uninstall_plugins'")):
            uninstall_plugins = get_option("uninstall_plugins")
            delete_option("uninstall_plugins")
            add_option("uninstall_plugins", uninstall_plugins, None, "no")
        # end if
    # end if
# end def upgrade_340
#// 
#// Execute changes made in WordPress 3.5.
#// 
#// @ignore
#// @since 3.5.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_350(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 22006 and wpdb.get_var(str("SELECT link_id FROM ") + str(wpdb.links) + str(" LIMIT 1")):
        update_option("link_manager_enabled", 1)
        pass
    # end if
    if wp_current_db_version < 21811 and wp_should_upgrade_global_tables():
        meta_keys = Array()
        for name in php_array_merge(get_post_types(), get_taxonomies()):
            if False != php_strpos(name, "-"):
                meta_keys[-1] = "edit_" + php_str_replace("-", "_", name) + "_per_page"
            # end if
        # end for
        if meta_keys:
            meta_keys = php_implode("', '", meta_keys)
            wpdb.query(str("DELETE FROM ") + str(wpdb.usermeta) + str(" WHERE meta_key IN ('") + str(meta_keys) + str("')"))
        # end if
    # end if
    if wp_current_db_version < 22422:
        term = get_term_by("slug", "post-format-standard", "post_format")
        if term:
            wp_delete_term(term.term_id, "post_format")
        # end if
    # end if
# end def upgrade_350
#// 
#// Execute changes made in WordPress 3.7.
#// 
#// @ignore
#// @since 3.7.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_370(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    if wp_current_db_version < 25824:
        wp_clear_scheduled_hook("wp_auto_updates_maybe_update")
    # end if
# end def upgrade_370
#// 
#// Execute changes made in WordPress 3.7.2.
#// 
#// @ignore
#// @since 3.7.2
#// @since 3.8.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_372(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    if wp_current_db_version < 26148:
        wp_clear_scheduled_hook("wp_maybe_auto_update")
    # end if
# end def upgrade_372
#// 
#// Execute changes made in WordPress 3.8.0.
#// 
#// @ignore
#// @since 3.8.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_380(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    if wp_current_db_version < 26691:
        deactivate_plugins(Array("mp6/mp6.php"), True)
    # end if
# end def upgrade_380
#// 
#// Execute changes made in WordPress 4.0.0.
#// 
#// @ignore
#// @since 4.0.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_400(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    if wp_current_db_version < 29630:
        if (not is_multisite()) and False == get_option("WPLANG"):
            if php_defined("WPLANG") and "" != WPLANG and php_in_array(WPLANG, get_available_languages()):
                update_option("WPLANG", WPLANG)
            else:
                update_option("WPLANG", "")
            # end if
        # end if
    # end if
# end def upgrade_400
#// 
#// Execute changes made in WordPress 4.2.0.
#// 
#// @ignore
#// @since 4.2.0
#//
def upgrade_420(*args_):
    
    pass
# end def upgrade_420
#// 
#// Executes changes made in WordPress 4.3.0.
#// 
#// @ignore
#// @since 4.3.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_430(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 32364:
        upgrade_430_fix_comments()
    # end if
    #// Shared terms are split in a separate process.
    if wp_current_db_version < 32814:
        update_option("finished_splitting_shared_terms", 0)
        wp_schedule_single_event(time() + 1 * MINUTE_IN_SECONDS, "wp_split_shared_term_batch")
    # end if
    if wp_current_db_version < 33055 and "utf8mb4" == wpdb.charset:
        if is_multisite():
            tables = wpdb.tables("blog")
        else:
            tables = wpdb.tables("all")
            if (not wp_should_upgrade_global_tables()):
                global_tables = wpdb.tables("global")
                tables = php_array_diff_assoc(tables, global_tables)
            # end if
        # end if
        for table in tables:
            maybe_convert_table_to_utf8mb4(table)
        # end for
    # end if
# end def upgrade_430
#// 
#// Executes comments changes made in WordPress 4.3.0.
#// 
#// @ignore
#// @since 4.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_430_fix_comments(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    content_length = wpdb.get_col_length(wpdb.comments, "comment_content")
    if is_wp_error(content_length):
        return
    # end if
    if False == content_length:
        content_length = Array({"type": "byte", "length": 65535})
    elif (not php_is_array(content_length)):
        length = int(content_length) if int(content_length) > 0 else 65535
        content_length = Array({"type": "byte", "length": length})
    # end if
    if "byte" != content_length["type"] or 0 == content_length["length"]:
        #// Sites with malformed DB schemas are on their own.
        return
    # end if
    allowed_length = php_intval(content_length["length"]) - 10
    comments = wpdb.get_results(str("SELECT `comment_ID` FROM `") + str(wpdb.comments) + str("`\n           WHERE `comment_date_gmt` > '2015-04-26'\n           AND LENGTH( `comment_content` ) >= ") + str(allowed_length) + str("\n           AND ( `comment_content` LIKE '%<%' OR `comment_content` LIKE '%>%' )"))
    for comment in comments:
        wp_delete_comment(comment.comment_ID, True)
    # end for
# end def upgrade_430_fix_comments
#// 
#// Executes changes made in WordPress 4.3.1.
#// 
#// @ignore
#// @since 4.3.1
#//
def upgrade_431(*args_):
    
    #// Fix incorrect cron entries for term splitting.
    cron_array = _get_cron_array()
    if (php_isset(lambda : cron_array["wp_batch_split_terms"])):
        cron_array["wp_batch_split_terms"] = None
        _set_cron_array(cron_array)
    # end if
# end def upgrade_431
#// 
#// Executes changes made in WordPress 4.4.0.
#// 
#// @ignore
#// @since 4.4.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_440(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 34030:
        wpdb.query(str("ALTER TABLE ") + str(wpdb.options) + str(" MODIFY option_name VARCHAR(191)"))
    # end if
    #// Remove the unused 'add_users' role.
    roles = wp_roles()
    for role in roles.role_objects:
        if role.has_cap("add_users"):
            role.remove_cap("add_users")
        # end if
    # end for
# end def upgrade_440
#// 
#// Executes changes made in WordPress 4.5.0.
#// 
#// @ignore
#// @since 4.5.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_450(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version < 36180:
        wp_clear_scheduled_hook("wp_maybe_auto_update")
    # end if
    #// Remove unused email confirmation options, moved to usermeta.
    if wp_current_db_version < 36679 and is_multisite():
        wpdb.query(str("DELETE FROM ") + str(wpdb.options) + str(" WHERE option_name REGEXP '^[0-9]+_new_email$'"))
    # end if
    #// Remove unused user setting for wpLink.
    delete_user_setting("wplink")
# end def upgrade_450
#// 
#// Executes changes made in WordPress 4.6.0.
#// 
#// @ignore
#// @since 4.6.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_460(*args_):
    
    global wp_current_db_version
    php_check_if_defined("wp_current_db_version")
    #// Remove unused post meta.
    if wp_current_db_version < 37854:
        delete_post_meta_by_key("_post_restored_from")
    # end if
    #// Remove plugins with callback as an array object/method as the uninstall hook, see #13786.
    if wp_current_db_version < 37965:
        uninstall_plugins = get_option("uninstall_plugins", Array())
        if (not php_empty(lambda : uninstall_plugins)):
            for basename,callback in uninstall_plugins:
                if php_is_array(callback) and php_is_object(callback[0]):
                    uninstall_plugins[basename] = None
                # end if
            # end for
            update_option("uninstall_plugins", uninstall_plugins)
        # end if
    # end if
# end def upgrade_460
#// 
#// Executes changes made in WordPress 5.0.0.
#// 
#// @ignore
#// @since 5.0.0
#// @deprecated 5.1.0
#//
def upgrade_500(*args_):
    
    pass
# end def upgrade_500
#// 
#// Executes changes made in WordPress 5.1.0.
#// 
#// @ignore
#// @since 5.1.0
#//
def upgrade_510(*args_):
    
    delete_site_option("upgrade_500_was_gutenberg_active")
# end def upgrade_510
#// 
#// Executes changes made in WordPress 5.3.0.
#// 
#// @ignore
#// @since 5.3.0
#//
def upgrade_530(*args_):
    
    #// 
    #// The `admin_email_lifespan` option may have been set by an admin that just logged in,
    #// saw the verification screen, clicked on a button there, and is now upgrading the db,
    #// or by populate_options() that is called earlier in upgrade_all().
    #// In the second case `admin_email_lifespan` should be reset so the verification screen
    #// is shown next time an admin logs in.
    #//
    if php_function_exists("current_user_can") and (not current_user_can("manage_options")):
        update_option("admin_email_lifespan", 0)
    # end if
# end def upgrade_530
#// 
#// Executes network-level upgrade routines.
#// 
#// @since 3.0.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def upgrade_network(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    #// Always clear expired transients.
    delete_expired_transients(True)
    #// 2.8
    if wp_current_db_version < 11549:
        wpmu_sitewide_plugins = get_site_option("wpmu_sitewide_plugins")
        active_sitewide_plugins = get_site_option("active_sitewide_plugins")
        if wpmu_sitewide_plugins:
            if (not active_sitewide_plugins):
                sitewide_plugins = wpmu_sitewide_plugins
            else:
                sitewide_plugins = php_array_merge(active_sitewide_plugins, wpmu_sitewide_plugins)
            # end if
            update_site_option("active_sitewide_plugins", sitewide_plugins)
        # end if
        delete_site_option("wpmu_sitewide_plugins")
        delete_site_option("deactivated_sitewide_plugins")
        start = 0
        while True:
            rows = wpdb.get_results(str("SELECT meta_key, meta_value FROM ") + str(wpdb.sitemeta) + str(" ORDER BY meta_id LIMIT ") + str(start) + str(", 20"))
            if not (rows):
                break
            # end if
            for row in rows:
                value = row.meta_value
                if (not php_no_error(lambda: unserialize(value))):
                    value = stripslashes(value)
                # end if
                if value != row.meta_value:
                    update_site_option(row.meta_key, value)
                # end if
            # end for
            start += 20
        # end while
    # end if
    #// 3.0
    if wp_current_db_version < 13576:
        update_site_option("global_terms_enabled", "1")
    # end if
    #// 3.3
    if wp_current_db_version < 19390:
        update_site_option("initial_db_version", wp_current_db_version)
    # end if
    if wp_current_db_version < 19470:
        if False == get_site_option("active_sitewide_plugins"):
            update_site_option("active_sitewide_plugins", Array())
        # end if
    # end if
    #// 3.4
    if wp_current_db_version < 20148:
        #// 'allowedthemes' keys things by stylesheet. 'allowed_themes' keyed things by name.
        allowedthemes = get_site_option("allowedthemes")
        allowed_themes = get_site_option("allowed_themes")
        if False == allowedthemes and php_is_array(allowed_themes) and allowed_themes:
            converted = Array()
            themes = wp_get_themes()
            for stylesheet,theme_data in themes:
                if (php_isset(lambda : allowed_themes[theme_data.get("Name")])):
                    converted[stylesheet] = True
                # end if
            # end for
            update_site_option("allowedthemes", converted)
            delete_site_option("allowed_themes")
        # end if
    # end if
    #// 3.5
    if wp_current_db_version < 21823:
        update_site_option("ms_files_rewriting", "1")
    # end if
    #// 3.5.2
    if wp_current_db_version < 24448:
        illegal_names = get_site_option("illegal_names")
        if php_is_array(illegal_names) and php_count(illegal_names) == 1:
            illegal_name = reset(illegal_names)
            illegal_names = php_explode(" ", illegal_name)
            update_site_option("illegal_names", illegal_names)
        # end if
    # end if
    #// 4.2
    if wp_current_db_version < 31351 and "utf8mb4" == wpdb.charset:
        if wp_should_upgrade_global_tables():
            wpdb.query(str("ALTER TABLE ") + str(wpdb.usermeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
            wpdb.query(str("ALTER TABLE ") + str(wpdb.site) + str(" DROP INDEX domain, ADD INDEX domain(domain(140),path(51))"))
            wpdb.query(str("ALTER TABLE ") + str(wpdb.sitemeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
            wpdb.query(str("ALTER TABLE ") + str(wpdb.signups) + str(" DROP INDEX domain_path, ADD INDEX domain_path(domain(140),path(51))"))
            tables = wpdb.tables("global")
            #// sitecategories may not exist.
            if (not wpdb.get_var(str("SHOW TABLES LIKE '") + str(tables["sitecategories"]) + str("'"))):
                tables["sitecategories"] = None
            # end if
            for table in tables:
                maybe_convert_table_to_utf8mb4(table)
            # end for
        # end if
    # end if
    #// 4.3
    if wp_current_db_version < 33055 and "utf8mb4" == wpdb.charset:
        if wp_should_upgrade_global_tables():
            upgrade = False
            indexes = wpdb.get_results(str("SHOW INDEXES FROM ") + str(wpdb.signups))
            for index in indexes:
                if "domain_path" == index.Key_name and "domain" == index.Column_name and 140 != index.Sub_part:
                    upgrade = True
                    break
                # end if
            # end for
            if upgrade:
                wpdb.query(str("ALTER TABLE ") + str(wpdb.signups) + str(" DROP INDEX domain_path, ADD INDEX domain_path(domain(140),path(51))"))
            # end if
            tables = wpdb.tables("global")
            #// sitecategories may not exist.
            if (not wpdb.get_var(str("SHOW TABLES LIKE '") + str(tables["sitecategories"]) + str("'"))):
                tables["sitecategories"] = None
            # end if
            for table in tables:
                maybe_convert_table_to_utf8mb4(table)
            # end for
        # end if
    # end if
    #// 5.1
    if wp_current_db_version < 44467:
        network_id = get_main_network_id()
        delete_network_option(network_id, "site_meta_supported")
        is_site_meta_supported()
    # end if
# end def upgrade_network
#// 
#// General functions we use to actually do stuff.
#// 
#// 
#// Creates a table in the database if it doesn't already exist.
#// 
#// This method checks for an existing database and creates a new one if it's not
#// already present. It doesn't rely on MySQL's "IF NOT EXISTS" statement, but chooses
#// to query all tables first and then run the SQL statement creating the table.
#// 
#// @since 1.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $table_name Database table name to create.
#// @param string $create_ddl SQL statement to create table.
#// @return bool If table already exists or was created by function.
#//
def maybe_create_table(table_name=None, create_ddl=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    query = wpdb.prepare("SHOW TABLES LIKE %s", wpdb.esc_like(table_name))
    if wpdb.get_var(query) == table_name:
        return True
    # end if
    #// Didn't find it, so try to create it.
    wpdb.query(create_ddl)
    #// We cannot directly tell that whether this succeeded!
    if wpdb.get_var(query) == table_name:
        return True
    # end if
    return False
# end def maybe_create_table
#// 
#// Drops a specified index from a table.
#// 
#// @since 1.0.1
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $table Database table name.
#// @param string $index Index name to drop.
#// @return true True, when finished.
#//
def drop_index(table=None, index=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    wpdb.hide_errors()
    wpdb.query(str("ALTER TABLE `") + str(table) + str("` DROP INDEX `") + str(index) + str("`"))
    #// Now we need to take out all the extra ones we may have created.
    i = 0
    while i < 25:
        
        wpdb.query(str("ALTER TABLE `") + str(table) + str("` DROP INDEX `") + str(index) + str("_") + str(i) + str("`"))
        i += 1
    # end while
    wpdb.show_errors()
    return True
# end def drop_index
#// 
#// Adds an index to a specified table.
#// 
#// @since 1.0.1
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $table Database table name.
#// @param string $index Database table index column.
#// @return true True, when done with execution.
#//
def add_clean_index(table=None, index=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    drop_index(table, index)
    wpdb.query(str("ALTER TABLE `") + str(table) + str("` ADD INDEX ( `") + str(index) + str("` )"))
    return True
# end def add_clean_index
#// 
#// Adds column to a database table if it doesn't already exist.
#// 
#// @since 1.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $table_name  The table name to modify.
#// @param string $column_name The column name to add to the table.
#// @param string $create_ddl  The SQL statement used to add the column.
#// @return bool True if already exists or on successful completion, false on error.
#//
def maybe_add_column(table_name=None, column_name=None, create_ddl=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    for column in wpdb.get_col(str("DESC ") + str(table_name), 0):
        if column == column_name:
            return True
        # end if
    # end for
    #// Didn't find it, so try to create it.
    wpdb.query(create_ddl)
    #// We cannot directly tell that whether this succeeded!
    for column in wpdb.get_col(str("DESC ") + str(table_name), 0):
        if column == column_name:
            return True
        # end if
    # end for
    return False
# end def maybe_add_column
#// 
#// If a table only contains utf8 or utf8mb4 columns, convert it to utf8mb4.
#// 
#// @since 4.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $table The table to convert.
#// @return bool true if the table was converted, false if it wasn't.
#//
def maybe_convert_table_to_utf8mb4(table=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    results = wpdb.get_results(str("SHOW FULL COLUMNS FROM `") + str(table) + str("`"))
    if (not results):
        return False
    # end if
    for column in results:
        if column.Collation:
            charset = php_explode("_", column.Collation)
            charset = php_strtolower(charset)
            if "utf8" != charset and "utf8mb4" != charset:
                #// Don't upgrade tables that have non-utf8 columns.
                return False
            # end if
        # end if
    # end for
    table_details = wpdb.get_row(str("SHOW TABLE STATUS LIKE '") + str(table) + str("'"))
    if (not table_details):
        return False
    # end if
    table_charset = php_explode("_", table_details.Collation)
    table_charset = php_strtolower(table_charset)
    if "utf8mb4" == table_charset:
        return True
    # end if
    return wpdb.query(str("ALTER TABLE ") + str(table) + str(" CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
# end def maybe_convert_table_to_utf8mb4
#// 
#// Retrieve all options as it was for 1.2.
#// 
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return stdClass List of options.
#//
def get_alloptions_110(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    all_options = php_new_class("stdClass", lambda : stdClass())
    options = wpdb.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb.options))
    if options:
        for option in options:
            if "siteurl" == option.option_name or "home" == option.option_name or "category_base" == option.option_name:
                option.option_value = untrailingslashit(option.option_value)
            # end if
            all_options.option.option_name = stripslashes(option.option_value)
        # end for
    # end if
    return all_options
# end def get_alloptions_110
#// 
#// Utility version of get_option that is private to installation/upgrade.
#// 
#// @ignore
#// @since 1.5.1
#// @access private
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $setting Option name.
#// @return mixed
#//
def __get_option(setting=None, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    global wpdb
    php_check_if_defined("wpdb")
    if "home" == setting and php_defined("WP_HOME"):
        return untrailingslashit(WP_HOME)
    # end if
    if "siteurl" == setting and php_defined("WP_SITEURL"):
        return untrailingslashit(WP_SITEURL)
    # end if
    option = wpdb.get_var(wpdb.prepare(str("SELECT option_value FROM ") + str(wpdb.options) + str(" WHERE option_name = %s"), setting))
    if "home" == setting and "" == option:
        return __get_option("siteurl")
    # end if
    if "siteurl" == setting or "home" == setting or "category_base" == setting or "tag_base" == setting:
        option = untrailingslashit(option)
    # end if
    return maybe_unserialize(option)
# end def __get_option
#// 
#// Filters for content to remove unnecessary slashes.
#// 
#// @since 1.5.0
#// 
#// @param string $content The content to modify.
#// @return string The de-slashed content.
#//
def deslash(content=None, *args_):
    
    #// Note: \\\ inside a regex denotes a single backslash.
    #// 
    #// Replace one or more backslashes followed by a single quote with
    #// a single quote.
    #//
    content = php_preg_replace("/\\\\+'/", "'", content)
    #// 
    #// Replace one or more backslashes followed by a double quote with
    #// a double quote.
    #//
    content = php_preg_replace("/\\\\+\"/", "\"", content)
    #// Replace one or more backslashes with one backslash.
    content = php_preg_replace("/\\\\+/", "\\", content)
    return content
# end def deslash
#// 
#// Modifies the database based on specified SQL statements.
#// 
#// Useful for creating new tables and updating existing tables to a new structure.
#// 
#// @since 1.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string[]|string $queries Optional. The query to run. Can be multiple queries
#// in an array, or a string of queries separated by
#// semicolons. Default empty string.
#// @param bool            $execute Optional. Whether or not to execute the query right away.
#// Default true.
#// @return array Strings containing the results of the various update queries.
#//
def dbDelta(queries="", execute=True, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    global wpdb
    php_check_if_defined("wpdb")
    if php_in_array(queries, Array("", "all", "blog", "global", "ms_global"), True):
        queries = wp_get_db_schema(queries)
    # end if
    #// Separate individual queries into an array.
    if (not php_is_array(queries)):
        queries = php_explode(";", queries)
        queries = php_array_filter(queries)
    # end if
    #// 
    #// Filters the dbDelta SQL queries.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[] $queries An array of dbDelta SQL queries.
    #//
    queries = apply_filters("dbdelta_queries", queries)
    cqueries = Array()
    #// Creation queries.
    iqueries = Array()
    #// Insertion queries.
    for_update = Array()
    #// Create a tablename index for an array ($cqueries) of queries.
    for qry in queries:
        if php_preg_match("|CREATE TABLE ([^ ]*)|", qry, matches):
            cqueries[php_trim(matches[1], "`")] = qry
            for_update[matches[1]] = "Created table " + matches[1]
        elif php_preg_match("|CREATE DATABASE ([^ ]*)|", qry, matches):
            array_unshift(cqueries, qry)
        elif php_preg_match("|INSERT INTO ([^ ]*)|", qry, matches):
            iqueries[-1] = qry
        elif php_preg_match("|UPDATE ([^ ]*)|", qry, matches):
            iqueries[-1] = qry
        else:
            pass
        # end if
    # end for
    #// 
    #// Filters the dbDelta SQL queries for creating tables and/or databases.
    #// 
    #// Queries filterable via this hook contain "CREATE TABLE" or "CREATE DATABASE".
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[] $cqueries An array of dbDelta create SQL queries.
    #//
    cqueries = apply_filters("dbdelta_create_queries", cqueries)
    #// 
    #// Filters the dbDelta SQL queries for inserting or updating.
    #// 
    #// Queries filterable via this hook contain "INSERT INTO" or "UPDATE".
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[] $iqueries An array of dbDelta insert or update SQL queries.
    #//
    iqueries = apply_filters("dbdelta_insert_queries", iqueries)
    text_fields = Array("tinytext", "text", "mediumtext", "longtext")
    blob_fields = Array("tinyblob", "blob", "mediumblob", "longblob")
    global_tables = wpdb.tables("global")
    for table,qry in cqueries:
        #// Upgrade global tables only for the main site. Don't upgrade at all if conditions are not optimal.
        if php_in_array(table, global_tables) and (not wp_should_upgrade_global_tables()):
            cqueries[table] = None
            for_update[table] = None
            continue
        # end if
        #// Fetch the table column structure from the database.
        suppress = wpdb.suppress_errors()
        tablefields = wpdb.get_results(str("DESCRIBE ") + str(table) + str(";"))
        wpdb.suppress_errors(suppress)
        if (not tablefields):
            continue
        # end if
        #// Clear the field and index arrays.
        cfields = Array()
        indices = Array()
        indices_without_subparts = Array()
        #// Get all of the field names in the query from between the parentheses.
        php_preg_match("|\\((.*)\\)|ms", qry, match2)
        qryline = php_trim(match2[1])
        #// Separate field lines into an array.
        flds = php_explode("\n", qryline)
        #// For every field line specified in the query.
        for fld in flds:
            fld = php_trim(fld, "   \n\r ,")
            #// Default trim characters, plus ','.
            #// Extract the field name.
            php_preg_match("|^([^ ]*)|", fld, fvals)
            fieldname = php_trim(fvals[1], "`")
            fieldname_lowercased = php_strtolower(fieldname)
            #// Verify the found field name.
            validfield = True
            for case in Switch(fieldname_lowercased):
                if case(""):
                    pass
                # end if
                if case("primary"):
                    pass
                # end if
                if case("index"):
                    pass
                # end if
                if case("fulltext"):
                    pass
                # end if
                if case("unique"):
                    pass
                # end if
                if case("key"):
                    pass
                # end if
                if case("spatial"):
                    validfield = False
                    #// 
                    #// Normalize the index definition.
                    #// 
                    #// This is done so the definition can be compared against the result of a
                    #// `SHOW INDEX FROM $table_name` query which returns the current table
                    #// index information.
                    #// 
                    #// Extract type, name and columns from the definition.
                    #// phpcs:disable Squiz.Strings.ConcatenationSpacing.PaddingFound -- don't remove regex indentation
                    php_preg_match("/^" + "(?P<index_type>" + "PRIMARY\\s+KEY|(?:UNIQUE|FULLTEXT|SPATIAL)\\s+(?:KEY|INDEX)|KEY|INDEX" + ")" + "\\s+" + "(?:" + "`?" + "(?P<index_name>" + "(?:[0-9a-zA-Z$_-]|[\\xC2-\\xDF][\\x80-\\xBF])+" + ")" + "`?" + "\\s+" + ")*" + "\\(" + "(?P<index_columns>" + ".+?" + ")" + "\\)" + "$/im", fld, index_matches)
                    #// phpcs:enable
                    #// Uppercase the index type and normalize space characters.
                    index_type = php_strtoupper(php_preg_replace("/\\s+/", " ", php_trim(index_matches["index_type"])))
                    #// 'INDEX' is a synonym for 'KEY', standardize on 'KEY'.
                    index_type = php_str_replace("INDEX", "KEY", index_type)
                    #// Escape the index name with backticks. An index for a primary key has no name.
                    index_name = "" if "PRIMARY KEY" == index_type else "`" + php_strtolower(index_matches["index_name"]) + "`"
                    #// Parse the columns. Multiple columns are separated by a comma.
                    index_columns = php_array_map("trim", php_explode(",", index_matches["index_columns"]))
                    index_columns_without_subparts = index_columns
                    #// Normalize columns.
                    for id,index_column in index_columns:
                        #// Extract column name and number of indexed characters (sub_part).
                        php_preg_match("/" + "`?" + "(?P<column_name>" + "(?:[0-9a-zA-Z$_-]|[\\xC2-\\xDF][\\x80-\\xBF])+" + ")" + "`?" + "(?:" + "\\s*" + "\\(" + "\\s*" + "(?P<sub_part>" + "\\d+" + ")" + "\\s*" + "\\)" + ")?" + "/", index_column, index_column_matches)
                        #// Escape the column name with backticks.
                        index_column = "`" + index_column_matches["column_name"] + "`"
                        #// We don't need to add the subpart to $index_columns_without_subparts
                        index_columns_without_subparts[id] = index_column
                        #// Append the optional sup part with the number of indexed characters.
                        if (php_isset(lambda : index_column_matches["sub_part"])):
                            index_column += "(" + index_column_matches["sub_part"] + ")"
                        # end if
                    # end for
                    #// Build the normalized index definition and add it to the list of indices.
                    indices[-1] = str(index_type) + str(" ") + str(index_name) + str(" (") + php_implode(",", index_columns) + ")"
                    indices_without_subparts[-1] = str(index_type) + str(" ") + str(index_name) + str(" (") + php_implode(",", index_columns_without_subparts) + ")"
                    index_column = None
                    index_column_matches = None
                    index_matches = None
                    index_type = None
                    index_name = None
                    index_columns = None
                    index_columns_without_subparts = None
                    break
                # end if
            # end for
            #// If it's a valid field, add it to the field array.
            if validfield:
                cfields[fieldname_lowercased] = fld
            # end if
        # end for
        #// For every field in the table.
        for tablefield in tablefields:
            tablefield_field_lowercased = php_strtolower(tablefield.Field)
            tablefield_type_lowercased = php_strtolower(tablefield.Type)
            #// If the table field exists in the field array...
            if php_array_key_exists(tablefield_field_lowercased, cfields):
                #// Get the field type from the query.
                php_preg_match("|`?" + tablefield.Field + "`? ([^ ]*( unsigned)?)|i", cfields[tablefield_field_lowercased], matches)
                fieldtype = matches[1]
                fieldtype_lowercased = php_strtolower(fieldtype)
                #// Is actual field type different from the field type in query?
                if tablefield.Type != fieldtype:
                    do_change = True
                    if php_in_array(fieldtype_lowercased, text_fields) and php_in_array(tablefield_type_lowercased, text_fields):
                        if php_array_search(fieldtype_lowercased, text_fields) < php_array_search(tablefield_type_lowercased, text_fields):
                            do_change = False
                        # end if
                    # end if
                    if php_in_array(fieldtype_lowercased, blob_fields) and php_in_array(tablefield_type_lowercased, blob_fields):
                        if php_array_search(fieldtype_lowercased, blob_fields) < php_array_search(tablefield_type_lowercased, blob_fields):
                            do_change = False
                        # end if
                    # end if
                    if do_change:
                        #// Add a query to change the column type.
                        cqueries[-1] = str("ALTER TABLE ") + str(table) + str(" CHANGE COLUMN `") + str(tablefield.Field) + str("` ") + cfields[tablefield_field_lowercased]
                        for_update[table + "." + tablefield.Field] = str("Changed type of ") + str(table) + str(".") + str(tablefield.Field) + str(" from ") + str(tablefield.Type) + str(" to ") + str(fieldtype)
                    # end if
                # end if
                #// Get the default value from the array.
                if php_preg_match("| DEFAULT '(.*?)'|i", cfields[tablefield_field_lowercased], matches):
                    default_value = matches[1]
                    if tablefield.Default != default_value:
                        #// Add a query to change the column's default value
                        cqueries[-1] = str("ALTER TABLE ") + str(table) + str(" ALTER COLUMN `") + str(tablefield.Field) + str("` SET DEFAULT '") + str(default_value) + str("'")
                        for_update[table + "." + tablefield.Field] = str("Changed default value of ") + str(table) + str(".") + str(tablefield.Field) + str(" from ") + str(tablefield.Default) + str(" to ") + str(default_value)
                    # end if
                # end if
                cfields[tablefield_field_lowercased] = None
            else:
                pass
            # end if
        # end for
        #// For every remaining field specified for the table.
        for fieldname,fielddef in cfields:
            #// Push a query line into $cqueries that adds the field to that table.
            cqueries[-1] = str("ALTER TABLE ") + str(table) + str(" ADD COLUMN ") + str(fielddef)
            for_update[table + "." + fieldname] = "Added column " + table + "." + fieldname
        # end for
        #// Index stuff goes here. Fetch the table index structure from the database.
        tableindices = wpdb.get_results(str("SHOW INDEX FROM ") + str(table) + str(";"))
        if tableindices:
            #// Clear the index array.
            index_ary = Array()
            #// For every index in the table.
            for tableindex in tableindices:
                keyname = php_strtolower(tableindex.Key_name)
                #// Add the index to the index data array.
                index_ary[keyname]["columns"][-1] = Array({"fieldname": tableindex.Column_name, "subpart": tableindex.Sub_part})
                index_ary[keyname]["unique"] = True if 0 == tableindex.Non_unique else False
                index_ary[keyname]["index_type"] = tableindex.Index_type
            # end for
            #// For each actual index in the index array.
            for index_name,index_data in index_ary:
                #// Build a create string to compare to the query.
                index_string = ""
                if "primary" == index_name:
                    index_string += "PRIMARY "
                elif index_data["unique"]:
                    index_string += "UNIQUE "
                # end if
                if "FULLTEXT" == php_strtoupper(index_data["index_type"]):
                    index_string += "FULLTEXT "
                # end if
                if "SPATIAL" == php_strtoupper(index_data["index_type"]):
                    index_string += "SPATIAL "
                # end if
                index_string += "KEY "
                if "primary" != index_name:
                    index_string += "`" + index_name + "`"
                # end if
                index_columns = ""
                #// For each column in the index.
                for column_data in index_data["columns"]:
                    if "" != index_columns:
                        index_columns += ","
                    # end if
                    #// Add the field to the column list string.
                    index_columns += "`" + column_data["fieldname"] + "`"
                # end for
                #// Add the column list to the index create string.
                index_string += str(" (") + str(index_columns) + str(")")
                #// Check if the index definition exists, ignoring subparts.
                aindex = php_array_search(index_string, indices_without_subparts)
                if False != aindex:
                    indices_without_subparts[aindex] = None
                    indices[aindex] = None
                # end if
            # end for
        # end if
        #// For every remaining index specified for the table.
        for index in indices:
            #// Push a query line into $cqueries that adds the index to that table.
            cqueries[-1] = str("ALTER TABLE ") + str(table) + str(" ADD ") + str(index)
            for_update[-1] = "Added index " + table + " " + index
        # end for
        cqueries[table] = None
        for_update[table] = None
    # end for
    allqueries = php_array_merge(cqueries, iqueries)
    if execute:
        for query in allqueries:
            wpdb.query(query)
        # end for
    # end if
    return for_update
# end def dbDelta
#// 
#// Updates the database tables to a new schema.
#// 
#// By default, updates all the tables to use the latest defined schema, but can also
#// be used to update a specific set of tables in wp_get_db_schema().
#// 
#// @since 1.5.0
#// 
#// @uses dbDelta
#// 
#// @param string $tables Optional. Which set of tables to update. Default is 'all'.
#//
def make_db_current(tables="all", *args_):
    
    alterations = dbDelta(tables)
    php_print("<ol>\n")
    for alteration in alterations:
        php_print(str("<li>") + str(alteration) + str("</li>\n"))
    # end for
    php_print("</ol>\n")
# end def make_db_current
#// 
#// Updates the database tables to a new schema, but without displaying results.
#// 
#// By default, updates all the tables to use the latest defined schema, but can
#// also be used to update a specific set of tables in wp_get_db_schema().
#// 
#// @since 1.5.0
#// 
#// @see make_db_current()
#// 
#// @param string $tables Optional. Which set of tables to update. Default is 'all'.
#//
def make_db_current_silent(tables="all", *args_):
    
    dbDelta(tables)
# end def make_db_current_silent
#// 
#// Creates a site theme from an existing theme.
#// 
#// {@internal Missing Long Description}}
#// 
#// @since 1.5.0
#// 
#// @param string $theme_name The name of the theme.
#// @param string $template   The directory name of the theme.
#// @return bool
#//
def make_site_theme_from_oldschool(theme_name=None, template=None, *args_):
    
    home_path = get_home_path()
    site_dir = WP_CONTENT_DIR + str("/themes/") + str(template)
    if (not php_file_exists(str(home_path) + str("/index.php"))):
        return False
    # end if
    #// 
    #// Copy files from the old locations to the site theme.
    #// TODO: This does not copy arbitrary include dependencies. Only the standard WP files are copied.
    #//
    files = Array({"index.php": "index.php", "wp-layout.css": "style.css", "wp-comments.php": "comments.php", "wp-comments-popup.php": "comments-popup.php"})
    for oldfile,newfile in files:
        if "index.php" == oldfile:
            oldpath = home_path
        else:
            oldpath = ABSPATH
        # end if
        #// Check to make sure it's not a new index.
        if "index.php" == oldfile:
            index = php_implode("", file(str(oldpath) + str("/") + str(oldfile)))
            if php_strpos(index, "WP_USE_THEMES") != False:
                if (not copy(WP_CONTENT_DIR + "/themes/" + WP_DEFAULT_THEME + "/index.php", str(site_dir) + str("/") + str(newfile))):
                    return False
                # end if
                continue
            # end if
        # end if
        if (not copy(str(oldpath) + str("/") + str(oldfile), str(site_dir) + str("/") + str(newfile))):
            return False
        # end if
        chmod(str(site_dir) + str("/") + str(newfile), 511)
        #// Update the blog header include in each file.
        lines = php_explode("\n", php_implode("", file(str(site_dir) + str("/") + str(newfile))))
        if lines:
            f = fopen(str(site_dir) + str("/") + str(newfile), "w")
            for line in lines:
                if php_preg_match("/require.*wp-blog-header/", line):
                    line = "//" + line
                # end if
                #// Update stylesheet references.
                line = php_str_replace("<?php echo __get_option('siteurl'); ?>/wp-layout.css", "<?php bloginfo('stylesheet_url'); ?>", line)
                #// Update comments template inclusion.
                line = php_str_replace("<?php include(ABSPATH . 'wp-comments.php'); ?>", "<?php comments_template(); ?>", line)
                fwrite(f, str(line) + str("\n"))
            # end for
            php_fclose(f)
        # end if
    # end for
    #// Add a theme header.
    header = str("/*\nTheme Name: ") + str(theme_name) + str("\nTheme URI: ") + __get_option("siteurl") + """
    Description: A theme automatically created by the update.
    Version: 1.0
    Author: Moi
    */
    """
    stylelines = php_file_get_contents(str(site_dir) + str("/style.css"))
    if stylelines:
        f = fopen(str(site_dir) + str("/style.css"), "w")
        fwrite(f, header)
        fwrite(f, stylelines)
        php_fclose(f)
    # end if
    return True
# end def make_site_theme_from_oldschool
#// 
#// Creates a site theme from the default theme.
#// 
#// {@internal Missing Long Description}}
#// 
#// @since 1.5.0
#// 
#// @param string $theme_name The name of the theme.
#// @param string $template   The directory name of the theme.
#// @return void|false
#//
def make_site_theme_from_default(theme_name=None, template=None, *args_):
    
    site_dir = WP_CONTENT_DIR + str("/themes/") + str(template)
    default_dir = WP_CONTENT_DIR + "/themes/" + WP_DEFAULT_THEME
    #// Copy files from the default theme to the site theme.
    #// $files = array( 'index.php', 'comments.php', 'comments-popup.php', 'footer.php', 'header.php', 'sidebar.php', 'style.css' );
    theme_dir = php_no_error(lambda: php_opendir(default_dir))
    if theme_dir:
        while True:
            theme_file = php_readdir(theme_dir)
            if not (theme_file != False):
                break
            # end if
            if php_is_dir(str(default_dir) + str("/") + str(theme_file)):
                continue
            # end if
            if (not copy(str(default_dir) + str("/") + str(theme_file), str(site_dir) + str("/") + str(theme_file))):
                return
            # end if
            chmod(str(site_dir) + str("/") + str(theme_file), 511)
        # end while
        php_closedir(theme_dir)
    # end if
    #// Rewrite the theme header.
    stylelines = php_explode("\n", php_implode("", file(str(site_dir) + str("/style.css"))))
    if stylelines:
        f = fopen(str(site_dir) + str("/style.css"), "w")
        for line in stylelines:
            if php_strpos(line, "Theme Name:") != False:
                line = "Theme Name: " + theme_name
            elif php_strpos(line, "Theme URI:") != False:
                line = "Theme URI: " + __get_option("url")
            elif php_strpos(line, "Description:") != False:
                line = "Description: Your theme."
            elif php_strpos(line, "Version:") != False:
                line = "Version: 1"
            elif php_strpos(line, "Author:") != False:
                line = "Author: You"
            # end if
            fwrite(f, line + "\n")
        # end for
        php_fclose(f)
    # end if
    #// Copy the images.
    umask(0)
    if (not mkdir(str(site_dir) + str("/images"), 511)):
        return False
    # end if
    images_dir = php_no_error(lambda: php_opendir(str(default_dir) + str("/images")))
    if images_dir:
        while True:
            image = php_readdir(images_dir)
            if not (image != False):
                break
            # end if
            if php_is_dir(str(default_dir) + str("/images/") + str(image)):
                continue
            # end if
            if (not copy(str(default_dir) + str("/images/") + str(image), str(site_dir) + str("/images/") + str(image))):
                return
            # end if
            chmod(str(site_dir) + str("/images/") + str(image), 511)
        # end while
        php_closedir(images_dir)
    # end if
# end def make_site_theme_from_default
#// 
#// Creates a site theme.
#// 
#// {@internal Missing Long Description}}
#// 
#// @since 1.5.0
#// 
#// @return string|false
#//
def make_site_theme(*args_):
    
    #// Name the theme after the blog.
    theme_name = __get_option("blogname")
    template = sanitize_title(theme_name)
    site_dir = WP_CONTENT_DIR + str("/themes/") + str(template)
    #// If the theme already exists, nothing to do.
    if php_is_dir(site_dir):
        return False
    # end if
    #// We must be able to write to the themes dir.
    if (not php_is_writable(WP_CONTENT_DIR + "/themes")):
        return False
    # end if
    umask(0)
    if (not mkdir(site_dir, 511)):
        return False
    # end if
    if php_file_exists(ABSPATH + "wp-layout.css"):
        if (not make_site_theme_from_oldschool(theme_name, template)):
            #// TODO: rm -rf the site theme directory.
            return False
        # end if
    else:
        if (not make_site_theme_from_default(theme_name, template)):
            #// TODO: rm -rf the site theme directory.
            return False
        # end if
    # end if
    #// Make the new site theme active.
    current_template = __get_option("template")
    if WP_DEFAULT_THEME == current_template:
        update_option("template", template)
        update_option("stylesheet", template)
    # end if
    return template
# end def make_site_theme
#// 
#// Translate user level to user role name.
#// 
#// @since 2.0.0
#// 
#// @param int $level User level.
#// @return string User role name.
#//
def translate_level_to_role(level=None, *args_):
    
    for case in Switch(level):
        if case(10):
            pass
        # end if
        if case(9):
            pass
        # end if
        if case(8):
            return "administrator"
        # end if
        if case(7):
            pass
        # end if
        if case(6):
            pass
        # end if
        if case(5):
            return "editor"
        # end if
        if case(4):
            pass
        # end if
        if case(3):
            pass
        # end if
        if case(2):
            return "author"
        # end if
        if case(1):
            return "contributor"
        # end if
        if case(0):
            pass
        # end if
        if case():
            return "subscriber"
        # end if
    # end for
# end def translate_level_to_role
#// 
#// Checks the version of the installed MySQL binary.
#// 
#// @since 2.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def wp_check_mysql_version(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    result = wpdb.check_database_version()
    if is_wp_error(result):
        wp_die(result)
    # end if
# end def wp_check_mysql_version
#// 
#// Disables the Automattic widgets plugin, which was merged into core.
#// 
#// @since 2.2.0
#//
def maybe_disable_automattic_widgets(*args_):
    
    plugins = __get_option("active_plugins")
    for plugin in plugins:
        if php_basename(plugin) == "widgets.php":
            array_splice(plugins, php_array_search(plugin, plugins), 1)
            update_option("active_plugins", plugins)
            break
        # end if
    # end for
# end def maybe_disable_automattic_widgets
#// 
#// Disables the Link Manager on upgrade if, at the time of upgrade, no links exist in the DB.
#// 
#// @since 3.5.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def maybe_disable_link_manager(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    if wp_current_db_version >= 22006 and get_option("link_manager_enabled") and (not wpdb.get_var(str("SELECT link_id FROM ") + str(wpdb.links) + str(" LIMIT 1"))):
        update_option("link_manager_enabled", 0)
    # end if
# end def maybe_disable_link_manager
#// 
#// Runs before the schema is upgraded.
#// 
#// @since 2.9.0
#// 
#// @global int  $wp_current_db_version The old (current) database version.
#// @global wpdb $wpdb                  WordPress database abstraction object.
#//
def pre_schema_upgrade(*args_):
    
    global wp_current_db_version,wpdb
    php_check_if_defined("wp_current_db_version","wpdb")
    #// Upgrade versions prior to 2.9.
    if wp_current_db_version < 11557:
        #// Delete duplicate options. Keep the option with the highest option_id.
        wpdb.query(str("DELETE o1 FROM ") + str(wpdb.options) + str(" AS o1 JOIN ") + str(wpdb.options) + str(" AS o2 USING (`option_name`) WHERE o2.option_id > o1.option_id"))
        #// Drop the old primary key and add the new.
        wpdb.query(str("ALTER TABLE ") + str(wpdb.options) + str(" DROP PRIMARY KEY, ADD PRIMARY KEY(option_id)"))
        #// Drop the old option_name index. dbDelta() doesn't do the drop.
        wpdb.query(str("ALTER TABLE ") + str(wpdb.options) + str(" DROP INDEX option_name"))
    # end if
    #// Multisite schema upgrades.
    if wp_current_db_version < 25448 and is_multisite() and wp_should_upgrade_global_tables():
        #// Upgrade versions prior to 3.7.
        if wp_current_db_version < 25179:
            #// New primary key for signups.
            wpdb.query(str("ALTER TABLE ") + str(wpdb.signups) + str(" ADD signup_id BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST"))
            wpdb.query(str("ALTER TABLE ") + str(wpdb.signups) + str(" DROP INDEX domain"))
        # end if
        if wp_current_db_version < 25448:
            #// Convert archived from enum to tinyint.
            wpdb.query(str("ALTER TABLE ") + str(wpdb.blogs) + str(" CHANGE COLUMN archived archived varchar(1) NOT NULL default '0'"))
            wpdb.query(str("ALTER TABLE ") + str(wpdb.blogs) + str(" CHANGE COLUMN archived archived tinyint(2) NOT NULL default 0"))
        # end if
    # end if
    #// Upgrade versions prior to 4.2.
    if wp_current_db_version < 31351:
        if (not is_multisite()) and wp_should_upgrade_global_tables():
            wpdb.query(str("ALTER TABLE ") + str(wpdb.usermeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
        # end if
        wpdb.query(str("ALTER TABLE ") + str(wpdb.terms) + str(" DROP INDEX slug, ADD INDEX slug(slug(191))"))
        wpdb.query(str("ALTER TABLE ") + str(wpdb.terms) + str(" DROP INDEX name, ADD INDEX name(name(191))"))
        wpdb.query(str("ALTER TABLE ") + str(wpdb.commentmeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
        wpdb.query(str("ALTER TABLE ") + str(wpdb.postmeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
        wpdb.query(str("ALTER TABLE ") + str(wpdb.posts) + str(" DROP INDEX post_name, ADD INDEX post_name(post_name(191))"))
    # end if
    #// Upgrade versions prior to 4.4.
    if wp_current_db_version < 34978:
        #// If compatible termmeta table is found, use it, but enforce a proper index and update collation.
        if wpdb.get_var(str("SHOW TABLES LIKE '") + str(wpdb.termmeta) + str("'")) and wpdb.get_results(str("SHOW INDEX FROM ") + str(wpdb.termmeta) + str(" WHERE Column_name = 'meta_key'")):
            wpdb.query(str("ALTER TABLE ") + str(wpdb.termmeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
            maybe_convert_table_to_utf8mb4(wpdb.termmeta)
        # end if
    # end if
# end def pre_schema_upgrade
if (not php_function_exists("install_global_terms")):
    #// 
    #// Install global terms.
    #// 
    #// @since 3.0.0
    #// 
    #// @global wpdb   $wpdb            WordPress database abstraction object.
    #// @global string $charset_collate
    #//
    def install_global_terms(*args_):
        
        global wpdb,charset_collate
        php_check_if_defined("wpdb","charset_collate")
        ms_queries = str("\nCREATE TABLE ") + str(wpdb.sitecategories) + str(""" (\n  cat_ID bigint(20) NOT NULL auto_increment,\n  cat_name varchar(55) NOT NULL default '',\n  category_nicename varchar(200) NOT NULL default '',\n  last_updated timestamp NOT NULL,\n  PRIMARY KEY  (cat_ID),\n  KEY category_nicename (category_nicename),\n  KEY last_updated (last_updated)\n) """) + str(charset_collate) + str(";\n")
        #// Now create tables.
        dbDelta(ms_queries)
    # end def install_global_terms
# end if
#// 
#// Determine if global tables should be upgraded.
#// 
#// This function performs a series of checks to ensure the environment allows
#// for the safe upgrading of global WordPress database tables. It is necessary
#// because global tables will commonly grow to millions of rows on large
#// installations, and the ability to control their upgrade routines can be
#// critical to the operation of large networks.
#// 
#// In a future iteration, this function may use `wp_is_large_network()` to more-
#// intelligently prevent global table upgrades. Until then, we make sure
#// WordPress is on the main site of the main network, to avoid running queries
#// more than once in multi-site or multi-network environments.
#// 
#// @since 4.3.0
#// 
#// @return bool Whether to run the upgrade routines on global tables.
#//
def wp_should_upgrade_global_tables(*args_):
    
    #// Return false early if explicitly not upgrading.
    if php_defined("DO_NOT_UPGRADE_GLOBAL_TABLES"):
        return False
    # end if
    #// Assume global tables should be upgraded.
    should_upgrade = True
    #// Set to false if not on main network (does not matter if not multi-network).
    if (not is_main_network()):
        should_upgrade = False
    # end if
    #// Set to false if not on main site of current network (does not matter if not multi-site).
    if (not is_main_site()):
        should_upgrade = False
    # end if
    #// 
    #// Filters if upgrade routines should be run on global tables.
    #// 
    #// @param bool $should_upgrade Whether to run the upgrade routines on global tables.
    #//
    return apply_filters("wp_should_upgrade_global_tables", should_upgrade)
# end def wp_should_upgrade_global_tables
