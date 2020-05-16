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
#// Post advanced form for inclusion in the administration panels.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Don't load directly.
if (not php_defined("ABSPATH")):
    php_print("-1")
    php_exit()
# end if
#// 
#// @global string       $post_type
#// @global WP_Post_Type $post_type_object
#// @global WP_Post      $post             Global post object.
#//
global post_type,post_type_object,post
php_check_if_defined("post_type","post_type_object","post")
#// Flag that we're not loading the block editor.
current_screen = get_current_screen()
current_screen.is_block_editor(False)
if is_multisite():
    add_action("admin_footer", "_admin_notice_post_locked")
else:
    check_users = get_users(Array({"fields": "ID", "number": 2}))
    if php_count(check_users) > 1:
        add_action("admin_footer", "_admin_notice_post_locked")
    # end if
    check_users = None
# end if
wp_enqueue_script("post")
_wp_editor_expand = False
_content_editor_dfw = False
#// 
#// Filters whether to enable the 'expand' functionality in the post editor.
#// 
#// @since 4.0.0
#// @since 4.1.0 Added the `$post_type` parameter.
#// 
#// @param bool   $expand    Whether to enable the 'expand' functionality. Default true.
#// @param string $post_type Post type.
#//
if post_type_supports(post_type, "editor") and (not wp_is_mobile()) and (not is_IE and php_preg_match("/MSIE [5678]/", PHP_SERVER["HTTP_USER_AGENT"])) and apply_filters("wp_editor_expand", True, post_type):
    wp_enqueue_script("editor-expand")
    _content_editor_dfw = True
    _wp_editor_expand = get_user_setting("editor_expand", "on") == "on"
# end if
if wp_is_mobile():
    wp_enqueue_script("jquery-touch-punch")
# end if
#// 
#// Post ID global
#// 
#// @name $post_ID
#// @var int
#//
post_ID = php_int(post_ID) if (php_isset(lambda : post_ID)) else 0
user_ID = php_int(user_ID) if (php_isset(lambda : user_ID)) else 0
action = action if (php_isset(lambda : action)) else ""
if get_option("page_for_posts") == post_ID and php_empty(lambda : post.post_content):
    add_action("edit_form_after_title", "_wp_posts_page_notice")
    remove_post_type_support(post_type, "editor")
# end if
thumbnail_support = current_theme_supports("post-thumbnails", post_type) and post_type_supports(post_type, "thumbnail")
if (not thumbnail_support) and "attachment" == post_type and post.post_mime_type:
    if wp_attachment_is("audio", post):
        thumbnail_support = post_type_supports("attachment:audio", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:audio")
    elif wp_attachment_is("video", post):
        thumbnail_support = post_type_supports("attachment:video", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:video")
    # end if
# end if
if thumbnail_support:
    add_thickbox()
    wp_enqueue_media(Array({"post": post_ID}))
# end if
#// Add the local autosave notice HTML.
add_action("admin_footer", "_local_storage_notice")
#// 
#// @todo Document the $messages array(s).
#//
permalink = get_permalink(post_ID)
if (not permalink):
    permalink = ""
# end if
messages = Array()
preview_post_link_html = ""
scheduled_post_link_html = ""
view_post_link_html = ""
preview_page_link_html = ""
scheduled_page_link_html = ""
view_page_link_html = ""
preview_url = get_preview_post_link(post)
viewable = is_post_type_viewable(post_type_object)
if viewable:
    #// Preview post link.
    preview_post_link_html = php_sprintf(" <a target=\"_blank\" href=\"%1$s\">%2$s</a>", esc_url(preview_url), __("Preview post"))
    #// Scheduled post preview link.
    scheduled_post_link_html = php_sprintf(" <a target=\"_blank\" href=\"%1$s\">%2$s</a>", esc_url(permalink), __("Preview post"))
    #// View post link.
    view_post_link_html = php_sprintf(" <a href=\"%1$s\">%2$s</a>", esc_url(permalink), __("View post"))
    #// Preview page link.
    preview_page_link_html = php_sprintf(" <a target=\"_blank\" href=\"%1$s\">%2$s</a>", esc_url(preview_url), __("Preview page"))
    #// Scheduled page preview link.
    scheduled_page_link_html = php_sprintf(" <a target=\"_blank\" href=\"%1$s\">%2$s</a>", esc_url(permalink), __("Preview page"))
    #// View page link.
    view_page_link_html = php_sprintf(" <a href=\"%1$s\">%2$s</a>", esc_url(permalink), __("View page"))
# end if
scheduled_date = php_sprintf(__("%1$s at %2$s"), date_i18n(_x("M j, Y", "publish box date format"), strtotime(post.post_date)), date_i18n(_x("H:i", "publish box time format"), strtotime(post.post_date)))
messages["post"] = Array({0: "", 1: __("Post updated.") + view_post_link_html, 2: __("Custom field updated."), 3: __("Custom field deleted."), 4: __("Post updated."), 5: php_sprintf(__("Post restored to revision from %s."), wp_post_revision_title(php_int(PHP_REQUEST["revision"]), False)) if (php_isset(lambda : PHP_REQUEST["revision"])) else False, 6: __("Post published.") + view_post_link_html, 7: __("Post saved."), 8: __("Post submitted.") + preview_post_link_html, 9: php_sprintf(__("Post scheduled for: %s."), "<strong>" + scheduled_date + "</strong>") + scheduled_post_link_html, 10: __("Post draft updated.") + preview_post_link_html})
messages["page"] = Array({0: "", 1: __("Page updated.") + view_page_link_html, 2: __("Custom field updated."), 3: __("Custom field deleted."), 4: __("Page updated."), 5: php_sprintf(__("Page restored to revision from %s."), wp_post_revision_title(php_int(PHP_REQUEST["revision"]), False)) if (php_isset(lambda : PHP_REQUEST["revision"])) else False, 6: __("Page published.") + view_page_link_html, 7: __("Page saved."), 8: __("Page submitted.") + preview_page_link_html, 9: php_sprintf(__("Page scheduled for: %s."), "<strong>" + scheduled_date + "</strong>") + scheduled_page_link_html, 10: __("Page draft updated.") + preview_page_link_html})
messages["attachment"] = array_fill(1, 10, __("Media file updated."))
#// Hack, for now.
#// 
#// Filters the post updated messages.
#// 
#// @since 3.0.0
#// 
#// @param array[] $messages Post updated messages. For defaults see `$messages` declarations above.
#//
messages = apply_filters("post_updated_messages", messages)
message = False
if (php_isset(lambda : PHP_REQUEST["message"])):
    PHP_REQUEST["message"] = absint(PHP_REQUEST["message"])
    if (php_isset(lambda : messages[post_type][PHP_REQUEST["message"]])):
        message = messages[post_type][PHP_REQUEST["message"]]
    elif (not (php_isset(lambda : messages[post_type]))) and (php_isset(lambda : messages["post"][PHP_REQUEST["message"]])):
        message = messages["post"][PHP_REQUEST["message"]]
    # end if
# end if
notice = False
form_extra = ""
if "auto-draft" == post.post_status:
    if "edit" == action:
        post.post_title = ""
    # end if
    autosave = False
    form_extra += "<input type='hidden' id='auto_draft' name='auto_draft' value='1' />"
else:
    autosave = wp_get_post_autosave(post_ID)
# end if
form_action = "editpost"
nonce_action = "update-post_" + post_ID
form_extra += "<input type='hidden' id='post_ID' name='post_ID' value='" + esc_attr(post_ID) + "' />"
#// Detect if there exists an autosave newer than the post and if that autosave is different than the post.
if autosave and mysql2date("U", autosave.post_modified_gmt, False) > mysql2date("U", post.post_modified_gmt, False):
    for autosave_field,_autosave_field in _wp_post_revision_fields(post):
        if normalize_whitespace(autosave.autosave_field) != normalize_whitespace(post.autosave_field):
            notice = php_sprintf(__("There is an autosave of this post that is more recent than the version below. <a href=\"%s\">View the autosave</a>"), get_edit_post_link(autosave.ID))
            break
        # end if
    # end for
    #// If this autosave isn't different from the current post, begone.
    if (not notice):
        wp_delete_post_revision(autosave.ID)
    # end if
    autosave_field = None
    _autosave_field = None
# end if
post_type_object = get_post_type_object(post_type)
#// All meta boxes should be defined and added before the first do_meta_boxes() call (or potentially during the do_meta_boxes action).
php_include_file(ABSPATH + "wp-admin/includes/meta-boxes.php", once=True)
register_and_do_post_meta_boxes(post)
add_screen_option("layout_columns", Array({"max": 2, "default": 2}))
if "post" == post_type:
    customize_display = "<p>" + __("The title field and the big Post Editing Area are fixed in place, but you can reposition all the other boxes using drag and drop. You can also minimize or expand them by clicking the title bar of each box. Use the Screen Options tab to unhide more boxes (Excerpt, Send Trackbacks, Custom Fields, Discussion, Slug, Author) or to choose a 1- or 2-column layout for this screen.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "customize-display", "title": __("Customizing This Display"), "content": customize_display}))
    title_and_editor = "<p>" + __("<strong>Title</strong> &mdash; Enter a title for your post. After you enter a title, you&#8217;ll see the permalink below, which you can edit.") + "</p>"
    title_and_editor += "<p>" + __("<strong>Post editor</strong> &mdash; Enter the text for your post. There are two modes of editing: Visual and Text. Choose the mode by clicking on the appropriate tab.") + "</p>"
    title_and_editor += "<p>" + __("Visual mode gives you an editor that is similar to a word processor. Click the Toolbar Toggle button to get a second row of controls.") + "</p>"
    title_and_editor += "<p>" + __("The Text mode allows you to enter HTML along with your post text. Note that &lt;p&gt; and &lt;br&gt; tags are converted to line breaks when switching to the Text editor to make it less cluttered. When you type, a single line break can be used instead of typing &lt;br&gt;, and two line breaks instead of paragraph tags. The line breaks are converted back to tags automatically.") + "</p>"
    title_and_editor += "<p>" + __("You can insert media files by clicking the button above the post editor and following the directions. You can align or edit images using the inline formatting toolbar available in Visual mode.") + "</p>"
    title_and_editor += "<p>" + __("You can enable distraction-free writing mode using the icon to the right. This feature is not available for old browsers or devices with small screens, and requires that the full-height editor be enabled in Screen Options.") + "</p>"
    title_and_editor += "<p>" + __("Keyboard users: When you&#8217;re working in the visual editor, you can use <kbd>Alt + F10</kbd> to access the toolbar.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "title-post-editor", "title": __("Title and Post Editor"), "content": title_and_editor}))
    get_current_screen().set_help_sidebar("<p>" + php_sprintf(__("You can also create posts with the <a href=\"%s\">Press This bookmarklet</a>."), "tools.php") + "</p>" + "<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/wordpress-editor/\">Documentation on Writing and Editing Posts</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
elif "page" == post_type:
    about_pages = "<p>" + __("Pages are similar to posts in that they have a title, body text, and associated metadata, but they are different in that they are not part of the chronological blog stream, kind of like permanent posts. Pages are not categorized or tagged, but can have a hierarchy. You can nest pages under other pages by making one the &#8220;Parent&#8221; of the other, creating a group of pages.") + "</p>" + "<p>" + __("Creating a Page is very similar to creating a Post, and the screens can be customized in the same way using drag and drop, the Screen Options tab, and expanding/collapsing boxes as you choose. This screen also has the distraction-free writing space, available in both the Visual and Text modes via the Fullscreen buttons. The Page editor mostly works the same as the Post editor, but there are some Page-specific features in the Page Attributes box.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "about-pages", "title": __("About Pages"), "content": about_pages}))
    get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/pages-add-new-screen/\">Documentation on Adding New Pages</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/pages-screen/\">Documentation on Editing Pages</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
elif "attachment" == post_type:
    get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen allows you to edit fields for metadata in a file within the media library.") + "</p>" + "<p>" + __("For images only, you can click on Edit Image under the thumbnail to expand out an inline image editor with icons for cropping, rotating, or flipping the image as well as for undoing and redoing. The boxes on the right give you more options for scaling the image, for cropping it, and for cropping the thumbnail in a different way than you crop the original image. You can click on Help in those boxes to get more information.") + "</p>" + "<p>" + __("Note that you crop the image by clicking on it (the Crop icon is already selected) and dragging the cropping frame to select the desired part. Then click Save to retain the cropping.") + "</p>" + "<p>" + __("Remember to click Update Media to save metadata entered or changed.") + "</p>"}))
    get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/edit-media/\">Documentation on Edit Media</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
# end if
if "post" == post_type or "page" == post_type:
    inserting_media = "<p>" + __("You can upload and insert media (images, audio, documents, etc.) by clicking the Add Media button. You can select from the images and files already uploaded to the Media Library, or upload new media to add to your page or post. To create an image gallery, select the images to add and click the &#8220;Create a new gallery&#8221; button.") + "</p>"
    inserting_media += "<p>" + __("You can also embed media from many popular websites including Twitter, YouTube, Flickr and others by pasting the media URL on its own line into the content of your post/page. <a href=\"https://wordpress.org/support/article/embeds/\">Learn more about embeds</a>.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "inserting-media", "title": __("Inserting Media"), "content": inserting_media}))
# end if
if "post" == post_type:
    publish_box = "<p>" + __("Several boxes on this screen contain settings for how your content will be published, including:") + "</p>"
    publish_box += "<ul><li>" + __("<strong>Publish</strong> &mdash; You can set the terms of publishing your post in the Publish box. For Status, Visibility, and Publish (immediately), click on the Edit link to reveal more options. Visibility includes options for password-protecting a post or making it stay at the top of your blog indefinitely (sticky). The Password protected option allows you to set an arbitrary password for each post. The Private option hides the post from everyone except editors and administrators. Publish (immediately) allows you to set a future or past date and time, so you can schedule a post to be published in the future or backdate a post.") + "</li>"
    if current_theme_supports("post-formats") and post_type_supports("post", "post-formats"):
        publish_box += "<li>" + __("<strong>Format</strong> &mdash; Post Formats designate how your theme will display a specific post. For example, you could have a <em>standard</em> blog post with a title and paragraphs, or a short <em>aside</em> that omits the title and contains a short text blurb. Your theme could enable all or some of 10 possible formats. <a href=\"https://wordpress.org/support/article/post-formats/#supported-formats\">Learn more about each post format</a>.") + "</li>"
    # end if
    if current_theme_supports("post-thumbnails") and post_type_supports("post", "thumbnail"):
        publish_box += "<li>" + php_sprintf(__("<strong>%s</strong> &mdash; This allows you to associate an image with your post without inserting it. This is usually useful only if your theme makes use of the image as a post thumbnail on the home page, a custom header, etc."), esc_html(post_type_object.labels.featured_image)) + "</li>"
    # end if
    publish_box += "</ul>"
    get_current_screen().add_help_tab(Array({"id": "publish-box", "title": __("Publish Settings"), "content": publish_box}))
    discussion_settings = "<p>" + __("<strong>Send Trackbacks</strong> &mdash; Trackbacks are a way to notify legacy blog systems that you&#8217;ve linked to them. Enter the URL(s) you want to send trackbacks. If you link to other WordPress sites they&#8217;ll be notified automatically using pingbacks, and this field is unnecessary.") + "</p>"
    discussion_settings += "<p>" + __("<strong>Discussion</strong> &mdash; You can turn comments and pings on or off, and if there are comments on the post, you can see them here and moderate them.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "discussion-settings", "title": __("Discussion Settings"), "content": discussion_settings}))
elif "page" == post_type:
    page_attributes = "<p>" + __("<strong>Parent</strong> &mdash; You can arrange your pages in hierarchies. For example, you could have an &#8220;About&#8221; page that has &#8220;Life Story&#8221; and &#8220;My Dog&#8221; pages under it. There are no limits to how many levels you can nest pages.") + "</p>" + "<p>" + __("<strong>Template</strong> &mdash; Some themes have custom templates you can use for certain pages that might have additional features or custom layouts. If so, you&#8217;ll see them in this dropdown menu.") + "</p>" + "<p>" + __("<strong>Order</strong> &mdash; Pages are usually ordered alphabetically, but you can choose your own order by entering a number (1 for first, etc.) in this field.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "page-attributes", "title": __("Page Attributes"), "content": page_attributes}))
# end if
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("""
<div class=\"wrap\">
<h1 class=\"wp-heading-inline\">
""")
php_print(esc_html(title))
php_print("</h1>\n\n")
if (php_isset(lambda : post_new_file)) and current_user_can(post_type_object.cap.create_posts):
    php_print(" <a href=\"" + esc_url(admin_url(post_new_file)) + "\" class=\"page-title-action\">" + esc_html(post_type_object.labels.add_new) + "</a>")
# end if
php_print("""
<hr class=\"wp-header-end\">
""")
if notice:
    php_print("<div id=\"notice\" class=\"notice notice-warning\"><p id=\"has-newer-autosave\">")
    php_print(notice)
    php_print("</p></div>\n")
# end if
if message:
    php_print("<div id=\"message\" class=\"updated notice notice-success is-dismissible\"><p>")
    php_print(message)
    php_print("</p></div>\n")
# end if
php_print("<div id=\"lost-connection-notice\" class=\"error hidden\">\n <p><span class=\"spinner\"></span> ")
_e("<strong>Connection lost.</strong> Saving has been disabled until you&#8217;re reconnected.")
php_print(" <span class=\"hide-if-no-sessionstorage\">")
_e("We&#8217;re backing up this post in your browser, just in case.")
php_print("""</span>
</p>
</div>
<form name=\"post\" action=\"post.php\" method=\"post\" id=\"post\"
""")
#// 
#// Fires inside the post editor form tag.
#// 
#// @since 3.0.0
#// 
#// @param WP_Post $post Post object.
#//
do_action("post_edit_form_tag", post)
referer = wp_get_referer()
php_print(">\n")
wp_nonce_field(nonce_action)
php_print("<input type=\"hidden\" id=\"user-id\" name=\"user_ID\" value=\"")
php_print(php_int(user_ID))
php_print("\" />\n<input type=\"hidden\" id=\"hiddenaction\" name=\"action\" value=\"")
php_print(esc_attr(form_action))
php_print("\" />\n<input type=\"hidden\" id=\"originalaction\" name=\"originalaction\" value=\"")
php_print(esc_attr(form_action))
php_print("\" />\n<input type=\"hidden\" id=\"post_author\" name=\"post_author\" value=\"")
php_print(esc_attr(post.post_author))
php_print("\" />\n<input type=\"hidden\" id=\"post_type\" name=\"post_type\" value=\"")
php_print(esc_attr(post_type))
php_print("\" />\n<input type=\"hidden\" id=\"original_post_status\" name=\"original_post_status\" value=\"")
php_print(esc_attr(post.post_status))
php_print("\" />\n<input type=\"hidden\" id=\"referredby\" name=\"referredby\" value=\"")
php_print(esc_url(referer) if referer else "")
php_print("\" />\n")
if (not php_empty(lambda : active_post_lock)):
    php_print("<input type=\"hidden\" id=\"active_post_lock\" value=\"")
    php_print(esc_attr(php_implode(":", active_post_lock)))
    php_print("\" />\n  ")
# end if
if "draft" != get_post_status(post):
    wp_original_referer_field(True, "previous")
# end if
php_print(form_extra)
wp_nonce_field("meta-box-order", "meta-box-order-nonce", False)
wp_nonce_field("closedpostboxes", "closedpostboxesnonce", False)
php_print("\n")
#// 
#// Fires at the beginning of the edit form.
#// 
#// At this point, the required hidden fields and nonces have already been output.
#// 
#// @since 3.7.0
#// 
#// @param WP_Post $post Post object.
#//
do_action("edit_form_top", post)
php_print("\n<div id=\"poststuff\">\n<div id=\"post-body\" class=\"metabox-holder columns-")
php_print("1" if 1 == get_current_screen().get_columns() else "2")
php_print("""\">
<div id=\"post-body-content\">
""")
if post_type_supports(post_type, "title"):
    php_print("<div id=\"titlediv\">\n<div id=\"titlewrap\">\n  ")
    #// 
    #// Filters the title field placeholder text.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string  $text Placeholder text. Default 'Add title'.
    #// @param WP_Post $post Post object.
    #//
    title_placeholder = apply_filters("enter_title_here", __("Add title"), post)
    php_print(" <label class=\"screen-reader-text\" id=\"title-prompt-text\" for=\"title\">")
    php_print(title_placeholder)
    php_print("</label>\n   <input type=\"text\" name=\"post_title\" size=\"30\" value=\"")
    php_print(esc_attr(post.post_title))
    php_print("\" id=\"title\" spellcheck=\"true\" autocomplete=\"off\" />\n</div>\n    ")
    #// 
    #// Fires before the permalink field in the edit form.
    #// 
    #// @since 4.1.0
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action("edit_form_before_permalink", post)
    php_print("<div class=\"inside\">\n ")
    if viewable:
        sample_permalink_html = get_sample_permalink_html(post.ID) if post_type_object.public else ""
        #// As of 4.4, the Get Shortlink button is hidden by default.
        if has_filter("pre_get_shortlink") or has_filter("get_shortlink"):
            shortlink = wp_get_shortlink(post.ID, "post")
            if (not php_empty(lambda : shortlink)) and shortlink != permalink and home_url("?page_id=" + post.ID) != permalink:
                sample_permalink_html += "<input id=\"shortlink\" type=\"hidden\" value=\"" + esc_attr(shortlink) + "\" /><button type=\"button\" class=\"button button-small\" onclick=\"prompt(&#39;URL:&#39;, jQuery('#shortlink').val());\">" + __("Get Shortlink") + "</button>"
            # end if
        # end if
        if post_type_object.public and (not "pending" == get_post_status(post) and (not current_user_can(post_type_object.cap.publish_posts))):
            has_sample_permalink = sample_permalink_html and "auto-draft" != post.post_status
            php_print(" <div id=\"edit-slug-box\" class=\"hide-if-no-js\">\n            ")
            if has_sample_permalink:
                php_print(sample_permalink_html)
            # end if
            php_print(" </div>\n            ")
        # end if
    # end if
    php_print("</div>\n ")
    wp_nonce_field("samplepermalink", "samplepermalinknonce", False)
    php_print("</div><!-- /titlediv -->\n   ")
# end if
#// 
#// Fires after the title field.
#// 
#// @since 3.5.0
#// 
#// @param WP_Post $post Post object.
#//
do_action("edit_form_after_title", post)
if post_type_supports(post_type, "editor"):
    _wp_editor_expand_class = ""
    if _wp_editor_expand:
        _wp_editor_expand_class = " wp-editor-expand"
    # end if
    php_print("<div id=\"postdivrich\" class=\"postarea")
    php_print(_wp_editor_expand_class)
    php_print("\">\n\n  ")
    wp_editor(post.post_content, "content", Array({"_content_editor_dfw": _content_editor_dfw, "drag_drop_upload": True, "tabfocus_elements": "content-html,save-post", "editor_height": 300, "tinymce": Array({"resize": False, "wp_autoresize_on": _wp_editor_expand, "add_unload_trigger": False, "wp_keep_scroll_position": (not is_IE)})}))
    php_print("<table id=\"post-status-info\"><tbody><tr>\n <td id=\"wp-word-count\" class=\"hide-if-no-js\">\n ")
    printf(__("Word count: %s"), "<span class=\"word-count\">0</span>")
    php_print("""   </td>
    <td class=\"autosave-info\">
    <span class=\"autosave-message\">&nbsp;</span>
    """)
    if "auto-draft" != post.post_status:
        php_print("<span id=\"last-edit\">")
        last_user = get_userdata(get_post_meta(post_ID, "_edit_last", True))
        if last_user:
            #// translators: 1: Name of most recent post author, 2: Post edited date, 3: Post edited time.
            printf(__("Last edited by %1$s on %2$s at %3$s"), esc_html(last_user.display_name), mysql2date(__("F j, Y"), post.post_modified), mysql2date(__("g:i a"), post.post_modified))
        else:
            #// translators: 1: Post edited date, 2: Post edited time.
            printf(__("Last edited on %1$s at %2$s"), mysql2date(__("F j, Y"), post.post_modified), mysql2date(__("g:i a"), post.post_modified))
        # end if
        php_print("</span>")
    # end if
    php_print("""   </td>
    <td id=\"content-resize-handle\" class=\"hide-if-no-js\"><br /></td>
    </tr></tbody></table>
    </div>
    """)
# end if
#// 
#// Fires after the content editor.
#// 
#// @since 3.5.0
#// 
#// @param WP_Post $post Post object.
#//
do_action("edit_form_after_editor", post)
php_print("""</div><!-- /post-body-content -->
<div id=\"postbox-container-1\" class=\"postbox-container\">
""")
if "page" == post_type:
    #// 
    #// Fires before meta boxes with 'side' context are output for the 'page' post type.
    #// 
    #// The submitpage box is a meta box with 'side' context, so this hook fires just before it is output.
    #// 
    #// @since 2.5.0
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action("submitpage_box", post)
else:
    #// 
    #// Fires before meta boxes with 'side' context are output for all post types other than 'page'.
    #// 
    #// The submitpost box is a meta box with 'side' context, so this hook fires just before it is output.
    #// 
    #// @since 2.5.0
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action("submitpost_box", post)
# end if
do_meta_boxes(post_type, "side", post)
php_print("</div>\n<div id=\"postbox-container-2\" class=\"postbox-container\">\n")
do_meta_boxes(None, "normal", post)
if "page" == post_type:
    #// 
    #// Fires after 'normal' context meta boxes have been output for the 'page' post type.
    #// 
    #// @since 1.5.0
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action("edit_page_form", post)
else:
    #// 
    #// Fires after 'normal' context meta boxes have been output for all post types other than 'page'.
    #// 
    #// @since 1.5.0
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action("edit_form_advanced", post)
# end if
do_meta_boxes(None, "advanced", post)
php_print("</div>\n")
#// 
#// Fires after all meta box sections have been output, before the closing #post-body div.
#// 
#// @since 2.1.0
#// 
#// @param WP_Post $post Post object.
#//
do_action("dbx_post_sidebar", post)
php_print("""</div><!-- /post-body -->
<br class=\"clear\" />
</div><!-- /poststuff -->
</form>
</div>
""")
if post_type_supports(post_type, "comments"):
    wp_comment_reply()
# end if
php_print("\n")
if (not wp_is_mobile()) and post_type_supports(post_type, "title") and "" == post.post_title:
    php_print("""<script type=\"text/javascript\">
try{document.post.title.focus();}catch(e){}
    </script>
    """)
# end if
