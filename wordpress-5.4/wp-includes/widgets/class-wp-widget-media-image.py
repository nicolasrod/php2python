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
    def render_media(self, instance=None):
        
        instance = php_array_merge(wp_list_pluck(self.get_instance_schema(), "default"), instance)
        instance = wp_parse_args(instance, Array({"size": "thumbnail"}))
        attachment = None
        if self.is_attachment_with_mime_type(instance["attachment_id"], self.widget_options["mime_type"]):
            attachment = get_post(instance["attachment_id"])
        # end if
        if attachment:
            caption = ""
            if (not (php_isset(lambda : instance["caption"]))):
                caption = attachment.post_excerpt
            elif php_trim(instance["caption"]):
                caption = instance["caption"]
            # end if
            image_attributes = Array({"class": php_sprintf("image wp-image-%d %s", attachment.ID, instance["image_classes"]), "style": "max-width: 100%; height: auto;"})
            if (not php_empty(lambda : instance["image_title"])):
                image_attributes["title"] = instance["image_title"]
            # end if
            if instance["alt"]:
                image_attributes["alt"] = instance["alt"]
            # end if
            size = instance["size"]
            if "custom" == size or (not php_in_array(size, php_array_merge(get_intermediate_image_sizes(), Array("full")), True)):
                size = Array(instance["width"], instance["height"])
            # end if
            image_attributes["class"] += php_sprintf(" attachment-%1$s size-%1$s", join("x", size) if php_is_array(size) else size)
            image = wp_get_attachment_image(attachment.ID, size, False, image_attributes)
            caption_size = _wp_get_image_size_from_meta(instance["size"], wp_get_attachment_metadata(attachment.ID))
            width = 0 if php_empty(lambda : caption_size[0]) else caption_size[0]
        else:
            if php_empty(lambda : instance["url"]):
                return
            # end if
            instance["size"] = "custom"
            caption = instance["caption"]
            width = instance["width"]
            classes = "image " + instance["image_classes"]
            if 0 == instance["width"]:
                instance["width"] = ""
            # end if
            if 0 == instance["height"]:
                instance["height"] = ""
            # end if
            image = php_sprintf("<img class=\"%1$s\" src=\"%2$s\" alt=\"%3$s\" width=\"%4$s\" height=\"%5$s\" />", esc_attr(classes), esc_url(instance["url"]), esc_attr(instance["alt"]), esc_attr(instance["width"]), esc_attr(instance["height"]))
        # end if
        #// End if().
        url = ""
        if "file" == instance["link_type"]:
            url = wp_get_attachment_url(attachment.ID) if attachment else instance["url"]
        elif attachment and "post" == instance["link_type"]:
            url = get_attachment_link(attachment.ID)
        elif "custom" == instance["link_type"] and (not php_empty(lambda : instance["link_url"])):
            url = instance["link_url"]
        # end if
        if url:
            link = php_sprintf("<a href=\"%s\"", esc_url(url))
            if (not php_empty(lambda : instance["link_classes"])):
                link += php_sprintf(" class=\"%s\"", esc_attr(instance["link_classes"]))
            # end if
            if (not php_empty(lambda : instance["link_rel"])):
                link += php_sprintf(" rel=\"%s\"", esc_attr(instance["link_rel"]))
            # end if
            if (not php_empty(lambda : instance["link_target_blank"])):
                link += " target=\"_blank\""
            # end if
            link += ">"
            link += image
            link += "</a>"
            image = wp_targeted_link_rel(link)
        # end if
        if caption:
            image = img_caption_shortcode(Array({"width": width, "caption": caption}), image)
        # end if
        php_print(image)
    # end def render_media
    #// 
    #// Loads the required media files for the media manager and scripts for media widgets.
    #// 
    #// @since 4.8.0
    #//
    def enqueue_admin_scripts(self):
        
        super().enqueue_admin_scripts()
        handle = "media-image-widget"
        wp_enqueue_script(handle)
        exported_schema = Array()
        for field,field_schema in self.get_instance_schema():
            exported_schema[field] = wp_array_slice_assoc(field_schema, Array("type", "default", "enum", "minimum", "format", "media_prop", "should_preview_update"))
        # end for
        wp_add_inline_script(handle, php_sprintf("wp.mediaWidgets.modelConstructors[ %s ].prototype.schema = %s;", wp_json_encode(self.id_base), wp_json_encode(exported_schema)))
        wp_add_inline_script(handle, php_sprintf("""
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
