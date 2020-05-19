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
#// Toolbar API: Top-level Toolbar functionality
#// 
#// @package WordPress
#// @subpackage Toolbar
#// @since 3.1.0
#// 
#// 
#// Instantiate the admin bar object and set it up as a global for access elsewhere.
#// 
#// UNHOOKING THIS FUNCTION WILL NOT PROPERLY REMOVE THE ADMIN BAR.
#// For that, use show_admin_bar(false) or the {@see 'show_admin_bar'} filter.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @global WP_Admin_Bar $wp_admin_bar
#// 
#// @return bool Whether the admin bar was successfully initialized.
#//
def _wp_admin_bar_init(*_args_):
    
    
    global wp_admin_bar_
    php_check_if_defined("wp_admin_bar_")
    if (not is_admin_bar_showing()):
        return False
    # end if
    #// Load the admin bar class code ready for instantiation
    php_include_file(ABSPATH + WPINC + "/class-wp-admin-bar.php", once=True)
    #// Instantiate the admin bar
    #// 
    #// Filters the admin bar class to instantiate.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $wp_admin_bar_class Admin bar class to use. Default 'WP_Admin_Bar'.
    #//
    admin_bar_class_ = apply_filters("wp_admin_bar_class", "WP_Admin_Bar")
    if php_class_exists(admin_bar_class_):
        wp_admin_bar_ = php_new_class(admin_bar_class_, lambda : {**locals(), **globals()}[admin_bar_class_]())
    else:
        return False
    # end if
    wp_admin_bar_.initialize()
    wp_admin_bar_.add_menus()
    return True
# end def _wp_admin_bar_init
#// 
#// Renders the admin bar to the page based on the $wp_admin_bar->menu member var.
#// 
#// This is called very early on the {@see 'wp_body_open'} action so that it will render
#// before anything else being added to the page body.
#// 
#// For backward compatibility with themes not using the 'wp_body_open' action,
#// the function is also called late on {@see 'wp_footer'}.
#// 
#// It includes the {@see 'admin_bar_menu'} action which should be used to hook in and
#// add new menus to the admin bar. That way you can be sure that you are adding at most
#// optimal point, right before the admin bar is rendered. This also gives you access to
#// the `$post` global, among others.
#// 
#// @since 3.1.0
#// @since 5.4.0 Called on 'wp_body_open' action first, with 'wp_footer' as a fallback.
#// 
#// @global WP_Admin_Bar $wp_admin_bar
#// 
#// @staticvar bool $rendered
#//
def wp_admin_bar_render(*_args_):
    
    
    global wp_admin_bar_
    php_check_if_defined("wp_admin_bar_")
    rendered_ = False
    if rendered_:
        return
    # end if
    if (not is_admin_bar_showing()) or (not php_is_object(wp_admin_bar_)):
        return
    # end if
    #// 
    #// Load all necessary admin bar items.
    #// 
    #// This is the hook used to add, remove, or manipulate admin bar items.
    #// 
    #// @since 3.1.0
    #// 
    #// @param WP_Admin_Bar $wp_admin_bar WP_Admin_Bar instance, passed by reference
    #//
    do_action_ref_array("admin_bar_menu", Array(wp_admin_bar_))
    #// 
    #// Fires before the admin bar is rendered.
    #// 
    #// @since 3.1.0
    #//
    do_action("wp_before_admin_bar_render")
    wp_admin_bar_.render()
    #// 
    #// Fires after the admin bar is rendered.
    #// 
    #// @since 3.1.0
    #//
    do_action("wp_after_admin_bar_render")
    rendered_ = True
# end def wp_admin_bar_render
#// 
#// Add the WordPress logo menu.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_wp_menu(wp_admin_bar_=None, *_args_):
    
    
    if current_user_can("read"):
        about_url_ = self_admin_url("about.php")
    elif is_multisite():
        about_url_ = get_dashboard_url(get_current_user_id(), "about.php")
    else:
        about_url_ = False
    # end if
    wp_logo_menu_args_ = Array({"id": "wp-logo", "title": "<span class=\"ab-icon\"></span><span class=\"screen-reader-text\">" + __("About WordPress") + "</span>", "href": about_url_})
    #// Set tabindex="0" to make sub menus accessible when no URL is available.
    if (not about_url_):
        wp_logo_menu_args_["meta"] = Array({"tabindex": 0})
    # end if
    wp_admin_bar_.add_node(wp_logo_menu_args_)
    if about_url_:
        #// Add "About WordPress" link.
        wp_admin_bar_.add_node(Array({"parent": "wp-logo", "id": "about", "title": __("About WordPress"), "href": about_url_}))
    # end if
    #// Add WordPress.org link.
    wp_admin_bar_.add_node(Array({"parent": "wp-logo-external", "id": "wporg", "title": __("WordPress.org"), "href": __("https://wordpress.org/")}))
    #// Add Codex link.
    wp_admin_bar_.add_node(Array({"parent": "wp-logo-external", "id": "documentation", "title": __("Documentation"), "href": __("https://codex.wordpress.org/")}))
    #// Add forums link.
    wp_admin_bar_.add_node(Array({"parent": "wp-logo-external", "id": "support-forums", "title": __("Support"), "href": __("https://wordpress.org/support/")}))
    #// Add feedback link.
    wp_admin_bar_.add_node(Array({"parent": "wp-logo-external", "id": "feedback", "title": __("Feedback"), "href": __("https://wordpress.org/support/forum/requests-and-feedback")}))
# end def wp_admin_bar_wp_menu
#// 
#// Add the sidebar toggle button.
#// 
#// @since 3.8.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_sidebar_toggle(wp_admin_bar_=None, *_args_):
    
    
    if is_admin():
        wp_admin_bar_.add_node(Array({"id": "menu-toggle", "title": "<span class=\"ab-icon\"></span><span class=\"screen-reader-text\">" + __("Menu") + "</span>", "href": "#"}))
    # end if
# end def wp_admin_bar_sidebar_toggle
#// 
#// Add the "My Account" item.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_my_account_item(wp_admin_bar_=None, *_args_):
    
    
    user_id_ = get_current_user_id()
    current_user_ = wp_get_current_user()
    if (not user_id_):
        return
    # end if
    if current_user_can("read"):
        profile_url_ = get_edit_profile_url(user_id_)
    elif is_multisite():
        profile_url_ = get_dashboard_url(user_id_, "profile.php")
    else:
        profile_url_ = False
    # end if
    avatar_ = get_avatar(user_id_, 26)
    #// translators: %s: Current user's display name.
    howdy_ = php_sprintf(__("Howdy, %s"), "<span class=\"display-name\">" + current_user_.display_name + "</span>")
    class_ = "" if php_empty(lambda : avatar_) else "with-avatar"
    wp_admin_bar_.add_node(Array({"id": "my-account", "parent": "top-secondary", "title": howdy_ + avatar_, "href": profile_url_, "meta": Array({"class": class_})}))
# end def wp_admin_bar_my_account_item
#// 
#// Add the "My Account" submenu items.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_my_account_menu(wp_admin_bar_=None, *_args_):
    
    
    user_id_ = get_current_user_id()
    current_user_ = wp_get_current_user()
    if (not user_id_):
        return
    # end if
    if current_user_can("read"):
        profile_url_ = get_edit_profile_url(user_id_)
    elif is_multisite():
        profile_url_ = get_dashboard_url(user_id_, "profile.php")
    else:
        profile_url_ = False
    # end if
    wp_admin_bar_.add_group(Array({"parent": "my-account", "id": "user-actions"}))
    user_info_ = get_avatar(user_id_, 64)
    user_info_ += str("<span class='display-name'>") + str(current_user_.display_name) + str("</span>")
    if current_user_.display_name != current_user_.user_login:
        user_info_ += str("<span class='username'>") + str(current_user_.user_login) + str("</span>")
    # end if
    wp_admin_bar_.add_node(Array({"parent": "user-actions", "id": "user-info", "title": user_info_, "href": profile_url_, "meta": Array({"tabindex": -1})}))
    if False != profile_url_:
        wp_admin_bar_.add_node(Array({"parent": "user-actions", "id": "edit-profile", "title": __("Edit My Profile"), "href": profile_url_}))
    # end if
    wp_admin_bar_.add_node(Array({"parent": "user-actions", "id": "logout", "title": __("Log Out"), "href": wp_logout_url()}))
# end def wp_admin_bar_my_account_menu
#// 
#// Add the "Site Name" menu.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_site_menu(wp_admin_bar_=None, *_args_):
    
    
    #// Don't show for logged out users.
    if (not is_user_logged_in()):
        return
    # end if
    #// Show only when the user is a member of this site, or they're a super admin.
    if (not is_user_member_of_blog()) and (not current_user_can("manage_network")):
        return
    # end if
    blogname_ = get_bloginfo("name")
    if (not blogname_):
        blogname_ = php_preg_replace("#^(https?://)?(www.)?#", "", get_home_url())
    # end if
    if is_network_admin():
        #// translators: %s: Site title.
        blogname_ = php_sprintf(__("Network Admin: %s"), esc_html(get_network().site_name))
    elif is_user_admin():
        #// translators: %s: Site title.
        blogname_ = php_sprintf(__("User Dashboard: %s"), esc_html(get_network().site_name))
    # end if
    title_ = wp_html_excerpt(blogname_, 40, "&hellip;")
    wp_admin_bar_.add_node(Array({"id": "site-name", "title": title_, "href": home_url("/") if is_admin() or (not current_user_can("read")) else admin_url()}))
    #// Create submenu items.
    if is_admin():
        #// Add an option to visit the site.
        wp_admin_bar_.add_node(Array({"parent": "site-name", "id": "view-site", "title": __("Visit Site"), "href": home_url("/")}))
        if is_blog_admin() and is_multisite() and current_user_can("manage_sites"):
            wp_admin_bar_.add_node(Array({"parent": "site-name", "id": "edit-site", "title": __("Edit Site"), "href": network_admin_url("site-info.php?id=" + get_current_blog_id())}))
        # end if
    elif current_user_can("read"):
        #// We're on the front end, link to the Dashboard.
        wp_admin_bar_.add_node(Array({"parent": "site-name", "id": "dashboard", "title": __("Dashboard"), "href": admin_url()}))
        #// Add the appearance submenu items.
        wp_admin_bar_appearance_menu(wp_admin_bar_)
    # end if
# end def wp_admin_bar_site_menu
#// 
#// Adds the "Customize" link to the Toolbar.
#// 
#// @since 4.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar WP_Admin_Bar instance.
#// @global WP_Customize_Manager $wp_customize
#//
def wp_admin_bar_customize_menu(wp_admin_bar_=None, *_args_):
    
    
    global wp_customize_
    php_check_if_defined("wp_customize_")
    #// Don't show for users who can't access the customizer or when in the admin.
    if (not current_user_can("customize")) or is_admin():
        return
    # end if
    #// Don't show if the user cannot edit a given customize_changeset post currently being previewed.
    if is_customize_preview() and wp_customize_.changeset_post_id() and (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, wp_customize_.changeset_post_id())):
        return
    # end if
    current_url_ = "https://" if is_ssl() else "http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"]
    if is_customize_preview() and wp_customize_.changeset_uuid():
        current_url_ = remove_query_arg("customize_changeset_uuid", current_url_)
    # end if
    customize_url_ = add_query_arg("url", urlencode(current_url_), wp_customize_url())
    if is_customize_preview():
        customize_url_ = add_query_arg(Array({"changeset_uuid": wp_customize_.changeset_uuid()}), customize_url_)
    # end if
    wp_admin_bar_.add_node(Array({"id": "customize", "title": __("Customize"), "href": customize_url_, "meta": Array({"class": "hide-if-no-customize"})}))
    add_action("wp_before_admin_bar_render", "wp_customize_support_script")
# end def wp_admin_bar_customize_menu
#// 
#// Add the "My Sites/[Site Name]" menu and all submenus.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_my_sites_menu(wp_admin_bar_=None, *_args_):
    
    
    #// Don't show for logged out users or single site mode.
    if (not is_user_logged_in()) or (not is_multisite()):
        return
    # end if
    #// Show only when the user has at least one site, or they're a super admin.
    if php_count(wp_admin_bar_.user.blogs) < 1 and (not current_user_can("manage_network")):
        return
    # end if
    if wp_admin_bar_.user.active_blog:
        my_sites_url_ = get_admin_url(wp_admin_bar_.user.active_blog.blog_id, "my-sites.php")
    else:
        my_sites_url_ = admin_url("my-sites.php")
    # end if
    wp_admin_bar_.add_node(Array({"id": "my-sites", "title": __("My Sites"), "href": my_sites_url_}))
    if current_user_can("manage_network"):
        wp_admin_bar_.add_group(Array({"parent": "my-sites", "id": "my-sites-super-admin"}))
        wp_admin_bar_.add_node(Array({"parent": "my-sites-super-admin", "id": "network-admin", "title": __("Network Admin"), "href": network_admin_url()}))
        wp_admin_bar_.add_node(Array({"parent": "network-admin", "id": "network-admin-d", "title": __("Dashboard"), "href": network_admin_url()}))
        if current_user_can("manage_sites"):
            wp_admin_bar_.add_node(Array({"parent": "network-admin", "id": "network-admin-s", "title": __("Sites"), "href": network_admin_url("sites.php")}))
        # end if
        if current_user_can("manage_network_users"):
            wp_admin_bar_.add_node(Array({"parent": "network-admin", "id": "network-admin-u", "title": __("Users"), "href": network_admin_url("users.php")}))
        # end if
        if current_user_can("manage_network_themes"):
            wp_admin_bar_.add_node(Array({"parent": "network-admin", "id": "network-admin-t", "title": __("Themes"), "href": network_admin_url("themes.php")}))
        # end if
        if current_user_can("manage_network_plugins"):
            wp_admin_bar_.add_node(Array({"parent": "network-admin", "id": "network-admin-p", "title": __("Plugins"), "href": network_admin_url("plugins.php")}))
        # end if
        if current_user_can("manage_network_options"):
            wp_admin_bar_.add_node(Array({"parent": "network-admin", "id": "network-admin-o", "title": __("Settings"), "href": network_admin_url("settings.php")}))
        # end if
    # end if
    #// Add site links.
    wp_admin_bar_.add_group(Array({"parent": "my-sites", "id": "my-sites-list", "meta": Array({"class": "ab-sub-secondary" if current_user_can("manage_network") else ""})}))
    for blog_ in wp_admin_bar_.user.blogs:
        switch_to_blog(blog_.userblog_id)
        blavatar_ = "<div class=\"blavatar\"></div>"
        blogname_ = blog_.blogname
        if (not blogname_):
            blogname_ = php_preg_replace("#^(https?://)?(www.)?#", "", get_home_url())
        # end if
        menu_id_ = "blog-" + blog_.userblog_id
        if current_user_can("read"):
            wp_admin_bar_.add_node(Array({"parent": "my-sites-list", "id": menu_id_, "title": blavatar_ + blogname_, "href": admin_url()}))
            wp_admin_bar_.add_node(Array({"parent": menu_id_, "id": menu_id_ + "-d", "title": __("Dashboard"), "href": admin_url()}))
        else:
            wp_admin_bar_.add_node(Array({"parent": "my-sites-list", "id": menu_id_, "title": blavatar_ + blogname_, "href": home_url()}))
        # end if
        if current_user_can(get_post_type_object("post").cap.create_posts):
            wp_admin_bar_.add_node(Array({"parent": menu_id_, "id": menu_id_ + "-n", "title": get_post_type_object("post").labels.new_item, "href": admin_url("post-new.php")}))
        # end if
        if current_user_can("edit_posts"):
            wp_admin_bar_.add_node(Array({"parent": menu_id_, "id": menu_id_ + "-c", "title": __("Manage Comments"), "href": admin_url("edit-comments.php")}))
        # end if
        wp_admin_bar_.add_node(Array({"parent": menu_id_, "id": menu_id_ + "-v", "title": __("Visit Site"), "href": home_url("/")}))
        restore_current_blog()
    # end for
# end def wp_admin_bar_my_sites_menu
#// 
#// Provide a shortlink.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_shortlink_menu(wp_admin_bar_=None, *_args_):
    
    
    short_ = wp_get_shortlink(0, "query")
    id_ = "get-shortlink"
    if php_empty(lambda : short_):
        return
    # end if
    html_ = "<input class=\"shortlink-input\" type=\"text\" readonly=\"readonly\" value=\"" + esc_attr(short_) + "\" />"
    wp_admin_bar_.add_node(Array({"id": id_, "title": __("Shortlink"), "href": short_, "meta": Array({"html": html_})}))
# end def wp_admin_bar_shortlink_menu
#// 
#// Provide an edit link for posts and terms.
#// 
#// @since 3.1.0
#// 
#// @global WP_Term  $tag
#// @global WP_Query $wp_the_query WordPress Query object.
#// @global int      $user_id      The ID of the user being edited. Not to be confused with the
#// global $user_ID, which contains the ID of the current user.
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_edit_menu(wp_admin_bar_=None, *_args_):
    
    
    global tag_
    global wp_the_query_
    global user_id_
    php_check_if_defined("tag_","wp_the_query_","user_id_")
    if is_admin():
        current_screen_ = get_current_screen()
        post_ = get_post()
        if "post" == current_screen_.base:
            post_type_object_ = get_post_type_object(post_.post_type)
        elif "edit" == current_screen_.base:
            post_type_object_ = get_post_type_object(current_screen_.post_type)
        # end if
        if "post" == current_screen_.base and "add" != current_screen_.action and post_type_object_ and current_user_can("read_post", post_.ID) and post_type_object_.public and post_type_object_.show_in_admin_bar:
            if "draft" == post_.post_status:
                preview_link_ = get_preview_post_link(post_)
                wp_admin_bar_.add_node(Array({"id": "preview", "title": post_type_object_.labels.view_item, "href": esc_url(preview_link_), "meta": Array({"target": "wp-preview-" + post_.ID})}))
            else:
                wp_admin_bar_.add_node(Array({"id": "view", "title": post_type_object_.labels.view_item, "href": get_permalink(post_.ID)}))
            # end if
        elif "edit" == current_screen_.base and post_type_object_ and post_type_object_.public and post_type_object_.show_in_admin_bar and get_post_type_archive_link(post_type_object_.name) and (not "post" == post_type_object_.name and "posts" == get_option("show_on_front")):
            wp_admin_bar_.add_node(Array({"id": "archive", "title": post_type_object_.labels.view_items, "href": get_post_type_archive_link(current_screen_.post_type)}))
        elif "term" == current_screen_.base and (php_isset(lambda : tag_)) and php_is_object(tag_) and (not is_wp_error(tag_)):
            tax_ = get_taxonomy(tag_.taxonomy)
            if is_taxonomy_viewable(tax_):
                wp_admin_bar_.add_node(Array({"id": "view", "title": tax_.labels.view_item, "href": get_term_link(tag_)}))
            # end if
        elif "user-edit" == current_screen_.base and (php_isset(lambda : user_id_)):
            user_object_ = get_userdata(user_id_)
            view_link_ = get_author_posts_url(user_object_.ID)
            if user_object_.exists() and view_link_:
                wp_admin_bar_.add_node(Array({"id": "view", "title": __("View User"), "href": view_link_}))
            # end if
        # end if
    else:
        current_object_ = wp_the_query_.get_queried_object()
        if php_empty(lambda : current_object_):
            return
        # end if
        if (not php_empty(lambda : current_object_.post_type)):
            post_type_object_ = get_post_type_object(current_object_.post_type)
            edit_post_link_ = get_edit_post_link(current_object_.ID)
            if post_type_object_ and edit_post_link_ and current_user_can("edit_post", current_object_.ID) and post_type_object_.show_in_admin_bar:
                wp_admin_bar_.add_node(Array({"id": "edit", "title": post_type_object_.labels.edit_item, "href": edit_post_link_}))
            # end if
        elif (not php_empty(lambda : current_object_.taxonomy)):
            tax_ = get_taxonomy(current_object_.taxonomy)
            edit_term_link_ = get_edit_term_link(current_object_.term_id, current_object_.taxonomy)
            if tax_ and edit_term_link_ and current_user_can("edit_term", current_object_.term_id):
                wp_admin_bar_.add_node(Array({"id": "edit", "title": tax_.labels.edit_item, "href": edit_term_link_}))
            # end if
        elif php_is_a(current_object_, "WP_User") and current_user_can("edit_user", current_object_.ID):
            edit_user_link_ = get_edit_user_link(current_object_.ID)
            if edit_user_link_:
                wp_admin_bar_.add_node(Array({"id": "edit", "title": __("Edit User"), "href": edit_user_link_}))
            # end if
        # end if
    # end if
# end def wp_admin_bar_edit_menu
#// 
#// Add "Add New" menu.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_new_content_menu(wp_admin_bar_=None, *_args_):
    
    
    actions_ = Array()
    cpts_ = get_post_types(Array({"show_in_admin_bar": True}), "objects")
    if (php_isset(lambda : cpts_["post"])) and current_user_can(cpts_["post"].cap.create_posts):
        actions_["post-new.php"] = Array(cpts_["post"].labels.name_admin_bar, "new-post")
    # end if
    if (php_isset(lambda : cpts_["attachment"])) and current_user_can("upload_files"):
        actions_["media-new.php"] = Array(cpts_["attachment"].labels.name_admin_bar, "new-media")
    # end if
    if current_user_can("manage_links"):
        actions_["link-add.php"] = Array(_x("Link", "add new from admin bar"), "new-link")
    # end if
    if (php_isset(lambda : cpts_["page"])) and current_user_can(cpts_["page"].cap.create_posts):
        actions_["post-new.php?post_type=page"] = Array(cpts_["page"].labels.name_admin_bar, "new-page")
    # end if
    cpts_["post"] = None
    cpts_["page"] = None
    cpts_["attachment"] = None
    #// Add any additional custom post types.
    for cpt_ in cpts_:
        if (not current_user_can(cpt_.cap.create_posts)):
            continue
        # end if
        key_ = "post-new.php?post_type=" + cpt_.name
        actions_[key_] = Array(cpt_.labels.name_admin_bar, "new-" + cpt_.name)
    # end for
    #// Avoid clash with parent node and a 'content' post type.
    if (php_isset(lambda : actions_["post-new.php?post_type=content"])):
        actions_["post-new.php?post_type=content"][1] = "add-new-content"
    # end if
    if current_user_can("create_users") or is_multisite() and current_user_can("promote_users"):
        actions_["user-new.php"] = Array(_x("User", "add new from admin bar"), "new-user")
    # end if
    if (not actions_):
        return
    # end if
    title_ = "<span class=\"ab-icon\"></span><span class=\"ab-label\">" + _x("New", "admin bar menu group label") + "</span>"
    wp_admin_bar_.add_node(Array({"id": "new-content", "title": title_, "href": admin_url(current(php_array_keys(actions_)))}))
    for link_,action_ in actions_.items():
        title_, id_ = action_
        wp_admin_bar_.add_node(Array({"parent": "new-content", "id": id_, "title": title_, "href": admin_url(link_)}))
    # end for
# end def wp_admin_bar_new_content_menu
#// 
#// Add edit comments link with awaiting moderation count bubble.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_comments_menu(wp_admin_bar_=None, *_args_):
    
    
    if (not current_user_can("edit_posts")):
        return
    # end if
    awaiting_mod_ = wp_count_comments()
    awaiting_mod_ = awaiting_mod_.moderated
    awaiting_text_ = php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", awaiting_mod_), number_format_i18n(awaiting_mod_))
    icon_ = "<span class=\"ab-icon\"></span>"
    title_ = "<span class=\"ab-label awaiting-mod pending-count count-" + awaiting_mod_ + "\" aria-hidden=\"true\">" + number_format_i18n(awaiting_mod_) + "</span>"
    title_ += "<span class=\"screen-reader-text comments-in-moderation-text\">" + awaiting_text_ + "</span>"
    wp_admin_bar_.add_node(Array({"id": "comments", "title": icon_ + title_, "href": admin_url("edit-comments.php")}))
# end def wp_admin_bar_comments_menu
#// 
#// Add appearance submenu items to the "Site Name" menu.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_appearance_menu(wp_admin_bar_=None, *_args_):
    
    
    wp_admin_bar_.add_group(Array({"parent": "site-name", "id": "appearance"}))
    if current_user_can("switch_themes"):
        wp_admin_bar_.add_node(Array({"parent": "appearance", "id": "themes", "title": __("Themes"), "href": admin_url("themes.php")}))
    # end if
    if (not current_user_can("edit_theme_options")):
        return
    # end if
    if current_theme_supports("widgets"):
        wp_admin_bar_.add_node(Array({"parent": "appearance", "id": "widgets", "title": __("Widgets"), "href": admin_url("widgets.php")}))
    # end if
    if current_theme_supports("menus") or current_theme_supports("widgets"):
        wp_admin_bar_.add_node(Array({"parent": "appearance", "id": "menus", "title": __("Menus"), "href": admin_url("nav-menus.php")}))
    # end if
    if current_theme_supports("custom-background"):
        wp_admin_bar_.add_node(Array({"parent": "appearance", "id": "background", "title": __("Background"), "href": admin_url("themes.php?page=custom-background"), "meta": Array({"class": "hide-if-customize"})}))
    # end if
    if current_theme_supports("custom-header"):
        wp_admin_bar_.add_node(Array({"parent": "appearance", "id": "header", "title": __("Header"), "href": admin_url("themes.php?page=custom-header"), "meta": Array({"class": "hide-if-customize"})}))
    # end if
# end def wp_admin_bar_appearance_menu
#// 
#// Provide an update link if theme/plugin/core updates are available.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_updates_menu(wp_admin_bar_=None, *_args_):
    
    
    update_data_ = wp_get_update_data()
    if (not update_data_["counts"]["total"]):
        return
    # end if
    title_ = "<span class=\"ab-icon\"></span><span class=\"ab-label\">" + number_format_i18n(update_data_["counts"]["total"]) + "</span>"
    title_ += "<span class=\"screen-reader-text\">" + update_data_["title"] + "</span>"
    wp_admin_bar_.add_node(Array({"id": "updates", "title": title_, "href": network_admin_url("update-core.php"), "meta": Array({"title": update_data_["title"]})}))
# end def wp_admin_bar_updates_menu
#// 
#// Add search form.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_search_menu(wp_admin_bar_=None, *_args_):
    
    
    if is_admin():
        return
    # end if
    form_ = "<form action=\"" + esc_url(home_url("/")) + "\" method=\"get\" id=\"adminbarsearch\">"
    form_ += "<input class=\"adminbar-input\" name=\"s\" id=\"adminbar-search\" type=\"text\" value=\"\" maxlength=\"150\" />"
    form_ += "<label for=\"adminbar-search\" class=\"screen-reader-text\">" + __("Search") + "</label>"
    form_ += "<input type=\"submit\" class=\"adminbar-button\" value=\"" + __("Search") + "\"/>"
    form_ += "</form>"
    wp_admin_bar_.add_node(Array({"parent": "top-secondary", "id": "search", "title": form_, "meta": Array({"class": "admin-bar-search", "tabindex": -1})}))
# end def wp_admin_bar_search_menu
#// 
#// Add a link to exit recovery mode when Recovery Mode is active.
#// 
#// @since 5.2.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_recovery_mode_menu(wp_admin_bar_=None, *_args_):
    
    
    if (not wp_is_recovery_mode()):
        return
    # end if
    url_ = wp_login_url()
    url_ = add_query_arg("action", WP_Recovery_Mode.EXIT_ACTION, url_)
    url_ = wp_nonce_url(url_, WP_Recovery_Mode.EXIT_ACTION)
    wp_admin_bar_.add_node(Array({"parent": "top-secondary", "id": "recovery-mode", "title": __("Exit Recovery Mode"), "href": url_}))
# end def wp_admin_bar_recovery_mode_menu
#// 
#// Add secondary menus.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_add_secondary_groups(wp_admin_bar_=None, *_args_):
    
    
    wp_admin_bar_.add_group(Array({"id": "top-secondary", "meta": Array({"class": "ab-top-secondary"})}))
    wp_admin_bar_.add_group(Array({"parent": "wp-logo", "id": "wp-logo-external", "meta": Array({"class": "ab-sub-secondary"})}))
# end def wp_admin_bar_add_secondary_groups
#// 
#// Style and scripts for the admin bar.
#// 
#// @since 3.1.0
#//
def wp_admin_bar_header(*_args_):
    
    
    type_attr_ = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
    php_print("<style")
    php_print(type_attr_)
    php_print(" media=\"print\">#wpadminbar { display:none; }</style>\n ")
# end def wp_admin_bar_header
#// 
#// Default admin bar callback.
#// 
#// @since 3.1.0
#//
def _admin_bar_bump_cb(*_args_):
    
    
    type_attr_ = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
    php_print("<style")
    php_print(type_attr_)
    php_print(""" media=\"screen\">
    html { margin-top: 32px !important; }
    * html body { margin-top: 32px !important; }
    @media screen and ( max-width: 782px ) {
    html { margin-top: 46px !important; }
    * html body { margin-top: 46px !important; }
    }
    </style>
    """)
# end def _admin_bar_bump_cb
#// 
#// Sets the display status of the admin bar.
#// 
#// This can be called immediately upon plugin load. It does not need to be called
#// from a function hooked to the {@see 'init'} action.
#// 
#// @since 3.1.0
#// 
#// @global bool $show_admin_bar
#// 
#// @param bool $show Whether to allow the admin bar to show.
#//
def show_admin_bar(show_=None, *_args_):
    
    
    global show_admin_bar_
    php_check_if_defined("show_admin_bar_")
    show_admin_bar_ = php_bool(show_)
# end def show_admin_bar
#// 
#// Determines whether the admin bar should be showing.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.1.0
#// 
#// @global bool   $show_admin_bar
#// @global string $pagenow
#// 
#// @return bool Whether the admin bar should be showing.
#//
def is_admin_bar_showing(*_args_):
    
    
    global show_admin_bar_
    global pagenow_
    php_check_if_defined("show_admin_bar_","pagenow_")
    #// For all these types of requests, we never want an admin bar.
    if php_defined("XMLRPC_REQUEST") or php_defined("DOING_AJAX") or php_defined("IFRAME_REQUEST") or wp_is_json_request():
        return False
    # end if
    if is_embed():
        return False
    # end if
    #// Integrated into the admin.
    if is_admin():
        return True
    # end if
    if (not (php_isset(lambda : show_admin_bar_))):
        if (not is_user_logged_in()) or "wp-login.php" == pagenow_:
            show_admin_bar_ = False
        else:
            show_admin_bar_ = _get_admin_bar_pref()
        # end if
    # end if
    #// 
    #// Filters whether to show the admin bar.
    #// 
    #// Returning false to this hook is the recommended way to hide the admin bar.
    #// The user's display preference is used for logged in users.
    #// 
    #// @since 3.1.0
    #// 
    #// @param bool $show_admin_bar Whether the admin bar should be shown. Default false.
    #//
    show_admin_bar_ = apply_filters("show_admin_bar", show_admin_bar_)
    return show_admin_bar_
# end def is_admin_bar_showing
#// 
#// Retrieve the admin bar display preference of a user.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @param string $context Context of this preference check. Defaults to 'front'. The 'admin'
#// preference is no longer used.
#// @param int $user Optional. ID of the user to check, defaults to 0 for current user.
#// @return bool Whether the admin bar should be showing for this user.
#//
def _get_admin_bar_pref(context_="front", user_=0, *_args_):
    
    
    pref_ = get_user_option(str("show_admin_bar_") + str(context_), user_)
    if False == pref_:
        return True
    # end if
    return "true" == pref_
# end def _get_admin_bar_pref
