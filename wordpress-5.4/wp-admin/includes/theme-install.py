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
#// WordPress Theme Installation Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#//
themes_allowedtags_ = Array({"a": Array({"href": Array(), "title": Array(), "target": Array()})}, {"abbr": Array({"title": Array()})}, {"acronym": Array({"title": Array()})}, {"code": Array(), "pre": Array(), "em": Array(), "strong": Array(), "div": Array(), "p": Array(), "ul": Array(), "ol": Array(), "li": Array(), "h1": Array(), "h2": Array(), "h3": Array(), "h4": Array(), "h5": Array(), "h6": Array(), "img": Array({"src": Array(), "class": Array(), "alt": Array()})})
theme_field_defaults_ = Array({"description": True, "sections": False, "tested": True, "requires": True, "rating": True, "downloaded": True, "downloadlink": True, "last_updated": True, "homepage": True, "tags": True, "num_ratings": True})
#// 
#// Retrieve list of WordPress theme features (aka theme tags).
#// 
#// @since 2.8.0
#// 
#// @deprecated since 3.1.0 Use get_theme_feature_list() instead.
#// 
#// @return array
#//
def install_themes_feature_list(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.1.0", "get_theme_feature_list()")
    cache_ = get_transient("wporg_theme_feature_list")
    if (not cache_):
        set_transient("wporg_theme_feature_list", Array(), 3 * HOUR_IN_SECONDS)
    # end if
    if cache_:
        return cache_
    # end if
    feature_list_ = themes_api("feature_list", Array())
    if is_wp_error(feature_list_):
        return Array()
    # end if
    set_transient("wporg_theme_feature_list", feature_list_, 3 * HOUR_IN_SECONDS)
    return feature_list_
# end def install_themes_feature_list
#// 
#// Display search form for searching themes.
#// 
#// @since 2.8.0
#// 
#// @param bool $type_selector
#//
def install_theme_search_form(type_selector_=None, *_args_):
    if type_selector_ is None:
        type_selector_ = True
    # end if
    
    type_ = wp_unslash(PHP_REQUEST["type"]) if (php_isset(lambda : PHP_REQUEST["type"])) else "term"
    term_ = wp_unslash(PHP_REQUEST["s"]) if (php_isset(lambda : PHP_REQUEST["s"])) else ""
    if (not type_selector_):
        php_print("<p class=\"install-help\">" + __("Search for themes by keyword.") + "</p>")
    # end if
    php_print("<form id=\"search-themes\" method=\"get\">\n <input type=\"hidden\" name=\"tab\" value=\"search\" />\n   ")
    if type_selector_:
        php_print(" <label class=\"screen-reader-text\" for=\"typeselector\">")
        _e("Type of search")
        php_print("</label>\n   <select name=\"type\" id=\"typeselector\">\n    <option value=\"term\" ")
        selected("term", type_)
        php_print(">")
        _e("Keyword")
        php_print("</option>\n  <option value=\"author\" ")
        selected("author", type_)
        php_print(">")
        _e("Author")
        php_print("</option>\n  <option value=\"tag\" ")
        selected("tag", type_)
        php_print(">")
        _ex("Tag", "Theme Installer")
        php_print("""</option>
        </select>
        <label class=\"screen-reader-text\" for=\"s\">
        """)
        for case in Switch(type_):
            if case("term"):
                _e("Search by keyword")
                break
            # end if
            if case("author"):
                _e("Search by author")
                break
            # end if
            if case("tag"):
                _e("Search by tag")
                break
            # end if
        # end for
        php_print(" </label>\n  ")
    else:
        php_print(" <label class=\"screen-reader-text\" for=\"s\">")
        _e("Search by keyword")
        php_print("</label>\n   ")
    # end if
    php_print(" <input type=\"search\" name=\"s\" id=\"s\" size=\"30\" value=\"")
    php_print(esc_attr(term_))
    php_print("\" autofocus=\"autofocus\" />\n  ")
    submit_button(__("Search"), "", "search", False)
    php_print("</form>\n    ")
# end def install_theme_search_form
#// 
#// Display tags filter for themes.
#// 
#// @since 2.8.0
#//
def install_themes_dashboard(*_args_):
    
    
    install_theme_search_form(False)
    php_print("<h4>")
    _e("Feature Filter")
    php_print("</h4>\n<p class=\"install-help\">")
    _e("Find a theme based on specific features.")
    php_print("""</p>
    <form method=\"get\">
    <input type=\"hidden\" name=\"tab\" value=\"search\" />
    """)
    feature_list_ = get_theme_feature_list()
    php_print("<div class=\"feature-filter\">")
    for feature_name_,features_ in feature_list_:
        feature_name_ = esc_html(feature_name_)
        php_print("<div class=\"feature-name\">" + feature_name_ + "</div>")
        php_print("<ol class=\"feature-group\">")
        for feature_,feature_name_ in features_:
            feature_name_ = esc_html(feature_name_)
            feature_ = esc_attr(feature_)
            php_print("\n<li>\n <input type=\"checkbox\" name=\"features[]\" id=\"feature-id-")
            php_print(feature_)
            php_print("\" value=\"")
            php_print(feature_)
            php_print("\" />\n  <label for=\"feature-id-")
            php_print(feature_)
            php_print("\">")
            php_print(feature_name_)
            php_print("""</label>
            </li>
            """)
        # end for
        php_print("</ol>\n<br class=\"clear\" />\n      ")
    # end for
    php_print("""
    </div>
    <br class=\"clear\" />
    """)
    submit_button(__("Find Themes"), "", "search")
    php_print("</form>\n    ")
# end def install_themes_dashboard
#// 
#// @since 2.8.0
#//
def install_themes_upload(*_args_):
    
    
    php_print("<p class=\"install-help\">")
    _e("If you have a theme in a .zip format, you may install it by uploading it here.")
    php_print("</p>\n<form method=\"post\" enctype=\"multipart/form-data\" class=\"wp-upload-form\" action=\"")
    php_print(self_admin_url("update.php?action=upload-theme"))
    php_print("\">\n    ")
    wp_nonce_field("theme-upload")
    php_print(" <label class=\"screen-reader-text\" for=\"themezip\">")
    _e("Theme zip file")
    php_print("</label>\n   <input type=\"file\" id=\"themezip\" name=\"themezip\" />\n ")
    submit_button(__("Install Now"), "", "install-theme-submit", False)
    php_print("</form>\n    ")
# end def install_themes_upload
#// 
#// Prints a theme on the Install Themes pages.
#// 
#// @deprecated 3.4.0
#// 
#// @global WP_Theme_Install_List_Table $wp_list_table
#// 
#// @param object $theme
#//
def display_theme(theme_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0")
    global wp_list_table_
    php_check_if_defined("wp_list_table_")
    if (not (php_isset(lambda : wp_list_table_))):
        wp_list_table_ = _get_list_table("WP_Theme_Install_List_Table")
    # end if
    wp_list_table_.prepare_items()
    wp_list_table_.single_row(theme_)
# end def display_theme
#// 
#// Display theme content based on theme list.
#// 
#// @since 2.8.0
#// 
#// @global WP_Theme_Install_List_Table $wp_list_table
#//
def display_themes(*_args_):
    
    
    global wp_list_table_
    php_check_if_defined("wp_list_table_")
    if (not (php_isset(lambda : wp_list_table_))):
        wp_list_table_ = _get_list_table("WP_Theme_Install_List_Table")
    # end if
    wp_list_table_.prepare_items()
    wp_list_table_.display()
# end def display_themes
#// 
#// Display theme information in dialog box form.
#// 
#// @since 2.8.0
#// 
#// @global WP_Theme_Install_List_Table $wp_list_table
#//
def install_theme_information(*_args_):
    
    
    global wp_list_table_
    php_check_if_defined("wp_list_table_")
    theme_ = themes_api("theme_information", Array({"slug": wp_unslash(PHP_REQUEST["theme"])}))
    if is_wp_error(theme_):
        wp_die(theme_)
    # end if
    iframe_header(__("Theme Installation"))
    if (not (php_isset(lambda : wp_list_table_))):
        wp_list_table_ = _get_list_table("WP_Theme_Install_List_Table")
    # end if
    wp_list_table_.theme_installer_single(theme_)
    iframe_footer()
    php_exit(0)
# end def install_theme_information
