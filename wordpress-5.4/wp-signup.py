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
def do_signup_header(*args_):
    
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
wp_query.is_404 = False
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
def wpmu_signup_stylesheet(*args_):
    
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
def show_blog_form(blogname="", blog_title="", errors="", *args_):
    
    if (not is_wp_error(errors)):
        errors = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    current_network = get_network()
    #// Blog name.
    if (not is_subdomain_install()):
        php_print("<label for=\"blogname\">" + __("Site Name:") + "</label>")
    else:
        php_print("<label for=\"blogname\">" + __("Site Domain:") + "</label>")
    # end if
    errmsg = errors.get_error_message("blogname")
    if errmsg:
        php_print("     <p class=\"error\">")
        php_print(errmsg)
        php_print("</p>\n       ")
    # end if
    if (not is_subdomain_install()):
        php_print("<span class=\"prefix_address\">" + current_network.domain + current_network.path + "</span><input name=\"blogname\" type=\"text\" id=\"blogname\" value=\"" + esc_attr(blogname) + "\" maxlength=\"60\" /><br />")
    else:
        site_domain = php_preg_replace("|^www\\.|", "", current_network.domain)
        php_print("<input name=\"blogname\" type=\"text\" id=\"blogname\" value=\"" + esc_attr(blogname) + "\" maxlength=\"60\" /><span class=\"suffix_address\">." + esc_html(site_domain) + "</span><br />")
    # end if
    if (not is_user_logged_in()):
        if (not is_subdomain_install()):
            site = current_network.domain + current_network.path + __("sitename")
        else:
            site = __("domain") + "." + site_domain + current_network.path
        # end if
        printf("<p>(<strong>%s</strong>) %s</p>", php_sprintf(__("Your address will be %s."), site), __("Must be at least 4 characters, letters and numbers only. It cannot be changed, so choose carefully!"))
    # end if
    pass
    php_print(" <label for=\"blog_title\">")
    _e("Site Title:")
    php_print("</label>\n   ")
    errmsg = errors.get_error_message("blog_title")
    if errmsg:
        php_print("     <p class=\"error\">")
        php_print(errmsg)
        php_print("</p>\n       ")
    # end if
    php_print("<input name=\"blog_title\" type=\"text\" id=\"blog_title\" value=\"" + esc_attr(blog_title) + "\" />")
    php_print("\n   ")
    #// Site Language.
    languages = signup_get_available_languages()
    if (not php_empty(lambda : languages)):
        php_print("     <p>\n           <label for=\"site-language\">")
        _e("Site Language:")
        php_print("</label>\n           ")
        #// Network default.
        lang = get_site_option("WPLANG")
        if (php_isset(lambda : PHP_POST["WPLANG"])):
            lang = PHP_POST["WPLANG"]
        # end if
        #// Use US English if the default isn't available.
        if (not php_in_array(lang, languages)):
            lang = ""
        # end if
        wp_dropdown_languages(Array({"name": "WPLANG", "id": "site-language", "selected": lang, "languages": languages, "show_available_translations": False}))
        php_print("     </p>\n      ")
    # end if
    #// Languages.
    blog_public_on_checked = ""
    blog_public_off_checked = ""
    if (php_isset(lambda : PHP_POST["blog_public"])) and "0" == PHP_POST["blog_public"]:
        blog_public_off_checked = "checked=\"checked\""
    else:
        blog_public_on_checked = "checked=\"checked\""
    # end if
    php_print("""
    <div id=\"privacy\">
    <p class=\"privacy-intro\">
    """)
    _e("Privacy:")
    php_print("         ")
    _e("Allow search engines to index this site.")
    php_print("         <br style=\"clear:both\" />\n           <label class=\"checkbox\" for=\"blog_public_on\">\n             <input type=\"radio\" id=\"blog_public_on\" name=\"blog_public\" value=\"1\" ")
    php_print(blog_public_on_checked)
    php_print(" />\n                <strong>")
    _e("Yes")
    php_print("""</strong>
    </label>
    <label class=\"checkbox\" for=\"blog_public_off\">
    <input type=\"radio\" id=\"blog_public_off\" name=\"blog_public\" value=\"0\" """)
    php_print(blog_public_off_checked)
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
    do_action("signup_blogform", errors)
# end def show_blog_form
#// 
#// Validate the new site signup
#// 
#// @since MU (3.0.0)
#// 
#// @return array Contains the new site data and error messages.
#//
def validate_blog_form(*args_):
    
    user = ""
    if is_user_logged_in():
        user = wp_get_current_user()
    # end if
    return wpmu_validate_blog_signup(PHP_POST["blogname"], PHP_POST["blog_title"], user)
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
def show_user_form(user_name="", user_email="", errors="", *args_):
    
    if (not is_wp_error(errors)):
        errors = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    #// Username.
    php_print("<label for=\"user_name\">" + __("Username:") + "</label>")
    errmsg = errors.get_error_message("user_name")
    if errmsg:
        php_print("<p class=\"error\">" + errmsg + "</p>")
    # end if
    php_print("<input name=\"user_name\" type=\"text\" id=\"user_name\" value=\"" + esc_attr(user_name) + "\" autocapitalize=\"none\" autocorrect=\"off\" maxlength=\"60\" /><br />")
    _e("(Must be at least 4 characters, letters and numbers only.)")
    php_print("\n   <label for=\"user_email\">")
    _e("Email&nbsp;Address:")
    php_print("</label>\n   ")
    errmsg = errors.get_error_message("user_email")
    if errmsg:
        php_print("     <p class=\"error\">")
        php_print(errmsg)
        php_print("</p>\n   ")
    # end if
    php_print(" <input name=\"user_email\" type=\"email\" id=\"user_email\" value=\"")
    php_print(esc_attr(user_email))
    php_print("\" maxlength=\"200\" /><br />")
    _e("We send your registration email to this address. (Double-check your email address before continuing.)")
    php_print(" ")
    errmsg = errors.get_error_message("generic")
    if errmsg:
        php_print("<p class=\"error\">" + errmsg + "</p>")
    # end if
    #// 
    #// Fires at the end of the user registration form on the site sign-up form.
    #// 
    #// @since 3.0.0
    #// 
    #// @param WP_Error $errors A WP_Error object containing 'user_name' or 'user_email' errors.
    #//
    do_action("signup_extra_fields", errors)
# end def show_user_form
#// 
#// Validate user signup name and email
#// 
#// @since MU (3.0.0)
#// 
#// @return array Contains username, email, and error messages.
#//
def validate_user_form(*args_):
    
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
def signup_another_blog(blogname="", blog_title="", errors="", *args_):
    
    current_user = wp_get_current_user()
    if (not is_wp_error(errors)):
        errors = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    signup_defaults = Array({"blogname": blogname, "blog_title": blog_title, "errors": errors})
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
    filtered_results = apply_filters("signup_another_blog_init", signup_defaults)
    blogname = filtered_results["blogname"]
    blog_title = filtered_results["blog_title"]
    errors = filtered_results["errors"]
    #// translators: %s: Network title.
    php_print("<h2>" + php_sprintf(__("Get <em>another</em> %s site in seconds"), get_network().site_name) + "</h2>")
    if errors.has_errors():
        php_print("<p>" + __("There was a problem, please correct the form below and try again.") + "</p>")
    # end if
    php_print(" <p>\n       ")
    printf(__("Welcome back, %s. By filling out the form below, you can <strong>add another site to your account</strong>. There is no limit to the number of sites you can have, so create to your heart&#8217;s content, but write responsibly!"), current_user.display_name)
    php_print(" </p>\n\n    ")
    blogs = get_blogs_of_user(current_user.ID)
    if (not php_empty(lambda : blogs)):
        php_print("\n           <p>")
        _e("Sites you are already a member of:")
        php_print("</p>\n           <ul>\n              ")
        for blog in blogs:
            home_url = get_home_url(blog.userblog_id)
            php_print("<li><a href=\"" + esc_url(home_url) + "\">" + home_url + "</a></li>")
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
    show_blog_form(blogname, blog_title, errors)
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
def validate_another_blog_signup(*args_):
    
    global blogname,blog_title,errors,domain,path
    php_check_if_defined("blogname","blog_title","errors","domain","path")
    current_user = wp_get_current_user()
    if (not is_user_logged_in()):
        php_exit(0)
    # end if
    result = validate_blog_form()
    #// Extracted values set/overwrite globals.
    domain = result["domain"]
    path = result["path"]
    blogname = result["blogname"]
    blog_title = result["blog_title"]
    errors = result["errors"]
    if errors.has_errors():
        signup_another_blog(blogname, blog_title, errors)
        return False
    # end if
    public = int(PHP_POST["blog_public"])
    blog_meta_defaults = Array({"lang_id": 1, "public": public})
    #// Handle the language setting for the new site.
    if (not php_empty(lambda : PHP_POST["WPLANG"])):
        languages = signup_get_available_languages()
        if php_in_array(PHP_POST["WPLANG"], languages):
            language = wp_unslash(sanitize_text_field(PHP_POST["WPLANG"]))
            if language:
                blog_meta_defaults["WPLANG"] = language
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
    meta_defaults = apply_filters_deprecated("signup_create_blog_meta", Array(blog_meta_defaults), "3.0.0", "add_signup_meta")
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
    meta = apply_filters("add_signup_meta", meta_defaults)
    blog_id = wpmu_create_blog(domain, path, blog_title, current_user.ID, meta, get_current_network_id())
    if is_wp_error(blog_id):
        return False
    # end if
    confirm_another_blog_signup(domain, path, blog_title, current_user.user_login, current_user.user_email, meta, blog_id)
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
def confirm_another_blog_signup(domain=None, path=None, blog_title=None, user_name=None, user_email="", meta=Array(), blog_id=0, *args_):
    
    if blog_id:
        switch_to_blog(blog_id)
        home_url = home_url("/")
        login_url = wp_login_url()
        restore_current_blog()
    else:
        home_url = "http://" + domain + path
        login_url = "http://" + domain + path + "wp-login.php"
    # end if
    site = php_sprintf("<a href=\"%1$s\">%2$s</a>", esc_url(home_url), blog_title)
    php_print(" <h2>\n  ")
    #// translators: %s: Site title.
    printf(__("The site %s is yours."), site)
    php_print(" </h2>\n <p>\n       ")
    printf(__("%1$s is your new site. <a href=\"%2$s\">Log in</a> as &#8220;%3$s&#8221; using your existing password."), php_sprintf("<a href=\"%s\">%s</a>", esc_url(home_url), untrailingslashit(domain + path)), esc_url(login_url), user_name)
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
def signup_user(user_name="", user_email="", errors="", *args_):
    
    global active_signup
    php_check_if_defined("active_signup")
    if (not is_wp_error(errors)):
        errors = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    signup_for = esc_html(PHP_POST["signup_for"]) if (php_isset(lambda : PHP_POST["signup_for"])) else "blog"
    signup_user_defaults = Array({"user_name": user_name, "user_email": user_email, "errors": errors})
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
    filtered_results = apply_filters("signup_user_init", signup_user_defaults)
    user_name = filtered_results["user_name"]
    user_email = filtered_results["user_email"]
    errors = filtered_results["errors"]
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
    show_user_form(user_name, user_email, errors)
    php_print("\n       <p>\n       ")
    if "blog" == active_signup:
        php_print("         <input id=\"signupblog\" type=\"hidden\" name=\"signup_for\" value=\"blog\" />\n        ")
    elif "user" == active_signup:
        php_print("         <input id=\"signupblog\" type=\"hidden\" name=\"signup_for\" value=\"user\" />\n        ")
    else:
        php_print("         <input id=\"signupblog\" type=\"radio\" name=\"signup_for\" value=\"blog\" ")
        checked(signup_for, "blog")
        php_print(" />\n            <label class=\"checkbox\" for=\"signupblog\">")
        _e("Gimme a site!")
        php_print("</label>\n           <br />\n            <input id=\"signupuser\" type=\"radio\" name=\"signup_for\" value=\"user\" ")
        checked(signup_for, "user")
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
def validate_user_signup(*args_):
    
    result = validate_user_form()
    user_name = result["user_name"]
    user_email = result["user_email"]
    errors = result["errors"]
    if errors.has_errors():
        signup_user(user_name, user_email, errors)
        return False
    # end if
    if "blog" == PHP_POST["signup_for"]:
        signup_blog(user_name, user_email)
        return False
    # end if
    #// This filter is documented in wp-signup.php
    wpmu_signup_user(user_name, user_email, apply_filters("add_signup_meta", Array()))
    confirm_user_signup(user_name, user_email)
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
def confirm_user_signup(user_name=None, user_email=None, *args_):
    
    php_print(" <h2>\n  ")
    #// translators: %s: Username.
    printf(__("%s is your new username"), user_name)
    php_print(" </h2>\n <p>")
    _e("But, before you can start using your new username, <strong>you must activate it</strong>.")
    php_print("</p>\n   <p>\n   ")
    #// translators: %s: Email address.
    printf(__("Check your inbox at %s and click the link given."), "<strong>" + user_email + "</strong>")
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
def signup_blog(user_name="", user_email="", blogname="", blog_title="", errors="", *args_):
    
    if (not is_wp_error(errors)):
        errors = php_new_class("WP_Error", lambda : WP_Error())
    # end if
    signup_blog_defaults = Array({"user_name": user_name, "user_email": user_email, "blogname": blogname, "blog_title": blog_title, "errors": errors})
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
    filtered_results = apply_filters("signup_blog_init", signup_blog_defaults)
    user_name = filtered_results["user_name"]
    user_email = filtered_results["user_email"]
    blogname = filtered_results["blogname"]
    blog_title = filtered_results["blog_title"]
    errors = filtered_results["errors"]
    if php_empty(lambda : blogname):
        blogname = user_name
    # end if
    php_print(" <form id=\"setupform\" method=\"post\" action=\"wp-signup.php\">\n      <input type=\"hidden\" name=\"stage\" value=\"validate-blog-signup\" />\n       <input type=\"hidden\" name=\"user_name\" value=\"")
    php_print(esc_attr(user_name))
    php_print("\" />\n      <input type=\"hidden\" name=\"user_email\" value=\"")
    php_print(esc_attr(user_email))
    php_print("\" />\n      ")
    #// This action is documented in wp-signup.php
    do_action("signup_hidden_fields", "validate-site")
    php_print("     ")
    show_blog_form(blogname, blog_title, errors)
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
def validate_blog_signup(*args_):
    
    #// Re-validate user info.
    user_result = wpmu_validate_user_signup(PHP_POST["user_name"], PHP_POST["user_email"])
    user_name = user_result["user_name"]
    user_email = user_result["user_email"]
    user_errors = user_result["errors"]
    if user_errors.has_errors():
        signup_user(user_name, user_email, user_errors)
        return False
    # end if
    result = wpmu_validate_blog_signup(PHP_POST["blogname"], PHP_POST["blog_title"])
    domain = result["domain"]
    path = result["path"]
    blogname = result["blogname"]
    blog_title = result["blog_title"]
    errors = result["errors"]
    if errors.has_errors():
        signup_blog(user_name, user_email, blogname, blog_title, errors)
        return False
    # end if
    public = int(PHP_POST["blog_public"])
    signup_meta = Array({"lang_id": 1, "public": public})
    #// Handle the language setting for the new site.
    if (not php_empty(lambda : PHP_POST["WPLANG"])):
        languages = signup_get_available_languages()
        if php_in_array(PHP_POST["WPLANG"], languages):
            language = wp_unslash(sanitize_text_field(PHP_POST["WPLANG"]))
            if language:
                signup_meta["WPLANG"] = language
            # end if
        # end if
    # end if
    #// This filter is documented in wp-signup.php
    meta = apply_filters("add_signup_meta", signup_meta)
    wpmu_signup_blog(domain, path, blog_title, user_name, user_email, meta)
    confirm_blog_signup(domain, path, blog_title, user_name, user_email, meta)
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
def confirm_blog_signup(domain=None, path=None, blog_title=None, user_name="", user_email="", meta=Array(), *args_):
    
    php_print(" <h2>\n  ")
    #// translators: %s: Site address.
    printf(__("Congratulations! Your new site, %s, is almost ready."), str("<a href='http://") + str(domain) + str(path) + str("'>") + str(blog_title) + str("</a>"))
    php_print(" </h2>\n\n   <p>")
    _e("But, before you can start using your site, <strong>you must activate it</strong>.")
    php_print("</p>\n   <p>\n   ")
    #// translators: %s: Email address.
    printf(__("Check your inbox at %s and click the link given."), "<strong>" + user_email + "</strong>")
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
    printf(__("Have you entered your email correctly? You have entered %s, if it&#8217;s incorrect, you will not receive your email."), user_email)
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
def signup_get_available_languages(*args_):
    
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
    languages = apply_filters("signup_get_available_languages", get_available_languages())
    #// 
    #// Strip any non-installed languages and return.
    #// 
    #// Re-call get_available_languages() here in case a language pack was installed
    #// in a callback hooked to the 'signup_get_available_languages' filter before this point.
    #//
    return php_array_intersect_assoc(languages, get_available_languages())
# end def signup_get_available_languages
#// Main.
active_signup = get_site_option("registration", "none")
#// 
#// Filters the type of site sign-up.
#// 
#// @since 3.0.0
#// 
#// @param string $active_signup String that returns registration type. The value can be
#// 'all', 'none', 'blog', or 'user'.
#//
active_signup = apply_filters("wpmu_active_signup", active_signup)
if current_user_can("manage_network"):
    php_print("<div class=\"mu_alert\">")
    _e("Greetings Network Administrator!")
    php_print(" ")
    for case in Switch(active_signup):
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
newblogname = php_strtolower(php_preg_replace("/^-|-$|[^-a-zA-Z0-9]/", "", PHP_REQUEST["new"])) if (php_isset(lambda : PHP_REQUEST["new"])) else None
current_user = wp_get_current_user()
if "none" == active_signup:
    _e("Registration has been disabled.")
elif "blog" == active_signup and (not is_user_logged_in()):
    login_url = wp_login_url(network_site_url("wp-signup.php"))
    #// translators: %s: Login URL.
    printf(__("You must first <a href=\"%s\">log in</a>, and then you can create a new site."), login_url)
else:
    stage = PHP_POST["stage"] if (php_isset(lambda : PHP_POST["stage"])) else "default"
    for case in Switch(stage):
        if case("validate-user-signup"):
            if "all" == active_signup or "blog" == PHP_POST["signup_for"] and "blog" == active_signup or "user" == PHP_POST["signup_for"] and "user" == active_signup:
                validate_user_signup()
            else:
                _e("User registration has been disabled.")
            # end if
            break
        # end if
        if case("validate-blog-signup"):
            if "all" == active_signup or "blog" == active_signup:
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
            user_email = PHP_POST["user_email"] if (php_isset(lambda : PHP_POST["user_email"])) else ""
            #// 
            #// Fires when the site sign-up form is sent.
            #// 
            #// @since 3.0.0
            #//
            do_action("preprocess_signup_form")
            if is_user_logged_in() and "all" == active_signup or "blog" == active_signup:
                signup_another_blog(newblogname)
            elif (not is_user_logged_in()) and "all" == active_signup or "user" == active_signup:
                signup_user(newblogname, user_email)
            elif (not is_user_logged_in()) and "blog" == active_signup:
                _e("Sorry, new registrations are not allowed at this time.")
            else:
                _e("You are logged in already. No need to register again!")
            # end if
            if newblogname:
                newblog = get_blogaddress_by_name(newblogname)
                if "blog" == active_signup or "all" == active_signup:
                    printf("<p><em>" + __("The site you were looking for, %s, does not exist, but you can create it now!") + "</em></p>", "<strong>" + newblog + "</strong>")
                else:
                    printf("<p><em>" + __("The site you were looking for, %s, does not exist.") + "</em></p>", "<strong>" + newblog + "</strong>")
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
