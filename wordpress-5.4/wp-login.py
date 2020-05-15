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
#// WordPress User Page
#// 
#// Handles authentication, registering, resetting passwords, forgot password,
#// and other user handling.
#// 
#// @package WordPress
#// 
#// Make sure that the WordPress bootstrap has run before continuing.
php_include_file(__DIR__ + "/wp-load.php", once=False)
#// Redirect to HTTPS login if forced to use SSL.
if force_ssl_admin() and (not is_ssl()):
    if 0 == php_strpos(PHP_SERVER["REQUEST_URI"], "http"):
        wp_safe_redirect(set_url_scheme(PHP_SERVER["REQUEST_URI"], "https"))
        php_exit(0)
    else:
        wp_safe_redirect("https://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
        php_exit(0)
    # end if
# end if
#// 
#// Output the login page header.
#// 
#// @since 2.1.0
#// 
#// @global string      $error         Login error message set by deprecated pluggable wp_login() function
#// or plugins replacing it.
#// @global bool|string $interim_login Whether interim login modal is being displayed. String 'success'
#// upon successful login.
#// @global string      $action        The action that brought the visitor to the login page.
#// 
#// @param string   $title    Optional. WordPress login Page title to display in the `<title>` element.
#// Default 'Log In'.
#// @param string   $message  Optional. Message to display in header. Default empty.
#// @param WP_Error $wp_error Optional. The error to pass. Default is a WP_Error instance.
#//
def login_header(title="Log In", message="", wp_error=None, *args_):
    
    global error,interim_login,action
    php_check_if_defined("error","interim_login","action")
    #// Don't index any of these forms.
    add_action("login_head", "wp_sensitive_page_meta")
    add_action("login_head", "wp_login_viewport_meta")
    if (not is_wp_error(wp_error)):
        wp_error = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    #// Shake it!
    shake_error_codes = Array("empty_password", "empty_email", "invalid_email", "invalidcombo", "empty_username", "invalid_username", "incorrect_password", "retrieve_password_email_failure")
    #// 
    #// Filters the error codes array for shaking the login form.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $shake_error_codes Error codes that shake the login form.
    #//
    shake_error_codes = apply_filters("shake_error_codes", shake_error_codes)
    if shake_error_codes and wp_error.has_errors() and php_in_array(wp_error.get_error_code(), shake_error_codes, True):
        add_action("login_footer", "wp_shake_js", 12)
    # end if
    login_title = get_bloginfo("name", "display")
    #// translators: Login screen title. 1: Login screen name, 2: Network or site name.
    login_title = php_sprintf(__("%1$s &lsaquo; %2$s &#8212; WordPress"), title, login_title)
    if wp_is_recovery_mode():
        #// translators: %s: Login screen title.
        login_title = php_sprintf(__("Recovery Mode &#8212; %s"), login_title)
    # end if
    #// 
    #// Filters the title tag content for login page.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $login_title The page title, with extra context added.
    #// @param string $title       The original page title.
    #//
    login_title = apply_filters("login_title", login_title, title)
    php_print("<!DOCTYPE html>\n    <!--[if IE 8]>\n        <html xmlns=\"http://www.w3.org/1999/xhtml\" class=\"ie8\" ")
    language_attributes()
    php_print(""">
    <![endif]-->
    <!--[if !(IE 8) ]><!-->
    <html xmlns=\"http://www.w3.org/1999/xhtml\" """)
    language_attributes()
    php_print(""">
    <!--<![endif]-->
    <head>
    <meta http-equiv=\"Content-Type\" content=\"""")
    bloginfo("html_type")
    php_print("; charset=")
    bloginfo("charset")
    php_print("\" />\n  <title>")
    php_print(login_title)
    php_print("</title>\n   ")
    wp_enqueue_style("login")
    #// 
    #// Remove all stored post data on logging out.
    #// This could be added by add_action('login_head'...) like wp_shake_js(),
    #// but maybe better if it's not removable by plugins.
    #//
    if "loggedout" == wp_error.get_error_code():
        php_print("     <script>if(\"sessionStorage\" in window){try{for(var key in sessionStorage){if(key.indexOf(\"wp-autosave-\")!=-1){sessionStorage.removeItem(key)}}}catch(e){}};</script>\n      ")
    # end if
    #// 
    #// Enqueue scripts and styles for the login page.
    #// 
    #// @since 3.1.0
    #//
    do_action("login_enqueue_scripts")
    #// 
    #// Fires in the login page header after scripts are enqueued.
    #// 
    #// @since 2.1.0
    #//
    do_action("login_head")
    login_header_url = __("https://wordpress.org/")
    #// 
    #// Filters link URL of the header logo above login form.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $login_header_url Login header logo URL.
    #//
    login_header_url = apply_filters("login_headerurl", login_header_url)
    login_header_title = ""
    #// 
    #// Filters the title attribute of the header logo above login form.
    #// 
    #// @since 2.1.0
    #// @deprecated 5.2.0 Use {@see 'login_headertext'} instead.
    #// 
    #// @param string $login_header_title Login header logo title attribute.
    #//
    login_header_title = apply_filters_deprecated("login_headertitle", Array(login_header_title), "5.2.0", "login_headertext", __("Usage of the title attribute on the login logo is not recommended for accessibility reasons. Use the link text instead."))
    login_header_text = __("Powered by WordPress") if php_empty(lambda : login_header_title) else login_header_title
    #// 
    #// Filters the link text of the header logo above the login form.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string $login_header_text The login header logo link text.
    #//
    login_header_text = apply_filters("login_headertext", login_header_text)
    classes = Array("login-action-" + action, "wp-core-ui")
    if is_rtl():
        classes[-1] = "rtl"
    # end if
    if interim_login:
        classes[-1] = "interim-login"
        php_print("     <style type=\"text/css\">html{background-color: transparent;}</style>\n     ")
        if "success" == interim_login:
            classes[-1] = "interim-login-success"
        # end if
    # end if
    classes[-1] = " locale-" + sanitize_html_class(php_strtolower(php_str_replace("_", "-", get_locale())))
    #// 
    #// Filters the login page body classes.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array  $classes An array of body classes.
    #// @param string $action  The action that brought the visitor to the login page.
    #//
    classes = apply_filters("login_body_class", classes, action)
    php_print(" </head>\n   <body class=\"login no-js ")
    php_print(esc_attr(php_implode(" ", classes)))
    php_print("""\">
    <script type=\"text/javascript\">
    document.body.className = document.body.className.replace('no-js','js');
    </script>
    """)
    #// 
    #// Fires in the login page header after the body tag is opened.
    #// 
    #// @since 4.6.0
    #//
    do_action("login_header")
    php_print(" <div id=\"login\">\n        <h1><a href=\"")
    php_print(esc_url(login_header_url))
    php_print("\">")
    php_print(login_header_text)
    php_print("</a></h1>\n  ")
    #// 
    #// Filters the message to display above the login form.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $message Login message text.
    #//
    message = apply_filters("login_message", message)
    if (not php_empty(lambda : message)):
        php_print(message + "\n")
    # end if
    #// In case a plugin uses $error rather than the $wp_errors object.
    if (not php_empty(lambda : error)):
        wp_error.add("error", error)
        error = None
    # end if
    if wp_error.has_errors():
        errors = ""
        messages = ""
        for code in wp_error.get_error_codes():
            severity = wp_error.get_error_data(code)
            for error_message in wp_error.get_error_messages(code):
                if "message" == severity:
                    messages += "   " + error_message + "<br />\n"
                else:
                    errors += " " + error_message + "<br />\n"
                # end if
            # end for
        # end for
        if (not php_empty(lambda : errors)):
            #// 
            #// Filters the error messages displayed above the login form.
            #// 
            #// @since 2.1.0
            #// 
            #// @param string $errors Login error message.
            #//
            php_print("<div id=\"login_error\">" + apply_filters("login_errors", errors) + "</div>\n")
        # end if
        if (not php_empty(lambda : messages)):
            #// 
            #// Filters instructional messages displayed above the login form.
            #// 
            #// @since 2.5.0
            #// 
            #// @param string $messages Login messages.
            #//
            php_print("<p class=\"message\">" + apply_filters("login_messages", messages) + "</p>\n")
        # end if
    # end if
# end def login_header
#// End of login_header().
#// 
#// Outputs the footer for the login page.
#// 
#// @since 3.1.0
#// 
#// @global bool|string $interim_login Whether interim login modal is being displayed. String 'success'
#// upon successful login.
#// 
#// @param string $input_id Which input to auto-focus.
#//
def login_footer(input_id="", *args_):
    
    global interim_login
    php_check_if_defined("interim_login")
    #// Don't allow interim logins to navigate away from the page.
    if (not interim_login):
        php_print("     <p id=\"backtoblog\"><a href=\"")
        php_print(esc_url(home_url("/")))
        php_print("\">\n        ")
        #// translators: %s: Site title.
        printf(_x("&larr; Back to %s", "site"), get_bloginfo("title", "display"))
        php_print("     </a></p>\n      ")
        the_privacy_policy_link("<div class=\"privacy-policy-page-link\">", "</div>")
    # end if
    php_print(" </div>")
    pass
    php_print("\n   ")
    if (not php_empty(lambda : input_id)):
        php_print("     <script type=\"text/javascript\">\n     try{document.getElementById('")
        php_print(input_id)
        php_print("""').focus();}catch(e){}
    if(typeof wpOnload=='function')wpOnload();
        </script>
        """)
    # end if
    #// 
    #// Fires in the login page footer.
    #// 
    #// @since 3.1.0
    #//
    do_action("login_footer")
    php_print("""   <div class=\"clear\"></div>
    </body>
    </html>
    """)
# end def login_footer
#// 
#// Outputs the Javascript to handle the form shaking.
#// 
#// @since 3.0.0
#//
def wp_shake_js(*args_):
    
    php_print("""   <script type=\"text/javascript\">
    document.querySelector('form').classList.add('shake');
    </script>
    """)
# end def wp_shake_js
#// 
#// Outputs the viewport meta tag.
#// 
#// @since 3.7.0
#//
def wp_login_viewport_meta(*args_):
    
    php_print(" <meta name=\"viewport\" content=\"width=device-width\" />\n ")
# end def wp_login_viewport_meta
#// 
#// Handles sending password retrieval email to user.
#// 
#// @since 2.5.0
#// 
#// @return bool|WP_Error True: when finish. WP_Error on error
#//
def retrieve_password(*args_):
    
    errors = php_new_class("WP_Error", lambda : WP_Error())
    user_data = False
    if php_empty(lambda : PHP_POST["user_login"]) or (not php_is_string(PHP_POST["user_login"])):
        errors.add("empty_username", __("<strong>Error</strong>: Enter a username or email address."))
    elif php_strpos(PHP_POST["user_login"], "@"):
        user_data = get_user_by("email", php_trim(wp_unslash(PHP_POST["user_login"])))
        if php_empty(lambda : user_data):
            errors.add("invalid_email", __("<strong>Error</strong>: There is no account with that username or email address."))
        # end if
    else:
        login = php_trim(wp_unslash(PHP_POST["user_login"]))
        user_data = get_user_by("login", login)
    # end if
    #// 
    #// Fires before errors are returned from a password reset request.
    #// 
    #// @since 2.1.0
    #// @since 4.4.0 Added the `$errors` parameter.
    #// @since 5.4.0 Added the `$user_data` parameter.
    #// 
    #// @param WP_Error $errors A WP_Error object containing any errors generated
    #// by using invalid credentials.
    #// @param WP_User|false    WP_User object if found, false if the user does not exist.
    #//
    do_action("lostpassword_post", errors, user_data)
    if errors.has_errors():
        return errors
    # end if
    if (not user_data):
        errors.add("invalidcombo", __("<strong>Error</strong>: There is no account with that username or email address."))
        return errors
    # end if
    #// Redefining user_login ensures we return the right case in the email.
    user_login = user_data.user_login
    user_email = user_data.user_email
    key = get_password_reset_key(user_data)
    if is_wp_error(key):
        return key
    # end if
    if is_multisite():
        site_name = get_network().site_name
    else:
        #// 
        #// The blogname option is escaped with esc_html on the way into the database
        #// in sanitize_option we want to reverse this for the plain text arena of emails.
        #//
        site_name = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
    # end if
    message = __("Someone has requested a password reset for the following account:") + "\r\n\r\n"
    #// translators: %s: Site name.
    message += php_sprintf(__("Site Name: %s"), site_name) + "\r\n\r\n"
    #// translators: %s: User login.
    message += php_sprintf(__("Username: %s"), user_login) + "\r\n\r\n"
    message += __("If this was a mistake, just ignore this email and nothing will happen.") + "\r\n\r\n"
    message += __("To reset your password, visit the following address:") + "\r\n\r\n"
    message += network_site_url(str("wp-login.php?action=rp&key=") + str(key) + str("&login=") + rawurlencode(user_login), "login") + "\r\n"
    #// translators: Password reset notification email subject. %s: Site title.
    title = php_sprintf(__("[%s] Password Reset"), site_name)
    #// 
    #// Filters the subject of the password reset email.
    #// 
    #// @since 2.8.0
    #// @since 4.4.0 Added the `$user_login` and `$user_data` parameters.
    #// 
    #// @param string  $title      Default email title.
    #// @param string  $user_login The username for the user.
    #// @param WP_User $user_data  WP_User object.
    #//
    title = apply_filters("retrieve_password_title", title, user_login, user_data)
    #// 
    #// Filters the message body of the password reset mail.
    #// 
    #// If the filtered message is empty, the password reset email will not be sent.
    #// 
    #// @since 2.8.0
    #// @since 4.1.0 Added `$user_login` and `$user_data` parameters.
    #// 
    #// @param string  $message    Default mail message.
    #// @param string  $key        The activation key.
    #// @param string  $user_login The username for the user.
    #// @param WP_User $user_data  WP_User object.
    #//
    message = apply_filters("retrieve_password_message", message, key, user_login, user_data)
    if message and (not wp_mail(user_email, wp_specialchars_decode(title), message)):
        errors.add("retrieve_password_email_failure", php_sprintf(__("<strong>Error</strong>: The email could not be sent. Your site may not be correctly configured to send emails. <a href=\"%s\">Get support for resetting your password</a>."), esc_url(__("https://wordpress.org/support/article/resetting-your-password/"))))
        return errors
    # end if
    return True
# end def retrieve_password
#// 
#// Main.
#//
action = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else "login"
errors = php_new_class("WP_Error", lambda : WP_Error())
if (php_isset(lambda : PHP_REQUEST["key"])):
    action = "resetpass"
# end if
default_actions = Array("confirm_admin_email", "postpass", "logout", "lostpassword", "retrievepassword", "resetpass", "rp", "register", "login", "confirmaction", WP_Recovery_Mode_Link_Service.LOGIN_ACTION_ENTERED)
#// Validate action so as to default to the login screen.
if (not php_in_array(action, default_actions, True)) and False == has_filter("login_form_" + action):
    action = "login"
# end if
nocache_headers()
php_header("Content-Type: " + get_bloginfo("html_type") + "; charset=" + get_bloginfo("charset"))
if php_defined("RELOCATE") and RELOCATE:
    #// Move flag is set.
    if (php_isset(lambda : PHP_SERVER["PATH_INFO"])) and PHP_SERVER["PATH_INFO"] != PHP_SERVER["PHP_SELF"]:
        PHP_SERVER["PHP_SELF"] = php_str_replace(PHP_SERVER["PATH_INFO"], "", PHP_SERVER["PHP_SELF"])
    # end if
    url = php_dirname(set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["PHP_SELF"]))
    if get_option("siteurl") != url:
        update_option("siteurl", url)
    # end if
# end if
#// Set a cookie now to see if they are supported by the browser.
secure = "https" == php_parse_url(wp_login_url(), PHP_URL_SCHEME)
setcookie(TEST_COOKIE, "WP Cookie check", 0, COOKIEPATH, COOKIE_DOMAIN, secure)
if SITECOOKIEPATH != COOKIEPATH:
    setcookie(TEST_COOKIE, "WP Cookie check", 0, SITECOOKIEPATH, COOKIE_DOMAIN, secure)
# end if
#// 
#// Fires when the login form is initialized.
#// 
#// @since 3.2.0
#//
do_action("login_init")
#// 
#// Fires before a specified login form action.
#// 
#// The dynamic portion of the hook name, `$action`, refers to the action
#// that brought the visitor to the login form. Actions include 'postpass',
#// 'logout', 'lostpassword', etc.
#// 
#// @since 2.8.0
#//
do_action(str("login_form_") + str(action))
http_post = "POST" == PHP_SERVER["REQUEST_METHOD"]
interim_login = (php_isset(lambda : PHP_REQUEST["interim-login"]))
#// 
#// Filters the separator used between login form navigation links.
#// 
#// @since 4.9.0
#// 
#// @param string $login_link_separator The separator used between login form navigation links.
#//
login_link_separator = apply_filters("login_link_separator", " | ")
for case in Switch(action):
    if case("confirm_admin_email"):
        #// 
        #// Note that `is_user_logged_in()` will return false immediately after logging in
        #// as the current user is not set, see wp-includes/pluggable.php.
        #// However this action runs on a redirect after logging in.
        #//
        if (not is_user_logged_in()):
            wp_safe_redirect(wp_login_url())
            php_exit(0)
        # end if
        if (not php_empty(lambda : PHP_REQUEST["redirect_to"])):
            redirect_to = PHP_REQUEST["redirect_to"]
        else:
            redirect_to = admin_url()
        # end if
        if current_user_can("manage_options"):
            admin_email = get_option("admin_email")
        else:
            wp_safe_redirect(redirect_to)
            php_exit(0)
        # end if
        #// 
        #// Filters the interval for dismissing the admin email confirmation screen.
        #// 
        #// If `0` (zero) is returned, the "Remind me later" link will not be displayed.
        #// 
        #// @since 5.3.1
        #// 
        #// @param int $interval Interval time (in seconds). Default is 3 days.
        #//
        remind_interval = int(apply_filters("admin_email_remind_interval", 3 * DAY_IN_SECONDS))
        if (not php_empty(lambda : PHP_REQUEST["remind_me_later"])):
            if (not wp_verify_nonce(PHP_REQUEST["remind_me_later"], "remind_me_later_nonce")):
                wp_safe_redirect(wp_login_url())
                php_exit(0)
            # end if
            if remind_interval > 0:
                update_option("admin_email_lifespan", time() + remind_interval)
            # end if
            wp_safe_redirect(redirect_to)
            php_exit(0)
        # end if
        if (not php_empty(lambda : PHP_POST["correct-admin-email"])):
            if (not check_admin_referer("confirm_admin_email", "confirm_admin_email_nonce")):
                wp_safe_redirect(wp_login_url())
                php_exit(0)
            # end if
            #// 
            #// Filters the interval for redirecting the user to the admin email confirmation screen.
            #// 
            #// If `0` (zero) is returned, the user will not be redirected.
            #// 
            #// @since 5.3.0
            #// 
            #// @param int $interval Interval time (in seconds). Default is 6 months.
            #//
            admin_email_check_interval = int(apply_filters("admin_email_check_interval", 6 * MONTH_IN_SECONDS))
            if admin_email_check_interval > 0:
                update_option("admin_email_lifespan", time() + admin_email_check_interval)
            # end if
            wp_safe_redirect(redirect_to)
            php_exit(0)
        # end if
        login_header(__("Confirm your administration email"), "", errors)
        #// 
        #// Fires before the admin email confirm form.
        #// 
        #// @since 5.3.0
        #// 
        #// @param WP_Error $errors A `WP_Error` object containing any errors generated by using invalid
        #// credentials. Note that the error object may not contain any errors.
        #//
        do_action("admin_email_confirm", errors)
        php_print("\n       <form class=\"admin-email-confirm-form\" name=\"admin-email-confirm-form\" action=\"")
        php_print(esc_url(site_url("wp-login.php?action=confirm_admin_email", "login_post")))
        php_print("\" method=\"post\">\n            ")
        #// 
        #// Fires inside the admin-email-confirm-form form tags, before the hidden fields.
        #// 
        #// @since 5.3.0
        #//
        do_action("admin_email_confirm_form")
        wp_nonce_field("confirm_admin_email", "confirm_admin_email_nonce")
        php_print("         <input type=\"hidden\" name=\"redirect_to\" value=\"")
        php_print(esc_attr(redirect_to))
        php_print("""\" />
        <h1 class=\"admin-email__heading\">
        """)
        _e("Administration email verification")
        php_print("         </h1>\n         <p class=\"admin-email__details\">\n                ")
        _e("Please verify that the <strong>administration email</strong> for this website is still correct.")
        php_print("             ")
        #// translators: URL to the WordPress help section about admin email.
        admin_email_help_url = __("https://wordpress.org/support/article/settings-general-screen/#email-address")
        #// translators: accessibility text
        accessibility_text = php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)"))
        printf("<a href=\"%s\" rel=\"noopener noreferrer\" target=\"_blank\">%s%s</a>", esc_url(admin_email_help_url), __("Why is this important?"), accessibility_text)
        php_print("         </p>\n          <p class=\"admin-email__details\">\n                ")
        printf(__("Current administration email: %s"), "<strong>" + esc_html(admin_email) + "</strong>")
        php_print("         </p>\n          <p class=\"admin-email__details\">\n                ")
        _e("This email may be different from your personal email address.")
        php_print("""           </p>
        <div class=\"admin-email__actions\">
        <div class=\"admin-email__actions-primary\">
        """)
        change_link = admin_url("options-general.php")
        change_link = add_query_arg("highlight", "confirm_admin_email", change_link)
        php_print("                 <a class=\"button button-large\" href=\"")
        php_print(esc_url(change_link))
        php_print("\">")
        _e("Update")
        php_print("</a>\n                   <input type=\"submit\" name=\"correct-admin-email\" id=\"correct-admin-email\" class=\"button button-primary button-large\" value=\"")
        esc_attr_e("The email is correct")
        php_print("\" />\n              </div>\n                ")
        if remind_interval > 0:
            php_print("                 <div class=\"admin-email__actions-secondary\">\n                        ")
            remind_me_link = wp_login_url(redirect_to)
            remind_me_link = add_query_arg(Array({"action": "confirm_admin_email", "remind_me_later": wp_create_nonce("remind_me_later_nonce")}), remind_me_link)
            php_print("                     <a href=\"")
            php_print(esc_url(remind_me_link))
            php_print("\">")
            _e("Remind me later")
            php_print("</a>\n                   </div>\n                ")
        # end if
        php_print("""           </div>
        </form>
        """)
        login_footer()
        break
    # end if
    if case("postpass"):
        if (not php_array_key_exists("post_password", PHP_POST)):
            wp_safe_redirect(wp_get_referer())
            php_exit(0)
        # end if
        php_include_file(ABSPATH + WPINC + "/class-phpass.php", once=True)
        hasher = php_new_class("PasswordHash", lambda : PasswordHash(8, True))
        #// 
        #// Filters the life span of the post password cookie.
        #// 
        #// By default, the cookie expires 10 days from creation. To turn this
        #// into a session cookie, return 0.
        #// 
        #// @since 3.7.0
        #// 
        #// @param int $expires The expiry time, as passed to setcookie().
        #//
        expire = apply_filters("post_password_expires", time() + 10 * DAY_IN_SECONDS)
        referer = wp_get_referer()
        if referer:
            secure = "https" == php_parse_url(referer, PHP_URL_SCHEME)
        else:
            secure = False
        # end if
        setcookie("wp-postpass_" + COOKIEHASH, hasher.hashpassword(wp_unslash(PHP_POST["post_password"])), expire, COOKIEPATH, COOKIE_DOMAIN, secure)
        wp_safe_redirect(wp_get_referer())
        php_exit(0)
    # end if
    if case("logout"):
        check_admin_referer("log-out")
        user = wp_get_current_user()
        wp_logout()
        if (not php_empty(lambda : PHP_REQUEST["redirect_to"])):
            redirect_to = PHP_REQUEST["redirect_to"]
            requested_redirect_to = redirect_to
        else:
            redirect_to = add_query_arg(Array({"loggedout": "true", "wp_lang": get_user_locale(user)}), wp_login_url())
            requested_redirect_to = ""
        # end if
        #// 
        #// Filters the log out redirect URL.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string  $redirect_to           The redirect destination URL.
        #// @param string  $requested_redirect_to The requested redirect destination URL passed as a parameter.
        #// @param WP_User $user                  The WP_User object for the user that's logging out.
        #//
        redirect_to = apply_filters("logout_redirect", redirect_to, requested_redirect_to, user)
        wp_safe_redirect(redirect_to)
        php_exit(0)
    # end if
    if case("lostpassword"):
        pass
    # end if
    if case("retrievepassword"):
        if http_post:
            errors = retrieve_password()
            if (not is_wp_error(errors)):
                redirect_to = PHP_REQUEST["redirect_to"] if (not php_empty(lambda : PHP_REQUEST["redirect_to"])) else "wp-login.php?checkemail=confirm"
                wp_safe_redirect(redirect_to)
                php_exit(0)
            # end if
        # end if
        if (php_isset(lambda : PHP_REQUEST["error"])):
            if "invalidkey" == PHP_REQUEST["error"]:
                errors.add("invalidkey", __("Your password reset link appears to be invalid. Please request a new link below."))
            elif "expiredkey" == PHP_REQUEST["error"]:
                errors.add("expiredkey", __("Your password reset link has expired. Please request a new link below."))
            # end if
        # end if
        lostpassword_redirect = PHP_REQUEST["redirect_to"] if (not php_empty(lambda : PHP_REQUEST["redirect_to"])) else ""
        #// 
        #// Filters the URL redirected to after submitting the lostpassword/retrievepassword form.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $lostpassword_redirect The redirect destination URL.
        #//
        redirect_to = apply_filters("lostpassword_redirect", lostpassword_redirect)
        #// 
        #// Fires before the lost password form.
        #// 
        #// @since 1.5.1
        #// @since 5.1.0 Added the `$errors` parameter.
        #// 
        #// @param WP_Error $errors A `WP_Error` object containing any errors generated by using invalid
        #// credentials. Note that the error object may not contain any errors.
        #//
        do_action("lost_password", errors)
        login_header(__("Lost Password"), "<p class=\"message\">" + __("Please enter your username or email address. You will receive an email message with instructions on how to reset your password.") + "</p>", errors)
        user_login = ""
        if (php_isset(lambda : PHP_POST["user_login"])) and php_is_string(PHP_POST["user_login"]):
            user_login = wp_unslash(PHP_POST["user_login"])
        # end if
        php_print("\n       <form name=\"lostpasswordform\" id=\"lostpasswordform\" action=\"")
        php_print(esc_url(network_site_url("wp-login.php?action=lostpassword", "login_post")))
        php_print("\" method=\"post\">\n            <p>\n               <label for=\"user_login\">")
        _e("Username or Email Address")
        php_print("</label>\n               <input type=\"text\" name=\"user_login\" id=\"user_login\" class=\"input\" value=\"")
        php_print(esc_attr(user_login))
        php_print("\" size=\"20\" autocapitalize=\"off\" />\n           </p>\n          ")
        #// 
        #// Fires inside the lostpassword form tags, before the hidden fields.
        #// 
        #// @since 2.1.0
        #//
        do_action("lostpassword_form")
        php_print("         <input type=\"hidden\" name=\"redirect_to\" value=\"")
        php_print(esc_attr(redirect_to))
        php_print("\" />\n          <p class=\"submit\">\n              <input type=\"submit\" name=\"wp-submit\" id=\"wp-submit\" class=\"button button-primary button-large\" value=\"")
        esc_attr_e("Get New Password")
        php_print("""\" />
        </p>
        </form>
        <p id=\"nav\">
        <a href=\"""")
        php_print(esc_url(wp_login_url()))
        php_print("\">")
        _e("Log in")
        php_print("</a>\n           ")
        if get_option("users_can_register"):
            registration_url = php_sprintf("<a href=\"%s\">%s</a>", esc_url(wp_registration_url()), __("Register"))
            php_print(esc_html(login_link_separator))
            #// This filter is documented in wp-includes/general-template.php
            php_print(apply_filters("register", registration_url))
        # end if
        php_print("     </p>\n      ")
        login_footer("user_login")
        break
    # end if
    if case("resetpass"):
        pass
    # end if
    if case("rp"):
        rp_path = php_explode("?", wp_unslash(PHP_SERVER["REQUEST_URI"]))
        rp_cookie = "wp-resetpass-" + COOKIEHASH
        if (php_isset(lambda : PHP_REQUEST["key"])):
            value = php_sprintf("%s:%s", wp_unslash(PHP_REQUEST["login"]), wp_unslash(PHP_REQUEST["key"]))
            setcookie(rp_cookie, value, 0, rp_path, COOKIE_DOMAIN, is_ssl(), True)
            wp_safe_redirect(remove_query_arg(Array("key", "login")))
            php_exit(0)
        # end if
        if (php_isset(lambda : PHP_COOKIE[rp_cookie])) and 0 < php_strpos(PHP_COOKIE[rp_cookie], ":"):
            rp_login, rp_key = php_explode(":", wp_unslash(PHP_COOKIE[rp_cookie]), 2)
            user = check_password_reset_key(rp_key, rp_login)
            if (php_isset(lambda : PHP_POST["pass1"])) and (not hash_equals(rp_key, PHP_POST["rp_key"])):
                user = False
            # end if
        else:
            user = False
        # end if
        if (not user) or is_wp_error(user):
            setcookie(rp_cookie, " ", time() - YEAR_IN_SECONDS, rp_path, COOKIE_DOMAIN, is_ssl(), True)
            if user and user.get_error_code() == "expired_key":
                wp_redirect(site_url("wp-login.php?action=lostpassword&error=expiredkey"))
            else:
                wp_redirect(site_url("wp-login.php?action=lostpassword&error=invalidkey"))
            # end if
            php_exit(0)
        # end if
        errors = php_new_class("WP_Error", lambda : WP_Error())
        if (php_isset(lambda : PHP_POST["pass1"])) and PHP_POST["pass1"] != PHP_POST["pass2"]:
            errors.add("password_reset_mismatch", __("The passwords do not match."))
        # end if
        #// 
        #// Fires before the password reset procedure is validated.
        #// 
        #// @since 3.5.0
        #// 
        #// @param WP_Error         $errors WP Error object.
        #// @param WP_User|WP_Error $user   WP_User object if the login and reset key match. WP_Error object otherwise.
        #//
        do_action("validate_password_reset", errors, user)
        if (not errors.has_errors()) and (php_isset(lambda : PHP_POST["pass1"])) and (not php_empty(lambda : PHP_POST["pass1"])):
            reset_password(user, PHP_POST["pass1"])
            setcookie(rp_cookie, " ", time() - YEAR_IN_SECONDS, rp_path, COOKIE_DOMAIN, is_ssl(), True)
            login_header(__("Password Reset"), "<p class=\"message reset-pass\">" + __("Your password has been reset.") + " <a href=\"" + esc_url(wp_login_url()) + "\">" + __("Log in") + "</a></p>")
            login_footer()
            php_exit(0)
        # end if
        wp_enqueue_script("utils")
        wp_enqueue_script("user-profile")
        login_header(__("Reset Password"), "<p class=\"message reset-pass\">" + __("Enter your new password below.") + "</p>", errors)
        php_print("     <form name=\"resetpassform\" id=\"resetpassform\" action=\"")
        php_print(esc_url(network_site_url("wp-login.php?action=resetpass", "login_post")))
        php_print("\" method=\"post\" autocomplete=\"off\">\n           <input type=\"hidden\" id=\"user_login\" value=\"")
        php_print(esc_attr(rp_login))
        php_print("""\" autocomplete=\"off\" />
        <div class=\"user-pass1-wrap\">
        <p>
        <label for=\"pass1\">""")
        _e("New password")
        php_print("""</label>
        </p>
        <div class=\"wp-pwd\">
        <input type=\"password\" data-reveal=\"1\" data-pw=\"""")
        php_print(esc_attr(wp_generate_password(16)))
        php_print("\" name=\"pass1\" id=\"pass1\" class=\"input password-input\" size=\"24\" value=\"\" autocomplete=\"off\" aria-describedby=\"pass-strength-result\" />\n\n                   <button type=\"button\" class=\"button button-secondary wp-hide-pw hide-if-no-js\" data-toggle=\"0\" aria-label=\"")
        esc_attr_e("Hide password")
        php_print("""\">
        <span class=\"dashicons dashicons-hidden\" aria-hidden=\"true\"></span>
        </button>
        <div id=\"pass-strength-result\" class=\"hide-if-no-js\" aria-live=\"polite\">""")
        _e("Strength indicator")
        php_print("""</div>
        </div>
        <div class=\"pw-weak\">
        <input type=\"checkbox\" name=\"pw_weak\" id=\"pw-weak\" class=\"pw-checkbox\" />
        <label for=\"pw-weak\">""")
        _e("Confirm use of weak password")
        php_print("""</label>
        </div>
        </div>
        <p class=\"user-pass2-wrap\">
        <label for=\"pass2\">""")
        _e("Confirm new password")
        php_print("""</label>
        <input type=\"password\" name=\"pass2\" id=\"pass2\" class=\"input\" size=\"20\" value=\"\" autocomplete=\"off\" />
        </p>
        <p class=\"description indicator-hint\">""")
        php_print(wp_get_password_hint())
        php_print("""</p>
        <br class=\"clear\" />
        """)
        #// 
        #// Fires following the 'Strength indicator' meter in the user password reset form.
        #// 
        #// @since 3.9.0
        #// 
        #// @param WP_User $user User object of the user whose password is being reset.
        #//
        do_action("resetpass_form", user)
        php_print("         <input type=\"hidden\" name=\"rp_key\" value=\"")
        php_print(esc_attr(rp_key))
        php_print("\" />\n          <p class=\"submit\">\n              <input type=\"submit\" name=\"wp-submit\" id=\"wp-submit\" class=\"button button-primary button-large\" value=\"")
        esc_attr_e("Reset Password")
        php_print("""\" />
        </p>
        </form>
        <p id=\"nav\">
        <a href=\"""")
        php_print(esc_url(wp_login_url()))
        php_print("\">")
        _e("Log in")
        php_print("</a>\n           ")
        if get_option("users_can_register"):
            registration_url = php_sprintf("<a href=\"%s\">%s</a>", esc_url(wp_registration_url()), __("Register"))
            php_print(esc_html(login_link_separator))
            #// This filter is documented in wp-includes/general-template.php
            php_print(apply_filters("register", registration_url))
        # end if
        php_print("     </p>\n      ")
        login_footer("user_pass")
        break
    # end if
    if case("register"):
        if is_multisite():
            #// 
            #// Filters the Multisite sign up URL.
            #// 
            #// @since 3.0.0
            #// 
            #// @param string $sign_up_url The sign up URL.
            #//
            wp_redirect(apply_filters("wp_signup_location", network_site_url("wp-signup.php")))
            php_exit(0)
        # end if
        if (not get_option("users_can_register")):
            wp_redirect(site_url("wp-login.php?registration=disabled"))
            php_exit(0)
        # end if
        user_login = ""
        user_email = ""
        if http_post:
            if (php_isset(lambda : PHP_POST["user_login"])) and php_is_string(PHP_POST["user_login"]):
                user_login = wp_unslash(PHP_POST["user_login"])
            # end if
            if (php_isset(lambda : PHP_POST["user_email"])) and php_is_string(PHP_POST["user_email"]):
                user_email = wp_unslash(PHP_POST["user_email"])
            # end if
            errors = register_new_user(user_login, user_email)
            if (not is_wp_error(errors)):
                redirect_to = PHP_POST["redirect_to"] if (not php_empty(lambda : PHP_POST["redirect_to"])) else "wp-login.php?checkemail=registered"
                wp_safe_redirect(redirect_to)
                php_exit(0)
            # end if
        # end if
        registration_redirect = PHP_REQUEST["redirect_to"] if (not php_empty(lambda : PHP_REQUEST["redirect_to"])) else ""
        #// 
        #// Filters the registration redirect URL.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $registration_redirect The redirect destination URL.
        #//
        redirect_to = apply_filters("registration_redirect", registration_redirect)
        login_header(__("Registration Form"), "<p class=\"message register\">" + __("Register For This Site") + "</p>", errors)
        php_print("     <form name=\"registerform\" id=\"registerform\" action=\"")
        php_print(esc_url(site_url("wp-login.php?action=register", "login_post")))
        php_print("\" method=\"post\" novalidate=\"novalidate\">\n          <p>\n               <label for=\"user_login\">")
        _e("Username")
        php_print("</label>\n               <input type=\"text\" name=\"user_login\" id=\"user_login\" class=\"input\" value=\"")
        php_print(esc_attr(wp_unslash(user_login)))
        php_print("""\" size=\"20\" autocapitalize=\"off\" />
        </p>
        <p>
        <label for=\"user_email\">""")
        _e("Email")
        php_print("</label>\n               <input type=\"email\" name=\"user_email\" id=\"user_email\" class=\"input\" value=\"")
        php_print(esc_attr(wp_unslash(user_email)))
        php_print("\" size=\"25\" />\n          </p>\n          ")
        #// 
        #// Fires following the 'Email' field in the user registration form.
        #// 
        #// @since 2.1.0
        #//
        do_action("register_form")
        php_print("         <p id=\"reg_passmail\">\n               ")
        _e("Registration confirmation will be emailed to you.")
        php_print("         </p>\n          <br class=\"clear\" />\n            <input type=\"hidden\" name=\"redirect_to\" value=\"")
        php_print(esc_attr(redirect_to))
        php_print("\" />\n          <p class=\"submit\">\n              <input type=\"submit\" name=\"wp-submit\" id=\"wp-submit\" class=\"button button-primary button-large\" value=\"")
        esc_attr_e("Register")
        php_print("""\" />
        </p>
        </form>
        <p id=\"nav\">
        <a href=\"""")
        php_print(esc_url(wp_login_url()))
        php_print("\">")
        _e("Log in")
        php_print("</a>\n               ")
        php_print(esc_html(login_link_separator))
        php_print("         <a href=\"")
        php_print(esc_url(wp_lostpassword_url()))
        php_print("\">")
        _e("Lost your password?")
        php_print("</a>\n       </p>\n      ")
        login_footer("user_login")
        break
    # end if
    if case("confirmaction"):
        if (not (php_isset(lambda : PHP_REQUEST["request_id"]))):
            wp_die(__("Missing request ID."))
        # end if
        if (not (php_isset(lambda : PHP_REQUEST["confirm_key"]))):
            wp_die(__("Missing confirm key."))
        # end if
        request_id = int(PHP_REQUEST["request_id"])
        key = sanitize_text_field(wp_unslash(PHP_REQUEST["confirm_key"]))
        result = wp_validate_user_request_key(request_id, key)
        if is_wp_error(result):
            wp_die(result)
        # end if
        #// 
        #// Fires an action hook when the account action has been confirmed by the user.
        #// 
        #// Using this you can assume the user has agreed to perform the action by
        #// clicking on the link in the confirmation email.
        #// 
        #// After firing this action hook the page will redirect to wp-login a callback
        #// redirects or exits first.
        #// 
        #// @since 4.9.6
        #// 
        #// @param int $request_id Request ID.
        #//
        do_action("user_request_action_confirmed", request_id)
        message = _wp_privacy_account_request_confirmed_message(request_id)
        login_header(__("User action confirmed."), message)
        login_footer()
        php_exit(0)
    # end if
    if case("login"):
        pass
    # end if
    if case():
        secure_cookie = ""
        customize_login = (php_isset(lambda : PHP_REQUEST["customize-login"]))
        if customize_login:
            wp_enqueue_script("customize-base")
        # end if
        #// If the user wants SSL but the session is not SSL, force a secure cookie.
        if (not php_empty(lambda : PHP_POST["log"])) and (not force_ssl_admin()):
            user_name = sanitize_user(wp_unslash(PHP_POST["log"]))
            user = get_user_by("login", user_name)
            if (not user) and php_strpos(user_name, "@"):
                user = get_user_by("email", user_name)
            # end if
            if user:
                if get_user_option("use_ssl", user.ID):
                    secure_cookie = True
                    force_ssl_admin(True)
                # end if
            # end if
        # end if
        if (php_isset(lambda : PHP_REQUEST["redirect_to"])):
            redirect_to = PHP_REQUEST["redirect_to"]
            #// Redirect to HTTPS if user wants SSL.
            if secure_cookie and False != php_strpos(redirect_to, "wp-admin"):
                redirect_to = php_preg_replace("|^http://|", "https://", redirect_to)
            # end if
        else:
            redirect_to = admin_url()
        # end if
        reauth = False if php_empty(lambda : PHP_REQUEST["reauth"]) else True
        user = wp_signon(Array(), secure_cookie)
        if php_empty(lambda : PHP_COOKIE[LOGGED_IN_COOKIE]):
            if php_headers_sent():
                user = php_new_class("WP_Error", lambda : WP_Error("test_cookie", php_sprintf(__("<strong>Error</strong>: Cookies are blocked due to unexpected output. For help, please see <a href=\"%1$s\">this documentation</a> or try the <a href=\"%2$s\">support forums</a>."), __("https://wordpress.org/support/article/cookies/"), __("https://wordpress.org/support/forums/"))))
            elif (php_isset(lambda : PHP_POST["testcookie"])) and php_empty(lambda : PHP_COOKIE[TEST_COOKIE]):
                #// If cookies are disabled, we can't log in even with a valid user and password.
                user = php_new_class("WP_Error", lambda : WP_Error("test_cookie", php_sprintf(__("<strong>Error</strong>: Cookies are blocked or not supported by your browser. You must <a href=\"%s\">enable cookies</a> to use WordPress."), __("https://wordpress.org/support/article/cookies/#enable-cookies-in-your-browser"))))
            # end if
        # end if
        requested_redirect_to = PHP_REQUEST["redirect_to"] if (php_isset(lambda : PHP_REQUEST["redirect_to"])) else ""
        #// 
        #// Filters the login redirect URL.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string           $redirect_to           The redirect destination URL.
        #// @param string           $requested_redirect_to The requested redirect destination URL passed as a parameter.
        #// @param WP_User|WP_Error $user                  WP_User object if login was successful, WP_Error object otherwise.
        #//
        redirect_to = apply_filters("login_redirect", redirect_to, requested_redirect_to, user)
        if (not is_wp_error(user)) and (not reauth):
            if interim_login:
                message = "<p class=\"message\">" + __("You have logged in successfully.") + "</p>"
                interim_login = "success"
                login_header("", message)
                php_print("             </div>\n                ")
                #// This action is documented in wp-login.php
                do_action("login_footer")
                if customize_login:
                    php_print("                 <script type=\"text/javascript\">setTimeout( function(){ new wp.customize.Messenger({ url: '")
                    php_print(wp_customize_url())
                    php_print("', channel: 'login' }).send('login') }, 1000 );</script>\n                   ")
                # end if
                php_print("             </body></html>\n                ")
                php_exit(0)
            # end if
            #// Check if it is time to add a redirect to the admin email confirmation screen.
            if php_is_a(user, "WP_User") and user.exists() and user.has_cap("manage_options"):
                admin_email_lifespan = int(get_option("admin_email_lifespan"))
                #// If `0` (or anything "falsey" as it is cast to int) is returned, the user will not be redirected
                #// to the admin email confirmation screen.
                #// This filter is documented in wp-login.php
                admin_email_check_interval = int(apply_filters("admin_email_check_interval", 6 * MONTH_IN_SECONDS))
                if admin_email_check_interval > 0 and time() > admin_email_lifespan:
                    redirect_to = add_query_arg(Array({"action": "confirm_admin_email", "wp_lang": get_user_locale(user)}), wp_login_url(redirect_to))
                # end if
            # end if
            if php_empty(lambda : redirect_to) or "wp-admin/" == redirect_to or admin_url() == redirect_to:
                #// If the user doesn't belong to a blog, send them to user admin. If the user can't edit posts, send them to their profile.
                if is_multisite() and (not get_active_blog_for_user(user.ID)) and (not is_super_admin(user.ID)):
                    redirect_to = user_admin_url()
                elif is_multisite() and (not user.has_cap("read")):
                    redirect_to = get_dashboard_url(user.ID)
                elif (not user.has_cap("edit_posts")):
                    redirect_to = admin_url("profile.php") if user.has_cap("read") else home_url()
                # end if
                wp_redirect(redirect_to)
                php_exit(0)
            # end if
            wp_safe_redirect(redirect_to)
            php_exit(0)
        # end if
        errors = user
        #// Clear errors if loggedout is set.
        if (not php_empty(lambda : PHP_REQUEST["loggedout"])) or reauth:
            errors = php_new_class("WP_Error", lambda : WP_Error())
        # end if
        if php_empty(lambda : PHP_POST) and errors.get_error_codes() == Array("empty_username", "empty_password"):
            errors = php_new_class("WP_Error", lambda : WP_Error("", ""))
        # end if
        if interim_login:
            if (not errors.has_errors()):
                errors.add("expired", __("Your session has expired. Please log in to continue where you left off."), "message")
            # end if
        else:
            #// Some parts of this script use the main login form to display a message.
            if (php_isset(lambda : PHP_REQUEST["loggedout"])) and PHP_REQUEST["loggedout"]:
                errors.add("loggedout", __("You are now logged out."), "message")
            elif (php_isset(lambda : PHP_REQUEST["registration"])) and "disabled" == PHP_REQUEST["registration"]:
                errors.add("registerdisabled", __("User registration is currently not allowed."))
            elif (php_isset(lambda : PHP_REQUEST["checkemail"])) and "confirm" == PHP_REQUEST["checkemail"]:
                errors.add("confirm", __("Check your email for the confirmation link."), "message")
            elif (php_isset(lambda : PHP_REQUEST["checkemail"])) and "newpass" == PHP_REQUEST["checkemail"]:
                errors.add("newpass", __("Check your email for your new password."), "message")
            elif (php_isset(lambda : PHP_REQUEST["checkemail"])) and "registered" == PHP_REQUEST["checkemail"]:
                errors.add("registered", __("Registration complete. Please check your email."), "message")
            elif php_strpos(redirect_to, "about.php?updated"):
                errors.add("updated", __("<strong>You have successfully updated WordPress!</strong> Please log back in to see what&#8217;s new."), "message")
            elif WP_Recovery_Mode_Link_Service.LOGIN_ACTION_ENTERED == action:
                errors.add("enter_recovery_mode", __("Recovery Mode Initialized. Please log in to continue."), "message")
            # end if
        # end if
        #// 
        #// Filters the login page errors.
        #// 
        #// @since 3.6.0
        #// 
        #// @param WP_Error $errors      WP Error object.
        #// @param string   $redirect_to Redirect destination URL.
        #//
        errors = apply_filters("wp_login_errors", errors, redirect_to)
        #// Clear any stale cookies.
        if reauth:
            wp_clear_auth_cookie()
        # end if
        login_header(__("Log In"), "", errors)
        if (php_isset(lambda : PHP_POST["log"])):
            user_login = esc_attr(wp_unslash(PHP_POST["log"])) if "incorrect_password" == errors.get_error_code() or "empty_password" == errors.get_error_code() else ""
        # end if
        rememberme = (not php_empty(lambda : PHP_POST["rememberme"]))
        if errors.has_errors():
            aria_describedby_error = " aria-describedby=\"login_error\""
        else:
            aria_describedby_error = ""
        # end if
        wp_enqueue_script("user-profile")
        php_print("\n       <form name=\"loginform\" id=\"loginform\" action=\"")
        php_print(esc_url(site_url("wp-login.php", "login_post")))
        php_print("\" method=\"post\">\n            <p>\n               <label for=\"user_login\">")
        _e("Username or Email Address")
        php_print("</label>\n               <input type=\"text\" name=\"log\" id=\"user_login\"")
        php_print(aria_describedby_error)
        php_print(" class=\"input\" value=\"")
        php_print(esc_attr(user_login))
        php_print("""\" size=\"20\" autocapitalize=\"off\" />
        </p>
        <div class=\"user-pass-wrap\">
        <label for=\"user_pass\">""")
        _e("Password")
        php_print("</label>\n               <div class=\"wp-pwd\">\n                    <input type=\"password\" name=\"pwd\" id=\"user_pass\"")
        php_print(aria_describedby_error)
        php_print(" class=\"input password-input\" value=\"\" size=\"20\" />\n                  <button type=\"button\" class=\"button button-secondary wp-hide-pw hide-if-no-js\" data-toggle=\"0\" aria-label=\"")
        esc_attr_e("Show password")
        php_print("""\">
        <span class=\"dashicons dashicons-visibility\" aria-hidden=\"true\"></span>
        </button>
        </div>
        </div>
        """)
        #// 
        #// Fires following the 'Password' field in the login form.
        #// 
        #// @since 2.1.0
        #//
        do_action("login_form")
        php_print("         <p class=\"forgetmenot\"><input name=\"rememberme\" type=\"checkbox\" id=\"rememberme\" value=\"forever\" ")
        checked(rememberme)
        php_print(" /> <label for=\"rememberme\">")
        esc_html_e("Remember Me")
        php_print("</label></p>\n           <p class=\"submit\">\n              <input type=\"submit\" name=\"wp-submit\" id=\"wp-submit\" class=\"button button-primary button-large\" value=\"")
        esc_attr_e("Log In")
        php_print("\" />\n              ")
        if interim_login:
            php_print("                 <input type=\"hidden\" name=\"interim-login\" value=\"1\" />\n                  ")
        else:
            php_print("                 <input type=\"hidden\" name=\"redirect_to\" value=\"")
            php_print(esc_attr(redirect_to))
            php_print("\" />\n                  ")
        # end if
        if customize_login:
            php_print("                 <input type=\"hidden\" name=\"customize-login\" value=\"1\" />\n                    ")
        # end if
        php_print("""               <input type=\"hidden\" name=\"testcookie\" value=\"1\" />
        </p>
        </form>
        """)
        if (not interim_login):
            php_print("         <p id=\"nav\">\n                ")
            if (not (php_isset(lambda : PHP_REQUEST["checkemail"]))) or (not php_in_array(PHP_REQUEST["checkemail"], Array("confirm", "newpass"), True)):
                if get_option("users_can_register"):
                    registration_url = php_sprintf("<a href=\"%s\">%s</a>", esc_url(wp_registration_url()), __("Register"))
                    #// This filter is documented in wp-includes/general-template.php
                    php_print(apply_filters("register", registration_url))
                    php_print(esc_html(login_link_separator))
                # end if
                php_print("                 <a href=\"")
                php_print(esc_url(wp_lostpassword_url()))
                php_print("\">")
                _e("Lost your password?")
                php_print("</a>\n                   ")
            # end if
            php_print("         </p>\n          ")
        # end if
        login_script = "function wp_attempt_focus() {"
        login_script += "setTimeout( function() {"
        login_script += "try {"
        if user_login:
            login_script += "d = document.getElementById( \"user_pass\" ); d.value = \"\";"
        else:
            login_script += "d = document.getElementById( \"user_login\" );"
            if errors.get_error_code() == "invalid_username":
                login_script += "d.value = \"\";"
            # end if
        # end if
        login_script += "d.focus(); d.select();"
        login_script += "} catch( er ) {}"
        login_script += "}, 200);"
        login_script += "}\n"
        #// End of wp_attempt_focus().
        #// 
        #// Filters whether to print the call to `wp_attempt_focus()` on the login screen.
        #// 
        #// @since 4.8.0
        #// 
        #// @param bool $print Whether to print the function call. Default true.
        #//
        if apply_filters("enable_login_autofocus", True) and (not error):
            login_script += "wp_attempt_focus();\n"
        # end if
        #// Run `wpOnload()` if defined.
        login_script += "if ( typeof wpOnload === 'function' ) { wpOnload() }"
        php_print("     <script type=\"text/javascript\">\n         ")
        php_print(login_script)
        php_print("     </script>\n     ")
        if interim_login:
            php_print("""           <script type=\"text/javascript\">
            ( function() {
        try {
            var i, links = document.getElementsByTagName( 'a' );
        for ( i in links ) {
        if ( links[i].href ) {
            links[i].target = '_blank';
            links[i].rel = 'noreferrer noopener';
            }
            }
            } catch( er ) {}
            }());
            </script>
            """)
        # end if
        login_footer()
        break
    # end if
# end for
pass
