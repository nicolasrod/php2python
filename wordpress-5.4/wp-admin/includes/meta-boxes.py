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
#// WordPress Administration Meta Boxes API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Post-related Meta Boxes.
#// 
#// 
#// Displays post submit form fields.
#// 
#// @since 2.7.0
#// 
#// @global string $action
#// 
#// @param WP_Post  $post Current post object.
#// @param array    $args {
#// Array of arguments for building the post submit meta box.
#// 
#// @type string   $id       Meta box 'id' attribute.
#// @type string   $title    Meta box title.
#// @type callable $callback Meta box display callback.
#// @type array    $args     Extra meta box arguments.
#// }
#//
def post_submit_meta_box(post=None, args=Array(), *args_):
    
    global action
    php_check_if_defined("action")
    post_type = post.post_type
    post_type_object = get_post_type_object(post_type)
    can_publish = current_user_can(post_type_object.cap.publish_posts)
    php_print("""<div class=\"submitbox\" id=\"submitpost\">
    <div id=\"minor-publishing\">
    """)
    pass
    php_print("<div style=\"display:none;\">\n  ")
    submit_button(__("Save"), "", "save")
    php_print("""</div>
    <div id=\"minor-publishing-actions\">
    <div id=\"save-action\">
    """)
    if "publish" != post.post_status and "future" != post.post_status and "pending" != post.post_status:
        private_style = ""
        if "private" == post.post_status:
            private_style = "style=\"display:none\""
        # end if
        php_print("<input ")
        php_print(private_style)
        php_print(" type=\"submit\" name=\"save\" id=\"save-post\" value=\"")
        esc_attr_e("Save Draft")
        php_print("\" class=\"button\" />\n<span class=\"spinner\"></span>\n")
    elif "pending" == post.post_status and can_publish:
        php_print("<input type=\"submit\" name=\"save\" id=\"save-post\" value=\"")
        esc_attr_e("Save as Pending")
        php_print("\" class=\"button\" />\n<span class=\"spinner\"></span>\n")
    # end if
    php_print("</div>\n ")
    if is_post_type_viewable(post_type_object):
        php_print("<div id=\"preview-action\">\n        ")
        preview_link = esc_url(get_preview_post_link(post))
        if "publish" == post.post_status:
            preview_button_text = __("Preview Changes")
        else:
            preview_button_text = __("Preview")
        # end if
        preview_button = php_sprintf("%1$s<span class=\"screen-reader-text\"> %2$s</span>", preview_button_text, __("(opens in a new tab)"))
        php_print("<a class=\"preview button\" href=\"")
        php_print(preview_link)
        php_print("\" target=\"wp-preview-")
        php_print(int(post.ID))
        php_print("\" id=\"post-preview\">")
        php_print(preview_button)
        php_print("""</a>
        <input type=\"hidden\" name=\"wp-preview\" id=\"wp-preview\" value=\"\" />
        </div>
        """)
    # end if
    pass
    php_print(" ")
    #// 
    #// Fires before the post time/date setting in the Publish meta box.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Post $post WP_Post object for the current post.
    #//
    do_action("post_submitbox_minor_actions", post)
    php_print("""<div class=\"clear\"></div>
    </div><!-- #minor-publishing-actions -->
    <div id=\"misc-publishing-actions\">
    <div class=\"misc-pub-section misc-pub-post-status\">
    """)
    _e("Status:")
    php_print(" <span id=\"post-status-display\">\n         ")
    for case in Switch(post.post_status):
        if case("private"):
            _e("Privately Published")
            break
        # end if
        if case("publish"):
            _e("Published")
            break
        # end if
        if case("future"):
            _e("Scheduled")
            break
        # end if
        if case("pending"):
            _e("Pending Review")
            break
        # end if
        if case("draft"):
            pass
        # end if
        if case("auto-draft"):
            _e("Draft")
            break
        # end if
    # end for
    php_print("</span>\n    ")
    if "publish" == post.post_status or "private" == post.post_status or can_publish:
        private_style = ""
        if "private" == post.post_status:
            private_style = "style=\"display:none\""
        # end if
        php_print("<a href=\"#post_status\" ")
        php_print(private_style)
        php_print(" class=\"edit-post-status hide-if-no-js\" role=\"button\"><span aria-hidden=\"true\">")
        _e("Edit")
        php_print("</span> <span class=\"screen-reader-text\">")
        _e("Edit status")
        php_print("""</span></a>
        <div id=\"post-status-select\" class=\"hide-if-js\">
        <input type=\"hidden\" name=\"hidden_post_status\" id=\"hidden_post_status\" value=\"""")
        php_print(esc_attr("draft" if "auto-draft" == post.post_status else post.post_status))
        php_print("\" />\n<label for=\"post_status\" class=\"screen-reader-text\">")
        _e("Set status")
        php_print("</label>\n<select name=\"post_status\" id=\"post_status\">\n     ")
        if "publish" == post.post_status:
            php_print("<option")
            selected(post.post_status, "publish")
            php_print(" value='publish'>")
            _e("Published")
            php_print("</option>\n")
        elif "private" == post.post_status:
            php_print("<option")
            selected(post.post_status, "private")
            php_print(" value='publish'>")
            _e("Privately Published")
            php_print("</option>\n")
        elif "future" == post.post_status:
            php_print("<option")
            selected(post.post_status, "future")
            php_print(" value='future'>")
            _e("Scheduled")
            php_print("</option>\n")
        # end if
        php_print("<option")
        selected(post.post_status, "pending")
        php_print(" value='pending'>")
        _e("Pending Review")
        php_print("</option>\n      ")
        if "auto-draft" == post.post_status:
            php_print("<option")
            selected(post.post_status, "auto-draft")
            php_print(" value='draft'>")
            _e("Draft")
            php_print("</option>\n")
        else:
            php_print("<option")
            selected(post.post_status, "draft")
            php_print(" value='draft'>")
            _e("Draft")
            php_print("</option>\n")
        # end if
        php_print("</select>\n<a href=\"#post_status\" class=\"save-post-status hide-if-no-js button\">")
        _e("OK")
        php_print("</a>\n<a href=\"#post_status\" class=\"cancel-post-status hide-if-no-js button-cancel\">")
        _e("Cancel")
        php_print("""</a>
        </div>
        """)
    # end if
    php_print("""</div><!-- .misc-pub-section -->
    <div class=\"misc-pub-section misc-pub-visibility\" id=\"visibility\">
    """)
    _e("Visibility:")
    php_print(" <span id=\"post-visibility-display\">\n                         ")
    if "private" == post.post_status:
        post.post_password = ""
        visibility = "private"
        visibility_trans = __("Private")
    elif (not php_empty(lambda : post.post_password)):
        visibility = "password"
        visibility_trans = __("Password protected")
    elif "post" == post_type and is_sticky(post.ID):
        visibility = "public"
        visibility_trans = __("Public, Sticky")
    else:
        visibility = "public"
        visibility_trans = __("Public")
    # end if
    php_print(esc_html(visibility_trans))
    php_print("</span>\n    ")
    if can_publish:
        php_print("<a href=\"#visibility\" class=\"edit-visibility hide-if-no-js\" role=\"button\"><span aria-hidden=\"true\">")
        _e("Edit")
        php_print("</span> <span class=\"screen-reader-text\">")
        _e("Edit visibility")
        php_print("""</span></a>
        <div id=\"post-visibility-select\" class=\"hide-if-js\">
        <input type=\"hidden\" name=\"hidden_post_password\" id=\"hidden-post-password\" value=\"""")
        php_print(esc_attr(post.post_password))
        php_print("\" />\n      ")
        if "post" == post_type:
            php_print("<input type=\"checkbox\" style=\"display:none\" name=\"hidden_post_sticky\" id=\"hidden-post-sticky\" value=\"sticky\" ")
            checked(is_sticky(post.ID))
            php_print(" />\n")
        # end if
        php_print("<input type=\"hidden\" name=\"hidden_post_visibility\" id=\"hidden-post-visibility\" value=\"")
        php_print(esc_attr(visibility))
        php_print("\" />\n<input type=\"radio\" name=\"visibility\" id=\"visibility-radio-public\" value=\"public\" ")
        checked(visibility, "public")
        php_print(" /> <label for=\"visibility-radio-public\" class=\"selectit\">")
        _e("Public")
        php_print("</label><br />\n     ")
        if "post" == post_type and current_user_can("edit_others_posts"):
            php_print("<span id=\"sticky-span\"><input id=\"sticky\" name=\"sticky\" type=\"checkbox\" value=\"sticky\" ")
            checked(is_sticky(post.ID))
            php_print(" /> <label for=\"sticky\" class=\"selectit\">")
            _e("Stick this post to the front page")
            php_print("</label><br /></span>\n")
        # end if
        php_print("<input type=\"radio\" name=\"visibility\" id=\"visibility-radio-password\" value=\"password\" ")
        checked(visibility, "password")
        php_print(" /> <label for=\"visibility-radio-password\" class=\"selectit\">")
        _e("Password protected")
        php_print("</label><br />\n<span id=\"password-span\"><label for=\"post_password\">")
        _e("Password:")
        php_print("</label> <input type=\"text\" name=\"post_password\" id=\"post_password\" value=\"")
        php_print(esc_attr(post.post_password))
        php_print("\"  maxlength=\"255\" /><br /></span>\n<input type=\"radio\" name=\"visibility\" id=\"visibility-radio-private\" value=\"private\" ")
        checked(visibility, "private")
        php_print(" /> <label for=\"visibility-radio-private\" class=\"selectit\">")
        _e("Private")
        php_print("""</label><br />
        <p>
        <a href=\"#visibility\" class=\"save-post-visibility hide-if-no-js button\">""")
        _e("OK")
        php_print("</a>\n   <a href=\"#visibility\" class=\"cancel-post-visibility hide-if-no-js button-cancel\">")
        _e("Cancel")
        php_print("""</a>
        </p>
        </div>
        """)
    # end if
    php_print("""
    </div><!-- .misc-pub-section -->
    """)
    #// translators: Publish box date string. 1: Date, 2: Time. See https://www.php.net/date
    date_string = __("%1$s at %2$s")
    #// translators: Publish box date format, see https://www.php.net/date
    date_format = _x("M j, Y", "publish box date format")
    #// translators: Publish box time format, see https://www.php.net/date
    time_format = _x("H:i", "publish box time format")
    if 0 != post.ID:
        if "future" == post.post_status:
            #// Scheduled for publishing at a future date.
            #// translators: Post date information. %s: Date on which the post is currently scheduled to be published.
            stamp = __("Scheduled for: %s")
        elif "publish" == post.post_status or "private" == post.post_status:
            #// Already published.
            #// translators: Post date information. %s: Date on which the post was published.
            stamp = __("Published on: %s")
        elif "0000-00-00 00:00:00" == post.post_date_gmt:
            #// Draft, 1 or more saves, no date specified.
            stamp = __("Publish <b>immediately</b>")
        elif time() < strtotime(post.post_date_gmt + " +0000"):
            #// Draft, 1 or more saves, future date specified.
            #// translators: Post date information. %s: Date on which the post is to be published.
            stamp = __("Schedule for: %s")
        else:
            #// Draft, 1 or more saves, date specified.
            #// translators: Post date information. %s: Date on which the post is to be published.
            stamp = __("Publish on: %s")
        # end if
        date = php_sprintf(date_string, date_i18n(date_format, strtotime(post.post_date)), date_i18n(time_format, strtotime(post.post_date)))
    else:
        #// Draft (no saves, and thus no date specified).
        stamp = __("Publish <b>immediately</b>")
        date = php_sprintf(date_string, date_i18n(date_format, strtotime(current_time("mysql"))), date_i18n(time_format, strtotime(current_time("mysql"))))
    # end if
    if (not php_empty(lambda : args["args"]["revisions_count"])):
        php_print("<div class=\"misc-pub-section misc-pub-revisions\">\n        ")
        #// translators: Post revisions heading. %s: The number of available revisions.
        printf(__("Revisions: %s"), "<b>" + number_format_i18n(args["args"]["revisions_count"]) + "</b>")
        php_print(" <a class=\"hide-if-no-js\" href=\"")
        php_print(esc_url(get_edit_post_link(args["args"]["revision_id"])))
        php_print("\"><span aria-hidden=\"true\">")
        _ex("Browse", "revisions")
        php_print("</span> <span class=\"screen-reader-text\">")
        _e("Browse revisions")
        php_print("</span></a>\n</div>\n        ")
    # end if
    if can_publish:
        pass
        php_print("<div class=\"misc-pub-section curtime misc-pub-curtime\">\n  <span id=\"timestamp\">\n       ")
        printf(stamp, "<b>" + date + "</b>")
        php_print(" </span>\n   <a href=\"#edit_timestamp\" class=\"edit-timestamp hide-if-no-js\" role=\"button\">\n       <span aria-hidden=\"true\">")
        _e("Edit")
        php_print("</span>\n        <span class=\"screen-reader-text\">")
        _e("Edit date and time")
        php_print("""</span>
        </a>
        <fieldset id=\"timestampdiv\" class=\"hide-if-js\">
        <legend class=\"screen-reader-text\">""")
        _e("Date and time")
        php_print("</legend>\n      ")
        touch_time("edit" == action, 1)
        php_print(" </fieldset>\n</div>")
        pass
    # end if
    php_print("\n   ")
    if "draft" == post.post_status and get_post_meta(post.ID, "_customize_changeset_uuid", True):
        php_print(" <div class=\"notice notice-info notice-alt inline\">\n      <p>\n           ")
        php_print(php_sprintf(__("This draft comes from your <a href=\"%s\">unpublished customization changes</a>. You can edit, but there&#8217;s no need to publish now. It will be published automatically with those changes."), esc_url(add_query_arg("changeset_uuid", rawurlencode(get_post_meta(post.ID, "_customize_changeset_uuid", True)), admin_url("customize.php")))))
        php_print("     </p>\n  </div>\n    ")
    # end if
    php_print("\n   ")
    #// 
    #// Fires after the post time/date setting in the Publish meta box.
    #// 
    #// @since 2.9.0
    #// @since 4.4.0 Added the `$post` parameter.
    #// 
    #// @param WP_Post $post WP_Post object for the current post.
    #//
    do_action("post_submitbox_misc_actions", post)
    php_print("""</div>
    <div class=\"clear\"></div>
    </div>
    <div id=\"major-publishing-actions\">
    """)
    #// 
    #// Fires at the beginning of the publishing actions section of the Publish meta box.
    #// 
    #// @since 2.7.0
    #// @since 4.9.0 Added the `$post` parameter.
    #// 
    #// @param WP_Post|null $post WP_Post object for the current post on Edit Post screen,
    #// null on Edit Link screen.
    #//
    do_action("post_submitbox_start", post)
    php_print("<div id=\"delete-action\">\n ")
    if current_user_can("delete_post", post.ID):
        if (not EMPTY_TRASH_DAYS):
            delete_text = __("Delete Permanently")
        else:
            delete_text = __("Move to Trash")
        # end if
        php_print("<a class=\"submitdelete deletion\" href=\"")
        php_print(get_delete_post_link(post.ID))
        php_print("\">")
        php_print(delete_text)
        php_print("</a>\n                                                   ")
    # end if
    php_print("""</div>
    <div id=\"publishing-action\">
    <span class=\"spinner\"></span>
    """)
    if (not php_in_array(post.post_status, Array("publish", "future", "private"))) or 0 == post.ID:
        if can_publish:
            if (not php_empty(lambda : post.post_date_gmt)) and time() < strtotime(post.post_date_gmt + " +0000"):
                php_print("     <input name=\"original_publish\" type=\"hidden\" id=\"original_publish\" value=\"")
                php_print(esc_attr_x("Schedule", "post action/button label"))
                php_print("\" />\n              ")
                submit_button(_x("Schedule", "post action/button label"), "primary large", "publish", False)
                php_print(" ")
            else:
                php_print("     <input name=\"original_publish\" type=\"hidden\" id=\"original_publish\" value=\"")
                esc_attr_e("Publish")
                php_print("\" />\n      ")
                submit_button(__("Publish"), "primary large", "publish", False)
                php_print("     ")
            # end if
        else:
            php_print("     <input name=\"original_publish\" type=\"hidden\" id=\"original_publish\" value=\"")
            esc_attr_e("Submit for Review")
            php_print("\" />\n      ")
            submit_button(__("Submit for Review"), "primary large", "publish", False)
            php_print("     ")
        # end if
    else:
        php_print("     <input name=\"original_publish\" type=\"hidden\" id=\"original_publish\" value=\"")
        esc_attr_e("Update")
        php_print("\" />\n      <input name=\"save\" type=\"submit\" class=\"button button-primary button-large\" id=\"publish\" value=\"")
        esc_attr_e("Update")
        php_print("\" />\n      ")
    # end if
    php_print("""</div>
    <div class=\"clear\"></div>
    </div>
    </div>
    """)
# end def post_submit_meta_box
#// 
#// Display attachment submit form fields.
#// 
#// @since 3.5.0
#// 
#// @param object $post
#//
def attachment_submit_meta_box(post=None, *args_):
    
    php_print("""<div class=\"submitbox\" id=\"submitpost\">
    <div id=\"minor-publishing\">
    """)
    pass
    php_print("<div style=\"display:none;\">\n  ")
    submit_button(__("Save"), "", "save")
    php_print("""</div>
    <div id=\"misc-publishing-actions\">
    <div class=\"misc-pub-section curtime misc-pub-curtime\">
    <span id=\"timestamp\">
    """)
    uploaded_on = php_sprintf(__("%1$s at %2$s"), date_i18n(_x("M j, Y", "publish box date format"), strtotime(post.post_date)), date_i18n(_x("H:i", "publish box time format"), strtotime(post.post_date)))
    #// translators: Attachment information. %s: Date the attachment was uploaded.
    printf(__("Uploaded on: %s"), "<b>" + uploaded_on + "</b>")
    php_print("""       </span>
    </div><!-- .misc-pub-section -->
    """)
    #// 
    #// Fires after the 'Uploaded on' section of the Save meta box
    #// in the attachment editing screen.
    #// 
    #// @since 3.5.0
    #// @since 4.9.0 Added the `$post` parameter.
    #// 
    #// @param WP_Post $post WP_Post object for the current attachment.
    #//
    do_action("attachment_submitbox_misc_actions", post)
    php_print("""</div><!-- #misc-publishing-actions -->
    <div class=\"clear\"></div>
    </div><!-- #minor-publishing -->
    <div id=\"major-publishing-actions\">
    <div id=\"delete-action\">
    """)
    if current_user_can("delete_post", post.ID):
        if EMPTY_TRASH_DAYS and MEDIA_TRASH:
            php_print("<a class='submitdelete deletion' href='" + get_delete_post_link(post.ID) + "'>" + __("Move to Trash") + "</a>")
        else:
            delete_ays = " onclick='return showNotice.warn();'" if (not MEDIA_TRASH) else ""
            php_print(str("<a class='submitdelete deletion'") + str(delete_ays) + str(" href='") + get_delete_post_link(post.ID, None, True) + "'>" + __("Delete Permanently") + "</a>")
        # end if
    # end if
    php_print("""   </div>
    <div id=\"publishing-action\">
    <span class=\"spinner\"></span>
    <input name=\"original_publish\" type=\"hidden\" id=\"original_publish\" value=\"""")
    esc_attr_e("Update")
    php_print("\" />\n      <input name=\"save\" type=\"submit\" class=\"button button-primary button-large\" id=\"publish\" value=\"")
    esc_attr_e("Update")
    php_print("""\" />
    </div>
    <div class=\"clear\"></div>
    </div><!-- #major-publishing-actions -->
    </div>
    """)
# end def attachment_submit_meta_box
#// 
#// Display post format form elements.
#// 
#// @since 3.1.0
#// 
#// @param WP_Post $post Post object.
#// @param array   $box {
#// Post formats meta box arguments.
#// 
#// @type string   $id       Meta box 'id' attribute.
#// @type string   $title    Meta box title.
#// @type callable $callback Meta box display callback.
#// @type array    $args     Extra meta box arguments.
#// }
#//
def post_format_meta_box(post=None, box=None, *args_):
    
    if current_theme_supports("post-formats") and post_type_supports(post.post_type, "post-formats"):
        post_formats = get_theme_support("post-formats")
        if php_is_array(post_formats[0]):
            post_format = get_post_format(post.ID)
            if (not post_format):
                post_format = "0"
            # end if
            #// Add in the current one if it isn't there yet, in case the current theme doesn't support it.
            if post_format and (not php_in_array(post_format, post_formats[0])):
                post_formats[0][-1] = post_format
            # end if
            php_print("     <div id=\"post-formats-select\">\n      <fieldset>\n            <legend class=\"screen-reader-text\">")
            _e("Post Formats")
            php_print("</legend>\n          <input type=\"radio\" name=\"post_format\" class=\"post-format\" id=\"post-format-0\" value=\"0\" ")
            checked(post_format, "0")
            php_print(" /> <label for=\"post-format-0\" class=\"post-format-icon post-format-standard\">")
            php_print(get_post_format_string("standard"))
            php_print("</label>\n           ")
            for format in post_formats[0]:
                php_print("         <br /><input type=\"radio\" name=\"post_format\" class=\"post-format\" id=\"post-format-")
                php_print(esc_attr(format))
                php_print("\" value=\"")
                php_print(esc_attr(format))
                php_print("\" ")
                checked(post_format, format)
                php_print(" /> <label for=\"post-format-")
                php_print(esc_attr(format))
                php_print("\" class=\"post-format-icon post-format-")
                php_print(esc_attr(format))
                php_print("\">")
                php_print(esc_html(get_post_format_string(format)))
                php_print("</label>\n           ")
            # end for
            php_print("     </fieldset>\n   </div>\n            ")
        # end if
    # end if
# end def post_format_meta_box
#// 
#// Display post tags form fields.
#// 
#// @since 2.6.0
#// 
#// @todo Create taxonomy-agnostic wrapper for this.
#// 
#// @param WP_Post $post Post object.
#// @param array   $box {
#// Tags meta box arguments.
#// 
#// @type string   $id       Meta box 'id' attribute.
#// @type string   $title    Meta box title.
#// @type callable $callback Meta box display callback.
#// @type array    $args {
#// Extra meta box arguments.
#// 
#// @type string $taxonomy Taxonomy. Default 'post_tag'.
#// }
#// }
#//
def post_tags_meta_box(post=None, box=None, *args_):
    
    defaults = Array({"taxonomy": "post_tag"})
    if (not (php_isset(lambda : box["args"]))) or (not php_is_array(box["args"])):
        args = Array()
    else:
        args = box["args"]
    # end if
    parsed_args = wp_parse_args(args, defaults)
    tax_name = esc_attr(parsed_args["taxonomy"])
    taxonomy = get_taxonomy(parsed_args["taxonomy"])
    user_can_assign_terms = current_user_can(taxonomy.cap.assign_terms)
    comma = _x(",", "tag delimiter")
    terms_to_edit = get_terms_to_edit(post.ID, tax_name)
    if (not php_is_string(terms_to_edit)):
        terms_to_edit = ""
    # end if
    php_print("<div class=\"tagsdiv\" id=\"")
    php_print(tax_name)
    php_print("""\">
    <div class=\"jaxtag\">
    <div class=\"nojs-tags hide-if-js\">
    <label for=\"tax-input-""")
    php_print(tax_name)
    php_print("\">")
    php_print(taxonomy.labels.add_or_remove_items)
    php_print("</label>\n       <p><textarea name=\"")
    php_print(str("tax_input[") + str(tax_name) + str("]"))
    php_print("\" rows=\"3\" cols=\"20\" class=\"the-tags\" id=\"tax-input-")
    php_print(tax_name)
    php_print("\" ")
    disabled((not user_can_assign_terms))
    php_print(" aria-describedby=\"new-tag-")
    php_print(tax_name)
    php_print("-desc\">")
    php_print(php_str_replace(",", comma + " ", terms_to_edit))
    pass
    php_print("</textarea></p>\n    </div>\n    ")
    if user_can_assign_terms:
        php_print(" <div class=\"ajaxtag hide-if-no-js\">\n     <label class=\"screen-reader-text\" for=\"new-tag-")
        php_print(tax_name)
        php_print("\">")
        php_print(taxonomy.labels.add_new_item)
        php_print("</label>\n       <input data-wp-taxonomy=\"")
        php_print(tax_name)
        php_print("\" type=\"text\" id=\"new-tag-")
        php_print(tax_name)
        php_print("\" name=\"newtag[")
        php_print(tax_name)
        php_print("]\" class=\"newtag form-input-tip\" size=\"16\" autocomplete=\"off\" aria-describedby=\"new-tag-")
        php_print(tax_name)
        php_print("-desc\" value=\"\" />\n      <input type=\"button\" class=\"button tagadd\" value=\"")
        esc_attr_e("Add")
        php_print("\" />\n  </div>\n    <p class=\"howto\" id=\"new-tag-")
        php_print(tax_name)
        php_print("-desc\">")
        php_print(taxonomy.labels.separate_items_with_commas)
        php_print("</p>\n   ")
    elif php_empty(lambda : terms_to_edit):
        php_print("     <p>")
        php_print(taxonomy.labels.no_terms)
        php_print("</p>\n   ")
    # end if
    php_print("""   </div>
    <ul class=\"tagchecklist\" role=\"list\"></ul>
    </div>
    """)
    if user_can_assign_terms:
        php_print("<p class=\"hide-if-no-js\"><button type=\"button\" class=\"button-link tagcloud-link\" id=\"link-")
        php_print(tax_name)
        php_print("\" aria-expanded=\"false\">")
        php_print(taxonomy.labels.choose_from_most_used)
        php_print("</button></p>\n")
    # end if
    php_print(" ")
# end def post_tags_meta_box
#// 
#// Display post categories form fields.
#// 
#// @since 2.6.0
#// 
#// @todo Create taxonomy-agnostic wrapper for this.
#// 
#// @param WP_Post $post Post object.
#// @param array   $box {
#// Categories meta box arguments.
#// 
#// @type string   $id       Meta box 'id' attribute.
#// @type string   $title    Meta box title.
#// @type callable $callback Meta box display callback.
#// @type array    $args {
#// Extra meta box arguments.
#// 
#// @type string $taxonomy Taxonomy. Default 'category'.
#// }
#// }
#//
def post_categories_meta_box(post=None, box=None, *args_):
    
    defaults = Array({"taxonomy": "category"})
    if (not (php_isset(lambda : box["args"]))) or (not php_is_array(box["args"])):
        args = Array()
    else:
        args = box["args"]
    # end if
    parsed_args = wp_parse_args(args, defaults)
    tax_name = esc_attr(parsed_args["taxonomy"])
    taxonomy = get_taxonomy(parsed_args["taxonomy"])
    php_print(" <div id=\"taxonomy-")
    php_print(tax_name)
    php_print("\" class=\"categorydiv\">\n      <ul id=\"")
    php_print(tax_name)
    php_print("-tabs\" class=\"category-tabs\">\n           <li class=\"tabs\"><a href=\"#")
    php_print(tax_name)
    php_print("-all\">")
    php_print(taxonomy.labels.all_items)
    php_print("</a></li>\n          <li class=\"hide-if-no-js\"><a href=\"#")
    php_print(tax_name)
    php_print("-pop\">")
    php_print(esc_html(taxonomy.labels.most_used))
    php_print("""</a></li>
    </ul>
    <div id=\"""")
    php_print(tax_name)
    php_print("-pop\" class=\"tabs-panel\" style=\"display: none;\">\n          <ul id=\"")
    php_print(tax_name)
    php_print("checklist-pop\" class=\"categorychecklist form-no-clear\" >\n                ")
    popular_ids = wp_popular_terms_checklist(tax_name)
    php_print("""           </ul>
    </div>
    <div id=\"""")
    php_print(tax_name)
    php_print("-all\" class=\"tabs-panel\">\n           ")
    name = "post_category" if "category" == tax_name else "tax_input[" + tax_name + "]"
    #// Allows for an empty term set to be sent. 0 is an invalid term ID and will be ignored by empty() checks.
    php_print(str("<input type='hidden' name='") + str(name) + str("[]' value='0' />"))
    php_print("         <ul id=\"")
    php_print(tax_name)
    php_print("checklist\" data-wp-lists=\"list:")
    php_print(tax_name)
    php_print("\" class=\"categorychecklist form-no-clear\">\n              ")
    wp_terms_checklist(post.ID, Array({"taxonomy": tax_name, "popular_cats": popular_ids}))
    php_print("         </ul>\n     </div>\n    ")
    if current_user_can(taxonomy.cap.edit_terms):
        php_print("         <div id=\"")
        php_print(tax_name)
        php_print("-adder\" class=\"wp-hidden-children\">\n             <a id=\"")
        php_print(tax_name)
        php_print("-add-toggle\" href=\"#")
        php_print(tax_name)
        php_print("-add\" class=\"hide-if-no-js taxonomy-add-new\">\n                   ")
        #// translators: %s: Add New taxonomy label.
        printf(__("+ %s"), taxonomy.labels.add_new_item)
        php_print("             </a>\n              <p id=\"")
        php_print(tax_name)
        php_print("-add\" class=\"category-add wp-hidden-child\">\n                 <label class=\"screen-reader-text\" for=\"new")
        php_print(tax_name)
        php_print("\">")
        php_print(taxonomy.labels.add_new_item)
        php_print("</label>\n                   <input type=\"text\" name=\"new")
        php_print(tax_name)
        php_print("\" id=\"new")
        php_print(tax_name)
        php_print("\" class=\"form-required form-input-tip\" value=\"")
        php_print(esc_attr(taxonomy.labels.new_item_name))
        php_print("\" aria-required=\"true\"/>\n                    <label class=\"screen-reader-text\" for=\"new")
        php_print(tax_name)
        php_print("_parent\">\n                     ")
        php_print(taxonomy.labels.parent_item_colon)
        php_print("                 </label>\n                  ")
        parent_dropdown_args = Array({"taxonomy": tax_name, "hide_empty": 0, "name": "new" + tax_name + "_parent", "orderby": "name", "hierarchical": 1, "show_option_none": "&mdash; " + taxonomy.labels.parent_item + " &mdash;"})
        #// 
        #// Filters the arguments for the taxonomy parent dropdown on the Post Edit page.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array $parent_dropdown_args {
        #// Optional. Array of arguments to generate parent dropdown.
        #// 
        #// @type string   $taxonomy         Name of the taxonomy to retrieve.
        #// @type bool     $hide_if_empty    True to skip generating markup if no
        #// categories are found. Default 0.
        #// @type string   $name             Value for the 'name' attribute
        #// of the select element.
        #// Default "new{$tax_name}_parent".
        #// @type string   $orderby          Which column to use for ordering
        #// terms. Default 'name'.
        #// @type bool|int $hierarchical     Whether to traverse the taxonomy
        #// hierarchy. Default 1.
        #// @type string   $show_option_none Text to display for the "none" option.
        #// Default "&mdash; {$parent} &mdash;",
        #// where `$parent` is 'parent_item'
        #// taxonomy label.
        #// }
        #//
        parent_dropdown_args = apply_filters("post_edit_category_parent_dropdown_args", parent_dropdown_args)
        wp_dropdown_categories(parent_dropdown_args)
        php_print("                 <input type=\"button\" id=\"")
        php_print(tax_name)
        php_print("-add-submit\" data-wp-lists=\"add:")
        php_print(tax_name)
        php_print("checklist:")
        php_print(tax_name)
        php_print("-add\" class=\"button category-add-submit\" value=\"")
        php_print(esc_attr(taxonomy.labels.add_new_item))
        php_print("\" />\n                  ")
        wp_nonce_field("add-" + tax_name, "_ajax_nonce-add-" + tax_name, False)
        php_print("                 <span id=\"")
        php_print(tax_name)
        php_print("""-ajax-response\"></span>
        </p>
        </div>
        """)
    # end if
    php_print(" </div>\n    ")
# end def post_categories_meta_box
#// 
#// Display post excerpt form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $post
#//
def post_excerpt_meta_box(post=None, *args_):
    
    php_print("<label class=\"screen-reader-text\" for=\"excerpt\">")
    _e("Excerpt")
    php_print("</label><textarea rows=\"1\" cols=\"40\" name=\"excerpt\" id=\"excerpt\">")
    php_print(post.post_excerpt)
    pass
    php_print("</textarea>\n<p>\n   ")
    printf(__("Excerpts are optional hand-crafted summaries of your content that can be used in your theme. <a href=\"%s\">Learn more about manual excerpts</a>."), __("https://wordpress.org/support/article/excerpt/"))
    php_print("</p>\n   ")
# end def post_excerpt_meta_box
#// 
#// Display trackback links form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $post
#//
def post_trackback_meta_box(post=None, *args_):
    
    form_trackback = "<input type=\"text\" name=\"trackback_url\" id=\"trackback_url\" class=\"code\" value=\"" + esc_attr(php_str_replace("\n", " ", post.to_ping)) + "\" aria-describedby=\"trackback-url-desc\" />"
    if "" != post.pinged:
        pings = "<p>" + __("Already pinged:") + "</p><ul>"
        already_pinged = php_explode("\n", php_trim(post.pinged))
        for pinged_url in already_pinged:
            pings += "\n    <li>" + esc_html(pinged_url) + "</li>"
        # end for
        pings += "</ul>"
    # end if
    php_print("<p>\n    <label for=\"trackback_url\">")
    _e("Send trackbacks to:")
    php_print("</label>\n   ")
    php_print(form_trackback)
    php_print("</p>\n<p id=\"trackback-url-desc\" class=\"howto\">")
    _e("Separate multiple URLs with spaces")
    php_print("</p>\n<p>\n  ")
    printf(__("Trackbacks are a way to notify legacy blog systems that you&#8217;ve linked to them. If you link other WordPress sites, they&#8217;ll be notified automatically using <a href=\"%s\">pingbacks</a>, no other action necessary."), __("https://wordpress.org/support/article/introduction-to-blogging/#comments"))
    php_print("</p>\n   ")
    if (not php_empty(lambda : pings)):
        php_print(pings)
    # end if
# end def post_trackback_meta_box
#// 
#// Display custom fields form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $post
#//
def post_custom_meta_box(post=None, *args_):
    
    php_print("<div id=\"postcustomstuff\">\n<div id=\"ajax-response\"></div>\n ")
    metadata = has_meta(post.ID)
    for key,value in metadata:
        if is_protected_meta(metadata[key]["meta_key"], "post") or (not current_user_can("edit_post_meta", post.ID, metadata[key]["meta_key"])):
            metadata[key] = None
        # end if
    # end for
    list_meta(metadata)
    meta_form(post)
    php_print("</div>\n<p>\n    ")
    printf(__("Custom fields can be used to add extra metadata to a post that you can <a href=\"%s\">use in your theme</a>."), __("https://wordpress.org/support/article/custom-fields/"))
    php_print("</p>\n   ")
# end def post_custom_meta_box
#// 
#// Display comments status form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $post
#//
def post_comment_status_meta_box(post=None, *args_):
    
    php_print("<input name=\"advanced_view\" type=\"hidden\" value=\"1\" />\n<p class=\"meta-options\">\n   <label for=\"comment_status\" class=\"selectit\"><input name=\"comment_status\" type=\"checkbox\" id=\"comment_status\" value=\"open\" ")
    checked(post.comment_status, "open")
    php_print(" /> ")
    _e("Allow comments")
    php_print("</label><br />\n <label for=\"ping_status\" class=\"selectit\"><input name=\"ping_status\" type=\"checkbox\" id=\"ping_status\" value=\"open\" ")
    checked(post.ping_status, "open")
    php_print(" />\n        ")
    printf(__("Allow <a href=\"%s\">trackbacks and pingbacks</a> on this page"), __("https://wordpress.org/support/article/introduction-to-blogging/#managing-comments"))
    php_print(" </label>\n  ")
    #// 
    #// Fires at the end of the Discussion meta box on the post editing screen.
    #// 
    #// @since 3.1.0
    #// 
    #// @param WP_Post $post WP_Post object of the current post.
    #//
    do_action("post_comment_status_meta_box-options", post)
    pass
    php_print("</p>\n   ")
# end def post_comment_status_meta_box
#// 
#// Display comments for post table header
#// 
#// @since 3.0.0
#// 
#// @param array $result table header rows
#// @return array
#//
def post_comment_meta_box_thead(result=None, *args_):
    
    result["cb"] = None
    result["response"] = None
    return result
# end def post_comment_meta_box_thead
#// 
#// Display comments for post.
#// 
#// @since 2.8.0
#// 
#// @param object $post
#//
def post_comment_meta_box(post=None, *args_):
    
    wp_nonce_field("get-comments", "add_comment_nonce", False)
    php_print(" <p class=\"hide-if-no-js\" id=\"add-new-comment\"><button type=\"button\" class=\"button\" onclick=\"window.commentReply && commentReply.addcomment(")
    php_print(post.ID)
    php_print(");\">")
    _e("Add Comment")
    php_print("</button></p>\n  ")
    total = get_comments(Array({"post_id": post.ID, "number": 1, "count": True}))
    wp_list_table = _get_list_table("WP_Post_Comments_List_Table")
    wp_list_table.display(True)
    if 1 > total:
        php_print("<p id=\"no-comments\">" + __("No comments yet.") + "</p>")
    else:
        hidden = get_hidden_meta_boxes(get_current_screen())
        if (not php_in_array("commentsdiv", hidden)):
            php_print("         <script type=\"text/javascript\">jQuery(document).ready(function(){commentsBox.get(")
            php_print(total)
            php_print(", 10);});</script>\n         ")
        # end if
        php_print("     <p class=\"hide-if-no-js\" id=\"show-comments\"><a href=\"#commentstatusdiv\" onclick=\"commentsBox.load(")
        php_print(total)
        php_print(");return false;\">")
        _e("Show comments")
        php_print("</a> <span class=\"spinner\"></span></p>\n       ")
    # end if
    wp_comment_trashnotice()
# end def post_comment_meta_box
#// 
#// Display slug form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $post
#//
def post_slug_meta_box(post=None, *args_):
    
    #// This filter is documented in wp-admin/edit-tag-form.php
    editable_slug = apply_filters("editable_slug", post.post_name, post)
    php_print("<label class=\"screen-reader-text\" for=\"post_name\">")
    _e("Slug")
    php_print("</label><input name=\"post_name\" type=\"text\" size=\"13\" id=\"post_name\" value=\"")
    php_print(esc_attr(editable_slug))
    php_print("\" />\n  ")
# end def post_slug_meta_box
#// 
#// Display form field with list of authors.
#// 
#// @since 2.6.0
#// 
#// @global int $user_ID
#// 
#// @param object $post
#//
def post_author_meta_box(post=None, *args_):
    
    global user_ID
    php_check_if_defined("user_ID")
    php_print("<label class=\"screen-reader-text\" for=\"post_author_override\">")
    _e("Author")
    php_print("</label>\n   ")
    wp_dropdown_users(Array({"who": "authors", "name": "post_author_override", "selected": user_ID if php_empty(lambda : post.ID) else post.post_author, "include_selected": True, "show": "display_name_with_login"}))
# end def post_author_meta_box
#// 
#// Display list of revisions.
#// 
#// @since 2.6.0
#// 
#// @param object $post
#//
def post_revisions_meta_box(post=None, *args_):
    
    wp_list_post_revisions(post)
# end def post_revisions_meta_box
#// 
#// Page-related Meta Boxes.
#// 
#// 
#// Display page attributes form fields.
#// 
#// @since 2.7.0
#// 
#// @param object $post
#//
def page_attributes_meta_box(post=None, *args_):
    
    if is_post_type_hierarchical(post.post_type):
        dropdown_args = Array({"post_type": post.post_type, "exclude_tree": post.ID, "selected": post.post_parent, "name": "parent_id", "show_option_none": __("(no parent)"), "sort_column": "menu_order, post_title", "echo": 0})
        #// 
        #// Filters the arguments used to generate a Pages drop-down element.
        #// 
        #// @since 3.3.0
        #// 
        #// @see wp_dropdown_pages()
        #// 
        #// @param array   $dropdown_args Array of arguments used to generate the pages drop-down.
        #// @param WP_Post $post          The current post.
        #//
        dropdown_args = apply_filters("page_attributes_dropdown_pages_args", dropdown_args, post)
        pages = wp_dropdown_pages(dropdown_args)
        if (not php_empty(lambda : pages)):
            php_print("<p class=\"post-attributes-label-wrapper parent-id-label-wrapper\"><label class=\"post-attributes-label\" for=\"parent_id\">")
            _e("Parent")
            php_print("</label></p>\n           ")
            php_print(pages)
            php_print("         ")
        # end if
        pass
    # end if
    #// End hierarchical check.
    if php_count(get_page_templates(post)) > 0 and get_option("page_for_posts") != post.ID:
        template = post.page_template if (not php_empty(lambda : post.page_template)) else False
        php_print("<p class=\"post-attributes-label-wrapper page-template-label-wrapper\"><label class=\"post-attributes-label\" for=\"page_template\">")
        _e("Template")
        php_print("</label>\n       ")
        #// 
        #// Fires immediately after the label inside the 'Template' section
        #// of the 'Page Attributes' meta box.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string  $template The template used for the current post.
        #// @param WP_Post $post     The current post.
        #//
        do_action("page_attributes_meta_box_template", template, post)
        php_print("</p>\n<select name=\"page_template\" id=\"page_template\">\n     ")
        #// 
        #// Filters the title of the default page template displayed in the drop-down.
        #// 
        #// @since 4.1.0
        #// 
        #// @param string $label   The display value for the default page template title.
        #// @param string $context Where the option label is displayed. Possible values
        #// include 'meta-box' or 'quick-edit'.
        #//
        default_title = apply_filters("default_page_template_title", __("Default Template"), "meta-box")
        php_print("<option value=\"default\">")
        php_print(esc_html(default_title))
        php_print("</option>\n      ")
        page_template_dropdown(template, post.post_type)
        php_print("</select>\n")
    # end if
    php_print(" ")
    if post_type_supports(post.post_type, "page-attributes"):
        php_print("<p class=\"post-attributes-label-wrapper menu-order-label-wrapper\"><label class=\"post-attributes-label\" for=\"menu_order\">")
        _e("Order")
        php_print("</label></p>\n<input name=\"menu_order\" type=\"text\" size=\"4\" id=\"menu_order\" value=\"")
        php_print(esc_attr(post.menu_order))
        php_print("\" />\n      ")
        #// 
        #// Fires before the help hint text in the 'Page Attributes' meta box.
        #// 
        #// @since 4.9.0
        #// 
        #// @param WP_Post $post The current post.
        #//
        do_action("page_attributes_misc_attributes", post)
        php_print("     ")
        if "page" == post.post_type and get_current_screen().get_help_tabs():
            php_print("<p class=\"post-attributes-help-text\">")
            _e("Need help? Use the Help tab above the screen title.")
            php_print("</p>\n           ")
        # end if
    # end if
# end def page_attributes_meta_box
#// 
#// Link-related Meta Boxes.
#// 
#// 
#// Display link create form fields.
#// 
#// @since 2.7.0
#// 
#// @param object $link
#//
def link_submit_meta_box(link=None, *args_):
    
    php_print("""<div class=\"submitbox\" id=\"submitlink\">
    <div id=\"minor-publishing\">
    """)
    pass
    php_print("<div style=\"display:none;\">\n  ")
    submit_button(__("Save"), "", "save", False)
    php_print("""</div>
    <div id=\"minor-publishing-actions\">
    <div id=\"preview-action\">
    """)
    if (not php_empty(lambda : link.link_id)):
        php_print(" <a class=\"preview button\" href=\"")
        php_print(link.link_url)
        php_print("\" target=\"_blank\">")
        _e("Visit Link")
        php_print("</a>\n")
    # end if
    php_print("""</div>
    <div class=\"clear\"></div>
    </div>
    <div id=\"misc-publishing-actions\">
    <div class=\"misc-pub-section misc-pub-private\">
    <label for=\"link_private\" class=\"selectit\"><input id=\"link_private\" name=\"link_visible\" type=\"checkbox\" value=\"N\" """)
    checked(link.link_visible, "N")
    php_print(" /> ")
    _e("Keep this link private")
    php_print("""</label>
    </div>
    </div>
    </div>
    <div id=\"major-publishing-actions\">
    """)
    #// This action is documented in wp-admin/includes/meta-boxes.php
    do_action("post_submitbox_start", None)
    php_print("<div id=\"delete-action\">\n ")
    if (not php_empty(lambda : PHP_REQUEST["action"])) and "edit" == PHP_REQUEST["action"] and current_user_can("manage_links"):
        printf("<a class=\"submitdelete deletion\" href=\"%s\" onclick=\"return confirm( '%s' );\">%s</a>", wp_nonce_url(str("link.php?action=delete&amp;link_id=") + str(link.link_id), "delete-bookmark_" + link.link_id), esc_js(php_sprintf(__("You are about to delete this link '%s'\n  'Cancel' to stop, 'OK' to delete."), link.link_name)), __("Delete"))
    # end if
    php_print("""</div>
    <div id=\"publishing-action\">
    """)
    if (not php_empty(lambda : link.link_id)):
        php_print(" <input name=\"save\" type=\"submit\" class=\"button button-primary button-large\" id=\"publish\" value=\"")
        esc_attr_e("Update Link")
        php_print("\" />\n")
    else:
        php_print(" <input name=\"save\" type=\"submit\" class=\"button button-primary button-large\" id=\"publish\" value=\"")
        esc_attr_e("Add Link")
        php_print("\" />\n")
    # end if
    php_print("""</div>
    <div class=\"clear\"></div>
    </div>
    """)
    #// 
    #// Fires at the end of the Publish box in the Link editing screen.
    #// 
    #// @since 2.5.0
    #//
    do_action("submitlink_box")
    php_print("<div class=\"clear\"></div>\n</div>\n    ")
# end def link_submit_meta_box
#// 
#// Display link categories form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $link
#//
def link_categories_meta_box(link=None, *args_):
    
    php_print("<div id=\"taxonomy-linkcategory\" class=\"categorydiv\">\n   <ul id=\"category-tabs\" class=\"category-tabs\">\n     <li class=\"tabs\"><a href=\"#categories-all\">")
    _e("All Categories")
    php_print("</a></li>\n      <li class=\"hide-if-no-js\"><a href=\"#categories-pop\">")
    _ex("Most Used", "categories")
    php_print("""</a></li>
    </ul>
    <div id=\"categories-all\" class=\"tabs-panel\">
    <ul id=\"categorychecklist\" data-wp-lists=\"list:category\" class=\"categorychecklist form-no-clear\">
    """)
    if (php_isset(lambda : link.link_id)):
        wp_link_category_checklist(link.link_id)
    else:
        wp_link_category_checklist()
    # end if
    php_print("""       </ul>
    </div>
    <div id=\"categories-pop\" class=\"tabs-panel\" style=\"display: none;\">
    <ul id=\"categorychecklist-pop\" class=\"categorychecklist form-no-clear\">
    """)
    wp_popular_terms_checklist("link_category")
    php_print("""       </ul>
    </div>
    <div id=\"category-adder\" class=\"wp-hidden-children\">
    <a id=\"category-add-toggle\" href=\"#category-add\" class=\"taxonomy-add-new\">""")
    _e("+ Add New Category")
    php_print("</a>\n       <p id=\"link-category-add\" class=\"wp-hidden-child\">\n            <label class=\"screen-reader-text\" for=\"newcat\">")
    _e("+ Add New Category")
    php_print("</label>\n           <input type=\"text\" name=\"newcat\" id=\"newcat\" class=\"form-required form-input-tip\" value=\"")
    esc_attr_e("New category name")
    php_print("\" aria-required=\"true\" />\n           <input type=\"button\" id=\"link-category-add-submit\" data-wp-lists=\"add:categorychecklist:link-category-add\" class=\"button\" value=\"")
    esc_attr_e("Add")
    php_print("\" />\n          ")
    wp_nonce_field("add-link-category", "_ajax_nonce", False)
    php_print("""           <span id=\"category-ajax-response\"></span>
    </p>
    </div>
    </div>
    """)
# end def link_categories_meta_box
#// 
#// Display form fields for changing link target.
#// 
#// @since 2.6.0
#// 
#// @param object $link
#//
def link_target_meta_box(link=None, *args_):
    
    php_print("<fieldset><legend class=\"screen-reader-text\"><span>")
    _e("Target")
    php_print("</span></legend>\n<p><label for=\"link_target_blank\" class=\"selectit\">\n<input id=\"link_target_blank\" type=\"radio\" name=\"link_target\" value=\"_blank\" ")
    php_print("checked=\"checked\"" if (php_isset(lambda : link.link_target)) and "_blank" == link.link_target else "")
    php_print(" />\n    ")
    _e("<code>_blank</code> &mdash; new window or tab.")
    php_print("</label></p>\n<p><label for=\"link_target_top\" class=\"selectit\">\n<input id=\"link_target_top\" type=\"radio\" name=\"link_target\" value=\"_top\" ")
    php_print("checked=\"checked\"" if (php_isset(lambda : link.link_target)) and "_top" == link.link_target else "")
    php_print(" />\n    ")
    _e("<code>_top</code> &mdash; current window or tab, with no frames.")
    php_print("</label></p>\n<p><label for=\"link_target_none\" class=\"selectit\">\n<input id=\"link_target_none\" type=\"radio\" name=\"link_target\" value=\"\" ")
    php_print("checked=\"checked\"" if (php_isset(lambda : link.link_target)) and "" == link.link_target else "")
    php_print(" />\n    ")
    _e("<code>_none</code> &mdash; same window or tab.")
    php_print("</label></p>\n</fieldset>\n<p>")
    _e("Choose the target frame for your link.")
    php_print("</p>\n   ")
# end def link_target_meta_box
#// 
#// Display checked checkboxes attribute for xfn microformat options.
#// 
#// @since 1.0.1
#// 
#// @global object $link
#// 
#// @param string $class
#// @param string $value
#// @param mixed $deprecated Never used.
#//
def xfn_check(class_=None, value="", deprecated="", *args_):
    
    global link
    php_check_if_defined("link")
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.5.0")
        pass
    # end if
    link_rel = link.link_rel if (php_isset(lambda : link.link_rel)) else ""
    #// In PHP 5.3: $link_rel = $link->link_rel ?: '';
    rels = php_preg_split("/\\s+/", link_rel)
    if "" != value and php_in_array(value, rels):
        php_print(" checked=\"checked\"")
    # end if
    if "" == value:
        if "family" == class_ and php_strpos(link_rel, "child") == False and php_strpos(link_rel, "parent") == False and php_strpos(link_rel, "sibling") == False and php_strpos(link_rel, "spouse") == False and php_strpos(link_rel, "kin") == False:
            php_print(" checked=\"checked\"")
        # end if
        if "friendship" == class_ and php_strpos(link_rel, "friend") == False and php_strpos(link_rel, "acquaintance") == False and php_strpos(link_rel, "contact") == False:
            php_print(" checked=\"checked\"")
        # end if
        if "geographical" == class_ and php_strpos(link_rel, "co-resident") == False and php_strpos(link_rel, "neighbor") == False:
            php_print(" checked=\"checked\"")
        # end if
        if "identity" == class_ and php_in_array("me", rels):
            php_print(" checked=\"checked\"")
        # end if
    # end if
# end def xfn_check
#// 
#// Display xfn form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $link
#//
def link_xfn_meta_box(link=None, *args_):
    
    php_print("<table class=\"links-table\">\n  <tr>\n      <th scope=\"row\"><label for=\"link_rel\">")
    #// translators: xfn: http://gmpg.org/xfn
    _e("rel:")
    php_print("</label></th>\n      <td><input type=\"text\" name=\"link_rel\" id=\"link_rel\" value=\"")
    php_print(esc_attr(link.link_rel) if (php_isset(lambda : link.link_rel)) else "")
    php_print("""\" /></td>
    </tr>
    <tr>
    <th scope=\"row\">""")
    #// translators: xfn: http://gmpg.org/xfn
    _e("identity")
    php_print("</th>\n      <td><fieldset><legend class=\"screen-reader-text\"><span>")
    #// translators: xfn: http://gmpg.org/xfn
    _e("identity")
    php_print("</span></legend>\n           <label for=\"me\">\n            <input type=\"checkbox\" name=\"identity\" value=\"me\" id=\"me\" ")
    xfn_check("identity", "me")
    php_print(" />\n            ")
    _e("another web address of mine")
    php_print("""</label>
    </fieldset></td>
    </tr>
    <tr>
    <th scope=\"row\">""")
    #// translators: xfn: http://gmpg.org/xfn
    _e("friendship")
    php_print("</th>\n      <td><fieldset><legend class=\"screen-reader-text\"><span>")
    #// translators: xfn: http://gmpg.org/xfn
    _e("friendship")
    php_print("</span></legend>\n           <label for=\"contact\">\n           <input class=\"valinp\" type=\"radio\" name=\"friendship\" value=\"contact\" id=\"contact\" ")
    xfn_check("friendship", "contact")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("contact")
    php_print("         </label>\n          <label for=\"acquaintance\">\n          <input class=\"valinp\" type=\"radio\" name=\"friendship\" value=\"acquaintance\" id=\"acquaintance\" ")
    xfn_check("friendship", "acquaintance")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("acquaintance")
    php_print("         </label>\n          <label for=\"friend\">\n            <input class=\"valinp\" type=\"radio\" name=\"friendship\" value=\"friend\" id=\"friend\" ")
    xfn_check("friendship", "friend")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("friend")
    php_print("         </label>\n          <label for=\"friendship\">\n            <input name=\"friendship\" type=\"radio\" class=\"valinp\" value=\"\" id=\"friendship\" ")
    xfn_check("friendship")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("none")
    php_print("""           </label>
    </fieldset></td>
    </tr>
    <tr>
    <th scope=\"row\"> """)
    #// translators: xfn: http://gmpg.org/xfn
    _e("physical")
    php_print(" </th>\n     <td><fieldset><legend class=\"screen-reader-text\"><span>")
    #// translators: xfn: http://gmpg.org/xfn
    _e("physical")
    php_print("</span></legend>\n           <label for=\"met\">\n           <input class=\"valinp\" type=\"checkbox\" name=\"physical\" value=\"met\" id=\"met\" ")
    xfn_check("physical", "met")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("met")
    php_print("""           </label>
    </fieldset></td>
    </tr>
    <tr>
    <th scope=\"row\"> """)
    #// translators: xfn: http://gmpg.org/xfn
    _e("professional")
    php_print(" </th>\n     <td><fieldset><legend class=\"screen-reader-text\"><span>")
    #// translators: xfn: http://gmpg.org/xfn
    _e("professional")
    php_print("</span></legend>\n           <label for=\"co-worker\">\n         <input class=\"valinp\" type=\"checkbox\" name=\"professional\" value=\"co-worker\" id=\"co-worker\" ")
    xfn_check("professional", "co-worker")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("co-worker")
    php_print("         </label>\n          <label for=\"colleague\">\n         <input class=\"valinp\" type=\"checkbox\" name=\"professional\" value=\"colleague\" id=\"colleague\" ")
    xfn_check("professional", "colleague")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("colleague")
    php_print("""           </label>
    </fieldset></td>
    </tr>
    <tr>
    <th scope=\"row\">""")
    #// translators: xfn: http://gmpg.org/xfn
    _e("geographical")
    php_print("</th>\n      <td><fieldset><legend class=\"screen-reader-text\"><span> ")
    #// translators: xfn: http://gmpg.org/xfn
    _e("geographical")
    php_print(" </span></legend>\n          <label for=\"co-resident\">\n           <input class=\"valinp\" type=\"radio\" name=\"geographical\" value=\"co-resident\" id=\"co-resident\" ")
    xfn_check("geographical", "co-resident")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("co-resident")
    php_print("         </label>\n          <label for=\"neighbor\">\n          <input class=\"valinp\" type=\"radio\" name=\"geographical\" value=\"neighbor\" id=\"neighbor\" ")
    xfn_check("geographical", "neighbor")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("neighbor")
    php_print("         </label>\n          <label for=\"geographical\">\n          <input class=\"valinp\" type=\"radio\" name=\"geographical\" value=\"\" id=\"geographical\" ")
    xfn_check("geographical")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("none")
    php_print("""           </label>
    </fieldset></td>
    </tr>
    <tr>
    <th scope=\"row\">""")
    #// translators: xfn: http://gmpg.org/xfn
    _e("family")
    php_print("</th>\n      <td><fieldset><legend class=\"screen-reader-text\"><span> ")
    #// translators: xfn: http://gmpg.org/xfn
    _e("family")
    php_print(" </span></legend>\n          <label for=\"child\">\n         <input class=\"valinp\" type=\"radio\" name=\"family\" value=\"child\" id=\"child\" ")
    xfn_check("family", "child")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("child")
    php_print("         </label>\n          <label for=\"kin\">\n           <input class=\"valinp\" type=\"radio\" name=\"family\" value=\"kin\" id=\"kin\" ")
    xfn_check("family", "kin")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("kin")
    php_print("         </label>\n          <label for=\"parent\">\n            <input class=\"valinp\" type=\"radio\" name=\"family\" value=\"parent\" id=\"parent\" ")
    xfn_check("family", "parent")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("parent")
    php_print("         </label>\n          <label for=\"sibling\">\n           <input class=\"valinp\" type=\"radio\" name=\"family\" value=\"sibling\" id=\"sibling\" ")
    xfn_check("family", "sibling")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("sibling")
    php_print("         </label>\n          <label for=\"spouse\">\n            <input class=\"valinp\" type=\"radio\" name=\"family\" value=\"spouse\" id=\"spouse\" ")
    xfn_check("family", "spouse")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("spouse")
    php_print("         </label>\n          <label for=\"family\">\n            <input class=\"valinp\" type=\"radio\" name=\"family\" value=\"\" id=\"family\" ")
    xfn_check("family")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("none")
    php_print("""           </label>
    </fieldset></td>
    </tr>
    <tr>
    <th scope=\"row\">""")
    #// translators: xfn: http://gmpg.org/xfn
    _e("romantic")
    php_print("</th>\n      <td><fieldset><legend class=\"screen-reader-text\"><span> ")
    #// translators: xfn: http://gmpg.org/xfn
    _e("romantic")
    php_print(" </span></legend>\n          <label for=\"muse\">\n          <input class=\"valinp\" type=\"checkbox\" name=\"romantic\" value=\"muse\" id=\"muse\" ")
    xfn_check("romantic", "muse")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("muse")
    php_print("         </label>\n          <label for=\"crush\">\n         <input class=\"valinp\" type=\"checkbox\" name=\"romantic\" value=\"crush\" id=\"crush\" ")
    xfn_check("romantic", "crush")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("crush")
    php_print("         </label>\n          <label for=\"date\">\n          <input class=\"valinp\" type=\"checkbox\" name=\"romantic\" value=\"date\" id=\"date\" ")
    xfn_check("romantic", "date")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("date")
    php_print("         </label>\n          <label for=\"romantic\">\n          <input class=\"valinp\" type=\"checkbox\" name=\"romantic\" value=\"sweetheart\" id=\"romantic\" ")
    xfn_check("romantic", "sweetheart")
    php_print(" />&nbsp;")
    #// translators: xfn: http://gmpg.org/xfn
    _e("sweetheart")
    php_print("""           </label>
    </fieldset></td>
    </tr>
    </table>
    <p>""")
    _e("If the link is to a person, you can specify your relationship with them using the above form. If you would like to learn more about the idea check out <a href=\"http://gmpg.org/xfn/\">XFN</a>.")
    php_print("</p>\n   ")
# end def link_xfn_meta_box
#// 
#// Display advanced link options form fields.
#// 
#// @since 2.6.0
#// 
#// @param object $link
#//
def link_advanced_meta_box(link=None, *args_):
    
    php_print("<table class=\"links-table\" cellpadding=\"0\">\n    <tr>\n      <th scope=\"row\"><label for=\"link_image\">")
    _e("Image Address")
    php_print("</label></th>\n      <td><input type=\"text\" name=\"link_image\" class=\"code\" id=\"link_image\" maxlength=\"255\" value=\"")
    php_print(esc_attr(link.link_image) if (php_isset(lambda : link.link_image)) else "")
    php_print("""\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"rss_uri\">""")
    _e("RSS Address")
    php_print("</label></th>\n      <td><input name=\"link_rss\" class=\"code\" type=\"text\" id=\"rss_uri\" maxlength=\"255\" value=\"")
    php_print(esc_attr(link.link_rss) if (php_isset(lambda : link.link_rss)) else "")
    php_print("""\" /></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"link_notes\">""")
    _e("Notes")
    php_print("</label></th>\n      <td><textarea name=\"link_notes\" id=\"link_notes\" rows=\"10\">")
    php_print(link.link_notes if (php_isset(lambda : link.link_notes)) else "")
    pass
    php_print("""</textarea></td>
    </tr>
    <tr>
    <th scope=\"row\"><label for=\"link_rating\">""")
    _e("Rating")
    php_print("</label></th>\n      <td><select name=\"link_rating\" id=\"link_rating\" size=\"1\">\n       ")
    parsed_args = 0
    while parsed_args <= 10:
        
        php_print("<option value=\"" + parsed_args + "\"")
        if (php_isset(lambda : link.link_rating)) and link.link_rating == parsed_args:
            php_print(" selected=\"selected\"")
        # end if
        php_print(">" + parsed_args + "</option>")
        parsed_args += 1
    # end while
    php_print("     </select>&nbsp;")
    _e("(Leave at 0 for no rating.)")
    php_print("""       </td>
    </tr>
    </table>
    """)
# end def link_advanced_meta_box
#// 
#// Display post thumbnail meta box.
#// 
#// @since 2.9.0
#// 
#// @param WP_Post $post A post object.
#//
def post_thumbnail_meta_box(post=None, *args_):
    
    thumbnail_id = get_post_meta(post.ID, "_thumbnail_id", True)
    php_print(_wp_post_thumbnail_html(thumbnail_id, post.ID))
# end def post_thumbnail_meta_box
#// 
#// Display fields for ID3 data
#// 
#// @since 3.9.0
#// 
#// @param WP_Post $post A post object.
#//
def attachment_id3_data_meta_box(post=None, *args_):
    
    meta = Array()
    if (not php_empty(lambda : post.ID)):
        meta = wp_get_attachment_metadata(post.ID)
    # end if
    for key,label in wp_get_attachment_id3_keys(post, "edit"):
        value = ""
        if (not php_empty(lambda : meta[key])):
            value = meta[key]
        # end if
        php_print(" <p>\n       <label for=\"title\">")
        php_print(label)
        php_print("</label><br />\n     <input type=\"text\" name=\"id3_")
        php_print(esc_attr(key))
        php_print("\" id=\"id3_")
        php_print(esc_attr(key))
        php_print("\" class=\"large-text\" value=\"")
        php_print(esc_attr(value))
        php_print("\" />\n  </p>\n      ")
    # end for
# end def attachment_id3_data_meta_box
#// 
#// Registers the default post meta boxes, and runs the `do_meta_boxes` actions.
#// 
#// @since 5.0.0
#// 
#// @param WP_Post $post The post object that these meta boxes are being generated for.
#//
def register_and_do_post_meta_boxes(post=None, *args_):
    
    post_type = post.post_type
    post_type_object = get_post_type_object(post_type)
    thumbnail_support = current_theme_supports("post-thumbnails", post_type) and post_type_supports(post_type, "thumbnail")
    if (not thumbnail_support) and "attachment" == post_type and post.post_mime_type:
        if wp_attachment_is("audio", post):
            thumbnail_support = post_type_supports("attachment:audio", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:audio")
        elif wp_attachment_is("video", post):
            thumbnail_support = post_type_supports("attachment:video", "thumbnail") or current_theme_supports("post-thumbnails", "attachment:video")
        # end if
    # end if
    publish_callback_args = Array({"__back_compat_meta_box": True})
    if post_type_supports(post_type, "revisions") and "auto-draft" != post.post_status:
        revisions = wp_get_post_revisions(post.ID)
        #// We should aim to show the revisions meta box only when there are revisions.
        if php_count(revisions) > 1:
            reset(revisions)
            #// Reset pointer for key().
            publish_callback_args = Array({"revisions_count": php_count(revisions), "revision_id": key(revisions), "__back_compat_meta_box": True})
            add_meta_box("revisionsdiv", __("Revisions"), "post_revisions_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
        # end if
    # end if
    if "attachment" == post_type:
        wp_enqueue_script("image-edit")
        wp_enqueue_style("imgareaselect")
        add_meta_box("submitdiv", __("Save"), "attachment_submit_meta_box", None, "side", "core", Array({"__back_compat_meta_box": True}))
        add_action("edit_form_after_title", "edit_form_image_editor")
        if wp_attachment_is("audio", post):
            add_meta_box("attachment-id3", __("Metadata"), "attachment_id3_data_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
        # end if
    else:
        add_meta_box("submitdiv", __("Publish"), "post_submit_meta_box", None, "side", "core", publish_callback_args)
    # end if
    if current_theme_supports("post-formats") and post_type_supports(post_type, "post-formats"):
        add_meta_box("formatdiv", _x("Format", "post format"), "post_format_meta_box", None, "side", "core", Array({"__back_compat_meta_box": True}))
    # end if
    #// All taxonomies.
    for tax_name in get_object_taxonomies(post):
        taxonomy = get_taxonomy(tax_name)
        if (not taxonomy.show_ui) or False == taxonomy.meta_box_cb:
            continue
        # end if
        label = taxonomy.labels.name
        if (not is_taxonomy_hierarchical(tax_name)):
            tax_meta_box_id = "tagsdiv-" + tax_name
        else:
            tax_meta_box_id = tax_name + "div"
        # end if
        add_meta_box(tax_meta_box_id, label, taxonomy.meta_box_cb, None, "side", "core", Array({"taxonomy": tax_name, "__back_compat_meta_box": True}))
    # end for
    if post_type_supports(post_type, "page-attributes") or php_count(get_page_templates(post)) > 0:
        add_meta_box("pageparentdiv", post_type_object.labels.attributes, "page_attributes_meta_box", None, "side", "core", Array({"__back_compat_meta_box": True}))
    # end if
    if thumbnail_support and current_user_can("upload_files"):
        add_meta_box("postimagediv", esc_html(post_type_object.labels.featured_image), "post_thumbnail_meta_box", None, "side", "low", Array({"__back_compat_meta_box": True}))
    # end if
    if post_type_supports(post_type, "excerpt"):
        add_meta_box("postexcerpt", __("Excerpt"), "post_excerpt_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
    # end if
    if post_type_supports(post_type, "trackbacks"):
        add_meta_box("trackbacksdiv", __("Send Trackbacks"), "post_trackback_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
    # end if
    if post_type_supports(post_type, "custom-fields"):
        add_meta_box("postcustom", __("Custom Fields"), "post_custom_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": (not bool(get_user_meta(get_current_user_id(), "enable_custom_fields", True))), "__block_editor_compatible_meta_box": True}))
    # end if
    #// 
    #// Fires in the middle of built-in meta box registration.
    #// 
    #// @since 2.1.0
    #// @deprecated 3.7.0 Use {@see 'add_meta_boxes'} instead.
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action_deprecated("dbx_post_advanced", Array(post), "3.7.0", "add_meta_boxes")
    #// Allow the Discussion meta box to show up if the post type supports comments,
    #// or if comments or pings are open.
    if comments_open(post) or pings_open(post) or post_type_supports(post_type, "comments"):
        add_meta_box("commentstatusdiv", __("Discussion"), "post_comment_status_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
    # end if
    stati = get_post_stati(Array({"public": True}))
    if php_empty(lambda : stati):
        stati = Array("publish")
    # end if
    stati[-1] = "private"
    if php_in_array(get_post_status(post), stati):
        #// If the post type support comments, or the post has comments,
        #// allow the Comments meta box.
        if comments_open(post) or pings_open(post) or post.comment_count > 0 or post_type_supports(post_type, "comments"):
            add_meta_box("commentsdiv", __("Comments"), "post_comment_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
        # end if
    # end if
    if (not "pending" == get_post_status(post) and (not current_user_can(post_type_object.cap.publish_posts))):
        add_meta_box("slugdiv", __("Slug"), "post_slug_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
    # end if
    if post_type_supports(post_type, "author") and current_user_can(post_type_object.cap.edit_others_posts):
        add_meta_box("authordiv", __("Author"), "post_author_meta_box", None, "normal", "core", Array({"__back_compat_meta_box": True}))
    # end if
    #// 
    #// Fires after all built-in meta boxes have been added.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string  $post_type Post type.
    #// @param WP_Post $post      Post object.
    #//
    do_action("add_meta_boxes", post_type, post)
    #// 
    #// Fires after all built-in meta boxes have been added, contextually for the given post type.
    #// 
    #// The dynamic portion of the hook, `$post_type`, refers to the post type of the post.
    #// 
    #// @since 3.0.0
    #// 
    #// @param WP_Post $post Post object.
    #//
    do_action(str("add_meta_boxes_") + str(post_type), post)
    #// 
    #// Fires after meta boxes have been added.
    #// 
    #// Fires once for each of the default meta box contexts: normal, advanced, and side.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string                $post_type Post type of the post on Edit Post screen, 'link' on Edit Link screen,
    #// 'dashboard' on Dashboard screen.
    #// @param string                $context   Meta box context. Possible values include 'normal', 'advanced', 'side'.
    #// @param WP_Post|object|string $post      Post object on Edit Post screen, link object on Edit Link screen,
    #// an empty string on Dashboard screen.
    #//
    do_action("do_meta_boxes", post_type, "normal", post)
    #// This action is documented in wp-admin/includes/meta-boxes.php
    do_action("do_meta_boxes", post_type, "advanced", post)
    #// This action is documented in wp-admin/includes/meta-boxes.php
    do_action("do_meta_boxes", post_type, "side", post)
# end def register_and_do_post_meta_boxes