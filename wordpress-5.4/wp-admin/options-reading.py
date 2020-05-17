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
#// Reading settings administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_options")):
    wp_die(__("Sorry, you are not allowed to manage options for this site."))
# end if
title_ = __("Reading Settings")
parent_file_ = "options-general.php"
add_action("admin_head", "options_reading_add_js")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen contains the settings that affect the display of your content.") + "</p>" + "<p>" + php_sprintf(__("You can choose what&#8217;s displayed on the homepage of your site. It can be posts in reverse chronological order (classic blog), or a fixed/static page. To set a static homepage, you first need to create two <a href=\"%s\">Pages</a>. One will become the homepage, and the other will be where your posts are displayed."), "post-new.php?post_type=page") + "</p>" + "<p>" + php_sprintf(__("You can also control the display of your content in RSS feeds, including the maximum number of posts to display and whether to show full text or a summary. <a href=\"%s\">Learn more about feeds</a>."), __("https://wordpress.org/support/article/wordpress-feeds/")) + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "site-visibility", "title": __("Site Visibility") if has_action("blog_privacy_selector") else __("Search Engine Visibility"), "content": "<p>" + __("You can choose whether or not your site will be crawled by robots, ping services, and spiders. If you want those services to ignore your site, click the checkbox next to &#8220;Discourage search engines from indexing this site&#8221; and click the Save Changes button at the bottom of the screen. Note that your privacy is not complete; your site is still visible on the web.") + "</p>" + "<p>" + __("When this setting is in effect, a reminder is shown in the At a Glance box of the Dashboard that says, &#8220;Search Engines Discouraged,&#8221; to remind you that your site is not being crawled.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/settings-reading-screen/\">Documentation on Reading Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(esc_html(title_))
php_print("""</h1>
<form method=\"post\" action=\"options.php\">
""")
settings_fields("reading")
if (not php_in_array(get_option("blog_charset"), Array("utf8", "utf-8", "UTF8", "UTF-8"))):
    add_settings_field("blog_charset", __("Encoding for pages and feeds"), "options_reading_blog_charset", "reading", "default", Array({"label_for": "blog_charset"}))
# end if
php_print("\n")
if (not get_pages()):
    php_print("<input name=\"show_on_front\" type=\"hidden\" value=\"posts\" />\n<table class=\"form-table\" role=\"presentation\">\n   ")
    if "posts" != get_option("show_on_front"):
        update_option("show_on_front", "posts")
    # end if
else:
    if "page" == get_option("show_on_front") and (not get_option("page_on_front")) and (not get_option("page_for_posts")):
        update_option("show_on_front", "posts")
    # end if
    php_print("<table class=\"form-table\" role=\"presentation\">\n<tr>\n<th scope=\"row\">")
    _e("Your homepage displays")
    php_print("</th>\n<td id=\"front-static-pages\"><fieldset><legend class=\"screen-reader-text\"><span>")
    _e("Your homepage displays")
    php_print("</span></legend>\n   <p><label>\n        <input name=\"show_on_front\" type=\"radio\" value=\"posts\" class=\"tog\" ")
    checked("posts", get_option("show_on_front"))
    php_print(" />\n        ")
    _e("Your latest posts")
    php_print("""   </label>
    </p>
    <p><label>
    <input name=\"show_on_front\" type=\"radio\" value=\"page\" class=\"tog\" """)
    checked("page", get_option("show_on_front"))
    php_print(" />\n        ")
    printf(__("A <a href=\"%s\">static page</a> (select below)"), "edit.php?post_type=page")
    php_print("""   </label>
    </p>
    <ul>
    <li><label for=\"page_on_front\">
    """)
    printf(__("Homepage: %s"), wp_dropdown_pages(Array({"name": "page_on_front", "echo": 0, "show_option_none": __("&mdash; Select &mdash;"), "option_none_value": "0", "selected": get_option("page_on_front")})))
    php_print("</label></li>\n  <li><label for=\"page_for_posts\">\n    ")
    printf(__("Posts page: %s"), wp_dropdown_pages(Array({"name": "page_for_posts", "echo": 0, "show_option_none": __("&mdash; Select &mdash;"), "option_none_value": "0", "selected": get_option("page_for_posts")})))
    php_print("</label></li>\n</ul>\n   ")
    if "page" == get_option("show_on_front") and get_option("page_for_posts") == get_option("page_on_front"):
        php_print(" <div id=\"front-page-warning\" class=\"error inline\"><p>")
        _e("<strong>Warning:</strong> these pages should not be the same!")
        php_print("</p></div>\n ")
    # end if
    php_print(" ")
    if get_option("wp_page_for_privacy_policy") == get_option("page_for_posts") or get_option("wp_page_for_privacy_policy") == get_option("page_on_front"):
        php_print(" <div id=\"privacy-policy-page-warning\" class=\"error inline\"><p>")
        _e("<strong>Warning:</strong> these pages should not be the same as your Privacy Policy page!")
        php_print("</p></div>\n ")
    # end if
    php_print("</fieldset></td>\n</tr>\n")
# end if
php_print("<tr>\n<th scope=\"row\"><label for=\"posts_per_page\">")
_e("Blog pages show at most")
php_print("</label></th>\n<td>\n<input name=\"posts_per_page\" type=\"number\" step=\"1\" min=\"1\" id=\"posts_per_page\" value=\"")
form_option("posts_per_page")
php_print("\" class=\"small-text\" /> ")
_e("posts")
php_print("""</td>
</tr>
<tr>
<th scope=\"row\"><label for=\"posts_per_rss\">""")
_e("Syndication feeds show the most recent")
php_print("</label></th>\n<td><input name=\"posts_per_rss\" type=\"number\" step=\"1\" min=\"1\" id=\"posts_per_rss\" value=\"")
form_option("posts_per_rss")
php_print("\" class=\"small-text\" /> ")
_e("items")
php_print("""</td>
</tr>
<tr>
<th scope=\"row\">""")
_e("For each post in a feed, include")
php_print(" </th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("For each post in a feed, include")
php_print(" </span></legend>\n  <p>\n       <label><input name=\"rss_use_excerpt\" type=\"radio\" value=\"0\" ")
checked(0, get_option("rss_use_excerpt"))
php_print(" /> ")
_e("Full text")
php_print("</label><br />\n     <label><input name=\"rss_use_excerpt\" type=\"radio\" value=\"1\" ")
checked(1, get_option("rss_use_excerpt"))
php_print(" /> ")
_e("Summary")
php_print("""</label>
</p>
<p class=\"description\">
""")
printf(__("Your theme determines how content is displayed in browsers. <a href=\"%s\">Learn more about feeds</a>."), __("https://wordpress.org/support/article/wordpress-feeds/"))
php_print("""   </p>
</fieldset></td>
</tr>
<tr class=\"option-site-visibility\">
<th scope=\"row\">""")
_e("Site Visibility") if has_action("blog_privacy_selector") else _e("Search Engine Visibility")
php_print(" </th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Site Visibility") if has_action("blog_privacy_selector") else _e("Search Engine Visibility")
php_print(" </span></legend>\n")
if has_action("blog_privacy_selector"):
    php_print(" <input id=\"blog-public\" type=\"radio\" name=\"blog_public\" value=\"1\" ")
    checked("1", get_option("blog_public"))
    php_print(" />\n    <label for=\"blog-public\">")
    _e("Allow search engines to index this site")
    php_print("</label><br/>\n  <input id=\"blog-norobots\" type=\"radio\" name=\"blog_public\" value=\"0\" ")
    checked("0", get_option("blog_public"))
    php_print(" />\n    <label for=\"blog-norobots\">")
    _e("Discourage search engines from indexing this site")
    php_print("</label>\n   <p class=\"description\">")
    _e("Note: Neither of these options blocks access to your site &mdash; it is up to search engines to honor your request.")
    php_print("</p>\n   ")
    #// 
    #// Enable the legacy 'Site Visibility' privacy options.
    #// 
    #// By default the privacy options form displays a single checkbox to 'discourage' search
    #// engines from indexing the site. Hooking to this action serves a dual purpose:
    #// 1. Disable the single checkbox in favor of a multiple-choice list of radio buttons.
    #// 2. Open the door to adding additional radio button choices to the list.
    #// 
    #// Hooking to this action also converts the 'Search Engine Visibility' heading to the more
    #// open-ended 'Site Visibility' heading.
    #// 
    #// @since 2.1.0
    #//
    do_action("blog_privacy_selector")
else:
    php_print(" <label for=\"blog_public\"><input name=\"blog_public\" type=\"checkbox\" id=\"blog_public\" value=\"0\" ")
    checked("0", get_option("blog_public"))
    php_print(" />\n    ")
    _e("Discourage search engines from indexing this site")
    php_print("</label>\n   <p class=\"description\">")
    _e("It is up to search engines to honor this request.")
    php_print("</p>\n")
# end if
php_print("""</fieldset></td>
</tr>
""")
do_settings_fields("reading", "default")
php_print("</table>\n\n")
do_settings_sections("reading")
php_print("\n")
submit_button()
php_print("</form>\n</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
