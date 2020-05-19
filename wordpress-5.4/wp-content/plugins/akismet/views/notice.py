#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
pass
if type_ == "plugin":
    php_print("<div class=\"updated\" id=\"akismet_setup_prompt\">\n    <form name=\"akismet_activate\" action=\"")
    php_print(esc_url(Akismet_Admin.get_page_url()))
    php_print("""\" method=\"POST\">
    <div class=\"akismet_activate\">
    <div class=\"aa_a\">A</div>
    <div class=\"aa_button_container\">
    <div class=\"aa_button_border\">
    <input type=\"submit\" class=\"aa_button\" value=\"""")
    esc_attr_e("Set up your Akismet account", "akismet")
    php_print("""\" />
    </div>
    </div>
    <div class=\"aa_description\">""")
    _e("<strong>Almost done</strong> - configure Akismet and say goodbye to spam", "akismet")
    php_print("""</div>
    </div>
    </form>
    </div>
    """)
elif type_ == "spam-check":
    php_print("<div class=\"notice notice-warning\">\n  <p><strong>")
    esc_html_e("Akismet has detected a problem.", "akismet")
    php_print("</strong></p>\n  <p>")
    esc_html_e("Some comments have not yet been checked for spam by Akismet. They have been temporarily held for moderation and will automatically be rechecked later.", "akismet")
    php_print("</p>\n   ")
    if link_text_:
        php_print("     <p>")
        php_print(link_text_)
        php_print("</p>\n   ")
    # end if
    php_print("</div>\n")
elif type_ == "alert":
    php_print("<div class='error'>\n    <p><strong>")
    php_printf(esc_html__("Akismet Error Code: %s", "akismet"), code_)
    php_print("</strong></p>\n  <p>")
    php_print(esc_html(msg_))
    php_print("</p>\n   <p>")
    #// translators: the placeholder is a clickable URL that leads to more information regarding an error code.
    php_printf(esc_html__("For more information: %s", "akismet"), "<a href=\"https://akismet.com/errors/" + code_ + "\">https://akismet.com/errors/" + code_ + "</a>")
    php_print(" </p>\n</div>\n")
elif type_ == "notice":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status failed\">")
    php_print(notice_header_)
    php_print("</h3>\n  <p class=\"akismet-description\">\n     ")
    php_print(notice_text_)
    php_print(" </p>\n</div>\n")
elif type_ == "missing-functions":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status failed\">")
    esc_html_e("Network functions are disabled.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("Your web host or server administrator has disabled PHP&#8217;s <code>gethostbynamel</code> function.  <strong>Akismet cannot work correctly until this is fixed.</strong>  Please contact your web host or firewall administrator and give them <a href=\"%s\" target=\"_blank\">this information about Akismet&#8217;s system requirements</a>.", "akismet"), "https://blog.akismet.com/akismet-hosting-faq/")
    php_print("</p>\n</div>\n")
elif type_ == "servers-be-down":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status failed\">")
    esc_html_e("Your site can&#8217;t connect to the Akismet servers.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("Your firewall may be blocking Akismet from connecting to its API. Please contact your host and refer to <a href=\"%s\" target=\"_blank\">our guide about firewalls</a>.", "akismet"), "https://blog.akismet.com/akismet-hosting-faq/")
    php_print("</p>\n</div>\n")
elif type_ == "active-dunning":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status\">")
    esc_html_e("Please update your payment information.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("We cannot process your payment. Please <a href=\"%s\" target=\"_blank\">update your payment details</a>.", "akismet"), "https://akismet.com/account/")
    php_print("</p>\n</div>\n")
elif type_ == "cancelled":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status\">")
    esc_html_e("Your Akismet plan has been cancelled.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("Please visit your <a href=\"%s\" target=\"_blank\">Akismet account page</a> to reactivate your subscription.", "akismet"), "https://akismet.com/account/")
    php_print("</p>\n</div>\n")
elif type_ == "suspended":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status failed\">")
    esc_html_e("Your Akismet subscription is suspended.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("Please contact <a href=\"%s\" target=\"_blank\">Akismet support</a> for assistance.", "akismet"), "https://akismet.com/contact/")
    php_print("</p>\n</div>\n")
elif type_ == "active-notice" and time_saved_:
    php_print("<div class=\"akismet-alert akismet-active\">\n   <h3 class=\"akismet-key-status\">")
    php_print(esc_html(time_saved_))
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("You can help us fight spam and upgrade your account by <a href=\"%s\" target=\"_blank\">contributing a token amount</a>.", "akismet"), "https://akismet.com/account/upgrade/")
    php_print("</p>\n</div>\n")
elif type_ == "missing":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status failed\">")
    esc_html_e("There is a problem with your API key.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("Please contact <a href=\"%s\" target=\"_blank\">Akismet support</a> for assistance.", "akismet"), "https://akismet.com/contact/")
    php_print("</p>\n</div>\n")
elif type_ == "no-sub":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status failed\">")
    esc_html_e("You don&#8217;t have an Akismet plan.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">\n     ")
    php_printf(__("In 2012, Akismet began using subscription plans for all accounts (even free ones). A plan has not been assigned to your account, and we&#8217;d appreciate it if you&#8217;d <a href=\"%s\" target=\"_blank\">sign into your account</a> and choose one.", "akismet"), "https://akismet.com/account/upgrade/")
    php_print("     <br /><br />\n      ")
    php_printf(__("Please <a href=\"%s\" target=\"_blank\">contact our support team</a> with any questions.", "akismet"), "https://akismet.com/contact/")
    php_print(" </p>\n</div>\n")
elif type_ == "new-key-valid":
    global wpdb_
    php_check_if_defined("wpdb_")
    check_pending_link_ = False
    at_least_one_comment_in_moderation_ = (not (not wpdb_.get_var(str("SELECT comment_ID FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = '0' LIMIT 1"))))
    if at_least_one_comment_in_moderation_:
        check_pending_link_ = "edit-comments.php?akismet_recheck=" + wp_create_nonce("akismet_recheck")
    # end if
    php_print("<div class=\"akismet-alert akismet-active\">\n   <h3 class=\"akismet-key-status\">")
    esc_html_e("Akismet is now protecting your site from spam. Happy blogging!", "akismet")
    php_print("</h3>\n  ")
    if check_pending_link_:
        php_print("     <p class=\"akismet-description\">")
        php_printf(__("Would you like to <a href=\"%s\">check pending comments</a>?", "akismet"), esc_url(check_pending_link_))
        php_print("</p>\n   ")
    # end if
    php_print("</div>\n")
elif type_ == "new-key-invalid":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status\">")
    esc_html_e("The key you entered is invalid. Please double-check it.", "akismet")
    php_print("</h3>\n</div>\n")
elif type_ == "existing-key-invalid":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status\">")
    esc_html_e("Your API key is no longer valid. Please enter a new key or contact support@akismet.com.", "akismet")
    php_print("</h3>\n</div>\n")
elif type_ == "new-key-failed":
    php_print("<div class=\"akismet-alert akismet-critical\">\n <h3 class=\"akismet-key-status\">")
    esc_html_e("The API key you entered could not be verified.", "akismet")
    php_print("</h3>\n  <p class=\"akismet-description\">")
    php_printf(__("The connection to akismet.com could not be established. Please refer to <a href=\"%s\" target=\"_blank\">our guide about firewalls</a> and check your server configuration.", "akismet"), "https://blog.akismet.com/akismet-hosting-faq/")
    php_print("</p>\n</div>\n")
elif type_ == "limit-reached" and php_in_array(level_, Array("yellow", "red")):
    php_print("<div class=\"akismet-alert akismet-critical\">\n ")
    if level_ == "yellow":
        php_print(" <h3 class=\"akismet-key-status failed\">")
        esc_html_e("You&#8217;re using your Akismet key on more sites than your Pro subscription allows.", "akismet")
        php_print("</h3>\n  <p class=\"akismet-description\">\n     ")
        php_printf(__("Your Pro subscription allows the use of Akismet on only one site. Please <a href=\"%s\" target=\"_blank\">purchase additional Pro subscriptions</a> or upgrade to an Enterprise subscription that allows the use of Akismet on unlimited sites.", "akismet"), "https://docs.akismet.com/billing/add-more-sites/")
        php_print("     <br /><br />\n      ")
        php_printf(__("Please <a href=\"%s\" target=\"_blank\">contact our support team</a> with any questions.", "akismet"), "https://akismet.com/contact/")
        php_print(" </p>\n  ")
    elif level_ == "red":
        php_print(" <h3 class=\"akismet-key-status failed\">")
        esc_html_e("You&#8217;re using Akismet on far too many sites for your Pro subscription.", "akismet")
        php_print("</h3>\n  <p class=\"akismet-description\">\n     ")
        php_printf(__("To continue your service, <a href=\"%s\" target=\"_blank\">upgrade to an Enterprise subscription</a>, which covers an unlimited number of sites.", "akismet"), "https://akismet.com/account/upgrade/")
        php_print("     <br /><br />\n      ")
        php_printf(__("Please <a href=\"%s\" target=\"_blank\">contact our support team</a> with any questions.", "akismet"), "https://akismet.com/contact/")
        php_print(" </p>\n  ")
    # end if
    php_print("</div>\n")
elif type_ == "privacy":
    php_print("<div class=\"notice notice-warning is-dismissible\" id=\"akismet-privacy-notice-admin-notice\">\n    <p><strong>")
    esc_html_e("Akismet & Privacy.", "akismet")
    php_print("</strong></p>\n  <p>")
    esc_html_e("To help your site with transparency under privacy laws like the GDPR, Akismet can display a notice to your users under your comment forms. This feature is disabled by default, however, you can turn it on below.", "akismet")
    php_print("</p>\n   <p>")
    php_printf(__(" Please <a href=\"%s\">enable</a> or <a href=\"%s\">disable</a> this feature. <a href=\"%s\" id=\"akismet-privacy-notice-control-notice-info-link\" target=\"_blank\">More information</a>.", "akismet"), admin_url(apply_filters("akismet_comment_form_privacy_notice_url_display", "options-general.php?page=akismet-key-config&akismet_comment_form_privacy_notice=display")), admin_url(apply_filters("akismet_comment_form_privacy_notice_url_hide", "options-general.php?page=akismet-key-config&akismet_comment_form_privacy_notice=hide")), "https://akismet.com/privacy/")
    php_print("</p>\n</div>\n")
# end if
