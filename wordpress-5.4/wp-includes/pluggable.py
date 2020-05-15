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
    def wp_set_current_user(id=None, name="", *args_):
        
        global current_user
        php_check_if_defined("current_user")
        #// If `$id` matches the current user, there is nothing to do.
        if (php_isset(lambda : current_user)) and type(current_user).__name__ == "WP_User" and id == current_user.ID and None != id:
            return current_user
        # end if
        current_user = php_new_class("WP_User", lambda : WP_User(id, name))
        setup_userdata(current_user.ID)
        #// 
        #// Fires after the current user is set.
        #// 
        #// @since 2.0.1
        #//
        do_action("set_current_user")
        return current_user
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
    def wp_get_current_user(*args_):
        
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
    def get_userdata(user_id=None, *args_):
        
        return get_user_by("id", user_id)
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
    def get_user_by(field=None, value=None, *args_):
        
        userdata = WP_User.get_data_by(field, value)
        if (not userdata):
            return False
        # end if
        user = php_new_class("WP_User", lambda : WP_User())
        user.init(userdata)
        return user
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
    def cache_users(user_ids=None, *args_):
        
        global wpdb
        php_check_if_defined("wpdb")
        clean = _get_non_cached_ids(user_ids, "users")
        if php_empty(lambda : clean):
            return
        # end if
        list = php_implode(",", clean)
        users = wpdb.get_results(str("SELECT * FROM ") + str(wpdb.users) + str(" WHERE ID IN (") + str(list) + str(")"))
        ids = Array()
        for user in users:
            update_user_caches(user)
            ids[-1] = user.ID
        # end for
        update_meta_cache("user", ids)
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
    def wp_mail(to=None, subject=None, message=None, headers="", attachments=Array(), *args_):
        
        #// Compact the input, apply the filters, and extract them back out.
        #// 
        #// Filters the wp_mail() arguments.
        #// 
        #// @since 2.2.0
        #// 
        #// @param array $args A compacted array of wp_mail() arguments, including the "to" email,
        #// subject, message, headers, and attachments values.
        #//
        atts = apply_filters("wp_mail", compact("to", "subject", "message", "headers", "attachments"))
        if (php_isset(lambda : atts["to"])):
            to = atts["to"]
        # end if
        if (not php_is_array(to)):
            to = php_explode(",", to)
        # end if
        if (php_isset(lambda : atts["subject"])):
            subject = atts["subject"]
        # end if
        if (php_isset(lambda : atts["message"])):
            message = atts["message"]
        # end if
        if (php_isset(lambda : atts["headers"])):
            headers = atts["headers"]
        # end if
        if (php_isset(lambda : atts["attachments"])):
            attachments = atts["attachments"]
        # end if
        if (not php_is_array(attachments)):
            attachments = php_explode("\n", php_str_replace("\r\n", "\n", attachments))
        # end if
        global phpmailer
        php_check_if_defined("phpmailer")
        #// (Re)create it, if it's gone missing.
        if (not type(phpmailer).__name__ == "PHPMailer"):
            php_include_file(ABSPATH + WPINC + "/class-phpmailer.php", once=True)
            php_include_file(ABSPATH + WPINC + "/class-smtp.php", once=True)
            phpmailer = php_new_class("PHPMailer", lambda : PHPMailer(True))
        # end if
        #// Headers.
        cc = Array()
        bcc = Array()
        reply_to = Array()
        if php_empty(lambda : headers):
            headers = Array()
        else:
            if (not php_is_array(headers)):
                #// Explode the headers out, so this function can take
                #// both string headers and an array of headers.
                tempheaders = php_explode("\n", php_str_replace("\r\n", "\n", headers))
            else:
                tempheaders = headers
            # end if
            headers = Array()
            #// If it's actually got contents.
            if (not php_empty(lambda : tempheaders)):
                #// Iterate through the raw headers.
                for header in tempheaders:
                    if php_strpos(header, ":") == False:
                        if False != php_stripos(header, "boundary="):
                            parts = php_preg_split("/boundary=/i", php_trim(header))
                            boundary = php_trim(php_str_replace(Array("'", "\""), "", parts[1]))
                        # end if
                        continue
                    # end if
                    #// Explode them out.
                    name, content = php_explode(":", php_trim(header), 2)
                    #// Cleanup crew.
                    name = php_trim(name)
                    content = php_trim(content)
                    for case in Switch(php_strtolower(name)):
                        if case("from"):
                            bracket_pos = php_strpos(content, "<")
                            if False != bracket_pos:
                                #// Text before the bracketed email is the "From" name.
                                if bracket_pos > 0:
                                    from_name = php_substr(content, 0, bracket_pos - 1)
                                    from_name = php_str_replace("\"", "", from_name)
                                    from_name = php_trim(from_name)
                                # end if
                                from_email = php_substr(content, bracket_pos + 1)
                                from_email = php_str_replace(">", "", from_email)
                                from_email = php_trim(from_email)
                                pass
                            elif "" != php_trim(content):
                                from_email = php_trim(content)
                            # end if
                            break
                        # end if
                        if case("content-type"):
                            if php_strpos(content, ";") != False:
                                type, charset_content = php_explode(";", content)
                                content_type = php_trim(type)
                                if False != php_stripos(charset_content, "charset="):
                                    charset = php_trim(php_str_replace(Array("charset=", "\""), "", charset_content))
                                elif False != php_stripos(charset_content, "boundary="):
                                    boundary = php_trim(php_str_replace(Array("BOUNDARY=", "boundary=", "\""), "", charset_content))
                                    charset = ""
                                # end if
                                pass
                            elif "" != php_trim(content):
                                content_type = php_trim(content)
                            # end if
                            break
                        # end if
                        if case("cc"):
                            cc = php_array_merge(cc, php_explode(",", content))
                            break
                        # end if
                        if case("bcc"):
                            bcc = php_array_merge(bcc, php_explode(",", content))
                            break
                        # end if
                        if case("reply-to"):
                            reply_to = php_array_merge(reply_to, php_explode(",", content))
                            break
                        # end if
                        if case():
                            #// Add it to our grand headers array.
                            headers[php_trim(name)] = php_trim(content)
                            break
                        # end if
                    # end for
                # end for
            # end if
        # end if
        #// Empty out the values that may be set.
        phpmailer.clearallrecipients()
        phpmailer.clearattachments()
        phpmailer.clearcustomheaders()
        phpmailer.clearreplytos()
        #// Set "From" name and email.
        #// If we don't have a name from the input headers.
        if (not (php_isset(lambda : from_name))):
            from_name = "WordPress"
        # end if
        #// 
        #// If we don't have an email from the input headers, default to wordpress@$sitename
        #// Some hosts will block outgoing mail from this address if it doesn't exist,
        #// but there's no easy alternative. Defaulting to admin_email might appear to be
        #// another option, but some hosts may refuse to relay mail from an unknown domain.
        #// See https://core.trac.wordpress.org/ticket/5007.
        #//
        if (not (php_isset(lambda : from_email))):
            #// Get the site domain and get rid of www.
            sitename = php_strtolower(PHP_SERVER["SERVER_NAME"])
            if php_substr(sitename, 0, 4) == "www.":
                sitename = php_substr(sitename, 4)
            # end if
            from_email = "wordpress@" + sitename
        # end if
        #// 
        #// Filters the email address to send from.
        #// 
        #// @since 2.2.0
        #// 
        #// @param string $from_email Email address to send from.
        #//
        from_email = apply_filters("wp_mail_from", from_email)
        #// 
        #// Filters the name to associate with the "from" email address.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $from_name Name associated with the "from" email address.
        #//
        from_name = apply_filters("wp_mail_from_name", from_name)
        try: 
            phpmailer.setfrom(from_email, from_name, False)
        except phpmailerException as e:
            mail_error_data = compact("to", "subject", "message", "headers", "attachments")
            mail_error_data["phpmailer_exception_code"] = e.getcode()
            #// This filter is documented in wp-includes/pluggable.php
            do_action("wp_mail_failed", php_new_class("WP_Error", lambda : WP_Error("wp_mail_failed", e.getmessage(), mail_error_data)))
            return False
        # end try
        #// Set mail's subject and body.
        phpmailer.Subject = subject
        phpmailer.Body = message
        #// Set destination addresses, using appropriate methods for handling addresses.
        address_headers = compact("to", "cc", "bcc", "reply_to")
        for address_header,addresses in address_headers:
            if php_empty(lambda : addresses):
                continue
            # end if
            for address in addresses:
                try: 
                    #// Break $recipient into name and address parts if in the format "Foo <bar@baz.com>".
                    recipient_name = ""
                    if php_preg_match("/(.*)<(.+)>/", address, matches):
                        if php_count(matches) == 3:
                            recipient_name = matches[1]
                            address = matches[2]
                        # end if
                    # end if
                    for case in Switch(address_header):
                        if case("to"):
                            phpmailer.addaddress(address, recipient_name)
                            break
                        # end if
                        if case("cc"):
                            phpmailer.addcc(address, recipient_name)
                            break
                        # end if
                        if case("bcc"):
                            phpmailer.addbcc(address, recipient_name)
                            break
                        # end if
                        if case("reply_to"):
                            phpmailer.addreplyto(address, recipient_name)
                            break
                        # end if
                    # end for
                except phpmailerException as e:
                    continue
                # end try
            # end for
        # end for
        #// Set to use PHP's mail().
        phpmailer.ismail()
        #// Set Content-Type and charset.
        #// If we don't have a content-type from the input headers.
        if (not (php_isset(lambda : content_type))):
            content_type = "text/plain"
        # end if
        #// 
        #// Filters the wp_mail() content type.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $content_type Default wp_mail() content type.
        #//
        content_type = apply_filters("wp_mail_content_type", content_type)
        phpmailer.ContentType = content_type
        #// Set whether it's plaintext, depending on $content_type.
        if "text/html" == content_type:
            phpmailer.ishtml(True)
        # end if
        #// If we don't have a charset from the input headers.
        if (not (php_isset(lambda : charset))):
            charset = get_bloginfo("charset")
        # end if
        #// 
        #// Filters the default wp_mail() charset.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $charset Default email charset.
        #//
        phpmailer.CharSet = apply_filters("wp_mail_charset", charset)
        #// Set custom headers.
        if (not php_empty(lambda : headers)):
            for name,content in headers:
                #// Only add custom headers not added automatically by PHPMailer.
                if (not php_in_array(name, Array("MIME-Version", "X-Mailer"))):
                    phpmailer.addcustomheader(php_sprintf("%1$s: %2$s", name, content))
                # end if
            # end for
            if False != php_stripos(content_type, "multipart") and (not php_empty(lambda : boundary)):
                phpmailer.addcustomheader(php_sprintf("Content-Type: %s;\n   boundary=\"%s\"", content_type, boundary))
            # end if
        # end if
        if (not php_empty(lambda : attachments)):
            for attachment in attachments:
                try: 
                    phpmailer.addattachment(attachment)
                except phpmailerException as e:
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
        do_action_ref_array("phpmailer_init", Array(phpmailer))
        #// Send!
        try: 
            return phpmailer.send()
        except phpmailerException as e:
            mail_error_data = compact("to", "subject", "message", "headers", "attachments")
            mail_error_data["phpmailer_exception_code"] = e.getcode()
            #// 
            #// Fires after a phpmailerException is caught.
            #// 
            #// @since 4.4.0
            #// 
            #// @param WP_Error $error A WP_Error object with the phpmailerException message, and an array
            #// containing the mail recipient, subject, message, headers, and attachments.
            #//
            do_action("wp_mail_failed", php_new_class("WP_Error", lambda : WP_Error("wp_mail_failed", e.getmessage(), mail_error_data)))
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
    def wp_authenticate(username=None, password=None, *args_):
        
        username = sanitize_user(username)
        password = php_trim(password)
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
        user = apply_filters("authenticate", None, username, password)
        if None == user:
            #// TODO: What should the error message be? (Or would these even happen?)
            #// Only needed if all authentication handlers fail to return anything.
            user = php_new_class("WP_Error", lambda : WP_Error("authentication_failed", __("<strong>Error</strong>: Invalid username, email address or incorrect password.")))
        # end if
        ignore_codes = Array("empty_username", "empty_password")
        if is_wp_error(user) and (not php_in_array(user.get_error_code(), ignore_codes)):
            error = user
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
            do_action("wp_login_failed", username, error)
        # end if
        return user
    # end def wp_authenticate
# end if
if (not php_function_exists("wp_logout")):
    #// 
    #// Log the current user out.
    #// 
    #// @since 2.5.0
    #//
    def wp_logout(*args_):
        
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
    def wp_validate_auth_cookie(cookie="", scheme="", *args_):
        global PHP_GLOBALS
        cookie_elements = wp_parse_auth_cookie(cookie, scheme)
        if (not cookie_elements):
            #// 
            #// Fires if an authentication cookie is malformed.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string $cookie Malformed auth cookie.
            #// @param string $scheme Authentication scheme. Values include 'auth', 'secure_auth',
            #// or 'logged_in'.
            #//
            do_action("auth_cookie_malformed", cookie, scheme)
            return False
        # end if
        scheme = cookie_elements["scheme"]
        username = cookie_elements["username"]
        hmac = cookie_elements["hmac"]
        token = cookie_elements["token"]
        expired = cookie_elements["expiration"]
        expiration = cookie_elements["expiration"]
        #// Allow a grace period for POST and Ajax requests.
        if wp_doing_ajax() or "POST" == PHP_SERVER["REQUEST_METHOD"]:
            expired += HOUR_IN_SECONDS
        # end if
        #// Quick check to see if an honest cookie has expired.
        if expired < time():
            #// 
            #// Fires once an authentication cookie has expired.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_expired", cookie_elements)
            return False
        # end if
        user = get_user_by("login", username)
        if (not user):
            #// 
            #// Fires if a bad username is entered in the user authentication process.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_bad_username", cookie_elements)
            return False
        # end if
        pass_frag = php_substr(user.user_pass, 8, 4)
        key = wp_hash(username + "|" + pass_frag + "|" + expiration + "|" + token, scheme)
        #// If ext/hash is not present, compat.php's hash_hmac() does not support sha256.
        algo = "sha256" if php_function_exists("hash") else "sha1"
        hash = hash_hmac(algo, username + "|" + expiration + "|" + token, key)
        if (not hash_equals(hash, hmac)):
            #// 
            #// Fires if a bad authentication cookie hash is encountered.
            #// 
            #// @since 2.7.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_bad_hash", cookie_elements)
            return False
        # end if
        manager = WP_Session_Tokens.get_instance(user.ID)
        if (not manager.verify(token)):
            #// 
            #// Fires if a bad session token is encountered.
            #// 
            #// @since 4.0.0
            #// 
            #// @param string[] $cookie_elements An array of data for the authentication cookie.
            #//
            do_action("auth_cookie_bad_session_token", cookie_elements)
            return False
        # end if
        #// Ajax/POST grace period set above.
        if expiration < time():
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
        do_action("auth_cookie_valid", cookie_elements, user)
        return user.ID
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
    def wp_generate_auth_cookie(user_id=None, expiration=None, scheme="auth", token="", *args_):
        
        user = get_userdata(user_id)
        if (not user):
            return ""
        # end if
        if (not token):
            manager = WP_Session_Tokens.get_instance(user_id)
            token = manager.create(expiration)
        # end if
        pass_frag = php_substr(user.user_pass, 8, 4)
        key = wp_hash(user.user_login + "|" + pass_frag + "|" + expiration + "|" + token, scheme)
        #// If ext/hash is not present, compat.php's hash_hmac() does not support sha256.
        algo = "sha256" if php_function_exists("hash") else "sha1"
        hash = hash_hmac(algo, user.user_login + "|" + expiration + "|" + token, key)
        cookie = user.user_login + "|" + expiration + "|" + token + "|" + hash
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
        return apply_filters("auth_cookie", cookie, user_id, expiration, scheme, token)
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
    def wp_parse_auth_cookie(cookie="", scheme="", *args_):
        
        if php_empty(lambda : cookie):
            for case in Switch(scheme):
                if case("auth"):
                    cookie_name = AUTH_COOKIE
                    break
                # end if
                if case("secure_auth"):
                    cookie_name = SECURE_AUTH_COOKIE
                    break
                # end if
                if case("logged_in"):
                    cookie_name = LOGGED_IN_COOKIE
                    break
                # end if
                if case():
                    if is_ssl():
                        cookie_name = SECURE_AUTH_COOKIE
                        scheme = "secure_auth"
                    else:
                        cookie_name = AUTH_COOKIE
                        scheme = "auth"
                    # end if
                # end if
            # end for
            if php_empty(lambda : PHP_COOKIE[cookie_name]):
                return False
            # end if
            cookie = PHP_COOKIE[cookie_name]
        # end if
        cookie_elements = php_explode("|", cookie)
        if php_count(cookie_elements) != 4:
            return False
        # end if
        username, expiration, token, hmac = cookie_elements
        return compact("username", "expiration", "token", "hmac", "scheme")
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
    def wp_set_auth_cookie(user_id=None, remember=False, secure="", token="", *args_):
        
        if remember:
            #// 
            #// Filters the duration of the authentication cookie expiration period.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int  $length   Duration of the expiration period in seconds.
            #// @param int  $user_id  User ID.
            #// @param bool $remember Whether to remember the user login. Default false.
            #//
            expiration = time() + apply_filters("auth_cookie_expiration", 14 * DAY_IN_SECONDS, user_id, remember)
            #// 
            #// Ensure the browser will continue to send the cookie after the expiration time is reached.
            #// Needed for the login grace period in wp_validate_auth_cookie().
            #//
            expire = expiration + 12 * HOUR_IN_SECONDS
        else:
            #// This filter is documented in wp-includes/pluggable.php
            expiration = time() + apply_filters("auth_cookie_expiration", 2 * DAY_IN_SECONDS, user_id, remember)
            expire = 0
        # end if
        if "" == secure:
            secure = is_ssl()
        # end if
        #// Front-end cookie is secure when the auth cookie is secure and the site's home URL uses HTTPS.
        secure_logged_in_cookie = secure and "https" == php_parse_url(get_option("home"), PHP_URL_SCHEME)
        #// 
        #// Filters whether the auth cookie should only be sent over HTTPS.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool $secure  Whether the cookie should only be sent over HTTPS.
        #// @param int  $user_id User ID.
        #//
        secure = apply_filters("secure_auth_cookie", secure, user_id)
        #// 
        #// Filters whether the logged in cookie should only be sent over HTTPS.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool $secure_logged_in_cookie Whether the logged in cookie should only be sent over HTTPS.
        #// @param int  $user_id                 User ID.
        #// @param bool $secure                  Whether the auth cookie should only be sent over HTTPS.
        #//
        secure_logged_in_cookie = apply_filters("secure_logged_in_cookie", secure_logged_in_cookie, user_id, secure)
        if secure:
            auth_cookie_name = SECURE_AUTH_COOKIE
            scheme = "secure_auth"
        else:
            auth_cookie_name = AUTH_COOKIE
            scheme = "auth"
        # end if
        if "" == token:
            manager = WP_Session_Tokens.get_instance(user_id)
            token = manager.create(expiration)
        # end if
        auth_cookie = wp_generate_auth_cookie(user_id, expiration, scheme, token)
        logged_in_cookie = wp_generate_auth_cookie(user_id, expiration, "logged_in", token)
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
        do_action("set_auth_cookie", auth_cookie, expire, expiration, user_id, scheme, token)
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
        do_action("set_logged_in_cookie", logged_in_cookie, expire, expiration, user_id, "logged_in", token)
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
        setcookie(auth_cookie_name, auth_cookie, expire, PLUGINS_COOKIE_PATH, COOKIE_DOMAIN, secure, True)
        setcookie(auth_cookie_name, auth_cookie, expire, ADMIN_COOKIE_PATH, COOKIE_DOMAIN, secure, True)
        setcookie(LOGGED_IN_COOKIE, logged_in_cookie, expire, COOKIEPATH, COOKIE_DOMAIN, secure_logged_in_cookie, True)
        if COOKIEPATH != SITECOOKIEPATH:
            setcookie(LOGGED_IN_COOKIE, logged_in_cookie, expire, SITECOOKIEPATH, COOKIE_DOMAIN, secure_logged_in_cookie, True)
        # end if
    # end def wp_set_auth_cookie
# end if
if (not php_function_exists("wp_clear_auth_cookie")):
    #// 
    #// Removes all of the cookies associated with authentication.
    #// 
    #// @since 2.5.0
    #//
    def wp_clear_auth_cookie(*args_):
        
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
    def is_user_logged_in(*args_):
        
        user = wp_get_current_user()
        return user.exists()
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
    def auth_redirect(*args_):
        
        secure = is_ssl() or force_ssl_admin()
        #// 
        #// Filters whether to use a secure authentication redirect.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool $secure Whether to use a secure authentication redirect. Default false.
        #//
        secure = apply_filters("secure_auth_redirect", secure)
        #// If https is required and request is http, redirect.
        if secure and (not is_ssl()) and False != php_strpos(PHP_SERVER["REQUEST_URI"], "wp-admin"):
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
        scheme = apply_filters("auth_redirect_scheme", "")
        user_id = wp_validate_auth_cookie("", scheme)
        if user_id:
            #// 
            #// Fires before the authentication redirect.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int $user_id User ID.
            #//
            do_action("auth_redirect", user_id)
            #// If the user wants ssl but the session is not ssl, redirect.
            if (not secure) and get_user_option("use_ssl", user_id) and False != php_strpos(PHP_SERVER["REQUEST_URI"], "wp-admin"):
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
        redirect = wp_get_referer() if php_strpos(PHP_SERVER["REQUEST_URI"], "/options.php") and wp_get_referer() else set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
        login_url = wp_login_url(redirect, True)
        wp_redirect(login_url)
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
    def check_admin_referer(action=-1, query_arg="_wpnonce", *args_):
        
        if -1 == action:
            _doing_it_wrong(__FUNCTION__, __("You should specify a nonce action to be verified by using the first parameter."), "3.2.0")
        # end if
        adminurl = php_strtolower(admin_url())
        referer = php_strtolower(wp_get_referer())
        result = wp_verify_nonce(PHP_REQUEST[query_arg], action) if (php_isset(lambda : PHP_REQUEST[query_arg])) else False
        #// 
        #// Fires once the admin request has been validated or not.
        #// 
        #// @since 1.5.1
        #// 
        #// @param string    $action The nonce action.
        #// @param false|int $result False if the nonce is invalid, 1 if the nonce is valid and generated between
        #// 0-12 hours ago, 2 if the nonce is valid and generated between 12-24 hours ago.
        #//
        do_action("check_admin_referer", action, result)
        if (not result) and (not -1 == action and php_strpos(referer, adminurl) == 0):
            wp_nonce_ays(action)
            php_exit(0)
        # end if
        return result
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
    def check_ajax_referer(action=-1, query_arg=False, die=True, *args_):
        
        if -1 == action:
            _doing_it_wrong(__FUNCTION__, __("You should specify a nonce action to be verified by using the first parameter."), "4.7")
        # end if
        nonce = ""
        if query_arg and (php_isset(lambda : PHP_REQUEST[query_arg])):
            nonce = PHP_REQUEST[query_arg]
        elif (php_isset(lambda : PHP_REQUEST["_ajax_nonce"])):
            nonce = PHP_REQUEST["_ajax_nonce"]
        elif (php_isset(lambda : PHP_REQUEST["_wpnonce"])):
            nonce = PHP_REQUEST["_wpnonce"]
        # end if
        result = wp_verify_nonce(nonce, action)
        #// 
        #// Fires once the Ajax request has been validated or not.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string    $action The Ajax nonce action.
        #// @param false|int $result False if the nonce is invalid, 1 if the nonce is valid and generated between
        #// 0-12 hours ago, 2 if the nonce is valid and generated between 12-24 hours ago.
        #//
        do_action("check_ajax_referer", action, result)
        if die and False == result:
            if wp_doing_ajax():
                wp_die(-1, 403)
            else:
                php_print("-1")
                php_exit()
            # end if
        # end if
        return result
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
    def wp_redirect(location=None, status=302, x_redirect_by="WordPress", *args_):
        
        global is_IIS
        php_check_if_defined("is_IIS")
        #// 
        #// Filters the redirect location.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $location The path or URL to redirect to.
        #// @param int    $status   The HTTP response status code to use.
        #//
        location = apply_filters("wp_redirect", location, status)
        #// 
        #// Filters the redirect HTTP response status code to use.
        #// 
        #// @since 2.3.0
        #// 
        #// @param int    $status   The HTTP response status code to use.
        #// @param string $location The path or URL to redirect to.
        #//
        status = apply_filters("wp_redirect_status", status, location)
        if (not location):
            return False
        # end if
        if status < 300 or 399 < status:
            wp_die(__("HTTP redirect status code must be a redirection code, 3xx."))
        # end if
        location = wp_sanitize_redirect(location)
        if (not is_IIS) and PHP_SAPI != "cgi-fcgi":
            status_header(status)
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
        x_redirect_by = apply_filters("x_redirect_by", x_redirect_by, status, location)
        if php_is_string(x_redirect_by):
            php_header(str("X-Redirect-By: ") + str(x_redirect_by))
        # end if
        php_header(str("Location: ") + str(location), True, status)
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
    def wp_sanitize_redirect(location=None, *args_):
        
        #// Encode spaces.
        location = php_str_replace(" ", "%20", location)
        regex = """/
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
        location = preg_replace_callback(regex, "_wp_sanitize_utf8_in_redirect", location)
        location = php_preg_replace("|[^a-z0-9-~+_.?#=&;,/:%!*\\[\\]()@]|i", "", location)
        location = wp_kses_no_null(location)
        #// Remove %0D and %0A from location.
        strip = Array("%0d", "%0a", "%0D", "%0A")
        return _deep_replace(strip, location)
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
    def _wp_sanitize_utf8_in_redirect(matches=None, *args_):
        
        return urlencode(matches[0])
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
    def wp_safe_redirect(location=None, status=302, x_redirect_by="WordPress", *args_):
        
        #// Need to look at the URL the way it will end up in wp_redirect().
        location = wp_sanitize_redirect(location)
        #// 
        #// Filters the redirect fallback URL for when the provided redirect is not safe (local).
        #// 
        #// @since 4.3.0
        #// 
        #// @param string $fallback_url The fallback URL to use by default.
        #// @param int    $status       The HTTP response status code to use.
        #//
        location = wp_validate_redirect(location, apply_filters("wp_safe_redirect_fallback", admin_url(), status))
        return wp_redirect(location, status, x_redirect_by)
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
    def wp_validate_redirect(location=None, default="", *args_):
        
        location = php_trim(location, "     \n\r ")
        #// Browsers will assume 'http' is your protocol, and will obey a redirect to a URL starting with '//'.
        if php_substr(location, 0, 2) == "//":
            location = "http:" + location
        # end if
        #// In PHP 5 parse_url() may fail if the URL query part contains 'http://'.
        #// See https://bugs.php.net/bug.php?id=38143
        cut = php_strpos(location, "?")
        test = php_substr(location, 0, cut) if cut else location
        #// @-operator is used to prevent possible warnings in PHP < 5.3.3.
        lp = php_no_error(lambda: php_parse_url(test))
        #// Give up if malformed URL.
        if False == lp:
            return default
        # end if
        #// Allow only 'http' and 'https' schemes. No 'data:', etc.
        if (php_isset(lambda : lp["scheme"])) and (not "http" == lp["scheme"] or "https" == lp["scheme"]):
            return default
        # end if
        if (not (php_isset(lambda : lp["host"]))) and (not php_empty(lambda : lp["path"])) and "/" != lp["path"][0]:
            path = ""
            if (not php_empty(lambda : PHP_SERVER["REQUEST_URI"])):
                path = php_dirname(php_parse_url("http://placeholder" + PHP_SERVER["REQUEST_URI"], PHP_URL_PATH) + "?")
                path = wp_normalize_path(path)
            # end if
            location = "/" + php_ltrim(path + "/", "/") + location
        # end if
        #// Reject if certain components are set but host is not.
        #// This catches URLs like https:host.com for which parse_url() does not set the host field.
        if (not (php_isset(lambda : lp["host"]))) and (php_isset(lambda : lp["scheme"])) or (php_isset(lambda : lp["user"])) or (php_isset(lambda : lp["pass"])) or (php_isset(lambda : lp["port"])):
            return default
        # end if
        #// Reject malformed components parse_url() can return on odd inputs.
        for component in Array("user", "pass", "host"):
            if (php_isset(lambda : lp[component])) and strpbrk(lp[component], ":/?#@"):
                return default
            # end if
        # end for
        wpp = php_parse_url(home_url())
        #// 
        #// Filters the whitelist of hosts to redirect to.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string[] $hosts An array of allowed host names.
        #// @param string   $host  The host name of the redirect destination; empty string if not set.
        #//
        allowed_hosts = apply_filters("allowed_redirect_hosts", Array(wpp["host"]), lp["host"] if (php_isset(lambda : lp["host"])) else "")
        if (php_isset(lambda : lp["host"])) and (not php_in_array(lp["host"], allowed_hosts)) and php_strtolower(wpp["host"]) != lp["host"]:
            location = default
        # end if
        return location
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
    def wp_notify_postauthor(comment_id=None, deprecated=None, *args_):
        
        if None != deprecated:
            _deprecated_argument(__FUNCTION__, "3.8.0")
        # end if
        comment = get_comment(comment_id)
        if php_empty(lambda : comment) or php_empty(lambda : comment.comment_post_ID):
            return False
        # end if
        post = get_post(comment.comment_post_ID)
        author = get_userdata(post.post_author)
        #// Who to notify? By default, just the post author, but others can be added.
        emails = Array()
        if author:
            emails[-1] = author.user_email
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
        emails = apply_filters("comment_notification_recipients", emails, comment.comment_ID)
        emails = php_array_filter(emails)
        #// If there are no addresses to send the comment to, bail.
        if (not php_count(emails)):
            return False
        # end if
        #// Facilitate unsetting below without knowing the keys.
        emails = php_array_flip(emails)
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
        notify_author = apply_filters("comment_notification_notify_author", False, comment.comment_ID)
        #// The comment was left by the author.
        if author and (not notify_author) and comment.user_id == post.post_author:
            emails[author.user_email] = None
        # end if
        #// The author moderated a comment on their own post.
        if author and (not notify_author) and get_current_user_id() == post.post_author:
            emails[author.user_email] = None
        # end if
        #// The post author is no longer a member of the blog.
        if author and (not notify_author) and (not user_can(post.post_author, "read_post", post.ID)):
            emails[author.user_email] = None
        # end if
        #// If there's no email to send the comment to, bail, otherwise flip array back around for use below.
        if (not php_count(emails)):
            return False
        else:
            emails = php_array_flip(emails)
        # end if
        switched_locale = switch_to_locale(get_locale())
        comment_author_domain = ""
        if WP_Http.is_ip_address(comment.comment_author_IP):
            comment_author_domain = gethostbyaddr(comment.comment_author_IP)
        # end if
        #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
        #// We want to reverse this for the plain text arena of emails.
        blogname = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        comment_content = wp_specialchars_decode(comment.comment_content)
        for case in Switch(comment.comment_type):
            if case("trackback"):
                #// translators: %s: Post title.
                notify_message = php_sprintf(__("New trackback on your post \"%s\""), post.post_title) + "\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment.comment_author, comment.comment_author_IP, comment_author_domain) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message += php_sprintf(__("URL: %s"), comment.comment_author_url) + "\r\n"
                #// translators: %s: Comment text.
                notify_message += php_sprintf(__("Comment: %s"), "\r\n" + comment_content) + "\r\n\r\n"
                notify_message += __("You can see all trackbacks on this post here:") + "\r\n"
                #// translators: Trackback notification email subject. 1: Site title, 2: Post title.
                subject = php_sprintf(__("[%1$s] Trackback: \"%2$s\""), blogname, post.post_title)
                break
            # end if
            if case("pingback"):
                #// translators: %s: Post title.
                notify_message = php_sprintf(__("New pingback on your post \"%s\""), post.post_title) + "\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment.comment_author, comment.comment_author_IP, comment_author_domain) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message += php_sprintf(__("URL: %s"), comment.comment_author_url) + "\r\n"
                #// translators: %s: Comment text.
                notify_message += php_sprintf(__("Comment: %s"), "\r\n" + comment_content) + "\r\n\r\n"
                notify_message += __("You can see all pingbacks on this post here:") + "\r\n"
                #// translators: Pingback notification email subject. 1: Site title, 2: Post title.
                subject = php_sprintf(__("[%1$s] Pingback: \"%2$s\""), blogname, post.post_title)
                break
            # end if
            if case():
                #// Comments.
                #// translators: %s: Post title.
                notify_message = php_sprintf(__("New comment on your post \"%s\""), post.post_title) + "\r\n"
                #// translators: 1: Comment author's name, 2: Comment author's IP address, 3: Comment author's hostname.
                notify_message += php_sprintf(__("Author: %1$s (IP address: %2$s, %3$s)"), comment.comment_author, comment.comment_author_IP, comment_author_domain) + "\r\n"
                #// translators: %s: Comment author email.
                notify_message += php_sprintf(__("Email: %s"), comment.comment_author_email) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message += php_sprintf(__("URL: %s"), comment.comment_author_url) + "\r\n"
                if comment.comment_parent and user_can(post.post_author, "edit_comment", comment.comment_parent):
                    #// translators: Comment moderation. %s: Parent comment edit URL.
                    notify_message += php_sprintf(__("In reply to: %s"), admin_url(str("comment.php?action=editcomment&c=") + str(comment.comment_parent) + str("#wpbody-content"))) + "\r\n"
                # end if
                #// translators: %s: Comment text.
                notify_message += php_sprintf(__("Comment: %s"), "\r\n" + comment_content) + "\r\n\r\n"
                notify_message += __("You can see all comments on this post here:") + "\r\n"
                #// translators: Comment notification email subject. 1: Site title, 2: Post title.
                subject = php_sprintf(__("[%1$s] Comment: \"%2$s\""), blogname, post.post_title)
                break
            # end if
        # end for
        notify_message += get_permalink(comment.comment_post_ID) + "#comments\r\n\r\n"
        #// translators: %s: Comment URL.
        notify_message += php_sprintf(__("Permalink: %s"), get_comment_link(comment)) + "\r\n"
        if user_can(post.post_author, "edit_comment", comment.comment_ID):
            if EMPTY_TRASH_DAYS:
                #// translators: Comment moderation. %s: Comment action URL.
                notify_message += php_sprintf(__("Trash it: %s"), admin_url(str("comment.php?action=trash&c=") + str(comment.comment_ID) + str("#wpbody-content"))) + "\r\n"
            else:
                #// translators: Comment moderation. %s: Comment action URL.
                notify_message += php_sprintf(__("Delete it: %s"), admin_url(str("comment.php?action=delete&c=") + str(comment.comment_ID) + str("#wpbody-content"))) + "\r\n"
            # end if
            #// translators: Comment moderation. %s: Comment action URL.
            notify_message += php_sprintf(__("Spam it: %s"), admin_url(str("comment.php?action=spam&c=") + str(comment.comment_ID) + str("#wpbody-content"))) + "\r\n"
        # end if
        wp_email = "wordpress@" + php_preg_replace("#^www\\.#", "", php_strtolower(PHP_SERVER["SERVER_NAME"]))
        if "" == comment.comment_author:
            from_ = str("From: \"") + str(blogname) + str("\" <") + str(wp_email) + str(">")
            if "" != comment.comment_author_email:
                reply_to = str("Reply-To: ") + str(comment.comment_author_email)
            # end if
        else:
            from_ = str("From: \"") + str(comment.comment_author) + str("\" <") + str(wp_email) + str(">")
            if "" != comment.comment_author_email:
                reply_to = str("Reply-To: \"") + str(comment.comment_author_email) + str("\" <") + str(comment.comment_author_email) + str(">")
            # end if
        # end if
        message_headers = str(from_) + str("\n") + "Content-Type: text/plain; charset=\"" + get_option("blog_charset") + "\"\n"
        if (php_isset(lambda : reply_to)):
            message_headers += reply_to + "\n"
        # end if
        #// 
        #// Filters the comment notification email text.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $notify_message The comment notification email text.
        #// @param int    $comment_id     Comment ID.
        #//
        notify_message = apply_filters("comment_notification_text", notify_message, comment.comment_ID)
        #// 
        #// Filters the comment notification email subject.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $subject    The comment notification email subject.
        #// @param int    $comment_id Comment ID.
        #//
        subject = apply_filters("comment_notification_subject", subject, comment.comment_ID)
        #// 
        #// Filters the comment notification email headers.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $message_headers Headers for the comment notification email.
        #// @param int    $comment_id      Comment ID.
        #//
        message_headers = apply_filters("comment_notification_headers", message_headers, comment.comment_ID)
        for email in emails:
            wp_mail(email, wp_specialchars_decode(subject), notify_message, message_headers)
        # end for
        if switched_locale:
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
    def wp_notify_moderator(comment_id=None, *args_):
        
        global wpdb
        php_check_if_defined("wpdb")
        maybe_notify = get_option("moderation_notify")
        #// 
        #// Filters whether to send the site moderator email notifications, overriding the site setting.
        #// 
        #// @since 4.4.0
        #// 
        #// @param bool $maybe_notify Whether to notify blog moderator.
        #// @param int  $comment_ID   The id of the comment for the notification.
        #//
        maybe_notify = apply_filters("notify_moderator", maybe_notify, comment_id)
        if (not maybe_notify):
            return True
        # end if
        comment = get_comment(comment_id)
        post = get_post(comment.comment_post_ID)
        user = get_userdata(post.post_author)
        #// Send to the administration and to the post author if the author can modify the comment.
        emails = Array(get_option("admin_email"))
        if user and user_can(user.ID, "edit_comment", comment_id) and (not php_empty(lambda : user.user_email)):
            if 0 != strcasecmp(user.user_email, get_option("admin_email")):
                emails[-1] = user.user_email
            # end if
        # end if
        switched_locale = switch_to_locale(get_locale())
        comment_author_domain = ""
        if WP_Http.is_ip_address(comment.comment_author_IP):
            comment_author_domain = gethostbyaddr(comment.comment_author_IP)
        # end if
        comments_waiting = wpdb.get_var(str("SELECT COUNT(*) FROM ") + str(wpdb.comments) + str(" WHERE comment_approved = '0'"))
        #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
        #// We want to reverse this for the plain text arena of emails.
        blogname = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        comment_content = wp_specialchars_decode(comment.comment_content)
        for case in Switch(comment.comment_type):
            if case("trackback"):
                #// translators: %s: Post title.
                notify_message = php_sprintf(__("A new trackback on the post \"%s\" is waiting for your approval"), post.post_title) + "\r\n"
                notify_message += get_permalink(comment.comment_post_ID) + "\r\n\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment.comment_author, comment.comment_author_IP, comment_author_domain) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message += php_sprintf(__("URL: %s"), comment.comment_author_url) + "\r\n"
                notify_message += __("Trackback excerpt: ") + "\r\n" + comment_content + "\r\n\r\n"
                break
            # end if
            if case("pingback"):
                #// translators: %s: Post title.
                notify_message = php_sprintf(__("A new pingback on the post \"%s\" is waiting for your approval"), post.post_title) + "\r\n"
                notify_message += get_permalink(comment.comment_post_ID) + "\r\n\r\n"
                #// translators: 1: Trackback/pingback website name, 2: Website IP address, 3: Website hostname.
                notify_message += php_sprintf(__("Website: %1$s (IP address: %2$s, %3$s)"), comment.comment_author, comment.comment_author_IP, comment_author_domain) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message += php_sprintf(__("URL: %s"), comment.comment_author_url) + "\r\n"
                notify_message += __("Pingback excerpt: ") + "\r\n" + comment_content + "\r\n\r\n"
                break
            # end if
            if case():
                #// Comments.
                #// translators: %s: Post title.
                notify_message = php_sprintf(__("A new comment on the post \"%s\" is waiting for your approval"), post.post_title) + "\r\n"
                notify_message += get_permalink(comment.comment_post_ID) + "\r\n\r\n"
                #// translators: 1: Comment author's name, 2: Comment author's IP address, 3: Comment author's hostname.
                notify_message += php_sprintf(__("Author: %1$s (IP address: %2$s, %3$s)"), comment.comment_author, comment.comment_author_IP, comment_author_domain) + "\r\n"
                #// translators: %s: Comment author email.
                notify_message += php_sprintf(__("Email: %s"), comment.comment_author_email) + "\r\n"
                #// translators: %s: Trackback/pingback/comment author URL.
                notify_message += php_sprintf(__("URL: %s"), comment.comment_author_url) + "\r\n"
                if comment.comment_parent:
                    #// translators: Comment moderation. %s: Parent comment edit URL.
                    notify_message += php_sprintf(__("In reply to: %s"), admin_url(str("comment.php?action=editcomment&c=") + str(comment.comment_parent) + str("#wpbody-content"))) + "\r\n"
                # end if
                #// translators: %s: Comment text.
                notify_message += php_sprintf(__("Comment: %s"), "\r\n" + comment_content) + "\r\n\r\n"
                break
            # end if
        # end for
        #// translators: Comment moderation. %s: Comment action URL.
        notify_message += php_sprintf(__("Approve it: %s"), admin_url(str("comment.php?action=approve&c=") + str(comment_id) + str("#wpbody-content"))) + "\r\n"
        if EMPTY_TRASH_DAYS:
            #// translators: Comment moderation. %s: Comment action URL.
            notify_message += php_sprintf(__("Trash it: %s"), admin_url(str("comment.php?action=trash&c=") + str(comment_id) + str("#wpbody-content"))) + "\r\n"
        else:
            #// translators: Comment moderation. %s: Comment action URL.
            notify_message += php_sprintf(__("Delete it: %s"), admin_url(str("comment.php?action=delete&c=") + str(comment_id) + str("#wpbody-content"))) + "\r\n"
        # end if
        #// translators: Comment moderation. %s: Comment action URL.
        notify_message += php_sprintf(__("Spam it: %s"), admin_url(str("comment.php?action=spam&c=") + str(comment_id) + str("#wpbody-content"))) + "\r\n"
        notify_message += php_sprintf(_n("Currently %s comment is waiting for approval. Please visit the moderation panel:", "Currently %s comments are waiting for approval. Please visit the moderation panel:", comments_waiting), number_format_i18n(comments_waiting)) + "\r\n"
        notify_message += admin_url("edit-comments.php?comment_status=moderated#wpbody-content") + "\r\n"
        #// translators: Comment moderation notification email subject. 1: Site title, 2: Post title.
        subject = php_sprintf(__("[%1$s] Please moderate: \"%2$s\""), blogname, post.post_title)
        message_headers = ""
        #// 
        #// Filters the list of recipients for comment moderation emails.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string[] $emails     List of email addresses to notify for comment moderation.
        #// @param int      $comment_id Comment ID.
        #//
        emails = apply_filters("comment_moderation_recipients", emails, comment_id)
        #// 
        #// Filters the comment moderation email text.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $notify_message Text of the comment moderation email.
        #// @param int    $comment_id     Comment ID.
        #//
        notify_message = apply_filters("comment_moderation_text", notify_message, comment_id)
        #// 
        #// Filters the comment moderation email subject.
        #// 
        #// @since 1.5.2
        #// 
        #// @param string $subject    Subject of the comment moderation email.
        #// @param int    $comment_id Comment ID.
        #//
        subject = apply_filters("comment_moderation_subject", subject, comment_id)
        #// 
        #// Filters the comment moderation email headers.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $message_headers Headers for the comment moderation email.
        #// @param int    $comment_id      Comment ID.
        #//
        message_headers = apply_filters("comment_moderation_headers", message_headers, comment_id)
        for email in emails:
            wp_mail(email, wp_specialchars_decode(subject), notify_message, message_headers)
        # end for
        if switched_locale:
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
    def wp_password_change_notification(user=None, *args_):
        
        #// Send a copy of password change notification to the admin,
        #// but check to see if it's the admin whose password we're changing, and skip this.
        if 0 != strcasecmp(user.user_email, get_option("admin_email")):
            #// translators: %s: User name.
            message = php_sprintf(__("Password changed for user: %s"), user.user_login) + "\r\n"
            #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
            #// We want to reverse this for the plain text arena of emails.
            blogname = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
            wp_password_change_notification_email = Array({"to": get_option("admin_email"), "subject": __("[%s] Password Changed"), "message": message, "headers": ""})
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
            wp_password_change_notification_email = apply_filters("wp_password_change_notification_email", wp_password_change_notification_email, user, blogname)
            wp_mail(wp_password_change_notification_email["to"], wp_specialchars_decode(php_sprintf(wp_password_change_notification_email["subject"], blogname)), wp_password_change_notification_email["message"], wp_password_change_notification_email["headers"])
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
    def wp_new_user_notification(user_id=None, deprecated=None, notify="", *args_):
        
        if None != deprecated:
            _deprecated_argument(__FUNCTION__, "4.3.1")
        # end if
        #// Accepts only 'user', 'admin' , 'both' or default '' as $notify.
        if (not php_in_array(notify, Array("user", "admin", "both", ""), True)):
            return
        # end if
        user = get_userdata(user_id)
        #// The blogname option is escaped with esc_html() on the way into the database in sanitize_option().
        #// We want to reverse this for the plain text arena of emails.
        blogname = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
        if "user" != notify:
            switched_locale = switch_to_locale(get_locale())
            #// translators: %s: Site title.
            message = php_sprintf(__("New user registration on your site %s:"), blogname) + "\r\n\r\n"
            #// translators: %s: User login.
            message += php_sprintf(__("Username: %s"), user.user_login) + "\r\n\r\n"
            #// translators: %s: User email address.
            message += php_sprintf(__("Email: %s"), user.user_email) + "\r\n"
            wp_new_user_notification_email_admin = Array({"to": get_option("admin_email"), "subject": __("[%s] New User Registration"), "message": message, "headers": ""})
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
            wp_new_user_notification_email_admin = apply_filters("wp_new_user_notification_email_admin", wp_new_user_notification_email_admin, user, blogname)
            wp_mail(wp_new_user_notification_email_admin["to"], wp_specialchars_decode(php_sprintf(wp_new_user_notification_email_admin["subject"], blogname)), wp_new_user_notification_email_admin["message"], wp_new_user_notification_email_admin["headers"])
            if switched_locale:
                restore_previous_locale()
            # end if
        # end if
        #// `$deprecated` was pre-4.3 `$plaintext_pass`. An empty `$plaintext_pass` didn't sent a user notification.
        if "admin" == notify or php_empty(lambda : deprecated) and php_empty(lambda : notify):
            return
        # end if
        key = get_password_reset_key(user)
        if is_wp_error(key):
            return
        # end if
        switched_locale = switch_to_locale(get_user_locale(user))
        #// translators: %s: User login.
        message = php_sprintf(__("Username: %s"), user.user_login) + "\r\n\r\n"
        message += __("To set your password, visit the following address:") + "\r\n\r\n"
        message += network_site_url(str("wp-login.php?action=rp&key=") + str(key) + str("&login=") + rawurlencode(user.user_login), "login") + "\r\n\r\n"
        message += wp_login_url() + "\r\n"
        wp_new_user_notification_email = Array({"to": user.user_email, "subject": __("[%s] Login Details"), "message": message, "headers": ""})
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
        wp_new_user_notification_email = apply_filters("wp_new_user_notification_email", wp_new_user_notification_email, user, blogname)
        wp_mail(wp_new_user_notification_email["to"], wp_specialchars_decode(php_sprintf(wp_new_user_notification_email["subject"], blogname)), wp_new_user_notification_email["message"], wp_new_user_notification_email["headers"])
        if switched_locale:
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
    def wp_nonce_tick(*args_):
        
        #// 
        #// Filters the lifespan of nonces in seconds.
        #// 
        #// @since 2.5.0
        #// 
        #// @param int $lifespan Lifespan of nonces in seconds. Default 86,400 seconds, or one day.
        #//
        nonce_life = apply_filters("nonce_life", DAY_IN_SECONDS)
        return ceil(time() / nonce_life / 2)
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
    def wp_verify_nonce(nonce=None, action=-1, *args_):
        
        nonce = str(nonce)
        user = wp_get_current_user()
        uid = int(user.ID)
        if (not uid):
            #// 
            #// Filters whether the user who generated the nonce is logged out.
            #// 
            #// @since 3.5.0
            #// 
            #// @param int    $uid    ID of the nonce-owning user.
            #// @param string $action The nonce action.
            #//
            uid = apply_filters("nonce_user_logged_out", uid, action)
        # end if
        if php_empty(lambda : nonce):
            return False
        # end if
        token = wp_get_session_token()
        i = wp_nonce_tick()
        #// Nonce generated 0-12 hours ago.
        expected = php_substr(wp_hash(i + "|" + action + "|" + uid + "|" + token, "nonce"), -12, 10)
        if hash_equals(expected, nonce):
            return 1
        # end if
        #// Nonce generated 12-24 hours ago.
        expected = php_substr(wp_hash(i - 1 + "|" + action + "|" + uid + "|" + token, "nonce"), -12, 10)
        if hash_equals(expected, nonce):
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
        do_action("wp_verify_nonce_failed", nonce, action, user, token)
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
    def wp_create_nonce(action=-1, *args_):
        
        user = wp_get_current_user()
        uid = int(user.ID)
        if (not uid):
            #// This filter is documented in wp-includes/pluggable.php
            uid = apply_filters("nonce_user_logged_out", uid, action)
        # end if
        token = wp_get_session_token()
        i = wp_nonce_tick()
        return php_substr(wp_hash(i + "|" + action + "|" + uid + "|" + token, "nonce"), -12, 10)
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
    def wp_salt(scheme="auth", *args_):
        
        cached_salts = Array()
        if (php_isset(lambda : cached_salts[scheme])):
            #// 
            #// Filters the WordPress salt.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string $cached_salt Cached salt for the given scheme.
            #// @param string $scheme      Authentication scheme. Values include 'auth',
            #// 'secure_auth', 'logged_in', and 'nonce'.
            #//
            return apply_filters("salt", cached_salts[scheme], scheme)
        # end if
        duplicated_keys = None
        if None == duplicated_keys:
            duplicated_keys = Array({"put your unique phrase here": True})
            for first in Array("AUTH", "SECURE_AUTH", "LOGGED_IN", "NONCE", "SECRET"):
                for second in Array("KEY", "SALT"):
                    if (not php_defined(str(first) + str("_") + str(second))):
                        continue
                    # end if
                    value = constant(str(first) + str("_") + str(second))
                    duplicated_keys[value] = (php_isset(lambda : duplicated_keys[value]))
                # end for
            # end for
        # end if
        values = Array({"key": "", "salt": ""})
        if php_defined("SECRET_KEY") and SECRET_KEY and php_empty(lambda : duplicated_keys[SECRET_KEY]):
            values["key"] = SECRET_KEY
        # end if
        if "auth" == scheme and php_defined("SECRET_SALT") and SECRET_SALT and php_empty(lambda : duplicated_keys[SECRET_SALT]):
            values["salt"] = SECRET_SALT
        # end if
        if php_in_array(scheme, Array("auth", "secure_auth", "logged_in", "nonce")):
            for type in Array("key", "salt"):
                const = php_strtoupper(str(scheme) + str("_") + str(type))
                if php_defined(const) and constant(const) and php_empty(lambda : duplicated_keys[constant(const)]):
                    values[type] = constant(const)
                elif (not values[type]):
                    values[type] = get_site_option(str(scheme) + str("_") + str(type))
                    if (not values[type]):
                        values[type] = wp_generate_password(64, True, True)
                        update_site_option(str(scheme) + str("_") + str(type), values[type])
                    # end if
                # end if
            # end for
        else:
            if (not values["key"]):
                values["key"] = get_site_option("secret_key")
                if (not values["key"]):
                    values["key"] = wp_generate_password(64, True, True)
                    update_site_option("secret_key", values["key"])
                # end if
            # end if
            values["salt"] = hash_hmac("md5", scheme, values["key"])
        # end if
        cached_salts[scheme] = values["key"] + values["salt"]
        #// This filter is documented in wp-includes/pluggable.php
        return apply_filters("salt", cached_salts[scheme], scheme)
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
    def wp_hash(data=None, scheme="auth", *args_):
        
        salt = wp_salt(scheme)
        return hash_hmac("md5", data, salt)
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
    def wp_hash_password(password=None, *args_):
        
        global wp_hasher
        php_check_if_defined("wp_hasher")
        if php_empty(lambda : wp_hasher):
            php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
            #// By default, use the portable hash from phpass.
            wp_hasher = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
        # end if
        return wp_hasher.hashpassword(php_trim(password))
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
    def wp_check_password(password=None, hash=None, user_id="", *args_):
        
        global wp_hasher
        php_check_if_defined("wp_hasher")
        #// If the hash is still md5...
        if php_strlen(hash) <= 32:
            check = hash_equals(hash, php_md5(password))
            if check and user_id:
                #// Rehash using new hash.
                wp_set_password(password, user_id)
                hash = wp_hash_password(password)
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
            return apply_filters("check_password", check, password, hash, user_id)
        # end if
        #// If the stored hash is longer than an MD5,
        #// presume the new style phpass portable hash.
        if php_empty(lambda : wp_hasher):
            php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
            #// By default, use the portable hash from phpass.
            wp_hasher = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
        # end if
        check = wp_hasher.checkpassword(password, hash)
        #// This filter is documented in wp-includes/pluggable.php
        return apply_filters("check_password", check, password, hash, user_id)
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
    def wp_generate_password(length=12, special_chars=True, extra_special_chars=False, *args_):
        
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if special_chars:
            chars += "!@#$%^&*()"
        # end if
        if extra_special_chars:
            chars += "-_ []{}<>~`+=,.;:/?|"
        # end if
        password = ""
        i = 0
        while i < length:
            
            password += php_substr(chars, wp_rand(0, php_strlen(chars) - 1), 1)
            i += 1
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
        return apply_filters("random_password", password, length, special_chars, extra_special_chars)
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
    def wp_rand(min=0, max=0, *args_):
        
        global rnd_value
        php_check_if_defined("rnd_value")
        #// Some misconfigured 32-bit environments (Entropy PHP, for example)
        #// truncate integers larger than PHP_INT_MAX to PHP_INT_MAX rather than overflowing them to floats.
        max_random_number = float("4294967295") if 3000000000 == 2147483647 else 4294967295
        #// 4294967295 = 0xffffffff
        #// We only handle ints, floats are truncated to their integer value.
        min = int(min)
        max = int(max)
        use_random_int_functionality = True
        if use_random_int_functionality:
            try: 
                _max = max if 0 != max else max_random_number
                #// wp_rand() can accept arguments in either order, PHP cannot.
                _max = php_max(min, _max)
                _min = php_min(min, _max)
                val = random_int(_min, _max)
                if False != val:
                    return absint(val)
                else:
                    use_random_int_functionality = False
                # end if
            except Error as e:
                use_random_int_functionality = False
            except Exception as e:
                use_random_int_functionality = False
            # end try
        # end if
        #// Reset $rnd_value after 14 uses.
        #// 32 (md5) + 40 (sha1) + 40 (sha1) / 8 = 14 random numbers from $rnd_value.
        if php_strlen(rnd_value) < 8:
            if php_defined("WP_SETUP_CONFIG"):
                seed = ""
            else:
                seed = get_transient("random_seed")
            # end if
            rnd_value = php_md5(uniqid(php_microtime() + mt_rand(), True) + seed)
            rnd_value += sha1(rnd_value)
            rnd_value += sha1(rnd_value + seed)
            seed = php_md5(seed + rnd_value)
            if (not php_defined("WP_SETUP_CONFIG")) and (not php_defined("WP_INSTALLING")):
                set_transient("random_seed", seed)
            # end if
        # end if
        #// Take the first 8 digits for our value.
        value = php_substr(rnd_value, 0, 8)
        #// Strip the first eight, leaving the remainder for the next call to wp_rand().
        rnd_value = php_substr(rnd_value, 8)
        value = abs(hexdec(value))
        #// Reduce the value to be within the min - max range.
        if 0 != max:
            value = min + max - min + 1 * value / max_random_number + 1
        # end if
        return abs(php_intval(value))
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
    def wp_set_password(password=None, user_id=None, *args_):
        
        global wpdb
        php_check_if_defined("wpdb")
        hash = wp_hash_password(password)
        wpdb.update(wpdb.users, Array({"user_pass": hash, "user_activation_key": ""}), Array({"ID": user_id}))
        clean_user_cache(user_id)
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
    def get_avatar(id_or_email=None, size=96, default="", alt="", args=None, *args_):
        
        defaults = Array({"size": 96, "height": None, "width": None, "default": get_option("avatar_default", "mystery"), "force_default": False, "rating": get_option("avatar_rating"), "scheme": None, "alt": "", "class": None, "force_display": False, "extra_attr": ""})
        if php_empty(lambda : args):
            args = Array()
        # end if
        args["size"] = int(size)
        args["default"] = default
        args["alt"] = alt
        args = wp_parse_args(args, defaults)
        if php_empty(lambda : args["height"]):
            args["height"] = args["size"]
        # end if
        if php_empty(lambda : args["width"]):
            args["width"] = args["size"]
        # end if
        if php_is_object(id_or_email) and (php_isset(lambda : id_or_email.comment_ID)):
            id_or_email = get_comment(id_or_email)
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
        avatar = apply_filters("pre_get_avatar", None, id_or_email, args)
        if (not php_is_null(avatar)):
            #// This filter is documented in wp-includes/pluggable.php
            return apply_filters("get_avatar", avatar, id_or_email, args["size"], args["default"], args["alt"], args)
        # end if
        if (not args["force_display"]) and (not get_option("show_avatars")):
            return False
        # end if
        url2x = get_avatar_url(id_or_email, php_array_merge(args, Array({"size": args["size"] * 2})))
        args = get_avatar_data(id_or_email, args)
        url = args["url"]
        if (not url) or is_wp_error(url):
            return False
        # end if
        class_ = Array("avatar", "avatar-" + int(args["size"]), "photo")
        if (not args["found_avatar"]) or args["force_default"]:
            class_[-1] = "avatar-default"
        # end if
        if args["class"]:
            if php_is_array(args["class"]):
                class_ = php_array_merge(class_, args["class"])
            else:
                class_[-1] = args["class"]
            # end if
        # end if
        avatar = php_sprintf("<img alt='%s' src='%s' srcset='%s' class='%s' height='%d' width='%d' %s/>", esc_attr(args["alt"]), esc_url(url), esc_url(url2x) + " 2x", esc_attr(join(" ", class_)), int(args["height"]), int(args["width"]), args["extra_attr"])
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
        return apply_filters("get_avatar", avatar, id_or_email, args["size"], args["default"], args["alt"], args)
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
    def wp_text_diff(left_string=None, right_string=None, args=None, *args_):
        
        defaults = Array({"title": "", "title_left": "", "title_right": "", "show_split_view": True})
        args = wp_parse_args(args, defaults)
        if (not php_class_exists("WP_Text_Diff_Renderer_Table", False)):
            php_include_file(ABSPATH + WPINC + "/wp-diff.php", once=False)
        # end if
        left_string = normalize_whitespace(left_string)
        right_string = normalize_whitespace(right_string)
        left_lines = php_explode("\n", left_string)
        right_lines = php_explode("\n", right_string)
        text_diff = php_new_class("Text_Diff", lambda : Text_Diff(left_lines, right_lines))
        renderer = php_new_class("WP_Text_Diff_Renderer_Table", lambda : WP_Text_Diff_Renderer_Table(args))
        diff = renderer.render(text_diff)
        if (not diff):
            return ""
        # end if
        r = "<table class='diff'>\n"
        if (not php_empty(lambda : args["show_split_view"])):
            r += "<col class='content diffsplit left' /><col class='content diffsplit middle' /><col class='content diffsplit right' />"
        else:
            r += "<col class='content' />"
        # end if
        if args["title"] or args["title_left"] or args["title_right"]:
            r += "<thead>"
        # end if
        if args["title"]:
            r += str("<tr class='diff-title'><th colspan='4'>") + str(args["title"]) + str("</th></tr>\n")
        # end if
        if args["title_left"] or args["title_right"]:
            r += "<tr class='diff-sub-title'>\n"
            r += str("  <td></td><th>") + str(args["title_left"]) + str("</th>\n")
            r += str("  <td></td><th>") + str(args["title_right"]) + str("</th>\n")
            r += "</tr>\n"
        # end if
        if args["title"] or args["title_left"] or args["title_right"]:
            r += "</thead>\n"
        # end if
        r += str("<tbody>\n") + str(diff) + str("\n</tbody>\n")
        r += "</table>"
        return r
    # end def wp_text_diff
# end if
