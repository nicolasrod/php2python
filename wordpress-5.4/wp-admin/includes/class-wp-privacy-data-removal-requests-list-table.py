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
#// List Table API: WP_Privacy_Data_Removal_Requests_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.9.6
#//
if (not php_class_exists("WP_Privacy_Requests_Table")):
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-requests-table.php", once=True)
# end if
#// 
#// WP_Privacy_Data_Removal_Requests_List_Table class.
#// 
#// @since 4.9.6
#//
class WP_Privacy_Data_Removal_Requests_List_Table(WP_Privacy_Requests_Table):
    request_type = "remove_personal_data"
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
        
        row_actions = Array()
        #// Allow the administrator to "force remove" the personal data even if confirmation has not yet been received.
        status = item.status
        if "request-confirmed" != status:
            #// This filter is documented in wp-admin/includes/ajax-actions.php
            erasers = apply_filters("wp_privacy_personal_data_erasers", Array())
            erasers_count = php_count(erasers)
            request_id = item.ID
            nonce = wp_create_nonce("wp-privacy-erase-personal-data-" + request_id)
            remove_data_markup = "<div class=\"remove-personal-data force-remove-personal-data\" " + "data-erasers-count=\"" + esc_attr(erasers_count) + "\" " + "data-request-id=\"" + esc_attr(request_id) + "\" " + "data-nonce=\"" + esc_attr(nonce) + "\">"
            remove_data_markup += "<span class=\"remove-personal-data-idle\"><button type=\"button\" class=\"button-link remove-personal-data-handle\">" + __("Force Erase Personal Data") + "</button></span>" + "<span class=\"remove-personal-data-processing hidden\">" + __("Erasing Data...") + " <span class=\"erasure-progress\"></span></span>" + "<span class=\"remove-personal-data-success hidden\">" + __("Erasure completed.") + "</span>" + "<span class=\"remove-personal-data-failed hidden\">" + __("Force Erasure has failed.") + " <button type=\"button\" class=\"button-link remove-personal-data-handle\">" + __("Retry") + "</button></span>"
            remove_data_markup += "</div>"
            row_actions = Array({"remove-data": remove_data_markup})
        # end if
        return php_sprintf("<a href=\"%1$s\">%2$s</a> %3$s", esc_url("mailto:" + item.email), item.email, self.row_actions(row_actions))
    # end def column_email
    #// 
    #// Next steps column.
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
                erasers = apply_filters("wp_privacy_personal_data_erasers", Array())
                erasers_count = php_count(erasers)
                request_id = item.ID
                nonce = wp_create_nonce("wp-privacy-erase-personal-data-" + request_id)
                php_print("<div class=\"remove-personal-data\" " + "data-force-erase=\"1\" " + "data-erasers-count=\"" + esc_attr(erasers_count) + "\" " + "data-request-id=\"" + esc_attr(request_id) + "\" " + "data-nonce=\"" + esc_attr(nonce) + "\">")
                php_print("             <span class=\"remove-personal-data-idle\"><button type=\"button\" class=\"button-link remove-personal-data-handle\">")
                _e("Erase Personal Data")
                php_print("</button></span>\n               <span class=\"remove-personal-data-processing hidden\">")
                _e("Erasing Data...")
                php_print(" <span class=\"erasure-progress\"></span></span>\n               <span class=\"remove-personal-data-success success-message hidden\" >")
                _e("Erasure completed.")
                php_print("</span>\n                <span class=\"remove-personal-data-failed hidden\">")
                _e("Data Erasure has failed.")
                php_print(" <button type=\"button\" class=\"button-link remove-personal-data-handle\">")
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
                php_print("<a href=\"" + esc_url(wp_nonce_url(add_query_arg(Array({"action": "delete", "request_id": Array(item.ID)}), admin_url("erase-personal-data.php")), "bulk-privacy_requests")) + "\">" + esc_html__("Remove request") + "</a>")
                break
            # end if
        # end for
    # end def column_next_steps
# end class WP_Privacy_Data_Removal_Requests_List_Table
