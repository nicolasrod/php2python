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
    def wp_install(blog_title_=None, user_name_=None, user_email_=None, public_=None, deprecated_="", user_password_="", language_="", *_args_):
        
        
        if (not php_empty(lambda : deprecated_)):
            _deprecated_argument(__FUNCTION__, "2.6.0")
        # end if
        wp_check_mysql_version()
        wp_cache_flush()
        make_db_current_silent()
        populate_options()
        populate_roles()
        update_option("blogname", blog_title_)
        update_option("admin_email", user_email_)
        update_option("blog_public", public_)
        #// Freshness of site - in the future, this could get more specific about actions taken, perhaps.
        update_option("fresh_site", 1)
        if language_:
            update_option("WPLANG", language_)
        # end if
        guessurl_ = wp_guess_url()
        update_option("siteurl", guessurl_)
        #// If not a public site, don't ping.
        if (not public_):
            update_option("default_pingback_flag", 0)
        # end if
        #// 
        #// Create default user. If the user already exists, the user tables are
        #// being shared among sites. Just set the role in that case.
        #//
        user_id_ = username_exists(user_name_)
        user_password_ = php_trim(user_password_)
        email_password_ = False
        user_created_ = False
        if (not user_id_) and php_empty(lambda : user_password_):
            user_password_ = wp_generate_password(12, False)
            message_ = __("<strong><em>Note that password</em></strong> carefully! It is a <em>random</em> password that was generated just for you.")
            user_id_ = wp_create_user(user_name_, user_password_, user_email_)
            update_user_option(user_id_, "default_password_nag", True, True)
            email_password_ = True
            user_created_ = True
        elif (not user_id_):
            #// Password has been provided.
            message_ = "<em>" + __("Your chosen password.") + "</em>"
            user_id_ = wp_create_user(user_name_, user_password_, user_email_)
            user_created_ = True
        else:
            message_ = __("User already exists. Password inherited.")
        # end if
        user_ = php_new_class("WP_User", lambda : WP_User(user_id_))
        user_.set_role("administrator")
        if user_created_:
            user_.user_url = guessurl_
            wp_update_user(user_)
        # end if
        wp_install_defaults(user_id_)
        wp_install_maybe_enable_pretty_permalinks()
        flush_rewrite_rules()
        wp_new_blog_notification(blog_title_, guessurl_, user_id_, user_password_ if email_password_ else __("The password you chose during installation."))
        wp_cache_flush()
        #// 
        #// Fires after a site is fully installed.
        #// 
        #// @since 3.9.0
        #// 
        #// @param WP_User $user The site owner.
        #//
        do_action("wp_install", user_)
        return Array({"url": guessurl_, "user_id": user_id_, "password": user_password_, "password_message": message_})
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
    def wp_install_defaults(user_id_=None, *_args_):
        
        
        global wpdb_
        global wp_rewrite_
        global table_prefix_
        php_check_if_defined("wpdb_","wp_rewrite_","table_prefix_")
        #// Default category.
        cat_name_ = __("Uncategorized")
        #// translators: Default category slug.
        cat_slug_ = sanitize_title(_x("Uncategorized", "Default category slug"))
        if global_terms_enabled():
            cat_id_ = wpdb_.get_var(wpdb_.prepare(str("SELECT cat_ID FROM ") + str(wpdb_.sitecategories) + str(" WHERE category_nicename = %s"), cat_slug_))
            if None == cat_id_:
                wpdb_.insert(wpdb_.sitecategories, Array({"cat_ID": 0, "cat_name": cat_name_, "category_nicename": cat_slug_, "last_updated": current_time("mysql", True)}))
                cat_id_ = wpdb_.insert_id
            # end if
            update_option("default_category", cat_id_)
        else:
            cat_id_ = 1
        # end if
        wpdb_.insert(wpdb_.terms, Array({"term_id": cat_id_, "name": cat_name_, "slug": cat_slug_, "term_group": 0}))
        wpdb_.insert(wpdb_.term_taxonomy, Array({"term_id": cat_id_, "taxonomy": "category", "description": "", "parent": 0, "count": 1}))
        cat_tt_id_ = wpdb_.insert_id
        #// First post.
        now_ = current_time("mysql")
        now_gmt_ = current_time("mysql", 1)
        first_post_guid_ = get_option("home") + "/?p=1"
        if is_multisite():
            first_post_ = get_site_option("first_post")
            if (not first_post_):
                first_post_ = "<!-- wp:paragraph -->\n<p>" + __("Welcome to %s. This is your first post. Edit or delete it, then start writing!") + "</p>\n<!-- /wp:paragraph -->"
            # end if
            first_post_ = php_sprintf(first_post_, php_sprintf("<a href=\"%s\">%s</a>", esc_url(network_home_url()), get_network().site_name))
            #// Back-compat for pre-4.4.
            first_post_ = php_str_replace("SITE_URL", esc_url(network_home_url()), first_post_)
            first_post_ = php_str_replace("SITE_NAME", get_network().site_name, first_post_)
        else:
            first_post_ = "<!-- wp:paragraph -->\n<p>" + __("Welcome to WordPress. This is your first post. Edit or delete it, then start writing!") + "</p>\n<!-- /wp:paragraph -->"
        # end if
        wpdb_.insert(wpdb_.posts, Array({"post_author": user_id_, "post_date": now_, "post_date_gmt": now_gmt_, "post_content": first_post_, "post_excerpt": "", "post_title": __("Hello world!"), "post_name": sanitize_title(_x("hello-world", "Default post slug")), "post_modified": now_, "post_modified_gmt": now_gmt_, "guid": first_post_guid_, "comment_count": 1, "to_ping": "", "pinged": "", "post_content_filtered": ""}))
        wpdb_.insert(wpdb_.term_relationships, Array({"term_taxonomy_id": cat_tt_id_, "object_id": 1}))
        #// Default comment.
        if is_multisite():
            first_comment_author_ = get_site_option("first_comment_author")
            first_comment_email_ = get_site_option("first_comment_email")
            first_comment_url_ = get_site_option("first_comment_url", network_home_url())
            first_comment_ = get_site_option("first_comment")
        # end if
        first_comment_author_ = first_comment_author_ if (not php_empty(lambda : first_comment_author_)) else __("A WordPress Commenter")
        first_comment_email_ = first_comment_email_ if (not php_empty(lambda : first_comment_email_)) else "wapuu@wordpress.example"
        first_comment_url_ = first_comment_url_ if (not php_empty(lambda : first_comment_url_)) else "https://wordpress.org/"
        first_comment_ = first_comment_ if (not php_empty(lambda : first_comment_)) else __("Hi, this is a comment.\nTo get started with moderating, editing, and deleting comments, please visit the Comments screen in the dashboard.\nCommenter avatars come from <a href=\"https://gravatar.com\">Gravatar</a>.")
        wpdb_.insert(wpdb_.comments, Array({"comment_post_ID": 1, "comment_author": first_comment_author_, "comment_author_email": first_comment_email_, "comment_author_url": first_comment_url_, "comment_date": now_, "comment_date_gmt": now_gmt_, "comment_content": first_comment_}))
        #// First page.
        if is_multisite():
            first_page_ = get_site_option("first_page")
        # end if
        if php_empty(lambda : first_page_):
            first_page_ = "<!-- wp:paragraph -->\n<p>"
            #// translators: First page content.
            first_page_ += __("This is an example page. It's different from a blog post because it will stay in one place and will show up in your site navigation (in most themes). Most people start with an About page that introduces them to potential site visitors. It might say something like this:")
            first_page_ += """</p>
            <!-- /wp:paragraph -->
            """
            first_page_ += "<!-- wp:quote -->\n<blockquote class=\"wp-block-quote\"><p>"
            #// translators: First page content.
            first_page_ += __("Hi there! I'm a bike messenger by day, aspiring actor by night, and this is my website. I live in Los Angeles, have a great dog named Jack, and I like pi&#241;a coladas. (And gettin' caught in the rain.)")
            first_page_ += """</p></blockquote>
            <!-- /wp:quote -->
            """
            first_page_ += "<!-- wp:paragraph -->\n<p>"
            #// translators: First page content.
            first_page_ += __("...or something like this:")
            first_page_ += """</p>
            <!-- /wp:paragraph -->
            """
            first_page_ += "<!-- wp:quote -->\n<blockquote class=\"wp-block-quote\"><p>"
            #// translators: First page content.
            first_page_ += __("The XYZ Doohickey Company was founded in 1971, and has been providing quality doohickeys to the public ever since. Located in Gotham City, XYZ employs over 2,000 people and does all kinds of awesome things for the Gotham community.")
            first_page_ += """</p></blockquote>
            <!-- /wp:quote -->
            """
            first_page_ += "<!-- wp:paragraph -->\n<p>"
            first_page_ += php_sprintf(__("As a new WordPress user, you should go to <a href=\"%s\">your dashboard</a> to delete this page and create new pages for your content. Have fun!"), admin_url())
            first_page_ += "</p>\n<!-- /wp:paragraph -->"
        # end if
        first_post_guid_ = get_option("home") + "/?page_id=2"
        wpdb_.insert(wpdb_.posts, Array({"post_author": user_id_, "post_date": now_, "post_date_gmt": now_gmt_, "post_content": first_page_, "post_excerpt": "", "comment_status": "closed", "post_title": __("Sample Page"), "post_name": __("sample-page"), "post_modified": now_, "post_modified_gmt": now_gmt_, "guid": first_post_guid_, "post_type": "page", "to_ping": "", "pinged": "", "post_content_filtered": ""}))
        wpdb_.insert(wpdb_.postmeta, Array({"post_id": 2, "meta_key": "_wp_page_template", "meta_value": "default"}))
        #// Privacy Policy page.
        if is_multisite():
            #// Disable by default unless the suggested content is provided.
            privacy_policy_content_ = get_site_option("default_privacy_policy_content")
        else:
            if (not php_class_exists("WP_Privacy_Policy_Content")):
                php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-policy-content.php", once=False)
            # end if
            privacy_policy_content_ = WP_Privacy_Policy_Content.get_default_content()
        # end if
        if (not php_empty(lambda : privacy_policy_content_)):
            privacy_policy_guid_ = get_option("home") + "/?page_id=3"
            wpdb_.insert(wpdb_.posts, Array({"post_author": user_id_, "post_date": now_, "post_date_gmt": now_gmt_, "post_content": privacy_policy_content_, "post_excerpt": "", "comment_status": "closed", "post_title": __("Privacy Policy"), "post_name": __("privacy-policy"), "post_modified": now_, "post_modified_gmt": now_gmt_, "guid": privacy_policy_guid_, "post_type": "page", "post_status": "draft", "to_ping": "", "pinged": "", "post_content_filtered": ""}))
            wpdb_.insert(wpdb_.postmeta, Array({"post_id": 3, "meta_key": "_wp_page_template", "meta_value": "default"}))
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
            update_user_meta(user_id_, "show_welcome_panel", 1)
        elif (not is_super_admin(user_id_)) and (not metadata_exists("user", user_id_, "show_welcome_panel")):
            update_user_meta(user_id_, "show_welcome_panel", 2)
        # end if
        if is_multisite():
            #// Flush rules to pick up the new page.
            wp_rewrite_.init()
            wp_rewrite_.flush_rules()
            user_ = php_new_class("WP_User", lambda : WP_User(user_id_))
            wpdb_.update(wpdb_.options, Array({"option_value": user_.user_email}), Array({"option_name": "admin_email"}))
            #// Remove all perms except for the login user.
            wpdb_.query(wpdb_.prepare(str("DELETE FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id != %d AND meta_key = %s"), user_id_, table_prefix_ + "user_level"))
            wpdb_.query(wpdb_.prepare(str("DELETE FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id != %d AND meta_key = %s"), user_id_, table_prefix_ + "capabilities"))
            #// Delete any caps that snuck into the previously active blog. (Hardcoded to blog 1 for now.)
            #// TODO: Get previous_blog_id.
            if (not is_super_admin(user_id_)) and 1 != user_id_:
                wpdb_.delete(wpdb_.usermeta, Array({"user_id": user_id_, "meta_key": wpdb_.base_prefix + "1_capabilities"}))
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
def wp_install_maybe_enable_pretty_permalinks(*_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
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
    permalink_structures_ = Array("/%year%/%monthnum%/%day%/%postname%/", "/index.php/%year%/%monthnum%/%day%/%postname%/")
    for permalink_structure_ in permalink_structures_:
        wp_rewrite_.set_permalink_structure(permalink_structure_)
        #// 
        #// Flush rules with the hard option to force refresh of the web-server's
        #// rewrite config file (e.g. .htaccess or web.config).
        #//
        wp_rewrite_.flush_rules(True)
        test_url_ = ""
        #// Test against a real WordPress post.
        first_post_ = get_page_by_path(sanitize_title(_x("hello-world", "Default post slug")), OBJECT, "post")
        if first_post_:
            test_url_ = get_permalink(first_post_.ID)
        # end if
        #// 
        #// Send a request to the site, and check whether
        #// the 'x-pingback' header is returned as expected.
        #// 
        #// Uses wp_remote_get() instead of wp_remote_head() because web servers
        #// can block head requests.
        #//
        response_ = wp_remote_get(test_url_, Array({"timeout": 5}))
        x_pingback_header_ = wp_remote_retrieve_header(response_, "x-pingback")
        pretty_permalinks_ = x_pingback_header_ and get_bloginfo("pingback_url") == x_pingback_header_
        if pretty_permalinks_:
            return True
        # end if
    # end for
    #// 
    #// If it makes it this far, pretty permalinks failed.
    #// Fallback to query-string permalinks.
    #//
    wp_rewrite_.set_permalink_structure("")
    wp_rewrite_.flush_rules(True)
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
    def wp_new_blog_notification(blog_title_=None, blog_url_=None, user_id_=None, password_=None, *_args_):
        
        
        user_ = php_new_class("WP_User", lambda : WP_User(user_id_))
        email_ = user_.user_email
        name_ = user_.user_login
        login_url_ = wp_login_url()
        message_ = php_sprintf(__("""Your new WordPress site has been successfully set up at:
        %1$s
        You can log in to the administrator account with the following information:
        Username: %2$s
        Password: %3$s
        Log in here: %4$s
        We hope you enjoy your new site. Thanks!
        --The WordPress Team
        https://wordpress.org/
        """), blog_url_, name_, password_, login_url_)
        wp_mail(email_, __("New WordPress Site"), message_)
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
    def wp_upgrade(*_args_):
        
        
        global wp_current_db_version_
        global wp_db_version_
        global wpdb_
        php_check_if_defined("wp_current_db_version_","wp_db_version_","wpdb_")
        wp_current_db_version_ = __get_option("db_version")
        #// We are up to date. Nothing to do.
        if wp_db_version_ == wp_current_db_version_:
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
            update_site_meta(get_current_blog_id(), "db_version", wp_db_version_)
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
        do_action("wp_upgrade", wp_db_version_, wp_current_db_version_)
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
def upgrade_all(*_args_):
    
    
    global wp_current_db_version_
    global wp_db_version_
    php_check_if_defined("wp_current_db_version_","wp_db_version_")
    wp_current_db_version_ = __get_option("db_version")
    #// We are up to date. Nothing to do.
    if wp_db_version_ == wp_current_db_version_:
        return
    # end if
    #// If the version is not set in the DB, try to guess the version.
    if php_empty(lambda : wp_current_db_version_):
        wp_current_db_version_ = 0
        #// If the template option exists, we have 1.5.
        template_ = __get_option("template")
        if (not php_empty(lambda : template_)):
            wp_current_db_version_ = 2541
        # end if
    # end if
    if wp_current_db_version_ < 6039:
        upgrade_230_options_table()
    # end if
    populate_options()
    if wp_current_db_version_ < 2541:
        upgrade_100()
        upgrade_101()
        upgrade_110()
        upgrade_130()
    # end if
    if wp_current_db_version_ < 3308:
        upgrade_160()
    # end if
    if wp_current_db_version_ < 4772:
        upgrade_210()
    # end if
    if wp_current_db_version_ < 4351:
        upgrade_old_slugs()
    # end if
    if wp_current_db_version_ < 5539:
        upgrade_230()
    # end if
    if wp_current_db_version_ < 6124:
        upgrade_230_old_tables()
    # end if
    if wp_current_db_version_ < 7499:
        upgrade_250()
    # end if
    if wp_current_db_version_ < 7935:
        upgrade_252()
    # end if
    if wp_current_db_version_ < 8201:
        upgrade_260()
    # end if
    if wp_current_db_version_ < 8989:
        upgrade_270()
    # end if
    if wp_current_db_version_ < 10360:
        upgrade_280()
    # end if
    if wp_current_db_version_ < 11958:
        upgrade_290()
    # end if
    if wp_current_db_version_ < 15260:
        upgrade_300()
    # end if
    if wp_current_db_version_ < 19389:
        upgrade_330()
    # end if
    if wp_current_db_version_ < 20080:
        upgrade_340()
    # end if
    if wp_current_db_version_ < 22422:
        upgrade_350()
    # end if
    if wp_current_db_version_ < 25824:
        upgrade_370()
    # end if
    if wp_current_db_version_ < 26148:
        upgrade_372()
    # end if
    if wp_current_db_version_ < 26691:
        upgrade_380()
    # end if
    if wp_current_db_version_ < 29630:
        upgrade_400()
    # end if
    if wp_current_db_version_ < 33055:
        upgrade_430()
    # end if
    if wp_current_db_version_ < 33056:
        upgrade_431()
    # end if
    if wp_current_db_version_ < 35700:
        upgrade_440()
    # end if
    if wp_current_db_version_ < 36686:
        upgrade_450()
    # end if
    if wp_current_db_version_ < 37965:
        upgrade_460()
    # end if
    if wp_current_db_version_ < 44719:
        upgrade_510()
    # end if
    if wp_current_db_version_ < 45744:
        upgrade_530()
    # end if
    maybe_disable_link_manager()
    maybe_disable_automattic_widgets()
    update_option("db_version", wp_db_version_)
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
def upgrade_100(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Get the title and ID of every post, post_name to check if it already has a value.
    posts_ = wpdb_.get_results(str("SELECT ID, post_title, post_name FROM ") + str(wpdb_.posts) + str(" WHERE post_name = ''"))
    if posts_:
        for post_ in posts_:
            if "" == post_.post_name:
                newtitle_ = sanitize_title(post_.post_title)
                wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_name = %s WHERE ID = %d"), newtitle_, post_.ID))
            # end if
        # end for
    # end if
    categories_ = wpdb_.get_results(str("SELECT cat_ID, cat_name, category_nicename FROM ") + str(wpdb_.categories))
    for category_ in categories_:
        if "" == category_.category_nicename:
            newtitle_ = sanitize_title(category_.cat_name)
            wpdb_.update(wpdb_.categories, Array({"category_nicename": newtitle_}), Array({"cat_ID": category_.cat_ID}))
        # end if
    # end for
    sql_ = str("UPDATE ") + str(wpdb_.options) + str("""\n      SET option_value = REPLACE(option_value, 'wp-links/links-images/', 'wp-images/links/')\n        WHERE option_name LIKE %s\n     AND option_value LIKE %s""")
    wpdb_.query(wpdb_.prepare(sql_, wpdb_.esc_like("links_rating_image") + "%", wpdb_.esc_like("wp-links/links-images/") + "%"))
    done_ids_ = wpdb_.get_results(str("SELECT DISTINCT post_id FROM ") + str(wpdb_.post2cat))
    if done_ids_:
        done_posts_ = Array()
        for done_id_ in done_ids_:
            done_posts_[-1] = done_id_.post_id
        # end for
        catwhere_ = " AND ID NOT IN (" + php_implode(",", done_posts_) + ")"
    else:
        catwhere_ = ""
    # end if
    allposts_ = wpdb_.get_results(str("SELECT ID, post_category FROM ") + str(wpdb_.posts) + str(" WHERE post_category != '0' ") + str(catwhere_))
    if allposts_:
        for post_ in allposts_:
            #// Check to see if it's already been imported.
            cat_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.post2cat) + str(" WHERE post_id = %d AND category_id = %d"), post_.ID, post_.post_category))
            if (not cat_) and 0 != post_.post_category:
                #// If there's no result.
                wpdb_.insert(wpdb_.post2cat, Array({"post_id": post_.ID, "category_id": post_.post_category}))
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
def upgrade_101(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Clean up indices, add a few.
    add_clean_index(wpdb_.posts, "post_name")
    add_clean_index(wpdb_.posts, "post_status")
    add_clean_index(wpdb_.categories, "category_nicename")
    add_clean_index(wpdb_.comments, "comment_approved")
    add_clean_index(wpdb_.comments, "comment_post_ID")
    add_clean_index(wpdb_.links, "link_category")
    add_clean_index(wpdb_.links, "link_visible")
# end def upgrade_101
#// 
#// Execute changes made in WordPress 1.2.
#// 
#// @ignore
#// @since 1.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_110(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Set user_nicename.
    users_ = wpdb_.get_results(str("SELECT ID, user_nickname, user_nicename FROM ") + str(wpdb_.users))
    for user_ in users_:
        if "" == user_.user_nicename:
            newname_ = sanitize_title(user_.user_nickname)
            wpdb_.update(wpdb_.users, Array({"user_nicename": newname_}), Array({"ID": user_.ID}))
        # end if
    # end for
    users_ = wpdb_.get_results(str("SELECT ID, user_pass from ") + str(wpdb_.users))
    for row_ in users_:
        if (not php_preg_match("/^[A-Fa-f0-9]{32}$/", row_.user_pass)):
            wpdb_.update(wpdb_.users, Array({"user_pass": php_md5(row_.user_pass)}), Array({"ID": row_.ID}))
        # end if
    # end for
    #// Get the GMT offset, we'll use that later on.
    all_options_ = get_alloptions_110()
    time_difference_ = all_options_.time_difference
    server_time_ = time() + gmdate("Z")
    weblogger_time_ = server_time_ + time_difference_ * HOUR_IN_SECONDS
    gmt_time_ = time()
    diff_gmt_server_ = gmt_time_ - server_time_ / HOUR_IN_SECONDS
    diff_weblogger_server_ = weblogger_time_ - server_time_ / HOUR_IN_SECONDS
    diff_gmt_weblogger_ = diff_gmt_server_ - diff_weblogger_server_
    gmt_offset_ = -diff_gmt_weblogger_
    #// Add a gmt_offset option, with value $gmt_offset.
    add_option("gmt_offset", gmt_offset_)
    #// 
    #// Check if we already set the GMT fields. If we did, then
    #// MAX(post_date_gmt) can't be '0000-00-00 00:00:00'.
    #// <michel_v> I just slapped myself silly for not thinking about it earlier.
    #//
    got_gmt_fields_ = (not wpdb_.get_var(str("SELECT MAX(post_date_gmt) FROM ") + str(wpdb_.posts)) == "0000-00-00 00:00:00")
    if (not got_gmt_fields_):
        #// Add or subtract time to all dates, to get GMT dates.
        add_hours_ = php_intval(diff_gmt_weblogger_)
        add_minutes_ = php_intval(60 * diff_gmt_weblogger_ - add_hours_)
        wpdb_.query(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_date_gmt = DATE_ADD(post_date, INTERVAL '") + str(add_hours_) + str(":") + str(add_minutes_) + str("' HOUR_MINUTE)"))
        wpdb_.query(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_modified = post_date"))
        wpdb_.query(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_modified_gmt = DATE_ADD(post_modified, INTERVAL '") + str(add_hours_) + str(":") + str(add_minutes_) + str("' HOUR_MINUTE) WHERE post_modified != '0000-00-00 00:00:00'"))
        wpdb_.query(str("UPDATE ") + str(wpdb_.comments) + str(" SET comment_date_gmt = DATE_ADD(comment_date, INTERVAL '") + str(add_hours_) + str(":") + str(add_minutes_) + str("' HOUR_MINUTE)"))
        wpdb_.query(str("UPDATE ") + str(wpdb_.users) + str(" SET user_registered = DATE_ADD(user_registered, INTERVAL '") + str(add_hours_) + str(":") + str(add_minutes_) + str("' HOUR_MINUTE)"))
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
def upgrade_130(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// Remove extraneous backslashes.
    posts_ = wpdb_.get_results(str("SELECT ID, post_title, post_content, post_excerpt, guid, post_date, post_name, post_status, post_author FROM ") + str(wpdb_.posts))
    if posts_:
        for post_ in posts_:
            post_content_ = addslashes(deslash(post_.post_content))
            post_title_ = addslashes(deslash(post_.post_title))
            post_excerpt_ = addslashes(deslash(post_.post_excerpt))
            if php_empty(lambda : post_.guid):
                guid_ = get_permalink(post_.ID)
            else:
                guid_ = post_.guid
            # end if
            wpdb_.update(wpdb_.posts, php_compact("post_title_", "post_content_", "post_excerpt_", "guid_"), Array({"ID": post_.ID}))
        # end for
    # end if
    #// Remove extraneous backslashes.
    comments_ = wpdb_.get_results(str("SELECT comment_ID, comment_author, comment_content FROM ") + str(wpdb_.comments))
    if comments_:
        for comment_ in comments_:
            comment_content_ = deslash(comment_.comment_content)
            comment_author_ = deslash(comment_.comment_author)
            wpdb_.update(wpdb_.comments, php_compact("comment_content_", "comment_author_"), Array({"comment_ID": comment_.comment_ID}))
        # end for
    # end if
    #// Remove extraneous backslashes.
    links_ = wpdb_.get_results(str("SELECT link_id, link_name, link_description FROM ") + str(wpdb_.links))
    if links_:
        for link_ in links_:
            link_name_ = deslash(link_.link_name)
            link_description_ = deslash(link_.link_description)
            wpdb_.update(wpdb_.links, php_compact("link_name_", "link_description_"), Array({"link_id": link_.link_id}))
        # end for
    # end if
    active_plugins_ = __get_option("active_plugins")
    #// 
    #// If plugins are not stored in an array, they're stored in the old
    #// newline separated format. Convert to new format.
    #//
    if (not php_is_array(active_plugins_)):
        active_plugins_ = php_explode("\n", php_trim(active_plugins_))
        update_option("active_plugins", active_plugins_)
    # end if
    #// Obsolete tables.
    wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "optionvalues")
    wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "optiontypes")
    wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "optiongroups")
    wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "optiongroup_options")
    #// Update comments table to use comment_type.
    wpdb_.query(str("UPDATE ") + str(wpdb_.comments) + str(" SET comment_type='trackback', comment_content = REPLACE(comment_content, '<trackback />', '') WHERE comment_content LIKE '<trackback />%'"))
    wpdb_.query(str("UPDATE ") + str(wpdb_.comments) + str(" SET comment_type='pingback', comment_content = REPLACE(comment_content, '<pingback />', '') WHERE comment_content LIKE '<pingback />%'"))
    #// Some versions have multiple duplicate option_name rows with the same values.
    options_ = wpdb_.get_results(str("SELECT option_name, COUNT(option_name) AS dupes FROM `") + str(wpdb_.options) + str("` GROUP BY option_name"))
    for option_ in options_:
        if 1 != option_.dupes:
            #// Could this be done in the query?
            limit_ = option_.dupes - 1
            dupe_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT option_id FROM ") + str(wpdb_.options) + str(" WHERE option_name = %s LIMIT %d"), option_.option_name, limit_))
            if dupe_ids_:
                dupe_ids_ = join(",", dupe_ids_)
                wpdb_.query(str("DELETE FROM ") + str(wpdb_.options) + str(" WHERE option_id IN (") + str(dupe_ids_) + str(")"))
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
def upgrade_160(*_args_):
    
    
    global wpdb_
    global wp_current_db_version_
    php_check_if_defined("wpdb_","wp_current_db_version_")
    populate_roles_160()
    users_ = wpdb_.get_results(str("SELECT * FROM ") + str(wpdb_.users))
    for user_ in users_:
        if (not php_empty(lambda : user_.user_firstname)):
            update_user_meta(user_.ID, "first_name", wp_slash(user_.user_firstname))
        # end if
        if (not php_empty(lambda : user_.user_lastname)):
            update_user_meta(user_.ID, "last_name", wp_slash(user_.user_lastname))
        # end if
        if (not php_empty(lambda : user_.user_nickname)):
            update_user_meta(user_.ID, "nickname", wp_slash(user_.user_nickname))
        # end if
        if (not php_empty(lambda : user_.user_level)):
            update_user_meta(user_.ID, wpdb_.prefix + "user_level", user_.user_level)
        # end if
        if (not php_empty(lambda : user_.user_icq)):
            update_user_meta(user_.ID, "icq", wp_slash(user_.user_icq))
        # end if
        if (not php_empty(lambda : user_.user_aim)):
            update_user_meta(user_.ID, "aim", wp_slash(user_.user_aim))
        # end if
        if (not php_empty(lambda : user_.user_msn)):
            update_user_meta(user_.ID, "msn", wp_slash(user_.user_msn))
        # end if
        if (not php_empty(lambda : user_.user_yim)):
            update_user_meta(user_.ID, "yim", wp_slash(user_.user_icq))
        # end if
        if (not php_empty(lambda : user_.user_description)):
            update_user_meta(user_.ID, "description", wp_slash(user_.user_description))
        # end if
        if (php_isset(lambda : user_.user_idmode)):
            idmode_ = user_.user_idmode
            if "nickname" == idmode_:
                id_ = user_.user_nickname
            # end if
            if "login" == idmode_:
                id_ = user_.user_login
            # end if
            if "firstname" == idmode_:
                id_ = user_.user_firstname
            # end if
            if "lastname" == idmode_:
                id_ = user_.user_lastname
            # end if
            if "namefl" == idmode_:
                id_ = user_.user_firstname + " " + user_.user_lastname
            # end if
            if "namelf" == idmode_:
                id_ = user_.user_lastname + " " + user_.user_firstname
            # end if
            if (not idmode_):
                id_ = user_.user_nickname
            # end if
            wpdb_.update(wpdb_.users, Array({"display_name": id_}), Array({"ID": user_.ID}))
        # end if
        #// FIXME: RESET_CAPS is temporary code to reset roles and caps if flag is set.
        caps_ = get_user_meta(user_.ID, wpdb_.prefix + "capabilities")
        if php_empty(lambda : caps_) or php_defined("RESET_CAPS"):
            level_ = get_user_meta(user_.ID, wpdb_.prefix + "user_level", True)
            role_ = translate_level_to_role(level_)
            update_user_meta(user_.ID, wpdb_.prefix + "capabilities", Array({role_: True}))
        # end if
    # end for
    old_user_fields_ = Array("user_firstname", "user_lastname", "user_icq", "user_aim", "user_msn", "user_yim", "user_idmode", "user_ip", "user_domain", "user_browser", "user_description", "user_nickname", "user_level")
    wpdb_.hide_errors()
    for old_ in old_user_fields_:
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.users) + str(" DROP ") + str(old_))
    # end for
    wpdb_.show_errors()
    #// Populate comment_count field of posts table.
    comments_ = wpdb_.get_results(str("SELECT comment_post_ID, COUNT(*) as c FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = '1' GROUP BY comment_post_ID"))
    if php_is_array(comments_):
        for comment_ in comments_:
            wpdb_.update(wpdb_.posts, Array({"comment_count": comment_.c}), Array({"ID": comment_.comment_post_ID}))
        # end for
    # end if
    #// 
    #// Some alpha versions used a post status of object instead of attachment
    #// and put the mime type in post_type instead of post_mime_type.
    #//
    if wp_current_db_version_ > 2541 and wp_current_db_version_ <= 3091:
        objects_ = wpdb_.get_results(str("SELECT ID, post_type FROM ") + str(wpdb_.posts) + str(" WHERE post_status = 'object'"))
        for object_ in objects_:
            wpdb_.update(wpdb_.posts, Array({"post_status": "attachment", "post_mime_type": object_.post_type, "post_type": ""}), Array({"ID": object_.ID}))
            meta_ = get_post_meta(object_.ID, "imagedata", True)
            if (not php_empty(lambda : meta_["file"])):
                update_attached_file(object_.ID, meta_["file"])
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
def upgrade_210(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 3506:
        #// Update status and type.
        posts_ = wpdb_.get_results(str("SELECT ID, post_status FROM ") + str(wpdb_.posts))
        if (not php_empty(lambda : posts_)):
            for post_ in posts_:
                status_ = post_.post_status
                type_ = "post"
                if "static" == status_:
                    status_ = "publish"
                    type_ = "page"
                elif "attachment" == status_:
                    status_ = "inherit"
                    type_ = "attachment"
                # end if
                wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_status = %s, post_type = %s WHERE ID = %d"), status_, type_, post_.ID))
            # end for
        # end if
    # end if
    if wp_current_db_version_ < 3845:
        populate_roles_210()
    # end if
    if wp_current_db_version_ < 3531:
        #// Give future posts a post_status of future.
        now_ = gmdate("Y-m-d H:i:59")
        wpdb_.query(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_status = 'future' WHERE post_status = 'publish' AND post_date_gmt > '") + str(now_) + str("'"))
        posts_ = wpdb_.get_results(str("SELECT ID, post_date FROM ") + str(wpdb_.posts) + str(" WHERE post_status ='future'"))
        if (not php_empty(lambda : posts_)):
            for post_ in posts_:
                wp_schedule_single_event(mysql2date("U", post_.post_date, False), "publish_future_post", Array(post_.ID))
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
def upgrade_230(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 5200:
        populate_roles_230()
    # end if
    #// Convert categories to terms.
    tt_ids_ = Array()
    have_tags_ = False
    categories_ = wpdb_.get_results(str("SELECT * FROM ") + str(wpdb_.categories) + str(" ORDER BY cat_ID"))
    for category_ in categories_:
        term_id_ = php_int(category_.cat_ID)
        name_ = category_.cat_name
        description_ = category_.category_description
        slug_ = category_.category_nicename
        parent_ = category_.category_parent
        term_group_ = 0
        #// Associate terms with the same slug in a term group and make slugs unique.
        exists_ = wpdb_.get_results(wpdb_.prepare(str("SELECT term_id, term_group FROM ") + str(wpdb_.terms) + str(" WHERE slug = %s"), slug_))
        if exists_:
            term_group_ = exists_[0].term_group
            id_ = exists_[0].term_id
            num_ = 2
            while True:
                alt_slug_ = slug_ + str("-") + str(num_)
                num_ += 1
                slug_check_ = wpdb_.get_var(wpdb_.prepare(str("SELECT slug FROM ") + str(wpdb_.terms) + str(" WHERE slug = %s"), alt_slug_))
                
                if slug_check_:
                    break
                # end if
            # end while
            slug_ = alt_slug_
            if php_empty(lambda : term_group_):
                term_group_ = wpdb_.get_var(str("SELECT MAX(term_group) FROM ") + str(wpdb_.terms) + str(" GROUP BY term_group")) + 1
                wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.terms) + str(" SET term_group = %d WHERE term_id = %d"), term_group_, id_))
            # end if
        # end if
        wpdb_.query(wpdb_.prepare(str("INSERT INTO ") + str(wpdb_.terms) + str(" (term_id, name, slug, term_group) VALUES\n     (%d, %s, %s, %d)"), term_id_, name_, slug_, term_group_))
        count_ = 0
        if (not php_empty(lambda : category_.category_count)):
            count_ = php_int(category_.category_count)
            taxonomy_ = "category"
            wpdb_.query(wpdb_.prepare(str("INSERT INTO ") + str(wpdb_.term_taxonomy) + str(" (term_id, taxonomy, description, parent, count) VALUES ( %d, %s, %s, %d, %d)"), term_id_, taxonomy_, description_, parent_, count_))
            tt_ids_[term_id_][taxonomy_] = php_int(wpdb_.insert_id)
        # end if
        if (not php_empty(lambda : category_.link_count)):
            count_ = php_int(category_.link_count)
            taxonomy_ = "link_category"
            wpdb_.query(wpdb_.prepare(str("INSERT INTO ") + str(wpdb_.term_taxonomy) + str(" (term_id, taxonomy, description, parent, count) VALUES ( %d, %s, %s, %d, %d)"), term_id_, taxonomy_, description_, parent_, count_))
            tt_ids_[term_id_][taxonomy_] = php_int(wpdb_.insert_id)
        # end if
        if (not php_empty(lambda : category_.tag_count)):
            have_tags_ = True
            count_ = php_int(category_.tag_count)
            taxonomy_ = "post_tag"
            wpdb_.insert(wpdb_.term_taxonomy, php_compact("term_id_", "taxonomy_", "description_", "parent_", "count_"))
            tt_ids_[term_id_][taxonomy_] = php_int(wpdb_.insert_id)
        # end if
        if php_empty(lambda : count_):
            count_ = 0
            taxonomy_ = "category"
            wpdb_.insert(wpdb_.term_taxonomy, php_compact("term_id_", "taxonomy_", "description_", "parent_", "count_"))
            tt_ids_[term_id_][taxonomy_] = php_int(wpdb_.insert_id)
        # end if
    # end for
    select_ = "post_id, category_id"
    if have_tags_:
        select_ += ", rel_type"
    # end if
    posts_ = wpdb_.get_results(str("SELECT ") + str(select_) + str(" FROM ") + str(wpdb_.post2cat) + str(" GROUP BY post_id, category_id"))
    for post_ in posts_:
        post_id_ = php_int(post_.post_id)
        term_id_ = php_int(post_.category_id)
        taxonomy_ = "category"
        if (not php_empty(lambda : post_.rel_type)) and "tag" == post_.rel_type:
            taxonomy_ = "tag"
        # end if
        tt_id_ = tt_ids_[term_id_][taxonomy_]
        if php_empty(lambda : tt_id_):
            continue
        # end if
        wpdb_.insert(wpdb_.term_relationships, Array({"object_id": post_id_, "term_taxonomy_id": tt_id_}))
    # end for
    #// < 3570 we used linkcategories. >= 3570 we used categories and link2cat.
    if wp_current_db_version_ < 3570:
        #// 
        #// Create link_category terms for link categories. Create a map of link
        #// category IDs to link_category terms.
        #//
        link_cat_id_map_ = Array()
        default_link_cat_ = 0
        tt_ids_ = Array()
        link_cats_ = wpdb_.get_results("SELECT cat_id, cat_name FROM " + wpdb_.prefix + "linkcategories")
        for category_ in link_cats_:
            cat_id_ = php_int(category_.cat_id)
            term_id_ = 0
            name_ = wp_slash(category_.cat_name)
            slug_ = sanitize_title(name_)
            term_group_ = 0
            #// Associate terms with the same slug in a term group and make slugs unique.
            exists_ = wpdb_.get_results(wpdb_.prepare(str("SELECT term_id, term_group FROM ") + str(wpdb_.terms) + str(" WHERE slug = %s"), slug_))
            if exists_:
                term_group_ = exists_[0].term_group
                term_id_ = exists_[0].term_id
            # end if
            if php_empty(lambda : term_id_):
                wpdb_.insert(wpdb_.terms, php_compact("name_", "slug_", "term_group_"))
                term_id_ = php_int(wpdb_.insert_id)
            # end if
            link_cat_id_map_[cat_id_] = term_id_
            default_link_cat_ = term_id_
            wpdb_.insert(wpdb_.term_taxonomy, Array({"term_id": term_id_, "taxonomy": "link_category", "description": "", "parent": 0, "count": 0}))
            tt_ids_[term_id_] = php_int(wpdb_.insert_id)
        # end for
        #// Associate links to categories.
        links_ = wpdb_.get_results(str("SELECT link_id, link_category FROM ") + str(wpdb_.links))
        if (not php_empty(lambda : links_)):
            for link_ in links_:
                if 0 == link_.link_category:
                    continue
                # end if
                if (not (php_isset(lambda : link_cat_id_map_[link_.link_category]))):
                    continue
                # end if
                term_id_ = link_cat_id_map_[link_.link_category]
                tt_id_ = tt_ids_[term_id_]
                if php_empty(lambda : tt_id_):
                    continue
                # end if
                wpdb_.insert(wpdb_.term_relationships, Array({"object_id": link_.link_id, "term_taxonomy_id": tt_id_}))
            # end for
        # end if
        #// Set default to the last category we grabbed during the upgrade loop.
        update_option("default_link_category", default_link_cat_)
    else:
        links_ = wpdb_.get_results(str("SELECT link_id, category_id FROM ") + str(wpdb_.link2cat) + str(" GROUP BY link_id, category_id"))
        for link_ in links_:
            link_id_ = php_int(link_.link_id)
            term_id_ = php_int(link_.category_id)
            taxonomy_ = "link_category"
            tt_id_ = tt_ids_[term_id_][taxonomy_]
            if php_empty(lambda : tt_id_):
                continue
            # end if
            wpdb_.insert(wpdb_.term_relationships, Array({"object_id": link_id_, "term_taxonomy_id": tt_id_}))
        # end for
    # end if
    if wp_current_db_version_ < 4772:
        #// Obsolete linkcategories table.
        wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "linkcategories")
    # end if
    #// Recalculate all counts.
    terms_ = wpdb_.get_results(str("SELECT term_taxonomy_id, taxonomy FROM ") + str(wpdb_.term_taxonomy))
    for term_ in terms_:
        if "post_tag" == term_.taxonomy or "category" == term_.taxonomy:
            count_ = wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_relationships) + str(", ") + str(wpdb_.posts) + str(" WHERE ") + str(wpdb_.posts) + str(".ID = ") + str(wpdb_.term_relationships) + str(".object_id AND post_status = 'publish' AND post_type = 'post' AND term_taxonomy_id = %d"), term_.term_taxonomy_id))
        else:
            count_ = wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_relationships) + str(" WHERE term_taxonomy_id = %d"), term_.term_taxonomy_id))
        # end if
        wpdb_.update(wpdb_.term_taxonomy, Array({"count": count_}), Array({"term_taxonomy_id": term_.term_taxonomy_id}))
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
def upgrade_230_options_table(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    old_options_fields_ = Array("option_can_override", "option_type", "option_width", "option_height", "option_description", "option_admin_level")
    wpdb_.hide_errors()
    for old_ in old_options_fields_:
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.options) + str(" DROP ") + str(old_))
    # end for
    wpdb_.show_errors()
# end def upgrade_230_options_table
#// 
#// Remove old categories, link2cat, and post2cat database tables.
#// 
#// @ignore
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_230_old_tables(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "categories")
    wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "link2cat")
    wpdb_.query("DROP TABLE IF EXISTS " + wpdb_.prefix + "post2cat")
# end def upgrade_230_old_tables
#// 
#// Upgrade old slugs made in version 2.2.
#// 
#// @ignore
#// @since 2.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def upgrade_old_slugs(*_args_):
    
    
    #// Upgrade people who were using the Redirect Old Slugs plugin.
    global wpdb_
    php_check_if_defined("wpdb_")
    wpdb_.query(str("UPDATE ") + str(wpdb_.postmeta) + str(" SET meta_key = '_wp_old_slug' WHERE meta_key = 'old_slug'"))
# end def upgrade_old_slugs
#// 
#// Execute changes made in WordPress 2.5.0.
#// 
#// @ignore
#// @since 2.5.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_250(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    if wp_current_db_version_ < 6689:
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
def upgrade_252(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    wpdb_.query(str("UPDATE ") + str(wpdb_.users) + str(" SET user_activation_key = ''"))
# end def upgrade_252
#// 
#// Execute changes made in WordPress 2.6.
#// 
#// @ignore
#// @since 2.6.0
#// 
#// @global int $wp_current_db_version The old (current) database version.
#//
def upgrade_260(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    if wp_current_db_version_ < 8000:
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
def upgrade_270(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 8980:
        populate_roles_270()
    # end if
    #// Update post_date for unpublished posts with empty timestamp.
    if wp_current_db_version_ < 8921:
        wpdb_.query(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_date = post_modified WHERE post_date = '0000-00-00 00:00:00'"))
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
def upgrade_280(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 10360:
        populate_roles_280()
    # end if
    if is_multisite():
        start_ = 0
        while True:
            rows_ = wpdb_.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb_.options) + str(" ORDER BY option_id LIMIT ") + str(start_) + str(", 20"))
            if not (rows_):
                break
            # end if
            for row_ in rows_:
                value_ = row_.option_value
                if (not php_no_error(lambda: unserialize(value_))):
                    value_ = stripslashes(value_)
                # end if
                if value_ != row_.option_value:
                    update_option(row_.option_name, value_)
                # end if
            # end for
            start_ += 20
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
def upgrade_290(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    if wp_current_db_version_ < 11958:
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
def upgrade_300(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 15093:
        populate_roles_300()
    # end if
    if wp_current_db_version_ < 14139 and is_multisite() and is_main_site() and (not php_defined("MULTISITE")) and get_site_option("siteurl") == False:
        add_site_option("siteurl", "")
    # end if
    #// 3.0 screen options key name changes.
    if wp_should_upgrade_global_tables():
        sql_ = str("DELETE FROM ") + str(wpdb_.usermeta) + str("""\n            WHERE meta_key LIKE %s\n            OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key LIKE %s\n           OR meta_key = 'manageedittagscolumnshidden'\n           OR meta_key = 'managecategoriescolumnshidden'\n         OR meta_key = 'manageedit-tagscolumnshidden'\n          OR meta_key = 'manageeditcolumnshidden'\n           OR meta_key = 'categories_per_page'\n           OR meta_key = 'edit_tags_per_page'""")
        prefix_ = wpdb_.esc_like(wpdb_.base_prefix)
        wpdb_.query(wpdb_.prepare(sql_, prefix_ + "%" + wpdb_.esc_like("meta-box-hidden") + "%", prefix_ + "%" + wpdb_.esc_like("closedpostboxes") + "%", prefix_ + "%" + wpdb_.esc_like("manage-") + "%" + wpdb_.esc_like("-columns-hidden") + "%", prefix_ + "%" + wpdb_.esc_like("meta-box-order") + "%", prefix_ + "%" + wpdb_.esc_like("metaboxorder") + "%", prefix_ + "%" + wpdb_.esc_like("screen_layout") + "%"))
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
def upgrade_330(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    global wp_registered_widgets_
    global sidebars_widgets_
    php_check_if_defined("wp_current_db_version_","wpdb_","wp_registered_widgets_","sidebars_widgets_")
    if wp_current_db_version_ < 19061 and wp_should_upgrade_global_tables():
        wpdb_.query(str("DELETE FROM ") + str(wpdb_.usermeta) + str(" WHERE meta_key IN ('show_admin_bar_admin', 'plugins_last_view')"))
    # end if
    if wp_current_db_version_ >= 11548:
        return
    # end if
    sidebars_widgets_ = get_option("sidebars_widgets", Array())
    _sidebars_widgets_ = Array()
    if (php_isset(lambda : sidebars_widgets_["wp_inactive_widgets"])) or php_empty(lambda : sidebars_widgets_):
        sidebars_widgets_["array_version"] = 3
    elif (not (php_isset(lambda : sidebars_widgets_["array_version"]))):
        sidebars_widgets_["array_version"] = 1
    # end if
    for case in Switch(sidebars_widgets_["array_version"]):
        if case(1):
            for index_,sidebar_ in sidebars_widgets_:
                if php_is_array(sidebar_):
                    for i_,name_ in sidebar_:
                        id_ = php_strtolower(name_)
                        if (php_isset(lambda : wp_registered_widgets_[id_])):
                            _sidebars_widgets_[index_][i_] = id_
                            continue
                        # end if
                        id_ = sanitize_title(name_)
                        if (php_isset(lambda : wp_registered_widgets_[id_])):
                            _sidebars_widgets_[index_][i_] = id_
                            continue
                        # end if
                        found_ = False
                        for widget_id_,widget_ in wp_registered_widgets_:
                            if php_strtolower(widget_["name"]) == php_strtolower(name_):
                                _sidebars_widgets_[index_][i_] = widget_["id"]
                                found_ = True
                                break
                            elif sanitize_title(widget_["name"]) == sanitize_title(name_):
                                _sidebars_widgets_[index_][i_] = widget_["id"]
                                found_ = True
                                break
                            # end if
                        # end for
                        if found_:
                            continue
                        # end if
                        _sidebars_widgets_[index_][i_] = None
                    # end for
                # end if
            # end for
            _sidebars_widgets_["array_version"] = 2
            sidebars_widgets_ = _sidebars_widgets_
            _sidebars_widgets_ = None
        # end if
        if case(2):
            sidebars_widgets_ = retrieve_widgets()
            sidebars_widgets_["array_version"] = 3
            update_option("sidebars_widgets", sidebars_widgets_)
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
def upgrade_340(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 19798:
        wpdb_.hide_errors()
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.options) + str(" DROP COLUMN blog_id"))
        wpdb_.show_errors()
    # end if
    if wp_current_db_version_ < 19799:
        wpdb_.hide_errors()
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.comments) + str(" DROP INDEX comment_approved"))
        wpdb_.show_errors()
    # end if
    if wp_current_db_version_ < 20022 and wp_should_upgrade_global_tables():
        wpdb_.query(str("DELETE FROM ") + str(wpdb_.usermeta) + str(" WHERE meta_key = 'themes_last_view'"))
    # end if
    if wp_current_db_version_ < 20080:
        if "yes" == wpdb_.get_var(str("SELECT autoload FROM ") + str(wpdb_.options) + str(" WHERE option_name = 'uninstall_plugins'")):
            uninstall_plugins_ = get_option("uninstall_plugins")
            delete_option("uninstall_plugins")
            add_option("uninstall_plugins", uninstall_plugins_, None, "no")
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
def upgrade_350(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 22006 and wpdb_.get_var(str("SELECT link_id FROM ") + str(wpdb_.links) + str(" LIMIT 1")):
        update_option("link_manager_enabled", 1)
        pass
    # end if
    if wp_current_db_version_ < 21811 and wp_should_upgrade_global_tables():
        meta_keys_ = Array()
        for name_ in php_array_merge(get_post_types(), get_taxonomies()):
            if False != php_strpos(name_, "-"):
                meta_keys_[-1] = "edit_" + php_str_replace("-", "_", name_) + "_per_page"
            # end if
        # end for
        if meta_keys_:
            meta_keys_ = php_implode("', '", meta_keys_)
            wpdb_.query(str("DELETE FROM ") + str(wpdb_.usermeta) + str(" WHERE meta_key IN ('") + str(meta_keys_) + str("')"))
        # end if
    # end if
    if wp_current_db_version_ < 22422:
        term_ = get_term_by("slug", "post-format-standard", "post_format")
        if term_:
            wp_delete_term(term_.term_id, "post_format")
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
def upgrade_370(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    if wp_current_db_version_ < 25824:
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
def upgrade_372(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    if wp_current_db_version_ < 26148:
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
def upgrade_380(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    if wp_current_db_version_ < 26691:
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
def upgrade_400(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    if wp_current_db_version_ < 29630:
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
def upgrade_420(*_args_):
    
    
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
def upgrade_430(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 32364:
        upgrade_430_fix_comments()
    # end if
    #// Shared terms are split in a separate process.
    if wp_current_db_version_ < 32814:
        update_option("finished_splitting_shared_terms", 0)
        wp_schedule_single_event(time() + 1 * MINUTE_IN_SECONDS, "wp_split_shared_term_batch")
    # end if
    if wp_current_db_version_ < 33055 and "utf8mb4" == wpdb_.charset:
        if is_multisite():
            tables_ = wpdb_.tables("blog")
        else:
            tables_ = wpdb_.tables("all")
            if (not wp_should_upgrade_global_tables()):
                global_tables_ = wpdb_.tables("global")
                tables_ = php_array_diff_assoc(tables_, global_tables_)
            # end if
        # end if
        for table_ in tables_:
            maybe_convert_table_to_utf8mb4(table_)
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
def upgrade_430_fix_comments(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    content_length_ = wpdb_.get_col_length(wpdb_.comments, "comment_content")
    if is_wp_error(content_length_):
        return
    # end if
    if False == content_length_:
        content_length_ = Array({"type": "byte", "length": 65535})
    elif (not php_is_array(content_length_)):
        length_ = php_int(content_length_) if php_int(content_length_) > 0 else 65535
        content_length_ = Array({"type": "byte", "length": length_})
    # end if
    if "byte" != content_length_["type"] or 0 == content_length_["length"]:
        #// Sites with malformed DB schemas are on their own.
        return
    # end if
    allowed_length_ = php_intval(content_length_["length"]) - 10
    comments_ = wpdb_.get_results(str("SELECT `comment_ID` FROM `") + str(wpdb_.comments) + str("`\n            WHERE `comment_date_gmt` > '2015-04-26'\n           AND LENGTH( `comment_content` ) >= ") + str(allowed_length_) + str("\n          AND ( `comment_content` LIKE '%<%' OR `comment_content` LIKE '%>%' )"))
    for comment_ in comments_:
        wp_delete_comment(comment_.comment_ID, True)
    # end for
# end def upgrade_430_fix_comments
#// 
#// Executes changes made in WordPress 4.3.1.
#// 
#// @ignore
#// @since 4.3.1
#//
def upgrade_431(*_args_):
    
    
    #// Fix incorrect cron entries for term splitting.
    cron_array_ = _get_cron_array()
    if (php_isset(lambda : cron_array_["wp_batch_split_terms"])):
        cron_array_["wp_batch_split_terms"] = None
        _set_cron_array(cron_array_)
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
def upgrade_440(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 34030:
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.options) + str(" MODIFY option_name VARCHAR(191)"))
    # end if
    #// Remove the unused 'add_users' role.
    roles_ = wp_roles()
    for role_ in roles_.role_objects:
        if role_.has_cap("add_users"):
            role_.remove_cap("add_users")
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
def upgrade_450(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ < 36180:
        wp_clear_scheduled_hook("wp_maybe_auto_update")
    # end if
    #// Remove unused email confirmation options, moved to usermeta.
    if wp_current_db_version_ < 36679 and is_multisite():
        wpdb_.query(str("DELETE FROM ") + str(wpdb_.options) + str(" WHERE option_name REGEXP '^[0-9]+_new_email$'"))
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
def upgrade_460(*_args_):
    
    
    global wp_current_db_version_
    php_check_if_defined("wp_current_db_version_")
    #// Remove unused post meta.
    if wp_current_db_version_ < 37854:
        delete_post_meta_by_key("_post_restored_from")
    # end if
    #// Remove plugins with callback as an array object/method as the uninstall hook, see #13786.
    if wp_current_db_version_ < 37965:
        uninstall_plugins_ = get_option("uninstall_plugins", Array())
        if (not php_empty(lambda : uninstall_plugins_)):
            for basename_,callback_ in uninstall_plugins_:
                if php_is_array(callback_) and php_is_object(callback_[0]):
                    uninstall_plugins_[basename_] = None
                # end if
            # end for
            update_option("uninstall_plugins", uninstall_plugins_)
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
def upgrade_500(*_args_):
    
    
    pass
# end def upgrade_500
#// 
#// Executes changes made in WordPress 5.1.0.
#// 
#// @ignore
#// @since 5.1.0
#//
def upgrade_510(*_args_):
    
    
    delete_site_option("upgrade_500_was_gutenberg_active")
# end def upgrade_510
#// 
#// Executes changes made in WordPress 5.3.0.
#// 
#// @ignore
#// @since 5.3.0
#//
def upgrade_530(*_args_):
    
    
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
def upgrade_network(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    #// Always clear expired transients.
    delete_expired_transients(True)
    #// 2.8
    if wp_current_db_version_ < 11549:
        wpmu_sitewide_plugins_ = get_site_option("wpmu_sitewide_plugins")
        active_sitewide_plugins_ = get_site_option("active_sitewide_plugins")
        if wpmu_sitewide_plugins_:
            if (not active_sitewide_plugins_):
                sitewide_plugins_ = wpmu_sitewide_plugins_
            else:
                sitewide_plugins_ = php_array_merge(active_sitewide_plugins_, wpmu_sitewide_plugins_)
            # end if
            update_site_option("active_sitewide_plugins", sitewide_plugins_)
        # end if
        delete_site_option("wpmu_sitewide_plugins")
        delete_site_option("deactivated_sitewide_plugins")
        start_ = 0
        while True:
            rows_ = wpdb_.get_results(str("SELECT meta_key, meta_value FROM ") + str(wpdb_.sitemeta) + str(" ORDER BY meta_id LIMIT ") + str(start_) + str(", 20"))
            if not (rows_):
                break
            # end if
            for row_ in rows_:
                value_ = row_.meta_value
                if (not php_no_error(lambda: unserialize(value_))):
                    value_ = stripslashes(value_)
                # end if
                if value_ != row_.meta_value:
                    update_site_option(row_.meta_key, value_)
                # end if
            # end for
            start_ += 20
        # end while
    # end if
    #// 3.0
    if wp_current_db_version_ < 13576:
        update_site_option("global_terms_enabled", "1")
    # end if
    #// 3.3
    if wp_current_db_version_ < 19390:
        update_site_option("initial_db_version", wp_current_db_version_)
    # end if
    if wp_current_db_version_ < 19470:
        if False == get_site_option("active_sitewide_plugins"):
            update_site_option("active_sitewide_plugins", Array())
        # end if
    # end if
    #// 3.4
    if wp_current_db_version_ < 20148:
        #// 'allowedthemes' keys things by stylesheet. 'allowed_themes' keyed things by name.
        allowedthemes_ = get_site_option("allowedthemes")
        allowed_themes_ = get_site_option("allowed_themes")
        if False == allowedthemes_ and php_is_array(allowed_themes_) and allowed_themes_:
            converted_ = Array()
            themes_ = wp_get_themes()
            for stylesheet_,theme_data_ in themes_:
                if (php_isset(lambda : allowed_themes_[theme_data_.get("Name")])):
                    converted_[stylesheet_] = True
                # end if
            # end for
            update_site_option("allowedthemes", converted_)
            delete_site_option("allowed_themes")
        # end if
    # end if
    #// 3.5
    if wp_current_db_version_ < 21823:
        update_site_option("ms_files_rewriting", "1")
    # end if
    #// 3.5.2
    if wp_current_db_version_ < 24448:
        illegal_names_ = get_site_option("illegal_names")
        if php_is_array(illegal_names_) and php_count(illegal_names_) == 1:
            illegal_name_ = reset(illegal_names_)
            illegal_names_ = php_explode(" ", illegal_name_)
            update_site_option("illegal_names", illegal_names_)
        # end if
    # end if
    #// 4.2
    if wp_current_db_version_ < 31351 and "utf8mb4" == wpdb_.charset:
        if wp_should_upgrade_global_tables():
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.usermeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.site) + str(" DROP INDEX domain, ADD INDEX domain(domain(140),path(51))"))
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.sitemeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.signups) + str(" DROP INDEX domain_path, ADD INDEX domain_path(domain(140),path(51))"))
            tables_ = wpdb_.tables("global")
            #// sitecategories may not exist.
            if (not wpdb_.get_var(str("SHOW TABLES LIKE '") + str(tables_["sitecategories"]) + str("'"))):
                tables_["sitecategories"] = None
            # end if
            for table_ in tables_:
                maybe_convert_table_to_utf8mb4(table_)
            # end for
        # end if
    # end if
    #// 4.3
    if wp_current_db_version_ < 33055 and "utf8mb4" == wpdb_.charset:
        if wp_should_upgrade_global_tables():
            upgrade_ = False
            indexes_ = wpdb_.get_results(str("SHOW INDEXES FROM ") + str(wpdb_.signups))
            for index_ in indexes_:
                if "domain_path" == index_.Key_name and "domain" == index_.Column_name and 140 != index_.Sub_part:
                    upgrade_ = True
                    break
                # end if
            # end for
            if upgrade_:
                wpdb_.query(str("ALTER TABLE ") + str(wpdb_.signups) + str(" DROP INDEX domain_path, ADD INDEX domain_path(domain(140),path(51))"))
            # end if
            tables_ = wpdb_.tables("global")
            #// sitecategories may not exist.
            if (not wpdb_.get_var(str("SHOW TABLES LIKE '") + str(tables_["sitecategories"]) + str("'"))):
                tables_["sitecategories"] = None
            # end if
            for table_ in tables_:
                maybe_convert_table_to_utf8mb4(table_)
            # end for
        # end if
    # end if
    #// 5.1
    if wp_current_db_version_ < 44467:
        network_id_ = get_main_network_id()
        delete_network_option(network_id_, "site_meta_supported")
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
def maybe_create_table(table_name_=None, create_ddl_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    query_ = wpdb_.prepare("SHOW TABLES LIKE %s", wpdb_.esc_like(table_name_))
    if wpdb_.get_var(query_) == table_name_:
        return True
    # end if
    #// Didn't find it, so try to create it.
    wpdb_.query(create_ddl_)
    #// We cannot directly tell that whether this succeeded!
    if wpdb_.get_var(query_) == table_name_:
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
def drop_index(table_=None, index_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    wpdb_.hide_errors()
    wpdb_.query(str("ALTER TABLE `") + str(table_) + str("` DROP INDEX `") + str(index_) + str("`"))
    #// Now we need to take out all the extra ones we may have created.
    i_ = 0
    while i_ < 25:
        
        wpdb_.query(str("ALTER TABLE `") + str(table_) + str("` DROP INDEX `") + str(index_) + str("_") + str(i_) + str("`"))
        i_ += 1
    # end while
    wpdb_.show_errors()
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
def add_clean_index(table_=None, index_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    drop_index(table_, index_)
    wpdb_.query(str("ALTER TABLE `") + str(table_) + str("` ADD INDEX ( `") + str(index_) + str("` )"))
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
def maybe_add_column(table_name_=None, column_name_=None, create_ddl_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    for column_ in wpdb_.get_col(str("DESC ") + str(table_name_), 0):
        if column_ == column_name_:
            return True
        # end if
    # end for
    #// Didn't find it, so try to create it.
    wpdb_.query(create_ddl_)
    #// We cannot directly tell that whether this succeeded!
    for column_ in wpdb_.get_col(str("DESC ") + str(table_name_), 0):
        if column_ == column_name_:
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
def maybe_convert_table_to_utf8mb4(table_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    results_ = wpdb_.get_results(str("SHOW FULL COLUMNS FROM `") + str(table_) + str("`"))
    if (not results_):
        return False
    # end if
    for column_ in results_:
        if column_.Collation:
            charset_ = php_explode("_", column_.Collation)
            charset_ = php_strtolower(charset_)
            if "utf8" != charset_ and "utf8mb4" != charset_:
                #// Don't upgrade tables that have non-utf8 columns.
                return False
            # end if
        # end if
    # end for
    table_details_ = wpdb_.get_row(str("SHOW TABLE STATUS LIKE '") + str(table_) + str("'"))
    if (not table_details_):
        return False
    # end if
    table_charset_ = php_explode("_", table_details_.Collation)
    table_charset_ = php_strtolower(table_charset_)
    if "utf8mb4" == table_charset_:
        return True
    # end if
    return wpdb_.query(str("ALTER TABLE ") + str(table_) + str(" CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
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
def get_alloptions_110(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    all_options_ = php_new_class("stdClass", lambda : stdClass())
    options_ = wpdb_.get_results(str("SELECT option_name, option_value FROM ") + str(wpdb_.options))
    if options_:
        for option_ in options_:
            if "siteurl" == option_.option_name or "home" == option_.option_name or "category_base" == option_.option_name:
                option_.option_value = untrailingslashit(option_.option_value)
            # end if
            all_options_.option_.option_name = stripslashes(option_.option_value)
        # end for
    # end if
    return all_options_
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
def __get_option(setting_=None, *_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    global wpdb_
    php_check_if_defined("wpdb_")
    if "home" == setting_ and php_defined("WP_HOME"):
        return untrailingslashit(WP_HOME)
    # end if
    if "siteurl" == setting_ and php_defined("WP_SITEURL"):
        return untrailingslashit(WP_SITEURL)
    # end if
    option_ = wpdb_.get_var(wpdb_.prepare(str("SELECT option_value FROM ") + str(wpdb_.options) + str(" WHERE option_name = %s"), setting_))
    if "home" == setting_ and "" == option_:
        return __get_option("siteurl")
    # end if
    if "siteurl" == setting_ or "home" == setting_ or "category_base" == setting_ or "tag_base" == setting_:
        option_ = untrailingslashit(option_)
    # end if
    return maybe_unserialize(option_)
# end def __get_option
#// 
#// Filters for content to remove unnecessary slashes.
#// 
#// @since 1.5.0
#// 
#// @param string $content The content to modify.
#// @return string The de-slashed content.
#//
def deslash(content_=None, *_args_):
    
    
    #// Note: \\\ inside a regex denotes a single backslash.
    #// 
    #// Replace one or more backslashes followed by a single quote with
    #// a single quote.
    #//
    content_ = php_preg_replace("/\\\\+'/", "'", content_)
    #// 
    #// Replace one or more backslashes followed by a double quote with
    #// a double quote.
    #//
    content_ = php_preg_replace("/\\\\+\"/", "\"", content_)
    #// Replace one or more backslashes with one backslash.
    content_ = php_preg_replace("/\\\\+/", "\\", content_)
    return content_
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
def dbDelta(queries_="", execute_=None, *_args_):
    if execute_ is None:
        execute_ = True
    # end if
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_in_array(queries_, Array("", "all", "blog", "global", "ms_global"), True):
        queries_ = wp_get_db_schema(queries_)
    # end if
    #// Separate individual queries into an array.
    if (not php_is_array(queries_)):
        queries_ = php_explode(";", queries_)
        queries_ = php_array_filter(queries_)
    # end if
    #// 
    #// Filters the dbDelta SQL queries.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[] $queries An array of dbDelta SQL queries.
    #//
    queries_ = apply_filters("dbdelta_queries", queries_)
    cqueries_ = Array()
    #// Creation queries.
    iqueries_ = Array()
    #// Insertion queries.
    for_update_ = Array()
    #// Create a tablename index for an array ($cqueries) of queries.
    for qry_ in queries_:
        if php_preg_match("|CREATE TABLE ([^ ]*)|", qry_, matches_):
            cqueries_[php_trim(matches_[1], "`")] = qry_
            for_update_[matches_[1]] = "Created table " + matches_[1]
        elif php_preg_match("|CREATE DATABASE ([^ ]*)|", qry_, matches_):
            array_unshift(cqueries_, qry_)
        elif php_preg_match("|INSERT INTO ([^ ]*)|", qry_, matches_):
            iqueries_[-1] = qry_
        elif php_preg_match("|UPDATE ([^ ]*)|", qry_, matches_):
            iqueries_[-1] = qry_
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
    cqueries_ = apply_filters("dbdelta_create_queries", cqueries_)
    #// 
    #// Filters the dbDelta SQL queries for inserting or updating.
    #// 
    #// Queries filterable via this hook contain "INSERT INTO" or "UPDATE".
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[] $iqueries An array of dbDelta insert or update SQL queries.
    #//
    iqueries_ = apply_filters("dbdelta_insert_queries", iqueries_)
    text_fields_ = Array("tinytext", "text", "mediumtext", "longtext")
    blob_fields_ = Array("tinyblob", "blob", "mediumblob", "longblob")
    global_tables_ = wpdb_.tables("global")
    for table_,qry_ in cqueries_:
        #// Upgrade global tables only for the main site. Don't upgrade at all if conditions are not optimal.
        if php_in_array(table_, global_tables_) and (not wp_should_upgrade_global_tables()):
            cqueries_[table_] = None
            for_update_[table_] = None
            continue
        # end if
        #// Fetch the table column structure from the database.
        suppress_ = wpdb_.suppress_errors()
        tablefields_ = wpdb_.get_results(str("DESCRIBE ") + str(table_) + str(";"))
        wpdb_.suppress_errors(suppress_)
        if (not tablefields_):
            continue
        # end if
        #// Clear the field and index arrays.
        cfields_ = Array()
        indices_ = Array()
        indices_without_subparts_ = Array()
        #// Get all of the field names in the query from between the parentheses.
        php_preg_match("|\\((.*)\\)|ms", qry_, match2_)
        qryline_ = php_trim(match2_[1])
        #// Separate field lines into an array.
        flds_ = php_explode("\n", qryline_)
        #// For every field line specified in the query.
        for fld_ in flds_:
            fld_ = php_trim(fld_, "     \n\r ,")
            #// Default trim characters, plus ','.
            #// Extract the field name.
            php_preg_match("|^([^ ]*)|", fld_, fvals_)
            fieldname_ = php_trim(fvals_[1], "`")
            fieldname_lowercased_ = php_strtolower(fieldname_)
            #// Verify the found field name.
            validfield_ = True
            for case in Switch(fieldname_lowercased_):
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
                    validfield_ = False
                    #// 
                    #// Normalize the index definition.
                    #// 
                    #// This is done so the definition can be compared against the result of a
                    #// `SHOW INDEX FROM $table_name` query which returns the current table
                    #// index information.
                    #// 
                    #// Extract type, name and columns from the definition.
                    #// phpcs:disable Squiz.Strings.ConcatenationSpacing.PaddingFound -- don't remove regex indentation
                    php_preg_match("/^" + "(?P<index_type>" + "PRIMARY\\s+KEY|(?:UNIQUE|FULLTEXT|SPATIAL)\\s+(?:KEY|INDEX)|KEY|INDEX" + ")" + "\\s+" + "(?:" + "`?" + "(?P<index_name>" + "(?:[0-9a-zA-Z$_-]|[\\xC2-\\xDF][\\x80-\\xBF])+" + ")" + "`?" + "\\s+" + ")*" + "\\(" + "(?P<index_columns>" + ".+?" + ")" + "\\)" + "$/im", fld_, index_matches_)
                    #// phpcs:enable
                    #// Uppercase the index type and normalize space characters.
                    index_type_ = php_strtoupper(php_preg_replace("/\\s+/", " ", php_trim(index_matches_["index_type"])))
                    #// 'INDEX' is a synonym for 'KEY', standardize on 'KEY'.
                    index_type_ = php_str_replace("INDEX", "KEY", index_type_)
                    #// Escape the index name with backticks. An index for a primary key has no name.
                    index_name_ = "" if "PRIMARY KEY" == index_type_ else "`" + php_strtolower(index_matches_["index_name"]) + "`"
                    #// Parse the columns. Multiple columns are separated by a comma.
                    index_columns_ = php_array_map("trim", php_explode(",", index_matches_["index_columns"]))
                    index_columns_without_subparts_ = index_columns_
                    #// Normalize columns.
                    for id_,index_column_ in index_columns_:
                        #// Extract column name and number of indexed characters (sub_part).
                        php_preg_match("/" + "`?" + "(?P<column_name>" + "(?:[0-9a-zA-Z$_-]|[\\xC2-\\xDF][\\x80-\\xBF])+" + ")" + "`?" + "(?:" + "\\s*" + "\\(" + "\\s*" + "(?P<sub_part>" + "\\d+" + ")" + "\\s*" + "\\)" + ")?" + "/", index_column_, index_column_matches_)
                        #// Escape the column name with backticks.
                        index_column_ = "`" + index_column_matches_["column_name"] + "`"
                        #// We don't need to add the subpart to $index_columns_without_subparts
                        index_columns_without_subparts_[id_] = index_column_
                        #// Append the optional sup part with the number of indexed characters.
                        if (php_isset(lambda : index_column_matches_["sub_part"])):
                            index_column_ += "(" + index_column_matches_["sub_part"] + ")"
                        # end if
                    # end for
                    #// Build the normalized index definition and add it to the list of indices.
                    indices_[-1] = str(index_type_) + str(" ") + str(index_name_) + str(" (") + php_implode(",", index_columns_) + ")"
                    indices_without_subparts_[-1] = str(index_type_) + str(" ") + str(index_name_) + str(" (") + php_implode(",", index_columns_without_subparts_) + ")"
                    index_column_ = None
                    index_column_matches_ = None
                    index_matches_ = None
                    index_type_ = None
                    index_name_ = None
                    index_columns_ = None
                    index_columns_without_subparts_ = None
                    break
                # end if
            # end for
            #// If it's a valid field, add it to the field array.
            if validfield_:
                cfields_[fieldname_lowercased_] = fld_
            # end if
        # end for
        #// For every field in the table.
        for tablefield_ in tablefields_:
            tablefield_field_lowercased_ = php_strtolower(tablefield_.Field)
            tablefield_type_lowercased_ = php_strtolower(tablefield_.Type)
            #// If the table field exists in the field array...
            if php_array_key_exists(tablefield_field_lowercased_, cfields_):
                #// Get the field type from the query.
                php_preg_match("|`?" + tablefield_.Field + "`? ([^ ]*( unsigned)?)|i", cfields_[tablefield_field_lowercased_], matches_)
                fieldtype_ = matches_[1]
                fieldtype_lowercased_ = php_strtolower(fieldtype_)
                #// Is actual field type different from the field type in query?
                if tablefield_.Type != fieldtype_:
                    do_change_ = True
                    if php_in_array(fieldtype_lowercased_, text_fields_) and php_in_array(tablefield_type_lowercased_, text_fields_):
                        if php_array_search(fieldtype_lowercased_, text_fields_) < php_array_search(tablefield_type_lowercased_, text_fields_):
                            do_change_ = False
                        # end if
                    # end if
                    if php_in_array(fieldtype_lowercased_, blob_fields_) and php_in_array(tablefield_type_lowercased_, blob_fields_):
                        if php_array_search(fieldtype_lowercased_, blob_fields_) < php_array_search(tablefield_type_lowercased_, blob_fields_):
                            do_change_ = False
                        # end if
                    # end if
                    if do_change_:
                        #// Add a query to change the column type.
                        cqueries_[-1] = str("ALTER TABLE ") + str(table_) + str(" CHANGE COLUMN `") + str(tablefield_.Field) + str("` ") + cfields_[tablefield_field_lowercased_]
                        for_update_[table_ + "." + tablefield_.Field] = str("Changed type of ") + str(table_) + str(".") + str(tablefield_.Field) + str(" from ") + str(tablefield_.Type) + str(" to ") + str(fieldtype_)
                    # end if
                # end if
                #// Get the default value from the array.
                if php_preg_match("| DEFAULT '(.*?)'|i", cfields_[tablefield_field_lowercased_], matches_):
                    default_value_ = matches_[1]
                    if tablefield_.Default != default_value_:
                        #// Add a query to change the column's default value
                        cqueries_[-1] = str("ALTER TABLE ") + str(table_) + str(" ALTER COLUMN `") + str(tablefield_.Field) + str("` SET DEFAULT '") + str(default_value_) + str("'")
                        for_update_[table_ + "." + tablefield_.Field] = str("Changed default value of ") + str(table_) + str(".") + str(tablefield_.Field) + str(" from ") + str(tablefield_.Default) + str(" to ") + str(default_value_)
                    # end if
                # end if
                cfields_[tablefield_field_lowercased_] = None
            else:
                pass
            # end if
        # end for
        #// For every remaining field specified for the table.
        for fieldname_,fielddef_ in cfields_:
            #// Push a query line into $cqueries that adds the field to that table.
            cqueries_[-1] = str("ALTER TABLE ") + str(table_) + str(" ADD COLUMN ") + str(fielddef_)
            for_update_[table_ + "." + fieldname_] = "Added column " + table_ + "." + fieldname_
        # end for
        #// Index stuff goes here. Fetch the table index structure from the database.
        tableindices_ = wpdb_.get_results(str("SHOW INDEX FROM ") + str(table_) + str(";"))
        if tableindices_:
            #// Clear the index array.
            index_ary_ = Array()
            #// For every index in the table.
            for tableindex_ in tableindices_:
                keyname_ = php_strtolower(tableindex_.Key_name)
                #// Add the index to the index data array.
                index_ary_[keyname_]["columns"][-1] = Array({"fieldname": tableindex_.Column_name, "subpart": tableindex_.Sub_part})
                index_ary_[keyname_]["unique"] = True if 0 == tableindex_.Non_unique else False
                index_ary_[keyname_]["index_type"] = tableindex_.Index_type
            # end for
            #// For each actual index in the index array.
            for index_name_,index_data_ in index_ary_:
                #// Build a create string to compare to the query.
                index_string_ = ""
                if "primary" == index_name_:
                    index_string_ += "PRIMARY "
                elif index_data_["unique"]:
                    index_string_ += "UNIQUE "
                # end if
                if "FULLTEXT" == php_strtoupper(index_data_["index_type"]):
                    index_string_ += "FULLTEXT "
                # end if
                if "SPATIAL" == php_strtoupper(index_data_["index_type"]):
                    index_string_ += "SPATIAL "
                # end if
                index_string_ += "KEY "
                if "primary" != index_name_:
                    index_string_ += "`" + index_name_ + "`"
                # end if
                index_columns_ = ""
                #// For each column in the index.
                for column_data_ in index_data_["columns"]:
                    if "" != index_columns_:
                        index_columns_ += ","
                    # end if
                    #// Add the field to the column list string.
                    index_columns_ += "`" + column_data_["fieldname"] + "`"
                # end for
                #// Add the column list to the index create string.
                index_string_ += str(" (") + str(index_columns_) + str(")")
                #// Check if the index definition exists, ignoring subparts.
                aindex_ = php_array_search(index_string_, indices_without_subparts_)
                if False != aindex_:
                    indices_without_subparts_[aindex_] = None
                    indices_[aindex_] = None
                # end if
            # end for
        # end if
        #// For every remaining index specified for the table.
        for index_ in indices_:
            #// Push a query line into $cqueries that adds the index to that table.
            cqueries_[-1] = str("ALTER TABLE ") + str(table_) + str(" ADD ") + str(index_)
            for_update_[-1] = "Added index " + table_ + " " + index_
        # end for
        cqueries_[table_] = None
        for_update_[table_] = None
    # end for
    allqueries_ = php_array_merge(cqueries_, iqueries_)
    if execute_:
        for query_ in allqueries_:
            wpdb_.query(query_)
        # end for
    # end if
    return for_update_
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
def make_db_current(tables_="all", *_args_):
    
    
    alterations_ = dbDelta(tables_)
    php_print("<ol>\n")
    for alteration_ in alterations_:
        php_print(str("<li>") + str(alteration_) + str("</li>\n"))
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
def make_db_current_silent(tables_="all", *_args_):
    
    
    dbDelta(tables_)
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
def make_site_theme_from_oldschool(theme_name_=None, template_=None, *_args_):
    
    
    home_path_ = get_home_path()
    site_dir_ = WP_CONTENT_DIR + str("/themes/") + str(template_)
    if (not php_file_exists(str(home_path_) + str("/index.php"))):
        return False
    # end if
    #// 
    #// Copy files from the old locations to the site theme.
    #// TODO: This does not copy arbitrary include dependencies. Only the standard WP files are copied.
    #//
    files_ = Array({"index.php": "index.php", "wp-layout.css": "style.css", "wp-comments.php": "comments.php", "wp-comments-popup.php": "comments-popup.php"})
    for oldfile_,newfile_ in files_:
        if "index.php" == oldfile_:
            oldpath_ = home_path_
        else:
            oldpath_ = ABSPATH
        # end if
        #// Check to make sure it's not a new index.
        if "index.php" == oldfile_:
            index_ = php_implode("", file(str(oldpath_) + str("/") + str(oldfile_)))
            if php_strpos(index_, "WP_USE_THEMES") != False:
                if (not copy(WP_CONTENT_DIR + "/themes/" + WP_DEFAULT_THEME + "/index.php", str(site_dir_) + str("/") + str(newfile_))):
                    return False
                # end if
                continue
            # end if
        # end if
        if (not copy(str(oldpath_) + str("/") + str(oldfile_), str(site_dir_) + str("/") + str(newfile_))):
            return False
        # end if
        chmod(str(site_dir_) + str("/") + str(newfile_), 511)
        #// Update the blog header include in each file.
        lines_ = php_explode("\n", php_implode("", file(str(site_dir_) + str("/") + str(newfile_))))
        if lines_:
            f_ = fopen(str(site_dir_) + str("/") + str(newfile_), "w")
            for line_ in lines_:
                if php_preg_match("/require.*wp-blog-header/", line_):
                    line_ = "//" + line_
                # end if
                #// Update stylesheet references.
                line_ = php_str_replace("<?php echo __get_option('siteurl'); ?>/wp-layout.css", "<?php bloginfo('stylesheet_url'); ?>", line_)
                #// Update comments template inclusion.
                line_ = php_str_replace("<?php include(ABSPATH . 'wp-comments.php'); ?>", "<?php comments_template(); ?>", line_)
                fwrite(f_, str(line_) + str("\n"))
            # end for
            php_fclose(f_)
        # end if
    # end for
    #// Add a theme header.
    header_ = str("/*\nTheme Name: ") + str(theme_name_) + str("\nTheme URI: ") + __get_option("siteurl") + """
    Description: A theme automatically created by the update.
    Version: 1.0
    Author: Moi
    */
    """
    stylelines_ = php_file_get_contents(str(site_dir_) + str("/style.css"))
    if stylelines_:
        f_ = fopen(str(site_dir_) + str("/style.css"), "w")
        fwrite(f_, header_)
        fwrite(f_, stylelines_)
        php_fclose(f_)
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
def make_site_theme_from_default(theme_name_=None, template_=None, *_args_):
    
    
    site_dir_ = WP_CONTENT_DIR + str("/themes/") + str(template_)
    default_dir_ = WP_CONTENT_DIR + "/themes/" + WP_DEFAULT_THEME
    #// Copy files from the default theme to the site theme.
    #// $files = array( 'index.php', 'comments.php', 'comments-popup.php', 'footer.php', 'header.php', 'sidebar.php', 'style.css' );
    theme_dir_ = php_no_error(lambda: php_opendir(default_dir_))
    if theme_dir_:
        while True:
            theme_file_ = php_readdir(theme_dir_)
            if not (theme_file_ != False):
                break
            # end if
            if php_is_dir(str(default_dir_) + str("/") + str(theme_file_)):
                continue
            # end if
            if (not copy(str(default_dir_) + str("/") + str(theme_file_), str(site_dir_) + str("/") + str(theme_file_))):
                return
            # end if
            chmod(str(site_dir_) + str("/") + str(theme_file_), 511)
        # end while
        php_closedir(theme_dir_)
    # end if
    #// Rewrite the theme header.
    stylelines_ = php_explode("\n", php_implode("", file(str(site_dir_) + str("/style.css"))))
    if stylelines_:
        f_ = fopen(str(site_dir_) + str("/style.css"), "w")
        for line_ in stylelines_:
            if php_strpos(line_, "Theme Name:") != False:
                line_ = "Theme Name: " + theme_name_
            elif php_strpos(line_, "Theme URI:") != False:
                line_ = "Theme URI: " + __get_option("url")
            elif php_strpos(line_, "Description:") != False:
                line_ = "Description: Your theme."
            elif php_strpos(line_, "Version:") != False:
                line_ = "Version: 1"
            elif php_strpos(line_, "Author:") != False:
                line_ = "Author: You"
            # end if
            fwrite(f_, line_ + "\n")
        # end for
        php_fclose(f_)
    # end if
    #// Copy the images.
    umask(0)
    if (not mkdir(str(site_dir_) + str("/images"), 511)):
        return False
    # end if
    images_dir_ = php_no_error(lambda: php_opendir(str(default_dir_) + str("/images")))
    if images_dir_:
        while True:
            image_ = php_readdir(images_dir_)
            if not (image_ != False):
                break
            # end if
            if php_is_dir(str(default_dir_) + str("/images/") + str(image_)):
                continue
            # end if
            if (not copy(str(default_dir_) + str("/images/") + str(image_), str(site_dir_) + str("/images/") + str(image_))):
                return
            # end if
            chmod(str(site_dir_) + str("/images/") + str(image_), 511)
        # end while
        php_closedir(images_dir_)
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
def make_site_theme(*_args_):
    
    
    #// Name the theme after the blog.
    theme_name_ = __get_option("blogname")
    template_ = sanitize_title(theme_name_)
    site_dir_ = WP_CONTENT_DIR + str("/themes/") + str(template_)
    #// If the theme already exists, nothing to do.
    if php_is_dir(site_dir_):
        return False
    # end if
    #// We must be able to write to the themes dir.
    if (not php_is_writable(WP_CONTENT_DIR + "/themes")):
        return False
    # end if
    umask(0)
    if (not mkdir(site_dir_, 511)):
        return False
    # end if
    if php_file_exists(ABSPATH + "wp-layout.css"):
        if (not make_site_theme_from_oldschool(theme_name_, template_)):
            #// TODO: rm -rf the site theme directory.
            return False
        # end if
    else:
        if (not make_site_theme_from_default(theme_name_, template_)):
            #// TODO: rm -rf the site theme directory.
            return False
        # end if
    # end if
    #// Make the new site theme active.
    current_template_ = __get_option("template")
    if WP_DEFAULT_THEME == current_template_:
        update_option("template", template_)
        update_option("stylesheet", template_)
    # end if
    return template_
# end def make_site_theme
#// 
#// Translate user level to user role name.
#// 
#// @since 2.0.0
#// 
#// @param int $level User level.
#// @return string User role name.
#//
def translate_level_to_role(level_=None, *_args_):
    
    
    for case in Switch(level_):
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
def wp_check_mysql_version(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    result_ = wpdb_.check_database_version()
    if is_wp_error(result_):
        wp_die(result_)
    # end if
# end def wp_check_mysql_version
#// 
#// Disables the Automattic widgets plugin, which was merged into core.
#// 
#// @since 2.2.0
#//
def maybe_disable_automattic_widgets(*_args_):
    
    
    plugins_ = __get_option("active_plugins")
    for plugin_ in plugins_:
        if php_basename(plugin_) == "widgets.php":
            array_splice(plugins_, php_array_search(plugin_, plugins_), 1)
            update_option("active_plugins", plugins_)
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
def maybe_disable_link_manager(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    if wp_current_db_version_ >= 22006 and get_option("link_manager_enabled") and (not wpdb_.get_var(str("SELECT link_id FROM ") + str(wpdb_.links) + str(" LIMIT 1"))):
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
def pre_schema_upgrade(*_args_):
    
    
    global wp_current_db_version_
    global wpdb_
    php_check_if_defined("wp_current_db_version_","wpdb_")
    #// Upgrade versions prior to 2.9.
    if wp_current_db_version_ < 11557:
        #// Delete duplicate options. Keep the option with the highest option_id.
        wpdb_.query(str("DELETE o1 FROM ") + str(wpdb_.options) + str(" AS o1 JOIN ") + str(wpdb_.options) + str(" AS o2 USING (`option_name`) WHERE o2.option_id > o1.option_id"))
        #// Drop the old primary key and add the new.
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.options) + str(" DROP PRIMARY KEY, ADD PRIMARY KEY(option_id)"))
        #// Drop the old option_name index. dbDelta() doesn't do the drop.
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.options) + str(" DROP INDEX option_name"))
    # end if
    #// Multisite schema upgrades.
    if wp_current_db_version_ < 25448 and is_multisite() and wp_should_upgrade_global_tables():
        #// Upgrade versions prior to 3.7.
        if wp_current_db_version_ < 25179:
            #// New primary key for signups.
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.signups) + str(" ADD signup_id BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST"))
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.signups) + str(" DROP INDEX domain"))
        # end if
        if wp_current_db_version_ < 25448:
            #// Convert archived from enum to tinyint.
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.blogs) + str(" CHANGE COLUMN archived archived varchar(1) NOT NULL default '0'"))
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.blogs) + str(" CHANGE COLUMN archived archived tinyint(2) NOT NULL default 0"))
        # end if
    # end if
    #// Upgrade versions prior to 4.2.
    if wp_current_db_version_ < 31351:
        if (not is_multisite()) and wp_should_upgrade_global_tables():
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.usermeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
        # end if
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.terms) + str(" DROP INDEX slug, ADD INDEX slug(slug(191))"))
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.terms) + str(" DROP INDEX name, ADD INDEX name(name(191))"))
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.commentmeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.postmeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
        wpdb_.query(str("ALTER TABLE ") + str(wpdb_.posts) + str(" DROP INDEX post_name, ADD INDEX post_name(post_name(191))"))
    # end if
    #// Upgrade versions prior to 4.4.
    if wp_current_db_version_ < 34978:
        #// If compatible termmeta table is found, use it, but enforce a proper index and update collation.
        if wpdb_.get_var(str("SHOW TABLES LIKE '") + str(wpdb_.termmeta) + str("'")) and wpdb_.get_results(str("SHOW INDEX FROM ") + str(wpdb_.termmeta) + str(" WHERE Column_name = 'meta_key'")):
            wpdb_.query(str("ALTER TABLE ") + str(wpdb_.termmeta) + str(" DROP INDEX meta_key, ADD INDEX meta_key(meta_key(191))"))
            maybe_convert_table_to_utf8mb4(wpdb_.termmeta)
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
    def install_global_terms(*_args_):
        
        
        global wpdb_
        global charset_collate_
        php_check_if_defined("wpdb_","charset_collate_")
        ms_queries_ = str("\nCREATE TABLE ") + str(wpdb_.sitecategories) + str(""" (\n  cat_ID bigint(20) NOT NULL auto_increment,\n  cat_name varchar(55) NOT NULL default '',\n  category_nicename varchar(200) NOT NULL default '',\n  last_updated timestamp NOT NULL,\n  PRIMARY KEY  (cat_ID),\n  KEY category_nicename (category_nicename),\n  KEY last_updated (last_updated)\n) """) + str(charset_collate_) + str(";\n")
        #// Now create tables.
        dbDelta(ms_queries_)
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
def wp_should_upgrade_global_tables(*_args_):
    
    
    #// Return false early if explicitly not upgrading.
    if php_defined("DO_NOT_UPGRADE_GLOBAL_TABLES"):
        return False
    # end if
    #// Assume global tables should be upgraded.
    should_upgrade_ = True
    #// Set to false if not on main network (does not matter if not multi-network).
    if (not is_main_network()):
        should_upgrade_ = False
    # end if
    #// Set to false if not on main site of current network (does not matter if not multi-site).
    if (not is_main_site()):
        should_upgrade_ = False
    # end if
    #// 
    #// Filters if upgrade routines should be run on global tables.
    #// 
    #// @param bool $should_upgrade Whether to run the upgrade routines on global tables.
    #//
    return apply_filters("wp_should_upgrade_global_tables", should_upgrade_)
# end def wp_should_upgrade_global_tables
