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
#// Widget API: WP_Widget_Media_Image class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.8.0
#// 
#// 
#// Core class that implements an image widget.
#// 
#// @since 4.8.0
#// 
#// @see WP_Widget_Media
#// @see WP_Widget
#//
class WP_Widget_Media_Image(WP_Widget_Media):
    #// 
    #// Constructor.
    #// 
    #// @since 4.8.0
    #//
    def __init__(self):
        
        
        super().__init__("media_image", __("Image"), Array({"description": __("Displays an image."), "mime_type": "image"}))
        self.l10n = php_array_merge(self.l10n, Array({"no_media_selected": __("No image selected"), "add_media": _x("Add Image", "label for button in the image widget"), "replace_media": _x("Replace Image", "label for button in the image widget; should preferably not be longer than ~13 characters long"), "edit_media": _x("Edit Image", "label for button in the image widget; should preferably not be longer than ~13 characters long"), "missing_attachment": php_sprintf(__("We can&#8217;t find that image. Check your <a href=\"%s\">media library</a> and make sure it wasn&#8217;t deleted."), esc_url(admin_url("upload.php"))), "media_library_state_multi": _n_noop("Image Widget (%d)", "Image Widget (%d)"), "media_library_state_single": __("Image Widget")}))
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
        
        
        return php_array_merge(Array({"size": Array({"type": "string", "enum": php_array_merge(get_intermediate_image_sizes(), Array("full", "custom")), "default": "medium", "description": __("Size")})}, {"width": Array({"type": "integer", "minimum": 0, "default": 0, "description": __("Width")})}, {"height": Array({"type": "integer", "minimum": 0, "default": 0, "description": __("Height")})}, {"caption": Array({"type": "string", "default": "", "sanitize_callback": "wp_kses_post", "description": __("Caption"), "should_preview_update": False})}, {"alt": Array({"type": "string", "default": "", "sanitize_callback": "sanitize_text_field", "description": __("Alternative Text")})}, {"link_type": Array({"type": "string", "enum": Array("none", "file", "post", "custom"), "default": "custom", "media_prop": "link", "description": __("Link To"), "should_preview_update": True})}, {"link_url": Array({"type": "string", "default": "", "format": "uri", "media_prop": "linkUrl", "description": __("URL"), "should_preview_update": True})}, {"image_classes": Array({"type": "string", "default": "", "sanitize_callback": Array(self, "sanitize_token_list"), "media_prop": "extraClasses", "description": __("Image CSS Class"), "should_preview_update": False})}, {"link_classes": Array({"type": "string", "default": "", "sanitize_callback": Array(self, "sanitize_token_list"), "media_prop": "linkClassName", "should_preview_update": False, "description": __("Link CSS Class")})}, {"link_rel": Array({"type": "string", "default": "", "sanitize_callback": Array(self, "sanitize_token_list"), "media_prop": "linkRel", "description": __("Link Rel"), "should_preview_update": False})}, {"link_target_blank": Array({"type": "boolean", "default": False, "media_prop": "linkTargetBlank", "description": __("Open link in a new tab"), "should_preview_update": False})}, {"image_title": Array({"type": "string", "default": "", "sanitize_callback": "sanitize_text_field", "media_prop": "title", "description": __("Image Title Attribute"), "should_preview_update": False})}), super().get_instance_schema())
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
        instance_ = wp_parse_args(instance_, Array({"size": "thumbnail"}))
        attachment_ = None
        if self.is_attachment_with_mime_type(instance_["attachment_id"], self.widget_options["mime_type"]):
            attachment_ = get_post(instance_["attachment_id"])
        # end if
        if attachment_:
            caption_ = ""
            if (not (php_isset(lambda : instance_["caption"]))):
                caption_ = attachment_.post_excerpt
            elif php_trim(instance_["caption"]):
                caption_ = instance_["caption"]
            # end if
            image_attributes_ = Array({"class": php_sprintf("image wp-image-%d %s", attachment_.ID, instance_["image_classes"]), "style": "max-width: 100%; height: auto;"})
            if (not php_empty(lambda : instance_["image_title"])):
                image_attributes_["title"] = instance_["image_title"]
            # end if
            if instance_["alt"]:
                image_attributes_["alt"] = instance_["alt"]
            # end if
            size_ = instance_["size"]
            if "custom" == size_ or (not php_in_array(size_, php_array_merge(get_intermediate_image_sizes(), Array("full")), True)):
                size_ = Array(instance_["width"], instance_["height"])
            # end if
            image_attributes_["class"] += php_sprintf(" attachment-%1$s size-%1$s", join("x", size_) if php_is_array(size_) else size_)
            image_ = wp_get_attachment_image(attachment_.ID, size_, False, image_attributes_)
            caption_size_ = _wp_get_image_size_from_meta(instance_["size"], wp_get_attachment_metadata(attachment_.ID))
            width_ = 0 if php_empty(lambda : caption_size_[0]) else caption_size_[0]
        else:
            if php_empty(lambda : instance_["url"]):
                return
            # end if
            instance_["size"] = "custom"
            caption_ = instance_["caption"]
            width_ = instance_["width"]
            classes_ = "image " + instance_["image_classes"]
            if 0 == instance_["width"]:
                instance_["width"] = ""
            # end if
            if 0 == instance_["height"]:
                instance_["height"] = ""
            # end if
            image_ = php_sprintf("<img class=\"%1$s\" src=\"%2$s\" alt=\"%3$s\" width=\"%4$s\" height=\"%5$s\" />", esc_attr(classes_), esc_url(instance_["url"]), esc_attr(instance_["alt"]), esc_attr(instance_["width"]), esc_attr(instance_["height"]))
        # end if
        #// End if().
        url_ = ""
        if "file" == instance_["link_type"]:
            url_ = wp_get_attachment_url(attachment_.ID) if attachment_ else instance_["url"]
        elif attachment_ and "post" == instance_["link_type"]:
            url_ = get_attachment_link(attachment_.ID)
        elif "custom" == instance_["link_type"] and (not php_empty(lambda : instance_["link_url"])):
            url_ = instance_["link_url"]
        # end if
        if url_:
            link_ = php_sprintf("<a href=\"%s\"", esc_url(url_))
            if (not php_empty(lambda : instance_["link_classes"])):
                link_ += php_sprintf(" class=\"%s\"", esc_attr(instance_["link_classes"]))
            # end if
            if (not php_empty(lambda : instance_["link_rel"])):
                link_ += php_sprintf(" rel=\"%s\"", esc_attr(instance_["link_rel"]))
            # end if
            if (not php_empty(lambda : instance_["link_target_blank"])):
                link_ += " target=\"_blank\""
            # end if
            link_ += ">"
            link_ += image_
            link_ += "</a>"
            image_ = wp_targeted_link_rel(link_)
        # end if
        if caption_:
            image_ = img_caption_shortcode(Array({"width": width_, "caption": caption_}), image_)
        # end if
        php_print(image_)
    # end def render_media
    #// 
    #// Loads the required media files for the media manager and scripts for media widgets.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_admin_scripts(self):
        
        
        super().enqueue_admin_scripts()
        handle_ = "media-image-widget"
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
        php_print("""       <script type=\"text/html\" id=\"tmpl-wp-media-widget-image-fields\">
        <# var elementIdPrefix = 'el' + String( Math.random() ) + '_'; #>
        <# if ( data.url ) { #>
        <p class=\"media-widget-image-link\">
        <label for=\"{{ elementIdPrefix }}linkUrl\">""")
        esc_html_e("Link to:")
        php_print("""</label>
        <input id=\"{{ elementIdPrefix }}linkUrl\" type=\"text\" class=\"widefat link\" value=\"{{ data.link_url }}\" placeholder=\"https://\" pattern=\"((\\w+:)?\\/\\/\\w.*|\\w+:(?!\\/\\/$)|\\/|\\?|#).*\">
        </p>
        <# } #>
        </script>
        <script type=\"text/html\" id=\"tmpl-wp-media-widget-image-preview\">
        <# if ( data.error && 'missing_attachment' === data.error ) { #>
        <div class=\"notice notice-error notice-alt notice-missing-attachment\">
        <p>""")
        php_print(self.l10n["missing_attachment"])
        php_print("""</p>
        </div>
        <# } else if ( data.error ) { #>
        <div class=\"notice notice-error notice-alt\">
        <p>""")
        _e("Unable to preview media due to an unknown error.")
        php_print("""</p>
        </div>
        <# } else if ( data.url ) { #>
        <img class=\"attachment-thumb\" src=\"{{ data.url }}\" draggable=\"false\" alt=\"{{ data.alt }}\"
        <# if ( ! data.alt && data.currentFilename ) { #>
        aria-label=\"
        """)
        php_print(esc_attr(php_sprintf(__("The current image has no alternative text. The file name is: %s"), "{{ data.currentFilename }}")))
        php_print("""                       \"
        <# } #>
        />
        <# } #>
        </script>
        """)
    # end def render_control_template_scripts
# end class WP_Widget_Media_Image
