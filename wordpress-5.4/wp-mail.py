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
#// Gets the email message from the user's mailbox to add as
#// a WordPress post. Mailbox connection information must be
#// configured under Settings > Writing
#// 
#// @package WordPress
#// 
#// Make sure that the WordPress bootstrap has run before continuing.
php_include_file(__DIR__ + "/wp-load.php", once=False)
#// This filter is documented in wp-admin/options.php
if (not apply_filters("enable_post_by_email_configuration", True)):
    wp_die(__("This action has been disabled by the administrator."), 403)
# end if
mailserver_url = get_option("mailserver_url")
if "mail.example.com" == mailserver_url or php_empty(lambda : mailserver_url):
    wp_die(__("This action has been disabled by the administrator."), 403)
# end if
#// 
#// Fires to allow a plugin to do a complete takeover of Post by Email.
#// 
#// @since 2.9.0
#//
do_action("wp-mail.php")
#// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
#// Get the POP3 class with which to access the mailbox.
php_include_file(ABSPATH + WPINC + "/class-pop3.php", once=True)
#// Only check at this interval for new messages.
if (not php_defined("WP_MAIL_INTERVAL")):
    php_define("WP_MAIL_INTERVAL", 5 * MINUTE_IN_SECONDS)
# end if
last_checked = get_transient("mailserver_last_checked")
if last_checked:
    wp_die(__("Slow down cowboy, no need to check for new mails so often!"))
# end if
set_transient("mailserver_last_checked", True, WP_MAIL_INTERVAL)
time_difference = get_option("gmt_offset") * HOUR_IN_SECONDS
phone_delim = "::"
pop3 = php_new_class("POP3", lambda : POP3())
if (not pop3.connect(get_option("mailserver_url"), get_option("mailserver_port"))) or (not pop3.user(get_option("mailserver_login"))):
    wp_die(esc_html(pop3.ERROR))
# end if
count = pop3.pass_(get_option("mailserver_pass"))
if False == count:
    wp_die(esc_html(pop3.ERROR))
# end if
if 0 == count:
    pop3.quit()
    wp_die(__("There doesn&#8217;t seem to be any new mail."))
# end if
i = 1
while i <= count:
    
    message = pop3.get(i)
    bodysignal = False
    boundary = ""
    charset = ""
    content = ""
    content_type = ""
    content_transfer_encoding = ""
    post_author = 1
    author_found = False
    for line in message:
        #// Body signal.
        if php_strlen(line) < 3:
            bodysignal = True
        # end if
        if bodysignal:
            content += line
        else:
            if php_preg_match("/Content-Type: /i", line):
                content_type = php_trim(line)
                content_type = php_substr(content_type, 14, php_strlen(content_type) - 14)
                content_type = php_explode(";", content_type)
                if (not php_empty(lambda : content_type[1])):
                    charset = php_explode("=", content_type[1])
                    charset = php_trim(charset[1]) if (not php_empty(lambda : charset[1])) else ""
                # end if
                content_type = content_type[0]
            # end if
            if php_preg_match("/Content-Transfer-Encoding: /i", line):
                content_transfer_encoding = php_trim(line)
                content_transfer_encoding = php_substr(content_transfer_encoding, 27, php_strlen(content_transfer_encoding) - 27)
                content_transfer_encoding = php_explode(";", content_transfer_encoding)
                content_transfer_encoding = content_transfer_encoding[0]
            # end if
            if "multipart/alternative" == content_type and False != php_strpos(line, "boundary=\"") and "" == boundary:
                boundary = php_trim(line)
                boundary = php_explode("\"", boundary)
                boundary = boundary[1]
            # end if
            if php_preg_match("/Subject: /i", line):
                subject = php_trim(line)
                subject = php_substr(subject, 9, php_strlen(subject) - 9)
                #// Captures any text in the subject before $phone_delim as the subject.
                if php_function_exists("iconv_mime_decode"):
                    subject = iconv_mime_decode(subject, 2, get_option("blog_charset"))
                else:
                    subject = wp_iso_descrambler(subject)
                # end if
                subject = php_explode(phone_delim, subject)
                subject = subject[0]
            # end if
            #// 
            #// Set the author using the email address (From or Reply-To, the last used)
            #// otherwise use the site admin.
            #//
            if (not author_found) and php_preg_match("/^(From|Reply-To): /", line):
                if php_preg_match("|[a-z0-9_.-]+@[a-z0-9_.-]+(?!.*<)|i", line, matches):
                    author = matches[0]
                else:
                    author = php_trim(line)
                # end if
                author = sanitize_email(author)
                if is_email(author):
                    #// translators: %s: Post author email address.
                    php_print("<p>" + php_sprintf(__("Author is %s"), author) + "</p>")
                    userdata = get_user_by("email", author)
                    if (not php_empty(lambda : userdata)):
                        post_author = userdata.ID
                        author_found = True
                    # end if
                # end if
            # end if
            if php_preg_match("/Date: /i", line):
                #// Of the form '20 Mar 2002 20:32:37 +0100'.
                ddate = php_str_replace("Date: ", "", php_trim(line))
                #// Remove parenthesised timezone string if it exists, as this confuses strtotime().
                ddate = php_preg_replace("!\\s*\\(.+\\)\\s*$!", "", ddate)
                ddate_timestamp = strtotime(ddate)
                post_date = gmdate("Y-m-d H:i:s", ddate_timestamp + time_difference)
                post_date_gmt = gmdate("Y-m-d H:i:s", ddate_timestamp)
            # end if
        # end if
    # end for
    #// Set $post_status based on $author_found and on author's publish_posts capability.
    if author_found:
        user = php_new_class("WP_User", lambda : WP_User(post_author))
        post_status = "publish" if user.has_cap("publish_posts") else "pending"
    else:
        #// Author not found in DB, set status to pending. Author already set to admin.
        post_status = "pending"
    # end if
    subject = php_trim(subject)
    if "multipart/alternative" == content_type:
        content = php_explode("--" + boundary, content)
        content = content[2]
        #// Match case-insensitive content-transfer-encoding.
        if php_preg_match("/Content-Transfer-Encoding: quoted-printable/i", content, delim):
            content = php_explode(delim[0], content)
            content = content[1]
        # end if
        content = strip_tags(content, "<img><p><br><i><b><u><em><strong><strike><font><span><div>")
    # end if
    content = php_trim(content)
    #// 
    #// Filters the original content of the email.
    #// 
    #// Give Post-By-Email extending plugins full access to the content, either
    #// the raw content, or the content of the last quoted-printable section.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $content The original email content.
    #//
    content = apply_filters("wp_mail_original_content", content)
    if False != php_stripos(content_transfer_encoding, "quoted-printable"):
        content = quoted_printable_decode(content)
    # end if
    if php_function_exists("iconv") and (not php_empty(lambda : charset)):
        content = iconv(charset, get_option("blog_charset"), content)
    # end if
    #// Captures any text in the body after $phone_delim as the body.
    content = php_explode(phone_delim, content)
    content = content[0] if php_empty(lambda : content[1]) else content[1]
    content = php_trim(content)
    #// 
    #// Filters the content of the post submitted by email before saving.
    #// 
    #// @since 1.2.0
    #// 
    #// @param string $content The email content.
    #//
    post_content = apply_filters("phone_content", content)
    post_title = xmlrpc_getposttitle(content)
    if "" == post_title:
        post_title = subject
    # end if
    post_category = Array(get_option("default_email_category"))
    post_data = compact("post_content", "post_title", "post_date", "post_date_gmt", "post_author", "post_category", "post_status")
    post_data = wp_slash(post_data)
    post_ID = wp_insert_post(post_data)
    if is_wp_error(post_ID):
        php_print("\n" + post_ID.get_error_message())
    # end if
    #// We couldn't post, for whatever reason. Better move forward to the next email.
    if php_empty(lambda : post_ID):
        continue
    # end if
    #// 
    #// Fires after a post submitted by email is published.
    #// 
    #// @since 1.2.0
    #// 
    #// @param int $post_ID The post ID.
    #//
    do_action("publish_phone", post_ID)
    php_print("\n<p><strong>" + __("Author:") + "</strong> " + esc_html(post_author) + "</p>")
    php_print("\n<p><strong>" + __("Posted title:") + "</strong> " + esc_html(post_title) + "</p>")
    if (not pop3.delete(i)):
        php_print("<p>" + php_sprintf(__("Oops: %s"), esc_html(pop3.ERROR)) + "</p>")
        pop3.reset()
        php_exit(0)
    else:
        php_print("<p>" + php_sprintf(__("Mission complete. Message %s deleted."), "<strong>" + i + "</strong>") + "</p>")
    # end if
    i += 1
# end while
pop3.quit()
