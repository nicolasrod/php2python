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
global wpcom_api_key,akismet_api_host,akismet_api_port
php_check_if_defined("wpcom_api_key","akismet_api_host","akismet_api_port")
wpcom_api_key = constant("WPCOM_API_KEY") if php_defined("WPCOM_API_KEY") else ""
akismet_api_host = Akismet.get_api_key() + ".rest.akismet.com"
akismet_api_port = 80
def akismet_test_mode(*args_):
    
    return Akismet.is_test_mode()
# end def akismet_test_mode
def akismet_http_post(request=None, host=None, path=None, port=80, ip=None, *args_):
    
    path = php_str_replace("/1.1/", "", path)
    return Akismet.http_post(request, path, ip)
# end def akismet_http_post
def akismet_microtime(*args_):
    
    return Akismet._get_microtime()
# end def akismet_microtime
def akismet_delete_old(*args_):
    
    return Akismet.delete_old_comments()
# end def akismet_delete_old
def akismet_delete_old_metadata(*args_):
    
    return Akismet.delete_old_comments_meta()
# end def akismet_delete_old_metadata
def akismet_check_db_comment(id=None, recheck_reason="recheck_queue", *args_):
    
    return Akismet.check_db_comment(id, recheck_reason)
# end def akismet_check_db_comment
def akismet_rightnow(*args_):
    
    if (not php_class_exists("Akismet_Admin")):
        return False
    # end if
    return Akismet_Admin.rightnow_stats()
# end def akismet_rightnow
def akismet_admin_init(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_admin_init
def akismet_version_warning(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_version_warning
def akismet_load_js_and_css(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_load_js_and_css
def akismet_nonce_field(action=-1, *args_):
    
    return wp_nonce_field(action)
# end def akismet_nonce_field
def akismet_plugin_action_links(links=None, file=None, *args_):
    
    return Akismet_Admin.plugin_action_links(links, file)
# end def akismet_plugin_action_links
def akismet_conf(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_conf
def akismet_stats_display(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_stats_display
def akismet_stats(*args_):
    
    return Akismet_Admin.dashboard_stats()
# end def akismet_stats
def akismet_admin_warnings(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_admin_warnings
def akismet_comment_row_action(a=None, comment=None, *args_):
    
    return Akismet_Admin.comment_row_actions(a, comment)
# end def akismet_comment_row_action
def akismet_comment_status_meta_box(comment=None, *args_):
    
    return Akismet_Admin.comment_status_meta_box(comment)
# end def akismet_comment_status_meta_box
def akismet_comments_columns(columns=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
    return columns
# end def akismet_comments_columns
def akismet_comment_column_row(column=None, comment_id=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_comment_column_row
def akismet_text_add_link_callback(m=None, *args_):
    
    return Akismet_Admin.text_add_link_callback(m)
# end def akismet_text_add_link_callback
def akismet_text_add_link_class(comment_text=None, *args_):
    
    return Akismet_Admin.text_add_link_class(comment_text)
# end def akismet_text_add_link_class
def akismet_check_for_spam_button(comment_status=None, *args_):
    
    return Akismet_Admin.check_for_spam_button(comment_status)
# end def akismet_check_for_spam_button
def akismet_submit_nonspam_comment(comment_id=None, *args_):
    
    return Akismet.submit_nonspam_comment(comment_id)
# end def akismet_submit_nonspam_comment
def akismet_submit_spam_comment(comment_id=None, *args_):
    
    return Akismet.submit_spam_comment(comment_id)
# end def akismet_submit_spam_comment
def akismet_transition_comment_status(new_status=None, old_status=None, comment=None, *args_):
    
    return Akismet.transition_comment_status(new_status, old_status, comment)
# end def akismet_transition_comment_status
def akismet_spam_count(type=False, *args_):
    
    return Akismet_Admin.get_spam_count(type)
# end def akismet_spam_count
def akismet_recheck_queue(*args_):
    
    return Akismet_Admin.recheck_queue()
# end def akismet_recheck_queue
def akismet_remove_comment_author_url(*args_):
    
    return Akismet_Admin.remove_comment_author_url()
# end def akismet_remove_comment_author_url
def akismet_add_comment_author_url(*args_):
    
    return Akismet_Admin.add_comment_author_url()
# end def akismet_add_comment_author_url
def akismet_check_server_connectivity(*args_):
    
    return Akismet_Admin.check_server_connectivity()
# end def akismet_check_server_connectivity
def akismet_get_server_connectivity(cache_timeout=86400, *args_):
    
    return Akismet_Admin.get_server_connectivity(cache_timeout)
# end def akismet_get_server_connectivity
def akismet_server_connectivity_ok(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
    return True
# end def akismet_server_connectivity_ok
def akismet_admin_menu(*args_):
    
    return Akismet_Admin.admin_menu()
# end def akismet_admin_menu
def akismet_load_menu(*args_):
    
    return Akismet_Admin.load_menu()
# end def akismet_load_menu
def akismet_init(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_init
def akismet_get_key(*args_):
    
    return Akismet.get_api_key()
# end def akismet_get_key
def akismet_check_key_status(key=None, ip=None, *args_):
    
    return Akismet.check_key_status(key, ip)
# end def akismet_check_key_status
def akismet_update_alert(response=None, *args_):
    
    return Akismet.update_alert(response)
# end def akismet_update_alert
def akismet_verify_key(key=None, ip=None, *args_):
    
    return Akismet.verify_key(key, ip)
# end def akismet_verify_key
def akismet_get_user_roles(user_id=None, *args_):
    
    return Akismet.get_user_roles(user_id)
# end def akismet_get_user_roles
def akismet_result_spam(approved=None, *args_):
    
    return Akismet.comment_is_spam(approved)
# end def akismet_result_spam
def akismet_result_hold(approved=None, *args_):
    
    return Akismet.comment_needs_moderation(approved)
# end def akismet_result_hold
def akismet_get_user_comments_approved(user_id=None, comment_author_email=None, comment_author=None, comment_author_url=None, *args_):
    
    return Akismet.get_user_comments_approved(user_id, comment_author_email, comment_author, comment_author_url)
# end def akismet_get_user_comments_approved
def akismet_update_comment_history(comment_id=None, message=None, event=None, *args_):
    
    return Akismet.update_comment_history(comment_id, message, event)
# end def akismet_update_comment_history
def akismet_get_comment_history(comment_id=None, *args_):
    
    return Akismet.get_comment_history(comment_id)
# end def akismet_get_comment_history
def akismet_cmp_time(a=None, b=None, *args_):
    
    return Akismet._cmp_time(a, b)
# end def akismet_cmp_time
def akismet_auto_check_update_meta(id=None, comment=None, *args_):
    
    return Akismet.auto_check_update_meta(id, comment)
# end def akismet_auto_check_update_meta
def akismet_auto_check_comment(commentdata=None, *args_):
    
    return Akismet.auto_check_comment(commentdata)
# end def akismet_auto_check_comment
def akismet_get_ip_address(*args_):
    
    return Akismet.get_ip_address()
# end def akismet_get_ip_address
def akismet_cron_recheck(*args_):
    
    return Akismet.cron_recheck()
# end def akismet_cron_recheck
def akismet_add_comment_nonce(post_id=None, *args_):
    
    return Akismet.add_comment_nonce(post_id)
# end def akismet_add_comment_nonce
def akismet_fix_scheduled_recheck(*args_):
    
    return Akismet.fix_scheduled_recheck()
# end def akismet_fix_scheduled_recheck
def akismet_spam_comments(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
    return Array()
# end def akismet_spam_comments
def akismet_spam_totals(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
    return Array()
# end def akismet_spam_totals
def akismet_manage_page(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_manage_page
def akismet_caught(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def akismet_caught
def redirect_old_akismet_urls(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
# end def redirect_old_akismet_urls
def akismet_kill_proxy_check(option=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0")
    return 0
# end def akismet_kill_proxy_check
def akismet_pingback_forwarded_for(r=None, url=None, *args_):
    
    #// This functionality is now in core.
    return False
# end def akismet_pingback_forwarded_for
def akismet_pre_check_pingback(method=None, *args_):
    
    return Akismet.pre_check_pingback(method)
# end def akismet_pre_check_pingback
