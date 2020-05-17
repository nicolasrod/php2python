#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// Sets up the WordPress Environment.
php_include_file(__DIR__ + "/wp-load.php", once=False)
add_action("wp_head", "wp_no_robots")
php_include_file(__DIR__ + "/wp-blog-header.php", once=False)
nocache_headers()
if php_is_array(get_site_option("illegal_names")) and (php_isset(lambda : PHP_REQUEST["new"])) and php_in_array(PHP_REQUEST["new"], get_site_option("illegal_names")):
    wp_redirect(network_home_url())
    php_exit(0)
# end if
#// 
#// Prints signup_header via wp_head
#// 
#// @since MU (3.0.0)
#//
def do_signup_header(*_args_):
    
    
    #// 
    #// Fires within the head section of the site sign-up screen.
    #// 
    #// @since 3.0.0
    #//
    do_action("signup_header")
# end def do_signup_header
add_action("wp_head", "do_signup_header")
if (not is_multisite()):
    wp_redirect(wp_registration_url())
    php_exit(0)
# end if
if (not is_main_site()):
    wp_redirect(network_site_url("wp-signup.php"))
    php_exit(0)
# end if
#// Fix for page title.
wp_query_.is_404 = False
#// 
#// Fires before the Site Signup page is loaded.
#// 
#// @since 4.4.0
#//
do_action("before_signup_header")
#// 
#// Prints styles for front-end Multisite signup pages
#// 
#// @since MU (3.0.0)
#//
def wpmu_signup_stylesheet(*_args_):
    
    
    php_print("""   <style type=\"text/css\">
    .mu_register { width: 90%; margin:0 auto; }
    .mu_register form { margin-top: 2em; }
    .mu_register .error { font-weight: 600; padding: 10px; color: #333333; background: #FFEBE8; border: 1px solid #CC0000; }
    .mu_register input[type=\"submit\"],
    .mu_register #blog_title,
    .mu_register #user_email,
    .mu_register #blogname,
    .mu_register #user_name { width:100%; font-size: 24px; margin:5px 0; }
    .mu_register #site-language { display: block; }
    .mu_register .prefix_address,
    .mu_register .suffix_address { font-size: 18px; display:inline; }
    .mu_register label { font-weight: 600; font-size: 15px; display: block; margin: 10px 0; }
    .mu_register label.checkbox { display:inline; }
    .mu_register .mu_alert { font-weight: 600; padding: 10px; color: #333333; background: #ffffe0; border: 1px solid #e6db55; }
    </style>
    """)
# end def wpmu_signup_stylesheet
add_action("wp_head", "wpmu_signup_stylesheet")
get_header("wp-signup")
#// 
#// Fires before the site sign-up form.
#// 
#// @since 3.0.0
#//
do_action("before_signup_form")
php_print("<div id=\"signup-content\" class=\"widecolumn\">\n<div class=\"mu_register wp-signup-container\" role=\"main\">\n")
#// 
#// Generates and displays the Signup and Create Site forms
#// 
#// @since MU (3.0.0)
#// 
#// @param string          $blogname   The new site name.
#// @param string          $blog_title The new site title.
#// @param WP_Error|string $errors     A WP_Error object containing existing errors. Defaults to empty string.
#//
def show_blog_form(blogname_="", blog_title_="", errors_="", *_args_):
    
    
    if (not is_wp_error(errors_)):
        errors_ = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    current_network_ = get_network()
    #// Blog name.
    if (not is_subdomain_install()):
        php_print("<label for=\"blogname\">" + __("Site Name:") + "</label>")
    else:
        php_print("<label for=\"blogname\">" + __("Site Domain:") + "</label>")
    # end if
    errmsg_ = errors_.get_error_message("blogname")
    if errmsg_:
        php_print("     <p class=\"error\">")
        php_print(errmsg_)
        php_print("</p>\n       ")
    # end if
    if (not is_subdomain_install()):
        php_print("<span class=\"prefix_address\">" + current_network_.domain + current_network_.path + "</span><input name=\"blogname\" type=\"text\" id=\"blogname\" value=\"" + esc_attr(blogname_) + "\" maxlength=\"60\" /><br />")
    else:
        site_domain_ = php_preg_replace("|^www\\.|", "", current_network_.domain)
        php_print("<input name=\"blogname\" type=\"text\" id=\"blogname\" value=\"" + esc_attr(blogname_) + "\" maxlength=\"60\" /><span class=\"suffix_address\">." + esc_html(site_domain_) + "</span><br />")
    # end if
    if (not is_user_logged_in()):
        if (not is_subdomain_install()):
            site_ = current_network_.domain + current_network_.path + __("sitename")
        else:
            site_ = __("domain") + "." + site_domain_ + current_network_.path
        # end if
        printf("<p>(<strong>%s</strong>) %s</p>", php_sprintf(__("Your address will be %s."), site_), __("Must be at least 4 characters, letters and numbers only. It cannot be changed, so choose carefully!"))
    # end if
    pass
    php_print(" <label for=\"blog_title\">")
    _e("Site Title:")
    php_print("</label>\n   ")
    errmsg_ = errors_.get_error_message("blog_title")
    if errmsg_:
        php_print("     <p class=\"error\">")
        php_print(errmsg_)
        php_print("</p>\n       ")
    # end if
    php_print("<input name=\"blog_title\" type=\"text\" id=\"blog_title\" value=\"" + esc_attr(blog_title_) + "\" />")
    php_print("\n   ")
    #// Site Language.
    languages_ = signup_get_available_languages()
    if (not php_empty(lambda : languages_)):
        php_print("     <p>\n           <label for=\"site-language\">")
        _e("Site Language:")
        php_print("</label>\n           ")
        #// Network default.
        lang_ = get_site_option("WPLANG")
        if (php_isset(lambda : PHP_POST["WPLANG"])):
            lang_ = PHP_POST["WPLANG"]
        # end if
        #// Use US English if the default isn't available.
        if (not php_in_array(lang_, languages_)):
            lang_ = ""
        # end if
        wp_dropdown_languages(Array({"name": "WPLANG", "id": "site-language", "selected": lang_, "languages": languages_, "show_available_translations": False}))
        php_print("     </p>\n      ")
    # end if
    #// Languages.
    blog_public_on_checked_ = ""
    blog_public_off_checked_ = ""
    if (php_isset(lambda : PHP_POST["blog_public"])) and "0" == PHP_POST["blog_public"]:
        blog_public_off_checked_ = "checked=\"checked\""
    else:
        blog_public_on_checked_ = "checked=\"checked\""
    # end if
    php_print("""
    <div id=\"privacy\">
    <p class=\"privacy-intro\">
    """)
    _e("Privacy:")
    php_print("         ")
    _e("Allow search engines to index this site.")
    php_print("         <br style=\"clear:both\" />\n           <label class=\"checkbox\" for=\"blog_public_on\">\n             <input type=\"radio\" id=\"blog_public_on\" name=\"blog_public\" value=\"1\" ")
    php_print(blog_public_on_checked_)
    php_print(" />\n                <strong>")
    _e("Yes")
    php_print("""</strong>
    </label>
    <label class=\"checkbox\" for=\"blog_public_off\">
    <input type=\"radio\" id=\"blog_public_off\" name=\"blog_public\" value=\"0\" """)
    php_print(blog_public_off_checked_)
    php_print(" />\n                <strong>")
    _e("No")
    php_print("""</strong>
    </label>
    </p>
    </div>
    """)
    #// 
    #// Fires after the site sign-up form.
    #// 
    #// @since 3.0.0
    #// 
    #// @param WP_Error $errors A WP_Error object possibly containing 'blogname' or 'blog_title' errors.
    #//
    do_action("signup_blogform", errors_)
# end def show_blog_form
#// 
#// Validate the new site signup
#// 
#// @since MU (3.0.0)
#// 
#// @return array Contains the new site data and error messages.
#//
def validate_blog_form(*_args_):
    
    
    user_ = ""
    if is_user_logged_in():
        user_ = wp_get_current_user()
    # end if
    return wpmu_validate_blog_signup(PHP_POST["blogname"], PHP_POST["blog_title"], user_)
# end def validate_blog_form
#// 
#// Display user registration form
#// 
#// @since MU (3.0.0)
#// 
#// @param string          $user_name  The entered username.
#// @param string          $user_email The entered email address.
#// @param WP_Error|string $errors     A WP_Error object containing existing errors. Defaults to empty string.
#//
def show_user_form(user_name_="", user_email_="", errors_="", *_args_):
    
    
    if (not is_wp_error(errors_)):
        errors_ = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    #// Username.
    php_print("<label for=\"user_name\">" + __("Username:") + "</label>")
    errmsg_ = errors_.get_error_message("user_name")
    if errmsg_:
        php_print("<p class=\"error\">" + errmsg_ + "</p>")
    # end if
    php_print("<input name=\"user_name\" type=\"text\" id=\"user_name\" value=\"" + esc_attr(user_name_) + "\" autocapitalize=\"none\" autocorrect=\"off\" maxlength=\"60\" /><br />")
    _e("(Must be at least 4 characters, letters and numbers only.)")
    php_print("\n   <label for=\"user_email\">")
    _e("Email&nbsp;Address:")
    php_print("</label>\n   ")
    errmsg_ = errors_.get_error_message("user_email")
    if errmsg_:
        php_print("     <p class=\"error\">")
        php_print(errmsg_)
        php_print("</p>\n   ")
    # end if
    php_print(" <input name=\"user_email\" type=\"email\" id=\"user_email\" value=\"")
    php_print(esc_attr(user_email_))
    php_print("\" maxlength=\"200\" /><br />")
    _e("We send your registration email to this address. (Double-check your email address before continuing.)")
    php_print(" ")
    errmsg_ = errors_.get_error_message("generic")
    if errmsg_:
        php_print("<p class=\"error\">" + errmsg_ + "</p>")
    # end if
    #// 
    #// Fires at the end of the user registration form on the site sign-up form.
    #// 
    #// @since 3.0.0
    #// 
    #// @param WP_Error $errors A WP_Error object containing 'user_name' or 'user_email' errors.
    #//
    do_action("signup_extra_fields", errors_)
# end def show_user_form
#// 
#// Validate user signup name and email
#// 
#// @since MU (3.0.0)
#// 
#// @return array Contains username, email, and error messages.
#//
def validate_user_form(*_args_):
    
    
    return wpmu_validate_user_signup(PHP_POST["user_name"], PHP_POST["user_email"])
# end def validate_user_form
#// 
#// Allow returning users to sign up for another site
#// 
#// @since MU (3.0.0)
#// 
#// @param string          $blogname   The new site name
#// @param string          $blog_title The new site title.
#// @param WP_Error|string $errors     A WP_Error object containing existing errors. Defaults to empty string.
#//
def signup_another_blog(blogname_="", blog_title_="", errors_="", *_args_):
    
    
    current_user_ = wp_get_current_user()
    if (not is_wp_error(errors_)):
        errors_ = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    signup_defaults_ = Array({"blogname": blogname_, "blog_title": blog_title_, "errors": errors_})
    #// 
    #// Filters the default site sign-up variables.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $signup_defaults {
    #// An array of default site sign-up variables.
    #// 
    #// @type string   $blogname   The site blogname.
    #// @type string   $blog_title The site title.
    #// @type WP_Error $errors     A WP_Error object possibly containing 'blogname' or 'blog_title' errors.
    #// }
    #//
    filtered_results_ = apply_filters("signup_another_blog_init", signup_defaults_)
    blogname_ = filtered_results_["blogname"]
    blog_title_ = filtered_results_["blog_title"]
    errors_ = filtered_results_["errors"]
    #// translators: %s: Network title.
    php_print("<h2>" + php_sprintf(__("Get <em>another</em> %s site in seconds"), get_network().site_name) + "</h2>")
    if errors_.has_errors():
        php_print("<p>" + __("There was a problem, please correct the form below and try again.") + "</p>")
    # end if
    php_print(" <p>\n       ")
    printf(__("Welcome back, %s. By filling out the form below, you can <strong>add another site to your account</strong>. There is no limit to the number of sites you can have, so create to your heart&#8217;s content, but write responsibly!"), current_user_.display_name)
    php_print(" </p>\n\n    ")
    blogs_ = get_blogs_of_user(current_user_.ID)
    if (not php_empty(lambda : blogs_)):
        php_print("\n           <p>")
        _e("Sites you are already a member of:")
        php_print("</p>\n           <ul>\n              ")
        for blog_ in blogs_:
            home_url_ = get_home_url(blog_.userblog_id)
            php_print("<li><a href=\"" + esc_url(home_url_) + "\">" + home_url_ + "</a></li>")
        # end for
        php_print("         </ul>\n ")
    # end if
    php_print("\n   <p>")
    _e("If you&#8217;re not going to use a great site domain, leave it for a new user. Now have at it!")
    php_print("""</p>
    <form id=\"setupform\" method=\"post\" action=\"wp-signup.php\">
    <input type=\"hidden\" name=\"stage\" value=\"gimmeanotherblog\" />
    """)
    #// 
    #// Hidden sign-up form fields output when creating another site or user.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string $context A string describing the steps of the sign-up process. The value can be
    #// 'create-another-site', 'validate-user', or 'validate-site'.
    #//
    do_action("signup_hidden_fields", "create-another-site")
    php_print("     ")
    show_blog_form(blogname_, blog_title_, errors_)
    php_print("     <p class=\"submit\"><input type=\"submit\" name=\"submit\" class=\"submit\" value=\"")
    esc_attr_e("Create Site")
    php_print("\" /></p>\n  </form>\n   ")
# end def signup_another_blog
#// 
#// Validate a new site signup for an existing user.
#// 
#// @global string          $blogname   The new site's subdomain or directory name.
#// @global string          $blog_title The new site's title.
#// @global WP_Error        $errors     Existing errors in the global scope.
#// @global string          $domain     The new site's domain.
#// @global string          $path       The new site's path.
#// 
#// @since MU (3.0.0)
#// 
#// @return null|bool True if site signup was validated, false if error.
#// The function halts all execution if the user is not logged in.
#//
def validate_another_blog_signup(*_args_):
    
    
    global blogname_
    global blog_title_
    global errors_
    global domain_
    global path_
    php_check_if_defined("blogname_","blog_title_","errors_","domain_","path_")
    current_user_ = wp_get_current_user()
    if (not is_user_logged_in()):
        php_exit(0)
    # end if
    result_ = validate_blog_form()
    #// Extracted values set/overwrite globals.
    domain_ = result_["domain"]
    path_ = result_["path"]
    blogname_ = result_["blogname"]
    blog_title_ = result_["blog_title"]
    errors_ = result_["errors"]
    if errors_.has_errors():
        signup_another_blog(blogname_, blog_title_, errors_)
        return False
    # end if
    public_ = php_int(PHP_POST["blog_public"])
    blog_meta_defaults_ = Array({"lang_id": 1, "public": public_})
    #// Handle the language setting for the new site.
    if (not php_empty(lambda : PHP_POST["WPLANG"])):
        languages_ = signup_get_available_languages()
        if php_in_array(PHP_POST["WPLANG"], languages_):
            language_ = wp_unslash(sanitize_text_field(PHP_POST["WPLANG"]))
            if language_:
                blog_meta_defaults_["WPLANG"] = language_
            # end if
        # end if
    # end if
    #// 
    #// Filters the new site meta variables.
    #// 
    #// Use the {@see 'add_signup_meta'} filter instead.
    #// 
    #// @since MU (3.0.0)
    #// @deprecated 3.0.0 Use the {@see 'add_signup_meta'} filter instead.
    #// 
    #// @param array $blog_meta_defaults An array of default blog meta variables.
    #//
    meta_defaults_ = apply_filters_deprecated("signup_create_blog_meta", Array(blog_meta_defaults_), "3.0.0", "add_signup_meta")
    #// 
    #// Filters the new default site meta variables.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $meta {
    #// An array of default site meta variables.
    #// 
    #// @type int $lang_id     The language ID.
    #// @type int $blog_public Whether search engines should be discouraged from indexing the site. 1 for true, 0 for false.
    #// }
    #//
    meta_ = apply_filters("add_signup_meta", meta_defaults_)
    blog_id_ = wpmu_create_blog(domain_, path_, blog_title_, current_user_.ID, meta_, get_current_network_id())
    if is_wp_error(blog_id_):
        return False
    # end if
    confirm_another_blog_signup(domain_, path_, blog_title_, current_user_.user_login, current_user_.user_email, meta_, blog_id_)
    return True
# end def validate_another_blog_signup
#// 
#// Confirm a new site signup.
#// 
#// @since MU (3.0.0)
#// @since 4.4.0 Added the `$blog_id` parameter.
#// 
#// @param string $domain     The domain URL.
#// @param string $path       The site root path.
#// @param string $blog_title The site title.
#// @param string $user_name  The username.
#// @param string $user_email The user's email address.
#// @param array  $meta       Any additional meta from the {@see 'add_signup_meta'} filter in validate_blog_signup().
#// @param int    $blog_id    The site ID.
#//
def confirm_another_blog_signup(domain_=None, path_=None, blog_title_=None, user_name_=None, user_email_="", meta_=None, blog_id_=0, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    if blog_id_:
        switch_to_blog(blog_id_)
        home_url_ = home_url("/")
        login_url_ = wp_login_url()
        restore_current_blog()
    else:
        home_url_ = "http://" + domain_ + path_
        login_url_ = "http://" + domain_ + path_ + "wp-login.php"
    # end if
    site_ = php_sprintf("<a href=\"%1$s\">%2$s</a>", esc_url(home_url_), blog_title_)
    php_print(" <h2>\n  ")
    #// translators: %s: Site title.
    printf(__("The site %s is yours."), site_)
    php_print(" </h2>\n <p>\n       ")
    printf(__("%1$s is your new site. <a href=\"%2$s\">Log in</a> as &#8220;%3$s&#8221; using your existing password."), php_sprintf("<a href=\"%s\">%s</a>", esc_url(home_url_), untrailingslashit(domain_ + path_)), esc_url(login_url_), user_name_)
    php_print(" </p>\n  ")
    #// 
    #// Fires when the site or user sign-up process is complete.
    #// 
    #// @since 3.0.0
    #//
    do_action("signup_finished")
# end def confirm_another_blog_signup
#// 
#// Setup the new user signup process
#// 
#// @since MU (3.0.0)
#// 
#// @param string          $user_name  The username.
#// @param string          $user_email The user's email.
#// @param WP_Error|string $errors     A WP_Error object containing existing errors. Defaults to empty string.
#//
def signup_user(user_name_="", user_email_="", errors_="", *_args_):
    
    
    global active_signup_
    php_check_if_defined("active_signup_")
    if (not is_wp_error(errors_)):
        errors_ = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    signup_for_ = esc_html(PHP_POST["signup_for"]) if (php_isset(lambda : PHP_POST["signup_for"])) else "blog"
    signup_user_defaults_ = Array({"user_name": user_name_, "user_email": user_email_, "errors": errors_})
    #// 
    #// Filters the default user variables used on the user sign-up form.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $signup_user_defaults {
    #// An array of default user variables.
    #// 
    #// @type string   $user_name  The user username.
    #// @type string   $user_email The user email address.
    #// @type WP_Error $errors     A WP_Error object with possible errors relevant to the sign-up user.
    #// }
    #//
    filtered_results_ = apply_filters("signup_user_init", signup_user_defaults_)
    user_name_ = filtered_results_["user_name"]
    user_email_ = filtered_results_["user_email"]
    errors_ = filtered_results_["errors"]
    php_print("\n   <h2>\n  ")
    #// translators: %s: Name of the network.
    printf(__("Get your own %s account in seconds"), get_network().site_name)
    php_print("""   </h2>
    <form id=\"setupform\" method=\"post\" action=\"wp-signup.php\" novalidate=\"novalidate\">
    <input type=\"hidden\" name=\"stage\" value=\"validate-user-signup\" />
    """)
    #// This action is documented in wp-signup.php
    do_action("signup_hidden_fields", "validate-user")
    php_print("     ")
    show_user_form(user_name_, user_email_, errors_)
    php_print("\n       <p>\n       ")
    if "blog" == active_signup_:
        php_print("         <input id=\"signupblog\" type=\"hidden\" name=\"signup_for\" value=\"blog\" />\n        ")
    elif "user" == active_signup_:
        php_print("         <input id=\"signupblog\" type=\"hidden\" name=\"signup_for\" value=\"user\" />\n        ")
    else:
        php_print("         <input id=\"signupblog\" type=\"radio\" name=\"signup_for\" value=\"blog\" ")
        checked(signup_for_, "blog")
        php_print(" />\n            <label class=\"checkbox\" for=\"signupblog\">")
        _e("Gimme a site!")
        php_print("</label>\n           <br />\n            <input id=\"signupuser\" type=\"radio\" name=\"signup_for\" value=\"user\" ")
        checked(signup_for_, "user")
        php_print(" />\n            <label class=\"checkbox\" for=\"signupuser\">")
        _e("Just a username, please.")
        php_print("</label>\n       ")
    # end if
    php_print("     </p>\n\n        <p class=\"submit\"><input type=\"submit\" name=\"submit\" class=\"submit\" value=\"")
    esc_attr_e("Next")
    php_print("\" /></p>\n  </form>\n   ")
# end def signup_user
#// 
#// Validate the new user signup
#// 
#// @since MU (3.0.0)
#// 
#// @return bool True if new user signup was validated, false if error
#//
def validate_user_signup(*_args_):
    
    
    result_ = validate_user_form()
    user_name_ = result_["user_name"]
    user_email_ = result_["user_email"]
    errors_ = result_["errors"]
    if errors_.has_errors():
        signup_user(user_name_, user_email_, errors_)
        return False
    # end if
    if "blog" == PHP_POST["signup_for"]:
        signup_blog(user_name_, user_email_)
        return False
    # end if
    #// This filter is documented in wp-signup.php
    wpmu_signup_user(user_name_, user_email_, apply_filters("add_signup_meta", Array()))
    confirm_user_signup(user_name_, user_email_)
    return True
# end def validate_user_signup
#// 
#// New user signup confirmation
#// 
#// @since MU (3.0.0)
#// 
#// @param string $user_name The username
#// @param string $user_email The user's email address
#//
def confirm_user_signup(user_name_=None, user_email_=None, *_args_):
    
    
    php_print(" <h2>\n  ")
    #// translators: %s: Username.
    printf(__("%s is your new username"), user_name_)
    php_print(" </h2>\n <p>")
    _e("But, before you can start using your new username, <strong>you must activate it</strong>.")
    php_print("</p>\n   <p>\n   ")
    #// translators: %s: Email address.
    printf(__("Check your inbox at %s and click the link given."), "<strong>" + user_email_ + "</strong>")
    php_print(" </p>\n  <p>")
    _e("If you do not activate your username within two days, you will have to sign up again.")
    php_print("</p>\n   ")
    #// This action is documented in wp-signup.php
    do_action("signup_finished")
# end def confirm_user_signup
#// 
#// Setup the new site signup
#// 
#// @since MU (3.0.0)
#// 
#// @param string          $user_name  The username.
#// @param string          $user_email The user's email address.
#// @param string          $blogname   The site name.
#// @param string          $blog_title The site title.
#// @param WP_Error|string $errors     A WP_Error object containing existing errors. Defaults to empty string.
#//
def signup_blog(user_name_="", user_email_="", blogname_="", blog_title_="", errors_="", *_args_):
    
    
    if (not is_wp_error(errors_)):
        errors_ = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    signup_blog_defaults_ = Array({"user_name": user_name_, "user_email": user_email_, "blogname": blogname_, "blog_title": blog_title_, "errors": errors_})
    #// 
    #// Filters the default site creation variables for the site sign-up form.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $signup_blog_defaults {
    #// An array of default site creation variables.
    #// 
    #// @type string   $user_name  The user username.
    #// @type string   $user_email The user email address.
    #// @type string   $blogname   The blogname.
    #// @type string   $blog_title The title of the site.
    #// @type WP_Error $errors     A WP_Error object with possible errors relevant to new site creation variables.
    #// }
    #//
    filtered_results_ = apply_filters("signup_blog_init", signup_blog_defaults_)
    user_name_ = filtered_results_["user_name"]
    user_email_ = filtered_results_["user_email"]
    blogname_ = filtered_results_["blogname"]
    blog_title_ = filtered_results_["blog_title"]
    errors_ = filtered_results_["errors"]
    if php_empty(lambda : blogname_):
        blogname_ = user_name_
    # end if
    php_print(" <form id=\"setupform\" method=\"post\" action=\"wp-signup.php\">\n      <input type=\"hidden\" name=\"stage\" value=\"validate-blog-signup\" />\n       <input type=\"hidden\" name=\"user_name\" value=\"")
    php_print(esc_attr(user_name_))
    php_print("\" />\n      <input type=\"hidden\" name=\"user_email\" value=\"")
    php_print(esc_attr(user_email_))
    php_print("\" />\n      ")
    #// This action is documented in wp-signup.php
    do_action("signup_hidden_fields", "validate-site")
    php_print("     ")
    show_blog_form(blogname_, blog_title_, errors_)
    php_print("     <p class=\"submit\"><input type=\"submit\" name=\"submit\" class=\"submit\" value=\"")
    esc_attr_e("Signup")
    php_print("\" /></p>\n  </form>\n   ")
# end def signup_blog
#// 
#// Validate new site signup
#// 
#// @since MU (3.0.0)
#// 
#// @return bool True if the site signup was validated, false if error
#//
def validate_blog_signup(*_args_):
    
    
    #// Re-validate user info.
    user_result_ = wpmu_validate_user_signup(PHP_POST["user_name"], PHP_POST["user_email"])
    user_name_ = user_result_["user_name"]
    user_email_ = user_result_["user_email"]
    user_errors_ = user_result_["errors"]
    if user_errors_.has_errors():
        signup_user(user_name_, user_email_, user_errors_)
        return False
    # end if
    result_ = wpmu_validate_blog_signup(PHP_POST["blogname"], PHP_POST["blog_title"])
    domain_ = result_["domain"]
    path_ = result_["path"]
    blogname_ = result_["blogname"]
    blog_title_ = result_["blog_title"]
    errors_ = result_["errors"]
    if errors_.has_errors():
        signup_blog(user_name_, user_email_, blogname_, blog_title_, errors_)
        return False
    # end if
    public_ = php_int(PHP_POST["blog_public"])
    signup_meta_ = Array({"lang_id": 1, "public": public_})
    #// Handle the language setting for the new site.
    if (not php_empty(lambda : PHP_POST["WPLANG"])):
        languages_ = signup_get_available_languages()
        if php_in_array(PHP_POST["WPLANG"], languages_):
            language_ = wp_unslash(sanitize_text_field(PHP_POST["WPLANG"]))
            if language_:
                signup_meta_["WPLANG"] = language_
            # end if
        # end if
    # end if
    #// This filter is documented in wp-signup.php
    meta_ = apply_filters("add_signup_meta", signup_meta_)
    wpmu_signup_blog(domain_, path_, blog_title_, user_name_, user_email_, meta_)
    confirm_blog_signup(domain_, path_, blog_title_, user_name_, user_email_, meta_)
    return True
# end def validate_blog_signup
#// 
#// New site signup confirmation
#// 
#// @since MU (3.0.0)
#// 
#// @param string $domain The domain URL
#// @param string $path The site root path
#// @param string $blog_title The new site title
#// @param string $user_name The user's username
#// @param string $user_email The user's email address
#// @param array $meta Any additional meta from the {@see 'add_signup_meta'} filter in validate_blog_signup()
#//
def confirm_blog_signup(domain_=None, path_=None, blog_title_=None, user_name_="", user_email_="", meta_=None, *_args_):
    if meta_ is None:
        meta_ = Array()
    # end if
    
    php_print(" <h2>\n  ")
    #// translators: %s: Site address.
    printf(__("Congratulations! Your new site, %s, is almost ready."), str("<a href='http://") + str(domain_) + str(path_) + str("'>") + str(blog_title_) + str("</a>"))
    php_print(" </h2>\n\n   <p>")
    _e("But, before you can start using your site, <strong>you must activate it</strong>.")
    php_print("</p>\n   <p>\n   ")
    #// translators: %s: Email address.
    printf(__("Check your inbox at %s and click the link given."), "<strong>" + user_email_ + "</strong>")
    php_print(" </p>\n  <p>")
    _e("If you do not activate your site within two days, you will have to sign up again.")
    php_print("</p>\n   <h2>")
    _e("Still waiting for your email?")
    php_print("</h2>\n  <p>\n       ")
    _e("If you haven&#8217;t received your email yet, there are a number of things you can do:")
    php_print("     <ul id=\"noemail-tips\">\n          <li><p><strong>")
    _e("Wait a little longer. Sometimes delivery of email can be delayed by processes outside of our control.")
    php_print("</strong></p></li>\n         <li><p>")
    _e("Check the junk or spam folder of your email client. Sometime emails wind up there by mistake.")
    php_print("</p></li>\n          <li>\n          ")
    #// translators: %s: Email address.
    printf(__("Have you entered your email correctly? You have entered %s, if it&#8217;s incorrect, you will not receive your email."), user_email_)
    php_print("""           </li>
    </ul>
    </p>
    """)
    #// This action is documented in wp-signup.php
    do_action("signup_finished")
# end def confirm_blog_signup
#// 
#// Retrieves languages available during the site/user signup process.
#// 
#// @since 4.4.0
#// 
#// @see get_available_languages()
#// 
#// @return array List of available languages.
#//
def signup_get_available_languages(*_args_):
    
    
    #// 
    #// Filters the list of available languages for front-end site signups.
    #// 
    #// Passing an empty array to this hook will disable output of the setting on the
    #// signup form, and the default language will be used when creating the site.
    #// 
    #// Languages not already installed will be stripped.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $available_languages Available languages.
    #//
    languages_ = apply_filters("signup_get_available_languages", get_available_languages())
    #// 
    #// Strip any non-installed languages and return.
    #// 
    #// Re-call get_available_languages() here in case a language pack was installed
    #// in a callback hooked to the 'signup_get_available_languages' filter before this point.
    #//
    return php_array_intersect_assoc(languages_, get_available_languages())
# end def signup_get_available_languages
#// Main.
active_signup_ = get_site_option("registration", "none")
#// 
#// Filters the type of site sign-up.
#// 
#// @since 3.0.0
#// 
#// @param string $active_signup String that returns registration type. The value can be
#// 'all', 'none', 'blog', or 'user'.
#//
active_signup_ = apply_filters("wpmu_active_signup", active_signup_)
if current_user_can("manage_network"):
    php_print("<div class=\"mu_alert\">")
    _e("Greetings Network Administrator!")
    php_print(" ")
    for case in Switch(active_signup_):
        if case("none"):
            _e("The network currently disallows registrations.")
            break
        # end if
        if case("blog"):
            _e("The network currently allows site registrations.")
            break
        # end if
        if case("user"):
            _e("The network currently allows user registrations.")
            break
        # end if
        if case():
            _e("The network currently allows both site and user registrations.")
            break
        # end if
    # end for
    php_print(" ")
    #// translators: %s: URL to Network Settings screen.
    printf(__("To change or disable registration go to your <a href=\"%s\">Options page</a>."), esc_url(network_admin_url("settings.php")))
    php_print("</div>")
# end if
newblogname_ = php_strtolower(php_preg_replace("/^-|-$|[^-a-zA-Z0-9]/", "", PHP_REQUEST["new"])) if (php_isset(lambda : PHP_REQUEST["new"])) else None
current_user_ = wp_get_current_user()
if "none" == active_signup_:
    _e("Registration has been disabled.")
elif "blog" == active_signup_ and (not is_user_logged_in()):
    login_url_ = wp_login_url(network_site_url("wp-signup.php"))
    #// translators: %s: Login URL.
    printf(__("You must first <a href=\"%s\">log in</a>, and then you can create a new site."), login_url_)
else:
    stage_ = PHP_POST["stage"] if (php_isset(lambda : PHP_POST["stage"])) else "default"
    for case in Switch(stage_):
        if case("validate-user-signup"):
            if "all" == active_signup_ or "blog" == PHP_POST["signup_for"] and "blog" == active_signup_ or "user" == PHP_POST["signup_for"] and "user" == active_signup_:
                validate_user_signup()
            else:
                _e("User registration has been disabled.")
            # end if
            break
        # end if
        if case("validate-blog-signup"):
            if "all" == active_signup_ or "blog" == active_signup_:
                validate_blog_signup()
            else:
                _e("Site registration has been disabled.")
            # end if
            break
        # end if
        if case("gimmeanotherblog"):
            validate_another_blog_signup()
            break
        # end if
        if case("default"):
            pass
        # end if
        if case():
            user_email_ = PHP_POST["user_email"] if (php_isset(lambda : PHP_POST["user_email"])) else ""
            #// 
            #// Fires when the site sign-up form is sent.
            #// 
            #// @since 3.0.0
            #//
            do_action("preprocess_signup_form")
            if is_user_logged_in() and "all" == active_signup_ or "blog" == active_signup_:
                signup_another_blog(newblogname_)
            elif (not is_user_logged_in()) and "all" == active_signup_ or "user" == active_signup_:
                signup_user(newblogname_, user_email_)
            elif (not is_user_logged_in()) and "blog" == active_signup_:
                _e("Sorry, new registrations are not allowed at this time.")
            else:
                _e("You are logged in already. No need to register again!")
            # end if
            if newblogname_:
                newblog_ = get_blogaddress_by_name(newblogname_)
                if "blog" == active_signup_ or "all" == active_signup_:
                    printf("<p><em>" + __("The site you were looking for, %s, does not exist, but you can create it now!") + "</em></p>", "<strong>" + newblog_ + "</strong>")
                else:
                    printf("<p><em>" + __("The site you were looking for, %s, does not exist.") + "</em></p>", "<strong>" + newblog_ + "</strong>")
                # end if
            # end if
            break
        # end if
    # end for
# end if
php_print("</div>\n</div>\n")
#// 
#// Fires after the sign-up forms, before wp_footer.
#// 
#// @since 3.0.0
#//
do_action("after_signup_form")
php_print("\n")
get_footer("wp-signup")
