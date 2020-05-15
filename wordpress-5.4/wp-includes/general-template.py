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
def get_header(name=None, *args_):
    
    #// 
    #// Fires before the header template file is loaded.
    #// 
    #// @since 2.1.0
    #// @since 2.8.0 $name parameter added.
    #// 
    #// @param string|null $name Name of the specific header file to use. null for the default header.
    #//
    do_action("get_header", name)
    templates = Array()
    name = str(name)
    if "" != name:
        templates[-1] = str("header-") + str(name) + str(".php")
    # end if
    templates[-1] = "header.php"
    locate_template(templates, True)
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
def get_footer(name=None, *args_):
    
    #// 
    #// Fires before the footer template file is loaded.
    #// 
    #// @since 2.1.0
    #// @since 2.8.0 $name parameter added.
    #// 
    #// @param string|null $name Name of the specific footer file to use. null for the default footer.
    #//
    do_action("get_footer", name)
    templates = Array()
    name = str(name)
    if "" != name:
        templates[-1] = str("footer-") + str(name) + str(".php")
    # end if
    templates[-1] = "footer.php"
    locate_template(templates, True)
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
def get_sidebar(name=None, *args_):
    
    #// 
    #// Fires before the sidebar template file is loaded.
    #// 
    #// @since 2.2.0
    #// @since 2.8.0 $name parameter added.
    #// 
    #// @param string|null $name Name of the specific sidebar file to use. null for the default sidebar.
    #//
    do_action("get_sidebar", name)
    templates = Array()
    name = str(name)
    if "" != name:
        templates[-1] = str("sidebar-") + str(name) + str(".php")
    # end if
    templates[-1] = "sidebar.php"
    locate_template(templates, True)
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
def get_template_part(slug=None, name=None, *args_):
    
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
    do_action(str("get_template_part_") + str(slug), slug, name)
    templates = Array()
    name = str(name)
    if "" != name:
        templates[-1] = str(slug) + str("-") + str(name) + str(".php")
    # end if
    templates[-1] = str(slug) + str(".php")
    #// 
    #// Fires before a template part is loaded.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string   $slug      The slug name for the generic template.
    #// @param string   $name      The name of the specialized template.
    #// @param string[] $templates Array of template files to search for, in order.
    #//
    do_action("get_template_part", slug, name, templates)
    locate_template(templates, True, False)
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
def get_search_form(args=Array(), *args_):
    
    #// 
    #// Fires before the search form is retrieved, at the start of get_search_form().
    #// 
    #// @since 2.7.0 as 'get_search_form' action.
    #// @since 3.6.0
    #// 
    #// @link https://core.trac.wordpress.org/ticket/19321
    #//
    do_action("pre_get_search_form")
    echo = True
    if (not php_is_array(args)):
        #// 
        #// Back compat: to ensure previous uses of get_search_form() continue to
        #// function as expected, we handle a value for the boolean $echo param removed
        #// in 5.2.0. Then we deal with the $args array and cast its defaults.
        #//
        echo = bool(args)
        #// Set an empty array and allow default arguments to take over.
        args = Array()
    # end if
    #// Defaults are to echo and to output no custom label on the form.
    defaults = Array({"echo": echo, "aria_label": ""})
    args = wp_parse_args(args, defaults)
    #// 
    #// Filters the array of arguments used when generating the search form.
    #// 
    #// @since 5.2.0
    #// 
    #// @param array $args The array of arguments for building the search form.
    #//
    args = apply_filters("search_form_args", args)
    format = "html5" if current_theme_supports("html5", "search-form") else "xhtml"
    #// 
    #// Filters the HTML format of the search form.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $format The type of markup to use in the search form.
    #// Accepts 'html5', 'xhtml'.
    #//
    format = apply_filters("search_form_format", format)
    search_form_template = locate_template("searchform.php")
    if "" != search_form_template:
        ob_start()
        php_include_file(search_form_template, once=False)
        form = ob_get_clean()
    else:
        #// Build a string containing an aria-label to use for the search form.
        if (php_isset(lambda : args["aria_label"])) and args["aria_label"]:
            aria_label = "aria-label=\"" + esc_attr(args["aria_label"]) + "\" "
        else:
            #// 
            #// If there's no custom aria-label, we can set a default here. At the
            #// moment it's empty as there's uncertainty about what the default should be.
            #//
            aria_label = ""
        # end if
        if "html5" == format:
            form = "<form role=\"search\" " + aria_label + "method=\"get\" class=\"search-form\" action=\"" + esc_url(home_url("/")) + "\">\n               <label>\n                   <span class=\"screen-reader-text\">" + _x("Search for:", "label") + "</span>\n                  <input type=\"search\" class=\"search-field\" placeholder=\"" + esc_attr_x("Search &hellip;", "placeholder") + "\" value=\"" + get_search_query() + "\" name=\"s\" />\n             </label>\n              <input type=\"submit\" class=\"search-submit\" value=\"" + esc_attr_x("Search", "submit button") + "\" />\n         </form>"
        else:
            form = "<form role=\"search\" " + aria_label + "method=\"get\" id=\"searchform\" class=\"searchform\" action=\"" + esc_url(home_url("/")) + "\">\n              <div>\n                 <label class=\"screen-reader-text\" for=\"s\">" + _x("Search for:", "label") + "</label>\n                  <input type=\"text\" value=\"" + get_search_query() + "\" name=\"s\" id=\"s\" />\n                  <input type=\"submit\" id=\"searchsubmit\" value=\"" + esc_attr_x("Search", "submit button") + "\" />\n             </div>\n            </form>"
        # end if
    # end if
    #// 
    #// Filters the HTML output of the search form.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $form The search form HTML output.
    #//
    result = apply_filters("get_search_form", form)
    if None == result:
        result = form
    # end if
    if args["echo"]:
        php_print(result)
    else:
        return result
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
def wp_loginout(redirect="", echo=True, *args_):
    
    if (not is_user_logged_in()):
        link = "<a href=\"" + esc_url(wp_login_url(redirect)) + "\">" + __("Log in") + "</a>"
    else:
        link = "<a href=\"" + esc_url(wp_logout_url(redirect)) + "\">" + __("Log out") + "</a>"
    # end if
    if echo:
        #// 
        #// Filters the HTML output for the Log In/Log Out link.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string $link The HTML link content.
        #//
        php_print(apply_filters("loginout", link))
    else:
        #// This filter is documented in wp-includes/general-template.php
        return apply_filters("loginout", link)
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
def wp_logout_url(redirect="", *args_):
    
    args = Array()
    if (not php_empty(lambda : redirect)):
        args["redirect_to"] = urlencode(redirect)
    # end if
    logout_url = add_query_arg(args, site_url("wp-login.php?action=logout", "login"))
    logout_url = wp_nonce_url(logout_url, "log-out")
    #// 
    #// Filters the logout URL.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $logout_url The HTML-encoded logout URL.
    #// @param string $redirect   Path to redirect to on logout.
    #//
    return apply_filters("logout_url", logout_url, redirect)
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
def wp_login_url(redirect="", force_reauth=False, *args_):
    
    login_url = site_url("wp-login.php", "login")
    if (not php_empty(lambda : redirect)):
        login_url = add_query_arg("redirect_to", urlencode(redirect), login_url)
    # end if
    if force_reauth:
        login_url = add_query_arg("reauth", "1", login_url)
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
    return apply_filters("login_url", login_url, redirect, force_reauth)
# end def wp_login_url
#// 
#// Returns the URL that allows the user to register on the site.
#// 
#// @since 3.6.0
#// 
#// @return string User registration URL.
#//
def wp_registration_url(*args_):
    
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
def wp_login_form(args=Array(), *args_):
    
    defaults = Array({"echo": True, "redirect": "https://" if is_ssl() else "http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"], "form_id": "loginform", "label_username": __("Username or Email Address"), "label_password": __("Password"), "label_remember": __("Remember Me"), "label_log_in": __("Log In"), "id_username": "user_login", "id_password": "user_pass", "id_remember": "rememberme", "id_submit": "wp-submit", "remember": True, "value_username": "", "value_remember": False})
    #// 
    #// Filters the default login form output arguments.
    #// 
    #// @since 3.0.0
    #// 
    #// @see wp_login_form()
    #// 
    #// @param array $defaults An array of default login form arguments.
    #//
    args = wp_parse_args(args, apply_filters("login_form_defaults", defaults))
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
    login_form_top = apply_filters("login_form_top", "", args)
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
    login_form_middle = apply_filters("login_form_middle", "", args)
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
    login_form_bottom = apply_filters("login_form_bottom", "", args)
    form = "\n      <form name=\"" + args["form_id"] + "\" id=\"" + args["form_id"] + "\" action=\"" + esc_url(site_url("wp-login.php", "login_post")) + "\" method=\"post\">\n         " + login_form_top + "\n            <p class=\"login-username\">\n              <label for=\"" + esc_attr(args["id_username"]) + "\">" + esc_html(args["label_username"]) + "</label>\n             <input type=\"text\" name=\"log\" id=\"" + esc_attr(args["id_username"]) + "\" class=\"input\" value=\"" + esc_attr(args["value_username"]) + """\" size=\"20\" />
    </p>
    <p class=\"login-password\">
    <label for=\"""" + esc_attr(args["id_password"]) + "\">" + esc_html(args["label_password"]) + "</label>\n               <input type=\"password\" name=\"pwd\" id=\"" + esc_attr(args["id_password"]) + "\" class=\"input\" value=\"\" size=\"20\" />\n          </p>\n          " + login_form_middle + "\n         " + "<p class=\"login-remember\"><label><input name=\"rememberme\" type=\"checkbox\" id=\"" + esc_attr(args["id_remember"]) + "\" value=\"forever\"" + " checked=\"checked\"" if args["value_remember"] else "" + " /> " + esc_html(args["label_remember"]) + "</label></p>" if args["remember"] else "" + "\n          <p class=\"login-submit\">\n                <input type=\"submit\" name=\"wp-submit\" id=\"" + esc_attr(args["id_submit"]) + "\" class=\"button button-primary\" value=\"" + esc_attr(args["label_log_in"]) + "\" />\n              <input type=\"hidden\" name=\"redirect_to\" value=\"" + esc_url(args["redirect"]) + "\" />\n            </p>\n          " + login_form_bottom + "\n     </form>"
    if args["echo"]:
        php_print(form)
    else:
        return form
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
def wp_lostpassword_url(redirect="", *args_):
    
    args = Array()
    if (not php_empty(lambda : redirect)):
        args["redirect_to"] = urlencode(redirect)
    # end if
    lostpassword_url = add_query_arg(args, network_site_url("wp-login.php?action=lostpassword", "login"))
    #// 
    #// Filters the Lost Password URL.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $lostpassword_url The lost password page URL.
    #// @param string $redirect         The path to redirect to on login.
    #//
    return apply_filters("lostpassword_url", lostpassword_url, redirect)
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
def wp_register(before="<li>", after="</li>", echo=True, *args_):
    
    if (not is_user_logged_in()):
        if get_option("users_can_register"):
            link = before + "<a href=\"" + esc_url(wp_registration_url()) + "\">" + __("Register") + "</a>" + after
        else:
            link = ""
        # end if
    elif current_user_can("read"):
        link = before + "<a href=\"" + admin_url() + "\">" + __("Site Admin") + "</a>" + after
    else:
        link = ""
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
    link = apply_filters("register", link)
    if echo:
        php_print(link)
    else:
        return link
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
def wp_meta(*args_):
    
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
def bloginfo(show="", *args_):
    
    php_print(get_bloginfo(show, "display"))
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
def get_bloginfo(show="", filter="raw", *args_):
    
    for case in Switch(show):
        if case("home"):
            pass
        # end if
        if case("siteurl"):
            #// Deprecated.
            _deprecated_argument(__FUNCTION__, "2.2.0", php_sprintf(__("The %1$s option is deprecated for the family of %2$s functions. Use the %3$s option instead."), "<code>" + show + "</code>", "<code>bloginfo()</code>", "<code>url</code>"))
        # end if
        if case("url"):
            output = home_url()
            break
        # end if
        if case("wpurl"):
            output = site_url()
            break
        # end if
        if case("description"):
            output = get_option("blogdescription")
            break
        # end if
        if case("rdf_url"):
            output = get_feed_link("rdf")
            break
        # end if
        if case("rss_url"):
            output = get_feed_link("rss")
            break
        # end if
        if case("rss2_url"):
            output = get_feed_link("rss2")
            break
        # end if
        if case("atom_url"):
            output = get_feed_link("atom")
            break
        # end if
        if case("comments_atom_url"):
            output = get_feed_link("comments_atom")
            break
        # end if
        if case("comments_rss2_url"):
            output = get_feed_link("comments_rss2")
            break
        # end if
        if case("pingback_url"):
            output = site_url("xmlrpc.php")
            break
        # end if
        if case("stylesheet_url"):
            output = get_stylesheet_uri()
            break
        # end if
        if case("stylesheet_directory"):
            output = get_stylesheet_directory_uri()
            break
        # end if
        if case("template_directory"):
            pass
        # end if
        if case("template_url"):
            output = get_template_directory_uri()
            break
        # end if
        if case("admin_email"):
            output = get_option("admin_email")
            break
        # end if
        if case("charset"):
            output = get_option("blog_charset")
            if "" == output:
                output = "UTF-8"
            # end if
            break
        # end if
        if case("html_type"):
            output = get_option("html_type")
            break
        # end if
        if case("version"):
            global wp_version
            php_check_if_defined("wp_version")
            output = wp_version
            break
        # end if
        if case("language"):
            #// 
            #// translators: Translate this to the correct language tag for your locale,
            #// see https://www.w3.org/International/articles/language-tags/ for reference.
            #// Do not translate into your own language.
            #//
            output = __("html_lang_attribute")
            if "html_lang_attribute" == output or php_preg_match("/[^a-zA-Z0-9-]/", output):
                output = determine_locale()
                output = php_str_replace("_", "-", output)
            # end if
            break
        # end if
        if case("text_direction"):
            _deprecated_argument(__FUNCTION__, "2.2.0", php_sprintf(__("The %1$s option is deprecated for the family of %2$s functions. Use the %3$s function instead."), "<code>" + show + "</code>", "<code>bloginfo()</code>", "<code>is_rtl()</code>"))
            if php_function_exists("is_rtl"):
                output = "rtl" if is_rtl() else "ltr"
            else:
                output = "ltr"
            # end if
            break
        # end if
        if case("name"):
            pass
        # end if
        if case():
            output = get_option("blogname")
            break
        # end if
    # end for
    url = True
    if php_strpos(show, "url") == False and php_strpos(show, "directory") == False and php_strpos(show, "home") == False:
        url = False
    # end if
    if "display" == filter:
        if url:
            #// 
            #// Filters the URL returned by get_bloginfo().
            #// 
            #// @since 2.0.5
            #// 
            #// @param string $output The URL returned by bloginfo().
            #// @param string $show   Type of information requested.
            #//
            output = apply_filters("bloginfo_url", output, show)
        else:
            #// 
            #// Filters the site information returned by get_bloginfo().
            #// 
            #// @since 0.71
            #// 
            #// @param mixed  $output The requested non-URL site information.
            #// @param string $show   Type of information requested.
            #//
            output = apply_filters("bloginfo", output, show)
        # end if
    # end if
    return output
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
def get_site_icon_url(size=512, url="", blog_id=0, *args_):
    
    switched_blog = False
    if is_multisite() and (not php_empty(lambda : blog_id)) and get_current_blog_id() != int(blog_id):
        switch_to_blog(blog_id)
        switched_blog = True
    # end if
    site_icon_id = get_option("site_icon")
    if site_icon_id:
        if size >= 512:
            size_data = "full"
        else:
            size_data = Array(size, size)
        # end if
        url = wp_get_attachment_image_url(site_icon_id, size_data)
    # end if
    if switched_blog:
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
    return apply_filters("get_site_icon_url", url, size, blog_id)
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
def site_icon_url(size=512, url="", blog_id=0, *args_):
    
    php_print(esc_url(get_site_icon_url(size, url, blog_id)))
# end def site_icon_url
#// 
#// Whether the site has a Site Icon.
#// 
#// @since 4.3.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default current blog.
#// @return bool Whether the site has a site icon or not.
#//
def has_site_icon(blog_id=0, *args_):
    
    return bool(get_site_icon_url(512, "", blog_id))
# end def has_site_icon
#// 
#// Determines whether the site has a custom logo.
#// 
#// @since 4.5.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default is the ID of the current blog.
#// @return bool Whether the site has a custom logo or not.
#//
def has_custom_logo(blog_id=0, *args_):
    
    switched_blog = False
    if is_multisite() and (not php_empty(lambda : blog_id)) and get_current_blog_id() != int(blog_id):
        switch_to_blog(blog_id)
        switched_blog = True
    # end if
    custom_logo_id = get_theme_mod("custom_logo")
    if switched_blog:
        restore_current_blog()
    # end if
    return bool(custom_logo_id)
# end def has_custom_logo
#// 
#// Returns a custom logo, linked to home.
#// 
#// @since 4.5.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default is the ID of the current blog.
#// @return string Custom logo markup.
#//
def get_custom_logo(blog_id=0, *args_):
    
    html = ""
    switched_blog = False
    if is_multisite() and (not php_empty(lambda : blog_id)) and get_current_blog_id() != int(blog_id):
        switch_to_blog(blog_id)
        switched_blog = True
    # end if
    custom_logo_id = get_theme_mod("custom_logo")
    #// We have a logo. Logo is go.
    if custom_logo_id:
        custom_logo_attr = Array({"class": "custom-logo"})
        #// 
        #// If the logo alt attribute is empty, get the site title and explicitly
        #// pass it to the attributes used by wp_get_attachment_image().
        #//
        image_alt = get_post_meta(custom_logo_id, "_wp_attachment_image_alt", True)
        if php_empty(lambda : image_alt):
            custom_logo_attr["alt"] = get_bloginfo("name", "display")
        # end if
        #// 
        #// If the alt attribute is not empty, there's no need to explicitly pass
        #// it because wp_get_attachment_image() already adds the alt attribute.
        #//
        html = php_sprintf("<a href=\"%1$s\" class=\"custom-logo-link\" rel=\"home\">%2$s</a>", esc_url(home_url("/")), wp_get_attachment_image(custom_logo_id, "full", False, custom_logo_attr))
    elif is_customize_preview():
        #// If no logo is set but we're in the Customizer, leave a placeholder (needed for the live preview).
        html = php_sprintf("<a href=\"%1$s\" class=\"custom-logo-link\" style=\"display:none;\"><img class=\"custom-logo\"/></a>", esc_url(home_url("/")))
    # end if
    if switched_blog:
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
    return apply_filters("get_custom_logo", html, blog_id)
# end def get_custom_logo
#// 
#// Displays a custom logo, linked to home.
#// 
#// @since 4.5.0
#// 
#// @param int $blog_id Optional. ID of the blog in question. Default is the ID of the current blog.
#//
def the_custom_logo(blog_id=0, *args_):
    
    php_print(get_custom_logo(blog_id))
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
def wp_get_document_title(*args_):
    
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
    title = apply_filters("pre_get_document_title", "")
    if (not php_empty(lambda : title)):
        return title
    # end if
    global page,paged
    php_check_if_defined("page","paged")
    title = Array({"title": ""})
    #// If it's a 404 page, use a "Page not found" title.
    if is_404():
        title["title"] = __("Page not found")
        pass
    elif is_search():
        #// translators: %s: Search query.
        title["title"] = php_sprintf(__("Search Results for &#8220;%s&#8221;"), get_search_query())
        pass
    elif is_front_page():
        title["title"] = get_bloginfo("name", "display")
        pass
    elif is_post_type_archive():
        title["title"] = post_type_archive_title("", False)
        pass
    elif is_tax():
        title["title"] = single_term_title("", False)
        pass
    elif is_home() or is_singular():
        title["title"] = single_post_title("", False)
        pass
    elif is_category() or is_tag():
        title["title"] = single_term_title("", False)
        pass
    elif is_author() and get_queried_object():
        author = get_queried_object()
        title["title"] = author.display_name
        pass
    elif is_year():
        title["title"] = get_the_date(_x("Y", "yearly archives date format"))
    elif is_month():
        title["title"] = get_the_date(_x("F Y", "monthly archives date format"))
    elif is_day():
        title["title"] = get_the_date()
    # end if
    #// Add a page number if necessary.
    if paged >= 2 or page >= 2 and (not is_404()):
        #// translators: %s: Page number.
        title["page"] = php_sprintf(__("Page %s"), php_max(paged, page))
    # end if
    #// Append the description or site title to give context.
    if is_front_page():
        title["tagline"] = get_bloginfo("description", "display")
    else:
        title["site"] = get_bloginfo("name", "display")
    # end if
    #// 
    #// Filters the separator for the document title.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $sep Document title separator. Default '-'.
    #//
    sep = apply_filters("document_title_separator", "-")
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
    title = apply_filters("document_title_parts", title)
    title = php_implode(str(" ") + str(sep) + str(" "), php_array_filter(title))
    title = wptexturize(title)
    title = convert_chars(title)
    title = esc_html(title)
    title = capital_P_dangit(title)
    return title
# end def wp_get_document_title
#// 
#// Displays title tag with content.
#// 
#// @ignore
#// @since 4.1.0
#// @since 4.4.0 Improved title output replaced `wp_title()`.
#// @access private
#//
def _wp_render_title_tag(*args_):
    
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
def wp_title(sep="&raquo;", display=True, seplocation="", *args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    m = get_query_var("m")
    year = get_query_var("year")
    monthnum = get_query_var("monthnum")
    day = get_query_var("day")
    search = get_query_var("s")
    title = ""
    t_sep = "%WP_TITLE_SEP%"
    #// Temporary separator, for accurate flipping, if necessary.
    #// If there is a post.
    if is_single() or is_home() and (not is_front_page()) or is_page() and (not is_front_page()):
        title = single_post_title("", False)
    # end if
    #// If there's a post type archive.
    if is_post_type_archive():
        post_type = get_query_var("post_type")
        if php_is_array(post_type):
            post_type = reset(post_type)
        # end if
        post_type_object = get_post_type_object(post_type)
        if (not post_type_object.has_archive):
            title = post_type_archive_title("", False)
        # end if
    # end if
    #// If there's a category or tag.
    if is_category() or is_tag():
        title = single_term_title("", False)
    # end if
    #// If there's a taxonomy.
    if is_tax():
        term = get_queried_object()
        if term:
            tax = get_taxonomy(term.taxonomy)
            title = single_term_title(tax.labels.name + t_sep, False)
        # end if
    # end if
    #// If there's an author.
    if is_author() and (not is_post_type_archive()):
        author = get_queried_object()
        if author:
            title = author.display_name
        # end if
    # end if
    #// Post type archives with has_archive should override terms.
    if is_post_type_archive() and post_type_object.has_archive:
        title = post_type_archive_title("", False)
    # end if
    #// If there's a month.
    if is_archive() and (not php_empty(lambda : m)):
        my_year = php_substr(m, 0, 4)
        my_month = wp_locale.get_month(php_substr(m, 4, 2))
        my_day = php_intval(php_substr(m, 6, 2))
        title = my_year + t_sep + my_month if my_month else "" + t_sep + my_day if my_day else ""
    # end if
    #// If there's a year.
    if is_archive() and (not php_empty(lambda : year)):
        title = year
        if (not php_empty(lambda : monthnum)):
            title += t_sep + wp_locale.get_month(monthnum)
        # end if
        if (not php_empty(lambda : day)):
            title += t_sep + zeroise(day, 2)
        # end if
    # end if
    #// If it's a search.
    if is_search():
        #// translators: 1: Separator, 2: Search query.
        title = php_sprintf(__("Search Results %1$s %2$s"), t_sep, strip_tags(search))
    # end if
    #// If it's a 404 page.
    if is_404():
        title = __("Page not found")
    # end if
    prefix = ""
    if (not php_empty(lambda : title)):
        prefix = str(" ") + str(sep) + str(" ")
    # end if
    #// 
    #// Filters the parts of the page title.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string[] $title_array Array of parts of the page title.
    #//
    title_array = apply_filters("wp_title_parts", php_explode(t_sep, title))
    #// Determines position of the separator and direction of the breadcrumb.
    if "right" == seplocation:
        #// Separator on right, so reverse the order.
        title_array = array_reverse(title_array)
        title = php_implode(str(" ") + str(sep) + str(" "), title_array) + prefix
    else:
        title = prefix + php_implode(str(" ") + str(sep) + str(" "), title_array)
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
    title = apply_filters("wp_title", title, sep, seplocation)
    #// Send it out.
    if display:
        php_print(title)
    else:
        return title
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
def single_post_title(prefix="", display=True, *args_):
    
    _post = get_queried_object()
    if (not (php_isset(lambda : _post.post_title))):
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
    title = apply_filters("single_post_title", _post.post_title, _post)
    if display:
        php_print(prefix + title)
    else:
        return prefix + title
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
def post_type_archive_title(prefix="", display=True, *args_):
    
    if (not is_post_type_archive()):
        return
    # end if
    post_type = get_query_var("post_type")
    if php_is_array(post_type):
        post_type = reset(post_type)
    # end if
    post_type_obj = get_post_type_object(post_type)
    #// 
    #// Filters the post type archive title.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $post_type_name Post type 'name' label.
    #// @param string $post_type      Post type.
    #//
    title = apply_filters("post_type_archive_title", post_type_obj.labels.name, post_type)
    if display:
        php_print(prefix + title)
    else:
        return prefix + title
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
def single_cat_title(prefix="", display=True, *args_):
    
    return single_term_title(prefix, display)
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
def single_tag_title(prefix="", display=True, *args_):
    
    return single_term_title(prefix, display)
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
def single_term_title(prefix="", display=True, *args_):
    
    term = get_queried_object()
    if (not term):
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
        term_name = apply_filters("single_cat_title", term.name)
    elif is_tag():
        #// 
        #// Filters the tag archive page title.
        #// 
        #// @since 2.3.0
        #// 
        #// @param string $term_name Tag name for archive being displayed.
        #//
        term_name = apply_filters("single_tag_title", term.name)
    elif is_tax():
        #// 
        #// Filters the custom taxonomy archive page title.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $term_name Term name for archive being displayed.
        #//
        term_name = apply_filters("single_term_title", term.name)
    else:
        return
    # end if
    if php_empty(lambda : term_name):
        return
    # end if
    if display:
        php_print(prefix + term_name)
    else:
        return prefix + term_name
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
def single_month_title(prefix="", display=True, *args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    m = get_query_var("m")
    year = get_query_var("year")
    monthnum = get_query_var("monthnum")
    if (not php_empty(lambda : monthnum)) and (not php_empty(lambda : year)):
        my_year = year
        my_month = wp_locale.get_month(monthnum)
    elif (not php_empty(lambda : m)):
        my_year = php_substr(m, 0, 4)
        my_month = wp_locale.get_month(php_substr(m, 4, 2))
    # end if
    if php_empty(lambda : my_month):
        return False
    # end if
    result = prefix + my_month + prefix + my_year
    if (not display):
        return result
    # end if
    php_print(result)
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
def the_archive_title(before="", after="", *args_):
    
    title = get_the_archive_title()
    if (not php_empty(lambda : title)):
        php_print(before + title + after)
    # end if
# end def the_archive_title
#// 
#// Retrieve the archive title based on the queried object.
#// 
#// @since 4.1.0
#// 
#// @return string Archive title.
#//
def get_the_archive_title(*args_):
    
    title = __("Archives")
    if is_category():
        #// translators: Category archive title. %s: Category name.
        title = php_sprintf(__("Category: %s"), single_cat_title("", False))
    elif is_tag():
        #// translators: Tag archive title. %s: Tag name.
        title = php_sprintf(__("Tag: %s"), single_tag_title("", False))
    elif is_author():
        #// translators: Author archive title. %s: Author name.
        title = php_sprintf(__("Author: %s"), "<span class=\"vcard\">" + get_the_author() + "</span>")
    elif is_year():
        #// translators: Yearly archive title. %s: Year.
        title = php_sprintf(__("Year: %s"), get_the_date(_x("Y", "yearly archives date format")))
    elif is_month():
        #// translators: Monthly archive title. %s: Month name and year.
        title = php_sprintf(__("Month: %s"), get_the_date(_x("F Y", "monthly archives date format")))
    elif is_day():
        #// translators: Daily archive title. %s: Date.
        title = php_sprintf(__("Day: %s"), get_the_date(_x("F j, Y", "daily archives date format")))
    elif is_tax("post_format"):
        if is_tax("post_format", "post-format-aside"):
            title = _x("Asides", "post format archive title")
        elif is_tax("post_format", "post-format-gallery"):
            title = _x("Galleries", "post format archive title")
        elif is_tax("post_format", "post-format-image"):
            title = _x("Images", "post format archive title")
        elif is_tax("post_format", "post-format-video"):
            title = _x("Videos", "post format archive title")
        elif is_tax("post_format", "post-format-quote"):
            title = _x("Quotes", "post format archive title")
        elif is_tax("post_format", "post-format-link"):
            title = _x("Links", "post format archive title")
        elif is_tax("post_format", "post-format-status"):
            title = _x("Statuses", "post format archive title")
        elif is_tax("post_format", "post-format-audio"):
            title = _x("Audio", "post format archive title")
        elif is_tax("post_format", "post-format-chat"):
            title = _x("Chats", "post format archive title")
        # end if
    elif is_post_type_archive():
        #// translators: Post type archive title. %s: Post type name.
        title = php_sprintf(__("Archives: %s"), post_type_archive_title("", False))
    elif is_tax():
        queried_object = get_queried_object()
        if queried_object:
            tax = get_taxonomy(queried_object.taxonomy)
            #// translators: Taxonomy term archive title. 1: Taxonomy singular name, 2: Current taxonomy term.
            title = php_sprintf(__("%1$s: %2$s"), tax.labels.singular_name, single_term_title("", False))
        # end if
    # end if
    #// 
    #// Filters the archive title.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $title Archive title to be displayed.
    #//
    return apply_filters("get_the_archive_title", title)
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
def the_archive_description(before="", after="", *args_):
    
    description = get_the_archive_description()
    if description:
        php_print(before + description + after)
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
def get_the_archive_description(*args_):
    
    if is_author():
        description = get_the_author_meta("description")
    elif is_post_type_archive():
        description = get_the_post_type_description()
    else:
        description = term_description()
    # end if
    #// 
    #// Filters the archive description.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $description Archive description to be displayed.
    #//
    return apply_filters("get_the_archive_description", description)
# end def get_the_archive_description
#// 
#// Retrieves the description for a post type archive.
#// 
#// @since 4.9.0
#// 
#// @return string The post type description.
#//
def get_the_post_type_description(*args_):
    
    post_type = get_query_var("post_type")
    if php_is_array(post_type):
        post_type = reset(post_type)
    # end if
    post_type_obj = get_post_type_object(post_type)
    #// Check if a description is set.
    if (php_isset(lambda : post_type_obj.description)):
        description = post_type_obj.description
    else:
        description = ""
    # end if
    #// 
    #// Filters the description for a post type archive.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string       $description   The post type description.
    #// @param WP_Post_Type $post_type_obj The post type object.
    #//
    return apply_filters("get_the_post_type_description", description, post_type_obj)
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
def get_archives_link(url=None, text=None, format="html", before="", after="", selected=False, *args_):
    
    text = wptexturize(text)
    url = esc_url(url)
    aria_current = " aria-current=\"page\"" if selected else ""
    if "link" == format:
        link_html = "   <link rel='archives' title='" + esc_attr(text) + str("' href='") + str(url) + str("' />\n")
    elif "option" == format:
        selected_attr = " selected='selected'" if selected else ""
        link_html = str("   <option value='") + str(url) + str("'") + str(selected_attr) + str(">") + str(before) + str(" ") + str(text) + str(" ") + str(after) + str("</option>\n")
    elif "html" == format:
        link_html = str("   <li>") + str(before) + str("<a href='") + str(url) + str("'") + str(aria_current) + str(">") + str(text) + str("</a>") + str(after) + str("</li>\n")
    else:
        #// Custom.
        link_html = str("   ") + str(before) + str("<a href='") + str(url) + str("'") + str(aria_current) + str(">") + str(text) + str("</a>") + str(after) + str("\n")
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
    return apply_filters("get_archives_link", link_html, url, text, format, before, after, selected)
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
def wp_get_archives(args="", *args_):
    
    global wpdb,wp_locale
    php_check_if_defined("wpdb","wp_locale")
    defaults = Array({"type": "monthly", "limit": "", "format": "html", "before": "", "after": "", "show_post_count": False, "echo": 1, "order": "DESC", "post_type": "post", "year": get_query_var("year"), "monthnum": get_query_var("monthnum"), "day": get_query_var("day"), "w": get_query_var("w")})
    parsed_args = wp_parse_args(args, defaults)
    post_type_object = get_post_type_object(parsed_args["post_type"])
    if (not is_post_type_viewable(post_type_object)):
        return
    # end if
    parsed_args["post_type"] = post_type_object.name
    if "" == parsed_args["type"]:
        parsed_args["type"] = "monthly"
    # end if
    if (not php_empty(lambda : parsed_args["limit"])):
        parsed_args["limit"] = absint(parsed_args["limit"])
        parsed_args["limit"] = " LIMIT " + parsed_args["limit"]
    # end if
    order = php_strtoupper(parsed_args["order"])
    if "ASC" != order:
        order = "DESC"
    # end if
    #// This is what will separate dates on weekly archive links.
    archive_week_separator = "&#8211;"
    sql_where = wpdb.prepare("WHERE post_type = %s AND post_status = 'publish'", parsed_args["post_type"])
    #// 
    #// Filters the SQL WHERE clause for retrieving archives.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $sql_where   Portion of SQL query containing the WHERE clause.
    #// @param array  $parsed_args An array of default arguments.
    #//
    where = apply_filters("getarchives_where", sql_where, parsed_args)
    #// 
    #// Filters the SQL JOIN clause for retrieving archives.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $sql_join    Portion of SQL query containing JOIN clause.
    #// @param array  $parsed_args An array of default arguments.
    #//
    join = apply_filters("getarchives_join", "", parsed_args)
    output = ""
    last_changed = wp_cache_get_last_changed("posts")
    limit = parsed_args["limit"]
    if "monthly" == parsed_args["type"]:
        query = str("SELECT YEAR(post_date) AS `year`, MONTH(post_date) AS `month`, count(ID) as posts FROM ") + str(wpdb.posts) + str(" ") + str(join) + str(" ") + str(where) + str(" GROUP BY YEAR(post_date), MONTH(post_date) ORDER BY post_date ") + str(order) + str(" ") + str(limit)
        key = php_md5(query)
        key = str("wp_get_archives:") + str(key) + str(":") + str(last_changed)
        results = wp_cache_get(key, "posts")
        if (not results):
            results = wpdb.get_results(query)
            wp_cache_set(key, results, "posts")
        # end if
        if results:
            after = parsed_args["after"]
            for result in results:
                url = get_month_link(result.year, result.month)
                if "post" != parsed_args["post_type"]:
                    url = add_query_arg("post_type", parsed_args["post_type"], url)
                # end if
                #// translators: 1: Month name, 2: 4-digit year.
                text = php_sprintf(__("%1$s %2$d"), wp_locale.get_month(result.month), result.year)
                if parsed_args["show_post_count"]:
                    parsed_args["after"] = "&nbsp;(" + result.posts + ")" + after
                # end if
                selected = is_archive() and str(parsed_args["year"]) == result.year and str(parsed_args["monthnum"]) == result.month
                output += get_archives_link(url, text, parsed_args["format"], parsed_args["before"], parsed_args["after"], selected)
            # end for
        # end if
    elif "yearly" == parsed_args["type"]:
        query = str("SELECT YEAR(post_date) AS `year`, count(ID) as posts FROM ") + str(wpdb.posts) + str(" ") + str(join) + str(" ") + str(where) + str(" GROUP BY YEAR(post_date) ORDER BY post_date ") + str(order) + str(" ") + str(limit)
        key = php_md5(query)
        key = str("wp_get_archives:") + str(key) + str(":") + str(last_changed)
        results = wp_cache_get(key, "posts")
        if (not results):
            results = wpdb.get_results(query)
            wp_cache_set(key, results, "posts")
        # end if
        if results:
            after = parsed_args["after"]
            for result in results:
                url = get_year_link(result.year)
                if "post" != parsed_args["post_type"]:
                    url = add_query_arg("post_type", parsed_args["post_type"], url)
                # end if
                text = php_sprintf("%d", result.year)
                if parsed_args["show_post_count"]:
                    parsed_args["after"] = "&nbsp;(" + result.posts + ")" + after
                # end if
                selected = is_archive() and str(parsed_args["year"]) == result.year
                output += get_archives_link(url, text, parsed_args["format"], parsed_args["before"], parsed_args["after"], selected)
            # end for
        # end if
    elif "daily" == parsed_args["type"]:
        query = str("SELECT YEAR(post_date) AS `year`, MONTH(post_date) AS `month`, DAYOFMONTH(post_date) AS `dayofmonth`, count(ID) as posts FROM ") + str(wpdb.posts) + str(" ") + str(join) + str(" ") + str(where) + str(" GROUP BY YEAR(post_date), MONTH(post_date), DAYOFMONTH(post_date) ORDER BY post_date ") + str(order) + str(" ") + str(limit)
        key = php_md5(query)
        key = str("wp_get_archives:") + str(key) + str(":") + str(last_changed)
        results = wp_cache_get(key, "posts")
        if (not results):
            results = wpdb.get_results(query)
            wp_cache_set(key, results, "posts")
        # end if
        if results:
            after = parsed_args["after"]
            for result in results:
                url = get_day_link(result.year, result.month, result.dayofmonth)
                if "post" != parsed_args["post_type"]:
                    url = add_query_arg("post_type", parsed_args["post_type"], url)
                # end if
                date = php_sprintf("%1$d-%2$02d-%3$02d 00:00:00", result.year, result.month, result.dayofmonth)
                text = mysql2date(get_option("date_format"), date)
                if parsed_args["show_post_count"]:
                    parsed_args["after"] = "&nbsp;(" + result.posts + ")" + after
                # end if
                selected = is_archive() and str(parsed_args["year"]) == result.year and str(parsed_args["monthnum"]) == result.month and str(parsed_args["day"]) == result.dayofmonth
                output += get_archives_link(url, text, parsed_args["format"], parsed_args["before"], parsed_args["after"], selected)
            # end for
        # end if
    elif "weekly" == parsed_args["type"]:
        week = _wp_mysql_week("`post_date`")
        query = str("SELECT DISTINCT ") + str(week) + str(" AS `week`, YEAR( `post_date` ) AS `yr`, DATE_FORMAT( `post_date`, '%Y-%m-%d' ) AS `yyyymmdd`, count( `ID` ) AS `posts` FROM `") + str(wpdb.posts) + str("` ") + str(join) + str(" ") + str(where) + str(" GROUP BY ") + str(week) + str(", YEAR( `post_date` ) ORDER BY `post_date` ") + str(order) + str(" ") + str(limit)
        key = php_md5(query)
        key = str("wp_get_archives:") + str(key) + str(":") + str(last_changed)
        results = wp_cache_get(key, "posts")
        if (not results):
            results = wpdb.get_results(query)
            wp_cache_set(key, results, "posts")
        # end if
        arc_w_last = ""
        if results:
            after = parsed_args["after"]
            for result in results:
                if result.week != arc_w_last:
                    arc_year = result.yr
                    arc_w_last = result.week
                    arc_week = get_weekstartend(result.yyyymmdd, get_option("start_of_week"))
                    arc_week_start = date_i18n(get_option("date_format"), arc_week["start"])
                    arc_week_end = date_i18n(get_option("date_format"), arc_week["end"])
                    url = add_query_arg(Array({"m": arc_year, "w": result.week}), home_url("/"))
                    if "post" != parsed_args["post_type"]:
                        url = add_query_arg("post_type", parsed_args["post_type"], url)
                    # end if
                    text = arc_week_start + archive_week_separator + arc_week_end
                    if parsed_args["show_post_count"]:
                        parsed_args["after"] = "&nbsp;(" + result.posts + ")" + after
                    # end if
                    selected = is_archive() and str(parsed_args["year"]) == result.yr and str(parsed_args["w"]) == result.week
                    output += get_archives_link(url, text, parsed_args["format"], parsed_args["before"], parsed_args["after"], selected)
                # end if
            # end for
        # end if
    elif "postbypost" == parsed_args["type"] or "alpha" == parsed_args["type"]:
        orderby = "post_title ASC " if "alpha" == parsed_args["type"] else "post_date DESC, ID DESC "
        query = str("SELECT * FROM ") + str(wpdb.posts) + str(" ") + str(join) + str(" ") + str(where) + str(" ORDER BY ") + str(orderby) + str(" ") + str(limit)
        key = php_md5(query)
        key = str("wp_get_archives:") + str(key) + str(":") + str(last_changed)
        results = wp_cache_get(key, "posts")
        if (not results):
            results = wpdb.get_results(query)
            wp_cache_set(key, results, "posts")
        # end if
        if results:
            for result in results:
                if "0000-00-00 00:00:00" != result.post_date:
                    url = get_permalink(result)
                    if result.post_title:
                        #// This filter is documented in wp-includes/post-template.php
                        text = strip_tags(apply_filters("the_title", result.post_title, result.ID))
                    else:
                        text = result.ID
                    # end if
                    selected = get_the_ID() == result.ID
                    output += get_archives_link(url, text, parsed_args["format"], parsed_args["before"], parsed_args["after"], selected)
                # end if
            # end for
        # end if
    # end if
    if parsed_args["echo"]:
        php_print(output)
    else:
        return output
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
def calendar_week_mod(num=None, *args_):
    
    base = 7
    return num - base * floor(num / base)
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
def get_calendar(initial=True, echo=True, *args_):
    
    global wpdb,m,monthnum,year,wp_locale,posts
    php_check_if_defined("wpdb","m","monthnum","year","wp_locale","posts")
    key = php_md5(m + monthnum + year)
    cache = wp_cache_get("get_calendar", "calendar")
    if cache and php_is_array(cache) and (php_isset(lambda : cache[key])):
        #// This filter is documented in wp-includes/general-template.php
        output = apply_filters("get_calendar", cache[key])
        if echo:
            php_print(output)
            return
        # end if
        return output
    # end if
    if (not php_is_array(cache)):
        cache = Array()
    # end if
    #// Quick check. If we have no posts at all, abort!
    if (not posts):
        gotsome = wpdb.get_var(str("SELECT 1 as test FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'post' AND post_status = 'publish' LIMIT 1"))
        if (not gotsome):
            cache[key] = ""
            wp_cache_set("get_calendar", cache, "calendar")
            return
        # end if
    # end if
    if (php_isset(lambda : PHP_REQUEST["w"])):
        w = int(PHP_REQUEST["w"])
    # end if
    #// week_begins = 0 stands for Sunday.
    week_begins = int(get_option("start_of_week"))
    #// Let's figure out when we are.
    if (not php_empty(lambda : monthnum)) and (not php_empty(lambda : year)):
        thismonth = zeroise(php_intval(monthnum), 2)
        thisyear = int(year)
    elif (not php_empty(lambda : w)):
        #// We need to get the month from MySQL.
        thisyear = int(php_substr(m, 0, 4))
        #// It seems MySQL's weeks disagree with PHP's.
        d = w - 1 * 7 + 6
        thismonth = wpdb.get_var(str("SELECT DATE_FORMAT((DATE_ADD('") + str(thisyear) + str("0101', INTERVAL ") + str(d) + str(" DAY) ), '%m')"))
    elif (not php_empty(lambda : m)):
        thisyear = int(php_substr(m, 0, 4))
        if php_strlen(m) < 6:
            thismonth = "01"
        else:
            thismonth = zeroise(int(php_substr(m, 4, 2)), 2)
        # end if
    else:
        thisyear = current_time("Y")
        thismonth = current_time("m")
    # end if
    unixmonth = mktime(0, 0, 0, thismonth, 1, thisyear)
    last_day = gmdate("t", unixmonth)
    #// Get the next and previous month and year with at least one post.
    previous = wpdb.get_row(str("SELECT MONTH(post_date) AS month, YEAR(post_date) AS year\n        FROM ") + str(wpdb.posts) + str("\n     WHERE post_date < '") + str(thisyear) + str("-") + str(thismonth) + str("""-01'\n       AND post_type = 'post' AND post_status = 'publish'\n            ORDER BY post_date DESC\n           LIMIT 1"""))
    next = wpdb.get_row(str("SELECT MONTH(post_date) AS month, YEAR(post_date) AS year\n        FROM ") + str(wpdb.posts) + str("\n     WHERE post_date > '") + str(thisyear) + str("-") + str(thismonth) + str("-") + str(last_day) + str(""" 23:59:59'\n      AND post_type = 'post' AND post_status = 'publish'\n            ORDER BY post_date ASC\n            LIMIT 1"""))
    #// translators: Calendar caption: 1: Month name, 2: 4-digit year.
    calendar_caption = _x("%1$s %2$s", "calendar caption")
    calendar_output = "<table id=\"wp-calendar\" class=\"wp-calendar-table\">\n <caption>" + php_sprintf(calendar_caption, wp_locale.get_month(thismonth), gmdate("Y", unixmonth)) + "</caption>\n  <thead>\n   <tr>"
    myweek = Array()
    wdcount = 0
    while wdcount <= 6:
        
        myweek[-1] = wp_locale.get_weekday(wdcount + week_begins % 7)
        wdcount += 1
    # end while
    for wd in myweek:
        day_name = wp_locale.get_weekday_initial(wd) if initial else wp_locale.get_weekday_abbrev(wd)
        wd = esc_attr(wd)
        calendar_output += str("\n      <th scope=\"col\" title=\"") + str(wd) + str("\">") + str(day_name) + str("</th>")
    # end for
    calendar_output += """
    </tr>
    </thead>
    <tbody>
    <tr>"""
    daywithpost = Array()
    #// Get days with posts.
    dayswithposts = wpdb.get_results(str("SELECT DISTINCT DAYOFMONTH(post_date)\n       FROM ") + str(wpdb.posts) + str(" WHERE post_date >= '") + str(thisyear) + str("-") + str(thismonth) + str("-01 00:00:00'\n     AND post_type = 'post' AND post_status = 'publish'\n        AND post_date <= '") + str(thisyear) + str("-") + str(thismonth) + str("-") + str(last_day) + str(" 23:59:59'"), ARRAY_N)
    if dayswithposts:
        for daywith in dayswithposts:
            daywithpost[-1] = daywith[0]
        # end for
    # end if
    #// See how much we should pad in the beginning.
    pad = calendar_week_mod(gmdate("w", unixmonth) - week_begins)
    if 0 != pad:
        calendar_output += "\n      " + "<td colspan=\"" + esc_attr(pad) + "\" class=\"pad\">&nbsp;</td>"
    # end if
    newrow = False
    daysinmonth = int(gmdate("t", unixmonth))
    day = 1
    while day <= daysinmonth:
        
        if (php_isset(lambda : newrow)) and newrow:
            calendar_output += """
            </tr>
            <tr>
            """
        # end if
        newrow = False
        if current_time("j") == day and current_time("m") == thismonth and current_time("Y") == thisyear:
            calendar_output += "<td id=\"today\">"
        else:
            calendar_output += "<td>"
        # end if
        if php_in_array(day, daywithpost):
            #// Any posts today?
            date_format = gmdate(_x("F j, Y", "daily archives date format"), strtotime(str(thisyear) + str("-") + str(thismonth) + str("-") + str(day)))
            #// translators: Post calendar label. %s: Date.
            label = php_sprintf(__("Posts published on %s"), date_format)
            calendar_output += php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_day_link(thisyear, thismonth, day), esc_attr(label), day)
        else:
            calendar_output += day
        # end if
        calendar_output += "</td>"
        if 6 == calendar_week_mod(gmdate("w", mktime(0, 0, 0, thismonth, day, thisyear)) - week_begins):
            newrow = True
        # end if
        day += 1
    # end while
    pad = 7 - calendar_week_mod(gmdate("w", mktime(0, 0, 0, thismonth, day, thisyear)) - week_begins)
    if 0 != pad and 7 != pad:
        calendar_output += "\n      " + "<td class=\"pad\" colspan=\"" + esc_attr(pad) + "\">&nbsp;</td>"
    # end if
    calendar_output += "\n  </tr>\n </tbody>"
    calendar_output += "\n  </table>"
    calendar_output += "<nav aria-label=\"" + __("Previous and next months") + "\" class=\"wp-calendar-nav\">"
    if previous:
        calendar_output += "\n      " + "<span class=\"wp-calendar-nav-prev\"><a href=\"" + get_month_link(previous.year, previous.month) + "\">&laquo; " + wp_locale.get_month_abbrev(wp_locale.get_month(previous.month)) + "</a></span>"
    else:
        calendar_output += "\n      " + "<span class=\"wp-calendar-nav-prev\">&nbsp;</span>"
    # end if
    calendar_output += "\n      " + "<span class=\"pad\">&nbsp;</span>"
    if next:
        calendar_output += "\n      " + "<span class=\"wp-calendar-nav-next\"><a href=\"" + get_month_link(next.year, next.month) + "\">" + wp_locale.get_month_abbrev(wp_locale.get_month(next.month)) + " &raquo;</a></span>"
    else:
        calendar_output += "\n      " + "<span class=\"wp-calendar-nav-next\">&nbsp;</span>"
    # end if
    calendar_output += "\n  </nav>"
    cache[key] = calendar_output
    wp_cache_set("get_calendar", cache, "calendar")
    if echo:
        #// 
        #// Filters the HTML calendar output.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string $calendar_output HTML output of the calendar.
        #//
        php_print(apply_filters("get_calendar", calendar_output))
        return
    # end if
    #// This filter is documented in wp-includes/general-template.php
    return apply_filters("get_calendar", calendar_output)
# end def get_calendar
#// 
#// Purge the cached results of get_calendar.
#// 
#// @see get_calendar
#// @since 2.1.0
#//
def delete_get_calendar_cache(*args_):
    
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
def allowed_tags(*args_):
    
    global allowedtags
    php_check_if_defined("allowedtags")
    allowed = ""
    for tag,attributes in allowedtags:
        allowed += "<" + tag
        if 0 < php_count(attributes):
            for attribute,limits in attributes:
                allowed += " " + attribute + "=\"\""
            # end for
        # end if
        allowed += "> "
    # end for
    return htmlentities(allowed)
# end def allowed_tags
#// Date/Time tags
#// 
#// Outputs the date in iso8601 format for xml files.
#// 
#// @since 1.0.0
#//
def the_date_xml(*args_):
    
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
def the_date(format="", before="", after="", echo=True, *args_):
    
    global currentday,previousday
    php_check_if_defined("currentday","previousday")
    the_date = ""
    if is_new_day():
        the_date = before + get_the_date(format) + after
        previousday = currentday
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
    the_date = apply_filters("the_date", the_date, format, before, after)
    if echo:
        php_print(the_date)
    else:
        return the_date
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
def get_the_date(format="", post=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    if "" == format:
        the_date = get_post_time(get_option("date_format"), False, post, True)
    else:
        the_date = get_post_time(format, False, post, True)
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
    return apply_filters("get_the_date", the_date, format, post)
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
def the_modified_date(format="", before="", after="", echo=True, *args_):
    
    the_modified_date = before + get_the_modified_date(format) + after
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
    the_modified_date = apply_filters("the_modified_date", the_modified_date, format, before, after)
    if echo:
        php_print(the_modified_date)
    else:
        return the_modified_date
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
def get_the_modified_date(format="", post=None, *args_):
    
    post = get_post(post)
    if (not post):
        #// For backward compatibility, failures go through the filter below.
        the_time = False
    elif php_empty(lambda : format):
        the_time = get_post_modified_time(get_option("date_format"), False, post, True)
    else:
        the_time = get_post_modified_time(format, False, post, True)
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
    return apply_filters("get_the_modified_date", the_time, format, post)
# end def get_the_modified_date
#// 
#// Display the time at which the post was written.
#// 
#// @since 0.71
#// 
#// @param string $format Either 'G', 'U', or PHP date format.
#//
def the_time(format="", *args_):
    
    #// 
    #// Filters the time a post was written for display.
    #// 
    #// @since 0.71
    #// 
    #// @param string $get_the_time The formatted time.
    #// @param string $format       The time format. Accepts 'G', 'U',
    #// or PHP date format.
    #//
    php_print(apply_filters("the_time", get_the_time(format), format))
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
def get_the_time(format="", post=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    if "" == format:
        the_time = get_post_time(get_option("time_format"), False, post, True)
    else:
        the_time = get_post_time(format, False, post, True)
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
    return apply_filters("get_the_time", the_time, format, post)
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
def get_post_time(format="U", gmt=False, post=None, translate=False, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    source = "gmt" if gmt else "local"
    datetime = get_post_datetime(post, "date", source)
    if False == datetime:
        return False
    # end if
    if "U" == format or "G" == format:
        time = datetime.gettimestamp()
        #// Returns a sum of timestamp with timezone offset. Ideally should never be used.
        if (not gmt):
            time += datetime.getoffset()
        # end if
    elif translate:
        time = wp_date(format, datetime.gettimestamp(), php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")) if gmt else None)
    else:
        if gmt:
            datetime = datetime.settimezone(php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")))
        # end if
        time = datetime.format(format)
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
    return apply_filters("get_post_time", time, format, gmt)
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
def get_post_datetime(post=None, field="date", source="local", *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    wp_timezone = wp_timezone()
    if "gmt" == source:
        time = post.post_modified_gmt if "modified" == field else post.post_date_gmt
        timezone = php_new_class("DateTimeZone", lambda : DateTimeZone("UTC"))
    else:
        time = post.post_modified if "modified" == field else post.post_date
        timezone = wp_timezone
    # end if
    if php_empty(lambda : time) or "0000-00-00 00:00:00" == time:
        return False
    # end if
    datetime = date_create_immutable_from_format("Y-m-d H:i:s", time, timezone)
    if False == datetime:
        return False
    # end if
    return datetime.settimezone(wp_timezone)
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
def get_post_timestamp(post=None, field="date", *args_):
    
    datetime = get_post_datetime(post, field)
    if False == datetime:
        return False
    # end if
    return datetime.gettimestamp()
# end def get_post_timestamp
#// 
#// Display the time at which the post was last modified.
#// 
#// @since 2.0.0
#// 
#// @param string $format Optional. Either 'G', 'U', or PHP date format defaults
#// to the value specified in the time_format option.
#//
def the_modified_time(format="", *args_):
    
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
    php_print(apply_filters("the_modified_time", get_the_modified_time(format), format))
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
def get_the_modified_time(format="", post=None, *args_):
    
    post = get_post(post)
    if (not post):
        #// For backward compatibility, failures go through the filter below.
        the_time = False
    elif php_empty(lambda : format):
        the_time = get_post_modified_time(get_option("time_format"), False, post, True)
    else:
        the_time = get_post_modified_time(format, False, post, True)
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
    return apply_filters("get_the_modified_time", the_time, format, post)
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
def get_post_modified_time(format="U", gmt=False, post=None, translate=False, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    source = "gmt" if gmt else "local"
    datetime = get_post_datetime(post, "modified", source)
    if False == datetime:
        return False
    # end if
    if "U" == format or "G" == format:
        time = datetime.gettimestamp()
        #// Returns a sum of timestamp with timezone offset. Ideally should never be used.
        if (not gmt):
            time += datetime.getoffset()
        # end if
    elif translate:
        time = wp_date(format, datetime.gettimestamp(), php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")) if gmt else None)
    else:
        if gmt:
            datetime = datetime.settimezone(php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")))
        # end if
        time = datetime.format(format)
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
    return apply_filters("get_post_modified_time", time, format, gmt)
# end def get_post_modified_time
#// 
#// Display the weekday on which the post was written.
#// 
#// @since 0.71
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#//
def the_weekday(*args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    post = get_post()
    if (not post):
        return
    # end if
    the_weekday = wp_locale.get_weekday(get_post_time("w", False, post))
    #// 
    #// Filters the weekday on which the post was written, for display.
    #// 
    #// @since 0.71
    #// 
    #// @param string $the_weekday
    #//
    php_print(apply_filters("the_weekday", the_weekday))
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
def the_weekday_date(before="", after="", *args_):
    
    global wp_locale,currentday,previousweekday
    php_check_if_defined("wp_locale","currentday","previousweekday")
    post = get_post()
    if (not post):
        return
    # end if
    the_weekday_date = ""
    if currentday != previousweekday:
        the_weekday_date += before
        the_weekday_date += wp_locale.get_weekday(get_post_time("w", False, post))
        the_weekday_date += after
        previousweekday = currentday
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
    php_print(apply_filters("the_weekday_date", the_weekday_date, before, after))
# end def the_weekday_date
#// 
#// Fire the wp_head action.
#// 
#// See {@see 'wp_head'}.
#// 
#// @since 1.2.0
#//
def wp_head(*args_):
    
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
def wp_footer(*args_):
    
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
def wp_body_open(*args_):
    
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
def feed_links(args=Array(), *args_):
    
    if (not current_theme_supports("automatic-feed-links")):
        return
    # end if
    defaults = Array({"separator": _x("&raquo;", "feed link"), "feedtitle": __("%1$s %2$s Feed"), "comstitle": __("%1$s %2$s Comments Feed")})
    args = wp_parse_args(args, defaults)
    #// 
    #// Filters whether to display the posts feed link.
    #// 
    #// @since 4.4.0
    #// 
    #// @param bool $show Whether to display the posts feed link. Default true.
    #//
    if apply_filters("feed_links_show_posts_feed", True):
        php_print("<link rel=\"alternate\" type=\"" + feed_content_type() + "\" title=\"" + esc_attr(php_sprintf(args["feedtitle"], get_bloginfo("name"), args["separator"])) + "\" href=\"" + esc_url(get_feed_link()) + "\" />\n")
    # end if
    #// 
    #// Filters whether to display the comments feed link.
    #// 
    #// @since 4.4.0
    #// 
    #// @param bool $show Whether to display the comments feed link. Default true.
    #//
    if apply_filters("feed_links_show_comments_feed", True):
        php_print("<link rel=\"alternate\" type=\"" + feed_content_type() + "\" title=\"" + esc_attr(php_sprintf(args["comstitle"], get_bloginfo("name"), args["separator"])) + "\" href=\"" + esc_url(get_feed_link("comments_" + get_default_feed())) + "\" />\n")
    # end if
# end def feed_links
#// 
#// Display the links to the extra feeds such as category feeds.
#// 
#// @since 2.8.0
#// 
#// @param array $args Optional arguments.
#//
def feed_links_extra(args=Array(), *args_):
    
    defaults = Array({"separator": _x("&raquo;", "feed link"), "singletitle": __("%1$s %2$s %3$s Comments Feed"), "cattitle": __("%1$s %2$s %3$s Category Feed"), "tagtitle": __("%1$s %2$s %3$s Tag Feed"), "taxtitle": __("%1$s %2$s %3$s %4$s Feed"), "authortitle": __("%1$s %2$s Posts by %3$s Feed"), "searchtitle": __("%1$s %2$s Search Results for &#8220;%3$s&#8221; Feed"), "posttypetitle": __("%1$s %2$s %3$s Feed")})
    args = wp_parse_args(args, defaults)
    if is_singular():
        id = 0
        post = get_post(id)
        if comments_open() or pings_open() or post.comment_count > 0:
            title = php_sprintf(args["singletitle"], get_bloginfo("name"), args["separator"], the_title_attribute(Array({"echo": False})))
            href = get_post_comments_feed_link(post.ID)
        # end if
    elif is_post_type_archive():
        post_type = get_query_var("post_type")
        if php_is_array(post_type):
            post_type = reset(post_type)
        # end if
        post_type_obj = get_post_type_object(post_type)
        title = php_sprintf(args["posttypetitle"], get_bloginfo("name"), args["separator"], post_type_obj.labels.name)
        href = get_post_type_archive_feed_link(post_type_obj.name)
    elif is_category():
        term = get_queried_object()
        if term:
            title = php_sprintf(args["cattitle"], get_bloginfo("name"), args["separator"], term.name)
            href = get_category_feed_link(term.term_id)
        # end if
    elif is_tag():
        term = get_queried_object()
        if term:
            title = php_sprintf(args["tagtitle"], get_bloginfo("name"), args["separator"], term.name)
            href = get_tag_feed_link(term.term_id)
        # end if
    elif is_tax():
        term = get_queried_object()
        if term:
            tax = get_taxonomy(term.taxonomy)
            title = php_sprintf(args["taxtitle"], get_bloginfo("name"), args["separator"], term.name, tax.labels.singular_name)
            href = get_term_feed_link(term.term_id, term.taxonomy)
        # end if
    elif is_author():
        author_id = php_intval(get_query_var("author"))
        title = php_sprintf(args["authortitle"], get_bloginfo("name"), args["separator"], get_the_author_meta("display_name", author_id))
        href = get_author_feed_link(author_id)
    elif is_search():
        title = php_sprintf(args["searchtitle"], get_bloginfo("name"), args["separator"], get_search_query(False))
        href = get_search_feed_link()
    # end if
    if (php_isset(lambda : title)) and (php_isset(lambda : href)):
        php_print("<link rel=\"alternate\" type=\"" + feed_content_type() + "\" title=\"" + esc_attr(title) + "\" href=\"" + esc_url(href) + "\" />" + "\n")
    # end if
# end def feed_links_extra
#// 
#// Display the link to the Really Simple Discovery service endpoint.
#// 
#// @link http://archipelago.phrasewise.com/rsd
#// @since 2.0.0
#//
def rsd_link(*args_):
    
    php_print("<link rel=\"EditURI\" type=\"application/rsd+xml\" title=\"RSD\" href=\"" + esc_url(site_url("xmlrpc.php?rsd", "rpc")) + "\" />" + "\n")
# end def rsd_link
#// 
#// Display the link to the Windows Live Writer manifest file.
#// 
#// @link https://msdn.microsoft.com/en-us/library/bb463265.aspx
#// @since 2.3.1
#//
def wlwmanifest_link(*args_):
    
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
def noindex(*args_):
    
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
def wp_no_robots(*args_):
    
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
def wp_sensitive_page_meta(*args_):
    
    php_print(" <meta name='robots' content='noindex,noarchive' />\n    <meta name='referrer' content='strict-origin-when-cross-origin' />\n    ")
# end def wp_sensitive_page_meta
#// 
#// Display site icon meta tags.
#// 
#// @since 4.3.0
#// 
#// @link https://www.whatwg.org/specs/web-apps/current-work/multipage/links.html#rel-icon HTML5 specification link icon.
#//
def wp_site_icon(*args_):
    
    if (not has_site_icon()) and (not is_customize_preview()):
        return
    # end if
    meta_tags = Array()
    icon_32 = get_site_icon_url(32)
    if php_empty(lambda : icon_32) and is_customize_preview():
        icon_32 = "/favicon.ico"
        pass
    # end if
    if icon_32:
        meta_tags[-1] = php_sprintf("<link rel=\"icon\" href=\"%s\" sizes=\"32x32\" />", esc_url(icon_32))
    # end if
    icon_192 = get_site_icon_url(192)
    if icon_192:
        meta_tags[-1] = php_sprintf("<link rel=\"icon\" href=\"%s\" sizes=\"192x192\" />", esc_url(icon_192))
    # end if
    icon_180 = get_site_icon_url(180)
    if icon_180:
        meta_tags[-1] = php_sprintf("<link rel=\"apple-touch-icon\" href=\"%s\" />", esc_url(icon_180))
    # end if
    icon_270 = get_site_icon_url(270)
    if icon_270:
        meta_tags[-1] = php_sprintf("<meta name=\"msapplication-TileImage\" content=\"%s\" />", esc_url(icon_270))
    # end if
    #// 
    #// Filters the site icon meta tags, so plugins can add their own.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string[] $meta_tags Array of Site Icon meta tags.
    #//
    meta_tags = apply_filters("site_icon_meta_tags", meta_tags)
    meta_tags = php_array_filter(meta_tags)
    for meta_tag in meta_tags:
        php_print(str(meta_tag) + str("\n"))
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
def wp_resource_hints(*args_):
    
    hints = Array({"dns-prefetch": wp_dependencies_unique_hosts(), "preconnect": Array(), "prefetch": Array(), "prerender": Array()})
    #// 
    #// Add DNS prefetch for the Emoji CDN.
    #// The path is removed in the foreach loop below.
    #// 
    #// This filter is documented in wp-includes/formatting.php
    hints["dns-prefetch"][-1] = apply_filters("emoji_svg_url", "https://s.w.org/images/core/emoji/12.0.0-1/svg/")
    for relation_type,urls in hints:
        unique_urls = Array()
        #// 
        #// Filters domains and URLs for resource hints of relation type.
        #// 
        #// @since 4.6.0
        #// 
        #// @param array  $urls          URLs to print for resource hints.
        #// @param string $relation_type The relation type the URLs are printed for, e.g. 'preconnect' or 'prerender'.
        #//
        urls = apply_filters("wp_resource_hints", urls, relation_type)
        for key,url in urls:
            atts = Array()
            if php_is_array(url):
                if (php_isset(lambda : url["href"])):
                    atts = url
                    url = url["href"]
                else:
                    continue
                # end if
            # end if
            url = esc_url(url, Array("http", "https"))
            if (not url):
                continue
            # end if
            if (php_isset(lambda : unique_urls[url])):
                continue
            # end if
            if php_in_array(relation_type, Array("preconnect", "dns-prefetch")):
                parsed = wp_parse_url(url)
                if php_empty(lambda : parsed["host"]):
                    continue
                # end if
                if "preconnect" == relation_type and (not php_empty(lambda : parsed["scheme"])):
                    url = parsed["scheme"] + "://" + parsed["host"]
                else:
                    #// Use protocol-relative URLs for dns-prefetch or if scheme is missing.
                    url = "//" + parsed["host"]
                # end if
            # end if
            atts["rel"] = relation_type
            atts["href"] = url
            unique_urls[url] = atts
        # end for
        for atts in unique_urls:
            html = ""
            for attr,value in atts:
                if (not is_scalar(value)) or (not php_in_array(attr, Array("as", "crossorigin", "href", "pr", "rel", "type"), True)) and (not php_is_numeric(attr)):
                    continue
                # end if
                value = esc_url(value) if "href" == attr else esc_attr(value)
                if (not php_is_string(attr)):
                    html += str(" ") + str(value)
                else:
                    html += str(" ") + str(attr) + str("='") + str(value) + str("'")
                # end if
            # end for
            html = php_trim(html)
            php_print(str("<link ") + str(html) + str(" />\n"))
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
def wp_dependencies_unique_hosts(*args_):
    
    global wp_scripts,wp_styles
    php_check_if_defined("wp_scripts","wp_styles")
    unique_hosts = Array()
    for dependencies in Array(wp_scripts, wp_styles):
        if type(dependencies).__name__ == "WP_Dependencies" and (not php_empty(lambda : dependencies.queue)):
            for handle in dependencies.queue:
                if (not (php_isset(lambda : dependencies.registered[handle]))):
                    continue
                # end if
                #// @var _WP_Dependency $dependency
                dependency = dependencies.registered[handle]
                parsed = wp_parse_url(dependency.src)
                if (not php_empty(lambda : parsed["host"])) and (not php_in_array(parsed["host"], unique_hosts)) and parsed["host"] != PHP_SERVER["SERVER_NAME"]:
                    unique_hosts[-1] = parsed["host"]
                # end if
            # end for
        # end if
    # end for
    return unique_hosts
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
def user_can_richedit(*args_):
    
    global wp_rich_edit,is_gecko,is_opera,is_safari,is_chrome,is_IE,is_edge
    php_check_if_defined("wp_rich_edit","is_gecko","is_opera","is_safari","is_chrome","is_IE","is_edge")
    if (not (php_isset(lambda : wp_rich_edit))):
        wp_rich_edit = False
        if get_user_option("rich_editing") == "true" or (not is_user_logged_in()):
            #// Default to 'true' for logged out users.
            if is_safari:
                wp_rich_edit = (not wp_is_mobile()) or php_preg_match("!AppleWebKit/(\\d+)!", PHP_SERVER["HTTP_USER_AGENT"], match) and php_intval(match[1]) >= 534
            elif is_IE:
                wp_rich_edit = php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Trident/7.0;") != False
            elif is_gecko or is_chrome or is_edge or is_opera and (not wp_is_mobile()):
                wp_rich_edit = True
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
    return apply_filters("user_can_richedit", wp_rich_edit)
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
def wp_default_editor(*args_):
    
    r = "tinymce" if user_can_richedit() else "html"
    #// Defaults.
    if wp_get_current_user():
        #// Look for cookie.
        ed = get_user_setting("editor", "tinymce")
        r = ed if php_in_array(ed, Array("tinymce", "html", "test")) else r
    # end if
    #// 
    #// Filters which editor should be displayed by default.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $r Which editor should be displayed by default. Either 'tinymce', 'html', or 'test'.
    #//
    return apply_filters("wp_default_editor", r)
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
def wp_editor(content=None, editor_id=None, settings=Array(), *args_):
    
    if (not php_class_exists("_WP_Editors", False)):
        php_include_file(ABSPATH + WPINC + "/class-wp-editor.php", once=False)
    # end if
    _WP_Editors.editor(content, editor_id, settings)
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
def wp_enqueue_editor(*args_):
    
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
def wp_enqueue_code_editor(args=None, *args_):
    
    if is_user_logged_in() and "false" == wp_get_current_user().syntax_highlighting:
        return False
    # end if
    settings = wp_get_code_editor_settings(args)
    if php_empty(lambda : settings) or php_empty(lambda : settings["codemirror"]):
        return False
    # end if
    wp_enqueue_script("code-editor")
    wp_enqueue_style("code-editor")
    if (php_isset(lambda : settings["codemirror"]["mode"])):
        mode = settings["codemirror"]["mode"]
        if php_is_string(mode):
            mode = Array({"name": mode})
        # end if
        if (not php_empty(lambda : settings["codemirror"]["lint"])):
            for case in Switch(mode["name"]):
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
    wp_add_inline_script("code-editor", php_sprintf("jQuery.extend( wp.codeEditor.defaultSettings, %s );", wp_json_encode(settings)))
    #// 
    #// Fires when scripts and styles are enqueued for the code editor.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $settings Settings for the enqueued code editor.
    #//
    do_action("wp_enqueue_code_editor", settings)
    return settings
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
def wp_get_code_editor_settings(args=None, *args_):
    
    settings = Array({"codemirror": Array({"indentUnit": 4, "indentWithTabs": True, "inputStyle": "contenteditable", "lineNumbers": True, "lineWrapping": True, "styleActiveLine": True, "continueComments": True, "extraKeys": Array({"Ctrl-Space": "autocomplete", "Ctrl-/": "toggleComment", "Cmd-/": "toggleComment", "Alt-F": "findPersistent", "Ctrl-F": "findPersistent", "Cmd-F": "findPersistent"})}, {"direction": "ltr", "gutters": Array()})}, {"csslint": Array({"errors": True, "box-model": True, "display-property-grouping": True, "duplicate-properties": True, "known-properties": True, "outline-none": True})}, {"jshint": Array({"boss": True, "curly": True, "eqeqeq": True, "eqnull": True, "es3": True, "expr": True, "immed": True, "noarg": True, "nonbsp": True, "onevar": True, "quotmark": "single", "trailing": True, "undef": True, "unused": True, "browser": True, "globals": Array({"_": False, "Backbone": False, "jQuery": False, "JSON": False, "wp": False})})}, {"htmlhint": Array({"tagname-lowercase": True, "attr-lowercase": True, "attr-value-double-quotes": False, "doctype-first": False, "tag-pair": True, "spec-char-escape": True, "id-unique": True, "src-not-empty": True, "attr-no-duplication": True, "alt-require": True, "space-tab-mixed-disabled": "tab", "attr-unsafe-chars": True})})
    type = ""
    if (php_isset(lambda : args["type"])):
        type = args["type"]
        #// Remap MIME types to ones that CodeMirror modes will recognize.
        if "application/x-patch" == type or "text/x-patch" == type:
            type = "text/x-diff"
        # end if
    elif (php_isset(lambda : args["file"])) and False != php_strpos(php_basename(args["file"]), "."):
        extension = php_strtolower(pathinfo(args["file"], PATHINFO_EXTENSION))
        for exts,mime in wp_get_mime_types():
            if php_preg_match("!^(" + exts + ")$!i", extension):
                type = mime
                break
            # end if
        # end for
        #// Supply any types that are not matched by wp_get_mime_types().
        if php_empty(lambda : type):
            for case in Switch(extension):
                if case("conf"):
                    type = "text/nginx"
                    break
                # end if
                if case("css"):
                    type = "text/css"
                    break
                # end if
                if case("diff"):
                    pass
                # end if
                if case("patch"):
                    type = "text/x-diff"
                    break
                # end if
                if case("html"):
                    pass
                # end if
                if case("htm"):
                    type = "text/html"
                    break
                # end if
                if case("http"):
                    type = "message/http"
                    break
                # end if
                if case("js"):
                    type = "text/javascript"
                    break
                # end if
                if case("json"):
                    type = "application/json"
                    break
                # end if
                if case("jsx"):
                    type = "text/jsx"
                    break
                # end if
                if case("less"):
                    type = "text/x-less"
                    break
                # end if
                if case("md"):
                    type = "text/x-gfm"
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
                    type = "application/x-httpd-php"
                    break
                # end if
                if case("scss"):
                    type = "text/x-scss"
                    break
                # end if
                if case("sass"):
                    type = "text/x-sass"
                    break
                # end if
                if case("sh"):
                    pass
                # end if
                if case("bash"):
                    type = "text/x-sh"
                    break
                # end if
                if case("sql"):
                    type = "text/x-sql"
                    break
                # end if
                if case("svg"):
                    type = "application/svg+xml"
                    break
                # end if
                if case("xml"):
                    type = "text/xml"
                    break
                # end if
                if case("yml"):
                    pass
                # end if
                if case("yaml"):
                    type = "text/x-yaml"
                    break
                # end if
                if case("txt"):
                    pass
                # end if
                if case():
                    type = "text/plain"
                    break
                # end if
            # end for
        # end if
    # end if
    if php_in_array(type, Array("text/css", "text/x-scss", "text/x-less", "text/x-sass"), True):
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": type, "lint": False, "autoCloseBrackets": True, "matchBrackets": True}))
    elif "text/x-diff" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "diff"}))
    elif "text/html" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "htmlmixed", "lint": True, "autoCloseBrackets": True, "autoCloseTags": True, "matchTags": Array({"bothTags": True})}))
        if (not current_user_can("unfiltered_html")):
            settings["htmlhint"]["kses"] = wp_kses_allowed_html("post")
        # end if
    elif "text/x-gfm" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "gfm", "highlightFormatting": True}))
    elif "application/javascript" == type or "text/javascript" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "javascript", "lint": True, "autoCloseBrackets": True, "matchBrackets": True}))
    elif False != php_strpos(type, "json"):
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": Array({"name": "javascript"})}, {"lint": True, "autoCloseBrackets": True, "matchBrackets": True}))
        if "application/ld+json" == type:
            settings["codemirror"]["mode"]["jsonld"] = True
        else:
            settings["codemirror"]["mode"]["json"] = True
        # end if
    elif False != php_strpos(type, "jsx"):
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "jsx", "autoCloseBrackets": True, "matchBrackets": True}))
    elif "text/x-markdown" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "markdown", "highlightFormatting": True}))
    elif "text/nginx" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "nginx"}))
    elif "application/x-httpd-php" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "php", "autoCloseBrackets": True, "autoCloseTags": True, "matchBrackets": True, "matchTags": Array({"bothTags": True})}))
    elif "text/x-sql" == type or "text/x-mysql" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "sql", "autoCloseBrackets": True, "matchBrackets": True}))
    elif False != php_strpos(type, "xml"):
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "xml", "autoCloseBrackets": True, "autoCloseTags": True, "matchTags": Array({"bothTags": True})}))
    elif "text/x-yaml" == type:
        settings["codemirror"] = php_array_merge(settings["codemirror"], Array({"mode": "yaml"}))
    else:
        settings["codemirror"]["mode"] = type
    # end if
    if (not php_empty(lambda : settings["codemirror"]["lint"])):
        settings["codemirror"]["gutters"][-1] = "CodeMirror-lint-markers"
    # end if
    #// Let settings supplied via args override any defaults.
    for key,value in wp_array_slice_assoc(args, Array("codemirror", "csslint", "jshint", "htmlhint")):
        settings[key] = php_array_merge(settings[key], value)
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
    return apply_filters("wp_code_editor_settings", settings, args)
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
def get_search_query(escaped=True, *args_):
    
    #// 
    #// Filters the contents of the search query variable.
    #// 
    #// @since 2.3.0
    #// 
    #// @param mixed $search Contents of the search query variable.
    #//
    query = apply_filters("get_search_query", get_query_var("s"))
    if escaped:
        query = esc_attr(query)
    # end if
    return query
# end def get_search_query
#// 
#// Displays the contents of the search query variable.
#// 
#// The search query string is passed through esc_attr() to ensure that it is safe
#// for placing in an html attribute.
#// 
#// @since 2.1.0
#//
def the_search_query(*args_):
    
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
def get_language_attributes(doctype="html", *args_):
    
    attributes = Array()
    if php_function_exists("is_rtl") and is_rtl():
        attributes[-1] = "dir=\"rtl\""
    # end if
    lang = get_bloginfo("language")
    if lang:
        if "text/html" == get_option("html_type") or "html" == doctype:
            attributes[-1] = "lang=\"" + esc_attr(lang) + "\""
        # end if
        if "text/html" != get_option("html_type") or "xhtml" == doctype:
            attributes[-1] = "xml:lang=\"" + esc_attr(lang) + "\""
        # end if
    # end if
    output = php_implode(" ", attributes)
    #// 
    #// Filters the language attributes for display in the html tag.
    #// 
    #// @since 2.5.0
    #// @since 4.3.0 Added the `$doctype` parameter.
    #// 
    #// @param string $output A space-separated list of language attributes.
    #// @param string $doctype The type of html document (xhtml|html).
    #//
    return apply_filters("language_attributes", output, doctype)
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
def language_attributes(doctype="html", *args_):
    
    php_print(get_language_attributes(doctype))
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
def paginate_links(args="", *args_):
    
    global wp_query,wp_rewrite
    php_check_if_defined("wp_query","wp_rewrite")
    #// Setting up default values based on the current URL.
    pagenum_link = html_entity_decode(get_pagenum_link())
    url_parts = php_explode("?", pagenum_link)
    #// Get max pages and current page out of the current query, if available.
    total = wp_query.max_num_pages if (php_isset(lambda : wp_query.max_num_pages)) else 1
    current = php_intval(get_query_var("paged")) if get_query_var("paged") else 1
    #// Append the format placeholder to the base URL.
    pagenum_link = trailingslashit(url_parts[0]) + "%_%"
    #// URL base depends on permalink settings.
    format = "index.php/" if wp_rewrite.using_index_permalinks() and (not php_strpos(pagenum_link, "index.php")) else ""
    format += user_trailingslashit(wp_rewrite.pagination_base + "/%#%", "paged") if wp_rewrite.using_permalinks() else "?paged=%#%"
    defaults = Array({"base": pagenum_link, "format": format, "total": total, "current": current, "aria_current": "page", "show_all": False, "prev_next": True, "prev_text": __("&laquo; Previous"), "next_text": __("Next &raquo;"), "end_size": 1, "mid_size": 2, "type": "plain", "add_args": Array(), "add_fragment": "", "before_page_number": "", "after_page_number": ""})
    args = wp_parse_args(args, defaults)
    if (not php_is_array(args["add_args"])):
        args["add_args"] = Array()
    # end if
    #// Merge additional query vars found in the original URL into 'add_args' array.
    if (php_isset(lambda : url_parts[1])):
        #// Find the format argument.
        format = php_explode("?", php_str_replace("%_%", args["format"], args["base"]))
        format_query = format[1] if (php_isset(lambda : format[1])) else ""
        wp_parse_str(format_query, format_args)
        #// Find the query args of the requested URL.
        wp_parse_str(url_parts[1], url_query_args)
        #// Remove the format argument from the array of query arguments, to avoid overwriting custom format.
        for format_arg,format_arg_value in format_args:
            url_query_args[format_arg] = None
        # end for
        args["add_args"] = php_array_merge(args["add_args"], urlencode_deep(url_query_args))
    # end if
    #// Who knows what else people pass in $args.
    total = int(args["total"])
    if total < 2:
        return
    # end if
    current = int(args["current"])
    end_size = int(args["end_size"])
    #// Out of bounds? Make it the default.
    if end_size < 1:
        end_size = 1
    # end if
    mid_size = int(args["mid_size"])
    if mid_size < 0:
        mid_size = 2
    # end if
    add_args = args["add_args"]
    r = ""
    page_links = Array()
    dots = False
    if args["prev_next"] and current and 1 < current:
        link = php_str_replace("%_%", "" if 2 == current else args["format"], args["base"])
        link = php_str_replace("%#%", current - 1, link)
        if add_args:
            link = add_query_arg(add_args, link)
        # end if
        link += args["add_fragment"]
        page_links[-1] = php_sprintf("<a class=\"prev page-numbers\" href=\"%s\">%s</a>", esc_url(apply_filters("paginate_links", link)), args["prev_text"])
    # end if
    n = 1
    while n <= total:
        
        if n == current:
            page_links[-1] = php_sprintf("<span aria-current=\"%s\" class=\"page-numbers current\">%s</span>", esc_attr(args["aria_current"]), args["before_page_number"] + number_format_i18n(n) + args["after_page_number"])
            dots = True
        else:
            if args["show_all"] or n <= end_size or current and n >= current - mid_size and n <= current + mid_size or n > total - end_size:
                link = php_str_replace("%_%", "" if 1 == n else args["format"], args["base"])
                link = php_str_replace("%#%", n, link)
                if add_args:
                    link = add_query_arg(add_args, link)
                # end if
                link += args["add_fragment"]
                page_links[-1] = php_sprintf("<a class=\"page-numbers\" href=\"%s\">%s</a>", esc_url(apply_filters("paginate_links", link)), args["before_page_number"] + number_format_i18n(n) + args["after_page_number"])
                dots = True
            elif dots and (not args["show_all"]):
                page_links[-1] = "<span class=\"page-numbers dots\">" + __("&hellip;") + "</span>"
                dots = False
            # end if
        # end if
        n += 1
    # end while
    if args["prev_next"] and current and current < total:
        link = php_str_replace("%_%", args["format"], args["base"])
        link = php_str_replace("%#%", current + 1, link)
        if add_args:
            link = add_query_arg(add_args, link)
        # end if
        link += args["add_fragment"]
        page_links[-1] = php_sprintf("<a class=\"next page-numbers\" href=\"%s\">%s</a>", esc_url(apply_filters("paginate_links", link)), args["next_text"])
    # end if
    for case in Switch(args["type"]):
        if case("array"):
            return page_links
        # end if
        if case("list"):
            r += "<ul class='page-numbers'>\n   <li>"
            r += join("</li>\n  <li>", page_links)
            r += "</li>\n</ul>\n"
            break
        # end if
        if case():
            r = join("\n", page_links)
            break
        # end if
    # end for
    return r
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
def wp_admin_css_color(key=None, name=None, url=None, colors=Array(), icons=Array(), *args_):
    
    global _wp_admin_css_colors
    php_check_if_defined("_wp_admin_css_colors")
    if (not (php_isset(lambda : _wp_admin_css_colors))):
        _wp_admin_css_colors = Array()
    # end if
    _wp_admin_css_colors[key] = Array({"name": name, "url": url, "colors": colors, "icon_colors": icons})
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
def register_admin_color_schemes(*args_):
    
    suffix = "-rtl" if is_rtl() else ""
    suffix += "" if SCRIPT_DEBUG else ".min"
    wp_admin_css_color("fresh", _x("Default", "admin color scheme"), False, Array("#222", "#333", "#0073aa", "#00a0d2"), Array({"base": "#a0a5aa", "focus": "#00a0d2", "current": "#fff"}))
    #// Other color schemes are not available when running out of src.
    if False != php_strpos(get_bloginfo("version"), "-src"):
        return
    # end if
    wp_admin_css_color("light", _x("Light", "admin color scheme"), admin_url(str("css/colors/light/colors") + str(suffix) + str(".css")), Array("#e5e5e5", "#999", "#d64e07", "#04a4cc"), Array({"base": "#999", "focus": "#ccc", "current": "#ccc"}))
    wp_admin_css_color("blue", _x("Blue", "admin color scheme"), admin_url(str("css/colors/blue/colors") + str(suffix) + str(".css")), Array("#096484", "#4796b3", "#52accc", "#74B6CE"), Array({"base": "#e5f8ff", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("midnight", _x("Midnight", "admin color scheme"), admin_url(str("css/colors/midnight/colors") + str(suffix) + str(".css")), Array("#25282b", "#363b3f", "#69a8bb", "#e14d43"), Array({"base": "#f1f2f3", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("sunrise", _x("Sunrise", "admin color scheme"), admin_url(str("css/colors/sunrise/colors") + str(suffix) + str(".css")), Array("#b43c38", "#cf4944", "#dd823b", "#ccaf0b"), Array({"base": "#f3f1f1", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("ectoplasm", _x("Ectoplasm", "admin color scheme"), admin_url(str("css/colors/ectoplasm/colors") + str(suffix) + str(".css")), Array("#413256", "#523f6d", "#a3b745", "#d46f15"), Array({"base": "#ece6f6", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("ocean", _x("Ocean", "admin color scheme"), admin_url(str("css/colors/ocean/colors") + str(suffix) + str(".css")), Array("#627c83", "#738e96", "#9ebaa0", "#aa9d88"), Array({"base": "#f2fcff", "focus": "#fff", "current": "#fff"}))
    wp_admin_css_color("coffee", _x("Coffee", "admin color scheme"), admin_url(str("css/colors/coffee/colors") + str(suffix) + str(".css")), Array("#46403c", "#59524c", "#c7a589", "#9ea476"), Array({"base": "#f3f2f1", "focus": "#fff", "current": "#fff"}))
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
def wp_admin_css_uri(file="wp-admin", *args_):
    
    if php_defined("WP_INSTALLING"):
        _file = str("./") + str(file) + str(".css")
    else:
        _file = admin_url(str(file) + str(".css"))
    # end if
    _file = add_query_arg("version", get_bloginfo("version"), _file)
    #// 
    #// Filters the URI of a WordPress admin CSS file.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $_file Relative path to the file with query arguments attached.
    #// @param string $file  Relative path to the file, minus its ".css" extension.
    #//
    return apply_filters("wp_admin_css_uri", _file, file)
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
def wp_admin_css(file="wp-admin", force_echo=False, *args_):
    
    #// For backward compatibility.
    handle = php_substr(file, 4) if 0 == php_strpos(file, "css/") else file
    if wp_styles().query(handle):
        if force_echo or did_action("wp_print_styles"):
            #// We already printed the style queue. Print this one immediately.
            wp_print_styles(handle)
        else:
            #// Add to style queue.
            wp_enqueue_style(handle)
        # end if
        return
    # end if
    stylesheet_link = php_sprintf("<link rel='stylesheet' href='%s' type='text/css' />\n", esc_url(wp_admin_css_uri(file)))
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
    php_print(apply_filters("wp_admin_css", stylesheet_link, file))
    if php_function_exists("is_rtl") and is_rtl():
        rtl_stylesheet_link = php_sprintf("<link rel='stylesheet' href='%s' type='text/css' />\n", esc_url(wp_admin_css_uri(str(file) + str("-rtl"))))
        #// This filter is documented in wp-includes/general-template.php
        php_print(apply_filters("wp_admin_css", rtl_stylesheet_link, str(file) + str("-rtl")))
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
def add_thickbox(*args_):
    
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
def wp_generator(*args_):
    
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
def the_generator(type=None, *args_):
    
    #// 
    #// Filters the output of the XHTML generator tag for display.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $generator_type The generator output.
    #// @param string $type           The type of generator to output. Accepts 'html',
    #// 'xhtml', 'atom', 'rss2', 'rdf', 'comment', 'export'.
    #//
    php_print(apply_filters("the_generator", get_the_generator(type), type) + "\n")
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
def get_the_generator(type="", *args_):
    
    if php_empty(lambda : type):
        current_filter = current_filter()
        if php_empty(lambda : current_filter):
            return
        # end if
        for case in Switch(current_filter):
            if case("rss2_head"):
                pass
            # end if
            if case("commentsrss2_head"):
                type = "rss2"
                break
            # end if
            if case("rss_head"):
                pass
            # end if
            if case("opml_head"):
                type = "comment"
                break
            # end if
            if case("rdf_header"):
                type = "rdf"
                break
            # end if
            if case("atom_head"):
                pass
            # end if
            if case("comments_atom_head"):
                pass
            # end if
            if case("app_head"):
                type = "atom"
                break
            # end if
        # end for
    # end if
    for case in Switch(type):
        if case("html"):
            gen = "<meta name=\"generator\" content=\"WordPress " + esc_attr(get_bloginfo("version")) + "\">"
            break
        # end if
        if case("xhtml"):
            gen = "<meta name=\"generator\" content=\"WordPress " + esc_attr(get_bloginfo("version")) + "\" />"
            break
        # end if
        if case("atom"):
            gen = "<generator uri=\"https://wordpress.org/\" version=\"" + esc_attr(get_bloginfo_rss("version")) + "\">WordPress</generator>"
            break
        # end if
        if case("rss2"):
            gen = "<generator>" + esc_url_raw("https://wordpress.org/?v=" + get_bloginfo_rss("version")) + "</generator>"
            break
        # end if
        if case("rdf"):
            gen = "<admin:generatorAgent rdf:resource=\"" + esc_url_raw("https://wordpress.org/?v=" + get_bloginfo_rss("version")) + "\" />"
            break
        # end if
        if case("comment"):
            gen = "<!-- generator=\"WordPress/" + esc_attr(get_bloginfo("version")) + "\" -->"
            break
        # end if
        if case("export"):
            gen = "<!-- generator=\"WordPress/" + esc_attr(get_bloginfo_rss("version")) + "\" created=\"" + gmdate("Y-m-d H:i") + "\" -->"
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
    return apply_filters(str("get_the_generator_") + str(type), gen, type)
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
def checked(checked=None, current=True, echo=True, *args_):
    
    return __checked_selected_helper(checked, current, echo, "checked")
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
def selected(selected=None, current=True, echo=True, *args_):
    
    return __checked_selected_helper(selected, current, echo, "selected")
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
def disabled(disabled=None, current=True, echo=True, *args_):
    
    return __checked_selected_helper(disabled, current, echo, "disabled")
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
def readonly(readonly=None, current=True, echo=True, *args_):
    
    return __checked_selected_helper(readonly, current, echo, "readonly")
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
def __checked_selected_helper(helper=None, current=None, echo=None, type=None, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    if str(helper) == str(current):
        result = str(" ") + str(type) + str("='") + str(type) + str("'")
    else:
        result = ""
    # end if
    if echo:
        php_print(result)
    # end if
    return result
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
def wp_heartbeat_settings(settings=None, *args_):
    
    if (not is_admin()):
        settings["ajaxurl"] = admin_url("admin-ajax.php", "relative")
    # end if
    if is_user_logged_in():
        settings["nonce"] = wp_create_nonce("heartbeat-nonce")
    # end if
    return settings
# end def wp_heartbeat_settings
