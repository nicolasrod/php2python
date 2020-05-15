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
#// WordPress Credits Administration API.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Retrieve the contributor credits.
#// 
#// @since 3.2.0
#// 
#// @return array|false A list of all of the contributors, or false on error.
#//
def wp_credits(*args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    locale = get_user_locale()
    results = get_site_transient("wordpress_credits_" + locale)
    if (not php_is_array(results)) or False != php_strpos(wp_version, "-") or (php_isset(lambda : results["data"]["version"])) and php_strpos(wp_version, results["data"]["version"]) != 0:
        url = str("http://api.wordpress.org/core/credits/1.1/?version=") + str(wp_version) + str("&locale=") + str(locale)
        options = Array({"user-agent": "WordPress/" + wp_version + "; " + home_url("/")})
        if wp_http_supports(Array("ssl")):
            url = set_url_scheme(url, "https")
        # end if
        response = wp_remote_get(url, options)
        if is_wp_error(response) or 200 != wp_remote_retrieve_response_code(response):
            return False
        # end if
        results = php_json_decode(wp_remote_retrieve_body(response), True)
        if (not php_is_array(results)):
            return False
        # end if
        set_site_transient("wordpress_credits_" + locale, results, DAY_IN_SECONDS)
    # end if
    return results
# end def wp_credits
#// 
#// Retrieve the link to a contributor's WordPress.org profile page.
#// 
#// @access private
#// @since 3.2.0
#// 
#// @param string $display_name  The contributor's display name (passed by reference).
#// @param string $username      The contributor's username.
#// @param string $profiles      URL to the contributor's WordPress.org profile page.
#//
def _wp_credits_add_profile_link(display_name=None, username=None, profiles=None, *args_):
    
    display_name = "<a href=\"" + esc_url(php_sprintf(profiles, username)) + "\">" + esc_html(display_name) + "</a>"
# end def _wp_credits_add_profile_link
#// 
#// Retrieve the link to an external library used in WordPress.
#// 
#// @access private
#// @since 3.2.0
#// 
#// @param string $data External library data (passed by reference).
#//
def _wp_credits_build_object_link(data=None, *args_):
    
    data = "<a href=\"" + esc_url(data[1]) + "\">" + esc_html(data[0]) + "</a>"
# end def _wp_credits_build_object_link
#// 
#// Displays the title for a given group of contributors.
#// 
#// @since 5.3.0
#// 
#// @param array $group_data The current contributor group.
#//
def wp_credits_section_title(group_data=Array(), *args_):
    
    if (not php_count(group_data)):
        return
    # end if
    if group_data["name"]:
        if "Translators" == group_data["name"]:
            #// Considered a special slug in the API response. (Also, will never be returned for en_US.)
            title = _x("Translators", "Translate this to be the equivalent of English Translators in your language for the credits page Translators section")
        elif (php_isset(lambda : group_data["placeholders"])):
            #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
            title = vsprintf(translate(group_data["name"]), group_data["placeholders"])
        else:
            #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
            title = translate(group_data["name"])
        # end if
        php_print("<h2 class=\"wp-people-group-title\">" + esc_html(title) + "</h2>\n")
    # end if
# end def wp_credits_section_title
#// 
#// Displays a list of contributors for a given group.
#// 
#// @since 5.3.0
#// 
#// @param array  $credits The credits groups returned from the API.
#// @param string $slug    The current group to display.
#//
def wp_credits_section_list(credits=Array(), slug="", *args_):
    
    group_data = credits["groups"][slug] if (php_isset(lambda : credits["groups"][slug])) else Array()
    credits_data = credits["data"]
    if (not php_count(group_data)):
        return
    # end if
    if (not php_empty(lambda : group_data["shuffle"])):
        shuffle(group_data["data"])
        pass
    # end if
    for case in Switch(group_data["type"]):
        if case("list"):
            array_walk(group_data["data"], "_wp_credits_add_profile_link", credits_data["profiles"])
            php_print("<p class=\"wp-credits-list\">" + wp_sprintf("%l.", group_data["data"]) + "</p>\n\n")
            break
        # end if
        if case("libraries"):
            array_walk(group_data["data"], "_wp_credits_build_object_link")
            php_print("<p class=\"wp-credits-list\">" + wp_sprintf("%l.", group_data["data"]) + "</p>\n\n")
            break
        # end if
        if case():
            compact = "compact" == group_data["type"]
            classes = "wp-people-group " + "compact" if compact else ""
            php_print("<ul class=\"" + classes + "\" id=\"wp-people-group-" + slug + "\">" + "\n")
            for person_data in group_data["data"]:
                php_print("<li class=\"wp-person\" id=\"wp-person-" + esc_attr(person_data[2]) + "\">" + "\n    ")
                php_print("<a href=\"" + esc_url(php_sprintf(credits_data["profiles"], person_data[2])) + "\" class=\"web\">")
                size = 40 if compact else 80
                data = get_avatar_data(person_data[1] + "@md5.gravatar.com", Array({"size": size}))
                data2x = get_avatar_data(person_data[1] + "@md5.gravatar.com", Array({"size": size * 2}))
                php_print("<img src=\"" + esc_url(data["url"]) + "\" srcset=\"" + esc_url(data2x["url"]) + " 2x\" class=\"gravatar\" alt=\"\" />" + "\n")
                php_print(esc_html(person_data[0]) + "</a>\n    ")
                if (not compact):
                    #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
                    php_print("<span class=\"title\">" + translate(person_data[3]) + "</span>\n")
                # end if
                php_print("</li>\n")
            # end for
            php_print("</ul>\n")
            break
        # end if
    # end for
# end def wp_credits_section_list
