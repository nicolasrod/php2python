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
def media_upload_tabs(*_args_):
    
    
    _default_tabs_ = Array({"type": __("From Computer"), "type_url": __("From URL"), "gallery": __("Gallery"), "library": __("Media Library")})
    #// 
    #// Filters the available tabs in the legacy (pre-3.5.0) media popup.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string[] $_default_tabs An array of media tabs.
    #//
    return apply_filters("media_upload_tabs", _default_tabs_)
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
def update_gallery_tab(tabs_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not (php_isset(lambda : PHP_REQUEST["post_id"]))):
        tabs_["gallery"] = None
        return tabs_
    # end if
    post_id_ = php_intval(PHP_REQUEST["post_id"])
    if post_id_:
        attachments_ = php_intval(wpdb_.get_var(wpdb_.prepare(str("SELECT count(*) FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'attachment' AND post_status != 'trash' AND post_parent = %d"), post_id_)))
    # end if
    if php_empty(lambda : attachments_):
        tabs_["gallery"] = None
        return tabs_
    # end if
    #// translators: %s: Number of attachments.
    tabs_["gallery"] = php_sprintf(__("Gallery (%s)"), str("<span id='attachments-count'>") + str(attachments_) + str("</span>"))
    return tabs_
# end def update_gallery_tab
#// 
#// Outputs the legacy media upload tabs UI.
#// 
#// @since 2.5.0
#// 
#// @global string $redir_tab
#//
def the_media_upload_tabs(*_args_):
    
    
    global redir_tab_
    php_check_if_defined("redir_tab_")
    tabs_ = media_upload_tabs()
    default_ = "type"
    if (not php_empty(lambda : tabs_)):
        php_print("<ul id='sidemenu'>\n")
        if (php_isset(lambda : redir_tab_)) and php_array_key_exists(redir_tab_, tabs_):
            current_ = redir_tab_
        elif (php_isset(lambda : PHP_REQUEST["tab"])) and php_array_key_exists(PHP_REQUEST["tab"], tabs_):
            current_ = PHP_REQUEST["tab"]
        else:
            #// This filter is documented in wp-admin/media-upload.php
            current_ = apply_filters("media_upload_default_tab", default_)
        # end if
        for callback_,text_ in tabs_.items():
            class_ = ""
            if current_ == callback_:
                class_ = " class='current'"
            # end if
            href_ = add_query_arg(Array({"tab": callback_, "s": False, "paged": False, "post_mime_type": False, "m": False}))
            link_ = "<a href='" + esc_url(href_) + str("'") + str(class_) + str(">") + str(text_) + str("</a>")
            php_print(" <li id='" + esc_attr(str("tab-") + str(callback_)) + str("'>") + str(link_) + str("</li>\n"))
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
def get_image_send_to_editor(id_=None, caption_=None, title_=None, align_=None, url_="", rel_=None, size_="medium", alt_="", *_args_):
    if rel_ is None:
        rel_ = False
    # end if
    
    html_ = get_image_tag(id_, alt_, "", align_, size_)
    if rel_:
        if php_is_string(rel_):
            rel_ = " rel=\"" + esc_attr(rel_) + "\""
        else:
            rel_ = " rel=\"attachment wp-att-" + php_intval(id_) + "\""
        # end if
    else:
        rel_ = ""
    # end if
    if url_:
        html_ = "<a href=\"" + esc_attr(url_) + "\"" + rel_ + ">" + html_ + "</a>"
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
    html_ = apply_filters("image_send_to_editor", html_, id_, caption_, title_, align_, url_, size_, alt_)
    return html_
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
def image_add_caption(html_=None, id_=None, caption_=None, title_=None, align_=None, url_=None, size_=None, alt_="", *_args_):
    
    
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
    caption_ = apply_filters("image_add_caption_text", caption_, id_)
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
    if php_empty(lambda : caption_) or apply_filters("disable_captions", ""):
        return html_
    # end if
    id_ = "attachment_" + id_ if 0 < php_int(id_) else ""
    if (not php_preg_match("/width=[\"']([0-9]+)/", html_, matches_)):
        return html_
    # end if
    width_ = matches_[1]
    caption_ = php_str_replace(Array("\r\n", "\r"), "\n", caption_)
    caption_ = preg_replace_callback("/<[a-zA-Z0-9]+(?: [^<>]+>)*/", "_cleanup_image_add_caption", caption_)
    #// Convert any remaining line breaks to <br />.
    caption_ = php_preg_replace("/[ \\n\\t]*\\n[ \\t]*/", "<br />", caption_)
    html_ = php_preg_replace("/(class=[\"'][^'\"]*)align(none|left|right|center)\\s?/", "$1", html_)
    if php_empty(lambda : align_):
        align_ = "none"
    # end if
    shcode_ = "[caption id=\"" + id_ + "\" align=\"align" + align_ + "\" width=\"" + width_ + "\"]" + html_ + " " + caption_ + "[/caption]"
    #// 
    #// Filters the image HTML markup including the caption shortcode.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $shcode The image HTML markup with caption shortcode.
    #// @param string $html   The image HTML markup.
    #//
    return apply_filters("image_add_caption_shortcode", shcode_, html_)
# end def image_add_caption
#// 
#// Private preg_replace callback used in image_add_caption()
#// 
#// @access private
#// @since 3.4.0
#//
def _cleanup_image_add_caption(matches_=None, *_args_):
    
    
    #// Remove any line breaks from inside the tags.
    return php_preg_replace("/[\\r\\n\\t]+/", " ", matches_[0])
# end def _cleanup_image_add_caption
#// 
#// Adds image html to editor
#// 
#// @since 2.5.0
#// 
#// @param string $html
#//
def media_send_to_editor(html_=None, *_args_):
    
    
    php_print(" <script type=\"text/javascript\">\n var win = window.dialogArguments || opener || parent || top;\n  win.send_to_editor( ")
    php_print(wp_json_encode(html_))
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
def media_handle_upload(file_id_=None, post_id_=None, post_data_=None, overrides_=None, *_args_):
    if post_data_ is None:
        post_data_ = Array()
    # end if
    if overrides_ is None:
        overrides_ = Array({"test_form": False})
    # end if
    
    time_ = current_time("mysql")
    post_ = get_post(post_id_)
    if post_:
        #// The post date doesn't usually matter for pages, so don't backdate this upload.
        if "page" != post_.post_type and php_substr(post_.post_date, 0, 4) > 0:
            time_ = post_.post_date
        # end if
    # end if
    file_ = wp_handle_upload(PHP_FILES[file_id_], overrides_, time_)
    if (php_isset(lambda : file_["error"])):
        return php_new_class("WP_Error", lambda : WP_Error("upload_error", file_["error"]))
    # end if
    name_ = PHP_FILES[file_id_]["name"]
    ext_ = pathinfo(name_, PATHINFO_EXTENSION)
    name_ = wp_basename(name_, str(".") + str(ext_))
    url_ = file_["url"]
    type_ = file_["type"]
    file_ = file_["file"]
    title_ = sanitize_text_field(name_)
    content_ = ""
    excerpt_ = ""
    if php_preg_match("#^audio#", type_):
        meta_ = wp_read_audio_metadata(file_)
        if (not php_empty(lambda : meta_["title"])):
            title_ = meta_["title"]
        # end if
        if (not php_empty(lambda : title_)):
            if (not php_empty(lambda : meta_["album"])) and (not php_empty(lambda : meta_["artist"])):
                #// translators: 1: Audio track title, 2: Album title, 3: Artist name.
                content_ += php_sprintf(__("\"%1$s\" from %2$s by %3$s."), title_, meta_["album"], meta_["artist"])
            elif (not php_empty(lambda : meta_["album"])):
                #// translators: 1: Audio track title, 2: Album title.
                content_ += php_sprintf(__("\"%1$s\" from %2$s."), title_, meta_["album"])
            elif (not php_empty(lambda : meta_["artist"])):
                #// translators: 1: Audio track title, 2: Artist name.
                content_ += php_sprintf(__("\"%1$s\" by %2$s."), title_, meta_["artist"])
            else:
                #// translators: %s: Audio track title.
                content_ += php_sprintf(__("\"%s\"."), title_)
            # end if
        elif (not php_empty(lambda : meta_["album"])):
            if (not php_empty(lambda : meta_["artist"])):
                #// translators: 1: Audio album title, 2: Artist name.
                content_ += php_sprintf(__("%1$s by %2$s."), meta_["album"], meta_["artist"])
            else:
                content_ += meta_["album"] + "."
            # end if
        elif (not php_empty(lambda : meta_["artist"])):
            content_ += meta_["artist"] + "."
        # end if
        if (not php_empty(lambda : meta_["year"])):
            #// translators: Audio file track information. %d: Year of audio track release.
            content_ += " " + php_sprintf(__("Released: %d."), meta_["year"])
        # end if
        if (not php_empty(lambda : meta_["track_number"])):
            track_number_ = php_explode("/", meta_["track_number"])
            if (php_isset(lambda : track_number_[1])):
                #// translators: Audio file track information. 1: Audio track number, 2: Total audio tracks.
                content_ += " " + php_sprintf(__("Track %1$s of %2$s."), number_format_i18n(track_number_[0]), number_format_i18n(track_number_[1]))
            else:
                #// translators: Audio file track information. %s: Audio track number.
                content_ += " " + php_sprintf(__("Track %s."), number_format_i18n(track_number_[0]))
            # end if
        # end if
        if (not php_empty(lambda : meta_["genre"])):
            #// translators: Audio file genre information. %s: Audio genre name.
            content_ += " " + php_sprintf(__("Genre: %s."), meta_["genre"])
        # end if
        pass
    elif 0 == php_strpos(type_, "image/"):
        image_meta_ = wp_read_image_metadata(file_)
        if image_meta_:
            if php_trim(image_meta_["title"]) and (not php_is_numeric(sanitize_title(image_meta_["title"]))):
                title_ = image_meta_["title"]
            # end if
            if php_trim(image_meta_["caption"]):
                excerpt_ = image_meta_["caption"]
            # end if
        # end if
    # end if
    #// Construct the attachment array.
    attachment_ = php_array_merge(Array({"post_mime_type": type_, "guid": url_, "post_parent": post_id_, "post_title": title_, "post_content": content_, "post_excerpt": excerpt_}), post_data_)
    attachment_["ID"] = None
    #// Save the data.
    attachment_id_ = wp_insert_attachment(attachment_, file_, post_id_, True)
    if (not is_wp_error(attachment_id_)):
        #// Set a custom header with the attachment_id.
        #// Used by the browser/client to resume creating image sub-sizes after a PHP fatal error.
        if (not php_headers_sent()):
            php_header("X-WP-Upload-Attachment-ID: " + attachment_id_)
        # end if
        #// The image sub-sizes are created during wp_generate_attachment_metadata().
        #// This is generally slow and may cause timeouts or out of memory errors.
        wp_update_attachment_metadata(attachment_id_, wp_generate_attachment_metadata(attachment_id_, file_))
    # end if
    return attachment_id_
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
def media_handle_sideload(file_array_=None, post_id_=0, desc_=None, post_data_=None, *_args_):
    if desc_ is None:
        desc_ = None
    # end if
    if post_data_ is None:
        post_data_ = Array()
    # end if
    
    overrides_ = Array({"test_form": False})
    time_ = current_time("mysql")
    post_ = get_post(post_id_)
    if post_:
        if php_substr(post_.post_date, 0, 4) > 0:
            time_ = post_.post_date
        # end if
    # end if
    file_ = wp_handle_sideload(file_array_, overrides_, time_)
    if (php_isset(lambda : file_["error"])):
        return php_new_class("WP_Error", lambda : WP_Error("upload_error", file_["error"]))
    # end if
    url_ = file_["url"]
    type_ = file_["type"]
    file_ = file_["file"]
    title_ = php_preg_replace("/\\.[^.]+$/", "", wp_basename(file_))
    content_ = ""
    #// Use image exif/iptc data for title and caption defaults if possible.
    image_meta_ = wp_read_image_metadata(file_)
    if image_meta_:
        if php_trim(image_meta_["title"]) and (not php_is_numeric(sanitize_title(image_meta_["title"]))):
            title_ = image_meta_["title"]
        # end if
        if php_trim(image_meta_["caption"]):
            content_ = image_meta_["caption"]
        # end if
    # end if
    if (php_isset(lambda : desc_)):
        title_ = desc_
    # end if
    #// Construct the attachment array.
    attachment_ = php_array_merge(Array({"post_mime_type": type_, "guid": url_, "post_parent": post_id_, "post_title": title_, "post_content": content_}), post_data_)
    attachment_["ID"] = None
    #// Save the attachment metadata.
    attachment_id_ = wp_insert_attachment(attachment_, file_, post_id_, True)
    if (not is_wp_error(attachment_id_)):
        wp_update_attachment_metadata(attachment_id_, wp_generate_attachment_metadata(attachment_id_, file_))
    # end if
    return attachment_id_
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
def wp_iframe(content_func_=None, *args_):
    
    
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
    if php_is_array(content_func_) and (not php_empty(lambda : content_func_[1])) and 0 == php_strpos(php_str(content_func_[1]), "media") or (not php_is_array(content_func_)) and 0 == php_strpos(content_func_, "media"):
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
    if php_is_string(content_func_):
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
        do_action(str("admin_head_") + str(content_func_))
    # end if
    body_id_attr_ = ""
    if (php_isset(lambda : PHP_GLOBALS["body_id"])):
        body_id_attr_ = " id=\"" + PHP_GLOBALS["body_id"] + "\""
    # end if
    php_print(" </head>\n   <body")
    php_print(body_id_attr_)
    php_print(""" class=\"wp-core-ui no-js\">
    <script type=\"text/javascript\">
    document.body.className = document.body.className.replace('no-js', 'js');
    </script>
    """)
    call_user_func_array(content_func_, args_)
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
def media_buttons(editor_id_="content", *_args_):
    
    
    instance_ = 0
    instance_ += 1
    post_ = get_post()
    if (not post_) and (not php_empty(lambda : PHP_GLOBALS["post_ID"])):
        post_ = PHP_GLOBALS["post_ID"]
    # end if
    wp_enqueue_media(Array({"post": post_}))
    img_ = "<span class=\"wp-media-buttons-icon\"></span> "
    id_attribute_ = " id=\"insert-media-button\"" if 1 == instance_ else ""
    php_printf("<button type=\"button\"%s class=\"button insert-media add_media\" data-editor=\"%s\">%s</button>", id_attribute_, esc_attr(editor_id_), img_ + __("Add Media"))
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
    legacy_filter_ = apply_filters_deprecated("media_buttons_context", Array(""), "3.5.0", "media_buttons")
    if legacy_filter_:
        #// #WP22559. Close <a> if a plugin started by closing <a> to open their own <a> tag.
        if 0 == php_stripos(php_trim(legacy_filter_), "</a>"):
            legacy_filter_ += "</a>"
        # end if
        php_print(legacy_filter_)
    # end if
# end def media_buttons
#// 
#// @global int $post_ID
#// @param string $type
#// @param int $post_id
#// @param string $tab
#// @return string
#//
def get_upload_iframe_src(type_=None, post_id_=None, tab_=None, *_args_):
    if type_ is None:
        type_ = None
    # end if
    if post_id_ is None:
        post_id_ = None
    # end if
    if tab_ is None:
        tab_ = None
    # end if
    
    global post_ID_
    php_check_if_defined("post_ID_")
    if php_empty(lambda : post_id_):
        post_id_ = post_ID_
    # end if
    upload_iframe_src_ = add_query_arg("post_id", php_int(post_id_), admin_url("media-upload.php"))
    if type_ and "media" != type_:
        upload_iframe_src_ = add_query_arg("type", type_, upload_iframe_src_)
    # end if
    if (not php_empty(lambda : tab_)):
        upload_iframe_src_ = add_query_arg("tab", tab_, upload_iframe_src_)
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
    upload_iframe_src_ = apply_filters(str(type_) + str("_upload_iframe_src"), upload_iframe_src_)
    return add_query_arg("TB_iframe", True, upload_iframe_src_)
# end def get_upload_iframe_src
#// 
#// Handles form submissions for the legacy media uploader.
#// 
#// @since 2.5.0
#// 
#// @return mixed void|object WP_Error on failure
#//
def media_upload_form_handler(*_args_):
    
    
    check_admin_referer("media-form")
    errors_ = None
    if (php_isset(lambda : PHP_POST["send"])):
        keys_ = php_array_keys(PHP_POST["send"])
        send_id_ = php_int(reset(keys_))
    # end if
    if (not php_empty(lambda : PHP_POST["attachments"])):
        for attachment_id_,attachment_ in PHP_POST["attachments"].items():
            post_ = get_post(attachment_id_, ARRAY_A)
            _post_ = post_
            if (not current_user_can("edit_post", attachment_id_)):
                continue
            # end if
            if (php_isset(lambda : attachment_["post_content"])):
                post_["post_content"] = attachment_["post_content"]
            # end if
            if (php_isset(lambda : attachment_["post_title"])):
                post_["post_title"] = attachment_["post_title"]
            # end if
            if (php_isset(lambda : attachment_["post_excerpt"])):
                post_["post_excerpt"] = attachment_["post_excerpt"]
            # end if
            if (php_isset(lambda : attachment_["menu_order"])):
                post_["menu_order"] = attachment_["menu_order"]
            # end if
            if (php_isset(lambda : send_id_)) and attachment_id_ == send_id_:
                if (php_isset(lambda : attachment_["post_parent"])):
                    post_["post_parent"] = attachment_["post_parent"]
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
            post_ = apply_filters("attachment_fields_to_save", post_, attachment_)
            if (php_isset(lambda : attachment_["image_alt"])):
                image_alt_ = wp_unslash(attachment_["image_alt"])
                if get_post_meta(attachment_id_, "_wp_attachment_image_alt", True) != image_alt_:
                    image_alt_ = wp_strip_all_tags(image_alt_, True)
                    #// update_post_meta() expects slashed.
                    update_post_meta(attachment_id_, "_wp_attachment_image_alt", wp_slash(image_alt_))
                # end if
            # end if
            if (php_isset(lambda : post_["errors"])):
                errors_[attachment_id_] = post_["errors"]
                post_["errors"] = None
            # end if
            if post_ != _post_:
                wp_update_post(post_)
            # end if
            for t_ in get_attachment_taxonomies(post_):
                if (php_isset(lambda : attachment_[t_])):
                    wp_set_object_terms(attachment_id_, php_array_map("trim", php_preg_split("/,+/", attachment_[t_])), t_, False)
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
    if (php_isset(lambda : send_id_)):
        attachment_ = wp_unslash(PHP_POST["attachments"][send_id_])
        html_ = attachment_["post_title"] if (php_isset(lambda : attachment_["post_title"])) else ""
        if (not php_empty(lambda : attachment_["url"])):
            rel_ = ""
            if php_strpos(attachment_["url"], "attachment_id") or get_attachment_link(send_id_) == attachment_["url"]:
                rel_ = " rel='attachment wp-att-" + esc_attr(send_id_) + "'"
            # end if
            html_ = str("<a href='") + str(attachment_["url"]) + str("'") + str(rel_) + str(">") + str(html_) + str("</a>")
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
        html_ = apply_filters("media_send_to_editor", html_, send_id_, attachment_)
        return media_send_to_editor(html_)
    # end if
    return errors_
# end def media_upload_form_handler
#// 
#// Handles the process of uploading media.
#// 
#// @since 2.5.0
#// 
#// @return null|string
#//
def wp_media_upload_handler(*_args_):
    
    
    errors_ = Array()
    id_ = 0
    if (php_isset(lambda : PHP_POST["html-upload"])) and (not php_empty(lambda : PHP_FILES)):
        check_admin_referer("media-form")
        #// Upload File button was clicked.
        id_ = media_handle_upload("async-upload", PHP_REQUEST["post_id"])
        PHP_FILES = None
        if is_wp_error(id_):
            errors_["upload_error"] = id_
            id_ = False
        # end if
    # end if
    if (not php_empty(lambda : PHP_POST["insertonlybutton"])):
        src_ = PHP_POST["src"]
        if (not php_empty(lambda : src_)) and (not php_strpos(src_, "://")):
            src_ = str("http://") + str(src_)
        # end if
        if (php_isset(lambda : PHP_POST["media_type"])) and "image" != PHP_POST["media_type"]:
            title_ = esc_html(wp_unslash(PHP_POST["title"]))
            if php_empty(lambda : title_):
                title_ = esc_html(wp_basename(src_))
            # end if
            if title_ and src_:
                html_ = "<a href='" + esc_url(src_) + str("'>") + str(title_) + str("</a>")
            # end if
            type_ = "file"
            ext_ = php_preg_replace("/^.+?\\.([^.]+)$/", "$1", src_)
            if ext_:
                ext_type_ = wp_ext2type(ext_)
                if "audio" == ext_type_ or "video" == ext_type_:
                    type_ = ext_type_
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
            html_ = apply_filters(str(type_) + str("_send_to_editor_url"), html_, esc_url_raw(src_), title_)
        else:
            align_ = ""
            alt_ = esc_attr(wp_unslash(PHP_POST["alt"]))
            if (php_isset(lambda : PHP_POST["align"])):
                align_ = esc_attr(wp_unslash(PHP_POST["align"]))
                class_ = str(" class='align") + str(align_) + str("'")
            # end if
            if (not php_empty(lambda : src_)):
                html_ = "<img src='" + esc_url(src_) + str("' alt='") + str(alt_) + str("'") + str(class_) + str(" />")
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
            html_ = apply_filters("image_send_to_editor_url", html_, esc_url_raw(src_), alt_, align_)
        # end if
        return media_send_to_editor(html_)
    # end if
    if (php_isset(lambda : PHP_POST["save"])):
        errors_["upload_notice"] = __("Saved.")
        wp_enqueue_script("admin-gallery")
        return wp_iframe("media_upload_gallery_form", errors_)
    elif (not php_empty(lambda : PHP_POST)):
        return_ = media_upload_form_handler()
        if php_is_string(return_):
            return return_
        # end if
        if php_is_array(return_):
            errors_ = return_
        # end if
    # end if
    if (php_isset(lambda : PHP_REQUEST["tab"])) and "type_url" == PHP_REQUEST["tab"]:
        type_ = "image"
        if (php_isset(lambda : PHP_REQUEST["type"])) and php_in_array(PHP_REQUEST["type"], Array("video", "audio", "file")):
            type_ = PHP_REQUEST["type"]
        # end if
        return wp_iframe("media_upload_type_url_form", type_, errors_, id_)
    # end if
    return wp_iframe("media_upload_type_form", "image", errors_, id_)
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
def media_sideload_image(file_=None, post_id_=0, desc_=None, return_="html", *_args_):
    if desc_ is None:
        desc_ = None
    # end if
    
    if (not php_empty(lambda : file_)):
        #// Set variables for storage, fix file filename for query strings.
        php_preg_match("/[^\\?]+\\.(jpe?g|jpe|gif|png)\\b/i", file_, matches_)
        if (not matches_):
            return php_new_class("WP_Error", lambda : WP_Error("image_sideload_failed", __("Invalid image URL.")))
        # end if
        file_array_ = Array()
        file_array_["name"] = wp_basename(matches_[0])
        #// Download file to temp location.
        file_array_["tmp_name"] = download_url(file_)
        #// If error storing temporarily, return the error.
        if is_wp_error(file_array_["tmp_name"]):
            return file_array_["tmp_name"]
        # end if
        #// Do the validation and storage stuff.
        id_ = media_handle_sideload(file_array_, post_id_, desc_)
        #// If error storing permanently, unlink.
        if is_wp_error(id_):
            php_no_error(lambda: unlink(file_array_["tmp_name"]))
            return id_
        # end if
        #// Store the original attachment source in meta.
        add_post_meta(id_, "_source_url", file_)
        #// If attachment id was requested, return it.
        if "id" == return_:
            return id_
        # end if
        src_ = wp_get_attachment_url(id_)
    # end if
    #// Finally, check to make sure the file has been saved, then return the HTML.
    if (not php_empty(lambda : src_)):
        if "src" == return_:
            return src_
        # end if
        alt_ = esc_attr(desc_) if (php_isset(lambda : desc_)) else ""
        html_ = str("<img src='") + str(src_) + str("' alt='") + str(alt_) + str("' />")
        return html_
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
def media_upload_gallery(*_args_):
    
    
    errors_ = Array()
    if (not php_empty(lambda : PHP_POST)):
        return_ = media_upload_form_handler()
        if php_is_string(return_):
            return return_
        # end if
        if php_is_array(return_):
            errors_ = return_
        # end if
    # end if
    wp_enqueue_script("admin-gallery")
    return wp_iframe("media_upload_gallery_form", errors_)
# end def media_upload_gallery
#// 
#// Retrieves the legacy media library form in an iframe.
#// 
#// @since 2.5.0
#// 
#// @return string|null
#//
def media_upload_library(*_args_):
    
    
    errors_ = Array()
    if (not php_empty(lambda : PHP_POST)):
        return_ = media_upload_form_handler()
        if php_is_string(return_):
            return return_
        # end if
        if php_is_array(return_):
            errors_ = return_
        # end if
    # end if
    return wp_iframe("media_upload_library_form", errors_)
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
def image_align_input_fields(post_=None, checked_="", *_args_):
    
    
    if php_empty(lambda : checked_):
        checked_ = get_user_setting("align", "none")
    # end if
    alignments_ = Array({"none": __("None"), "left": __("Left"), "center": __("Center"), "right": __("Right")})
    if (not php_array_key_exists(php_str(checked_), alignments_)):
        checked_ = "none"
    # end if
    out_ = Array()
    for name_,label_ in alignments_.items():
        name_ = esc_attr(name_)
        out_[-1] = str("<input type='radio' name='attachments[") + str(post_.ID) + str("][align]' id='image-align-") + str(name_) + str("-") + str(post_.ID) + str("' value='") + str(name_) + str("'") + " checked='checked'" if checked_ == name_ else "" + str(" /><label for='image-align-") + str(name_) + str("-") + str(post_.ID) + str("' class='align image-align-") + str(name_) + str("-label'>") + str(label_) + str("</label>")
    # end for
    return php_join("\n", out_)
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
def image_size_input_fields(post_=None, check_="", *_args_):
    
    
    #// 
    #// Filters the names and labels of the default image sizes.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[] $size_names Array of image size labels keyed by their name. Default values
    #// include 'Thumbnail', 'Medium', 'Large', and 'Full Size'.
    #//
    size_names_ = apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")}))
    if php_empty(lambda : check_):
        check_ = get_user_setting("imgsize", "medium")
    # end if
    out_ = Array()
    for size_,label_ in size_names_.items():
        downsize_ = image_downsize(post_.ID, size_)
        checked_ = ""
        #// Is this size selectable?
        enabled_ = downsize_[3] or "full" == size_
        css_id_ = str("image-size-") + str(size_) + str("-") + str(post_.ID)
        #// If this size is the default but that's not available, don't select it.
        if size_ == check_:
            if enabled_:
                checked_ = " checked='checked'"
            else:
                check_ = ""
            # end if
        elif (not check_) and enabled_ and "thumbnail" != size_:
            #// 
            #// If $check is not enabled, default to the first available size
            #// that's bigger than a thumbnail.
            #//
            check_ = size_
            checked_ = " checked='checked'"
        # end if
        html_ = "<div class='image-size-item'><input type='radio' " + disabled(enabled_, False, False) + str("name='attachments[") + str(post_.ID) + str("][image-size]' id='") + str(css_id_) + str("' value='") + str(size_) + str("'") + str(checked_) + str(" />")
        html_ += str("<label for='") + str(css_id_) + str("'>") + str(label_) + str("</label>")
        #// Only show the dimensions if that choice is available.
        if enabled_:
            html_ += str(" <label for='") + str(css_id_) + str("' class='help'>") + php_sprintf("(%d&nbsp;&times;&nbsp;%d)", downsize_[1], downsize_[2]) + "</label>"
        # end if
        html_ += "</div>"
        out_[-1] = html_
    # end for
    return Array({"label": __("Size"), "input": "html", "html": php_join("\n", out_)})
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
def image_link_input_fields(post_=None, url_type_="", *_args_):
    
    
    file_ = wp_get_attachment_url(post_.ID)
    link_ = get_attachment_link(post_.ID)
    if php_empty(lambda : url_type_):
        url_type_ = get_user_setting("urlbutton", "post")
    # end if
    url_ = ""
    if "file" == url_type_:
        url_ = file_
    elif "post" == url_type_:
        url_ = link_
    # end if
    return str("\n  <input type='text' class='text urlfield' name='attachments[") + str(post_.ID) + str("][url]' value='") + esc_attr(url_) + "' /><br />\n <button type='button' class='button urlnone' data-link-url=''>" + __("None") + "</button>\n <button type='button' class='button urlfile' data-link-url='" + esc_attr(file_) + "'>" + __("File URL") + "</button>\n  <button type='button' class='button urlpost' data-link-url='" + esc_attr(link_) + "'>" + __("Attachment Post URL") + "</button>\n"
# end def image_link_input_fields
#// 
#// Output a textarea element for inputting an attachment caption.
#// 
#// @since 3.4.0
#// 
#// @param WP_Post $edit_post Attachment WP_Post object.
#// @return string HTML markup for the textarea element.
#//
def wp_caption_input_textarea(edit_post_=None, *_args_):
    
    
    #// Post data is already escaped.
    name_ = str("attachments[") + str(edit_post_.ID) + str("][post_excerpt]")
    return "<textarea name=\"" + name_ + "\" id=\"" + name_ + "\">" + edit_post_.post_excerpt + "</textarea>"
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
def image_attachment_fields_to_edit(form_fields_=None, post_=None, *_args_):
    
    
    return form_fields_
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
def media_single_attachment_fields_to_edit(form_fields_=None, post_=None, *_args_):
    
    
    form_fields_["url"] = None
    form_fields_["align"] = None
    form_fields_["image-size"] = None
    return form_fields_
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
def media_post_single_attachment_fields_to_edit(form_fields_=None, post_=None, *_args_):
    
    
    form_fields_["image_url"] = None
    return form_fields_
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
def image_attachment_fields_to_save(post_=None, attachment_=None, *_args_):
    
    
    if php_substr(post_["post_mime_type"], 0, 5) == "image":
        if php_strlen(php_trim(post_["post_title"])) == 0:
            attachment_url_ = post_["attachment_url"] if (php_isset(lambda : post_["attachment_url"])) else post_["guid"]
            post_["post_title"] = php_preg_replace("/\\.\\w+$/", "", wp_basename(attachment_url_))
            post_["errors"]["post_title"]["errors"][-1] = __("Empty Title filled from filename.")
        # end if
    # end if
    return post_
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
def image_media_send_to_editor(html_=None, attachment_id_=None, attachment_=None, *_args_):
    
    
    post_ = get_post(attachment_id_)
    if php_substr(post_.post_mime_type, 0, 5) == "image":
        url_ = attachment_["url"]
        align_ = attachment_["align"] if (not php_empty(lambda : attachment_["align"])) else "none"
        size_ = attachment_["image-size"] if (not php_empty(lambda : attachment_["image-size"])) else "medium"
        alt_ = attachment_["image_alt"] if (not php_empty(lambda : attachment_["image_alt"])) else ""
        rel_ = php_strpos(url_, "attachment_id") or get_attachment_link(attachment_id_) == url_
        return get_image_send_to_editor(attachment_id_, attachment_["post_excerpt"], attachment_["post_title"], align_, url_, rel_, size_, alt_)
    # end if
    return html_
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
def get_attachment_fields_to_edit(post_=None, errors_=None, *_args_):
    if errors_ is None:
        errors_ = None
    # end if
    
    if php_is_int(post_):
        post_ = get_post(post_)
    # end if
    if php_is_array(post_):
        post_ = php_new_class("WP_Post", lambda : WP_Post(post_))
    # end if
    image_url_ = wp_get_attachment_url(post_.ID)
    edit_post_ = sanitize_post(post_, "edit")
    form_fields_ = Array({"post_title": Array({"label": __("Title"), "value": edit_post_.post_title})}, {"image_alt": Array(), "post_excerpt": Array({"label": __("Caption"), "input": "html", "html": wp_caption_input_textarea(edit_post_)})}, {"post_content": Array({"label": __("Description"), "value": edit_post_.post_content, "input": "textarea"})}, {"url": Array({"label": __("Link URL"), "input": "html", "html": image_link_input_fields(post_, get_option("image_default_link_type")), "helps": __("Enter a link URL or click above for presets.")})}, {"menu_order": Array({"label": __("Order"), "value": edit_post_.menu_order})}, {"image_url": Array({"label": __("File URL"), "input": "html", "html": str("<input type='text' class='text urlfield' readonly='readonly' name='attachments[") + str(post_.ID) + str("][url]' value='") + esc_attr(image_url_) + "' /><br />", "value": wp_get_attachment_url(post_.ID), "helps": __("Location of the uploaded file.")})})
    for taxonomy_ in get_attachment_taxonomies(post_):
        t_ = get_taxonomy(taxonomy_)
        if (not t_["public"]) or (not t_["show_ui"]):
            continue
        # end if
        if php_empty(lambda : t_["label"]):
            t_["label"] = taxonomy_
        # end if
        if php_empty(lambda : t_["args"]):
            t_["args"] = Array()
        # end if
        terms_ = get_object_term_cache(post_.ID, taxonomy_)
        if False == terms_:
            terms_ = wp_get_object_terms(post_.ID, taxonomy_, t_["args"])
        # end if
        values_ = Array()
        for term_ in terms_:
            values_[-1] = term_.slug
        # end for
        t_["value"] = php_join(", ", values_)
        form_fields_[taxonomy_] = t_
    # end for
    #// 
    #// Merge default fields with their errors, so any key passed with the error
    #// (e.g. 'error', 'helps', 'value') will replace the default.
    #// The recursive merge is easily traversed with array casting:
    #// foreach ( (array) $things as $thing )
    #//
    form_fields_ = php_array_merge_recursive(form_fields_, errors_)
    #// This was formerly in image_attachment_fields_to_edit().
    if php_substr(post_.post_mime_type, 0, 5) == "image":
        alt_ = get_post_meta(post_.ID, "_wp_attachment_image_alt", True)
        if php_empty(lambda : alt_):
            alt_ = ""
        # end if
        form_fields_["post_title"]["required"] = True
        form_fields_["image_alt"] = Array({"value": alt_, "label": __("Alternative Text"), "helps": __("Alt text for the image, e.g. &#8220;The Mona Lisa&#8221;")})
        form_fields_["align"] = Array({"label": __("Alignment"), "input": "html", "html": image_align_input_fields(post_, get_option("image_default_align"))})
        form_fields_["image-size"] = image_size_input_fields(post_, get_option("image_default_size", "medium"))
    else:
        form_fields_["image_alt"] = None
    # end if
    #// 
    #// Filters the attachment fields to edit.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array   $form_fields An array of attachment form fields.
    #// @param WP_Post $post        The WP_Post attachment object.
    #//
    form_fields_ = apply_filters("attachment_fields_to_edit", form_fields_, post_)
    return form_fields_
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
def get_media_items(post_id_=None, errors_=None, *_args_):
    
    
    attachments_ = Array()
    if post_id_:
        post_ = get_post(post_id_)
        if post_ and "attachment" == post_.post_type:
            attachments_ = Array({post_.ID: post_})
        else:
            attachments_ = get_children(Array({"post_parent": post_id_, "post_type": "attachment", "orderby": "menu_order ASC, ID", "order": "DESC"}))
        # end if
    else:
        if php_is_array(PHP_GLOBALS["wp_the_query"].posts):
            for attachment_ in PHP_GLOBALS["wp_the_query"].posts:
                attachments_[attachment_.ID] = attachment_
            # end for
        # end if
    # end if
    output_ = ""
    for id_,attachment_ in attachments_.items():
        if "trash" == attachment_.post_status:
            continue
        # end if
        item_ = get_media_item(id_, Array({"errors": errors_[id_] if (php_isset(lambda : errors_[id_])) else None}))
        if item_:
            output_ += str("\n<div id='media-item-") + str(id_) + str("' class='media-item child-of-") + str(attachment_.post_parent) + str(" preloaded'><div class='progress hidden'><div class='bar'></div></div><div id='media-upload-error-") + str(id_) + str("' class='hidden'></div><div class='filename hidden'></div>") + str(item_) + str("\n</div>")
        # end if
    # end for
    return output_
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
def get_media_item(attachment_id_=None, args_=None, *_args_):
    if args_ is None:
        args_ = None
    # end if
    
    global redir_tab_
    php_check_if_defined("redir_tab_")
    thumb_url_ = False
    attachment_id_ = php_intval(attachment_id_)
    if attachment_id_:
        thumb_url_ = wp_get_attachment_image_src(attachment_id_, "thumbnail", True)
        if thumb_url_:
            thumb_url_ = thumb_url_[0]
        # end if
    # end if
    post_ = get_post(attachment_id_)
    current_post_id_ = php_int(PHP_REQUEST["post_id"]) if (not php_empty(lambda : PHP_REQUEST["post_id"])) else 0
    default_args_ = Array({"errors": None, "send": post_type_supports(get_post_type(current_post_id_), "editor") if current_post_id_ else True, "delete": True, "toggle": True, "show_title": True})
    parsed_args_ = wp_parse_args(args_, default_args_)
    #// 
    #// Filters the arguments used to retrieve an image for the edit image form.
    #// 
    #// @since 3.1.0
    #// 
    #// @see get_media_item
    #// 
    #// @param array $parsed_args An array of arguments.
    #//
    parsed_args_ = apply_filters("get_media_item_args", parsed_args_)
    toggle_on_ = __("Show")
    toggle_off_ = __("Hide")
    file_ = get_attached_file(post_.ID)
    filename_ = esc_html(wp_basename(file_))
    title_ = esc_attr(post_.post_title)
    post_mime_types_ = get_post_mime_types()
    keys_ = php_array_keys(wp_match_mime_types(php_array_keys(post_mime_types_), post_.post_mime_type))
    type_ = reset(keys_)
    type_html_ = str("<input type='hidden' id='type-of-") + str(attachment_id_) + str("' value='") + esc_attr(type_) + "' />"
    form_fields_ = get_attachment_fields_to_edit(post_, parsed_args_["errors"])
    if parsed_args_["toggle"]:
        class_ = "startclosed" if php_empty(lambda : parsed_args_["errors"]) else "startopen"
        toggle_links_ = str("\n     <a class='toggle describe-toggle-on' href='#'>") + str(toggle_on_) + str("</a>\n        <a class='toggle describe-toggle-off' href='#'>") + str(toggle_off_) + str("</a>")
    else:
        class_ = ""
        toggle_links_ = ""
    # end if
    display_title_ = title_ if (not php_empty(lambda : title_)) else filename_
    #// $title shouldn't ever be empty, but just in case.
    display_title_ = "<div class='filename new'><span class='title'>" + wp_html_excerpt(display_title_, 60, "&hellip;") + "</span></div>" if parsed_args_["show_title"] else ""
    gallery_ = (php_isset(lambda : PHP_REQUEST["tab"])) and "gallery" == PHP_REQUEST["tab"] or (php_isset(lambda : redir_tab_)) and "gallery" == redir_tab_
    order_ = ""
    for key_,val_ in form_fields_.items():
        if "menu_order" == key_:
            if gallery_:
                order_ = str("<div class='menu_order'> <input class='menu_order_input' type='text' id='attachments[") + str(attachment_id_) + str("][menu_order]' name='attachments[") + str(attachment_id_) + str("][menu_order]' value='") + esc_attr(val_["value"]) + "' /></div>"
            else:
                order_ = str("<input type='hidden' name='attachments[") + str(attachment_id_) + str("][menu_order]' value='") + esc_attr(val_["value"]) + "' />"
            # end if
            form_fields_["menu_order"] = None
            break
        # end if
    # end for
    media_dims_ = ""
    meta_ = wp_get_attachment_metadata(post_.ID)
    if (php_isset(lambda : meta_["width"]) and php_isset(lambda : meta_["height"])):
        media_dims_ += str("<span id='media-dims-") + str(post_.ID) + str("'>") + str(meta_["width"]) + str("&nbsp;&times;&nbsp;") + str(meta_["height"]) + str("</span> ")
    # end if
    #// 
    #// Filters the media metadata.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string  $media_dims The HTML markup containing the media dimensions.
    #// @param WP_Post $post       The WP_Post attachment object.
    #//
    media_dims_ = apply_filters("media_meta", media_dims_, post_)
    image_edit_button_ = ""
    if wp_attachment_is_image(post_.ID) and wp_image_editor_supports(Array({"mime_type": post_.post_mime_type})):
        nonce_ = wp_create_nonce(str("image_editor-") + str(post_.ID))
        image_edit_button_ = str("<input type='button' id='imgedit-open-btn-") + str(post_.ID) + str("' onclick='imageEdit.open( ") + str(post_.ID) + str(", \"") + str(nonce_) + str("\" )' class='button' value='") + esc_attr__("Edit Image") + "' /> <span class='spinner'></span>"
    # end if
    attachment_url_ = get_permalink(attachment_id_)
    item_ = str("\n     ") + str(type_html_) + str("\n      ") + str(toggle_links_) + str("\n       ") + str(order_) + str("\n      ") + str(display_title_) + str("\n      <table class='slidetoggle describe ") + str(class_) + str("'>\n         <thead class='media-item-info' id='media-head-") + str(post_.ID) + str("'>\n            <tr>\n          <td class='A1B1' id='thumbnail-head-") + str(post_.ID) + str("'>\n          <p><a href='") + str(attachment_url_) + str("' target='_blank'><img class='thumbnail' src='") + str(thumb_url_) + str("' alt='' /></a></p>\n            <p>") + str(image_edit_button_) + str("""</p>\n         </td>\n         <td>\n          <p><strong>""") + __("File name:") + str("</strong> ") + str(filename_) + str("</p>\n           <p><strong>") + __("File type:") + str("</strong> ") + str(post_.post_mime_type) + str("</p>\n          <p><strong>") + __("Upload date:") + "</strong> " + mysql2date(__("F j, Y"), post_.post_date) + "</p>"
    if (not php_empty(lambda : media_dims_)):
        item_ += "<p><strong>" + __("Dimensions:") + str("</strong> ") + str(media_dims_) + str("</p>\n")
    # end if
    item_ += "</td></tr>\n"
    item_ += str("""\n      </thead>\n      <tbody>\n       <tr><td colspan='2' class='imgedit-response' id='imgedit-response-""") + str(post_.ID) + str("'></td></tr>\n\n      <tr><td style='display:none' colspan='2' class='image-editor' id='image-editor-") + str(post_.ID) + str("'></td></tr>\n\n       <tr><td colspan='2'><p class='media-types media-types-required-info'>") + php_sprintf(__("Required fields are marked %s"), "<span class=\"required\">*</span>") + "</p></td></tr>\n"
    defaults_ = Array({"input": "text", "required": False, "value": "", "extra_rows": Array()})
    if parsed_args_["send"]:
        parsed_args_["send"] = get_submit_button(__("Insert into Post"), "", str("send[") + str(attachment_id_) + str("]"), False)
    # end if
    delete_ = "" if php_empty(lambda : parsed_args_["delete"]) else parsed_args_["delete"]
    if delete_ and current_user_can("delete_post", attachment_id_):
        if (not EMPTY_TRASH_DAYS):
            delete_ = "<a href='" + wp_nonce_url(str("post.php?action=delete&amp;post=") + str(attachment_id_), "delete-post_" + attachment_id_) + str("' id='del[") + str(attachment_id_) + str("]' class='delete-permanently'>") + __("Delete Permanently") + "</a>"
        elif (not MEDIA_TRASH):
            delete_ = str("<a href='#' class='del-link' onclick=\"document.getElementById('del_attachment_") + str(attachment_id_) + str("').style.display='block';return false;\">") + __("Delete") + str("</a>\n              <div id='del_attachment_") + str(attachment_id_) + str("' class='del-attachment' style='display:none;'>") + "<p>" + php_sprintf(__("You are about to delete %s."), "<strong>" + filename_ + "</strong>") + "</p>\n              <a href='" + wp_nonce_url(str("post.php?action=delete&amp;post=") + str(attachment_id_), "delete-post_" + attachment_id_) + str("' id='del[") + str(attachment_id_) + str("]' class='button'>") + __("Continue") + "</a>\n              <a href='#' class='button' onclick=\"this.parentNode.style.display='none';return false;\">" + __("Cancel") + "</a>\n                </div>"
        else:
            delete_ = "<a href='" + wp_nonce_url(str("post.php?action=trash&amp;post=") + str(attachment_id_), "trash-post_" + attachment_id_) + str("' id='del[") + str(attachment_id_) + str("]' class='delete'>") + __("Move to Trash") + "</a>\n            <a href='" + wp_nonce_url(str("post.php?action=untrash&amp;post=") + str(attachment_id_), "untrash-post_" + attachment_id_) + str("' id='undo[") + str(attachment_id_) + str("]' class='undo hidden'>") + __("Undo") + "</a>"
        # end if
    else:
        delete_ = ""
    # end if
    thumbnail_ = ""
    calling_post_id_ = 0
    if (php_isset(lambda : PHP_REQUEST["post_id"])):
        calling_post_id_ = absint(PHP_REQUEST["post_id"])
    elif (php_isset(lambda : PHP_POST)) and php_count(PHP_POST):
        #// Like for async-upload where $_GET['post_id'] isn't set.
        calling_post_id_ = post_.post_parent
    # end if
    if "image" == type_ and calling_post_id_ and current_theme_supports("post-thumbnails", get_post_type(calling_post_id_)) and post_type_supports(get_post_type(calling_post_id_), "thumbnail") and get_post_thumbnail_id(calling_post_id_) != attachment_id_:
        calling_post_ = get_post(calling_post_id_)
        calling_post_type_object_ = get_post_type_object(calling_post_.post_type)
        ajax_nonce_ = wp_create_nonce(str("set_post_thumbnail-") + str(calling_post_id_))
        thumbnail_ = "<a class='wp-post-thumbnail' id='wp-post-thumbnail-" + attachment_id_ + str("' href='#' onclick='WPSetAsThumbnail(\"") + str(attachment_id_) + str("\", \"") + str(ajax_nonce_) + str("\");return false;'>") + esc_html(calling_post_type_object_.labels.use_featured_image) + "</a>"
    # end if
    if parsed_args_["send"] or thumbnail_ or delete_ and (not (php_isset(lambda : form_fields_["buttons"]))):
        form_fields_["buttons"] = Array({"tr": "        <tr class='submit'><td></td><td class='savesend'>" + parsed_args_["send"] + str(" ") + str(thumbnail_) + str(" ") + str(delete_) + str("</td></tr>\n")})
    # end if
    hidden_fields_ = Array()
    for id_,field_ in form_fields_.items():
        if "_" == id_[0]:
            continue
        # end if
        if (not php_empty(lambda : field_["tr"])):
            item_ += field_["tr"]
            continue
        # end if
        field_ = php_array_merge(defaults_, field_)
        name_ = str("attachments[") + str(attachment_id_) + str("][") + str(id_) + str("]")
        if "hidden" == field_["input"]:
            hidden_fields_[name_] = field_["value"]
            continue
        # end if
        required_ = "<span class=\"required\">*</span>" if field_["required"] else ""
        required_attr_ = " required" if field_["required"] else ""
        class_ = id_
        class_ += " form-required" if field_["required"] else ""
        item_ += str("      <tr class='") + str(class_) + str("'>\n         <th scope='row' class='label'><label for='") + str(name_) + str("'><span class='alignleft'>") + str(field_["label"]) + str(required_) + str("</span><br class='clear' /></label></th>\n         <td class='field'>")
        if (not php_empty(lambda : field_[field_["input"]])):
            item_ += field_[field_["input"]]
        elif "textarea" == field_["input"]:
            if "post_content" == id_ and user_can_richedit():
                #// Sanitize_post() skips the post_content when user_can_richedit.
                field_["value"] = php_htmlspecialchars(field_["value"], ENT_QUOTES)
            # end if
            #// Post_excerpt is already escaped by sanitize_post() in get_attachment_fields_to_edit().
            item_ += str("<textarea id='") + str(name_) + str("' name='") + str(name_) + str("'") + str(required_attr_) + str(">") + field_["value"] + "</textarea>"
        else:
            item_ += str("<input type='text' class='text' id='") + str(name_) + str("' name='") + str(name_) + str("' value='") + esc_attr(field_["value"]) + str("'") + str(required_attr_) + str(" />")
        # end if
        if (not php_empty(lambda : field_["helps"])):
            item_ += "<p class='help'>" + php_join("</p>\n<p class='help'>", array_unique(field_["helps"])) + "</p>"
        # end if
        item_ += "</td>\n       </tr>\n"
        extra_rows_ = Array()
        if (not php_empty(lambda : field_["errors"])):
            for error_ in array_unique(field_["errors"]):
                extra_rows_["error"][-1] = error_
            # end for
        # end if
        if (not php_empty(lambda : field_["extra_rows"])):
            for class_,rows_ in field_["extra_rows"].items():
                for html_ in rows_:
                    extra_rows_[class_][-1] = html_
                # end for
            # end for
        # end if
        for class_,rows_ in extra_rows_.items():
            for html_ in rows_:
                item_ += str("      <tr><td></td><td class='") + str(class_) + str("'>") + str(html_) + str("</td></tr>\n")
            # end for
        # end for
    # end for
    if (not php_empty(lambda : form_fields_["_final"])):
        item_ += str("      <tr class='final'><td colspan='2'>") + str(form_fields_["_final"]) + str("</td></tr>\n")
    # end if
    item_ += "  </tbody>\n"
    item_ += "  </table>\n"
    for name_,value_ in hidden_fields_.items():
        item_ += str("  <input type='hidden' name='") + str(name_) + str("' id='") + str(name_) + str("' value='") + esc_attr(value_) + "' />\n"
    # end for
    if post_.post_parent < 1 and (php_isset(lambda : PHP_REQUEST["post_id"])):
        parent_ = php_int(PHP_REQUEST["post_id"])
        parent_name_ = str("attachments[") + str(attachment_id_) + str("][post_parent]")
        item_ += str("  <input type='hidden' name='") + str(parent_name_) + str("' id='") + str(parent_name_) + str("' value='") + str(parent_) + str("' />\n")
    # end if
    return item_
# end def get_media_item
#// 
#// @since 3.5.0
#// 
#// @param int   $attachment_id
#// @param array $args
#// @return array
#//
def get_compat_media_markup(attachment_id_=None, args_=None, *_args_):
    if args_ is None:
        args_ = None
    # end if
    
    post_ = get_post(attachment_id_)
    default_args_ = Array({"errors": None, "in_modal": False})
    user_can_edit_ = current_user_can("edit_post", attachment_id_)
    args_ = wp_parse_args(args_, default_args_)
    #// This filter is documented in wp-admin/includes/media.php
    args_ = apply_filters("get_media_item_args", args_)
    form_fields_ = Array()
    if args_["in_modal"]:
        for taxonomy_ in get_attachment_taxonomies(post_):
            t_ = get_taxonomy(taxonomy_)
            if (not t_["public"]) or (not t_["show_ui"]):
                continue
            # end if
            if php_empty(lambda : t_["label"]):
                t_["label"] = taxonomy_
            # end if
            if php_empty(lambda : t_["args"]):
                t_["args"] = Array()
            # end if
            terms_ = get_object_term_cache(post_.ID, taxonomy_)
            if False == terms_:
                terms_ = wp_get_object_terms(post_.ID, taxonomy_, t_["args"])
            # end if
            values_ = Array()
            for term_ in terms_:
                values_[-1] = term_.slug
            # end for
            t_["value"] = php_join(", ", values_)
            t_["taxonomy"] = True
            form_fields_[taxonomy_] = t_
        # end for
    # end if
    #// 
    #// Merge default fields with their errors, so any key passed with the error
    #// (e.g. 'error', 'helps', 'value') will replace the default.
    #// The recursive merge is easily traversed with array casting:
    #// foreach ( (array) $things as $thing )
    #//
    form_fields_ = php_array_merge_recursive(form_fields_, args_["errors"])
    #// This filter is documented in wp-admin/includes/media.php
    form_fields_ = apply_filters("attachment_fields_to_edit", form_fields_, post_)
    form_fields_["image-size"] = None
    form_fields_["align"] = None
    form_fields_["image_alt"] = None
    form_fields_["post_title"] = None
    form_fields_["post_excerpt"] = None
    form_fields_["post_content"] = None
    form_fields_["url"] = None
    form_fields_["menu_order"] = None
    form_fields_["image_url"] = None
    #// This filter is documented in wp-admin/includes/media.php
    media_meta_ = apply_filters("media_meta", "", post_)
    defaults_ = Array({"input": "text", "required": False, "value": "", "extra_rows": Array(), "show_in_edit": True, "show_in_modal": True})
    hidden_fields_ = Array()
    item_ = ""
    for id_,field_ in form_fields_.items():
        if "_" == id_[0]:
            continue
        # end if
        name_ = str("attachments[") + str(attachment_id_) + str("][") + str(id_) + str("]")
        id_attr_ = str("attachments-") + str(attachment_id_) + str("-") + str(id_)
        if (not php_empty(lambda : field_["tr"])):
            item_ += field_["tr"]
            continue
        # end if
        field_ = php_array_merge(defaults_, field_)
        if (not field_["show_in_edit"]) and (not args_["in_modal"]) or (not field_["show_in_modal"]) and args_["in_modal"]:
            continue
        # end if
        if "hidden" == field_["input"]:
            hidden_fields_[name_] = field_["value"]
            continue
        # end if
        readonly_ = " readonly='readonly' " if (not user_can_edit_) and (not php_empty(lambda : field_["taxonomy"])) else ""
        required_ = "<span class=\"required\">*</span>" if field_["required"] else ""
        required_attr_ = " required" if field_["required"] else ""
        class_ = "compat-field-" + id_
        class_ += " form-required" if field_["required"] else ""
        item_ += str("      <tr class='") + str(class_) + str("'>")
        item_ += str("          <th scope='row' class='label'><label for='") + str(id_attr_) + str("'><span class='alignleft'>") + str(field_["label"]) + str("</span>") + str(required_) + str("<br class='clear' /></label>")
        item_ += "</th>\n           <td class='field'>"
        if (not php_empty(lambda : field_[field_["input"]])):
            item_ += field_[field_["input"]]
        elif "textarea" == field_["input"]:
            if "post_content" == id_ and user_can_richedit():
                #// sanitize_post() skips the post_content when user_can_richedit.
                field_["value"] = php_htmlspecialchars(field_["value"], ENT_QUOTES)
            # end if
            item_ += str("<textarea id='") + str(id_attr_) + str("' name='") + str(name_) + str("'") + str(required_attr_) + str(">") + field_["value"] + "</textarea>"
        else:
            item_ += str("<input type='text' class='text' id='") + str(id_attr_) + str("' name='") + str(name_) + str("' value='") + esc_attr(field_["value"]) + str("' ") + str(readonly_) + str(required_attr_) + str(" />")
        # end if
        if (not php_empty(lambda : field_["helps"])):
            item_ += "<p class='help'>" + php_join("</p>\n<p class='help'>", array_unique(field_["helps"])) + "</p>"
        # end if
        item_ += "</td>\n       </tr>\n"
        extra_rows_ = Array()
        if (not php_empty(lambda : field_["errors"])):
            for error_ in array_unique(field_["errors"]):
                extra_rows_["error"][-1] = error_
            # end for
        # end if
        if (not php_empty(lambda : field_["extra_rows"])):
            for class_,rows_ in field_["extra_rows"].items():
                for html_ in rows_:
                    extra_rows_[class_][-1] = html_
                # end for
            # end for
        # end if
        for class_,rows_ in extra_rows_.items():
            for html_ in rows_:
                item_ += str("      <tr><td></td><td class='") + str(class_) + str("'>") + str(html_) + str("</td></tr>\n")
            # end for
        # end for
    # end for
    if (not php_empty(lambda : form_fields_["_final"])):
        item_ += str("      <tr class='final'><td colspan='2'>") + str(form_fields_["_final"]) + str("</td></tr>\n")
    # end if
    if item_:
        item_ = "<p class=\"media-types media-types-required-info\">" + php_sprintf(__("Required fields are marked %s"), "<span class=\"required\">*</span>") + "</p>" + "<table class=\"compat-attachment-fields\">" + item_ + "</table>"
    # end if
    for hidden_field_,value_ in hidden_fields_.items():
        item_ += "<input type=\"hidden\" name=\"" + esc_attr(hidden_field_) + "\" value=\"" + esc_attr(value_) + "\" />" + "\n"
    # end for
    if item_:
        item_ = "<input type=\"hidden\" name=\"attachments[" + attachment_id_ + "][menu_order]\" value=\"" + esc_attr(post_.menu_order) + "\" />" + item_
    # end if
    return Array({"item": item_, "meta": media_meta_})
# end def get_compat_media_markup
#// 
#// Outputs the legacy media upload header.
#// 
#// @since 2.5.0
#//
def media_upload_header(*_args_):
    
    
    post_id_ = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    php_print("<script type=\"text/javascript\">post_id = " + post_id_ + ";</script>")
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
def media_upload_form(errors_=None, *_args_):
    if errors_ is None:
        errors_ = None
    # end if
    
    global type_
    global tab_
    global is_IE_
    global is_opera_
    php_check_if_defined("type_","tab_","is_IE_","is_opera_")
    if (not _device_can_upload()):
        php_print("<p>" + php_sprintf(__("The web browser on your device cannot be used to upload files. You may be able to use the <a href=\"%s\">native app for your device</a> instead."), "https://apps.wordpress.org/") + "</p>")
        return
    # end if
    upload_action_url_ = admin_url("async-upload.php")
    post_id_ = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    _type_ = type_ if (php_isset(lambda : type_)) else ""
    _tab_ = tab_ if (php_isset(lambda : tab_)) else ""
    max_upload_size_ = wp_max_upload_size()
    if (not max_upload_size_):
        max_upload_size_ = 0
    # end if
    php_print(" <div id=\"media-upload-notice\">\n  ")
    if (php_isset(lambda : errors_["upload_notice"])):
        php_print(errors_["upload_notice"])
    # end if
    php_print(" </div>\n    <div id=\"media-upload-error\">\n   ")
    if (php_isset(lambda : errors_["upload_error"])) and is_wp_error(errors_["upload_error"]):
        php_print(errors_["upload_error"].get_error_message())
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
    post_params_ = Array({"post_id": post_id_, "_wpnonce": wp_create_nonce("media-form"), "type": _type_, "tab": _tab_, "short": "1"})
    #// 
    #// Filters the media upload post parameters.
    #// 
    #// @since 3.1.0 As 'swfupload_post_params'
    #// @since 3.3.0
    #// 
    #// @param array $post_params An array of media upload parameters used by Plupload.
    #//
    post_params_ = apply_filters("upload_post_params", post_params_)
    #// 
    #// Since 4.9 the `runtimes` setting is hardcoded in our version of Plupload to `html5,html4`,
    #// and the `flash_swf_url` and `silverlight_xap_url` are not used.
    #//
    plupload_init_ = Array({"browse_button": "plupload-browse-button", "container": "plupload-upload-ui", "drop_element": "drag-drop-area", "file_data_name": "async-upload", "url": upload_action_url_, "filters": Array({"max_file_size": max_upload_size_ + "b"})}, {"multipart_params": post_params_})
    #// 
    #// Currently only iOS Safari supports multiple files uploading,
    #// but iOS 7.x has a bug that prevents uploading of videos when enabled.
    #// See #29602.
    #//
    if wp_is_mobile() and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "OS 7_") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "like Mac OS X") != False:
        plupload_init_["multi_selection"] = False
    # end if
    #// 
    #// Filters the default Plupload settings.
    #// 
    #// @since 3.3.0
    #// 
    #// @param array $plupload_init An array of default settings used by Plupload.
    #//
    plupload_init_ = apply_filters("plupload_init", plupload_init_)
    php_print(" <script type=\"text/javascript\">\n ")
    #// Verify size is an int. If not return default value.
    large_size_h_ = absint(get_option("large_size_h"))
    if (not large_size_h_):
        large_size_h_ = 1024
    # end if
    large_size_w_ = absint(get_option("large_size_w"))
    if (not large_size_w_):
        large_size_w_ = 1024
    # end if
    php_print(" var resize_height = ")
    php_print(large_size_h_)
    php_print(", resize_width = ")
    php_print(large_size_w_)
    php_print(",\n  wpUploaderInit = ")
    php_print(wp_json_encode(plupload_init_))
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
    php_printf(__("Maximum upload file size: %s."), esc_html(size_format(max_upload_size_)))
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
def media_upload_type_form(type_="file", errors_=None, id_=None, *_args_):
    if errors_ is None:
        errors_ = None
    # end if
    if id_ is None:
        id_ = None
    # end if
    
    media_upload_header()
    post_id_ = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    form_action_url_ = admin_url(str("media-upload.php?type=") + str(type_) + str("&tab=type&post_id=") + str(post_id_))
    #// 
    #// Filters the media upload form action URL.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $form_action_url The media upload form action URL.
    #// @param string $type            The type of media. Default 'file'.
    #//
    form_action_url_ = apply_filters("media_upload_form_url", form_action_url_, type_)
    form_class_ = "media-upload-form type-form validate"
    if get_user_setting("uploader"):
        form_class_ += " html-uploader"
    # end if
    php_print(" <form enctype=\"multipart/form-data\" method=\"post\" action=\"")
    php_print(esc_url(form_action_url_))
    php_print("\" class=\"")
    php_print(form_class_)
    php_print("\" id=\"")
    php_print(type_)
    php_print("-form\">\n       ")
    submit_button("", "hidden", "save", False)
    php_print(" <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id_))
    php_print("\" />\n      ")
    wp_nonce_field("media-form")
    php_print("\n   <h3 class=\"media-title\">")
    _e("Add media files from your computer")
    php_print("</h3>\n\n    ")
    media_upload_form(errors_)
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
    if id_:
        if (not is_wp_error(id_)):
            add_filter("attachment_fields_to_edit", "media_post_single_attachment_fields_to_edit", 10, 2)
            php_print(get_media_items(id_, errors_))
        else:
            php_print("<div id=\"media-upload-error\">" + esc_html(id_.get_error_message()) + "</div></div>")
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
def media_upload_type_url_form(type_=None, errors_=None, id_=None, *_args_):
    if type_ is None:
        type_ = None
    # end if
    if errors_ is None:
        errors_ = None
    # end if
    if id_ is None:
        id_ = None
    # end if
    
    if None == type_:
        type_ = "image"
    # end if
    media_upload_header()
    post_id_ = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    form_action_url_ = admin_url(str("media-upload.php?type=") + str(type_) + str("&tab=type&post_id=") + str(post_id_))
    #// This filter is documented in wp-admin/includes/media.php
    form_action_url_ = apply_filters("media_upload_form_url", form_action_url_, type_)
    form_class_ = "media-upload-form type-form validate"
    if get_user_setting("uploader"):
        form_class_ += " html-uploader"
    # end if
    php_print(" <form enctype=\"multipart/form-data\" method=\"post\" action=\"")
    php_print(esc_url(form_action_url_))
    php_print("\" class=\"")
    php_print(form_class_)
    php_print("\" id=\"")
    php_print(type_)
    php_print("-form\">\n   <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id_))
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
    php_print(apply_filters("type_url_form_media", wp_media_insert_url_form(type_)))
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
def media_upload_gallery_form(errors_=None, *_args_):
    
    
    global redir_tab_
    global type_
    php_check_if_defined("redir_tab_","type_")
    redir_tab_ = "gallery"
    media_upload_header()
    post_id_ = php_intval(PHP_REQUEST["post_id"])
    form_action_url_ = admin_url(str("media-upload.php?type=") + str(type_) + str("&tab=gallery&post_id=") + str(post_id_))
    #// This filter is documented in wp-admin/includes/media.php
    form_action_url_ = apply_filters("media_upload_form_url", form_action_url_, type_)
    form_class_ = "media-upload-form validate"
    if get_user_setting("uploader"):
        form_class_ += " html-uploader"
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
    php_print(esc_url(form_action_url_))
    php_print("\" class=\"")
    php_print(form_class_)
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
    php_print(get_media_items(post_id_, errors_))
    php_print("""   </div>
    <p class=\"ml-submit\">
    """)
    submit_button(__("Save all changes"), "savebutton", "save", False, Array({"id": "save-all", "style": "display: none;"}))
    php_print(" <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id_))
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
def media_upload_library_form(errors_=None, *_args_):
    
    global PHP_REQUEST
    global wpdb_
    global wp_query_
    global wp_locale_
    global type_
    global tab_
    global post_mime_types_
    php_check_if_defined("wpdb_","wp_query_","wp_locale_","type_","tab_","post_mime_types_")
    media_upload_header()
    post_id_ = php_intval(PHP_REQUEST["post_id"]) if (php_isset(lambda : PHP_REQUEST["post_id"])) else 0
    form_action_url_ = admin_url(str("media-upload.php?type=") + str(type_) + str("&tab=library&post_id=") + str(post_id_))
    #// This filter is documented in wp-admin/includes/media.php
    form_action_url_ = apply_filters("media_upload_form_url", form_action_url_, type_)
    form_class_ = "media-upload-form validate"
    if get_user_setting("uploader"):
        form_class_ += " html-uploader"
    # end if
    q_ = PHP_REQUEST
    q_["posts_per_page"] = 10
    q_["paged"] = php_intval(q_["paged"]) if (php_isset(lambda : q_["paged"])) else 0
    if q_["paged"] < 1:
        q_["paged"] = 1
    # end if
    q_["offset"] = q_["paged"] - 1 * 10
    if q_["offset"] < 1:
        q_["offset"] = 0
    # end if
    post_mime_types_, avail_post_mime_types_ = wp_edit_attachments_query(q_)
    php_print(" <form id=\"filter\" method=\"get\">\n   <input type=\"hidden\" name=\"type\" value=\"")
    php_print(esc_attr(type_))
    php_print("\" />\n  <input type=\"hidden\" name=\"tab\" value=\"")
    php_print(esc_attr(tab_))
    php_print("\" />\n  <input type=\"hidden\" name=\"post_id\" value=\"")
    php_print(php_int(post_id_))
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
    type_links_ = Array()
    _num_posts_ = wp_count_attachments()
    matches_ = wp_match_mime_types(php_array_keys(post_mime_types_), php_array_keys(_num_posts_))
    for _type_,reals_ in matches_.items():
        for real_ in reals_:
            if (php_isset(lambda : num_posts_[_type_])):
                num_posts_[_type_] += _num_posts_[real_]
            else:
                num_posts_[_type_] = _num_posts_[real_]
            # end if
        # end for
    # end for
    #// If available type specified by media button clicked, filter by that type.
    if php_empty(lambda : PHP_REQUEST["post_mime_type"]) and (not php_empty(lambda : num_posts_[type_])):
        PHP_REQUEST["post_mime_type"] = type_
        post_mime_types_, avail_post_mime_types_ = wp_edit_attachments_query()
    # end if
    if php_empty(lambda : PHP_REQUEST["post_mime_type"]) or "all" == PHP_REQUEST["post_mime_type"]:
        class_ = " class=\"current\""
    else:
        class_ = ""
    # end if
    type_links_[-1] = "<li><a href=\"" + esc_url(add_query_arg(Array({"post_mime_type": "all", "paged": False, "m": False}))) + "\"" + class_ + ">" + __("All Types") + "</a>"
    for mime_type_,label_ in post_mime_types_.items():
        class_ = ""
        if (not wp_match_mime_types(mime_type_, avail_post_mime_types_)):
            continue
        # end if
        if (php_isset(lambda : PHP_REQUEST["post_mime_type"])) and wp_match_mime_types(mime_type_, PHP_REQUEST["post_mime_type"]):
            class_ = " class=\"current\""
        # end if
        type_links_[-1] = "<li><a href=\"" + esc_url(add_query_arg(Array({"post_mime_type": mime_type_, "paged": False}))) + "\"" + class_ + ">" + php_sprintf(translate_nooped_plural(label_[2], num_posts_[mime_type_]), "<span id=\"" + mime_type_ + "-counter\">" + number_format_i18n(num_posts_[mime_type_]) + "</span>") + "</a>"
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
    php_print(php_implode(" | </li>", apply_filters("media_upload_mime_type_links", type_links_)) + "</li>")
    type_links_ = None
    php_print("""   </ul>
    <div class=\"tablenav\">
    """)
    page_links_ = paginate_links(Array({"base": add_query_arg("paged", "%#%"), "format": "", "prev_text": __("&laquo;"), "next_text": __("&raquo;"), "total": ceil(wp_query_.found_posts / 10), "current": q_["paged"]}))
    if page_links_:
        php_print(str("<div class='tablenav-pages'>") + str(page_links_) + str("</div>"))
    # end if
    php_print("\n   <div class=\"alignleft actions\">\n     ")
    arc_query_ = str("SELECT DISTINCT YEAR(post_date) AS yyear, MONTH(post_date) AS mmonth FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'attachment' ORDER BY post_date DESC")
    arc_result_ = wpdb_.get_results(arc_query_)
    month_count_ = php_count(arc_result_)
    selected_month_ = PHP_REQUEST["m"] if (php_isset(lambda : PHP_REQUEST["m"])) else 0
    if month_count_ and (not 1 == month_count_ and 0 == arc_result_[0].mmonth):
        php_print("         <select name='m'>\n         <option")
        selected(selected_month_, 0)
        php_print(" value='0'>")
        _e("All dates")
        php_print("</option>\n          ")
        for arc_row_ in arc_result_:
            if 0 == arc_row_.yyear:
                continue
            # end if
            arc_row_.mmonth = zeroise(arc_row_.mmonth, 2)
            if arc_row_.yyear + arc_row_.mmonth == selected_month_:
                default_ = " selected=\"selected\""
            else:
                default_ = ""
            # end if
            php_print(str("<option") + str(default_) + str(" value='") + esc_attr(arc_row_.yyear + arc_row_.mmonth) + "'>")
            php_print(esc_html(wp_locale_.get_month(arc_row_.mmonth) + str(" ") + str(arc_row_.yyear)))
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
    php_print(esc_url(form_action_url_))
    php_print("\" class=\"")
    php_print(form_class_)
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
    php_print(get_media_items(None, errors_))
    php_print(" </div>\n    <p class=\"ml-submit\">\n       ")
    submit_button(__("Save all changes"), "savebutton", "save", False)
    php_print(" <input type=\"hidden\" name=\"post_id\" id=\"post_id\" value=\"")
    php_print(php_int(post_id_))
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
def wp_media_insert_url_form(default_view_="image", *_args_):
    
    
    #// This filter is documented in wp-admin/includes/media.php
    if (not apply_filters("disable_captions", "")):
        caption_ = """
        <tr class=\"image-only\">
        <th scope=\"row\" class=\"label\">
        <label for=\"caption\"><span class=\"alignleft\">""" + __("Image Caption") + """</span></label>
        </th>
        <td class=\"field\"><textarea id=\"caption\" name=\"caption\"></textarea></td>
        </tr>"""
    else:
        caption_ = ""
    # end if
    default_align_ = get_option("image_default_align")
    if php_empty(lambda : default_align_):
        default_align_ = "none"
    # end if
    if "image" == default_view_:
        view_ = "image-only"
        table_class_ = ""
    else:
        view_ = "not-image"
        table_class_ = view_
    # end if
    return "\n  <p class=\"media-types\"><label><input type=\"radio\" name=\"media_type\" value=\"image\" id=\"image-only\"" + checked("image-only", view_, False) + " /> " + __("Image") + "</label> &nbsp; &nbsp; <label><input type=\"radio\" name=\"media_type\" value=\"generic\" id=\"not-image\"" + checked("not-image", view_, False) + " /> " + __("Audio, Video, or Other File") + "</label></p>\n    <p class=\"media-types media-types-required-info\">" + php_sprintf(__("Required fields are marked %s"), "<span class=\"required\">*</span>") + "</p>\n  <table class=\"describe " + table_class_ + """\"><tbody>
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
    <p class=\"help\">""" + __("Alt text for the image, e.g. &#8220;The Mona Lisa&#8221;") + "</p></td>\n       </tr>\n     " + caption_ + "\n      <tr class=\"align image-only\">\n           <th scope=\"row\" class=\"label\"><p><label for=\"align\">" + __("Alignment") + "</label></p></th>\n            <td class=\"field\">\n              <input name=\"align\" id=\"align-none\" value=\"none\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "none" == default_align_ else "" + " />\n               <label for=\"align-none\" class=\"align image-align-none-label\">" + __("None") + "</label>\n               <input name=\"align\" id=\"align-left\" value=\"left\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "left" == default_align_ else "" + " />\n               <label for=\"align-left\" class=\"align image-align-left-label\">" + __("Left") + "</label>\n               <input name=\"align\" id=\"align-center\" value=\"center\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "center" == default_align_ else "" + " />\n             <label for=\"align-center\" class=\"align image-align-center-label\">" + __("Center") + "</label>\n             <input name=\"align\" id=\"align-right\" value=\"right\" onclick=\"addExtImage.align='align'+this.value\" type=\"radio\"" + " checked=\"checked\"" if "right" == default_align_ else "" + " />\n                <label for=\"align-right\" class=\"align image-align-right-label\">" + __("Right") + """</label>
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
def media_upload_flash_bypass(*_args_):
    
    
    browser_uploader_ = admin_url("media-new.php?browser-uploader")
    post_ = get_post()
    if post_:
        browser_uploader_ += "&amp;post_id=" + php_intval(post_.ID)
    elif (not php_empty(lambda : PHP_GLOBALS["post_ID"])):
        browser_uploader_ += "&amp;post_id=" + php_intval(PHP_GLOBALS["post_ID"])
    # end if
    php_print(" <p class=\"upload-flash-bypass\">\n ")
    php_printf(__("You are using the multi-file uploader. Problems? Try the <a href=\"%1$s\" %2$s>browser uploader</a> instead."), browser_uploader_, "target=\"_blank\"")
    php_print(" </p>\n  ")
# end def media_upload_flash_bypass
#// 
#// Displays the browser's built-in uploader message.
#// 
#// @since 2.6.0
#//
def media_upload_html_bypass(*_args_):
    
    
    php_print(" <p class=\"upload-html-bypass hide-if-no-js\">\n        ")
    _e("You are using the browser&#8217;s built-in file uploader. The WordPress uploader includes multiple file selection and drag and drop capability. <a href=\"#\">Switch to the multi-file uploader</a>.")
    php_print(" </p>\n  ")
# end def media_upload_html_bypass
#// 
#// Used to display a "After a file has been uploaded..." help message.
#// 
#// @since 3.3.0
#//
def media_upload_text_after(*_args_):
    
    
    pass
# end def media_upload_text_after
#// 
#// Displays the checkbox to scale images.
#// 
#// @since 3.3.0
#//
def media_upload_max_image_resize(*_args_):
    
    
    checked_ = " checked=\"true\"" if get_user_setting("upload_resize") else ""
    a_ = ""
    end_ = ""
    if current_user_can("manage_options"):
        a_ = "<a href=\"" + esc_url(admin_url("options-media.php")) + "\" target=\"_blank\">"
        end_ = "</a>"
    # end if
    php_print(" <p class=\"hide-if-no-js\"><label>\n    <input name=\"image_resize\" type=\"checkbox\" id=\"image_resize\" value=\"true\"")
    php_print(checked_)
    php_print(" />\n    ")
    #// translators: 1: Link start tag, 2: Link end tag, 3: Width, 4: Height.
    php_printf(__("Scale images to match the large size selected in %1$simage options%2$s (%3$d &times; %4$d)."), a_, end_, php_int(get_option("large_size_w", "1024")), php_int(get_option("large_size_h", "1024")))
    php_print(" </label></p>\n  ")
# end def media_upload_max_image_resize
#// 
#// Displays the out of storage quota message in Multisite.
#// 
#// @since 3.5.0
#//
def multisite_over_quota_message(*_args_):
    
    
    php_print("<p>" + php_sprintf(__("Sorry, you have used your space allocation of %s. Please delete some files to upload more files."), size_format(get_space_allowed() * MB_IN_BYTES)) + "</p>")
# end def multisite_over_quota_message
#// 
#// Displays the image and editor in the post editor
#// 
#// @since 3.5.0
#// 
#// @param WP_Post $post A post object.
#//
def edit_form_image_editor(post_=None, *_args_):
    
    
    open_ = (php_isset(lambda : PHP_REQUEST["image-editor"]))
    if open_:
        php_include_file(ABSPATH + "wp-admin/includes/image-edit.php", once=True)
    # end if
    thumb_url_ = False
    attachment_id_ = php_intval(post_.ID)
    if attachment_id_:
        thumb_url_ = wp_get_attachment_image_src(attachment_id_, Array(900, 450), True)
    # end if
    alt_text_ = get_post_meta(post_.ID, "_wp_attachment_image_alt", True)
    att_url_ = wp_get_attachment_url(post_.ID)
    php_print(" <div class=\"wp_attachment_holder wp-clearfix\">\n  ")
    if wp_attachment_is_image(post_.ID):
        image_edit_button_ = ""
        if wp_image_editor_supports(Array({"mime_type": post_.post_mime_type})):
            nonce_ = wp_create_nonce(str("image_editor-") + str(post_.ID))
            image_edit_button_ = str("<input type='button' id='imgedit-open-btn-") + str(post_.ID) + str("' onclick='imageEdit.open( ") + str(post_.ID) + str(", \"") + str(nonce_) + str("\" )' class='button' value='") + esc_attr__("Edit Image") + "' /> <span class='spinner'></span>"
        # end if
        open_style_ = ""
        not_open_style_ = ""
        if open_:
            open_style_ = " style=\"display:none\""
        else:
            not_open_style_ = " style=\"display:none\""
        # end if
        php_print("     <div class=\"imgedit-response\" id=\"imgedit-response-")
        php_print(attachment_id_)
        php_print("\"></div>\n\n        <div")
        php_print(open_style_)
        php_print(" class=\"wp_attachment_image wp-clearfix\" id=\"media-head-")
        php_print(attachment_id_)
        php_print("\">\n            <p id=\"thumbnail-head-")
        php_print(attachment_id_)
        php_print("\"><img class=\"thumbnail\" src=\"")
        php_print(set_url_scheme(thumb_url_[0]))
        php_print("\" style=\"max-width:100%\" alt=\"\" /></p>\n            <p>")
        php_print(image_edit_button_)
        php_print("</p>\n       </div>\n        <div")
        php_print(not_open_style_)
        php_print(" class=\"image-editor\" id=\"image-editor-")
        php_print(attachment_id_)
        php_print("\">\n        ")
        if open_:
            wp_image_editor(attachment_id_)
        # end if
        php_print("     </div>\n        ")
    elif attachment_id_ and wp_attachment_is("audio", post_):
        wp_maybe_generate_attachment_metadata(post_)
        php_print(wp_audio_shortcode(Array({"src": att_url_})))
    elif attachment_id_ and wp_attachment_is("video", post_):
        wp_maybe_generate_attachment_metadata(post_)
        meta_ = wp_get_attachment_metadata(attachment_id_)
        w_ = php_min(meta_["width"], 640) if (not php_empty(lambda : meta_["width"])) else 0
        h_ = meta_["height"] if (not php_empty(lambda : meta_["height"])) else 0
        if h_ and w_ < meta_["width"]:
            h_ = round(meta_["height"] * w_ / meta_["width"])
        # end if
        attr_ = Array({"src": att_url_})
        if (not php_empty(lambda : w_)) and (not php_empty(lambda : h_)):
            attr_["width"] = w_
            attr_["height"] = h_
        # end if
        thumb_id_ = get_post_thumbnail_id(attachment_id_)
        if (not php_empty(lambda : thumb_id_)):
            attr_["poster"] = wp_get_attachment_url(thumb_id_)
        # end if
        php_print(wp_video_shortcode(attr_))
    elif (php_isset(lambda : thumb_url_[0])):
        php_print("     <div class=\"wp_attachment_image wp-clearfix\" id=\"media-head-")
        php_print(attachment_id_)
        php_print("\">\n            <p id=\"thumbnail-head-")
        php_print(attachment_id_)
        php_print("\">\n                <img class=\"thumbnail\" src=\"")
        php_print(set_url_scheme(thumb_url_[0]))
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
        do_action("wp_edit_form_attachment_display", post_)
    # end if
    php_print(" </div>\n    <div class=\"wp_attachment_details edit-form-section\">\n   ")
    if "image" == php_substr(post_.post_mime_type, 0, 5):
        php_print("     <p class=\"attachment-alt-text\">\n         <label for=\"attachment_alt\"><strong>")
        _e("Alternative Text")
        php_print("</strong></label><br />\n            <input type=\"text\" class=\"widefat\" name=\"_wp_attachment_image_alt\" id=\"attachment_alt\" aria-describedby=\"alt-text-description\" value=\"")
        php_print(esc_attr(alt_text_))
        php_print("""\" />
        </p>
        <p class=\"attachment-alt-text-description\" id=\"alt-text-description\">
        """)
        php_printf(__("<a href=\"%1$s\" %2$s>Describe the purpose of the image%3$s</a>. Leave empty if the image is purely decorative."), esc_url("https://www.w3.org/WAI/tutorials/images/decision-tree"), "target=\"_blank\" rel=\"noopener noreferrer\"", php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)")))
        php_print("     </p>\n  ")
    # end if
    php_print("\n       <p>\n           <label for=\"attachment_caption\"><strong>")
    _e("Caption")
    php_print("</strong></label><br />\n            <textarea class=\"widefat\" name=\"excerpt\" id=\"attachment_caption\">")
    php_print(post_.post_excerpt)
    php_print("""</textarea>
    </p>
    """)
    quicktags_settings_ = Array({"buttons": "strong,em,link,block,del,ins,img,ul,ol,li,code,close"})
    editor_args_ = Array({"textarea_name": "content", "textarea_rows": 5, "media_buttons": False, "tinymce": False, "quicktags": quicktags_settings_})
    php_print("\n   <label for=\"attachment_content\" class=\"attachment-content-description\"><strong>")
    _e("Description")
    php_print("</strong>\n  ")
    if php_preg_match("#^(audio|video)/#", post_.post_mime_type):
        php_print(": " + __("Displayed on attachment pages."))
    # end if
    php_print(" </label>\n  ")
    wp_editor(post_.post_content, "attachment_content", editor_args_)
    php_print("\n   </div>\n    ")
    extras_ = get_compat_media_markup(post_.ID)
    php_print(extras_["item"])
    php_print("<input type=\"hidden\" id=\"image-edit-context\" value=\"edit-attachment\" />" + "\n")
# end def edit_form_image_editor
#// 
#// Displays non-editable attachment metadata in the publish meta box.
#// 
#// @since 3.5.0
#//
def attachment_submitbox_metadata(*_args_):
    
    
    post_ = get_post()
    attachment_id_ = post_.ID
    file_ = get_attached_file(attachment_id_)
    filename_ = esc_html(wp_basename(file_))
    media_dims_ = ""
    meta_ = wp_get_attachment_metadata(attachment_id_)
    if (php_isset(lambda : meta_["width"]) and php_isset(lambda : meta_["height"])):
        media_dims_ += str("<span id='media-dims-") + str(attachment_id_) + str("'>") + str(meta_["width"]) + str("&nbsp;&times;&nbsp;") + str(meta_["height"]) + str("</span> ")
    # end if
    #// This filter is documented in wp-admin/includes/media.php
    media_dims_ = apply_filters("media_meta", media_dims_, post_)
    att_url_ = wp_get_attachment_url(attachment_id_)
    php_print(" <div class=\"misc-pub-section misc-pub-attachment\">\n      <label for=\"attachment_url\">")
    _e("File URL:")
    php_print("</label>\n       <input type=\"text\" class=\"widefat urlfield\" readonly=\"readonly\" name=\"attachment_url\" id=\"attachment_url\" value=\"")
    php_print(esc_attr(att_url_))
    php_print("""\" />
    </div>
    <div class=\"misc-pub-section misc-pub-filename\">
    """)
    _e("File name:")
    php_print(" <strong>")
    php_print(filename_)
    php_print("""</strong>
    </div>
    <div class=\"misc-pub-section misc-pub-filetype\">
    """)
    _e("File type:")
    php_print("     <strong>\n      ")
    if php_preg_match("/^.*?\\.(\\w+)$/", get_attached_file(post_.ID), matches_):
        php_print(esc_html(php_strtoupper(matches_[1])))
        mime_type_ = php_explode("/", post_.post_mime_type)
        if "image" != mime_type_ and (not php_empty(lambda : meta_["mime_type"])):
            if str(mime_type_) + str("/") + php_strtolower(matches_[1]) != meta_["mime_type"]:
                php_print(" (" + meta_["mime_type"] + ")")
            # end if
        # end if
    else:
        php_print(php_strtoupper(php_str_replace("image/", "", post_.post_mime_type)))
    # end if
    php_print("""       </strong>
    </div>
    """)
    file_size_ = False
    if (php_isset(lambda : meta_["filesize"])):
        file_size_ = meta_["filesize"]
    elif php_file_exists(file_):
        file_size_ = filesize(file_)
    # end if
    if (not php_empty(lambda : file_size_)):
        php_print("     <div class=\"misc-pub-section misc-pub-filesize\">\n            ")
        _e("File size:")
        php_print(" <strong>")
        php_print(size_format(file_size_))
        php_print("</strong>\n      </div>\n        ")
    # end if
    if php_preg_match("#^(audio|video)/#", post_.post_mime_type):
        fields_ = Array({"length_formatted": __("Length:"), "bitrate": __("Bitrate:")})
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
        fields_ = apply_filters("media_submitbox_misc_sections", fields_, post_)
        for key_,label_ in fields_.items():
            if php_empty(lambda : meta_[key_]):
                continue
            # end if
            php_print("         <div class=\"misc-pub-section misc-pub-mime-meta misc-pub-")
            php_print(sanitize_html_class(key_))
            php_print("\">\n                ")
            php_print(label_)
            php_print("             <strong>\n              ")
            for case in Switch(key_):
                if case("bitrate"):
                    php_print(round(meta_["bitrate"] / 1000) + "kb/s")
                    if (not php_empty(lambda : meta_["bitrate_mode"])):
                        php_print(" " + php_strtoupper(esc_html(meta_["bitrate_mode"])))
                    # end if
                    break
                # end if
                if case():
                    php_print(esc_html(meta_[key_]))
                    break
                # end if
            # end for
            php_print("             </strong>\n         </div>\n            ")
        # end for
        fields_ = Array({"dataformat": __("Audio Format:"), "codec": __("Audio Codec:")})
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
        audio_fields_ = apply_filters("audio_submitbox_misc_sections", fields_, post_)
        for key_,label_ in audio_fields_.items():
            if php_empty(lambda : meta_["audio"][key_]):
                continue
            # end if
            php_print("         <div class=\"misc-pub-section misc-pub-audio misc-pub-")
            php_print(sanitize_html_class(key_))
            php_print("\">\n                ")
            php_print(label_)
            php_print(" <strong>")
            php_print(esc_html(meta_["audio"][key_]))
            php_print("</strong>\n          </div>\n            ")
        # end for
    # end if
    if media_dims_:
        php_print("     <div class=\"misc-pub-section misc-pub-dimensions\">\n          ")
        _e("Dimensions:")
        php_print(" <strong>")
        php_print(media_dims_)
        php_print("</strong>\n      </div>\n        ")
    # end if
    if (not php_empty(lambda : meta_["original_image"])):
        php_print("     <div class=\"misc-pub-section misc-pub-original-image\">\n          ")
        _e("Original image:")
        php_print("         <a href=\"")
        php_print(esc_url(wp_get_original_image_url(attachment_id_)))
        php_print("\">\n                ")
        php_print(esc_html(wp_basename(wp_get_original_image_path(attachment_id_))))
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
def wp_add_id3_tag_data(metadata_=None, data_=None, *_args_):
    
    
    for version_ in Array("id3v2", "id3v1"):
        if (not php_empty(lambda : data_[version_]["comments"])):
            for key_,list_ in data_[version_]["comments"].items():
                if "length" != key_ and (not php_empty(lambda : list_)):
                    metadata_[key_] = wp_kses_post(reset(list_))
                    #// Fix bug in byte stream analysis.
                    if "terms_of_use" == key_ and 0 == php_strpos(metadata_[key_], "yright notice."):
                        metadata_[key_] = "Cop" + metadata_[key_]
                    # end if
                # end if
            # end for
            break
        # end if
    # end for
    if (not php_empty(lambda : data_["id3v2"]["APIC"])):
        image_ = reset(data_["id3v2"]["APIC"])
        if (not php_empty(lambda : image_["data"])):
            metadata_["image"] = Array({"data": image_["data"], "mime": image_["image_mime"], "width": image_["image_width"], "height": image_["image_height"]})
        # end if
    elif (not php_empty(lambda : data_["comments"]["picture"])):
        image_ = reset(data_["comments"]["picture"])
        if (not php_empty(lambda : image_["data"])):
            metadata_["image"] = Array({"data": image_["data"], "mime": image_["image_mime"]})
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
def wp_read_video_metadata(file_=None, *_args_):
    
    
    if (not php_file_exists(file_)):
        return False
    # end if
    metadata_ = Array()
    if (not php_defined("GETID3_TEMP_DIR")):
        php_define("GETID3_TEMP_DIR", get_temp_dir())
    # end if
    if (not php_class_exists("getID3", False)):
        php_include_file(ABSPATH + WPINC + "/ID3/getid3.php", once=False)
    # end if
    id3_ = php_new_class("getID3", lambda : getID3())
    data_ = id3_.analyze(file_)
    if (php_isset(lambda : data_["video"]["lossless"])):
        metadata_["lossless"] = data_["video"]["lossless"]
    # end if
    if (not php_empty(lambda : data_["video"]["bitrate"])):
        metadata_["bitrate"] = php_int(data_["video"]["bitrate"])
    # end if
    if (not php_empty(lambda : data_["video"]["bitrate_mode"])):
        metadata_["bitrate_mode"] = data_["video"]["bitrate_mode"]
    # end if
    if (not php_empty(lambda : data_["filesize"])):
        metadata_["filesize"] = php_int(data_["filesize"])
    # end if
    if (not php_empty(lambda : data_["mime_type"])):
        metadata_["mime_type"] = data_["mime_type"]
    # end if
    if (not php_empty(lambda : data_["playtime_seconds"])):
        metadata_["length"] = php_int(round(data_["playtime_seconds"]))
    # end if
    if (not php_empty(lambda : data_["playtime_string"])):
        metadata_["length_formatted"] = data_["playtime_string"]
    # end if
    if (not php_empty(lambda : data_["video"]["resolution_x"])):
        metadata_["width"] = php_int(data_["video"]["resolution_x"])
    # end if
    if (not php_empty(lambda : data_["video"]["resolution_y"])):
        metadata_["height"] = php_int(data_["video"]["resolution_y"])
    # end if
    if (not php_empty(lambda : data_["fileformat"])):
        metadata_["fileformat"] = data_["fileformat"]
    # end if
    if (not php_empty(lambda : data_["video"]["dataformat"])):
        metadata_["dataformat"] = data_["video"]["dataformat"]
    # end if
    if (not php_empty(lambda : data_["video"]["encoder"])):
        metadata_["encoder"] = data_["video"]["encoder"]
    # end if
    if (not php_empty(lambda : data_["video"]["codec"])):
        metadata_["codec"] = data_["video"]["codec"]
    # end if
    if (not php_empty(lambda : data_["audio"])):
        data_["audio"]["streams"] = None
        metadata_["audio"] = data_["audio"]
    # end if
    if php_empty(lambda : metadata_["created_timestamp"]):
        created_timestamp_ = wp_get_media_creation_timestamp(data_)
        if False != created_timestamp_:
            metadata_["created_timestamp"] = created_timestamp_
        # end if
    # end if
    wp_add_id3_tag_data(metadata_, data_)
    file_format_ = metadata_["fileformat"] if (php_isset(lambda : metadata_["fileformat"])) else None
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
    return apply_filters("wp_read_video_metadata", metadata_, file_, file_format_, data_)
# end def wp_read_video_metadata
#// 
#// Retrieve metadata from an audio file's ID3 tags.
#// 
#// @since 3.6.0
#// 
#// @param string $file Path to file.
#// @return array|bool Returns array of metadata, if found.
#//
def wp_read_audio_metadata(file_=None, *_args_):
    
    
    if (not php_file_exists(file_)):
        return False
    # end if
    metadata_ = Array()
    if (not php_defined("GETID3_TEMP_DIR")):
        php_define("GETID3_TEMP_DIR", get_temp_dir())
    # end if
    if (not php_class_exists("getID3", False)):
        php_include_file(ABSPATH + WPINC + "/ID3/getid3.php", once=False)
    # end if
    id3_ = php_new_class("getID3", lambda : getID3())
    data_ = id3_.analyze(file_)
    if (not php_empty(lambda : data_["audio"])):
        data_["audio"]["streams"] = None
        metadata_ = data_["audio"]
    # end if
    if (not php_empty(lambda : data_["fileformat"])):
        metadata_["fileformat"] = data_["fileformat"]
    # end if
    if (not php_empty(lambda : data_["filesize"])):
        metadata_["filesize"] = php_int(data_["filesize"])
    # end if
    if (not php_empty(lambda : data_["mime_type"])):
        metadata_["mime_type"] = data_["mime_type"]
    # end if
    if (not php_empty(lambda : data_["playtime_seconds"])):
        metadata_["length"] = php_int(round(data_["playtime_seconds"]))
    # end if
    if (not php_empty(lambda : data_["playtime_string"])):
        metadata_["length_formatted"] = data_["playtime_string"]
    # end if
    if php_empty(lambda : metadata_["created_timestamp"]):
        created_timestamp_ = wp_get_media_creation_timestamp(data_)
        if False != created_timestamp_:
            metadata_["created_timestamp"] = created_timestamp_
        # end if
    # end if
    wp_add_id3_tag_data(metadata_, data_)
    return metadata_
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
def wp_get_media_creation_timestamp(metadata_=None, *_args_):
    
    
    creation_date_ = False
    if php_empty(lambda : metadata_["fileformat"]):
        return creation_date_
    # end if
    for case in Switch(metadata_["fileformat"]):
        if case("asf"):
            if (php_isset(lambda : metadata_["asf"]["file_properties_object"]["creation_date_unix"])):
                creation_date_ = php_int(metadata_["asf"]["file_properties_object"]["creation_date_unix"])
            # end if
            break
        # end if
        if case("matroska"):
            pass
        # end if
        if case("webm"):
            if (php_isset(lambda : metadata_["matroska"]["comments"]["creation_time"]["0"])):
                creation_date_ = strtotime(metadata_["matroska"]["comments"]["creation_time"]["0"])
            elif (php_isset(lambda : metadata_["matroska"]["info"]["0"]["DateUTC_unix"])):
                creation_date_ = php_int(metadata_["matroska"]["info"]["0"]["DateUTC_unix"])
            # end if
            break
        # end if
        if case("quicktime"):
            pass
        # end if
        if case("mp4"):
            if (php_isset(lambda : metadata_["quicktime"]["moov"]["subatoms"]["0"]["creation_time_unix"])):
                creation_date_ = php_int(metadata_["quicktime"]["moov"]["subatoms"]["0"]["creation_time_unix"])
            # end if
            break
        # end if
    # end for
    return creation_date_
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
def wp_media_attach_action(parent_id_=None, action_="attach", *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not parent_id_):
        return
    # end if
    if (not current_user_can("edit_post", parent_id_)):
        wp_die(__("Sorry, you are not allowed to edit this post."))
    # end if
    ids_ = Array()
    for att_id_ in PHP_REQUEST["media"]:
        att_id_ = php_int(att_id_)
        if (not current_user_can("edit_post", att_id_)):
            continue
        # end if
        ids_[-1] = att_id_
    # end for
    if (not php_empty(lambda : ids_)):
        ids_string_ = php_implode(",", ids_)
        if "attach" == action_:
            result_ = wpdb_.query(wpdb_.prepare(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_parent = %d WHERE post_type = 'attachment' AND ID IN ( ") + str(ids_string_) + str(" )"), parent_id_))
        else:
            result_ = wpdb_.query(str("UPDATE ") + str(wpdb_.posts) + str(" SET post_parent = 0 WHERE post_type = 'attachment' AND ID IN ( ") + str(ids_string_) + str(" )"))
        # end if
        for att_id_ in ids_:
            clean_attachment_cache(att_id_)
        # end for
    # end if
    if (php_isset(lambda : result_)):
        location_ = "upload.php"
        referer_ = wp_get_referer()
        if referer_:
            if False != php_strpos(referer_, "upload.php"):
                location_ = remove_query_arg(Array("attached", "detach"), referer_)
            # end if
        # end if
        key_ = "attached" if "attach" == action_ else "detach"
        location_ = add_query_arg(Array({key_: result_}), location_)
        wp_redirect(location_)
        php_exit(0)
    # end if
# end def wp_media_attach_action
