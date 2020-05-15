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
#// List Table API: WP_Privacy_Data_Export_Requests_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.9.6
#//
if (not php_class_exists("WP_Privacy_Requests_Table")):
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-requests-table.php", once=True)
# end if
#// 
#// WP_Privacy_Data_Export_Requests_Table class.
#// 
#// @since 4.9.6
#//
class WP_Privacy_Data_Export_Requests_List_Table(WP_Privacy_Requests_Table):
    request_type = "export_personal_data"
    post_type = "user_request"
    #// 
    #// Actions column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Email column markup.
    #//
    def column_email(self, item=None):
        
        #// This filter is documented in wp-admin/includes/ajax-actions.php
        exporters = apply_filters("wp_privacy_personal_data_exporters", Array())
        exporters_count = php_count(exporters)
        request_id = item.ID
        nonce = wp_create_nonce("wp-privacy-export-personal-data-" + request_id)
        download_data_markup = "<div class=\"export-personal-data\" " + "data-exporters-count=\"" + esc_attr(exporters_count) + "\" " + "data-request-id=\"" + esc_attr(request_id) + "\" " + "data-nonce=\"" + esc_attr(nonce) + "\">"
        download_data_markup += "<span class=\"export-personal-data-idle\"><button type=\"button\" class=\"button-link export-personal-data-handle\">" + __("Download Personal Data") + "</button></span>" + "<span class=\"export-personal-data-processing hidden\">" + __("Downloading Data...") + " <span class=\"export-progress\"></span></span>" + "<span class=\"export-personal-data-success hidden\"><button type=\"button\" class=\"button-link export-personal-data-handle\">" + __("Download Personal Data Again") + "</button></span>" + "<span class=\"export-personal-data-failed hidden\">" + __("Download failed.") + " <button type=\"button\" class=\"button-link\">" + __("Retry") + "</button></span>"
        download_data_markup += "</div>"
        row_actions = Array({"download-data": download_data_markup})
        return php_sprintf("<a href=\"%1$s\">%2$s</a> %3$s", esc_url("mailto:" + item.email), item.email, self.row_actions(row_actions))
    # end def column_email
    #// 
    #// Displays the next steps column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #//
    def column_next_steps(self, item=None):
        
        status = item.status
        for case in Switch(status):
            if case("request-pending"):
                esc_html_e("Waiting for confirmation")
                break
            # end if
            if case("request-confirmed"):
                #// This filter is documented in wp-admin/includes/ajax-actions.php
                exporters = apply_filters("wp_privacy_personal_data_exporters", Array())
                exporters_count = php_count(exporters)
                request_id = item.ID
                nonce = wp_create_nonce("wp-privacy-export-personal-data-" + request_id)
                php_print("<div class=\"export-personal-data\" " + "data-send-as-email=\"1\" " + "data-exporters-count=\"" + esc_attr(exporters_count) + "\" " + "data-request-id=\"" + esc_attr(request_id) + "\" " + "data-nonce=\"" + esc_attr(nonce) + "\">")
                php_print("             <span class=\"export-personal-data-idle\"><button type=\"button\" class=\"button-link export-personal-data-handle\">")
                _e("Send Export Link")
                php_print("</button></span>\n               <span class=\"export-personal-data-processing hidden\">")
                _e("Sending Email...")
                php_print(" <span class=\"export-progress\"></span></span>\n                <span class=\"export-personal-data-success success-message hidden\">")
                _e("Email sent.")
                php_print("</span>\n                <span class=\"export-personal-data-failed hidden\">")
                _e("Email could not be sent.")
                php_print(" <button type=\"button\" class=\"button-link export-personal-data-handle\">")
                _e("Retry")
                php_print("</button></span>\n               ")
                php_print("</div>")
                break
            # end if
            if case("request-failed"):
                php_print("<button type=\"submit\" class=\"button-link\" name=\"privacy_action_email_retry[" + item.ID + "]\" id=\"privacy_action_email_retry[" + item.ID + "]\">" + __("Retry") + "</button>")
                break
            # end if
            if case("request-completed"):
                php_print("<a href=\"" + esc_url(wp_nonce_url(add_query_arg(Array({"action": "delete", "request_id": Array(item.ID)}), admin_url("export-personal-data.php")), "bulk-privacy_requests")) + "\">" + esc_html__("Remove request") + "</a>")
                break
            # end if
        # end for
    # end def column_next_steps
# end class WP_Privacy_Data_Export_Requests_List_Table
