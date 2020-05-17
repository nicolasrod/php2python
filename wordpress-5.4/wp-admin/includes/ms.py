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
def check_upload_size(file_=None, *_args_):
    
    
    if get_site_option("upload_space_check_disabled"):
        return file_
    # end if
    if "0" != file_["error"]:
        #// There's already an error.
        return file_
    # end if
    if php_defined("WP_IMPORTING"):
        return file_
    # end if
    space_left_ = get_upload_space_available()
    file_size_ = filesize(file_["tmp_name"])
    if space_left_ < file_size_:
        #// translators: %s: Required disk space in kilobytes.
        file_["error"] = php_sprintf(__("Not enough space to upload. %s KB needed."), number_format(file_size_ - space_left_ / KB_IN_BYTES))
    # end if
    if file_size_ > KB_IN_BYTES * get_site_option("fileupload_maxk", 1500):
        #// translators: %s: Maximum allowed file size in kilobytes.
        file_["error"] = php_sprintf(__("This file is too big. Files must be less than %s KB in size."), get_site_option("fileupload_maxk", 1500))
    # end if
    if upload_is_user_over_quota(False):
        file_["error"] = __("You have used your space quota. Please delete files before uploading.")
    # end if
    if "0" != file_["error"] and (not (php_isset(lambda : PHP_POST["html-upload"]))) and (not wp_doing_ajax()):
        wp_die(file_["error"] + " <a href=\"javascript:history.go(-1)\">" + __("Back") + "</a>")
    # end if
    return file_
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
def wpmu_delete_blog(blog_id_=None, drop_=None, *_args_):
    if drop_ is None:
        drop_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    switch_ = False
    if get_current_blog_id() != blog_id_:
        switch_ = True
        switch_to_blog(blog_id_)
    # end if
    blog_ = get_site(blog_id_)
    current_network_ = get_network()
    #// If a full blog object is not available, do not destroy anything.
    if drop_ and (not blog_):
        drop_ = False
    # end if
    #// Don't destroy the initial, main, or root blog.
    if drop_ and 1 == blog_id_ or is_main_site(blog_id_) or blog_.path == current_network_.path and blog_.domain == current_network_.domain:
        drop_ = False
    # end if
    upload_path_ = php_trim(get_option("upload_path"))
    #// If ms_files_rewriting is enabled and upload_path is empty, wp_upload_dir is not reliable.
    if drop_ and get_site_option("ms_files_rewriting") and php_empty(lambda : upload_path_):
        drop_ = False
    # end if
    if drop_:
        wp_delete_site(blog_id_)
    else:
        #// This action is documented in wp-includes/ms-blogs.php
        do_action_deprecated("delete_blog", Array(blog_id_, False), "5.1.0")
        users_ = get_users(Array({"blog_id": blog_id_, "fields": "ids"}))
        #// Remove users from this blog.
        if (not php_empty(lambda : users_)):
            for user_id_ in users_:
                remove_user_from_blog(user_id_, blog_id_)
            # end for
        # end if
        update_blog_status(blog_id_, "deleted", 1)
        #// This action is documented in wp-includes/ms-blogs.php
        do_action_deprecated("deleted_blog", Array(blog_id_, False), "5.1.0")
    # end if
    if switch_:
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
def wpmu_delete_user(id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_is_numeric(id_)):
        return False
    # end if
    id_ = php_int(id_)
    user_ = php_new_class("WP_User", lambda : WP_User(id_))
    if (not user_.exists()):
        return False
    # end if
    #// Global super-administrators are protected, and cannot be deleted.
    _super_admins_ = get_super_admins()
    if php_in_array(user_.user_login, _super_admins_, True):
        return False
    # end if
    #// 
    #// Fires before a user is deleted from the network.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param int $id ID of the user about to be deleted from the network.
    #//
    do_action("wpmu_delete_user", id_)
    blogs_ = get_blogs_of_user(id_)
    if (not php_empty(lambda : blogs_)):
        for blog_ in blogs_:
            switch_to_blog(blog_.userblog_id)
            remove_user_from_blog(id_, blog_.userblog_id)
            post_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_author = %d"), id_))
            for post_id_ in post_ids_:
                wp_delete_post(post_id_)
            # end for
            #// Clean links.
            link_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT link_id FROM ") + str(wpdb_.links) + str(" WHERE link_owner = %d"), id_))
            if link_ids_:
                for link_id_ in link_ids_:
                    wp_delete_link(link_id_)
                # end for
            # end if
            restore_current_blog()
        # end for
    # end if
    meta_ = wpdb_.get_col(wpdb_.prepare(str("SELECT umeta_id FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id = %d"), id_))
    for mid_ in meta_:
        delete_metadata_by_mid("user", mid_)
    # end for
    wpdb_.delete(wpdb_.users, Array({"ID": id_}))
    clean_user_cache(user_)
    #// This action is documented in wp-admin/includes/user.php
    do_action("deleted_user", id_, None)
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
def upload_is_user_over_quota(echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    if get_site_option("upload_space_check_disabled"):
        return False
    # end if
    space_allowed_ = get_space_allowed()
    if (not php_is_numeric(space_allowed_)):
        space_allowed_ = 10
        pass
    # end if
    space_used_ = get_space_used()
    if space_allowed_ - space_used_ < 0:
        if echo_:
            printf(__("Sorry, you have used your space allocation of %s. Please delete some files to upload more files."), size_format(space_allowed_ * MB_IN_BYTES))
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
def display_space_usage(*_args_):
    
    
    space_allowed_ = get_space_allowed()
    space_used_ = get_space_used()
    percent_used_ = space_used_ / space_allowed_ * 100
    space_ = size_format(space_allowed_ * MB_IN_BYTES)
    php_print(" <strong>\n  ")
    #// translators: Storage space that's been used. 1: Percentage of used space, 2: Total space allowed in megabytes or gigabytes.
    printf(__("Used: %1$s%% of %2$s"), number_format(percent_used_), space_)
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
def fix_import_form_size(size_=None, *_args_):
    
    
    if upload_is_user_over_quota(False):
        return 0
    # end if
    available_ = get_upload_space_available()
    return php_min(size_, available_)
# end def fix_import_form_size
#// 
#// Displays the site upload space quota setting form on the Edit Site Settings screen.
#// 
#// @since 3.0.0
#// 
#// @param int $id The ID of the site to display the setting for.
#//
def upload_space_setting(id_=None, *_args_):
    
    
    switch_to_blog(id_)
    quota_ = get_option("blog_upload_space")
    restore_current_blog()
    if (not quota_):
        quota_ = ""
    # end if
    php_print(" <tr>\n      <th><label for=\"blog-upload-space-number\">")
    _e("Site Upload Space Quota")
    php_print("</label></th>\n      <td>\n          <input type=\"number\" step=\"1\" min=\"0\" style=\"width: 100px\" name=\"option[blog_upload_space]\" id=\"blog-upload-space-number\" aria-describedby=\"blog-upload-space-desc\" value=\"")
    php_print(quota_)
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
def refresh_user_details(id_=None, *_args_):
    
    
    id_ = php_int(id_)
    user_ = get_userdata(id_)
    if (not user_):
        return False
    # end if
    clean_user_cache(user_)
    return id_
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
def format_code_lang(code_="", *_args_):
    
    
    code_ = php_strtolower(php_substr(code_, 0, 2))
    lang_codes_ = Array({"aa": "Afar", "ab": "Abkhazian", "af": "Afrikaans", "ak": "Akan", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "an": "Aragonese", "hy": "Armenian", "as": "Assamese", "av": "Avaric", "ae": "Avestan", "ay": "Aymara", "az": "Azerbaijani", "ba": "Bashkir", "bm": "Bambara", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bh": "Bihari", "bi": "Bislama", "bs": "Bosnian", "br": "Breton", "bg": "Bulgarian", "my": "Burmese", "ca": "Catalan; Valencian", "ch": "Chamorro", "ce": "Chechen", "zh": "Chinese", "cu": "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic", "cv": "Chuvash", "kw": "Cornish", "co": "Corsican", "cr": "Cree", "cs": "Czech", "da": "Danish", "dv": "Divehi; Dhivehi; Maldivian", "nl": "Dutch; Flemish", "dz": "Dzongkha", "en": "English", "eo": "Esperanto", "et": "Estonian", "ee": "Ewe", "fo": "Faroese", "fj": "Fijjian", "fi": "Finnish", "fr": "French", "fy": "Western Frisian", "ff": "Fulah", "ka": "Georgian", "de": "German", "gd": "Gaelic; Scottish Gaelic", "ga": "Irish", "gl": "Galician", "gv": "Manx", "el": "Greek, Modern", "gn": "Guarani", "gu": "Gujarati", "ht": "Haitian; Haitian Creole", "ha": "Hausa", "he": "Hebrew", "hz": "Herero", "hi": "Hindi", "ho": "Hiri Motu", "hu": "Hungarian", "ig": "Igbo", "is": "Icelandic", "io": "Ido", "ii": "Sichuan Yi", "iu": "Inuktitut", "ie": "Interlingue", "ia": "Interlingua (International Auxiliary Language Association)", "id": "Indonesian", "ik": "Inupiaq", "it": "Italian", "jv": "Javanese", "ja": "Japanese", "kl": "Kalaallisut; Greenlandic", "kn": "Kannada", "ks": "Kashmiri", "kr": "Kanuri", "kk": "Kazakh", "km": "Central Khmer", "ki": "Kikuyu; Gikuyu", "rw": "Kinyarwanda", "ky": "Kirghiz; Kyrgyz", "kv": "Komi", "kg": "Kongo", "ko": "Korean", "kj": "Kuanyama; Kwanyama", "ku": "Kurdish", "lo": "Lao", "la": "Latin", "lv": "Latvian", "li": "Limburgan; Limburger; Limburgish", "ln": "Lingala", "lt": "Lithuanian", "lb": "Luxembourgish; Letzeburgesch", "lu": "Luba-Katanga", "lg": "Ganda", "mk": "Macedonian", "mh": "Marshallese", "ml": "Malayalam", "mi": "Maori", "mr": "Marathi", "ms": "Malay", "mg": "Malagasy", "mt": "Maltese", "mo": "Moldavian", "mn": "Mongolian", "na": "Nauru", "nv": "Navajo; Navaho", "nr": "Ndebele, South; South Ndebele", "nd": "Ndebele, North; North Ndebele", "ng": "Ndonga", "ne": "Nepali", "nn": "Norwegian Nynorsk; Nynorsk, Norwegian", "nb": "BokmÃ¥l, Norwegian, Norwegian BokmÃ¥l", "no": "Norwegian", "ny": "Chichewa; Chewa; Nyanja", "oc": "Occitan, ProvenÃ§al", "oj": "Ojibwa", "or": "Oriya", "om": "Oromo", "os": "Ossetian; Ossetic", "pa": "Panjabi; Punjabi", "fa": "Persian", "pi": "Pali", "pl": "Polish", "pt": "Portuguese", "ps": "Pushto", "qu": "Quechua", "rm": "Romansh", "ro": "Romanian", "rn": "Rundi", "ru": "Russian", "sg": "Sango", "sa": "Sanskrit", "sr": "Serbian", "hr": "Croatian", "si": "Sinhala; Sinhalese", "sk": "Slovak", "sl": "Slovenian", "se": "Northern Sami", "sm": "Samoan", "sn": "Shona", "sd": "Sindhi", "so": "Somali", "st": "Sotho, Southern", "es": "Spanish; Castilian", "sc": "Sardinian", "ss": "Swati", "su": "Sundanese", "sw": "Swahili", "sv": "Swedish", "ty": "Tahitian", "ta": "Tamil", "tt": "Tatar", "te": "Telugu", "tg": "Tajik", "tl": "Tagalog", "th": "Thai", "bo": "Tibetan", "ti": "Tigrinya", "to": "Tonga (Tonga Islands)", "tn": "Tswana", "ts": "Tsonga", "tk": "Turkmen", "tr": "Turkish", "tw": "Twi", "ug": "Uighur; Uyghur", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "ve": "Venda", "vi": "Vietnamese", "vo": "VolapÃ¼k", "cy": "Welsh", "wa": "Walloon", "wo": "Wolof", "xh": "Xhosa", "yi": "Yiddish", "yo": "Yoruba", "za": "Zhuang; Chuang", "zu": "Zulu"})
    #// 
    #// Filters the language codes.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string[] $lang_codes Array of key/value pairs of language codes where key is the short version.
    #// @param string   $code       A two-letter designation of the language.
    #//
    lang_codes_ = apply_filters("lang_codes", lang_codes_, code_)
    return php_strtr(code_, lang_codes_)
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
def sync_category_tag_slugs(term_=None, taxonomy_=None, *_args_):
    
    
    if global_terms_enabled() and "category" == taxonomy_ or "post_tag" == taxonomy_:
        if php_is_object(term_):
            term_.slug = sanitize_title(term_.name)
        else:
            term_["slug"] = sanitize_title(term_["name"])
        # end if
    # end if
    return term_
# end def sync_category_tag_slugs
#// 
#// Displays an access denied message when a user tries to view a site's dashboard they
#// do not have access to.
#// 
#// @since 3.2.0
#// @access private
#//
def _access_denied_splash(*_args_):
    
    
    if (not is_user_logged_in()) or is_network_admin():
        return
    # end if
    blogs_ = get_blogs_of_user(get_current_user_id())
    if wp_list_filter(blogs_, Array({"userblog_id": get_current_blog_id()})):
        return
    # end if
    blog_name_ = get_bloginfo("name")
    if php_empty(lambda : blogs_):
        wp_die(php_sprintf(__("You attempted to access the \"%1$s\" dashboard, but you do not currently have privileges on this site. If you believe you should be able to access the \"%1$s\" dashboard, please contact your network administrator."), blog_name_), 403)
    # end if
    output_ = "<p>" + php_sprintf(__("You attempted to access the \"%1$s\" dashboard, but you do not currently have privileges on this site. If you believe you should be able to access the \"%1$s\" dashboard, please contact your network administrator."), blog_name_) + "</p>"
    output_ += "<p>" + __("If you reached this screen by accident and meant to visit one of your own sites, here are some shortcuts to help you find your way.") + "</p>"
    output_ += "<h3>" + __("Your Sites") + "</h3>"
    output_ += "<table>"
    for blog_ in blogs_:
        output_ += "<tr>"
        output_ += str("<td>") + str(blog_.blogname) + str("</td>")
        output_ += "<td><a href=\"" + esc_url(get_admin_url(blog_.userblog_id)) + "\">" + __("Visit Dashboard") + "</a> | " + "<a href=\"" + esc_url(get_home_url(blog_.userblog_id)) + "\">" + __("View Site") + "</a></td>"
        output_ += "</tr>"
    # end for
    output_ += "</table>"
    wp_die(output_, 403)
# end def _access_denied_splash
#// 
#// Checks if the current user has permissions to import new users.
#// 
#// @since 3.0.0
#// 
#// @param string $permission A permission to be checked. Currently not used.
#// @return bool True if the user has proper permissions, false if they do not.
#//
def check_import_new_users(permission_=None, *_args_):
    
    
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
def mu_dropdown_languages(lang_files_=None, current_="", *_args_):
    if lang_files_ is None:
        lang_files_ = Array()
    # end if
    
    flag_ = False
    output_ = Array()
    for val_ in lang_files_:
        code_lang_ = php_basename(val_, ".mo")
        if "en_US" == code_lang_:
            #// American English.
            flag_ = True
            ae_ = __("American English")
            output_[ae_] = "<option value=\"" + esc_attr(code_lang_) + "\"" + selected(current_, code_lang_, False) + "> " + ae_ + "</option>"
        elif "en_GB" == code_lang_:
            #// British English.
            flag_ = True
            be_ = __("British English")
            output_[be_] = "<option value=\"" + esc_attr(code_lang_) + "\"" + selected(current_, code_lang_, False) + "> " + be_ + "</option>"
        else:
            translated_ = format_code_lang(code_lang_)
            output_[translated_] = "<option value=\"" + esc_attr(code_lang_) + "\"" + selected(current_, code_lang_, False) + "> " + esc_html(translated_) + "</option>"
        # end if
    # end for
    if False == flag_:
        #// WordPress English.
        output_[-1] = "<option value=\"\"" + selected(current_, "", False) + ">" + __("English") + "</option>"
    # end if
    #// Order by name.
    uksort(output_, "strnatcasecmp")
    #// 
    #// Filters the languages available in the dropdown.
    #// 
    #// @since MU (3.0.0)
    #// 
    #// @param string[] $output     Array of HTML output for the dropdown.
    #// @param string[] $lang_files Array of available language files.
    #// @param string   $current    The current language code.
    #//
    output_ = apply_filters("mu_dropdown_languages", output_, lang_files_, current_)
    php_print(php_implode("\n   ", output_))
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
def site_admin_notice(*_args_):
    
    
    global wp_db_version_
    global pagenow_
    php_check_if_defined("wp_db_version_","pagenow_")
    if (not current_user_can("upgrade_network")):
        return False
    # end if
    if "upgrade.php" == pagenow_:
        return
    # end if
    if get_site_option("wpmu_upgrade_site") != wp_db_version_:
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
def avoid_blog_page_permalink_collision(data_=None, postarr_=None, *_args_):
    
    
    if is_subdomain_install():
        return data_
    # end if
    if "page" != data_["post_type"]:
        return data_
    # end if
    if (not (php_isset(lambda : data_["post_name"]))) or "" == data_["post_name"]:
        return data_
    # end if
    if (not is_main_site()):
        return data_
    # end if
    post_name_ = data_["post_name"]
    c_ = 0
    while True:
        
        if not (c_ < 10 and get_id_from_blogname(post_name_)):
            break
        # end if
        post_name_ += mt_rand(1, 10)
        c_ += 1
    # end while
    if post_name_ != data_["post_name"]:
        data_["post_name"] = post_name_
    # end if
    return data_
# end def avoid_blog_page_permalink_collision
#// 
#// Handles the display of choosing a user's primary site.
#// 
#// This displays the user's primary site and allows the user to choose
#// which site is primary.
#// 
#// @since 3.0.0
#//
def choose_primary_blog(*_args_):
    
    
    php_print(" <table class=\"form-table\" role=\"presentation\">\n    <tr>\n  ")
    pass
    php_print("     <th scope=\"row\"><label for=\"primary_blog\">")
    _e("Primary Site")
    php_print("</label></th>\n      <td>\n      ")
    all_blogs_ = get_blogs_of_user(get_current_user_id())
    primary_blog_ = get_user_meta(get_current_user_id(), "primary_blog", True)
    if php_count(all_blogs_) > 1:
        found_ = False
        php_print("         <select name=\"primary_blog\" id=\"primary_blog\">\n                ")
        for blog_ in all_blogs_:
            if primary_blog_ == blog_.userblog_id:
                found_ = True
            # end if
            php_print("                 <option value=\"")
            php_print(blog_.userblog_id)
            php_print("\"")
            selected(primary_blog_, blog_.userblog_id)
            php_print(">")
            php_print(esc_url(get_home_url(blog_.userblog_id)))
            php_print("</option>\n                  ")
        # end for
        php_print("         </select>\n         ")
        if (not found_):
            blog_ = reset(all_blogs_)
            update_user_meta(get_current_user_id(), "primary_blog", blog_.userblog_id)
        # end if
    elif php_count(all_blogs_) == 1:
        blog_ = reset(all_blogs_)
        php_print(esc_url(get_home_url(blog_.userblog_id)))
        if primary_blog_ != blog_.userblog_id:
            #// Set the primary blog again if it's out of sync with blog list.
            update_user_meta(get_current_user_id(), "primary_blog", blog_.userblog_id)
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
def can_edit_network(network_id_=None, *_args_):
    
    
    if get_current_network_id() == network_id_:
        result_ = True
    else:
        result_ = False
    # end if
    #// 
    #// Filters whether this network can be edited from this page.
    #// 
    #// @since 3.1.0
    #// 
    #// @param bool $result     Whether the network can be edited from this page.
    #// @param int  $network_id The network ID to check.
    #//
    return apply_filters("can_edit_network", result_, network_id_)
# end def can_edit_network
#// 
#// Thickbox image paths for Network Admin.
#// 
#// @since 3.1.0
#// 
#// @access private
#//
def _thickbox_path_admin_subfolder(*_args_):
    
    
    php_print("<script type=\"text/javascript\">\nvar tb_pathToImage = \"")
    php_print(includes_url("js/thickbox/loadingAnimation.gif", "relative"))
    php_print("\";\n</script>\n ")
# end def _thickbox_path_admin_subfolder
#// 
#// @param array $users
#//
def confirm_delete_users(users_=None, *_args_):
    
    
    current_user_ = wp_get_current_user()
    if (not php_is_array(users_)) or php_empty(lambda : users_):
        return False
    # end if
    php_print(" <h1>")
    esc_html_e("Users")
    php_print("</h1>\n\n    ")
    if 1 == php_count(users_):
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
    site_admins_ = get_super_admins()
    admin_out_ = "<option value=\"" + esc_attr(current_user_.ID) + "\">" + current_user_.user_login + "</option>"
    php_print(" <table class=\"form-table\" role=\"presentation\">\n    ")
    allusers_ = PHP_POST["allusers"]
    for user_id_ in allusers_:
        if "" != user_id_ and "0" != user_id_:
            delete_user_ = get_userdata(user_id_)
            if (not current_user_can("delete_user", delete_user_.ID)):
                wp_die(php_sprintf(__("Warning! User %s cannot be deleted."), delete_user_.user_login))
            # end if
            if php_in_array(delete_user_.user_login, site_admins_):
                wp_die(php_sprintf(__("Warning! User cannot be deleted. The user %s is a network administrator."), "<em>" + delete_user_.user_login + "</em>"))
            # end if
            php_print("         <tr>\n              <th scope=\"row\">")
            php_print(delete_user_.user_login)
            php_print("                 ")
            php_print("<input type=\"hidden\" name=\"user[]\" value=\"" + esc_attr(user_id_) + "\" />" + "\n")
            php_print("             </th>\n         ")
            blogs_ = get_blogs_of_user(user_id_, True)
            if (not php_empty(lambda : blogs_)):
                php_print("             <td><fieldset><p><legend>\n             ")
                printf(__("What should be done with content owned by %s?"), "<em>" + delete_user_.user_login + "</em>")
                php_print("             </legend></p>\n             ")
                for key_,details_ in blogs_:
                    blog_users_ = get_users(Array({"blog_id": details_.userblog_id, "fields": Array("ID", "user_login")}))
                    if php_is_array(blog_users_) and (not php_empty(lambda : blog_users_)):
                        user_site_ = "<a href='" + esc_url(get_home_url(details_.userblog_id)) + str("'>") + str(details_.blogname) + str("</a>")
                        user_dropdown_ = "<label for=\"reassign_user\" class=\"screen-reader-text\">" + __("Select a user") + "</label>"
                        user_dropdown_ += str("<select name='blog[") + str(user_id_) + str("][") + str(key_) + str("]' id='reassign_user'>")
                        user_list_ = ""
                        for user_ in blog_users_:
                            if (not php_in_array(user_.ID, allusers_)):
                                user_list_ += str("<option value='") + str(user_.ID) + str("'>") + str(user_.user_login) + str("</option>")
                            # end if
                        # end for
                        if "" == user_list_:
                            user_list_ = admin_out_
                        # end if
                        user_dropdown_ += user_list_
                        user_dropdown_ += "</select>\n"
                        php_print("                     <ul style=\"list-style:none;\">\n                           <li>\n                              ")
                        #// translators: %s: Link to user's site.
                        printf(__("Site: %s"), user_site_)
                        php_print("                         </li>\n                         <li><label><input type=\"radio\" id=\"delete_option0\" name=\"delete[")
                        php_print(details_.userblog_id + "][" + delete_user_.ID)
                        php_print("]\" value=\"delete\" checked=\"checked\" />\n                            ")
                        _e("Delete all content.")
                        php_print("</label></li>\n                          <li><label><input type=\"radio\" id=\"delete_option1\" name=\"delete[")
                        php_print(details_.userblog_id + "][" + delete_user_.ID)
                        php_print("]\" value=\"reassign\" />\n                          ")
                        _e("Attribute all content to:")
                        php_print("</label>\n                           ")
                        php_print(user_dropdown_)
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
    do_action("delete_user_form", current_user_, allusers_)
    if 1 == php_count(users_):
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
def network_settings_add_js(*_args_):
    
    
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
def network_edit_site_nav(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
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
    links_ = apply_filters("network_edit_site_nav_links", Array({"site-info": Array({"label": __("Info"), "url": "site-info.php", "cap": "manage_sites"})}, {"site-users": Array({"label": __("Users"), "url": "site-users.php", "cap": "manage_sites"})}, {"site-themes": Array({"label": __("Themes"), "url": "site-themes.php", "cap": "manage_sites"})}, {"site-settings": Array({"label": __("Settings"), "url": "site-settings.php", "cap": "manage_sites"})}))
    #// Parse arguments.
    parsed_args_ = wp_parse_args(args_, Array({"blog_id": php_int(PHP_REQUEST["blog_id"]) if (php_isset(lambda : PHP_REQUEST["blog_id"])) else 0, "links": links_, "selected": "site-info"}))
    #// Setup the links array.
    screen_links_ = Array()
    #// Loop through tabs.
    for link_id_,link_ in parsed_args_["links"]:
        #// Skip link if user can't access.
        if (not current_user_can(link_["cap"], parsed_args_["blog_id"])):
            continue
        # end if
        #// Link classes.
        classes_ = Array("nav-tab")
        #// Aria-current attribute.
        aria_current_ = ""
        #// Selected is set by the parent OR assumed by the $pagenow global.
        if parsed_args_["selected"] == link_id_ or link_["url"] == PHP_GLOBALS["pagenow"]:
            classes_[-1] = "nav-tab-active"
            aria_current_ = " aria-current=\"page\""
        # end if
        #// Escape each class.
        esc_classes_ = php_implode(" ", classes_)
        #// Get the URL for this link.
        url_ = add_query_arg(Array({"id": parsed_args_["blog_id"]}), network_admin_url(link_["url"]))
        #// Add link to nav links.
        screen_links_[link_id_] = "<a href=\"" + esc_url(url_) + "\" id=\"" + esc_attr(link_id_) + "\" class=\"" + esc_classes_ + "\"" + aria_current_ + ">" + esc_html(link_["label"]) + "</a>"
    # end for
    #// All done!
    php_print("<nav class=\"nav-tab-wrapper wp-clearfix\" aria-label=\"" + esc_attr__("Secondary menu") + "\">")
    php_print(php_implode("", screen_links_))
    php_print("</nav>")
# end def network_edit_site_nav
#// 
#// Returns the arguments for the help tab on the Edit Site screens.
#// 
#// @since 4.9.0
#// 
#// @return array Help tab arguments.
#//
def get_site_screen_help_tab_args(*_args_):
    
    
    return Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("The menu is for editing information specific to individual sites, particularly if the admin area of a site is unavailable.") + "</p>" + "<p>" + __("<strong>Info</strong> &mdash; The site URL is rarely edited as this can cause the site to not work properly. The Registered date and Last Updated date are displayed. Network admins can mark a site as archived, spam, deleted and mature, to remove from public listings or disable.") + "</p>" + "<p>" + __("<strong>Users</strong> &mdash; This displays the users associated with this site. You can also change their role, reset their password, or remove them from the site. Removing the user from the site does not remove the user from the network.") + "</p>" + "<p>" + php_sprintf(__("<strong>Themes</strong> &mdash; This area shows themes that are not already enabled across the network. Enabling a theme in this menu makes it accessible to this site. It does not activate the theme, but allows it to show in the site&#8217;s Appearance menu. To enable a theme for the entire network, see the <a href=\"%s\">Network Themes</a> screen."), network_admin_url("themes.php")) + "</p>" + "<p>" + __("<strong>Settings</strong> &mdash; This page shows a list of all settings associated with this site. Some are created by WordPress and others are created by plugins you activate. Note that some fields are grayed out and say Serialized Data. You cannot modify these values due to the way the setting is stored in the database.") + "</p>"})
# end def get_site_screen_help_tab_args
#// 
#// Returns the content for the help sidebar on the Edit Site screens.
#// 
#// @since 4.9.0
#// 
#// @return string Help sidebar content.
#//
def get_site_screen_help_sidebar_content(*_args_):
    
    
    return "<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/network-admin-sites-screen/\">Documentation on Site Management</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/forum/multisite/\">Support Forums</a>") + "</p>"
# end def get_site_screen_help_sidebar_content
