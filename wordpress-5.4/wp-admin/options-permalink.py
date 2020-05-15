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
#// Permalink Settings Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_options")):
    wp_die(__("Sorry, you are not allowed to manage options for this site."))
# end if
title = __("Permalink Settings")
parent_file = "options-general.php"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Permalinks are the permanent URLs to your individual pages and blog posts, as well as your category and tag archives. A permalink is the web address used to link to your content. The URL to each post should be permanent, and never change &#8212; hence the name permalink.") + "</p>" + "<p>" + __("This screen allows you to choose your permalink structure. You can choose from common settings or create custom URL structures.") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "permalink-settings", "title": __("Permalink Settings"), "content": "<p>" + __("Permalinks can contain useful information, such as the post date, title, or other elements. You can choose from any of the suggested permalink formats, or you can craft your own if you select Custom Structure.") + "</p>" + "<p>" + php_sprintf(__("If you pick an option other than Plain, your general URL path with structure tags (terms surrounded by %s) will also appear in the custom structure field and your path can be further modified there."), "<code>%</code>") + "</p>" + "<p>" + php_sprintf(__("When you assign multiple categories or tags to a post, only one can show up in the permalink: the lowest numbered category. This applies if your custom structure includes %1$s or %2$s."), "<code>%category%</code>", "<code>%tag%</code>") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "custom-structures", "title": __("Custom Structures"), "content": "<p>" + __("The Optional fields let you customize the &#8220;category&#8221; and &#8220;tag&#8221; base names that will appear in archive URLs. For example, the page listing all posts in the &#8220;Uncategorized&#8221; category could be <code>/topics/uncategorized</code> instead of <code>/category/uncategorized</code>.") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/settings-permalinks-screen/\">Documentation on Permalinks Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/using-permalinks/\">Documentation on Using Permalinks</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
home_path = get_home_path()
iis7_permalinks = iis7_supports_permalinks()
permalink_structure = get_option("permalink_structure")
prefix = ""
blog_prefix = ""
if (not got_url_rewrite()):
    prefix = "/index.php"
# end if
#// 
#// In a subdirectory configuration of multisite, the `/blog` prefix is used by
#// default on the main site to avoid collisions with other sites created on that
#// network. If the `permalink_structure` option has been changed to remove this
#// base prefix, WordPress core can no longer account for the possible collision.
#//
if is_multisite() and (not is_subdomain_install()) and is_main_site() and 0 == php_strpos(permalink_structure, "/blog/"):
    blog_prefix = "/blog"
# end if
category_base = get_option("category_base")
tag_base = get_option("tag_base")
update_required = False
if iis7_permalinks:
    if (not php_file_exists(home_path + "web.config")) and win_is_writable(home_path) or win_is_writable(home_path + "web.config"):
        writable = True
    else:
        writable = False
    # end if
elif is_nginx:
    writable = False
else:
    if (not php_file_exists(home_path + ".htaccess")) and php_is_writable(home_path) or php_is_writable(home_path + ".htaccess"):
        writable = True
    else:
        writable = False
        existing_rules = php_array_filter(extract_from_markers(home_path + ".htaccess", "WordPress"))
        new_rules = php_array_filter(php_explode("\n", wp_rewrite.mod_rewrite_rules()))
        update_required = new_rules != existing_rules
    # end if
# end if
using_index_permalinks = wp_rewrite.using_index_permalinks()
if (php_isset(lambda : PHP_POST["permalink_structure"])) or (php_isset(lambda : PHP_POST["category_base"])):
    check_admin_referer("update-permalink")
    if (php_isset(lambda : PHP_POST["permalink_structure"])):
        if (php_isset(lambda : PHP_POST["selection"])) and "custom" != PHP_POST["selection"]:
            permalink_structure = PHP_POST["selection"]
        else:
            permalink_structure = PHP_POST["permalink_structure"]
        # end if
        if (not php_empty(lambda : permalink_structure)):
            permalink_structure = php_preg_replace("#/+#", "/", "/" + php_str_replace("#", "", permalink_structure))
            if prefix and blog_prefix:
                permalink_structure = prefix + php_preg_replace("#^/?index\\.php#", "", permalink_structure)
            else:
                permalink_structure = blog_prefix + permalink_structure
            # end if
        # end if
        permalink_structure = sanitize_option("permalink_structure", permalink_structure)
        wp_rewrite.set_permalink_structure(permalink_structure)
    # end if
    if (php_isset(lambda : PHP_POST["category_base"])):
        category_base = PHP_POST["category_base"]
        if (not php_empty(lambda : category_base)):
            category_base = blog_prefix + php_preg_replace("#/+#", "/", "/" + php_str_replace("#", "", category_base))
        # end if
        wp_rewrite.set_category_base(category_base)
    # end if
    if (php_isset(lambda : PHP_POST["tag_base"])):
        tag_base = PHP_POST["tag_base"]
        if (not php_empty(lambda : tag_base)):
            tag_base = blog_prefix + php_preg_replace("#/+#", "/", "/" + php_str_replace("#", "", tag_base))
        # end if
        wp_rewrite.set_tag_base(tag_base)
    # end if
    message = __("Permalink structure updated.")
    if iis7_permalinks:
        if permalink_structure and (not using_index_permalinks) and (not writable):
            message = php_sprintf(__("You should update your %s file now."), "<code>web.config</code>")
        elif permalink_structure and (not using_index_permalinks) and writable:
            message = php_sprintf(__("Permalink structure updated. Remove write access on %s file now!"), "<code>web.config</code>")
        # end if
    elif (not is_nginx) and permalink_structure and (not using_index_permalinks) and (not writable) and update_required:
        message = php_sprintf(__("You should update your %s file now."), "<code>.htaccess</code>")
    # end if
    if (not get_settings_errors()):
        add_settings_error("general", "settings_updated", message, "success")
    # end if
    set_transient("settings_errors", get_settings_errors(), 30)
    wp_redirect(admin_url("options-permalink.php?settings-updated=true"))
    php_exit(0)
# end if
flush_rewrite_rules()
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n<h1>")
php_print(esc_html(title))
php_print("""</h1>
<form name=\"form\" action=\"options-permalink.php\" method=\"post\">
""")
wp_nonce_field("update-permalink")
php_print("\n   <p>\n   ")
printf(__("WordPress offers you the ability to create a custom URL structure for your permalinks and archives. Custom URL structures can improve the aesthetics, usability, and forward-compatibility of your links. A <a href=\"%s\">number of tags are available</a>, and here are some examples to get you started."), __("https://wordpress.org/support/article/using-permalinks/"))
php_print(" </p>\n\n")
if is_multisite() and (not is_subdomain_install()) and is_main_site() and 0 == php_strpos(permalink_structure, "/blog/"):
    permalink_structure = php_preg_replace("|^/?blog|", "", permalink_structure)
    category_base = php_preg_replace("|^/?blog|", "", category_base)
    tag_base = php_preg_replace("|^/?blog|", "", tag_base)
# end if
structures = Array({0: "", 1: prefix + "/%year%/%monthnum%/%day%/%postname%/", 2: prefix + "/%year%/%monthnum%/%postname%/", 3: prefix + "/" + _x("archives", "sample permalink base") + "/%post_id%", 4: prefix + "/%postname%/"})
php_print("<h2 class=\"title\">")
_e("Common Settings")
php_print("""</h2>
<table class=\"form-table permalink-structure\">
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"\" """)
checked("", permalink_structure)
php_print(" /> ")
_e("Plain")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home"))
php_print("""/?p=123</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures[1]))
php_print("\" ")
checked(structures[1], permalink_structure)
php_print(" /> ")
_e("Day and name")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix + prefix + "/" + gmdate("Y") + "/" + gmdate("m") + "/" + gmdate("d") + "/" + _x("sample-post", "sample permalink structure") + "/")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures[2]))
php_print("\" ")
checked(structures[2], permalink_structure)
php_print(" /> ")
_e("Month and name")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix + prefix + "/" + gmdate("Y") + "/" + gmdate("m") + "/" + _x("sample-post", "sample permalink structure") + "/")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures[3]))
php_print("\" ")
checked(structures[3], permalink_structure)
php_print(" /> ")
_e("Numeric")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix + prefix + "/" + _x("archives", "sample permalink base") + "/123")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures[4]))
php_print("\" ")
checked(structures[4], permalink_structure)
php_print(" /> ")
_e("Post name")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix + prefix + "/" + _x("sample-post", "sample permalink structure") + "/")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\">
<label><input name=\"selection\" id=\"custom_selection\" type=\"radio\" value=\"custom\" """)
checked((not php_in_array(permalink_structure, structures)))
php_print(" />\n            ")
_e("Custom Structure")
php_print("""           </label>
</th>
<td>
<code>""")
php_print(get_option("home") + blog_prefix)
php_print("</code>\n            <input name=\"permalink_structure\" id=\"permalink_structure\" type=\"text\" value=\"")
php_print(esc_attr(permalink_structure))
php_print("""\" class=\"regular-text code\" />
<div class=\"available-structure-tags hide-if-no-js\">
<div id=\"custom_selection_updated\" aria-live=\"assertive\" class=\"screen-reader-text\"></div>
""")
available_tags = Array({"year": __("%s (The year of the post, four digits, for example 2004.)"), "monthnum": __("%s (Month of the year, for example 05.)"), "day": __("%s (Day of the month, for example 28.)"), "hour": __("%s (Hour of the day, for example 15.)"), "minute": __("%s (Minute of the hour, for example 43.)"), "second": __("%s (Second of the minute, for example 33.)"), "post_id": __("%s (The unique ID of the post, for example 423.)"), "postname": __("%s (The sanitized post title (slug).)"), "category": __("%s (Category slug. Nested sub-categories appear as nested directories in the URL.)"), "author": __("%s (A sanitized version of the author name.)")})
#// 
#// Filters the list of available permalink structure tags on the Permalinks settings page.
#// 
#// @since 4.8.0
#// 
#// @param string[] $available_tags An array of key => value pairs of available permalink structure tags.
#//
available_tags = apply_filters("available_permalink_structure_tags", available_tags)
#// translators: %s: Permalink structure tag.
structure_tag_added = __("%s added to permalink structure")
#// translators: %s: Permalink structure tag.
structure_tag_already_used = __("%s (already used in permalink structure)")
if (not php_empty(lambda : available_tags)):
    php_print("                 <p>")
    _e("Available tags:")
    php_print("</p>\n                   <ul role=\"list\">\n                        ")
    for tag,explanation in available_tags:
        php_print("""                           <li>
        <button type=\"button\"
    class=\"button button-secondary\"
        aria-label=\"""")
        php_print(esc_attr(php_sprintf(explanation, tag)))
        php_print("\"\n                                     data-added=\"")
        php_print(esc_attr(php_sprintf(structure_tag_added, tag)))
        php_print("\"\n                                     data-used=\"")
        php_print(esc_attr(php_sprintf(structure_tag_already_used, tag)))
        php_print("\">\n                                    ")
        php_print("%" + tag + "%")
        php_print("                             </button>\n                         </li>\n                         ")
    # end for
    php_print("                 </ul>\n             ")
# end if
php_print("""           </div>
</td>
</tr>
</table>
<h2 class=\"title\">""")
_e("Optional")
php_print("</h2>\n<p>\n")
#// translators: %s: Placeholder that must come at the start of the URL.
printf(__("If you like, you may enter custom structures for your category and tag URLs here. For example, using <code>topics</code> as your category base would make your category links like <code>%s/topics/uncategorized/</code>. If you leave these blank the defaults will be used."), get_option("home") + blog_prefix + prefix)
php_print("""</p>
<table class=\"form-table\" role=\"presentation\">
<tr>
<th><label for=\"category_base\">""")
#// translators: Prefix for category permalinks.
_e("Category base")
php_print("</label></th>\n      <td>")
php_print(blog_prefix)
php_print(" <input name=\"category_base\" id=\"category_base\" type=\"text\" value=\"")
php_print(esc_attr(category_base))
php_print("""\" class=\"regular-text code\" /></td>
</tr>
<tr>
<th><label for=\"tag_base\">""")
_e("Tag base")
php_print("</label></th>\n      <td>")
php_print(blog_prefix)
php_print(" <input name=\"tag_base\" id=\"tag_base\" type=\"text\" value=\"")
php_print(esc_attr(tag_base))
php_print("\" class=\"regular-text code\" /></td>\n </tr>\n ")
do_settings_fields("permalink", "optional")
php_print("</table>\n\n")
do_settings_sections("permalink")
php_print("\n")
submit_button()
php_print("</form>\n")
if (not is_multisite()):
    php_print(" ")
    if iis7_permalinks:
        if (php_isset(lambda : PHP_POST["submit"])) and permalink_structure and (not using_index_permalinks) and (not writable):
            if php_file_exists(home_path + "web.config"):
                php_print("<p>\n                ")
                printf(__("If your %1$s file was <a href=\"%2$s\">writable</a>, we could do this automatically, but it isn&#8217;t so this is the url rewrite rule you should have in your %1$s file. Click in the field and press %3$s to select all. Then insert this rule inside of the %4$s element in %1$s file."), "<code>web.config</code>", __("https://wordpress.org/support/article/changing-file-permissions/"), "<kbd>CTRL + a</kbd>", "<code>/&lt;configuration&gt;/&lt;system.webServer&gt;/&lt;rewrite&gt;/&lt;rules&gt;</code>")
                php_print("</p>\n<form action=\"options-permalink.php\" method=\"post\">\n              ")
                wp_nonce_field("update-permalink")
                php_print(" <p><textarea rows=\"9\" class=\"large-text readonly\" name=\"rules\" id=\"rules\" readonly=\"readonly\">")
                php_print(esc_textarea(wp_rewrite.iis7_url_rewrite_rules()))
                php_print("""</textarea></p>
                </form>
                <p>
                """)
                printf(__("If you temporarily make your %s file writable for us to generate rewrite rules automatically, do not forget to revert the permissions after rule has been saved."), "<code>web.config</code>")
                php_print("</p>\n       ")
            else:
                php_print("<p>\n            ")
                printf(__("If the root directory of your site was <a href=\"%1$s\">writable</a>, we could do this automatically, but it isn&#8217;t so this is the url rewrite rule you should have in your %2$s file. Create a new file, called %2$s in the root directory of your site. Click in the field and press %3$s to select all. Then insert this code into the %2$s file."), __("https://wordpress.org/support/article/changing-file-permissions/"), "<code>web.config</code>", "<kbd>CTRL + a</kbd>")
                php_print("</p>\n<form action=\"options-permalink.php\" method=\"post\">\n          ")
                wp_nonce_field("update-permalink")
                php_print(" <p><textarea rows=\"18\" class=\"large-text readonly\" name=\"rules\" id=\"rules\" readonly=\"readonly\">")
                php_print(esc_textarea(wp_rewrite.iis7_url_rewrite_rules(True)))
                php_print("""</textarea></p>
                </form>
                <p>
                """)
                printf(__("If you temporarily make your site&#8217;s root directory writable for us to generate the %s file automatically, do not forget to revert the permissions after the file has been created."), "<code>web.config</code>")
                php_print("</p>\n       ")
            # end if
            php_print(" ")
        # end if
    elif is_nginx:
        php_print(" <p>")
        _e("<a href=\"https://wordpress.org/support/article/nginx/\">Documentation on Nginx configuration</a>.")
        php_print("</p>\n   ")
    else:
        if permalink_structure and (not using_index_permalinks) and (not writable) and update_required:
            php_print("<p>\n        ")
            printf(__("If your %1$s file was <a href=\"%2$s\">writable</a>, we could do this automatically, but it isn&#8217;t so these are the mod_rewrite rules you should have in your %1$s file. Click in the field and press %3$s to select all."), "<code>.htaccess</code>", __("https://wordpress.org/support/article/changing-file-permissions/"), "<kbd>CTRL + a</kbd>")
            php_print("</p>\n<form action=\"options-permalink.php\" method=\"post\">\n      ")
            wp_nonce_field("update-permalink")
            php_print(" <p><textarea rows=\"6\" class=\"large-text readonly\" name=\"rules\" id=\"rules\" readonly=\"readonly\">")
            php_print(esc_textarea(wp_rewrite.mod_rewrite_rules()))
            php_print("</textarea></p>\n</form>\n   ")
        # end if
    # end if
# end if
pass
php_print("""
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
