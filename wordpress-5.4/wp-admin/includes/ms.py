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
#// Multisite administration functions.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// 
#// Determine if uploaded file exceeds space quota.
#// 
#// @since 3.0.0
#// 
#// @param array $file $_FILES array for a given file.
#// @return array $_FILES array with 'error' key set if file exceeds quota. 'error' is empty otherwise.
#//
def check_upload_size(file=None, *args_):
    
    if get_site_option("upload_space_check_disabled"):
        return file
    # end if
    if "0" != file["error"]:
        #// There's already an error.
        return file
    # end if
    if php_defined("WP_IMPORTING"):
        return file
    # end if
    space_left = get_upload_space_available()
    file_size = filesize(file["tmp_name"])
    if space_left < file_size:
        #// translators: %s: Required disk space in kilobytes.
        file["error"] = php_sprintf(__("Not enough space to upload. %s KB needed."), number_format(file_size - space_left / KB_IN_BYTES))
    # end if
    if file_size > KB_IN_BYTES * get_site_option("fileupload_maxk", 1500):
        #// translators: %s: Maximum allowed file size in kilobytes.
        file["error"] = php_sprintf(__("This file is too big. Files must be less than %s KB in size."), get_site_option("fileupload_maxk", 1500))
    # end if
    if upload_is_user_over_quota(False):
        file["error"] = __("You have used your space quota. Please delete files before uploading.")
    # end if
    if "0" != file["error"] and (not (php_isset(lambda : PHP_POST["html-upload"]))) and (not wp_doing_ajax()):
        wp_die(file["error"] + " <a href=\"javascript:history.go(-1)\">" + __("Back") + "</a>")
    # end if
    return file
# end def check_upload_size
#// 
#// Delete a site.
#// 
#// @since 3.0.0
#// @since 5.1.0 Use wp_delete_site() internally to delete the site row from the database.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int  $blog_id Site ID.
#// @param bool $drop    True if site's database tables should be dropped. Default is false.
#//
def wpmu_delete_blog(blog_id=None, drop=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    switch = False
    if get_current_blog_id() != blog_id:
        switch = True
        switch_to_blog(blog_id)
    # end if
    blog = get_site(blog_id)
    current_network = get_network()
    #// If a full blog object is not available, do not destroy anything.
    if drop and (not blog):
        drop = False
    # end if
    #// Don't destroy the initial, main, or root blog.
    if drop and 1 == blog_id or is_main_site(blog_id) or blog.path == current_network.path and blog.domain == current_network.domain:
        drop = False
    # end if
    upload_path = php_trim(get_option("upload_path"))
    #// If ms_files_rewriting is enabled and upload_path is empty, wp_upload_dir is not reliable.
    if drop and get_site_option("ms_files_rewriting") and php_empty(lambda : upload_path):
        drop = False
    # end if
    if drop:
        wp_delete_site(blog_id)
    else:
        #// This action is documented in wp-includes/ms-blogs.php
        do_action_deprecated("delete_blog", Array(blog_id, False), "5.1.0")
        users = get_users(Array({"blog_id": blog_id, "fields": "ids"}))
        #// Remove users from this blog.
        if (not php_empty(lambda : users)):
            for user_id in users:
                remove_user_from_blog(user_id, blog_id)
            # end for
        # end if
        update_blog_status(blog_id, "deleted", 1)
        #// This action is documented in wp-includes/ms-blogs.php
        do_action_deprecated("deleted_blog", Array(blog_id, False), "5.1.0")
    # end if
    if switch:
        restore_current_blog()
    # end if
# end def wpmu_delete_blog
#// 
#// Delete a user from the network and remove from all sites.
#// 
#// @since 3.0.0
#// 
#// @todo Merge with wp_delete_user()?
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $id The user ID.
#// @return bool True if the user was deleted, otherwise false.
#//
def wpmu_delete_user(id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not php_is_numeric(id)):
        return False
    # end if
    id = int(id)
    user = php_new_class("WP_User", lambda : WP_User(id))
    if (not user.exists()):
        return False
    # end if
    #// Global super-administrators are protected, and cannot be deleted.
    _super_admins = get_super_admins()
    if php_in_array(user.user_login, _super_admins, True):
        return False
    # end if
    #// 
    #// Fires before a user is deleted from the network.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int $id ID of the user about to be deleted from the network.
    #//
    do_action("wpmu_delete_user", id)
    blogs = get_blogs_of_user(id)
    if (not php_empty(lambda : blogs)):
        for blog in blogs:
            switch_to_blog(blog.userblog_id)
            remove_user_from_blog(id, blog.userblog_id)
            post_ids = wpdb.get_col(wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_author = %d"), id))
            for post_id in post_ids:
                wp_delete_post(post_id)
            # end for
            #// Clean links.
            link_ids = wpdb.get_col(wpdb.prepare(str("SELECT link_id FROM ") + str(wpdb.links) + str(" WHERE link_owner = %d"), id))
            if link_ids:
                for link_id in link_ids:
                    wp_delete_link(link_id)
                # end for
            # end if
            restore_current_blog()
        # end for
    # end if
    meta = wpdb.get_col(wpdb.prepare(str("SELECT umeta_id FROM ") + str(wpdb.usermeta) + str(" WHERE user_id = %d"), id))
    for mid in meta:
        delete_metadata_by_mid("user", mid)
    # end for
    wpdb.delete(wpdb.users, Array({"ID": id}))
    clean_user_cache(user)
    #// This action is documented in wp-admin/includes/user.php
    do_action("deleted_user", id, None)
    return True
# end def wpmu_delete_user
#// 
#// Check whether a site has used its allotted upload space.
#// 
#// @since MU (3.0.0)
#// 
#// @param bool $echo Optional. If $echo is set and the quota is exceeded, a warning message is echoed. Default is true.
#// @return bool True if user is over upload space quota, otherwise false.
#//
def upload_is_user_over_quota(echo=True, *args_):
    
    if get_site_option("upload_space_check_disabled"):
        return False
    # end if
    space_allowed = get_space_allowed()
    if (not php_is_numeric(space_allowed)):
        space_allowed = 10
        pass
    # end if
    space_used = get_space_used()
    if space_allowed - space_used < 0:
        if echo:
            printf(__("Sorry, you have used your space allocation of %s. Please delete some files to upload more files."), size_format(space_allowed * MB_IN_BYTES))
        # end if
        return True
    else:
        return False
    # end if
# end def upload_is_user_over_quota
#// 
#// Displays the amount of disk space used by the current site. Not used in core.
#// 
#// @since MU (3.0.0)
#//
def display_space_usage(*args_):
    
    space_allowed = get_space_allowed()
    space_used = get_space_used()
    percent_used = space_used / space_allowed * 100
    space = size_format(space_allowed * MB_IN_BYTES)
    php_print(" <strong>\n  ")
    #// translators: Storage space that's been used. 1: Percentage of used space, 2: Total space allowed in megabytes or gigabytes.
    printf(__("Used: %1$s%% of %2$s"), number_format(percent_used), space)
    php_print(" </strong>\n ")
# end def display_space_usage
#// 
#// Get the remaining upload space for this site.
#// 
#// @since MU (3.0.0)
#// 
#// @param int $size Current max size in bytes
#// @return int Max size in bytes
#//
def fix_import_form_size(size=None, *args_):
    
    if upload_is_user_over_quota(False):
        return 0
    # end if
    available = get_upload_space_available()
    return php_min(size, available)
# end def fix_import_form_size
#// 
#// Displays the site upload space quota setting form on the Edit Site Settings screen.
#// 
#// @since 3.0.0
#// 
#// @param int $id The ID of the site to display the setting for.
#//
def upload_space_setting(id=None, *args_):
    
    switch_to_blog(id)
    quota = get_option("blog_upload_space")
    restore_current_blog()
    if (not quota):
        quota = ""
    # end if
    php_print(" <tr>\n      <th><label for=\"blog-upload-space-number\">")
    _e("Site Upload Space Quota")
    php_print("</label></th>\n      <td>\n          <input type=\"number\" step=\"1\" min=\"0\" style=\"width: 100px\" name=\"option[blog_upload_space]\" id=\"blog-upload-space-number\" aria-describedby=\"blog-upload-space-desc\" value=\"")
    php_print(quota)
    php_print("\" />\n          <span id=\"blog-upload-space-desc\"><span class=\"screen-reader-text\">")
    _e("Size in megabytes")
    php_print("</span> ")
    _e("MB (Leave blank for network default)")
    php_print("""</span>
    </td>
    </tr>
    """)
# end def upload_space_setting
#// 
#// Cleans the user cache for a specific user.
#// 
#// @since 3.0.0
#// 
#// @param int $id The user ID.
#// @return bool|int The ID of the refreshed user or false if the user does not exist.
#//
def refresh_user_details(id=None, *args_):
    
    id = int(id)
    user = get_userdata(id)
    if (not user):
        return False
    # end if
    clean_user_cache(user)
    return id
# end def refresh_user_details
#// 
#// Returns the language for a language code.
#// 
#// @since 3.0.0
#// 
#// @param string $code Optional. The two-letter language code. Default empty.
#// @return string The language corresponding to $code if it exists. If it does not exist,
#// then the first two letters of $code is returned.
#//
def format_code_lang(code="", *args_):
    
    code = php_strtolower(php_substr(code, 0, 2))
    lang_codes = Array({"aa": "Afar", "ab": "Abkhazian", "af": "Afrikaans", "ak": "Akan", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "an": "Aragonese", "hy": "Armenian", "as": "Assamese", "av": "Avaric", "ae": "Avestan", "ay": "Aymara", "az": "Azerbaijani", "ba": "Bashkir", "bm": "Bambara", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bh": "Bihari", "bi": "Bislama", "bs": "Bosnian", "br": "Breton", "bg": "Bulgarian", "my": "Burmese", "ca": "Catalan; Valencian", "ch": "Chamorro", "ce": "Chechen", "zh": "Chinese", "cu": "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic", "cv": "Chuvash", "kw": "Cornish", "co": "Corsican", "cr": "Cree", "cs": "Czech", "da": "Danish", "dv": "Divehi; Dhivehi; Maldivian", "nl": "Dutch; Flemish", "dz": "Dzongkha", "en": "English", "eo": "Esperanto", "et": "Estonian", "ee": "Ewe", "fo": "Faroese", "fj": "Fijjian", "fi": "Finnish", "fr": "French", "fy": "Western Frisian", "ff": "Fulah", "ka": "Georgian", "de": "German", "gd": "Gaelic; Scottish Gaelic", "ga": "Irish", "gl": "Galician", "gv": "Manx", "el": "Greek, Modern", "gn": "Guarani", "gu": "Gujarati", "ht": "Haitian; Haitian Creole", "ha": "Hausa", "he": "Hebrew", "hz": "Herero", "hi": "Hindi", "ho": "Hiri Motu", "hu": "Hungarian", "ig": "Igbo", "is": "Icelandic", "io": "Ido", "ii": "Sichuan Yi", "iu": "Inuktitut", "ie": "Interlingue", "ia": "Interlingua (International Auxiliary Language Association)", "id": "Indonesian", "ik": "Inupiaq", "it": "Italian", "jv": "Javanese", "ja": "Japanese", "kl": "Kalaallisut; Greenlandic", "kn": "Kannada", "ks": "Kashmiri", "kr": "Kanuri", "kk": "Kazakh", "km": "Central Khmer", "ki": "Kikuyu; Gikuyu", "rw": "Kinyarwanda", "ky": "Kirghiz; Kyrgyz", "kv": "Komi", "kg": "Kongo", "ko": "Korean", "kj": "Kuanyama; Kwanyama", "ku": "Kurdish", "lo": "Lao", "la": "Latin", "lv": "Latvian", "li": "Limburgan; Limburger; Limburgish", "ln": "Lingala", "lt": "Lithuanian", "lb": "Luxembourgish; Letzeburgesch", "lu": "Luba-Katanga", "lg": "Ganda", "mk": "Macedonian", "mh": "Marshallese", "ml": "Malayalam", "mi": "Maori", "mr": "Marathi", "ms": "Malay", "mg": "Malagasy", "mt": "Maltese", "mo": "Moldavian", "mn": "Mongolian", "na": "Nauru", "nv": "Navajo; Navaho", "nr": "Ndebele, South; South Ndebele", "nd": "Ndebele, North; North Ndebele", "ng": "Ndonga", "ne": "Nepali", "nn": "Norwegian Nynorsk; Nynorsk, Norwegian", "nb": "BokmÃ¥l, Norwegian, Norwegian BokmÃ¥l", "no": "Norwegian", "ny": "Chichewa; Chewa; Nyanja", "oc": "Occitan, ProvenÃ§al", "oj": "Ojibwa", "or": "Oriya", "om": "Oromo", "os": "Ossetian; Ossetic", "pa": "Panjabi; Punjabi", "fa": "Persian", "pi": "Pali", "pl": "Polish", "pt": "Portuguese", "ps": "Pushto", "qu": "Quechua", "rm": "Romansh", "ro": "Romanian", "rn": "Rundi", "ru": "Russian", "sg": "Sango", "sa": "Sanskrit", "sr": "Serbian", "hr": "Croatian", "si": "Sinhala; Sinhalese", "sk": "Slovak", "sl": "Slovenian", "se": "Northern Sami", "sm": "Samoan", "sn": "Shona", "sd": "Sindhi", "so": "Somali", "st": "Sotho, Southern", "es": "Spanish; Castilian", "sc": "Sardinian", "ss": "Swati", "su": "Sundanese", "sw": "Swahili", "sv": "Swedish", "ty": "Tahitian", "ta": "Tamil", "tt": "Tatar", "te": "Telugu", "tg": "Tajik", "tl": "Tagalog", "th": "Thai", "bo": "Tibetan", "ti": "Tigrinya", "to": "Tonga (Tonga Islands)", "tn": "Tswana", "ts": "Tsonga", "tk": "Turkmen", "tr": "Turkish", "tw": "Twi", "ug": "Uighur; Uyghur", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "ve": "Venda", "vi": "Vietnamese", "vo": "VolapÃ¼k", "cy": "Welsh", "wa": "Walloon", "wo": "Wolof", "xh": "Xhosa", "yi": "Yiddish", "yo": "Yoruba", "za": "Zhuang; Chuang", "zu": "Zulu"})
    #// 
    #// Filters the language codes.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string[] $lang_codes Array of key/value pairs of language codes where key is the short version.
    #// @param string   $code       A two-letter designation of the language.
    #//
    lang_codes = apply_filters("lang_codes", lang_codes, code)
    return php_strtr(code, lang_codes)
# end def format_code_lang
#// 
#// Synchronizes category and post tag slugs when global terms are enabled.
#// 
#// @since 3.0.0
#// 
#// @param WP_Term|array $term     The term.
#// @param string        $taxonomy The taxonomy for `$term`. Should be 'category' or 'post_tag', as these are
#// the only taxonomies which are processed by this function; anything else
#// will be returned untouched.
#// @return WP_Term|array Returns `$term`, after filtering the 'slug' field with `sanitize_title()`
#// if `$taxonomy` is 'category' or 'post_tag'.
#//
def sync_category_tag_slugs(term=None, taxonomy=None, *args_):
    
    if global_terms_enabled() and "category" == taxonomy or "post_tag" == taxonomy:
        if php_is_object(term):
            term.slug = sanitize_title(term.name)
        else:
            term["slug"] = sanitize_title(term["name"])
        # end if
    # end if
    return term
# end def sync_category_tag_slugs
#// 
#// Displays an access denied message when a user tries to view a site's dashboard they
#// do not have access to.
#// 
#// @since 3.2.0
#// @access private
#//
def _access_denied_splash(*args_):
    
    if (not is_user_logged_in()) or is_network_admin():
        return
    # end if
    blogs = get_blogs_of_user(get_current_user_id())
    if wp_list_filter(blogs, Array({"userblog_id": get_current_blog_id()})):
        return
    # end if
    blog_name = get_bloginfo("name")
    if php_empty(lambda : blogs):
        wp_die(php_sprintf(__("You attempted to access the \"%1$s\" dashboard, but you do not currently have privileges on this site. If you believe you should be able to access the \"%1$s\" dashboard, please contact your network administrator."), blog_name), 403)
    # end if
    output = "<p>" + php_sprintf(__("You attempted to access the \"%1$s\" dashboard, but you do not currently have privileges on this site. If you believe you should be able to access the \"%1$s\" dashboard, please contact your network administrator."), blog_name) + "</p>"
    output += "<p>" + __("If you reached this screen by accident and meant to visit one of your own sites, here are some shortcuts to help you find your way.") + "</p>"
    output += "<h3>" + __("Your Sites") + "</h3>"
    output += "<table>"
    for blog in blogs:
        output += "<tr>"
        output += str("<td>") + str(blog.blogname) + str("</td>")
        output += "<td><a href=\"" + esc_url(get_admin_url(blog.userblog_id)) + "\">" + __("Visit Dashboard") + "</a> | " + "<a href=\"" + esc_url(get_home_url(blog.userblog_id)) + "\">" + __("View Site") + "</a></td>"
        output += "</tr>"
    # end for
    output += "</table>"
    wp_die(output, 403)
# end def _access_denied_splash
#// 
#// Checks if the current user has permissions to import new users.
#// 
#// @since 3.0.0
#// 
#// @param string $permission A permission to be checked. Currently not used.
#// @return bool True if the user has proper permissions, false if they do not.
#//
def check_import_new_users(permission=None, *args_):
    
    if (not current_user_can("manage_network_users")):
        return False
    # end if
    return True
# end def check_import_new_users
#// See "import_allow_fetch_attachments" and "import_attachment_size_limit" filters too.
#// 
#// Generates and displays a drop-down of available languages.
#// 
#// @since 3.0.0
#// 
#// @param string[] $lang_files Optional. An array of the language files. Default empty array.
#// @param string   $current    Optional. The current language code. Default empty.
#//
def mu_dropdown_languages(lang_files=Array(), current="", *args_):
    
    flag = False
    output = Array()
    for val in lang_files:
        code_lang = php_basename(val, ".mo")
        if "en_US" == code_lang:
            #// American English.
            flag = True
            ae = __("American English")
            output[ae] = "<option value=\"" + esc_attr(code_lang) + "\"" + selected(current, code_lang, False) + "> " + ae + "</option>"
        elif "en_GB" == code_lang:
            #// British English.
            flag = True
            be = __("British English")
            output[be] = "<option value=\"" + esc_attr(code_lang) + "\"" + selected(current, code_lang, False) + "> " + be + "</option>"
        else:
            translated = format_code_lang(code_lang)
            output[translated] = "<option value=\"" + esc_attr(code_lang) + "\"" + selected(current, code_lang, False) + "> " + esc_html(translated) + "</option>"
        # end if
    # end for
    if False == flag:
        #// WordPress English.
        output[-1] = "<option value=\"\"" + selected(current, "", False) + ">" + __("English") + "</option>"
    # end if
    #// Order by name.
    uksort(output, "strnatcasecmp")
    #// 
    #// Filters the languages available in the dropdown.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string[] $output     Array of HTML output for the dropdown.
    #// @param string[] $lang_files Array of available language files.
    #// @param string   $current    The current language code.
    #//
    output = apply_filters("mu_dropdown_languages", output, lang_files, current)
    php_print(php_implode("\n   ", output))
# end def mu_dropdown_languages
#// 
#// Displays an admin notice to upgrade all sites after a core upgrade.
#// 
#// @since 3.0.0
#// 
#// @global int    $wp_db_version WordPress database version.
#// @global string $pagenow
#// 
#// @return false False if the current user is not a super admin.
#//
def site_admin_notice(*args_):
    
    global wp_db_version,pagenow
    php_check_if_defined("wp_db_version","pagenow")
    if (not current_user_can("upgrade_network")):
        return False
    # end if
    if "upgrade.php" == pagenow:
        return
    # end if
    if get_site_option("wpmu_upgrade_site") != wp_db_version:
        php_print("<div class='update-nag'>" + php_sprintf(__("Thank you for Updating! Please visit the <a href=\"%s\">Upgrade Network</a> page to update all your sites."), esc_url(network_admin_url("upgrade.php"))) + "</div>")
    # end if
# end def site_admin_notice
#// 
#// Avoids a collision between a site slug and a permalink slug.
#// 
#// In a subdirectory installation this will make sure that a site and a post do not use the
#// same subdirectory by checking for a site with the same name as a new post.
#// 
#// @since 3.0.0
#// 
#// @param array $data    An array of post data.
#// @param array $postarr An array of posts. Not currently used.
#// @return array The new array of post data after checking for collisions.
#//
def avoid_blog_page_permalink_collision(data=None, postarr=None, *args_):
    
    if is_subdomain_install():
        return data
    # end if
    if "page" != data["post_type"]:
        return data
    # end if
    if (not (php_isset(lambda : data["post_name"]))) or "" == data["post_name"]:
        return data
    # end if
    if (not is_main_site()):
        return data
    # end if
    post_name = data["post_name"]
    c = 0
    while True:
        
        if not (c < 10 and get_id_from_blogname(post_name)):
            break
        # end if
        post_name += mt_rand(1, 10)
        c += 1
    # end while
    if post_name != data["post_name"]:
        data["post_name"] = post_name
    # end if
    return data
# end def avoid_blog_page_permalink_collision
#// 
#// Handles the display of choosing a user's primary site.
#// 
#// This displays the user's primary site and allows the user to choose
#// which site is primary.
#// 
#// @since 3.0.0
#//
def choose_primary_blog(*args_):
    
    php_print(" <table class=\"form-table\" role=\"presentation\">\n    <tr>\n  ")
    pass
    php_print("     <th scope=\"row\"><label for=\"primary_blog\">")
    _e("Primary Site")
    php_print("</label></th>\n      <td>\n      ")
    all_blogs = get_blogs_of_user(get_current_user_id())
    primary_blog = get_user_meta(get_current_user_id(), "primary_blog", True)
    if php_count(all_blogs) > 1:
        found = False
        php_print("         <select name=\"primary_blog\" id=\"primary_blog\">\n                ")
        for blog in all_blogs:
            if primary_blog == blog.userblog_id:
                found = True
            # end if
            php_print("                 <option value=\"")
            php_print(blog.userblog_id)
            php_print("\"")
            selected(primary_blog, blog.userblog_id)
            php_print(">")
            php_print(esc_url(get_home_url(blog.userblog_id)))
            php_print("</option>\n                  ")
        # end for
        php_print("         </select>\n         ")
        if (not found):
            blog = reset(all_blogs)
            update_user_meta(get_current_user_id(), "primary_blog", blog.userblog_id)
        # end if
    elif php_count(all_blogs) == 1:
        blog = reset(all_blogs)
        php_print(esc_url(get_home_url(blog.userblog_id)))
        if primary_blog != blog.userblog_id:
            #// Set the primary blog again if it's out of sync with blog list.
            update_user_meta(get_current_user_id(), "primary_blog", blog.userblog_id)
        # end if
    else:
        php_print("N/A")
    # end if
    php_print("""       </td>
    </tr>
    </table>
    """)
# end def choose_primary_blog
#// 
#// Whether or not we can edit this network from this page.
#// 
#// By default editing of network is restricted to the Network Admin for that `$network_id`.
#// This function allows for this to be overridden.
#// 
#// @since 3.1.0
#// 
#// @param int $network_id The network ID to check.
#// @return bool True if network can be edited, otherwise false.
#//
def can_edit_network(network_id=None, *args_):
    
    if get_current_network_id() == network_id:
        result = True
    else:
        result = False
    # end if
    #// 
    #// Filters whether this network can be edited from this page.
    #// 
    #// @since 3.1.0
    #// 
    #// @param bool $result     Whether the network can be edited from this page.
    #// @param int  $network_id The network ID to check.
    #//
    return apply_filters("can_edit_network", result, network_id)
# end def can_edit_network
#// 
#// Thickbox image paths for Network Admin.
#// 
#// @since 3.1.0
#// 
#// @access private
#//
def _thickbox_path_admin_subfolder(*args_):
    
    php_print("<script type=\"text/javascript\">\nvar tb_pathToImage = \"")
    php_print(includes_url("js/thickbox/loadingAnimation.gif", "relative"))
    php_print("\";\n</script>\n ")
# end def _thickbox_path_admin_subfolder
#// 
#// @param array $users
#//
def confirm_delete_users(users=None, *args_):
    
    current_user = wp_get_current_user()
    if (not php_is_array(users)) or php_empty(lambda : users):
        return False
    # end if
    php_print(" <h1>")
    esc_html_e("Users")
    php_print("</h1>\n\n    ")
    if 1 == php_count(users):
        php_print("     <p>")
        _e("You have chosen to delete the user from all networks and sites.")
        php_print("</p>\n   ")
    else:
        php_print("     <p>")
        _e("You have chosen to delete the following users from all networks and sites.")
        php_print("</p>\n   ")
    # end if
    php_print("""
    <form action=\"users.php?action=dodelete\" method=\"post\">
    <input type=\"hidden\" name=\"dodelete\" />
    """)
    wp_nonce_field("ms-users-delete")
    site_admins = get_super_admins()
    admin_out = "<option value=\"" + esc_attr(current_user.ID) + "\">" + current_user.user_login + "</option>"
    php_print(" <table class=\"form-table\" role=\"presentation\">\n    ")
    allusers = PHP_POST["allusers"]
    for user_id in allusers:
        if "" != user_id and "0" != user_id:
            delete_user = get_userdata(user_id)
            if (not current_user_can("delete_user", delete_user.ID)):
                wp_die(php_sprintf(__("Warning! User %s cannot be deleted."), delete_user.user_login))
            # end if
            if php_in_array(delete_user.user_login, site_admins):
                wp_die(php_sprintf(__("Warning! User cannot be deleted. The user %s is a network administrator."), "<em>" + delete_user.user_login + "</em>"))
            # end if
            php_print("         <tr>\n              <th scope=\"row\">")
            php_print(delete_user.user_login)
            php_print("                 ")
            php_print("<input type=\"hidden\" name=\"user[]\" value=\"" + esc_attr(user_id) + "\" />" + "\n")
            php_print("             </th>\n         ")
            blogs = get_blogs_of_user(user_id, True)
            if (not php_empty(lambda : blogs)):
                php_print("             <td><fieldset><p><legend>\n             ")
                printf(__("What should be done with content owned by %s?"), "<em>" + delete_user.user_login + "</em>")
                php_print("             </legend></p>\n             ")
                for key,details in blogs:
                    blog_users = get_users(Array({"blog_id": details.userblog_id, "fields": Array("ID", "user_login")}))
                    if php_is_array(blog_users) and (not php_empty(lambda : blog_users)):
                        user_site = "<a href='" + esc_url(get_home_url(details.userblog_id)) + str("'>") + str(details.blogname) + str("</a>")
                        user_dropdown = "<label for=\"reassign_user\" class=\"screen-reader-text\">" + __("Select a user") + "</label>"
                        user_dropdown += str("<select name='blog[") + str(user_id) + str("][") + str(key) + str("]' id='reassign_user'>")
                        user_list = ""
                        for user in blog_users:
                            if (not php_in_array(user.ID, allusers)):
                                user_list += str("<option value='") + str(user.ID) + str("'>") + str(user.user_login) + str("</option>")
                            # end if
                        # end for
                        if "" == user_list:
                            user_list = admin_out
                        # end if
                        user_dropdown += user_list
                        user_dropdown += "</select>\n"
                        php_print("                     <ul style=\"list-style:none;\">\n                           <li>\n                              ")
                        #// translators: %s: Link to user's site.
                        printf(__("Site: %s"), user_site)
                        php_print("                         </li>\n                         <li><label><input type=\"radio\" id=\"delete_option0\" name=\"delete[")
                        php_print(details.userblog_id + "][" + delete_user.ID)
                        php_print("]\" value=\"delete\" checked=\"checked\" />\n                            ")
                        _e("Delete all content.")
                        php_print("</label></li>\n                          <li><label><input type=\"radio\" id=\"delete_option1\" name=\"delete[")
                        php_print(details.userblog_id + "][" + delete_user.ID)
                        php_print("]\" value=\"reassign\" />\n                          ")
                        _e("Attribute all content to:")
                        php_print("</label>\n                           ")
                        php_print(user_dropdown)
                        php_print("</li>\n                      </ul>\n                     ")
                    # end if
                # end for
                php_print("</fieldset></td></tr>")
            else:
                php_print("             <td><p>")
                _e("User has no sites or content and will be deleted.")
                php_print("</p></td>\n          ")
            # end if
            php_print("         </tr>\n         ")
        # end if
    # end for
    php_print(" </table>\n  ")
    #// This action is documented in wp-admin/users.php
    do_action("delete_user_form", current_user, allusers)
    if 1 == php_count(users):
        php_print("     <p>")
        _e("Once you hit &#8220;Confirm Deletion&#8221;, the user will be permanently removed.")
        php_print("</p>\n   ")
    else:
        php_print("     <p>")
        _e("Once you hit &#8220;Confirm Deletion&#8221;, these users will be permanently removed.")
        php_print("</p>\n       ")
    # end if
    submit_button(__("Confirm Deletion"), "primary")
    php_print(" </form>\n   ")
    return True
# end def confirm_delete_users
#// 
#// Print JavaScript in the header on the Network Settings screen.
#// 
#// @since 4.1.0
#//
def network_settings_add_js(*args_):
    
    php_print("""<script type=\"text/javascript\">
    jQuery(document).ready( function($) {
    var languageSelect = $( '#WPLANG' );
    $( 'form' ).submit( function() {
    // Don't show a spinner for English and installed languages,
    // as there is nothing to download.
if ( ! languageSelect.find( 'option:selected' ).data( 'installed' ) ) {
    $( '#submit', this ).after( '<span class=\"spinner language-install-spinner is-active\" />' );
    }
    });
    });
    </script>
    """)
# end def network_settings_add_js
#// 
#// Outputs the HTML for a network's "Edit Site" tabular interface.
#// 
#// @since 4.6.0
#// 
#// @param $args {
#// Optional. Array or string of Query parameters. Default empty array.
#// 
#// @type int    $blog_id  The site ID. Default is the current site.
#// @type array  $links    The tabs to include with (label|url|cap) keys.
#// @type string $selected The ID of the selected link.
#// }
#//
def network_edit_site_nav(args=Array(), *args_):
    
    #// 
    #// Filters the links that appear on site-editing network pages.
    #// 
    #// Default links: 'site-info', 'site-users', 'site-themes', and 'site-settings'.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array $links {
    #// An array of link data representing individual network admin pages.
    #// 
    #// @type array $link_slug {
    #// An array of information about the individual link to a page.
    #// 
    #// $type string $label Label to use for the link.
    #// $type string $url   URL, relative to `network_admin_url()` to use for the link.
    #// $type string $cap   Capability required to see the link.
    #// }
    #// }
    #//
    links = apply_filters("network_edit_site_nav_links", Array({"site-info": Array({"label": __("Info"), "url": "site-info.php", "cap": "manage_sites"})}, {"site-users": Array({"label": __("Users"), "url": "site-users.php", "cap": "manage_sites"})}, {"site-themes": Array({"label": __("Themes"), "url": "site-themes.php", "cap": "manage_sites"})}, {"site-settings": Array({"label": __("Settings"), "url": "site-settings.php", "cap": "manage_sites"})}))
    #// Parse arguments.
    parsed_args = wp_parse_args(args, Array({"blog_id": int(PHP_REQUEST["blog_id"]) if (php_isset(lambda : PHP_REQUEST["blog_id"])) else 0, "links": links, "selected": "site-info"}))
    #// Setup the links array.
    screen_links = Array()
    #// Loop through tabs.
    for link_id,link in parsed_args["links"]:
        #// Skip link if user can't access.
        if (not current_user_can(link["cap"], parsed_args["blog_id"])):
            continue
        # end if
        #// Link classes.
        classes = Array("nav-tab")
        #// Aria-current attribute.
        aria_current = ""
        #// Selected is set by the parent OR assumed by the $pagenow global.
        if parsed_args["selected"] == link_id or link["url"] == PHP_GLOBALS["pagenow"]:
            classes[-1] = "nav-tab-active"
            aria_current = " aria-current=\"page\""
        # end if
        #// Escape each class.
        esc_classes = php_implode(" ", classes)
        #// Get the URL for this link.
        url = add_query_arg(Array({"id": parsed_args["blog_id"]}), network_admin_url(link["url"]))
        #// Add link to nav links.
        screen_links[link_id] = "<a href=\"" + esc_url(url) + "\" id=\"" + esc_attr(link_id) + "\" class=\"" + esc_classes + "\"" + aria_current + ">" + esc_html(link["label"]) + "</a>"
    # end for
    #// All done!
    php_print("<nav class=\"nav-tab-wrapper wp-clearfix\" aria-label=\"" + esc_attr__("Secondary menu") + "\">")
    php_print(php_implode("", screen_links))
    php_print("</nav>")
# end def network_edit_site_nav
#// 
#// Returns the arguments for the help tab on the Edit Site screens.
#// 
#// @since 4.9.0
#// 
#// @return array Help tab arguments.
#//
def get_site_screen_help_tab_args(*args_):
    
    return Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("The menu is for editing information specific to individual sites, particularly if the admin area of a site is unavailable.") + "</p>" + "<p>" + __("<strong>Info</strong> &mdash; The site URL is rarely edited as this can cause the site to not work properly. The Registered date and Last Updated date are displayed. Network admins can mark a site as archived, spam, deleted and mature, to remove from public listings or disable.") + "</p>" + "<p>" + __("<strong>Users</strong> &mdash; This displays the users associated with this site. You can also change their role, reset their password, or remove them from the site. Removing the user from the site does not remove the user from the network.") + "</p>" + "<p>" + php_sprintf(__("<strong>Themes</strong> &mdash; This area shows themes that are not already enabled across the network. Enabling a theme in this menu makes it accessible to this site. It does not activate the theme, but allows it to show in the site&#8217;s Appearance menu. To enable a theme for the entire network, see the <a href=\"%s\">Network Themes</a> screen."), network_admin_url("themes.php")) + "</p>" + "<p>" + __("<strong>Settings</strong> &mdash; This page shows a list of all settings associated with this site. Some are created by WordPress and others are created by plugins you activate. Note that some fields are grayed out and say Serialized Data. You cannot modify these values due to the way the setting is stored in the database.") + "</p>"})
# end def get_site_screen_help_tab_args
#// 
#// Returns the content for the help sidebar on the Edit Site screens.
#// 
#// @since 4.9.0
#// 
#// @return string Help sidebar content.
#//
def get_site_screen_help_sidebar_content(*args_):
    
    return "<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/network-admin-sites-screen/\">Documentation on Site Management</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/forum/multisite/\">Support Forums</a>") + "</p>"
# end def get_site_screen_help_sidebar_content
