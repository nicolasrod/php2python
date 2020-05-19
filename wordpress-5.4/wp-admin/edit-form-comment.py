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
#// Edit comment form for inclusion in another file.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Don't load directly.
if (not php_defined("ABSPATH")):
    php_print("-1")
    php_exit()
# end if
php_print("<form name=\"post\" action=\"comment.php\" method=\"post\" id=\"post\">\n")
wp_nonce_field("update-comment_" + comment_.comment_ID)
php_print("<div class=\"wrap\">\n<h1>")
_e("Edit Comment")
php_print("""</h1>
<div id=\"poststuff\">
<input type=\"hidden\" name=\"action\" value=\"editedcomment\" />
<input type=\"hidden\" name=\"comment_ID\" value=\"""")
php_print(esc_attr(comment_.comment_ID))
php_print("\" />\n<input type=\"hidden\" name=\"comment_post_ID\" value=\"")
php_print(esc_attr(comment_.comment_post_ID))
php_print("""\" />
<div id=\"post-body\" class=\"metabox-holder columns-2\">
<div id=\"post-body-content\" class=\"edit-form-section edit-comment-section\">
""")
if "approved" == wp_get_comment_status(comment_) and comment_.comment_post_ID > 0:
    comment_link_ = get_comment_link(comment_)
    php_print("<div class=\"inside\">\n <div id=\"comment-link-box\">\n     <strong>")
    _ex("Permalink:", "comment")
    php_print("</strong>\n      <span id=\"sample-permalink\">\n            <a href=\"")
    php_print(esc_url(comment_link_))
    php_print("\">\n                ")
    php_print(esc_html(comment_link_))
    php_print("""           </a>
    </span>
    </div>
    </div>
    """)
# end if
php_print("<div id=\"namediv\" class=\"stuffbox\">\n<div class=\"inside\">\n<h2 class=\"edit-comment-author\">")
_e("Author")
php_print("</h2>\n<fieldset>\n<legend class=\"screen-reader-text\">")
_e("Comment Author")
php_print("""</legend>
<table class=\"form-table editcomment\" role=\"presentation\">
<tbody>
<tr>
<td class=\"first\"><label for=\"name\">""")
_e("Name")
php_print("</label></td>\n  <td><input type=\"text\" name=\"newcomment_author\" size=\"30\" value=\"")
php_print(esc_attr(comment_.comment_author))
php_print("""\" id=\"name\" /></td>
</tr>
<tr>
<td class=\"first\"><label for=\"email\">""")
_e("Email")
php_print("</label></td>\n  <td>\n      <input type=\"text\" name=\"newcomment_author_email\" size=\"30\" value=\"")
php_print(comment_.comment_author_email)
php_print("""\" id=\"email\" />
</td>
</tr>
<tr>
<td class=\"first\"><label for=\"newcomment_author_url\">""")
_e("URL")
php_print("</label></td>\n  <td>\n      <input type=\"text\" id=\"newcomment_author_url\" name=\"newcomment_author_url\" size=\"30\" class=\"code\" value=\"")
php_print(esc_attr(comment_.comment_author_url))
php_print("""\" />
</td>
</tr>
</tbody>
</table>
</fieldset>
</div>
</div>
<div id=\"postdiv\" class=\"postarea\">
""")
php_print("<label for=\"content\" class=\"screen-reader-text\">" + __("Comment") + "</label>")
quicktags_settings_ = Array({"buttons": "strong,em,link,block,del,ins,img,ul,ol,li,code,close"})
wp_editor(comment_.comment_content, "content", Array({"media_buttons": False, "tinymce": False, "quicktags": quicktags_settings_}))
wp_nonce_field("closedpostboxes", "closedpostboxesnonce", False)
php_print("""</div>
</div><!-- /post-body-content -->
<div id=\"postbox-container-1\" class=\"postbox-container\">
<div id=\"submitdiv\" class=\"stuffbox\" >
<h2>""")
_e("Save")
php_print("""</h2>
<div class=\"inside\">
<div class=\"submitbox\" id=\"submitcomment\">
<div id=\"minor-publishing\">
<div id=\"misc-publishing-actions\">
<div class=\"misc-pub-section misc-pub-comment-status\" id=\"comment-status\">
""")
_e("Status:")
php_print(" <span id=\"comment-status-display\">\n")
for case in Switch(comment_.comment_approved):
    if case("1"):
        _e("Approved")
        break
    # end if
    if case("0"):
        _e("Pending")
        break
    # end if
    if case("spam"):
        _e("Spam")
        break
    # end if
# end for
php_print("""</span>
<fieldset id=\"comment-status-radio\">
<legend class=\"screen-reader-text\">""")
_e("Comment status")
php_print("</legend>\n<label><input type=\"radio\"")
checked(comment_.comment_approved, "1")
php_print(" name=\"comment_status\" value=\"1\" />")
_ex("Approved", "comment status")
php_print("</label><br />\n<label><input type=\"radio\"")
checked(comment_.comment_approved, "0")
php_print(" name=\"comment_status\" value=\"0\" />")
_ex("Pending", "comment status")
php_print("</label><br />\n<label><input type=\"radio\"")
checked(comment_.comment_approved, "spam")
php_print(" name=\"comment_status\" value=\"spam\" />")
_ex("Spam", "comment status")
php_print("""</label>
</fieldset>
</div><!-- .misc-pub-section -->

<div class=\"misc-pub-section curtime misc-pub-curtime\">
""")
submitted_ = php_sprintf(__("%1$s at %2$s"), date_i18n(_x("M j, Y", "publish box date format"), strtotime(comment_.comment_date)), date_i18n(_x("H:i", "publish box time format"), strtotime(comment_.comment_date)))
php_print("<span id=\"timestamp\">\n")
#// translators: %s: Comment date.
php_printf(__("Submitted on: %s"), "<b>" + submitted_ + "</b>")
php_print("</span>\n<a href=\"#edit_timestamp\" class=\"edit-timestamp hide-if-no-js\"><span aria-hidden=\"true\">")
_e("Edit")
php_print("</span> <span class=\"screen-reader-text\">")
_e("Edit date and time")
php_print("</span></a>\n<fieldset id='timestampdiv' class='hide-if-js'>\n<legend class=\"screen-reader-text\">")
_e("Date and time")
php_print("</legend>\n")
touch_time("editcomment" == action_, 0)
php_print("""</fieldset>
</div>
""")
post_id_ = comment_.comment_post_ID
if current_user_can("edit_post", post_id_):
    post_link_ = "<a href='" + esc_url(get_edit_post_link(post_id_)) + "'>"
    post_link_ += esc_html(get_the_title(post_id_)) + "</a>"
else:
    post_link_ = esc_html(get_the_title(post_id_))
# end if
php_print("\n<div class=\"misc-pub-section misc-pub-response-to\">\n    ")
php_printf(__("In response to: %s"), "<b>" + post_link_ + "</b>")
php_print("</div>\n\n")
if comment_.comment_parent:
    parent_ = get_comment(comment_.comment_parent)
    if parent_:
        parent_link_ = esc_url(get_comment_link(parent_))
        name_ = get_comment_author(parent_)
        php_print(" <div class=\"misc-pub-section misc-pub-reply-to\">\n        ")
        php_printf(__("In reply to: %s"), "<b><a href=\"" + parent_link_ + "\">" + name_ + "</a></b>")
        php_print(" </div>\n        ")
    # end if
# end if
php_print("\n")
#// 
#// Filters miscellaneous actions for the edit comment form sidebar.
#// 
#// @since 4.3.0
#// 
#// @param string     $html    Output HTML to display miscellaneous action.
#// @param WP_Comment $comment Current comment object.
#//
php_print(apply_filters("edit_comment_misc_actions", "", comment_))
php_print("""
</div> <!-- misc actions -->
<div class=\"clear\"></div>
</div>
<div id=\"major-publishing-actions\">
<div id=\"delete-action\">
""")
php_print("<a class='submitdelete deletion' href='" + wp_nonce_url("comment.php?action=" + "deletecomment" if (not EMPTY_TRASH_DAYS) else "trashcomment" + str("&amp;c=") + str(comment_.comment_ID) + str("&amp;_wp_original_http_referer=") + urlencode(wp_get_referer()), "delete-comment_" + comment_.comment_ID) + "'>" + __("Delete Permanently") if (not EMPTY_TRASH_DAYS) else __("Move to Trash") + "</a>\n")
php_print("</div>\n<div id=\"publishing-action\">\n")
submit_button(__("Update"), "primary large", "save", False)
php_print("""</div>
<div class=\"clear\"></div>
</div>
</div>
</div>
</div><!-- /submitdiv -->
</div>
<div id=\"postbox-container-2\" class=\"postbox-container\">
""")
#// This action is documented in wp-admin/includes/meta-boxes.php
do_action("add_meta_boxes", "comment", comment_)
#// 
#// Fires when comment-specific meta boxes are added.
#// 
#// @since 3.0.0
#// 
#// @param WP_Comment $comment Comment object.
#//
do_action("add_meta_boxes_comment", comment_)
do_meta_boxes(None, "normal", comment_)
referer_ = wp_get_referer()
php_print("</div>\n\n<input type=\"hidden\" name=\"c\" value=\"")
php_print(esc_attr(comment_.comment_ID))
php_print("\" />\n<input type=\"hidden\" name=\"p\" value=\"")
php_print(esc_attr(comment_.comment_post_ID))
php_print("\" />\n<input name=\"referredby\" type=\"hidden\" id=\"referredby\" value=\"")
php_print(esc_url(referer_) if referer_ else "")
php_print("\" />\n")
wp_original_referer_field(True, "previous")
php_print("""<input type=\"hidden\" name=\"noredir\" value=\"1\" />
</div><!-- /post-body -->
</div>
</div>
</form>
""")
if (not wp_is_mobile()):
    php_print("""<script type=\"text/javascript\">
try{document.post.name.focus();}catch(e){}
    </script>
    """)
# end if
