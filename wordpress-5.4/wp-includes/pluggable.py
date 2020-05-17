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
#// These functions can be replaced via plugins. If plugins do not redefine these
#// functions, then these will be used instead.
#// 
#// @package WordPress
#//
if (not php_function_exists("wp_set_current_user")):
    #// 
    #// Changes the current user by ID or name.
    #// 
    #// Set $id to null and specify a name if you do not know a user's ID.
    #// 
    #// Some WordPress functionality is based on the current user and not based on
    #// the signed in user. Therefore, it opens the ability to edit and perform
    #// actions on users who aren't signed in.
    #// 
    #// @since 2.0.3
    #// @global WP_User $current_user The current user object which holds the user data.
    #// 
    #// @param int    $id   User ID
    #// @param string $name User's username
    #// @return WP_User Current user User object
    #//
    def wp_set_current_user(id_=None, name_="", *_args_):
        
        
        global current_user_
        php_check_if_defined("current_user_")
        #// If `$id` matches the current user, there is nothing to do.
        if (php_isset(lambda : current_user_)) and type(current_user_).__name__ == "WP_User" and id_ == current_user_.ID and None != id_:
            return current_user_
        # end if
        current_user_ = php_new_class("WP_User", lambda : WP_User(id_, name_))
        setup_userdata(current_user_.ID)
        #// 
        #// Fires after the current user is set.
        #// 
        #// @since 2.0.1
        #//
        do_action("set_current_user")
        return current_user_
    # end def wp_set_current_user
# end if
if (not php_function_exists("wp_get_current_user")):
    #// 
    #// Retrieve the current user object.
    #// 
    #// Will set the current user, if the current user is not set. The current user
    #// will be set to the logged-in person. If no user is logged-in, then it will
    #// set the current user to 0, which is invalid and won't have any permissions.
    #// 
    #// @since 2.0.3
    #// 
    #// @see _wp_get_current_user()
    #// @global WP_User $current_user Checks if the current user is set.
    #// 
    #// @return WP_User Current WP_User instance.
    #//
    def wp_get_current_user(*_args_):
        
        
        return _wp_get_current_user()
    # end def wp_get_current_user
# end if
if (not php_function_exists("get_userdata")):
    #// 
    #// Retrieve user info by user ID.
    #// 
    #// @since 0.71
    #// 
    #// @param int $user_id User ID
    #// @return WP_User|false WP_User object on success, false on failure.
    #//
    def get_userdata(user_id_=None, *_args_):
        
        
        return get_user_by("id", user_id_)
    # end def get_userdata
# end if
if (not php_function_exists("get_user_by")):
    #// 
    #// Retrieve user info by a given field
    #// 
    #// @since 2.8.0
    #// @since 4.4.0 Added 'ID' as an alias of 'id' for the `$field` parameter.
    #// 
    #// @param string     $field The field to retrieve the user with. id | ID | slug | email | login.
    #// @param int|string $value A value for $field. A user ID, slug, email address, or login name.
    #// @return WP_User|false WP_User object on success, false on failure.
    #//
    def get_user_by(field_=None, value_=None, *_args_):
        
        
        userdata_ = WP_User.get_data_by(field_, value_)
        if (not userdata_):
            return False
        # end if
        user_ = php_new_class("WP_User", lambda : WP_User())
        user_.init(userdata_)
        return user_
    # end def get_user_by
# end if
if (not php_function_exists("cache_users")):
    #// 
    #// Retrieve info for user lists to prevent multiple queries by get_userdata()
    #// 
    #// @since 3.0.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param array $user_ids User ID numbers list
    #//
    def cache_users(user_ids_=None, *_args_):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        clean_ = _get_non_cached_ids(user_ids_, "users")
        if php_empty(lambda : clean_):
            return
        # end if
        list_ = php_implode(",", clean_)
        users_ = wpdb_.get_results(str("SELECT * FROM ") + str(wpdb_.users) + str(" WHERE ID IN (") + str(list_) + str(")"))
        ids_ = Array()
        for user_ in users_:
            update_user_caches(user_)
            ids_[-1] = user_.ID
        # end for
        update_meta_cache("user", ids_)
    # end def cache_users
# end if
if (not php_function_exists("wp_mail")):
    #// 
    #// Sends an email, similar to PHP's mail function.
    #// 
    #// A true return value does not automatically mean that the user received the
    #// email successfully. It just only means that the method used was able to
    #// process the request without any errors.
    #// 
    #// The default content type is `text/plain` which does not allow using HTML.
    #// However, you can set the content type of the email by using the
    #// {@see 'wp_mail_content_type'} filter.
    #// 
    #// The default charset is based on the charset used on the blog. The charset can
    #// be set using the {@see 'wp_mail_charset'} filter.
    #// 
    #// @since 1.2.1
    #// 
    #// @global PHPMailer $phpmailer
    #// 
    #// @param string|array $to          Array or comma-separated list of email addresses to send message.
    #// @param string       $subject     Email subject
    #// @param string       $message     Message contents
    #// @param string|array $headers     Optional. Additional headers.
    #// @param string|array $attachments Optional. Files to attach.
    #// @return bool Whether the email contents were sent successfully.
    #//
    def wp_mail(to_=None, subject_=None, message_=None, headers_="", attachments_=None, *_args_):
        if attachments_ is None:
            attachments_ = Array()
        # end if
        
        #// Compact the input, apply the filters, and extract them back out.
        #// 
        #// Filters the wp_mail() arguments.
        #// 
        #// @since 2.2.0
        #// 
        #// @param array $args A compacted array of wp_mail() arguments, including the "to" email,
        #// subject, message, headers, and attachments values.
        #//
        atts_ = apply_filters("wp_mail", php_compact("to_", "subject_", "message_", "headers_", "attachments_"))
        if (php_isset(lambda : atts_["to"])):
            to_ = atts_["to"]
        # end if
        if (not php_is_array(to_)):
            to_ = php_explode(",", to_)
        # end if
        if (php_isset(lambda : atts_["subject"])):
            subject_ = atts_["subject"]
        # end if
        if (php_isset(lambda : atts_["message"])):
            message_ = atts_["message"]
        # end if
        if (php_isset(lambda : atts_["headers"])):
            headers_ = atts_["headers"]
        # end if
        if (php_isset(lambda : atts_["attachments"])):
            attachments_ = atts_["attachments"]
        # end if
        if (not php_is_array(attachments_)):
            attachments_ = php_explode("\n", php_str_replace("\r\n", "\n", attachments_))
        # end if
        global phpmailer_
        php_check_if_defined("phpmailer_")
        #// (Re)create it, if it's gone missing.
        if (not type(phpmailer_).__name__ == "PHPMailer"):
            php_include_file(ABSPATH + WPINC + "/class-phpmailer.php", once=True)
            php_include_file(ABSPATH + WPINC + "/class-smtp.php", once=True)
            phpmailer_ = php_new_class("PHPMailer", lambda : PHPMailer(True))
        # end if
        #// Headers.
        cc_ = Array()
        bcc_ = Array()
        reply_to_ = Array()
        if php_empty(lambda : headers_):
            headers_ = Array()
        else:
            if (not php_is_array(headers_)):
                #// Explode the headers out, so this function can take
                #// both string headers and an array of headers.
                tempheaders_ = php_explode("\n", php_str_replace("\r\n", "\n", headers_))
            else:
                tempheaders_ = headers_
            # end if
            headers_ = Array()
            #// If it's actually got contents.
            if (not php_empty(lambda : tempheaders_)):
                #// Iterate through the raw headers.
                for header_ in tempheaders_:
                    if php_strpos(header_, ":") == False:
                        if False != php_stripos(header_, "boundary="):
                            parts_ = php_preg_split("/boundary=/i", php_trim(header_))
                            boundary_ = php_trim(php_str_replace(Array("'", "\""), "", parts_[1]))
                        # end if
                        continue
                    # end if
                    #// Explode them out.
                    name_, content_ = php_explode(":", php_trim(header_), 2)
                    #// Cleanup crew.
                    name_ = php_trim(name_)
                    content_ = php_trim(content_)
                    for case in Switch(php_strtolower(name_)):
                        if case("from"):
                            bracket_pos_ = php_strpos(content_, "<")
                            if False != bracket_pos_:
                                #// Text before the bracketed email is the "From" name.
                                if bracket_pos_ > 0:
                                    from_name_ = php_substr(content_, 0, bracket_pos_ - 1)
                                    from_name_ = php_str_replace("\"", "", from_name_)
                                    from_name_ = php_trim(from_name_)
                                # end if
                                from_email_ = php_substr(content_, bracket_pos_ + 1)
                                from_email_ = php_str_replace(">", "", from_email_)
                                from_email_ = php_trim(from_email_)
                                pass
                            elif "" != php_trim(content_):
                                from_email_ = php_trim(content_)
                            # end if
                            break
                        # end if
                        if case("content-type"):
                            if php_strpos(content_, ";") != False:
                                type_, charset_content_ = php_explode(";", content_)
                                content_type_ = php_trim(type_)
                                if False != php_stripos(charset_content_, "charset="):
                                    charset_ = php_trim(php_str_replace(Array("charset=", "\""), "", charset_content_))
                                elif False != php_stripos(charset_content_, "boundary="):
                                    boundary_ = php_trim(php_str_replace(Array("BOUNDARY=", "boundary=", "\""), "", charset_content_))
                                    charset_ = ""
                                # end if
                                pass
                            elif "" != php_trim(content_):
                                content_type_ = php_trim(content_)
                            # end if
                            break
                        # end if
                        if case("cc"):
                            cc_ = php_array_merge(cc_, php_explode(",", content_))
                            break
                        # end if
                        if case("bcc"):
                            bcc_ = php_array_merge(bcc_, php_explode(",", content_))
                            break
                        # end if
                        if case("reply-to"):
                            reply_to_ = php_array_merge(reply_to_, php_explode(",", content_))
                            break
                        # end if
                        if case():
                            #// Add it to our grand headers array.
                            headers_[php_trim(name_)] = php_trim(content_)
                            break
                        # end if
                    # end for
                # end for
            # end if
        # end if
        #// Empty out the values that may be set.
        phpmailer_.clearallrecipients()
        phpmailer_.clearattachments()
        phpmailer_.clearcustomheaders()
        phpmailer_.clearreplytos()
        #// Set "From" name and email.
        #// If we don't have a name from the input headers.
        if (not (php_isset(lambda : from_name_))):
            from_name_ = "WordPress"
        # end if
        #// 
        #// If we don't have an email from the input headers, default to wordpress@$sitename
        #// Some hosts will block outgoing mail from this address if it doesn't exist,
        #// but there's no easy alternative. Defaulting to admin_email might appear to be
        #// another option, but some hosts may refuse to relay mail from an unknown domain.
        #// See https://core.trac.wordpress.org/ticket/5007.
        #//
        if (not (php_isset(lambda : from_email_))):
            #// Get the site domain and get rid of www.
            sitename_ = php_strtolower(PHP_SERVER["SERVER_NAME"])
            if php_substr(sitename_, 0, 4) == "www.":
                sitename_ = php_substr(sitename_, 4)
            # end if
            from_email_ = "wordpress@" + sitename_
        # end if
        #// 
        #// Filters the email address to send from.
        #// 
        #// @since 2.2.0
        #// 
        #// @param string $from_email Email address to send from.
        #//
        from_email_ = apply_filters("wp_mail_from", from_email_)
        #// 
        #// Filters the name to associate with the "from" email address.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $from_name Name associated with the "from" email address.
        #//
        from_name_ = apply_filters("wp_mail_from_name", from_name_)
        try: 
            phpmailer_.setfrom(from_email_, from_name_, False)
        except phpmailerException as e_:
            mail_error_data_ = php_compact("to_", "subject_", "message_", "headers_", "attachments_")
            mail_error_data_["phpmailer_exception_code"] = e_.getcode()
            #// This filter is documented in wp-includes/pluggable.php
            do_action("wp_mail_failed", php_new_class("WP_Error", lambda : WP_Error("wp_mail_failed", e_.getmessage(), mail_error_data_)))
            return False
        # end try
        #// Set mail's subject and body.
        phpmailer_.Subject = subject_
        phpmailer_.Body = message_
        #// Set destination addresses, using appropriate methods for handling addresses.
        address_headers_ = php_compact("to_", "cc_", "bcc_", "reply_to_")
        for address_header_,addresses_ in address_headers_:
            if php_empty(lambda : addresses_):
                continue
            # end if
            for address_ in addresses_:
                try: 
                    #// Break $recipient into name and address parts if in the format "Foo <bar@baz.com>".
                    recipient_name_ = ""
                    if php_preg_match("/(.*)<(.+)>/", address_, matches_):
                        if php_count(matches_) == 3:
                            recipient_name_ = matches_[1]
                            address_ = matches_[2]
                        # end if
                    # end if
                    for case in Switch(address_header_):
                        if case("to"):
                            phpmailer_.addaddress(address_, recipient_name_)
                            break
                        # end if
                        if case("cc"):
                            phpmailer_.addcc(address_, recipient_name_)
                            break
                        # end if
                        if case("bcc"):
                            phpmailer_.addbcc(address_, recipient_name_)
                            break
                        # end if
                        if case("reply_to"):
                            phpmailer_.addreplyto(address_, recipient_name_)
                            break
                        # end if
                    # end for
                except phpmailerException as e_:
                    continue
                # end try
            # end for
        # end for
        #// Set to use PHP's mail().
        phpmailer_.ismail()
        #// Set Content-Type and charset.
        #// If we don't have a content-type from the input headers.
        if (not (php_isset(lambda : content_type_))):
            content_type_ = "text/plain"
        # end if
        #// 
        #// Filters the wp_mail() content type.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $content_type Default wp_mail() content type.
        #//
        content_type_ = apply_filters("wp_mail_content_type", content_type_)
        phpmailer_.ContentType = content_type_
        #// Set whether it's plaintext, depending on $content_type.
        if "text/html" == content_type_:
            phpmailer_.ishtml(True)
        # end if
        #// If we don't have a charset from the input headers.
        if (not (php_isset(lambda : charset_))):
            charset_ = get_bloginfo("charset")
        # end if
        #// 
        #// Filters the default wp_mail() charset.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $charset Default email charset.
        #//
        phpmailer_.CharSet = apply_filters("wp_mail_charset", charset_)
        #// Set custom headers.
        if (not php_empty(lambda : headers_)):
            for name_,content_ in headers_:
                #// Only add custom headers not added automatically by PHPMailer.
                if (not php_in_array(name_, Array("MIME-Version", "X-Mailer"))):
                    phpmailer_.addcustomheader(php_sprintf("%1$s: %2$s", name_, content_))
                # end if
            # end for
            if False != php_stripos(content_type_, "multipart") and (not php_empty(lambda : boundary_)):
                phpmailer_.addcustomheader(php_sprintf("Content-Type: %s;\n  boundary=\"%s\"", content_type_, boundary_))
            # end if
        # end if
        if (not php_empty(lambda : attachments_)):
            for attachment_ in attachments_:
                try: 
                    phpmailer_.addattachment(attachment_)
                except phpmailerException as e_:
                    continue
                # end try
            # end for
        # end if
        #// 
        #// Fires after PHPMailer is initialized.
        #// 
        #// @since 2.2.0
        #// 
        #// @param PHPMailer $phpmailer The PHPMailer instance (passed by reference).
        #//
        do_action_ref_array("phpmailer_init", Array(phpmailer_))
        #// Send!
        try: 
            return phpmailer_.send()
        except phpmailerException as e_:
            mail_error_data_ = php_compact("to_", "subject_", "message_", "headers_", "attachments_")
            mail_error_data_["phpmailer_exception_code"] = e_.getcode()
            #// 
            #// Fires after a phpmailerException is caught.
            #// 
            #// @since 4.4.0
            #// 
            #// @param WP_Error $error A WP_Error object with the phpmailerException message, and an array
            #// containing the mail recipient, subject, message, headers, and attachments.
            #//
            do_action("wp_mail_failed", php_new_class("WP_Error", lambda : WP_Error("wp_mail_failed", e_.getmessage(), mail_error_data_)))
            return False
        # end try
    # end def wp_mail
# end if
if (not php_function_exists("wp_authenticate")):
    #// 
    #// Authenticate a user, confirming the login credentials are valid.
    #// 
    #// @since 2.5.0
    #// @since 4.5.0 `$username` now accepts an email address.
    #// 
    #// @param string $username User's username or email address.
    #// @param string $password User's password.
    #// @return WP_User|WP_Error WP_User object if the credentials are valid,
    #// otherwise WP_Error.
    #//
    def wp_authenticate(username_=None, password_=None, *_args_):
        
        
        username_ = sanitize_user(username_)
        password_ = php_trim(password_)
        #// 
        #// Filters whether a set of user login credentials are valid.
        #// 
        #// A WP_User object is returned if the credentials authenticate a user.
        #// WP_Error or null otherwise.
        #// 
        #// @since 2.8.0
        #// @since 4.5.0 `$username` now accepts an email address.
        #// 
        #// @param null|WP_User|WP_Error $user     WP_User if the user is authenticated.
        #// WP_Error or null otherwise.
        #// @param string                $username Username or email address.
        #// @param string                $password User password
        #//
        user_ = apply_filters("authenticate", None, username_, password_)
        if None == user_:
            #// TODO: What should the error message be? (Or would these even happen?)
            #// Only needed if all authentication handlers fail to return anything.
            user_ = php_new_class("WP_Error", lambda : WP_Error("authentication_failed", __("<strong>Error</strong>: Invalid username, email address or incorrect password.")))
        # end if
        ignore_codes_ = Array("empty_username", "empty_password")
        if is_wp_error(user_) and (not php_in_array(user_.get_error_code(), ignore_codes_)):
            error_ = user_
            #// 
            #// Fires after a user login has failed.
            #// 
            #// @since 2.5.0
            #// @since 4.5.0 The value of `$username` can now be an email address.
            #// @since 5.4.0 The `$error` parameter was added.
            #// 
            #// @param string   $username Username or email address.
            #// @param WP_Error $error    A WP_Error object with the authentication failure details.
            #//
            do_action("wp_login_failed", username_, error_)
        # end if
        return user_
    # end def wp_authenticate
# end if
if (not php_function_exists("wp_logout")):
    #// 
    #// Log the current user out.
    #// 
    #// @since 2.5.0
    #//
    def wp_logout(*_args_):
        
        
        wp_destroy_current_session()
        wp_clear_auth_cookie()
        wp_set_current_user(0)
        #// 
        #// Fires after a user is logged-out.
        #// 
        #// @since 1.5.0
        #//
        do_action("wp_logout")
    # end def wp_logout
# end if
if (not php_function_exists("wp_validate_auth_cookie")):
    #// 
    #// Validates authentication cookie.
    #// 
    #// The checks include making sure that the authentication cookie is set and
    #// pulling in the contents (if $cookie is not used).
    #// 
    #// Makes sure the cookie is not expired. Verifies the hash in cookie is what is
    #// should be and compares the two.
    #// 
    #// @since 2.5.0
    #// 
    #// @global int $login_grace_period
    #// 
    #// @param string $cookie Optional. If used, will validate contents instead of cookie's.
    #// @param string $scheme Optional. The cookie scheme to use: 'auth', 'secure_auth', or 'logged_in'.
    #// @return int|false User ID if valid cookie, false if invalid.
    #//
    def wp_validate_auth_cookie(cookie_="", scheme_="", *_args_):
        
        global PHP_GLOBALS
        cookie_elements_ = wp_parse_auth_cookie(cookie_, scheme_)
        if (not cookie_elements_):
            #// 
            #// Fires if an authentication cookie is malformed.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string $cookie Malformed auth cookie.
            #// @param string $scheme Authentication scheme. Values include 'auth', 'secure_auth',
            #// or 'logged_in'.
            #//
            do_action("auth_cookie_malformed", cookie_, scheme_)
            return False
        # end if
        scheme_ = cookie_elements_["scheme"]
        username_ = cookie_elements_["username"]
        hmac_ = cookie_elements_["hmac"]
        token_ = cookie_elements_["token"]
        expired_ = cookie_elements_["expiration"]
        expiration_ = cookie_elements_["expiration"]
        #// Allow a grace period for POST and Ajax requests.
        if wp_doing_ajax() or "POST" == PHP_SERVER["REQUEST_METHOD"]:
            expired_ += HOUR_IN_SECONDS
        # end if
        #// Quick check to see if an honest cookie has expired.
        if expired_ < time():
            #// 
            #// Fires once an authentication cookie has expired.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_expired", cookie_elements_)
            return False
        # end if
        user_ = get_user_by("login", username_)
        if (not user_):
            #// 
            #// Fires if a bad username is entered in the user authentication process.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_bad_username", cookie_elements_)
            return False
        # end if
        pass_frag_ = php_substr(user_.user_pass, 8, 4)
        key_ = wp_hash(username_ + "|" + pass_frag_ + "|" + expiration_ + "|" + token_, scheme_)
        #// If ext/hash is not present, compat.php's hash_hmac() does not support sha256.
        algo_ = "sha256" if php_function_exists("hash") else "sha1"
        hash_ = hash_hmac(algo_, username_ + "|" + expiration_ + "|" + token_, key_)
        if (not hash_equals(hash_, hmac_)):
            #// 
            #// Fires if a bad authentication cookie hash is encountered.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_bad_hash", cookie_elements_)
            return False
        # end if
        manager_ = WP_Session_Tokens.get_instance(user_.ID)
        if (not manager_.verify(token_)):
            #// 
            #// Fires if a bad session token is encountered.
            #// 
            #// @since 4.0.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_bad_session_token", cookie_elements_)
            return False
        # end if
        #// Ajax/POST grace period set above.
        if expiration_ < time():
            PHP_GLOBALS["login_grace_period"] = 1
        # end if
        #// 
        #// Fires once an authentication cookie has been validated.
        #// 
        #// @since 2.7.0
        #// 
        #// @param string[] $cookie_elements An array of data for the authentication cookie.
        #// @param WP_User  $user            User object.
        #//
        do_action("auth_cookie_valid", cookie_elements_, user_)
        return user_.ID
    # end def wp_validate_auth_cookie
# end if
if (not php_function_exists("wp_generate_auth_cookie")):
    #// 
    #// Generates authentication cookie contents.
    #// 
    #// @since 2.5.0
    #// @since 4.0.0 The `$token` parameter was added.
    #// 
    #// @param int    $user_id    User ID.
    #// @param int    $expiration The time the cookie expires as a UNIX timestamp.
    #// @param string $scheme     Optional. The cookie scheme to use: 'auth', 'secure_auth', or 'logged_in'.
    #// Default 'auth'.
    #// @param string $token      User's session token to use for this cookie.
    #// @return string Authentication cookie contents. Empty string if user does not exist.
    #//
    def wp_generate_auth_cookie(user_id_=None, expiration_=None, scheme_="auth", token_="", *_args_):
        
        
        user_ = get_userdata(user_id_)
        if (not user_):
            return ""
        # end if
        if (not token_):
            manager_ = WP_Session_Tokens.get_instance(user_id_)
            token_ = manager_.create(expiration_)
        # end if
        pass_frag_ = php_substr(user_.user_pass, 8, 4)
        key_ = wp_hash(user_.user_login + "|" + pass_frag_ + "|" + expiration_ + "|" + token_, scheme_)
        #// If ext/hash is not present, compat.php's hash_hmac() does not support sha256.
        algo_ = "sha256" if php_function_exists("hash") else "sha1"
        hash_ = hash_hmac(algo_, user_.user_login + "|" + expiration_ + "|" + token_, key_)
        cookie_ = user_.user_login + "|" + expiration_ + "|" + token_ + "|" + hash_
        #// 
        #// Filters the authentication cookie.
        #// 
        #// @since 2.5.0
        #// @since 4.0.0 The `$token` parameter was added.
        #// 
        #// @param string $cookie     Authentication cookie.
        #// @param int    $user_id    User ID.
        #// @param int    $expiration The time the cookie expires as a UNIX timestamp.
        #// @param string $scheme     Cookie scheme used. Accepts 'auth', 'secure_auth', or 'logged_in'.
        #// @param string $token      User's session token used.
        #//
        return apply_filters("auth_cookie", cookie_, user_id_, expiration_, scheme_, token_)
    # end def wp_generate_auth_cookie
# end if
if (not php_function_exists("wp_parse_auth_cookie")):
    #// 
    #// Parses a cookie into its components.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $cookie Authentication cookie.
    #// @param string $scheme Optional. The cookie scheme to use: 'auth', 'secure_auth', or 'logged_in'.
    #// @return string[]|false Authentication cookie components.
    #//
    def wp_parse_auth_cookie(cookie_="", scheme_="", *_args_):
        
        
        if php_empty(lambda : cookie_):
            for case in Switch(scheme_):
                if case("auth"):
                    cookie_name_ = AUTH_COOKIE
                    break
                # end if
                if case("secure_auth"):
                    cookie_name_ = SECURE_AUTH_COOKIE
                    break
                # end if
                if case("logged_in"):
                    cookie_name_ = LOGGED_IN_COOKIE
                    break
                # end if
                if case():
                    if is_ssl():
                        cookie_name_ = SECURE_AUTH_COOKIE
                        scheme_ = "secure_auth"
                    else:
                        cookie_name_ = AUTH_COOKIE
                        scheme_ = "auth"
                    # end if
                # end if
            # end for
            if php_empty(lambda : PHP_COOKIE[cookie_name_]):
                return False
            # end if
            cookie_ = PHP_COOKIE[cookie_name_]
        # end if
        cookie_elements_ = php_explode("|", cookie_)
        if php_count(cookie_elements_) != 4:
            return False
        # end if
        username_, expiration_, token_, hmac_ = cookie_elements_
        return php_compact("username_", "expiration_", "token_", "hmac_", "scheme_")
    # end def wp_parse_auth_cookie
# end if
if (not php_function_exists("wp_set_auth_cookie")):
    #// 
    #// Sets the authentication cookies based on user ID.
    #// 
    #// The $remember parameter increases the time that the cookie will be kept. The
    #// default the cookie is kept without remembering is two days. When $remember is
    #// set, the cookies will be kept for 14 days or two weeks.
    #// 
    #// @since 2.5.0
    #// @since 4.3.0 Added the `$token` parameter.
    #// 
    #// @param int         $user_id  User ID.
    #// @param bool        $remember Whether to remember the user.
    #// @param bool|string $secure   Whether the auth cookie should only be sent over HTTPS. Default is an empty
    #// string which means the value of `is_ssl()` will be used.
    #// @param string      $token    Optional. User's session token to use for this cookie.
    #//
    def wp_set_auth_cookie(user_id_=None, remember_=None, secure_="", token_="", *_args_):
        if remember_ is None:
            remember_ = False
        # end if
        
        if remember_:
            #// 
            #// Filters the duration of the authentication cookie expiration period.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int  $length   Duration of the expiration period in seconds.
            #// @param int  $user_id  User ID.
            #// @param bool $remember Whether to remember the user login. Default false.
            #//
            expiration_ = time() + apply_filters("auth_cookie_expiration", 14 * DAY_IN_SECONDS, user_id_, remember_)
            #// 
            #// Ensure the browser will continue to send the cookie after the expiration time is reached.
            #// Needed for the login grace period in wp_validate_auth_cookie().
            #//
            expire_ = expiration_ + 12 * HOUR_IN_SECONDS
        else:
            #// This filter is documented in wp-includes/pluggable.php
            expiration_ = time() + apply_filters("auth_cookie_expiration", 2 * DAY_IN_SECONDS, user_id_, remember_)
            expire_ = 0
        # end if
        if "" == secure_:
            secure_ = is_ssl()
        # end if
        #// Front-end cookie is secure when the auth cookie is secure and the site's home URL uses HTTPS.
        secure_logged_in_cookie_ = secure_ and "https" == php_parse_url(get_option("home"), PHP_URL_SCHEME)
        #// 
        #// Filters whether the auth cookie should only be sent over HTTPS.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool $secure  Whether the cookie should only be sent over HTTPS.
        #// @param int  $user_id User ID.
        #//
        secure_ = apply_filters("secure_auth_cookie", secure_, user_id_)
        #// 
        #// Filters whether the logged in cookie should only be sent over HTTPS.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool $secure_logged_in_cookie Whether the logged in cookie should only be sent over HTTPS.
        #// @param int  $user_id                 User ID.
        #// @param bool $secure                  Whether the auth cookie should only be sent over HTTPS.
        #//
        secure_logged_in_cookie_ = apply_filters("secure_logged_in_cookie", secure_logged_in_cookie_, user_id_, secure_)
        if secure_:
            auth_cookie_name_ = SECURE_AUTH_COOKIE
            scheme_ = "secure_auth"
        else:
            auth_cookie_name_ = AUTH_COOKIE
            scheme_ = "auth"
        # end if
        if "" == token_:
            manager_ = WP_Session_Tokens.get_instance(user_id_)
            token_ = manager_.create(expiration_)
        # end if
        auth_cookie_ = wp_generate_auth_cookie(user_id_, expiration_, scheme_, token_)
        logged_in_cookie_ = wp_generate_auth_cookie(user_id_, expiration_, "logged_in", token_)
        #// 
        #// Fires immediately before the authentication cookie is set.
        #// 
        #// @since 2.5.0
        #// @since 4.9.0 The `$token` parameter was added.
        #// 
        #// @param string $auth_cookie Authentication cookie value.
        #// @param int    $expire      The time the login grace period expires as a UNIX timestamp.
        #// Default is 12 hours past the cookie's expiration time.
        #// @param int    $expiration  The time when the authentication cookie expires as a UNIX timestamp.
        #// Default is 14 days from now.
        #// @param int    $user_id     User ID.
        #// @param string $scheme      Authentication scheme. Values include 'auth' or 'secure_auth'.
        #// @param string $token       User's session token to use for this cookie.
        #//
        do_action("set_auth_cookie", auth_cookie_, expire_, expiration_, user_id_, scheme_, token_)
        #// 
        #// Fires immediately before the logged-in authentication cookie is set.
        #// 
        #// @since 2.6.0
        #// @since 4.9.0 The `$token` parameter was added.
        #// 
        #// @param string $logged_in_cookie The logged-in cookie value.
        #// @param int    $expire           The time the login grace period expires as a UNIX timestamp.
        #// Default is 12 hours past the cookie's expiration time.
        #// @param int    $expiration       The time when the logged-in authentication cookie expires as a UNIX timestamp.
        #// Default is 14 days from now.
        #// @param int    $user_id          User ID.
        #// @param string $scheme           Authentication scheme. Default 'logged_in'.
        #// @param string $token            User's session token to use for this cookie.
        #//
        do_action("set_logged_in_cookie", logged_in_cookie_, expire_, expiration_, user_id_, "logged_in", token_)
        #// 
        #// Allows preventing auth cookies from actually being sent to the client.
        #// 
        #// @since 4.7.4
        #// 
        #// @param bool $send Whether to send auth cookies to the client.
        #//
        if (not apply_filters("send_auth_cookies", True)):
            return
        # end if
        setcookie(auth_cookie_name_, auth_cookie_, expire_, PLUGINS_COOKIE_PATH, COOKIE_DOMAIN, secure_, True)
        setcookie(auth_cookie_name_, auth_cookie_, expire_, ADMIN_COOKIE_PATH, COOKIE_DOMAIN, secure_, True)
        setcookie(LOGGED_IN_COOKIE, logged_in_cookie_, expire_, COOKIEPATH, COOKIE_DOMAIN, secure_logged_in_cookie_, True)
        if COOKIEPATH != SITECOOKIEPATH:
            setcookie(LOGGED_IN_COOKIE, logged_in_cookie_, expire_, SITECOOKIEPATH, COOKIE_DOMAIN, secure_logged_in_cookie_, True)
        # end if
    # end def wp_set_auth_cookie
# end if
if (not php_function_exists("wp_clear_auth_cookie")):
    #// 
    #// Removes all of the cookies associated with authentication.
    #// 
    #// @since 2.5.0
    #//
    def wp_clear_auth_cookie(*_args_):
        
        
        #// 
        #// Fires just before the authentication cookies are cleared.
        #// 
        #// @since 2.7.0
        #//
        do_action("clear_auth_cookie")
        #// This filter is documented in wp-includes/pluggable.php
        if (not apply_filters("send_auth_cookies", True)):
            return
        # end if
        #// Auth cookies.
        setcookie(AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, ADMIN_COOKIE_PATH, COOKIE_DOMAIN)
        setcookie(SECURE_AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, ADMIN_COOKIE_PATH, COOKIE_DOMAIN)
        setcookie(AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, PLUGINS_COOKIE_PATH, COOKIE_DOMAIN)
        setcookie(SECURE_AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, PLUGINS_COOKIE_PATH, COOKIE_DOMAIN)
        setcookie(LOGGED_IN_COOKIE, " ", time() - YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN)
        setcookie(LOGGED_IN_COOKIE, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH, COOKIE_DOMAIN)
        #// Settings cookies.
        setcookie("wp-settings-" + get_current_user_id(), " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH)
        setcookie("wp-settings-time-" + get_current_user_id(), " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH)
        #// Old cookies.
        setcookie(AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN)
        setcookie(AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH, COOKIE_DOMAIN)
        setcookie(SECURE_AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN)
        setcookie(SECURE_AUTH_COOKIE, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH, COOKIE_DOMAIN)
        #// Even older cookies.
        setcookie(USER_COOKIE, " ", time() - YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN)
        setcookie(PASS_COOKIE, " ", time() - YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN)
        setcookie(USER_COOKIE, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH, COOKIE_DOMAIN)
        setcookie(PASS_COOKIE, " ", time() - YEAR_IN_SECONDS, SITECOOKIEPATH, COOKIE_DOMAIN)
        #// Post password cookie.
        setcookie("wp-postpass_" + COOKIEHASH, " ", time() - YEAR_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN)
    # end def wp_clear_auth_cookie
# end if
if (not php_function_exists("is_user_logged_in")):
    #// 
    #// Determines whether the current visitor is a logged in user.
    #// 
    #// For more information on this and similar theme functions, check out
    #// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
    #// Conditional Tags} article in the Theme Developer Handbook.
    #// 
    #// @since 2.0.0
    #// 
    #// @return bool True if user is logged in, false if not logged in.
    #//
    def is_user_logged_in(*_args_):
        
        
        user_ = wp_get_current_user()
        return user_.exists()
    # end def is_user_logged_in
# end if
if (not php_function_exists("auth_redirect")):
    #// 
    #// Checks if a user is logged in, if not it redirects them to the login page.
    #// 
    #// When this code is called from a page, it checks to see if the user viewing the page is logged in.
    #// If the user is not logged in, they are redirected to the login page. The user is redirected
    #// in such a way that, upon logging in, they will be sent directly to the page they were originally
    #// trying to access.
    #// 
    #// @since 1.5.0
    #//
    def auth_redirect(*_args_):
        
        
        secure_ = is_ssl() or force_ssl_admin()
        #// 
        #// Filters whether to use a secure authentication redirect.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool $secure Whether to use a secure authentication redirect. Default false.
        #//
        secure_ = apply_filters("secure_auth_redirect", secure_)
        #// If https is required and request is http, redirect.
        if secure_ and (not is_ssl()) and False != php_strpos(PHP_SERVER["REQUEST_URI"], "wp-admin"):
            if 0 == php_strpos(PHP_SERVER["REQUEST_URI"], "http"):
                wp_redirect(set_url_scheme(PHP_SERVER["REQUEST_URI"], "https"))
                php_exit(0)
            else:
                wp_redirect("https://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
                php_exit(0)
            # end if
        # end if
        #// 
        #// Filters the authentication redirect scheme.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string $scheme Authentication redirect scheme. Default empty.
        #//
        scheme_ = apply_filters("auth_redirect_scheme", "")
        user_id_ = wp_validate_auth_cookie("", scheme_)
        if user_id_:
            #// 
            #// Fires before the authentication redirect.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int $user_id User ID.
            #//
            do_action("auth_redirect", user_id_)
            #// If the user wants ssl but the session is not ssl, redirect.
            if (not secure_) and get_user_option("use_ssl", user_id_) and False != php_strpos(PHP_SERVER["REQUEST_URI"], "wp-admin"):
                if 0 == php_strpos(PHP_SERVER["REQUEST_URI"], "http"):
                    wp_redirect(set_url_scheme(PHP_SERVER["REQUEST_URI"], "https"))
                    php_exit(0)
                else:
                    wp_redirect("https://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
                    php_exit(0)
                # end if
            # end if
            return
            pass
        # end if
        #// The cookie is no good, so force login.
        nocache_headers()
        redirect_ = wp_get_referer() if php_strpos(PHP_SERVER["REQUEST_URI"], "/options.php") and wp_get_referer() else set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
        login_url_ = wp_login_url(redirect_, True)
        wp_redirect(login_url_)
        php_exit(0)
    # end def auth_redirect
# end if
if (not php_function_exists("check_admin_referer")):
    #// 
    #// Ensures intent by verifying that a user was referred from another admin page with the correct security nonce.
    #// 
    #// This function ensures the user intends to perform a given action, which helps protect against clickjacking style
    #// attacks. It verifies intent, not authorisation, therefore it does not verify the user's capabilities. This should
    #// be performed with `current_user_can()` or similar.
    #// 
    #// If the nonce value is invalid, the function will exit with an "Are You Sure?" style message.
    #// 
    #// @since 1.2.0
    #// @since 2.5.0 The `$query_arg` parameter was added.
    #// 
    #// @param int|string $action    The nonce action.
    #// @param string     $query_arg Optional. Key to check for nonce in `$_REQUEST`. Default '_wpnonce'.
    #// @return int|false 1 if the nonce is valid and generated between 0-12 hours ago,
    #// 2 if the nonce is valid and generated between 12-24 hours ago.
    #// False if the nonce is invalid.
    #//
    def check_admin_referer(action_=None, query_arg_="_wpnonce", *_args_):
        if action_ is None:
            action_ = -1
        # end if
        
        if -1 == action_:
            _doing_it_wrong(__FUNCTION__, __("You should specify a nonce action to be verified by using the first parameter."), "3.2.0")
        # end if
        adminurl_ = php_strtolower(admin_url())
        referer_ = php_strtolower(wp_get_referer())
        result_ = wp_verify_nonce(PHP_REQUEST[query_arg_], action_) if (php_isset(lambda : PHP_REQUEST[query_arg_])) else False
        #// 
        #// Fires once the admin request has been validated or not.
        #// 
        #// @since 1.5.1
        #// 
        #// @param string    $action The nonce action.
        #// @param false|int $result False if the nonce is invalid, 1 if the nonce is valid and generated between
        #// 0-12 hours ago, 2 if the nonce is valid and generated between 12-24 hours ago.
        #//
        do_action("check_admin_referer", action_, result_)
        if (not result_) and (not -1 == action_ and php_strpos(referer_, adminurl_) == 0):
            wp_nonce_ays(action_)
            php_exit(0)
        # end if
        return result_
    # end def check_admin_referer
# end if
if (not php_function_exists("check_ajax_referer")):
    #// 
    #// Verifies the Ajax request to prevent processing requests external of the blog.
    #// 
    #// @since 2.0.3
    #// 
    #// @param int|string   $action    Action nonce.
    #// @param false|string $query_arg Optional. Key to check for the nonce in `$_REQUEST` (since 2.5). If false,
    #// `$_REQUEST` values will be evaluated for '_ajax_nonce', and '_wpnonce'
    #// (in that order). Default false.
    #// @param bool         $die       Optional. Whether to die early when the nonce cannot be verified.
    #// Default true.
    #// @return int|false 1 if the nonce is valid and generated between 0-12 hours ago,
    #// 2 if the nonce is valid and generated between 12-24 hours ago.
    #// False if the nonce is invalid.
    #//
    def check_ajax_referer(action_=None, query_arg_=None, die_=None, *_args_):
        if action_ is None:
            action_ = -1
        # end if
        if query_arg_ is None:
            query_arg_ = False
        # end if
        if die_ is None:
            die_ = True
        # end if
        
        if -1 == action_:
            _doing_it_wrong(__FUNCTION__, __("You should specify a nonce action to be verified by using the first parameter."), "4.7")
        # end if
        nonce_ = ""
        if query_arg_ and (php_isset(lambda : PHP_REQUEST[query_arg_])):
            nonce_ = PHP_REQUEST[query_arg_]
        elif (php_isset(lambda : PHP_REQUEST["_ajax_nonce"])):
            nonce_ = PHP_REQUEST["_ajax_nonce"]
        elif (php_isset(lambda : PHP_REQUEST["_wpnonce"])):
            nonce_ = PHP_REQUEST["_wpnonce"]
        # end if
        result_ = wp_verify_nonce(nonce_, action_)
        #// 
        #// Fires once the Ajax request has been validated or not.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string    $action The Ajax nonce action.
        #// @param false|int $result False if the nonce is invalid, 1 if the nonce is valid and generated between
        #// 0-12 hours ago, 2 if the nonce is valid and generated between 12-24 hours ago.
        #//
        do_action("check_ajax_referer", action_, result_)
        if die_ and False == result_:
            if wp_doing_ajax():
                wp_die(-1, 403)
            else:
                php_print("-1")
                php_exit()
            # end if
        # end if
        return result_
    # end def check_ajax_referer
# end if
if (not php_function_exists("wp_redirect")):
    #// 
    #// Redirects to another page.
    #// 
    #// Note: wp_redirect() does not exit automatically, and should almost always be
    #// followed by a call to `exit;`:
    #// 
    #// wp_redirect( $url );
    #// exit;
    #// 
    #// Exiting can also be selectively manipulated by using wp_redirect() as a conditional
    #// in conjunction with the {@see 'wp_redirect'} and {@see 'wp_redirect_location'} filters:
    #// 
    #// if ( wp_redirect( $url ) ) {
    #// exit;
    #// }
    #// 
    #// @since 1.5.1
    #// @since 5.1.0 The `$x_redirect_by` parameter was added.
    #// @since 5.4.0 On invalid status codes, wp_die() is called.
    #// 
    #// @global bool $is_IIS
    #// 
    #// @param string $location      The path or URL to redirect to.
    #// @param int    $status        Optional. HTTP response status code to use. Default '302' (Moved Temporarily).
    #// @param string $x_redirect_by Optional. The application doing the redirect. Default 'WordPress'.
    #// @return bool False if the redirect was cancelled, true otherwise.
    #//
    def wp_redirect(location_=None, status_=302, x_redirect_by_="WordPress", *_args_):
        
        
        global is_IIS_
        php_check_if_defined("is_IIS_")
        #// 
        #// Filters the redirect location.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $location The path or URL to redirect to.
        #// @param int    $status   The HTTP response status code to use.
        #//
        location_ = apply_filters("wp_redirect", location_, status_)
        #// 
        #// Filters the redirect HTTP response status code to use.
        #// 
        #// @since 2.3.0
        #// 
        #// @param int    $status   The HTTP response status code to use.
        #// @param string $location The path or URL to redirect to.
        #//
        status_ = apply_filters("wp_redirect_status", status_, location_)
        if (not location_):
            return False
        # end if
        if status_ < 300 or 399 < status_:
            wp_die(__("HTTP redirect status code must be a redirection code, 3xx."))
        # end if
        location_ = wp_sanitize_redirect(location_)
        if (not is_IIS_) and PHP_SAPI != "cgi-fcgi":
            status_header(status_)
            pass
        # end if
        #// 
        #// Filters the X-Redirect-By header.
        #// 
        #// Allows applications to identify themselves when they're doing a redirect.
        #// 
        #// @since 5.1.0
        #// 
        #// @param string $x_redirect_by The application doing the redirect.
        #// @param int    $status        Status code to use.
        #// @param string $location      The path to redirect to.
        #//
        x_redirect_by_ = apply_filters("x_redirect_by", x_redirect_by_, status_, location_)
        if php_is_string(x_redirect_by_):
            php_header(str("X-Redirect-By: ") + str(x_redirect_by_))
        # end if
        php_header(str("Location: ") + str(location_), True, status_)
        return True
    # end def wp_redirect
# end if
if (not php_function_exists("wp_sanitize_redirect")):
    #// 
    #// Sanitizes a URL for use in a redirect.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $location The path to redirect to.
    #// @return string Redirect-sanitized URL.
    #//
    def wp_sanitize_redirect(location_=None, *_args_):
        
        
        #// Encode spaces.
        location_ = php_str_replace(" ", "%20", location_)
        regex_ = """/
        (
        (?: [\\xC2-\\xDF][\\x80-\\xBF]        # double-byte sequences   110xxxxx 10xxxxxx
        |   \\xE0[\\xA0-\\xBF][\\x80-\\xBF]    # triple-byte sequences   1110xxxx 10xxxxxx * 2
        |   [\\xE1-\\xEC][\\x80-\\xBF]{2}
        |   \\xED[\\x80-\\x9F][\\x80-\\xBF]
        |   [\\xEE-\\xEF][\\x80-\\xBF]{2}
        |   \\xF0[\\x90-\\xBF][\\x80-\\xBF]{2} # four-byte sequences   11110xxx 10xxxxxx * 3
        |   [\\xF1-\\xF3][\\x80-\\xBF]{3}
        |   \\xF4[\\x80-\\x8F][\\x80-\\xBF]{2}
        ){1,40}                              # ...one or more times
        )/x"""
        location_ = preg_replace_callback(regex_, "_wp_sanitize_utf8_in_redirect", location_)
        location_ = php_preg_replace("|[^a-z0-9-~+_.?#=&;,/:%!*\\[\\]()@]|i", "", location_)
        location_ = wp_kses_no_null(location_)
        #// Remove %0D and %0A from location.
        strip_ = Array("%0d", "%0a", "%0D", "%0A")
        return _deep_replace(strip_, location_)
    # end def wp_sanitize_redirect
    #// 
    #// URL encode UTF-8 characters in a URL.
    #// 
    #// @ignore
    #// @since 4.2.0
    #// @access private
    #// 
    #// @see wp_sanitize_redirect()
    #// 
    #// @param array $matches RegEx matches against the redirect location.
    #// @return string URL-encoded version of the first RegEx match.
    #//
    def _wp_sanitize_utf8_in_redirect(matches_=None, *_args_):
        
        
        return urlencode(matches_[0])
    # end def _wp_sanitize_utf8_in_redirect
# end if
if (not php_function_exists("wp_safe_redirect")):
    #// 
    #// Performs a safe (local) redirect, using wp_redirect().
    #// 
    #// Checks whether the $location is using an allowed host, if it has an absolute
    #// path. A plugin can therefore set or remove allowed host(s) to or from the
    #// list.
    #// 
    #// If the host is not allowed, then the redirect defaults to wp-admin on the siteurl
    #// instead. This prevents malicious redirects which redirect to another host,
    #// but only used in a few places.
    #// 
    #// Note: wp_safe_redirect() does not exit automatically, and should almost always be
    #// followed by a call to `exit;`:
    #// 
    #// wp_safe_redirect( $url );
    #// exit;
    #// 
    #// Exiting can also be selectively manipulated by using wp_safe_redirect() as a conditional
    #// in conjunction with the {@see 'wp_redirect'} and {@see 'wp_redirect_location'} filters:
    #// 
    #// if ( wp_safe_redirect( $url ) ) {
    #// exit;
    #// }
    #// 
    #// @since 2.3.0
    #// @since 5.1.0 The return value from wp_redirect() is now passed on, and the `$x_redirect_by` parameter was added.
    #// 
    #// @param string $location      The path or URL to redirect to.
    #// @param int    $status        Optional. HTTP response status code to use. Default '302' (Moved Temporarily).
    #// @param string $x_redirect_by Optional. The application doing the redirect. Default 'WordPress'.
    #// @return bool  $redirect False if the redirect was cancelled, true otherwise.
    #//
    def wp_safe_redirect(location_=None, status_=302, x_redirect_by_="WordPress", *_args_):
        
        
        #// Need to look at the URL the way it will end up in wp_redirect().
        location_ = wp_sanitize_redirect(location_)
        #// 
        #// Filters the redirect fallback URL for when the provided redirect is not safe (local).
        #// 
        #// @since 4.3.0
        #// 
        #// @param string $fallback_url The fallback URL to use by default.
        #// @param int    $status       The HTTP response status code to use.
        #//
        location_ = wp_validate_redirect(location_, apply_filters("wp_safe_redirect_fallback", admin_url(), status_))
        return wp_redirect(location_, status_, x_redirect_by_)
    # end def wp_safe_redirect
# end if
if (not php_function_exists("wp_validate_redirect")):
    #// 
    #// Validates a URL for use in a redirect.
    #// 
    #// Checks whether the $location is using an allowed host, if it has an absolute
    #// path. A plugin can therefore set or remove allowed host(s) to or from the
    #// list.
    #// 
    #// If the host is not allowed, then the redirect is to $default supplied
    #// 
    #// @since 2.8.1
    #// 
    #// @param string $location The redirect to validate
    #// @param string $default  The value to return if $location is not allowed
    #// @return string redirect-sanitized URL
    #//
    def wp_validate_redirect(location_=None, default_="", *_args_):
        
        
        location_ = php_trim(location_, "   \n\r ")
        #// Browsers will assume 'http' is your protocol, and will obey a redirect to a URL starting with '//'.
        if php_substr(location_, 0, 2) == "//":
            location_ = "http:" + location_
        # end if
        #// In PHP 5 parse_url() may fail if the URL query part contains 'http://'.
        #// See https://bugs.php.net/bug.php?id=38143
        cut_ = php_strpos(location_, "?")
        test_ = php_substr(location_, 0, cut_) if cut_ else location_
        #// @-operator is used to prevent possible warnings in PHP < 5.3.3.
        lp_ = php_no_error(lambda: php_parse_url(test_))
        #// Give up if malformed URL.
        if False == lp_:
            return default_
        # end if
        #// Allow only 'http' and 'https' schemes. No 'data:', etc.
        if (php_isset(lambda : lp_["scheme"])) and (not "http" == lp_["scheme"] or "https" == lp_["scheme"]):
            return default_
        # end if
        if (not (php_isset(lambda : lp_["host"]))) and (not php_empty(lambda : lp_["path"])) and "/" != lp_["path"][0]:
            path_ = ""
            if (not php_empty(lambda : PHP_SERVER["REQUEST_URI"])):
                path_ = php_dirname(php_parse_url("http://placeholder" + PHP_SERVER["REQUEST_URI"], PHP_URL_PATH) + "?")
                path_ = wp_normalize_path(path_)
            # end if
            location_ = "/" + php_ltrim(path_ + "/", "/") + location_
        # end if
        #// Reject if certain components are set but host is not.
        #// This catches URLs like https:host.com for which parse_url() does not set the host field.
        if (not (php_isset(lambda : lp_["host"]))) and (php_isset(lambda : lp_["scheme"])) or (php_isset(lambda : lp_["user"])) or (php_isset(lambda : lp_["pass"])) or (php_isset(lambda : lp_["port"])):
            return default_
        # end if
        #// Reject malformed components parse_url() can return on odd inputs.
        for component_ in Array("user", "pass", "host"):
            if (php_isset(lambda : lp_[component_])) and strpbrk(lp_[component_], ":/?#@"):
                return default_
            # end if
        # end for
        wpp_ = php_parse_url(home_url())
        #// 
        #// Filters the whitelist of hosts to redirect to.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string[] $hosts An array of allowed host names.
        #// @param string   $host  The host name of the redirect destination; empty string if not set.
        #//
        allowed_hosts_ = apply_filters("allowed_redirect_hosts", Array(wpp_["host"]), lp_["host"] if (php_isset(lambda : lp_["host"])) else "")
        if (php_isset(lambda : lp_["host"])) and (not php_in_array(lp_["host"], allowed_hosts_)) and php_strtolower(wpp_["host"]) != lp_["host"]:
            location_ = default_
        # end if
        return location_
    # end def wp_validate_redirect
# end if
if (not php_function_exists("wp_notify_postauthor")):
    #// 
    #// Notify an author (and/or others) of a comment/trackback/pingback on a post.
    #// 
    #// @since 1.0.0
    #// 
    #// @param int|WP_Comment  $comment_id Comment ID or WP_Comment object.
    #// @param string          $deprecated Not used
    #// @return bool True on completion. False if no email addresses were specified.
    #//
    def wp_notify_postauthor(comment_id_=None, deprecated_=None, *_args_):
        if deprecated_ is None:
            deprecated_ = None
        # end if
        
        if None != deprecated_:
            _deprecated_argument(__FUNCTION__, "3.8.0")
        # end if
        comment_ = get_comment(comment_id_)
        if php_empty(lambda : comment_) or php_empty(lambda : comment_.comment_post_ID):
            return False
        # end if
        post_ = get_post(comment_.comment_post_ID)
        author_ = get_userdata(post_.post_author)
        #// Who to notify? By default, just the post author, but others can be added.
        emails_ = Array()
        if author_:
            emails_[-1] = author_.user_email
        # end if
        #// 
        #// Filters the list of email addresses to receive a comment notification.
        #// 
        #// By default, only post authors are notified of comments. This filter allows
        #// others to be added.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string[] $emails     An array of email addresses to receive a comment notification.
        #// @param int      $comment_id The comment ID.
        #//
        emails_ = apply_filters("comment_notification_recipients", emails_, comment_.comment_ID)
        emails_ = php_array_filter(emails_)
        #// If there are no addresses to send the comment to, bail.
        if (not php_count(emails_)):
            return False
        # end if
        #// Facilitate unsetting below without knowing the keys.
        emails_ = php_array_flip(emails_)
        #// 
        #// Filters whether to notify comment authors of their comments on their own posts.
        #// 
        #// By default, comment authors aren't notified of their comments on their own
        #// posts. This filter allows you to override that.
        #// 
        #// @since 3.8.0
        #// 
        #// @param bool $notify     Whether to notify the post author of their own comment.
        #// Default false.
        #// @param int  $comment_id The comment ID.
        #//
        notify_author_ = apply_filters("comment_notification_notify_author", False, comment_.comment_ID)
        #// The comment was left by the author.
        if author_ and (not notify_author_) and comment_.user_id == post_.post_author:
            emails_[author_.user_email] = None
        # end if
        #// The author moderated a comment on their own post.
        if author_ and (not notify_author_) and get_current_user_id() == post_.post_author:
            emails_[author_.user_email] = None
        # end if
        #// The post author is no longer a member of the blog.
        if author_ and (not notify_author_) and (not user_can(post_.post_author, "read_post", post_.ID)):
            emails_[author_.user_email] = None
        # end if
        #// If there's no email to send the comment to, bail, otherwise flip array back around for use below.
        if (not php_count(emails_)):
            return False
        else:
            emails_ = php_array_flip(emails_)
        # end if
        switched_locale_ = switch_to_locale(get_locale())
        comment_author_domain_ = ""
        if WP_Http.is_ip_address(comment_.comment_author_IP):
            comment_author_domain_ = gethostbyaddr(comment_.comment_author_IP)
        # end if
        #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
        #// We want to reverse this for the plain text arena of emails.
        blogname_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        comment_content_ = wp_specialchars_decode(comment_.comment_content)
        for case in Switch(comment_.comment_type):
            if case("trackback"):
                #// translators: %s: Post title.
                notify_message_ = php_sprintf(__("New trackback on your post \"%s\""), post_.post_title) + "\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message_ += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment_.comment_author, comment_.comment_author_IP, comment_author_domain_) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message_ += php_sprintf(__("URL: %s"), comment_.comment_author_url) + "\r\n"
                #// translators: %s: Comment text.
                notify_message_ += php_sprintf(__("Comment: %s"), "\r\n" + comment_content_) + "\r\n\r\n"
                notify_message_ += __("You can see all trackbacks on this post here:") + "\r\n"
                #// translators: Trackback notification email subject. 1: Site title, 2: Post title.
                subject_ = php_sprintf(__("[%1$s] Trackback: \"%2$s\""), blogname_, post_.post_title)
                break
            # end if
            if case("pingback"):
                #// translators: %s: Post title.
                notify_message_ = php_sprintf(__("New pingback on your post \"%s\""), post_.post_title) + "\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message_ += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment_.comment_author, comment_.comment_author_IP, comment_author_domain_) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message_ += php_sprintf(__("URL: %s"), comment_.comment_author_url) + "\r\n"
                #// translators: %s: Comment text.
                notify_message_ += php_sprintf(__("Comment: %s"), "\r\n" + comment_content_) + "\r\n\r\n"
                notify_message_ += __("You can see all pingbacks on this post here:") + "\r\n"
                #// translators: Pingback notification email subject. 1: Site title, 2: Post title.
                subject_ = php_sprintf(__("[%1$s] Pingback: \"%2$s\""), blogname_, post_.post_title)
                break
            # end if
            if case():
                #// Comments.
                #// translators: %s: Post title.
                notify_message_ = php_sprintf(__("New comment on your post \"%s\""), post_.post_title) + "\r\n"
                #// translators: 1: Comment author's name, 2: Comment author's IP address, 3: Comment author's hostname.
                notify_message_ += php_sprintf(__("Author: %1$s (IP address: %2$s, %3$s)"), comment_.comment_author, comment_.comment_author_IP, comment_author_domain_) + "\r\n"
                #// translators: %s: Comment author email.
                notify_message_ += php_sprintf(__("Email: %s"), comment_.comment_author_email) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message_ += php_sprintf(__("URL: %s"), comment_.comment_author_url) + "\r\n"
                if comment_.comment_parent and user_can(post_.post_author, "edit_comment", comment_.comment_parent):
                    #// translators: Comment moderation. %s: Parent comment edit URL.
                    notify_message_ += php_sprintf(__("In reply to: %s"), admin_url(str("comment.php?action=editcomment&c=") + str(comment_.comment_parent) + str("#wpbody-content"))) + "\r\n"
                # end if
                #// translators: %s: Comment text.
                notify_message_ += php_sprintf(__("Comment: %s"), "\r\n" + comment_content_) + "\r\n\r\n"
                notify_message_ += __("You can see all comments on this post here:") + "\r\n"
                #// translators: Comment notification email subject. 1: Site title, 2: Post title.
                subject_ = php_sprintf(__("[%1$s] Comment: \"%2$s\""), blogname_, post_.post_title)
                break
            # end if
        # end for
        notify_message_ += get_permalink(comment_.comment_post_ID) + "#comments\r\n\r\n"
        #// translators: %s: Comment URL.
        notify_message_ += php_sprintf(__("Permalink: %s"), get_comment_link(comment_)) + "\r\n"
        if user_can(post_.post_author, "edit_comment", comment_.comment_ID):
            if EMPTY_TRASH_DAYS:
                #// translators: Comment moderation. %s: Comment action URL.
                notify_message_ += php_sprintf(__("Trash it: %s"), admin_url(str("comment.php?action=trash&c=") + str(comment_.comment_ID) + str("#wpbody-content"))) + "\r\n"
            else:
                #// translators: Comment moderation. %s: Comment action URL.
                notify_message_ += php_sprintf(__("Delete it: %s"), admin_url(str("comment.php?action=delete&c=") + str(comment_.comment_ID) + str("#wpbody-content"))) + "\r\n"
            # end if
            #// translators: Comment moderation. %s: Comment action URL.
            notify_message_ += php_sprintf(__("Spam it: %s"), admin_url(str("comment.php?action=spam&c=") + str(comment_.comment_ID) + str("#wpbody-content"))) + "\r\n"
        # end if
        wp_email_ = "wordpress@" + php_preg_replace("#^www\\.#", "", php_strtolower(PHP_SERVER["SERVER_NAME"]))
        if "" == comment_.comment_author:
            from_ = str("From: \"") + str(blogname_) + str("\" <") + str(wp_email_) + str(">")
            if "" != comment_.comment_author_email:
                reply_to_ = str("Reply-To: ") + str(comment_.comment_author_email)
            # end if
        else:
            from_ = str("From: \"") + str(comment_.comment_author) + str("\" <") + str(wp_email_) + str(">")
            if "" != comment_.comment_author_email:
                reply_to_ = str("Reply-To: \"") + str(comment_.comment_author_email) + str("\" <") + str(comment_.comment_author_email) + str(">")
            # end if
        # end if
        message_headers_ = str(from_) + str("\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
        if (php_isset(lambda : reply_to_)):
            message_headers_ += reply_to_ + "\n"
        # end if
        #// 
        #// Filters the comment notification email text.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $notify_message The comment notification email text.
        #// @param int    $comment_id     Comment ID.
        #//
        notify_message_ = apply_filters("comment_notification_text", notify_message_, comment_.comment_ID)
        #// 
        #// Filters the comment notification email subject.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $subject    The comment notification email subject.
        #// @param int    $comment_id Comment ID.
        #//
        subject_ = apply_filters("comment_notification_subject", subject_, comment_.comment_ID)
        #// 
        #// Filters the comment notification email headers.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $message_headers Headers for the comment notification email.
        #// @param int    $comment_id      Comment ID.
        #//
        message_headers_ = apply_filters("comment_notification_headers", message_headers_, comment_.comment_ID)
        for email_ in emails_:
            wp_mail(email_, wp_specialchars_decode(subject_), notify_message_, message_headers_)
        # end for
        if switched_locale_:
            restore_previous_locale()
        # end if
        return True
    # end def wp_notify_postauthor
# end if
if (not php_function_exists("wp_notify_moderator")):
    #// 
    #// Notifies the moderator of the site about a new comment that is awaiting approval.
    #// 
    #// @since 1.0.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// Uses the {@see 'notify_moderator'} filter to determine whether the site moderator
    #// should be notified, overriding the site setting.
    #// 
    #// @param int $comment_id Comment ID.
    #// @return true Always returns true.
    #//
    def wp_notify_moderator(comment_id_=None, *_args_):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        maybe_notify_ = get_option("moderation_notify")
        #// 
        #// Filters whether to send the site moderator email notifications, overriding the site setting.
        #// 
        #// @since 4.4.0
        #// 
        #// @param bool $maybe_notify Whether to notify blog moderator.
        #// @param int  $comment_ID   The id of the comment for the notification.
        #//
        maybe_notify_ = apply_filters("notify_moderator", maybe_notify_, comment_id_)
        if (not maybe_notify_):
            return True
        # end if
        comment_ = get_comment(comment_id_)
        post_ = get_post(comment_.comment_post_ID)
        user_ = get_userdata(post_.post_author)
        #// Send to the administration and to the post author if the author can modify the comment.
        emails_ = Array(get_option("admin_email"))
        if user_ and user_can(user_.ID, "edit_comment", comment_id_) and (not php_empty(lambda : user_.user_email)):
            if 0 != strcasecmp(user_.user_email, get_option("admin_email")):
                emails_[-1] = user_.user_email
            # end if
        # end if
        switched_locale_ = switch_to_locale(get_locale())
        comment_author_domain_ = ""
        if WP_Http.is_ip_address(comment_.comment_author_IP):
            comment_author_domain_ = gethostbyaddr(comment_.comment_author_IP)
        # end if
        comments_waiting_ = wpdb_.get_var(str("SELECT COUNT(*) FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = '0'"))
        #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
        #// We want to reverse this for the plain text arena of emails.
        blogname_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        comment_content_ = wp_specialchars_decode(comment_.comment_content)
        for case in Switch(comment_.comment_type):
            if case("trackback"):
                #// translators: %s: Post title.
                notify_message_ = php_sprintf(__("A new trackback on the post \"%s\" is waiting for your approval"), post_.post_title) + "\r\n"
                notify_message_ += get_permalink(comment_.comment_post_ID) + "\r\n\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message_ += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment_.comment_author, comment_.comment_author_IP, comment_author_domain_) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message_ += php_sprintf(__("URL: %s"), comment_.comment_author_url) + "\r\n"
                notify_message_ += __("Trackback excerpt: ") + "\r\n" + comment_content_ + "\r\n\r\n"
                break
            # end if
            if case("pingback"):
                #// translators: %s: Post title.
                notify_message_ = php_sprintf(__("A new pingback on the post \"%s\" is waiting for your approval"), post_.post_title) + "\r\n"
                notify_message_ += get_permalink(comment_.comment_post_ID) + "\r\n\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message_ += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment_.comment_author, comment_.comment_author_IP, comment_author_domain_) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message_ += php_sprintf(__("URL: %s"), comment_.comment_author_url) + "\r\n"
                notify_message_ += __("Pingback excerpt: ") + "\r\n" + comment_content_ + "\r\n\r\n"
                break
            # end if
            if case():
                #// Comments.
                #// translators: %s: Post title.
                notify_message_ = php_sprintf(__("A new comment on the post \"%s\" is waiting for your approval"), post_.post_title) + "\r\n"
                notify_message_ += get_permalink(comment_.comment_post_ID) + "\r\n\r\n"
                #// translators: 1: Comment author's name, 2: Comment author's IP address, 3: Comment author's hostname.
                notify_message_ += php_sprintf(__("Author: %1$s (IP address: %2$s, %3$s)"), comment_.comment_author, comment_.comment_author_IP, comment_author_domain_) + "\r\n"
                #// translators: %s: Comment author email.
                notify_message_ += php_sprintf(__("Email: %s"), comment_.comment_author_email) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message_ += php_sprintf(__("URL: %s"), comment_.comment_author_url) + "\r\n"
                if comment_.comment_parent:
                    #// translators: Comment moderation. %s: Parent comment edit URL.
                    notify_message_ += php_sprintf(__("In reply to: %s"), admin_url(str("comment.php?action=editcomment&c=") + str(comment_.comment_parent) + str("#wpbody-content"))) + "\r\n"
                # end if
                #// translators: %s: Comment text.
                notify_message_ += php_sprintf(__("Comment: %s"), "\r\n" + comment_content_) + "\r\n\r\n"
                break
            # end if
        # end for
        #// translators: Comment moderation. %s: Comment action URL.
        notify_message_ += php_sprintf(__("Approve it: %s"), admin_url(str("comment.php?action=approve&c=") + str(comment_id_) + str("#wpbody-content"))) + "\r\n"
        if EMPTY_TRASH_DAYS:
            #// translators: Comment moderation. %s: Comment action URL.
            notify_message_ += php_sprintf(__("Trash it: %s"), admin_url(str("comment.php?action=trash&c=") + str(comment_id_) + str("#wpbody-content"))) + "\r\n"
        else:
            #// translators: Comment moderation. %s: Comment action URL.
            notify_message_ += php_sprintf(__("Delete it: %s"), admin_url(str("comment.php?action=delete&c=") + str(comment_id_) + str("#wpbody-content"))) + "\r\n"
        # end if
        #// translators: Comment moderation. %s: Comment action URL.
        notify_message_ += php_sprintf(__("Spam it: %s"), admin_url(str("comment.php?action=spam&c=") + str(comment_id_) + str("#wpbody-content"))) + "\r\n"
        notify_message_ += php_sprintf(_n("Currently %s comment is waiting for approval. Please visit the moderation panel:", "Currently %s comments are waiting for approval. Please visit the moderation panel:", comments_waiting_), number_format_i18n(comments_waiting_)) + "\r\n"
        notify_message_ += admin_url("edit-comments.php?comment_status=moderated#wpbody-content") + "\r\n"
        #// translators: Comment moderation notification email subject. 1: Site title, 2: Post title.
        subject_ = php_sprintf(__("[%1$s] Please moderate: \"%2$s\""), blogname_, post_.post_title)
        message_headers_ = ""
        #// 
        #// Filters the list of recipients for comment moderation emails.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string[] $emails     List of email addresses to notify for comment moderation.
        #// @param int      $comment_id Comment ID.
        #//
        emails_ = apply_filters("comment_moderation_recipients", emails_, comment_id_)
        #// 
        #// Filters the comment moderation email text.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $notify_message Text of the comment moderation email.
        #// @param int    $comment_id     Comment ID.
        #//
        notify_message_ = apply_filters("comment_moderation_text", notify_message_, comment_id_)
        #// 
        #// Filters the comment moderation email subject.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $subject    Subject of the comment moderation email.
        #// @param int    $comment_id Comment ID.
        #//
        subject_ = apply_filters("comment_moderation_subject", subject_, comment_id_)
        #// 
        #// Filters the comment moderation email headers.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $message_headers Headers for the comment moderation email.
        #// @param int    $comment_id      Comment ID.
        #//
        message_headers_ = apply_filters("comment_moderation_headers", message_headers_, comment_id_)
        for email_ in emails_:
            wp_mail(email_, wp_specialchars_decode(subject_), notify_message_, message_headers_)
        # end for
        if switched_locale_:
            restore_previous_locale()
        # end if
        return True
    # end def wp_notify_moderator
# end if
if (not php_function_exists("wp_password_change_notification")):
    #// 
    #// Notify the blog admin of a user changing password, normally via email.
    #// 
    #// @since 2.7.0
    #// 
    #// @param WP_User $user User object.
    #//
    def wp_password_change_notification(user_=None, *_args_):
        
        
        #// Send a copy of password change notification to the admin,
        #// but check to see if it's the admin whose password we're changing, and skip this.
        if 0 != strcasecmp(user_.user_email, get_option("admin_email")):
            #// translators: %s: User name.
            message_ = php_sprintf(__("Password changed for user: %s"), user_.user_login) + "\r\n"
            #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
            #// We want to reverse this for the plain text arena of emails.
            blogname_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
            wp_password_change_notification_email_ = Array({"to": get_option("admin_email"), "subject": __("[%s] Password Changed"), "message": message_, "headers": ""})
            #// 
            #// Filters the contents of the password change notification email sent to the site admin.
            #// 
            #// @since 4.9.0
            #// 
            #// @param array   $wp_password_change_notification_email {
            #// Used to build wp_mail().
            #// 
            #// @type string $to      The intended recipient - site admin email address.
            #// @type string $subject The subject of the email.
            #// @type string $message The body of the email.
            #// @type string $headers The headers of the email.
            #// }
            #// @param WP_User $user     User object for user whose password was changed.
            #// @param string  $blogname The site title.
            #//
            wp_password_change_notification_email_ = apply_filters("wp_password_change_notification_email", wp_password_change_notification_email_, user_, blogname_)
            wp_mail(wp_password_change_notification_email_["to"], wp_specialchars_decode(php_sprintf(wp_password_change_notification_email_["subject"], blogname_)), wp_password_change_notification_email_["message"], wp_password_change_notification_email_["headers"])
        # end if
    # end def wp_password_change_notification
# end if
if (not php_function_exists("wp_new_user_notification")):
    #// 
    #// Email login credentials to a newly-registered user.
    #// 
    #// A new user registration notification is also sent to admin email.
    #// 
    #// @since 2.0.0
    #// @since 4.3.0 The `$plaintext_pass` parameter was changed to `$notify`.
    #// @since 4.3.1 The `$plaintext_pass` parameter was deprecated. `$notify` added as a third parameter.
    #// @since 4.6.0 The `$notify` parameter accepts 'user' for sending notification only to the user created.
    #// 
    #// @param int    $user_id    User ID.
    #// @param null   $deprecated Not used (argument deprecated).
    #// @param string $notify     Optional. Type of notification that should happen. Accepts 'admin' or an empty
    #// string (admin only), 'user', or 'both' (admin and user). Default empty.
    #//
    def wp_new_user_notification(user_id_=None, deprecated_=None, notify_="", *_args_):
        if deprecated_ is None:
            deprecated_ = None
        # end if
        
        if None != deprecated_:
            _deprecated_argument(__FUNCTION__, "4.3.1")
        # end if
        #// Accepts only 'user', 'admin' , 'both' or default '' as $notify.
        if (not php_in_array(notify_, Array("user", "admin", "both", ""), True)):
            return
        # end if
        user_ = get_userdata(user_id_)
        #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
        #// We want to reverse this for the plain text arena of emails.
        blogname_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        if "user" != notify_:
            switched_locale_ = switch_to_locale(get_locale())
            #// translators: %s: Site title.
            message_ = php_sprintf(__("New user registration on your site %s:"), blogname_) + "\r\n\r\n"
            #// translators: %s: User login.
            message_ += php_sprintf(__("Username: %s"), user_.user_login) + "\r\n\r\n"
            #// translators: %s: User email address.
            message_ += php_sprintf(__("Email: %s"), user_.user_email) + "\r\n"
            wp_new_user_notification_email_admin_ = Array({"to": get_option("admin_email"), "subject": __("[%s] New User Registration"), "message": message_, "headers": ""})
            #// 
            #// Filters the contents of the new user notification email sent to the site admin.
            #// 
            #// @since 4.9.0
            #// 
            #// @param array   $wp_new_user_notification_email_admin {
            #// Used to build wp_mail().
            #// 
            #// @type string $to      The intended recipient - site admin email address.
            #// @type string $subject The subject of the email.
            #// @type string $message The body of the email.
            #// @type string $headers The headers of the email.
            #// }
            #// @param WP_User $user     User object for new user.
            #// @param string  $blogname The site title.
            #//
            wp_new_user_notification_email_admin_ = apply_filters("wp_new_user_notification_email_admin", wp_new_user_notification_email_admin_, user_, blogname_)
            wp_mail(wp_new_user_notification_email_admin_["to"], wp_specialchars_decode(php_sprintf(wp_new_user_notification_email_admin_["subject"], blogname_)), wp_new_user_notification_email_admin_["message"], wp_new_user_notification_email_admin_["headers"])
            if switched_locale_:
                restore_previous_locale()
            # end if
        # end if
        #// `$deprecated` was pre-4.3 `$plaintext_pass`. An empty `$plaintext_pass` didn't sent a user notification.
        if "admin" == notify_ or php_empty(lambda : deprecated_) and php_empty(lambda : notify_):
            return
        # end if
        key_ = get_password_reset_key(user_)
        if is_wp_error(key_):
            return
        # end if
        switched_locale_ = switch_to_locale(get_user_locale(user_))
        #// translators: %s: User login.
        message_ = php_sprintf(__("Username: %s"), user_.user_login) + "\r\n\r\n"
        message_ += __("To set your password, visit the following address:") + "\r\n\r\n"
        message_ += network_site_url(str("wp-login.php?action=rp&key=") + str(key_) + str("&login=") + rawurlencode(user_.user_login), "login") + "\r\n\r\n"
        message_ += wp_login_url() + "\r\n"
        wp_new_user_notification_email_ = Array({"to": user_.user_email, "subject": __("[%s] Login Details"), "message": message_, "headers": ""})
        #// 
        #// Filters the contents of the new user notification email sent to the new user.
        #// 
        #// @since 4.9.0
        #// 
        #// @param array   $wp_new_user_notification_email {
        #// Used to build wp_mail().
        #// 
        #// @type string $to      The intended recipient - New user email address.
        #// @type string $subject The subject of the email.
        #// @type string $message The body of the email.
        #// @type string $headers The headers of the email.
        #// }
        #// @param WP_User $user     User object for new user.
        #// @param string  $blogname The site title.
        #//
        wp_new_user_notification_email_ = apply_filters("wp_new_user_notification_email", wp_new_user_notification_email_, user_, blogname_)
        wp_mail(wp_new_user_notification_email_["to"], wp_specialchars_decode(php_sprintf(wp_new_user_notification_email_["subject"], blogname_)), wp_new_user_notification_email_["message"], wp_new_user_notification_email_["headers"])
        if switched_locale_:
            restore_previous_locale()
        # end if
    # end def wp_new_user_notification
# end if
if (not php_function_exists("wp_nonce_tick")):
    #// 
    #// Returns the time-dependent variable for nonce creation.
    #// 
    #// A nonce has a lifespan of two ticks. Nonces in their second tick may be
    #// updated, e.g. by autosave.
    #// 
    #// @since 2.5.0
    #// 
    #// @return float Float value rounded up to the next highest integer.
    #//
    def wp_nonce_tick(*_args_):
        
        
        #// 
        #// Filters the lifespan of nonces in seconds.
        #// 
        #// @since 2.5.0
        #// 
        #// @param int $lifespan Lifespan of nonces in seconds. Default 86,400 seconds, or one day.
        #//
        nonce_life_ = apply_filters("nonce_life", DAY_IN_SECONDS)
        return ceil(time() / nonce_life_ / 2)
    # end def wp_nonce_tick
# end if
if (not php_function_exists("wp_verify_nonce")):
    #// 
    #// Verifies that a correct security nonce was used with time limit.
    #// 
    #// A nonce is valid for 24 hours (by default).
    #// 
    #// @since 2.0.3
    #// 
    #// @param string     $nonce  Nonce value that was used for verification, usually via a form field.
    #// @param string|int $action Should give context to what is taking place and be the same when nonce was created.
    #// @return int|false 1 if the nonce is valid and generated between 0-12 hours ago,
    #// 2 if the nonce is valid and generated between 12-24 hours ago.
    #// False if the nonce is invalid.
    #//
    def wp_verify_nonce(nonce_=None, action_=None, *_args_):
        if action_ is None:
            action_ = -1
        # end if
        
        nonce_ = php_str(nonce_)
        user_ = wp_get_current_user()
        uid_ = php_int(user_.ID)
        if (not uid_):
            #// 
            #// Filters whether the user who generated the nonce is logged out.
            #// 
            #// @since 3.5.0
            #// 
            #// @param int    $uid    ID of the nonce-owning user.
            #// @param string $action The nonce action.
            #//
            uid_ = apply_filters("nonce_user_logged_out", uid_, action_)
        # end if
        if php_empty(lambda : nonce_):
            return False
        # end if
        token_ = wp_get_session_token()
        i_ = wp_nonce_tick()
        #// Nonce generated 0-12 hours ago.
        expected_ = php_substr(wp_hash(i_ + "|" + action_ + "|" + uid_ + "|" + token_, "nonce"), -12, 10)
        if hash_equals(expected_, nonce_):
            return 1
        # end if
        #// Nonce generated 12-24 hours ago.
        expected_ = php_substr(wp_hash(i_ - 1 + "|" + action_ + "|" + uid_ + "|" + token_, "nonce"), -12, 10)
        if hash_equals(expected_, nonce_):
            return 2
        # end if
        #// 
        #// Fires when nonce verification fails.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string     $nonce  The invalid nonce.
        #// @param string|int $action The nonce action.
        #// @param WP_User    $user   The current user object.
        #// @param string     $token  The user's session token.
        #//
        do_action("wp_verify_nonce_failed", nonce_, action_, user_, token_)
        #// Invalid nonce.
        return False
    # end def wp_verify_nonce
# end if
if (not php_function_exists("wp_create_nonce")):
    #// 
    #// Creates a cryptographic token tied to a specific action, user, user session,
    #// and window of time.
    #// 
    #// @since 2.0.3
    #// @since 4.0.0 Session tokens were integrated with nonce creation
    #// 
    #// @param string|int $action Scalar value to add context to the nonce.
    #// @return string The token.
    #//
    def wp_create_nonce(action_=None, *_args_):
        if action_ is None:
            action_ = -1
        # end if
        
        user_ = wp_get_current_user()
        uid_ = php_int(user_.ID)
        if (not uid_):
            #// This filter is documented in wp-includes/pluggable.php
            uid_ = apply_filters("nonce_user_logged_out", uid_, action_)
        # end if
        token_ = wp_get_session_token()
        i_ = wp_nonce_tick()
        return php_substr(wp_hash(i_ + "|" + action_ + "|" + uid_ + "|" + token_, "nonce"), -12, 10)
    # end def wp_create_nonce
# end if
if (not php_function_exists("wp_salt")):
    #// 
    #// Returns a salt to add to hashes.
    #// 
    #// Salts are created using secret keys. Secret keys are located in two places:
    #// in the database and in the wp-config.php file. The secret key in the database
    #// is randomly generated and will be appended to the secret keys in wp-config.php.
    #// 
    #// The secret keys in wp-config.php should be updated to strong, random keys to maximize
    #// security. Below is an example of how the secret key constants are defined.
    #// Do not paste this example directly into wp-config.php. Instead, have a
    #// {@link https://api.wordpress.org/secret-key/1.1/salt/ secret key created} just
    #// for you.
    #// 
    #// define('AUTH_KEY',         ' Xakm<o xQy rw4EMsLKM-?!T+,PFF})H4lzcW57AF0U@N@< >M%G4Yt>f`z]MON');
    #// define('SECURE_AUTH_KEY',  'LzJ}op]mr|6+![P}Ak:uNdJCJZd>(Hx.-Mh#Tz)pCIU#uGEnfFz|f ;;eU%/U^O~');
    #// define('LOGGED_IN_KEY',    '|i|Ux`9<p-h$aFf(qnT:sDO:D1P^wZ$$/Ra@miTJi9G;ddp_<q}6H1)o|a +&JCM');
    #// define('NONCE_KEY',        '%:R{[P|,s.KuMltH5}cI;/k<Gx~j!f0I)m_sIyu+&NJZ)-iO>z7X>QYR0Z_XnZ@|');
    #// define('AUTH_SALT',        'eZyT)-Naw]F8CwA*VaW#q*|.)g@o}||wf~@C-YSt}(dh_r6EbI#A,y|nU2{B#JBW');
    #// define('SECURE_AUTH_SALT', '!=oLUTXh,QW=H `}`L|9/^4-3 STz},T(w}W<I`.JjPi)<Bmf1v,HpGe}T1:Xt7n');
    #// define('LOGGED_IN_SALT',   '+XSqHc;@Q*K_b|Z?NC[3H!!EONbh.n<+=uKR:>*c(u`g~EJBf#8u#R{mUEZrozmm');
    #// define('NONCE_SALT',       'h`GXHhD>SLWVfg1(1(N{;.V!MoE(SfbA_ksP@&`+AycHcAV$+?@3q+rxV{%^VyKT');
    #// 
    #// Salting passwords helps against tools which has stored hashed values of
    #// common dictionary strings. The added values makes it harder to crack.
    #// 
    #// @since 2.5.0
    #// 
    #// @link https://api.wordpress.org/secret-key/1.1/salt/ Create secrets for wp-config.php
    #// 
    #// @staticvar array $cached_salts
    #// @staticvar array $duplicated_keys
    #// 
    #// @param string $scheme Authentication scheme (auth, secure_auth, logged_in, nonce)
    #// @return string Salt value
    #//
    def wp_salt(scheme_="auth", *_args_):
        
        
        cached_salts_ = Array()
        if (php_isset(lambda : cached_salts_[scheme_])):
            #// 
            #// Filters the WordPress salt.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string $cached_salt Cached salt for the given scheme.
            #// @param string $scheme      Authentication scheme. Values include 'auth',
            #// 'secure_auth', 'logged_in', and 'nonce'.
            #//
            return apply_filters("salt", cached_salts_[scheme_], scheme_)
        # end if
        duplicated_keys_ = None
        if None == duplicated_keys_:
            duplicated_keys_ = Array({"put your unique phrase here": True})
            for first_ in Array("AUTH", "SECURE_AUTH", "LOGGED_IN", "NONCE", "SECRET"):
                for second_ in Array("KEY", "SALT"):
                    if (not php_defined(str(first_) + str("_") + str(second_))):
                        continue
                    # end if
                    value_ = constant(str(first_) + str("_") + str(second_))
                    duplicated_keys_[value_] = (php_isset(lambda : duplicated_keys_[value_]))
                # end for
            # end for
        # end if
        values_ = Array({"key": "", "salt": ""})
        if php_defined("SECRET_KEY") and SECRET_KEY and php_empty(lambda : duplicated_keys_[SECRET_KEY]):
            values_["key"] = SECRET_KEY
        # end if
        if "auth" == scheme_ and php_defined("SECRET_SALT") and SECRET_SALT and php_empty(lambda : duplicated_keys_[SECRET_SALT]):
            values_["salt"] = SECRET_SALT
        # end if
        if php_in_array(scheme_, Array("auth", "secure_auth", "logged_in", "nonce")):
            for type_ in Array("key", "salt"):
                const_ = php_strtoupper(str(scheme_) + str("_") + str(type_))
                if php_defined(const_) and constant(const_) and php_empty(lambda : duplicated_keys_[constant(const_)]):
                    values_[type_] = constant(const_)
                elif (not values_[type_]):
                    values_[type_] = get_site_option(str(scheme_) + str("_") + str(type_))
                    if (not values_[type_]):
                        values_[type_] = wp_generate_password(64, True, True)
                        update_site_option(str(scheme_) + str("_") + str(type_), values_[type_])
                    # end if
                # end if
            # end for
        else:
            if (not values_["key"]):
                values_["key"] = get_site_option("secret_key")
                if (not values_["key"]):
                    values_["key"] = wp_generate_password(64, True, True)
                    update_site_option("secret_key", values_["key"])
                # end if
            # end if
            values_["salt"] = hash_hmac("md5", scheme_, values_["key"])
        # end if
        cached_salts_[scheme_] = values_["key"] + values_["salt"]
        #// This filter is documented in wp-includes/pluggable.php
        return apply_filters("salt", cached_salts_[scheme_], scheme_)
    # end def wp_salt
# end if
if (not php_function_exists("wp_hash")):
    #// 
    #// Get hash of given string.
    #// 
    #// @since 2.0.3
    #// 
    #// @param string $data   Plain text to hash
    #// @param string $scheme Authentication scheme (auth, secure_auth, logged_in, nonce)
    #// @return string Hash of $data
    #//
    def wp_hash(data_=None, scheme_="auth", *_args_):
        
        
        salt_ = wp_salt(scheme_)
        return hash_hmac("md5", data_, salt_)
    # end def wp_hash
# end if
if (not php_function_exists("wp_hash_password")):
    #// 
    #// Create a hash (encrypt) of a plain text password.
    #// 
    #// For integration with other applications, this function can be overwritten to
    #// instead use the other package password checking algorithm.
    #// 
    #// @since 2.5.0
    #// 
    #// @global PasswordHash $wp_hasher PHPass object
    #// 
    #// @param string $password Plain text user password to hash
    #// @return string The hash string of the password
    #//
    def wp_hash_password(password_=None, *_args_):
        
        
        global wp_hasher_
        php_check_if_defined("wp_hasher_")
        if php_empty(lambda : wp_hasher_):
            php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
            #// By default, use the portable hash from phpass.
            wp_hasher_ = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
        # end if
        return wp_hasher_.hashpassword(php_trim(password_))
    # end def wp_hash_password
# end if
if (not php_function_exists("wp_check_password")):
    #// 
    #// Checks the plaintext password against the encrypted Password.
    #// 
    #// Maintains compatibility between old version and the new cookie authentication
    #// protocol using PHPass library. The $hash parameter is the encrypted password
    #// and the function compares the plain text password when encrypted similarly
    #// against the already encrypted password to see if they match.
    #// 
    #// For integration with other applications, this function can be overwritten to
    #// instead use the other package password checking algorithm.
    #// 
    #// @since 2.5.0
    #// 
    #// @global PasswordHash $wp_hasher PHPass object used for checking the password
    #// against the $hash + $password
    #// @uses PasswordHash::CheckPassword
    #// 
    #// @param string     $password Plaintext user's password
    #// @param string     $hash     Hash of the user's password to check against.
    #// @param string|int $user_id  Optional. User ID.
    #// @return bool False, if the $password does not match the hashed password
    #//
    def wp_check_password(password_=None, hash_=None, user_id_="", *_args_):
        
        
        global wp_hasher_
        php_check_if_defined("wp_hasher_")
        #// If the hash is still md5...
        if php_strlen(hash_) <= 32:
            check_ = hash_equals(hash_, php_md5(password_))
            if check_ and user_id_:
                #// Rehash using new hash.
                wp_set_password(password_, user_id_)
                hash_ = wp_hash_password(password_)
            # end if
            #// 
            #// Filters whether the plaintext password matches the encrypted password.
            #// 
            #// @since 2.5.0
            #// 
            #// @param bool       $check    Whether the passwords match.
            #// @param string     $password The plaintext password.
            #// @param string     $hash     The hashed password.
            #// @param string|int $user_id  User ID. Can be empty.
            #//
            return apply_filters("check_password", check_, password_, hash_, user_id_)
        # end if
        #// If the stored hash is longer than an MD5,
        #// presume the new style phpass portable hash.
        if php_empty(lambda : wp_hasher_):
            php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
            #// By default, use the portable hash from phpass.
            wp_hasher_ = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
        # end if
        check_ = wp_hasher_.checkpassword(password_, hash_)
        #// This filter is documented in wp-includes/pluggable.php
        return apply_filters("check_password", check_, password_, hash_, user_id_)
    # end def wp_check_password
# end if
if (not php_function_exists("wp_generate_password")):
    #// 
    #// Generates a random password drawn from the defined set of characters.
    #// 
    #// Uses wp_rand() is used to create passwords with far less predictability
    #// than similar native PHP functions like `rand()` or `mt_rand()`.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int  $length              Optional. The length of password to generate. Default 12.
    #// @param bool $special_chars       Optional. Whether to include standard special characters.
    #// Default true.
    #// @param bool $extra_special_chars Optional. Whether to include other special characters.
    #// Used when generating secret keys and salts. Default false.
    #// @return string The random password.
    #//
    def wp_generate_password(length_=12, special_chars_=None, extra_special_chars_=None, *_args_):
        if special_chars_ is None:
            special_chars_ = True
        # end if
        if extra_special_chars_ is None:
            extra_special_chars_ = False
        # end if
        
        chars_ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if special_chars_:
            chars_ += "!@#$%^&*()"
        # end if
        if extra_special_chars_:
            chars_ += "-_ []{}<>~`+=,.;:/?|"
        # end if
        password_ = ""
        i_ = 0
        while i_ < length_:
            
            password_ += php_substr(chars_, wp_rand(0, php_strlen(chars_) - 1), 1)
            i_ += 1
        # end while
        #// 
        #// Filters the randomly-generated password.
        #// 
        #// @since 3.0.0
        #// @since 5.3.0 Added the `$length`, `$special_chars`, and `$extra_special_chars` parameters.
        #// 
        #// @param string $password            The generated password.
        #// @param int    $length              The length of password to generate.
        #// @param bool   $special_chars       Whether to include standard special characters.
        #// @param bool   $extra_special_chars Whether to include other special characters.
        #//
        return apply_filters("random_password", password_, length_, special_chars_, extra_special_chars_)
    # end def wp_generate_password
# end if
if (not php_function_exists("wp_rand")):
    #// 
    #// Generates a random number.
    #// 
    #// @since 2.6.2
    #// @since 4.4.0 Uses PHP7 random_int() or the random_compat library if available.
    #// 
    #// @global string $rnd_value
    #// @staticvar string $seed
    #// @staticvar bool $use_random_int_functionality
    #// 
    #// @param int $min Lower limit for the generated number
    #// @param int $max Upper limit for the generated number
    #// @return int A random number between min and max
    #//
    def wp_rand(min_=0, max_=0, *_args_):
        
        
        global rnd_value_
        php_check_if_defined("rnd_value_")
        #// Some misconfigured 32-bit environments (Entropy PHP, for example)
        #// truncate integers larger than PHP_INT_MAX to PHP_INT_MAX rather than overflowing them to floats.
        max_random_number_ = php_float("4294967295") if 3000000000 == 2147483647 else 4294967295
        #// 4294967295 = 0xffffffff
        #// We only handle ints, floats are truncated to their integer value.
        min_ = php_int(min_)
        max_ = php_int(max_)
        use_random_int_functionality_ = True
        if use_random_int_functionality_:
            try: 
                _max_ = max_ if 0 != max_ else max_random_number_
                #// wp_rand() can accept arguments in either order, PHP cannot.
                _max_ = php_max(min_, _max_)
                _min_ = php_min(min_, _max_)
                val_ = php_random_int(_min_, _max_)
                if False != val_:
                    return absint(val_)
                else:
                    use_random_int_functionality_ = False
                # end if
            except Error as e_:
                use_random_int_functionality_ = False
            except Exception as e_:
                use_random_int_functionality_ = False
            # end try
        # end if
        #// Reset $rnd_value after 14 uses.
        #// 32 (md5) + 40 (sha1) + 40 (sha1) / 8 = 14 random numbers from $rnd_value.
        if php_strlen(rnd_value_) < 8:
            if php_defined("WP_SETUP_CONFIG"):
                seed_ = ""
            else:
                seed_ = get_transient("random_seed")
            # end if
            rnd_value_ = php_md5(uniqid(php_microtime() + mt_rand(), True) + seed_)
            rnd_value_ += sha1(rnd_value_)
            rnd_value_ += sha1(rnd_value_ + seed_)
            seed_ = php_md5(seed_ + rnd_value_)
            if (not php_defined("WP_SETUP_CONFIG")) and (not php_defined("WP_INSTALLING")):
                set_transient("random_seed", seed_)
            # end if
        # end if
        #// Take the first 8 digits for our value.
        value_ = php_substr(rnd_value_, 0, 8)
        #// Strip the first eight, leaving the remainder for the next call to wp_rand().
        rnd_value_ = php_substr(rnd_value_, 8)
        value_ = abs(hexdec(value_))
        #// Reduce the value to be within the min - max range.
        if 0 != max_:
            value_ = min_ + max_ - min_ + 1 * value_ / max_random_number_ + 1
        # end if
        return abs(php_intval(value_))
    # end def wp_rand
# end if
if (not php_function_exists("wp_set_password")):
    #// 
    #// Updates the user's password with a new encrypted one.
    #// 
    #// For integration with other applications, this function can be overwritten to
    #// instead use the other package password checking algorithm.
    #// 
    #// Please note: This function should be used sparingly and is really only meant for single-time
    #// application. Leveraging this improperly in a plugin or theme could result in an endless loop
    #// of password resets if precautions are not taken to ensure it does not execute on every page load.
    #// 
    #// @since 2.5.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $password The plaintext new user password
    #// @param int    $user_id  User ID
    #//
    def wp_set_password(password_=None, user_id_=None, *_args_):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        hash_ = wp_hash_password(password_)
        wpdb_.update(wpdb_.users, Array({"user_pass": hash_, "user_activation_key": ""}), Array({"ID": user_id_}))
        clean_user_cache(user_id_)
    # end def wp_set_password
# end if
if (not php_function_exists("get_avatar")):
    #// 
    #// Retrieve the avatar `<img>` tag for a user, email address, MD5 hash, comment, or post.
    #// 
    #// @since 2.5.0
    #// @since 4.2.0 Optional `$args` parameter added.
    #// 
    #// @param mixed $id_or_email The Gravatar to retrieve. Accepts a user_id, gravatar md5 hash,
    #// user email, WP_User object, WP_Post object, or WP_Comment object.
    #// @param int    $size       Optional. Height and width of the avatar image file in pixels. Default 96.
    #// @param string $default    Optional. URL for the default image or a default type. Accepts '404'
    #// (return a 404 instead of a default image), 'retro' (8bit), 'monsterid'
    #// (monster), 'wavatar' (cartoon face), 'indenticon' (the "quilt"),
    #// 'mystery', 'mm', or 'mysteryman' (The Oyster Man), 'blank' (transparent GIF),
    #// or 'gravatar_default' (the Gravatar logo). Default is the value of the
    #// 'avatar_default' option, with a fallback of 'mystery'.
    #// @param string $alt        Optional. Alternative text to use in &lt;img&gt; tag. Default empty.
    #// @param array  $args       {
    #// Optional. Extra arguments to retrieve the avatar.
    #// 
    #// @type int          $height        Display height of the avatar in pixels. Defaults to $size.
    #// @type int          $width         Display width of the avatar in pixels. Defaults to $size.
    #// @type bool         $force_default Whether to always show the default image, never the Gravatar. Default false.
    #// @type string       $rating        What rating to display avatars up to. Accepts 'G', 'PG', 'R', 'X', and are
    #// judged in that order. Default is the value of the 'avatar_rating' option.
    #// @type string       $scheme        URL scheme to use. See set_url_scheme() for accepted values.
    #// Default null.
    #// @type array|string $class         Array or string of additional classes to add to the &lt;img&gt; element.
    #// Default null.
    #// @type bool         $force_display Whether to always show the avatar - ignores the show_avatars option.
    #// Default false.
    #// @type string       $extra_attr    HTML attributes to insert in the IMG element. Is not sanitized. Default empty.
    #// }
    #// @return string|false `<img>` tag for the user's avatar. False on failure.
    #//
    def get_avatar(id_or_email_=None, size_=96, default_="", alt_="", args_=None, *_args_):
        if args_ is None:
            args_ = None
        # end if
        
        defaults_ = Array({"size": 96, "height": None, "width": None, "default": get_option("avatar_default", "mystery"), "force_default": False, "rating": get_option("avatar_rating"), "scheme": None, "alt": "", "class": None, "force_display": False, "extra_attr": ""})
        if php_empty(lambda : args_):
            args_ = Array()
        # end if
        args_["size"] = php_int(size_)
        args_["default"] = default_
        args_["alt"] = alt_
        args_ = wp_parse_args(args_, defaults_)
        if php_empty(lambda : args_["height"]):
            args_["height"] = args_["size"]
        # end if
        if php_empty(lambda : args_["width"]):
            args_["width"] = args_["size"]
        # end if
        if php_is_object(id_or_email_) and (php_isset(lambda : id_or_email_.comment_ID)):
            id_or_email_ = get_comment(id_or_email_)
        # end if
        #// 
        #// Filters whether to retrieve the avatar URL early.
        #// 
        #// Passing a non-null value will effectively short-circuit get_avatar(), passing
        #// the value through the {@see 'get_avatar'} filter and returning early.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string|null $avatar      HTML for the user's avatar. Default null.
        #// @param mixed       $id_or_email The Gravatar to retrieve. Accepts a user_id, gravatar md5 hash,
        #// user email, WP_User object, WP_Post object, or WP_Comment object.
        #// @param array       $args        Arguments passed to get_avatar_url(), after processing.
        #//
        avatar_ = apply_filters("pre_get_avatar", None, id_or_email_, args_)
        if (not php_is_null(avatar_)):
            #// This filter is documented in wp-includes/pluggable.php
            return apply_filters("get_avatar", avatar_, id_or_email_, args_["size"], args_["default"], args_["alt"], args_)
        # end if
        if (not args_["force_display"]) and (not get_option("show_avatars")):
            return False
        # end if
        url2x_ = get_avatar_url(id_or_email_, php_array_merge(args_, Array({"size": args_["size"] * 2})))
        args_ = get_avatar_data(id_or_email_, args_)
        url_ = args_["url"]
        if (not url_) or is_wp_error(url_):
            return False
        # end if
        class_ = Array("avatar", "avatar-" + php_int(args_["size"]), "photo")
        if (not args_["found_avatar"]) or args_["force_default"]:
            class_[-1] = "avatar-default"
        # end if
        if args_["class"]:
            if php_is_array(args_["class"]):
                class_ = php_array_merge(class_, args_["class"])
            else:
                class_[-1] = args_["class"]
            # end if
        # end if
        avatar_ = php_sprintf("<img alt='%s' src='%s' srcset='%s' class='%s' height='%d' width='%d' %s/>", esc_attr(args_["alt"]), esc_url(url_), esc_url(url2x_) + " 2x", esc_attr(join(" ", class_)), php_int(args_["height"]), php_int(args_["width"]), args_["extra_attr"])
        #// 
        #// Filters the avatar to retrieve.
        #// 
        #// @since 2.5.0
        #// @since 4.2.0 The `$args` parameter was added.
        #// 
        #// @param string $avatar      &lt;img&gt; tag for the user's avatar.
        #// @param mixed  $id_or_email The Gravatar to retrieve. Accepts a user_id, gravatar md5 hash,
        #// user email, WP_User object, WP_Post object, or WP_Comment object.
        #// @param int    $size        Square avatar width and height in pixels to retrieve.
        #// @param string $default     URL for the default image or a default type. Accepts '404', 'retro', 'monsterid',
        #// 'wavatar', 'indenticon','mystery' (or 'mm', or 'mysteryman'), 'blank', or 'gravatar_default'.
        #// Default is the value of the 'avatar_default' option, with a fallback of 'mystery'.
        #// @param string $alt         Alternative text to use in the avatar image tag. Default empty.
        #// @param array  $args        Arguments passed to get_avatar_data(), after processing.
        #//
        return apply_filters("get_avatar", avatar_, id_or_email_, args_["size"], args_["default"], args_["alt"], args_)
    # end def get_avatar
# end if
if (not php_function_exists("wp_text_diff")):
    #// 
    #// Displays a human readable HTML representation of the difference between two strings.
    #// 
    #// The Diff is available for getting the changes between versions. The output is
    #// HTML, so the primary use is for displaying the changes. If the two strings
    #// are equivalent, then an empty string will be returned.
    #// 
    #// @since 2.6.0
    #// 
    #// @see wp_parse_args() Used to change defaults to user defined settings.
    #// @uses Text_Diff
    #// @uses WP_Text_Diff_Renderer_Table
    #// 
    #// @param string       $left_string  "old" (left) version of string
    #// @param string       $right_string "new" (right) version of string
    #// @param string|array $args {
    #// Associative array of options to pass to WP_Text_Diff_Renderer_Table().
    #// 
    #// @type string $title           Titles the diff in a manner compatible
    #// with the output. Default empty.
    #// @type string $title_left      Change the HTML to the left of the title.
    #// Default empty.
    #// @type string $title_right     Change the HTML to the right of the title.
    #// Default empty.
    #// @type bool   $show_split_view True for split view (two columns), false for
    #// un-split view (single column). Default true.
    #// }
    #// @return string Empty string if strings are equivalent or HTML with differences.
    #//
    def wp_text_diff(left_string_=None, right_string_=None, args_=None, *_args_):
        if args_ is None:
            args_ = None
        # end if
        
        defaults_ = Array({"title": "", "title_left": "", "title_right": "", "show_split_view": True})
        args_ = wp_parse_args(args_, defaults_)
        if (not php_class_exists("WP_Text_Diff_Renderer_Table", False)):
            php_include_file(ABSPATH + WPINC + "/wp-diff.php", once=False)
        # end if
        left_string_ = normalize_whitespace(left_string_)
        right_string_ = normalize_whitespace(right_string_)
        left_lines_ = php_explode("\n", left_string_)
        right_lines_ = php_explode("\n", right_string_)
        text_diff_ = php_new_class("Text_Diff", lambda : Text_Diff(left_lines_, right_lines_))
        renderer_ = php_new_class("WP_Text_Diff_Renderer_Table", lambda : WP_Text_Diff_Renderer_Table(args_))
        diff_ = renderer_.render(text_diff_)
        if (not diff_):
            return ""
        # end if
        r_ = "<table class='diff'>\n"
        if (not php_empty(lambda : args_["show_split_view"])):
            r_ += "<col class='content diffsplit left' /><col class='content diffsplit middle' /><col class='content diffsplit right' />"
        else:
            r_ += "<col class='content' />"
        # end if
        if args_["title"] or args_["title_left"] or args_["title_right"]:
            r_ += "<thead>"
        # end if
        if args_["title"]:
            r_ += str("<tr class='diff-title'><th colspan='4'>") + str(args_["title"]) + str("</th></tr>\n")
        # end if
        if args_["title_left"] or args_["title_right"]:
            r_ += "<tr class='diff-sub-title'>\n"
            r_ += str(" <td></td><th>") + str(args_["title_left"]) + str("</th>\n")
            r_ += str(" <td></td><th>") + str(args_["title_right"]) + str("</th>\n")
            r_ += "</tr>\n"
        # end if
        if args_["title"] or args_["title_left"] or args_["title_right"]:
            r_ += "</thead>\n"
        # end if
        r_ += str("<tbody>\n") + str(diff_) + str("\n</tbody>\n")
        r_ += "</table>"
        return r_
    # end def wp_text_diff
# end if
