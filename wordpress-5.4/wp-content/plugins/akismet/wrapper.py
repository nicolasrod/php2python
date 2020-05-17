#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
global wpcom_api_key_
global akismet_api_host_
global akismet_api_port_
php_check_if_defined("wpcom_api_key_","akismet_api_host_","akismet_api_port_")
wpcom_api_key_ = constant("WPCOM_API_KEY") if php_defined("WPCOM_API_KEY") else ""
akismet_api_host_ = Akismet.get_api_key() + ".rest.akismet.com"
akismet_api_port_ = 80
def akismet_test_mode(*_args_):
    
    
    return Akismet.is_test_mode()
# end def akismet_test_mode
def akismet_http_post(request_=None, host_=None, path_=None, port_=80, ip_=None, *_args_):
    if ip_ is None:
        ip_ = None
    # end if
    
    path_ = php_str_replace("/1.1/", "", path_)
    return Akismet.http_post(request_, path_, ip_)
# end def akismet_http_post
def akismet_microtime(*_args_):
    
    
    return Akismet._get_microtime()
# end def akismet_microtime
def akismet_delete_old(*_args_):
    
    
    return Akismet.delete_old_comments()
# end def akismet_delete_old
def akismet_delete_old_metadata(*_args_):
    
    
    return Akismet.delete_old_comments_meta()
# end def akismet_delete_old_metadata
def akismet_check_db_comment(id_=None, recheck_reason_="recheck_queue", *_args_):
    
    
    return Akismet.check_db_comment(id_, recheck_reason_)
# end def akismet_check_db_comment
def akismet_rightnow(*_args_):
    
    
    if (not php_class_exists("Akismet_Admin")):
        return False
    # end if
    return Akismet_Admin.rightnow_stats()
# end def akismet_rightnow
def akismet_admin_init(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_admin_init
def akismet_version_warning(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_version_warning
def akismet_load_js_and_css(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_load_js_and_css
def akismet_nonce_field(action_=None, *_args_):
    if action_ is None:
        action_ = -1
    # end if
    
    return wp_nonce_field(action_)
# end def akismet_nonce_field
def akismet_plugin_action_links(links_=None, file_=None, *_args_):
    
    
    return Akismet_Admin.plugin_action_links(links_, file_)
# end def akismet_plugin_action_links
def akismet_conf(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_conf
def akismet_stats_display(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_stats_display
def akismet_stats(*_args_):
    
    
    return Akismet_Admin.dashboard_stats()
# end def akismet_stats
def akismet_admin_warnings(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_admin_warnings
def akismet_comment_row_action(a_=None, comment_=None, *_args_):
    
    
    return Akismet_Admin.comment_row_actions(a_, comment_)
# end def akismet_comment_row_action
def akismet_comment_status_meta_box(comment_=None, *_args_):
    
    
    return Akismet_Admin.comment_status_meta_box(comment_)
# end def akismet_comment_status_meta_box
def akismet_comments_columns(columns_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
    return columns_
# end def akismet_comments_columns
def akismet_comment_column_row(column_=None, comment_id_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_comment_column_row
def akismet_text_add_link_callback(m_=None, *_args_):
    
    
    return Akismet_Admin.text_add_link_callback(m_)
# end def akismet_text_add_link_callback
def akismet_text_add_link_class(comment_text_=None, *_args_):
    
    
    return Akismet_Admin.text_add_link_class(comment_text_)
# end def akismet_text_add_link_class
def akismet_check_for_spam_button(comment_status_=None, *_args_):
    
    
    return Akismet_Admin.check_for_spam_button(comment_status_)
# end def akismet_check_for_spam_button
def akismet_submit_nonspam_comment(comment_id_=None, *_args_):
    
    
    return Akismet.submit_nonspam_comment(comment_id_)
# end def akismet_submit_nonspam_comment
def akismet_submit_spam_comment(comment_id_=None, *_args_):
    
    
    return Akismet.submit_spam_comment(comment_id_)
# end def akismet_submit_spam_comment
def akismet_transition_comment_status(new_status_=None, old_status_=None, comment_=None, *_args_):
    
    
    return Akismet.transition_comment_status(new_status_, old_status_, comment_)
# end def akismet_transition_comment_status
def akismet_spam_count(type_=None, *_args_):
    if type_ is None:
        type_ = False
    # end if
    
    return Akismet_Admin.get_spam_count(type_)
# end def akismet_spam_count
def akismet_recheck_queue(*_args_):
    
    
    return Akismet_Admin.recheck_queue()
# end def akismet_recheck_queue
def akismet_remove_comment_author_url(*_args_):
    
    
    return Akismet_Admin.remove_comment_author_url()
# end def akismet_remove_comment_author_url
def akismet_add_comment_author_url(*_args_):
    
    
    return Akismet_Admin.add_comment_author_url()
# end def akismet_add_comment_author_url
def akismet_check_server_connectivity(*_args_):
    
    
    return Akismet_Admin.check_server_connectivity()
# end def akismet_check_server_connectivity
def akismet_get_server_connectivity(cache_timeout_=86400, *_args_):
    
    
    return Akismet_Admin.get_server_connectivity(cache_timeout_)
# end def akismet_get_server_connectivity
def akismet_server_connectivity_ok(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
    return True
# end def akismet_server_connectivity_ok
def akismet_admin_menu(*_args_):
    
    
    return Akismet_Admin.admin_menu()
# end def akismet_admin_menu
def akismet_load_menu(*_args_):
    
    
    return Akismet_Admin.load_menu()
# end def akismet_load_menu
def akismet_init(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_init
def akismet_get_key(*_args_):
    
    
    return Akismet.get_api_key()
# end def akismet_get_key
def akismet_check_key_status(key_=None, ip_=None, *_args_):
    if ip_ is None:
        ip_ = None
    # end if
    
    return Akismet.check_key_status(key_, ip_)
# end def akismet_check_key_status
def akismet_update_alert(response_=None, *_args_):
    
    
    return Akismet.update_alert(response_)
# end def akismet_update_alert
def akismet_verify_key(key_=None, ip_=None, *_args_):
    if ip_ is None:
        ip_ = None
    # end if
    
    return Akismet.verify_key(key_, ip_)
# end def akismet_verify_key
def akismet_get_user_roles(user_id_=None, *_args_):
    
    
    return Akismet.get_user_roles(user_id_)
# end def akismet_get_user_roles
def akismet_result_spam(approved_=None, *_args_):
    
    
    return Akismet.comment_is_spam(approved_)
# end def akismet_result_spam
def akismet_result_hold(approved_=None, *_args_):
    
    
    return Akismet.comment_needs_moderation(approved_)
# end def akismet_result_hold
def akismet_get_user_comments_approved(user_id_=None, comment_author_email_=None, comment_author_=None, comment_author_url_=None, *_args_):
    
    
    return Akismet.get_user_comments_approved(user_id_, comment_author_email_, comment_author_, comment_author_url_)
# end def akismet_get_user_comments_approved
def akismet_update_comment_history(comment_id_=None, message_=None, event_=None, *_args_):
    if event_ is None:
        event_ = None
    # end if
    
    return Akismet.update_comment_history(comment_id_, message_, event_)
# end def akismet_update_comment_history
def akismet_get_comment_history(comment_id_=None, *_args_):
    
    
    return Akismet.get_comment_history(comment_id_)
# end def akismet_get_comment_history
def akismet_cmp_time(a_=None, b_=None, *_args_):
    
    
    return Akismet._cmp_time(a_, b_)
# end def akismet_cmp_time
def akismet_auto_check_update_meta(id_=None, comment_=None, *_args_):
    
    
    return Akismet.auto_check_update_meta(id_, comment_)
# end def akismet_auto_check_update_meta
def akismet_auto_check_comment(commentdata_=None, *_args_):
    
    
    return Akismet.auto_check_comment(commentdata_)
# end def akismet_auto_check_comment
def akismet_get_ip_address(*_args_):
    
    
    return Akismet.get_ip_address()
# end def akismet_get_ip_address
def akismet_cron_recheck(*_args_):
    
    
    return Akismet.cron_recheck()
# end def akismet_cron_recheck
def akismet_add_comment_nonce(post_id_=None, *_args_):
    
    
    return Akismet.add_comment_nonce(post_id_)
# end def akismet_add_comment_nonce
def akismet_fix_scheduled_recheck(*_args_):
    
    
    return Akismet.fix_scheduled_recheck()
# end def akismet_fix_scheduled_recheck
def akismet_spam_comments(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
    return Array()
# end def akismet_spam_comments
def akismet_spam_totals(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
    return Array()
# end def akismet_spam_totals
def akismet_manage_page(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_manage_page
def akismet_caught(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_caught
def redirect_old_akismet_urls(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def redirect_old_akismet_urls
def akismet_kill_proxy_check(option_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0")
    return 0
# end def akismet_kill_proxy_check
def akismet_pingback_forwarded_for(r_=None, url_=None, *_args_):
    
    
    #// This functionality is now in core.
    return False
# end def akismet_pingback_forwarded_for
def akismet_pre_check_pingback(method_=None, *_args_):
    
    
    return Akismet.pre_check_pingback(method_)
# end def akismet_pre_check_pingback
