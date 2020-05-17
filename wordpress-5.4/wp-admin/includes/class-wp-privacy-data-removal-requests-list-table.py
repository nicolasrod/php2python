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
    #// 
    #// Action name for the requests this table will work with.
    #// 
    #// @since 4.9.6
    #// 
    #// @var string $request_type Name of action.
    #//
    request_type = "remove_personal_data"
    #// 
    #// Post type for the requests.
    #// 
    #// @since 4.9.6
    #// 
    #// @var string $post_type The post type.
    #//
    post_type = "user_request"
    #// 
    #// Actions column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Email column markup.
    #//
    def column_email(self, item_=None):
        
        
        row_actions_ = Array()
        #// Allow the administrator to "force remove" the personal data even if confirmation has not yet been received.
        status_ = item_.status
        if "request-confirmed" != status_:
            #// This filter is documented in wp-admin/includes/ajax-actions.php
            erasers_ = apply_filters("wp_privacy_personal_data_erasers", Array())
            erasers_count_ = php_count(erasers_)
            request_id_ = item_.ID
            nonce_ = wp_create_nonce("wp-privacy-erase-personal-data-" + request_id_)
            remove_data_markup_ = "<div class=\"remove-personal-data force-remove-personal-data\" " + "data-erasers-count=\"" + esc_attr(erasers_count_) + "\" " + "data-request-id=\"" + esc_attr(request_id_) + "\" " + "data-nonce=\"" + esc_attr(nonce_) + "\">"
            remove_data_markup_ += "<span class=\"remove-personal-data-idle\"><button type=\"button\" class=\"button-link remove-personal-data-handle\">" + __("Force Erase Personal Data") + "</button></span>" + "<span class=\"remove-personal-data-processing hidden\">" + __("Erasing Data...") + " <span class=\"erasure-progress\"></span></span>" + "<span class=\"remove-personal-data-success hidden\">" + __("Erasure completed.") + "</span>" + "<span class=\"remove-personal-data-failed hidden\">" + __("Force Erasure has failed.") + " <button type=\"button\" class=\"button-link remove-personal-data-handle\">" + __("Retry") + "</button></span>"
            remove_data_markup_ += "</div>"
            row_actions_ = Array({"remove-data": remove_data_markup_})
        # end if
        return php_sprintf("<a href=\"%1$s\">%2$s</a> %3$s", esc_url("mailto:" + item_.email), item_.email, self.row_actions(row_actions_))
    # end def column_email
    #// 
    #// Next steps column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #//
    def column_next_steps(self, item_=None):
        
        
        status_ = item_.status
        for case in Switch(status_):
            if case("request-pending"):
                esc_html_e("Waiting for confirmation")
                break
            # end if
            if case("request-confirmed"):
                #// This filter is documented in wp-admin/includes/ajax-actions.php
                erasers_ = apply_filters("wp_privacy_personal_data_erasers", Array())
                erasers_count_ = php_count(erasers_)
                request_id_ = item_.ID
                nonce_ = wp_create_nonce("wp-privacy-erase-personal-data-" + request_id_)
                php_print("<div class=\"remove-personal-data\" " + "data-force-erase=\"1\" " + "data-erasers-count=\"" + esc_attr(erasers_count_) + "\" " + "data-request-id=\"" + esc_attr(request_id_) + "\" " + "data-nonce=\"" + esc_attr(nonce_) + "\">")
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
                php_print("<button type=\"submit\" class=\"button-link\" name=\"privacy_action_email_retry[" + item_.ID + "]\" id=\"privacy_action_email_retry[" + item_.ID + "]\">" + __("Retry") + "</button>")
                break
            # end if
            if case("request-completed"):
                php_print("<a href=\"" + esc_url(wp_nonce_url(add_query_arg(Array({"action": "delete", "request_id": Array(item_.ID)}), admin_url("erase-personal-data.php")), "bulk-privacy_requests")) + "\">" + esc_html__("Remove request") + "</a>")
                break
            # end if
        # end for
    # end def column_next_steps
# end class WP_Privacy_Data_Removal_Requests_List_Table
