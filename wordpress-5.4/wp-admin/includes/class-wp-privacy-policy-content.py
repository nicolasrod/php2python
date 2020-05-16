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
#// WP_Privacy_Policy_Content class.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.9.6
#//
class WP_Privacy_Policy_Content():
    policy_content = Array()
    #// 
    #// Constructor
    #// 
    #// @since 4.9.6
    #//
    def __init__(self):
        
        pass
    # end def __init__
    #// 
    #// Add content to the postbox shown when editing the privacy policy.
    #// 
    #// Plugins and themes should suggest text for inclusion in the site's privacy policy.
    #// The suggested text should contain information about any functionality that affects user privacy,
    #// and will be shown in the Suggested Privacy Policy Content postbox.
    #// 
    #// Intended for use from `wp_add_privacy_policy_content()`.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $plugin_name The name of the plugin or theme that is suggesting content for the site's privacy policy.
    #// @param string $policy_text The suggested content for inclusion in the policy.
    #//
    @classmethod
    def add(self, plugin_name=None, policy_text=None):
        
        if php_empty(lambda : plugin_name) or php_empty(lambda : policy_text):
            return
        # end if
        data = Array({"plugin_name": plugin_name, "policy_text": policy_text})
        if (not php_in_array(data, self.policy_content, True)):
            self.policy_content[-1] = data
        # end if
    # end def add
    #// 
    #// Quick check if any privacy info has changed.
    #// 
    #// @since 4.9.6
    #//
    @classmethod
    def text_change_check(self):
        
        policy_page_id = php_int(get_option("wp_page_for_privacy_policy"))
        #// The site doesn't have a privacy policy.
        if php_empty(lambda : policy_page_id):
            return False
        # end if
        if (not current_user_can("edit_post", policy_page_id)):
            return False
        # end if
        old = get_post_meta(policy_page_id, "_wp_suggested_privacy_policy_content")
        #// Updates are not relevant if the user has not reviewed any suggestions yet.
        if php_empty(lambda : old):
            return False
        # end if
        cached = get_option("_wp_suggested_policy_text_has_changed")
        #// 
        #// When this function is called before `admin_init`, `self::$policy_content`
        #// has not been populated yet, so use the cached result from the last
        #// execution instead.
        #//
        if (not did_action("admin_init")):
            return "changed" == cached
        # end if
        new = self.policy_content
        #// Remove the extra values added to the meta.
        for key,data in old:
            if (not php_empty(lambda : data["removed"])):
                old[key] = None
                continue
            # end if
            old[key] = Array({"plugin_name": data["plugin_name"], "policy_text": data["policy_text"]})
        # end for
        #// Normalize the order of texts, to facilitate comparison.
        sort(old)
        sort(new)
        #// The == operator (equal, not identical) was used intentionally.
        #// See http://php.net/manual/en/language.operators.array.php
        if new != old:
            #// A plugin was activated or deactivated, or some policy text has changed.
            #// Show a notice on the relevant screens to inform the admin.
            add_action("admin_notices", Array("WP_Privacy_Policy_Content", "policy_text_changed_notice"))
            state = "changed"
        else:
            state = "not-changed"
        # end if
        #// Cache the result for use before `admin_init` (see above).
        if cached != state:
            update_option("_wp_suggested_policy_text_has_changed", state)
        # end if
        return "changed" == state
    # end def text_change_check
    #// 
    #// Output a warning when some privacy info has changed.
    #// 
    #// @since 4.9.6
    #//
    @classmethod
    def policy_text_changed_notice(self):
        
        global post
        php_check_if_defined("post")
        screen = get_current_screen().id
        if "privacy" != screen:
            return
        # end if
        php_print("     <div class=\"policy-text-updated notice notice-warning is-dismissible\">\n          <p>\n           ")
        printf(__("The suggested privacy policy text has changed. Please <a href=\"%s\">review the guide</a> and update your privacy policy."), esc_url(admin_url("privacy-policy-guide.php")))
        php_print("         </p>\n      </div>\n        ")
    # end def policy_text_changed_notice
    #// 
    #// Update the cached policy info when the policy page is updated.
    #// 
    #// @since 4.9.6
    #// @access private
    #//
    @classmethod
    def _policy_page_updated(self, post_id=None):
        
        policy_page_id = php_int(get_option("wp_page_for_privacy_policy"))
        if (not policy_page_id) or policy_page_id != php_int(post_id):
            return
        # end if
        #// Remove updated|removed status.
        old = get_post_meta(policy_page_id, "_wp_suggested_privacy_policy_content")
        done = Array()
        update_cache = False
        for old_key,old_data in old:
            if (not php_empty(lambda : old_data["removed"])):
                #// Remove the old policy text.
                update_cache = True
                continue
            # end if
            if (not php_empty(lambda : old_data["updated"])):
                #// 'updated' is now 'added'.
                done[-1] = Array({"plugin_name": old_data["plugin_name"], "policy_text": old_data["policy_text"], "added": old_data["updated"]})
                update_cache = True
            else:
                done[-1] = old_data
            # end if
        # end for
        if update_cache:
            delete_post_meta(policy_page_id, "_wp_suggested_privacy_policy_content")
            #// Update the cache.
            for data in done:
                add_post_meta(policy_page_id, "_wp_suggested_privacy_policy_content", data)
            # end for
        # end if
    # end def _policy_page_updated
    #// 
    #// Check for updated, added or removed privacy policy information from plugins.
    #// 
    #// Caches the current info in post_meta of the policy page.
    #// 
    #// @since 4.9.6
    #// 
    #// @return array The privacy policy text/information added by core and plugins.
    #//
    @classmethod
    def get_suggested_policy_text(self):
        
        policy_page_id = php_int(get_option("wp_page_for_privacy_policy"))
        checked = Array()
        time = time()
        update_cache = False
        new = self.policy_content
        old = Array()
        if policy_page_id:
            old = get_post_meta(policy_page_id, "_wp_suggested_privacy_policy_content")
        # end if
        #// Check for no-changes and updates.
        for new_key,new_data in new:
            for old_key,old_data in old:
                found = False
                if new_data["policy_text"] == old_data["policy_text"]:
                    #// Use the new plugin name in case it was changed, translated, etc.
                    if old_data["plugin_name"] != new_data["plugin_name"]:
                        old_data["plugin_name"] = new_data["plugin_name"]
                        update_cache = True
                    # end if
                    #// A plugin was re-activated.
                    if (not php_empty(lambda : old_data["removed"])):
                        old_data["removed"] = None
                        old_data["added"] = time
                        update_cache = True
                    # end if
                    checked[-1] = old_data
                    found = True
                elif new_data["plugin_name"] == old_data["plugin_name"]:
                    #// The info for the policy was updated.
                    checked[-1] = Array({"plugin_name": new_data["plugin_name"], "policy_text": new_data["policy_text"], "updated": time})
                    found = True
                    update_cache = True
                # end if
                if found:
                    new[new_key] = None
                    old[old_key] = None
                    continue
                # end if
            # end for
        # end for
        if (not php_empty(lambda : new)):
            #// A plugin was activated.
            for new_data in new:
                if (not php_empty(lambda : new_data["plugin_name"])) and (not php_empty(lambda : new_data["policy_text"])):
                    new_data["added"] = time
                    checked[-1] = new_data
                # end if
            # end for
            update_cache = True
        # end if
        if (not php_empty(lambda : old)):
            #// A plugin was deactivated.
            for old_data in old:
                if (not php_empty(lambda : old_data["plugin_name"])) and (not php_empty(lambda : old_data["policy_text"])):
                    data = Array({"plugin_name": old_data["plugin_name"], "policy_text": old_data["policy_text"], "removed": time})
                    checked[-1] = data
                # end if
            # end for
            update_cache = True
        # end if
        if update_cache and policy_page_id:
            delete_post_meta(policy_page_id, "_wp_suggested_privacy_policy_content")
            #// Update the cache.
            for data in checked:
                add_post_meta(policy_page_id, "_wp_suggested_privacy_policy_content", data)
            # end for
        # end if
        return checked
    # end def get_suggested_policy_text
    #// 
    #// Add a notice with a link to the guide when editing the privacy policy page.
    #// 
    #// @since 4.9.6
    #// @since 5.0.0 The `$post` parameter was made optional.
    #// 
    #// @param WP_Post|null $post The currently edited post. Default null.
    #//
    @classmethod
    def notice(self, post=None):
        
        if is_null(post):
            global post
            php_check_if_defined("post")
        else:
            post = get_post(post)
        # end if
        if (not type(post).__name__ == "WP_Post"):
            return
        # end if
        if (not current_user_can("manage_privacy_options")):
            return
        # end if
        current_screen = get_current_screen()
        policy_page_id = php_int(get_option("wp_page_for_privacy_policy"))
        if "post" != current_screen.base or policy_page_id != post.ID:
            return
        # end if
        message = __("Need help putting together your new Privacy Policy page? Check out our guide for recommendations on what content to include, along with policies suggested by your plugins and theme.")
        url = esc_url(admin_url("privacy-policy-guide.php"))
        label = __("View Privacy Policy Guide.")
        if get_current_screen().is_block_editor():
            wp_enqueue_script("wp-notices")
            action = Array({"url": url, "label": label})
            wp_add_inline_script("wp-notices", php_sprintf("wp.data.dispatch( \"core/notices\" ).createWarningNotice( \"%s\", { actions: [ %s ], isDismissible: false } )", message, wp_json_encode(action)), "after")
        else:
            php_print("         <div class=\"notice notice-warning inline wp-pp-notice\">\n             <p>\n               ")
            php_print(message)
            printf(" <a href=\"%s\" target=\"_blank\">%s <span class=\"screen-reader-text\">%s</span></a>", url, label, __("(opens in a new tab)"))
            php_print("             </p>\n          </div>\n            ")
        # end if
    # end def notice
    #// 
    #// Output the privacy policy guide together with content from the theme and plugins.
    #// 
    #// @since 4.9.6
    #//
    @classmethod
    def privacy_policy_guide(self):
        
        content_array = self.get_suggested_policy_text()
        content = ""
        toc = Array("<li><a href=\"#wp-privacy-policy-guide-introduction\">" + __("Introduction") + "</a></li>")
        date_format = __("F j, Y")
        copy = __("Copy this section to clipboard")
        return_to_top = "<a href=\"#\" class=\"return-to-top\">" + __("&uarr; Return to Top") + "</a>"
        for section in content_array:
            class_ = ""
            meta = ""
            removed = ""
            if (not php_empty(lambda : section["removed"])):
                class_ = " text-removed"
                date = date_i18n(date_format, section["removed"])
                #// translators: %s: Date of plugin deactivation.
                meta = php_sprintf(__("Removed %s."), date)
                #// translators: %s: Date of plugin deactivation.
                removed = __("You deactivated this plugin on %s and may no longer need this policy.")
                removed = "<div class=\"error inline\"><p>" + php_sprintf(removed, date) + "</p></div>"
            elif (not php_empty(lambda : section["updated"])):
                class_ = " text-updated"
                date = date_i18n(date_format, section["updated"])
                #// translators: %s: Date of privacy policy text update.
                meta = php_sprintf(__("Updated %s."), date)
            # end if
            if meta:
                meta = "<br><span class=\"privacy-text-meta\">" + meta + "</span>"
            # end if
            plugin_name = esc_html(section["plugin_name"])
            toc_id = "wp-privacy-policy-guide-" + sanitize_title(plugin_name)
            toc[-1] = php_sprintf("<li><a href=\"#%1$s\">%2$s</a>" + meta + "</li>", toc_id, plugin_name)
            content += "<div class=\"privacy-text-section" + class_ + "\">"
            content += "<a id=\"" + toc_id + "\">&nbsp;</a>"
            #// translators: %s: Plugin name.
            content += "<h2>" + php_sprintf(__("Source: %s"), plugin_name) + "</h2>"
            content += removed
            content += "<div class=\"policy-text\">" + section["policy_text"] + "</div>"
            content += return_to_top
            if php_empty(lambda : section["removed"]):
                content += "<div class=\"privacy-text-actions\">"
                content += "<button type=\"button\" class=\"privacy-text-copy button\">"
                content += copy
                content += "<span class=\"screen-reader-text\">"
                #// translators: %s: Plugin name.
                content += php_sprintf(__("Copy suggested policy text from %s."), plugin_name)
                content += "</span>"
                content += "</button>"
                content += "</div>"
            # end if
            content += "</div>\n"
            pass
        # end for
        if php_count(toc) > 2:
            php_print("         <div  class=\"privacy-text-box-toc\">\n             <p>")
            _e("Table of Contents")
            php_print("</p>\n               <ol>\n                  ")
            php_print(php_implode("\n", toc))
            php_print("             </ol>\n         </div>\n            ")
        # end if
        php_print("""       <div class=\"privacy-text-box\">
        <div class=\"privacy-text-box-head\">
        <a id=\"wp-privacy-policy-guide-introduction\">&nbsp;</a>
        <h2>""")
        _e("Introduction")
        php_print("</h2>\n              <p>")
        _e("Hello,")
        php_print("</p>\n               <p>")
        _e("This text template will help you to create your web site&#8217;s privacy policy.")
        php_print("</p>\n               <p>")
        _e("We have suggested the sections you will need. Under each section heading you will find a short summary of what information you should provide, which will help you to get started. Some sections include suggested policy content, others will have to be completed with information from your theme and plugins.")
        php_print("</p>\n               <p>")
        _e("Please edit your privacy policy content, making sure to delete the summaries, and adding any information from your theme and plugins. Once you publish your policy page, remember to add it to your navigation menu.")
        php_print("</p>\n               <p>")
        _e("It is your responsibility to write a comprehensive privacy policy, to make sure it reflects all national and international legal requirements on privacy, and to keep your policy current and accurate.")
        php_print("""</p>
        </div>
        <div class=\"privacy-text-box-body\">
        """)
        php_print(content)
        php_print("         </div>\n        </div>\n        ")
    # end def privacy_policy_guide
    #// 
    #// Return the default suggested privacy policy content.
    #// 
    #// @since 4.9.6
    #// @since 5.0.0 Added the `$blocks` parameter.
    #// 
    #// @param bool $description Whether to include the descriptions under the section headings. Default false.
    #// @param bool $blocks      Whether to format the content for the block editor. Default true.
    #// @return string The default policy content.
    #//
    @classmethod
    def get_default_content(self, description=False, blocks=True):
        
        suggested_text = "<strong class=\"privacy-policy-tutorial\">" + __("Suggested text:") + " </strong>" if description else ""
        content = ""
        strings = Array()
        #// Start of the suggested privacy policy text.
        if description:
            strings[-1] = "<div class=\"wp-suggested-text\">"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("Who we are") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should note your site URL, as well as the name of the company, organization, or individual behind it, and some accurate contact information.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("The amount of information you may be required to show will vary depending on your local or national business regulations. You may, for example, be required to display a physical address, a registered address, or your company registration number.") + "</p>"
        # end if
        #// translators: Default privacy policy text. %s: Site URL.
        strings[-1] = "<p>" + suggested_text + php_sprintf(__("Our website address is: %s."), get_bloginfo("url", "display")) + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("What personal data we collect and why we collect it") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should note what personal data you collect from users and site visitors. This may include personal data, such as name, email address, personal account preferences; transactional data, such as purchase information; and technical data, such as information about cookies.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("You should also note any collection and retention of sensitive personal data, such as data concerning health.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In addition to listing what personal data you collect, you need to note why you collect it. These explanations must note either the legal basis for your data collection and retention or the active consent the user has given.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("Personal data is not just created by a user&#8217;s interactions with your site. Personal data is also generated from technical processes such as contact forms, comments, cookies, analytics, and third party embeds.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("By default WordPress does not collect any personal data about visitors, and only collects the data shown on the User Profile screen from registered users. However some of your plugins may collect personal data. You should add the relevant information below.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("Comments") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this subsection you should note what information is captured through comments. We have noted the data which WordPress collects by default.") + "</p>"
        # end if
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + suggested_text + __("When visitors leave comments on the site we collect the data shown in the comments form, and also the visitor&#8217;s IP address and browser user agent string to help spam detection.") + "</p>"
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + __("An anonymized string created from your email address (also called a hash) may be provided to the Gravatar service to see if you are using it. The Gravatar service privacy policy is available here: https://automattic.com/privacy/. After approval of your comment, your profile picture is visible to the public in the context of your comment.") + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("Media") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this subsection you should note what information may be disclosed by users who can upload media files. All uploaded files are usually publicly accessible.") + "</p>"
        # end if
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + suggested_text + __("If you upload images to the website, you should avoid uploading images with embedded location data (EXIF GPS) included. Visitors to the website can download and extract any location data from images on the website.") + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("Contact forms") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("By default, WordPress does not include a contact form. If you use a contact form plugin, use this subsection to note what personal data is captured when someone submits a contact form, and how long you keep it. For example, you may note that you keep contact form submissions for a certain period for customer service purposes, but you do not use the information submitted through them for marketing purposes.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("Cookies") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this subsection you should list the cookies your web site uses, including those set by your plugins, social media, and analytics. We have provided the cookies which WordPress installs by default.") + "</p>"
        # end if
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + suggested_text + __("If you leave a comment on our site you may opt-in to saving your name, email address and website in cookies. These are for your convenience so that you do not have to fill in your details again when you leave another comment. These cookies will last for one year.") + "</p>"
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + __("If you visit our login page, we will set a temporary cookie to determine if your browser accepts cookies. This cookie contains no personal data and is discarded when you close your browser.") + "</p>"
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + __("When you log in, we will also set up several cookies to save your login information and your screen display choices. Login cookies last for two days, and screen options cookies last for a year. If you select &quot;Remember Me&quot;, your login will persist for two weeks. If you log out of your account, the login cookies will be removed.") + "</p>"
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + __("If you edit or publish an article, an additional cookie will be saved in your browser. This cookie includes no personal data and simply indicates the post ID of the article you just edited. It expires after 1 day.") + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("Embedded content from other websites") + "</h3>"
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + suggested_text + __("Articles on this site may include embedded content (e.g. videos, images, articles, etc.). Embedded content from other websites behaves in the exact same way as if the visitor has visited the other website.") + "</p>"
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + __("These websites may collect data about you, use cookies, embed additional third-party tracking, and monitor your interaction with that embedded content, including tracking your interaction with the embedded content if you have an account and are logged in to that website.") + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("Analytics") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this subsection you should note what analytics package you use, how users can opt out of analytics tracking, and a link to your analytics provider&#8217;s privacy policy, if any.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("By default WordPress does not collect any analytics data. However, many web hosting accounts collect some anonymous analytics data. You may also have installed a WordPress plugin that provides analytics services. In that case, add information from that plugin here.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("Who we share your data with") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should name and list all third party providers with whom you share site data, including partners, cloud-based services, payment processors, and third party service providers, and note what data you share with them and why. Link to their own privacy policies if possible.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("By default WordPress does not share any personal data with anyone.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("How long we retain your data") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should explain how long you retain personal data collected or processed by the web site. While it is your responsibility to come up with the schedule of how long you keep each dataset for and why you keep it, that information does need to be listed here. For example, you may want to say that you keep contact form entries for six months, analytics records for a year, and customer purchase records for ten years.") + "</p>"
        # end if
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + suggested_text + __("If you leave a comment, the comment and its metadata are retained indefinitely. This is so we can recognize and approve any follow-up comments automatically instead of holding them in a moderation queue.") + "</p>"
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + __("For users that register on our website (if any), we also store the personal information they provide in their user profile. All users can see, edit, or delete their personal information at any time (except they cannot change their username). Website administrators can also see and edit that information.") + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("What rights you have over your data") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should explain what rights your users have over their data and how they can invoke those rights.") + "</p>"
        # end if
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + suggested_text + __("If you have an account on this site, or have left comments, you can request to receive an exported file of the personal data we hold about you, including any data you have provided to us. You can also request that we erase any personal data we hold about you. This does not include any data we are obliged to keep for administrative, legal, or security purposes.") + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("Where we send your data") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should list all transfers of your site data outside the European Union and describe the means by which that data is safeguarded to European data protection standards. This could include your web hosting, cloud storage, or other third party services.") + "</p>"
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("European data protection law requires data about European residents which is transferred outside the European Union to be safeguarded to the same standards as if the data was in Europe. So in addition to listing where data goes, you should describe how you ensure that these standards are met either by yourself or by your third party providers, whether that is through an agreement such as Privacy Shield, model clauses in your contracts, or binding corporate rules.") + "</p>"
        # end if
        #// translators: Default privacy policy text.
        strings[-1] = "<p>" + suggested_text + __("Visitor comments may be checked through an automated spam detection service.") + "</p>"
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("Your contact information") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should provide a contact method for privacy-specific concerns. If you are required to have a Data Protection Officer, list their name and full contact details here as well.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h2>" + __("Additional information") + "</h2>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("If you use your site for commercial purposes and you engage in more complex collection or processing of personal data, you should note the following information in your privacy policy in addition to the information we have already discussed.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("How we protect your data") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should explain what measures you have taken to protect your users&#8217; data. This could include technical measures such as encryption; security measures such as two factor authentication; and measures such as staff training in data protection. If you have carried out a Privacy Impact Assessment, you can mention it here too.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("What data breach procedures we have in place") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("In this section you should explain what procedures you have in place to deal with data breaches, either potential or real, such as internal reporting systems, contact mechanisms, or bug bounties.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("What third parties we receive data from") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("If your web site receives data about users from third parties, including advertisers, this information must be included within the section of your privacy policy dealing with third party data.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("What automated decision making and/or profiling we do with user data") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("If your web site provides a service which includes automated decision making - for example, allowing customers to apply for credit, or aggregating their data into an advertising profile - you must note that this is taking place, and include information about how that information is used, what decisions are made with that aggregated data, and what rights users have over decisions made without human intervention.") + "</p>"
        # end if
        #// translators: Default privacy policy heading.
        strings[-1] = "<h3>" + __("Industry regulatory disclosure requirements") + "</h3>"
        if description:
            #// translators: Privacy policy tutorial.
            strings[-1] = "<p class=\"privacy-policy-tutorial\">" + __("If you are a member of a regulated industry, or if you are subject to additional privacy laws, you may be required to disclose that information here.") + "</p>"
            strings[-1] = "</div>"
        # end if
        if blocks:
            for key,string in strings:
                if 0 == php_strpos(string, "<p>"):
                    strings[key] = "<!-- wp:paragraph -->" + string + "<!-- /wp:paragraph -->"
                # end if
                if 0 == php_strpos(string, "<h2>"):
                    strings[key] = "<!-- wp:heading -->" + string + "<!-- /wp:heading -->"
                # end if
                if 0 == php_strpos(string, "<h3>"):
                    strings[key] = "<!-- wp:heading {\"level\":3} -->" + string + "<!-- /wp:heading -->"
                # end if
            # end for
        # end if
        content = php_implode("", strings)
        #// End of the suggested privacy policy text.
        #// 
        #// Filters the default content suggested for inclusion in a privacy policy.
        #// 
        #// @since 4.9.6
        #// @since 5.0.0 Added the `$strings`, `$description`, and `$blocks` parameters.
        #// 
        #// @param string   $content     The default policy content.
        #// @param string[] $strings     An array of privacy policy content strings.
        #// @param bool     $description Whether policy descriptions should be included.
        #// @param bool     $blocks      Whether the content should be formatted for the block editor.
        #//
        return apply_filters("wp_get_default_privacy_policy_content", content, strings, description, blocks)
    # end def get_default_content
    #// 
    #// Add the suggested privacy policy text to the policy postbox.
    #// 
    #// @since 4.9.6
    #//
    @classmethod
    def add_suggested_content(self):
        
        content = self.get_default_content(True, False)
        wp_add_privacy_policy_content(__("WordPress"), content)
    # end def add_suggested_content
# end class WP_Privacy_Policy_Content
