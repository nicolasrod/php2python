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
php_print("""<div id=\"akismet-plugin-container\">
<div class=\"akismet-masthead\">
<div class=\"akismet-masthead__inside-container\">
<div class=\"akismet-masthead__logo-container\">
<img class=\"akismet-masthead__logo\" src=\"""")
php_print(esc_url(plugins_url("../_inc/img/logo-full-2x.png", __FILE__)))
php_print("""\" alt=\"Akismet\" />
</div>
</div>
</div>
<div class=\"akismet-lower\">
""")
if Akismet.get_api_key():
    php_print("         ")
    Akismet_Admin.display_status()
    php_print("     ")
# end if
php_print("     ")
if (not php_empty(lambda : notices)):
    php_print("         ")
    for notice in notices:
        php_print("             ")
        Akismet.view("notice", notice)
        php_print("         ")
    # end for
    php_print("     ")
# end if
php_print("     ")
if stat_totals and (php_isset(lambda : stat_totals["all"])) and int(stat_totals["all"].spam) > 0:
    php_print("""           <div class=\"akismet-card\">
    <div class=\"akismet-section-header\">
    <div class=\"akismet-section-header__label\">
    <span>""")
    esc_html_e("Statistics", "akismet")
    php_print("""</span>
    </div>
    <div class=\"akismet-section-header__actions\">
    <a href=\"""")
    php_print(esc_url(Akismet_Admin.get_page_url("stats")))
    php_print("\">\n                            ")
    esc_html_e("Detailed Stats", "akismet")
    php_print("""                       </a>
    </div>
    </div>
    
    <div class=\"akismet-new-snapshot\">
    <iframe allowtransparency=\"true\" scrolling=\"no\" frameborder=\"0\" style=\"width: 100%; height: 220px; overflow: hidden;\" src=\"""")
    printf("//akismet.com/web/1.0/snapshot.php?blog=%s&api_key=%s&height=200&locale=%s", urlencode(get_option("home")), Akismet.get_api_key(), get_locale())
    php_print("""\"></iframe>
    <ul>
    <li>
    <h3>""")
    esc_html_e("Past six months", "akismet")
    php_print("</h3>\n                          <span>")
    php_print(number_format(stat_totals["6-months"].spam))
    php_print("</span>\n                            ")
    php_print(esc_html(_n("Spam blocked", "Spam blocked", stat_totals["6-months"].spam, "akismet")))
    php_print("                     </li>\n                     <li>\n                          <h3>")
    esc_html_e("All time", "akismet")
    php_print("</h3>\n                          <span>")
    php_print(number_format(stat_totals["all"].spam))
    php_print("</span>\n                            ")
    php_print(esc_html(_n("Spam blocked", "Spam blocked", stat_totals["all"].spam, "akismet")))
    php_print("                     </li>\n                     <li>\n                          <h3>")
    esc_html_e("Accuracy", "akismet")
    php_print("</h3>\n                          <span>")
    php_print(floatval(stat_totals["all"].accuracy))
    php_print("%</span>\n                           ")
    printf(_n("%s missed spam", "%s missed spam", stat_totals["all"].missed_spam, "akismet"), number_format(stat_totals["all"].missed_spam))
    php_print("                         |\n                         ")
    printf(_n("%s false positive", "%s false positives", stat_totals["all"].false_positives, "akismet"), number_format(stat_totals["all"].false_positives))
    php_print("""                       </li>
    </ul>
    </div>
    </div>
    """)
# end if
php_print("\n       ")
if akismet_user:
    php_print("""           <div class=\"akismet-card\">
    <div class=\"akismet-section-header\">
    <div class=\"akismet-section-header__label\">
    <span>""")
    esc_html_e("Settings", "akismet")
    php_print("""</span>
    </div>
    </div>
    <div class=\"inside\">
    <form action=\"""")
    php_print(esc_url(Akismet_Admin.get_page_url()))
    php_print("""\" method=\"POST\">
    <table cellspacing=\"0\" class=\"akismet-settings\">
    <tbody>
    """)
    if (not Akismet.predefined_api_key()):
        php_print("                             <tr>\n                                  <th class=\"akismet-api-key\" width=\"10%\" align=\"left\" scope=\"row\">")
        esc_html_e("API Key", "akismet")
        php_print("""</th>
        <td width=\"5%\"/>
        <td align=\"left\">
        <span class=\"api-key\"><input id=\"key\" name=\"key\" type=\"text\" size=\"15\" value=\"""")
        php_print(esc_attr(get_option("wordpress_api_key")))
        php_print("\" class=\"")
        php_print(esc_attr("regular-text code " + akismet_user.status))
        php_print("""\"></span>
        </td>
        </tr>
        """)
    # end if
    php_print("                             ")
    if (php_isset(lambda : PHP_REQUEST["ssl_status"])):
        php_print("                                 <tr>\n                                      <th align=\"left\" scope=\"row\">")
        esc_html_e("SSL Status", "akismet")
        php_print("""</th>
        <td></td>
        <td align=\"left\">
        <p>
        """)
        if (not wp_http_supports(Array("ssl"))):
            php_print("<b>")
            esc_html_e("Disabled.", "akismet")
            php_print("</b> ")
            esc_html_e("Your Web server cannot make SSL requests; contact your Web host and ask them to add support for SSL requests.", "akismet")
        else:
            ssl_disabled = get_option("akismet_ssl_disabled")
            if ssl_disabled:
                php_print("<b>")
                esc_html_e("Temporarily disabled.", "akismet")
                php_print("</b> ")
                esc_html_e("Akismet encountered a problem with a previous SSL request and disabled it temporarily. It will begin using SSL for requests again shortly.", "akismet")
            else:
                php_print("<b>")
                esc_html_e("Enabled.", "akismet")
                php_print("</b> ")
                esc_html_e("All systems functional.", "akismet")
            # end if
        # end if
        php_print("""                                           </p>
        </td>
        </tr>
        """)
    # end if
    php_print("                             <tr>\n                                  <th align=\"left\" scope=\"row\">")
    esc_html_e("Comments", "akismet")
    php_print("""</th>
    <td></td>
    <td align=\"left\">
    <p>
    <label for=\"akismet_show_user_comments_approved\" title=\"""")
    esc_attr_e("Show approved comments", "akismet")
    php_print("""\">
    <input
    name=\"akismet_show_user_comments_approved\"
    id=\"akismet_show_user_comments_approved\"
    value=\"1\"
    type=\"checkbox\"
    """)
    #// If the option isn't set, or if it's enabled ('1'), or if it was enabled a long time ago ('true'), check the checkbox.
    checked(True, php_in_array(get_option("akismet_show_user_comments_approved"), Array(False, "1", "true"), True))
    php_print("                                                 />\n                                                ")
    esc_html_e("Show the number of approved comments beside each comment author", "akismet")
    php_print("""                                           </label>
    </p>
    </td>
    </tr>
    <tr>
    <th class=\"strictness\" align=\"left\" scope=\"row\">""")
    esc_html_e("Strictness", "akismet")
    php_print("""</th>
    <td></td>
    <td align=\"left\">
    <fieldset><legend class=\"screen-reader-text\"><span>""")
    esc_html_e("Akismet anti-spam strictness", "akismet")
    php_print("</span></legend>\n                                       <p><label for=\"akismet_strictness_1\"><input type=\"radio\" name=\"akismet_strictness\" id=\"akismet_strictness_1\" value=\"1\" ")
    checked("1", get_option("akismet_strictness"))
    php_print(" /> ")
    esc_html_e("Silently discard the worst and most pervasive spam so I never see it.", "akismet")
    php_print("</label></p>\n                                       <p><label for=\"akismet_strictness_0\"><input type=\"radio\" name=\"akismet_strictness\" id=\"akismet_strictness_0\" value=\"0\" ")
    checked("0", get_option("akismet_strictness"))
    php_print(" /> ")
    esc_html_e("Always put spam in the Spam folder for review.", "akismet")
    php_print("</label></p>\n                                       </fieldset>\n                                       <span class=\"akismet-note\"><strong>")
    esc_html_e("Note:", "akismet")
    php_print("</strong>\n                                      ")
    delete_interval = php_max(1, php_intval(apply_filters("akismet_delete_comment_interval", 15)))
    printf(_n("Spam in the <a href=\"%1$s\">spam folder</a> older than 1 day is deleted automatically.", "Spam in the <a href=\"%1$s\">spam folder</a> older than %2$d days is deleted automatically.", delete_interval, "akismet"), admin_url("edit-comments.php?comment_status=spam"), delete_interval)
    php_print("""                                   </td>
    </tr>
    <tr>
    <th class=\"comment-form-privacy-notice\" align=\"left\" scope=\"row\">""")
    esc_html_e("Privacy", "akismet")
    php_print("""</th>
    <td></td>
    <td align=\"left\">
    <fieldset><legend class=\"screen-reader-text\"><span>""")
    esc_html_e("Akismet privacy notice", "akismet")
    php_print("</span></legend>\n                                       <p><label for=\"akismet_comment_form_privacy_notice_display\"><input type=\"radio\" name=\"akismet_comment_form_privacy_notice\" id=\"akismet_comment_form_privacy_notice_display\" value=\"display\" ")
    checked("display", get_option("akismet_comment_form_privacy_notice"))
    php_print(" /> ")
    esc_html_e("Display a privacy notice under your comment forms.", "akismet")
    php_print("</label></p>\n                                       <p><label for=\"akismet_comment_form_privacy_notice_hide\"><input type=\"radio\" name=\"akismet_comment_form_privacy_notice\" id=\"akismet_comment_form_privacy_notice_hide\" value=\"hide\" ")
    php_print(checked("hide", get_option("akismet_comment_form_privacy_notice"), False) if php_in_array(get_option("akismet_comment_form_privacy_notice"), Array("display", "hide")) else "checked=\"checked\"")
    php_print(" /> ")
    esc_html_e("Do not display privacy notice.", "akismet")
    php_print("</label></p>\n                                       </fieldset>\n                                       <span class=\"akismet-note\">")
    esc_html_e("To help your site with transparency under privacy laws like the GDPR, Akismet can display a notice to your users under your comment forms. This feature is disabled by default, however, you can turn it on above.", "akismet")
    php_print("""</span>
    </td>
    </tr>
    </tbody>
    </table>
    <div class=\"akismet-card-actions\">
    """)
    if (not Akismet.predefined_api_key()):
        php_print("                         <div id=\"delete-action\">\n                                <a class=\"submitdelete deletion\" href=\"")
        php_print(esc_url(Akismet_Admin.get_page_url("delete_key")))
        php_print("\">")
        esc_html_e("Disconnect this account", "akismet")
        php_print("</a>\n                           </div>\n                            ")
    # end if
    php_print("                         ")
    wp_nonce_field(Akismet_Admin.NONCE)
    php_print("                         <div id=\"publishing-action\">\n                                <input type=\"hidden\" name=\"action\" value=\"enter-key\">\n                               <input type=\"submit\" name=\"submit\" id=\"submit\" class=\"akismet-button akismet-could-be-primary\" value=\"")
    esc_attr_e("Save Changes", "akismet")
    php_print("""\">
    </div>
    <div class=\"clear\"></div>
    </div>
    </form>
    </div>
    </div>
    
    """)
    if (not Akismet.predefined_api_key()):
        php_print("""               <div class=\"akismet-card\">
        <div class=\"akismet-section-header\">
        <div class=\"akismet-section-header__label\">
        <span>""")
        esc_html_e("Account", "akismet")
        php_print("""</span>
        </div>
        </div>
        
        <div class=\"inside\">
        <table cellspacing=\"0\" border=\"0\" class=\"akismet-settings\">
        <tbody>
        <tr>
        <th scope=\"row\" align=\"left\">""")
        esc_html_e("Subscription Type", "akismet")
        php_print("""</th>
        <td width=\"5%\"/>
        <td align=\"left\">
        <p>""")
        php_print(esc_html(akismet_user.account_name))
        php_print("""</p>
        </td>
        </tr>
        <tr>
        <th scope=\"row\" align=\"left\">""")
        esc_html_e("Status", "akismet")
        php_print("""</th>
        <td width=\"5%\"/>
        <td align=\"left\">
        <p>""")
        if "cancelled" == akismet_user.status:
            esc_html_e("Cancelled", "akismet")
        elif "suspended" == akismet_user.status:
            esc_html_e("Suspended", "akismet")
        elif "missing" == akismet_user.status:
            esc_html_e("Missing", "akismet")
        elif "no-sub" == akismet_user.status:
            esc_html_e("No Subscription Found", "akismet")
        else:
            esc_html_e("Active", "akismet")
        # end if
        php_print("""</p>
        </td>
        </tr>
        """)
        if akismet_user.next_billing_date:
            php_print("                             <tr>\n                                  <th scope=\"row\" align=\"left\">")
            esc_html_e("Next Billing Date", "akismet")
            php_print("""</th>
            <td width=\"5%\"/>
            <td align=\"left\">
            <p>""")
            php_print(date("F j, Y", akismet_user.next_billing_date))
            php_print("""</p>
            </td>
            </tr>
            """)
        # end if
        php_print("""                           </tbody>
        </table>
        <div class=\"akismet-card-actions\">
        <div id=\"publishing-action\">
        """)
        Akismet.view("get", Array({"text": __("Upgrade", "akismet") if akismet_user.account_type == "free-api-key" and akismet_user.status == "active" else __("Change", "akismet"), "redirect": "upgrade"}))
        php_print("""                           </div>
        <div class=\"clear\"></div>
        </div>
        </div>
        </div>
        """)
    # end if
    php_print("     ")
# end if
php_print(" </div>\n</div>\n")
