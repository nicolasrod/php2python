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
#// General template tags that can go anywhere in a template.
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// Load header template.
#// 
#// Includes the header template for a theme or if a name is specified then a
#// specialised header will be included.
#// 
#// For the parameter, if the file is called "header-special.php" then specify
#// "special".
#// 
#// @since 1.5.0
#// 
#// @param string $name The name of the specialised header.
#//
def get_header(name_=None, *_args_):
    
    
    #// 
    #// Fires before the header template file is loaded.
    #// 
    #// @since 2.1.0
    #// @since 2.8.0 $name parameter added.
    #// 
    #// @param string|null $name Name of the specific header file to use. null for the default header.
    #//
    do_action("get_header", name_)
    templates_ = Array()
    name_ = php_str(name_)
    if "" != name_:
        templates_[-1] = str("header-") + str(name_) + str(".php")
    # end if
    templates_[-1] = "header.php"
    locate_template(templates_, True)
# end def get_header
#// 
#// Load footer template.
#// 
#// Includes the footer template for a theme or if a name is specified then a
#// specialised footer will be included.
#// 
#// For the parameter, if the file is called "footer-special.php" then specify
#// "special".
#// 
#// @since 1.5.0
#// 
#// @param string $name The name of the specialised footer.
#//
def get_footer(name_=None, *_args_):
    
    
    #// 
    #// Fires before the footer template file is loaded.
    #// 
    #// @since 2.1.0
    #// @since 2.8.0 $name parameter added.
    #// 
    #// @param string|null $name Name of the specific footer file to use. null for the default footer.
    #//
    do_action("get_footer", name_)
    templates_ = Array()
    name_ = php_str(name_)
    if "" != name_:
        templates_[-1] = str("footer-") + str(name_) + str(".php")
    # end if
    templates_[-1] = "footer.php"
    locate_template(templates_, True)
# end def get_footer
#// 
#// Load sidebar template.
#// 
#// Includes the sidebar template for a theme or if a name is specified then a
#// specialised sidebar will be included.
#// 
#// For the parameter, if the file is called "sidebar-special.php" then specify
#// "special".
#// 
#// @since 1.5.0
#// 
#// @param string $name The name of the specialised sidebar.
#//
def get_sidebar(name_=None, *_args_):
    
    
    #// 
    #// Fires before the sidebar template file is loaded.
    #// 
    #// @since 2.2.0
    #// @since 2.8.0 $name parameter added.
    #// 
    #// @param string|null $name Name of the specific sidebar file to use. null for the default sidebar.
    #//
    do_action("get_sidebar", name_)
    templates_ = Array()
    name_ = php_str(name_)
    if "" != name_:
        templates_[-1] = str("sidebar-") + str(name_) + str(".php")
    # end if
    templates_[-1] = "sidebar.php"
    locate_template(templates_, True)
# end def get_sidebar
#// 
#// Loads a template part into a template.
#// 
#// Provides a simple mechanism for child themes to overload reusable sections of code
#// in the theme.
#// 
#// Includes the named template part for a theme or if a name is specified then a
#// specialised part will be included. If the theme contains no {slug}.php file
#// then no template will be included.
#// 
#// The template is included using require, not require_once, so you may include the
#// same template part multiple times.
#// 
#// For the $name parameter, if the file is called "{slug}-special.php" then specify
#// "special".
#// 
#// @since 3.0.0
#// 
#// @param string $slug The slug name for the generic template.
#// @param string $name The name of the specialised template.
#//
def get_template_part(slug_=None, name_=None, *_args_):
    
    
    #// 
    #// Fires before the specified template part file is loaded.
    #// 
    #// The dynamic portion of the hook name, `$slug`, refers to the slug name
    #// for the generic template part.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string      $slug The slug name for the generic template.
    #// @param string|null $name The name of the specialized template.
    #//
    do_action(str("get_template_part_") + str(slug_), slug_, name_)
    templates_ = Array()
    name_ = php_str(name_)
    if "" != name_:
        templates_[-1] = str(slug_) + str("-") + str(name_) + str(".php")
    # end if
    templates_[-1] = str(slug_) + str(".php")
    #// 
    #// Fires before a template part is loaded.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string   $slug      The slug name for the generic template.
    #// @param string   $name      The name of the specialized template.
    #// @param string[] $templates Array of template files to search for, in order.
    #//
    do_action("get_template_part", slug_, name_, templates_)
    locate_template(templates_, True, False)
# end def get_template_part
#// 
#// Display search form.
#// 
#// Will first attempt to locate the searchform.php file in either the child or
#// the parent, then load it. If it doesn't exist, then the default search form
#// will be displayed. The default search form is HTML, which will be displayed.
#// There is a filter applied to the search form HTML in order to edit or replace
#// it. The filter is {@see 'get_search_form'}.
#// 
#// This function is primarily used by themes which want to hardcode the search
#// form into the sidebar and also by the search widget in WordPress.
#// 
#// There is also an action that is called whenever the function is run called,
#// {@see 'pre_get_search_form'}. This can be useful for outputting JavaScript that the
#// search relies on or various formatting that applies to the beginning of the
#// search. To give a few examples of what it can be used for.
#// 
#// @since 2.7.0
#// @since 5.2.0 The $args array parameter was added in place of an $echo boolean flag.
#// 
#// @param array $args {
#// Optional. Array of display arguments.
#// 
#// @type bool   $echo       Whether to echo or return the form. Default true.
#// @type string $aria_label ARIA label for the search form. Useful to distinguish
#// multiple search forms on the same page and improve
#// accessibility. Default empty.
#// }
#// @return void|string Void if 'echo' argument is true, search form HTML if 'echo' is false.
#//
def get_search_form(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// 
    #// Fires before the search form is retrieved, at the start of get_search_form().
    #// 
    #// @since 2.7.0 as 'get_search_form' action.
    #// @since 3.6.0
    #// 
    #// @link https://core.trac.wordpress.org/ticket/19321
    #//
    do_action("pre_get_search_form")
    echo_ = True
    if (not php_is_array(args_)):
        #// 
        #// Back compat: to ensure previous uses of get_search_form() continue to
        #// function as expected, we handle a value for the boolean $echo param removed
        #// in 5.2.0. Then we deal with the $args array and cast its defaults.
        #//
        echo_ = php_bool(args_)
        #// Set an empty array and allow default arguments to take over.
        args_ = Array()
    # end if
    #// Defaults are to echo and to output no custom label on the form.
    defaults_ = Array({"echo": echo_, "aria_label": ""})
    args_ = wp_parse_args(args_, defaults_)
    #// 
    #// Filters the array of arguments used when generating the search form.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $args The array of arguments for building the search form.
    #//
    args_ = apply_filters("search_form_args", args_)
    format_ = "html5" if current_theme_supports("html5", "search-form") else "xhtml"
    #// 
    #// Filters the HTML format of the search form.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $format The type of markup to use in the search form.
    #// Accepts 'html5', 'xhtml'.
    #//
    format_ = apply_filters("search_form_format", format_)
    search_form_template_ = locate_template("searchform.php")
    if "" != search_form_template_:
        ob_start()
        php_include_file(search_form_template_, once=False)
        form_ = ob_get_clean()
    else:
        #// Build a string containing an aria-label to use for the search form.
        if (php_isset(lambda : args_["aria_label"])) and args_["aria_label"]:
            aria_label_ = "aria-label=\"" + esc_attr(args_["aria_label"]) + "\" "
        else:
            #// 
            #// If there's no custom aria-label, we can set a default here. At the
            #// moment it's empty as there's uncertainty about what the default should be.
            #//
            aria_label_ = ""
        # end if
        if "html5" == format_:
            form_ = "<form role=\"search\" " + aria_label_ + "method=\"get\" class=\"search-form\" action=\"" + esc_url(home_url("/")) + "\">\n             <label>\n                   <span class=\"screen-reader-text\">" + _x("Search for:", "label") + "</span>\n                  <input type=\"search\" class=\"search-field\" placeholder=\"" + esc_attr_x("Search &hellip;", "placeholder") + "\" value=\"" + get_search_query() + "\" name=\"s\" />\n             </label>\n              <input type=\"submit\" class=\"search-submit\" value=\"" + esc_attr_x("Search", "submit button") + "\" />\n         </form>"
        else:
            form_ = "<form role=\"search\" " + aria_label_ + "method=\"get\" id=\"searchform\" class=\"searchform\" action=\"" + esc_url(home_url("/")) + "\">\n                <div>\n                 <label class=\"screen-reader-text\" for=\"s\">" + _x("Search for:", "label") + "</label>\n                  <input type=\"text\" value=\"" + get_search_query() + "\" name=\"s\" id=\"s\" />\n                  <input type=\"submit\" id=\"searchsubmit\" value=\"" + esc_attr_x("Search", "submit button") + "\" />\n             </div>\n            </form>"
        # end if
    # end if
    #// 
    #// Filters the HTML output of the search form.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $form The search form HTML output.
    #//
    result_ = apply_filters("get_search_form", form_)
    if None == result_:
        result_ = form_
    # end if
    if args_["echo"]:
        php_print(result_)
    else:
        return result_
    # end if
# end def get_search_form
#// 
#// Display the Log In/Out link.
#// 
#// Displays a link, which allows users to navigate to the Log In page to log in
#// or log out depending on whether they are currently logged in.
#// 
#// @since 1.5.0
#// 
#// @param string $redirect Optional path to redirect to on login/logout.
#// @param bool   $echo     Default to echo and not return the link.
#// @return void|string Void if `$echo` argument is true, log in/out link if `$echo` is false.
#//
def wp_loginout(redirect_="", echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    if (not is_user_logged_in()):
        link_ = "<a href=\"" + esc_url(wp_login_url(redirect_)) + "\">" + __("Log in") + "</a>"
    else:
        link_ = "<a href=\"" + esc_url(wp_logout_url(redirect_)) + "\">" + __("Log out") + "</a>"
    # end if
    if echo_:
        #// 
        #// Filters the HTML output for the Log In/Log Out link.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string $link The HTML link content.
        #//
        php_print(apply_filters("loginout", link_))
    else:
        #// This filter is documented in wp-includes/general-template.php
        return apply_filters("loginout", link_)
    # end if
# end def wp_loginout
#// 
#// Retrieves the logout URL.
#// 
#// Returns the URL that allows the user to log out of the site.
#// 
#// @since 2.7.0
#// 
#// @param string $redirect Path to redirect to on logout.
#// @return string The logout URL. Note: HTML-encoded via esc_html() in wp_nonce_url().
#//
def wp_logout_url(redirect_="", *_args_):
    
    
    args_ = Array()
    if (not php_empty(lambda : redirect_)):
        args_["redirect_to"] = urlencode(redirect_)
    # end if
    logout_url_ = add_query_arg(args_, site_url("wp-login.php?action=logout", "login"))
    logout_url_ = wp_nonce_url(logout_url_, "log-out")
    #// 
    #// Filters the logout URL.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $logout_url The HTML-encoded logout URL.
    #// @param string $redirect   Path to redirect to on logout.
    #//
    return apply_filters("logout_url", logout_url_, redirect_)
# end def wp_logout_url
#// 
#// Retrieves the login URL.
#// 
#// @since 2.7.0
#// 
#// @param string $redirect     Path to redirect to on log in.
#// @param bool   $force_reauth Whether to force reauthorization, even if a cookie is present.
#// Default false.
#// @return string The login URL. Not HTML-encoded.
#//
def wp_login_url(redirect_="", force_reauth_=None, *_args_):
    if force_reauth_ is None:
        force_reauth_ = False
    # end if
    
    login_url_ = site_url("wp-login.php", "login")
    if (not php_empty(lambda : redirect_)):
        login_url_ = add_query_arg("redirect_to", urlencode(redirect_), login_url_)
    # end if
    if force_reauth_:
        login_url_ = add_query_arg("reauth", "1", login_url_)
    # end if
    #// 
    #// Filters the login URL.
    #// 
    #// @since 2.8.0
    #// @since 4.2.0 The `$force_reauth` parameter was added.
    #// 
    #// @param string $login_url    The login URL. Not HTML-encoded.
    #// @param string $redirect     The path to redirect to on login, if supplied.
    #// @param bool   $force_reauth Whether to force reauthorization, even if a cookie is present.
    #//
    return apply_filters("login_url", login_url_, redirect_, force_reauth_)
# end def wp_login_url
#// 
#// Returns the URL that allows the user to register on the site.
#// 
#// @since 3.6.0
#// 
#// @return string User registration URL.
#//
def wp_registration_url(*_args_):
    
    
    #// 
    #// Filters the user registration URL.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $register The user registration URL.
    #//
    return apply_filters("register_url", site_url("wp-login.php?action=register", "login"))
# end def wp_registration_url
#// 
#// Provides a simple login form for use anywhere within WordPress.
#// 
#// The login form HTML is echoed by default. Pass a false value for `$echo` to return it instead.
#// 
#// @since 3.0.0
#// 
#// @param array $args {
#// Optional. Array of options to control the form output. Default empty array.
#// 
#// @type bool   $echo           Whether to display the login form or return the form HTML code.
#// Default true (echo).
#// @type string $redirect       URL to redirect to. Must be absolute, as in "https://example.com/mypage/".
#// Default is to redirect back to the request URI.
#// @type string $form_id        ID attribute value for the form. Default 'loginform'.
#// @type string $label_username Label for the username or email address field. Default 'Username or Email Address'.
#// @type string $label_password Label for the password field. Default 'Password'.
#// @type string $label_remember Label for the remember field. Default 'Remember Me'.
#// @type string $label_log_in   Label for the submit button. Default 'Log In'.
#// @type string $id_username    ID attribute value for the username field. Default 'user_login'.
#// @type string $id_password    ID attribute value for the password field. Default 'user_pass'.
#// @type string $id_remember    ID attribute value for the remember field. Default 'rememberme'.
#// @type string $id_submit      ID attribute value for the submit button. Default 'wp-submit'.
#// @type bool   $remember       Whether to display the "rememberme" checkbox in the form.
#// @type string $value_username Default value for the username field. Default empty.
#// @type bool   $value_remember Whether the "Remember Me" checkbox should be checked by default.
#// Default false (unchecked).
#// 
#// }
#// @return void|string Void if 'echo' argument is true, login form HTML if 'echo' is false.
#//
def wp_login_form(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"echo": True, "redirect": "https://" if is_ssl() else "http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"], "form_id": "loginform", "label_username": __("Username or Email Address"), "label_password": __("Password"), "label_remember": __("Remember Me"), "label_log_in": __("Log In"), "id_username": "user_login", "id_password": "user_pass", "id_remember": "rememberme", "id_submit": "wp-submit", "remember": True, "value_username": "", "value_remember": False})
    #// 
    #// Filters the default login form output arguments.
    #// 
    #// @since 3.0.0
    #// 
    #// @see wp_login_form()
    #// 
    #// @param array $defaults An array of default login form arguments.
    #//
    args_ = wp_parse_args(args_, apply_filters("login_form_defaults", defaults_))
    #// 
    #// Filters content to display at the top of the login form.
    #// 
    #// The filter evaluates just following the opening form tag element.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $content Content to display. Default empty.
    #// @param array  $args    Array of login form arguments.
    #//
    login_form_top_ = apply_filters("login_form_top", "", args_)
    #// 
    #// Filters content to display in the middle of the login form.
    #// 
    #// The filter evaluates just following the location where the 'login-password'
    #// field is displayed.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $content Content to display. Default empty.
    #// @param array  $args    Array of login form arguments.
    #//
    login_form_middle_ = apply_filters("login_form_middle", "", args_)
    #// 
    #// Filters content to display at the bottom of the login form.
    #// 
    #// The filter evaluates just preceding the closing form tag element.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $content Content to display. Default empty.
    #// @param array  $args    Array of login form arguments.
    #//
    login_form_bottom_ = apply_filters("login_form_bottom", "", args_)
    form_ = "\n     <form name=\"" + args_["form_id"] + "\" id=\"" + args_["form_id"] + "\" action=\"" + esc_url(site_url("wp-login.php", "login_post")) + "\" method=\"post\">\n           " + login_form_top_ + "\n           <p class=\"login-username\">\n              <label for=\"" + esc_attr(args_["id_username"]) + "\">" + esc_html(args_["label_username"]) + "</label>\n               <input type=\"text\" name=\"log\" id=\"" + esc_attr(args_["id_username"]) + "\" class=\"input\" value=\"" + esc_attr(args_["value_username"]) + """\" size=\"20\" />
    </p>
    <p class=\"login-password\">
    <label for=\"""" + esc_attr(args_["id_password"]) + "\">" + esc_html(args_["label_password"]) + "</label>\n             <input type=\"password\" name=\"pwd\" id=\"" + esc_attr(args_["id_password"]) + "\" class=\"input\" value=\"\" size=\"20\" />\n         </p>\n          " + login_form_middle_ + "\n            " + "<p class=\"login-remember\"><label><input name=\"rememberme\" type=\"checkbox\" id=\"" + esc_attr(args_["id_remember"]) + "\" value=\"forever\"" + " checked=\"checked\"" if args_["value_remember"] else "" + " /> " + esc_html(args_["label_remember"]) + "</label></p>" if args_["remember"] else "" + "\n          <p class=\"login-submit\">\n                <input type=\"submit\" name=\"wp-submit\" id=\"" + esc_attr(args_["id_submit"]) + "\" class=\"button button-primary\" value=\"" + esc_attr(args_["label_log_in"]) + "\" />\n                <input type=\"hidden\" name=\"redirect_to\" value=\"" + esc_url(args_["redirect"]) + "\" />\n           </p>\n          " + login_form_bottom_ + "\n        </form>"
    if args_["echo"]:
        php_print(form_)
    else:
        return form_
    # end if
# end def wp_login_form
#// 
#// Returns the URL that allows the user to retrieve the lost password
#// 
#// @since 2.8.0
#// 
#// @param string $redirect Path to redirect to on login.
#// @return string Lost password URL.
#//
def wp_lostpassword_url(redirect_="", *_args_):
    
    
    args_ = Array()
    if (not php_empty(lambda : redirect_)):
        args_["redirect_to"] = urlencode(redirect_)
    # end if
    lostpassword_url_ = add_query_arg(args_, network_site_url("wp-login.php?action=lostpassword", "login"))
    #// 
    #// Filters the Lost Password URL.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $lostpassword_url The lost password page URL.
    #// @param string $redirect         The path to redirect to on login.
    #//
    return apply_filters("lostpassword_url", lostpassword_url_, redirect_)
# end def wp_lostpassword_url
#// 
#// Display the Registration or Admin link.
#// 
#// Display a link which allows the user to navigate to the registration page if
#// not logged in and registration is enabled or to the dashboard if logged in.
#// 
#// @since 1.5.0
#// 
#// @param string $before Text to output before the link. Default `<li>`.
#// @param string $after  Text to output after the link. Default `</li>`.
#// @param bool   $echo   Default to echo and not return the link.
#// @return void|string Void if `$echo` argument is true, registration or admin link
#// if `$echo` is false.
#//
def wp_register(before_="<li>", after_="</li>", echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    if (not is_user_logged_in()):
        if get_option("users_can_register"):
            link_ = before_ + "<a href=\"" + esc_url(wp_registration_url()) + "\">" + __("Register") + "</a>" + after_
        else:
            link_ = ""
        # end if
    elif current_user_can("read"):
        link_ = before_ + "<a href=\"" + admin_url() + "\">" + __("Site Admin") + "</a>" + after_
    else:
        link_ = ""
    # end if
    #// 
    #// Filters the HTML link to the Registration or Admin page.
    #// 
    #// Users are sent to the admin page if logged-in, or the registration page
    #// if enabled and logged-out.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $link The HTML code for the link to the Registration or Admin page.
    #//
    link_ = apply_filters("register", link_)
    if echo_:
        php_print(link_)
    else:
        return link_
    # end if
# end def wp_register
#// 
#// Theme container function for the 'wp_meta' action.
#// 
#// The {@see 'wp_meta'} action can have several purposes, depending on how you use it,
#// but one purpose might have been to allow for theme switching.
#// 
#// @since 1.5.0
#// 
#// @link https://core.trac.wordpress.org/ticket/1458 Explanation of 'wp_meta' action.
#//
def wp_meta(*_args_):
    
    
    #// 
    #// Fires before displaying echoed content in the sidebar.
    #// 
    #// @since 1.5.0
    #//
    do_action("wp_meta")
# end def wp_meta
#// 
#// Displays information about the current site.
#// 
#// @since 0.71
#// 
#// @see get_bloginfo() For possible `$show` values
#// 
#// @param string $show Optional. Site information to display. Default empty.
#//
def bloginfo(show_="", *_args_):
    
    
    php_print(get_bloginfo(show_, "display"))
# end def bloginfo
#// 
#// Retrieves information about the current site.
#// 
#// Possible values for `$show` include:
#// 
#// - 'name' - Site title (set in Settings > General)
#// - 'description' - Site tagline (set in Settings > General)
#// - 'wpurl' - The WordPress address (URL) (set in Settings > General)
#// - 'url' - The Site address (URL) (set in Settings > General)
#// - 'admin_email' - Admin email (set in Settings > General)
#// - 'charset' - The "Encoding for pages and feeds"  (set in Settings > Reading)
#// - 'version' - The current WordPress version
#// - 'html_type' - The content-type (default: "text/html"). Themes and plugins
#// can override the default value using the {@see 'pre_option_html_type'} filter
#// - 'text_direction' - The text direction determined by the site's language. is_rtl()
#// should be used instead
#// - 'language' - Language code for the current site
#// - 'stylesheet_url' - URL to the stylesheet for the active theme. An active child theme
#// will take precedence over this value
#// - 'stylesheet_directory' - Directory path for the active theme.  An active child theme
#// will take precedence over this value
#// - 'template_url' / 'template_directory' - URL of the active theme's directory. An active
#// child theme will NOT take precedence over this value
#// - 'pingback_url' - The pingback XML-RPC file URL (xmlrpc.php)
#// - 'atom_url' - The Atom feed URL (/feed/atom)
#// - 'rdf_url' - The RDF/RSS 1.0 feed URL (/feed/rdf)
#// - 'rss_url' - The RSS 0.92 feed URL (/feed/rss)
#// - 'rss2_url' - The RSS 2.0 feed URL (/feed)
#// - 'comments_atom_url' - The comments Atom feed URL (/comments/feed)
#// - 'comments_rss2_url' - The comments RSS 2.0 feed URL (/comments/feed)
#// 
#// Some `$show` values are deprecated and will be removed in future versions.
#// These options will trigger the _deprecated_argument() function.
#// 
#// Deprecated arguments include:
#// 
#// - 'siteurl' - Use 'url' instead
#// - 'home' - Use 'url' instead
#// 
#// @since 0.71
#// 
#// @global string $wp_version The WordPress version string.
#// 
#// @param string $show   Optional. Site info to retrieve. Default empty (site name).
#// @param string $filter Optional. How to filter what is retrieved. Default 'raw'.
#// @return string Mostly string values, might be empty.
#//
def get_bloginfo(show_="", filter_="raw", *_args_):
    
    
    for case in Switch(show_):
        if case("home"):
            pass
        # end if
        if case("siteurl"):
            #// Deprecated.
            _deprecated_argument(__FUNCTION__, "2.2.0", php_sprintf(__("The %1$s option is deprecated for the family of %2$s functions. Use the %3$s option instead."), "<code>" + show_ + "</code>", "<code>bloginfo()</code>", "<code>url</code>"))
        # end if
        if case("url"):
            output_ = home_url()
            break
        # end if
        if case("wpurl"):
            output_ = site_url()
            break
        # end if
        if case("description"):
            output_ = get_option("blogdescription")
            break
        # end if
        if case("rdf_url"):
            output_ = get_feed_link("rdf")
            break
        # end if
        if case("rss_url"):
            output_ = get_feed_link("rss")
            break
        # end if
        if case("rss2_url"):
            output_ = get_feed_link("rss2")
            break
        # end if
        if case("atom_url"):
            output_ = get_feed_link("atom")
            break
        # end if
        if case("comments_atom_url"):
            output_ = get_feed_link("comments_atom")
            break
        # end if
        if case("comments_rss2_url"):
            output_ = get_feed_link("comments_rss2")
            break
        # end if
        if case("pingback_url"):
            output_ = site_url("xmlrpc.php")
            break
        # end if
        if case("stylesheet_url"):
            output_ = get_stylesheet_uri()
            break
        # end if
        if case("stylesheet_directory"):
            output_ = get_stylesheet_directory_uri()
            break
        # end if
        if case("template_directory"):
            pass
        # end if
        if case("template_url"):
            output_ = get_template_directory_uri()
            break
        # end if
        if case("admin_email"):
            output_ = get_option("admin_email")
            break
        # end if
        if case("charset"):
            output_ = get_option("blog_charset")
            if "" == output_:
                output_ = "UTF-8"
            # end if
            break
        # end if
        if case("html_type"):
            output_ = get_option("html_type")
            break
        # end if
        if case("version"):
            global wp_version_
            php_check_if_defined("wp_version_")
            output_ = wp_version_
            break
        # end if
        if case("language"):
            #// 
            #// translators: Translate this to the correct language tag for your locale,
            #// see https://www.w3.org/International/articles/language-tags/ for reference.
            #// Do not translate into your own language.
            #//
            output_ = __("html_lang_attribute")
            if "html_lang_attribute" == output_ or php_preg_match("/[^a-zA-Z0-9-]/", output_):
                output_ = determine_locale()
                output_ = php_str_replace("_", "-", output_)
            # end if
            break
        # end if
        if case("text_direction"):
            _deprecated_argument(__FUNCTION__, "2.2.0", php_sprintf(__("The %1$s option is deprecated for the family of %2$s functions. Use the %3$s function instead."), "<code>" + show_ + "</code>", "<code>bloginfo()</code>", "<code>is_rtl()</code>"))
            if php_function_exists("is_rtl"):
                output_ = "rtl" if is_rtl() else "ltr"
            else:
                output_ = "ltr"
            # end if
            break
        # end if
        if case("name"):
            pass
        # end if
        if case():
            output_ = get_option("blogname")
            break
        # end if
    # end for
    url_ = True
    if php_strpos(show_, "url") == False and php_strpos(show_, "directory") == False and php_strpos(show_, "home") == False:
        url_ = False
    # end if
    if "display" == filter_:
        if url_:
            #// 
            #// Filters the URL returned by get_bloginfo().
            #// 
            #// @since 2.0.5
            #// 
            #// @param string $output The URL returned by bloginfo().
            #// @param string $show   Type of information requested.
            #//
            output_ = apply_filters("bloginfo_url", output_, show_)
        else:
            #// 
            #// Filters the site information returned by get_bloginfo().
            #// 
            #// @since 0.71
            #// 
            #// @param mixed  $output The requested non-URL site information.
            #// @param string $show   Type of information requested.
            #//
            output_ = apply_filters("bloginfo", output_, show_)
        # end if
    # end if
    return output_
# end def get_bloginfo
#// 
#// Returns the Site Icon URL.
#// 
#// @since 4.3.0
#// 
#// @param int    $size    Optional. Size of the site icon. Default 512 (pixels).
#// @param string $url     Optional. Fallback url if no site icon is found. Default empty.
#// @param int    $blog_id Optional. ID of the blog to get the site icon for. Default current blog.
#// @return string Site Icon URL.
#//
def get_site_icon_url(size_=512, url_="", blog_id_=0, *_args_):
    
    
    switched_blog_ = False
    if is_multisite() and (not php_empty(lambda : blog_id_)) and get_current_blog_id() != php_int(blog_id_):
        switch_to_blog(blog_id_)
        switched_blog_ = True
    # end if
    site_icon_id_ = get_option("site_icon")
    if site_icon_id_:
        if size_ >= 512:
            size_data_ = "full"
        else:
            size_data_ = Array(size_, size_)
        # end if
        url_ = wp_get_attachment_image_url(site_icon_id_, size_data_)
    # end if
    if switched_blog_:
        restore_current_blog()
    # end if
    #// 
    #// Filters the site icon URL.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $url     Site icon URL.
    #// @param int    $size    Size of the site icon.
    #// @param int    $blog_id ID of the blog to get the site icon for.
    #//
    return apply_filters("get_site_icon_url", url_, size_, blog_id_)
# end def get_site_icon_url
#// 
#// Displays the Site Icon URL.
#// 
#// @since 4.3.0
#// 
#// @param int    $size    Optional. Size of the site icon. Default 512 (pixels).
#// @param string $url     Optional. Fallback url if no site icon is found. Default empty.
#// @param int    $blog_id Optional. ID of the blog to get the site icon for. Default current blog.
#//
def site_icon_url(size_=512, url_="", blog_id_=0, *_args_):
    
    
    php_print(esc_url(get_site_icon_url(size_, url_, blog_id_)))
# end def site_icon_url
#// 
#// Whether the site has a Site Icon.
#// 
#// @since 4.3.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default current blog.
#// @return bool Whether the site has a site icon or not.
#//
def has_site_icon(blog_id_=0, *_args_):
    
    
    return php_bool(get_site_icon_url(512, "", blog_id_))
# end def has_site_icon
#// 
#// Determines whether the site has a custom logo.
#// 
#// @since 4.5.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default is the ID of the current blog.
#// @return bool Whether the site has a custom logo or not.
#//
def has_custom_logo(blog_id_=0, *_args_):
    
    
    switched_blog_ = False
    if is_multisite() and (not php_empty(lambda : blog_id_)) and get_current_blog_id() != php_int(blog_id_):
        switch_to_blog(blog_id_)
        switched_blog_ = True
    # end if
    custom_logo_id_ = get_theme_mod("custom_logo")
    if switched_blog_:
        restore_current_blog()
    # end if
    return php_bool(custom_logo_id_)
# end def has_custom_logo
#// 
#// Returns a custom logo, linked to home.
#// 
#// @since 4.5.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default is the ID of the current blog.
#// @return string Custom logo markup.
#//
def get_custom_logo(blog_id_=0, *_args_):
    
    
    html_ = ""
    switched_blog_ = False
    if is_multisite() and (not php_empty(lambda : blog_id_)) and get_current_blog_id() != php_int(blog_id_):
        switch_to_blog(blog_id_)
        switched_blog_ = True
    # end if
    custom_logo_id_ = get_theme_mod("custom_logo")
    #// We have a logo. Logo is go.
    if custom_logo_id_:
        custom_logo_attr_ = Array({"class": "custom-logo"})
        #// 
        #// If the logo alt attribute is empty, get the site title and explicitly
        #// pass it to the attributes used by wp_get_attachment_image().
        #//
        image_alt_ = get_post_meta(custom_logo_id_, "_wp_attachment_image_alt", True)
        if php_empty(lambda : image_alt_):
            custom_logo_attr_["alt"] = get_bloginfo("name", "display")
        # end if
        #// 
        #// If the alt attribute is not empty, there's no need to explicitly pass
        #// it because wp_get_attachment_image() already adds the alt attribute.
        #//
        html_ = php_sprintf("<a href=\"%1$s\" class=\"custom-logo-link\" rel=\"home\">%2$s</a>", esc_url(home_url("/")), wp_get_attachment_image(custom_logo_id_, "full", False, custom_logo_attr_))
    elif is_customize_preview():
        #// If no logo is set but we're in the Customizer, leave a placeholder (needed for the live preview).
        html_ = php_sprintf("<a href=\"%1$s\" class=\"custom-logo-link\" style=\"display:none;\"><img class=\"custom-logo\"/></a>", esc_url(home_url("/")))
    # end if
    if switched_blog_:
        restore_current_blog()
    # end if
    #// 
    #// Filters the custom logo output.
    #// 
    #// @since 4.5.0
    #// @since 4.6.0 Added the `$blog_id` parameter.
    #// 
    #// @param string $html    Custom logo HTML output.
    #// @param int    $blog_id ID of the blog to get the custom logo for.
    #//
    return apply_filters("get_custom_logo", html_, blog_id_)
# end def get_custom_logo
#// 
#// Displays a custom logo, linked to home.
#// 
#// @since 4.5.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default is the ID of the current blog.
#//
def the_custom_logo(blog_id_=0, *_args_):
    
    
    php_print(get_custom_logo(blog_id_))
# end def the_custom_logo
#// 
#// Returns document title for the current page.
#// 
#// @since 4.4.0
#// 
#// @global int $page  Page number of a single post.
#// @global int $paged Page number of a list of posts.
#// 
#// @return string Tag with the document title.
#//
def wp_get_document_title(*_args_):
    
    
    #// 
    #// Filters the document title before it is generated.
    #// 
    #// Passing a non-empty value will short-circuit wp_get_document_title(),
    #// returning that value instead.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $title The document title. Default empty string.
    #//
    title_ = apply_filters("pre_get_document_title", "")
    if (not php_empty(lambda : title_)):
        return title_
    # end if
    global page_
    global paged_
    php_check_if_defined("page_","paged_")
    title_ = Array({"title": ""})
    #// If it's a 404 page, use a "Page not found" title.
    if is_404():
        title_["title"] = __("Page not found")
        pass
    elif is_search():
        #// translators: %s: Search query.
        title_["title"] = php_sprintf(__("Search Results for &#8220;%s&#8221;"), get_search_query())
        pass
    elif is_front_page():
        title_["title"] = get_bloginfo("name", "display")
        pass
    elif is_post_type_archive():
        title_["title"] = post_type_archive_title("", False)
        pass
    elif is_tax():
        title_["title"] = single_term_title("", False)
        pass
    elif is_home() or is_singular():
        title_["title"] = single_post_title("", False)
        pass
    elif is_category() or is_tag():
        title_["title"] = single_term_title("", False)
        pass
    elif is_author() and get_queried_object():
        author_ = get_queried_object()
        title_["title"] = author_.display_name
        pass
    elif is_year():
        title_["title"] = get_the_date(_x("Y", "yearly archives date format"))
    elif is_month():
        title_["title"] = get_the_date(_x("F Y", "monthly archives date format"))
    elif is_day():
        title_["title"] = get_the_date()
    # end if
    #// Add a page number if necessary.
    if paged_ >= 2 or page_ >= 2 and (not is_404()):
        #// translators: %s: Page number.
        title_["page"] = php_sprintf(__("Page %s"), php_max(paged_, page_))
    # end if
    #// Append the description or site title to give context.
    if is_front_page():
        title_["tagline"] = get_bloginfo("description", "display")
    else:
        title_["site"] = get_bloginfo("name", "display")
    # end if
    #// 
    #// Filters the separator for the document title.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $sep Document title separator. Default '-'.
    #//
    sep_ = apply_filters("document_title_separator", "-")
    #// 
    #// Filters the parts of the document title.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $title {
    #// The document title parts.
    #// 
    #// @type string $title   Title of the viewed page.
    #// @type string $page    Optional. Page number if paginated.
    #// @type string $tagline Optional. Site description when on home page.
    #// @type string $site    Optional. Site title when not on home page.
    #// }
    #//
    title_ = apply_filters("document_title_parts", title_)
    title_ = php_implode(str(" ") + str(sep_) + str(" "), php_array_filter(title_))
    title_ = wptexturize(title_)
    title_ = convert_chars(title_)
    title_ = esc_html(title_)
    title_ = capital_P_dangit(title_)
    return title_
# end def wp_get_document_title
#// 
#// Displays title tag with content.
#// 
#// @ignore
#// @since 4.1.0
#// @since 4.4.0 Improved title output replaced `wp_title()`.
#// @access private
#//
def _wp_render_title_tag(*_args_):
    
    
    if (not current_theme_supports("title-tag")):
        return
    # end if
    php_print("<title>" + wp_get_document_title() + "</title>" + "\n")
# end def _wp_render_title_tag
#// 
#// Display or retrieve page title for all areas of blog.
#// 
#// By default, the page title will display the separator before the page title,
#// so that the blog title will be before the page title. This is not good for
#// title display, since the blog title shows up on most tabs and not what is
#// important, which is the page that the user is looking at.
#// 
#// There are also SEO benefits to having the blog title after or to the 'right'
#// of the page title. However, it is mostly common sense to have the blog title
#// to the right with most browsers supporting tabs. You can achieve this by
#// using the seplocation parameter and setting the value to 'right'. This change
#// was introduced around 2.5.0, in case backward compatibility of themes is
#// important.
#// 
#// @since 1.0.0
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @param string $sep         Optional, default is '&raquo;'. How to separate the various items
#// within the page title.
#// @param bool   $display     Optional, default is true. Whether to display or retrieve title.
#// @param string $seplocation Optional. Location of the separator ('left' or 'right').
#// @return string|null String on retrieve, null when displaying.
#//
def wp_title(sep_="&raquo;", display_=None, seplocation_="", *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    m_ = get_query_var("m")
    year_ = get_query_var("year")
    monthnum_ = get_query_var("monthnum")
    day_ = get_query_var("day")
    search_ = get_query_var("s")
    title_ = ""
    t_sep_ = "%WP_TITLE_SEP%"
    #// Temporary separator, for accurate flipping, if necessary.
    #// If there is a post.
    if is_single() or is_home() and (not is_front_page()) or is_page() and (not is_front_page()):
        title_ = single_post_title("", False)
    # end if
    #// If there's a post type archive.
    if is_post_type_archive():
        post_type_ = get_query_var("post_type")
        if php_is_array(post_type_):
            post_type_ = reset(post_type_)
        # end if
        post_type_object_ = get_post_type_object(post_type_)
        if (not post_type_object_.has_archive):
            title_ = post_type_archive_title("", False)
        # end if
    # end if
    #// If there's a category or tag.
    if is_category() or is_tag():
        title_ = single_term_title("", False)
    # end if
    #// If there's a taxonomy.
    if is_tax():
        term_ = get_queried_object()
        if term_:
            tax_ = get_taxonomy(term_.taxonomy)
            title_ = single_term_title(tax_.labels.name + t_sep_, False)
        # end if
    # end if
    #// If there's an author.
    if is_author() and (not is_post_type_archive()):
        author_ = get_queried_object()
        if author_:
            title_ = author_.display_name
        # end if
    # end if
    #// Post type archives with has_archive should override terms.
    if is_post_type_archive() and post_type_object_.has_archive:
        title_ = post_type_archive_title("", False)
    # end if
    #// If there's a month.
    if is_archive() and (not php_empty(lambda : m_)):
        my_year_ = php_substr(m_, 0, 4)
        my_month_ = wp_locale_.get_month(php_substr(m_, 4, 2))
        my_day_ = php_intval(php_substr(m_, 6, 2))
        title_ = my_year_ + t_sep_ + my_month_ if my_month_ else "" + t_sep_ + my_day_ if my_day_ else ""
    # end if
    #// If there's a year.
    if is_archive() and (not php_empty(lambda : year_)):
        title_ = year_
        if (not php_empty(lambda : monthnum_)):
            title_ += t_sep_ + wp_locale_.get_month(monthnum_)
        # end if
        if (not php_empty(lambda : day_)):
            title_ += t_sep_ + zeroise(day_, 2)
        # end if
    # end if
    #// If it's a search.
    if is_search():
        #// translators: 1: Separator, 2: Search query.
        title_ = php_sprintf(__("Search Results %1$s %2$s"), t_sep_, strip_tags(search_))
    # end if
    #// If it's a 404 page.
    if is_404():
        title_ = __("Page not found")
    # end if
    prefix_ = ""
    if (not php_empty(lambda : title_)):
        prefix_ = str(" ") + str(sep_) + str(" ")
    # end if
    #// 
    #// Filters the parts of the page title.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string[] $title_array Array of parts of the page title.
    #//
    title_array_ = apply_filters("wp_title_parts", php_explode(t_sep_, title_))
    #// Determines position of the separator and direction of the breadcrumb.
    if "right" == seplocation_:
        #// Separator on right, so reverse the order.
        title_array_ = array_reverse(title_array_)
        title_ = php_implode(str(" ") + str(sep_) + str(" "), title_array_) + prefix_
    else:
        title_ = prefix_ + php_implode(str(" ") + str(sep_) + str(" "), title_array_)
    # end if
    #// 
    #// Filters the text of the page title.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $title       Page title.
    #// @param string $sep         Title separator.
    #// @param string $seplocation Location of the separator ('left' or 'right').
    #//
    title_ = apply_filters("wp_title", title_, sep_, seplocation_)
    #// Send it out.
    if display_:
        php_print(title_)
    else:
        return title_
    # end if
# end def wp_title
#// 
#// Display or retrieve page title for post.
#// 
#// This is optimized for single.php template file for displaying the post title.
#// 
#// It does not support placing the separator after the title, but by leaving the
#// prefix parameter empty, you can set the title separator manually. The prefix
#// does not automatically place a space between the prefix, so if there should
#// be a space, the parameter value will need to have it at the end.
#// 
#// @since 0.71
#// 
#// @param string $prefix  Optional. What to display before the title.
#// @param bool   $display Optional, default is true. Whether to display or retrieve title.
#// @return string|void Title when retrieving.
#//
def single_post_title(prefix_="", display_=None, *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    _post_ = get_queried_object()
    if (not (php_isset(lambda : _post_.post_title))):
        return
    # end if
    #// 
    #// Filters the page title for a single post.
    #// 
    #// @since 0.71
    #// 
    #// @param string  $_post_title The single post page title.
    #// @param WP_Post $_post       The current post.
    #//
    title_ = apply_filters("single_post_title", _post_.post_title, _post_)
    if display_:
        php_print(prefix_ + title_)
    else:
        return prefix_ + title_
    # end if
# end def single_post_title
#// 
#// Display or retrieve title for a post type archive.
#// 
#// This is optimized for archive.php and archive-{$post_type}.php template files
#// for displaying the title of the post type.
#// 
#// @since 3.1.0
#// 
#// @param string $prefix  Optional. What to display before the title.
#// @param bool   $display Optional, default is true. Whether to display or retrieve title.
#// @return string|void Title when retrieving, null when displaying or failure.
#//
def post_type_archive_title(prefix_="", display_=None, *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    if (not is_post_type_archive()):
        return
    # end if
    post_type_ = get_query_var("post_type")
    if php_is_array(post_type_):
        post_type_ = reset(post_type_)
    # end if
    post_type_obj_ = get_post_type_object(post_type_)
    #// 
    #// Filters the post type archive title.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $post_type_name Post type 'name' label.
    #// @param string $post_type      Post type.
    #//
    title_ = apply_filters("post_type_archive_title", post_type_obj_.labels.name, post_type_)
    if display_:
        php_print(prefix_ + title_)
    else:
        return prefix_ + title_
    # end if
# end def post_type_archive_title
#// 
#// Display or retrieve page title for category archive.
#// 
#// Useful for category template files for displaying the category page title.
#// The prefix does not automatically place a space between the prefix, so if
#// there should be a space, the parameter value will need to have it at the end.
#// 
#// @since 0.71
#// 
#// @param string $prefix  Optional. What to display before the title.
#// @param bool   $display Optional, default is true. Whether to display or retrieve title.
#// @return string|void Title when retrieving.
#//
def single_cat_title(prefix_="", display_=None, *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    return single_term_title(prefix_, display_)
# end def single_cat_title
#// 
#// Display or retrieve page title for tag post archive.
#// 
#// Useful for tag template files for displaying the tag page title. The prefix
#// does not automatically place a space between the prefix, so if there should
#// be a space, the parameter value will need to have it at the end.
#// 
#// @since 2.3.0
#// 
#// @param string $prefix  Optional. What to display before the title.
#// @param bool   $display Optional, default is true. Whether to display or retrieve title.
#// @return string|void Title when retrieving.
#//
def single_tag_title(prefix_="", display_=None, *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    return single_term_title(prefix_, display_)
# end def single_tag_title
#// 
#// Display or retrieve page title for taxonomy term archive.
#// 
#// Useful for taxonomy term template files for displaying the taxonomy term page title.
#// The prefix does not automatically place a space between the prefix, so if there should
#// be a space, the parameter value will need to have it at the end.
#// 
#// @since 3.1.0
#// 
#// @param string $prefix  Optional. What to display before the title.
#// @param bool   $display Optional, default is true. Whether to display or retrieve title.
#// @return string|void Title when retrieving.
#//
def single_term_title(prefix_="", display_=None, *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    term_ = get_queried_object()
    if (not term_):
        return
    # end if
    if is_category():
        #// 
        #// Filters the category archive page title.
        #// 
        #// @since 2.0.10
        #// 
        #// @param string $term_name Category name for archive being displayed.
        #//
        term_name_ = apply_filters("single_cat_title", term_.name)
    elif is_tag():
        #// 
        #// Filters the tag archive page title.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $term_name Tag name for archive being displayed.
        #//
        term_name_ = apply_filters("single_tag_title", term_.name)
    elif is_tax():
        #// 
        #// Filters the custom taxonomy archive page title.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $term_name Term name for archive being displayed.
        #//
        term_name_ = apply_filters("single_term_title", term_.name)
    else:
        return
    # end if
    if php_empty(lambda : term_name_):
        return
    # end if
    if display_:
        php_print(prefix_ + term_name_)
    else:
        return prefix_ + term_name_
    # end if
# end def single_term_title
#// 
#// Display or retrieve page title for post archive based on date.
#// 
#// Useful for when the template only needs to display the month and year,
#// if either are available. The prefix does not automatically place a space
#// between the prefix, so if there should be a space, the parameter value
#// will need to have it at the end.
#// 
#// @since 0.71
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @param string $prefix  Optional. What to display before the title.
#// @param bool   $display Optional, default is true. Whether to display or retrieve title.
#// @return string|void Title when retrieving.
#//
def single_month_title(prefix_="", display_=None, *_args_):
    if display_ is None:
        display_ = True
    # end if
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    m_ = get_query_var("m")
    year_ = get_query_var("year")
    monthnum_ = get_query_var("monthnum")
    if (not php_empty(lambda : monthnum_)) and (not php_empty(lambda : year_)):
        my_year_ = year_
        my_month_ = wp_locale_.get_month(monthnum_)
    elif (not php_empty(lambda : m_)):
        my_year_ = php_substr(m_, 0, 4)
        my_month_ = wp_locale_.get_month(php_substr(m_, 4, 2))
    # end if
    if php_empty(lambda : my_month_):
        return False
    # end if
    result_ = prefix_ + my_month_ + prefix_ + my_year_
    if (not display_):
        return result_
    # end if
    php_print(result_)
# end def single_month_title
#// 
#// Display the archive title based on the queried object.
#// 
#// @since 4.1.0
#// 
#// @see get_the_archive_title()
#// 
#// @param string $before Optional. Content to prepend to the title. Default empty.
#// @param string $after  Optional. Content to append to the title. Default empty.
#//
def the_archive_title(before_="", after_="", *_args_):
    
    
    title_ = get_the_archive_title()
    if (not php_empty(lambda : title_)):
        php_print(before_ + title_ + after_)
    # end if
# end def the_archive_title
#// 
#// Retrieve the archive title based on the queried object.
#// 
#// @since 4.1.0
#// 
#// @return string Archive title.
#//
def get_the_archive_title(*_args_):
    
    
    title_ = __("Archives")
    if is_category():
        #// translators: Category archive title. %s: Category name.
        title_ = php_sprintf(__("Category: %s"), single_cat_title("", False))
    elif is_tag():
        #// translators: Tag archive title. %s: Tag name.
        title_ = php_sprintf(__("Tag: %s"), single_tag_title("", False))
    elif is_author():
        #// translators: Author archive title. %s: Author name.
        title_ = php_sprintf(__("Author: %s"), "<span class=\"vcard\">" + get_the_author() + "</span>")
    elif is_year():
        #// translators: Yearly archive title. %s: Year.
        title_ = php_sprintf(__("Year: %s"), get_the_date(_x("Y", "yearly archives date format")))
    elif is_month():
        #// translators: Monthly archive title. %s: Month name and year.
        title_ = php_sprintf(__("Month: %s"), get_the_date(_x("F Y", "monthly archives date format")))
    elif is_day():
        #// translators: Daily archive title. %s: Date.
        title_ = php_sprintf(__("Day: %s"), get_the_date(_x("F j, Y", "daily archives date format")))
    elif is_tax("post_format"):
        if is_tax("post_format", "post-format-aside"):
            title_ = _x("Asides", "post format archive title")
        elif is_tax("post_format", "post-format-gallery"):
            title_ = _x("Galleries", "post format archive title")
        elif is_tax("post_format", "post-format-image"):
            title_ = _x("Images", "post format archive title")
        elif is_tax("post_format", "post-format-video"):
            title_ = _x("Videos", "post format archive title")
        elif is_tax("post_format", "post-format-quote"):
            title_ = _x("Quotes", "post format archive title")
        elif is_tax("post_format", "post-format-link"):
            title_ = _x("Links", "post format archive title")
        elif is_tax("post_format", "post-format-status"):
            title_ = _x("Statuses", "post format archive title")
        elif is_tax("post_format", "post-format-audio"):
            title_ = _x("Audio", "post format archive title")
        elif is_tax("post_format", "post-format-chat"):
            title_ = _x("Chats", "post format archive title")
        # end if
    elif is_post_type_archive():
        #// translators: Post type archive title. %s: Post type name.
        title_ = php_sprintf(__("Archives: %s"), post_type_archive_title("", False))
    elif is_tax():
        queried_object_ = get_queried_object()
        if queried_object_:
            tax_ = get_taxonomy(queried_object_.taxonomy)
            #// translators: Taxonomy term archive title. 1: Taxonomy singular name, 2: Current taxonomy term.
            title_ = php_sprintf(__("%1$s: %2$s"), tax_.labels.singular_name, single_term_title("", False))
        # end if
    # end if
    #// 
    #// Filters the archive title.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $title Archive title to be displayed.
    #//
    return apply_filters("get_the_archive_title", title_)
# end def get_the_archive_title
#// 
#// Display category, tag, term, or author description.
#// 
#// @since 4.1.0
#// 
#// @see get_the_archive_description()
#// 
#// @param string $before Optional. Content to prepend to the description. Default empty.
#// @param string $after  Optional. Content to append to the description. Default empty.
#//
def the_archive_description(before_="", after_="", *_args_):
    
    
    description_ = get_the_archive_description()
    if description_:
        php_print(before_ + description_ + after_)
    # end if
# end def the_archive_description
#// 
#// Retrieves the description for an author, post type, or term archive.
#// 
#// @since 4.1.0
#// @since 4.7.0 Added support for author archives.
#// @since 4.9.0 Added support for post type archives.
#// 
#// @see term_description()
#// 
#// @return string Archive description.
#//
def get_the_archive_description(*_args_):
    
    
    if is_author():
        description_ = get_the_author_meta("description")
    elif is_post_type_archive():
        description_ = get_the_post_type_description()
    else:
        description_ = term_description()
    # end if
    #// 
    #// Filters the archive description.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $description Archive description to be displayed.
    #//
    return apply_filters("get_the_archive_description", description_)
# end def get_the_archive_description
#// 
#// Retrieves the description for a post type archive.
#// 
#// @since 4.9.0
#// 
#// @return string The post type description.
#//
def get_the_post_type_description(*_args_):
    
    
    post_type_ = get_query_var("post_type")
    if php_is_array(post_type_):
        post_type_ = reset(post_type_)
    # end if
    post_type_obj_ = get_post_type_object(post_type_)
    #// Check if a description is set.
    if (php_isset(lambda : post_type_obj_.description)):
        description_ = post_type_obj_.description
    else:
        description_ = ""
    # end if
    #// 
    #// Filters the description for a post type archive.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string       $description   The post type description.
    #// @param WP_Post_Type $post_type_obj The post type object.
    #//
    return apply_filters("get_the_post_type_description", description_, post_type_obj_)
# end def get_the_post_type_description
#// 
#// Retrieve archive link content based on predefined or custom code.
#// 
#// The format can be one of four styles. The 'link' for head element, 'option'
#// for use in the select element, 'html' for use in list (either ol or ul HTML
#// elements). Custom content is also supported using the before and after
#// parameters.
#// 
#// The 'link' format uses the `<link>` HTML element with the **archives
#// relationship. The before and after parameters are not used. The text
#// parameter is used to describe the link.
#// 
#// The 'option' format uses the option HTML element for use in select element.
#// The value is the url parameter and the before and after parameters are used
#// between the text description.
#// 
#// The 'html' format, which is the default, uses the li HTML element for use in
#// the list HTML elements. The before parameter is before the link and the after
#// parameter is after the closing link.
#// 
#// The custom format uses the before parameter before the link ('a' HTML
#// element) and the after parameter after the closing link tag. If the above
#// three values for the format are not used, then custom format is assumed.
#// 
#// @since 1.0.0
#// @since 5.2.0 Added the `$selected` parameter.
#// 
#// @param string $url      URL to archive.
#// @param string $text     Archive text description.
#// @param string $format   Optional, default is 'html'. Can be 'link', 'option', 'html', or custom.
#// @param string $before   Optional. Content to prepend to the description. Default empty.
#// @param string $after    Optional. Content to append to the description. Default empty.
#// @param bool   $selected Optional. Set to true if the current page is the selected archive page.
#// @return string HTML link content for archive.
#//
def get_archives_link(url_=None, text_=None, format_="html", before_="", after_="", selected_=None, *_args_):
    if selected_ is None:
        selected_ = False
    # end if
    
    text_ = wptexturize(text_)
    url_ = esc_url(url_)
    aria_current_ = " aria-current=\"page\"" if selected_ else ""
    if "link" == format_:
        link_html_ = "  <link rel='archives' title='" + esc_attr(text_) + str("' href='") + str(url_) + str("' />\n")
    elif "option" == format_:
        selected_attr_ = " selected='selected'" if selected_ else ""
        link_html_ = str("  <option value='") + str(url_) + str("'") + str(selected_attr_) + str(">") + str(before_) + str(" ") + str(text_) + str(" ") + str(after_) + str("</option>\n")
    elif "html" == format_:
        link_html_ = str("  <li>") + str(before_) + str("<a href='") + str(url_) + str("'") + str(aria_current_) + str(">") + str(text_) + str("</a>") + str(after_) + str("</li>\n")
    else:
        #// Custom.
        link_html_ = str("  ") + str(before_) + str("<a href='") + str(url_) + str("'") + str(aria_current_) + str(">") + str(text_) + str("</a>") + str(after_) + str("\n")
    # end if
    #// 
    #// Filters the archive link content.
    #// 
    #// @since 2.6.0
    #// @since 4.5.0 Added the `$url`, `$text`, `$format`, `$before`, and `$after` parameters.
    #// @since 5.2.0 Added the `$selected` parameter.
    #// 
    #// @param string $link_html The archive HTML link content.
    #// @param string $url       URL to archive.
    #// @param string $text      Archive text description.
    #// @param string $format    Link format. Can be 'link', 'option', 'html', or custom.
    #// @param string $before    Content to prepend to the description.
    #// @param string $after     Content to append to the description.
    #// @param bool   $selected  True if the current page is the selected archive.
    #//
    return apply_filters("get_archives_link", link_html_, url_, text_, format_, before_, after_, selected_)
# end def get_archives_link
#// 
#// Display archive links based on type and format.
#// 
#// @since 1.2.0
#// @since 4.4.0 The `$post_type` argument was added.
#// @since 5.2.0 The `$year`, `$monthnum`, `$day`, and `$w` arguments were added.
#// 
#// @see get_archives_link()
#// 
#// @global wpdb      $wpdb      WordPress database abstraction object.
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @param string|array $args {
#// Default archive links arguments. Optional.
#// 
#// @type string     $type            Type of archive to retrieve. Accepts 'daily', 'weekly', 'monthly',
#// 'yearly', 'postbypost', or 'alpha'. Both 'postbypost' and 'alpha'
#// display the same archive link list as well as post titles instead
#// of displaying dates. The difference between the two is that 'alpha'
#// will order by post title and 'postbypost' will order by post date.
#// Default 'monthly'.
#// @type string|int $limit           Number of links to limit the query to. Default empty (no limit).
#// @type string     $format          Format each link should take using the $before and $after args.
#// Accepts 'link' (`<link>` tag), 'option' (`<option>` tag), 'html'
#// (`<li>` tag), or a custom format, which generates a link anchor
#// with $before preceding and $after succeeding. Default 'html'.
#// @type string     $before          Markup to prepend to the beginning of each link. Default empty.
#// @type string     $after           Markup to append to the end of each link. Default empty.
#// @type bool       $show_post_count Whether to display the post count alongside the link. Default false.
#// @type bool|int   $echo            Whether to echo or return the links list. Default 1|true to echo.
#// @type string     $order           Whether to use ascending or descending order. Accepts 'ASC', or 'DESC'.
#// Default 'DESC'.
#// @type string     $post_type       Post type. Default 'post'.
#// @type string     $year            Year. Default current year.
#// @type string     $monthnum        Month number. Default current month number.
#// @type string     $day             Day. Default current day.
#// @type string     $w               Week. Default current week.
#// }
#// @return void|string Void if 'echo' argument is true, archive links if 'echo' is false.
#//
def wp_get_archives(args_="", *_args_):
    
    
    global wpdb_
    global wp_locale_
    php_check_if_defined("wpdb_","wp_locale_")
    defaults_ = Array({"type": "monthly", "limit": "", "format": "html", "before": "", "after": "", "show_post_count": False, "echo": 1, "order": "DESC", "post_type": "post", "year": get_query_var("year"), "monthnum": get_query_var("monthnum"), "day": get_query_var("day"), "w": get_query_var("w")})
    parsed_args_ = wp_parse_args(args_, defaults_)
    post_type_object_ = get_post_type_object(parsed_args_["post_type"])
    if (not is_post_type_viewable(post_type_object_)):
        return
    # end if
    parsed_args_["post_type"] = post_type_object_.name
    if "" == parsed_args_["type"]:
        parsed_args_["type"] = "monthly"
    # end if
    if (not php_empty(lambda : parsed_args_["limit"])):
        parsed_args_["limit"] = absint(parsed_args_["limit"])
        parsed_args_["limit"] = " LIMIT " + parsed_args_["limit"]
    # end if
    order_ = php_strtoupper(parsed_args_["order"])
    if "ASC" != order_:
        order_ = "DESC"
    # end if
    #// This is what will separate dates on weekly archive links.
    archive_week_separator_ = "&#8211;"
    sql_where_ = wpdb_.prepare("WHERE post_type = %s AND post_status = 'publish'", parsed_args_["post_type"])
    #// 
    #// Filters the SQL WHERE clause for retrieving archives.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $sql_where   Portion of SQL query containing the WHERE clause.
    #// @param array  $parsed_args An array of default arguments.
    #//
    where_ = apply_filters("getarchives_where", sql_where_, parsed_args_)
    #// 
    #// Filters the SQL JOIN clause for retrieving archives.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $sql_join    Portion of SQL query containing JOIN clause.
    #// @param array  $parsed_args An array of default arguments.
    #//
    join_ = apply_filters("getarchives_join", "", parsed_args_)
    output_ = ""
    last_changed_ = wp_cache_get_last_changed("posts")
    limit_ = parsed_args_["limit"]
    if "monthly" == parsed_args_["type"]:
        query_ = str("SELECT YEAR(post_date) AS `year`, MONTH(post_date) AS `month`, count(ID) as posts FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" ") + str(where_) + str(" GROUP BY YEAR(post_date), MONTH(post_date) ORDER BY post_date ") + str(order_) + str(" ") + str(limit_)
        key_ = php_md5(query_)
        key_ = str("wp_get_archives:") + str(key_) + str(":") + str(last_changed_)
        results_ = wp_cache_get(key_, "posts")
        if (not results_):
            results_ = wpdb_.get_results(query_)
            wp_cache_set(key_, results_, "posts")
        # end if
        if results_:
            after_ = parsed_args_["after"]
            for result_ in results_:
                url_ = get_month_link(result_.year, result_.month)
                if "post" != parsed_args_["post_type"]:
                    url_ = add_query_arg("post_type", parsed_args_["post_type"], url_)
                # end if
                #// translators: 1: Month name, 2: 4-digit year.
                text_ = php_sprintf(__("%1$s %2$d"), wp_locale_.get_month(result_.month), result_.year)
                if parsed_args_["show_post_count"]:
                    parsed_args_["after"] = "&nbsp;(" + result_.posts + ")" + after_
                # end if
                selected_ = is_archive() and php_str(parsed_args_["year"]) == result_.year and php_str(parsed_args_["monthnum"]) == result_.month
                output_ += get_archives_link(url_, text_, parsed_args_["format"], parsed_args_["before"], parsed_args_["after"], selected_)
            # end for
        # end if
    elif "yearly" == parsed_args_["type"]:
        query_ = str("SELECT YEAR(post_date) AS `year`, count(ID) as posts FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" ") + str(where_) + str(" GROUP BY YEAR(post_date) ORDER BY post_date ") + str(order_) + str(" ") + str(limit_)
        key_ = php_md5(query_)
        key_ = str("wp_get_archives:") + str(key_) + str(":") + str(last_changed_)
        results_ = wp_cache_get(key_, "posts")
        if (not results_):
            results_ = wpdb_.get_results(query_)
            wp_cache_set(key_, results_, "posts")
        # end if
        if results_:
            after_ = parsed_args_["after"]
            for result_ in results_:
                url_ = get_year_link(result_.year)
                if "post" != parsed_args_["post_type"]:
                    url_ = add_query_arg("post_type", parsed_args_["post_type"], url_)
                # end if
                text_ = php_sprintf("%d", result_.year)
                if parsed_args_["show_post_count"]:
                    parsed_args_["after"] = "&nbsp;(" + result_.posts + ")" + after_
                # end if
                selected_ = is_archive() and php_str(parsed_args_["year"]) == result_.year
                output_ += get_archives_link(url_, text_, parsed_args_["format"], parsed_args_["before"], parsed_args_["after"], selected_)
            # end for
        # end if
    elif "daily" == parsed_args_["type"]:
        query_ = str("SELECT YEAR(post_date) AS `year`, MONTH(post_date) AS `month`, DAYOFMONTH(post_date) AS `dayofmonth`, count(ID) as posts FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" ") + str(where_) + str(" GROUP BY YEAR(post_date), MONTH(post_date), DAYOFMONTH(post_date) ORDER BY post_date ") + str(order_) + str(" ") + str(limit_)
        key_ = php_md5(query_)
        key_ = str("wp_get_archives:") + str(key_) + str(":") + str(last_changed_)
        results_ = wp_cache_get(key_, "posts")
        if (not results_):
            results_ = wpdb_.get_results(query_)
            wp_cache_set(key_, results_, "posts")
        # end if
        if results_:
            after_ = parsed_args_["after"]
            for result_ in results_:
                url_ = get_day_link(result_.year, result_.month, result_.dayofmonth)
                if "post" != parsed_args_["post_type"]:
                    url_ = add_query_arg("post_type", parsed_args_["post_type"], url_)
                # end if
                date_ = php_sprintf("%1$d-%2$02d-%3$02d 00:00:00", result_.year, result_.month, result_.dayofmonth)
                text_ = mysql2date(get_option("date_format"), date_)
                if parsed_args_["show_post_count"]:
                    parsed_args_["after"] = "&nbsp;(" + result_.posts + ")" + after_
                # end if
                selected_ = is_archive() and php_str(parsed_args_["year"]) == result_.year and php_str(parsed_args_["monthnum"]) == result_.month and php_str(parsed_args_["day"]) == result_.dayofmonth
                output_ += get_archives_link(url_, text_, parsed_args_["format"], parsed_args_["before"], parsed_args_["after"], selected_)
            # end for
        # end if
    elif "weekly" == parsed_args_["type"]:
        week_ = _wp_mysql_week("`post_date`")
        query_ = str("SELECT DISTINCT ") + str(week_) + str(" AS `week`, YEAR( `post_date` ) AS `yr`, DATE_FORMAT( `post_date`, '%Y-%m-%d' ) AS `yyyymmdd`, count( `ID` ) AS `posts` FROM `") + str(wpdb_.posts) + str("` ") + str(join_) + str(" ") + str(where_) + str(" GROUP BY ") + str(week_) + str(", YEAR( `post_date` ) ORDER BY `post_date` ") + str(order_) + str(" ") + str(limit_)
        key_ = php_md5(query_)
        key_ = str("wp_get_archives:") + str(key_) + str(":") + str(last_changed_)
        results_ = wp_cache_get(key_, "posts")
        if (not results_):
            results_ = wpdb_.get_results(query_)
            wp_cache_set(key_, results_, "posts")
        # end if
        arc_w_last_ = ""
        if results_:
            after_ = parsed_args_["after"]
            for result_ in results_:
                if result_.week != arc_w_last_:
                    arc_year_ = result_.yr
                    arc_w_last_ = result_.week
                    arc_week_ = get_weekstartend(result_.yyyymmdd, get_option("start_of_week"))
                    arc_week_start_ = date_i18n(get_option("date_format"), arc_week_["start"])
                    arc_week_end_ = date_i18n(get_option("date_format"), arc_week_["end"])
                    url_ = add_query_arg(Array({"m": arc_year_, "w": result_.week}), home_url("/"))
                    if "post" != parsed_args_["post_type"]:
                        url_ = add_query_arg("post_type", parsed_args_["post_type"], url_)
                    # end if
                    text_ = arc_week_start_ + archive_week_separator_ + arc_week_end_
                    if parsed_args_["show_post_count"]:
                        parsed_args_["after"] = "&nbsp;(" + result_.posts + ")" + after_
                    # end if
                    selected_ = is_archive() and php_str(parsed_args_["year"]) == result_.yr and php_str(parsed_args_["w"]) == result_.week
                    output_ += get_archives_link(url_, text_, parsed_args_["format"], parsed_args_["before"], parsed_args_["after"], selected_)
                # end if
            # end for
        # end if
    elif "postbypost" == parsed_args_["type"] or "alpha" == parsed_args_["type"]:
        orderby_ = "post_title ASC " if "alpha" == parsed_args_["type"] else "post_date DESC, ID DESC "
        query_ = str("SELECT * FROM ") + str(wpdb_.posts) + str(" ") + str(join_) + str(" ") + str(where_) + str(" ORDER BY ") + str(orderby_) + str(" ") + str(limit_)
        key_ = php_md5(query_)
        key_ = str("wp_get_archives:") + str(key_) + str(":") + str(last_changed_)
        results_ = wp_cache_get(key_, "posts")
        if (not results_):
            results_ = wpdb_.get_results(query_)
            wp_cache_set(key_, results_, "posts")
        # end if
        if results_:
            for result_ in results_:
                if "0000-00-00 00:00:00" != result_.post_date:
                    url_ = get_permalink(result_)
                    if result_.post_title:
                        #// This filter is documented in wp-includes/post-template.php
                        text_ = strip_tags(apply_filters("the_title", result_.post_title, result_.ID))
                    else:
                        text_ = result_.ID
                    # end if
                    selected_ = get_the_ID() == result_.ID
                    output_ += get_archives_link(url_, text_, parsed_args_["format"], parsed_args_["before"], parsed_args_["after"], selected_)
                # end if
            # end for
        # end if
    # end if
    if parsed_args_["echo"]:
        php_print(output_)
    else:
        return output_
    # end if
# end def wp_get_archives
#// 
#// Get number of days since the start of the week.
#// 
#// @since 1.5.0
#// 
#// @param int $num Number of day.
#// @return float Days since the start of the week.
#//
def calendar_week_mod(num_=None, *_args_):
    
    
    base_ = 7
    return num_ - base_ * floor(num_ / base_)
# end def calendar_week_mod
#// 
#// Display calendar with days that have posts as links.
#// 
#// The calendar is cached, which will be retrieved, if it exists. If there are
#// no posts for the month, then it will not be displayed.
#// 
#// @since 1.0.0
#// 
#// @global wpdb      $wpdb      WordPress database abstraction object.
#// @global int       $m
#// @global int       $monthnum
#// @global int       $year
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// @global array     $posts
#// 
#// @param bool $initial Optional, default is true. Use initial calendar names.
#// @param bool $echo    Optional, default is true. Set to false for return.
#// @return void|string Void if `$echo` argument is true, calendar HTML if `$echo` is false.
#//
def get_calendar(initial_=None, echo_=None, *_args_):
    if initial_ is None:
        initial_ = True
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    global wpdb_
    global m_
    global monthnum_
    global year_
    global wp_locale_
    global posts_
    php_check_if_defined("wpdb_","m_","monthnum_","year_","wp_locale_","posts_")
    key_ = php_md5(m_ + monthnum_ + year_)
    cache_ = wp_cache_get("get_calendar", "calendar")
    if cache_ and php_is_array(cache_) and (php_isset(lambda : cache_[key_])):
        #// This filter is documented in wp-includes/general-template.php
        output_ = apply_filters("get_calendar", cache_[key_])
        if echo_:
            php_print(output_)
            return
        # end if
        return output_
    # end if
    if (not php_is_array(cache_)):
        cache_ = Array()
    # end if
    #// Quick check. If we have no posts at all, abort!
    if (not posts_):
        gotsome_ = wpdb_.get_var(str("SELECT 1 as test FROM ") + str(wpdb_.posts) + str(" WHERE post_type = 'post' AND post_status = 'publish' LIMIT 1"))
        if (not gotsome_):
            cache_[key_] = ""
            wp_cache_set("get_calendar", cache_, "calendar")
            return
        # end if
    # end if
    if (php_isset(lambda : PHP_REQUEST["w"])):
        w_ = php_int(PHP_REQUEST["w"])
    # end if
    #// week_begins = 0 stands for Sunday.
    week_begins_ = php_int(get_option("start_of_week"))
    #// Let's figure out when we are.
    if (not php_empty(lambda : monthnum_)) and (not php_empty(lambda : year_)):
        thismonth_ = zeroise(php_intval(monthnum_), 2)
        thisyear_ = php_int(year_)
    elif (not php_empty(lambda : w_)):
        #// We need to get the month from MySQL.
        thisyear_ = php_int(php_substr(m_, 0, 4))
        #// It seems MySQL's weeks disagree with PHP's.
        d_ = w_ - 1 * 7 + 6
        thismonth_ = wpdb_.get_var(str("SELECT DATE_FORMAT((DATE_ADD('") + str(thisyear_) + str("0101', INTERVAL ") + str(d_) + str(" DAY) ), '%m')"))
    elif (not php_empty(lambda : m_)):
        thisyear_ = php_int(php_substr(m_, 0, 4))
        if php_strlen(m_) < 6:
            thismonth_ = "01"
        else:
            thismonth_ = zeroise(php_int(php_substr(m_, 4, 2)), 2)
        # end if
    else:
        thisyear_ = current_time("Y")
        thismonth_ = current_time("m")
    # end if
    unixmonth_ = mktime(0, 0, 0, thismonth_, 1, thisyear_)
    last_day_ = gmdate("t", unixmonth_)
    #// Get the next and previous month and year with at least one post.
    previous_ = wpdb_.get_row(str("SELECT MONTH(post_date) AS month, YEAR(post_date) AS year\n      FROM ") + str(wpdb_.posts) + str("\n        WHERE post_date < '") + str(thisyear_) + str("-") + str(thismonth_) + str("""-01'\n     AND post_type = 'post' AND post_status = 'publish'\n            ORDER BY post_date DESC\n           LIMIT 1"""))
    next_ = wpdb_.get_row(str("SELECT MONTH(post_date) AS month, YEAR(post_date) AS year\n      FROM ") + str(wpdb_.posts) + str("\n        WHERE post_date > '") + str(thisyear_) + str("-") + str(thismonth_) + str("-") + str(last_day_) + str(""" 23:59:59'\n       AND post_type = 'post' AND post_status = 'publish'\n            ORDER BY post_date ASC\n            LIMIT 1"""))
    #// translators: Calendar caption: 1: Month name, 2: 4-digit year.
    calendar_caption_ = _x("%1$s %2$s", "calendar caption")
    calendar_output_ = "<table id=\"wp-calendar\" class=\"wp-calendar-table\">\n    <caption>" + php_sprintf(calendar_caption_, wp_locale_.get_month(thismonth_), gmdate("Y", unixmonth_)) + "</caption>\n  <thead>\n   <tr>"
    myweek_ = Array()
    wdcount_ = 0
    while wdcount_ <= 6:
        
        myweek_[-1] = wp_locale_.get_weekday(wdcount_ + week_begins_ % 7)
        wdcount_ += 1
    # end while
    for wd_ in myweek_:
        day_name_ = wp_locale_.get_weekday_initial(wd_) if initial_ else wp_locale_.get_weekday_abbrev(wd_)
        wd_ = esc_attr(wd_)
        calendar_output_ += str("\n     <th scope=\"col\" title=\"") + str(wd_) + str("\">") + str(day_name_) + str("</th>")
    # end for
    calendar_output_ += """
    </tr>
    </thead>
    <tbody>
    <tr>"""
    daywithpost_ = Array()
    #// Get days with posts.
    dayswithposts_ = wpdb_.get_results(str("SELECT DISTINCT DAYOFMONTH(post_date)\n     FROM ") + str(wpdb_.posts) + str(" WHERE post_date >= '") + str(thisyear_) + str("-") + str(thismonth_) + str("-01 00:00:00'\n      AND post_type = 'post' AND post_status = 'publish'\n        AND post_date <= '") + str(thisyear_) + str("-") + str(thismonth_) + str("-") + str(last_day_) + str(" 23:59:59'"), ARRAY_N)
    if dayswithposts_:
        for daywith_ in dayswithposts_:
            daywithpost_[-1] = daywith_[0]
        # end for
    # end if
    #// See how much we should pad in the beginning.
    pad_ = calendar_week_mod(gmdate("w", unixmonth_) - week_begins_)
    if 0 != pad_:
        calendar_output_ += "\n     " + "<td colspan=\"" + esc_attr(pad_) + "\" class=\"pad\">&nbsp;</td>"
    # end if
    newrow_ = False
    daysinmonth_ = php_int(gmdate("t", unixmonth_))
    day_ = 1
    while day_ <= daysinmonth_:
        
        if (php_isset(lambda : newrow_)) and newrow_:
            calendar_output_ += """
            </tr>
            <tr>
            """
        # end if
        newrow_ = False
        if current_time("j") == day_ and current_time("m") == thismonth_ and current_time("Y") == thisyear_:
            calendar_output_ += "<td id=\"today\">"
        else:
            calendar_output_ += "<td>"
        # end if
        if php_in_array(day_, daywithpost_):
            #// Any posts today?
            date_format_ = gmdate(_x("F j, Y", "daily archives date format"), strtotime(str(thisyear_) + str("-") + str(thismonth_) + str("-") + str(day_)))
            #// translators: Post calendar label. %s: Date.
            label_ = php_sprintf(__("Posts published on %s"), date_format_)
            calendar_output_ += php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_day_link(thisyear_, thismonth_, day_), esc_attr(label_), day_)
        else:
            calendar_output_ += day_
        # end if
        calendar_output_ += "</td>"
        if 6 == calendar_week_mod(gmdate("w", mktime(0, 0, 0, thismonth_, day_, thisyear_)) - week_begins_):
            newrow_ = True
        # end if
        day_ += 1
    # end while
    pad_ = 7 - calendar_week_mod(gmdate("w", mktime(0, 0, 0, thismonth_, day_, thisyear_)) - week_begins_)
    if 0 != pad_ and 7 != pad_:
        calendar_output_ += "\n     " + "<td class=\"pad\" colspan=\"" + esc_attr(pad_) + "\">&nbsp;</td>"
    # end if
    calendar_output_ += "\n </tr>\n </tbody>"
    calendar_output_ += "\n </table>"
    calendar_output_ += "<nav aria-label=\"" + __("Previous and next months") + "\" class=\"wp-calendar-nav\">"
    if previous_:
        calendar_output_ += "\n     " + "<span class=\"wp-calendar-nav-prev\"><a href=\"" + get_month_link(previous_.year, previous_.month) + "\">&laquo; " + wp_locale_.get_month_abbrev(wp_locale_.get_month(previous_.month)) + "</a></span>"
    else:
        calendar_output_ += "\n     " + "<span class=\"wp-calendar-nav-prev\">&nbsp;</span>"
    # end if
    calendar_output_ += "\n     " + "<span class=\"pad\">&nbsp;</span>"
    if next_:
        calendar_output_ += "\n     " + "<span class=\"wp-calendar-nav-next\"><a href=\"" + get_month_link(next_.year, next_.month) + "\">" + wp_locale_.get_month_abbrev(wp_locale_.get_month(next_.month)) + " &raquo;</a></span>"
    else:
        calendar_output_ += "\n     " + "<span class=\"wp-calendar-nav-next\">&nbsp;</span>"
    # end if
    calendar_output_ += "\n </nav>"
    cache_[key_] = calendar_output_
    wp_cache_set("get_calendar", cache_, "calendar")
    if echo_:
        #// 
        #// Filters the HTML calendar output.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $calendar_output HTML output of the calendar.
        #//
        php_print(apply_filters("get_calendar", calendar_output_))
        return
    # end if
    #// This filter is documented in wp-includes/general-template.php
    return apply_filters("get_calendar", calendar_output_)
# end def get_calendar
#// 
#// Purge the cached results of get_calendar.
#// 
#// @see get_calendar
#// @since 2.1.0
#//
def delete_get_calendar_cache(*_args_):
    
    
    wp_cache_delete("get_calendar", "calendar")
# end def delete_get_calendar_cache
#// 
#// Display all of the allowed tags in HTML format with attributes.
#// 
#// This is useful for displaying in the comment area, which elements and
#// attributes are supported. As well as any plugins which want to display it.
#// 
#// @since 1.0.1
#// 
#// @global array $allowedtags
#// 
#// @return string HTML allowed tags entity encoded.
#//
def allowed_tags(*_args_):
    
    
    global allowedtags_
    php_check_if_defined("allowedtags_")
    allowed_ = ""
    for tag_,attributes_ in allowedtags_:
        allowed_ += "<" + tag_
        if 0 < php_count(attributes_):
            for attribute_,limits_ in attributes_:
                allowed_ += " " + attribute_ + "=\"\""
            # end for
        # end if
        allowed_ += "> "
    # end for
    return htmlentities(allowed_)
# end def allowed_tags
#// Date/Time tags
#// 
#// Outputs the date in iso8601 format for xml files.
#// 
#// @since 1.0.0
#//
def the_date_xml(*_args_):
    
    
    php_print(mysql2date("Y-m-d", get_post().post_date, False))
# end def the_date_xml
#// 
#// Display or Retrieve the date the current post was written (once per date)
#// 
#// Will only output the date if the current post's date is different from the
#// previous one output.
#// 
#// i.e. Only one date listing will show per day worth of posts shown in the loop, even if the
#// function is called several times for each post.
#// 
#// HTML output can be filtered with 'the_date'.
#// Date string output can be filtered with 'get_the_date'.
#// 
#// @since 0.71
#// 
#// @global string $currentday  The day of the current post in the loop.
#// @global string $previousday The day of the previous post in the loop.
#// 
#// @param string $format Optional. PHP date format defaults to the date_format option if not specified.
#// @param string $before Optional. Output before the date.
#// @param string $after  Optional. Output after the date.
#// @param bool   $echo   Optional, default is display. Whether to echo the date or return it.
#// @return string|void String if retrieving.
#//
def the_date(format_="", before_="", after_="", echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    global currentday_
    global previousday_
    php_check_if_defined("currentday_","previousday_")
    the_date_ = ""
    if is_new_day():
        the_date_ = before_ + get_the_date(format_) + after_
        previousday_ = currentday_
    # end if
    #// 
    #// Filters the date a post was published for display.
    #// 
    #// @since 0.71
    #// 
    #// @param string $the_date The formatted date string.
    #// @param string $format   PHP date format. Defaults to 'date_format' option
    #// if not specified.
    #// @param string $before   HTML output before the date.
    #// @param string $after    HTML output after the date.
    #//
    the_date_ = apply_filters("the_date", the_date_, format_, before_, after_)
    if echo_:
        php_print(the_date_)
    else:
        return the_date_
    # end if
# end def the_date
#// 
#// Retrieve the date on which the post was written.
#// 
#// Unlike the_date() this function will always return the date.
#// Modify output with the {@see 'get_the_date'} filter.
#// 
#// @since 3.0.0
#// 
#// @param  string      $format Optional. PHP date format defaults to the date_format option if not specified.
#// @param  int|WP_Post $post   Optional. Post ID or WP_Post object. Default current post.
#// @return string|false Date the current post was written. False on failure.
#//
def get_the_date(format_="", post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    if "" == format_:
        the_date_ = get_post_time(get_option("date_format"), False, post_, True)
    else:
        the_date_ = get_post_time(format_, False, post_, True)
    # end if
    #// 
    #// Filters the date a post was published.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string      $the_date The formatted date.
    #// @param string      $format   PHP date format. Defaults to 'date_format' option
    #// if not specified.
    #// @param int|WP_Post $post     The post object or ID.
    #//
    return apply_filters("get_the_date", the_date_, format_, post_)
# end def get_the_date
#// 
#// Display the date on which the post was last modified.
#// 
#// @since 2.1.0
#// 
#// @param string $format Optional. PHP date format defaults to the date_format option if not specified.
#// @param string $before Optional. Output before the date.
#// @param string $after  Optional. Output after the date.
#// @param bool   $echo   Optional, default is display. Whether to echo the date or return it.
#// @return string|void String if retrieving.
#//
def the_modified_date(format_="", before_="", after_="", echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    the_modified_date_ = before_ + get_the_modified_date(format_) + after_
    #// 
    #// Filters the date a post was last modified for display.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $the_modified_date The last modified date.
    #// @param string $format            PHP date format. Defaults to 'date_format' option
    #// if not specified.
    #// @param string $before            HTML output before the date.
    #// @param string $after             HTML output after the date.
    #//
    the_modified_date_ = apply_filters("the_modified_date", the_modified_date_, format_, before_, after_)
    if echo_:
        php_print(the_modified_date_)
    else:
        return the_modified_date_
    # end if
# end def the_modified_date
#// 
#// Retrieve the date on which the post was last modified.
#// 
#// @since 2.1.0
#// @since 4.6.0 Added the `$post` parameter.
#// 
#// @param string      $format Optional. PHP date format defaults to the date_format option if not specified.
#// @param int|WP_Post $post   Optional. Post ID or WP_Post object. Default current post.
#// @return string|false Date the current post was modified. False on failure.
#//
def get_the_modified_date(format_="", post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        #// For backward compatibility, failures go through the filter below.
        the_time_ = False
    elif php_empty(lambda : format_):
        the_time_ = get_post_modified_time(get_option("date_format"), False, post_, True)
    else:
        the_time_ = get_post_modified_time(format_, False, post_, True)
    # end if
    #// 
    #// Filters the date a post was last modified.
    #// 
    #// @since 2.1.0
    #// @since 4.6.0 Added the `$post` parameter.
    #// 
    #// @param string|bool  $the_time The formatted date or false if no post is found.
    #// @param string       $format   PHP date format. Defaults to value specified in
    #// 'date_format' option.
    #// @param WP_Post|null $post     WP_Post object or null if no post is found.
    #//
    return apply_filters("get_the_modified_date", the_time_, format_, post_)
# end def get_the_modified_date
#// 
#// Display the time at which the post was written.
#// 
#// @since 0.71
#// 
#// @param string $format Either 'G', 'U', or PHP date format.
#//
def the_time(format_="", *_args_):
    
    
    #// 
    #// Filters the time a post was written for display.
    #// 
    #// @since 0.71
    #// 
    #// @param string $get_the_time The formatted time.
    #// @param string $format       The time format. Accepts 'G', 'U',
    #// or PHP date format.
    #//
    php_print(apply_filters("the_time", get_the_time(format_), format_))
# end def the_time
#// 
#// Retrieve the time at which the post was written.
#// 
#// @since 1.5.0
#// 
#// @param string      $format Optional. Format to use for retrieving the time the post
#// was written. Either 'G', 'U', or PHP date format defaults
#// to the value specified in the time_format option. Default empty.
#// @param int|WP_Post $post   WP_Post object or ID. Default is global `$post` object.
#// @return string|int|false Formatted date string or Unix timestamp if `$format` is 'U' or 'G'.
#// False on failure.
#//
def get_the_time(format_="", post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    if "" == format_:
        the_time_ = get_post_time(get_option("time_format"), False, post_, True)
    else:
        the_time_ = get_post_time(format_, False, post_, True)
    # end if
    #// 
    #// Filters the time a post was written.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string      $the_time The formatted time.
    #// @param string      $format   Format to use for retrieving the time the post was written.
    #// Accepts 'G', 'U', or PHP date format value specified
    #// in 'time_format' option. Default empty.
    #// @param int|WP_Post $post     WP_Post object or ID.
    #//
    return apply_filters("get_the_time", the_time_, format_, post_)
# end def get_the_time
#// 
#// Retrieve the time at which the post was written.
#// 
#// @since 2.0.0
#// 
#// @param string      $format    Optional. Format to use for retrieving the time the post
#// was written. Either 'G', 'U', or PHP date format. Default 'U'.
#// @param bool        $gmt       Optional. Whether to retrieve the GMT time. Default false.
#// @param int|WP_Post $post      WP_Post object or ID. Default is global `$post` object.
#// @param bool        $translate Whether to translate the time string. Default false.
#// @return string|int|false Formatted date string or Unix timestamp if `$format` is 'U' or 'G'.
#// False on failure.
#//
def get_post_time(format_="U", gmt_=None, post_=None, translate_=None, *_args_):
    if gmt_ is None:
        gmt_ = False
    # end if
    if translate_ is None:
        translate_ = False
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    source_ = "gmt" if gmt_ else "local"
    datetime_ = get_post_datetime(post_, "date", source_)
    if False == datetime_:
        return False
    # end if
    if "U" == format_ or "G" == format_:
        time_ = datetime_.gettimestamp()
        #// Returns a sum of timestamp with timezone offset. Ideally should never be used.
        if (not gmt_):
            time_ += datetime_.getoffset()
        # end if
    elif translate_:
        time_ = wp_date(format_, datetime_.gettimestamp(), php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")) if gmt_ else None)
    else:
        if gmt_:
            datetime_ = datetime_.settimezone(php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")))
        # end if
        time_ = datetime_.format(format_)
    # end if
    #// 
    #// Filters the localized time a post was written.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $time   The formatted time.
    #// @param string $format Format to use for retrieving the time the post was written.
    #// Accepts 'G', 'U', or PHP date format. Default 'U'.
    #// @param bool   $gmt    Whether to retrieve the GMT time. Default false.
    #//
    return apply_filters("get_post_time", time_, format_, gmt_)
# end def get_post_time
#// 
#// Retrieve post published or modified time as a `DateTimeImmutable` object instance.
#// 
#// The object will be set to the timezone from WordPress settings.
#// 
#// For legacy reasons, this function allows to choose to instantiate from local or UTC time in database.
#// Normally this should make no difference to the result. However, the values might get out of sync in database,
#// typically because of timezone setting changes. The parameter ensures the ability to reproduce backwards
#// compatible behaviors in such cases.
#// 
#// @since 5.3.0
#// 
#// @param int|WP_Post $post   Optional. WP_Post object or ID. Default is global `$post` object.
#// @param string      $field  Optional. Published or modified time to use from database. Accepts 'date' or 'modified'.
#// Default 'date'.
#// @param string      $source Optional. Local or UTC time to use from database. Accepts 'local' or 'gmt'.
#// Default 'local'.
#// @return DateTimeImmutable|false Time object on success, false on failure.
#//
def get_post_datetime(post_=None, field_="date", source_="local", *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    wp_timezone_ = wp_timezone()
    if "gmt" == source_:
        time_ = post_.post_modified_gmt if "modified" == field_ else post_.post_date_gmt
        timezone_ = php_new_class("DateTimeZone", lambda : DateTimeZone("UTC"))
    else:
        time_ = post_.post_modified if "modified" == field_ else post_.post_date
        timezone_ = wp_timezone_
    # end if
    if php_empty(lambda : time_) or "0000-00-00 00:00:00" == time_:
        return False
    # end if
    datetime_ = date_create_immutable_from_format("Y-m-d H:i:s", time_, timezone_)
    if False == datetime_:
        return False
    # end if
    return datetime_.settimezone(wp_timezone_)
# end def get_post_datetime
#// 
#// Retrieve post published or modified time as a Unix timestamp.
#// 
#// Note that this function returns a true Unix timestamp, not summed with timezone offset
#// like older WP functions.
#// 
#// @since 5.3.0
#// 
#// @param int|WP_Post $post  Optional. WP_Post object or ID. Default is global `$post` object.
#// @param string      $field Optional. Published or modified time to use from database. Accepts 'date' or 'modified'.
#// Default 'date'.
#// @return int|false Unix timestamp on success, false on failure.
#//
def get_post_timestamp(post_=None, field_="date", *_args_):
    
    
    datetime_ = get_post_datetime(post_, field_)
    if False == datetime_:
        return False
    # end if
    return datetime_.gettimestamp()
# end def get_post_timestamp
#// 
#// Display the time at which the post was last modified.
#// 
#// @since 2.0.0
#// 
#// @param string $format Optional. Either 'G', 'U', or PHP date format defaults
#// to the value specified in the time_format option.
#//
def the_modified_time(format_="", *_args_):
    
    
    #// 
    #// Filters the localized time a post was last modified, for display.
    #// 
    #// @since 2.0.0
    #// 
    #// @param string $get_the_modified_time The formatted time.
    #// @param string $format                The time format. Accepts 'G', 'U',
    #// or PHP date format. Defaults to value
    #// specified in 'time_format' option.
    #//
    php_print(apply_filters("the_modified_time", get_the_modified_time(format_), format_))
# end def the_modified_time
#// 
#// Retrieve the time at which the post was last modified.
#// 
#// @since 2.0.0
#// @since 4.6.0 Added the `$post` parameter.
#// 
#// @param string      $format Optional. Format to use for retrieving the time the post
#// was modified. Either 'G', 'U', or PHP date format defaults
#// to the value specified in the time_format option. Default empty.
#// @param int|WP_Post $post   Optional. Post ID or WP_Post object. Default current post.
#// @return string|false Formatted date string or Unix timestamp. False on failure.
#//
def get_the_modified_time(format_="", post_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        #// For backward compatibility, failures go through the filter below.
        the_time_ = False
    elif php_empty(lambda : format_):
        the_time_ = get_post_modified_time(get_option("time_format"), False, post_, True)
    else:
        the_time_ = get_post_modified_time(format_, False, post_, True)
    # end if
    #// 
    #// Filters the localized time a post was last modified.
    #// 
    #// @since 2.0.0
    #// @since 4.6.0 Added the `$post` parameter.
    #// 
    #// @param string|bool  $the_time The formatted time or false if no post is found.
    #// @param string       $format   Format to use for retrieving the time the post was
    #// written. Accepts 'G', 'U', or PHP date format. Defaults
    #// to value specified in 'time_format' option.
    #// @param WP_Post|null $post     WP_Post object or null if no post is found.
    #//
    return apply_filters("get_the_modified_time", the_time_, format_, post_)
# end def get_the_modified_time
#// 
#// Retrieve the time at which the post was last modified.
#// 
#// @since 2.0.0
#// 
#// @param string      $format    Optional. Format to use for retrieving the time the post
#// was modified. Either 'G', 'U', or PHP date format. Default 'U'.
#// @param bool        $gmt       Optional. Whether to retrieve the GMT time. Default false.
#// @param int|WP_Post $post      WP_Post object or ID. Default is global `$post` object.
#// @param bool        $translate Whether to translate the time string. Default false.
#// @return string|int|false Formatted date string or Unix timestamp if `$format` is 'U' or 'G'.
#// False on failure.
#//
def get_post_modified_time(format_="U", gmt_=None, post_=None, translate_=None, *_args_):
    if gmt_ is None:
        gmt_ = False
    # end if
    if translate_ is None:
        translate_ = False
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    source_ = "gmt" if gmt_ else "local"
    datetime_ = get_post_datetime(post_, "modified", source_)
    if False == datetime_:
        return False
    # end if
    if "U" == format_ or "G" == format_:
        time_ = datetime_.gettimestamp()
        #// Returns a sum of timestamp with timezone offset. Ideally should never be used.
        if (not gmt_):
            time_ += datetime_.getoffset()
        # end if
    elif translate_:
        time_ = wp_date(format_, datetime_.gettimestamp(), php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")) if gmt_ else None)
    else:
        if gmt_:
            datetime_ = datetime_.settimezone(php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")))
        # end if
        time_ = datetime_.format(format_)
    # end if
    #// 
    #// Filters the localized time a post was last modified.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $time   The formatted time.
    #// @param string $format Format to use for retrieving the time the post was modified.
    #// Accepts 'G', 'U', or PHP date format. Default 'U'.
    #// @param bool   $gmt    Whether to retrieve the GMT time. Default false.
    #//
    return apply_filters("get_post_modified_time", time_, format_, gmt_)
# end def get_post_modified_time
#// 
#// Display the weekday on which the post was written.
#// 
#// @since 0.71
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#//
def the_weekday(*_args_):
    
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    post_ = get_post()
    if (not post_):
        return
    # end if
    the_weekday_ = wp_locale_.get_weekday(get_post_time("w", False, post_))
    #// 
    #// Filters the weekday on which the post was written, for display.
    #// 
    #// @since 0.71
    #// 
    #// @param string $the_weekday
    #//
    php_print(apply_filters("the_weekday", the_weekday_))
# end def the_weekday
#// 
#// Display the weekday on which the post was written.
#// 
#// Will only output the weekday if the current post's weekday is different from
#// the previous one output.
#// 
#// @since 0.71
#// 
#// @global WP_Locale $wp_locale       WordPress date and time locale object.
#// @global string    $currentday      The day of the current post in the loop.
#// @global string    $previousweekday The day of the previous post in the loop.
#// 
#// @param string $before Optional. Output before the date.
#// @param string $after  Optional. Output after the date.
#//
def the_weekday_date(before_="", after_="", *_args_):
    
    
    global wp_locale_
    global currentday_
    global previousweekday_
    php_check_if_defined("wp_locale_","currentday_","previousweekday_")
    post_ = get_post()
    if (not post_):
        return
    # end if
    the_weekday_date_ = ""
    if currentday_ != previousweekday_:
        the_weekday_date_ += before_
        the_weekday_date_ += wp_locale_.get_weekday(get_post_time("w", False, post_))
        the_weekday_date_ += after_
        previousweekday_ = currentday_
    # end if
    #// 
    #// Filters the localized date on which the post was written, for display.
    #// 
    #// @since 0.71
    #// 
    #// @param string $the_weekday_date The weekday on which the post was written.
    #// @param string $before           The HTML to output before the date.
    #// @param string $after            The HTML to output after the date.
    #//
    php_print(apply_filters("the_weekday_date", the_weekday_date_, before_, after_))
# end def the_weekday_date
#// 
#// Fire the wp_head action.
#// 
#// See {@see 'wp_head'}.
#// 
#// @since 1.2.0
#//
def wp_head(*_args_):
    
    
    #// 
    #// Prints scripts or data in the head tag on the front end.
    #// 
    #// @since 1.5.0
    #//
    do_action("wp_head")
# end def wp_head
#// 
#// Fire the wp_footer action.
#// 
#// See {@see 'wp_footer'}.
#// 
#// @since 1.5.1
#//
def wp_footer(*_args_):
    
    
    #// 
    #// Prints scripts or data before the closing body tag on the front end.
    #// 
    #// @since 1.5.1
    #//
    do_action("wp_footer")
# end def wp_footer
#// 
#// Fire the wp_body_open action.
#// 
#// See {@see 'wp_body_open'}.
#// 
#// @since 5.2.0
#//
def wp_body_open(*_args_):
    
    
    #// 
    #// Triggered after the opening body tag.
    #// 
    #// @since 5.2.0
    #//
    do_action("wp_body_open")
# end def wp_body_open
#// 
#// Display the links to the general feeds.
#// 
#// @since 2.8.0
#// 
#// @param array $args Optional arguments.
#//
def feed_links(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    if (not current_theme_supports("automatic-feed-links")):
        return
    # end if
    defaults_ = Array({"separator": _x("&raquo;", "feed link"), "feedtitle": __("%1$s %2$s Feed"), "comstitle": __("%1$s %2$s Comments Feed")})
    args_ = wp_parse_args(args_, defaults_)
    #// 
    #// Filters whether to display the posts feed link.
    #// 
    #// @since 4.4.0
    #// 
    #// @param bool $show Whether to display the posts feed link. Default true.
    #//
    if apply_filters("feed_links_show_posts_feed", True):
        php_print("<link rel=\"alternate\" type=\"" + feed_content_type() + "\" title=\"" + esc_attr(php_sprintf(args_["feedtitle"], get_bloginfo("name"), args_["separator"])) + "\" href=\"" + esc_url(get_feed_link()) + "\" />\n")
    # end if
    #// 
    #// Filters whether to display the comments feed link.
    #// 
    #// @since 4.4.0
    #// 
    #// @param bool $show Whether to display the comments feed link. Default true.
    #//
    if apply_filters("feed_links_show_comments_feed", True):
        php_print("<link rel=\"alternate\" type=\"" + feed_content_type() + "\" title=\"" + esc_attr(php_sprintf(args_["comstitle"], get_bloginfo("name"), args_["separator"])) + "\" href=\"" + esc_url(get_feed_link("comments_" + get_default_feed())) + "\" />\n")
    # end if
# end def feed_links
#// 
#// Display the links to the extra feeds such as category feeds.
#// 
#// @since 2.8.0
#// 
#// @param array $args Optional arguments.
#//
def feed_links_extra(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"separator": _x("&raquo;", "feed link"), "singletitle": __("%1$s %2$s %3$s Comments Feed"), "cattitle": __("%1$s %2$s %3$s Category Feed"), "tagtitle": __("%1$s %2$s %3$s Tag Feed"), "taxtitle": __("%1$s %2$s %3$s %4$s Feed"), "authortitle": __("%1$s %2$s Posts by %3$s Feed"), "searchtitle": __("%1$s %2$s Search Results for &#8220;%3$s&#8221; Feed"), "posttypetitle": __("%1$s %2$s %3$s Feed")})
    args_ = wp_parse_args(args_, defaults_)
    if is_singular():
        id_ = 0
        post_ = get_post(id_)
        if comments_open() or pings_open() or post_.comment_count > 0:
            title_ = php_sprintf(args_["singletitle"], get_bloginfo("name"), args_["separator"], the_title_attribute(Array({"echo": False})))
            href_ = get_post_comments_feed_link(post_.ID)
        # end if
    elif is_post_type_archive():
        post_type_ = get_query_var("post_type")
        if php_is_array(post_type_):
            post_type_ = reset(post_type_)
        # end if
        post_type_obj_ = get_post_type_object(post_type_)
        title_ = php_sprintf(args_["posttypetitle"], get_bloginfo("name"), args_["separator"], post_type_obj_.labels.name)
        href_ = get_post_type_archive_feed_link(post_type_obj_.name)
    elif is_category():
        term_ = get_queried_object()
        if term_:
            title_ = php_sprintf(args_["cattitle"], get_bloginfo("name"), args_["separator"], term_.name)
            href_ = get_category_feed_link(term_.term_id)
        # end if
    elif is_tag():
        term_ = get_queried_object()
        if term_:
            title_ = php_sprintf(args_["tagtitle"], get_bloginfo("name"), args_["separator"], term_.name)
            href_ = get_tag_feed_link(term_.term_id)
        # end if
    elif is_tax():
        term_ = get_queried_object()
        if term_:
            tax_ = get_taxonomy(term_.taxonomy)
            title_ = php_sprintf(args_["taxtitle"], get_bloginfo("name"), args_["separator"], term_.name, tax_.labels.singular_name)
            href_ = get_term_feed_link(term_.term_id, term_.taxonomy)
        # end if
    elif is_author():
        author_id_ = php_intval(get_query_var("author"))
        title_ = php_sprintf(args_["authortitle"], get_bloginfo("name"), args_["separator"], get_the_author_meta("display_name", author_id_))
        href_ = get_author_feed_link(author_id_)
    elif is_search():
        title_ = php_sprintf(args_["searchtitle"], get_bloginfo("name"), args_["separator"], get_search_query(False))
        href_ = get_search_feed_link()
    # end if
    if (php_isset(lambda : title_)) and (php_isset(lambda : href_)):
        php_print("<link rel=\"alternate\" type=\"" + feed_content_type() + "\" title=\"" + esc_attr(title_) + "\" href=\"" + esc_url(href_) + "\" />" + "\n")
    # end if
# end def feed_links_extra
#// 
#// Display the link to the Really Simple Discovery service endpoint.
#// 
#// @link http://archipelago.phrasewise.com/rsd
#// @since 2.0.0
#//
def rsd_link(*_args_):
    
    
    php_print("<link rel=\"EditURI\" type=\"application/rsd+xml\" title=\"RSD\" href=\"" + esc_url(site_url("xmlrpc.php?rsd", "rpc")) + "\" />" + "\n")
# end def rsd_link
#// 
#// Display the link to the Windows Live Writer manifest file.
#// 
#// @link https://msdn.microsoft.com/en-us/library/bb463265.aspx
#// @since 2.3.1
#//
def wlwmanifest_link(*_args_):
    
    
    php_print("<link rel=\"wlwmanifest\" type=\"application/wlwmanifest+xml\" href=\"" + includes_url("wlwmanifest.xml") + "\" /> " + "\n")
# end def wlwmanifest_link
#// 
#// Displays a noindex meta tag if required by the blog configuration.
#// 
#// If a blog is marked as not being public then the noindex meta tag will be
#// output to tell web robots not to index the page content. Add this to the
#// {@see 'wp_head'} action.
#// 
#// Typical usage is as a {@see 'wp_head'} callback:
#// 
#// add_action( 'wp_head', 'noindex' );
#// 
#// @see wp_no_robots
#// 
#// @since 2.1.0
#//
def noindex(*_args_):
    
    
    #// If the blog is not public, tell robots to go away.
    if "0" == get_option("blog_public"):
        wp_no_robots()
    # end if
# end def noindex
#// 
#// Display a noindex meta tag.
#// 
#// Outputs a noindex meta tag that tells web robots not to index the page content.
#// Typical usage is as a {@see 'wp_head'} callback. add_action( 'wp_head', 'wp_no_robots' );
#// 
#// @since 3.3.0
#// @since 5.3.0 Echo "noindex,nofollow" if search engine visibility is discouraged.
#//
def wp_no_robots(*_args_):
    
    
    if get_option("blog_public"):
        php_print("<meta name='robots' content='noindex,follow' />\n")
        return
    # end if
    php_print("<meta name='robots' content='noindex,nofollow' />\n")
# end def wp_no_robots
#// 
#// Display a noindex,noarchive meta tag and referrer origin-when-cross-origin meta tag.
#// 
#// Outputs a noindex,noarchive meta tag that tells web robots not to index or cache the page content.
#// Outputs a referrer origin-when-cross-origin meta tag that tells the browser not to send the full
#// url as a referrer to other sites when cross-origin assets are loaded.
#// 
#// Typical usage is as a wp_head callback. add_action( 'wp_head', 'wp_sensitive_page_meta' );
#// 
#// @since 5.0.1
#//
def wp_sensitive_page_meta(*_args_):
    
    
    php_print(" <meta name='robots' content='noindex,noarchive' />\n    <meta name='referrer' content='strict-origin-when-cross-origin' />\n    ")
# end def wp_sensitive_page_meta
#// 
#// Display site icon meta tags.
#// 
#// @since 4.3.0
#// 
#// @link https://www.whatwg.org/specs/web-apps/current-work/multipage/links.html#rel-icon HTML5 specification link icon.
#//
def wp_site_icon(*_args_):
    
    
    if (not has_site_icon()) and (not is_customize_preview()):
        return
    # end if
    meta_tags_ = Array()
    icon_32_ = get_site_icon_url(32)
    if php_empty(lambda : icon_32_) and is_customize_preview():
        icon_32_ = "/favicon.ico"
        pass
    # end if
    if icon_32_:
        meta_tags_[-1] = php_sprintf("<link rel=\"icon\" href=\"%s\" sizes=\"32x32\" />", esc_url(icon_32_))
    # end if
    icon_192_ = get_site_icon_url(192)
    if icon_192_:
        meta_tags_[-1] = php_sprintf("<link rel=\"icon\" href=\"%s\" sizes=\"192x192\" />", esc_url(icon_192_))
    # end if
    icon_180_ = get_site_icon_url(180)
    if icon_180_:
        meta_tags_[-1] = php_sprintf("<link rel=\"apple-touch-icon\" href=\"%s\" />", esc_url(icon_180_))
    # end if
    icon_270_ = get_site_icon_url(270)
    if icon_270_:
        meta_tags_[-1] = php_sprintf("<meta name=\"msapplication-TileImage\" content=\"%s\" />", esc_url(icon_270_))
    # end if
    #// 
    #// Filters the site icon meta tags, so plugins can add their own.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string[] $meta_tags Array of Site Icon meta tags.
    #//
    meta_tags_ = apply_filters("site_icon_meta_tags", meta_tags_)
    meta_tags_ = php_array_filter(meta_tags_)
    for meta_tag_ in meta_tags_:
        php_print(str(meta_tag_) + str("\n"))
    # end for
# end def wp_site_icon
#// 
#// Prints resource hints to browsers for pre-fetching, pre-rendering
#// and pre-connecting to web sites.
#// 
#// Gives hints to browsers to prefetch specific pages or render them
#// in the background, to perform DNS lookups or to begin the connection
#// handshake (DNS, TCP, TLS) in the background.
#// 
#// These performance improving indicators work by using `<link rel"…">`.
#// 
#// @since 4.6.0
#//
def wp_resource_hints(*_args_):
    
    
    hints_ = Array({"dns-prefetch": wp_dependencies_unique_hosts(), "preconnect": Array(), "prefetch": Array(), "prerender": Array()})
    #// 
    #// Add DNS prefetch for the Emoji CDN.
    #// The path is removed in the foreach loop below.
    #// 
    #// This filter is documented in wp-includes/formatting.php
    hints_["dns-prefetch"][-1] = apply_filters("emoji_svg_url", "https://s.w.org/images/core/emoji/12.0.0-1/svg/")
    for relation_type_,urls_ in hints_:
        unique_urls_ = Array()
        #// 
        #// Filters domains and URLs for resource hints of relation type.
        #// 
        #// @since 4.6.0
        #// 
        #// @param array  $urls          URLs to print for resource hints.
        #// @param string $relation_type The relation type the URLs are printed for, e.g. 'preconnect' or 'prerender'.
        #//
        urls_ = apply_filters("wp_resource_hints", urls_, relation_type_)
        for key_,url_ in urls_:
            atts_ = Array()
            if php_is_array(url_):
                if (php_isset(lambda : url_["href"])):
                    atts_ = url_
                    url_ = url_["href"]
                else:
                    continue
                # end if
            # end if
            url_ = esc_url(url_, Array("http", "https"))
            if (not url_):
                continue
            # end if
            if (php_isset(lambda : unique_urls_[url_])):
                continue
            # end if
            if php_in_array(relation_type_, Array("preconnect", "dns-prefetch")):
                parsed_ = wp_parse_url(url_)
                if php_empty(lambda : parsed_["host"]):
                    continue
                # end if
                if "preconnect" == relation_type_ and (not php_empty(lambda : parsed_["scheme"])):
                    url_ = parsed_["scheme"] + "://" + parsed_["host"]
                else:
                    #// Use protocol-relative URLs for dns-prefetch or if scheme is missing.
                    url_ = "//" + parsed_["host"]
                # end if
            # end if
            atts_["rel"] = relation_type_
            atts_["href"] = url_
            unique_urls_[url_] = atts_
        # end for
        for atts_ in unique_urls_:
            html_ = ""
            for attr_,value_ in atts_:
                if (not is_scalar(value_)) or (not php_in_array(attr_, Array("as", "crossorigin", "href", "pr", "rel", "type"), True)) and (not php_is_numeric(attr_)):
                    continue
                # end if
                value_ = esc_url(value_) if "href" == attr_ else esc_attr(value_)
                if (not php_is_string(attr_)):
                    html_ += str(" ") + str(value_)
                else:
                    html_ += str(" ") + str(attr_) + str("='") + str(value_) + str("'")
                # end if
            # end for
            html_ = php_trim(html_)
            php_print(str("<link ") + str(html_) + str(" />\n"))
        # end for
    # end for
# end def wp_resource_hints
#// 
#// Retrieves a list of unique hosts of all enqueued scripts and styles.
#// 
#// @since 4.6.0
#// 
#// @return string[] A list of unique hosts of enqueued scripts and styles.
#//
def wp_dependencies_unique_hosts(*_args_):
    
    
    global wp_scripts_
    global wp_styles_
    php_check_if_defined("wp_scripts_","wp_styles_")
    unique_hosts_ = Array()
    for dependencies_ in Array(wp_scripts_, wp_styles_):
        if type(dependencies_).__name__ == "WP_Dependencies" and (not php_empty(lambda : dependencies_.queue)):
            for handle_ in dependencies_.queue:
                if (not (php_isset(lambda : dependencies_.registered[handle_]))):
                    continue
                # end if
                #// @var _WP_Dependency $dependency
                dependency_ = dependencies_.registered[handle_]
                parsed_ = wp_parse_url(dependency_.src)
                if (not php_empty(lambda : parsed_["host"])) and (not php_in_array(parsed_["host"], unique_hosts_)) and parsed_["host"] != PHP_SERVER["SERVER_NAME"]:
                    unique_hosts_[-1] = parsed_["host"]
                # end if
            # end for
        # end if
    # end for
    return unique_hosts_
# end def wp_dependencies_unique_hosts
#// 
#// Whether the user can access the visual editor.
#// 
#// Checks if the user can access the visual editor and that it's supported by the user's browser.
#// 
#// @since 2.0.0
#// 
#// @global bool $wp_rich_edit Whether the user can access the visual editor.
#// @global bool $is_gecko     Whether the browser is Gecko-based.
#// @global bool $is_opera     Whether the browser is Opera.
#// @global bool $is_safari    Whether the browser is Safari.
#// @global bool $is_chrome    Whether the browser is Chrome.
#// @global bool $is_IE        Whether the browser is Internet Explorer.
#// @global bool $is_edge      Whether the browser is Microsoft Edge.
#// 
#// @return bool True if the user can access the visual editor, false otherwise.
#//
def user_can_richedit(*_args_):
    
    
    global wp_rich_edit_
    global is_gecko_
    global is_opera_
    global is_safari_
    global is_chrome_
    global is_IE_
    global is_edge_
    php_check_if_defined("wp_rich_edit_","is_gecko_","is_opera_","is_safari_","is_chrome_","is_IE_","is_edge_")
    if (not (php_isset(lambda : wp_rich_edit_))):
        wp_rich_edit_ = False
        if get_user_option("rich_editing") == "true" or (not is_user_logged_in()):
            #// Default to 'true' for logged out users.
            if is_safari_:
                wp_rich_edit_ = (not wp_is_mobile()) or php_preg_match("!AppleWebKit/(\\d+)!", PHP_SERVER["HTTP_USER_AGENT"], match_) and php_intval(match_[1]) >= 534
            elif is_IE_:
                wp_rich_edit_ = php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Trident/7.0;") != False
            elif is_gecko_ or is_chrome_ or is_edge_ or is_opera_ and (not wp_is_mobile()):
                wp_rich_edit_ = True
            # end if
        # end if
    # end if
    #// 
    #// Filters whether the user can access the visual editor.
    #// 
    #// @since 2.1.0
    #// 
    #// @param bool $wp_rich_edit Whether the user can access the visual editor.
    #//
    return apply_filters("user_can_richedit", wp_rich_edit_)
# end def user_can_richedit
#// 
#// Find out which editor should be displayed by default.
#// 
#// Works out which of the two editors to display as the current editor for a
#// user. The 'html' setting is for the "Text" editor tab.
#// 
#// @since 2.5.0
#// 
#// @return string Either 'tinymce', or 'html', or 'test'
#//
def wp_default_editor(*_args_):
    
    
    r_ = "tinymce" if user_can_richedit() else "html"
    #// Defaults.
    if wp_get_current_user():
        #// Look for cookie.
        ed_ = get_user_setting("editor", "tinymce")
        r_ = ed_ if php_in_array(ed_, Array("tinymce", "html", "test")) else r_
    # end if
    #// 
    #// Filters which editor should be displayed by default.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $r Which editor should be displayed by default. Either 'tinymce', 'html', or 'test'.
    #//
    return apply_filters("wp_default_editor", r_)
# end def wp_default_editor
#// 
#// Renders an editor.
#// 
#// Using this function is the proper way to output all needed components for both TinyMCE and Quicktags.
#// _WP_Editors should not be used directly. See https://core.trac.wordpress.org/ticket/17144.
#// 
#// NOTE: Once initialized the TinyMCE editor cannot be safely moved in the DOM. For that reason
#// running wp_editor() inside of a meta box is not a good idea unless only Quicktags is used.
#// On the post edit screen several actions can be used to include additional editors
#// containing TinyMCE: 'edit_page_form', 'edit_form_advanced' and 'dbx_post_sidebar'.
#// See https://core.trac.wordpress.org/ticket/19173 for more information.
#// 
#// @see _WP_Editors::editor()
#// @see _WP_Editors::parse_settings()
#// @since 3.3.0
#// 
#// @param string $content   Initial content for the editor.
#// @param string $editor_id HTML ID attribute value for the textarea and TinyMCE.
#// Should not contain square brackets.
#// @param array  $settings  See _WP_Editors::parse_settings() for description.
#//
def wp_editor(content_=None, editor_id_=None, settings_=None, *_args_):
    if settings_ is None:
        settings_ = Array()
    # end if
    
    if (not php_class_exists("_WP_Editors", False)):
        php_include_file(ABSPATH + WPINC + "/class-wp-editor.php", once=False)
    # end if
    _WP_Editors.editor(content_, editor_id_, settings_)
# end def wp_editor
#// 
#// Outputs the editor scripts, stylesheets, and default settings.
#// 
#// The editor can be initialized when needed after page load.
#// See wp.editor.initialize() in wp-admin/js/editor.js for initialization options.
#// 
#// @uses _WP_Editors
#// @since 4.8.0
#//
def wp_enqueue_editor(*_args_):
    
    
    if (not php_class_exists("_WP_Editors", False)):
        php_include_file(ABSPATH + WPINC + "/class-wp-editor.php", once=False)
    # end if
    _WP_Editors.enqueue_default_editor()
# end def wp_enqueue_editor
#// 
#// Enqueue assets needed by the code editor for the given settings.
#// 
#// @since 4.9.0
#// 
#// @see wp_enqueue_editor()
#// @see wp_get_code_editor_settings();
#// @see _WP_Editors::parse_settings()
#// 
#// @param array $args {
#// Args.
#// 
#// @type string   $type       The MIME type of the file to be edited.
#// @type string   $file       Filename to be edited. Extension is used to sniff the type. Can be supplied as alternative to `$type` param.
#// @type WP_Theme $theme      Theme being edited when on theme editor.
#// @type string   $plugin     Plugin being edited when on plugin editor.
#// @type array    $codemirror Additional CodeMirror setting overrides.
#// @type array    $csslint    CSSLint rule overrides.
#// @type array    $jshint     JSHint rule overrides.
#// @type array    $htmlhint   JSHint rule overrides.
#// }
#// @return array|false Settings for the enqueued code editor, or false if the editor was not enqueued.
#//
def wp_enqueue_code_editor(args_=None, *_args_):
    
    
    if is_user_logged_in() and "false" == wp_get_current_user().syntax_highlighting:
        return False
    # end if
    settings_ = wp_get_code_editor_settings(args_)
    if php_empty(lambda : settings_) or php_empty(lambda : settings_["codemirror"]):
        return False
    # end if
    wp_enqueue_script("code-editor")
    wp_enqueue_style("code-editor")
    if (php_isset(lambda : settings_["codemirror"]["mode"])):
        mode_ = settings_["codemirror"]["mode"]
        if php_is_string(mode_):
            mode_ = Array({"name": mode_})
        # end if
        if (not php_empty(lambda : settings_["codemirror"]["lint"])):
            for case in Switch(mode_["name"]):
                if case("css"):
                    pass
                # end if
                if case("text/css"):
                    pass
                # end if
                if case("text/x-scss"):
                    pass
                # end if
                if case("text/x-less"):
                    wp_enqueue_script("csslint")
                    break
                # end if
                if case("htmlmixed"):
                    pass
                # end if
                if case("text/html"):
                    pass
                # end if
                if case("php"):
                    pass
                # end if
                if case("application/x-httpd-php"):
                    pass
                # end if
                if case("text/x-php"):
                    wp_enqueue_script("htmlhint")
                    wp_enqueue_script("csslint")
                    wp_enqueue_script("jshint")
                    if (not current_user_can("unfiltered_html")):
                        wp_enqueue_script("htmlhint-kses")
                    # end if
                    break
                # end if
                if case("javascript"):
                    pass
                # end if
                if case("application/ecmascript"):
                    pass
                # end if
                if case("application/json"):
                    pass
                # end if
                if case("application/javascript"):
                    pass
                # end if
                if case("application/ld+json"):
                    pass
                # end if
                if case("text/typescript"):
                    pass
                # end if
                if case("application/typescript"):
                    wp_enqueue_script("jshint")
                    wp_enqueue_script("jsonlint")
                    break
                # end if
            # end for
        # end if
    # end if
    wp_add_inline_script("code-editor", php_sprintf("jQuery.extend( wp.codeEditor.defaultSettings, %s );", wp_json_encode(settings_)))
    #// 
    #// Fires when scripts and styles are enqueued for the code editor.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $settings Settings for the enqueued code editor.
    #//
    do_action("wp_enqueue_code_editor", settings_)
    return settings_
# end def wp_enqueue_code_editor
#// 
#// Generate and return code editor settings.
#// 
#// @since 5.0.0
#// 
#// @see wp_enqueue_code_editor()
#// 
#// @param array $args {
#// Args.
#// 
#// @type string   $type       The MIME type of the file to be edited.
#// @type string   $file       Filename to be edited. Extension is used to sniff the type. Can be supplied as alternative to `$type` param.
#// @type WP_Theme $theme      Theme being edited when on theme editor.
#// @type string   $plugin     Plugin being edited when on plugin editor.
#// @type array    $codemirror Additional CodeMirror setting overrides.
#// @type array    $csslint    CSSLint rule overrides.
#// @type array    $jshint     JSHint rule overrides.
#// @type array    $htmlhint   JSHint rule overrides.
#// }
#// @return array|false Settings for the code editor.
#//
def wp_get_code_editor_settings(args_=None, *_args_):
    
    
    settings_ = Array({"codemirror": Array({"indentUnit": 4, "indentWithTabs": True, "inputStyle": "contenteditable", "lineNumbers": True, "lineWrapping": True, "styleActiveLine": True, "continueComments": True, "extraKeys": Array({"Ctrl-Space": "autocomplete", "Ctrl-/": "toggleComment", "Cmd-/": "toggleComment", "Alt-F": "findPersistent", "Ctrl-F": "findPersistent", "Cmd-F": "findPersistent"})}, {"direction": "ltr", "gutters": Array()})}, {"csslint": Array({"errors": True, "box-model": True, "display-property-grouping": True, "duplicate-properties": True, "known-properties": True, "outline-none": True})}, {"jshint": Array({"boss": True, "curly": True, "eqeqeq": True, "eqnull": True, "es3": True, "expr": True, "immed": True, "noarg": True, "nonbsp": True, "onevar": True, "quotmark": "single", "trailing": True, "undef": True, "unused": True, "browser": True, "globals": Array({"_": False, "Backbone": False, "jQuery": False, "JSON": False, "wp": False})})}, {"htmlhint": Array({"tagname-lowercase": True, "attr-lowercase": True, "attr-value-double-quotes": False, "doctype-first": False, "tag-pair": True, "spec-char-escape": True, "id-unique": True, "src-not-empty": True, "attr-no-duplication": True, "alt-require": True, "space-tab-mixed-disabled": "tab", "attr-unsafe-chars": True})})
    type_ = ""
    if (php_isset(lambda : args_["type"])):
        type_ = args_["type"]
        #// Remap MIME types to ones that CodeMirror modes will recognize.
        if "application/x-patch" == type_ or "text/x-patch" == type_:
            type_ = "text/x-diff"
        # end if
    elif (php_isset(lambda : args_["file"])) and False != php_strpos(php_basename(args_["file"]), "."):
        extension_ = php_strtolower(pathinfo(args_["file"], PATHINFO_EXTENSION))
        for exts_,mime_ in wp_get_mime_types():
            if php_preg_match("!^(" + exts_ + ")$!i", extension_):
                type_ = mime_
                break
            # end if
        # end for
        #// Supply any types that are not matched by wp_get_mime_types().
        if php_empty(lambda : type_):
            for case in Switch(extension_):
                if case("conf"):
                    type_ = "text/nginx"
                    break
                # end if
                if case("css"):
                    type_ = "text/css"
                    break
                # end if
                if case("diff"):
                    pass
                # end if
                if case("patch"):
                    type_ = "text/x-diff"
                    break
                # end if
                if case("html"):
                    pass
                # end if
                if case("htm"):
                    type_ = "text/html"
                    break
                # end if
                if case("http"):
                    type_ = "message/http"
                    break
                # end if
                if case("js"):
                    type_ = "text/javascript"
                    break
                # end if
                if case("json"):
                    type_ = "application/json"
                    break
                # end if
                if case("jsx"):
                    type_ = "text/jsx"
                    break
                # end if
                if case("less"):
                    type_ = "text/x-less"
                    break
                # end if
                if case("md"):
                    type_ = "text/x-gfm"
                    break
                # end if
                if case("php"):
                    pass
                # end if
                if case("phtml"):
                    pass
                # end if
                if case("php3"):
                    pass
                # end if
                if case("php4"):
                    pass
                # end if
                if case("php5"):
                    pass
                # end if
                if case("php7"):
                    pass
                # end if
                if case("phps"):
                    type_ = "application/x-httpd-php"
                    break
                # end if
                if case("scss"):
                    type_ = "text/x-scss"
                    break
                # end if
                if case("sass"):
                    type_ = "text/x-sass"
                    break
                # end if
                if case("sh"):
                    pass
                # end if
                if case("bash"):
                    type_ = "text/x-sh"
                    break
                # end if
                if case("sql"):
                    type_ = "text/x-sql"
                    break
                # end if
                if case("svg"):
                    type_ = "application/svg+xml"
                    break
                # end if
                if case("xml"):
                    type_ = "text/xml"
                    break
                # end if
                if case("yml"):
                    pass
                # end if
                if case("yaml"):
                    type_ = "text/x-yaml"
                    break
                # end if
                if case("txt"):
                    pass
                # end if
                if case():
                    type_ = "text/plain"
                    break
                # end if
            # end for
        # end if
    # end if
    if php_in_array(type_, Array("text/css", "text/x-scss", "text/x-less", "text/x-sass"), True):
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": type_, "lint": False, "autoCloseBrackets": True, "matchBrackets": True}))
    elif "text/x-diff" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "diff"}))
    elif "text/html" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "htmlmixed", "lint": True, "autoCloseBrackets": True, "autoCloseTags": True, "matchTags": Array({"bothTags": True})}))
        if (not current_user_can("unfiltered_html")):
            settings_["htmlhint"]["kses"] = wp_kses_allowed_html("post")
        # end if
    elif "text/x-gfm" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "gfm", "highlightFormatting": True}))
    elif "application/javascript" == type_ or "text/javascript" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "javascript", "lint": True, "autoCloseBrackets": True, "matchBrackets": True}))
    elif False != php_strpos(type_, "json"):
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": Array({"name": "javascript"})}, {"lint": True, "autoCloseBrackets": True, "matchBrackets": True}))
        if "application/ld+json" == type_:
            settings_["codemirror"]["mode"]["jsonld"] = True
        else:
            settings_["codemirror"]["mode"]["json"] = True
        # end if
    elif False != php_strpos(type_, "jsx"):
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "jsx", "autoCloseBrackets": True, "matchBrackets": True}))
    elif "text/x-markdown" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "markdown", "highlightFormatting": True}))
    elif "text/nginx" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "nginx"}))
    elif "application/x-httpd-php" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "php", "autoCloseBrackets": True, "autoCloseTags": True, "matchBrackets": True, "matchTags": Array({"bothTags": True})}))
    elif "text/x-sql" == type_ or "text/x-mysql" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "sql", "autoCloseBrackets": True, "matchBrackets": True}))
    elif False != php_strpos(type_, "xml"):
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "xml", "autoCloseBrackets": True, "autoCloseTags": True, "matchTags": Array({"bothTags": True})}))
    elif "text/x-yaml" == type_:
        settings_["codemirror"] = php_array_merge(settings_["codemirror"], Array({"mode": "yaml"}))
    else:
        settings_["codemirror"]["mode"] = type_
    # end if
    if (not php_empty(lambda : settings_["codemirror"]["lint"])):
        settings_["codemirror"]["gutters"][-1] = "CodeMirror-lint-markers"
    # end if
    #// Let settings supplied via args override any defaults.
    for key_,value_ in wp_array_slice_assoc(args_, Array("codemirror", "csslint", "jshint", "htmlhint")):
        settings_[key_] = php_array_merge(settings_[key_], value_)
    # end for
    #// 
    #// Filters settings that are passed into the code editor.
    #// 
    #// Returning a falsey value will disable the syntax-highlighting code editor.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $settings The array of settings passed to the code editor. A falsey value disables the editor.
    #// @param array $args {
    #// Args passed when calling `get_code_editor_settings()`.
    #// 
    #// @type string   $type       The MIME type of the file to be edited.
    #// @type string   $file       Filename being edited.
    #// @type WP_Theme $theme      Theme being edited when on theme editor.
    #// @type string   $plugin     Plugin being edited when on plugin editor.
    #// @type array    $codemirror Additional CodeMirror setting overrides.
    #// @type array    $csslint    CSSLint rule overrides.
    #// @type array    $jshint     JSHint rule overrides.
    #// @type array    $htmlhint   JSHint rule overrides.
    #// }
    #//
    return apply_filters("wp_code_editor_settings", settings_, args_)
# end def wp_get_code_editor_settings
#// 
#// Retrieves the contents of the search WordPress query variable.
#// 
#// The search query string is passed through esc_attr() to ensure that it is safe
#// for placing in an html attribute.
#// 
#// @since 2.3.0
#// 
#// @param bool $escaped Whether the result is escaped. Default true.
#// Only use when you are later escaping it. Do not use unescaped.
#// @return string
#//
def get_search_query(escaped_=None, *_args_):
    if escaped_ is None:
        escaped_ = True
    # end if
    
    #// 
    #// Filters the contents of the search query variable.
    #// 
    #// @since 2.3.0
    #// 
    #// @param mixed $search Contents of the search query variable.
    #//
    query_ = apply_filters("get_search_query", get_query_var("s"))
    if escaped_:
        query_ = esc_attr(query_)
    # end if
    return query_
# end def get_search_query
#// 
#// Displays the contents of the search query variable.
#// 
#// The search query string is passed through esc_attr() to ensure that it is safe
#// for placing in an html attribute.
#// 
#// @since 2.1.0
#//
def the_search_query(*_args_):
    
    
    #// 
    #// Filters the contents of the search query variable for display.
    #// 
    #// @since 2.3.0
    #// 
    #// @param mixed $search Contents of the search query variable.
    #//
    php_print(esc_attr(apply_filters("the_search_query", get_search_query(False))))
# end def the_search_query
#// 
#// Gets the language attributes for the html tag.
#// 
#// Builds up a set of html attributes containing the text direction and language
#// information for the page.
#// 
#// @since 4.3.0
#// 
#// @param string $doctype Optional. The type of html document. Accepts 'xhtml' or 'html'. Default 'html'.
#//
def get_language_attributes(doctype_="html", *_args_):
    
    
    attributes_ = Array()
    if php_function_exists("is_rtl") and is_rtl():
        attributes_[-1] = "dir=\"rtl\""
    # end if
    lang_ = get_bloginfo("language")
    if lang_:
        if "text/html" == get_option("html_type") or "html" == doctype_:
            attributes_[-1] = "lang=\"" + esc_attr(lang_) + "\""
        # end if
        if "text/html" != get_option("html_type") or "xhtml" == doctype_:
            attributes_[-1] = "xml:lang=\"" + esc_attr(lang_) + "\""
        # end if
    # end if
    output_ = php_implode(" ", attributes_)
    #// 
    #// Filters the language attributes for display in the html tag.
    #// 
    #// @since 2.5.0
    #// @since 4.3.0 Added the `$doctype` parameter.
    #// 
    #// @param string $output A space-separated list of language attributes.
    #// @param string $doctype The type of html document (xhtml|html).
    #//
    return apply_filters("language_attributes", output_, doctype_)
# end def get_language_attributes
#// 
#// Displays the language attributes for the html tag.
#// 
#// Builds up a set of html attributes containing the text direction and language
#// information for the page.
#// 
#// @since 2.1.0
#// @since 4.3.0 Converted into a wrapper for get_language_attributes().
#// 
#// @param string $doctype Optional. The type of html document. Accepts 'xhtml' or 'html'. Default 'html'.
#//
def language_attributes(doctype_="html", *_args_):
    
    
    php_print(get_language_attributes(doctype_))
# end def language_attributes
#// 
#// Retrieve paginated link for archive post pages.
#// 
#// Technically, the function can be used to create paginated link list for any
#// area. The 'base' argument is used to reference the url, which will be used to
#// create the paginated links. The 'format' argument is then used for replacing
#// the page number. It is however, most likely and by default, to be used on the
#// archive post pages.
#// 
#// The 'type' argument controls format of the returned value. The default is
#// 'plain', which is just a string with the links separated by a newline
#// character. The other possible values are either 'array' or 'list'. The
#// 'array' value will return an array of the paginated link list to offer full
#// control of display. The 'list' value will place all of the paginated links in
#// an unordered HTML list.
#// 
#// The 'total' argument is the total amount of pages and is an integer. The
#// 'current' argument is the current page number and is also an integer.
#// 
#// An example of the 'base' argument is "http://example.com/all_posts.php%_%"
#// and the '%_%' is required. The '%_%' will be replaced by the contents of in
#// the 'format' argument. An example for the 'format' argument is "?page=%#%"
#// and the '%#%' is also required. The '%#%' will be replaced with the page
#// number.
#// 
#// You can include the previous and next links in the list by setting the
#// 'prev_next' argument to true, which it is by default. You can set the
#// previous text, by using the 'prev_text' argument. You can set the next text
#// by setting the 'next_text' argument.
#// 
#// If the 'show_all' argument is set to true, then it will show all of the pages
#// instead of a short list of the pages near the current page. By default, the
#// 'show_all' is set to false and controlled by the 'end_size' and 'mid_size'
#// arguments. The 'end_size' argument is how many numbers on either the start
#// and the end list edges, by default is 1. The 'mid_size' argument is how many
#// numbers to either side of current page, but not including current page.
#// 
#// It is possible to add query vars to the link by using the 'add_args' argument
#// and see add_query_arg() for more information.
#// 
#// The 'before_page_number' and 'after_page_number' arguments allow users to
#// augment the links themselves. Typically this might be to add context to the
#// numbered links so that screen reader users understand what the links are for.
#// The text strings are added before and after the page number - within the
#// anchor tag.
#// 
#// @since 2.1.0
#// @since 4.9.0 Added the `aria_current` argument.
#// 
#// @global WP_Query   $wp_query   WordPress Query object.
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string|array $args {
#// Optional. Array or string of arguments for generating paginated links for archives.
#// 
#// @type string $base               Base of the paginated url. Default empty.
#// @type string $format             Format for the pagination structure. Default empty.
#// @type int    $total              The total amount of pages. Default is the value WP_Query's
#// `max_num_pages` or 1.
#// @type int    $current            The current page number. Default is 'paged' query var or 1.
#// @type string $aria_current       The value for the aria-current attribute. Possible values are 'page',
#// 'step', 'location', 'date', 'time', 'true', 'false'. Default is 'page'.
#// @type bool   $show_all           Whether to show all pages. Default false.
#// @type int    $end_size           How many numbers on either the start and the end list edges.
#// Default 1.
#// @type int    $mid_size           How many numbers to either side of the current pages. Default 2.
#// @type bool   $prev_next          Whether to include the previous and next links in the list. Default true.
#// @type bool   $prev_text          The previous page text. Default '&laquo; Previous'.
#// @type bool   $next_text          The next page text. Default 'Next &raquo;'.
#// @type string $type               Controls format of the returned value. Possible values are 'plain',
#// 'array' and 'list'. Default is 'plain'.
#// @type array  $add_args           An array of query args to add. Default false.
#// @type string $add_fragment       A string to append to each link. Default empty.
#// @type string $before_page_number A string to appear before the page number. Default empty.
#// @type string $after_page_number  A string to append after the page number. Default empty.
#// }
#// @return string|array|void String of page links or array of page links, depending on 'type' argument.
#// Void if total number of pages is less than 2.
#//
def paginate_links(args_="", *_args_):
    
    
    global wp_query_
    global wp_rewrite_
    php_check_if_defined("wp_query_","wp_rewrite_")
    #// Setting up default values based on the current URL.
    pagenum_link_ = html_entity_decode(get_pagenum_link())
    url_parts_ = php_explode("?", pagenum_link_)
    #// Get max pages and current page out of the current query, if available.
    total_ = wp_query_.max_num_pages if (php_isset(lambda : wp_query_.max_num_pages)) else 1
    current_ = php_intval(get_query_var("paged")) if get_query_var("paged") else 1
    #// Append the format placeholder to the base URL.
    pagenum_link_ = trailingslashit(url_parts_[0]) + "%_%"
    #// URL base depends on permalink settings.
    format_ = "index.php/" if wp_rewrite_.using_index_permalinks() and (not php_strpos(pagenum_link_, "index.php")) else ""
    format_ += user_trailingslashit(wp_rewrite_.pagination_base + "/%#%", "paged") if wp_rewrite_.using_permalinks() else "?paged=%#%"
    defaults_ = Array({"base": pagenum_link_, "format": format_, "total": total_, "current": current_, "aria_current": "page", "show_all": False, "prev_next": True, "prev_text": __("&laquo; Previous"), "next_text": __("Next &raquo;"), "end_size": 1, "mid_size": 2, "type": "plain", "add_args": Array(), "add_fragment": "", "before_page_number": "", "after_page_number": ""})
    args_ = wp_parse_args(args_, defaults_)
    if (not php_is_array(args_["add_args"])):
        args_["add_args"] = Array()
    # end if
    #// Merge additional query vars found in the original URL into 'add_args' array.
    if (php_isset(lambda : url_parts_[1])):
        #// Find the format argument.
        format_ = php_explode("?", php_str_replace("%_%", args_["format"], args_["base"]))
        format_query_ = format_[1] if (php_isset(lambda : format_[1])) else ""
        wp_parse_str(format_query_, format_args_)
        #// Find the query args of the requested URL.
        wp_parse_str(url_parts_[1], url_query_args_)
        #// Remove the format argument from the array of query arguments, to avoid overwriting custom format.
        for format_arg_,format_arg_value_ in format_args_:
            url_query_args_[format_arg_] = None
        # end for
        args_["add_args"] = php_array_merge(args_["add_args"], urlencode_deep(url_query_args_))
    # end if
    #// Who knows what else people pass in $args.
    total_ = php_int(args_["total"])
    if total_ < 2:
        return
    # end if
    current_ = php_int(args_["current"])
    end_size_ = php_int(args_["end_size"])
    #// Out of bounds? Make it the default.
    if end_size_ < 1:
        end_size_ = 1
    # end if
    mid_size_ = php_int(args_["mid_size"])
    if mid_size_ < 0:
        mid_size_ = 2
    # end if
    add_args_ = args_["add_args"]
    r_ = ""
    page_links_ = Array()
    dots_ = False
    if args_["prev_next"] and current_ and 1 < current_:
        link_ = php_str_replace("%_%", "" if 2 == current_ else args_["format"], args_["base"])
        link_ = php_str_replace("%#%", current_ - 1, link_)
        if add_args_:
            link_ = add_query_arg(add_args_, link_)
        # end if
        link_ += args_["add_fragment"]
        page_links_[-1] = php_sprintf("<a class=\"prev page-numbers\" href=\"%s\">%s</a>", esc_url(apply_filters("paginate_links", link_)), args_["prev_text"])
    # end if
    n_ = 1
    while n_ <= total_:
        
        if n_ == current_:
            page_links_[-1] = php_sprintf("<span aria-current=\"%s\" class=\"page-numbers current\">%s</span>", esc_attr(args_["aria_current"]), args_["before_page_number"] + number_format_i18n(n_) + args_["after_page_number"])
            dots_ = True
        else:
            if args_["show_all"] or n_ <= end_size_ or current_ and n_ >= current_ - mid_size_ and n_ <= current_ + mid_size_ or n_ > total_ - end_size_:
                link_ = php_str_replace("%_%", "" if 1 == n_ else args_["format"], args_["base"])
                link_ = php_str_replace("%#%", n_, link_)
                if add_args_:
                    link_ = add_query_arg(add_args_, link_)
                # end if
                link_ += args_["add_fragment"]
                page_links_[-1] = php_sprintf("<a class=\"page-numbers\" href=\"%s\">%s</a>", esc_url(apply_filters("paginate_links", link_)), args_["before_page_number"] + number_format_i18n(n_) + args_["after_page_number"])
                dots_ = True
            elif dots_ and (not args_["show_all"]):
                page_links_[-1] = "<span class=\"page-numbers dots\">" + __("&hellip;") + "</span>"
                dots_ = False
            # end if
        # end if
        n_ += 1
    # end while
    if args_["prev_next"] and current_ and current_ < total_:
        link_ = php_str_replace("%_%", args_["format"], args_["base"])
        link_ = php_str_replace("%#%", current_ + 1, link_)
        if add_args_:
            link_ = add_query_arg(add_args_, link_)
        # end if
        link_ += args_["add_fragment"]
        page_links_[-1] = php_sprintf("<a class=\"next page-numbers\" href=\"%s\">%s</a>", esc_url(apply_filters("paginate_links", link_)), args_["next_text"])
    # end if
    for case in Switch(args_["type"]):
        if case("array"):
            return page_links_
        # end if
        if case("list"):
            r_ += "<ul class='page-numbers'>\n  <li>"
            r_ += join("</li>\n <li>", page_links_)
            r_ += "</li>\n</ul>\n"
            break
        # end if
        if case():
            r_ = join("\n", page_links_)
            break
        # end if
    # end for
    return r_
# end def paginate_links
#// 
#// Registers an admin color scheme css file.
#// 
#// Allows a plugin to register a new admin color scheme. For example:
#// 
#// wp_admin_css_color( 'classic', __( 'Classic' ), admin_url( "css/colors-classic.css" ), array(
#// '#07273E', '#14568A', '#D54E21', '#2683AE'
#// ) );
#// 
#// @since 2.5.0
#// 
#// @global array $_wp_admin_css_colors
#// 
#// @param string $key    The unique key for this theme.
#// @param string $name   The name of the theme.
#// @param string $url    The URL of the CSS file containing the color scheme.
#// @param array  $colors Optional. An array of CSS color definition strings which are used
#// to give the user a feel for the theme.
#// @param array  $icons {
#// Optional. CSS color definitions used to color any SVG icons.
#// 
#// @type string $base    SVG icon base color.
#// @type string $focus   SVG icon color on focus.
#// @type string $current SVG icon color of current admin menu link.
#// }
#//
def wp_admin_css_color(key_=None, name_=None, url_=None, colors_=None, icons_=None, *_args_):
    if colors_ is None:
        colors_ = Array()
    # end if
    if icons_ is None:
        icons_ = Array()
    # end if
    
    global _wp_admin_css_colors_
    php_check_if_defined("_wp_admin_css_colors_")
    if (not (php_isset(lambda : _wp_admin_css_colors_))):
        _wp_admin_css_colors_ = Array()
    # end if
    _wp_admin_css_colors_[key_] = Array({"name": name_, "url": url_, "colors": colors_, "icon_colors": icons_})
# end def wp_admin_css_color
#// 
#// Registers the default admin color schemes.
#// 
#// Registers the initial set of eight color schemes in the Profile section
#// of the dashboard which allows for styling the admin menu and toolbar.
#// 
#// @see wp_admin_css_color()
#// 
#// @since 3.0.0
#//
def register_admin_color_schemes(*_args_):
    
    
    suffix_ = "-rtl" if is_rtl() else ""
    suffix_ += "" if SCRIPT_DEBUG else ".min"
    wp_admin_css_color("fresh", _x("Default", "admin color scheme"), False, Array("#222", "#333", "#0073aa", "#00a0d2"), Array({"base": "#a0a5aa", "focus": "#00a0d2", "current": "#fff"}))
    #// Other color schemes are not available when running out of src.
    if False != php_strpos(get_bloginfo("version"), "-src"):
        return
    # end if
    wp_admin_css_color("light", _x("Light", "admin color scheme"), admin_url(str("css/colors/light/colors") + str(suffix_) + str(".css")), Array("#e5e5e5", "#999", "#d64e07", "#04a4cc"), Array({"base": "#999", "focus": "#ccc", "current": "#ccc"}))
    wp_admin_css_color("blue", _x("Blue", "admin color scheme"), admin_url(str("css/colors/blue/colors") + str(suffix_) + str(".css")), Array("#096484", "#4796b3", "#52accc", "#74B6CE"), Array({"base": "#e5f8ff", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("midnight", _x("Midnight", "admin color scheme"), admin_url(str("css/colors/midnight/colors") + str(suffix_) + str(".css")), Array("#25282b", "#363b3f", "#69a8bb", "#e14d43"), Array({"base": "#f1f2f3", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("sunrise", _x("Sunrise", "admin color scheme"), admin_url(str("css/colors/sunrise/colors") + str(suffix_) + str(".css")), Array("#b43c38", "#cf4944", "#dd823b", "#ccaf0b"), Array({"base": "#f3f1f1", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("ectoplasm", _x("Ectoplasm", "admin color scheme"), admin_url(str("css/colors/ectoplasm/colors") + str(suffix_) + str(".css")), Array("#413256", "#523f6d", "#a3b745", "#d46f15"), Array({"base": "#ece6f6", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("ocean", _x("Ocean", "admin color scheme"), admin_url(str("css/colors/ocean/colors") + str(suffix_) + str(".css")), Array("#627c83", "#738e96", "#9ebaa0", "#aa9d88"), Array({"base": "#f2fcff", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("coffee", _x("Coffee", "admin color scheme"), admin_url(str("css/colors/coffee/colors") + str(suffix_) + str(".css")), Array("#46403c", "#59524c", "#c7a589", "#9ea476"), Array({"base": "#f3f2f1", "focus": "#fff", "current": "#fff"}))
# end def register_admin_color_schemes
#// 
#// Displays the URL of a WordPress admin CSS file.
#// 
#// @see WP_Styles::_css_href and its {@see 'style_loader_src'} filter.
#// 
#// @since 2.3.0
#// 
#// @param string $file file relative to wp-admin/ without its ".css" extension.
#// @return string
#//
def wp_admin_css_uri(file_="wp-admin", *_args_):
    
    
    if php_defined("WP_INSTALLING"):
        _file_ = str("./") + str(file_) + str(".css")
    else:
        _file_ = admin_url(str(file_) + str(".css"))
    # end if
    _file_ = add_query_arg("version", get_bloginfo("version"), _file_)
    #// 
    #// Filters the URI of a WordPress admin CSS file.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $_file Relative path to the file with query arguments attached.
    #// @param string $file  Relative path to the file, minus its ".css" extension.
    #//
    return apply_filters("wp_admin_css_uri", _file_, file_)
# end def wp_admin_css_uri
#// 
#// Enqueues or directly prints a stylesheet link to the specified CSS file.
#// 
#// "Intelligently" decides to enqueue or to print the CSS file. If the
#// {@see 'wp_print_styles'} action has *not* yet been called, the CSS file will be
#// enqueued. If the {@see 'wp_print_styles'} action has been called, the CSS link will
#// be printed. Printing may be forced by passing true as the $force_echo
#// (second) parameter.
#// 
#// For backward compatibility with WordPress 2.3 calling method: If the $file
#// (first) parameter does not correspond to a registered CSS file, we assume
#// $file is a file relative to wp-admin/ without its ".css" extension. A
#// stylesheet link to that generated URL is printed.
#// 
#// @since 2.3.0
#// 
#// @param string $file       Optional. Style handle name or file name (without ".css" extension) relative
#// to wp-admin/. Defaults to 'wp-admin'.
#// @param bool   $force_echo Optional. Force the stylesheet link to be printed rather than enqueued.
#//
def wp_admin_css(file_="wp-admin", force_echo_=None, *_args_):
    if force_echo_ is None:
        force_echo_ = False
    # end if
    
    #// For backward compatibility.
    handle_ = php_substr(file_, 4) if 0 == php_strpos(file_, "css/") else file_
    if wp_styles().query(handle_):
        if force_echo_ or did_action("wp_print_styles"):
            #// We already printed the style queue. Print this one immediately.
            wp_print_styles(handle_)
        else:
            #// Add to style queue.
            wp_enqueue_style(handle_)
        # end if
        return
    # end if
    stylesheet_link_ = php_sprintf("<link rel='stylesheet' href='%s' type='text/css' />\n", esc_url(wp_admin_css_uri(file_)))
    #// 
    #// Filters the stylesheet link to the specified CSS file.
    #// 
    #// If the site is set to display right-to-left, the RTL stylesheet link
    #// will be used instead.
    #// 
    #// @since 2.3.0
    #// @param string $stylesheet_link HTML link element for the stylesheet.
    #// @param string $file            Style handle name or filename (without ".css" extension)
    #// relative to wp-admin/. Defaults to 'wp-admin'.
    #//
    php_print(apply_filters("wp_admin_css", stylesheet_link_, file_))
    if php_function_exists("is_rtl") and is_rtl():
        rtl_stylesheet_link_ = php_sprintf("<link rel='stylesheet' href='%s' type='text/css' />\n", esc_url(wp_admin_css_uri(str(file_) + str("-rtl"))))
        #// This filter is documented in wp-includes/general-template.php
        php_print(apply_filters("wp_admin_css", rtl_stylesheet_link_, str(file_) + str("-rtl")))
    # end if
# end def wp_admin_css
#// 
#// Enqueues the default ThickBox js and css.
#// 
#// If any of the settings need to be changed, this can be done with another js
#// file similar to media-upload.js. That file should
#// require array('thickbox') to ensure it is loaded after.
#// 
#// @since 2.5.0
#//
def add_thickbox(*_args_):
    
    
    wp_enqueue_script("thickbox")
    wp_enqueue_style("thickbox")
    if is_network_admin():
        add_action("admin_head", "_thickbox_path_admin_subfolder")
    # end if
# end def add_thickbox
#// 
#// Displays the XHTML generator that is generated on the wp_head hook.
#// 
#// See {@see 'wp_head'}.
#// 
#// @since 2.5.0
#//
def wp_generator(*_args_):
    
    
    #// 
    #// Filters the output of the XHTML generator tag.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $generator_type The XHTML generator.
    #//
    the_generator(apply_filters("wp_generator_type", "xhtml"))
# end def wp_generator
#// 
#// Display the generator XML or Comment for RSS, ATOM, etc.
#// 
#// Returns the correct generator type for the requested output format. Allows
#// for a plugin to filter generators overall the {@see 'the_generator'} filter.
#// 
#// @since 2.5.0
#// 
#// @param string $type The type of generator to output - (html|xhtml|atom|rss2|rdf|comment|export).
#//
def the_generator(type_=None, *_args_):
    
    
    #// 
    #// Filters the output of the XHTML generator tag for display.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $generator_type The generator output.
    #// @param string $type           The type of generator to output. Accepts 'html',
    #// 'xhtml', 'atom', 'rss2', 'rdf', 'comment', 'export'.
    #//
    php_print(apply_filters("the_generator", get_the_generator(type_), type_) + "\n")
# end def the_generator
#// 
#// Creates the generator XML or Comment for RSS, ATOM, etc.
#// 
#// Returns the correct generator type for the requested output format. Allows
#// for a plugin to filter generators on an individual basis using the
#// {@see 'get_the_generator_$type'} filter.
#// 
#// @since 2.5.0
#// 
#// @param string $type The type of generator to return - (html|xhtml|atom|rss2|rdf|comment|export).
#// @return string|void The HTML content for the generator.
#//
def get_the_generator(type_="", *_args_):
    
    
    if php_empty(lambda : type_):
        current_filter_ = current_filter()
        if php_empty(lambda : current_filter_):
            return
        # end if
        for case in Switch(current_filter_):
            if case("rss2_head"):
                pass
            # end if
            if case("commentsrss2_head"):
                type_ = "rss2"
                break
            # end if
            if case("rss_head"):
                pass
            # end if
            if case("opml_head"):
                type_ = "comment"
                break
            # end if
            if case("rdf_header"):
                type_ = "rdf"
                break
            # end if
            if case("atom_head"):
                pass
            # end if
            if case("comments_atom_head"):
                pass
            # end if
            if case("app_head"):
                type_ = "atom"
                break
            # end if
        # end for
    # end if
    for case in Switch(type_):
        if case("html"):
            gen_ = "<meta name=\"generator\" content=\"WordPress " + esc_attr(get_bloginfo("version")) + "\">"
            break
        # end if
        if case("xhtml"):
            gen_ = "<meta name=\"generator\" content=\"WordPress " + esc_attr(get_bloginfo("version")) + "\" />"
            break
        # end if
        if case("atom"):
            gen_ = "<generator uri=\"https://wordpress.org/\" version=\"" + esc_attr(get_bloginfo_rss("version")) + "\">WordPress</generator>"
            break
        # end if
        if case("rss2"):
            gen_ = "<generator>" + esc_url_raw("https://wordpress.org/?v=" + get_bloginfo_rss("version")) + "</generator>"
            break
        # end if
        if case("rdf"):
            gen_ = "<admin:generatorAgent rdf:resource=\"" + esc_url_raw("https://wordpress.org/?v=" + get_bloginfo_rss("version")) + "\" />"
            break
        # end if
        if case("comment"):
            gen_ = "<!-- generator=\"WordPress/" + esc_attr(get_bloginfo("version")) + "\" -->"
            break
        # end if
        if case("export"):
            gen_ = "<!-- generator=\"WordPress/" + esc_attr(get_bloginfo_rss("version")) + "\" created=\"" + gmdate("Y-m-d H:i") + "\" -->"
            break
        # end if
    # end for
    #// 
    #// Filters the HTML for the retrieved generator type.
    #// 
    #// The dynamic portion of the hook name, `$type`, refers to the generator type.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $gen  The HTML markup output to wp_head().
    #// @param string $type The type of generator. Accepts 'html', 'xhtml', 'atom',
    #// 'rss2', 'rdf', 'comment', 'export'.
    #//
    return apply_filters(str("get_the_generator_") + str(type_), gen_, type_)
# end def get_the_generator
#// 
#// Outputs the html checked attribute.
#// 
#// Compares the first two arguments and if identical marks as checked
#// 
#// @since 1.0.0
#// 
#// @param mixed $checked One of the values to compare
#// @param mixed $current (true) The other value to compare if not just true
#// @param bool  $echo    Whether to echo or just return the string
#// @return string html attribute or empty string
#//
def checked(checked_=None, current_=None, echo_=None, *_args_):
    if current_ is None:
        current_ = True
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    return __checked_selected_helper(checked_, current_, echo_, "checked")
# end def checked
#// 
#// Outputs the html selected attribute.
#// 
#// Compares the first two arguments and if identical marks as selected
#// 
#// @since 1.0.0
#// 
#// @param mixed $selected One of the values to compare
#// @param mixed $current  (true) The other value to compare if not just true
#// @param bool  $echo     Whether to echo or just return the string
#// @return string html attribute or empty string
#//
def selected(selected_=None, current_=None, echo_=None, *_args_):
    if current_ is None:
        current_ = True
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    return __checked_selected_helper(selected_, current_, echo_, "selected")
# end def selected
#// 
#// Outputs the html disabled attribute.
#// 
#// Compares the first two arguments and if identical marks as disabled
#// 
#// @since 3.0.0
#// 
#// @param mixed $disabled One of the values to compare
#// @param mixed $current  (true) The other value to compare if not just true
#// @param bool  $echo     Whether to echo or just return the string
#// @return string html attribute or empty string
#//
def disabled(disabled_=None, current_=None, echo_=None, *_args_):
    if current_ is None:
        current_ = True
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    return __checked_selected_helper(disabled_, current_, echo_, "disabled")
# end def disabled
#// 
#// Outputs the html readonly attribute.
#// 
#// Compares the first two arguments and if identical marks as readonly
#// 
#// @since 4.9.0
#// 
#// @param mixed $readonly One of the values to compare
#// @param mixed $current  (true) The other value to compare if not just true
#// @param bool  $echo     Whether to echo or just return the string
#// @return string html attribute or empty string
#//
def readonly(readonly_=None, current_=None, echo_=None, *_args_):
    if current_ is None:
        current_ = True
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    return __checked_selected_helper(readonly_, current_, echo_, "readonly")
# end def readonly
#// 
#// Private helper function for checked, selected, disabled and readonly.
#// 
#// Compares the first two arguments and if identical marks as $type
#// 
#// @since 2.8.0
#// @access private
#// 
#// @param mixed  $helper  One of the values to compare
#// @param mixed  $current (true) The other value to compare if not just true
#// @param bool   $echo    Whether to echo or just return the string
#// @param string $type    The type of checked|selected|disabled|readonly we are doing
#// @return string html attribute or empty string
#//
def __checked_selected_helper(helper_=None, current_=None, echo_=None, type_=None, *_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    if php_str(helper_) == php_str(current_):
        result_ = str(" ") + str(type_) + str("='") + str(type_) + str("'")
    else:
        result_ = ""
    # end if
    if echo_:
        php_print(result_)
    # end if
    return result_
# end def __checked_selected_helper
#// 
#// Default settings for heartbeat
#// 
#// Outputs the nonce used in the heartbeat XHR
#// 
#// @since 3.6.0
#// 
#// @param array $settings
#// @return array $settings
#//
def wp_heartbeat_settings(settings_=None, *_args_):
    
    
    if (not is_admin()):
        settings_["ajaxurl"] = admin_url("admin-ajax.php", "relative")
    # end if
    if is_user_logged_in():
        settings_["nonce"] = wp_create_nonce("heartbeat-nonce")
    # end if
    return settings_
# end def wp_heartbeat_settings
