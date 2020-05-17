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
mailserver_url_ = get_option("mailserver_url")
if "mail.example.com" == mailserver_url_ or php_empty(lambda : mailserver_url_):
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
last_checked_ = get_transient("mailserver_last_checked")
if last_checked_:
    wp_die(__("Slow down cowboy, no need to check for new mails so often!"))
# end if
set_transient("mailserver_last_checked", True, WP_MAIL_INTERVAL)
time_difference_ = get_option("gmt_offset") * HOUR_IN_SECONDS
phone_delim_ = "::"
pop3_ = php_new_class("POP3", lambda : POP3())
if (not pop3_.connect(get_option("mailserver_url"), get_option("mailserver_port"))) or (not pop3_.user(get_option("mailserver_login"))):
    wp_die(esc_html(pop3_.ERROR))
# end if
count_ = pop3_.pass_(get_option("mailserver_pass"))
if False == count_:
    wp_die(esc_html(pop3_.ERROR))
# end if
if 0 == count_:
    pop3_.quit()
    wp_die(__("There doesn&#8217;t seem to be any new mail."))
# end if
i_ = 1
while i_ <= count_:
    
    message_ = pop3_.get(i_)
    bodysignal_ = False
    boundary_ = ""
    charset_ = ""
    content_ = ""
    content_type_ = ""
    content_transfer_encoding_ = ""
    post_author_ = 1
    author_found_ = False
    for line_ in message_:
        #// Body signal.
        if php_strlen(line_) < 3:
            bodysignal_ = True
        # end if
        if bodysignal_:
            content_ += line_
        else:
            if php_preg_match("/Content-Type: /i", line_):
                content_type_ = php_trim(line_)
                content_type_ = php_substr(content_type_, 14, php_strlen(content_type_) - 14)
                content_type_ = php_explode(";", content_type_)
                if (not php_empty(lambda : content_type_[1])):
                    charset_ = php_explode("=", content_type_[1])
                    charset_ = php_trim(charset_[1]) if (not php_empty(lambda : charset_[1])) else ""
                # end if
                content_type_ = content_type_[0]
            # end if
            if php_preg_match("/Content-Transfer-Encoding: /i", line_):
                content_transfer_encoding_ = php_trim(line_)
                content_transfer_encoding_ = php_substr(content_transfer_encoding_, 27, php_strlen(content_transfer_encoding_) - 27)
                content_transfer_encoding_ = php_explode(";", content_transfer_encoding_)
                content_transfer_encoding_ = content_transfer_encoding_[0]
            # end if
            if "multipart/alternative" == content_type_ and False != php_strpos(line_, "boundary=\"") and "" == boundary_:
                boundary_ = php_trim(line_)
                boundary_ = php_explode("\"", boundary_)
                boundary_ = boundary_[1]
            # end if
            if php_preg_match("/Subject: /i", line_):
                subject_ = php_trim(line_)
                subject_ = php_substr(subject_, 9, php_strlen(subject_) - 9)
                #// Captures any text in the subject before $phone_delim as the subject.
                if php_function_exists("iconv_mime_decode"):
                    subject_ = iconv_mime_decode(subject_, 2, get_option("blog_charset"))
                else:
                    subject_ = wp_iso_descrambler(subject_)
                # end if
                subject_ = php_explode(phone_delim_, subject_)
                subject_ = subject_[0]
            # end if
            #// 
            #// Set the author using the email address (From or Reply-To, the last used)
            #// otherwise use the site admin.
            #//
            if (not author_found_) and php_preg_match("/^(From|Reply-To): /", line_):
                if php_preg_match("|[a-z0-9_.-]+@[a-z0-9_.-]+(?!.*<)|i", line_, matches_):
                    author_ = matches_[0]
                else:
                    author_ = php_trim(line_)
                # end if
                author_ = sanitize_email(author_)
                if is_email(author_):
                    #// translators: %s: Post author email address.
                    php_print("<p>" + php_sprintf(__("Author is %s"), author_) + "</p>")
                    userdata_ = get_user_by("email", author_)
                    if (not php_empty(lambda : userdata_)):
                        post_author_ = userdata_.ID
                        author_found_ = True
                    # end if
                # end if
            # end if
            if php_preg_match("/Date: /i", line_):
                #// Of the form '20 Mar 2002 20:32:37 +0100'.
                ddate_ = php_str_replace("Date: ", "", php_trim(line_))
                #// Remove parenthesised timezone string if it exists, as this confuses strtotime().
                ddate_ = php_preg_replace("!\\s*\\(.+\\)\\s*$!", "", ddate_)
                ddate_timestamp_ = strtotime(ddate_)
                post_date_ = gmdate("Y-m-d H:i:s", ddate_timestamp_ + time_difference_)
                post_date_gmt_ = gmdate("Y-m-d H:i:s", ddate_timestamp_)
            # end if
        # end if
    # end for
    #// Set $post_status based on $author_found and on author's publish_posts capability.
    if author_found_:
        user_ = php_new_class("WP_User", lambda : WP_User(post_author_))
        post_status_ = "publish" if user_.has_cap("publish_posts") else "pending"
    else:
        #// Author not found in DB, set status to pending. Author already set to admin.
        post_status_ = "pending"
    # end if
    subject_ = php_trim(subject_)
    if "multipart/alternative" == content_type_:
        content_ = php_explode("--" + boundary_, content_)
        content_ = content_[2]
        #// Match case-insensitive content-transfer-encoding.
        if php_preg_match("/Content-Transfer-Encoding: quoted-printable/i", content_, delim_):
            content_ = php_explode(delim_[0], content_)
            content_ = content_[1]
        # end if
        content_ = strip_tags(content_, "<img><p><br><i><b><u><em><strong><strike><font><span><div>")
    # end if
    content_ = php_trim(content_)
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
    content_ = apply_filters("wp_mail_original_content", content_)
    if False != php_stripos(content_transfer_encoding_, "quoted-printable"):
        content_ = quoted_printable_decode(content_)
    # end if
    if php_function_exists("iconv") and (not php_empty(lambda : charset_)):
        content_ = iconv(charset_, get_option("blog_charset"), content_)
    # end if
    #// Captures any text in the body after $phone_delim as the body.
    content_ = php_explode(phone_delim_, content_)
    content_ = content_[0] if php_empty(lambda : content_[1]) else content_[1]
    content_ = php_trim(content_)
    #// 
    #// Filters the content of the post submitted by email before saving.
    #// 
    #// @since 1.2.0
    #// 
    #// @param string $content The email content.
    #//
    post_content_ = apply_filters("phone_content", content_)
    post_title_ = xmlrpc_getposttitle(content_)
    if "" == post_title_:
        post_title_ = subject_
    # end if
    post_category_ = Array(get_option("default_email_category"))
    post_data_ = php_compact("post_content_", "post_title_", "post_date_", "post_date_gmt_", "post_author_", "post_category_", "post_status_")
    post_data_ = wp_slash(post_data_)
    post_ID_ = wp_insert_post(post_data_)
    if is_wp_error(post_ID_):
        php_print("\n" + post_ID_.get_error_message())
    # end if
    #// We couldn't post, for whatever reason. Better move forward to the next email.
    if php_empty(lambda : post_ID_):
        continue
    # end if
    #// 
    #// Fires after a post submitted by email is published.
    #// 
    #// @since 1.2.0
    #// 
    #// @param int $post_ID The post ID.
    #//
    do_action("publish_phone", post_ID_)
    php_print("\n<p><strong>" + __("Author:") + "</strong> " + esc_html(post_author_) + "</p>")
    php_print("\n<p><strong>" + __("Posted title:") + "</strong> " + esc_html(post_title_) + "</p>")
    if (not pop3_.delete(i_)):
        php_print("<p>" + php_sprintf(__("Oops: %s"), esc_html(pop3_.ERROR)) + "</p>")
        pop3_.reset()
        php_exit(0)
    else:
        php_print("<p>" + php_sprintf(__("Mission complete. Message %s deleted."), "<strong>" + i_ + "</strong>") + "</p>")
    # end if
    i_ += 1
# end while
pop3_.quit()
