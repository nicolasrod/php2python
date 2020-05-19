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
#// WordPress Administration Privacy Tools API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Resend an existing request and return the result.
#// 
#// @since 4.9.6
#// @access private
#// 
#// @param int $request_id Request ID.
#// @return bool|WP_Error Returns true/false based on the success of sending the email, or a WP_Error object.
#//
def _wp_privacy_resend_request(request_id_=None, *_args_):
    
    
    request_id_ = absint(request_id_)
    request_ = get_post(request_id_)
    if (not request_) or "user_request" != request_.post_type:
        return php_new_class("WP_Error", lambda : WP_Error("privacy_request_error", __("Invalid request.")))
    # end if
    result_ = wp_send_user_request(request_id_)
    if is_wp_error(result_):
        return result_
    elif (not result_):
        return php_new_class("WP_Error", lambda : WP_Error("privacy_request_error", __("Unable to initiate confirmation request.")))
    # end if
    return True
# end def _wp_privacy_resend_request
#// 
#// Marks a request as completed by the admin and logs the current timestamp.
#// 
#// @since 4.9.6
#// @access private
#// 
#// @param  int          $request_id Request ID.
#// @return int|WP_Error $result     Request ID on success or WP_Error.
#//
def _wp_privacy_completed_request(request_id_=None, *_args_):
    
    
    #// Get the request.
    request_id_ = absint(request_id_)
    request_ = wp_get_user_request(request_id_)
    if (not request_):
        return php_new_class("WP_Error", lambda : WP_Error("privacy_request_error", __("Invalid request.")))
    # end if
    update_post_meta(request_id_, "_wp_user_request_completed_timestamp", time())
    result_ = wp_update_post(Array({"ID": request_id_, "post_status": "request-completed"}))
    return result_
# end def _wp_privacy_completed_request
#// 
#// Handle list table actions.
#// 
#// @since 4.9.6
#// @access private
#//
def _wp_personal_data_handle_actions(*_args_):
    
    
    if (php_isset(lambda : PHP_POST["privacy_action_email_retry"])):
        check_admin_referer("bulk-privacy_requests")
        request_id_ = absint(current(php_array_keys(wp_unslash(PHP_POST["privacy_action_email_retry"]))))
        result_ = _wp_privacy_resend_request(request_id_)
        if is_wp_error(result_):
            add_settings_error("privacy_action_email_retry", "privacy_action_email_retry", result_.get_error_message(), "error")
        else:
            add_settings_error("privacy_action_email_retry", "privacy_action_email_retry", __("Confirmation request sent again successfully."), "success")
        # end if
    elif (php_isset(lambda : PHP_POST["action"])):
        action_ = sanitize_key(wp_unslash(PHP_POST["action"])) if (not php_empty(lambda : PHP_POST["action"])) else ""
        for case in Switch(action_):
            if case("add_export_personal_data_request"):
                pass
            # end if
            if case("add_remove_personal_data_request"):
                check_admin_referer("personal-data-request")
                if (not (php_isset(lambda : PHP_POST["type_of_action"]) and php_isset(lambda : PHP_POST["username_or_email_for_privacy_request"]))):
                    add_settings_error("action_type", "action_type", __("Invalid action."), "error")
                # end if
                action_type_ = sanitize_text_field(wp_unslash(PHP_POST["type_of_action"]))
                username_or_email_address_ = sanitize_text_field(wp_unslash(PHP_POST["username_or_email_for_privacy_request"]))
                email_address_ = ""
                if (not php_in_array(action_type_, _wp_privacy_action_request_types(), True)):
                    add_settings_error("action_type", "action_type", __("Invalid action."), "error")
                # end if
                if (not is_email(username_or_email_address_)):
                    user_ = get_user_by("login", username_or_email_address_)
                    if (not type(user_).__name__ == "WP_User"):
                        add_settings_error("username_or_email_for_privacy_request", "username_or_email_for_privacy_request", __("Unable to add this request. A valid email address or username must be supplied."), "error")
                    else:
                        email_address_ = user_.user_email
                    # end if
                else:
                    email_address_ = username_or_email_address_
                # end if
                if php_empty(lambda : email_address_):
                    break
                # end if
                request_id_ = wp_create_user_request(email_address_, action_type_)
                if is_wp_error(request_id_):
                    add_settings_error("username_or_email_for_privacy_request", "username_or_email_for_privacy_request", request_id_.get_error_message(), "error")
                    break
                elif (not request_id_):
                    add_settings_error("username_or_email_for_privacy_request", "username_or_email_for_privacy_request", __("Unable to initiate confirmation request."), "error")
                    break
                # end if
                wp_send_user_request(request_id_)
                add_settings_error("username_or_email_for_privacy_request", "username_or_email_for_privacy_request", __("Confirmation request initiated successfully."), "success")
                break
            # end if
        # end for
    # end if
# end def _wp_personal_data_handle_actions
#// 
#// Cleans up failed and expired requests before displaying the list table.
#// 
#// @since 4.9.6
#// @access private
#//
def _wp_personal_data_cleanup_requests(*_args_):
    
    
    #// This filter is documented in wp-includes/user.php
    expires_ = php_int(apply_filters("user_request_key_expiration", DAY_IN_SECONDS))
    requests_query_ = php_new_class("WP_Query", lambda : WP_Query(Array({"post_type": "user_request", "posts_per_page": -1, "post_status": "request-pending", "fields": "ids", "date_query": Array(Array({"column": "post_modified_gmt", "before": expires_ + " seconds ago"}))})))
    request_ids_ = requests_query_.posts
    for request_id_ in request_ids_:
        wp_update_post(Array({"ID": request_id_, "post_status": "request-failed", "post_password": ""}))
    # end for
# end def _wp_personal_data_cleanup_requests
#// 
#// Generate a single group for the personal data export report.
#// 
#// @since 4.9.6
#// @since 5.4.0 Added the `$group_id` and `$groups_count` parameters.
#// 
#// @param array $group_data {
#// The group data to render.
#// 
#// @type string $group_label  The user-facing heading for the group, e.g. 'Comments'.
#// @type array  $items        {
#// An array of group items.
#// 
#// @type array  $group_item_data  {
#// An array of name-value pairs for the item.
#// 
#// @type string $name   The user-facing name of an item name-value pair, e.g. 'IP Address'.
#// @type string $value  The user-facing value of an item data pair, e.g. '50.60.70.0'.
#// }
#// }
#// }
#// @param string  $group_id     The group identifier.
#// @param int     $groups_count The number of all groups
#// @return string $group_html   The HTML for this group and its items.
#//
def wp_privacy_generate_personal_data_export_group_html(group_data_=None, group_id_="", groups_count_=1, *_args_):
    
    
    group_id_attr_ = sanitize_title_with_dashes(group_data_["group_label"] + "-" + group_id_)
    group_html_ = "<h2 id=\"" + esc_attr(group_id_attr_) + "\">"
    group_html_ += esc_html(group_data_["group_label"])
    items_count_ = php_count(group_data_["items"])
    if items_count_ > 1:
        group_html_ += php_sprintf(" <span class=\"count\">(%d)</span>", items_count_)
    # end if
    group_html_ += "</h2>"
    if (not php_empty(lambda : group_data_["group_description"])):
        group_html_ += "<p>" + esc_html(group_data_["group_description"]) + "</p>"
    # end if
    group_html_ += "<div>"
    for group_item_id_,group_item_data_ in group_data_["items"].items():
        group_html_ += "<table>"
        group_html_ += "<tbody>"
        for group_item_datum_ in group_item_data_:
            value_ = group_item_datum_["value"]
            #// If it looks like a link, make it a link.
            if False == php_strpos(value_, " ") and 0 == php_strpos(value_, "http://") or 0 == php_strpos(value_, "https://"):
                value_ = "<a href=\"" + esc_url(value_) + "\">" + esc_html(value_) + "</a>"
            # end if
            group_html_ += "<tr>"
            group_html_ += "<th>" + esc_html(group_item_datum_["name"]) + "</th>"
            group_html_ += "<td>" + wp_kses(value_, "personal_data_export") + "</td>"
            group_html_ += "</tr>"
        # end for
        group_html_ += "</tbody>"
        group_html_ += "</table>"
    # end for
    if 1 < groups_count_:
        group_html_ += "<div class=\"return_to_top\">"
        group_html_ += "<a href=\"#top\">" + esc_html__("&uarr; Return to top") + "</a>"
        group_html_ += "</div>"
    # end if
    group_html_ += "</div>"
    return group_html_
# end def wp_privacy_generate_personal_data_export_group_html
#// 
#// Generate the personal data export file.
#// 
#// @since 4.9.6
#// 
#// @param int $request_id The export request ID.
#//
def wp_privacy_generate_personal_data_export_file(request_id_=None, *_args_):
    
    
    if (not php_class_exists("ZipArchive")):
        wp_send_json_error(__("Unable to generate export file. ZipArchive not available."))
    # end if
    #// Get the request.
    request_ = wp_get_user_request(request_id_)
    if (not request_) or "export_personal_data" != request_.action_name:
        wp_send_json_error(__("Invalid request ID when generating export file."))
    # end if
    email_address_ = request_.email
    if (not is_email(email_address_)):
        wp_send_json_error(__("Invalid email address when generating export file."))
    # end if
    #// Create the exports folder if needed.
    exports_dir_ = wp_privacy_exports_dir()
    exports_url_ = wp_privacy_exports_url()
    if (not wp_mkdir_p(exports_dir_)):
        wp_send_json_error(__("Unable to create export folder."))
    # end if
    #// Protect export folder from browsing.
    index_pathname_ = exports_dir_ + "index.html"
    if (not php_file_exists(index_pathname_)):
        file_ = fopen(index_pathname_, "w")
        if False == file_:
            wp_send_json_error(__("Unable to protect export folder from browsing."))
        # end if
        fwrite(file_, "<!-- Silence is golden. -->")
        php_fclose(file_)
    # end if
    obscura_ = wp_generate_password(32, False, False)
    file_basename_ = "wp-personal-data-file-" + obscura_
    html_report_filename_ = wp_unique_filename(exports_dir_, file_basename_ + ".html")
    html_report_pathname_ = wp_normalize_path(exports_dir_ + html_report_filename_)
    json_report_filename_ = file_basename_ + ".json"
    json_report_pathname_ = wp_normalize_path(exports_dir_ + json_report_filename_)
    #// 
    #// Gather general data needed.
    #// 
    #// Title.
    title_ = php_sprintf(__("Personal Data Export for %s"), email_address_)
    #// And now, all the Groups.
    groups_ = get_post_meta(request_id_, "_export_data_grouped", True)
    #// First, build an "About" group on the fly for this report.
    about_group_ = Array({"group_label": _x("About", "personal data group label"), "group_description": _x("Overview of export report.", "personal data group description"), "items": Array({"about-1": Array(Array({"name": _x("Report generated for", "email address"), "value": email_address_}), Array({"name": _x("For site", "website name"), "value": get_bloginfo("name")}), Array({"name": _x("At URL", "website URL"), "value": get_bloginfo("url")}), Array({"name": _x("On", "date/time"), "value": current_time("mysql")}))})})
    #// Merge in the special about group.
    groups_ = php_array_merge(Array({"about": about_group_}), groups_)
    groups_count_ = php_count(groups_)
    #// Convert the groups to JSON format.
    groups_json_ = wp_json_encode(groups_)
    #// 
    #// Handle the JSON export.
    #//
    file_ = fopen(json_report_pathname_, "w")
    if False == file_:
        wp_send_json_error(__("Unable to open export file (JSON report) for writing."))
    # end if
    fwrite(file_, "{")
    fwrite(file_, "\"" + title_ + "\":")
    fwrite(file_, groups_json_)
    fwrite(file_, "}")
    php_fclose(file_)
    #// 
    #// Handle the HTML export.
    #//
    file_ = fopen(html_report_pathname_, "w")
    if False == file_:
        wp_send_json_error(__("Unable to open export file (HTML report) for writing."))
    # end if
    fwrite(file_, "<!DOCTYPE html>\n")
    fwrite(file_, "<html>\n")
    fwrite(file_, "<head>\n")
    fwrite(file_, "<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />\n")
    fwrite(file_, "<style type='text/css'>")
    fwrite(file_, "body { color: black; font-family: Arial, sans-serif; font-size: 11pt; margin: 15px auto; width: 860px; }")
    fwrite(file_, "table { background: #f0f0f0; border: 1px solid #ddd; margin-bottom: 20px; width: 100%; }")
    fwrite(file_, "th { padding: 5px; text-align: left; width: 20%; }")
    fwrite(file_, "td { padding: 5px; }")
    fwrite(file_, "tr:nth-child(odd) { background-color: #fafafa; }")
    fwrite(file_, ".return_to_top { text-align:right; }")
    fwrite(file_, "</style>")
    fwrite(file_, "<title>")
    fwrite(file_, esc_html(title_))
    fwrite(file_, "</title>")
    fwrite(file_, "</head>\n")
    fwrite(file_, "<body>\n")
    fwrite(file_, "<h1 id=\"top\">" + esc_html__("Personal Data Export") + "</h1>")
    #// Create TOC.
    if 1 < groups_count_:
        fwrite(file_, "<div id=\"table_of_contents\">")
        fwrite(file_, "<h2>" + esc_html__("Table of Contents") + "</h2>")
        fwrite(file_, "<ul>")
        for group_id_,group_data_ in groups_.items():
            group_label_ = esc_html(group_data_["group_label"])
            group_id_attr_ = sanitize_title_with_dashes(group_data_["group_label"] + "-" + group_id_)
            group_items_count_ = php_count(group_data_["items"])
            if group_items_count_ > 1:
                group_label_ += php_sprintf(" <span class=\"count\">(%d)</span>", group_items_count_)
            # end if
            fwrite(file_, "<li>")
            fwrite(file_, "<a href=\"#" + esc_attr(group_id_attr_) + "\">" + group_label_ + "</a>")
            fwrite(file_, "</li>")
        # end for
        fwrite(file_, "</ul>")
        fwrite(file_, "</div>")
    # end if
    #// Now, iterate over every group in $groups and have the formatter render it in HTML.
    for group_id_,group_data_ in groups_.items():
        fwrite(file_, wp_privacy_generate_personal_data_export_group_html(group_data_, group_id_, groups_count_))
    # end for
    fwrite(file_, "</body>\n")
    fwrite(file_, "</html>\n")
    php_fclose(file_)
    #// 
    #// Now, generate the ZIP.
    #// 
    #// If an archive has already been generated, then remove it and reuse the
    #// filename, to avoid breaking any URLs that may have been previously sent
    #// via email.
    #//
    error_ = False
    archive_url_ = get_post_meta(request_id_, "_export_file_url", True)
    archive_pathname_ = get_post_meta(request_id_, "_export_file_path", True)
    if php_empty(lambda : archive_pathname_) or php_empty(lambda : archive_url_):
        archive_filename_ = file_basename_ + ".zip"
        archive_pathname_ = exports_dir_ + archive_filename_
        archive_url_ = exports_url_ + archive_filename_
        update_post_meta(request_id_, "_export_file_url", archive_url_)
        update_post_meta(request_id_, "_export_file_path", wp_normalize_path(archive_pathname_))
    # end if
    if (not php_empty(lambda : archive_pathname_)) and php_file_exists(archive_pathname_):
        wp_delete_file(archive_pathname_)
    # end if
    zip_ = php_new_class("ZipArchive", lambda : ZipArchive())
    if True == zip_.open(archive_pathname_, ZipArchive.CREATE):
        if (not zip_.addfile(json_report_pathname_, "export.json")):
            error_ = __("Unable to add data to JSON file.")
        # end if
        if (not zip_.addfile(html_report_pathname_, "index.html")):
            error_ = __("Unable to add data to HTML file.")
        # end if
        zip_.close()
        if (not error_):
            #// 
            #// Fires right after all personal data has been written to the export file.
            #// 
            #// @since 4.9.6
            #// @since 5.4.0 Added the `$json_report_pathname` parameter.
            #// 
            #// @param string $archive_pathname     The full path to the export file on the filesystem.
            #// @param string $archive_url          The URL of the archive file.
            #// @param string $html_report_pathname The full path to the HTML personal data report on the filesystem.
            #// @param int    $request_id           The export request ID.
            #// @param string $json_report_pathname The full path to the JSON personal data report on the filesystem.
            #//
            do_action("wp_privacy_personal_data_export_file_created", archive_pathname_, archive_url_, html_report_pathname_, request_id_, json_report_pathname_)
        # end if
    else:
        error_ = __("Unable to open export file (archive) for writing.")
    # end if
    #// Remove the JSON file.
    unlink(json_report_pathname_)
    #// Remove the HTML file.
    unlink(html_report_pathname_)
    if error_:
        wp_send_json_error(error_)
    # end if
# end def wp_privacy_generate_personal_data_export_file
#// 
#// Send an email to the user with a link to the personal data export file
#// 
#// @since 4.9.6
#// 
#// @param int $request_id The request ID for this personal data export.
#// @return true|WP_Error True on success or `WP_Error` on failure.
#//
def wp_privacy_send_personal_data_export_email(request_id_=None, *_args_):
    
    
    #// Get the request.
    request_ = wp_get_user_request(request_id_)
    if (not request_) or "export_personal_data" != request_.action_name:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_request", __("Invalid request ID when sending personal data export email.")))
    # end if
    #// Localize message content for user; fallback to site default for visitors.
    if (not php_empty(lambda : request_.user_id)):
        locale_ = get_user_locale(request_.user_id)
    else:
        locale_ = get_locale()
    # end if
    switched_locale_ = switch_to_locale(locale_)
    #// This filter is documented in wp-includes/functions.php
    expiration_ = apply_filters("wp_privacy_export_expiration", 3 * DAY_IN_SECONDS)
    expiration_date_ = date_i18n(get_option("date_format"), time() + expiration_)
    export_file_url_ = get_post_meta(request_id_, "_export_file_url", True)
    site_name_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
    site_url_ = home_url()
    #// 
    #// Filters the recipient of the personal data export email notification.
    #// Should be used with great caution to avoid sending the data export link to wrong emails.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string          $request_email The email address of the notification recipient.
    #// @param WP_User_Request $request       The request that is initiating the notification.
    #//
    request_email_ = apply_filters("wp_privacy_personal_data_email_to", request_.email, request_)
    email_data_ = Array({"request": request_, "expiration": expiration_, "expiration_date": expiration_date_, "message_recipient": request_email_, "export_file_url": export_file_url_, "sitename": site_name_, "siteurl": site_url_})
    #// translators: Personal data export notification email subject. %s: Site title.
    subject_ = php_sprintf(__("[%s] Personal Data Export"), site_name_)
    #// 
    #// Filters the subject of the email sent when an export request is completed.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $subject    The email subject.
    #// @param string $sitename   The name of the site.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request           User request object.
    #// @type int             $expiration        The time in seconds until the export file expires.
    #// @type string          $expiration_date   The localized date and time when the export file expires.
    #// @type string          $message_recipient The address that the email will be sent to. Defaults
    #// to the value of `$request->email`, but can be changed
    #// by the `wp_privacy_personal_data_email_to` filter.
    #// @type string          $export_file_url   The export file URL.
    #// @type string          $sitename          The site name sending the mail.
    #// @type string          $siteurl           The site URL sending the mail.
    #// }
    #//
    subject_ = apply_filters("wp_privacy_personal_data_email_subject", subject_, site_name_, email_data_)
    #// translators: Do not translate EXPIRATION, LINK, SITENAME, SITEURL: those are placeholders.
    email_text_ = __("""Howdy,
    Your request for an export of personal data has been completed. You may
    download your personal data by clicking on the link below. For privacy
    and security, we will automatically delete the file on ###EXPIRATION###,
    so please download it before then.
    ###LINK###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    #// 
    #// Filters the text of the email sent with a personal data export file.
    #// 
    #// The following strings have a special meaning and will get replaced dynamically:
    #// ###EXPIRATION###         The date when the URL will be automatically deleted.
    #// ###LINK###               URL of the personal data export file for the user.
    #// ###SITENAME###           The name of the site.
    #// ###SITEURL###            The URL to the site.
    #// 
    #// @since 4.9.6
    #// @since 5.3.0 Introduced the `$email_data` array.
    #// 
    #// @param string $email_text Text in the email.
    #// @param int    $request_id The request ID for this personal data export.
    #// @param array  $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request           User request object.
    #// @type int             $expiration        The time in seconds until the export file expires.
    #// @type string          $expiration_date   The localized date and time when the export file expires.
    #// @type string          $message_recipient The address that the email will be sent to. Defaults
    #// to the value of `$request->email`, but can be changed
    #// by the `wp_privacy_personal_data_email_to` filter.
    #// @type string          $export_file_url   The export file URL.
    #// @type string          $sitename          The site name sending the mail.
    #// @type string          $siteurl           The site URL sending the mail.
    #//
    content_ = apply_filters("wp_privacy_personal_data_email_content", email_text_, request_id_, email_data_)
    content_ = php_str_replace("###EXPIRATION###", expiration_date_, content_)
    content_ = php_str_replace("###LINK###", esc_url_raw(export_file_url_), content_)
    content_ = php_str_replace("###EMAIL###", request_email_, content_)
    content_ = php_str_replace("###SITENAME###", site_name_, content_)
    content_ = php_str_replace("###SITEURL###", esc_url_raw(site_url_), content_)
    headers_ = ""
    #// 
    #// Filters the headers of the email sent with a personal data export file.
    #// 
    #// @since 5.4.0
    #// 
    #// @param string|array $headers    The email headers.
    #// @param string       $subject    The email subject.
    #// @param string       $content    The email content.
    #// @param int          $request_id The request ID.
    #// @param array        $email_data {
    #// Data relating to the account action email.
    #// 
    #// @type WP_User_Request $request           User request object.
    #// @type int             $expiration        The time in seconds until the export file expires.
    #// @type string          $expiration_date   The localized date and time when the export file expires.
    #// @type string          $message_recipient The address that the email will be sent to. Defaults
    #// to the value of `$request->email`, but can be changed
    #// by the `wp_privacy_personal_data_email_to` filter.
    #// @type string          $export_file_url   The export file URL.
    #// @type string          $sitename          The site name sending the mail.
    #// @type string          $siteurl           The site URL sending the mail.
    #// }
    #//
    headers_ = apply_filters("wp_privacy_personal_data_email_headers", headers_, subject_, content_, request_id_, email_data_)
    mail_success_ = wp_mail(request_email_, subject_, content_, headers_)
    if switched_locale_:
        restore_previous_locale()
    # end if
    if (not mail_success_):
        return php_new_class("WP_Error", lambda : WP_Error("privacy_email_error", __("Unable to send personal data export email.")))
    # end if
    return True
# end def wp_privacy_send_personal_data_export_email
#// 
#// Intercept personal data exporter page Ajax responses in order to assemble the personal data export file.
#// @see wp_privacy_personal_data_export_page
#// @since 4.9.6
#// 
#// @param array  $response        The response from the personal data exporter for the given page.
#// @param int    $exporter_index  The index of the personal data exporter. Begins at 1.
#// @param string $email_address   The email address of the user whose personal data this is.
#// @param int    $page            The page of personal data for this exporter. Begins at 1.
#// @param int    $request_id      The request ID for this personal data export.
#// @param bool   $send_as_email   Whether the final results of the export should be emailed to the user.
#// @param string $exporter_key    The slug (key) of the exporter.
#// @return array The filtered response.
#//
def wp_privacy_process_personal_data_export_page(response_=None, exporter_index_=None, email_address_=None, page_=None, request_id_=None, send_as_email_=None, exporter_key_=None, *_args_):
    
    
    #// Do some simple checks on the shape of the response from the exporter.
    #// If the exporter response is malformed, don't attempt to consume it - let it
    #// pass through to generate a warning to the user by default Ajax processing.
    #//
    if (not php_is_array(response_)):
        return response_
    # end if
    if (not php_array_key_exists("done", response_)):
        return response_
    # end if
    if (not php_array_key_exists("data", response_)):
        return response_
    # end if
    if (not php_is_array(response_["data"])):
        return response_
    # end if
    #// Get the request.
    request_ = wp_get_user_request(request_id_)
    if (not request_) or "export_personal_data" != request_.action_name:
        wp_send_json_error(__("Invalid request ID when merging exporter data."))
    # end if
    export_data_ = Array()
    #// First exporter, first page? Reset the report data accumulation array.
    if 1 == exporter_index_ and 1 == page_:
        update_post_meta(request_id_, "_export_data_raw", export_data_)
    else:
        export_data_ = get_post_meta(request_id_, "_export_data_raw", True)
    # end if
    #// Now, merge the data from the exporter response into the data we have accumulated already.
    export_data_ = php_array_merge(export_data_, response_["data"])
    update_post_meta(request_id_, "_export_data_raw", export_data_)
    #// If we are not yet on the last page of the last exporter, return now.
    #// This filter is documented in wp-admin/includes/ajax-actions.php
    exporters_ = apply_filters("wp_privacy_personal_data_exporters", Array())
    is_last_exporter_ = php_count(exporters_) == exporter_index_
    exporter_done_ = response_["done"]
    if (not is_last_exporter_) or (not exporter_done_):
        return response_
    # end if
    #// Last exporter, last page - let's prepare the export file.
    #// First we need to re-organize the raw data hierarchically in groups and items.
    groups_ = Array()
    for export_datum_ in export_data_:
        group_id_ = export_datum_["group_id"]
        group_label_ = export_datum_["group_label"]
        group_description_ = ""
        if (not php_empty(lambda : export_datum_["group_description"])):
            group_description_ = export_datum_["group_description"]
        # end if
        if (not php_array_key_exists(group_id_, groups_)):
            groups_[group_id_] = Array({"group_label": group_label_, "group_description": group_description_, "items": Array()})
        # end if
        item_id_ = export_datum_["item_id"]
        if (not php_array_key_exists(item_id_, groups_[group_id_]["items"])):
            groups_[group_id_]["items"][item_id_] = Array()
        # end if
        old_item_data_ = groups_[group_id_]["items"][item_id_]
        merged_item_data_ = php_array_merge(export_datum_["data"], old_item_data_)
        groups_[group_id_]["items"][item_id_] = merged_item_data_
    # end for
    #// Then save the grouped data into the request.
    delete_post_meta(request_id_, "_export_data_raw")
    update_post_meta(request_id_, "_export_data_grouped", groups_)
    #// 
    #// Generate the export file from the collected, grouped personal data.
    #// 
    #// @since 4.9.6
    #// 
    #// @param int $request_id The export request ID.
    #//
    do_action("wp_privacy_personal_data_export_file", request_id_)
    #// Clear the grouped data now that it is no longer needed.
    delete_post_meta(request_id_, "_export_data_grouped")
    #// If the destination is email, send it now.
    if send_as_email_:
        mail_success_ = wp_privacy_send_personal_data_export_email(request_id_)
        if is_wp_error(mail_success_):
            wp_send_json_error(mail_success_.get_error_message())
        # end if
        #// Update the request to completed state when the export email is sent.
        _wp_privacy_completed_request(request_id_)
    else:
        #// Modify the response to include the URL of the export file so the browser can fetch it.
        export_file_url_ = get_post_meta(request_id_, "_export_file_url", True)
        if (not php_empty(lambda : export_file_url_)):
            response_["url"] = export_file_url_
        # end if
    # end if
    return response_
# end def wp_privacy_process_personal_data_export_page
#// 
#// Mark erasure requests as completed after processing is finished.
#// 
#// This intercepts the Ajax responses to personal data eraser page requests, and
#// monitors the status of a request. Once all of the processing has finished, the
#// request is marked as completed.
#// 
#// @since 4.9.6
#// 
#// @see wp_privacy_personal_data_erasure_page
#// 
#// @param array  $response      The response from the personal data eraser for
#// the given page.
#// @param int    $eraser_index  The index of the personal data eraser. Begins
#// at 1.
#// @param string $email_address The email address of the user whose personal
#// data this is.
#// @param int    $page          The page of personal data for this eraser.
#// Begins at 1.
#// @param int    $request_id    The request ID for this personal data erasure.
#// @return array The filtered response.
#//
def wp_privacy_process_personal_data_erasure_page(response_=None, eraser_index_=None, email_address_=None, page_=None, request_id_=None, *_args_):
    
    
    #// 
    #// If the eraser response is malformed, don't attempt to consume it; let it
    #// pass through, so that the default Ajax processing will generate a warning
    #// to the user.
    #//
    if (not php_is_array(response_)):
        return response_
    # end if
    if (not php_array_key_exists("done", response_)):
        return response_
    # end if
    if (not php_array_key_exists("items_removed", response_)):
        return response_
    # end if
    if (not php_array_key_exists("items_retained", response_)):
        return response_
    # end if
    if (not php_array_key_exists("messages", response_)):
        return response_
    # end if
    #// Get the request.
    request_ = wp_get_user_request(request_id_)
    if (not request_) or "remove_personal_data" != request_.action_name:
        wp_send_json_error(__("Invalid request ID when processing eraser data."))
    # end if
    #// This filter is documented in wp-admin/includes/ajax-actions.php
    erasers_ = apply_filters("wp_privacy_personal_data_erasers", Array())
    is_last_eraser_ = php_count(erasers_) == eraser_index_
    eraser_done_ = response_["done"]
    if (not is_last_eraser_) or (not eraser_done_):
        return response_
    # end if
    _wp_privacy_completed_request(request_id_)
    #// 
    #// Fires immediately after a personal data erasure request has been marked completed.
    #// 
    #// @since 4.9.6
    #// 
    #// @param int $request_id The privacy request post ID associated with this request.
    #//
    do_action("wp_privacy_personal_data_erased", request_id_)
    return response_
# end def wp_privacy_process_personal_data_erasure_page
