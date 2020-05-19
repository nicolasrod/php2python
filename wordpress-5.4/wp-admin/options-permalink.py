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
title_ = __("Permalink Settings")
parent_file_ = "options-general.php"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Permalinks are the permanent URLs to your individual pages and blog posts, as well as your category and tag archives. A permalink is the web address used to link to your content. The URL to each post should be permanent, and never change &#8212; hence the name permalink.") + "</p>" + "<p>" + __("This screen allows you to choose your permalink structure. You can choose from common settings or create custom URL structures.") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "permalink-settings", "title": __("Permalink Settings"), "content": "<p>" + __("Permalinks can contain useful information, such as the post date, title, or other elements. You can choose from any of the suggested permalink formats, or you can craft your own if you select Custom Structure.") + "</p>" + "<p>" + php_sprintf(__("If you pick an option other than Plain, your general URL path with structure tags (terms surrounded by %s) will also appear in the custom structure field and your path can be further modified there."), "<code>%</code>") + "</p>" + "<p>" + php_sprintf(__("When you assign multiple categories or tags to a post, only one can show up in the permalink: the lowest numbered category. This applies if your custom structure includes %1$s or %2$s."), "<code>%category%</code>", "<code>%tag%</code>") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "custom-structures", "title": __("Custom Structures"), "content": "<p>" + __("The Optional fields let you customize the &#8220;category&#8221; and &#8220;tag&#8221; base names that will appear in archive URLs. For example, the page listing all posts in the &#8220;Uncategorized&#8221; category could be <code>/topics/uncategorized</code> instead of <code>/category/uncategorized</code>.") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/settings-permalinks-screen/\">Documentation on Permalinks Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/using-permalinks/\">Documentation on Using Permalinks</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
home_path_ = get_home_path()
iis7_permalinks_ = iis7_supports_permalinks()
permalink_structure_ = get_option("permalink_structure")
prefix_ = ""
blog_prefix_ = ""
if (not got_url_rewrite()):
    prefix_ = "/index.php"
# end if
#// 
#// In a subdirectory configuration of multisite, the `/blog` prefix is used by
#// default on the main site to avoid collisions with other sites created on that
#// network. If the `permalink_structure` option has been changed to remove this
#// base prefix, WordPress core can no longer account for the possible collision.
#//
if is_multisite() and (not is_subdomain_install()) and is_main_site() and 0 == php_strpos(permalink_structure_, "/blog/"):
    blog_prefix_ = "/blog"
# end if
category_base_ = get_option("category_base")
tag_base_ = get_option("tag_base")
update_required_ = False
if iis7_permalinks_:
    if (not php_file_exists(home_path_ + "web.config")) and win_is_writable(home_path_) or win_is_writable(home_path_ + "web.config"):
        writable_ = True
    else:
        writable_ = False
    # end if
elif is_nginx_:
    writable_ = False
else:
    if (not php_file_exists(home_path_ + ".htaccess")) and php_is_writable(home_path_) or php_is_writable(home_path_ + ".htaccess"):
        writable_ = True
    else:
        writable_ = False
        existing_rules_ = php_array_filter(extract_from_markers(home_path_ + ".htaccess", "WordPress"))
        new_rules_ = php_array_filter(php_explode("\n", wp_rewrite_.mod_rewrite_rules()))
        update_required_ = new_rules_ != existing_rules_
    # end if
# end if
using_index_permalinks_ = wp_rewrite_.using_index_permalinks()
if (php_isset(lambda : PHP_POST["permalink_structure"])) or (php_isset(lambda : PHP_POST["category_base"])):
    check_admin_referer("update-permalink")
    if (php_isset(lambda : PHP_POST["permalink_structure"])):
        if (php_isset(lambda : PHP_POST["selection"])) and "custom" != PHP_POST["selection"]:
            permalink_structure_ = PHP_POST["selection"]
        else:
            permalink_structure_ = PHP_POST["permalink_structure"]
        # end if
        if (not php_empty(lambda : permalink_structure_)):
            permalink_structure_ = php_preg_replace("#/+#", "/", "/" + php_str_replace("#", "", permalink_structure_))
            if prefix_ and blog_prefix_:
                permalink_structure_ = prefix_ + php_preg_replace("#^/?index\\.php#", "", permalink_structure_)
            else:
                permalink_structure_ = blog_prefix_ + permalink_structure_
            # end if
        # end if
        permalink_structure_ = sanitize_option("permalink_structure", permalink_structure_)
        wp_rewrite_.set_permalink_structure(permalink_structure_)
    # end if
    if (php_isset(lambda : PHP_POST["category_base"])):
        category_base_ = PHP_POST["category_base"]
        if (not php_empty(lambda : category_base_)):
            category_base_ = blog_prefix_ + php_preg_replace("#/+#", "/", "/" + php_str_replace("#", "", category_base_))
        # end if
        wp_rewrite_.set_category_base(category_base_)
    # end if
    if (php_isset(lambda : PHP_POST["tag_base"])):
        tag_base_ = PHP_POST["tag_base"]
        if (not php_empty(lambda : tag_base_)):
            tag_base_ = blog_prefix_ + php_preg_replace("#/+#", "/", "/" + php_str_replace("#", "", tag_base_))
        # end if
        wp_rewrite_.set_tag_base(tag_base_)
    # end if
    message_ = __("Permalink structure updated.")
    if iis7_permalinks_:
        if permalink_structure_ and (not using_index_permalinks_) and (not writable_):
            message_ = php_sprintf(__("You should update your %s file now."), "<code>web.config</code>")
        elif permalink_structure_ and (not using_index_permalinks_) and writable_:
            message_ = php_sprintf(__("Permalink structure updated. Remove write access on %s file now!"), "<code>web.config</code>")
        # end if
    elif (not is_nginx_) and permalink_structure_ and (not using_index_permalinks_) and (not writable_) and update_required_:
        message_ = php_sprintf(__("You should update your %s file now."), "<code>.htaccess</code>")
    # end if
    if (not get_settings_errors()):
        add_settings_error("general", "settings_updated", message_, "success")
    # end if
    set_transient("settings_errors", get_settings_errors(), 30)
    wp_redirect(admin_url("options-permalink.php?settings-updated=true"))
    php_exit(0)
# end if
flush_rewrite_rules()
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n<h1>")
php_print(esc_html(title_))
php_print("""</h1>
<form name=\"form\" action=\"options-permalink.php\" method=\"post\">
""")
wp_nonce_field("update-permalink")
php_print("\n   <p>\n   ")
printf(__("WordPress offers you the ability to create a custom URL structure for your permalinks and archives. Custom URL structures can improve the aesthetics, usability, and forward-compatibility of your links. A <a href=\"%s\">number of tags are available</a>, and here are some examples to get you started."), __("https://wordpress.org/support/article/using-permalinks/"))
php_print(" </p>\n\n")
if is_multisite() and (not is_subdomain_install()) and is_main_site() and 0 == php_strpos(permalink_structure_, "/blog/"):
    permalink_structure_ = php_preg_replace("|^/?blog|", "", permalink_structure_)
    category_base_ = php_preg_replace("|^/?blog|", "", category_base_)
    tag_base_ = php_preg_replace("|^/?blog|", "", tag_base_)
# end if
structures_ = Array({0: "", 1: prefix_ + "/%year%/%monthnum%/%day%/%postname%/", 2: prefix_ + "/%year%/%monthnum%/%postname%/", 3: prefix_ + "/" + _x("archives", "sample permalink base") + "/%post_id%", 4: prefix_ + "/%postname%/"})
php_print("<h2 class=\"title\">")
_e("Common Settings")
php_print("""</h2>
<table class=\"form-table permalink-structure\">
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"\" """)
checked("", permalink_structure_)
php_print(" /> ")
_e("Plain")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home"))
php_print("""/?p=123</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures_[1]))
php_print("\" ")
checked(structures_[1], permalink_structure_)
php_print(" /> ")
_e("Day and name")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix_ + prefix_ + "/" + gmdate("Y") + "/" + gmdate("m") + "/" + gmdate("d") + "/" + _x("sample-post", "sample permalink structure") + "/")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures_[2]))
php_print("\" ")
checked(structures_[2], permalink_structure_)
php_print(" /> ")
_e("Month and name")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix_ + prefix_ + "/" + gmdate("Y") + "/" + gmdate("m") + "/" + _x("sample-post", "sample permalink structure") + "/")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures_[3]))
php_print("\" ")
checked(structures_[3], permalink_structure_)
php_print(" /> ")
_e("Numeric")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix_ + prefix_ + "/" + _x("archives", "sample permalink base") + "/123")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\"><label><input name=\"selection\" type=\"radio\" value=\"""")
php_print(esc_attr(structures_[4]))
php_print("\" ")
checked(structures_[4], permalink_structure_)
php_print(" /> ")
_e("Post name")
php_print("</label></th>\n      <td><code>")
php_print(get_option("home") + blog_prefix_ + prefix_ + "/" + _x("sample-post", "sample permalink structure") + "/")
php_print("""</code></td>
</tr>
<tr>
<th scope=\"row\">
<label><input name=\"selection\" id=\"custom_selection\" type=\"radio\" value=\"custom\" """)
checked((not php_in_array(permalink_structure_, structures_)))
php_print(" />\n            ")
_e("Custom Structure")
php_print("""           </label>
</th>
<td>
<code>""")
php_print(get_option("home") + blog_prefix_)
php_print("</code>\n            <input name=\"permalink_structure\" id=\"permalink_structure\" type=\"text\" value=\"")
php_print(esc_attr(permalink_structure_))
php_print("""\" class=\"regular-text code\" />
<div class=\"available-structure-tags hide-if-no-js\">
<div id=\"custom_selection_updated\" aria-live=\"assertive\" class=\"screen-reader-text\"></div>
""")
available_tags_ = Array({"year": __("%s (The year of the post, four digits, for example 2004.)"), "monthnum": __("%s (Month of the year, for example 05.)"), "day": __("%s (Day of the month, for example 28.)"), "hour": __("%s (Hour of the day, for example 15.)"), "minute": __("%s (Minute of the hour, for example 43.)"), "second": __("%s (Second of the minute, for example 33.)"), "post_id": __("%s (The unique ID of the post, for example 423.)"), "postname": __("%s (The sanitized post title (slug).)"), "category": __("%s (Category slug. Nested sub-categories appear as nested directories in the URL.)"), "author": __("%s (A sanitized version of the author name.)")})
#// 
#// Filters the list of available permalink structure tags on the Permalinks settings page.
#// 
#// @since 4.8.0
#// 
#// @param string[] $available_tags An array of key => value pairs of available permalink structure tags.
#//
available_tags_ = apply_filters("available_permalink_structure_tags", available_tags_)
#// translators: %s: Permalink structure tag.
structure_tag_added_ = __("%s added to permalink structure")
#// translators: %s: Permalink structure tag.
structure_tag_already_used_ = __("%s (already used in permalink structure)")
if (not php_empty(lambda : available_tags_)):
    php_print("                 <p>")
    _e("Available tags:")
    php_print("</p>\n                   <ul role=\"list\">\n                        ")
    for tag_,explanation_ in available_tags_.items():
        php_print("""                           <li>
        <button type=\"button\"
    class=\"button button-secondary\"
        aria-label=\"""")
        php_print(esc_attr(php_sprintf(explanation_, tag_)))
        php_print("\"\n                                     data-added=\"")
        php_print(esc_attr(php_sprintf(structure_tag_added_, tag_)))
        php_print("\"\n                                     data-used=\"")
        php_print(esc_attr(php_sprintf(structure_tag_already_used_, tag_)))
        php_print("\">\n                                    ")
        php_print("%" + tag_ + "%")
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
printf(__("If you like, you may enter custom structures for your category and tag URLs here. For example, using <code>topics</code> as your category base would make your category links like <code>%s/topics/uncategorized/</code>. If you leave these blank the defaults will be used."), get_option("home") + blog_prefix_ + prefix_)
php_print("""</p>
<table class=\"form-table\" role=\"presentation\">
<tr>
<th><label for=\"category_base\">""")
#// translators: Prefix for category permalinks.
_e("Category base")
php_print("</label></th>\n      <td>")
php_print(blog_prefix_)
php_print(" <input name=\"category_base\" id=\"category_base\" type=\"text\" value=\"")
php_print(esc_attr(category_base_))
php_print("""\" class=\"regular-text code\" /></td>
</tr>
<tr>
<th><label for=\"tag_base\">""")
_e("Tag base")
php_print("</label></th>\n      <td>")
php_print(blog_prefix_)
php_print(" <input name=\"tag_base\" id=\"tag_base\" type=\"text\" value=\"")
php_print(esc_attr(tag_base_))
php_print("\" class=\"regular-text code\" /></td>\n </tr>\n ")
do_settings_fields("permalink", "optional")
php_print("</table>\n\n")
do_settings_sections("permalink")
php_print("\n")
submit_button()
php_print("</form>\n")
if (not is_multisite()):
    php_print(" ")
    if iis7_permalinks_:
        if (php_isset(lambda : PHP_POST["submit"])) and permalink_structure_ and (not using_index_permalinks_) and (not writable_):
            if php_file_exists(home_path_ + "web.config"):
                php_print("<p>\n                ")
                printf(__("If your %1$s file was <a href=\"%2$s\">writable</a>, we could do this automatically, but it isn&#8217;t so this is the url rewrite rule you should have in your %1$s file. Click in the field and press %3$s to select all. Then insert this rule inside of the %4$s element in %1$s file."), "<code>web.config</code>", __("https://wordpress.org/support/article/changing-file-permissions/"), "<kbd>CTRL + a</kbd>", "<code>/&lt;configuration&gt;/&lt;system.webServer&gt;/&lt;rewrite&gt;/&lt;rules&gt;</code>")
                php_print("</p>\n<form action=\"options-permalink.php\" method=\"post\">\n              ")
                wp_nonce_field("update-permalink")
                php_print(" <p><textarea rows=\"9\" class=\"large-text readonly\" name=\"rules\" id=\"rules\" readonly=\"readonly\">")
                php_print(esc_textarea(wp_rewrite_.iis7_url_rewrite_rules()))
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
                php_print(esc_textarea(wp_rewrite_.iis7_url_rewrite_rules(True)))
                php_print("""</textarea></p>
                </form>
                <p>
                """)
                printf(__("If you temporarily make your site&#8217;s root directory writable for us to generate the %s file automatically, do not forget to revert the permissions after the file has been created."), "<code>web.config</code>")
                php_print("</p>\n       ")
            # end if
            php_print(" ")
        # end if
    elif is_nginx_:
        php_print(" <p>")
        _e("<a href=\"https://wordpress.org/support/article/nginx/\">Documentation on Nginx configuration</a>.")
        php_print("</p>\n   ")
    else:
        if permalink_structure_ and (not using_index_permalinks_) and (not writable_) and update_required_:
            php_print("<p>\n        ")
            printf(__("If your %1$s file was <a href=\"%2$s\">writable</a>, we could do this automatically, but it isn&#8217;t so these are the mod_rewrite rules you should have in your %1$s file. Click in the field and press %3$s to select all."), "<code>.htaccess</code>", __("https://wordpress.org/support/article/changing-file-permissions/"), "<kbd>CTRL + a</kbd>")
            php_print("</p>\n<form action=\"options-permalink.php\" method=\"post\">\n      ")
            wp_nonce_field("update-permalink")
            php_print(" <p><textarea rows=\"6\" class=\"large-text readonly\" name=\"rules\" id=\"rules\" readonly=\"readonly\">")
            php_print(esc_textarea(wp_rewrite_.mod_rewrite_rules()))
            php_print("</textarea></p>\n</form>\n   ")
        # end if
    # end if
# end if
pass
php_print("""
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
