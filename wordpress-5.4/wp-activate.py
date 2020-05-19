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
#// Confirms that the activation key that is sent in an email after a user signs
#// up for a new site matches the key for that user and then displays confirmation.
#// 
#// @package WordPress
#//
php_define("WP_INSTALLING", True)
#// Sets up the WordPress Environment.
php_include_file(__DIR__ + "/wp-load.php", once=False)
php_include_file(__DIR__ + "/wp-blog-header.php", once=False)
if (not is_multisite()):
    wp_redirect(wp_registration_url())
    php_exit(0)
# end if
valid_error_codes_ = Array("already_active", "blog_taken")
activate_path_ = php_explode("?", wp_unslash(PHP_SERVER["REQUEST_URI"]))
activate_cookie_ = "wp-activate-" + COOKIEHASH
key_ = ""
result_ = None
if (php_isset(lambda : PHP_REQUEST["key"])) and (php_isset(lambda : PHP_POST["key"])) and PHP_REQUEST["key"] != PHP_POST["key"]:
    wp_die(__("A key value mismatch has been detected. Please follow the link provided in your activation email."), __("An error occurred during the activation"), 400)
elif (not php_empty(lambda : PHP_REQUEST["key"])):
    key_ = PHP_REQUEST["key"]
elif (not php_empty(lambda : PHP_POST["key"])):
    key_ = PHP_POST["key"]
# end if
if key_:
    redirect_url_ = remove_query_arg("key")
    if remove_query_arg(False) != redirect_url_:
        setcookie(activate_cookie_, key_, 0, activate_path_, COOKIE_DOMAIN, is_ssl(), True)
        wp_safe_redirect(redirect_url_)
        php_exit(0)
    else:
        result_ = wpmu_activate_signup(key_)
    # end if
# end if
if None == result_ and (php_isset(lambda : PHP_COOKIE[activate_cookie_])):
    key_ = PHP_COOKIE[activate_cookie_]
    result_ = wpmu_activate_signup(key_)
    setcookie(activate_cookie_, " ", time() - YEAR_IN_SECONDS, activate_path_, COOKIE_DOMAIN, is_ssl(), True)
# end if
if None == result_ or is_wp_error(result_) and "invalid_key" == result_.get_error_code():
    status_header(404)
elif is_wp_error(result_):
    error_code_ = result_.get_error_code()
    if (not php_in_array(error_code_, valid_error_codes_)):
        status_header(400)
    # end if
# end if
nocache_headers()
if php_is_object(wp_object_cache_):
    wp_object_cache_.cache_enabled = False
# end if
#// Fix for page title.
wp_query_.is_404 = False
#// 
#// Fires before the Site Activation page is loaded.
#// 
#// @since 3.0.0
#//
do_action("activate_header")
#// 
#// Adds an action hook specific to this page.
#// 
#// Fires on {@see 'wp_head'}.
#// 
#// @since MU (3.0.0)
#//
def do_activate_header(*_args_):
    
    
    #// 
    #// Fires before the Site Activation page is loaded.
    #// 
    #// Fires on the {@see 'wp_head'} action.
    #// 
    #// @since 3.0.0
    #//
    do_action("activate_wp_head")
# end def do_activate_header
add_action("wp_head", "do_activate_header")
#// 
#// Loads styles specific to this page.
#// 
#// @since MU (3.0.0)
#//
def wpmu_activate_stylesheet(*_args_):
    
    
    php_print("""   <style type=\"text/css\">
    form { margin-top: 2em; }
    #submit, #key { width: 90%; font-size: 24px; }
    #language { margin-top: .5em; }
    .error { background: #f66; }
    span.h3 { padding: 0 8px; font-size: 1.3em; font-weight: 600; }
    </style>
    """)
# end def wpmu_activate_stylesheet
add_action("wp_head", "wpmu_activate_stylesheet")
add_action("wp_head", "wp_sensitive_page_meta")
get_header("wp-activate")
php_print("""
<div id=\"signup-content\" class=\"widecolumn\">
<div class=\"wp-activate-container\">
""")
if (not key_):
    php_print("\n       <h2>")
    _e("Activation Key Required")
    php_print("</h2>\n      <form name=\"activateform\" id=\"activateform\" method=\"post\" action=\"")
    php_print(network_site_url("wp-activate.php"))
    php_print("\">\n            <p>\n               <label for=\"key\">")
    _e("Activation Key:")
    php_print("""</label>
    <br /><input type=\"text\" name=\"key\" id=\"key\" value=\"\" size=\"50\" />
    </p>
    <p class=\"submit\">
    <input id=\"submit\" type=\"submit\" name=\"Submit\" class=\"submit\" value=\"""")
    esc_attr_e("Activate")
    php_print("""\" />
    </p>
    </form>
    """)
else:
    if is_wp_error(result_) and php_in_array(result_.get_error_code(), valid_error_codes_):
        signup_ = result_.get_error_data()
        php_print("         <h2>")
        _e("Your account is now active!")
        php_print("</h2>\n          ")
        php_print("<p class=\"lead-in\">")
        if "" == signup_.domain + signup_.path:
            php_printf(__("Your account has been activated. You may now <a href=\"%1$s\">log in</a> to the site using your chosen username of &#8220;%2$s&#8221;. Please check your email inbox at %3$s for your password and login instructions. If you do not receive an email, please check your junk or spam folder. If you still do not receive an email within an hour, you can <a href=\"%4$s\">reset your password</a>."), network_site_url("wp-login.php", "login"), signup_.user_login, signup_.user_email, wp_lostpassword_url())
        else:
            php_printf(__("Your site at %1$s is active. You may now log in to your site using your chosen username of &#8220;%2$s&#8221;. Please check your email inbox at %3$s for your password and login instructions. If you do not receive an email, please check your junk or spam folder. If you still do not receive an email within an hour, you can <a href=\"%4$s\">reset your password</a>."), php_sprintf("<a href=\"http://%1$s\">%1$s</a>", signup_.domain), signup_.user_login, signup_.user_email, wp_lostpassword_url())
        # end if
        php_print("</p>")
    elif None == result_ or is_wp_error(result_):
        php_print("         <h2>")
        _e("An error occurred during the activation")
        php_print("</h2>\n          ")
        if is_wp_error(result_):
            php_print("             <p>")
            php_print(result_.get_error_message())
            php_print("</p>\n           ")
        # end if
        php_print("         ")
    else:
        url_ = get_home_url(php_int(result_["blog_id"])) if (php_isset(lambda : result_["blog_id"])) else ""
        user_ = get_userdata(php_int(result_["user_id"]))
        php_print("         <h2>")
        _e("Your account is now active!")
        php_print("""</h2>
        <div id=\"signup-welcome\">
        <p><span class=\"h3\">""")
        _e("Username:")
        php_print("</span> ")
        php_print(user_.user_login)
        php_print("</p>\n           <p><span class=\"h3\">")
        _e("Password:")
        php_print("</span> ")
        php_print(result_["password"])
        php_print("""</p>
        </div>
        """)
        if url_ and network_home_url("", "http") != url_:
            switch_to_blog(php_int(result_["blog_id"]))
            login_url_ = wp_login_url()
            restore_current_blog()
            php_print("             <p class=\"view\">\n                ")
            #// translators: 1: Site URL, 2: Login URL.
            php_printf(__("Your account is now activated. <a href=\"%1$s\">View your site</a> or <a href=\"%2$s\">Log in</a>"), url_, esc_url(login_url_))
            php_print("             </p>\n          ")
        else:
            php_print("             <p class=\"view\">\n                ")
            #// translators: 1: Login URL, 2: Network home URL.
            php_printf(__("Your account is now activated. <a href=\"%1$s\">Log in</a> or go back to the <a href=\"%2$s\">homepage</a>."), network_site_url("wp-login.php", "login"), network_home_url())
            php_print("             </p>\n              ")
        # end if
    # end if
# end if
php_print("""   </div>
</div>
<script type=\"text/javascript\">
var key_input = document.getElementById('key');
key_input && key_input.focus();
</script>
""")
get_footer("wp-activate")
