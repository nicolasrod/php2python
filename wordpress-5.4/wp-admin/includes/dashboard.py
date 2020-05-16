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
#// WordPress Dashboard Widget Administration Screen API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Registers dashboard widgets.
#// 
#// Handles POST data, sets up filters.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_registered_widgets
#// @global array $wp_registered_widget_controls
#// @global array $wp_dashboard_control_callbacks
#//
def wp_dashboard_setup(*args_):
    
    global wp_registered_widgets,wp_registered_widget_controls,wp_dashboard_control_callbacks
    php_check_if_defined("wp_registered_widgets","wp_registered_widget_controls","wp_dashboard_control_callbacks")
    wp_dashboard_control_callbacks = Array()
    screen = get_current_screen()
    #// Register Widgets and Controls
    response = wp_check_browser_version()
    if response and response["upgrade"]:
        add_filter("postbox_classes_dashboard_dashboard_browser_nag", "dashboard_browser_nag_class")
        if response["insecure"]:
            wp_add_dashboard_widget("dashboard_browser_nag", __("You are using an insecure browser!"), "wp_dashboard_browser_nag")
        else:
            wp_add_dashboard_widget("dashboard_browser_nag", __("Your browser is out of date!"), "wp_dashboard_browser_nag")
        # end if
    # end if
    #// PHP Version.
    response = wp_check_php_version()
    if response and (php_isset(lambda : response["is_acceptable"])) and (not response["is_acceptable"]) and current_user_can("update_php"):
        add_filter("postbox_classes_dashboard_dashboard_php_nag", "dashboard_php_nag_class")
        wp_add_dashboard_widget("dashboard_php_nag", __("PHP Update Required"), "wp_dashboard_php_nag")
    # end if
    #// Site Health.
    if current_user_can("view_site_health_checks") and (not is_network_admin()):
        if (not php_class_exists("WP_Site_Health")):
            php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
        # end if
        WP_Site_Health.get_instance()
        wp_enqueue_style("site-health")
        wp_enqueue_script("site-health")
        wp_add_dashboard_widget("dashboard_site_health", __("Site Health Status"), "wp_dashboard_site_health")
    # end if
    #// Right Now.
    if is_blog_admin() and current_user_can("edit_posts"):
        wp_add_dashboard_widget("dashboard_right_now", __("At a Glance"), "wp_dashboard_right_now")
    # end if
    if is_network_admin():
        wp_add_dashboard_widget("network_dashboard_right_now", __("Right Now"), "wp_network_dashboard_right_now")
    # end if
    #// Activity Widget.
    if is_blog_admin():
        wp_add_dashboard_widget("dashboard_activity", __("Activity"), "wp_dashboard_site_activity")
    # end if
    #// QuickPress Widget.
    if is_blog_admin() and current_user_can(get_post_type_object("post").cap.create_posts):
        quick_draft_title = php_sprintf("<span class=\"hide-if-no-js\">%1$s</span> <span class=\"hide-if-js\">%2$s</span>", __("Quick Draft"), __("Your Recent Drafts"))
        wp_add_dashboard_widget("dashboard_quick_press", quick_draft_title, "wp_dashboard_quick_press")
    # end if
    #// WordPress Events and News.
    wp_add_dashboard_widget("dashboard_primary", __("WordPress Events and News"), "wp_dashboard_events_news")
    if is_network_admin():
        #// 
        #// Fires after core widgets for the Network Admin dashboard have been registered.
        #// 
        #// @since 3.1.0
        #//
        do_action("wp_network_dashboard_setup")
        #// 
        #// Filters the list of widgets to load for the Network Admin dashboard.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[] $dashboard_widgets An array of dashboard widget IDs.
        #//
        dashboard_widgets = apply_filters("wp_network_dashboard_widgets", Array())
    elif is_user_admin():
        #// 
        #// Fires after core widgets for the User Admin dashboard have been registered.
        #// 
        #// @since 3.1.0
        #//
        do_action("wp_user_dashboard_setup")
        #// 
        #// Filters the list of widgets to load for the User Admin dashboard.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[] $dashboard_widgets An array of dashboard widget IDs.
        #//
        dashboard_widgets = apply_filters("wp_user_dashboard_widgets", Array())
    else:
        #// 
        #// Fires after core widgets for the admin dashboard have been registered.
        #// 
        #// @since 2.5.0
        #//
        do_action("wp_dashboard_setup")
        #// 
        #// Filters the list of widgets to load for the admin dashboard.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string[] $dashboard_widgets An array of dashboard widget IDs.
        #//
        dashboard_widgets = apply_filters("wp_dashboard_widgets", Array())
    # end if
    for widget_id in dashboard_widgets:
        name = wp_registered_widgets[widget_id]["name"] if php_empty(lambda : wp_registered_widgets[widget_id]["all_link"]) else wp_registered_widgets[widget_id]["name"] + str(" <a href='") + str(wp_registered_widgets[widget_id]["all_link"]) + str("' class='edit-box open-box'>") + __("View all") + "</a>"
        wp_add_dashboard_widget(widget_id, name, wp_registered_widgets[widget_id]["callback"], wp_registered_widget_controls[widget_id]["callback"])
    # end for
    if "POST" == PHP_SERVER["REQUEST_METHOD"] and (php_isset(lambda : PHP_POST["widget_id"])):
        check_admin_referer("edit-dashboard-widget_" + PHP_POST["widget_id"], "dashboard-widget-nonce")
        ob_start()
        #// Hack - but the same hack wp-admin/widgets.php uses.
        wp_dashboard_trigger_widget_control(PHP_POST["widget_id"])
        ob_end_clean()
        wp_redirect(remove_query_arg("edit"))
        php_exit(0)
    # end if
    #// This action is documented in wp-admin/includes/meta-boxes.php
    do_action("do_meta_boxes", screen.id, "normal", "")
    #// This action is documented in wp-admin/includes/meta-boxes.php
    do_action("do_meta_boxes", screen.id, "side", "")
# end def wp_dashboard_setup
#// 
#// Adds a new dashboard widget.
#// 
#// @since 2.7.0
#// 
#// @global array $wp_dashboard_control_callbacks
#// 
#// @param string   $widget_id        Widget ID  (used in the 'id' attribute for the widget).
#// @param string   $widget_name      Title of the widget.
#// @param callable $callback         Function that fills the widget with the desired content.
#// The function should echo its output.
#// @param callable $control_callback Optional. Function that outputs controls for the widget. Default null.
#// @param array    $callback_args    Optional. Data that should be set as the $args property of the widget array
#// (which is the second parameter passed to your callback). Default null.
#//
def wp_add_dashboard_widget(widget_id=None, widget_name=None, callback=None, control_callback=None, callback_args=None, *args_):
    
    screen = get_current_screen()
    global wp_dashboard_control_callbacks
    php_check_if_defined("wp_dashboard_control_callbacks")
    private_callback_args = Array({"__widget_basename": widget_name})
    if is_null(callback_args):
        callback_args = private_callback_args
    elif php_is_array(callback_args):
        callback_args = php_array_merge(callback_args, private_callback_args)
    # end if
    if control_callback and current_user_can("edit_dashboard") and php_is_callable(control_callback):
        wp_dashboard_control_callbacks[widget_id] = control_callback
        if (php_isset(lambda : PHP_REQUEST["edit"])) and widget_id == PHP_REQUEST["edit"]:
            url = php_explode("#", add_query_arg("edit", False), 2)
            widget_name += " <span class=\"postbox-title-action\"><a href=\"" + esc_url(url) + "\">" + __("Cancel") + "</a></span>"
            callback = "_wp_dashboard_control_callback"
        else:
            url = php_explode("#", add_query_arg("edit", widget_id), 2)
            widget_name += " <span class=\"postbox-title-action\"><a href=\"" + esc_url(str(url) + str("#") + str(widget_id)) + "\" class=\"edit-box open-box\">" + __("Configure") + "</a></span>"
        # end if
    # end if
    side_widgets = Array("dashboard_quick_press", "dashboard_primary")
    location = "normal"
    if php_in_array(widget_id, side_widgets):
        location = "side"
    # end if
    high_priority_widgets = Array("dashboard_browser_nag", "dashboard_php_nag")
    priority = "core"
    if php_in_array(widget_id, high_priority_widgets, True):
        priority = "high"
    # end if
    add_meta_box(widget_id, widget_name, callback, screen, location, priority, callback_args)
# end def wp_add_dashboard_widget
#// 
#// Outputs controls for the current dashboard widget.
#// 
#// @access private
#// @since 2.7.0
#// 
#// @param mixed $dashboard
#// @param array $meta_box
#//
def _wp_dashboard_control_callback(dashboard=None, meta_box=None, *args_):
    
    php_print("<form method=\"post\" class=\"dashboard-widget-control-form wp-clearfix\">")
    wp_dashboard_trigger_widget_control(meta_box["id"])
    wp_nonce_field("edit-dashboard-widget_" + meta_box["id"], "dashboard-widget-nonce")
    php_print("<input type=\"hidden\" name=\"widget_id\" value=\"" + esc_attr(meta_box["id"]) + "\" />")
    submit_button(__("Submit"))
    php_print("</form>")
# end def _wp_dashboard_control_callback
#// 
#// Displays the dashboard.
#// 
#// @since 2.5.0
#//
def wp_dashboard(*args_):
    
    screen = get_current_screen()
    columns = absint(screen.get_columns())
    columns_css = ""
    if columns:
        columns_css = str(" columns-") + str(columns)
    # end if
    php_print("<div id=\"dashboard-widgets\" class=\"metabox-holder")
    php_print(columns_css)
    php_print("\">\n    <div id=\"postbox-container-1\" class=\"postbox-container\">\n  ")
    do_meta_boxes(screen.id, "normal", "")
    php_print(" </div>\n    <div id=\"postbox-container-2\" class=\"postbox-container\">\n  ")
    do_meta_boxes(screen.id, "side", "")
    php_print(" </div>\n    <div id=\"postbox-container-3\" class=\"postbox-container\">\n  ")
    do_meta_boxes(screen.id, "column3", "")
    php_print(" </div>\n    <div id=\"postbox-container-4\" class=\"postbox-container\">\n  ")
    do_meta_boxes(screen.id, "column4", "")
    php_print("""   </div>
    </div>
    """)
    wp_nonce_field("closedpostboxes", "closedpostboxesnonce", False)
    wp_nonce_field("meta-box-order", "meta-box-order-nonce", False)
# end def wp_dashboard
#// 
#// Dashboard Widgets.
#// 
#// 
#// Dashboard widget that displays some basic stats about the site.
#// 
#// Formerly 'Right Now'. A streamlined 'At a Glance' as of 3.8.
#// 
#// @since 2.7.0
#//
def wp_dashboard_right_now(*args_):
    
    php_print(" <div class=\"main\">\n  <ul>\n  ")
    #// Posts and Pages.
    for post_type in Array("post", "page"):
        num_posts = wp_count_posts(post_type)
        if num_posts and num_posts.publish:
            if "post" == post_type:
                #// translators: %s: Number of posts.
                text = _n("%s Post", "%s Posts", num_posts.publish)
            else:
                #// translators: %s: Number of pages.
                text = _n("%s Page", "%s Pages", num_posts.publish)
            # end if
            text = php_sprintf(text, number_format_i18n(num_posts.publish))
            post_type_object = get_post_type_object(post_type)
            if post_type_object and current_user_can(post_type_object.cap.edit_posts):
                printf("<li class=\"%1$s-count\"><a href=\"edit.php?post_type=%1$s\">%2$s</a></li>", post_type, text)
            else:
                printf("<li class=\"%1$s-count\"><span>%2$s</span></li>", post_type, text)
            # end if
        # end if
    # end for
    #// Comments.
    num_comm = wp_count_comments()
    if num_comm and num_comm.approved or num_comm.moderated:
        #// translators: %s: Number of comments.
        text = php_sprintf(_n("%s Comment", "%s Comments", num_comm.approved), number_format_i18n(num_comm.approved))
        php_print("     <li class=\"comment-count\"><a href=\"edit-comments.php\">")
        php_print(text)
        php_print("</a></li>\n      ")
        moderated_comments_count_i18n = number_format_i18n(num_comm.moderated)
        #// translators: %s: Number of comments.
        text = php_sprintf(_n("%s Comment in moderation", "%s Comments in moderation", num_comm.moderated), moderated_comments_count_i18n)
        php_print("     <li class=\"comment-mod-count\n     ")
        if (not num_comm.moderated):
            php_print(" hidden")
        # end if
        php_print("     \"><a href=\"edit-comments.php?comment_status=moderated\" class=\"comments-in-moderation-text\">")
        php_print(text)
        php_print("</a></li>\n      ")
    # end if
    #// 
    #// Filters the array of extra elements to list in the 'At a Glance'
    #// dashboard widget.
    #// 
    #// Prior to 3.8.0, the widget was named 'Right Now'. Each element
    #// is wrapped in list-item tags on output.
    #// 
    #// @since 3.8.0
    #// 
    #// @param string[] $items Array of extra 'At a Glance' widget items.
    #//
    elements = apply_filters("dashboard_glance_items", Array())
    if elements:
        php_print("<li>" + php_implode("</li>\n<li>", elements) + "</li>\n")
    # end if
    php_print(" </ul>\n ")
    update_right_now_message()
    #// Check if search engines are asked not to index this site.
    if (not is_network_admin()) and (not is_user_admin()) and current_user_can("manage_options") and "0" == get_option("blog_public"):
        #// 
        #// Filters the link title attribute for the 'Search Engines Discouraged'
        #// message displayed in the 'At a Glance' dashboard widget.
        #// 
        #// Prior to 3.8.0, the widget was named 'Right Now'.
        #// 
        #// @since 3.0.0
        #// @since 4.5.0 The default for `$title` was updated to an empty string.
        #// 
        #// @param string $title Default attribute text.
        #//
        title = apply_filters("privacy_on_link_title", "")
        #// 
        #// Filters the link label for the 'Search Engines Discouraged' message
        #// displayed in the 'At a Glance' dashboard widget.
        #// 
        #// Prior to 3.8.0, the widget was named 'Right Now'.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $content Default text.
        #//
        content = apply_filters("privacy_on_link_text", __("Search Engines Discouraged"))
        title_attr = "" if "" == title else str(" title='") + str(title) + str("'")
        php_print(str("<p><a href='options-reading.php'") + str(title_attr) + str(">") + str(content) + str("</a></p>"))
    # end if
    php_print(" </div>\n    ")
    #// 
    #// activity_box_end has a core action, but only prints content when multisite.
    #// Using an output buffer is the only way to really check if anything's displayed here.
    #//
    ob_start()
    #// 
    #// Fires at the end of the 'At a Glance' dashboard widget.
    #// 
    #// Prior to 3.8.0, the widget was named 'Right Now'.
    #// 
    #// @since 2.5.0
    #//
    do_action("rightnow_end")
    #// 
    #// Fires at the end of the 'At a Glance' dashboard widget.
    #// 
    #// Prior to 3.8.0, the widget was named 'Right Now'.
    #// 
    #// @since 2.0.0
    #//
    do_action("activity_box_end")
    actions = ob_get_clean()
    if (not php_empty(lambda : actions)):
        php_print(" <div class=\"sub\">\n       ")
        php_print(actions)
        php_print(" </div>\n        ")
    # end if
# end def wp_dashboard_right_now
#// 
#// @since 3.1.0
#//
def wp_network_dashboard_right_now(*args_):
    
    actions = Array()
    if current_user_can("create_sites"):
        actions["create-site"] = "<a href=\"" + network_admin_url("site-new.php") + "\">" + __("Create a New Site") + "</a>"
    # end if
    if current_user_can("create_users"):
        actions["create-user"] = "<a href=\"" + network_admin_url("user-new.php") + "\">" + __("Create a New User") + "</a>"
    # end if
    c_users = get_user_count()
    c_blogs = get_blog_count()
    #// translators: %s: Number of users on the network.
    user_text = php_sprintf(_n("%s user", "%s users", c_users), number_format_i18n(c_users))
    #// translators: %s: Number of sites on the network.
    blog_text = php_sprintf(_n("%s site", "%s sites", c_blogs), number_format_i18n(c_blogs))
    #// translators: 1: Text indicating the number of sites on the network, 2: Text indicating the number of users on the network.
    sentence = php_sprintf(__("You have %1$s and %2$s."), blog_text, user_text)
    if actions:
        php_print("<ul class=\"subsubsub\">")
        for class_,action in actions:
            actions[class_] = str(" <li class='") + str(class_) + str("'>") + str(action)
        # end for
        php_print(php_implode(" |</li>\n", actions) + "</li>\n")
        php_print("</ul>")
    # end if
    php_print(" <br class=\"clear\" />\n\n  <p class=\"youhave\">")
    php_print(sentence)
    php_print("""</p>
    """)
    #// 
    #// Fires in the Network Admin 'Right Now' dashboard widget
    #// just before the user and site search form fields.
    #// 
    #// @since MU (3.0.0)
    #//
    do_action("wpmuadminresult")
    php_print("\n   <form action=\"")
    php_print(network_admin_url("users.php"))
    php_print("\" method=\"get\">\n     <p>\n           <label class=\"screen-reader-text\" for=\"search-users\">")
    _e("Search Users")
    php_print("</label>\n           <input type=\"search\" name=\"s\" value=\"\" size=\"30\" autocomplete=\"off\" id=\"search-users\"/>\n           ")
    submit_button(__("Search Users"), "", False, False, Array({"id": "submit_users"}))
    php_print("""       </p>
    </form>
    <form action=\"""")
    php_print(network_admin_url("sites.php"))
    php_print("\" method=\"get\">\n     <p>\n           <label class=\"screen-reader-text\" for=\"search-sites\">")
    _e("Search Sites")
    php_print("</label>\n           <input type=\"search\" name=\"s\" value=\"\" size=\"30\" autocomplete=\"off\" id=\"search-sites\"/>\n           ")
    submit_button(__("Search Sites"), "", False, False, Array({"id": "submit_sites"}))
    php_print("     </p>\n  </form>\n   ")
    #// 
    #// Fires at the end of the 'Right Now' widget in the Network Admin dashboard.
    #// 
    #// @since MU (3.0.0)
    #//
    do_action("mu_rightnow_end")
    #// 
    #// Fires at the end of the 'Right Now' widget in the Network Admin dashboard.
    #// 
    #// @since MU (3.0.0)
    #//
    do_action("mu_activity_box_end")
# end def wp_network_dashboard_right_now
#// 
#// The Quick Draft widget display and creation of drafts.
#// 
#// @since 3.8.0
#// 
#// @global int $post_ID
#// 
#// @param string $error_msg Optional. Error message. Default false.
#//
def wp_dashboard_quick_press(error_msg=False, *args_):
    
    global post_ID
    php_check_if_defined("post_ID")
    if (not current_user_can("edit_posts")):
        return
    # end if
    #// Check if a new auto-draft (= no new post_ID) is needed or if the old can be used
    last_post_id = php_int(get_user_option("dashboard_quick_press_last_post_id"))
    #// Get the last post_ID.
    if last_post_id:
        post = get_post(last_post_id)
        if php_empty(lambda : post) or "auto-draft" != post.post_status:
            #// auto-draft doesn't exist anymore.
            post = get_default_post_to_edit("post", True)
            update_user_option(get_current_user_id(), "dashboard_quick_press_last_post_id", php_int(post.ID))
            pass
        else:
            post.post_title = ""
            pass
        # end if
    else:
        post = get_default_post_to_edit("post", True)
        user_id = get_current_user_id()
        #// Don't create an option if this is a super admin who does not belong to this site.
        if php_in_array(get_current_blog_id(), php_array_keys(get_blogs_of_user(user_id))):
            update_user_option(user_id, "dashboard_quick_press_last_post_id", php_int(post.ID))
            pass
        # end if
    # end if
    post_ID = php_int(post.ID)
    php_print("\n   <form name=\"post\" action=\"")
    php_print(esc_url(admin_url("post.php")))
    php_print("\" method=\"post\" id=\"quick-press\" class=\"initial-form hide-if-no-js\">\n\n      ")
    if error_msg:
        php_print("     <div class=\"error\">")
        php_print(error_msg)
        php_print("</div>\n     ")
    # end if
    php_print("""
    <div class=\"input-text-wrap\" id=\"title-wrap\">
    <label for=\"title\">
    """)
    #// This filter is documented in wp-admin/edit-form-advanced.php
    php_print(apply_filters("enter_title_here", __("Title"), post))
    php_print("""           </label>
    <input type=\"text\" name=\"post_title\" id=\"title\" autocomplete=\"off\" />
    </div>
    <div class=\"textarea-wrap\" id=\"description-wrap\">
    <label for=\"content\">""")
    _e("Content")
    php_print("</label>\n           <textarea name=\"content\" id=\"content\" placeholder=\"")
    esc_attr_e("What&#8217;s on your mind?")
    php_print("""\" class=\"mceEditor\" rows=\"3\" cols=\"15\" autocomplete=\"off\"></textarea>
    </div>
    <p class=\"submit\">
    <input type=\"hidden\" name=\"action\" id=\"quickpost-action\" value=\"post-quickdraft-save\" />
    <input type=\"hidden\" name=\"post_ID\" value=\"""")
    php_print(post_ID)
    php_print("\" />\n          <input type=\"hidden\" name=\"post_type\" value=\"post\" />\n           ")
    wp_nonce_field("add-post")
    php_print("         ")
    submit_button(__("Save Draft"), "primary", "save", False, Array({"id": "save-post"}))
    php_print("""           <br class=\"clear\" />
    </p>
    </form>
    """)
    wp_dashboard_recent_drafts()
# end def wp_dashboard_quick_press
#// 
#// Show recent drafts of the user on the dashboard.
#// 
#// @since 2.7.0
#// 
#// @param WP_Post[] $drafts Optional. Array of posts to display. Default false.
#//
def wp_dashboard_recent_drafts(drafts=False, *args_):
    
    if (not drafts):
        query_args = Array({"post_type": "post", "post_status": "draft", "author": get_current_user_id(), "posts_per_page": 4, "orderby": "modified", "order": "DESC"})
        #// 
        #// Filters the post query arguments for the 'Recent Drafts' dashboard widget.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array $query_args The query arguments for the 'Recent Drafts' dashboard widget.
        #//
        query_args = apply_filters("dashboard_recent_drafts_query_args", query_args)
        drafts = get_posts(query_args)
        if (not drafts):
            return
        # end if
    # end if
    php_print("<div class=\"drafts\">")
    if php_count(drafts) > 3:
        printf("<p class=\"view-all\"><a href=\"%s\">%s</a></p>" + "\n", esc_url(admin_url("edit.php?post_status=draft")), __("View all drafts"))
    # end if
    php_print("<h2 class=\"hide-if-no-js\">" + __("Your Recent Drafts") + "</h2>\n<ul>")
    #// translators: Maximum number of words used in a preview of a draft on the dashboard.
    draft_length = php_intval(_x("10", "draft_length"))
    drafts = php_array_slice(drafts, 0, 3)
    for draft in drafts:
        url = get_edit_post_link(draft.ID)
        title = _draft_or_post_title(draft.ID)
        php_print("<li>\n")
        printf("<div class=\"draft-title\"><a href=\"%s\" aria-label=\"%s\">%s</a><time datetime=\"%s\">%s</time></div>", esc_url(url), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), title)), esc_html(title), get_the_time("c", draft), get_the_time(__("F j, Y"), draft))
        the_content = wp_trim_words(draft.post_content, draft_length)
        if the_content:
            php_print("<p>" + the_content + "</p>")
        # end if
        php_print("</li>\n")
    # end for
    php_print("</ul>\n</div>")
# end def wp_dashboard_recent_drafts
#// 
#// Outputs a row for the Recent Comments widget.
#// 
#// @access private
#// @since 2.7.0
#// 
#// @global WP_Comment $comment Global comment object.
#// 
#// @param WP_Comment $comment   The current comment.
#// @param bool       $show_date Optional. Whether to display the date.
#//
def _wp_dashboard_recent_comments_row(comment=None, show_date=True, *args_):
    global PHP_GLOBALS
    PHP_GLOBALS["comment"] = copy.deepcopy(comment)
    if comment.comment_post_ID > 0:
        comment_post_title = _draft_or_post_title(comment.comment_post_ID)
        comment_post_url = get_the_permalink(comment.comment_post_ID)
        comment_post_link = str("<a href='") + str(comment_post_url) + str("'>") + str(comment_post_title) + str("</a>")
    else:
        comment_post_link = ""
    # end if
    actions_string = ""
    if current_user_can("edit_comment", comment.comment_ID):
        #// Pre-order it: Approve | Reply | Edit | Spam | Trash.
        actions = Array({"approve": "", "unapprove": "", "reply": "", "edit": "", "spam": "", "trash": "", "delete": "", "view": ""})
        del_nonce = esc_html("_wpnonce=" + wp_create_nonce(str("delete-comment_") + str(comment.comment_ID)))
        approve_nonce = esc_html("_wpnonce=" + wp_create_nonce(str("approve-comment_") + str(comment.comment_ID)))
        approve_url = esc_url(str("comment.php?action=approvecomment&p=") + str(comment.comment_post_ID) + str("&c=") + str(comment.comment_ID) + str("&") + str(approve_nonce))
        unapprove_url = esc_url(str("comment.php?action=unapprovecomment&p=") + str(comment.comment_post_ID) + str("&c=") + str(comment.comment_ID) + str("&") + str(approve_nonce))
        spam_url = esc_url(str("comment.php?action=spamcomment&p=") + str(comment.comment_post_ID) + str("&c=") + str(comment.comment_ID) + str("&") + str(del_nonce))
        trash_url = esc_url(str("comment.php?action=trashcomment&p=") + str(comment.comment_post_ID) + str("&c=") + str(comment.comment_ID) + str("&") + str(del_nonce))
        delete_url = esc_url(str("comment.php?action=deletecomment&p=") + str(comment.comment_post_ID) + str("&c=") + str(comment.comment_ID) + str("&") + str(del_nonce))
        actions["approve"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-a aria-button-if-js\" aria-label=\"%s\">%s</a>", approve_url, str("dim:the-comment-list:comment-") + str(comment.comment_ID) + str(":unapproved:e7e7d3:e7e7d3:new=approved"), esc_attr__("Approve this comment"), __("Approve"))
        actions["unapprove"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-u aria-button-if-js\" aria-label=\"%s\">%s</a>", unapprove_url, str("dim:the-comment-list:comment-") + str(comment.comment_ID) + str(":unapproved:e7e7d3:e7e7d3:new=unapproved"), esc_attr__("Unapprove this comment"), __("Unapprove"))
        actions["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", str("comment.php?action=editcomment&amp;c=") + str(comment.comment_ID), esc_attr__("Edit this comment"), __("Edit"))
        actions["reply"] = php_sprintf("<button type=\"button\" onclick=\"window.commentReply && commentReply.open('%s','%s');\" class=\"vim-r button-link hide-if-no-js\" aria-label=\"%s\">%s</button>", comment.comment_ID, comment.comment_post_ID, esc_attr__("Reply to this comment"), __("Reply"))
        actions["spam"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"vim-s vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", spam_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str("::spam=1"), esc_attr__("Mark this comment as spam"), _x("Spam", "verb"))
        if (not EMPTY_TRASH_DAYS):
            actions["delete"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"delete vim-d vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", delete_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str("::trash=1"), esc_attr__("Delete this comment permanently"), __("Delete Permanently"))
        else:
            actions["trash"] = php_sprintf("<a href=\"%s\" data-wp-lists=\"%s\" class=\"delete vim-d vim-destructive aria-button-if-js\" aria-label=\"%s\">%s</a>", trash_url, str("delete:the-comment-list:comment-") + str(comment.comment_ID) + str("::trash=1"), esc_attr__("Move this comment to the Trash"), _x("Trash", "verb"))
        # end if
        actions["view"] = php_sprintf("<a class=\"comment-link\" href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(get_comment_link(comment)), esc_attr__("View this comment"), __("View"))
        #// 
        #// Filters the action links displayed for each comment in the 'Recent Comments'
        #// dashboard widget.
        #// 
        #// @since 2.6.0
        #// 
        #// @param string[]   $actions An array of comment actions. Default actions include:
        #// 'Approve', 'Unapprove', 'Edit', 'Reply', 'Spam',
        #// 'Delete', and 'Trash'.
        #// @param WP_Comment $comment The comment object.
        #//
        actions = apply_filters("comment_row_actions", php_array_filter(actions), comment)
        i = 0
        for action,link in actions:
            i += 1
            sep = "" if "approve" == action or "unapprove" == action and 2 == i or 1 == i else " | "
            #// Reply and quickedit need a hide-if-no-js span.
            if "reply" == action or "quickedit" == action:
                action += " hide-if-no-js"
            # end if
            if "view" == action and "1" != comment.comment_approved:
                action += " hidden"
            # end if
            actions_string += str("<span class='") + str(action) + str("'>") + str(sep) + str(link) + str("</span>")
        # end for
    # end if
    php_print("\n       <li id=\"comment-")
    php_print(comment.comment_ID)
    php_print("\" ")
    comment_class(Array("comment-item", wp_get_comment_status(comment)), comment)
    php_print(">\n\n            ")
    comment_row_class = ""
    if get_option("show_avatars"):
        php_print(get_avatar(comment, 50, "mystery"))
        comment_row_class += " has-avatar"
    # end if
    php_print("\n           ")
    if (not comment.comment_type) or "comment" == comment.comment_type:
        php_print("\n           <div class=\"dashboard-comment-wrap has-row-actions ")
        php_print(comment_row_class)
        php_print("\">\n            <p class=\"comment-meta\">\n                ")
        #// Comments might not have a post they relate to, e.g. programmatically created ones.
        if comment_post_link:
            printf(__("From %1$s on %2$s %3$s"), "<cite class=\"comment-author\">" + get_comment_author_link(comment) + "</cite>", comment_post_link, "<span class=\"approve\">" + __("[Pending]") + "</span>")
        else:
            printf(__("From %1$s %2$s"), "<cite class=\"comment-author\">" + get_comment_author_link(comment) + "</cite>", "<span class=\"approve\">" + __("[Pending]") + "</span>")
        # end if
        php_print("         </p>\n\n                ")
    else:
        for case in Switch(comment.comment_type):
            if case("pingback"):
                type = __("Pingback")
                break
            # end if
            if case("trackback"):
                type = __("Trackback")
                break
            # end if
            if case():
                type = ucwords(comment.comment_type)
            # end if
        # end for
        type = esc_html(type)
        php_print("         <div class=\"dashboard-comment-wrap has-row-actions\">\n            <p class=\"comment-meta\">\n                ")
        #// Pingbacks, Trackbacks or custom comment types might not have a post they relate to, e.g. programmatically created ones.
        if comment_post_link:
            printf(_x("%1$s on %2$s %3$s", "dashboard"), str("<strong>") + str(type) + str("</strong>"), comment_post_link, "<span class=\"approve\">" + __("[Pending]") + "</span>")
        else:
            printf(_x("%1$s %2$s", "dashboard"), str("<strong>") + str(type) + str("</strong>"), "<span class=\"approve\">" + __("[Pending]") + "</span>")
        # end if
        php_print("         </p>\n          <p class=\"comment-author\">")
        comment_author_link(comment)
        php_print("</p>\n\n         ")
    # end if
    pass
    php_print("         <blockquote><p>")
    comment_excerpt(comment)
    php_print("</p></blockquote>\n          ")
    if actions_string:
        php_print("         <p class=\"row-actions\">")
        php_print(actions_string)
        php_print("</p>\n           ")
    # end if
    php_print("         </div>\n        </li>\n ")
    PHP_GLOBALS["comment"] = None
# end def _wp_dashboard_recent_comments_row
#// 
#// Callback function for Activity widget.
#// 
#// @since 3.8.0
#//
def wp_dashboard_site_activity(*args_):
    
    php_print("<div id=\"activity-widget\">")
    future_posts = wp_dashboard_recent_posts(Array({"max": 5, "status": "future", "order": "ASC", "title": __("Publishing Soon"), "id": "future-posts"}))
    recent_posts = wp_dashboard_recent_posts(Array({"max": 5, "status": "publish", "order": "DESC", "title": __("Recently Published"), "id": "published-posts"}))
    recent_comments = wp_dashboard_recent_comments()
    if (not future_posts) and (not recent_posts) and (not recent_comments):
        php_print("<div class=\"no-activity\">")
        php_print("<p class=\"smiley\" aria-hidden=\"true\"></p>")
        php_print("<p>" + __("No activity yet!") + "</p>")
        php_print("</div>")
    # end if
    php_print("</div>")
# end def wp_dashboard_site_activity
#// 
#// Generates Publishing Soon and Recently Published sections.
#// 
#// @since 3.8.0
#// 
#// @param array $args {
#// An array of query and display arguments.
#// 
#// @type int    $max     Number of posts to display.
#// @type string $status  Post status.
#// @type string $order   Designates ascending ('ASC') or descending ('DESC') order.
#// @type string $title   Section title.
#// @type string $id      The container id.
#// }
#// @return bool False if no posts were found. True otherwise.
#//
def wp_dashboard_recent_posts(args=None, *args_):
    
    query_args = Array({"post_type": "post", "post_status": args["status"], "orderby": "date", "order": args["order"], "posts_per_page": php_intval(args["max"]), "no_found_rows": True, "cache_results": False, "perm": "editable" if "future" == args["status"] else "readable"})
    #// 
    #// Filters the query arguments used for the Recent Posts widget.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array $query_args The arguments passed to WP_Query to produce the list of posts.
    #//
    query_args = apply_filters("dashboard_recent_posts_query_args", query_args)
    posts = php_new_class("WP_Query", lambda : WP_Query(query_args))
    if posts.have_posts():
        php_print("<div id=\"" + args["id"] + "\" class=\"activity-block\">")
        php_print("<h3>" + args["title"] + "</h3>")
        php_print("<ul>")
        today = current_time("Y-m-d")
        tomorrow = current_datetime().modify("+1 day").format("Y-m-d")
        year = current_time("Y")
        while True:
            
            if not (posts.have_posts()):
                break
            # end if
            posts.the_post()
            time = get_the_time("U")
            if gmdate("Y-m-d", time) == today:
                relative = __("Today")
            elif gmdate("Y-m-d", time) == tomorrow:
                relative = __("Tomorrow")
            elif gmdate("Y", time) != year:
                #// translators: Date and time format for recent posts on the dashboard, from a different calendar year, see https://www.php.net/date
                relative = date_i18n(__("M jS Y"), time)
            else:
                #// translators: Date and time format for recent posts on the dashboard, see https://www.php.net/date
                relative = date_i18n(__("M jS"), time)
            # end if
            #// Use the post edit link for those who can edit, the permalink otherwise.
            recent_post_link = get_edit_post_link() if current_user_can("edit_post", get_the_ID()) else get_permalink()
            draft_or_post_title = _draft_or_post_title()
            printf("<li><span>%1$s</span> <a href=\"%2$s\" aria-label=\"%3$s\">%4$s</a></li>", php_sprintf(_x("%1$s, %2$s", "dashboard"), relative, get_the_time()), recent_post_link, esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), draft_or_post_title)), draft_or_post_title)
        # end while
        php_print("</ul>")
        php_print("</div>")
    else:
        return False
    # end if
    wp_reset_postdata()
    return True
# end def wp_dashboard_recent_posts
#// 
#// Show Comments section.
#// 
#// @since 3.8.0
#// 
#// @param int $total_items Optional. Number of comments to query. Default 5.
#// @return bool False if no comments were found. True otherwise.
#//
def wp_dashboard_recent_comments(total_items=5, *args_):
    
    #// Select all comment types and filter out spam later for better query performance.
    comments = Array()
    comments_query = Array({"number": total_items * 5, "offset": 0})
    if (not current_user_can("edit_posts")):
        comments_query["status"] = "approve"
    # end if
    while True:
        possible = get_comments(comments_query)
        if not (php_count(comments) < total_items and possible):
            break
        # end if
        if (not php_is_array(possible)):
            break
        # end if
        for comment in possible:
            if (not current_user_can("read_post", comment.comment_post_ID)):
                continue
            # end if
            comments[-1] = comment
            if php_count(comments) == total_items:
                break
            # end if
        # end for
        comments_query["offset"] += comments_query["number"]
        comments_query["number"] = total_items * 10
    # end while
    if comments:
        php_print("<div id=\"latest-comments\" class=\"activity-block\">")
        php_print("<h3>" + __("Recent Comments") + "</h3>")
        php_print("<ul id=\"the-comment-list\" data-wp-lists=\"list:comment\">")
        for comment in comments:
            _wp_dashboard_recent_comments_row(comment)
        # end for
        php_print("</ul>")
        if current_user_can("edit_posts"):
            php_print("<h3 class=\"screen-reader-text\">" + __("View more comments") + "</h3>")
            _get_list_table("WP_Comments_List_Table").views()
        # end if
        wp_comment_reply(-1, False, "dashboard", False)
        wp_comment_trashnotice()
        php_print("</div>")
    else:
        return False
    # end if
    return True
# end def wp_dashboard_recent_comments
#// 
#// Display generic dashboard RSS widget feed.
#// 
#// @since 2.5.0
#// 
#// @param string $widget_id
#//
def wp_dashboard_rss_output(widget_id=None, *args_):
    
    widgets = get_option("dashboard_widget_options")
    php_print("<div class=\"rss-widget\">")
    wp_widget_rss_output(widgets[widget_id])
    php_print("</div>")
# end def wp_dashboard_rss_output
#// 
#// Checks to see if all of the feed url in $check_urls are cached.
#// 
#// If $check_urls is empty, look for the rss feed url found in the dashboard
#// widget options of $widget_id. If cached, call $callback, a function that
#// echoes out output for this widget. If not cache, echo a "Loading..." stub
#// which is later replaced by Ajax call (see top of /wp-admin/index.php)
#// 
#// @since 2.5.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @param string   $widget_id  The widget ID.
#// @param callable $callback   The callback function used to display each feed.
#// @param array    $check_urls RSS feeds.
#// @param mixed    ...$args    Optional additional parameters to pass to the callback function.
#// @return bool True on success, false on failure.
#//
def wp_dashboard_cached_rss_widget(widget_id=None, callback=None, check_urls=Array(), *args):
    
    loading = "<p class=\"widget-loading hide-if-no-js\">" + __("Loading&hellip;") + "</p><div class=\"hide-if-js notice notice-error inline\"><p>" + __("This widget requires JavaScript.") + "</p></div>"
    doing_ajax = wp_doing_ajax()
    if php_empty(lambda : check_urls):
        widgets = get_option("dashboard_widget_options")
        if php_empty(lambda : widgets[widget_id]["url"]) and (not doing_ajax):
            php_print(loading)
            return False
        # end if
        check_urls = Array(widgets[widget_id]["url"])
    # end if
    locale = get_user_locale()
    cache_key = "dash_v2_" + php_md5(widget_id + "_" + locale)
    output = get_transient(cache_key)
    if False != output:
        php_print(output)
        return True
    # end if
    if (not doing_ajax):
        php_print(loading)
        return False
    # end if
    if callback and php_is_callable(callback):
        array_unshift(args, widget_id, check_urls)
        ob_start()
        call_user_func_array(callback, args)
        #// Default lifetime in cache of 12 hours (same as the feeds).
        set_transient(cache_key, ob_get_flush(), 12 * HOUR_IN_SECONDS)
    # end if
    return True
# end def wp_dashboard_cached_rss_widget
#// 
#// Dashboard Widgets Controls.
#// 
#// 
#// Calls widget control callback.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_dashboard_control_callbacks
#// 
#// @param int $widget_control_id Registered Widget ID.
#//
def wp_dashboard_trigger_widget_control(widget_control_id=False, *args_):
    
    global wp_dashboard_control_callbacks
    php_check_if_defined("wp_dashboard_control_callbacks")
    if is_scalar(widget_control_id) and widget_control_id and (php_isset(lambda : wp_dashboard_control_callbacks[widget_control_id])) and php_is_callable(wp_dashboard_control_callbacks[widget_control_id]):
        php_call_user_func(wp_dashboard_control_callbacks[widget_control_id], "", Array({"id": widget_control_id, "callback": wp_dashboard_control_callbacks[widget_control_id]}))
    # end if
# end def wp_dashboard_trigger_widget_control
#// 
#// The RSS dashboard widget control.
#// 
#// Sets up $args to be used as input to wp_widget_rss_form(). Handles POST data
#// from RSS-type widgets.
#// 
#// @since 2.5.0
#// 
#// @param string $widget_id
#// @param array $form_inputs
#//
def wp_dashboard_rss_control(widget_id=None, form_inputs=Array(), *args_):
    global PHP_POST
    widget_options = get_option("dashboard_widget_options")
    if (not widget_options):
        widget_options = Array()
    # end if
    if (not (php_isset(lambda : widget_options[widget_id]))):
        widget_options[widget_id] = Array()
    # end if
    number = 1
    #// Hack to use wp_widget_rss_form().
    widget_options[widget_id]["number"] = number
    if "POST" == PHP_SERVER["REQUEST_METHOD"] and (php_isset(lambda : PHP_POST["widget-rss"][number])):
        PHP_POST["widget-rss"][number] = wp_unslash(PHP_POST["widget-rss"][number])
        widget_options[widget_id] = wp_widget_rss_process(PHP_POST["widget-rss"][number])
        widget_options[widget_id]["number"] = number
        #// Title is optional. If black, fill it if possible.
        if (not widget_options[widget_id]["title"]) and (php_isset(lambda : PHP_POST["widget-rss"][number]["title"])):
            rss = fetch_feed(widget_options[widget_id]["url"])
            if is_wp_error(rss):
                widget_options[widget_id]["title"] = htmlentities(__("Unknown Feed"))
            else:
                widget_options[widget_id]["title"] = htmlentities(strip_tags(rss.get_title()))
                rss.__del__()
                rss = None
            # end if
        # end if
        update_option("dashboard_widget_options", widget_options)
        locale = get_user_locale()
        cache_key = "dash_v2_" + php_md5(widget_id + "_" + locale)
        delete_transient(cache_key)
    # end if
    wp_widget_rss_form(widget_options[widget_id], form_inputs)
# end def wp_dashboard_rss_control
#// 
#// Renders the Events and News dashboard widget.
#// 
#// @since 4.8.0
#//
def wp_dashboard_events_news(*args_):
    
    wp_print_community_events_markup()
    php_print("\n   <div class=\"wordpress-news hide-if-no-js\">\n      ")
    wp_dashboard_primary()
    php_print("""   </div>
    <p class=\"community-events-footer\">
    """)
    printf("<a href=\"%1$s\" target=\"_blank\">%2$s <span class=\"screen-reader-text\">%3$s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a>", "https://make.wordpress.org/community/meetups-landing-page", __("Meetups"), __("(opens in a new tab)"))
    php_print("""
    |
    """)
    printf("<a href=\"%1$s\" target=\"_blank\">%2$s <span class=\"screen-reader-text\">%3$s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a>", "https://central.wordcamp.org/schedule/", __("WordCamps"), __("(opens in a new tab)"))
    php_print("""
    |
    """)
    printf("<a href=\"%1$s\" target=\"_blank\">%2$s <span class=\"screen-reader-text\">%3$s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a>", esc_url(_x("https://wordpress.org/news/", "Events and News dashboard widget")), __("News"), __("(opens in a new tab)"))
    php_print(" </p>\n\n    ")
# end def wp_dashboard_events_news
#// 
#// Prints the markup for the Community Events section of the Events and News Dashboard widget.
#// 
#// @since 4.8.0
#//
def wp_print_community_events_markup(*args_):
    
    php_print("""
    <div class=\"community-events-errors notice notice-error inline hide-if-js\">
    <p class=\"hide-if-js\">
    """)
    _e("This widget requires JavaScript.")
    php_print("""       </p>
    <p class=\"community-events-error-occurred\" aria-hidden=\"true\">
    """)
    _e("An error occurred. Please try again.")
    php_print("""       </p>
    <p class=\"community-events-could-not-locate\" aria-hidden=\"true\"></p>
    </div>
    <div class=\"community-events-loading hide-if-no-js\">
    """)
    _e("Loading&hellip;")
    php_print(" </div>\n\n  ")
    pass
    php_print("""   <div id=\"community-events\" class=\"community-events\" aria-hidden=\"true\">
    <div class=\"activity-block\">
    <p>
    <span id=\"community-events-location-message\"></span>
    <button class=\"button-link community-events-toggle-location\" aria-label=\"""")
    esc_attr_e("Edit city")
    php_print("""\" aria-expanded=\"false\">
    <span class=\"dashicons dashicons-edit\"></span>
    </button>
    </p>
    <form class=\"community-events-form\" aria-hidden=\"true\" action=\"""")
    php_print(esc_url(admin_url("admin-ajax.php")))
    php_print("\" method=\"post\">\n                <label for=\"community-events-location\">\n                 ")
    _e("City:")
    php_print("             </label>\n              ")
    pass
    php_print("             <input id=\"community-events-location\" class=\"regular-text\" type=\"text\" name=\"community-events-location\" placeholder=\"")
    esc_attr_e("Cincinnati")
    php_print("\" />\n\n                ")
    submit_button(__("Submit"), "secondary", "community-events-submit", False)
    php_print("\n               <button class=\"community-events-cancel button-link\" type=\"button\" aria-expanded=\"false\">\n                    ")
    _e("Cancel")
    php_print("""               </button>
    <span class=\"spinner\"></span>
    </form>
    </div>
    <ul class=\"community-events-results activity-block last\"></ul>
    </div>
    """)
# end def wp_print_community_events_markup
#// 
#// Renders the events templates for the Event and News widget.
#// 
#// @since 4.8.0
#//
def wp_print_community_events_templates(*args_):
    
    php_print("\n   <script id=\"tmpl-community-events-attend-event-near\" type=\"text/template\">\n        ")
    printf(__("Attend an upcoming event near %s."), "<strong>{{ data.location.description }}</strong>")
    php_print("""   </script>
    <script id=\"tmpl-community-events-could-not-locate\" type=\"text/template\">
    """)
    printf(__("We couldn&#8217;t locate %s. Please try another nearby city. For example: Kansas City; Springfield; Portland."), "<em>{{data.unknownCity}}</em>")
    php_print("""   </script>
    <script id=\"tmpl-community-events-event-list\" type=\"text/template\">
    <# _.each( data.events, function( event ) { #>
    <li class=\"event event-{{ event.type }} wp-clearfix\">
    <div class=\"event-info\">
    <div class=\"dashicons event-icon\" aria-hidden=\"true\"></div>
    <div class=\"event-info-inner\">
    <a class=\"event-title\" href=\"{{ event.url }}\">{{ event.title }}</a>
    <span class=\"event-city\">{{ event.location.location }}</span>
    </div>
    </div>
    <div class=\"event-date-time\">
    <span class=\"event-date\">{{ event.formatted_date }}</span>
    <# if ( 'meetup' === event.type ) { #>
    <span class=\"event-time\">{{ event.formatted_time }}</span>
    <# } #>
    </div>
    </li>
    <# } ) #>
    </script>
    <script id=\"tmpl-community-events-no-upcoming-events\" type=\"text/template\">
    <li class=\"event-none\">
    <# if ( data.location.description ) { #>
    """)
    printf(__("There aren&#8217;t any events scheduled near %1$s at the moment. Would you like to <a href=\"%2$s\">organize one</a>?"), "{{ data.location.description }}", __("https://make.wordpress.org/community/handbook/meetup-organizer/welcome/"))
    php_print("\n           <# } else { #>\n                ")
    printf(__("There aren&#8217;t any events scheduled near you at the moment. Would you like to <a href=\"%s\">organize one</a>?"), __("https://make.wordpress.org/community/handbook/meetup-organizer/welcome/"))
    php_print("""           <# } #>
    </li>
    </script>
    """)
# end def wp_print_community_events_templates
#// 
#// 'WordPress Events and News' dashboard widget.
#// 
#// @since 2.7.0
#// @since 4.8.0 Removed popular plugins feed.
#//
def wp_dashboard_primary(*args_):
    
    feeds = Array({"news": Array({"link": apply_filters("dashboard_primary_link", __("https://wordpress.org/news/")), "url": apply_filters("dashboard_primary_feed", __("https://wordpress.org/news/feed/")), "title": apply_filters("dashboard_primary_title", __("WordPress Blog")), "items": 1, "show_summary": 0, "show_author": 0, "show_date": 0})}, {"planet": Array({"link": apply_filters("dashboard_secondary_link", __("https://planet.wordpress.org/")), "url": apply_filters("dashboard_secondary_feed", __("https://planet.wordpress.org/feed/")), "title": apply_filters("dashboard_secondary_title", __("Other WordPress News")), "items": apply_filters("dashboard_secondary_items", 3), "show_summary": 0, "show_author": 0, "show_date": 0})})
    wp_dashboard_cached_rss_widget("dashboard_primary", "wp_dashboard_primary_output", feeds)
# end def wp_dashboard_primary
#// 
#// Displays the WordPress events and news feeds.
#// 
#// @since 3.8.0
#// @since 4.8.0 Removed popular plugins feed.
#// 
#// @param string $widget_id Widget ID.
#// @param array  $feeds     Array of RSS feeds.
#//
def wp_dashboard_primary_output(widget_id=None, feeds=None, *args_):
    
    for type,args in feeds:
        args["type"] = type
        php_print("<div class=\"rss-widget\">")
        wp_widget_rss_output(args["url"], args)
        php_print("</div>")
    # end for
# end def wp_dashboard_primary_output
#// 
#// Displays file upload quota on dashboard.
#// 
#// Runs on the {@see 'activity_box_end'} hook in wp_dashboard_right_now().
#// 
#// @since 3.0.0
#// 
#// @return bool|null True if not multisite, user can't upload files, or the space check option is disabled.
#//
def wp_dashboard_quota(*args_):
    
    if (not is_multisite()) or (not current_user_can("upload_files")) or get_site_option("upload_space_check_disabled"):
        return True
    # end if
    quota = get_space_allowed()
    used = get_space_used()
    if used > quota:
        percentused = "100"
    else:
        percentused = used / quota * 100
    # end if
    used_class = " warning" if percentused >= 70 else ""
    used = round(used, 2)
    percentused = number_format(percentused)
    php_print(" <h3 class=\"mu-storage\">")
    _e("Storage Space")
    php_print("""</h3>
    <div class=\"mu-storage\">
    <ul>
    <li class=\"storage-count\">
    """)
    text = php_sprintf(__("%s MB Space Allowed"), number_format_i18n(quota))
    printf("<a href=\"%1$s\">%2$s <span class=\"screen-reader-text\">(%3$s)</span></a>", esc_url(admin_url("upload.php")), text, __("Manage Uploads"))
    php_print("     </li><li class=\"storage-count ")
    php_print(used_class)
    php_print("\">\n            ")
    text = php_sprintf(__("%1$s MB (%2$s%%) Space Used"), number_format_i18n(used, 2), percentused)
    printf("<a href=\"%1$s\" class=\"musublink\">%2$s <span class=\"screen-reader-text\">(%3$s)</span></a>", esc_url(admin_url("upload.php")), text, __("Manage Uploads"))
    php_print("""       </li>
    </ul>
    </div>
    """)
# end def wp_dashboard_quota
#// 
#// Displays the browser update nag.
#// 
#// @since 3.2.0
#//
def wp_dashboard_browser_nag(*args_):
    
    notice = ""
    response = wp_check_browser_version()
    if response:
        if response["insecure"]:
            msg = php_sprintf(__("It looks like you're using an insecure version of %s. Using an outdated browser makes your computer unsafe. For the best WordPress experience, please update your browser."), php_sprintf("<a href=\"%s\">%s</a>", esc_url(response["update_url"]), esc_html(response["name"])))
        else:
            msg = php_sprintf(__("It looks like you're using an old version of %s. For the best WordPress experience, please update your browser."), php_sprintf("<a href=\"%s\">%s</a>", esc_url(response["update_url"]), esc_html(response["name"])))
        # end if
        browser_nag_class = ""
        if (not php_empty(lambda : response["img_src"])):
            img_src = response["img_src_ssl"] if is_ssl() and (not php_empty(lambda : response["img_src_ssl"])) else response["img_src"]
            notice += "<div class=\"alignright browser-icon\"><a href=\"" + esc_attr(response["update_url"]) + "\"><img src=\"" + esc_attr(img_src) + "\" alt=\"\" /></a></div>"
            browser_nag_class = " has-browser-icon"
        # end if
        notice += str("<p class='browser-update-nag") + str(browser_nag_class) + str("'>") + str(msg) + str("</p>")
        browsehappy = "https://browsehappy.com/"
        locale = get_user_locale()
        if "en_US" != locale:
            browsehappy = add_query_arg("locale", locale, browsehappy)
        # end if
        notice += "<p>" + php_sprintf(__("<a href=\"%1$s\" class=\"update-browser-link\">Update %2$s</a> or learn how to <a href=\"%3$s\" class=\"browse-happy-link\">browse happy</a>"), esc_attr(response["update_url"]), esc_html(response["name"]), esc_url(browsehappy)) + "</p>"
        notice += "<p class=\"hide-if-no-js\"><a href=\"\" class=\"dismiss\" aria-label=\"" + esc_attr__("Dismiss the browser warning panel") + "\">" + __("Dismiss") + "</a></p>"
        notice += "<div class=\"clear\"></div>"
    # end if
    #// 
    #// Filters the notice output for the 'Browse Happy' nag meta box.
    #// 
    #// @since 3.2.0
    #// 
    #// @param string $notice   The notice content.
    #// @param array  $response An array containing web browser information. See `wp_check_browser_version()`.
    #//
    php_print(apply_filters("browse-happy-notice", notice, response))
    pass
# end def wp_dashboard_browser_nag
#// 
#// Adds an additional class to the browser nag if the current version is insecure.
#// 
#// @since 3.2.0
#// 
#// @param string[] $classes Array of meta box classes.
#// @return string[] Modified array of meta box classes.
#//
def dashboard_browser_nag_class(classes=None, *args_):
    
    response = wp_check_browser_version()
    if response and response["insecure"]:
        classes[-1] = "browser-insecure"
    # end if
    return classes
# end def dashboard_browser_nag_class
#// 
#// Checks if the user needs a browser update.
#// 
#// @since 3.2.0
#// 
#// @return array|bool Array of browser data on success, false on failure.
#//
def wp_check_browser_version(*args_):
    
    if php_empty(lambda : PHP_SERVER["HTTP_USER_AGENT"]):
        return False
    # end if
    key = php_md5(PHP_SERVER["HTTP_USER_AGENT"])
    response = get_site_transient("browser_" + key)
    if False == response:
        #// Include an unmodified $wp_version.
        php_include_file(ABSPATH + WPINC + "/version.php", once=False)
        url = "http://api.wordpress.org/core/browse-happy/1.1/"
        options = Array({"body": Array({"useragent": PHP_SERVER["HTTP_USER_AGENT"]})}, {"user-agent": "WordPress/" + wp_version + "; " + home_url("/")})
        if wp_http_supports(Array("ssl")):
            url = set_url_scheme(url, "https")
        # end if
        response = wp_remote_post(url, options)
        if is_wp_error(response) or 200 != wp_remote_retrieve_response_code(response):
            return False
        # end if
        #// 
        #// Response should be an array with:
        #// 'platform' - string - A user-friendly platform name, if it can be determined
        #// 'name' - string - A user-friendly browser name
        #// 'version' - string - The version of the browser the user is using
        #// 'current_version' - string - The most recent version of the browser
        #// 'upgrade' - boolean - Whether the browser needs an upgrade
        #// 'insecure' - boolean - Whether the browser is deemed insecure
        #// 'update_url' - string - The url to visit to upgrade
        #// 'img_src' - string - An image representing the browser
        #// 'img_src_ssl' - string - An image (over SSL) representing the browser
        #//
        response = php_json_decode(wp_remote_retrieve_body(response), True)
        if (not php_is_array(response)):
            return False
        # end if
        set_site_transient("browser_" + key, response, WEEK_IN_SECONDS)
    # end if
    return response
# end def wp_check_browser_version
#// 
#// Displays the PHP update nag.
#// 
#// @since 5.1.0
#//
def wp_dashboard_php_nag(*args_):
    
    response = wp_check_php_version()
    if (not response):
        return
    # end if
    if (php_isset(lambda : response["is_secure"])) and (not response["is_secure"]):
        msg = __("WordPress has detected that your site is running on an insecure version of PHP.")
    else:
        msg = __("WordPress has detected that your site is running on an outdated version of PHP.")
    # end if
    php_print(" <p>")
    php_print(msg)
    php_print("</p>\n\n <h3>")
    _e("What is PHP and how does it affect my site?")
    php_print("</h3>\n  <p>")
    _e("PHP is the programming language we use to build and maintain WordPress. Newer versions of PHP are both faster and more secure, so updating will have a positive effect on your site&#8217;s performance.")
    php_print("""</p>
    <p class=\"button-container\">
    """)
    printf("<a class=\"button button-primary\" href=\"%1$s\" target=\"_blank\" rel=\"noopener noreferrer\">%2$s <span class=\"screen-reader-text\">%3$s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a>", esc_url(wp_get_update_php_url()), __("Learn more about updating PHP"), __("(opens in a new tab)"))
    php_print(" </p>\n  ")
    wp_update_php_annotation()
    wp_direct_php_update_button()
# end def wp_dashboard_php_nag
#// 
#// Adds an additional class to the PHP nag if the current version is insecure.
#// 
#// @since 5.1.0
#// 
#// @param string[] $classes Array of meta box classes.
#// @return string[] Modified array of meta box classes.
#//
def dashboard_php_nag_class(classes=None, *args_):
    
    response = wp_check_php_version()
    if response and (php_isset(lambda : response["is_secure"])) and (not response["is_secure"]):
        classes[-1] = "php-insecure"
    # end if
    return classes
# end def dashboard_php_nag_class
#// 
#// Displays the Site Health Status widget.
#// 
#// @since 5.4.0
#//
def wp_dashboard_site_health(*args_):
    
    get_issues = get_transient("health-check-site-status-result")
    issue_counts = Array()
    if False != get_issues:
        issue_counts = php_json_decode(get_issues, True)
    # end if
    if (not php_is_array(issue_counts)) or (not issue_counts):
        issue_counts = Array({"good": 0, "recommended": 0, "critical": 0})
    # end if
    issues_total = issue_counts["recommended"] + issue_counts["critical"]
    php_print("""   <div class=\"health-check-title-section site-health-progress-wrapper loading hide-if-no-js\">
    <div class=\"site-health-progress\">
    <svg role=\"img\" aria-hidden=\"true\" focusable=\"false\" width=\"100%\" height=\"100%\" viewBox=\"0 0 200 200\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\">
    <circle r=\"90\" cx=\"100\" cy=\"100\" fill=\"transparent\" stroke-dasharray=\"565.48\" stroke-dashoffset=\"0\"></circle>
    <circle id=\"bar\" r=\"90\" cx=\"100\" cy=\"100\" fill=\"transparent\" stroke-dasharray=\"565.48\" stroke-dashoffset=\"0\"></circle>
    </svg>
    </div>
    <div class=\"site-health-progress-label\">
    """)
    if False == get_issues:
        php_print("             ")
        _e("No information yet&hellip;")
        php_print("         ")
    else:
        php_print("             ")
        _e("Results are still loading&hellip;")
        php_print("         ")
    # end if
    php_print("""       </div>
    </div>
    """)
    if False == get_issues:
        php_print("     <p>\n           ")
        printf(__("Site health checks will automatically run periodically to gather information about your site. You can also <a href=\"%s\">visit the Site Health screen</a> to gather information about your site now."), esc_url(admin_url("site-health.php")))
        php_print("     </p>\n  ")
    else:
        php_print("     <p>\n           ")
        if issue_counts["critical"] > 0:
            php_print("             ")
            _e("Your site has critical issues that should be addressed as soon as possible to improve its performance and security.")
            php_print("         ")
        elif issues_total <= 0:
            php_print("             ")
            _e("Great job! Your site currently passes all site health checks.")
            php_print("         ")
        else:
            php_print("             ")
            _e("Your site&#8217;s health is looking good, but there are still some things you can do to improve its performance and security.")
            php_print("         ")
        # end if
        php_print("     </p>\n  ")
    # end if
    php_print("\n   ")
    if issues_total > 0 and False != get_issues:
        php_print("     <p>\n           ")
        printf(_n("Take a look at the <strong>%1$d item</strong> on the <a href=\"%2$s\">Site Health screen</a>.", "Take a look at the <strong>%1$d items</strong> on the <a href=\"%2$s\">Site Health screen</a>.", issues_total), issues_total, esc_url(admin_url("site-health.php")))
        php_print("     </p>\n  ")
    # end if
    php_print("\n   ")
# end def wp_dashboard_site_health
#// 
#// Empty function usable by plugins to output empty dashboard widget (to be populated later by JS).
#// 
#// @since 2.5.0
#//
def wp_dashboard_empty(*args_):
    
    pass
# end def wp_dashboard_empty
#// 
#// Displays a welcome panel to introduce users to WordPress.
#// 
#// @since 3.3.0
#//
def wp_welcome_panel(*args_):
    
    php_print(" <div class=\"welcome-panel-content\">\n <h2>")
    _e("Welcome to WordPress!")
    php_print("</h2>\n  <p class=\"about-description\">")
    _e("We&#8217;ve assembled some links to get you started:")
    php_print("""</p>
    <div class=\"welcome-panel-column-container\">
    <div class=\"welcome-panel-column\">
    """)
    if current_user_can("customize"):
        php_print("         <h3>")
        _e("Get Started")
        php_print("</h3>\n          <a class=\"button button-primary button-hero load-customize hide-if-no-customize\" href=\"")
        php_print(wp_customize_url())
        php_print("\">")
        _e("Customize Your Site")
        php_print("</a>\n       ")
    # end if
    php_print("     <a class=\"button button-primary button-hero hide-if-customize\" href=\"")
    php_print(admin_url("themes.php"))
    php_print("\">")
    _e("Customize Your Site")
    php_print("</a>\n       ")
    if current_user_can("install_themes") or current_user_can("switch_themes") and php_count(wp_get_themes(Array({"allowed": True}))) > 1:
        php_print("         ")
        themes_link = add_query_arg("autofocus[panel]", "themes", admin_url("customize.php")) if current_user_can("customize") else admin_url("themes.php")
        php_print("         <p class=\"hide-if-no-customize\">\n                ")
        #// translators: %s: URL to Themes panel in Customizer or Themes screen.
        printf(__("or, <a href=\"%s\">change your theme completely</a>"), themes_link)
        php_print("         </p>\n      ")
    # end if
    php_print(" </div>\n    <div class=\"welcome-panel-column\">\n      <h3>")
    _e("Next Steps")
    php_print("</h3>\n      <ul>\n      ")
    if "page" == get_option("show_on_front") and (not get_option("page_for_posts")):
        php_print("         <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-edit-page\">" + __("Edit your front page") + "</a>", get_edit_post_link(get_option("page_on_front")))
        php_print("</li>\n          <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-add-page\">" + __("Add additional pages") + "</a>", admin_url("post-new.php?post_type=page"))
        php_print("</li>\n      ")
    elif "page" == get_option("show_on_front"):
        php_print("         <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-edit-page\">" + __("Edit your front page") + "</a>", get_edit_post_link(get_option("page_on_front")))
        php_print("</li>\n          <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-add-page\">" + __("Add additional pages") + "</a>", admin_url("post-new.php?post_type=page"))
        php_print("</li>\n          <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-write-blog\">" + __("Add a blog post") + "</a>", admin_url("post-new.php"))
        php_print("</li>\n      ")
    else:
        php_print("         <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-write-blog\">" + __("Write your first blog post") + "</a>", admin_url("post-new.php"))
        php_print("</li>\n          <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-add-page\">" + __("Add an About page") + "</a>", admin_url("post-new.php?post_type=page"))
        php_print("</li>\n          <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-setup-home\">" + __("Set up your homepage") + "</a>", add_query_arg("autofocus[section]", "static_front_page", admin_url("customize.php")) if current_user_can("customize") else admin_url("options-reading.php"))
        php_print("</li>\n      ")
    # end if
    php_print("         <li>")
    printf("<a href=\"%s\" class=\"welcome-icon welcome-view-site\">" + __("View your site") + "</a>", home_url("/"))
    php_print("""</li>
    </ul>
    </div>
    <div class=\"welcome-panel-column welcome-panel-last\">
    <h3>""")
    _e("More Actions")
    php_print("</h3>\n      <ul>\n      ")
    if current_theme_supports("widgets"):
        php_print("         <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-widgets\">" + __("Manage widgets") + "</a>", admin_url("widgets.php"))
        php_print("</li>\n      ")
    # end if
    php_print("     ")
    if current_theme_supports("menus"):
        php_print("         <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-menus\">" + __("Manage menus") + "</a>", admin_url("nav-menus.php"))
        php_print("</li>\n      ")
    # end if
    php_print("     ")
    if current_user_can("manage_options"):
        php_print("         <li>")
        printf("<a href=\"%s\" class=\"welcome-icon welcome-comments\">" + __("Turn comments on or off") + "</a>", admin_url("options-discussion.php"))
        php_print("</li>\n      ")
    # end if
    php_print("         <li>")
    printf("<a href=\"%s\" class=\"welcome-icon welcome-learn-more\">" + __("Learn more about getting started") + "</a>", __("https://wordpress.org/support/article/first-steps-with-wordpress-b/"))
    php_print("""</li>
    </ul>
    </div>
    </div>
    </div>
    """)
# end def wp_welcome_panel
