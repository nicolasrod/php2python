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
#// Widget API: WP_Widget_Media_Video class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.8.0
#// 
#// 
#// Core class that implements a video widget.
#// 
#// @since 4.8.0
#// 
#// @see WP_Widget_Media
#// @see WP_Widget
#//
class WP_Widget_Media_Video(WP_Widget_Media):
    #// 
    #// Constructor.
    #// 
    #// @since 4.8.0
    #//
    def __init__(self):
        
        
        super().__init__("media_video", __("Video"), Array({"description": __("Displays a video from the media library or from YouTube, Vimeo, or another provider."), "mime_type": "video"}))
        self.l10n = php_array_merge(self.l10n, Array({"no_media_selected": __("No video selected"), "add_media": _x("Add Video", "label for button in the video widget"), "replace_media": _x("Replace Video", "label for button in the video widget; should preferably not be longer than ~13 characters long"), "edit_media": _x("Edit Video", "label for button in the video widget; should preferably not be longer than ~13 characters long"), "missing_attachment": php_sprintf(__("We can&#8217;t find that video. Check your <a href=\"%s\">media library</a> and make sure it wasn&#8217;t deleted."), esc_url(admin_url("upload.php"))), "media_library_state_multi": _n_noop("Video Widget (%d)", "Video Widget (%d)"), "media_library_state_single": __("Video Widget"), "unsupported_file_type": php_sprintf(__("Sorry, we can&#8217;t load the video at the supplied URL. Please check that the URL is for a supported video file (%s) or stream (e.g. YouTube and Vimeo)."), "<code>." + php_implode("</code>, <code>.", wp_get_video_extensions()) + "</code>")}))
    # end def __init__
    #// 
    #// Get schema for properties of a widget instance (item).
    #// 
    #// @since 4.8.0
    #// 
    #// @see WP_REST_Controller::get_item_schema()
    #// @see WP_REST_Controller::get_additional_fields()
    #// @link https://core.trac.wordpress.org/ticket/35574
    #// 
    #// @return array Schema for properties.
    #//
    def get_instance_schema(self):
        
        
        schema_ = Array({"preload": Array({"type": "string", "enum": Array("none", "auto", "metadata"), "default": "metadata", "description": __("Preload"), "should_preview_update": False})}, {"loop": Array({"type": "boolean", "default": False, "description": __("Loop"), "should_preview_update": False})}, {"content": Array({"type": "string", "default": "", "sanitize_callback": "wp_kses_post", "description": __("Tracks (subtitles, captions, descriptions, chapters, or metadata)"), "should_preview_update": False})})
        for video_extension_ in wp_get_video_extensions():
            schema_[video_extension_] = Array({"type": "string", "default": "", "format": "uri", "description": php_sprintf(__("URL to the %s video source file"), video_extension_)})
        # end for
        return php_array_merge(schema_, super().get_instance_schema())
    # end def get_instance_schema
    #// 
    #// Render the media on the frontend.
    #// 
    #// @since 4.8.0
    #// 
    #// @param array $instance Widget instance props.
    #//
    def render_media(self, instance_=None):
        
        
        instance_ = php_array_merge(wp_list_pluck(self.get_instance_schema(), "default"), instance_)
        attachment_ = None
        if self.is_attachment_with_mime_type(instance_["attachment_id"], self.widget_options["mime_type"]):
            attachment_ = get_post(instance_["attachment_id"])
        # end if
        src_ = instance_["url"]
        if attachment_:
            src_ = wp_get_attachment_url(attachment_.ID)
        # end if
        if php_empty(lambda : src_):
            return
        # end if
        youtube_pattern_ = "#^https?://(?:www\\.)?(?:youtube\\.com/watch|youtu\\.be/)#"
        vimeo_pattern_ = "#^https?://(.+\\.)?vimeo\\.com/.*#"
        if attachment_ or php_preg_match(youtube_pattern_, src_) or php_preg_match(vimeo_pattern_, src_):
            add_filter("wp_video_shortcode", Array(self, "inject_video_max_width_style"))
            php_print(wp_video_shortcode(php_array_merge(instance_, php_compact("src")), instance_["content"]))
            remove_filter("wp_video_shortcode", Array(self, "inject_video_max_width_style"))
        else:
            php_print(self.inject_video_max_width_style(wp_oembed_get(src_)))
        # end if
    # end def render_media
    #// 
    #// Inject max-width and remove height for videos too constrained to fit inside sidebars on frontend.
    #// 
    #// @since 4.8.0
    #// 
    #// @param string $html Video shortcode HTML output.
    #// @return string HTML Output.
    #//
    def inject_video_max_width_style(self, html_=None):
        
        
        html_ = php_preg_replace("/\\sheight=\"\\d+\"/", "", html_)
        html_ = php_preg_replace("/\\swidth=\"\\d+\"/", "", html_)
        html_ = php_preg_replace("/(?<=width:)\\s*\\d+px(?=;?)/", "100%", html_)
        return html_
    # end def inject_video_max_width_style
    #// 
    #// Enqueue preview scripts.
    #// 
    #// These scripts normally are enqueued just-in-time when a video shortcode is used.
    #// In the customizer, however, widgets can be dynamically added and rendered via
    #// selective refresh, and so it is important to unconditionally enqueue them in
    #// case a widget does get added.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_preview_scripts(self):
        
        
        #// This filter is documented in wp-includes/media.php
        if "mediaelement" == apply_filters("wp_video_shortcode_library", "mediaelement"):
            wp_enqueue_style("wp-mediaelement")
            wp_enqueue_script("mediaelement-vimeo")
            wp_enqueue_script("wp-mediaelement")
        # end if
    # end def enqueue_preview_scripts
    #// 
    #// Loads the required scripts and styles for the widget control.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_admin_scripts(self):
        
        
        super().enqueue_admin_scripts()
        handle_ = "media-video-widget"
        wp_enqueue_script(handle_)
        exported_schema_ = Array()
        for field_,field_schema_ in self.get_instance_schema():
            exported_schema_[field_] = wp_array_slice_assoc(field_schema_, Array("type", "default", "enum", "minimum", "format", "media_prop", "should_preview_update"))
        # end for
        wp_add_inline_script(handle_, php_sprintf("wp.mediaWidgets.modelConstructors[ %s ].prototype.schema = %s;", wp_json_encode(self.id_base), wp_json_encode(exported_schema_)))
        wp_add_inline_script(handle_, php_sprintf("""
        wp.mediaWidgets.controlConstructors[ %1$s ].prototype.mime_type = %2$s;
        wp.mediaWidgets.controlConstructors[ %1$s ].prototype.l10n = _.extend( {}, wp.mediaWidgets.controlConstructors[ %1$s ].prototype.l10n, %3$s );
        """, wp_json_encode(self.id_base), wp_json_encode(self.widget_options["mime_type"]), wp_json_encode(self.l10n)))
    # end def enqueue_admin_scripts
    #// 
    #// Render form template scripts.
    #// 
    #// @since 4.8.0
    #//
    def render_control_template_scripts(self):
        
        
        super().render_control_template_scripts()
        php_print("""       <script type=\"text/html\" id=\"tmpl-wp-media-widget-video-preview\">
        <# if ( data.error && 'missing_attachment' === data.error ) { #>
        <div class=\"notice notice-error notice-alt notice-missing-attachment\">
        <p>""")
        php_print(self.l10n["missing_attachment"])
        php_print("""</p>
        </div>
        <# } else if ( data.error && 'unsupported_file_type' === data.error ) { #>
        <div class=\"notice notice-error notice-alt notice-missing-attachment\">
        <p>""")
        php_print(self.l10n["unsupported_file_type"])
        php_print("""</p>
        </div>
        <# } else if ( data.error ) { #>
        <div class=\"notice notice-error notice-alt\">
        <p>""")
        _e("Unable to preview media due to an unknown error.")
        php_print("""</p>
        </div>
        <# } else if ( data.is_oembed && data.model.poster ) { #>
        <a href=\"{{ data.model.src }}\" target=\"_blank\" class=\"media-widget-video-link\">
        <img src=\"{{ data.model.poster }}\" />
        </a>
        <# } else if ( data.is_oembed ) { #>
        <a href=\"{{ data.model.src }}\" target=\"_blank\" class=\"media-widget-video-link no-poster\">
        <span class=\"dashicons dashicons-format-video\"></span>
        </a>
        <# } else if ( data.model.src ) { #>
        """)
        wp_underscore_video_template()
        php_print("         <# } #>\n       </script>\n     ")
    # end def render_control_template_scripts
# end class WP_Widget_Media_Video
