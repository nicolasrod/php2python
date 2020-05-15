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
#// The custom header image script.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// The custom header image class.
#// 
#// @since 2.1.0
#//
class Custom_Image_Header():
    admin_header_callback = Array()
    admin_image_div_callback = Array()
    default_headers = Array()
    updated = Array()
    #// 
    #// Constructor - Register administration header callback.
    #// 
    #// @since 2.1.0
    #// @param callable $admin_header_callback
    #// @param callable $admin_image_div_callback Optional custom image div output callback.
    #//
    def __init__(self, admin_header_callback=None, admin_image_div_callback=""):
        
        self.admin_header_callback = admin_header_callback
        self.admin_image_div_callback = admin_image_div_callback
        add_action("admin_menu", Array(self, "init"))
        add_action("customize_save_after", Array(self, "customize_set_last_used"))
        add_action("wp_ajax_custom-header-crop", Array(self, "ajax_header_crop"))
        add_action("wp_ajax_custom-header-add", Array(self, "ajax_header_add"))
        add_action("wp_ajax_custom-header-remove", Array(self, "ajax_header_remove"))
    # end def __init__
    #// 
    #// Set up the hooks for the Custom Header admin page.
    #// 
    #// @since 2.1.0
    #//
    def init(self):
        
        page = add_theme_page(__("Header"), __("Header"), "edit_theme_options", "custom-header", Array(self, "admin_page"))
        if (not page):
            return
        # end if
        add_action(str("admin_print_scripts-") + str(page), Array(self, "js_includes"))
        add_action(str("admin_print_styles-") + str(page), Array(self, "css_includes"))
        add_action(str("admin_head-") + str(page), Array(self, "help"))
        add_action(str("admin_head-") + str(page), Array(self, "take_action"), 50)
        add_action(str("admin_head-") + str(page), Array(self, "js"), 50)
        if self.admin_header_callback:
            add_action(str("admin_head-") + str(page), self.admin_header_callback, 51)
        # end if
    # end def init
    #// 
    #// Adds contextual help.
    #// 
    #// @since 3.0.0
    #//
    def help(self):
        
        get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen is used to customize the header section of your theme.") + "</p>" + "<p>" + __("You can choose from the theme&#8217;s default header images, or use one of your own. You can also customize how your Site Title and Tagline are displayed.") + "<p>"}))
        get_current_screen().add_help_tab(Array({"id": "set-header-image", "title": __("Header Image"), "content": "<p>" + __("You can set a custom image header for your site. Simply upload the image and crop it, and the new header will go live immediately. Alternatively, you can use an image that has already been uploaded to your Media Library by clicking the &#8220;Choose Image&#8221; button.") + "</p>" + "<p>" + __("Some themes come with additional header images bundled. If you see multiple images displayed, select the one you&#8217;d like and click the &#8220;Save Changes&#8221; button.") + "</p>" + "<p>" + __("If your theme has more than one default header image, or you have uploaded more than one custom header image, you have the option of having WordPress display a randomly different image on each page of your site. Click the &#8220;Random&#8221; radio button next to the Uploaded Images or Default Images section to enable this feature.") + "</p>" + "<p>" + __("If you don&#8217;t want a header image to be displayed on your site at all, click the &#8220;Remove Header Image&#8221; button at the bottom of the Header Image section of this page. If you want to re-enable the header image later, you just have to select one of the other image options and click &#8220;Save Changes&#8221;.") + "</p>"}))
        get_current_screen().add_help_tab(Array({"id": "set-header-text", "title": __("Header Text"), "content": "<p>" + php_sprintf(__("For most themes, the header text is your Site Title and Tagline, as defined in the <a href=\"%s\">General Settings</a> section."), admin_url("options-general.php")) + "</p>" + "<p>" + __("In the Header Text section of this page, you can choose whether to display this text or hide it. You can also choose a color for the text by clicking the Select Color button and either typing in a legitimate HTML hex value, e.g. &#8220;#ff0000&#8221; for red, or by choosing a color using the color picker.") + "</p>" + "<p>" + __("Don&#8217;t forget to click &#8220;Save Changes&#8221; when you&#8217;re done!") + "</p>"}))
        get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Appearance_Header_Screen\">Documentation on Custom Header</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
    # end def help
    #// 
    #// Get the current step.
    #// 
    #// @since 2.6.0
    #// 
    #// @return int Current step
    #//
    def step(self):
        
        if (not (php_isset(lambda : PHP_REQUEST["step"]))):
            return 1
        # end if
        step = int(PHP_REQUEST["step"])
        if step < 1 or 3 < step or 2 == step and (not wp_verify_nonce(PHP_REQUEST["_wpnonce-custom-header-upload"], "custom-header-upload")) or 3 == step and (not wp_verify_nonce(PHP_REQUEST["_wpnonce"], "custom-header-crop-image")):
            return 1
        # end if
        return step
    # end def step
    #// 
    #// Set up the enqueue for the JavaScript files.
    #// 
    #// @since 2.1.0
    #//
    def js_includes(self):
        
        step = self.step()
        if 1 == step or 3 == step:
            wp_enqueue_media()
            wp_enqueue_script("custom-header")
            if current_theme_supports("custom-header", "header-text"):
                wp_enqueue_script("wp-color-picker")
            # end if
        elif 2 == step:
            wp_enqueue_script("imgareaselect")
        # end if
    # end def js_includes
    #// 
    #// Set up the enqueue for the CSS files
    #// 
    #// @since 2.7.0
    #//
    def css_includes(self):
        
        step = self.step()
        if 1 == step or 3 == step and current_theme_supports("custom-header", "header-text"):
            wp_enqueue_style("wp-color-picker")
        elif 2 == step:
            wp_enqueue_style("imgareaselect")
        # end if
    # end def css_includes
    #// 
    #// Execute custom header modification.
    #// 
    #// @since 2.6.0
    #//
    def take_action(self):
        global PHP_POST
        if (not current_user_can("edit_theme_options")):
            return
        # end if
        if php_empty(lambda : PHP_POST):
            return
        # end if
        self.updated = True
        if (php_isset(lambda : PHP_POST["resetheader"])):
            check_admin_referer("custom-header-options", "_wpnonce-custom-header-options")
            self.reset_header_image()
            return
        # end if
        if (php_isset(lambda : PHP_POST["removeheader"])):
            check_admin_referer("custom-header-options", "_wpnonce-custom-header-options")
            self.remove_header_image()
            return
        # end if
        if (php_isset(lambda : PHP_POST["text-color"])) and (not (php_isset(lambda : PHP_POST["display-header-text"]))):
            check_admin_referer("custom-header-options", "_wpnonce-custom-header-options")
            set_theme_mod("header_textcolor", "blank")
        elif (php_isset(lambda : PHP_POST["text-color"])):
            check_admin_referer("custom-header-options", "_wpnonce-custom-header-options")
            PHP_POST["text-color"] = php_str_replace("#", "", PHP_POST["text-color"])
            color = php_preg_replace("/[^0-9a-fA-F]/", "", PHP_POST["text-color"])
            if php_strlen(color) == 6 or php_strlen(color) == 3:
                set_theme_mod("header_textcolor", color)
            elif (not color):
                set_theme_mod("header_textcolor", "blank")
            # end if
        # end if
        if (php_isset(lambda : PHP_POST["default-header"])):
            check_admin_referer("custom-header-options", "_wpnonce-custom-header-options")
            self.set_header_image(PHP_POST["default-header"])
            return
        # end if
    # end def take_action
    #// 
    #// Process the default headers
    #// 
    #// @since 3.0.0
    #// 
    #// @global array $_wp_default_headers
    #//
    def process_default_headers(self):
        
        global _wp_default_headers
        php_check_if_defined("_wp_default_headers")
        if (not (php_isset(lambda : _wp_default_headers))):
            return
        # end if
        if (not php_empty(lambda : self.default_headers)):
            return
        # end if
        self.default_headers = _wp_default_headers
        template_directory_uri = get_template_directory_uri()
        stylesheet_directory_uri = get_stylesheet_directory_uri()
        for header in php_array_keys(self.default_headers):
            self.default_headers[header]["url"] = php_sprintf(self.default_headers[header]["url"], template_directory_uri, stylesheet_directory_uri)
            self.default_headers[header]["thumbnail_url"] = php_sprintf(self.default_headers[header]["thumbnail_url"], template_directory_uri, stylesheet_directory_uri)
        # end for
    # end def process_default_headers
    #// 
    #// Display UI for selecting one of several default headers.
    #// 
    #// Show the random image option if this theme has multiple header images.
    #// Random image option is on by default if no header has been set.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $type The header type. One of 'default' (for the Uploaded Images control)
    #// or 'uploaded' (for the Uploaded Images control).
    #//
    def show_header_selector(self, type="default"):
        
        if "default" == type:
            headers = self.default_headers
        else:
            headers = get_uploaded_header_images()
            type = "uploaded"
        # end if
        if 1 < php_count(headers):
            php_print("<div class=\"random-header\">")
            php_print("<label><input name=\"default-header\" type=\"radio\" value=\"random-" + type + "-image\"" + checked(is_random_header_image(type), True, False) + " />")
            _e("<strong>Random:</strong> Show a different image on each page.")
            php_print("</label>")
            php_print("</div>")
        # end if
        php_print("<div class=\"available-headers\">")
        for header_key,header in headers:
            header_thumbnail = header["thumbnail_url"]
            header_url = header["url"]
            header_alt_text = "" if php_empty(lambda : header["alt_text"]) else header["alt_text"]
            php_print("<div class=\"default-header\">")
            php_print("<label><input name=\"default-header\" type=\"radio\" value=\"" + esc_attr(header_key) + "\" " + checked(header_url, get_theme_mod("header_image"), False) + " />")
            width = ""
            if (not php_empty(lambda : header["attachment_id"])):
                width = " width=\"230\""
            # end if
            php_print("<img src=\"" + set_url_scheme(header_thumbnail) + "\" alt=\"" + esc_attr(header_alt_text) + "\"" + width + " /></label>")
            php_print("</div>")
        # end for
        php_print("<div class=\"clear\"></div></div>")
    # end def show_header_selector
    #// 
    #// Execute JavaScript depending on step.
    #// 
    #// @since 2.1.0
    #//
    def js(self):
        
        step = self.step()
        if 1 == step or 3 == step and current_theme_supports("custom-header", "header-text"):
            self.js_1()
        elif 2 == step:
            self.js_2()
        # end if
    # end def js
    #// 
    #// Display JavaScript based on Step 1 and 3.
    #// 
    #// @since 2.6.0
    #//
    def js_1(self):
        
        default_color = ""
        if current_theme_supports("custom-header", "default-text-color"):
            default_color = get_theme_support("custom-header", "default-text-color")
            if default_color and False == php_strpos(default_color, "#"):
                default_color = "#" + default_color
            # end if
        # end if
        php_print("<script type=\"text/javascript\">\n(function($){\n   var default_color = '")
        php_print(default_color)
        php_print("""',
        header_text_fields;
        function pickColor(color) {
        $('#name').css('color', color);
        $('#desc').css('color', color);
        $('#text-color').val(color);
        }
        function toggle_text() {
        var checked = $('#display-header-text').prop('checked'),
        text_color;
        header_text_fields.toggle( checked );
    if ( ! checked )
        return;
        text_color = $('#text-color');
    if ( '' == text_color.val().replace('#', '') ) {
        text_color.val( default_color );
        pickColor( default_color );
        } else {
        pickColor( text_color.val() );
        }
        }
        $(document).ready(function() {
        var text_color = $('#text-color');
        header_text_fields = $('.displaying-header-text');
        text_color.wpColorPicker({
        change: function( event, ui ) {
        pickColor( text_color.wpColorPicker('color') );
        },
        clear: function() {
        pickColor( '' );
        }
        });
        $('#display-header-text').click( toggle_text );
        """)
        if (not display_header_text()):
            php_print("     toggle_text();\n        ")
        # end if
        php_print("""   });
        })(jQuery);
        </script>
        """)
    # end def js_1
    #// 
    #// Display JavaScript based on Step 2.
    #// 
    #// @since 2.6.0
    #//
    def js_2(self):
        
        php_print("""<script type=\"text/javascript\">
        function onEndCrop( coords ) {
        jQuery( '#x1' ).val(coords.x);
        jQuery( '#y1' ).val(coords.y);
        jQuery( '#width' ).val(coords.w);
        jQuery( '#height' ).val(coords.h);
        }
        jQuery(document).ready(function() {
        var xinit = """)
        php_print(absint(get_theme_support("custom-header", "width")))
        php_print(";\n      var yinit = ")
        php_print(absint(get_theme_support("custom-header", "height")))
        php_print(""";
        var ratio = xinit / yinit;
        var ximg = jQuery('img#upload').width();
        var yimg = jQuery('img#upload').height();
    if ( yimg < yinit || ximg < xinit ) {
    if ( ximg / yimg > ratio ) {
        yinit = yimg;
        xinit = yinit * ratio;
        } else {
        xinit = ximg;
        yinit = xinit / ratio;
        }
        }
        jQuery('img#upload').imgAreaSelect({
        handles: true,
        keys: true,
        show: true,
        x1: 0,
        y1: 0,
        x2: xinit,
        y2: yinit,
        """)
        if (not current_theme_supports("custom-header", "flex-height")) and (not current_theme_supports("custom-header", "flex-width")):
            php_print("         aspectRatio: xinit + ':' + yinit,\n             ")
        # end if
        if (not current_theme_supports("custom-header", "flex-height")):
            php_print("         maxHeight: ")
            php_print(get_theme_support("custom-header", "height"))
            php_print(",\n              ")
        # end if
        if (not current_theme_supports("custom-header", "flex-width")):
            php_print("         maxWidth: ")
            php_print(get_theme_support("custom-header", "width"))
            php_print(",\n              ")
        # end if
        php_print("""           onInit: function () {
        jQuery('#width').val(xinit);
        jQuery('#height').val(yinit);
        },
        onSelectChange: function(img, c) {
        jQuery('#x1').val(c.x1);
        jQuery('#y1').val(c.y1);
        jQuery('#width').val(c.width);
        jQuery('#height').val(c.height);
        }
        });
        });
        </script>
        """)
    # end def js_2
    #// 
    #// Display first step of custom header image page.
    #// 
    #// @since 2.1.0
    #//
    def step_1(self):
        
        self.process_default_headers()
        php_print("\n<div class=\"wrap\">\n<h1>")
        _e("Custom Header")
        php_print("</h1>\n\n        ")
        if current_user_can("customize"):
            php_print("<div class=\"notice notice-info hide-if-no-customize\">\n    <p>\n           ")
            printf(__("You can now manage and live-preview Custom Header in the <a href=\"%s\">Customizer</a>."), admin_url("customize.php?autofocus[control]=header_image"))
            php_print(" </p>\n</div>\n      ")
        # end if
        php_print("\n       ")
        if (not php_empty(lambda : self.updated)):
            php_print("<div id=\"message\" class=\"updated\">\n <p>\n           ")
            #// translators: %s: Home URL.
            printf(__("Header updated. <a href=\"%s\">Visit your site</a> to see how it looks."), home_url("/"))
            php_print(" </p>\n</div>\n      ")
        # end if
        php_print("\n<h2>")
        _e("Header Image")
        php_print("""</h2>
        <table class=\"form-table\" role=\"presentation\">
        <tbody>
        """)
        if get_custom_header() or display_header_text():
            php_print("<tr>\n<th scope=\"row\">")
            _e("Preview")
            php_print("</th>\n<td>\n            ")
            if self.admin_image_div_callback:
                php_call_user_func(self.admin_image_div_callback)
            else:
                custom_header = get_custom_header()
                header_image = get_header_image()
                if header_image:
                    header_image_style = "background-image:url(" + esc_url(header_image) + ");"
                else:
                    header_image_style = ""
                # end if
                if custom_header.width:
                    header_image_style += "max-width:" + custom_header.width + "px;"
                # end if
                if custom_header.height:
                    header_image_style += "height:" + custom_header.height + "px;"
                # end if
                php_print(" <div id=\"headimg\" style=\"")
                php_print(header_image_style)
                php_print("\">\n                ")
                if display_header_text():
                    style = " style=\"color:#" + get_header_textcolor() + ";\""
                else:
                    style = " style=\"display:none;\""
                # end if
                php_print("     <h1><a id=\"name\" class=\"displaying-header-text\" ")
                php_print(style)
                php_print(" onclick=\"return false;\" href=\"")
                bloginfo("url")
                php_print("\" tabindex=\"-1\">")
                bloginfo("name")
                php_print("</a></h1>\n      <div id=\"desc\" class=\"displaying-header-text\" ")
                php_print(style)
                php_print(">")
                bloginfo("description")
                php_print("</div>\n </div>\n            ")
            # end if
            php_print("</td>\n</tr>\n       ")
        # end if
        php_print("\n       ")
        if current_user_can("upload_files") and current_theme_supports("custom-header", "uploads"):
            php_print("<tr>\n<th scope=\"row\">")
            _e("Select Image")
            php_print("</th>\n<td>\n    <p>")
            _e("You can select an image to be shown at the top of your site by uploading from your computer or choosing from your media library. After selecting an image you will be able to crop it.")
            php_print("<br />\n         ")
            if (not current_theme_supports("custom-header", "flex-height")) and (not current_theme_supports("custom-header", "flex-width")):
                #// translators: 1: Image width in pixels, 2: Image height in pixels.
                printf(__("Images of exactly <strong>%1$d &times; %2$d pixels</strong> will be used as-is.") + "<br />", get_theme_support("custom-header", "width"), get_theme_support("custom-header", "height"))
            elif current_theme_supports("custom-header", "flex-height"):
                if (not current_theme_supports("custom-header", "flex-width")):
                    printf(__("Images should be at least %s wide.") + " ", php_sprintf("<strong>" + __("%d pixels") + "</strong>", get_theme_support("custom-header", "width")))
                # end if
            elif current_theme_supports("custom-header", "flex-width"):
                if (not current_theme_supports("custom-header", "flex-height")):
                    printf(__("Images should be at least %s tall.") + " ", php_sprintf("<strong>" + __("%d pixels") + "</strong>", get_theme_support("custom-header", "height")))
                # end if
            # end if
            if current_theme_supports("custom-header", "flex-height") or current_theme_supports("custom-header", "flex-width"):
                if current_theme_supports("custom-header", "width"):
                    printf(__("Suggested width is %s.") + " ", php_sprintf("<strong>" + __("%d pixels") + "</strong>", get_theme_support("custom-header", "width")))
                # end if
                if current_theme_supports("custom-header", "height"):
                    printf(__("Suggested height is %s.") + " ", php_sprintf("<strong>" + __("%d pixels") + "</strong>", get_theme_support("custom-header", "height")))
                # end if
            # end if
            php_print(" </p>\n  <form enctype=\"multipart/form-data\" id=\"upload-form\" class=\"wp-upload-form\" method=\"post\" action=\"")
            php_print(esc_url(add_query_arg("step", 2)))
            php_print("\">\n    <p>\n       <label for=\"upload\">")
            _e("Choose an image from your computer:")
            php_print("""</label><br />
            <input type=\"file\" id=\"upload\" name=\"import\" />
            <input type=\"hidden\" name=\"action\" value=\"save\" />
            """)
            wp_nonce_field("custom-header-upload", "_wpnonce-custom-header-upload")
            php_print("         ")
            submit_button(__("Upload"), "", "submit", False)
            php_print(" </p>\n          ")
            modal_update_href = esc_url(add_query_arg(Array({"page": "custom-header", "step": 2, "_wpnonce-custom-header-upload": wp_create_nonce("custom-header-upload")}), admin_url("themes.php")))
            php_print(" <p>\n       <label for=\"choose-from-library-link\">")
            _e("Or choose an image from your media library:")
            php_print("</label><br />\n     <button id=\"choose-from-library-link\" class=\"button\"\n          data-update-link=\"")
            php_print(esc_attr(modal_update_href))
            php_print("\"\n         data-choose=\"")
            esc_attr_e("Choose a Custom Header")
            php_print("\"\n         data-update=\"")
            esc_attr_e("Set as header")
            php_print("\">")
            _e("Choose Image")
            php_print("""</button>
            </p>
            </form>
            </td>
            </tr>
            """)
        # end if
        php_print("""</tbody>
        </table>
        <form method=\"post\" action=\"""")
        php_print(esc_url(add_query_arg("step", 1)))
        php_print("\">\n        ")
        submit_button(None, "screen-reader-text", "save-header-options", False)
        php_print("<table class=\"form-table\" role=\"presentation\">\n<tbody>\n        ")
        if get_uploaded_header_images():
            php_print("<tr>\n<th scope=\"row\">")
            _e("Uploaded Images")
            php_print("</th>\n<td>\n    <p>")
            _e("You can choose one of your previously uploaded headers, or show a random one.")
            php_print("</p>\n           ")
            self.show_header_selector("uploaded")
            php_print("</td>\n</tr>\n           ")
        # end if
        if (not php_empty(lambda : self.default_headers)):
            php_print("<tr>\n<th scope=\"row\">")
            _e("Default Images")
            php_print("</th>\n<td>\n            ")
            if current_theme_supports("custom-header", "uploads"):
                php_print(" <p>")
                _e("If you don&lsquo;t want to upload your own image, you can use one of these cool headers, or show a random one.")
                php_print("</p>\n   ")
            else:
                php_print(" <p>")
                _e("You can use one of these cool headers or show a random one on each page.")
                php_print("</p>\n   ")
            # end if
            php_print("         ")
            self.show_header_selector("default")
            php_print("</td>\n</tr>\n           ")
        # end if
        if get_header_image():
            php_print("<tr>\n<th scope=\"row\">")
            _e("Remove Image")
            php_print("</th>\n<td>\n    <p>")
            _e("This will remove the header image. You will not be able to restore any customizations.")
            php_print("</p>\n           ")
            submit_button(__("Remove Header Image"), "", "removeheader", False)
            php_print("</td>\n</tr>\n           ")
        # end if
        default_image = php_sprintf(get_theme_support("custom-header", "default-image"), get_template_directory_uri(), get_stylesheet_directory_uri())
        if default_image and get_header_image() != default_image:
            php_print("<tr>\n<th scope=\"row\">")
            _e("Reset Image")
            php_print("</th>\n<td>\n    <p>")
            _e("This will restore the original header image. You will not be able to restore any customizations.")
            php_print("</p>\n           ")
            submit_button(__("Restore Original Header Image"), "", "resetheader", False)
            php_print("</td>\n</tr>\n   ")
        # end if
        php_print("""</tbody>
        </table>
        """)
        if current_theme_supports("custom-header", "header-text"):
            php_print("\n<h2>")
            _e("Header Text")
            php_print("""</h2>
            <table class=\"form-table\" role=\"presentation\">
            <tbody>
            <tr>
            <th scope=\"row\">""")
            _e("Header Text")
            php_print("""</th>
            <td>
            <p>
            <label><input type=\"checkbox\" name=\"display-header-text\" id=\"display-header-text\"""")
            checked(display_header_text())
            php_print(" /> ")
            _e("Show header text with your image.")
            php_print("""</label>
            </p>
            </td>
            </tr>
            <tr class=\"displaying-header-text\">
            <th scope=\"row\">""")
            _e("Text Color")
            php_print("""</th>
            <td>
            <p>
            """)
            default_color = ""
            if current_theme_supports("custom-header", "default-text-color"):
                default_color = get_theme_support("custom-header", "default-text-color")
                if default_color and False == php_strpos(default_color, "#"):
                    default_color = "#" + default_color
                # end if
            # end if
            default_color_attr = " data-default-color=\"" + esc_attr(default_color) + "\"" if default_color else ""
            header_textcolor = get_header_textcolor() if display_header_text() else get_theme_support("custom-header", "default-text-color")
            if header_textcolor and False == php_strpos(header_textcolor, "#"):
                header_textcolor = "#" + header_textcolor
            # end if
            php_print("<input type=\"text\" name=\"text-color\" id=\"text-color\" value=\"" + esc_attr(header_textcolor) + "\"" + default_color_attr + " />")
            if default_color:
                #// translators: %s: Default text color.
                php_print(" <span class=\"description hide-if-js\">" + php_sprintf(_x("Default: %s", "color"), esc_html(default_color)) + "</span>")
            # end if
            php_print("""   </p>
            </td>
            </tr>
            </tbody>
            </table>
            """)
        # end if
        #// 
        #// Fires just before the submit button in the custom header options form.
        #// 
        #// @since 3.1.0
        #//
        do_action("custom_header_options")
        wp_nonce_field("custom-header-options", "_wpnonce-custom-header-options")
        php_print("\n       ")
        submit_button(None, "primary", "save-header-options")
        php_print("""</form>
        </div>
        """)
    # end def step_1
    #// 
    #// Display second step of custom header image page.
    #// 
    #// @since 2.1.0
    #//
    def step_2(self):
        
        check_admin_referer("custom-header-upload", "_wpnonce-custom-header-upload")
        if (not current_theme_supports("custom-header", "uploads")):
            wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("The current theme does not support uploading a custom header image.") + "</p>", 403)
        # end if
        if php_empty(lambda : PHP_POST) and (php_isset(lambda : PHP_REQUEST["file"])):
            attachment_id = absint(PHP_REQUEST["file"])
            file = get_attached_file(attachment_id, True)
            url = wp_get_attachment_image_src(attachment_id, "full")
            url = url[0]
        elif (php_isset(lambda : PHP_POST)):
            data = self.step_2_manage_upload()
            attachment_id = data["attachment_id"]
            file = data["file"]
            url = data["url"]
        # end if
        if php_file_exists(file):
            width, height, type, attr = php_no_error(lambda: getimagesize(file))
        else:
            data = wp_get_attachment_metadata(attachment_id)
            height = data["height"] if (php_isset(lambda : data["height"])) else 0
            width = data["width"] if (php_isset(lambda : data["width"])) else 0
            data = None
        # end if
        max_width = 0
        #// For flex, limit size of image displayed to 1500px unless theme says otherwise.
        if current_theme_supports("custom-header", "flex-width"):
            max_width = 1500
        # end if
        if current_theme_supports("custom-header", "max-width"):
            max_width = php_max(max_width, get_theme_support("custom-header", "max-width"))
        # end if
        max_width = php_max(max_width, get_theme_support("custom-header", "width"))
        #// If flexible height isn't supported and the image is the exact right size.
        if (not current_theme_supports("custom-header", "flex-height")) and (not current_theme_supports("custom-header", "flex-width")) and get_theme_support("custom-header", "width") == width and get_theme_support("custom-header", "height") == height:
            #// Add the metadata.
            if php_file_exists(file):
                wp_update_attachment_metadata(attachment_id, wp_generate_attachment_metadata(attachment_id, file))
            # end if
            self.set_header_image(compact("url", "attachment_id", "width", "height"))
            #// 
            #// Fires after the header image is set or an error is returned.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string $file          Path to the file.
            #// @param int    $attachment_id Attachment ID.
            #//
            do_action("wp_create_file_in_uploads", file, attachment_id)
            #// For replication.
            return self.finished()
        elif width > max_width:
            oitar = width / max_width
            image = wp_crop_image(attachment_id, 0, 0, width, height, max_width, height / oitar, False, php_str_replace(wp_basename(file), "midsize-" + wp_basename(file), file))
            if (not image) or is_wp_error(image):
                wp_die(__("Image could not be processed. Please go back and try again."), __("Image Processing Error"))
            # end if
            #// This filter is documented in wp-admin/includes/class-custom-image-header.php
            image = apply_filters("wp_create_file_in_uploads", image, attachment_id)
            #// For replication.
            url = php_str_replace(wp_basename(url), wp_basename(image), url)
            width = width / oitar
            height = height / oitar
        else:
            oitar = 1
        # end if
        php_print("\n<div class=\"wrap\">\n<h1>")
        _e("Crop Header Image")
        php_print("</h1>\n\n<form method=\"post\" action=\"")
        php_print(esc_url(add_query_arg("step", 3)))
        php_print("\">\n    <p class=\"hide-if-no-js\">")
        _e("Choose the part of the image you want to use as your header.")
        php_print("</p>\n   <p class=\"hide-if-js\"><strong>")
        _e("You need JavaScript to choose a part of the image.")
        php_print("""</strong></p>
        <div id=\"crop_image\" style=\"position: relative\">
        <img src=\"""")
        php_print(esc_url(url))
        php_print("\" id=\"upload\" width=\"")
        php_print(width)
        php_print("\" height=\"")
        php_print(height)
        php_print("""\" alt=\"\" />
        </div>
        <input type=\"hidden\" name=\"x1\" id=\"x1\" value=\"0\"/>
        <input type=\"hidden\" name=\"y1\" id=\"y1\" value=\"0\"/>
        <input type=\"hidden\" name=\"width\" id=\"width\" value=\"""")
        php_print(esc_attr(width))
        php_print("\"/>\n   <input type=\"hidden\" name=\"height\" id=\"height\" value=\"")
        php_print(esc_attr(height))
        php_print("\"/>\n   <input type=\"hidden\" name=\"attachment_id\" id=\"attachment_id\" value=\"")
        php_print(esc_attr(attachment_id))
        php_print("\" />\n  <input type=\"hidden\" name=\"oitar\" id=\"oitar\" value=\"")
        php_print(esc_attr(oitar))
        php_print("\" />\n      ")
        if php_empty(lambda : PHP_POST) and (php_isset(lambda : PHP_REQUEST["file"])):
            php_print(" <input type=\"hidden\" name=\"create-new-attachment\" value=\"true\" />\n   ")
        # end if
        php_print("     ")
        wp_nonce_field("custom-header-crop-image")
        php_print("\n   <p class=\"submit\">\n      ")
        submit_button(__("Crop and Publish"), "primary", "submit", False)
        php_print("     ")
        if (php_isset(lambda : oitar)) and 1 == oitar and current_theme_supports("custom-header", "flex-height") or current_theme_supports("custom-header", "flex-width"):
            submit_button(__("Skip Cropping, Publish Image as Is"), "", "skip-cropping", False)
        # end if
        php_print("""   </p>
        </form>
        </div>
        """)
    # end def step_2
    #// 
    #// Upload the file to be cropped in the second step.
    #// 
    #// @since 3.4.0
    #//
    def step_2_manage_upload(self):
        
        overrides = Array({"test_form": False})
        uploaded_file = PHP_FILES["import"]
        wp_filetype = wp_check_filetype_and_ext(uploaded_file["tmp_name"], uploaded_file["name"])
        if (not wp_match_mime_types("image", wp_filetype["type"])):
            wp_die(__("The uploaded file is not a valid image. Please try again."))
        # end if
        file = wp_handle_upload(uploaded_file, overrides)
        if (php_isset(lambda : file["error"])):
            wp_die(file["error"], __("Image Upload Error"))
        # end if
        url = file["url"]
        type = file["type"]
        file = file["file"]
        filename = wp_basename(file)
        #// Construct the object array.
        object = Array({"post_title": filename, "post_content": url, "post_mime_type": type, "guid": url, "context": "custom-header"})
        #// Save the data.
        attachment_id = wp_insert_attachment(object, file)
        return compact("attachment_id", "file", "filename", "url", "type")
    # end def step_2_manage_upload
    #// 
    #// Display third step of custom header image page.
    #// 
    #// @since 2.1.0
    #// @since 4.4.0 Switched to using wp_get_attachment_url() instead of the guid
    #// for retrieving the header image URL.
    #//
    def step_3(self):
        global PHP_POST
        check_admin_referer("custom-header-crop-image")
        if (not current_theme_supports("custom-header", "uploads")):
            wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("The current theme does not support uploading a custom header image.") + "</p>", 403)
        # end if
        if (not php_empty(lambda : PHP_POST["skip-cropping"])) and (not current_theme_supports("custom-header", "flex-height") or current_theme_supports("custom-header", "flex-width")):
            wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("The current theme does not support a flexible sized header image.") + "</p>", 403)
        # end if
        if PHP_POST["oitar"] > 1:
            PHP_POST["x1"] = PHP_POST["x1"] * PHP_POST["oitar"]
            PHP_POST["y1"] = PHP_POST["y1"] * PHP_POST["oitar"]
            PHP_POST["width"] = PHP_POST["width"] * PHP_POST["oitar"]
            PHP_POST["height"] = PHP_POST["height"] * PHP_POST["oitar"]
        # end if
        attachment_id = absint(PHP_POST["attachment_id"])
        original = get_attached_file(attachment_id)
        dimensions = self.get_header_dimensions(Array({"height": PHP_POST["height"], "width": PHP_POST["width"]}))
        height = dimensions["dst_height"]
        width = dimensions["dst_width"]
        if php_empty(lambda : PHP_POST["skip-cropping"]):
            cropped = wp_crop_image(attachment_id, int(PHP_POST["x1"]), int(PHP_POST["y1"]), int(PHP_POST["width"]), int(PHP_POST["height"]), width, height)
        elif (not php_empty(lambda : PHP_POST["create-new-attachment"])):
            cropped = _copy_image_file(attachment_id)
        else:
            cropped = get_attached_file(attachment_id)
        # end if
        if (not cropped) or is_wp_error(cropped):
            wp_die(__("Image could not be processed. Please go back and try again."), __("Image Processing Error"))
        # end if
        #// This filter is documented in wp-admin/includes/class-custom-image-header.php
        cropped = apply_filters("wp_create_file_in_uploads", cropped, attachment_id)
        #// For replication.
        object = self.create_attachment_object(cropped, attachment_id)
        if (not php_empty(lambda : PHP_POST["create-new-attachment"])):
            object["ID"] = None
        # end if
        #// Update the attachment.
        attachment_id = self.insert_attachment(object, cropped)
        url = wp_get_attachment_url(attachment_id)
        self.set_header_image(compact("url", "attachment_id", "width", "height"))
        #// Cleanup.
        medium = php_str_replace(wp_basename(original), "midsize-" + wp_basename(original), original)
        if php_file_exists(medium):
            wp_delete_file(medium)
        # end if
        if php_empty(lambda : PHP_POST["create-new-attachment"]) and php_empty(lambda : PHP_POST["skip-cropping"]):
            wp_delete_file(original)
        # end if
        return self.finished()
    # end def step_3
    #// 
    #// Display last step of custom header image page.
    #// 
    #// @since 2.1.0
    #//
    def finished(self):
        
        self.updated = True
        self.step_1()
    # end def finished
    #// 
    #// Display the page based on the current step.
    #// 
    #// @since 2.1.0
    #//
    def admin_page(self):
        
        if (not current_user_can("edit_theme_options")):
            wp_die(__("Sorry, you are not allowed to customize headers."))
        # end if
        step = self.step()
        if 2 == step:
            self.step_2()
        elif 3 == step:
            self.step_3()
        else:
            self.step_1()
        # end if
    # end def admin_page
    #// 
    #// Unused since 3.5.0.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $form_fields
    #// @return array $form_fields
    #//
    def attachment_fields_to_edit(self, form_fields=None):
        
        return form_fields
    # end def attachment_fields_to_edit
    #// 
    #// Unused since 3.5.0.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $tabs
    #// @return array $tabs
    #//
    def filter_upload_tabs(self, tabs=None):
        
        return tabs
    # end def filter_upload_tabs
    #// 
    #// Choose a header image, selected from existing uploaded and default headers,
    #// or provide an array of uploaded header data (either new, or from media library).
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $choice Which header image to select. Allows for values of 'random-default-image',
    #// for randomly cycling among the default images; 'random-uploaded-image', for randomly cycling
    #// among the uploaded images; the key of a default image registered for that theme; and
    #// the key of an image uploaded for that theme (the attachment ID of the image).
    #// Or an array of arguments: attachment_id, url, width, height. All are required.
    #//
    def set_header_image(self, choice=None):
        
        if php_is_array(choice) or php_is_object(choice):
            choice = choice
            if (not (php_isset(lambda : choice["attachment_id"]))) or (not (php_isset(lambda : choice["url"]))):
                return
            # end if
            choice["url"] = esc_url_raw(choice["url"])
            header_image_data = Array({"attachment_id": choice["attachment_id"], "url": choice["url"], "thumbnail_url": choice["url"], "height": choice["height"], "width": choice["width"]})
            update_post_meta(choice["attachment_id"], "_wp_attachment_is_custom_header", get_stylesheet())
            set_theme_mod("header_image", choice["url"])
            set_theme_mod("header_image_data", header_image_data)
            return
        # end if
        if php_in_array(choice, Array("remove-header", "random-default-image", "random-uploaded-image")):
            set_theme_mod("header_image", choice)
            remove_theme_mod("header_image_data")
            return
        # end if
        uploaded = get_uploaded_header_images()
        if uploaded and (php_isset(lambda : uploaded[choice])):
            header_image_data = uploaded[choice]
        else:
            self.process_default_headers()
            if (php_isset(lambda : self.default_headers[choice])):
                header_image_data = self.default_headers[choice]
            else:
                return
            # end if
        # end if
        set_theme_mod("header_image", esc_url_raw(header_image_data["url"]))
        set_theme_mod("header_image_data", header_image_data)
    # end def set_header_image
    #// 
    #// Remove a header image.
    #// 
    #// @since 3.4.0
    #//
    def remove_header_image(self):
        
        self.set_header_image("remove-header")
    # end def remove_header_image
    #// 
    #// Reset a header image to the default image for the theme.
    #// 
    #// This method does not do anything if the theme does not have a default header image.
    #// 
    #// @since 3.4.0
    #//
    def reset_header_image(self):
        
        self.process_default_headers()
        default = get_theme_support("custom-header", "default-image")
        if (not default):
            self.remove_header_image()
            return
        # end if
        default = php_sprintf(default, get_template_directory_uri(), get_stylesheet_directory_uri())
        default_data = Array()
        for header,details in self.default_headers:
            if details["url"] == default:
                default_data = details
                break
            # end if
        # end for
        set_theme_mod("header_image", default)
        set_theme_mod("header_image_data", default_data)
    # end def reset_header_image
    #// 
    #// Calculate width and height based on what the currently selected theme supports.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array $dimensions
    #// @return array dst_height and dst_width of header image.
    #//
    def get_header_dimensions(self, dimensions=None):
        
        max_width = 0
        width = absint(dimensions["width"])
        height = absint(dimensions["height"])
        theme_height = get_theme_support("custom-header", "height")
        theme_width = get_theme_support("custom-header", "width")
        has_flex_width = current_theme_supports("custom-header", "flex-width")
        has_flex_height = current_theme_supports("custom-header", "flex-height")
        has_max_width = current_theme_supports("custom-header", "max-width")
        dst = Array({"dst_height": None, "dst_width": None})
        #// For flex, limit size of image displayed to 1500px unless theme says otherwise.
        if has_flex_width:
            max_width = 1500
        # end if
        if has_max_width:
            max_width = php_max(max_width, get_theme_support("custom-header", "max-width"))
        # end if
        max_width = php_max(max_width, theme_width)
        if has_flex_height and (not has_flex_width) or width > max_width:
            dst["dst_height"] = absint(height * max_width / width)
        elif has_flex_height and has_flex_width:
            dst["dst_height"] = height
        else:
            dst["dst_height"] = theme_height
        # end if
        if has_flex_width and (not has_flex_height) or width > max_width:
            dst["dst_width"] = absint(width * max_width / width)
        elif has_flex_width and has_flex_height:
            dst["dst_width"] = width
        else:
            dst["dst_width"] = theme_width
        # end if
        return dst
    # end def get_header_dimensions
    #// 
    #// Create an attachment 'object'.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $cropped              Cropped image URL.
    #// @param int    $parent_attachment_id Attachment ID of parent image.
    #// @return array Attachment object.
    #//
    def create_attachment_object(self, cropped=None, parent_attachment_id=None):
        
        parent = get_post(parent_attachment_id)
        parent_url = wp_get_attachment_url(parent.ID)
        url = php_str_replace(wp_basename(parent_url), wp_basename(cropped), parent_url)
        size = php_no_error(lambda: getimagesize(cropped))
        image_type = size["mime"] if size else "image/jpeg"
        object = Array({"ID": parent_attachment_id, "post_title": wp_basename(cropped), "post_mime_type": image_type, "guid": url, "context": "custom-header", "post_parent": parent_attachment_id})
        return object
    # end def create_attachment_object
    #// 
    #// Insert an attachment and its metadata.
    #// 
    #// @since 3.9.0
    #// 
    #// @param array  $object  Attachment object.
    #// @param string $cropped Cropped image URL.
    #// @return int Attachment ID.
    #//
    def insert_attachment(self, object=None, cropped=None):
        
        parent_id = object["post_parent"] if (php_isset(lambda : object["post_parent"])) else None
        object["post_parent"] = None
        attachment_id = wp_insert_attachment(object, cropped)
        metadata = wp_generate_attachment_metadata(attachment_id, cropped)
        #// If this is a crop, save the original attachment ID as metadata.
        if parent_id:
            metadata["attachment_parent"] = parent_id
        # end if
        #// 
        #// Filters the header image attachment metadata.
        #// 
        #// @since 3.9.0
        #// 
        #// @see wp_generate_attachment_metadata()
        #// 
        #// @param array $metadata Attachment metadata.
        #//
        metadata = apply_filters("wp_header_image_attachment_metadata", metadata)
        wp_update_attachment_metadata(attachment_id, metadata)
        return attachment_id
    # end def insert_attachment
    #// 
    #// Gets attachment uploaded by Media Manager, crops it, then saves it as a
    #// new object. Returns JSON-encoded object details.
    #// 
    #// @since 3.9.0
    #//
    def ajax_header_crop(self):
        
        check_ajax_referer("image_editor-" + PHP_POST["id"], "nonce")
        if (not current_user_can("edit_theme_options")):
            wp_send_json_error()
        # end if
        if (not current_theme_supports("custom-header", "uploads")):
            wp_send_json_error()
        # end if
        crop_details = PHP_POST["cropDetails"]
        dimensions = self.get_header_dimensions(Array({"height": crop_details["height"], "width": crop_details["width"]}))
        attachment_id = absint(PHP_POST["id"])
        cropped = wp_crop_image(attachment_id, int(crop_details["x1"]), int(crop_details["y1"]), int(crop_details["width"]), int(crop_details["height"]), int(dimensions["dst_width"]), int(dimensions["dst_height"]))
        if (not cropped) or is_wp_error(cropped):
            wp_send_json_error(Array({"message": __("Image could not be processed. Please go back and try again.")}))
        # end if
        #// This filter is documented in wp-admin/includes/class-custom-image-header.php
        cropped = apply_filters("wp_create_file_in_uploads", cropped, attachment_id)
        #// For replication.
        object = self.create_attachment_object(cropped, attachment_id)
        previous = self.get_previous_crop(object)
        if previous:
            object["ID"] = previous
        else:
            object["ID"] = None
        # end if
        new_attachment_id = self.insert_attachment(object, cropped)
        object["attachment_id"] = new_attachment_id
        object["url"] = wp_get_attachment_url(new_attachment_id)
        object["width"] = dimensions["dst_width"]
        object["height"] = dimensions["dst_height"]
        wp_send_json_success(object)
    # end def ajax_header_crop
    #// 
    #// Given an attachment ID for a header image, updates its "last used"
    #// timestamp to now.
    #// 
    #// Triggered when the user tries adds a new header image from the
    #// Media Manager, even if s/he doesn't save that change.
    #// 
    #// @since 3.9.0
    #//
    def ajax_header_add(self):
        
        check_ajax_referer("header-add", "nonce")
        if (not current_user_can("edit_theme_options")):
            wp_send_json_error()
        # end if
        attachment_id = absint(PHP_POST["attachment_id"])
        if attachment_id < 1:
            wp_send_json_error()
        # end if
        key = "_wp_attachment_custom_header_last_used_" + get_stylesheet()
        update_post_meta(attachment_id, key, time())
        update_post_meta(attachment_id, "_wp_attachment_is_custom_header", get_stylesheet())
        wp_send_json_success()
    # end def ajax_header_add
    #// 
    #// Given an attachment ID for a header image, unsets it as a user-uploaded
    #// header image for the current theme.
    #// 
    #// Triggered when the user clicks the overlay "X" button next to each image
    #// choice in the Customizer's Header tool.
    #// 
    #// @since 3.9.0
    #//
    def ajax_header_remove(self):
        
        check_ajax_referer("header-remove", "nonce")
        if (not current_user_can("edit_theme_options")):
            wp_send_json_error()
        # end if
        attachment_id = absint(PHP_POST["attachment_id"])
        if attachment_id < 1:
            wp_send_json_error()
        # end if
        key = "_wp_attachment_custom_header_last_used_" + get_stylesheet()
        delete_post_meta(attachment_id, key)
        delete_post_meta(attachment_id, "_wp_attachment_is_custom_header", get_stylesheet())
        wp_send_json_success()
    # end def ajax_header_remove
    #// 
    #// Updates the last-used postmeta on a header image attachment after saving a new header image via the Customizer.
    #// 
    #// @since 3.9.0
    #// 
    #// @param WP_Customize_Manager $wp_customize Customize manager.
    #//
    def customize_set_last_used(self, wp_customize=None):
        
        header_image_data_setting = wp_customize.get_setting("header_image_data")
        if (not header_image_data_setting):
            return
        # end if
        data = header_image_data_setting.post_value()
        if (not (php_isset(lambda : data["attachment_id"]))):
            return
        # end if
        attachment_id = data["attachment_id"]
        key = "_wp_attachment_custom_header_last_used_" + get_stylesheet()
        update_post_meta(attachment_id, key, time())
    # end def customize_set_last_used
    #// 
    #// Gets the details of default header images if defined.
    #// 
    #// @since 3.9.0
    #// 
    #// @return array Default header images.
    #//
    def get_default_header_images(self):
        
        self.process_default_headers()
        #// Get the default image if there is one.
        default = get_theme_support("custom-header", "default-image")
        if (not default):
            #// If not, easy peasy.
            return self.default_headers
        # end if
        default = php_sprintf(default, get_template_directory_uri(), get_stylesheet_directory_uri())
        already_has_default = False
        for k,h in self.default_headers:
            if h["url"] == default:
                already_has_default = True
                break
            # end if
        # end for
        if already_has_default:
            return self.default_headers
        # end if
        #// If the one true image isn't included in the default set, prepend it.
        header_images = Array()
        header_images["default"] = Array({"url": default, "thumbnail_url": default, "description": "Default"})
        #// The rest of the set comes after.
        return php_array_merge(header_images, self.default_headers)
    # end def get_default_header_images
    #// 
    #// Gets the previously uploaded header images.
    #// 
    #// @since 3.9.0
    #// 
    #// @return array Uploaded header images.
    #//
    def get_uploaded_header_images(self):
        
        header_images = get_uploaded_header_images()
        timestamp_key = "_wp_attachment_custom_header_last_used_" + get_stylesheet()
        alt_text_key = "_wp_attachment_image_alt"
        for header_image in header_images:
            header_meta = get_post_meta(header_image["attachment_id"])
            header_image["timestamp"] = header_meta[timestamp_key] if (php_isset(lambda : header_meta[timestamp_key])) else ""
            header_image["alt_text"] = header_meta[alt_text_key] if (php_isset(lambda : header_meta[alt_text_key])) else ""
        # end for
        return header_images
    # end def get_uploaded_header_images
    #// 
    #// Get the ID of a previous crop from the same base image.
    #// 
    #// @since 4.9.0
    #// 
    #// @param  array $object A crop attachment object.
    #// @return int|false An attachment ID if one exists. False if none.
    #//
    def get_previous_crop(self, object=None):
        
        header_images = self.get_uploaded_header_images()
        #// Bail early if there are no header images.
        if php_empty(lambda : header_images):
            return False
        # end if
        previous = False
        for image in header_images:
            if image["attachment_parent"] == object["post_parent"]:
                previous = image["attachment_id"]
                break
            # end if
        # end for
        return previous
    # end def get_previous_crop
# end class Custom_Image_Header
