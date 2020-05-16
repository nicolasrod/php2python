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
def _wp_admin_bar_init(*args_):
    
    global wp_admin_bar
    php_check_if_defined("wp_admin_bar")
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
    admin_bar_class = apply_filters("wp_admin_bar_class", "WP_Admin_Bar")
    if php_class_exists(admin_bar_class):
        wp_admin_bar = php_new_class(admin_bar_class, lambda : {**locals(), **globals()}[admin_bar_class]())
    else:
        return False
    # end if
    wp_admin_bar.initialize()
    wp_admin_bar.add_menus()
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
def wp_admin_bar_render(*args_):
    
    global wp_admin_bar
    php_check_if_defined("wp_admin_bar")
    rendered = False
    if rendered:
        return
    # end if
    if (not is_admin_bar_showing()) or (not php_is_object(wp_admin_bar)):
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
    do_action_ref_array("admin_bar_menu", Array(wp_admin_bar))
    #// 
    #// Fires before the admin bar is rendered.
    #// 
    #// @since 3.1.0
    #//
    do_action("wp_before_admin_bar_render")
    wp_admin_bar.render()
    #// 
    #// Fires after the admin bar is rendered.
    #// 
    #// @since 3.1.0
    #//
    do_action("wp_after_admin_bar_render")
    rendered = True
# end def wp_admin_bar_render
#// 
#// Add the WordPress logo menu.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_wp_menu(wp_admin_bar=None, *args_):
    
    if current_user_can("read"):
        about_url = self_admin_url("about.php")
    elif is_multisite():
        about_url = get_dashboard_url(get_current_user_id(), "about.php")
    else:
        about_url = False
    # end if
    wp_logo_menu_args = Array({"id": "wp-logo", "title": "<span class=\"ab-icon\"></span><span class=\"screen-reader-text\">" + __("About WordPress") + "</span>", "href": about_url})
    #// Set tabindex="0" to make sub menus accessible when no URL is available.
    if (not about_url):
        wp_logo_menu_args["meta"] = Array({"tabindex": 0})
    # end if
    wp_admin_bar.add_node(wp_logo_menu_args)
    if about_url:
        #// Add "About WordPress" link.
        wp_admin_bar.add_node(Array({"parent": "wp-logo", "id": "about", "title": __("About WordPress"), "href": about_url}))
    # end if
    #// Add WordPress.org link.
    wp_admin_bar.add_node(Array({"parent": "wp-logo-external", "id": "wporg", "title": __("WordPress.org"), "href": __("https://wordpress.org/")}))
    #// Add Codex link.
    wp_admin_bar.add_node(Array({"parent": "wp-logo-external", "id": "documentation", "title": __("Documentation"), "href": __("https://codex.wordpress.org/")}))
    #// Add forums link.
    wp_admin_bar.add_node(Array({"parent": "wp-logo-external", "id": "support-forums", "title": __("Support"), "href": __("https://wordpress.org/support/")}))
    #// Add feedback link.
    wp_admin_bar.add_node(Array({"parent": "wp-logo-external", "id": "feedback", "title": __("Feedback"), "href": __("https://wordpress.org/support/forum/requests-and-feedback")}))
# end def wp_admin_bar_wp_menu
#// 
#// Add the sidebar toggle button.
#// 
#// @since 3.8.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_sidebar_toggle(wp_admin_bar=None, *args_):
    
    if is_admin():
        wp_admin_bar.add_node(Array({"id": "menu-toggle", "title": "<span class=\"ab-icon\"></span><span class=\"screen-reader-text\">" + __("Menu") + "</span>", "href": "#"}))
    # end if
# end def wp_admin_bar_sidebar_toggle
#// 
#// Add the "My Account" item.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_my_account_item(wp_admin_bar=None, *args_):
    
    user_id = get_current_user_id()
    current_user = wp_get_current_user()
    if (not user_id):
        return
    # end if
    if current_user_can("read"):
        profile_url = get_edit_profile_url(user_id)
    elif is_multisite():
        profile_url = get_dashboard_url(user_id, "profile.php")
    else:
        profile_url = False
    # end if
    avatar = get_avatar(user_id, 26)
    #// translators: %s: Current user's display name.
    howdy = php_sprintf(__("Howdy, %s"), "<span class=\"display-name\">" + current_user.display_name + "</span>")
    class_ = "" if php_empty(lambda : avatar) else "with-avatar"
    wp_admin_bar.add_node(Array({"id": "my-account", "parent": "top-secondary", "title": howdy + avatar, "href": profile_url, "meta": Array({"class": class_})}))
# end def wp_admin_bar_my_account_item
#// 
#// Add the "My Account" submenu items.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_my_account_menu(wp_admin_bar=None, *args_):
    
    user_id = get_current_user_id()
    current_user = wp_get_current_user()
    if (not user_id):
        return
    # end if
    if current_user_can("read"):
        profile_url = get_edit_profile_url(user_id)
    elif is_multisite():
        profile_url = get_dashboard_url(user_id, "profile.php")
    else:
        profile_url = False
    # end if
    wp_admin_bar.add_group(Array({"parent": "my-account", "id": "user-actions"}))
    user_info = get_avatar(user_id, 64)
    user_info += str("<span class='display-name'>") + str(current_user.display_name) + str("</span>")
    if current_user.display_name != current_user.user_login:
        user_info += str("<span class='username'>") + str(current_user.user_login) + str("</span>")
    # end if
    wp_admin_bar.add_node(Array({"parent": "user-actions", "id": "user-info", "title": user_info, "href": profile_url, "meta": Array({"tabindex": -1})}))
    if False != profile_url:
        wp_admin_bar.add_node(Array({"parent": "user-actions", "id": "edit-profile", "title": __("Edit My Profile"), "href": profile_url}))
    # end if
    wp_admin_bar.add_node(Array({"parent": "user-actions", "id": "logout", "title": __("Log Out"), "href": wp_logout_url()}))
# end def wp_admin_bar_my_account_menu
#// 
#// Add the "Site Name" menu.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_site_menu(wp_admin_bar=None, *args_):
    
    #// Don't show for logged out users.
    if (not is_user_logged_in()):
        return
    # end if
    #// Show only when the user is a member of this site, or they're a super admin.
    if (not is_user_member_of_blog()) and (not current_user_can("manage_network")):
        return
    # end if
    blogname = get_bloginfo("name")
    if (not blogname):
        blogname = php_preg_replace("#^(https?://)?(www.)?#", "", get_home_url())
    # end if
    if is_network_admin():
        #// translators: %s: Site title.
        blogname = php_sprintf(__("Network Admin: %s"), esc_html(get_network().site_name))
    elif is_user_admin():
        #// translators: %s: Site title.
        blogname = php_sprintf(__("User Dashboard: %s"), esc_html(get_network().site_name))
    # end if
    title = wp_html_excerpt(blogname, 40, "&hellip;")
    wp_admin_bar.add_node(Array({"id": "site-name", "title": title, "href": home_url("/") if is_admin() or (not current_user_can("read")) else admin_url()}))
    #// Create submenu items.
    if is_admin():
        #// Add an option to visit the site.
        wp_admin_bar.add_node(Array({"parent": "site-name", "id": "view-site", "title": __("Visit Site"), "href": home_url("/")}))
        if is_blog_admin() and is_multisite() and current_user_can("manage_sites"):
            wp_admin_bar.add_node(Array({"parent": "site-name", "id": "edit-site", "title": __("Edit Site"), "href": network_admin_url("site-info.php?id=" + get_current_blog_id())}))
        # end if
    elif current_user_can("read"):
        #// We're on the front end, link to the Dashboard.
        wp_admin_bar.add_node(Array({"parent": "site-name", "id": "dashboard", "title": __("Dashboard"), "href": admin_url()}))
        #// Add the appearance submenu items.
        wp_admin_bar_appearance_menu(wp_admin_bar)
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
def wp_admin_bar_customize_menu(wp_admin_bar=None, *args_):
    
    global wp_customize
    php_check_if_defined("wp_customize")
    #// Don't show for users who can't access the customizer or when in the admin.
    if (not current_user_can("customize")) or is_admin():
        return
    # end if
    #// Don't show if the user cannot edit a given customize_changeset post currently being previewed.
    if is_customize_preview() and wp_customize.changeset_post_id() and (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, wp_customize.changeset_post_id())):
        return
    # end if
    current_url = "https://" if is_ssl() else "http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"]
    if is_customize_preview() and wp_customize.changeset_uuid():
        current_url = remove_query_arg("customize_changeset_uuid", current_url)
    # end if
    customize_url = add_query_arg("url", urlencode(current_url), wp_customize_url())
    if is_customize_preview():
        customize_url = add_query_arg(Array({"changeset_uuid": wp_customize.changeset_uuid()}), customize_url)
    # end if
    wp_admin_bar.add_node(Array({"id": "customize", "title": __("Customize"), "href": customize_url, "meta": Array({"class": "hide-if-no-customize"})}))
    add_action("wp_before_admin_bar_render", "wp_customize_support_script")
# end def wp_admin_bar_customize_menu
#// 
#// Add the "My Sites/[Site Name]" menu and all submenus.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_my_sites_menu(wp_admin_bar=None, *args_):
    
    #// Don't show for logged out users or single site mode.
    if (not is_user_logged_in()) or (not is_multisite()):
        return
    # end if
    #// Show only when the user has at least one site, or they're a super admin.
    if php_count(wp_admin_bar.user.blogs) < 1 and (not current_user_can("manage_network")):
        return
    # end if
    if wp_admin_bar.user.active_blog:
        my_sites_url = get_admin_url(wp_admin_bar.user.active_blog.blog_id, "my-sites.php")
    else:
        my_sites_url = admin_url("my-sites.php")
    # end if
    wp_admin_bar.add_node(Array({"id": "my-sites", "title": __("My Sites"), "href": my_sites_url}))
    if current_user_can("manage_network"):
        wp_admin_bar.add_group(Array({"parent": "my-sites", "id": "my-sites-super-admin"}))
        wp_admin_bar.add_node(Array({"parent": "my-sites-super-admin", "id": "network-admin", "title": __("Network Admin"), "href": network_admin_url()}))
        wp_admin_bar.add_node(Array({"parent": "network-admin", "id": "network-admin-d", "title": __("Dashboard"), "href": network_admin_url()}))
        if current_user_can("manage_sites"):
            wp_admin_bar.add_node(Array({"parent": "network-admin", "id": "network-admin-s", "title": __("Sites"), "href": network_admin_url("sites.php")}))
        # end if
        if current_user_can("manage_network_users"):
            wp_admin_bar.add_node(Array({"parent": "network-admin", "id": "network-admin-u", "title": __("Users"), "href": network_admin_url("users.php")}))
        # end if
        if current_user_can("manage_network_themes"):
            wp_admin_bar.add_node(Array({"parent": "network-admin", "id": "network-admin-t", "title": __("Themes"), "href": network_admin_url("themes.php")}))
        # end if
        if current_user_can("manage_network_plugins"):
            wp_admin_bar.add_node(Array({"parent": "network-admin", "id": "network-admin-p", "title": __("Plugins"), "href": network_admin_url("plugins.php")}))
        # end if
        if current_user_can("manage_network_options"):
            wp_admin_bar.add_node(Array({"parent": "network-admin", "id": "network-admin-o", "title": __("Settings"), "href": network_admin_url("settings.php")}))
        # end if
    # end if
    #// Add site links.
    wp_admin_bar.add_group(Array({"parent": "my-sites", "id": "my-sites-list", "meta": Array({"class": "ab-sub-secondary" if current_user_can("manage_network") else ""})}))
    for blog in wp_admin_bar.user.blogs:
        switch_to_blog(blog.userblog_id)
        blavatar = "<div class=\"blavatar\"></div>"
        blogname = blog.blogname
        if (not blogname):
            blogname = php_preg_replace("#^(https?://)?(www.)?#", "", get_home_url())
        # end if
        menu_id = "blog-" + blog.userblog_id
        if current_user_can("read"):
            wp_admin_bar.add_node(Array({"parent": "my-sites-list", "id": menu_id, "title": blavatar + blogname, "href": admin_url()}))
            wp_admin_bar.add_node(Array({"parent": menu_id, "id": menu_id + "-d", "title": __("Dashboard"), "href": admin_url()}))
        else:
            wp_admin_bar.add_node(Array({"parent": "my-sites-list", "id": menu_id, "title": blavatar + blogname, "href": home_url()}))
        # end if
        if current_user_can(get_post_type_object("post").cap.create_posts):
            wp_admin_bar.add_node(Array({"parent": menu_id, "id": menu_id + "-n", "title": get_post_type_object("post").labels.new_item, "href": admin_url("post-new.php")}))
        # end if
        if current_user_can("edit_posts"):
            wp_admin_bar.add_node(Array({"parent": menu_id, "id": menu_id + "-c", "title": __("Manage Comments"), "href": admin_url("edit-comments.php")}))
        # end if
        wp_admin_bar.add_node(Array({"parent": menu_id, "id": menu_id + "-v", "title": __("Visit Site"), "href": home_url("/")}))
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
def wp_admin_bar_shortlink_menu(wp_admin_bar=None, *args_):
    
    short = wp_get_shortlink(0, "query")
    id = "get-shortlink"
    if php_empty(lambda : short):
        return
    # end if
    html = "<input class=\"shortlink-input\" type=\"text\" readonly=\"readonly\" value=\"" + esc_attr(short) + "\" />"
    wp_admin_bar.add_node(Array({"id": id, "title": __("Shortlink"), "href": short, "meta": Array({"html": html})}))
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
def wp_admin_bar_edit_menu(wp_admin_bar=None, *args_):
    
    global tag,wp_the_query,user_id
    php_check_if_defined("tag","wp_the_query","user_id")
    if is_admin():
        current_screen = get_current_screen()
        post = get_post()
        if "post" == current_screen.base:
            post_type_object = get_post_type_object(post.post_type)
        elif "edit" == current_screen.base:
            post_type_object = get_post_type_object(current_screen.post_type)
        # end if
        if "post" == current_screen.base and "add" != current_screen.action and post_type_object and current_user_can("read_post", post.ID) and post_type_object.public and post_type_object.show_in_admin_bar:
            if "draft" == post.post_status:
                preview_link = get_preview_post_link(post)
                wp_admin_bar.add_node(Array({"id": "preview", "title": post_type_object.labels.view_item, "href": esc_url(preview_link), "meta": Array({"target": "wp-preview-" + post.ID})}))
            else:
                wp_admin_bar.add_node(Array({"id": "view", "title": post_type_object.labels.view_item, "href": get_permalink(post.ID)}))
            # end if
        elif "edit" == current_screen.base and post_type_object and post_type_object.public and post_type_object.show_in_admin_bar and get_post_type_archive_link(post_type_object.name) and (not "post" == post_type_object.name and "posts" == get_option("show_on_front")):
            wp_admin_bar.add_node(Array({"id": "archive", "title": post_type_object.labels.view_items, "href": get_post_type_archive_link(current_screen.post_type)}))
        elif "term" == current_screen.base and (php_isset(lambda : tag)) and php_is_object(tag) and (not is_wp_error(tag)):
            tax = get_taxonomy(tag.taxonomy)
            if is_taxonomy_viewable(tax):
                wp_admin_bar.add_node(Array({"id": "view", "title": tax.labels.view_item, "href": get_term_link(tag)}))
            # end if
        elif "user-edit" == current_screen.base and (php_isset(lambda : user_id)):
            user_object = get_userdata(user_id)
            view_link = get_author_posts_url(user_object.ID)
            if user_object.exists() and view_link:
                wp_admin_bar.add_node(Array({"id": "view", "title": __("View User"), "href": view_link}))
            # end if
        # end if
    else:
        current_object = wp_the_query.get_queried_object()
        if php_empty(lambda : current_object):
            return
        # end if
        if (not php_empty(lambda : current_object.post_type)):
            post_type_object = get_post_type_object(current_object.post_type)
            edit_post_link = get_edit_post_link(current_object.ID)
            if post_type_object and edit_post_link and current_user_can("edit_post", current_object.ID) and post_type_object.show_in_admin_bar:
                wp_admin_bar.add_node(Array({"id": "edit", "title": post_type_object.labels.edit_item, "href": edit_post_link}))
            # end if
        elif (not php_empty(lambda : current_object.taxonomy)):
            tax = get_taxonomy(current_object.taxonomy)
            edit_term_link = get_edit_term_link(current_object.term_id, current_object.taxonomy)
            if tax and edit_term_link and current_user_can("edit_term", current_object.term_id):
                wp_admin_bar.add_node(Array({"id": "edit", "title": tax.labels.edit_item, "href": edit_term_link}))
            # end if
        elif php_is_a(current_object, "WP_User") and current_user_can("edit_user", current_object.ID):
            edit_user_link = get_edit_user_link(current_object.ID)
            if edit_user_link:
                wp_admin_bar.add_node(Array({"id": "edit", "title": __("Edit User"), "href": edit_user_link}))
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
def wp_admin_bar_new_content_menu(wp_admin_bar=None, *args_):
    
    actions = Array()
    cpts = get_post_types(Array({"show_in_admin_bar": True}), "objects")
    if (php_isset(lambda : cpts["post"])) and current_user_can(cpts["post"].cap.create_posts):
        actions["post-new.php"] = Array(cpts["post"].labels.name_admin_bar, "new-post")
    # end if
    if (php_isset(lambda : cpts["attachment"])) and current_user_can("upload_files"):
        actions["media-new.php"] = Array(cpts["attachment"].labels.name_admin_bar, "new-media")
    # end if
    if current_user_can("manage_links"):
        actions["link-add.php"] = Array(_x("Link", "add new from admin bar"), "new-link")
    # end if
    if (php_isset(lambda : cpts["page"])) and current_user_can(cpts["page"].cap.create_posts):
        actions["post-new.php?post_type=page"] = Array(cpts["page"].labels.name_admin_bar, "new-page")
    # end if
    cpts["post"] = None
    cpts["page"] = None
    cpts["attachment"] = None
    #// Add any additional custom post types.
    for cpt in cpts:
        if (not current_user_can(cpt.cap.create_posts)):
            continue
        # end if
        key = "post-new.php?post_type=" + cpt.name
        actions[key] = Array(cpt.labels.name_admin_bar, "new-" + cpt.name)
    # end for
    #// Avoid clash with parent node and a 'content' post type.
    if (php_isset(lambda : actions["post-new.php?post_type=content"])):
        actions["post-new.php?post_type=content"][1] = "add-new-content"
    # end if
    if current_user_can("create_users") or is_multisite() and current_user_can("promote_users"):
        actions["user-new.php"] = Array(_x("User", "add new from admin bar"), "new-user")
    # end if
    if (not actions):
        return
    # end if
    title = "<span class=\"ab-icon\"></span><span class=\"ab-label\">" + _x("New", "admin bar menu group label") + "</span>"
    wp_admin_bar.add_node(Array({"id": "new-content", "title": title, "href": admin_url(current(php_array_keys(actions)))}))
    for link,action in actions:
        title, id = action
        wp_admin_bar.add_node(Array({"parent": "new-content", "id": id, "title": title, "href": admin_url(link)}))
    # end for
# end def wp_admin_bar_new_content_menu
#// 
#// Add edit comments link with awaiting moderation count bubble.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_comments_menu(wp_admin_bar=None, *args_):
    
    if (not current_user_can("edit_posts")):
        return
    # end if
    awaiting_mod = wp_count_comments()
    awaiting_mod = awaiting_mod.moderated
    awaiting_text = php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", awaiting_mod), number_format_i18n(awaiting_mod))
    icon = "<span class=\"ab-icon\"></span>"
    title = "<span class=\"ab-label awaiting-mod pending-count count-" + awaiting_mod + "\" aria-hidden=\"true\">" + number_format_i18n(awaiting_mod) + "</span>"
    title += "<span class=\"screen-reader-text comments-in-moderation-text\">" + awaiting_text + "</span>"
    wp_admin_bar.add_node(Array({"id": "comments", "title": icon + title, "href": admin_url("edit-comments.php")}))
# end def wp_admin_bar_comments_menu
#// 
#// Add appearance submenu items to the "Site Name" menu.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_appearance_menu(wp_admin_bar=None, *args_):
    
    wp_admin_bar.add_group(Array({"parent": "site-name", "id": "appearance"}))
    if current_user_can("switch_themes"):
        wp_admin_bar.add_node(Array({"parent": "appearance", "id": "themes", "title": __("Themes"), "href": admin_url("themes.php")}))
    # end if
    if (not current_user_can("edit_theme_options")):
        return
    # end if
    if current_theme_supports("widgets"):
        wp_admin_bar.add_node(Array({"parent": "appearance", "id": "widgets", "title": __("Widgets"), "href": admin_url("widgets.php")}))
    # end if
    if current_theme_supports("menus") or current_theme_supports("widgets"):
        wp_admin_bar.add_node(Array({"parent": "appearance", "id": "menus", "title": __("Menus"), "href": admin_url("nav-menus.php")}))
    # end if
    if current_theme_supports("custom-background"):
        wp_admin_bar.add_node(Array({"parent": "appearance", "id": "background", "title": __("Background"), "href": admin_url("themes.php?page=custom-background"), "meta": Array({"class": "hide-if-customize"})}))
    # end if
    if current_theme_supports("custom-header"):
        wp_admin_bar.add_node(Array({"parent": "appearance", "id": "header", "title": __("Header"), "href": admin_url("themes.php?page=custom-header"), "meta": Array({"class": "hide-if-customize"})}))
    # end if
# end def wp_admin_bar_appearance_menu
#// 
#// Provide an update link if theme/plugin/core updates are available.
#// 
#// @since 3.1.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_updates_menu(wp_admin_bar=None, *args_):
    
    update_data = wp_get_update_data()
    if (not update_data["counts"]["total"]):
        return
    # end if
    title = "<span class=\"ab-icon\"></span><span class=\"ab-label\">" + number_format_i18n(update_data["counts"]["total"]) + "</span>"
    title += "<span class=\"screen-reader-text\">" + update_data["title"] + "</span>"
    wp_admin_bar.add_node(Array({"id": "updates", "title": title, "href": network_admin_url("update-core.php"), "meta": Array({"title": update_data["title"]})}))
# end def wp_admin_bar_updates_menu
#// 
#// Add search form.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_search_menu(wp_admin_bar=None, *args_):
    
    if is_admin():
        return
    # end if
    form = "<form action=\"" + esc_url(home_url("/")) + "\" method=\"get\" id=\"adminbarsearch\">"
    form += "<input class=\"adminbar-input\" name=\"s\" id=\"adminbar-search\" type=\"text\" value=\"\" maxlength=\"150\" />"
    form += "<label for=\"adminbar-search\" class=\"screen-reader-text\">" + __("Search") + "</label>"
    form += "<input type=\"submit\" class=\"adminbar-button\" value=\"" + __("Search") + "\"/>"
    form += "</form>"
    wp_admin_bar.add_node(Array({"parent": "top-secondary", "id": "search", "title": form, "meta": Array({"class": "admin-bar-search", "tabindex": -1})}))
# end def wp_admin_bar_search_menu
#// 
#// Add a link to exit recovery mode when Recovery Mode is active.
#// 
#// @since 5.2.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_recovery_mode_menu(wp_admin_bar=None, *args_):
    
    if (not wp_is_recovery_mode()):
        return
    # end if
    url = wp_login_url()
    url = add_query_arg("action", WP_Recovery_Mode.EXIT_ACTION, url)
    url = wp_nonce_url(url, WP_Recovery_Mode.EXIT_ACTION)
    wp_admin_bar.add_node(Array({"parent": "top-secondary", "id": "recovery-mode", "title": __("Exit Recovery Mode"), "href": url}))
# end def wp_admin_bar_recovery_mode_menu
#// 
#// Add secondary menus.
#// 
#// @since 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar
#//
def wp_admin_bar_add_secondary_groups(wp_admin_bar=None, *args_):
    
    wp_admin_bar.add_group(Array({"id": "top-secondary", "meta": Array({"class": "ab-top-secondary"})}))
    wp_admin_bar.add_group(Array({"parent": "wp-logo", "id": "wp-logo-external", "meta": Array({"class": "ab-sub-secondary"})}))
# end def wp_admin_bar_add_secondary_groups
#// 
#// Style and scripts for the admin bar.
#// 
#// @since 3.1.0
#//
def wp_admin_bar_header(*args_):
    
    type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
    php_print("<style")
    php_print(type_attr)
    php_print(" media=\"print\">#wpadminbar { display:none; }</style>\n ")
# end def wp_admin_bar_header
#// 
#// Default admin bar callback.
#// 
#// @since 3.1.0
#//
def _admin_bar_bump_cb(*args_):
    
    type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
    php_print("<style")
    php_print(type_attr)
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
def show_admin_bar(show=None, *args_):
    
    global show_admin_bar
    php_check_if_defined("show_admin_bar")
    show_admin_bar = php_bool(show)
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
def is_admin_bar_showing(*args_):
    
    global show_admin_bar,pagenow
    php_check_if_defined("show_admin_bar","pagenow")
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
    if (not (php_isset(lambda : show_admin_bar))):
        if (not is_user_logged_in()) or "wp-login.php" == pagenow:
            show_admin_bar = False
        else:
            show_admin_bar = _get_admin_bar_pref()
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
    show_admin_bar = apply_filters("show_admin_bar", show_admin_bar)
    return show_admin_bar
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
def _get_admin_bar_pref(context="front", user=0, *args_):
    
    pref = get_user_option(str("show_admin_bar_") + str(context), user)
    if False == pref:
        return True
    # end if
    return "true" == pref
# end def _get_admin_bar_pref
