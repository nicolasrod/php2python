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
#// WordPress media templates.
#// 
#// @package WordPress
#// @subpackage Media
#// @since 3.5.0
#// 
#// 
#// Output the markup for a audio tag to be used in an Underscore template
#// when data.model is passed.
#// 
#// @since 3.9.0
#//
def wp_underscore_audio_template(*_args_):
    
    
    audio_types_ = wp_get_audio_extensions()
    php_print("""<audio style=\"visibility: hidden\"
    controls
class=\"wp-audio-shortcode\"
    width=\"{{ _.isUndefined( data.model.width ) ? 400 : data.model.width }}\"
    preload=\"{{ _.isUndefined( data.model.preload ) ? 'none' : data.model.preload }}\"
    <#
    """)
    for attr_ in Array("autoplay", "loop"):
        php_print(" if ( ! _.isUndefined( data.model.")
        php_print(attr_)
        php_print(" ) && data.model.")
        php_print(attr_)
        php_print(" ) {\n       #> ")
        php_print(attr_)
        php_print("<#\n }\n ")
    # end for
    php_print("""#>
    >
    <# if ( ! _.isEmpty( data.model.src ) ) { #>
    <source src=\"{{ data.model.src }}\" type=\"{{ wp.media.view.settings.embedMimes[ data.model.src.split('.').pop() ] }}\" />
    <# } #>
    """)
    for type_ in audio_types_:
        php_print(" <# if ( ! _.isEmpty( data.model.")
        php_print(type_)
        php_print(" ) ) { #>\n  <source src=\"{{ data.model.")
        php_print(type_)
        php_print(" }}\" type=\"{{ wp.media.view.settings.embedMimes[ '")
        php_print(type_)
        php_print("' ] }}\" />\n    <# } #>\n       ")
    # end for
    php_print("</audio>\n   ")
# end def wp_underscore_audio_template
#// 
#// Output the markup for a video tag to be used in an Underscore template
#// when data.model is passed.
#// 
#// @since 3.9.0
#//
def wp_underscore_video_template(*_args_):
    
    
    video_types_ = wp_get_video_extensions()
    php_print("""<#  var w_rule = '', classes = [],
    w, h, settings = wp.media.view.settings,
    isYouTube = isVimeo = false;
if ( ! _.isEmpty( data.model.src ) ) {
    isYouTube = data.model.src.match(/youtube|youtu\\.be/);
    isVimeo = -1 !== data.model.src.indexOf('vimeo');
    }
if ( settings.contentWidth && data.model.width >= settings.contentWidth ) {
    w = settings.contentWidth;
    } else {
    w = data.model.width;
    }
if ( w !== data.model.width ) {
    h = Math.ceil( ( data.model.height * w ) / data.model.width );
    } else {
    h = data.model.height;
    }
if ( w ) {
    w_rule = 'width: ' + w + 'px; ';
    }
if ( isYouTube ) {
    classes.push( 'youtube-video' );
    }
if ( isVimeo ) {
    classes.push( 'vimeo-video' );
    }
    #>
    <div style=\"{{ w_rule }}\" class=\"wp-video\">
    <video controls
class=\"wp-video-shortcode {{ classes.join( ' ' ) }}\"
    <# if ( w ) { #>width=\"{{ w }}\"<# } #>
    <# if ( h ) { #>height=\"{{ h }}\"<# } #>
    """)
    props_ = Array({"poster": "", "preload": "metadata"})
    for key_,value_ in props_:
        if php_empty(lambda : value_):
            php_print("     <#\n        if ( ! _.isUndefined( data.model.")
            php_print(key_)
            php_print(" ) && data.model.")
            php_print(key_)
            php_print(" ) {\n           #> ")
            php_print(key_)
            php_print("=\"{{ data.model.")
            php_print(key_)
            php_print(" }}\"<#\n        } #>\n          ")
        else:
            php_print(key_)
            php_print("         =\"{{ _.isUndefined( data.model.")
            php_print(key_)
            php_print(" ) ? '")
            php_print(value_)
            php_print("' : data.model.")
            php_print(key_)
            php_print(" }}\"\n          ")
        # end if
    # end for
    php_print(" <#\n    ")
    for attr_ in Array("autoplay", "loop"):
        php_print(" if ( ! _.isUndefined( data.model.")
        php_print(attr_)
        php_print(" ) && data.model.")
        php_print(attr_)
        php_print(" ) {\n       #> ")
        php_print(attr_)
        php_print("<#\n }\n ")
    # end for
    php_print("""#>
    >
    <# if ( ! _.isEmpty( data.model.src ) ) {
if ( isYouTube ) { #>
    <source src=\"{{ data.model.src }}\" type=\"video/youtube\" />
    <# } else if ( isVimeo ) { #>
    <source src=\"{{ data.model.src }}\" type=\"video/vimeo\" />
    <# } else { #>
    <source src=\"{{ data.model.src }}\" type=\"{{ settings.embedMimes[ data.model.src.split('.').pop() ] }}\" />
    <# }
    } #>
    """)
    for type_ in video_types_:
        php_print(" <# if ( data.model.")
        php_print(type_)
        php_print(" ) { #>\n    <source src=\"{{ data.model.")
        php_print(type_)
        php_print(" }}\" type=\"{{ settings.embedMimes[ '")
        php_print(type_)
        php_print("' ] }}\" />\n    <# } #>\n   ")
    # end for
    php_print("""   {{{ data.model.content }}}
    </video>
    </div>
    """)
# end def wp_underscore_video_template
#// 
#// Prints the templates used in the media manager.
#// 
#// @since 3.5.0
#// 
#// @global bool $is_IE
#//
def wp_print_media_templates(*_args_):
    
    
    global is_IE_
    php_check_if_defined("is_IE_")
    class_ = "media-modal wp-core-ui"
    if is_IE_ and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE 7") != False:
        class_ += " ie7"
    # end if
    alt_text_description_ = php_sprintf(__("<a href=\"%1$s\" %2$s>Describe the purpose of the image%3$s</a>. Leave empty if the image is purely decorative."), esc_url("https://www.w3.org/WAI/tutorials/images/decision-tree"), "target=\"_blank\" rel=\"noopener noreferrer\"", php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)")))
    php_print("\n   ")
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-media-frame\">\n       <div class=\"media-frame-title\" id=\"media-frame-title\"></div>\n      <h2 class=\"media-frame-menu-heading\">")
    _ex("Actions", "media modal menu actions")
    php_print("</h2>\n      <button type=\"button\" class=\"button button-link media-frame-menu-toggle\" aria-expanded=\"false\">\n         ")
    _ex("Menu", "media modal menu")
    php_print("""           <span class=\"dashicons dashicons-arrow-down\" aria-hidden=\"true\"></span>
    </button>
    <div class=\"media-frame-menu\"></div>
    <div class=\"media-frame-tab-panel\">
    <div class=\"media-frame-router\"></div>
    <div class=\"media-frame-content\"></div>
    </div>
    <h2 class=\"media-frame-actions-heading screen-reader-text\">
    """)
    #// translators: Accessibility text.
    _e("Selected media actions")
    php_print("""       </h2>
    <div class=\"media-frame-toolbar\"></div>
    <div class=\"media-frame-uploader\"></div>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-media-modal\">\n       <div tabindex=\"0\" class=\"")
    php_print(class_)
    php_print("\" role=\"dialog\" aria-labelledby=\"media-frame-title\">\n          <# if ( data.hasCloseButton ) { #>\n                <button type=\"button\" class=\"media-modal-close\"><span class=\"media-modal-icon\"><span class=\"screen-reader-text\">")
    _e("Close dialog")
    php_print("""</span></span></button>
    <# } #>
    <div class=\"media-modal-content\" role=\"document\"></div>
    </div>
    <div class=\"media-modal-backdrop\"></div>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-uploader-window\">\n       <div class=\"uploader-window-content\">\n           <div class=\"uploader-editor-title\">")
    _e("Drop files to upload")
    php_print("""</div>
    </div>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-uploader-editor\">\n       <div class=\"uploader-editor-content\">\n           <div class=\"uploader-editor-title\">")
    _e("Drop files to upload")
    php_print("""</div>
    </div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-uploader-inline\">
    <# var messageClass = data.message ? 'has-upload-message' : 'no-upload-message'; #>
    <# if ( data.canClose ) { #>
    <button class=\"close dashicons dashicons-no\"><span class=\"screen-reader-text\">""")
    _e("Close uploader")
    php_print("""</span></button>
    <# } #>
    <div class=\"uploader-inline-content {{ messageClass }}\">
    <# if ( data.message ) { #>
    <h2 class=\"upload-message\">{{ data.message }}</h2>
    <# } #>
    """)
    if (not _device_can_upload()):
        php_print("         <div class=\"upload-ui\">\n             <h2 class=\"upload-instructions\">")
        _e("Your browser cannot upload files")
        php_print("</h2>\n              <p>\n               ")
        printf(__("The web browser on your device cannot be used to upload files. You may be able to use the <a href=\"%s\">native app for your device</a> instead."), "https://apps.wordpress.org/")
        php_print("             </p>\n          </div>\n        ")
    elif is_multisite() and (not is_upload_space_available()):
        php_print("         <div class=\"upload-ui\">\n             <h2 class=\"upload-instructions\">")
        _e("Upload Limit Exceeded")
        php_print("</h2>\n              ")
        #// This action is documented in wp-admin/includes/media.php
        do_action("upload_ui_over_quota")
        php_print("         </div>\n        ")
    else:
        php_print("         <div class=\"upload-ui\">\n             <h2 class=\"upload-instructions drop-instructions\">")
        _e("Drop files to upload")
        php_print("</h2>\n              <p class=\"upload-instructions drop-instructions\">")
        _ex("or", "Uploader: Drop files here - or - Select Files")
        php_print("</p>\n               <button type=\"button\" class=\"browser button button-hero\">")
        _e("Select Files")
        php_print("""</button>
        </div>
        <div class=\"upload-inline-status\"></div>
        <div class=\"post-upload-ui\">
        """)
        #// This action is documented in wp-admin/includes/media.php
        do_action("pre-upload-ui")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        #// This action is documented in wp-admin/includes/media.php
        do_action("pre-plupload-upload-ui")
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        if 10 == remove_action("post-plupload-upload-ui", "media_upload_flash_bypass"):
            #// This action is documented in wp-admin/includes/media.php
            do_action("post-plupload-upload-ui")
            #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
            add_action("post-plupload-upload-ui", "media_upload_flash_bypass")
        else:
            #// This action is documented in wp-admin/includes/media.php
            do_action("post-plupload-upload-ui")
            pass
        # end if
        max_upload_size_ = wp_max_upload_size()
        if (not max_upload_size_):
            max_upload_size_ = 0
        # end if
        php_print("\n               <p class=\"max-upload-size\">\n             ")
        printf(__("Maximum upload file size: %s."), esc_html(size_format(max_upload_size_)))
        php_print("""               </p>
        <# if ( data.suggestedWidth && data.suggestedHeight ) { #>
        <p class=\"suggested-dimensions\">
        """)
        #// translators: 1: Suggested width number, 2: Suggested height number.
        printf(__("Suggested image dimensions: %1$s by %2$s pixels."), "{{data.suggestedWidth}}", "{{data.suggestedHeight}}")
        php_print("""                   </p>
        <# } #>
        """)
        #// This action is documented in wp-admin/includes/media.php
        do_action("post-upload-ui")
        pass
        php_print("         </div>\n        ")
    # end if
    php_print("""       </div>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-media-library-view-switcher\">\n       <a href=\"")
    php_print(esc_url(add_query_arg("mode", "list", PHP_SERVER["REQUEST_URI"])))
    php_print("\" class=\"view-list\">\n            <span class=\"screen-reader-text\">")
    _e("List View")
    php_print("</span>\n        </a>\n      <a href=\"")
    php_print(esc_url(add_query_arg("mode", "grid", PHP_SERVER["REQUEST_URI"])))
    php_print("\" class=\"view-grid current\" aria-current=\"page\">\n          <span class=\"screen-reader-text\">")
    _e("Grid View")
    php_print("""</span>
    </a>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-uploader-status\">\n       <h2>")
    _e("Uploading")
    php_print("</h2>\n      <button type=\"button\" class=\"button-link upload-dismiss-errors\"><span class=\"screen-reader-text\">")
    _e("Dismiss Errors")
    php_print("""</span></button>
    <div class=\"media-progress-bar\"><div></div></div>
    <div class=\"upload-details\">
    <span class=\"upload-count\">
    <span class=\"upload-index\"></span> / <span class=\"upload-total\"></span>
    </span>
    <span class=\"upload-detail-separator\">&ndash;</span>
    <span class=\"upload-filename\"></span>
    </div>
    <div class=\"upload-errors\"></div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-uploader-status-error\">
    <span class=\"upload-error-filename\">{{{ data.filename }}}</span>
    <span class=\"upload-error-message\">{{ data.message }}</span>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-edit-attachment-frame\">\n     <div class=\"edit-media-header\">\n         <button class=\"left dashicons\"<# if ( ! data.hasPrevious ) { #> disabled<# } #>><span class=\"screen-reader-text\">")
    _e("Edit previous media item")
    php_print("</span></button>\n           <button class=\"right dashicons\"<# if ( ! data.hasNext ) { #> disabled<# } #>><span class=\"screen-reader-text\">")
    _e("Edit next media item")
    php_print("</span></button>\n           <button type=\"button\" class=\"media-modal-close\"><span class=\"media-modal-icon\"><span class=\"screen-reader-text\">")
    _e("Close dialog")
    php_print("""</span></span></button>
    </div>
    <div class=\"media-frame-title\"></div>
    <div class=\"media-frame-content\"></div>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-attachment-details-two-column\">\n     <div class=\"attachment-media-view {{ data.orientation }}\">\n          <h2 class=\"screen-reader-text\">")
    _e("Attachment Preview")
    php_print("""</h2>
    <div class=\"thumbnail thumbnail-{{ data.type }}\">
    <# if ( data.uploading ) { #>
    <div class=\"media-progress-bar\"><div></div></div>
    <# } else if ( data.sizes && data.sizes.large ) { #>
    <img class=\"details-image\" src=\"{{ data.sizes.large.url }}\" draggable=\"false\" alt=\"\" />
    <# } else if ( data.sizes && data.sizes.full ) { #>
    <img class=\"details-image\" src=\"{{ data.sizes.full.url }}\" draggable=\"false\" alt=\"\" />
    <# } else if ( -1 === jQuery.inArray( data.type, [ 'audio', 'video' ] ) ) { #>
    <img class=\"details-image icon\" src=\"{{ data.icon }}\" draggable=\"false\" alt=\"\" />
    <# } #>
    <# if ( 'audio' === data.type ) { #>
    <div class=\"wp-media-wrapper\">
    <audio style=\"visibility: hidden\" controls class=\"wp-audio-shortcode\" width=\"100%\" preload=\"none\">
    <source type=\"{{ data.mime }}\" src=\"{{ data.url }}\"/>
    </audio>
    </div>
    <# } else if ( 'video' === data.type ) {
    var w_rule = '';
if ( data.width ) {
    w_rule = 'width: ' + data.width + 'px;';
    } else if ( wp.media.view.settings.contentWidth ) {
    w_rule = 'width: ' + wp.media.view.settings.contentWidth + 'px;';
    }
    #>
    <div style=\"{{ w_rule }}\" class=\"wp-media-wrapper wp-video\">
    <video controls=\"controls\" class=\"wp-video-shortcode\" preload=\"metadata\"
    <# if ( data.width ) { #>width=\"{{ data.width }}\"<# } #>
    <# if ( data.height ) { #>height=\"{{ data.height }}\"<# } #>
    <# if ( data.image && data.image.src !== data.icon ) { #>poster=\"{{ data.image.src }}\"<# } #>>
    <source type=\"{{ data.mime }}\" src=\"{{ data.url }}\"/>
    </video>
    </div>
    <# } #>
    <div class=\"attachment-actions\">
    <# if ( 'image' === data.type && ! data.uploading && data.sizes && data.can.save ) { #>
    <button type=\"button\" class=\"button edit-attachment\">""")
    _e("Edit Image")
    php_print("</button>\n                  <# } else if ( 'pdf' === data.subtype && data.sizes ) { #>\n                    <p>")
    _e("Document Preview")
    php_print("""</p>
    <# } #>
    </div>
    </div>
    </div>
    <div class=\"attachment-info\">
    <span class=\"settings-save-status\" role=\"status\">
    <span class=\"spinner\"></span>
    <span class=\"saved\">""")
    esc_html_e("Saved.")
    php_print("""</span>
    </span>
    <div class=\"details\">
    <h2 class=\"screen-reader-text\">""")
    _e("Details")
    php_print("</h2>\n              <div class=\"filename\"><strong>")
    _e("File name:")
    php_print("</strong> {{ data.filename }}</div>\n                <div class=\"filename\"><strong>")
    _e("File type:")
    php_print("</strong> {{ data.mime }}</div>\n                <div class=\"uploaded\"><strong>")
    _e("Uploaded on:")
    php_print("</strong> {{ data.dateFormatted }}</div>\n\n             <div class=\"file-size\"><strong>")
    _e("File size:")
    php_print("""</strong> {{ data.filesizeHumanReadable }}</div>
    <# if ( 'image' === data.type && ! data.uploading ) { #>
    <# if ( data.width && data.height ) { #>
    <div class=\"dimensions\"><strong>""")
    _e("Dimensions:")
    php_print("</strong>\n                          ")
    #// translators: 1: A number of pixels wide, 2: A number of pixels tall.
    printf(__("%1$s by %2$s pixels"), "{{ data.width }}", "{{ data.height }}")
    php_print("""                       </div>
    <# } #>
    <# if ( data.originalImageURL && data.originalImageName ) { #>
    """)
    _e("Original image:")
    php_print("""                       <a href=\"{{ data.originalImageURL }}\">{{data.originalImageName}}</a>
    <# } #>
    <# } #>
    <# if ( data.fileLength && data.fileLengthHumanReadable ) { #>
    <div class=\"file-length\"><strong>""")
    _e("Length:")
    php_print("""</strong>
    <span aria-hidden=\"true\">{{ data.fileLength }}</span>
    <span class=\"screen-reader-text\">{{ data.fileLengthHumanReadable }}</span>
    </div>
    <# } #>
    <# if ( 'audio' === data.type && data.meta.bitrate ) { #>
    <div class=\"bitrate\">
    <strong>""")
    _e("Bitrate:")
    php_print("""</strong> {{ Math.round( data.meta.bitrate / 1000 ) }}kb/s
    <# if ( data.meta.bitrate_mode ) { #>
    {{ ' ' + data.meta.bitrate_mode.toUpperCase() }}
    <# } #>
    </div>
    <# } #>
    <div class=\"compat-meta\">
    <# if ( data.compat && data.compat.meta ) { #>
    {{{ data.compat.meta }}}
    <# } #>
    </div>
    </div>
    <div class=\"settings\">
    <# var maybeReadOnly = data.can.save || data.allowLocalEdits ? '' : 'readonly'; #>
    <# if ( 'image' === data.type ) { #>
    <span class=\"setting has-description\" data-setting=\"alt\">
    <label for=\"attachment-details-two-column-alt-text\" class=\"name\">""")
    _e("Alternative Text")
    php_print("""</label>
    <input type=\"text\" id=\"attachment-details-two-column-alt-text\" value=\"{{ data.alt }}\" aria-describedby=\"alt-text-description\" {{ maybeReadOnly }} />
    </span>
    <p class=\"description\" id=\"alt-text-description\">""")
    php_print(alt_text_description_)
    php_print("</p>\n               <# } #>\n               ")
    if post_type_supports("attachment", "title"):
        php_print("             <span class=\"setting\" data-setting=\"title\">\n                   <label for=\"attachment-details-two-column-title\" class=\"name\">")
        _e("Title")
        php_print("""</label>
        <input type=\"text\" id=\"attachment-details-two-column-title\" value=\"{{ data.title }}\" {{ maybeReadOnly }} />
        </span>
        """)
    # end if
    php_print("             <# if ( 'audio' === data.type ) { #>\n              ")
    for key_,label_ in Array({"artist": __("Artist"), "album": __("Album")}):
        php_print("             <span class=\"setting\" data-setting=\"")
        php_print(esc_attr(key_))
        php_print("\">\n                    <label for=\"attachment-details-two-column-")
        php_print(esc_attr(key_))
        php_print("\" class=\"name\">")
        php_print(label_)
        php_print("</label>\n                   <input type=\"text\" id=\"attachment-details-two-column-")
        php_print(esc_attr(key_))
        php_print("\" value=\"{{ data.")
        php_print(key_)
        php_print(" || data.meta.")
        php_print(key_)
        php_print(" || '' }}\" />\n             </span>\n               ")
    # end for
    php_print("             <# } #>\n               <span class=\"setting\" data-setting=\"caption\">\n                 <label for=\"attachment-details-two-column-caption\" class=\"name\">")
    _e("Caption")
    php_print("""</label>
    <textarea id=\"attachment-details-two-column-caption\" {{ maybeReadOnly }}>{{ data.caption }}</textarea>
    </span>
    <span class=\"setting\" data-setting=\"description\">
    <label for=\"attachment-details-two-column-description\" class=\"name\">""")
    _e("Description")
    php_print("""</label>
    <textarea id=\"attachment-details-two-column-description\" {{ maybeReadOnly }}>{{ data.description }}</textarea>
    </span>
    <span class=\"setting\">
    <span class=\"name\">""")
    _e("Uploaded By")
    php_print("""</span>
    <span class=\"value\">{{ data.authorName }}</span>
    </span>
    <# if ( data.uploadedToTitle ) { #>
    <span class=\"setting\">
    <span class=\"name\">""")
    _e("Uploaded To")
    php_print("""</span>
    <# if ( data.uploadedToLink ) { #>
    <span class=\"value\"><a href=\"{{ data.uploadedToLink }}\">{{ data.uploadedToTitle }}</a></span>
    <# } else { #>
    <span class=\"value\">{{ data.uploadedToTitle }}</span>
    <# } #>
    </span>
    <# } #>
    <span class=\"setting\" data-setting=\"url\">
    <label for=\"attachment-details-two-column-copy-link\" class=\"name\">""")
    _e("Copy Link")
    php_print("""</label>
    <input type=\"text\" id=\"attachment-details-two-column-copy-link\" value=\"{{ data.url }}\" readonly />
    </span>
    <div class=\"attachment-compat\"></div>
    </div>
    <div class=\"actions\">
    <a class=\"view-attachment\" href=\"{{ data.link }}\">""")
    _e("View attachment page")
    php_print("</a>\n               <# if ( data.can.save ) { #> |\n                    <a href=\"{{ data.editLink }}\">")
    _e("Edit more details")
    php_print("""</a>
    <# } #>
    <# if ( ! data.uploading && data.can.remove ) { #> |
    """)
    if MEDIA_TRASH:
        php_print("                     <# if ( 'trash' === data.status ) { #>\n                            <button type=\"button\" class=\"button-link untrash-attachment\">")
        _e("Restore from Trash")
        php_print("</button>\n                      <# } else { #>\n                            <button type=\"button\" class=\"button-link trash-attachment\">")
        _e("Move to Trash")
        php_print("</button>\n                      <# } #>\n                   ")
    else:
        php_print("                     <button type=\"button\" class=\"button-link delete-attachment\">")
        _e("Delete Permanently")
        php_print("</button>\n                  ")
    # end if
    php_print("""               <# } #>
    </div>
    </div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-attachment\">
    <div class=\"attachment-preview js--select-attachment type-{{ data.type }} subtype-{{ data.subtype }} {{ data.orientation }}\">
    <div class=\"thumbnail\">
    <# if ( data.uploading ) { #>
    <div class=\"media-progress-bar\"><div style=\"width: {{ data.percent }}%\"></div></div>
    <# } else if ( 'image' === data.type && data.sizes ) { #>
    <div class=\"centered\">
    <img src=\"{{ data.size.url }}\" draggable=\"false\" alt=\"\" />
    </div>
    <# } else { #>
    <div class=\"centered\">
    <# if ( data.image && data.image.src && data.image.src !== data.icon ) { #>
    <img src=\"{{ data.image.src }}\" class=\"thumbnail\" draggable=\"false\" alt=\"\" />
    <# } else if ( data.sizes && data.sizes.medium ) { #>
    <img src=\"{{ data.sizes.medium.url }}\" class=\"thumbnail\" draggable=\"false\" alt=\"\" />
    <# } else { #>
    <img src=\"{{ data.icon }}\" class=\"icon\" draggable=\"false\" alt=\"\" />
    <# } #>
    </div>
    <div class=\"filename\">
    <div>{{ data.filename }}</div>
    </div>
    <# } #>
    </div>
    <# if ( data.buttons.close ) { #>
    <button type=\"button\" class=\"button-link attachment-close media-modal-icon\"><span class=\"screen-reader-text\">""")
    _e("Remove")
    php_print("""</span></button>
    <# } #>
    </div>
    <# if ( data.buttons.check ) { #>
    <button type=\"button\" class=\"check\" tabindex=\"-1\"><span class=\"media-modal-icon\"></span><span class=\"screen-reader-text\">""")
    _e("Deselect")
    php_print("""</span></button>
    <# } #>
    <#
    var maybeReadOnly = data.can.save || data.allowLocalEdits ? '' : 'readonly';
if ( data.describe ) {
if ( 'image' === data.type ) { #>
    <input type=\"text\" value=\"{{ data.caption }}\" class=\"describe\" data-setting=\"caption\"
    aria-label=\"""")
    esc_attr_e("Caption")
    php_print("\"\n                 placeholder=\"")
    esc_attr_e("Caption&hellip;")
    php_print("""\" {{ maybeReadOnly }} />
    <# } else { #>
    <input type=\"text\" value=\"{{ data.title }}\" class=\"describe\" data-setting=\"title\"
    <# if ( 'video' === data.type ) { #>
    aria-label=\"""")
    esc_attr_e("Video title")
    php_print("\"\n                     placeholder=\"")
    esc_attr_e("Video title&hellip;")
    php_print("\"\n                 <# } else if ( 'audio' === data.type ) { #>\n                       aria-label=\"")
    esc_attr_e("Audio title")
    php_print("\"\n                     placeholder=\"")
    esc_attr_e("Audio title&hellip;")
    php_print("\"\n                 <# } else { #>\n                        aria-label=\"")
    esc_attr_e("Media title")
    php_print("\"\n                     placeholder=\"")
    esc_attr_e("Media title&hellip;")
    php_print("""\"
    <# } #> {{ maybeReadOnly }} />
    <# }
    } #>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-attachment-details\">\n        <h2>\n          ")
    _e("Attachment Details")
    php_print("         <span class=\"settings-save-status\" role=\"status\">\n             <span class=\"spinner\"></span>\n               <span class=\"saved\">")
    esc_html_e("Saved.")
    php_print("""</span>
    </span>
    </h2>
    <div class=\"attachment-info\">
    <div class=\"thumbnail thumbnail-{{ data.type }}\">
    <# if ( data.uploading ) { #>
    <div class=\"media-progress-bar\"><div></div></div>
    <# } else if ( 'image' === data.type && data.sizes ) { #>
    <img src=\"{{ data.size.url }}\" draggable=\"false\" alt=\"\" />
    <# } else { #>
    <img src=\"{{ data.icon }}\" class=\"icon\" draggable=\"false\" alt=\"\" />
    <# } #>
    </div>
    <div class=\"details\">
    <div class=\"filename\">{{ data.filename }}</div>
    <div class=\"uploaded\">{{ data.dateFormatted }}</div>
    <div class=\"file-size\">{{ data.filesizeHumanReadable }}</div>
    <# if ( 'image' === data.type && ! data.uploading ) { #>
    <# if ( data.width && data.height ) { #>
    <div class=\"dimensions\">
    """)
    #// translators: 1: A number of pixels wide, 2: A number of pixels tall.
    printf(__("%1$s by %2$s pixels"), "{{ data.width }}", "{{ data.height }}")
    php_print("""                       </div>
    <# } #>
    <# if ( data.originalImageURL && data.originalImageName ) { #>
    """)
    _e("Original image:")
    php_print("""                       <a href=\"{{ data.originalImageURL }}\">{{data.originalImageName}}</a>
    <# } #>
    <# if ( data.can.save && data.sizes ) { #>
    <a class=\"edit-attachment\" href=\"{{ data.editLink }}&amp;image-editor\" target=\"_blank\">""")
    _e("Edit Image")
    php_print("""</a>
    <# } #>
    <# } #>
    <# if ( data.fileLength && data.fileLengthHumanReadable ) { #>
    <div class=\"file-length\">""")
    _e("Length:")
    php_print("""                       <span aria-hidden=\"true\">{{ data.fileLength }}</span>
    <span class=\"screen-reader-text\">{{ data.fileLengthHumanReadable }}</span>
    </div>
    <# } #>
    <# if ( ! data.uploading && data.can.remove ) { #>
    """)
    if MEDIA_TRASH:
        php_print("                 <# if ( 'trash' === data.status ) { #>\n                        <button type=\"button\" class=\"button-link untrash-attachment\">")
        _e("Restore from Trash")
        php_print("</button>\n                  <# } else { #>\n                        <button type=\"button\" class=\"button-link trash-attachment\">")
        _e("Move to Trash")
        php_print("</button>\n                  <# } #>\n                   ")
    else:
        php_print("                     <button type=\"button\" class=\"button-link delete-attachment\">")
        _e("Delete Permanently")
        php_print("</button>\n                  ")
    # end if
    php_print("""               <# } #>
    <div class=\"compat-meta\">
    <# if ( data.compat && data.compat.meta ) { #>
    {{{ data.compat.meta }}}
    <# } #>
    </div>
    </div>
    </div>
    <# var maybeReadOnly = data.can.save || data.allowLocalEdits ? '' : 'readonly'; #>
    <# if ( 'image' === data.type ) { #>
    <span class=\"setting has-description\" data-setting=\"alt\">
    <label for=\"attachment-details-alt-text\" class=\"name\">""")
    _e("Alt Text")
    php_print("""</label>
    <input type=\"text\" id=\"attachment-details-alt-text\" value=\"{{ data.alt }}\" aria-describedby=\"alt-text-description\" {{ maybeReadOnly }} />
    </span>
    <p class=\"description\" id=\"alt-text-description\">""")
    php_print(alt_text_description_)
    php_print("</p>\n       <# } #>\n       ")
    if post_type_supports("attachment", "title"):
        php_print("     <span class=\"setting\" data-setting=\"title\">\n           <label for=\"attachment-details-title\" class=\"name\">")
        _e("Title")
        php_print("""</label>
        <input type=\"text\" id=\"attachment-details-title\" value=\"{{ data.title }}\" {{ maybeReadOnly }} />
        </span>
        """)
    # end if
    php_print("     <# if ( 'audio' === data.type ) { #>\n      ")
    for key_,label_ in Array({"artist": __("Artist"), "album": __("Album")}):
        php_print("     <span class=\"setting\" data-setting=\"")
        php_print(esc_attr(key_))
        php_print("\">\n            <label for=\"attachment-details-")
        php_print(esc_attr(key_))
        php_print("\" class=\"name\">")
        php_print(label_)
        php_print("</label>\n           <input type=\"text\" id=\"attachment-details-")
        php_print(esc_attr(key_))
        php_print("\" value=\"{{ data.")
        php_print(key_)
        php_print(" || data.meta.")
        php_print(key_)
        php_print(" || '' }}\" />\n     </span>\n       ")
    # end for
    php_print("     <# } #>\n       <span class=\"setting\" data-setting=\"caption\">\n         <label for=\"attachment-details-caption\" class=\"name\">")
    _e("Caption")
    php_print("""</label>
    <textarea id=\"attachment-details-caption\" {{ maybeReadOnly }}>{{ data.caption }}</textarea>
    </span>
    <span class=\"setting\" data-setting=\"description\">
    <label for=\"attachment-details-description\" class=\"name\">""")
    _e("Description")
    php_print("""</label>
    <textarea id=\"attachment-details-description\" {{ maybeReadOnly }}>{{ data.description }}</textarea>
    </span>
    <span class=\"setting\" data-setting=\"url\">
    <label for=\"attachment-details-copy-link\" class=\"name\">""")
    _e("Copy Link")
    php_print("""</label>
    <input type=\"text\" id=\"attachment-details-copy-link\" value=\"{{ data.url }}\" readonly />
    </span>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-media-selection\">
    <div class=\"selection-info\">
    <span class=\"count\"></span>
    <# if ( data.editable ) { #>
    <button type=\"button\" class=\"button-link edit-selection\">""")
    _e("Edit Selection")
    php_print("""</button>
    <# } #>
    <# if ( data.clearable ) { #>
    <button type=\"button\" class=\"button-link clear-selection\">""")
    _e("Clear")
    php_print("""</button>
    <# } #>
    </div>
    <div class=\"selection-view\"></div>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-attachment-display-settings\">\n       <h2>")
    _e("Attachment Display Settings")
    php_print("""</h2>
    <# if ( 'image' === data.type ) { #>
    <span class=\"setting align\">
    <label for=\"attachment-display-settings-alignment\" class=\"name\">""")
    _e("Alignment")
    php_print("""</label>
    <select id=\"attachment-display-settings-alignment\" class=\"alignment\"
    data-setting=\"align\"
    <# if ( data.userSettings ) { #>
    data-user-setting=\"align\"
    <# } #>>
    <option value=\"left\">
    """)
    esc_html_e("Left")
    php_print("                 </option>\n                 <option value=\"center\">\n                     ")
    esc_html_e("Center")
    php_print("                 </option>\n                 <option value=\"right\">\n                      ")
    esc_html_e("Right")
    php_print("                 </option>\n                 <option value=\"none\" selected>\n                      ")
    esc_html_e("None")
    php_print("""                   </option>
    </select>
    </span>
    <# } #>
    <span class=\"setting\">
    <label for=\"attachment-display-settings-link-to\" class=\"name\">
    <# if ( data.model.canEmbed ) { #>
    """)
    _e("Embed or Link")
    php_print("             <# } else { #>\n                    ")
    _e("Link To")
    php_print("""               <# } #>
    </label>
    <select id=\"attachment-display-settings-link-to\" class=\"link-to\"
    data-setting=\"link\"
    <# if ( data.userSettings && ! data.model.canEmbed ) { #>
    data-user-setting=\"urlbutton\"
    <# } #>>
    <# if ( data.model.canEmbed ) { #>
    <option value=\"embed\" selected>
    """)
    esc_html_e("Embed Media Player")
    php_print("""               </option>
    <option value=\"file\">
    <# } else { #>
    <option value=\"none\" selected>
    """)
    esc_html_e("None")
    php_print("""               </option>
    <option value=\"file\">
    <# } #>
    <# if ( data.model.canEmbed ) { #>
    """)
    esc_html_e("Link to Media File")
    php_print("             <# } else { #>\n                    ")
    esc_html_e("Media File")
    php_print("""               <# } #>
    </option>
    <option value=\"post\">
    <# if ( data.model.canEmbed ) { #>
    """)
    esc_html_e("Link to Attachment Page")
    php_print("             <# } else { #>\n                    ")
    esc_html_e("Attachment Page")
    php_print("""               <# } #>
    </option>
    <# if ( 'image' === data.type ) { #>
    <option value=\"custom\">
    """)
    esc_html_e("Custom URL")
    php_print("""               </option>
    <# } #>
    </select>
    </span>
    <span class=\"setting\">
    <label for=\"attachment-display-settings-link-to-custom\" class=\"name\">""")
    _e("URL")
    php_print("""</label>
    <input type=\"text\" id=\"attachment-display-settings-link-to-custom\" class=\"link-to-custom\" data-setting=\"linkUrl\" />
    </span>
    <# if ( 'undefined' !== typeof data.sizes ) { #>
    <span class=\"setting\">
    <label for=\"attachment-display-settings-size\" class=\"name\">""")
    _e("Size")
    php_print("""</label>
    <select id=\"attachment-display-settings-size\" class=\"size\" name=\"size\"
    data-setting=\"size\"
    <# if ( data.userSettings ) { #>
    data-user-setting=\"imgsize\"
    <# } #>>
    """)
    #// This filter is documented in wp-admin/includes/media.php
    sizes_ = apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")}))
    for value_,name_ in sizes_:
        php_print("                     <#\n                        var size = data.sizes['")
        php_print(esc_js(value_))
        php_print("'];\n                        if ( size ) { #>\n                          <option value=\"")
        php_print(esc_attr(value_))
        php_print("\" ")
        selected(value_, "full")
        php_print(">\n                              ")
        php_print(esc_html(name_))
        php_print(""" &ndash; {{ size.width }} &times; {{ size.height }}
        </option>
        <# } #>
        """)
    # end for
    php_print("""               </select>
    </span>
    <# } #>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-gallery-settings\">\n      <h2>")
    _e("Gallery Settings")
    php_print("""</h2>
    <span class=\"setting\">
    <label for=\"gallery-settings-link-to\" class=\"name\">""")
    _e("Link To")
    php_print("""</label>
    <select id=\"gallery-settings-link-to\" class=\"link-to\"
    data-setting=\"link\"
    <# if ( data.userSettings ) { #>
    data-user-setting=\"urlbutton\"
    <# } #>>
    <option value=\"post\" <# if ( ! wp.media.galleryDefaults.link || 'post' == wp.media.galleryDefaults.link ) {
    #>selected=\"selected\"<# }
    #>>
    """)
    esc_html_e("Attachment Page")
    php_print("             </option>\n             <option value=\"file\" <# if ( 'file' == wp.media.galleryDefaults.link ) { #>selected=\"selected\"<# } #>>\n                    ")
    esc_html_e("Media File")
    php_print("             </option>\n             <option value=\"none\" <# if ( 'none' == wp.media.galleryDefaults.link ) { #>selected=\"selected\"<# } #>>\n                    ")
    esc_html_e("None")
    php_print("""               </option>
    </select>
    </span>
    <span class=\"setting\">
    <label for=\"gallery-settings-columns\" class=\"name select-label-inline\">""")
    _e("Columns")
    php_print("""</label>
    <select id=\"gallery-settings-columns\" class=\"columns\" name=\"columns\"
    data-setting=\"columns\">
    """)
    i_ = 1
    while i_ <= 9:
        
        php_print("                 <option value=\"")
        php_print(esc_attr(i_))
        php_print("\" <#\n                      if ( ")
        php_print(i_)
        php_print(" == wp.media.galleryDefaults.columns ) { #>selected=\"selected\"<# }\n                   #>>\n                       ")
        php_print(esc_html(i_))
        php_print("                 </option>\n             ")
        i_ += 1
    # end while
    php_print("""           </select>
    </span>
    <span class=\"setting\">
    <input type=\"checkbox\" id=\"gallery-settings-random-order\" data-setting=\"_orderbyRandom\" />
    <label for=\"gallery-settings-random-order\" class=\"checkbox-label-inline\">""")
    _e("Random Order")
    php_print("""</label>
    </span>
    <span class=\"setting size\">
    <label for=\"gallery-settings-size\" class=\"name\">""")
    _e("Size")
    php_print("""</label>
    <select id=\"gallery-settings-size\" class=\"size\" name=\"size\"
    data-setting=\"size\"
    <# if ( data.userSettings ) { #>
    data-user-setting=\"imgsize\"
    <# } #>
    >
    """)
    #// This filter is documented in wp-admin/includes/media.php
    size_names_ = apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")}))
    for size_,label_ in size_names_:
        php_print("                 <option value=\"")
        php_print(esc_attr(size_))
        php_print("\">\n                        ")
        php_print(esc_html(label_))
        php_print("                 </option>\n             ")
    # end for
    php_print("""           </select>
    </span>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-playlist-settings\">\n     <h2>")
    _e("Playlist Settings")
    php_print("""</h2>
    <# var emptyModel = _.isEmpty( data.model ),
    isVideo = 'video' === data.controller.get('library').props.get('type'); #>
    <span class=\"setting\">
    <input type=\"checkbox\" id=\"playlist-settings-show-list\" data-setting=\"tracklist\" <# if ( emptyModel ) { #>
    checked=\"checked\"
    <# } #> />
    <label for=\"playlist-settings-show-list\" class=\"checkbox-label-inline\">
    <# if ( isVideo ) { #>
    """)
    _e("Show Video List")
    php_print("             <# } else { #>\n                ")
    _e("Show Tracklist")
    php_print("""               <# } #>
    </label>
    </span>
    <# if ( ! isVideo ) { #>
    <span class=\"setting\">
    <input type=\"checkbox\" id=\"playlist-settings-show-artist\" data-setting=\"artists\" <# if ( emptyModel ) { #>
    checked=\"checked\"
    <# } #> />
    <label for=\"playlist-settings-show-artist\" class=\"checkbox-label-inline\">
    """)
    _e("Show Artist Name in Tracklist")
    php_print("""           </label>
    </span>
    <# } #>
    <span class=\"setting\">
    <input type=\"checkbox\" id=\"playlist-settings-show-images\" data-setting=\"images\" <# if ( emptyModel ) { #>
    checked=\"checked\"
    <# } #> />
    <label for=\"playlist-settings-show-images\" class=\"checkbox-label-inline\">
    """)
    _e("Show Images")
    php_print("""           </label>
    </span>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-embed-link-settings\">\n       <span class=\"setting link-text\">\n            <label for=\"embed-link-settings-link-text\" class=\"name\">")
    _e("Link Text")
    php_print("""</label>
    <input type=\"text\" id=\"embed-link-settings-link-text\" class=\"alignment\" data-setting=\"linkText\" />
    </span>
    <div class=\"embed-container\" style=\"display: none;\">
    <div class=\"embed-preview\"></div>
    </div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-embed-image-settings\">
    <div class=\"wp-clearfix\">
    <div class=\"thumbnail\">
    <img src=\"{{ data.model.url }}\" draggable=\"false\" alt=\"\" />
    </div>
    </div>
    <span class=\"setting alt-text has-description\">
    <label for=\"embed-image-settings-alt-text\" class=\"name\">""")
    _e("Alternative Text")
    php_print("""</label>
    <input type=\"text\" id=\"embed-image-settings-alt-text\" data-setting=\"alt\" aria-describedby=\"alt-text-description\" />
    </span>
    <p class=\"description\" id=\"alt-text-description\">""")
    php_print(alt_text_description_)
    php_print("</p>\n\n     ")
    #// This filter is documented in wp-admin/includes/media.php
    if (not apply_filters("disable_captions", "")):
        php_print("         <span class=\"setting caption\">\n              <label for=\"embed-image-settings-caption\" class=\"name\">")
        _e("Caption")
        php_print("""</label>
        <textarea id=\"embed-image-settings-caption\" data-setting=\"caption\" />
        </span>
        """)
    # end if
    php_print("\n       <fieldset class=\"setting-group\">\n            <legend class=\"name\">")
    _e("Align")
    php_print("""</legend>
    <span class=\"setting align\">
    <span class=\"button-group button-large\" data-setting=\"align\">
    <button class=\"button\" value=\"left\">
    """)
    esc_html_e("Left")
    php_print("                 </button>\n                 <button class=\"button\" value=\"center\">\n                        ")
    esc_html_e("Center")
    php_print("                 </button>\n                 <button class=\"button\" value=\"right\">\n                     ")
    esc_html_e("Right")
    php_print("                 </button>\n                 <button class=\"button active\" value=\"none\">\n                       ")
    esc_html_e("None")
    php_print("""                   </button>
    </span>
    </span>
    </fieldset>
    <fieldset class=\"setting-group\">
    <legend class=\"name\">""")
    _e("Link To")
    php_print("""</legend>
    <span class=\"setting link-to\">
    <span class=\"button-group button-large\" data-setting=\"link\">
    <button class=\"button\" value=\"file\">
    """)
    esc_html_e("Image URL")
    php_print("                 </button>\n                 <button class=\"button\" value=\"custom\">\n                        ")
    esc_html_e("Custom URL")
    php_print("                 </button>\n                 <button class=\"button active\" value=\"none\">\n                       ")
    esc_html_e("None")
    php_print("""                   </button>
    </span>
    </span>
    <span class=\"setting\">
    <label for=\"embed-image-settings-link-to-custom\" class=\"name\">""")
    _e("URL")
    php_print("""</label>
    <input type=\"text\" id=\"embed-image-settings-link-to-custom\" class=\"link-to-custom\" data-setting=\"linkUrl\" />
    </span>
    </fieldset>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-image-details\">
    <div class=\"media-embed\">
    <div class=\"embed-media-settings\">
    <div class=\"column-settings\">
    <span class=\"setting alt-text has-description\">
    <label for=\"image-details-alt-text\" class=\"name\">""")
    _e("Alternative Text")
    php_print("""</label>
    <input type=\"text\" id=\"image-details-alt-text\" data-setting=\"alt\" value=\"{{ data.model.alt }}\" aria-describedby=\"alt-text-description\" />
    </span>
    <p class=\"description\" id=\"alt-text-description\">""")
    php_print(alt_text_description_)
    php_print("</p>\n\n                 ")
    #// This filter is documented in wp-admin/includes/media.php
    if (not apply_filters("disable_captions", "")):
        php_print("                     <span class=\"setting caption\">\n                          <label for=\"image-details-caption\" class=\"name\">")
        _e("Caption")
        php_print("""</label>
        <textarea id=\"image-details-caption\" data-setting=\"caption\">{{ data.model.caption }}</textarea>
        </span>
        """)
    # end if
    php_print("\n                   <h2>")
    _e("Display Settings")
    php_print("</h2>\n                  <fieldset class=\"setting-group\">\n                        <legend class=\"legend-inline\">")
    _e("Align")
    php_print("""</legend>
    <span class=\"setting align\">
    <span class=\"button-group button-large\" data-setting=\"align\">
    <button class=\"button\" value=\"left\">
    """)
    esc_html_e("Left")
    php_print("                             </button>\n                             <button class=\"button\" value=\"center\">\n                                    ")
    esc_html_e("Center")
    php_print("                             </button>\n                             <button class=\"button\" value=\"right\">\n                                 ")
    esc_html_e("Right")
    php_print("                             </button>\n                             <button class=\"button active\" value=\"none\">\n                                   ")
    esc_html_e("None")
    php_print("""                               </button>
    </span>
    </span>
    </fieldset>
    <# if ( data.attachment ) { #>
    <# if ( 'undefined' !== typeof data.attachment.sizes ) { #>
    <span class=\"setting size\">
    <label for=\"image-details-size\" class=\"name\">""")
    _e("Size")
    php_print("""</label>
    <select id=\"image-details-size\" class=\"size\" name=\"size\"
    data-setting=\"size\"
    <# if ( data.userSettings ) { #>
    data-user-setting=\"imgsize\"
    <# } #>>
    """)
    #// This filter is documented in wp-admin/includes/media.php
    sizes_ = apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")}))
    for value_,name_ in sizes_:
        php_print("                                     <#\n                                        var size = data.sizes['")
        php_print(esc_js(value_))
        php_print("'];\n                                        if ( size ) { #>\n                                          <option value=\"")
        php_print(esc_attr(value_))
        php_print("\">\n                                                ")
        php_print(esc_html(name_))
        php_print(""" &ndash; {{ size.width }} &times; {{ size.height }}
        </option>
        <# } #>
        """)
    # end for
    php_print("                                 <option value=\"")
    php_print(esc_attr("custom"))
    php_print("\">\n                                        ")
    _e("Custom Size")
    php_print("""                                   </option>
    </select>
    </span>
    <# } #>
    <div class=\"custom-size wp-clearfix<# if ( data.model.size !== 'custom' ) { #> hidden<# } #>\">
    <span class=\"custom-size-setting\">
    <label for=\"image-details-size-width\">""")
    _e("Width")
    php_print("""</label>
    <input type=\"number\" id=\"image-details-size-width\" aria-describedby=\"image-size-desc\" data-setting=\"customWidth\" step=\"1\" value=\"{{ data.model.customWidth }}\" />
    </span>
    <span class=\"sep\" aria-hidden=\"true\">&times;</span>
    <span class=\"custom-size-setting\">
    <label for=\"image-details-size-height\">""")
    _e("Height")
    php_print("""</label>
    <input type=\"number\" id=\"image-details-size-height\" aria-describedby=\"image-size-desc\" data-setting=\"customHeight\" step=\"1\" value=\"{{ data.model.customHeight }}\" />
    </span>
    <p id=\"image-size-desc\" class=\"description\">""")
    _e("Image size in pixels")
    php_print("""</p>
    </div>
    <# } #>
    <span class=\"setting link-to\">
    <label for=\"image-details-link-to\" class=\"name\">""")
    _e("Link To")
    php_print("""</label>
    <select id=\"image-details-link-to\" data-setting=\"link\">
    <# if ( data.attachment ) { #>
    <option value=\"file\">
    """)
    esc_html_e("Media File")
    php_print("                         </option>\n                         <option value=\"post\">\n                               ")
    esc_html_e("Attachment Page")
    php_print("""                           </option>
    <# } else { #>
    <option value=\"file\">
    """)
    esc_html_e("Image URL")
    php_print("""                           </option>
    <# } #>
    <option value=\"custom\">
    """)
    esc_html_e("Custom URL")
    php_print("                         </option>\n                         <option value=\"none\">\n                               ")
    esc_html_e("None")
    php_print("""                           </option>
    </select>
    </span>
    <span class=\"setting\">
    <label for=\"image-details-link-to-custom\" class=\"name\">""")
    _e("URL")
    php_print("""</label>
    <input type=\"text\" id=\"image-details-link-to-custom\" class=\"link-to-custom\" data-setting=\"linkUrl\" />
    </span>
    <div class=\"advanced-section\">
    <h2><button type=\"button\" class=\"button-link advanced-toggle\">""")
    _e("Advanced Options")
    php_print("""</button></h2>
    <div class=\"advanced-settings hidden\">
    <div class=\"advanced-image\">
    <span class=\"setting title-text\">
    <label for=\"image-details-title-attribute\" class=\"name\">""")
    _e("Image Title Attribute")
    php_print("""</label>
    <input type=\"text\" id=\"image-details-title-attribute\" data-setting=\"title\" value=\"{{ data.model.title }}\" />
    </span>
    <span class=\"setting extra-classes\">
    <label for=\"image-details-css-class\" class=\"name\">""")
    _e("Image CSS Class")
    php_print("""</label>
    <input type=\"text\" id=\"image-details-css-class\" data-setting=\"extraClasses\" value=\"{{ data.model.extraClasses }}\" />
    </span>
    </div>
    <div class=\"advanced-link\">
    <span class=\"setting link-target\">
    <input type=\"checkbox\" id=\"image-details-link-target\" data-setting=\"linkTargetBlank\" value=\"_blank\" <# if ( data.model.linkTargetBlank ) { #>checked=\"checked\"<# } #>>
    <label for=\"image-details-link-target\" class=\"checkbox-label\">""")
    _e("Open link in a new tab")
    php_print("""</label>
    </span>
    <span class=\"setting link-rel\">
    <label for=\"image-details-link-rel\" class=\"name\">""")
    _e("Link Rel")
    php_print("""</label>
    <input type=\"text\" id=\"image-details-link-rel\" data-setting=\"linkRel\" value=\"{{ data.model.linkRel }}\" />
    </span>
    <span class=\"setting link-class-name\">
    <label for=\"image-details-link-css-class\" class=\"name\">""")
    _e("Link CSS Class")
    php_print("""</label>
    <input type=\"text\" id=\"image-details-link-css-class\" data-setting=\"linkClassName\" value=\"{{ data.model.linkClassName }}\" />
    </span>
    </div>
    </div>
    </div>
    </div>
    <div class=\"column-image\">
    <div class=\"image\">
    <img src=\"{{ data.model.url }}\" draggable=\"false\" alt=\"\" />
    <# if ( data.attachment && window.imageEdit ) { #>
    <div class=\"actions\">
    <input type=\"button\" class=\"edit-attachment button\" value=\"""")
    esc_attr_e("Edit Original")
    php_print("\" />\n                              <input type=\"button\" class=\"replace-attachment button\" value=\"")
    esc_attr_e("Replace")
    php_print("""\" />
    </div>
    <# } #>
    </div>
    </div>
    </div>
    </div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-image-editor\">
    <div id=\"media-head-{{ data.id }}\"></div>
    <div id=\"image-editor-{{ data.id }}\"></div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-audio-details\">
    <# var ext, html5types = {
    mp3: wp.media.view.settings.embedMimes.mp3,
    ogg: wp.media.view.settings.embedMimes.ogg
    }; #>
    """)
    audio_types_ = wp_get_audio_extensions()
    php_print("     <div class=\"media-embed media-embed-details\">\n           <div class=\"embed-media-settings embed-audio-settings\">\n             ")
    wp_underscore_audio_template()
    php_print("""
    <# if ( ! _.isEmpty( data.model.src ) ) {
    ext = data.model.src.split('.').pop();
if ( html5types[ ext ] ) {
    delete html5types[ ext ];
    }
    #>
    <span class=\"setting\">
    <label for=\"audio-details-source\" class=\"name\">""")
    _e("URL")
    php_print("</label>\n                   <input type=\"text\" id=\"audio-details-source\" readonly data-setting=\"src\" value=\"{{ data.model.src }}\" />\n                  <button type=\"button\" class=\"button-link remove-setting\">")
    _e("Remove audio source")
    php_print("""</button>
    </span>
    <# } #>
    """)
    for type_ in audio_types_:
        php_print("             <# if ( ! _.isEmpty( data.model.")
        php_print(type_)
        php_print(" ) ) {\n                 if ( ! _.isUndefined( html5types.")
        php_print(type_)
        php_print(" ) ) {\n                     delete html5types.")
        php_print(type_)
        php_print(""";
        }
        #>
        <span class=\"setting\">
        <label for=\"audio-details-""")
        php_print(type_ + "-source")
        php_print("\" class=\"name\">")
        php_print(php_strtoupper(type_))
        php_print("</label>\n                   <input type=\"text\" id=\"audio-details-")
        php_print(type_ + "-source")
        php_print("\" readonly data-setting=\"")
        php_print(type_)
        php_print("\" value=\"{{ data.model.")
        php_print(type_)
        php_print(" }}\" />\n                   <button type=\"button\" class=\"button-link remove-setting\">")
        _e("Remove audio source")
        php_print("""</button>
        </span>
        <# } #>
        """)
    # end for
    php_print("""
    <# if ( ! _.isEmpty( html5types ) ) { #>
    <fieldset class=\"setting-group\">
    <legend class=\"name\">""")
    _e("Add alternate sources for maximum HTML5 playback")
    php_print("""</legend>
    <span class=\"setting\">
    <span class=\"button-large\">
    <# _.each( html5types, function (mime, type) { #>
    <button class=\"button add-media-source\" data-mime=\"{{ mime }}\">{{ type }}</button>
    <# } ) #>
    </span>
    </span>
    </fieldset>
    <# } #>
    <fieldset class=\"setting-group\">
    <legend class=\"name\">""")
    _e("Preload")
    php_print("""</legend>
    <span class=\"setting preload\">
    <span class=\"button-group button-large\" data-setting=\"preload\">
    <button class=\"button\" value=\"auto\">""")
    _ex("Auto", "auto preload")
    php_print("</button>\n                          <button class=\"button\" value=\"metadata\">")
    _e("Metadata")
    php_print("</button>\n                          <button class=\"button active\" value=\"none\">")
    _e("None")
    php_print("""</button>
    </span>
    </span>
    </fieldset>
    <span class=\"setting-group\">
    <span class=\"setting checkbox-setting autoplay\">
    <input type=\"checkbox\" id=\"audio-details-autoplay\" data-setting=\"autoplay\" />
    <label for=\"audio-details-autoplay\" class=\"checkbox-label\">""")
    _e("Autoplay")
    php_print("""</label>
    </span>
    <span class=\"setting checkbox-setting\">
    <input type=\"checkbox\" id=\"audio-details-loop\" data-setting=\"loop\" />
    <label for=\"audio-details-loop\" class=\"checkbox-label\">""")
    _e("Loop")
    php_print("""</label>
    </span>
    </span>
    </div>
    </div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-video-details\">
    <# var ext, html5types = {
    mp4: wp.media.view.settings.embedMimes.mp4,
    ogv: wp.media.view.settings.embedMimes.ogv,
    webm: wp.media.view.settings.embedMimes.webm
    }; #>
    """)
    video_types_ = wp_get_video_extensions()
    php_print("""       <div class=\"media-embed media-embed-details\">
    <div class=\"embed-media-settings embed-video-settings\">
    <div class=\"wp-video-holder\">
    <#
    var w = ! data.model.width || data.model.width > 640 ? 640 : data.model.width,
    h = ! data.model.height ? 360 : data.model.height;
if ( data.model.width && w !== data.model.width ) {
    h = Math.ceil( ( h * w ) / data.model.width );
    }
    #>
    """)
    wp_underscore_video_template()
    php_print("""
    <# if ( ! _.isEmpty( data.model.src ) ) {
    ext = data.model.src.split('.').pop();
if ( html5types[ ext ] ) {
    delete html5types[ ext ];
    }
    #>
    <span class=\"setting\">
    <label for=\"video-details-source\" class=\"name\">""")
    _e("URL")
    php_print("</label>\n                   <input type=\"text\" id=\"video-details-source\" readonly data-setting=\"src\" value=\"{{ data.model.src }}\" />\n                  <button type=\"button\" class=\"button-link remove-setting\">")
    _e("Remove video source")
    php_print("""</button>
    </span>
    <# } #>
    """)
    for type_ in video_types_:
        php_print("             <# if ( ! _.isEmpty( data.model.")
        php_print(type_)
        php_print(" ) ) {\n                 if ( ! _.isUndefined( html5types.")
        php_print(type_)
        php_print(" ) ) {\n                     delete html5types.")
        php_print(type_)
        php_print(""";
        }
        #>
        <span class=\"setting\">
        <label for=\"video-details-""")
        php_print(type_ + "-source")
        php_print("\" class=\"name\">")
        php_print(php_strtoupper(type_))
        php_print("</label>\n                   <input type=\"text\" id=\"video-details-")
        php_print(type_ + "-source")
        php_print("\" readonly data-setting=\"")
        php_print(type_)
        php_print("\" value=\"{{ data.model.")
        php_print(type_)
        php_print(" }}\" />\n                   <button type=\"button\" class=\"button-link remove-setting\">")
        _e("Remove video source")
        php_print("""</button>
        </span>
        <# } #>
        """)
    # end for
    php_print("""               </div>
    <# if ( ! _.isEmpty( html5types ) ) { #>
    <fieldset class=\"setting-group\">
    <legend class=\"name\">""")
    _e("Add alternate sources for maximum HTML5 playback")
    php_print("""</legend>
    <span class=\"setting\">
    <span class=\"button-large\">
    <# _.each( html5types, function (mime, type) { #>
    <button class=\"button add-media-source\" data-mime=\"{{ mime }}\">{{ type }}</button>
    <# } ) #>
    </span>
    </span>
    </fieldset>
    <# } #>
    <# if ( ! _.isEmpty( data.model.poster ) ) { #>
    <span class=\"setting\">
    <label for=\"video-details-poster-image\" class=\"name\">""")
    _e("Poster Image")
    php_print("</label>\n                   <input type=\"text\" id=\"video-details-poster-image\" readonly data-setting=\"poster\" value=\"{{ data.model.poster }}\" />\n                  <button type=\"button\" class=\"button-link remove-setting\">")
    _e("Remove poster image")
    php_print("""</button>
    </span>
    <# } #>
    <fieldset class=\"setting-group\">
    <legend class=\"name\">""")
    _e("Preload")
    php_print("""</legend>
    <span class=\"setting preload\">
    <span class=\"button-group button-large\" data-setting=\"preload\">
    <button class=\"button\" value=\"auto\">""")
    _ex("Auto", "auto preload")
    php_print("</button>\n                          <button class=\"button\" value=\"metadata\">")
    _e("Metadata")
    php_print("</button>\n                          <button class=\"button active\" value=\"none\">")
    _e("None")
    php_print("""</button>
    </span>
    </span>
    </fieldset>
    <span class=\"setting-group\">
    <span class=\"setting checkbox-setting autoplay\">
    <input type=\"checkbox\" id=\"video-details-autoplay\" data-setting=\"autoplay\" />
    <label for=\"video-details-autoplay\" class=\"checkbox-label\">""")
    _e("Autoplay")
    php_print("""</label>
    </span>
    <span class=\"setting checkbox-setting\">
    <input type=\"checkbox\" id=\"video-details-loop\" data-setting=\"loop\" />
    <label for=\"video-details-loop\" class=\"checkbox-label\">""")
    _e("Loop")
    php_print("""</label>
    </span>
    </span>
    <span class=\"setting\" data-setting=\"content\">
    <#
    var content = '';
if ( ! _.isEmpty( data.model.content ) ) {
    var tracks = jQuery( data.model.content ).filter( 'track' );
    _.each( tracks.toArray(), function( track, index ) {
    content += track.outerHTML; #>
    <label for=\"video-details-track-{{ index }}\" class=\"name\">""")
    _e("Tracks (subtitles, captions, descriptions, chapters, or metadata)")
    php_print("""</label>
    <input class=\"content-track\" type=\"text\" id=\"video-details-track-{{ index }}\" aria-describedby=\"video-details-track-desc-{{ index }}\" value=\"{{ track.outerHTML }}\" />
    <span class=\"description\" id=\"video-details-track-desc-{{ index }}\">
    """)
    printf(__("The %1$s, %2$s, and %3$s values can be edited to set the video track language and kind."), "srclang", "label", "kind")
    php_print("                     </span>\n                       <button type=\"button\" class=\"button-link remove-setting remove-track\">")
    _ex("Remove video track", "media")
    php_print("""</button><br/>
    <# } ); #>
    <# } else { #>
    <span class=\"name\">""")
    _e("Tracks (subtitles, captions, descriptions, chapters, or metadata)")
    php_print("</span><br />\n                  <em>")
    _e("There are no associated subtitles.")
    php_print("""</em>
    <# } #>
    <textarea class=\"hidden content-setting\">{{ content }}</textarea>
    </span>
    </div>
    </div>
    </script>
    """)
    pass
    php_print("""   <script type=\"text/html\" id=\"tmpl-editor-gallery\">
    <# if ( data.attachments.length ) { #>
    <div class=\"gallery gallery-columns-{{ data.columns }}\">
    <# _.each( data.attachments, function( attachment, index ) { #>
    <dl class=\"gallery-item\">
    <dt class=\"gallery-icon\">
    <# if ( attachment.thumbnail ) { #>
    <img src=\"{{ attachment.thumbnail.url }}\" width=\"{{ attachment.thumbnail.width }}\" height=\"{{ attachment.thumbnail.height }}\" alt=\"{{ attachment.alt }}\" />
    <# } else { #>
    <img src=\"{{ attachment.url }}\" alt=\"{{ attachment.alt }}\" />
    <# } #>
    </dt>
    <# if ( attachment.caption ) { #>
    <dd class=\"wp-caption-text gallery-caption\">
    {{{ data.verifyHTML( attachment.caption ) }}}
    </dd>
    <# } #>
    </dl>
    <# if ( index % data.columns === data.columns - 1 ) { #>
    <br style=\"clear: both;\">
    <# } #>
    <# } ); #>
    </div>
    <# } else { #>
    <div class=\"wpview-error\">
    <div class=\"dashicons dashicons-format-gallery\"></div><p>""")
    _e("No items found.")
    php_print("""</p>
    </div>
    <# } #>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-crop-content\">\n      <img class=\"crop-image\" src=\"{{ data.url }}\" alt=\"")
    esc_attr_e("Image crop area preview. Requires mouse interaction.")
    php_print("""\">
    <div class=\"upload-errors\"></div>
    </script>
    """)
    pass
    php_print(" <script type=\"text/html\" id=\"tmpl-site-icon-preview\">\n     <h2>")
    _e("Preview")
    php_print("</h2>\n      <strong aria-hidden=\"true\">")
    _e("As a browser icon")
    php_print("</strong>\n      <div class=\"favicon-preview\">\n           <img src=\"")
    php_print(esc_url(admin_url("images/" + "browser-rtl.png" if is_rtl() else "browser.png")))
    php_print("""\" class=\"browser-preview\" width=\"182\" height=\"\" alt=\"\" />
    <div class=\"favicon\">
    <img id=\"preview-favicon\" src=\"{{ data.url }}\" alt=\"""")
    esc_attr_e("Preview as a browser icon")
    php_print("\"/>\n           </div>\n            <span class=\"browser-title\" aria-hidden=\"true\"><# print( '")
    bloginfo("name")
    php_print("""' ) #></span>
    </div>
    <strong aria-hidden=\"true\">""")
    _e("As an app icon")
    php_print("</strong>\n      <div class=\"app-icon-preview\">\n          <img id=\"preview-app-icon\" src=\"{{ data.url }}\" alt=\"")
    esc_attr_e("Preview as an app icon")
    php_print("""\"/>
    </div>
    </script>
    """)
    #// 
    #// Fires when the custom Backbone media templates are printed.
    #// 
    #// @since 3.5.0
    #//
    do_action("print_media_templates")
# end def wp_print_media_templates
