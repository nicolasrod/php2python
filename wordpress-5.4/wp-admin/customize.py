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
#// Theme Customize Screen.
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 3.4.0
#//
php_define("IFRAME_REQUEST", True)
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("customize")):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to customize this site.") + "</p>", 403)
# end if
#// 
#// @global WP_Scripts           $wp_scripts
#// @global WP_Customize_Manager $wp_customize
#//
global wp_scripts,wp_customize
php_check_if_defined("wp_scripts","wp_customize")
if wp_customize.changeset_post_id():
    changeset_post = get_post(wp_customize.changeset_post_id())
    if (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post.ID)):
        wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit this changeset.") + "</p>", 403)
    # end if
    missed_schedule = "future" == changeset_post.post_status and get_post_time("G", True, changeset_post) < time()
    if missed_schedule:
        #// 
        #// Note that an Ajax request spawns here instead of just calling `wp_publish_post( $changeset_post->ID )`.
        #// 
        #// Because WP_Customize_Manager is not instantiated for customize.php with the `settings_previewed=false`
        #// argument, settings cannot be reliably saved. Some logic short-circuits if the current value is the
        #// same as the value being saved. This is particularly true for options via `update_option()`.
        #// 
        #// By opening an Ajax request, this is avoided and the changeset is published. See #39221.
        #//
        nonces = wp_customize.get_nonces()
        request_args = Array({"nonce": nonces["save"], "customize_changeset_uuid": wp_customize.changeset_uuid(), "wp_customize": "on", "customize_changeset_status": "publish"})
        ob_start()
        php_print("     ")
        wp_print_scripts(Array("wp-util"))
        php_print("     <script>\n          wp.ajax.post( 'customize_save', ")
        php_print(wp_json_encode(request_args))
        php_print(" );\n        </script>\n     ")
        script = ob_get_clean()
        wp_die("<h1>" + __("Your scheduled changes just published") + "</h1>" + "<p><a href=\"" + esc_url(remove_query_arg("changeset_uuid")) + "\">" + __("Customize New Changes") + "</a></p>" + script, 200)
    # end if
    if php_in_array(get_post_status(changeset_post.ID), Array("publish", "trash"), True):
        wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("This changeset cannot be further modified.") + "</p>" + "<p><a href=\"" + esc_url(remove_query_arg("changeset_uuid")) + "\">" + __("Customize New Changes") + "</a></p>", 403)
    # end if
# end if
wp_reset_vars(Array("url", "return", "autofocus"))
if (not php_empty(lambda : url)):
    wp_customize.set_preview_url(wp_unslash(url))
# end if
if (not php_empty(lambda : return_)):
    wp_customize.set_return_url(wp_unslash(return_))
# end if
if (not php_empty(lambda : autofocus)) and php_is_array(autofocus):
    wp_customize.set_autofocus(wp_unslash(autofocus))
# end if
registered = wp_scripts.registered
wp_scripts = php_new_class("WP_Scripts", lambda : WP_Scripts())
wp_scripts.registered = registered
add_action("customize_controls_print_scripts", "print_head_scripts", 20)
add_action("customize_controls_print_footer_scripts", "_wp_footer_scripts")
add_action("customize_controls_print_styles", "print_admin_styles", 20)
#// 
#// Fires when Customizer controls are initialized, before scripts are enqueued.
#// 
#// @since 3.4.0
#//
do_action("customize_controls_init")
wp_enqueue_script("heartbeat")
wp_enqueue_script("customize-controls")
wp_enqueue_style("customize-controls")
#// 
#// Enqueue Customizer control scripts.
#// 
#// @since 3.4.0
#//
do_action("customize_controls_enqueue_scripts")
#// Let's roll.
php_header("Content-Type: " + get_option("html_type") + "; charset=" + get_option("blog_charset"))
wp_user_settings()
_wp_admin_html_begin()
body_class = "wp-core-ui wp-customizer js"
if wp_is_mobile():
    body_class += " mobile"
    php_print(" <meta name=\"viewport\" id=\"viewport-meta\" content=\"width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=1.2\" />\n   ")
# end if
if wp_customize.is_ios():
    body_class += " ios"
# end if
if is_rtl():
    body_class += " rtl"
# end if
body_class += " locale-" + sanitize_html_class(php_strtolower(php_str_replace("_", "-", get_user_locale())))
admin_title = php_sprintf(wp_customize.get_document_title_template(), __("Loading&hellip;"))
php_print("<title>")
php_print(admin_title)
php_print("""</title>
<script type=\"text/javascript\">
var ajaxurl = """)
php_print(wp_json_encode(admin_url("admin-ajax.php", "relative")))
php_print(""",
pagenow = 'customize';
</script>
""")
#// 
#// Fires when Customizer control styles are printed.
#// 
#// @since 3.4.0
#//
do_action("customize_controls_print_styles")
#// 
#// Fires when Customizer control scripts are printed.
#// 
#// @since 3.4.0
#//
do_action("customize_controls_print_scripts")
php_print("</head>\n<body class=\"")
php_print(esc_attr(body_class))
php_print("""\">
<div class=\"wp-full-overlay expanded\">
<form id=\"customize-controls\" class=\"wrap wp-full-overlay-sidebar\">
<div id=\"customize-header-actions\" class=\"wp-full-overlay-header\">
""")
save_text = __("Publish") if wp_customize.is_theme_active() else __("Activate &amp; Publish")
php_print("         <div id=\"customize-save-button-wrapper\" class=\"customize-save-button-wrapper\" >\n               ")
submit_button(save_text, "primary save", "save", False)
php_print("             <button id=\"publish-settings\" class=\"publish-settings button-primary button dashicons dashicons-admin-generic\" aria-label=\"")
esc_attr_e("Publish Settings")
php_print("""\" aria-expanded=\"false\" disabled></button>
</div>
<span class=\"spinner\"></span>
<button type=\"button\" class=\"customize-controls-preview-toggle\">
<span class=\"controls\">""")
_e("Customize")
php_print("</span>\n                <span class=\"preview\">")
_e("Preview")
php_print("</span>\n            </button>\n         <a class=\"customize-controls-close\" href=\"")
php_print(esc_url(wp_customize.get_return_url()))
php_print("\">\n                <span class=\"screen-reader-text\">")
_e("Close the Customizer and go back to the previous page")
php_print("""</span>
</a>
</div>
<div id=\"customize-sidebar-outer-content\">
<div id=\"customize-outer-theme-controls\">
<ul class=\"customize-outer-pane-parent\">""")
pass
php_print("""</ul>
</div>
</div>
<div id=\"widgets-right\" class=\"wp-clearfix\"><!-- For Widget Customizer, many widgets try to look for instances under div#widgets-right, so we have to add that ID to a container div in the Customizer for compat -->
<div id=\"customize-notifications-area\" class=\"customize-control-notifications-container\">
<ul></ul>
</div>
<div class=\"wp-full-overlay-sidebar-content\" tabindex=\"-1\">
<div id=\"customize-info\" class=\"accordion-section customize-info\">
<div class=\"accordion-section-title\">
<span class=\"preview-notice\">
""")
#// translators: %s: The site/panel title in the Customizer.
php_print(php_sprintf(__("You are customizing %s"), "<strong class=\"panel-title site-title\">" + get_bloginfo("name", "display") + "</strong>"))
php_print("                     </span>\n                       <button type=\"button\" class=\"customize-help-toggle dashicons dashicons-editor-help\" aria-expanded=\"false\"><span class=\"screen-reader-text\">")
_e("Help")
php_print("""</span></button>
</div>
<div class=\"customize-panel-description\">
""")
_e("The Customizer allows you to preview changes to your site before publishing them. You can navigate to different pages on your site within the preview. Edit shortcuts are shown for some editable elements.")
php_print("""                   </div>
</div>
<div id=\"customize-theme-controls\">
<ul class=\"customize-pane-parent\">""")
pass
php_print("""</ul>
</div>
</div>
</div>
<div id=\"customize-footer-actions\" class=\"wp-full-overlay-footer\">
<button type=\"button\" class=\"collapse-sidebar button\" aria-expanded=\"true\" aria-label=\"""")
php_print(esc_attr(_x("Hide Controls", "label for hide controls button without length constraints")))
php_print("\">\n                <span class=\"collapse-sidebar-arrow\"></span>\n                <span class=\"collapse-sidebar-label\">")
_ex("Hide Controls", "short (~12 characters) label for hide controls button")
php_print("</span>\n            </button>\n         ")
previewable_devices = wp_customize.get_previewable_devices()
php_print("         ")
if (not php_empty(lambda : previewable_devices)):
    php_print("         <div class=\"devices-wrapper\">\n               <div class=\"devices\">\n                   ")
    for device,settings in previewable_devices:
        php_print("                     ")
        if php_empty(lambda : settings["label"]):
            continue
        # end if
        active = (not php_empty(lambda : settings["default"]))
        class_ = "preview-" + device
        if active:
            class_ += " active"
        # end if
        php_print("                     <button type=\"button\" class=\"")
        php_print(esc_attr(class_))
        php_print("\" aria-pressed=\"")
        php_print(esc_attr(active))
        php_print("\" data-device=\"")
        php_print(esc_attr(device))
        php_print("\">\n                            <span class=\"screen-reader-text\">")
        php_print(esc_html(settings["label"]))
        php_print("</span>\n                        </button>\n                 ")
    # end for
    php_print("             </div>\n            </div>\n            ")
# end if
php_print("""       </div>
</form>
<div id=\"customize-preview\" class=\"wp-full-overlay-main\"></div>
""")
#// 
#// Prints templates, control scripts, and settings in the footer.
#// 
#// @since 3.4.0
#//
do_action("customize_controls_print_footer_scripts")
php_print("""</div>
</body>
</html>
""")
