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
#// Media settings administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_options")):
    wp_die(__("Sorry, you are not allowed to manage options for this site."))
# end if
title_ = __("Media Settings")
parent_file_ = "options-general.php"
media_options_help_ = "<p>" + __("You can set maximum sizes for images inserted into your written content; you can also insert an image as Full Size.") + "</p>"
if (not is_multisite()) and get_option("upload_url_path") or get_option("upload_path") != "wp-content/uploads" and get_option("upload_path"):
    media_options_help_ += "<p>" + __("Uploading Files allows you to choose the folder and path for storing your uploaded files.") + "</p>"
# end if
media_options_help_ += "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": media_options_help_}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/settings-media-screen/\">Documentation on Media Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(esc_html(title_))
php_print("""</h1>
<form action=\"options.php\" method=\"post\">
""")
settings_fields("media")
php_print("\n<h2 class=\"title\">")
_e("Image sizes")
php_print("</h2>\n<p>")
_e("The sizes listed below determine the maximum dimensions in pixels to use when adding an image to the Media Library.")
php_print("""</p>
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\">""")
_e("Thumbnail size")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Thumbnail size")
php_print("</span></legend>\n<label for=\"thumbnail_size_w\">")
_e("Width")
php_print("</label>\n<input name=\"thumbnail_size_w\" type=\"number\" step=\"1\" min=\"0\" id=\"thumbnail_size_w\" value=\"")
form_option("thumbnail_size_w")
php_print("\" class=\"small-text\" />\n<br />\n<label for=\"thumbnail_size_h\">")
_e("Height")
php_print("</label>\n<input name=\"thumbnail_size_h\" type=\"number\" step=\"1\" min=\"0\" id=\"thumbnail_size_h\" value=\"")
form_option("thumbnail_size_h")
php_print("\" class=\"small-text\" />\n</fieldset>\n<input name=\"thumbnail_crop\" type=\"checkbox\" id=\"thumbnail_crop\" value=\"1\" ")
checked("1", get_option("thumbnail_crop"))
php_print("/>\n<label for=\"thumbnail_crop\">")
_e("Crop thumbnail to exact dimensions (normally thumbnails are proportional)")
php_print("""</label>
</td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Medium size")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Medium size")
php_print("</span></legend>\n<label for=\"medium_size_w\">")
_e("Max Width")
php_print("</label>\n<input name=\"medium_size_w\" type=\"number\" step=\"1\" min=\"0\" id=\"medium_size_w\" value=\"")
form_option("medium_size_w")
php_print("\" class=\"small-text\" />\n<br />\n<label for=\"medium_size_h\">")
_e("Max Height")
php_print("</label>\n<input name=\"medium_size_h\" type=\"number\" step=\"1\" min=\"0\" id=\"medium_size_h\" value=\"")
form_option("medium_size_h")
php_print("""\" class=\"small-text\" />
</fieldset></td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Large size")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Large size")
php_print("</span></legend>\n<label for=\"large_size_w\">")
_e("Max Width")
php_print("</label>\n<input name=\"large_size_w\" type=\"number\" step=\"1\" min=\"0\" id=\"large_size_w\" value=\"")
form_option("large_size_w")
php_print("\" class=\"small-text\" />\n<br />\n<label for=\"large_size_h\">")
_e("Max Height")
php_print("</label>\n<input name=\"large_size_h\" type=\"number\" step=\"1\" min=\"0\" id=\"large_size_h\" value=\"")
form_option("large_size_h")
php_print("""\" class=\"small-text\" />
</fieldset></td>
</tr>
""")
do_settings_fields("media", "default")
php_print("</table>\n\n")
#// 
#// @global array $wp_settings
#//
if (php_isset(lambda : PHP_GLOBALS["wp_settings"]["media"]["embeds"])):
    php_print("<h2 class=\"title\">")
    _e("Embeds")
    php_print("</h2>\n<table class=\"form-table\" role=\"presentation\">\n  ")
    do_settings_fields("media", "embeds")
    php_print("</table>\n")
# end if
php_print("\n")
if (not is_multisite()):
    php_print("<h2 class=\"title\">")
    _e("Uploading Files")
    php_print("</h2>\n<table class=\"form-table\" role=\"presentation\">\n  ")
    #// If upload_url_path is not the default (empty), and upload_path is not the default ('wp-content/uploads' or empty).
    if get_option("upload_url_path") or get_option("upload_path") != "wp-content/uploads" and get_option("upload_path"):
        php_print("<tr>\n<th scope=\"row\"><label for=\"upload_path\">")
        _e("Store uploads in this folder")
        php_print("</label></th>\n<td><input name=\"upload_path\" type=\"text\" id=\"upload_path\" value=\"")
        php_print(esc_attr(get_option("upload_path")))
        php_print("\" class=\"regular-text code\" />\n<p class=\"description\">\n       ")
        #// translators: %s: wp-content/uploads
        php_printf(__("Default is %s"), "<code>wp-content/uploads</code>")
        php_print("""</p>
        </td>
        </tr>
        <tr>
        <th scope=\"row\"><label for=\"upload_url_path\">""")
        _e("Full URL path to files")
        php_print("</label></th>\n<td><input name=\"upload_url_path\" type=\"text\" id=\"upload_url_path\" value=\"")
        php_print(esc_attr(get_option("upload_url_path")))
        php_print("\" class=\"regular-text code\" />\n<p class=\"description\">")
        _e("Configuring this is optional. By default, it should be blank.")
        php_print("""</p>
        </td>
        </tr>
        <tr>
        <td colspan=\"2\" class=\"td-full\">
        """)
    else:
        php_print("<tr>\n<td class=\"td-full\">\n")
    # end if
    php_print("<label for=\"uploads_use_yearmonth_folders\">\n<input name=\"uploads_use_yearmonth_folders\" type=\"checkbox\" id=\"uploads_use_yearmonth_folders\" value=\"1\"")
    checked("1", get_option("uploads_use_yearmonth_folders"))
    php_print(" />\n    ")
    _e("Organize my uploads into month- and year-based folders")
    php_print("""</label>
    </td>
    </tr>
    """)
    do_settings_fields("media", "uploads")
    php_print("</table>\n")
# end if
php_print("\n")
do_settings_sections("media")
php_print("\n")
submit_button()
php_print("""
</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
