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
#// Multisite delete site panel.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#//
php_include_file(__DIR__ + "/admin.php", once=True)
if (not is_multisite()):
    wp_die(__("Multisite support is not enabled."))
# end if
if (not current_user_can("delete_site")):
    wp_die(__("Sorry, you are not allowed to delete this site."))
# end if
if (php_isset(lambda : PHP_REQUEST["h"])) and "" != PHP_REQUEST["h"] and False != get_option("delete_blog_hash"):
    if hash_equals(get_option("delete_blog_hash"), PHP_REQUEST["h"]):
        wpmu_delete_blog(get_current_blog_id())
        wp_die(php_sprintf(__("Thank you for using %s, your site has been deleted. Happy trails to you until we meet again."), get_network().site_name))
    else:
        wp_die(__("Sorry, the link you clicked is stale. Please select another option."))
    # end if
# end if
blog_ = get_site()
user_ = wp_get_current_user()
title_ = __("Delete Site")
parent_file_ = "tools.php"
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">")
php_print("<h1>" + esc_html(title_) + "</h1>")
if (php_isset(lambda : PHP_POST["action"])) and "deleteblog" == PHP_POST["action"] and (php_isset(lambda : PHP_POST["confirmdelete"])) and "1" == PHP_POST["confirmdelete"]:
    check_admin_referer("delete-blog")
    hash_ = wp_generate_password(20, False)
    update_option("delete_blog_hash", hash_)
    url_delete_ = esc_url(admin_url("ms-delete-site.php?h=" + hash_))
    switched_locale_ = switch_to_locale(get_locale())
    #// translators: Do not translate USERNAME, URL_DELETE, SITE_NAME: those are placeholders.
    content_ = __("""Howdy ###USERNAME###,
    You recently clicked the 'Delete Site' link on your site and filled in a
    form on that page.
    If you really want to delete your site, click the link below. You will not
    be asked to confirm again so only click this link if you are absolutely certain:
    ###URL_DELETE###
    If you delete your site, please consider opening a new site here
    some time in the future! (But remember your current site and username
    are gone forever.)
    Thanks for using the site,
    Webmaster
    ###SITE_NAME###""")
    #// 
    #// Filters the email content sent when a site in a Multisite network is deleted.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $content The email content that will be sent to the user who deleted a site in a Multisite network.
    #//
    content_ = apply_filters("delete_site_email_content", content_)
    content_ = php_str_replace("###USERNAME###", user_.user_login, content_)
    content_ = php_str_replace("###URL_DELETE###", url_delete_, content_)
    content_ = php_str_replace("###SITE_NAME###", get_network().site_name, content_)
    wp_mail(get_option("admin_email"), php_sprintf(__("[%s] Delete My Site"), wp_specialchars_decode(get_option("blogname"))), content_)
    if switched_locale_:
        restore_previous_locale()
    # end if
    php_print("\n   <p>")
    _e("Thank you. Please check your email for a link to confirm your action. Your site will not be deleted until this link is clicked.")
    php_print("</p>\n\n ")
else:
    php_print(" <p>\n   ")
    printf(__("If you do not want to use your %s site any more, you can delete it using the form below. When you click <strong>Delete My Site Permanently</strong> you will be sent an email with a link in it. Click on this link to delete your site."), get_network().site_name)
    php_print(" </p>\n  <p>")
    _e("Remember, once deleted your site cannot be restored.")
    php_print("""</p>
    <form method=\"post\" name=\"deletedirect\">
    """)
    wp_nonce_field("delete-blog")
    php_print("     <input type=\"hidden\" name=\"action\" value=\"deleteblog\" />\n        <p><input id=\"confirmdelete\" type=\"checkbox\" name=\"confirmdelete\" value=\"1\" /> <label for=\"confirmdelete\"><strong>\n      ")
    printf(__("I'm sure I want to permanently disable my site, and I am aware I can never get it back or use %s again."), blog_.domain + blog_.path)
    php_print("     </strong></label></p>\n     ")
    submit_button(__("Delete My Site Permanently"))
    php_print(" </form>\n   ")
# end if
php_print("</div>")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
