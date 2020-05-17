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
#// Privacy tools, Erase Personal Data screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("erase_others_personal_data")) or (not current_user_can("delete_users")):
    wp_die(__("Sorry, you are not allowed to erase data on this site."))
# end if
#// Handle list table actions.
_wp_personal_data_handle_actions()
#// Cleans up failed and expired requests before displaying the list table.
_wp_personal_data_cleanup_requests()
wp_enqueue_script("privacy-tools")
add_screen_option("per_page", Array({"default": 20, "option": "remove_personal_data_requests_per_page"}))
_list_table_args_ = Array({"plural": "privacy_requests", "singular": "privacy_request"})
requests_table_ = _get_list_table("WP_Privacy_Data_Removal_Requests_List_Table", _list_table_args_)
requests_table_.screen.set_screen_reader_content(Array({"heading_views": __("Filter erase personal data list"), "heading_pagination": __("Erase personal data list navigation"), "heading_list": __("Erase personal data list")}))
requests_table_.process_bulk_action()
requests_table_.prepare_items()
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap nosubsub\">\n    <h1>")
esc_html_e("Erase Personal Data")
php_print("""</h1>
<hr class=\"wp-header-end\" />
""")
settings_errors()
php_print("\n   <form action=\"")
php_print(esc_url(admin_url("erase-personal-data.php")))
php_print("\" method=\"post\" class=\"wp-privacy-request-form\">\n      <h2>")
esc_html_e("Add Data Erasure Request")
php_print("</h2>\n      <p>")
esc_html_e("An email will be sent to the user at this email address asking them to verify the request.")
php_print("""</p>
<div class=\"wp-privacy-request-form-field\">
<label for=\"username_or_email_for_privacy_request\">""")
esc_html_e("Username or email address")
php_print("</label>\n           <input type=\"text\" required class=\"regular-text\" id=\"username_or_email_for_privacy_request\" name=\"username_or_email_for_privacy_request\" />\n           ")
submit_button(__("Send Request"), "secondary", "submit", False)
php_print("     </div>\n        ")
wp_nonce_field("personal-data-request")
php_print("""       <input type=\"hidden\" name=\"action\" value=\"add_remove_personal_data_request\" />
<input type=\"hidden\" name=\"type_of_action\" value=\"remove_personal_data\" />
</form>
<hr />
""")
requests_table_.views()
php_print("\n   <form class=\"search-form wp-clearfix\">\n      ")
requests_table_.search_box(__("Search Requests"), "requests")
php_print("     <input type=\"hidden\" name=\"filter-status\" value=\"")
php_print(esc_attr(sanitize_text_field(PHP_REQUEST["filter-status"])) if (php_isset(lambda : PHP_REQUEST["filter-status"])) else "")
php_print("\" />\n      <input type=\"hidden\" name=\"orderby\" value=\"")
php_print(esc_attr(sanitize_text_field(PHP_REQUEST["orderby"])) if (php_isset(lambda : PHP_REQUEST["orderby"])) else "")
php_print("\" />\n      <input type=\"hidden\" name=\"order\" value=\"")
php_print(esc_attr(sanitize_text_field(PHP_REQUEST["order"])) if (php_isset(lambda : PHP_REQUEST["order"])) else "")
php_print("""\" />
</form>
<form method=\"post\">
""")
requests_table_.display()
requests_table_.embed_scripts()
php_print("""   </form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
