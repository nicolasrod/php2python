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
def wp_credits(*_args_):
    
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    locale_ = get_user_locale()
    results_ = get_site_transient("wordpress_credits_" + locale_)
    if (not php_is_array(results_)) or False != php_strpos(wp_version_, "-") or (php_isset(lambda : results_["data"]["version"])) and php_strpos(wp_version_, results_["data"]["version"]) != 0:
        url_ = str("http://api.wordpress.org/core/credits/1.1/?version=") + str(wp_version_) + str("&locale=") + str(locale_)
        options_ = Array({"user-agent": "WordPress/" + wp_version_ + "; " + home_url("/")})
        if wp_http_supports(Array("ssl")):
            url_ = set_url_scheme(url_, "https")
        # end if
        response_ = wp_remote_get(url_, options_)
        if is_wp_error(response_) or 200 != wp_remote_retrieve_response_code(response_):
            return False
        # end if
        results_ = php_json_decode(wp_remote_retrieve_body(response_), True)
        if (not php_is_array(results_)):
            return False
        # end if
        set_site_transient("wordpress_credits_" + locale_, results_, DAY_IN_SECONDS)
    # end if
    return results_
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
def _wp_credits_add_profile_link(display_name_=None, username_=None, profiles_=None, *_args_):
    
    
    display_name_ = "<a href=\"" + esc_url(php_sprintf(profiles_, username_)) + "\">" + esc_html(display_name_) + "</a>"
# end def _wp_credits_add_profile_link
#// 
#// Retrieve the link to an external library used in WordPress.
#// 
#// @access private
#// @since 3.2.0
#// 
#// @param string $data External library data (passed by reference).
#//
def _wp_credits_build_object_link(data_=None, *_args_):
    
    
    data_ = "<a href=\"" + esc_url(data_[1]) + "\">" + esc_html(data_[0]) + "</a>"
# end def _wp_credits_build_object_link
#// 
#// Displays the title for a given group of contributors.
#// 
#// @since 5.3.0
#// 
#// @param array $group_data The current contributor group.
#//
def wp_credits_section_title(group_data_=None, *_args_):
    if group_data_ is None:
        group_data_ = Array()
    # end if
    
    if (not php_count(group_data_)):
        return
    # end if
    if group_data_["name"]:
        if "Translators" == group_data_["name"]:
            #// Considered a special slug in the API response. (Also, will never be returned for en_US.)
            title_ = _x("Translators", "Translate this to be the equivalent of English Translators in your language for the credits page Translators section")
        elif (php_isset(lambda : group_data_["placeholders"])):
            #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
            title_ = vsprintf(translate(group_data_["name"]), group_data_["placeholders"])
        else:
            #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
            title_ = translate(group_data_["name"])
        # end if
        php_print("<h2 class=\"wp-people-group-title\">" + esc_html(title_) + "</h2>\n")
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
def wp_credits_section_list(credits_=None, slug_="", *_args_):
    if credits_ is None:
        credits_ = Array()
    # end if
    
    group_data_ = credits_["groups"][slug_] if (php_isset(lambda : credits_["groups"][slug_])) else Array()
    credits_data_ = credits_["data"]
    if (not php_count(group_data_)):
        return
    # end if
    if (not php_empty(lambda : group_data_["shuffle"])):
        shuffle(group_data_["data"])
        pass
    # end if
    for case in Switch(group_data_["type"]):
        if case("list"):
            php_array_walk(group_data_["data"], "_wp_credits_add_profile_link", credits_data_["profiles"])
            php_print("<p class=\"wp-credits-list\">" + wp_sprintf("%l.", group_data_["data"]) + "</p>\n\n")
            break
        # end if
        if case("libraries"):
            php_array_walk(group_data_["data"], "_wp_credits_build_object_link")
            php_print("<p class=\"wp-credits-list\">" + wp_sprintf("%l.", group_data_["data"]) + "</p>\n\n")
            break
        # end if
        if case():
            compact_ = "compact" == group_data_["type"]
            classes_ = "wp-people-group " + "compact" if compact_ else ""
            php_print("<ul class=\"" + classes_ + "\" id=\"wp-people-group-" + slug_ + "\">" + "\n")
            for person_data_ in group_data_["data"]:
                php_print("<li class=\"wp-person\" id=\"wp-person-" + esc_attr(person_data_[2]) + "\">" + "\n   ")
                php_print("<a href=\"" + esc_url(php_sprintf(credits_data_["profiles"], person_data_[2])) + "\" class=\"web\">")
                size_ = 40 if compact_ else 80
                data_ = get_avatar_data(person_data_[1] + "@md5.gravatar.com", Array({"size": size_}))
                data2x_ = get_avatar_data(person_data_[1] + "@md5.gravatar.com", Array({"size": size_ * 2}))
                php_print("<img src=\"" + esc_url(data_["url"]) + "\" srcset=\"" + esc_url(data2x_["url"]) + " 2x\" class=\"gravatar\" alt=\"\" />" + "\n")
                php_print(esc_html(person_data_[0]) + "</a>\n   ")
                if (not compact_):
                    #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
                    php_print("<span class=\"title\">" + translate(person_data_[3]) + "</span>\n")
                # end if
                php_print("</li>\n")
            # end for
            php_print("</ul>\n")
            break
        # end if
    # end for
# end def wp_credits_section_list
