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
#// WordPress Administration Media API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Defines the default media upload tabs
#// 
#// @since 2.5.0
#// 
#// @return string[] Default tabs.
#//
def media_upload_tabs(*args_):
    
    _default_tabs = Array({"type": __("From Computer"), "type_url": __("From URL"), "gallery": __("Gallery"), "library": __("Media Library")})
    #// 
    #// Filters the available tabs in the legacy (pre-3.5.0) media popup.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string[] $_default_tabs An array of media tabs.
    #//
    return apply_filters("media_upload_tabs", _default_tabs)
# end def media_upload_tabs
#// 
#// Adds the gallery tab back to the tabs array if post has image attachments
#// 
#// @since 2.5.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $tabs
#// @return array $tabs with gallery if post has image attachment
#//
def update_gallery_tab(tabs=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not (php_isset(lambda : PHP_REQUEST["post_id"]))):
        tabs["gallery"] = None
        return tabs
    # end if
    post_id = php_intval(PHP_REQUEST["post_id"])
    if post_id:
        attachments = php_intval(wpdb.get_var(wpdb.prepare(str("SELECT count(*) FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'attachment' AND post_status != 'trash' AND post_parent = %d"), post_id)))
    # end if
    if php_empty(lambda : attachments):
        tabs["gallery"] = None
        return tabs
    # end if
    #// translators: %s: Number of attachments.
    tabs["gallery"] = php_sprintf(__("Gallery (%s)"), str("<span id='attachments-count'>") + str(attachments) + str("</span>"))
    return tabs
# end def update_gallery_tab
#// 
#// Outputs the legacy media upload tabs UI.
#// 
#// @since 2.5.0
#// 
#// @global string $redir_tab
#//
def the_media_upload_tabs(*args_):
    
    global redir_tab
    php_check_if_defined("redir_tab")
    tabs = media_upload_tabs()
    default = "type"
    if (not php_empty(lambda : tabs)):
        php_print("<ul id='sidemenu'>\n")
        if (php_isset(lambda : redir_tab)) and php_array_key_exists(redir_tab, tabs):
            current = redir_tab
        elif (php_isset(lambda : PHP_REQUEST["tab"])) and php_array_key_exists(PHP_REQUEST["tab"], tabs):
            current = PHP_REQUEST["tab"]
        else:
            #// This filter is documented in wp-admin/media-upload.php
            current = apply_filters("media_upload_default_tab", default)
        # end if
        for callback,text in tabs:
            class_ = ""
            if current == callback:
                class_ = " class='current'"
            # end if
            href = add_query_arg(Array({"tab": callback, "s": False, "paged": False, "post_mime_type": False, "m": False}))
            link = "<a href='" + esc_url(href) + str("'") + str(class_) + str(">") + str(text) + str("</a>")
            php_print(" <li id='" + esc_attr(str("tab-") + str(callback)) + str("'>") + str(link) + str("</li>\n"))
        # end for
        php_print("</ul>\n")
    # end if
# end def the_media_upload_tabs
#// 
#// Retrieves the image HTML to send to the editor.
#// 
#// @since 2.5.0
#// 
#// @param int          $id      Image attachment id.
#// @param string       $caption Image caption.
#// @param string       $title   Image title attribute.
#// @param string       $align   Image CSS alignment property.
#// @param string       $url     Optional. Image src URL. Default empty.
#// @param bool|string  $rel     Optional. Value for rel attribute or whether to add a default value. Default false.
#// @param string|array $size    Optional. Image size. Accepts any valid image size, or an array of width
#// and height values in pixels (in that order). Default 'medium'.
#// @param string       $alt     Optional. Image alt attribute. Default empty.
#// @return string The HTML output to insert into the editor.
#//
def get_image_send_to_editor(id=None, caption=None, title=None, align=None, url="", rel=False, size="medium", alt="", *args_):
    
    html = get_image_tag(id, alt, "", align, size)
    if rel:
        if php_is_string(rel):
            rel = " rel=\"" + esc_attr(rel) + "\""
        else:
            rel = " rel=\"attachment wp-att-" + php_intval(id) + "\""
        # end if
    else:
        rel = ""
    # end if
    if url:
        html = "<a href=\"" + esc_attr(url) + "\"" + rel + ">" + html + "</a>"
    # end if
    #// 
    #// Filters the image HTML markup to send to the editor when inserting an image.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string       $html    The image HTML markup to send.
    #// @param int          $id      The attachment id.
    #// @param string       $caption The image caption.
    #// @param string       $title   The image title.
    #// @param string       $align   The image alignment.
    #// @param string       $url     The image source URL.
    #// @param string|array $size    Size of image. Image size or array of width and height values
    #// (in that order). Default 'medium'.
    #// @param string       $alt     The image alternative, or alt, text.
    #//
    html = apply_filters("image_send_to_editor", html, id, caption, title, align, url, size, alt)
    return html
# end def get_image_send_to_editor
#// 
#// Adds image shortcode with caption to editor
#// 
#// @since 2.6.0
#// 
#// @param string  $html    The image HTML markup to send.
#// @param integer $id      Image attachment ID.
#// @param string  $caption Image caption.
#// @param string  $title   Image title attribute (not used).
#// @param string  $align   Image CSS alignment property.
#// @param string  $url     Image source URL (not used).
#// @param string  $size    Image size (`thumbnail`, `medium`, `large`, `full`, or added with `add_image_size()`) (not used).
#// @param string  $alt     Image `alt` attribute (not used).
#// @return string The image HTML markup with caption shortcode.
#//
def image_add_caption(html=None, id=None, caption=None, title=None, align=None, url=None, size=None, alt="", *args_):
    
    #// 
    #// Filters the caption text.
    #// 
    #// Note: If the caption text is empty, the caption shortcode will not be appended
    #// to the image HTML when inserted into the editor.
    #// 
    #// Passing an empty value also prevents the {@see 'image_add_caption_shortcode'}
    #// Filters from being evaluated at the end of image_add_caption().
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $caption The original caption text.
    #// @param int    $id      The attachment ID.
    #//
    caption = apply_filters("image_add_caption_text", caption, id)
    #// 
    #// Filters whether to disable captions.
    #// 
    #// Prevents image captions from being appended to image HTML when inserted into the editor.
    #// 
    #// @since 2.6.0
    #// 
    #// @param bool $bool Whether to disable appending captions. Returning true to the filter
    #// will disable captions. Default empty string.
    #//
    if php_empty(lambda : caption) or apply_filters("disable_captions", ""):
        return html
    # end if
    id = "attachment_" + id if 0 < php_int(id) else ""
    if (not php_preg_match("/width=[\"']([0-9]+)/", html, matches)):
        return html
    # end if
    width = matches[1]
    caption = php_str_replace(Array("\r\n", "\r"), "\n", caption)
    caption = preg_replace_callback("/<[a-zA-Z0-9]+(?: [^<>]+>)*/", "_cleanup_image_add_caption", caption)
    #// Convert any remaining line breaks to <br />.
    caption = php_preg_replace("/[ \\n\\t]*\\n[ \\t]*/", "<br />", caption)
    html = php_preg_replace("/(class=[\"'][^'\"]*)align(none|left|right|center)\\s?/", "$1", html)
    if php_empty(lambda : align):
        align = "none"
    # end if
    shcode = "[caption id=\"" + id + "\" align=\"align" + align + "\" width=\"" + width + "\"]" + html + " " + caption + "[/caption]"
    #// 
    #// Filters the image HTML markup including the caption shortcode.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $shcode The image HTML markup with caption shortcode.
    #// @param string $html   The image HTML markup.
    #//
    return apply_filters("image_add_caption_shortcode", shcode, html)
# end def image_add_caption
#// 
#// Private preg_replace callback used in image_add_caption()
#// 
#// @access private
#// @since 3.4.0
#//
def _cleanup_image_add_caption(matches=None, *args_):
    
    #// Remove any line breaks from inside the tags.
    return php_preg_replace("/[\\r\\n\\t]+/", " ", matches[0])
# end def _cleanup_image_add_caption
#// 
#// Adds image html to editor
#// 
#// @since 2.5.0
#// 
#// @param string $html
#//
def media_send_to_editor(html=None, *args_):
    
    php_print(" <script type=\"text/javascript\">\n var win = window.dialogArguments || opener || parent || top;\n  win.send_to_editor( ")
    php_print(wp_json_encode(html))
    php_print(" );\n    </script>\n ")
    php_exit(0)
# end def media_send_to_editor
#// 
#// Save a file submitted from a POST request and create an attachment post for it.
#// 
#// @since 2.5.0
#// 
#// @param string $file_id   Index of the `$_FILES` array that the file was sent. Required.
#// @param int    $post_id   The post ID of a post to attach the media item to. Required, but can
#// be set to 0, creating a media item that has no relationship to a post.
#// @param array  $post_data Overwrite some of the attachment. Optional.
#// @param array  $overrides Override the wp_handle_upload() behavior. Optional.
#// @return int|WP_Error ID of the attachment or a WP_Error object on failure.
#//
def media_handle_upload(file_id=None, post_id=None, post_data=Array(), overrides=Array({"test_form": False}), *args_):
    
    time = current_time("mysql")
    post = get_post(post_id)
    if post:
        #// The post date doesn't usually matter for pages, so don't backdate this upload.
        if "page" != post.post_type and php_substr(post.post_date, 0, 4) > 0:
            time = post.post_date
        # end if
    # end if
    file = wp_handle_upload(PHP_FILES[file_id], overrides, time)
    if (php_isset(lambda : file["error"])):
        return php_new_class("WP_Error", lambda : WP_Error("upload_error", file["error"]))
    # end if
    name = PHP_FILES[file_id]["name"]
    ext = pathinfo(name, PATHINFO_EXTENSION)
    name = wp_basename(name, str(".") + str(ext))
    url = file["url"]
    type = file["type"]
    file = file["file"]
    title = sanitize_text_field(name)
    content = ""
    excerpt = ""
    if php_preg_match("#^audio#", type):
        meta = wp_read_audio_metadata(file)
        if (not php_empty(lambda : meta["title"])):
            title = meta["title"]
        # end if
        if (not php_empty(lambda : title)):
            if (not php_empty(lambda : meta["album"])) and (not php_empty(lambda : meta["artist"])):
                #// translators: 1: Audio track title, 2: Album title, 3: Artist name.
                content += php_sprintf(__("\"%1$s\" from %2$s by %3$s."), title, meta["album"], meta["artist"])
            elif (not php_empty(lambda : meta["album"])):
                #// translators: 1: Audio track title, 2: Album title.
                content += php_sprintf(__("\"%1$s\" from %2$s."), title, meta["album"])
            elif (not php_empty(lambda : meta["artist"])):
                #// translators: 1: Audio track title, 2: Artist name.
                content += php_sprintf(__("\"%1$s\" by %2$s."), title, meta["artist"])
            else:
                #// translators: %s: Audio track title.
                content += php_sprintf(__("\"%s\"."), title)
            # end if
        elif (not php_empty(lambda : meta["album"])):
            if (not php_empty(lambda : meta["artist"])):
                #// translators: 1: Audio album title, 2: Artist name.
                content += php_sprintf(__("%1$s by %2$s."), meta["album"], meta["artist"])
            else:
                content += meta["album"] + "."
            # end if
        elif (not php_empty(lambda : meta["artist"])):
            content += meta["artist"] + "."
        # end if
        if (not php_empty(lambda : meta["year"])):
            #// translators: Audio file track information. %d: Year of audio track release.
            content += " " + php_sprintf(__("Released: %d."), meta["year"])
        # end if
        if (not php_empty(lambda : meta["track_number"])):
            track_number = php_explode("/", meta["track_number"])
            if (php_isset(lambda : track_number[1])):
                #// translators: Audio file track information. 1: Audio track number, 2: Total audio tracks.
                content += " " + php_sprintf(__("Track %1$s of %2$s."), number_format_i18n(track_number[0]), number_format_i18n(track_number[1]))
            else:
                #// translators: Audio file track information. %s: Audio track number.
                content += " " + php_sprintf(__("Track %s."), number_format_i18n(track_number[0]))
            # end if
        # end if
        if (not php_empty(lambda : meta["genre"])):
            #// translators: Audio file genre information. %s: Audio genre name.
            content += " " + php_sprintf(__("Genre: %s."), meta["genre"])
        # end if
        pass
    elif 0 == php_strpos(type, "image/"):
        image_meta = wp_read_image_metadata(file)
        if image_meta:
            if php_trim(image_meta["title"]) and (not php_is_numeric(sanitize_title(image_meta["title"]))):
                title = image_meta["title"]
            # end if
            if php_trim(image_meta["caption"]):
                excerpt = image_meta["caption"]
            # end if
        # end if
    # end if
    #// Construct the attachment array.
    attachment = php_array_merge(Array({"post_mime_type": type, "guid": url, "post_parent": post_id, "post_title": title, "post_content": content, "post_excerpt": excerpt}), post_data)
    attachment["ID"] = None
    #// Save the data.
    attachment_id = wp_insert_attachment(attachment, file, post_id, True)
    if (not is_wp_error(attachment_id)):
        #// Set a custom header with the attachment_id.
        #// Used by the browser/client to resume creating image sub-sizes after a PHP fatal error.
        if (not php_headers_sent()):
            php_header("X-WP-Upload-Attachment-ID: " + attachment_id)
        # end if
        #// The image sub-sizes are created during wp_generate_attachment_metadata().
        #// This is generally slow and may cause timeouts or out of memory errors.
        wp_update_attachment_metadata(attachment_id, wp_generate_attachment_metadata(attachment_id, file))
    # end if
    return attachment_id
# end def media_handle_upload
#// 
#// Handles a side-loaded file in the same way as an uploaded file is handled by media_handle_upload().
#// 
#// @since 2.6.0
#// @since 5.3.0 The `$post_id` parameter was made optional.
#// 
#// @param array  $file_array Array similar to a `$_FILES` upload array.
#// @param int    $post_id    Optional. The post ID the media is associated with.
#// @param string $desc       Optional. Description of the side-loaded file. Default null.
#// @param array  $post_data  Optional. Post data to override. Default empty array.
#// @return int|WP_Error The ID of the attachment or a WP_Error on failure.
#//
def media_handle_sideload(file_array=None, post_id=0, desc=None, post_data=Array(), *args_):
    
    overrides = Array({"test_form": False})
    time = current_time("mysql")
    post = get_post(post_id)
    if post:
        if php_substr(post.post_date, 0, 4) > 0:
            time = post.post_date
        # end if
    # end if
    file = wp_handle_sideload(file_array, overrides, time)
    if (php_isset(lambda : file["error"])):
        return php_new_class("WP_Error", lambda : WP_Error("upload_error", file["error"]))
    # end if
    url = file["url"]
    type = file["type"]
    file = file["file"]
    title = php_preg_replace("/\\.[^.]+$/", "", wp_basename(file))
    content = ""
    #// Use image exif/iptc data for title and caption defaults if possible.
    image_meta = wp_read_image_metadata(file)
    if image_meta:
        if php_trim(image_meta["title"]) and (not php_is_numeric(sanitize_title(image_meta["title"]))):
            title = image_meta["title"]
        # end if
        if php_trim(image_meta["caption"]):
            content = image_meta["caption"]
        # end if
    # end if
    if (php_isset(lambda : desc)):
        title = desc
    # end if
    #// Construct the attachment array.
    attachment = php_array_merge(Array({"post_mime_type": type, "guid": url, "post_parent": post_id, "post_title": title, "post_content": content}), post_data)
    attachment["ID"] = None
    #// Save the attachment metadata.
    attachment_id = wp_insert_attachment(attachment, file, post_id, True)
    if (not is_wp_error(attachment_id)):
        wp_update_attachment_metadata(attachment_id, wp_generate_attachment_metadata(attachment_id, file))
    # end if
    return attachment_id
# end def media_handle_sideload
#// 
#// Outputs the iframe to display the media upload page.
#// 
#// @since 2.5.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @global int $body_id
#// 
#// @param callable $content_func Function that outputs the content.
#// @param mixed    ...$args      Optional additional parameters to pass to the callback function when it's called.
#//
def wp_iframe(content_func=None, *args):
    
    _wp_admin_html_begin()
    php_print(" <title>")
    bloginfo("name")
    php_print(" &rsaquo; ")
    _e("Uploads")
    php_print(" &#8212; ")
    _e("WordPress")
    php_print("</title>\n   ")
    wp_enqueue_style("colors")
    #// Check callback name for 'media'.
    if php_is_array(content_func) and (not php_empty(lambda : content_func[1])) and 0 == php_strpos(php_str(content_func[1]), "media") or (not php_is_array(content_func)) and 0 == php_strpos(content_func, "media"):
        wp_enqueue_style("deprecated-media")
    # end if
    wp_enqueue_style("ie")
    php_print(" <script type=\"text/javascript\">\n addLoadEvent = function(func){if(typeof jQuery!=\"undefined\")jQuery(document).ready(func);else if(typeof wpOnload!='function'){wpOnload=func;}else{var oldonload=wpOnload;wpOnload=function(){oldonload();func();}}};\n    var ajaxurl = '")
    php_print(admin_url("admin-ajax.php", "relative"))
    php_print("', pagenow = 'media-upload-popup', adminpage = 'media-upload-popup',\n   isRtl = ")
    php_print(php_int(is_rtl()))
    php_print(";\n  </script>\n ")
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_enqueue_scripts", "media-upload-popup")
    #// 
    #// Fires when admin styles enqueued for the legacy (pre-3.5.0) media upload popup are printed.
    #// 
    #// @since 2.9.0
    #//
    do_action("admin_print_styles-media-upload-popup")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_print_styles")
    #// 
    #// Fires when admin scripts enqueued for the legacy (pre-3.5.0) media upload popup are printed.
    #// 
    #// @since 2.9.0
    #//
    do_action("admin_print_scripts-media-upload-popup")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_print_scripts")
    #// 
    #// Fires when scripts enqueued for the admin header for the legacy (pre-3.5.0)
    #// media upload popup are printed.
    #// 
    #// @since 2.9.0
    #//
    do_action("admin_head-media-upload-popup")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    #// This action is documented in wp-admin/admin-header.php
    do_action("admin_head")
    if php_is_string(content_func):
        #// 
        #// Fires in the admin header for each specific form tab in the legacy
        #// (pre-3.5.0) media upload popup.
        #// 
        #// The dynamic portion of the hook, `$content_func`, refers to the form
        #// callback for the media upload type. Possible values include
        #// 'media_upload_type_form', 'media_upload_type_url_form', and
        #// 'media_upload_library_form'.
        #// 
        #// @since 2.5.0
        #//
        do_action(str("admin_head_") + str(content_func))
    # end if
    body_id_attr = ""
    if (php_isset(lambda : PHP_GLOBALS["body_id"])):
        body_id_attr = " id=\"" + PHP_GLOBALS["body_id"] + "\""
    # end if
    php_print(" </head>\n   <body")
    php_print(body_id_attr)
    php_print(""" class=\"wp-core-ui no-js\">
    <script type=\"text/javascript\">
    document.body.className = document.body.className.replace('no-js', 'js');
    </script>
    """)
    call_user_func_array(content_func, args)
    #// This action is documented in wp-admin/admin-footer.php
    do_action("admin_print_footer_scripts")
    php_print("""   <script type=\"text/javascript\">if(typeof wpOnload=='function')wpOnload();</script>
    </body>
    </html>
    """)
# end def wp_iframe
#// 
#// Adds the media button to the editor
#// 
#// @since 2.5.0
#// 
#// @global int $post_ID
#// 
#// @staticvar int $instance
#// 
#// @param string $editor_id
#//
def media_buttons(editor_id="content", *args_):
    
    media_buttons.instance = 0
    media_buttons.instance += 1
    post = get_post()
    if (not post) and (not php_empty(lambda : PHP_GLOBALS["post_ID"])):
        post = PHP_GLOBALS["post_ID"]
    # end if
    wp_enqueue_media(Array({"post": post}))
    img = "<span class=\"wp-media-buttons-icon\"></span> "
    id_attribute = " id=\"insert-media-button\"" if 1 == media_buttons.instance else ""
    printf("<button type=\"button\"%s class=\"button insert-media add_media\" data-editor=\"%s\">%s</button>", id_attribute, esc_attr(editor_id), img + __("Add Media"))
    #// 
    #// Filters the legacy (pre-3.5.0) media buttons.
    #// 
    #// Use {@see 'media_buttons'} action instead.
    #// 
    #// @since 2.5.0
    #// @deprecated 3.5.0 Use {@see 'media_buttons'} action instead.
    #// 
    #// @param string $string Media buttons context. Default empty.
    #//
    legacy_filter = apply_filters_deprecated("media_buttons_context", Array(""), "3.5.0", "media_buttons")
    if legacy_filter:
        #// #WP22559. Close <a> if a plugin started by closing <a> to open their own <a> tag.
        if 0 == php_stripos(php_trim(legacy_filter), "</a>"):
            legacy_filter += "</a>"
        # end if
        php_print(legacy_filter)
    # end if
# end def media_buttons
#// 
#// @global int $post_ID
#// @param string $type
#// @param int $post_id
#// @param string $tab
#// @return string
#//
def get_upload_iframe_src(type=None, post_id=None, tab=None, *args_):
    
    global post_ID
    php_check_if_defined("post_ID")
    if php_empty(lambda : post_id):
        post_id = post_ID
    # end if
    upload_iframe_src = add_query_arg("post_id", php_int(post_id), admin_url("media-upload.php"))
    if type and "media" != type:
        upload_iframe_src = add_query_arg("type", type, upload_iframe_src)
    # end if
    if (not php_empty(lambda : tab)):
        upload_iframe_src = add_query_arg("tab", tab, upload_iframe_src)
    # end if
    #// 
    #// Filters the upload iframe source URL for a specific media type.
    #// 
    #// The dynamic portion of the hook name, `$type`, refers to the type
    #// of media uploaded.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $upload_iframe_src The upload iframe source URL by type.
    #//
    upload_iframe_src = apply_filters(str(type) + str("_upload_iframe_src"), upload_iframe_src)
    return add_query_arg("TB_iframe", True, upload_iframe_src)
# end def get_upload_iframe_src
#// 
#// Handles form submissions for the legacy media uploader.
#// 
#// @since 2.5.0
#// 
#// @return mixed void|object WP_Error on failure
#//
def media_upload_form_handler(*args_):
    
    check_admin_referer("media-form")
    errors = None
    if (php_isset(lambda : PHP_POST["send"])):
        keys = php_array_keys(PHP_POST["send"])
        send_id = php_int(reset(keys))
    # end if
    if (not php_empty(lambda : PHP_POST["attachments"])):
        for attachment_id,attachment in PHP_POST["attachments"]:
            post = get_post(attachment_id, ARRAY_A)
            _post = post
            if (not current_user_can("edit_post", attachment_id)):
                continue
            # end if
            if (php_isset(lambda : attachment["post_content"])):
                post["post_content"] = attachment["post_content"]
            # end if
            if (php_isset(lambda : attachment["post_title"])):
                post["post_title"] = attachment["post_title"]
            # end if
            if (php_isset(lambda : attachment["post_excerpt"])):
                post["post_excerpt"] = attachment["post_excerpt"]
            # end if
            if (php_isset(lambda : attachment["menu_order"])):
                post["menu_order"] = attachment["menu_order"]
            # end if
            if (php_isset(lambda : send_id)) and attachment_id == send_id:
                if (php_isset(lambda : attachment["post_parent"])):
                    post["post_parent"] = attachment["post_parent"]
                # end if
            # end if
            #// 
            #// Filters the attachment fields to be saved.
            #// 
            #// @since 2.5.0
            #// 
            #// @see wp_get_attachment_metadata()
            #// 
            #// @param array $post       An array of post data.
            #// @param array $attachment An array of attachment metadata.
            #//
            post = apply_filters("attachment_fields_to_save", post, attachment)
            if (php_isset(lambda : attachment["image_alt"])):
                image_alt = wp_unslash(attachment["image_alt"])
                if get_post_meta(attachment_id, "_wp_attachment_image_alt", True) != image_alt:
                    image_alt = wp_strip_all_tags(image_alt, True)
                    #// update_post_meta() expects slashed.
                    update_post_meta(attachment_id, "_wp_attachment_image_alt", wp_slash(image_alt))
                # end if
            # end if
            if (php_isset(lambda : post["errors"])):
                errors[attachment_id] = post["errors"]
                post["errors"] = None
            # end if
            if post != _post:
                wp_update_post(post)
            # end if
            for t in get_attachment_taxonomies(post):
                if (php_isset(lambda : attachment[t])):
                    wp_set_object_terms(attachment_id, php_array_map("trim", php_preg_split("/,+/", attachment[t])), t, False)
                # end if
            # end for
        # end for
    # end if
    if (php_isset(lambda : PHP_POST["insert-gallery"])) or (php_isset(lambda : PHP_POST["update-gallery"])):
        php_print("""       <script type=\"text/javascript\">
        var win = window.dialogArguments || opener || parent || top;
        win.tb_remove();
        </script>
        """)
        php_exit(0)
    # end if
    if (php_isset(lambda : send_id)):
        attachment = wp_unslash(PHP_POST["attachments"][send_id])
        html = attachment["post_title"] if (php_isset(lambda : attachment["post_title"])) else ""
        if (not php_empty(lambda : attachment["url"])):
            rel = ""
            if php_strpos(attachment["url"], "attachment_id") or get_attachment_link(send_id) == attachment["url"]:
                rel = " rel='attachment wp-att-" + esc_attr(send_id) + "'"
            # end if
            html = str("<a href='") + str(attachment["url"]) + str("'") + str(rel) + str(">") + str(html) + str("</a>")
        # end if
        #// 
        #// Filters the HTML markup for a media item sent to the editor.
        #// 
        #// @since 2.5.0
        #// 
        #// @see wp_get_attachment_metadata()
        #// 
        #// @param string $html       HTML markup for a media item sent to the editor.
        #// @param int    $send_id    The first key from the $_POST['send'] data.
        #// @param array  $attachment Array of attachment metadata.
        #//
        html = apply_filters("media_send_to_editor", html, send_id, attachment)
        return media_send_to_editor(html)
    # end if
    return errors
# end def media_upload_form_handler
#// 
#// Handles the process of uploading media.
#// 
#// @since 2.5.0
#// 
#// @return null|string
#//
def wp_media_upload_handler(*args_):
    
    errors = Array()
    id = 0
    if (php_isset(lambda : PHP_POST["html-upload"])) and (not php_empty(lambda : PHP_FILES)):
        check_admin_referer("media-form")
        #// Upload File button was clicked.
        id = media_handle_upload("async-upload", PHP_REQUEST["post_id"])
        PHP_FILES = None
        if is_wp_error(id):
            errors["upload_error"] = id
            id = False
        # end if
    # end if
    if (not php_empty(lambda : PHP_POST["insertonlybutton"])):
        src = PHP_POST["src"]
        if (not php_empty(lambda : src)) and (not php_strpos(src, "://")):
            src = str("http://") + str(src)
        # end if
        if (php_isset(lambda : PHP_POST["media_type"])) and "image" != PHP_POST["media_type"]:
            title = esc_html(wp_unslash(PHP_POST["title"]))
            if php_empty(lambda : title):
                title = esc_html(wp_basename(src))
            # end if
            if title and src:
                html = "<a href='" + esc_url(src) + str("'>") + str(title) + str("</a>")
            # end if
            type = "file"
            ext = php_preg_replace("/^.+?\\.([^.]+)$/", "$1", src)
            if ext:
                ext_type = wp_ext2type(ext)
                if "audio" == ext_type or "video" == ext_type:
                    type = ext_type
                # end if
            # end if
            #// 
            #// Filters the URL sent to the editor for a specific media type.
            #// 
            #// The dynamic portion of the hook name, `$type`, refers to the type
            #// of media being sent.
            #// 
            #// @since 3.3.0
            #// 
            #// @param string $html  HTML markup sent to the editor.
            #// @param string $src   Media source URL.
            #// @param string $title Media title.
            #//
            html = apply_filters(str(type) + str("_send_to_editor_url"), html, esc_url_raw(src), title)
        else:
            align = ""
            alt = esc_attr(wp_unslash(PHP_POST["alt"]))
            if (php_isset(lambda : PHP_POST["align"])):
                align = esc_attr(wp_unslash(PHP_POST["align"]))
                class_ = str(" class='align") + str(align) + str("'")
            # end if
            if (not php_empty(lambda : src)):
                html = "<img src='" + esc_url(src) + str("' alt='") + str(alt) + str("'") + str(class_) + str(" />")
            # end if
            #// 
            #// Filters the image URL sent to the editor.
            #// 
            #// @since 2.8.0
            #// 
            #// @param string $html  HTML markup sent to the editor for an image.
            #// @param string $src   Image source URL.
            #// @param string $alt   Image alternate, or alt, text.
            #// @param string $align The image alignment. Default 'alignnone'. Possible values include
            #// 'alignleft', 'aligncenter', 'alignright', 'alignnone'.
            #//
            html = apply_filters("image_send_to_editor_url", html, esc_url_raw(src), alt, align)
        # end if
        return media_send_to_editor(html)
    # end if
    if (php_isset(lambda : PHP_POST["save"])):
        errors["upload_notice"] = __("Saved.")
        wp_enqueue_script("admin-gallery")
        return wp_iframe("media_upload_gallery_form", errors)
    elif (not php_empty(lambda : PHP_POST)):
        return_ = media_upload_form_handler()
        if php_is_string(return_):
            return return_
        # end if
        if php_is_array(return_):
            errors = return_
        # end if
    # end if
    if (php_isset(lambda : PHP_REQUEST["tab"])) and "type_url" == PHP_REQUEST["tab"]:
        type = "image"
        if (php_isset(lambda : PHP_REQUEST["type"])) and php_in_array(PHP_REQUEST["type"], Array("video", "audio", "file")):
            type = PHP_REQUEST["type"]
        # end if
        return wp_iframe("media_upload_type_url_form", type, errors, id)
    # end if
    return wp_iframe("media_upload_type_form", "image", errors, id)
# end def wp_media_upload_handler
#// 
#// Downloads an image from the specified URL and attaches it to a post.
#// 
#// @since 2.6.0
#// @since 4.2.0 Introduced the `$return` parameter.
#// @since 4.8.0 Introduced the 'id' option within the `$return` parameter.
#// @since 5.3.0 The `$post_id` parameter was made optional.
#// @since 5.4.0 The original URL of the attachment is stored in the `_source_url`
#// post meta value.
#// 
#// @param string $file    The URL of the image to download.
#// @param int    $post_id Optional. The post ID the media is to be associated with.
#// @param string $desc    Optional. Description of the image.
#// @param string $return  Optional. Accepts 'html' (image tag html) or 'src' (URL),
#// or 'id' (attachment ID). Default 'html'.
#// @return string|WP_Error Populated HTML img tag on success, WP_Error object otherwise.
#//
def media_sideload_image(file=None, post_id=0, desc=None, return_="html", *args_):
    
    if (not php_empty(lambda : file)):
        #// Set variables for storage, fix file filename for query strings.
        php_preg_match("/[^\\?]+\\.(jpe?g|jpe|gif|png)\\b/i", file, matches)
        if (not matches):
            return php_new_class("WP_Error", lambda : WP_Error("image_sideload_failed", __("Invalid image URL.")))
        # end if
        file_array = Array()
        file_array["name"] = wp_basename(matches[0])
        #// Download file to temp location.
        file_array["tmp_name"] = download_url(file)
        #// If error storing temporarily, return the error.
        if is_wp_error(file_array["tmp_name"]):
            return file_array["tmp_name"]
        # end if
        #// Do the validation and storage stuff.
        id = media_handle_sideload(file_array, post_id, desc)
        #// If error storing permanently, unlink.
        if is_wp_error(id):
            php_no_error(lambda: unlink(file_array["tmp_name"]))
            return id
        # end if
        #// Store the original attachment source in meta.
        add_post_meta(id, "_source_url", file)
        #// If attachment id was requested, return it.
        if "id" == return_:
            return id
        # end if
        src = wp_get_attachment_url(id)
    # end if
    #// Finally, check to make sure the file has been saved, then return the HTML.
    if (not php_empty(lambda : src)):
        if "src" == return_:
            return src
        # end if
        alt = esc_attr(desc) if (php_isset(lambda : desc)) else ""
        html = str("<img src='") + str(src) + str("' alt='") + str(alt) + str("' />")
        return html
    else:
        return php_new_class("WP_Error", lambda : WP_Error("image_sideload_failed"))
    # end if
# end def media_sideload_image
#// 
#// Retrieves the legacy media uploader form in an iframe.
#// 
#// @since 2.5.0
#// 
#// @return string|null
#//
def media_upload_gallery(*args_):
    
    errors = Array()
    if (not php_empty(lambda : PHP_POST)):
        return_ = media_upload_form_handler()
        if php_is_string(return_):
            return return_
        # end if
        if php_is_array(return_):
            errors = return_
        # end if
    # end if
    wp_enqueue_script("admin-gallery")
    return wp_iframe("media_upload_gallery_form", errors)
# end def media_upload_gallery
#// 
#// Retrieves the legacy media library form in an iframe.
#// 
#// @since 2.5.0
#// 
#// @return string|null
#//
def media_upload_library(*args_):
    
    errors = Array()
    if (not php_empty(lambda : PHP_POST)):
        return_ = media_upload_form_handler()
        if php_is_string(return_):
            return return_
        # end if
        if php_is_array(return_):
            errors = return_
        # end if
    # end if
    return wp_iframe("media_upload_library_form", errors)
# end def media_upload_library
#// 
#// Retrieve HTML for the image alignment radio buttons with the specified one checked.
#// 
#// @since 2.7.0
#// 
#// @param WP_Post $post
#// @param string $checked
#// @return string
#//
def image_align_input_fields(post=None, checked="", *args_):
    
    if php_empty(lambda : checked):
        checked = get_user_setting("align", "none")
    # end if
    alignments = Array({"none": __("None"), "left": __("Left"), "center": __("Center"), "right": __("Right")})
    if (not php_array_key_exists(php_str(checked), alignments)):
        checked = "none"
    # end if
    out = Array()
    for name,label in alignments:
        name = esc_attr(name)
        out[-1] = str("<input type='radio' name='attachments[") + str(post.ID) + str("][align]' id='image-align-") + str(name) + str("-") + str(post.ID) + str("' value='") + str(name) + str("'") + " checked='checked'" if checked == name else "" + str(" /><label for='image-align-") + str(name) + str("-") + str(post.ID) + str("' class='align image-align-") + str(name) + str("-label'>") + str(label) + str("</label>")
    # end for
    return join("\n", out)
# end def image_align_input_fields
#// 
#// Retrieve HTML for the size radio buttons with the specified one checked.
#// 
#// @since 2.7.0
#// 
#// @param WP_Post $post
#// @param bool|string $check
#// @return array
#//
def image_size_input_fields(post=None, check="", *args_):
    
    #// 
    #// Filters the names and labels of the default image sizes.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[] $size_names Array of image size labels keyed by their name. Default values
    #// include 'Thumbnail', 'Medium', 'Large', and 'Full Size'.
    #//
    size_names = apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")}))
    if php_empty(lambda : check):
        check = get_user_setting("imgsize", "medium")
    # end if
    out = Array()
    for size,label in size_names:
        downsize = image_downsize(post.ID, size)
        checked = ""
        #// Is this size selectable?
        enabled = downsize[3] or "full" == size
        css_id = str("image-size-") + str(size) + str("-") + str(post.ID)
        #// If this size is the default but that's not available, don't select it.
        if size == check:
            if enabled:
                checked = " checked='checked'"
            else:
                check = ""
            # end if
        elif (not check) and enabled and "thumbnail" != size:
            #// 
            #// If $check is not enabled, default to the first available size
            #// that's bigger than a thumbnail.
            #//
            check = size
            checked = " checked='checked'"
        # end if
        html = "<div class='image-size-item'><input type='radio' " + disabled(enabled, False, False) + str("name='attachments[") + str(post.ID) + str("][image-size]' id='") + str(css_id) + str("' value='") + str(size) + str("'") + str(checked) + str(" />")
        html += str("<label for='") + str(css_id) + str("'>") + str(label) + str("</label>")
        #// Only show the dimensions if that choice is available.
        if enabled:
            html += str(" <label for='") + str(css_id) + str("' class='help'>") + php_sprintf("(%d&nbsp;&times;&nbsp;%d)", downsize[1], downsize[2]) + "</label>"
        # end if
        html += "</div>"
        out[-1] = html
    # end for
    return Array({"label": __("Size"), "input": "html", "html": join("\n", out)})
# end def image_size_input_fields
#// 
#// Retrieve HTML for the Link URL buttons with the default link type as specified.
#// 
#// @since 2.7.0
#// 
#// @param WP_Post $post
#// @param string $url_type
#// @return string
#//
def image_link_input_fields(post=None, url_type="", *args_):
    
    file = wp_get_attachment_url(post.ID)
    link = get_attachment_link(post.ID)
    if php_empty(lambda : url_type):
        url_type = get_user_setting("urlbutton", "post")
    # end if
    url = ""
    if "file" == url_type:
        url = file
    elif "post" == url_type:
        url = link
    # end if
    return str("\n  <input type='text' class='text urlfield' name='attachments[") + str(post.ID) + str("][url]' value='") + esc_attr(url) + "' /><br />\n   <button type='button' class='button urlnone' data-link-url=''>" + __("None") + "</button>\n <button type='button' class='button urlfile' data-link-url='" + esc_attr(file) + "'>" + __("File URL") + "</button>\n   <button type='button' class='button urlpost' data-link-url='" + esc_attr(link) + "'>" + __("Attachment Post URL") + "</button>\n"
# end def image_link_input_fields
#// 
#// Output a textarea element for inputting an attachment caption.
#// 
#// @since 3.4.0
#// 
#// @param WP_Post $edit_post Attachment WP_Post object.
#// @return string HTML markup for the textarea element.
#//
def wp_caption_input_textarea(edit_post=None, *args_):
    
    #// Post data is already escaped.
    name = str("attachments[") + str(edit_post.ID) + str("][post_excerpt]")
    return "<textarea name=\"" + name + "\" id=\"" + name + "\">" + edit_post.post_excerpt + "</textarea>"
# end def wp_caption_input_textarea
#// 
#// Retrieves the image attachment fields to edit form fields.
#// 
#// @since 2.5.0
#// 
#// @param array $form_fields
#// @param object $post
#// @return array
#//
def image_attachment_fields_to_edit(form_fields=None, post=None, *args_):
    
    return form_fields
# end def image_attachment_fields_to_edit
#// 
#// Retrieves the single non-image attachment fields to edit form fields.
#// 
#// @since 2.5.0
#// 
#// @param array   $form_fields An array of attachment form fields.
#// @param WP_Post $post        The WP_Post attachment object.
#// @return array Filtered attachment form fields.
#//
def media_single_attachment_fields_to_edit(form_fields=None, post=None, *args_):
    
    form_fields["url"] = None
    form_fields["align"] = None
    form_fields["image-size"] = None
    return form_fields
# end def media_single_attachment_fields_to_edit
#// 
#// Retrieves the post non-image attachment fields to edit form fields.
#// 
#// @since 2.8.0
#// 
#// @param array   $form_fields An array of attachment form fields.
#// @param WP_Post $post        The WP_Post attachment object.
#// @return array Filtered attachment form fields.
#//
def media_post_single_attachment_fields_to_edit(form_fields=None, post=None, *args_):
    
    form_fields["image_url"] = None
    return form_fields
# end def media_post_single_attachment_fields_to_edit
#// 
#// Filters input from media_upload_form_handler() and assigns a default
#// post_title from the file name if none supplied.
#// 
#// Illustrates the use of the {@see 'attachment_fields_to_save'} filter
#// which can be used to add default values to any field before saving to DB.
#// 
#// @since 2.5.0
#// 
#// @param array $post       The WP_Post attachment object converted to an array.
#// @param array $attachment An array of attachment metadata.
#// @return array Filtered attachment post object.
#//
def image_attachment_fields_to_save(post=None, attachment=None, *args_):
    
    if php_substr(post["post_mime_type"], 0, 5) == "image":
        if php_strlen(php_trim(post["post_title"])) == 0:
            attachment_url = post["attachment_url"] if (php_isset(lambda : post["attachment_url"])) else post["guid"]
            post["post_title"] = php_preg_replace("/\\.\\w+$/", "", wp_basename(attachment_url))
            post["errors"]["post_title"]["errors"][-1] = __("Empty Title filled from filename.")
        # end if
    # end if
    return post
# end def image_attachment_fields_to_save
#// 
#// Retrieves the media element HTML to send to the editor.
#// 
#// @since 2.5.0
#// 
#// @param string $html
#// @param integer $attachment_id
#// @param array $attachment
#// @return string
#//
def image_media_send_to_editor(html=None, attachment_id=None, attachment=None, *args_):
    
    post = get_post(attachment_id)
    if php_substr(post.post_mime_type, 0, 5) == "image":
        url = attachment["url"]
        align = attachment["align"] if (not php_empty(lambda : attachment["align"])) else "none"
        size = attachment["image-size"] if (not php_empty(lambda : attachment["image-size"])) else "medium"
        alt = attachment["image_alt"] if (not php_empty(lambda : attachment["image_alt"])) else ""
        rel = php_strpos(url, "attachment_id") or get_attachment_link(attachment_id) == url
        return get_image_send_to_editor(attachment_id, attachment["post_excerpt"], attachment["post_title"], align, url, rel, size, alt)
    # end if
    return html
# end def image_media_send_to_editor
#// 
#// Retrieves the attachment fields to edit form fields.
#// 
#// @since 2.5.0
#// 
#// @param WP_Post $post
#// @param array $errors
#// @return array
#//
def get_attachment_fields_to_edit(post=None, errors=None, *args_):
    
    if php_is_int(post):
        post = get_post(post)
    # end if
    if php_is_array(post):
        post = php_new_class("WP_Post", lambda : WP_Post(post))
    # end if
    image_url = wp_get_attachment_url(post.ID)
    edit_post = sanitize_post(post, "edit")
    form_fields = Array({"post_title": Array({"label": __("Title"), "value": edit_post.post_title})}, {"image_alt": Array(), "post_excerpt": Array({"label": __("Caption"), "input": "html", "html": wp_caption_input_textarea(edit_post)})}, {"post_content": Array({"label": __("Description"), "value": edit_post.post_content, "input": "textarea"})}, {"url": Array({"label": __("Link URL"), "input": "html", "html": image_link_input_fields(post, get_option("image_default_link_type")), "helps": __("Enter a link URL or click above for presets.")})}, {"menu_order": Array({"label": __("Order"), "value": edit_post.menu_order})}, {"image_url": Array({"label": __("File URL"), "input": "html", "html": str("<input type='text' class='text urlfield' readonly='readonly' name='attachments[") + str(post.ID) + str("][url]' value='") + esc_attr(image_url) + "' /><br />", "value": wp_get_attachment_url(post.ID), "helps": __("Location of the uploaded file.")})})
    for taxonomy in get_attachment_taxonomies(post):
        t = get_taxonomy(taxonomy)
        if (not t["public"]) or (not t["show_ui"]):
            continue
        # end if
        if php_empty(lambda : t["label"]):
            t["label"] = taxonomy
        # end if
        if php_empty(lambda : t["args"]):
            t["args"] = Array()
        # end if
        terms = get_object_term_cache(post.ID, taxonomy)
        if False == terms:
            terms = wp_get_object_terms(post.ID, taxonomy, t["args"])
        # end if
        values = Array()
        for term in terms:
            values[-1] = term.slug
        # end for
        t["value"] = join(", ", values)
        form_fields[taxonomy] = t
    # end for
    #// 
    #// Merge default fields with their errors, so any key passed with the error
    #// (e.g. 'error', 'helps', 'value') will replace the default.
    #// The recursive merge is easily traversed with array casting:
    #// foreach ( (array) $things as $thing )
    #//
    form_fields = php_array_merge_recursive(form_fields, errors)
    #// This was formerly in image_attachment_fields_to_edit().
    if php_substr(post.post_mime_type, 0, 5) == "image":
        alt = get_post_meta(post.ID, "_wp_attachment_image_alt", True)
        if php_empty(lambda : alt):
            alt = ""
        # end if
        form_fields["post_title"]["required"] = True
        form_fields["image_alt"] = Array({"value": alt, "label": __("Alternative Text"), "helps": __("Alt text for the image, e.g. &#8220;The Mona Lisa&#8221;")})
        form_fields["align"] = Array({"label": __("Alignment"), "input": "html", "html": image_align_input_fields(post, get_option("image_default_align"))})
        form_fields["image-size"] = image_size_input_fields(post, get_option("image_default_size", "medium"))
    else:
        form_fields["image_alt"] = None
    # end if
    #// 
    #// Filters the attachment fields to edit.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array   $form_fields An array of attachment form fields.
    #// @param WP_Post $post        The WP_Post attachment object.
    #//
    form_fields = apply_filters("attachment_fields_to_edit", form_fields, post)
    return form_fields
# end def get_attachment_fields_to_edit
#// 
#// Retrieve HTML for media items of post gallery.
#// 
#// The HTML markup retrieved will be created for the progress of SWF Upload
#// component. Will also create link for showing and hiding the form to modify
#// the image attachment.
#// 
#// @since 2.5.0
#// 
#// @global WP_Query $wp_the_query WordPress Query object.
#// 
#// @param int $post_id Optional. Post ID.
#// @param array $errors Errors for attachment, if any.
#// @return string
#//
def get_media_items(post_id=None, errors=None, *args_):
    
    attachments = Array()
    if post_id:
        post = get_post(post_id)
        if post and "attachment" == post.post_type:
            attachments = Array({post.ID: post})
        else:
            attachments = get_children(Array({"post_parent": post_id, "post_type": "attachment", "orderby": "menu_order ASC, ID", "order": "DESC"}))
        # end if
    else:
        if php_is_array(PHP_GLOBALS["wp_the_query"].posts):
            for attachment in PHP_GLOBALS["wp_the_query"].posts:
                attachments[attachment.ID] = attachment
            # end for
        # end if
    # end if
    output = ""
    for id,attachment in attachments:
        if "trash" == attachment.post_status:
            continue
        # end if
        item = get_media_item(id, Array({"errors": errors[id] if (php_isset(lambda : errors[id])) else None}))
        if item:
            output += str("\n<div id='media-item-") + str(id) + str("' class='media-item child-of-") + str(attachment.post_parent) + str(" preloaded'><div class='progress hidden'><div class='bar'></div></div><div id='media-upload-error-") + str(id) + str("' class='hidden'></div><div class='filename hidden'></div>") + str(item) + str("\n</div>")
        # end if
    # end for
    return output
# end def get_media_items
#// 
#// Retrieve HTML form for modifying the image attachment.
#// 
#// @since 2.5.0
#// 
#// @global string $redir_tab
#// 
#// @param int $attachment_id Attachment ID for modification.
#// @param string|array $args Optional. Override defaults.
#// @return string HTML form for attachment.
#//
def get_media_item(attachment_id=None, args=None, *args_):
    
    global redir_tab
    php_check_if_defined("redir_tab")
    thumb_url = False
    attachment_id = php_intval(attachment_id)
    if attachment_id:
        thumb_url = wp_get_attachment_image_src(attachment_id, "thumbnail", True)
        if thumb_url:
            thumb_url = thumb_url[0]
        # end if
    # end if
    post = get_post(attachment_id)
    current_post_id = php_int(PHP_REQUEST["post_id"]) if (not php_empty(lambda : PHP_REQUEST["post_id"])) else 0
    default_args = Array({"errors": None, "send": post_type_supports(get_post_type(current_post_id), "editor") if current_post_id else True, "delete": True, "toggle": True, "show_title": True})
    parsed_args = wp_parse_args(args, default_args)
    #// 
    #// Filters the arguments used to retrieve an image for the edit image form.
    #// 
    #// @since 3.1.0
    #// 
    #// @see get_media_item
    #// 
    #// @param array $parsed_args An array of arguments.
    #//
    parsed_args = apply_filters("get_media_item_args", parsed_args)
    toggle_on = __("Show")
    toggle_off = __("Hide")
    file = get_attached_file(post.ID)
    filename = esc_html(wp_basename(file))
    title = esc_attr(post.post_title)
    post_mime_types = get_post_mime_types()
    keys = php_array_keys(wp_match_mime_types(php_array_keys(post_mime_types), post.post_mime_type))
    type = reset(keys)
    type_html = str("<input type='hidden' id='type-of-") + str(attachment_id) + str("' value='") + esc_attr(type) + "' />"
    form_fields = get_attachment_fields_to_edit(post, parsed_args["errors"])
    if parsed_args["toggle"]:
        class_ = "startclosed" if php_empty(lambda : parsed_args["errors"]) else "startopen"
        toggle_links = str("\n      <a class='toggle describe-toggle-on' href='#'>") + str(toggle_on) + str("</a>\n     <a class='toggle describe-toggle-off' href='#'>") + str(toggle_off) + str("</a>")
    else:
        class_ = ""
        toggle_links = ""
    # end if
    display_title = title if (not php_empty(lambda : title)) else filename
    #// $title shouldn't ever be empty, but just in case.
    display_title = "<div class='filename new'><span class='title'>" + wp_html_excerpt(display_title, 60, "&hellip;") + "</span></div>" if parsed_args["show_title"] else ""
    gallery = (php_isset(lambda : PHP_REQUEST["tab"])) and "gallery" == PHP_REQUEST["tab"] or (php_isset(lambda : redir_tab)) and "gallery" == redir_tab
    order = ""
    for key,val in form_fields:
        if "menu_order" == key:
            if gallery:
                order = str("<div class='menu_order'> <input class='menu_order_input' type='text' id='attachments[") + str(attachment_id) + str("][menu_order]' name='attachments[") + str(attachment_id) + str("][menu_order]' value='") + esc_attr(val["value"]) + "' /></div>"
            else:
                order = str("<input type='hidden' name='attachments[") + str(attachment_id) + str("][menu_order]' value='") + esc_attr(val["value"]) + "' />"
            # end if
            form_fields["menu_order"] = None
            break
        # end if
    # end for
    media_dims = ""
    meta = wp_get_attachment_metadata(post.ID)
    if (php_isset(lambda : meta["width"]) and php_isset(lambda : meta["height"])):
        media_dims += str("<span id='media-dims-") + str(post.ID) + str("'>") + str(meta["width"]) + str("&nbsp;&times;&nbsp;") + str(meta["height"]) + str("</span> ")
    # end if
    #// 
    #// Filters the media metadata.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string  $media_dims The HTML markup containing the media dimensions.
    #// @param WP_Post $post       The WP_Post attachment object.
    #//
    media_dims = apply_filters("media_meta", media_dims, post)
    image_edit_button = ""
    if wp_attachment_is_image(post.ID) and wp_image_editor_supports(Array({"mime_type": post.post_mime_type})):
        nonce = wp_create_nonce(str("image_editor-") + str(post.ID))
        image_edit_button = str("<input type='button' id='imgedit-open-btn-") + str(post.ID) + str("' onclick='imageEdit.open( ") + str(post.ID) + str(", \"") + str(nonce) + str("\" )' class='button' value='") + esc_attr__("Edit Image") + "' /> <span class='spinner'></span>"
    # end if
    attachment_url = get_permalink(attachment_id)
    item = str("\n      ") + str(type_html) + str("\n       ") + str(toggle_links) + str("\n        ") + str(order) + str("\n       ") + str(display_title) + str("\n       <table class='slidetoggle describe ") + str(class_) + str("'>\n         <thead class='media-item-info' id='media-head-") + str(post.ID) + str("'>\n         <tr>\n          <td class='A1B1' id='thumbnail-head-") + str(post.ID) + str("'>\n           <p><a href='") + str(attachment_url) + str("' target='_blank'><img class='thumbnail' src='") + str(thumb_url) + str("' alt='' /></a></p>\n          <p>") + str(image_edit_button) + str("""</p>\n          </td>\n         <td>\n          <p><strong>""") + __("File name:") + str("</strong> ") + str(filename) + str("</p>\n            <p><strong>") + __("File type:") + str("</strong> ") + str(post.post_mime_type) + str("</p>\n           <p><strong>") + __("Upload date:") + "</strong> " + mysql2date(__("F j, Y"), post.post_date) + "</p>"
    if (not php_empty(lambda : media_dims)):
        item += "<p><strong>" + __("Dimensions:") + str("</strong> ") + str(media_dims) + str("</p>\n")
    # end if
    item += "</td></tr>\n"
    item += str("""\n       </thead>\n      <tbody>\n       <tr><td colspan='2' class='imgedit-response' id='imgedit-response-""") + str(post.ID) + str("'></td></tr>\n\n       <tr><td style='display:none' colspan='2' class='image-editor' id='image-editor-") + str(post.ID) + str("'></td></tr>\n\n        <tr><td colspan='2'><p class='media-types media-types-required-info'>") + php_sprintf(__("Required fields are marked %s"), "<span class=\"required\">*</span>") + "</p></td></tr>\n"
    defaults = Array({"input": "text", "required": False, "value": "", "extra_rows": Array()})
    if parsed_args["send"]:
        parsed_args["send"] = get_submit_button(__("Insert into Post"), "", str("send[") + str(attachment_id) + str("]"), False)
    # end if
    delete = "" if php_empty(lambda : parsed_args["delete"]) else parsed_args["delete"]
    if delete and current_user_can("delete_post", attachment_id):
        if (not EMPTY_TRASH_DAYS):
            delete = "<a href='" + wp_nonce_url(str("post.php?action=delete&amp;post=") + str(attachment_id), "delete-post_" + attachment_id) + str("' id='del[") + str(attachment_id) + str("]' class='delete-permanently'>") + __("Delete Permanently") + "</a>"
        elif (not MEDIA_TRASH):
            delete = str("<a href='#' class='del-link' onclick=\"document.getElementById('del_attachment_") + str(attachment_id) + str("').style.display='block';return false;\">") + __("Delete") + str("</a>\n                <div id='del_attachment_") + str(attachment_id) + str("' class='del-attachment' style='display:none;'>") + "<p>" + php_sprintf(__("You are about to delete %s."), "<strong>" + filename + "</strong>") + "</p>\n                <a href='" + wp_nonce_url(str("post.php?action=delete&amp;post=") + str(attachment_id), "delete-post_" + attachment_id) + str("' id='del[") + str(attachment_id) + str("]' class='button'>") + __("Continue") + "</a>\n             <a href='#' class='button' onclick=\"this.parentNode.style.display='none';return false;\">" + __("Cancel") + "</a>\n                </div>"
        else:
            delete = "<a href='" + wp_nonce_url(str("post.php?action=trash&amp;post=") + str(attachment_id), "trash-post_" + attachment_id) + str("' id='del[") + str(attachment_id) + str("]' class='delete'>") + __("Move to Trash") + "</a>\n            <a href='" + wp_nonce_url(str("post.php?action=untrash&amp;post=") + str(attachment_id), "untrash-post_" + attachment_id) + str("' id='undo[") + str(attachment_id) + str("]' class='undo hidden'>") + __("Undo") + "</a>"
        # end if
    else:
        delete = ""
    # end if
    thumbnail = ""
    calling_post_id = 0
    if (php_isset(lambda : PHP_REQUEST["post_id"])):
        calling_post_id = absint(PHP_REQUEST["post_id"])
    elif (php_isset(lambda : PHP_POST)) and php_count(PHP_POST):
        #// Like for async-upload where $_GET['post_id'] isn't set.
        calling_post_id = post.post_parent
    # end if
    if "image" == type and calling_post_id and current_theme_supports("post-thumbnails", get_post_type(calling_post_id)) and post_type_supports(get_post_type(calling_post_id), "thumbnail") and get_post_thumbnail_id(calling_post_id) != attachment_id:
        calling_post = get_post(calling_post_id)
        calling_post_type_object = get_post_type_object(calling_post.post_type)
        ajax_nonce = wp_create_nonce(str("set_post_thumbnail-") + str(calling_post_id))
        thumbnail = "<a class='wp-post-thumbnail' id='wp-post-thumbnail-" + attachment_id + str("' href='#' onclick='WPSetAsThumbnail(\"") + str(attachment_id) + str("\", \"") + str(ajax_nonce) + str("\");return false;'>") + esc_html(calling_post_type_object.labels.use_featured_image) + "</a>"
    # end if
    if parsed_args["send"] or thumbnail or delete and (not (php_isset(lambda : form_fields["buttons"]))):
        form_fields["buttons"] = Array({"tr": "     <tr class='submit'><td></td><td class='savesend'>" + parsed_args["send"] + str(" ") + str(thumbnail) + str(" ") + str(delete) + str("</td></tr>\n")})
    # end if
    hidden_fields = Array()
    for id,field in form_fields:
        if "_" == id[0]:
            continue
        # end if
        if (not php_empty(lambda : field["tr"])):
            item += field["tr"]
            continue
        # end if
        field = php_array_merge(defaults, field)
        name = str("attachments[") + str(attachment_id) + str("][") + str(id) + str("]")
        if "hidden" == field["input"]:
            hidden_fields[name] = field["value"]
            continue
        # end if
        required = "<span class=\"required\">*</span>" if field["required"] else ""
        required_attr = " required" if field["required"] else ""
        class_ = id
        class_ += " form-required" if field["required"] else ""
        item += str("       <tr class='") + str(class_) + str("'>\n         <th scope='row' class='label'><label for='") + str(name) + str("'><span class='alignleft'>") + str(field["label"]) + str(required) + str("</span><br class='clear' /></label></th>\n            <td class='field'>")
        if (not php_empty(lambda : field[field["input"]])):
            item += field[field["input"]]
        elif "textarea" == field["input"]:
            if "post_content" == id and user_can_richedit():
                #// Sanitize_post() skips the post_content when user_can_richedit.
                field["value"] = htmlspecialchars(field["value"], ENT_QUOTES)
            # end if
            #// Post_excerpt is already escaped by sanitize_post() in get_attachment_fields_to_edit().
            item += str("<textarea id='") + str(name) + str("' name='") + str(name) + str("'") + str(required_attr) + str(">") + field["value"] + "</textarea>"
        else:
            item += str("<input type='text' class='text' id='") + str(name) + str("' name='") + str(name) + str("' value='") + esc_attr(field["value"]) + str("'") + str(required_attr) + str(" />")
        # end if
        if (not php_empty(lambda : field["helps"])):
            item += "<p class='help'>" + join("</p>\n<p class='help'>", array_unique(field["helps"])) + "</p>"
        # end if
        item += "</td>\n        </tr>\n"
        extra_rows = Array()
        if (not php_empty(lambda : field["errors"])):
            for error in array_unique(field["errors"]):
                extra_rows["error"][-1] = error
            # end for
        # end if
        if (not php_empty(lambda : field["extra_rows"])):
            for class_,rows in field["extra_rows"]:
                for html in rows:
                    extra_rows[class_][-1] = html
                # end for
            # end for
        # end if
        for class_,rows in extra_rows:
            for html in rows:
                item += str("       <tr><td></td><td class='") + str(class_) + str("'>") + str(html) + str("</td></tr>\n")
            # end for
        # end for
    # end for
    if (not php_empty(lambda : form_fields["_final"])):
        item += str("       <tr class='final'><td colspan='2'>") + str(form_fields["_final"]) + str("</td></tr>\n")
    # end if
    item += "   </tbody>\n"
    item += "   </table>\n"
    for name,value in hidden_fields:
        item += str("   <input type='hidden' name='") + str(name) + str("' id='") + str(name) + str("' value='") + esc_attr(value) + "' />\n"
    # end for
    if post.post_parent < 1 and (php_isset(lambda : PHP_REQUEST["post_id"])):
        parent = php_int(PHP_REQUEST["post_id"])
        parent_name = str("attachments[") + str(attachment_id) + str("][post_parent]")
        item += str("   <input type='hidden' name='") + str(parent_name) + str("' id='") + str(parent_name) + str("' value='") + str(parent) + str("' />\n")
    # end if
    return item
# end def get_media_item
#// 
#// @since 3.5.0
#// 
#// @param int   $attachment_id
#// @param array $args
#// @return array
#//
def get_compat_media_markup(attachment_id=None, args=None, *args_):
    
    post = get_post(attachment_id)
    default_args = Array({"errors": None, "in_modal": False})
    user_can_edit = current_user_can("edit_post", attachment_id)
    args = wp_parse_args(args, default_args)
    #// This filter is documented in wp-admin/includes/media.php
    args = apply_filters("get_media_item_args", args)
    form_fields = Array()
    if args["in_modal"]:
        for taxonomy in get_attachment_taxonomies(post):
            t = get_taxonomy(taxonomy)
            if (not t["public"]) or (not t["show_ui"]):
                continue
            # end if
            if php_empty(lambda : t["label"]):
                t["label"] = taxonomy
            # end if
            if php_empty(lambda : t["args"]):
                t["args"] = Array()
            # end if
            terms = get_object_term_cache(post.ID, taxonomy)
            if False == terms:
                terms = wp_get_object_terms(post.ID, taxonomy, t["args"])
            # end if
            values = Array()
            for term in terms:
                values[-1] = term.slug
            # end for
            t["value"] = join(", ", values)
            t["taxonomy"] = True
            form_fields[taxonomy] = t
        # end for
    # end if
    #// 
    #// Merge default fields with their errors, so any key passed with the error
    #// (e.g. 'error', 'helps', 'value') will replace the default.
    #// The recursive merge is easily traversed with array casting:
    #// foreach ( (array) $things as $thing )
    #//
    form_fields = php_array_merge_recursive(form_fields, args["errors"])
    #// This filter is documented in wp-admin/includes/media.php
    form_fields = apply_filters("attachment_fields_to_edit", form_fields, post)
    form_fields["image-size"] = None
    form_fields["align"] = None
    form_fields["image_alt"] = None
    form_fields["post_title"] = None
    form_fields["post_excerpt"] = None
    form_fields["post_content"] = None
    form_fields["url"] = None
    form_fields["menu_order"] = None
    form_fields["image_url"] = None
    #// This filter is documented in wp-admin/includes/media.php
    media_meta = apply_filters("media_meta", "", post)
    defaults = Array({"input": "text", "required": False, "value": "", "extra_rows": Array(), "show_in_edit": True, "show_in_modal": True})
    hidden_fields = Array()
    item = ""
    for id,field in form_fields:
        if "_" == id[0]:
            continue
        # end if
        name = str("attachments[") + str(attachment_id) + str("][") + str(id) + str("]")
        id_attr = str("attachments-") + str(attachment_id) + str("-") + str(id)
        if (not php_empty(lambda : field["tr"])):
            item += field["tr"]
            continue
        # end if
        field = php_array_merge(defaults, field)
        if (not field["show_in_edit"]) and (not args["in_modal"]) or (not field["show_in_modal"]) and args["in_modal"]:
            continue
        # end if
        if "hidden" == field["input"]:
            hidden_fields[name] = field["value"]
            continue
        # end if
        readonly = " readonly='readonly' " if (not user_can_edit) and (not php_empty(lambda : field["taxonomy"])) else ""
        required = "<span class=\"required\">*</span>" if field["required"] else ""
        required_attr = " required" if field["required"] else ""
        class_ = "compat-field-" + id
        class_ += " form-required" if field["required"] else ""
        item += str("       <tr class='") + str(class_) + str("'>")
        item += str("           <th scope='row' class='label'><label for='") + str(id_attr) + str("'><span class='alignleft'>") + str(field["label"]) + str("</span>") + str(required) + str("<br class='clear' /></label>")
        item += "</th>\n            <td class='field'>"
        if (not php_empty(lambda : field[field["input"]])):
            item += field[field["input"]]
        elif "textarea" == field["input"]:
            if "post_content" == id and user_can_richedit():
                #// sanitize_post() skips the post_content when user_can_richedit.
                field["value"] = htmlspecialchars(field["value"], ENT_QUOTES)
            # end if
            item += str("<textarea id='") + str(id_attr) + str("' name='") + str(name) + str("'") + str(required_attr) + str(">") + field["value"] + "</textarea>"
        else:
            item += str("<input type='text' class='text' id='") + str(id_attr) + str("' name='") + str(name) + str("' value='") + esc_attr(field["value"]) + str("' ") + str(readonly) + str(required_attr) + str(" />")
        # end if
        if (not php_empty(lambda : field["helps"])):
            item += "<p class='help'>" + join("</p>\n<p class='help'>", array_unique(field["helps"])) + "</p>"
        # end if
        item += "</td>\n        </tr>\n"
        extra_rows = Array()
        if (not php_empty(lambda : field["errors"])):
            for error in array_unique(field["errors"]):
                extra_rows["error"][-1] = error
            # end for
        # end if
        if (not php_empty(lambda : field["extra_rows"])):
            for class_,rows in field["extra_rows"]:
                for html in rows:
                    extra_rows[class_][-1] = html
                # end for
            # end for
        # end if
        for class_,rows in extra_rows:
            for html in rows:
                item += str("       <tr><td></td><td class='") + str(class_) + str("'>") + str(html) + str("</td></tr>\n")
            # end for
        # end for
    # end for
    if (not php_empty(lambda : form_fields["_final"])):
        item += str("       <tr class='final'><td colspan='2'>") + str(form_fields["_final"]) + str("</td></tr>\n")
    # end if
    if item:
        item = "<p class=\"media-types media-types-required-info\">" + php_sprintf(__("Required fields are marked %s"), "<span class=\"required\">*</span>") + "</p>" + "<table class=\"compat-attachment-fields\">" + item + "</table>"
    # end if
    for hidden_field,value in hidden_fields:
        item += "<input type=\"hidden\" name=\"" + esc_attr(hidden_field) + "\" value=\"" + esc_attr(value) + "\" />" + "\n"
    # end for
    if item:
        item = "<input type=\"hidden\" name=\"attachments[" + attachment_id + "][menu_order]\" value=\"" + esc_attr(post.menu_order) + "\" />" + item
    # end if
    return Array({"item": item, "meta": media_meta})
# end def get_compat_media_markup
#// 
#// Outputs the legacy media upload header.
#// 
#// @since 2.5.0
#//
def media_upload_header(*args_):
    
    post_id = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    php_print("<script type=\"text/javascript\">post_id = " + post_id + ";</script>")
    if php_empty(lambda : PHP_REQUEST["chromeless"]):
        php_print("<div id=\"media-upload-header\">")
        the_media_upload_tabs()
        php_print("</div>")
    # end if
# end def media_upload_header
#// 
#// Outputs the legacy media upload form.
#// 
#// @since 2.5.0
#// 
#// @global string $type
#// @global string $tab
#// @global bool   $is_IE
#// @global bool   $is_opera
#// 
#// @param array $errors
#//
def media_upload_form(errors=None, *args_):
    
    global type,tab,is_IE,is_opera
    php_check_if_defined("type","tab","is_IE","is_opera")
    if (not _device_can_upload()):
        php_print("<p>" + php_sprintf(__("The web browser on your device cannot be used to upload files. You may be able to use the <a href=\"%s\">native app for your device</a> instead."), "https://apps.wordpress.org/") + "</p>")
        return
    # end if
    upload_action_url = admin_url("async-upload.php")
    post_id = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    _type = type if (php_isset(lambda : type)) else ""
    _tab = tab if (php_isset(lambda : tab)) else ""
    max_upload_size = wp_max_upload_size()
    if (not max_upload_size):
        max_upload_size = 0
    # end if
    php_print(" <div id=\"media-upload-notice\">\n  ")
    if (php_isset(lambda : errors["upload_notice"])):
        php_print(errors["upload_notice"])
    # end if
    php_print(" </div>\n    <div id=\"media-upload-error\">\n   ")
    if (php_isset(lambda : errors["upload_error"])) and is_wp_error(errors["upload_error"]):
        php_print(errors["upload_error"].get_error_message())
    # end if
    php_print(" </div>\n    ")
    if is_multisite() and (not is_upload_space_available()):
        #// 
        #// Fires when an upload will exceed the defined upload space quota for a network site.
        #// 
        #// @since 3.5.0
        #//
        do_action("upload_ui_over_quota")
        return
    # end if
    #// 
    #// Fires just before the legacy (pre-3.5.0) upload interface is loaded.
    #// 
    #// @since 2.6.0
    #//
    do_action("pre-upload-ui")
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    post_params = Array({"post_id": post_id, "_wpnonce": wp_create_nonce("media-form"), "type": _type, "tab": _tab, "short": "1"})
    #// 
    #// Filters the media upload post parameters.
    #// 
    #// @since 3.1.0 As 'swfupload_post_params'
    #// @since 3.3.0
    #// 
    #// @param array $post_params An array of media upload parameters used by Plupload.
    #//
    post_params = apply_filters("upload_post_params", post_params)
    #// 
    #// Since 4.9 the `runtimes` setting is hardcoded in our version of Plupload to `html5,html4`,
    #// and the `flash_swf_url` and `silverlight_xap_url` are not used.
    #//
    plupload_init = Array({"browse_button": "plupload-browse-button", "container": "plupload-upload-ui", "drop_element": "drag-drop-area", "file_data_name": "async-upload", "url": upload_action_url, "filters": Array({"max_file_size": max_upload_size + "b"})}, {"multipart_params": post_params})
    #// 
    #// Currently only iOS Safari supports multiple files uploading,
    #// but iOS 7.x has a bug that prevents uploading of videos when enabled.
    #// See #29602.
    #//
    if wp_is_mobile() and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "OS 7_") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "like Mac OS X") != False:
        plupload_init["multi_selection"] = False
    # end if
    #// 
    #// Filters the default Plupload settings.
    #// 
    #// @since 3.3.0
    #// 
    #// @param array $plupload_init An array of default settings used by Plupload.
    #//
    plupload_init = apply_filters("plupload_init", plupload_init)
    php_print(" <script type=\"text/javascript\">\n ")
    #// Verify size is an int. If not return default value.
    large_size_h = absint(get_option("large_size_h"))
    if (not large_size_h):
        large_size_h = 1024
    # end if
    large_size_w = absint(get_option("large_size_w"))
    if (not large_size_w):
        large_size_w = 1024
    # end if
    php_print(" var resize_height = ")
    php_print(large_size_h)
    php_print(", resize_width = ")
    php_print(large_size_w)
    php_print(",\n  wpUploaderInit = ")
    php_print(wp_json_encode(plupload_init))
    php_print(""";
    </script>
    <div id=\"plupload-upload-ui\" class=\"hide-if-no-js\">
    """)
    #// 
    #// Fires before the upload interface loads.
    #// 
    #// @since 2.6.0 As 'pre-flash-upload-ui'
    #// @since 3.3.0
    #//
    do_action("pre-plupload-upload-ui")
    pass
    php_print(" <div id=\"drag-drop-area\">\n       <div class=\"drag-drop-inside\">\n      <p class=\"drag-drop-info\">")
    _e("Drop files to upload")
    php_print("</p>\n       <p>")
    _ex("or", "Uploader: Drop files here - or - Select Files")
    php_print("</p>\n       <p class=\"drag-drop-buttons\"><input id=\"plupload-browse-button\" type=\"button\" value=\"")
    esc_attr_e("Select Files")
    php_print("""\" class=\"button\" /></p>
    </div>
    </div>
    """)
    #// 
    #// Fires after the upload interface loads.
    #// 
    #// @since 2.6.0 As 'post-flash-upload-ui'
    #// @since 3.3.0
    #//
    do_action("post-plupload-upload-ui")
    pass
    php_print("""   </div>
    <div id=\"html-upload-ui\" class=\"hide-if-js\">
    """)
    #// 
    #// Fires before the upload button in the media upload interface.
    #// 
    #// @since 2.6.0
    #//
    do_action("pre-html-upload-ui")
    pass
    php_print(" <p id=\"async-upload-wrap\">\n      <label class=\"screen-reader-text\" for=\"async-upload\">")
    _e("Upload")
    php_print("</label>\n       <input type=\"file\" name=\"async-upload\" id=\"async-upload\" />\n     ")
    submit_button(__("Upload"), "primary", "html-upload", False)
    php_print("     <a href=\"#\" onclick=\"try{top.tb_remove();}catch(e){}; return false;\">")
    _e("Cancel")
    php_print("""</a>
    </p>
    <div class=\"clear\"></div>
    """)
    #// 
    #// Fires after the upload button in the media upload interface.
    #// 
    #// @since 2.6.0
    #//
    do_action("post-html-upload-ui")
    pass
    php_print("""   </div>
    <p class=\"max-upload-size\">
    """)
    #// translators: %s: Maximum allowed file size.
    printf(__("Maximum upload file size: %s."), esc_html(size_format(max_upload_size)))
    php_print("</p>\n   ")
    #// 
    #// Fires on the post upload UI screen.
    #// 
    #// Legacy (pre-3.5.0) media workflow hook.
    #// 
    #// @since 2.6.0
    #//
    do_action("post-upload-ui")
    pass
# end def media_upload_form
#// 
#// Outputs the legacy media upload form for a given media type.
#// 
#// @since 2.5.0
#// 
#// @param string $type
#// @param object $errors
#// @param integer $id
#//
def media_upload_type_form(type="file", errors=None, id=None, *args_):
    
    media_upload_header()
    post_id = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    form_action_url = admin_url(str("media-upload.php?type=") + str(type) + str("&tab=type&post_id=") + str(post_id))
    #// 
    #// Filters the media upload form action URL.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $form_action_url The media upload form action URL.
    #// @param string $type            The type of media. Default 'file'.
    #//
    form_action_url = apply_filters("media_upload_form_url", form_action_url, type)
    form_class = "media-upload-form type-form validate"
    if get_user_setting("uploader"):
        form_class += " html-uploader"
    # end if
    php_print(" <form enctype=\"multipart/form-data\" method=\"post\" action=\"")
    php_print(esc_url(form_action_url))
    php_print("\" class=\"")
    php_print(form_class)
    php_print("\" id=\"")
    php_print(type)
    php_print("-form\">\n       ")
    submit_button("", "hidden", "save", False)
    php_print(" <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id))
    php_print("\" />\n      ")
    wp_nonce_field("media-form")
    php_print("\n   <h3 class=\"media-title\">")
    _e("Add media files from your computer")
    php_print("</h3>\n\n    ")
    media_upload_form(errors)
    php_print("""
    <script type=\"text/javascript\">
    jQuery(function($){
    var preloaded = $(\".media-item.preloaded\");
if ( preloaded.length > 0 ) {
    preloaded.each(function(){prepareMediaItem({id:this.id.replace(/[^0-9]/g, '')},'');});
    }
    updateMediaForm();
    });
    </script>
    <div id=\"media-items\">
    """)
    if id:
        if (not is_wp_error(id)):
            add_filter("attachment_fields_to_edit", "media_post_single_attachment_fields_to_edit", 10, 2)
            php_print(get_media_items(id, errors))
        else:
            php_print("<div id=\"media-upload-error\">" + esc_html(id.get_error_message()) + "</div></div>")
            php_exit(0)
        # end if
    # end if
    php_print("""   </div>
    <p class=\"savebutton ml-submit\">
    """)
    submit_button(__("Save all changes"), "", "save", False)
    php_print(" </p>\n  </form>\n   ")
# end def media_upload_type_form
#// 
#// Outputs the legacy media upload form for external media.
#// 
#// @since 2.7.0
#// 
#// @param string $type
#// @param object $errors
#// @param integer $id
#//
def media_upload_type_url_form(type=None, errors=None, id=None, *args_):
    
    if None == type:
        type = "image"
    # end if
    media_upload_header()
    post_id = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    form_action_url = admin_url(str("media-upload.php?type=") + str(type) + str("&tab=type&post_id=") + str(post_id))
    #// This filter is documented in wp-admin/includes/media.php
    form_action_url = apply_filters("media_upload_form_url", form_action_url, type)
    form_class = "media-upload-form type-form validate"
    if get_user_setting("uploader"):
        form_class += " html-uploader"
    # end if
    php_print(" <form enctype=\"multipart/form-data\" method=\"post\" action=\"")
    php_print(esc_url(form_action_url))
    php_print("\" class=\"")
    php_print(form_class)
    php_print("\" id=\"")
    php_print(type)
    php_print("-form\">\n   <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id))
    php_print("\" />\n      ")
    wp_nonce_field("media-form")
    php_print("\n   <h3 class=\"media-title\">")
    _e("Insert media from another website")
    php_print("""</h3>
    <script type=\"text/javascript\">
    var addExtImage = {
    width : '',
    height : '',
    align : 'alignnone',
    insert : function() {
    var t = this, html, f = document.forms[0], cls, title = '', alt = '', caption = '';
if ( '' == f.src.value || '' == t.width )
    return false;
if ( f.alt.value )
    alt = f.alt.value.replace(/'/g, '&#039;').replace(/\"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    """)
    #// This filter is documented in wp-admin/includes/media.php
    if (not apply_filters("disable_captions", "")):
        php_print("""           if ( f.caption.value ) {
        caption = f.caption.value.replace(/\\r\\n|\\r/g, '\\n');
        caption = caption.replace(/<[a-zA-Z0-9]+( [^<>]+)?>/g, function(a){
        return a.replace(/[\\r\\n\\t]+/, ' ');
        });
        caption = caption.replace(/\\s*\\n\\s*/g, '<br />');
        }
        """)
    # end if
    php_print("""       cls = caption ? '' : ' class=\"'+t.align+'\"';
    html = '<img alt=\"'+alt+'\" src=\"'+f.src.value+'\"'+cls+' width=\"'+t.width+'\" height=\"'+t.height+'\" />';
if ( f.url.value ) {
    url = f.url.value.replace(/'/g, '&#039;').replace(/\"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    html = '<a href=\"'+url+'\">'+html+'</a>';
    }
if ( caption )
    html = '[caption id=\"\" align=\"'+t.align+'\" width=\"'+t.width+'\"]'+html+caption+'[/caption]';
    var win = window.dialogArguments || opener || parent || top;
    win.send_to_editor(html);
    return false;
    },
    resetImageData : function() {
    var t = addExtImage;
    t.width = t.height = '';
    document.getElementById('go_button').style.color = '#bbb';
if ( ! document.forms[0].src.value )
    document.getElementById('status_img').innerHTML = '';
else document.getElementById('status_img').innerHTML = '<img src=\"""")
    php_print(esc_url(admin_url("images/no.png")))
    php_print("""\" alt=\"\" />';
    },
    updateImageData : function() {
    var t = addExtImage;
    t.width = t.preloadImg.width;
    t.height = t.preloadImg.height;
    document.getElementById('go_button').style.color = '#333';
    document.getElementById('status_img').innerHTML = '<img src=\"""")
    php_print(esc_url(admin_url("images/yes.png")))
    php_print("""\" alt=\"\" />';
    },
    getImageData : function() {
if ( jQuery('table.describe').hasClass('not-image') )
    return;
    var t = addExtImage, src = document.forms[0].src.value;
if ( ! src ) {
    t.resetImageData();
    return false;
    }
    document.getElementById('status_img').innerHTML = '<img src=\"""")
    php_print(esc_url(admin_url("images/spinner-2x.gif")))
    php_print("""\" alt=\"\" width=\"16\" height=\"16\" />';
    t.preloadImg = new Image();
    t.preloadImg.onload = t.updateImageData;
    t.preloadImg.onerror = t.resetImageData;
    t.preloadImg.src = src;
    }
    };
    jQuery(document).ready( function($) {
    $('.media-types input').click( function() {
    $('table.describe').toggleClass('not-image', $('#not-image').prop('checked') );
    });
    });
    </script>
    <div id=\"media-items\">
    <div class=\"media-item media-blank\">
    """)
    #// 
    #// Filters the insert media from URL form HTML.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $form_html The insert from URL form HTML.
    #//
    php_print(apply_filters("type_url_form_media", wp_media_insert_url_form(type)))
    php_print("""   </div>
    </div>
    </form>
    """)
# end def media_upload_type_url_form
#// 
#// Adds gallery form to upload iframe
#// 
#// @since 2.5.0
#// 
#// @global string $redir_tab
#// @global string $type
#// @global string $tab
#// 
#// @param array $errors
#//
def media_upload_gallery_form(errors=None, *args_):
    
    global redir_tab,type
    php_check_if_defined("redir_tab","type")
    redir_tab = "gallery"
    media_upload_header()
    post_id = php_intval(PHP_REQUEST["post_id"])
    form_action_url = admin_url(str("media-upload.php?type=") + str(type) + str("&tab=gallery&post_id=") + str(post_id))
    #// This filter is documented in wp-admin/includes/media.php
    form_action_url = apply_filters("media_upload_form_url", form_action_url, type)
    form_class = "media-upload-form validate"
    if get_user_setting("uploader"):
        form_class += " html-uploader"
    # end if
    php_print("""   <script type=\"text/javascript\">
    jQuery(function($){
    var preloaded = $(\".media-item.preloaded\");
if ( preloaded.length > 0 ) {
    preloaded.each(function(){prepareMediaItem({id:this.id.replace(/[^0-9]/g, '')},'');});
    updateMediaForm();
    }
    });
    </script>
    <div id=\"sort-buttons\" class=\"hide-if-no-js\">
    <span>
    """)
    _e("All Tabs:")
    php_print(" <a href=\"#\" id=\"showall\">")
    _e("Show")
    php_print("</a>\n   <a href=\"#\" id=\"hideall\" style=\"display:none;\">")
    _e("Hide")
    php_print("</a>\n   </span>\n       ")
    _e("Sort Order:")
    php_print(" <a href=\"#\" id=\"asc\">")
    _e("Ascending")
    php_print("</a> |\n <a href=\"#\" id=\"desc\">")
    _e("Descending")
    php_print("</a> |\n <a href=\"#\" id=\"clear\">")
    _ex("Clear", "verb")
    php_print("</a>\n   </div>\n    <form enctype=\"multipart/form-data\" method=\"post\" action=\"")
    php_print(esc_url(form_action_url))
    php_print("\" class=\"")
    php_print(form_class)
    php_print("\" id=\"gallery-form\">\n        ")
    wp_nonce_field("media-form")
    php_print("     ")
    pass
    php_print(" <table class=\"widefat\">\n <thead><tr>\n   <th>")
    _e("Media")
    php_print("</th>\n  <th class=\"order-head\">")
    _e("Order")
    php_print("</th>\n  <th class=\"actions-head\">")
    _e("Actions")
    php_print("""</th>
    </tr></thead>
    </table>
    <div id=\"media-items\">
    """)
    add_filter("attachment_fields_to_edit", "media_post_single_attachment_fields_to_edit", 10, 2)
    php_print("     ")
    php_print(get_media_items(post_id, errors))
    php_print("""   </div>
    <p class=\"ml-submit\">
    """)
    submit_button(__("Save all changes"), "savebutton", "save", False, Array({"id": "save-all", "style": "display: none;"}))
    php_print(" <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id))
    php_print("\" />\n  <input type=\"hidden\" name=\"type\" value=\"")
    php_print(esc_attr(PHP_GLOBALS["type"]))
    php_print("\" />\n  <input type=\"hidden\" name=\"tab\" value=\"")
    php_print(esc_attr(PHP_GLOBALS["tab"]))
    php_print("""\" />
    </p>
    <div id=\"gallery-settings\" style=\"display:none;\">
    <div class=\"title\">""")
    _e("Gallery Settings")
    php_print("""</div>
    <table id=\"basic\" class=\"describe\"><tbody>
    <tr>
    <th scope=\"row\" class=\"label\">
    <label>
    <span class=\"alignleft\">""")
    _e("Link thumbnails to:")
    php_print("""</span>
    </label>
    </th>
    <td class=\"field\">
    <input type=\"radio\" name=\"linkto\" id=\"linkto-file\" value=\"file\" />
    <label for=\"linkto-file\" class=\"radio\">""")
    _e("Image File")
    php_print("""</label>
    <input type=\"radio\" checked=\"checked\" name=\"linkto\" id=\"linkto-post\" value=\"post\" />
    <label for=\"linkto-post\" class=\"radio\">""")
    _e("Attachment Page")
    php_print("""</label>
    </td>
    </tr>
    <tr>
    <th scope=\"row\" class=\"label\">
    <label>
    <span class=\"alignleft\">""")
    _e("Order images by:")
    php_print("""</span>
    </label>
    </th>
    <td class=\"field\">
    <select id=\"orderby\" name=\"orderby\">
    <option value=\"menu_order\" selected=\"selected\">""")
    _e("Menu order")
    php_print("</option>\n              <option value=\"title\">")
    _e("Title")
    php_print("</option>\n              <option value=\"post_date\">")
    _e("Date/Time")
    php_print("</option>\n              <option value=\"rand\">")
    _e("Random")
    php_print("""</option>
    </select>
    </td>
    </tr>
    <tr>
    <th scope=\"row\" class=\"label\">
    <label>
    <span class=\"alignleft\">""")
    _e("Order:")
    php_print("""</span>
    </label>
    </th>
    <td class=\"field\">
    <input type=\"radio\" checked=\"checked\" name=\"order\" id=\"order-asc\" value=\"asc\" />
    <label for=\"order-asc\" class=\"radio\">""")
    _e("Ascending")
    php_print("""</label>
    <input type=\"radio\" name=\"order\" id=\"order-desc\" value=\"desc\" />
    <label for=\"order-desc\" class=\"radio\">""")
    _e("Descending")
    php_print("""</label>
    </td>
    </tr>
    <tr>
    <th scope=\"row\" class=\"label\">
    <label>
    <span class=\"alignleft\">""")
    _e("Gallery columns:")
    php_print("""</span>
    </label>
    </th>
    <td class=\"field\">
    <select id=\"columns\" name=\"columns\">
    <option value=\"1\">1</option>
    <option value=\"2\">2</option>
    <option value=\"3\" selected=\"selected\">3</option>
    <option value=\"4\">4</option>
    <option value=\"5\">5</option>
    <option value=\"6\">6</option>
    <option value=\"7\">7</option>
    <option value=\"8\">8</option>
    <option value=\"9\">9</option>
    </select>
    </td>
    </tr>
    </tbody></table>
    <p class=\"ml-submit\">
    <input type=\"button\" class=\"button\" style=\"display:none;\" onMouseDown=\"wpgallery.update();\" name=\"insert-gallery\" id=\"insert-gallery\" value=\"""")
    esc_attr_e("Insert gallery")
    php_print("\" />\n  <input type=\"button\" class=\"button\" style=\"display:none;\" onMouseDown=\"wpgallery.update();\" name=\"update-gallery\" id=\"update-gallery\" value=\"")
    esc_attr_e("Update gallery settings")
    php_print("""\" />
    </p>
    </div>
    </form>
    """)
# end def media_upload_gallery_form
#// 
#// Outputs the legacy media upload form for the media library.
#// 
#// @since 2.5.0
#// 
#// @global wpdb      $wpdb            WordPress database abstraction object.
#// @global WP_Query  $wp_query        WordPress Query object.
#// @global WP_Locale $wp_locale       WordPress date and time locale object.
#// @global string    $type
#// @global string    $tab
#// @global array     $post_mime_types
#// 
#// @param array $errors
#//
def media_upload_library_form(errors=None, *args_):
    global PHP_REQUEST
    global wpdb,wp_query,wp_locale,type,tab,post_mime_types
    php_check_if_defined("wpdb","wp_query","wp_locale","type","tab","post_mime_types")
    media_upload_header()
    post_id = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    form_action_url = admin_url(str("media-upload.php?type=") + str(type) + str("&tab=library&post_id=") + str(post_id))
    #// This filter is documented in wp-admin/includes/media.php
    form_action_url = apply_filters("media_upload_form_url", form_action_url, type)
    form_class = "media-upload-form validate"
    if get_user_setting("uploader"):
        form_class += " html-uploader"
    # end if
    q = PHP_REQUEST
    q["posts_per_page"] = 10
    q["paged"] = php_intval(q["paged"]) if (php_isset(lambda : q["paged"])) else 0
    if q["paged"] < 1:
        q["paged"] = 1
    # end if
    q["offset"] = q["paged"] - 1 * 10
    if q["offset"] < 1:
        q["offset"] = 0
    # end if
    post_mime_types, avail_post_mime_types = wp_edit_attachments_query(q)
    php_print(" <form id=\"filter\" method=\"get\">\n   <input type=\"hidden\" name=\"type\" value=\"")
    php_print(esc_attr(type))
    php_print("\" />\n  <input type=\"hidden\" name=\"tab\" value=\"")
    php_print(esc_attr(tab))
    php_print("\" />\n  <input type=\"hidden\" name=\"post_id\" value=\"")
    php_print(php_int(post_id))
    php_print("\" />\n  <input type=\"hidden\" name=\"post_mime_type\" value=\"")
    php_print(esc_attr(PHP_REQUEST["post_mime_type"]) if (php_isset(lambda : PHP_REQUEST["post_mime_type"])) else "")
    php_print("\" />\n  <input type=\"hidden\" name=\"context\" value=\"")
    php_print(esc_attr(PHP_REQUEST["context"]) if (php_isset(lambda : PHP_REQUEST["context"])) else "")
    php_print("""\" />
    <p id=\"media-search\" class=\"search-box\">
    <label class=\"screen-reader-text\" for=\"media-search-input\">""")
    _e("Search Media")
    php_print(":</label>\n      <input type=\"search\" id=\"media-search-input\" name=\"s\" value=\"")
    the_search_query()
    php_print("\" />\n      ")
    submit_button(__("Search Media"), "", "", False)
    php_print("""   </p>
    <ul class=\"subsubsub\">
    """)
    type_links = Array()
    _num_posts = wp_count_attachments()
    matches = wp_match_mime_types(php_array_keys(post_mime_types), php_array_keys(_num_posts))
    for _type,reals in matches:
        for real in reals:
            if (php_isset(lambda : num_posts[_type])):
                num_posts[_type] += _num_posts[real]
            else:
                num_posts[_type] = _num_posts[real]
            # end if
        # end for
    # end for
    #// If available type specified by media button clicked, filter by that type.
    if php_empty(lambda : PHP_REQUEST["post_mime_type"]) and (not php_empty(lambda : num_posts[type])):
        PHP_REQUEST["post_mime_type"] = type
        post_mime_types, avail_post_mime_types = wp_edit_attachments_query()
    # end if
    if php_empty(lambda : PHP_REQUEST["post_mime_type"]) or "all" == PHP_REQUEST["post_mime_type"]:
        class_ = " class=\"current\""
    else:
        class_ = ""
    # end if
    type_links[-1] = "<li><a href=\"" + esc_url(add_query_arg(Array({"post_mime_type": "all", "paged": False, "m": False}))) + "\"" + class_ + ">" + __("All Types") + "</a>"
    for mime_type,label in post_mime_types:
        class_ = ""
        if (not wp_match_mime_types(mime_type, avail_post_mime_types)):
            continue
        # end if
        if (php_isset(lambda : PHP_REQUEST["post_mime_type"])) and wp_match_mime_types(mime_type, PHP_REQUEST["post_mime_type"]):
            class_ = " class=\"current\""
        # end if
        type_links[-1] = "<li><a href=\"" + esc_url(add_query_arg(Array({"post_mime_type": mime_type, "paged": False}))) + "\"" + class_ + ">" + php_sprintf(translate_nooped_plural(label[2], num_posts[mime_type]), "<span id=\"" + mime_type + "-counter\">" + number_format_i18n(num_posts[mime_type]) + "</span>") + "</a>"
    # end for
    #// 
    #// Filters the media upload mime type list items.
    #// 
    #// Returned values should begin with an `<li>` tag.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string[] $type_links An array of list items containing mime type link HTML.
    #//
    php_print(php_implode(" | </li>", apply_filters("media_upload_mime_type_links", type_links)) + "</li>")
    type_links = None
    php_print("""   </ul>
    <div class=\"tablenav\">
    """)
    page_links = paginate_links(Array({"base": add_query_arg("paged", "%#%"), "format": "", "prev_text": __("&laquo;"), "next_text": __("&raquo;"), "total": ceil(wp_query.found_posts / 10), "current": q["paged"]}))
    if page_links:
        php_print(str("<div class='tablenav-pages'>") + str(page_links) + str("</div>"))
    # end if
    php_print("\n   <div class=\"alignleft actions\">\n     ")
    arc_query = str("SELECT DISTINCT YEAR(post_date) AS yyear, MONTH(post_date) AS mmonth FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'attachment' ORDER BY post_date DESC")
    arc_result = wpdb.get_results(arc_query)
    month_count = php_count(arc_result)
    selected_month = PHP_REQUEST["m"] if (php_isset(lambda : PHP_REQUEST["m"])) else 0
    if month_count and (not 1 == month_count and 0 == arc_result[0].mmonth):
        php_print("         <select name='m'>\n         <option")
        selected(selected_month, 0)
        php_print(" value='0'>")
        _e("All dates")
        php_print("</option>\n          ")
        for arc_row in arc_result:
            if 0 == arc_row.yyear:
                continue
            # end if
            arc_row.mmonth = zeroise(arc_row.mmonth, 2)
            if arc_row.yyear + arc_row.mmonth == selected_month:
                default = " selected=\"selected\""
            else:
                default = ""
            # end if
            php_print(str("<option") + str(default) + str(" value='") + esc_attr(arc_row.yyear + arc_row.mmonth) + "'>")
            php_print(esc_html(wp_locale.get_month(arc_row.mmonth) + str(" ") + str(arc_row.yyear)))
            php_print("</option>\n")
        # end for
        php_print("         </select>\n     ")
    # end if
    php_print("\n       ")
    submit_button(__("Filter &#187;"), "", "post-query-submit", False)
    php_print("""
    </div>
    <br class=\"clear\" />
    </div>
    </form>
    <form enctype=\"multipart/form-data\" method=\"post\" action=\"""")
    php_print(esc_url(form_action_url))
    php_print("\" class=\"")
    php_print(form_class)
    php_print("\" id=\"library-form\">\n    ")
    wp_nonce_field("media-form")
    php_print(" ")
    pass
    php_print("""
    <script type=\"text/javascript\">
    jQuery(function($){
    var preloaded = $(\".media-item.preloaded\");
if ( preloaded.length > 0 ) {
    preloaded.each(function(){prepareMediaItem({id:this.id.replace(/[^0-9]/g, '')},'');});
    updateMediaForm();
    }
    });
    </script>
    <div id=\"media-items\">
    """)
    add_filter("attachment_fields_to_edit", "media_post_single_attachment_fields_to_edit", 10, 2)
    php_print("     ")
    php_print(get_media_items(None, errors))
    php_print(" </div>\n    <p class=\"ml-submit\">\n       ")
    submit_button(__("Save all changes"), "savebutton", "save", False)
    php_print(" <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id))
    php_print("""\" />
    </p>
    </form>
    """)
# end def media_upload_library_form
#// 
#// Creates the form for external url
#// 
#// @since 2.7.0
#// 
#// @param string $default_view
#// @return string the form html
#//
def wp_media_insert_url_form(default_view="image", *args_):
    
    #// This filter is documented in wp-admin/includes/media.php
    if (not apply_filters("disable_captions", "")):
        caption = """
        <tr class=\"image-only\">
        <th scope=\"row\" class=\"label\">
        <label for=\"caption\"><span class=\"alignleft\">""" + __("Image Caption") + """</span></label>
        </th>
        <td class=\"field\"><textarea id=\"caption\" name=\"caption\"></textarea></td>
        </tr>"""
    else:
        caption = ""
    # end if
    default_align = get_option("image_default_align")
    if php_empty(lambda : default_align):
        default_align = "none"
    # end if
    if "image" == default_view:
        view = "image-only"
        table_class = ""
    else:
        view = "not-image"
        table_class = view
    # end if
    return "\n  <p class=\"media-types\"><label><input type=\"radio\" name=\"media_type\" value=\"image\" id=\"image-only\"" + checked("image-only", view, False) + " /> " + __("Image") + "</label> &nbsp; &nbsp; <label><input type=\"radio\" name=\"media_type\" value=\"generic\" id=\"not-image\"" + checked("not-image", view, False) + " /> " + __("Audio, Video, or Other File") + "</label></p>\n  <p class=\"media-types media-types-required-info\">" + php_sprintf(__("Required fields are marked %s"), "<span class=\"required\">*</span>") + "</p>\n  <table class=\"describe " + table_class + """\"><tbody>
    <tr>
    <th scope=\"row\" class=\"label\" style=\"width:130px;\">
    <label for=\"src\"><span class=\"alignleft\">""" + __("URL") + """</span> <span class=\"required\">*</span></label>
    <span class=\"alignright\" id=\"status_img\"></span>
    </th>
    <td class=\"field\"><input id=\"src\" name=\"src\" value=\"\" type=\"text\" required onblur=\"addExtImage.getImageData()\" /></td>
    </tr>
    <tr>
    <th scope=\"row\" class=\"label\">
    <label for=\"title\"><span class=\"alignleft\">""" + __("Title") + """</span> <span class=\"required\">*</span></label>
    </th>
    <td class=\"field\"><input id=\"title\" name=\"title\" value=\"\" type=\"text\" required /></td>
    </tr>
    <tr class=\"not-image\"><td></td><td><p class=\"help\">""" + __("Link text, e.g. &#8220;Ransom Demands (PDF)&#8221;") + """</p></td></tr>
    <tr class=\"image-only\">
    <th scope=\"row\" class=\"label\">
    <label for=\"alt\"><span class=\"alignleft\">""" + __("Alternative Text") + """</span></label>
    </th>
    <td class=\"field\"><input id=\"alt\" name=\"alt\" value=\"\" type=\"text\" required />
    <p class=\"help\">""" + __("Alt text for the image, e.g. &#8220;The Mona Lisa&#8221;") + "</p></td>\n       </tr>\n     " + caption + "\n       <tr class=\"align image-only\">\n           <th scope=\"row\" class=\"label\"><p><label for=\"align\">" + __("Alignment") + "</label></p></th>\n            <td class=\"field\">\n              <input name=\"align\" id=\"align-none\" value=\"none\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "none" == default_align else "" + " />\n                <label for=\"align-none\" class=\"align image-align-none-label\">" + __("None") + "</label>\n               <input name=\"align\" id=\"align-left\" value=\"left\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "left" == default_align else "" + " />\n                <label for=\"align-left\" class=\"align image-align-left-label\">" + __("Left") + "</label>\n               <input name=\"align\" id=\"align-center\" value=\"center\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "center" == default_align else "" + " />\n              <label for=\"align-center\" class=\"align image-align-center-label\">" + __("Center") + "</label>\n             <input name=\"align\" id=\"align-right\" value=\"right\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "right" == default_align else "" + " />\n             <label for=\"align-right\" class=\"align image-align-right-label\">" + __("Right") + """</label>
    </td>
    </tr>
    <tr class=\"image-only\">
    <th scope=\"row\" class=\"label\">
    <label for=\"url\"><span class=\"alignleft\">""" + __("Link Image To:") + """</span></label>
    </th>
    <td class=\"field\"><input id=\"url\" name=\"url\" value=\"\" type=\"text\" /><br />
    <button type=\"button\" class=\"button\" value=\"\" onclick=\"document.forms[0].url.value=null\">""" + __("None") + "</button>\n            <button type=\"button\" class=\"button\" value=\"\" onclick=\"document.forms[0].url.value=document.forms[0].src.value\">" + __("Link to image") + "</button>\n          <p class=\"help\">" + __("Enter a link URL or click above for presets.") + """</p></td>
    </tr>
    <tr class=\"image-only\">
    <td></td>
    <td>
    <input type=\"button\" class=\"button\" id=\"go_button\" style=\"color:#bbb;\" onclick=\"addExtImage.insert()\" value=\"""" + esc_attr__("Insert into Post") + """\" />
    </td>
    </tr>
    <tr class=\"not-image\">
    <td></td>
    <td>
    """ + get_submit_button(__("Insert into Post"), "", "insertonlybutton", False) + """
    </td>
    </tr>
    </tbody></table>"""
# end def wp_media_insert_url_form
#// 
#// Displays the multi-file uploader message.
#// 
#// @since 2.6.0
#// 
#// @global int $post_ID
#//
def media_upload_flash_bypass(*args_):
    
    browser_uploader = admin_url("media-new.php?browser-uploader")
    post = get_post()
    if post:
        browser_uploader += "&amp;post_id=" + php_intval(post.ID)
    elif (not php_empty(lambda : PHP_GLOBALS["post_ID"])):
        browser_uploader += "&amp;post_id=" + php_intval(PHP_GLOBALS["post_ID"])
    # end if
    php_print(" <p class=\"upload-flash-bypass\">\n ")
    printf(__("You are using the multi-file uploader. Problems? Try the <a href=\"%1$s\" %2$s>browser uploader</a> instead."), browser_uploader, "target=\"_blank\"")
    php_print(" </p>\n  ")
# end def media_upload_flash_bypass
#// 
#// Displays the browser's built-in uploader message.
#// 
#// @since 2.6.0
#//
def media_upload_html_bypass(*args_):
    
    php_print(" <p class=\"upload-html-bypass hide-if-no-js\">\n        ")
    _e("You are using the browser&#8217;s built-in file uploader. The WordPress uploader includes multiple file selection and drag and drop capability. <a href=\"#\">Switch to the multi-file uploader</a>.")
    php_print(" </p>\n  ")
# end def media_upload_html_bypass
#// 
#// Used to display a "After a file has been uploaded..." help message.
#// 
#// @since 3.3.0
#//
def media_upload_text_after(*args_):
    
    pass
# end def media_upload_text_after
#// 
#// Displays the checkbox to scale images.
#// 
#// @since 3.3.0
#//
def media_upload_max_image_resize(*args_):
    
    checked = " checked=\"true\"" if get_user_setting("upload_resize") else ""
    a = ""
    end_ = ""
    if current_user_can("manage_options"):
        a = "<a href=\"" + esc_url(admin_url("options-media.php")) + "\" target=\"_blank\">"
        end_ = "</a>"
    # end if
    php_print(" <p class=\"hide-if-no-js\"><label>\n    <input name=\"image_resize\" type=\"checkbox\" id=\"image_resize\" value=\"true\"")
    php_print(checked)
    php_print(" />\n    ")
    #// translators: 1: Link start tag, 2: Link end tag, 3: Width, 4: Height.
    printf(__("Scale images to match the large size selected in %1$simage options%2$s (%3$d &times; %4$d)."), a, end_, php_int(get_option("large_size_w", "1024")), php_int(get_option("large_size_h", "1024")))
    php_print(" </label></p>\n  ")
# end def media_upload_max_image_resize
#// 
#// Displays the out of storage quota message in Multisite.
#// 
#// @since 3.5.0
#//
def multisite_over_quota_message(*args_):
    
    php_print("<p>" + php_sprintf(__("Sorry, you have used your space allocation of %s. Please delete some files to upload more files."), size_format(get_space_allowed() * MB_IN_BYTES)) + "</p>")
# end def multisite_over_quota_message
#// 
#// Displays the image and editor in the post editor
#// 
#// @since 3.5.0
#// 
#// @param WP_Post $post A post object.
#//
def edit_form_image_editor(post=None, *args_):
    
    open_ = (php_isset(lambda : PHP_REQUEST["image-editor"]))
    if open_:
        php_include_file(ABSPATH + "wp-admin/includes/image-edit.php", once=True)
    # end if
    thumb_url = False
    attachment_id = php_intval(post.ID)
    if attachment_id:
        thumb_url = wp_get_attachment_image_src(attachment_id, Array(900, 450), True)
    # end if
    alt_text = get_post_meta(post.ID, "_wp_attachment_image_alt", True)
    att_url = wp_get_attachment_url(post.ID)
    php_print(" <div class=\"wp_attachment_holder wp-clearfix\">\n  ")
    if wp_attachment_is_image(post.ID):
        image_edit_button = ""
        if wp_image_editor_supports(Array({"mime_type": post.post_mime_type})):
            nonce = wp_create_nonce(str("image_editor-") + str(post.ID))
            image_edit_button = str("<input type='button' id='imgedit-open-btn-") + str(post.ID) + str("' onclick='imageEdit.open( ") + str(post.ID) + str(", \"") + str(nonce) + str("\" )' class='button' value='") + esc_attr__("Edit Image") + "' /> <span class='spinner'></span>"
        # end if
        open_style = ""
        not_open_style = ""
        if open_:
            open_style = " style=\"display:none\""
        else:
            not_open_style = " style=\"display:none\""
        # end if
        php_print("     <div class=\"imgedit-response\" id=\"imgedit-response-")
        php_print(attachment_id)
        php_print("\"></div>\n\n        <div")
        php_print(open_style)
        php_print(" class=\"wp_attachment_image wp-clearfix\" id=\"media-head-")
        php_print(attachment_id)
        php_print("\">\n            <p id=\"thumbnail-head-")
        php_print(attachment_id)
        php_print("\"><img class=\"thumbnail\" src=\"")
        php_print(set_url_scheme(thumb_url[0]))
        php_print("\" style=\"max-width:100%\" alt=\"\" /></p>\n            <p>")
        php_print(image_edit_button)
        php_print("</p>\n       </div>\n        <div")
        php_print(not_open_style)
        php_print(" class=\"image-editor\" id=\"image-editor-")
        php_print(attachment_id)
        php_print("\">\n        ")
        if open_:
            wp_image_editor(attachment_id)
        # end if
        php_print("     </div>\n        ")
    elif attachment_id and wp_attachment_is("audio", post):
        wp_maybe_generate_attachment_metadata(post)
        php_print(wp_audio_shortcode(Array({"src": att_url})))
    elif attachment_id and wp_attachment_is("video", post):
        wp_maybe_generate_attachment_metadata(post)
        meta = wp_get_attachment_metadata(attachment_id)
        w = php_min(meta["width"], 640) if (not php_empty(lambda : meta["width"])) else 0
        h = meta["height"] if (not php_empty(lambda : meta["height"])) else 0
        if h and w < meta["width"]:
            h = round(meta["height"] * w / meta["width"])
        # end if
        attr = Array({"src": att_url})
        if (not php_empty(lambda : w)) and (not php_empty(lambda : h)):
            attr["width"] = w
            attr["height"] = h
        # end if
        thumb_id = get_post_thumbnail_id(attachment_id)
        if (not php_empty(lambda : thumb_id)):
            attr["poster"] = wp_get_attachment_url(thumb_id)
        # end if
        php_print(wp_video_shortcode(attr))
    elif (php_isset(lambda : thumb_url[0])):
        php_print("     <div class=\"wp_attachment_image wp-clearfix\" id=\"media-head-")
        php_print(attachment_id)
        php_print("\">\n            <p id=\"thumbnail-head-")
        php_print(attachment_id)
        php_print("\">\n                <img class=\"thumbnail\" src=\"")
        php_print(set_url_scheme(thumb_url[0]))
        php_print("""\" style=\"max-width:100%\" alt=\"\" />
        </p>
        </div>
        """)
    else:
        #// 
        #// Fires when an attachment type can't be rendered in the edit form.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Post $post A post object.
        #//
        do_action("wp_edit_form_attachment_display", post)
    # end if
    php_print(" </div>\n    <div class=\"wp_attachment_details edit-form-section\">\n   ")
    if "image" == php_substr(post.post_mime_type, 0, 5):
        php_print("     <p class=\"attachment-alt-text\">\n         <label for=\"attachment_alt\"><strong>")
        _e("Alternative Text")
        php_print("</strong></label><br />\n            <input type=\"text\" class=\"widefat\" name=\"_wp_attachment_image_alt\" id=\"attachment_alt\" aria-describedby=\"alt-text-description\" value=\"")
        php_print(esc_attr(alt_text))
        php_print("""\" />
        </p>
        <p class=\"attachment-alt-text-description\" id=\"alt-text-description\">
        """)
        printf(__("<a href=\"%1$s\" %2$s>Describe the purpose of the image%3$s</a>. Leave empty if the image is purely decorative."), esc_url("https://www.w3.org/WAI/tutorials/images/decision-tree"), "target=\"_blank\" rel=\"noopener noreferrer\"", php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)")))
        php_print("     </p>\n  ")
    # end if
    php_print("\n       <p>\n           <label for=\"attachment_caption\"><strong>")
    _e("Caption")
    php_print("</strong></label><br />\n            <textarea class=\"widefat\" name=\"excerpt\" id=\"attachment_caption\">")
    php_print(post.post_excerpt)
    php_print("""</textarea>
    </p>
    """)
    quicktags_settings = Array({"buttons": "strong,em,link,block,del,ins,img,ul,ol,li,code,close"})
    editor_args = Array({"textarea_name": "content", "textarea_rows": 5, "media_buttons": False, "tinymce": False, "quicktags": quicktags_settings})
    php_print("\n   <label for=\"attachment_content\" class=\"attachment-content-description\"><strong>")
    _e("Description")
    php_print("</strong>\n  ")
    if php_preg_match("#^(audio|video)/#", post.post_mime_type):
        php_print(": " + __("Displayed on attachment pages."))
    # end if
    php_print(" </label>\n  ")
    wp_editor(post.post_content, "attachment_content", editor_args)
    php_print("\n   </div>\n    ")
    extras = get_compat_media_markup(post.ID)
    php_print(extras["item"])
    php_print("<input type=\"hidden\" id=\"image-edit-context\" value=\"edit-attachment\" />" + "\n")
# end def edit_form_image_editor
#// 
#// Displays non-editable attachment metadata in the publish meta box.
#// 
#// @since 3.5.0
#//
def attachment_submitbox_metadata(*args_):
    
    post = get_post()
    attachment_id = post.ID
    file = get_attached_file(attachment_id)
    filename = esc_html(wp_basename(file))
    media_dims = ""
    meta = wp_get_attachment_metadata(attachment_id)
    if (php_isset(lambda : meta["width"]) and php_isset(lambda : meta["height"])):
        media_dims += str("<span id='media-dims-") + str(attachment_id) + str("'>") + str(meta["width"]) + str("&nbsp;&times;&nbsp;") + str(meta["height"]) + str("</span> ")
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    media_dims = apply_filters("media_meta", media_dims, post)
    att_url = wp_get_attachment_url(attachment_id)
    php_print(" <div class=\"misc-pub-section misc-pub-attachment\">\n      <label for=\"attachment_url\">")
    _e("File URL:")
    php_print("</label>\n       <input type=\"text\" class=\"widefat urlfield\" readonly=\"readonly\" name=\"attachment_url\" id=\"attachment_url\" value=\"")
    php_print(esc_attr(att_url))
    php_print("""\" />
    </div>
    <div class=\"misc-pub-section misc-pub-filename\">
    """)
    _e("File name:")
    php_print(" <strong>")
    php_print(filename)
    php_print("""</strong>
    </div>
    <div class=\"misc-pub-section misc-pub-filetype\">
    """)
    _e("File type:")
    php_print("     <strong>\n      ")
    if php_preg_match("/^.*?\\.(\\w+)$/", get_attached_file(post.ID), matches):
        php_print(esc_html(php_strtoupper(matches[1])))
        mime_type = php_explode("/", post.post_mime_type)
        if "image" != mime_type and (not php_empty(lambda : meta["mime_type"])):
            if str(mime_type) + str("/") + php_strtolower(matches[1]) != meta["mime_type"]:
                php_print(" (" + meta["mime_type"] + ")")
            # end if
        # end if
    else:
        php_print(php_strtoupper(php_str_replace("image/", "", post.post_mime_type)))
    # end if
    php_print("""       </strong>
    </div>
    """)
    file_size = False
    if (php_isset(lambda : meta["filesize"])):
        file_size = meta["filesize"]
    elif php_file_exists(file):
        file_size = filesize(file)
    # end if
    if (not php_empty(lambda : file_size)):
        php_print("     <div class=\"misc-pub-section misc-pub-filesize\">\n            ")
        _e("File size:")
        php_print(" <strong>")
        php_print(size_format(file_size))
        php_print("</strong>\n      </div>\n        ")
    # end if
    if php_preg_match("#^(audio|video)/#", post.post_mime_type):
        fields = Array({"length_formatted": __("Length:"), "bitrate": __("Bitrate:")})
        #// 
        #// Filters the audio and video metadata fields to be shown in the publish meta box.
        #// 
        #// The key for each item in the array should correspond to an attachment
        #// metadata key, and the value should be the desired label.
        #// 
        #// @since 3.7.0
        #// @since 4.9.0 Added the `$post` parameter.
        #// 
        #// @param array   $fields An array of the attachment metadata keys and labels.
        #// @param WP_Post $post   WP_Post object for the current attachment.
        #//
        fields = apply_filters("media_submitbox_misc_sections", fields, post)
        for key,label in fields:
            if php_empty(lambda : meta[key]):
                continue
            # end if
            php_print("         <div class=\"misc-pub-section misc-pub-mime-meta misc-pub-")
            php_print(sanitize_html_class(key))
            php_print("\">\n                ")
            php_print(label)
            php_print("             <strong>\n              ")
            for case in Switch(key):
                if case("bitrate"):
                    php_print(round(meta["bitrate"] / 1000) + "kb/s")
                    if (not php_empty(lambda : meta["bitrate_mode"])):
                        php_print(" " + php_strtoupper(esc_html(meta["bitrate_mode"])))
                    # end if
                    break
                # end if
                if case():
                    php_print(esc_html(meta[key]))
                    break
                # end if
            # end for
            php_print("             </strong>\n         </div>\n            ")
        # end for
        fields = Array({"dataformat": __("Audio Format:"), "codec": __("Audio Codec:")})
        #// 
        #// Filters the audio attachment metadata fields to be shown in the publish meta box.
        #// 
        #// The key for each item in the array should correspond to an attachment
        #// metadata key, and the value should be the desired label.
        #// 
        #// @since 3.7.0
        #// @since 4.9.0 Added the `$post` parameter.
        #// 
        #// @param array   $fields An array of the attachment metadata keys and labels.
        #// @param WP_Post $post   WP_Post object for the current attachment.
        #//
        audio_fields = apply_filters("audio_submitbox_misc_sections", fields, post)
        for key,label in audio_fields:
            if php_empty(lambda : meta["audio"][key]):
                continue
            # end if
            php_print("         <div class=\"misc-pub-section misc-pub-audio misc-pub-")
            php_print(sanitize_html_class(key))
            php_print("\">\n                ")
            php_print(label)
            php_print(" <strong>")
            php_print(esc_html(meta["audio"][key]))
            php_print("</strong>\n          </div>\n            ")
        # end for
    # end if
    if media_dims:
        php_print("     <div class=\"misc-pub-section misc-pub-dimensions\">\n          ")
        _e("Dimensions:")
        php_print(" <strong>")
        php_print(media_dims)
        php_print("</strong>\n      </div>\n        ")
    # end if
    if (not php_empty(lambda : meta["original_image"])):
        php_print("     <div class=\"misc-pub-section misc-pub-original-image\">\n          ")
        _e("Original image:")
        php_print("         <a href=\"")
        php_print(esc_url(wp_get_original_image_url(attachment_id)))
        php_print("\">\n                ")
        php_print(esc_html(wp_basename(wp_get_original_image_path(attachment_id))))
        php_print("         </a>\n      </div>\n        ")
    # end if
# end def attachment_submitbox_metadata
#// 
#// Parse ID3v2, ID3v1, and getID3 comments to extract usable data
#// 
#// @since 3.6.0
#// 
#// @param array $metadata An existing array with data
#// @param array $data Data supplied by ID3 tags
#//
def wp_add_id3_tag_data(metadata=None, data=None, *args_):
    
    for version in Array("id3v2", "id3v1"):
        if (not php_empty(lambda : data[version]["comments"])):
            for key,list in data[version]["comments"]:
                if "length" != key and (not php_empty(lambda : list)):
                    metadata[key] = wp_kses_post(reset(list))
                    #// Fix bug in byte stream analysis.
                    if "terms_of_use" == key and 0 == php_strpos(metadata[key], "yright notice."):
                        metadata[key] = "Cop" + metadata[key]
                    # end if
                # end if
            # end for
            break
        # end if
    # end for
    if (not php_empty(lambda : data["id3v2"]["APIC"])):
        image = reset(data["id3v2"]["APIC"])
        if (not php_empty(lambda : image["data"])):
            metadata["image"] = Array({"data": image["data"], "mime": image["image_mime"], "width": image["image_width"], "height": image["image_height"]})
        # end if
    elif (not php_empty(lambda : data["comments"]["picture"])):
        image = reset(data["comments"]["picture"])
        if (not php_empty(lambda : image["data"])):
            metadata["image"] = Array({"data": image["data"], "mime": image["image_mime"]})
        # end if
    # end if
# end def wp_add_id3_tag_data
#// 
#// Retrieve metadata from a video file's ID3 tags
#// 
#// @since 3.6.0
#// 
#// @param string $file Path to file.
#// @return array|bool Returns array of metadata, if found.
#//
def wp_read_video_metadata(file=None, *args_):
    
    if (not php_file_exists(file)):
        return False
    # end if
    metadata = Array()
    if (not php_defined("GETID3_TEMP_DIR")):
        php_define("GETID3_TEMP_DIR", get_temp_dir())
    # end if
    if (not php_class_exists("getID3", False)):
        php_include_file(ABSPATH + WPINC + "/ID3/getid3.php", once=False)
    # end if
    id3 = php_new_class("getID3", lambda : getID3())
    data = id3.analyze(file)
    if (php_isset(lambda : data["video"]["lossless"])):
        metadata["lossless"] = data["video"]["lossless"]
    # end if
    if (not php_empty(lambda : data["video"]["bitrate"])):
        metadata["bitrate"] = php_int(data["video"]["bitrate"])
    # end if
    if (not php_empty(lambda : data["video"]["bitrate_mode"])):
        metadata["bitrate_mode"] = data["video"]["bitrate_mode"]
    # end if
    if (not php_empty(lambda : data["filesize"])):
        metadata["filesize"] = php_int(data["filesize"])
    # end if
    if (not php_empty(lambda : data["mime_type"])):
        metadata["mime_type"] = data["mime_type"]
    # end if
    if (not php_empty(lambda : data["playtime_seconds"])):
        metadata["length"] = php_int(round(data["playtime_seconds"]))
    # end if
    if (not php_empty(lambda : data["playtime_string"])):
        metadata["length_formatted"] = data["playtime_string"]
    # end if
    if (not php_empty(lambda : data["video"]["resolution_x"])):
        metadata["width"] = php_int(data["video"]["resolution_x"])
    # end if
    if (not php_empty(lambda : data["video"]["resolution_y"])):
        metadata["height"] = php_int(data["video"]["resolution_y"])
    # end if
    if (not php_empty(lambda : data["fileformat"])):
        metadata["fileformat"] = data["fileformat"]
    # end if
    if (not php_empty(lambda : data["video"]["dataformat"])):
        metadata["dataformat"] = data["video"]["dataformat"]
    # end if
    if (not php_empty(lambda : data["video"]["encoder"])):
        metadata["encoder"] = data["video"]["encoder"]
    # end if
    if (not php_empty(lambda : data["video"]["codec"])):
        metadata["codec"] = data["video"]["codec"]
    # end if
    if (not php_empty(lambda : data["audio"])):
        data["audio"]["streams"] = None
        metadata["audio"] = data["audio"]
    # end if
    if php_empty(lambda : metadata["created_timestamp"]):
        created_timestamp = wp_get_media_creation_timestamp(data)
        if False != created_timestamp:
            metadata["created_timestamp"] = created_timestamp
        # end if
    # end if
    wp_add_id3_tag_data(metadata, data)
    file_format = metadata["fileformat"] if (php_isset(lambda : metadata["fileformat"])) else None
    #// 
    #// Filters the array of metadata retrieved from a video.
    #// 
    #// In core, usually this selection is what is stored.
    #// More complete data can be parsed from the `$data` parameter.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array  $metadata       Filtered Video metadata.
    #// @param string $file           Path to video file.
    #// @param string $file_format    File format of video, as analyzed by getID3.
    #// @param string $data           Raw metadata from getID3.
    #//
    return apply_filters("wp_read_video_metadata", metadata, file, file_format, data)
# end def wp_read_video_metadata
#// 
#// Retrieve metadata from an audio file's ID3 tags.
#// 
#// @since 3.6.0
#// 
#// @param string $file Path to file.
#// @return array|bool Returns array of metadata, if found.
#//
def wp_read_audio_metadata(file=None, *args_):
    
    if (not php_file_exists(file)):
        return False
    # end if
    metadata = Array()
    if (not php_defined("GETID3_TEMP_DIR")):
        php_define("GETID3_TEMP_DIR", get_temp_dir())
    # end if
    if (not php_class_exists("getID3", False)):
        php_include_file(ABSPATH + WPINC + "/ID3/getid3.php", once=False)
    # end if
    id3 = php_new_class("getID3", lambda : getID3())
    data = id3.analyze(file)
    if (not php_empty(lambda : data["audio"])):
        data["audio"]["streams"] = None
        metadata = data["audio"]
    # end if
    if (not php_empty(lambda : data["fileformat"])):
        metadata["fileformat"] = data["fileformat"]
    # end if
    if (not php_empty(lambda : data["filesize"])):
        metadata["filesize"] = php_int(data["filesize"])
    # end if
    if (not php_empty(lambda : data["mime_type"])):
        metadata["mime_type"] = data["mime_type"]
    # end if
    if (not php_empty(lambda : data["playtime_seconds"])):
        metadata["length"] = php_int(round(data["playtime_seconds"]))
    # end if
    if (not php_empty(lambda : data["playtime_string"])):
        metadata["length_formatted"] = data["playtime_string"]
    # end if
    if php_empty(lambda : metadata["created_timestamp"]):
        created_timestamp = wp_get_media_creation_timestamp(data)
        if False != created_timestamp:
            metadata["created_timestamp"] = created_timestamp
        # end if
    # end if
    wp_add_id3_tag_data(metadata, data)
    return metadata
# end def wp_read_audio_metadata
#// 
#// Parse creation date from media metadata.
#// 
#// The getID3 library doesn't have a standard method for getting creation dates,
#// so the location of this data can vary based on the MIME type.
#// 
#// @since 4.9.0
#// 
#// @link https://github.com/JamesHeinrich/getID3/blob/master/structure.txt
#// 
#// @param array $metadata The metadata returned by getID3::analyze().
#// @return int|bool A UNIX timestamp for the media's creation date if available
#// or a boolean FALSE if a timestamp could not be determined.
#//
def wp_get_media_creation_timestamp(metadata=None, *args_):
    
    creation_date = False
    if php_empty(lambda : metadata["fileformat"]):
        return creation_date
    # end if
    for case in Switch(metadata["fileformat"]):
        if case("asf"):
            if (php_isset(lambda : metadata["asf"]["file_properties_object"]["creation_date_unix"])):
                creation_date = php_int(metadata["asf"]["file_properties_object"]["creation_date_unix"])
            # end if
            break
        # end if
        if case("matroska"):
            pass
        # end if
        if case("webm"):
            if (php_isset(lambda : metadata["matroska"]["comments"]["creation_time"]["0"])):
                creation_date = strtotime(metadata["matroska"]["comments"]["creation_time"]["0"])
            elif (php_isset(lambda : metadata["matroska"]["info"]["0"]["DateUTC_unix"])):
                creation_date = php_int(metadata["matroska"]["info"]["0"]["DateUTC_unix"])
            # end if
            break
        # end if
        if case("quicktime"):
            pass
        # end if
        if case("mp4"):
            if (php_isset(lambda : metadata["quicktime"]["moov"]["subatoms"]["0"]["creation_time_unix"])):
                creation_date = php_int(metadata["quicktime"]["moov"]["subatoms"]["0"]["creation_time_unix"])
            # end if
            break
        # end if
    # end for
    return creation_date
# end def wp_get_media_creation_timestamp
#// 
#// Encapsulate logic for Attach/Detach actions
#// 
#// @since 4.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $parent_id Attachment parent ID.
#// @param string $action    Optional. Attach/detach action. Accepts 'attach' or 'detach'.
#// Default 'attach'.
#//
def wp_media_attach_action(parent_id=None, action="attach", *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not parent_id):
        return
    # end if
    if (not current_user_can("edit_post", parent_id)):
        wp_die(__("Sorry, you are not allowed to edit this post."))
    # end if
    ids = Array()
    for att_id in PHP_REQUEST["media"]:
        att_id = php_int(att_id)
        if (not current_user_can("edit_post", att_id)):
            continue
        # end if
        ids[-1] = att_id
    # end for
    if (not php_empty(lambda : ids)):
        ids_string = php_implode(",", ids)
        if "attach" == action:
            result = wpdb.query(wpdb.prepare(str("UPDATE ") + str(wpdb.posts) + str(" SET post_parent = %d WHERE post_type = 'attachment' AND ID IN ( ") + str(ids_string) + str(" )"), parent_id))
        else:
            result = wpdb.query(str("UPDATE ") + str(wpdb.posts) + str(" SET post_parent = 0 WHERE post_type = 'attachment' AND ID IN ( ") + str(ids_string) + str(" )"))
        # end if
        for att_id in ids:
            clean_attachment_cache(att_id)
        # end for
    # end if
    if (php_isset(lambda : result)):
        location = "upload.php"
        referer = wp_get_referer()
        if referer:
            if False != php_strpos(referer, "upload.php"):
                location = remove_query_arg(Array("attached", "detach"), referer)
            # end if
        # end if
        key = "attached" if "attach" == action else "detach"
        location = add_query_arg(Array({key: result}), location)
        wp_redirect(location)
        php_exit(0)
    # end if
# end def wp_media_attach_action
