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
#// Discussion settings administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_options")):
    wp_die(__("Sorry, you are not allowed to manage options for this site."))
# end if
title = __("Discussion Settings")
parent_file = "options-general.php"
add_action("admin_print_footer_scripts", "options_discussion_add_js")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("This screen provides many options for controlling the management and display of comments and links to your posts/pages. So many, in fact, they won&#8217;t all fit here! :) Use the documentation links to get information on what each discussion setting does.") + "</p>" + "<p>" + __("You must click the Save Changes button at the bottom of the screen for new settings to take effect.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/settings-discussion-screen/\">Documentation on Discussion Settings</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(esc_html(title))
php_print("""</h1>
<form method=\"post\" action=\"options.php\">
""")
settings_fields("discussion")
php_print("""
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\">""")
_e("Default post settings")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Default post settings")
php_print("</span></legend>\n<label for=\"default_pingback_flag\">\n<input name=\"default_pingback_flag\" type=\"checkbox\" id=\"default_pingback_flag\" value=\"1\" ")
checked("1", get_option("default_pingback_flag"))
php_print(" />\n")
_e("Attempt to notify any blogs linked to from the post")
php_print("""</label>
<br />
<label for=\"default_ping_status\">
<input name=\"default_ping_status\" type=\"checkbox\" id=\"default_ping_status\" value=\"open\" """)
checked("open", get_option("default_ping_status"))
php_print(" />\n")
_e("Allow link notifications from other blogs (pingbacks and trackbacks) on new posts")
php_print("""</label>
<br />
<label for=\"default_comment_status\">
<input name=\"default_comment_status\" type=\"checkbox\" id=\"default_comment_status\" value=\"open\" """)
checked("open", get_option("default_comment_status"))
php_print(" />\n")
_e("Allow people to submit comments on new posts")
php_print("</label>\n<br />\n<p class=\"description\">")
php_print("(" + __("These settings may be overridden for individual posts.") + ")")
php_print("""</p>
</fieldset></td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Other comment settings")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Other comment settings")
php_print("</span></legend>\n<label for=\"require_name_email\"><input type=\"checkbox\" name=\"require_name_email\" id=\"require_name_email\" value=\"1\" ")
checked("1", get_option("require_name_email"))
php_print(" /> ")
_e("Comment author must fill out name and email")
php_print("""</label>
<br />
<label for=\"comment_registration\">
<input name=\"comment_registration\" type=\"checkbox\" id=\"comment_registration\" value=\"1\" """)
checked("1", get_option("comment_registration"))
php_print(" />\n")
_e("Users must be registered and logged in to comment")
if (not get_option("users_can_register")) and is_multisite():
    php_print(" " + __("(Signup has been disabled. Only members of this site can comment.)"))
# end if
php_print("""</label>
<br />
<label for=\"close_comments_for_old_posts\">
<input name=\"close_comments_for_old_posts\" type=\"checkbox\" id=\"close_comments_for_old_posts\" value=\"1\" """)
checked("1", get_option("close_comments_for_old_posts"))
php_print(" />\n")
printf(__("Automatically close comments on posts older than %s days"), "</label> <label for=\"close_comments_days_old\"><input name=\"close_comments_days_old\" type=\"number\" min=\"0\" step=\"1\" id=\"close_comments_days_old\" value=\"" + esc_attr(get_option("close_comments_days_old")) + "\" class=\"small-text\" />")
php_print("""</label>
<br />
<label for=\"show_comments_cookies_opt_in\">
<input name=\"show_comments_cookies_opt_in\" type=\"checkbox\" id=\"show_comments_cookies_opt_in\" value=\"1\" """)
checked("1", get_option("show_comments_cookies_opt_in"))
php_print(" />\n")
_e("Show comments cookies opt-in checkbox, allowing comment author cookies to be set")
php_print("""</label>
<br />
<label for=\"thread_comments\">
<input name=\"thread_comments\" type=\"checkbox\" id=\"thread_comments\" value=\"1\" """)
checked("1", get_option("thread_comments"))
php_print(" />\n")
#// 
#// Filters the maximum depth of threaded/nested comments.
#// 
#// @since 2.7.0
#// 
#// @param int $max_depth The maximum depth of threaded comments. Default 10.
#//
maxdeep = int(apply_filters("thread_comments_depth_max", 10))
thread_comments_depth = "</label> <label for=\"thread_comments_depth\"><select name=\"thread_comments_depth\" id=\"thread_comments_depth\">"
i = 2
while i <= maxdeep:
    
    thread_comments_depth += "<option value='" + esc_attr(i) + "'"
    if get_option("thread_comments_depth") == i:
        thread_comments_depth += " selected='selected'"
    # end if
    thread_comments_depth += str(">") + str(i) + str("</option>")
    i += 1
# end while
thread_comments_depth += "</select>"
#// translators: %s: Number of levels.
printf(__("Enable threaded (nested) comments %s levels deep"), thread_comments_depth)
php_print("""</label>
<br />
<label for=\"page_comments\">
<input name=\"page_comments\" type=\"checkbox\" id=\"page_comments\" value=\"1\" """)
checked("1", get_option("page_comments"))
php_print(" />\n")
default_comments_page = "</label> <label for=\"default_comments_page\"><select name=\"default_comments_page\" id=\"default_comments_page\"><option value=\"newest\""
if "newest" == get_option("default_comments_page"):
    default_comments_page += " selected=\"selected\""
# end if
default_comments_page += ">" + __("last") + "</option><option value=\"oldest\""
if "oldest" == get_option("default_comments_page"):
    default_comments_page += " selected=\"selected\""
# end if
default_comments_page += ">" + __("first") + "</option></select>"
printf(__("Break comments into pages with %1$s top level comments per page and the %2$s page displayed by default"), "</label> <label for=\"comments_per_page\"><input name=\"comments_per_page\" type=\"number\" step=\"1\" min=\"0\" id=\"comments_per_page\" value=\"" + esc_attr(get_option("comments_per_page")) + "\" class=\"small-text\" />", default_comments_page)
php_print("""</label>
<br />
<label for=\"comment_order\">
""")
comment_order = "<select name=\"comment_order\" id=\"comment_order\"><option value=\"asc\""
if "asc" == get_option("comment_order"):
    comment_order += " selected=\"selected\""
# end if
comment_order += ">" + __("older") + "</option><option value=\"desc\""
if "desc" == get_option("comment_order"):
    comment_order += " selected=\"selected\""
# end if
comment_order += ">" + __("newer") + "</option></select>"
#// translators: %s: Form field control for 'older' or 'newer' comments.
printf(__("Comments should be displayed with the %s comments at the top of each page"), comment_order)
php_print("""</label>
</fieldset></td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Email me whenever")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Email me whenever")
php_print("</span></legend>\n<label for=\"comments_notify\">\n<input name=\"comments_notify\" type=\"checkbox\" id=\"comments_notify\" value=\"1\" ")
checked("1", get_option("comments_notify"))
php_print(" />\n")
_e("Anyone posts a comment")
php_print(""" </label>
<br />
<label for=\"moderation_notify\">
<input name=\"moderation_notify\" type=\"checkbox\" id=\"moderation_notify\" value=\"1\" """)
checked("1", get_option("moderation_notify"))
php_print(" />\n")
_e("A comment is held for moderation")
php_print(""" </label>
</fieldset></td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Before a comment appears")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Before a comment appears")
php_print("</span></legend>\n<label for=\"comment_moderation\">\n<input name=\"comment_moderation\" type=\"checkbox\" id=\"comment_moderation\" value=\"1\" ")
checked("1", get_option("comment_moderation"))
php_print(" />\n")
_e("Comment must be manually approved")
php_print(" </label>\n<br />\n<label for=\"comment_whitelist\"><input type=\"checkbox\" name=\"comment_whitelist\" id=\"comment_whitelist\" value=\"1\" ")
checked("1", get_option("comment_whitelist"))
php_print(" /> ")
_e("Comment author must have a previously approved comment")
php_print("""</label>
</fieldset></td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Comment Moderation")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Comment Moderation")
php_print("</span></legend>\n<p><label for=\"comment_max_links\">\n")
printf(__("Hold a comment in the queue if it contains %s or more links. (A common characteristic of comment spam is a large number of hyperlinks.)"), "<input name=\"comment_max_links\" type=\"number\" step=\"1\" min=\"0\" id=\"comment_max_links\" value=\"" + esc_attr(get_option("comment_max_links")) + "\" class=\"small-text\" />")
php_print("</label></p>\n\n<p><label for=\"moderation_keys\">")
_e("When a comment contains any of these words in its content, name, URL, email, or IP address, it will be held in the <a href=\"edit-comments.php?comment_status=moderated\">moderation queue</a>. One word or IP address per line. It will match inside words, so &#8220;press&#8221; will match &#8220;WordPress&#8221;.")
php_print("</label></p>\n<p>\n<textarea name=\"moderation_keys\" rows=\"10\" cols=\"50\" id=\"moderation_keys\" class=\"large-text code\">")
php_print(esc_textarea(get_option("moderation_keys")))
php_print("""</textarea>
</p>
</fieldset></td>
</tr>
<tr>
<th scope=\"row\">""")
_e("Comment Blocklist")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Comment Blocklist")
php_print("</span></legend>\n<p><label for=\"blacklist_keys\">")
_e("When a comment contains any of these words in its content, name, URL, email, or IP address, it will be put in the Trash. One word or IP address per line. It will match inside words, so &#8220;press&#8221; will match &#8220;WordPress&#8221;.")
php_print("</label></p>\n<p>\n<textarea name=\"blacklist_keys\" rows=\"10\" cols=\"50\" id=\"blacklist_keys\" class=\"large-text code\">")
php_print(esc_textarea(get_option("blacklist_keys")))
php_print("""</textarea>
</p>
</fieldset></td>
</tr>
""")
do_settings_fields("discussion", "default")
php_print("</table>\n\n<h2 class=\"title\">")
_e("Avatars")
php_print("</h2>\n\n<p>")
_e("An avatar is an image that follows you from weblog to weblog appearing beside your name when you comment on avatar enabled sites. Here you can enable the display of avatars for people who comment on your site.")
php_print("</p>\n\n")
#// The above would be a good place to link to the documentation on the Gravatar functions, for putting it in themes. Anything like that?
show_avatars = get_option("show_avatars")
show_avatars_class = ""
if (not show_avatars):
    show_avatars_class = " hide-if-js"
# end if
php_print("""
<table class=\"form-table\" role=\"presentation\">
<tr>
<th scope=\"row\">""")
_e("Avatar Display")
php_print("""</th>
<td>
<label for=\"show_avatars\">
<input type=\"checkbox\" id=\"show_avatars\" name=\"show_avatars\" value=\"1\" """)
checked(show_avatars, 1)
php_print(" />\n        ")
_e("Show Avatars")
php_print("""   </label>
</td>
</tr>
<tr class=\"avatar-settings""")
php_print(show_avatars_class)
php_print("\">\n<th scope=\"row\">")
_e("Maximum Rating")
php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Maximum Rating")
php_print("</span></legend>\n\n")
ratings = Array({"G": __("G &#8212; Suitable for all audiences"), "PG": __("PG &#8212; Possibly offensive, usually for audiences 13 and above"), "R": __("R &#8212; Intended for adult audiences above 17"), "X": __("X &#8212; Even more mature than above")})
for key,rating in ratings:
    selected = "checked=\"checked\"" if get_option("avatar_rating") == key else ""
    php_print("\n   <label><input type='radio' name='avatar_rating' value='" + esc_attr(key) + str("' ") + str(selected) + str("/> ") + str(rating) + str("</label><br />"))
# end for
php_print("""
</fieldset></td>
</tr>
<tr class=\"avatar-settings""")
php_print(show_avatars_class)
php_print("\">\n<th scope=\"row\">")
_e("Default Avatar")
php_print("</th>\n<td class=\"defaultavatarpicker\"><fieldset><legend class=\"screen-reader-text\"><span>")
_e("Default Avatar")
php_print("""</span></legend>
<p>
""")
_e("For users without a custom avatar of their own, you can either display a generic logo or a generated one based on their email address.")
php_print("""<br />
</p>
""")
avatar_defaults = Array({"mystery": __("Mystery Person"), "blank": __("Blank"), "gravatar_default": __("Gravatar Logo"), "identicon": __("Identicon (Generated)"), "wavatar": __("Wavatar (Generated)"), "monsterid": __("MonsterID (Generated)"), "retro": __("Retro (Generated)")})
#// 
#// Filters the default avatars.
#// 
#// Avatars are stored in key/value pairs, where the key is option value,
#// and the name is the displayed avatar name.
#// 
#// @since 2.6.0
#// 
#// @param string[] $avatar_defaults Associative array of default avatars.
#//
avatar_defaults = apply_filters("avatar_defaults", avatar_defaults)
default = get_option("avatar_default", "mystery")
avatar_list = ""
#// Force avatars on to display these choices.
add_filter("pre_option_show_avatars", "__return_true", 100)
for default_key,default_name in avatar_defaults:
    selected = "checked=\"checked\" " if default == default_key else ""
    avatar_list += str("\n  <label><input type='radio' name='avatar_default' id='avatar_") + str(default_key) + str("' value='") + esc_attr(default_key) + str("' ") + str(selected) + str("/> ")
    avatar_list += get_avatar(user_email, 32, default_key, "", Array({"force_default": True}))
    avatar_list += " " + default_name + "</label>"
    avatar_list += "<br />"
# end for
remove_filter("pre_option_show_avatars", "__return_true", 100)
#// 
#// Filters the HTML output of the default avatar list.
#// 
#// @since 2.6.0
#// 
#// @param string $avatar_list HTML markup of the avatar list.
#//
php_print(apply_filters("default_avatar_select", avatar_list))
php_print("""
</fieldset></td>
</tr>
""")
do_settings_fields("discussion", "avatars")
php_print("</table>\n\n")
do_settings_sections("discussion")
php_print("\n")
submit_button()
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)